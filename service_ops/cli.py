from __future__ import annotations

import argparse
import asyncio
import json
from collections.abc import Sequence

from service_ops.health import print_checks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m service_ops")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="ตรวจ Codespace, Azure CLI และ .env")
    check_parser.add_argument("--bootstrap", action="store_true", help=argparse.SUPPRESS)
    check_parser.add_argument(
        "--strict", action="store_true", help="ให้ ACTION ทำให้คำสั่งคืนสถานะไม่สำเร็จ"
    )

    agent_parser = subparsers.add_parser("agent", help="สนทนากับ Service Operations Agent")
    agent_parser.add_argument("--prompt", help="ส่งคำถามหนึ่งครั้งแทน interactive mode")
    agent_mode = agent_parser.add_mutually_exclusive_group()
    agent_mode.add_argument(
        "--iq", action="store_true", help="ใช้ portal-managed Foundry IQ agent"
    )
    agent_mode.add_argument(
        "--escalation",
        action="store_true",
        help="ใช้ code-first agent และ simulated escalation tool",
    )

    mcp_server_parser = subparsers.add_parser("mcp-server", help="เริ่ม local MCP server")
    mcp_server_parser.add_argument("--host", default="127.0.0.1")
    mcp_server_parser.add_argument("--port", default=8000, type=int)

    mcp_agent_parser = subparsers.add_parser("mcp-agent", help="ถาม MCP-enabled agent")
    mcp_agent_parser.add_argument("--source", choices=("learn", "local"), default="local")
    mcp_agent_parser.add_argument("--prompt", required=True)

    workflow_parser = subparsers.add_parser("workflow", help="ทดสอบ ticket-triage workflow")
    workflow_parser.add_argument("--mode", choices=("local", "foundry"), default="local")

    multi_agent_parser = subparsers.add_parser(
        "multi-agent", help="รัน summarizer, classifier และ resolver ตามลำดับ"
    )
    multi_agent_parser.add_argument("--feedback", required=True)
    return parser


async def _run_agent(prompt: str | None, *, iq: bool, escalation: bool) -> int:
    if iq:
        from service_ops.foundry_iq import ask_foundry_iq as ask
        from service_ops.foundry_iq import build_foundry_iq_agent as build
    elif escalation:
        from service_ops.escalation import ask_escalation_agent as ask
        from service_ops.escalation import build_escalation_agent as build
    else:
        from service_ops.agent import ask_agent as ask
        from service_ops.agent import build_agent as build

    try:
        if prompt:
            print(await ask(prompt))
            return 0

        agent = build()
        print("Service Operations Agent พร้อมแล้ว พิมพ์ exit เพื่อจบ")
        while True:
            question = input("You: ").strip()
            if question.lower() in {"exit", "quit"}:
                return 0
            if question:
                print(f"Agent: {await ask(question, agent=agent)}")
    except (NotImplementedError, ValueError) as error:
        print(f"ACTION: {error}")
        return 2


async def _run_mcp_agent(prompt: str, source: str) -> int:
    from service_ops.mcp_agent import ask_with_mcp

    try:
        print(await ask_with_mcp(prompt, source))  # type: ignore[arg-type]
        return 0
    except (NotImplementedError, ValueError) as error:
        print(f"ACTION: {error}")
        return 2


async def _run_multi_agent(feedback: str) -> int:
    from service_ops.multi_agent import run_multi_agent

    try:
        print(await run_multi_agent(feedback))
        return 0
    except (NotImplementedError, ValueError) as error:
        print(f"ACTION: {error}")
        return 2


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "check":
        return print_checks(bootstrap=args.bootstrap, strict=args.strict)
    if args.command == "agent":
        return asyncio.run(_run_agent(args.prompt, iq=args.iq, escalation=args.escalation))
    if args.command == "mcp-server":
        from service_ops.mcp_server import run_server

        try:
            run_server(host=args.host, port=args.port)
            return 0
        except KeyboardInterrupt:
            print("\nLocal MCP server stopped.")
            return 0
        except (NotImplementedError, ValueError) as error:
            print(f"ACTION: {error}")
            return 2
    if args.command == "mcp-agent":
        return asyncio.run(_run_mcp_agent(args.prompt, args.source))
    if args.command == "workflow":
        from service_ops.workflow import invoke_foundry_workflow, run_local_workflow

        try:
            result = (
                invoke_foundry_workflow()
                if args.mode == "foundry"
                else json.dumps(run_local_workflow(), ensure_ascii=False, indent=2)
            )
            print(result)
            return 0
        except (NotImplementedError, ValueError) as error:
            print(f"ACTION: {error}")
            return 2
    if args.command == "multi-agent":
        return asyncio.run(_run_multi_agent(args.feedback))
    if args.command is None:
        return 0
    raise AssertionError(f"Unhandled command: {args.command}")
