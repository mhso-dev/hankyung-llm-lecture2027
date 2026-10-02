"""Ch 27 06절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe06.py P <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  P : 회차마다 바깥 에이전트(조회 도구 없음 · 명세 rule-checker(lookup_rule·한도 4) + 같은 이름 general-purpose(한도 2)
      · 바깥 호출 한도 10 · 기록 훅 record_tool_names를 바깥과 두 명세에 · 우리 시스템 메시지 글)를 새로 만들고,
      같은 질문 입력으로 한 번 실행 — 노트북 5절 본 실행과 같은 코드
입력·규정 글·도구·명세·훅·한도·시스템 메시지 글·질문은 06-probe.md §0과 같다(노트북과 같은 코드).
노트북과 다른 점은 하나: 기록만 하는 콜백(on_llm_end — 응답마다 도구 요청 이름·인자·사용량·글)을 invoke 설정에 넣는다
(서브에이전트 응답은 바깥 목록에 없어, 서브에이전트가 부른 도구와 토큰을 노트북 밖에서만 기록하려고). 요청 수·요청 내용은 바꾸지 않는다.
디스크에 파일을 쓰지 않는다(기본 백엔드 — 상태 칸 files). 호출 ID 값은 기록하지 않는다.
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
from langchain_core.callbacks import BaseCallbackHandler  # noqa: E402

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


seen_tool_lists = []


@wrap_model_call
def record_tool_names(request, handler):
    names = []
    for item in request.tools:
        names.append(item.name)
    seen_tool_lists.append(names)
    # 기록만 하고, 요청은 그대로 모델에게 보냅니다
    return handler(request)


checker_limit = ModelCallLimitMiddleware(run_limit=4, exit_behavior="end")
rule_checker = {
    "name": "rule-checker",
    "description": "교육센터 자료실 규정을 찾아 확인하는 담당입니다. 규정 도구 lookup_rule은 이 담당만 가졌습니다.",
    "system_prompt": "맡은 일에 맞는 규정을 lookup_rule로 찾으세요. 찾은 규정 글을 write_file로 /notes/rule-check.md에 적으세요. 그다음 찾은 내용을 두 문장의 한국어로 보고하세요.",
    "tools": [lookup_rule],
    "middleware": [checker_limit, record_tool_names],
}
helper_limit = ModelCallLimitMiddleware(run_limit=2, exit_behavior="end")
helper_spec = {
    "name": "general-purpose",
    "description": "교재용 도우미입니다. 맡긴 일을 짧게 처리합니다.",
    "system_prompt": "맡긴 일을 두 문장의 한국어로 처리하세요.",
    "middleware": [helper_limit, record_tool_names],
}
outer_limit = ModelCallLimitMiddleware(run_limit=10, exit_behavior="end")
parent_text = "자료실 규정은 직접 찾지 말고, task 도구로 rule-checker에게 맡기세요. 받은 보고를 바탕으로 두 문장의 한국어로 답하세요."
QUESTION = "교육센터 자료실에서 빌린 책의 반납 날짜를 늘리려면 어떻게 하나요? 두 문장으로 답해 주세요."
NOTE = "/notes/rule-check.md"


def build_parent():
    """노트북 4절 셀(run_parent)과 같은 줄."""
    run_parent = create_deep_agent(
        model=model,
        system_prompt=parent_text,
        middleware=[outer_limit, record_tool_names],
        subagents=[rule_checker, helper_spec],
    )
    return run_parent


def tool_names(agent):
    tool_node = agent.nodes["tools"].bound
    names = list(tool_node.tools_by_name)
    names.sort()
    return names


class Recorder(BaseCallbackHandler):
    """기록만 하는 콜백 — 모델 응답마다 도구 요청 이름·인자·사용량·글."""

    def __init__(self):
        self.rows = []

    def on_llm_end(self, response, **kwargs):
        message = response.generations[0][0].message
        self.rows.append({
            "calls": [[c["name"], c["args"]] for c in message.tool_calls],
            "usage": message.usage_metadata,
            "text": message.text,
        })


def summarize(result, first_count, graph_tools, recorder):
    msgs = result["messages"]
    new = msgs[first_count:]
    ais = [m for m in new if type(m).__name__ == "AIMessage"]
    row = {"kinds": [type(m).__name__ for m in msgs]}
    row["outer_names_per_reply"] = [[c["name"] for c in m.tool_calls] for m in ais]
    row["task_types"] = [c["args"].get("subagent_type") for m in ais for c in m.tool_calls if c["name"] == "task"]
    row["task_descriptions"] = [c["args"].get("description") for m in ais for c in m.tool_calls if c["name"] == "task"]
    tms = [m for m in new if type(m).__name__ == "ToolMessage"]
    row["outer_tool_msgs"] = [[m.name, m.status, len(m.content)] for m in tms]
    row["task_reports"] = [m.content for m in tms if m.name == "task"]
    row["graph_tools"] = graph_tools
    row["hook_lists"] = [list(x) for x in seen_tool_lists]
    row["hook_total"] = len(seen_tool_lists)
    row["hook_task"] = len([x for x in seen_tool_lists if "task" in x])
    row["hook_lookup"] = len([x for x in seen_tool_lists if "lookup_rule" in x])
    row["hook_neither"] = len([x for x in seen_tool_lists if "task" not in x and "lookup_rule" not in x])
    row["hook_both"] = len([x for x in seen_tool_lists if "task" in x and "lookup_rule" in x])
    row["outer_requests"] = len(ais)
    row["outer_tool_replies"] = len([m for m in ais if m.tool_calls])
    usage_none = [m for m in ais if m.usage_metadata is None]
    row["limit_hit_outer"] = bool(usage_none) or ("Model call limits exceeded" in str(msgs[-1].content))
    row["limit_text_in_reports"] = any("Model call limits exceeded" in r for r in row["task_reports"])
    row["files_keys"] = list(result["files"])
    row["note_in_files"] = NOTE in result["files"]
    row["note_content"] = result["files"][NOTE]["content"] if NOTE in result["files"] else None
    row["note_eq_rule_extend"] = row["note_content"] == library_rules["연장"] if row["note_content"] is not None else None
    row["write_file_in_outer"] = "write_file" in [m.name for m in tms]
    row["lookup_in_outer"] = "lookup_rule" in [m.name for m in tms]
    row["ch26_count"] = row["outer_requests"] + len(row["task_types"]) * 1
    row["ch26_eq_hook"] = row["ch26_count"] == row["hook_total"]
    row["outer_plus_lookup_eq_total"] = row["hook_task"] + row["hook_lookup"] == row["hook_total"]
    row["callback_responses"] = recorder.rows
    row["callback_count"] = len(recorder.rows)
    if not usage_none:
        tin = sum(m.usage_metadata["input_tokens"] for m in ais)
        tout = sum(m.usage_metadata["output_tokens"] for m in ais)
        row["outer_input_tokens"], row["outer_output_tokens"] = tin, tout
        row["outer_cost_nocache"] = round((tin * 0.75 + tout * 4.50) / 1000000, 6)
    all_in = sum((r["usage"] or {}).get("input_tokens", 0) for r in recorder.rows)
    all_out = sum((r["usage"] or {}).get("output_tokens", 0) for r in recorder.rows)
    all_cache = sum(((r["usage"] or {}).get("input_token_details") or {}).get("cache_read", 0) for r in recorder.rows)
    row["all_input_tokens"], row["all_output_tokens"], row["all_cache_read"] = all_in, all_out, all_cache
    row["all_cost_nocache"] = round((all_in * 0.75 + all_out * 4.50) / 1000000, 6)
    row["all_cost_cache"] = round(((all_in - all_cache) * 0.75 + all_cache * 0.075 + all_out * 4.50) / 1000000, 6)
    row["answer"] = msgs[-1].text
    return row


def main():
    global seen_tool_lists
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    assert mode == "P"
    with open(out, "a", encoding="utf-8") as handle:
        for _ in range(rounds):
            row = {"cond": "delegate", "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            seen_tool_lists = []
            recorder = Recorder()
            try:
                run_parent = build_parent()
                graph_tools = tool_names(run_parent)
                first_input = {"messages": [HumanMessage(content=QUESTION)]}
                input_count = len(first_input["messages"])
                result = run_parent.invoke(first_input, {"callbacks": [recorder]})
                row.update(summarize(result, input_count, graph_tools, recorder))
            except Exception as error:  # 기록만 하고 다음으로(다시 보내지 않음)
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
                row["hook_requests_at_error"] = len(seen_tool_lists)
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False)[:3000])


if __name__ == "__main__":
    main()
