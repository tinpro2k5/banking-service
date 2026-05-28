"""Intent classifier for the gRPC microservice using Ollama only."""

from __future__ import annotations

import json
import re

from app.clients.ollama_client import OllamaClient
from app.core.schemas import IntentResult
from app.data.policies import POLICIES


_VALID_INTENTS = set(POLICIES.keys())
_JSON_BLOCK_RE = re.compile(r"\{.*\}", re.DOTALL)


class IntentNode:
    def __init__(self) -> None:
        self._ollama = OllamaClient()

    @staticmethod
    def _extract_json_payload(raw: str) -> dict:
        text = raw.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE | re.DOTALL)

        match = _JSON_BLOCK_RE.search(text)
        if match:
            text = match.group(0)

        payload = json.loads(text)
        if not isinstance(payload, dict):
            raise ValueError("Ollama response is not a JSON object")
        return payload

    @staticmethod
    def _normalize_confidence(value: object) -> float:
        try:
            confidence = float(value)
        except (TypeError, ValueError):
            return 0.0
        if confidence != confidence:  # NaN guard
            return 0.0
        return max(0.0, min(1.0, confidence))

    @staticmethod
    def _normalize_intent(value: object) -> str:
        intent = str(value or "").strip()
        return intent if intent in _VALID_INTENTS else "unknown_intent"

    def _build_result(self, payload: dict, raw: str) -> IntentResult:
        intent = self._normalize_intent(payload.get("intent"))
        confidence = self._normalize_confidence(payload.get("confidence"))
        reason = str(payload.get("reason", "")).strip()

        if intent == "unknown_intent":
            if not reason:
                reason = f"Invalid or unsupported intent returned by Ollama. Raw output: {raw}"
        elif not reason:
            reason = f"Classified as {intent}."

        return IntentResult(intent=intent, confidence=confidence, reason=reason)

    def _ollama_classify(self, message: str) -> IntentResult:
        labels = ", ".join(POLICIES.keys())
        prompt = f"""Classify the customer message into exactly one of these banking intents:
{labels}

Return JSON with keys: intent, confidence, reason.
Keep the JSON values concise; the `reason` field should be no longer than 3 sentences.
Message: {message}
"""
        raw = self._ollama.generate(prompt)
        try:
            payload = self._extract_json_payload(raw)
            return self._build_result(payload, raw)
        except Exception as exc:
            return IntentResult(
                intent="unknown_intent",
                confidence=0.0,
                reason=f"Failed to parse or validate Ollama JSON. Error: {exc} | Raw Output: {raw}"
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
