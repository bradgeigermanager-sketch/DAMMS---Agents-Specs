from __future__ import annotations
from typing import Any, Dict, List, Callable
from .models import ScoredDocument


FilterFn = Callable[[ScoredDocument], bool]


def apply_filters(
    docs: List[ScoredDocument],
    filters: Dict[str, Any] | None,
) -> List[ScoredDocument]:
    if not filters:
        return docs

    fns: List[FilterFn] = []

    for key, value in filters.items():
        if isinstance(value, dict) and "min" in value or "max" in value:
            fns.append(_range_filter(key, value))
        else:
            fns.append(_equals_filter(key, value))

    result = []
    for doc in docs:
        if all(fn(doc) for fn in fns):
            result.append(doc)
    return result


def _equals_filter(field: str, expected: Any) -> FilterFn:
    def _fn(doc: ScoredDocument) -> bool:
        return doc.metadata and doc.metadata.get(field) == expected
    return _fn


def _range_filter(field: str, spec: Dict[str, Any]) -> FilterFn:
    min_v = spec.get("min")
    max_v = spec.get("max")

    def _fn(doc: ScoredDocument) -> bool:
        if not doc.metadata or field not in doc.metadata:
            return False
        value = doc.metadata[field]
        if min_v is not None and value < min_v:
            return False
        if max_v is not None and value > max_v:
            return False
        return True

    return _fn
