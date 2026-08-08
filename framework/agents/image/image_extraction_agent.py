"""
Image/Figure Extraction Agent.

Responsible for extracting structural metadata
from image and figure layout regions.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.image_extraction_schema import (
    ImageFigureExtractionResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class ImageFigureExtractionAgent(BaseAgent):
    """
    Extract image and figure metadata from
    document layout nodes.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="image_figure_extraction_agent",
            description=(
                "Extracts structural information "
                "from document images and figures."
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
        Execute image/figure extraction.
        """

        if self.logger:

            self.logger.info(
                "Starting Image/Figure Extraction."
            )

        prompt_template = self.prompt_registry.get(
            "image_figure_extraction"
        )

        image_nodes = [
            node
            for node in state.layout.nodes
            if node.classification
            in {
                "Image",
                "image",
                "Figure",
                "figure",
                "Photograph",
                "photograph",
                "Diagram",
                "diagram",
                "Chart",
                "chart",
                "Graph",
                "graph",
                "Medical Image",
                "medical_image",
            }
        ]

        if self.logger:

            self.logger.info(
                f"Found {len(image_nodes)} "
                "image/figure node(s)."
            )

        for index, node in enumerate(
            image_nodes,
            start=1,
        ):

            prompt = prompt_template.build(
                text=node.text,
                page_number=node.page_number,
                layout_type=node.layout_type,
            )

            response = await self.router.chat(
                capability="image_figure_extraction",
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
                ImageFigureExtractionResponse,
            )

            node.metadata[
                "image_figure_extraction"
            ] = parsed.model_dump()

            node.metadata[
                "image_figure_confidence"
            ] = parsed.confidence

            node.metadata[
                "figure_index"
            ] = index

            if parsed.notes:

                node.metadata[
                    "image_figure_notes"
                ] = parsed.notes

        state.checkpoint.stage = (
            "image_figure_extraction_completed"
        )

        if self.logger:

            self.logger.info(
                "Image/Figure Extraction Complete."
            )

        return state