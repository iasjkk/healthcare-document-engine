"""
End-to-end test for TableValidationAgent.

Run:

    python -m tests.test_table_validation_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.table.table_validation_agent import (
    TableValidationAgent,
)

from framework.prompts.prompt_registry import (
    PromptRegistry,
)

from framework.prompts.table_validation_prompt import (
    TableValidationPrompt,
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
        "table_validation",
        TableValidationPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = TableValidationAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Existing table extraction
    #
    # This simulates the output of your existing
    # TableExtractionAgent.
    # ==========================================================

    table_node = LayoutNode(
        node_id="node-001",
        parent_id=None,
        layout_type="TABLE",
        page_number=1,
        text=(
            "Laboratory Results\n"
            "Test | Result | Reference Range\n"
            "Hemoglobin | 13.5 | 12-16 g/dL\n"
            "WBC | 7.2 | 4-11 x10^9/L\n"
            "Platelets | 250 | 150-450 x10^9/L"
        ),
        metadata={
            "table_extraction": {
                "table_id": "node-001_table",
                "headers": [
                    "Test",
                    "Result",
                    "Reference Range",
                ],
                "rows": [
                    [
                        "Hemoglobin",
                        "13.5",
                        "12-16 g/dL",
                    ],
                    [
                        "WBC",
                        "7.2",
                        "4-11 x10^9/L",
                    ],
                    [
                        "Platelets",
                        "250",
                        "150-450 x10^9/L",
                    ],
                ],
                "cells": [
                    {
                        "row": 0,
                        "column": 0,
                        "value": "Hemoglobin",
                    },
                    {
                        "row": 0,
                        "column": 1,
                        "value": "13.5",
                    },
                    {
                        "row": 0,
                        "column": 2,
                        "value": "12-16 g/dL",
                    },
                ],
                "confidence": 0.97,
                "notes": "",
                "metadata": {},
            }
        },
    )

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="table-validation-test",
        ),

        document=DocumentState(
            document_id="doc-table-validation-001",
            file_name="clinical_report.txt",
            file_path="clinical_report.txt",
            file_type="text/plain",
            pages=[
                PageState(
                    page_number=1,
                    content=(
                        "Laboratory Results\n"
                        "Test | Result | Reference Range\n"
                        "Hemoglobin | 13.5 | 12-16 g/dL\n"
                        "WBC | 7.2 | 4-11 x10^9/L\n"
                        "Platelets | 250 | 150-450 x10^9/L"
                    ),
                )
            ],
        ),

        layout=LayoutState(
            nodes=[
                table_node,
            ],
        ),

        entities=EntityState(),

        relations=RelationState(),

        validation=ValidationState(),

        model=ModelState(),

        metrics=MetricsState(),

        checkpoint=CheckpointState(
            checkpoint_id=str(uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            stage="table_validation",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()

    print("=" * 80)
    print("RUNNING TABLE VALIDATION AGENT")
    print("=" * 80)

    result = await agent.execute(
        state
    )

    # ==========================================================
    # Result
    # ==========================================================

    print()

    print("=" * 80)
    print("TABLE VALIDATION RESULT")
    print("=" * 80)

    validation = (
        result.layout.nodes[0]
        .metadata.get(
            "table_validation",
            {},
        )
    )

    validation_status = validation.get(
        "validation_status",
        "unknown",
    )

    validation_is_valid = validation.get(
        "is_valid",
        False,
    )

    validation_confidence = validation.get(
        "confidence",
        0.0,
    )

    validation_issues = validation.get(
        "issues",
        [],
    )

    validation_warnings = validation.get(
        "warnings",
        [],
    )

    print()

    print(
        "Table ID:",
        validation.get(
            "table_id"
        ),
    )

    print(
        "Valid:",
        validation_is_valid,
    )

    print(
        "Status:",
        validation_status,
    )

    print(
        "Confidence:",
        validation_confidence,
    )

    print(
        "Issues:",
        validation_issues,
    )

    print(
        "Warnings:",
        validation_warnings,
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