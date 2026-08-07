"""
Central Configuration Manager

Every module should import this class.

Never import YAML directly.
"""

from typing import Any

from framework.config.config_loader import ConfigLoader
from framework.config.settings import settings


class ConfigManager:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance._initialize()

        return cls._instance

    # --------------------------------------------

    def _initialize(self):

        loader = ConfigLoader()

        self.config = loader.load_all()

        self.environment = settings

    # --------------------------------------------

    def get(self, key: str, default=None):

        keys = key.split(".")

        value = self.config

        for item in keys:

            if isinstance(value, dict):

                value = value.get(item)

            else:

                return default

            if value is None:

                return default

        return value

    # --------------------------------------------

    def env(self, key: str):

        return getattr(self.environment, key)