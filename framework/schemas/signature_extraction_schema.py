"""
Schema for Signature Extraction.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SignatureItem(BaseModel):
    """Single extracted signature."""

    text: str = ""

    page_number: int = 1

    signature_type: str = "unknown"

    signer_role: str = ""

    signed: bool = True

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class SignatureExtractionResponse(BaseModel):
    """Structured signature extraction result."""

    signatures: list[SignatureItem] = Field(
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