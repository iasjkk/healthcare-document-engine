"""
Schema for Clinical Summary Agent.
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


class ClinicalSummaryResponse(BaseModel):
    """
    Structured response returned by the
    Clinical Summary Agent.
    """

    summary: str = Field(
        default="",
        description="Concise clinical summary.",
    )

    key_findings: list[str] = Field(
        default_factory=list,
        description="Important clinical findings.",
    )

    diagnoses: list[str] = Field(
        default_factory=list,
        description="Identified diagnoses.",
    )

    medications: list[MedicationSummary] = Field(
        default_factory=list,
        description="Structured medication information.",
    )

    allergies: list[str] = Field(
        default_factory=list,
        description="Documented allergies.",
    )

    laboratory_findings: list[str] = Field(
        default_factory=list,
        description="Important laboratory findings.",
    )

    pathology_findings: list[str] = Field(
        default_factory=list,
        description="Important pathology findings.",
    )

    biomarkers: list[str] = Field(
        default_factory=list,
        description="Important biomarker findings.",
    )

    procedures: list[str] = Field(
        default_factory=list,
        description="Relevant procedures.",
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="Explicit recommendations from source.",
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