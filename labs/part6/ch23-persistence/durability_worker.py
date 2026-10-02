# Ch 23 04절 — 노트북이 자식 프로세스로 실행하는 스크립트입니다.
# 노드 first → second 두 개짜리 그래프를 SQLite 체크포인터와 함께 한 번 실행합니다.
# 둘째 노드는 신호 파일을 만든 뒤, 첫 실행 단계에서는 30초 쉽니다.
# 노트북은 그 30초 사이에 이 프로세스를 강제로 끝냅니다.
#
# 명령줄에서 받는 글 다섯(노트북이 이 차례로 넘깁니다. 파일 이름은 모두 노트북 임시 폴더 안의 이름):
#   1 SQLite 파일 이름 · 2 신호 파일 이름 · 3 기록 파일 이름 · 4 저장 시점(exit·async·sync) · 5 단계(first-run·resume)
import operator
import sqlite3
import sys
import time
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END

# sys.argv는 명령줄에서 받은 글의 목록이고, 0번 자리에는 이 스크립트의 이름이 들어 있습니다
sqlite_name = sys.argv[1]
signal_name = sys.argv[2]
record_name = sys.argv[3]
mode = sys.argv[4]
phase = sys.argv[5]
# 첫 실행 단계에서 둘째 노드가 쉬는 초입니다
pause_seconds = 30


# 노드가 마친 이름을 이어 붙이는 칸 하나를 둔 상태 형식입니다(노트북 2절의 StepState와 같은 모양)
class StepState(TypedDict):
    completed: Annotated[list[str], operator.add]


# 노드 이름 하나를 기록 파일 끝에 한 줄로 덧붙입니다(여는 방식 "a"는 파일 끝에 이어 씁니다)
def write_record(node_name):
    with open(record_name, "a", encoding="utf-8") as record_file:
        record_file.write(node_name + "\n")


# 첫째 노드: 기록 파일에 자기 이름을 적고, 마친 이름 first를 냅니다
def first(state):
    write_record("first")
    return {"completed": ["first"]}


# 둘째 노드: 기록 파일에 자기 이름을 적고 신호 파일을 만든 뒤, 첫 실행 단계에서만 30초 쉽니다
def second(state):
    write_record("second")
    with open(signal_name, "w", encoding="utf-8") as signal_file:
        signal_file.write("second")
    if phase == "first-run":
        time.sleep(pause_seconds)
    return {"completed": ["second"]}


# 노트북 2절과 같은 모양의 설계 객체입니다(노드 이름 first·second, 엣지 셋)
builder = StateGraph(StepState)
builder.add_node("first", first)
builder.add_node("second", second)
builder.add_edge(START, "first")
builder.add_edge("first", "second")
builder.add_edge("second", END)

# 스레드 이름은 저장 시점 이름을 그대로 씁니다
config = {"configurable": {"thread_id": mode}}
connection = sqlite3.connect(sqlite_name, check_same_thread=False)
saver = SqliteSaver(connection)
graph = builder.compile(checkpointer=saver)
saved = graph.get_state(config)
# 다시 실행 단계에서 다음에 실행할 노드가 저장되어 있으면, 새 입력 없이(None) 그 체크포인트부터 이어 갑니다
if phase == "resume" and len(saved.next) > 0:
    graph.invoke(None, config, durability=mode)
else:
    # 첫 실행 단계이거나 저장된 것이 없으면, 빈 목록을 넣어 처음부터 실행합니다
    graph.invoke({"completed": []}, config, durability=mode)
connection.close()
