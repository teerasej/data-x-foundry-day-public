from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential

from service_ops.config import REPOSITORY_ROOT, Settings

TICKET_FILE = REPOSITORY_ROOT / "exercises/05-build-foundry-workflow/files/service-tickets.json"
FOUNDRY_WORKFLOW_NAME = "fabrikam-service-ticket-triage"


@dataclass(frozen=True)
class TicketRoute:
    ticket_id: str
    category: str
    confidence: float
    route: str
    recommendation: str


def load_tickets(path: Path = TICKET_FILE) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))["tickets"]


def route_ticket(ticket: dict[str, Any]) -> TicketRoute:
    """Provide a deterministic offline fallback for the preview visual workflow."""
    description = ticket["description"].casefold()
    if any(term in description for term in ("403", "api", "error", "timeout")):
        category, confidence = "Technical", 0.91
    elif any(term in description for term in ("charged", "refund", "billing")):
        category, confidence = "Billing", 0.93
    elif len(description.split()) < 6:
        category, confidence = "General", 0.55
    else:
        category, confidence = "General", 0.82

    if confidence <= 0.6:
        route = "request-more-information"
        recommendation = "Ask the requester for the affected service and exact symptom."
    elif category == "Billing":
        route = "human-escalation"
        recommendation = "Escalate to a human billing specialist; do not promise a refund."
    else:
        route = "automated-response"
        recommendation = "Draft a concise response from approved service guidance."

    return TicketRoute(ticket["ticket_id"], category, confidence, route, recommendation)


def run_local_workflow(path: Path = TICKET_FILE) -> list[dict[str, Any]]:
    return [asdict(route_ticket(ticket)) for ticket in load_tickets(path)]


def invoke_foundry_workflow(
    settings: Settings | None = None,
    *,
    workflow_name: str = FOUNDRY_WORKFLOW_NAME,
    credential_factory: Callable[[], Any] = AzureCliCredential,
    project_client_factory: Callable[..., Any] = AIProjectClient,
) -> str:
    """Invoke the saved visual workflow. Complete this function in Exercise 5."""
    settings = settings or Settings.from_environment()
    settings.require_chat_agent()
    # TODO Exercise 5: invoke the saved workflow through the project OpenAI client.
    del workflow_name, credential_factory, project_client_factory
    raise NotImplementedError(
        "Complete invoke_foundry_workflow() by following Exercise 5, Practice 3."
    )
