"""
End-to-end test for SectionHeadingExtractionAgent.

Run:

    python -m tests.test.section.extraction_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.section.section_heading_extraction_agent import (
    SectionHeadingExtractionAgent,
)

from framework.prompts.prompt_registry import (
    PromptRegistry,
)

from framework.prompts.section_heading_extraction_prompt import (
    SectionHeadingExtractionPrompt,
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
        "section_heading_extraction",
        SectionHeadingExtractionPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = SectionHeadingExtractionAgent(

        router=router,

        prompt_registry=prompt_registry,

    )

    # ==========================================================
    # Sample Document
    # ==========================================================

    document_text = """
HISTORY OF PRESENT ILLNESS

Patient presents with chest pain for three days.

MEDICATIONS

Metformin 500 mg twice daily.

LABORATORY RESULTS

Hemoglobin: 13.2 g/dL
"""

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(

            run_id=str(uuid4()),

            workflow_id="section-heading-test",

        ),

        document=DocumentState(

            document_id="doc-section-001",

            file_name="clinical_report.txt",

            file_path="clinical_report.txt",

            file_type="text/plain",

            pages=[

                PageState(

                    page_number=1,

                    content=document_text,

                )

            ],

        ),

        layout=LayoutState(

            nodes=[

                LayoutNode(

                    node_id="heading-001",

                    parent_id=None,

                    layout_type="section_heading",

                    page_number=1,

                    text="HISTORY OF PRESENT ILLNESS",

                    classification="Section Heading",

                    confidence=0.99,

                ),

                LayoutNode(

                    node_id="heading-002",

                    parent_id=None,

                    layout_type="section_heading",

                    page_number=1,

                    text="MEDICATIONS",

                    classification="Section Heading",

                    confidence=0.99,

                ),

                LayoutNode(

                    node_id="heading-003",

                    parent_id=None,

                    layout_type="section_heading",

                    page_number=1,

                    text="LABORATORY RESULTS",

                    classification="Section Heading",

                    confidence=0.99,

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

            stage="section_heading_extraction",

        ),

    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()

    print("=" * 80)

    print("RUNNING SECTION HEADING EXTRACTION AGENT")

    print("=" * 80)

    result = await agent.execute(
        state
    )

    # ==========================================================
    # Results
    # ==========================================================

    print()

    print("=" * 80)

    print("SECTION HEADING RESULTS")

    print("=" * 80)

    for node in result.layout.nodes:

        if node.classification != "Section Heading":

            continue

        extracted = node.metadata.get(
            "section_heading"
        )

        print()

        print(
            "Node ID:",
            node.node_id,
        )

        print(
            "Original:",
            extracted.get(
                "original_text",
                "",
            ),
        )

        print(
            "Cleaned:",
            extracted.get(
                "text",
                "",
            ),
        )

        print(
            "Section Type:",
            extracted.get(
                "section_type",
                "",
            ),
        )

        print(
            "Level:",
            extracted.get(
                "level",
                "",
            ),
        )

        print(
            "Confidence:",
            extracted.get(
                "confidence",
                "",
            ),
        )

        notes = extracted.get(
            "notes",
            "",
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