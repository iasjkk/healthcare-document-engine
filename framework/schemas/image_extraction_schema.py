"""
Schema for Image/Figure Extraction.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ImageFigureItem(BaseModel):
    """Single extracted image or figure."""

    figure_id: str = ""

    title: str = ""

    figure_type: str = "unknown"

    description: str = ""

    page_number: int = 1

    text_content: str = ""

    has_caption: bool = False

    caption: str = ""

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class ImageFigureExtractionResponse(BaseModel):
    """Structured image/figure extraction result."""

    figures: list[ImageFigureItem] = Field(
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