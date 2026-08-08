"""
Standard execution result returned by every framework agent.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from framework.state.workflow_state import WorkflowState


class AgentResult(BaseModel):
    """
    Standard result returned by every agent.

    This object contains both the updated workflow state and
    execution metadata.
    """

    # ---------------------------------------------------------
    # Execution Status
    # ---------------------------------------------------------

    success: bool = True

    message: str = ""

    warnings: list[str] = Field(default_factory=list)

    errors: list[str] = Field(default_factory=list)

    # ---------------------------------------------------------
    # Updated Workflow
    # ---------------------------------------------------------

    state: WorkflowState

    # ---------------------------------------------------------
    # Execution Metrics
    # ---------------------------------------------------------

    started_at: datetime | None = None

    finished_at: datetime | None = None

    execution_time: float = 0.0

    # ---------------------------------------------------------
    # LLM Usage
    # ---------------------------------------------------------

    provider: str = ""

    model: str = ""

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    cost: float = 0.0

    # ---------------------------------------------------------
    # Optional Data
    # ---------------------------------------------------------

    metadata: dict[str, Any] = Field(default_factory=dict)

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0