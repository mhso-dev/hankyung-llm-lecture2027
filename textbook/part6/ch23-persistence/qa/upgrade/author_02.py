"""Ch 23 02절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 author_02.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_02.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
이후 run_section.sh 가 pre_exec.sh(PostgreSQL 켜기) → 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **paired 형식 유지**(chapter.json). 슬러그 그대로.

## 결정 1 — 실제 PostgreSQL (챕터 리드 결정 3, 선택지 A)

노트북은 Ch 12 02절과 같은 접속 글(127.0.0.1:55432 · student · rag_lab)로 붙고, 이름 공간(SQL SCHEMA) ch23_lab만
지우고 새로 만든다. 학생은 Ch 12 02절 Docker 컨테이너 hankyung-part3-pgvector를 다시 켠다(포트 충돌 없음).
작업 기기는 Docker가 없어 qa/upgrade/pre_exec.sh 가 Ch 12의 conda-forge PostgreSQL 17.11 바이너리로 이 챕터 전용 새
클러스터(/tmp/ch23-02/pgdata)를 같은 접속 글로 켜고, 부른 셸이 끝날 때 끈다(Ch 12 데이터 폴더는 건드리지 않음).

## 결정 2 — paired Before = 실제 결함

같은 그래프·같은 체크포인터·같은 입력에서 setup() 한 줄만 다르다. Before는 표가 없어 UndefinedTable(42P01)을
`except psycopg.Error as error`(Ch 12 02 모양)로 받아 출력하고, 표가 여전히 없음을 본다. After는 setup() → 표 넷 ·
표 만들기 기록 열 줄 → 01절과 같은 합계 3 → 7 → 체크포인트 여섯 = 표 checkpoints 여섯 줄 → 값 바꿔 보기 둘
(setup() 한 번 더 · 스레드 customer-b) → 체크포인터 연결을 닫은 뒤에도 줄 수 그대로 → 작업 폴더 [] .

## 결정 3 — 연결은 Ch 12 02처럼 connect → close (with 없음)

PostgresSaver(saver_conn)에 넘길 연결은 autocommit=True·row_factory=dict_row(설치판 패키지 설명), 이름 공간은
`SET search_path TO ch23_lab`. 우리 SQL은 2절 연결 conn(튜플 줄)로. from_conn_string·with 는 b7 한 줄(실행 안 함).

## 01절과 같은 셀 (아래 assert)

설치 셀 모양·임시 폴더 셀 모양(앞머리만 ch23-02-), 상태 형식 STATE·노드 NODE·CONFIG_A·CONFIG_B·FILES 는 01절 셀과 글자까지 같다.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`sorted`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·
튜플 풀기·세미콜론·`isinstance`·별표 풀기·`with`·`is`·데코레이터·클래스(상태 형식 말고)·`except Exception`·모델·파일 쓰기.
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
SLUG = "02-PostgresSaver-준비와-스키마"
TITLE_TEXT = "PostgresSaver 준비와 스키마"
SRC = ROOT / "textbook/part6/ch23-persistence/_src" / (SLUG + ".html")
# 교재 출력을 만든 실행의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답)에서 읽은 값
RUNSEC = os.environ.get("AUTHOR02_RUNSEC", "5초 안에")
RUNS_SENTENCE = os.environ.get("AUTHOR02_RUNS_SENTENCE", "새 커널로 두 번 실행했을 때 코드 셀 28개의 출력이 모두 같았습니다.")

INSTALL = install_source(["langgraph==1.2.11", "langgraph-checkpoint-postgres==3.0.5", "psycopg[binary,pool]==3.3.3"])

IMPORTS = r'''# 01절 그래프 이름(Ch 13 01·02절)에, PostgreSQL에 붙는 이름과 체크포인터 하나를 더해 가져옵니다
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
# 패키지 psycopg는 Ch 12 02절에서 PostgreSQL에 붙을 때 쓴 패키지입니다
import psycopg
from psycopg.rows import dict_row
# 체크포인트를 PostgreSQL 표에 쓰는 체크포인터입니다
from langgraph.checkpoint.postgres import PostgresSaver

print("이 절에서 새로 가져온 이름:", "dict_row", "PostgresSaver")'''

# 01절 임시 폴더 셀에서 앞머리만 바꾼 셀(아래 assert)
FOLDER = author_01.FOLDER.replace("ch23-01-", "ch23-02-")

CONNECT = r'''# Ch 12 02절과 같은 접속 글로 데이터베이스에 붙고, 서버 판 번호를 봅니다
database_url = "postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab"
conn = psycopg.connect(database_url, autocommit=True)
cur = conn.cursor()
cur.execute("SELECT current_setting('server_version')")
print("PostgreSQL 판:", cur.fetchone()[0])'''

DEF_TABLES = r'''# 이름 공간 ch23_lab 안의 표 이름을 이름 차례로 읽어, 목록으로 내놓습니다
def table_names(cursor):
    sql = "SELECT table_name FROM information_schema.tables"
    sql = sql + " WHERE table_schema = 'ch23_lab' ORDER BY table_name"
    cursor.execute(sql)
    names = []
    # 줄마다 첫 칸이 표 이름입니다
    for row in cursor.fetchall():
        names.append(row[0])
    return names'''

NAMESPACE = r'''# 이 절의 표를 담을 이름 공간 ch23_lab을, 있으면 안의 표까지 지우고 빈 채로 새로 만듭니다
cur.execute("DROP SCHEMA IF EXISTS ch23_lab CASCADE")
cur.execute("CREATE SCHEMA ch23_lab")
print("ch23_lab 안의 표:", table_names(cur))'''

SAVER_CONN = r'''# 체크포인터가 쓸 연결을 따로 열고, 이 연결이 표를 찾을 이름 공간을 ch23_lab으로 정합니다
saver_conn = psycopg.connect(database_url, autocommit=True, row_factory=dict_row)
saver_cur = saver_conn.cursor()
saver_cur.execute("SET search_path TO ch23_lab")
# SHOW 문장은 설정 값 하나를 한 줄로 내놓습니다
saver_cur.execute("SHOW search_path")
print("체크포인터 연결이 표를 찾는 이름 공간:", saver_cur.fetchone())'''

SAVER = r'''# 이 연결을 넘겨 PostgreSQL 체크포인터를 만듭니다(아직 표를 만들지 않음)
saver = PostgresSaver(saver_conn)
print("체크포인터의 종류:", type(saver).__name__)'''

MIGRATIONS = r'''# 표 만들기 때 차례로 실행할 문장 목록에서, 문장마다 첫 줄만 봅니다(데이터베이스에는 보내지 않음)
statements = PostgresSaver.MIGRATIONS
print("표 만들기 문장 수:", len(statements))
print("번호 | 문장의 첫 줄")
for number in range(len(statements)):
    # 앞뒤 빈칸과 줄바꿈을 떼고, 첫 줄만 남깁니다
    first_line = statements[number].strip().splitlines()[0]
    print(number, "|", first_line)'''

# 01절 셀과 글자까지 같다(아래 assert)
STATE = author_01.STATE
NODE = author_01.NODE
CONFIG_A = author_01.CONFIG_A
CONFIG_B = author_01.CONFIG_B
FILES = author_01.FILES

BUILD = r'''# 01절과 같은 노드 하나·엣지 둘을 설계 객체에 적고, PostgreSQL 체크포인터와 함께 컴파일합니다
builder = StateGraph(CountState)
builder.add_node("add", add_amount)
builder.add_edge(START, "add")
builder.add_edge("add", END)
graph = builder.compile(checkpointer=saver)
print("붙은 체크포인터의 종류:", type(graph.checkpointer).__name__)'''

BEFORE_RUN = r'''# 표 만들기 setup()을 부르지 않은 채 01절 첫 실행과 같은 입력으로 실행합니다(이 셀만 올라온 오류를 받아 출력합니다)
try:
    graph.invoke({"total": 0, "amount": 3, "trace": []}, config_a)
except psycopg.Error as error:
    print("받은 오류:", type(error).__name__)
    # diag.message_primary는 서버가 보낸 오류 글, sqlstate는 오류 번호입니다
    print("오류 글:", error.diag.message_primary)
    print("오류 번호:", error.sqlstate)'''

BEFORE_TABLES = r'''# 실행이 멈춘 뒤, 이름 공간 ch23_lab에 표가 생겼는지 다시 봅니다
print("ch23_lab 안의 표:", table_names(cur))'''

AFTER_SETUP = r'''# 표 만들기 setup()을 부르고, 이름 공간 ch23_lab에 생긴 표를 봅니다
saver.setup()
names_after = table_names(cur)
print("setup() 뒤 표 수:", len(names_after))
print("ch23_lab 안의 표:", names_after)
# 설치판의 표 만들기 문장이 정하는 수라, 실행마다 같아야 합니다
assert len(names_after) == 4, "setup() 뒤 표는 넷이어야 합니다"'''

VERSIONS = r'''# 표 만들기 기록 checkpoint_migrations에 적힌 판 번호를 작은 것부터 읽습니다
cur.execute("SELECT v FROM ch23_lab.checkpoint_migrations ORDER BY v")
versions = []
for row in cur.fetchall():
    versions.append(row[0])
print("표 만들기 기록 줄 수:", len(versions))
print("판 번호:", versions)'''

AFTER_FIRST = r'''# 5절 Before와 같은 입력으로 스레드 customer-a의 첫 실행을 합니다
first_result = graph.invoke({"total": 0, "amount": 3, "trace": []}, config_a)
print("첫 실행 결과:", first_result)'''

AFTER_SECOND = r'''# 같은 스레드로 이번 수 4만 넣어 다시 실행합니다(01절 6절 둘째 실행과 같은 입력)
second_result = graph.invoke({"amount": 4}, config_a)
print("둘째 실행 결과:", second_result)
# 표에 저장된 합계 3에서 이어 가므로, 실행마다 같아야 하는 값입니다
assert second_result["total"] == 7, "같은 스레드의 둘째 실행은 합계 7이어야 합니다"'''

DEF_COLUMNS = r'''# 이름 공간 ch23_lab의 표 하나에 있는 칸 이름을 놓인 차례대로 읽어, 목록으로 내놓습니다
def column_names(cursor, table_name):
    sql = "SELECT column_name FROM information_schema.columns"
    sql = sql + " WHERE table_schema = 'ch23_lab' AND table_name = %s"
    sql = sql + " ORDER BY ordinal_position"
    cursor.execute(sql, (table_name,))
    names = []
    for row in cursor.fetchall():
        names.append(row[0])
    return names'''

COLUMNS = r'''# 체크포인트를 담는 표 checkpoints의 칸 이름을 봅니다
print("표 checkpoints의 칸:", column_names(cur, "checkpoints"))'''

DEF_COUNT = r'''# 표 checkpoints에서 스레드 이름 하나의 줄 수를 셉니다(스레드 이름은 자리표시자 %s로 넘김)
def count_checkpoints(cursor, thread_name):
    sql = "SELECT count(*) FROM ch23_lab.checkpoints WHERE thread_id = %s"
    cursor.execute(sql, (thread_name,))
    return cursor.fetchone()[0]'''

ROWS_A = r'''# 스레드 customer-a의 체크포인트 목록 수와, 2절 연결로 센 표 checkpoints의 줄 수를 견줍니다
history_a = list(graph.get_state_history(config_a))
print("get_state_history로 센 수:", len(history_a))
rows_a = count_checkpoints(cur, "customer-a")
print("표 checkpoints의 customer-a 줄 수:", rows_a)
# 체크포인트 하나가 한 줄이라, 실행마다 같아야 하는 관계입니다
assert rows_a == len(history_a), "체크포인트 수와 표의 줄 수가 같아야 합니다"'''

SETUP_AGAIN = r'''# 값 바꿔 보기: 표가 이미 있는데 setup()을 한 번 더 부르고, 기록과 쌓인 줄을 다시 셉니다
saver.setup()
cur.execute("SELECT count(*) FROM ch23_lab.checkpoint_migrations")
print("둘째 setup() 뒤 표 만들기 기록 줄 수:", cur.fetchone()[0])
print("customer-a 줄 수:", count_checkpoints(cur, "customer-a"))'''

ROWS_TABLE = r'''# 두 스레드의 표 checkpoints 줄 수를 라벨 줄 아래에 차례로 출력합니다
print("스레드 | 표 checkpoints의 줄 수")
for thread_name in ["customer-a", "customer-b"]:
    print(thread_name, "|", count_checkpoints(cur, thread_name))'''

CLOSE = r'''# 체크포인터의 연결을 먼저 닫고 2절 연결로 줄 수를 다시 센 뒤, 2절 연결도 닫습니다
saver_conn.close()
print("체크포인터 연결 닫힘:", saver_conn.closed)
print("customer-a 줄 수:", count_checkpoints(cur, "customer-a"))
conn.close()
print("조회 연결 닫힘:", conn.closed)'''

FIG1 = "02-1-연결-둘과-이름-공간-하나"
FIG1_ALT = os.environ.get("AUTHOR02_FIG1_ALT", "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 접속 글 하나 127.0.0.1:55432 rag_lab에서 화살표 두 개가 나갑니다. 왼쪽 화살표는 초록 상자 체크포인터 연결 saver_conn autocommit=True dict_row search_path ch23_lab으로 가고, 그 아래 회색 상자 체크포인터 PostgresSaver 그래프 graph에 붙음으로 이어집니다. 오른쪽 화살표는 초록 상자 조회 연결 conn autocommit=True로 갑니다. 회색 상자에서 체크포인트를 씀, 조회 연결에서 표 이름과 줄 수를 읽음이라고 적힌 화살표가 맨 아래 칸 이름 공간 ch23_lab으로 모이고, 칸 안 노란 상자에는 setup() 뒤 표 넷 checkpoints checkpoint_blobs checkpoint_writes checkpoint_migrations가 적힌 그림")
FIG1_CAP = "접속 글 하나로 연결 둘을 열어, 하나는 체크포인터에 넘기고 하나로는 이름 공간 ch23_lab의 표를 직접 읽습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 우리가 넘긴 접속 글과 그것으로 연 연결 둘이고, 회색 상자는 라이브러리의 체크포인터입니다.
왼쪽 연결은 체크포인터에 넘기고, 오른쪽 연결로는 우리가 표를 직접 읽습니다.
노란 상자는 노트북 6절에서 출력으로 확인한 표 넷입니다."""

FIG2 = "02-2-표-만들기-문장-열과-기록-열-줄"
FIG2_ALT = os.environ.get("AUTHOR02_FIG2_ALT", "위에서 아래로 읽는 흐름도입니다. 맨 위 회색 상자 표 만들기 문장 열 개 속성 MIGRATIONS 번호 0부터 9에서 파란 상자 saver.setup() 처음 부름으로 갑니다. 그 아래 칸 setup() 뒤 이름 공간 ch23_lab 안에는 왼쪽 노란 상자 표 넷과 오른쪽 노란 상자 표 만들기 기록 판 번호 0부터 9 열 줄이 나란히 있습니다. 칸에서 파란 상자 saver.setup() 한 번 더를 지나, 맨 아래 노란 상자 기록 열 줄 그대로 customer-a 여섯 줄 그대로로 가는 그림")
FIG2_CAP = "표 만들기 문장 열 개가 한 번씩 실행되어 판 번호 열 줄이 적혔고, 둘째 setup()은 기록을 늘리지 않았습니다."
FIG2_READ = """위에서 아래로 읽습니다.
맨 위 회색 상자는 설치판 체크포인터 클래스가 가진 문장 목록이고, 노트북 3절에서 첫 줄만 보았습니다.
파란 상자는 우리가 부른 메서드이고, 노란 상자는 노트북 6·8절 출력입니다.
기록 열 줄과 문장 열 개는 판 번호로 짝을 이룹니다."""

FIG3 = "02-3-표를-만들기-전과-뒤"
FIG3_ALT = os.environ.get("AUTHOR02_FIG3_ALT", "위에서 아래로 읽는 그림입니다. 맨 위 파란 상자 같은 그래프 graph 같은 체크포인터 스레드 customer-a 입력 total 0 amount 3에서 칸 둘로 화살표가 갑니다. 왼쪽 칸 Before setup() 없이에는 빨간 상자 받은 오류 UndefinedTable 표 checkpoints 없음 오류 번호 42P01 아래로 빨간 상자 멈춘 뒤에도 ch23_lab 안의 표 없음이 있습니다. 오른쪽 칸 After setup() 뒤에는 노란 상자 표 넷 표 만들기 기록 열 줄 아래로 노란 상자 첫 실행 합계 3 둘째 실행 amount 4 합계 7이 있는 그림")
FIG3_CAP = "같은 그래프와 같은 입력인데, 표를 만들기 전에는 UndefinedTable을 받고 표를 만든 뒤에는 01절처럼 합계 7이 됩니다."
FIG3_READ = """맨 위 파란 상자는 두 칸이 함께 쓰는 그래프와 입력입니다.
왼쪽 칸은 노트북 5절 Before, 오른쪽 칸은 6절 After이고, 칸 안은 위에서 아래로 읽습니다.
빨간 상자는 Before의 결함 결과이고, 노란 상자는 After에서 출력으로 확인한 값입니다.
두 칸의 차이는 메서드 `setup()`을 불렀는지 하나입니다."""

FIG4 = "02-4-스레드마다-표에-쌓인-줄"
FIG4_ALT = os.environ.get("AUTHOR02_FIG4_ALT", "칸 둘이 나란히 놓이고 그 아래에 상자 둘이 있는 그림입니다. 왼쪽 칸 스레드 customer-a에는 노란 상자 get_state_history 체크포인트 여섯 아래 노란 상자 표 checkpoints 여섯 줄이 있습니다. 오른쪽 칸 스레드 customer-b에는 노란 상자 실행 결과 합계 4 아래 노란 상자 표 checkpoints 세 줄이 있습니다. 두 칸 아래 회색 상자에는 두 스레드 모두 같은 표 checkpoints 칸 thread_id의 값으로 갈림, 맨 아래 노란 상자에는 체크포인터 연결을 닫은 뒤에도 customer-a 여섯 줄 작업 폴더 파일 없음이 적힌 그림")
FIG4_CAP = "두 스레드의 체크포인트가 같은 표 checkpoints에 여섯 줄과 세 줄로 쌓였고, 체크포인터 연결을 닫은 뒤에도 줄 수는 그대로였습니다."
FIG4_READ = """칸 둘이 스레드 둘이고, 칸 안은 위에서 아래로 읽습니다.
칸 안 노란 상자는 노트북 7·8절 출력입니다.
가운데 회색 상자는 두 칸에 모두 해당하는 사실입니다.
맨 아래 노란 상자는 노트북 9절 출력입니다."""

ILLU = "02-5-속지를-끼운-사진첩과-빈-사진첩"
ILLU_ALT = os.environ.get("AUTHOR02_ILLU_ALT", "흰 바탕에 넓은 나무 탁자 하나가 있고, 그 위에 펼친 고리 사진첩 둘이 왼쪽과 오른쪽에 떨어져 놓인 그림입니다. 왼쪽 사진첩의 고리에는 사진을 꽂는 비닐 속지가 없고, 안쪽에는 파란 판만 있습니다. 왼쪽 사진첩 밖 탁자 위에는 작은 체스판이 찍힌 즉석사진 한 장이 따로 놓여 있습니다. 오른쪽 사진첩의 고리에는 비닐 속지 한 장이 끼워져 있고, 같은 즉석사진 여섯 장이 두 장씩 세 줄로 꽂혀 있습니다. 두 사진첩 사이 앞쪽에는 즉석카메라 하나가 있는 그림")
ILLU_CAP = os.environ.get("AUTHOR02_ILLU_CAP", "속지가 없는 왼쪽 사진첩에는 사진을 꽂을 자리가 없고, 속지를 끼운 오른쪽 사진첩에는 사진 여섯 장이 꽂혔습니다.")
ILLU_READ = os.environ.get("AUTHOR02_ILLU_READ", "탁자 위에 펼친 사진첩 둘이 왼쪽과 오른쪽에 있고, 그 사이 앞쪽에 카메라 하나가 있습니다. 왼쪽 사진첩은 Before로, 고리에 비닐 속지가 없어 사진 한 장이 사진첩 밖에 따로 놓였습니다. 오른쪽 사진첩은 After로, 속지 한 장에 사진 여섯 장이 두 장씩 세 줄로 꽂혔습니다. 속지는 표 <code>checkpoints</code>, 사진 여섯 장은 스레드 <code>customer-a</code>의 여섯 줄, 카메라는 01절처럼 체크포인터입니다. 나머지 표 셋은 그림에 없고, 사진첩 안쪽의 파란 판은 코드의 무엇과도 짝짓지 않습니다.")

DOCKER = """```bash
docker run --name hankyung-part3-pgvector \\
  -e POSTGRES_USER=student \\
  -e POSTGRES_PASSWORD=local-practice-only \\
  -e POSTGRES_DB=rag_lab \\
  -p 127.0.0.1:55432:5432 \\
  -d pgvector/pgvector:0.8.2-pg17
```"""

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 01절 그래프에 PostgreSQL 체크포인터를 붙이고, 표를 만들기 전에 실행해 받은 오류를 봅니다.
2. 메서드 `setup()`으로 표를 만든 뒤 같은 입력으로 다시 실행하고, 생긴 표와 표 만들기 기록을 읽습니다.
3. 체크포인트가 데이터베이스 표에 스레드마다 한 줄씩 쌓이는 것을 셉니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
01절처럼 매번 같은 값을 내는 우리 노드로, 저장된 값이 맞는지 출력으로 가릅니다.

PostgreSQL 서버가 `127.0.0.1:55432`에서 켜져 있어야 합니다.
Ch 12 02절에서 만든 Docker 컨테이너 `hankyung-part3-pgvector`를 그대로 씁니다.
꺼져 있으면 터미널에서 `docker start hankyung-part3-pgvector`로 켭니다.
컨테이너가 없으면 Ch 12 실습 폴더 `README.md`와 같은 아래 명령으로 먼저 만듭니다.

""" + DOCKER + """

노트북은 데이터베이스 `rag_lab` 안에 이름 공간 `ch23_lab`을 만들어 씁니다.
다시 실행하면 그 이름 공간만 지우고 처음부터 만듭니다.
작업 폴더에는 파일을 쓰지 않고, 읽어 오는 자료 파일도 없습니다.
교재 출력을 만든 실행에서는 노트북 전체가 """ + RUNSEC + """ 끝났습니다.

**기준 버전** — 첫 셀에서 패키지 셋을 설치합니다.
판은 langgraph 1.2.11과 langgraph-checkpoint-postgres 3.0.5입니다.
패키지 psycopg의 판은 3.3.3입니다.

교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다.
그 서버는 Docker 컨테이너가 아니라, 같은 접속 글로 켠 서버입니다.
데이터베이스 PostgreSQL의 필수 최소 판은 설치한 패키지 설명에 없고, 17 말고는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~7절을 읽습니다.
데이터베이스에 붙고, 표를 만들기 전과 뒤를 견주고, 쌓인 줄을 세는 자리입니다.
8·9절은 값을 바꿔 보고 연결을 닫는 자리이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch23-persistence`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

01절의 체크포인터 `InMemorySaver`는 이 프로그램의 메모리에만 저장했습니다.
이 절은 체크포인트를 PostgreSQL 데이터베이스의 표에 쓰는 체크포인터 `PostgresSaver`를 씁니다.
이 체크포인터는 쓰기 전에, 체크포인트를 담을 표를 먼저 만들어야 합니다.
표를 만들지 않고 실행한 것이 5절의 Before, 표를 만든 뒤 실행한 것이 6절의 After입니다.

첫 셀은 패키지 셋을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langgraph: 1.2.11`·`langgraph-checkpoint-postgres: 3.0.5`·`psycopg: 3.3.3`이 보입니다.
세 판 모두 실습 폴더 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
상태 형식과 그래프를 만드는 이름은 01절과 같습니다.
패키지 psycopg는 Ch 12 02절에서 PostgreSQL에 붙을 때 쓴 패키지입니다.
새로 가져오는 이름은 `dict_row`와 체크포인터 `PostgresSaver` 둘이고, 뜻은 3절에서 풉니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `이 절에서 새로 가져온 이름: dict_row PostgresSaver`가 보입니다.
이름 `dict_row`는 패키지 psycopg에 들어 있습니다.
체크포인터 `PostgresSaver`는 첫 셀에서 설치한 langgraph-checkpoint-postgres에 들어 있습니다.

다음 셀은 01절처럼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다.
이 절의 체크포인트는 데이터베이스 서버에 저장되니, 작업 폴더에는 파일이 생기지 않을 것입니다.
9절에서 폴더가 그대로 비어 있는지 봅니다."""),
        setup(FOLDER),
        md("""**결과 읽기** — 출력 줄 `임시 폴더 이름에 ch23-02-이 들어 있는가: True`로, 이 절의 폴더를 만들었습니다.
출력 줄 `현재 작업 폴더의 파일: []`로, 빈 폴더에서 시작합니다.

## 2. 데이터베이스에 붙기

이 절은 Ch 12 02절의 PostgreSQL 컨테이너를 그대로 씁니다.
다음 셀은 Ch 12 02절과 같은 접속 글로 데이터베이스에 붙고, 서버 판 번호를 봅니다.
함수 `psycopg.connect`와 인자 `autocommit=True`는 그 절에서 배웠습니다.
메서드 `cursor`·`execute`·`fetchone`도 그 절과 같습니다.
접속 글에는 수업 전용 암호가 들어 있어 출력하지 않습니다."""),
        code(CONNECT),
        md("""**결과 읽기** — 출력 줄 `PostgreSQL 판: 17.11`이 보입니다.
서버에 붙었고, 문장 하나를 실행해 답을 받았습니다.
이 판 번호는 교재 출력을 만든 서버의 값이라, 컨테이너에 따라 다르게 나올 수 있습니다.
서버가 꺼져 있으면 이 셀이 오류 `OperationalError`로 멈춥니다.
이 장면은 노트북 밖에서 확인했고, 이 노트북에서는 실행하지 않았습니다.

체크포인터의 표는 데이터베이스 안의 이름 공간 하나에 모아 둡니다.
이름 공간(SQL 낱말 `SCHEMA`)은 한 데이터베이스 안에서 표들을 이름으로 묶어 두는 자리입니다.
사진첩 한 권에 그 사진첩의 속지만 끼워 두는 것과 같습니다.
이 절의 이름 공간은 `ch23_lab`이고, Ch 12 표와 섞이지 않게 따로 둡니다.

다음 셀은 이름 공간 `ch23_lab` 안의 표 이름을 목록으로 읽는 함수입니다.
데이터베이스 PostgreSQL은 이름 공간 `information_schema`의 목록 `tables`에 표를 한 줄씩 보여 줍니다.
Ch 4 03절의 `SELECT … WHERE … ORDER BY` 모양으로, 이름 공간이 `ch23_lab`인 줄만 이름 차례로 읽습니다."""),
        code(DEF_TABLES),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `table_names`는 인자로 받은 커서로 문장을 실행하고, 줄마다 첫 칸인 표 이름을 목록에 담습니다.

다음 셀은 이름 공간 `ch23_lab`을 만듭니다.
문장 `DROP SCHEMA IF EXISTS ch23_lab CASCADE`는 그 이름 공간이 있으면 안의 표까지 함께 지웁니다.
노트북을 다시 실행해도 빈 이름 공간에서 시작하려는 줄이고, 다른 이름 공간의 표는 지우지 않습니다.
문장 `CREATE SCHEMA ch23_lab`이 빈 이름 공간을 새로 만듭니다."""),
        code(NAMESPACE),
        md("""**결과 읽기** — 출력 줄 `ch23_lab 안의 표: []`입니다.
이름 공간은 생겼지만, 아직 표는 하나도 없습니다.

## 3. PostgreSQL 체크포인터 만들기

이 체크포인터는 데이터베이스에 붙은 연결 하나를 받아, 그 연결로 체크포인트를 쓰고 읽습니다.
다음 셀은 체크포인터가 쓸 연결을 2절 연결과 따로 엽니다.
인자 `row_factory=dict_row`는 받아 온 줄을, 칸 이름이 키인 딕셔너리로 내놓게 합니다.
설치판 패키지 설명은 연결을 직접 만들 때 이 인자와 `autocommit=True`를 함께 주라고 적습니다.
문장 `SET search_path TO ch23_lab`은 이 연결이 이름 공간을 적지 않은 표 이름을 `ch23_lab`에서 찾게 합니다."""),
        code(SAVER_CONN),
        md("""**결과 읽기** — 출력 줄 `체크포인터 연결이 표를 찾는 이름 공간: {'search_path': 'ch23_lab'}`입니다.
받아 온 줄이 튜플이 아니라, 칸 이름 `search_path`가 키인 딕셔너리로 나왔습니다.
이 연결로 이름 공간을 적지 않은 표를 만들면, 그 표도 `ch23_lab`에 생깁니다.

다음 셀은 이 연결을 넘겨 체크포인터를 만듭니다.
클래스 `PostgresSaver`는 연결 하나를 받아, 체크포인트를 PostgreSQL 표에 쓰는 체크포인터를 만듭니다."""),
        code(SAVER),
        md("""**결과 읽기** — 출력 줄 `체크포인터의 종류: PostgresSaver`입니다.
설치판 소스로 보면, 체크포인터를 만드는 것만으로는 데이터베이스에 문장을 보내지 않습니다.

표를 만드는 일은 메서드 `setup()`이 맡습니다.
이 메서드가 실행할 문장들은 클래스의 속성 `MIGRATIONS`에 목록으로 들어 있습니다.
속성 이름은 Ch 21 04절의 「옮기기」와 같은 영어 낱말이지만, 여기서는 표를 만들고 고치는 문장의 차례입니다.
다음 셀은 데이터베이스에 보내지 않고, 이 목록의 문장마다 첫 줄만 봅니다."""),
        code(MIGRATIONS),
        md("""**결과 읽기** — 출력 줄 `표 만들기 문장 수: 10`입니다.
라벨 줄 `번호 | 문장의 첫 줄` 아래 열 줄을 봅니다.
번호 0부터 3까지 네 문장이 표 넷을 만들고, 번호 6부터 8까지 세 문장은 칸 `thread_id`에 색인을 만듭니다.
번호 4와 9는 이미 만든 표의 칸을 고치고, 번호 5의 `SELECT 1;`은 아무것도 바꾸지 않는 문장입니다.

## 4. 01절 그래프에 붙이기

그래프는 01절과 같은 상태 형식과 노드로 만듭니다.
다음 두 셀은 01절 2절의 상태 형식 셀·노드 셀과 글자까지 같습니다."""),
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 `total`은 합계, `amount`는 이번 수, `trace`는 실행 흔적입니다.

다음 셀은 01절과 같은 노드 함수입니다."""),
        code(NODE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `add_amount`는 합계에 이번 수를 더한 값과, 실행 흔적 한 칸을 냅니다.

다음 셀은 01절처럼 노드 하나와 엣지 둘을 설계 객체에 적습니다.
컴파일할 때 인자 `checkpointer`에 3절의 PostgreSQL 체크포인터를 넘깁니다.
01절 4절과 다른 곳은 넘긴 체크포인터 하나뿐입니다."""),
        code(BUILD),
        md("""**결과 읽기** — 출력 줄 `붙은 체크포인터의 종류: PostgresSaver`입니다.
그래프에 PostgreSQL 체크포인터가 붙었습니다.
아직 메서드 `setup()`을 부르지 않았으니, 2절에서 만든 이름 공간에는 표가 없습니다.

다음 셀은 01절 5절과 같은 설정 딕셔너리를 만듭니다.
스레드 이름도 01절과 같은 `customer-a`입니다."""),
        code(CONFIG_A),
        md("""**결과 읽기** — 출력 줄 `스레드 customer-a의 설정: {'configurable': {'thread_id': 'customer-a'}}`입니다.
01절 노트북의 체크포인트는 그 커널의 메모리에 있었고, 이 노트북과는 상관이 없습니다.

## 5. 표를 만들기 전에 실행하기 (Before)""", lesson_part="before"),
        md("""다음 셀은 표 만들기 `setup()`을 부르지 않은 채, 01절 첫 실행과 같은 입력으로 그래프를 실행합니다.
실행 전에 예상해 봅니다.
체크포인트를 담을 표가 없으니, 어딘가에서 멈출 것입니다.
이 셀만 올라온 오류를 받아 출력하고, 셀은 끝까지 갑니다.
받는 오류는 Ch 12 02절처럼 psycopg 오류 전체인 `psycopg.Error`입니다.""", lesson_part="before"),
        code(BEFORE_RUN, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `받은 오류: UndefinedTable`입니다.
오류 글 `relation "checkpoints" does not exist`는 표 `checkpoints`가 없다는 뜻입니다.
출력 줄 `오류 번호: 42P01`은 PostgreSQL이 이 오류에 붙이는 다섯 글자 번호입니다.
오류 이름 `UndefinedTable`은 `psycopg.Error`의 한 종류라, 이 `except` 줄이 받았습니다.

설치판 소스로 보면, 그래프는 실행을 시작할 때 그 스레드의 마지막 체크포인트를 먼저 찾습니다.
찾을 표가 없어 그 자리에서 멈췄고, 메서드 `invoke`는 결과를 내놓지 못했습니다.
오류를 받지 않는 실제 프로그램이라면 여기서 멈춥니다.
이것이 이 절의 Before 결함입니다.
노트북 밖에서 본 `OperationalError`는 서버가 꺼져서 난 오류였고, 이 오류는 서버에 붙었지만 표가 없어서 났습니다.

다음 셀은 실행이 멈춘 뒤, 이름 공간 `ch23_lab`에 표가 생겼는지 다시 봅니다.""", lesson_part="before"),
        code(BEFORE_TABLES, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `ch23_lab 안의 표: []`로, 표는 여전히 하나도 없습니다.
체크포인터를 붙인 그래프를 실행해도, 이 체크포인터는 표를 스스로 만들지 않았습니다.

## 6. 표를 만든 뒤 실행하기 (After)""", lesson_part="after"),
        md("""이제 결함을 고칩니다.
표 만들기(`setup()`)는 체크포인터가 쓸 표를 데이터베이스에 만드는 일입니다.
빈 사진첩에 속지를 끼워, 사진을 꽂을 자리를 먼저 마련하는 것과 같습니다.
다음 셀은 3절의 문장들을 실행하는 메서드 `saver.setup()`을 부르고, 이름 공간 `ch23_lab`의 표를 다시 봅니다.
셀 끝 `assert`는 실행마다 같아야 하는 표 수에만 겁니다.""", lesson_part="after"),
        code(AFTER_SETUP, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `setup() 뒤 표 수: 4`입니다.
라벨 `ch23_lab 안의 표:` 뒤 목록에 표 넷이 이름 차례로 있습니다.
표 `checkpoints`는 체크포인트를 한 줄씩 담는 표이고, 7절에서 줄을 셉니다.
나머지 셋의 쓰임은 설치판 소스로 보면 이렇습니다.
표 `checkpoint_blobs`는 수·글이 아닌 칸 값을, `checkpoint_writes`는 체크포인트에 딸린 쓰기를 따로 담습니다.

표 `checkpoint_migrations`는 표 만들기 기록입니다.
표 만들기 기록은 표 만들기 문장 가운데 어디까지 실행했는지 판 번호로 적어 두는 표입니다.
속지를 끼울 때마다 끼운 차례를 적어 두는 목록과 같습니다.
다음 셀은 이 표에 적힌 판 번호를 작은 것부터 읽습니다.""", lesson_part="after"),
        code(VERSIONS, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `표 만들기 기록 줄 수: 10`과 `판 번호: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`입니다.
3절에서 본 표 만들기 문장 열 개가 모두 실행되어, 문장마다 판 번호 한 줄이 적혔습니다.
설치판 소스에서 `setup()`은 먼저 이 기록 표를 만드는 0번 문장을 실행합니다.
그 문장은 표가 이미 있으면 아무 일도 하지 않고, 그다음에는 마지막 판 번호 뒤 문장만 실행합니다.
그래서 이 기록이 있으면, 이미 실행한 1번부터의 문장은 다시 실행하지 않습니다.

다음 셀은 5절과 같은 입력으로 스레드 `customer-a`의 첫 실행을 합니다.
실행 전에 예상해 봅니다.
이제 표가 있으니 01절 첫 실행처럼 합계 3이 나올 것입니다.""", lesson_part="after"),
        code(AFTER_FIRST, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `첫 실행 결과: {'total': 3, 'amount': 3, 'trace': ['add']}`는 01절 첫 실행과 같습니다.
5절과 같은 그래프·체크포인터·입력이고, 달라진 것은 `setup()` 한 줄뿐입니다.

다음 셀은 01절 6절처럼 같은 스레드로 이번 수 4만 넣어 다시 실행합니다.
체크포인터가 표에서 합계 3을 읽어 오면, 01절처럼 합계 7이 될 것입니다.
셀 끝 `assert`는 실행마다 같아야 하는 합계에만 겁니다.""", lesson_part="after"),
        code(AFTER_SECOND, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `둘째 실행 결과: {'total': 7, 'amount': 4, 'trace': ['add', 'add']}`입니다.
합계가 표에 저장된 3에서 이어져 7이 되었고, 01절 6절과 같은 값입니다.
체크포인터를 `InMemorySaver`에서 `PostgresSaver`로 바꿔도, 같은 스레드로 다시 실행한 결과는 같았습니다.

## 7. 표의 구조와 쌓인 줄 보기

이 절 제목의 마지막 말은 체크포인터가 쓰는 표들의 구조, 곧 표 이름과 표의 칸을 가리킵니다.
SQL 낱말 `SCHEMA`는 같은 영어 낱말이지만, 이 절은 그것을 이름 공간이라고 불렀습니다.
표 이름은 6절에서 보았으니, 이번에는 표 `checkpoints`의 칸을 봅니다.
다음 셀은 표 하나의 칸 이름을 놓인 차례대로 읽는 함수입니다.
표 이름은 이 문장의 값 자리라, Ch 12 02절처럼 자리표시자 `%s`로 넘깁니다.""", lesson_part="after"),
        code(DEF_COLUMNS, lesson_part="after"),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
목록 `columns`는 `tables`와 같은 이름 공간 `information_schema`에 있고, 표의 칸을 한 줄씩 보여 줍니다.
칸 `ordinal_position`은 그 표에서 칸이 놓인 차례입니다.

다음 셀은 표 `checkpoints`의 칸 이름을 봅니다.""", lesson_part="after"),
        code(COLUMNS, lesson_part="after"),
        md("""**결과 읽기** — 라벨 `표 checkpoints의 칸:` 뒤 목록에 칸 이름 일곱 개가 있습니다.
칸 `thread_id`에 스레드 이름이 들어가, 한 표 안에서 스레드마다 줄을 가를 수 있습니다.
칸 `checkpoint`에는 체크포인트 내용이 들어갑니다.
칸 `checkpoint_id`는 체크포인트마다 다른 이름이라, 이 절은 그 값을 출력하지 않습니다.

다음 셀은 표 `checkpoints`에서 스레드 이름 하나의 줄 수를 세는 함수입니다.
스레드 이름을 자리표시자 `%s`로 넘기고, Ch 12 02절처럼 `count(*)`로 줄 수를 셉니다.""", lesson_part="after"),
        code(DEF_COUNT, lesson_part="after"),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
원소 하나짜리 튜플 `(thread_name,)`은 값 하나를 자리표시자에 넘기는 모양입니다.

다음 셀은 스레드 `customer-a`의 체크포인트를 두 가지로 셉니다.
하나는 01절의 메서드 `get_state_history`, 다른 하나는 표 `checkpoints`의 줄 수입니다.
표는 체크포인터의 연결이 아니라, 2절에서 연 연결로 셉니다.
셀 끝 `assert`는 두 수가 같은지에만 겁니다.""", lesson_part="after"),
        code(ROWS_A, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `get_state_history로 센 수: 6`과 `표 checkpoints의 customer-a 줄 수: 6`입니다.
01절처럼 실행 두 번에 체크포인트가 셋씩, 모두 여섯이 쌓였습니다.
체크포인트 하나가 표 `checkpoints`의 한 줄입니다.
체크포인터가 쓴 줄을, 다른 연결에서도 같은 수로 셀 수 있었습니다.

## 8. 값 바꿔 보기 · 표 만들기를 한 번 더, 스레드 이름 바꾸기

첫째로 바꿀 것은 `setup()`을 부르는 횟수입니다.
실행 전에 예상해 봅니다.
표 만들기 기록이 있으니 새로 실행할 문장이 없어, 기록은 열 줄 그대로일 것입니다.
표 `checkpoints`에 쌓인 줄도 그대로 남을 것입니다.""", lesson_part="after"),
        code(SETUP_AGAIN, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `둘째 setup() 뒤 표 만들기 기록 줄 수: 10`과 `customer-a 줄 수: 6`입니다.
두 번째로 불러도 오류가 없었고, 표 만들기 기록과 쌓인 줄이 그대로입니다.
이 판에서는 표를 이미 만든 데이터베이스에서 `setup()`을 다시 불러도 괜찮았습니다.

둘째로 바꿀 것은 스레드 이름 하나입니다.
다음 셀은 01절 9절과 같은 셀로, 새 스레드 `customer-b`에 합계 0과 이번 수 4를 넣습니다.
실행 전에 예상해 봅니다.
표 `checkpoints`에는 스레드 `customer-b`의 줄이 따로 세 줄 생길 것입니다.""", lesson_part="after"),
        code(CONFIG_B, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `customer-b 실행 결과: {'total': 4, 'amount': 4, 'trace': ['add']}`는 01절 9절과 같습니다.

다음 셀은 두 스레드의 줄 수를 라벨 줄 아래에 차례로 출력합니다.""", lesson_part="after"),
        code(ROWS_TABLE, lesson_part="after"),
        md("""**결과 읽기** — 라벨 줄 `스레드 | 표 checkpoints의 줄 수` 아래 두 줄입니다.
줄 `customer-a | 6`과 `customer-b | 3`으로, 스레드마다 실행 횟수에 맞는 줄이 따로 쌓였습니다.
두 스레드의 줄은 같은 표에 있고, 칸 `thread_id`의 값으로 갈립니다.

## 9. 연결 닫기와 작업 폴더

다음 셀은 체크포인터의 연결을 먼저 닫고, 2절 연결로 스레드 `customer-a`의 줄 수를 다시 셉니다.
그다음 2절 연결도 닫습니다.
실행 전에 예상해 봅니다.
체크포인트가 데이터베이스 서버의 표에 있으니, 체크포인터 연결을 닫아도 여섯 줄 그대로일 것입니다.""", lesson_part="after"),
        code(CLOSE, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `체크포인터 연결 닫힘: True`와 `customer-a 줄 수: 6`입니다.
체크포인터의 연결을 닫은 뒤에도, 표의 줄은 그대로 남았습니다.
출력 줄 `조회 연결 닫힘: True`로 두 연결을 모두 닫았습니다.
그래프 `graph`의 체크포인터는 닫힌 연결을 가지고 있어, 이 노트북은 여기부터 그래프를 쓰지 않습니다.

다음 셀은 01절 11절처럼 작업 폴더에 파일이 생겼는지 봅니다.""", lesson_part="after"),
        code(FILES, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `현재 작업 폴더의 파일: []`과 `파일 수: 0`입니다.
체크포인트는 작업 폴더가 아니라 데이터베이스 서버에 저장되었습니다.

## 정리

1. 표 만들기 전에 실행하자, 표 `checkpoints`가 없어 오류 `UndefinedTable`을 받았습니다.
2. 메서드 `setup()`은 표 넷을 만들고, 표 만들기 기록에 판 번호 열 줄을 적었습니다.
3. 표를 만든 뒤에는 01절처럼 합계 7이 되었고, 체크포인트 여섯이 표에 여섯 줄로 쌓였습니다.

03절에서는 연결과 그래프 객체를 새로 만들어도, 같은 스레드의 대화를 이어 가는지 봅니다.""", lesson_part="after"),
    ]


L_CH02_05 = author_01.L_CH02_05
L_CH04_03 = author_01.L_CH04_03
L_CH12_02 = "../../part3/ch12-retrieval-tuning/02-pgvector와-HNSW.html"
L_CH21_04 = "../ch21-create-agent/04-0x에서-1x로-마이그레이션.html"
L_01 = "01-체크포인터와-스레드.html"
L_03 = "03-스레드-재개와-대화-이어가기.html"
L_05 = "05-pending-writes와-장애-복구.html"

COMPARE_ROWS = [
    ("메서드 <code>setup()</code>", "부르지 않음", "부름"),
    ("스레드 <code>customer-a</code> 첫 실행", "받은 오류 <code>UndefinedTable</code>·오류 번호 <code>42P01</code>", "합계 3"),
    ("같은 스레드 둘째 실행", "—", "합계 7"),
    ("이름 공간 <code>ch23_lab</code> 안의 표", "없음 <code>[]</code>", "넷"),
    ("표 만들기 기록", "—", "열 줄(판 번호 0~9)"),
    ("표 <code>checkpoints</code>의 <code>customer-a</code> 줄", "—", "여섯"),
]

LOOK_B5 = "노트북 2절에서 이름 공간 <code>ch23_lab</code>이 빈 목록 <code>[]</code>으로 시작하는지 봅니다. 3절 출력 <code>{'search_path': 'ch23_lab'}</code>로 체크포인터 연결이 이 이름 공간을 보는지 확인합니다. 3절 출력 <code>표 만들기 문장 수: 10</code>의 열 문장이 6절에서 실행됩니다."
LOOK_B6 = "노트북 5절 출력 <code>받은 오류: UndefinedTable</code>·<code>오류 번호: 42P01</code>과 6절 출력 <code>setup() 뒤 표 수: 4</code>로 Before와 After를 견줍니다. 7절 출력 <code>표 checkpoints의 customer-a 줄 수: 6</code>과 8절 줄 <code>customer-b | 3</code>으로 줄이 스레드마다 쌓이는 것을 셉니다."


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
    compare = table_html(["견준 것", "Before(표 만들기 전)", "After(표 만들기 뒤)"], COMPARE_ROWS)
    return """<!--meta: 강의 1h | 실습 1.5h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>PostgreSQL 체크포인터를 표 만들기 전에 쓰면 받는 오류와, 메서드 <code>setup()</code> 뒤의 결과를 견줄 수 있습니다.</li>
<li>메서드 <code>setup()</code>이 만든 표 넷과 표 만들기 기록을 SQL로 읽을 수 있습니다.</li>
<li>체크포인트가 표 <code>checkpoints</code>에 스레드마다 한 줄씩 쌓이는 것을 셀 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_01 + """\">01절</a>의 체크포인터 <code>InMemorySaver</code>는 이 프로그램의 메모리에만 저장했습니다. 체크포인트를 프로그램 밖에 남기려면, 파일이나 데이터베이스에 써야 합니다. 이 절은 PostgreSQL 데이터베이스의 표에 쓰는 체크포인터 <code>PostgresSaver</code>를 씁니다. 이 체크포인터는 쓰기 전에, 체크포인트를 담을 표를 먼저 만들어야 합니다.</p><p>표를 만들지 않고 실행하면 무엇이 일어나는지가 이 절의 Before입니다. 표를 만든 뒤 같은 입력으로 실행하는 것이 After입니다. 제목의 마지막 말은 체크포인터가 쓰는 표들의 구조, 곧 표 이름과 표의 칸을 가리킵니다. SQL 낱말 <code>SCHEMA</code>는 같은 영어 낱말이지만, 이 절은 그것을 이름 공간이라고 부르고 제목의 말과 나눠 씁니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH12_02 + """\">Ch 12 02절</a>에서는 패키지 psycopg로 PostgreSQL에 붙어, 메서드 <code>execute</code>와 <code>fetchone</code>으로 문장을 실행했습니다. 값은 자리표시자 <code>%s</code>로 넘겼고, 오류는 <code>except psycopg.Error as error</code>로 받았습니다. 이 절도 같은 접속 글과 같은 Docker 컨테이너를 씁니다.</p><p><a href=\"""" + L_CH04_03 + """\">Ch 4 03절</a>에서는 SQLite 표를 <code>SELECT … WHERE … ORDER BY</code>로 조회했습니다. 이 절은 같은 모양의 문장으로, PostgreSQL이 보여 주는 표 목록과 칸 목록을 읽습니다. 오류를 그 셀에서만 받는 <code>try</code>·<code>except</code>는 <a href=\"""" + L_CH02_05 + """\">Ch 2 05절</a>에서 배웠습니다.</p><p><a href=\"""" + L_01 + """\">01절</a>에서는 체크포인터를 붙인 그래프로 스레드 <code>customer-a</code>의 합계를 3에서 7로 이어 갔습니다. 체크포인트는 실행 한 번에 셋씩, 모두 여섯이 쌓였습니다. 이 절은 같은 상태 형식과 노드로 그래프를 만들고, 체크포인터만 바꿉니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절의 체스판과 즉석사진을 떠올립니다. 사진을 오래 남기려면, 사진을 꽂아 둘 사진첩이 있어야 합니다. 그런데 새로 산 사진첩에는 비닐 속지가 끼워져 있지 않습니다. 속지가 없으면 사진을 찍고도 꽂을 자리가 없습니다.</p><p>속지를 먼저 끼워 두면, 그때부터 사진을 꽂을 수 있습니다. 데이터베이스의 이름 공간이 사진첩 한 권이고, 표가 속지입니다. 메서드 <code>setup()</code>은 빈 사진첩에 속지를 끼우는 일이고, 이 절에서는 표 넷을 한꺼번에 만듭니다. 사진 한 장이 표 <code>checkpoints</code>의 한 줄, 곧 체크포인트 하나입니다. 01절의 메모리 체크포인터는 사진첩까지 카메라가 들고 있었다면, 이 절은 사진첩을 카메라 밖에 둡니다.</p>
""" + illustration_block() + """<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>이름 공간(SQL 낱말 <code>SCHEMA</code>)</td><td>한 데이터베이스 안에서 표들을 이름으로 묶어 두는 자리입니다. 사진첩 한 권에 그 사진첩의 속지만 끼워 두는 것과 같습니다. 이 절에서는 <code>CREATE SCHEMA ch23_lab</code>으로 만들고, 체크포인터의 표가 모두 여기에 생깁니다.</td></tr><tr><td>표 만들기(<code>setup()</code>)</td><td>체크포인터가 쓸 표를 데이터베이스에 만드는 일입니다. 빈 사진첩에 속지를 끼우는 일과 같습니다. 이 절에서는 메서드 <code>saver.setup()</code>이 표 넷을 만들었습니다.</td></tr><tr><td>표 만들기 기록(표 <code>checkpoint_migrations</code>)</td><td>표 만들기 문장 가운데 어디까지 실행했는지, 판 번호로 적어 두는 표입니다. 속지를 끼울 때마다 끼운 차례를 적어 두는 목록과 같습니다. 이 절에서는 판 번호 0부터 9까지 열 줄이 적혔습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 이름 공간은 노트북 2절의 <code>CREATE SCHEMA ch23_lab</code>으로 만들고, 3절의 <code>SET search_path TO ch23_lab</code>으로 체크포인터 연결에 알려 줍니다. 표 만들기는 6절의 <code>saver.setup()</code> 한 줄입니다. 표 만들기 기록은 6절 출력 <code>표 만들기 기록 줄 수: 10</code>의 열 줄입니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>표를 먼저 만들어야 하는 까닭</h3><p>그래프는 실행을 시작할 때 그 스레드의 마지막 체크포인트를 찾고, 단계를 마칠 때마다 체크포인트를 씁니다. PostgreSQL 체크포인터는 이 일을 표 <code>checkpoints</code>에 문장을 보내 합니다. 표가 없으면 첫 문장에서 PostgreSQL이 오류를 냅니다. 설치판 소스의 메서드 설명도, 처음 쓸 때 사용자가 <code>setup()</code>을 직접 불러야 한다고 적습니다.</p><p>메서드 <code>setup()</code>이 실행하는 문장은 클래스의 속성 <code>MIGRATIONS</code>에 열 개가 들어 있습니다. 속성 이름은 <a href=\"""" + L_CH21_04 + """\">Ch 21 04절</a>의 「옮기기」와 같은 영어 낱말이지만, 여기서는 표를 만들고 고치는 문장의 차례입니다. 실행한 문장은 표 만들기 기록에 판 번호로 남습니다. 설치판 소스에서 다음에 부르면, 기록 표를 만드는 0번 문장을 먼저 실행합니다. 이 문장은 표가 이미 있으면 아무 일도 하지 않고, 그 뒤에는 마지막 판 번호 뒤 문장만 실행합니다.</p>
<h3>다른 상황에 적용</h3><p>새 데이터베이스에 체크포인터를 처음 붙일 때 <code>setup()</code>을 한 번 부릅니다. 표를 이미 만든 데이터베이스라면, 노트북 8절처럼 다시 불러도 기록과 쌓인 줄이 그대로였습니다. 여러 프로그램이 같은 표를 함께 쓰는 모습은 이번에 실행하지 않았습니다.</p>
<h3>비교와 경계</h3><p>01절 <code>InMemorySaver</code>는 표를 만들 일이 없었지만, 체크포인트가 프로그램의 메모리에만 있었습니다. 이 절의 체크포인트는 데이터베이스 서버의 표에 남아, 다른 연결로도 셀 수 있었습니다. 체크포인터의 연결을 닫은 뒤에도 표의 줄 수는 그대로였습니다. <a href=\"""" + L_03 + """\">03절</a>에서 쓸 SQLite 체크포인터는 필요할 때 표를 스스로 만듭니다. 설치한 langgraph-checkpoint-sqlite 3.0.3 소스가 그렇게 적습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북을 실행하기 전에 PostgreSQL 서버를 켜 둡니다. Ch 12 02절에서 만든 Docker 컨테이너 <code>hankyung-part3-pgvector</code>를 그대로 씁니다. 꺼져 있으면 <code>docker start hankyung-part3-pgvector</code>로 켭니다. 컨테이너가 없으면 이 챕터 실습 폴더 <code>README.md</code>에 적은 <code>docker run</code> 명령으로 만들고, 같은 명령이 노트북 첫 셀에도 있습니다. 접속 글은 Ch 12 02절과 같은 <code>postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab</code>입니다.</p><p>노트북은 데이터베이스 <code>rag_lab</code> 안에 이름 공간 <code>ch23_lab</code>을 만들어 씁니다. 다시 실행하면 그 이름 공간만 지우고 처음부터 만듭니다. 01절처럼 매번 같은 값을 내는 우리 노드로 저장된 값을 가르려고, 모델은 부르지 않습니다. 모델 요청은 0번이고, API 키 셀도 없습니다.</p><p>예시 부분은 데이터베이스에 붙어 이름 공간을 만들고, 체크포인터와 01절 그래프를 준비합니다. 체크포인터가 실행할 표 만들기 문장 열 개의 첫 줄도 미리 봅니다.</p>
{{notebook:""" + SLUG + """|example}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>일부러 실패해 보기</h2><p>아래 Before 셀은 표 만들기 <code>setup()</code>을 부르지 않은 채, 01절 첫 실행과 같은 입력으로 그래프를 실행합니다. 이어지는 After 셀은 <code>setup()</code>을 부른 뒤 같은 실행을 합니다. After 뒤에는 표의 구조와 쌓인 줄을 보고, 값 두 가지를 바꿔 봅니다.</p>
{{notebook:""" + SLUG + """|failure}}
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + compare + """
<p>표를 만들기 전에는 첫 실행에서 오류 <code>UndefinedTable</code>을 받았고, 오류 번호는 <code>42P01</code>이었습니다. 오류 글은 표 <code>checkpoints</code>가 없다는 것이었고, 그래프는 결과를 내놓지 못했습니다. 실행이 멈춘 뒤에도 이름 공간 <code>ch23_lab</code>에는 표가 하나도 생기지 않았습니다. 체크포인터를 만들어 그래프에 붙이는 것만으로는 표가 준비되지 않습니다.</p><p>메서드 <code>setup()</code>을 부르자 표 넷이 생겼고, 표 만들기 기록에 판 번호 0부터 9까지 열 줄이 적혔습니다. 그 뒤 Before와 같은 입력으로 첫 실행은 합계 3, 둘째 실행은 합계 7이 되어 01절과 같았습니다. 그래프·체크포인터·입력은 Before와 같고, 달라진 것은 <code>setup()</code> 한 줄입니다.</p><p>스레드 <code>customer-a</code>의 체크포인트 여섯은 표 <code>checkpoints</code>의 여섯 줄이었고, 스레드 <code>customer-b</code>는 세 줄이었습니다. 두 스레드의 줄은 한 표에 있고, 칸 <code>thread_id</code>의 값으로 갈립니다. 메서드 <code>setup()</code>을 한 번 더 불러도 오류 없이 기록은 열 줄 그대로였습니다. 체크포인터의 연결을 닫은 뒤에도 다른 연결로 센 줄 수는 그대로였습니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>모델을 부르지 않아, 노트북 출력은 새 커널로 두 번 실행해도 글자까지 같아야 합니다. """ + RUNS_SENTENCE + """ 두 실행 모두 이름 공간 <code>ch23_lab</code>이 없는 데이터베이스에서 시작했습니다.</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>이 절의 준비물 안내는 Ch 12와 같은 Docker 이미지 <code>pgvector/pgvector:0.8.2-pg17</code>로 만든 컨테이너를 씁니다. 이번 교재 출력은 그 환경에서 만들지 않았습니다. 같은 접속 글로 켠 PostgreSQL 17.11 서버에서 만들었고, 판 번호 줄은 서버에 따라 다르게 나올 수 있습니다.</li><li>서버가 꺼져 있으면 노트북 2절의 연결 셀이 <code>OperationalError</code>로 멈춥니다. 표가 없어서 나는 Before의 <code>UndefinedTable</code>과는 다른 오류입니다. 이 장면은 노트북 밖에서 확인했고, 노트북에서는 실행하지 않았습니다.</li><li>접속 글의 암호는 Ch 12와 같은 수업 전용 값입니다. 다른 환경에 쓰지 않고, 노트북은 접속 글을 출력하지 않습니다.</li><li>노트북은 이름 공간 <code>ch23_lab</code>을 지우고 다시 만듭니다. 이 이름 공간에 다른 표를 두지 않습니다.</li><li>연결을 직접 만들어 넘길 때는 <code>autocommit=True</code>와 <code>row_factory=dict_row</code>를 함께 주라고 설치판 패키지 설명이 적습니다. 둘 가운데 하나를 빠뜨린 장면은 이번에 실행하지 않았습니다.</li><li>공식 문서 예시는 <code>with PostgresSaver.from_conn_string(접속 글) as saver:</code> 모양을 씁니다. 이 절은 Ch 12 02절처럼 연결을 직접 열고 닫았습니다. 설치판 소스에서 이 모양은 같은 두 인자에 <code>prepare_threshold=0</code>을 더해 연결을 열고, <code>with</code> 블록이 끝나면 연결을 닫습니다. 이 모양은 노트북에서 실행하지 않았습니다.</li><li>표 <code>checkpoint_blobs</code>와 <code>checkpoint_writes</code>의 쓰임은 설치판 소스로만 보았고, 줄은 읽지 않았습니다. 체크포인트에 딸린 쓰기는 <a href=\"""" + L_05 + """\">05절</a>에서 다룹니다.</li><li>칸 <code>checkpoint_id</code>처럼 실행마다 달라지는 값은 출력하지 않았습니다.</li><li>여러 프로그램이 같은 표를 함께 쓰는 모습, 연결 묶음(<code>psycopg_pool</code>), 권한 나누기, 백업은 이번에 실행하지 않았습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>표 만들기 전에 실행하자, 표 <code>checkpoints</code>가 없어 오류 <code>UndefinedTable</code>을 받았습니다.</li><li>메서드 <code>setup()</code>은 표 넷을 만들고, 표 만들기 기록에 판 번호 열 줄을 적었습니다.</li><li>표를 만든 뒤에는 01절처럼 합계 7이 되었고, 체크포인트 여섯이 표에 여섯 줄로 쌓였습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_03 + """\">03절</a>에서는 연결과 그래프 객체를 새로 만들어도, 같은 스레드의 대화를 이어 가는지 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 표 만들기 <code>setup()</code>을 부르기 전에 그래프를 실행하자 어떤 오류를 받았고, 그 까닭은 무엇인가요?</p><p class="quiz-a">오류 <code>UndefinedTable</code>을 받았습니다. 그래프가 체크포인트를 찾을 표 <code>checkpoints</code>가 아직 없었기 때문입니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">2. 메서드 <code>setup()</code>을 부른 뒤 이름 공간 <code>ch23_lab</code>에 무엇이 생겼나요?</p><p class="quiz-a">표 넷이 생겼고, 그 가운데 표 만들기 기록에는 판 번호 0부터 9까지 열 줄이 적혔습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">3. 스레드 <code>customer-a</code>의 체크포인트 여섯은 데이터베이스의 어디에 있었나요?</p><p class="quiz-a">표 <code>checkpoints</code>에 칸 <code>thread_id</code>가 <code>customer-a</code>인 줄 여섯으로 있었습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">4. 메서드 <code>setup()</code>을 두 번째로 부르면 어떻게 되었고, 그 까닭은 무엇인가요?</p><p class="quiz-a">오류 없이 표 만들기 기록이 열 줄 그대로였습니다. 설치판 소스에서 <code>setup()</code>은 기록 표를 만드는 0번 문장을 먼저 실행하는데, 표가 이미 있어 아무 일도 하지 않았습니다. 그 뒤 마지막 판 번호 다음 문장부터 실행하는데, 남은 문장이 없었습니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langgraph/checkpointers">LangGraph Checkpointers</a></div>확인 2026-09-25 · PostgreSQL 체크포인터 <code>PostgresSaver</code>와, 만든 뒤 <code>setup()</code>을 부르는 예를 적습니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langgraph/persistence">LangGraph Persistence</a></div>확인 2026-09-25 · 프로그램 밖에 남기는 체크포인터로 <code>PostgresSaver</code>를 적습니다.</li><li><div>langgraph-checkpoint-postgres 3.0.5 패키지 설명</div>처음 쓸 때 <code>setup()</code>을 부르라고 적습니다. 연결을 직접 만들 때 줄 두 인자도 적습니다.</li><li>같은 판 소스 <code>langgraph/checkpoint/postgres/__init__.py</code> 54~75행은 <code>from_conn_string</code>, 77~102행은 <code>setup()</code>입니다.</li><li>같은 파일 301~308행은 수·글이 아닌 칸 값을 표 <code>checkpoint_blobs</code>에 따로 두는 자리, 336~351행은 쓰기를 담는 자리입니다.</li><li>같은 판 <code>langgraph/checkpoint/postgres/base.py</code> 37~85행은 표 만들기 문장 목록 <code>MIGRATIONS</code>입니다.</li><li><div>langgraph-checkpoint-sqlite 3.0.3 소스</div><code>langgraph/checkpoint/sqlite/__init__.py</code> 122~128행은 SQLite 체크포인터의 <code>setup()</code> 설명입니다.</li><li>langgraph 1.2.11 소스 <code>langgraph/pregel/_loop.py</code> 1651~1654행 — 실행을 시작할 때 마지막 체크포인트를 찾는 자리입니다.</li><li>psycopg 3.3.3 소스 <code>psycopg/connection.py</code> 155~176행 — <code>with</code> 블록이 끝날 때 연결을 닫는 자리입니다.</li><li>Ch 12 02절에서 psycopg와 자리표시자를 보았습니다. Ch 4 03절에서 SQL 조회를, 01절에서 체크포인터와 스레드를 보았습니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    # 01절 셀과 글자까지 같은 셀
    assert STATE == author_01.STATE and NODE == author_01.NODE
    assert CONFIG_A == author_01.CONFIG_A and CONFIG_B == author_01.CONFIG_B and FILES == author_01.FILES
    # 임시 폴더 셀은 01절 셀에서 앞머리 ch23-01- → ch23-02- 만 다르다(세 곳)
    assert FOLDER != author_01.FOLDER and FOLDER.replace("ch23-02-", "ch23-01-") == author_01.FOLDER
    assert author_01.FOLDER.count("ch23-01-") == 3
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "02", SLUG, "paired", cells())
        print("wrote", path)
