"""
Healthcare Document Engine orchestrator.

Builds and executes the healthcare workflow using the
existing AgentRegistry and ProviderRegistry.
"""

from __future__ import annotations

from framework.core.base_orchestrator import BaseOrchestrator
from framework.orchestrator.graph import HealthcareWorkflow
from framework.state.workflow_state import WorkflowState


class HealthcareOrchestrator(BaseOrchestrator):
    """
    Main application orchestrator.

    Agents are resolved from the injected AgentRegistry.
    """

    REQUIRED_AGENTS = (
        "document_structure",
        "entity_extraction",
        "entity_normalization",
        "entity_validation",
        "relation_extraction",
        "relation_normalization",
        "relation_validation",
        "clinical_summary",
        "final_report",
    )

    def __init__(
        self,
        agent_registry,
        provider_registry=None,
    ) -> None:

        super().__init__(
            name="healthcare_orchestrator",
            description=(
                "Orchestrates the complete healthcare document "
                "understanding and reporting workflow."
            ),
            version="1.0.0",
        )

        self.set_agent_registry(agent_registry)

        if provider_registry is not None:
            self.set_provider_registry(provider_registry)

        self.workflow = None

    async def initialize(self) -> None:
        """
        Resolve all required agents and construct the workflow.
        """

        await super().initialize()

        if self.agent_registry is None:
            raise RuntimeError(
                "AgentRegistry has not been configured."
            )

        agents = {}

        for name in self.REQUIRED_AGENTS:
            try:
                agents[name] = self.agent_registry.get(name)
            except KeyError as exc:
                raise RuntimeError(
                    f"Required agent '{name}' is not registered."
                ) from exc

        self.workflow = HealthcareWorkflow(
            document_structure_agent=agents["document_structure"],
            entity_extraction_agent=agents["entity_extraction"],
            entity_normalization_agent=agents["entity_normalization"],
            entity_validation_agent=agents["entity_validation"],
            relation_extraction_agent=agents["relation_extraction"],
            relation_normalization_agent=agents["relation_normalization"],
            relation_validation_agent=agents["relation_validation"],
            clinical_summary_agent=agents["clinical_summary"],
            final_report_agent=agents["final_report"],
        )

    async def run(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        """
        Execute the healthcare workflow.
        """

        if not self.enabled:
            raise RuntimeError(
                "HealthcareOrchestrator is disabled."
            )

        if self.workflow is None:
            raise RuntimeError(
                "HealthcareOrchestrator has not been initialized."
            )

        return await self.workflow.run(state)

    async def shutdown(self) -> None:
        """
        Shutdown the orchestrator.
        """

        self.workflow = None

        await super().shutdown()