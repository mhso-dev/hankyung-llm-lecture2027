"""Ch 25 03절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe03.py <T3|R3> <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  T3 : stream_mode=["messages", "updates", "custom"] — 노트북 본 실행과 같은 코드(사건마다 시각을 적음)
  R3 : stream_mode=["updates", "messages", "custom"] — 값 바꿔 보기 후보(모드 목록의 차례만 바꿈)
입력·시스템 메시지 글·노드는 02절과 같다(03-probe.md §0).
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")

from typing_extensions import TypedDict  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langgraph.config import get_stream_writer  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402

model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
system_text = "배송 문의에 답하는 안내 도우미입니다. 두 문장의 한국어로 답하세요."
QUESTION = "주문한 책이 아직 오지 않았어요. 언제 받을 수 있나요?"
MODES = {"T3": ["messages", "updates", "custom"], "R3": ["updates", "messages", "custom"]}


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


def collect_timed_events(graph_to_run, graph_input, config, modes):
    timed_run = {"start": time.perf_counter(), "events": [], "times": []}
    for event in graph_to_run.stream(graph_input, config, stream_mode=modes):
        timed_run["events"].append(event)
        timed_run["times"].append(time.perf_counter())
    timed_run["end"] = time.perf_counter()
    return timed_run


# Ch 21 runner_tools.py 판 본문 그대로(probe 전용 사본)
def estimate_cost(usage, input_rate, cached_input_rate, output_rate):
    if usage is None:
        return None
    details = usage.get("input_token_details", {})
    cache_read = details.get("cache_read", 0)
    normal_input = usage["input_tokens"] - cache_read
    input_cost = normal_input * input_rate + cache_read * cached_input_rate
    output_cost = usage["output_tokens"] * output_rate
    price_unit = 1000000
    return (input_cost + output_cost) / price_unit


def runs_of(events):
    out = []
    for mode, _ in events:
        if not out or out[-1] != mode:
            out.append(mode)
    return out


def summarize(run):
    events, times, start, end = run["events"], run["times"], run["start"], run["end"]
    row = {"n_events": len(events), "n_times": len(times), "runs": runs_of(events)}
    counts = {}
    for mode, _ in events:
        counts[mode] = counts.get(mode, 0) + 1
    row["counts"] = counts
    row["first_mode"] = events[0][0]
    row["first_data"] = events[0][1] if events[0][0] != "messages" else "<messages>"
    msg_pos = [i + 1 for i, (m, _) in enumerate(events) if m == "messages"]
    row["first_msg_pos"] = msg_pos[0] if msg_pos else None
    row["first_msg_textlen"] = len(events[msg_pos[0] - 1][1][0].text) if msg_pos else None
    text_pos = None
    for i, (m, d) in enumerate(events):
        if m == "messages" and d[0].text != "":
            text_pos = i + 1
            break
    row["first_text_pos"] = text_pos
    row["custom_pos"] = [i + 1 for i, (m, _) in enumerate(events) if m == "custom"]
    row["updates_pos"] = [i + 1 for i, (m, _) in enumerate(events) if m == "updates"]
    row["updates_last"] = row["updates_pos"] == [len(events)]
    row["times_eq_events"] = len(times) == len(events)
    row["non_decreasing"] = all(times[i] <= times[i + 1] for i in range(len(times) - 1)) and start <= times[0] and times[-1] <= end
    t_first = times[0]
    t_msg = times[msg_pos[0] - 1] if msg_pos else None
    t_text = times[text_pos - 1] if text_pos else None
    row["first_lt_text"] = t_first < t_text if t_text else None
    row["text_lt_end"] = t_text < end if t_text else None
    row["msg_le_text"] = t_msg <= t_text if t_text else None
    last_msg_t = times[msg_pos[-1] - 1] if msg_pos else None
    second_custom_t = times[row["custom_pos"][1] - 1] if len(row["custom_pos"]) > 1 else None
    row["custom100_after_last_msg"] = (second_custom_t >= last_msg_t) if (last_msg_t and second_custom_t) else None
    row["s_first_event"] = round(t_first - start, 3)
    row["s_first_msg"] = round(t_msg - start, 3) if t_msg else None
    row["s_first_text"] = round(t_text - start, 3) if t_text else None
    row["s_last_msg"] = round(last_msg_t - start, 3) if last_msg_t else None
    row["s_custom100"] = round(second_custom_t - start, 3) if second_custom_t else None
    row["s_total"] = round(end - start, 3)
    row["s_after_text"] = round(end - t_text, 3) if t_text else None
    row["ratio_text_total"] = round((t_text - start) / (end - start), 3) if t_text else None
    usages = [d[0].usage_metadata for m, d in events if m == "messages" and d[0].usage_metadata is not None]
    row["n_usage"] = len(usages)
    usage = usages[0] if usages else None
    row["usage"] = dict(usage) if usage else None
    row["cost"] = round(estimate_cost(usage, 0.75, 0.075, 4.50), 6) if usage else None
    joined = ""
    for m, d in events:
        if m == "messages":
            joined = joined + d[0].text
    ups = [d for m, d in events if m == "updates"]
    final = ups[0]["write_answer"]["answer"] if ups else None
    row["joined_eq_final"] = joined == final
    row["answer_len"] = len(final) if final is not None else None
    row["answer"] = final
    return row


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            row = {"mode": mode, "round": round_no, "at": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
            graph_input = {"question": QUESTION, "answer": ""}
            try:
                run = collect_timed_events(graph, graph_input, None, MODES[mode])
                row.update(summarize(run))
            except Exception as error:  # 기록만 하고 다음 회차로
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
            handle.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
            print(json.dumps(row, ensure_ascii=False, default=str)[:1800])


if __name__ == "__main__":
    main()
