"""Author Ch23/Ch24 notebooks, sources, QA records, and figure specifications."""
from __future__ import annotations
# 2026-09-25 Ch 23 품질 개선: 이 파일은 Ch 23과 Ch 24를 함께 쓰는 옛 생성기입니다.
# Ch 23 개선본(노트북·_src·그림)은 textbook/part6/ch23-persistence/qa/upgrade/author_NN.py가 씁니다.
# 그래서 write_all()은 Ch 23 쪽(노트북·_src·figures/_gen_figures.py)을 건너뛰고, Ch 24 쪽 동작은 그대로 둡니다.
# 2026-09-25 Ch 24 01절 품질 개선: Ch 24 개선본(노트북·_src·그림·도구 파일)은
# textbook/part6/ch24-human-in-the-loop/qa/upgrade/author_NN.py가 씁니다. 이 파일을 실행하면 Ch 24 개선본을
# 옛 판으로 덮어쓰므로, 아래 줄에서 실행을 막습니다(Ch 23 쪽은 이미 건너뛰어 영향 없음). 읽기 자료로만 둡니다.
raise SystemExit("옛 Ch 23·Ch 24 공용 생성기입니다. Ch 23은 ch23-persistence/qa/upgrade/author_NN.py, "
                 "Ch 24는 ch24-human-in-the-loop/qa/upgrade/author_NN.py를 쓰세요.")
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

def lines(text: str) -> list[str]:
    return text.strip("\n").splitlines(keepends=True)

def md(source: str, part: str = "example") -> dict:
    return {"cell_type": "markdown", "id": "m", "metadata": {"lesson_part": part}, "source": lines(source)}

def code(source: str, part: str = "example") -> dict:
    return {"cell_type": "code", "execution_count": None, "id": "c", "metadata": {"lesson_part": part}, "outputs": [], "source": lines(source)}

def notebook(title: str, question: str, fmt: str, cells: list[dict]) -> dict:
    result = [md(f"# {title}\n\n{question}"), *cells]
    for index, cell in enumerate(result, 1):
        cell["id"] = f"cell-{index:02d}"
        if fmt == "experiment":
            cell["metadata"].pop("lesson_part", None)
    return {
        "cells": result,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "lesson_format": fmt,
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

NOTEBOOKS: dict[str, dict] = {}

NOTEBOOKS["ch23-persistence/01-체크포인터와-스레드"] = notebook(
    "체크포인터와 스레드", "같은 thread_id와 다른 thread_id는 저장된 상태를 어떻게 나누는지 확인합니다.", "experiment", [
    md("## 그래프와 체크포인터 준비\n\n`InMemorySaver`를 연결한 작은 누적 그래프를 만듭니다."),
    code('''from typing_extensions import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

class State(TypedDict):
    total: int
    events: list[str]

def add(state: State) -> dict:
    value = state["events"][-1]
    return {"total": state["total"] + int(value)}

builder = StateGraph(State)
builder.add_node("add", add)
builder.add_edge(START, "add")
builder.add_edge("add", END)
memory = InMemorySaver()
graph = builder.compile(checkpointer=memory)
print("checkpointer:", type(memory).__name__)'''),
    md("## 같은 스레드로 두 번 실행\n\n같은 `thread_id`를 사용하면 두 번째 입력을 기존 상태에 이어서 처리합니다."),
    code('''config_a = {"configurable": {"thread_id": "customer-a"}}
first = graph.invoke({"total": 0, "events": ["3"]}, config_a)
second = graph.invoke({"events": ["4"]}, config_a)
snapshot = graph.get_state(config_a)
print("first total:", first["total"])
print("second total:", second["total"])
print("saved total:", snapshot.values["total"])
print("next:", snapshot.next)'''),
    md("## 다른 스레드와 기록 비교\n\n입력은 같게 두고 `thread_id`만 바꾸어 상태 격리를 확인합니다."),
    code('''config_b = {"configurable": {"thread_id": "customer-b"}}
other = graph.invoke({"total": 0, "events": ["4"]}, config_b)
history_a = list(graph.get_state_history(config_a))
history_b = list(graph.get_state_history(config_b))
print("customer-a total:", second["total"], "history:", len(history_a))
print("customer-b total:", other["total"], "history:", len(history_b))
assert second["total"] == 7 and other["total"] == 4'''),
])

NOTEBOOKS["ch23-persistence/02-PostgresSaver-준비와-스키마"] = notebook(
    "PostgresSaver 준비와 스키마", "빈 PostgreSQL 스키마에서 setup 전후의 실행 결과와 생성 테이블을 확인합니다.", "paired", [
    md("## 접속과 그래프 준비\n\n로컬 실습 데이터베이스 안에 전용 스키마를 새로 만듭니다."),
    code('''import os
import psycopg
from typing_extensions import TypedDict
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, START, StateGraph

base_uri = os.getenv("CH23_POSTGRES_URI", "postgresql://postgres:postgres@localhost:55432/postgres")
with psycopg.connect(base_uri, autocommit=True) as conn:
    conn.execute("DROP SCHEMA IF EXISTS ch23_lab CASCADE")
    conn.execute("CREATE SCHEMA ch23_lab")
db_uri = base_uri + "?options=-csearch_path%3Dch23_lab"

class State(TypedDict):
    value: int

builder = StateGraph(State)
builder.add_node("double", lambda state: {"value": state["value"] * 2})
builder.add_edge(START, "double")
builder.add_edge("double", END)
print("schema: ch23_lab")'''),
    md("## Before: setup 없이 실행", "before"),
    code('''before_error = ""
try:
    with PostgresSaver.from_conn_string(db_uri) as saver:
        builder.compile(checkpointer=saver).invoke(
            {"value": 6}, {"configurable": {"thread_id": "before"}}
        )
except Exception as exc:
    before_error = f"{type(exc).__name__}: {exc}"
print(before_error.splitlines()[0])
assert "UndefinedTable" in before_error''', "before"),
    md("## After: setup 뒤 실행하고 표 확인", "after"),
    code('''with PostgresSaver.from_conn_string(db_uri) as saver:
    saver.setup()
    graph = builder.compile(checkpointer=saver)
    after = graph.invoke({"value": 6}, {"configurable": {"thread_id": "after"}})

with psycopg.connect(base_uri) as conn:
    rows = conn.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema='ch23_lab' ORDER BY table_name"
    ).fetchall()
tables = [row[0] for row in rows]
print("result:", after)
print("tables:", tables)
assert after["value"] == 12 and "checkpoints" in tables and "checkpoint_writes" in tables''', "after"),
])

NOTEBOOKS["ch23-persistence/03-스레드-재개와-대화-이어가기"] = notebook(
    "스레드 재개와 대화 이어가기", "프로그램 객체를 새로 만든 뒤에도 같은 스레드의 상태가 이어지는지 확인합니다.", "experiment", [
    md("## 파일 체크포인터 준비\n\n실행을 반복해도 결과가 일정하도록 이전 실습 파일을 지웁니다."),
    code('''import sqlite3
import operator
from pathlib import Path
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

candidates = [Path.cwd(), *Path.cwd().parents]
lab = next((p / "labs/part6/ch23-persistence" for p in candidates if (p / "labs/part6/ch23-persistence").is_dir()), None)
if lab is None:
    lab = next(p for p in candidates if p.name == "ch23-persistence")
db_path = lab / "data/thread-resume.sqlite"
db_path.parent.mkdir(parents=True, exist_ok=True)
db_path.unlink(missing_ok=True)'''),
    md("## 누적 상태 그래프 준비\n\n질문과 답변 목록에 `operator.add` 리듀서를 적용합니다."),
    code('''class State(TypedDict):
    turns: Annotated[list[str], operator.add]

def respond(state: State) -> dict:
    return {"turns": [f"답변 {len(state['turns'])}"]}

builder = StateGraph(State)
builder.add_node("respond", respond)
builder.add_edge(START, "respond")
builder.add_edge("respond", END)'''),
    md("## 첫 프로그램 실행\n\n첫 연결을 닫기 전에 체크포인트가 파일에 기록됐는지 확인합니다."),
    code('''config = {"configurable": {"thread_id": "conversation-23"}}
with sqlite3.connect(db_path, check_same_thread=False) as conn:
    graph_first = builder.compile(checkpointer=SqliteSaver(conn))
    first = graph_first.invoke({"turns": ["질문 1"]}, config, durability="sync")
print("first process:", first["turns"])
print("database bytes:", db_path.stat().st_size)'''),
    md("## 새 프로그램 객체에서 재개\n\n새 연결과 새 그래프 객체를 만들고 같은 스레드에 질문을 추가합니다."),
    code('''with sqlite3.connect(db_path, check_same_thread=False) as conn:
    graph_second = builder.compile(checkpointer=SqliteSaver(conn))
    resumed = graph_second.invoke({"turns": ["질문 2"]}, config, durability="sync")
    saved = graph_second.get_state(config)
print("second process:", resumed["turns"])
print("saved next:", saved.next)
assert resumed["turns"] == ["질문 1", "답변 1", "질문 2", "답변 3"]'''),
])

NOTEBOOKS["ch23-persistence/04-내구-실행-모드-비교"] = notebook(
    "내구 실행 모드 비교", "같은 지점에서 자식 프로세스를 종료했을 때 exit, async, sync가 남기는 체크포인트를 비교합니다.", "experiment", [
    md("## 실험 함수 준비\n\n자식 프로세스가 두 번째 노드에 진입하면 즉시 종료하고 SQLite 체크포인트를 직접 읽습니다."),
    code('''import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver

candidates = [Path.cwd(), *Path.cwd().parents]
lab = next((p / "labs/part6/ch23-persistence" for p in candidates if (p / "labs/part6/ch23-persistence").is_dir()), None)
if lab is None:
    lab = next(p for p in candidates if p.name == "ch23-persistence")
worker = lab / "durability_worker.py"
run_dir = lab / "data" / "durability"
run_dir.mkdir(parents=True, exist_ok=True)'''),
    md("## 체크포인트 읽기 함수\n\n자식 프로세스가 종료된 뒤 같은 스레드의 최신 저장 상태를 읽습니다."),
    code('''def read_saved(db_path: Path, mode: str) -> dict | None:
    if not db_path.exists():
        return None
    with sqlite3.connect(db_path, check_same_thread=False) as conn:
        saved = SqliteSaver(conn).get_tuple({"configurable": {"thread_id": mode}})
    return None if saved is None else saved.checkpoint.get("channel_values", {})'''),
    md("## 중단 뒤 재개 함수\n\nready 파일은 두 번째 노드 진입 신호이고 deadline은 20초 대기 상한입니다."),
    code('''def kill_and_resume(mode: str) -> dict:
    db_path = run_dir / f"{mode}.sqlite"
    ready = run_dir / f"{mode}.ready"
    trace = ready.with_suffix(".trace")
    for path in [db_path, ready, trace]:
        path.unlink(missing_ok=True)
    process = subprocess.Popen([sys.executable, str(worker), str(db_path), str(ready), mode])
    deadline = time.time() + 20
    while not ready.exists() and time.time() < deadline:
        time.sleep(0.02)
    assert ready.exists(), f"{mode} worker did not enter second node"
    process.kill()
    process.wait(timeout=5)
    before = read_saved(db_path, mode)
    subprocess.run([sys.executable, str(worker), str(db_path), str(ready), mode, "resume"], check=True, timeout=20)
    after = read_saved(db_path, mode)
    calls = trace.read_text(encoding="utf-8").splitlines()
    return {"mode": mode, "before": before, "after": after, "calls": calls}'''),
    md("## 같은 중단 시점에서 세 모드 실행\n\n실행 모드 외의 그래프, 입력, 종료 시점을 고정합니다."),
    code('''observations = [kill_and_resume(mode) for mode in ["exit", "async", "sync"]]
for row in observations:
    print(row)
assert observations[0]["before"] is None
assert "first" in observations[2]["before"].get("completed", [])
assert all(row["after"].get("completed") == ["first", "second"] for row in observations)'''),
    md("## 손실 범위 요약\n\n저장된 `completed`와 노드 호출 횟수를 함께 표시합니다."),
    code('''for row in observations:
    before = None if row["before"] is None else row["before"].get("completed")
    print(f"{row['mode']:5} -> before={before}, after={row['after'].get('completed')}, calls={row['calls']}")
print("async는 저장 작업과 종료 시점의 경합에 따라 이번 관찰값과 달라질 수 있습니다.")'''),
])

NOTEBOOKS["ch23-persistence/05-pending-writes와-장애-복구"] = notebook(
    "pending writes와 장애 복구", "같은 단계의 한 노드가 실패해도 성공한 병렬 노드가 다시 실행되지 않는지 확인합니다.", "experiment", [
    md("## 병렬 그래프 준비\n\n`good`과 `flaky`를 같은 단계에 놓고 로컬 로그로 호출 횟수를 셉니다."),
    code('''from pathlib import Path
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

candidates = [Path.cwd(), *Path.cwd().parents]
lab = next((p / "labs/part6/ch23-persistence" for p in candidates if (p / "labs/part6/ch23-persistence").is_dir()), None)
if lab is None:
    lab = next(p for p in candidates if p.name == "ch23-persistence")
trace_path = lab / "data/pending-trace.txt"
allow_path = lab / "data/allow-flaky"
trace_path.parent.mkdir(parents=True, exist_ok=True)
trace_path.unlink(missing_ok=True)
allow_path.unlink(missing_ok=True)

class State(TypedDict):
    results: Annotated[list[str], lambda left, right: left + right]'''),
    md("## 병렬 노드와 실행 경로\n\n두 노드는 호출 이름을 기록하고 `flaky`만 첫 실행에서 실패합니다."),
    code('''def record(name: str) -> None:
    with trace_path.open("a", encoding="utf-8") as stream:
        stream.write(name + "\\n")

def good(state: State) -> dict:
    record("good")
    return {"results": ["good-result"]}

def flaky(state: State) -> dict:
    record("flaky")
    if not allow_path.exists():
        raise RuntimeError("temporary failure")
    return {"results": ["flaky-result"]}

builder = StateGraph(State)
builder.add_node("good", good)
builder.add_node("flaky", flaky)
builder.add_edge(START, "good")
builder.add_edge(START, "flaky")
builder.add_edge("good", END)
builder.add_edge("flaky", END)
graph = builder.compile(checkpointer=InMemorySaver())'''),
    md("## 첫 실행의 부분 성공\n\n오류가 발생한 뒤 저장된 pending write와 호출 로그를 읽습니다."),
    code('''config = {"configurable": {"thread_id": "pending-23"}}
try:
    graph.invoke({"results": []}, config)
except RuntimeError as exc:
    print(type(exc).__name__, str(exc))
before_lines = trace_path.read_text(encoding="utf-8").splitlines()
snapshot = graph.get_state(config)
print("calls before resume:", before_lines)
print("tasks:", [(task.name, bool(task.error), len(task.result or [])) for task in snapshot.tasks])'''),
    md("## 실패 원인을 없애고 재개\n\n입력을 다시 넣지 않고 `None`으로 재개합니다."),
    code('''allow_path.write_text("ok", encoding="utf-8")
resumed = graph.invoke(None, config)
after_lines = trace_path.read_text(encoding="utf-8").splitlines()
print("calls after resume:", after_lines)
print("results:", sorted(resumed["results"]))
assert after_lines.count("good") == 1
assert after_lines.count("flaky") == 2
assert sorted(resumed["results"]) == ["flaky-result", "good-result"]'''),
])

NOTEBOOKS["ch23-persistence/06-노드-재시작과-멱등성"] = notebook(
    "노드 재시작과 멱등성", "부작용 뒤에 프로세스가 종료된 노드를 재개할 때 멱등 키가 중복 기록을 막는지 확인합니다.", "paired", [
    md("## 실제 중단과 재개 함수\n\n작업 파일에 주문 번호를 기록한 직후 자식 프로세스를 종료합니다."),
    code('''import subprocess
import sys
import time
from pathlib import Path

candidates = [Path.cwd(), *Path.cwd().parents]
lab = next((p / "labs/part6/ch23-persistence" for p in candidates if (p / "labs/part6/ch23-persistence").is_dir()), None)
if lab is None:
    lab = next(p for p in candidates if p.name == "ch23-persistence")
worker = lab / "idempotency_worker.py"
run_dir = lab / "data" / "idempotency"
run_dir.mkdir(parents=True, exist_ok=True)'''),
    md("## 중단과 재개 함수\n\n같은 SQLite 체크포인트와 전략 이름으로 새 프로세스를 실행합니다."),
    code('''def interrupt_then_resume(strategy: str) -> list[str]:
    db = run_dir / f"{strategy}.sqlite"
    log = run_dir / f"{strategy}.log"
    ready = run_dir / f"{strategy}.ready"
    for path in [db, log, ready]:
        path.unlink(missing_ok=True)
    first = subprocess.Popen([sys.executable, str(worker), str(db), str(log), str(ready), strategy, "first"])
    deadline = time.time() + 20
    while not ready.exists() and time.time() < deadline:
        time.sleep(0.02)
    assert ready.exists()
    first.kill()
    first.wait(timeout=5)
    second = subprocess.run(
        [sys.executable, str(worker), str(db), str(log), str(ready), strategy, "resume"],
        check=True, capture_output=True, text=True, timeout=20,
    )
    return log.read_text(encoding="utf-8").splitlines()'''),
    md("## Before: 멱등 키를 검사하지 않는 쓰기", "before"),
    code('''naive_lines = interrupt_then_resume("naive")
print("naive log:", naive_lines)
print("same operation count:", naive_lines.count("order-2306"))
assert naive_lines.count("order-2306") == 2''', "before"),
    md("## After: operation_id로 중복 쓰기 차단", "after"),
    code('''idempotent_lines = interrupt_then_resume("idempotent")
print("idempotent log:", idempotent_lines)
print("same operation count:", idempotent_lines.count("order-2306"))
assert idempotent_lines.count("order-2306") == 1''', "after"),
])

NOTEBOOKS["ch24-human-in-the-loop/01-interrupt-승인-게이트"] = notebook(
    "interrupt 승인 게이트", "로컬 쓰기 전에 승인 여부를 확인해야 거절된 작업이 실행되지 않는지 확인합니다.", "paired", [
    md("## 승인 대상과 기록 파일 준비\n\n되돌릴 수 없는 동작을 대신해 로컬 파일 기록을 사용합니다."),
    code('''from pathlib import Path
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

candidates = [Path.cwd(), *Path.cwd().parents]
lab = next((p / "labs/part6/ch24-human-in-the-loop" for p in candidates if (p / "labs/part6/ch24-human-in-the-loop").is_dir()), None)
if lab is None:
    lab = next(p for p in candidates if p.name == "ch24-human-in-the-loop")
effect_path = lab / "approval-effects.txt"
effect_path.unlink(missing_ok=True)

class State(TypedDict):
    request: str
    status: str

def write_effect(request: str) -> None:
    with effect_path.open("a", encoding="utf-8") as stream:
        stream.write(request + "\\n")'''),
    md("## Before: 부작용 뒤에 승인 요청", "before"),
    code('''def unsafe_node(state: State) -> dict:
    write_effect(state["request"])
    approved = interrupt({"request": state["request"], "question": "승인합니까?"})
    return {"status": "approved" if approved else "rejected"}

unsafe_builder = StateGraph(State)
unsafe_builder.add_node("gate", unsafe_node)
unsafe_builder.add_edge(START, "gate")
unsafe_builder.add_edge("gate", END)
unsafe = unsafe_builder.compile(checkpointer=InMemorySaver())
unsafe_config = {"configurable": {"thread_id": "unsafe"}}
paused = unsafe.invoke({"request": "transfer-local", "status": "new"}, unsafe_config)
rejected = unsafe.invoke(Command(resume=False), unsafe_config)
print("status:", rejected["status"])
print("writes despite rejection:", effect_path.read_text(encoding="utf-8").splitlines())''', "before"),
    md("## After: 승인 뒤에만 부작용 실행", "after"),
    code('''effect_path.unlink(missing_ok=True)
def safe_node(state: State) -> dict:
    approved = interrupt({"request": state["request"], "question": "승인합니까?"})
    if not approved:
        return {"status": "rejected"}
    write_effect(state["request"])
    return {"status": "approved"}

safe_builder = StateGraph(State)
safe_builder.add_node("gate", safe_node)
safe_builder.add_edge(START, "gate")
safe_builder.add_edge("gate", END)
safe = safe_builder.compile(checkpointer=InMemorySaver())
safe_config = {"configurable": {"thread_id": "safe"}}
safe.invoke({"request": "transfer-local", "status": "new"}, safe_config)
rejected = safe.invoke(Command(resume=False), safe_config)
print("status:", rejected["status"])
print("effect file exists:", effect_path.exists())
assert rejected["status"] == "rejected" and not effect_path.exists()''', "after"),
])

NOTEBOOKS["ch24-human-in-the-loop/02-Command-resume으로-실행-재개"] = notebook(
    "Command(resume=)으로 실행 재개", "잘못된 승인 입력을 다시 요청하고 올바른 값으로 같은 스레드를 완료하는 과정을 확인합니다.", "experiment", [
    md("## 입력 검증 노드 준비\n\n`interrupt()`를 반복문 안에 두고 허용할 문자열을 제한합니다."),
    code('''from typing_extensions import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

class State(TypedDict):
    request: str
    decision: str

def review(state: State) -> dict:
    prompt = {"request": state["request"], "allowed": ["approve", "reject"]}
    while True:
        decision = interrupt(prompt)
        if decision in {"approve", "reject"}:
            return {"decision": decision}
        prompt = {**prompt, "error": f"허용하지 않는 값: {decision}"}

builder = StateGraph(State)
builder.add_node("review", review)
builder.add_edge(START, "review")
builder.add_edge("review", END)
graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "review-2402"}}'''),
    md("## 처음 중단하고 잘못된 값 전달\n\n각 호출 뒤 `__interrupt__`에 담긴 질문을 확인합니다."),
    code('''first = graph.invoke({"request": "publish-local", "decision": ""}, config)
second = graph.invoke(Command(resume="maybe"), config)
print("first prompt:", first["__interrupt__"][0].value)
print("second prompt:", second["__interrupt__"][0].value)
assert "error" in second["__interrupt__"][0].value'''),
    md("## 올바른 값으로 완료\n\n같은 `thread_id`에 `Command(resume=...)`을 전달합니다."),
    code('''final = graph.invoke(Command(resume="approve"), config)
snapshot = graph.get_state(config)
print("final:", final)
print("next:", snapshot.next)
print("history count:", len(list(graph.get_state_history(config))))
assert final["decision"] == "approve" and snapshot.next == ()'''),
])

NOTEBOOKS["ch24-human-in-the-loop/03-상태-기록과-다른-분기-재실행"] = notebook(
    "상태 기록과 다른 분기 재실행", "완료된 실행의 중간 체크포인트에서 값을 바꾸어 원본을 보존한 새 분기를 만들 수 있는지 확인합니다.", "experiment", [
    md("## 가격 계산 그래프 준비\n\n가격 확정 뒤 할인율을 적용하는 두 노드로 분기 지점을 만듭니다."),
    code('''from typing_extensions import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

class State(TypedDict):
    base_price: int
    rate: float
    final_price: int
    trace: list[str]

def quote(state: State) -> dict:
    return {"trace": state["trace"] + ["quote"]}

def discount(state: State) -> dict:
    return {
        "final_price": int(state["base_price"] * (1 - state["rate"])),
        "trace": state["trace"] + [f"discount:{state['rate']}"]
    }'''),
    md("## 그래프 컴파일\n\n두 노드를 순서대로 연결하고 메모리 체크포인터를 붙입니다."),
    code('''builder = StateGraph(State)
builder.add_node("quote", quote)
builder.add_node("discount", discount)
builder.add_edge(START, "quote")
builder.add_edge("quote", "discount")
builder.add_edge("discount", END)
graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "price-2403"}}'''),
    md("## 원본 실행과 기록 조회\n\n`next`가 `discount`인 상태를 분기 기준으로 고릅니다."),
    code('''original = graph.invoke(
    {"base_price": 10_000, "rate": 0.1, "final_price": 0, "trace": []}, config
)
history = list(graph.get_state_history(config))
before_discount = next(item for item in history if item.next == ("discount",))
original_final_config = graph.get_state(config).config
print("original:", original)
print("history:", [(item.metadata.get("step"), item.next) for item in reversed(history)])
assert original["final_price"] == 9000'''),
    md("## 할인율을 바꾼 분기 실행\n\n선택한 체크포인트의 상태를 갱신한 뒤 `None`으로 이어서 실행합니다."),
    code('''fork_config = graph.update_state(before_discount.config, {"rate": 0.2})
forked = graph.invoke(None, fork_config)
original_saved = graph.get_state(original_final_config)
fork_saved = graph.get_state(fork_config)
print("original final:", original_saved.values["final_price"])
print("fork final:", forked["final_price"])
print("fork trace:", forked["trace"])
print("checkpoint ids differ:", original_saved.config != fork_saved.config)
assert original_saved.values["final_price"] == 9000
assert forked["final_price"] == 8000'''),
])

def section_html(chapter: str, slug: str, title: str, fmt: str, why: str, concept: str, observation: str, next_text: str, terms: list[str]) -> str:
    detail = LESSON_DETAILS[f"{chapter}/{slug}"]
    lab_hours = LAB_HOURS[f"{chapter}/{slug}"]
    failure_title = "일부러 실패해 보기" if fmt == "paired" else "실험 결과 해석"
    token = f"{{{{notebook:{slug}|example}}}}" if fmt == "paired" else f"{{{{notebook:{slug}}}}}"
    failure_token = f"{{{{notebook:{slug}|failure}}}}" if fmt == "paired" else ""
    refs = """<ul><li><a href=\"https://docs.langchain.com/oss/python/langgraph/persistence\">LangGraph Persistence 공식 문서</a> · 확인 2026-09-11 · LangGraph 1.2.11</li><li><a href=\"https://docs.langchain.com/oss/python/langgraph/interrupts\">LangGraph Interrupts 공식 문서</a> · 확인 2026-09-11 · LangGraph 1.2.11</li><li><a href=\"https://docs.langchain.com/oss/python/langgraph/use-time-travel\">LangGraph Time Travel 공식 문서</a> · 확인 2026-09-11 · LangGraph 1.2.11</li><li><a href=\"https://github.com/langchain-ai/langgraph/blob/main/LICENSE\">LangGraph MIT 라이선스</a> · 확인 2026-09-11</li></ul>"""
    quiz = detail["quiz"]
    quiz_html = "".join(f'<details class="quiz"><summary>{i}. {q}</summary><p class="quiz-a"><b>해설</b> — {a}</p></details>' for i, (q, a) in enumerate(quiz, 1))
    return f'''<!--meta: 강의 1h · 실습 {lab_hours}h | 코드 Jupyter Notebook | 새 용어 {len(terms)} -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul><li>{terms[0]}가 저장하거나 제어하는 대상을 설명할 수 있습니다.</li><li>노트북의 실제 상태와 실행 기록을 읽을 수 있습니다.</li><li>장애 또는 사람의 입력 뒤에 실행할 안전한 재개 방법을 고를 수 있습니다.</li></ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>{why}</p><p>상태가 있다는 사실만으로 실행이 안전하게 이어지지는 않습니다. 언제 저장됐는지, 어떤 식별자로 다시 찾는지, 이미 실행된 부작용이 있는지를 함께 확인해야 합니다. 이번 절은 이 세 질문을 코드와 실제 출력으로 연결합니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>{detail["prior"]}</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>구체적인 상황</h3><p>{detail["situation"]}</p><h3>정의</h3><p>{concept}</p><p>{detail["definition"]}</p><h3>도식 읽기</h3>{{{{svg:{slug.split('-', 1)[0]}-흐름}}}}<p>{detail["figure"]}</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>{detail["walk"]}</p>{token}<p class="look"><b>확인할 점</b> — {observation}</p>
<h2 id="b6"><span class="no">6</span>{failure_title}</h2>{failure_token}<p>{detail["analysis"]}</p><p>{observation}</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul>{''.join(f'<li>{item}</li>' for item in detail["cautions"])}</ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>{terms[0]}의 역할을 실제 상태와 출력으로 확인했습니다.</li><li>재개는 저장된 상태와 다음 노드 정보를 함께 사용합니다.</li><li>외부 부작용은 그래프 상태와 별도의 중복 방지 설계가 필요합니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — {next_text}</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>{quiz_html}
<h2 id="b10"><span class="no">10</span>참고 자료</h2>{refs}
'''

LAB_HOURS = {
    "ch23-persistence/01-체크포인터와-스레드": "1.5",
    "ch23-persistence/02-PostgresSaver-준비와-스키마": "1.5",
    "ch23-persistence/03-스레드-재개와-대화-이어가기": "1.5",
    "ch23-persistence/04-내구-실행-모드-비교": "2",
    "ch23-persistence/05-pending-writes와-장애-복구": "1.5",
    "ch23-persistence/06-노드-재시작과-멱등성": "2",
    "ch24-human-in-the-loop/01-interrupt-승인-게이트": "1.5",
    "ch24-human-in-the-loop/02-Command-resume으로-실행-재개": "1.5",
    "ch24-human-in-the-loop/03-상태-기록과-다른-분기-재실행": "2",
}

LESSON_DETAILS = {
    "ch23-persistence/01-체크포인터와-스레드": {
        "prior": "Ch13의 StateGraph는 한 번의 invoke 안에서 State를 노드 사이에 전달했습니다. Ch20의 도구 반복도 같은 실행 안에서 메시지를 누적했습니다. 이번 절에서는 실행이 끝난 뒤에도 값을 찾을 수 있도록 compile(checkpointer=memory)를 사용하고, config의 configurable.thread_id가 어느 기록을 읽을지 지정합니다.",
        "situation": "상담 시스템에서 customer-a가 앞서 입력한 3에 이어 4를 보내면 합계는 7이어야 합니다. 같은 시각 customer-b가 4를 보내도 customer-a의 3이 섞이면 안 됩니다. 체크포인트는 계산 결과를 남기고 스레드는 두 고객의 기록 경계를 만듭니다.",
        "definition": "StateSnapshot의 values는 그 시점의 채널 값이고 next는 다음에 실행할 노드 이름입니다. 실행을 마친 스냅샷에서 next가 빈 튜플이면 이어서 실행할 노드가 없다는 뜻입니다. get_state_history()는 입력, 노드 실행, 종료 뒤에 만들어진 스냅샷을 최신순으로 반환합니다.",
        "figure": "도식의 ‘입력 + thread_id’에서 시작해 ‘체크포인트 저장’을 거칩니다. customer-a는 ‘같은 스레드 재개’로 이동하고 customer-b는 ‘다른 스레드 격리’로 이동합니다. 노트북의 total 7과 total 4가 두 경로의 결과입니다.",
        "walk": "첫 셀은 total과 events를 가진 State와 add 노드를 정의하고 InMemorySaver를 붙입니다. customer-a 설정으로 3을 실행한 뒤 같은 설정에 4를 입력합니다. 마지막 셀은 입력 4를 유지한 채 thread_id만 customer-b로 바꾸어 누적값과 기록 수를 비교합니다.",
        "analysis": "customer-a의 첫 결과는 3, 두 번째 결과는 7이며 저장된 최신 values의 total도 7입니다. customer-b는 4에서 시작합니다. 기록 수가 각각 6과 3인 것은 customer-a가 두 번, customer-b가 한 번 실행됐기 때문입니다. 기록 수 자체를 대화 턴 수로 해석하지 않습니다.",
        "cautions": ["InMemorySaver의 내용은 Python 프로세스가 끝나면 사라집니다.", "thread_id를 사용자 입력에서 그대로 받기보다 인증된 사용자와 대화 식별자에서 서버가 생성합니다.", "체크포인트 상태에는 비밀 키와 불필요한 개인정보를 넣지 않습니다."],
        "quiz": [("customer-a의 두 번째 total이 7인 이유는 무엇인가요?", "같은 thread_id의 최신 체크포인트 total 3을 읽고 새 입력 4를 더했기 때문입니다."), ("customer-b의 total이 4인 결과가 보여 주는 것은 무엇인가요?", "다른 thread_id는 customer-a의 저장 상태를 읽지 않는다는 것을 보여 줍니다."), ("StateSnapshot.next가 빈 튜플이라는 뜻은 무엇인가요?", "현재 실행에서 이어서 실행할 노드가 없다는 뜻입니다."), ("InMemorySaver를 운영 재개 저장소로 쓰기 어려운 이유는 무엇인가요?", "프로세스가 종료되면 메모리의 체크포인트도 사라지기 때문입니다.")],
    },
    "ch23-persistence/02-PostgresSaver-준비와-스키마": {
        "prior": "Ch4에서 PostgreSQL 스키마와 information_schema.tables를 조회했습니다. 앞 절에서는 같은 thread_id가 메모리 체크포인트를 찾는 과정을 확인했습니다. 이번 절은 그 저장 위치를 ch23_lab 스키마로 옮기고, Ch4의 표 조회로 실제 생성 결과를 확인합니다.",
        "situation": "서버가 재시작된 뒤에도 주문 처리 위치를 찾으려면 체크포인트가 애플리케이션 메모리 밖에 있어야 합니다. PostgreSQL은 여러 프로세스가 같은 저장소를 사용할 수 있지만, PostgresSaver가 사용할 표를 먼저 준비해야 합니다.",
        "definition": "PostgresSaver.from_conn_string()은 autocommit과 dict_row를 갖춘 연결을 준비합니다. setup()은 checkpoint_migrations, checkpoints, checkpoint_blobs, checkpoint_writes 표를 생성하거나 필요한 마이그레이션을 적용합니다. 새 배포 환경에서 한 번 실행하고 일반 요청마다 반복하지 않습니다.",
        "figure": "‘PostgreSQL 연결’ 다음의 ‘PostgresSaver.setup’ 상자가 준비 단계입니다. 그 결과 ‘체크포인트 표’가 생겨야 ‘그래프 실행 저장’이 성공합니다. Before의 UndefinedTable은 두 번째 상자를 건너뛴 경로이고, After의 네 표 목록은 정상 경로입니다.",
        "walk": "로컬 postgres:17 컨테이너의 ch23_lab 스키마를 비우고 value를 두 배로 만드는 그래프를 정의합니다. Before는 setup 없이 thread_id before를 실행해 실제 UndefinedTable을 수집합니다. After는 setup을 호출한 뒤 thread_id after를 실행하고 information_schema에서 표 이름을 읽습니다.",
        "analysis": "Before의 오류는 학생이 만든 검사 함수가 아니라 PostgreSQL이 존재하지 않는 checkpoints 관계를 조회하며 반환한 오류입니다. After의 value는 6에서 12가 됐고 checkpoints와 checkpoint_writes가 모두 확인됐습니다. 계산 성공과 저장 스키마 준비를 서로 다른 출력으로 검증한 셈입니다.",
        "cautions": ["실습 URI의 postgres/postgres 계정은 로컬 컨테이너 전용이며 운영 자격 증명으로 사용하지 않습니다.", "수동 psycopg 연결을 넘길 때는 autocommit=True와 row_factory=dict_row 요구를 공식 README에서 다시 확인합니다.", "setup을 명시적 트랜잭션 안에서 호출하지 않습니다. 일부 마이그레이션은 CREATE INDEX CONCURRENTLY를 사용합니다."],
        "quiz": [("setup 전 실행에서 발생한 데이터베이스 오류는 무엇인가요?", "checkpoints 표가 없어서 PostgreSQL의 UndefinedTable이 발생했습니다."), ("checkpoint_writes 표는 어떤 정보를 저장하나요?", "완전한 다음 체크포인트 전의 중간 쓰기와 pending writes를 저장합니다."), ("information_schema.tables를 조회한 이유는 무엇인가요?", "setup이 실제 PostgreSQL 스키마에 표를 만들었는지 확인하기 위해서입니다."), ("setup을 일반 요청마다 호출하지 않는 이유는 무엇인가요?", "배포 준비 단계의 스키마 마이그레이션이며 매 요청의 그래프 실행과 역할이 다르기 때문입니다.")],
    },
    "ch23-persistence/03-스레드-재개와-대화-이어가기": {
        "prior": "앞 절에서 PostgresSaver가 프로세스 밖의 데이터베이스에 체크포인트를 남기는 구조를 확인했습니다. 이번 절은 설치 부담을 줄이기 위해 SQLiteSaver를 사용하지만, 첫 연결을 닫고 새 연결과 새 그래프 객체를 만드는 방식으로 프로세스 경계를 모사합니다.",
        "situation": "사용자가 질문 1을 보낸 요청과 질문 2를 보낸 요청은 서로 다른 웹 요청에서 처리될 수 있습니다. 두 번째 요청의 코드가 첫 번째 graph 변수를 참조하지 않아도 저장 파일과 thread_id가 같으면 앞선 턴을 불러올 수 있어야 합니다.",
        "definition": "turns 채널에는 operator.add 리듀서를 지정합니다. 새 입력 목록과 노드가 반환한 목록을 기존 목록 뒤에 더하므로 질문과 답변 순서가 보존됩니다. 리듀서가 없으면 새 turns 값이 이전 목록을 덮어씁니다. 첫 번째 연결을 닫는 것은 graph_first라는 Python 객체를 더 이상 사용할 수 없게 만드는 과정입니다. 두 번째 연결은 SQLite 파일에 저장된 채널 값과 다음 노드 정보만으로 실행을 구성합니다.",
        "figure": "‘프로세스 1 실행’이 data/thread-resume.sqlite의 ‘SQLite 체크포인트’를 만듭니다. 연결을 닫는 ‘프로세스 1 종료’ 뒤 ‘프로세스 2 재개’가 같은 파일과 conversation-23을 사용합니다. 출력의 네 항목 목록이 이 경로를 확인합니다.",
        "walk": "실습 폴더를 현재 노트북 위치와 상위 폴더에서 찾아 절대 개인 경로를 사용하지 않습니다. 첫 with 블록에서 질문 1을 동기 저장한 뒤 연결을 닫습니다. 두 번째 with 블록은 새 SqliteSaver와 새 graph_second를 만들고 같은 config에 질문 2를 넣습니다.",
        "analysis": "두 번째 결과는 질문 1, 답변 1, 질문 2, 답변 3 순서입니다. 답변 번호 3은 응답 노드가 실행되기 전 상태에 세 항목이 있다는 뜻입니다. saved.next가 빈 튜플이므로 두 번째 호출도 끝까지 완료됐습니다.",
        "cautions": ["SQLite는 이 실습과 단일 프로세스 개발에 알맞지만 다중 서버 운영의 동시성 요구는 별도로 검토합니다.", "새 대화를 시작할 때는 이전 thread_id를 재사용하지 않습니다.", "메시지 목록이 계속 커지면 요약이나 보존 기간 정책을 별도로 설계합니다."],
        "quiz": [("두 번째 실행이 첫 번째 Python graph 객체 없이도 이어진 근거는 무엇인가요?", "같은 SQLite 파일과 thread_id에서 최신 체크포인트를 읽었기 때문입니다."), ("turns에 operator.add가 필요한 이유는 무엇인가요?", "새 질문과 답변을 이전 목록 뒤에 추가하기 위해서입니다."), ("db_path를 상위 폴더에서 찾는 코드는 무엇을 해결하나요?", "프로젝트 루트와 노트북 폴더 어느 위치에서 실행해도 제공 파일을 찾게 합니다."), ("질문 2에 새 thread_id를 쓰면 어떤 결과가 예상되나요?", "질문 1과 답변 1이 없는 새 상태에서 시작합니다.")],
    },
    "ch23-persistence/04-내구-실행-모드-비교": {
        "prior": "앞 절은 정상 종료한 두 프로세스 사이의 재개를 확인했습니다. 이제 정상 종료라는 조건을 없앱니다. SQLiteSaver와 같은 thread_id는 유지하고, 두 번째 노드에 들어간 자식 프로세스를 운영체제 수준에서 종료해 durability 인자만 비교합니다.",
        "situation": "first 노드가 분류를 마치고 second 노드가 긴 외부 처리를 시작한 순간 서버가 종료됐다고 가정합니다. 복구 뒤 first를 다시 실행해야 하는지, second부터 시작할 수 있는지는 first 결과가 종료 전에 저장됐는지에 달려 있습니다.",
        "definition": "sync는 first 체크포인트 저장이 완료된 뒤 second를 시작합니다. async는 저장과 second 실행을 겹치므로 지연을 줄일 수 있지만 매우 이른 종료에서는 저장 완료 여부가 달라질 수 있습니다. exit는 그래프가 끝날 때만 저장하므로 중간 종료에서 완료된 노드 결과가 남지 않습니다.",
        "figure": "‘노드 1 완료’에서 세 경로로 갈라집니다. sync 상자는 저장 뒤 이동, async 상자는 저장과 이동의 겹침, exit 상자는 종료 시 저장을 뜻합니다. 실제 calls에서 exit만 first가 두 번 나타나며 두 체크포인트 모드는 second만 다시 실행합니다.",
        "walk": "durability_worker.py는 first와 second 이름을 trace에 기록합니다. second 진입 직후 ready 파일을 만들고 30초 기다립니다. 부모 셀은 ready를 확인하면 kill()로 프로세스를 종료하고 get_tuple로 중단 상태를 읽은 다음 새 자식 프로세스에서 같은 스레드를 실제 재개합니다.",
        "analysis": "exit의 before는 None이고 재개 과정은 입력부터 다시 시작해 calls가 first, second, first, second입니다. 이번 실행의 async와 sync에는 completed=['first']가 남아 calls가 first, second, second였습니다. 세 모드 모두 재개 뒤 completed=['first','second']로 끝났습니다. async 결과는 저장 장치와 kill 시점이 달라지면 sync와 다를 수 있습니다.",
        "cautions": ["kill 직전 ready 파일은 second 함수에 진입했다는 신호이며 second가 상태를 반환했다는 뜻이 아닙니다.", "async 한 번의 관찰로 모든 장애 시점에 first가 보존된다고 단정하지 않습니다.", "복구 범위를 줄여도 노드 내부 부작용의 정확히 한 번 실행을 보장하지 않습니다."],
        "quiz": [("exit 재개에서 first가 다시 실행된 근거는 무엇인가요?", "before가 None이고 calls에 first가 두 번 기록됐습니다."), ("sync 재개가 second부터 시작한 근거는 무엇인가요?", "중단 전 completed에 first가 있고 calls에서 first는 한 번, second는 두 번입니다."), ("ready 파일은 무엇을 증명하나요?", "자식 프로세스가 second 노드 함수에 진입했음을 증명합니다."), ("async의 결과를 반복 측정해야 하는 이유는 무엇인가요?", "체크포인트 저장과 다음 노드가 겹치므로 프로세스 종료 시점과 저장 속도에 따라 결과가 달라질 수 있습니다.")],
    },
    "ch23-persistence/05-pending-writes와-장애-복구": {
        "prior": "앞 절에서는 순차 노드의 경계에서 저장 모드를 비교했습니다. 이번 절은 START에서 good과 flaky가 동시에 시작하는 같은 superstep을 사용합니다. 하나가 성공하고 하나가 실패한 부분 완료 상태가 재개에 어떤 영향을 주는지 살펴봅니다.",
        "situation": "같은 단계에서 문서 저장은 성공했지만 알림 전송은 일시 오류로 실패했다고 가정합니다. 전체 단계를 반복하면 문서 저장이 두 번 실행될 수 있습니다. 성공한 작업의 반환값을 중간 쓰기로 보존하면 실패한 알림만 다시 시도할 수 있습니다.",
        "definition": "checkpoint_writes 계열의 pending writes는 superstep이 완전히 끝나기 전에 각 task가 반환한 쓰기를 보존합니다. StateSnapshot.tasks에는 성공한 good의 result와 실패한 flaky의 error가 함께 나타납니다. 재개 입력으로 None을 전달하면 새 실행을 시작하지 않고 이 미완료 단계에서 이어 갑니다.",
        "figure": "도식의 첫 상자에서 good과 flaky가 같은 단계로 실행됩니다. good은 ‘pending write’에 도달하고 flaky는 실패합니다. 마지막 ‘재개: flaky만 재실행’ 경로는 calls after resume의 good 1회, flaky 2회와 대응합니다.",
        "walk": "trace_path는 실제 함수 호출 이름을 한 줄씩 기록합니다. allow_path가 없을 때 flaky는 RuntimeError를 냅니다. 오류를 받은 뒤 snapshot.tasks를 읽고, allow_path를 만든 다음 graph.invoke(None, config)으로 같은 superstep을 재개합니다.",
        "analysis": "첫 호출 로그는 good, flaky이며 tasks에는 good의 한 결과와 flaky의 오류가 보입니다. 재개 뒤 로그에는 flaky만 한 번 추가됩니다. 최종 results에 good-result와 flaky-result가 모두 있으므로 성공한 중간 쓰기는 보존되고 실패한 task만 다시 실행됐습니다.",
        "cautions": ["pending writes는 같은 superstep에서 런타임이 받은 상태 쓰기를 보존하며 외부 시스템의 부작용을 되돌리지 않습니다.", "병렬 노드가 같은 키를 쓰면 리듀서 또는 충돌 처리 규칙이 필요합니다.", "실패 원인이 계속 남아 있으면 재개도 다시 실패하므로 재시도 한도와 운영 알림을 둡니다."],
        "quiz": [("재개 뒤 good이 다시 실행되지 않은 증거는 무엇인가요?", "trace에서 good은 전체 1회이고 flaky만 2회입니다."), ("StateSnapshot.tasks에서 확인한 두 항목의 차이는 무엇인가요?", "good에는 result가 있고 flaky에는 RuntimeError가 있습니다."), ("invoke(None, config)의 None은 무엇을 뜻하나요?", "새 입력을 추가하지 않고 저장된 미완료 실행에서 이어 간다는 뜻입니다."), ("pending writes가 외부 결제 중복까지 막아 주나요?", "막아 주지 않습니다. 외부 쓰기는 별도의 멱등 키가 필요합니다.")],
    },
    "ch23-persistence/06-노드-재시작과-멱등성": {
        "prior": "앞 절의 good 노드는 상태 반환까지 마쳐 pending write가 생겼습니다. 이번 절은 외부 파일에 주문 번호를 쓴 뒤 상태를 반환하기 전에 프로세스를 종료합니다. 체크포인트가 다음 노드 경계로 이동하지 못했으므로 같은 charge 노드가 처음부터 다시 시작됩니다.",
        "situation": "결제 요청이 외부 서비스에는 반영됐지만 응답을 상태에 저장하기 전에 서버가 종료될 수 있습니다. 재개한 charge가 같은 요청을 다시 보내면 이중 결제가 됩니다. 호출마다 바뀌지 않는 주문 작업 키로 이미 처리했는지 확인해야 합니다.",
        "definition": "operation_id는 비즈니스 작업 한 건을 식별합니다. naive 전략은 호출할 때마다 로그에 추가합니다. idempotent 전략은 같은 operation_id가 이미 있으면 추가하지 않습니다. 이 실습의 파일 검사는 실제 운영에서 데이터베이스의 고유 키나 결제 API의 idempotency key에 대응합니다.",
        "figure": "‘외부 쓰기’ 다음 ‘상태 반환 전 종료’가 장애 지점입니다. 재개는 ‘노드 처음부터 재시작’으로 이동합니다. 마지막 ‘operation_id로 중복 차단’ 상자가 After의 한 줄 로그를 설명합니다.",
        "walk": "idempotency_worker.py는 order-2306을 파일에 쓴 뒤 ready 신호를 만들고 기다립니다. 부모 셀은 이 프로세스를 kill하고 같은 SQLite와 thread_id로 resume 프로세스를 실행합니다. 전략 이름 외의 종료 지점과 입력은 동일합니다.",
        "analysis": "naive 로그에는 order-2306이 두 줄입니다. 첫 프로세스와 재개 프로세스가 charge의 파일 쓰기를 각각 실행했습니다. idempotent 로그에는 한 줄만 남습니다. 두 번째 charge도 시작됐지만 기존 키를 확인하고 외부 쓰기를 건너뛰었습니다.",
        "cautions": ["확인과 쓰기를 별도 연산으로 구현하면 동시 요청 사이에 경쟁 조건이 생길 수 있으므로 운영에서는 원자적 고유 제약을 사용합니다.", "operation_id의 보존 기간은 외부 서비스의 재시도 가능 기간보다 짧지 않게 정합니다.", "멱등 처리가 어려운 작업은 interrupt 승인과 보상 작업을 함께 설계합니다."],
        "quiz": [("naive 로그가 두 줄이 된 실행 경로를 설명해 보세요.", "첫 charge가 기록한 뒤 종료됐고 재개한 charge가 처음부터 시작해 다시 기록했습니다."), ("idempotent 전략도 charge 노드 자체는 다시 실행되나요?", "실행됩니다. 다만 기존 operation_id를 확인하고 외부 쓰기를 생략합니다."), ("파일 목록 검사가 운영 환경에서 충분하지 않은 이유는 무엇인가요?", "동시에 두 요청이 검사하면 둘 다 미처리로 판단할 수 있으므로 원자적 고유 제약이 필요합니다."), ("체크포인트가 노드 내부 코드 줄마다 저장되지 않는다는 사실이 왜 중요한가요?", "상태 반환 전 장애에서는 노드가 처음부터 재시작되어 앞선 부작용도 반복될 수 있기 때문입니다.")],
    },
    "ch24-human-in-the-loop/01-interrupt-승인-게이트": {
        "prior": "Ch23에서 노드는 장애 뒤 처음부터 재시작될 수 있고 외부 쓰기에는 멱등성이 필요하다는 점을 확인했습니다. 이번 절은 실행을 시작하기 전에 사람이 요청을 검토하는 경계를 추가합니다. 체크포인터는 InMemorySaver를 사용해 승인 흐름 자체에 집중합니다.",
        "situation": "로컬 파일 쓰기를 송금이나 배포 같은 되돌리기 어려운 작업이라고 가정합니다. 거절할 수 있는 화면을 보여 주더라도 실제 쓰기가 이미 끝난 뒤라면 승인 게이트의 목적을 달성하지 못합니다. 코드 순서가 정책 문구만큼 중요합니다.",
        "definition": "interrupt(payload)는 payload를 __interrupt__에 담아 호출자에게 반환하고 현재 노드 실행을 중단합니다. Command(resume=value)를 같은 thread_id로 전달하면 value가 interrupt()의 반환값이 됩니다. 재개할 때 노드는 처음부터 실행되므로 interrupt 앞 코드는 다시 실행됩니다.",
        "figure": "‘요청 상태 저장’ 뒤 ‘interrupt 승인 질문’이 나오고 사람이 승인 또는 거절을 선택합니다. ‘승인일 때만 로컬 쓰기’는 safe_node의 if 문과 대응합니다. Before는 마지막 두 상자의 순서가 뒤바뀐 비교 경로입니다.",
        "walk": "effect_path는 노트북 폴더와 프로젝트 루트 어디에서 실행해도 찾을 수 있는 로컬 파일입니다. unsafe_node는 write_effect 뒤 interrupt를 호출합니다. safe_node는 interrupt 반환값이 참일 때만 write_effect를 호출합니다. 두 그래프 모두 False로 재개해 순서만 비교합니다.",
        "analysis": "unsafe 경로는 거절 상태인데도 transfer-local이 두 줄 남았습니다. 첫 중단과 재개에서 노드 앞부분이 각각 실행됐기 때문입니다. safe 경로는 rejected를 반환하고 effect 파일이 없습니다. 승인 질문을 외부 쓰기 앞에 둔 효과를 실제 파일로 확인했습니다.",
        "cautions": ["interrupt를 try/except로 감싸면 런타임의 중단 신호를 일반 오류로 처리할 수 있으므로 공식 규칙을 따릅니다.", "payload는 JSON으로 직렬화할 수 있는 요청 ID, 요약, 위험 수준처럼 검토에 필요한 값만 담습니다.", "interrupt 앞에 필요한 쓰기가 있다면 재실행돼도 같은 결과를 내도록 멱등하게 만듭니다."],
        "quiz": [("unsafe 경로에서 같은 값이 두 줄 기록된 이유는 무엇인가요?", "중단 전 한 번 쓰고 재개 시 노드가 처음부터 실행되며 한 번 더 썼기 때문입니다."), ("safe_node에서 False를 전달하면 write_effect가 호출되지 않는 이유는 무엇인가요?", "interrupt 반환값을 확인한 if not approved 분기가 먼저 rejected를 반환하기 때문입니다."), ("interrupt payload에 넣기 알맞은 값은 무엇인가요?", "요청 ID와 사람이 판단할 요약처럼 JSON 직렬화가 가능하고 검토에 필요한 값입니다."), ("이 실습이 실제 송금을 실행하지 않는 이유는 무엇인가요?", "학습용 로컬 부작용으로 승인 순서를 안전하게 관찰하기 위해서입니다.")],
    },
    "ch24-human-in-the-loop/02-Command-resume으로-실행-재개": {
        "prior": "앞 절에서 interrupt가 실행을 멈추고 Command(resume=False)가 거절 값을 돌려주는 기본 흐름을 확인했습니다. 이번 절은 한 번의 승인·거절로 끝나지 않는 입력 검증을 다룹니다. 동일한 interrupt 호출 순서를 유지하는 while 반복을 사용합니다.",
        "situation": "승인 화면이 maybe 같은 허용되지 않은 값을 보내거나 오래된 클라이언트가 예상과 다른 문자열을 보낼 수 있습니다. 잘못된 값을 승인으로 해석하거나 실행을 버리지 않고, 오류 설명을 포함한 새 중단 상태를 반환해야 합니다.",
        "definition": "첫 graph.invoke는 입력 상태를 받아 interrupt에서 멈춥니다. Command(resume='maybe')는 첫 interrupt의 반환값이 되지만 허용 집합에 없으므로 while이 다음 interrupt를 호출합니다. 두 번째 Command(resume='approve')는 두 번째 interrupt의 반환값이 되어 노드가 상태 갱신을 반환합니다.",
        "figure": "‘interrupt에서 중단’과 ‘Command(resume=값)’ 사이를 사람이 응답할 때마다 오갑니다. 노드는 처음부터 다시 실행하지만 같은 순서의 interrupt가 저장된 값을 소비합니다. ‘검증 뒤 완료 또는 재질문’ 상자가 maybe와 approve의 두 경로를 나눕니다.",
        "walk": "review 노드는 allowed를 approve와 reject로 고정합니다. 첫 출력의 payload에는 요청과 허용값만 있습니다. maybe를 전달한 두 번째 출력에는 error가 추가됩니다. 마지막 호출은 같은 review-2402 스레드에 approve를 전달하고 get_state로 next를 확인합니다.",
        "analysis": "첫 prompt와 두 번째 prompt의 request와 allowed는 같습니다. 달라진 값은 error 한 항목뿐입니다. approve 뒤 final.decision은 approve이고 next가 빈 튜플이므로 실행이 완료됐습니다. history count 3은 중단을 세 번 뜻하는 값이 아니라 최신 체크포인트 기록 수입니다.",
        "cautions": ["재개할 때 다른 thread_id를 쓰면 기다리던 interrupt를 찾지 못합니다.", "노드 안의 여러 interrupt 호출 순서를 조건에 따라 바꾸지 않습니다.", "승인 값과 승인자, 승인 시각의 감사 기록은 그래프 상태와 운영 정책에 맞게 별도로 보존합니다."],
        "quiz": [("maybe를 전달한 뒤 그래프가 완료되지 않은 이유는 무엇인가요?", "허용 집합에 없는 값이라 review가 오류를 포함한 다음 interrupt를 호출했기 때문입니다."), ("Command(resume='approve')의 문자열은 어디에서 읽히나요?", "중단돼 있던 review 노드의 interrupt() 반환값으로 읽힙니다."), ("재개 호출에 같은 thread_id가 필요한 이유는 무엇인가요?", "체크포인터가 해당 스레드의 중단 상태와 재개할 interrupt를 찾아야 하기 때문입니다."), ("interrupt 순서를 바꾸면 어떤 문제가 생기나요?", "저장된 재개 값이 의도와 다른 interrupt 호출에 대응할 수 있습니다.")],
    },
    "ch24-human-in-the-loop/03-상태-기록과-다른-분기-재실행": {
        "prior": "앞 절까지는 최신 중단 상태를 같은 스레드에서 이어 갔습니다. 체크포인터에는 최신 상태뿐 아니라 단계별 StateSnapshot도 남습니다. 이번 절은 완료된 가격 계산의 과거 snapshot을 골라 할인율 하나만 바꾼 새 경로를 실행합니다.",
        "situation": "10% 할인으로 계산을 마친 뒤 20% 할인 시나리오를 검토해야 한다고 가정합니다. 원본 결과 9000을 지우거나 START부터 모든 작업을 반복할 필요는 없습니다. quote가 끝나고 discount가 시작되기 전 상태에서 rate만 바꾸면 됩니다.",
        "definition": "get_state_history(config)는 최신순으로 snapshot을 반환합니다. snapshot.next가 ('discount',)인 항목은 quote 결과가 저장됐고 discount가 다음인 지점입니다. update_state(snapshot.config, {'rate': 0.2})는 그 과거 상태를 부모로 하는 새 체크포인트를 만들며 원본 완료 체크포인트는 남깁니다.",
        "figure": "‘get_state_history’에서 ‘과거 체크포인트 선택’으로 이동해 next가 discount인 항목을 고릅니다. ‘update_state로 값 변경’은 rate만 0.2로 바꾸고, ‘새 분기 invoke’는 discount 뒤쪽만 실행합니다. quote가 분기 trace에서 한 번만 보이는 이유입니다.",
        "walk": "quote는 trace에 이름만 추가하고 discount는 base_price와 rate로 final_price를 계산합니다. 원본 완료 뒤 original_final_config를 따로 보존합니다. 과거 before_discount.config를 update_state로 갱신하고 반환된 fork_config에 invoke(None)를 호출합니다.",
        "analysis": "원본 설정을 직접 읽은 final_price는 9000이고 분기는 8000입니다. fork trace에는 기존 quote와 새 discount:0.2가 있어 quote 결과가 재사용됐음을 보여 줍니다. 두 최신 config가 다르므로 새 분기가 원본 완료 체크포인트를 덮어쓰지 않았습니다.",
        "cautions": ["과거 지점 뒤의 LLM 호출, API 요청, interrupt는 다시 실행되므로 비용과 부작용을 검토합니다.", "업데이트할 상태 키가 어느 노드의 출력으로 간주되는지 필요하면 as_node를 명시합니다.", "time travel은 외부 시스템 시간을 되돌리지 않습니다. 이미 수행한 외부 쓰기는 별도 보상이나 격리가 필요합니다."],
        "quiz": [("분기 기준으로 next가 discount인 snapshot을 고른 이유는 무엇인가요?", "quote 결과는 보존하고 할인 계산부터 새 rate로 다시 실행하기 위해서입니다."), ("원본 9000과 분기 8000이 함께 남는 근거는 무엇인가요?", "원본 완료 config를 따로 읽었고 fork config가 다른 체크포인트를 가리킵니다."), ("fork trace에서 quote가 새로 추가되지 않은 이유는 무엇인가요?", "분기 지점이 quote 완료 뒤이므로 저장된 quote 결과를 재사용했기 때문입니다."), ("time travel로 외부 결제도 자동 취소되나요?", "아닙니다. 그래프 상태 분기와 외부 시스템의 보상 작업은 별도로 처리해야 합니다.")],
    },
}

SECTION_INFO = {
    "ch23-persistence": [
        ("01-체크포인터와-스레드", "체크포인터와 스레드", "experiment", "에이전트가 여러 차례 호출되는 동안 같은 사용자의 상태를 이어 가고 다른 사용자의 상태는 섞지 않아야 합니다.", "체크포인터(checkpointer)는 그래프 단계가 끝날 때 상태 스냅샷을 저장합니다. 스레드(thread)는 관련 체크포인트를 묶는 논리적 실행 단위이며 thread_id가 그 묶음을 찾는 키가 됩니다.", "같은 thread_id의 두 실행은 total 7로 이어졌고 다른 thread_id는 total 4에서 독립적으로 시작했습니다.", "다음 절에서는 메모리 대신 PostgreSQL에 체크포인트 표를 만듭니다.", ["체크포인터", "스레드", "체크포인트"]),
        ("02-PostgresSaver-준비와-스키마", "PostgresSaver 준비와 스키마", "paired", "운영 프로세스가 종료되어도 상태를 남기려면 별도 데이터베이스가 필요합니다. Ch4에서 배운 스키마와 표 조회를 체크포인터 준비에 적용합니다.", "PostgresSaver는 PostgreSQL에 체크포인트와 중간 쓰기를 저장하는 구현입니다. 최초 한 번 setup()을 호출해야 필요한 표와 마이그레이션 기록이 생성됩니다.", "setup 전에는 UndefinedTable이 발생했고 setup 뒤에는 value 12와 checkpoints, checkpoint_writes 표를 확인했습니다.", "다음 절에서는 연결과 그래프 객체를 새로 만들어도 같은 스레드를 이어 갑니다.", ["PostgresSaver", "setup", "마이그레이션"]),
        ("03-스레드-재개와-대화-이어가기", "스레드 재개와 대화 이어가기", "experiment", "웹 요청마다 그래프 객체가 새로 만들어져도 사용자는 이전 대화가 이어지기를 기대합니다. 상태가 프로세스 메모리가 아니라 저장소에 있어야 이 요구를 충족합니다.", "재개(resume)는 같은 thread_id의 최신 체크포인트를 읽고 새 입력을 기존 상태에 합쳐 다음 실행을 시작하는 동작입니다. 저장소 연결과 그래프 객체가 달라져도 thread_id와 체크포인트가 같으면 상태를 찾을 수 있습니다.", "첫 연결을 닫은 뒤 새 연결에서 질문 2를 넣었고 질문 1과 답변 1이 그대로 남았습니다.", "다음 절에서는 프로세스를 강제로 종료해 저장 모드별 손실 범위를 비교합니다.", ["재개", "영속 저장소", "상태 스냅샷"]),
        ("04-내구-실행-모드-비교", "내구 실행 모드 비교", "experiment", "체크포인트를 자주 동기 저장하면 복구 범위가 작아지지만 다음 노드가 기다리는 시간이 늘어날 수 있습니다. 저장 시점을 선택하려면 세 모드의 차이를 실제 중단에서 확인해야 합니다.", "내구성(durability) 모드는 체크포인트 저장 완료와 다음 노드 실행의 관계를 정합니다. sync는 저장 완료 뒤 다음 단계로 가고, async는 다음 단계와 저장을 겹쳐 실행하며, exit는 실행이 끝날 때 저장합니다.", "두 번째 노드 진입 직후 자식 프로세스를 kill했습니다. sync에는 first 완료 상태가 남았고 exit에는 완료 체크포인트가 없었습니다. async 값은 실제 실행 출력에 기록했습니다.", "다음 절에서는 같은 단계의 병렬 노드 중 일부만 성공했을 때 pending writes를 확인합니다.", ["durability", "sync", "async", "exit"]),
        ("05-pending-writes와-장애-복구", "pending writes와 장애 복구", "experiment", "병렬 처리 하나가 실패했다고 이미 성공한 느린 작업까지 반복하면 비용과 부작용이 늘어납니다. 같은 단계의 부분 성공을 보존하는 단위가 필요합니다.", "pending writes는 체크포인트 단계가 완전히 끝나기 전에 성공한 작업의 중간 쓰기입니다. 재개할 때 런타임은 이 결과를 사용해 성공한 노드를 건너뛰고 실패한 노드만 다시 실행할 수 있습니다.", "첫 실행에서 good과 flaky가 한 번씩 실행됐고 재개 뒤 good은 총 1회, flaky는 총 2회였습니다. 최종 상태에는 두 결과가 모두 포함됐습니다.", "다음 절에서는 노드 자체가 다시 시작될 때 외부 쓰기의 중복을 막습니다.", ["pending writes", "superstep", "부분 성공"]),
        ("06-노드-재시작과-멱등성", "노드 재시작과 멱등성", "paired", "체크포인트는 노드 안의 각 코드 줄 뒤에 저장되지 않습니다. 외부 쓰기 뒤 상태 반환 전에 프로세스가 끝나면 같은 노드가 다시 시작됩니다.", "멱등성(idempotency)은 같은 작업을 여러 번 요청해도 외부 결과가 한 번 적용된 것과 같게 유지되는 성질입니다. operation_id를 이미 처리한 키로 기록하면 재시작한 노드가 중복 쓰기를 건너뛸 수 있습니다.", "같은 지점에서 자식 프로세스를 종료하고 재개했습니다. 단순 추가 방식은 주문 번호가 2줄, 멱등 키 방식은 1줄 남았습니다.", "Ch24에서는 노드 실행 전에 사람의 승인 값을 받아 부작용 여부를 결정합니다.", ["멱등성", "operation_id", "노드 재시작"]),
    ],
    "ch24-human-in-the-loop": [
        ("01-interrupt-승인-게이트", "interrupt 승인 게이트", "paired", "결제·배포·삭제처럼 되돌리기 어려운 동작은 모델의 판단만으로 실행하지 않고 사람이 요청 내용을 확인해야 합니다.", "interrupt()는 노드 실행을 중단하고 JSON으로 직렬화할 수 있는 승인 요청을 호출자에게 반환합니다. 체크포인터가 현재 상태를 저장하므로 같은 thread_id로 승인 값을 전달할 때 이어서 실행할 수 있습니다.", "부작용 뒤에 interrupt를 둔 Before는 거절해도 기록이 남았습니다. interrupt를 먼저 둔 After는 거절 상태를 반환하고 파일을 만들지 않았습니다.", "다음 절에서는 Command(resume=) 값이 interrupt()의 반환값이 되는 과정을 확인합니다.", ["interrupt", "승인 게이트", "중단 상태"]),
        ("02-Command-resume으로-실행-재개", "Command(resume=)으로 실행 재개", "experiment", "사람의 응답은 늦게 도착하거나 허용한 형식과 다를 수 있습니다. 중단된 실행을 잃지 않고 값을 검증한 뒤 다시 요청해야 합니다.", "Command(resume=value)는 같은 스레드의 중단된 interrupt()에 value를 전달합니다. 재개하면 노드는 처음부터 다시 실행되며 interrupt 호출 순서가 같아야 저장된 재개 값과 정확히 대응합니다.", "첫 호출은 승인 질문에서 멈췄고 maybe를 전달한 두 번째 호출은 오류 설명과 함께 다시 멈췄습니다. approve를 전달하자 decision이 저장되고 next가 빈 튜플이 됐습니다.", "다음 절에서는 완료된 기록을 열어 중간 상태에서 새 분기를 만듭니다.", ["Command", "resume", "재개 값"]),
        ("03-상태-기록과-다른-분기-재실행", "상태 기록과 다른 분기 재실행", "experiment", "운영 중 잘못된 파라미터나 판단을 발견했을 때 전체 실행을 지우지 않고 과거 지점에서 다른 선택을 시험할 수 있어야 합니다.", "get_state_history()는 스레드의 StateSnapshot을 최신순으로 반환합니다. 과거 체크포인트에 update_state()로 새 값을 쓰면 원본 기록을 보존한 새 분기 설정이 생기고 invoke(None, config)으로 그 지점 뒤를 다시 실행할 수 있습니다.", "원본 할인율 0.1의 최종 가격은 9000으로 유지됐고 과거 체크포인트에서 0.2로 바꾼 분기는 8000을 반환했습니다.", "Ch25에서는 저장된 실행에서 상태·메시지·사용자 정의 진행 상황을 스트리밍합니다.", ["상태 기록", "time travel", "분기"]),
    ],
}

FIGURES = {
    "ch23-persistence": {
        "01-흐름": (["입력 + thread_id", "체크포인트 저장", "같은 스레드 재개", "다른 스레드 격리"], "thread_id가 관련 체크포인트를 묶어 같은 스레드의 상태만 이어 줍니다."),
        "02-흐름": (["PostgreSQL 연결", "PostgresSaver.setup", "체크포인트 표", "그래프 실행 저장"], "setup이 스키마를 준비한 뒤 그래프 실행이 체크포인트와 중간 쓰기를 저장합니다."),
        "03-흐름": (["프로세스 1 실행", "SQLite 체크포인트", "프로세스 1 종료", "프로세스 2 재개"], "프로세스 객체가 달라져도 같은 저장소와 thread_id로 상태를 이어 갑니다."),
        "04-흐름": (["노드 1 완료", "sync: 저장 후 이동", "async: 저장과 다음 노드 겹침", "exit: 종료 시 저장"], "세 내구 실행 모드는 저장 완료와 다음 노드 실행의 순서를 다르게 정합니다."),
        "05-흐름": (["같은 단계 병렬 실행", "good 성공 → pending write", "flaky 실패", "재개: flaky만 재실행"], "pending write가 성공한 병렬 노드의 결과를 보존해 재개 시 중복 실행을 줄입니다."),
        "06-흐름": (["외부 쓰기", "상태 반환 전 종료", "노드 처음부터 재시작", "operation_id로 중복 차단"], "노드는 처음부터 재시작되므로 외부 쓰기는 operation_id를 사용해 멱등하게 처리합니다."),
    },
    "ch24-human-in-the-loop": {
        "01-흐름": (["요청 상태 저장", "interrupt 승인 질문", "사람의 승인/거절", "승인일 때만 로컬 쓰기"], "승인 게이트를 부작용 앞에 두어 거절된 요청의 쓰기를 막습니다."),
        "02-흐름": (["interrupt에서 중단", "Command(resume=값)", "노드 처음부터 재실행", "검증 뒤 완료 또는 재질문"], "Command의 값이 같은 스레드의 interrupt 반환값으로 전달됩니다."),
        "03-흐름": (["get_state_history", "과거 체크포인트 선택", "update_state로 값 변경", "새 분기 invoke"], "과거 상태를 갱신하면 원본을 보존한 다른 분기에서 후속 노드를 다시 실행합니다."),
    },
}

CODE_COMMENTS = {
    "ch23-persistence/01-체크포인터와-스레드": ["체크포인터를 붙인 누적 그래프와 상태 형식을 정의합니다.", "customer-a 스레드에 3과 4를 차례로 넣어 누적 상태를 읽습니다.", "thread_id만 customer-b로 바꾸어 저장 상태가 섞이지 않는지 비교합니다."],
    "ch23-persistence/02-PostgresSaver-준비와-스키마": ["ch23_lab 전용 스키마와 두 배 계산 그래프를 준비합니다.", "setup을 호출하지 않은 PostgresSaver의 실제 UndefinedTable 오류를 기록합니다.", "setup 뒤 같은 그래프를 실행하고 생성된 체크포인트 표 이름을 조회합니다."],
    "ch23-persistence/03-스레드-재개와-대화-이어가기": ["노트북 위치와 프로젝트 루트 양쪽에서 실습 폴더와 SQLite 파일을 준비합니다.", "질문과 답변을 이어 붙이는 리듀서와 응답 노드를 정의합니다.", "첫 SQLite 연결에서 질문 1과 답변 1을 동기 저장한 뒤 연결을 닫습니다.", "새 SQLite 연결과 새 그래프 객체에서 같은 thread_id에 질문 2를 추가합니다."],
    "ch23-persistence/04-내구-실행-모드-비교": ["worker는 실제 종료할 자식 프로세스이고 run_dir는 모드별 SQLite 파일 위치입니다.", "read_saved는 프로세스 종료 뒤 thread_id에 연결된 최신 채널 값을 읽습니다.", "ready 파일을 두 번째 노드 진입 신호로 사용하고 deadline 20초 안에 자식 프로세스를 종료·재개합니다.", "그래프와 종료 시점을 고정하고 exit, async, sync만 바꾸어 세 번 실행합니다.", "중단 전 저장값, 재개 후 완료값, 실제 노드 호출 순서를 모드별로 나란히 표시합니다."],
    "ch23-persistence/05-pending-writes와-장애-복구": ["good과 flaky의 호출 횟수를 셀 로컬 파일과 병렬 상태 형식을 준비합니다.", "good은 성공 결과를 쓰고 flaky는 허용 파일이 생기기 전까지 실제 RuntimeError를 냅니다.", "같은 superstep의 첫 실행을 실패시키고 저장된 task와 호출 순서를 확인합니다.", "허용 파일을 만든 뒤 입력 없이 재개해 good은 1회, flaky는 2회인지 검사합니다."],
    "ch23-persistence/06-노드-재시작과-멱등성": ["worker와 모드별 SQLite·로그 파일을 둘 실습 경로를 찾습니다.", "외부 쓰기 직후 자식 프로세스를 종료하고 같은 체크포인트에서 새 프로세스로 재개합니다.", "중복 검사가 없는 naive 전략에서 같은 operation_id가 두 번 기록되는지 확인합니다.", "처리된 operation_id를 검사하는 전략에서 로컬 쓰기가 한 줄만 남는지 확인합니다."],
    "ch24-human-in-the-loop/01-interrupt-승인-게이트": ["승인 결과를 기록할 로컬 파일과 HITL 상태 형식을 준비합니다.", "부작용 뒤 interrupt를 둔 그래프를 거절해도 파일 기록이 남는지 확인합니다.", "interrupt를 먼저 둔 그래프를 거절해 파일 자체가 생성되지 않는지 확인합니다."],
    "ch24-human-in-the-loop/02-Command-resume으로-실행-재개": ["approve와 reject만 허용하는 interrupt 입력 검증 노드를 준비합니다.", "첫 중단 뒤 maybe를 전달해 오류가 추가된 두 번째 interrupt 값을 읽습니다.", "같은 thread_id에 approve를 전달해 decision과 종료 상태를 확인합니다."],
    "ch24-human-in-the-loop/03-상태-기록과-다른-분기-재실행": ["가격·할인율·실행 기록을 담는 상태와 두 계산 노드를 정의합니다.", "quote 다음 discount가 실행되도록 그래프를 연결하고 체크포인터를 붙입니다.", "할인율 0.1의 원본을 완료하고 next가 discount인 체크포인트를 고릅니다.", "선택한 상태의 할인율만 0.2로 바꾸어 새 분기의 최종 가격을 계산합니다."],
}

def write_all() -> None:
    for key, data in NOTEBOOKS.items():
        chapter, slug = key.split("/", 1)
        if chapter == "ch23-persistence":  # Ch 23 개선본을 옛 판으로 덮어쓰지 않도록 건너뜀(2026-09-25)
            continue
        packages = "langgraph==1.2.11"
        if chapter == "ch23-persistence" and slug.startswith("02-"):
            packages += " langgraph-checkpoint-postgres==3.0.5 'psycopg[binary,pool]==3.3.3'"
        elif chapter == "ch23-persistence" and not slug.startswith("01-"):
            packages += " langgraph-checkpoint-sqlite==3.0.3"
        data["cells"][1:1] = [
            md("## 실행 환경 준비\n\nPython 3.12 커널에 이 절에서 사용할 패키지 버전을 고정합니다."),
            code(f"# 실습에 필요한 패키지를 같은 버전으로 설치합니다.\n%pip install -q {packages}"),
        ]
        comment_index = 0
        for index, cell in enumerate(data["cells"], 1):
            cell["id"] = f"cell-{index:02d}"
            if cell["cell_type"] == "code" and not "".join(cell["source"]).startswith("#"):
                comment = CODE_COMMENTS[key][comment_index]
                comment_index += 1
                cell["source"] = lines(f"# {comment}\n" + "".join(cell["source"]))
        path = ROOT / "labs/part6" / chapter / "notebooks" / f"{slug}.ipynb"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    for chapter, items in SECTION_INFO.items():
        if chapter == "ch23-persistence":  # Ch 23 _src·figures/_gen_figures.py도 건너뜀(2026-09-25)
            print("skip ch23: textbook/part6/ch23-persistence/qa/upgrade/author_NN.py가 Ch 23 파일을 씁니다")
            continue
        for slug, title, fmt, why, concept, observation, next_text, terms in items:
            path = ROOT / "textbook/part6" / chapter / "_src" / f"{slug}.html"
            path.write_text(section_html(chapter, slug, title, fmt, why, concept, observation, next_text, terms), encoding="utf-8")

        figure_dir = ROOT / "textbook/part6" / chapter / "figures"
        figure_dir.mkdir(parents=True, exist_ok=True)
        spec_repr = repr(FIGURES[chapter])
        generator = f'''"""Generate Ch23/Ch24 diagrams with the established Part 5 renderer."""\nfrom pathlib import Path\nimport sys\nsys.path.insert(0, str(Path(__file__).resolve().parents[3] / "part5"))\nfrom _figure import linear, render\nHERE = Path(__file__).resolve().parent\nRAW = {spec_repr}\nif __name__ == "__main__":\n    for name, (labels, caption) in RAW.items():\n        roles = ["data", "code", "failure", "tool"]\n        render(HERE, name, linear([(label, roles[i % len(roles)]) for i, label in enumerate(labels)], caption))\n    print(f"generated {{len(RAW)}} SVG/Excalidraw pairs")\n'''
        (figure_dir / "_gen_figures.py").write_text(generator, encoding="utf-8")

if __name__ == "__main__":
    write_all()
    print(f"wrote {len(NOTEBOOKS)} notebooks and sources")
