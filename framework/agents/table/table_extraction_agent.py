"""
Table Extraction Agent.

Responsible for:

- Finding layout nodes classified as tables.
- Sending each table to the configured LLM.
- Parsing and validating the LLM response.
- Storing the extracted table in node.metadata["table"].
- Updating workflow checkpoint state.

The agent processes one table node at a time so that:

- failures are isolated,
- retries can be implemented later,
- large documents do not create unnecessarily large prompts,
- individual table extraction can be logged and debugged.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.table_extraction_schema import (
    TableExtractionResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class TableExtractionAgent(BaseAgent):
    """
    Extract structured tables from classified layout nodes.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="table_extraction_agent",
            description=(
                "Extracts structured tables from "
                "healthcare documents."
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
        Extract all tables present in the layout state.
        """

        if self.logger:
            self.logger.info(
                "Starting Table Extraction."
            )

        # ------------------------------------------------------
        # Get Prompt
        # ------------------------------------------------------

        prompt_template = self.prompt_registry.get(
            "table_extraction"
        )

        # ------------------------------------------------------
        # Find Table Nodes
        # ------------------------------------------------------

        table_nodes = [

            node

            for node in state.layout.nodes

            if node.classification == "Table"

        ]

        total_tables = len(table_nodes)

        if self.logger:

            self.logger.info(
                f"Found {total_tables} table node(s)."
            )

        # ------------------------------------------------------
        # Process Tables
        # ------------------------------------------------------

        for index, node in enumerate(
            table_nodes,
            start=1,
        ):

            if self.logger:

                self.logger.info(
                    f"[{index}/{total_tables}] "
                    f"Extracting table node "
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

                capability="table_extraction",

                messages=[

                    {
                        "role": "system",
                        "content": (
                            "You are an expert "
                            "healthcare document "
                            "table extraction system. "
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
            # Extract Message Content
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

                TableExtractionResponse,

            )

            # --------------------------------------------------
            # Store Result
            # --------------------------------------------------

            node.metadata["table"] = (
                parsed.model_dump()
            )

            # Keep extraction confidence separately so
            # downstream agents can access it easily.

            node.metadata["table_confidence"] = (
                parsed.confidence
            )

            if parsed.notes:

                node.metadata["table_notes"] = (
                    parsed.notes
                )

            if self.logger:

                self.logger.info(
                    f"Table node {node.node_id} "
                    f"extracted successfully."
                )

        # ------------------------------------------------------
        # Update Checkpoint
        # ------------------------------------------------------

        state.checkpoint.stage = (
            "table_extraction_completed"
        )

        if self.logger:

            self.logger.info(
                "Table Extraction Complete."
            )

        return state