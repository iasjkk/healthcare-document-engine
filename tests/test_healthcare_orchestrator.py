"""
Registry-based HealthcareOrchestrator test.

Verifies that the orchestrator resolves all required agents
from AgentRegistry and constructs the workflow correctly.
"""

from __future__ import annotations

import asyncio

from framework.registry.agent_registry import AgentRegistry
from framework.orchestrator.healthcare_orchestrator import (
    HealthcareOrchestrator,
)


class MockAgent:
    """
    Minimal agent object for registry testing.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    async def run(self, state):
        return state


def build_registry() -> AgentRegistry:
    """
    Build a registry containing all required workflow agents.
    """

    registry = AgentRegistry()

    agent_names = [
        "entity_extraction",
        "entity_normalization",
        "entity_validation",
        "relation_extraction",
        "relation_normalization",
        "relation_validation",
        "clinical_summary",
        "final_report",
    ]

    for name in agent_names:
        registry.register(
            name,
            MockAgent(name),
        )

    return registry


async def main() -> None:

    print("=" * 70)
    print("REGISTRY-BASED HEALTHCARE ORCHESTRATOR TEST")
    print("=" * 70)

    registry = build_registry()

    print("\nRegistered agents:")

    for name in registry.list():
        print(f"  ✓ {name}")

    orchestrator = HealthcareOrchestrator(
        agent_registry=registry,
    )

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    await orchestrator.initialize()

    assert orchestrator.workflow is not None

    print("\n✓ AgentRegistry injected")
    print("✓ All required agents resolved")
    print("✓ HealthcareWorkflow constructed")

    # ---------------------------------------------------------
    # Verify workflow references
    # ---------------------------------------------------------

    workflow = orchestrator.workflow

    assert (
        workflow.entity_extraction_agent
        is registry.get("entity_extraction")
    )

    assert (
        workflow.entity_normalization_agent
        is registry.get("entity_normalization")
    )

    assert (
        workflow.entity_validation_agent
        is registry.get("entity_validation")
    )

    assert (
        workflow.relation_extraction_agent
        is registry.get("relation_extraction")
    )

    assert (
        workflow.relation_normalization_agent
        is registry.get("relation_normalization")
    )

    assert (
        workflow.relation_validation_agent
        is registry.get("relation_validation")
    )

    assert (
        workflow.clinical_summary_agent
        is registry.get("clinical_summary")
    )

    assert (
        workflow.final_report_agent
        is registry.get("final_report")
    )

    print("✓ All workflow agents point to registry instances")

    # ---------------------------------------------------------
    # Shutdown
    # ---------------------------------------------------------

    await orchestrator.shutdown()

    assert orchestrator.workflow is None

    print("✓ Orchestrator shutdown completed")

    print("\n" + "=" * 70)
    print("REGISTRY-BASED ORCHESTRATOR TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())