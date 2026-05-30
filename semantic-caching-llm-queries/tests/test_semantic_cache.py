from semantic_caching_llm_queries.cache import InMemorySemanticCache
from semantic_caching_llm_queries.embeddings import FakeEmbeddings
from semantic_caching_llm_queries.models import LLMAnswer, LLMQuery
from semantic_caching_llm_queries.service import SemanticCachedLLMService


class FakeLLM:
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, query: LLMQuery) -> LLMAnswer:
        self.calls += 1
        return LLMAnswer(text=f"resp:{query.text}")


class FakeClock:
    def __init__(self) -> None:
        self.now_val = 100.0

    def now(self) -> float:
        return self.now_val

    def advance(self, sec: float) -> None:
        self.now_val += sec


def test_semantic_hit_for_similar_query() -> None:
    llm = FakeLLM()
    emb = FakeEmbeddings()
    cache = InMemorySemanticCache(similarity_threshold=0.9)
    svc = SemanticCachedLLMService(llm, emb, cache, ttl_seconds=60)

    r1, h1 = svc.generate(LLMQuery(text="What is semantic caching", model="m1"))
    r2, h2 = svc.generate(LLMQuery(text="what is semantic caching?", model="m1"))

    assert h1 is False
    assert h2 is True
    assert r1.text == r2.text
    assert llm.calls == 1


def test_model_isolation_prevents_cross_model_hit() -> None:
    llm = FakeLLM()
    emb = FakeEmbeddings()
    cache = InMemorySemanticCache(similarity_threshold=0.8)
    svc = SemanticCachedLLMService(llm, emb, cache, ttl_seconds=60)

    svc.generate(LLMQuery(text="Tell me about vectors", model="m1"))
    _, hit = svc.generate(LLMQuery(text="Tell me about vectors", model="m2"))

    assert hit is False
    assert llm.calls == 2


def test_ttl_expiry() -> None:
    clock = FakeClock()
    llm = FakeLLM()
    emb = FakeEmbeddings()
    cache = InMemorySemanticCache(similarity_threshold=0.8, now_fn=clock.now)
    svc = SemanticCachedLLMService(llm, emb, cache, ttl_seconds=5)

    svc.generate(LLMQuery(text="Explain cosine similarity", model="m1"))
    clock.advance(6)
    _, hit = svc.generate(LLMQuery(text="Explain cosine similarity", model="m1"))

    assert hit is False
    assert llm.calls == 2
