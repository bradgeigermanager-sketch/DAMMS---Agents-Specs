from __future__ import annotations
from typing import Any, Dict, List

from engines.base.governance_rules import BaseGovernanceRulesEngine
from .models import GovernanceDecision
from .policies import PolicyBundle, default_policy_bundle
from .exceptions import GovernanceError


class RulesMatcher:
    @staticmethod
    def matches(rule: Dict[str, Any], message: Dict[str, Any]) -> bool:
        match = rule.get("match", {})
        ctx = message.get("policy_context", {}) or {}
        for key, expected in match.items():
            if ctx.get(key) != expected:
                return False
        return True


class GovernanceRulesEngine(BaseGovernanceRulesEngine):
    """
    Production-grade scaffold for governance rules evaluation.
    """

    def __init__(self, policies: PolicyBundle | None = None) -> None:
        self.policies = policies or default_policy_bundle()

    async def evaluate(self, message: Dict[str, Any]) -> Dict[str, Any]:
        try:
            decision = await self._evaluate_internal(message)
        except Exception as e:
            raise GovernanceError(f"Governance evaluation failed: {e}") from e
        return decision.__dict__

    async def _evaluate_internal(
        self,
        message: Dict[str, Any],
    ) -> GovernanceDecision:
        base_decision = GovernanceDecision(
            action="allow",
            reason="No blocking policies triggered.",
            policies_triggered=[],
            risk_level=(message.get("policy_context") or {}).get("risk_level", "low"),
            overrides_applied=[],
            metadata={},
        )

        base_decision = await self.apply_escalation_rules(message, base_decision)
        base_decision = await self.apply_jurisdictional_rules(message, base_decision)
        base_decision = await self.apply_override_logic(message, base_decision)

        return base_decision

    async def apply_escalation_rules(
        self,
        message: Dict[str, Any],
        decision: GovernanceDecision | None = None,
    ) -> GovernanceDecision:
        if decision is None:
            decision = GovernanceDecision(
                action="allow",
                reason="",
                policies_triggered=[],
                risk_level=(message.get("policy_context") or {}).get(
                    "risk_level", "low"
                ),
                overrides_applied=[],
                metadata={},
            )

        rules = self.policies.get_rules()
        ctx = message.get("policy_context") or {}
        risk_level = ctx.get("risk_level", "low")

        for r in rules:
            if not RulesMatcher.matches(r, {"policy_context": {"risk_level": risk_level}}):
                continue
            decision.policies_triggered.append(r["id"])
            decision.action = r["action"]
            decision.reason = r["reason"]

        return decision

    async def apply_jurisdictional_rules(
        self,
        message: Dict[str, Any],
        decision: GovernanceDecision,
    ) -> GovernanceDecision:
        jurisdiction = (message.get("policy_context") or {}).get("jurisdiction")
        if jurisdiction == "EU":
            decision.metadata.setdefault("jurisdictional_notes", []).append(
                "EU-specific governance rules applied."
            )
        return decision

    async def apply_override_logic(
        self,
        message: Dict[str, Any],
        decision: GovernanceDecision,
    ) -> GovernanceDecision:
        safety_override = (message.get("policy_context") or {}).get(
            "safety_override", False
        )
        if safety_override and decision.action == "allow":
            decision.action = "escalate"
            decision.overrides_applied.append("safety_override")
            decision.reason = "Safety override forced escalation."
        return decision
