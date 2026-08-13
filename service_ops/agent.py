from __future__ import annotations

from collections.abc import Callable
from typing import Any

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

from service_ops.config import Settings
from service_ops.data_tools import list_service_metrics, search_service_handbook

AGENT_INSTRUCTIONS = """
You are the Fabrikam Service Operations Agent.

- Answer service-policy questions using search_service_handbook.
- Analyze operational performance using list_service_metrics.
- State which synthetic source or tool you used.
- Never invent a policy, metric, customer, incident, or production fact.
- If the supplied data is insufficient, say what is missing and recommend human review.
- Keep the answer concise and practical.
""".strip()


def build_agent(
    settings: Settings | None = None,
    *,
    credential_factory: Callable[[], Any] = AzureCliCredential,
    client_factory: Callable[..., Any] = FoundryChatClient,
    agent_factory: Callable[..., Any] = Agent,
) -> Any:
    """Build the code-owned service agent. Complete this function in Exercise 2."""
    settings = settings or Settings.from_environment()
    settings.require_chat_agent()

    # TODO Exercise 2: create AzureCliCredential, FoundryChatClient, and Agent.
    # Add search_service_handbook and list_service_metrics as local function tools.
    del credential_factory, client_factory, agent_factory
    raise NotImplementedError("Complete build_agent() by following Exercise 2, Practice 2.")


async def ask_agent(prompt: str, *, agent: Any | None = None) -> str:
    active_agent = agent or build_agent()
    result = await active_agent.run(prompt)
    text = getattr(result, "text", None)
    return text if text is not None else str(result)
