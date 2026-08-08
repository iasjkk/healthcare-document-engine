"""
Footer Extraction Agent.

Responsible for identifying document footers.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.footer_extraction_schema import (
    FooterExtractionResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class FooterExtractionAgent(BaseAgent):
    """
    Extract footers from document layout nodes.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="footer_extraction_agent",
            description=(
                "Extracts document footers from "
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
        Execute footer extraction.
        """

        if self.logger:

            self.logger.info(
                "Starting Footer Extraction."
            )

        prompt_template = self.prompt_registry.get(
            "footer_extraction"
        )

        footer_nodes = [
            node
            for node in state.layout.nodes
            if node.classification
            in {
                "Footer",
                "footer",
                "Document Footer",
                "document_footer",
            }
        ]

        if self.logger:

            self.logger.info(
                f"Found {len(footer_nodes)} "
                "footer node(s)."
            )

        for node in footer_nodes:

            prompt = prompt_template.build(
                text=node.text,
                page_number=node.page_number,
                layout_type=node.layout_type,
            )

            response = await self.router.chat(
                capability="footer_extraction",
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
                FooterExtractionResponse,
            )

            node.metadata[
                "footer_extraction"
            ] = parsed.model_dump()

            node.metadata[
                "footer_confidence"
            ] = parsed.confidence

            if parsed.notes:

                node.metadata[
                    "footer_notes"
                ] = parsed.notes

        state.checkpoint.stage = (
            "footer_extraction_completed"
        )

        if self.logger:

            self.logger.info(
                "Footer Extraction Complete."
            )

        return state