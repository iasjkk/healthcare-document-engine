"""
Prompt for document structure analysis.
"""

from framework.prompts.base_prompt import BasePrompt


class DocumentStructurePrompt(BasePrompt):
    """
    Analyze healthcare document structure.

    Used by:
    DocumentStructureAgent
    """


    def __init__(self):

        super().__init__(
            name="document_structure",
            version="1.0.0",
        )


    def build(
        self,
        document_content: str,
    ) -> str:


        return f"""
You are an expert healthcare document
understanding AI system.

Your task is to analyze the structure
of the healthcare document provided below.

Identify:

1. Document metadata
2. Document title
3. Sections
4. Subsections
5. Paragraph hierarchy
6. Tables
7. Bullet lists
8. Numbered lists
9. Forms
10. Page boundaries
11. Reading order


Rules:

- Preserve the original hierarchy.
- Do not summarize.
- Do not remove information.
- Maintain page references.
- Return only valid JSON.

Expected JSON format:

{{
    "document_metadata": {{}},

    "sections": [],

    "layout_elements": [],

    "pages": []
}}


Healthcare Document:

-----------------------

{document_content}

-----------------------
"""