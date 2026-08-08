"""
Schema for Paragraph Extraction Agent.

The Paragraph Extraction Agent receives a document layout
node classified as a paragraph and converts the content into
a clean, structured representation.

The schema deliberately keeps the original text so that
downstream clinical entity extraction can work from the
source content without losing information.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ParagraphExtractionResponse(BaseModel):
    """
    Structured response returned by the LLM for a paragraph.
    """

    text: str = Field(
        default="",
        description=(
            "Cleaned paragraph text while preserving "
            "the original meaning and information."
        ),
    )

    original_text: str = Field(
        default="",
        description=(
            "Original paragraph text supplied to the model."
        ),
    )

    paragraph_type: str = Field(
        default="general",
        description=(
            "General classification of the paragraph content."
        ),
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description=(
            "Confidence in the paragraph extraction."
        ),
    )

    notes: str = Field(
        default="",
        description=(
            "Notes about OCR problems, ambiguity, "
            "or extraction decisions."
        ),
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Additional metadata associated with "
            "the extracted paragraph."
        ),
    )