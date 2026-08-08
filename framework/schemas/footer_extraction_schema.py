"""
Schema for Footer Extraction.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class FooterItem(BaseModel):
    """Single extracted footer."""

    text: str = ""

    page_number: int = 1

    footer_type: str = "general"

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class FooterExtractionResponse(BaseModel):
    """Structured footer extraction result."""

    footers: list[FooterItem] = Field(
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