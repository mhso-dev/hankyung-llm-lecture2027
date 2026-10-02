"""Ch 26 04절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe04.py P1|P2|P3|P4 <회차 수> <기록 파일(JSONL, 이어 쓰기)>
      python probe04.py BUILD   (가짜 키 글로 객체·그래프만 만들고 요청은 보내지 않음 — 구조 확인용)
  P1 : 서브에이전트(중앙 에이전트 + 분야 이름을 받는 도구 하나) — 노트북 3절
  P2 : 핸드오프(안내 담당 + 넘기기 도구 하나 + 분야 노드 셋) — 노트북 4절
  P3 : 라우터(03절 그래프 그대로) — 노트북 5절
  P4 : P1 중앙 에이전트에 호출 한도 1 — 노트북 7절
입력·규정 글·시스템 메시지 글·도구 글은 04-probe.md §0과 같다(노트북과 같은 코드).
노드 classify_by_model은 노트북과 같고, 기록용으로 받은 결과를 probe_log에 복사하는 한 줄만 더했다(요청 수 같음).
도구 파일 함수(message_kinds·usage_with_specialists·writer_names·send_to_desks·sum_usage)는 01~03절 노트북 셀과 같은 본문을 여기에 적었다.
"""
import json
import operator
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Literal

from dotenv import load_dotenv
from typing_extensions import TypedDict

ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")

from pydantic import BaseModel, Field  # noqa: E402
from langchain.agents import create_agent  # noqa: E402
from langchain.agents.middleware import ModelCallLimitMiddleware  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import AnyMessage, HumanMessage, ToolMessage  # noqa: E402
from langchain.tools import ToolRuntime, tool  # noqa: E402
from langchain_core.exceptions import ModelInvalidRequestError  # noqa: E402
from langgraph.checkpoint.memory import InMemorySaver  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402
from langgraph.graph.message import add_messages  # noqa: E402
from langgraph.types import Command, Send  # noqa: E402


# ---- 도구 파일 함수(01·02·03절 노트북 셀 본문 그대로, Ch 19 05절 sum_usage)
def sum_usage(messages):
    total = {"requests": 0, "input_tokens": 0, "output_tokens": 0}
    for message in messages:
        if type(message).__name__ == "AIMessage":
            usage = message.usage_metadata
            total["requests"] = total["requests"] + 1
            total["input_tokens"] = total["input_tokens"] + usage["input_tokens"]
            total["output_tokens"] = total["output_tokens"] + usage["output_tokens"]
    return total


def message_kinds(messages):
    kinds = []
    for message in messages:
        kinds.append(type(message).__name__)
    return kinds


def usage_with_specialists(new_messages, inner_runs):
    total = sum_usage(new_messages)
    for inner_list in inner_runs:
        inner_usage = sum_usage(inner_list)
        for key in total:
            total[key] = total[key] + inner_usage[key]
    return total


def writer_names(messages):
    names = []
    for message in messages:
        if type(message).__name__ == "AIMessage":
            names.append(message.name)
    return names


def send_to_desks(state):
    sends = []
    for desk in state["desks"]:
        branch = {"desk": desk, "question": state["question"]}
        sends.append(Send(desk, branch))
    return sends


# ---- 노트북 셀과 같은 코드
model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")

desk_names = ["loan_desk", "interlibrary_desk", "facility_desk"]
loan_rules = "[교재용 대출·반납 규정] 일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다. 반납 예정일 전에 한 번, 7일 연장할 수 있습니다."
loan_rules = loan_rules + " 예약한 사람이 있는 책은 연장할 수 없습니다. 연체한 일수만큼 새 대출이 제한됩니다."
interlibrary_rules = "[교재용 상호대차 규정] 다른 도서관의 책은 자료실 창구에서 상호대차로 신청합니다."
interlibrary_rules = interlibrary_rules + " 신청한 책은 보통 3~5일 뒤에 도착합니다."
interlibrary_rules = interlibrary_rules + " 책이 도착하면 문자로 알리고, 7일 안에 찾아가야 합니다."
facility_rules = "[교재용 시설 규정] 자료실은 평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다."

answer_rule = " 문의 가운데 아래 교재용 규정에 해당하는 부분에만 한 문장의 한국어로 답하세요.\n"
loan_text = "도서관 자료실의 대출 규정 담당입니다." + answer_rule + loan_rules
interlibrary_text = "도서관 자료실의 상호대차 담당입니다." + answer_rule + interlibrary_rules
facility_text = "도서관 자료실의 시설 담당입니다." + answer_rule + facility_rules
desk_agents = {}
desk_agents["loan_desk"] = create_agent(model, tools=[], system_prompt=loan_text, name="loan_desk")
desk_agents["interlibrary_desk"] = create_agent(model, tools=[], system_prompt=interlibrary_text, name="interlibrary_desk")
desk_agents["facility_desk"] = create_agent(model, tools=[], system_prompt=facility_text, name="facility_desk")

specialist_runs = []


@tool
def ask_desk_agent(desk: str, question: str):
    """문의 가운데 한 분야 부분을 그 분야 담당(loan_desk·interlibrary_desk·facility_desk)에게 맡기고, 담당의 답 글을 받습니다."""
    agent = desk_agents[desk]
    inner_input = {"messages": [HumanMessage(content=question)]}
    inner_result = agent.invoke(inner_input)
    specialist_runs.append(inner_result["messages"])
    return inner_result["messages"][-1].text


desk_guide = " loan_desk는 대출·반납·연장·연체, interlibrary_desk는 다른 도서관 책을 빌려 오는 상호대차를 맡습니다."
desk_guide = desk_guide + " facility_desk는 자료실 운영 시간과 시설을 맡습니다."
central_text = "도서관 자료실 문의 창구의 안내 도우미입니다. 규정을 묻는 부분은 직접 답하지 말고 ask_desk_agent 도구로 담당에게 맡기세요."
central_text = central_text + desk_guide + " 담당이 준 답을 바탕으로 두 문장의 한국어로 답하세요."
supervisor = create_agent(model, tools=[ask_desk_agent], system_prompt=central_text)

question_text = "빌린 책을 연장하려면 어떻게 하나요? 토요일 운영 시간도 알려 주세요."
limit_config = {"recursion_limit": 10}


def answered_desks(inner_runs, names):
    desks = []
    for desk in names:
        for inner_list in inner_runs:
            if inner_list[-1].name == desk:
                desks.append(desk)
    return desks


class TeamState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    active_agent: str


@tool
def transfer_to_desk(desk: str, runtime: ToolRuntime):
    """문의를 맡을 담당 한 명(loan_desk·interlibrary_desk·facility_desk)에게 대화를 넘깁니다."""
    last_message = runtime.state["messages"][-1]
    transfer_message = ToolMessage(content=desk + " 담당에게 넘겼습니다.", tool_call_id=runtime.tool_call_id)
    update = {"active_agent": desk, "messages": [last_message, transfer_message]}
    return Command(goto=desk, update=update, graph=Command.PARENT)


front_text = "도서관 자료실 문의 창구의 안내 담당입니다. 문의에 직접 답하지 말고, 맡을 담당 한 명을 골라 transfer_to_desk 도구로 넘기세요."
front_text = front_text + desk_guide
front_agent = create_agent(model, tools=[transfer_to_desk], system_prompt=front_text, name="front_desk")

team_builder = StateGraph(TeamState)
team_builder.add_node("front_desk", front_agent, destinations=("loan_desk", "interlibrary_desk", "facility_desk"))
for desk in desk_names:
    team_builder.add_node(desk, desk_agents[desk])
    team_builder.add_edge(desk, END)
team_builder.add_edge(START, "front_desk")
team_graph = team_builder.compile(checkpointer=InMemorySaver())


class DeskChoice(BaseModel):
    desks: list[Literal["loan_desk", "interlibrary_desk", "facility_desk"]] = Field(description="문의에 답할 담당 이름 목록")


classify_text = "도서관 자료실 문의 창구의 안내 도우미입니다. 문의를 읽고 답할 담당을 모두 고르세요."
classify_text = classify_text + desk_guide + " 맡을 담당이 없으면 빈 목록을 내세요."
classifier = model.with_structured_output(DeskChoice, include_raw=True)


class ModelRouteState(TypedDict):
    question: str
    desks: list[str]
    answers: Annotated[list[dict], operator.add]
    summary: str
    responses: Annotated[list[AnyMessage], operator.add]


probe_log = []


def classify_by_model(state):
    messages = [("system", classify_text), ("user", state["question"])]
    result = classifier.invoke(messages)
    probe_log.append(result)
    choice = result["parsed"]
    return {"desks": choice.desks, "responses": [result["raw"]]}


def ask_desk(state):
    agent = desk_agents[state["desk"]]
    result = agent.invoke({"messages": [HumanMessage(content=state["question"])]})
    reply = result["messages"][-1]
    answer = {"desk": state["desk"], "reply": reply.text}
    return {"answers": [answer], "responses": [reply]}


def join_answers(state):
    summary = ""
    for desk in desk_names:
        for answer in state["answers"]:
            if answer["desk"] == desk:
                summary = summary + "[" + desk + "] " + answer["reply"] + "\n"
    return {"summary": summary}


model_builder = StateGraph(ModelRouteState)
model_builder.add_node("classify", classify_by_model)
model_builder.add_node("join_answers", join_answers)
for desk in desk_names:
    model_builder.add_node(desk, ask_desk)
    model_builder.add_edge(desk, "join_answers")
model_builder.add_edge(START, "classify")
model_builder.add_conditional_edges("classify", send_to_desks, desk_names)
model_builder.add_edge("join_answers", END)
model_graph = model_builder.compile()

call_limit = ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")
limited_agent = create_agent(model, tools=[ask_desk_agent], system_prompt=central_text, middleware=[call_limit])


def is_complete(collected, needed, has_final):
    for desk in needed:
        if desk not in collected:
            return False
    return has_final


needed_desks = ["loan_desk", "facility_desk"]


# ---- 기록용(노트북에 없음)
def cost(usage):
    # 2026-09-17 요금표(100만 토큰당 달러) — 청구 금액 아님
    return round((usage["input_tokens"] * 0.75 + usage["output_tokens"] * 4.50) / 1000000, 6)


def calls_of(messages):
    rows = []
    for m in messages:
        if type(m).__name__ == "AIMessage":
            rows.append([[c["name"], c["args"].get("desk"), c["args"].get("question")] for c in m.tool_calls])
    return rows


def run_case(case, out):
    specialist_runs.clear()
    probe_log.clear()
    row = {"case": case, "time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            if case in ("P1", "P4"):
                agent = supervisor if case == "P1" else limited_agent
                sub_input = {"messages": [HumanMessage(content=question_text)]}
                result = agent.invoke(sub_input, limit_config)
                new = result["messages"][1:]
                last = new[-1]
                row["kinds"] = message_kinds(new)
                row["calls_per_response"] = calls_of(new)
                row["specialist_calls"] = len(specialist_runs)
                row["inner_lens"] = [len(r) for r in specialist_runs]
                row["answered"] = answered_desks(specialist_runs, desk_names)
                row["tool_msgs"] = row["kinds"].count("ToolMessage")
                row["tool_calls"] = sum(len(m.tool_calls) for m in new if type(m).__name__ == "AIMessage")
                row["last_usage_none"] = last.usage_metadata is None
                row["last_tool_calls"] = len(last.tool_calls)
                row["last_text"] = last.text
                row["final"] = last.usage_metadata is not None and len(last.tool_calls) == 0
                model_new = [m for m in new if not (type(m).__name__ == "AIMessage" and m.usage_metadata is None)]
                usage = usage_with_specialists(model_new, specialist_runs)
                row["central_model_responses"] = sum(1 for m in model_new if type(m).__name__ == "AIMessage")
                row["requests"] = usage["requests"]
                row["formula_ok"] = usage["requests"] == (row["central_model_responses"]) + len(specialist_runs)
                row["input_tokens"], row["output_tokens"], row["cost_usd"] = usage["input_tokens"], usage["output_tokens"], cost(usage)
                row["complete"] = is_complete(row["answered"], needed_desks, row["final"])
            elif case == "P2":
                # P2 첫 판(체크포인터 없음)은 5/5 서비스 오류라 기록만 남기고, P2b부터 노트북 판(체크포인터 + 오류 받기 + get_state)
                hand_config = {"configurable": {"thread_id": "hand-" + row["time"]}, "recursion_limit": 10}
                hand_input = {"messages": [HumanMessage(content=question_text)], "active_agent": ""}
                try:
                    team_graph.invoke(hand_input, hand_config)
                    row["hand_error"] = None
                except ModelInvalidRequestError as error:
                    error_text = error.body["message"]
                    row["hand_error"] = type(error).__name__
                    row["status_code"] = error.status_code
                    row["error_first"] = error_text.split(". ")[0]
                    row["body_keys"] = sorted(error.body)
                hand_state = team_graph.get_state(hand_config)
                new = hand_state.values["messages"][1:]
                usage = sum_usage(new)
                row["kinds"] = message_kinds(new)
                row["calls_per_response"] = calls_of(new)
                row["transfer_calls"] = len(new[0].tool_calls)
                row["writers"] = writer_names(new)
                row["active_agent"] = hand_state.values["active_agent"]
                row["next"] = list(hand_state.next)
                row["final"] = new[-1].name == hand_state.values["active_agent"]
                tms = [m for m in new if type(m).__name__ == "ToolMessage"]
                row["tool_msg_texts"] = [m.content for m in tms]
                row["pair_first_ok"] = len(tms) > 0 and tms[0].tool_call_id == new[0].tool_calls[0]["id"]
                row["requests"] = usage["requests"]
                row["input_tokens"], row["output_tokens"], row["cost_usd"] = usage["input_tokens"], usage["output_tokens"], cost(usage)
                row["last_text"] = new[-1].text
                row["complete"] = is_complete(row["writers"], needed_desks, row["final"])
            elif case == "P3":
                route_input = {"question": question_text, "desks": [], "answers": [], "summary": "", "responses": []}
                result = model_graph.invoke(route_input, limit_config)
                usage = sum_usage(result["responses"])
                route_desks = [a["desk"] for a in result["answers"]]
                row["desks"] = result["desks"]
                row["answer_rows"] = len(result["answers"])
                row["answer_desks_sorted"] = sorted(route_desks)
                row["parsing_error"] = [str(r["parsing_error"]) for r in probe_log]
                row["requests"] = usage["requests"]
                row["formula_ok"] = usage["requests"] == 1 + len(result["desks"])
                row["input_tokens"], row["output_tokens"], row["cost_usd"] = usage["input_tokens"], usage["output_tokens"], cost(usage)
                row["summary"] = result["summary"]
                row["final"] = result["summary"] != ""
                row["complete"] = is_complete(route_desks, needed_desks, row["final"])
        except Exception as error:  # 기록만 하고 다시 보내지 않음
            row["error"] = type(error).__name__ + ": " + str(error)[:400]
    row["warnings"] = [str(w.message)[:200] for w in caught]
    out.write(json.dumps(row, ensure_ascii=False) + "\n")
    out.flush()
    keys = ["time", "hand_error", "status_code", "error_first", "transfer_calls", "next", "tool_msg_texts", "kinds", "calls_per_response", "specialist_calls", "answered", "writers", "active_agent", "desks", "requests",
            "input_tokens", "output_tokens", "cost_usd", "final", "complete", "last_text", "error", "warnings"]
    print(json.dumps({k: row[k] for k in keys if k in row}, ensure_ascii=False))


if __name__ == "__main__":
    if sys.argv[1] == "BUILD":
        print("front nodes:", list(front_agent.get_graph().nodes))
        print("limited nodes:", list(limited_agent.get_graph().nodes))
        print("team nodes:", list(team_builder.nodes))
        print("team structure:")
        print(team_graph.get_graph().draw_mermaid())
        print("classify_text:", classify_text)
        print("tool args:", list(ask_desk_agent.args), list(transfer_to_desk.args))
        raise SystemExit(0)
    case, count, path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    with open(path, "a", encoding="utf-8") as out:
        for _ in range(count):
            run_case("P2" if case == "P2b" else case, out)
