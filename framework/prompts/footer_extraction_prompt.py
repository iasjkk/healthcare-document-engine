"""
Prompt for Footer Extraction Agent.
"""

from __future__ import annotations

from framework.prompts.base_prompt import BasePrompt


class FooterExtractionPrompt(BasePrompt):
    """
    Extract document footers.
    """

    def __init__(self) -> None:

        super().__init__(
            name="footer_extraction",
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

Your task is to identify document footers
from the supplied document region.

This is DOCUMENT STRUCTURE extraction only.

Do not diagnose the patient.

Do not interpret clinical information.

Do not invent missing information.

------------------------------------------------------------
OUTPUT
------------------------------------------------------------

Return ONLY valid JSON.

Do not use Markdown.

Do not use ```json.

Return exactly:

{{
    "footers": [
        {{
            "text": "",
            "page_number": 1,
            "footer_type": "general",
            "confidence": 0.0,
            "metadata": {{}}
        }}
    ],
    "confidence": 0.0,
    "notes": "",
    "metadata": {{}}
}}

------------------------------------------------------------
FOOTER TYPES
------------------------------------------------------------

Use one of:

"page_number"
"copyright"
"confidentiality"
"organization"
"contact"
"date"
"document_identifier"
"general"

Examples:

Page 1 of 5
Confidential Medical Record
© 2026 City General Hospital
Medical Record No. MRN-12345

------------------------------------------------------------
FOOTER
------------------------------------------------------------

A footer is normally located near the
bottom of a document page.

Footers may repeat across multiple pages.

Do not classify ordinary body text as a footer.

Do not classify a section heading as a footer.

Do not treat the last paragraph of a document
as a footer merely because it appears last.

------------------------------------------------------------
PAGE NUMBERS
------------------------------------------------------------

Preserve page-number information exactly
when available.

Examples:

Page 1 of 5

1 / 5

Page 2

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