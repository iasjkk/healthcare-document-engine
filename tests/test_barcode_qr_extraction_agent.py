"""
End-to-end test for BarcodeQRExtractionAgent.

Run:

    python -m tests.test_barcode_qr_extraction_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.barcode.barcode_qr_extraction_agent import (
    BarcodeQRExtractionAgent,
)

from framework.prompts.barcode_qr_extraction_prompt import (
    BarcodeQRExtractionPrompt,
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
        "barcode_qr_extraction",
        BarcodeQRExtractionPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = BarcodeQRExtractionAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Sample document
    # ==========================================================

    barcode_text = """
SPECIMEN LABEL

Patient Specimen

Barcode:
LAB202608070001

Specimen Type:
Blood

QR Code:
https://hospital.example/specimen/LAB202608070001

Context:
Laboratory specimen tracking label.
"""

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="barcode-qr-extraction-test",
        ),

        document=DocumentState(
            document_id="doc-barcode-001",
            file_name="specimen_label.txt",
            file_path="specimen_label.txt",
            file_type="text/plain",
            pages=[
                PageState(
                    page_number=1,
                    content=barcode_text,
                )
            ],
        ),

        layout=LayoutState(
            nodes=[
                LayoutNode(
                    node_id="barcode-001",
                    parent_id=None,
                    layout_type="barcode",
                    page_number=1,
                    text=(
                        "Barcode: "
                        "LAB202608070001"
                    ),
                    classification="Barcode",
                ),
                LayoutNode(
                    node_id="qr-001",
                    parent_id=None,
                    layout_type="qr_code",
                    page_number=1,
                    text=(
                        "QR Code: "
                        "https://hospital.example/"
                        "specimen/LAB202608070001"
                    ),
                    classification="QR Code",
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
            stage="barcode_qr_extraction",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING BARCODE / QR EXTRACTION AGENT")
    print("=" * 80)

    result = await agent.execute(state)

    # ==========================================================
    # Results
    # ==========================================================

    print()
    print("=" * 80)
    print("BARCODE / QR EXTRACTION RESULT")
    print("=" * 80)

    for node in result.layout.nodes:

        extracted = node.metadata.get(
            "barcode_qr_extraction"
        )

        if not extracted:
            continue

        print()

        print(
            "Node:",
            node.node_id,
        )

        print(
            "Overall Confidence:",
            extracted.get(
                "confidence"
            ),
        )

        for code in extracted.get(
            "codes",
            [],
        ):

            print(
                f"- Code ID: "
                f"{code.get('code_id')}"
            )

            print(
                f"  Type: "
                f"{code.get('code_type')}"
            )

            print(
                f"  Format: "
                f"{code.get('format')}"
            )

            print(
                f"  Value: "
                f"{code.get('value')}"
            )

            print(
                f"  Page: "
                f"{code.get('page_number')}"
            )

            print(
                f"  Context: "
                f"{code.get('context')}"
            )

            print(
                f"  Valid: "
                f"{code.get('is_valid')}"
            )

            print(
                f"  Confidence: "
                f"{code.get('confidence')}"
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