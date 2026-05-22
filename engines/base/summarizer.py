# `engines/base/summarizer.py`

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseSummarizer(ABC):
    """
    Multi-document summarization, abstraction, compression,
    and citation-preserving synthesis.
    """

    @abstractmethod
    async def summarize(self, raw_documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Produce a concise summary with citations."""
        raise NotImplementedError

    @abstractmethod
    async def abstract(self, raw_documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Produce a higher-level abstraction."""
        raise NotImplementedError

    @abstractmethod
    async def compress(self, raw_documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Produce a compressed version preserving key facts."""
        raise NotImplementedError
```
