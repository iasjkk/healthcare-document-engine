"""
Healthcare entity state.
"""

from typing import Any

from pydantic import BaseModel, Field


class Entity(BaseModel):
    entity_id: str

    entity_type: str

    value: str

    confidence: float = 1.0

    page_number: int | None = None

    source_node: str | None = None

    normalized_value: str | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


class EntityState(BaseModel):
    entities: list[Entity] = Field(default_factory=list)