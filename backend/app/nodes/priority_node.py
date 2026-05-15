"""Rule-based priority scoring node."""

from app.core.schemas import PriorityResult


HIGH_PRIORITY_KEYWORDS = [
    "fraud",
    "stolen",
    "unauthorized",
    "blocked",
    "lost",
    "scam",
    "hack",
    "compromised",
    "security",
    "urgent",
]
MEDIUM_PRIORITY_KEYWORDS = [
    "not received",
    "failed",
    "error",
    "wrong amount",
    "refund",
    "dispute",
    "delay",
    "issue",
    "problem",
    "help",
    "support",
]


class PriorityNode:
    def run(self, message: str, intent: str) -> PriorityResult:
        msg = message.lower()
        if any(keyword in msg for keyword in HIGH_PRIORITY_KEYWORDS):
            return PriorityResult(level="high", reason="Message contains urgent or security-related keywords.")
        if any(keyword in msg for keyword in MEDIUM_PRIORITY_KEYWORDS):
            return PriorityResult(level="medium", reason="Message indicates a transaction-related issue.")
        if intent in {"blocked_card", "card_payment_not_recognised", "cash_withdrawal_not_recognised"}:
            return PriorityResult(level="high", reason="Intent suggests a potentially risky banking issue.")
        return PriorityResult(level="low", reason="Routine inquiry.")
