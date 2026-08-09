from service_ops.config import Settings


def test_settings_detect_missing_chat_values() -> None:
    settings = Settings.from_environment(env={})
    assert settings.missing_for_chat_agent() == (
        "FOUNDRY_PROJECT_ENDPOINT",
        "FOUNDRY_MODEL",
    )


def test_settings_accept_configured_chat_values() -> None:
    settings = Settings.from_environment(
        env={
            "FOUNDRY_PROJECT_ENDPOINT": "https://example.services.ai.azure.com/api/projects/demo",
            "FOUNDRY_MODEL": "approved-model",
        }
    )
    assert settings.missing_for_chat_agent() == ()
