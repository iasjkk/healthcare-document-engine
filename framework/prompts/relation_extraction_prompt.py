"""
Prompt for healthcare relation extraction.
"""

from __future__ import annotations

import json
from typing import Any

from framework.prompts.base_prompt import BasePrompt


class RelationExtractionPrompt(BasePrompt):
    """
    Builds prompts for extracting relationships between
    healthcare entities.
    """

    def __init__(self) -> None:
        super().__init__(
            name="relation_extraction"
        )

    def build(
        self,
        *,
        entities: list[dict[str, Any]],
        text: str,
        **kwargs: Any,
    ) -> str:
        """
        Build the relation extraction prompt.
        """

        entities_json = json.dumps(
            entities,
            indent=2,
            ensure_ascii=False,
            default=str,
        )

        return f"""
You are a healthcare relation extraction system.

Your task is to identify explicit semantic relationships
between healthcare entities appearing in the supplied document.

You will receive:

1. The original document text.
2. A list of entities already extracted from the document.

Your job is ONLY to extract relationships that are explicitly
supported by the document.

============================================================
IMPORTANT RULES
============================================================

1. Only extract relations supported by the document text.

2. Do NOT invent relations.

3. Do NOT infer unsupported clinical relationships.

4. Use the supplied entity IDs exactly.

5. Every relation MUST reference an existing source entity.

6. Every relation MUST reference an existing target entity.

7. Do not create entities.

8. Do not modify entity IDs.

9. Preserve the meaning expressed in the source document.

10. If there is no explicit relationship, return an empty list.

11. Extract clinically meaningful relationships such as:

    - medication → dosage
    - medication → frequency
    - medication → route
    - medication → status
    - diagnosis → symptom
    - diagnosis → finding
    - diagnosis → procedure
    - diagnosis → biomarker
    - biomarker → status
    - biomarker → value
    - biomarker → percentage
    - gene → variant
    - gene → mutation
    - procedure → finding
    - pathology finding → diagnosis
    - laboratory test → result
    - laboratory test → value
    - laboratory test → unit

12. Relation types should preserve the wording and meaning
    found in the source document.

13. Do not normalize relation types into canonical terminology.
    Normalization is performed by a later agent.

14. Use concise relation type names.

15. Every extracted relation must have a unique relation_id.

16. Confidence must be between 0.0 and 1.0.

============================================================
RELATION TYPE EXAMPLES
============================================================

Examples include:

MEDICATION_HAS_DOSAGE

MEDICATION_HAS_FREQUENCY

MEDICATION_HAS_ROUTE

MEDICATION_HAS_STATUS

DIAGNOSIS_HAS_SYMPTOM

DIAGNOSIS_HAS_FINDING

DIAGNOSIS_HAS_BIOMARKER

DIAGNOSIS_ASSOCIATED_WITH_PROCEDURE

BIOMARKER_HAS_STATUS

BIOMARKER_HAS_VALUE

BIOMARKER_HAS_PERCENTAGE

GENE_HAS_VARIANT

GENE_HAS_MUTATION

PROCEDURE_HAS_FINDING

PATHOLOGY_HAS_DIAGNOSIS

LAB_TEST_HAS_RESULT

LAB_TEST_HAS_VALUE

LAB_TEST_HAS_UNIT

These are examples only.

Do not create a relation merely because its type appears
in the examples.

============================================================
DOCUMENT TEXT
============================================================

{text}

============================================================
EXTRACTED ENTITIES
============================================================

{entities_json}

============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

Return exactly this structure:

{{
    "relations": [
        {{
            "relation_id": "relation_001",
            "source_entity_id": "entity_001",
            "target_entity_id": "entity_002",
            "relation_type": "MEDICATION_HAS_DOSAGE",
            "confidence": 0.98,
            "attributes": {{}},
            "metadata": {{}}
        }}
    ],
    "confidence": 0.98,
    "notes": "",
    "metadata": {{}}
}}

============================================================
FINAL REQUIREMENTS
============================================================

- Valid JSON only.
- No Markdown.
- No explanation outside JSON.
- Do not use ```json.
- Do not invent relations.
- Do not invent entities.
- Use only supplied entity IDs.
- Preserve explicit clinical meaning.
"""