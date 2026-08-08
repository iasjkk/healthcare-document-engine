"""
Section Heading Extraction Agent.

Responsible for:

- Finding section-heading layout nodes.
- Structuring heading text.
- Classifying broad section type.
- Determining heading hierarchy.
- Validating the LLM response.
- Storing the result in node.metadata["section_heading"].
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.section_heading_extraction_schema import (
    SectionHeadingExtractionResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class SectionHeadingExtractionAgent(BaseAgent):
    """
    Extract and structure section headings.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="section_heading_extraction_agent",
            description=(
                "Extracts and structures section headings "
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
        Extract all section-heading nodes.
        """

        if self.logger:

            self.logger.info(
                "Starting Section Heading Extraction."
            )

        prompt_template = self.prompt_registry.get(
            "section_heading_extraction"
        )

        heading_nodes = [

            node

            for node in state.layout.nodes

            if node.classification
            in {
                "Section Heading",
                "section_heading",
                "SectionHeading",
            }

        ]

        total = len(heading_nodes)

        if self.logger:

            self.logger.info(
                f"Found {total} section heading node(s)."
            )

        for index, node in enumerate(
            heading_nodes,
            start=1,
        ):

            if self.logger:

                self.logger.info(
                    f"[{index}/{total}] "
                    f"Processing heading "
                    f"{node.node_id}."
                )

            prompt = prompt_template.build(

                text=node.text,

                page_number=node.page_number,

                layout_type=node.layout_type,

            )

            response = await self.router.chat(

                capability="section_heading_extraction",

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

                response
                ["choices"]
                [0]
                ["message"]
                ["content"]

            )

            parsed = parse_json_response(

                result_text,

                SectionHeadingExtractionResponse,

            )

            node.metadata[
                "section_heading"
            ] = parsed.model_dump()

            node.metadata[
                "section_heading_confidence"
            ] = parsed.confidence

            if parsed.notes:

                node.metadata[
                    "section_heading_notes"
                ] = parsed.notes

            if self.logger:

                self.logger.info(
                    f"Heading {node.node_id} "
                    f"processed successfully."
                )

        state.checkpoint.stage = (
            "section_heading_extraction_completed"
        )

        if self.logger:

            self.logger.info(
                "Section Heading Extraction Complete."
            )

        return state