"""
Layout hierarchy state.
"""

from __future__ import annotations

from pydantic import BaseModel, Field



class LayoutNode(BaseModel):
    """
    Single node in document layout tree.
    """

    node_id: str

    parent_id: str | None = None

    layout_type: str

    page_number: int

    text: str = ""

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