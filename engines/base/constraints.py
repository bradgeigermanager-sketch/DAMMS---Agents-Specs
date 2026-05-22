# `engines/base/constraints.py`

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseConstraintSet(ABC):
    """
    Evaluates structural, domain, and safety constraints.
    """

    @abstractmethod
    async def check(self, message: Dict[str, Any]) -> List[str]:
        """Run all constraints and return violations."""
        raise NotImplementedError

    @abstractmethod
    async def check_structure(self, message: Dict[str, Any]) -> List[str]:
        """Check formatting, length, and structural rules."""
        raise NotImplementedError

    @abstractmethod
    async def check_domain_rules(self, message: Dict[str, Any]) -> List[str]:
        """Check domain-specific constraints."""
        raise NotImplementedError

    @abstractmethod
    async def check_safety_constraints(self, message: Dict[str, Any]) -> List[str]:
        """Check safety-related constraints."""
        raise NotImplementedError
```
