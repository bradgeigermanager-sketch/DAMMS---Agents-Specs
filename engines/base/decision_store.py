# `engines/base/decision_store.py`

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseDecisionStore(ABC):
    """
    Persistent, tamper-evident audit log for governance decisions.
    """

    @abstractmethod
    async def save(self, message: Dict[str, Any], decision: Dict[str, Any]) -> None:
        """Append a governance decision to the audit log."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_trace(self, trace_id: str) -> List[Dict[str, Any]]:
        """Retrieve all decisions associated with a causal trace."""
        raise NotImplementedError

    @abstractmethod
    async def export_audit_log(self) -> List[Dict[str, Any]]:
        """Export the full audit log for compliance."""
        raise NotImplementedError
```
