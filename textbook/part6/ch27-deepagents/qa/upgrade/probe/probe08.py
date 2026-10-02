"""Ch 27 08절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe08.py P <회차 수> <기록 파일(JSONL, 이어 쓰기)>
      python probe08.py DRY 1 <기록 파일>   (가짜 키 글·.env 읽지 않음 — 조립·손 요청만, 모델 요청 0)
  P : 회차마다 보고 에이전트(바깥 호출 한도 10 · 같은 이름 general-purpose 명세(한도 2) · 자료 폴더 쓰기 막기 권한 규칙 ·
      interrupt_on write_file · 새 InMemorySaver · 우리 시스템 메시지 글)를 새로 만들고, 규칙 없는 Deep Agent의 작은 그래프에
      손 요청 write_file 셋으로 교재용 자료를 상태 칸 files에 넣은 뒤(모델 없음), 자료가 든 files와 질문 한 줄로 실행 →
      멈추면 멈춘 도구 요청마다 승인 결정 하나를 넣어 같은 스레드로 이어 감 — 노트북 2·3·6·7절과 같은 코드
입력·자료 글·명세·한도·규칙·시스템 메시지 글·질문·결정은 08-probe.md §0과 같다(노트북과 같은 코드).
노트북과 다른 점: 없다(서브에이전트 요청을 세려고 콜백을 넣지 않음 — task를 부르면 기록에 task 수가 남음). 기록만 더 자세히 남긴다.
디스크에 파일을 쓰지 않는다(기본 백엔드 — 상태 칸 files, 체크포인터는 메모리). 호출 ID 값은 기록하지 않는다.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
if sys.argv[1] == "DRY":
    os.environ["OPENAI_API_KEY"] = "sk-not-a-real-key"
else:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")

from deepagents import FilesystemMiddleware, FilesystemPermission, create_deep_agent  # noqa: E402
from deepagents.middleware.filesystem import FilesystemState  # noqa: E402
from langchain.agents.middleware import ModelCallLimitMiddleware  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import AIMessage, HumanMessage  # noqa: E402
from langgraph.checkpoint.memory import InMemorySaver  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402
from langgraph.types import Command  # noqa: E402

model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
helper_limit = ModelCallLimitMiddleware(run_limit=2, exit_behavior="end")
helper_spec = {
    "name": "general-purpose",
    "description": "교재용 도우미입니다. 맡긴 일을 짧게 처리합니다.",
    "system_prompt": "맡긴 일을 두 문장의 한국어로 처리하세요.",
    "middleware": [helper_limit],
}
outer_limit = ModelCallLimitMiddleware(run_limit=10, exit_behavior="end")
source_texts = {
    "/sources/closing-notice.md": "# 서가 정리 휴관 안내\n10월 셋째 주 토요일은 서가 정리로 자료실을 열지 않습니다.\n이날은 대출·연장·반납 창구를 열지 않습니다.",
    "/sources/return-box.md": "# 무인 반납함 안내\n자료실 정문 옆 무인 반납함은 휴관일에도 쓸 수 있습니다.\n반납함에 넣은 책은 다음 운영일에 반납 처리됩니다.",
    "/sources/new-books.md": "# 새로 들어온 책\n이번 달에는 데이터 분석 입문서 세 권이 들어왔습니다.\n새 책은 들어온 날부터 일주일 동안 자료실 안에서만 볼 수 있습니다.",
}
source_rule = FilesystemPermission(operations=["write"], paths=["/sources/**"], mode="deny")
report_text = "자료는 /sources/ 폴더의 파일에만 있습니다. 먼저 grep으로 관련 파일을 찾고, 찾은 파일을 read_file로 읽으세요. 그다음 파일에 적힌 내용만으로 두 문장의 한국어 답을 써서 write_file로 /reports/answer.md에 적으세요. 답의 문장마다 근거 파일 위치를 [/sources/파일 이름.md] 꼴로 붙이세요. 파일에 적은 뒤에는 적은 파일 위치를 한 문장으로 알려 주세요."
question = "휴관일에 무인 반납함에 넣은 책은 언제 반납 처리되나요?"


def tools_only_graph(agent):
    builder = StateGraph(FilesystemState)
    builder.add_node("tools", agent.nodes["tools"].bound)
    builder.add_edge(START, "tools")
    builder.add_edge("tools", END)
    return builder.compile()


def review_graph(agent, checkpointer):
    builder = StateGraph(FilesystemState)
    builder.add_node("review", agent.nodes["HumanInTheLoopMiddleware.after_model"].bound)
    builder.add_node("tools", agent.nodes["tools"].bound)
    builder.add_edge(START, "review")
    builder.add_edge("review", "tools")
    builder.add_edge("tools", END)
    return builder.compile(checkpointer=checkpointer)


def find_source_marks(answer):
    marks = []
    pieces = answer.split("[")
    for piece in pieces[1:]:
        if "]" in piece:
            inside = piece.split("]")[0]
            marks.append("[" + inside + "]")
    return marks


def check_citations(answer, known):
    rows = []
    for mark in find_source_marks(answer):
        cited = mark[1:-1]
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
    """노트북 2·3절 셀과 같은 줄(규칙 없는 Deep Agent로 자료 넣기 · 권한 규칙 · 보고 에이전트)."""
    seed_agent = create_deep_agent(model=model)
    seed_graph = tools_only_graph(seed_agent)
    write_calls = []
    for path in source_texts:
        write_args = {"file_path": path, "content": source_texts[path]}
        write_calls.append({"name": "write_file", "args": write_args, "id": "hand_" + path, "type": "tool_call"})
    write_request = AIMessage(content="", tool_calls=write_calls)
    seed_result = seed_graph.invoke({"messages": [write_request]})
    source_files = seed_result["files"]
    report_agent = create_deep_agent(
        model=model,
        system_prompt=report_text,
        middleware=[outer_limit],
        subagents=[helper_spec],
        permissions=[source_rule],
        interrupt_on={"write_file": True},
        checkpointer=InMemorySaver(),
    )
    return report_agent, source_files


def hand_checks(report_agent, source_files):
    """노트북 4·5절(모델 없음)과 같은 손 요청 — DRY에서만 기록."""
    row = {}
    allow_args = {"file_path": "/reports/check.md", "content": "점검 메모"}
    deny_args = {"file_path": "/sources/new-books.md", "content": "바꾼 글"}
    allow_call = {"name": "write_file", "args": allow_args, "id": "hand_allow_1", "type": "tool_call"}
    deny_call = {"name": "write_file", "args": deny_args, "id": "hand_deny_1", "type": "tool_call"}
    two_request = AIMessage(content="", tool_calls=[allow_call, deny_call])
    guard_graph = tools_only_graph(report_agent)
    guard_result = guard_graph.invoke({"messages": [two_request], "files": source_files})
    row["guard"] = [[m.name, m.content, m.status] for m in guard_result["messages"][1:]]
    row["guard_files"] = list(guard_result["files"])
    same_agent = create_deep_agent(model=model, permissions=[source_rule], middleware=[FilesystemMiddleware()])
    same_graph = tools_only_graph(same_agent)
    same_result = same_graph.invoke({"messages": [two_request], "files": source_files})
    row["same"] = [[m.name, m.content, m.status] for m in same_result["messages"][1:]]
    hand_graph = review_graph(report_agent, InMemorySaver())
    hand_config = {"configurable": {"thread_id": "hand-approval"}}
    report_call = {"name": "write_file", "args": allow_args, "id": "hand_report_1", "type": "tool_call"}
    report_request = AIMessage(content="", tool_calls=[report_call])
    hand_result = hand_graph.invoke({"messages": [report_request], "files": source_files}, hand_config)
    row["hand_keys"] = list(hand_result)
    row["hand_next"] = list(hand_graph.get_state(hand_config).next)
    row["hand_value"] = hand_result["__interrupt__"][0].value
    hand_after = hand_graph.invoke(Command(resume={"decisions": [{"type": "approve"}]}), hand_config)
    row["hand_after"] = [[type(m).__name__, getattr(m, "status", None), m.content] for m in hand_after["messages"]]
    plain_config = {"configurable": {"thread_id": "hand-plain"}}
    hand_graph.invoke({"messages": [report_request], "files": source_files}, plain_config)
    try:
        hand_graph.invoke(Command(resume="approve"), plain_config)
    except TypeError as error:
        row["plain_answer_error"] = type(error).__name__ + ": " + str(error)
    return row


def usage_row(ais):
    tin = sum(m.usage_metadata["input_tokens"] for m in ais)
    tout = sum(m.usage_metadata["output_tokens"] for m in ais)
    tcache = sum(((m.usage_metadata.get("input_token_details") or {}).get("cache_read", 0)) for m in ais)
    return {
        "input_tokens": tin, "output_tokens": tout, "cache_read": tcache,
        "cost_nocache": round((tin * 0.75 + tout * 4.50) / 1000000, 6),
        "cost_cache": round(((tin - tcache) * 0.75 + tcache * 0.075 + tout * 4.50) / 1000000, 6),
    }


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    assert mode in ("P", "DRY")
    with open(out, "a", encoding="utf-8") as handle:
        for _ in range(rounds):
            row = {"cond": "report", "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            try:
                report_agent, source_files = build_and_fill()
                row["graph_nodes"] = list(report_agent.get_graph().nodes)
                row["graph_tools"] = tool_names(report_agent)
                row["source_files"] = list(source_files)
                if mode == "DRY":
                    row.update(hand_checks(report_agent, source_files))
                    handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                    print(json.dumps(row, ensure_ascii=False))
                    continue
                run_config = {"configurable": {"thread_id": "report-run"}}
                first_input = {"messages": [HumanMessage(content=question)], "files": source_files}
                input_count = len(first_input["messages"])
                first_result = report_agent.invoke(first_input, run_config)
                first_msgs = first_result["messages"]
                row["paused"] = "__interrupt__" in first_result
                row["first_kinds"] = [type(m).__name__ for m in first_msgs]
                first_ais = [m for m in first_msgs[input_count:] if type(m).__name__ == "AIMessage"]
                row["first_requests"] = len(first_ais)
                decisions = []
                if "__interrupt__" in first_result:
                    paused_value = first_result["__interrupt__"][0].value
                    row["paused_actions"] = [[a["name"], a["args"].get("file_path"), len(a["args"].get("content", ""))] for a in paused_value["action_requests"]]
                    row["paused_contents"] = [a["args"].get("content") for a in paused_value["action_requests"]]
                    row["allowed"] = [r["allowed_decisions"] for r in paused_value["review_configs"]]
                    row["files_at_pause"] = list(report_agent.get_state(run_config).values.get("files", {}))
                    for action in paused_value["action_requests"]:
                        decisions.append({"type": "approve"})
                row["decisions"] = len(decisions)
                run_result = first_result
                if len(decisions) > 0:
                    run_result = report_agent.invoke(Command(resume={"decisions": decisions}), run_config)
                msgs = run_result["messages"]
                run_new = msgs[input_count:]
                ais = [m for m in run_new if type(m).__name__ == "AIMessage"]
                row["paused_again"] = "__interrupt__" in run_result
                row["kinds"] = [type(m).__name__ for m in msgs]
                row["names_per_reply"] = [[c["name"] for c in m.tool_calls] for m in ais]
                row["calls_per_reply"] = [[[c["name"], c["args"]] for c in m.tool_calls] for m in ais]
                tms = [m for m in run_new if type(m).__name__ == "ToolMessage"]
                row["tool_msgs"] = [[m.name, m.status, len(m.content)] for m in tms]
                row["tool_msg_texts"] = [[m.name, m.content] for m in tms]
                row["grep_patterns"] = call_args(run_new, "grep", "pattern")
                row["read_paths"] = call_args(run_new, "read_file", "file_path")
                row["write_paths"] = call_args(run_new, "write_file", "file_path")
                row["task_types"] = call_args(run_new, "task", "subagent_type")
                row["answer"] = msgs[-1].text
                row["files_after"] = list(run_result["files"])
                same = True
                for path in source_texts:
                    if run_result["files"][path]["content"] != source_texts[path]:
                        same = False
                row["sources_same"] = same
                report_path = "/reports/answer.md"
                if report_path in run_result["files"]:
                    body = run_result["files"][report_path]["content"]
                    row["report"] = body
                    row["report_rows"] = check_citations(body, source_files)
                row["requests"] = len(ais)
                row["resume_requests"] = len(ais) - len(first_ais)
                row["tool_replies"] = len([m for m in ais if len(m.tool_calls) > 0])
                usage_none = [m for m in ais if m.usage_metadata is None]
                row["limit_hit"] = bool(usage_none) or ("Model call limits exceeded" in str(msgs[-1].content))
                row["req_eq_replies_plus1"] = row["requests"] == row["tool_replies"] + 1
                if not usage_none:
                    row.update(usage_row(ais))
                    row["first_input_tokens"] = ais[0].usage_metadata["input_tokens"]
            except Exception as error:  # 기록만 하고 다음으로(다시 보내지 않음)
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False)[:4000])


if __name__ == "__main__":
    main()
