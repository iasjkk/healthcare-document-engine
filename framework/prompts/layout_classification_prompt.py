"""
Prompt for Layout Classification Agent.

The model classifies ONE layout node.

Input
-----
A single LayoutNode.

Output
------
Strict JSON matching LayoutClassificationResponse.
"""

from __future__ import annotations

from framework.prompts.base_prompt import BasePrompt


class LayoutClassificationPrompt(BasePrompt):
    """
    Prompt for classifying one layout node.
    """

    def __init__(self) -> None:

        super().__init__(
            name="layout_classification",
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
You are an expert Healthcare Document Layout Analyzer.

Your task is to classify ONE document block.

----------------------------------------
Available Classes
----------------------------------------

Heading
SubHeading
Paragraph
Table
BulletList
Header
Footer
PageNumber
Signature
Address
LaboratoryResult
Medication
Diagnosis
Observation
Other

----------------------------------------
Guidelines
----------------------------------------

Heading
- Large section titles
- Examples:
  "Diagnosis"
  "Medication"
  "Clinical History"

SubHeading
- Smaller title below heading
- Usually introduces subsection

Paragraph
- Continuous narrative text
- Sentences
- Clinical notes

Table
- Rows
- Columns
- Laboratory values
- Test result grids

BulletList
- Multiple bullet points
- Lists

Header
- Hospital information
- Logo area
- Document title

Footer
- Copyright
- Confidentiality
- Contact information

PageNumber
- Isolated page numbers

Signature
- Doctor signature
- Physician name
- Sign area

Address
- Hospital address
- Contact information

LaboratoryResult
- Individual lab result
- Usually:
    Hemoglobin 13.2
    WBC 7.1

Medication
- Drug names
- Prescriptions
- Dosage

Diagnosis
- Diagnosis statements

Observation
- Clinical observations

Other
- Anything that doesn't fit above

----------------------------------------
Rules
----------------------------------------

Return ONLY JSON.

Do NOT explain.

Do NOT use markdown.

Do NOT wrap inside ```.

JSON format:

{{
    "classification":"Heading",
    "confidence":0.98,
    "reason":"Short reason"
}}

----------------------------------------
Node Information
----------------------------------------

Page Number:

{page_number}

Detected Layout Type:

{layout_type}

Node Text:

{text}
"""