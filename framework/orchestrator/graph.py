"""
Healthcare Document Engine workflow orchestration.

Runs the complete agent pipeline using the standard BaseAgent
lifecycle through agent.run().
"""

from __future__ import annotations

from typing import Any

from framework.state.workflow_state import WorkflowState


class HealthcareWorkflow:
    """
    Complete healthcare document processing workflow.

    Pipeline
    --------
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
    """

    def __init__(
        self,
        document_structure_agent,
        entity_extraction_agent: Any,
        entity_normalization_agent: Any,
        entity_validation_agent: Any,
        relation_extraction_agent: Any,
        relation_normalization_agent: Any,
        relation_validation_agent: Any,
        clinical_summary_agent: Any,
        final_report_agent: Any,
    ) -> None:

        self.document_structure_agent = document_structure_agent
        self.entity_extraction_agent = entity_extraction_agent
        self.entity_normalization_agent = entity_normalization_agent
        self.entity_validation_agent = entity_validation_agent

        self.relation_extraction_agent = relation_extraction_agent
        self.relation_normalization_agent = relation_normalization_agent
        self.relation_validation_agent = relation_validation_agent

        self.clinical_summary_agent = clinical_summary_agent
        self.final_report_agent = final_report_agent

    async def run(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        """
        Execute the complete workflow.

        Every agent is executed through BaseAgent.run()
        so the standard lifecycle hooks are preserved.
        """

        # =====================================================
        # Document Structure
        # =====================================================

        state = await self.document_structure_agent.run(state)

        # =====================================================
        # Entity Pipeline
        # =====================================================

        state = await self.entity_extraction_agent.run(state)

        state = await self.entity_normalization_agent.run(state)

        state = await self.entity_validation_agent.run(state)

        # =====================================================
        # Relation Pipeline
        # =====================================================

        state = await self.relation_extraction_agent.run(state)

        state = await self.relation_normalization_agent.run(state)

        state = await self.relation_validation_agent.run(state)

        # =====================================================
        # Clinical Summary
        # =====================================================

        state = await self.clinical_summary_agent.run(state)

        # =====================================================
        # Final Report
        # =====================================================

        state = await self.final_report_agent.run(state)

        return state