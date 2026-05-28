"""Abstract client base classes.

This module defines common interfaces for external clients used by the
backend.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional



class BaseLLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError
    def chat(self, messages: list[dict[str, str]]) -> str:
        """Optional method for LLMs that support chat-based interactions."""
        raise NotImplementedError("This LLM client does not support chat interactions.")

@dataclass
class IntentPrediction:
    intent: str
    confidence: Optional[float] = None
    reason: Optional[str] = None

class BaseIntentClient(ABC):
    """Interface for intent prediction clients.
    Implementations should return an `IntentPrediction` instance. 
    """

    @abstractmethod
    def predict(self, message: str) -> IntentPrediction:
        raise NotImplementedError
