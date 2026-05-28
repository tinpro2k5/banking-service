"""Lightweight validation node for generated responses."""

from __future__ import annotations

from typing import Optional

from app.core.schemas import ValidationResult


class ValidationNode:
    def run(self, draft: str, intent: str, confidence: Optional[float]) -> ValidationResult:
        issues = []
        if len(draft) < 30:
            issues.append("Draft is too short.")
        if confidence is not None and confidence < 0.5:
            issues.append(f"Low intent confidence: {confidence}")
        banking_terms = [
            "account",
            "card",
            "transfer",
            "refund",
            "support",
            "transaction",
            "bank",
            "loan",
            "payment",
            "balance",
            "statement",
            "branch",
            "customer service",
            "banking",
            "credit",
            "debit",
            "withdrawal",
            "deposit",
            "fee",
            "interest",
            "overdraft",
            "suspicious",
            "fraud",
            "bill",
            "charge"
        ]
        if not any(term in draft.lower() for term in banking_terms):
            issues.append("Draft may lack banking-specific content.")
        valid = len(issues) == 0
        return ValidationResult(valid=valid, issues="; ".join(issues) if issues else None)
