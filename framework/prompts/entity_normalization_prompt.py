"""
Prompt for healthcare entity normalization.
"""

from __future__ import annotations

import json

from framework.prompts.base_prompt import BasePrompt


class EntityNormalizationPrompt(BasePrompt):
    """
    Normalize extracted healthcare entities.
    """

    def __init__(self) -> None:

        super().__init__(
            name="entity_normalization",
            version="1.0.0",
        )

    def build(
        self,
        *,
        entities: list[dict],
    ) -> str:

        entity_json = json.dumps(
            entities,
            indent=2,
            ensure_ascii=False,
        )

        return f"""
You are an expert healthcare information
normalization system.

Your task is to normalize already-extracted
healthcare entities.

The entities have already been extracted from
the source document.

Do NOT perform new entity extraction.

Do NOT invent information.

Do NOT diagnose the patient.

Do NOT infer clinical meaning that is not
explicitly represented by the source entity.

------------------------------------------------------------
OUTPUT
------------------------------------------------------------

Return ONLY valid JSON.

Do not use Markdown.

Do not use ```json.

Return exactly:

{{
    "entities": [
        {{
            "entity_id": "",
            "entity_type": "unknown",
            "original_text": "",
            "normalized_text": "",
            "page_number": 1,
            "source_node_id": "",
            "confidence": 0.0,
            "normalization_status": "unchanged",
            "attributes": {{}},
            "metadata": {{}}
        }}
    ],
    "confidence": 0.0,
    "notes": "",
    "metadata": {{}}
}}

------------------------------------------------------------
NORMALIZATION PRINCIPLES
------------------------------------------------------------

1. Preserve original_text exactly.

2. normalized_text should be a clean,
   consistent representation.

3. Do not change the underlying meaning.

4. Do not add information that is not present.

5. Preserve page_number.

6. Preserve source_node_id.

7. Preserve entity_id.

8. Do not remove provenance.

------------------------------------------------------------
NORMALIZATION STATUS
------------------------------------------------------------

Use one of:

"normalized"

"unchanged"

"partially_normalized"

"uncertain"

------------------------------------------------------------
PERSON NAMES
------------------------------------------------------------

Example:

Original:

"John Doe"

Normalized:

"John Doe"

Status:

"unchanged"

Do not reorder the name unless the source
explicitly indicates a structured format.

------------------------------------------------------------
MEDICATIONS
------------------------------------------------------------

Example:

Original:

"Metformin"

Normalized:

"metformin"

Attributes may contain:

{{
    "generic_name": "metformin"
}}

Do not invent a brand name.

------------------------------------------------------------
DOSAGE
------------------------------------------------------------

Example:

"500"

Normalized:

"500"

Do not convert units here.

------------------------------------------------------------
DOSAGE UNITS
------------------------------------------------------------

Normalize obvious textual equivalents.

Example:

"milligrams"

→

"mg"

Example:

"milliliter"

→

"mL"

Only perform normalization when unambiguous.

------------------------------------------------------------
FREQUENCY
------------------------------------------------------------

Examples:

"twice daily"

"2 times per day"

"bid"

If the source explicitly contains:

"bid"

you may normalize to:

"twice daily"

Do not infer frequency from dosage.

------------------------------------------------------------
LAB UNITS
------------------------------------------------------------

Normalize obvious unit formatting.

Examples:

"mg / dL"

→

"mg/dL"

"g / L"

→

"g/L"

Do not convert units mathematically.

Unit conversion belongs to a later module.

------------------------------------------------------------
DATES
------------------------------------------------------------

Do not convert dates into a different
calendar representation.

For example:

"12/05/1980"

may remain:

"12/05/1980"

Date standardization will happen in a
dedicated temporal normalization layer.

------------------------------------------------------------
BIOMARKERS
------------------------------------------------------------

Example:

"HER2"

may normalize to:

"HER2"

Do not replace it with another biomarker.

If the source contains:

"HER2 positive"

preserve the status in attributes:

{{
    "status": "positive"
}}

------------------------------------------------------------
GENES
------------------------------------------------------------

Examples:

"brca1"

→

"BRCA1"

"BRCA-1"

→

"BRCA1"

Only normalize obvious formatting differences.

Do not infer a gene from an unrelated term.

------------------------------------------------------------
SPECIMEN IDENTIFIERS
------------------------------------------------------------

Preserve identifiers exactly unless there is
an obvious formatting normalization.

Do NOT remove:

- leading zeros
- hyphens
- prefixes

unless the normalization is explicitly safe.

------------------------------------------------------------
DIAGNOSES
------------------------------------------------------------

Do not replace a diagnosis with a more specific
diagnosis.

Example:

"Invasive ductal carcinoma"

must not become:

"Breast cancer"

unless the source explicitly says that.

------------------------------------------------------------
UNKNOWN / UNCERTAIN
------------------------------------------------------------

If normalization is uncertain:

keep the original text

and use:

"normalization_status": "uncertain"

------------------------------------------------------------
INPUT ENTITIES
------------------------------------------------------------

{entity_json}

------------------------------------------------------------
FINAL INSTRUCTION
------------------------------------------------------------

Return ONLY the JSON object.
"""