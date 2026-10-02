"""Ch 31 04절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§5-3·§6 paired).

사용:
  python3 -B author_04.py            → 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_04.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
이후 run_section.sh 가 pre_exec.sh(PostgreSQL 켜기) → 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **paired 형식 유지**. 슬러그 `04-커넥션-풀-고갈과-대응` 그대로.
재개 작업: 앞 작업자가 설계·노트북 밖 확인(5/5)·문서 확인을 끝내고 기기 연결이 끊겨 멈춤 — 코드 셀 상수는
.cache/ch31-04/resume/author_04_draft.py 그대로(VARY 둘째 주석 줄만 더함), 제목 셀·cells()·_src 본문은 재개 작업자가 새로 씀.

## 결정 1 — paired: Before = 닫지 않고 둔 연결(반납 누락, 실제 결함 — handoff §03 → §04 2), After = close() + async with

엔진 create_async_engine(database_url, pool_size=1, max_overflow=0, pool_timeout=0.2). 조회는 표 없이 SELECT current_database().
예시(3·4절) = async with로 빌리고 반납 · 함수 ask_database · 연결 하나를 빌린 채 둘째 → sqlalchemy.exc.TimeoutError(노랑) · 이름 가르기.
Before(5절) = conn = await engine.connect() → 조회 → 닫지 않음 → 빌려 간 1·쉬는 0 → 다음 요청 → TimeoutError(노랑) → 받지 못함(빨강).
After(6절) = await conn.close() → async with 셀 → 같은 다음 요청 셀 → ch31_lab. 값 바꿔 보기(7절) = 대기 제한 1.0 → timeout 1.00.
정리(8절) = 닫지 않은 연결 닫기 → dispose → 0·0(다시 실행해도 같은 출력). 다음 요청 셀은 세 곳 같은 상수(__main__ 대조).
노트북 밖 /tmp/ch31-04/exp/e1_scene.py 5/5 같음(stdout 91c726007280fa11, stderr 0바이트) — 재개 때 2번 더 같음.

## 결정 2 — 이름 가르기: import sqlalchemy.exc · except sqlalchemy.exc.TimeoutError as error · issubclass·__module__ 첫 풀이 · Ch 16 05와 이음
## 결정 3 — 말: 커넥션 풀 → 연결 풀(01) · 고갈 → 빌려 줄 연결이 없다(제목 풀이만) · pool_timeout → 대기 제한 · 반납 · 닫지 않고 둔 연결 · 이름 가림
##          패키지·서버 번호는 「버전」(03 모양 — 이 절은 교환대 「판」을 비유에 씀)
## 쓰지 않은 것: f-string·내포식·lambda·조건 표현식·next·create_task·gather·time·클래스·데코레이터·힌트·기본값 매개변수·세미콜론·가짜 모델
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part7/ch31-database/notebooks"
FIGS = ROOT / "textbook/part7/ch31-database/figures"
SLUG = "04-커넥션-풀-고갈과-대응"
TITLE_TEXT = "커넥션 풀 고갈과 대응"
SRC = ROOT / "textbook/part7/ch31-database/_src" / (SLUG + ".html")
AUTHOR01 = ROOT / "textbook/part7/ch31-database/qa/upgrade/author_01.py"
RUNS_SENTENCE = os.environ.get("AUTHOR04_RUNS_SENTENCE", "새 커널로 두 번 실행해 견주자, 코드 셀 스물하나의 출력이 셀마다 모두 같았습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 모델을 부르지 않아, 이 절의 출력은 정해 둔 풀 설정과 빌려 간 연결 수로 정해집니다.")

# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["sqlalchemy[asyncio]==2.0.43", "asyncpg==0.30.0"])

IMPORTS = r'''# SQLAlchemy의 오류 모듈·SQL 글·비동기 엔진에 쓸 이름을 가져옵니다
# 오류 이름 TimeoutError는 따로 가져오지 않고, 모듈 sqlalchemy.exc째 가져옵니다(까닭은 4절에서 봅니다)
import sqlalchemy.exc
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

print("가져온 이름:", "sqlalchemy.exc", "text", "create_async_engine")'''

SETTINGS = r'''# 데이터베이스 접속 글을 정합니다(비밀번호 postgres는 이 실습에서만 쓰는 연습용 값입니다)
database_url = "postgresql+asyncpg://postgres:postgres@127.0.0.1:55431/ch31_lab"
# 비밀번호가 찍히지 않게, 글을 @에서 나눠 앞의 드라이버 부분과 뒤의 서버 부분만 출력합니다
url_parts = database_url.split("@")
print("드라이버 부분:", database_url.split("://")[0])
print("서버 주소와 데이터베이스:", url_parts[1])'''

ENGINE = r'''# 연결 풀이 작은 비동기 엔진을 만듭니다(풀에 둘 연결 수 1, 더 만들 연결 수 0, 대기 제한 0.2초)
engine = create_async_engine(database_url, pool_size=1, max_overflow=0, pool_timeout=0.2)
print("풀의 종류:", type(engine.pool).__name__)
print("풀에 둘 연결 수:", engine.pool.size())
# timeout()은 빌려 줄 연결이 없을 때 기다릴 초, 곧 대기 제한을 내놓습니다
print("대기 제한(초):", engine.pool.timeout())'''

ASK_SQL = r'''# 연결로 보낼 짧은 조회를 SQL 글 객체로 만듭니다(지금 붙은 데이터베이스의 이름을 묻습니다)
ask_sql = text("SELECT current_database()")
print("SQL 글:", ask_sql)'''

BORROW = r'''# async with 블록으로 연결을 하나 빌려 조회하고, 블록 안과 밖에서 풀의 연결 수를 봅니다
async with engine.connect() as conn:
    result = await conn.execute(ask_sql)
    print("받은 데이터베이스 이름:", result.scalar_one())
    print("블록 안 - 빌려 간 연결 수:", engine.pool.checkedout())
# 블록이 끝나면 연결은 닫히지 않고 풀에 다시 들어갑니다
print("블록 밖 - 빌려 간 연결 수:", engine.pool.checkedout())
print("블록 밖 - 풀에 쉬고 있는 연결 수:", engine.pool.checkedin())'''

STATUS = r'''# 풀의 상태를 한 줄 글로 봅니다(풀 크기·쉬고 있는 연결·더 만든 연결·빌려 간 연결 차례)
print("풀 상태:")
print(engine.pool.status())'''

DEF_ASK = r'''# 다음 요청이 할 일: 연결을 async with로 빌려 데이터베이스 이름을 묻고, 받은 이름을 내놓습니다
async def ask_database():
    async with engine.connect() as request_conn:
        result = await request_conn.execute(ask_sql)
        database_name = result.scalar_one()
    return database_name'''

CALL_ASK = r'''# 함수를 한 번 불러 이름을 받고, 함수가 끝난 뒤 빌려 간 연결 수를 봅니다
database_name = await ask_database()
print("받은 데이터베이스 이름:", database_name)
print("빌려 간 연결 수:", engine.pool.checkedout())'''

EXHAUST = r'''# 첫째 연결을 빌린 채로, 블록 안에서 둘째 연결을 빌려 봅니다(오류가 나면 이름과 글을 출력합니다)
async with engine.connect() as first_conn:
    print("첫째 연결을 빌린 동안 빌려 간 연결 수:", engine.pool.checkedout())
    try:
        async with engine.connect() as second_conn:
            print("둘째 연결도 받았습니다")
    except sqlalchemy.exc.TimeoutError as error:
        print("받은 오류:", type(error).__name__)
        print("오류 글:", error)
print("첫째 블록이 끝난 뒤 빌려 간 연결 수:", engine.pool.checkedout())'''

NAME_CHECK = r'''# 받은 오류의 종류가 든 모듈과, 무엇을 이어받은 종류인지 봅니다
pool_error = sqlalchemy.exc.TimeoutError
print("오류 종류가 든 모듈:", pool_error.__module__)
print("SQLAlchemyError를 이어받는가:", issubclass(pool_error, sqlalchemy.exc.SQLAlchemyError))
# 모듈 이름 없이 적은 TimeoutError는 파이썬에 들어 있는 오류 종류입니다
print("파이썬의 TimeoutError를 이어받는가:", issubclass(pool_error, TimeoutError))'''

LEAK = r'''# Before: async with 없이 연결을 빌려 데이터베이스 이름을 묻고, 연결을 닫지 않은 채 셀을 끝냅니다
conn = await engine.connect()
result = await conn.execute(ask_sql)
print("받은 데이터베이스 이름:", result.scalar_one())
# 조회는 끝났지만, 연결이 풀에 다시 들어갔는지 연결 수로 봅니다
before_checked_out = engine.pool.checkedout()
print("빌려 간 연결 수:", before_checked_out)
print("풀에 쉬고 있는 연결 수:", engine.pool.checkedin())'''

NEXT_REQUEST = r'''# 다음 요청: 함수 ask_database로 연결을 빌려 보고, 오류가 나면 받은 오류의 이름과 글을 출력합니다
try:
    database_name = await ask_database()
    print("받은 데이터베이스 이름:", database_name)
except sqlalchemy.exc.TimeoutError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:", error)'''

STILL_OPEN = r'''# 닫지 않고 둔 연결 conn으로 한 번 더 묻고, 풀 상태를 봅니다
result = await conn.execute(ask_sql)
print("닫지 않은 연결로 받은 이름:", result.scalar_one())
print("풀 상태:")
print(engine.pool.status())'''

CLOSE = r'''# After: 닫지 않고 둔 연결을 닫습니다(풀에서 빌린 연결은 닫으면 풀에 다시 들어갑니다)
await conn.close()
print("빌려 간 연결 수:", engine.pool.checkedout())
print("풀에 쉬고 있는 연결 수:", engine.pool.checkedin())'''

FIXED = r'''# After: Before 셀과 같은 일을 async with 블록 안에서 합니다(블록이 끝나면 연결이 반납됩니다)
async with engine.connect() as conn:
    result = await conn.execute(ask_sql)
    print("받은 데이터베이스 이름:", result.scalar_one())
after_checked_out = engine.pool.checkedout()
print("빌려 간 연결 수:", after_checked_out)
print("풀에 쉬고 있는 연결 수:", engine.pool.checkedin())'''

COMPARE = r'''# Before 셀과 After 셀이 끝난 뒤의 빌려 간 연결 수를 모아 보고, 지금 풀 상태를 봅니다
print("Before 셀 뒤 빌려 간 연결 수:", before_checked_out)
print("After 셀 뒤 빌려 간 연결 수:", after_checked_out)
print("풀 상태:")
print(engine.pool.status())'''

VARY = r'''# 값 바꿔 보기: 대기 제한만 1.0초로 바꾼 엔진을 새로 만들고, Before 셀처럼 연결을 닫지 않고 둡니다
# 대기 제한은 엔진을 만들 때 정하므로, 지금 엔진의 풀을 먼저 비웁니다
await engine.dispose()
engine = create_async_engine(database_url, pool_size=1, max_overflow=0, pool_timeout=1.0)
conn = await engine.connect()
result = await conn.execute(ask_sql)
print("받은 데이터베이스 이름:", result.scalar_one())
print("대기 제한(초):", engine.pool.timeout())
print("빌려 간 연결 수:", engine.pool.checkedout())'''

CLEANUP = r'''# 끝 정리: 값 바꿔 보기에서 닫지 않고 둔 연결을 닫고, 엔진의 풀을 비웁니다
await conn.close()
print("닫은 뒤 빌려 간 연결 수:", engine.pool.checkedout())
await engine.dispose()
print("풀을 비운 뒤 쉬고 있는 연결 수:", engine.pool.checkedin())'''

# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/04-figures.md)
FIG1 = "04-1-연결을-빌리고-풀에-다시-넣기"
FIG1_ALT = "위에서 아래로 여섯 상자가 한 줄로 이어진 흐름도입니다. 초록 상자 접속 글 127.0.0.1:55431/ch31_lab에서 파란 상자 create_async_engine pool_size=1 max_overflow=0 pool_timeout=0.2로, 다시 회색 상자 연결 풀 AsyncAdaptedQueuePool 풀에 둘 연결 하나 대기 제한 0.2초로 갑니다. 이어서 파란 상자 async with engine.connect() 연결 하나를 빌려 SELECT current_database(), 노란 상자 블록 안 빌려 간 연결 하나 받은 이름 ch31_lab, 노란 상자 블록이 끝난 뒤 반납 빌려 간 연결 없음 쉬고 있는 연결 하나로 이어지는 그림"
FIG1_CAP = "풀에 둘 연결이 하나인 엔진에서 async with로 빌린 연결은, 블록이 끝나자 반납되어 쉬고 있는 연결로 남았습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 셀에 적은 접속 글이고, 파란 상자 둘은 우리가 부른 함수와 블록입니다.
회색 상자는 라이브러리가 만든 연결 풀이고, 종류 이름은 노트북 2절 출력에 있습니다.
노란 상자 둘은 노트북 3절 출력으로 확인한 연결 수와 받은 이름입니다."""

FIG2 = "04-2-연결-하나를-빌린-채-둘째-빌리기"
FIG2_ALT = "위에서 아래로 여섯 상자가 한 줄로 이어진 흐름도입니다. 파란 상자 async with engine.connect() 첫째 연결을 빌림에서 노란 상자 첫째를 빌린 동안 빌려 간 연결 하나로, 다시 파란 상자 블록 안에서 둘째 연결을 빌리려 함으로 갑니다. 이어서 회색 상자 풀 크기 하나 더 만들 연결 없음 대기 제한 0.2초 동안 반납을 기다림, 노란 상자 받은 오류 TimeoutError QueuePool limit of size 1 overflow 0 reached timeout 0.20, 노란 상자 오류가 든 모듈 sqlalchemy.exc 파이썬의 TimeoutError를 이어받는가 False로 이어지는 그림"
FIG2_CAP = "첫째 연결을 빌린 채 둘째를 빌리자, 크기 하나인 풀은 대기 제한 안에 연결을 주지 못하고 TimeoutError를 냈습니다."
FIG2_READ = """위에서 아래로 읽습니다.
파란 상자 둘은 노트북 4절에서 우리가 적은 블록 둘입니다.
회색 상자는 풀이 반납을 기다리는 일로, 설치된 SQLAlchemy 소스에서 확인했습니다.
노란 상자 셋은 4절 출력으로 확인한 연결 수, 받은 오류, 오류 종류의 모듈과 이어받음입니다."""

FIG3 = "04-3-닫지-않고-둔-연결의-Before"
FIG3_ALT = "위에서 아래로 다섯 상자가 한 줄로 이어진 흐름도입니다. 파란 상자 Before 셀 conn = await engine.connect() 조회 뒤 닫지 않음에서 파란 상자 다음 요청 ask_database async with로 빌리려 함으로, 다시 노란 상자 받은 오류 TimeoutError timeout 0.20으로 갑니다. 이어서 빨간 상자 다음 요청은 연결을 받지 못함 빌려 간 연결 하나 쉬고 있는 연결 없음, 노란 상자 닫지 않은 conn으로 조회 받은 이름 ch31_lab Current Checked out connections: 1로 이어지는 그림"
FIG3_CAP = "Before 셀이 닫지 않고 둔 연결이 빌려 간 채 남아, 다음 요청은 대기 제한 안에 연결을 받지 못했습니다."
FIG3_READ = """위에서 아래로 읽습니다.
파란 상자 둘은 노트북 5절의 Before 셀과 다음 요청 셀입니다.
노란 상자 둘은 받아 출력한 오류와, 닫지 않은 연결로 다시 물은 결과입니다.
빨간 상자는 Before 결함 결과로, 다음 요청이 연결을 받지 못한 것과 그때의 연결 수입니다."""

FIG4 = "04-4-닫지-않은-셀과-async-with-셀-견주기"
FIG4_ALT = "위에 회색 상자 하나가 있고 아래에 칸 둘이 나란히 놓인 그림입니다. 회색 상자 두 셀 같음 풀 크기 하나 대기 제한 0.2초 SELECT current_database() 받은 이름 ch31_lab에서 두 칸으로 화살표가 갑니다. 한 칸 Before 닫지 않음에는 파란 상자 conn = await engine.connect() 조회 뒤 셀을 끝냄, 빨간 상자 셀 뒤 빌려 간 연결 하나 쉬고 있는 연결 없음, 노란 상자 다음 요청 받은 오류 TimeoutError가 있습니다. 다른 칸 After 닫고 async with에는 파란 상자 await conn.close() 뒤 async with engine.connect(), 노란 상자 셀 뒤 빌려 간 연결 없음 쉬고 있는 연결 하나, 노란 상자 다음 요청 받은 이름 ch31_lab이 있는 그림"
FIG4_CAP = "같은 조회를 한 두 셀 가운데 Before는 빌려 간 연결 하나를 남겼고, After는 반납해 다음 요청이 이름을 받았습니다."
FIG4_READ = """맨 위 회색 상자는 두 셀에서 같았던 엔진 설정·조회·받은 이름입니다.
왼쪽 Before 칸과 오른쪽 After 칸의 파란 상자가 두 셀에서 다른 줄입니다.
빨간 상자는 Before 셀의 결함 결과이고, 노란 상자는 출력으로 확인한 값입니다.
두 칸의 값은 노트북 5절과 6절 출력입니다."""

ILLU = "04-5-판에-꽂힌-채인-선과-받침에-놓인-선"
ILLU_ALT = "흰 바탕에 짙은 남색 교환대 둘이 나란히 놓여 화면을 채웁니다. 교환대마다 세워 둔 판 가운데에 흰 테두리의 둥근 꽂는 자리가 하나 있고, 판 아래에는 앞으로 누운 선반이 있습니다. 선반마다 둥근 받침 구멍이 하나 있습니다. 왼쪽 교환대는 겨자색 선 하나의 금빛 끝이 판의 자리에 꽂혀 있고, 선은 선반 위를 지나 아래로 내려가며, 선반의 받침 구멍은 비어 있습니다. 오른쪽 교환대는 겨자색 선의 금빛 끝이 선반의 받침 구멍에 곧게 세워져 있고, 판의 자리는 비어 있습니다. 사람·손·글자·숫자·화살표·불은 없는 그림"
ILLU_CAP = "왼쪽 교환대는 선이 판에 꽂힌 채 받침 구멍이 비어 있고, 오른쪽 교환대는 선 끝이 받침 구멍에 세워져 있습니다."
ILLU_READ = "짙은 남색 교환대 둘이 나란히 있습니다. 교환대마다 판에 꽂는 자리가 하나, 선반에 받침 구멍이 하나, 겨자색 선이 한 가닥입니다. 왼쪽은 선 끝이 판의 자리에 꽂혀 있고, 선반의 받침 구멍은 비어 있습니다. 오른쪽은 선 끝이 받침 구멍에 세워져 있고, 판의 자리는 비어 있습니다. 왼쪽이 연결을 닫지 않은 Before 셀 뒤, 오른쪽이 반납한 After 셀 뒤의 풀입니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 풀에 둘 연결 수가 1인 엔진을 만들고, 연결을 빌리고 풀에 다시 넣는 것을 연결 수로 봅니다.
2. 빌린 연결을 닫지 않고 두면, 다음 요청이 연결을 받지 못하고 오류를 받는 것을 봅니다.
3. 연결을 닫거나 `async with` 블록으로 빌려, 다음 요청이 다시 연결을 받는 것을 확인합니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
예상 비용도 0달러입니다.

01절과 같은 PostgreSQL 서버가 `127.0.0.1:55431`에서 켜져 있어야 합니다.
서버는 01절 준비물의 Docker 컨테이너 `kdt-ch31-postgres`입니다.
꺼져 있으면 터미널에서 `docker start kdt-ch31-postgres`로 다시 켭니다.
컨테이너를 아직 만들지 않았다면, 01절 노트북 맨 위 준비물의 `docker run` 명령을 먼저 실행합니다.

노트북은 표를 만들지 않고, 서버에 지금 데이터베이스의 이름만 묻습니다.
작업 폴더에 파일을 쓰지 않고, 읽어 오는 자료 파일도 없습니다.
오류를 받는 셀은 대기 제한만큼 기다린 뒤 끝나지만, 걸린 시간은 재지 않습니다.

**기준 버전** — 첫 셀에서 패키지 둘을 설치합니다.
버전은 sqlalchemy 2.0.43과 asyncpg 0.30.0이고, 실습 폴더 잠금과 같습니다.
교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다.
그 서버는 Docker 컨테이너가 아니라, 같은 접속 글로 켠 서버입니다.

Docker 이미지로 켜면 서버 버전 번호의 끝자리가 다를 수 있습니다.
다른 버전과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~4절을 읽습니다.
풀의 크기와 대기 제한, 받은 오류의 이름을 처음 보는 자리입니다.
5·6절은 Before와 After이고, 7절은 값 바꿔 보기입니다.
5~7절은 실습 시간에 실행하고, 8절은 엔진의 풀을 비우는 정리입니다.

실습 폴더 `labs/part7/ch31-database`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

01절에서는 비동기 엔진이 연결 풀을 두고, 빌린 연결을 블록이 끝나면 풀에 다시 넣는 것을 봤습니다.
이 절은 풀에 빌려 줄 연결이 하나도 남지 않을 때 무슨 일이 생기는지 봅니다.
그런 일이 생기는 흔한 까닭 하나는, 빌려 간 연결을 닫지 않고 두는 것입니다.

절 제목의 커넥션 풀(connection pool)은 01절에서 본 연결 풀입니다.
제목의 고갈은 풀에 빌려 줄 연결이 하나도 남지 않은 상태를 말합니다.
이 교재 본문에서는 「빌려 줄 연결이 없다」고 적습니다.

첫 셀은 01절과 같은 패키지 둘을 설치하고, 설치된 버전 번호를 출력합니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `sqlalchemy: 2.0.43`과 `asyncpg: 0.30.0`이 보입니다.
01절과 같은 버전이고, 실습 폴더 잠금과 같습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
오류 이름은 따로 가져오지 않고, 모듈 `sqlalchemy.exc`를 통째로 가져옵니다.
02절은 이 모듈에서 오류 이름 `IntegrityError`만 가져왔습니다.
이 절에서 받을 오류는 이름이 `TimeoutError`라, 파이썬에 이미 있는 이름과 겹칩니다.
어떻게 겹치는지는 4절에서 봅니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `가져온 이름: sqlalchemy.exc text create_async_engine`이 보입니다.
이 노트북에는 API 키를 확인하는 셀이 없습니다.
모델을 부르지 않기 때문입니다.

## 2. 연결 풀이 작은 엔진

다음 셀은 01절 2절의 설정 셀과 글자까지 같은 셀로, 연습용 접속 글을 정합니다.
이 노트북도 `.env` 파일을 읽지 않습니다.
서버를 다른 주소나 계정으로 켰다면 이 셀의 글만 고칩니다."""),
        code(SETTINGS),
        md("""**결과 읽기** — 출력 줄 `드라이버 부분: postgresql+asyncpg`가 보입니다.
라벨 `서버 주소와 데이터베이스:` 뒤의 `127.0.0.1:55431/ch31_lab`은 01절과 같은 서버와 데이터베이스입니다.
비밀번호가 든 가운데 부분은 출력하지 않았습니다.

다음 셀은 연결 풀이 아주 작은 엔진을 만듭니다.
인자 `pool_size=1`은 풀에 둘 연결 수이고, `max_overflow=0`은 그 밖에 더 만들 연결 수입니다.
두 인자는 01절에서 봤고, 이 엔진은 연결을 한 번에 하나만 빌려 줄 수 있습니다.
새 인자 `pool_timeout=0.2`는 빌려 줄 연결이 없을 때 기다릴 초입니다.
이 교재에서는 이 값을 「대기 제한」이라고 부릅니다."""),
        code(ENGINE),
        md("""**결과 읽기** — 출력 줄 `풀의 종류: AsyncAdaptedQueuePool`과 `풀에 둘 연결 수: 1`이 보입니다.
출력 줄 `대기 제한(초): 0.2`는 인자로 준 값입니다.
SQLAlchemy 문서는 비동기 엔진이 따로 정하지 않으면 이 종류의 풀을 쓴다고 적습니다.
엔진을 만들기만 해서는 서버에 붙지 않는 것은 01절과 같습니다.

## 3. 연결을 빌리고 풀에 다시 넣기

연결을 빌려 서버에 짧은 조회 하나를 보내 봅니다.
PostgreSQL 함수 `current_database()`는 지금 붙은 데이터베이스의 이름을 내놓습니다.
표가 없어도 되는 조회라, 이 절은 이름 공간과 표를 만들지 않습니다.
다음 셀은 이 조회를 SQL 글 객체로 만듭니다."""),
        code(ASK_SQL),
        md("""**결과 읽기** — 출력 줄 `SQL 글: SELECT current_database()`가 보입니다.
이 셀은 객체를 만들기만 했고, 서버에는 아직 아무것도 보내지 않았습니다.

다음 셀은 01절처럼 `async with` 블록으로 연결을 하나 빌립니다.
블록 안과 밖에서, 빌려 간 연결 수와 풀에 쉬고 있는 연결 수를 봅니다.
메서드 `checkedout()`과 `checkedin()`은 01절에서 본 그 두 수를 내놓습니다."""),
        code(BORROW),
        md("""**결과 읽기** — 출력 줄 `받은 데이터베이스 이름: ch31_lab`이 보입니다.
출력 줄 `블록 안 - 빌려 간 연결 수: 1`은 블록 안에서 연결 하나를 빌려 쓰는 중이라는 뜻입니다.
블록이 끝나자 `블록 밖 - 빌려 간 연결 수: 0`과 `블록 밖 - 풀에 쉬고 있는 연결 수: 1`이 되었습니다.
빌린 연결을 풀에 다시 넣는 일을, 이 교재에서는 「반납」이라고 부릅니다.

블록이 끝나면 연결을 닫는 메서드 `close()`가 불립니다.
풀에서 빌린 연결은 닫아도 서버와 끊기지 않고, 풀에 다시 들어갑니다.
SQLAlchemy 문서도 닫은 연결이 풀에 놓인다고 적습니다.

다음 셀은 풀의 상태를 한 줄 글로 봅니다.
메서드 `status()`는 풀 크기·쉬고 있는 연결·더 만든 연결·빌려 간 연결의 수를 한 줄 글로 내놓습니다."""),
        code(STATUS),
        md("""**결과 읽기** — 라벨 줄 아래 `Pool size: 1  Connections in pool: 1 Current Overflow: 0 Current Checked out connections: 0`이 보입니다.
풀 크기 1, 쉬고 있는 연결 1, 더 만든 연결 0, 빌려 간 연결 0이라는 뜻입니다.
앞 셀에서 센 연결 수와 같습니다.

## 4. 빌려 줄 연결이 없을 때

서비스에서는 요청이 올 때마다 연결을 빌려 조회합니다.
다음 셀의 함수 `ask_database`는 그런 요청 하나가 하는 일입니다.
연결을 `async with`로 빌려 데이터베이스 이름을 묻고, 받은 이름을 내놓습니다.
블록이 끝나면 연결은 풀에 반납됩니다."""),
        code(DEF_ASK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 안의 연결 이름 `request_conn`은 셀 맨 위의 이름 `conn`과 겹치지 않게 지었습니다.

다음 셀은 이 함수를 한 번 불러 봅니다."""),
        code(CALL_ASK),
        md("""**결과 읽기** — 출력 줄 `받은 데이터베이스 이름: ch31_lab`과 `빌려 간 연결 수: 0`이 보입니다.
함수가 끝날 때 연결을 반납해, 빌려 간 연결이 남지 않았습니다.

이번에는 연결 하나를 빌린 채로, 블록 안에서 둘째 연결을 빌려 봅니다.
풀에 둘 연결 수가 1이고 더 만들 연결 수가 0이라, 둘째에게 빌려 줄 연결이 없습니다.
그때 풀은 대기 제한 0.2초 동안 연결이 반납되기를 기다립니다.
오류가 날 것이므로 Ch 2 05절처럼 `try`로 감싸고, 받은 오류의 이름과 글을 출력합니다.
받을 오류 이름은 모듈 이름을 붙여 `sqlalchemy.exc.TimeoutError`로 적습니다.

실행 전에 예상해 봅니다.
둘째 연결을 빌리는 줄은 무엇을 받을까요?"""),
        code(EXHAUST),
        md("""**결과 읽기** — 출력 줄 `첫째 연결을 빌린 동안 빌려 간 연결 수: 1`과 `받은 오류: TimeoutError`가 보입니다.
라벨 `오류 글:` 뒤에는 `QueuePool limit of size 1 overflow 0 reached, connection timed out, timeout 0.20`이 있습니다.
크기 1·더 만들 연결 0인 풀이 대기 제한 0.20초 안에 연결을 주지 못했다는 뜻입니다.
둘째 블록 안의 출력 줄은 찍히지 않았습니다.

오류 글 끝의 괄호 안 주소는 SQLAlchemy 문서에서 이 오류를 설명하는 곳입니다.
문서는 이 오류의 흔한 까닭으로, 빌려 간 연결을 반납하지 않고 열어 두는 것을 듭니다.
첫째 블록이 끝난 뒤에는 `첫째 블록이 끝난 뒤 빌려 간 연결 수: 0`이 되었습니다.

다음 셀은 받은 오류의 종류를 살펴봅니다.
속성 `__module__`은 그 종류가 정의된 모듈의 이름입니다.
함수 `issubclass`는 앞의 종류가 뒤의 종류를 이어받았는지 참·거짓으로 내놓습니다.
마지막 줄의 `TimeoutError`는 모듈 이름 없이 적어, 파이썬에 들어 있는 오류 종류를 가리킵니다."""),
        code(NAME_CHECK),
        md("""**결과 읽기** — 출력 줄 `오류 종류가 든 모듈: sqlalchemy.exc`와 `SQLAlchemyError를 이어받는가: True`가 보입니다.
출력 줄 `파이썬의 TimeoutError를 이어받는가: False`는 두 오류가 이름만 같다는 뜻입니다.

Ch 16 05절의 재시도 함수는 `except TimeoutError`로 파이썬의 오류를 받았습니다.
`except` 줄은 적은 종류와, 그 종류를 이어받은 종류만 받습니다.
그래서 모듈 이름 없이 적은 `except TimeoutError`로는 이 절의 오류를 받지 못합니다.
그 줄로 받아 보는 셀은 두지 않았고, 위 출력과 파이썬 문서의 규칙으로 판단한 것입니다.

반대로 `from sqlalchemy.exc import TimeoutError`처럼 이름만 가져오면, 파이썬의 `TimeoutError`가 가려집니다.
같은 이름을 새로 가져와 앞의 이름을 쓸 수 없게 되는 일을, 이 교재에서는 「이름 가림」이라고 부릅니다.
게시판에 같은 제목의 새 공지를 겹쳐 붙이면, 아래 공지가 가려 보이지 않는 것과 비슷합니다.
이 절은 모듈째 가져와, 받을 때 `sqlalchemy.exc.TimeoutError`로 적어 이름 가림을 피했습니다."""),
        md("""## 5. 닫지 않고 둔 연결 (Before)

Before 셀은 `async with` 없이 연결을 빌립니다.
메서드 `engine.connect()`를 await로 부르면, 연결 하나를 빌려 이름 `conn`에 담습니다.
조회는 3절과 같지만, 셀이 끝날 때까지 연결을 닫지 않습니다.

실행 전에 예상해 봅니다.
셀이 끝난 뒤 빌려 간 연결 수는 몇일까요?""", lesson_part="before"),
        code(LEAK, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `받은 데이터베이스 이름: ch31_lab`이 보입니다.
조회가 끝났는데도 `빌려 간 연결 수: 1`과 `풀에 쉬고 있는 연결 수: 0`입니다.
연결을 닫지 않아, 풀에 다시 들어가지 않았습니다.
이 값은 변수 `before_checked_out`에 남겨 6절에서 견줍니다.

다음 셀은 다음 요청 하나를 보냅니다.
4절의 함수 `ask_database`로 연결을 빌려 보고, 오류가 나면 이름과 글을 출력합니다.

실행 전에 예상해 봅니다.
다음 요청은 연결을 받을까요?""", lesson_part="before"),
        code(NEXT_REQUEST, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `받은 오류: TimeoutError`가 보입니다.
라벨 `오류 글:` 뒤에는 `QueuePool limit of size 1 overflow 0 reached, connection timed out, timeout 0.20`이 있습니다.
4절에서 첫째 연결을 빌린 채 둘째를 빌릴 때와 같은 오류입니다.
다음 요청은 연결을 받지 못했고, 데이터베이스 이름도 받지 못했습니다.
이것이 이 절의 Before 결함입니다.

4절에서는 첫째 블록이 끝나자 연결이 반납되었습니다.
Before 셀의 연결은 셀이 끝난 뒤에도 빌려 간 채 풀 밖에 있습니다.
다음 셀은 그 연결이 아직 쓸 수 있는 연결인지 봅니다.""", lesson_part="before"),
        code(STILL_OPEN, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `닫지 않은 연결로 받은 이름: ch31_lab`이 보입니다.
라벨 줄 아래 풀 상태는 `Connections in pool: 0`과 `Current Checked out connections: 1`입니다.
닫지 않은 연결은 망가지지 않았고, 서버와 이어진 채 빌려 간 연결로 남아 있습니다.
풀 크기 1을 모두 빌려 주어, 다음 요청에게 줄 연결이 없었던 것입니다.""", lesson_part="before"),
        md("""## 6. 연결을 닫고 async with로 빌리기 (After)

After 쪽 첫 셀은 Before 셀이 닫지 않고 둔 연결을 닫습니다.
메서드 `close()`는 3절에서 블록 끝이 부르던 그 메서드입니다.
풀에서 빌린 연결은 닫으면 풀에 다시 들어갑니다.""", lesson_part="after"),
        code(CLOSE, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `빌려 간 연결 수: 0`과 `풀에 쉬고 있는 연결 수: 1`이 보입니다.
닫은 연결이 풀에 반납되었습니다.

닫는 줄을 잊지 않으려면, 연결을 처음부터 `async with` 블록으로 빌리면 됩니다.
다음 셀은 Before 셀과 같은 조회를 블록 안에서 합니다.
Before 셀과 다른 곳은 연결을 빌리는 줄의 모양과, 연결 수를 담는 변수 이름입니다.""", lesson_part="after"),
        code(FIXED, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `받은 데이터베이스 이름: ch31_lab`과 `빌려 간 연결 수: 0`이 보입니다.
같은 조회를 했는데, 셀이 끝난 뒤 빌려 간 연결이 남지 않았습니다.
블록이 끝날 때 연결을 닫아 풀에 반납했기 때문입니다.

다음 셀은 5절과 같은 다음 요청을 보냅니다.
셀의 코드는 5절의 다음 요청 셀과 글자까지 같습니다.

실행 전에 예상해 봅니다.
이번에는 다음 요청이 연결을 받을까요?""", lesson_part="after"),
        code(NEXT_REQUEST, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `받은 데이터베이스 이름: ch31_lab`이 보입니다.
5절에서 오류를 받았던 같은 셀이, 이번에는 연결을 받아 이름을 받았습니다.
풀의 설정은 바꾸지 않았고, 달라진 것은 빌린 연결을 반납했는지 하나입니다.

다음 셀은 Before 셀과 After 셀이 끝난 뒤의 빌려 간 연결 수를 모아 봅니다.""", lesson_part="after"),
        code(COMPARE, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `Before 셀 뒤 빌려 간 연결 수: 1`과 `After 셀 뒤 빌려 간 연결 수: 0`이 보입니다.
라벨 줄 아래 풀 상태는 `Connections in pool: 1`과 `Current Checked out connections: 0`입니다.
두 셀은 같은 조회를 했고, 다른 것은 연결을 반납했는지 하나였습니다.

## 7. 값 바꿔 보기: 대기 제한

값 하나만 바꿔 봅니다.
바꿀 것은 대기 제한이고, 0.2초 대신 1.0초를 줍니다.
대기 제한은 엔진을 만들 때 정하므로, 지금 엔진의 풀을 비우고 엔진을 새로 만듭니다.
메서드 `dispose()`는 01절처럼 풀에 쉬고 있는 연결을 모두 닫습니다.
그다음 Before 셀처럼 연결 하나를 빌려 닫지 않고 둡니다.""", lesson_part="after"),
        code(VARY, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `대기 제한(초): 1.0`과 `빌려 간 연결 수: 1`이 보입니다.
새 엔진에서도 연결 하나를 빌린 채 닫지 않았습니다.

다음 셀은 5절·6절과 같은 다음 요청을 보냅니다.

실행 전에 예상해 봅니다.
대기 제한이 다섯 배로 길어지면, 다음 요청은 연결을 받을까요?""", lesson_part="after"),
        code(NEXT_REQUEST, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `받은 오류: TimeoutError`가 보입니다.
오류 글 끝이 `timeout 1.00`으로 바뀌었고, 나머지는 5절의 오류 글과 같습니다.
대기 제한을 늘려도, 기다리는 동안 닫지 않은 연결은 반납되지 않았습니다.
걸린 시간은 재지 않았고, 출력에서 달라진 것은 오류 글 끝의 대기 제한 값뿐입니다.

## 8. 정리: 연결 닫기와 풀 비우기

다음 셀은 7절에서 닫지 않고 둔 연결을 닫고, 엔진의 풀을 비웁니다.
노트북을 다시 실행해도 빌려 간 연결이 남지 않게 하려는 것입니다.""", lesson_part="after"),
        code(CLEANUP, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `닫은 뒤 빌려 간 연결 수: 0`과 `풀을 비운 뒤 쉬고 있는 연결 수: 0`이 보입니다.
이 노트북은 표를 만들지 않아, 서버에 남긴 것이 없습니다.
처음부터 다시 실행하면 2절이 엔진을 새로 만들어 같은 출력이 나옵니다.

## 정리

1. 풀에 둘 연결 수가 1인 엔진에서 연결 하나를 빌린 채 둘째를 빌리자, `TimeoutError`를 받았습니다.
2. 빌린 연결을 닫지 않고 두자, 다음 요청이 대기 제한 0.2초 안에 연결을 받지 못했습니다.
3. 연결을 닫거나 `async with` 블록으로 빌리자 빌려 간 연결이 0이 되어, 다음 요청이 이름을 받았습니다.

05절에서는 같은 PostgreSQL 서버에 검색 문서 표와 체크포인터 표를 함께 두고, 백업과 복원을 해 봅니다.""", lesson_part="after"),
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
    """노트북용 마크다운 한 단락(백틱·줄바꿈)을 _src 문단 글로 바꿉니다(01·02절 생성기와 같은 함수)."""
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


L_CH02_05 = "../../part1/ch02-python/05-파일과-예외.html"
L_CH16_05 = "../../part4/ch16-guardrails/05-재시도-폴백과-감사-로그.html"
L_CH30_02 = "../ch30-fastapi-serving/02-의존성으로-Agent-주입.html"
L_01 = "01-SQLAlchemy-비동기-PostgreSQL.html"
L_02 = "02-트랜잭션과-원자성.html"
L_03 = "03-Alembic-적용과-롤백.html"
L_05 = "05-pgvector-체크포인터-공존과-백업.html"

TERM_ROWS = [
    ("대기 제한(<code>pool_timeout</code>)", "풀에 빌려 줄 연결이 없을 때, 새 요청이 반납을 기다리는 초의 한도입니다. 공용 자전거 거치대에서 반납을 기다리다, 정해 둔 시간이 지나면 기다림을 그만두는 것과 같습니다. 이 절에서는 <code>pool_timeout=0.2</code>이고, 오류 글 끝에 <code>timeout 0.20</code>으로 적혔습니다."),
    ("반납", "빌린 연결을 닫아 풀에 다시 넣는 일입니다. 공용 자전거를 다 탄 뒤 거치대에 다시 세워 두는 것과 같습니다. 이 절에서는 <code>await conn.close()</code> 한 줄이나 <code>async with</code> 블록의 끝이 반납입니다."),
    ("이름 가림", "같은 이름을 새로 가져오거나 만들어, 앞에 있던 같은 이름을 쓸 수 없게 되는 일입니다. 게시판에 같은 제목의 새 공지를 겹쳐 붙이면 아래 공지가 가려지는 것과 같습니다. 이 절에서 <code>from sqlalchemy.exc import TimeoutError</code>를 쓰면 파이썬의 <code>TimeoutError</code>가 가려지므로, 모듈째 가져와 <code>sqlalchemy.exc.TimeoutError</code>로 적었습니다."),
]

COMPARE_ROWS = [
    ("연결을 빌린 줄", "<code>conn = await engine.connect()</code>", "<code>async with engine.connect() as conn:</code>"),
    ("받은 데이터베이스 이름", "<code>ch31_lab</code>", "<code>ch31_lab</code>"),
    ("셀 뒤 빌려 간 연결 수", "<code>1</code>", "<code>0</code>"),
    ("셀 뒤 풀에 쉬고 있는 연결 수", "<code>0</code>", "<code>1</code>"),
    ("다음 요청이 받은 것", "<code>받은 오류: TimeoutError</code>", "<code>받은 데이터베이스 이름: ch31_lab</code>"),
]

B4_ANALOGY = ("<p>옛 전화 교환대 한 대를 떠올려 봅니다. 교환대에는 세워 둔 판과, 그 아래 앞으로 누운 선반이 있습니다. "
              "판에는 선을 꽂는 자리가 하나 있고, 선반에는 선 끝을 세워 두는 받침 구멍이 하나 있습니다. 선은 한 가닥뿐입니다. "
              "쓰지 않을 때는 선 끝을 받침 구멍에 세워 두고, 통화를 이을 때 뽑아 판의 자리에 꽂습니다.</p>"
              "<p>같은 교환대 둘을 나란히 놓습니다. 왼쪽 교환대는 선이 판의 자리에 꽂힌 채이고, 받침 구멍은 비어 있습니다. "
              "오른쪽 교환대는 선 끝이 받침 구멍에 세워져 있고, 판의 자리는 비어 있습니다.</p>"
              "<p>선 한 가닥이 연결 하나이고, 교환대 한 대가 풀 크기 1인 연결 풀입니다. 받침에 세워 둔 선은 풀에 쉬고 있는 연결이고, 판에 꽂힌 선은 빌려 간 연결입니다. "
              "왼쪽은 통화가 끝났는데도 선을 뽑지 않은 Before 셀의 모습이라, 다음 통화에 쓸 선이 받침에 없습니다. "
              "오른쪽은 선을 받침에 다시 세워 둔 After 셀의 모습입니다.</p>"
              "<p>비유와 다른 점이 있습니다. 실제 연결은 받침에 있든 판에 꽂혔든 서버와 이어져 있습니다. "
              "<a href=\"" + L_01 + "\">01절</a> 비유에서 켜진 불로 보인 그 이어짐은, 이 그림에서는 그리지 않았습니다.</p>")

LOOK_B5 = "노트북 3절에서 <code>블록 안 - 빌려 간 연결 수: 1</code>과 <code>블록 밖 - 빌려 간 연결 수: 0</code>을 봅니다. 4절에서 <code>받은 오류: TimeoutError</code>와 오류 글 끝의 <code>timeout 0.20</code>을 찾습니다. 같은 4절의 <code>파이썬의 TimeoutError를 이어받는가: False</code>도 확인합니다."
LOOK_B6 = "Before 셀에서 <code>빌려 간 연결 수: 1</code>과, 다음 요청의 <code>받은 오류: TimeoutError</code>를 봅니다. After 쪽에서 <code>빌려 간 연결 수: 0</code>과 <code>받은 데이터베이스 이름: ch31_lab</code>을 확인합니다. 7절 오류 글 끝의 <code>timeout 1.00</code>도 찾습니다."


def src_html() -> str:
    terms = table_html(["말", "뜻"], TERM_ROWS)
    compare = table_html(["견준 것", "Before 셀(닫지 않음)", "After 셀(async with)"], COMPARE_ROWS)
    return """<!--meta: 강의 1h | 실습 2h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>풀 크기와 대기 제한을 정한 엔진에서, 빌려 간 연결 수와 풀 상태를 출력으로 읽을 수 있습니다.</li>
<li>빌린 연결을 닫지 않고 두면, 다음 요청이 <code>sqlalchemy.exc.TimeoutError</code>를 받는 것을 재현할 수 있습니다.</li>
<li>연결을 닫거나 <code>async with</code> 블록으로 빌려, 다음 요청이 다시 연결을 받는 것을 확인할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>에이전트 서비스는 요청이 올 때마다 데이터베이스 연결을 빌려, 대화 기록이나 상태를 읽고 씁니다. 연결 풀이 한 번에 빌려 줄 수 있는 연결의 수는 정해져 있습니다. 한 요청이 빌린 연결을 반납하지 않으면, 서버가 멀쩡해도 다음 요청이 연결을 받지 못합니다. 이 절은 그 장면을 풀 크기가 1인 엔진에서 일부러 만들고 고칩니다.</p><p>절 제목의 커넥션 풀(connection pool)은 <a href=\"""" + L_01 + """\">01절</a>에서 본 연결 풀입니다. 제목의 고갈은 풀에 빌려 줄 연결이 하나도 남지 않은 상태를 말합니다. 이 교재 본문에서는 「빌려 줄 연결이 없다」고 적습니다. 제목의 대응은 빌린 연결을 반납하도록 코드를 고치는 일입니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_01 + """\">01절</a>에서는 비동기 엔진을 만들 때 인자 <code>pool_size</code>와 <code>max_overflow</code>로 연결 풀의 크기를 정했습니다. 블록 <code>async with engine.connect()</code>로 빌린 연결은 블록이 끝나자 풀에 다시 들어갔습니다. 메서드 <code>checkedin()</code>과 <code>checkedout()</code>으로 쉬고 있는 연결과 빌려 간 연결을 셌습니다. 함께 기다린 실행은 풀에 둘 연결 수와 같은 셋을 한꺼번에 빌렸습니다. 이 절은 풀에 둘 연결 수보다 많이 빌리려 할 때를 봅니다.</p><p><a href=\"""" + L_02 + """\">02절</a>에서는 블록 하나가 한 묶음 작업이고, 받은 오류를 <code>try</code>로 받아 이름과 코드를 출력했습니다. <a href=\"""" + L_03 + """\">03절</a>은 Alembic으로 표 구조를 판마다 바꿨고, 그 끝에서 이 절을 예고했습니다. 이 절의 오류 받기는 02절 모양을 따르고, <a href=\"""" + L_CH02_05 + """\">Ch 2 05절</a>의 <code>try</code>와 <code>except</code>를 씁니다.</p><p><a href=\"""" + L_CH30_02 + """\">Ch 30 02절</a>에서는 첫 테스트가 적은 재정의를 지우지 않아, 다음 테스트까지 504를 받았습니다. 재정의 딕셔너리를 비우자 다음 테스트가 200을 받았습니다. 이 절의 Before도 같은 모양입니다. 앞 요청이 반납하지 않은 연결 때문에, 다음 요청이 연결을 받지 못합니다.</p><p><a href=\"""" + L_CH16_05 + """\">Ch 16 05절</a>의 재시도 함수는 <code>except TimeoutError</code>로 파이썬의 오류를 받았습니다. 이 절에서 받을 오류도 이름이 <code>TimeoutError</code>이지만, 다른 오류입니다. 그래서 받을 때 모듈 이름을 붙여 적습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3>""" + B4_ANALOGY + """
""" + illustration_block() + """<h3>풀의 크기와 대기 제한</h3><p>연결 풀은 인자 <code>pool_size</code>만큼 연결을 두고, 인자 <code>max_overflow</code>만큼 더 만들 수 있습니다. 빌려 간 연결이 두 수의 합에 이르면, 풀에 빌려 줄 연결이 없습니다. 그때 새 요청은 빌려 간 연결 하나가 반납되기를 기다립니다. 인자 <code>pool_timeout</code>이 그 기다림의 한도이고, 이 교재에서는 대기 제한이라고 부릅니다.</p><p>대기 제한 안에 반납이 없으면, 풀은 오류 <code>sqlalchemy.exc.TimeoutError</code>를 냅니다. 오류 글에는 풀 크기·더 만들 연결 수·대기 제한이 적힙니다. 인자를 적지 않으면 풀 크기 5·더 만들 연결 10·대기 제한 30초라고 SQLAlchemy 문서가 적습니다. <a href=\"""" + L_02 + """\">02절</a>의 <code>풀에 둘 연결 수: 5</code>가 그 기본값이었습니다.</p><p>연결을 반납하는 방법은 둘입니다. 연결의 메서드 <code>close()</code>를 부르거나, 연결을 <code>async with</code> 블록으로 빌리는 것입니다. 블록이 끝날 때도 <code>close()</code>가 불립니다. 풀에서 빌린 연결은 닫아도 서버와 끊기지 않고, 풀에 다시 들어갑니다.</p>
""" + terms + """
<p>새 말을 이 절 코드에서 보면 이렇습니다. 엔진은 <code>대기 제한(초): 0.2</code>를 출력했고, 받은 오류 글은 <code>timeout 0.20</code>으로 끝났습니다. 블록이 끝나 반납하자 <code>블록 밖 - 빌려 간 연결 수: 0</code>이 되었습니다. 받은 오류의 모듈은 <code>sqlalchemy.exc</code>였습니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>받은 오류의 이름 가르기</h3><p>이 절에서 받은 오류의 이름은 <code>TimeoutError</code>이고, 모듈 <code>sqlalchemy.exc</code>에 있습니다. 파이썬에도 같은 이름의 오류가 들어 있습니다. 노트북 4절 출력에서 SQLAlchemy의 오류는 파이썬의 오류를 이어받지 않았습니다. 파이썬 문서는 <code>except</code> 줄이 적은 종류와 그 종류를 이어받은 종류만 받는다고 적습니다.</p><p>그래서 모듈 이름 없이 <code>except TimeoutError</code>라고 적으면 이 절의 오류를 받지 못합니다. 그 줄로 받아 보는 장면은 노트북에서 실행하지 않았습니다. 반대로 <code>from sqlalchemy.exc import TimeoutError</code>로 이름만 가져오면, 그 뒤의 <code>TimeoutError</code>는 SQLAlchemy의 오류를 가리킵니다. 이 절은 <code>import sqlalchemy.exc</code>로 모듈째 가져오고, 받을 때 <code>sqlalchemy.exc.TimeoutError</code>로 적었습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 01절과 같은 접속 글로, 풀 크기 1·더 만들 연결 0·대기 제한 0.2초인 엔진을 만듭니다. 3절은 연결을 빌려 데이터베이스 이름을 묻고, 블록 안과 밖의 연결 수와 풀 상태를 봅니다. 4절은 다음 요청이 할 일을 함수로 만들고, 연결 하나를 빌린 채 둘째를 빌려 받은 오류를 읽습니다.</p><p>모델 요청은 0번이고, API 키 없이 실행합니다. 데이터베이스 서버는 01절과 같은 Docker 컨테이너 <code>kdt-ch31-postgres</code>입니다. 표를 만들지 않고, 작업 폴더에 파일을 쓰지 않습니다. 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """|example}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>일부러 실패해 보기</h2><p>아래 Before 셀은 <code>async with</code> 없이 연결을 빌리고, 조회만 한 뒤 닫지 않습니다. 이어서 4절의 함수 <code>ask_database</code>로 다음 요청을 보냅니다. After 쪽은 먼저 그 연결을 닫고, 같은 조회를 <code>async with</code> 블록 안에서 합니다. 다음 요청 셀은 Before와 After에서 글자까지 같습니다.</p>
{{notebook:""" + SLUG + """|failure}}
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + compare + """
<p>두 셀은 같은 엔진으로 같은 조회를 했고, 받은 이름도 <code>ch31_lab</code>으로 같았습니다. 다른 것은 셀이 끝난 뒤 연결을 반납했는지 하나였습니다. 그 차이가 다음 요청의 결과를 갈랐습니다.</p><p>Before 셀의 연결은 조회가 끝난 뒤에도 빌려 간 채 남았습니다. 풀 크기가 1이라, 다음 요청에게 빌려 줄 연결이 없었습니다. 다음 요청은 대기 제한 0.2초 안에 연결을 받지 못해 <code>TimeoutError</code>를 받았습니다. 닫지 않은 연결로는 조회가 여전히 되었으므로, 서버나 연결이 망가진 것은 아닙니다.</p><p>After 쪽은 먼저 <code>await conn.close()</code>로 연결을 닫아, 쉬고 있는 연결을 1로 만들었습니다. 같은 조회를 <code>async with</code> 블록으로 한 뒤에도 빌려 간 연결은 0이었습니다. 같은 다음 요청 셀이 이번에는 <code>받은 데이터베이스 이름: ch31_lab</code>을 받았습니다.</p><p>노트북 7절에서는 대기 제한만 1.0초로 바꾸고, 다시 연결을 닫지 않고 두었습니다. 다음 요청은 또 <code>TimeoutError</code>를 받았고, 오류 글 끝만 <code>timeout 1.00</code>으로 바뀌었습니다. 기다리는 동안 반납하는 코드가 없으면, 대기 제한을 늘려도 연결은 오지 않습니다.</p><p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>대기 제한을 늘리거나 풀을 키우면, 오류가 늦게 나거나 덜 날 수 있습니다. 그러나 반납하지 않는 코드가 있으면, 빌려 간 연결이 쌓여 결국 같은 오류를 받습니다. 노트북 밖에서 풀 크기를 2로 두고 연결 하나를 닫지 않자, 다음 요청은 연결을 받았습니다. 연결 하나를 더 닫지 않고 두자, 그다음 요청이 <code>QueuePool limit of size 2</code>로 시작하는 오류를 받았습니다.</li><li>Before 셀만 두 번 실행하면, 둘째 실행의 <code>await engine.connect()</code> 줄이 <code>TimeoutError</code>를 받습니다. 첫째 실행이 빌린 연결이 아직 반납되지 않았기 때문입니다. 이 장면은 노트북 밖에서 확인했습니다. 새 커널로 처음부터 차례로 실행하면 교재와 같은 출력이 나옵니다.</li><li>함수 안에서 연결을 빌리고 닫지 않은 채 함수가 끝나도, 연결은 빌려 간 채로 남습니다. 노트북 밖에서 확인하자, 함수가 끝난 직후 빌려 간 연결은 1이었습니다. 파이썬의 쓰레기 수거(garbage collection)를 직접 부른 뒤에야 0이 되었습니다. 쓰레기 수거는 더 쓰지 않는 객체를 파이썬이 스스로 치우는 일입니다.</li><li>오류 출력(stderr)에 찍힌 경고 글은 그 연결을 끊는다고 적었습니다. SQLAlchemy 문서도 비동기 드라이버에서는 이렇게 치워지는 반납을 지원하지 않는다고 적습니다. 반납은 코드에서 직접 합니다.</li><li>닫지 않은 연결은 서버 쪽에서 한 묶음 작업이 열린 채였습니다. 노트북 밖에서 서버의 연결 목록 <code>pg_stat_activity</code>를 보자, 그 연결의 상태는 <code>idle in transaction</code>이었습니다. 라이브러리 SQLAlchemy는 연결로 첫 SQL 글을 보낼 때 한 묶음 작업을 저절로 시작합니다. 연결을 닫아 반납하자 풀이 그 작업을 취소했고, 상태는 <code>idle</code>이 되었습니다.</li><li>서비스 프로세스가 여럿이면 연결 풀도 프로세스마다 하나씩 있습니다. 프로세스마다 풀 크기와 더 만들 연결 수를 더한 값의 합이, 서버가 받는 연결 수 안에 들어가야 합니다. 이 기기 서버의 설정 <code>max_connections</code>는 <code>100</code>이었고, PostgreSQL 문서도 보통 100이라고 적습니다. 여러 프로세스를 띄우는 장면은 실행하지 않았습니다.</li><li>4절처럼 연결을 겹쳐 빌려야 하는 코드라면, 인자 <code>max_overflow</code>를 1로 둘 수 있습니다. 노트북 밖에서 확인하자 둘째 연결도 받았고, 풀 상태 글은 <code>Current Overflow: 1 Current Checked out connections: 2</code>였습니다. 둘을 반납한 뒤에는 쉬고 있는 연결이 1로 남았습니다.</li><li>한 작업이 연결을 쥔 동안 다른 작업이 연결을 빌리는 장면은, 결과가 쥔 시간과 대기 제한에 따라 갈립니다. 함수 <code>asyncio.create_task</code>는 코루틴을 기다리지 않고 이벤트 루프에 맡겨, 다음 줄과 함께 진행되게 합니다. 노트북 밖에서 이 함수로 두 작업을 함께 진행해, 조건마다 다섯 번씩 보았습니다.</li><li>첫 작업이 0.6초 쥐고 대기 제한이 0.2초면 다섯 번 모두 <code>TimeoutError</code>였습니다. 0.3초 쥐고 대기 제한이 1.0초면 다섯 번 모두 이름을 받았습니다. 기다린 시간에 기대는 장면이라, 노트북에서는 실행하지 않았습니다.</li><li>노트북을 쓰기 전에 노트북 밖에서 같은 장면을 파이썬 파일로 다섯 번 실행했고, 출력이 다섯 번 모두 같았습니다. 연결 수·풀 상태 글·오류 글 모두 실행할 때마다 같은 값입니다.</li><li>교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다. 그 서버는 Docker 컨테이너가 아니라 같은 접속 글로 켠 서버입니다. Docker 이미지로 켜면 버전 번호의 끝자리가 다를 수 있습니다. SQLAlchemy 문서는 2.0.54 버전이고, 교재 출력은 설치된 2.0.43 버전으로 만들었습니다. 다른 버전과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>풀 크기가 1인 엔진에서 연결 하나를 빌린 채 둘째를 빌리자, <code>sqlalchemy.exc.TimeoutError</code>를 받았습니다.</li><li>빌린 연결을 닫지 않고 두자 빌려 간 연결이 1로 남아, 다음 요청이 대기 제한 안에 연결을 받지 못했습니다.</li><li>연결을 닫거나 <code>async with</code> 블록으로 빌리자 빌려 간 연결이 0이 되어, 같은 다음 요청이 이름을 받았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_05 + """\">05절</a>에서는 같은 PostgreSQL 서버에 검색 문서 표와 체크포인터 표를 함께 둡니다. 그 서버에서 백업과 복원을 해 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. 엔진을 <code>pool_size=1, max_overflow=0, pool_timeout=0.2</code>로 만들었습니다. 세 인자는 각각 무엇을 정하나요?</p><p class="quiz-a">풀에 둘 연결 수, 그 밖에 더 만들 연결 수, 빌려 줄 연결이 없을 때 기다릴 초입니다. 마지막 값을 이 교재에서는 대기 제한이라고 부릅니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">2. Before 셀이 끝난 뒤 빌려 간 연결 수와 쉬고 있는 연결 수는 무엇이었고, 다음 요청은 무엇을 받았나요?</p><p class="quiz-a">빌려 간 연결은 1, 쉬고 있는 연결은 0이었습니다. 다음 요청은 <code>TimeoutError</code>를 받았습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">3. After 쪽에서 다음 요청이 연결을 받게 한 줄은 무엇인가요? 풀의 설정을 바꿨나요?</p><p class="quiz-a">줄 <code>await conn.close()</code>로 닫지 않은 연결을 닫았고, 같은 조회는 <code>async with</code> 블록으로 했습니다. 풀의 설정은 바꾸지 않았습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">4. 대기 제한을 1.0초로 바꾸고 연결을 닫지 않고 두자, 다음 요청은 무엇을 받았나요?</p><p class="quiz-a">같은 <code>TimeoutError</code>를 받았고, 오류 글 끝만 <code>timeout 1.00</code>으로 바뀌었습니다. 기다리는 동안 연결을 반납하는 코드가 없었기 때문입니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">5. 동료가 모듈 이름 없이 <code>except TimeoutError:</code>로 이 절의 오류를 받으려 합니다. 받을 수 있나요?</p><p class="quiz-a">받을 수 없습니다. 모듈 이름 없이 적은 <code>TimeoutError</code>는 파이썬의 오류이고, SQLAlchemy의 오류는 그것을 이어받지 않았습니다. 그 줄로 받아 보지는 않았고, 4절 출력과 파이썬 문서의 규칙에서 나온 답입니다. 모듈 이름을 붙여 <code>except sqlalchemy.exc.TimeoutError</code>로 적습니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.sqlalchemy.org/en/20/core/pooling.html">SQLAlchemy Connection Pooling</a></div>확인 2026-09-29 · 문서 2.0.54 · 인자 <code>pool_size</code>·<code>max_overflow</code>·<code>pool_timeout</code>의 기본값은 5·10·30초라고 적습니다. 연결을 닫으면 끊지 않고 풀에 다시 넣는다고 적습니다. 비동기 엔진은 따로 정하지 않으면 <code>AsyncAdaptedQueuePool</code>을 쓴다고 적습니다. 쓰레기 수거로 치워지는 반납은 비동기 드라이버에서 지원하지 않는다고 적습니다.</li><li><div><a href="https://docs.sqlalchemy.org/en/20/errors.html#error-3o7r">SQLAlchemy Error Messages · QueuePool limit … reached</a></div>확인 2026-09-29 · 오류 글 끝의 주소가 가리키는 설명입니다. 흔한 까닭으로 빌려 간 연결을 반납하지 않고 열어 두는 것을 듭니다. 쓰레기 수거로 치워지는 반납에는 기댈 수 없다고 적습니다. 메서드 <code>close()</code>를 부르거나 <code>with</code> 블록을 쓰라고 합니다.</li><li><div><a href="https://docs.sqlalchemy.org/en/20/core/exceptions.html">SQLAlchemy Core Exceptions</a></div>확인 2026-09-29 · 오류 <code>TimeoutError</code>는 풀에서 연결을 얻다가 시간이 다 되면 난다고 적습니다. 이어받는 종류는 <code>SQLAlchemyError</code>입니다.</li><li><div><a href="https://docs.sqlalchemy.org/en/20/core/connections.html">SQLAlchemy Working with Engines and Connections</a></div>확인 2026-09-29 · 연결로 첫 SQL 글을 보내면 한 묶음 작업이 저절로 시작된다고 적습니다. 연결이 풀에 반납될 때 풀이 그 작업을 취소한다고 적습니다.</li><li><div><a href="https://docs.python.org/3/tutorial/errors.html">Python Tutorial · Errors and Exceptions</a></div>확인 2026-09-29 · 문서 3.14.7 · 줄 <code>except</code>는 적은 종류와 그 종류를 이어받은 종류만 받는다고 적습니다.</li><li><div><a href="https://docs.python.org/3/library/exceptions.html">Python Built-in Exceptions</a></div>확인 2026-09-29 · 파이썬의 <code>TimeoutError</code>는 운영체제 수준의 시간 초과이고, <code>OSError</code>를 이어받는다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/runtime-config-connection.html">PostgreSQL 17 Connections and Authentication</a></div>확인 2026-09-29 · 설정 <code>max_connections</code>는 서버가 함께 받는 연결 수의 한도이고, 기본값은 보통 100이라고 적습니다. 서버를 켤 때만 정할 수 있다고 적습니다.</li><li>설치판 sqlalchemy 2.0.43 소스 <code>pool/impl.py</code> 74~76행은 세 인자의 기본값 5·10·30.0입니다. 166~171행은 빌려 줄 연결이 없을 때 오류 글과 코드 <code>3o7r</code>을 붙여 <code>TimeoutError</code>를 냅니다. 230~256행은 <code>status()</code>·<code>size()</code>·<code>timeout()</code>·<code>checkedin()</code>·<code>checkedout()</code>이고, 259행이 <code>AsyncAdaptedQueuePool</code>입니다.</li><li>설치판 <code>exc.py</code> 287~288행은 <code>TimeoutError</code>가 <code>SQLAlchemyError</code>만 이어받는 자리입니다. <code>ext/asyncio/engine.py</code> 475~482행은 연결의 <code>close()</code>가 열린 한 묶음 작업도 취소한다고 적습니다. 894~896행은 <code>async with</code> 블록이 끝날 때 <code>close()</code>를 부르는 자리입니다. <code>pool/base.py</code> 1016~1025행은 쓰레기 수거가 반납하지 않은 연결을 치울 때의 경고 글입니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    # 2절 설정 셀은 01절 셀 글 그대로(「01절 2절의 설정 셀과 글자까지 같은 셀」 문장의 근거)
    assert SETTINGS in AUTHOR01.read_text(encoding="utf-8"), "SETTINGS가 01절 셀과 다릅니다"
    # 다음 요청 셀은 5·6·7절 세 곳이 같은 상수(「글자까지 같습니다」 문장의 근거)
    request_cells = 0
    for cell in cells():
        if cell["cell_type"] == "code" and "".join(cell["source"]) == NEXT_REQUEST:
            request_cells = request_cells + 1
    assert request_cells == 3, "다음 요청 셀이 세 곳이 아닙니다"
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "04", SLUG, "paired", cells())
        print("wrote", path)
