"""
Healthcare relation state.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Relation(BaseModel):
    """
    Represents a relationship between two healthcare entities.
    """

    relation_id: str

    source_entity_id: str

    target_entity_id: str

    relation_type: str

    confidence: float = 1.0

    attributes: dict[str, Any] = Field(
        default_factory=dict
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class RelationState(BaseModel):
    """
    Collection of extracted healthcare relations.
    """

    relations: list[Relation] = Field(
        default_factory=list
    )