"""
Schema for validation results.
"""

from pydantic import BaseModel, Field


class ValidationIssue(BaseModel):

    severity: str

    message: str

    location: str | None = None


class ValidationResponse(BaseModel):

    valid: bool = True

    issues: list[ValidationIssue] = Field(
        default_factory=list
    )