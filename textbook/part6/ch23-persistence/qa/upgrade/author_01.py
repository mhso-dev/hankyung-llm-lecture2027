"""Ch 23 01절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 author_01.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_01.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**(chapter.json).

## 결정 1 — 모델을 부르지 않는다 (챕터 리드 결정 1, M1·M3)

이 챕터는 상태를 저장하고 이어 가는 일이 주제다. 매번 같은 값을 내는 우리 노드(수를 더하는 함수)로 그래프를 만들어
저장된 값이 맞는지 출력으로 가른다. 모델 요청 0번, 키 셀 없음(Ch 13 01~06·Ch 20 03 선례). 잠금은 바꾸지 않는다.

## 결정 2 — 모든 절이 빈 임시 폴더에서 시작한다 (챕터 리드 결정 2, Ch 4 03절 선례)

준비 셀 차례: 설치 → 가져오기 → 임시 폴더(`tempfile.mkdtemp(prefix="ch23-NN-")` → `os.chdir()` → `os.listdir()`).
도구 파일을 가져오는 절은 옮기기 전에 가져온다(규격 §2-7 5번). 폴더 위치는 실행마다 달라 출력하지 않고,
이름에 앞머리가 들어 있는지(`True`)만 출력한다. 이 절의 `InMemorySaver`는 파일을 쓰지 않으므로 11절에서 폴더가 비어 있는지 본다.

## 결정 3 — 옛 판 모양(customer-a 3 → 7 · customer-b 4)을 지키고, 체크포인트 수를 센다

옛 판 그래프(칸 `total`·`events`, 노드 `add`)를 칸 `total`·`amount`·`trace`(실행 흔적, Ch 13 02절 `operator.add`)로 바꿨다.
체크포인터 없는 그래프(3절, `KeyError`)와 견주고, `get_state`·`get_state_history`로 저장된 것을 센다(6·3·6).
값 바꿔 보기 둘: 스레드 이름만(customer-b) · 둘째 입력에 합계 칸(customer-c). 옛 판의 Store 문장은 b7 한 줄(실행 안 함)로만.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`sorted`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·
튜플 풀기·세미콜론·`isinstance`·별표 풀기·`with`·`is`·데코레이터·클래스(상태 형식 말고)·모델·파일 쓰기.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch23-persistence/notebooks"
FIGS = ROOT / "textbook/part6/ch23-persistence/figures"
SLUG = "01-체크포인터와-스레드"
TITLE_TEXT = "체크포인터와 스레드"
SRC = ROOT / "textbook/part6/ch23-persistence/_src" / (SLUG + ".html")
# 교재 출력을 만든 실행의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답)에서 읽은 값
RUNSEC = os.environ.get("AUTHOR01_RUNSEC", "5초 안에")

INSTALL = install_source(["langgraph==1.2.11", "langgraph-checkpoint==4.2.0"])

IMPORTS = r'''# 상태 형식과 그래프를 만들 이름(Ch 13 01·02절)과, 체크포인터 하나를 가져옵니다
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
# 체크포인트를 이 프로그램의 메모리에 담아 두는 체크포인터입니다
from langgraph.checkpoint.memory import InMemorySaver

print("이 절에서 새로 가져온 이름:", "InMemorySaver")'''

FOLDER = r'''# 파일이 생기는지 볼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다(Ch 4 03절과 같은 모양)
import os
import tempfile

# mkdtemp()는 운영체제 임시 폴더 안에 새 폴더를 만들고, 그 폴더의 위치를 글로 내놓습니다
practice_folder = tempfile.mkdtemp(prefix="ch23-01-")
# chdir()는 터미널의 cd처럼 현재 작업 폴더를 옮깁니다
os.chdir(practice_folder)
print("임시 폴더 이름에 ch23-01-이 들어 있는가:", "ch23-01-" in practice_folder)
print("현재 작업 폴더의 파일:", os.listdir())'''

STATE = r'''# 합계·이번 수·실행 흔적 칸을 둔 상태 형식을 만듭니다(실행 흔적 칸에만 Ch 13 02절 이어 붙이기 규칙)
class CountState(TypedDict):
    total: int
    amount: int
    trace: Annotated[list[str], operator.add]'''

NODE = r'''# 합계 칸에 이번 수를 더한 값과, 실행 흔적에 넣을 자기 이름을 냅니다
def add_amount(state):
    new_total = state["total"] + state["amount"]
    # 규칙을 적은 실행 흔적 칸에는 자기 몫 한 칸만 냅니다(Ch 13 02절)
    return {"total": new_total, "trace": ["add"]}'''

HAND = r'''# 노드 함수도 보통 함수입니다. 손으로 만든 상태를 넣어 그래프 없이 직접 불러 봅니다
hand_state = {"total": 3, "amount": 4, "trace": ["add"]}
hand_update = add_amount(hand_state)
print("add_amount가 낸 갱신:", hand_update)'''

PLAIN_BUILD = r'''# 노드 하나와 엣지 둘을 설계 객체에 적고, 먼저 체크포인터 없이 컴파일합니다(Ch 13 01절 모양)
builder = StateGraph(CountState)
builder.add_node("add", add_amount)
builder.add_edge(START, "add")
builder.add_edge("add", END)
plain_graph = builder.compile()
print("컴파일 결과의 종류:", type(plain_graph).__name__)
# 속성 checkpointer에는 그래프에 붙은 체크포인터가 들어 있습니다
print("붙은 체크포인터:", plain_graph.checkpointer)'''

PLAIN_FIRST = r'''# 체크포인터 없는 그래프에 합계 0과 이번 수 3을 넣어 실행합니다
plain_first = plain_graph.invoke({"total": 0, "amount": 3, "trace": []})
print("첫 실행 결과:", plain_first)'''

PLAIN_SECOND = r'''# 같은 그래프에 이번 수 4만 넣어 다시 실행합니다(이 셀만 올라온 오류를 받아 출력합니다)
try:
    plain_graph.invoke({"amount": 4})
except KeyError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:", error)'''

MEMORY = r'''# 체크포인터 하나를 만들고, 3절의 설계 객체를 이 체크포인터와 함께 다시 컴파일합니다
memory = InMemorySaver()
graph = builder.compile(checkpointer=memory)
print("체크포인터의 종류:", type(memory).__name__)
print("붙은 체크포인터의 종류:", type(graph.checkpointer).__name__)'''

CONFIG_A = r'''# 설정 딕셔너리의 키 configurable 아래에 스레드 이름 thread_id를 적습니다
config_a = {"configurable": {"thread_id": "customer-a"}}
print("스레드 customer-a의 설정:", config_a)'''

FIRST = r'''# 스레드 customer-a로 첫 실행을 합니다(입력은 3절 첫 실행과 같음)
first_result = graph.invoke({"total": 0, "amount": 3, "trace": []}, config_a)
print("첫 실행 결과:", first_result)'''

SECOND = r'''# 같은 스레드로 이번 수 4만 넣어 다시 실행합니다(입력은 3절 둘째 실행과 같음)
second_result = graph.invoke({"amount": 4}, config_a)
print("둘째 실행 결과:", second_result)
# 저장된 합계 3에서 이어 가므로, 실행마다 같아야 하는 값입니다
assert second_result["total"] == 7, "같은 스레드의 둘째 실행은 합계 7이어야 합니다"'''

GET_STATE = r'''# 스레드 customer-a의 마지막 체크포인트를 읽습니다(get_state는 체크포인트 하나를 담은 객체를 내놓음)
saved_a = graph.get_state(config_a)
print("읽은 것의 종류:", type(saved_a).__name__)
print("저장된 칸 값:", saved_a.values)
print("다음에 실행할 노드:", saved_a.next)
print("단계 번호:", saved_a.metadata["step"])'''

DEF_HISTORY = r'''# 체크포인트 목록을 받아, 하나마다 단계 번호·만든 자리·다음 노드·칸 값을 한 줄로 출력합니다(내놓는 값 없음)
def print_history(history):
    print("단계 번호 | 만든 자리 | 다음 노드 | 칸 값")
    for snapshot in history:
        step = snapshot.metadata["step"]
        source = snapshot.metadata["source"]
        print(step, "|", source, "|", snapshot.next, "|", snapshot.values)'''

HISTORY_A = r'''# 스레드 customer-a의 체크포인트 목록을 받아 수를 세고, 한 줄씩 봅니다(목록은 최신 것부터)
history_a = list(graph.get_state_history(config_a))
print("customer-a의 체크포인트 수:", len(history_a))
print_history(history_a)
# 실행 두 번에 셋씩이라, 실행마다 같아야 하는 수입니다
assert len(history_a) == 6, "customer-a의 체크포인트는 여섯이어야 합니다"'''

CONFIG_B = r'''# 값 바꿔 보기: 스레드 이름만 customer-b로 바꾸고, 새 스레드라 합계 0부터 넣습니다
config_b = {"configurable": {"thread_id": "customer-b"}}
other_result = graph.invoke({"total": 0, "amount": 4, "trace": []}, config_b)
print("customer-b 실행 결과:", other_result)'''

HISTORY_B = r'''# 스레드 customer-b의 체크포인트 수와, customer-a의 마지막 합계를 다시 봅니다
history_b = list(graph.get_state_history(config_b))
print("customer-b의 체크포인트 수:", len(history_b))
again_a = graph.get_state(config_a)
print("customer-a의 마지막 합계:", again_a.values["total"])'''

MISSING = r'''# 한 번도 실행하지 않은 스레드 이름으로 마지막 체크포인트를 읽어 봅니다
config_new = {"configurable": {"thread_id": "customer-new"}}
empty_state = graph.get_state(config_new)
print("저장된 칸 값:", empty_state.values)
print("다음에 실행할 노드:", empty_state.next)'''

C_FIRST = r'''# 값 바꿔 보기: 새 스레드 customer-c에 customer-a 첫 실행과 같은 입력을 넣습니다
config_c = {"configurable": {"thread_id": "customer-c"}}
third_first = graph.invoke({"total": 0, "amount": 3, "trace": []}, config_c)
print("customer-c 첫 실행 결과:", third_first)'''

C_SECOND = r'''# 둘째 실행 입력에 합계 칸 total 0도 함께 넣습니다(customer-a 둘째 실행과 다른 값은 이것 하나)
third_second = graph.invoke({"total": 0, "amount": 4}, config_c)
print("customer-c 둘째 실행 결과:", third_second)'''

C_HISTORY = r'''# 스레드 customer-c의 체크포인트 목록에서, 합계 칸이 어느 단계에서 바뀌었는지 봅니다
history_c = list(graph.get_state_history(config_c))
print("customer-c의 체크포인트 수:", len(history_c))
print_history(history_c)'''

NO_THREAD = r'''# 설정 딕셔너리 없이, 체크포인터를 붙인 그래프를 불러 봅니다(이 셀만 올라온 오류를 받아 출력합니다)
try:
    graph.invoke({"total": 0, "amount": 1, "trace": []})
except ValueError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:", error)'''

NEW_SAVER = r'''# 체크포인터를 새로 하나 만들어 같은 설계 객체로 컴파일하고, 스레드 customer-a를 읽어 봅니다
fresh_graph = builder.compile(checkpointer=InMemorySaver())
fresh_state = fresh_graph.get_state(config_a)
print("저장된 칸 값:", fresh_state.values)
print("다음에 실행할 노드:", fresh_state.next)'''

FILES = r'''# 지금까지 실행하는 동안 작업 폴더에 파일이 생겼는지 봅니다
file_names = os.listdir()
print("현재 작업 폴더의 파일:", file_names)
print("파일 수:", len(file_names))'''

DEF_ROW = r'''# 스레드 이름 하나로 마지막 체크포인트와 목록을 읽어, 기록 한 줄(한국어 키 딕셔너리)을 만듭니다
def thread_row(compiled_graph, thread_name):
    config = {"configurable": {"thread_id": thread_name}}
    saved = compiled_graph.get_state(config)
    history = list(compiled_graph.get_state_history(config))
    row = {"스레드": thread_name, "합계": saved.values["total"]}
    row["실행 흔적"] = saved.values["trace"]
    row["체크포인트 수"] = len(history)
    return row'''

ROWS = r'''# 세 스레드의 기록 줄을 목록에 담습니다
thread_rows = []
thread_rows.append(thread_row(graph, "customer-a"))
thread_rows.append(thread_row(graph, "customer-b"))
thread_rows.append(thread_row(graph, "customer-c"))
print("담은 기록 줄 수:", len(thread_rows))'''

TABLE = r'''# 스레드·합계·실행 흔적·체크포인트 수를 라벨 줄 아래에 차례로 출력합니다
print("스레드 | 합계 | 실행 흔적 | 체크포인트 수")
for row in thread_rows:
    print(row["스레드"], "|", row["합계"], "|", row["실행 흔적"], "|", row["체크포인트 수"])'''

FIG1 = "01-1-스레드마다-따로-쌓이는-체크포인트"
FIG1_ALT = os.environ.get("AUTHOR01_FIG1_ALT", "위에서 아래로 내려가는 흐름도입니다. 맨 위 초록 상자 설정 딕셔너리 키 configurable 아래 thread_id에서 invoke의 둘째 인자라고 적힌 화살표가 회색 상자 그래프 graph 체크포인터를 붙여 컴파일로 갑니다. 그래프에서 단계를 마칠 때마다 저장이라고 적힌 화살표가 회색 상자 체크포인터 InMemorySaver 이 프로그램의 메모리에 저장으로 갑니다. 체크포인터에서 점선 두 갈래가 나가, thread_id가 customer-a이면 노란 상자 스레드 customer-a 체크포인트 여섯 합계 7로, thread_id가 customer-b이면 노란 상자 스레드 customer-b 체크포인트 셋 합계 4로 가는 그림")
FIG1_CAP = "체크포인터 하나가 스레드 이름마다 체크포인트 줄을 따로 두어, customer-a에는 여섯 개와 합계 7, customer-b에는 세 개와 합계 4가 남았습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 우리가 넘긴 값이고, 회색 상자는 라이브러리가 만든 그래프와 체크포인터입니다.
노란 상자는 노트북 8·9절에서 출력으로 확인한 값입니다.
체크포인터에서 나가는 두 점선은 스레드 이름에 따라 저장할 줄을 고르는 자리입니다."""

FIG2 = "01-2-체크포인터가-없을-때와-있을-때"
FIG2_ALT = os.environ.get("AUTHOR01_FIG2_ALT", "맨 위 파란 상자 같은 설계 객체 builder 노드 add 함수 add_amount에서 칸 둘로 화살표가 갑니다. 왼쪽 칸 체크포인터 없이 컴파일에는 노란 상자 첫 실행 total 0 amount 3 합계 3 아래로 노란 상자 둘째 실행 amount 4만 받은 오류 KeyError가 있습니다. 오른쪽 칸 체크포인터를 붙이고 스레드 customer-a에는 노란 상자 첫 실행 total 0 amount 3 합계 3 아래로 노란 상자 둘째 실행 amount 4만 합계 7 실행 흔적 두 칸이 있는 그림")
FIG2_CAP = "같은 설계 객체에 같은 두 입력을 넣었는데, 체크포인터가 없으면 둘째 실행에서 KeyError를 받고 있으면 합계 7이 됩니다."
FIG2_READ = """맨 위 파란 상자는 노트북 3절에서 우리가 적은 설계 객체이고, 두 칸이 이 객체를 함께 씁니다.
왼쪽 칸은 3절, 오른쪽 칸은 5·6절 출력이고, 칸 안은 위에서 아래로 읽습니다.
두 칸의 첫 실행 입력은 서로 같고, 둘째 실행 입력도 서로 같습니다.
왼쪽 아래 오류는 셀에서 받아 출력한 오류라 노란 상자로 그렸습니다."""

FIG3 = "01-3-같은-스레드의-체크포인트-여섯"
FIG3_ALT = os.environ.get("AUTHOR01_FIG3_ALT", "칸 둘이 왼쪽에서 오른쪽으로 놓인 그림입니다. 왼쪽 칸 첫 실행 입력 total 0 amount 3에는 노란 상자 셋이 위에서 아래로 놓입니다. 단계 -1 input 다음 __start__ 실행 흔적 빈 목록만, 단계 0 loop 다음 add 합계 0 이번 수 3, 단계 1 loop 다음 없음 합계 3입니다. 오른쪽 칸 둘째 실행 입력 amount 4에는 단계 2 input 다음 __start__ 합계 3 이번 수 3, 단계 3 loop 다음 add 합계 3 이번 수 4, 단계 4 loop 다음 없음 합계 7이 있습니다. 왼쪽 칸에서 오른쪽 칸으로 화살표 하나가 가는 그림")
FIG3_CAP = "스레드 customer-a의 체크포인트 여섯을 오래된 것부터 놓으면, 실행 한 번에 셋씩 쌓여 단계 4에서 합계 7이 됩니다."
FIG3_READ = """왼쪽 칸이 첫 실행, 오른쪽 칸이 둘째 실행이고, 칸 안은 위에서 아래로 읽습니다.
노트북 8절은 최신 것부터 출력했는데, 그림은 오래된 것부터 놓았습니다.
노란 상자는 모두 8절 출력의 한 줄이고, 「다음 없음」은 빈 튜플 `()`입니다.
단계 2 상자는 둘째 입력을 넣기 전이라, 이번 수가 아직 3입니다."""

FIG4 = "01-4-세-스레드의-마지막-상태"
FIG4_ALT = os.environ.get("AUTHOR01_FIG4_ALT", "칸 셋이 나란히 놓이고 아래에 회색 상자 하나가 있는 그림입니다. 칸 customer-a에는 초록 상자 둘째 입력 amount 4 아래 노란 상자 합계 7 실행 흔적 두 칸 체크포인트 여섯이 있습니다. 칸 customer-b에는 초록 상자 한 번뿐인 입력 total 0 amount 4 아래 노란 상자 합계 4 실행 흔적 한 칸 체크포인트 셋이 있습니다. 칸 customer-c에는 초록 상자 둘째 입력 total 0 amount 4 아래 노란 상자 합계 4 실행 흔적 두 칸 체크포인트 여섯이 있습니다. 아래 회색 상자에는 세 스레드 모두 같은 graph와 memory, a와 c의 첫 입력은 total 0 amount 3이라고 적힌 그림")
FIG4_CAP = "같은 그래프와 체크포인터에서도 스레드마다 합계가 따로 남았고, 둘째 입력에 합계 0을 넣은 customer-c는 7이 아니라 4가 되었습니다."
FIG4_READ = """칸 셋이 스레드 셋이고, 칸 안은 위에서 아래로 읽습니다.
초록 상자는 마지막으로 넣은 입력이고, 노란 상자는 노트북 12절 출력입니다.
맨 아래 회색 상자의 앞 두 줄은 세 칸 모두에 해당하는 사실입니다. 뒤 두 줄은 a와 c 칸에만 해당합니다.
왼쪽 칸과 오른쪽 칸은 둘째 입력의 `total` 0 하나만 다릅니다."""

ILLU = "01-5-판마다-따로-쌓이는-즉석사진"
ILLU_ALT = os.environ.get("AUTHOR01_ILLU_ALT", "흰 바탕에 나무 탁자 둘이 왼쪽과 오른쪽에 떨어져 놓인 그림입니다. 두 탁자 위에는 체스 말이 몇 개 선 체스판이 하나씩 있고, 판의 일부는 그림 가장자리에서 잘려 있습니다. 왼쪽 탁자의 체스판 앞에는 작은 체스판이 찍힌 즉석사진 여섯 장이 세 장씩 두 줄로 놓여 있습니다. 오른쪽 탁자의 체스판 앞에는 같은 즉석사진 세 장이 한 줄로 놓여 있습니다. 두 탁자 사이 바닥에는 회색 즉석카메라 하나가 있는 그림")
ILLU_CAP = os.environ.get("AUTHOR01_ILLU_CAP", "사진을 판마다 따로 두어, 왼쪽 판 앞에는 여섯 장, 오른쪽 판 앞에는 세 장이 놓였습니다.")
ILLU_READ = os.environ.get("AUTHOR01_ILLU_READ", "왼쪽과 오른쪽 나무 탁자 위에 체스판이 하나씩 있습니다. 왼쪽 판 앞에는 즉석사진 여섯 장이 세 장씩 두 줄로, 오른쪽 판 앞에는 세 장이 한 줄로 놓였습니다. 사진은 섞이지 않고 제 판 앞에만 있고, 두 탁자 사이 바닥에는 카메라 하나만 있습니다. 왼쪽 여섯 장이 스레드 <code>customer-a</code>의 체크포인트 여섯, 오른쪽 세 장이 <code>customer-b</code>의 셋이고, 카메라가 체크포인터 하나입니다. 체스 말의 개수와 자리, 판이 그림 가장자리에서 잘린 것은 코드의 무엇과도 짝짓지 않습니다.")

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 체크포인터 없이 두 번 실행한 그래프와, 체크포인터를 붙여 같은 스레드로 두 번 실행한 그래프를 견줍니다.
2. 저장된 상태와 체크포인트 목록을 읽어, 무엇이 몇 개 저장됐는지 셉니다.
3. 스레드 이름이나 입력 칸 하나를 바꿔, 스레드마다 상태가 따로 쌓이는 것을 확인합니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
그래서 `.env` 파일을 읽는 셀과 키를 확인하는 셀이 없습니다.
이 챕터는 상태를 저장하고 이어 가는 일이 주제입니다.
매번 같은 값을 내는 우리 노드로 그래프를 만들어야, 저장된 값이 맞는지 출력으로 가를 수 있습니다.

노트북은 빈 임시 폴더를 만들어 그 폴더에서 실행합니다.
이 절의 체크포인터는 파일을 쓰지 않고, 읽어 오는 자료 파일도 없습니다.
교재 출력을 만든 실행에서는 노트북 전체가 """ + RUNSEC + """ 끝났습니다.
설치 셀에 걸리는 시간은 네트워크에 따라 달라집니다.

**기준 버전** — 첫 셀에서 패키지 둘을 설치합니다.
판은 langgraph 1.2.11과, 체크포인터가 들어 있는 langgraph-checkpoint 4.2.0입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~8절을 읽습니다.
체크포인터를 붙이기 전과 뒤를 견주고, 저장된 것을 세는 자리입니다.
9~12절은 스레드 이름과 입력 칸을 바꿔 보는 자리이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch23-persistence`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

Ch 21까지의 그래프는 실행이 끝나면 상태를 따로 남기지 않았습니다.
이 챕터는 실행 중 상태를 저장해 두었다가, 다음 실행에서 이어 쓰는 법을 배웁니다.
챕터 제목의 Persistence는 실행이 끝난 뒤에도 상태를 남겨 두는 일(상태 저장)입니다.
제목의 Durable Execution은 멈춘 실행을 저장된 자리부터 다시 이어 가는 일(이어 실행)입니다.
이 절은 그 첫걸음으로, 상태를 저장하는 부품과 저장된 상태를 나누는 이름을 봅니다.

첫 셀은 패키지 둘을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langgraph: 1.2.11`·`langgraph-checkpoint: 4.2.0`이 보입니다.
두 판 모두 실습 폴더 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
상태 형식과 그래프를 만드는 이름은 Ch 13 01·02절과 같습니다.
새로 가져오는 이름은 체크포인터 `InMemorySaver` 하나이고, 뜻은 4절에서 풉니다.
모델을 부르지 않는 절이라, Ch 20 03절처럼 모델과 메시지 이름은 가져오지 않습니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `이 절에서 새로 가져온 이름: InMemorySaver`가 보입니다.
이 이름은 모듈 `langgraph.checkpoint.memory`에 있고, 첫 셀에서 설치한 langgraph-checkpoint에 들어 있습니다.

다음 셀은 Ch 4 03절처럼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다.
이 챕터의 뒤 절들은 체크포인트를 파일에 씁니다.
실습 폴더에 파일을 남기지 않으려고, 모든 절이 이 모양으로 빈 임시 폴더에서 시작합니다.
이 절의 체크포인터는 파일을 쓰지 않는데, 11절에서 폴더가 그대로 비어 있는지 봅니다.

폴더 위치는 컴퓨터마다 달라 출력하지 않고, 폴더 이름에 붙인 앞머리만 확인합니다.
모듈 `os`와 `tempfile`은 Python에 들어 있는 기능 묶음입니다."""),
        setup(FOLDER),
        md("""**결과 읽기** — 출력 줄 `임시 폴더 이름에 ch23-01-이 들어 있는가: True`로, 이 절의 폴더를 만들었습니다.
출력 줄 `현재 작업 폴더의 파일: []`로, 빈 폴더에서 시작합니다.

## 2. 상태 형식과 노드

이 절의 그래프는 수를 이어 더하는 작은 그래프입니다.
다음 셀은 상태 형식입니다.
칸 `total`은 지금까지의 합계, 칸 `amount`는 이번에 더할 수입니다.
칸 `trace`는 Ch 13 01절의 실행 흔적이고, 이 칸에만 Ch 13 02절 규칙 `operator.add`를 적습니다.
나머지 두 칸은 규칙이 없어, 새 값이 오면 덮어씁니다."""),
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
상태 형식 이름은 Ch 13 약속대로 칸 구성에 맞춰 새로 붙인 `CountState`입니다.

다음 셀은 노드 함수입니다.
합계 칸에 이번 수를 더한 값과, 실행 흔적에 넣을 자기 이름 `"add"`를 냅니다."""),
        code(NODE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `add_amount`는 칸 `amount`를 읽기만 하고, 갱신에는 넣지 않습니다.

Ch 13 01절처럼 다음 셀은 이 노드 함수를 그래프 없이 직접 불러 봅니다.
손으로 만든 상태의 합계는 3, 이번 수는 4입니다."""),
        code(HAND),
        md("""**결과 읽기** — 출력 줄 `add_amount가 낸 갱신: {'total': 7, 'trace': ['add']}`입니다.
합계 3에 4를 더한 7과, 실행 흔적 한 칸이 갱신에 들어 있습니다.
노드 함수는 받은 상태만 보고 계산하므로, 같은 상태를 넣으면 늘 같은 갱신을 냅니다.

## 3. 체크포인터 없이 두 번 실행하기

먼저 Ch 13 01절 모양 그대로, 체크포인터 없이 그래프를 만듭니다.
다음 셀은 노드 하나와 엣지 둘을 설계 객체에 적고 컴파일합니다.
마지막 줄은 그래프에 체크포인터가 붙었는지 봅니다."""),
        code(PLAIN_BUILD),
        md("""**결과 읽기** — 출력 줄 `컴파일 결과의 종류: CompiledStateGraph`는 Ch 13 01절과 같습니다.
출력 줄 `붙은 체크포인터: None`으로, 이 그래프에는 체크포인터가 없습니다.
값 `None`은 Python에서 「값이 없음」을 뜻합니다.

다음 셀은 합계 0과 이번 수 3을 넣어 실행합니다."""),
        code(PLAIN_FIRST),
        md("""**결과 읽기** — 출력 줄 `첫 실행 결과: {'total': 3, 'amount': 3, 'trace': ['add']}`입니다.
합계 칸이 0에서 3이 되었고, 실행 흔적에 `add`가 한 칸 남았습니다.

다음 셀은 같은 그래프에 이번 수 4만 넣어 다시 실행합니다.
실행 전에 예상해 봅니다.
앞 실행의 합계 3이 남아 있다면 7이 나올 것입니다.
이 셀만 올라온 오류를 받아 출력하고, 셀은 끝까지 갑니다.
오류를 받는 `try`·`except`는 Ch 2 05절에서 배웠습니다."""),
        code(PLAIN_SECOND),
        md("""**결과 읽기** — 출력 줄 `받은 오류: KeyError`와 `오류 글: 'total'`입니다.
노드 함수가 칸 `total`을 찾았는데, 상태에 그 칸이 없었다는 뜻입니다.
둘째 실행은 넣은 칸 `amount` 하나만 가진 상태에서 시작했습니다.
체크포인터가 없는 그래프는 실행이 끝나면 상태를 남기지 않기 때문입니다.
Ch 21 03절에서도 결과 상태는 실행 한 번 안에서만 보았습니다.

## 4. 체크포인터를 붙여 컴파일하기

체크포인터(checkpointer)는 그래프가 단계를 하나 마칠 때마다 그때의 상태를 저장해 두는 부품입니다.
체스 판을 한 수마다 사진으로 찍어 두는 카메라와 사진첩에 견줄 수 있습니다.
이 절에서는 클래스 `InMemorySaver`로 만든 체크포인터를, 메서드 `compile`의 인자 `checkpointer`로 넘깁니다.
단계는 Ch 20 03절에서 본, 그래프가 노드를 골라 한 번 실행하는 차례입니다.

클래스 `InMemorySaver`는 저장한 것을 이 Python 프로그램(커널)의 메모리에 둡니다.
다음 셀은 체크포인터를 만들고, 3절의 설계 객체를 이 체크포인터와 함께 다시 컴파일합니다.
설계 객체는 그대로이고, 컴파일할 때 넘긴 인자 하나만 다릅니다."""),
        code(MEMORY),
        md("""**결과 읽기** — 출력 줄 `체크포인터의 종류: InMemorySaver`입니다.
출력 줄 `붙은 체크포인터의 종류: InMemorySaver`로, 새 그래프에 이 체크포인터가 붙었습니다.
이름 `graph`가 체크포인터를 붙인 그래프이고, `plain_graph`는 3절의 체크포인터 없는 그래프입니다.

## 5. 스레드 이름과 첫 실행

스레드(thread)는 한 이름으로 묶인 체크포인트들의 줄입니다.
판 하나 앞에 그 판의 사진만 모아 둔 것과 같습니다.
스레드 이름은 설정 딕셔너리에 적어, 메서드 `invoke`의 둘째 인자로 넘깁니다.
설정 딕셔너리는 Ch 20 03절에서 실행 한도 `recursion_limit`을 적은 그 딕셔너리입니다.
이번에는 키 `configurable` 아래에 딕셔너리를 하나 더 두고, 그 안에 스레드 이름 `thread_id`를 적습니다."""),
        code(CONFIG_A),
        md("""**결과 읽기** — 출력 줄 `스레드 customer-a의 설정: {'configurable': {'thread_id': 'customer-a'}}`입니다.
스레드 이름은 우리가 정하는 글이고, 이 절에서는 `customer-a`로 정했습니다.
설정 딕셔너리는 상태에 들어가지 않습니다.

다음 셀은 이 설정으로 첫 실행을 합니다.
입력은 3절 첫 실행과 같은 합계 0과 이번 수 3입니다."""),
        code(FIRST),
        md("""**결과 읽기** — 출력 줄 `첫 실행 결과: {'total': 3, 'amount': 3, 'trace': ['add']}`는 3절 첫 실행과 같습니다.
체크포인터를 붙여도 한 번의 실행 결과는 달라지지 않았습니다.
달라진 것은 이 실행의 상태가 스레드 `customer-a`에 저장된 것이고, 7·8절에서 읽습니다.

## 6. 같은 스레드로 한 번 더 실행하기

다음 셀은 3절 둘째 실행처럼 이번 수 4만 넣고, 같은 설정 `config_a`로 실행합니다.
실행 전에 예상해 봅니다.
체크포인터가 스레드 `customer-a`의 마지막 상태를 꺼내 오면, 합계 3에 4를 더해 7이 될 것입니다.
셀 끝 `assert`는 실행마다 같아야 하는 합계에만 겁니다."""),
        code(SECOND),
        md("""**결과 읽기** — 출력 줄 `둘째 실행 결과: {'total': 7, 'amount': 4, 'trace': ['add', 'add']}`입니다.
합계가 저장된 3에서 이어져 7이 되었고, 3절에서 받은 `KeyError`는 나지 않았습니다.
실행 흔적 칸은 첫 실행의 `add` 뒤에 둘째 실행의 `add`가 붙어 두 칸입니다.
넣은 칸 `amount`는 4로 바뀌었고, 넣지 않은 칸 `total`은 저장된 값에서 시작했습니다.

## 7. 저장된 상태 읽기

메서드 `get_state`는 설정 딕셔너리를 받아, 그 스레드의 마지막 체크포인트를 객체 하나로 내놓습니다.
그 객체의 속성 `values`는 저장된 칸 값이고, `next`는 다음에 실행할 노드 이름들입니다.
속성 `metadata`는 체크포인트에 붙은 정보이고, 키 `step`에 단계 번호가 들어 있습니다."""),
        code(GET_STATE),
        md("""**결과 읽기** — 출력 줄 `읽은 것의 종류: StateSnapshot`입니다.
출력 줄 `저장된 칸 값: {'total': 7, 'amount': 4, 'trace': ['add', 'add']}`는 6절 둘째 실행 결과와 같습니다.
출력 줄 `다음에 실행할 노드: ()`는 빈 튜플이라, 이어서 실행할 노드가 없다는 뜻입니다.
출력 줄 `단계 번호: 4`는 다음 8절 목록의 맨 위 줄과 같은 번호입니다.

## 8. 체크포인트 목록 세기

체크포인트(checkpoint)는 체크포인터가 한 번 저장한 상태 하나입니다.
사진첩의 사진 한 장과 같습니다.
메서드 `get_state_history`는 한 스레드의 체크포인트를 최신 것부터 차례로 내놓습니다.
내놓은 것을 함수 `list`로 목록에 담으면 수를 셀 수 있습니다.

다음 셀은 체크포인트 목록을 받아 한 줄씩 출력하는 함수입니다.
한 줄에는 단계 번호, 만든 자리(키 `source`), 다음 노드, 칸 값을 적습니다.
목록의 항목은 7절에서 읽은 객체와 같은 종류입니다."""),
        code(DEF_HISTORY),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `print_history`는 인자로 받은 목록만 읽고, 노트북의 다른 이름에 기대지 않습니다.

다음 셀은 스레드 `customer-a`의 체크포인트 목록을 받아 수를 세고, 이 함수로 봅니다.
실행 전에 예상해 봅니다.
실행을 두 번 했으니, 체크포인트도 둘 이상일 것입니다.
셀 끝 `assert`는 실행마다 같아야 하는 체크포인트 수에만 겁니다."""),
        code(HISTORY_A),
        md("""**결과 읽기** — 출력 줄 `customer-a의 체크포인트 수: 6`입니다.
라벨 줄 `단계 번호 | 만든 자리 | 다음 노드 | 칸 값` 아래 여섯 줄이 최신 것부터 놓였습니다.
맨 아래 줄 `-1 | input | ('__start__',) | {'trace': []}`는 첫 입력을 받은 때의 체크포인트입니다.
맨 위 줄은 7절에서 읽은 마지막 체크포인트이고, 단계 번호가 `4`입니다.

한 번 실행할 때마다 체크포인트가 셋씩 쌓였습니다.
첫 실행은 단계 -1·0·1, 둘째 실행은 단계 2·3·4입니다.
셋은 입력을 받은 때, 입력을 칸에 넣은 뒤, 노드 `add`를 마친 뒤입니다.
입력을 받은 때의 체크포인트는 첫 단계 0보다 앞이라, 번호가 -1입니다.
만든 자리는 첫째가 `input`이고, 나머지 둘이 `loop`입니다.

단계 2 줄의 칸 값은 둘째 입력을 넣기 전 값이라, 이번 수가 아직 3입니다.
다음 노드 `__start__`는 Ch 13 01절의 가상 시작점이고, 입력을 칸에 넣을 차례라는 뜻입니다.

## 9. 값 바꿔 보기 · 스레드 이름만 바꾸기

바꿀 값은 설정 딕셔너리의 스레드 이름 하나입니다.
이번 수는 6절 둘째 실행과 같은 4를 넣습니다.
새 스레드에는 저장된 합계가 없어, 3절처럼 오류가 나지 않게 합계 0도 함께 넣습니다.
실행 전에 예상해 봅니다.
스레드 `customer-b`는 스레드 `customer-a`의 합계 7을 읽지 않아, 결과 합계가 4일 것입니다."""),
        code(CONFIG_B),
        md("""**결과 읽기** — 출력 줄 `customer-b 실행 결과: {'total': 4, 'amount': 4, 'trace': ['add']}`입니다.
합계가 0에서 시작해 4가 되었고, 실행 흔적도 한 칸입니다.
같은 그래프 `graph`와 같은 체크포인터를 썼지만, 스레드 `customer-a`의 값은 섞이지 않았습니다.

다음 셀은 스레드 `customer-b`의 체크포인트 수와, 스레드 `customer-a`의 마지막 합계를 다시 봅니다."""),
        code(HISTORY_B),
        md("""**결과 읽기** — 출력 줄 `customer-b의 체크포인트 수: 3`으로, 실행 한 번의 체크포인트 셋입니다.
출력 줄 `customer-a의 마지막 합계: 7`로, 스레드 `customer-b`를 실행한 뒤에도 그대로입니다.
체크포인터 하나가 스레드 이름마다 체크포인트 줄을 따로 두었습니다.

다음 셀은 한 번도 실행하지 않은 스레드 이름 `customer-new`로 마지막 체크포인트를 읽어 봅니다."""),
        code(MISSING),
        md("""**결과 읽기** — 출력 줄 `저장된 칸 값: {}`과 `다음에 실행할 노드: ()`입니다.
체크포인트가 없는 스레드는 빈 딕셔너리를 내놓았고, 오류는 나지 않았습니다.
그래서 스레드 이름을 잘못 적으면, 오류 없이 빈 상태를 읽게 됩니다.

## 10. 값 바꿔 보기 · 둘째 입력에 합계 칸도 넣기

6절에서 넣지 않은 칸 `total`은 저장된 값에서 시작했습니다.
이번에는 둘째 실행 입력에 합계 칸도 넣으면 어떻게 되는지 봅니다.
다음 셀은 새 스레드 `customer-c`에 먼저 스레드 `customer-a` 첫 실행과 같은 입력을 넣습니다."""),
        code(C_FIRST),
        md("""**결과 읽기** — 출력 줄 `customer-c 첫 실행 결과: {'total': 3, 'amount': 3, 'trace': ['add']}`는 5절 첫 실행과 같습니다.

바꿀 값은 둘째 실행 입력에 더한 합계 칸 `total` 0 하나입니다.
실행 전에 예상해 봅니다.
Ch 13 02절에서 본 것처럼, 규칙 없는 칸은 새로 들어온 값으로 덮어씁니다.
체크포인터가 저장된 합계 3을 꺼내 와도, 입력의 0이 그 값을 덮어쓸 것입니다.
그러면 합계는 0에 4를 더한 4가 되고, 실행 흔적 칸은 두 칸이 될 것입니다."""),
        code(C_SECOND),
        md("""**결과 읽기** — 출력 줄 `customer-c 둘째 실행 결과: {'total': 4, 'amount': 4, 'trace': ['add', 'add']}`입니다.
예상대로 합계는 4이고, 실행 흔적은 두 칸입니다.
같은 스레드로 다시 실행해도, 입력에 적은 규칙 없는 칸은 저장된 값 대신 입력 값에서 시작했습니다.

다음 셀은 스레드 `customer-c`의 체크포인트 목록에서, 합계 칸이 어느 단계에서 바뀌었는지 봅니다."""),
        code(C_HISTORY),
        md("""**결과 읽기** — 출력 줄 `customer-c의 체크포인트 수: 6`은 스레드 `customer-a`와 같은 수입니다.
단계 2 줄의 합계는 3이고, 단계 3 줄 `3 | loop | ('add',) | {'total': 0, 'amount': 4, 'trace': ['add']}`에서 0이 되었습니다.
입력을 칸에 넣는 자리에서, 저장된 3이 입력의 0으로 덮어써졌습니다.
그 뒤 노드 `add`가 0에 4를 더해, 단계 4에서 합계 4가 되었습니다.

## 11. 스레드 이름이 없을 때와 새 체크포인터

다음 셀은 설정 딕셔너리 없이, 체크포인터를 붙인 그래프를 불러 봅니다.
실행 전에 예상해 봅니다.
저장할 스레드를 알 수 없으니 오류가 날 것입니다.
이 셀만 올라온 오류를 받아 출력하고, 셀은 끝까지 갑니다."""),
        code(NO_THREAD),
        md("""**결과 읽기** — 출력 줄 `받은 오류: ValueError`입니다.
오류 글 `Checkpointer requires one or more of the following 'configurable' keys: thread_id, checkpoint_ns, checkpoint_id`를 봅니다.
체크포인터를 쓰려면 키 `configurable` 아래에 이름이 하나 이상 있어야 한다는 뜻입니다.
이 절은 그 가운데 `thread_id`만 쓰고, 나머지 두 이름은 쓰지 않았습니다.

다음 셀은 체크포인터를 새로 하나 만들어, 같은 설계 객체로 다시 컴파일합니다.
그리고 스레드 `customer-a`의 마지막 체크포인트를 읽어 봅니다.
실행 전에 예상해 봅니다.
체크포인트가 체크포인터 객체 안에 저장된다면, 새 체크포인터는 아무것도 모를 것입니다."""),
        code(NEW_SAVER),
        md("""**결과 읽기** — 출력 줄 `저장된 칸 값: {}`과 `다음에 실행할 노드: ()`로, 9절의 처음 보는 스레드와 같습니다.
스레드 이름이 같아도, 체크포인터가 다르면 저장된 체크포인트를 읽지 못했습니다.
체크포인트는 그래프가 아니라, 체크포인터 객체 `memory` 안에 있습니다.
커널을 다시 시작하면 메모리의 이 객체도 사라지는데, 이번에 커널을 다시 시작해 보지는 않았습니다.

다음 셀은 지금까지 실행하는 동안 작업 폴더에 파일이 생겼는지 봅니다."""),
        code(FILES),
        md("""**결과 읽기** — 출력 줄 `현재 작업 폴더의 파일: []`과 `파일 수: 0`입니다.
체크포인터 `InMemorySaver`는 파일을 쓰지 않았습니다.
체크포인트를 데이터베이스나 파일에 남기는 체크포인터는 02·03절에서 씁니다.

## 12. 스레드별로 모아 보기

다음 셀은 스레드 이름 하나로 마지막 체크포인트와 목록을 읽어, 기록 한 줄을 만드는 함수입니다.
Ch 13 01절 `run_row`처럼 한국어 키 딕셔너리 한 줄에 담습니다.
그래프는 인자로 받아, 노트북의 이름 `graph`에 기대지 않습니다."""),
        code(DEF_ROW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `thread_row`는 메서드 `get_state`와 `get_state_history`를 한 번씩 부릅니다.

다음 셀은 세 스레드의 기록 줄을 목록에 담습니다."""),
        code(ROWS),
        md("""**결과 읽기** — 출력 줄 `담은 기록 줄 수: 3`입니다.

다음 셀은 네 칸을 라벨 줄 아래에 차례로 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 `스레드 | 합계 | 실행 흔적 | 체크포인트 수` 아래 세 줄입니다.
줄 `customer-a | 7 | ['add', 'add'] | 6`은 같은 스레드로 두 번 실행한 결과입니다.
줄 `customer-b | 4 | ['add'] | 3`은 스레드 이름만 바꾼 결과입니다.
줄 `customer-c | 4 | ['add', 'add'] | 6`은 둘째 입력에 합계 0을 더 넣은 결과입니다.
세 스레드는 같은 그래프와 같은 체크포인터를 썼지만, 체크포인트 줄은 이름마다 따로입니다.

## 정리

1. 체크포인터를 붙인 그래프를 같은 스레드로 다시 실행하자, 저장된 합계 3에서 이어 7이 되었습니다.
2. 스레드 이름이 다르면 체크포인트 줄도 따로라, 스레드 `customer-b`는 합계 0에서 시작해 4가 되었습니다.
3. 한 번 실행할 때마다 체크포인트가 셋씩 쌓였고, 체크포인터 `InMemorySaver`는 파일을 남기지 않았습니다.

02절에서는 체크포인트를 PostgreSQL 데이터베이스에 저장합니다.
그 전에 체크포인트를 담을 표를 만드는 일부터 봅니다."""),
    ]


def html_text(text: str) -> str:
    """노트북용 마크다운 한 단락(백틱·줄바꿈)을 _src 문단 글로 바꿉니다."""
    parts = text.replace("\n", " ").split("`")
    out = ""
    for index in range(len(parts)):
        if index % 2 == 1:
            out = out + "<code>" + parts[index] + "</code>"
        else:
            out = out + parts[index]
    return out


L_CH02_05 = "../../part1/ch02-python/05-파일과-예외.html"
L_CH04_03 = "../../part1/ch04-data-tools/03-SQL로-조회-함수-만들기.html"
L_CH13_01 = "../../part4/ch13-langgraph-basics/01-StateGraph와-노드-엣지.html"
L_CH13_02 = "../../part4/ch13-langgraph-basics/02-State-갱신.html"
L_CH20_03 = "../../part5/ch20-tool-node/03-recursion-limit과-명시적-종료.html"
L_CH21_03 = "../ch21-create-agent/03-AgentState와-context-schema.html"
L_02 = "02-PostgresSaver-준비와-스키마.html"
L_03 = "03-스레드-재개와-대화-이어가기.html"
L_04 = "04-내구-실행-모드-비교.html"
L_05 = "05-pending-writes와-장애-복구.html"

THREAD_ROWS = [
    ("<code>customer-a</code>", "첫 실행 <code>total</code> 0·<code>amount</code> 3 → 둘째 실행 <code>amount</code> 4", "7", "<code>['add', 'add']</code>", "6"),
    ("<code>customer-b</code>", "한 번 <code>total</code> 0·<code>amount</code> 4", "4", "<code>['add']</code>", "3"),
    ("<code>customer-c</code>", "첫 실행 <code>total</code> 0·<code>amount</code> 3 → 둘째 실행 <code>total</code> 0·<code>amount</code> 4", "4", "<code>['add', 'add']</code>", "6"),
]


def table_html(head: list, rows: list) -> str:
    head_html = ""
    for value in head:
        head_html = head_html + "<th>" + value + "</th>"
    body = ""
    for row in rows:
        cells_html = ""
        for value in row:
            cells_html = cells_html + "<td>" + value + "</td>"
        body = body + "<tr>" + cells_html + "</tr>"
    return "<table><thead><tr>" + head_html + "</tr></thead><tbody>" + body + "</tbody></table>"


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


def src_html() -> str:
    thread_table = table_html(["스레드", "넣은 값", "합계", "실행 흔적", "체크포인트 수"], THREAD_ROWS)
    return """<!--meta: 강의 1h | 실습 1.5h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>체크포인터를 붙인 그래프가 같은 스레드의 다음 실행에서 저장된 상태를 이어 쓰는 것을 출력으로 확인할 수 있습니다.</li>
<li>메서드 <code>get_state</code>와 <code>get_state_history</code>로 저장된 상태와 체크포인트 수를 읽을 수 있습니다.</li>
<li>스레드 이름과 입력 칸을 바꾼 결과로, 스레드마다 상태가 따로 쌓이는 것을 설명할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>지금까지의 그래프는 실행이 끝나면 상태를 따로 남기지 않았습니다. <a href=\"""" + L_CH21_03 + """\">Ch 21 03절</a>에서도 결과 상태는 실행 한 번 안에서만 보았습니다. 그런데 대화를 이어 가는 에이전트는 앞 실행의 상태를 다음 실행에서 이어 써야 합니다. 여러 사람이 같은 그래프를 쓰면, 사람마다 상태를 따로 두어야 합니다.</p><p>챕터 제목의 Persistence는 실행이 끝난 뒤에도 상태를 남겨 두는 일(상태 저장)입니다. 제목의 Durable Execution은 멈춘 실행을 저장된 자리부터 다시 이어 가는 일(이어 실행)입니다. 이 절은 그 첫걸음으로, 상태를 저장하는 부품과 저장된 상태를 나누는 이름을 봅니다. 수를 이어 더하는 작은 그래프로, 합계 3이 다음 실행에서 7이 되는지 셉니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH13_01 + """\">Ch 13 01절</a>에서는 상태 형식·노드·엣지로 그래프를 적고, 컴파일해 실행했습니다. <a href=\"""" + L_CH13_02 + """\">Ch 13 02절</a>에서는 칸에 이어 붙이기 규칙 <code>operator.add</code>를 적었습니다. 규칙을 적지 않은 칸은 새 값으로 덮어쓰는 것도 보았습니다.</p><p><a href=\"""" + L_CH20_03 + """\">Ch 20 03절</a>에서는 메서드 <code>invoke</code>의 둘째 인자인 설정 딕셔너리에 실행 한도를 적었습니다. 그 절에서 그래프가 노드를 골라 한 번 실행하는 차례를 단계라고 불렀습니다. 멈춘 실행을 저장된 자리부터 이어 가는 일은 <a href=\"""" + L_04 + """\">04절</a>과 <a href=\"""" + L_05 + """\">05절</a>에서 다룹니다.</p><p><a href=\"""" + L_CH21_03 + """\">Ch 21 03절</a>에서는 에이전트 그래프의 결과 상태를 실행 한 번 안에서만 보았습니다. 빈 임시 폴더에서 실행하는 준비 셀은 <a href=\"""" + L_CH04_03 + """\">Ch 4 03절</a> 모양입니다. 오류를 받아 출력하는 <code>try</code>·<code>except</code>는 <a href=\"""" + L_CH02_05 + """\">Ch 2 05절</a>에서 배웠습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>체스를 두는 판 두 개가 있다고 합시다. 판마다 수를 둘 때마다 즉석사진을 찍어, 그 판 앞에 모아 둡니다. 판을 치웠다가도 마지막 사진을 보고 말을 다시 놓으면 이어서 둘 수 있습니다. 두 판의 사진은 섞지 않고, 판마다 따로 둡니다.</p><p>사진을 찍어 모아 두는 일을 맡는 것이 체크포인터이고, 사진 한 장이 체크포인트입니다. 판 하나와 그 판 앞의 사진 묶음이 스레드입니다. 이 절의 그래프는 한 번 실행할 때마다 사진을 세 장 남깁니다. 그래서 두 번 실행한 스레드 <code>customer-a</code>에는 여섯 장, 한 번 실행한 <code>customer-b</code>에는 세 장이 쌓입니다.</p>
""" + illustration_block() + """<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>체크포인터(checkpointer)</td><td>그래프가 단계를 하나 마칠 때마다 그때의 상태를 저장해 두는 부품입니다. 판마다 한 수씩 사진을 찍어 두는 카메라와 사진첩과 같습니다. 이 절에서는 <code>InMemorySaver()</code>로 만들어 메서드 <code>compile</code>의 인자 <code>checkpointer</code>로 넘깁니다.</td></tr><tr><td>체크포인트(checkpoint)</td><td>체크포인터가 한 번 저장한 상태 하나입니다. 사진 한 장과 같습니다. 이 절에서는 실행 한 번에 셋씩 쌓였고, 메서드 <code>get_state_history</code>가 최신 것부터 내놓습니다.</td></tr><tr><td>스레드(thread)</td><td>한 이름으로 묶인 체크포인트들의 줄입니다. 판 하나 앞에 그 판의 사진만 모아 둔 것과 같습니다. 이 절에서는 설정 딕셔너리의 <code>thread_id</code>에 적은 <code>customer-a</code>가 스레드 이름입니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 체크포인터는 노트북 4절의 <code>graph = builder.compile(checkpointer=memory)</code>로 그래프에 붙습니다. 스레드는 5절의 설정 딕셔너리 <code>{"configurable": {"thread_id": "customer-a"}}</code>로 고릅니다. 체크포인트는 8절 출력 <code>customer-a의 체크포인트 수: 6</code>의 여섯 개입니다.</p>
{{mermaid:""" + FIG1 + "|" + FIG1_ALT + "|" + FIG1_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG1_READ) + """</p>
<h3>같은 스레드로 다시 부를 때 칸 값이 정해지는 차례</h3><p>체크포인터를 붙인 그래프를 같은 스레드로 다시 부르면, 그 스레드의 마지막 체크포인트에서 시작합니다. 새 입력은 그 상태의 칸에 들어가고, 그다음에 노드가 실행됩니다. 입력에 넣지 않은 칸은 저장된 값 그대로이고, 규칙 없는 칸에 넣은 값은 저장된 값을 덮어씁니다. 노트북 6절의 합계 7과 10절의 합계 4가 이 차이입니다.</p>
<h3>다른 상황에 적용</h3><p>대화를 이어 가는 에이전트라면 대화 하나에 스레드 이름 하나를 붙입니다. 같은 대화의 다음 질문은 같은 이름으로, 새 대화는 새 이름으로 부릅니다. 대화 기록을 저장해 이어 가는 모습은 <a href=\"""" + L_03 + """\">03절</a>에서 봅니다. 이 절에서는 에이전트 그래프에 체크포인터를 붙여 보지는 않았습니다.</p>
<h3>비교와 경계</h3><p>체크포인터 <code>InMemorySaver</code>는 이 프로그램의 메모리에만 저장합니다. 노트북 11절에서 새 체크포인터로는 같은 스레드 이름을 읽지 못했고, 작업 폴더에도 파일이 생기지 않았습니다. 설치판 소스의 설명도 이 체크포인터를 디버깅이나 시험용으로만 쓰라고 적습니다. 프로그램 밖에 남기는 체크포인터는 <a href=\"""" + L_02 + """\">02절</a>과 <a href=\"""" + L_03 + """\">03절</a>에서 씁니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 상태 형식과 노드 함수를 적고, 체크포인터 없이 컴파일한 그래프를 두 번 실행합니다. 다음으로 같은 설계 객체를 <code>InMemorySaver</code>와 함께 컴파일하고, 스레드 <code>customer-a</code>로 두 번 실행합니다. 저장된 상태와 체크포인트 목록을 읽은 뒤, 스레드 이름과 입력 칸을 하나씩 바꿔 봅니다.</p><p>이 절은 모델을 부르지 않아 모델 요청은 0번이고, API 키 셀도 없습니다. 모델 답이 실행마다 달라지면, 저장된 값이 맞는지 가르기 어렵기 때문입니다. 노드는 수를 더하는 우리 함수라, 같은 입력에 늘 같은 값을 냅니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — 노트북 3절에서 둘째 실행이 <code>KeyError</code>를 받았는지, 6절에서 같은 입력으로 합계 7이 되었는지 봅니다. 8절에서 체크포인트가 여섯이고, 실행 한 번에 셋씩인지 셉니다. 9절에서 스레드 <code>customer-b</code>를 실행한 뒤에도 <code>customer-a</code>의 합계가 7인지 확인합니다.</p>
{{mermaid:""" + FIG2 + "|" + FIG2_ALT + "|" + FIG2_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG2_READ) + """</p>
{{mermaid:""" + FIG3 + "|" + FIG3_ALT + "|" + FIG3_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG3_READ) + """</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>값 바꿔 보기는 둘입니다. 노트북 9절은 스레드 이름만, 10절은 둘째 실행 입력의 합계 칸만 바꿨습니다. 아래 표는 12절 출력을 스레드마다 한 줄로 옮기고, 넣은 값을 더한 것입니다.</p>
""" + thread_table + """
{{mermaid:""" + FIG4 + "|" + FIG4_ALT + "|" + FIG4_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG4_READ) + """</p>
<p>스레드 이름이 다르면, 같은 그래프와 같은 체크포인터에서도 체크포인트 줄이 따로였습니다. 스레드 <code>customer-b</code>를 실행한 뒤에도 <code>customer-a</code>의 합계는 7 그대로였습니다. 한 번도 실행하지 않은 스레드 이름은 오류 없이 빈 딕셔너리를 내놓았습니다.</p><p>스레드 <code>customer-c</code>는 둘째 실행 입력에 합계 0을 넣자, 저장된 합계 3 대신 0에서 더해 4가 되었습니다. 체크포인트 목록으로 보면, 입력을 칸에 넣은 단계 3에서 합계가 0으로 바뀌었습니다. 같은 스레드의 다음 실행은 저장된 상태를 그대로 쓰지 않습니다. 그 위에 새 입력을 칸의 규칙대로 넣은 뒤, 노드를 실행합니다.</p><p>체크포인트 수는 실행 횟수를 따라갔습니다. 실행 한 번에 셋이라, 두 번 실행한 스레드는 여섯, 한 번 실행한 스레드는 셋입니다. 이 수는 대화의 차례 수가 아니고, 노드가 하나인 이 그래프에서 센 수입니다. 노드가 여럿인 그래프의 체크포인트 수는 이번에 세지 않았습니다.</p><p>모델을 부르지 않아, 노트북 출력은 새 커널로 두 번 실행해도 글자까지 같아야 합니다. """ + os.environ.get("AUTHOR01_RUNS_SENTENCE", "새 커널로 두 번 실행했을 때 코드 셀 28개의 출력이 모두 같았습니다.") + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>체크포인터 <code>InMemorySaver</code>는 이 프로그램의 메모리에만 저장합니다. 새 체크포인터 객체로 읽지 못하는 것까지 확인했고, 커널을 다시 시작해 보지는 않았습니다.</li><li>공식 문서는 메모리에 저장한 체크포인트가 프로세스를 다시 시작하면 모두 사라진다고 적습니다. 설치판 소스(<code>langgraph/checkpoint/memory/__init__.py</code> 36~42행)도 디버깅이나 시험용으로만 쓰라고 적습니다.</li><li>한 번도 실행하지 않은 스레드 이름을 읽으면, 오류 없이 빈 딕셔너리 <code>{}</code>가 나왔습니다. 스레드 이름을 잘못 적어도 오류로는 알 수 없습니다.</li><li>체크포인터를 붙인 그래프를 설정 딕셔너리 없이 부르면 <code>ValueError</code>가 났습니다. 이 오류를 내는 자리는 설치판 <code>langgraph/pregel/main.py</code> 2589~2593행입니다.</li><li>체크포인트에는 상태의 칸이 모두 저장됩니다. 비밀 키나 필요 없는 개인정보를 상태 칸에 넣지 않습니다.</li><li>여러 스레드가 함께 쓰는 저장소(Store)는 이 챕터에서 실행하지 않았습니다.</li><li>저장 시점을 고르는 일은 <a href=\"""" + L_04 + """\">04절</a>, 노드가 실패해 멈춘 실행을 이어 가는 일은 <a href=\"""" + L_05 + """\">05절</a>에서 봅니다. 이 절에서는 성공한 실행만 저장했습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>체크포인터를 붙인 그래프를 같은 스레드로 다시 실행하자, 저장된 합계 3에서 이어 7이 되었습니다.</li><li>스레드 이름이 다르면 체크포인트 줄도 따로라, 스레드 <code>customer-b</code>는 합계 0에서 시작해 4가 되었습니다.</li><li>한 번 실행할 때마다 체크포인트가 셋씩 쌓였고, 체크포인터 <code>InMemorySaver</code>는 파일을 남기지 않았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_02 + """\">02절</a>에서는 체크포인트를 PostgreSQL 데이터베이스에 저장합니다. 그 전에 체크포인트를 담을 표를 만드는 일부터 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 체크포인터 없이 컴파일한 그래프에 둘째 실행으로 이번 수 4만 넣자 어떻게 되었나요?</p><p class="quiz-a">오류 <code>KeyError</code>를 받았습니다. 첫 실행의 상태가 남지 않아, 노드가 합계 칸 <code>total</code>을 찾지 못했습니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">2. 체크포인터를 붙이고 스레드 <code>customer-a</code>로 같은 두 입력을 넣었을 때, 둘째 실행의 합계가 7인 까닭은 무엇인가요?</p><p class="quiz-a">그 스레드의 마지막 체크포인트에 저장된 합계 3에서 시작해 4를 더했기 때문입니다. 틀렸다면 노트북 6·7절을 다시 읽습니다.</p><p class="quiz-q">3. 스레드 <code>customer-a</code>의 체크포인트가 여섯 개인 까닭은 무엇인가요?</p><p class="quiz-a">실행을 두 번 했고, 한 번에 셋씩 쌓였기 때문입니다. 셋은 입력을 받은 때, 입력을 칸에 넣은 뒤, 노드를 마친 뒤입니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p><p class="quiz-q">4. 스레드 <code>customer-c</code>의 둘째 입력에 합계 0을 넣자 합계가 4가 된 까닭은 무엇인가요?</p><p class="quiz-a">규칙 없는 칸 <code>total</code>은 입력 값으로 덮어써져, 저장된 3 대신 0에서 4를 더했기 때문입니다. 틀렸다면 노트북 10절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langgraph/checkpointers">LangGraph Checkpointers</a></div>확인 2026-09-25 · 단계마다 상태를 저장하는 체크포인터, 설정의 <code>thread_id</code>, 최신 것부터 놓이는 체크포인트 목록을 적습니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langgraph/persistence">LangGraph Persistence</a></div>확인 2026-09-25 · 스레드 단위 저장과, 메모리 체크포인터는 프로세스를 다시 시작하면 사라진다는 점을 적습니다.</li><li>langgraph-checkpoint 4.2.0 소스 <code>langgraph/checkpoint/memory/__init__.py</code> 33~66행 — 체크포인터 <code>InMemorySaver</code>의 설명입니다.</li><li>같은 소스 334~354행은 스레드 이름으로 고른 체크포인트를 최신 것부터 늘어놓는 자리입니다.</li><li>langgraph 1.2.11 소스 <code>langgraph/pregel/main.py</code> 2589~2593행 — 설정 없이 부를 때 나는 오류입니다.</li><li>같은 판 <code>langgraph/graph/state.py</code> 1177~1179행은 메서드 <code>compile</code>의 인자 <code>checkpointer</code>입니다.</li><li>Ch 13 01·02절에서 상태 형식과 칸 규칙을, Ch 20 03절에서 설정 딕셔너리와 단계를 보았습니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "01", SLUG, "experiment", cells())
        print("wrote", path)
