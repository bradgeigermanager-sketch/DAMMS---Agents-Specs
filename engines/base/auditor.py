# `engines/base/auditor.py`

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseKnowledgeAuditor(ABC):
    """
    Evaluates retrieved knowledge for reliability, conflicts,
    hallucination risk, and DAMMS governance compliance.
    """

    @abstractmethod
    async def audit(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run the full audit pipeline and return a structured report."""
        raise NotImplementedError

    @abstractmethod
    async def check_conflicts(self, results: List[Dict[str, Any]]) -> List[str]:
        """Detect contradictions or inconsistencies across sources."""
        raise NotImplementedError

    @abstractmethod
    async def evaluate_source_reliability(
        self,
        results: List[Dict[str, Any]],
    ) -> Dict[str, float]:
        """Score each source for reliability."""
        raise NotImplementedError

    @abstractmethod
    async def hallucination_risk(
        self,
        results: List[Dict[str, Any]],
    ) -> float:
        """Estimate hallucination risk based on evidence density."""
        raise NotImplementedError
```
