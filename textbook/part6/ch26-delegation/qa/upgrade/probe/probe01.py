"""Ch 26 01절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe01.py <P1|P2> <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  P1 : 대출 연장 문의 한 줄로 중앙 에이전트 실행 — 노트북 본 실행과 같은 코드
  P2 : 앞 차례 기록 두 줄(손으로 적음) 뒤에 같은 문의 — 값 바꿔 보기 후보
입력·규정 글·시스템 메시지 글·도구는 01-probe.md §0과 같다(노트북과 같은 코드).
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")

from langchain.agents import create_agent  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import AIMessage, HumanMessage  # noqa: E402
from langchain.tools import tool  # noqa: E402

model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
loan_rules = "[교재용 대출·반납 규정] 일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다. 반납 예정일 전에 한 번, 7일 연장할 수 있습니다. 예약한 사람이 있는 책은 연장할 수 없습니다. 연체한 일수만큼 새 대출이 제한됩니다."
loan_desk_text = "도서관 자료실의 대출 규정 담당입니다. 아래 교재용 규정만 근거로 두 문장의 한국어로 답하세요.\n" + loan_rules
loan_desk = create_agent(model, tools=[], system_prompt=loan_desk_text)
specialist_runs = []


@tool
def ask_loan_desk(question: str):
    """도서관 대출·반납 규정을 묻는 질문 하나를 대출 규정 담당에게 맡기고, 담당의 답 글을 받습니다."""
    inner_input = {"messages": [HumanMessage(content=question)]}
    inner_result = loan_desk.invoke(inner_input)
    specialist_runs.append(inner_result["messages"])
    return inner_result["messages"][-1].text


central_text = "도서관 자료실 문의 창구의 안내 도우미입니다. 대출·반납 규정을 묻는 질문은 직접 답하지 말고 ask_loan_desk 도구에 맡기세요. 도구가 준 답을 바탕으로 두 문장의 한국어로 답하세요."
supervisor = create_agent(model, tools=[ask_loan_desk], system_prompt=central_text)
run_limit = {"recursion_limit": 10}
QUESTION = "빌린 책의 반납 날짜를 늘리려면 어떻게 하나요?"
HISTORY = [HumanMessage(content="자료실은 토요일에도 여나요?"), AIMessage(content="네, 토요일에는 10:00~17:00에 운영합니다.")]


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
    return (usage["input_tokens"] * 0.75 + usage["output_tokens"] * 4.50) / 1000000


def kinds(messages):
    return [type(m).__name__ for m in messages]


def main():
    global specialist_runs
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            row = {"mode": mode, "round": round_no, "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            specialist_runs = []
            if mode == "P1":
                messages = [HumanMessage(content=QUESTION)]
            else:
                messages = HISTORY + [HumanMessage(content=QUESTION)]
            try:
                result = supervisor.invoke({"messages": messages}, run_limit)
                outer = result["messages"]
                row["outer_n"] = len(outer)
                row["outer_kinds"] = kinds(outer)
                ais = [m for m in outer if type(m).__name__ == "AIMessage"]
                row["calls_per_response"] = [len(m.tool_calls) for m in ais]
                row["tool_names"] = [c["name"] for m in ais for c in m.tool_calls]
                passed = [c["args"].get("question") for m in ais for c in m.tool_calls]
                row["passed"] = passed
                row["runs"] = len(specialist_runs)
                row["inner_n"] = [len(r) for r in specialist_runs]
                row["inner_kinds"] = [kinds(r) for r in specialist_runs]
                row["inner_first_in_passed"] = [r[0].content in passed for r in specialist_runs]
                tool_contents = [m.content for m in outer if type(m).__name__ == "ToolMessage"]
                inner_last = [r[-1].text for r in specialist_runs]
                row["toolmsg_eq_inner_last"] = [c in inner_last for c in tool_contents]
                row["system_in_lists"] = [k for k in row["outer_kinds"] if k == "SystemMessage"] + [k for r in row["inner_kinds"] for k in r if k == "SystemMessage"]
                hist_words = ["토요일", "10:00~17:00"]
                row["history_in_inner"] = any(w in str(m.content) for r in specialist_runs for m in r for w in hist_words)
                ou = sum_usage(outer)
                row["outer_usage"] = ou
                inner_total = {"requests": 0, "input_tokens": 0, "output_tokens": 0}
                for r in specialist_runs:
                    iu = sum_usage(r)
                    for k in inner_total:
                        inner_total[k] = inner_total[k] + iu[k]
                row["inner_usage"] = inner_total
                total = {k: ou[k] + inner_total[k] for k in ou}
                row["total_requests"] = total["requests"]
                tool_responses = len([m for m in ais if m.tool_calls])
                row["formula_ok"] = total["requests"] == (tool_responses + 1) + len(specialist_runs) * 1
                row["outer_eq_central"] = ou["requests"] == len(ais)
                row["cost"] = round(estimate_cost(total), 6)
                row["answer"] = outer[-1].text
                row["answer_len"] = len(outer[-1].text)
                row["inner_answers"] = inner_last
            except Exception as error:  # 기록만 하고 다음 회차로(다시 보내지 않음)
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False)[:1800])


if __name__ == "__main__":
    main()
