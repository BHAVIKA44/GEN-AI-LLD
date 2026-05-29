from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from .models import GenerateRequest, GenerateResponse
from .providers import FakeStreamingLLMProvider
from .service import LLMService


def create_app(service: LLMService | None = None) -> FastAPI:
    app = FastAPI(title="LLM Streaming API")
    llm_service = service or LLMService(FakeStreamingLLMProvider())

    @app.post("/generate", response_model=GenerateResponse)
    async def generate(req: GenerateRequest) -> GenerateResponse:
        text = await llm_service.generate(req.prompt)
        return GenerateResponse(text=text)

    @app.post("/generate/stream")
    async def generate_stream(req: GenerateRequest) -> StreamingResponse:
        return StreamingResponse(llm_service.stream_sse(req.prompt), media_type="text/event-stream")

    return app
