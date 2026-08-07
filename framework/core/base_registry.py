"""
framework.core.base_registry
============================

Generic registry implementation.

All framework registries inherit from this class.

Examples
--------
- AgentRegistry
- ProviderRegistry
- ParserRegistry
- ValidatorRegistry
- WorkflowRegistry
"""

from __future__ import annotations

from abc import ABC
from collections import OrderedDict
from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class BaseRegistry(ABC, Generic[T]):
    """
    Generic registry for framework components.

    Components are registered using a unique string key.
    """

    def __init__(self) -> None:
        self._registry: OrderedDict[str, T] = OrderedDict()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, name: str, component: T) -> None:
        """
        Register a component.

        Raises
        ------
        ValueError
            If the name already exists.
        """

        if name in self._registry:
            raise ValueError(
                f"'{name}' is already registered."
            )

        self._registry[name] = component

    # ------------------------------------------------------------------
    # Removal
    # ------------------------------------------------------------------

    def unregister(self, name: str) -> None:
        """
        Remove a registered component.
        """

        self._registry.pop(name, None)

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, name: str) -> T:
        """
        Retrieve a registered component.

        Raises
        ------
        KeyError
            If component is not registered.
        """

        if name not in self._registry:
            raise KeyError(
                f"'{name}' is not registered."
            )

        return self._registry[name]

    def exists(self, name: str) -> bool:
        """
        Check whether a component exists.
        """

        return name in self._registry

    # ------------------------------------------------------------------
    # Collection Operations
    # ------------------------------------------------------------------

    def list(self) -> list[str]:
        """
        Return all registered names.
        """

        return list(self._registry.keys())

    def values(self) -> list[T]:
        """
        Return all registered components.
        """

        return list(self._registry.values())

    def items(self):
        """
        Return registry items.
        """

        return self._registry.items()

    def clear(self) -> None:
        """
        Remove all registered components.
        """

        self._registry.clear()

    # ------------------------------------------------------------------
    # Python Magic Methods
    # ------------------------------------------------------------------

    def __contains__(self, name: str) -> bool:
        return name in self._registry

    def __len__(self) -> int:
        return len(self._registry)

    def __iter__(self) -> Iterator[T]:
        return iter(self._registry.values())

    def __getitem__(self, name: str) -> T:
        return self.get(name)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(size={len(self)})"
        )