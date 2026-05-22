from __future__ import annotations
from typing import Any, Dict, List, Optional

from engines.base.retriever import BaseRetriever
from .models import ScoredDocument
from .filters import apply_filters
from .scoring import fuse_scores
from .exceptions import RetrievalError


class KeywordSearchBackend:
    async def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Return list of {id, score, metadata, text}
        """
        raise NotImplementedError


class HybridRetriever(BaseRetriever):
    """
    Combines vector search and keyword search with weighted scoring.
    """

    def __init__(
        self,
        vector_retriever: BaseRetriever,
        keyword_backend: KeywordSearchBackend,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3,
    ) -> None:
        self.vector_retriever = vector_retriever
        self.keyword_backend = keyword_backend
        self.vector_weight = vector_weight
        self.keyword_weight = keyword_weight

    async def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        # Default to hybrid behavior
        return await self.hybrid_search(query, filters=filters, top_k=top_k)

    async def hybrid_search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        if top_k <= 0:
            return []

        # Run vector + keyword in parallel (conceptually; actual parallelism via asyncio.gather)
        from asyncio import gather

        try:
            vec_task = self.vector_retriever.search(query, filters=None, top_k=top_k)
            kw_task = self.keyword_backend.search(query, filters=None, top_k=top_k)
            vec_results, kw_results = await gather(vec_task, kw_task)
        except Exception as e:
            raise RetrievalError(f"Hybrid search failed: {e}") from e

        docs: Dict[str, ScoredDocument] = {}

        for r in vec_results:
            doc_id = r["id"]
            docs[doc_id] = ScoredDocument(
                id=doc_id,
                text=r.get("text", ""),
                vector_score=float(r.get("score", 0.0)),
                metadata=r.get("metadata") or {},
            )

        for r in kw_results:
            doc_id = r["id"]
            if doc_id in docs:
                docs[doc_id].keyword_score = float(r.get("score", 0.0))
            else:
                docs[doc_id] = ScoredDocument(
                    id=doc_id,
                    text=r.get("text", ""),
                    keyword_score=float(r.get("score", 0.0)),
                    metadata=r.get("metadata") or {},
                )

        doc_list = list(docs.values())
        doc_list = apply_filters(doc_list, filters)
        doc_list = fuse_scores(
            doc_list,
            vector_weight=self.vector_weight,
            keyword_weight=self.keyword_weight,
        )

        return [
            {
                "id": d.id,
                "text": d.text,
                "score": d.final_score,
                "metadata": d.metadata,
            }
            for d in doc_list[:top_k]
        ]

    async def fetch_metadata(
        self,
        ids: List[str],
    ) -> List[Dict[str, Any]]:
        # Delegate to underlying vector retriever (which knows metadata store)
        return await self.vector_retriever.fetch_metadata(ids)
