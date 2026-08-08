"""
Schemas for healthcare entity validation.

Defines the structured response expected from
EntityValidationAgent.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class EntityValidationResult(BaseModel):
    """
    Validation result for a single healthcare entity.
    """

    entity_id: str

    is_valid: bool

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    validation_status: str = "valid"

    issues: list[str] = Field(
        default_factory=list
    )

    warnings: list[str] = Field(
        default_factory=list
    )

    corrected_value: str | None = None

    corrected_entity_type: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class EntityValidationResponse(BaseModel):
    """
    Complete validation response from the LLM.
    """

    entities: list[EntityValidationResult] = Field(
        default_factory=list
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    notes: str | None = None