"""
Schema for List Extraction.

Represents ordered and unordered lists found in
healthcare documents.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ListItem(BaseModel):
    """Single list item."""

    item_id: str = ""

    text: str = ""

    position: int = 0

    level: int = 1

    marker: str = ""

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class ListExtractionResponse(BaseModel):
    """Structured list extraction result."""

    list_type: str = "unordered"

    items: list[ListItem] = Field(
        default_factory=list
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    notes: str = ""

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )