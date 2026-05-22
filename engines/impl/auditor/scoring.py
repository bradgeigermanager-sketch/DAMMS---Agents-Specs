from __future__ import annotations
from typing import Dict, List


async def aggregate_answer(results: List[Dict[str, any]]) -> str:
    """
    Simple answer synthesis:
    - picks the most common answer
    - real implementation would use LLM summarization
    """
    answers = {}
    for r in results:
        a = r.get("answer")
        if not a:
            continue
        answers[a] = answers.get(a, 0) + 1

    if not answers:
        return "No answer available."

    return max(answers.items(), key=lambda x: x[1])[0]
