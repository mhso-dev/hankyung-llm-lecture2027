"""Ch 27 04절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe04.py P <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  P : 회차마다 새 임시 폴더(tempfile.mkdtemp(prefix="ch27-04-"))를 뿌리 폴더로 삼는 디스크 백엔드로 Deep Agent를 새로 만들고,
      같은 질문 입력으로 한 번 실행 — 노트북 5절 본 실행과 같은 코드
입력·규정 글·도구·명세·훅·한도·질문은 04-probe.md §0과 같다(노트북과 같은 코드).
임시 폴더는 지우지 않는다(04-diagnosis.md 삭제 승인 목록에 적음).
"""
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")

from deepagents import create_deep_agent  # noqa: E402
from deepagents.backends import FilesystemBackend  # noqa: E402
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


outer_limit = ModelCallLimitMiddleware(run_limit=10, exit_behavior="end")
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


QUESTION = "교육센터 자료실의 대출, 연장, 연체 규정을 찾아, 찾은 규정 글을 /notes/rules.md 파일에 적어 두세요. 그다음 처음 온 학생에게 줄 안내문을 세 문장으로 써 주세요."


def tool_names(agent):
    tool_node = agent.nodes["tools"].bound
    names = list(tool_node.tools_by_name)
    names.sort()
    return names


def build_agent():
    """노트북 5절 두 셀(run_folder·run_backend, run_agent)과 같은 줄."""
    run_folder = tempfile.mkdtemp(prefix="ch27-04-")
    run_backend = FilesystemBackend(root_dir=run_folder)
    run_agent = create_deep_agent(
        model=model,
        tools=[lookup_rule],
        backend=run_backend,
        middleware=[outer_limit, record_tool_names],
        subagents=[helper_spec],
    )
    return run_folder, run_agent


def disk_files(folder):
    found = []
    for base, _dirs, files in os.walk(folder):
        for name in files:
            found.append(os.path.relpath(os.path.join(base, name), folder))
    found.sort()
    return found


def summarize(result, first_count, run_folder, graph_tools):
    msgs = result["messages"]
    new = msgs[first_count:]
    ais = [m for m in new if type(m).__name__ == "AIMessage"]
    row = {"kinds": [type(m).__name__ for m in msgs]}
    row["names_per_reply"] = [[c["name"] for c in m.tool_calls] for m in ais]
    row["lookup_args"] = [c["args"] for m in ais for c in m.tool_calls if c["name"] == "lookup_rule"]
    written = [c["args"] for m in ais for c in m.tool_calls if c["name"] == "write_file"]
    row["write_paths"] = [a.get("file_path") for a in written]
    row["write_lens"] = [len(a.get("content", "")) for a in written]
    row["task_count"] = sum([[c["name"] for c in m.tool_calls].count("task") for m in ais])
    row["other_fs_calls"] = [c["name"] for m in ais for c in m.tool_calls if c["name"] not in ("lookup_rule", "write_file")]
    row["tool_status"] = [(m.name, m.status, m.content if m.name != "lookup_rule" else "") for m in new if type(m).__name__ == "ToolMessage"]
    row["hook_requests"] = len(seen_tool_lists)
    row["hook_first_tools"] = seen_tool_lists[0] if seen_tool_lists else None
    row["hook_tool_counts"] = [len(n) for n in seen_tool_lists]
    row["execute_in_any"] = any("execute" in n for n in seen_tool_lists)
    row["graph_tools"] = len(graph_tools)
    row["files_key"] = "files" in result
    row["files_list"] = list(result["files"]) if "files" in result else None
    row["top_names"] = sorted(os.listdir(run_folder))
    row["disk_files"] = disk_files(run_folder)
    eq = []
    for a in written:
        path = os.path.join(run_folder, a.get("file_path", "").lstrip("/"))
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as handle:
                eq.append(handle.read() == a.get("content"))
        else:
            eq.append(None)
    row["disk_eq_args"] = eq
    usage_none = [m for m in ais if m.usage_metadata is None]
    row["limit_hit"] = bool(usage_none) or ("Model call limits exceeded" in str(msgs[-1].content))
    row["requests"] = len(ais)
    row["tool_replies"] = len([m for m in ais if m.tool_calls])
    row["requests_eq_hook"] = len(ais) == len(seen_tool_lists)
    if not usage_none:
        tin = sum(m.usage_metadata["input_tokens"] for m in ais)
        tout = sum(m.usage_metadata["output_tokens"] for m in ais)
        cache = sum(m.usage_metadata.get("input_token_details", {}).get("cache_read", 0) for m in ais)
        row["input_tokens"], row["output_tokens"], row["cache_read"] = tin, tout, cache
        row["per_request_input"] = [m.usage_metadata["input_tokens"] for m in ais]
        row["cost_nocache"] = round((tin * 0.75 + tout * 4.50) / 1000000, 6)
        row["cost_cache"] = round(((tin - cache) * 0.75 + cache * 0.075 + tout * 4.50) / 1000000, 6)
    row["answer"] = msgs[-1].text
    row["answer_len"] = len(msgs[-1].text)
    return row


def main():
    global seen_tool_lists
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    assert mode == "P"
    with open(out, "a", encoding="utf-8") as handle:
        for _ in range(rounds):
            row = {"cond": "disk", "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            seen_tool_lists = []
            try:
                run_folder, run_agent = build_agent()
                graph_tools = tool_names(run_agent)
                row["folder_prefix_ok"] = "ch27-04-" in run_folder
                row["folder_empty_before"] = os.listdir(run_folder) == []
                first_input = {"messages": [HumanMessage(content=QUESTION)]}
                input_count = len(first_input["messages"])
                result = run_agent.invoke(first_input)
                row.update(summarize(result, input_count, run_folder, graph_tools))
            except Exception as error:  # 기록만 하고 다음으로(다시 보내지 않음)
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
                row["hook_requests_at_error"] = len(seen_tool_lists)
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False)[:2000])


if __name__ == "__main__":
    main()
