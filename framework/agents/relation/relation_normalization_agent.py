"""
Healthcare Relation Normalization Agent.

Normalizes relations produced by
RelationExtractionAgent while preserving
source entity references and provenance.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.relation_normalization_schema import (
    RelationNormalizationResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class RelationNormalizationAgent(BaseAgent):
    """
    Normalize healthcare relations.

    Canonical relation collection:

        state.relations.relations

    The LLM is allowed to normalize relation
    semantics but is not allowed to modify
    source entity identifiers.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="relation_normalization_agent",
            description=(
                "Normalizes extracted healthcare "
                "relations while preserving "
                "entity references and provenance."
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
        Execute relation normalization.
        """

        if self.logger:

            self.logger.info(
                "Starting Relation Normalization."
            )

        # ------------------------------------------------------
        # RelationState is the source of truth.
        # ------------------------------------------------------

        relations = state.relations.relations

        if not relations:

            if self.logger:

                self.logger.warning(
                    "No relations found for normalization."
                )

            state.checkpoint.stage = (
                "relation_normalization_completed"
            )

            return state

        # ------------------------------------------------------
        # Convert relations into prompt payload.
        # ------------------------------------------------------

        relation_payload = []

        for relation in relations:

            relation_payload.append(
                {
                    "relation_id": relation.relation_id,
                    "source_entity_id": (
                        relation.source_entity_id
                    ),
                    "target_entity_id": (
                        relation.target_entity_id
                    ),
                    "relation_type": (
                        relation.relation_type
                    ),
                    "confidence": (
                        relation.confidence
                    ),
                    "attributes": (
                        relation.attributes
                    ),
                    "metadata": (
                        relation.metadata
                    ),
                }
            )

        # ------------------------------------------------------
        # Build prompt.
        # ------------------------------------------------------

        prompt_template = self.prompt_registry.get(
            "relation_normalization"
        )

        prompt = prompt_template.build(
            relations=relation_payload
        )

        # ------------------------------------------------------
        # LLM call.
        # ------------------------------------------------------

        response = await self.router.chat(
            capability="relation_normalization",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert healthcare "
                        "relation normalization system. "
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
        # Extract response.
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
        # Parse and validate.
        # ------------------------------------------------------

        parsed = parse_json_response(
            result_text,
            RelationNormalizationResponse,
        )

        # ------------------------------------------------------
        # Index normalized relations by relation ID.
        # ------------------------------------------------------

        normalized_by_id = {
            relation.relation_id: relation
            for relation in parsed.relations
        }

        normalized_count = 0

        # ------------------------------------------------------
        # Apply normalization.
        #
        # IMPORTANT:
        #
        # Source and target entity IDs are preserved
        # from the application state.
        # ------------------------------------------------------

        for relation in relations:

            normalized = normalized_by_id.get(
                relation.relation_id
            )

            if normalized is None:

                if self.logger:

                    self.logger.warning(
                        "No normalization result "
                        f"returned for relation "
                        f"{relation.relation_id}."
                    )

                relation.metadata[
                    "normalization_status"
                ] = "not_normalized"

                relation.metadata[
                    "normalization_confidence"
                ] = 0.0

                continue

            # --------------------------------------------------
            # Preserve original relation type.
            # --------------------------------------------------

            original_relation_type = (
                relation.relation_type
            )

            relation.metadata[
                "original_relation_type"
            ] = original_relation_type

            # --------------------------------------------------
            # Update normalized relation type.
            # --------------------------------------------------

            relation.relation_type = (
                normalized.normalized_relation_type
            )

            # --------------------------------------------------
            # Store normalization metadata.
            # --------------------------------------------------

            relation.metadata[
                "normalization_status"
            ] = normalized.normalization_status

            relation.metadata[
                "normalization_confidence"
            ] = normalized.confidence

            if normalized.original_relation_type:

                relation.metadata[
                    "llm_original_relation_type"
                ] = (
                    normalized.original_relation_type
                )

            if normalized.attributes:

                relation.attributes.update(
                    normalized.attributes
                )

            if normalized.metadata:

                relation.metadata[
                    "normalization_metadata"
                ] = normalized.metadata

            normalized_count += 1

        # ------------------------------------------------------
        # Entity references remain untouched.
        # ------------------------------------------------------

        state.relations.relations = relations

        # ------------------------------------------------------
        # Checkpoint.
        # ------------------------------------------------------

        state.checkpoint.stage = (
            "relation_normalization_completed"
        )

        if self.logger:

            self.logger.info(
                "Relation Normalization Complete. "
                f"Normalized "
                f"{normalized_count} "
                "of "
                f"{len(relations)} "
                "relation(s)."
            )

        return state