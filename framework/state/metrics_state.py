"""
Metrics state.
"""

from pydantic import BaseModel


class MetricsState(BaseModel):
    execution_time: float = 0.0

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    estimated_cost: float = 0.0