"""
framework.registry.parser_registry
==================================

Registry for parsers.
"""

from framework.core.base_parser import BaseParser
from framework.core.base_registry import BaseRegistry


class ParserRegistry(BaseRegistry[BaseParser]):
    """
    Registry for parsers.
    """

    pass