"""
Healthcare Relation Extraction Agent.
"""

from __future__ import annotations

import json
from typing import Any

from framework.core.base_agent import BaseAgent
from framework.schemas.relation_extraction_schema import (
    RelationExtractionResponse,
)
from framework.state.relation_state import Relation
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response

from framework.prompts.relation_extraction_prompt import (
    RelationExtractionPrompt,
)


class RelationExtractionAgent(BaseAgent):
    """
    Extracts explicit relationships between healthcare entities.
    """

    def __init__(self, router) -> None:
        super().__init__(
            name="relation_extraction_agent",
            description=(
                "Extracts explicit semantic relationships "
                "between healthcare entities."
            ),
        )

        self.router = router
        self.prompt_builder = RelationExtractionPrompt()

    async def execute(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        """
        Execute relation extraction.
        """

        # ---------------------------------------------------------
        # Collect document text
        # ---------------------------------------------------------

        text = self._get_document_text(state)

        # ---------------------------------------------------------
        # Collect entities
        # ---------------------------------------------------------

        entities = self._get_entities(state)

        # ---------------------------------------------------------
        # If there is no text or no entities, there can be
        # no reliable relation extraction.
        # ---------------------------------------------------------

        if not text or not entities:

            state.relations.relations = []

            self._record_metadata(
                state,
                extracted_count=0,
                status="skipped",
                reason=(
                    "No document text or entities were "
                    "available for relation extraction."
                ),
            )

            return state

        # ---------------------------------------------------------
        # Build prompt
        # ---------------------------------------------------------

        prompt = self.prompt_builder.build(
            entities=entities,
            text=text,
        )

        # ---------------------------------------------------------
        # Call model router
        # ---------------------------------------------------------

        response = await self.router.chat(
            capability="relation_extraction",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise healthcare "
                        "relation extraction system."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        # ---------------------------------------------------------
        # Extract model content
        # ---------------------------------------------------------

        content = self._get_response_content(response)

        # ---------------------------------------------------------
        # Parse structured response
        # ---------------------------------------------------------

        parsed = parse_json_response(
            content,
            RelationExtractionResponse,
        )

        # ---------------------------------------------------------
        # Convert schema objects into RelationState objects
        # ---------------------------------------------------------

        relations: list[Relation] = []

        valid_entity_ids = {
            str(entity.get("entity_id"))
            for entity in entities
            if entity.get("entity_id") is not None
        }

        for extracted in parsed.relations:

            # Prevent references to nonexistent entities.
            if (
                extracted.source_entity_id
                not in valid_entity_ids
            ):
                continue

            if (
                extracted.target_entity_id
                not in valid_entity_ids
            ):
                continue

            relation = Relation(
                relation_id=extracted.relation_id,
                source_entity_id=(
                    extracted.source_entity_id
                ),
                target_entity_id=(
                    extracted.target_entity_id
                ),
                relation_type=extracted.relation_type,
                confidence=extracted.confidence,
                attributes=dict(
                    extracted.attributes
                ),
                metadata={
                    **extracted.metadata,
                    "extraction_agent": (
                        "relation_extraction_agent"
                    ),
                },
            )

            relations.append(relation)

        # ---------------------------------------------------------
        # Update canonical RelationState
        # ---------------------------------------------------------

        state.relations.relations = relations

        # ---------------------------------------------------------
        # Store metadata
        # ---------------------------------------------------------

        self._record_metadata(
            state,
            extracted_count=len(relations),
            status="completed",
            model_confidence=parsed.confidence,
            notes=parsed.notes,
        )

        return state

    # =============================================================
    # Helpers
    # =============================================================

    @staticmethod
    def _get_document_text(
        state: WorkflowState,
    ) -> str:
        """
        Extract document text from DocumentState.

        Supports the common field names used by the project.
        """

        document = state.document

        for field_name in (
            "text",
            "content",
            "raw_text",
            "document_text",
        ):

            if hasattr(document, field_name):

                value = getattr(
                    document,
                    field_name,
                )

                if isinstance(value, str) and value.strip():
                    return value

        # Fallback to model_dump.
        if hasattr(document, "model_dump"):

            data = document.model_dump()

            for field_name in (
                "text",
                "content",
                "raw_text",
                "document_text",
            ):

                value = data.get(field_name)

                if isinstance(value, str) and value.strip():
                    return value

        return ""

    @staticmethod
    def _get_entities(
        state: WorkflowState,
    ) -> list[dict[str, Any]]:
        """
        Convert EntityState into JSON-compatible dictionaries.
        """

        entities_state = state.entities

        if not hasattr(
            entities_state,
            "entities",
        ):
            return []

        entities = entities_state.entities

        result: list[dict[str, Any]] = []

        for entity in entities:

            if hasattr(entity, "model_dump"):
                result.append(
                    entity.model_dump()
                )

            elif isinstance(entity, dict):
                result.append(entity)

        return result

    @staticmethod
    def _get_response_content(
        response: Any,
    ) -> str:
        """
        Extract textual content from the ModelRouter response.
        """

        if isinstance(response, str):
            return response

        if isinstance(response, dict):

            # Common OpenRouter-style response.
            choices = response.get("choices")

            if choices:

                first = choices[0]

                if isinstance(first, dict):

                    message = first.get(
                        "message"
                    )

                    if isinstance(message, dict):

                        content = message.get(
                            "content"
                        )

                        if content is not None:
                            return str(content)

                    content = first.get(
                        "content"
                    )

                    if content is not None:
                        return str(content)

            # Some providers return content directly.
            content = response.get("content")

            if content is not None:
                return str(content)

            # Already structured response.
            return json.dumps(
                response,
                ensure_ascii=False,
            )

        return str(response)

    @staticmethod
    def _record_metadata(
        state: WorkflowState,
        **metadata: Any,
    ) -> None:
        """
        Store extraction metadata without requiring a new state field.
        """

        if not hasattr(
            state.relations,
            "metadata",
        ):
            return

        state.relations.metadata.update(
            metadata
        )