"""
End-to-end test for SignatureExtractionAgent.

Run:

    python -m tests.test_signature_extraction_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.signature.signature_extraction_agent import (
    SignatureExtractionAgent,
)

from framework.prompts.signature_extraction_prompt import (
    SignatureExtractionPrompt,
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
        "signature_extraction",
        SignatureExtractionPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = SignatureExtractionAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Sample document
    # ==========================================================

    content = """
DISCHARGE SUMMARY

Patient was discharged in stable condition.

Electronically signed by Dr. John Smith
Physician
Date: 2026-08-08
"""

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="signature-extraction-test",
        ),

        document=DocumentState(
            document_id="doc-signature-001",
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
                    node_id="signature-001",
                    parent_id=None,
                    layout_type="signature",
                    page_number=1,
                    text=(
                        "Electronically signed by "
                        "Dr. John Smith\n"
                        "Physician\n"
                        "Date: 2026-08-08"
                    ),
                    classification="Signature",
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
            stage="signature_extraction",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING SIGNATURE EXTRACTION AGENT")
    print("=" * 80)

    result = await agent.execute(state)

    # ==========================================================
    # Results
    # ==========================================================

    print()
    print("=" * 80)
    print("SIGNATURE EXTRACTION RESULT")
    print("=" * 80)

    for node in result.layout.nodes:

        extracted = node.metadata.get(
            "signature_extraction"
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

        for signature in extracted.get(
            "signatures",
            [],
        ):

            print(
                f"- Text: "
                f"{signature.get('text')}"
            )

            print(
                f"  Type: "
                f"{signature.get('signature_type')}"
            )

            print(
                f"  Signer Role: "
                f"{signature.get('signer_role')}"
            )

            print(
                f"  Signed: "
                f"{signature.get('signed')}"
            )

            print(
                f"  Page: "
                f"{signature.get('page_number')}"
            )

            print(
                f"  Confidence: "
                f"{signature.get('confidence')}"
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