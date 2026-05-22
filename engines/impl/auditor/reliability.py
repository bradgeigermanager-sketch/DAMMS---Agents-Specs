from __future__ import annotations
from typing import Dict, List


async def score_reliability(results: List[Dict[str, any]]) -> Dict[str, float]:
    """
    Assigns reliability scores based on:
    - source type
    - citation density
    - metadata quality
    - recency
    """
    scores = {}

    for r in results:
        base = 0.5
        meta = r.get("metadata", {})

        if meta.get("source_type") == "official":
            base += 0.3
        if meta.get("citations"):
            base += 0.1
        if meta.get("year") and meta["year"] >= 2020:
            base += 0.1

        scores[r["id"]] = min(base, 1.0)

    return scores
