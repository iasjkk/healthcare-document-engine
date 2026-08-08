"""
Healthcare Table Validation Agent.

Validates table extraction results stored on
LayoutNode metadata.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.table_validation_schema import (
    TableValidationResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class TableValidationAgent(BaseAgent):
    """
    Validate extracted healthcare tables.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="table_validation_agent",
            description=(
                "Validates extracted healthcare "
                "tables while preserving "
                "source traceability."
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
        Execute table validation.
        """

        if self.logger:

            self.logger.info(
                "Starting Table Validation."
            )

        prompt_template = self.prompt_registry.get(
            "table_validation"
        )

        table_nodes = [
            node
            for node in state.layout.nodes
            if node.layout_type
            and node.layout_type.upper() == "TABLE"
            and node.metadata.get(
                "table_extraction"
            )
        ]

        if self.logger:

            self.logger.info(
                f"Found {len(table_nodes)} "
                "table node(s) for validation."
            )

        if not table_nodes:

            if self.logger:

                self.logger.warning(
                    "No extracted tables found "
                    "for validation."
                )

            state.checkpoint.stage = (
                "table_validation_completed"
            )

            return state

        validated_count = 0
        warning_count = 0
        invalid_count = 0

        for node in table_nodes:

            # --------------------------------------------------
            # Existing extraction
            # --------------------------------------------------

            table_data = node.metadata.get(
                "table_extraction",
                {},
            )

            if not table_data:

                continue

            # --------------------------------------------------
            # Generate deterministic table ID.
            # --------------------------------------------------

            table_id = table_data.get(
                "table_id"
            )

            if not table_id:

                table_id = (
                    f"{node.node_id}_table"
                )

                table_data[
                    "table_id"
                ] = table_id

            # --------------------------------------------------
            # Prompt
            # --------------------------------------------------

            prompt = prompt_template.build(
                table=table_data,
                page_number=node.page_number,
                node_id=node.node_id,
            )

            # --------------------------------------------------
            # LLM
            # --------------------------------------------------

            response = await self.router.chat(
                capability="table_validation",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert healthcare "
                            "table validation system. "
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

            # --------------------------------------------------
            # Parse
            # --------------------------------------------------

            parsed = parse_json_response(
                result_text,
                TableValidationResponse,
            )

            validation = parsed.result

            # --------------------------------------------------
            # Enforce provenance
            # --------------------------------------------------

            validation.table_id = table_id

            # --------------------------------------------------
            # Basic application-level checks
            # --------------------------------------------------

            structural_issues = []

            headers = table_data.get(
                "headers",
                [],
            )

            rows = table_data.get(
                "rows",
                [],
            )

            cells = table_data.get(
                "cells",
                [],
            )

            if not isinstance(
                headers,
                list,
            ):

                structural_issues.append(
                    "Headers are not a list."
                )

            if not isinstance(
                rows,
                list,
            ):

                structural_issues.append(
                    "Rows are not a list."
                )

            if not isinstance(
                cells,
                list,
            ):

                structural_issues.append(
                    "Cells are not a list."
                )

            # --------------------------------------------------
            # Row/header consistency
            # --------------------------------------------------

            if (
                isinstance(headers, list)
                and isinstance(rows, list)
                and headers
            ):

                expected_columns = len(
                    headers
                )

                for row_index, row in enumerate(
                    rows
                ):

                    if not isinstance(
                        row,
                        list,
                    ):

                        structural_issues.append(
                            f"Row {row_index} "
                            "is not a list."
                        )

                        continue

                    if len(row) != expected_columns:

                        structural_issues.append(
                            f"Row {row_index} "
                            f"contains "
                            f"{len(row)} "
                            "value(s), expected "
                            f"{expected_columns}."
                        )

            # --------------------------------------------------
            # Final status
            # --------------------------------------------------

            issues = list(
                validation.issues
            )

            issues.extend(
                structural_issues
            )

            if structural_issues:

                final_status = "invalid"
                final_valid = False

                invalid_count += 1

            elif (
                validation.validation_status
                == "invalid"
            ):

                final_status = "invalid"
                final_valid = False

                invalid_count += 1

            elif (
                validation.validation_status
                == "warning"
            ):

                final_status = "warning"
                final_valid = True

                warning_count += 1

            else:

                final_status = "valid"
                final_valid = True

                validated_count += 1

            # --------------------------------------------------
            # Store validation result on LayoutNode.
            # --------------------------------------------------

            node.metadata[
                "table_validation"
            ] = {
                "table_id": table_id,
                "is_valid": final_valid,
                "validation_status": final_status,
                "confidence": validation.confidence,
                "issues": issues,
                "warnings": validation.warnings,
                "attributes": validation.attributes,
                "metadata": validation.metadata,
                "notes": parsed.notes,
            }

            # --------------------------------------------------
            # Preserve original table extraction.
            # --------------------------------------------------

            node.metadata[
                "table_extraction"
            ] = table_data

        # ------------------------------------------------------
        # Checkpoint
        # ------------------------------------------------------

        state.checkpoint.stage = (
            "table_validation_completed"
        )

        if self.logger:

            self.logger.info(
                "Table Validation Complete. "
                f"Valid: {validated_count}, "
                f"Warnings: {warning_count}, "
                f"Invalid: {invalid_count}."
            )

        return state