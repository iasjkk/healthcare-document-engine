"""
framework.core.base_provider
============================

Abstract base class for all AI model providers.

Every provider implementation (OpenAI, OpenRouter, Ollama, Gemini,
Azure OpenAI, etc.) must inherit from this class.

Responsibilities
----------------
- Standard provider lifecycle
- Health check
- Model discovery
- Chat completion
- Embeddings (optional)
- Cleanup
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from framework.core.base_component import BaseComponent


class BaseProvider(BaseComponent, ABC):
    """
    Abstract base class for all model providers.
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

    # ------------------------------------------------------------------
    # Provider Lifecycle
    # ------------------------------------------------------------------

    @abstractmethod
    async def connect(self) -> None:
        """
        Initialize provider resources.
        """
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self) -> None:
        """
        Release provider resources.
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verify provider availability.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Model Information
    # ------------------------------------------------------------------

    @abstractmethod
    async def list_models(self) -> list[str]:
        """
        Return available model names.
        """
        raise NotImplementedError

    @abstractmethod
    async def supports_model(
        self,
        model_name: str,
    ) -> bool:
        """
        Check if a model is supported.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    @abstractmethod
    async def chat(
        self,
        **kwargs: Any,
    ) -> Any:
        """
        Chat completion.

        Concrete providers decide how requests are handled.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Embeddings (Optional)
    # ------------------------------------------------------------------

    async def embeddings(
        self,
        **kwargs: Any,
    ) -> Any:
        """
        Optional embedding generation.

        Providers not supporting embeddings can override
        or leave the default implementation.
        """
        raise NotImplementedError(
            f"{self.name} does not support embeddings."
        )

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @property
    def provider_name(self) -> str:
        return self.name