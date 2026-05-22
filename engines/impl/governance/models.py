from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class GovernanceDecision:
    action: str  # "allow", "block", "escalate", "modify"
    reason: str
    policies_triggered: List[str]
    risk_level: str  # "low", "medium", "high"
    overrides_applied: List[str]
    metadata: Dict[str, Any]
    user_message: Optional[str] = None
