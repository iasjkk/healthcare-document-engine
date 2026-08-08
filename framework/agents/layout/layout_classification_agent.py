"""
Layout Classification Agent.

Responsible for:

- Classifying every LayoutNode
- Updating node.classification
- Updating node.confidence

Input
-----
WorkflowState.layout.nodes

Output
------
WorkflowState.layout.nodes
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent

from framework.router.model_router import ModelRouter

from framework.prompts.prompt_registry import PromptRegistry

from framework.schemas.layout_classification_schema import (
    LayoutClassificationResponse,
)

from framework.utils.json_parser import (
    parse_json_response,
)

from framework.state.workflow_state import WorkflowState


class LayoutClassificationAgent(BaseAgent):
    """
    Classifies every layout node.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(

            name="layout_classification_agent",

            description="Healthcare Layout Classification",

        )

        self.router = router

        self.prompt_registry = prompt_registry

    async def execute(
        self,
        state: WorkflowState,
    ) -> WorkflowState:

        if self.logger:

            self.logger.info(
                "Starting Layout Classification."
            )

        prompt_template = self.prompt_registry.get(
            "layout_classification"
        )

        total_nodes = len(state.layout.nodes)

        for index, node in enumerate(
            state.layout.nodes,
            start=1,
        ):

            if self.logger:

                self.logger.info(

                    f"[{index}/{total_nodes}] "

                    f"Classifying node "

                    f"{node.node_id}"

                )

            prompt = prompt_template.build(

                text=node.text,

                page_number=node.page_number,

                layout_type=node.layout_type,

            )

            response = await self.router.chat(

                capability="layout_classification",

                messages=[

                    {

                        "role": "system",

                        "content": (

                            "You are an expert "

                            "healthcare document "

                            "layout classifier."

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

                ["choices"][0]

                ["message"]

                ["content"]

            )

            parsed = parse_json_response(

                result_text,

                LayoutClassificationResponse,

            )

            node.classification = parsed.classification.value

            node.confidence = parsed.confidence

        state.checkpoint.stage = (
            "layout_classification_completed"
        )

        if self.logger:

            self.logger.info(

                "Layout Classification Complete."

            )

        return state