"""
Base prompt abstraction.
"""

from abc import ABC, abstractmethod


class BasePrompt(ABC):
    """
    Base class for all prompts.

    Every prompt should:
    - have a name
    - generate formatted text
    """


    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
    ) -> None:

        self.name = name
        self.version = version


    @abstractmethod
    def build(
        self,
        **kwargs,
    ) -> str:
        """
        Build final prompt.
        """

        raise NotImplementedError


    def __repr__(self):

        return (
            f"{self.__class__.__name__}"
            f"(name={self.name}, "
            f"version={self.version})"
        )