"""
Healthcare Entity Extraction Agent.

Extracts healthcare entities from document
layout nodes while preserving source traceability.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.entity_extraction_schema import (
    EntityExtractionResponse,
)
from framework.state.entity_state import Entity
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class EntityExtractionAgent(BaseAgent):
    """
    Extract healthcare entities from document layout nodes.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="entity_extraction_agent",
            description=(
                "Extracts healthcare entities from "
                "structured document content."
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
        Execute healthcare entity extraction.
        """

        if self.logger:
            self.logger.info(
                "Starting Entity Extraction."
            )

        # ------------------------------------------------------
        # Prompt
        # ------------------------------------------------------

        prompt_template = self.prompt_registry.get(
            "entity_extraction"
        )

        # ------------------------------------------------------
        # Select meaningful layout nodes
        # ------------------------------------------------------

        nodes = [
            node
            for node in state.layout.nodes
            if node.text
            and node.text.strip()
        ]

        if self.logger:
            self.logger.info(
                f"Processing {len(nodes)} "
                "layout node(s) for entity extraction."
            )

        extracted_entities: list[Entity] = []

        # ------------------------------------------------------
        # Process each layout node
        # ------------------------------------------------------

        for node in nodes:

            prompt = prompt_template.build(
                text=node.text,
                page_number=node.page_number,
                node_id=node.node_id,
                layout_type=node.layout_type,
            )

            # --------------------------------------------------
            # LLM call
            # --------------------------------------------------

            response = await self.router.chat(
                capability="entity_extraction",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert healthcare "
                            "entity extraction system. "
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
            # Extract response
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
            # Parse and validate
            # --------------------------------------------------

            parsed = parse_json_response(
                result_text,
                EntityExtractionResponse,
            )

            # --------------------------------------------------
            # Store node-level extraction information.
            #
            # LayoutNode.metadata is intentionally used for
            # traceability and debugging.
            # --------------------------------------------------

            node.metadata[
                "entity_extraction"
            ] = parsed.model_dump()

            node.metadata[
                "entity_extraction_confidence"
            ] = parsed.confidence

            if parsed.notes:

                node.metadata[
                    "entity_extraction_notes"
                ] = parsed.notes

            # --------------------------------------------------
            # Convert schema entities into application
            # EntityState entities.
            # --------------------------------------------------

            for entity_index, extracted in enumerate(
                parsed.entities,
                start=1,
            ):

                entity_id = (
                    extracted.entity_id
                    or (
                        f"{node.node_id}"
                        f"_entity_{entity_index}"
                    )
                )

                entity = Entity(
                    entity_id=entity_id,

                    entity_type=(
                        extracted.entity_type
                    ),

                    value=(
                        extracted.text
                    ),

                    confidence=(
                        extracted.confidence
                    ),

                    page_number=(
                        node.page_number
                    ),

                    source_node=(
                        node.node_id
                    ),

                    normalized_value=(
                        extracted.normalized_text
                        or None
                    ),

                    metadata={
                        "attributes": (
                            extracted.attributes
                        ),

                        "extraction_metadata": (
                            extracted.metadata
                        ),

                        "start_offset": (
                            extracted.start_offset
                        ),

                        "end_offset": (
                            extracted.end_offset
                        ),

                        "layout_type": (
                            node.layout_type
                        ),

                        "extraction_confidence": (
                            parsed.confidence
                        ),

                        "extraction_notes": (
                            parsed.notes
                        ),
                    },
                )

                extracted_entities.append(
                    entity
                )

        # ------------------------------------------------------
        # EntityState is the source of truth.
        # ------------------------------------------------------

        state.entities.entities = (
            extracted_entities
        )

        # ------------------------------------------------------
        # Checkpoint
        # ------------------------------------------------------

        state.checkpoint.stage = (
            "entity_extraction_completed"
        )

        if self.logger:
            self.logger.info(
                "Entity Extraction Complete. "
                f"Extracted "
                f"{len(extracted_entities)} "
                "entity(s)."
            )

        return state