"""
Registry for prompt templates.
"""

from framework.core.base_registry import (
    BaseRegistry,
)

from framework.prompts.base_prompt import (
    BasePrompt,
)


class PromptRegistry(
    BaseRegistry[BasePrompt]
):
    """
    Registry containing all prompts.
    """

    pass