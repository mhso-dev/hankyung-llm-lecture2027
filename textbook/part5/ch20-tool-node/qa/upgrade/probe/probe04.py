"""Ch 20 04절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe04.py <입력 L|G|T|B> <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  L : 「자료실에서 일반 도서를 며칠 대출할 수 있나요?」
  G : 「안녕하세요. 한 문장으로 인사해 주세요.」
  T : 「자료실 운영 시간과 연체 규정을 함께 알려 주세요.」
  B : 「자료실에서 일반 도서를 며칠 빌릴 수 있나요?」(값 바꿔 보기)
회차마다 (가) 규칙 갈래 그래프와 (나) 모델 선택 그래프에 같은 질문을 한 번씩 넣는다.
그래프·도구·상태 형식·규칙은 04절 노트북 셀과 같은 코드(04-probe.md §0).
"""
import json
import operator
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")

from typing_extensions import TypedDict  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import AIMessage, AnyMessage, HumanMessage  # noqa: E402
from langchain.tools import tool  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402
from langgraph.graph.message import add_messages  # noqa: E402
from langgraph.prebuilt import ToolNode, tools_condition  # noqa: E402

QUESTIONS = {
    "L": "자료실에서 일반 도서를 며칠 대출할 수 있나요?",
    "G": "안녕하세요. 한 문장으로 인사해 주세요.",
    "T": "자료실 운영 시간과 연체 규정을 함께 알려 주세요.",
    "B": "자료실에서 일반 도서를 며칠 빌릴 수 있나요?",
}
POLICIES = {
    "대출": "일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.",
    "운영": "평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.",
    "연체": "연체한 일수만큼 새 대출이 제한됩니다.",
}


@tool
def lookup_policy(topic: str):
    """교육센터 자료실 규정 하나를 주제어로 찾습니다. topic에는 대출, 운영, 연체 가운데 하나를 넣습니다."""
    if topic not in POLICIES:
        raise ValueError("지원하지 않는 주제: " + topic)
    return POLICIES[topic]


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    trace: Annotated[list[str], operator.add]


model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
tools = [lookup_policy]
bound_model = model.bind_tools(tools, parallel_tool_calls=False)
tool_node = ToolNode(tools)


# (가) 규칙 갈래 그래프
def keyword_topic(question):
    if "대출" in question:
        return "대출"
    if "운영" in question:
        return "운영"
    if "연체" in question:
        return "연체"
    return ""


def pick_by_rule(state):
    question = state["messages"][0].content
    if keyword_topic(question) == "":
        return "answer"
    return "request"


def make_rule_request(state):
    question = state["messages"][0].content
    topic = keyword_topic(question)
    rule_call = {"name": "lookup_policy", "args": {"topic": topic}, "id": "rule_call_1", "type": "tool_call"}
    request = AIMessage(content="", tool_calls=[rule_call])
    return {"messages": [request], "trace": ["request"]}


def call_answer(state):
    response = model.invoke(state["messages"])
    return {"messages": [response], "trace": ["answer"]}


rule_builder = StateGraph(AgentState)
rule_builder.add_node("request", make_rule_request)
rule_builder.add_node("tools", tool_node)
rule_builder.add_node("answer", call_answer)
rule_builder.add_conditional_edges(START, pick_by_rule, {"request": "request", "answer": "answer"})
rule_builder.add_edge("request", "tools")
rule_builder.add_edge("tools", "answer")
rule_builder.add_edge("answer", END)
rule_graph = rule_builder.compile()


# (나) 모델 선택 그래프 — 01절 그래프
def call_model(state):
    response = bound_model.invoke(state["messages"])
    return {"messages": [response], "trace": ["model"]}


model_builder = StateGraph(AgentState)
model_builder.add_node("model", call_model)
model_builder.add_node("tools", tool_node)
model_builder.add_edge(START, "model")
model_builder.add_conditional_edges("model", tools_condition, {"tools": "tools", END: END})
model_builder.add_edge("tools", "model")
model_graph = model_builder.compile()


def summarize(result):
    kinds, topics, tool_out, usages = [], [], [], []
    for message in result["messages"]:
        kind = type(message).__name__
        kinds.append(kind)
        if kind == "AIMessage":
            for c in message.tool_calls:
                topics.append(c["args"].get("topic", c["args"]))
            usage = message.usage_metadata
            if usage is not None:
                usages.append({"input": usage["input_tokens"], "output": usage["output_tokens"],
                               "cache_read": usage.get("input_token_details", {}).get("cache_read")})
        if kind == "ToolMessage":
            tool_out.append({"status": message.status, "content": message.content})
    last = result["messages"][-1]
    return {"trace": result["trace"], "kinds": kinds, "topics": topics, "tool_messages": tool_out,
            "usage": usages, "n_requests": len(usages),
            "input_total": sum(u["input"] for u in usages), "output_total": sum(u["output"] for u in usages),
            "last_calls": len(last.tool_calls), "answer": last.content,
            "model_name": last.response_metadata.get("model_name")}


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    question = QUESTIONS[mode]
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            for graph_name, graph in [("rule", rule_graph), ("model", model_graph)]:
                row = {"mode": mode, "graph": graph_name, "round": round_no, "question": question,
                       "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
                try:
                    result = graph.invoke({"messages": [HumanMessage(content=question)], "trace": []})
                    row.update(summarize(result))
                except Exception as error:  # 기록만 하고 다음으로
                    row["error"] = type(error).__name__ + ": " + str(error)[:300]
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                print(mode, graph_name, round_no, row.get("trace"), row.get("topics"),
                      row.get("usage"), row.get("error", ""))


if __name__ == "__main__":
    main()
