from __future__ import annotations
from typing import Any, Dict, List

from engines.base.constraints import BaseConstraintSet
from .registry import ConstraintRegistry, ConstraintFn
from .models import ConstraintViolation
from .exceptions import ConstraintError


def _length_constraint(max_chars: int) -> ConstraintFn:
    def _fn(message: Dict[str, Any]) -> List[ConstraintViolation]:
        content = (message.get("content") or "").strip()
        if len(content) <= max_chars:
            return []
        return [
            ConstraintViolation(
                code="length_exceeded",
                message=f"Content exceeds maximum length of {max_chars} characters.",
                severity="medium",
                details={"max_chars": max_chars, "actual": len(content)},
            )
        ]
    return _fn


def _required_field(field: str) -> ConstraintFn:
    def _fn(message: Dict[str, Any]) -> List[ConstraintViolation]:
        if field in message and message[field] not in (None, ""):
            return []
        return [
            ConstraintViolation(
                code="missing_field",
                message=f"Required field '{field}' is missing.",
                severity="high",
                details={"field": field},
            )
        ]
    return _fn


class DefaultConstraintSet(BaseConstraintSet):
    """
    Production-grade scaffold for constraint evaluation.
    """

    def __init__(self, registry: ConstraintRegistry | None = None) -> None:
        self.registry = registry or self._build_default_registry()

    def _build_default_registry(self) -> ConstraintRegistry:
        reg = ConstraintRegistry()
        reg.register_structural(_length_constraint(8000))
        reg.register_structural(_required_field("content"))
        return reg

    async def check(self, message: Dict[str, Any]) -> List[str]:
        try:
            violations: List[ConstraintViolation] = []
            violations.extend(await self._run_group(self.registry.structural, message))
            violations.extend(await self._run_group(self.registry.domain, message))
            violations.extend(await self._run_group(self.registry.safety, message))
        except Exception as e:
            raise ConstraintError(f"Constraint evaluation failed: {e}") from e

        return [v.message for v in violations]

    async def check_structure(self, message: Dict[str, Any]) -> List[str]:
        violations = await self._run_group(self.registry.structural, message)
        return [v.message for v in violations]

    async def check_domain_rules(self, message: Dict[str, Any]) -> List[str]:
        violations = await self._run_group(self.registry.domain, message)
        return [v.message for v in violations]

    async def check_safety_constraints(self, message: Dict[str, Any]) -> List[str]:
        violations = await self._run_group(self.registry.safety, message)
        return [v.message for v in violations]

    async def _run_group(
        self,
        fns: List[ConstraintFn],
        message: Dict[str, Any],
    ) -> List[ConstraintViolation]:
        all_violations: List[ConstraintViolation] = []
        for fn in fns:
            v = fn(message)
            if v:
                all_violations.extend(v)
        return all_violations
