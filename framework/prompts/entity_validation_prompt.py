"""
Prompt for healthcare entity validation.
"""

from __future__ import annotations

import json
from typing import Any

from framework.prompts.base_prompt import BasePrompt


class EntityValidationPrompt(BasePrompt):
    """
    Build the prompt used to validate extracted
    and normalized healthcare entities.
    """

    def __init__(
        self,
        version: str = "1.0.0",
    ) -> None:

        super().__init__(
            name="entity_validation",
            version=version,
        )

    def build(
        self,
        entities: list[dict[str, Any]],
    ) -> str:
        """
        Build entity validation prompt.
        """

        entities_json = json.dumps(
            entities,
            indent=2,
            ensure_ascii=False,
        )

        return f"""
You are an expert healthcare information
validation system.

Your task is to validate healthcare entities
that were extracted from a clinical document
and subsequently normalized.

You must evaluate:

1. Whether the entity text is clinically plausible.
2. Whether the entity type is appropriate.
3. Whether the normalized value is appropriate.
4. Whether the entity contains obvious extraction errors.
5. Whether there are inconsistencies between the
   entity type, original text, and normalized value.
6. Whether the entity appears to be a false positive.
7. Whether the entity contains clinically meaningful
   warnings or issues.

IMPORTANT RULES:

- Do not invent entities.
- Do not invent clinical facts.
- Do not change entity IDs.
- Do not change page numbers.
- Do not change source node IDs.
- Preserve the original entity provenance.
- Validate each entity independently.
- If an entity is valid, return is_valid=true.
- If an entity is suspicious or incorrect, return
  is_valid=false.
- Use corrected_value only when a clear correction
  can be confidently suggested.
- Use corrected_entity_type only when the entity
  type is clearly incorrect.
- Keep confidence between 0 and 1.
- Return one validation result for every input entity.
- Return ONLY valid JSON.
- Do not use Markdown code fences.

INPUT ENTITIES:

{entities_json}

Return JSON using exactly this structure:

{{
  "entities": [
    {{
      "entity_id": "string",
      "is_valid": true,
      "confidence": 0.0,
      "validation_status": "valid",
      "issues": [],
      "warnings": [],
      "corrected_value": null,
      "corrected_entity_type": null,
      "metadata": {{}}
    }}
  ],
  "confidence": 0.0,
  "notes": null
}}
""".strip()