"""
End-to-end test for FinalReportAgent.

Run:

    python -m tests.test_final_report_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.report.final_report_agent import (
    FinalReportAgent,
)

from framework.prompts.final_report_prompt import (
    FinalReportPrompt,
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

from framework.state.clinical_summary_state import (
    ClinicalSummaryState,
    MedicationSummary,
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
        "final_report",
        FinalReportPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = FinalReportAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Document
    # ==========================================================

    document = DocumentState(
        document_id="doc-final-report-001",
        file_name="clinical_report.txt",
        file_path="clinical_report.txt",
        file_type="text/plain",
        pages=[
            PageState(
                page_number=1,
                content=(
                    "Clinical Report\n\n"
                    "Patient is taking Metformin "
                    "500 mg twice daily.\n"
                    "HER2 positive.\n"
                    "BRCA1 mutation detected."
                ),
            )
        ],
    )

    # ==========================================================
    # Clinical Summary
    # ==========================================================

    clinical_summary = ClinicalSummaryState(

        summary=(
            "Patient is taking Metformin 500 mg "
            "twice daily. HER2 is positive and "
            "BRCA1 mutation was detected."
        ),

        key_findings=[
            "HER2 positive",
            "BRCA1 mutation detected",
        ],

        diagnoses=[],

        medications=[
            MedicationSummary(
                name="Metformin",
                dosage="500 mg",
                frequency="twice daily",
                route="",
                status="",
                metadata={},
            ),
        ],

        allergies=[],

        laboratory_findings=[],

        pathology_findings=[],

        biomarkers=[
            "HER2 positive",
            "BRCA1 mutation detected",
        ],

        procedures=[],

        recommendations=[],

        confidence=0.95,

        notes="",

        metadata={},
    )

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="final-report-test",
        ),

        document=document,

        layout=LayoutState(),

        entities=EntityState(),

        validation=ValidationState(),

        relations=RelationState(),

        clinical_summary=clinical_summary,

        model=ModelState(),

        metrics=MetricsState(),

        checkpoint=CheckpointState(
            checkpoint_id=str(uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            stage="final_report",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING FINAL REPORT AGENT")
    print("=" * 80)
    print()

    try:

        result = await agent.execute(
            state
        )

    except Exception as exc:

        print()
        print("=" * 80)
        print("FINAL REPORT FAILED")
        print("=" * 80)
        print()

        print(
            f"{type(exc).__name__}: {exc}"
        )

        raise

    # ==========================================================
    # Retrieve Final Report
    # ==========================================================

    final_report = (
        result.clinical_summary.metadata.get(
            "final_report",
            {},
        )
    )

    # ==========================================================
    # Display Report
    # ==========================================================

    print()
    print("=" * 80)
    print("FINAL CLINICAL REPORT")
    print("=" * 80)
    print()

    print(
        "Title:",
        final_report.get(
            "title",
            "",
        ),
    )

    print()

    print("Summary:")
    print("-" * 80)

    print(
        final_report.get(
            "summary",
            "",
        )
    )

    print()

    print(
        "Validation Status:",
        final_report.get(
            "validation_status",
            "",
        ),
    )

    print(
        "Confidence:",
        final_report.get(
            "confidence",
            0.0,
        ),
    )

    # ==========================================================
    # Key Findings
    # ==========================================================

    print()
    print("KEY FINDINGS")
    print("-" * 80)

    for finding in final_report.get(
        "key_findings",
        [],
    ):

        print(
            f"- {finding}"
        )

    # ==========================================================
    # Diagnoses
    # ==========================================================

    print()
    print("DIAGNOSES")
    print("-" * 80)

    for diagnosis in final_report.get(
        "diagnoses",
        [],
    ):

        print(
            f"- {diagnosis}"
        )

    # ==========================================================
    # Medications
    # ==========================================================

    print()
    print("MEDICATIONS")
    print("-" * 80)

    for medication in final_report.get(
        "medications",
        [],
    ):
        print(
            f"- {medication.get('name', '')}"
            f" | Dosage: {medication.get('dosage', '')}"
            f" | Frequency: {medication.get('frequency', '')}"
            f" | Route: {medication.get('route', '')}"
            f" | Status: {medication.get('status', '')}"
        )

    # ==========================================================
    # Allergies
    # ==========================================================

    print()
    print("ALLERGIES")
    print("-" * 80)

    for allergy in final_report.get(
        "allergies",
        [],
    ):

        print(
            f"- {allergy}"
        )

    # ==========================================================
    # Laboratory Findings
    # ==========================================================

    print()
    print("LABORATORY FINDINGS")
    print("-" * 80)

    for finding in final_report.get(
        "laboratory_findings",
        [],
    ):

        print(
            f"- {finding}"
        )

    # ==========================================================
    # Pathology Findings
    # ==========================================================

    print()
    print("PATHOLOGY FINDINGS")
    print("-" * 80)

    for finding in final_report.get(
        "pathology_findings",
        [],
    ):

        print(
            f"- {finding}"
        )

    # ==========================================================
    # Biomarkers
    # ==========================================================

    print()
    print("BIOMARKERS")
    print("-" * 80)

    for biomarker in final_report.get(
        "biomarkers",
        [],
    ):

        print(
            f"- {biomarker}"
        )

    # ==========================================================
    # Procedures
    # ==========================================================

    print()
    print("PROCEDURES")
    print("-" * 80)

    for procedure in final_report.get(
        "procedures",
        [],
    ):

        print(
            f"- {procedure}"
        )

    # ==========================================================
    # Recommendations
    # ==========================================================

    print()
    print("RECOMMENDATIONS")
    print("-" * 80)

    for recommendation in final_report.get(
        "recommendations",
        [],
    ):

        print(
            f"- {recommendation}"
        )

    # ==========================================================
    # Report Sections
    # ==========================================================

    print()
    print("REPORT SECTIONS")
    print("-" * 80)

    for section in final_report.get(
        "sections",
        [],
    ):

        print()

        print(
            section.get(
                "title",
                "",
            )
        )

        print(
            section.get(
                "content",
                "",
            )
        )

    # ==========================================================
    # Notes
    # ==========================================================

    print()
    print("NOTES")
    print("-" * 80)

    print(
        final_report.get(
            "notes",
            "",
        )
    )

    # ==========================================================
    # Metadata
    # ==========================================================

    print()
    print("METADATA")
    print("-" * 80)

    print(
        final_report.get(
            "metadata",
            {},
        )
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

    # ==========================================================
    # Assertions
    # ==========================================================

    print()
    print("=" * 80)
    print("VALIDATION")
    print("=" * 80)
    print()

    assert (
        "final_report"
        in result.clinical_summary.metadata
    )

    assert isinstance(
        final_report,
        dict,
    )

    assert (
        final_report.get(
            "title"
        )
        is not None
    )

    assert (
        final_report.get(
            "summary"
        )
        is not None
    )

    assert (
        isinstance(
            final_report.get(
                "sections",
                [],
            ),
            list,
        )
    )

    assert (
        result.checkpoint.stage
        == "final_report_completed"
    )

    print(
        "✓ Final report exists"
    )

    print(
        "✓ Report title exists"
    )

    print(
        "✓ Report summary exists"
    )

    print(
        "✓ Report sections exist"
    )

    print(
        "✓ Final report stored in "
        "ClinicalSummaryState.metadata"
    )

    print(
        "✓ Checkpoint completed"
    )

    print()
    print("=" * 80)
    print("FINAL REPORT TEST PASSED")
    print("=" * 80)

    # ==========================================================
    # Cleanup
    # ==========================================================

    await provider.disconnect()


if __name__ == "__main__":

    asyncio.run(main())