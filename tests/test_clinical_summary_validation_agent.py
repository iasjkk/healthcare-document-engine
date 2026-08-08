"""
End-to-end test for ClinicalSummaryValidationAgent.

Run:

    python -m tests.test_clinical_summary_validation_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.clinical.clinical_summary_validation_agent import (
    ClinicalSummaryValidationAgent,
)

from framework.prompts.clinical_summary_validation_prompt import (
    ClinicalSummaryValidationPrompt,
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
        "clinical_summary_validation",
        ClinicalSummaryValidationPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = ClinicalSummaryValidationAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Source document
    # ==========================================================

    document = DocumentState(
        document_id="doc-validation-001",
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
    # Clinical Summary
    # ==========================================================

    clinical_summary = ClinicalSummaryState(

        summary=(
            "Patient is taking Metformin 500 mg "
            "twice daily. HER2 is positive and "
            "a BRCA1 mutation was detected."
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
            )
        ],

        allergies=[],

        laboratory_findings=[],

        pathology_findings=[],

        biomarkers=[
            "HER2 positive",
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
            workflow_id=(
                "clinical-summary-validation-test"
            ),
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
            stage=(
                "clinical_summary_validation"
            ),
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print(
        "RUNNING CLINICAL SUMMARY VALIDATION AGENT"
    )
    print("=" * 80)

    print()

    try:

        result = await agent.execute(
            state
        )

    except Exception as exc:

        print()
        print("=" * 80)
        print(
            "CLINICAL SUMMARY VALIDATION FAILED"
        )
        print("=" * 80)

        print()

        print(
            f"{type(exc).__name__}: {exc}"
        )

        raise

    # ==========================================================
    # Results
    # ==========================================================

    print()
    print("=" * 80)
    print(
        "CLINICAL SUMMARY VALIDATION RESULT"
    )
    print("=" * 80)

    print()

    validation_metadata = (
        result.clinical_summary.metadata.get(
            "clinical_summary_validation",
            {},
        )
    )

    print(
        "Valid:",
        validation_metadata.get(
            "valid",
            False,
        ),
    )

    print(
        "Confidence:",
        validation_metadata.get(
            "confidence",
            0.0,
        ),
    )

    print(
        "Notes:",
        validation_metadata.get(
            "notes",
            "",
        ),
    )

    print()

    # ==========================================================
    # Validation Issues
    # ==========================================================

    print("=" * 80)
    print("VALIDATION ISSUES")
    print("=" * 80)

    print()

    if result.validation.issues:

        for index, issue in enumerate(
            result.validation.issues,
            start=1,
        ):

            print(
                f"{index}. "
                f"[{issue.severity}] "
                f"{issue.code}"
            )

            print(
                f"   {issue.message}"
            )

            print()

    else:

        print(
            "No validation issues found."
        )

    # ==========================================================
    # Checkpoint
    # ==========================================================

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
        result.clinical_summary
        is not None
    )

    assert (
        "clinical_summary_validation"
        in result.clinical_summary.metadata
    )

    assert (
        result.checkpoint.stage
        == "clinical_summary_validation_completed"
    )

    assert isinstance(
        result.validation.issues,
        list,
    )

    print(
        "✓ Clinical summary exists"
    )

    print(
        "✓ Validation metadata exists"
    )

    print(
        "✓ Validation issues are stored "
        "in ValidationState"
    )

    print(
        "✓ Checkpoint completed"
    )

    print()
    print("=" * 80)
    print(
        "CLINICAL SUMMARY VALIDATION TEST PASSED"
    )
    print("=" * 80)

    # ==========================================================
    # Cleanup
    # ==========================================================

    await provider.disconnect()


if __name__ == "__main__":

    asyncio.run(main())