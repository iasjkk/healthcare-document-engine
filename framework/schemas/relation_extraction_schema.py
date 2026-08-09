"""
Schemas for healthcare relation extraction.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class RelationExtractionResult(BaseModel):
    """
    Represents one relation extracted between two healthcare entities.
    """

    relation_id: str = Field(
        ...,
        description="Unique identifier for the extracted relation.",
    )

    source_entity_id: str = Field(
        ...,
        description="ID of the source entity.",
    )

    target_entity_id: str = Field(
        ...,
        description="ID of the target entity.",
    )

    relation_type: str = Field(
        ...,
        description="Original relation type expressed in the document.",
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence in the extracted relation.",
    )

    attributes: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional relation attributes.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional extraction metadata.",
    )


class RelationExtractionResponse(BaseModel):
    """
    Complete response returned by the Relation Extraction Agent.
    """

    relations: list[RelationExtractionResult] = Field(
        default_factory=list,
        description="Extracted healthcare relations.",
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Overall extraction confidence.",
    )

    notes: str = Field(
        default="",
        description="Extraction notes or ambiguities.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional response metadata.",
    )