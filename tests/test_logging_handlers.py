from framework.logging.handlers import HandlerManager
from framework.logging.models import (
    EventType,
    LogEvent,
    LogLevel,
)


def main():

    manager = HandlerManager()

    event = LogEvent(
        level=LogLevel.INFO,
        event_type=EventType.WORKFLOW_STARTED,
        message="Healthcare workflow started",
        module="WorkflowEngine",
    )

    manager.emit(event)

    manager.close()

    print("\nRun directory:")

    print(manager.run_path)


if __name__ == "__main__":
    main()