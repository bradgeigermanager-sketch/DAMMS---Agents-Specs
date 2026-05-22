from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ConstraintViolation:
    code: str
    message: str
    severity: str  # "low", "medium", "high"
    details: Dict[str, Any]
