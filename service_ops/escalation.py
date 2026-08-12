from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

from service_ops.config import REPOSITORY_ROOT, Settings

ESCALATION_FILE = (
    REPOSITORY_ROOT / "exercises/06-build-agent-framework-agent/files/escalation-request.json"
)


def load_escalation_request(path: Path = ESCALATION_FILE) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def create_escalation(
    request_id: str,
    reason: str,
    priority: Literal["low", "medium", "high"],
) -> dict[str, str]:
    """Simulate an escalation without writing to an external system."""
    digest = hashlib.sha256(f"{request_id}|{reason}|{priority}".encode()).hexdigest()[:8]
    return {
        "escalation_id": f"ESC-{digest.upper()}",
        "request_id": request_id,
        "priority": priority,
        "status": "simulated-only",
        "reason": reason,
    }


def build_escalation_agent(
    settings: Settings | None = None,
    *,
    credential_factory: Callable[[], Any] = AzureCliCredential,
    client_factory: Callable[..., Any] = FoundryChatClient,
    agent_factory: Callable[..., Any] = Agent,
) -> Any:
    """Build a code-first agent with the simulated tool. Complete this in Exercise 6."""
    settings = settings or Settings.from_environment()
    settings.require_chat_agent()
    # TODO Exercise 6: create the client and expose only create_escalation to the Agent.
    del credential_factory, client_factory, agent_factory
    raise NotImplementedError(
        "Complete build_escalation_agent() by following Exercise 6, Practice 2."
    )


async def ask_escalation_agent(prompt: str, *, agent: Any | None = None) -> str:
    active_agent = agent or build_escalation_agent()
    result = await active_agent.run(prompt)
    return getattr(result, "text", str(result))
