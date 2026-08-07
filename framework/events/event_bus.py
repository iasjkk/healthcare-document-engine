"""
framework.events.event_bus
==========================

Simple publish-subscribe event bus.

Components publish events without knowing who
is listening.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Callable

from framework.logging.models import EventType, LogEvent


class EventBus:
    """
    Publish-subscribe event bus.
    """

    def __init__(self) -> None:
        self._subscribers: dict[
            EventType,
            list[Callable[[LogEvent], None]]
        ] = defaultdict(list)

    def subscribe(
        self,
        event_type: EventType,
        callback: Callable[[LogEvent], None],
    ) -> None:
        """
        Register a callback for an event type.
        """
        self._subscribers[event_type].append(callback)

    def unsubscribe(
        self,
        event_type: EventType,
        callback: Callable[[LogEvent], None],
    ) -> None:
        """
        Remove a subscriber.
        """
        if callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)

    def publish(self, event: LogEvent) -> None:
        """
        Notify all subscribers.
        """
        for callback in self._subscribers.get(event.event_type, []):
            try:
                callback(event)
            except Exception as exc:
                print(f"Subscriber failed: {exc}")