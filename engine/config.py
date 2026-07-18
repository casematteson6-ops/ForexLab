"""
Configuration loader for ForexLab.
Loads settings from config/settings.yaml.
"""

from pathlib import Path
import yaml


class Config:
    def __init__(self):
        config_path = Path("config/settings.yaml")

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}"
            )

        with open(config_path, "r", encoding="utf-8") as file:
            self.settings = yaml.safe_load(file)

    def get(self, section, key):
        """Return a configuration value."""
        return self.settings[section][key]