from __future__ import annotations

from typing import Any

from framework.core.base_agent import BaseAgent
from framework.state.workflow_state import WorkflowState

# Keep these imports exactly as they exist in your current file.
# They are shown here based on the code you provided.
from framework.schemas.final_report_schema import FinalReportResponse
from framework.utils.json_parser import parse_json_response


class FinalReportAgent(BaseAgent):
    """
    Generates the final clinical report.
    """

    def __init__(
        self,
        router: Any,
        prompt_registry: Any,
        logger: Any | None = None,
    ) -> None:

        super().__init__(
            name="final_report",
            description="Generates the final clinical report.",
            version="1.0.0",
        )

        self.router = router
        self.prompt_registry = prompt_registry

        if logger is not None:
            self.logger = logger

    async def execute(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        """
        Generate the final clinical report.
        """

        if self.logger:
            self.logger.info(
                "Starting Final Report Agent."
            )

        # ------------------------------------------------------
        # Document
        # ------------------------------------------------------

        document_data = {
            "document_id": (
                state.document.document_id
            ),
            "file_name": (
                state.document.file_name
            ),
            "file_path": (
                state.document.file_path
            ),
            "file_type": (
                state.document.file_type
            ),
            "pages": [
                {
                    "page_number": page.page_number,
                    "content": page.content,
                }
                for page in state.document.pages
            ],
        }

        # ------------------------------------------------------
        # Clinical Summary
        # ------------------------------------------------------

        clinical_summary = (
            state.clinical_summary.model_dump(
                mode="json"
            )
        )

        # ------------------------------------------------------
        # Entities
        # ------------------------------------------------------

        entities = (
            state.entities.model_dump(
                mode="json"
            )
        )

        # ------------------------------------------------------
        # Relations
        # ------------------------------------------------------

        relations = (
            state.relations.model_dump(
                mode="json"
            )
        )

        # ------------------------------------------------------
        # Validation
        # ------------------------------------------------------

        validation = (
            state.validation.model_dump(
                mode="json"
            )
        )

        # ------------------------------------------------------
        # Prompt
        # ------------------------------------------------------

        prompt_template = (
            self.prompt_registry.get(
                "final_report"
            )
        )

        prompt = prompt_template.build(
            document_data=document_data,
            clinical_summary=clinical_summary,
            entities=entities,
            relations=relations,
            validation=validation,
        )

        # ------------------------------------------------------
        # LLM
        # ------------------------------------------------------

        response = await self.router.chat(
            capability="final_report",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert healthcare "
                        "clinical report generation system. "
                        "Return only valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        # ------------------------------------------------------
        # Response extraction
        # ------------------------------------------------------

        result_text = (
            response[
                "choices"
            ][0][
                "message"
            ][
                "content"
            ]
        )

        # ------------------------------------------------------
        # Parse
        # ------------------------------------------------------

        parsed = parse_json_response(
            result_text,
            FinalReportResponse,
        )

        # ------------------------------------------------------
        # Store final report
        #
        # WorkflowState does not currently have a
        # final_report field.
        # ------------------------------------------------------

        state.clinical_summary.metadata[
            "final_report"
        ] = parsed.model_dump(
            mode="json"
        )

        # ------------------------------------------------------
        # Store generation metadata
        # ------------------------------------------------------

        state.clinical_summary.metadata[
            "final_report_generation"
        ] = {
            "confidence": parsed.confidence,
            "validation_status": (
                parsed.validation_status
            ),
            "notes": parsed.notes,
        }

        # ------------------------------------------------------
        # Checkpoint
        # ------------------------------------------------------

        state.checkpoint.stage = (
            "final_report_completed"
        )

        # ------------------------------------------------------
        # Logging
        # ------------------------------------------------------

        if self.logger:
            self.logger.info(
                "Final Report Agent completed. "
                f"Confidence={parsed.confidence}"
            )

        return state