"""Compatibility protobuf module for the intent gRPC service."""

from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass
class IntentRequest:
    message: str = ""

    def SerializeToString(self) -> bytes:
        return json.dumps({"message": self.message}).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "IntentRequest":
        payload = json.loads(data.decode("utf-8") or "{}")
        return cls(message=str(payload.get("message", "")))


@dataclass
class IntentResponse:
    intent: str = "unknown_intent"
    confidence: float = 0.0
    reason: str = ""

    def SerializeToString(self) -> bytes:
        return json.dumps(
            {
                "intent": self.intent,
                "confidence": self.confidence,
                "reason": self.reason,
            }
        ).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "IntentResponse":
        payload = json.loads(data.decode("utf-8") or "{}")
        return cls(
            intent=str(payload.get("intent", "unknown_intent")),
            confidence=float(payload.get("confidence", 0.0) or 0.0),
            reason=str(payload.get("reason", "")),
        )
