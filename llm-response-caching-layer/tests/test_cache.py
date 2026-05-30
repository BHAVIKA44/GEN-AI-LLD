from llm_response_caching_layer.cache import InMemoryTTLCache
from llm_response_caching_layer.models import LLMRequest, LLMResponse
from llm_response_caching_layer.service import CachedLLMService


class FakeProvider:
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, request: LLMRequest) -> LLMResponse:
        self.calls += 1
        return LLMResponse(text=f"answer:{request.prompt}")


class FakeClock:
    def __init__(self) -> None:
        self.t = 1000.0

    def now(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


def test_cache_hit_avoids_provider_call() -> None:
    provider = FakeProvider()
    clock = FakeClock()
    cache = InMemoryTTLCache(now_fn=clock.now)
    service = CachedLLMService(provider=provider, cache=cache, ttl_seconds=60)

    req = LLMRequest(prompt="hello", model="gpt-test", temperature=0.1)
    r1, hit1 = service.generate(req)
    r2, hit2 = service.generate(req)

    assert hit1 is False
    assert hit2 is True
    assert r1.text == r2.text
    assert provider.calls == 1


def test_cache_expires_after_ttl() -> None:
    provider = FakeProvider()
    clock = FakeClock()
    cache = InMemoryTTLCache(now_fn=clock.now)
    service = CachedLLMService(provider=provider, cache=cache, ttl_seconds=10)

    req = LLMRequest(prompt="who are you", model="gpt-test")
    service.generate(req)
    clock.advance(11)
    _, hit = service.generate(req)

    assert hit is False
    assert provider.calls == 2


def test_different_requests_have_different_cache_keys() -> None:
    provider = FakeProvider()
    clock = FakeClock()
    cache = InMemoryTTLCache(now_fn=clock.now)
    service = CachedLLMService(provider=provider, cache=cache, ttl_seconds=60)

    service.generate(LLMRequest(prompt="p1", model="gpt-test"))
    service.generate(LLMRequest(prompt="p2", model="gpt-test"))

    assert provider.calls == 2
