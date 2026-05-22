# `engines/base/retriever.py`

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseRetriever(ABC):
    """
    Abstract interface for retrieval engines.
    Supports vector search, hybrid search, metadata filtering,
    and multi-source retrieval pipelines.
    """

    @abstractmethod
    async def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        """Perform semantic or keyword search and return ranked results."""
        raise NotImplementedError

    @abstractmethod
    async def hybrid_search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        """Combine vector + keyword search with scoring and reranking."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_metadata(
        self,
        ids: List[str],
    ) -> List[Dict[str, Any]]:
        """Fetch metadata for retrieved items."""
        raise NotImplementedError
```

