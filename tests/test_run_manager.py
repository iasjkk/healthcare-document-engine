from framework.runtime.run_manager import RunManager


def main():

    with RunManager(
        workflow_name="Healthcare Workflow"
    ) as run:

        print("Run ID:")
        print(run.run_id)

        print()

        print("Run Directory:")
        print(run.run_directory)

        print()

        print("Prompt Path:")
        print(run.get_path("prompts"))

        print()

        print("Response Path:")
        print(run.get_path("responses"))


if __name__ == "__main__":
    main()