"""Response generation node using Ollama."""

from __future__ import annotations

import re

from app.clients.ollama_client import OllamaClient
from app.core.schemas import DraftResult


_PLACEHOLDER_RE = re.compile(r"\[([^\]]{3,50})\]")


class DraftNode:
    def __init__(self) -> None:
        self.client = OllamaClient()

    @staticmethod
    def _extract_missing_info(draft: str) -> str | None:
        matches = _PLACEHOLDER_RE.findall(draft)
        if not matches:
            return None
        seen: set[str] = set()
        unique = [item for item in matches if not (item in seen or seen.add(item))]
        return "Missing: " + ", ".join(unique)

    @staticmethod
    def _fallback_draft(message: str, intent: str, priority: str, policy: str) -> str:
        return (
            f"Thank you for reaching out about {intent.replace('_', ' ')}. "
            f"Based on our policy: {policy} "
            f"We have marked this as a {priority} priority case and will continue with the request for: {message}"
        )

    def run(self, message: str, intent: str, priority: str, policy: str) -> DraftResult:
        prompt = f"""You are a banking customer support agent.

Customer message: {message}
Detected intent: {intent}
Priority level: {priority}
Relevant policy: {policy}

Return the answer using these labels:
Draft reply:
Missing information:
Next recommended action:

Keep the response concise, polite, and specific to banking support. If no extra information is needed, write None under Missing information.
"""
        try:
            draft = self.client.generate(prompt).strip()
        except Exception:
            draft = self._fallback_draft(message, intent, priority, policy)

        missing_info = self._extract_missing_info(draft)
        next_action = "request_more_information" if missing_info else "send_reply"
        if priority == "high":
            next_action = "escalate_to_human"
        return DraftResult(draft=draft, missing_info=missing_info, next_action=next_action)
