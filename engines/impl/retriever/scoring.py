from __future__ import annotations
from typing import List
from .models import ScoredDocument


def normalize_scores(scores: List[float]) -> List[float]:
    if not scores:
        return []
    max_s = max(scores)
    min_s = min(scores)
    if max_s == min_s:
        return [1.0 for _ in scores]
    return [(s - min_s) / (max_s - min_s) for s in scores]


def fuse_scores(
    docs: List[ScoredDocument],
    vector_weight: float = 0.7,
    keyword_weight: float = 0.3,
) -> List[ScoredDocument]:
    v_scores = [d.vector_score or 0.0 for d in docs]
    k_scores = [d.keyword_score or 0.0 for d in docs]

    v_norm = normalize_scores(v_scores)
    k_norm = normalize_scores(k_scores)

    for d, vs, ks in zip(docs, v_norm, k_norm):
        d.final_score = vector_weight * vs + keyword_weight * ks

    docs.sort(key=lambda d: d.final_score or 0.0, reverse=True)
    return docs
