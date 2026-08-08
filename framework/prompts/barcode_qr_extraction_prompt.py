"""
Prompt for Barcode / QR Extraction Agent.
"""

from __future__ import annotations

from framework.prompts.base_prompt import BasePrompt


class BarcodeQRExtractionPrompt(BasePrompt):
    """
    Extract and normalize barcode / QR information.
    """

    def __init__(self) -> None:

        super().__init__(
            name="barcode_qr_extraction",
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
structured-data extraction system.

Your task is to identify barcode and QR-code
information from the supplied document text.

This is NOT a medical interpretation task.

Do not diagnose the patient.

Do not invent barcode values.

Only return a barcode or QR value if it is
explicitly present in the supplied information.

------------------------------------------------------------
OUTPUT
------------------------------------------------------------

Return ONLY valid JSON.

Do not use Markdown.

Do not use ```json.

Return exactly:

{{
    "codes": [
        {{
            "code_id": "",
            "code_type": "unknown",
            "value": "",
            "format": "",
            "page_number": 1,
            "context": "",
            "is_valid": false,
            "confidence": 0.0,
            "metadata": {{}}
        }}
    ],
    "confidence": 0.0,
    "notes": "",
    "metadata": {{}}
}}

------------------------------------------------------------
CODE TYPES
------------------------------------------------------------

Use one of:

"qr"
"barcode"
"unknown"

------------------------------------------------------------
BARCODE FORMATS
------------------------------------------------------------

Possible formats include:

"QR_CODE"
"CODE128"
"CODE39"
"EAN13"
"EAN8"
"UPC_A"
"UPC_E"
"ITF"
"DATA_MATRIX"
"PDF417"
"AZTEC"
"UNKNOWN"

Only assign a specific format when the input
provides sufficient evidence.

------------------------------------------------------------
VALUE
------------------------------------------------------------

The value must be copied exactly from the
supplied information.

Do not:

- invent missing characters
- correct characters
- alter capitalization
- remove leading zeros
- add prefixes
- infer missing digits

Example:

Input:

QR: https://example.com/patient/12345

Return:

"value": "https://example.com/patient/12345"

------------------------------------------------------------
VALIDATION
------------------------------------------------------------

Set:

"is_valid": true

only when the supplied value can reasonably
be identified as a complete code value.

Do NOT perform checksum validation unless
the necessary information is explicitly available.

If the code is incomplete or uncertain:

"is_valid": false

------------------------------------------------------------
CONTEXT
------------------------------------------------------------

Extract nearby contextual information when
available.

Examples:

"Patient identification label"

"Specimen tracking label"

"Laboratory accession number"

"Medication package"

"Insurance card"

Do not infer context that is not supported
by the supplied text.

------------------------------------------------------------
HEALTHCARE IDENTIFIERS
------------------------------------------------------------

A barcode or QR code may contain:

- patient identifier
- specimen identifier
- accession number
- laboratory identifier
- medication identifier
- prescription identifier
- insurance identifier
- document identifier

Do not expose or invent sensitive information
beyond what is explicitly provided.

------------------------------------------------------------
IMPORTANT
------------------------------------------------------------

If the input contains no identifiable
barcode or QR information, return:

{{
    "codes": [],
    "confidence": 1.0,
    "notes": "No barcode or QR code information identified.",
    "metadata": {{}}
}}

------------------------------------------------------------
INPUT
------------------------------------------------------------

Page Number:
{page_number}

Layout Type:
{layout_type}

Associated OCR/Text:

{text}

------------------------------------------------------------
FINAL INSTRUCTION
------------------------------------------------------------

Return ONLY the JSON object.
"""