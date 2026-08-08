"""
Schema for Table Extraction Agent.

The Table Extraction Agent receives one layout node
classified as a Table and converts its text into a
structured representation.

The schema is intentionally generic because healthcare
documents contain many different table structures.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TableCell(BaseModel):
    """
    Represents one cell in an extracted table.
    """

    row: int = Field(
        ...,
        ge=0,
        description="Zero-based row index.",
    )

    column: int = Field(
        ...,
        ge=0,
        description="Zero-based column index.",
    )

    value: str = Field(
        default="",
        description="Cell text.",
    )


class TableExtractionResponse(BaseModel):
    """
    Structured response returned by the LLM.
    """

    headers: list[str] = Field(
        default_factory=list,
        description="Table column headers.",
    )

    rows: list[list[str]] = Field(
        default_factory=list,
        description="Extracted table rows.",
    )

    cells: list[TableCell] = Field(
        default_factory=list,
        description="Optional cell-level representation.",
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
        description="Additional extraction metadata.",
    )
