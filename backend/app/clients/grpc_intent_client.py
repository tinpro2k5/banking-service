"""gRPC client wrapper for the intent service."""

from __future__ import annotations

from dataclasses import dataclass

import grpc

from app.clients.intent_grpc import intent_service_pb2, intent_service_pb2_grpc
from app.core.settings import settings


@dataclass
class IntentPrediction:
    intent: str
    confidence: float | None
    reason: str | None = None


class GrpcIntentClient:
    def __init__(self, host: str | None = None, port: int | None = None, timeout: float | None = None) -> None:
        target = f"{host or settings.intent_service_host}:{port or settings.intent_service_port}"
        self._channel = grpc.insecure_channel(target)
        self._stub = intent_service_pb2_grpc.IntentServiceStub(self._channel)
        self._timeout = timeout or settings.intent_service_timeout

    def predict(self, message: str) -> IntentPrediction:
        response = self._stub.PredictIntent(
            intent_service_pb2.IntentRequest(message=message),
            timeout=self._timeout,
        )
        confidence = response.confidence
        if confidence is not None:
            try:
                confidence = float(confidence)
            except (TypeError, ValueError):
                confidence = None
        return IntentPrediction(intent=response.intent, confidence=confidence, reason=response.reason or None)
