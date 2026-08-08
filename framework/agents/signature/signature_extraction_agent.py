"""
Signature Extraction Agent.

Responsible for identifying signatures and
signature-related regions.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.signature_extraction_schema import (
    SignatureExtractionResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class SignatureExtractionAgent(BaseAgent):
    """
    Extract signatures from document layout nodes.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="signature_extraction_agent",
            description=(
                "Extracts signatures from "
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
        Execute signature extraction.
        """

        if self.logger:

            self.logger.info(
                "Starting Signature Extraction."
            )

        prompt_template = self.prompt_registry.get(
            "signature_extraction"
        )

        signature_nodes = [
            node
            for node in state.layout.nodes
            if node.classification
            in {
                "Signature",
                "signature",
                "Signature Line",
                "signature_line",
                "Electronic Signature",
                "electronic_signature",
            }
        ]

        if self.logger:

            self.logger.info(
                f"Found {len(signature_nodes)} "
                "signature node(s)."
            )

        for node in signature_nodes:

            prompt = prompt_template.build(
                text=node.text,
                page_number=node.page_number,
                layout_type=node.layout_type,
            )

            response = await self.router.chat(
                capability="signature_extraction",
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
                SignatureExtractionResponse,
            )

            node.metadata[
                "signature_extraction"
            ] = parsed.model_dump()

            node.metadata[
                "signature_confidence"
            ] = parsed.confidence

            if parsed.notes:

                node.metadata[
                    "signature_notes"
                ] = parsed.notes

        state.checkpoint.stage = (
            "signature_extraction_completed"
        )

        if self.logger:

            self.logger.info(
                "Signature Extraction Complete."
            )

        return state