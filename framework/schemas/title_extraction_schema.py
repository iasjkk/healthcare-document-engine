"""
Schema for Title Extraction.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TitleExtractionResponse(BaseModel):
    """
    Structured document title extraction result.
    """

    title: str = ""

    original_text: str = ""

    title_type: str = "general"

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    notes: str = ""

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )