"""
Schemas for healthcare relation normalization.

Defines the structured response expected from
RelationNormalizationAgent.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class RelationNormalizationResult(BaseModel):
    """
    Normalization result for a single relation.
    """

    relation_id: str

    normalized_relation_type: str

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    normalization_status: str = "normalized"

    original_relation_type: str | None = None

    attributes: dict[str, Any] = Field(
        default_factory=dict
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class RelationNormalizationResponse(BaseModel):
    """
    Complete relation normalization response.
    """

    relations: list[RelationNormalizationResult] = Field(
        default_factory=list
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    notes: str | None = None
