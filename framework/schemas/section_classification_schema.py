"""
Schema for Section Classification Agent.

Classifies document layout nodes into meaningful
clinical/document sections.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SectionClassificationResult(BaseModel):
    """
    Classification result for one document node.
    """

    node_id: str

    section: str

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    reasoning: str = ""

    attributes: dict[str, Any] = Field(
        default_factory=dict
    )


class SectionClassificationResponse(BaseModel):
    """
    Structured response returned by the LLM.
    """

    result: SectionClassificationResult

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    notes: str = ""