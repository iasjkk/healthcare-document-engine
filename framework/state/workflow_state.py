"""
framework.state.workflow_state
==============================

Root workflow state for the Healthcare Document Engine.

This is the single source of truth shared across the entire
workflow. Every agent reads from and writes to this object.

State is divided into:

1. Runtime State
2. Document Understanding State
3. Clinical Understanding State
4. Metrics & Validation
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from framework.state.checkpoint_state import CheckpointState
from framework.state.document_state import DocumentState
from framework.state.entity_state import EntityState
from framework.state.relation_state import RelationState
from framework.state.execution_state import ExecutionState
from framework.state.layout_state import LayoutState
from framework.state.metrics_state import MetricsState
from framework.state.model_state import ModelState
from framework.state.validation_state import ValidationState
from framework.state.clinical_summary_state import (
    ClinicalSummaryState,
)

class WorkflowState(BaseModel):
    """
    Root state shared by the complete workflow.

    This object is passed between LangGraph nodes, AutoGen
    agents, and custom orchestration components.
    """

    # ------------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------------

    execution: ExecutionState

    # ------------------------------------------------------------------
    # Document Understanding
    # ------------------------------------------------------------------

    document: DocumentState

    layout: LayoutState

    # ------------------------------------------------------------------
    # Clinical Understanding
    # ------------------------------------------------------------------

    entities: EntityState

    validation: ValidationState

    relations: RelationState = Field(
        default_factory=RelationState
    )

    clinical_summary: ClinicalSummaryState

    # ------------------------------------------------------------------
    # AI Model Execution
    # ------------------------------------------------------------------

    model: ModelState

    # ------------------------------------------------------------------
    # Runtime Metrics
    # ------------------------------------------------------------------

    metrics: MetricsState

    # ------------------------------------------------------------------
    # Workflow Checkpoints
    # ------------------------------------------------------------------

    checkpoint: CheckpointState = Field(
        default_factory=lambda: CheckpointState(

            checkpoint_id="",

            timestamp="",

            stage="",

        )
    )