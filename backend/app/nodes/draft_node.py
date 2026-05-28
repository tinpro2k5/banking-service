"""Response generation node using Ollama."""

from __future__ import annotations

import re
from app.clients.base import BaseLLMClient
from app.clients.ollama_client import OllamaClient
from app.core.schemas import DraftResult
import json

_PLACEHOLDER_RE = re.compile(r"\[([^\]]{3,50})\]")


class DraftNode:
    def __init__(self) -> None:
        self.client: BaseLLMClient = OllamaClient()

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
        prompt = f"""You are a banking customer support agent analyzer.
Your task is to draft a reply to the customer and analyze the context.

Current Context:
- Detected intent: {intent}
- Priority level: {priority}
- Relevant policy: {policy}

You MUST respond ONLY with a JSON object matching this schema:
{{
    "draft_reply": "Your polite, concise, and specific banking support reply here",
    "missing_information": "List placeholders inside square brackets like [ACCOUNT_ID] if missing, otherwise null",
    "next_recommended_action": "The next step for the system/agent"
}}
"""
        draft = ""
        missing_info = None
        
        try:
            # 1. Truyền thêm format="json" vào hàm chat
            response_text = self.client.chat([
                {"role": "system", "content": prompt}, 
                {"role": "user", "content": message}
            ], format="json").strip()
            
            # 2. Parse cục JSON mà LLM trả về
            result_json = json.loads(response_text)
            draft = result_json.get("draft_reply", "")
            
            # 3. Lấy missing info trực tiếp từ JSON, nếu có thì mới dùng regex quét nhãn
            raw_missing = result_json.get("missing_information", "")
            if raw_missing and raw_missing != "null":
                missing_info = self._extract_missing_info(raw_missing)

        except Exception:
            draft = self._fallback_draft(message, intent, priority, policy)
            missing_info = self._extract_missing_info(draft)

        # 4. Tính toán next_action dựa trên data đã bóc tách sạch sẽ
        next_action = "request_more_information" if missing_info else "send_reply"
        if priority == "high":
            next_action = "escalate_to_human"
            
        return DraftResult(draft=draft, missing_info=missing_info, next_action=next_action)