"""
Prompt for healthcare entity extraction.
"""

from __future__ import annotations

from framework.prompts.base_prompt import BasePrompt


class EntityExtractionPrompt(BasePrompt):
    """
    Extract healthcare entities from document text.
    """

    def __init__(self) -> None:

        super().__init__(
            name="entity_extraction",
            version="1.0.0",
        )

    def build(
        self,
        *,
        text: str,
        page_number: int,
        node_id: str,
        layout_type: str,
    ) -> str:

        return f"""
You are an expert healthcare document
information extraction system.

Your task is to extract explicitly stated
healthcare entities from the supplied text.

This is ENTITY EXTRACTION only.

Do not diagnose the patient.

Do not infer information that is not explicitly
present.

Do not invent missing values.

Do not provide medical recommendations.

------------------------------------------------------------
OUTPUT
------------------------------------------------------------

Return ONLY valid JSON.

Do not use Markdown.

Do not use ```json.

Return exactly:

{{
    "entities": [
        {{
            "entity_id": "",
            "entity_type": "unknown",
            "text": "",
            "normalized_text": "",
            "page_number": 1,
            "source_node_id": "",
            "start_offset": null,
            "end_offset": null,
            "confidence": 0.0,
            "attributes": {{}},
            "metadata": {{}}
        }}
    ],
    "confidence": 0.0,
    "notes": "",
    "metadata": {{}}
}}

------------------------------------------------------------
ENTITY TYPES
------------------------------------------------------------

Use one of the following entity types whenever
applicable.

PATIENT

PATIENT_ID

MEDICAL_RECORD_NUMBER

SPECIMEN_ID

ACCESSION_NUMBER

DATE

AGE

SEX

PHONE

EMAIL

ADDRESS

ORGANIZATION

PROVIDER

PHYSICIAN

DEPARTMENT

HOSPITAL

CLINIC

MEDICATION

DRUG

DOSAGE

DOSAGE_UNIT

FREQUENCY

ROUTE

DURATION

DIAGNOSIS

SYMPTOM

CONDITION

PROCEDURE

SURGERY

LAB_TEST

LAB_RESULT

BIOMARKER

GENE

PROTEIN

MUTATION

VARIANT

ANATOMICAL_SITE

BODY_PART

PATHOLOGY_FINDING

RADIOLOGY_FINDING

IMAGING_STUDY

VITAL_SIGN

MEASUREMENT

UNIT

ALLERGY

FAMILY_HISTORY

SOCIAL_HISTORY

INSURANCE

INSURANCE_ID

CLAIM_ID

ORDER_ID

ENCOUNTER_ID

DOCUMENT_ID

OTHER

------------------------------------------------------------
PATIENT
------------------------------------------------------------

Example:

"Patient: John Doe"

Extract:

{{
    "entity_type": "PATIENT",
    "text": "John Doe",
    "normalized_text": "John Doe"
}}

------------------------------------------------------------
PATIENT IDENTIFIERS
------------------------------------------------------------

Example:

"MRN: 123456"

Extract:

{{
    "entity_type": "MEDICAL_RECORD_NUMBER",
    "text": "123456",
    "normalized_text": "123456"
}}

Do not change leading zeros.

------------------------------------------------------------
DATES
------------------------------------------------------------

Example:

"DOB: 12/05/1980"

Extract:

{{
    "entity_type": "DATE",
    "text": "12/05/1980",
    "normalized_text": "12/05/1980"
}}

Do not change date format at this stage.

Date normalization belongs to a later module.

------------------------------------------------------------
MEDICATIONS
------------------------------------------------------------

Example:

"Metformin 500 mg twice daily"

Extract separate entities where appropriate:

MEDICATION:
"Metformin"

DOSAGE:
"500"

DOSAGE_UNIT:
"mg"

FREQUENCY:
"twice daily"

Do not infer an unspecified dosage.

------------------------------------------------------------
LAB RESULTS
------------------------------------------------------------

Example:

"Hemoglobin: 12.5 g/dL"

Extract:

LAB_TEST:
"Hemoglobin"

LAB_RESULT:
"12.5"

UNIT:
"g/dL"

Do not determine whether the result is normal
or abnormal.

That belongs to the validation/clinical
interpretation layer.

------------------------------------------------------------
BIOMARKERS
------------------------------------------------------------

Example:

"HER2 positive"

Extract:

BIOMARKER:
"HER2"

and preserve the status in attributes:

{{
    "status": "positive"
}}

Do not infer additional clinical meaning.

------------------------------------------------------------
GENES
------------------------------------------------------------

Example:

"BRCA1 mutation detected"

Extract:

GENE:
"BRCA1"

MUTATION:
"mutation"

If a specific variant is explicitly present,
extract it as VARIANT.

------------------------------------------------------------
PATHOLOGY
------------------------------------------------------------

Example:

"Invasive ductal carcinoma"

Extract:

PATHOLOGY_FINDING:
"Invasive ductal carcinoma"

Do not invent tumor grade, stage, receptor
status, or other information.

------------------------------------------------------------
RADIOLOGY
------------------------------------------------------------

Example:

"MRI of the brain"

Extract:

IMAGING_STUDY:
"MRI"

ANATOMICAL_SITE:
"brain"

Do not interpret the image or invent findings.

------------------------------------------------------------
ENTITY BOUNDARIES
------------------------------------------------------------

The "text" field should contain the exact
text span representing the entity.

The "normalized_text" field may contain a
clean representation, but should not introduce
information absent from the source.

------------------------------------------------------------
SOURCE INFORMATION
------------------------------------------------------------

Every entity must contain:

page_number

source_node_id

This is required for traceability.

------------------------------------------------------------
CONFIDENCE
------------------------------------------------------------

Confidence must be between 0 and 1.

Use lower confidence when entity boundaries
or entity type are ambiguous.

------------------------------------------------------------
INPUT
------------------------------------------------------------

Page Number:
{page_number}

Source Node ID:
{node_id}

Layout Type:
{layout_type}

Text:

{text}

------------------------------------------------------------
FINAL INSTRUCTION
------------------------------------------------------------

Return ONLY the JSON object.
"""