# `engines/base/governance_rules.py`

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseGovernanceRulesEngine(ABC):
    """
    Evaluates messages against governance policies, escalation rules,
    jurisdictional constraints, and override logic.
    """

    @abstractmethod
    async def evaluate(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Return a structured governance decision."""
        raise NotImplementedError

    @abstractmethod
    async def apply_escalation_rules(
        self,
        message: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Apply escalation logic based on risk and content."""
        raise NotImplementedError

    @abstractmethod
    async def apply_jurisdictional_rules(
        self,
        message: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Apply region-specific legal/governance constraints."""
        raise NotImplementedError

    @abstractmethod
    async def apply_override_logic(
        self,
        message: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Apply override rules (e.g., safety > user intent)."""
        raise NotImplementedError
```
