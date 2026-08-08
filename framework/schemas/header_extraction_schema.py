"""
Schema for Header Extraction.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HeaderItem(BaseModel):
    """Single extracted header."""

    text: str = ""

    page_number: int = 1

    header_type: str = "general"

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class HeaderExtractionResponse(BaseModel):
    """Structured header extraction result."""

    headers: list[HeaderItem] = Field(
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