"""
Prompt for Final Clinical Report Generation Agent.

The Final Report Agent combines the outputs of the clinical
understanding pipeline into one structured clinical report.
"""

from __future__ import annotations

from typing import Any


class FinalReportPrompt:
    """
    Builds the prompt used by the Final Report Agent.
    """

    name = "final_report"

    system_prompt = """
You are a Clinical Final Report Generation Agent.

Your responsibility is to combine the structured information
available in the workflow state into a coherent, accurate,
clinically useful final report.

You MUST follow these rules:

1. Use only information available in the supplied workflow state.
2. Do not invent clinical facts.
3. Do not infer unsupported diagnoses.
4. Preserve clinically important values exactly when possible.
5. Preserve medication dosage, frequency, route, and status.
6. Preserve biomarker names and results.
7. If information is unavailable, use an empty string or empty list.
8. Do not omit clinically important information.
9. Do not introduce recommendations that are not supported by
   the supplied clinical information.
10. Return ONLY valid JSON.
11. Do not return Markdown.
12. Do not wrap JSON inside ```json fences.
"""

    output_schema = """
{
    "title": "Clinical Report",

    "summary": "",

    "sections": [
        {
            "title": "",
            "content": "",
            "metadata": {}
        }
    ],

    "key_findings": [],

    "diagnoses": [],

    "medications": [
        {
            "name": "",
            "dosage": "",
            "frequency": "",
            "route": "",
            "status": "",
            "metadata": {}
        }
    ],

    "allergies": [],

    "laboratory_findings": [],

    "pathology_findings": [],

    "biomarkers": [
        {
            "name": "",
            "result": "",
            "status": "",
            "value": "",
            "unit": "",
            "percentage": "",
            "metadata": {}
        }
    ],

    "procedures": [],

    "recommendations": [],

    "validation_status": "validated",

    "confidence": 1.0,

    "notes": "",

    "metadata": {}
}
"""

    def build(
        self,
        *,
        workflow_state: Any = None,
        context: Any = None,
        **kwargs: Any,
    ) -> str:
        """
        Build the final-report prompt.

        Supports workflow_state or context so that the prompt
        remains compatible with different agent implementations.
        """

        source = (
            workflow_state
            if workflow_state is not None
            else context
        )

        source_data = self._serialize(source)

        return f"""
{self.system_prompt}

============================================================
CLINICAL WORKFLOW DATA
============================================================

{source_data}

============================================================
TASK
============================================================

Generate the final clinical report using ONLY the information
contained in the workflow data.

The report should consolidate:

- Clinical summary
- Key findings
- Diagnoses
- Medications
- Allergies
- Laboratory findings
- Pathology findings
- Biomarkers
- Procedures
- Recommendations
- Validation information

Do not create unsupported medical information.

============================================================
MEDICATION RULE
============================================================

Every medication MUST be represented as an object.

Correct:

"medications": [
    {{
        "name": "Metformin",
        "dosage": "500 mg",
        "frequency": "twice daily",
        "route": "",
        "status": "",
        "metadata": {{}}
    }}
]

Incorrect:

"medications": [
    "Metformin 500 mg twice daily"
]

============================================================
BIOMARKER RULE
============================================================

Every biomarker MUST be represented as an object.

Correct:

"biomarkers": [
    {{
        "name": "HER2",
        "result": "positive",
        "status": "positive",
        "value": "",
        "unit": "",
        "percentage": "",
        "metadata": {{}}
    }}
]

Incorrect:

"biomarkers": [
    "HER2 positive"
]

============================================================
OUTPUT SCHEMA
============================================================

Return ONLY a JSON object matching this structure:

{self.output_schema}

============================================================
FINAL INSTRUCTIONS
============================================================

- Return valid JSON only.
- Do not return Markdown.
- Do not add comments.
- Do not add explanatory text.
- Do not invent missing information.
- Use empty strings for unavailable scalar values.
- Use empty lists for unavailable collections.
- Keep confidence between 0.0 and 1.0.
"""

    def render(
        self,
        *,
        workflow_state: Any = None,
        context: Any = None,
        **kwargs: Any,
    ) -> str:
        """
        Alias for build().
        """

        return self.build(
            workflow_state=workflow_state,
            context=context,
            **kwargs,
        )

    def format(
        self,
        workflow_state: Any = None,
        context: Any = None,
        **kwargs: Any,
    ) -> str:
        """
        Alias for build().
        """

        return self.build(
            workflow_state=workflow_state,
            context=context,
            **kwargs,
        )

    @staticmethod
    def _serialize(value: Any) -> str:
        """
        Convert Pydantic models, dictionaries, and arbitrary
        objects into readable prompt data.
        """

        if value is None:
            return "{}"

        if hasattr(value, "model_dump"):
            value = value.model_dump()

        elif hasattr(value, "dict"):
            value = value.dict()

        elif not isinstance(value, (dict, list, tuple, str)):
            try:
                value = vars(value)
            except TypeError:
                value = str(value)

        try:
            import json

            return json.dumps(
                value,
                indent=2,
                ensure_ascii=False,
                default=str,
            )

        except Exception:
            return str(value)