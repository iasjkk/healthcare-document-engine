"""
Document Structure Agent.

Responsible for:

- Understanding document hierarchy
- Detecting sections
- Detecting tables
- Detecting paragraphs
- Creating layout representation
"""

from __future__ import annotations

import json
from typing import Any


from framework.core.base_agent import BaseAgent
from framework.router.model_router import ModelRouter
from framework.prompts.prompt_registry import PromptRegistry

from framework.state.workflow_state import WorkflowState
from framework.state.layout_state import LayoutNode


class DocumentStructureAgent(BaseAgent):
    """
    First stage healthcare document agent.
    """


    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:


        super().__init__(
            name="document_structure_agent",
            description=(
                "Analyzes healthcare document structure"
            ),
        )


        self.router = router

        self.prompt_registry = prompt_registry



    async def execute(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        """
        Execute document structure extraction.
        """


        # ------------------------------------
        # Collect document content
        # ------------------------------------

        document_content = "\n\n".join(

            page.content

            for page in state.document.pages

        )


        # ------------------------------------
        # Build Prompt
        # ------------------------------------

        prompt = (
            self.prompt_registry
            .get("document_structure")
            .build(
                document_content=document_content
            )
        )


        # ------------------------------------
        # LLM Call
        # ------------------------------------

        response = await self.router.chat(

            capability="document_structure",

            messages=[

                {
                    "role": "system",
                    "content": (
                        "You are a healthcare "
                        "document analysis expert."
                    ),
                },

                {
                    "role": "user",
                    "content": prompt,
                },

            ],

        )


        # ------------------------------------
        # Extract Response
        # ------------------------------------

        result_text = (

            response
            ["choices"]
            [0]
            ["message"]
            ["content"]

        )


        # ------------------------------------
        # Parse JSON
        # ------------------------------------

        try:

            structured_data = json.loads(
                result_text
            )

        except json.JSONDecodeError:

            structured_data = {

                "raw_response": result_text

            }


        # ------------------------------------
        # Update Layout State
        # ------------------------------------

        state.layout.nodes = [

            LayoutNode(

                node_id=str(index),

                layout_type=node.get(
                    "type",
                    "section"
                ),

                page_number=node.get(
                    "page_number",
                    1
                ),

                text=node.get(
                    "text",
                    ""
                ),

            )

            for index, node in enumerate(
                structured_data.get(
                    "sections",
                    []
                )
            )

        ]


        # ------------------------------------
        # Update checkpoint
        # ------------------------------------

        state.checkpoint.stage = (
            "document_structure_completed"
        )


        return state