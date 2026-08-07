"""
Test DocumentStructureAgent end-to-end execution.

Flow:

WorkflowState
        |
        v
DocumentStructureAgent
        |
        v
ModelRouter
        |
        v
OpenRouterProvider
        |
        v
LayoutState update
"""

import asyncio

from dotenv import load_dotenv


# Core
from framework.providers.openrouter_provider import (
    OpenRouterProvider,
)

from framework.registry.provider_registry import (
    ProviderRegistry,
)

from framework.router.model_router import (
    ModelRouter,
)


# Prompt
from framework.prompts.prompt_registry import (
    PromptRegistry,
)

from framework.prompts.document_structure_prompt import (
    DocumentStructurePrompt,
)


# Agent
from framework.agents.document.document_structure_agent import (
    DocumentStructureAgent,
)


# States
from framework.state.workflow_state import (
    WorkflowState,
)

from framework.state.document_state import (
    DocumentState,
    PageState,
)

from framework.state.layout_state import (
    LayoutState,
)

from framework.state.execution_state import (
    ExecutionState,
)

from framework.state.entity_state import (
    EntityState,
)

from framework.state.validation_state import (
    ValidationState,
)

from framework.state.model_state import (
    ModelState,
)

from framework.state.metrics_state import (
    MetricsState,
)

from framework.state.checkpoint_state import (
    CheckpointState,
)



async def main():

    # ==================================================
    # Environment
    # ==================================================

    load_dotenv()


    # ==================================================
    # Provider Registry
    # ==================================================

    provider_registry = ProviderRegistry()


    provider_registry.register(

        "openrouter",

        OpenRouterProvider(),

    )


    # ==================================================
    # Model Router
    # ==================================================

    router = ModelRouter(

        provider_registry

    )


    # ==================================================
    # Prompt Registry
    # ==================================================

    prompt_registry = PromptRegistry()


    prompt_registry.register(

        "document_structure",

        DocumentStructurePrompt(),

    )


    # ==================================================
    # Agent
    # ==================================================

    agent = DocumentStructureAgent(

        router,

        prompt_registry,

    )


    # ==================================================
    # Workflow State
    # ==================================================

    state = WorkflowState(

        # ------------------------------
        # Runtime
        # ------------------------------

        execution=ExecutionState(

            run_id="RUN-001",

            workflow_id=(
                "document_structure_workflow"
            ),

        ),


        # ------------------------------
        # Document
        # ------------------------------

        document=DocumentState(

            document_id="DOC-001",

            file_name=(
                "clinical_discharge_summary.docx"
            ),

            file_path=(
                "samples/"
                "clinical_discharge_summary.docx"
            ),

            file_type="docx",


            pages=[

                PageState(

                    page_number=1,


                    content="""

Clinical Discharge Summary


Patient Information

Name: John Smith

Age: 54

Gender: Male


Diagnosis

Type 2 Diabetes Mellitus


Medication

Metformin 500mg twice daily


Laboratory Results

HbA1c: 7.2%


Follow Up

Review after 3 months

""",

                )

            ],

        ),


        # ------------------------------
        # Other states
        # ------------------------------

        layout=LayoutState(),


        entities=EntityState(),


        validation=ValidationState(),


        model=ModelState(),


        metrics=MetricsState(),


        checkpoint=CheckpointState(

            checkpoint_id="CHK-001",

            timestamp=(
                "2026-08-07T18:15:00Z"
            ),

            stage=(
                "document_structure"
            ),

        ),

    )


    # ==================================================
    # Execute Agent
    # ==================================================

    result = await agent.execute(

        state

    )


    # ==================================================
    # Output
    # ==================================================

    print("\n")
    print("=" * 70)
    print("DOCUMENT STRUCTURE RESULT")
    print("=" * 70)


    print(

        result.layout.nodes

    )


    print("\n")
    print("=" * 70)
    print("CHECKPOINT")
    print("=" * 70)


    print(

        result.checkpoint

    )


    print("\n")
    print("=" * 70)
    print("MODEL STATE")
    print("=" * 70)


    print(

        result.model

    )



if __name__ == "__main__":

    asyncio.run(main())