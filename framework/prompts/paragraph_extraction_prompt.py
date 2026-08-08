"""
Prompt for Paragraph Extraction Agent.

The agent receives one layout node that has already been
classified as a paragraph and produces a clean, structured
representation while preserving the original clinical
information.
"""

from __future__ import annotations

from framework.prompts.base_prompt import BasePrompt


class ParagraphExtractionPrompt(BasePrompt):
    """
    Prompt for extracting and structuring paragraph content.
    """

    def __init__(self) -> None:
        super().__init__(
            name="paragraph_extraction",
            version="1.0.0",
        )

    def build(
        self,
        *,
        text: str,
        page_number: int,
        layout_type: str,
    ) -> str:
        """
        Build the paragraph extraction prompt.
        """

        return f"""
You are an expert healthcare document processing system.

Your task is to process ONE paragraph from a healthcare
document.

The paragraph may come from:

- Clinical notes
- Pathology reports
- Laboratory reports
- Radiology reports
- Discharge summaries
- Operative reports
- Medical histories
- Consultation notes
- Prescription documents
- Insurance documents
- Healthcare forms

Your job is to clean and structure the paragraph while
preserving the information exactly.

------------------------------------------------------------
IMPORTANT
------------------------------------------------------------

Return ONLY valid JSON.

Do NOT return Markdown.

Do NOT use ```json.

Do NOT provide explanations outside the JSON object.

The response must follow this structure:

{{
    "text": "",
    "original_text": "",
    "paragraph_type": "general",
    "confidence": 0.0,
    "notes": "",
    "metadata": {{}}
}}

------------------------------------------------------------
TEXT PRESERVATION RULES
------------------------------------------------------------

1. Preserve all clinically relevant information.

2. Do NOT invent information.

3. Do NOT remove clinically meaningful details.

4. Do NOT diagnose the patient.

5. Do NOT add medical interpretation.

6. Do NOT change laboratory values.

7. Do NOT change numerical values.

8. Do NOT change dates.

9. Do NOT change medication doses.

10. Do NOT change units.

11. Do NOT change anatomical terminology.

12. Do NOT change disease names.

13. Do NOT change test names.

14. Do NOT change patient identifiers.

15. Do NOT infer missing information.

------------------------------------------------------------
OCR CLEANING
------------------------------------------------------------

You may correct obvious OCR errors when the intended text
is unambiguous.

Examples:

"Patlent" → "Patient"

"hemoglobln" → "hemoglobin"

"medicatlon" → "medication"

However, do NOT make corrections when the intended value
is uncertain.

For example:

"13.2" must remain "13.2".

"7.5 mg/dL" must remain "7.5 mg/dL".

------------------------------------------------------------
WHITESPACE
------------------------------------------------------------

You may:

- Remove repeated spaces.
- Remove unnecessary line breaks.
- Join words incorrectly split by OCR.
- Normalize obvious whitespace problems.

Do not remove meaningful formatting such as:

- bullet points
- numbered items
- section labels
- medication lists
- dates
- measurements

------------------------------------------------------------
PARAGRAPH TYPE
------------------------------------------------------------

Identify the broad structural/semantic type of the paragraph.

Possible values include:

- "history"
- "clinical_note"
- "diagnosis"
- "symptoms"
- "medication"
- "procedure"
- "laboratory"
- "radiology"
- "pathology"
- "assessment"
- "plan"
- "discharge_summary"
- "general"

Use "general" when the type cannot be determined safely.

Do not make a clinical diagnosis based on the paragraph.

------------------------------------------------------------
ORIGINAL TEXT
------------------------------------------------------------

The "original_text" field MUST contain the paragraph exactly
as supplied to you.

Do not clean or modify this field.

The "text" field contains the cleaned version.

Example:

{{
    "text": "Patient complains of chest pain for 3 days.",
    "original_text": "Patient c/o chest pain x 3 days.",
    "paragraph_type": "clinical_note",
    "confidence": 0.96,
    "notes": "",
    "metadata": {{}}
}}

------------------------------------------------------------
AMBIGUOUS OCR
------------------------------------------------------------

If OCR is severely damaged, preserve the uncertain content
instead of inventing a correction.

Example:

Input:

"Patient has diab??tes"

Possible output:

{{
    "text": "Patient has diab??tes",
    "original_text": "Patient has diab??tes",
    "paragraph_type": "general",
    "confidence": 0.55,
    "notes": "OCR ambiguity in disease name.",
    "metadata": {{}}
}}

------------------------------------------------------------
HEALTHCARE SAFETY
------------------------------------------------------------

This task is document processing only.

Do not:

- diagnose
- recommend treatment
- recommend medication
- interpret laboratory results
- infer disease severity
- infer patient outcomes

Only extract and clean the supplied document content.

------------------------------------------------------------
INPUT INFORMATION
------------------------------------------------------------

Page Number:
{page_number}

Layout Type:
{layout_type}

Paragraph:

{text}

------------------------------------------------------------
FINAL INSTRUCTION
------------------------------------------------------------

Return ONLY the JSON object.

No Markdown.
No commentary.
No additional text.
"""