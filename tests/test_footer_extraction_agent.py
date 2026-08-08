"""
End-to-end test for FooterExtractionAgent.

Run:

    python -m tests.test_footer_extraction_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.footer.footer_extraction_agent import (
    FooterExtractionAgent,
)

from framework.prompts.footer_extraction_prompt import (
    FooterExtractionPrompt,
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
        "footer_extraction",
        FooterExtractionPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = FooterExtractionAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Sample document
    # ==========================================================

    content = """
Patient was discharged in stable condition.

Follow-up appointment recommended.

Confidential Medical Record
Page 1 of 5
© 2026 City General Hospital
"""

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="footer-extraction-test",
        ),

        document=DocumentState(
            document_id="doc-footer-001",
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
                    node_id="footer-001",
                    parent_id=None,
                    layout_type="footer",
                    page_number=1,
                    text=(
                        "Confidential Medical Record\n"
                        "Page 1 of 5\n"
                        "© 2026 City General Hospital"
                    ),
                    classification="Footer",
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
            stage="footer_extraction",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING FOOTER EXTRACTION AGENT")
    print("=" * 80)

    result = await agent.execute(state)

    # ==========================================================
    # Results
    # ==========================================================

    print()
    print("=" * 80)
    print("FOOTER EXTRACTION RESULT")
    print("=" * 80)

    for node in result.layout.nodes:

        extracted = node.metadata.get(
            "footer_extraction"
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

        for footer in extracted.get(
            "footers",
            [],
        ):

            print(
                f"- {footer.get('text')}"
            )

            print(
                f"  Type: "
                f"{footer.get('footer_type')}"
            )

            print(
                f"  Page: "
                f"{footer.get('page_number')}"
            )

            print(
                f"  Confidence: "
                f"{footer.get('confidence')}"
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