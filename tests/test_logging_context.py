from framework.logging.context import (
    clear_metadata,
    get_context,
    reset_context,
    update_context,
)


def main():

    print("\nCreating new execution context...\n")

    ctx = reset_context()

    print(ctx)

    print("\nUpdating context...\n")

    update_context(
        workflow_id="workflow_001",
        document_id="patient_123.docx",
        current_node="DocumentParser",
        current_agent="ParserAgent",
        current_model="Gemma-3",
        custom_value="Hello World",
    )

    print(get_context())

    print("\nClearing metadata...\n")

    clear_metadata()

    print(get_context())


if __name__ == "__main__":
    main()