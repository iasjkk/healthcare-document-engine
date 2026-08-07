from framework.logging.models import (
    EventType,
    LogEvent,
    LogLevel,
)


def main():
    event = LogEvent(
        level=LogLevel.INFO,
        event_type=EventType.WORKFLOW_STARTED,
        message="Workflow execution started.",
    )

    print(event.model_dump_json(indent=2))


if __name__ == "__main__":
    main()