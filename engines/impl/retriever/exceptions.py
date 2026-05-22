from __future__ import annotations


class RetrievalError(Exception):
    """Generic retrieval failure."""


class IndexNotReadyError(RetrievalError):
    """Raised when the vector index is not initialized or ready."""


class ToolExecutionError(RetrievalError):
    """Raised when a retrieval tool fails or returns invalid data."""
