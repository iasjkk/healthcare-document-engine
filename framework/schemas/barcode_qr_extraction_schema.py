"""
Schema for Barcode / QR Extraction.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class BarcodeQRItem(BaseModel):
    """Single detected barcode or QR code."""

    code_id: str = ""

    code_type: str = "unknown"

    value: str = ""

    format: str = ""

    page_number: int = 1

    context: str = ""

    is_valid: bool = False

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class BarcodeQRExtractionResponse(BaseModel):
    """Structured barcode/QR extraction result."""

    codes: list[BarcodeQRItem] = Field(
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