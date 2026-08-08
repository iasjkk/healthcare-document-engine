"""
Barcode / QR Extraction Agent.

Responsible for extracting and normalizing
barcode and QR-code information from document
layout regions.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.barcode_qr_extraction_schema import (
    BarcodeQRExtractionResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class BarcodeQRExtractionAgent(BaseAgent):
    """
    Extract barcode and QR-code information
    from document layout nodes.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="barcode_qr_extraction_agent",
            description=(
                "Extracts barcode and QR-code "
                "information from healthcare documents."
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
        Execute barcode / QR extraction.
        """

        if self.logger:

            self.logger.info(
                "Starting Barcode/QR Extraction."
            )

        prompt_template = self.prompt_registry.get(
            "barcode_qr_extraction"
        )

        barcode_nodes = [
            node
            for node in state.layout.nodes
            if node.classification
            in {
                "Barcode",
                "barcode",
                "QR",
                "QR Code",
                "qr",
                "qr_code",
                "Barcode/QR",
                "barcode_qr",
                "Data Matrix",
                "data_matrix",
            }
        ]

        if self.logger:

            self.logger.info(
                f"Found {len(barcode_nodes)} "
                "barcode/QR node(s)."
            )

        for index, node in enumerate(
            barcode_nodes,
            start=1,
        ):

            prompt = prompt_template.build(
                text=node.text,
                page_number=node.page_number,
                layout_type=node.layout_type,
            )

            response = await self.router.chat(
                capability="barcode_qr_extraction",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert healthcare "
                            "document structured-data "
                            "extraction system. "
                            "Return only valid JSON."
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
                BarcodeQRExtractionResponse,
            )

            node.metadata[
                "barcode_qr_extraction"
            ] = parsed.model_dump()

            node.metadata[
                "barcode_qr_confidence"
            ] = parsed.confidence

            node.metadata[
                "barcode_qr_index"
            ] = index

            if parsed.notes:

                node.metadata[
                    "barcode_qr_notes"
                ] = parsed.notes

        state.checkpoint.stage = (
            "barcode_qr_extraction_completed"
        )

        if self.logger:

            self.logger.info(
                "Barcode/QR Extraction Complete."
            )

        return state