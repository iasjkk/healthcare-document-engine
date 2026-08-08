"""
End-to-end test for FormFieldExtractionAgent.

Run:

    python -m tests.test_form_field_extraction_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.form.form_field_extraction_agent import (
    FormFieldExtractionAgent,
)

from framework.prompts.form_field_extraction_prompt import (
    FormFieldExtractionPrompt,
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
        "form_field_extraction",
        FormFieldExtractionPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = FormFieldExtractionAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Sample form
    # ==========================================================

    content = """
PATIENT REGISTRATION FORM

Patient Name: John Doe

Date of Birth: 12/05/1980

Medical Record Number: MRN-12345

Phone: 9876543210

Email: john.doe@example.com

Gender:
☑ Male
☐ Female

Insurance Provider: ABC Health Insurance

Emergency Contact: Jane Doe
"""

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="form-field-extraction-test",
        ),

        document=DocumentState(
            document_id="doc-form-001",
            file_name="patient_registration.txt",
            file_path="patient_registration.txt",
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
                    node_id="form-001",
                    parent_id=None,
                    layout_type="form",
                    page_number=1,
                    text=content,
                    classification="Form",
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
            stage="form_field_extraction",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING FORM FIELD EXTRACTION AGENT")
    print("=" * 80)

    result = await agent.execute(state)

    # ==========================================================
    # Results
    # ==========================================================

    print()
    print("=" * 80)
    print("FORM FIELD EXTRACTION RESULT")
    print("=" * 80)

    for node in result.layout.nodes:

        extracted = node.metadata.get(
            "form_field_extraction"
        )

        if not extracted:
            continue

        print()

        print(
            "Overall Confidence:",
            extracted.get(
                "confidence"
            ),
        )

        for field in extracted.get(
            "fields",
            [],
        ):

            print(
                f"- {field.get('field_name')}"
            )

            print(
                f"  Label: "
                f"{field.get('field_label')}"
            )

            print(
                f"  Value: "
                f"{field.get('field_value')}"
            )

            print(
                f"  Type: "
                f"{field.get('field_type')}"
            )

            print(
                f"  Page: "
                f"{field.get('page_number')}"
            )

            print(
                f"  Required: "
                f"{field.get('required')}"
            )

            print(
                f"  Confidence: "
                f"{field.get('confidence')}"
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