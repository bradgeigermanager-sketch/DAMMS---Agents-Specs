from __future__ import annotations
from typing import Any, Dict, List, Optional

from engines.base.retriever import BaseRetriever
from .models import ScoredDocument, RetrievalResult
from .filters import apply_filters
from .exceptions import IndexNotReadyError, RetrievalError


class EmbeddingModel:
    async def embed(self, text: str) -> List[float]:
        raise NotImplementedError

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError


class VectorIndex:
    async def add(
        self,
        ids: List[str],
        vectors: List[List[float]],
        metadata: List[Dict[str, Any]],
    ) -> None:
        raise NotImplementedError

    async def search(
        self,
        vector: List[float],
        top_k: int,
    ) -> List[Dict[str, Any]]:
        """
        Return list of {id, score, metadata, text?}
        """
        raise NotImplementedError

    async def delete(self, ids: List[str]) -> None:
        raise NotImplementedError


class MetadataStore:
    async def get_text(self, doc_id: str) -> str:
        raise NotImplementedError

    async def get_metadata(self, doc_id: str) -> Dict[str, Any]:
        raise NotImplementedError


class VectorRetriever(BaseRetriever):
    """
    Generic vector-based retriever using an embedding model,
    a vector index, and a metadata store.
    """

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        index: VectorIndex,
        metadata_store: MetadataStore,
    ) -> None:
        self.embedding_model = embedding_model
        self.index = index
        self.metadata_store = metadata_store

    async def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        if top_k <= 0:
            return []

        try:
            query_vec = await self.embedding_model.embed(query)
        except Exception as e:
            raise RetrievalError(f"Failed to embed query: {e}") from e

        try:
            raw_results = await self.index.search(query_vec, top_k)
        except Exception as e:
            raise IndexNotReadyError(f"Vector index search failed: {e}") from e

        docs: List[ScoredDocument] = []
        for r in raw_results:
            doc_id = r["id"]
            text = await self.metadata_store.get_text(doc_id)
            metadata = await self.metadata_store.get_metadata(doc_id)
            docs.append(
                ScoredDocument(
                    id=doc_id,
                    text=text,
                    vector_score=float(r.get("score", 0.0)),
                    metadata=metadata or {},
                )
            )

        docs = apply_filters(docs, filters)
        docs.sort(key=lambda d: d.vector_score or 0.0, reverse=True)

        return [
            {
                "id": d.id,
                "text": d.text,
                "score": d.vector_score,
                "metadata": d.metadata,
            }
            for d in docs[:top_k]
        ]

    async def hybrid_search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        # Pure vector retriever doesn't implement hybrid;
        # hybrid is provided by HybridRetriever.
        return await self.search(query, filters=filters, top_k=top_k)

    async def fetch_metadata(
        self,
        ids: List[str],
    ) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for doc_id in ids:
            text = await self.metadata_store.get_text(doc_id)
            metadata = await self.metadata_store.get_metadata(doc_id)
            results.append(
                {
                    "id": doc_id,
                    "text": text,
                    "metadata": metadata,
                }
            )
        return results
