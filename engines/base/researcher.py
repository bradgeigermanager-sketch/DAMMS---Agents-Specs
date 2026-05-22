# `engines/base/researcher.py`

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseWebResearcher(ABC):
    """
    Multi-source research engine with parallel fetch, deduplication,
    structured extraction, and source scoring.
    """

    @abstractmethod
    async def run(self, query: str) -> Dict[str, Any]:
        """Run the full research pipeline."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_sources(self, query: str) -> List[Dict[str, Any]]:
        """Fetch raw data from multiple sources."""
        raise NotImplementedError

    @abstractmethod
    async def extract_structured_data(
        self,
        raw: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Extract structured information from raw documents."""
        raise NotImplementedError
```
