from __future__ import annotations
from typing import Any, Dict, List

from engines.base.auditor import BaseKnowledgeAuditor
from .models import AuditReport, AuditIssue
from .conflict_detection import detect_conflicts
from .reliability import score_reliability
from .hallucination import estimate_hallucination_risk
from .scoring import aggregate_answer


class DefaultKnowledgeAuditor(BaseKnowledgeAuditor):
    """
    Production-grade scaffold for knowledge auditing.
    """

    async def audit(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        conflicts = await detect_conflicts(results)
        reliability = await score_reliability(results)
        hallucination_risk = await estimate_hallucination_risk(results)
        answer = await aggregate_answer(results)

        issues = []
        if conflicts:
            issues.append(
                AuditIssue(
                    type="conflict",
                    description="Conflicting information detected.",
                    severity="high",
                )
            )
        if hallucination_risk > 0.5:
            issues.append(
                AuditIssue(
                    type="hallucination",
                    description="High hallucination risk.",
                    severity="medium",
                )
            )

        report = AuditReport(
            answer=answer,
            sources=results,
            issues=issues,
            reliability_score=sum(reliability.values()) / len(reliability)
            if reliability
            else 0.0,
            hallucination_risk=hallucination_risk,
            conflicts=conflicts,
        )

        return report.__dict__

    async def check_conflicts(self, results: List[Dict[str, Any]]) -> List[str]:
        return await detect_conflicts(results)

    async def evaluate_source_reliability(
        self,
        results: List[Dict[str, Any]],
    ) -> Dict[str, float]:
        return await score_reliability(results)

    async def hallucination_risk(
        self,
        results: List[Dict[str, Any]],
    ) -> float:
        return await estimate_hallucination_risk(results)
