from __future__ import annotations
import hashlib
import json
from typing import Any, Dict, List

from engines.base.decision_store import BaseDecisionStore


class InMemoryDecisionStore(BaseDecisionStore):
    """
    Append-only, tamper-evident in-memory decision store.
    Replace with DB-backed implementation in production.
    """

    def __init__(self) -> None:
        self._log: List[Dict[str, Any]] = []
        self._last_hash: str | None = None

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        payload = json.dumps(entry, sort_keys=True).encode("utf-8")
        base = payload + (self._last_hash.encode("utf-8") if self._last_hash else b"")
        return hashlib.sha256(base).hexdigest()

    async def save(self, message: Dict[str, Any], decision: Dict[str, Any]) -> None:
        entry = {
            "message": message,
            "decision": decision,
        }
        entry_hash = self._hash_entry(entry)
        entry["hash"] = entry_hash
        entry["prev_hash"] = self._last_hash
        self._last_hash = entry_hash
        self._log.append(entry)

    async def get_by_trace(self, trace_id: str) -> List[Dict[str, Any]]:
        results = []
        for e in self._log:
            msg = e.get("message") or {}
            if (msg.get("trace_id") or msg.get("trace", {})).get("id") == trace_id:
                results.append(e)
        return results

    async def export_audit_log(self) -> List[Dict[str, Any]]:
        return list(self._log)
