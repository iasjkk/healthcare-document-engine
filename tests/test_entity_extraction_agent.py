"""
End-to-end test for EntityExtractionAgent.

Run:

    python -m tests.test_entity_extraction_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.entity.entity_extraction_agent import (
    EntityExtractionAgent,
)

from framework.prompts.entity_extraction_prompt import (
    EntityExtractionPrompt,
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

from framework.state.clinical_summary_state import (
    ClinicalSummaryState,
    MedicationSummary,
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
        "entity_extraction",
        EntityExtractionPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = EntityExtractionAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Sample healthcare document
    # ==========================================================

    patient_text = """
PATIENT INFORMATION

Patient Name: John Doe

Date of Birth: 12/05/1980

Medical Record Number: MRN-123456

Gender: Male

Diagnosis: Invasive ductal carcinoma

Medication: Metformin 500 mg twice daily

Laboratory Results:

Hemoglobin: 12.5 g/dL

HER2: Positive

BRCA1 mutation detected.

MRI of the brain was performed.

Specimen accession number:
ACC-2026-00123.
"""

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="entity-extraction-test",
        ),

        document=DocumentState(
            document_id="doc-entity-001",
            file_name="clinical_report.txt",
            file_path="clinical_report.txt",
            file_type="text/plain",
            pages=[
                PageState(
                    page_number=1,
                    content=patient_text,
                )
            ],
        ),

        layout=LayoutState(
            nodes=[
                LayoutNode(
                    node_id="clinical-001",
                    parent_id=None,
                    layout_type="section",
                    page_number=1,
                    text=patient_text,
                    classification="Section",
                ),
            ]
        ),

        entities=EntityState(),

        validation=ValidationState(),

        model=ModelState(),

        metrics=MetricsState(),

        clinical_summary=ClinicalSummaryState(),

        checkpoint=CheckpointState(
            checkpoint_id=str(uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            stage="entity_extraction",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING ENTITY EXTRACTION AGENT")
    print("=" * 80)

    result = await agent.execute(state)

    # ==========================================================
    # Results
    # ==========================================================

    print()
    print("=" * 80)
    print("ENTITY EXTRACTION RESULT")
    print("=" * 80)

    extraction = result.metadata.get(
        "entity_extraction",
        {},
    )

    print()

    print(
        "Entity Count:",
        extraction.get(
            "entity_count",
            0,
        ),
    )

    print()

    for entity in extraction.get(
        "entities",
        [],
    ):

        print(
            f"- {entity.get('entity_type')}"
        )

        print(
            f"  Text: "
            f"{entity.get('text')}"
        )

        print(
            f"  Normalized: "
            f"{entity.get('normalized_text')}"
        )

        print(
            f"  Page: "
            f"{entity.get('page_number')}"
        )

        print(
            f"  Source Node: "
            f"{entity.get('source_node_id')}"
        )

        print(
            f"  Confidence: "
            f"{entity.get('confidence')}"
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