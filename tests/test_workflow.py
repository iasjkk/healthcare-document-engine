"""
Workflow orchestration smoke test.

Verifies that all workflow stages execute in the expected order.
"""

from __future__ import annotations

import asyncio

from framework.orchestrator.graph import HealthcareWorkflow


class MockAgent:
    """
    Minimal BaseAgent-like object used for workflow testing.
    """

    def __init__(
        self,
        name: str,
        calls: list[str],
    ) -> None:
        self.name = name
        self.calls = calls

    async def run(self, state):
        self.calls.append(self.name)
        return state


async def main() -> None:

    print("=" * 70)
    print("HEALTHCARE WORKFLOW TEST")
    print("=" * 70)

    calls: list[str] = []

    workflow = HealthcareWorkflow(
        entity_extraction_agent=MockAgent(
            "entity_extraction",
            calls,
        ),
        entity_normalization_agent=MockAgent(
            "entity_normalization",
            calls,
        ),
        entity_validation_agent=MockAgent(
            "entity_validation",
            calls,
        ),
        relation_extraction_agent=MockAgent(
            "relation_extraction",
            calls,
        ),
        relation_normalization_agent=MockAgent(
            "relation_normalization",
            calls,
        ),
        relation_validation_agent=MockAgent(
            "relation_validation",
            calls,
        ),
        clinical_summary_agent=MockAgent(
            "clinical_summary",
            calls,
        ),
        final_report_agent=MockAgent(
            "final_report",
            calls,
        ),
    )

    # We don't need a real WorkflowState for this smoke test because
    # MockAgent simply returns the state unchanged.
    state = object()

    result = await workflow.run(state)

    expected = [
        "entity_extraction",
        "entity_normalization",
        "entity_validation",
        "relation_extraction",
        "relation_normalization",
        "relation_validation",
        "clinical_summary",
        "final_report",
    ]

    print("\nExecution order:")
    for index, name in enumerate(calls, start=1):
        print(f"{index}. {name}")

    assert calls == expected, (
        f"Unexpected workflow order.\n"
        f"Expected: {expected}\n"
        f"Actual:   {calls}"
    )

    assert result is state

    print("\n✓ Workflow ordering is correct")
    print("✓ All workflow stages are connected")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())