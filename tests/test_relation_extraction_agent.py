"""
Test RelationExtractionAgent.

Run:

python -m tests.test_relation_extraction_agent
"""

from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime, timezone
from types import SimpleNamespace

from framework.agents.relation.relation_extraction_agent import (
    RelationExtractionAgent,
)
from framework.router.model_router import ModelRouter
from framework.state.relation_state import RelationState
from framework.state.workflow_state import WorkflowState


def create_mock_entities() -> list[dict]:
    """
    Create sample healthcare entities.
    """

    return [
        {
            "entity_id": "entity_001",
            "text": "Metformin",
            "entity_type": "MEDICATION",
            "normalized_value": "Metformin",
            "confidence": 0.99,
            "metadata": {},
        },
        {
            "entity_id": "entity_002",
            "text": "500 mg",
            "entity_type": "DOSAGE",
            "normalized_value": "500 mg",
            "confidence": 0.98,
            "metadata": {},
        },
        {
            "entity_id": "entity_003",
            "text": "twice daily",
            "entity_type": "FREQUENCY",
            "normalized_value": "twice daily",
            "confidence": 0.97,
            "metadata": {},
        },
        {
            "entity_id": "entity_004",
            "text": "HER2",
            "entity_type": "BIOMARKER",
            "normalized_value": "HER2",
            "confidence": 0.98,
            "metadata": {},
        },
        {
            "entity_id": "entity_005",
            "text": "positive",
            "entity_type": "STATUS",
            "normalized_value": "positive",
            "confidence": 0.96,
            "metadata": {},
        },
    ]


def create_test_state() -> WorkflowState:
    """
    Create a minimal WorkflowState.

    NOTE:
    Adapt the non-clinical state constructors only if your existing
    project requires additional mandatory fields.
    """

    entities = create_mock_entities()

    state = WorkflowState.model_construct(
        execution=None,
        document=SimpleNamespace(
            text=(
                "The patient was prescribed Metformin "
                "500 mg twice daily. HER2 was positive."
            )
        ),
        layout=None,
        entities=SimpleNamespace(
            entities=entities
        ),
        validation=None,
        relations=RelationState(),
        clinical_summary=None,
        model=None,
        metrics=None,
        checkpoint=None,
    )

    return state


class MockRouter:
    """
    Mock ModelRouter for deterministic testing.

    This avoids OpenRouter/API calls.
    """

    async def chat(
        self,
        capability: str,
        messages: list[dict[str, str]],
        **kwargs,
    ) -> dict:

        assert (
            capability
            == "relation_extraction"
        )

        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "relations": [
                                    {
                                        "relation_id": (
                                            "relation_001"
                                        ),
                                        "source_entity_id": (
                                            "entity_001"
                                        ),
                                        "target_entity_id": (
                                            "entity_002"
                                        ),
                                        "relation_type": (
                                            "MEDICATION_HAS_DOSAGE"
                                        ),
                                        "confidence": 0.98,
                                        "attributes": {},
                                        "metadata": {},
                                    },
                                    {
                                        "relation_id": (
                                            "relation_002"
                                        ),
                                        "source_entity_id": (
                                            "entity_001"
                                        ),
                                        "target_entity_id": (
                                            "entity_003"
                                        ),
                                        "relation_type": (
                                            "MEDICATION_HAS_FREQUENCY"
                                        ),
                                        "confidence": 0.97,
                                        "attributes": {},
                                        "metadata": {},
                                    },
                                    {
                                        "relation_id": (
                                            "relation_003"
                                        ),
                                        "source_entity_id": (
                                            "entity_004"
                                        ),
                                        "target_entity_id": (
                                            "entity_005"
                                        ),
                                        "relation_type": (
                                            "BIOMARKER_HAS_STATUS"
                                        ),
                                        "confidence": 0.96,
                                        "attributes": {},
                                        "metadata": {},
                                    },
                                ],
                                "confidence": 0.97,
                                "notes": "",
                                "metadata": {},
                            }
                        )
                    }
                }
            ]
        }


async def main() -> None:
    """
    Execute the relation extraction test.
    """

    print("=" * 80)
    print("RELATION EXTRACTION AGENT TEST")
    print("=" * 80)

    state = create_test_state()

    router = MockRouter()

    agent = RelationExtractionAgent(
        router=router
    )

    result = await agent.execute(
        state
    )

    relations = (
        result.relations.relations
    )

    print()
    print(
        f"Extracted relations: "
        f"{len(relations)}"
    )

    print()

    for relation in relations:

        print(
            f"Relation ID : "
            f"{relation.relation_id}"
        )

        print(
            f"Source      : "
            f"{relation.source_entity_id}"
        )

        print(
            f"Target      : "
            f"{relation.target_entity_id}"
        )

        print(
            f"Type        : "
            f"{relation.relation_type}"
        )

        print(
            f"Confidence  : "
            f"{relation.confidence}"
        )

        print("-" * 80)

    assert len(relations) == 3

    assert (
        relations[0].relation_type
        == "MEDICATION_HAS_DOSAGE"
    )

    assert (
        relations[1].relation_type
        == "MEDICATION_HAS_FREQUENCY"
    )

    assert (
        relations[2].relation_type
        == "BIOMARKER_HAS_STATUS"
    )

    print()
    print("PASS: Relation extraction test completed.")


if __name__ == "__main__":
    asyncio.run(main())