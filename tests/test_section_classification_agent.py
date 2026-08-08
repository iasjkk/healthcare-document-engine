"""
End-to-end test for SectionClassificationAgent.

Run:

    python -m tests.test_section_classification_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.section.section_classification_agent import (
    SectionClassificationAgent,
)

from framework.prompts.prompt_registry import (
    PromptRegistry,
)

from framework.prompts.section_classification_prompt import (
    SectionClassificationPrompt,
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

from framework.state.relation_state import (
    RelationState,
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
        "section_classification",
        SectionClassificationPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = SectionClassificationAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Layout Nodes
    # ==========================================================

    nodes = [

        LayoutNode(
            node_id="node-001",
            parent_id=None,
            layout_type="TEXT",
            page_number=1,
            text="Laboratory Results",
        ),

        LayoutNode(
            node_id="node-002",
            parent_id=None,
            layout_type="TEXT",
            page_number=1,
            text=(
                "Hemoglobin: 13.5 g/dL. "
                "WBC: 7.2 x10^9/L. "
                "Platelets: 250 x10^9/L."
            ),
        ),

        LayoutNode(
            node_id="node-003",
            parent_id=None,
            layout_type="TEXT",
            page_number=1,
            text=(
                "The patient was diagnosed with "
                "HER2-positive breast carcinoma."
            ),
        ),

        LayoutNode(
            node_id="node-004",
            parent_id=None,
            layout_type="TABLE",
            page_number=2,
            text=(
                "Test | Result | Reference Range\n"
                "Hemoglobin | 13.5 | 12-16 g/dL"
            ),
        ),
    ]

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="section-classification-test",
        ),

        document=DocumentState(
            document_id="doc-section-001",
            file_name="clinical_report.txt",
            file_path="clinical_report.txt",
            file_type="text/plain",
            pages=[
                PageState(
                    page_number=1,
                    content=(
                        "Laboratory Results\n"
                        "Hemoglobin: 13.5 g/dL.\n"
                        "WBC: 7.2 x10^9/L.\n"
                        "The patient was diagnosed with "
                        "HER2-positive breast carcinoma."
                    ),
                ),
                PageState(
                    page_number=2,
                    content=(
                        "Test | Result | Reference Range\n"
                        "Hemoglobin | 13.5 | 12-16 g/dL"
                    ),
                ),
            ],
        ),

        layout=LayoutState(
            nodes=nodes,
        ),

        entities=EntityState(),

        relations=RelationState(),

        validation=ValidationState(),

        model=ModelState(),

        metrics=MetricsState(),

        checkpoint=CheckpointState(
            checkpoint_id=str(uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            stage="section_classification",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()

    print("=" * 80)
    print("RUNNING SECTION CLASSIFICATION AGENT")
    print("=" * 80)

    result = await agent.execute(
        state
    )

    # ==========================================================
    # Results
    # ==========================================================

    print()

    print("=" * 80)
    print("SECTION CLASSIFICATION RESULT")
    print("=" * 80)

    print()

    for node in result.layout.nodes:

        classification = node.metadata.get(
            "section_classification",
            {},
        )

        section = classification.get(
            "section",
            "UNKNOWN",
        )

        confidence = classification.get(
            "confidence",
            0.0,
        )

        print(
            f"- Node ID: "
            f"{node.node_id}"
        )

        print(
            f"  Text: "
            f"{node.text[:100]}"
        )

        print(
            f"  Layout Type: "
            f"{node.layout_type}"
        )

        print(
            f"  Section: "
            f"{section}"
        )

        print(
            f"  Confidence: "
            f"{confidence}"
        )

        print()

    # ==========================================================
    # Checkpoint
    # ==========================================================

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