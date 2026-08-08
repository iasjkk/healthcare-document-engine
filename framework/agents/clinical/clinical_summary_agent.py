"""
Healthcare Clinical Summary Agent.

Generates a concise clinical summary from
structured healthcare information.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4
from datetime import datetime

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter

from framework.schemas.clinical_summary_schema import (
    ClinicalSummaryResponse,
)

from framework.state.workflow_state import WorkflowState

from framework.utils.json_parser import (
    parse_json_response,
)


class ClinicalSummaryAgent(BaseAgent):
    """
    Generates a clinical summary from validated
    healthcare entities and relations.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="clinical_summary_agent",
            description=(
                "Generates concise clinical summaries "
                "from structured healthcare information."
            ),
            version="1.0.0",
        )

        self.router = router
        self.prompt_registry = prompt_registry

    async def execute(
        self,
        state: WorkflowState,
    ) -> WorkflowState:

        if self.logger:

            self.logger.info(
                "Starting Clinical Summary."
            )

        # --------------------------------------------------
        # Build structured clinical input.
        # --------------------------------------------------

        clinical_data: dict[str, Any] = {
            "document": {
                "document_id": (
                    state.document.document_id
                ),
                "file_name": (
                    state.document.file_name
                ),
            },
            "entities": [],
            "relations": [],
        }

        # --------------------------------------------------
        # Entities
        # --------------------------------------------------

        for entity in state.entities.entities:

            clinical_data["entities"].append(
                {
                    "entity_id": entity.entity_id,
                    "entity_type": entity.entity_type,
                    "value": entity.value,
                    "normalized_value": (
                        entity.normalized_value
                    ),
                    "confidence": entity.confidence,
                    "page_number": entity.page_number,
                    "source_node": entity.source_node,
                    "metadata": entity.metadata,
                }
            )

        # --------------------------------------------------
        # Relations
        # --------------------------------------------------

        for relation in state.relations.relations:

            clinical_data["relations"].append(
                relation.model_dump()
            )

        # --------------------------------------------------
        # Check whether information exists.
        # --------------------------------------------------

        if (
            not clinical_data["entities"]
            and not clinical_data["relations"]
        ):

            if self.logger:

                self.logger.warning(
                    "No clinical information "
                    "available for summarization."
                )

            state.clinical_summary = (
                state.clinical_summary.model_copy(
                    update={
                        "summary": "",
                        "key_findings": [],
                        "confidence": 0.0,
                        "notes": (
                            "No clinical information "
                            "was available."
                        ),
                    }
                )
            )

            state.checkpoint.stage = (
                "clinical_summary_completed"
            )

            return state

        # --------------------------------------------------
        # Prompt
        # --------------------------------------------------

        prompt_template = (
            self.prompt_registry.get(
                "clinical_summary"
            )
        )

        prompt = prompt_template.build(
            clinical_data=clinical_data
        )

        # --------------------------------------------------
        # LLM
        # --------------------------------------------------

        response = await self.router.chat(
            capability="clinical_summary",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert healthcare "
                        "clinical summarization system. "
                        "Return only valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        # --------------------------------------------------
        # Response
        # --------------------------------------------------

        result_text = (
            response[
                "choices"
            ][0][
                "message"
            ][
                "content"
            ]
        )

        # --------------------------------------------------
        # Parse
        # --------------------------------------------------

        parsed = parse_json_response(
            result_text,
            ClinicalSummaryResponse,
        )

        # --------------------------------------------------
        # Store clinical summary.
        # --------------------------------------------------

        state.clinical_summary.summary = (
            parsed.summary
        )

        state.clinical_summary.key_findings = (
            parsed.key_findings
        )

        state.clinical_summary.diagnoses = (
            parsed.diagnoses
        )

        state.clinical_summary.medications = (
            parsed.medications
        )

        state.clinical_summary.allergies = (
            parsed.allergies
        )

        state.clinical_summary.laboratory_findings = (
            parsed.laboratory_findings
        )

        state.clinical_summary.pathology_findings = (
            parsed.pathology_findings
        )

        state.clinical_summary.biomarkers = (
            parsed.biomarkers
        )

        state.clinical_summary.procedures = (
            parsed.procedures
        )

        state.clinical_summary.recommendations = (
            parsed.recommendations
        )

        state.clinical_summary.confidence = (
            parsed.confidence
        )

        state.clinical_summary.notes = (
            parsed.notes
        )

        state.clinical_summary.metadata = (
            parsed.metadata
        )

        # --------------------------------------------------
        # Checkpoint
        # --------------------------------------------------

        state.checkpoint.stage = (
            "clinical_summary_completed"
        )

        if self.logger:

            self.logger.info(
                "Clinical Summary Complete."
            )

        return state