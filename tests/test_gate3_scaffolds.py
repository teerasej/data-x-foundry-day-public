import pytest

from service_ops.config import Settings
from service_ops.escalation import build_escalation_agent, create_escalation
from service_ops.foundry_iq import build_foundry_iq_agent
from service_ops.mcp_agent import build_mcp_agent
from service_ops.mcp_server import create_mcp_server, find_service_status, summarize_queue
from service_ops.multi_agent import build_multi_agent_workflow
from service_ops.workflow import invoke_foundry_workflow, run_local_workflow

CHAT_SETTINGS = Settings(
    foundry_project_endpoint="https://example.services.ai.azure.com/api/projects/demo",
    foundry_model="approved-model",
)
MANAGED_SETTINGS = Settings(
    foundry_project_endpoint="https://example.services.ai.azure.com/api/projects/demo",
    foundry_agent_name="fabrikam-iq-agent",
    foundry_agent_version="1",
    foundry_iq_mcp_endpoint="https://example.search.windows.net/knowledgebases/demo/mcp",
)


@pytest.mark.parametrize(
    ("builder", "args"),
    [
        (create_mcp_server, ()),
        (build_mcp_agent, ("local", CHAT_SETTINGS)),
        (build_foundry_iq_agent, (MANAGED_SETTINGS,)),
        (invoke_foundry_workflow, (CHAT_SETTINGS,)),
        (build_escalation_agent, (CHAT_SETTINGS,)),
        (build_multi_agent_workflow, (CHAT_SETTINGS,)),
    ],
)
def test_gate3_starter_marks_each_learner_implementation(builder, args) -> None:
    with pytest.raises(NotImplementedError, match="Exercise"):
        builder(*args)


def test_mcp_sample_helpers_are_deterministic() -> None:
    assert find_service_status("customer portal")["status"] == "degraded"
    assert summarize_queue()["waiting_requests"] == 14


def test_simulated_escalation_is_stable_and_side_effect_free() -> None:
    first = create_escalation("SR-2001", "Complete outage", "high")
    second = create_escalation("SR-2001", "Complete outage", "high")
    assert first == second
    assert first["status"] == "simulated-only"


def test_local_workflow_routes_all_three_paths() -> None:
    routes = {item["route"] for item in run_local_workflow()}
    assert routes == {
        "automated-response",
        "human-escalation",
        "request-more-information",
    }
