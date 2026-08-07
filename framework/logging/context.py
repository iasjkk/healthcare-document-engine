"""
framework.logging.context
=========================

Execution context for the logging framework.

This module stores execution-specific information that
is automatically attached to every log event.

The implementation uses Python's contextvars, making it
safe for:

- Threads
- AsyncIO
- LangGraph
- AutoGen
- FastAPI

No module should use global variables for execution state.
"""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class LoggingContext:
    """
    Stores metadata for the current workflow execution.
    """

    # ---------------------------------------------------------
    # Execution identifiers
    # ---------------------------------------------------------

    run_id: str = field(default_factory=lambda: str(uuid4()))

    workflow_id: str | None = None

    trace_id: str | None = None

    document_id: str | None = None

    session_id: str | None = None

    # ---------------------------------------------------------
    # Current execution state
    # ---------------------------------------------------------

    current_node: str | None = None

    current_agent: str | None = None

    current_model: str | None = None

    # ---------------------------------------------------------
    # User-defined metadata
    # ---------------------------------------------------------

    metadata: dict[str, Any] = field(default_factory=dict)


# -------------------------------------------------------------------------
# Context Variable
# -------------------------------------------------------------------------

_logging_context: ContextVar[LoggingContext] = ContextVar(
    "logging_context",
    default=LoggingContext(),
)


# -------------------------------------------------------------------------
# Public API
# -------------------------------------------------------------------------

def get_context() -> LoggingContext:
    """
    Return the current execution context.
    """
    return _logging_context.get()


def set_context(context: LoggingContext) -> None:
    """
    Replace the current execution context.
    """
    _logging_context.set(context)


def reset_context() -> LoggingContext:
    """
    Create a brand new execution context.

    Returns
    -------
    LoggingContext
        Newly created context.
    """

    context = LoggingContext()

    _logging_context.set(context)

    return context


def update_context(**kwargs) -> LoggingContext:
    """
    Update values in the current context.

    Unknown fields are automatically stored inside
    the metadata dictionary.

    Example
    -------
    update_context(
        workflow_id="workflow_001",
        current_node="Parser",
        current_agent="LayoutAgent",
    )
    """

    context = get_context()

    for key, value in kwargs.items():

        if hasattr(context, key):

            setattr(context, key, value)

        else:

            context.metadata[key] = value

    return context


def clear_metadata() -> None:
    """
    Remove all custom metadata while preserving
    workflow identifiers.
    """

    context = get_context()

    context.metadata.clear()