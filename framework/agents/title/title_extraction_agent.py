"""
Title Extraction Agent.

Responsible for extracting document-level titles.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.title_extraction_schema import (
    TitleExtractionResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class TitleExtractionAgent(BaseAgent):
    """
    Extract document titles from layout nodes.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="title_extraction_agent",
            description=(
                "Extracts document-level titles "
                "from healthcare documents."
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
        Execute title extraction.
        """

        if self.logger:
            self.logger.info(
                "Starting Title Extraction."
            )

        prompt_template = self.prompt_registry.get(
            "title_extraction"
        )

        title_nodes = [
            node
            for node in state.layout.nodes
            if node.classification
            in {
                "Title",
                "title",
                "Document Title",
                "document_title",
            }
        ]

        if self.logger:
            self.logger.info(
                f"Found {len(title_nodes)} "
                "title node(s)."
            )

        for node in title_nodes:

            prompt = prompt_template.build(
                text=node.text,
                page_number=node.page_number,
                layout_type=node.layout_type,
            )

            response = await self.router.chat(
                capability="title_extraction",
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
                TitleExtractionResponse,
            )

            node.metadata[
                "title_extraction"
            ] = parsed.model_dump()

            node.metadata[
                "title"
            ] = parsed.title

            node.metadata[
                "title_type"
            ] = parsed.title_type

            node.metadata[
                "title_confidence"
            ] = parsed.confidence

            if parsed.notes:
                node.metadata[
                    "title_notes"
                ] = parsed.notes

        state.checkpoint.stage = (
            "title_extraction_completed"
        )

        if self.logger:
            self.logger.info(
                "Title Extraction Complete."
            )

        return state