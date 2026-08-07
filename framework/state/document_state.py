"""
Document state models.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PageState(BaseModel):
    page_number: int
    content: str = ""
    sections: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentState(BaseModel):
    document_id: str
    file_name: str
    file_path: str
    file_type: str

    pages: list[PageState] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)