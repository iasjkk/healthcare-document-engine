from framework.prompts import (
    DocumentStructurePrompt,
    PromptRegistry,
)


def main():

    registry = PromptRegistry()


    prompt = DocumentStructurePrompt()


    registry.register(
        "document_structure",
        prompt,
    )


    generated_prompt = registry.get(
        "document_structure"
    ).build(
        document_content="""
        Patient Name: John Doe

        Diagnosis:
        Diabetes
        """
    )


    print(generated_prompt)



if __name__ == "__main__":
    main()