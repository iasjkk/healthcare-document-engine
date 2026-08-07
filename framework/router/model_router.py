"""
framework.router.model_router
=============================

Routes model requests to the appropriate provider
based on routing policies.
"""

from __future__ import annotations

from typing import Any

from framework.registry.provider_registry import ProviderRegistry
from framework.router.routing_policy import (
    RoutingPolicy,
    get_policy,
)


class ModelRouter:
    """
    Central model router.

    Responsibilities
    ----------------
    - Resolve routing policy
    - Lookup provider
    - Execute inference
    """

    def __init__(
        self,
        provider_registry: ProviderRegistry,
    ) -> None:

        self.provider_registry = provider_registry

    # ---------------------------------------------------------
    # Policy
    # ---------------------------------------------------------

    def get_policy(
        self,
        capability: str,
    ) -> RoutingPolicy:

        return get_policy(capability)

    # ---------------------------------------------------------
    # Provider
    # ---------------------------------------------------------

    def get_provider(
        self,
        provider_name: str,
    ):

        return self.provider_registry.get(provider_name)

    # ---------------------------------------------------------
    # Chat
    # ---------------------------------------------------------

    async def chat(
        self,
        capability: str,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> dict:
        """
        Execute a chat request using the routing policy.
        """

        policy = self.get_policy(capability)

        provider = self.get_provider(policy.provider)

        payload = {
            "model": policy.model,
            "messages": messages,
            "reasoning": policy.reasoning,
            "temperature": policy.temperature,
            "max_tokens": policy.max_tokens,
        }

        payload.update(kwargs)

        return await provider.chat(**payload)

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    async def health_check(self) -> dict[str, bool]:
        """
        Health status of all registered providers.
        """

        status = {}

        for name, provider in self.provider_registry.items():

            status[name] = await provider.health_check()

        return status

    # ---------------------------------------------------------
    # Available Providers
    # ---------------------------------------------------------

    def providers(self) -> list[str]:

        return self.provider_registry.list()

    # ---------------------------------------------------------
    # Available Models
    # ---------------------------------------------------------

    async def models(self) -> dict[str, list[str]]:

        result = {}

        for name, provider in self.provider_registry.items():

            result[name] = await provider.list_models()

        return result