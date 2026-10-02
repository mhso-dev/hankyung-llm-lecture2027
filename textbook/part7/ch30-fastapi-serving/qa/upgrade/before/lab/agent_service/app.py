from __future__ import annotations

import asyncio
import logging
import os
from collections.abc import AsyncIterable
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.sse import EventSourceResponse, ServerSentEvent

from .agent import agent
from .live_agent import build_live_agent
from .schemas import ChatRequest, ChatResponse, HealthResponse

app = FastAPI(title="교육용 Agent API", version="1.0.0")
logger = logging.getLogger(__name__)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "Last-Event-ID"],
    expose_headers=["X-Request-ID"],
)


async def get_agent():
    return agent


async def get_live_agent():
    return build_live_agent()


async def get_timeout() -> float:
    return 2.0


async def get_resume_index(
    body: ChatRequest,
    last_event_id: Annotated[str | None, Header(alias="Last-Event-ID")] = None,
) -> int:
    if last_event_id is None:
        return 0
    prefix = f"{body.thread_id}:"
    if not last_event_id.startswith(prefix):
        raise HTTPException(status_code=400, detail="Last-Event-ID의 thread가 다릅니다")
    try:
        return int(last_event_id.removeprefix(prefix)) + 1
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Last-Event-ID 형식이 올바르지 않습니다") from exc


async def require_token(authorization: Annotated[str | None, Header()] = None) -> str:
    expected = os.getenv("DEMO_API_TOKEN", "local-demo-token")
    if authorization != f"Bearer {expected}":
        raise HTTPException(status_code=401, detail="인증 정보가 올바르지 않습니다")
    return expected


AgentDep = Annotated[object, Depends(get_agent)]
LiveAgentDep = Annotated[object, Depends(get_live_agent)]
TimeoutDep = Annotated[float, Depends(get_timeout)]
ResumeIndexDep = Annotated[int, Depends(get_resume_index)]
AuthDep = Annotated[str, Depends(require_token)]


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/v1/chat", response_model=ChatResponse)
async def chat(body: ChatRequest, runtime: AgentDep, _token: AuthDep, timeout: TimeoutDep) -> ChatResponse:
    try:
        result = await asyncio.wait_for(
            runtime.ainvoke({"messages": [body.question]}), timeout=timeout
        )
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="Agent 응답 시간이 초과되었습니다") from exc
    return ChatResponse(answer=result["answer"], thread_id=body.thread_id)


@app.post("/v1/chat/live", response_model=ChatResponse)
async def live_chat(body: ChatRequest, runtime: LiveAgentDep, _token: AuthDep) -> ChatResponse:
    result = await asyncio.wait_for(
        runtime.ainvoke({"messages": [{"role": "user", "content": body.question}]}),
        timeout=45.0,
    )
    return ChatResponse(answer=result["messages"][-1].text, thread_id=body.thread_id)


def _event_id(thread_id: str, index: int) -> str:
    return f"{thread_id}:{index}"


@app.post("/v1/chat/stream", response_class=EventSourceResponse)
async def chat_stream(
    body: ChatRequest,
    runtime: AgentDep,
    _token: AuthDep,
    timeout: TimeoutDep,
    start: ResumeIndexDep,
) -> AsyncIterable[ServerSentEvent]:
    index = 0
    try:
        async with asyncio.timeout(timeout):
            async for chunk in runtime.astream(
                {"messages": [body.question]}, stream_mode="custom"
            ):
                if index >= start:
                    yield ServerSentEvent(
                        data=chunk, event="token", id=_event_id(body.thread_id, index)
                    )
                index += 1
        yield ServerSentEvent(data={"thread_id": body.thread_id}, event="done")
    except Exception:
        logger.exception("Agent SSE stream failed", extra={"thread_id": body.thread_id})
        yield ServerSentEvent(
            data={"code": "stream_failed", "message": "Agent 스트림이 중단되었습니다"},
            event="error",
        )


@app.post("/v1/chat/live/stream", response_class=EventSourceResponse)
async def live_chat_stream(
    body: ChatRequest, runtime: LiveAgentDep, _token: AuthDep
) -> AsyncIterable[ServerSentEvent]:
    index = 0
    try:
        async with asyncio.timeout(45.0):
            async for message, metadata in runtime.astream(
                {"messages": [{"role": "user", "content": body.question}]},
                stream_mode="messages",
            ):
                if metadata.get("langgraph_node") != "model":
                    continue
                for block in message.content_blocks:
                    if block.get("type") == "text" and block.get("text"):
                        yield ServerSentEvent(
                            data={"token": block["text"]},
                            event="token",
                            id=_event_id(body.thread_id, index),
                        )
                        index += 1
        yield ServerSentEvent(data={"thread_id": body.thread_id}, event="done")
    except Exception:
        logger.exception("Live Agent SSE stream failed", extra={"thread_id": body.thread_id})
        yield ServerSentEvent(
            data={"code": "live_stream_failed", "message": "Agent 스트림이 중단되었습니다"},
            event="error",
        )
