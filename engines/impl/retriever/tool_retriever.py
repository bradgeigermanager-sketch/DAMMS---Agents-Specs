from __future__ import annotations
from typing import Any, Dict, List, Optional, Callable, Awaitable

from engines.base.retriever import BaseRetriever
from .exceptions import ToolExecutionError


ToolFn = Callable[[str, Optional[Dict[str, Any]], int], Awaitable[List[Dict[str, Any]]]]


class ToolRetriever(BaseRetriever):
    """
    Retriever that delegates to external tools (APIs, search engines, etc.).
    Tools must conform to a simple async interface.
    """

    def __init__(self, tools: Dict[str, ToolFn], default_tool: str) -> None:
        self.tools = tools
        self.default_tool = default_tool

    async def _run_tool(
        self,
        tool_name: str,
        query: str,
        filters: Optional[Dict[str, Any]],
        top_k: int,
    ) -> List[Dict[str, Any]]:
        if tool_name not in self.tools:
            raise ToolExecutionError(f"Unknown retrieval tool: {tool_name}")
        tool = self.tools[tool_name]
        try:
            return await tool(query, filters, top_k)
        except Exception as e:
            raise ToolExecutionError(f"Tool {tool_name} failed: {e}") from e

    async def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        return await self._run_tool(self.default_tool, query, filters, top_k)

    async def hybrid_search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        # For tool-based retriever, hybrid can mean using a specific hybrid-capable tool
        return await self._run_tool(self.default_tool, query, filters, top_k)

    async def fetch_metadata(
        self,
        ids: List[str],
    ) -> List[Dict[str, Any]]:
        # Tool-based retriever may not support metadata fetch; leave as no-op or override per tool.
        return []
