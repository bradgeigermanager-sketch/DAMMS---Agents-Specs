from __future__ import annotations
from typing import Any, Dict, List


class PolicyBundle:
    """
    Simple in-memory policy bundle.
    In a real system this would be loaded from config / policy service.
    """

    def __init__(self, rules: List[Dict[str, Any]]) -> None:
        self.rules = rules

    def get_rules(self) -> List[Dict[str, Any]]:
        return self.rules


def default_policy_bundle() -> PolicyBundle:
    """
    Example policy set:
    - high-risk content -> escalate or block
    - jurisdictional constraints
    """
    rules = [
        {
            "id": "block_explicit_harm",
            "match": {"risk_level": "high"},
            "action": "block",
            "reason": "High-risk content not allowed.",
        },
        {
            "id": "escalate_medium_risk",
            "match": {"risk_level": "medium"},
            "action": "escalate",
            "reason": "Medium-risk content requires escalation.",
        },
    ]
    return PolicyBundle(rules)
