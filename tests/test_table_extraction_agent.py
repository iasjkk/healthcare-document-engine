"""
End-to-end test for TableExtractionAgent.

Run:

    python -m tests.test_table_extraction_agent

The test uses the configured OpenRouter API and therefore
requires:

    OPEN_ROUTER_API_KEY

to be available in the environment.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.table.table_extraction_agent import (
    TableExtractionAgent,
)

from framework.prompts.layout_classification_prompt import (
    LayoutClassificationPrompt,
)

from framework.prompts.prompt_registry import (
    PromptRegistry,
)

from framework.prompts.table_extraction_prompt import (
    TableExtractionPrompt,
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
        "table_extraction",
        TableExtractionPrompt(),
    )

    # Registering this as well keeps the prompt registry
    # compatible with the document/layout pipeline.

    prompt_registry.register(
        "layout_classification",
        LayoutClassificationPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = TableExtractionAgent(

        router=router,

        prompt_registry=prompt_registry,

    )

    # ==========================================================
    # Sample Healthcare Document
    # ==========================================================

    document_text = """
Laboratory Investigation Report

Patient Name: John Doe
Patient ID: HCP-1001

Test              Result       Unit        Reference Range

Hemoglobin        13.2         g/dL        12.0-16.0

WBC               7.5          x10^3/uL    4.0-11.0

Platelets         250          x10^3/uL    150-450

Glucose            96          mg/dL       70-100
"""

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(

            run_id=str(uuid4()),

            workflow_id="table-extraction-test",

        ),

        document=DocumentState(

            document_id="doc-table-001",

            file_name="laboratory_report.txt",

            file_path="laboratory_report.txt",

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

                    node_id="table-001",

                    parent_id=None,

                    layout_type="table",

                    page_number=1,

                    text=(
                        "Test              Result       "
                        "Unit        Reference Range\n"
                        "Hemoglobin        13.2         "
                        "g/dL        12.0-16.0\n"
                        "WBC               7.5          "
                        "x10^3/uL    4.0-11.0\n"
                        "Platelets         250          "
                        "x10^3/uL    150-450\n"
                        "Glucose            96           "
                        "mg/dL       70-100"
                    ),

                    classification="Table",

                    confidence=0.99,

                ),

                LayoutNode(

                    node_id="paragraph-001",

                    parent_id=None,

                    layout_type="paragraph",

                    page_number=1,

                    text=(
                        "Patient Name: John Doe"
                    ),

                    classification="Paragraph",

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

            stage="table_extraction",

        ),

    )

    # ==========================================================
    # Execute Agent
    # ==========================================================

    print()

    print("=" * 80)

    print("RUNNING TABLE EXTRACTION AGENT")

    print("=" * 80)

    result = await agent.execute(state)

    # ==========================================================
    # Result
    # ==========================================================

    print()

    print("=" * 80)

    print("TABLE EXTRACTION RESULT")

    print("=" * 80)

    for node in result.layout.nodes:

        print()

        print("Node ID        :", node.node_id)

        print("Classification :", node.classification)

        if node.classification != "Table":

            continue

        table = node.metadata.get(
            "table"
        )

        confidence = node.metadata.get(
            "table_confidence"
        )

        notes = node.metadata.get(
            "table_notes",
            "",
        )

        print()

        print("Headers:")

        for header in table.get(
            "headers",
            [],
        ):

            print(
                f"  - {header}"
            )

        print()

        print("Rows:")

        for row in table.get(
            "rows",
            [],
        ):

            print(
                "  ",
                row,
            )

        print()

        print(
            "Confidence:",
            confidence,
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
