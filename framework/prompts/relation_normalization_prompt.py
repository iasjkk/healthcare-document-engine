"""
Prompt for healthcare relation normalization.
"""

from __future__ import annotations

import json
from typing import Any

from framework.prompts.base_prompt import BasePrompt


class RelationNormalizationPrompt(BasePrompt):
    """
    Builds prompts for normalizing healthcare
    relation types.
    """

    def __init__(
        self,
        version: str = "1.0.0",
    ) -> None:

        super().__init__(
            name="relation_normalization",
            version=version,
        )

    def build(
        self,
        relations: list[dict[str, Any]],
    ) -> str:
        """
        Build the relation normalization prompt.
        """

        relations_json = json.dumps(
            relations,
            indent=2,
            ensure_ascii=False,
        )

        return f"""
You are an expert healthcare knowledge graph
relation normalization system.

Your task is to normalize relationship types
between healthcare entities.

You will receive relations produced by a
previous relation extraction stage.

Your job is ONLY to normalize the relation type.

IMPORTANT RULES:

1. Preserve relation_id exactly.
2. Do not modify source_entity_id.
3. Do not modify target_entity_id.
4. Do not invent entities.
5. Do not remove relations.
6. Do not invent clinical facts.
7. Preserve the meaning of the original relation.
8. Map semantically equivalent relation expressions
   to one canonical relation type.
9. Use concise UPPER_SNAKE_CASE relation types.
10. Return exactly one result for every input relation.
11. Keep confidence between 0 and 1.
12. Return ONLY valid JSON.
13. Do not use Markdown code fences.

Examples of normalization:

"takes"
"taking"
"uses"
"prescribed"
    -> MEDICATION_TAKEN_BY

"has dosage"
"dosage"
"dose"
    -> MEDICATION_HAS_DOSAGE

"frequency"
"taken twice daily"
"administered daily"
    -> MEDICATION_HAS_FREQUENCY

"indication"
"used for"
"treatment for"
    -> MEDICATION_TREATS_CONDITION

"biomarker status"
"marker status"
    -> BIOMARKER_HAS_STATUS

"gene mutation"
"gene variant"
    -> GENE_HAS_VARIANT

"associated with"
"related to"
    -> ASSOCIATED_WITH

"causes"
"leads to"
    -> CAUSES

Only use a relation type that preserves the
meaning of the original relation.

If no normalization is appropriate, preserve
the original relation type after converting it
to a clean UPPER_SNAKE_CASE representation.

INPUT RELATIONS:

{relations_json}

Return JSON using exactly this structure:

{{
  "relations": [
    {{
      "relation_id": "string",
      "normalized_relation_type": "CANONICAL_RELATION",
      "confidence": 0.0,
      "normalization_status": "normalized",
      "original_relation_type": "string",
      "attributes": {{}},
      "metadata": {{}}
    }}
  ],
  "confidence": 0.0,
  "notes": null
}}
""".strip()