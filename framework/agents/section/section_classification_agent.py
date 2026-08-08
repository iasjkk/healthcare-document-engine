"""
Healthcare Section Classification Agent.

Classifies document layout nodes into semantic
healthcare/document sections.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.section_classification_schema import (
    SectionClassificationResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class SectionClassificationAgent(BaseAgent):
    """
    Classify document sections.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="section_classification_agent",
            description=(
                "Classifies healthcare document "
                "layout nodes into semantic sections."
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
        Execute section classification.
        """

        if self.logger:

            self.logger.info(
                "Starting Section Classification."
            )

        prompt_template = self.prompt_registry.get(
            "section_classification"
        )

        # --------------------------------------------------
        # Select meaningful nodes.
        # --------------------------------------------------

        nodes = [
            node
            for node in state.layout.nodes
            if node.text
            and node.text.strip()
        ]

        if self.logger:

            self.logger.info(
                f"Processing {len(nodes)} "
                "node(s) for section classification."
            )

        classified_count = 0

        # --------------------------------------------------
        # Process nodes.
        # --------------------------------------------------

        for node in nodes:

            # --------------------------------------------------
            # Existing TABLE nodes.
            #
            # Do not ask the LLM to reinterpret them.
            # --------------------------------------------------

            if (
                node.layout_type
                and node.layout_type.upper()
                == "TABLE"
            ):

                node.metadata[
                    "section_classification"
                ] = {
                    "node_id": node.node_id,
                    "section": "TABLE",
                    "confidence": (
                        node.confidence
                        if node.confidence is not None
                        else 1.0
                    ),
                    "reasoning": (
                        "Node is explicitly "
                        "classified as TABLE."
                    ),
                    "attributes": {},
                }

                classified_count += 1

                continue

            # --------------------------------------------------
            # Prompt
            # --------------------------------------------------

            prompt = prompt_template.build(
                text=node.text,
                node_id=node.node_id,
                page_number=node.page_number,
                layout_type=node.layout_type,
            )

            # --------------------------------------------------
            # LLM
            # --------------------------------------------------

            response = await self.router.chat(
                capability="section_classification",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert healthcare "
                            "document section classification "
                            "system. Return only valid JSON."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

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
                SectionClassificationResponse,
            )

            result = parsed.result

            # --------------------------------------------------
            # Enforce provenance.
            # --------------------------------------------------

            result.node_id = node.node_id

            # --------------------------------------------------
            # Application-level safeguards.
            # --------------------------------------------------

            if not result.section:

                result.section = "OTHER"

            # --------------------------------------------------
            # Store result on LayoutNode.
            # --------------------------------------------------

            node.metadata[
                "section_classification"
            ] = {
                "node_id": node.node_id,
                "section": result.section,
                "confidence": result.confidence,
                "reasoning": result.reasoning,
                "attributes": result.attributes,
                "notes": parsed.notes,
            }

            classified_count += 1

        # --------------------------------------------------
        # Checkpoint
        # --------------------------------------------------

        state.checkpoint.stage = (
            "section_classification_completed"
        )

        if self.logger:

            self.logger.info(
                "Section Classification Complete. "
                f"Classified "
                f"{classified_count} "
                "node(s)."
            )

        return state