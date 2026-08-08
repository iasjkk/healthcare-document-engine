"""
Healthcare Entity Validation Agent.

Validates extracted and normalized healthcare
entities while preserving provenance.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.entity_validation_schema import (
    EntityValidationResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class EntityValidationAgent(BaseAgent):
    """
    Validate healthcare entities.

    The canonical entity collection is:

        state.entities.entities

    Validation information is stored in:

        Entity.metadata
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="entity_validation_agent",
            description=(
                "Validates extracted and normalized "
                "healthcare entities."
            ),
            version="1.0.0",
        )

        self.router = router
        self.prompt_registry = prompt_registry

    async def execute(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        """
        Execute healthcare entity validation.
        """

        if self.logger:
            self.logger.info(
                "Starting Entity Validation."
            )

        # ------------------------------------------------------
        # EntityState is the source of truth.
        # ------------------------------------------------------

        entities = state.entities.entities

        if not entities:

            if self.logger:
                self.logger.warning(
                    "No entities found for validation."
                )

            state.checkpoint.stage = (
                "entity_validation_completed"
            )

            return state

        # ------------------------------------------------------
        # Build prompt payload.
        # ------------------------------------------------------

        entity_payload = [
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
            for entity in entities
        ]

        # ------------------------------------------------------
        # Prompt
        # ------------------------------------------------------

        prompt_template = self.prompt_registry.get(
            "entity_validation"
        )

        prompt = prompt_template.build(
            entities=entity_payload
        )

        # ------------------------------------------------------
        # LLM
        # ------------------------------------------------------

        response = await self.router.chat(
            capability="entity_validation",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert healthcare "
                        "entity validation system. "
                        "Return only valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        # ------------------------------------------------------
        # Extract response
        # ------------------------------------------------------

        result_text = (
            response[
                "choices"
            ][0][
                "message"
            ][
                "content"
            ]
        )

        # ------------------------------------------------------
        # Parse and validate response.
        # ------------------------------------------------------

        parsed = parse_json_response(
            result_text,
            EntityValidationResponse,
        )

        # ------------------------------------------------------
        # Index validation results by entity ID.
        # ------------------------------------------------------

        validation_by_id = {
            result.entity_id: result
            for result in parsed.entities
        }

        validated_count = 0
        invalid_count = 0
        warning_count = 0

        # ------------------------------------------------------
        # Apply validation results.
        #
        # IMPORTANT:
        #
        # The LLM cannot overwrite source provenance.
        # ------------------------------------------------------

        for entity in entities:

            validation = validation_by_id.get(
                entity.entity_id
            )

            if validation is None:

                if self.logger:
                    self.logger.warning(
                        "No validation result "
                        f"returned for entity "
                        f"{entity.entity_id}."
                    )

                entity.metadata[
                    "validation_status"
                ] = "not_validated"

                entity.metadata[
                    "validation_confidence"
                ] = 0.0

                continue

            # --------------------------------------------------
            # Store validation result.
            # --------------------------------------------------

            entity.metadata[
                "is_valid"
            ] = validation.is_valid

            entity.metadata[
                "validation_status"
            ] = validation.validation_status

            entity.metadata[
                "validation_confidence"
            ] = validation.confidence

            entity.metadata[
                "validation_issues"
            ] = validation.issues

            entity.metadata[
                "validation_warnings"
            ] = validation.warnings

            # --------------------------------------------------
            # Store suggested corrections.
            #
            # We deliberately do NOT overwrite the original
            # value or entity type automatically.
            # --------------------------------------------------

            if validation.corrected_value:

                entity.metadata[
                    "suggested_corrected_value"
                ] = validation.corrected_value

            if validation.corrected_entity_type:

                entity.metadata[
                    "suggested_corrected_entity_type"
                ] = (
                    validation.corrected_entity_type
                )

            # --------------------------------------------------
            # Preserve additional validation metadata.
            # --------------------------------------------------

            if validation.metadata:

                entity.metadata[
                    "validation_metadata"
                ] = validation.metadata

            # --------------------------------------------------
            # Counters
            # --------------------------------------------------

            if validation.is_valid:
                validated_count += 1
            else:
                invalid_count += 1

            if validation.warnings:
                warning_count += 1

        # ------------------------------------------------------
        # Store aggregate validation information.
        #
        # We store this inside EntityState metadata rather
        # than WorkflowState.metadata.
        # ------------------------------------------------------

        # EntityState itself remains the source of truth.
        state.entities.entities = entities

        # ------------------------------------------------------
        # Checkpoint
        # ------------------------------------------------------

        state.checkpoint.stage = (
            "entity_validation_completed"
        )

        if self.logger:
            self.logger.info(
                "Entity Validation Complete. "
                f"Valid: {validated_count}, "
                f"Invalid: {invalid_count}, "
                f"Warnings: {warning_count}."
            )

        return state
