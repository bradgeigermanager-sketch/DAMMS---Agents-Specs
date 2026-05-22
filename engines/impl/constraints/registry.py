from __future__ import annotations
from typing import Any, Callable, Dict, List

from .models import ConstraintViolation

ConstraintFn = Callable[[Dict[str, Any]], List[ConstraintViolation]]


class ConstraintRegistry:
    """
    Simple in-memory registry of constraint functions.
    """

    def __init__(self) -> None:
        self._structural: List[ConstraintFn] = []
        self._domain: List[ConstraintFn] = []
        self._safety: List[ConstraintFn] = []

    def register_structural(self, fn: ConstraintFn) -> None:
        self._structural.append(fn)

    def register_domain(self, fn: ConstraintFn) -> None:
        self._domain.append(fn)

    def register_safety(self, fn: ConstraintFn) -> None:
        self._safety.append(fn)

    @property
    def structural(self) -> List[ConstraintFn]:
        return list(self._structural)

    @property
    def domain(self) -> List[ConstraintFn]:
        return list(self._domain)

    @property
    def safety(self) -> List[ConstraintFn]:
        return list(self._safety)
