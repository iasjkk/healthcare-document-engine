"""
framework.providers.openrouter_provider
=======================================

OpenRouter provider implementation.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from framework.core.base_provider import BaseProvider


class OpenRouterProvider(BaseProvider):
    """
    OpenRouter provider.
    """

    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(
        self,
        api_key: str | None = None,
        timeout: float = 120.0,
    ) -> None:

        super().__init__(
            name="openrouter",
            description="OpenRouter AI Provider",
            version="1.0.0",
        )

        self.api_key = api_key or os.getenv("OPEN_ROUTER_API_KEY")

        if not self.api_key:
            raise ValueError(
                "OPEN_ROUTER_API_KEY environment variable is not set."
            )

        self.timeout = timeout

        self.client: httpx.AsyncClient | None = None

    # ==========================================================
    # Internal
    # ==========================================================

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    # ==========================================================
    # Lifecycle
    # ==========================================================

    async def connect(self) -> None:

        if self.client is None:

            self.client = httpx.AsyncClient(
                timeout=self.timeout,
                headers=self.headers,
            )

            if self.logger:
                self.logger.info(
                    "Connected to OpenRouter."
                )

    async def disconnect(self) -> None:

        if self.client:

            await self.client.aclose()

            self.client = None

            if self.logger:
                self.logger.info(
                    "Disconnected from OpenRouter."
                )

    async def health_check(self) -> bool:

        try:

            await self.list_models()

            return True

        except Exception:

            return False

    # ==========================================================
    # Models
    # ==========================================================

    async def list_models(self) -> list[str]:

        if self.client is None:
            await self.connect()

        response = await self.client.get(
            f"{self.BASE_URL}/models"
        )

        response.raise_for_status()

        data = response.json()

        return [
            model["id"]
            for model in data.get("data", [])
        ]

    async def supports_model(
        self,
        model_name: str,
    ) -> bool:

        models = await self.list_models()

        return model_name in models

    # ==========================================================
    # Chat
    # ==========================================================

    async def chat(
        self,
        **kwargs: Any,
    ) -> dict:

        if self.client is None:
            await self.connect()

        model = kwargs["model"]

        messages = kwargs["messages"]

        reasoning = kwargs.get(
            "reasoning",
            False,
        )

        payload = {
            "model": model,
            "messages": messages,
        }

        if reasoning:

            payload["reasoning"] = {
                "enabled": True
            }

        response = await self.client.post(
            f"{self.BASE_URL}/chat/completions",
            json=payload,
        )

        response.raise_for_status()

        return response.json()