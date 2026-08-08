"""
Layout hierarchy state.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from typing import Any

class LayoutNode(BaseModel):
    """
    Single node in document layout tree.
    """

    node_id: str

    parent_id: str | None = None

    layout_type: str

    page_number: int

    text: str = ""

    classification: str | None = None

    confidence: float | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

    children: list["LayoutNode"] = Field(
        default_factory=list
    )



class LayoutState(BaseModel):
    """
    Document layout understanding state.
    """

    nodes: list[LayoutNode] = Field(
        default_factory=list
    )


LayoutNode.model_rebuild()