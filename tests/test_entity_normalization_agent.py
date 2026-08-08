"""
End-to-end test for EntityNormalizationAgent.

Run:

    python -m tests.test_entity_normalization_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.entity.entity_normalization_agent import (
    EntityNormalizationAgent,
)

from framework.prompts.entity_normalization_prompt import (
    EntityNormalizationPrompt,
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
        "entity_normalization",
        EntityNormalizationPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = EntityNormalizationAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Previously extracted entities
    #
    # These are now represented by the actual Entity model.
    # ==========================================================

    extracted_entities = [
        Entity(
            entity_id="node-001_entity_1",
            entity_type="MEDICATION",
            value="Metformin",
            confidence=0.98,
            page_number=1,
            source_node="node-001",
            normalized_value=None,
            metadata={},
        ),

        Entity(
            entity_id="node-001_entity_2",
            entity_type="DOSAGE",
            value="500",
            confidence=0.99,
            page_number=1,
            source_node="node-001",
            normalized_value=None,
            metadata={},
        ),

        Entity(
            entity_id="node-001_entity_3",
            entity_type="DOSAGE_UNIT",
            value="milligrams",
            confidence=0.98,
            page_number=1,
            source_node="node-001",
            normalized_value=None,
            metadata={},
        ),

        Entity(
            entity_id="node-001_entity_4",
            entity_type="FREQUENCY",
            value="twice daily",
            confidence=0.99,
            page_number=1,
            source_node="node-001",
            normalized_value=None,
            metadata={},
        ),

        Entity(
            entity_id="node-001_entity_5",
            entity_type="BIOMARKER",
            value="HER2",
            confidence=0.97,
            page_number=1,
            source_node="node-001",
            normalized_value=None,
            metadata={
                "attributes": {
                    "status": "positive",
                }
            },
        ),

        Entity(
            entity_id="node-001_entity_6",
            entity_type="GENE",
            value="brca1",
            confidence=0.96,
            page_number=1,
            source_node="node-001",
            normalized_value=None,
            metadata={},
        ),
    ]

    # ==========================================================
    # Workflow State
    #
    # IMPORTANT:
    # No WorkflowState.metadata.
    #
    # Entities belong to EntityState.
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="entity-normalization-test",
        ),

        document=DocumentState(
            document_id="doc-normalization-001",
            file_name="clinical_report.txt",
            file_path="clinical_report.txt",
            file_type="text/plain",
            pages=[
                PageState(
                    page_number=1,
                    content=(
                        "Metformin 500 milligrams "
                        "twice daily. HER2 positive. "
                        "brca1 mutation detected."
                    ),
                )
            ],
        ),

        layout=LayoutState(),

        entities=EntityState(
            entities=extracted_entities,
        ),

        validation=ValidationState(),

        model=ModelState(),

        metrics=MetricsState(),

        checkpoint=CheckpointState(
            checkpoint_id=str(uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            stage="entity_normalization",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()
    print("=" * 80)
    print("RUNNING ENTITY NORMALIZATION AGENT")
    print("=" * 80)

    result = await agent.execute(
        state
    )

    # ==========================================================
    # Results
    # ==========================================================

    entities = result.entities.entities

    print()
    print("=" * 80)
    print("NORMALIZATION RESULT")
    print("=" * 80)

    print()

    print(
        "Entity Count:",
        len(entities),
    )

    print()

    for entity in entities:

        normalization_status = entity.metadata.get(
            "normalization_status"
        )

        normalization_confidence = entity.metadata.get(
            "normalization_confidence"
        )

        print(
            f"- ID: {entity.entity_id}"
        )

        print(
            f"  Type: {entity.entity_type}"
        )

        print(
            f"  Original: {entity.value}"
        )

        print(
            f"  Normalized: "
            f"{entity.normalized_value}"
        )

        print(
            f"  Confidence: {entity.confidence}"
        )

        print(
            f"  Page: {entity.page_number}"
        )

        print(
            f"  Source Node: {entity.source_node}"
        )

        print(
            f"  Normalization Status: "
            f"{normalization_status}"
        )

        print(
            f"  Normalization Confidence: "
            f"{normalization_confidence}"
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