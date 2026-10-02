"""Ch 27 05절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe05.py P <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  P : 회차마다 기본 한도 그대로의 Deep Agent(도구 read_visit_log, 기본 백엔드 StateBackend — 디스크 0)를 새로 만들고,
      같은 질문 입력으로 한 번 실행 — 노트북 6절 본 실행과 같은 코드
입력·방문 기록·도구·명세·훅·한도·질문은 05-probe.md §0과 같다(노트북과 같은 코드).
디스크에 파일을 쓰지 않는다(옮겨 둔 결과는 상태 칸 files에만). 호출 ID 값은 기록에서 <id>로 가린다.
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
log_line_count = 2000
lost_number = 345
lost_line = "방문 기록 " + str(lost_number) + ": 분실물 신고 — 파란 우산 1개를 안내 데스크에 맡김"


@tool
def read_visit_log():
    """교육센터 자료실의 오늘 방문 기록 전체를 한 번에 내놓습니다."""
    visit_lines = []
    for number in range(1, log_line_count + 1):
        line = "방문 기록 " + str(number) + ": 열람실에서 신문과 잡지, 새로 들어온 책 목록을 읽고 나감"
        # 정해 둔 자리 한 줄만 분실물 기록으로 바꿉니다
        if number == lost_number:
            line = lost_line
        visit_lines.append(line)
    return "\n".join(visit_lines)


visit_log_text = read_visit_log.invoke({})
outer_limit = ModelCallLimitMiddleware(run_limit=10, exit_behavior="end")
helper_limit = ModelCallLimitMiddleware(run_limit=2, exit_behavior="end")
helper_spec = {
    "name": "general-purpose",
    "description": "교재용 도우미입니다. 맡긴 일을 짧게 처리합니다.",
    "system_prompt": "맡긴 일을 두 문장의 한국어로 처리하세요.",
    "middleware": [helper_limit],
}
seen_sizes = []


@wrap_model_call
def record_sizes(request, handler):
    total = 0
    for message in request.messages:
        total = total + len(message.text)
    seen_sizes.append(total)
    # 기록만 하고, 요청은 그대로 모델에게 보냅니다
    return handler(request)


QUESTION = "교육센터 자료실의 오늘 방문 기록을 불러와서, 분실물 신고가 적힌 기록을 찾아 주세요. 무엇을 어디에 맡겼는지 한 문장으로 답해 주세요."
DEFAULT_THRESHOLD = 4 * 20000


def tool_names(agent):
    tool_node = agent.nodes["tools"].bound
    names = list(tool_node.tools_by_name)
    names.sort()
    return names


def build_agent():
    """노트북 6절 셀(run_agent)과 같은 줄."""
    run_agent = create_deep_agent(
        model=model,
        tools=[read_visit_log],
        middleware=[outer_limit, record_sizes],
        subagents=[helper_spec],
    )
    return run_agent


def mask(value, ids):
    text = json.dumps(value, ensure_ascii=False)
    for one in ids:
        text = text.replace(one, "<id>")
    return json.loads(text)


def summarize(result, first_count, graph_tools):
    msgs = result["messages"]
    new = msgs[first_count:]
    ais = [m for m in new if type(m).__name__ == "AIMessage"]
    log_ids = [c["id"] for m in ais for c in m.tool_calls if c["name"] == "read_visit_log"]
    row = {"kinds": [type(m).__name__ for m in msgs]}
    row["names_per_reply"] = [[c["name"] for c in m.tool_calls] for m in ais]
    row["log_calls"] = len(log_ids)
    row["file_tool_calls"] = mask([[c["name"], c["args"]] for m in ais for c in m.tool_calls if c["name"] not in ("read_visit_log", "task")], log_ids)
    row["task_count"] = sum([[c["name"] for c in m.tool_calls].count("task") for m in ais])
    tms = [m for m in new if type(m).__name__ == "ToolMessage"]
    row["tool_msgs"] = [[m.name, m.status, len(m.content), m.content.startswith("Tool result too large")] for m in tms]
    row["log_msg_is_notice"] = [m.content.startswith("Tool result too large") and len(m.content) < len(visit_log_text) for m in tms if m.name == "read_visit_log"]
    row["max_tool_msg_len"] = max([len(m.content) for m in tms], default=0)
    offloaded = [k for k in result["files"] if k.startswith("/large_tool_results/")]
    row["files_keys_masked"] = mask(list(result["files"]), log_ids)
    row["offloaded_count"] = len(offloaded)
    row["offloaded_eq_log"] = [result["files"][k]["content"] == visit_log_text for k in offloaded]
    row["hook_sizes"] = list(seen_sizes)
    row["hook_all_smaller"] = all(s < len(visit_log_text) for s in seen_sizes)
    row["hook_requests"] = len(seen_sizes)
    row["graph_tools"] = len(graph_tools)
    usage_none = [m for m in ais if m.usage_metadata is None]
    row["limit_hit"] = bool(usage_none) or ("Model call limits exceeded" in str(msgs[-1].content))
    row["requests"] = len(ais)
    row["tool_replies"] = len([m for m in ais if m.tool_calls])
    row["requests_eq_hook"] = len(ais) == len(seen_sizes)
    if not usage_none:
        tin = sum(m.usage_metadata["input_tokens"] for m in ais)
        tout = sum(m.usage_metadata["output_tokens"] for m in ais)
        cache = sum(m.usage_metadata.get("input_token_details", {}).get("cache_read", 0) for m in ais)
        row["input_tokens"], row["output_tokens"], row["cache_read"] = tin, tout, cache
        row["per_request_input"] = [m.usage_metadata["input_tokens"] for m in ais]
        row["cost_nocache"] = round((tin * 0.75 + tout * 4.50) / 1000000, 6)
        row["cost_cache"] = round(((tin - cache) * 0.75 + cache * 0.075 + tout * 4.50) / 1000000, 6)
    answer = msgs[-1].text
    row["answer"] = answer
    row["answer_len"] = len(answer)
    row["answer_has_item_and_place"] = ("우산" in answer) and ("안내 데스크" in answer)
    return row


def main():
    global seen_sizes
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    assert mode == "P"
    assert len(visit_log_text) > DEFAULT_THRESHOLD
    with open(out, "a", encoding="utf-8") as handle:
        for _ in range(rounds):
            row = {"cond": "default-limit", "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            seen_sizes = []
            try:
                run_agent = build_agent()
                graph_tools = tool_names(run_agent)
                first_input = {"messages": [HumanMessage(content=QUESTION)]}
                input_count = len(first_input["messages"])
                result = run_agent.invoke(first_input)
                row.update(summarize(result, input_count, graph_tools))
            except Exception as error:  # 기록만 하고 다음으로(다시 보내지 않음)
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
                row["hook_requests_at_error"] = len(seen_sizes)
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False)[:2500])


if __name__ == "__main__":
    main()
