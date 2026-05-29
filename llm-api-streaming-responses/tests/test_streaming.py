import pytest
from httpx import ASGITransport, AsyncClient

from llm_api_streaming_responses.api import create_app


async def _read_sse_lines(response) -> list[str]:
    lines: list[str] = []
    async for line in response.aiter_lines():
        if line.startswith("data: "):
            lines.append(line[len("data: ") :])
    return lines


@pytest.mark.asyncio
async def test_generate_endpoint() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/generate", json={"prompt": "hello"})

    assert resp.status_code == 200
    assert resp.json()["text"] == "Echo: hello"


@pytest.mark.asyncio
async def test_streaming_endpoint_sends_done_event() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/generate/stream", json={"prompt": "hello world"})
        payloads = await _read_sse_lines(resp)

    assert resp.status_code == 200
    assert any('"type": "token"' in p for p in payloads)
    assert payloads[-1] == '{"type": "done"}'
