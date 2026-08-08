"""
Header Extraction Agent.

Responsible for identifying document headers.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.header_extraction_schema import (
    HeaderExtractionResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class HeaderExtractionAgent(BaseAgent):
    """
    Extract headers from document layout nodes.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="header_extraction_agent",
            description=(
                "Extracts document headers from "
                "healthcare documents."
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
        Execute header extraction.
        """

        if self.logger:

            self.logger.info(
                "Starting Header Extraction."
            )

        prompt_template = self.prompt_registry.get(
            "header_extraction"
        )

        header_nodes = [
            node
            for node in state.layout.nodes
            if node.classification
            in {
                "Header",
                "header",
                "Document Header",
                "document_header",
            }
        ]

        if self.logger:

            self.logger.info(
                f"Found {len(header_nodes)} "
                "header node(s)."
            )

        for node in header_nodes:

            prompt = prompt_template.build(
                text=node.text,
                page_number=node.page_number,
                layout_type=node.layout_type,
            )

            response = await self.router.chat(
                capability="header_extraction",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert healthcare "
                            "document structure extraction "
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

            parsed = parse_json_response(
                result_text,
                HeaderExtractionResponse,
            )

            node.metadata[
                "header_extraction"
            ] = parsed.model_dump()

            node.metadata[
                "header_confidence"
            ] = parsed.confidence

            if parsed.notes:

                node.metadata[
                    "header_notes"
                ] = parsed.notes

        state.checkpoint.stage = (
            "header_extraction_completed"
        )

        if self.logger:

            self.logger.info(
                "Header Extraction Complete."
            )

        return state