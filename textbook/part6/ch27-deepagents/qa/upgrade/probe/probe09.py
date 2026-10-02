"""Ch 27 09절(실습) 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe09.py A <회차 수> <기록 파일(JSONL, 이어 쓰기)>   실행 1 조건(사람 승인 켬 interrupt_on={"write_file": True})
      python probe09.py B <회차 수> <기록 파일>                    실행 2 조건(사람 승인 끔 interrupt_on={}) — 값 하나만 다름
      python probe09.py DRY 1 <기록 파일>   (가짜 키 글·.env 읽지 않음 — 두 조건의 조립만, 모델 요청 0)
  회차마다 메모 에이전트(바깥 호출 한도 10 · 같은 이름 general-purpose 명세(한도 2) · 우리 시스템 메시지 글 · 조건의 interrupt_on ·
  새 InMemorySaver)를 새로 만들고, 요청 글 한 줄로 실행 → 멈추면 멈춘 도구 요청마다 승인 결정 하나를 넣어 같은 스레드로 이어 감
  — 노트북 2·3·5·6절과 같은 코드. 입력·명세·한도·시스템 메시지 글·요청 글·결정은 09-probe.md §0과 같다.
노트북과 다른 점: 없다. 기록만 더 자세히 남긴다.
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

from deepagents import create_deep_agent  # noqa: E402
from langchain.agents.middleware import ModelCallLimitMiddleware  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import HumanMessage  # noqa: E402
from langgraph.checkpoint.memory import InMemorySaver  # noqa: E402
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
memo_path = "/reports/notice.md"
memo_text = "사용자가 보낸 안내 글을 자료실 이용자에게 보낼 한국어 한 문장으로 다듬으세요. 다듬은 문장은 write_file로 /reports/notice.md에 적으세요. write_file 말고 다른 도구는 쓰지 마세요. 파일에 적은 뒤에는 파일을 다시 읽지 말고, 적은 파일 위치를 한 문장으로 알려 주세요."
request_text = "안내 글: 자료실 정문 옆 무인 반납함은 휴관일에도 쓸 수 있습니다. 반납함에 넣은 책은 다음 운영일에 반납 처리됩니다."
run_config = {"configurable": {"thread_id": "memo-run"}}
APPROVAL = {"A": {"write_file": True}, "B": {}, "DRY": None}


def build_memo_agent(approval):
    return create_deep_agent(
        model=model,
        system_prompt=memo_text,
        middleware=[outer_limit],
        subagents=[helper_spec],
        interrupt_on=approval,
        checkpointer=InMemorySaver(),
    )


def call_args(messages, tool_name, arg_name):
    values = []
    for message in messages:
        if type(message).__name__ == "AIMessage":
            for call in message.tool_calls:
                if call["name"] == tool_name:
                    values.append(call["args"][arg_name])
    return values


def usage_row(ais):
    tin = sum(m.usage_metadata["input_tokens"] for m in ais)
    tout = sum(m.usage_metadata["output_tokens"] for m in ais)
    tcache = sum(((m.usage_metadata.get("input_token_details") or {}).get("cache_read", 0)) for m in ais)
    return {
        "input_tokens": tin, "output_tokens": tout, "cache_read": tcache,
        "cost_nocache": round((tin * 0.75 + tout * 4.50) / 1000000, 6),
        "cost_cache": round(((tin - tcache) * 0.75 + tcache * 0.075 + tout * 4.50) / 1000000, 6),
    }


def structure(agent):
    graph = agent.get_graph()
    names = list(agent.nodes["tools"].bound.tools_by_name)
    names.sort()
    return {"graph_nodes": list(graph.nodes), "has_hitl": "HumanInTheLoopMiddleware.after_model" in graph.nodes,
            "tool_count": len(names), "recursion_limit": agent.config["recursion_limit"]}


def one_run(mode):
    row = {"cond": mode, "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
    agent = build_memo_agent(APPROVAL[mode])
    row.update(structure(agent))
    first_input = {"messages": [HumanMessage(content=request_text)]}
    input_count = len(first_input["messages"])
    first_result = agent.invoke(first_input, run_config)
    row["paused"] = "__interrupt__" in first_result
    row["first_keys"] = list(first_result)
    row["memo_after_first"] = memo_path in first_result["files"]
    row["first_kinds"] = [type(m).__name__ for m in first_result["messages"]]
    first_ais = [m for m in first_result["messages"][input_count:] if type(m).__name__ == "AIMessage"]
    row["first_requests"] = len(first_ais)
    decisions = []
    paused_text = ""
    if "__interrupt__" in first_result:
        paused_value = first_result["__interrupt__"][0].value
        row["paused_actions"] = [[a["name"], a["args"].get("file_path"), len(a["args"].get("content", ""))] for a in paused_value["action_requests"]]
        row["allowed"] = [r["allowed_decisions"] for r in paused_value["review_configs"]]
        for action in paused_value["action_requests"]:
            paused_text = action["args"]["content"]
            decisions.append({"type": "approve"})
        row["paused_text"] = paused_text
    row["decisions"] = len(decisions)
    final = first_result
    if len(decisions) > 0:
        final = agent.invoke(Command(resume={"decisions": decisions}), run_config)
    msgs = final["messages"]
    run_new = msgs[input_count:]
    ais = [m for m in run_new if type(m).__name__ == "AIMessage"]
    row["paused_again"] = "__interrupt__" in final
    row["kinds"] = [type(m).__name__ for m in msgs]
    row["names_per_reply"] = [[c["name"] for c in m.tool_calls] for m in ais]
    row["calls_per_reply"] = [[[c["name"], c["args"]] for c in m.tool_calls] for m in ais]
    tms = [m for m in run_new if type(m).__name__ == "ToolMessage"]
    row["tool_msgs"] = [[m.name, m.status, m.content] for m in tms]
    row["write_paths"] = call_args(run_new, "write_file", "file_path")
    row["read_paths"] = call_args(run_new, "read_file", "file_path")
    row["task_types"] = call_args(run_new, "task", "subagent_type")
    row["answer"] = msgs[-1].text
    row["files_after"] = list(final["files"])
    if memo_path in final["files"]:
        body = final["files"][memo_path]["content"]
        row["memo"] = body
        row["memo_eq_paused"] = body == paused_text
    row["requests"] = len(ais)
    row["resume_requests"] = len(ais) - len(first_ais)
    row["tool_replies"] = len([m for m in ais if len(m.tool_calls) > 0])
    usage_none = [m for m in ais if m.usage_metadata is None]
    row["limit_hit"] = bool(usage_none) or ("Model call limits exceeded" in str(msgs[-1].content))
    row["req_eq_replies_plus1"] = row["requests"] == row["tool_replies"] + 1
    if not usage_none:
        row.update(usage_row(ais))
        row["first_input_tokens"] = ais[0].usage_metadata["input_tokens"]
    return row


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    assert mode in ("A", "B", "DRY")
    with open(out, "a", encoding="utf-8") as handle:
        for _ in range(rounds):
            if mode == "DRY":
                row = {"cond": "DRY", "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
                row["A"] = structure(build_memo_agent(APPROVAL["A"]))
                row["B"] = structure(build_memo_agent(APPROVAL["B"]))
            else:
                try:
                    row = one_run(mode)
                except Exception as error:  # 기록만 하고 다음으로(다시 보내지 않음)
                    row = {"cond": mode, "error": type(error).__name__ + ": " + str(error)[:300]}
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False)[:4000])


if __name__ == "__main__":
    main()
