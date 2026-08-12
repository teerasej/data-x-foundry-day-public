from service_ops.cli import build_parser, main


def test_all_workshop_commands_are_registered() -> None:
    parser = build_parser()
    help_text = parser.format_help()
    for command in ("check", "agent", "mcp-server", "mcp-agent", "workflow", "multi-agent"):
        assert command in help_text


def test_local_workflow_command_is_deterministic(capsys) -> None:
    assert main(["workflow"]) == 0
    output = capsys.readouterr().out
    assert '"ticket_id": "SR-1001"' in output
    assert '"route": "human-escalation"' in output
