"""
Schema for Final Clinical Report Generation Agent.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class MedicationReport(BaseModel):
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


class BiomarkerReport(BaseModel):
    """
    Structured biomarker information.
    """

    name: str = ""

    result: str = ""

    status: str = ""

    value: str = ""

    unit: str = ""

    percentage: str = ""

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class FinalReportSection(BaseModel):
    """
    Represents one section of the final clinical report.
    """

    title: str = ""

    content: str = ""

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class FinalReportResponse(BaseModel):
    """
    Structured response returned by the Final Report Agent.
    """

    title: str = Field(
        default="Clinical Report"
    )

    summary: str = ""

    sections: list[FinalReportSection] = Field(
        default_factory=list
    )

    key_findings: list[str] = Field(
        default_factory=list
    )

    diagnoses: list[str] = Field(
        default_factory=list
    )

    medications: list[MedicationReport] = Field(
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

    biomarkers: list[BiomarkerReport] = Field(
        default_factory=list
    )

    procedures: list[str] = Field(
        default_factory=list
    )

    recommendations: list[str] = Field(
        default_factory=list
    )

    validation_status: str = Field(
        default="validated"
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