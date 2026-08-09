from service_ops.cli import FUTURE_COMMANDS, main


def test_future_commands_are_visible_but_non_blocking(capsys) -> None:
    for command in FUTURE_COMMANDS:
        assert main([command]) == 0
    output = capsys.readouterr().out
    assert "Review Gate" in output
