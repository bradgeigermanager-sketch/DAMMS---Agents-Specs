# `engines/base/memory_store.py`

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseMemoryStore(ABC):
    """
    Long-term memory backend with vector + metadata storage,
    retention policies, and governance compliance.
    """

    @abstractmethod
    async def store(self, payload: Dict[str, Any]) -> str:
        """Store memory and return a unique key."""
        raise NotImplementedError

    @abstractmethod
    async def retrieve(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve memory by key."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete memory by key."""
        raise NotImplementedError

    @abstractmethod
    async def search(self, query: str) -> List[Dict[str, Any]]:
        """Semantic search over stored memories."""
        raise NotImplementedError
```
