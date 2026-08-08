"""
Schema for healthcare entity normalization.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class NormalizedEntity(BaseModel):
    """
    Normalized representation of an extracted entity.
    """

    entity_id: str = ""

    entity_type: str = "unknown"

    original_text: str = ""

    normalized_text: str = ""

    page_number: int = 1

    source_node_id: str = ""

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    normalization_status: str = "unchanged"

    attributes: dict[str, Any] = Field(
        default_factory=dict
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class EntityNormalizationResponse(BaseModel):
    """
    Response containing normalized entities.
    """

    entities: list[NormalizedEntity] = Field(
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