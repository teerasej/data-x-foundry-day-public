from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal

from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

from service_ops.config import Settings

MCPSource = Literal["learn", "local"]
MICROSOFT_LEARN_MCP_ENDPOINT = "https://learn.microsoft.com/api/mcp"

MCP_AGENT_INSTRUCTIONS = """
You are the Fabrikam Service Operations Agent with MCP tools.
Use the MCP tools when the answer depends on Microsoft documentation
or the synthetic service snapshot.
Name the MCP source you used. Never present synthetic service data as production data.
If a tool cannot answer, say what is missing and recommend human review.
""".strip()


def build_mcp_agent(
    source: MCPSource,
    settings: Settings | None = None,
    *,
    credential_factory: Callable[[], Any] = AzureCliCredential,
    client_factory: Callable[..., Any] = FoundryChatClient,
    tool_factory: Callable[..., Any] = MCPStreamableHTTPTool,
    agent_factory: Callable[..., Any] = Agent,
) -> Any:
    """Build an MCP-enabled agent. Complete this function in Exercise 3."""
    settings = settings or Settings.from_environment()
    settings.require_chat_agent()

    # TODO Exercise 3: choose the trusted endpoint, create the MCP tool and create the Agent.
    del source, credential_factory, client_factory, tool_factory, agent_factory
    raise NotImplementedError("Complete build_mcp_agent() by following Exercise 3.")


async def ask_with_mcp(prompt: str, source: MCPSource, *, agent: Any | None = None) -> str:
    if agent is not None:
        result = await agent.run(prompt)
        return getattr(result, "text", str(result))

    active_agent = build_mcp_agent(source)
    async with active_agent:
        result = await active_agent.run(prompt)
    return getattr(result, "text", str(result))
