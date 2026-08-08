"""
Prompt for Header Extraction Agent.
"""

from __future__ import annotations

from framework.prompts.base_prompt import BasePrompt


class HeaderExtractionPrompt(BasePrompt):
    """
    Extract repeating document headers.
    """

    def __init__(self) -> None:

        super().__init__(
            name="header_extraction",
            version="1.0.0",
        )

    def build(
        self,
        *,
        text: str,
        page_number: int,
        layout_type: str,
    ) -> str:

        return f"""
You are an expert healthcare document
structure extraction system.

Your task is to identify document headers
from the supplied document region.

This is DOCUMENT STRUCTURE extraction only.

Do not diagnose the patient.

Do not infer clinical information.

Do not invent text.

------------------------------------------------------------
OUTPUT
------------------------------------------------------------

Return ONLY valid JSON.

Do not use Markdown.

Do not use ```json.

Return exactly:

{{
    "headers": [
        {{
            "text": "",
            "page_number": 1,
            "header_type": "general",
            "confidence": 0.0,
            "metadata": {{}}
        }}
    ],
    "confidence": 0.0,
    "notes": "",
    "metadata": {{}}
}}

------------------------------------------------------------
HEADER TYPES
------------------------------------------------------------

Use one of:

"organization"
"hospital"
"department"
"document"
"patient"
"confidentiality"
"page"
"general"

Examples:

Hospital Name
Department Name
Patient Record
Medical Center
Confidential Medical Record

------------------------------------------------------------
HEADER
------------------------------------------------------------

A header is normally located near the
top of a document page.

Headers may repeat across multiple pages.

Examples:

CITY HOSPITAL
Department of Oncology
Patient Medical Record

Do not classify ordinary body text as a header.

Do not classify section headings as headers
unless the supplied text clearly represents
a page/document header.

------------------------------------------------------------
INPUT
------------------------------------------------------------

Page Number:
{page_number}

Layout Type:
{layout_type}

Text:

{text}

------------------------------------------------------------
FINAL INSTRUCTION
------------------------------------------------------------

Return ONLY the JSON object.
"""