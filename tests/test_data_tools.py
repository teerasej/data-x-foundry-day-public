import json

from service_ops.data_tools import list_service_metrics, search_service_handbook


def test_handbook_search_returns_priority_section() -> None:
    result = search_service_handbook("company-wide outage priority acknowledgement")
    assert "P1" in result
    assert "15 minutes" in result


def test_handbook_search_handles_unknown_topic() -> None:
    result = search_service_handbook("penguin habitat")
    assert result.startswith("No matching handbook section")


def test_metrics_are_deterministic_and_synthetic() -> None:
    metrics = json.loads(list_service_metrics())
    by_name = {item["metric"]: item for item in metrics}
    assert by_name["resolution_rate_percent"]["status_note"] == "below_target"
    assert by_name["open_p1_incidents"]["value"] == "1"
