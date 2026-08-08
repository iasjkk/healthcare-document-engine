"""
End-to-end test for HeaderExtractionAgent.

Run:

    python -m tests.test_header_extraction_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.header.header_extraction_agent import (
    HeaderExtractionAgent,
)

from framework.prompts.header_extraction_prompt import (
    HeaderExtractionPrompt,
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
        "header_extraction",
        HeaderExtractionPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = HeaderExtractionAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Sample document
    # ==========================================================

    content = """
CITY GENERAL HOSPITAL
DEPARTMENT OF ONCOLOGY
CONFIDENTIAL MEDICAL RECORD

Patient Name: John Doe

HISTORY OF PRESENT ILLNESS

Patient was admitted for evaluation.
"""

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="header-extraction-test",
        ),

        document=DocumentState(
            document_id="doc-header-001",
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
                    node_id="header-001",
                    parent_id=None,
                    layout_type="header",
                    page_number=1,
                    text=(
                        "CITY GENERAL HOSPITAL\n"
                        "DEPARTMENT OF ONCOLOGY\n"
                        "CONFIDENTIAL MEDICAL RECORD"
                    ),
                    classification="Header",
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
            stage="header_extraction",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING HEADER EXTRACTION AGENT")
    print("=" * 80)

    result = await agent.execute(state)

    # ==========================================================
    # Results
    # ==========================================================

    print()
    print("=" * 80)
    print("HEADER EXTRACTION RESULT")
    print("=" * 80)

    for node in result.layout.nodes:

        extracted = node.metadata.get(
            "header_extraction"
        )

        if not extracted:
            continue

        print()

        print(
            "Confidence:",
            extracted.get(
                "confidence"
            ),
        )

        for header in extracted.get(
            "headers",
            [],
        ):

            print(
                f"- {header.get('text')}"
            )

            print(
                f"  Type: "
                f"{header.get('header_type')}"
            )

            print(
                f"  Page: "
                f"{header.get('page_number')}"
            )

            print(
                f"  Confidence: "
                f"{header.get('confidence')}"
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