"""HTTP client for Ollama, used as an optional classifier backend."""

from __future__ import annotations

import requests

from app.clients.base import BaseLLMClient
from app.core.settings import settings


class OllamaClient(BaseLLMClient):
    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{settings.ollama_base_url.rstrip('/')}/api/generate",
            json={"model": settings.ollama_model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return str(data.get("response", "")).strip()
