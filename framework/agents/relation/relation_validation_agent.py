"""
Healthcare Relation Validation Agent.

Validates healthcare relations against the
available entity set while preserving provenance.
"""

from __future__ import annotations

from framework.core.base_agent import BaseAgent
from framework.prompts.prompt_registry import PromptRegistry
from framework.router.model_router import ModelRouter
from framework.schemas.relation_validation_schema import (
    RelationValidationResponse,
)
from framework.state.workflow_state import WorkflowState
from framework.utils.json_parser import parse_json_response


class RelationValidationAgent(BaseAgent):
    """
    Validate healthcare relations.

    Canonical inputs:

        state.entities.entities
        state.relations.relations

    The application layer performs structural
    validation and preserves entity references.
    The LLM performs semantic validation.
    """

    def __init__(
        self,
        router: ModelRouter,
        prompt_registry: PromptRegistry,
    ) -> None:

        super().__init__(
            name="relation_validation_agent",
            description=(
                "Validates healthcare relations "
                "against extracted entities while "
                "preserving provenance."
            ),
            version="1.0.0",
        )

        self.router = router
        self.prompt_registry = prompt_registry

    async def execute(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        """
        Execute relation validation.
        """

        if self.logger:

            self.logger.info(
                "Starting Relation Validation."
            )

        # ------------------------------------------------------
        # Get entities and relations.
        # ------------------------------------------------------

        entities = state.entities.entities

        relations = state.relations.relations

        if not relations:

            if self.logger:

                self.logger.warning(
                    "No relations found for validation."
                )

            state.checkpoint.stage = (
                "relation_validation_completed"
            )

            return state

        # ------------------------------------------------------
        # Build entity lookup.
        # ------------------------------------------------------

        entity_ids = {
            entity.entity_id
            for entity in entities
        }

        entity_payload = []

        for entity in entities:

            entity_payload.append(
                {
                    "entity_id": entity.entity_id,
                    "entity_type": entity.entity_type,
                    "value": entity.value,
                    "normalized_value": (
                        entity.normalized_value
                    ),
                    "confidence": entity.confidence,
                    "page_number": entity.page_number,
                    "source_node": entity.source_node,
                    "attributes": entity.metadata,
                }
            )

        # ------------------------------------------------------
        # Build relation payload.
        # ------------------------------------------------------

        relation_payload = []

        for relation in relations:

            relation_payload.append(
                {
                    "relation_id": relation.relation_id,
                    "source_entity_id": (
                        relation.source_entity_id
                    ),
                    "target_entity_id": (
                        relation.target_entity_id
                    ),
                    "relation_type": (
                        relation.relation_type
                    ),
                    "confidence": relation.confidence,
                    "attributes": relation.attributes,
                    "metadata": relation.metadata,
                }
            )

        # ------------------------------------------------------
        # Build prompt.
        # ------------------------------------------------------

        prompt_template = self.prompt_registry.get(
            "relation_validation"
        )

        prompt = prompt_template.build(
            relations=relation_payload,
            entities=entity_payload,
        )

        # ------------------------------------------------------
        # LLM call.
        # ------------------------------------------------------

        response = await self.router.chat(
            capability="relation_validation",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert healthcare "
                        "relation validation system. "
                        "Return only valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        # ------------------------------------------------------
        # Extract response.
        # ------------------------------------------------------

        result_text = (
            response[
                "choices"
            ][0][
                "message"
            ][
                "content"
            ]
        )

        # ------------------------------------------------------
        # Parse and validate.
        # ------------------------------------------------------

        parsed = parse_json_response(
            result_text,
            RelationValidationResponse,
        )

        validation_by_id = {
            result.relation_id: result
            for result in parsed.relations
        }

        validated_count = 0
        invalid_count = 0
        warning_count = 0

        # ------------------------------------------------------
        # Apply validation results.
        # ------------------------------------------------------

        for relation in relations:

            validation = validation_by_id.get(
                relation.relation_id
            )

            # --------------------------------------------------
            # Structural validation performed by application.
            # --------------------------------------------------

            structural_issues = []

            if (
                relation.source_entity_id
                not in entity_ids
            ):

                structural_issues.append(
                    "Source entity does not exist."
                )

            if (
                relation.target_entity_id
                not in entity_ids
            ):

                structural_issues.append(
                    "Target entity does not exist."
                )

            if not relation.relation_type:

                structural_issues.append(
                    "Relation type is empty."
                )

            # --------------------------------------------------
            # No LLM result.
            # --------------------------------------------------

            if validation is None:

                relation.metadata[
                    "validation_status"
                ] = "warning"

                relation.metadata[
                    "validation_confidence"
                ] = 0.0

                relation.metadata[
                    "validation_issues"
                ] = [
                    "No validation result returned "
                    "by the model."
                ]

                warning_count += 1

                continue

            # --------------------------------------------------
            # Combine structural + semantic issues.
            # --------------------------------------------------

            issues = list(
                validation.issues
            )

            issues.extend(
                structural_issues
            )

            # --------------------------------------------------
            # Determine final validation status.
            #
            # Structural errors always override
            # the LLM's decision.
            # --------------------------------------------------

            if structural_issues:

                final_status = "invalid"
                final_valid = False

            elif validation.validation_status == "invalid":

                final_status = "invalid"
                final_valid = False

            elif validation.validation_status == "warning":

                final_status = "warning"
                final_valid = True

            else:

                final_status = "valid"
                final_valid = True

            # --------------------------------------------------
            # Store validation information.
            # --------------------------------------------------

            relation.metadata[
                "validation_status"
            ] = final_status

            relation.metadata[
                "validation_is_valid"
            ] = final_valid

            relation.metadata[
                "validation_confidence"
            ] = validation.confidence

            relation.metadata[
                "validation_issues"
            ] = issues

            relation.metadata[
                "validation_warnings"
            ] = validation.warnings

            if validation.attributes:

                relation.attributes.update(
                    validation.attributes
                )

            if validation.metadata:

                relation.metadata[
                    "validation_metadata"
                ] = validation.metadata

            # --------------------------------------------------
            # Counters.
            # --------------------------------------------------

            if final_status == "invalid":

                invalid_count += 1

            elif final_status == "warning":

                warning_count += 1

            else:

                validated_count += 1

        # ------------------------------------------------------
        # Preserve canonical relation state.
        # ------------------------------------------------------

        state.relations.relations = relations

        # ------------------------------------------------------
        # Checkpoint.
        # ------------------------------------------------------

        state.checkpoint.stage = (
            "relation_validation_completed"
        )

        if self.logger:

            self.logger.info(
                "Relation Validation Complete. "
                f"Valid: {validated_count}, "
                f"Warnings: {warning_count}, "
                f"Invalid: {invalid_count}."
            )

        return state