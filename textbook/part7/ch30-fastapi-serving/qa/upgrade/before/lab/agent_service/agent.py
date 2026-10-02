from __future__ import annotations

import asyncio
from typing import Annotated, TypedDict

from langgraph.config import get_stream_writer
from langgraph.graph import END, START, StateGraph
from operator import add


class AgentState(TypedDict):
    messages: Annotated[list[str], add]
    answer: str


def _compose_answer(question: str) -> str:
    """외부 API 없이 서비스 계층을 검증할 수 있는 교육용 답을 만듭니다."""
    if "오류" in question:
        raise RuntimeError("교육용 스트림 오류")
    return f"질문을 확인했습니다: {question}"


async def answer_node(state: AgentState) -> dict[str, object]:
    question = state["messages"][-1]
    answer = _compose_answer(question)
    try:
        writer = get_stream_writer()
    except RuntimeError:
        writer = None
    for piece in answer.split():
        await asyncio.sleep(0)
        if writer is not None:
            writer({"token": piece + " "})
    return {"answer": answer}


def build_agent():
    """실제 LangGraph 실행 객체를 구성합니다."""
    graph = StateGraph(AgentState)
    graph.add_node("answer", answer_node)
    graph.add_edge(START, "answer")
    graph.add_edge("answer", END)
    return graph.compile()


agent = build_agent()
