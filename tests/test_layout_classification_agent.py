"""
Test Layout Classification Agent.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.layout.layout_classification_agent import (
    LayoutClassificationAgent,
)

from framework.prompts.prompt_registry import (
    PromptRegistry,
)

from framework.prompts.layout_classification_prompt import (
    LayoutClassificationPrompt,
)

from framework.router.model_router import (
    ModelRouter,
)

from framework.providers.openrouter_provider import (
    OpenRouterProvider,
)

from framework.registry.provider_registry import (
    ProviderRegistry,
)

from framework.state.workflow_state import (
    WorkflowState,
)

from framework.state.document_state import (
    DocumentState,
    PageState,
)

from framework.state.layout_state import (
    LayoutState,
    LayoutNode,
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

from framework.state.metrics_state import (
    MetricsState,
)

from framework.state.model_state import (
    ModelState,
)

from framework.state.checkpoint_state import (
    CheckpointState,
)


async def main():

    # ---------------------------------------------------------
    # Provider
    # ---------------------------------------------------------

    provider = OpenRouterProvider()

    registry = ProviderRegistry()

    registry.register(
        "openrouter",
        provider,
    )

    router = ModelRouter(registry)

    # ---------------------------------------------------------
    # Prompt Registry
    # ---------------------------------------------------------

    prompts = PromptRegistry()

    prompts.register(
        "layout_classification",
        LayoutClassificationPrompt(),
    )

    # ---------------------------------------------------------
    # Agent
    # ---------------------------------------------------------

    agent = LayoutClassificationAgent(

        router=router,

        prompt_registry=prompts,

    )

    # ---------------------------------------------------------
    # Workflow State
    # ---------------------------------------------------------

    state = WorkflowState(

        execution=ExecutionState(

            run_id=str(uuid4()),

            workflow_id="layout-test",

        ),

        document=DocumentState(

            document_id="doc001",

            file_name="sample.txt",

            file_path="sample.txt",

            file_type="text/plain",

            pages=[

                PageState(

                    page_number=1,

                    content="Dummy",

                )

            ],

        ),

        layout=LayoutState(

            nodes=[

                LayoutNode(

                    node_id="1",

                    page_number=1,

                    layout_type="section",

                    text="Diagnosis",

                ),

                LayoutNode(

                    node_id="2",

                    page_number=1,

                    layout_type="paragraph",

                    text=(
                        "Patient has fever "
                        "for three days."
                    ),

                ),

                LayoutNode(

                    node_id="3",

                    page_number=1,

                    layout_type="table",

                    text=(
                        "Hemoglobin 13.2\n"
                        "WBC 7.5\n"
                        "Platelets 250"
                    ),

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

            stage="layout_classification",

        ),

    )

    # ---------------------------------------------------------
    # Execute
    # ---------------------------------------------------------

    result = await agent.execute(state)

    print()

    print("=" * 80)

    print("LAYOUT CLASSIFICATION RESULT")

    print("=" * 80)

    for node in result.layout.nodes:

        print()

        print("Node ID       :", node.node_id)

        print("Text          :", node.text)

        print("Type          :", node.layout_type)

        print("Classification:", node.classification)

        print("Confidence    :", node.confidence)

    print()

    print("=" * 80)

    print("Checkpoint")

    print("=" * 80)

    print(result.checkpoint.stage)

    await provider.disconnect()


if __name__ == "__main__":
    asyncio.run(main())