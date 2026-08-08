"""
Schemas for healthcare relation validation.

Defines the structured response expected from
RelationValidationAgent.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class RelationValidationResult(BaseModel):
    """
    Validation result for a single healthcare relation.
    """

    relation_id: str

    is_valid: bool

    validation_status: str = "valid"

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    issues: list[str] = Field(
        default_factory=list
    )

    warnings: list[str] = Field(
        default_factory=list
    )

    attributes: dict[str, Any] = Field(
        default_factory=dict
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class RelationValidationResponse(BaseModel):
    """
    Complete relation validation response.
    """

    relations: list[RelationValidationResult] = Field(
        default_factory=list
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    notes: str | None = None