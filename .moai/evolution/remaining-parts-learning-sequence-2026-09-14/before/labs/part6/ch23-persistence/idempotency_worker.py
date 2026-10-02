"""Create a local side effect, then wait so a parent can terminate the node."""
from __future__ import annotations
import sqlite3
import sys
import time
from pathlib import Path
from typing_extensions import TypedDict
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

class State(TypedDict):
    operation_id: str
    result: str

db_path, log_path, ready_path, strategy, phase = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], sys.argv[5]

def charge(state: State):
    key = state["operation_id"]
    existing = log_path.read_text(encoding="utf-8").splitlines() if log_path.exists() else []
    if strategy == "naive" or key not in existing:
        with log_path.open("a", encoding="utf-8") as stream:
            stream.write(key + "\n")
    ready_path.write_text("side-effect-complete", encoding="utf-8")
    if phase == "first":
        time.sleep(30)
    return {"result": "charged"}

builder = StateGraph(State)
builder.add_node("charge", charge)
builder.add_edge(START, "charge")
builder.add_edge("charge", END)
with sqlite3.connect(db_path, check_same_thread=False) as conn:
    graph = builder.compile(checkpointer=SqliteSaver(conn))
    graph_input = {"operation_id": "order-2306", "result": ""} if phase == "first" else None
    graph.invoke(graph_input, {"configurable": {"thread_id": strategy}}, durability="sync")
