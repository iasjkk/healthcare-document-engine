"""
END-TO-END HEALTHCARE WORKFLOW TEST

Tests the complete workflow:

    Entity Extraction
        ↓
    Entity Normalization
        ↓
    Entity Validation
        ↓
    Relation Extraction
        ↓
    Relation Normalization
        ↓
    Relation Validation
        ↓
    Clinical Summary
        ↓
    Final Report

This test intentionally uses mock agents.

No OpenRouter/API calls are made.
"""

from __future__ import annotations

import asyncio
from typing import Any

from framework.orchestrator.healthcare_orchestrator import (
    HealthcareOrchestrator,
)

from framework.registry.agent_registry import AgentRegistry


# ============================================================
# Mock Agent
# ============================================================


class MockAgent:
    """
    Lightweight mock agent implementing the interface required
    by HealthcareWorkflow.

    Each agent:

    1. Records execution.
    2. Updates the WorkflowState.
    3. Returns the same state.
    """

    def __init__(
        self,
        name: str,
        execution_log: list[str],
    ) -> None:

        self.name = name
        self.execution_log = execution_log

    async def run(self, state):

        self.execution_log.append(self.name)

        # ----------------------------------------------------
        # Simulate state changes produced by each stage.
        # ----------------------------------------------------

        if self.name == "entity_extraction":

            state.checkpoint.stage = (
                "e2e_entity_extraction_completed"
            )

        elif self.name == "entity_normalization":

            state.checkpoint.stage = (
                "e2e_entity_normalization_completed"
            )

        elif self.name == "entity_validation":

            state.checkpoint.stage = (
                "e2e_entity_validation_completed"
            )

        elif self.name == "relation_extraction":

            state.checkpoint.stage = (
                "e2e_relation_extraction_completed"
            )

        elif self.name == "relation_normalization":

            state.checkpoint.stage = (
                "e2e_relation_normalization_completed"
            )

        elif self.name == "relation_validation":

            state.checkpoint.stage = (
                "e2e_relation_validation_completed"
            )

        elif self.name == "clinical_summary":

            state.checkpoint.stage = (
                "clinical_summary_completed"
            )

        elif self.name == "final_report":

            state.checkpoint.stage = (
                "final_report_completed"
            )

        return state

# ============================================================
# Workflow State Factory
# ============================================================


def create_test_state():
    from framework.state.workflow_state import WorkflowState

    from framework.state.execution_state import ExecutionState
    from framework.state.document_state import DocumentState
    from framework.state.layout_state import LayoutState
    from framework.state.entity_state import EntityState
    from framework.state.validation_state import ValidationState
    from framework.state.model_state import ModelState
    from framework.state.metrics_state import MetricsState
    from framework.state.clinical_summary_state import (
        ClinicalSummaryState,
    )

    state = WorkflowState(
        execution=ExecutionState(
            run_id="test-run-001",
            workflow_id="healthcare-workflow-test",
        ),
        document=DocumentState(
            document_id="test-document-001",
            file_name="test_clinical_document.pdf",
            file_path="tests/data/test_clinical_document.pdf",
            file_type="pdf",
        ),
        layout=LayoutState(),
        entities=EntityState(
            entities=[],
            metadata={},
        ),
        validation=ValidationState(),
        clinical_summary=ClinicalSummaryState(
            metadata={},
        ),
        model=ModelState(),
        metrics=MetricsState(),
    )

    return state

# ============================================================
# Main Test
# ============================================================


async def main():

    print()
    print("=" * 80)
    print("END-TO-END HEALTHCARE WORKFLOW TEST")
    print("=" * 80)

    execution_log: list[str] = []

    # --------------------------------------------------------
    # Create mock agents.
    # --------------------------------------------------------

    agents = {
        name: MockAgent(
            name=name,
            execution_log=execution_log,
        )
        for name in (
            "entity_extraction",
            "entity_normalization",
            "entity_validation",
            "relation_extraction",
            "relation_normalization",
            "relation_validation",
            "clinical_summary",
            "final_report",
        )
    }

    # --------------------------------------------------------
    # Register agents.
    # --------------------------------------------------------

    registry = AgentRegistry()

    for name, agent in agents.items():

        registry.register(
            name,
            agent,
        )

    print()
    print("Registered mock agents:")

    for name in registry.list():

        print(f"✓ {name}")

    # --------------------------------------------------------
    # Construct orchestrator.
    # --------------------------------------------------------

    orchestrator = HealthcareOrchestrator(
        agent_registry=registry,
    )

    await orchestrator.initialize()

    print()
    print("✓ HealthcareOrchestrator initialized")
    print("✓ HealthcareWorkflow constructed")

    # --------------------------------------------------------
    # Create initial state.
    # --------------------------------------------------------

    state = create_test_state()

    print()
    print("✓ Initial WorkflowState created")

    # --------------------------------------------------------
    # Execute complete workflow.
    # --------------------------------------------------------

    result = await orchestrator.run(state)

    # --------------------------------------------------------
    # Expected execution order.
    # --------------------------------------------------------

    expected_order = [
        "entity_extraction",
        "entity_normalization",
        "entity_validation",
        "relation_extraction",
        "relation_normalization",
        "relation_validation",
        "clinical_summary",
        "final_report",
    ]

    print()
    print("Execution order:")

    for index, name in enumerate(
        execution_log,
        start=1,
    ):

        print(f"{index}. {name}")

    # --------------------------------------------------------
    # Verify execution order.
    # --------------------------------------------------------

    assert execution_log == expected_order, (
        "Workflow execution order is incorrect.\n"
        f"Expected: {expected_order}\n"
        f"Actual:   {execution_log}"
    )

    print()
    print("✓ All 8 agents executed in correct order")

    # --------------------------------------------------------
    # Verify state propagation.
    # --------------------------------------------------------

    expected_order = [
        "entity_extraction",
        "entity_normalization",
        "entity_validation",
        "relation_extraction",
        "relation_normalization",
        "relation_validation",
        "clinical_summary",
        "final_report",
    ]

    assert execution_log == expected_order

    print("✓ All 8 agents executed in correct order")

    # --------------------------------------------------------
    # Verify final checkpoint.
    # --------------------------------------------------------

    assert (
        result.checkpoint.stage
        == "final_report_completed"
    )

    print("✓ Final checkpoint completed")

    # --------------------------------------------------------
    # Shutdown.
    # --------------------------------------------------------

    await orchestrator.shutdown()

    assert orchestrator.workflow is None

    print("✓ Orchestrator shutdown completed")

    # --------------------------------------------------------
    # Final result.
    # --------------------------------------------------------

    print()
    print("=" * 80)
    print("✓ END-TO-END WORKFLOW TEST PASSED")
    print("=" * 80)
    print()


if __name__ == "__main__":

    asyncio.run(main())