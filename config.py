"""Centralized configuration loaded from environment variables (.env)."""
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    google_api_key: str
    google_cx: str
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str
    azure_openai_deployment: str

    def validate(self) -> None:
        missing = [
            name
            for name, value in [
                ("GOOGLE_API_KEY", self.google_api_key),
                ("GOOGLE_CX", self.google_cx),
                ("AZURE_OPENAI_API_KEY", self.azure_openai_api_key),
                ("AZURE_OPENAI_ENDPOINT", self.azure_openai_endpoint),
                ("AZURE_OPENAI_API_VERSION", self.azure_openai_api_version),
                ("AZURE_OPENAI_DEPLOYMENT", self.azure_openai_deployment),
            ]
            if not value
        ]
        if missing:
            raise RuntimeError(
                "Missing required environment variable(s): "
                + ", ".join(missing)
                + ". Fill them in your .env file (see .env.example)."
            )


def load_settings() -> Settings:
    return Settings(
        google_api_key=os.getenv("GOOGLE_API_KEY", ""),
        google_cx=os.getenv("GOOGLE_CX", ""),
        azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
        azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", ""),
        azure_openai_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", ""),
    )
