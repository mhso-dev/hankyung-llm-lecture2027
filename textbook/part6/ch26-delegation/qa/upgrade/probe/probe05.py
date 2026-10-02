"""Ch 26 05절(챕터 끝 실습 절) 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe05.py A1|B1|A2|B2|L2|L1 <회차 수> <기록 파일(JSONL, 이어 쓰기)>
      python probe05.py BUILD   (객체만 만들고 요청은 보내지 않음 — 구조 확인용)
  §0 판(분류 모델을 앞에 둔 흐름 — 두 실행 2 후보가 규칙을 채우지 못해 쓰지 않음):
  A1·B1 : 실행 1 후보 문의(한 분야)
  A2·B2 : 실행 2 후보 문의(맡을 분야 없음)
  §0-2 판(노트북 판 — 04절 중앙 에이전트 + 호출 한도 + 완료 조건, 문의 A1):
  L2 : 호출 한도 2 — 노트북 6절(실행 1)
  L1 : 호출 한도 1 — 노트북 7절(실행 2)
입력·규정 글·시스템 메시지 글·도구 글·조립 함수는 05-probe.md §0·§0-2와 같다(노트북과 같은 코드).
노드 classify_by_model은 노트북과 같고, 기록용으로 받은 결과를 probe_log에 복사하는 한 줄만 더했다(요청 수 같음).
도구 파일 함수(message_kinds·usage_with_specialists·sum_usage·answered_desks·is_complete)는 01·04절 노트북 셀과 같은 본문을 여기에 적었다.
"""
import json
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")

from pydantic import BaseModel, Field  # noqa: E402
from langchain.agents import create_agent  # noqa: E402
from langchain.agents.middleware import ModelCallLimitMiddleware  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import HumanMessage  # noqa: E402
from langchain.tools import tool  # noqa: E402


# ---- 도구 파일 함수(01·04절 노트북 셀 본문 그대로, Ch 19 05절 sum_usage)
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


def answered_desks(inner_runs, names):
    desks = []
    for desk in names:
        for inner_list in inner_runs:
            if inner_list[-1].name == desk:
                desks.append(desk)
    return desks


def is_complete(collected, needed, has_final):
    for desk in needed:
        if desk not in collected:
            return False
    return has_final


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


class DeskChoice(BaseModel):
    desks: list[Literal["loan_desk", "interlibrary_desk", "facility_desk"]] = Field(description="문의에 답할 담당 이름 목록")


desk_guide = " loan_desk는 대출·반납·연장·연체, interlibrary_desk는 다른 도서관 책을 빌려 오는 상호대차를 맡습니다."
desk_guide = desk_guide + " facility_desk는 자료실 운영 시간과 시설을 맡습니다."
classify_text = "도서관 자료실 문의 창구의 안내 도우미입니다. 문의를 읽고 답할 담당을 모두 고르세요."
classify_text = classify_text + desk_guide + " 맡을 담당이 없으면 빈 목록을 내세요."
classifier = model.with_structured_output(DeskChoice, include_raw=True)

probe_log = []


def classify_by_model(state):
    messages = [("system", classify_text), ("user", state["question"])]
    result = classifier.invoke(messages)
    probe_log.append(result)
    choice = result["parsed"]
    return {"desks": choice.desks, "responses": [result["raw"]]}


specialist_runs = []


@tool
def ask_desk_agent(desk: str, question: str):
    """문의 가운데 한 분야 부분을 그 분야 담당(loan_desk·interlibrary_desk·facility_desk)에게 맡기고, 담당의 답 글을 받습니다."""
    agent = desk_agents[desk]
    inner_input = {"messages": [HumanMessage(content=question)]}
    inner_result = agent.invoke(inner_input)
    specialist_runs.append(inner_result["messages"])
    return inner_result["messages"][-1].text


central_text = "도서관 자료실 문의 창구의 안내 도우미입니다. 규정을 묻는 부분은 직접 답하지 말고 ask_desk_agent 도구로 담당에게 맡기세요."
central_text = central_text + desk_guide + " 담당이 준 답을 바탕으로 두 문장의 한국어로 답하세요."
supervisor = create_agent(model, tools=[ask_desk_agent], system_prompt=central_text)
limit_config = {"recursion_limit": 10}


def final_answer_given(new_messages):
    if len(new_messages) == 0:
        return False
    last = new_messages[-1]
    return last.usage_metadata is not None and len(last.tool_calls) == 0


def summarize_run(record, inner_runs):
    collected = answered_desks(inner_runs, desk_names)
    has_final = final_answer_given(record["center_new"])
    usage = usage_with_specialists(record["center_new"], inner_runs)
    route_usage = sum_usage(record["responses"])
    for key in usage:
        usage[key] = usage[key] + route_usage[key]
    done = is_complete(collected, record["needed"], has_final)
    return {"needed": record["needed"], "collected": collected, "final": has_final, "usage": usage, "complete": done}


def handle_inquiry(question):
    route = classify_by_model({"question": question})
    center_new = []
    if len(route["desks"]) != 0:
        center_input = {"messages": [HumanMessage(content=question)]}
        center_result = supervisor.invoke(center_input, limit_config)
        center_new = center_result["messages"][1:]
    return {"needed": route["desks"], "responses": route["responses"], "center_new": center_new}


# ---- §0-2 판(노트북 판) — 조립 함수와 기록 장치
def count_run_usage(new_messages, inner_runs):
    counted = new_messages
    if new_messages[-1].usage_metadata is None:
        counted = new_messages[:-1]
    return usage_with_specialists(counted, inner_runs)


def summarize_limited(new_messages, inner_runs, needed):
    collected = answered_desks(inner_runs, desk_names)
    last = new_messages[-1]
    has_final = last.usage_metadata is not None and len(last.tool_calls) == 0
    usage = count_run_usage(new_messages, inner_runs)
    done = is_complete(collected, needed, has_final)
    return {"collected": collected, "final": has_final, "usage": usage, "complete": done}


def handle_limited(limit, question):
    call_limit = ModelCallLimitMiddleware(run_limit=limit, exit_behavior="end")
    center = create_agent(model, tools=[ask_desk_agent], system_prompt=central_text, middleware=[call_limit])
    center_input = {"messages": [HumanMessage(content=question)]}
    center_result = center.invoke(center_input, limit_config)
    return center_result["messages"][1:]


needed_desks = ["loan_desk"]
LIMITS = {"L2": 2, "L1": 1}


QUESTIONS = {
    "A1": "빌린 책의 반납 날짜를 늘리려면 어떻게 하나요?",
    "B1": "책은 몇 권까지 빌릴 수 있나요?",
    "A2": "자료실에 우산을 두고 온 것 같아요.",
    "B2": "자료실 근처에 점심 먹을 식당이 있나요?",
}


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
    question = QUESTIONS["A1"] if case in LIMITS else QUESTIONS[case]
    row = {"case": case, "question": question, "time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            if case in LIMITS:
                new = handle_limited(LIMITS[case], question)
                summary = summarize_limited(new, specialist_runs, needed_desks)
                last = new[-1]
                row["limit"] = LIMITS[case]
                row["kinds"] = message_kinds(new)
                row["calls_per_response"] = calls_of(new)
                row["specialist_calls"] = len(specialist_runs)
                row["inner_lens"] = [len(r) for r in specialist_runs]
                row["tool_msgs"] = row["kinds"].count("ToolMessage")
                row["tool_calls"] = sum(len(m.tool_calls) for m in new if type(m).__name__ == "AIMessage")
                row["collected"] = summary["collected"]
                row["final"] = summary["final"]
                row["last_usage_none"] = last.usage_metadata is None
                row["requests"] = summary["usage"]["requests"]
                central_model = sum(1 for m in new if type(m).__name__ == "AIMessage" and m.usage_metadata is not None)
                row["formula_ok"] = summary["usage"]["requests"] == central_model + len(specialist_runs)
                row["complete"] = summary["complete"]
                row["input_tokens"], row["output_tokens"] = summary["usage"]["input_tokens"], summary["usage"]["output_tokens"]
                row["cost_usd"] = cost(summary["usage"])
                row["last_text"] = last.text
                raise StopIteration
            record = handle_inquiry(QUESTIONS[case])
            summary = summarize_run(record, specialist_runs)
            new = record["center_new"]
            row["needed"] = record["needed"]
            row["parsing_error"] = [str(r["parsing_error"]) for r in probe_log]
            row["center_called"] = len(new) != 0
            row["kinds"] = message_kinds(new)
            row["calls_per_response"] = calls_of(new)
            row["specialist_calls"] = len(specialist_runs)
            row["inner_lens"] = [len(r) for r in specialist_runs]
            row["tool_msgs"] = row["kinds"].count("ToolMessage")
            row["tool_calls"] = sum(len(m.tool_calls) for m in new if type(m).__name__ == "AIMessage")
            row["collected"] = summary["collected"]
            row["final"] = summary["final"]
            row["requests"] = summary["usage"]["requests"]
            central_responses = sum(1 for m in new if type(m).__name__ == "AIMessage")
            row["formula_ok"] = summary["usage"]["requests"] == 1 + central_responses + len(specialist_runs)
            row["complete"] = summary["complete"]
            row["input_tokens"], row["output_tokens"] = summary["usage"]["input_tokens"], summary["usage"]["output_tokens"]
            row["cost_usd"] = cost(summary["usage"])
            row["last_text"] = new[-1].text if new else None
        except StopIteration:
            pass
        except Exception as error:  # 기록만 하고 다시 보내지 않음
            row["error"] = type(error).__name__ + ": " + str(error)[:400]
    row["warnings"] = [str(w.message)[:200] for w in caught]
    out.write(json.dumps(row, ensure_ascii=False) + "\n")
    out.flush()
    keys = ["time", "limit", "needed", "parsing_error", "center_called", "kinds", "calls_per_response", "specialist_calls", "inner_lens", "collected", "final",
            "last_usage_none", "requests", "formula_ok", "complete", "input_tokens", "output_tokens", "cost_usd", "last_text", "error", "warnings"]
    print(json.dumps({k: row[k] for k in keys if k in row}, ensure_ascii=False))


if __name__ == "__main__":
    if sys.argv[1] == "BUILD":
        print("supervisor nodes:", list(supervisor.get_graph().nodes))
        print("classify_text:", classify_text)
        print("tool args:", list(ask_desk_agent.args))
        raise SystemExit(0)
    case, count, path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    with open(path, "a", encoding="utf-8") as out:
        for _ in range(count):
            run_case(case, out)
