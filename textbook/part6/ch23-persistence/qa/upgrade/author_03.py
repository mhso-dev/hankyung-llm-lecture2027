"""Ch 23 03절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 author_03.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_03.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**(chapter.json). 슬러그 그대로.

## 결정 1 — 메시지 칸에 코드가 만든 메시지 (챕터 리드 결정 1, M3)

상태 형식은 Ch 13 04절 모양의 메시지 칸(`add_messages`) 하나. 입력은 HumanMessage, 답은 노드 함수 reply가
사람 메시지 수를 세어 만든 AIMessage(「N번째 질문을 받았습니다」 — 모델 글이 아님). 메시지는 종류(클래스 이름)와 글로
출력한다(Ch 22 09 b8 「종류별로 출력한 대화 기록」). 메시지 번호(id)는 add_messages가 uuid4로 붙여 실행마다 달라 출력하지 않는다.
메시지 클래스는 langchain-core에서 가져온다(langchain 1.4.0 langchain/messages/__init__.py 7행이 같은 클래스를 다시 내놓음).

## 결정 2 — SQLite 파일은 임시 폴더에 (챕터 리드 결정 2)

준비 셀 셋(설치 → 가져오기 → 임시 폴더 ch23-03-). 파일 chat.sqlite·other.sqlite는 임시 폴더에만. 파일 크기는 출력하지 않고
(WAL 때문에 연결이 열린 동안 본 파일 크기가 저장된 양과 맞지 않음), 파일 이름 목록은 sorted로 출력한다(새 커널 두 번 같음 확인).

## 결정 3 — 결정적 장면: 닫고 새로 만들어 이어 가기

첫 연결(check_same_thread=False)·첫 SqliteSaver·첫 그래프로 두 번 묻기(메시지 넷, 체크포인트 여섯, 단계 4)
→ first_conn.close()(닫은 연결·첫 그래프 모두 ProgrammingError) → 새 연결·새 SqliteSaver·새 그래프가 같은 파일의
conversation-a를 읽음(단계 4·메시지 넷) → 셋째 질문(메시지 여섯, 3번째, 체크포인트 아홉·단계 7).
값 바꿔 보기 둘: 스레드 이름만(conversation-b → 1번째) · 파일 이름만(other.sqlite → {}). 끝에 with SqliteSaver.from_conn_string
(설치판 sqlite/__init__.py 113~120행 contextlib.closing)으로 블록이 끝나면 닫히는 것을 오류로 확인. durability는 쓰지 않는다(04절 몫).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·
튜플 풀기·세미콜론·`isinstance`·별표 풀기·`is`·데코레이터·클래스(상태 형식 말고)·`except Exception`·`durability`·모델.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nbkit import RUN_DATE, code, install_source, md, setup, write_notebook  # noqa: E402
import author_01  # noqa: E402
from author_01 import html_text, table_html  # noqa: E402

LAB = ROOT / "labs/part6/ch23-persistence/notebooks"
FIGS = ROOT / "textbook/part6/ch23-persistence/figures"
SLUG = "03-스레드-재개와-대화-이어가기"
TITLE_TEXT = "스레드 재개와 대화 이어가기"
SRC = ROOT / "textbook/part6/ch23-persistence/_src" / (SLUG + ".html")
# 교재 출력을 만든 실행의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답)에서 읽은 값
RUNSEC = os.environ.get("AUTHOR03_RUNSEC", "5초 안에")
RUNS_SENTENCE = os.environ.get("AUTHOR03_RUNS_SENTENCE", "새 커널로 두 번 실행했을 때 코드 셀 29개의 출력이 모두 같았습니다.")

INSTALL = install_source(["langgraph==1.2.11", "langgraph-checkpoint-sqlite==3.0.3", "langchain-core==1.6.2"])

IMPORTS = r'''# SQLite 모듈(Ch 4 03절)·그래프 이름(Ch 13 01절)·메시지 이름(Ch 13 04절)에, SQLite 체크포인터를 더해 가져옵니다
import sqlite3
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
# 체크포인트를 SQLite 파일의 표에 쓰는 체크포인터입니다
from langgraph.checkpoint.sqlite import SqliteSaver

print("이 절에서 새로 가져온 이름:", "SqliteSaver")
# sqlite_version에는 Python에 들어 있는 SQLite의 판 번호 글이 들어 있습니다
print("SQLite 판:", sqlite3.sqlite_version)'''

# 01절 임시 폴더 셀에서 앞머리만 바꾼 셀(아래 assert)
FOLDER = author_01.FOLDER.replace("ch23-01-", "ch23-03-")

STATE = r'''# 메시지 칸 하나에 메시지 리듀서를 적은 상태 형식을 만듭니다(Ch 13 04절 모양)
class ConversationState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]'''

NODE = r'''# 메시지 칸에서 사람 메시지 수를 세어, 몇 번째 질문인지 적은 AI 메시지 하나를 냅니다
def reply(state):
    question_count = 0
    for message in state["messages"]:
        if type(message).__name__ == "HumanMessage":
            question_count = question_count + 1
    # 모델을 부르지 않고, 센 수로 코드가 답 글을 만듭니다
    answer_text = str(question_count) + "번째 질문을 받았습니다"
    return {"messages": [AIMessage(content=answer_text)]}'''

HAND = r'''# 노드 함수도 보통 함수입니다. 사람 메시지 하나를 담은 상태를 손으로 만들어 직접 불러 봅니다
hand_state = {"messages": [HumanMessage(content="대출 기간은 며칠인가요?")]}
hand_update = reply(hand_state)
hand_message = hand_update["messages"][0]
print("낸 메시지의 종류:", type(hand_message).__name__)
print("낸 메시지의 글:", hand_message.text)'''

DEF_PRINT = r'''# 메시지 목록을 받아, 라벨 줄 아래에 메시지마다 종류와 글을 한 줄씩 출력합니다(내놓는 값 없음)
def print_conversation(messages):
    print("메시지 종류 | 글")
    for message in messages:
        print(type(message).__name__, "|", message.text)'''

BUILDER = r'''# 노드 하나와 엣지 둘을 설계 객체에 적습니다(컴파일은 3절에서 체크포인터를 만든 뒤에 합니다)
builder = StateGraph(ConversationState)
builder.add_node("reply", reply)
builder.add_edge(START, "reply")
builder.add_edge("reply", END)
print("등록한 노드:", list(builder.nodes))'''

DEF_TABLES = r'''# SQLite 연결 하나로 파일 안의 표 이름을 이름 차례로 읽어, 목록으로 내놓습니다
def sqlite_tables(connection):
    sql = "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    cursor = connection.execute(sql)
    names = []
    # 줄마다 첫 칸이 표 이름입니다
    for row in cursor.fetchall():
        names.append(row[0])
    return names'''

CONNECT = r'''# 작업 폴더의 파일 chat.sqlite에 첫 연결을 엽니다(파일이 없으면 새로 만듦 — Ch 4 03절)
first_conn = sqlite3.connect("chat.sqlite", check_same_thread=False)
# 목록을 이름 차례로 보려고 sorted로 정렬합니다
file_names = sorted(os.listdir())
print("현재 작업 폴더의 파일:", file_names)'''

FIRST_GRAPH = r'''# 첫 연결을 넘겨 SQLite 체크포인터를 만들고, 2절의 설계 객체를 이 체크포인터와 함께 컴파일합니다
first_saver = SqliteSaver(first_conn)
first_graph = builder.compile(checkpointer=first_saver)
print("붙은 체크포인터의 종류:", type(first_graph.checkpointer).__name__)
print("chat.sqlite 안의 표:", sqlite_tables(first_conn))'''

TURN1 = r'''# 스레드 conversation-a로, 첫 질문을 사람 메시지 하나에 담아 실행합니다
config_a = {"configurable": {"thread_id": "conversation-a"}}
question_1 = HumanMessage(content="대출 기간은 며칠인가요?")
first_turn = first_graph.invoke({"messages": [question_1]}, config_a)
print_conversation(first_turn["messages"])'''

TABLES_AFTER = r'''# 첫 실행 뒤, 파일 chat.sqlite 안에 표가 생겼는지 다시 봅니다
print("chat.sqlite 안의 표:", sqlite_tables(first_conn))'''

TURN2 = r'''# 같은 스레드로, 둘째 질문 하나만 넣어 실행합니다
question_2 = HumanMessage(content="연장은 몇 번 할 수 있나요?")
second_turn = first_graph.invoke({"messages": [question_2]}, config_a)
print_conversation(second_turn["messages"])'''

HISTORY_FIRST = r'''# 첫 그래프로 스레드 conversation-a의 체크포인트 수와 마지막 단계 번호를 봅니다
history_first = list(first_graph.get_state_history(config_a))
print("체크포인트 수:", len(history_first))
# 목록은 최신 것부터라, 맨 앞이 마지막 체크포인트입니다(01절)
print("마지막 체크포인트의 단계 번호:", history_first[0].metadata["step"])'''

FILES_OPEN = r'''# 연결이 열린 채로, 작업 폴더의 파일을 이름 차례로 봅니다
file_names = sorted(os.listdir())
print("현재 작업 폴더의 파일:", file_names)'''

CLOSE = r'''# 첫 연결을 닫고, 닫은 연결로 문장 하나를 보내 봅니다(이 셀만 올라온 오류를 받아 출력합니다)
first_conn.close()
try:
    first_conn.execute("SELECT 1")
except sqlite3.ProgrammingError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:", error)'''

OLD_GRAPH = r'''# 닫은 연결을 쓰던 첫 그래프로 스레드 conversation-a를 읽어 봅니다(이 셀만 올라온 오류를 받아 출력합니다)
try:
    first_graph.get_state(config_a)
except sqlite3.ProgrammingError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:", error)'''

FILES_CLOSED = r'''# 첫 연결을 닫은 뒤, 작업 폴더의 파일을 다시 봅니다
file_names = sorted(os.listdir())
print("현재 작업 폴더의 파일:", file_names)'''

NEW_OBJECTS = r'''# 같은 파일에 새 연결을 열고, 새 체크포인터와 새 그래프를 만듭니다(설계 객체는 2절 것 그대로)
second_conn = sqlite3.connect("chat.sqlite", check_same_thread=False)
second_saver = SqliteSaver(second_conn)
second_graph = builder.compile(checkpointer=second_saver)
print("붙은 체크포인터의 종류:", type(second_graph.checkpointer).__name__)'''

READ_SAVED = r'''# 새 입력을 넣기 전에, 새 그래프로 스레드 conversation-a의 마지막 체크포인트를 읽습니다
saved_a = second_graph.get_state(config_a)
print("단계 번호:", saved_a.metadata["step"])
print("다음에 실행할 노드:", saved_a.next)
print_conversation(saved_a.values["messages"])'''

TURN3 = r'''# 새 그래프로 같은 스레드에, 셋째 질문 하나만 넣어 실행합니다
question_3 = HumanMessage(content="반납은 어디서 하나요?")
third_turn = second_graph.invoke({"messages": [question_3]}, config_a)
print_conversation(third_turn["messages"])
# 저장된 메시지 넷 뒤에 둘이 붙고, 답 글은 코드가 센 수라 실행마다 같아야 합니다
assert len(third_turn["messages"]) == 6, "메시지는 여섯이어야 합니다"
assert third_turn["messages"][-1].text == "3번째 질문을 받았습니다"'''

HISTORY_SECOND = r'''# 새 그래프로 체크포인트 수와 마지막 단계 번호를 다시 봅니다
history_second = list(second_graph.get_state_history(config_a))
print("체크포인트 수:", len(history_second))
print("마지막 체크포인트의 단계 번호:", history_second[0].metadata["step"])'''

THREAD_B = r'''# 값 바꿔 보기: 스레드 이름만 conversation-b로 바꾸고, 셋째 질문과 같은 글을 넣습니다
config_b = {"configurable": {"thread_id": "conversation-b"}}
question_b = HumanMessage(content="반납은 어디서 하나요?")
other_turn = second_graph.invoke({"messages": [question_b]}, config_b)
print_conversation(other_turn["messages"])'''

ROWS = r'''# 표 checkpoints에서 스레드마다 줄 수를 셉니다(스레드 이름은 자리표시자 ?로 넘김 — Ch 4 03절)
sql = "SELECT count(*) FROM checkpoints WHERE thread_id = ?"
print("스레드 | 표 checkpoints의 줄 수")
for thread_name in ["conversation-a", "conversation-b"]:
    cursor = second_conn.execute(sql, [thread_name])
    print(thread_name, "|", cursor.fetchone()[0])'''

OTHER_FILE = r'''# 값 바꿔 보기: 파일 이름만 other.sqlite로 바꿔 새 그래프를 만들고, 스레드 conversation-a를 읽습니다
other_conn = sqlite3.connect("other.sqlite", check_same_thread=False)
other_saver = SqliteSaver(other_conn)
other_graph = builder.compile(checkpointer=other_saver)
other_state = other_graph.get_state(config_a)
print("저장된 칸 값:", other_state.values)
print("다음에 실행할 노드:", other_state.next)
# 이 파일은 더 쓰지 않으므로 연결을 바로 닫습니다
other_conn.close()'''

WITH_BLOCK = r'''# with 블록 안에서만 열리는 연결로 체크포인터를 만들어, 스레드 conversation-a를 읽습니다
with SqliteSaver.from_conn_string("chat.sqlite") as block_saver:
    block_graph = builder.compile(checkpointer=block_saver)
    block_state = block_graph.get_state(config_a)
    print("블록 안에서 읽은 메시지 수:", len(block_state.values["messages"]))'''

AFTER_BLOCK = r'''# 블록이 끝난 뒤, 같은 그래프로 다시 읽어 봅니다(이 셀만 올라온 오류를 받아 출력합니다)
try:
    block_graph.get_state(config_a)
except sqlite3.ProgrammingError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:", error)'''

FILES_END = r'''# 남은 연결 second_conn도 닫고, 작업 폴더에 남은 파일을 봅니다
second_conn.close()
file_names = sorted(os.listdir())
print("현재 작업 폴더의 파일:", file_names)'''

FIG1 = "03-1-닫아도-파일에-남는-대화"
FIG1_ALT = os.environ.get("AUTHOR03_FIG1_ALT", "위에서 아래로 읽는 흐름도입니다. 맨 위 칸 첫 객체 5절에서 연결을 닫음 안에는 초록 상자 첫 연결 first_conn 아래 회색 상자 첫 체크포인터와 첫 그래프 질문 둘을 넣음이 있습니다. 이 칸에서 체크포인트를 씀이라고 적힌 화살표가 초록 상자 파일 chat.sqlite 스레드 conversation-a 체크포인트 여섯 메시지 넷으로 갑니다. 파일에서 마지막 체크포인트를 읽음이라고 적힌 화살표가 칸 새 객체 6절에서 새로 만듦으로 갑니다. 그 칸 안에는 초록 상자 새 연결 second_conn 아래 회색 상자 새 체크포인터와 새 그래프 셋째 질문을 넣음이 있습니다. 맨 아래 노란 상자에는 메시지 여섯 3번째 질문을 받았습니다 체크포인트 아홉이 적힌 그림")
FIG1_CAP = "첫 연결을 닫아도 대화는 파일 chat.sqlite에 남아, 새 연결로 만든 새 그래프가 셋째 질문을 이어 받았습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 연결과 파일이고, 회색 상자는 라이브러리의 체크포인터와 그래프입니다.
위 칸의 객체는 노트북 5절에서 닫혀 더 쓸 수 없고, 아래 칸의 객체는 6절에서 새로 만들었습니다.
두 칸을 잇는 것은 파일 하나뿐이고, 맨 아래 노란 상자는 6절 출력입니다."""

FIG2 = "03-2-질문마다-쌓인-메시지"
FIG2_ALT = os.environ.get("AUTHOR03_FIG2_ALT", "위에서 아래로 상자 다섯이 한 줄로 이어진 흐름도입니다. 첫 노란 상자는 첫 질문 뒤 메시지 둘 HumanMessage 대출 기간은 며칠인가요 AIMessage 1번째 질문을 받았습니다입니다. 둘째 노란 상자는 둘째 질문 뒤 메시지 넷 앞 두 메시지 그대로 AIMessage 2번째 질문을 받았습니다입니다. 셋째 파란 상자는 first_conn.close 첫 연결을 닫음 새 연결과 새 그래프를 만듦입니다. 넷째 노란 상자는 새 그래프가 읽은 마지막 체크포인트 단계 번호 4 메시지 넷입니다. 다섯째 노란 상자는 셋째 질문 뒤 메시지 여섯 AIMessage 3번째 질문을 받았습니다인 그림")
FIG2_CAP = "메시지는 질문마다 둘씩 쌓여 둘·넷·여섯이 되었고, 연결을 닫고 새로 연 뒤에도 넷에서 이어졌습니다."
FIG2_READ = """위에서 아래로 한 줄로 읽습니다.
노란 상자는 노트북 4·6절에서 출력으로 확인한 메시지 칸이고, 파란 상자는 5·6절에서 우리가 한 일입니다.
파란 상자 앞뒤로 메시지 수가 넷 그대로이고, 단계 번호도 4에서 이어집니다.
답 글의 번호는 노드가 사람 메시지를 센 수라 1·2·3으로 늘었습니다."""

FIG3 = "03-3-스레드-이름과-파일-이름-바꿔-보기"
FIG3_ALT = os.environ.get("AUTHOR03_FIG3_ALT", "칸 셋이 나란히 놓이고 아래에 회색 상자 하나가 있는 그림입니다. 왼쪽 칸 같은 파일 같은 스레드에는 초록 상자 chat.sqlite conversation-a 셋째 질문 아래 노란 상자 메시지 여섯 3번째 질문을 받았습니다 표의 줄 아홉이 있습니다. 가운데 칸 같은 파일 다른 스레드에는 초록 상자 chat.sqlite conversation-b 같은 글의 질문 아래 노란 상자 메시지 둘 1번째 질문을 받았습니다 표의 줄 셋이 있습니다. 오른쪽 칸 다른 파일 같은 스레드에는 초록 상자 other.sqlite conversation-a 입력 없이 읽기만 아래 노란 상자 저장된 칸 값 빈 딕셔너리 다음 노드 없음이 있습니다. 아래 회색 상자에는 세 칸 모두 같은 설계 객체 builder 같은 노드 reply가 적힌 그림")
FIG3_CAP = "같은 파일의 같은 스레드만 앞 대화를 이어 3번째 질문이 되었고, 스레드 이름이나 파일 이름이 다르면 앞 대화가 없었습니다."
FIG3_READ = """칸 셋의 제목은 파일과 스레드가 왼쪽 칸과 같은지 다른지이고, 칸 안은 위에서 아래로 읽습니다.
초록 상자는 연 파일·스레드 이름과 넣은 입력이고, 노란 상자는 노트북 6·7·8절 출력입니다.
왼쪽과 가운데 칸은 스레드 이름만, 왼쪽과 오른쪽 칸은 파일 이름만 다릅니다.
맨 아래 회색 상자는 세 칸에 모두 해당하는 사실입니다."""

FIG4 = "03-4-연결을-닫는-두-모양"
FIG4_ALT = os.environ.get("AUTHOR03_FIG4_ALT", "칸 둘이 나란히 놓이고 아래에 회색 상자 하나가 있는 그림입니다. 왼쪽 칸 5절 메서드 close에는 파란 상자 first_conn.close 아래 노란 상자 첫 그래프로 읽기 받은 오류 ProgrammingError가 있습니다. 오른쪽 칸 9절 with 블록에는 노란 상자 블록 안에서 읽은 메시지 여섯 아래 노란 상자 블록이 끝난 뒤 읽기 받은 오류 ProgrammingError가 있습니다. 아래 회색 상자에는 두 모양 모두 파일 chat.sqlite는 남음 연결을 모두 닫은 뒤 옆 파일 없음이 적힌 그림")
FIG4_CAP = "메서드 close로 닫든 with 블록이 끝나 닫히든, 닫힌 연결을 쓰던 그래프는 ProgrammingError를 받았고 파일은 남았습니다."
FIG4_READ = """칸 둘이 연결을 닫는 두 모양이고, 칸 안은 위에서 아래로 읽습니다.
파란 상자는 우리가 부른 메서드이고, 노란 상자는 노트북 5·9절 출력입니다.
왼쪽은 메서드를 직접 불러 닫았고, 오른쪽은 블록이 끝나며 저절로 닫혔습니다.
맨 아래 회색 상자는 두 칸에 모두 해당하는 사실이고, 5절과 9절의 파일 목록에서 확인했습니다."""

ILLU = "03-5-마지막-사진을-보고-다시-놓은-체스판"
ILLU_ALT = os.environ.get("AUTHOR03_ILLU_ALT", "흰 바탕에 나무 탁자 하나를 조금 위에서 본 그림입니다. 탁자 가운데 체스판 위에 검은 말 둘과 흰 말 둘, 모두 네 개가 서 있습니다. 체스판 바로 앞에는 흰 테두리 즉석사진 한 장이 놓여 있고, 사진 속에도 말 네 개가 같은 모양으로 선 작은 체스판이 있습니다. 체스판 왼쪽에는 속이 빈 채 열린 나무 상자 하나, 오른쪽에는 닫힌 파란 사진첩 하나가 있습니다. 카메라와 다른 사진은 없는 그림")
ILLU_CAP = os.environ.get("AUTHOR03_ILLU_CAP", "상자에 넣어 두었던 말 네 개를, 사진첩에서 꺼낸 마지막 사진 한 장을 보고 판 위에 다시 놓았습니다.")
ILLU_READ = os.environ.get("AUTHOR03_ILLU_READ", "나무 탁자 가운데 체스판 위에 말 네 개가 서 있고, 판 바로 앞에 즉석사진 한 장이 놓였습니다. 사진 속 작은 판에도 말 네 개가 같은 모양으로 서 있고, 왼쪽 나무 상자는 비었고 오른쪽 사진첩은 닫혀 있습니다. 닫힌 사진첩이 파일 <code>chat.sqlite</code>이고, 판 앞의 사진 한 장이 새 그래프가 읽은 마지막 체크포인트입니다. 말을 다시 놓은 판이, 새 그래프가 이어 가는 스레드 <code>conversation-a</code>입니다. 빈 상자는 말을 넣어 두었던 자리로 5절에서 닫은 첫 객체와 짝짓고, 말의 종류·색과 판의 칸 수는 무엇과도 짝짓지 않습니다.")

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 메시지 칸을 둔 그래프에 SQLite 체크포인터를 붙여, 한 스레드로 질문 두 개를 넣습니다.
2. 첫 연결을 닫아 첫 체크포인터와 첫 그래프를 못 쓰게 한 뒤, 모두 새로 만듭니다.
3. 새 그래프로 같은 스레드에 셋째 질문을 넣어, 앞 대화가 이어지는지 확인합니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
01절처럼 매번 같은 값을 내는 우리 노드로, 저장된 값이 맞는지 출력으로 가릅니다.
답 메시지의 글도 모델이 쓴 글이 아니라, 노드 함수가 질문 수를 세어 만든 글입니다.

노트북은 빈 임시 폴더를 만들어 그 폴더에서 실행합니다.
체크포인트를 담는 SQLite 파일은 이 임시 폴더에 생기고, 실습 폴더에는 파일을 남기지 않습니다.
읽어 오는 자료 파일은 없습니다.
교재 출력을 만든 실행에서는 노트북 전체가 """ + RUNSEC + """ 끝났습니다.
설치 셀에 걸리는 시간은 네트워크에 따라 달라집니다.

**기준 버전** — 첫 셀에서 패키지 셋을 설치합니다.
그래프는 langgraph 1.2.11입니다.
SQLite 체크포인터는 langgraph-checkpoint-sqlite 3.0.3에 들어 있습니다.
메시지 클래스가 든 langchain-core의 판은 1.6.2입니다.

교재 출력은 Linux의 Python 3.12.13과, 그 Python에 들어 있는 SQLite 3.53.1로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~6절을 읽습니다.
첫 연결로 대화를 쌓고, 연결을 닫은 뒤 새 그래프로 이어 가는 자리입니다.
7~9절은 스레드 이름과 파일 이름을 바꿔 보고, 연결을 닫는 다른 모양을 보는 자리입니다.
이 부분은 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch23-persistence`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

01절의 체크포인터 `InMemorySaver`는 이 프로그램의 메모리에만 저장했습니다.
02절에서는 PostgreSQL 표에 저장했지만, 새 연결로 스레드를 이어 가 보지는 않았습니다.
이 절은 체크포인트를 SQLite 파일에 쓰고, 연결과 그래프 객체를 모두 새로 만들어 같은 대화를 이어 갑니다.
대화는 Ch 13 04절의 메시지 칸에 사람 메시지와 AI 메시지로 쌓습니다.

첫 셀은 패키지 셋을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langgraph: 1.2.11`·`langgraph-checkpoint-sqlite: 3.0.3`·`langchain-core: 1.6.2`가 보입니다.
세 판 모두 실습 폴더 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모듈 `sqlite3`는 Ch 4 03절에서 SQLite 파일을 다룰 때 쓴 모듈입니다.
메시지 클래스 셋은 Ch 13 04절과 같지만, 이 절은 클래스가 원래 들어 있는 langchain-core에서 가져옵니다.
메시지 리듀서 `add_messages`는 그 절처럼 langgraph에서 가져옵니다.
새로 가져오는 이름은 체크포인터 `SqliteSaver` 하나이고, 뜻은 3절에서 풉니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `이 절에서 새로 가져온 이름: SqliteSaver`와 `SQLite 판: 3.53.1`이 보입니다.
체크포인터 `SqliteSaver`는 첫 셀에서 설치한 langgraph-checkpoint-sqlite에 들어 있습니다.
SQLite 판 번호는 Python에 들어 있는 SQLite의 판이라, 컴퓨터에 따라 다르게 나올 수 있습니다.

다음 셀은 01절처럼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다.
이 절의 SQLite 파일은 모두 이 임시 폴더에 생깁니다."""),
        setup(FOLDER),
        md("""**결과 읽기** — 출력 줄 `임시 폴더 이름에 ch23-03-이 들어 있는가: True`로, 이 절의 폴더를 만들었습니다.
출력 줄 `현재 작업 폴더의 파일: []`로, 빈 폴더에서 시작합니다.

## 2. 메시지 칸과 노드

이 절의 그래프는 질문 하나를 받을 때마다 답 메시지 하나를 붙이는 작은 그래프입니다.
다음 셀은 상태 형식입니다.
칸은 Ch 13 04절의 메시지 칸 `messages` 하나이고, 메시지 리듀서 `add_messages`를 적습니다.
번호를 적지 않은 메시지는 리듀서가 새 번호를 붙여, 목록 뒤에 이어 붙입니다.
칸 구성이 Ch 13 04절과 달라, Ch 13 약속대로 상태 형식 이름을 새로 붙였습니다."""),
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
표시 `Annotated`로 칸 `messages`에 메시지 리듀서를 적었습니다.

다음 셀은 노드 함수입니다.
메시지 칸에서 사람 메시지가 몇 개인지 세어, 「N번째 질문을 받았습니다」라는 글을 만듭니다.
그 글을 AI 메시지 하나에 담아 냅니다.
이 글은 모델이 쓴 답이 아니라, 우리 코드가 센 수로 만든 글입니다."""),
        code(NODE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
메시지의 종류는 01절처럼 `type(message).__name__`으로 읽고, 그 이름이 `HumanMessage`일 때만 셉니다.
메시지 칸에 규칙을 적었으므로, 노드는 새 AI 메시지 하나만 냅니다.

다음 셀은 01절처럼 이 노드 함수를 그래프 없이 직접 불러 봅니다.
손으로 만든 상태에는 사람 메시지 하나만 있습니다."""),
        code(HAND),
        md("""**결과 읽기** — 출력 줄 `낸 메시지의 종류: AIMessage`와 `낸 메시지의 글: 1번째 질문을 받았습니다`입니다.
사람 메시지가 하나라서 1번째입니다.
같은 상태를 넣으면 늘 같은 글이 나오므로, 저장된 대화가 맞는지 출력으로 가를 수 있습니다.

다음 셀은 메시지 목록을 한 줄씩 출력하는 함수입니다.
Ch 22 09절에서는 `message.type`으로 종류를 찍었고, 이 절은 01절처럼 클래스 이름으로 종류를 찍고 글을 적습니다.
메시지 번호는 리듀서가 실행마다 새로 붙여 달라지므로 출력하지 않습니다."""),
        code(DEF_PRINT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `print_conversation`은 인자로 받은 목록만 읽고, 노트북의 다른 이름에 기대지 않습니다.

다음 셀은 노드 하나와 엣지 둘을 설계 객체에 적습니다.
01절과 달리 여기서는 컴파일하지 않고, 3절에서 체크포인터를 만든 뒤 컴파일합니다."""),
        code(BUILDER),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['reply']`입니다.
설계 객체 `builder`는 이 절 끝까지 그대로 씁니다.
01절에서 본 것처럼 체크포인트는 그래프가 아니라 체크포인터 쪽에 있어, 설계 객체는 체크포인트를 담지 않습니다.

## 3. SQLite 파일에 체크포인터 붙이기

SQLite 체크포인터는 체크포인트를 SQLite 파일 하나의 표에 쓰는 체크포인터입니다.
02절의 비유를 이어 쓰면, 파일 하나가 사진첩 한 권이고 표가 속지입니다.
이 절에서는 클래스 `SqliteSaver`에 SQLite 연결 하나를 넘겨 만듭니다.

먼저 파일 안의 표 이름을 읽는 함수를 만듭니다.
SQLite 파일은 자기 안의 표 목록을 표 `sqlite_master`에 적어 둡니다.
Ch 4 03절의 `SELECT … WHERE … ORDER BY` 모양으로, 종류가 `table`인 줄의 이름만 읽습니다."""),
        code(DEF_TABLES),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `sqlite_tables`는 인자로 받은 연결로 문장을 보내고, 줄마다 첫 칸인 표 이름을 목록에 담습니다.

다음 셀은 파일 `chat.sqlite`에 첫 연결을 엽니다.
Ch 4 03절에서 본 것처럼, 함수 `connect`는 파일이 없으면 새로 만듭니다.

인자 `check_same_thread=False`는 연결을 연 실행 흐름 밖에서도 이 연결을 쓰게 합니다.
인자 이름의 thread는 이 챕터의 스레드(`thread_id`)가 아니라, 한 프로그램 안에서 따로 도는 일의 줄(실행 흐름)을 가리킵니다.
그래프가 체크포인트를 쓰는 일을 다른 실행 흐름에 맡기기 때문에 이 인자가 필요합니다.
설치판 소스의 예시도 이 인자를 주고, 체크포인터가 잠금으로 한 번에 하나씩만 쓴다고 적습니다."""),
        code(CONNECT),
        md("""**결과 읽기** — 출력 줄 `현재 작업 폴더의 파일: ['chat.sqlite']`로, 파일 하나가 생겼습니다.
아직 체크포인터를 만들지 않았습니다.

다음 셀은 이 연결을 넘겨 SQLite 체크포인터를 만들고, 설계 객체를 이 체크포인터와 함께 컴파일합니다.
마지막 줄은 파일 안에 표가 있는지 봅니다."""),
        code(FIRST_GRAPH),
        md("""**결과 읽기** — 출력 줄 `붙은 체크포인터의 종류: SqliteSaver`입니다.
출력 줄 `chat.sqlite 안의 표: []`로, 체크포인터를 만들어 붙여도 아직 표는 없습니다.

## 4. 첫 연결로 두 번 묻기

다음 셀은 스레드 `conversation-a`의 설정을 적고, 첫 질문을 사람 메시지 하나에 담아 실행합니다.
설정 딕셔너리는 01절과 같은 모양이고, 스레드 이름만 다릅니다.
실행 전에 예상해 봅니다.
메시지 칸에는 질문과 노드가 만든 답이 붙어, 메시지가 둘일 것입니다."""),
        code(TURN1),
        md("""**결과 읽기** — 라벨 줄 `메시지 종류 | 글` 아래 두 줄입니다.
첫 줄 `HumanMessage | 대출 기간은 며칠인가요?`는 우리가 넣은 질문입니다.
둘째 줄 `AIMessage | 1번째 질문을 받았습니다`는 노드가 붙인 답입니다.

다음 셀은 파일 안에 표가 생겼는지 다시 봅니다.
02절에서 SQLite 체크포인터는 필요할 때 표를 스스로 만든다고 적었는데, 그것을 출력으로 확인합니다."""),
        code(TABLES_AFTER),
        md("""**결과 읽기** — 출력 줄 `chat.sqlite 안의 표: ['checkpoints', 'writes']`입니다.
02절과 달리 표 만들기 `setup()`을 부르지 않았는데, 첫 실행에서 표 둘이 생겼습니다.
설치판 소스에서도 이 체크포인터는 파일을 처음 읽거나 쓸 때 메서드 `setup()`을 스스로 부릅니다.
표 `checkpoints`는 02절처럼 체크포인트를 한 줄씩 담는 표이고, 7절에서 줄을 셉니다.

다음 셀은 같은 스레드로 둘째 질문 하나만 넣어 실행합니다.
실행 전에 예상해 봅니다.
체크포인터가 저장된 메시지 둘을 꺼내 오면, 새 질문이 뒤에 붙어 2번째 질문이 될 것입니다."""),
        code(TURN2),
        md("""**결과 읽기** — 라벨 줄 아래 네 줄입니다.
마지막 줄 `AIMessage | 2번째 질문을 받았습니다`로, 노드가 앞 질문까지 세었습니다.
입력에는 둘째 질문 하나만 넣었지만, 메시지 칸에는 첫 실행의 두 메시지가 앞에 남아 있습니다.

01절 10절에서는 규칙 없는 합계 칸에 넣은 값이 저장된 값을 덮어썼습니다.
이번 메시지 칸은 리듀서를 적은 칸이라, 넣은 메시지가 저장된 목록 뒤에 붙었습니다.

다음 셀은 01절처럼 체크포인트 목록을 받아 수를 세고, 맨 앞 체크포인트의 단계 번호를 봅니다."""),
        code(HISTORY_FIRST),
        md("""**결과 읽기** — 출력 줄 `체크포인트 수: 6`과 `마지막 체크포인트의 단계 번호: 4`입니다.
01절처럼 노드 하나인 그래프라, 실행 한 번에 체크포인트가 셋씩 쌓였습니다.
이 여섯은 파일 `chat.sqlite`의 표 `checkpoints`에 있습니다.

다음 셀은 연결이 열린 채로 작업 폴더의 파일을 봅니다.
Ch 4에서처럼 `sorted`로 정렬해, 파일 이름을 차례대로 봅니다."""),
        code(FILES_OPEN),
        md("""**결과 읽기** — 출력 줄 `현재 작업 폴더의 파일: ['chat.sqlite', 'chat.sqlite-shm', 'chat.sqlite-wal']`입니다.
본 파일 옆에 이름 끝이 `-shm`과 `-wal`인 파일 둘이 더 생겼습니다.
이 둘은 연결이 열려 있는 동안 SQLite가 본 파일과 함께 쓰는 파일입니다.
설치판 소스에서 체크포인터는 표를 만들 때 이렇게 쓰는 방식을 켭니다.

## 5. 첫 연결 닫기

이제 첫 연결을 닫습니다.
Ch 4 03절처럼 메서드 `close`를 부르면, 그 연결로는 더 문장을 보낼 수 없습니다.
다음 셀은 연결을 닫은 뒤, 닫은 연결로 문장 하나를 보내 봅니다.
이 셀만 올라온 오류를 받아 출력하고, 셀은 끝까지 갑니다."""),
        code(CLOSE),
        md("""**결과 읽기** — 출력 줄 `받은 오류: ProgrammingError`입니다.
오류 글 `Cannot operate on a closed database.`는 닫힌 데이터베이스로는 일할 수 없다는 뜻입니다.
연결이 닫혔습니다.

첫 체크포인터와 첫 그래프는 이 연결을 쓰는 객체입니다.
다음 셀은 첫 그래프로 스레드 `conversation-a`를 읽어 봅니다.
실행 전에 예상해 봅니다.
체크포인터의 연결이 닫혔으니, 첫 그래프도 읽지 못할 것입니다."""),
        code(OLD_GRAPH),
        md("""**결과 읽기** — 출력 줄 `받은 오류: ProgrammingError`로, 첫 그래프도 같은 오류를 받았습니다.
첫 연결·첫 체크포인터·첫 그래프는 더 쓸 수 없습니다.
이 절은 객체를 만든 때부터 이렇게 더 쓸 수 없게 된 때까지를 객체의 수명이라고 부릅니다.

다음 셀은 첫 연결을 닫은 뒤, 작업 폴더의 파일을 다시 봅니다."""),
        code(FILES_CLOSED),
        md("""**결과 읽기** — 출력 줄 `현재 작업 폴더의 파일: ['chat.sqlite']`입니다.
연결을 닫자 옆 파일 둘이 없어지고, 본 파일 하나만 남았습니다.
SQLite 설명서는 마지막 연결을 닫을 때 옆 파일의 내용을 본 파일에 옮기고 옆 파일을 지운다고 적습니다.
본 파일에 남은 대화는 6절에서 새 연결로 읽습니다.

## 6. 새 연결과 새 그래프로 이어 가기

이제 같은 파일에 새 연결을 열고, 새 체크포인터와 새 그래프를 만듭니다.
프로그램을 다시 시작했다면, 이렇게 모두 새로 만들어야 합니다.
설계 객체 `builder`는 체크포인트를 담지 않으므로 2절 것을 그대로 씁니다.
객체를 새로 만든 뒤 같은 스레드 이름으로 대화를 이어 가는 일을, 이 절은 스레드 재개라고 부릅니다."""),
        code(NEW_OBJECTS),
        md("""**결과 읽기** — 출력 줄 `붙은 체크포인터의 종류: SqliteSaver`입니다.
연결·체크포인터·그래프가 모두 3절과 다른 새 객체입니다.
3절과 같은 것은 설계 객체와 파일 이름 `chat.sqlite`뿐입니다.

다음 셀은 새 입력을 넣기 전에, 새 그래프로 스레드 `conversation-a`의 마지막 체크포인트를 읽습니다.
실행 전에 예상해 봅니다.
01절에서 새 `InMemorySaver`는 같은 스레드를 읽지 못했습니다.
이번에는 체크포인트가 파일에 있으니, 새 그래프도 메시지 넷을 읽을 것입니다."""),
        code(READ_SAVED),
        md("""**결과 읽기** — 출력 줄 `단계 번호: 4`는 4절에서 본 마지막 체크포인트의 번호와 같습니다.
출력 줄 `다음에 실행할 노드: ()`로, 그 대화는 끝난 채로 저장되어 있습니다.
라벨 줄 아래 네 줄은 4절 둘째 실행 뒤의 메시지 칸과 같습니다.
새 연결로 연 파일에서, 첫 연결이 쓴 대화를 그대로 읽었습니다.

다음 셀은 새 그래프로 같은 스레드에 셋째 질문 하나만 넣어 실행합니다.
실행 전에 예상해 봅니다.
앞 질문 둘이 이어진다면, 노드가 3번째 질문이라고 쓸 것입니다.
셀 끝 `assert`는 코드가 정하는 메시지 수와 답 글에만 겁니다."""),
        code(TURN3),
        md("""**결과 읽기** — 라벨 줄 아래 여섯 줄입니다.
마지막 줄 `AIMessage | 3번째 질문을 받았습니다`로, 새 그래프가 앞 대화에 이어 셋째 질문을 받았습니다.
첫 연결과 첫 그래프는 닫혔지만, 파일의 체크포인트로 대화가 이어졌습니다.
메시지 칸에는 질문과 답이 함께 쌓여, 메시지가 둘·넷·여섯으로 늘었습니다.

다음 셀은 새 그래프로 체크포인트 수와 마지막 단계 번호를 다시 봅니다."""),
        code(HISTORY_SECOND),
        md("""**결과 읽기** — 출력 줄 `체크포인트 수: 9`와 `마지막 체크포인트의 단계 번호: 7`입니다.
4절의 여섯에 셋째 실행의 셋이 더해졌고, 단계 번호도 4 다음부터 이어졌습니다.
새 그래프가 쓴 체크포인트도 같은 파일의 같은 스레드에 쌓였습니다.

## 7. 값 바꿔 보기 · 스레드 이름만 바꾸기

바꿀 값은 설정 딕셔너리의 스레드 이름 하나입니다.
넣는 메시지는 6절 셋째 질문과 같은 글입니다.
실행 전에 예상해 봅니다.
스레드 `conversation-b`에는 저장된 메시지가 없어, 1번째 질문이 될 것입니다."""),
        code(THREAD_B),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄이고, 마지막 줄은 `AIMessage | 1번째 질문을 받았습니다`입니다.
같은 파일과 같은 그래프를 썼지만, 스레드 `conversation-a`의 대화는 섞이지 않았습니다.

다음 셀은 표 `checkpoints`에서 스레드마다 줄 수를 셉니다.
스레드 이름은 Ch 4 03절처럼 자리표시자 `?`로 넘깁니다.
문장은 6절의 새 연결 `second_conn`으로 보냅니다."""),
        code(ROWS),
        md("""**결과 읽기** — 라벨 줄 `스레드 | 표 checkpoints의 줄 수` 아래 두 줄입니다.
줄 `conversation-a | 9`는 6절에서 센 체크포인트 아홉과 같습니다.
줄 `conversation-b | 3`은 한 번 실행한 스레드의 체크포인트 셋입니다.
두 스레드의 줄은 파일 하나, 표 하나에 있고 칸 `thread_id`의 값으로 갈립니다.

## 8. 값 바꿔 보기 · 파일 이름만 바꾸기

이번에는 스레드 이름을 `conversation-a` 그대로 두고, 연결할 파일 이름만 `other.sqlite`로 바꿉니다.
실행 전에 예상해 봅니다.
새 파일에는 체크포인트가 없으니, 01절 11절의 새 체크포인터처럼 빈 딕셔너리를 읽을 것입니다.
이 파일은 더 쓰지 않으므로, 셀 끝에서 연결을 바로 닫습니다."""),
        code(OTHER_FILE),
        md("""**결과 읽기** — 출력 줄 `저장된 칸 값: {}`과 `다음에 실행할 노드: ()`입니다.
스레드 이름이 같아도, 파일이 다르면 저장된 대화를 읽지 못했습니다.
대화는 파일 `chat.sqlite` 안에만 있습니다.

## 9. with 블록으로 연결 닫기

설치판 소스의 설명 예시는 SQLite 체크포인터를 메서드 `from_conn_string`과 `with` 블록으로도 만듭니다.
`with` 블록은 Ch 2 05절에서 파일을, Ch 10 02절에서 라이브러리 객체를 열 때 썼습니다.
설치판 소스에서 이 모양은 블록을 시작할 때 연결을 열고, 블록이 끝나면 그 연결을 닫습니다.
인자 `check_same_thread=False`도 소스 안에서 함께 줍니다.
다음 셀은 이 모양으로 스레드 `conversation-a`를 읽습니다."""),
        code(WITH_BLOCK),
        md("""**결과 읽기** — 출력 줄 `블록 안에서 읽은 메시지 수: 6`으로, 블록 안의 새 체크포인터도 같은 대화를 읽었습니다.

다음 셀은 블록이 끝난 뒤, 같은 그래프로 다시 읽어 봅니다.
실행 전에 예상해 봅니다.
블록이 끝나며 연결이 닫혔다면, 5절처럼 오류를 받을 것입니다."""),
        code(AFTER_BLOCK),
        md("""**결과 읽기** — 출력 줄 `받은 오류: ProgrammingError`로, 블록이 끝나며 연결이 닫혔습니다.
메서드 `close`를 따로 부르지 않아도, 블록을 벗어나면 연결이 닫힙니다.

다음 셀은 남은 연결 `second_conn`도 닫고, 작업 폴더에 남은 파일을 봅니다."""),
        code(FILES_END),
        md("""**결과 읽기** — 출력 줄 `현재 작업 폴더의 파일: ['chat.sqlite', 'other.sqlite']`입니다.
연결을 모두 닫아, 옆 파일 없이 본 파일 둘만 남았습니다.
두 파일은 임시 폴더에 있어, 실습 폴더에는 남지 않습니다.

## 정리

1. 연결·체크포인터·그래프를 모두 새로 만들어도, 같은 파일의 같은 스레드에서 대화가 이어져 3번째 질문이 되었습니다.
2. 첫 연결을 닫자 첫 그래프는 `ProgrammingError`를 받았고, 체크포인트는 파일 `chat.sqlite`에 남았습니다.
3. 스레드 이름이 다르면 1번째 질문부터였고, 파일이 다르면 저장된 대화를 읽지 못했습니다.

04절에서는 저장하는 때를 바꿔 가며, 프로그램을 강제로 끝낸 뒤 무엇이 남는지 봅니다."""),
    ]


L_CH02_05 = "../../part1/ch02-python/05-파일과-예외.html"
L_CH04_03 = "../../part1/ch04-data-tools/03-SQL로-조회-함수-만들기.html"
L_CH10_02 = "../../part3/ch10-document-processing/02-PDF와-표-OCR.html"
L_CH13_04 = "../../part4/ch13-langgraph-basics/04-add_messages-리듀서.html"
L_CH21_04 = "../ch21-create-agent/04-0x에서-1x로-마이그레이션.html"
L_CH22_09 = "../ch22-middleware/09-Middleware-실습.html"
L_01 = "01-체크포인터와-스레드.html"
L_02 = "02-PostgresSaver-준비와-스키마.html"
L_04 = "04-내구-실행-모드-비교.html"

RESULT_ROWS = [
    ("<code>chat.sqlite</code>", "<code>conversation-a</code>", "질문 셋(셋째는 새 그래프로)", "6", "<code>AIMessage | 3번째 질문을 받았습니다</code>", "9"),
    ("<code>chat.sqlite</code>", "<code>conversation-b</code>", "셋째 질문과 같은 글 하나", "2", "<code>AIMessage | 1번째 질문을 받았습니다</code>", "3"),
    ("<code>other.sqlite</code>", "<code>conversation-a</code>", "없음(읽기만)", "없음(<code>{}</code>)", "—", "세지 않음"),
]

LOOK_B5 = "노트북 4절에서 둘째 질문 뒤 메시지가 넷이고, 마지막 줄이 <code>AIMessage | 2번째 질문을 받았습니다</code>인지 봅니다. 5절에서 닫은 연결과 첫 그래프가 모두 <code>ProgrammingError</code>를 받았는지 확인합니다. 6절에서 새 그래프가 <code>단계 번호: 4</code>를 읽고, 셋째 질문 뒤 <code>AIMessage | 3번째 질문을 받았습니다</code>가 되었는지 봅니다."


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
    result_table = table_html(["파일", "스레드", "넣은 것", "메시지 수", "마지막 메시지", "체크포인트(표의 줄)"], RESULT_ROWS)
    return """<!--meta: 강의 1h | 실습 1.5h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>연결과 그래프 객체를 모두 새로 만든 뒤에도, SQLite 파일에 저장된 대화를 이어 가는 것을 출력으로 확인할 수 있습니다.</li>
<li>메시지 칸에 쌓인 사람 메시지와 AI 메시지를 종류별로 출력해, 저장된 대화 기록을 읽을 수 있습니다.</li>
<li>연결을 닫은 뒤의 옛 객체, 다른 스레드 이름, 다른 파일에서 결과가 어떻게 달라지는지 설명할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>대화 프로그램은 사용자가 다음 질문을 보낼 때, 앞 질문을 받은 객체가 그대로 남아 있다고 기대할 수 없습니다. 프로그램을 다시 시작하면 메모리의 객체는 모두 사라집니다. 그래도 사용자는 앞 대화에 이어 답을 받기를 기대합니다.</p><p><a href=\"""" + L_01 + """\">01절</a>의 체크포인터는 메모리에만 저장해, 새 체크포인터로는 같은 스레드를 읽지 못했습니다. <a href=\"""" + L_02 + """\">02절</a>에서는 PostgreSQL 표에 저장했지만, 새 연결로 스레드를 이어 가 보지는 않았습니다. 이 절은 SQLite 파일에 대화를 저장하고, 연결·체크포인터·그래프를 모두 새로 만든 뒤 같은 대화를 이어 갑니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH04_03 + """\">Ch 4 03절</a>에서는 임시 폴더의 SQLite 파일에 연결을 열고, 문장을 보내 표를 읽은 뒤 연결을 닫았습니다. 값은 자리표시자 <code>?</code>로 넘겼습니다. <a href=\"""" + L_CH13_04 + """\">Ch 13 04절</a>에서는 메시지 칸에 메시지 리듀서 <code>add_messages</code>를 적고, 사람 메시지와 AI 메시지를 쌓았습니다.</p><p><a href=\"""" + L_CH22_09 + """\">Ch 22 09절</a>에서는 에이전트가 쌓은 대화 기록을 메시지 종류별로 출력했습니다. 이 절은 그런 대화 기록을 프로그램 밖 파일에 저장하고, 다시 이어 갑니다. <code>with</code> 블록은 <a href=\"""" + L_CH02_05 + """\">Ch 2 05절</a>에서 파일을, <a href=\"""" + L_CH10_02 + """\">Ch 10 02절</a>에서 라이브러리 객체(PDF 문서)를 열 때 썼습니다. <a href=\"""" + L_CH21_04 + """\">Ch 21 04절</a>에서는 경고 목록을 모을 때 썼습니다.</p><p><a href=\"""" + L_01 + """\">01절</a>에서는 체크포인터·체크포인트·스레드를 배우고, 메서드 <code>get_state</code>와 <code>get_state_history</code>로 저장된 것을 읽었습니다. <a href=\"""" + L_02 + """\">02절</a>에서는 체크포인트가 표 <code>checkpoints</code>에 한 줄씩 쌓이는 것을 셌습니다. 그때 SQLite 체크포인터는 표를 스스로 만든다고 소스로만 적었는데, 이 절에서 출력으로 확인합니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절의 체스판과 즉석사진을 다시 떠올립니다. 저녁에 판을 치우고 말을 상자에 넣었습니다. 한 수마다 찍은 사진은 사진첩에 꽂아 두었습니다. 다음 날 사진첩에서 마지막 사진을 꺼내 보고, 사진대로 말을 다시 놓으면 어제 판에 이어서 둘 수 있습니다.</p><p>판과 말을 치운 것이 연결·체크포인터·그래프 객체를 닫은 것이고, 사진첩이 SQLite 파일입니다. 마지막 사진을 보고 말을 다시 놓는 것이, 새 그래프가 마지막 체크포인트를 읽는 일입니다. 다른 사진첩을 펼치면 그 판의 사진은 없습니다.</p>
""" + illustration_block() + """<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>SQLite 체크포인터</td><td>체크포인트를 SQLite 파일 하나의 표에 쓰는 체크포인터입니다. 사진을 사진첩 한 권에 꽂아 두어, 판을 치워도 사진이 남는 것과 같습니다. 이 절에서는 <code>SqliteSaver(first_conn)</code>으로 만들었고, 파일 <code>chat.sqlite</code>에 표 둘이 생겼습니다.</td></tr><tr><td>객체의 수명</td><td>객체를 만든 때부터, 닫혀서 더 쓸 수 없게 된 때까지입니다. 판과 말은 저녁에 치우지만, 사진첩의 사진은 다음 날에도 남는 것과 같습니다. 이 절에서는 첫 연결을 닫자 첫 그래프가 오류를 받았고, 파일의 체크포인트는 남았습니다.</td></tr><tr><td>스레드 재개</td><td>객체를 새로 만든 뒤, 같은 스레드 이름으로 마지막 체크포인트부터 대화를 이어 가는 일입니다. 다음 날 마지막 사진을 보고 말을 다시 놓은 뒤, 이어서 두는 것과 같습니다. 이 절에서는 새 그래프가 메시지 넷을 읽고, 셋째 질문에 3번째라고 답했습니다. Ch 24에서 사람의 확인을 받아 멈춘 실행을 다시 움직이는 일과는 다른 장면입니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. SQLite 체크포인터는 노트북 3절의 <code>first_saver = SqliteSaver(first_conn)</code>입니다. 객체의 수명은 5절에서 연결을 닫은 뒤 첫 그래프가 받은 <code>ProgrammingError</code>로 보입니다. 스레드 재개는 6절의 <code>second_graph.invoke({"messages": [question_3]}, config_a)</code>입니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>닫아도 남는 것과 사라지는 것</h3><p>연결을 닫으면, 그 연결을 쓰던 체크포인터와 그래프는 더 쓸 수 없습니다. 그러나 파일에 이미 쓴 체크포인트는 남습니다. 같은 파일에 새 연결을 열어 새 체크포인터를 만들면, 새 그래프는 그 스레드의 마지막 체크포인트부터 시작합니다. 01절에서 새 <code>InMemorySaver</code>가 같은 스레드를 읽지 못한 것과 다른 점입니다.</p><p>새 입력은 01절에서 본 차례대로 칸에 들어갑니다. 메시지 칸은 리듀서를 적은 칸이라, 새 사람 메시지가 저장된 목록 뒤에 붙습니다. 그래서 노드가 앞 질문까지 세어 3번째라고 씁니다. 01절 10절의 합계 칸처럼 규칙 없는 칸이었다면, 넣은 값이 저장된 값을 덮어썼을 것입니다.</p>
<h3>다른 상황에 적용</h3><p>사용자가 다음 날 같은 상담을 이어 가려면, 프로그램은 그 대화의 스레드 이름과 같은 파일을 다시 씁니다. 새 대화는 새 스레드 이름으로 시작합니다. 이 절에서는 프로그램을 다시 시작해 보지는 않았고, 한 커널 안에서 객체를 모두 새로 만들었습니다. 새로 시작한 프로그램에서 이어 가는 모습은 <a href=\"""" + L_04 + """\">04절</a>에서 봅니다.</p>
<h3>비교와 경계</h3><p>SQLite 체크포인터의 표는 <code>checkpoints</code>와 <code>writes</code> 둘이었고, 02절 PostgreSQL 체크포인터의 표는 넷이었습니다. 이름도 <code>writes</code>와 <code>checkpoint_writes</code>처럼 다르고, 나머지 두 표에 해당하는 표는 SQLite 쪽에 없습니다. SQLite 체크포인터는 표 만들기를 스스로 불렀지만, PostgreSQL 체크포인터는 우리가 <code>setup()</code>을 불러야 했습니다.</p><p>설치판 소스의 설명은 SQLite 체크포인터를 가벼운 데모와 작은 프로젝트용이라고 적습니다. 공식 문서도 실험과 로컬 작업에 알맞다고 적습니다. 여러 프로그램이 한 파일을 함께 쓰는 모습은 이번에 실행하지 않았습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 메시지 칸 상태 형식과 노드를 적고, 첫 연결로 만든 SQLite 체크포인터로 질문 둘을 넣습니다. 첫 연결을 닫아 첫 그래프가 오류를 받는 것을 본 뒤, 연결·체크포인터·그래프를 모두 새로 만들어 셋째 질문을 넣습니다. 끝으로 스레드 이름과 파일 이름을 하나씩 바꿔 보고, <code>with</code> 블록으로 연결을 닫는 모양을 봅니다.</p><p>이 절은 모델을 부르지 않아 모델 요청은 0번이고, API 키 셀도 없습니다. 답 메시지의 글은 노드 함수가 사람 메시지 수를 세어 만든 글이고, 모델이 쓴 답이 아닙니다. 그래서 같은 입력에는 늘 같은 글이 나와, 대화가 이어졌는지 출력으로 가를 수 있습니다. SQLite 파일은 노트북이 만든 빈 임시 폴더에 생깁니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>값 바꿔 보기는 둘입니다. 노트북 7절은 스레드 이름만, 8절은 연결할 파일 이름만 바꿨습니다. 아래 표는 6~8절 출력을 파일과 스레드마다 한 줄로 옮긴 것입니다.</p>
""" + result_table + """
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>같은 파일의 같은 스레드만 앞 대화를 이어 갔습니다. 새 그래프는 첫 그래프와 다른 객체였지만, 파일에 남은 마지막 체크포인트에서 시작해 3번째 질문이 되었습니다. 스레드 이름만 바꾸면 같은 파일 안에서도 1번째 질문부터였습니다. 파일 이름만 바꾸면 스레드 이름이 같아도 빈 딕셔너리를 읽었습니다.</p><p>이어 가는 데 필요한 것은 그래프 객체가 아니라, 파일과 스레드 이름의 짝이었습니다. 01절의 체크포인트는 체크포인터 객체 안에 있어, 새 체크포인터로는 읽지 못했습니다. 이 절의 체크포인트는 체크포인터 객체보다 오래 남는 파일 안에 있었습니다. 그래서 체크포인터를 새로 만들어도, 같은 파일만 열면 이어 갈 수 있었습니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>연결을 닫는 모양은 둘을 보았습니다. 5절은 메서드 <code>close</code>를 직접 불렀고, 9절은 <code>with</code> 블록이 끝나며 닫혔습니다. 두 경우 모두 닫힌 연결을 쓰던 그래프는 <code>ProgrammingError</code>를 받았습니다. 연결이 열린 동안에는 본 파일 옆에 파일 둘이 더 있었고, 연결을 모두 닫자 없어졌습니다.</p><p>모델을 부르지 않아, 노트북 출력은 새 커널로 두 번 실행해도 글자까지 같아야 합니다. """ + RUNS_SENTENCE + """ 두 실행 모두 빈 임시 폴더에서 시작했습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>답 메시지의 글은 노드 함수가 만든 글이고, 모델이 쓴 답이 아닙니다. 모델 답이나 도구 메시지가 든 대화를 저장해 보지는 않았습니다.</li><li>인자 <code>check_same_thread=False</code>를 빼고 같은 모양의 작은 그래프를 실행하면, 그래프 실행 중에 <code>ProgrammingError</code>가 났습니다. 이 장면은 노트북 밖에서 다섯 번 확인했고, 노트북에서는 실행하지 않았습니다.</li><li>설치판 소스 <code>langgraph/pregel/_loop.py</code> 1199~1202행에서 그래프는 체크포인트 저장을 다른 실행 흐름에 맡깁니다. 실행 흐름은 한 프로그램 안에서 따로 도는 일의 줄입니다. 인자 이름 <code>check_same_thread</code>의 thread도 이 실행 흐름을 가리키고, 이 챕터의 스레드(<code>thread_id</code>)와는 다른 말입니다. 실행이 끝날 때는 맡긴 저장이 모두 끝나기를 기다립니다(<code>langgraph/pregel/_executor.py</code> 105~107행).</li><li><code>with sqlite3.connect(…) as 이름:</code> 모양은 블록이 끝나도 연결을 닫지 않는다고 Python 설명서가 적습니다. 노트북 밖에서도 블록 뒤에 문장이 실행되는 것을 확인했습니다. 연결을 닫으려면 5절처럼 <code>close</code>를 부르거나, 9절 모양을 씁니다.</li><li>연결이 열려 있는 동안에는 바뀐 내용이 옆 파일(<code>-wal</code>)에 먼저 쌓인다고 SQLite 설명서가 적습니다. 그래서 본 파일의 크기로 저장된 양을 가늠하지 않았고, 파일 크기는 출력하지 않았습니다.</li><li>프로그램(커널)을 다시 시작해 이어 가 보지는 않았습니다. 한 커널 안에서 연결·체크포인터·그래프를 모두 새로 만들었습니다.</li><li>메시지 번호와 체크포인트 ID는 실행마다 새로 붙어 출력하지 않았습니다. 메시지 번호는 메시지 리듀서가 붙입니다(<code>langgraph/graph/message.py</code> 202~208행).</li><li>대화가 길어지면 메시지 칸과 파일도 계속 커집니다. 오래된 메시지를 줄이는 일은 이 절에서 하지 않았습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13과 SQLite 3.53.1로 만들었습니다. 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>연결·체크포인터·그래프를 모두 새로 만들어도, 같은 파일의 같은 스레드에서 대화가 이어져 3번째 질문이 되었습니다.</li><li>첫 연결을 닫자 첫 그래프는 <code>ProgrammingError</code>를 받았고, 체크포인트는 파일 <code>chat.sqlite</code>에 남았습니다.</li><li>스레드 이름이 다르면 1번째 질문부터였고, 파일이 다르면 저장된 대화를 읽지 못했습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_04 + """\">04절</a>에서는 저장하는 때를 바꿔 가며, 프로그램을 강제로 끝낸 뒤 무엇이 남는지 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 첫 연결을 닫은 뒤 첫 그래프로 스레드 <code>conversation-a</code>를 읽자 어떻게 되었나요?</p><p class="quiz-a">오류 <code>ProgrammingError</code>를 받았습니다. 첫 그래프의 체크포인터가 쓰던 연결이 닫혀, 더 쓸 수 없었기 때문입니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">2. 새 그래프에 셋째 질문 하나만 넣었는데, 답이 「3번째 질문을 받았습니다」가 된 까닭은 무엇인가요?</p><p class="quiz-a">새 그래프가 파일에 남은 마지막 체크포인트의 메시지 넷에서 시작했기 때문입니다. 메시지 리듀서가 새 질문을 그 뒤에 붙여, 노드가 사람 메시지 셋을 셌습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">3. 파일 이름만 <code>other.sqlite</code>로 바꾸자 같은 스레드 이름으로도 대화를 읽지 못한 까닭은 무엇인가요?</p><p class="quiz-a">대화의 체크포인트는 파일 <code>chat.sqlite</code>의 표에 있고, 새 파일에는 없기 때문입니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p><p class="quiz-q">4. <code>with</code> 블록으로 만든 체크포인터를 붙인 그래프가, 블록이 끝난 뒤 오류를 받은 까닭은 무엇인가요?</p><p class="quiz-a">메서드 <code>from_conn_string</code>이 블록이 끝날 때 연결을 닫기 때문입니다. 설치판 소스로 이 동작을 확인했고, 노트북에서는 오류로 보았습니다. 틀렸다면 노트북 9절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langgraph/checkpointers">LangGraph Checkpointers</a></div>확인 2026-09-25 · SQLite 체크포인터를 실험과 로컬 작업에 알맞다고 적고, 설치할 패키지 이름을 적습니다.</li><li><div><a href="https://www.sqlite.org/wal.html">SQLite Write-Ahead Logging</a></div>확인 2026-09-25 · 바뀐 내용을 옆 파일에 먼저 적고, 마지막 연결을 닫을 때 옆 파일 둘을 지운다고 적습니다.</li><li><div><a href="https://docs.python.org/3.12/library/sqlite3.html">Python 3.12 sqlite3</a></div>확인 2026-09-25 · 인자 <code>check_same_thread</code>의 뜻과, 연결의 <code>with</code> 블록이 연결을 닫지 않는다는 점을 적습니다.</li><li>langgraph-checkpoint-sqlite 3.0.3 소스 <code>langgraph/checkpoint/sqlite/__init__.py</code> 37~70행 — 클래스 설명과 예시입니다.</li><li>같은 파일 92~120행은 <code>from_conn_string</code>이고, 블록이 끝나면 연결을 닫습니다.</li><li>같은 파일 122~159행은 표 둘을 만드는 <code>setup()</code>이고, 175행에서 체크포인터가 스스로 부릅니다.</li><li>langgraph 1.2.11 소스 <code>langgraph/graph/message.py</code> 202~208행 — 메시지에 번호를 붙이는 자리입니다.</li><li>langchain 1.4.0 소스 <code>langchain/messages/__init__.py</code> 7행 — 메시지 클래스를 langchain-core에서 가져와 그대로 내놓습니다.</li><li>Ch 4 03절에서 SQLite 조회를, Ch 13 04절에서 메시지 칸을, 01·02절에서 체크포인터와 표를 보았습니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    # 임시 폴더 셀은 01절 셀에서 앞머리 ch23-01- → ch23-03- 만 다르다(세 곳)
    assert FOLDER != author_01.FOLDER and FOLDER.replace("ch23-03-", "ch23-01-") == author_01.FOLDER
    assert author_01.FOLDER.count("ch23-01-") == 3
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "03", SLUG, "experiment", cells())
        print("wrote", path)
