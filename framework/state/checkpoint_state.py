"""
Checkpoint state.
"""

from pydantic import BaseModel


class CheckpointState(BaseModel):
    checkpoint_id: str

    timestamp: str

    stage: str