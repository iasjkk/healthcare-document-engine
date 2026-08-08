"""
Prompt for Section Classification Agent.
"""

from __future__ import annotations

from framework.prompts.base_prompt import BasePrompt


class SectionClassificationPrompt(BasePrompt):
    """
    Builds prompts for document section classification.
    """

    def __init__(
        self,
        version: str = "1.0.0",
    ) -> None:

        super().__init__(
            name="section_classification",
            version=version,
        )

    def build(
        self,
        text: str,
        node_id: str,
        page_number: int,
        layout_type: str,
    ) -> str:
        """
        Build section classification prompt.
        """

        return f"""
You are an expert healthcare document
section classification system.

Classify the supplied document node into the
most appropriate semantic section.

--------------------------------------------------
SOURCE INFORMATION
--------------------------------------------------

Node ID:
{node_id}

Page Number:
{page_number}

Layout Type:
{layout_type}

--------------------------------------------------
TEXT
--------------------------------------------------

{text}

--------------------------------------------------
ALLOWED SECTION LABELS
--------------------------------------------------

Use one of the following labels whenever possible:

TITLE
PATIENT_INFORMATION
DEMOGRAPHICS
CHIEF_COMPLAINT
HISTORY_OF_PRESENT_ILLNESS
PAST_MEDICAL_HISTORY
PAST_SURGICAL_HISTORY
FAMILY_HISTORY
SOCIAL_HISTORY
MEDICATIONS
ALLERGIES
VITAL_SIGNS
PHYSICAL_EXAMINATION
LABORATORY_RESULTS
PATHOLOGY
IMAGING
RADIOLOGY
DIAGNOSIS
ASSESSMENT
PLAN
TREATMENT
PROCEDURE
SURGERY
GENETIC_TESTING
BIOMARKERS
ONCOLOGY
STAGING
FOLLOW_UP
DISCHARGE_SUMMARY
CLINICAL_NOTES
TABLE
REFERENCE
SIGNATURE
FOOTER
HEADER
OTHER

--------------------------------------------------
CLASSIFICATION RULES
--------------------------------------------------

1. Use the semantic meaning of the text.

2. Do not classify solely from the layout type.

3. A heading should normally be classified
   according to the section it introduces.

4. Medication-related content should be
   classified as MEDICATIONS.

5. Laboratory measurements should be
   classified as LABORATORY_RESULTS.

6. Pathology findings should be classified
   as PATHOLOGY.

7. Cancer staging information should be
   classified as STAGING.

8. Genetic mutations and molecular testing
   should normally be classified as
   GENETIC_TESTING or BIOMARKERS.

9. A table node containing structured table
   information should be classified as TABLE.

10. Do not invent clinical information.

11. Preserve the supplied node_id.

--------------------------------------------------
OUTPUT
--------------------------------------------------

Return ONLY valid JSON.

Return exactly:

{{
  "result": {{
    "node_id": "{node_id}",
    "section": "LABORATORY_RESULTS",
    "confidence": 0.98,
    "reasoning": "",
    "attributes": {{}}
  }},
  "confidence": 0.98,
  "notes": ""
}}
""".strip()