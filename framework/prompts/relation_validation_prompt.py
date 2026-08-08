"""
Prompt for healthcare relation validation.
"""

from __future__ import annotations

import json
from typing import Any

from framework.prompts.base_prompt import BasePrompt


class RelationValidationPrompt(BasePrompt):
    """
    Builds prompts for validating healthcare relations.
    """

    def __init__(
        self,
        version: str = "1.0.0",
    ) -> None:

        super().__init__(
            name="relation_validation",
            version=version,
        )

    def build(
        self,
        relations: list[dict[str, Any]],
        entities: list[dict[str, Any]],
    ) -> str:
        """
        Build the relation validation prompt.
        """

        relations_json = json.dumps(
            relations,
            indent=2,
            ensure_ascii=False,
        )

        entities_json = json.dumps(
            entities,
            indent=2,
            ensure_ascii=False,
        )

        return f"""
You are an expert healthcare knowledge graph
relation validation system.

Your task is to validate relationships between
healthcare entities.

You will receive:

1. A list of healthcare entities.
2. A list of extracted and normalized relations.

Your job is to determine whether each relation
is clinically and structurally reasonable.

IMPORTANT RULES:

1. Preserve relation_id exactly.
2. Do not modify source_entity_id.
3. Do not modify target_entity_id.
4. Do not invent entities.
5. Do not invent relations.
6. Do not change relation_type.
7. Do not normalize the relation again.
8. Validate whether the source entity exists.
9. Validate whether the target entity exists.
10. Check whether the relation is semantically
    compatible with the entity types.
11. Do not reject a relation merely because it
    is uncommon if it is clinically plausible.
12. Do not create medical facts that are not present
    in the input.
13. Use confidence between 0 and 1.
14. Return one validation result for every relation.
15. Return ONLY valid JSON.
16. Do not use Markdown code fences.

VALIDATION STATUS VALUES:

"valid"
    Relation is structurally and semantically valid.

"invalid"
    Relation contains a serious structural or
    semantic problem.

"warning"
    Relation is possible but has uncertainty or
    insufficient evidence.

Examples:

MEDICATION -> DOSAGE
relation_type = MEDICATION_HAS_DOSAGE
    => valid

MEDICATION -> FREQUENCY
relation_type = MEDICATION_HAS_FREQUENCY
    => valid

GENE -> VARIANT
relation_type = GENE_HAS_VARIANT
    => valid

BIOMARKER -> STATUS
relation_type = BIOMARKER_HAS_STATUS
    => valid

Unknown source entity
    => invalid

Unknown target entity
    => invalid

A relation whose entity types clearly contradict
the relation type
    => invalid

A clinically plausible but unusual relation
    => warning rather than automatically invalid.

ENTITIES:

{entities_json}

RELATIONS:

{relations_json}

Return JSON using exactly this structure:

{{
  "relations": [
    {{
      "relation_id": "relation_001",
      "is_valid": true,
      "validation_status": "valid",
      "confidence": 0.95,
      "issues": [],
      "warnings": [],
      "attributes": {{}},
      "metadata": {{}}
    }}
  ],
  "confidence": 0.95,
  "notes": null
}}
""".strip()