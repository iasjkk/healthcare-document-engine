"""
Schema for Section Heading Extraction.

A section heading identifies the semantic section of a
healthcare document without performing clinical interpretation.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SectionHeadingExtractionResponse(BaseModel):
    """
    Structured section-heading extraction response.
    """

    text: str = Field(
        default="",
        description="Cleaned section heading text.",
    )

    original_text: str = Field(
        default="",
        description="Original heading text.",
    )

    section_type: str = Field(
        default="general",
        description=(
            "Broad section category such as history, "
            "medications, diagnosis, laboratory, etc."
        ),
    )

    level: int = Field(
        default=1,
        ge=1,
        le=10,
        description="Hierarchy level of the heading.",
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Extraction confidence.",
    )

    notes: str = Field(
        default="",
        description="Extraction or OCR notes.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional heading metadata.",
    )