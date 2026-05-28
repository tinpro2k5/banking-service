"""Application settings for the API gateway."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    intent_service_host: str = "intent-service"
    intent_service_port: int = 50051
    intent_service_timeout: float = 20.0
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gpt-oss:20b"
    frontend_base_url: str = "http://frontend:8501"


settings = Settings()
