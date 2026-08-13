from __future__ import annotations

from collections.abc import Callable
from typing import Any

from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import SequentialBuilder
from azure.identity import AzureCliCredential

from service_ops.config import Settings

SUMMARIZER_INSTRUCTIONS = """
Summarize the service request in one neutral sentence. Preserve the request ID and key symptom.
Do not classify or recommend an action.
""".strip()

CLASSIFIER_INSTRUCTIONS = """
Classify the summarized request as Billing, Technical, General, or Positive feedback.
Return the category and a confidence from 0 to 1. Do not recommend an action.
""".strip()

RESOLVER_INSTRUCTIONS = """
Use the full conversation to recommend exactly one next action.
Billing goes to human review. Technical receives safe troubleshooting.
Low confidence asks for details.
Never promise a refund or claim that an external ticket was created.
""".strip()


def build_multi_agent_workflow(
    settings: Settings | None = None,
    *,
    credential_factory: Callable[[], Any] = AzureCliCredential,
    client_factory: Callable[..., Any] = FoundryChatClient,
    builder_factory: Callable[..., Any] = SequentialBuilder,
) -> Any:
    """Build the sequential workflow. Complete this function in Exercise 7."""
    settings = settings or Settings.from_environment()
    settings.require_chat_agent()
    # TODO Exercise 7: create three agents and build the sequential orchestration.
    del credential_factory, client_factory, builder_factory
    raise NotImplementedError(
        "Complete build_multi_agent_workflow() by following Exercise 7, Practice 1."
    )


async def run_multi_agent(prompt: str, *, workflow: Any | None = None) -> str:
    active_workflow = workflow or build_multi_agent_workflow()
    events = await active_workflow.run(prompt)
    outputs = events.get_outputs()
    if not outputs:
        return "No workflow output was produced."
    final = outputs[-1]
    text = getattr(final, "text", None)
    if text:
        return text
    messages = getattr(final, "messages", ())
    return "\n".join(message.text for message in messages if getattr(message, "text", None))
