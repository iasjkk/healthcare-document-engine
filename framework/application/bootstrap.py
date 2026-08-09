"""
Application bootstrap and dependency wiring.

This module is responsible for constructing the healthcare
document engine and injecting all required dependencies.

Architecture
------------

OpenRouterProvider
        ↓
ProviderRegistry
        ↓
ModelRouter
        ↓
PromptRegistry
        ↓
AgentRegistry
        ↓
HealthcareOrchestrator

The bootstrap layer owns construction only.

Agents remain responsible for their own execution logic.
Routing remains controlled by routing_policy.py.
The orchestrator remains responsible for workflow execution.
"""

from __future__ import annotations

from framework.agents.clinical.clinical_summary_agent import (
    ClinicalSummaryAgent,
)
from framework.agents.document.document_structure_agent import (
    DocumentStructureAgent,
)
from framework.agents.entity.entity_extraction_agent import (
    EntityExtractionAgent,
)
from framework.agents.entity.entity_normalization_agent import (
    EntityNormalizationAgent,
)
from framework.agents.entity.entity_validation_agent import (
    EntityValidationAgent,
)
from framework.agents.relation.relation_extraction_agent import (
    RelationExtractionAgent,
)
from framework.agents.relation.relation_normalization_agent import (
    RelationNormalizationAgent,
)
from framework.agents.relation.relation_validation_agent import (
    RelationValidationAgent,
)
from framework.agents.report.final_report_agent import (
    FinalReportAgent,
)

from framework.orchestrator.healthcare_orchestrator import (
    HealthcareOrchestrator,
)

from framework.prompts.prompt_registry import (
    PromptRegistry,
)

from framework.prompts.document_structure_prompt import (
    DocumentStructurePrompt,
)
from framework.prompts.entity_extraction_prompt import (
    EntityExtractionPrompt,
)
from framework.prompts.entity_normalization_prompt import (
    EntityNormalizationPrompt,
)
from framework.prompts.entity_validation_prompt import (
    EntityValidationPrompt,
)
from framework.prompts.relation_extraction_prompt import (
    RelationExtractionPrompt,
)
from framework.prompts.relation_normalization_prompt import (
    RelationNormalizationPrompt,
)
from framework.prompts.relation_validation_prompt import (
    RelationValidationPrompt,
)
from framework.prompts.clinical_summary_prompt import (
    ClinicalSummaryPrompt,
)
from framework.prompts.final_report_prompt import (
    FinalReportPrompt,
)

from framework.providers.openrouter_provider import (
    OpenRouterProvider,
)

from framework.registry.agent_registry import (
    AgentRegistry,
)
from framework.registry.provider_registry import (
    ProviderRegistry,
)

from framework.router.model_router import (
    ModelRouter,
)


def build_provider_registry() -> ProviderRegistry:
    """
    Construct and populate the provider registry.
    """

    registry = ProviderRegistry()

    openrouter = OpenRouterProvider()

    registry.register(
        "openrouter",
        openrouter,
    )

    return registry


def build_prompt_registry() -> PromptRegistry:
    """
    Construct and populate the prompt registry.
    """

    registry = PromptRegistry()

    registry.register(
        "document_structure",
        DocumentStructurePrompt(),
    )

    registry.register(
        "entity_extraction",
        EntityExtractionPrompt(),
    )

    registry.register(
        "entity_normalization",
        EntityNormalizationPrompt(),
    )

    registry.register(
        "entity_validation",
        EntityValidationPrompt(),
    )

    registry.register(
        "relation_extraction",
        RelationExtractionPrompt(),
    )

    registry.register(
        "relation_normalization",
        RelationNormalizationPrompt(),
    )

    registry.register(
        "relation_validation",
        RelationValidationPrompt(),
    )

    registry.register(
        "clinical_summary",
        ClinicalSummaryPrompt(),
    )

    registry.register(
        "final_report",
        FinalReportPrompt(),
    )

    return registry


def build_model_router(
    provider_registry: ProviderRegistry,
) -> ModelRouter:
    """
    Construct the central model router.
    """

    return ModelRouter(
        provider_registry=provider_registry,
    )


def build_agent_registry(
    router: ModelRouter,
    prompt_registry: PromptRegistry,
) -> AgentRegistry:
    """
    Construct and register all workflow agents.

    Agent constructors are kept exactly aligned with the
    currently implemented agent classes.
    """

    registry = AgentRegistry()

    # ---------------------------------------------------------
    # Document
    # ---------------------------------------------------------

    registry.register(
        "document_structure",
        DocumentStructureAgent(
            router=router,
            prompt_registry=prompt_registry,
        ),
    )

    # ---------------------------------------------------------
    # Entity
    # ---------------------------------------------------------

    registry.register(
        "entity_extraction",
        EntityExtractionAgent(
            router=router,
            prompt_registry=prompt_registry,
        ),
    )

    registry.register(
        "entity_normalization",
        EntityNormalizationAgent(
            router=router,
            prompt_registry=prompt_registry,
        ),
    )

    registry.register(
        "entity_validation",
        EntityValidationAgent(
            router=router,
            prompt_registry=prompt_registry,
        ),
    )

    # ---------------------------------------------------------
    # Relation
    # ---------------------------------------------------------

    registry.register(
        "relation_extraction",
        RelationExtractionAgent(
            router=router,
        ),
    )

    registry.register(
        "relation_normalization",
        RelationNormalizationAgent(
            router=router,
            prompt_registry=prompt_registry,
        ),
    )

    registry.register(
        "relation_validation",
        RelationValidationAgent(
            router=router,
            prompt_registry=prompt_registry,
        ),
    )

    # ---------------------------------------------------------
    # Clinical Summary
    # ---------------------------------------------------------

    registry.register(
        "clinical_summary",
        ClinicalSummaryAgent(
            router=router,
            prompt_registry=prompt_registry,
        ),
    )

    # ---------------------------------------------------------
    # Final Report
    # ---------------------------------------------------------

    registry.register(
        "final_report",
        FinalReportAgent(
            router=router,
            prompt_registry=prompt_registry,
        ),
    )

    return registry


def build_healthcare_orchestrator(
    agent_registry: AgentRegistry,
    provider_registry: ProviderRegistry | None = None,
) -> HealthcareOrchestrator:
    """
    Construct the healthcare orchestrator.

    Initialization is intentionally separate from construction.
    """

    return HealthcareOrchestrator(
        agent_registry=agent_registry,
        provider_registry=provider_registry,
    )


def build_application() -> HealthcareOrchestrator:
    """
    Build the complete healthcare document engine.

    Returns
    -------
    HealthcareOrchestrator
        Fully wired orchestrator. Call initialize() before run().
    """

    # ---------------------------------------------------------
    # Providers
    # ---------------------------------------------------------

    provider_registry = build_provider_registry()

    # ---------------------------------------------------------
    # Router
    # ---------------------------------------------------------

    router = build_model_router(
        provider_registry,
    )

    # ---------------------------------------------------------
    # Prompts
    # ---------------------------------------------------------

    prompt_registry = build_prompt_registry()

    # ---------------------------------------------------------
    # Agents
    # ---------------------------------------------------------

    agent_registry = build_agent_registry(
        router=router,
        prompt_registry=prompt_registry,
    )

    # ---------------------------------------------------------
    # Orchestrator
    # ---------------------------------------------------------

    orchestrator = build_healthcare_orchestrator(
        agent_registry=agent_registry,
        provider_registry=provider_registry,
    )

    return orchestrator