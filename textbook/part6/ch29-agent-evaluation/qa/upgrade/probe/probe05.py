"""Ch 29 05절(실습) 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe05.py R <시작 회차> <끝 회차> <기록 파일(JSONL, 이어 쓰기)>
  R : 노트북 2~7절과 같은 코드 — 도구 둘을 붙인 에이전트(create_agent + 실행 한도 20)를 호출 한도 4(실행 1)와
      호출 한도 2(실행 2)로 한 번씩 실행해, 두 궤적을 검색어를 뺀 모드 넷으로 판정하고 04절 공통 칸 두 줄로 옮겨 담는다.
      회차마다 요청 약 5번(실행 1 = 3 + 실행 2 = 2, 상한 4 + 2 = 6). 평가 모델은 부르지 않는다.
입력·도구·시스템 메시지 글·한도·질문·기준 궤적은 05-probe.md §0과 같다(노트북과 같은 코드).
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT / "labs/part6/ch29-agent-evaluation/notebooks"))

from agentevals.trajectory.match import create_trajectory_match_evaluator  # noqa: E402
from langchain.agents import create_agent  # noqa: E402
from langchain.agents.middleware import ModelCallLimitMiddleware  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import HumanMessage  # noqa: E402
from langchain.tools import tool  # noqa: E402
from eval_tools import called_tool_names, four_modes, make_trajectory, show_messages, sum_usage, tool_call_names  # noqa: E402

model = init_chat_model(
    "openai:gpt-5.4-mini",
    temperature=0,
    reasoning_effort="none",
)

question = "일반 도서는 며칠 동안 빌릴 수 있나요?"
reference_answer = "일반 도서는 14일 동안 빌릴 수 있습니다."
tool_results = {
    "search_documents": "[LIB-001] 일반 도서는 14일 동안 대출할 수 있습니다. 예약자가 없으면 한 번 연장할 수 있습니다.",
    "check_source": "LIB-001 문서가 있습니다. 제목: 도서 대출 기간",
}
search_args = {"query": "도서 대출 기간"}
source_args = {"doc_id": "LIB-001"}
reference_calls = [
    {"name": "search_documents", "args": search_args, "id": "call_1", "type": "tool_call"},
    {"name": "check_source", "args": source_args, "id": "call_2", "type": "tool_call"},
]
reference = make_trajectory(question, reference_calls, tool_results, reference_answer)


@tool
def search_documents(query: str):
    """도서관 규정 문서를 검색어로 찾아, 문서 ID를 붙인 글로 내놓습니다."""
    return tool_results["search_documents"]


@tool
def check_source(doc_id: str):
    """문서 ID로 그 문서가 있는지 확인하고, 있으면 제목을 내놓습니다."""
    if doc_id == "LIB-001":
        return tool_results["check_source"]
    return doc_id + " 문서가 없습니다."


modes = ["strict", "unordered", "subset", "superset"]
search_free = {}
for mode in modes:
    search_free[mode] = create_trajectory_match_evaluator(
        trajectory_match_mode=mode,
        tool_args_match_overrides={"search_documents": "ignore"},
    )

agent_rule = "도서관 규정 질문에는 먼저 search_documents로 문서를 찾고, 찾은 문서 ID로 check_source를 불러 문서가 있는지 확인한 뒤, 확인한 문서의 글만 근거로 한국어 한 문장으로 답하세요."
run_config = {"recursion_limit": 20}


def run_agent(limit):
    call_limit = ModelCallLimitMiddleware(run_limit=limit, exit_behavior="end")
    agent = create_agent(model, tools=[search_documents, check_source], system_prompt=agent_rule, middleware=[call_limit])
    first_input = {"messages": [HumanMessage(content=question)]}
    result = agent.invoke(first_input, run_config)
    return result["messages"]


def count_asked(messages):
    asked = 0
    for message in messages:
        if type(message).__name__ == "AIMessage":
            if len(tool_call_names(message)) > 0:
                asked = asked + 1
    return asked


def model_part(messages):
    if messages[-1].usage_metadata is None:
        return messages[:-1]
    return messages


def run_row(name, messages, usage, score):
    return {
        "이름": name,
        "요청 수": usage["requests"],
        "도구 요청 수": len(called_tool_names(messages)),
        "토큰 수": usage["input_tokens"] + usage["output_tokens"],
        "걸린 초": None,
        "점수": float(score),
    }


def trajectory_text(messages):
    parts = []
    for m in messages:
        calls = [[c["name"], c["args"]] for c in getattr(m, "tool_calls", [])]
        parts.append(type(m).__name__ + "|" + str(m.content) + "|" + json.dumps(calls, ensure_ascii=False))
    return "\n".join(parts)


def record(name, limit, msgs):
    row = {"limit": limit}
    row["kinds"] = [type(m).__name__ for m in msgs]
    row["has_system"] = "SystemMessage" in row["kinds"]
    ais = [m for m in msgs if type(m).__name__ == "AIMessage"]
    row["calls_per_ai"] = [len(m.tool_calls) for m in ais]
    row["ai_usage_none"] = [m.usage_metadata is None for m in ais]
    row["tool_order"] = called_tool_names(msgs)
    row["tool_args"] = [c["args"] for m in ais for c in m.tool_calls]
    tms = [m for m in msgs if type(m).__name__ == "ToolMessage"]
    row["tool_status"] = [m.status for m in tms]
    row["tool_texts_equal_reference"] = [m.content in tool_results.values() for m in tms]
    part = model_part(msgs)
    usage = sum_usage(part)
    asked = count_asked(msgs)
    row["cut_last"] = len(msgs) - len(part)
    row["asked"] = asked
    row["requests"] = usage["requests"]
    row["formula"] = usage["requests"] == asked + 1
    row["last_content"] = msgs[-1].content
    row["last_usage_none"] = msgs[-1].usage_metadata is None
    row["last_equals_reference_answer"] = msgs[-1].content == reference_answer
    mw = [m for m in part if type(m).__name__ == "AIMessage"]
    row["per_request_input"] = [m.usage_metadata["input_tokens"] for m in mw]
    row["per_request_output"] = [m.usage_metadata["output_tokens"] for m in mw]
    row["cache"] = [m.usage_metadata.get("input_token_details", {}).get("cache_read", 0) for m in mw]
    row["tokens"] = {"input": usage["input_tokens"], "output": usage["output_tokens"]}
    row["cost_notebook_way"] = round((usage["input_tokens"] * 0.75 + usage["output_tokens"] * 4.50) / 1000000, 6)
    row["trajectory_sha_no_ids"] = hashlib.sha256(trajectory_text(msgs).encode("utf-8")).hexdigest()[:12]
    modes_row = four_modes(msgs, reference, search_free)
    row["search_free_modes"] = modes_row
    row["common_row"] = run_row(name, msgs, usage, modes_row["strict"])
    return row


def main():
    mode, start, end, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    assert mode == "R"
    node_agent = create_agent(model, tools=[search_documents, check_source], system_prompt=agent_rule,
                              middleware=[ModelCallLimitMiddleware(run_limit=4, exit_behavior="end")])
    nodes = list(node_agent.get_graph().nodes)
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(start, end + 1):
            row = {"mode": mode, "round": round_no, "start": datetime.now(timezone.utc).strftime("%H:%M:%SZ"), "nodes": nodes}
            try:
                first_messages = run_agent(4)
                row["run1"] = record("실행 1(한도 4)", 4, first_messages)
            except Exception as error:  # 기록만 하고 다음으로(다시 보내지 않음)
                row["run1_error"] = type(error).__name__ + ": " + str(error)[:300]
            try:
                second_messages = run_agent(2)
                row["run2"] = record("실행 2(한도 2)", 2, second_messages)
            except Exception as error:
                row["run2_error"] = type(error).__name__ + ": " + str(error)[:300]
            if "run1" in row and "run2" in row:
                a = [[c["name"], c["args"]] for m in first_messages if type(m).__name__ == "AIMessage" for c in m.tool_calls]
                b = [[c["name"], c["args"]] for m in second_messages if type(m).__name__ == "AIMessage" for c in m.tool_calls]
                row["run2_calls_equal_run1"] = a == b
            row["end"] = datetime.now(timezone.utc).strftime("%H:%M:%SZ")
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
            print(json.dumps(row, ensure_ascii=False)[:3000])


if __name__ == "__main__":
    main()
