"""
Schema for Form Field Extraction.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class FormFieldItem(BaseModel):
    """Single extracted form field."""

    field_name: str = ""

    field_label: str = ""

    field_value: str = ""

    field_type: str = "text"

    page_number: int = 1

    required: bool = False

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class FormFieldExtractionResponse(BaseModel):
    """Structured form field extraction result."""

    fields: list[FormFieldItem] = Field(
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