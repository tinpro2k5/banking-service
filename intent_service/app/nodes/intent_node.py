"""Intent classifier for the gRPC microservice using Ollama only."""

from __future__ import annotations

import json
import re

from app.clients.ollama_client import OllamaClient
from app.core.schemas import IntentResult
from app.core.settings import settings
from app.data.policies import POLICIES

class IntentNode:
    def __init__(self) -> None:
        self._ollama = OllamaClient()

    def _ollama_classify(self, message: str) -> IntentResult:
        labels = ", ".join(POLICIES.keys())
        prompt = f"""Classify the customer message into exactly one of these banking intents:
{labels}

Return JSON with keys: intent, confidence, reason.
Message: {message}
"""
        raw = self._ollama.generate(prompt)
        try:
            payload = json.loads(raw)
            return IntentResult(
                intent=str(payload.get("intent", "unknown_intent")),
                confidence=float(payload.get("confidence", 0.0) or 0.0),
                reason=str(payload.get("reason", "")),
            )
        except Exception as exc:
            # If Ollama returns invalid JSON, return a fallback with the raw output for debugging
            return IntentResult(
                intent="unknown_intent",
                confidence=0.0,
                reason=f"Failed to parse JSON. Error: {exc} | Raw Output: {raw}"
            )

    def run(self, message: str) -> IntentResult:
        try:
            return self._ollama_classify(message)
        except Exception as exc:
            return IntentResult(
                intent="unknown_intent",
                confidence=0.0,
                reason=f"Ollama HTTP connection failed: {exc}"
            )
