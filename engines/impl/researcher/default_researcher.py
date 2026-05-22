from __future__ import annotations
from typing import Any, Dict, List

from engines.base.researcher import BaseWebResearcher
from .models import ResearchSource, ResearchResult
from .exceptions import ResearchError
from .utils import deduplicate_sources, score_sources


class HttpClient:
    """
    Minimal async HTTP client abstraction.
    Plug in aiohttp/httpx/etc. in a real implementation.
    """

    async def get(self, url: str) -> str:
        raise NotImplementedError


class SearchBackend:
    """
    Abstract search backend that returns a list of URLs + titles for a query.
    """

    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, str]]:
        """
        Returns: [{"url": "...", "title": "..."}]
        """
        raise NotImplementedError


class DefaultWebResearcher(BaseWebResearcher):
    """
    Production-grade scaffold for multi-source web research.
    """

    def __init__(
        self,
        http_client: HttpClient,
        search_backend: SearchBackend,
        max_sources: int = 5,
    ) -> None:
        self.http_client = http_client
        self.search_backend = search_backend
        self.max_sources = max_sources

    async def run(self, query: str) -> Dict[str, Any]:
        try:
            raw_sources = await self.fetch_sources(query)
            structured = await self.extract_structured_data(
                [s.__dict__ for s in raw_sources]
            )
            result = ResearchResult(
                query=query,
                sources=raw_sources,
                structured=structured,
            )
            return {
                "query": result.query,
                "sources": [s.__dict__ for s in result.sources],
                "structured": result.structured,
            }
        except Exception as e:
            raise ResearchError(f"Research pipeline failed: {e}") from e

    async def fetch_sources(self, query: str) -> List[Dict[str, Any]]:
        from asyncio import gather

        search_results = await self.search_backend.search(
            query,
            top_k=self.max_sources,
        )

        tasks = []
        for r in search_results:
            url = r["url"]
            title = r.get("title", url)
            tasks.append(self._fetch_single(url, title))

        sources = await gather(*tasks, return_exceptions=True)

        cleaned: List[ResearchSource] = []
        for s in sources:
            if isinstance(s, Exception):
                continue
            cleaned.append(s)

        cleaned = deduplicate_sources(cleaned)
        cleaned = score_sources(cleaned)
        return [s.__dict__ for s in cleaned]

    async def _fetch_single(self, url: str, title: str) -> ResearchSource:
        try:
            content = await self.http_client.get(url)
        except Exception as e:
            raise ResearchError(f"Failed to fetch {url}: {e}") from e

        return ResearchSource(
            url=url,
            title=title,
            content=content,
            score=0.0,
            metadata={},
        )

    async def extract_structured_data(
        self,
        raw: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Very simple structured extraction:
        - returns titles, urls, and first N characters as 'snippets'
        Real implementation would do entity/claim extraction, etc.
        """
        structured_sources = []
        for r in raw:
            content = r.get("content") or ""
            structured_sources.append(
                {
                    "url": r.get("url"),
                    "title": r.get("title"),
                    "snippet": content[:500],
                }
            )

        return {
            "sources": structured_sources,
            "summary": "Structured extraction placeholder. Replace with real NLP pipeline.",
        }
