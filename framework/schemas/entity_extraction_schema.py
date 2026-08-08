"""
Schema for healthcare entity extraction.

The schema intentionally preserves the original
text span so that downstream normalization and
validation can trace every entity back to the
document source.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ExtractedEntity(BaseModel):
    """
    Single healthcare entity extracted from a document.
    """

    entity_id: str = ""

    entity_type: str = "unknown"

    text: str = ""

    normalized_text: str = ""

    page_number: int = 1

    source_node_id: str = ""

    start_offset: int | None = None

    end_offset: int | None = None

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    attributes: dict[str, Any] = Field(
        default_factory=dict
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class EntityExtractionResponse(BaseModel):
    """
    Response containing healthcare entities.
    """

    entities: list[ExtractedEntity] = Field(
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