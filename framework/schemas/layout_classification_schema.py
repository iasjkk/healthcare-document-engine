"""
Schema for Layout Classification Agent.

The model classifies ONE layout node at a time.

Input
-----
LayoutNode.text

Output
------
Heading
Paragraph
Table
Footer
...

This schema validates the LLM response.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# Supported Layout Classes
# ==========================================================

class LayoutClassification(str, Enum):

    HEADING = "Heading"

    SUBHEADING = "SubHeading"

    PARAGRAPH = "Paragraph"

    TABLE = "Table"

    BULLET_LIST = "BulletList"

    HEADER = "Header"

    FOOTER = "Footer"

    PAGE_NUMBER = "PageNumber"

    SIGNATURE = "Signature"

    ADDRESS = "Address"

    LAB_RESULT = "LaboratoryResult"

    MEDICATION = "Medication"

    DIAGNOSIS = "Diagnosis"

    OBSERVATION = "Observation"

    OTHER = "Other"


# ==========================================================
# Response Schema
# ==========================================================

class LayoutClassificationResponse(BaseModel):
    """
    Validated response from the LLM.
    """

    classification: LayoutClassification = Field(
        ...,
        description="Predicted layout class.",
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score.",
    )

    reason: str = Field(
        default="",
        description="Short explanation.",
    )