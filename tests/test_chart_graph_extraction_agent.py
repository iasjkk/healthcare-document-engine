"""
End-to-end test for ChartGraphExtractionAgent.

Run:

    python -m tests.test_chart_graph_extraction_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.chart.chart_graph_extraction_agent import (
    ChartGraphExtractionAgent,
)

from framework.prompts.chart_graph_extraction_prompt import (
    ChartGraphExtractionPrompt,
)

from framework.prompts.prompt_registry import (
    PromptRegistry,
)

from framework.providers.openrouter_provider import (
    OpenRouterProvider,
)

from framework.registry.provider_registry import (
    ProviderRegistry,
)

from framework.router.model_router import (
    ModelRouter,
)

from framework.state.checkpoint_state import (
    CheckpointState,
)

from framework.state.document_state import (
    DocumentState,
    PageState,
)

from framework.state.entity_state import (
    EntityState,
)

from framework.state.execution_state import (
    ExecutionState,
)

from framework.state.layout_state import (
    LayoutNode,
    LayoutState,
)

from framework.state.metrics_state import (
    MetricsState,
)

from framework.state.model_state import (
    ModelState,
)

from framework.state.validation_state import (
    ValidationState,
)

from framework.state.workflow_state import (
    WorkflowState,
)


async def main() -> None:

    # ==========================================================
    # Provider
    # ==========================================================

    provider = OpenRouterProvider()

    provider_registry = ProviderRegistry()

    provider_registry.register(
        "openrouter",
        provider,
    )

    router = ModelRouter(
        provider_registry
    )

    # ==========================================================
    # Prompt Registry
    # ==========================================================

    prompt_registry = PromptRegistry()

    prompt_registry.register(
        "chart_graph_extraction",
        ChartGraphExtractionPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = ChartGraphExtractionAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Sample chart
    # ==========================================================

    content = """
Figure 4: Monthly Patient Admissions

Line chart.

X-axis: Month

Y-axis: Patient Count

Legend:
Emergency
Outpatient

January:
Emergency 120
Outpatient 300

February:
Emergency 135
Outpatient 325

March:
Emergency 150
Outpatient 350
"""

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="chart-graph-extraction-test",
        ),

        document=DocumentState(
            document_id="doc-chart-001",
            file_name="admissions_report.txt",
            file_path="admissions_report.txt",
            file_type="text/plain",
            pages=[
                PageState(
                    page_number=1,
                    content=content,
                )
            ],
        ),

        layout=LayoutState(
            nodes=[
                LayoutNode(
                    node_id="chart-001",
                    parent_id=None,
                    layout_type="chart",
                    page_number=1,
                    text=content,
                    classification="Chart",
                ),
            ]
        ),

        entities=EntityState(),

        validation=ValidationState(),

        model=ModelState(),

        metrics=MetricsState(),

        checkpoint=CheckpointState(
            checkpoint_id=str(uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            stage="chart_graph_extraction",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING CHART/GRAPH EXTRACTION AGENT")
    print("=" * 80)

    result = await agent.execute(state)

    # ==========================================================
    # Results
    # ==========================================================

    print()
    print("=" * 80)
    print("CHART/GRAPH EXTRACTION RESULT")
    print("=" * 80)

    for node in result.layout.nodes:

        extracted = node.metadata.get(
            "chart_graph_extraction"
        )

        if not extracted:
            continue

        print()

        print(
            "Overall Confidence:",
            extracted.get(
                "confidence"
            ),
        )

        for chart in extracted.get(
            "charts",
            [],
        ):

            print(
                f"- Chart ID: "
                f"{chart.get('chart_id')}"
            )

            print(
                f"  Title: "
                f"{chart.get('title')}"
            )

            print(
                f"  Type: "
                f"{chart.get('chart_type')}"
            )

            print(
                f"  X Axis: "
                f"{chart.get('x_axis_label')}"
            )

            print(
                f"  Y Axis: "
                f"{chart.get('y_axis_label')}"
            )

            print(
                f"  Legend: "
                f"{chart.get('legend')}"
            )

            print(
                f"  Description: "
                f"{chart.get('description')}"
            )

            print(
                f"  Confidence: "
                f"{chart.get('confidence')}"
            )

            for series in chart.get(
                "series",
                [],
            ):

                print(
                    f"  Series: "
                    f"{series.get('name')}"
                )

                for value in series.get(
                    "values",
                    [],
                ):

                    print(
                        f"    "
                        f"{value.get('label')}: "
                        f"{value.get('value')}"
                    )

    # ==========================================================
    # Checkpoint
    # ==========================================================

    print()
    print("=" * 80)
    print("CHECKPOINT")
    print("=" * 80)

    print(
        result.checkpoint.stage
    )

    # ==========================================================
    # Cleanup
    # ==========================================================

    await provider.disconnect()


if __name__ == "__main__":

    asyncio.run(main())