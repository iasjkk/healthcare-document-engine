"""
framework.logging.models
========================

This module defines all structured logging models used
throughout the framework.

This module should NEVER contain
business logic.

Responsibilities
----------------
- Log Levels
- Event Types
- Log Event Schema
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


# ------------------------------------------------------------------
# Log Levels
# ------------------------------------------------------------------

class LogLevel(str, Enum):
    """
    Logging severity levels.
    """

    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# ------------------------------------------------------------------
# Event Types
# ------------------------------------------------------------------

class EventType(str, Enum):
    """
    Types of events emitted by the framework.
    """

    WORKFLOW_STARTED = "WORKFLOW_STARTED"
    WORKFLOW_FINISHED = "WORKFLOW_FINISHED"

    NODE_STARTED = "NODE_STARTED"
    NODE_FINISHED = "NODE_FINISHED"

    AGENT_STARTED = "AGENT_STARTED"
    AGENT_FINISHED = "AGENT_FINISHED"

    MODEL_REQUEST = "MODEL_REQUEST"
    MODEL_RESPONSE = "MODEL_RESPONSE"

    VALIDATION_STARTED = "VALIDATION_STARTED"
    VALIDATION_FINISHED = "VALIDATION_FINISHED"

    CHECKPOINT_CREATED = "CHECKPOINT_CREATED"
    CHECKPOINT_RESTORED = "CHECKPOINT_RESTORED"

    RETRY = "RETRY"

    WARNING = "WARNING"
    ERROR = "ERROR"


# ------------------------------------------------------------------
# Log Event
# ------------------------------------------------------------------

class LogEvent(BaseModel):
    """
    Represents one structured log event.

    Every log produced by the framework will use this model.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    # --------------------------
    # Event Metadata
    # --------------------------

    event_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique Event ID",
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC Timestamp",
    )

    level: LogLevel

    event_type: EventType

    message: str

    # --------------------------
    # Workflow Metadata
    # --------------------------

    run_id: str | None = None

    workflow_id: str | None = None

    trace_id: str | None = None

    node_id: str | None = None

    parent_node: str | None = None

    # --------------------------
    # Source Information
    # --------------------------

    module: str | None = None

    function: str | None = None

    agent: str | None = None

    # --------------------------
    # Model Information
    # --------------------------

    provider: str | None = None

    model: str | None = None

    # --------------------------
    # Performance
    # --------------------------

    execution_time: float | None = None

    cpu_percent: float | None = None

    memory_mb: float | None = None

    # --------------------------
    # LLM Usage
    # --------------------------

    prompt_tokens: int | None = None

    completion_tokens: int |None = None

    total_tokens: int | None = None

    estimated_cost: float | None = None

    # --------------------------
    # Extra Metadata
    # --------------------------

    metadata: dict[str, Any] = Field(default_factory=dict)