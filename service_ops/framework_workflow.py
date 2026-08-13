from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal, Never

from agent_framework import (
    AgentExecutor,
    AgentExecutorRequest,
    AgentExecutorResponse,
    Case,
    Default,
    Message,
    WorkflowBuilder,
    WorkflowContext,
    WorkflowViz,
    executor,
)
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from pydantic import BaseModel, Field

from service_ops.config import Settings
from service_ops.workflow import TICKET_FILE, TicketRoute, load_tickets

TRIAGE_INSTRUCTIONS = """
Classify each synthetic Fabrikam service ticket as exactly Billing, Technical, or General.
Return its ticket ID and a confidence from 0 to 1.
Billing means an incorrect charge, refund, or payment.
Technical means an API error, timeout, integration, or system failure.
General means a how-to, navigation, report, or unclear request.
A short request with missing context must have confidence 0.6 or lower.
Return only the configured structured response.
""".strip()

RESOLUTION_INSTRUCTIONS = """
Draft one concise and safe response for a synthetic service ticket.
For Technical, suggest one or two high-level troubleshooting checks.
For General, explain the next information or navigation step.
Never request credentials or production customer data.
Do not claim that an external action was completed.
Return only the configured structured response.
""".strip()

CURRENT_TICKET_KEY = "current_ticket"
CURRENT_DECISION_KEY = "current_decision"


class TriageResponse(BaseModel):
    ticket_id: str
    category: Literal["Billing", "Technical", "General"]
    confidence: float = Field(ge=0, le=1)


class ResolutionResponse(BaseModel):
    recommendation: str


@dataclass(frozen=True)
class TicketDecision:
    ticket_id: str
    description: str
    category: str
    confidence: float


def needs_more_information(decision: TicketDecision) -> bool:
    return decision.confidence <= 0.6


def needs_billing_review(decision: TicketDecision) -> bool:
    return decision.confidence > 0.6 and decision.category == "Billing"


@executor(id="prepare_ticket")
async def prepare_ticket(
    ticket: dict[str, Any], ctx: WorkflowContext[AgentExecutorRequest]
) -> None:
    ticket_id = str(ticket["ticket_id"])
    description = str(ticket["description"])
    ctx.set_state(CURRENT_TICKET_KEY, {"ticket_id": ticket_id, "description": description})
    await ctx.send_message(
        AgentExecutorRequest(
            messages=[Message(role="user", contents=[f"{ticket_id}: {description}"])],
            should_respond=True,
        )
    )


@executor(id="parse_triage_response")
async def parse_triage_response(
    response: AgentExecutorResponse, ctx: WorkflowContext[TicketDecision]
) -> None:
    triage = TriageResponse.model_validate_json(response.agent_response.text)
    ticket: dict[str, str] = ctx.get_state(CURRENT_TICKET_KEY)
    if triage.ticket_id != ticket["ticket_id"]:
        raise ValueError(
            f"Triage returned {triage.ticket_id!r} for ticket {ticket['ticket_id']!r}."
        )
    await ctx.send_message(
        TicketDecision(
            ticket_id=ticket["ticket_id"],
            description=ticket["description"],
            category=triage.category,
            confidence=triage.confidence,
        )
    )


@executor(id="request_more_information")
async def request_more_information(
    decision: TicketDecision, ctx: WorkflowContext[Never, TicketRoute]
) -> None:
    await ctx.yield_output(
        TicketRoute(
            ticket_id=decision.ticket_id,
            category=decision.category,
            confidence=decision.confidence,
            route="request-more-information",
            recommendation="Ask the requester for the affected service and exact symptom.",
        )
    )


@executor(id="request_billing_review")
async def request_billing_review(
    decision: TicketDecision, ctx: WorkflowContext[Never, TicketRoute]
) -> None:
    await ctx.yield_output(
        TicketRoute(
            ticket_id=decision.ticket_id,
            category=decision.category,
            confidence=decision.confidence,
            route="human-escalation",
            recommendation="Escalate to a human billing specialist; do not promise a refund.",
        )
    )


@executor(id="prepare_resolution_request")
async def prepare_resolution_request(
    decision: TicketDecision, ctx: WorkflowContext[AgentExecutorRequest]
) -> None:
    ctx.set_state(CURRENT_DECISION_KEY, decision)
    await ctx.send_message(
        AgentExecutorRequest(
            messages=[
                Message(
                    role="user",
                    contents=[
                        f"Ticket {decision.ticket_id} is {decision.category}: "
                        f"{decision.description}"
                    ],
                )
            ],
            should_respond=True,
        )
    )


@executor(id="finalize_automated_response")
async def finalize_automated_response(
    response: AgentExecutorResponse, ctx: WorkflowContext[Never, TicketRoute]
) -> None:
    resolution = ResolutionResponse.model_validate_json(response.agent_response.text)
    decision: TicketDecision = ctx.get_state(CURRENT_DECISION_KEY)
    await ctx.yield_output(
        TicketRoute(
            ticket_id=decision.ticket_id,
            category=decision.category,
            confidence=decision.confidence,
            route="automated-response",
            recommendation=resolution.recommendation,
        )
    )


def build_ticket_workflow(
    settings: Settings | None = None,
    *,
    credential_factory: Callable[[], Any] = AzureCliCredential,
    client_factory: Callable[..., Any] = FoundryChatClient,
    agent_executor_factory: Callable[..., Any] = AgentExecutor,
    builder_factory: Callable[..., Any] = WorkflowBuilder,
) -> Any:
    """Build the optional Agent Framework routing graph for one ticket."""
    settings = settings or Settings.from_environment()
    settings.require_chat_agent()
    # TODO Exercise 5a: create the two agents and connect the typed routing graph.
    del credential_factory, client_factory, agent_executor_factory, builder_factory
    raise NotImplementedError(
        "Complete build_ticket_workflow() by following Exercise 5a, Practice 2."
    )


async def run_framework_workflow(
    path: Path = TICKET_FILE, *, workflow: Any | None = None
) -> list[dict[str, Any]]:
    active_workflow = workflow or build_ticket_workflow()
    routes: list[dict[str, Any]] = []
    for ticket in load_tickets(path):
        result = await active_workflow.run(ticket)
        outputs = result.get_outputs()
        if len(outputs) != 1 or not isinstance(outputs[0], TicketRoute):
            raise RuntimeError("Each ticket must produce exactly one TicketRoute output.")
        routes.append(asdict(outputs[0]))
    return routes


def render_workflow_mermaid(*, workflow: Any | None = None) -> str:
    active_workflow = workflow or build_ticket_workflow()
    return WorkflowViz(active_workflow).to_mermaid()