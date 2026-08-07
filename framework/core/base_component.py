"""
framework.core.base_component
=============================

Base class for every framework component.

All agents, models, parsers, validators, storage providers,
and orchestrators inherit from BaseComponent.

Responsibilities
----------------
- Unique identity
- Metadata
- Configuration
- Runtime dependencies
- Lifecycle hooks
"""

from __future__ import annotations

from abc import ABC
from typing import Any
from uuid import uuid4


class BaseComponent(ABC):
    """
    Base class for all framework components.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        version: str = "1.0.0",
        enabled: bool = True,
    ) -> None:

        self.component_id = str(uuid4())

        self.name = name

        self.description = description

        self.version = version

        self.enabled = enabled

        # Runtime dependencies
        self.logger = None
        self.event_bus = None
        self.run_manager = None
        self.config = None

        # User-defined metadata
        self.metadata: dict[str, Any] = {}

    # ---------------------------------------------------------
    # Dependency Injection
    # ---------------------------------------------------------

    def set_logger(self, logger) -> None:
        self.logger = logger

    def set_event_bus(self, event_bus) -> None:
        self.event_bus = event_bus

    def set_run_manager(self, run_manager) -> None:
        self.run_manager = run_manager

    def set_config(self, config) -> None:
        self.config = config

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def add_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    # ---------------------------------------------------------
    # Lifecycle Hooks
    # ---------------------------------------------------------

    def initialize(self) -> None:
        """
        Called before the component starts.
        Override in subclasses if needed.
        """
        pass

    def shutdown(self) -> None:
        """
        Called before application shutdown.
        """
        pass

    def health_check(self) -> bool:
        """
        Returns True if component is healthy.
        """
        return self.enabled

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def info(self) -> dict[str, Any]:
        """
        Return component information.
        """
        return {
            "component_id": self.component_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "enabled": self.enabled,
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"version='{self.version}')"
        )