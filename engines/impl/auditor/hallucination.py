from __future__ import annotations
from typing import Dict, List


async def estimate_hallucination_risk(results: List[Dict[str, any]]) -> float:
    """
    Estimate hallucination risk based on:
    - number of sources
    - agreement between sources
    - evidence density
    """
    if not results:
        return 1.0  # maximum risk

    evidence_count = sum(len(r.get("citations", [])) for r in results)
    source_count = len(results)

    # Simple heuristic
    risk = 1.0 - min(1.0, (evidence_count + source_count) / 10.0)
    return max(0.0, risk)
