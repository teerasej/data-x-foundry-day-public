from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from service_ops.config import REPOSITORY_ROOT

SERVICE_STATUS_FILE = (
    REPOSITORY_ROOT / "exercises/03-extend-agent-with-mcp/files/service-status.json"
)


def load_service_status(path: Path = SERVICE_STATUS_FILE) -> dict[str, Any]:
    """Load the synthetic status snapshot used by the local MCP server."""
    return json.loads(path.read_text(encoding="utf-8"))


def find_service_status(service_name: str, path: Path = SERVICE_STATUS_FILE) -> dict[str, Any]:
    """Return one synthetic service record using case-insensitive matching."""
    normalized = service_name.strip().casefold()
    for service in load_service_status(path)["services"]:
        if service["name"].casefold() == normalized:
            return service
    return {
        "status": "not_found",
        "message": f"No synthetic status record exists for {service_name!r}.",
    }


def summarize_queue(path: Path = SERVICE_STATUS_FILE) -> dict[str, Any]:
    """Return the synthetic queue summary."""
    return load_service_status(path)["queue_summary"]


def create_mcp_server(*, host: str = "127.0.0.1", port: int = 8000) -> FastMCP:
    """Create the local MCP server. Complete this function in Exercise 3."""
    # TODO Exercise 3: create FastMCP and register both helper functions with @server.tool().
    del host, port
    raise NotImplementedError(
        "Complete create_mcp_server() by following Exercise 3, Practice 2."
    )


def run_server(*, host: str = "127.0.0.1", port: int = 8000) -> None:
    server = create_mcp_server(host=host, port=port)
    server.run(transport="streamable-http")
