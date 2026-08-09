from __future__ import annotations

import argparse
import asyncio
from collections.abc import Sequence

from service_ops.health import print_checks

FUTURE_COMMANDS = {
    "mcp-server": "Exercise 3 จะเพิ่ม local MCP server ใน Review Gate ถัดไป",
    "mcp-agent": "Exercise 3 จะเพิ่ม MCP-enabled agent ใน Review Gate ถัดไป",
    "workflow": "Exercise 5 จะเพิ่ม workflow command ใน Review Gate ถัดไป",
    "multi-agent": "Exercise 7 จะเพิ่ม multi-agent command ใน Review Gate ถัดไป",
}


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

    for command in FUTURE_COMMANDS:
        subparsers.add_parser(command)
    return parser


async def _run_agent(prompt: str | None) -> int:
    from service_ops.agent import ask_agent, build_agent

    try:
        if prompt:
            print(await ask_agent(prompt))
            return 0

        agent = build_agent()
        print("Service Operations Agent พร้อมแล้ว พิมพ์ exit เพื่อจบ")
        while True:
            question = input("You: ").strip()
            if question.lower() in {"exit", "quit"}:
                return 0
            if question:
                print(f"Agent: {await ask_agent(question, agent=agent)}")
    except (NotImplementedError, ValueError) as error:
        print(f"ACTION: {error}")
        return 2


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "check":
        return print_checks(bootstrap=args.bootstrap, strict=args.strict)
    if args.command == "agent":
        return asyncio.run(_run_agent(args.prompt))
    if args.command in FUTURE_COMMANDS:
        print(FUTURE_COMMANDS[args.command])
        return 0
    raise AssertionError(f"Unhandled command: {args.command}")
