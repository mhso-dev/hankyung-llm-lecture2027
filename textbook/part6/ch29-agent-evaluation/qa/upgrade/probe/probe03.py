"""Ch 29 03절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe03.py A <시작 회차> <끝 회차> <기록 파일(JSONL, 이어 쓰기)>
  A : 노트북 4~6절과 같은 코드 — 도구 둘을 붙인 에이전트(create_agent + 호출 한도 4 + 실행 한도 20)를 한 번 실행해
      궤적을 만들고, 검색 도구만 인자를 보지 않는 모드 넷으로 판정한 뒤, 평가 모델로 두 번 판정한다
      (① 에이전트 궤적 그대로 ② 마지막 답 글만 틀린 글로 바꾼 궤적). 회차마다 요청 약 5번(에이전트 3 + 평가 모델 2).
입력·도구·시스템 메시지 글·한도·질문·판정 머리글은 03-probe.md §0과 같다(노트북과 같은 코드).
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

from agentevals.trajectory.llm import TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE, create_trajectory_llm_as_judge  # noqa: E402
from agentevals.trajectory.match import create_trajectory_match_evaluator  # noqa: E402
from langchain.agents import create_agent  # noqa: E402
from langchain.agents.middleware import ModelCallLimitMiddleware  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import AIMessage, HumanMessage  # noqa: E402
from langchain.tools import tool  # noqa: E402
from langchain_core.callbacks import get_usage_metadata_callback  # noqa: E402
from eval_tools import called_tool_names, make_trajectory, trajectory_pass  # noqa: E402

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
wrong_text = "일반 도서는 7일 동안 빌릴 수 있습니다."

model = init_chat_model(
    "openai:gpt-5.4-mini",
    temperature=0,
    reasoning_effort="none",
)
accuracy_judge = create_trajectory_llm_as_judge(judge=model, prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE)


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


call_limit = ModelCallLimitMiddleware(run_limit=4, exit_behavior="end")
agent_rule = "도서관 규정 질문에는 먼저 search_documents로 문서를 찾고, 찾은 문서 ID로 check_source를 불러 문서가 있는지 확인한 뒤, 확인한 문서의 글만 근거로 한국어 한 문장으로 답하세요."
library_agent = create_agent(model, tools=[search_documents, check_source], system_prompt=agent_rule, middleware=[call_limit])
run_config = {"recursion_limit": 20}

modes = ["strict", "unordered", "subset", "superset"]
exact_modes = {}
search_free = {}
for mode in modes:
    exact_modes[mode] = create_trajectory_match_evaluator(trajectory_match_mode=mode)
    search_free[mode] = create_trajectory_match_evaluator(
        trajectory_match_mode=mode,
        tool_args_match_overrides={"search_documents": "ignore"},
    )


def four_modes(messages, reference, evaluators):
    row = {}
    for mode in evaluators:
        row[mode] = trajectory_pass(messages, reference, evaluators[mode])
    return row


def judged(messages):
    with get_usage_metadata_callback() as cb:
        verdict = accuracy_judge(outputs=messages, reference_outputs=reference)
    usage = {}
    for name, value in cb.usage_metadata.items():
        usage = {"model": name, "input": value["input_tokens"], "output": value["output_tokens"],
                 "cache": value.get("input_token_details", {}).get("cache_read", 0)}
    return verdict, usage, len(cb.usage_metadata)


def trajectory_text(messages):
    parts = []
    for m in messages:
        parts.append(type(m).__name__ + "|" + str(m.content) + "|" + json.dumps(getattr(m, "tool_calls", []) and [[c["name"], c["args"]] for c in m.tool_calls], ensure_ascii=False))
    return "\n".join(parts)


def main():
    mode, start, end, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    assert mode == "A"
    nodes = list(library_agent.get_graph().nodes)
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(start, end + 1):
            row = {"mode": mode, "round": round_no, "start": datetime.now(timezone.utc).strftime("%H:%M:%SZ"), "nodes": nodes}
            try:
                first_input = {"messages": [HumanMessage(content=question)]}
                result = library_agent.invoke(first_input, run_config)
                msgs = result["messages"]
                row["kinds"] = [type(m).__name__ for m in msgs]
                row["has_system"] = "SystemMessage" in row["kinds"]
                ais = [m for m in msgs if type(m).__name__ == "AIMessage"]
                row["calls_per_response"] = [len(m.tool_calls) for m in ais]
                row["tool_order"] = called_tool_names(msgs)
                row["tool_args"] = [c["args"] for m in ais for c in m.tool_calls]
                tms = [m for m in msgs if type(m).__name__ == "ToolMessage"]
                row["tool_status"] = [m.status for m in tms]
                row["tool_texts_equal_reference"] = [m.content in tool_results.values() for m in tms]
                asked = len([m for m in ais if m.tool_calls])
                row["asked_responses"] = asked
                row["requests"] = len(ais)
                row["requests_eq_asked_plus_1"] = len(ais) == asked + 1
                usage_none = [m for m in ais if m.usage_metadata is None]
                row["limit_hit"] = bool(usage_none) or ("limit" in str(msgs[-1].content).lower())
                if not usage_none:
                    tin = sum(m.usage_metadata["input_tokens"] for m in ais)
                    tout = sum(m.usage_metadata["output_tokens"] for m in ais)
                    cache = sum(m.usage_metadata.get("input_token_details", {}).get("cache_read", 0) for m in ais)
                    row["agent_tokens"] = {"input": tin, "output": tout, "cache": cache,
                                           "per_request_input": [m.usage_metadata["input_tokens"] for m in ais],
                                           "per_request_output": [m.usage_metadata["output_tokens"] for m in ais]}
                    row["agent_cost_notebook_way"] = round((tin * 0.75 + tout * 4.50) / 1000000, 6)
                row["answer"] = msgs[-1].content
                row["answer_equals_reference"] = msgs[-1].content == reference_answer
                row["trajectory_sha"] = hashlib.sha256(trajectory_text(msgs).encode("utf-8")).hexdigest()[:12]
                row["exact_modes"] = four_modes(msgs, reference, exact_modes)
                row["search_free_modes"] = four_modes(msgs, reference, search_free)
                verdict, usage, n_models = judged(msgs)
                row["judge_agent"] = {"key": verdict["key"], "score": verdict["score"], "comment": verdict["comment"], "usage": usage, "models_seen": n_models}
                wrong_run = msgs.copy()
                wrong_run[-1] = AIMessage(content=wrong_text)
                row["wrong_run_strict_search_free"] = trajectory_pass(wrong_run, reference, search_free["strict"])
                verdict2, usage2, n_models2 = judged(wrong_run)
                row["judge_wrong"] = {"key": verdict2["key"], "score": verdict2["score"], "comment": verdict2["comment"], "usage": usage2, "models_seen": n_models2}
            except Exception as error:  # 기록만 하고 다음 회차로(다시 보내지 않음)
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
            row["end"] = datetime.now(timezone.utc).strftime("%H:%M:%SZ")
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
            print(json.dumps(row, ensure_ascii=False)[:2500])


if __name__ == "__main__":
    main()
