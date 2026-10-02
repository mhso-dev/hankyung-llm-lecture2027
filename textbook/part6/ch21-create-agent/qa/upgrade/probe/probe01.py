"""Ch 21 01절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe01.py <입력 L|G|T> <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  L : 「자료실에서 일반 도서를 며칠 빌릴 수 있나요?」
  G : 「안녕하세요. 한 문장으로 인사해 주세요.」
  T : 「자료실 운영 시간과 연체 규정을 함께 알려 주세요.」(값 바꿔 보기 후보)
자료·도구는 Ch 20 01절 노트북 셀과 같은 코드, 에이전트는 01절 노트북과 같은 create_agent 호출(01-probe.md §0).
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
from langchain.messages import HumanMessage  # noqa: E402
from langchain.tools import tool  # noqa: E402

QUESTIONS = {
    "L": "자료실에서 일반 도서를 며칠 빌릴 수 있나요?",
    "G": "안녕하세요. 한 문장으로 인사해 주세요.",
    "T": "자료실 운영 시간과 연체 규정을 함께 알려 주세요.",
}
POLICIES = {
    "대출": "일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.",
    "운영": "평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.",
    "연체": "연체한 일수만큼 새 대출이 제한됩니다.",
}
SYSTEM_TEXT = "교육센터 자료실 안내 도우미입니다. 자료실 규정을 묻는 질문에는 lookup_policy 도구로 찾은 규정 글에 근거해 답하세요."


@tool
def lookup_policy(topic: str):
    """교육센터 자료실 규정 하나를 주제어로 찾습니다. topic에는 대출, 운영, 연체 가운데 하나를 넣습니다."""
    if topic not in POLICIES:
        raise ValueError("지원하지 않는 주제: " + topic)
    return POLICIES[topic]


model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
agent = create_agent(model, tools=[lookup_policy], system_prompt=SYSTEM_TEXT)


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
            tools_out.append({"status": message.status, "content": message.content, "name": message.name})
            msg_ids.append(message.tool_call_id)
    return {"keys": sorted(result.keys()), "kinds": kinds, "calls": calls, "tool_messages": tools_out,
            "id_pair": req_ids == msg_ids, "n_ai": kinds.count("AIMessage"), "usage": usages,
            "has_system": "SystemMessage" in kinds,
            "last_calls": len(result["messages"][-1].tool_calls), "answer": result["messages"][-1].content,
            "model_name": result["messages"][-1].response_metadata.get("model_name")}


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    question = QUESTIONS[mode]
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            row = {"mode": mode, "round": round_no, "question": question,
                   "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            try:
                result = agent.invoke({"messages": [HumanMessage(content=question)]})
                row.update(summarize(result))
            except Exception as error:  # 기록만 하고 다음 회차로
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(mode, round_no, row.get("keys"), row.get("kinds"), row.get("calls"), row.get("id_pair"),
                  row.get("usage"), row.get("error", ""))


if __name__ == "__main__":
    main()
