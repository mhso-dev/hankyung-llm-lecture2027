"""Ch 21 07절(실습) 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe07.py <후보 A|B> <설정 R0|R3> <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  A  : 07-probe.md §0-2 입력 그대로
  B  : A + 시스템 메시지 글 끝 한 문장(07-probe.md §0-3)
  R0 : context={"member_id": "M-0317", "overdue_days": 0}
  R3 : context={"member_id": "M-0317", "overdue_days": 3}  (바꾼 값 — 실행 정보 하나)
자료·도구·실행 정보 형식은 01·03절 셀과 같은 코드, 양식 클래스는 07절에서 정한 것(07-probe.md §0-2).
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")

from typing_extensions import TypedDict  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402
from langchain.agents import create_agent  # noqa: E402
from langchain.agents.structured_output import ToolStrategy  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import HumanMessage  # noqa: E402
from langchain.tools import ToolRuntime, tool  # noqa: E402

QUESTION = "제가 지금 새 책을 빌릴 수 있는지 확인해 주세요. 일반 도서 대출 규정도 함께 알려 주세요."
POLICIES = {
    "대출": "일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.",
    "운영": "평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.",
    "연체": "연체한 일수만큼 새 대출이 제한됩니다.",
}
SYSTEM_A = ("교육센터 자료실 안내 도우미입니다. 자료실 규정을 묻는 질문에는 lookup_policy 도구로 찾은 규정 글에 근거해 답하세요. "
            "이용자가 지금 새 책을 빌릴 수 있는지 물으면 check_my_loan 도구로 확인한 결과에 근거해 답하세요.")
SYSTEM_B = SYSTEM_A + " 두 도구가 모두 필요하면 한 번에 함께 부르고, 도구 결과를 받은 뒤에 LoanAnswer로 답을 정리하세요."
CONTEXTS = {"R0": {"member_id": "M-0317", "overdue_days": 0}, "R3": {"member_id": "M-0317", "overdue_days": 3}}


@tool
def lookup_policy(topic: str):
    """교육센터 자료실 규정 하나를 주제어로 찾습니다. topic에는 대출, 운영, 연체 가운데 하나를 넣습니다."""
    if topic not in POLICIES:
        raise ValueError("지원하지 않는 주제: " + topic)
    return POLICIES[topic]


class MemberContext(TypedDict):
    member_id: str
    overdue_days: int


@tool
def check_my_loan(runtime: ToolRuntime[MemberContext]):
    """자료실 이용자 본인이 지금 새 책을 빌릴 수 있는지 확인합니다."""
    member = runtime.context["member_id"]
    days = runtime.context["overdue_days"]
    if days == 0:
        return "이용자 " + member + ": 연체가 없어 새 대출을 할 수 있습니다."
    return "이용자 " + member + ": 연체 " + str(days) + "일. " + POLICIES["연체"]


class LoanAnswer(BaseModel):
    can_borrow: Literal["가능", "불가"] = Field(description="check_my_loan 도구 결과로 본, 지금 새 책을 빌릴 수 있는지")
    answer: str = Field(description="두 도구 결과에 근거한 한두 문장 답")


model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")


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
            usages.append({"input": usage["input_tokens"], "output": usage["output_tokens"],
                           "cache_read": usage.get("input_token_details", {}).get("cache_read")})
        if kind == "ToolMessage":
            tools_out.append({"name": message.name, "status": message.status, "content": message.content})
            msg_ids.append(message.tool_call_id)
    last_ai = [m for m in result["messages"] if type(m).__name__ == "AIMessage"][-1]
    parsed = result.get("structured_response")
    return {"keys": list(result.keys()), "kinds": kinds, "calls": calls, "tool_messages": tools_out,
            "id_pair": req_ids == msg_ids, "n_ai": kinds.count("AIMessage"), "usage": usages,
            "structured_type": type(parsed).__name__, "structured": parsed.model_dump() if parsed is not None else None,
            "last_ai_calls": len(last_ai.tool_calls), "last_ai_content_len": len(last_ai.content),
            "model_name": last_ai.response_metadata.get("model_name")}


def main():
    cand, mode, rounds, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    system_text = SYSTEM_A if cand == "A" else SYSTEM_B
    agent = create_agent(model, tools=[lookup_policy, check_my_loan], system_prompt=system_text,
                         response_format=ToolStrategy(LoanAnswer), context_schema=MemberContext)
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            row = {"cand": cand, "mode": mode, "round": round_no, "question": QUESTION, "context": CONTEXTS[mode],
                   "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            try:
                result = agent.invoke({"messages": [HumanMessage(content=QUESTION)]}, context=CONTEXTS[mode])
                row.update(summarize(result))
            except Exception as error:  # 기록만 하고 다음 회차로
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(cand, mode, round_no, row.get("kinds"), row.get("calls"), row.get("id_pair"),
                  row.get("structured"), row.get("usage"), row.get("error", ""))


if __name__ == "__main__":
    main()
