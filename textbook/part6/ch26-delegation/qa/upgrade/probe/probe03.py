"""Ch 26 03절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe03.py P1 <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  P1 : 모델 분류 노드 + Send 팬아웃 + 전문 에이전트 노드 + 종합 노드 그래프 — 노트북 6~7절 본 실행과 같은 코드
입력·규정 글·시스템 메시지 글·양식 클래스는 03-probe.md §0과 같다(노트북과 같은 코드).
노드 classify_by_model은 노트북과 같고, 기록용으로 받은 결과를 probe_log에 복사하는 한 줄만 더했다(요청 수 같음).
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
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import AnyMessage, HumanMessage  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402
from langgraph.types import Send  # noqa: E402

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


class DeskChoice(BaseModel):
    desks: list[Literal["loan_desk", "interlibrary_desk", "facility_desk"]] = Field(description="문의에 답할 담당 이름 목록")


classify_text = "도서관 자료실 문의 창구의 안내 도우미입니다. 문의를 읽고 답할 담당을 모두 고르세요."
classify_text = classify_text + " loan_desk는 대출·반납·연장·연체, interlibrary_desk는 다른 도서관 책을 빌려 오는 상호대차를 맡습니다."
classify_text = classify_text + " facility_desk는 자료실 운영 시간과 시설을 맡습니다. 맡을 담당이 없으면 빈 목록을 내세요."
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


def send_to_desks(state):
    sends = []
    for desk in state["desks"]:
        branch = {"desk": desk, "question": state["question"]}
        sends.append(Send(desk, branch))
    return sends


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

first_question = "빌린 책을 연장하려면 어떻게 하나요? 토요일 운영 시간도 알려 주세요."


def sum_usage(messages):
    total = {"requests": 0, "input_tokens": 0, "output_tokens": 0}
    for message in messages:
        if type(message).__name__ == "AIMessage":
            usage = message.usage_metadata
            total["requests"] = total["requests"] + 1
            total["input_tokens"] = total["input_tokens"] + usage["input_tokens"]
            total["output_tokens"] = total["output_tokens"] + usage["output_tokens"]
    return total


def cost(usage):
    # 2026-09-17 요금표(100만 토큰당 달러) — 청구 금액 아님
    return (usage["input_tokens"] * 0.75 + usage["output_tokens"] * 4.50) / 1000000


def run_p1(out):
    probe_log.clear()
    row = {"case": "P1", "time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            model_config = {"recursion_limit": 10}
            model_input = {"question": first_question, "desks": [], "answers": [], "summary": "", "responses": []}
            model_result = model_graph.invoke(model_input, model_config)
            usage = sum_usage(model_result["responses"])
            row["desks"] = model_result["desks"]
            row["desk_set"] = sorted(model_result["desks"])
            row["answer_rows"] = len(model_result["answers"])
            row["answer_desks"] = sorted(a["desk"] for a in model_result["answers"])
            row["responses"] = len(model_result["responses"])
            row["response_names"] = [m.name for m in model_result["responses"]]
            row["requests"] = usage["requests"]
            row["input_tokens"] = usage["input_tokens"]
            row["output_tokens"] = usage["output_tokens"]
            row["cost_usd"] = round(cost(usage), 6)
            row["parsing_error"] = [str(r["parsing_error"]) for r in probe_log]
            row["summary_lines"] = len([l for l in model_result["summary"].split("\n") if l])
            row["summary"] = model_result["summary"]
            row["reply_lengths"] = [len(a["reply"]) for a in model_result["answers"]]
            row["struct_rows_eq_desks"] = len(model_result["answers"]) == len(model_result["desks"])
            row["struct_req_eq_desks_plus1"] = usage["requests"] == len(model_result["desks"]) + 1
            row["struct_resp_eq_req"] = len(model_result["responses"]) == usage["requests"]
        except Exception as error:  # 기록만 하고 다시 보내지 않음
            row["error"] = type(error).__name__ + ": " + str(error)[:300]
    row["warnings"] = [str(w.message)[:200] for w in caught]
    out.write(json.dumps(row, ensure_ascii=False) + "\n")
    out.flush()
    print(json.dumps({k: row.get(k) for k in ["time", "desks", "answer_rows", "requests", "input_tokens", "output_tokens", "cost_usd", "parsing_error", "error", "warnings"]}, ensure_ascii=False))


if __name__ == "__main__":
    case, count, path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    with open(path, "a", encoding="utf-8") as out:
        for _ in range(count):
            if case == "P1":
                run_p1(out)
