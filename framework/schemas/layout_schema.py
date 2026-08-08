"""
Schema for layout classification.
"""

from pydantic import BaseModel, Field


class LayoutClassification(BaseModel):

    node_id: str

    layout_type: str

    confidence: float = 1.0


class LayoutClassificationResponse(BaseModel):

    nodes: list[LayoutClassification] = Field(
        default_factory=list
    )