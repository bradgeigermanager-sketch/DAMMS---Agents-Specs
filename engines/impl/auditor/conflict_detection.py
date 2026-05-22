from __future__ import annotations
from typing import Dict, List


async def detect_conflicts(results: List[Dict[str, any]]) -> List[str]:
    """
    Simple conflict detection:
    - looks for contradictory claims in metadata or extracted fields
    - real implementation would use claim extraction + contradiction models
    """
    conflicts = []
    seen_claims = {}

    for r in results:
        claims = r.get("claims", [])
        for c in claims:
            key = c.get("property")
            value = c.get("value")
            if key in seen_claims and seen_claims[key] != value:
                conflicts.append(
                    f"Conflict on '{key}': '{seen_claims[key]}' vs '{value}'"
                )
            else:
                seen_claims[key] = value

    return conflicts
