"""
End-to-end test for KeyValueExtractionAgent.

Run:

    python -m tests.test.key_value.extraction_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.key_value.key_value_extraction_agent import (
    KeyValueExtractionAgent,
)

from framework.prompts.key_value_extraction_prompt import (
    KeyValueExtractionPrompt,
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
        "key_value_extraction",
        KeyValueExtractionPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = KeyValueExtractionAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Test document
    # ==========================================================

    content = """
Patient Name: John Doe
Date of Birth: 12/03/1980
Patient ID: PAT-12345
MRN: 987654
Date of Admission: 01/08/2026
Physician: Dr. Smith
Department: Oncology
"""

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="key-value-extraction-test",
        ),

        document=DocumentState(

            document_id="doc-kv-001",

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
                    node_id="kv-001",
                    parent_id=None,
                    layout_type="key_value",
                    page_number=1,
                    text=content,
                    classification="Key-Value",
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
            stage="key_value_extraction",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING KEY-VALUE EXTRACTION AGENT")
    print("=" * 80)

    result = await agent.execute(state)

    # ==========================================================
    # Result
    # ==========================================================

    print()
    print("=" * 80)
    print("KEY-VALUE EXTRACTION RESULT")
    print("=" * 80)

    for node in result.layout.nodes:

        extracted = node.metadata.get(
            "key_value"
        )

        if not extracted:
            continue

        print()

        for item in extracted.get(
            "items",
            [],
        ):

            print(
                f"{item.get('key')}: "
                f"{item.get('value')}"
            )

            print(
                f"  normalized_key: "
                f"{item.get('normalized_key')}"
            )

            print(
                f"  value_type: "
                f"{item.get('value_type')}"
            )

            print(
                f"  confidence: "
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