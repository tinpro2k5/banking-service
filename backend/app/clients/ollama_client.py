"""HTTP client for Ollama response generation."""

from __future__ import annotations

import requests

from app.clients.base import BaseLLMClient
from app.core.settings import settings


class OllamaClient(BaseLLMClient):
    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{settings.ollama_base_url.rstrip('/')}/api/generate",
            json={
                "model": settings.ollama_model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return str(data.get("response", "")).strip()

    def chat(self, messages: list[dict[str, str]], format: str | None = None) -> str:
        payload = {
            "model": settings.ollama_model,
            "messages": messages,
            "stream": False,
        }
        if format:
            payload["format"] = format  # Thêm dòng này để ép Ollama trả JSON chuẩn

        response = requests.post(
            f"{settings.ollama_base_url.rstrip('/')}/api/chat",
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        message_obj = data.get("message", {})
        return str(message_obj.get("content", "")).strip()
