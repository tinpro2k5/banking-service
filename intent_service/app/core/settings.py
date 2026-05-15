"""Settings for the intent service."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    grpc_host: str = "0.0.0.0"
    grpc_port: int = 50051
    intent_mode: str = "heuristic"
    ollama_base_url: str = "http://ollama:11434"
    ollama_model: str = "gpt-oss:20b"


settings = Settings()
