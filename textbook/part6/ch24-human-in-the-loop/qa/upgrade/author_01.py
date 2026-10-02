"""Ch 24 01절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 author_01.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다).
                                    도구 파일은 없거나 이 생성기 판(함수 셋)과 같을 때만 쓴다. 03절이 함수 둘을 더한 판
                                    (TOOLS로 시작하는 더 긴 판)이면 건너뛰고 알린다(마감 A-10 — 03·04 가져오기를 지키려고).
  python3 author_01.py --src-only → _src 본문만 다시 쓴다(노트북·도구 파일 그대로)
  python3 author_01.py --tools-copy DIR → 도구 파일 글을 DIR에만 쓴다(묶음 모양 확인용 사본, 실습 폴더는 건드리지 않음)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **paired 형식 유지**. 슬러그 그대로(Ch 23 07 b8 링크).

## 결정 1 — 모델을 부르지 않는다 (챕터 리드 결정 1, M1)

사람의 답은 셀에 적은 값("approve"·"reject")을 Command(resume=…)에 넣는다. 모델 요청 0번, 키 셀 없음.
잠금에 모델 패키지가 없고, 묶음 실행 검사(textbook/part6/qa/check_bundle_execution.py)가 이 노트북을 키 없이 새 커널로 돌린다.
dotenv도 가져오지 않는다(검사는 --with python-dotenv를 주지만 학생 .venv에는 없음).

## 결정 2 — 파일은 임시 폴더에만, 지우는 줄 없음 (챕터 리드 결정 2)

준비 셀 차례: 설치 → 가져오기(도구 파일 포함, 작업 위치를 옮기기 전) → 임시 폴더(Ch 23 01 셀에서 앞머리만 ch24-01-).
옛 판의 실습 폴더 맨 위 approval-effects.txt와 unlink 두 줄을 없애고, 장면마다 다른 기록 파일 이름(before.record 등)을 쓴다.

## 결정 3 — paired: Before = 적고 나서 묻기(실제 결함), After = 묻고 나서 승인일 때만 적기

Before charge_then_ask는 append_key → interrupt. 거절(reject)로 이어 가도 노드가 처음부터 다시 실행되어 같은 키 두 줄(빨강).
After ask_then_charge는 interrupt → 답이 approve일 때만 append_key. 거절이면 파일 없음, 값 바꿔 보기 승인이면 한 줄.
노드 안 print로 노드가 두 번 시작하는 것을 셀 출력에 보인다. 6절은 Ch 23 06 append_key_once로 묻기 전 접수 기록을
멱등하게 적는 노드(receive_then_ask) — 이어 가도 한 줄(Ch 30 06 「중복 실행 방지 원칙」이 기대는 문장의 실행 근거).

## 결정 4 — 도구 파일 approval_tools.py를 이 절이 처음 만든다 (챕터 리드 결정 4, B안)

Ch 23 checkpoint_tools.py에서 이 노트북이 쓰는 함수 셋(04 read_record · 06 append_key·append_key_once)만 본문을 글자 그대로
옮긴다(아래 check_same_as_ch23 — Ch 23 도구 파일과 문자열·AST 대조). SQLite를 가져오지 않는다(이 챕터 잠금에 없음).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·
튜플 풀기·별표 풀기·`{**…}`·`while True`·숫자 밑줄·세미콜론·`isinstance`·데코레이터·클래스(상태 형식 말고)·`try`·`Path`·`unlink`·모델.
Interrupt.id·체크포인트 ID는 출력하지 않는다(실행마다 바뀜).
"""
from __future__ import annotations

import ast
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch24-human-in-the-loop/notebooks"
TOOLS_PATH = LAB / "approval_tools.py"
CH23_TOOLS = ROOT / "labs/part6/ch23-persistence/notebooks/checkpoint_tools.py"
FIGS = ROOT / "textbook/part6/ch24-human-in-the-loop/figures"
SLUG = "01-interrupt-승인-게이트"
TITLE_TEXT = "interrupt 승인 게이트"
SRC = ROOT / "textbook/part6/ch24-human-in-the-loop/_src" / (SLUG + ".html")
# 교재 출력을 만든 실행의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답)에서 읽은 값
RUNSEC = os.environ.get("AUTHOR01_RUNSEC", "2초 안에")
RUNS_SENTENCE = os.environ.get("AUTHOR01_RUNS_SENTENCE", "새 커널로 두 번 실행했을 때 코드 셀 28개의 출력이 모두 같았습니다.")

# ---------------------------------------------------------------- 도구 파일 (Ch 23 함수 셋, 글자 그대로)
DEF_RECORD = r'''# 기록 파일을 읽어, 줄마다 적힌 노드 이름을 목록으로 내놓습니다
def read_record(record_name):
    with open(record_name, encoding="utf-8") as record_file:
        text = record_file.read()
    return text.split()'''

DEF_APPEND = r'''# 기록 파일 끝에 주문 키 한 줄을 덧붙이고, 한 일을 글 "적음"으로 내놓습니다
def append_key(record_name, order_key):
    # 여는 방식 "a"는 파일 끝에 이어 쓰고, 파일이 없으면 새로 만듭니다
    with open(record_name, "a", encoding="utf-8") as record_file:
        record_file.write(order_key + "\n")
    return "적음"'''

DEF_ONCE = r'''# 기록 파일에 같은 주문 키가 이미 있으면 건너뛰고, 없을 때만 한 줄을 덧붙입니다
def append_key_once(record_name, order_key):
    written_keys = []
    # 기록 파일이 있을 때만 읽습니다(처음 부를 때는 파일이 없습니다)
    if os.path.exists(record_name):
        with open(record_name, encoding="utf-8") as record_file:
            written_keys = record_file.read().split()
    if order_key in written_keys:
        return "건너뜀"
    return append_key(record_name, order_key)'''

TOOLS_HEAD = '''"""Ch 24 Human-in-the-Loop와 Time Travel — 앞 챕터와 이 챕터 앞 절에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from approval_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
Ch 23 01·04·06절 노트북에서 처음 적은 함수 넷과 이 챕터 03절 노트북에서 처음 적은 함수 하나는 본문을 글자 그대로 옮겼습니다.
Ch 23 도구 파일 checkpoint_tools.py는 SQLite 체크포인터를 가져오는데, 이 챕터 실습 폴더에는 그 패키지가 없습니다.
그래서 파일째 가져오지 않고, 이 챕터 노트북이 쓰는 함수만 옮겼습니다.
read_record의 설명 주석은 Ch 23 04절 그대로라 「노드 이름」이라고 적혀 있고, 이 챕터에서는 주문 키를 읽습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""

import os
'''

TOOL_PARTS = [
    ("Ch 23 04절에서 배웠습니다 — 04절 노트북 3절의 같은 이름 함수를 옮겼습니다", DEF_RECORD),
    ("Ch 23 06절에서 배웠습니다 — 06절 노트북 2절의 같은 이름 함수를 옮겼습니다", DEF_APPEND),
    ("Ch 23 06절에서 배웠습니다 — 06절 노트북 2절의 같은 이름 함수를 옮겼습니다", DEF_ONCE),
]


def tools_text() -> str:
    text = TOOLS_HEAD
    for note, definition in TOOL_PARTS:
        text = text + "\n\n# " + note + "\n" + definition + "\n"
    return text


TOOLS = tools_text()


def check_same_as_ch23() -> None:
    """도구 파일의 함수 셋이 Ch 23 도구 파일(checkpoint_tools.py)의 같은 이름 함수와 글자·AST 모두 같은지 확인합니다."""
    ch23 = CH23_TOOLS.read_text(encoding="utf-8")
    ch23_tree = ast.parse(ch23)
    ch23_defs = {}
    for node in ch23_tree.body:
        if isinstance(node, ast.FunctionDef):
            ch23_defs[node.name] = ast.dump(node)
    tree = ast.parse(TOOLS)
    found = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            found[node.name] = ast.dump(node)
    assert sorted(found) == ["append_key", "append_key_once", "read_record"], sorted(found)
    for note, definition in TOOL_PARTS:
        # 주석 머리줄 + 설명 주석 + 본문이 Ch 23 파일에 한 덩어리로 들어 있다
        assert ("# " + note + "\n" + definition) in ch23, note
        name = ast.parse(definition).body[0].name
        assert found[name] == ch23_defs[name], name
    # SQLite·langgraph를 가져오지 않는다(이 챕터 잠금에 SQLite 체크포인터가 없음)
    assert "sqlite" not in TOOLS.lower().replace("sqlite 체크포인터", "") and "langgraph" not in TOOLS
    assert "interrupt" not in TOOLS


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["langgraph==1.2.11", "langgraph-checkpoint==4.2.0"])

IMPORTS = r'''# 그래프 이름(Ch 13 01절)·체크포인터(Ch 23 01절)와, 멈춤 표시에 쓸 이름 둘을 가져옵니다
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
# interrupt는 노드를 멈추는 함수, Command는 멈춘 그래프에 사람의 답을 넘길 때 쓰는 객체입니다
from langgraph.types import Command, interrupt
# Ch 23 04·06절에서 배운 함수 셋을 도구 파일에서 가져옵니다
from approval_tools import append_key, append_key_once, read_record

print("langgraph.types에서 가져온 이름:", "Command, interrupt")
print("도구 파일에서 가져온 함수:", "append_key, append_key_once, read_record")'''

# Ch 23 01절 임시 폴더 셀에서 앞머리(ch23-01- → ch24-01-)와 선례 절 이름만 바꾼 셀(아래 assert)
CH23_FOLDER = r'''# 파일이 생기는지 볼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다(Ch 4 03절과 같은 모양)
import os
import tempfile

# mkdtemp()는 운영체제 임시 폴더 안에 새 폴더를 만들고, 그 폴더의 위치를 글로 내놓습니다
practice_folder = tempfile.mkdtemp(prefix="ch23-01-")
# chdir()는 터미널의 cd처럼 현재 작업 폴더를 옮깁니다
os.chdir(practice_folder)
print("임시 폴더 이름에 ch23-01-이 들어 있는가:", "ch23-01-" in practice_folder)
print("현재 작업 폴더의 파일:", os.listdir())'''
FOLDER = CH23_FOLDER.replace("ch23-01-", "ch24-01-").replace("(Ch 4 03절과 같은 모양)", "(Ch 23 01절과 같은 모양)")

STATE = r'''# 주문 키·결제 기록 파일 이름·사람의 답 칸을 둔 상태 형식을 만듭니다(Ch 13 01절 모양, 세 칸 모두 규칙 없음)
class ApprovalState(TypedDict):
    order_key: str
    record_name: str
    answer: str'''

DEF_ASK = r'''# 멈춤 표시로 사람에게 묻고, 받은 답을 칸 answer에 내는 노드입니다(파일은 쓰지 않습니다)
def ask_only(state):
    print("노드 ask_only 시작")
    # interrupt는 처음 부를 때 이 줄에서 그래프를 멈추고, 이어 갈 때는 사람의 답을 내놓습니다
    question = {"order_key": state["order_key"], "question": "결제할까요?"}
    answer = interrupt(question)
    print("받은 답:", answer)
    return {"answer": answer}'''


def builder_cell(node_name: str, prefix: str, extra: str = "") -> str:
    """노드 하나를 START → 노드 → END로 잇고 체크포인터를 붙여 컴파일하는 셀(절마다 이름만 다름)."""
    return ("# 노드 하나를 START → " + node_name + " → END로 잇고, 체크포인터를 붙여 컴파일합니다\n"
            + prefix + "_builder = StateGraph(ApprovalState)\n"
            + prefix + '_builder.add_node("' + node_name + '", ' + node_name + ")\n"
            + prefix + '_builder.add_edge(START, "' + node_name + '")\n'
            + prefix + '_builder.add_edge("' + node_name + '", END)\n'
            + "# 멈춘 자리를 저장해 두어야 나중에 이어 갈 수 있어, 체크포인터를 붙입니다\n"
            + prefix + "_graph = " + prefix + "_builder.compile(checkpointer=InMemorySaver())\n"
            + extra
            + 'print("등록한 노드:", list(' + prefix + "_builder.nodes))")


BUILD_ASK = builder_cell("ask_only", "ask", 'ask_config = {"configurable": {"thread_id": "ask-only"}}\n'
                         'print("스레드 이름:", ask_config["configurable"]["thread_id"])\n')

FIRST_ASK = r'''# 첫 실행: 노드가 멈춤 표시에서 멈추면, invoke는 그때까지의 상태를 내놓습니다
first_result = ask_graph.invoke({"order_key": "order-2401", "answer": "대기"}, ask_config)
print("결과의 키:", list(first_result))
print("칸 answer:", first_result["answer"])'''

MARKS = r'''# 키 __interrupt__의 목록에서 멈춤 표시 수와, 첫 멈춤 표시에 담긴 질문 값을 꺼냅니다
paused_marks = first_result["__interrupt__"]
print("멈춤 표시 수:", len(paused_marks))
first_mark = paused_marks[0]
print("멈춤 표시의 종류:", type(first_mark).__name__)
# 속성 value에는 interrupt에 넣은 질문 값이 그대로 들어 있습니다(아이디는 실행마다 달라 출력하지 않음)
print("질문 값:", first_mark.value)'''

PAUSED_STATE = r'''# 멈춘 스레드의 마지막 체크포인트에서 다음에 실행할 노드와 저장된 칸 값을 읽습니다
paused_state = ask_graph.get_state(ask_config)
print("다음에 실행할 노드:", paused_state.next)
print("저장된 칸 값:", paused_state.values)'''

PAUSED_TASK = r'''# 멈춘 작업(task)에 딸린 질문 값과, 지금까지 쌓인 체크포인트 수를 봅니다
paused_task = paused_state.tasks[0]
print("멈춘 작업의 노드:", paused_task.name)
# 속성 interrupts는 이 작업에 딸린 멈춤 표시의 목록입니다
print("작업에 딸린 질문 값:", paused_task.interrupts[0].value)
paused_history = list(ask_graph.get_state_history(ask_config))
print("체크포인트 수:", len(paused_history))'''

RESUME_ASK = r'''# 사람의 답 "approve"를 Command의 자리 resume에 담아, 같은 스레드로 이어 갑니다
resume_result = ask_graph.invoke(Command(resume="approve"), ask_config)
print("이어 간 뒤 결과:", resume_result)'''

DONE_ASK = r'''# 이어 간 뒤 다음에 실행할 노드와 체크포인트 수를 봅니다
done_state = ask_graph.get_state(ask_config)
print("다음에 실행할 노드:", done_state.next)
done_history = list(ask_graph.get_state_history(ask_config))
print("체크포인트 수:", len(done_history))
# 노드 하나짜리 그래프를 한 번 끝까지 실행한 수라, 실행마다 같아야 합니다
assert len(done_history) == 3, "이어 간 뒤 체크포인트는 셋이어야 합니다"'''

DEF_BEFORE = r'''# Before 노드: 결제 기록 파일에 주문 키를 먼저 적고, 그다음 멈춤 표시로 묻습니다
def charge_then_ask(state):
    print("노드 charge_then_ask 시작")
    note = append_key(state["record_name"], state["order_key"])
    print("결제 기록:", note)
    question = {"order_key": state["order_key"], "question": "결제할까요?"}
    answer = interrupt(question)
    print("받은 답:", answer)
    return {"answer": answer}'''

BUILD_BEFORE = builder_cell("charge_then_ask", "before")

FIRST_BEFORE = r'''# 첫 실행: 기록 파일 이름 before.record를 넣고, 멈춘 뒤 그 파일에 적힌 키를 읽습니다
before_config = {"configurable": {"thread_id": "before"}}
before_input = {"order_key": "order-2401", "record_name": "before.record", "answer": "대기"}
before_paused = before_graph.invoke(before_input, before_config)
print("멈춤 표시 수:", len(before_paused["__interrupt__"]))
print("멈춘 뒤 기록 파일의 키:", read_record("before.record"))'''

RESUME_BEFORE = r'''# 사람의 답 "reject"로 이어 가고, 칸 answer와 결제 기록 파일의 키를 봅니다
before_result = before_graph.invoke(Command(resume="reject"), before_config)
print("칸 answer:", before_result["answer"])
before_keys = read_record("before.record")
print("기록 파일의 키:", before_keys)
before_count = before_keys.count("order-2401")
print("같은 키가 적힌 줄 수:", before_count)
# 우리 노드가 정하는 값이라 실행마다 같아야 합니다
assert before_count == 2, "적고 나서 묻는 노드는 거절해도 같은 키를 두 줄 남깁니다"'''

DEF_AFTER = r'''# After 노드: 먼저 멈춤 표시로 묻고, 답이 approve일 때만 결제 기록을 적습니다
def ask_then_charge(state):
    print("노드 ask_then_charge 시작")
    question = {"order_key": state["order_key"], "question": "결제할까요?"}
    answer = interrupt(question)
    print("받은 답:", answer)
    if answer == "approve":
        note = append_key(state["record_name"], state["order_key"])
        print("결제 기록:", note)
    return {"answer": answer}'''

BUILD_AFTER = builder_cell("ask_then_charge", "after")

FIRST_REJECT = r'''# 첫 실행: 기록 파일 이름 after-reject.record를 넣고, 멈춘 뒤 그 파일이 있는지 봅니다
reject_config = {"configurable": {"thread_id": "after-reject"}}
reject_input = {"order_key": "order-2401", "record_name": "after-reject.record", "answer": "대기"}
reject_paused = after_graph.invoke(reject_input, reject_config)
print("멈춤 표시 수:", len(reject_paused["__interrupt__"]))
print("기록 파일이 있는가:", os.path.exists("after-reject.record"))'''

RESUME_REJECT = r'''# 4절과 같은 답 "reject"로 이어 가고, 칸 answer와 기록 파일이 있는지 봅니다
reject_result = after_graph.invoke(Command(resume="reject"), reject_config)
print("칸 answer:", reject_result["answer"])
reject_exists = os.path.exists("after-reject.record")
print("기록 파일이 있는가:", reject_exists)
# 거절이면 쓰는 줄에 닿지 않으므로 실행마다 같아야 합니다
assert not reject_exists, "묻고 나서 적는 노드는 거절이면 기록 파일을 만들지 않습니다"'''

FIRST_APPROVE = r'''# 값 바꿔 보기: 새 스레드 after-approve로 첫 실행을 하고, 멈춘 뒤 기록 파일이 있는지 봅니다
approve_config = {"configurable": {"thread_id": "after-approve"}}
approve_input = {"order_key": "order-2401", "record_name": "after-approve.record", "answer": "대기"}
approve_paused = after_graph.invoke(approve_input, approve_config)
print("멈춤 표시 수:", len(approve_paused["__interrupt__"]))
print("기록 파일이 있는가:", os.path.exists("after-approve.record"))'''

RESUME_APPROVE = r'''# 사람의 답 하나만 "approve"로 바꿔 이어 가고, 칸 answer와 결제 기록 파일의 키를 봅니다
approve_result = after_graph.invoke(Command(resume="approve"), approve_config)
print("칸 answer:", approve_result["answer"])
approve_keys = read_record("after-approve.record")
print("기록 파일의 키:", approve_keys)
approve_count = approve_keys.count("order-2401")
print("같은 키가 적힌 줄 수:", approve_count)
# 쓰는 줄은 멈춤 표시 뒤에 있어, 노드가 두 번 시작해도 한 번만 적습니다
assert approve_count == 1, "묻고 나서 적는 노드는 승인이면 키를 한 줄만 남깁니다"'''

DEF_RECEIVE = r'''# 접수 기록을 멱등하게 먼저 적고(같은 키가 있으면 건너뜀), 그다음 멈춤 표시로 묻는 노드입니다
def receive_then_ask(state):
    print("노드 receive_then_ask 시작")
    note = append_key_once(state["record_name"], state["order_key"])
    print("접수 기록:", note)
    question = {"order_key": state["order_key"], "question": "결제할까요?"}
    answer = interrupt(question)
    print("받은 답:", answer)
    return {"answer": answer}'''

BUILD_RECEIVE = builder_cell("receive_then_ask", "receipt")

RUN_RECEIVE = r'''# 기록 파일 이름 receipt.record로 첫 실행을 한 뒤, 4절과 같은 답 "reject"로 이어 갑니다
receipt_config = {"configurable": {"thread_id": "receipt"}}
receipt_input = {"order_key": "order-2401", "record_name": "receipt.record", "answer": "대기"}
receipt_graph.invoke(receipt_input, receipt_config)
print("멈춘 뒤 접수 기록의 키:", read_record("receipt.record"))
receipt_result = receipt_graph.invoke(Command(resume="reject"), receipt_config)
print("칸 answer:", receipt_result["answer"])
print("이어 간 뒤 접수 기록의 키:", read_record("receipt.record"))'''

SCENES = r'''# 4~6절의 네 장면을 노드 이름·사람의 답·기록 파일 이름 한 줄씩으로 모읍니다
scenes = []
scenes.append(["charge_then_ask", before_result["answer"], "before.record"])
scenes.append(["ask_then_charge", reject_result["answer"], "after-reject.record"])
scenes.append(["ask_then_charge", approve_result["answer"], "after-approve.record"])
scenes.append(["receive_then_ask", receipt_result["answer"], "receipt.record"])
print("모은 장면 수:", len(scenes))'''

TABLE = r'''# 장면마다 기록 파일에 같은 주문 키가 적힌 줄 수를 세어, 라벨 줄 아래에 한 줄씩 출력합니다
print("노드 | 사람의 답 | 기록 파일 | 같은 키가 적힌 줄 수")
for scene in scenes:
    # 기록 파일이 없으면 적힌 줄이 없으므로 0으로 둡니다
    key_count = 0
    if os.path.exists(scene[2]):
        scene_keys = read_record(scene[2])
        key_count = scene_keys.count("order-2401")
    print(scene[0], "|", scene[1], "|", scene[2], "|", key_count)'''

FILES_END = r'''# 작업 폴더에 남은 파일을 봅니다(모두 이 절의 임시 폴더 안에 있습니다)
file_names = sorted(os.listdir())
print("작업 폴더의 파일:", file_names)
print("파일 수:", len(file_names))'''

# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/01-figures.md)
FIG1 = "01-1-멈추고-사람의-답으로-이어-가는-차례"
FIG1_ALT = os.environ.get("AUTHOR01_FIG1_ALT", "위에서 아래로 상자 일곱이 한 줄로 이어진 흐름도입니다. 첫 초록 상자는 첫 invoke 주문 키 order-2401, 둘째 파란 상자는 노드 ask_only 시작 interrupt에서 멈춤입니다. 셋째 노란 상자는 멈춤 표시 하나와 질문 값, 체크포인트 둘입니다. 넷째 초록 상자는 사람의 답 approve, 다섯째 파란 상자는 Command resume=approve 같은 스레드로 invoke입니다. 여섯째 파란 상자는 노드 ask_only를 처음부터 다시 실행 interrupt가 답을 내놓음, 일곱째 노란 상자는 칸 answer approve 체크포인트 셋인 그림")
FIG1_CAP = "노드는 멈춤 표시에서 멈췄다가, 사람의 답을 넣어 이어 가자 처음부터 다시 실행되어 답을 받았습니다."
FIG1_READ = """위에서 아래로 한 줄로 읽습니다.
초록 상자는 우리가 넣은 값과 사람의 답이고, 파란 상자는 우리가 적은 노드와 부른 줄입니다.
노란 상자는 노트북 2·3절에서 출력으로 확인한 값입니다.
둘째 상자와 여섯째 상자는 같은 노드이고, 노드는 두 번 시작했습니다."""

FIG2 = "01-2-멈춘-동안-체크포인터에-남은-것"
FIG2_ALT = os.environ.get("AUTHOR01_FIG2_ALT", "위에서 아래로 읽는 흐름도입니다. 맨 위 파란 상자 멈춘 뒤 get_state 스레드 ask-only에서 칸 체크포인터에 남은 것으로 화살표가 갑니다. 칸 안에는 노란 상자 넷이 위아래로 놓입니다. 다음에 실행할 노드 ask_only, 칸 값 order-2401 answer 대기, 작업 ask_only에 딸린 질문 값 결제할까요, 체크포인트 둘입니다. 칸에서 맨 아래 노란 상자 Command resume=approve 뒤 다음 노드 없음 체크포인트 셋으로 화살표가 가는 그림")
FIG2_CAP = "멈춘 동안 체크포인터에는 끝나지 않은 노드와 질문 값이 남았고, 이어 간 뒤 체크포인트가 셋이 되었습니다."
FIG2_READ = """위에서 아래로 읽습니다.
파란 상자는 우리가 부른 줄이고, 노란 상자는 모두 노트북 3절 출력입니다.
칸 안의 네 상자는 멈춘 동안 한꺼번에 읽은 값이라 화살표 없이 쌓았습니다.
맨 아래 상자는 사람의 답으로 이어 간 뒤의 값입니다."""

FIG3 = "01-3-같은-거절에서-적고-묻기와-묻고-적기"
FIG3_ALT = os.environ.get("AUTHOR01_FIG3_ALT", "위에 회색 상자 하나가 있고 아래에 칸 둘이 나란히 놓인 그림입니다. 회색 상자에는 두 노드 같음 주문 키 order-2401 사람의 답 reject 노드가 두 번 시작이 적혀 있고, 두 칸으로 화살표가 갑니다. 칸 Before charge_then_ask에는 파란 상자 적고 나서 멈춤 이어 갈 때 다시 적음 아래에 빨간 상자 거절인데 같은 키 두 줄이 있습니다. 칸 After ask_then_charge에는 파란 상자 묻고 나서 approve일 때만 적음 아래에 노란 상자 기록 파일 없음이 있는 그림")
FIG3_CAP = "같은 거절을 넣어도, 적고 나서 묻는 노드는 같은 키를 두 줄 남겼고 묻고 나서 적는 노드는 파일을 만들지 않았습니다."
FIG3_READ = """맨 위 회색 상자는 두 노드 모두에서 확인한 값이고, 노트북 4·5절 출력입니다.
칸 둘은 Before와 After이고, 칸 안은 위에서 아래로 노드가 한 일과 그 결과입니다.
빨간 상자가 Before 결함이고, 노란 상자는 After 출력입니다."""

FIG4 = "01-4-네-장면의-기록-줄-수"
FIG4_ALT = os.environ.get("AUTHOR01_FIG4_ALT", "위에 회색 상자 하나가 있고 아래에 칸 둘이 나란히 놓인 그림입니다. 회색 상자에는 네 장면 같음 주문 키 order-2401 노드가 두 번 시작이 적혀 있습니다. 칸 묻기 전에 적는 노드에는 빨간 상자 charge_then_ask 답 reject 결제 기록 두 줄 아래에 노란 상자 receive_then_ask 답 reject append_key_once로 접수 기록 한 줄이 있습니다. 칸 묻고 나서 적는 노드에는 노란 상자 ask_then_charge 답 reject 기록 파일 없음 아래에 노란 상자 ask_then_charge 답 approve 결제 기록 한 줄이 있는 그림")
FIG4_CAP = "묻기 전에 적은 쓰기는 거절에도 남았고, 멱등하게 적으면 한 줄, 묻고 나서 적으면 승인일 때만 한 줄이었습니다."
FIG4_READ = """맨 위 회색 상자는 네 장면 모두에서 확인한 값입니다.
왼쪽 칸은 멈춤 표시 앞에서 적는 두 노드, 오른쪽 칸은 뒤에서 적는 노드의 두 답입니다.
상자는 모두 노트북 6절 끝의 견주기 출력 한 줄씩이고, 칸 안 두 상자는 나란히 놓인 장면이라 화살표 없이 쌓았습니다.
빨간 상자는 Before 결함 결과입니다."""

ILLU = "01-5-빈자리-앞의-컵과-빈자리-뒤의-컵"
ILLU_ALT = os.environ.get("AUTHOR01_ILLU_ALT", "흰 바탕에 흰 탁자 하나를 조금 위에서 본 그림입니다. 탁자 위에 나무 도미노 두 줄이 위아래로 놓였습니다. 두 줄 모두 왼쪽 도미노는 넘어져 있고, 가운데 빈자리 오른쪽 도미노는 서 있습니다. 위 줄에는 빈자리 왼쪽, 넘어진 도미노 곁에 흰 컵 하나가 옆으로 쓰러져 있습니다. 아래 줄에는 서 있는 도미노 오른쪽 끝에 흰 컵 하나가 똑바로 서 있습니다. 글자·숫자·사람·손은 없는 그림")
ILLU_CAP = os.environ.get("AUTHOR01_ILLU_CAP", "빈자리 앞에 둔 위 줄의 컵은 이미 쓰러졌고, 빈자리 뒤에 둔 아래 줄의 컵은 서 있습니다.")
ILLU_READ = os.environ.get("AUTHOR01_ILLU_READ", "흰 탁자 위에 도미노 두 줄이 위아래로 있고, 두 줄 모두 빈자리 왼쪽은 넘어졌고 오른쪽은 서 있습니다. 위 줄의 컵은 빈자리 왼쪽에서 옆으로 쓰러졌고, 아래 줄의 컵은 빈자리 뒤 줄 끝에 서 있습니다. 첫 실행이 멈추고 사람이 아직 답하지 않은 때의 모습이고, 빈자리가 멈춤 표시, 쓰러진 컵이 결제 기록입니다. 위 줄이 적고 나서 묻는 <code>charge_then_ask</code>, 아래 줄이 묻고 나서 적는 <code>ask_then_charge</code>입니다. 서 있는 도미노의 개수와 탁자 다리는 무엇과도 짝짓지 않습니다.")

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 노드 안의 멈춤 표시로 그래프를 멈추고, 멈춘 동안 무엇이 저장되는지 봅니다.
2. 사람의 답을 넣어 같은 실행을 이어 가고, 노드가 몇 번 시작하는지 셉니다.
3. 결제 기록을 먼저 적고 묻는 노드와, 묻고 나서 적는 노드에 같은 거절을 넣어 기록을 견줍니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
사람의 답은 우리가 셀에 적어 넣는 값(`"approve"`·`"reject"`)입니다.
실제 서비스라면 화면에서 사람이 고른 값을 같은 자리에 넣습니다.
매번 같은 값을 내는 우리 노드로, 기록이 몇 줄 남는지 출력으로 가릅니다.

결제는 실제 결제 서비스를 부르지 않고, Ch 23 06절처럼 기록 파일에 주문 키를 한 줄 적는 것으로 대신합니다.
노트북은 빈 임시 폴더를 만들어 그 폴더에서 실행합니다.
기록 파일은 모두 이 임시 폴더에 생기고, 실습 폴더에는 남지 않습니다.
읽어 오는 자료 파일은 없습니다.
걸린 시간은 재지 않았습니다.

**기준 버전** — 첫 셀에서 패키지 둘을 설치합니다.
그래프는 langgraph 1.2.11, 체크포인터는 langgraph-checkpoint 4.2.0에 들어 있습니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.
설치 셀에 걸리는 시간은 네트워크에 따라 달라집니다.

**강의와 실습 범위** — 강의 시간에는 2~5절을 읽습니다.
멈춤 표시와 사람의 답을 보고, 묻는 자리와 적는 자리의 차례를 견주는 자리입니다.
6절은 묻기 전에 꼭 적어야 하는 기록을 한 번만 남기는 자리이고, 실습 시간에 실행합니다.
셀 하나만 다시 실행하면 같은 스레드와 같은 기록 파일에 이어 적어 값이 달라집니다.
처음 값으로 다시 보려면 1절 임시 폴더 셀부터 다시 실행합니다.

실습 폴더 `labs/part6/ch24-human-in-the-loop`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

Ch 23에서는 체크포인터로 상태를 저장하고, 멈춘 실행을 저장된 자리부터 이어 갔습니다.
그때 실행이 멈춘 까닭은 실패나 강제 종료였습니다.
이 절에서는 그래프가 스스로 멈춰 사람의 확인을 기다리게 합니다.
절 제목의 「승인 게이트」는 Ch 17 02절의 승인 지점과 같은 뜻이라, 본문에서는 승인 지점이라고 씁니다.
Ch 18 01절의 게이트(중간 결과를 코드로 검사하는 자리)와는 다른 말입니다.

첫 셀은 패키지 둘을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langgraph: 1.2.11`과 `langgraph-checkpoint: 4.2.0`이 보입니다.
두 판 모두 실습 폴더 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
상태 형식과 그래프 이름은 Ch 13 01절, 체크포인터 `InMemorySaver`는 Ch 23 01절과 같습니다.
새로 쓰는 이름은 모듈 `langgraph.types`의 `interrupt`이고, 뜻은 2절에서 풉니다.
함께 가져오는 `Command`는 Ch 13 06절에서 갱신과 다음 노드 이름을 담았던 객체입니다.
마지막 가져오기 줄은 Ch 23에서 배운 함수 셋을 도구 파일 `approval_tools.py`에서 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: append_key, append_key_once, read_record`가 보입니다.
세 함수는 Ch 23 04절과 06절 노트북에서 처음 적은 함수입니다.

앞에서 배운 함수는 `approval_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있어, 작업 위치를 옮기기 전에 가져왔습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다.

함수 `append_key`는 기록 파일 끝에 키 한 줄을 적고 글 `적음`을 내놓습니다.
함수 `append_key_once`는 같은 키가 이미 적혀 있으면 적지 않고 `건너뜀`을 내놓습니다.
함수 `read_record`는 기록 파일의 줄을 목록으로 읽습니다.
Ch 23 도구 파일은 SQLite 체크포인터를 가져와, 이 챕터에서는 쓰는 함수만 새 도구 파일에 옮겼습니다.

다음 셀은 Ch 23 01절처럼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다.
이 절의 기록 파일은 모두 이 폴더에 생기고, 실습 폴더에는 남지 않습니다.
폴더 위치는 컴퓨터마다 달라 출력하지 않고, 폴더 이름의 앞머리만 확인합니다."""),
        setup(FOLDER),
        md("""**결과 읽기** — 출력 줄 `임시 폴더 이름에 ch24-01-이 들어 있는가: True`로, 이 절의 폴더를 만들었습니다.
출력 줄 `현재 작업 폴더의 파일: []`로, 빈 폴더에서 시작합니다.

## 2. 멈춤 표시로 멈추고 사람의 답으로 이어 가기

Ch 17 02절에서는 부작용이 생기는 단계 앞에서 사람이 확인하는 자리를 승인 지점이라고 불렀습니다.
Ch 17 03절의 사람 확인은 그 자리에 닿으면 반복을 멈추고 사람에게 넘겼고, 이어 가지는 않았습니다.
이 절은 그래프 안에 승인 지점을 두고, 사람의 답을 받아 같은 실행을 이어 갑니다.

먼저 상태 형식을 만듭니다.
칸 `order_key`는 주문 키, 칸 `record_name`은 결제 기록 파일 이름, 칸 `answer`는 사람의 답입니다.
세 칸 모두 규칙을 적지 않아, 새 값이 오면 덮어씁니다."""),
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 절의 그래프 넷이 모두 이 상태 형식을 씁니다.

멈춤 표시(interrupt)는 노드가 그 자리에서 그래프를 멈추고, 사람에게 보일 값을 남기는 일입니다.
도미노 줄 가운데 한 자리를 비워 두면, 넘어지던 줄이 그 빈자리에서 멈추는 것과 같습니다.
이 절 코드에서는 노드 안에서 함수 `interrupt`를 부르는 줄입니다.

질문 값은 멈춤 표시와 함께 사람에게 보일 값입니다.
빈자리 옆에 세워 둔 안내판처럼, 무엇을 정해야 하는지 알려 줍니다.
이 절에서는 주문 키와 질문 글 `결제할까요?`를 담은 딕셔너리입니다.

다음 셀은 질문만 하고 파일은 쓰지 않는 노드입니다.
노드가 시작할 때와 답을 받은 뒤에 한 줄씩 출력하게 해, 노드가 몇 번 실행되는지 셀 출력으로 봅니다."""),
        code(DEF_ASK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `interrupt`는 처음 부를 때 그 줄에서 노드를 멈춥니다.
그래서 첫 실행에서는 그 아래의 `받은 답:` 줄과 갱신을 내는 줄까지 가지 않습니다.

다음 셀은 이 노드 하나로 그래프를 만들고, Ch 23 01절처럼 체크포인터 `InMemorySaver`를 붙여 컴파일합니다.
멈춘 자리를 저장해 두어야 나중에 그 자리부터 이어 갈 수 있기 때문입니다.
공식 문서도 멈춤 표시를 쓰려면 체크포인터와 설정의 스레드 이름이 있어야 한다고 적습니다."""),
        code(BUILD_ASK),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['ask_only']`와 `스레드 이름: ask-only`가 보입니다.

다음 셀은 주문 키와 답 칸의 처음 값 `대기`를 넣어 실행합니다.
이 노드는 파일을 쓰지 않아, 칸 `record_name`은 넣지 않았습니다.
실행 전에 예상해 봅니다.
노드는 질문하는 줄에서 멈추고, 셀 출력에는 노드가 시작했다는 줄 하나만 보일 것입니다."""),
        code(FIRST_ASK),
        md("""**결과 읽기** — 출력 첫 줄 `노드 ask_only 시작`은 노드 안의 `print`가 찍은 줄이고, `받은 답:` 줄은 없습니다.
출력 줄 `결과의 키: ['order_key', 'answer', '__interrupt__']`에 키 `__interrupt__`가 더해졌습니다.
출력 줄 `칸 answer: 대기`로, 칸 값은 아직 처음 값입니다.
노드가 끝나지 않았으므로 노드가 낼 갱신은 칸에 들어가지 않았습니다.

다음 셀은 키 `__interrupt__`에 든 것을 봅니다.
목록에는 멈춤 표시 하나마다 항목이 하나씩 들어 있습니다.
항목에는 아이디도 있는데, 실행마다 바뀌어 출력하지 않고 질문 값만 꺼냅니다."""),
        code(MARKS),
        md("""**결과 읽기** — 출력 줄 `멈춤 표시 수: 1`과 `멈춤 표시의 종류: Interrupt`가 보입니다.
출력 줄 `질문 값: {'order_key': 'order-2401', 'question': '결제할까요?'}`는 노드가 함수 `interrupt`에 넣은 딕셔너리 그대로입니다.
실제 서비스라면 이 질문 값을 화면에 띄우고, 사람이 고른 답을 받습니다.

## 3. 멈춘 동안 저장된 것

그래프가 멈춘 동안 체크포인터에 무엇이 남았는지, Ch 23 01절의 `get_state`로 읽습니다.
다음 셀은 다음에 실행할 노드와 저장된 칸 값을 봅니다."""),
        code(PAUSED_STATE),
        md("""**결과 읽기** — 출력 줄 `다음에 실행할 노드: ('ask_only',)`와 `저장된 칸 값: {'order_key': 'order-2401', 'answer': '대기'}`입니다.
노드 `ask_only`는 끝나지 않아, 다음에 실행할 노드로 남았습니다.
Ch 23 05절에서 실패로 멈춘 노드가 다음 노드로 남았던 것과 같은 자리입니다.

다음 셀은 속성 `tasks`로 멈춘 작업을 봅니다.
Ch 23 05절에서 실패한 작업의 오류를 읽었던 속성입니다.
이번에는 작업에 딸린 멈춤 표시의 질문 값을 읽고, 체크포인트 수도 셉니다."""),
        code(PAUSED_TASK),
        md("""**결과 읽기** — 출력 줄 `멈춘 작업의 노드: ask_only`와 `체크포인트 수: 2`가 보입니다.
출력 줄 `작업에 딸린 질문 값: {'order_key': 'order-2401', 'question': '결제할까요?'}`로, 질문 값도 저장되었습니다.
그래서 그래프는 사람이 답할 때까지 기다릴 수 있습니다.
체크포인트 둘은 입력을 받은 때와 입력을 칸에 넣은 뒤이고, 노드를 마친 뒤의 것은 아직 없습니다.

사람의 답으로 이어 가기는 멈춘 스레드에 사람의 답을 넘겨, 멈춘 노드부터 실행을 이어 가는 일입니다.
도미노 줄의 빈자리에 사람이 도미노 하나를 놓으면, 뒤쪽 줄이 다시 넘어가기 시작하는 것과 같습니다.
이 절 코드에서는 `Command(resume=답)`을 `invoke`에 넣는 줄입니다.
자리 `resume`에 넣은 값이, 노드 안 함수 `interrupt`가 내놓는 값이 됩니다.
비유와 달리 실제 그래프는 멈춘 줄이 아니라 노드의 첫 줄부터 다시 실행하고, 다음 셀에서 그 모습을 봅니다.

Ch 23 03절의 스레드 재개는 객체를 새로 만든 뒤 같은 스레드로 대화를 이어 가는 일이었습니다.
Ch 23 04·06절 스크립트의 단계 `resume`은 강제 종료 뒤 새 프로세스로 다시 실행하는 단계였습니다.
이름에 같은 영어 낱말이 들어 있어도, 사람의 답을 넣어 이어 가는 이 절의 장면과는 다릅니다.

다음 셀은 사람의 답 `approve`로 이어 갑니다.
실행 전에 예상해 봅니다.
노드가 처음부터 다시 실행되어 시작 줄이 한 번 더 찍히고, 이번에는 답을 받을 것입니다."""),
        code(RESUME_ASK),
        md("""**결과 읽기** — 출력 첫 줄 `노드 ask_only 시작`이 이 셀에서 한 번 더 찍혔습니다.
노드는 멈춘 줄이 아니라 첫 줄부터 다시 실행되었습니다.
출력 줄 `받은 답: approve`로, 함수 `interrupt`가 이번에는 멈추지 않고 사람의 답을 내놓았습니다.
출력 줄 `이어 간 뒤 결과: {'order_key': 'order-2401', 'answer': 'approve'}`에는 키 `__interrupt__`가 없습니다.

공식 문서도 이어 갈 때 멈춘 줄이 아니라 노드 전체를 처음부터 다시 시작한다고 적습니다.
다음 셀은 이어 간 뒤의 체크포인트를 봅니다."""),
        code(DONE_ASK),
        md("""**결과 읽기** — 출력 줄 `다음에 실행할 노드: ()`와 `체크포인트 수: 3`입니다.
멈춘 동안의 둘에, 노드를 마친 뒤의 하나가 더해졌습니다.
Ch 23 01절에서 노드 하나짜리 그래프를 한 번 실행했을 때 쌓인 수와 같습니다.
노드는 두 번 시작했지만 끝난 것은 한 번이라, 체크포인트도 하나만 늘었습니다.

## 4. 적고 나서 묻는 노드 (Before)""", lesson_part="before"),
        md("""이제 승인 지점 앞뒤에 부작용을 둡니다.
부작용은 Ch 23 06절처럼 결제 기록 파일에 주문 키를 한 줄 적는 일입니다.
먼저 결제 기록을 적은 뒤에 묻는 노드를 만듭니다.
3절에서 본 대로, 노드는 이어 갈 때 처음부터 다시 실행된다는 점을 떠올려 봅니다.""", lesson_part="before"),
        code(DEF_BEFORE, lesson_part="before"),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `append_key`는 부를 때마다 기록 파일 끝에 키 한 줄을 적습니다.
이 노드에서는 그 줄이 멈춤 표시보다 앞에 있습니다.

다음 셀은 2절과 같은 모양으로, 이 노드 하나짜리 그래프를 만듭니다.""", lesson_part="before"),
        code(BUILD_BEFORE, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['charge_then_ask']`입니다.

다음 셀은 첫 실행을 합니다.
기록 파일 이름은 `before.record`, 스레드 이름은 `before`입니다.
실행 전에 예상해 봅니다.
노드는 묻기 전에 기록을 적으니, 멈춘 지금 파일에는 키가 한 줄 있을 것입니다.""", lesson_part="before"),
        code(FIRST_BEFORE, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `노드 charge_then_ask 시작`과 `결제 기록: 적음` 다음에 그래프가 멈췄습니다.
출력 줄 `멈춤 표시 수: 1`로, 멈춤 표시가 하나 남았습니다.
출력 줄 `멈춘 뒤 기록 파일의 키: ['order-2401']`입니다.
사람이 아직 답하지 않았는데, 결제 기록은 이미 한 줄 적혔습니다.

다음 셀은 사람의 답 `reject`로 이어 갑니다.
거절이니 결제 기록은 남지 않아야 합니다.
실행 전에 예상해 봅니다.
노드가 처음부터 다시 실행되니, 기록을 한 번 더 적을 것입니다.""", lesson_part="before"),
        code(RESUME_BEFORE, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `노드 charge_then_ask 시작`과 `결제 기록: 적음`이 이 셀에서 한 번 더 찍혔습니다.
출력 줄 `받은 답: reject`와 `칸 answer: reject`로, 사람은 거절했습니다.
그런데 출력 줄 `기록 파일의 키: ['order-2401', 'order-2401']`과 `같은 키가 적힌 줄 수: 2`입니다.
거절했는데도 결제 기록이 두 줄 남았습니다.
이것이 이 절의 Before 결함입니다.

결함은 둘입니다.
하나는 사람이 답하기 전에 이미 적었다는 것입니다.
다른 하나는 이어 갈 때 노드가 처음부터 다시 실행되어, 한 번 더 적었다는 것입니다.
승인 지점을 두었어도, 부작용이 그 앞에 있으면 거절이 쓰기를 막지 못합니다.""", lesson_part="before"),
        md("""## 5. 묻고 나서 적는 노드 (After)

이제 결함을 고칩니다.
바꾸는 것은 노드 안 줄의 차례 하나입니다.
먼저 묻고, 받은 답이 `approve`일 때만 결제 기록을 적습니다.""", lesson_part="after"),
        code(DEF_AFTER, lesson_part="after"),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
멈춤 표시 앞에는 파일을 건드리는 줄이 없습니다.
그래서 이어 갈 때 노드가 처음부터 다시 실행되어도, 멈추기 전에 적는 일은 없습니다.
답이 `approve`가 아니면 쓰는 줄을 건너뛰고, 답만 칸에 냅니다.

다음 셀은 4절과 같은 모양으로 그래프를 만듭니다.""", lesson_part="after"),
        code(BUILD_AFTER, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['ask_then_charge']`입니다.

다음 셀은 4절과 같은 주문 키로 첫 실행을 합니다.
기록 파일 이름은 `after-reject.record`, 스레드 이름은 `after-reject`입니다.
파일이 있는지는 Ch 23 04절에서 쓴 함수 `os.path.exists`로 봅니다.
실행 전에 예상해 봅니다.
묻기 전에는 적지 않으니, 멈춘 지금 기록 파일은 없을 것입니다.""", lesson_part="after"),
        code(FIRST_REJECT, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `노드 ask_then_charge 시작` 다음에 그래프가 멈췄고, 출력 줄 `멈춤 표시 수: 1`이 보입니다.
출력 줄 `기록 파일이 있는가: False`로, 멈춘 지금 기록 파일이 없습니다.

다음 셀은 4절과 같은 답 `reject`로 이어 갑니다.
실행 전에 예상해 봅니다.
노드는 처음부터 다시 실행되지만, 답이 거절이라 파일은 여전히 없을 것입니다.""", lesson_part="after"),
        code(RESUME_REJECT, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `노드 ask_then_charge 시작`이 이 셀에서 한 번 더 찍혔고, `받은 답: reject`가 뒤따릅니다.
출력 줄 `칸 answer: reject`와 `기록 파일이 있는가: False`입니다.
노드는 4절처럼 두 번 시작했지만, 결제 기록은 한 줄도 남지 않았습니다.
사람의 거절이 쓰기를 막았습니다.

값 바꿔 보기: 사람의 답 하나만 `approve`로 바꿉니다.
스레드와 기록 파일은 새 이름 `after-approve`를 씁니다.
다음 셀은 첫 실행입니다.
실행 전에 예상해 봅니다.
여기까지는 거절 때와 같이, 멈춘 지금 기록 파일이 없을 것입니다.""", lesson_part="after"),
        code(FIRST_APPROVE, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `멈춤 표시 수: 1`과 `기록 파일이 있는가: False`는 거절 때의 첫 실행과 같습니다.

다음 셀은 사람의 답 `approve`로 이어 갑니다.
실행 전에 예상해 봅니다.
이어 갈 때 쓰는 줄에 한 번 닿으니, 결제 기록은 한 줄일 것입니다.""", lesson_part="after"),
        code(RESUME_APPROVE, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `받은 답: approve` 다음에 `결제 기록: 적음`이 찍혔습니다.
출력 줄 `기록 파일의 키: ['order-2401']`과 `같은 키가 적힌 줄 수: 1`입니다.
승인하자 결제 기록이 한 줄 남았습니다.
쓰는 줄이 멈춤 표시 뒤에 있어, 노드가 두 번 시작해도 한 번만 적었습니다.

## 6. 묻기 전에 꼭 적어야 한다면

되돌리기 어려운 일은 5절처럼 묻고 나서 합니다.
그런데 사람이 답하기 전에 남겨야 하는 기록도 있습니다.
예를 들어 요청을 받았다는 접수 기록은 묻기 전에 적어 둘 수 있습니다.
공식 문서는 멈춤 표시 앞의 부작용을 되도록 멱등하게 만들라고 적습니다.
Ch 23 06절에서 멱등성은 몇 번 실행해도 결과가 한 번 실행한 것과 같은 성질이었습니다.

다음 셀은 4절 노드에서 쓰는 함수 하나만 `append_key_once`로 바꾼 노드입니다.
적는 곳은 결제 기록이 아니라 접수 기록 파일입니다.""", lesson_part="after"),
        code(DEF_RECEIVE, lesson_part="after"),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `append_key_once`는 Ch 23 06절에서 배운 함수이고, 주문 키가 멱등 키입니다.

다음 셀은 이 노드 하나짜리 그래프를 만듭니다.""", lesson_part="after"),
        code(BUILD_RECEIVE, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['receive_then_ask']`입니다.

다음 셀은 기록 파일 이름 `receipt.record`로 첫 실행을 하고, 4절과 같은 답 `reject`로 이어 갑니다.
실행 전에 예상해 봅니다.
노드는 두 번 시작하지만, 둘째에는 이미 적힌 키를 찾아 건너뛸 것입니다.""", lesson_part="after"),
        code(RUN_RECEIVE, lesson_part="after"),
        md("""**결과 읽기** — 첫 실행에서 `접수 기록: 적음`이, 이어 갈 때 `접수 기록: 건너뜀`이 찍혔습니다.
출력 줄 `멈춘 뒤 접수 기록의 키: ['order-2401']`과 `이어 간 뒤 접수 기록의 키: ['order-2401']`이 같습니다.
노드는 두 번 시작했지만, 접수 기록은 한 줄만 남았습니다.
출력 줄 `칸 answer: reject`처럼 거절했어도, 이 한 줄은 남습니다.
그래서 멱등하게 적는 방법은 접수 기록처럼 거절돼도 남아도 되는 쓰기에만 씁니다.

다음 셀은 4~6절의 네 장면을 한 목록에 모읍니다.
사람의 답은 각 장면의 결과에서 칸 `answer`를 꺼내 씁니다.""", lesson_part="after"),
        code(SCENES, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `모은 장면 수: 4`입니다.

다음 셀은 장면마다 기록 파일에 같은 주문 키가 적힌 줄 수를 세어, 한 줄씩 출력합니다.
기록 파일이 없으면 줄 수를 0으로 둡니다.""", lesson_part="after"),
        code(TABLE, lesson_part="after"),
        md("""**결과 읽기** — 라벨 줄 아래 첫 줄은 `charge_then_ask | reject | before.record | 2`입니다.
그 아래 세 줄은 `ask_then_charge | reject | after-reject.record | 0`과 `ask_then_charge | approve | after-approve.record | 1`, `receive_then_ask | reject | receipt.record | 1`입니다.
같은 거절이라도 적는 줄이 멈춤 표시 앞에 있으면 기록이 남았습니다.
멈춤 표시 뒤에서 적으면 승인일 때만 한 줄이었습니다.

다음 셀은 작업 폴더에 남은 파일을 봅니다.""", lesson_part="after"),
        code(FILES_END, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `작업 폴더의 파일: ['after-approve.record', 'before.record', 'receipt.record']`와 `파일 수: 3`입니다.
거절한 `after-reject.record`는 만들어지지 않았습니다.
이 파일들은 모두 임시 폴더에 있어, 실습 폴더에는 남지 않습니다.

## 정리

1. 노드 안에서 함수 `interrupt`를 부르자 그래프가 멈추고, 결과의 키 `__interrupt__`에 질문 값이 남았습니다.
2. 사람의 답을 `Command(resume=…)`에 담아 이어 가자, 노드가 처음부터 다시 실행되었습니다.
3. 적고 나서 묻는 노드는 거절에도 결제 기록을 두 줄 남겼고, 묻고 나서 적는 노드는 거절이면 0줄이었습니다.

02절에서는 사람의 답을 검사해, 허용하지 않는 값이면 다시 묻는 방법을 봅니다.""", lesson_part="after"),
    ]


# ---------------------------------------------------------------- _src 본문
def html_text(text: str) -> str:
    """노트북용 마크다운 한 단락(백틱·줄바꿈)을 _src 문단 글로 바꿉니다(Ch 23 01 생성기와 같은 함수)."""
    parts = text.replace("\n", " ").split("`")
    out = ""
    for index in range(len(parts)):
        if index % 2 == 1:
            out = out + "<code>" + parts[index] + "</code>"
        else:
            out = out + parts[index]
    return out


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


L_CH13_01 = "../../part4/ch13-langgraph-basics/01-StateGraph와-노드-엣지.html"
L_CH13_06 = "../../part4/ch13-langgraph-basics/06-Command-갱신과-이동.html"
L_CH17_02 = "../../part5/ch17-agent-overview/02-워크플로우가-충분한-조건.html"
L_CH17_03 = "../../part5/ch17-agent-overview/03-모델-도구-루프와-정지-조건.html"
L_CH18_01 = "../../part5/ch18-workflow-patterns/01-게이트가-있는-프롬프트-체이닝.html"
L_CH19_06 = "../../part5/ch19-model-tools/06-오류와-읽기-쓰기-분리.html"
L_CH23_01 = "../ch23-persistence/01-체크포인터와-스레드.html"
L_CH23_03 = "../ch23-persistence/03-스레드-재개와-대화-이어가기.html"
L_CH23_04 = "../ch23-persistence/04-내구-실행-모드-비교.html"
L_CH23_05 = "../ch23-persistence/05-pending-writes와-장애-복구.html"
L_CH23_06 = "../ch23-persistence/06-노드-재시작과-멱등성.html"
L_CH23_07 = "../ch23-persistence/07-Persistence-실습.html"
L_02 = "02-Command-resume으로-실행-재개.html"
L_03 = "03-상태-기록과-다른-분기-재실행.html"

COMPARE_ROWS = [
    ("사람의 답", "<code>reject</code>", "<code>reject</code>"),
    ("멈춘 뒤 기록 파일", "<code>['order-2401']</code>", "없음(<code>False</code>)"),
    ("노드가 시작한 횟수", "두 번(첫 실행 · 이어 갈 때)", "두 번(첫 실행 · 이어 갈 때)"),
    ("이어 간 뒤 칸 <code>answer</code>", "<code>reject</code>", "<code>reject</code>"),
    ("이어 간 뒤 같은 키가 적힌 줄 수", "2", "0(파일 없음)"),
    ("값 바꿔 보기: 답 <code>approve</code>", "—", "1"),
]

LOOK_B5 = "노트북 2절에서 첫 실행의 출력이 <code>노드 ask_only 시작</code> 한 줄뿐이고, 결과에 키 <code>__interrupt__</code>가 있는지 봅니다. 3절에서 멈춘 동안 <code>다음에 실행할 노드: ('ask_only',)</code>와 <code>체크포인트 수: 2</code>인지 확인합니다. 이어 간 셀에서 시작 줄이 한 번 더 찍히고, <code>받은 답: approve</code>와 <code>체크포인트 수: 3</code>이 나오는지 봅니다."
LOOK_B6 = "Before 마지막 셀에서 <code>칸 answer: reject</code>인데 <code>같은 키가 적힌 줄 수: 2</code>인지 봅니다. After에서 같은 거절 뒤 <code>기록 파일이 있는가: False</code>, 승인 뒤 <code>같은 키가 적힌 줄 수: 1</code>인지 확인합니다. 6절 견주기의 줄 <code>receive_then_ask | reject | receipt.record | 1</code>도 봅니다."


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


def mermaid_block(name: str, alt: str, caption: str, reading: str) -> str:
    return ("{{mermaid:" + name + "|" + alt + "|" + caption + "}}\n"
            + '<p class="look"><b>도식 읽기</b> — ' + html_text(reading) + "</p>\n")


def src_html() -> str:
    compare = table_html(["견준 것", "Before(<code>charge_then_ask</code>)", "After(<code>ask_then_charge</code>)"], COMPARE_ROWS)
    return """<!--meta: 강의 1h | 실습 1.5h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>노드 안의 멈춤 표시로 그래프를 멈추고, 사람의 답을 넣어 같은 스레드를 이어 갈 수 있습니다.</li>
<li>멈춘 동안 체크포인트에 남은 다음 노드와 질문 값을 읽을 수 있습니다.</li>
<li>같은 거절을 넣어, 부작용을 멈춤 표시 앞에 둔 노드와 뒤에 둔 노드의 기록을 견줄 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>결제·배포·삭제처럼 되돌리기 어려운 일은 모델이나 코드가 혼자 정하지 않고, 사람이 먼저 확인하게 합니다. <a href=\"""" + L_CH17_02 + """\">Ch 17 02절</a>은 이런 자리를 승인 지점이라고 불렀습니다. 그런데 확인을 묻는 자리가 쓰기 뒤에 있으면, 사람이 거절해도 기록은 이미 남습니다. 이 절은 그래프 안에 승인 지점을 두고, 묻는 자리와 쓰는 자리의 차례가 결과를 바꾸는지 기록 파일로 셉니다.</p><p>챕터 제목의 Human-in-the-Loop는 실행 흐름 가운데에 사람의 확인을 끼워 넣는 방식입니다. Time Travel은 지난 체크포인트로 돌아가 다시 실행하는 일이고, <a href=\"""" + L_03 + """\">03절</a>에서 다룹니다. 절 제목의 interrupt는 그래프를 멈추는 함수 이름이고, 「승인 게이트」는 승인 지점과 같은 뜻입니다. <a href=\"""" + L_CH18_01 + """\">Ch 18 01절</a>의 게이트(중간 결과를 코드로 검사하는 자리)와는 다른 말이라, 본문에서는 승인 지점이라고 씁니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH17_02 + """\">Ch 17 02절</a>에서는 부작용이 생기는 단계 앞에서 사람이 확인하는 자리를 승인 지점이라고 불렀습니다. <a href=\"""" + L_CH17_03 + """\">Ch 17 03절</a>의 사람 확인은 그 자리에 닿으면 반복을 멈추고 사람에게 넘겼고, 이어 가지는 않았습니다. <a href=\"""" + L_CH19_06 + """\">Ch 19 06절</a>에서는 사람 확인 값이 참일 때만 쓰기 도구를 모델에게 알렸습니다. 이 절은 멈춘 뒤 사람의 답을 받아 같은 실행을 이어 갑니다.</p><p>Ch 23 <a href=\"""" + L_CH23_06 + """\">06절</a>·<a href=\"""" + L_CH23_07 + """\">07절</a>에서는 노드가 장애 뒤 처음부터 다시 실행될 수 있음을 확인했습니다. 그래서 바깥 쓰기에는 멱등성이 필요했습니다. 체크포인터는 <a href=\"""" + L_CH23_01 + """\">Ch 23 01절</a>의 <code>InMemorySaver</code>를 씁니다. 결제 흉내인 기록 파일과 함수 셋(<code>append_key</code>·<code>append_key_once</code>·<code>read_record</code>)은 Ch 23 04·06절 그대로이고, 도구 파일에서 가져옵니다. <a href=\"""" + L_CH13_06 + """\">Ch 13 06절</a>의 객체 <code>Command</code>는 갱신과 다음 노드 이름을 담았는데, 이 절에서는 다른 자리 <code>resume</code>을 씁니다.</p><p><a href=\"""" + L_CH23_03 + """\">Ch 23 03절</a>의 스레드 재개는 객체를 새로 만든 뒤 같은 스레드로 대화를 이어 가는 일이었습니다. <a href=\"""" + L_CH23_04 + """\">Ch 23 04절</a>·06절 스크립트의 단계 <code>resume</code>은 강제 종료 뒤 새 프로세스로 다시 실행하는 단계였습니다. 이 절은 멈춰 기다리던 실행에 사람의 답을 넣어 이어 가고, 이 일을 「사람의 답으로 이어 가기」라고 부릅니다. 영어 낱말 resume이 겹쳐도 세 장면은 서로 다릅니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>도미노 줄을 세우면서 가운데 한 자리를 비워 둔다고 합시다. 앞에서 넘어진 도미노는 빈자리에서 멈춥니다. 사람이 그 자리에 도미노 하나를 놓아야 뒤쪽 줄이 이어 넘어갑니다. 아무것도 놓지 않으면 빈자리 뒤는 그대로 서 있습니다.</p><p>줄 끝에 컵을 두면, 컵은 사람이 빈자리에 도미노를 놓았을 때만 넘어집니다. 그런데 컵을 빈자리 앞에 두면, 사람이 정하기도 전에 넘어집니다. 빈자리가 멈춤 표시, 빈자리에 도미노를 놓는 일이 사람의 답, 넘어진 컵이 결제 기록입니다.</p><p>비유와 다른 점이 하나 있습니다. 실제 그래프는 이어 갈 때 멈춘 노드의 첫 줄부터 다시 실행합니다. 도미노로 말하면 빈자리 앞의 몇 개를 다시 세워 한 번 더 넘기는 셈입니다. 그래서 빈자리 앞에 둔 컵은 이어 갈 때 한 번 더 쓰러집니다(노트북 4절의 두 줄).</p>
""" + illustration_block() + """<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>멈춤 표시(interrupt)</td><td>노드가 그 자리에서 그래프를 멈추고, 사람에게 보일 값을 남기는 일입니다. 도미노 줄에 비워 둔 자리에서 넘어지던 줄이 멈추는 것과 같습니다. 이 절에서는 노드 안에서 함수 <code>interrupt</code>를 부르는 줄이고, 멈춘 결과의 키 <code>__interrupt__</code>에 표시가 남습니다.</td></tr><tr><td>질문 값</td><td>멈춤 표시와 함께 사람에게 보일 값입니다. 빈자리 옆에 세워 둔 안내판처럼, 무엇을 정해야 하는지 알려 줍니다. 이 절에서는 주문 키와 질문 글 <code>결제할까요?</code>를 담은 딕셔너리입니다.</td></tr><tr><td>사람의 답으로 이어 가기</td><td>멈춘 스레드에 사람의 답을 넘겨, 멈춘 노드부터 실행을 이어 가는 일입니다. 빈자리에 사람이 도미노를 놓으면 뒤쪽 줄이 다시 넘어가는 것과 같습니다. 다만 실제 그래프는 멈춘 줄이 아니라 노드의 첫 줄부터 다시 실행합니다. 이 절에서는 <code>Command(resume=답)</code>을 <code>invoke</code>에 넣고, 그 답이 노드 안 <code>interrupt</code>가 내놓는 값이 됩니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 멈춤 표시는 노트북 2절 출력 <code>결과의 키: ['order_key', 'answer', '__interrupt__']</code>에서 보입니다. 질문 값은 출력 <code>질문 값: {'order_key': 'order-2401', 'question': '결제할까요?'}</code>입니다. 사람의 답으로 이어 가기는 3절에서 답 <code>approve</code>를 넣은 셀이고, 출력 <code>받은 답: approve</code>가 그 결과입니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>이어 갈 때 노드를 처음부터 다시 실행하는 까닭</h3><p>설치판 소스 <code>langgraph/types.py</code> 858~864행의 설명은 이렇게 적습니다. 노드 안에서 함수 <code>interrupt</code>를 처음 부르면 오류 <code>GraphInterrupt</code>를 일으켜 실행을 멈춥니다. 이어 갈 때는 노드의 첫 줄부터 모든 줄을 다시 실행합니다. 공식 문서도 멈춘 줄이 아니라 노드 전체를 처음부터 다시 시작한다고 적습니다.</p><p>다시 실행된 노드가 같은 <code>interrupt</code>에 닿으면, 이번에는 멈추지 않고 넘겨받은 사람의 답을 내놓습니다. 그래서 <code>interrupt</code> 앞의 줄은 첫 실행과 이어 가기에서 두 번 실행됩니다. 노트북 3절에서 <code>노드 ask_only 시작</code>이 두 번 찍힌 것이 이 모습입니다. 같은 까닭으로, 설치판 870~871행은 멈춘 자리를 저장할 체크포인터가 있어야 한다고 적습니다.</p>
<h3>다른 상황에 적용</h3><p>보내기·삭제·배포처럼 되돌리기 어려운 일은 모두 이 절의 결제 기록과 같습니다. 이런 일을 하는 노드에서는 먼저 묻고, 승인일 때만 합니다. 묻기 전에 꼭 해야 하는 쓰기는 <a href=\"""" + L_CH23_06 + """\">Ch 23 06절</a>처럼 멱등 키로 한 번만 반영되게 적습니다. 노트북 6절에서 접수 기록을 <code>append_key_once</code>로 적자, 이어 간 뒤에도 한 줄이었습니다. 다만 그 한 줄은 거절해도 남으므로, 되돌리기 어려운 일에는 이 방법을 쓰지 않습니다.</p><p>어떤 도구·어떤 인자에 승인 지점을 둘지는 서비스가 정할 일입니다. 이 절은 쓰기 하나만 다루었고, 읽기만 하는 일에 묻는 장면은 만들지 않았습니다.</p>
<h3>비교와 경계</h3><p>Ch 17 03절의 사람 확인에는 멈춘 뒤 이어 가는 코드가 없었습니다. 이 절의 멈춤 표시는 체크포인터에 멈춘 자리와 질문 값을 남겨, 사람의 답을 받은 뒤 같은 스레드로 이어 갑니다. <a href=\"""" + L_CH23_05 + """\">Ch 23 05절</a>·07절의 <code>invoke(None, config)</code>는 원인을 없앤 뒤 새 입력 없이 이어 갔습니다. 이 절은 사람의 답을 담은 <code>Command</code>를 넣어 이어 갑니다. 받은 답을 검사해, 허용하지 않는 값이면 다시 묻는 일은 <a href=\"""" + L_02 + """\">02절</a>에서 다룹니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 질문만 하는 노드로 멈춤 표시와 사람의 답을 봅니다. 멈춘 동안 <code>get_state</code>로 다음 노드와 질문 값, 체크포인트 수를 읽습니다. 예시 부분은 여기까지이고, 결제 기록을 적는 두 노드는 이 페이지 6블록의 Before와 After에 있습니다.</p><p>이 절은 모델을 부르지 않아 모델 요청은 0번이고, API 키 셀도 없습니다. 사람의 답도 셀에 적은 값(<code>approve</code>·<code>reject</code>)이라, 같은 입력에 늘 같은 출력이 나옵니다. 실제 서비스라면 질문 값을 화면에 띄우고, 사람이 고른 답을 같은 자리에 넣습니다. 기록 파일은 노트북이 만든 빈 임시 폴더에 생깁니다.</p>
{{notebook:""" + SLUG + """|example}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>일부러 실패해 보기</h2><p>아래 Before 셀은 결제 기록을 먼저 적고 묻는 노드에 거절을 넣습니다. After 셀은 노드 안 줄의 차례만 바꿔, 같은 거절과 승인을 넣습니다. 노트북 6절은 묻기 전에 꼭 적어야 하는 접수 기록을 멱등하게 적고, 네 장면을 한 표로 견줍니다.</p>
{{notebook:""" + SLUG + """|failure}}
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + compare + """
<p>두 노드 모두 같은 주문 키와 같은 거절을 받았고, 노드는 두 번 시작했습니다. 달랐던 것은 쓰는 줄이 멈춤 표시 앞에 있었는지입니다. Before 노드는 첫 실행에서 한 줄을 적고, 이어 갈 때 처음부터 다시 실행되며 한 줄을 더 적었습니다. After 노드는 멈춤 표시 뒤에서 답을 먼저 보았고, 거절이라 쓰는 줄에 닿지 않았습니다.</p><p>값 바꿔 보기에서 답만 <code>approve</code>로 바꾸자, After는 이어 갈 때 한 번만 적었습니다. 쓰는 줄이 멈춤 표시 뒤에 있으면, 노드가 두 번 시작해도 적는 것은 승인 뒤 한 번뿐입니다. 승인 지점은 부작용 앞에 두어야 거절이 쓰기를 막습니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>6절의 <code>receive_then_ask</code>는 멈춤 표시 앞에서 접수 기록을 적었지만, 이어 갈 때 이미 적힌 키를 찾아 건너뛰었습니다. 그래서 두 번 시작해도 한 줄이었습니다. 이것이 <a href=\"""" + L_CH23_06 + """\">Ch 23 06절</a> 멱등 쓰기의 쓰임새이고, 같은 일을 두 번 반영하지 않게 하는 방법입니다. 다만 거절했어도 그 한 줄은 남았으므로, 되돌리기 어려운 일은 묻고 나서 합니다.</p><p>모델을 부르지 않아, 노트북 출력은 새 커널로 다시 실행해도 같아야 합니다. """ + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>함수 <code>interrupt</code>를 <code>try</code>·<code>except</code>로 감싸지 않습니다. 공식 문서는 멈춤이 특별한 오류로 일어나, 감싸면 그 오류를 받아 버려 그래프에 전해지지 않는다고 적습니다. 노트북 밖 확인에서 <code>except Exception</code>으로 감싸자 오류 <code>GraphInterrupt</code>를 받고, 멈추지 않은 채 노드가 끝났습니다. 이 장면은 노트북에서 실행하지 않았습니다.</li><li>질문 값에는 JSON으로 적을 수 있는 값(글·수·목록·딕셔너리)만 넣습니다. 공식 문서는 체크포인터에 따라 함수 같은 값은 저장하지 못할 수 있다고 적습니다. 이 절은 딕셔너리만 넣어 보았습니다.</li><li>이 절의 After 노드는 <code>approve</code>가 아닌 답을 모두 쓰지 않는 쪽으로 다룹니다. <code>approve</code>·<code>reject</code> 말고 다른 글은 이번에 넣어 보지 않았습니다. 허용하지 않는 답을 알려 주고 다시 묻는 일은 <a href=\"""" + L_02 + """\">02절</a>에서 봅니다.</li><li>6절의 멱등 키 확인은 Ch 23 06절처럼 기록 파일을 읽은 뒤에 적는 방식이고, 한 커널 안에서만 보았습니다. 여러 프로그램이 같은 파일에 함께 쓰는 장면은 실행하지 않았습니다.</li><li>멈춤 표시 항목에는 아이디도 들어 있지만, 실행마다 바뀌어 출력하지 않았습니다. 체크포인트 수 2·3은 노드 하나짜리 이 그래프의 값입니다.</li><li>셀 하나만 다시 실행하면 같은 스레드와 같은 기록 파일에 이어 적어, 줄 수가 달라집니다. 처음 값으로 다시 보려면 1절 임시 폴더 셀부터 다시 실행합니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>노드 안에서 함수 <code>interrupt</code>를 부르자 그래프가 멈추고, 결과의 키 <code>__interrupt__</code>에 질문 값이 남았습니다.</li><li>사람의 답을 <code>Command(resume=…)</code>에 담아 이어 가자, 노드가 처음부터 다시 실행되어 답을 받았습니다.</li><li>적고 나서 묻는 노드는 거절에도 결제 기록을 두 줄 남겼고, 묻고 나서 적는 노드는 거절이면 0줄, 승인이면 한 줄이었습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_02 + """\">02절</a>에서는 사람의 답을 검사해, 허용하지 않는 값이면 다시 묻는 방법을 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 첫 실행에서 노드 <code>ask_only</code>의 <code>받은 답:</code> 줄이 찍히지 않은 까닭은 무엇인가요?</p><p class="quiz-a">함수 <code>interrupt</code>가 처음 불린 줄에서 그래프를 멈춰, 그 아래 줄까지 가지 않았기 때문입니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">2. 사람의 답으로 이어 간 셀에서 <code>노드 ask_only 시작</code>이 한 번 더 찍힌 까닭은 무엇인가요?</p><p class="quiz-a">이어 갈 때 노드를 멈춘 줄이 아니라 첫 줄부터 다시 실행하기 때문입니다. 다시 만난 <code>interrupt</code>는 멈추지 않고 사람의 답을 내놓았습니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">3. 노드 <code>charge_then_ask</code>에 거절을 넣었는데 같은 키가 두 줄 남은 까닭은 무엇인가요?</p><p class="quiz-a">묻기 전에 첫 실행에서 한 줄을 적었고, 이어 갈 때 노드가 처음부터 다시 실행되며 한 줄을 더 적었기 때문입니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">4. 접수 기록을 <code>append_key_once</code>로 적은 노드는 거절해도 한 줄이 남았습니다. 결제 기록에 이 방법을 쓰지 않는 까닭은 무엇인가요?</p><p class="quiz-a">멱등하게 적으면 두 줄은 막지만, 묻기 전에 적은 한 줄은 거절해도 남기 때문입니다. 되돌리기 어려운 일은 묻고 나서 승인일 때만 합니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langgraph/interrupts">LangGraph Interrupts</a></div>확인 2026-09-25 · 멈춤 표시를 쓰려면 체크포인터와 스레드 이름이 있어야 한다고 적습니다. 이어 갈 때 노드 전체를 처음부터 다시 시작하고, 멈춤 표시 앞의 부작용은 되도록 멱등해야 한다고도 적습니다.</li><li>같은 문서는 멈춤 표시를 <code>try</code>로 감싸지 말고, 질문 값은 저장할 수 있는 값만 쓰라고 적습니다. 기본 <code>invoke</code>의 결과 키 <code>__interrupt__</code>와, <code>Command(resume=…)</code>의 값이 <code>interrupt</code>가 내놓는 값이 된다는 점도 적습니다.</li><li>langgraph 1.2.11 소스 <code>langgraph/types.py</code> 851~871행 — 함수 <code>interrupt</code>의 설명입니다. 처음 부르면 멈추고, 이어 갈 때 노드를 처음부터 다시 실행하며, 체크포인터가 있어야 한다고 적습니다.</li><li>같은 판 <code>langgraph/errors.py</code> 50행과 102행은 오류 <code>GraphInterrupt</code>가 <code>Exception</code>을 잇는 자리입니다.</li><li>Ch 17 02절에서 승인 지점을, Ch 23 06절에서 멱등 쓰기를, Ch 13 06절에서 객체 <code>Command</code>를 보았습니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    check_same_as_ch23()
    # 임시 폴더 셀은 Ch 23 01절 셀에서 앞머리 ch23-01- → ch24-01-(세 곳)과 선례 절 이름만 다르다
    assert FOLDER.count("ch24-01-") == 3 and "ch23" not in FOLDER
    assert FOLDER.replace("ch24-01-", "ch23-01-").replace("(Ch 23 01절과 같은 모양)", "(Ch 4 03절과 같은 모양)") == CH23_FOLDER
    ch23_author = ROOT / "textbook/part6/ch23-persistence/qa/upgrade/author_01.py"
    assert CH23_FOLDER in ch23_author.read_text(encoding="utf-8")
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "approval_tools.py").write_text(TOOLS, encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        # 도구 파일은 없거나 이 판과 같을 때만 쓴다. 뒤 절(03)이 함수를 더한 판이면 덮어쓰지 않는다(마감 A-10).
        current = ""
        if TOOLS_PATH.is_file():
            current = TOOLS_PATH.read_text(encoding="utf-8")
        assert current == "" or current.startswith(TOOLS), "도구 파일이 01절 판으로 시작하지 않습니다"
        if current == "" or current == TOOLS:
            TOOLS_PATH.write_text(TOOLS, encoding="utf-8")
            print("wrote", TOOLS_PATH)
        else:
            print("skip", TOOLS_PATH, "(뒤 절이 함수를 더한 판 — 덮어쓰지 않음)")
        path = write_notebook(LAB, "01", SLUG, "paired", cells())
        print("wrote", path)
