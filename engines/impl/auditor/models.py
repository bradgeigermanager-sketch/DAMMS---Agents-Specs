from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class AuditIssue:
    type: str
    description: str
    severity: str  # low, medium, high


@dataclass
class AuditReport:
    answer: str
    sources: List[Dict[str, Any]]
    issues: List[AuditIssue]
    reliability_score: float
    hallucination_risk: float
    conflicts: List[str]
