from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    cerebras_api_key: str = ""
    cerebras_base_url: str = "https://api.cerebras.ai/v1"
    cerebras_model: str = "gpt-oss-120b"

    checkpointer: str = "memory"
    postgres_url: str = ""

    # memory store
    store_backend: str = "memory"

    log_level: str = "INFO"

    @property
    def is_configured(self) -> bool:
        return bool(self.cerebras_api_key)

settings = Settings()

