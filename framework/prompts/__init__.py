"""
Prompt management layer.

Contains reusable and version-controlled
prompts used by AI agents.
"""

from framework.prompts.base_prompt import BasePrompt
from framework.prompts.document_structure_prompt import (
    DocumentStructurePrompt,
)
from framework.prompts.prompt_registry import (
    PromptRegistry,
)

__all__ = [
    "BasePrompt",
    "DocumentStructurePrompt",
    "PromptRegistry",
]