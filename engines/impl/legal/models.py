from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class LegalEvaluation:
    compliant: bool
    violations: List[str]
    jurisdiction: str
    metadata: Dict[str, Any]
