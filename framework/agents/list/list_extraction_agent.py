"""
List Extraction Agent.

Responsible for extracting structured lists from
healthcare document layout nodes.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.list_extraction_schema import (
    ListExtractionResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class ListExtractionAgent(BaseAgent):
    """
    Extract structured lists from document nodes.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="list_extraction_agent",
            description=(
                "Extracts structured lists from "
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
        Execute list extraction.
        """

        if self.logger:

            self.logger.info(
                "Starting List Extraction."
            )

        prompt_template = self.prompt_registry.get(
            "list_extraction"
        )

        list_nodes = [
            node
            for node in state.layout.nodes
            if node.classification
            in {
                "List",
                "list",
                "ListItem",
                "list_item",
            }
        ]

        if self.logger:

            self.logger.info(
                f"Found {len(list_nodes)} "
                "list node(s)."
            )

        for node in list_nodes:

            prompt = prompt_template.build(
                text=node.text,
                page_number=node.page_number,
                layout_type=node.layout_type,
            )

            response = await self.router.chat(
                capability="list_extraction",
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
                ListExtractionResponse,
            )

            node.metadata[
                "list_extraction"
            ] = parsed.model_dump()

            node.metadata[
                "list_type"
            ] = parsed.list_type

            node.metadata[
                "list_confidence"
            ] = parsed.confidence

            if parsed.notes:

                node.metadata[
                    "list_notes"
                ] = parsed.notes

        state.checkpoint.stage = (
            "list_extraction_completed"
        )

        if self.logger:

            self.logger.info(
                "List Extraction Complete."
            )

        return state