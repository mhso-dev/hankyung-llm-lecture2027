"""Ch 26 02절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe02.py P1 <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  P1 : 두 담당 바깥 그래프를 같은 스레드로 두 차례 실행 — 노트북 6~7절 본 실행과 같은 코드
입력·규정 글·시스템 메시지 글·도구는 02-probe.md §0과 같다(노트북과 같은 코드).
"""
import json
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from typing_extensions import TypedDict

ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")

from langchain.agents import create_agent  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import AnyMessage, HumanMessage, ToolMessage  # noqa: E402
from langchain.tools import ToolRuntime, tool  # noqa: E402
from langgraph.checkpoint.memory import InMemorySaver  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402
from langgraph.graph.message import add_messages  # noqa: E402
from langgraph.types import Command  # noqa: E402

model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")


class TeamState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    active_agent: str


def pick_desk(state):
    if state["active_agent"] == "interlibrary_desk":
        return "interlibrary_desk"
    return "loan_desk"


interlibrary_rules = "[교재용 상호대차 규정] 다른 도서관의 책은 자료실 창구에서 상호대차로 신청합니다. 신청한 책은 보통 3~5일 뒤에 도착합니다. 책이 도착하면 문자로 알리고, 7일 안에 찾아가야 합니다."
interlibrary_text = "도서관 자료실의 상호대차 담당입니다. 아래 교재용 규정만 근거로 두 문장의 한국어로 답하세요.\n" + interlibrary_rules
interlibrary_agent = create_agent(model, tools=[], system_prompt=interlibrary_text, name="interlibrary_desk")


@tool
def transfer_to_interlibrary(runtime: ToolRuntime):
    """다른 도서관의 책을 빌려 오는 상호대차 문의를 상호대차 담당에게 넘깁니다."""
    last_message = runtime.state["messages"][-1]
    transfer_message = ToolMessage(content="상호대차 담당에게 넘겼습니다.", tool_call_id=runtime.tool_call_id)
    update = {"active_agent": "interlibrary_desk", "messages": [last_message, transfer_message]}
    return Command(goto="interlibrary_desk", update=update, graph=Command.PARENT)


loan_rules = "[교재용 대출·반납 규정] 일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다. 반납 예정일 전에 한 번, 7일 연장할 수 있습니다. 예약한 사람이 있는 책은 연장할 수 없습니다. 연체한 일수만큼 새 대출이 제한됩니다."
loan_text = "도서관 자료실의 대출 규정 담당입니다. 아래 교재용 규정만 근거로 두 문장의 한국어로 답하세요. 다른 도서관의 책을 빌려 오는 상호대차 문의는 직접 답하지 말고 transfer_to_interlibrary 도구로 넘기세요.\n" + loan_rules
loan_agent = create_agent(model, tools=[transfer_to_interlibrary], system_prompt=loan_text, name="loan_desk")

team_builder = StateGraph(TeamState)
team_builder.add_node("loan_desk", loan_agent, destinations=("interlibrary_desk", END))
team_builder.add_node("interlibrary_desk", interlibrary_agent)
team_builder.add_conditional_edges(START, pick_desk, ["loan_desk", "interlibrary_desk"])
team_builder.add_edge("interlibrary_desk", END)
team_graph = team_builder.compile(checkpointer=InMemorySaver())

FIRST = "다른 도서관에 있는 책도 빌려 볼 수 있나요?"
SECOND = "신청하면 며칠 뒤에 받을 수 있나요?"


def sum_usage(messages):
    total = {"requests": 0, "input_tokens": 0, "output_tokens": 0}
    for message in messages:
        if type(message).__name__ == "AIMessage":
            usage = message.usage_metadata
            total["requests"] = total["requests"] + 1
            total["input_tokens"] = total["input_tokens"] + usage["input_tokens"]
            total["output_tokens"] = total["output_tokens"] + usage["output_tokens"]
    return total


def estimate_cost(usage):
    return round((usage["input_tokens"] * 0.75 + usage["output_tokens"] * 4.50) / 1000000, 6)


def kinds(messages):
    return [type(m).__name__ for m in messages]


def writers(messages):
    return [m.name for m in messages if type(m).__name__ == "AIMessage"]


def calls(messages):
    return [[c["name"] for c in m.tool_calls] for m in messages if type(m).__name__ == "AIMessage"]


def pairs(messages):
    req = [c["id"] for m in messages if type(m).__name__ == "AIMessage" for c in m.tool_calls]
    got = [m.tool_call_id for m in messages if type(m).__name__ == "ToolMessage"]
    return req == got and len(req) > 0


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    assert mode == "P1"
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            row = {"mode": mode, "round": round_no, "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            config = {"configurable": {"thread_id": "probe-team-" + str(round_no) + "-" + row["at"]}, "recursion_limit": 10}
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                try:
                    first = team_graph.invoke({"messages": [HumanMessage(content=FIRST)], "active_agent": ""}, config)
                    fm = first["messages"]
                    row["t1_n"] = len(fm)
                    row["t1_kinds"] = kinds(fm)
                    row["t1_calls"] = calls(fm)
                    row["t1_writers"] = writers(fm)
                    row["t1_pair"] = pairs(fm)
                    row["t1_tool_texts"] = [m.content for m in fm if type(m).__name__ == "ToolMessage"]
                    row["t1_active"] = first["active_agent"]
                    row["t1_next"] = list(team_graph.get_state(config).next)
                    u1 = sum_usage(fm[1:])
                    row["t1_usage"] = u1
                    row["t1_cost"] = estimate_cost(u1)
                    row["t1_answer"] = fm[-1].text
                    row["t1_answer_len"] = len(fm[-1].text)
                    second = team_graph.invoke({"messages": [HumanMessage(content=SECOND)]}, config)
                    sm = second["messages"]
                    new = sm[len(fm):]
                    row["t2_new_kinds"] = kinds(new)
                    row["t2_writers"] = writers(sm[len(fm) + 1:])
                    row["t2_active"] = second["active_agent"]
                    row["t2_next"] = list(team_graph.get_state(config).next)
                    u2 = sum_usage(sm[len(fm) + 1:])
                    row["t2_usage"] = u2
                    row["t2_cost"] = estimate_cost(u2)
                    row["t2_answer"] = sm[-1].text
                    row["t2_answer_len"] = len(sm[-1].text)
                except Exception as error:  # noqa: BLE001
                    row["error"] = type(error).__name__ + ": " + str(error)[:300]
            row["warnings"] = [str(w.category.__name__) + ": " + str(w.message)[:200] for w in caught]
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False))


if __name__ == "__main__":
    main()
