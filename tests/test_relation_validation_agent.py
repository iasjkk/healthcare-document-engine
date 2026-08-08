"""
End-to-end test for RelationValidationAgent.

Run from project root:

    python -m tests.test_relation.relation_validation.agent

Requires:

    OPEN_ROUTER_API_KEY
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

from framework.agents.relation.relation_validation_agent import (
    RelationValidationAgent,
)

from framework.prompts.prompt_registry import (
    PromptRegistry,
)

from framework.prompts.relation_validation_prompt import (
    RelationValidationPrompt,
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
    Relation,
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
        "relation_validation",
        RelationValidationPrompt(),
    )

    # ==========================================================
    # Agent
    # ==========================================================

    agent = RelationValidationAgent(
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
            value="500 mg",
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
    # ==========================================================

    relations = [

        # ------------------------------------------------------
        # Valid relation.
        # ------------------------------------------------------

        Relation(
            relation_id="relation_001",
            source_entity_id="entity_001",
            target_entity_id="entity_002",
            relation_type="MEDICATION_HAS_DOSAGE",
            confidence=0.96,
            attributes={},
            metadata={},
        ),

        # ------------------------------------------------------
        # Valid relation.
        # ------------------------------------------------------

        Relation(
            relation_id="relation_002",
            source_entity_id="entity_001",
            target_entity_id="entity_003",
            relation_type="MEDICATION_HAS_FREQUENCY",
            confidence=0.95,
            attributes={},
            metadata={},
        ),

        # ------------------------------------------------------
        # Invalid relation intentionally included.
        #
        # entity_999 does not exist.
        # Application-level validation must catch this.
        # ------------------------------------------------------

        Relation(
            relation_id="relation_003",
            source_entity_id="entity_001",
            target_entity_id="entity_999",
            relation_type="MEDICATION_HAS_DOSAGE",
            confidence=0.90,
            attributes={},
            metadata={},
        ),
    ]

    # ==========================================================
    # Workflow State
    # ==========================================================

    state = WorkflowState(

        execution=ExecutionState(
            run_id=str(uuid4()),
            workflow_id="relation-validation-test",
        ),

        document=DocumentState(
            document_id="doc-relation-validation-001",
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
            stage="relation_validation",
        ),
    )

    # ==========================================================
    # Execute
    # ==========================================================

    print()

    print("=" * 80)
    print("RUNNING RELATION VALIDATION AGENT")
    print("=" * 80)

    result = await agent.execute(
        state
    )

    # ==========================================================
    # Results
    # ==========================================================

    validated_relations = (
        result.relations.relations
    )

    print()

    print("=" * 80)
    print("RELATION VALIDATION RESULT")
    print("=" * 80)

    print()

    print(
        "Relation Count:",
        len(validated_relations),
    )

    print()

    for relation in validated_relations:

        status = relation.metadata.get(
            "validation_status"
        )

        is_valid = relation.metadata.get(
            "validation_is_valid"
        )

        confidence = relation.metadata.get(
            "validation_confidence"
        )

        issues = relation.metadata.get(
            "validation_issues",
            [],
        )

        warnings = relation.metadata.get(
            "validation_warnings",
            [],
        )

        print(
            f"- Relation ID: "
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
            f"  Relation Type: "
            f"{relation.relation_type}"
        )

        print(
            f"  Valid: "
            f"{is_valid}"
        )

        print(
            f"  Status: "
            f"{status}"
        )

        print(
            f"  Confidence: "
            f"{confidence}"
        )

        print(
            f"  Issues: "
            f"{issues}"
        )

        print(
            f"  Warnings: "
            f"{warnings}"
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