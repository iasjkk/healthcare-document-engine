"""
End-to-end test for RelationNormalizationAgent.

Run:

    python -m tests.test_relation_normalization_agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.relation.relation_normalization_agent import (
    RelationNormalizationAgent,
)

from framework.prompts.prompt_registry import (
    PromptRegistry,
)

from framework.prompts.relation_normalization_prompt import (
    RelationNormalizationPrompt,
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

from framework.state.relation_state import (
    Relation,
    RelationState,
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
        "relation_normalization",
        RelationNormalizationPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = RelationNormalizationAgent(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ==========================================================
    # Entities
    # ==========================================================

    entities = [
        Entity(
            entity_id="entity_001",
            entity_type="MEDICATION",
            value="Metformin",
            confidence=0.98,
            page_number=1,
            source_node="node-001",
            normalized_value="metformin",
            metadata={},
        ),
        Entity(
            entity_id="entity_002",
            entity_type="DOSAGE",
            value="500",
            confidence=0.99,
            page_number=1,
            source_node="node-001",
            normalized_value="500 mg",
            metadata={},
        ),
        Entity(
            entity_id="entity_003",
            entity_type="FREQUENCY",
            value="twice daily",
            confidence=0.99,
            page_number=1,
            source_node="node-001",
            normalized_value="BID",
            metadata={},
        ),
        Entity(
            entity_id="entity_004",
            entity_type="BIOMARKER",
            value="HER2",
            confidence=0.97,
            page_number=1,
            source_node="node-001",
            normalized_value="HER2",
            metadata={},
        ),
    ]

    # ==========================================================
    # Relations
    #
    # These represent output from RelationExtractionAgent.
    # ==========================================================

    relations = [
        Relation(
            relation_id="relation_001",
            source_entity_id="entity_001",
            target_entity_id="entity_002",
            relation_type="has dosage",
            confidence=0.96,
            attributes={},
            metadata={},
        ),

        Relation(
            relation_id="relation_002",
            source_entity_id="entity_001",
            target_entity_id="entity_003",
            relation_type="taken twice daily",
            confidence=0.95,
            attributes={},
            metadata={},
        ),

        Relation(
            relation_id="relation_003",
            source_entity_id="entity_004",
            target_entity_id="entity_004",
            relation_type="biomarker status",
            confidence=0.90,
            attributes={
                "status": "positive",
            },
            metadata={},
        ),
    ]

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="relation-normalization-test",
        ),

        document=DocumentState(
            document_id="doc-relation-normalization-001",
            file_name="clinical_report.txt",
            file_path="clinical_report.txt",
            file_type="text/plain",
            pages=[
                PageState(
                    page_number=1,
                    content=(
                        "Metformin 500 milligrams "
                        "twice daily. HER2 positive."
                    ),
                )
            ],
        ),

        layout=LayoutState(),

        entities=EntityState(
            entities=entities,
        ),

        relations=RelationState(
            relations=relations,
        ),

        validation=ValidationState(),

        model=ModelState(),

        metrics=MetricsState(),

        checkpoint=CheckpointState(
            checkpoint_id=str(uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            stage="relation_normalization",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()

    print("=" * 80)
    print("RUNNING RELATION NORMALIZATION AGENT")
    print("=" * 80)

    result = await agent.execute(
        state
    )

    # ==========================================================
    # Results
    # ==========================================================

    normalized_relations = (
        result.relations.relations
    )

    print()

    print("=" * 80)
    print("RELATION NORMALIZATION RESULT")
    print("=" * 80)

    print()

    print(
        "Relation Count:",
        len(normalized_relations),
    )

    print()

    for relation in normalized_relations:

        normalization_status = (
            relation.metadata.get(
                "normalization_status"
            )
        )

        normalization_confidence = (
            relation.metadata.get(
                "normalization_confidence"
            )
        )

        original_relation_type = (
            relation.metadata.get(
                "original_relation_type"
            )
        )

        print(
            f"- ID: "
            f"{relation.relation_id}"
        )

        print(
            f"  Source Entity: "
            f"{relation.source_entity_id}"
        )

        print(
            f"  Target Entity: "
            f"{relation.target_entity_id}"
        )

        print(
            f"  Original Relation: "
            f"{original_relation_type}"
        )

        print(
            f"  Normalized Relation: "
            f"{relation.relation_type}"
        )

        print(
            f"  Confidence: "
            f"{normalization_confidence}"
        )

        print(
            f"  Status: "
            f"{normalization_status}"
        )

        print(
            f"  Attributes: "
            f"{relation.attributes}"
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