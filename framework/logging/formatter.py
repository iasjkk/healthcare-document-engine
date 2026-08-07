"""
framework.logging.formatter
===========================

Formatting utilities for LogEvent.

This module is responsible ONLY for formatting.

It never writes files.
It never prints.
It never creates directories.

Those responsibilities belong to handlers.
"""

from __future__ import annotations

import json
from datetime import datetime

from framework.logging.models import LogEvent


class LogFormatter:
    """
    Converts LogEvent objects into different representations.
    """

    @staticmethod
    def format_json(event: LogEvent) -> dict:
        """
        Convert LogEvent into a JSON-serializable dictionary.
        """

        return event.model_dump(
            mode="json",
            exclude_none=True,
        )

    @staticmethod
    def format_json_string(
        event: LogEvent,
        indent: int | None = None,
    ) -> str:
        """
        Convert LogEvent into JSON string.
        """

        return json.dumps(
            LogFormatter.format_json(event),
            indent=indent,
            ensure_ascii=False,
        )

    @staticmethod
    def format_console(event: LogEvent) -> str:
        """
        Create a concise human-readable console message.
        """

        timestamp = datetime.fromisoformat(
            event.timestamp.isoformat()
        ).strftime("%H:%M:%S")

        module = event.module or "-"

        return (
            f"{timestamp} | "
            f"{event.level.value:<8} | "
            f"{module:<20} | "
            f"{event.message}"
        )