"""Ch 20 02절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe02.py <입력 P|K|D> <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  P : 주차 질문 + 손으로 만든 요청 {"topic": "주차"} → 오류 처리 함수 노드(After)
  K : 대출 질문 + 인자 이름이 틀린 요청 {"주제": "대출"} → 기본값 노드(값 바꿔 보기)
  D : 모델 없이 정해지는 두 경우(Before = P 입력 + 기본값 노드, K 입력 + 오류 처리 함수 노드) 한 번씩
그래프·도구·상태 형식·오류 처리 함수는 02절 노트북 셀과 같은 코드(02-probe.md §0).
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
from langchain.tools import ToolException, tool  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402
from langgraph.graph.message import add_messages  # noqa: E402
from langgraph.prebuilt import ToolNode, tools_condition  # noqa: E402

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


def call_model(state):
    response = bound_model.invoke(state["messages"])
    return {"messages": [response], "trace": ["model"]}


path_map = {"tools": "tools", END: END}


def build_graph(tool_node):
    builder = StateGraph(AgentState)
    builder.add_node("model", call_model)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "tools")
    builder.add_conditional_edges("model", tools_condition, path_map)
    builder.add_edge("tools", "model")
    return builder.compile()


def handle_policy_error(error: ValueError):
    reason = str(error)
    return "규정을 찾지 못했습니다(" + reason + "). 이 도구로 찾을 수 있는 주제어는 대출, 운영, 연체입니다."


PARK_Q = "자료실 주차 규정을 알려 주세요."
LOAN_Q = "자료실에서 일반 도서를 며칠 빌릴 수 있나요?"
park_call = {"name": "lookup_policy", "args": {"topic": "주차"}, "id": "hand_call_park", "type": "tool_call"}
key_call = {"name": "lookup_policy", "args": {"주제": "대출"}, "id": "hand_call_key", "type": "tool_call"}


def state_of(question, call):
    return {"messages": [HumanMessage(content=question), AIMessage(content="", tool_calls=[call])], "trace": []}


default_graph = build_graph(ToolNode(tools))
policy_graph = build_graph(ToolNode(tools, handle_tool_errors=handle_policy_error))


def summarize(result):
    kinds, calls, tools_out, usages, req_ids, msg_ids = [], [], [], [], [], []
    for message in result["messages"]:
        kind = type(message).__name__
        kinds.append(kind)
        if kind == "AIMessage":
            calls.append([[c["name"], c["args"]] for c in message.tool_calls])
            for c in message.tool_calls:
                req_ids.append(c["id"])
            usage = message.usage_metadata
            if usage:
                usages.append({"input": usage["input_tokens"], "output": usage["output_tokens"],
                               "cache_read": usage.get("input_token_details", {}).get("cache_read")})
        if kind == "ToolMessage":
            tools_out.append({"status": message.status, "content": message.content, "name": message.name,
                              "id": message.tool_call_id})
            msg_ids.append(message.tool_call_id)
    last = result["messages"][-1]
    return {"trace": result["trace"], "kinds": kinds, "calls": calls, "tool_messages": tools_out,
            "id_pair": req_ids == msg_ids, "n_requests": len(result["trace"]), "usage": usages,
            "last_calls": len(last.tool_calls), "answer": last.content,
            "model_name": last.response_metadata.get("model_name")}


def run_det(out):
    rows = []
    for label, graph, question, call in [("before", default_graph, PARK_Q, park_call),
                                         ("key_policy", policy_graph, LOAN_Q, key_call)]:
        row = {"mode": "D", "case": label, "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
        try:
            graph.invoke(state_of(question, call))
            row["error"] = None
        except (ValueError, ToolException) as error:
            row["error"] = type(error).__name__ + ": " + str(error)[:300]
        rows.append(row)
        print(row)
    with open(out, "a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    if mode == "D":
        run_det(out)
        return
    if mode == "P":
        graph, question, call = policy_graph, PARK_Q, park_call
    else:
        graph, question, call = default_graph, LOAN_Q, key_call
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            row = {"mode": mode, "round": round_no, "question": question, "call": call,
                   "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            try:
                result = graph.invoke(state_of(question, call))
                row.update(summarize(result))
            except Exception as error:  # 기록만 하고 다음 회차로
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(mode, round_no, row.get("trace"), row.get("kinds"), row.get("calls"), row.get("id_pair"),
                  [t["status"] for t in row.get("tool_messages", [])], row.get("usage"), row.get("error", ""))


if __name__ == "__main__":
    main()
