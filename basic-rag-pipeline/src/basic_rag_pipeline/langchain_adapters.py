from __future__ import annotations

from dataclasses import dataclass

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .interfaces import KnowledgeIndexer, QueryAnsweringService
from .models import RAGResult, SourceChunk


class FakeEmbeddings(Embeddings):
    def __init__(self, dims: int = 24) -> None:
        self._dims = dims

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        vec = [0.0] * self._dims
        for i, ch in enumerate(text.lower()):
            vec[i % self._dims] += (ord(ch) % 29) / 29.0
        norm = sum(v * v for v in vec) ** 0.5
        return vec if norm == 0 else [v / norm for v in vec]


class OfflineContextEchoModel(BaseChatModel):
    @property
    def _llm_type(self) -> str:
        return "offline-context-echo"

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        text = "\n".join(getattr(m, "content", "") for m in messages)
        marker = "CONTEXT:\n"
        if marker in text:
            context = text.split(marker, 1)[1].strip()
            answer = context.split("\n\n", 1)[0] if context else "I don't have enough context to answer that."
        else:
            answer = "I don't have enough context to answer that."
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=answer))])


@dataclass
class LangChainFaissIndexer(KnowledgeIndexer):
    splitter: RecursiveCharacterTextSplitter
    vector_store: FAISS

    def index_texts(self, texts: list[str]) -> int:
        docs = [Document(page_content=t) for t in texts if t.strip()]
        split_docs = self.splitter.split_documents(docs)
        if split_docs:
            self.vector_store.add_documents(split_docs)
        return len(split_docs)


@dataclass
class LangChainRAGService(QueryAnsweringService):
    vector_store: FAISS
    chat_model: BaseChatModel

    def answer(self, query: str, top_k: int = 3) -> RAGResult:
        if not query.strip():
            raise ValueError("query must not be empty")
        if top_k <= 0:
            raise ValueError("top_k must be > 0")

        hits = self.vector_store.similarity_search_with_score(query, k=top_k)
        sources = [SourceChunk(content=doc.page_content, score=float(score)) for doc, score in hits]

        context = "\n\n".join(s.content for s in sources)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Answer only from provided context; if context missing, say insufficient context."),
                ("human", "QUESTION:\n{question}\n\nCONTEXT:\n{context}"),
            ]
        )
        messages = prompt.format_messages(question=query, context=context)
        answer = self.chat_model.invoke(messages).content
        return RAGResult(answer=answer, sources=sources)
