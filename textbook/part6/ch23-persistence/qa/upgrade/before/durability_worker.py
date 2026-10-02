"""Run one graph long enough for the parent notebook to terminate this process."""
from __future__ import annotations
import json
import sqlite3
import sys
import time
from pathlib import Path
from typing_extensions import TypedDict
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

class State(TypedDict):
    completed: list[str]

db_path, ready_path, mode = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
phase = sys.argv[4] if len(sys.argv) > 4 else "initial"
trace_path = ready_path.with_suffix(".trace")

def first(state: State) -> dict:
    with trace_path.open("a", encoding="utf-8") as stream:
        stream.write("first\n")
    return {"completed": state["completed"] + ["first"]}

def second(state: State) -> dict:
    with trace_path.open("a", encoding="utf-8") as stream:
        stream.write("second\n")
    ready_path.write_text(json.dumps({"mode": mode, "entered": "second"}), encoding="utf-8")
    if phase == "initial":
        time.sleep(30)
    return {"completed": state["completed"] + ["second"]}

builder = StateGraph(State)
builder.add_node("first", first)
builder.add_node("second", second)
builder.add_edge(START, "first")
builder.add_edge("first", "second")
builder.add_edge("second", END)
with sqlite3.connect(db_path, check_same_thread=False) as conn:
    graph = builder.compile(checkpointer=SqliteSaver(conn))
    graph_input = {"completed": []} if phase == "initial" or mode == "exit" else None
    graph.invoke(graph_input, {"configurable": {"thread_id": mode}}, durability=mode)
