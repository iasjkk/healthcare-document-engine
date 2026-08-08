"""
Healthcare Entity Normalization Agent.

Normalizes entities produced by EntityExtractionAgent
while preserving provenance.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.entity_normalization_schema import (
    EntityNormalizationResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class EntityNormalizationAgent(BaseAgent):
    """
    Normalize healthcare entities.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="entity_normalization_agent",
            description=(
                "Normalizes extracted healthcare "
                "entities while preserving provenance."
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
        Execute entity normalization.
        """

        if self.logger:
            self.logger.info(
                "Starting Entity Normalization."
            )

        # ------------------------------------------------------
        # EntityState is the input.
        # ------------------------------------------------------

        entities = state.entities.entities

        if not entities:

            if self.logger:
                self.logger.warning(
                    "No extracted entities found."
                )

            state.checkpoint.stage = (
                "entity_normalization_completed"
            )

            return state

        # ------------------------------------------------------
        # Convert Entity objects into prompt payload.
        # ------------------------------------------------------

        entity_payload = [
            {
                "entity_id": entity.entity_id,
                "entity_type": entity.entity_type,
                "text": entity.value,
                "normalized_text": (
                    entity.normalized_value or ""
                ),
                "page_number": entity.page_number,
                "source_node_id": (
                    entity.source_node or ""
                ),
                "confidence": entity.confidence,
                "attributes": entity.metadata,
            }
            for entity in entities
        ]

        # ------------------------------------------------------
        # Build prompt
        # ------------------------------------------------------

        prompt_template = self.prompt_registry.get(
            "entity_normalization"
        )

        prompt = prompt_template.build(
            entities=entity_payload
        )

        # ------------------------------------------------------
        # LLM call
        # ------------------------------------------------------

        response = await self.router.chat(
            capability="entity_normalization",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert healthcare "
                        "entity normalization system. "
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
        # Parse and validate
        # ------------------------------------------------------

        parsed = parse_json_response(
            result_text,
            EntityNormalizationResponse,
        )

        # ------------------------------------------------------
        # Index normalized entities by ID.
        # ------------------------------------------------------

        normalized_by_id = {
            entity.entity_id: entity
            for entity in parsed.entities
        }

        # ------------------------------------------------------
        # Update existing Entity objects.
        #
        # We do NOT replace EntityState with a second
        # normalization structure.
        # ------------------------------------------------------

        normalized_count = 0

        for entity in entities:

            normalized = normalized_by_id.get(
                entity.entity_id
            )

            if normalized is None:

                if self.logger:
                    self.logger.warning(
                        "No normalization result "
                        f"for entity "
                        f"{entity.entity_id}."
                    )

                continue

            # --------------------------------------------------
            # Update normalized value.
            # --------------------------------------------------

            entity.normalized_value = (
                normalized.normalized_text
            )

            # --------------------------------------------------
            # Preserve original provenance.
            #
            # Do NOT allow the LLM to overwrite:
            #
            # - entity_id
            # - value
            # - page_number
            # - source_node
            # --------------------------------------------------

            # --------------------------------------------------
            # Store normalization metadata.
            # --------------------------------------------------

            entity.metadata[
                "normalization_status"
            ] = normalized.normalization_status

            entity.metadata[
                "normalization_confidence"
            ] = normalized.confidence

            if normalized.attributes:

                entity.metadata[
                    "normalized_attributes"
                ] = normalized.attributes

            if normalized.metadata:

                entity.metadata[
                    "normalization_metadata"
                ] = normalized.metadata

            normalized_count += 1

        # ------------------------------------------------------
        # EntityState already contains the updated objects.
        # ------------------------------------------------------

        state.entities.entities = entities

        # ------------------------------------------------------
        # Checkpoint
        # ------------------------------------------------------

        state.checkpoint.stage = (
            "entity_normalization_completed"
        )

        if self.logger:
            self.logger.info(
                "Entity Normalization Complete. "
                f"Normalized "
                f"{normalized_count} "
                "of "
                f"{len(entities)} "
                "entity(s)."
            )

        return state