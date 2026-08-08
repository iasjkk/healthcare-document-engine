"""
Paragraph Extraction Agent.

Responsible for:

- Finding layout nodes classified as paragraphs.
- Sending paragraph content to the configured LLM.
- Cleaning OCR/document text.
- Validating the LLM response with Pydantic.
- Storing the extracted paragraph in node.metadata["paragraph"].
- Updating workflow checkpoint state.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.paragraph_extraction_schema import (
    ParagraphExtractionResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class ParagraphExtractionAgent(BaseAgent):
    """
    Extract and clean paragraph content from healthcare documents.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="paragraph_extraction_agent",
            description=(
                "Extracts and cleans paragraph content "
                "from healthcare documents."
            ),
            version="1.0.0",
        )

        self.router = router
        self.prompt_registry = prompt_registry

    # ==========================================================
    # Execute
    # ==========================================================

    async def execute(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        """
        Extract all paragraph nodes from the document layout.
        """

        if self.logger:
            self.logger.info(
                "Starting Paragraph Extraction."
            )

        # ------------------------------------------------------
        # Get Prompt
        # ------------------------------------------------------

        prompt_template = self.prompt_registry.get(
            "paragraph_extraction"
        )

        # ------------------------------------------------------
        # Find Paragraph Nodes
        # ------------------------------------------------------

        paragraph_nodes = [

            node

            for node in state.layout.nodes

            if node.classification == "Paragraph"

        ]

        total_paragraphs = len(
            paragraph_nodes
        )

        if self.logger:
            self.logger.info(
                f"Found {total_paragraphs} "
                f"paragraph node(s)."
            )

        # ------------------------------------------------------
        # Process Paragraphs
        # ------------------------------------------------------

        for index, node in enumerate(
            paragraph_nodes,
            start=1,
        ):

            if self.logger:

                self.logger.info(
                    f"[{index}/{total_paragraphs}] "
                    f"Extracting paragraph node "
                    f"{node.node_id}."
                )

            # --------------------------------------------------
            # Build Prompt
            # --------------------------------------------------

            prompt = prompt_template.build(

                text=node.text,

                page_number=node.page_number,

                layout_type=node.layout_type,

            )

            # --------------------------------------------------
            # LLM Request
            # --------------------------------------------------

            response = await self.router.chat(

                capability="paragraph_extraction",

                messages=[

                    {
                        "role": "system",
                        "content": (
                            "You are an expert "
                            "healthcare document "
                            "processing system. "
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
            # Extract Model Response
            # --------------------------------------------------

            result_text = (

                response
                ["choices"]
                [0]
                ["message"]
                ["content"]

            )

            # --------------------------------------------------
            # Validate Response
            # --------------------------------------------------

            parsed = parse_json_response(

                result_text,

                ParagraphExtractionResponse,

            )

            # --------------------------------------------------
            # Store Result
            # --------------------------------------------------

            node.metadata["paragraph"] = (
                parsed.model_dump()
            )

            node.metadata[
                "paragraph_confidence"
            ] = parsed.confidence

            if parsed.notes:

                node.metadata[
                    "paragraph_notes"
                ] = parsed.notes

            if self.logger:

                self.logger.info(
                    f"Paragraph node "
                    f"{node.node_id} "
                    f"extracted successfully."
                )

        # ------------------------------------------------------
        # Update Checkpoint
        # ------------------------------------------------------

        state.checkpoint.stage = (
            "paragraph_extraction_completed"
        )

        if self.logger:

            self.logger.info(
                "Paragraph Extraction Complete."
            )

        return state