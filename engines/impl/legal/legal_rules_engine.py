from __future__ import annotations
from typing import Any, Dict, List

from engines.base.legal_rules import BaseLegalRulesEngine
from .models import LegalEvaluation
from .rulesets import LegalRuleSet, default_legal_rules
from .exceptions import LegalEvaluationError


class LegalRulesEngine(BaseLegalRulesEngine):
    """
    Production-grade scaffold for legal compliance evaluation.
    """

    def __init__(self, ruleset: LegalRuleSet | None = None) -> None:
        self.ruleset = ruleset or default_legal_rules()

    async def evaluate(self, message: Dict[str, Any]) -> Dict[str, Any]:
        try:
            jurisdiction = (message.get("policy_context") or {}).get(
                "jurisdiction", "GLOBAL"
            )
            violations = []

            violations.extend(await self.check_jurisdiction(message))
            violations.extend(await self.check_privacy_rules(message))
            violations.extend(await self.check_ip_rules(message))

            compliant = len(violations) == 0

            evaluation = LegalEvaluation(
                compliant=compliant,
                violations=violations,
                jurisdiction=jurisdiction,
                metadata={},
            )
            return evaluation.__dict__

        except Exception as e:
            raise LegalEvaluationError(f"Legal evaluation failed: {e}") from e

    async def check_jurisdiction(self, message: Dict[str, Any]) -> List[str]:
        jurisdiction = (message.get("policy_context") or {}).get(
            "jurisdiction", "GLOBAL"
        )
        rules = self.ruleset.get_rules_for_jurisdiction(jurisdiction)
        violations = []

        for r in rules:
            if r["check"] == "privacy":
                # Privacy checks handled separately
                continue
            if r["check"] == "export":
                if (message.get("content") or "").lower().count("restricted") > 0:
                    violations.append(r["message"])

        return violations

    async def check_privacy_rules(self, message: Dict[str, Any]) -> List[str]:
        content = message.get("content") or ""
        violations = []

        # Simple heuristic: detect personal data patterns
        if any(token in content.lower() for token in ["ssn", "passport", "address"]):
            violations.append("Potential personal data detected.")

        # Apply jurisdictional privacy rules
        jurisdiction = (message.get("policy_context") or {}).get(
            "jurisdiction", "GLOBAL"
        )
        rules = self.ruleset.get_rules_for_jurisdiction(jurisdiction)

        for r in rules:
            if r["check"] == "privacy":
                violations.append(r["message"])

        return violations

    async def check_ip_rules(self, message: Dict[str, Any]) -> List[str]:
        content = message.get("content") or ""
        violations = []

        # Simple heuristic: detect copyrighted content patterns
        if "©" in content or "all rights reserved" in content.lower():
            violations.append("Possible copyrighted material detected.")

        # Apply global IP rules
        global_rules = self.ruleset.get_rules_for_jurisdiction("GLOBAL")
        for r in global_rules:
            if r["check"] == "ip":
                violations.append(r["message"])

        return violations
