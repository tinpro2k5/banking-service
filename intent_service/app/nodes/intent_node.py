"""Intent classifier for the gRPC microservice."""

from __future__ import annotations

import json
import re

from app.clients.ollama_client import OllamaClient
from app.core.schemas import IntentResult
from app.core.settings import settings
from app.data.policies import POLICIES


INTENT_PATTERNS: dict[str, list[str]] = {
    "transfer_not_received_by_recipient": ["transfer not received", "recipient has not received", "missing transfer", "bank transfer not received"],
    "card_not_received": ["card not received", "card hasn't arrived", "card has not arrived", "debit card delivery"],
    "blocked_card": ["blocked card", "card blocked", "frozen card", "security block", "card is blocked"],
    "refund_not_showing_up": ["refund not showing", "refund missing", "refund not arrived", "refund pending"],
    "activate_my_card": ["activate my card", "card activation", "activate card"],
    "card_arrival": ["when will my card arrive", "card delivery", "card arrival", "shipping my card"],
    "card_payment_fee_charged": ["card payment fee", "fee charged", "merchant fee", "charged a fee"],
    "card_payment_not_recognised": ["not recognize this payment", "card payment not recognised", "unknown card payment", "i don't recognize this card payment"],
    "cash_withdrawal_charge": ["atm fee", "cash withdrawal charge", "withdrawal charge", "charged for atm"],
    "pending_card_payment": ["pending card payment", "card payment pending", "pending payment on card"],
    "pending_transfer": ["pending transfer", "transfer pending", "bank transfer pending"],
    "declined_transfer": ["transfer declined", "bank transfer declined", "transfer failed", "transfer was rejected"],
    "declined_card_payment": ["card payment declined", "card declined", "payment was declined"],
    "balance_not_updated_after_bank_transfer": ["balance not updated", "bank transfer balance", "money not reflected after transfer"],
    "cash_withdrawal_not_recognised": ["cash withdrawal not recognised", "atm withdrawal not recognised", "i do not recognize this withdrawal"],
    "card_linking": ["card linking", "link my card", "add my card", "card not linking"],
}


class IntentNode:
    def __init__(self) -> None:
        self._ollama = OllamaClient()

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\s+", " ", text.lower()).strip()

    def _heuristic_classify(self, message: str) -> IntentResult:
        normalized = self._normalize(message)
        best_intent = "unknown_intent"
        best_score = 0.0
        best_reason = "No intent pattern matched."

        for intent, phrases in INTENT_PATTERNS.items():
            for phrase in phrases:
                if phrase in normalized:
                    score = 0.95 if len(phrase.split()) >= 3 else 0.85
                    if score > best_score:
                        best_intent = intent
                        best_score = score
                        best_reason = f"Matched phrase: {phrase}"

        if best_intent == "unknown_intent":
            return IntentResult(intent=best_intent, confidence=0.32, reason=best_reason)

        return IntentResult(intent=best_intent, confidence=best_score, reason=best_reason)

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
        except Exception:
            return self._heuristic_classify(message)

    def run(self, message: str) -> IntentResult:
        if settings.intent_mode.lower() == "ollama":
            try:
                return self._ollama_classify(message)
            except Exception as exc:
                return IntentResult(intent="unknown_intent", confidence=0.0, reason=f"Ollama intent fallback: {exc}")
        return self._heuristic_classify(message)
