"""
Validation state.
"""

from pydantic import BaseModel, Field


class ValidationIssue(BaseModel):
    code: str

    message: str

    severity: str


class ValidationState(BaseModel):
    issues: list[ValidationIssue] = Field(default_factory=list)