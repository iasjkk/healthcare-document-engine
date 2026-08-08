"""
Schema for Key-Value Extraction.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class KeyValueItem(BaseModel):
    """Single extracted key-value pair."""

    key: str = ""

    value: str = ""

    normalized_key: str = ""

    value_type: str = "text"

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class KeyValueExtractionResponse(BaseModel):
    """Structured key-value extraction result."""

    items: list[KeyValueItem] = Field(
        default_factory=list
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    notes: str = ""