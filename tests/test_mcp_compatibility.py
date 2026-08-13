import asyncio
from importlib.metadata import version

import pytest
import uvicorn
from agent_framework import MCPStreamableHTTPTool
from mcp.server.fastmcp import FastMCP
from mcp.types import InitializeResult

from scripts.validate_repository import check_dependency_lock
from service_ops.health import _mcp_compatibility_check


def test_mcp_v1_contract_and_direct_dependency_lock() -> None:
    assert version("mcp") == "1.29.0"
    assert "protocolVersion" in InitializeResult.model_fields
    assert check_dependency_lock() == []


def test_health_check_reports_compatible_mcp() -> None:
    result = _mcp_compatibility_check()
    assert result.level == "READY"
    assert result.detail == "mcp 1.29.0 with v1 schema"


@pytest.mark.asyncio
async def test_agent_framework_connects_to_local_fastmcp(unused_tcp_port: int) -> None:
    server = FastMCP(
        name="compatibility-test",
        host="127.0.0.1",
        port=unused_tcp_port,
        streamable_http_path="/mcp",
        json_response=True,
        stateless_http=True,
    )

    @server.tool()
    def echo_status(service_name: str) -> dict[str, str]:
        return {"service": service_name, "status": "synthetic-ok"}

    uvicorn_server = uvicorn.Server(
        uvicorn.Config(
            server.streamable_http_app(),
            host="127.0.0.1",
            port=unused_tcp_port,
            log_level="warning",
        )
    )
    server_task = asyncio.create_task(uvicorn_server.serve())
    try:
        for _ in range(100):
            if uvicorn_server.started:
                break
            await asyncio.sleep(0.01)
        assert uvicorn_server.started

        tool = MCPStreamableHTTPTool(
            name="local-test",
            url=f"http://127.0.0.1:{unused_tcp_port}/mcp",
            approval_mode="never_require",
        )
        await tool.connect()
        try:
            result = await tool.call_tool("echo_status", service_name="portal")
        finally:
            await tool.close()

        serialized_result = str(
            [content.to_dict() if hasattr(content, "to_dict") else content for content in result]
        )
        assert "synthetic-ok" in serialized_result
    finally:
        uvicorn_server.should_exit = True
        await server_task