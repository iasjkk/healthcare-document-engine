"""
Configuration Loader

Responsibilities
----------------
1. Load YAML files
2. Deep merge dictionaries
3. Return one configuration dictionary

This module MUST NOT know anything about
environment variables or application logic.
"""

from pathlib import Path
from typing import Any

import yaml


class ConfigLoader:

    def __init__(self, config_directory: str = "configs"):

        self.config_directory = Path(config_directory)

    # --------------------------------------------------

    def load_yaml(self, filename: str) -> dict:

        path = self.config_directory / filename

        if not path.exists():
            raise FileNotFoundError(path)

        with open(path, "r", encoding="utf-8") as file:

            data = yaml.safe_load(file)

        return data or {}

    # --------------------------------------------------

    def deep_merge(
        self,
        source: dict,
        destination: dict,
    ) -> dict:

        for key, value in source.items():

            if (
                key in destination
                and isinstance(destination[key], dict)
                and isinstance(value, dict)
            ):

                self.deep_merge(value, destination[key])

            else:

                destination[key] = value

        return destination

    # --------------------------------------------------

    def load_all(self) -> dict[str, Any]:

        configuration = {}

        yaml_files = sorted(self.config_directory.glob("*.yaml"))

        for file in yaml_files:

            data = self.load_yaml(file.name)

            configuration = self.deep_merge(
                data,
                configuration,
            )

        return configuration