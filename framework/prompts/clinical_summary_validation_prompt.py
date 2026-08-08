"""
Prompt for Clinical Summary Validation Agent.
"""

from __future__ import annotations

import json
from typing import Any

from framework.prompts.base_prompt import BasePrompt


class ClinicalSummaryValidationPrompt(BasePrompt):
    """
    Builds prompts for validating a generated
    clinical summary against source information.
    """

    def __init__(
        self,
        version: str = "1.0.0",
    ) -> None:

        super().__init__(
            name="clinical_summary_validation",
            version=version,
        )

    def build(
        self,
        source_data: dict[str, Any],
        clinical_summary: dict[str, Any],
    ) -> str:
        """
        Build the validation prompt.
        """

        source_json = json.dumps(
            source_data,
            indent=2,
            ensure_ascii=False,
        )

        summary_json = json.dumps(
            clinical_summary,
            indent=2,
            ensure_ascii=False,
        )

        return f"""
You are an expert healthcare clinical
information validation system.

Your task is to validate a generated clinical
summary against the supplied source clinical
information.

The generated summary MUST be checked for
factual consistency, completeness, unsupported
claims, contradictions, and structural consistency.

--------------------------------------------------
SOURCE CLINICAL INFORMATION
--------------------------------------------------

{source_json}

--------------------------------------------------
GENERATED CLINICAL SUMMARY
--------------------------------------------------

{summary_json}

--------------------------------------------------
VALIDATION OBJECTIVE
--------------------------------------------------

Determine whether the generated clinical summary
is supported by the source information.

Do NOT rewrite the clinical summary.

Do NOT improve the clinical summary.

Do NOT add medical advice.

Only identify validation issues.

--------------------------------------------------
VALIDATION RULES
--------------------------------------------------

1. SOURCE GROUNDING

Every clinically meaningful claim in the summary
must be supported by the source information.

Flag information that cannot be found in the source.

--------------------------------------------------
2. HALLUCINATION

Flag:

- invented diagnoses
- invented medications
- invented symptoms
- invented laboratory findings
- invented pathology findings
- invented biomarkers
- invented procedures
- invented recommendations
- unsupported clinical conclusions

--------------------------------------------------
3. NEGATION

Verify that explicit negations are preserved.

For example:

Source:
"No evidence of metastasis."

Generated:
"Metastasis present."

This MUST be reported as an error.

--------------------------------------------------
4. UNCERTAINTY

Verify that uncertainty is preserved.

For example:

Source:
"Possible pneumonia."

Generated:
"Pneumonia confirmed."

This MUST be reported as an error.

--------------------------------------------------
5. MEDICATION VALIDATION

Validate:

- medication name
- dosage
- frequency
- route
- status

Do not require a medication attribute when
that attribute is absent from the source.

Flag medication information that contradicts
the source.

--------------------------------------------------
6. DIAGNOSIS VALIDATION

Every diagnosis must be supported by the source.

Do not treat symptoms, biomarkers, or laboratory
findings as diagnoses unless the source explicitly
does so.

--------------------------------------------------
7. LABORATORY VALIDATION

Check:

- test name
- value
- unit
- abnormality
- qualifiers

Do not require a reference range unless the
source contains one.

--------------------------------------------------
8. PATHOLOGY VALIDATION

Check:

- specimen
- pathology diagnosis
- histology
- grade
- stage
- biomarker results
- molecular findings

Do not infer missing pathology information.

--------------------------------------------------
9. BIOMARKER VALIDATION

Check that:

- biomarker name is correct
- result is correct
- positive/negative status is preserved
- percentages or measurements are preserved

Do not infer treatment recommendations.

--------------------------------------------------
10. GENETIC FINDINGS

Check:

- gene names
- mutation names
- variants
- mutation status
- detected/not detected status

Do not infer pathogenicity unless explicitly
present in the source.

--------------------------------------------------
11. PROCEDURES

Verify that every procedure mentioned in the
summary exists in the source.

--------------------------------------------------
12. RECOMMENDATIONS

Recommendations must be explicitly supported
by the source.

Flag newly generated medical advice.

--------------------------------------------------
13. CONTRADICTIONS

Identify contradictions between source and
generated summary.

Examples:

Source:
"HER2 negative."

Generated:
"HER2 positive."

Source:
"No known allergies."

Generated:
"Penicillin allergy."

--------------------------------------------------
14. OMISSIONS

Only flag an omission when the missing information
is clinically important and explicitly present
in the source.

Do not flag every minor omission.

--------------------------------------------------
15. DUPLICATES

Do not consider harmless duplication a serious
validation error.

--------------------------------------------------
16. SEVERITY

Use:

"info"
    Minor observation that does not affect
    clinical correctness.

"warning"
    Potential issue that should be reviewed.

"error"
    Factual or structural problem.

"critical"
    Serious clinical contradiction,
    hallucination, or dangerous misinformation.

--------------------------------------------------
17. CONFIDENCE

Return a confidence value between 0.0 and 1.0.

--------------------------------------------------
OUTPUT FORMAT
--------------------------------------------------

Return ONLY valid JSON.

Do not return Markdown.

Do not return explanations outside JSON.

Use exactly this structure:

{{
    "valid": true,

    "issues": [
        {{
            "code": "",
            "message": "",
            "severity": "warning",
            "field": "",
            "source_text": "",
            "generated_text": "",
            "metadata": {{}}
        }}
    ],

    "confidence": 0.95,

    "notes": "",

    "metadata": {{}}
}}

--------------------------------------------------
IMPORTANT
--------------------------------------------------

If there are no validation issues:

{{
    "valid": true,
    "issues": [],
    "confidence": 1.0,
    "notes": "No validation issues identified.",
    "metadata": {{}}
}}

If there is at least one error or critical issue,
"valid" MUST be false.

Warnings and informational observations may
still allow "valid" to be true.

Return ONLY the JSON object.
""".strip()