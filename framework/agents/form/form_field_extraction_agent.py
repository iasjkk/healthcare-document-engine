"""
Form Field Extraction Agent.

Responsible for extracting structured fields
from healthcare forms.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.form_field_extraction_schema import (
    FormFieldExtractionResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class FormFieldExtractionAgent(BaseAgent):
    """
    Extract form fields from layout nodes.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="form_field_extraction_agent",
            description=(
                "Extracts structured form fields "
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
        Execute form field extraction.
        """

        if self.logger:

            self.logger.info(
                "Starting Form Field Extraction."
            )

        prompt_template = self.prompt_registry.get(
            "form_field_extraction"
        )

        form_nodes = [
            node
            for node in state.layout.nodes
            if node.classification
            in {
                "Form",
                "form",
                "Form Field",
                "form_field",
                "Field",
                "field",
            }
        ]

        if self.logger:

            self.logger.info(
                f"Found {len(form_nodes)} "
                "form node(s)."
            )

        for node in form_nodes:

            prompt = prompt_template.build(
                text=node.text,
                page_number=node.page_number,
                layout_type=node.layout_type,
            )

            response = await self.router.chat(
                capability="form_field_extraction",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert healthcare "
                            "structured-data extraction "
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
                FormFieldExtractionResponse,
            )

            node.metadata[
                "form_field_extraction"
            ] = parsed.model_dump()

            node.metadata[
                "form_field_confidence"
            ] = parsed.confidence

            if parsed.notes:

                node.metadata[
                    "form_field_notes"
                ] = parsed.notes

        state.checkpoint.stage = (
            "form_field_extraction_completed"
        )

        if self.logger:

            self.logger.info(
                "Form Field Extraction Complete."
            )

        return state