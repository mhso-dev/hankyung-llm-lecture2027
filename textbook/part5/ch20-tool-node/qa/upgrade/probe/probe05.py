"""Ch 20 05절(실습) 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe05.py <후보 A|B|C> <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  A : 「자료실 주차 규정을 알려 주세요.」(02절 5절 질문 그대로)
  B : 「주제어 주차로 자료실 규정을 찾아 주세요.」
  C : 「자료실에서 일반 도서를 며칠 빌릴 수 있나요?」(01절 대출 질문, 마지막 대안)
회차마다 실행 1(한도 10) → 노드 실행 수 셈 → 실행 2(한도 = 실행 1의 노드 실행 수)를 차례로 보낸다.
그래프·도구·오류 처리 함수·상태 형식은 05절 노트북 셀과 같은 코드(05-probe.md §0).
노트북과 다른 점은 하나: 모델 노드 함수가 부른 횟수와 응답을 목록 model_calls에 적는다(실행 2처럼 결과를 받지 못한 실행의 요청 수를 세려고).
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
from langchain.messages import AnyMessage, HumanMessage  # noqa: E402
from langchain.tools import tool  # noqa: E402
from langgraph.errors import GraphRecursionError  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402
from langgraph.graph.message import add_messages  # noqa: E402
from langgraph.prebuilt import ToolNode, tools_condition  # noqa: E402

QUESTIONS = {
    "A": "자료실 주차 규정을 알려 주세요.",
    "B": "주제어 주차로 자료실 규정을 찾아 주세요.",
    "C": "자료실에서 일반 도서를 며칠 빌릴 수 있나요?",
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


def handle_policy_error(error: ValueError):
    reason = str(error)
    return "규정을 찾지 못했습니다(" + reason + "). 이 도구로 찾을 수 있는 주제어는 대출, 운영, 연체입니다."


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    trace: Annotated[list[str], operator.add]


model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
tools = [lookup_policy]
bound_model = model.bind_tools(tools, parallel_tool_calls=False)
model_calls = []  # 노트북 밖 확인에서만 쓰는 목록


def usage_of(message):
    usage = message.usage_metadata
    if usage is None:
        return None
    return {"input": usage["input_tokens"], "output": usage["output_tokens"],
            "cache_read": usage.get("input_token_details", {}).get("cache_read")}


def call_model(state):
    response = bound_model.invoke(state["messages"])
    model_calls.append({"tool_calls": [[c["name"], c["args"]] for c in response.tool_calls],
                        "usage": usage_of(response), "content": response.content})
    return {"messages": [response], "trace": ["model"]}


policy_node = ToolNode(tools, handle_tool_errors=handle_policy_error)
path_map = {"tools": "tools", END: END}
builder = StateGraph(AgentState)
builder.add_node("model", call_model)
builder.add_node("tools", policy_node)
builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition, path_map)
builder.add_edge("tools", "model")
graph = builder.compile()


def summarize(result):
    kinds, calls, tool_out, usages, req_ids, tool_ids = [], [], [], [], [], []
    for message in result["messages"]:
        kind = type(message).__name__
        kinds.append(kind)
        if kind == "AIMessage":
            for c in message.tool_calls:
                calls.append([c["name"], c["args"]])
                req_ids.append(c["id"])
            usages.append(usage_of(message))
        if kind == "ToolMessage":
            tool_out.append({"status": message.status, "content": message.content})
            tool_ids.append(message.tool_call_id)
    last = result["messages"][-1]
    steps = result["trace"].count("model") + len(tool_out)
    return {"trace": result["trace"], "kinds": kinds, "calls": calls, "tool_messages": tool_out,
            "id_pair": req_ids == tool_ids, "usage": usages, "steps": steps,
            "last_calls": len(last.tool_calls), "answer": last.content,
            "model_name": last.response_metadata.get("model_name")}


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    question = QUESTIONS[mode]
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            row = {"mode": mode, "round": round_no, "question": question,
                   "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            state = {"messages": [HumanMessage(content=question)], "trace": []}
            model_calls.clear()
            try:
                result = graph.invoke(state, {"recursion_limit": 10})
                row["run1"] = summarize(result)
                row["run1"]["model_calls"] = len(model_calls)
            except Exception as error:  # 기록만 하고 다음으로
                row["run1_error"] = type(error).__name__ + ": " + str(error)[:300]
            steps = row.get("run1", {}).get("steps")
            if steps is not None:
                model_calls.clear()
                run2 = {"limit": steps}
                try:
                    result2 = graph.invoke(state, {"recursion_limit": steps})
                    run2["finished"] = True
                    run2["trace"] = result2["trace"]
                except GraphRecursionError as error:
                    run2["finished"] = False
                    run2["error"] = type(error).__name__
                    run2["error_first_line"] = str(error).splitlines()[0]
                except Exception as error:
                    run2["other_error"] = type(error).__name__ + ": " + str(error)[:300]
                run2["model_calls"] = len(model_calls)
                run2["calls_detail"] = list(model_calls)
                row["run2"] = run2
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            r1 = row.get("run1", {})
            print(mode, round_no, r1.get("trace"), r1.get("calls"), [t["status"] for t in r1.get("tool_messages", [])],
                  r1.get("steps"), r1.get("usage"), "| run2:", row.get("run2", {}).get("error"),
                  row.get("run2", {}).get("model_calls"), row.get("run1_error", ""))


if __name__ == "__main__":
    main()
