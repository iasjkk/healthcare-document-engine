"""
Schema for document structure extraction.
"""

from pydantic import BaseModel, Field


class SectionSchema(BaseModel):
    """
    Single detected section.
    """

    type: str

    page_number: int

    text: str


class DocumentStructureResponse(BaseModel):
    """
    Output from DocumentStructureAgent.
    """

    sections: list[SectionSchema] = Field(
        default_factory=list
    )