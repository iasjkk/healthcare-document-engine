"""
Schema for Clinical Summary Validation Agent.

The Clinical Summary Validation Agent checks the generated
clinical summary against the source clinical information.

It does not modify the clinical summary directly.

Validation issues are later written into ValidationState.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ClinicalSummaryValidationIssue(BaseModel):
    """
    Represents one validation issue identified by the LLM.
    """

    code: str = Field(
        default="",
        description="Machine-readable validation issue code.",
    )

    message: str = Field(
        default="",
        description="Human-readable validation issue.",
    )

    severity: str = Field(
        default="warning",
        description=(
            "Issue severity. Expected values include "
            "info, warning, error, critical."
        ),
    )

    field: str = Field(
        default="",
        description=(
            "Clinical summary field associated with "
            "the issue."
        ),
    )

    source_text: str = Field(
        default="",
        description=(
            "Relevant source information supporting "
            "the validation result."
        ),
    )

    generated_text: str = Field(
        default="",
        description=(
            "Relevant generated summary information "
            "associated with the issue."
        ),
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional validation metadata.",
    )


class ClinicalSummaryValidationResponse(BaseModel):
    """
    Structured response returned by the Clinical
    Summary Validation Agent.
    """

    valid: bool = Field(
        default=True,
        description=(
            "Whether the generated clinical summary "
            "passed validation."
        ),
    )

    issues: list[ClinicalSummaryValidationIssue] = Field(
        default_factory=list,
        description="Validation issues.",
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Overall validation confidence.",
    )

    notes: str = Field(
        default="",
        description="Validation notes.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional validation metadata.",
    )