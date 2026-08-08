"""
End-to-end test for TitleExtractionAgent.

Run:

    python -m tests.test.title.extraction_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.title.title_extraction_agent import (
    TitleExtractionAgent,
)

from framework.prompts.prompt_registry import (
    PromptRegistry,
)

from framework.prompts.title_extraction_prompt import (
    TitleExtractionPrompt,
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
        "title_extraction",
        TitleExtractionPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = TitleExtractionAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Sample document
    # ==========================================================

    content = """
DISCHARGE SUMMARY

Patient Name: John Doe

HISTORY OF PRESENT ILLNESS

Patient was admitted with chest pain.

MEDICATIONS

Metformin 500 mg twice daily.
"""

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="title-extraction-test",
        ),

        document=DocumentState(
            document_id="doc-title-001",
            file_name="discharge_summary.txt",
            file_path="discharge_summary.txt",
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
                    node_id="title-001",
                    parent_id=None,
                    layout_type="title",
                    page_number=1,
                    text="DISCHARGE SUMMARY",
                    classification="Title",
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
            stage="title_extraction",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING TITLE EXTRACTION AGENT")
    print("=" * 80)

    result = await agent.execute(state)

    # ==========================================================
    # Results
    # ==========================================================

    print()
    print("=" * 80)
    print("TITLE EXTRACTION RESULT")
    print("=" * 80)

    for node in result.layout.nodes:

        extracted = node.metadata.get(
            "title_extraction"
        )

        if not extracted:
            continue

        print()

        print(
            "Original:",
            extracted.get(
                "original_text"
            ),
        )

        print(
            "Title:",
            extracted.get(
                "title"
            ),
        )

        print(
            "Title Type:",
            extracted.get(
                "title_type"
            ),
        )

        print(
            "Confidence:",
            extracted.get(
                "confidence"
            ),
        )

        notes = extracted.get(
            "notes"
        )

        if notes:
            print(
                "Notes:",
                notes,
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