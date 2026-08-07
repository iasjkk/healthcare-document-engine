from framework.logging.formatter import LogFormatter
from framework.logging.models import (
    EventType,
    LogEvent,
    LogLevel,
)


def main():

    event = LogEvent(
        level=LogLevel.INFO,
        event_type=EventType.NODE_STARTED,
        message="Document Parser Started",
        module="DocumentParser",
        workflow_id="workflow_001",
        node_id="parser",
    )

    print("\nJSON Dictionary\n")

    print(LogFormatter.format_json(event))

    print("\nJSON String\n")

    print(LogFormatter.format_json_string(event, indent=2))

    print("\nConsole\n")

    print(LogFormatter.format_console(event))


if __name__ == "__main__":
    main()