"""
framework.registry.validator_registry
=====================================

Registry for validators.
"""

from framework.core.base_registry import BaseRegistry
from framework.core.base_validator import BaseValidator


class ValidatorRegistry(BaseRegistry[BaseValidator]):
    """
    Registry for validators.
    """

    pass