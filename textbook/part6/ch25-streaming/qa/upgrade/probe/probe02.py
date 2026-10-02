"""Ch 25 02절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe02.py <M3|M2> <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  M3 : stream_mode=["messages", "updates", "custom"] — 노트북 본 실행과 같은 코드
  M2 : stream_mode=["updates", "custom"] — 값 바꿔 보기 후보. 평범한 콜백으로 on_llm_new_token 횟수를 셈
입력·지시 글·노드는 02-probe.md §0과 같다(노트북과 같은 코드).
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")

from typing_extensions import TypedDict  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain_core.callbacks import BaseCallbackHandler  # noqa: E402
from langgraph.config import get_stream_writer  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402

model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
system_text = "배송 문의에 답하는 안내 도우미입니다. 두 문장의 한국어로 답하세요."
QUESTION = "주문한 책이 아직 오지 않았어요. 언제 받을 수 있나요?"


class AnswerState(TypedDict):
    question: str
    answer: str


def write_answer(state):
    writer = get_stream_writer()
    writer({"stage": "before_model", "progress": 30})
    messages = [("system", system_text), ("user", state["question"])]
    response = model.invoke(messages)
    writer({"stage": "after_model", "progress": 100})
    return {"answer": response.text}


builder = StateGraph(AnswerState)
builder.add_node("write_answer", write_answer)
builder.add_edge(START, "write_answer")
builder.add_edge("write_answer", END)
graph = builder.compile()


class TokenCounter(BaseCallbackHandler):
    def __init__(self):
        self.count = 0

    def on_llm_new_token(self, token, **kwargs):
        self.count += 1


def runs_of(events):
    out = []
    for mode, _ in events:
        if not out or out[-1] != mode:
            out.append(mode)
    return out


def summarize_m3(events):
    row = {"n_events": len(events), "runs": runs_of(events)}
    counts = {}
    for mode, _ in events:
        counts[mode] = counts.get(mode, 0) + 1
    row["counts"] = counts
    row["custom_values"] = [d for m, d in events if m == "custom"]
    row["custom_pos"] = [i + 1 for i, (m, _) in enumerate(events) if m == "custom"]
    row["updates_pos"] = [i + 1 for i, (m, _) in enumerate(events) if m == "updates"]
    ups = [d for m, d in events if m == "updates"]
    row["updates_keys"] = [[list(u), list(u[list(u)[0]])] for u in ups]
    msg = [d for m, d in events if m == "messages"]
    row["msg_shape"] = sorted({(type(d).__name__, len(d), type(d[0]).__name__, type(d[1]).__name__) for d in msg})
    keysets = [tuple(sorted(d[1])) for d in msg]
    row["meta_keys_first"] = list(keysets[0]) if keysets else None
    row["meta_keys_all_same"] = len(set(keysets)) == 1
    for k in ["langgraph_node", "langgraph_step", "langgraph_triggers", "langgraph_path", "ls_provider",
              "ls_model_name", "ls_model_type", "ls_temperature", "checkpoint_ns"]:
        vals = []
        for d in msg:
            v = d[1].get(k, "<없음>")
            v = repr(v)
            if k == "checkpoint_ns":
                v = v.split(":")[0]
            if v not in vals:
                vals.append(v)
        row["meta_" + k] = vals
    row["n_chunks"] = len(msg)
    row["n_text"] = sum(1 for d in msg if d[0].text != "")
    empty = []
    for i, d in enumerate(msg):
        c = d[0]
        if c.text == "":
            empty.append([i + 1, c.response_metadata.get("finish_reason"), c.usage_metadata is not None,
                          c.chunk_position])
    row["empty"] = empty
    row["empty_from_end"] = [len(msg) - e[0] for e in empty]
    row["n_usage"] = sum(1 for d in msg if d[0].usage_metadata is not None)
    row["n_ids"] = len({d[0].id for d in msg})
    joined = ""
    for d in msg:
        joined = joined + d[0].text
    final = ups[0]["write_answer"]["answer"] if ups else None
    row["joined_eq_final"] = joined == final
    row["answer"] = final
    row["answer_len"] = len(final) if final is not None else None
    if msg:
        combined = msg[0][0]
        for d in msg[1:]:
            combined = combined + d[0]
        u = combined.usage_metadata
        row["usage"] = {"input": u["input_tokens"], "output": u["output_tokens"]} if u else None
        row["finish_reason"] = combined.response_metadata.get("finish_reason")
        row["model_name"] = combined.response_metadata.get("model_name")
        row["combined_type"] = type(combined).__name__
    return row


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            row = {"mode": mode, "round": round_no, "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            graph_input = {"question": QUESTION, "answer": ""}
            try:
                if mode == "M3":
                    events = list(graph.stream(graph_input, None, stream_mode=["messages", "updates", "custom"]))
                    row.update(summarize_m3(events))
                else:
                    counter = TokenCounter()
                    events = list(graph.stream(graph_input, {"callbacks": [counter]}, stream_mode=["updates", "custom"]))
                    counts = {}
                    for m, _ in events:
                        counts[m] = counts.get(m, 0) + 1
                    row.update({"n_events": len(events), "counts": counts, "runs": runs_of(events),
                                "custom_values": [d for m, d in events if m == "custom"],
                                "new_token_calls": counter.count,
                                "answer_len": len([d for m, d in events if m == "updates"][0]["write_answer"]["answer"])})
            except Exception as error:  # 기록만 하고 다음 회차로
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    main()
