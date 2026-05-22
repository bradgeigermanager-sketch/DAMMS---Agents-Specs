from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class RetrievedDocument:
    id: str
    text: str
    score: float
    metadata: Dict[str, Any]


@dataclass
class ScoredDocument:
    id: str
    text: str
    vector_score: Optional[float] = None
    keyword_score: Optional[float] = None
    final_score: Optional[float] = None
    metadata: Dict[str, Any] = None


@dataclass
class RetrievalResult:
    query: str
    documents: List[ScoredDocument]
    used_hybrid: bool = False
    filters_applied: Optional[Dict[str, Any]] = None
