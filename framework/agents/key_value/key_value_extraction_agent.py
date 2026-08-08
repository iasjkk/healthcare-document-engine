"""
Key-Value Extraction Agent.

Responsible for extracting explicit key-value
pairs from healthcare document layout nodes.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.key_value_extraction_schema import (
    KeyValueExtractionResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class KeyValueExtractionAgent(BaseAgent):
    """
    Extract key-value pairs from key-value layout nodes.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="key_value_extraction_agent",
            description=(
                "Extracts structured key-value pairs "
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
        Execute key-value extraction.
        """

        if self.logger:
            self.logger.info(
                "Starting Key-Value Extraction."
            )

        prompt_template = self.prompt_registry.get(
            "key_value_extraction"
        )

        key_value_nodes = [
            node
            for node in state.layout.nodes
            if node.classification
            in {
                "Key-Value",
                "key_value",
                "KeyValue",
                "key-value",
            }
        ]

        if self.logger:
            self.logger.info(
                f"Found {len(key_value_nodes)} "
                "key-value node(s)."
            )

        for node in key_value_nodes:

            prompt = prompt_template.build(
                text=node.text,
                page_number=node.page_number,
                layout_type=node.layout_type,
            )

            response = await self.router.chat(
                capability="key_value_extraction",
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
                KeyValueExtractionResponse,
            )

            node.metadata[
                "key_value"
            ] = parsed.model_dump()

            node.metadata[
                "key_value_confidence"
            ] = parsed.confidence

            if parsed.notes:
                node.metadata[
                    "key_value_notes"
                ] = parsed.notes

        state.checkpoint.stage = (
            "key_value_extraction_completed"
        )

        if self.logger:
            self.logger.info(
                "Key-Value Extraction Complete."
            )

        return state