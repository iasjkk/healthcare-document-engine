"""
framework.core.base_agent
=========================

Abstract base class for all workflow agents.

Every healthcare agent must inherit from this class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from framework.core.base_component import BaseComponent
from framework.state.workflow_state import WorkflowState


class BaseAgent(BaseComponent, ABC):
    """
    Base class for all workflow agents.
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

        self.provider = None

    # ---------------------------------------------------------
    # Dependency Injection
    # ---------------------------------------------------------

    def set_provider(self, provider: Any) -> None:
        self.provider = provider

    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    async def before_execute(
        self,
        state: WorkflowState,
    ) -> None:
        """
        Hook executed before execute().
        """

    @abstractmethod
    async def execute(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        """
        Execute the agent logic.

        Must be implemented by every concrete agent.
        """
        raise NotImplementedError

    async def after_execute(
        self,
        state: WorkflowState,
    ) -> None:
        """
        Hook executed after execute().
        """

    async def cleanup(self) -> None:
        """
        Cleanup resources.
        """

    # ---------------------------------------------------------
    # Main Entry Point
    # ---------------------------------------------------------

    async def run(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        """
        Standard execution lifecycle.
        """

        start_time = datetime.utcnow()

        await self.before_execute(state)

        updated_state = await self.execute(state)

        await self.after_execute(updated_state)

        end_time = datetime.utcnow()

        duration = (
            end_time - start_time
        ).total_seconds()

        if self.logger:

            self.logger.info(
                f"{self.name} completed "
                f"in {duration:.3f}s"
            )

        return updated_state