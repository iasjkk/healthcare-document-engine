from framework.events.event_bus import EventBus
from framework.logging.models import (
    EventType,
    LogEvent,
    LogLevel,
)


def logger(event):
    print(f"[LOGGER] {event.message}")


def metrics(event):
    print(f"[METRICS] {event.level}")


def main():

    bus = EventBus()

    bus.subscribe(
        EventType.WORKFLOW_STARTED,
        logger,
    )

    bus.subscribe(
        EventType.WORKFLOW_STARTED,
        metrics,
    )

    event = LogEvent(
        level=LogLevel.INFO,
        event_type=EventType.WORKFLOW_STARTED,
        message="Workflow Started",
    )

    bus.publish(event)


if __name__ == "__main__":
    main()