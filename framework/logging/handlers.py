"""
framework.logging.handlers
==========================

Logging handlers responsible for writing LogEvents
to different destinations.

Current handlers:
- ConsoleHandler
- JsonFileHandler

Future handlers:
- PromptHandler
- ResponseHandler
- MetricsHandler
- LangSmithHandler
- OpenTelemetryHandler
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from framework.logging.formatter import LogFormatter
from framework.logging.models import LogEvent


# ==========================================================
# Base Handler
# ==========================================================

class BaseHandler(ABC):
    """
    Abstract base class for all handlers.
    """

    @abstractmethod
    def emit(self, event: LogEvent) -> None:
        """Write a log event."""
        pass

    def close(self) -> None:
        """Optional cleanup."""
        pass


# ==========================================================
# Console Handler
# ==========================================================

class ConsoleHandler(BaseHandler):
    """
    Writes logs to the console.
    """

    def emit(self, event: LogEvent) -> None:
        print(LogFormatter.format_console(event))


# ==========================================================
# JSON File Handler
# ==========================================================

class JsonFileHandler(BaseHandler):
    """
    Writes structured logs to execution.jsonl
    """

    def __init__(self, run_directory: Path):

        self.run_directory = run_directory

        self.run_directory.mkdir(parents=True, exist_ok=True)

        self.file = open(
            self.run_directory / "execution.jsonl",
            "a",
            encoding="utf-8",
        )

    def emit(self, event: LogEvent) -> None:

        self.file.write(
            LogFormatter.format_json_string(event)
        )

        self.file.write("\n")

        self.file.flush()

    def close(self) -> None:

        self.file.close()


# ==========================================================
# Handler Manager
# ==========================================================

class HandlerManager:
    """
    Dispatches events to all registered handlers.
    """

    def __init__(self):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        run_id = uuid4().hex[:8]

        self.run_directory = (
            Path("artifacts")
            / "runs"
            / f"{timestamp}_{run_id}"
        )

        self.handlers: list[BaseHandler] = [
            ConsoleHandler(),
            JsonFileHandler(self.run_directory),
        ]

    @property
    def run_path(self) -> Path:
        return self.run_directory

    def emit(self, event: LogEvent):

        for handler in self.handlers:

            handler.emit(event)

    def close(self):

        for handler in self.handlers:

            handler.close()