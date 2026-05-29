from __future__ import annotations

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .langchain_adapters import (
    FakeEmbeddings,
    LangChainFaissIndexer,
    LangChainRAGService,
    OfflineContextEchoModel,
)


def build_default_rag() -> tuple[LangChainFaissIndexer, LangChainRAGService]:
    embeddings = FakeEmbeddings(dims=32)
    empty_vs = FAISS.from_texts(texts=["bootstrap"], embedding=embeddings)
    empty_vs.delete([empty_vs.index_to_docstore_id[0]])

    splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=40)
    indexer = LangChainFaissIndexer(splitter=splitter, vector_store=empty_vs)
    rag = LangChainRAGService(vector_store=empty_vs, chat_model=OfflineContextEchoModel())
    return indexer, rag
