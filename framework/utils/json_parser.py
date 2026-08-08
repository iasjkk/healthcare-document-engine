"""
Utilities for parsing LLM JSON responses.

Handles:

- Raw JSON
- JSON inside Markdown code fences
- Validation with Pydantic schemas
"""

from __future__ import annotations

import json
import re
from typing import Any, Type, TypeVar

from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


# ==========================================================
# JSON Extraction
# ==========================================================

def extract_json(text: str) -> dict[str, Any]:
    """
    Extract JSON object from an LLM response.

    Supports:

    - Raw JSON
    - ```json ... ```
    - ``` ... ```
    """

    text = text.strip()

    # ------------------------------------------------------
    # Raw JSON
    # ------------------------------------------------------

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # ------------------------------------------------------
    # Markdown JSON block
    # ------------------------------------------------------

    pattern = r"```(?:json)?\s*(.*?)\s*```"

    match = re.search(
        pattern,
        text,
        flags=re.DOTALL,
    )

    if match:

        json_text = match.group(1)

        return json.loads(json_text)

    raise ValueError(
        "No valid JSON found in model response."
    )


# ==========================================================
# Schema Validation
# ==========================================================

def parse_json_response(
    text: str,
    schema: Type[T],
) -> T:
    """
    Parse an LLM response into a Pydantic model.

    Example
    -------
    response = parse_json_response(
        llm_output,
        DocumentStructureResponse,
    )
    """

    data = extract_json(text)

    try:

        return schema.model_validate(data)

    except ValidationError as exc:

        raise ValueError(
            f"Schema validation failed:\n{exc}"
        ) from exc