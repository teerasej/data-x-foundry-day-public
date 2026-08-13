from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from service_ops.framework_workflow import (
    TicketDecision,
    TriageResponse,
    needs_billing_review,
    needs_more_information,
    run_framework_workflow,
)
from service_ops.workflow import TicketRoute, load_tickets


def test_triage_response_validates_category_and_confidence() -> None:
    with pytest.raises(ValidationError):
        TriageResponse(ticket_id="SR-1", category="Unknown", confidence=0.8)
    with pytest.raises(ValidationError):
        TriageResponse(ticket_id="SR-1", category="General", confidence=1.1)


def test_route_predicates_keep_low_confidence_first() -> None:
    uncertain_billing = TicketDecision("SR-1", "Billing help", "Billing", 0.6)
    confident_billing = TicketDecision("SR-2", "Charged twice", "Billing", 0.9)

    assert needs_more_information(uncertain_billing)
    assert not needs_billing_review(uncertain_billing)
    assert not needs_more_information(confident_billing)
    assert needs_billing_review(confident_billing)


class _FakeRunResult:
    def __init__(self, output: TicketRoute) -> None:
        self.output = output

    def get_outputs(self) -> list[TicketRoute]:
        return [self.output]


class _FakeWorkflow:
    def __init__(self) -> None:
        self.ticket_ids: list[str] = []

    async def run(self, ticket: dict[str, Any]) -> _FakeRunResult:
        self.ticket_ids.append(ticket["ticket_id"])
        return _FakeRunResult(
            TicketRoute(
                ticket_id=ticket["ticket_id"],
                category="General",
                confidence=0.5,
                route="request-more-information",
                recommendation="Ask for details.",
            )
        )


async def test_framework_runner_processes_each_ticket_once() -> None:
    workflow = _FakeWorkflow()

    routes = await run_framework_workflow(workflow=workflow)

    expected_ids = [ticket["ticket_id"] for ticket in load_tickets()]
    assert workflow.ticket_ids == expected_ids
    assert [route["ticket_id"] for route in routes] == expected_ids
    assert all(route["route"] == "request-more-information" for route in routes)