"""Intent node for the API gateway. It calls the gRPC intent service."""

from __future__ import annotations

from app.clients.grpc_intent_client import GrpcIntentClient
from app.clients.base import BaseIntentClient
from app.core.schemas import IntentResult


class IntentNode:
    def __init__(self) -> None:
        self._client: BaseIntentClient = GrpcIntentClient()

    def run(self, message: str) -> IntentResult:
        try:
            prediction = self._client.predict(message)
            return IntentResult(
                intent=prediction.intent or "unknown_intent",
                confidence=prediction.confidence,
                reason=prediction.reason,
            )
        except Exception as exc:  # pragma: no cover - network/runtime fallback
            return IntentResult(intent="unknown_intent", confidence=None, reason=f"Intent service unavailable: {exc}")
