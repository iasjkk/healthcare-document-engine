"""
Provider implementations.

Providers encapsulate communication with external AI services.

Available Providers
-------------------
- OpenRouterProvider
- OpenAIProvider
- GeminiProvider
- OllamaProvider
"""

from framework.providers.openrouter_provider import OpenRouterProvider

__all__ = [
    "OpenRouterProvider",
]