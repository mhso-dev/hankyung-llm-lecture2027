from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": text.splitlines(keepends=True)}


SETUP = '''# 고정한 패키지를 설치하고 비밀 키의 존재 여부만 확인합니다.
%pip install -q langchain==1.4.0 langchain-openai==1.6.0 langgraph==1.2.11 python-dotenv==1.2.3
from pathlib import Path
import os
from importlib.metadata import version
from dotenv import load_dotenv

for folder in [Path.cwd(), *Path.cwd().parents]:
    if (folder / ".env").is_file():
        load_dotenv(folder / ".env")
        break

MODEL = "gpt-5.4-mini"
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY가 필요합니다."
print({"langchain": version("langchain"), "langgraph": version("langgraph"), "model": MODEL, "cost_limit_usd": 1.0})
'''


def notebook(title: str, question: str, cells: list[tuple[str, str]]) -> dict:
    result = [md(f"# {title}\n\n{question}\n"), md("## 실행 환경 준비\n\nPython 3.12와 고정된 패키지 환경을 사용합니다. 키 값은 출력하지 않고 존재 여부만 확인합니다.\n"), code(SETUP)]
    for heading, source in cells:
        result.extend([md(f"## {heading}\n"), code(source)])
    return {"cells": result, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.12"}, "lesson_format": "experiment"}, "nbformat": 4, "nbformat_minor": 5}


NOTEBOOKS = {
"ch25-streaming/01-일곱-가지-stream-mode": notebook("일곱 가지 stream mode", "같은 그래프에서 일곱 모드는 어떤 사건을 서로 다른 크기로 보여 줄까요?", [
("그래프 준비", '''# 두 노드가 상태 변경분과 사용자 정의 진행률을 내보내는 그래프를 만듭니다.
from typing import TypedDict
from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    topic: str
    draft: str

def prepare(state: State) -> dict[str, str]:
    get_stream_writer()({"stage": "prepare", "progress": 50})
    return {"topic": state["topic"].strip()}

def write(state: State) -> dict[str, str]:
    get_stream_writer()({"stage": "write", "progress": 100})
    return {"draft": f"{state['topic']} 스트리밍 요약"}

builder = StateGraph(State)
builder.add_node("prepare", prepare)
builder.add_node("write", write)
builder.add_edge(START, "prepare")
builder.add_edge("prepare", "write")
builder.add_edge("write", END)
graph = builder.compile(checkpointer=InMemorySaver())
'''),
("일곱 모드 실행", '''# 같은 입력을 일곱 모드로 실행하고 사건 수와 첫 자료형을 기록합니다.
modes = ["values", "updates", "messages", "custom", "checkpoints", "tasks", "debug"]
counts = {}
for index, mode in enumerate(modes):
    config = {"configurable": {"thread_id": f"mode-{index}"}}
    events = list(graph.stream({"topic": "고객 문의", "draft": ""}, config, stream_mode=mode))
    counts[mode] = len(events)
    sample_type = type(events[0]).__name__ if events else "없음"
    print(f"{mode:11} events={len(events):2} first={sample_type}")
assert counts["messages"] == 0
assert counts["custom"] == 2
'''),
("여러 모드를 한 번에 구독", '''# updates와 custom을 함께 구독해 모드 이름과 자료를 나란히 확인합니다.
config = {"configurable": {"thread_id": "multi"}}
events = list(graph.stream(
    {"topic": "배송", "draft": ""}, config,
    stream_mode=["updates", "custom"],
))
for mode, data in events:
    print(mode, data)
assert {mode for mode, _ in events} == {"updates", "custom"}
''')]),
"ch25-streaming/02-토큰과-중간-진행-스트리밍": notebook("토큰과 중간 진행 스트리밍", "사용자가 기다리는 동안 토큰, 노드 완료, 업무 진행률을 어떻게 구분해 보여 줄까요?", [
("모델이 포함된 그래프", '''# 모델 호출 전후에 진행률을 내보내는 한 노드 그래프를 구성합니다.
from typing import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    question: str
    answer: str

model = init_chat_model(f"openai:{MODEL}", reasoning_effort="none")

def answer(state: State) -> dict[str, str]:
    writer = get_stream_writer()
    writer({"stage": "model_call", "progress": 30})
    response = model.invoke("두 문장으로 답하세요: " + state["question"])
    writer({"stage": "done", "progress": 100})
    return {"answer": response.text}

builder = StateGraph(State)
builder.add_node("answer", answer)
builder.add_edge(START, "answer")
builder.add_edge("answer", END)
graph = builder.compile()
print("그래프 준비 완료")
'''),
("세 종류의 사건 관찰", '''# 한 실행에서 토큰, 상태 변경분, 사용자 정의 진행률을 함께 셉니다.
seen = {"messages": 0, "updates": 0, "custom": 0}
preview = []
for mode, data in graph.stream(
    {"question": "스트리밍이 체감 지연을 줄이는 이유는 무엇인가요?", "answer": ""},
    stream_mode=["messages", "updates", "custom"],
):
    seen[mode] += 1
    if mode == "messages":
        chunk, metadata = data
        if chunk.text:
            preview.append(chunk.text)
    else:
        print(mode, data)
print("토큰 조각 수:", seen["messages"])
print("답변 앞부분:", "".join(preview)[:80])
assert seen["messages"] > 0 and seen["updates"] > 0 and seen["custom"] == 2
'''),
("표시 정책 만들기", '''# 사건 종류마다 사용자 화면에 표시할 문구를 구분합니다.
labels = {
    "messages": "답변을 작성하고 있습니다",
    "updates": "단계가 완료되었습니다",
    "custom": "업무 진행률이 바뀌었습니다",
}
for mode in ["messages", "updates", "custom"]:
    print(mode, "→", labels[mode])
''')]),
"ch25-streaming/03-TTFT와-total-비교": notebook("TTFT와 total 비교", "같은 에이전트를 세 모드로 실행할 때 첫 사건, 첫 토큰, 전체 완료 시간은 어떻게 달라질까요?", [
("측정 그래프 준비", '''# 같은 모델과 질문을 세 모드에서 측정할 그래프를 구성합니다.
from time import perf_counter
from typing import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    question: str
    answer: str

model = init_chat_model(f"openai:{MODEL}", reasoning_effort="none")
def answer(state: State) -> dict[str, str]:
    get_stream_writer()({"stage": "started"})
    response = model.invoke("세 문장 이내로 답하세요: " + state["question"])
    return {"answer": response.text}

builder = StateGraph(State)
builder.add_node("answer", answer)
builder.add_edge(START, "answer")
builder.add_edge("answer", END)
graph = builder.compile()
'''),
("세 모드에서 시간 측정", '''# first_event와 내용이 있는 첫 토큰, 마지막 사건 시각을 따로 기록합니다.
question = "고객에게 스트리밍의 장점을 설명해 주세요."
rows = []
for mode in ["updates", "messages", "custom"]:
    started = perf_counter()
    first_event = None
    first_token = None
    event_count = 0
    for data in graph.stream({"question": question, "answer": ""}, stream_mode=mode):
        elapsed = perf_counter() - started
        event_count += 1
        first_event = elapsed if first_event is None else first_event
        if mode == "messages":
            chunk, _ = data
            if chunk.text and first_token is None:
                first_token = elapsed
    total = perf_counter() - started
    rows.append({"mode": mode, "first_event_s": round(first_event or total, 3), "ttft_s": None if first_token is None else round(first_token, 3), "total_s": round(total, 3), "events": event_count})
for row in rows:
    print(row)
assert next(r for r in rows if r["mode"] == "messages")["ttft_s"] is not None
'''),
("지표를 구분해 해석", '''# TTFT가 있는 messages와 첫 사건만 있는 두 모드를 구분합니다.
for row in rows:
    meaning = "첫 토큰을 직접 측정" if row["ttft_s"] is not None else "첫 사건만 측정"
    print(row["mode"], meaning, "total=", row["total_s"])
print("네트워크 상태에 따라 수치는 실행할 때마다 달라질 수 있습니다.")
''')]),
"ch26-delegation/01-Subagent-도구-위임": notebook("Subagent 도구 위임", "중앙 에이전트가 전문 에이전트에 필요한 맥락만 전달하면 호출 경계가 어떻게 드러날까요?", [
("전문 에이전트를 도구로 감싸기", '''# 전문 에이전트를 도구로 감싸고 중앙 supervisor에 등록합니다.
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool

model = init_chat_model(f"openai:{MODEL}", reasoning_effort="none")
calls: list[str] = []
specialist = create_agent(model, tools=[], system_prompt="환불 정책 확인 항목을 두 문장으로 답하세요.")

@tool
def policy_specialist(question: str) -> str:
    """환불 정책 질문을 검토하고 핵심 근거만 반환합니다."""
    calls.append("policy_specialist")
    result = specialist.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].text

supervisor = create_agent(model, tools=[policy_specialist], system_prompt="환불이 포함된 요청에는 policy_specialist 도구를 반드시 한 번 사용한 뒤 고객 답변을 작성하세요.")
'''),
("중앙 에이전트가 결과 종합", '''# supervisor를 실제 실행하고 메시지 기록에서 도구 호출을 확인합니다.
request = "배송 지연 주문의 환불 가능 여부와 고객 안내 문구를 작성해 주세요."
result = supervisor.invoke({"messages": [{"role": "user", "content": request}]})
tool_names = [call["name"] for message in result["messages"] for call in getattr(message, "tool_calls", [])]
print("모델이 선택한 도구:", tool_names)
print("도구 실행 기록:", calls)
print("최종 답변:", result["messages"][-1].text)
assert tool_names == ["policy_specialist"] and calls == ["policy_specialist"]
'''),
("전달 맥락 줄이기", '''# 전체 기록과 전문 에이전트에 전달한 질문의 문자 수를 비교합니다.
full_context = request + "\\n" + "내부 기록 " * 100
focused_context = request
print({"전체_문자수": len(full_context), "전달_문자수": len(focused_context)})
assert len(focused_context) < len(full_context)
''')]),
"ch26-delegation/02-Handoff-상태-전환": notebook("Handoff 상태 전환", "대화의 담당자가 바뀌어도 다음 턴이 같은 담당자에서 이어지게 하려면 어떤 상태를 저장해야 할까요?", [
("활성 담당자 상태 정의", '''# 여러 턴에 유지할 active_agent 필드를 상태에 정의합니다.
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    message: str
    active_agent: str
    reply: str
'''),
("담당자 선택과 응답 함수", '''# 메시지와 이전 상태를 읽어 담당자를 선택하고 답변을 만듭니다.
def dispatch(state: State) -> dict[str, str]:
    text = state["message"]
    if "환불" in text:
        active = "refund_agent"
    elif state.get("active_agent"):
        active = state["active_agent"]
    else:
        active = "general_agent"
    return {"active_agent": active}

def respond(state: State) -> dict[str, str]:
    return {"reply": f"{state['active_agent']}가 답변합니다: {state['message']}"}
'''),
("체크포인터가 있는 그래프", '''# 체크포인터를 연결해 같은 thread_id의 상태를 다음 턴으로 이어갑니다.
builder = StateGraph(State)
builder.add_node("dispatch", dispatch)
builder.add_node("respond", respond)
builder.add_edge(START, "dispatch")
builder.add_edge("dispatch", "respond")
builder.add_edge("respond", END)
graph = builder.compile(checkpointer=InMemorySaver())
'''),
("두 턴을 같은 thread에서 실행", '''# 첫 턴에서 담당자를 바꾸고 두 번째 턴에서 유지되는지 확인합니다.
config = {"configurable": {"thread_id": "handoff-demo"}}
turn1 = graph.invoke({"message": "환불 담당자에게 연결해 주세요", "active_agent": "", "reply": ""}, config)
turn2 = graph.invoke({"message": "주문 번호는 A-102입니다"}, config)
print(turn1["active_agent"], "→", turn2["active_agent"])
print(turn2["reply"])
assert turn2["active_agent"] == "refund_agent"
'''),
("종료 조건 확인", '''# 필수 주문 번호와 담당자 상태가 모두 갖춰졌는지 판정합니다.
completed = "A-102" in turn2["message"] and turn2["active_agent"] == "refund_agent"
print({"필수정보_수집": completed, "다음_상태": "END" if completed else "refund_agent"})
assert completed
''')]),
"ch26-delegation/03-Router-분류와-병렬-실행": notebook("Router 분류와 병렬 실행", "한 번의 분류 결과로 서로 독립적인 전문 작업을 병렬 실행하면 호출 구조가 어떻게 달라질까요?", [
("구조화된 분류", '''# 모델이 요청에 필요한 전문 분야를 정해진 목록으로 반환하게 합니다.
from concurrent.futures import ThreadPoolExecutor
from typing import Literal
from pydantic import BaseModel
from langchain.chat_models import init_chat_model

class Route(BaseModel):
    destinations: list[Literal["policy", "shipping"]]

model = init_chat_model(f"openai:{MODEL}", reasoning_effort="none")
router = model.with_structured_output(Route)
request = "배송이 늦었습니다. 환불 규정과 현재 배송 안내를 함께 알려 주세요."
route = router.invoke("요청을 처리할 분야를 모두 고르세요: " + request)
print("선택된 분야:", route.destinations)
'''),
("선택된 전문가를 병렬 실행", '''# 서로 독립적인 전문 모델 호출을 최대 두 작업으로 동시에 실행합니다.
def run_specialist(name: str) -> str:
    prompts = {
        "policy": "환불 규정 확인 항목을 한 문장으로 답하세요: ",
        "shipping": "배송 상태 확인 항목을 한 문장으로 답하세요: ",
    }
    return model.invoke(prompts[name] + request).text

with ThreadPoolExecutor(max_workers=2) as pool:
    results = dict(zip(route.destinations, pool.map(run_specialist, route.destinations)))
for name, result in results.items():
    print(name, "→", result)
assert set(results) == set(route.destinations)
'''),
("병렬 결과 종합", '''# 분야 이름을 붙여 두 전문 결과를 하나의 근거 문자열로 합칩니다.
combined = "\\n".join(f"[{name}] {value}" for name, value in results.items())
print(combined)
print("전문 결과 수:", len(results))
''')]),
"ch26-delegation/04-호출-수-비용-종료-조건-비교": notebook("호출 수·비용·종료 조건 비교", "같은 과제를 세 위임 구조로 처리하면 모델 호출 수와 추정 비용, 종료 조건이 어떻게 달라질까요?", [
("호출 계측기 준비", '''# 세 구조가 함께 사용할 모델, 공식 단가, 기록 목록을 준비합니다.
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool

PRICE_PER_M_INPUT = 0.75
PRICE_PER_M_CACHED = 0.075
PRICE_PER_M_OUTPUT = 4.50
model = init_chat_model(f"openai:{MODEL}", reasoning_effort="none")
records: list[dict[str, object]] = []
task = "배송 지연과 환불 가능성을 확인하고 고객 안내를 세 문장으로 작성하세요."
'''),
("응답 사용량 기록 함수", '''# 일반 입력, 캐시 입력, 출력 토큰을 나누어 비용을 계산합니다.
def record_usage(pattern: str, role: str, response: object) -> None:
    usage = getattr(response, "usage_metadata", None) or {}
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    details = usage.get("input_token_details", {}) or {}
    cached_tokens = details.get("cache_read", 0)
    uncached_tokens = input_tokens - cached_tokens
    cost = (uncached_tokens * PRICE_PER_M_INPUT + cached_tokens * PRICE_PER_M_CACHED + output_tokens * PRICE_PER_M_OUTPUT) / 1_000_000
    records.append({"pattern": pattern, "role": role, "input": input_tokens, "cached": cached_tokens, "output": output_tokens, "cost_usd": cost})

def measured_call(pattern: str, role: str, prompt: str) -> str:
    response = model.invoke(prompt)
    record_usage(pattern, role, response)
    return response.text
'''),
("Subagent 구조 실행", '''# create_agent supervisor가 전문 도구를 실제로 선택하게 합니다.
@tool
def policy_tool(question: str) -> str:
    """환불 정책 확인 항목을 반환합니다."""
    return measured_call("subagent", "policy_tool", "환불 확인 항목: " + question)

subvisor = create_agent(model, tools=[policy_tool], system_prompt="환불 요청에는 policy_tool을 반드시 한 번 사용하고 결과를 종합하세요.")
sub_result = subvisor.invoke({"messages": [{"role": "user", "content": task}]})
sub_trace = [call["name"] for message in sub_result["messages"] for call in getattr(message, "tool_calls", [])]
for message in sub_result["messages"]:
    if getattr(message, "usage_metadata", None):
        record_usage("subagent", "supervisor", message)
sub_done = bool(sub_result["messages"][-1].text and sub_trace == ["policy_tool"])
print({"trace": sub_trace, "done": sub_done})
assert sub_done
'''),
("Handoff 노드와 분기", '''# active_agent를 읽는 조건 함수가 실제 다음 노드를 선택하게 합니다.
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class HandoffState(TypedDict):
    active_agent: str
    task: str
    shipping: str
    answer: str
    trace: list[str]

def shipping_node(state: HandoffState) -> dict[str, object]:
    result = measured_call("handoff", "shipping", "배송 확인 항목: " + state["task"])
    return {"shipping": result, "active_agent": "refund", "trace": ["shipping"]}

def refund_node(state: HandoffState) -> dict[str, object]:
    result = measured_call("handoff", "refund", "배송 결과를 이어받아 환불 답변: " + state["shipping"])
    return {"answer": result, "active_agent": "done", "trace": state["trace"] + ["refund"]}

def route_active(state: HandoffState) -> str:
    return state["active_agent"]
'''),
("Handoff 그래프 실행", '''# 조건부 엣지가 shipping과 refund를 차례로 선택하는지 trace로 확인합니다.
builder = StateGraph(HandoffState)
builder.add_node("shipping", shipping_node)
builder.add_node("refund", refund_node)
builder.add_conditional_edges(START, route_active, {"shipping": "shipping"})
builder.add_conditional_edges("shipping", route_active, {"refund": "refund"})
builder.add_edge("refund", END)
handoff_graph = builder.compile()
handoff_result = handoff_graph.invoke({"active_agent": "shipping", "task": task, "shipping": "", "answer": "", "trace": []})
handoff_done = bool(handoff_result["answer"] and handoff_result["active_agent"] == "done")
print({"trace": handoff_result["trace"], "active_agent": handoff_result["active_agent"]})
assert handoff_done and handoff_result["trace"] == ["shipping", "refund"]
'''),
("Router 구조 실행", '''# 구조화된 classifier의 destinations를 그대로 읽어 선택된 경로만 실행합니다.
from typing import Literal
from pydantic import BaseModel

class CompareRoute(BaseModel):
    destinations: list[Literal["policy", "shipping"]]

route_result = model.with_structured_output(CompareRoute, include_raw=True).invoke("요청에 필요한 분야를 모두 고르세요: " + task)
if route_result["parsing_error"] or not route_result["parsed"]:
    raise ValueError("라우터 구조화 출력 파싱 실패")
record_usage("router", "classifier", route_result["raw"])
destinations = route_result["parsed"].destinations
router_trace = ["classifier"]
router_results: list[str] = []
for destination in destinations:
    router_trace.append(destination)
    router_results.append(measured_call("router", destination, f"{destination} 담당자로 답하세요: " + task))
router_answer = measured_call("router", "synthesizer", "전문 결과를 세 문장으로 합치세요: " + " ".join(router_results))
router_trace.append("synthesizer")
router_done = bool(destinations and len(router_results) == len(destinations) and router_answer)
print({"route": destinations, "trace": router_trace, "done": router_done})
assert router_done and set(destinations) == {"policy", "shipping"}
'''),
("호출 수와 비용 집계", '''# 구조별 호출 수, 입력·출력 토큰, 추정 비용을 합산합니다.
summary: dict[str, dict[str, float]] = {}
for row in records:
    item = summary.setdefault(row["pattern"], {"calls": 0, "input": 0, "cached": 0, "output": 0, "cost_usd": 0.0})
    item["calls"] += 1
    item["input"] += row["input"]
    item["cached"] += row["cached"]
    item["output"] += row["output"]
    item["cost_usd"] += row["cost_usd"]
for name, item in summary.items():
    item["cost_usd"] = round(item["cost_usd"], 6)
    print(name, item)
assert all(item["cost_usd"] < 1 for item in summary.values())
'''),
("종료 조건 검증", '''# 앞 셀에서 계산한 완료 조건 세 개가 모두 참인지 검사합니다.
completion = {"subagent": sub_done, "handoff": handoff_done, "router": router_done}
for pattern, done in completion.items():
    print(pattern, "완료:", done)
assert all(completion.values())
''')]),
}


CHAPTERS = {
"ch25-streaming": {
    "part": 6, "part_title": "Part 6 · Agent 심화", "chapter": "ch25-streaming", "title": "Streaming", "hours": "총 8h · 강의 3h · 실습 5h",
    "objectives": ["LangGraph의 일곱 가지 stream mode가 내보내는 사건을 구분할 수 있습니다.", "토큰·노드 갱신·사용자 정의 진행 상황을 목적에 맞게 선택할 수 있습니다.", "첫 사건·첫 토큰까지의 시간·전체 완료 시간을 따로 측정할 수 있습니다."],
    "lab_path": "labs/part6/ch25-streaming",
    "sections": [("01-일곱-가지-stream-mode", "일곱 가지 stream mode"), ("02-토큰과-중간-진행-스트리밍", "토큰과 중간 진행 스트리밍"), ("03-TTFT와-total-비교", "TTFT와 total 비교")],
},
"ch26-delegation": {
    "part": 6, "part_title": "Part 6 · Agent 심화", "chapter": "ch26-delegation", "title": "위임 구조 — Subagents · Handoffs · Router", "hours": "총 8h · 강의 4h · 실습 4h",
    "objectives": ["Subagent·Handoff·Router의 제어 흐름과 맥락 소유자를 구분할 수 있습니다.", "같은 과제를 세 구조로 구현하고 실제 모델 호출을 계측할 수 있습니다.", "호출 수·추정 비용·종료 조건을 근거로 구조를 선택할 수 있습니다."],
    "lab_path": "labs/part6/ch26-delegation",
    "sections": [("01-Subagent-도구-위임", "Subagent 도구 위임"), ("02-Handoff-상태-전환", "Handoff 상태 전환"), ("03-Router-분류와-병렬-실행", "Router 분류와 병렬 실행"), ("04-호출-수-비용-종료-조건-비교", "호출 수·비용·종료 조건 비교")],
},
}


def page(chapter: str, slug: str, title: str, index: int) -> str:
    is25 = chapter == "ch25-streaming"
    meta = "강의 1h · 실습 " + ("1.5h" if is25 and index < 3 else "2h" if is25 else "1h") + " | 코드 Jupyter Notebook | 새 용어 5"
    if is25:
        reasons = [
            "한 번에 최종 답만 반환하면 사용자는 실행이 멈췄는지 판단하기 어렵습니다. LangGraph는 같은 실행을 일곱 종류의 사건으로 관찰하게 합니다. 이번 절에서는 상태 전체, 변경분, 토큰, 사용자 정의 진행률, 체크포인트, 태스크, 디버그 사건의 크기와 용도를 실제 출력으로 구분합니다.",
            "답변 토큰과 업무 진행률은 서로 다른 사실입니다. 토큰은 모델이 생성한 글의 일부이고, 중간 단계는 그래프 노드가 끝났다는 신호이며, custom 사건은 개발자가 정한 업무 진행 상황입니다. 화면에서 세 신호를 섞으면 ‘30% 완료’라는 표시가 실제보다 앞설 수 있습니다.",
            "스트리밍을 켰다는 사실만으로 응답 전체가 빨라지지는 않습니다. 사용자가 첫 변화를 본 시간, 실제 답변의 첫 토큰을 본 시간, 최종 결과가 끝난 시간을 따로 측정해야 합니다. 이 구분은 Ch30의 FastAPI 서버 전송 이벤트(SSE) 응답 설계에 그대로 이어집니다.",
        ][index-1]
        definitions = [
            "스트림 모드(stream mode)는 실행 중 어떤 종류의 사건을 소비자에게 내보낼지 정하는 옵션입니다. values는 각 단계 뒤의 전체 상태, updates는 노드가 바꾼 값, messages는 모델 메시지 조각과 메타데이터, custom은 노드가 직접 보낸 자료를 반환합니다. checkpoints는 저장된 상태 스냅숏, tasks는 태스크 시작·종료·오류, debug는 체크포인트와 태스크를 포함한 자세한 실행 정보를 제공합니다. checkpoints와 tasks는 체크포인터가 있어야 사건이 생깁니다.",
            "토큰 스트리밍(token streaming)은 messages 모드로 모델의 메시지 조각을 순서대로 받는 방식입니다. 중간 단계 스트리밍은 updates로 노드가 반환한 변경분을 받습니다. custom 모드는 get_stream_writer()로 ‘문서 2/5 처리’처럼 도메인에 맞는 값을 보냅니다. 도구 호출 진행 상황은 도구 내부에서 custom 사건을 보내야 실제 처리 단계를 나타낼 수 있습니다.",
            "첫 토큰까지의 시간(Time To First Token, TTFT)은 요청을 시작한 뒤 내용이 있는 첫 모델 메시지 조각을 받을 때까지 걸린 시간입니다. first_event는 모드와 관계없이 첫 사건을 받은 시간이고 total은 마지막 사건까지 소비한 전체 시간입니다. custom의 시작 사건을 TTFT라고 부르면 모델이 아직 답을 만들기 전의 값을 첫 토큰으로 오해하게 됩니다.",
        ][index-1]
        prior = "Ch23에서 체크포인터와 thread_id가 상태를 저장하는 방법을 배웠고, Ch24에서 interrupt와 재개 사건을 확인했습니다. 이번 챕터는 같은 실행을 사용자 화면과 운영 로그에 어떤 단위로 노출할지 다룹니다."
        interpretation = ["로컬 그래프에는 모델 호출이 없으므로 messages 사건은 0개였습니다. values 3개, updates 2개, custom 2개, checkpoints 4개, tasks 4개, debug 8개가 실제로 출력되었습니다. custom은 두 노드가 각각 한 번 보낸 두 사건입니다. 사건 수는 그래프 노드와 체크포인트 구성에 따라 달라지므로 고정된 제품 규격으로 간주하면 안 됩니다.", "실제 출력에서 messages는 73개 조각, updates는 answer 노드가 끝난 뒤의 변경분 1개, custom은 30%와 100% 진행 사건 2개로 나타났습니다. 메시지 조각의 개수는 공급자와 모델에 따라 달라집니다. 진행률은 개발자가 정의한 값이므로 실제 작업량과 일치하도록 계산 근거를 함께 설계해야 합니다.", "이번 실행에서 updates의 first_event와 total은 모두 0.991초였습니다. messages는 first_event 0.525초, 내용이 있는 첫 토큰까지 0.529초, total 1.008초였습니다. custom은 시작 사건이 0.001초에 왔고 total은 1.003초였습니다. 세 실행은 API를 각각 새로 호출했으므로 네트워크 조건이 완전히 같지는 않습니다. updates와 custom에는 TTFT가 없습니다."][index-1]
        notes = ["여러 모드를 리스트로 넘기면 기본 v1 형식에서 (mode, data) 튜플을 받습니다. 최신 문서의 version='v2'는 type·ns·data 필드를 가진 통일된 형식을 제공하지만 기준 버전에서 기본값은 v1이므로 코드에서 선택한 형식을 명시합니다.", "custom 진행률은 모델 토큰 수에서 자동으로 계산되지 않습니다. 도구가 실제로 완료한 파일 수나 레코드 수처럼 검증 가능한 분모와 분자를 사용합니다. messages의 metadata로 노드 이름과 호출을 필터링할 수 있습니다.", "한 번의 측정으로 모델이나 모드의 우열을 단정하지 않습니다. 운영 비교에서는 워밍업, 반복 횟수, 입력 길이, 네트워크 구간, 백분위수를 함께 기록합니다. 비용은 스트리밍 여부보다 실제 입력·출력 토큰과 호출 수에 좌우됩니다."] [index-1]
        next_text = ["다음 절에서는 messages·updates·custom을 한 실행에서 함께 구독하고 화면 문구를 각 사건의 의미에 맞춰 나눕니다.", "다음 절에서는 같은 에이전트를 세 모드로 각각 실행해 first_event, TTFT, total을 구분해 측정합니다.", "Ch30에서는 messages와 custom 사건을 FastAPI SSE로 브라우저에 전송하고 연결 종료와 재접속을 처리합니다."][index-1]
        refs = '<li><a href="https://docs.langchain.com/oss/python/langgraph/streaming">LangGraph Streaming 공식 문서</a> · 확인 2026-09-11 · LangGraph 1.2.11</li><li><a href="https://reference.langchain.com/python/langgraph/types/StreamMode">StreamMode API</a> · 확인 2026-09-11 · 일곱 모드 확인</li><li><a href="https://github.com/langchain-ai/langgraph/blob/main/LICENSE">LangGraph 라이선스</a> · 확인 2026-09-11 · MIT</li>'
    else:
        reasons = ["도구가 많아질수록 한 에이전트의 프롬프트와 대화 기록은 길어집니다. Subagent 패턴은 전문 작업을 별도의 문맥에서 수행하고 중앙 에이전트에는 필요한 결과만 반환합니다. 이번 절에서는 전문 에이전트를 도구 함수로 감싸고 호출 경계를 직접 기록합니다.", "사용자가 여러 턴에 걸쳐 같은 담당자와 대화해야 하면 매번 새로 분류하는 것만으로 부족합니다. Handoff는 active_agent 같은 상태를 바꾸고 다음 턴의 동작을 그 상태에 맞춰 선택합니다. 담당 전환과 완료 조건을 상태로 남겨야 대화가 예상한 위치에서 이어집니다.", "Router는 입력을 한 번 분류한 뒤 선택된 전문 작업을 실행합니다. 여러 독립 분야가 동시에 필요하면 병렬 fan-out을 사용할 수 있습니다. 중앙 에이전트가 매 턴 계획하는 Subagent와 달리 Router는 분류 단계의 결과가 실행 경로를 정합니다.", "위임 구조를 이름만으로 선택하면 비용과 종료 시점을 설명하기 어렵습니다. 같은 고객 문의를 세 구조로 처리하고 실제 모델 호출의 토큰 사용량을 모아 호출 수와 추정 비용을 비교합니다. 마지막에는 ‘무엇이 생기면 끝인가’를 각 구조의 상태로 적습니다."][index-1]
        definitions = ["서브에이전트(Subagent)는 중앙 에이전트가 도구처럼 호출하는 전문 에이전트입니다. 중앙 에이전트가 사용자 대화의 문맥을 소유하고, 전문 에이전트는 호출마다 필요한 질문을 받아 결과를 반환합니다. 공식 문서는 이를 중앙 집중 제어와 문맥 격리로 설명합니다. 단일 에이전트의 도구 몇 개로 충분하면 위임 계층을 추가할 이유가 없습니다.", "핸드오프(Handoff)는 도구 호출이나 그래프 노드가 active_agent 또는 current_step 상태를 바꾸어 제어권을 다른 담당 동작으로 전환하는 패턴입니다. 전환된 담당자는 사용자와 직접 대화할 수 있고, 체크포인터가 active_agent를 저장하면 다음 턴도 그 상태에서 이어집니다. 전환 도구가 메시지와 상태 중 무엇을 넘기는지 명시해야 합니다.", "라우터(Router)는 입력을 분류하여 하나 이상의 전문 경로로 보냅니다. Command는 한 경로, Send는 여러 경로로 동적 fan-out할 때 사용할 수 있습니다. 이 절에서는 구조화 출력으로 분야를 고르고 ThreadPoolExecutor로 선택된 전문가를 병렬 호출합니다. 병렬 실행은 서로의 결과에 의존하지 않을 때만 가능합니다.", "호출 수는 외부 모델 API가 실제로 실행된 횟수입니다. 비용 추정치는 응답의 usage_metadata에 있는 입력·출력 토큰과 수업에서 고정한 단가 가정을 곱해 계산합니다. 종료 조건(stop condition)은 필요한 전문 결과, 필수 상태, 최종 답변이 모두 존재하는지를 판정하는 규칙입니다. recursion_limit 같은 실행 한도는 비상 경계이며 업무 완료 조건을 대신하지 않습니다."][index-1]
        prior = "Ch20에서 ToolNode와 명시적 END 조건을, Ch23에서 thread_id와 체크포인터를 배웠습니다. Ch25에서는 실행 사건을 스트리밍했습니다. 이번 챕터에서는 여러 에이전트 사이의 제어권과 맥락을 어디에 둘지 결정합니다."
        interpretation = ["create_agent supervisor의 실제 메시지 기록에는 policy_specialist 도구 호출이 한 번 있었고 도구 함수 실행 기록도 같은 이름을 남겼습니다. 전체 문맥은 639자였지만 전문 에이전트에는 질문 38자만 전달했습니다. 문자 수 비교는 문맥 격리의 크기만 보여 주며 토큰 절감이나 품질 향상을 직접 증명하지는 않습니다.", "첫 턴의 ‘환불’ 표현이 active_agent를 refund_agent로 바꿨고 같은 thread_id의 두 번째 호출도 refund_agent를 유지했습니다. 주문 번호 A-102가 모이자 실습의 완료 조건이 참이 되어 다음 상태를 END로 표시했습니다. 실제 서비스에서는 전환 권한과 사용자 확인도 함께 설계해야 합니다.", "모델의 구조화 출력은 policy와 shipping 두 분야를 선택했고 두 전문 함수가 결과를 반환했습니다. 결과 출력 순서는 zip으로 입력 순서에 맞췄지만 실제 완료 시각은 다를 수 있습니다. 분류가 빠뜨린 분야는 실행되지 않으므로 라우터 평가에는 분류 정확도가 포함되어야 합니다.", "실제 제어 흐름에서 Subagent는 create_agent가 policy_tool을 선택했고, Handoff 조건부 엣지는 active_agent를 읽어 shipping→refund→done으로 이동했으며, Router의 구조화 출력은 policy와 shipping을 선택해 두 경로를 실행했습니다. Subagent는 3회·0.005498달러, Handoff는 2회·0.000785달러, Router는 4회·0.001574달러로 추정되었고 세 종료 조건은 모두 참이었습니다. 가격은 2026-09-11 공식 일반·캐시 입력과 출력 단가를 적용했습니다."][index-1]
        notes = ["전문 에이전트에 사용자 대화 전체를 무조건 전달하지 않습니다. 업무에 필요한 질문과 제약만 전달하고 반환값의 형식과 길이를 정합니다. 병렬 위임은 작업 사이에 선후 관계가 없을 때 사용합니다.", "Handoff는 단순 함수 호출과 다릅니다. 다음 사용자 턴에서 누가 응답할지 상태가 바뀝니다. 체크포인터를 운영 저장소로 바꾸면 개인정보 보존 기간과 삭제 정책도 함께 정해야 합니다.", "Router는 장기 대화를 스스로 관리하지 않습니다. 다중 턴 대화에서는 Router를 대화형 에이전트의 도구로 감싸거나 active_agent 상태를 추가할 수 있습니다. 분류 결과가 비어 있을 때의 기본 경로도 정해야 합니다.", "langgraph-supervisor 저장소는 대부분의 새 사용 사례에서 라이브러리보다 도구를 통한 직접 supervisor 구현을 권고합니다. 이 문구를 swarm 라이브러리 전체의 폐기 권고로 확대하면 안 됩니다. 라이브러리 사용 여부와 관계없이 호출 경계·맥락·종료 조건을 애플리케이션 코드에서 검증합니다."][index-1]
        next_text = ["다음 절에서는 사용자가 직접 대화하는 담당자가 바뀌는 Handoff를 active_agent 상태와 thread_id로 구현합니다.", "다음 절에서는 한 번의 구조화 분류가 여러 독립 전문가를 선택하고 병렬 실행하는 Router를 구현합니다.", "마지막 절에서는 같은 고객 문의를 세 구조로 실행하고 호출 수·토큰·비용·종료 조건을 한 표로 비교합니다.", "Ch27에서는 파일시스템·Subagent·문맥 관리를 미리 조립한 DeepAgents 하네스로 이 위임 구조를 확장합니다. Ch39에서는 종료 조건을 평가 지표와 실패 예산으로 다시 다룹니다."][index-1]
        refs = '<li><a href="https://docs.langchain.com/oss/python/langchain/multi-agent/subagents">LangChain Subagents 공식 문서</a> · 확인 2026-09-11</li><li><a href="https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs">LangChain Handoffs 공식 문서</a> · 확인 2026-09-11</li><li><a href="https://docs.langchain.com/oss/python/langchain/multi-agent/router">LangChain Router 공식 문서</a> · 확인 2026-09-11</li><li><a href="https://github.com/langchain-ai/langgraph-supervisor-py">langgraph-supervisor 공식 저장소</a> · 확인 2026-09-11 · 직접 도구 구현 권고 범위 확인</li><li><a href="https://github.com/langchain-ai/langgraph-swarm-py">langgraph-swarm 공식 저장소</a> · 확인 2026-09-11</li>'
    details = {
        ("ch25-streaming", 1): ("고객 문의 그래프의 prepare와 write 노드는 같은 상태를 처리하지만, 운영 화면은 진행률만 필요하고 디버거는 태스크와 체크포인트가 필요합니다. 하나의 실행에서 소비자마다 필요한 관찰 범위가 다릅니다.", "StateGraph에 InMemorySaver를 연결한 뒤 values부터 debug까지 같은 입력을 일곱 번 실행합니다. counts 딕셔너리에 사건 수를 모으고 messages가 0개, custom이 2개인지 검사합니다. 마지막 셀에서는 updates와 custom을 동시에 구독하여 (mode, data) 튜플을 확인합니다.", "왜 messages 사건이 0개였나요?", "prepare와 write 노드가 모델을 호출하지 않았기 때문입니다. messages는 그래프 안의 모델 호출에서 생깁니다.", "일곱 모드는 같은 실행을 서로 다른 크기로 보여 줍니다. 체크포인터가 필요한 모드와 모델 호출이 필요한 모드를 입력 조건과 함께 해석합니다."),
        ("ch25-streaming", 2): ("배송 안내 화면에서 글자가 나타나는 동안 ‘모델 호출 30%’와 ‘완료 100%’를 함께 표시하려고 합니다. 토큰 조각, 노드 완료, 업무 진행률은 발생 원인과 갱신 시점이 다릅니다.", "answer 노드는 모델 호출 앞뒤에 get_stream_writer()로 30과 100을 보냅니다. 같은 실행에서 messages·updates·custom을 구독하고 seen 딕셔너리로 개수를 셉니다. 실제 답변 앞부분도 합쳐 출력하여 토큰 조각이 순서대로 도착했는지 확인합니다.", "custom의 30과 100은 누가 정한 값인가요?", "LangGraph가 자동 계산한 값이 아니라 answer 노드의 개발자가 업무 단계에 맞춰 정한 값입니다.", "messages는 답변 조각, updates는 answer 상태 변경, custom은 개발자가 정의한 진행 사건입니다. 사용자 문구도 이 세 의미에 맞춰 나눕니다."),
        ("ch25-streaming", 3): ("사용자는 화면에 첫 변화가 나타나면 시스템이 동작한다고 느끼지만, 그 변화가 실제 답변 토큰인지 ‘시작됨’ 표시인지는 구분하기 어렵습니다. 세 시각을 같은 이름으로 기록하면 성능 보고서가 잘못됩니다.", "perf_counter()를 요청 직전에 시작하고 세 모드를 각각 새로 실행합니다. 첫 yield를 first_event로, messages의 내용이 있는 첫 chunk를 first_token으로, 반복 종료를 total로 기록합니다. rows의 ttft_s는 messages에서만 숫자가 됩니다.", "custom의 first_event 0.002초를 TTFT라고 부를 수 있나요?", "아닙니다. 그 사건은 노드가 보낸 시작 알림이며 모델 답변의 첫 토큰이 아닙니다.", "first_event와 TTFT와 total은 측정 지점이 다릅니다. 세 번의 별도 API 호출이라는 한계를 포함해 수치를 읽습니다."),
        ("ch26-delegation", 1): ("환불 전문가는 내부 기록 전체가 아니라 환불 판단에 필요한 고객 질문만 받아도 됩니다. 중앙 상담자는 전문 결과를 받아 고객 문장으로 다시 작성합니다. 이 경계가 문맥 격리의 최소 단위입니다.", "policy_specialist를 @tool로 정의하고 내부에서 모델을 호출합니다. 중앙 흐름은 도구 반환값을 다음 모델 호출의 근거로 사용합니다. calls에는 policy_specialist와 main_agent가 순서대로 남고, 전체 639자와 전달 38자를 비교합니다.", "전문 에이전트에 전체 문맥을 전달하지 않은 이유는 무엇인가요?", "전문 작업에 필요한 질문만 전달해 불필요한 기록이 전문 문맥을 차지하지 않게 하기 위해서입니다.", "Subagent는 중앙 에이전트가 호출하는 전문 도구입니다. calls와 전달 문자 수로 호출 경계와 문맥 경계를 따로 확인합니다."),
        ("ch26-delegation", 2): ("첫 턴에서 고객이 환불 담당자를 요청하고 두 번째 턴에서 주문 번호만 말합니다. 두 번째 문장에는 ‘환불’이 없으므로 이전 담당자를 저장하지 않으면 일반 상담으로 되돌아갑니다.", "dispatch는 새 메시지와 저장된 active_agent를 함께 읽습니다. InMemorySaver와 thread_id='handoff-demo'를 사용해 두 턴을 실행합니다. 두 번째 결과가 refund_agent를 유지하고 주문 번호 A-102가 있으면 완료 조건을 참으로 만듭니다.", "두 번째 턴이 refund_agent에서 이어진 근거는 무엇인가요?", "같은 thread_id의 체크포인트에 첫 턴의 active_agent가 저장되었기 때문입니다.", "Handoff는 다음 턴의 동작을 바꾸는 상태 전환입니다. active_agent 유지와 A-102 수집을 각각 대화 지속과 완료 판정의 근거로 사용합니다."),
        ("ch26-delegation", 3): ("배송 지연 문의에는 환불 규정과 배송 상태라는 두 독립 분야가 함께 들어 있습니다. 한 분야만 고르면 답이 빠지고, 순서대로 호출하면 서로 기다릴 필요가 없는 작업까지 지연됩니다.", "구조화 출력 Route가 policy와 shipping 목록을 반환합니다. ThreadPoolExecutor는 선택된 이름만 run_specialist에 전달합니다. results의 키와 route.destinations의 집합이 같은지 검사한 뒤 분야 이름을 붙여 combined로 합칩니다.", "Router의 분류가 policy를 빠뜨리면 어떤 결과가 생기나요?", "policy 전문 함수가 실행되지 않으므로 환불 규정 근거가 결과에서 빠집니다. 분류 정확도를 별도로 평가해야 합니다.", "Router는 먼저 경로를 정하고 독립 작업을 병렬 실행합니다. 선택 목록, 실행 결과의 키, 종합 문자열을 연결해 빠진 분야가 없는지 확인합니다."),
        ("ch26-delegation", 4): ("같은 고객 과제를 세 구조에 넣어도 내부 호출 경로는 다릅니다. 이름만 바꾼 고정 호출 목록으로는 차이를 검증할 수 없으므로 각 구조의 도구, 상태 전환, 분류 결과가 실제 다음 호출을 결정해야 합니다.", "Subagent는 policy_tool.invoke의 결과를 supervisor가 사용합니다. Handoff는 active_agent를 shipping에서 refund와 done으로 바꿉니다. Router는 실제 classifier 응답과 요청 핵심어로 destinations를 만들고 선택된 경로만 실행합니다. 모든 모델 응답의 usage_metadata를 records에 모읍니다.", "종료 조건이 실제로 검사되었다는 근거는 무엇인가요?", "sub_done·handoff_done·router_done을 각 구조의 반환값과 상태에서 계산하고 마지막 셀에서 모두 참인지 assert로 검사합니다.", "세 구조는 실제 제어 흐름과 완료 조건으로 실행됩니다. 일반 입력·캐시 입력·출력 토큰을 공식 단가에 따로 곱해 비용을 계산합니다."),
    }
    situation, execution, quiz_question, quiz_answer, section_summary = details[(chapter, index)]
    caption = f"{title}의 실행 흐름. 위에서 아래로 사건 또는 제어권이 이동합니다."
    return f'''<!--meta: {meta} -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul><li>{title}의 핵심 구성 요소를 실제 출력에서 구분할 수 있습니다.</li><li>같은 입력을 실행하고 호출 경계와 관찰 지표를 설명할 수 있습니다.</li><li>결과가 보여 주는 범위와 추가 측정이 필요한 범위를 나눌 수 있습니다.</li></ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>{reasons}</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>{prior}</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>구체적인 상황</h3><p>{situation}</p><h3>정의</h3><p>{definitions}</p><h3>도식 읽기</h3>{{{{svg:{index:02d}-흐름}}}}<p>{caption} 파란 상자는 실행 단계, 초록 상자는 전달되는 자료, 노란 상자는 측정값 또는 종료 판정을 나타냅니다. 화살표는 노트북에서 실제로 진행되는 호출이나 사건의 방향입니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>{execution}</p><p>설치 셀은 Python 3.12 환경에 LangChain 1.4.0, langchain-openai 1.6.0, LangGraph 1.2.11을 고정합니다. 예상 API 비용은 1달러 미만이며 키 값은 출력하지 않습니다.</p>{{{{notebook:{slug}}}}}<p class="look"><b>확인할 점</b> — 출력과 trace에서 위 설명의 변수와 단계가 실제로 이어지는지 확인합니다. assert는 관찰 결과가 기대한 구조를 만족하는지 확인하는 보조 수단입니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>{interpretation}</p><p>이 실험은 한 질문과 한 실행 환경의 결과입니다. 모델 응답 내용과 지연 시간은 실행할 때마다 달라질 수 있습니다. 구조의 품질을 비교하려면 여러 질문, 반복 실행, 오류율, 사용자 수정 횟수를 추가로 측정해야 합니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>{notes}</li><li>비밀 키는 .env에서 읽고 존재 여부만 확인합니다. 노트북 출력, 예외 메시지, 배포 묶음에 키가 포함되지 않았는지 발행 전에 검사합니다.</li><li>외부 모델 호출의 응답과 지연은 공급자 상태에 따라 달라집니다. 운영 기준은 반복 측정의 중앙값과 상위 백분위수로 정합니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>{section_summary}</li><li>출력값과 상태를 근거로 관찰한 범위를 설명합니다.</li><li>반복 측정이 없는 수치를 일반적인 성능으로 확대하지 않습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — {next_text}</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz"><summary>1. {quiz_question}</summary><p class="quiz-a"><b>해설</b> — {quiz_answer}</p></details><details class="quiz"><summary>2. 이 절의 assert가 확인하는 것은 무엇인가요?</summary><p class="quiz-a"><b>해설</b> — 노트북에서 출력한 사건, trace, 상태, 완료 조건이 의도한 구조와 일치하는지 확인합니다.</p></details><details class="quiz"><summary>3. 한 번의 실행 결과로 평균 성능을 단정할 수 없는 이유는 무엇인가요?</summary><p class="quiz-a"><b>해설</b> — 네트워크와 모델 출력이 실행할 때마다 달라질 수 있고 입력 종류도 하나뿐이기 때문입니다.</p></details><details class="quiz"><summary>4. API 키를 실습 출력에 표시하면 안 되는 이유는 무엇인가요?</summary><p class="quiz-a"><b>해설</b> — 노트북과 HTML이 공유될 때 비밀 값도 함께 공개될 수 있기 때문입니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul>{refs}</ul>
'''


def write() -> None:
    for key, nb in NOTEBOOKS.items():
        chapter, slug = key.split("/")
        path = ROOT / "labs" / "part6" / chapter / "notebooks" / f"{slug}.ipynb"
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
    for chapter, data in CHAPTERS.items():
        data = dict(data)
        tuples = data.pop("sections")
        data["sections"] = [{"slug": slug, "title": title, "format": "experiment"} for slug, title in tuples]
        tb = ROOT / "textbook" / "part6" / chapter
        lab = ROOT / "labs" / "part6" / chapter
        (tb / "chapter.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        pyproject = '''[project]\nname = "kdt-%s"\nversion = "0.1.0"\nrequires-python = ">=3.12,<3.13"\ndependencies = [\n  "langchain==1.4.0",\n  "langchain-openai==1.6.0",\n  "langgraph==1.2.11",\n  "python-dotenv==1.2.3",\n]\n\n[dependency-groups]\ndev = ["ipykernel==7.3.0", "nbclient==0.11.0", "pip==26.2", "ruff==0.15.6"]\n\n[tool.uv]\npackage = false\n''' % chapter
        (lab / "pyproject.toml").write_text(pyproject)
        (lab / "README.md").write_text(f"# {data['title']} 실습\n\n노트북을 번호 순서대로 새 Python 3.12 커널에서 실행합니다. `.env`의 `OPENAI_API_KEY` 값은 출력하지 않습니다. 절별 예상 API 비용은 1달러 미만입니다.\n")
        for i, (slug, title) in enumerate(tuples, 1):
            (tb / "_src" / f"{slug}.html").write_text(page(chapter, slug, title, i))
        research = """# 공식 문서 조사 기록\n\n- 확인일: 2026-09-11\n- 기준 버전: Python 3.12, LangChain 1.4.0, langchain-openai 1.6.0, LangGraph 1.2.11\n- 공식 문서의 StreamMode는 values, updates, messages, custom, checkpoints, tasks, debug의 7개입니다.\n- streaming 문서는 단일 모드의 기본 v1 출력, 복수 모드의 `(mode, data)` 출력, 최신 v2의 `type/ns/data` 통일 형식을 구분합니다. 이 교재 코드는 기준 버전의 기본 v1 형식을 사용합니다.\n- Subagents 공식 문서는 중앙 에이전트가 전문 에이전트를 도구로 호출하고 사용자 문맥을 소유한다고 설명합니다.\n- Handoffs 공식 문서는 `active_agent` 또는 `current_step` 같은 상태 변경을 핵심으로 설명합니다.\n- Router 공식 문서는 단일 경로에 Command, 병렬 fan-out에 Send를 안내합니다.\n- `langgraph-supervisor-py` 저장소는 대부분의 사용 사례에서 supervisor 패턴을 도구로 직접 구현할 것을 권고합니다. `langgraph-swarm-py` 저장소에는 동일한 전면 권고 문구가 확인되지 않아 두 라이브러리를 함께 폐기 대상으로 서술하지 않습니다.\n- GPT-5.4 mini 공식 가격은 2026-09-11 확인 기준 100만 토큰당 일반 입력 0.75달러, 캐시 입력 0.075달러, 출력 4.50달러입니다. 실습은 usage_metadata의 cache_read를 일반 입력에서 분리합니다.\n\n## 출처\n\n- https://docs.langchain.com/oss/python/langgraph/streaming\n- https://reference.langchain.com/python/langgraph/types/StreamMode\n- https://docs.langchain.com/oss/python/langchain/multi-agent/subagents\n- https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs\n- https://docs.langchain.com/oss/python/langchain/multi-agent/router\n- https://github.com/langchain-ai/langgraph-supervisor-py\n- https://github.com/langchain-ai/langgraph-swarm-py\n- https://developers.openai.com/api/docs/models/gpt-5.4-mini\n"""
        (tb / "research.md").write_text(research)
        checklist = "# 집필 점검표\n\n" + "\n".join(f"## {slug}\n\n- 학습 질문: {title}의 실행 경계와 관찰값은 무엇인가?\n- 입력과 비교 조건: 노트북의 고정 입력과 모드 또는 위임 구조만 변경\n- 실제 연산: 새 커널에서 LangGraph 또는 LangChain 모델 호출\n- 관찰 결과: 실행 출력과 verification 해시로 확인\n- 형식: experiment\n- 해석 범위: 한 질문·한 실행의 결과이며 일반 성능으로 확대하지 않음\n- 본문과 그림: 노트북 출력과 도식 요소를 대조\n- 별도 검토: 후속 독립 언어 검토 예정\n" for slug, title in tuples)
        if chapter == "ch25-streaming":
            checklist += "\n## 실제 실행 근거\n\n- 01: values=3, updates=2, messages=0, custom=2, checkpoints=4, tasks=4, debug=8\n- 02: messages 73개 조각, updates 1개, custom 2개\n- 03: messages first event 0.525초, TTFT 0.529초, total 1.008초\n- 실행 검증: 3개 노트북 12개 코드 셀 새 커널 통과\n"
        else:
            checklist += "\n## 실제 실행 근거\n\n- 01: create_agent가 policy_specialist를 실제 선택, 전체 639자·전달 38자\n- 02: 같은 thread에서 refund_agent 유지, A-102 수집 후 END 판정\n- 03: 구조화 분류가 policy와 shipping 선택, 전문 결과 2개\n- 04: Subagent 3회·0.005498달러, Handoff 2회·0.000785달러, Router 4회·0.001574달러\n- 실행 검증: 4개 노트북 23개 코드 셀 새 커널 통과\n"
        (tb / "qa" / "authoring-checklist.md").parent.mkdir(exist_ok=True)
        (tb / "qa" / "authoring-checklist.md").write_text(checklist)
        (tb / "집필점검표.md").write_text(checklist)
        public_files = [
            f"textbook/part6/{chapter}/index.html",
            *[f"textbook/part6/{chapter}/{slug}.html" for slug, _ in tuples],
            f"labs/part6/{chapter}/README.md",
            *[f"labs/part6/{chapter}/notebooks/{slug}.ipynb" for slug, _ in tuples],
        ]
        (tb / "qa" / "public-files.json").write_text(json.dumps(public_files, ensure_ascii=False, indent=2) + "\n")


def write_pages_only() -> None:
    for chapter, data in CHAPTERS.items():
        for index, (slug, title) in enumerate(data["sections"], 1):
            path = ROOT / "textbook" / "part6" / chapter / "_src" / f"{slug}.html"
            path.write_text(page(chapter, slug, title, index))


if __name__ == "__main__":
    import sys
    write_pages_only() if "--pages-only" in sys.argv else write()
