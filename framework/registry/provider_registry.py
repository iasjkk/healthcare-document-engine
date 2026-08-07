"""
framework.registry.provider_registry
====================================

Registry for model providers.
"""

from framework.core.base_provider import BaseProvider
from framework.core.base_registry import BaseRegistry


class ProviderRegistry(BaseRegistry[BaseProvider]):
    """
    Registry for model providers.
    """

    pass