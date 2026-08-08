"""
Chart/Graph Extraction Agent.

Responsible for extracting structural information
from chart and graph layout nodes.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.chart_graph_extraction_schema import (
    ChartGraphExtractionResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class ChartGraphExtractionAgent(BaseAgent):
    """
    Extract chart and graph information from
    document layout nodes.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="chart_graph_extraction_agent",
            description=(
                "Extracts structural information "
                "from charts and graphs."
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
        Execute chart/graph extraction.
        """

        if self.logger:

            self.logger.info(
                "Starting Chart/Graph Extraction."
            )

        prompt_template = self.prompt_registry.get(
            "chart_graph_extraction"
        )

        chart_nodes = [
            node
            for node in state.layout.nodes
            if node.classification
            in {
                "Chart",
                "chart",
                "Graph",
                "graph",
                "Bar Chart",
                "bar_chart",
                "Line Chart",
                "line_chart",
                "Pie Chart",
                "pie_chart",
                "Histogram",
                "histogram",
                "Scatter Plot",
                "scatter_plot",
            }
        ]

        if self.logger:

            self.logger.info(
                f"Found {len(chart_nodes)} "
                "chart/graph node(s)."
            )

        for index, node in enumerate(
            chart_nodes,
            start=1,
        ):

            prompt = prompt_template.build(
                text=node.text,
                page_number=node.page_number,
                layout_type=node.layout_type,
            )

            response = await self.router.chat(
                capability="chart_graph_extraction",
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
                ChartGraphExtractionResponse,
            )

            node.metadata[
                "chart_graph_extraction"
            ] = parsed.model_dump()

            node.metadata[
                "chart_graph_confidence"
            ] = parsed.confidence

            node.metadata[
                "chart_graph_index"
            ] = index

            if parsed.notes:

                node.metadata[
                    "chart_graph_notes"
                ] = parsed.notes

        state.checkpoint.stage = (
            "chart_graph_extraction_completed"
        )

        if self.logger:

            self.logger.info(
                "Chart/Graph Extraction Complete."
            )

        return state