"""
End-to-end test for ClinicalSummaryAgent.

Run:

    python -m tests.test_clinical_summary_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.clinical.clinical_summary_agent import (
    ClinicalSummaryAgent,
)

from framework.prompts.clinical_summary_prompt import (
    ClinicalSummaryPrompt,
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
    Entity,
    EntityState,
)

from framework.state.execution_state import (
    ExecutionState,
)

from framework.state.layout_state import (
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

from framework.state.clinical_summary_state import (
    ClinicalSummaryState,
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
        "clinical_summary",
        ClinicalSummaryPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = ClinicalSummaryAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Sample clinical entities
    # ==========================================================

    entities = EntityState(
        entities=[
            Entity(
                entity_id="node-001_entity_1",
                entity_type="MEDICATION",
                value="Metformin",
                confidence=0.98,
                page_number=1,
                source_node="node-001",
                normalized_value="Metformin",
                metadata={
                    "dosage": "500 mg",
                    "frequency": "twice daily",
                },
            ),

            Entity(
                entity_id="node-001_entity_2",
                entity_type="DOSAGE",
                value="500 mg",
                confidence=0.99,
                page_number=1,
                source_node="node-001",
                normalized_value="500 mg",
            ),

            Entity(
                entity_id="node-001_entity_3",
                entity_type="FREQUENCY",
                value="twice daily",
                confidence=0.99,
                page_number=1,
                source_node="node-001",
                normalized_value="twice daily",
            ),

            Entity(
                entity_id="node-001_entity_4",
                entity_type="BIOMARKER",
                value="HER2 positive",
                confidence=0.97,
                page_number=1,
                source_node="node-001",
                normalized_value="HER2 positive",
                metadata={
                    "biomarker": "HER2",
                    "status": "positive",
                },
            ),

            Entity(
                entity_id="node-001_entity_5",
                entity_type="GENE",
                value="brca1",
                confidence=0.96,
                page_number=1,
                source_node="node-001",
                normalized_value="BRCA1",
                metadata={
                    "mutation_status": "detected",
                },
            ),

            Entity(
                entity_id="node-001_entity_6",
                entity_type="GENETIC_FINDING",
                value="BRCA1 mutation detected",
                confidence=0.96,
                page_number=1,
                source_node="node-001",
                normalized_value="BRCA1 mutation detected",
            ),
        ]
    )

    # ==========================================================
    # Document
    # ==========================================================

    document = DocumentState(
        document_id="doc-summary-001",
        file_name="clinical_report.txt",
        file_path="clinical_report.txt",
        file_type="text/plain",
        pages=[
            PageState(
                page_number=1,
                content=(
                    "Clinical Report\n\n"
                    "Medication: Metformin 500 mg "
                    "twice daily.\n"
                    "HER2 positive.\n"
                    "BRCA1 mutation detected."
                ),
            )
        ],
    )

    # ==========================================================
    # Layout
    # ==========================================================

    layout = LayoutState()

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="clinical-summary-test",
        ),

        document=document,

        layout=layout,

        entities=entities,

        validation=ValidationState(),

        relations=RelationState(),

        clinical_summary=ClinicalSummaryState(),

        model=ModelState(),

        metrics=MetricsState(),

        checkpoint=CheckpointState(
            checkpoint_id=str(uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            stage="clinical_summary",
        ),
    )

    # ==========================================================
    # Print initial state
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING CLINICAL SUMMARY AGENT")
    print("=" * 80)

    print()

    print("Input Entities:")

    for entity in state.entities.entities:

        print(
            f"- {entity.entity_type}: "
            f"{entity.value}"
        )

    print()

    # ==========================================================
    # Execute Agent
    # ==========================================================

    try:

        result = await agent.execute(
            state
        )

    except Exception as exc:

        print()
        print("=" * 80)
        print("CLINICAL SUMMARY AGENT FAILED")
        print("=" * 80)

        print()

        print(
            f"{type(exc).__name__}: {exc}"
        )

        raise

    # ==========================================================
    # Clinical Summary
    # ==========================================================

    summary = result.clinical_summary

    print()
    print("=" * 80)
    print("CLINICAL SUMMARY RESULT")
    print("=" * 80)

    print()

    # ==========================================================
    # Summary
    # ==========================================================

    print("Summary:")
    print(summary.summary)

    print()

    # ==========================================================
    # Key Findings
    # ==========================================================

    print("Key Findings:")

    if summary.key_findings:

        for finding in summary.key_findings:

            print(
                f"- {finding}"
            )

    else:

        print("- None")

    print()

    # ==========================================================
    # Diagnoses
    # ==========================================================

    print("Diagnoses:")

    if summary.diagnoses:

        for diagnosis in summary.diagnoses:

            print(
                f"- {diagnosis}"
            )

    else:

        print("- None")

    print()

    # ==========================================================
    # Medications
    # ==========================================================

    print("Medications:")

    if summary.medications:

        for medication in summary.medications:

            print(
                f"- Name: "
                f"{medication.name}"
            )

            print(
                f"  Dosage: "
                f"{medication.dosage}"
            )

            print(
                f"  Frequency: "
                f"{medication.frequency}"
            )

            print(
                f"  Route: "
                f"{medication.route}"
            )

            print(
                f"  Status: "
                f"{medication.status}"
            )

            if medication.metadata:

                print(
                    f"  Metadata: "
                    f"{medication.metadata}"
                )

    else:

        print("- None")

    print()

    # ==========================================================
    # Allergies
    # ==========================================================

    print("Allergies:")

    if summary.allergies:

        for allergy in summary.allergies:

            print(
                f"- {allergy}"
            )

    else:

        print("- None")

    print()

    # ==========================================================
    # Laboratory Findings
    # ==========================================================

    print("Laboratory Findings:")

    if summary.laboratory_findings:

        for finding in (
            summary.laboratory_findings
        ):

            print(
                f"- {finding}"
            )

    else:

        print("- None")

    print()

    # ==========================================================
    # Pathology Findings
    # ==========================================================

    print("Pathology Findings:")

    if summary.pathology_findings:

        for finding in (
            summary.pathology_findings
        ):

            print(
                f"- {finding}"
            )

    else:

        print("- None")

    print()

    # ==========================================================
    # Biomarkers
    # ==========================================================

    print("Biomarkers:")

    if summary.biomarkers:

        for biomarker in summary.biomarkers:

            print(
                f"- {biomarker}"
            )

    else:

        print("- None")

    print()

    # ==========================================================
    # Procedures
    # ==========================================================

    print("Procedures:")

    if summary.procedures:

        for procedure in summary.procedures:

            print(
                f"- {procedure}"
            )

    else:

        print("- None")

    print()

    # ==========================================================
    # Recommendations
    # ==========================================================

    print("Recommendations:")

    if summary.recommendations:

        for recommendation in (
            summary.recommendations
        ):

            print(
                f"- {recommendation}"
            )

    else:

        print("- None")

    print()

    # ==========================================================
    # Confidence
    # ==========================================================

    print("Confidence:")
    print(summary.confidence)

    print()

    # ==========================================================
    # Notes
    # ==========================================================

    print("Notes:")
    print(summary.notes)

    print()

    # ==========================================================
    # Metadata
    # ==========================================================

    print("Metadata:")
    print(summary.metadata)

    print()

    # ==========================================================
    # Model Execution Information
    # ==========================================================

    print("=" * 80)
    print("MODEL EXECUTIONS")
    print("=" * 80)

    print()

    print(
        "Model execution count:",
        len(
            result.model.executions
        ),
    )

    for execution in (
        result.model.executions
    ):

        print()

        print(
            "Execution ID:",
            execution.execution_id,
        )

        print(
            "Status:",
            execution.status,
        )

        print(
            "Retry Count:",
            execution.retry_count,
        )

        print(
            "Started At:",
            execution.started_at,
        )

        print(
            "Completed At:",
            execution.completed_at,
        )

        if execution.error_message:

            print(
                "Error:",
                execution.error_message,
            )

    # ==========================================================
    # Checkpoint
    # ==========================================================

    print()
    print("=" * 80)
    print("CHECKPOINT")
    print("=" * 80)

    print()

    print(
        "Stage:",
        result.checkpoint.stage,
    )

    print(
        "Checkpoint ID:",
        result.checkpoint.checkpoint_id,
    )

    # ==========================================================
    # Basic Assertions
    # ==========================================================

    print()
    print("=" * 80)
    print("VALIDATION")
    print("=" * 80)

    print()

    assert result.clinical_summary is not None

    assert isinstance(
        result.clinical_summary.summary,
        str,
    )

    assert 0.0 <= (
        result.clinical_summary.confidence
    ) <= 1.0

    assert (
        result.checkpoint.stage
        == "clinical_summary_completed"
    )

    print(
        "✓ Clinical summary state exists"
    )

    print(
        "✓ Summary is a string"
    )

    print(
        "✓ Confidence is valid"
    )

    print(
        "✓ Checkpoint completed"
    )

    # ==========================================================
    # Medication Validation
    # ==========================================================

    for medication in (
        result.clinical_summary.medications
    ):

        assert isinstance(
            medication.name,
            str,
        )

        assert isinstance(
            medication.dosage,
            str,
        )

        assert isinstance(
            medication.frequency,
            str,
        )

        assert isinstance(
            medication.route,
            str,
        )

        assert isinstance(
            medication.status,
            str,
        )

    print(
        "✓ Medication structure is valid"
    )

    # ==========================================================
    # Final
    # ==========================================================

    print()
    print("=" * 80)
    print("CLINICAL SUMMARY TEST PASSED")
    print("=" * 80)

    # ==========================================================
    # Cleanup
    # ==========================================================

    await provider.disconnect()


if __name__ == "__main__":

    asyncio.run(main())
