"""Pydantic schemas shared by the API gateway.
Used in multiple nodes and the main API handler"
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class CustomerRequest(BaseModel):
    message: str = Field(min_length=1)


class IntentResult(BaseModel):
    intent: str
    confidence: Optional[float] = None
    reason: Optional[str] = None


class PriorityResult(BaseModel):
    level: Literal["low", "medium", "high"]
    reason: str


class PolicyResult(BaseModel):
    policy_text: str


class DraftResult(BaseModel):
    draft: str
    missing_info: Optional[str] = None
    next_action: Optional[str] = None


class ValidationResult(BaseModel):
    valid: bool
    issues: Optional[str] = None


class RouterResult(BaseModel):
    action: Literal["reply", "ask_more", "escalate"]
    reason: str


class SystemConfig(BaseModel):
    api_host: str
    api_port: int
    intent_service_host: str
    intent_service_port: int
    intent_service_timeout: float
    ollama_base_url: str
    ollama_model: str
    frontend_base_url: str


class AgentResponse(BaseModel):
    intent: IntentResult
    priority: PriorityResult
    policy: PolicyResult
    draft: DraftResult
    validation: ValidationResult
    routing: RouterResult
    final_reply: str
