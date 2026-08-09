import pytest

from service_ops.agent import build_agent
from service_ops.config import Settings


def test_starter_requires_learner_to_complete_build_agent() -> None:
    settings = Settings(
        foundry_project_endpoint="https://example.services.ai.azure.com/api/projects/demo",
        foundry_model="approved-model",
    )
    with pytest.raises(NotImplementedError, match="Exercise 2"):
        build_agent(settings)
