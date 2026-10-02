# Ch 23 06절 — 노트북이 자식 프로세스로 실행하는 스크립트입니다.
# 노드 receive_order → charge 두 개짜리 그래프를 SQLite 체크포인터와 함께 한 번 실행합니다.
# 둘째 노드 charge는 결제 기록 파일에 주문 키를 한 줄 적고 신호 파일을 만든 뒤, 첫 실행 단계에서는 30초 쉽니다.
# 노트북은 그 30초 사이에 이 프로세스를 강제로 끝냅니다. 결제는 실제 서비스가 아니라 파일에 한 줄 적는 흉내입니다.
#
# 명령줄에서 받는 글 다섯(04절 스크립트와 같은 차례, 파일 이름은 모두 노트북 임시 폴더 안의 이름):
#   1 SQLite 파일 이름 · 2 신호 파일 이름 · 3 결제 기록 파일 이름 · 4 쓰기 방식(naive·idempotent) · 5 단계(first-run·resume)
import operator
import os
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
strategy = sys.argv[4]
phase = sys.argv[5]
# 첫 실행 단계에서 둘째 노드가 쉬는 초입니다
pause_seconds = 30
# 저장 시점은 sync입니다(04절: 둘째 노드에서 끊겨도 첫째 노드까지의 체크포인트가 파일에 남습니다)
durability_mode = "sync"


# 주문 키 칸과, 노드가 한 일을 이어 붙이는 칸을 둔 상태 형식입니다(노트북 3절의 OrderState와 같은 모양)
class OrderState(TypedDict):
    order_key: str
    notes: Annotated[list[str], operator.add]


# 기록 파일 끝에 주문 키 한 줄을 덧붙이고, 한 일을 글 "적음"으로 내놓습니다
def append_key(record_name, order_key):
    # 여는 방식 "a"는 파일 끝에 이어 쓰고, 파일이 없으면 새로 만듭니다
    with open(record_name, "a", encoding="utf-8") as record_file:
        record_file.write(order_key + "\n")
    return "적음"


# 기록 파일에 같은 주문 키가 이미 있으면 건너뛰고, 없을 때만 한 줄을 덧붙입니다
def append_key_once(record_name, order_key):
    written_keys = []
    # 기록 파일이 있을 때만 읽습니다(처음 부를 때는 파일이 없습니다)
    if os.path.exists(record_name):
        with open(record_name, encoding="utf-8") as record_file:
            written_keys = record_file.read().split()
    if order_key in written_keys:
        return "건너뜀"
    return append_key(record_name, order_key)


# 신호 파일을 만들어, 둘째 노드가 결제 기록을 마쳤다고 노트북에 알립니다
def write_signal():
    with open(signal_name, "w", encoding="utf-8") as signal_file:
        signal_file.write("charge")


# 첫째 노드: 한 일 "주문 받음"을 목록에 담아 냅니다
def receive_order(state):
    return {"notes": ["주문 받음"]}


# 둘째 노드: 쓰기 방식에 따라 결제 기록 파일에 주문 키를 적고, 신호 파일을 만든 뒤 첫 실행 단계에서만 30초 쉽니다
def charge(state):
    order_key = state["order_key"]
    if strategy == "idempotent":
        note = append_key_once(record_name, order_key)
    else:
        note = append_key(record_name, order_key)
    write_signal()
    if phase == "first-run":
        time.sleep(pause_seconds)
    return {"notes": [note]}


# 노트북 3절과 같은 모양의 설계 객체입니다(노드 이름 receive_order·charge, 엣지 셋)
builder = StateGraph(OrderState)
builder.add_node("receive_order", receive_order)
builder.add_node("charge", charge)
builder.add_edge(START, "receive_order")
builder.add_edge("receive_order", "charge")
builder.add_edge("charge", END)

# 스레드 이름은 쓰기 방식 이름을 그대로 씁니다
config = {"configurable": {"thread_id": strategy}}
connection = sqlite3.connect(sqlite_name, check_same_thread=False)
saver = SqliteSaver(connection)
graph = builder.compile(checkpointer=saver)
saved = graph.get_state(config)
# 다시 실행 단계에서 다음에 실행할 노드가 저장되어 있으면, 새 입력 없이(None) 그 체크포인트부터 이어 갑니다
if phase == "resume" and len(saved.next) > 0:
    graph.invoke(None, config, durability=durability_mode)
else:
    # 첫 실행 단계이거나 저장된 것이 없으면, 주문 키를 넣어 처음부터 실행합니다
    graph.invoke({"order_key": "order-2306", "notes": []}, config, durability=durability_mode)
connection.close()
