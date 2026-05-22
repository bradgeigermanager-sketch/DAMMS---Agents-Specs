# `engines/base/legal_rules.py`

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseLegalRulesEngine(ABC):
    """
    Evaluates legal compliance: jurisdiction, privacy, IP, export controls.
    """

    @abstractmethod
    async def evaluate(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Return structured legal compliance evaluation."""
        raise NotImplementedError

    @abstractmethod
    async def check_jurisdiction(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Apply jurisdiction-specific legal rules."""
        raise NotImplementedError

    @abstractmethod
    async def check_privacy_rules(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Check privacy and data protection constraints."""
        raise NotImplementedError

    @abstractmethod
    async def check_ip_rules(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Check intellectual property and copyright boundaries."""
        raise NotImplementedError
```
