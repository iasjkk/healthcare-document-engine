"""
End-to-end test for ListExtractionAgent.

Run:

    python -m tests.test.list.extraction_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.list.list_extraction_agent import (
    ListExtractionAgent,
)

from framework.prompts.list_extraction_prompt import (
    ListExtractionPrompt,
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
        "list_extraction",
        ListExtractionPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = ListExtractionAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Sample document
    # ==========================================================

    content = """
Current Medications:

- Metformin 500 mg twice daily
- Aspirin 75 mg once daily
- Atorvastatin 20 mg at night

Allergies:

- Penicillin
- Sulfa drugs
"""

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="list-extraction-test",
        ),

        document=DocumentState(
            document_id="doc-list-001",
            file_name="patient_record.txt",
            file_path="patient_record.txt",
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
                    node_id="list-001",
                    parent_id=None,
                    layout_type="list",
                    page_number=1,
                    text=(
                        "- Metformin 500 mg twice daily\n"
                        "- Aspirin 75 mg once daily\n"
                        "- Atorvastatin 20 mg at night"
                    ),
                    classification="List",
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
            stage="list_extraction",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING LIST EXTRACTION AGENT")
    print("=" * 80)

    result = await agent.execute(state)

    # ==========================================================
    # Results
    # ==========================================================

    print()
    print("=" * 80)
    print("LIST EXTRACTION RESULT")
    print("=" * 80)

    for node in result.layout.nodes:

        extracted = node.metadata.get(
            "list_extraction"
        )

        if not extracted:
            continue

        print()

        print(
            "List Type:",
            extracted.get(
                "list_type"
            ),
        )

        print(
            "Confidence:",
            extracted.get(
                "confidence"
            ),
        )

        print()

        for item in extracted.get(
            "items",
            [],
        ):

            print(
                f"{item.get('position')}. "
                f"{item.get('text')}"
            )

            print(
                f"   Level: "
                f"{item.get('level')}"
            )

            print(
                f"   Marker: "
                f"{item.get('marker')}"
            )

            print(
                f"   Confidence: "
                f"{item.get('confidence')}"
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