from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ResearchSource:
    url: str
    title: str
    content: str
    score: float
    metadata: Dict[str, Any]


@dataclass
class ResearchResult:
    query: str
    sources: List[ResearchSource]
    structured: Dict[str, Any]
