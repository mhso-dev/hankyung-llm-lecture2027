"""Ch 30 09절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe09.py <회차 번호> <기록 파일(JSONL, 이어 쓰기)>
프로세스 하나(= 새 커널 하나처럼)가 노트북의 모델 요청 셀 셋과 같은 코드를 차례로 부른다.
  (a) 시험용 클라이언트로 POST /v1/chat/live          — 노트북 2절
  (b) 시험용 클라이언트로 POST /v1/chat/live/stream   — 노트북 3절(06 도구 파일 함수로 SSE 사건을 나눔)
  (c) build_live_agent().astream(…, stream_mode="messages")를 모음 — 노트북 4절 실험
입력(질문·요청 머리·스레드 이름)과 판단 규칙은 09-probe.md §0과 같다.
측정용 덧붙임 둘(노트북에는 없음, 요청 내용은 바꾸지 않음):
  · httpx 클라이언트의 send를 감싸 모델 서비스(api.openai.com)로 나간 HTTP 요청 수를 단계마다 셈
  · 도구 함수 lookup_library_hours의 func를 감싸, 단계마다 도구가 받은 인자를 적음
"""
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[6]
LAB = ROOT / "labs/part7/ch30-fastapi-serving"
load_dotenv(ROOT / ".env")
os.chdir(LAB)
sys.path.insert(0, str(LAB))
sys.path.insert(0, str(LAB / "notebooks"))

from serve_tools import join_tokens, parse_sse, split_sse  # noqa: E402

sent = {"n": 0}
_async_send = httpx.AsyncClient.send
_sync_send = httpx.Client.send


async def counting_async_send(self, request, **kwargs):
    if request.url.host == "api.openai.com":
        sent["n"] += 1
    return await _async_send(self, request, **kwargs)


def counting_sync_send(self, request, **kwargs):
    if request.url.host == "api.openai.com":
        sent["n"] += 1
    return _sync_send(self, request, **kwargs)


httpx.AsyncClient.send = counting_async_send
httpx.Client.send = counting_sync_send

from fastapi.testclient import TestClient  # noqa: E402
from agent_service.app import app  # noqa: E402
from agent_service import live_agent as live_module  # noqa: E402

tool_days = []
_tool_func = live_module.lookup_library_hours.func


def recording_tool(day):
    tool_days.append(day)
    return _tool_func(day)


live_module.lookup_library_hours.func = recording_tool

auth_headers = {"Authorization": "Bearer local-demo-token"}
question_body = {"question": "한빛도서관 월요일 운영 시간은?", "thread_id": "live-1"}


def now():
    return datetime.now(timezone.utc).strftime("%H:%M:%SZ")


def step_a(client, row):
    before_n, before_t = sent["n"], len(tool_days)
    response = client.post("/v1/chat/live", json=question_body, headers=auth_headers)
    body = response.json()
    row["a_status"] = response.status_code
    row["a_keys"] = list(body)
    row["a_thread_id"] = body.get("thread_id")
    row["a_answer"] = body.get("answer")
    row["a_answer_len"] = len(body.get("answer") or "")
    row["a_requests"] = sent["n"] - before_n
    row["a_tool_days"] = tool_days[before_t:]


def step_b(client, row):
    before_n, before_t = sent["n"], len(tool_days)
    response = client.post("/v1/chat/live/stream", json=question_body, headers=auth_headers)
    events = [parse_sse(t) for t in split_sse(response.text)]
    names = [e.get("event") for e in events]
    row["b_status"] = response.status_code
    row["b_content_type"] = response.headers.get("content-type")
    row["b_event_count"] = len(events)
    row["b_names_set"] = sorted(set(names))
    row["b_first_event"] = names[0] if names else None
    row["b_last_event"] = names[-1] if names else None
    row["b_token_count"] = names.count("token")
    ids = [e.get("id") for e in events]
    row["b_first_id"] = ids[0] if ids else None
    row["b_last_token_id"] = ids[-2] if len(ids) > 1 else None
    row["b_ids_consecutive"] = [e.get("id") for e in events if e.get("event") == "token"] == [
        "live-1:" + str(i) for i in range(names.count("token"))]
    row["b_done_fields"] = sorted(events[-1]) if events else None
    row["b_done_data"] = json.loads(events[-1]["data"]) if events and "data" in events[-1] else None
    token_values = [json.loads(e["data"]) for e in events if e.get("event") == "token"]
    row["b_token_keys"] = sorted(set(k for v in token_values for k in v))
    row["b_joined"] = join_tokens(token_values)
    row["b_joined_len"] = len(row["b_joined"])
    row["b_joined_eq_a"] = row["b_joined"] == row.get("a_answer")
    row["b_requests"] = sent["n"] - before_n
    row["b_tool_days"] = tool_days[before_t:]
    row["b_error_events"] = [e.get("data") for e in events if e.get("event") == "error"]


async def step_c(row):
    before_n, before_t = sent["n"], len(tool_days)
    live_agent = live_module.build_live_agent()
    live_input = {"messages": [{"role": "user", "content": question_body["question"]}]}
    message_events = []
    async for event in live_agent.astream(live_input, stream_mode="messages"):
        message_events.append(event)
    row["c_event_count"] = len(message_events)
    row["c_event_shape"] = sorted(set(type(e).__name__ + str(len(e)) for e in message_events))
    nodes = [e[1]["langgraph_node"] for e in message_events]
    order = []
    for n in nodes:
        if not order or order[-1] != n:
            order.append(n)
    row["c_node_order"] = order
    row["c_node_counts"] = {n: nodes.count(n) for n in sorted(set(nodes))}
    row["c_types_by_node"] = {n: sorted(set(type(e[0]).__name__ for e in message_events if e[1]["langgraph_node"] == n)) for n in sorted(set(nodes))}
    tools_events = [e for e in message_events if e[1]["langgraph_node"] == "tools"]
    row["c_tools_texts"] = [e[0].text for e in tools_events]
    row["c_tools_names"] = [getattr(e[0], "name", None) for e in tools_events]
    row["c_tools_positions"] = [i + 1 for i, e in enumerate(message_events) if e[1]["langgraph_node"] == "tools"]
    ids = []
    pattern = []
    for e in message_events:
        if e[1]["langgraph_node"] == "model":
            if e[0].id not in ids:
                ids.append(e[0].id)
            pattern.append(ids.index(e[0].id))
    runs = []
    for p in pattern:
        if runs and runs[-1][0] == p:
            runs[-1][1] += 1
        else:
            runs.append([p, 1])
    row["c_model_id_runs"] = runs
    row["c_distinct_model_ids"] = len(ids)
    row["c_none_ids"] = sum(1 for e in message_events if e[0].id is None)
    text_eq = True
    for e in message_events:
        joined = "".join(b["text"] for b in e[0].content_blocks if b.get("type") == "text" and b.get("text"))
        if joined != e[0].text:
            text_eq = False
    row["c_text_eq_blocks"] = text_eq
    run1 = "".join(e[0].text for e in message_events if e[1]["langgraph_node"] in ["model"])
    run2 = "".join(e[0].text for e in message_events if e[1]["langgraph_node"] in ["model", "tools"])
    row["c_run1"] = run1
    row["c_run2"] = run2
    row["c_run2_eq_tools_plus_run1"] = run2 == "".join(row["c_tools_texts"]) + run1
    row["c_run1_starts_with_tool"] = run1.startswith("09:00~18:00")
    row["c_len_diff"] = len(run2) - len(run1)
    row["c_text_chunks_model"] = sum(1 for e in message_events if e[1]["langgraph_node"] == "model" and e[0].text != "")
    arg_parts = {}
    for e in message_events:
        for chunk in getattr(e[0], "tool_call_chunks", []) or []:
            key = (e[0].id, chunk.get("index"))
            arg_parts[key] = arg_parts.get(key, "") + (chunk.get("args") or "")
    row["c_tool_call_args"] = list(arg_parts.values())
    usage = [e[0].usage_metadata for e in message_events if getattr(e[0], "usage_metadata", None)]
    row["c_usage_chunks"] = len(usage)
    row["c_input_tokens"] = sum(u["input_tokens"] for u in usage)
    row["c_output_tokens"] = sum(u["output_tokens"] for u in usage)
    row["c_cache_read"] = sum(u.get("input_token_details", {}).get("cache_read", 0) for u in usage)
    row["c_per_request_input"] = [u["input_tokens"] for u in usage]
    row["c_per_request_output"] = [u["output_tokens"] for u in usage]
    row["c_requests"] = sent["n"] - before_n
    row["c_tool_days"] = tool_days[before_t:]
    row["c_first_meta_keys"] = sorted(message_events[0][1]) if message_events else None


async def main():
    round_no, out = sys.argv[1], sys.argv[2]
    row = {"round": int(round_no), "start": now(), "key_set": os.getenv("OPENAI_API_KEY") is not None}
    client = TestClient(app)
    for name, step in [("a", step_a), ("b", step_b)]:
        try:
            step(client, row)
        except Exception as error:  # 기록만 하고 다음 단계로(다시 보내지 않음)
            row[name + "_error"] = type(error).__name__ + ": " + str(error)[:300]
    try:
        await step_c(row)
    except Exception as error:
        row["c_error"] = type(error).__name__ + ": " + str(error)[:300]
    row["total_requests"] = sent["n"]
    row["end"] = now()
    with open(out, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps(row, ensure_ascii=False)[:3000])


if __name__ == "__main__":
    asyncio.run(main())
