"""Ch 27 02절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe02.py P1 <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  P1 : 자료실 규정 도구 하나를 더한 Deep Agent(바깥 호출 한도 3 + 같은 이름 general-purpose 명세 한도 2 + 기록 훅)에
       질문 한 줄을 넣어 한 번 실행 — 노트북 5절 본 실행과 같은 코드
입력·규정 글·도구·명세·훅은 02-probe.md §0과 같다(노트북과 같은 코드).
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")

from deepagents import create_deep_agent  # noqa: E402
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_model_call  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import HumanMessage  # noqa: E402
from langchain.tools import tool  # noqa: E402

model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
library_rules = {
    "대출": "일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.",
    "연장": "반납 예정일 전에 한 번, 7일 연장할 수 있습니다. 예약한 사람이 있는 책은 연장할 수 없습니다.",
    "연체": "연체한 일수만큼 새 대출이 제한됩니다.",
    "운영": "평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.",
}


@tool
def lookup_rule(topic: str):
    """교육센터 자료실 규정 하나를 주제어로 찾습니다. topic에는 대출, 연장, 연체, 운영 가운데 하나를 넣습니다."""
    # 없는 주제어면 오류 대신 정해 둔 안내 글을 내놓습니다
    if topic in library_rules:
        return library_rules[topic]
    return "그런 주제어의 규정은 없습니다. 대출, 연장, 연체, 운영 가운데 하나를 넣어 주세요."


outer_limit = ModelCallLimitMiddleware(run_limit=3, exit_behavior="end")
helper_limit = ModelCallLimitMiddleware(run_limit=2, exit_behavior="end")
helper_spec = {
    "name": "general-purpose",
    "description": "교재용 도우미입니다. 맡긴 일을 짧게 처리합니다.",
    "system_prompt": "맡긴 일을 두 문장의 한국어로 처리하세요.",
    "middleware": [helper_limit],
}
seen_tool_lists = []


@wrap_model_call
def record_tool_names(request, handler):
    names = []
    for item in request.tools:
        names.append(item.name)
    seen_tool_lists.append(names)
    # 기록만 하고, 요청은 그대로 모델에게 보냅니다
    return handler(request)


rule_agent = create_deep_agent(
    model=model,
    tools=[lookup_rule],
    middleware=[outer_limit, record_tool_names],
    subagents=[helper_spec],
)
QUESTION = "교육센터 자료실에서 빌린 책의 반납 날짜를 늘리려면 어떻게 하나요? 두 문장으로 답해 주세요."


def tool_names(agent):
    tool_node = agent.nodes["tools"].bound
    names = list(tool_node.tools_by_name)
    names.sort()
    return names


def main():
    global seen_tool_lists
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    assert mode == "P1"
    graph_tools = tool_names(rule_agent)
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            row = {"mode": mode, "round": round_no, "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            seen_tool_lists = []
            first_input = {"messages": [HumanMessage(content=QUESTION)]}
            try:
                result = rule_agent.invoke(first_input)
                msgs = result["messages"]
                new = msgs[len(first_input["messages"]):]
                row["kinds"] = [type(m).__name__ for m in msgs]
                ais = [m for m in new if type(m).__name__ == "AIMessage"]
                row["calls_per_response"] = [len(m.tool_calls) for m in ais]
                row["tool_names"] = [c["name"] for m in ais for c in m.tool_calls]
                row["tool_args"] = [c["args"] for m in ais for c in m.tool_calls]
                row["tool_contents"] = [m.content for m in new if type(m).__name__ == "ToolMessage"]
                row["tool_status"] = [m.status for m in new if type(m).__name__ == "ToolMessage"]
                row["hook_requests"] = len(seen_tool_lists)
                row["hook_counts"] = [len(n) for n in seen_tool_lists]
                row["hook_first"] = seen_tool_lists[0] if seen_tool_lists else None
                row["hook_all_same"] = all(n == seen_tool_lists[0] for n in seen_tool_lists) if seen_tool_lists else None
                row["execute_in_any"] = any("execute" in n for n in seen_tool_lists)
                row["graph_only"] = [n for n in graph_tools if seen_tool_lists and n not in seen_tool_lists[0]]
                usage_none = [m for m in ais if m.usage_metadata is None]
                row["limit_hit"] = bool(usage_none) or ("Model call limits exceeded" in str(msgs[-1].content))
                if not usage_none:
                    tin = sum(m.usage_metadata["input_tokens"] for m in ais)
                    tout = sum(m.usage_metadata["output_tokens"] for m in ais)
                    cache = sum(m.usage_metadata.get("input_token_details", {}).get("cache_read", 0) for m in ais)
                    row["requests"] = len(ais)
                    row["input_tokens"], row["output_tokens"], row["cache_read"] = tin, tout, cache
                    row["per_request_input"] = [m.usage_metadata["input_tokens"] for m in ais]
                    row["cost"] = round(((tin - cache) * 0.75 + cache * 0.075 + tout * 4.50) / 1000000, 6)
                row["requests_eq_hook"] = len(ais) == len(seen_tool_lists)
                row["answer"] = msgs[-1].text
                row["answer_len"] = len(msgs[-1].text)
            except Exception as error:  # 기록만 하고 다음 회차로(다시 보내지 않음)
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    main()
