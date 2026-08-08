"""
End-to-end test for ParagraphExtractionAgent.

Run from the project root:

    python -m tests.test.paragraph.extraction_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.paragraph.paragraph_extraction_agent import (
    ParagraphExtractionAgent,
)

from framework.prompts.paragraph_extraction_prompt import (
    ParagraphExtractionPrompt,
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
        "paragraph_extraction",
        ParagraphExtractionPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = ParagraphExtractionAgent(

        router=router,

        prompt_registry=prompt_registry,

    )

    # ==========================================================
    # Sample Healthcare Document
    # ==========================================================

    paragraph_text = (
        "Patlent c/o chest pain x 3 days. "
        "Denies shortness of breath. "
        "Past history of hypertension."
    )

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(

            run_id=str(uuid4()),

            workflow_id="paragraph-extraction-test",

        ),

        document=DocumentState(

            document_id="doc-paragraph-001",

            file_name="clinical_note.txt",

            file_path="clinical_note.txt",

            file_type="text/plain",

            pages=[

                PageState(

                    page_number=1,

                    content=paragraph_text,

                )

            ],

        ),

        layout=LayoutState(

            nodes=[

                LayoutNode(

                    node_id="paragraph-001",

                    parent_id=None,

                    layout_type="paragraph",

                    page_number=1,

                    text=paragraph_text,

                    classification="Paragraph",

                    confidence=0.98,

                ),

            ],

        ),

        entities=EntityState(),

        validation=ValidationState(),

        model=ModelState(),

        metrics=MetricsState(),

        checkpoint=CheckpointState(

            checkpoint_id=str(uuid4()),

            timestamp=datetime.utcnow().isoformat(),

            stage="paragraph_extraction",

        ),

    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()

    print("=" * 80)

    print("RUNNING PARAGRAPH EXTRACTION AGENT")

    print("=" * 80)

    result = await agent.execute(
        state
    )

    # ==========================================================
    # Result
    # ==========================================================

    print()

    print("=" * 80)

    print("PARAGRAPH EXTRACTION RESULT")

    print("=" * 80)

    for node in result.layout.nodes:

        print()

        print(
            "Node ID        :",
            node.node_id,
        )

        print(
            "Classification :",
            node.classification,
        )

        if node.classification != "Paragraph":

            continue

        paragraph = node.metadata.get(
            "paragraph"
        )

        if not paragraph:

            print(
                "ERROR: No paragraph "
                "extraction found."
            )

            continue

        print()

        print(
            "Original Text:"
        )

        print(
            paragraph.get(
                "original_text",
                "",
            )
        )

        print()

        print(
            "Cleaned Text:"
        )

        print(
            paragraph.get(
                "text",
                "",
            )
        )

        print()

        print(
            "Paragraph Type:"
        )

        print(
            paragraph.get(
                "paragraph_type",
                "",
            )
        )

        print()

        print(
            "Confidence:"
        )

        print(
            paragraph.get(
                "confidence",
                "",
            )
        )

        notes = paragraph.get(
            "notes",
            "",
        )

        if notes:

            print()

            print(
                "Notes:"
            )

            print(
                notes
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