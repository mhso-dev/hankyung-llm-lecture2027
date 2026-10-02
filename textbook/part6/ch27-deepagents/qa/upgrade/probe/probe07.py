"""Ch 27 07절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe07.py P <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  P : 회차마다 조사 에이전트(새 도구 0 · 바깥 호출 한도 10 · 같은 이름 general-purpose 명세(한도 2) · 우리 시스템 메시지 글)를 새로 만들고,
      그 도구 실행 노드만 든 작은 그래프에 손 요청 write_file 셋으로 교재용 자료를 상태 칸 files에 넣은 뒤(모델 없음),
      자료가 든 files와 질문 한 줄로 한 번 실행 — 노트북 3·5절과 같은 코드
입력·자료 글·명세·한도·시스템 메시지 글·질문·판정 함수는 07-probe.md §0과 같다(노트북과 같은 코드).
노트북과 다른 점은 없다(서브에이전트를 쓰지 않아 콜백을 넣지 않음). 기록만 더 자세히 남긴다.
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
from deepagents.middleware.filesystem import FilesystemState  # noqa: E402
from langchain.agents.middleware import ModelCallLimitMiddleware  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import AIMessage, HumanMessage  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402

model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
helper_limit = ModelCallLimitMiddleware(run_limit=2, exit_behavior="end")
helper_spec = {
    "name": "general-purpose",
    "description": "교재용 도우미입니다. 맡긴 일을 짧게 처리합니다.",
    "system_prompt": "맡긴 일을 두 문장의 한국어로 처리하세요.",
    "middleware": [helper_limit],
}
outer_limit = ModelCallLimitMiddleware(run_limit=10, exit_behavior="end")
research_text = "자료는 /sources/ 폴더의 파일에만 있습니다. 먼저 grep으로 관련 파일을 찾고, 찾은 파일을 read_file로 읽으세요. 그다음 파일에 적힌 내용만으로 두 문장의 한국어로 답하세요. 답의 문장마다 근거 파일 위치를 [/sources/파일 이름.md] 꼴로 붙이세요."
source_texts = {
    "/sources/closing-notice.md": "# 서가 정리 휴관 안내\n10월 셋째 주 토요일은 서가 정리로 자료실을 열지 않습니다.\n이날은 대출·연장·반납 창구를 열지 않습니다.",
    "/sources/return-box.md": "# 무인 반납함 안내\n자료실 정문 옆 무인 반납함은 휴관일에도 쓸 수 있습니다.\n반납함에 넣은 책은 다음 운영일에 반납 처리됩니다.",
    "/sources/new-books.md": "# 새로 들어온 책\n이번 달에는 데이터 분석 입문서 세 권이 들어왔습니다.\n새 책은 들어온 날부터 일주일 동안 자료실 안에서만 볼 수 있습니다.",
}
QUESTION = "10월 셋째 주 토요일에 빌린 책을 반납할 수 있나요?"


def tools_only_graph(agent):
    builder = StateGraph(FilesystemState)
    builder.add_node("tools", agent.nodes["tools"].bound)
    builder.add_edge(START, "tools")
    builder.add_edge("tools", END)
    return builder.compile()


def check_citations(text, known):
    rows = []
    for piece in text.split("[")[1:]:
        if "]" in piece:
            cited = piece.split("]")[0]
            rows.append({"인용": cited, "있는가": cited in known})
    return rows


def call_args(messages, tool_name, arg_name):
    values = []
    for message in messages:
        if type(message).__name__ == "AIMessage":
            for call in message.tool_calls:
                if call["name"] == tool_name:
                    values.append(call["args"][arg_name])
    return values


def tool_names(agent):
    tool_node = agent.nodes["tools"].bound
    names = list(tool_node.tools_by_name)
    names.sort()
    return names


def build_and_fill():
    """노트북 2·3절 셀과 같은 줄(조사 에이전트 · 작은 그래프 · 손 요청 write_file 셋)."""
    research_agent = create_deep_agent(
        model=model,
        system_prompt=research_text,
        middleware=[outer_limit],
        subagents=[helper_spec],
    )
    small_graph = tools_only_graph(research_agent)
    write_calls = []
    for path in source_texts:
        write_args = {"file_path": path, "content": source_texts[path]}
        write_calls.append({"name": "write_file", "args": write_args, "id": "hand_" + path, "type": "tool_call"})
    write_request = AIMessage(content="", tool_calls=write_calls)
    write_result = small_graph.invoke({"messages": [write_request]})
    source_files = write_result["files"]
    return research_agent, write_result, source_files


def summarize(result, input_count, graph_tools, write_result, source_files):
    msgs = result["messages"]
    run_new = msgs[input_count:]
    ais = [m for m in run_new if type(m).__name__ == "AIMessage"]
    row = {"kinds": [type(m).__name__ for m in msgs]}
    row["graph_tools"] = graph_tools
    row["write_tool_msgs"] = [[m.name, m.status, m.content] for m in write_result["messages"][1:]]
    row["source_files"] = list(source_files)
    row["calls_per_reply"] = [[[c["name"], c["args"]] for c in m.tool_calls] for m in ais]
    row["names_per_reply"] = [[c["name"] for c in m.tool_calls] for m in ais]
    tms = [m for m in run_new if type(m).__name__ == "ToolMessage"]
    row["tool_msgs"] = [[m.name, m.status, len(m.content)] for m in tms]
    row["tool_msg_texts"] = [[m.name, m.content] for m in tms]
    row["grep_patterns"] = call_args(run_new, "grep", "pattern")
    row["read_paths"] = call_args(run_new, "read_file", "file_path")
    row["task_types"] = call_args(run_new, "task", "subagent_type")
    row["answer"] = msgs[-1].text
    row["rows_files"] = check_citations(row["answer"], result["files"])
    row["rows_read"] = check_citations(row["answer"], row["read_paths"])
    row["cited"] = [r["인용"] for r in row["rows_files"]]
    row["files_after"] = list(result["files"])
    row["files_same"] = list(result["files"]) == list(source_files)
    row["result_keys"] = list(result)
    row["outer_requests"] = len(ais)
    row["tool_replies"] = len([m for m in ais if len(m.tool_calls) > 0])
    usage_none = [m for m in ais if m.usage_metadata is None]
    row["limit_hit"] = bool(usage_none) or ("Model call limits exceeded" in str(msgs[-1].content))
    row["req_eq_replies_plus1"] = row["outer_requests"] == row["tool_replies"] + 1
    if not usage_none:
        tin = sum(m.usage_metadata["input_tokens"] for m in ais)
        tout = sum(m.usage_metadata["output_tokens"] for m in ais)
        tcache = sum(((m.usage_metadata.get("input_token_details") or {}).get("cache_read", 0)) for m in ais)
        row["input_tokens"], row["output_tokens"], row["cache_read"] = tin, tout, tcache
        row["first_input_tokens"] = ais[0].usage_metadata["input_tokens"]
        row["cost_nocache"] = round((tin * 0.75 + tout * 4.50) / 1000000, 6)
        row["cost_cache"] = round(((tin - tcache) * 0.75 + tcache * 0.075 + tout * 4.50) / 1000000, 6)
    return row


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    assert mode in ("P", "DRY")
    with open(out, "a", encoding="utf-8") as handle:
        for _ in range(rounds):
            row = {"cond": "research", "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            try:
                research_agent, write_result, source_files = build_and_fill()
                graph_tools = tool_names(research_agent)
                if mode == "DRY":
                    row["graph_tools"] = graph_tools
                    row["source_files"] = list(source_files)
                    row["write_tool_msgs"] = [[m.name, m.status, m.content] for m in write_result["messages"][1:]]
                    print(json.dumps(row, ensure_ascii=False))
                    continue
                first_input = {"messages": [HumanMessage(content=QUESTION)], "files": source_files}
                input_count = len(first_input["messages"])
                result = research_agent.invoke(first_input)
                row.update(summarize(result, input_count, graph_tools, write_result, source_files))
            except Exception as error:  # 기록만 하고 다음으로(다시 보내지 않음)
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False)[:3500])


if __name__ == "__main__":
    main()
