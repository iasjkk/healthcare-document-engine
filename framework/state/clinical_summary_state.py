"""
Clinical summary state.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class MedicationSummary(BaseModel):
    """
    Structured medication information.
    """

    name: str = ""

    dosage: str = ""

    frequency: str = ""

    route: str = ""

    status: str = ""

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class ClinicalSummaryState(BaseModel):
    """
    Stores the generated clinical summary.
    """

    summary: str = ""

    key_findings: list[str] = Field(
        default_factory=list
    )

    diagnoses: list[str] = Field(
        default_factory=list
    )

    medications: list[MedicationSummary] = Field(
        default_factory=list
    )

    allergies: list[str] = Field(
        default_factory=list
    )

    laboratory_findings: list[str] = Field(
        default_factory=list
    )

    pathology_findings: list[str] = Field(
        default_factory=list
    )

    biomarkers: list[str] = Field(
        default_factory=list
    )

    procedures: list[str] = Field(
        default_factory=list
    )

    recommendations: list[str] = Field(
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