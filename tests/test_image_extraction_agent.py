"""
End-to-end test for ImageFigureExtractionAgent.

Run:

    python -m tests.test_image_extraction_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.image.image_extraction_agent import (
    ImageFigureExtractionAgent,
)

from framework.prompts.image_extraction_prompt import (
    ImageFigureExtractionPrompt,
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
        "image_figure_extraction",
        ImageFigureExtractionPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = ImageFigureExtractionAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Sample document
    # ==========================================================

    content = """
PATHOLOGY REPORT

Figure 1: Histopathology image of tissue sample.

The image contains an associated caption.

Figure 2: Diagnostic workflow diagram.

Figure 3: Patient treatment pathway.
"""

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="image-figure-extraction-test",
        ),

        document=DocumentState(
            document_id="doc-image-001",
            file_name="pathology_report.txt",
            file_path="pathology_report.txt",
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
                    node_id="figure-001",
                    parent_id=None,
                    layout_type="figure",
                    page_number=1,
                    text=(
                        "Figure 1: Histopathology "
                        "image of tissue sample."
                    ),
                    classification="Figure",
                ),
                LayoutNode(
                    node_id="figure-002",
                    parent_id=None,
                    layout_type="diagram",
                    page_number=1,
                    text=(
                        "Figure 2: Diagnostic "
                        "workflow diagram."
                    ),
                    classification="Diagram",
                ),
                LayoutNode(
                    node_id="figure-003",
                    parent_id=None,
                    layout_type="figure",
                    page_number=1,
                    text=(
                        "Figure 3: Patient "
                        "treatment pathway."
                    ),
                    classification="Figure",
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
            stage="image_figure_extraction",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING IMAGE/FIGURE EXTRACTION AGENT")
    print("=" * 80)

    result = await agent.execute(state)

    # ==========================================================
    # Results
    # ==========================================================

    print()
    print("=" * 80)
    print("IMAGE/FIGURE EXTRACTION RESULT")
    print("=" * 80)

    for node in result.layout.nodes:

        extracted = node.metadata.get(
            "image_figure_extraction"
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

        for figure in extracted.get(
            "figures",
            [],
        ):

            print(
                f"- Figure ID: "
                f"{figure.get('figure_id')}"
            )

            print(
                f"  Title: "
                f"{figure.get('title')}"
            )

            print(
                f"  Type: "
                f"{figure.get('figure_type')}"
            )

            print(
                f"  Description: "
                f"{figure.get('description')}"
            )

            print(
                f"  Page: "
                f"{figure.get('page_number')}"
            )

            print(
                f"  Caption: "
                f"{figure.get('caption')}"
            )

            print(
                f"  Confidence: "
                f"{figure.get('confidence')}"
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