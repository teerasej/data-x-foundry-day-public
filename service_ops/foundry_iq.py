from __future__ import annotations

from collections.abc import Callable
from typing import Any

from agent_framework.foundry import FoundryAgent
from azure.identity import AzureCliCredential

from service_ops.config import Settings


def build_foundry_iq_agent(
    settings: Settings | None = None,
    *,
    credential_factory: Callable[[], Any] = AzureCliCredential,
    agent_factory: Callable[..., Any] = FoundryAgent,
) -> Any:
    """Connect to the portal-managed Foundry IQ agent. Complete this in Exercise 4."""
    settings = settings or Settings.from_environment()
    settings.require_managed_agent()

    # TODO Exercise 4: create FoundryAgent with project endpoint, name, version and CLI credential.
    del credential_factory, agent_factory
    raise NotImplementedError(
        "Complete build_foundry_iq_agent() by following Exercise 4, Practice 3."
    )


async def ask_foundry_iq(prompt: str, *, agent: Any | None = None) -> str:
    active_agent = agent or build_foundry_iq_agent()
    result = await active_agent.run(prompt)
    return getattr(result, "text", str(result))
