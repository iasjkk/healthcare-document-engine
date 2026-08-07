"""
Workflow execution state.
"""

from pydantic import BaseModel


class ExecutionState(BaseModel):
    run_id: str

    workflow_id: str

    current_agent: str | None = None

    current_node: str | None = None

    current_model: str | None = None

    retry_count: int = 0