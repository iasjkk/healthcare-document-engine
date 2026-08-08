"""
Schema for Chart/Graph Extraction.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChartDataPoint(BaseModel):
    """Single chart data point."""

    label: str = ""

    value: str = ""

    series: str = ""

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )


class ChartSeries(BaseModel):
    """Single chart data series."""

    name: str = ""

    values: list[ChartDataPoint] = Field(
        default_factory=list
    )


class ChartGraphItem(BaseModel):
    """Single extracted chart or graph."""

    chart_id: str = ""

    title: str = ""

    chart_type: str = "unknown"

    x_axis_label: str = ""

    y_axis_label: str = ""

    x_axis_unit: str = ""

    y_axis_unit: str = ""

    legend: list[str] = Field(
        default_factory=list
    )

    series: list[ChartSeries] = Field(
        default_factory=list
    )

    page_number: int = 1

    caption: str = ""

    description: str = ""

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class ChartGraphExtractionResponse(BaseModel):
    """Structured chart/graph extraction result."""

    charts: list[ChartGraphItem] = Field(
        default_factory=list
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    notes: str = ""

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )