"""
Prompt for Table Validation Agent.
"""

from __future__ import annotations

import json
from typing import Any

from framework.prompts.base_prompt import BasePrompt


class TableValidationPrompt(BasePrompt):
    """
    Builds prompts for validating extracted tables.
    """

    def __init__(
        self,
        version: str = "1.0.0",
    ) -> None:

        super().__init__(
            name="table_validation",
            version=version,
        )

    def build(
        self,
        table: dict[str, Any],
        page_number: int,
        node_id: str,
    ) -> str:
        """
        Build validation prompt.
        """

        table_json = json.dumps(
            table,
            indent=2,
            ensure_ascii=False,
        )

        return f"""
You are an expert healthcare document
table validation system.

Validate the following table extracted from
a healthcare document.

DO NOT extract a new table.

DO NOT modify the supplied table.

Your task is only to determine whether the
existing extraction is structurally and
semantically reasonable.

--------------------------------------------------
SOURCE INFORMATION
--------------------------------------------------

Page Number:
{page_number}

Source Node ID:
{node_id}

--------------------------------------------------
EXTRACTED TABLE
--------------------------------------------------

{table_json}

--------------------------------------------------
VALIDATION RULES
--------------------------------------------------

Check:

1. Are the headers reasonable?

2. Are rows consistently structured?

3. Does the number of values in each row
   reasonably correspond to the headers?

4. Are cells malformed or obviously misplaced?

5. Are there missing values that appear to be
   extraction errors?

6. Are duplicate rows or columns present?

7. Does the content plausibly represent a table?

8. Are numeric values reasonably represented?

9. Are healthcare units preserved?

10. Are clinically meaningful values represented
    consistently?

IMPORTANT:

- Do not invent missing values.
- Do not correct the table.
- Do not rewrite cell values.
- Do not normalize medical terminology.
- Do not modify headers.
- Do not modify rows.
- Do not modify source identifiers.
- Preserve the supplied table_id.
- Return exactly one validation result.

--------------------------------------------------
STATUS
--------------------------------------------------

Use:

valid
    Table is usable.

warning
    Table is usable but contains uncertainty.

invalid
    Table contains a significant structural
    or semantic problem.

--------------------------------------------------
OUTPUT
--------------------------------------------------

Return ONLY valid JSON.

Return exactly this structure:

{{
  "result": {{
    "table_id": "node-001_table",
    "is_valid": true,
    "validation_status": "valid",
    "confidence": 0.98,
    "issues": [],
    "warnings": [],
    "attributes": {{}},
    "metadata": {{}}
  }},
  "confidence": 0.98,
  "notes": ""
}}
""".strip()