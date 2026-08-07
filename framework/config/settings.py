"""
Environment Settings

Loads values from .env

Nothing else.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    OPENROUTER_API_KEY: str = ""

    OPENAI_API_KEY: str = ""

    ANTHROPIC_API_KEY: str = ""

    GOOGLE_API_KEY: str = ""

    model_config = SettingsConfigDict(

        env_file=".env",

        extra="ignore",

    )


settings = Settings()