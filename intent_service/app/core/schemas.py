"""Schemas for the intent service internals."""

from pydantic import BaseModel


class IntentResult(BaseModel):
    intent: str
    confidence: float
    reason: str
