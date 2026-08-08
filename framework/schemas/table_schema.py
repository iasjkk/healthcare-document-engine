"""
Schema for extracted tables.
"""

from pydantic import BaseModel, Field


class TableCell(BaseModel):

    value: str


class TableRow(BaseModel):

    cells: list[TableCell] = Field(
        default_factory=list
    )


class TableSchema(BaseModel):

    table_id: str

    headers: list[str] = Field(
        default_factory=list
    )

    rows: list[TableRow] = Field(
        default_factory=list
    )


class TableExtractionResponse(BaseModel):

    tables: list[TableSchema] = Field(
        default_factory=list
    )