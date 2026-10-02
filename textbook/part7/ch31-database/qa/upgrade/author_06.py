"""Ch 31 06절(챕터 끝 실습 절) 생성기 (QUALITY-UPGRADE.md §7-2·§2·§2-7·§3·§4·§5-3·§6 experiment).

사용:
  python3 -B author_06.py            → 노트북 + _src 본문을 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_06.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
이후 run_section.sh 가 pre_exec.sh(PostgreSQL 켜기) → 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
새로 만든 절이라 qa/upgrade/before/ 에 원본이 없다. **experiment 형식**(chapter.json), lesson_part 없음.
설계와 노트북 밖 확인 5번은 qa/upgrade/06-design.md.

## 결정 1 — 붙인 앞 절 기능 셋 (handoff 「§05 → 실습 절」 2번 표 · 준비 노트 §14 주제 예)

상담실 하루의 상담 시간이 정해져 있고, 문의 셋(01절 표 requests와 같은 번호·이름 — 1 환불 · 2 배송 · 3 결제)이
차례로 예약을 신청하는 그래프 하나:
02 한 묶음 작업(노드 book_inquiry의 begin 블록 하나 — 예약 줄 넣기 + 상담 시간 빼기, CHECK 위반 23514를 받으면 booked 0)
04 작은 연결 풀(pool_size=1·max_overflow=0·pool_timeout=0.2 — 오류로 끝난 블록도 반납해야 다음 문의가 연결을 받음)
05 체크포인터(같은 이름 공간 ch31_practice에 SET search_path·setup() · 스레드 = 문의 이름 · get_state · 새 연결로 다시 컴파일해 읽기).
셋 모두 실행 1·2 흐름에서 쓰인다. 받쳐 주는 것: 01 이름 공간 지우고 만들기·to_regnamespace·checkedin · 03 동기 엔진·설정 셀·array_agg.
뺀 것과 까닭은 b3 한 단락·06-design.md §3: 01 gather · 03 Alembic · 05 pgvector 색인·백업·복원 · 04 대기 제한 바꾸기.

## 결정 2 — 실행 2는 처음 상담 시간 하나만 (first_start = 50 → second_start = 30)

02 After(한 블록 → 오류 뒤 취소)의 모양이 실행 2 둘째 문의에서 다시 나오므로 b2 「새로 볼 것」은 실행이 보인 만큼만(Ch 26 05 검토 B-7):
셋 가운데 한 문의만 취소되고 흐름이 이어짐 · 풀 크기 1인데 다음 문의가 연결을 받음·빌려 간 연결 0 · 취소된 문의의 상태도 저장(booked 0)·
체크포인트 줄 수 두 실행 모두 9 · 새 연결로도 같은 상태.

## 결정 3 — 모델 요청 0 (챕터 결정 M0 · 05 인계 5 · Ch 23·24·30 10 선례) · 동기만(그래프 invoke + PostgresSaver가 psycopg 동기 연결)

결론은 줄 수·예약 번호·남은 분·풀 상태·get_state 값(매번 같은 값 — 노트북 밖 5/5 /tmp/ch31-06/exp/e2_cells.py md5 7cdaba069fc4d0d4). 키 셀 없음.

## 결정 4 — 도구 파일 만들지 않음 (챕터 공통 8 S1): 앞 절 함수를 다시 쓰지 않음 — 이 절 함수 넷은 흐름을 잇는 새 함수.

## 쓰지 않은 것
f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`range`·`str`·`bool`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`.items`·`+=`·기본값 매개변수·변수·반환 힌트(상태 형식 칸 int 말고)·대입 풀기(for 포함)·
별표 풀기·`while`·`raise`·세미콜론·`isinstance`·클래스(TypedDict 하나 말고)·데코레이터·`await`·`async`·`asyncio`·가짜 모델·파일 쓰기.
호출 깊이 2 이하. 01~05 노트북에 없던 내장 이름·속성·키워드 인자·노드 종류·가져온 이름 0(/tmp/ch31-06/tools/astdiff.py).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part7/ch31-database/notebooks"
FIGS = ROOT / "textbook/part7/ch31-database/figures"
SLUG = "06-DB와-상태-영속화-실습"
TITLE_TEXT = "DB와 상태 영속화 실습: 상담 예약 그래프에서 처음 상담 시간 하나만 바꾸기"
SRC = ROOT / "textbook/part7/ch31-database/_src" / (SLUG + ".html")
AUTHOR03 = ROOT / "textbook/part7/ch31-database/qa/upgrade/author_03.py"
NB03 = LAB / "03-Alembic-적용과-롤백.ipynb"
RUNS_SENTENCE = os.environ.get("AUTHOR06_RUNS_SENTENCE", "새 커널로 두 번 실행해 견주자, 코드 셀 스물셋의 출력이 셀마다 모두 같았습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 노트북 밖에서 같은 흐름을 다섯 번 실행했을 때도 출력이 모두 같았습니다.")

# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["sqlalchemy==2.0.43", "psycopg[binary]==3.3.3", "langgraph==1.2.11", "langgraph-checkpoint-postgres==3.0.5"])

IMPORTS = r'''# psycopg·LangGraph·SQLAlchemy에서 이 실습에 쓸 이름을 가져옵니다(모두 03·05절에서 가져온 이름입니다)
import psycopg
from psycopg.rows import dict_row
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

print("가져온 이름:", "psycopg", "dict_row", "TypedDict", "StateGraph", "PostgresSaver", "create_engine", "text", "IntegrityError")'''

SETTINGS = r'''# 데이터베이스 접속 글을 정합니다(비밀번호 postgres는 이 실습에서만 쓰는 연습용 값입니다)
database_url = "postgresql+psycopg://postgres:postgres@127.0.0.1:55431/ch31_lab"
# 비밀번호가 찍히지 않게, 글을 @에서 나눠 앞의 드라이버 부분과 뒤의 서버 부분만 출력합니다
url_parts = database_url.split("@")
print("드라이버 부분:", database_url.split("://")[0])
print("서버 주소와 데이터베이스:", url_parts[1])'''

SAVER_URL = r'''# 체크포인터가 psycopg에 바로 줄 접속 글을 만듭니다(드라이버 표시 +psycopg만 뺍니다)
saver_url = database_url.replace("postgresql+psycopg://", "postgresql://")
print("체크포인터 접속 글의 드라이버 부분:", saver_url.split("://")[0])
# @ 뒤의 서버 부분이 설정 셀의 글과 같은지 참·거짓으로 봅니다
print("같은 서버와 데이터베이스인가:", saver_url.split("@")[1] == url_parts[1])'''

ENGINE = r'''# 동기 엔진을 만듭니다(04절과 같은 풀 값 — 풀에 둘 연결 수 1, 더 만들 연결 수 0, 대기 제한 0.2초)
engine = create_engine(database_url, pool_size=1, max_overflow=0, pool_timeout=0.2)
print("풀에 둘 연결 수:", engine.pool.size())
print("대기 제한(초):", engine.pool.timeout())
print("빌려 간 연결 수:", engine.pool.checkedout())'''

TABLE_SQL = r'''# 하루의 두 표를 만드는 SQL 글과, 처음 상담 시간을 넣는 SQL 글 객체를 정합니다
# CHECK (minutes >= 0)은 남은 상담 시간이 0 이상이어야 한다는 조건입니다(02절 잔액 칸과 같은 모양)
schedule_sql = "CREATE TABLE ch31_practice.schedule (minutes int CHECK (minutes >= 0))"
bookings_sql = "CREATE TABLE ch31_practice.bookings (no int PRIMARY KEY)"
start_sql = text("INSERT INTO ch31_practice.schedule VALUES (:minutes)")
print("상담 시간 표를 만드는 SQL 글:")
print(schedule_sql)
print("예약 표를 만드는 SQL 글:")
print(bookings_sql)'''

WORK_SQL = r'''# 문의 하나가 한 묶음으로 보낼 SQL 글 객체 둘을 정합니다(예약 줄 넣기와 상담 시간 빼기)
book_sql = text("INSERT INTO ch31_practice.bookings VALUES (:no)")
take_sql = text("UPDATE ch31_practice.schedule SET minutes = minutes - :minutes")
print("예약 줄을 넣는 SQL 글:", book_sql)
print("상담 시간을 빼는 SQL 글:", take_sql)'''

INQUIRIES = r'''# 문의 셋을 정합니다(번호·이름은 01절 표와 같고, 필요한 상담 시간은 실행 전에 이 절에서 정한 값입니다)
inquiries = [
    {"name": "환불", "no": 1, "minutes": 10},
    {"name": "배송", "no": 2, "minutes": 30},
    {"name": "결제", "no": 3, "minutes": 10},
]
print("번호 | 문의 | 필요한 상담 시간(분) — 실행 전에 정한 값")
for inquiry in inquiries:
    print(inquiry["no"], "|", inquiry["name"], "|", inquiry["minutes"])'''

SAVER = r'''# 체크포인터가 쓸 연결을 따로 열고, 표를 찾고 만들 이름 공간을 ch31_practice로 정합니다(05절 4절 모양)
saver_conn = psycopg.connect(saver_url, autocommit=True, row_factory=dict_row)
saver_conn.cursor().execute("SET search_path TO ch31_practice")
checkpointer = PostgresSaver(saver_conn)
# 표 만들기 setup()은 4절 함수 open_day가 하루를 열 때마다 부릅니다
print("체크포인터의 종류:", type(checkpointer).__name__)'''

STATE = r'''# 문의 번호·필요한 상담 시간·남긴 예약 줄 수, 세 칸을 둔 상태 형식을 만듭니다
class BookingState(TypedDict):
    no: int
    minutes: int
    booked: int'''

NODE = r'''# 노드 함수: 예약 줄 넣기와 상담 시간 빼기를 begin 블록 하나에 넣고, 남긴 예약 줄 수를 냅니다
def book_inquiry(state):
    # 02절 한 묶음 작업: 빼기가 CHECK를 어기면 블록이 확정하지 않고 넣기까지 취소합니다
    try:
        with engine.begin() as conn:
            conn.execute(book_sql, {"no": state["no"]})
            conn.execute(take_sql, {"minutes": state["minutes"]})
    except IntegrityError as error:
        print("문의", state["no"], "받은 오류:", type(error).__name__, error.orig.sqlstate)
        return {"booked": 0}
    return {"booked": 1}'''

GRAPH = r'''# 노드 하나·엣지 둘을 설계 객체에 적고, 체크포인터와 함께 컴파일합니다(05절 4절과 같은 차례)
builder = StateGraph(BookingState)
builder.add_node("book", book_inquiry)
builder.add_edge(START, "book")
builder.add_edge("book", END)
graph = builder.compile(checkpointer=checkpointer)
print("붙은 체크포인터의 종류:", type(graph.checkpointer).__name__)'''

OPEN_DAY = r'''# 하루를 새로 엽니다: 이름 공간을 지우고 다시 만들어 두 표와 처음 상담 시간을 넣고, 체크포인터 표도 만듭니다
def open_day(start_minutes):
    # 01절처럼 이름 공간을 안의 표까지 지우고 다시 만듭니다(다섯 SQL 글이 한 묶음으로 확정됩니다)
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS ch31_practice CASCADE"))
        conn.execute(text("CREATE SCHEMA ch31_practice"))
        conn.execute(text(schedule_sql))
        conn.execute(text(bookings_sql))
        conn.execute(start_sql, {"minutes": start_minutes})
    # 05절 표 만들기: 지운 체크포인터 표 넷을 새 이름 공간에 다시 만듭니다
    checkpointer.setup()'''

READ_TABLES = r'''# 기록 장치: 남은 상담 시간·예약된 문의 번호·체크포인트 줄 수를 읽어, 딕셔너리로 내놓습니다
def read_tables():
    with engine.connect() as conn:
        minutes = conn.execute(text("SELECT minutes FROM ch31_practice.schedule")).scalar_one()
        # 03절처럼 array_agg(… ORDER BY …)로 번호 차례의 목록 하나를 받습니다
        booked = conn.execute(text("SELECT array_agg(no ORDER BY no) FROM ch31_practice.bookings")).scalar_one()
        saved = conn.execute(text("SELECT count(*) FROM ch31_practice.checkpoints")).scalar_one()
    return {"남은 상담 시간(분)": minutes, "예약된 문의 번호": booked, "체크포인트 줄 수": saved}'''

SEND = r'''# 문의 하나를 제 스레드(문의 이름)로 그래프에 보내고, 노드가 남긴 예약 줄 수를 내놓습니다
def send_inquiry(inquiry):
    inquiry_input = {"no": inquiry["no"], "minutes": inquiry["minutes"]}
    # 05절처럼 설정 딕셔너리의 thread_id로 스레드를 정합니다
    thread_config = {"configurable": {"thread_id": inquiry["name"]}}
    final_state = graph.invoke(inquiry_input, thread_config)
    return final_state["booked"]'''

RUN1 = r'''# 실행 1: 처음 상담 시간 50분으로 하루를 열고, 문의 셋을 차례로 보냅니다
first_start = 50
open_day(first_start)
first_booked = []
for inquiry in inquiries:
    first_booked.append(send_inquiry(inquiry))
print("처음 상담 시간(분):", first_start)
print("문의마다 남긴 예약 줄 수:", first_booked)'''

CHECK1 = r'''# 실행 1이 끝난 뒤, 표에서 읽은 값·빌려 간 연결 수와 배송 문의의 저장된 상태를 봅니다
first_tables = read_tables()
first_out = engine.pool.checkedout()
first_state = graph.get_state({"configurable": {"thread_id": "배송"}}).values
print("표에서 읽은 값:", first_tables)
print("빌려 간 연결 수:", first_out)
print("배송 문의의 저장된 상태:", first_state)'''

RUN2 = r'''# 실행 2: 바꾼 값은 처음 상담 시간 하나입니다(50분 → 30분, 문의 셋과 차례는 같습니다)
second_start = 30
open_day(second_start)
second_booked = []
for inquiry in inquiries:
    second_booked.append(send_inquiry(inquiry))
print("처음 상담 시간(분):", second_start)
print("문의마다 남긴 예약 줄 수:", second_booked)'''

CHECK2 = r'''# 실행 2가 끝난 뒤, 표에서 읽은 값·빌려 간 연결 수와 배송 문의의 저장된 상태를 봅니다
second_tables = read_tables()
second_out = engine.pool.checkedout()
second_state = graph.get_state({"configurable": {"thread_id": "배송"}}).values
print("표에서 읽은 값:", second_tables)
print("빌려 간 연결 수:", second_out)
print("배송 문의의 저장된 상태:", second_state)'''

POOL = r'''# 두 실행이 끝난 뒤 엔진의 풀 상태를 한 줄 글로 봅니다(04절에서 쓴 메서드 status)
print("풀 상태:")
print(engine.pool.status())'''

TABLE = r'''# 두 실행을 한 줄씩 견줍니다(처음 상담 시간·남긴 예약 줄 수·표에서 읽은 값·빌려 간 연결 수)
print("실행 | 처음 상담 시간(분) | 남긴 예약 줄 수 | 표에서 읽은 값 | 빌려 간 연결 수")
print("실행 1 |", first_start, "|", first_booked, "|", first_tables, "|", first_out)
print("실행 2 |", second_start, "|", second_booked, "|", second_tables, "|", second_out)'''

RECONNECT = r'''# 체크포인터 연결을 닫고, 새 연결로 설계 객체를 다시 컴파일해 배송 문의의 상태를 읽습니다(05절 6절 함수 모양)
saver_conn.close()
check_conn = psycopg.connect(saver_url, autocommit=True, row_factory=dict_row)
check_conn.cursor().execute("SET search_path TO ch31_practice")
check_graph = builder.compile(checkpointer=PostgresSaver(check_conn))
check_values = check_graph.get_state({"configurable": {"thread_id": "배송"}}).values
print("새 연결로 읽은 배송 문의의 상태:", check_values)
check_conn.close()'''

CLEANUP = r'''# 끝 정리: 이름 공간 ch31_practice를 체크포인터 표까지 지우고, 남았는지 물은 뒤 풀을 비웁니다
with engine.begin() as conn:
    conn.execute(text("DROP SCHEMA ch31_practice CASCADE"))
    result = conn.execute(text("SELECT to_regnamespace('ch31_practice')"))
    left_namespace = result.scalar_one()
engine.dispose()
print("남은 이름 공간:", left_namespace)
print("풀에 쉬고 있는 연결 수:", engine.pool.checkedin())'''

# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/06-figures.md)
FIG1 = "06-1-세-절의-기능을-이은-조립도"
FIG1_ALT = "위에서 아래로 읽는 조립도입니다. 초록 상자 문의 셋 환불 10분 배송 30분 결제 10분에서 파란 상자 send_inquiry graph.invoke 스레드는 문의 이름으로 화살표가 갑니다. 여기서 두 쪽으로 이어집니다. 왼쪽은 파란 상자 노드 book_inquiry begin 블록 하나 02절에서, 연결 빌림과 반납 화살표로 회색 상자 엔진의 연결 풀 풀 크기 1 대기 제한 0.2초 04절로 갑니다. 오른쪽은 단계마다 상태 저장 화살표로 회색 상자 체크포인터 PostgresSaver 따로 연 연결 05절로 갑니다. 두 회색 상자에서 맨 아래 회색 상자 이름 공간 ch31_practice schedule bookings 체크포인터 표 넷으로 화살표가 모이는 그림"
FIG1_CAP = "문의는 노드의 한 묶음 작업으로 표에 적히고, 그 상태는 체크포인터가 따로 연 연결로 적힙니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 셀에 적은 문의 셋이고, 파란 상자 둘은 우리가 만든 함수와 노드입니다.
회색 상자 셋은 라이브러리의 연결 풀과 체크포인터, 그리고 PostgreSQL의 이름 공간입니다.
상자에 적은 절 번호는 그 부품을 배운 절입니다.
왼쪽 노드 쪽과 오른쪽 체크포인터 쪽은 서로 다른 연결로 같은 이름 공간에 적습니다."""

FIG2 = "06-2-실행-1의-실제-차례"
FIG2_ALT = "위에서 아래로 일곱 상자가 한 줄로 이어진 흐름도입니다. 초록 상자 처음 상담 시간 50분에서 파란 상자 open_day 이름 공간 새로 setup으로 갑니다. 이어서 파란 상자 셋이 차례로 이어집니다. book_inquiry 문의 1 환불 10분, book_inquiry 문의 2 배송 30분, book_inquiry 문의 3 결제 10분입니다. 그 아래 노란 상자 남긴 예약 줄 수 1 1 1에서, 마지막 노란 상자 남은 상담 시간 0분 예약 번호 1 2 3 체크포인트 줄 아홉 빌려 간 연결 없음 배송 상태 booked 1로 이어지는 그림"
FIG2_CAP = "실행 1은 하루를 연 뒤 문의 셋을 차례로 예약했고, 남은 상담 시간 0분과 빌려 간 연결 없음으로 끝났습니다."
FIG2_READ = """위에서 아래로 읽습니다.
초록 상자는 실행 1 셀에 적은 처음 상담 시간이고, 파란 상자 넷은 그 셀이 차례로 부른 함수와 노드입니다.
노란 상자 둘은 노트북 5절 두 셀의 출력으로 확인한 값입니다.
노드는 문의마다 한 번씩, 적힌 차례대로 실행되었습니다."""

FIG3 = "06-3-처음-상담-시간만-바꾼-두-실행"
FIG3_ALT = "위에 회색 상자 하나가 있고 아래에 칸 둘이 나란히 놓인 그림입니다. 회색 상자 두 실행 같음 문의 셋 10 30 10분 같은 그래프 풀 크기 1에서 두 칸으로 화살표가 갑니다. 왼쪽 칸 실행 1에는 초록 상자 처음 상담 시간 50분 아래 노란 상자 남긴 예약 줄 수 1 1 1 남은 0분 예약 번호 1 2 3 배송 상태 booked 1이 있습니다. 오른쪽 칸 실행 2 값 하나만 바꿈에는 파란 상자 처음 상담 시간 30분 아래 노란 상자 문의 2 받은 오류 IntegrityError 23514, 그 아래 노란 상자 남긴 예약 줄 수 1 0 1 남은 10분 예약 번호 1 3 배송 상태 booked 0이 있습니다. 두 칸에서 맨 아래 노란 상자 두 실행 모두 체크포인트 줄 아홉 빌려 간 연결 없음으로 화살표가 모이는 그림"
FIG3_CAP = "처음 상담 시간 하나만 줄이자 배송 문의만 예약되지 않았고, 체크포인트 줄 수와 빌려 간 연결은 두 실행이 같았습니다."
FIG3_READ = """맨 위 회색 상자는 두 실행에서 같았던 조건입니다.
왼쪽 칸이 실행 1, 오른쪽 칸이 실행 2이고, 칸마다 위 상자가 셀에 적은 처음 상담 시간입니다.
실행 1 칸의 것은 초록이고, 실행 2 칸의 것은 바꾼 값이라 파랑입니다.
노란 상자는 노트북 5·6절 출력이고, 받은 오류 상자는 실행 2 칸에만 있습니다.
맨 아래 상자는 두 칸의 출력에서 모두 확인한 값입니다."""

ILLU = "06-4-세-판을-한-틀에-끼운-교환대"
ILLU_ALT = "흰 바탕에 가로로 긴 검은 금속 틀 하나가 화면을 가로지릅니다. 틀 안에 청록·테라코타·옅은 노랑 판 셋이 틈을 두고 나란히 끼워져 있습니다. 왼쪽 청록 판에는 둥근 꽂는 자리 하나가 있고, 흰 선 하나가 꽂혀 틀 아래로 곧게 늘어집니다. 가운데 테라코타 판에는 꽂는 자리 여섯이 두 줄 세 칸으로 있습니다. 왼쪽 칸과 오른쪽 칸은 위아래 자리가 흰 선 하나씩으로 이어져 있고, 가운데 칸의 두 자리는 비어 있습니다. 오른쪽 옅은 노랑 판에는 위에 경첩이 달린 회색 둥근 덮개 셋이 한 줄로 있습니다. 사람·손·글자·숫자·화살표·불은 없는 그림"
ILLU_CAP = "세 판을 한 틀에 끼운 교환대에서 가운데 판의 한 칸만 비었고, 오른쪽 판에는 덮개 셋이 모두 있습니다."
ILLU_READ = "검은 틀 하나에 색이 다른 판 셋이 끼워져 있습니다. 왼쪽 판에는 꽂는 자리가 하나뿐이고, 흰 선 하나가 꽂혀 있습니다. 가운데 판의 세 칸 가운데 왼쪽과 오른쪽 칸은 위아래 자리가 선으로 이어졌고, 가운데 칸은 두 자리가 모두 비었습니다. 오른쪽 판에는 둥근 덮개 셋이 한 줄로 있습니다. 가운데 칸이 비어 있어도, 덮개는 셋입니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 02절 한 묶음 작업, 04절 작은 연결 풀, 05절 체크포인터를 상담 예약 그래프 하나로 잇습니다.
2. 처음 상담 시간 50분으로 문의 셋을 보내고, 표와 체크포인터 표, 연결 풀을 확인합니다.
3. 처음 상담 시간 하나만 30분으로 바꿔 다시 보내고, 두 실행을 견줍니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
예상 비용도 0달러입니다.

01절과 같은 PostgreSQL 서버가 `127.0.0.1:55431`에서 켜져 있어야 합니다.
서버는 01절 준비물의 Docker 컨테이너 `kdt-ch31-postgres`입니다.
꺼져 있으면 터미널에서 `docker start kdt-ch31-postgres`로 다시 켭니다.
컨테이너를 아직 만들지 않았다면, 01절 노트북 맨 위 준비물의 `docker run` 명령을 먼저 실행합니다.

노트북은 데이터베이스 `ch31_lab` 안에 이름 공간 `ch31_practice`를 만들어 쓰고, 끝에서 지웁니다.
작업 폴더와 운영체제 임시 폴더에는 파일을 쓰지 않습니다.
걸린 시간은 재지 않습니다.

**기준 버전** — 첫 셀에서 패키지 넷을 설치합니다.
버전은 sqlalchemy 2.0.43과 psycopg 3.3.3입니다.
그래프 패키지 langgraph는 1.2.11입니다.
체크포인터 패키지 langgraph-checkpoint-postgres는 3.0.5입니다.
넷 모두 실습 폴더 잠금과 같습니다.

교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다.
그 서버는 Docker 컨테이너가 아니라, 같은 접속 글로 켠 서버입니다.
Docker 이미지로 켜면 서버 버전 번호의 끝자리가 다를 수 있습니다.
Windows·macOS에서는 실행하지 않았습니다.

**실습 범위** — 이 절은 이 챕터 끝의 실습 절입니다.
강사와 함께 첫 셀부터 차례로 실행하고, 따로 내는 과제는 없습니다.
실습 시간 30분 안팎에 맞춘 분량입니다.

실습 폴더 `labs/part7/ch31-database`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이 절은 이 챕터의 실습 절입니다.
01~05절에서 배운 것 가운데 셋을 상담 예약 흐름 하나로 이어 실행합니다.
02절의 한 묶음 작업, 04절의 작은 연결 풀과 반납, 05절의 체크포인터입니다.
새 문법과 새 라이브러리 함수는 넣지 않고, 흐름을 잇는 함수만 이 절에서 만듭니다.

절 제목의 DB는 데이터베이스(database)입니다.
제목의 상태 영속화는 Ch 23에서 배운 상태 저장(Persistence)과 같은 뜻입니다.

01·02·04절은 await를 쓰는 비동기 엔진을 썼습니다.
이 절은 03·05절처럼 await 없이 쓰는 동기 드라이버 psycopg만 씁니다.
그래프를 `invoke`로 부르고, 체크포인터 `PostgresSaver`가 psycopg의 동기 연결을 쓰기 때문입니다.
그래서 노드 안의 한 묶음 작업도 03절처럼 동기 엔진으로 적습니다.
블록 `engine.begin()`과 연결 풀의 뜻은 02·04절과 같습니다.

첫 셀은 이 절이 쓰는 패키지 넷을 설치하고, 설치된 버전 번호를 출력합니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `sqlalchemy: 2.0.43`, `psycopg: 3.3.3`, `langgraph: 1.2.11`, `langgraph-checkpoint-postgres: 3.0.5`가 보입니다.
넷 모두 실습 폴더 잠금과 같고, 03·05절에서 쓴 버전과도 같습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
연결 모듈 psycopg와 `dict_row`, 상태 형식 `TypedDict`, 그래프 이름과 `PostgresSaver`는 05절에서 가져온 이름입니다.
동기 엔진 `create_engine`과 SQL 글 `text`, 오류 이름 `IntegrityError`는 03절에서 가져온 이름입니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `가져온 이름:` 뒤에 이름 여덟이 보입니다.
이 노트북에는 API 키를 확인하는 셀이 없습니다.
모델을 부르지 않기 때문입니다.

## 2. 오늘의 상황과 재료

상담실 하루에는 상담할 수 있는 시간이 정해져 있습니다.
문의 셋이 차례로 상담 예약을 신청하고, 예약 하나는 그 문의에 필요한 시간만큼 하루의 상담 시간을 씁니다.
남은 시간보다 긴 문의는 예약되지 않아야 합니다.
문의 셋은 01절 표 `requests`의 문의와 번호·이름이 같습니다.

다음 셀은 03절 노트북 2절의 설정 셀과 글자까지 같은 셀로, 연습용 접속 글을 정합니다.
드라이버 부분 `postgresql+psycopg`는 SQLAlchemy가 psycopg로 서버에 붙게 하는 표시입니다."""),
        code(SETTINGS),
        md("""**결과 읽기** — 출력 줄 `드라이버 부분: postgresql+psycopg`가 보입니다.
라벨 `서버 주소와 데이터베이스:` 뒤의 `127.0.0.1:55431/ch31_lab`은 01절과 같은 서버와 데이터베이스입니다.
비밀번호가 든 가운데 부분은 출력하지 않았습니다.

다음 셀은 체크포인터가 쓸 접속 글을 만듭니다.
05절처럼 psycopg에 바로 주는 글이라, 드라이버 표시 `+psycopg`가 붙지 않습니다.
메서드 `replace`로 그 표시만 빼고, @ 뒤의 서버 부분이 같은지 참·거짓으로 봅니다."""),
        code(SAVER_URL),
        md("""**결과 읽기** — 출력 줄 `체크포인터 접속 글의 드라이버 부분: postgresql`과 `같은 서버와 데이터베이스인가: True`가 보입니다.
두 글은 드라이버 표시만 다르고, 같은 서버의 같은 데이터베이스를 가리킵니다.

다음 셀은 동기 엔진을 만듭니다.
풀 인자는 04절과 같은 값으로, 풀에 둘 연결 수 1, 더 만들 연결 수 0, 대기 제한 0.2초입니다.
그래서 빌려 간 연결이 반납되지 않으면, 다음 문의는 0.2초를 기다린 뒤 연결을 받지 못합니다.
04절에서는 같은 풀 값의 비동기 엔진으로 그 오류를 봤습니다."""),
        code(ENGINE),
        md("""**결과 읽기** — 출력 줄 `풀에 둘 연결 수: 1`과 `대기 제한(초): 0.2`가 보입니다.
엔진을 만들기만 해서, 출력 줄 `빌려 간 연결 수: 0`입니다.

다음 셀은 하루의 두 표를 만드는 SQL 글을 정합니다.
상담 시간 표 `schedule`은 남은 상담 시간(분) 한 칸을 둔 표이고, 줄은 하나입니다.
그 칸의 `CHECK (minutes >= 0)`은 02절 잔액 칸처럼, 남은 시간이 0보다 작아지는 줄을 서버가 막는 조건입니다.
예약 표 `bookings`는 예약된 문의 번호를 한 줄씩 담습니다.
처음 상담 시간을 넣는 글은 값 자리 `:minutes`를 둔 SQL 글 객체로 만듭니다."""),
        code(TABLE_SQL),
        md("""**결과 읽기** — 라벨 줄 아래에 두 표를 만드는 SQL 글이 보입니다.
표 이름 앞의 `ch31_practice.`는 이 절의 이름 공간입니다.
두 표는 4절 함수 `open_day`가 하루를 열 때마다 만듭니다.

다음 셀은 문의 하나가 보낼 SQL 글 둘을 정합니다.
하나는 예약 표에 문의 번호 한 줄을 넣고, 하나는 상담 시간 표에서 그 문의의 분을 뺍니다.
두 글은 3절 노드에서 begin 블록 하나에 함께 들어갑니다.
02절에서 본 것처럼, 뒤의 빼기가 막히면 앞의 넣기도 남지 않아야 합니다."""),
        code(WORK_SQL),
        md("""**결과 읽기** — 출력 줄 `예약 줄을 넣는 SQL 글:`과 `상담 시간을 빼는 SQL 글:` 뒤에 두 글이 보입니다.
빼는 글에는 WHERE가 없습니다.
상담 시간 표의 줄이 하나뿐이라, 그 줄의 값이 바뀝니다.

다음 셀은 문의 셋을 정합니다.
번호와 이름은 01절 표와 같고, 필요한 상담 시간 10·30·10분은 실행 전에 이 절에서 정한 값입니다.
셋을 더하면 50분입니다.
이름은 뒤에서 그래프의 스레드 이름으로 씁니다."""),
        code(INQUIRIES),
        md("""**결과 읽기** — 라벨 줄 아래에 `2 | 배송 | 30`처럼 문의마다 한 줄이 보입니다.
가장 긴 문의는 30분짜리 배송입니다.

## 3. 체크포인터와 그래프

다음 셀은 05절 4절처럼 체크포인터가 쓸 연결을 따로 엽니다.
인자 `autocommit=True`는 SQL 글마다 바로 확정하는 설정이고, `row_factory=dict_row`는 줄을 딕셔너리로 받는 설정입니다.
문장 `SET search_path TO ch31_practice`는 체크포인터 표를 이 절의 이름 공간에 두게 합니다.
이름 공간은 아직 없어도 되고, 표 만들기 `setup()`은 4절에서 하루를 열 때 부릅니다."""),
        code(SAVER),
        md("""**결과 읽기** — 출력 줄 `체크포인터의 종류: PostgresSaver`가 보입니다.
이 연결은 엔진의 풀과 따로 연 연결입니다.
그래서 엔진의 풀은 이 연결을 빌려 주지도, 세지도 않습니다.

다음 세 셀은 모델을 쓰지 않는 그래프를 만듭니다.
상태 형식의 칸은 셋이고, 모두 정수입니다.
칸 `no`는 문의 번호, `minutes`는 필요한 상담 시간, `booked`는 노드가 남긴 예약 줄 수입니다.
05절처럼 상태 형식 `TypedDict`는 칸만 적은 클래스입니다."""),
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 `booked`는 노드가 채웁니다.

다음 셀의 노드 함수 `book_inquiry`는 문의 하나의 예약을 한 묶음 작업으로 처리합니다.
블록 `engine.begin()` 하나에 예약 줄 넣기와 상담 시간 빼기를 함께 넣습니다.
빼기가 CHECK를 어기면, 블록은 확정하지 않고 넣기까지 취소합니다.
함수는 그 오류 `IntegrityError`를 받아 문의 번호와 오류 코드를 출력하고, 남긴 예약 줄 수 0을 냅니다.
오류가 없으면 1을 냅니다."""),
        code(NODE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
오류를 받아 값을 내는 모양은 03절 함수 `try_upgrade`와 같습니다.
노드가 오류를 받으므로, 그래프 실행은 오류로 끝나지 않고 다음 문의로 이어 갈 수 있습니다.

다음 셀은 05절처럼 설계 객체에 노드 하나와 엣지 둘을 적고, 체크포인터와 함께 컴파일합니다."""),
        code(GRAPH),
        md("""**결과 읽기** — 출력 줄 `붙은 체크포인터의 종류: PostgresSaver`가 보입니다.
이 그래프는 문의 하나를 받을 때마다 상태를 체크포인터 표에 적습니다.

## 4. 조립과 기록 장치

다음 셀의 함수 `open_day`는 하루를 새로 엽니다.
01절처럼 이름 공간 `ch31_practice`를 안의 표까지 지우고 다시 만든 뒤, 두 표를 만들고 처음 상담 시간 한 줄을 넣습니다.
이 다섯 SQL 글도 begin 블록 하나에서 한 묶음으로 확정됩니다.
이름 공간을 지우면 체크포인터 표도 지워지므로, 블록 뒤에 표 만들기 `setup()`을 다시 부릅니다.
그래서 실행 1과 실행 2는 서로의 표를 보지 않고, 같은 빈 자리에서 시작합니다."""),
        code(OPEN_DAY),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
인자 `start_minutes`가 실행 1과 실행 2에서 달라지는 값입니다.

다음 셀의 함수 `read_tables`는 결과를 볼 기록 장치입니다.
남은 상담 시간과 예약된 문의 번호, 체크포인터 표 `checkpoints`의 줄 수를 읽어 딕셔너리로 내놓습니다.
문의 번호는 03절처럼 `array_agg`에 `ORDER BY`를 붙여, 번호 차례의 목록 하나로 받습니다."""),
        code(READ_TABLES),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
연결은 03절처럼 `with engine.connect()` 블록으로 빌리고, 블록이 끝나면 풀에 반납합니다.

다음 셀의 함수 `send_inquiry`는 문의 하나를 그래프에 보냅니다.
스레드 이름은 문의 이름이고, 05절처럼 설정 딕셔너리의 `thread_id`에 넣습니다.
그래프 실행이 끝나면, 마지막 상태에서 노드가 남긴 예약 줄 수를 꺼내 내놓습니다."""),
        code(SEND),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이제 조립이 끝났습니다.
노드의 한 묶음 작업은 02절, 풀 크기 1인 엔진은 04절, 체크포인터와 스레드는 05절에서 배운 것입니다.

## 5. 실행 1 — 처음 상담 시간 50분

다음 셀은 처음 상담 시간 50분으로 하루를 열고, 문의 셋을 차례로 보냅니다.
50분은 세 문의의 시간을 더한 값이라, 모두 들어갑니다.

실행 전에 예상해 봅니다.
마지막 문의 뒤에 남은 상담 시간은 0분이 됩니다.
조건 CHECK는 이 0분을 막을까요?"""),
        code(RUN1),
        md("""**결과 읽기** — 출력 줄 `문의마다 남긴 예약 줄 수: [1, 1, 1]`이 보입니다.
세 문의 모두 예약되었고, 받은 오류를 알리는 줄은 없습니다.
조건이 0 이상이라, 남은 시간 0분은 막히지 않았습니다.

다음 셀은 실행 1이 끝난 뒤 표에서 읽은 값과 빌려 간 연결 수, 배송 문의의 저장된 상태를 봅니다.
메서드 `get_state`는 05절처럼 그 스레드의 마지막 체크포인트를 읽습니다."""),
        code(CHECK1),
        md("""**결과 읽기** — 라벨 `표에서 읽은 값:` 뒤에 `'남은 상담 시간(분)': 0`과 `'예약된 문의 번호': [1, 2, 3]`이 보입니다.
그 뒤의 `'체크포인트 줄 수': 9`는 문의 셋이 셋씩 남긴 체크포인트입니다.
05절에서 노드 하나인 그래프를 한 번 실행하자 체크포인트가 셋 쌓인 것과 같습니다.
출력 줄 `빌려 간 연결 수: 0`은 노드가 빌린 연결을 모두 반납했다는 뜻입니다.
배송 문의의 저장된 상태는 `{'no': 2, 'minutes': 30, 'booked': 1}`입니다.

## 6. 실행 2 — 처음 상담 시간 하나만 바꿈

다음 셀은 값 하나만 바꿉니다.
처음 상담 시간을 50분에서 30분으로 줄이고, 같은 문의 셋을 같은 차례로 보냅니다.

실행 전에 예상해 봅니다.
환불 10분 뒤 남은 시간은 20분이고, 배송은 30분이 필요합니다.
배송 문의는 어떻게 될까요?
풀에 연결이 하나뿐인데, 그다음 결제 문의는 연결을 받을 수 있을까요?"""),
        code(RUN2),
        md("""**결과 읽기** — 출력 첫 줄 `문의 2 받은 오류: IntegrityError 23514`는 노드가 출력한 줄입니다.
배송 문의의 빼기가 CHECK 제약을 어겨, 02절과 같은 오류 코드를 받았습니다.
출력 줄 `문의마다 남긴 예약 줄 수: [1, 0, 1]`에서 배송만 0입니다.
결제 문의는 배송 뒤에도 예약되었습니다.
풀에 연결이 하나뿐인데도 결제 문의가 연결을 받았으므로, 오류로 끝난 블록도 연결을 반납한 것입니다.

다음 셀은 실행 1과 같은 모양으로, 표에서 읽은 값과 저장된 상태를 봅니다."""),
        code(CHECK2),
        md("""**결과 읽기** — 라벨 `표에서 읽은 값:` 뒤에 `'남은 상담 시간(분)': 10`과 `'예약된 문의 번호': [1, 3]`이 보입니다.
배송 문의의 예약 줄은 넣었다가 취소되어 남지 않았고, 배송의 30분도 빠지지 않았습니다.
30분에서 환불 10분과 결제 10분만 빠져, 10분이 남았습니다.
그 뒤의 `'체크포인트 줄 수': 9`와 출력 줄 `빌려 간 연결 수: 0`은 실행 1과 같습니다.

배송 문의의 저장된 상태는 `{'no': 2, 'minutes': 30, 'booked': 0}`입니다.
배송 문의의 한 묶음 작업은 노드 함수 안에서 이미 취소되었습니다.
노드는 그 오류를 받아 `{"booked": 0}`을 내고 끝났고, 체크포인터는 노드가 끝난 뒤 그 상태를 표에 적었습니다.
그래서 예약되지 않은 문의의 상태도 체크포인터 표에 남았습니다.

다음 셀은 두 실행이 끝난 뒤 엔진의 풀 상태를, 04절처럼 한 줄 글로 봅니다."""),
        code(POOL),
        md("""**결과 읽기** — 라벨 줄 아래 `Pool size: 1  Connections in pool: 1 Current Overflow: 0 Current Checked out connections: 0`이 보입니다.
풀 크기 1, 쉬고 있는 연결 1, 빌려 간 연결 0입니다.
04절 After에서 본 풀 상태 글과 같은 글입니다.

## 7. 두 실행 견주기

다음 셀은 두 실행의 값을 한 줄씩 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄이 두 실행입니다.
실행 1 줄은 `실행 1 | 50 | [1, 1, 1] |`로 시작하고, 실행 2 줄은 `실행 2 | 30 | [1, 0, 1] |`로 시작합니다.
바꾼 값은 처음 상담 시간 하나였고, 배송 문의의 예약과 남은 상담 시간이 갈렸습니다.
체크포인트 줄 수와 빌려 간 연결 수는 두 실행이 같았습니다.

## 8. 새 연결로 상태 다시 읽기

체크포인터 표에 저장된 상태가, 연결을 닫은 뒤에도 남는지 봅니다.
다음 셀은 체크포인터 연결을 닫고, 새 연결로 같은 설계 객체를 다시 컴파일합니다.
05절 6절의 함수 `restored_state`와 같은 모양이고, 이번에는 같은 데이터베이스를 읽습니다.
그래프는 실행하지 않고, 배송 스레드의 저장된 상태만 읽습니다."""),
        code(RECONNECT),
        md("""**결과 읽기** — 출력 줄 `새 연결로 읽은 배송 문의의 상태: {'no': 2, 'minutes': 30, 'booked': 0}`이 보입니다.
6절에서 읽은 값과 같습니다.
상태는 연결이나 그래프 객체가 아니라, 데이터베이스의 표에 남아 있습니다.
이것이 제목의 상태 영속화입니다.
새 연결은 셀 끝에서 닫았습니다.

## 9. 정리: 이름 공간 지우기

다음 셀은 이름 공간 `ch31_practice`를 안의 표까지 지웁니다.
상담 시간 표·예약 표와 함께 체크포인터 표 넷도 지워집니다.
그다음 01절처럼 남았는지 묻고, 엔진의 풀을 비웁니다."""),
        code(CLEANUP),
        md("""**결과 읽기** — 출력 줄 `남은 이름 공간: None`과 `풀에 쉬고 있는 연결 수: 0`이 보입니다.
처음부터 다시 실행하면 같은 출력이 나옵니다.
05절을 실행했다면 확장 vector가 데이터베이스에 남아 있습니다.
이 절은 확장을 쓰지 않아 그대로 둡니다.

## 정리

1. 02절 한 묶음 작업, 04절 작은 연결 풀, 05절 체크포인터를 상담 예약 그래프 하나로 이었습니다.
2. 처음 상담 시간을 30분으로 줄이자 배송 문의만 예약되지 않았고, 결제 문의는 반납된 연결로 예약되었습니다.
3. 예약되지 않은 배송 문의의 상태 `{'no': 2, 'minutes': 30, 'booked': 0}`도 체크포인터 표에 남아, 새 연결로 다시 읽혔습니다.

이 절로 Ch 31이 끝납니다.
다음 챕터 Ch 32는 Docker와 컨테이너를 다룹니다.
그 04절은 Compose로 서비스와 PostgreSQL·pgvector를 함께 띄웁니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
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


def html_text(text: str) -> str:
    """노트북용 마크다운 한 단락(백틱·줄바꿈)을 _src 문단 글로 바꿉니다(01~05절 생성기와 같은 함수)."""
    parts = text.replace("\n", " ").split("`")
    out = ""
    for index in range(len(parts)):
        if index % 2 == 1:
            out = out + "<code>" + parts[index] + "</code>"
        else:
            out = out + parts[index]
    return out


def mermaid_block(name: str, alt: str, caption: str, reading: str) -> str:
    """.mmd가 있을 때만 본문에 넣습니다(새 커널 A·B를 그림보다 먼저 돌릴 때 빌드가 멈추지 않게)."""
    if not (FIGS / (name + ".mmd")).is_file():
        return ""
    return ("{{mermaid:" + name + "|" + alt + "|" + caption + "}}\n"
            + '<p class="look"><b>도식 읽기</b> — ' + html_text(reading) + "</p>\n")


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or ILLU_READ.startswith("[["):
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


L_CH23_01 = "../../part6/ch23-persistence/01-체크포인터와-스레드.html"
L_CH32 = "../ch32-docker/index.html"
L_01 = "01-SQLAlchemy-비동기-PostgreSQL.html"
L_02 = "02-트랜잭션과-원자성.html"
L_03 = "03-Alembic-적용과-롤백.html"
L_04 = "04-커넥션-풀-고갈과-대응.html"
L_05 = "05-pgvector-체크포인터-공존과-백업.html"

LEARNED_ROWS = [
    ('<a href="' + L_01 + '">01절</a>', "이름 공간을 지우고 다시 만들기, <code>to_regnamespace</code>, 풀의 <code>checkedin()</code>·<code>checkedout()</code>, 표 <code>requests</code>의 문의 셋(환불·배송·결제)",
     "함수 <code>open_day</code>의 이름 공간 준비, 9절 정리, 문의 셋의 번호와 이름"),
    ('<a href="' + L_02 + '">02절</a>', "한 묶음 작업(<code>begin()</code> 블록 하나)·확정·취소, <code>CHECK</code> 제약, <code>except IntegrityError as error</code>와 <code>error.orig.sqlstate</code>, <code>UPDATE</code>",
     "노드 <code>book_inquiry</code>의 예약 줄 넣기와 상담 시간 빼기, 실행 2의 <code>23514</code>"),
    ('<a href="' + L_03 + '">03절</a>', "동기 엔진 <code>create_engine</code>과 <code>with engine.begin()</code>, 접속 글 <code>postgresql+psycopg</code>, <code>array_agg</code>에 붙인 <code>ORDER BY</code>",
     "설정 셀(03절 2절 셀과 글자까지 같음), 동기 엔진, 예약된 문의 번호 읽기"),
    ('<a href="' + L_04 + '">04절</a>', "풀 크기 1·더 만들 연결 0·대기 제한 0.2초, 반납, <code>timeout()</code>·<code>status()</code>",
     "엔진의 풀 값, 두 실행 뒤 빌려 간 연결 수와 풀 상태 글"),
    ('<a href="' + L_05 + '">05절</a>', "체크포인터 연결(<code>autocommit=True</code>·<code>dict_row</code>·<code>SET search_path</code>), 표 만들기 <code>setup()</code>, 모델을 쓰지 않는 그래프, 스레드와 <code>get_state</code>, 새 연결로 다시 컴파일하기",
     "체크포인터와 그래프, 배송 문의의 저장된 상태, 8절의 새 연결로 다시 읽기"),
]

COMPARE_ROWS = [
    ("바꾼 값 — 처음 상담 시간(분)", "<code>50</code>", "<code>30</code>"),
    ("노드가 출력한 받은 오류", "없음", "<code>문의 2 받은 오류: IntegrityError 23514</code>"),
    ("문의마다 남긴 예약 줄 수", "<code>[1, 1, 1]</code>", "<code>[1, 0, 1]</code>"),
    ("남은 상담 시간(분)", "<code>0</code>", "<code>10</code>"),
    ("예약된 문의 번호", "<code>[1, 2, 3]</code>", "<code>[1, 3]</code>"),
    ("체크포인트 줄 수", "<code>9</code>", "<code>9</code>"),
    ("빌려 간 연결 수", "<code>0</code>", "<code>0</code>"),
    ("배송 문의의 저장된 상태", "<code>{'no': 2, 'minutes': 30, 'booked': 1}</code>", "<code>{'no': 2, 'minutes': 30, 'booked': 0}</code>"),
]

B4_ANALOGY = ("<p>옛 전화 교환대를 판 셋으로 조립한다고 해 봅니다. 긴 틀 하나에 하는 일이 다른 판 셋을 나란히 끼웁니다. 왼쪽 판에는 꽂는 자리가 하나뿐이고, 선 하나가 꽂혀 있습니다. 통화마다 이 선 하나를 차례로 씁니다.</p><p>가운데 판은 통화 하나에 한 칸을 씁니다. 한 칸의 위아래 두 자리는 선 하나로 함께 이어지거나, 둘 다 비어 있습니다. 한쪽 끝만 꽂힌 칸은 두지 않습니다. 오른쪽 판에는 통화마다 덮개 하나를 달아, 어떤 통화가 지나갔는지 남겨 둡니다.</p><p>그림은 실행 2가 끝난 모습입니다. 가운데 판의 가운데 칸은 비어 있지만, 오른쪽 판의 덮개는 셋입니다.</p><p>틀이 이 절의 그래프이고, 왼쪽 판이 풀 크기 1인 연결 풀입니다. 01절 비유처럼 꽂힌 선 하나가 연결 하나입니다. 가운데 판의 한 칸이 문의 하나의 한 묶음 작업이고, 비어 있는 가운데 칸이 한 묶음 작업이 취소된 배송 문의입니다. 오른쪽 판의 덮개 셋이 체크포인터 표에 저장된 문의 셋의 상태입니다.</p><p>비유와 다른 점이 있습니다. 실제 연결은 문의마다 풀에서 빌렸다가 반납합니다. 체크포인터는 덮개가 아니라 표의 줄로 상태를 적고, 문의 하나에 체크포인트 셋을 남겼습니다. 04절 비유와 달리, 이 그림의 꽂힌 선은 빌려 간 연결이 아니라 풀에 있는 연결 하나를 뜻합니다. 실행 2 뒤 빌려 간 연결은 0이었습니다.</p>")

LOOK_B5 = "노트북 5절에서 <code>문의마다 남긴 예약 줄 수: [1, 1, 1]</code>과 <code>'남은 상담 시간(분)': 0</code>을 봅니다. 6절에서 <code>문의 2 받은 오류: IntegrityError 23514</code>와 <code>[1, 0, 1]</code>, <code>'예약된 문의 번호': [1, 3]</code>을 찾습니다. 두 실행 뒤 출력 줄 <code>빌려 간 연결 수: 0</code>인지도 확인합니다."
LOOK_B6 = "7절 표에서 <code>실행 2 | 30 | [1, 0, 1] |</code>로 시작하는 줄을 찾습니다. 6절 풀 상태 글의 <code>Current Checked out connections: 0</code>과, 8절 출력의 <code>'booked': 0</code>도 확인합니다. 바꾼 값은 처음 상담 시간 하나뿐이라, 두 줄의 차이는 모두 그 값에서 나왔습니다."


def src_html() -> str:
    learned = table_html(["절", "배운 것", "실습에서 쓰는 곳"], LEARNED_ROWS)
    compare = table_html(["견준 것", "실행 1", "실행 2"], COMPARE_ROWS)
    return """<!--meta: 실습 30분 | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 0 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>02절 한 묶음 작업, 04절 작은 연결 풀, 05절 체크포인터를 상담 예약 그래프 하나로 이어 실행할 수 있습니다.</li>
<li>처음 상담 시간 하나만 바꾼 실행에서, 한 문의만 예약되지 않고 흐름이 이어지는 것을 확인할 수 있습니다.</li>
<li>예약되지 않은 문의의 상태도 체크포인터 표에 남는 까닭을 설명하고, 새 연결로 다시 읽을 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>이 챕터에서는 데이터베이스를 쓰는 방법을 절마다 따로 익혔습니다. <a href=\"""" + L_02 + """\">02절</a>은 두 변경을 한 묶음 작업으로 묶었고, <a href=\"""" + L_04 + """\">04절</a>은 빌린 연결을 반납해야 다음 요청이 연결을 받는 것을 봤습니다. <a href=\"""" + L_05 + """\">05절</a>은 그래프의 상태를 체크포인터로 PostgreSQL 표에 저장했습니다. 실제 서비스에서는 이 일들이 문의 하나를 처리하는 동안 함께 일어납니다.</p><p>이번 실습은 세 기능을 상담 예약 그래프 하나에 모아 실행합니다. 처음 상담 시간 하나만 바꿔 한 번 더 실행하고, 두 실행을 견줍니다. 02절에서도 블록 안의 빼기가 막히면 앞의 변경까지 취소되었습니다. 새로 볼 것은 그 취소가 문의 셋의 흐름 가운데에서 일어날 때입니다. 뒤의 문의가 연결을 받는지, 예약되지 않은 문의의 상태가 저장되는지 봅니다.</p><p>제목의 DB는 데이터베이스(database)입니다. 제목의 상태 영속화는 <a href=\"""" + L_CH23_01 + """\">Ch 23</a>에서 배운 상태 저장(Persistence)과 같은 뜻입니다. 이번 절은 이 챕터의 실습입니다. 01~05절에서 쓴 이름과 Ch 2에서 배운 문법만 쓰고, 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p><p><b>이 절의 질문</b> — 세 기능을 한 흐름으로 이으면, 한 문의가 막혀도 나머지 문의와 상태 저장은 이어질까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>이번 실습은 아래 절에서 배운 이름을 그대로 씁니다. 앞 절 함수를 다시 적지 않고, 흐름을 잇는 함수 넷만 노트북에 새로 적습니다.</p>
""" + learned + """
<p>붙인 기능은 02절 한 묶음 작업, 04절 작은 연결 풀과 반납, 05절 체크포인터 셋입니다. 셋 모두 실행 1·2 흐름에서 일합니다. 01절과 03절에서는 이름 공간 준비와 동기 엔진처럼 흐름을 받쳐 주는 이름을 빌려 썼습니다.</p><p>노드가 문의를 차례로 받으므로, 01절의 함께 기다리기(<code>gather</code>)는 쓰지 않았습니다. 03절의 판 올리기와 내리기는 표 구조를 바꾸는 흐름이 아니고, 판 파일 사본까지 더하면 분량이 커져 뺐습니다. 05절의 pgvector 색인과 백업·복원은 검색과 백업 명령이 더해지고, 05절의 확장 실험을 되풀이하게 되어 뺐습니다.</p><p>01·02·04절은 await를 쓰는 비동기 엔진을 썼고, 이 절은 03·05절처럼 동기 드라이버 psycopg만 씁니다. 그래프를 <code>invoke</code>로 부르고, 체크포인터 <code>PostgresSaver</code>가 psycopg의 동기 연결을 쓰기 때문입니다. 그래서 노드 안의 한 묶음 작업도 03절처럼 동기 엔진의 <code>begin()</code> 블록으로 적습니다. 블록과 연결 풀의 뜻은 02·04절과 같습니다.</p><p>이 챕터의 실습은 모델을 부르지 않습니다. 01~05절도 모델 없이 결과를 갈랐고, 이번 흐름의 결론도 줄 수와 저장된 상태처럼 매번 같은 값입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3>""" + B4_ANALOGY + """
""" + illustration_block() + """<h3>실습 조립의 구성</h3><p>실습의 흐름은 그래프 하나입니다. 문의 하나가 그래프에 들어가면 노드 <code>book_inquiry</code>가 한 번 실행됩니다. 노드는 엔진의 풀에서 연결 하나를 빌려 한 묶음 작업을 보내고, 블록이 끝나면 반납합니다. 노드 함수가 끝나 상태를 내면, 체크포인터가 따로 연 연결로 그 상태를 표에 적습니다.</p><p>상담 시간 표·예약 표와 체크포인터 표 넷은 모두 이름 공간 <code>ch31_practice</code>에 있습니다. 두 가지 표는 다른 연결로 적힙니다. 두 표를 한 묶음 작업으로 함께 확정하는 설계는 이 절에서 실행하지 않았습니다. 이 절에서 새로 배우는 말은 없습니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 03절 설정 셀과 같은 접속 글로 동기 엔진을 만들고, 두 표의 SQL 글과 문의 셋을 정합니다. 3절은 체크포인터와 노드 하나인 그래프를 만듭니다. 4절은 하루를 여는 함수와 기록 장치, 문의를 보내는 함수를 만듭니다. 5·6절은 처음 상담 시간만 다른 두 실행이고, 7절은 두 실행을 견줍니다. 8절은 새 연결로 상태를 다시 읽고, 9절은 이름 공간을 지웁니다.</p><p>모델 요청은 0번이고, API 키 없이 실행합니다. 데이터베이스 서버는 01절과 같은 Docker 컨테이너 <code>kdt-ch31-postgres</code>입니다. 작업 폴더와 운영체제 임시 폴더에는 파일을 쓰지 않습니다. 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>두 실행은 처음 상담 시간 하나만 달랐습니다. 문의 셋과 차례, 그래프, 엔진의 풀 값, 체크포인터는 같았습니다. 결과는 아래 표와 같았습니다.</p>
""" + compare + """
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>실행 1에서는 50분이 세 문의의 시간 합과 같아, 세 문의가 모두 예약되고 0분이 남았습니다. 조건이 0 이상이라, 남은 시간 0분은 막히지 않았습니다.</p><p>실행 2에서는 환불 뒤 20분이 남은 자리에 배송 30분이 왔습니다. 빼기가 CHECK 제약을 어겨 블록이 취소되었고, 앞에서 넣은 배송의 예약 줄도 남지 않았습니다. 02절에서 본 취소와 같은 모양입니다. 노드가 오류를 받아 0을 냈으므로 흐름은 이어졌고, 결제 문의가 뒤이어 예약되었습니다.</p><p>엔진의 풀에는 연결이 하나뿐이었습니다. 결제 문의가 예약되었고 두 실행 뒤 빌려 간 연결 수가 0이었으므로, <code>begin()</code> 블록은 오류로 끝날 때도 연결을 반납했습니다. 노트북 밖에서 같은 풀 값의 엔진으로 연결 하나를 닫지 않고 두었습니다. 그러자 다음 블록은 대기 제한 0.2초를 넘겨 연결을 받지 못했습니다.</p><p>체크포인트 줄 수는 두 실행 모두 9였습니다. 배송 문의의 저장된 상태는 실행 2에서 <code>'booked': 0</code>이었고, 연결을 닫은 뒤 새 연결로도 같은 값이 읽혔습니다. 배송 문의의 한 묶음 작업은 노드 함수 안에서 이미 취소되었습니다. 노드는 그 오류를 받아 <code>{"booked": 0}</code>을 내고 끝났고, 체크포인터는 노드가 끝난 뒤 그 상태를 적었습니다. 그래서 예약되지 않은 문의의 상태도 남습니다.</p><p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>문의마다 필요한 상담 시간 10·30·10분과 처음 상담 시간 50·30분은 이 절에서 실행 전에 정한 값입니다. 실행 2에서 가운데 문의가 조건을 넘도록 고른, 흐름을 보여 주는 예입니다. 문의 셋의 번호와 이름은 01절 표 <code>requests</code>에서 가져왔습니다.</li><li>예약 표와 체크포인터 표는 같은 이름 공간에 있지만, 다른 연결로 확정됩니다. 두 표가 한 묶음 작업으로 함께 취소되는지 가르는 장면은 이 절에서 실행하지 않았습니다. 둘이 함께 확정되어야 하는 서비스라면 설계를 따로 해야 하고, 그 방법은 이 챕터에서 다루지 않았습니다.</li><li>설치판 langgraph 1.2.11 소스의 <code>pregel/_runner.py</code> 207~221행은 노드 함수를 끝까지 실행한 뒤 그 결과를 적습니다. 같은 소스의 <code>pregel/_loop.py</code> 683~718행은 한 단계가 끝난 뒤 체크포인트를 적습니다. 그래서 노드 안에서 취소된 한 묶음 작업과 상관없이, 노드가 낸 상태가 저장됩니다.</li><li>노드는 오류 <code>IntegrityError</code>만 받습니다. 연결을 받지 못한 <code>sqlalchemy.exc.TimeoutError</code> 같은 다른 오류는 받지 않아, 노드 밖으로 올라갑니다. 이번 실행에서는 그런 오류가 나지 않았고, 그때의 그래프 동작은 실행하지 않았습니다.</li><li>노트북 밖에서 같은 풀 값의 동기 엔진으로 연결 하나를 닫지 않고 두었습니다. 그러자 다음 <code>begin()</code> 블록은 <code>sqlalchemy.exc.TimeoutError</code>를 받았고, 오류 글의 앞부분은 04절 Before와 같았습니다. 같은 엔진에서 CHECK 위반으로 끝난 블록 뒤에는 빌려 간 연결 수가 0이었습니다. 두 번 실행해 두 번 모두 같았습니다.</li><li>하루를 열 때마다 이름 공간을 지우므로, 실행 1의 표와 체크포인터 표는 실행 2 앞에서 지워집니다. 두 실행의 값은 변수에 남겨 7절에서 견줍니다. 두 실행이 같은 스레드 이름을 쓰지만, 실행마다 체크포인터 표를 새로 만들어 섞이지 않습니다.</li><li>체크포인터 연결은 05절처럼 <code>autocommit=True</code>와 <code>dict_row</code>로 직접 열었습니다. 체크포인터 패키지 문서는 연결을 직접 만들 때 이 두 설정을 주라고 적습니다.</li><li>노트북을 쓰기 전에 노트북 밖에서 같은 흐름을 파이썬 파일로 다섯 번 실행했습니다. 다섯 번 모두 출력이 같았고, 오류 출력은 없었습니다.</li><li>교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다. 그 서버는 Docker 컨테이너가 아니라 같은 접속 글로 켠 서버입니다. Docker 이미지로 켜면 서버 버전 번호의 끝자리가 다를 수 있습니다. 다른 버전과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>02절 한 묶음 작업, 04절 작은 연결 풀, 05절 체크포인터를 상담 예약 그래프 하나로 이었습니다.</li><li>처음 상담 시간을 30분으로 줄이자 배송 문의만 예약되지 않았고, 결제 문의는 반납된 연결로 예약되었습니다.</li><li>예약되지 않은 배송 문의의 상태 <code>{'no': 2, 'minutes': 30, 'booked': 0}</code>도 체크포인터 표에 남아, 새 연결로 다시 읽혔습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 31이 끝납니다. 다음 챕터 <a href=\"""" + L_CH32 + """\">Ch 32</a>는 Docker와 컨테이너를 다룹니다. 그 04절은 Compose로 서비스와 PostgreSQL·pgvector를 함께 띄웁니다. 이 절이 만든 이름 공간은 끝에서 지워, 다음 챕터로 넘기는 표는 없습니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. 노드 <code>book_inquiry</code>가 <code>begin()</code> 블록 하나에 넣은 SQL 글 둘은 무엇이고, 실행 2에서 배송 문의의 예약 줄은 왜 남지 않았나요?</p><p class="quiz-a">예약 표에 문의 번호를 넣는 글과, 상담 시간 표에서 그 문의의 분을 빼는 글입니다. 빼기가 CHECK 제약을 어겨 오류 코드 <code>23514</code>를 받자, 블록은 확정하지 않고 넣기까지 취소했습니다. 틀렸다면 노트북 3절과 6절을 다시 읽습니다.</p><p class="quiz-q">2. 엔진의 풀에 연결이 하나뿐인데, 실행 2의 결제 문의가 연결을 받은 까닭은 무엇인가요?</p><p class="quiz-a">배송 문의의 <code>begin()</code> 블록이 오류로 끝날 때도 연결을 풀에 반납했기 때문입니다. 두 실행 뒤 빌려 간 연결 수는 0이었고, 풀 상태 글에도 빌려 간 연결이 0이었습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">3. 실행 2에서 남은 상담 시간이 10분인 까닭은 무엇인가요?</p><p class="quiz-a">처음 30분에서 환불 10분과 결제 10분만 빠졌기 때문입니다. 배송 30분은 블록이 취소되어 빠지지 않았습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">4. 배송 문의의 한 묶음 작업은 취소되었는데, 체크포인터 표에는 무엇이 남았나요?</p><p class="quiz-a">상태 <code>{'no': 2, 'minutes': 30, 'booked': 0}</code>이 남았고, 체크포인트 줄 수도 실행 1과 같은 9였습니다. 배송 문의의 한 묶음 작업은 노드 안에서 이미 취소되었고, 노드는 오류를 받아 <code>{"booked": 0}</code>을 내고 끝났습니다. 체크포인터는 노드가 끝난 뒤 그 상태를 적었습니다. 틀렸다면 노트북 6절과 8절을 다시 읽습니다.</p><p class="quiz-q">5. 실행 2가 실행 1의 예약 줄과 체크포인트를 보지 않은 까닭은 무엇인가요?</p><p class="quiz-a">함수 <code>open_day</code>가 하루를 열 때마다 이름 공간을 안의 표까지 지우고 다시 만들기 때문입니다. 체크포인터 표도 함께 지워져, 표 만들기 <code>setup()</code>으로 다시 만듭니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.sqlalchemy.org/en/20/core/connections.html">SQLAlchemy Working with Engines and Connections</a></div>확인 2026-09-29 · 문서 2.0.54 · 블록 <code>engine.begin()</code>은 정상으로 끝나면 확정한다고 적습니다. 오류가 나면 취소한 뒤, 그 오류를 밖으로 내보낸다고 적습니다. 블록이 끝나면 연결을 풀에 반납한다고 적습니다.</li><li><div><a href="https://docs.sqlalchemy.org/en/20/core/pooling.html">SQLAlchemy Connection Pooling</a></div>확인 2026-09-29 · 문서 2.0.54 · 엔진은 따로 정하지 않으면 풀 <code>QueuePool</code>을 쓴다고 적습니다. 인자 <code>pool_size</code>·<code>max_overflow</code>·<code>pool_timeout</code>의 뜻을 적고, 연결을 닫으면 풀에 다시 넣는다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/ddl-constraints.html">PostgreSQL 17 Constraints</a></div>확인 2026-09-29 · CHECK 제약은 칸 값이 참·거짓 식을 만족해야 한다는 조건이라고 적습니다. 어기는 값을 저장하려 하면 오류가 난다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/ddl-schemas.html">PostgreSQL 17 Schemas</a></div>확인 2026-09-29 · 이름 공간을 안의 것까지 지우려면 <code>DROP SCHEMA … CASCADE</code>를 쓴다고 적습니다. 설정 <code>search_path</code>에 적은 첫 이름 공간에, 이름 공간을 적지 않은 새 표가 생긴다고 적습니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langgraph/checkpointers">LangGraph Checkpointers</a></div>확인 2026-09-29 · 그래프는 단계마다 체크포인트를 만들고, 스레드는 체크포인트에 붙는 이름이라고 적습니다. 메서드 <code>get_state</code>는 그 스레드의 마지막 체크포인트를 내놓고, 칸 <code>values</code>에 상태 값이 있다고 적습니다.</li><li><div><a href="https://pypi.org/project/langgraph-checkpoint-postgres/">langgraph-checkpoint-postgres</a></div>확인 2026-09-29 · 문서 3.1.2 · 연결을 직접 만들면 <code>autocommit=True</code>와 <code>row_factory=dict_row</code>를 주라고 적습니다. 처음 쓸 때 <code>setup()</code>으로 표를 만들라고 적습니다.</li><li>설치판 sqlalchemy 2.0.43 소스 <code>engine/base.py</code> 3216~3243행은 동기 엔진의 <code>begin()</code>입니다. 연결을 <code>with</code> 블록으로 빌리고, 그 안에서 <code>conn.begin()</code> 블록을 엽니다. 228~232행은 연결의 <code>with</code> 블록이 끝날 때 <code>close()</code>를 부르는 자리입니다. <code>pool/impl.py</code> 43행이 풀 <code>QueuePool</code>입니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


def notebook_code_cells(path: Path) -> list:
    nb = json.loads(path.read_text(encoding="utf-8"))
    sources = []
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source = cell["source"]
            if not isinstance(source, str):
                source = "".join(source)
            sources.append(source)
    return sources


if __name__ == "__main__":
    # 2절 설정 셀은 03절 설정 셀과 글자까지 같음(「03절 노트북 2절의 설정 셀과 글자까지 같은 셀」 문장의 근거)
    assert SETTINGS in AUTHOR03.read_text(encoding="utf-8"), "SETTINGS가 03절 생성기의 셀 글과 다릅니다"
    assert SETTINGS in notebook_code_cells(NB03), "SETTINGS가 03절 노트북의 코드 셀과 다릅니다"
    # 도구 파일을 만들지 않음 — 01~05 노트북 함수 이름을 이 절에서 다시 정의하지 않는지 확인
    earlier_names = ["read_question", "read_balances", "add_balances", "transfer_one_block", "transfer_two_blocks",
                     "show_state", "try_upgrade", "ask_database", "shared_tables", "run_tool", "restore_copy",
                     "read_restored", "restored_state", "double_value"]
    code_count = 0
    for cell in cells():
        if cell["cell_type"] == "code":
            code_count = code_count + 1
            for name in earlier_names:
                assert ("def " + name + "(") not in cell["source"], name
    assert 20 <= code_count <= 32, "코드 셀 수가 20~32 밖입니다"
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "06", SLUG, "experiment", cells())
        print("wrote", path, "code cells", code_count)
