"""Ch 27 03절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe03.py P <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  P : 회차마다 노트북 5절(할 일 목록 없이 — 한도만 준 Deep Agent)과 6절(우리 시스템 메시지 글 + 할 일 목록 미들웨어)을
      같은 질문 입력(first_input 하나)으로 차례로 한 번씩 실행 — 노트북 5·6절 본 실행과 같은 코드
입력·규정 글·도구·명세·훅·시스템 메시지 글·질문은 03-probe.md §0과 같다(노트북과 같은 코드).
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")

from deepagents import create_deep_agent  # noqa: E402
from langchain.agents.middleware import ModelCallLimitMiddleware, TodoListMiddleware, wrap_model_call  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import HumanMessage  # noqa: E402
from langchain.tools import tool  # noqa: E402

model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
todo_middleware = TodoListMiddleware()
guide_text = todo_middleware.system_prompt
our_system_text = "당신은 교육센터 자료실 안내를 돕는 도우미입니다. 규정을 여러 개 찾아야 하는 일은 먼저 write_todos로 할 일 목록을 적고 시작하세요. 답은 한국어로 씁니다."
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


outer_limit = ModelCallLimitMiddleware(run_limit=10, exit_behavior="end")
helper_limit = ModelCallLimitMiddleware(run_limit=2, exit_behavior="end")
helper_spec = {
    "name": "general-purpose",
    "description": "교재용 도우미입니다. 맡긴 일을 짧게 처리합니다.",
    "system_prompt": "맡긴 일을 두 문장의 한국어로 처리하세요.",
    "middleware": [helper_limit],
}
seen_system_texts = []
seen_tool_lists = []


@wrap_model_call
def record_request(request, handler):
    seen_system_texts.append(request.system_message.text)
    names = []
    for item in request.tools:
        names.append(item.name)
    seen_tool_lists.append(names)
    # 기록만 하고, 요청은 그대로 모델에게 보냅니다
    return handler(request)


plain_agent = create_deep_agent(
    model=model,
    tools=[lookup_rule],
    middleware=[outer_limit, record_request],
    subagents=[helper_spec],
)
plan_agent = create_deep_agent(
    model=model,
    tools=[lookup_rule],
    system_prompt=our_system_text,
    middleware=[outer_limit, todo_middleware, record_request],
    subagents=[helper_spec],
)
QUESTION = "교육센터 자료실에 처음 온 학생에게 줄 안내문을 쓰려고 합니다. 대출, 연장, 연체 규정을 찾아 세 문장으로 정리해 주세요."


def tool_names(agent):
    tool_node = agent.nodes["tools"].bound
    names = list(tool_node.tools_by_name)
    names.sort()
    return names


def summarize(result, first_count, graph_tools):
    msgs = result["messages"]
    new = msgs[first_count:]
    ais = [m for m in new if type(m).__name__ == "AIMessage"]
    row = {"kinds": [type(m).__name__ for m in msgs]}
    row["names_per_reply"] = [[c["name"] for c in m.tool_calls] for m in ais]
    row["tool_args"] = [c["args"] for m in ais for c in m.tool_calls if c["name"] != "write_todos"]
    row["todo_counts"] = [[c["name"] for c in m.tool_calls].count("write_todos") for m in ais]
    row["task_count"] = sum([[c["name"] for c in m.tool_calls].count("task") for m in ais])
    row["tool_status"] = [(m.name, m.status) for m in new if type(m).__name__ == "ToolMessage"]
    row["hook_requests"] = len(seen_system_texts)
    row["first_system_text"] = seen_system_texts[0] if seen_system_texts else None
    row["system_all_same"] = all(t == seen_system_texts[0] for t in seen_system_texts) if seen_system_texts else None
    row["system_eq_joined"] = [t == our_system_text + "\n\n" + guide_text for t in seen_system_texts]
    row["hook_first_tools"] = seen_tool_lists[0] if seen_tool_lists else None
    row["hook_tool_counts"] = [len(n) for n in seen_tool_lists]
    row["write_todos_received"] = ("write_todos" in seen_tool_lists[0]) if seen_tool_lists else None
    row["execute_in_any"] = any("execute" in n for n in seen_tool_lists)
    row["graph_tools"] = len(graph_tools)
    row["todos_in_result"] = "todos" in result
    row["todos"] = result.get("todos")
    row["todo_items"] = len(result["todos"]) if "todos" in result else None
    usage_none = [m for m in ais if m.usage_metadata is None]
    row["limit_hit"] = bool(usage_none) or ("Model call limits exceeded" in str(msgs[-1].content))
    row["requests"] = len(ais)
    row["requests_eq_hook"] = len(ais) == len(seen_system_texts)
    if not usage_none:
        tin = sum(m.usage_metadata["input_tokens"] for m in ais)
        tout = sum(m.usage_metadata["output_tokens"] for m in ais)
        cache = sum(m.usage_metadata.get("input_token_details", {}).get("cache_read", 0) for m in ais)
        row["input_tokens"], row["output_tokens"], row["cache_read"] = tin, tout, cache
        row["per_request_input"] = [m.usage_metadata["input_tokens"] for m in ais]
        row["first_input_tokens"] = ais[0].usage_metadata["input_tokens"] if ais else None
        row["cost_nocache"] = round((tin * 0.75 + tout * 4.50) / 1000000, 6)
        row["cost_cache"] = round(((tin - cache) * 0.75 + cache * 0.075 + tout * 4.50) / 1000000, 6)
    row["answer"] = msgs[-1].text
    row["answer_len"] = len(msgs[-1].text)
    return row


def main():
    global seen_system_texts, seen_tool_lists
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    assert mode == "P"
    plain_graph_tools = tool_names(plain_agent)
    plan_graph_tools = tool_names(plan_agent)
    with open(out, "a", encoding="utf-8") as handle:
        for _ in range(rounds):
            first_input = {"messages": [HumanMessage(content=QUESTION)]}
            input_count = len(first_input["messages"])
            for label, agent, graph_tools in [("plain", plain_agent, plain_graph_tools), ("plan", plan_agent, plan_graph_tools)]:
                row = {"cond": label, "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
                seen_system_texts = []
                seen_tool_lists = []
                try:
                    result = agent.invoke(first_input)
                    row.update(summarize(result, input_count, graph_tools))
                except Exception as error:  # 기록만 하고 다음으로(다시 보내지 않음)
                    row["error"] = type(error).__name__ + ": " + str(error)[:300]
                    row["hook_requests_at_error"] = len(seen_system_texts)
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                short = dict(row)
                short.pop("first_system_text", None)
                print(json.dumps(short, ensure_ascii=False)[:1800])


if __name__ == "__main__":
    main()
