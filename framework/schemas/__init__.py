"""
Pydantic response schemas used by AI agents.

Every LLM response should be validated against one of these
schemas before updating WorkflowState.
"""

from .document_structure_schema import (
    SectionSchema,
    DocumentStructureResponse,
)

from .layout_schema import (
    LayoutClassification,
    LayoutClassificationResponse,
)

from .table_schema import (
    TableCell,
    TableRow,
    TableSchema,
    TableExtractionResponse,
)

from .entity_schema import (
    ClinicalEntity,
    EntityExtractionResponse,
)

from .validation_schema import (
    ValidationIssue,
    ValidationResponse,
)