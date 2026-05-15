"""Policy retrieval node."""

from app.core.schemas import PolicyResult
from app.data.policies import BankingPolicies


class PolicyNode:
    def __init__(self) -> None:
        self._banking_policies = BankingPolicies()

    def run(self, intent: str) -> PolicyResult:
        return PolicyResult(policy_text=self._banking_policies.get_policy(intent))
