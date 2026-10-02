"""Ch31 원본 본문, 노트북, 서비스 예제와 QA 문서를 생성합니다."""
from __future__ import annotations
# 2026-09-29 Ch 31 01절 품질 개선: 이 파일은 Ch 31 옛 노트북 다섯·_src 다섯·chapter.json·실습 폴더 파일을 출력 없이 덮어쓰는 옛 생성기입니다.
# 개선본은 textbook/part7/ch31-database/qa/upgrade/author_NN.py가 씁니다. 실행하면 개선본을 옛 판으로 덮어쓰므로, 아래 줄에서 실행을 막습니다.
# 내용은 고치지 않았습니다(이 설명 세 줄과 아래 한 줄만 더함). 옮기기는 챕터 마감 몫(qa/upgrade/before/generators/blocked/)입니다.
raise SystemExit('옛 Ch 31 생성기(qa/author_ch31.py)입니다. 실행하면 개선본 노트북·_src·chapter.json을 옛 판으로 덮어씁니다. 개선본은 qa/upgrade/author_NN.py를 쓰세요.')

import json
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[4]
TB = ROOT / "textbook/part7/ch31-database"
LAB = ROOT / "labs/part7/ch31-database"


def md(source: str, part: str | None = None) -> dict:
    metadata = {} if part is None else {"lesson_part": part}
    return {"cell_type": "markdown", "id": "", "metadata": metadata, "source": source.splitlines(keepends=True)}


def code(source: str, part: str | None = None) -> dict:
    metadata = {} if part is None else {"lesson_part": part}
    return {"cell_type": "code", "execution_count": None, "id": "", "metadata": metadata,
            "outputs": [], "source": dedent(source).strip().splitlines(keepends=True)}


def notebook(title: str, lesson_format: str, cells: list[dict]) -> dict:
    cells = [md(f"# {title}\n\n실제 PostgreSQL 17에서 운영 데이터베이스의 한 가지 문제를 재현하고 해결합니다.")] + cells
    for index, cell in enumerate(cells, 1):
        cell["id"] = f"cell-{index:02d}"
    return {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python", "version": "3.12"}, "lesson_format": lesson_format},
            "nbformat": 4, "nbformat_minor": 5}


INSTALL = code("""
# 이 챕터에서 고정한 패키지를 설치합니다.
%pip install -q 'sqlalchemy[asyncio]==2.0.43' asyncpg==0.30.0 alembic==1.16.5
%pip install -q 'psycopg[binary,pool]==3.3.3' pgvector==0.4.1
%pip install -q langgraph==1.2.11 langgraph-checkpoint-postgres==3.0.5
""")

DB_PREP = code("""
# 전용 실습 데이터베이스 주소만 준비하며 비밀 값은 출력하지 않습니다.
import os
ASYNC_URL = os.getenv(
    "CH31_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:55431/ch31_lab",
)
SYNC_URL = ASYNC_URL.replace("postgresql+asyncpg", "postgresql+psycopg")
NATIVE_URL = ASYNC_URL.replace("postgresql+asyncpg", "postgresql")
print("database: ch31_lab, credentials: hidden")
""")


NBS = {
"01-SQLAlchemy-비동기-PostgreSQL": notebook("SQLAlchemy 비동기 PostgreSQL", "experiment", [
    md("## 실행 환경 준비\n\n`AsyncEngine`과 `AsyncSession`으로 네트워크 I/O를 기다리는 동안 다른 작업을 진행할 수 있는지 확인합니다."), INSTALL, DB_PREP,
    md("## 비동기 엔진과 테이블 준비\n\n전용 `ch31_async` 스키마에 상담 요청 세 건을 저장합니다."),
    code("""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(ASYNC_URL, pool_size=3, max_overflow=0)
Session = async_sessionmaker(engine, expire_on_commit=False)
async with engine.begin() as conn:
    await conn.execute(text("DROP SCHEMA IF EXISTS ch31_async CASCADE"))
    await conn.execute(text("CREATE SCHEMA ch31_async"))
    await conn.execute(text("CREATE TABLE ch31_async.requests (id int primary key, question text)"))
    await conn.execute(text("INSERT INTO ch31_async.requests VALUES (1,'환불'),(2,'배송'),(3,'결제')"))
print("rows prepared: 3")
"""),
    md("## 세션으로 조회\n\n세션은 한 작업의 데이터베이스 대화를 나타냅니다. 작업마다 새 세션을 사용합니다."),
    code("""
async def read_question(item_id: int) -> str:
    async with Session() as session:
        result = await session.execute(
            text("SELECT question FROM ch31_async.requests WHERE id=:id"), {"id": item_id}
        )
        return result.scalar_one()

questions = [await read_question(i) for i in range(1, 4)]
print(questions)
assert questions == ["환불", "배송", "결제"]
"""),
    md("## 순차 실행과 동시 실행 비교\n\n같은 `pg_sleep(0.15)` 쿼리 세 건의 실행 방식만 바꿉니다."),
    code("""
from time import perf_counter
async def delayed_read(item_id: int) -> str:
    async with Session() as session:
        row = await session.execute(text(
            "SELECT question FROM ch31_async.requests, pg_sleep(0.15) WHERE id=:id"
        ), {"id": item_id})
        return row.scalar_one()

start = perf_counter()
sequential = [await delayed_read(i) for i in range(1, 4)]
sequential_s = perf_counter() - start
start = perf_counter()
concurrent = await asyncio.gather(*(delayed_read(i) for i in range(1, 4)))
concurrent_s = perf_counter() - start
print(f"sequential={sequential_s:.3f}s, concurrent={concurrent_s:.3f}s")
assert sequential == concurrent and concurrent_s < sequential_s
await engine.dispose()
"""),
]),
"02-트랜잭션과-원자성": notebook("트랜잭션과 원자성", "paired", [
    md("## 실행 환경 준비\n\n이체 중 오류가 발생했을 때 두 잔액 변경이 함께 취소되는지 확인합니다."), INSTALL, DB_PREP,
    code("""
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine(ASYNC_URL)
async with engine.begin() as conn:
    await conn.execute(text("DROP SCHEMA IF EXISTS ch31_tx CASCADE"))
    await conn.execute(text("CREATE SCHEMA ch31_tx"))
    account_ddl = (
        "CREATE TABLE ch31_tx.accounts("
        "id int primary key, balance int CHECK(balance>=0))"
    )
    await conn.execute(text(account_ddl))
    await conn.execute(text("INSERT INTO ch31_tx.accounts VALUES (1,500),(2,500)"))
print("initial total: 1000")
"""),
    md("## 실패 재현\n\n출금과 입금을 별도 트랜잭션으로 처리하면 첫 변경만 확정될 수 있습니다.", "before"),
    code("""
try:
    async with engine.begin() as conn:
        await conn.execute(text("UPDATE ch31_tx.accounts SET balance=balance-100 WHERE id=1"))
    raise RuntimeError("입금 직전 장애")
except RuntimeError as exc:
    print(type(exc).__name__, exc)
async with engine.connect() as conn:
    before = (await conn.execute(text("SELECT id,balance FROM ch31_tx.accounts ORDER BY id"))).all()
print("before:", before, "total:", sum(row.balance for row in before))
assert [row.balance for row in before] == [400, 500]
""", "before"),
    md("## 수정\n\n두 변경을 한 `engine.begin()` 블록에 넣으면 예외가 블록 전체를 롤백합니다.", "after"),
    code("""
async with engine.begin() as conn:
    await conn.execute(text("UPDATE ch31_tx.accounts SET balance=500"))
try:
    async with engine.begin() as conn:
        await conn.execute(text("UPDATE ch31_tx.accounts SET balance=balance-100 WHERE id=1"))
        raise RuntimeError("입금 직전 장애")
        await conn.execute(text("UPDATE ch31_tx.accounts SET balance=balance+100 WHERE id=2"))
except RuntimeError:
    pass
async with engine.connect() as conn:
    after = (await conn.execute(text("SELECT id,balance FROM ch31_tx.accounts ORDER BY id"))).all()
print("after:", after, "total:", sum(row.balance for row in after))
assert [row.balance for row in after] == [500, 500]
await engine.dispose()
""", "after"),
]),
"03-Alembic-적용과-롤백": notebook("Alembic 적용과 롤백", "paired", [
    md("## 실행 환경 준비\n\n마이그레이션 파일을 적용하고 되돌린 뒤 데이터베이스 스키마를 직접 조회합니다."), INSTALL, DB_PREP,
    code("""
import os, subprocess
from pathlib import Path
# 현재 폴더와 상위 폴더에서 제공된 마이그레이션 설정을 찾습니다.
candidates = [parent / "labs/part7/ch31-database" for parent in (Path.cwd(), *Path.cwd().parents)]
candidates += [Path.cwd(), Path.cwd().parent]
LAB_ROOT = next(path for path in candidates if (path / "alembic.ini").is_file())
env = os.environ | {"CH31_SYNC_URL": SYNC_URL}
def alembic(*args: str) -> str:
    result = subprocess.run(
        ["alembic", "-c", str(LAB_ROOT / "alembic.ini"), *args],
        cwd=LAB_ROOT, env=env, text=True, capture_output=True, check=True,
    )
    return (result.stdout + result.stderr).strip()
print("migration directory:", LAB_ROOT.name)
"""),
    md("## 마이그레이션 적용\n\n`upgrade head`가 표와 버전 기록을 함께 만드는지 확인합니다."),
    code("""
import psycopg
with psycopg.connect(NATIVE_URL, autocommit=True) as conn:
    conn.execute("DROP SCHEMA IF EXISTS ch31_migration CASCADE")
print(alembic("upgrade", "head").splitlines()[-1])
with psycopg.connect(NATIVE_URL) as conn:
    applied = conn.execute("SELECT to_regclass('ch31_migration.tickets')::text").fetchone()[0]
print("applied table:", applied)
assert applied == "ch31_migration.tickets"
"""),
    md("## 실패 확인\n\n`downgrade base` 뒤에는 이전 코드가 기대하던 표를 조회할 수 없습니다.", "before"),
    code("""
print(alembic("downgrade", "base").splitlines()[-1])
with psycopg.connect(NATIVE_URL) as conn:
    removed = conn.execute("SELECT to_regclass('ch31_migration.tickets')").fetchone()[0]
print("after downgrade:", removed)
assert removed is None
""", "before"),
    md("## 수정\n\n배포 코드와 맞는 리비전을 다시 적용해 표를 복구합니다.", "after"),
    code("""
print(alembic("upgrade", "head").splitlines()[-1])
with psycopg.connect(NATIVE_URL) as conn:
    restored = conn.execute("SELECT to_regclass('ch31_migration.tickets')::text").fetchone()[0]
print("restored:", restored)
assert restored == "ch31_migration.tickets"
""", "after"),
]),
"04-커넥션-풀-고갈과-대응": notebook("커넥션 풀 고갈과 대응", "paired", [
    md("## 실행 환경 준비\n\n연결 한 개만 허용한 풀에서 두 번째 작업이 기다리다 실패하는 상황을 재현합니다."), INSTALL, DB_PREP,
    md("## 실패 재현\n\n첫 작업이 연결을 점유한 동안 두 번째 작업의 대기 제한을 0.2초로 둡니다.", "before"),
    code("""
import asyncio
from sqlalchemy import text
from sqlalchemy.exc import TimeoutError
from sqlalchemy.ext.asyncio import create_async_engine

small = create_async_engine(ASYNC_URL, pool_size=1, max_overflow=0, pool_timeout=0.2)
async def hold_connection(delay: float) -> None:
    async with small.connect() as conn:
        await conn.execute(text("SELECT pg_sleep(:delay)"), {"delay": delay})
holder = asyncio.create_task(hold_connection(0.6))
await asyncio.sleep(0.05)
try:
    await hold_connection(0.01)
except TimeoutError as exc:
    exhausted = type(exc).__name__
await holder
print("before:", exhausted)
assert exhausted == "TimeoutError"
await small.dispose()
""", "before"),
    md("## 수정\n\n대기 제한을 실제 쿼리 시간보다 길게 두고, 연결 블록을 짧게 유지합니다.", "after"),
    code("""
healthy = create_async_engine(ASYNC_URL, pool_size=1, max_overflow=0, pool_timeout=1.0)
async def short_query(delay: float) -> int:
    async with healthy.connect() as conn:
        result = await conn.execute(
            text("SELECT 1 FROM pg_sleep(:delay)"), {"delay": delay}
        )
        return result.scalar_one()
first = asyncio.create_task(short_query(0.25))
await asyncio.sleep(0.05)
second = await short_query(0.01)
print("after:", await first, second, healthy.pool.status())
assert second == 1
await healthy.dispose()
""", "after"),
]),
"05-pgvector-체크포인터-공존과-백업": notebook("pgvector·체크포인터 공존과 백업", "experiment", [
    md("## 실행 환경 준비\n\n한 스키마에 애플리케이션 벡터 표와 LangGraph 체크포인터 표를 만들고 논리 백업에 함께 포함되는지 확인합니다."), INSTALL, DB_PREP,
    code("""
import os, subprocess
import psycopg
from langgraph.checkpoint.postgres import PostgresSaver

BASE_URL = NATIVE_URL
with psycopg.connect(BASE_URL, autocommit=True) as conn:
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.execute("DROP SCHEMA IF EXISTS ch31_shared CASCADE")
    conn.execute("CREATE SCHEMA ch31_shared")
shared_url = BASE_URL + "?options=-csearch_path%3Dch31_shared%2Cpublic"
print("schema: ch31_shared")
"""),
    md("## 벡터 표와 HNSW 인덱스\n\n세 문서를 저장하고 코사인 거리용 HNSW 인덱스를 만듭니다."),
    code("""
with psycopg.connect(shared_url, autocommit=True) as conn:
    conn.execute("CREATE TABLE documents(id int primary key, content text, embedding vector(3))")
    rows = "(1,'배송','[1,0,0]'),(2,'환불','[0,1,0]'),(3,'결제','[0,0,1]')"
    conn.execute("INSERT INTO documents VALUES " + rows)
    index_ddl = (
        "CREATE INDEX documents_embedding_hnsw ON documents "
        "USING hnsw (embedding vector_cosine_ops)"
    )
    conn.execute(index_ddl)
with psycopg.connect(shared_url) as conn:
    nearest = conn.execute(
        "SELECT content FROM documents "
        "ORDER BY embedding <=> '[0.9,0.1,0]' LIMIT 2"
    ).fetchall()
print("nearest:", [row[0] for row in nearest])
assert nearest[0][0] == "배송"
"""),
    md("## 실제 쿼리 계획\n\n행이 세 개뿐인 표에서 최적화기가 HNSW보다 순차 스캔을 선택하는지 실행 계획을 읽습니다."),
    code("""
with psycopg.connect(shared_url) as conn:
    plan_rows = conn.execute(
        "EXPLAIN (ANALYZE, BUFFERS, COSTS OFF) "
        "SELECT content FROM documents "
        "ORDER BY embedding <=> '[0.9,0.1,0]' LIMIT 2"
    ).fetchall()
plan = "\\n".join(row[0] for row in plan_rows)
print(plan)
print("uses hnsw:", "documents_embedding_hnsw" in plan)
assert "Scan" in plan and "Execution Time" in plan
"""),
    md("## 체크포인터 표 공존\n\n공식 체크포인터 구현의 `setup()`으로 같은 스키마에 운영 표를 추가합니다."),
    code("""
with PostgresSaver.from_conn_string(shared_url) as saver:
    saver.setup()
    from typing_extensions import TypedDict
    from langgraph.graph import END, START, StateGraph
    class State(TypedDict):
        value: int
    graph_builder = StateGraph(State)
    graph_builder.add_node("double", lambda state: {"value": state["value"] * 2})
    graph_builder.add_edge(START, "double")
    graph_builder.add_edge("double", END)
    graph = graph_builder.compile(checkpointer=saver)
    saved = graph.invoke({"value": 6}, {"configurable": {"thread_id": "backup-demo"}})
with psycopg.connect(BASE_URL) as conn:
    tables = [row[0] for row in conn.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema='ch31_shared' ORDER BY table_name"
    )]
    checkpoint_count = conn.execute(
        "SELECT count(*) FROM ch31_shared.checkpoints"
    ).fetchone()[0]
print("saved:", saved, "checkpoint rows:", checkpoint_count)
assert saved["value"] == 12 and checkpoint_count > 0
"""),
    md("## 논리 백업 확인\n\n전용 스키마를 SQL 형식으로 덤프하고 두 종류의 표 정의가 모두 포함되는지 검사합니다."),
    code("""
container = os.getenv("CH31_POSTGRES_CONTAINER", "kdt-ch31-postgres")
dump = subprocess.run(
    ["docker", "exec", container, "pg_dump", "-U", "postgres", "-d", "ch31_lab",
     "--schema=ch31_shared", "--no-owner", "--no-privileges"],
    text=True, capture_output=True, check=True,
).stdout
for command in (["dropdb", "-U", "postgres", "--if-exists", "ch31_restore"],
                ["createdb", "-U", "postgres", "ch31_restore"]):
    subprocess.run(["docker", "exec", container, *command], check=True)
subprocess.run(
    ["docker", "exec", container, "psql", "-U", "postgres", "-d", "ch31_restore",
     "-c", "CREATE EXTENSION vector"], check=True, capture_output=True,
)
subprocess.run(
    ["docker", "exec", "-i", container, "psql", "-U", "postgres", "-d", "ch31_restore"],
    input=dump, text=True, check=True, capture_output=True,
)
restore_url = BASE_URL.replace("/ch31_lab", "/ch31_restore")
with psycopg.connect(restore_url) as conn:
    restored = conn.execute("SELECT (SELECT count(*) FROM ch31_shared.documents), "
                            "(SELECT count(*) FROM ch31_shared.checkpoints)").fetchone()
    index_ok = conn.execute("SELECT to_regclass('ch31_shared.documents_embedding_hnsw') IS NOT NULL").fetchone()[0]
print("restored rows:", restored, "hnsw:", index_ok)
assert "CREATE TABLE ch31_shared.documents" in dump
assert restored[0] == 3 and restored[1] > 0 and index_ok
"""),
]),
}


INFO = {
"01-SQLAlchemy-비동기-PostgreSQL": {
"title":"SQLAlchemy 비동기 PostgreSQL", "hours":"강의 1h · 실습 2h", "terms":"AsyncEngine, AsyncSession, 비동기 I/O, 커넥션 풀",
"why":"Ch30에서 FastAPI 요청 함수를 비동기로 작성했습니다. 요청 함수가 데이터베이스를 기다리는 동안 이벤트 루프까지 멈추면 다른 사용자의 요청을 처리하지 못합니다. 이 절에서는 비동기 드라이버와 세션을 사용해 같은 조회 세 건을 순차 실행과 동시 실행으로 비교합니다.",
"prior":"Ch2에서 `async`와 `await`가 대기 가능한 작업을 표현한다는 점을 배웠고, Ch30에서는 FastAPI 경로 함수를 비동기로 작성했습니다. Ch4에서 만든 관계형 표와 기본 SQL도 다시 사용합니다.",
"concept":"식당의 주문 담당자가 한 주문의 조리가 끝날 때까지 계산대 앞에 서 있으면 다음 손님을 받지 못합니다. 주문표를 주방에 넘긴 뒤 다른 주문을 받으면 같은 시간에 더 많은 손님을 응대할 수 있습니다. 비동기 입력·출력(asynchronous I/O)은 데이터베이스 응답처럼 외부 작업을 기다리는 동안 이벤트 루프가 다른 작업을 진행하게 하는 방식입니다. `AsyncEngine`은 비동기 드라이버와 연결 풀을 관리하고, `AsyncSession`은 한 업무 작업에서 실행한 조회와 변경을 묶습니다. 하나의 세션은 변경 가능한 상태를 가지므로 여러 `asyncio` 작업이 공유하지 않습니다. 각 작업이 세션 팩터리에서 자기 세션을 받아야 합니다.",
"observed":"실제 실행에서는 0.15초 대기 쿼리 세 건의 순차 실행 시간이 약 0.46초였고, 연결 세 개로 동시 실행한 시간은 약 0.20초였습니다. 운영 성능 전체를 뜻하지 않으며, 인위적인 대기와 로컬 네트워크에서 동시 대기의 차이만 보여 줍니다.",
"notes":["비동기 함수 안에서 동기 데이터베이스 드라이버를 호출하면 이벤트 루프가 멈출 수 있습니다.","`AsyncSession` 하나를 여러 동시 작업이 공유하면 트랜잭션 상태가 섞일 수 있습니다.","애플리케이션 종료 시 `await engine.dispose()`로 풀의 유휴 연결을 정리합니다."],
"next":"다음 절에서는 세션과 연결이 변경 작업을 어떤 단위로 확정하고 되돌리는지 확인합니다.",
"quiz":[("`AsyncEngine`을 사용하는 주된 이유는 무엇인가요?","데이터베이스 응답을 기다리는 동안 이벤트 루프가 다른 작업을 처리할 수 있게 하기 위해서입니다."),("`AsyncSession`을 여러 동시 작업이 공유해도 되나요?","안 됩니다. 세션은 한 논리 트랜잭션의 변경 가능한 상태를 가지므로 작업마다 별도 세션을 사용합니다."),("동시 실행 시간이 짧아진 결과가 모든 쿼리의 성능 향상을 보장하나요?","보장하지 않습니다. 이 실험은 독립적인 대기 쿼리 세 건과 연결 세 개라는 조건에서만 동시 대기 효과를 확인했습니다."),("엔진을 마칠 때 호출한 메서드는 무엇인가요?","`await engine.dispose()`이며 풀의 유휴 연결을 정리합니다.")],
"refs":["https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html · 확인 2026-09-11 · SQLAlchemy 2.0","https://docs.sqlalchemy.org/en/20/orm/session_basics.html · 확인 2026-09-11 · 세션 동시성"]},
"02-트랜잭션과-원자성": {
"title":"트랜잭션과 원자성", "hours":"강의 1h · 실습 2h", "terms":"트랜잭션, 원자성, commit, rollback, 격리 수준",
"why":"에이전트 서비스는 메시지 저장, 사용량 차감, 작업 상태 갱신을 한 요청에서 함께 수행할 수 있습니다. 중간 단계만 데이터베이스에 남으면 다음 재개에서 사실과 다른 상태를 읽습니다. 이 절에서는 이체의 출금과 입금을 사용해 함께 확정하거나 함께 취소하는 경계를 확인합니다.",
"prior":"앞 절에서 작업마다 비동기 세션을 만들었습니다. Ch23에서는 중단 뒤 재개와 멱등성을 배웠습니다. 여기서는 재개가 읽을 데이터 자체를 서로 맞게 저장하는 방법을 다룹니다.",
"concept":"은행 창구에서 한 계좌의 돈만 줄이고 상대 계좌의 돈을 늘리지 않으면 장부 총액이 달라집니다. 두 기록은 하나의 업무 단위로 처리해야 합니다. 트랜잭션(transaction)은 여러 SQL 문을 하나의 확정 단위로 묶습니다. 원자성(atomicity)은 그 안의 변경이 모두 반영되거나 모두 취소되는 성질입니다. `commit`은 변경을 확정하고 `rollback`은 아직 확정하지 않은 변경을 취소합니다. PostgreSQL의 기본 격리 수준인 READ COMMITTED에서는 각 문장이 시작될 때 이미 확정된 행을 봅니다. 더 강한 격리 수준은 동시 변경 이상을 줄이지만 충돌 재시도 가능성과 비용도 함께 고려해야 합니다.",
"observed":"Before에서는 출금 트랜잭션이 먼저 확정된 뒤 장애가 발생해 잔액이 400과 500, 총액이 900으로 남았습니다. After에서는 두 변경을 같은 `engine.begin()` 블록에 넣었습니다. 입금 전 예외가 블록 전체를 롤백해 두 잔액은 500과 500, 총액 1000을 유지했습니다.",
"notes":["트랜잭션을 오래 유지하면 잠금과 풀 연결 점유 시간이 늘어납니다.","외부 결제 API 호출은 데이터베이스 롤백으로 취소되지 않으므로 멱등성 키와 보상 작업이 필요합니다.","SERIALIZABLE에서 충돌로 취소된 트랜잭션은 같은 업무 키로 안전하게 재시도해야 합니다."],
"next":"다음 절에서는 트랜잭션을 사용하는 코드가 기대하는 표 구조를 버전별 마이그레이션으로 관리합니다.",
"quiz":[("원자성은 어떤 상태를 보장하나요?","한 트랜잭션 안의 변경이 전부 확정되거나 전부 취소되는 상태를 보장합니다."),("Before의 총액이 900이 된 이유는 무엇인가요?","출금이 별도 트랜잭션에서 먼저 커밋된 뒤 입금 전에 장애가 발생했기 때문입니다."),("`engine.begin()` 블록에서 예외가 나면 어떻게 되나요?","블록에서 시작한 아직 확정되지 않은 트랜잭션을 롤백합니다."),("외부 API 호출도 데이터베이스 롤백으로 취소되나요?","취소되지 않습니다. 멱등성 키나 보상 작업을 별도로 설계해야 합니다.")],
"refs":["https://docs.sqlalchemy.org/en/20/core/connections.html · 확인 2026-09-11 · 트랜잭션","https://www.postgresql.org/docs/current/sql-set-transaction.html · 확인 2026-09-11 · PostgreSQL 18 문서"]},
"03-Alembic-적용과-롤백": {
"title":"Alembic 적용과 롤백", "hours":"강의 1h · 실습 2h", "terms":"마이그레이션, revision, upgrade, downgrade",
"why":"코드 배포에서 모델 필드를 추가해도 이미 운영 중인 데이터베이스 표는 자동으로 바뀌지 않습니다. 코드와 스키마 버전이 어긋나면 요청이 시작된 뒤에야 없는 열이나 표 오류가 나타납니다. 이 절에서는 변경 파일을 버전 기록으로 남기고 적용과 롤백을 실제 카탈로그 조회로 확인합니다.",
"prior":"Ch4에서 `CREATE TABLE`을 실행했고 앞 절에서는 트랜잭션 경계를 정했습니다. Alembic은 이 DDL 변경의 순서와 현재 적용 위치를 파일과 버전 표로 관리합니다.",
"concept":"건물 도면을 지우고 매번 새로 그리면 어느 공사에서 문제가 생겼는지 알기 어렵습니다. 변경 도면에 번호를 붙이고 순서대로 적용하면 현재 상태와 되돌릴 지점을 확인할 수 있습니다. 마이그레이션(migration)은 데이터베이스 구조 변경을 순서가 있는 코드로 기록하는 작업입니다. 리비전(revision)은 한 변경의 식별자이며 `down_revision`은 바로 앞 변경을 가리킵니다. `upgrade()`는 앞으로 적용할 DDL을, `downgrade()`는 되돌릴 DDL을 작성합니다. 자동 생성은 모델과 데이터베이스의 차이를 초안으로 만들 뿐이므로, 데이터 손실 가능성과 제약 조건을 사람이 읽어야 합니다.",
"observed":"`upgrade head` 뒤에는 `ch31_migration.tickets`와 Alembic 버전 기록이 생성되었습니다. `downgrade base` 뒤 `to_regclass`는 NULL을 반환해 표가 제거됐음을 확인했습니다. 다시 `upgrade head`를 실행하자 같은 표가 복구되었습니다. 표를 되돌렸다는 사실만 확인했으며 운영 데이터가 안전하게 복원된다는 뜻은 아닙니다.",
"notes":["삭제 열이나 타입 축소는 롤백만으로 데이터를 복구하지 못할 수 있으므로 먼저 백업과 복원 연습이 필요합니다.","여러 애플리케이션 인스턴스가 시작할 때 동시에 마이그레이션을 실행하지 않도록 배포 단계에서 한 번 실행합니다.","자동 생성 결과에는 이름 없는 제약 조건과 데이터 변환 절차가 빠질 수 있어 파일을 검토해야 합니다."],
"next":"다음 절에서는 요청이 늘 때 마이그레이션된 데이터베이스 연결을 풀에서 어떻게 빌리고 반환하는지 확인합니다.",
"quiz":[("리비전의 `down_revision`은 무엇을 가리키나요?","현재 변경 바로 앞에 적용되어야 하는 리비전을 가리킵니다."),("`upgrade head`의 `head`는 무엇인가요?","현재 마이그레이션 계보에서 가장 최신 리비전을 뜻합니다."),("자동 생성 파일을 그대로 적용하면 안 되는 이유는 무엇인가요?","Alembic이 의도와 데이터 변환 안전성을 모두 알 수 없으므로 생성된 DDL과 손실 가능성을 사람이 확인해야 합니다."),("이 실습의 롤백 검사가 보장하지 않는 것은 무엇인가요?","운영 데이터가 백업 없이 복원된다는 점은 보장하지 않습니다.")],
"refs":["https://alembic.sqlalchemy.org/en/latest/tutorial.html · 확인 2026-09-11 · Alembic 1.16","https://alembic.sqlalchemy.org/en/latest/autogenerate.html · 확인 2026-09-11 · 자동 생성"]},
"04-커넥션-풀-고갈과-대응": {
"title":"커넥션 풀 고갈과 대응", "hours":"강의 1h · 실습 2h", "terms":"커넥션 풀, pool_size, max_overflow, pool_timeout",
"why":"FastAPI가 동시에 많은 요청을 받아도 PostgreSQL이 허용하는 연결 수는 제한되어 있습니다. 요청마다 새 연결을 무제한으로 만들거나 반환을 늦추면 데이터베이스가 정상이어도 애플리케이션에서 대기 시간 초과가 발생합니다. 이 절에서는 크기 1인 풀을 의도적으로 고갈시키고 대기 제한과 연결 범위를 조정합니다.",
"prior":"첫 절에서 `AsyncEngine`이 연결 풀을 관리한다는 점을 확인했습니다. 앞 절까지 만든 트랜잭션과 마이그레이션도 결국 풀에서 빌린 연결로 실행됩니다.",
"concept":"도서관에 열람용 태블릿이 한 대뿐이면 한 사람이 반납할 때까지 다음 사람이 기다립니다. 반납 시간이 없으면 대기열은 끝없이 늘어납니다. 커넥션 풀(connection pool)은 미리 열어 둔 데이터베이스 연결을 요청에 빌려주고 사용 뒤 다시 보관하는 구성 요소입니다. `pool_size`는 유지하는 연결 수, `max_overflow`는 순간적으로 추가할 연결 수, `pool_timeout`은 연결을 얻기 위해 기다릴 최대 초입니다. 이 값은 각각 크게 정하는 문제가 아닙니다. 애플리케이션 프로세스 수를 곱한 전체 연결 수가 PostgreSQL 한도와 운영 여유 안에 들어가야 합니다.",
"observed":"Before에서는 풀 크기 1, 추가 연결 0, 대기 제한 0.2초로 설정했습니다. 첫 쿼리가 0.6초 동안 연결을 점유하자 두 번째 쿼리는 `TimeoutError`를 냈습니다. After에서는 첫 작업을 0.25초로 줄이고 대기 제한을 1초로 늘렸습니다. 두 번째 작업은 첫 연결이 반환된 뒤 같은 풀 연결을 받아 1을 반환했습니다.",
"notes":["대기 제한만 늘리면 오류가 늦게 나타날 뿐 처리량 문제는 남을 수 있습니다.","세션과 결과 스트림을 요청 수명보다 오래 보관하지 말고 필요한 데이터만 읽은 뒤 연결을 반환합니다.","프로세스가 네 개면 프로세스별 풀 설정의 합계를 계산하고 관리자·마이그레이션용 연결 여유도 남깁니다."],
"next":"마지막 절에서는 같은 PostgreSQL 인스턴스에 벡터 표와 체크포인터 표가 있을 때 색인과 백업 범위를 확인합니다.",
"quiz":[("`pool_timeout`은 무엇을 제한하나요?","풀에서 사용 가능한 연결을 얻기 위해 기다리는 최대 시간을 제한합니다."),("풀 크기를 무조건 크게 잡을 수 없는 이유는 무엇인가요?","여러 프로세스의 풀 합계가 PostgreSQL 연결 한도와 메모리를 소모하기 때문입니다."),("Before에서 `TimeoutError`가 난 직접 원인은 무엇인가요?","유일한 연결이 0.6초 동안 점유됐는데 두 번째 작업의 대기 제한은 0.2초였기 때문입니다."),("After에서 함께 바꾼 두 조건은 무엇인가요?","연결 점유 시간을 줄이고 대기 제한을 실제 쿼리 시간보다 길게 정했습니다.")],
"refs":["https://docs.sqlalchemy.org/en/20/core/pooling.html · 확인 2026-09-11 · SQLAlchemy 2.0","https://docs.sqlalchemy.org/en/20/errors.html#queuepool-limit-of-size-x-overflow-y-reached-connection-timed-out-timeout-z · 확인 2026-09-11"]},
"05-pgvector-체크포인터-공존과-백업": {
"title":"pgvector·체크포인터 공존과 백업", "hours":"강의 1h · 실습 3h", "terms":"HNSW, 연산자 클래스, 체크포인터, 논리 백업, 복원 연습",
"why":"에이전트 서비스는 검색 문서와 실행 상태를 같은 PostgreSQL에 저장할 수 있습니다. 벡터 표만 백업하면 대화 재개 정보가 사라지고, 체크포인터 표만 백업하면 검색 결과를 다시 만들 시간과 원본이 필요합니다. 마지막 절에서는 두 표 집합이 함께 존재하는 구조와 HNSW 인덱스, 논리 백업의 포함 범위를 확인합니다.",
"prior":"Ch12에서 pgvector의 거리 연산과 HNSW를 사용했고 Ch23에서는 PostgresSaver의 `setup()`이 체크포인터 표를 만든다는 점을 확인했습니다. 이번 절은 두 결과를 한 운영 스키마에서 함께 관리합니다.",
"concept":"한 창고에 상품과 배송 장부를 함께 보관하면 창고 주소는 하나지만 재고와 장부의 수명과 복구 우선순위는 다릅니다. PostgreSQL 스키마는 관련 표의 이름 공간을 나누며, 인덱스는 특정 표의 조회 경로를 추가합니다. HNSW(Hierarchical Navigable Small World)는 여러 층의 근접 그래프를 탐색하는 근사 최근접 이웃 인덱스입니다. 코사인 거리 쿼리에는 `vector_cosine_ops` 연산자 클래스를 맞춰야 합니다. 체크포인터는 그래프 실행 단계의 상태와 중간 쓰기를 저장합니다. 논리 백업(logical backup)은 `pg_dump`가 스키마와 행을 SQL 또는 아카이브 형식으로 추출하는 방식입니다. 백업 파일의 존재만으로 복구가 보장되지 않으므로 별도 데이터베이스에 복원하고 애플리케이션 조회까지 확인해야 합니다.",
"observed":"전용 `ch31_shared` 스키마에 문서 세 건과 코사인 HNSW 인덱스를 만들었습니다. `[0.9,0.1,0]`에 가장 가까운 문서는 ‘배송’이었습니다. 데이터가 세 행뿐이어서 실제 `EXPLAIN (ANALYZE, BUFFERS)`에서는 최적화기가 순차 스캔을 선택했습니다. 인덱스를 만들었다는 사실만으로 모든 쿼리가 그 인덱스를 사용하지 않음을 확인했습니다. PostgresSaver로 value 6을 12로 계산한 체크포인트를 실제 저장했습니다. 논리 덤프를 별도 `ch31_restore` 데이터베이스에 복원한 뒤 문서 3행, 1개 이상의 체크포인트 행, HNSW 인덱스를 다시 조회했습니다.",
"notes":["근사 인덱스는 정확 검색과 속도·재현율 특성이 다르므로 Ch11 평가셋으로 변경 전후를 측정합니다.","WAL과 정기 논리 백업은 목적이 다릅니다. 필요한 복구 시점과 허용 손실 시간을 먼저 정합니다.","백업에는 확장 설치 명령과 역할·권한이 환경에 따라 다르게 포함될 수 있으므로 깨끗한 복원 대상에서 연습합니다.","벡터를 원문에서 다시 만들 수 있더라도 사용한 임베딩 모델 버전과 전처리 설정을 함께 보관해야 같은 결과를 재현할 수 있습니다."],
"next":"Ch32에서는 이 애플리케이션과 PostgreSQL·pgvector를 Compose 서비스로 묶고 헬스체크와 시크릿을 설정합니다.",
"quiz":[("코사인 거리용 HNSW 인덱스에 사용한 연산자 클래스는 무엇인가요?","`vector_cosine_ops`입니다."),("검색 표와 체크포인터 표를 함께 확인한 이유는 무엇인가요?","한 에이전트 서비스의 검색 데이터와 실행 재개 상태가 같은 백업 범위에 포함되는지 확인하기 위해서입니다."),("백업 파일이 만들어지면 복구 준비가 끝났다고 볼 수 있나요?","볼 수 없습니다. 별도 데이터베이스에 복원하고 표, 행, 인덱스, 애플리케이션 조회를 확인해야 합니다."),("벡터를 다시 생성할 때 함께 보관해야 할 정보는 무엇인가요?","원문뿐 아니라 임베딩 모델 버전과 전처리 설정을 함께 보관해야 합니다."),("HNSW를 추가하면 정확 검색과 결과가 항상 같나요?","항상 같지 않습니다. 근사 검색이므로 평가셋에서 재현율과 지연을 함께 측정해야 합니다.")],
"refs":["https://github.com/pgvector/pgvector · 확인 2026-09-11 · pgvector 0.8.1 실습","https://www.postgresql.org/docs/current/app-pgdump.html · 확인 2026-09-11 · PostgreSQL 18 문서","https://github.com/langchain-ai/langgraph/tree/main/libs/checkpoint-postgres · 확인 2026-09-11 · checkpoint-postgres 3.0"]},
}


def source(slug: str, item: dict, fmt: str) -> str:
    diagram = f"{{{{svg:{slug.split('-',1)[0]}-흐름}}}}"
    quiz = "".join(f'<details class="quiz"><summary>{i}. {q}</summary><p class="quiz-a"><b>해설</b> — {a}</p></details>' for i,(q,a) in enumerate(item["quiz"],1))
    notes = "".join(f"<li>{x}</li>" for x in item["notes"])
    refs = "".join(
        f'<li><a href="{x.split(" · ", 1)[0]}">{item["title"]} 공식 문서</a> · {x.split(" · ", 1)[1]}</li>'
        for x in item["refs"]
    )
    title6 = "실험 결과 해석" if fmt == "experiment" else "일부러 실패해 보기"
    nb1 = f"{{{{notebook:{slug}}}}}" if fmt == "experiment" else f"{{{{notebook:{slug}|example}}}}"
    nb2 = "" if fmt == "experiment" else f"{{{{notebook:{slug}|failure}}}}"
    diagram_reading = {
        "01": "푸른 요청 상자에서 시작해 붉은 세션 상자와 초록 연결 풀을 지나 보라색 PostgreSQL 응답으로 이동합니다. 색은 처리 단계를 구분하며 실패 여부를 뜻하지 않습니다.",
        "02": "푸른 출금 뒤 붉은 트랜잭션 경계 안에서 초록색 오류를 만나면 보라색 전체 롤백으로 이동합니다. 화살표는 변경을 확정하기 전의 실행 순서입니다.",
        "03": "푸른 리비전 파일을 붉은 upgrade 명령이 적용하면 초록색 버전 표와 tickets 표가 생깁니다. 보라색 downgrade는 반대 방향 변경을 실행합니다.",
        "04": "푸른 동시 요청이 붉은 크기 1인 풀에 모이고 초록색 대기 제한을 지납니다. 보라색 마지막 상자는 연결 반환과 TimeoutError 두 결과가 갈리는 지점입니다.",
        "05": "푸른 문서·HNSW와 붉은 체크포인터 표가 초록색 ch31_shared 스키마에 공존합니다. 보라색 pg_dump 상자는 이 스키마를 선택한 논리 백업입니다.",
    }[slug[:2]]
    operation_note = {
        "01": "운영 코드에서는 엔진을 애플리케이션 시작 시 한 번 만들고 요청마다 다시 만들지 않습니다. 엔진은 접속 주소와 풀을 오래 유지하고, 세션은 요청이나 백그라운드 작업 한 건처럼 짧은 범위에서 생성합니다. FastAPI 의존성이라면 `yield` 앞에서 세션을 만들고 뒤에서 닫아 반환할 수 있습니다. 조회 결과를 모두 메모리에 옮긴 뒤 응답을 만드는지, 결과 스트림을 보내는 동안에도 연결을 점유하는지 구분해야 합니다. 후자는 느린 클라이언트 한 명이 연결을 오래 차지할 수 있습니다. 또한 비동기는 데이터베이스가 SQL을 더 빨리 계산하게 만들지 않습니다. 여러 독립 작업의 대기 시간을 겹칠 수 있게 합니다. CPU를 많이 쓰는 변환이나 하나의 트랜잭션 안에서 순서가 필요한 SQL은 `gather`로 묶는 대상이 아닙니다. 동시 실행을 늘리기 전에 작업이 서로 독립적인지, 풀에 충분한 연결이 있는지, PostgreSQL이 추가 부하를 감당하는지 차례로 확인합니다.",
        "02": "트랜잭션 경계는 함수의 길이가 아니라 업무 규칙으로 정합니다. 주문 상태를 ‘결제 완료’로 바꾸는 일과 결제 이력을 추가하는 일이 함께 성립해야 한다면 같은 경계에 둡니다. 조회 결과를 화면에 표시하는 작업까지 트랜잭션에 포함해 연결을 오래 점유할 필요는 없습니다. 예외를 잡은 뒤 계속 세션을 사용하려면 먼저 롤백이 끝났는지도 확인합니다. 데이터베이스 제약 조건은 마지막 방어선입니다. 잔액이 음수가 될 수 없다면 CHECK 제약을 두고, 업무 한 건이 중복 저장되면 안 된다면 고유 키를 둡니다. 애플리케이션의 사전 검사만으로는 두 동시 요청이 같은 값을 보고 함께 통과할 수 있습니다. 격리 수준을 높일 때는 실패가 사라진다고 가정하지 않습니다. 충돌한 트랜잭션이 취소될 수 있으므로 재시도 횟수, 같은 업무 식별자, 사용자에게 보여 줄 결과를 함께 설계합니다.",
        "03": "배포 순서는 새 코드와 이전 코드가 잠시 함께 실행될 수 있다는 전제에서 정합니다. 새 열을 바로 필수로 만들기보다 먼저 NULL을 허용해 추가하고, 새 코드가 값을 쓰게 한 뒤 기존 행을 채우고, 마지막 배포에서 제약을 강화하는 방식이 안전할 수 있습니다. 이를 확장과 축소 패턴이라고 부릅니다. 롤백 파일도 작성 가능하다는 사실과 운영에서 안전하게 실행 가능하다는 사실은 다릅니다. 열을 삭제한 뒤 downgrade로 같은 이름의 열을 다시 만들더라도 원래 행 값은 돌아오지 않습니다. 큰 표의 인덱스 생성은 오랜 잠금이나 많은 I/O를 만들 수 있으므로 PostgreSQL 버전과 `CREATE INDEX CONCURRENTLY` 사용 조건을 따로 검토합니다. CI에서는 빈 데이터베이스에 처음부터 head까지 적용하는 경로와, 현재 운영 리비전에서 다음 리비전으로 이동하는 경로를 모두 시험합니다. 배포 기록에는 적용한 리비전 ID와 실행 시간을 남겨 장애 시 코드 버전과 스키마 버전을 함께 찾을 수 있게 합니다.",
        "04": "풀 설정은 프로세스 하나의 숫자만 보면 부족합니다. 예를 들어 웹 프로세스 네 개가 `pool_size=5`, `max_overflow=5`를 사용하면 순간 최대 연결은 40개가 될 수 있습니다. 여기에 작업 프로세스, 관리자 접속, 마이그레이션 연결을 더한 값이 PostgreSQL의 허용 범위 안에 있어야 합니다. 풀 고갈 지표는 오류 수만이 아닙니다. 연결 체크아웃 대기 시간, 체크아웃된 연결 수, 쿼리 시간, 트랜잭션 시간을 함께 관찰해야 원인이 느린 SQL인지 반환 누락인지 구분할 수 있습니다. `pool_pre_ping`은 오래된 연결을 사용하기 전에 상태를 확인하는 데 도움을 주지만 매번 추가 왕복이 생깁니다. `pool_recycle`은 일정 시간이 지난 연결을 교체하지만 실행 중인 쿼리를 빠르게 만들지는 않습니다. 요청 제한과 백프레셔도 필요합니다. 데이터베이스가 처리할 수 있는 수보다 많은 작업을 무제한으로 대기시키면 메모리와 사용자 대기 시간만 늘어납니다. 짧은 대기 뒤 명확한 오류를 반환하고 재시도 정책을 적용할지 업무 특성에 따라 결정합니다.",
        "05": "공존 설계에서는 같은 서버를 쓴다는 사실보다 소유권과 복구 순서를 문서로 남기는 일이 중요합니다. 애플리케이션 마이그레이션이 체크포인터 패키지가 만든 표를 변경하지 않게 스키마와 권한을 나눌 수 있습니다. 백업 범위에는 표뿐 아니라 확장, 함수, 인덱스, 시퀀스와 필요한 역할을 검토합니다. HNSW 인덱스는 원본 벡터 행에서 다시 만들 수 있으므로 복구 시간을 줄이기 위해 백업할지, 백업 크기를 줄이고 복원 뒤 재생성할지 선택할 수 있습니다. 선택은 데이터량과 허용 복구 시간에 달려 있습니다. 체크포인터는 오래된 스레드를 계속 보관하면 빠르게 늘 수 있으므로 제품의 보존 기간과 삭제 작업을 정합니다. `pg_dump`는 실행 시점의 서로 맞는 스냅샷을 만들지만, 지속 복제나 시점 복구 전체를 대신하지 않습니다. 정기 복원 훈련에서는 새 데이터베이스에 확장을 설치하고 덤프를 복원한 뒤 최근 스레드 재개, 문서 검색, 인덱스 존재와 권한을 애플리케이션 경로로 확인합니다.",
    }[slug[:2]]
    summaries = {
        "01": ["`AsyncEngine`은 비동기 드라이버와 연결 풀을 관리합니다.", "동시 작업마다 별도 `AsyncSession`을 만들며 하나의 세션을 공유하지 않습니다.", "대기 쿼리 세 건은 순차 약 0.46초, 동시 약 0.20초였습니다."],
        "02": ["트랜잭션은 함께 성립해야 하는 SQL 변경을 한 확정 단위로 묶습니다.", "별도 커밋은 장애 뒤 총액 900을 남겼고 한 경계의 롤백은 총액 1000을 유지했습니다.", "외부 API 부작용에는 데이터베이스 롤백과 별도의 멱등성 설계가 필요합니다."],
        "03": ["Alembic 리비전은 스키마 변경의 앞뒤 순서를 코드로 기록합니다.", "upgrade, downgrade, 재적용을 `to_regclass`의 표 존재 여부로 확인했습니다.", "되돌리는 DDL이 있어도 삭제한 운영 데이터가 자동으로 복원되지는 않습니다."],
        "04": ["풀 크기와 추가 연결 수는 모든 프로세스의 합계로 계산합니다.", "유일한 연결이 대기 제한보다 오래 점유되자 `TimeoutError`가 발생했습니다.", "연결 범위를 짧게 하고 대기 시간·쿼리 시간·체크아웃 수를 함께 관찰합니다."],
        "05": ["HNSW 인덱스는 거리 연산자 클래스와 쿼리가 맞아야 하며 작은 표에서는 선택되지 않을 수 있습니다.", "문서 표와 실제 체크포인트 행을 같은 스키마에 저장했습니다.", "논리 덤프를 별도 데이터베이스에 복원해 문서 행, 체크포인트 행, HNSW 인덱스를 확인했습니다."],
    }[slug[:2]]
    summary_html = "".join(f"<li>{line}</li>" for line in summaries)
    verification_note = {
        "01": "배포 전에는 요청 수를 한 단계씩 늘리며 활성 세션 수와 풀 체크아웃 수를 기록합니다. 동기 드라이버가 섞이지 않았는지 실행 경로를 확인하고, 타임아웃 뒤 세션이 닫히는지도 시험합니다. 취소된 요청이 연결을 계속 점유한다면 동시 처리 수를 늘리기 전에 정리 경로를 고쳐야 합니다.",
        "02": "장애 시험은 각 SQL 문 사이에서 예외가 난 경우를 나누어 실행합니다. 롤백 뒤 업무 합계와 행별 상태를 모두 조회하고, 같은 요청을 다시 보냈을 때 중복 행이 생기지 않는지도 확인합니다. 운영 로그에는 비밀 값 대신 업무 식별자와 트랜잭션 결과를 남깁니다.",
        "03": "마이그레이션 검증에서는 빈 데이터베이스 적용, 현재 리비전에서 다음 리비전 적용, 한 단계 롤백을 구분합니다. 각 경로에서 Alembic 버전과 실제 열·제약·인덱스를 조회합니다. 시간 측정이 필요한 DDL은 운영과 비슷한 행 수의 복제 환경에서 실행합니다.",
        "04": "부하 시험은 평균 지연만 보지 않고 연결 대기 시간의 상위 백분위수와 시간 초과 수를 함께 기록합니다. 쿼리 종료 뒤 체크아웃 수가 원래 값으로 돌아오는지 확인합니다. 연결 누수가 의심되면 요청별 체크아웃과 체크인 이벤트를 짧은 기간 추적합니다.",
        "05": "복원 검증은 빈 대상에 확장을 준비하고 덤프를 적용하는 순간부터 시작합니다. 문서 수와 체크포인트 수를 원본과 대조하고, 인덱스 정의와 실제 검색·스레드 재개를 확인합니다. 이번 실습은 행 수와 인덱스 존재까지 실행했으며 그래프 스레드 재개는 추가 검증 항목으로 남깁니다.",
    }[slug[:2]]
    measurement_limit = {
        "01": "실제 서비스에서는 쿼리별 지연뿐 아니라 한 요청이 세션을 보유한 전체 시간도 측정합니다. 동시 실행 개수를 풀 크기보다 크게 바꿔 대기 구간이 생기는 지점을 찾고, 그 결과를 요청 제한 설정에 반영합니다.",
        "02": "동시 이체까지 검증하려면 두 작업이 같은 계좌를 갱신하도록 실행하고 잠금 대기와 최종 잔액을 확인합니다. 이번 절은 한 요청 내부의 중간 장애만 다루므로 동시 갱신의 격리 현상까지 일반화하지 않습니다.",
        "03": "롤백 시간을 측정할 때는 DDL 실행 시간과 데이터 되채우기 시간을 나눕니다. 배포 제한 시간을 넘는 변경은 한 리비전에 모두 넣지 않고 호환 가능한 여러 단계로 나누어 각 단계의 중단 가능 지점을 기록합니다.",
        "04": "After가 성공한 이유는 풀 용량이 늘어서가 아니라 첫 연결이 제한 시간 안에 반환됐기 때문입니다. 요청 수가 계속 늘면 다시 대기하므로 실제 처리량과 허용 지연을 기준으로 풀과 작업 큐를 함께 조정합니다.",
        "05": "실행 계획의 Seq Scan은 HNSW 생성 실패가 아닙니다. 세 행에서는 전체를 읽고 정렬하는 비용이 작아 최적화기가 순차 스캔을 선택했습니다. 행 수와 통계를 운영 규모에 맞춘 뒤 같은 EXPLAIN을 반복해야 인덱스 선택과 버퍼 사용을 판단할 수 있습니다.",
    }[slug[:2]]
    return dedent(f"""
    <!--meta: {item['hours']} | 코드 Jupyter Notebook | 새 용어 {len(item['terms'].split(', '))} -->
    <h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul><li>{item['title']}의 구성 요소를 실제 PostgreSQL 출력으로 설명할 수 있습니다.</li><li>운영 장애 조건을 재현하고 코드 또는 설정으로 대응할 수 있습니다.</li><li>관찰한 결과와 운영 전체에 적용할 수 없는 범위를 구분할 수 있습니다.</li></ul></div>
    <h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>{item['why']}</p>
    <h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>{item['prior']}</p>
    <h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>구체적인 상황</h3><p>{item['concept'].split('. ')[0]}.</p><h3>정의</h3><p>{'. '.join(item['concept'].split('. ')[1:])}</p><p><strong>이 절의 새 용어</strong> — {item['terms']}</p><h3>운영에서 경계를 정하는 방법</h3><p>{operation_note}</p><h3>도식 읽기</h3>{diagram}<p>{diagram_reading}</p>
    <h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 전용 스키마를 먼저 만들고 같은 셀에서 필요한 입력을 준비합니다. 첫 셀부터 순서대로 실행한 뒤 출력과 `assert`를 함께 확인합니다.</p>{nb1}<p class="look"><b>확인할 점</b> — 출력의 표 이름, 행 값, 오류 이름, 실행 시간을 본문에 적힌 관찰과 대조합니다.</p>
    <h2 id="b6"><span class="no">6</span>{title6}</h2><p>{item['observed']}</p>{nb2}<p>이 결과는 Docker의 독립 PostgreSQL 17.8 컨테이너와 작은 데이터에서 측정했습니다. 행 수, 네트워크, 디스크, 동시 요청 수가 달라지면 시간과 실행 계획도 달라집니다.</p><p>{measurement_limit}</p>
    <h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul>{notes}</ul><h3>운영 전 확인 순서</h3><p>{verification_note}</p>
    <h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul>{summary_html}</ul><p><strong>다음 학습과 이어지는 지점</strong> — {item['next']}</p>
    <h2 id="b9"><span class="no">9</span>복습 문제</h2>{quiz}
    <h2 id="b10"><span class="no">10</span>참고 자료</h2><ul>{refs}</ul><p><strong>확인 필요 항목</strong> — 운영 배포 전에는 조직의 허용 연결 수, 백업 보존 기간, 복구 목표 시간과 실제 데이터 규모를 별도로 확인해야 합니다.</p>
    """).strip()+"\n"


def write_files() -> None:
    for slug, nb in NBS.items():
        (LAB / "notebooks" / f"{slug}.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1)+"\n", encoding="utf-8")
    config = json.loads((TB / "chapter.json").read_text(encoding="utf-8"))
    config.update({"part_title":"Part 7 · Agent 서비스 개발", "hours":"총 16h · 강의 5h · 실습 11h",
                   "objectives":["비동기 SQLAlchemy와 트랜잭션으로 PostgreSQL 작업 경계를 설계합니다.","Alembic 적용·롤백과 커넥션 풀 고갈을 실제 환경에서 재현하고 대응합니다.","pgvector와 체크포인터 표의 공존 및 논리 백업 범위를 확인합니다."]})
    (TB / "chapter.json").write_text(json.dumps(config, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    formats = {x["slug"]:x["format"] for x in config["sections"]}
    for slug, item in INFO.items():
        (TB / "_src" / f"{slug}.html").write_text(source(slug,item,formats[slug]), encoding="utf-8")


if __name__ == "__main__":
    write_files()
