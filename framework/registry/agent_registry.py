"""
framework.registry.agent_registry
=================================

Registry for workflow agents.
"""

from framework.core.base_agent import BaseAgent
from framework.core.base_registry import BaseRegistry


class AgentRegistry(BaseRegistry[BaseAgent]):
    """
    Registry for workflow agents.
    """

    pass