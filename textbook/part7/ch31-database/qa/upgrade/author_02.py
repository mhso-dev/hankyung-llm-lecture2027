"""Ch 31 02절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§5-3·§6 paired).

사용:
  python3 -B author_02.py            → 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_02.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
이후 run_section.sh 가 pre_exec.sh(PostgreSQL 켜기) → 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **paired 형식 유지**. 슬러그 `02-트랜잭션과-원자성` 그대로.

## 결정 1 — paired: Before = CHECK 위반(실제 결함, handoff §01 → §02 2), After = 한 begin 블록

표 ch31_tx.accounts(id int PRIMARY KEY, balance int CHECK (balance >= 0)) 500·500.
Before 함수 transfer_two_blocks(더하기·빼기를 begin 블록 둘에 하나씩) → 1번에서 2번으로 600 → 첫 블록(2번 +600) 확정 →
둘째 블록(1번 −600)이 IntegrityError·SQLSTATE 23514·accounts_balance_check로 막힘(받은 오류 노랑) →
[(1, 500), (2, 1100)] 합계 1600(받은 결함 결과 — 빨강). After 함수 transfer_one_block(4절 예시에서 정의한 한 블록) →
같은 오류 → [(1, 500), (2, 500)] 합계 1000(노랑). 블록 안에서 읽은 2번 잔액 1100 → 블록 밖 500(취소를 처음 보임 — 01 3절 약속).
값 바꿔 보기 = 보낼 돈만 500 → [(1, 0), (2, 1000)](CHECK >= 0, 오류 없음). 옛 판 「코드가 직접 던진 RuntimeError」 장면은 쓰지 않는다.
노트북 밖 /tmp/ch31-02/exp/p1_scene.py 5/5 같음(빼기 먼저 두 블록 → 첫 블록에서 막혀 500·500 — b7).
받는 계좌에 먼저 더하는 차례는 Before 결함이 출력에 보이게 정한 예(규격 §3 — b7에 밝힘).

## 결정 2 — 말(handoff 「뒤 절이 정할 말」)

트랜잭션 → 「한 묶음 작업(트랜잭션)」(Ch 23 금지어 — 절 제목에만 원어, 본문 첫 자리 괄호) · 커밋 → 「확정(커밋)」(Ch 4 03 이음) ·
롤백 → 「취소(롤백)」(03 제목의 롤백 = 판 내리기와 다른 뜻을 한 문장) · 원자성은 제목 말(뜻 → 계약서 예 → 코드) ·
CHECK 제약·오류 코드(SQLSTATE)는 첫 풀이 한 문장씩(Ch 4 03 「제약(constraint)」·sqlite3.IntegrityError 이음). 「되돌」·「돌려」 0.

## 결정 3 — 접속·이름 공간(handoff 챕터 공통 2·§01 → §02 7)

설정 셀 SETTINGS = author_01.SETTINGS 글자 그대로(__main__에서 문자열 대조). 엔진은 풀 인자 없이(기본 5 — 한 문장).
이름 공간 ch31_tx를 3절에서 지우고 다시 만들고, 8절에서 지운 뒤 to_regnamespace → None·dispose(두 번 실행해도 같은 출력).
오류 출력은 매번 같은 것만: type(error).__name__ · error.orig.sqlstate · 드라이버 오류 글 error.orig(서버 주소·PID·시각 없음 확인).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·대입 풀기·별표 풀기·`while`·
세미콜론·`isinstance`·클래스·데코레이터·ORM·`AsyncSession`·`os.environ`·`create_task`·가짜 모델. `try`는 `except IntegrityError as error`만(Ch 2 05).
async def 셋(read_balances·transfer_one_block·transfer_two_blocks) + def 하나(add_balances), 셀당 하나. 호출 깊이 2 이하.
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
SLUG = "02-트랜잭션과-원자성"
TITLE_TEXT = "트랜잭션과 원자성"
SRC = ROOT / "textbook/part7/ch31-database/_src" / (SLUG + ".html")
AUTHOR01 = ROOT / "textbook/part7/ch31-database/qa/upgrade/author_01.py"
RUNS_SENTENCE = os.environ.get("AUTHOR02_RUNS_SENTENCE", "새 커널로 두 번 실행해 견주자, 코드 셀 스물셋의 출력이 셀마다 모두 같았습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 모델을 부르지 않아, 이 절의 출력은 서버에 남은 잔액과 받은 오류로 정해집니다.")

# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["sqlalchemy[asyncio]==2.0.43", "asyncpg==0.30.0"])

IMPORTS = r'''# SQL 글·받을 오류 이름·비동기 엔진에 쓸 이름을 가져옵니다
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine

print("가져온 이름:", "text", "IntegrityError", "create_async_engine")'''

SETTINGS = r'''# 데이터베이스 접속 글을 정합니다(비밀번호 postgres는 이 실습에서만 쓰는 연습용 값입니다)
database_url = "postgresql+asyncpg://postgres:postgres@127.0.0.1:55431/ch31_lab"
# 비밀번호가 찍히지 않게, 글을 @에서 나눠 앞의 드라이버 부분과 뒤의 서버 부분만 출력합니다
url_parts = database_url.split("@")
print("드라이버 부분:", database_url.split("://")[0])
print("서버 주소와 데이터베이스:", url_parts[1])'''

ENGINE = r'''# 접속 글로 비동기 엔진을 만듭니다(풀 인자를 적지 않아 SQLAlchemy가 정한 기본값을 씁니다)
engine = create_async_engine(database_url)
print("엔진의 종류:", type(engine).__name__)
print("풀에 둘 연결 수:", engine.pool.size())'''

PREPARE = r'''# 이름 공간 ch31_tx를 지우고 다시 만든 뒤, 표 accounts에 계좌 두 줄을 넣습니다
# CHECK (balance >= 0)은 잔액 칸이 0 이상이어야 한다는 조건이고, 어기는 줄은 서버가 막습니다
table_sql = "CREATE TABLE ch31_tx.accounts (id int PRIMARY KEY, balance int CHECK (balance >= 0))"
insert_sql = "INSERT INTO ch31_tx.accounts VALUES (1, 500), (2, 500)"
async with engine.begin() as conn:
    await conn.execute(text("DROP SCHEMA IF EXISTS ch31_tx CASCADE"))
    await conn.execute(text("CREATE SCHEMA ch31_tx"))
    await conn.execute(text(table_sql))
    inserted = await conn.execute(text(insert_sql))
print("넣은 줄 수:", inserted.rowcount)'''

DEF_READ = r'''# 두 계좌의 번호와 잔액을 번호 차례로 읽어, 줄 목록을 내놓습니다(연결 하나를 빌렸다가 풀에 다시 넣습니다)
async def read_balances():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT id, balance FROM ch31_tx.accounts ORDER BY id"))
        rows = result.fetchall()
    return rows'''

DEF_ADD = r'''# 줄 목록을 받아 잔액을 모두 더한 합계를 내놓습니다(줄의 칸 값은 row.balance처럼 칸 이름으로 꺼냅니다)
def add_balances(rows):
    total = 0
    for row in rows:
        total = total + row.balance
    return total'''

SHOW_START = r'''# 처음 잔액과 합계를 봅니다(합계는 뒤에서 견줄 기준으로 남겨 둡니다)
rows = await read_balances()
start_total = add_balances(rows)
print("잔액:", rows)
print("합계:", start_total)'''

UPDATE_SQL = r'''# 잔액을 바꾸는 SQL 글 둘을 객체로 만듭니다(계좌 번호와 금액이 들어갈 자리를 둡니다)
# UPDATE는 WHERE 조건에 맞는 줄에서, SET 뒤에 적은 칸 값을 바꿉니다
deposit_sql = text("UPDATE ch31_tx.accounts SET balance = balance + :amount WHERE id = :id")
withdraw_sql = text("UPDATE ch31_tx.accounts SET balance = balance - :amount WHERE id = :id")
print("더하는 SQL 글:", deposit_sql)
print("빼는 SQL 글:", withdraw_sql)'''

DEF_ONE = r'''# 받는 계좌에 더하기와 보내는 계좌에서 빼기를 begin 블록 하나에 함께 넣은 이체 함수를 정의합니다
async def transfer_one_block(from_id, to_id, amount):
    async with engine.begin() as conn:
        await conn.execute(deposit_sql, {"id": to_id, "amount": amount})
        await conn.execute(withdraw_sql, {"id": from_id, "amount": amount})'''

TRANSFER_100 = r'''# 1번 계좌에서 2번 계좌로 100을 한 블록으로 보내고, 잔액과 합계를 봅니다
await transfer_one_block(1, 2, 100)
rows = await read_balances()
print("잔액:", rows)
print("합계:", add_balances(rows))'''

DEF_TWO = r'''# Before: 더하기와 빼기를 begin 블록 둘에 하나씩 넣어, 블록마다 따로 확정하는 이체 함수를 정의합니다
async def transfer_two_blocks(from_id, to_id, amount):
    async with engine.begin() as conn:
        await conn.execute(deposit_sql, {"id": to_id, "amount": amount})
    async with engine.begin() as conn:
        await conn.execute(withdraw_sql, {"id": from_id, "amount": amount})'''

RESET = r'''# 두 계좌의 잔액을 모두 500으로 다시 맞추고, 잔액을 봅니다
async with engine.begin() as conn:
    reset = await conn.execute(text("UPDATE ch31_tx.accounts SET balance = 500"))
print("다시 500으로 맞춘 줄 수:", reset.rowcount)
rows = await read_balances()
print("잔액:", rows)'''

BEFORE_CALL = r'''# 1번에서 2번으로 600을 블록 둘로 보내 보고, 오류가 나면 받은 오류의 이름·코드·글을 출력합니다
try:
    await transfer_two_blocks(1, 2, 600)
except IntegrityError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 코드(SQLSTATE):", error.orig.sqlstate)
    print("드라이버가 받은 오류 글:")
    print(error.orig)'''

SHOW_BEFORE = r'''# Before 판의 이체가 끝난 뒤, 잔액과 합계를 봅니다
rows = await read_balances()
before_total = add_balances(rows)
print("잔액:", rows)
print("합계:", before_total)'''

AFTER_CALL = r'''# After: 같은 600을 한 블록으로 보내 보고, 오류가 나면 받은 오류의 이름과 코드를 출력합니다
try:
    await transfer_one_block(1, 2, 600)
except IntegrityError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 코드(SQLSTATE):", error.orig.sqlstate)'''

SHOW_AFTER = r'''# After 판의 이체가 끝난 뒤, 잔액과 합계를 봅니다
rows = await read_balances()
after_total = add_balances(rows)
print("잔액:", rows)
print("합계:", after_total)'''

INSIDE = r'''# 같은 이체를 한 블록으로 다시 하되, 더하기와 빼기 사이에 블록 안에서 2번 잔액을 읽습니다
one_sql = text("SELECT balance FROM ch31_tx.accounts WHERE id = :id")
try:
    async with engine.begin() as conn:
        await conn.execute(deposit_sql, {"id": 2, "amount": 600})
        inside = await conn.execute(one_sql, {"id": 2})
        print("블록 안에서 읽은 2번 잔액:", inside.scalar_one())
        await conn.execute(withdraw_sql, {"id": 1, "amount": 600})
except IntegrityError as error:
    print("받은 오류:", type(error).__name__)'''

SHOW_INSIDE = r'''# 블록이 끝난 뒤, 블록 밖에서 두 계좌의 잔액을 다시 읽습니다
rows = await read_balances()
print("잔액:", rows)'''

COMPARE = r'''# 처음 합계와 두 판이 끝난 뒤의 합계를 모아, 처음과 같은지 참·거짓으로 봅니다
print("처음 합계:", start_total)
print("Before 뒤 합계:", before_total)
print("After 뒤 합계:", after_total)
print("Before 뒤 합계가 처음과 같은가:", before_total == start_total)
print("After 뒤 합계가 처음과 같은가:", after_total == start_total)'''

VARY = r'''# 값 바꿔 보기: 보낼 돈만 600에서 500으로 바꿔, 같은 한 블록 함수로 보냅니다
amount = 500
await transfer_one_block(1, 2, amount)
rows = await read_balances()
print("보낸 돈:", amount)
print("잔액:", rows)
print("합계:", add_balances(rows))'''

CLEANUP = r'''# 끝 정리: 이름 공간 ch31_tx를 안의 표까지 지우고, 남았는지 물은 뒤 풀을 비웁니다
async with engine.begin() as conn:
    await conn.execute(text("DROP SCHEMA ch31_tx CASCADE"))
    result = await conn.execute(text("SELECT to_regnamespace('ch31_tx')"))
    left_namespace = result.scalar_one()
await engine.dispose()
print("남은 이름 공간:", left_namespace)
print("풀에 쉬고 있는 연결 수:", engine.pool.checkedin())'''

# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/02-figures.md)
FIG1 = "02-1-한-묶음-작업의-두-갈래"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 파란 상자 async with engine.begin() 블록 안 두 줄, 2번에 더하기와 1번에서 빼기에서 점선 화살표 둘이 갈라집니다. 한 점선은 회색 상자 블록이 오류 없이 끝남 두 줄을 함께 확정으로, 다시 노란 상자 이체 100 뒤 1번 400 2번 600으로 갑니다. 다른 점선은 회색 상자 블록 안에서 오류 두 줄을 함께 취소로, 다시 노란 상자 이체 600 뒤 1번 500 2번 500으로 가는 그림"
FIG1_CAP = "블록 하나 안의 두 줄은 오류 없이 끝나면 함께 확정되었고, 오류가 나면 함께 취소되어 잔액이 그대로였습니다."
FIG1_READ = """위에서 아래로 읽습니다.
파란 상자는 우리가 적은 블록과 그 안의 두 줄입니다.
회색 상자 둘은 블록이 끝날 때 라이브러리가 보내는 확정과 취소이고, 점선은 둘 가운데 한쪽으로 가는 갈래입니다.
노란 상자는 노트북 4절과 6절 출력으로 확인한 잔액입니다."""

FIG2 = "02-2-계좌-표-준비와-이체-100"
FIG2_ALT = "위에서 아래로 여섯 상자가 한 줄로 이어진 흐름도입니다. 파란 상자 begin 블록 이름 공간 ch31_tx 표 accounts CHECK 잔액 0 이상에서 초록 상자 계좌 두 줄 1번 500 2번 500으로, 노란 상자 처음 합계 1000으로 갑니다. 이어서 파란 상자 transfer_one_block 1번에서 2번으로 100 더하기와 빼기 한 블록, 회색 상자 블록 끝 확정, 노란 상자 1번 400 2번 600 합계 1000으로 이어지는 그림"
FIG2_CAP = "잔액이 0 이상이어야 하는 표에서 100을 한 블록으로 보내자, 두 줄이 함께 확정되어 합계 1000이 그대로였습니다."
FIG2_READ = """위에서 아래로 읽습니다.
파란 상자 둘은 노트북 3절의 표 만들기 블록과 4절의 이체 함수입니다.
초록 상자는 표에 넣은 계좌 두 줄이고, 회색 상자는 블록 끝의 확정입니다.
노란 상자 둘은 3절과 4절 출력으로 확인한 잔액과 합계입니다."""

FIG3 = "02-3-블록-둘로-따로-확정한-Before"
FIG3_ALT = "위에서 아래로 읽는 흐름도입니다. 회색 상자 처음 1번 500 2번 500 이체 600에서 첫째 begin 블록 칸의 파란 상자 2번에 600 더하기로, 다시 회색 상자 블록 끝 확정으로 갑니다. 이어서 둘째 begin 블록 칸의 파란 상자 1번에서 600 빼기, 노란 상자 받은 오류 IntegrityError SQLSTATE 23514 1번 -100은 CHECK에 걸림, 마지막 빨간 상자 남은 잔액 1번 500 2번 1100 합계 1600으로 이어지는 그림"
FIG3_CAP = "블록 둘로 나눈 Before 판은 첫째 블록의 더하기를 이미 확정해, 둘째 블록의 빼기가 막힌 뒤 합계 1600이 남았습니다."
FIG3_READ = """위에서 아래로 읽습니다.
맨 위 회색 상자는 Before 판을 시작할 때의 잔액과 보낼 돈입니다.
칸 둘은 begin 블록 둘이고, 칸 안 파란 상자가 블록마다 보낸 SQL 글 하나입니다.
노란 상자는 노트북 5절에서 받아 출력한 오류이고, 빨간 상자는 그 뒤에 남은 잔액과 합계입니다."""

FIG4 = "02-4-블록-둘과-블록-하나-견주기"
FIG4_ALT = "위에 회색 상자 하나가 있고 아래에 칸 둘이 나란히 놓인 그림입니다. 회색 상자 두 판 같음 처음 1번 500 2번 500 이체 600 받은 오류 23514에서 두 칸으로 화살표가 갑니다. 한 칸 Before 블록 둘에는 파란 상자 더하기 확정 뒤 빼기가 막힘 아래 빨간 상자 1번 500 2번 1100 합계 1600이 있습니다. 다른 칸 After 블록 하나에는 파란 상자 빼기가 막혀 더하기도 취소 아래 노란 상자 1번 500 2번 500 합계 1000이 있는 그림"
FIG4_CAP = "같은 오류를 받은 두 판 가운데, 블록 둘로 나눈 Before는 합계 1600을, 블록 하나인 After는 처음 합계 1000을 남겼습니다."
FIG4_READ = """맨 위 회색 상자는 두 판에서 같았던 처음 잔액·보낼 돈·받은 오류 코드입니다.
왼쪽 Before 칸과 오른쪽 After 칸의 제목이 두 판에서 다른 블록의 수이고, 파란 상자는 그 블록에서 일어난 일입니다.
빨간 상자는 Before 판의 결함 결과이고, 노란 상자는 After 판의 결과입니다.
두 칸의 잔액과 합계는 노트북 5절과 6절 출력입니다."""

ILLU = "02-5-양-끝이-꽂힌-선과-한-끝만-꽂힌-선"
ILLU_ALT = "흰 바탕에 짙은 초록 금속 판 하나가 가로를 채우고, 판 아래쪽에 옅은 나무 선반이 있습니다. 구멍 하나짜리 둥근 꽂는 자리 여섯이 두 개씩 짝을 지어 한 줄로 있고, 자리마다 위에 작은 둥근 불이 있습니다. 왼쪽 짝은 파란 선 하나의 양 끝이 두 자리에 꽂혀 아래로 휘어 이어지고, 불 둘이 초록으로 켜져 있습니다. 가운데 짝은 파란 선 하나의 한 끝만 왼쪽 자리에 꽂혀 선반 앞을 지나 아래로 늘어지고, 불은 왼쪽 하나만 켜져 있습니다. 오른쪽 짝은 두 자리가 비어 불 둘이 회색이고, 파란 선 하나가 선반 위에 감겨 놓여 있습니다. 사람·손·글자·숫자·화살표는 없는 그림"
ILLU_CAP = "양 끝이 꽂힌 짝은 불 둘이, 한 끝만 꽂힌 짝은 불 하나가 켜져 있고, 두 자리가 빈 짝은 불이 모두 꺼져 있습니다."
ILLU_READ = "초록 금속 판 하나에 꽂는 자리 여섯이 두 개씩 짝 셋으로 놓여 있습니다. 왼쪽 짝은 선의 양 끝이 모두 꽂혀 불 둘이 켜져 있습니다. 가운데 짝은 한 끝만 꽂히고 다른 끝은 아래로 늘어져, 불 하나만 켜져 있습니다. 오른쪽 짝은 두 자리가 모두 비어 불이 꺼져 있고, 선은 선반 위에 감겨 있습니다. 짝 하나가 이체의 두 변경이고, 왼쪽이 이체 100, 가운데가 Before 판, 오른쪽이 After 판이 남긴 모습입니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 잔액이 0 이상이어야 하는 계좌 표를 만들고, 두 계좌 사이에서 돈을 보냅니다.
2. 잔액을 바꾸는 두 줄을 블록 둘로 따로 확정하면, 둘째 줄이 막힐 때 첫째 줄만 남는 것을 봅니다.
3. 두 줄을 블록 하나로 묶어, 둘째 줄이 막히면 첫째 줄도 함께 취소되는 것을 확인합니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
예상 비용도 0달러입니다.

01절과 같은 PostgreSQL 서버가 `127.0.0.1:55431`에서 켜져 있어야 합니다.
서버는 01절 준비물의 Docker 컨테이너 `kdt-ch31-postgres`입니다.
꺼져 있으면 터미널에서 `docker start kdt-ch31-postgres`로 다시 켭니다.
컨테이너를 아직 만들지 않았다면, 01절 노트북 맨 위 준비물의 `docker run` 명령을 먼저 실행합니다.

노트북은 데이터베이스 `ch31_lab` 안에 이름 공간 `ch31_tx`를 만들어 쓰고, 끝에서 지웁니다.
작업 폴더에 파일을 쓰지 않고, 읽어 오는 자료 파일도 없습니다.
걸린 시간은 재지 않습니다.

**기준 버전** — 첫 셀에서 패키지 둘을 설치합니다.
버전은 sqlalchemy 2.0.43과 asyncpg 0.30.0이고, 실습 폴더 잠금과 같습니다.
교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다.
그 서버는 Docker 컨테이너가 아니라, 같은 접속 글로 켠 서버입니다.

Docker 이미지로 켜면 서버 버전 번호의 끝자리가 다를 수 있습니다.
다른 버전과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~4절을 읽습니다.
계좌 표·CHECK 제약·한 묶음 작업을 처음 보는 자리입니다.
5·6절은 Before와 After이고, 7절은 값 바꿔 보기입니다.
5~7절은 실습 시간에 실행하고, 8절은 만든 이름 공간을 지우는 정리입니다.

실습 폴더 `labs/part7/ch31-database`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

01절에서는 블록 `engine.begin()`이 안의 SQL 글을 한 묶음으로 실행하고, 오류 없이 끝나면 확정하는 것을 봤습니다.
이 절은 그 블록 안에서 오류가 나면 무엇이 남는지 봅니다.
보기로는 두 계좌 사이에서 돈을 보내는 이체를 씁니다.

절 제목의 트랜잭션(transaction)은 데이터베이스가 한 묶음으로 다루는 작업입니다.
이 교재 본문에서는 「한 묶음 작업」이라고 부릅니다.
제목의 원자성은 4절에서 풉니다.

첫 셀은 01절과 같은 패키지 둘을 설치하고, 설치된 버전 번호를 출력합니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `sqlalchemy: 2.0.43`과 `asyncpg: 0.30.0`이 보입니다.
01절과 같은 버전이고, 실습 폴더 잠금과 같습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
오류 이름 `IntegrityError`는 패키지 sqlalchemy의 모듈 `exc`에서 가져옵니다.
Ch 4 03절에서 sqlite3가 제약을 어긴 행에 낸 오류와 이름이 같습니다.
이 절에서는 PostgreSQL 서버가 막은 변경을, SQLAlchemy가 이 이름의 오류로 알려 줍니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `가져온 이름: text IntegrityError create_async_engine`이 보입니다.
이 노트북에는 API 키를 확인하는 셀이 없습니다.
모델을 부르지 않기 때문입니다.

## 2. 데이터베이스에 붙기

다음 셀은 01절 2절의 설정 셀과 글자까지 같은 셀로, 연습용 접속 글을 정합니다.
이 노트북도 `.env` 파일을 읽지 않습니다.
서버를 다른 주소나 계정으로 켰다면 이 셀의 글만 고칩니다."""),
        code(SETTINGS),
        md("""**결과 읽기** — 출력 줄 `드라이버 부분: postgresql+asyncpg`가 보입니다.
라벨 `서버 주소와 데이터베이스:` 뒤의 `127.0.0.1:55431/ch31_lab`은 01절과 같은 서버와 데이터베이스입니다.
비밀번호가 든 가운데 부분은 출력하지 않았습니다.

다음 셀은 이 접속 글로 비동기 엔진을 만듭니다.
01절과 달리 풀 인자를 적지 않아, SQLAlchemy가 정한 기본값을 씁니다.
이 절은 연결을 한 번에 하나씩만 빌려 쓰므로, 풀의 크기는 결과에 닿지 않습니다."""),
        code(ENGINE),
        md("""**결과 읽기** — 출력 줄 `엔진의 종류: AsyncEngine`과 `풀에 둘 연결 수: 5`가 보입니다.
풀에 둘 연결 수 5는 SQLAlchemy의 기본값입니다.
엔진을 만들기만 해서는 서버에 붙지 않는 것은 01절과 같습니다.

## 3. 계좌 표와 CHECK 제약

이 절의 표 `accounts`는 계좌 번호 칸 `id`와 잔액 칸 `balance`를 가집니다.
표는 이름 공간 `ch31_tx`에 두고, 01절처럼 처음에 지우고 다시 만듭니다.

잔액 칸에는 제약을 겁니다.
Ch 4 03절에서 제약(constraint)은 표에 적어 두고, 어기는 행을 막는 조건이었습니다.
CHECK 제약은 칸 값이 적어 둔 식을 만족해야 한다는 조건입니다.
이 표의 `CHECK (balance >= 0)`은 잔액이 0 이상이어야 한다는 뜻입니다.
잔액이 0보다 작아지는 줄은 PostgreSQL 서버가 저장하지 않고 오류를 냅니다."""),
        code(PREPARE),
        md("""**결과 읽기** — 출력 줄 `넣은 줄 수: 2`가 보입니다.
계좌 두 줄이 잔액 500씩으로 표에 들어갔습니다.
블록이 오류 없이 끝나, 이름 공간·표·두 줄을 한꺼번에 확정했습니다.

다음 두 셀은 잔액을 읽는 함수와 잔액을 더하는 함수를 정의합니다.
함수 `read_balances`는 연결을 하나 빌려, 두 계좌의 번호와 잔액을 번호 차례로 읽습니다.
메서드 `fetchall`은 01절처럼 결과의 줄을 모두 목록으로 꺼냅니다."""),
        code(DEF_READ),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수는 불릴 때마다 연결을 빌렸다가, 블록이 끝나면 풀에 다시 넣습니다.

다음 셀의 함수 `add_balances`는 줄 목록을 받아 잔액을 모두 더한 합계를 내놓습니다.
줄의 칸 값은 `row.balance`처럼 점 뒤에 칸 이름을 적어 꺼냅니다.
두 계좌 사이에서 돈을 보내기만 하면, 합계는 처음과 같아야 합니다."""),
        code(DEF_ADD),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
합계를 세는 모양은 Ch 2 02절의 `for` 반복문과 같습니다.

다음 셀은 두 함수로 처음 잔액과 합계를 봅니다.
합계는 변수 `start_total`에 남겨, 뒤에서 견줄 기준으로 씁니다."""),
        code(SHOW_START),
        md("""**결과 읽기** — 출력 줄 `잔액: [(1, 500), (2, 500)]`과 `합계: 1000`이 보입니다.
줄 하나는 계좌 번호와 잔액의 튜플 모양으로 찍힙니다.
두 계좌의 잔액을 더한 1000이 이 절의 기준 합계입니다.

## 4. 한 묶음 작업으로 이체하기

이체는 받는 계좌의 잔액에 더하고, 보내는 계좌의 잔액에서 빼는 일입니다.
두 줄 가운데 하나만 바뀌면 합계가 달라집니다.
그래서 두 줄은 모두 바뀌거나, 모두 그대로여야 합니다.

한 묶음 작업(트랜잭션)은 여러 SQL 글을 한 묶음으로 실행하고, 끝에서 한꺼번에 확정하는 작업입니다.
장바구니에 담은 물건을 한 번에 계산해, 결제가 되면 모두 사고 안 되면 아무것도 사지 않는 것과 비슷합니다.
이 절의 코드에서는 블록 `async with engine.begin() as conn:` 하나가 한 묶음 작업 하나입니다.
블록이 오류 없이 끝나면 블록 안의 변경을 한꺼번에 확정(커밋)합니다.
확정은 Ch 4 03절의 커밋과 같은 일입니다.

제목의 원자성(atomicity)은 한 묶음 작업 안의 변경이 모두 확정되거나, 모두 없던 일이 되는 성질입니다.
두 사람이 모두 서명해야 효력이 생기는 계약서와 비슷합니다.
한 사람만 서명한 계약서는 없는 계약입니다.
이 절에서는 6절 After 판의 잔액으로 이 성질을 확인합니다.

다음 셀은 잔액을 바꾸는 SQL 글 둘을 객체로 만듭니다.
SQL 문장 `UPDATE`는 `WHERE` 조건에 맞는 줄에서, `SET` 뒤에 적은 칸 값을 바꿉니다.
글 `balance = balance + :amount`는 지금 잔액에 금액을 더한 값으로 바꾸라는 뜻입니다.
자리 `:amount`와 `:id`에는 01절처럼 실행할 때 따로 넘긴 값이 들어갑니다."""),
        code(UPDATE_SQL),
        md("""**결과 읽기** — 라벨 `더하는 SQL 글:`과 `빼는 SQL 글:` 뒤에 두 SQL 글이 그대로 찍혔습니다.
두 글은 `+`와 `-`만 다릅니다.
이 셀은 객체를 만들기만 했고, 서버에는 아직 아무것도 보내지 않았습니다.

다음 셀의 함수 `transfer_one_block`은 보내는 계좌·받는 계좌·금액을 받아 이체합니다.
블록 하나 안에서 받는 계좌에 먼저 더하고, 그다음 보내는 계좌에서 뺍니다.
이 차례는 5절의 결과가 잘 보이도록 정한 것이고, 까닭은 5절 끝에서 봅니다."""),
        code(DEF_ONE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
두 await 줄이 같은 블록 안에 있어, 두 변경이 한 묶음 작업이 됩니다.

다음 셀은 1번 계좌에서 2번 계좌로 100을 보내고, 잔액과 합계를 봅니다."""),
        code(TRANSFER_100),
        md("""**결과 읽기** — 출력 줄 `잔액: [(1, 400), (2, 600)]`과 `합계: 1000`이 보입니다.
1번은 100이 줄고 2번은 100이 늘어, 합계는 처음과 같습니다.
블록이 오류 없이 끝나 두 변경을 함께 확정했습니다."""),
        md("""## 5. 블록 둘로 따로 확정하는 이체 (Before)

이번에는 1번 계좌에서 2번 계좌로 600을 보냅니다.
1번 계좌의 잔액은 500이라, 600을 빼면 CHECK 제약에 걸립니다.
Before 판의 이체 함수는 더하기와 빼기를 블록 둘에 하나씩 넣습니다.
블록마다 따로 확정하므로, 한 묶음 작업이 둘로 나뉩니다.
다음 셀은 그 함수를 정의합니다.""", lesson_part="before"),
        code(DEF_TWO, lesson_part="before"),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `transfer_one_block`과 다른 곳은 둘째 `async with engine.begin() as conn:` 줄 하나입니다.

다음 셀은 4절의 이체로 바뀐 잔액을, 두 계좌 모두 500으로 다시 맞춥니다.
조건 `WHERE`를 적지 않은 `UPDATE`는 표의 모든 줄을 바꿉니다.""", lesson_part="before"),
        code(RESET, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `다시 500으로 맞춘 줄 수: 2`와 `잔액: [(1, 500), (2, 500)]`이 보입니다.
두 계좌가 처음과 같은 잔액이 되었습니다.

다음 셀은 Before 판 함수로 600을 보내 봅니다.
둘째 블록에서 오류가 날 것이므로, Ch 2 05절처럼 오류 이름 `IntegrityError`만 받는 `try`로 감쌉니다.
받은 오류의 이름과 오류 코드, 드라이버가 받은 오류 글을 출력하고 셀은 끝까지 갑니다.
실행 전에 예상해 봅니다.
오류가 난 뒤, 두 계좌의 잔액은 무엇일까요?""", lesson_part="before"),
        code(BEFORE_CALL, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `받은 오류: IntegrityError`와 `오류 코드(SQLSTATE): 23514`가 보입니다.
라벨 줄 아래 오류 글에는 `violates check constraint "accounts_balance_check"`가 있습니다.
그 아래 줄 `DETAIL:  Failing row contains (1, -100).`은 막힌 줄이 1번 계좌라는 뜻입니다.
1번 잔액이 -100이 될 뻔해서, 둘째 블록의 빼기가 CHECK 제약에 막혔습니다.

오류 코드 SQLSTATE는 PostgreSQL 서버가 오류마다 붙이는 다섯 글자 코드입니다.
PostgreSQL 문서는 `23514`를 CHECK 제약 위반(check_violation)이라고 적습니다.
제약 이름 `accounts_balance_check`는 이름을 적지 않은 제약에 서버가 붙인 이름입니다.
오류 글 맨 앞의 `CheckViolationError`는 드라이버 asyncpg의 오류 이름입니다.

라벨 `드라이버가 받은 오류 글:` 아래 글은 속성 `orig`의 글입니다.
속성 `orig`에 든 것은 SQLAlchemy가 드라이버 오류를 파이썬 데이터베이스 약속(DB-API)의 모양으로 바꾼 오류입니다.
그래서 그 글 첫머리에 드라이버의 오류 이름이 붙어 찍혔습니다.

다음 셀은 오류가 난 뒤의 잔액과 합계를 봅니다.""", lesson_part="before"),
        code(SHOW_BEFORE, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `잔액: [(1, 500), (2, 1100)]`과 `합계: 1600`이 보입니다.
1번에서는 빠지지 않았는데, 2번에는 600이 더해져 있습니다.
합계가 처음 1000보다 600 많아졌습니다.
이것이 이 절의 Before 결함입니다.

첫째 블록은 오류 없이 끝나, 더하기를 이미 확정했습니다.
둘째 블록의 오류는 둘째 블록의 빼기만 막았고, 이미 확정한 첫째 블록에는 닿지 않았습니다.
오류는 받았지만, 데이터베이스에는 반쯤 끝난 이체가 남았습니다.

4절에서 받는 계좌에 먼저 더하게 정한 것은 이 결함이 잔액에 보이게 하려는 것입니다.
노트북 밖에서 빼기를 먼저 하는 블록 둘로 600을 보내 보자, 첫째 블록에서 막혀 잔액이 그대로였습니다.
그래도 블록이 둘이면, 둘째 블록이 막힐 때 첫째 블록의 확정은 남습니다.""", lesson_part="before"),
        md("""## 6. 블록 하나로 묶은 이체 (After)

After 판은 4절의 함수 `transfer_one_block`으로 같은 600을 보냅니다.
더하기와 빼기가 블록 하나 안에 있어, 한 묶음 작업 하나입니다.
다음 셀은 먼저 두 계좌를 다시 500으로 맞춥니다.""", lesson_part="after"),
        code(RESET, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `다시 500으로 맞춘 줄 수: 2`와 `잔액: [(1, 500), (2, 500)]`이 보입니다.
Before 판을 시작할 때와 같은 잔액입니다.

다음 셀은 같은 600을 블록 하나로 보내 봅니다.
실행 전에 예상해 봅니다.
같은 오류가 나면, 2번 계좌에 더한 600은 남을까요?""", lesson_part="after"),
        code(AFTER_CALL, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `받은 오류: IntegrityError`와 `오류 코드(SQLSTATE): 23514`가 보입니다.
Before 판과 같은 오류를 받았습니다.
빼기가 CHECK 제약에 막힌 것도 같습니다.

다음 셀은 오류가 난 뒤의 잔액과 합계를 봅니다.""", lesson_part="after"),
        code(SHOW_AFTER, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `잔액: [(1, 500), (2, 500)]`과 `합계: 1000`이 보입니다.
2번 계좌에 더한 600이 남지 않았고, 합계는 처음과 같습니다.

블록 안에서 오류가 나면, 블록은 안의 변경을 확정하지 않고 모두 없던 일로 합니다.
이것을 취소(롤백, rollback)라고 부릅니다.
연필로 적어 둔 것을 볼펜으로 옮겨 적기 전에, 지우개로 모두 지우는 것과 비슷합니다.
받은 오류는 블록 밖으로 나와 `except` 줄이 받았습니다.
03절 제목의 롤백은 표 구조의 판을 내리는 일이라, 이 절의 취소와 뜻이 다릅니다.

다음 셀은 같은 이체를 한 번 더 하되, 더하기와 빼기 사이에 블록 안에서 2번 잔액을 읽습니다.
블록 안에서는 더하기가 정말 일어났는지 보려는 것입니다.
메서드 `scalar_one`은 01절처럼 결과가 한 줄일 때 그 줄의 첫 칸 값을 꺼냅니다.""", lesson_part="after"),
        code(INSIDE, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `블록 안에서 읽은 2번 잔액: 1100`과 `받은 오류: IntegrityError`가 보입니다.
블록 안에서는 더하기가 일어나, 2번 잔액이 1100이었습니다.
그다음 빼기가 막혀, 블록이 오류로 끝났습니다.

다음 셀은 블록 밖에서 잔액을 다시 읽습니다.""", lesson_part="after"),
        code(SHOW_INSIDE, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `잔액: [(1, 500), (2, 500)]`이 보입니다.
블록 안에서 읽은 1100은 확정되지 않고 취소되어, 2번 잔액은 다시 500입니다.
두 변경이 모두 없던 일이 되었고, 이것이 제목의 원자성입니다.

다음 셀은 처음 합계와 두 판이 끝난 뒤의 합계를 한곳에 모아 견줍니다.""", lesson_part="after"),
        code(COMPARE, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `Before 뒤 합계가 처음과 같은가: False`와 `After 뒤 합계가 처음과 같은가: True`가 보입니다.
Before 판은 합계 `1600`을, After 판은 합계 `1000`을 남겼습니다.
두 판은 같은 오류를 받았고, 다른 것은 블록의 수 하나였습니다.

## 7. 값 바꿔 보기: 보낼 돈

값 하나만 바꿔 봅니다.
바꿀 것은 보낼 돈이고, 600 대신 1번 잔액과 같은 500을 보냅니다.
함수는 After 판의 `transfer_one_block` 그대로입니다.
실행 전에 예상해 봅니다.
1번 잔액이 0이 되는 이체는 CHECK 제약에 막힐까요?""", lesson_part="after"),
        code(VARY, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `보낸 돈: 500`과 `잔액: [(1, 0), (2, 1000)]`이 보입니다.
출력 줄 `합계: 1000`은 처음 합계와 같습니다.
CHECK 제약은 잔액 0 이상을 허용하므로, 오류 없이 두 변경을 함께 확정했습니다.
한 묶음 작업은 막히지 않으면 모두 확정하고, 막히면 모두 취소합니다.

## 8. 정리: 이름 공간 지우기

다음 셀은 이름 공간 `ch31_tx`를 안의 표까지 지우고, 엔진의 풀도 비웁니다.
PostgreSQL 함수 `to_regnamespace`는 01절처럼, 이름 공간이 없으면 빈 값을 내놓습니다.""", lesson_part="after"),
        code(CLEANUP, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `남은 이름 공간: None`과 `풀에 쉬고 있는 연결 수: 0`이 보입니다.
이 노트북을 처음부터 다시 실행하면, 3절이 이름 공간을 새로 만들어 같은 출력이 나옵니다.

## 정리

1. 표의 CHECK 제약은 잔액을 0보다 작게 만드는 빼기를 막았고, 받은 오류의 코드는 `23514`였습니다.
2. 더하기와 빼기를 블록 둘로 따로 확정하자, 빼기가 막힌 뒤에도 더하기가 남아 합계가 1600이 되었습니다.
3. 두 줄을 블록 하나로 묶자, 같은 오류에서 두 변경이 함께 취소되어 합계가 1000으로 남았습니다.

03절에서는 Alembic으로 표 구조를 판마다 바꾸는 방법을 봅니다.""", lesson_part="after"),
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
    """노트북용 마크다운 한 단락(백틱·줄바꿈)을 _src 문단 글로 바꿉니다(01절 생성기와 같은 함수)."""
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


L_CH02_02 = "../../part1/ch02-python/02-조건문과-반복문.html"
L_CH02_05 = "../../part1/ch02-python/05-파일과-예외.html"
L_CH04_03 = "../../part1/ch04-data-tools/03-SQL로-조회-함수-만들기.html"
L_CH23_04 = "../../part6/ch23-persistence/04-내구-실행-모드-비교.html"
L_CH23_06 = "../../part6/ch23-persistence/06-노드-재시작과-멱등성.html"
L_01 = "01-SQLAlchemy-비동기-PostgreSQL.html"
L_03 = "03-Alembic-적용과-롤백.html"

TERM_ROWS = [
    ("한 묶음 작업(트랜잭션, transaction)", "여러 SQL 글을 한 묶음으로 실행하고, 끝에서 한꺼번에 확정하는 작업입니다. 장바구니의 물건을 한 번에 계산해, 결제가 되면 모두 사고 안 되면 아무것도 사지 않는 것과 같습니다. 이 절에서는 블록 <code>async with engine.begin() as conn:</code> 하나가 한 묶음 작업 하나입니다."),
    ("원자성(atomicity)", "한 묶음 작업 안의 변경이 모두 확정되거나, 모두 없던 일이 되는 성질입니다. 두 사람이 모두 서명해야 효력이 생기는 계약서와 같습니다. 이 절에서는 빼기가 막히자 같은 블록의 더하기도 남지 않았습니다."),
    ("취소(롤백, rollback)", "블록 안에서 오류가 나면, 확정하지 않고 블록 안의 변경을 모두 없던 일로 하는 것입니다. 연필로 적어 둔 것을 볼펜으로 옮겨 적기 전에 지우개로 모두 지우는 것과 같습니다. 이 절에서는 블록 안에서 읽은 2번 잔액 1100이 블록 밖에서 500이었습니다."),
]

COMPARE_ROWS = [
    ("더하기와 빼기의 자리", "begin 블록 둘에 하나씩", "begin 블록 하나에 함께"),
    ("받은 오류", "<code>IntegrityError</code> · <code>23514</code>", "<code>IntegrityError</code> · <code>23514</code>"),
    ("오류가 난 뒤 잔액", "<code>[(1, 500), (2, 1100)]</code>", "<code>[(1, 500), (2, 500)]</code>"),
    ("합계(처음 1000)", "<code>1600</code>", "<code>1000</code>"),
    ("합계가 처음과 같은가", "<code>False</code>", "<code>True</code>"),
]

B4_ANALOGY = ("<p>옛 전화 교환대의 넓은 판 하나를 떠올려 봅니다. 판에는 꽂는 자리가 두 개씩 짝을 지어 놓여 있고, 자리마다 위에 작은 불이 달려 있습니다. "
              "통화 하나를 이으려면 선 한 가닥의 양 끝을 짝이 되는 두 자리에 모두 꽂아야 합니다. 끝이 꽂힌 자리에는 불이 켜집니다.</p>"
              "<p>판에 짝 셋이 왼쪽부터 나란히 있습니다. 첫째 짝은 선의 양 끝이 두 자리에 모두 꽂혀, 불 둘이 켜져 있습니다. "
              "둘째 짝은 한 끝만 꽂히고 다른 끝은 아래로 늘어져, 불 하나만 켜져 있습니다. "
              "셋째 짝은 두 자리가 모두 비어 불이 꺼져 있고, 선은 판 아래쪽 나무 선반에 감겨 놓여 있습니다.</p>"
              "<p>짝이 된 두 자리가 이체의 두 변경이고, 선 한 가닥이 한 묶음 작업입니다. 첫째 짝은 이체 100처럼 두 변경이 모두 확정된 모습입니다. "
              "둘째 짝은 Before 판처럼 한쪽만 남은 모습이고, 셋째 짝은 After 판처럼 두 변경이 모두 취소된 모습입니다. "
              "교환대에서 쓸모 있는 모습은 첫째와 셋째뿐입니다.</p>"
              "<p>비유와 다른 점이 있습니다. 실제 블록은 안의 변경을 하나씩 먼저 적용해 둡니다. 그리고 블록이 끝날 때 한꺼번에 확정하거나, 한꺼번에 취소합니다.</p>")

LOOK_B5 = "노트북 3절 끝에서 <code>잔액: [(1, 500), (2, 500)]</code>과 <code>합계: 1000</code>을 봅니다. 4절 이체 뒤 <code>잔액: [(1, 400), (2, 600)]</code>과 합계 1000을 확인합니다. 2절의 <code>풀에 둘 연결 수: 5</code>는 SQLAlchemy의 기본값입니다."
LOOK_B6 = "Before 판에서 <code>오류 코드(SQLSTATE): 23514</code>와 <code>잔액: [(1, 500), (2, 1100)]</code>을 봅니다. After 판에서 같은 오류 코드와 <code>잔액: [(1, 500), (2, 500)]</code>을 확인합니다. 블록 안에서 읽은 2번 잔액 1100과, 7절의 <code>잔액: [(1, 0), (2, 1000)]</code>도 찾습니다."


def src_html() -> str:
    terms = table_html(["말", "뜻"], TERM_ROWS)
    compare = table_html(["견준 것", "Before(블록 둘)", "After(블록 하나)"], COMPARE_ROWS)
    return """<!--meta: 강의 1h | 실습 2h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>잔액 칸에 CHECK 제약을 건 표에서, 제약을 어기는 빼기가 받은 오류와 오류 코드를 출력으로 확인할 수 있습니다.</li>
<li>이체의 두 변경을 블록 둘로 따로 확정하면, 둘째 변경이 막힌 뒤 첫째 변경만 남는 것을 재현할 수 있습니다.</li>
<li>두 변경을 블록 <code>engine.begin()</code> 하나로 묶어, 오류가 나면 모두 취소되는 것을 잔액과 합계로 확인할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>에이전트 서비스의 요청 하나가 데이터베이스의 줄 여럿을 함께 바꿀 때가 있습니다. 예를 들어 대화 기록 한 줄을 저장하면서, 사용자가 쓸 수 있는 남은 횟수를 하나 줄이는 일입니다. 둘 가운데 하나만 남으면, 다음 요청은 사실과 다른 상태를 읽습니다. 이 절은 두 계좌 사이의 이체로, 함께 바꿔야 하는 두 줄을 다룹니다.</p><p>절 제목의 트랜잭션(transaction)은 데이터베이스가 한 묶음으로 다루는 작업입니다. 이 교재 본문에서는 「한 묶음 작업」이라고 부릅니다. 제목의 원자성은 그 작업 안의 변경이 모두 확정되거나 모두 없던 일이 되는 성질입니다. <a href=\"""" + L_01 + """\">01절</a>에서는 오류 없이 끝난 블록 <code>engine.begin()</code>이 변경을 확정하는 것만 봤고, 이 절은 블록 안에서 오류가 날 때를 봅니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_01 + """\">01절</a>에서는 비동기 엔진을 만들고, 연결 풀에서 빌린 연결로 SQL 글을 보냈습니다. 블록 <code>engine.begin()</code>으로 이름 공간과 표를 만들고, 블록이 오류 없이 끝나면 확정되는 것을 봤습니다. SQL 글 속 <code>:id</code> 같은 자리에 값을 따로 넘기는 방법도 이 절에서 그대로 씁니다.</p><p><a href=\"""" + L_CH04_03 + """\">Ch 4 03절</a>에서는 표에 기본 키·외래 키 제약을 걸고, 어기는 행을 넣다가 오류 <code>sqlite3.IntegrityError</code>를 받았습니다. 넣은 행은 <code>commit()</code>으로 확정했습니다. <a href=\"""" + L_CH02_05 + """\">Ch 2 05절</a>에서는 <code>try</code>와 <code>except</code>로 이름이 맞는 오류만 받아, 셀을 끝까지 실행했습니다. 이 절은 세 가지를 PostgreSQL 서버의 CHECK 제약과 블록 <code>engine.begin()</code>에 씁니다.</p><p><a href=\"""" + L_CH23_04 + """\">Ch 23 04절</a>부터 <a href=\"""" + L_CH23_06 + """\">06절</a>까지는 멈춘 그래프를 체크포인트에서 이어 실행했습니다. 06절에서는 다시 실행된 단계가 바깥 파일에 같은 쓰기를 두 번 하지 않게, 멱등 키로 이미 한 일인지 확인했습니다. 이 절은 그보다 앞의 물음을 봅니다. 이어 실행할 때 읽을 데이터베이스의 줄들이 반쯤 바뀐 채 남지 않게 하는 방법입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3>""" + B4_ANALOGY + """
""" + illustration_block() + """<h3>한 묶음 작업과 원자성</h3><p>블록 <code>engine.begin()</code> 하나가 한 묶음 작업 하나입니다. 블록 안의 SQL 글은 차례로 서버에 가서 적용되지만, 아직 확정된 것은 아닙니다. 블록이 오류 없이 끝나면 라이브러리가 확정(커밋)을 보내고, 블록 안에서 오류가 나면 취소(롤백)를 보냅니다. SQLAlchemy 문서도 블록이 정상으로 끝나면 확정하고, 오류가 나면 취소한 뒤 그 오류를 블록 밖으로 내보낸다고 적습니다.</p><p>PostgreSQL 문서는 한 묶음 작업이 여러 단계를, 모두 되거나 모두 안 되는 하나의 일로 묶는다고 적습니다. 문서의 예도 한 계좌에서 빼고 다른 계좌에 더하는 이체입니다. 둘 가운데 한쪽만 남으면 안 되는 일을 한 블록에 넣는 것이 이 절의 방법입니다.</p>
""" + terms + """
<p>새 말을 이 절 코드에서 보면 이렇습니다. 이체 함수 <code>transfer_one_block</code>의 블록 하나가 한 묶음 작업이고, 100을 보내자 <code>잔액: [(1, 400), (2, 600)]</code>으로 두 줄이 함께 확정되었습니다. 600을 보내자 빼기가 막혀 더하기도 남지 않았고, 잔액은 <code>[(1, 500), (2, 500)]</code>이었습니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>CHECK 제약과 오류 코드</h3><p>CHECK 제약은 칸 값이 적어 둔 식을 만족해야 한다는 조건입니다. 이 절의 표는 잔액 칸에 <code>CHECK (balance >= 0)</code>을 걸었습니다. 잔액을 0보다 작게 만드는 변경은 서버가 저장하지 않고 오류를 냅니다. 제약 이름을 적지 않으면 서버가 이름을 붙이고, 이 표에서는 <code>accounts_balance_check</code>였습니다.</p><p>오류 코드 SQLSTATE는 PostgreSQL 서버가 오류마다 붙이는 다섯 글자 코드입니다. 앞 두 글자가 오류의 갈래이고, <code>23</code>은 제약을 어긴 오류의 갈래입니다. 이 절의 <code>23514</code>는 CHECK 제약 위반입니다. PostgreSQL 문서는 오류를 가릴 때 오류 글보다 이 코드를 보라고 적습니다.</p><p>라이브러리 SQLAlchemy는 서버의 오류를 <code>IntegrityError</code>로 감쌉니다. 속성 <code>orig</code>에는 SQLAlchemy가 드라이버 오류를 파이썬 데이터베이스 약속(DB-API)의 모양으로 바꾼 오류가 있습니다. 그 오류의 글 첫머리에 드라이버 오류 이름 <code>CheckViolationError</code>가 붙습니다.</p><h3>이 절의 취소와 03절 제목의 롤백</h3><p>이 절에서 취소는 블록 <code>engine.begin()</code>이 오류로 끝날 때, 블록 안의 변경을 확정하지 않는 일입니다. <a href=\"""" + L_03 + """\">03절</a> 제목의 롤백은 Alembic으로 표 구조의 판을 내리는 일이라, 뜻이 다릅니다. 둘 다 영어로 rollback이라 부르지만, 이 교재에서는 말을 나눠 씁니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 01절과 같은 접속 글로 엔진을 만듭니다. 3절은 CHECK 제약을 건 표 <code>accounts</code>에 계좌 두 줄을 넣고, 잔액을 읽는 함수와 더하는 함수를 정의합니다. 4절은 SQL 문장 <code>UPDATE</code>로 잔액을 바꾸는 이체 함수를 만들고, 100을 보냅니다.</p><p>모델 요청은 0번이고, API 키 없이 실행합니다. 데이터베이스 서버는 01절과 같은 Docker 컨테이너 <code>kdt-ch31-postgres</code>입니다. 작업 폴더에 파일을 쓰지 않고, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """|example}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>일부러 실패해 보기</h2><p>아래 Before 셀은 1번 계좌에서 2번 계좌로 600을 보냅니다. 1번 잔액이 500이라, 빼기는 CHECK 제약에 걸립니다. Before 판의 함수는 더하기와 빼기를 블록 둘에 넣어 따로 확정합니다. After 셀은 4절의 한 블록 함수로 같은 600을 보냅니다.</p>
{{notebook:""" + SLUG + """|failure}}
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + compare + """
<p>두 판은 같은 오류를 받았습니다. 받은 오류는 <code>IntegrityError</code>이고, 오류 코드는 <code>23514</code>였습니다. 다른 것은 블록의 수 하나였고, 그 차이가 남은 잔액을 갈랐습니다.</p><p>Before 판에서 첫째 블록은 오류 없이 끝나, 더하기를 이미 확정했습니다. 둘째 블록의 오류는 둘째 블록의 빼기만 막았고, 확정이 끝난 첫째 블록에는 닿지 않았습니다. 그래서 2번 잔액만 1100이 되어, 합계가 1600으로 남았습니다. 오류를 받고 셀은 끝까지 갔지만, 데이터베이스에는 반쯤 끝난 이체가 남은 것입니다.</p><p>After 판은 더하기와 빼기가 한 블록 안에 있었습니다. 블록 안에서 2번 잔액은 1100이 되었지만, 빼기가 막히자 블록이 두 변경을 함께 취소했습니다. 블록 밖에서 다시 읽은 잔액은 500과 500이었고, 합계는 처음과 같은 1000이었습니다.</p><p>노트북 7절에서 보낼 돈만 500으로 바꾸자, 같은 한 블록 함수가 오류 없이 두 변경을 확정했습니다. 1번 잔액 0은 제약 <code>balance >= 0</code>을 만족하기 때문입니다. 한 블록은 막힌 이체는 모두 취소하고, 막히지 않은 이체는 모두 확정했습니다.</p><p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>이 절의 이체 함수는 받는 계좌에 먼저 더하고, 보내는 계좌에서 뺍니다. 이 차례는 Before 판의 결함이 잔액에 보이게 하려고 정한 예입니다. 노트북 밖에서 빼기를 먼저 하는 블록 둘로 600을 보내 보자, 첫째 블록에서 막혀 잔액이 500과 500 그대로였습니다. 그래도 블록이 둘이면, 둘째 블록이 막힐 때 첫째 블록의 확정은 남습니다.</li><li>한 묶음 작업의 취소는 데이터베이스 안의 변경에만 닿습니다. 블록 안에서 바깥 서비스에 보낸 요청은 취소되지 않습니다. 이미 끝난 바깥 일을 반대 방향의 일로 맞추는 것을 보상 작업이라고 부르고, 결제를 취소하는 요청이 그 예입니다. 이 챕터에서는 보상 작업을 실행하지 않았습니다. 같은 일을 두 번 하지 않게 하는 멱등 키는 <a href=\"""" + L_CH23_06 + """\">Ch 23 06절</a>에서 봤습니다.</li><li>노트북 밖에서 받은 오류를 <code>print(error)</code>로 모두 찍어 보니, SQL 글과 넘긴 값, 오류 설명 주소까지 여러 줄이 나왔습니다. 이 절은 매번 같은 오류 이름·오류 코드와, 드라이버가 받은 오류 글만 출력했습니다. 오류를 가릴 때는 PostgreSQL 문서대로 글보다 오류 코드를 봅니다.</li><li>이 절은 오류 이름 <code>IntegrityError</code>만 받아 셀을 끝까지 실행했습니다. 받지 않은 오류는 Ch 2 05절에서 본 것처럼 셀 밖으로 나와 실행을 멈춥니다. 실제 서비스에서는 받은 오류를 기록하고, 요청한 쪽에 실패를 알려야 합니다.</li><li>잔액이 0보다 작아지지 않게 파이썬 코드에서 먼저 검사할 수도 있습니다. 이 절은 그런 검사를 두지 않고, 서버의 CHECK 제약이 막게 했습니다. 여러 연결이 같은 계좌를 함께 바꾸는 장면은 이 절에서 실행하지 않았습니다.</li><li>노트북을 쓰기 전에 노트북 밖에서 같은 장면을 파이썬 파일로 다섯 번 실행했고, 출력이 다섯 번 모두 같았습니다. 잔액·합계·오류 코드·오류 글 모두 실행할 때마다 같은 값입니다.</li><li>교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다. 그 서버는 Docker 컨테이너가 아니라 같은 접속 글로 켠 서버입니다. Docker 이미지로 켜면 버전 번호의 끝자리가 다를 수 있습니다. 다른 버전과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>표의 CHECK 제약은 잔액을 0보다 작게 만드는 빼기를 막았고, 받은 오류는 <code>IntegrityError</code>, 오류 코드는 <code>23514</code>였습니다.</li><li>두 변경을 블록 둘로 따로 확정하자, 빼기가 막힌 뒤에도 더하기가 남아 합계가 1600이 되었습니다.</li><li>두 변경을 블록 하나로 묶자, 같은 오류에서 두 변경이 함께 취소되어 합계가 1000으로 남았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_03 + """\">03절</a>에서는 Alembic으로 표 구조를 판마다 바꾸는 방법을 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. 표 <code>accounts</code>의 CHECK 제약은 무엇을 막았고, 막을 때 받은 오류 이름과 오류 코드는 무엇이었나요?</p><p class="quiz-a">잔액을 0보다 작게 만드는 빼기를 막았습니다. 받은 오류는 <code>IntegrityError</code>, 오류 코드는 <code>23514</code>였습니다. 틀렸다면 노트북 3절과 5절을 다시 읽습니다.</p><p class="quiz-q">2. Before 판에서 합계가 1600이 된 까닭은 무엇인가요?</p><p class="quiz-a">첫째 블록이 2번 계좌의 더하기를 이미 확정했기 때문입니다. 둘째 블록의 빼기가 막혀도, 확정된 더하기는 남았습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">3. After 판에서 블록 안에서 읽은 2번 잔액과, 블록 밖에서 다시 읽은 2번 잔액은 무엇이었나요?</p><p class="quiz-a">블록 안에서는 1100, 블록 밖에서는 500이었습니다. 빼기가 막히자 블록이 더하기까지 함께 취소했습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">4. 보낼 돈을 500으로 바꾸자 오류가 나지 않은 까닭은 무엇인가요?</p><p class="quiz-a">1번 잔액이 0이 되는데, 제약 <code>balance >= 0</code>은 0을 허용하기 때문입니다. 한 블록이 두 변경을 함께 확정해 잔액은 <code>[(1, 0), (2, 1000)]</code>이었습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">5. 동료가 「블록 안에서 결제 서비스에 요청을 보냈어도, 오류가 나면 블록이 결제까지 취소한다」고 말합니다. 맞나요?</p><p class="quiz-a">맞지 않습니다. 블록의 취소는 데이터베이스 안의 변경에만 닿습니다. 바깥에 보낸 요청은 보상 작업으로 따로 맞춰야 하고, 이 챕터에서는 실행하지 않았습니다. 틀렸다면 본문 7블록을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.sqlalchemy.org/en/20/core/connections.html">SQLAlchemy Working with Engines and Connections</a></div>확인 2026-09-29 · 블록 <code>begin()</code>은 정상으로 끝나면 확정한다고 적습니다. 오류가 나면 취소한 뒤, 그 오류를 밖으로 내보낸다고 적습니다.</li><li><div><a href="https://docs.sqlalchemy.org/en/20/core/exceptions.html">SQLAlchemy Core Exceptions</a></div>확인 2026-09-29 · 오류 <code>IntegrityError</code>는 DB-API 쪽 같은 이름 오류를 감싸고, 감싼 오류는 속성 <code>orig</code>에 있다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/tutorial-transactions.html">PostgreSQL 17 Transactions</a></div>확인 2026-09-29 · 한 묶음 작업은 여러 단계를 모두 되거나 모두 안 되는 하나의 일로 묶는다고 적습니다. 두 계좌 사이 이체를 예로 들고, 취소하면 그때까지의 변경이 모두 없어진다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/ddl-constraints.html">PostgreSQL 17 Constraints</a></div>확인 2026-09-29 · CHECK 제약은 칸 값이 참·거짓 식을 만족해야 한다는 조건이라고 적습니다. 어기는 값을 저장하려 하면 오류가 난다고 적습니다. 제약 이름을 적지 않으면 서버가 이름을 고른다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/errcodes-appendix.html">PostgreSQL 17 Error Codes</a></div>확인 2026-09-29 · 오류 코드는 다섯 글자이고, 앞 두 글자가 갈래라고 적습니다. 갈래 23은 제약 위반이고 <code>23514</code>는 <code>check_violation</code>입니다. 오류를 가릴 때는 글보다 코드를 보라고 적습니다.</li><li>설치판 sqlalchemy 2.0.43 소스 <code>ext/asyncio/engine.py</code> 1050~1068행은 <code>begin()</code>이 연결을 빌리고 <code>conn.begin()</code> 블록을 여는 자리입니다. 1419~1420행은 그 블록이 끝날 때 동기 쪽 끝내기로 넘깁니다. <code>engine/util.py</code> 143~162행은 오류가 없으면 확정하고, 오류가 있으면 취소합니다.</li><li>설치판 <code>dialects/postgresql/asyncpg.py</code> 786~791행은 드라이버 오류를 SQLAlchemy 쪽 오류로 바꿉니다. 이때 글 앞에 드라이버 오류의 종류를 붙이고, 속성 <code>sqlstate</code>를 채웁니다. 그래서 오류 글이 <code>CheckViolationError</code>로 시작합니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    # 2절 설정 셀은 01절 셀 글 그대로(「01절 2절의 설정 셀과 글자까지 같은 셀」 문장의 근거)
    assert SETTINGS in AUTHOR01.read_text(encoding="utf-8"), "SETTINGS가 01절 셀과 다릅니다"
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "02", SLUG, "paired", cells())
        print("wrote", path)
