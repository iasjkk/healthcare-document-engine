"""
framework.core.base_orchestrator
================================

Abstract base class for all workflow orchestrators.

Concrete implementations:
    - LangGraphOrchestrator
    - AutoGenOrchestrator
    - HybridOrchestrator

Responsibilities
----------------
- Orchestrate workflow execution
- Coordinate agents
- Maintain workflow lifecycle
- Interact with registries
- Manage execution state

NOTE:
This class DOES NOT own agents or providers.
Those responsibilities belong to the Registry layer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from framework.core.base_component import BaseComponent
from framework.state.workflow_state import WorkflowState


class BaseOrchestrator(BaseComponent, ABC):
    """
    Base class for all orchestrators.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        version: str = "1.0.0",
        enabled: bool = True,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            version=version,
            enabled=enabled,
        )

        # ----------------------------------------------------------
        # Registries (Injected)
        # ----------------------------------------------------------

        self.agent_registry = None
        self.provider_registry = None
        self.parser_registry = None
        self.validator_registry = None
        self.workflow_registry = None

    # ==========================================================
    # Registry Injection
    # ==========================================================

    def set_agent_registry(self, registry) -> None:
        """
        Inject AgentRegistry.
        """
        self.agent_registry = registry

    def set_provider_registry(self, registry) -> None:
        """
        Inject ProviderRegistry.
        """
        self.provider_registry = registry

    def set_parser_registry(self, registry) -> None:
        """
        Inject ParserRegistry.
        """
        self.parser_registry = registry

    def set_validator_registry(self, registry) -> None:
        """
        Inject ValidatorRegistry.
        """
        self.validator_registry = registry

    def set_workflow_registry(self, registry) -> None:
        """
        Inject WorkflowRegistry.
        """
        self.workflow_registry = registry

    # ==========================================================
    # Lifecycle
    # ==========================================================

    async def initialize(self) -> None:
        """
        Initialize orchestrator resources.

        Override in subclasses if needed.
        """
        pass

    async def shutdown(self) -> None:
        """
        Shutdown orchestrator resources.
        """
        pass

    async def pause(self) -> None:
        """
        Pause workflow execution.
        """
        pass

    async def resume(self) -> None:
        """
        Resume workflow execution.
        """
        pass

    async def stop(self) -> None:
        """
        Stop workflow execution.
        """
        pass

    # ==========================================================
    # Execution
    # ==========================================================

    @abstractmethod
    async def run(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        """
        Execute the workflow.

        Parameters
        ----------
        state : WorkflowState
            Shared workflow state.

        Returns
        -------
        WorkflowState
            Updated workflow state.
        """
        raise NotImplementedError