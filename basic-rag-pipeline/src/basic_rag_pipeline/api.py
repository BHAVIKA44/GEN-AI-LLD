from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .factory import build_default_rag


class IngestRequest(BaseModel):
    texts: list[str] = Field(default_factory=list)


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


def create_app() -> FastAPI:
    app = FastAPI(title="Basic RAG Pipeline")
    indexer, rag = build_default_rag()

    @app.post("/ingest")
    def ingest(req: IngestRequest) -> dict[str, int]:
        return {"indexed_chunks": indexer.index_texts(req.texts)}

    @app.post("/answer")
    def answer(req: QueryRequest) -> dict:
        result = rag.answer(req.query, req.top_k)
        return {
            "answer": result.answer,
            "sources": [{"content": s.content, "score": s.score} for s in result.sources],
        }

    return app
