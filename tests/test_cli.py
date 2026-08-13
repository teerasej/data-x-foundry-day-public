from service_ops.cli import build_parser, main


def test_all_workshop_commands_are_registered() -> None:
    parser = build_parser()
    help_text = parser.format_help()
    for command in (
        "check",
        "agent",
        "mcp-server",
        "mcp-agent",
        "workflow",
        "workflow-framework",
        "multi-agent",
    ):
        assert command in help_text


def test_local_workflow_command_is_deterministic(capsys) -> None:
    assert main(["workflow"]) == 0
    output = capsys.readouterr().out
    assert '"ticket_id": "SR-1001"' in output
    assert '"route": "human-escalation"' in output


def test_framework_workflow_diagram_command(capsys, monkeypatch) -> None:
    monkeypatch.setattr(
        "service_ops.framework_workflow.render_workflow_mermaid",
        lambda: "flowchart TD\n  triage --> route",
    )

    assert main(["workflow-framework", "--diagram"]) == 0
    output = capsys.readouterr().out
    assert "flowchart TD" in output
