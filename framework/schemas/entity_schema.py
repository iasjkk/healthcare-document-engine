"""
Schema for clinical entity extraction.
"""

from pydantic import BaseModel, Field


class ClinicalEntity(BaseModel):

    entity_type: str

    text: str

    normalized_value: str | None = None

    confidence: float = 1.0

    page_number: int | None = None


class EntityExtractionResponse(BaseModel):

    entities: list[ClinicalEntity] = Field(
        default_factory=list
    )