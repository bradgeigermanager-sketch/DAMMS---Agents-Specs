from __future__ import annotations
from typing import Any, Dict, List


class LegalRuleSet:
    """
    Simple in-memory legal ruleset.
    Real systems would load these from a policy service.
    """

    def __init__(self, rules: Dict[str, List[Dict[str, Any]]]) -> None:
        self.rules = rules

    def get_rules_for_jurisdiction(self, jurisdiction: str) -> List[Dict[str, Any]]:
        return self.rules.get(jurisdiction, [])


def default_legal_rules() -> LegalRuleSet:
    """
    Example legal rules:
    - EU: strict privacy, data minimization
    - US: export control checks
    - Global: IP boundaries
    """
    return LegalRuleSet(
        rules={
            "EU": [
                {
                    "id": "gdpr_privacy",
                    "check": "privacy",
                    "message": "Personal data processing must comply with GDPR.",
                },
                {
                    "id": "data_minimization",
                    "check": "privacy",
                    "message": "Data minimization required under GDPR.",
                },
            ],
            "US": [
                {
                    "id": "export_control",
                    "check": "export",
                    "message": "Export-controlled content detected.",
                }
            ],
            "GLOBAL": [
                {
                    "id": "ip_protection",
                    "check": "ip",
                    "message": "Potential IP/copyright violation.",
                }
            ],
        }
    )
