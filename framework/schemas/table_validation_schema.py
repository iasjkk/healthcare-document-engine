"""
Schema for Table Validation Agent.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TableValidationResult(BaseModel):
    """
    Validation result for one extracted table.
    """

    table_id: str

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


class TableValidationResponse(BaseModel):
    """
    Structured response returned by the LLM.
    """

    result: TableValidationResult

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    notes: str = ""