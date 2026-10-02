"""Ch 31 05절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§5-3·§6 experiment).

사용:
  python3 -B author_05.py            → 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_05.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
이후 run_section.sh 가 pre_exec.sh(PostgreSQL 켜기 + pgenv bin을 PATH 끝에) → 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**. 슬러그 `05-pgvector-체크포인터-공존과-백업` 그대로.

## 결정 1 — 공존: 검색 문서 표와 체크포인터 표를 같은 이름 공간 ch31_shared에 (Ch 23 02 모양)

psycopg 동기 연결 둘(조회용 conn · 체크포인터용 saver_conn = autocommit·dict_row·SET search_path TO ch31_shared) — Ch 12 02·Ch 23 02 이음.
setup()이 체크포인터 표 넷을 ch31_shared에 만든다 → 첫 셀의 DROP SCHEMA … CASCADE가 체크포인터 표도 함께 지워 다시 실행해도 줄 수 같음
(handoff §04 → §05 6 「public에 생기므로」는 search_path를 정하지 않을 때의 이야기 — 옛 판도 search_path로 ch31_shared에 둠).
문서 벡터는 손으로 정한 3차원 값(배송·환불·결제 쪽) — 임베딩 모델이 만든 값이 아님을 셀 주석·설명에 밝힘. 모델 요청 0.

## 결정 2 — experiment: 가설 → 실행 1(확장 없이 복원) → 실행 2(바꾼 값 하나: 복원 전에 CREATE EXTENSION vector) → 결과 표 → 결론

이름 공간 하나만 덤프(--schema)하면 public의 확장 vector는 파일에 들지 않음(pg_dump 문서 · pg_restore --list 확장 항목 False).
실행 1 = 종료 코드 1 · 오류 첫 줄 type "public.vector" does not exist · errors ignored on restore: 5 · 표 넷(문서 표 없음) · 저장된 값 {'value': 12}.
실행 2 = 종료 코드 0 · 표 다섯(문서 3줄) · {'value': 12} · 복원 DB에서 enable_seqscan off 계획 Index Scan using documents_embedding_hnsw.
실험 변수로 enable_seqscan(준비 노트 후보)을 쓰지 않은 까닭: Ch 12 02 실행 3이 이미 그 실험 — 이 절은 3절에서 계획 줄만 보이고,
복원 뒤 색인이 쓰이는지 확인하는 자리에 그 설정을 씀. 노트북 밖 /tmp/ch31-05/exp/e3_scene.py 5/5 같음(목차 원문 줄의 OID만 달라 출력하지 않음 · e1_scene.py는 --no-owner 판이라 오류 넷).
노트북은 --no-owner를 주지 않아 표 주인 정하기(ALTER … OWNER TO)까지 오류 다섯 — 모두 documents에 걸림.

## 결정 3 — 백업 명령 자리(챕터 리드 결정): shutil.which("pg_dump") → 있으면 이 컴퓨터(--host·--port·--username + PGPASSWORD 환경 변수),
## 없으면 docker exec -i kdt-ch31-postgres(컨테이너 안 --username만 — 공식 이미지는 컨테이너 안 접속을 trust). 조건 표현식 없이 if 문.
## 작업 기기는 pre_exec.sh가 pgenv bin을 PATH 끝에 더함(pg_dump·pg_restore 17.11). Docker 쪽은 교재 출력에서 실행하지 않음.
## 덤프 파일은 tempfile.mkdtemp 임시 폴더(지우지 않고 둠), 출력에 위치·바이트 수 없음.
## 쓰지 않은 것: f-string·내포식·lambda·조건 표현식·next·기본값 매개변수·힌트·클래스(상태 형식 TypedDict 하나 말고)·데코레이터·세미콜론·가짜 모델
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
SLUG = "05-pgvector-체크포인터-공존과-백업"
TITLE_TEXT = "pgvector 체크포인터 공존과 백업"
SRC = ROOT / "textbook/part7/ch31-database/_src" / (SLUG + ".html")
AUTHOR01 = ROOT / "textbook/part7/ch31-database/qa/upgrade/author_01.py"
RUNS_SENTENCE = os.environ.get("AUTHOR05_RUNS_SENTENCE", "새 커널로 두 번 실행해 견주자, 코드 셀 서른하나의 출력이 셀마다 모두 같았습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 모델을 부르지 않아, 이 절의 출력은 손으로 정한 벡터와 서버에 만든 표로 정해집니다.")

# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["psycopg[binary]==3.3.3", "langgraph==1.2.11", "langgraph-checkpoint-postgres==3.0.5"])

IMPORTS = r'''# 명령 찾기·명령 실행·임시 폴더·환경 변수에 쓸 모듈과, psycopg·LangGraph 이름을 가져옵니다
import os
import shutil
import subprocess
import tempfile
import psycopg
from psycopg.rows import dict_row
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
# 체크포인트를 PostgreSQL 표에 쓰는 체크포인터입니다(Ch 23 02절)
from langgraph.checkpoint.postgres import PostgresSaver

print("가져온 이름:", "psycopg", "dict_row", "TypedDict", "StateGraph", "PostgresSaver")'''

SETTINGS = r'''# 데이터베이스 접속 글을 정합니다(비밀번호 postgres는 이 실습에서만 쓰는 연습용 값입니다)
database_url = "postgresql://postgres:postgres@127.0.0.1:55431/ch31_lab"
# 비밀번호가 찍히지 않게, 글을 @에서 나눠 앞의 드라이버 부분과 뒤의 서버 부분만 출력합니다
url_parts = database_url.split("@")
print("드라이버 부분:", database_url.split("://")[0])
print("서버 주소와 데이터베이스:", url_parts[1])'''

CONNECT = r'''# 조회에 쓸 연결을 열고, pgvector 확장을 켠 뒤 서버와 확장의 버전을 봅니다
conn = psycopg.connect(database_url, autocommit=True)
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
cur.execute("SELECT current_setting('server_version')")
print("PostgreSQL 버전:", cur.fetchone()[0])
cur.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
print("pgvector 확장 버전:", cur.fetchone()[0])'''

DEF_TABLES = r'''# 커서 하나로 이름 공간 ch31_shared 안의 표 이름을 이름 차례로 읽어, 목록으로 내놓습니다
def shared_tables(cursor):
    sql = "SELECT table_name FROM information_schema.tables"
    sql = sql + " WHERE table_schema = 'ch31_shared' ORDER BY table_name"
    cursor.execute(sql)
    names = []
    for row in cursor.fetchall():
        names.append(row[0])
    return names'''

RESET = r'''# 복원 데이터베이스의 접속 글을 정하고, 앞 실행이 남긴 것을 지운 뒤 빈 이름 공간 ch31_shared를 만듭니다
restore_url = database_url.replace("/ch31_lab", "/ch31_restore")
cur.execute("DROP DATABASE IF EXISTS ch31_restore")
cur.execute("DROP SCHEMA IF EXISTS ch31_shared CASCADE")
cur.execute("CREATE SCHEMA ch31_shared")
print("ch31_shared 안의 표:", shared_tables(cur))'''

DOCS = r'''# 이름 공간 ch31_shared에 벡터 칸이 있는 검색 문서 표를 만들고, 문서 세 줄을 넣습니다
cur.execute("CREATE TABLE ch31_shared.documents (id int PRIMARY KEY, content text, embedding vector(3))")
# 벡터의 세 숫자는 차례로 배송·환불·결제 쪽을 뜻하게 손으로 정했습니다(임베딩 모델이 만든 값이 아닙니다)
rows_sql = "(1, '배송', '[1,0,0]'), (2, '환불', '[0,1,0]'), (3, '결제', '[0,0,1]')"
cur.execute("INSERT INTO ch31_shared.documents VALUES " + rows_sql)
print("넣은 줄 수:", cur.rowcount)'''

INDEX = r'''# 벡터 칸에 코사인 거리용 HNSW 색인을 만듭니다(Ch 12 02절과 같은 연산자 종류 vector_cosine_ops)
index_sql = "CREATE INDEX documents_embedding_hnsw ON ch31_shared.documents"
index_sql = index_sql + " USING hnsw (embedding vector_cosine_ops)"
cur.execute(index_sql)
print("색인 만들기 SQL:")
print(index_sql)'''

SEARCH = r'''# 질문 벡터 하나로 코사인 거리가 가까운 문서 둘을 받아 옵니다(질문 벡터도 손으로 정한 값입니다)
search_sql = "SELECT content, embedding <=> %s FROM ch31_shared.documents ORDER BY embedding <=> %s LIMIT 2"
question_vector = "[0.9,0.1,0]"
cur.execute(search_sql, (question_vector, question_vector))
hits = []
for row in cur.fetchall():
    hits.append((row[0], round(row[1], 4)))
print("가까운 문서와 코사인 거리:", hits)'''

PLAN = r'''# 같은 SQL 글 앞에 EXPLAIN (COSTS OFF)를 붙여, 서버가 고른 계획 줄만 봅니다(검색은 하지 않습니다)
cur.execute("EXPLAIN (COSTS OFF) " + search_sql, (question_vector, question_vector))
print("계획 줄:")
for row in cur.fetchall():
    print(row[0])'''

SAVER = r'''# 체크포인터가 쓸 연결을 따로 열고, 표를 찾고 만들 이름 공간을 ch31_shared로 정합니다(Ch 23 02절 모양)
saver_conn = psycopg.connect(database_url, autocommit=True, row_factory=dict_row)
saver_cur = saver_conn.cursor()
saver_cur.execute("SET search_path TO ch31_shared")
checkpointer = PostgresSaver(saver_conn)
# 표 만들기 setup()은 체크포인터가 쓸 표 넷을 이 이름 공간에 만듭니다
checkpointer.setup()
print("ch31_shared 안의 표:", shared_tables(cur))'''

STATE = r'''# 값 칸 하나만 둔 상태 형식을 만듭니다
class ValueState(TypedDict):
    value: int'''

NODE = r'''# 노드 함수: 받은 상태의 값을 두 배로 한 값을 냅니다(모델을 부르지 않습니다)
def double_value(state):
    doubled = state["value"] * 2
    return {"value": doubled}'''

GRAPH = r'''# 노드 하나·엣지 둘을 설계 객체에 적고, PostgreSQL 체크포인터와 함께 컴파일합니다
builder = StateGraph(ValueState)
builder.add_node("double", double_value)
builder.add_edge(START, "double")
builder.add_edge("double", END)
graph = builder.compile(checkpointer=checkpointer)
print("붙은 체크포인터의 종류:", type(graph.checkpointer).__name__)'''

INVOKE = r'''# 스레드 이름 backup-demo로 값 6을 넣어 한 번 실행하고, 체크포인터가 저장한 상태를 읽습니다
thread_config = {"configurable": {"thread_id": "backup-demo"}}
result = graph.invoke({"value": 6}, thread_config)
print("실행 결과:", result)
print("get_state로 읽은 값:", graph.get_state(thread_config).values)'''

COUNTS = r'''# 체크포인터 표 넷의 줄 수를 셉니다(표 이름은 값이 아니라 SQL 글의 일부라 이어 붙입니다)
checkpoint_tables = ["checkpoints", "checkpoint_blobs", "checkpoint_writes", "checkpoint_migrations"]
print("표 | 줄 수")
for table_name in checkpoint_tables:
    cur.execute("SELECT count(*) FROM ch31_shared." + table_name)
    print(table_name, "|", cur.fetchone()[0])'''

FIND_TOOL = r'''# 명령 pg_dump를 이 컴퓨터에서 찾고, 없으면 Docker 컨테이너 안의 명령을 부르게 명령 앞부분을 정합니다
pg_dump_found = shutil.which("pg_dump")
if pg_dump_found is None:
    command_start = ["docker", "exec", "-i", "kdt-ch31-postgres"]
    server_args = ["--username=postgres"]
    print("명령을 부를 자리: Docker 컨테이너 kdt-ch31-postgres 안")
else:
    command_start = []
    server_args = ["--host=127.0.0.1", "--port=55431", "--username=postgres"]
    print("명령을 부를 자리: 이 컴퓨터")'''

DEF_RUN = r'''# 명령 이름과 인자 목록, 명령에 보낼 입력을 받아 명령을 실행하고, 끝난 결과 객체를 내놓습니다
def run_tool(tool_args, input_bytes):
    # 앞부분(이 컴퓨터면 빈 목록)·명령과 인자·서버 인자를 이어 명령 목록 하나를 만듭니다
    command = command_start + tool_args + server_args
    result = subprocess.run(command, input=input_bytes, capture_output=True, env=tool_env)
    return result'''

ENV_VERSION = r'''# 명령에 넘길 환경 변수를 노트북 환경에서 복사하고, 연습용 비밀번호를 PGPASSWORD에 넣습니다(값은 출력하지 않습니다)
tool_env = dict(os.environ)
tool_env["PGPASSWORD"] = "postgres"
# pg_dump의 버전을 봅니다(보낼 입력이 없어 None을 넘깁니다)
version_result = run_tool(["pg_dump", "--version"], None)
version_text = version_result.stdout.decode("utf-8")
print("pg_dump 버전:", version_text.strip())'''

BACKUP = r'''# 운영체제 임시 폴더에 새 폴더를 만들고, 이름 공간 ch31_shared 하나만 덤프 파일로 받아 씁니다
backup_folder = tempfile.mkdtemp(prefix="ch31-05-")
dump_file = backup_folder + "/ch31_shared.dump"
dump_result = run_tool(["pg_dump", "--format=custom", "--schema=ch31_shared", "--dbname=ch31_lab"], None)
# 명령이 표준 출력으로 낸 바이트를 그대로 파일에 씁니다("wb"는 바이트 쓰기)
with open(dump_file, "wb") as dump_out:
    dump_out.write(dump_result.stdout)
print("pg_dump 종료 코드:", dump_result.returncode)
print("덤프 파일이 생겼는가:", os.path.exists(dump_file))'''

LIST = r'''# 덤프 파일을 바이트로 읽고, pg_restore --list로 받은 목차에서 표 항목과 확장 항목을 찾습니다
with open(dump_file, "rb") as dump_in:
    dump_bytes = dump_in.read()
list_result = run_tool(["pg_restore", "--list"], dump_bytes)
list_text = list_result.stdout.decode("utf-8")
print("목차에 문서 표 항목이 있는가:", " TABLE ch31_shared documents " in list_text)
print("목차에 체크포인트 표 항목이 있는가:", " TABLE ch31_shared checkpoints " in list_text)
print("목차에 확장 항목이 있는가:", " EXTENSION " in list_text)'''

DEF_RESTORE = r'''# 복원 데이터베이스를 새로 만들고, 정한 대로 확장을 만든 뒤 덤프 파일을 복원해 끝난 결과 객체를 내놓습니다
def restore_copy(make_extension):
    cur.execute("DROP DATABASE IF EXISTS ch31_restore")
    cur.execute("CREATE DATABASE ch31_restore")
    if make_extension:
        extension_conn = psycopg.connect(restore_url, autocommit=True)
        extension_conn.cursor().execute("CREATE EXTENSION vector")
        extension_conn.close()
    return run_tool(["pg_restore", "--dbname=ch31_restore"], dump_bytes)'''

DEF_READ = r'''# 복원 데이터베이스의 이름 공간 ch31_shared에서 표마다 줄 수를 세어, 표 이름을 키로 한 딕셔너리로 내놓습니다
def read_restored():
    check_conn = psycopg.connect(restore_url, autocommit=True)
    check_cur = check_conn.cursor()
    row_counts = {}
    for table_name in shared_tables(check_cur):
        check_cur.execute("SELECT count(*) FROM ch31_shared." + table_name)
        row_counts[table_name] = check_cur.fetchone()[0]
    check_conn.close()
    return row_counts'''

DEF_STATE = r'''# 복원 데이터베이스의 체크포인터 표로 같은 설계 객체를 다시 컴파일해, 스레드 backup-demo의 저장된 값을 내놓습니다
def restored_state():
    state_conn = psycopg.connect(restore_url, autocommit=True, row_factory=dict_row)
    state_conn.cursor().execute("SET search_path TO ch31_shared")
    restored_graph = builder.compile(checkpointer=PostgresSaver(state_conn))
    saved_values = restored_graph.get_state(thread_config).values
    state_conn.close()
    return saved_values'''

RUN1 = r'''# 실행 1: 확장을 만들지 않은 새 데이터베이스에 덤프 파일을 복원하고, 종료 코드와 오류 출력을 봅니다
make_extension = False
first_restore = restore_copy(make_extension)
first_errors = first_restore.stderr.decode("utf-8").splitlines()
print("pg_restore 종료 코드:", first_restore.returncode)
print("오류 출력 첫 줄:", first_errors[0])
print("오류 출력 끝 줄:", first_errors[-1])'''

READ1 = r'''# 실행 1의 복원 데이터베이스에서 표마다 줄 수와, 스레드 backup-demo의 저장된 값을 읽습니다
first_counts = read_restored()
first_values = restored_state()
print("표마다 줄 수:", first_counts)
print("저장된 값:", first_values)'''

RUN2 = r'''# 실행 2: 바꾼 값은 확장 만들기 하나입니다(같은 덤프 파일을 확장을 만든 새 데이터베이스에 복원)
make_extension = True
second_restore = restore_copy(make_extension)
second_errors = second_restore.stderr.decode("utf-8").splitlines()
print("pg_restore 종료 코드:", second_restore.returncode)
print("오류 출력 줄 수:", len(second_errors))'''

READ2 = r'''# 실행 2의 복원 데이터베이스에서 표마다 줄 수와, 스레드 backup-demo의 저장된 값을 읽습니다
second_counts = read_restored()
second_values = restored_state()
print("표마다 줄 수:", second_counts)
print("저장된 값:", second_values)'''

TABLE = r'''# 두 실행을 한 줄씩 견줍니다(확장 만들기·종료 코드·복원된 표 수·문서 표가 있는가·저장된 값)
print("실행 | 확장 만들기 | 종료 코드 | 복원된 표 수 | 문서 표가 있는가 | 저장된 값")
print("실행 1 |", False, "|", first_restore.returncode, "|", len(first_counts), "|", "documents" in first_counts, "|", first_values)
print("실행 2 |", True, "|", second_restore.returncode, "|", len(second_counts), "|", "documents" in second_counts, "|", second_values)'''

RESTORED_PLAN = r'''# 실행 2의 복원 데이터베이스에서 enable_seqscan을 off로 두고, 같은 검색의 계획 줄을 봅니다
plan_conn = psycopg.connect(restore_url, autocommit=True)
plan_cur = plan_conn.cursor()
plan_cur.execute("SET enable_seqscan = off")
plan_cur.execute("EXPLAIN (COSTS OFF) " + search_sql, (question_vector, question_vector))
print("복원 데이터베이스의 계획 줄:")
for row in plan_cur.fetchall():
    print(row[0])
plan_conn.close()'''

CLEANUP = r'''# 끝 정리: 체크포인터 연결을 닫고, 복원 데이터베이스와 이름 공간 ch31_shared를 지운 뒤 남았는지 봅니다
saver_conn.close()
cur.execute("DROP DATABASE ch31_restore")
cur.execute("DROP SCHEMA ch31_shared CASCADE")
cur.execute("SELECT to_regnamespace('ch31_shared')")
print("남은 이름 공간:", cur.fetchone()[0])
cur.execute("SELECT count(*) FROM pg_database WHERE datname = 'ch31_restore'")
print("남은 복원 데이터베이스 수:", cur.fetchone()[0])
conn.close()'''

# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/05-figures.md)
FIG1 = "05-1-한-이름-공간에-두-가지-표"
FIG1_ALT = "위에서 아래로 읽는 그림입니다. 초록 상자 접속 글 127.0.0.1:55431/ch31_lab에서 이름 공간 ch31_shared 칸으로 화살표가 갑니다. 칸 안에는 초록 상자 문서 표 documents 문서 셋 벡터 칸과, 그 아래 파란 상자 HNSW 색인 documents_embedding_hnsw가 있습니다. 같은 칸 안에 회색 상자 체크포인터 표 넷 setup()이 만듦도 있습니다. 칸 밖 회색 상자 확장 vector 0.8.1 기본 이름 공간 public에서 문서 표로, 자료형을 빌려 씀이라는 점선이 갑니다. 칸에서 노란 상자 표 다섯 checkpoints 줄 셋 저장된 값 value 12로 이어지는 그림"
FIG1_CAP = "검색 문서 표·HNSW 색인·체크포인터 표 넷이 한 이름 공간에 함께 있고, 문서 표만 public에 있는 확장의 자료형을 빌려 씁니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 셀에 적은 접속 글과 우리가 넣은 문서 표이고, 파란 상자는 우리가 만든 색인입니다.
회색 상자 둘은 PostgreSQL 확장과, 표 만들기 setup()이 만든 체크포인터 표입니다.
노란 상자는 노트북 4절 출력으로 확인한 값입니다.
점선은 문서 표만 확장의 자료형에 기댄다는 뜻입니다."""

FIG2 = "05-2-백업-명령-자리와-덤프-파일"
FIG2_ALT = "위에서 아래로 읽는 그림입니다. 파란 상자 shutil.which로 pg_dump 찾기에서 점선 둘이 갈라집니다. 한 갈래는 노란 상자 찾음 이 컴퓨터의 명령 pg_dump 17.11이고, 다른 갈래는 회색 상자 못 찾음 docker exec -i kdt-ch31-postgres 안의 명령 교재 출력에서는 실행하지 않음입니다. 두 갈래가 파란 상자 pg_dump --format=custom --schema=ch31_shared로 모이고, 이어서 초록 상자 임시 폴더의 덤프 파일 하나, 마지막 노란 상자 종료 코드 0 목차에 문서 표 True 체크포인트 표 True 확장 False로 이어지는 그림"
FIG2_CAP = "명령 pg_dump는 이 컴퓨터에서 찾았고, 이름 공간을 골라 받은 덤프 파일에는 두 가지 표가 있고, 확장은 들지 않았습니다."
FIG2_READ = """위에서 아래로 읽습니다.
점선 두 갈래는 노트북 5절의 if 문이 고르는 두 자리입니다.
교재 출력은 노란 갈래로 만들었고, 회색 갈래는 실행하지 않았습니다.
파란 상자는 우리가 부른 함수와 명령이고, 초록 상자는 명령이 쓴 파일입니다.
맨 아래 노란 상자는 5절 출력으로 확인한 종료 코드와 목차입니다."""

FIG3 = "05-3-확장-없이-복원한-실행-1"
FIG3_ALT = "위에서 아래로 여섯 상자가 한 줄로 이어진 흐름도입니다. 파란 상자 restore_copy make_extension=False에서 회색 상자 새 데이터베이스 ch31_restore 확장 없음으로, 다시 파란 상자 pg_restore --dbname=ch31_restore 입력은 덤프 파일로 갑니다. 이어서 노란 상자 종료 코드 1 type public.vector does not exist errors ignored on restore: 5, 노란 상자 표 넷 문서 표 없음 checkpoints 줄 셋, 노란 상자 저장된 값 value 12로 이어지는 그림"
FIG3_CAP = "확장이 없는 새 데이터베이스에 복원하자 문서 표만 만들어지지 않았고, 체크포인터 표와 저장된 값은 돌아왔습니다."
FIG3_READ = """위에서 아래로 읽습니다.
파란 상자 둘은 노트북 6절 함수와 그 안에서 부른 명령이고, 회색 상자는 서버에 새로 만든 데이터베이스입니다.
노란 상자 셋은 7절 출력으로 확인한 종료 코드·오류 줄·표·저장된 값입니다.
받아 출력한 오류라 노랑이고, 이 절에 빨간 상자는 없습니다."""

FIG4 = "05-4-확장-만들기-하나를-바꾼-두-실행"
FIG4_ALT = "위에 회색 상자 하나가 있고 아래에 칸 둘이 나란히 놓인 그림입니다. 회색 상자 두 실행 같음 같은 덤프 파일 함수 restore_copy 새 데이터베이스 ch31_restore에서 두 칸으로 화살표가 갑니다. 한 칸 실행 1 확장 만들기 False에는 파란 상자 확장 없이 pg_restore 아래 노란 상자 종료 코드 1 표 넷 문서 표 없음이 있습니다. 다른 칸 실행 2 확장 만들기 True에는 파란 상자 CREATE EXTENSION vector 뒤 pg_restore 아래 노란 상자 종료 코드 0 표 다섯 documents 줄 셋, 그 아래 노란 상자 enable_seqscan off 계획 Index Scan using documents_embedding_hnsw가 있습니다. 두 칸에서 맨 아래 노란 상자 두 실행 모두 checkpoints 줄 셋 저장된 값 value 12로 화살표가 모이는 그림"
FIG4_CAP = "확장 만들기 하나만 바꾸자 종료 코드와 문서 표가 갈렸고, 체크포인터 표와 저장된 값은 두 실행이 같았습니다."
FIG4_READ = """맨 위 회색 상자는 두 실행에서 같았던 조건입니다.
두 칸이 실행 1과 실행 2이고, 파란 상자가 바꾼 값 하나로 달라진 복원 방법입니다.
노란 상자는 노트북 7·8·9절 출력입니다.
색인 계획 줄은 문서 표가 있는 실행 2 칸에서만 봤습니다.
맨 아래 상자는 두 칸의 출력에서 모두 확인한 값입니다."""

ILLU = "05-5-자리를-단-판과-달지-않은-판"
ILLU_ALT = "흰 바탕에 옅은 회색 금속 판 둘이 나란히 서서 화면을 채웁니다. 판마다 가운데에 가로로 긴 띠가 있고, 아래 끝에 좁은 턱이 있습니다. 왼쪽 판의 띠에는 구리색 둥근 꽂는 자리 넷이 한 줄로 있고, 오른쪽 끝은 구멍 없는 밋밋한 자리입니다. 네 자리에 짙은 회색 선이 하나씩 꽂혀 턱 아래로 늘어지고, 노란 초록 선 하나는 꽂히지 않은 채 턱 위에 누워 있습니다. 오른쪽 판의 띠에는 구리색 꽂는 자리 다섯이 한 줄로 있고, 앞의 넷에 짙은 회색 선이, 오른쪽 끝 자리에 노란 초록 선이 꽂혀 모두 아래로 늘어집니다. 사람·손·글자·숫자·화살표·불은 없는 그림"
ILLU_CAP = "자리를 달지 않은 왼쪽 판에는 회색 선 넷만 꽂혔고, 자리를 단 오른쪽 판에는 노란 초록 선까지 선 다섯이 꽂혔습니다."
ILLU_READ = "옅은 회색 판 둘이 나란히 있습니다. 왼쪽 판에는 꽂는 자리가 넷뿐이고, 다섯째 자리는 구멍 없이 막혀 있습니다. 그래서 회색 선 넷만 꽂혀 있고, 노란 초록 선은 턱 위에 놓여 있습니다. 오른쪽 판에는 자리가 다섯이라, 회색 선 넷과 노란 초록 선 하나가 모두 꽂혀 있습니다. 왼쪽이 확장 없이 복원한 실행 1, 오른쪽이 확장을 먼저 만든 실행 2이고, 노란 초록 선이 검색 문서 표입니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 한 이름 공간에 pgvector 검색 문서 표·HNSW 색인과 체크포인터 표를 함께 만듭니다.
2. 명령 `pg_dump`로 그 이름 공간 하나를 덤프 파일로 받고, 파일에 든 항목을 봅니다.
3. 확장이 없는 새 데이터베이스와 확장을 만든 새 데이터베이스에 복원해, 돌아온 것을 견줍니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
예상 비용도 0달러입니다.

01절과 같은 PostgreSQL 서버가 `127.0.0.1:55431`에서 켜져 있어야 합니다.
서버는 01절 준비물의 Docker 컨테이너 `kdt-ch31-postgres`입니다.
꺼져 있으면 터미널에서 `docker start kdt-ch31-postgres`로 다시 켭니다.
컨테이너를 아직 만들지 않았다면, 01절 노트북 맨 위 준비물의 `docker run` 명령을 먼저 실행합니다.

노트북은 데이터베이스 `ch31_lab` 안에 이름 공간 `ch31_shared`를 만들어 쓰고, 끝에서 지웁니다.
복원을 받을 데이터베이스 `ch31_restore`도 새로 만들었다가 끝에서 지웁니다.
작업 폴더에는 파일을 쓰지 않고, 덤프 파일 하나만 운영체제 임시 폴더에 씁니다.
걸린 시간은 재지 않습니다.

**백업 명령** — 이 노트북은 PostgreSQL의 명령 `pg_dump`와 `pg_restore`를 부릅니다.
이 컴퓨터에 명령 `pg_dump`가 있으면 그것을 쓰고, 없으면 Docker 컨테이너 안의 명령을 부릅니다.
이 컴퓨터의 명령을 쓸 때는 앞자리(주 버전)가 서버와 같은 17인 명령이 안전합니다.
16 이하는 백업을 받지 못하고, 18 이상이 만든 파일은 17 서버에 들어간다고 장담하지 않습니다.

**기준 버전** — 첫 셀에서 패키지 셋을 설치합니다.
버전은 psycopg 3.3.3과 langgraph 1.2.11입니다.
체크포인터 패키지 langgraph-checkpoint-postgres는 3.0.5이고, 셋 모두 실습 폴더 잠금과 같습니다.
교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다.
확장 pgvector는 0.8.1입니다.

그 서버는 Docker 컨테이너가 아니라, 같은 접속 글로 켠 서버입니다.
Docker 이미지로 켜면 서버 버전 번호의 끝자리가 다를 수 있습니다.
명령 `pg_dump`와 `pg_restore`도 서버와 같은 17.11 버전을 이 컴퓨터에서 불렀습니다.
Docker 컨테이너 안의 명령을 부르는 쪽과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~5절을 읽습니다.
같은 이름 공간에 두 가지 표를 두고, 이름 공간 하나를 덤프 파일로 받는 자리입니다.
6~9절은 가설을 세우고 두 복원을 견주는 실험이고, 실습 시간에 실행합니다.
10절은 만든 데이터베이스와 이름 공간을 지우는 정리입니다.

실습 폴더 `labs/part7/ch31-database`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이 절은 01~04절과 같은 PostgreSQL 서버에 두 가지 표를 함께 둡니다.
하나는 벡터 칸이 있는 검색 문서 표이고, 하나는 그래프의 상태를 저장하는 체크포인터 표입니다.
그리고 두 표를 파일 하나로 백업하고, 새 데이터베이스에 복원해 봅니다.

절 제목의 pgvector는 PostgreSQL에 벡터 칸과 벡터 거리 계산을 더하는 확장입니다.
제목의 체크포인터는 Ch 23 01절에서 배운 말로, 그래프가 단계를 마칠 때마다 상태를 저장하는 부품입니다.
제목의 공존은 두 가지 표를 같은 이름 공간에 함께 두는 것을 말합니다.

01·02·04절은 드라이버 asyncpg로 await를 쓰는 비동기 엔진을 썼습니다.
이 절은 03절처럼 await 없이 쓰는 동기 드라이버 psycopg를 씁니다.
체크포인터 `PostgresSaver`가 psycopg의 동기 연결로 표를 읽고 쓰기 때문입니다.

첫 셀은 이 절이 쓰는 패키지 셋을 설치하고, 설치된 버전 번호를 출력합니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `psycopg: 3.3.3`, `langgraph: 1.2.11`, `langgraph-checkpoint-postgres: 3.0.5`가 보입니다.
세 버전 모두 실습 폴더 잠금과 같고, Ch 23 02절에서 쓴 버전과도 같습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모듈 `os`·`shutil`·`subprocess`·`tempfile`은 Python에 들어 있는 기능 묶음입니다.
모듈 `shutil`과 `tempfile`은 03절에서, `subprocess`는 Ch 2 08절에서 썼습니다.
상태 형식 `TypedDict`와 그래프 이름, 체크포인터 `PostgresSaver`는 Ch 23 02절에서 가져온 이름입니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `가져온 이름: psycopg dict_row TypedDict StateGraph PostgresSaver`가 보입니다.
이 노트북에는 API 키를 확인하는 셀이 없습니다.
모델을 부르지 않기 때문입니다.

## 2. 같은 서버에 붙기

다음 셀은 01절 2절의 설정 셀과 드라이버 부분만 다른 셀로, 연습용 접속 글을 정합니다.
01절 글의 `postgresql+asyncpg` 자리가 이 셀에서는 `postgresql`입니다.
이 글은 SQLAlchemy를 거치지 않고 psycopg에 바로 주는 글이라, 드라이버 표시가 붙지 않습니다.
서버 주소·포트·계정·데이터베이스는 01절과 같습니다."""),
        code(SETTINGS),
        md("""**결과 읽기** — 출력 줄 `드라이버 부분: postgresql`이 보입니다.
라벨 `서버 주소와 데이터베이스:` 뒤의 `127.0.0.1:55431/ch31_lab`은 01절과 같은 서버와 데이터베이스입니다.
비밀번호가 든 가운데 부분은 출력하지 않았습니다.

다음 셀은 Ch 12 02절처럼 psycopg로 연결을 열고, 커서로 SQL 글을 보냅니다.
인자 `autocommit=True`는 SQL 글을 보낼 때마다 바로 확정하는 설정입니다.
문장 `CREATE EXTENSION IF NOT EXISTS vector`는 이 데이터베이스에 pgvector 확장이 없을 때만 켭니다.
확장은 PostgreSQL에 새 자료형과 함수를 더하는 꾸러미입니다."""),
        code(CONNECT),
        md("""**결과 읽기** — 출력 줄 `PostgreSQL 버전: 17.11`과 `pgvector 확장 버전: 0.8.1`이 보입니다.
서버 버전은 Docker 이미지로 켜면 끝자리가 다를 수 있습니다.

확장 0.8.1은 01절 Docker 이미지 태그 `pgvector/pgvector:0.8.1-pg17`의 버전과 같습니다.
확장은 데이터베이스 `ch31_lab`의 기본 이름 공간 `public`에 생깁니다.
이 사실은 7절의 오류 글에서 다시 봅니다.

## 3. 검색 문서 표와 HNSW 색인

이 절의 표는 모두 이름 공간 `ch31_shared`에 둡니다.
다음 셀은 이 이름 공간 안의 표 이름을 읽는 함수입니다.
Ch 23 02절의 함수 `table_names`와 같은 일을 하고, 읽는 이름 공간만 다릅니다.
인자로 커서를 받아, 뒤에서 다른 데이터베이스의 커서에도 씁니다."""),
        code(DEF_TABLES),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
자리 `information_schema.tables`는 데이터베이스의 표 목록을 담은 자리로, Ch 23 02절에서도 썼습니다.

다음 셀은 복원에 쓸 데이터베이스의 접속 글을 정하고, 앞 실행이 남긴 것을 지웁니다.
메서드 `replace`로 접속 글 끝의 데이터베이스 이름만 `ch31_restore`로 바꿉니다.
문장 `DROP DATABASE IF EXISTS`는 그 데이터베이스가 있으면 통째로 지웁니다.
이름 공간은 01절처럼 안의 표까지 지우고 빈 채로 새로 만듭니다."""),
        code(RESET),
        md("""**결과 읽기** — 출력 줄 `ch31_shared 안의 표: []`가 보입니다.
빈 이름 공간에서 시작합니다.
이 셀이 체크포인터 표까지 함께 지우게 되는 까닭은 4절에서 봅니다.

다음 셀은 검색 문서 표 `documents`를 만들고 문서 세 줄을 넣습니다.
칸 `embedding`의 자료형 `vector(3)`은 숫자 셋짜리 벡터를 담는 pgvector 자료형입니다.
벡터 값은 임베딩 모델이 만든 값이 아니라, 실행 전에 손으로 정한 값입니다.
세 숫자는 차례로 배송·환불·결제 쪽을 뜻하고, 문서마다 제 쪽 숫자만 1입니다.
모델 요청 없이 표와 백업을 보려고 이렇게 작은 값을 골랐습니다."""),
        code(DOCS),
        md("""**결과 읽기** — 출력 줄 `넣은 줄 수: 3`이 보입니다.
커서의 속성 `rowcount`는 앞 SQL 글이 바꾼 줄 수입니다.

다음 셀은 칸 `embedding`에 HNSW 색인을 만듭니다.
색인 HNSW는 Ch 12 02절에서 본 벡터 색인으로, 가까운 벡터를 빨리 찾게 도와줍니다.
pgvector 문서는 이 색인이 여러 층의 그래프를 만든다고 적습니다.
연산자 종류 `vector_cosine_ops`는 코사인 거리에 맞춘 색인을 만듭니다."""),
        code(INDEX),
        md("""**결과 읽기** — 라벨 줄 아래 SQL 글에 색인 이름 `documents_embedding_hnsw`가 보입니다.
이 이름은 복원한 데이터베이스에서도 찾아봅니다.

다음 셀은 질문 벡터 하나로 가까운 문서 둘을 받아 옵니다.
연산자 `<=>`는 Ch 12 02절처럼 두 벡터의 코사인 거리를 셈합니다.
질문 벡터 `[0.9,0.1,0]`도 손으로 정한 값으로, 배송 쪽이 크고 환불 쪽이 조금 있는 질문입니다.
벡터는 Ch 12 02절처럼 글로 바꿔 `%s` 자리에 값으로 넘깁니다."""),
        code(SEARCH),
        md("""**결과 읽기** — 출력 줄 `가까운 문서와 코사인 거리: [('배송', 0.0061), ('환불', 0.8896)]`이 보입니다.
배송 문서가 가장 가깝고, 환불 문서가 그다음입니다.
거리는 함수 `round`로 소수 넷째 자리까지 남겼습니다.

다음 셀은 같은 SQL 글 앞에 `EXPLAIN (COSTS OFF)`를 붙입니다.
낱말 `EXPLAIN`은 서버가 그 SQL 글을 어떤 차례로 처리할지 적은 계획을 내놓게 합니다.
Ch 12 02절에서는 그 계획에서 표를 읽는 방법이 적힌 줄을 봤고, 이 교재는 그 줄을 계획 줄이라고 부릅니다.
설정 `COSTS OFF`는 어림 비용 숫자를 빼고, 계획 줄만 남깁니다.
검색은 하지 않고 계획만 봅니다."""),
        code(PLAN),
        md("""**결과 읽기** — 라벨 줄 아래 네 줄이 계획 줄입니다.
맨 아래 줄 `->  Seq Scan on documents`는 표의 줄을 처음부터 모두 읽는다는 뜻입니다.
색인 `documents_embedding_hnsw`가 있는데도, 서버는 색인을 쓰지 않는 계획을 골랐습니다.
Ch 12 02절에서 본 것처럼, 줄이 적은 표에서는 서버가 이렇게 고를 수 있습니다.
pgvector 문서도 표가 작으면 표를 모두 읽는 편이 빠를 수 있다고 적습니다.

색인을 쓰는 계획은 9절에서 복원한 데이터베이스로 봅니다.

## 4. 체크포인터 표를 같은 이름 공간에

이제 같은 이름 공간에 체크포인터 표를 둡니다.
다음 셀은 Ch 23 02절처럼 체크포인터가 쓸 연결을 따로 엽니다.
인자 `row_factory=dict_row`는 줄을 딕셔너리로 받게 하는 설정이고, 체크포인터가 이 모양을 씁니다.
문장 `SET search_path TO ch31_shared`는 이 연결이 표를 찾고 만들 이름 공간을 정합니다.
그래서 표 만들기 `setup()`이 체크포인터 표를 `ch31_shared`에 만듭니다.

이름 공간을 정하지 않으면, 체크포인터 표는 기본 이름 공간 `public`에 생깁니다.
이 절은 두 가지 표를 한 이름 공간에 두어, 이름 공간 하나로 함께 백업합니다.
3절에서 이름 공간을 지우면 체크포인터 표도 함께 지워져, 다시 실행해도 줄 수가 같습니다."""),
        code(SAVER),
        md("""**결과 읽기** — 출력 줄 `ch31_shared 안의 표:` 뒤에 표 다섯이 보입니다.
표 `documents`는 3절에서 만든 검색 문서 표입니다.
나머지 넷 `checkpoint_blobs`·`checkpoint_migrations`·`checkpoint_writes`·`checkpoints`는 `setup()`이 만든 표입니다.

Ch 23 02절에서 이름 공간 `ch23_lab`에 생긴 표 넷과 같은 이름입니다.

다음 세 셀은 모델을 쓰지 않는 그래프를 만듭니다.
상태 형식은 값 칸 하나이고, 노드 하나가 값을 두 배로 만듭니다.
Ch 23 01절처럼 체크포인터가 상태를 저장하는 모습만 보려는 그래프입니다.
상태 형식 `TypedDict`는 칸만 적은 클래스로, Ch 23에서 쓴 모양입니다."""),
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 `value`에는 정수가 들어갑니다.

다음 셀의 노드 함수 `double_value`는 받은 상태의 값을 두 배로 한 값을 냅니다.
모델을 부르지 않는 보통 함수입니다."""),
        code(NODE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수가 내는 딕셔너리의 키 `value`가 상태의 칸 이름과 같아, 그 칸이 새 값으로 바뀝니다.

다음 셀은 Ch 23 02절처럼 설계 객체에 노드 하나와 엣지 둘을 적고, 체크포인터와 함께 컴파일합니다."""),
        code(GRAPH),
        md("""**결과 읽기** — 출력 줄 `붙은 체크포인터의 종류: PostgresSaver`가 보입니다.
이 그래프는 단계를 마칠 때마다 상태를 체크포인터 표에 적습니다.

다음 셀은 스레드 이름 `backup-demo`로 값 6을 넣어 한 번 실행합니다.
메서드 `get_state`는 Ch 23 01절처럼 그 스레드의 마지막 체크포인트를 읽습니다."""),
        code(INVOKE),
        md("""**결과 읽기** — 출력 줄 `실행 결과: {'value': 12}`와 `get_state로 읽은 값: {'value': 12}`가 보입니다.
노드가 6을 두 배로 만들었고, 체크포인터가 그 상태를 같은 이름 공간의 표에 저장했습니다.
복원한 데이터베이스에서도 이 값을 읽어 봅니다.

다음 셀은 체크포인터 표 넷의 줄 수를 셉니다.
표 이름은 값이 아니라 SQL 글의 일부라, `%s` 자리가 아니라 글을 이어 붙여 넣습니다."""),
        code(COUNTS),
        md("""**결과 읽기** — 라벨 줄 아래 `checkpoints | 3`과 `checkpoint_migrations | 10`이 보입니다.
Ch 23 01절에서 본 것처럼, 노드 하나인 그래프를 한 번 실행하자 체크포인트가 셋 쌓였습니다.
표 만들기 기록의 줄 수 10은 Ch 23 02절과 같습니다.
나머지 두 표의 `checkpoint_blobs | 1`과 `checkpoint_writes | 3`은 복원 뒤에 같은 수인지만 봅니다.

## 5. 백업: 이름 공간 하나를 덤프 파일로

백업(backup)은 데이터베이스의 표와 줄을 파일로 옮겨 적어 두는 일입니다.
휴대폰의 연락처를 파일 하나로 내보내 두는 것과 비슷합니다.
이 절에서는 PostgreSQL의 명령 `pg_dump`가 이 일을 합니다.
명령 `pg_dump`가 만든 백업 파일을 덤프(dump) 파일이라고 부릅니다.

이 명령은 파이썬 함수가 아니라 따로 설치된 프로그램입니다.
이 컴퓨터에 PostgreSQL을 설치했다면 그 안에 들어 있습니다.
설치하지 않았다면, 01절 Docker 컨테이너 안에 같은 명령이 있습니다.
다음 셀은 이 컴퓨터에서 명령을 찾고, 없으면 컨테이너 안의 명령을 부르게 정합니다.

함수 `shutil.which`는 명령 이름을 받아, 운영체제가 명령을 찾는 폴더들에서 그 명령을 찾습니다.
찾으면 명령 파일의 위치를 글로, 못 찾으면 `None`을 내놓습니다.
명령 `docker exec -i`는 켜져 있는 컨테이너 안에서 명령 하나를 실행하고, 이 컴퓨터의 입력을 넘깁니다.
교재 출력은 이 컴퓨터의 명령으로 만들었고, Docker 쪽 갈래는 실행하지 않았습니다."""),
        code(FIND_TOOL),
        md("""**결과 읽기** — 출력 줄 `명령을 부를 자리: 이 컴퓨터`가 보입니다.
교재 출력을 만든 컴퓨터에는 PostgreSQL 17.11의 명령이 있었습니다.
찾은 위치는 컴퓨터마다 달라 출력하지 않았습니다.

목록 `server_args`는 명령 끝에 붙일 서버 인자입니다.
이 컴퓨터 쪽은 01절 접속 글과 같은 주소·포트·계정을 적습니다.
컨테이너 쪽은 계정만 적고, 컨테이너 안의 서버에 비밀번호 없이 붙습니다.
PostgreSQL Docker 이미지 문서는 컨테이너 안에서 붙으면 비밀번호를 묻지 않는다고 적습니다.

다음 셀의 함수 `run_tool`은 명령 이름과 인자 목록, 명령에 보낼 입력을 받아 명령을 실행합니다.
함수 `subprocess.run`은 Ch 2 08절에서 pytest를 부를 때 썼습니다.
인자 `input`은 명령의 입력으로 보낼 바이트이고, `None`이면 보내지 않습니다.
인자 `env`는 명령에 넘길 환경 변수 딕셔너리입니다.
인자 `capture_output=True`는 Ch 2 08절처럼 명령의 출력을 받아 둡니다."""),
        code(DEF_RUN),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
Ch 2 08절과 달리 `text=True`를 주지 않아, 출력을 글이 아니라 바이트로 받습니다.
덤프 파일이 글이 아닌 바이트로 된 파일이기 때문입니다.
함수가 쓰는 `tool_env`는 다음 셀에서 만듭니다.

다음 셀은 명령에 넘길 환경 변수를 준비합니다.
환경 변수는 03절에서 본 말로, 프로그램이 시작할 때 받는 이름과 값의 목록입니다.
PostgreSQL 명령들은 환경 변수 `PGPASSWORD`에서 비밀번호를 읽습니다.
노트북 환경을 Ch 28 03절처럼 `dict(os.environ)`로 복사한 뒤, 연습용 비밀번호를 넣습니다.
값은 출력하지 않습니다.

이어서 `pg_dump --version`으로 명령의 버전을 봅니다.
메서드 `decode`는 바이트를 글로 바꾸고, `strip`은 앞뒤의 빈칸과 줄바꿈을 뗍니다."""),
        code(ENV_VERSION),
        md("""**결과 읽기** — 출력 줄 `pg_dump 버전: pg_dump (PostgreSQL) 17.11`이 보입니다.
서버와 앞자리(주 버전)가 같은 17입니다.
PostgreSQL 문서는 명령 `pg_dump`가 제 주 버전보다 새 서버에서는 백업을 받지 않는다고 적습니다.
더 높은 주 버전이 만든 파일은 낮은 주 버전 서버에 들어간다고 장담하지 않는다고도 적습니다.

앞자리가 17이 아니면, 5절 첫 셀의 `pg_dump_found = shutil.which("pg_dump")` 다음 줄에 `pg_dump_found = None`을 더합니다.
그러면 컨테이너 안의 명령을 고릅니다.
다음 셀은 명령이 실패해도 멈추지 않으니, 출력 줄 `pg_dump 종료 코드:`가 0인지 꼭 봅니다.

다음 셀은 이름 공간 `ch31_shared` 하나만 덤프 파일로 받습니다.
인자 `--schema=ch31_shared`가 이름 공간을 고르고, `--format=custom`은 파일 모양을 고릅니다.
이 모양은 명령 `pg_restore`로 복원하는 파일 모양입니다.
파일은 03절처럼 함수 `tempfile.mkdtemp`로 만든 운영체제 임시 폴더에 씁니다.
파일 열기 `with open`은 Ch 2 05절에서 썼고, `"wb"`는 바이트를 쓰는 모드입니다."""),
        code(BACKUP),
        md("""**결과 읽기** — 출력 줄 `pg_dump 종료 코드: 0`과 `덤프 파일이 생겼는가: True`가 보입니다.
종료 코드 0은 명령이 오류 없이 끝났다는 뜻입니다.
파일의 위치와 크기는 실행마다 달라 출력하지 않았습니다.
임시 폴더의 파일은 노트북이 지우지 않고 둡니다.

다음 셀은 덤프 파일을 다시 읽어, 파일에 든 항목의 목차를 받습니다.
인자 `--list`를 준 `pg_restore`는 데이터베이스에 붙지 않고 목차만 출력합니다.
파일을 명령의 입력으로 보내므로, 컨테이너 안의 명령도 같은 셀로 읽을 수 있습니다.
목차 한 줄에는 항목의 종류와 이름, 그리고 실행마다 바뀌는 번호가 적혀 있습니다.
그래서 줄을 그대로 출력하지 않고, 찾는 글이 목차에 있는지만 봅니다."""),
        code(LIST),
        md("""**결과 읽기** — 출력 줄 `목차에 문서 표 항목이 있는가: True`와 `목차에 체크포인트 표 항목이 있는가: True`가 보입니다.
두 가지 표가 파일 하나에 함께 들어갔습니다.
출력 줄 `목차에 확장 항목이 있는가: False`는 파일에 pgvector 확장이 없다는 뜻입니다.

명령 `pg_dump`에 이름 공간을 골라 주면, 확장은 파일에 넣지 않습니다.
이 절의 확장은 `public`에 있지만, 노트북 밖에서 확장을 이름 공간 안에 만들어 덤프해도 목차에 없었습니다.
PostgreSQL 문서도 이름 공간을 고르면 그 이름 공간이 기대는 다른 것은 덤프하지 않는다고 적습니다.

## 6. 가설과 복원 함수

복원(restore)은 백업 파일로 표와 줄을 데이터베이스에 다시 만드는 일입니다.
새 휴대폰에서 내보내 둔 연락처 파일을 가져오는 것과 비슷합니다.
이 절에서는 명령 `pg_restore`가 덤프 파일을 새 데이터베이스 `ch31_restore`에 복원합니다.

실행 전에 가설을 세웁니다.
덤프 파일에는 확장이 없고, 문서 표의 칸 `embedding`은 확장이 만든 자료형입니다.
그래서 확장이 없는 새 데이터베이스에 복원하면, 문서 표만 만들어지지 않을 것입니다.
체크포인터 표 넷은 확장을 쓰지 않으므로 돌아오고, 저장된 값도 읽힐 것입니다.

실행 1은 확장을 만들지 않은 새 데이터베이스에 복원합니다.
실행 2에서 바꾸는 값은 하나로, 복원하기 전에 새 데이터베이스에 확장을 만듭니다.
두 실행은 같은 덤프 파일과 같은 함수를 씁니다.

다음 셀의 함수 `restore_copy`는 복원 데이터베이스를 지우고 새로 만듭니다.
인자 `make_extension`이 참이면 확장을 만들고, 거짓이면 만들지 않습니다.
그다음 덤프 파일을 명령 `pg_restore`의 입력으로 보내 복원합니다.
문장 `CREATE DATABASE`는 한 묶음 작업 안에서는 돌지 않는다고 PostgreSQL 문서가 적습니다.
그래서 SQL 글마다 바로 확정하는 2절 연결의 커서 `cur`로 보냅니다."""),
        code(DEF_RESTORE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 안의 연결 `extension_conn`은 확장을 만든 뒤 바로 닫습니다.
누가 붙어 있는 데이터베이스는 지울 수 없다고 PostgreSQL 문서가 적기 때문입니다.

다음 셀의 함수 `read_restored`는 복원 데이터베이스에 붙어, 이름 공간 `ch31_shared`의 표마다 줄 수를 셉니다.
3절의 함수 `shared_tables`에 복원 데이터베이스의 커서를 넘겨 표 이름을 받습니다.
결과는 표 이름을 키로, 줄 수를 값으로 한 딕셔너리입니다."""),
        code(DEF_READ),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀의 함수 `restored_state`는 복원 데이터베이스의 체크포인터 표로 설계 객체 `builder`를 다시 컴파일합니다.
그 그래프로 스레드 `backup-demo`의 저장된 값을 읽어 내놓습니다.
그래프를 실행하지는 않고, 저장된 상태만 읽습니다."""),
        code(DEF_STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 안에서 연 연결은 값을 읽은 뒤 닫습니다.

## 7. 실행 1: 확장 없이 복원

다음 셀은 `make_extension = False`로 복원합니다.
명령이 오류를 내면, 오류 글은 표준 오류 출력(stderr)으로 옵니다.
메서드 `splitlines`는 글을 줄마다 나눈 목록을 내놓고, 이 셀은 그 첫 줄과 끝 줄만 출력합니다.

실행 전에 예상해 봅니다.
종료 코드는 0일까요?"""),
        code(RUN1),
        md("""**결과 읽기** — 출력 줄 `pg_restore 종료 코드: 1`이 보입니다.
오류 출력 첫 줄에는 `type "public.vector" does not exist`가 있습니다.
문서 표를 만드는 SQL 글이 자료형 `public.vector`를 찾지 못한 것입니다.
끝 줄 `pg_restore: warning: errors ignored on restore: 5`는 오류 다섯을 넘기고 끝까지 복원했다는 뜻입니다.

PostgreSQL 문서는 `pg_restore`가 오류를 만나도 멈추지 않고, 끝에 오류 수를 적는다고 합니다.
노트북 밖에서 오류 출력을 모두 보자, 오류 다섯은 모두 표 `ch31_shared.documents`에 걸린 것이었습니다.
표 만들기에서 막힌 뒤, 표 주인 정하기·줄 넣기·기본 키·HNSW 색인이 표가 없어 차례로 막혔습니다.

다음 셀은 실행 1의 복원 데이터베이스에서 표마다 줄 수와 저장된 값을 읽습니다."""),
        code(READ1),
        md("""**결과 읽기** — 라벨 `표마다 줄 수:` 뒤에 표 넷이 보이고, `documents`는 없습니다.
체크포인터 표의 줄 수는 `'checkpoints': 3`처럼 4절에서 센 수와 같습니다.
출력 줄 `저장된 값: {'value': 12}`는 원래 데이터베이스에서 읽은 값과 같습니다.
가설대로, 확장이 없어도 체크포인터 표는 돌아왔고 문서 표만 빠졌습니다.

## 8. 실행 2: 확장을 만든 뒤 복원

다음 셀은 값 하나만 바꿔 `make_extension = True`로 복원합니다.
함수는 복원 데이터베이스를 다시 지우고 새로 만든 뒤, 확장부터 만듭니다.

실행 전에 예상해 봅니다.
이번에는 문서 표도 돌아올까요?"""),
        code(RUN2),
        md("""**결과 읽기** — 출력 줄 `pg_restore 종료 코드: 0`과 `오류 출력 줄 수: 0`이 보입니다.
오류 없이 복원을 마쳤습니다.

다음 셀은 실행 1과 같은 모양으로 표와 저장된 값을 읽습니다."""),
        code(READ2),
        md("""**결과 읽기** — 라벨 `표마다 줄 수:` 뒤에 표 다섯이 보이고, `'documents': 3`이 있습니다.
체크포인터 표 넷의 줄 수는 실행 1과 같습니다.
출력 줄 `저장된 값: {'value': 12}`도 같습니다.

## 9. 두 실행 견주기

다음 셀은 두 실행의 값을 한 줄씩 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄이 두 실행입니다.
실행 1 줄은 `실행 1 | False | 1 | 4 | False | {'value': 12}`입니다.
실행 2 줄은 `실행 2 | True | 0 | 5 | True | {'value': 12}`입니다.
바꾼 값은 확장 만들기 하나였고, 종료 코드와 문서 표가 있는지가 갈렸습니다.
저장된 값은 두 실행이 같았습니다.

복원한 HNSW 색인이 쓰이는지도 봅니다.
3절에서 서버는 줄이 적은 표라 색인을 쓰지 않는 계획을 골랐습니다.
다음 셀은 Ch 12 02절처럼 설정 `enable_seqscan`을 off로 둡니다.
이 설정은 서버가 표를 모두 읽는 계획을 되도록 고르지 않게 합니다.
문장 `SET`은 이 연결에서만 설정을 바꿉니다."""),
        code(RESTORED_PLAN),
        md("""**결과 읽기** — 라벨 줄 아래 `->  Index Scan using documents_embedding_hnsw on documents`가 보입니다.
서버가 복원한 색인으로 줄을 찾는 계획을 골랐습니다.
Ch 12 02절은 이런 계획 줄을 색인 스캔이라고 불렀습니다.
색인도 표와 함께 복원되어, 쓸 수 있는 상태로 돌아왔습니다.
연결은 셀 끝에서 닫았습니다.

## 10. 정리: 복원 데이터베이스와 이름 공간 지우기

다음 셀은 체크포인터 연결을 닫고, 복원 데이터베이스와 이름 공간 `ch31_shared`를 지웁니다.
복원 데이터베이스에 붙은 연결은 앞 셀들이 모두 닫았습니다.
pgvector 확장은 `ch31_lab`에 남겨 둡니다.
다시 실행하면 2절이 `IF NOT EXISTS`로 있는 확장을 그대로 씁니다."""),
        code(CLEANUP),
        md("""**결과 읽기** — 출력 줄 `남은 이름 공간: None`과 `남은 복원 데이터베이스 수: 0`이 보입니다.
이름 공간과 함께 문서 표와 체크포인터 표 넷도 지워졌습니다.
처음부터 다시 실행하면 같은 출력이 나옵니다.
임시 폴더의 덤프 파일은 실습 폴더 밖에 있어 그대로 둡니다.

## 정리

1. 한 이름 공간에 pgvector 문서 표·HNSW 색인과 체크포인터 표 넷을 함께 두었습니다.
2. 명령 `pg_dump`로 그 이름 공간을 덤프 파일 하나로 받았고, 파일에 두 가지 표는 있고 확장은 없었습니다.
3. 확장 없이 복원하자 문서 표만 빠졌고, 확장을 먼저 만들자 표 다섯과 저장된 값 `{'value': 12}`가 모두 돌아왔습니다.

06절은 이 챕터의 실습 절입니다.
02절 한 묶음 작업, 04절 작은 연결 풀, 05절 체크포인터를 상담 예약 그래프 하나로 이어 실행합니다."""),
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
    """노트북용 마크다운 한 단락(백틱·줄바꿈)을 _src 문단 글로 바꿉니다(01~04절 생성기와 같은 함수)."""
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
L_CH02_08 = "../../part1/ch02-python/08-pytest.html"
L_CH12_02 = "../../part3/ch12-retrieval-tuning/02-pgvector와-HNSW.html"
L_CH23_01 = "../../part6/ch23-persistence/01-체크포인터와-스레드.html"
L_CH23_02 = "../../part6/ch23-persistence/02-PostgresSaver-준비와-스키마.html"
L_CH28_03 = "../../part6/ch28-mcp/03-stdio와-원격-전송-권한-경계.html"
L_CH30_10 = "../ch30-fastapi-serving/10-FastAPI-서빙-실습.html"
L_01 = "01-SQLAlchemy-비동기-PostgreSQL.html"
L_02 = "02-트랜잭션과-원자성.html"
L_03 = "03-Alembic-적용과-롤백.html"
L_04 = "04-커넥션-풀-고갈과-대응.html"

TERM_ROWS = [
    ("백업(backup)", "데이터베이스의 표와 줄을 파일로 옮겨 적어 두는 일입니다. 휴대폰의 연락처를 파일 하나로 내보내 두는 것과 같습니다. 이 절에서는 명령 <code>pg_dump</code>가 이름 공간 <code>ch31_shared</code>를 파일 하나로 받습니다."),
    ("복원(restore)", "백업 파일로 표와 줄을 데이터베이스에 다시 만드는 일입니다. 새 휴대폰에서 내보내 둔 연락처 파일을 가져오는 것과 같습니다. 이 절에서는 명령 <code>pg_restore</code>가 새 데이터베이스 <code>ch31_restore</code>에 복원합니다."),
    ("덤프 파일(dump)", "명령 <code>pg_dump</code>가 만든 백업 파일입니다. 연락처를 내보낸 파일 그 자체에 해당합니다. 이 절은 <code>pg_restore</code>로 복원하는 모양 <code>--format=custom</code>으로 받았고, 목차는 <code>pg_restore --list</code>로 봅니다."),
]

COMPARE_ROWS = [
    ("바꾼 값(복원 전에 확장 만들기)", "<code>False</code>", "<code>True</code>"),
    ("<code>pg_restore</code> 종료 코드", "<code>1</code>", "<code>0</code>"),
    ("오류 출력", "첫 줄 <code>type \"public.vector\" does not exist</code> · 끝 줄 <code>errors ignored on restore: 5</code>", "0줄"),
    ("복원된 표", "넷(<code>documents</code> 없음)", "다섯(<code>'documents': 3</code>)"),
    ("체크포인터 표 줄 수", "<code>'checkpoints': 3</code>을 비롯해 4절과 같음", "실행 1과 같음"),
    ("저장된 값", "<code>{'value': 12}</code>", "<code>{'value': 12}</code>"),
]

B4_ANALOGY = ("<p>옛 전화 교환대에서, 판에 선이 꽂힌 모양을 배선표 한 장에 적어 둔다고 해 봅니다. "
              "새 판에서 배선표대로 다시 꽂으면 같은 모양을 만들 수 있습니다. "
              "배선표가 덤프 파일이고, 새 판에 다시 꽂는 일이 복원입니다.</p>"
              "<p>그런데 선 하나는 판에 따로 단 자리에만 꽂힙니다. 그 자리는 판을 만들 때 달아야 하고, 배선표에는 적혀 있지 않습니다. "
              "</p><p>같은 새 판 둘을 나란히 놓습니다. 왼쪽 판은 그 자리를 달지 않아, 짙은 회색 선 넷만 꽂혀 있습니다. "
              "노란 초록 선 하나는 판 아래 턱에 놓여 있습니다. 오른쪽 판은 자리를 먼저 달아, 선 다섯이 모두 꽂혀 있습니다.</p>"
              "<p>새 판 하나가 복원을 받은 데이터베이스이고, 회색 선 넷이 체크포인터 표 넷입니다. "
              "노란 초록 선이 검색 문서 표이고, 따로 다는 자리가 확장 vector입니다. 왼쪽 판이 실행 1, 오른쪽 판이 실행 2입니다.</p>"
              "<p>비유와 다른 점이 있습니다. 실제 복원은 선을 옮겨 꽂는 일이 아니라, 파일에 적힌 SQL 글로 표를 새로 만들고 줄을 넣는 일입니다.</p>")

LOOK_B5 = "노트북 3절에서 계획 줄 <code>Seq Scan on documents</code>를 봅니다. 4절에서 표 다섯과 <code>get_state로 읽은 값: {'value': 12}</code>를 확인합니다. 5절의 <code>pg_dump 버전: pg_dump (PostgreSQL) 17.11</code>과 <code>목차에 확장 항목이 있는가: False</code>도 찾습니다. 앞자리가 17이 아니면 7블록의 방법으로 컨테이너 안의 명령을 고르고, <code>pg_dump 종료 코드: 0</code>인지 봅니다."
LOOK_B6 = "7절에서 <code>pg_restore 종료 코드: 1</code>과 오류 출력 첫 줄의 <code>public.vector</code>를 봅니다. 8절에서 <code>pg_restore 종료 코드: 0</code>과 <code>'documents': 3</code>을 확인합니다. 두 실행 모두 <code>저장된 값: {'value': 12}</code>인지, 9절 계획 줄에 <code>Index Scan using documents_embedding_hnsw</code>가 있는지도 봅니다."


def src_html() -> str:
    terms = table_html(["말", "뜻"], TERM_ROWS)
    compare = table_html(["견준 것", "실행 1(확장 없이)", "실행 2(확장을 만든 뒤)"], COMPARE_ROWS)
    return """<!--meta: 강의 1h | 실습 3h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>한 이름 공간에 pgvector 문서 표·HNSW 색인과 체크포인터 표를 함께 만들고, 표 목록과 줄 수로 확인할 수 있습니다.</li>
<li>명령 <code>pg_dump</code>로 이름 공간 하나를 덤프 파일로 받고, 파일에 든 항목을 목차로 확인할 수 있습니다.</li>
<li>확장이 없을 때와 있을 때 복원한 결과를 견주어, 복원 전에 무엇을 준비해야 하는지 설명할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>에이전트 서비스는 검색에 쓸 문서 벡터와, 그래프가 저장한 실행 상태를 함께 둘 수 있습니다. 둘 다 PostgreSQL 표라면 같은 서버의 같은 이름 공간에 둘 수 있고, 백업도 한 번에 받을 수 있습니다. 다만 백업 파일 하나만으로 새 데이터베이스가 다시 만들어지는지는 따로 확인해야 합니다. 이 절은 그 확인을 실제로 해 봅니다.</p><p>절 제목의 pgvector는 PostgreSQL에 벡터 칸과 벡터 거리 계산을 더하는 확장입니다. 제목의 체크포인터는 <a href=\"""" + L_CH23_01 + """\">Ch 23 01절</a>에서 배운 말로, 그래프가 단계를 마칠 때마다 상태를 저장하는 부품입니다. 제목의 공존은 두 가지 표를 같은 이름 공간에 함께 두는 것을 말합니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_01 + """\">01절</a>에서는 절마다 제 이름 공간을 지우고 다시 만들었습니다. <a href=\"""" + L_02 + """\">02절</a>은 한 묶음 작업과 확정을, <a href=\"""" + L_03 + """\">03절</a>은 표 구조의 판 올리기와 내리기를 봤습니다. 03절은 판을 내리면 칸의 값도 없어지므로, 값을 남기려면 데이터베이스를 파일로 남겨야 한다고 적었습니다. 이 절의 백업이 그 방법입니다. <a href=\"""" + L_04 + """\">04절</a>은 빌린 연결을 닫아 반납해야 다음 요청이 연결을 받는 것을 봤습니다.</p><p>01·02·04절은 드라이버 asyncpg로 await를 쓰는 비동기 엔진을 썼습니다. 이 절은 03절처럼 await 없이 쓰는 동기 드라이버 psycopg를 씁니다. 체크포인터 <code>PostgresSaver</code>가 psycopg의 동기 연결로 표를 읽고 쓰기 때문입니다. 이 절도 04절처럼 연 연결을 모두 직접 닫습니다.</p><p><a href=\"""" + L_CH12_02 + """\">Ch 12 02절</a>에서는 psycopg로 서버에 붙어 pgvector 확장을 켰습니다. 벡터 칸이 있는 표에 HNSW 색인을 만들고, 연산자 <code>&lt;=&gt;</code>로 코사인 거리를 셈했습니다. 낱말 <code>EXPLAIN</code>이 내놓은 계획 줄에서 색인을 쓰는지 봤고, 설정 <code>enable_seqscan</code>을 off로 두면 색인 스캔이 되는 것도 봤습니다. 그 절의 컨테이너는 포트 55432와 계정 <code>student</code>를 썼고, 이 챕터의 컨테이너는 포트 55431과 계정 <code>postgres</code>를 씁니다.</p><p><a href=\"""" + L_CH23_01 + """\">Ch 23 01절</a>에서는 체크포인터 <code>InMemorySaver</code>로 스레드마다 상태를 메모리에 저장하고, <code>get_state</code>로 읽었습니다. <a href=\"""" + L_CH23_02 + """\">Ch 23 02절</a>에서는 <code>PostgresSaver</code>와 표 만들기 <code>setup()</code>으로 체크포인트를 PostgreSQL 표에 저장했습니다. 그 절은 <code>SET search_path</code>로 체크포인터 표를 이름 공간 <code>ch23_lab</code>에 두었습니다. 이 절은 같은 방법으로 표를 <code>ch31_shared</code>에 둡니다.</p><p><a href=\"""" + L_CH30_10 + """\">Ch 30 10절</a>은 이 절이 체크포인터로 그래프의 실행 상태를 PostgreSQL 표에 저장한다고 예고했습니다. 이 절은 모델을 쓰지 않는 그래프로 그 저장을 보이고, Ch 30의 앱에 붙이지는 않습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3>""" + B4_ANALOGY + """
""" + illustration_block() + """<h3>한 이름 공간에 두 가지 표</h3><p>이 절의 이름 공간 <code>ch31_shared</code>에는 표가 다섯 있습니다. 표 <code>documents</code>는 우리가 만든 검색 문서 표이고, 칸 <code>embedding</code>의 자료형은 pgvector의 <code>vector(3)</code>입니다. 나머지 넷은 체크포인터의 표 만들기 <code>setup()</code>이 만든 표입니다. 체크포인터 연결에 <code>SET search_path TO ch31_shared</code>를 보내 두어, 표 넷이 이 이름 공간에 생겼습니다.</p><p>확장 vector는 이 이름 공간이 아니라 기본 이름 공간 <code>public</code>에 있습니다. 문서 표의 칸은 그 확장의 자료형을 빌려 씁니다. 그래서 문서 표는 확장에 기대고, 체크포인터 표는 기대지 않습니다. 이 차이가 복원에서 드러납니다.</p>
""" + terms + """
<p>새 말을 이 절 코드에서 보면 이렇습니다. 백업을 받은 명령은 <code>pg_dump 종료 코드: 0</code>으로 끝났고, 덤프 파일의 목차에는 문서 표와 체크포인트 표가 있었습니다. 목차에 확장은 없었습니다. 복원은 실행 1에서 <code>pg_restore 종료 코드: 1</code>, 실행 2에서 <code>pg_restore 종료 코드: 0</code>이었습니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>계획 줄과 색인</h3><p>낱말 <code>EXPLAIN</code>을 SQL 글 앞에 붙이면, 서버는 검색하지 않고 처리할 계획만 내놓습니다. 설정 <code>COSTS OFF</code>는 어림 비용 숫자를 빼서, 실행할 때마다 같은 계획 줄만 남깁니다. 이 절의 표는 줄이 셋뿐이라, 서버는 색인이 있어도 표를 모두 읽는 계획을 골랐습니다. pgvector 문서도 표가 작으면 표를 모두 읽는 편이 빠를 수 있다고 적습니다.</p><p>설정 <code>enable_seqscan</code>을 off로 두면, 서버는 표를 모두 읽는 계획을 되도록 고르지 않습니다. PostgreSQL 문서는 이런 설정을 계획을 바꾸는 거친 방법이라 적고, 잠깐 쓰는 용도로 권합니다. 이 절은 복원한 색인이 쓰이는지 보려고만 이 설정을 씁니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 01절과 드라이버 부분만 다른 접속 글로 psycopg 연결을 열고, pgvector 확장을 켭니다. 3절은 이름 공간 <code>ch31_shared</code>에 문서 표와 HNSW 색인을 만들고, 가까운 문서와 계획 줄을 봅니다. 4절은 체크포인터 표를 같은 이름 공간에 만들고, 모델을 쓰지 않는 그래프를 한 번 실행합니다. 5절은 명령 <code>pg_dump</code>를 찾아 그 이름 공간을 덤프 파일로 받고, 목차를 봅니다.</p><p>모델 요청은 0번이고, API 키 없이 실행합니다. 데이터베이스 서버는 01절과 같은 Docker 컨테이너 <code>kdt-ch31-postgres</code>입니다. 작업 폴더에는 파일을 쓰지 않고, 덤프 파일 하나만 운영체제 임시 폴더에 씁니다. 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>가설은 이랬습니다. 이름 공간 하나만 받은 덤프 파일에는 확장이 없으므로, 확장이 없는 데이터베이스에서는 문서 표만 만들어지지 않을 것입니다. 체크포인터 표와 저장된 값은 돌아올 것입니다. 아래 표는 두 실행에서 본 값을 모은 것입니다.</p>
""" + compare + """
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>실행 1의 <code>pg_restore</code>는 종료 코드 1로 끝났습니다. 오류 출력 첫 줄은 자료형 <code>public.vector</code>가 없다는 글이었고, 끝 줄은 오류 다섯을 넘겼다고 적었습니다. 복원된 표는 체크포인터 표 넷뿐이었고, 저장된 값 <code>{'value': 12}</code>는 그대로 읽혔습니다. 가설과 맞는 결과입니다.</p><p>실행 2에서 바꾼 값은 복원 전에 확장을 만드는 것 하나였습니다. 종료 코드는 0이었고, 문서 표까지 표 다섯이 돌아왔습니다. 문서 표의 줄은 셋이었습니다. 설정 <code>enable_seqscan</code>을 off로 두자, 복원한 HNSW 색인으로 줄을 찾는 계획이 나왔습니다.</p><p>두 실행을 가른 것은 확장 하나였습니다. 이름 공간만 백업하면, 그 표들이 기대는 확장은 파일에 들지 않았습니다. 그래서 이런 덤프 파일은 복원할 데이터베이스에 같은 확장을 먼저 만들어야 모두 돌아옵니다. 체크포인터 표는 확장에 기대지 않아, 두 실행 모두 같은 줄 수와 저장된 값으로 돌아왔습니다.</p><p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>이름 공간 하나만 덤프하면, 그 이름 공간이 기대는 다른 것은 파일에 들지 않습니다. PostgreSQL 문서는 그런 덤프가 빈 데이터베이스에 혼자 복원된다고 장담하지 않는다고 적습니다. 노트북 밖에서 같은 명령에 인자 <code>--extension=vector</code>를 더하자, 확장 항목이 파일에 들었습니다. 이름 공간을 고르지 않고 데이터베이스 전체를 덤프해도 들었습니다. 이 절은 복원 전에 확장을 먼저 만드는 방법을 썼습니다.</li><li>명령 <code>pg_restore</code>는 기본으로 오류를 넘기고 끝까지 복원한다고 PostgreSQL 문서가 적습니다. 그래서 실행 1처럼 일부 표만 돌아온 데이터베이스가 남을 수 있습니다. 종료 코드와 끝 줄의 오류 수를 꼭 확인합니다. 문서는 인자 <code>--single-transaction</code>을 주면 모두 되거나 하나도 안 된다고 적습니다. <a href=\"""" + L_02 + """\">02절</a>의 한 묶음 작업과 같은 생각이고, 이번에 실행하지는 않았습니다.</li><li>노트북 밖에서 실행 1의 오류 출력을 모두 보자, 오류 다섯은 모두 표 <code>ch31_shared.documents</code>에 걸린 것이었습니다. 표 만들기가 막힌 뒤, 표 주인 정하기와 줄 넣기, 기본 키, HNSW 색인 만들기가 차례로 막혔습니다.</li><li>PostgreSQL 문서는 명령 <code>pg_dump</code>가 제 주 버전(앞자리)보다 새 서버에서는 백업을 받지 않는다고 적습니다. 더 높은 주 버전의 명령이 만든 파일은 낮은 주 버전 서버에 들어간다고 장담하지 않는다고도 적습니다. 그래서 서버와 앞자리가 같은 17인 명령이 안전합니다.</li><li>5절의 백업 셀은 종료 코드를 확인하지 않습니다. 명령이 실패해도 빈 파일을 쓰고 <code>덤프 파일이 생겼는가: True</code>를 찍어, 단서는 <code>pg_dump 종료 코드:</code> 줄뿐입니다. 이 컴퓨터 명령의 앞자리가 17이 아니면, 5절 첫 셀의 <code>pg_dump_found = shutil.which("pg_dump")</code> 다음 줄에 <code>pg_dump_found = None</code>을 더해 컨테이너 안의 명령을 고릅니다. 교재 출력은 서버와 같은 17.11 버전의 명령을 이 컴퓨터에서 불러 만들었습니다.</li><li>Docker 쪽 갈래 <code>docker exec -i kdt-ch31-postgres</code>는 교재 출력에서 실행하지 않았습니다. 컨테이너 안에서는 계정만 적고 비밀번호 없이 붙는데, PostgreSQL Docker 이미지 문서가 그렇게 적습니다. 컨테이너 안의 명령은 서버와 같은 이미지에 들어 있습니다.</li><li>연습용 비밀번호는 환경 변수 <code>PGPASSWORD</code>로 넘겼고, 명령 목록과 출력에는 적지 않았습니다. PostgreSQL 문서는 보안 까닭으로 이 환경 변수를 권하지 않고, 비밀번호 파일을 쓰라고 적습니다. 연습 밖의 서버에서는 문서의 비밀번호 파일을 씁니다.</li><li>체크포인터 연결에 이름 공간을 정하지 않으면, <code>setup()</code>은 표 넷을 기본 이름 공간 <code>public</code>에 만듭니다. 노트북 밖에서 따로 만든 데이터베이스로 확인했습니다. 그러면 이름 공간 <code>ch31_shared</code>만 백업할 때 체크포인터 표가 파일에 들지 않습니다.</li><li>노트북 밖에서 원래 데이터베이스에도 설정 <code>enable_seqscan</code>을 off로 두자, 3절 검색의 계획 줄이 색인 스캔이 되었습니다. 노트북에서는 복원한 데이터베이스에서만 이 설정을 썼습니다.</li><li>목차 줄 앞의 번호는 서버가 붙인 항목 번호라, 노트북 밖에서 다시 실행할 때마다 바뀌었습니다. 그래서 노트북은 목차에 찾는 글이 있는지만 출력합니다.</li><li>이 절의 체크포인터는 동기 <code>PostgresSaver</code>입니다. LangGraph 문서는 await로 쓰는 비동기 체크포인터 <code>AsyncPostgresSaver</code>도 적습니다. psycopg 문서는 Windows에서 psycopg의 비동기 연결이 기본 이벤트 루프와 맞지 않는다고 적습니다. 비동기 체크포인터는 이 절에서 실행하지 않았습니다.</li><li>노트북을 쓰기 전에 노트북 밖에서 같은 장면을 파이썬 파일로 다섯 번 실행했습니다. 목차 줄 번호 말고는 출력이 다섯 번 모두 같았습니다. 거리·계획 줄·표 목록·줄 수·종료 코드·오류 첫 줄과 끝 줄·저장된 값 모두 같았습니다.</li><li>교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다. 확장 pgvector는 0.8.1이고, 체크포인터 패키지는 설치된 3.0.5 버전입니다. 그 서버는 Docker 컨테이너가 아니라 같은 접속 글로 켠 서버입니다. Docker 이미지로 켜면 버전 번호의 끝자리가 다를 수 있습니다. 다른 버전과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>한 이름 공간에 pgvector 문서 표·HNSW 색인과 체크포인터 표 넷을 함께 두었습니다.</li><li>명령 <code>pg_dump</code>로 그 이름 공간을 덤프 파일 하나로 받았고, 파일에 두 가지 표는 있고 확장은 없었습니다.</li><li>확장 없이 복원하자 문서 표만 빠졌고, 확장을 먼저 만들자 표 다섯과 저장된 값 <code>{'value': 12}</code>가 모두 돌아왔습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href="06-DB와-상태-영속화-실습.html">06절</a>은 이 챕터의 실습 절입니다. 02절 한 묶음 작업, 04절 작은 연결 풀, 05절 체크포인터를 상담 예약 그래프 하나로 이어 실행합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. 체크포인터 표를 검색 문서 표와 같은 이름 공간에 두려고, 체크포인터 연결에 무엇을 보냈나요?</p><p class="quiz-a">문장 <code>SET search_path TO ch31_shared</code>를 보냈습니다. 그래서 <code>setup()</code>이 표 넷을 <code>ch31_shared</code>에 만들었습니다. 보내지 않으면 표는 기본 이름 공간 <code>public</code>에 생겼습니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">2. 5절 목차에서 확장 항목이 <code>False</code>였던 까닭은 무엇인가요?</p><p class="quiz-a">명령 <code>pg_dump</code>에 이름 공간 <code>ch31_shared</code>를 골라 주면, 확장은 어느 이름 공간에 있든 파일에 넣지 않기 때문입니다. 노트북 밖에서 확장을 이름 공간 안에 만들어 덤프해도 목차에 없었습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">3. 실행 1의 종료 코드와 복원된 표는 무엇이었나요?</p><p class="quiz-a">종료 코드는 1이었습니다. 체크포인터 표 넷만 돌아왔고, 문서 표 <code>documents</code>는 없었습니다. 저장된 값은 <code>{'value': 12}</code>로 읽혔습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">4. 실행 2에서 바꾼 값은 무엇이고, 결과는 어떻게 달라졌나요?</p><p class="quiz-a">복원하기 전에 새 데이터베이스에 확장을 만든 것 하나를 바꿨습니다. 종료 코드는 0이었고, 문서 표까지 표 다섯이 돌아왔습니다. 문서 표의 줄은 셋이었습니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p><p class="quiz-q">5. 동료가 「<code>pg_restore</code>가 끝까지 실행되었으니 복원은 된 것」이라고 말합니다. 맞나요?</p><p class="quiz-a">맞지 않을 수 있습니다. 명령 <code>pg_restore</code>는 기본으로 오류를 넘기고 끝까지 가서, 실행 1처럼 종료 코드 1과 오류 수만 남깁니다. 종료 코드와 끝 줄의 오류 수, 돌아온 표를 확인해야 합니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://github.com/pgvector/pgvector/blob/v0.8.1/README.md">pgvector README (v0.8.1)</a></div>확인 2026-09-29 · 색인 HNSW는 여러 층의 그래프를 만든다고 적습니다. 연산자 <code>&lt;=&gt;</code>는 코사인 거리이고, 코사인 거리 색인은 <code>vector_cosine_ops</code>로 만듭니다. 표가 작으면 표를 모두 읽는 편이 빠를 수 있다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/app-pgdump.html">PostgreSQL 17 pg_dump</a></div>확인 2026-09-29 · 인자 <code>-n</code>으로 이름 공간을 고르면, 그 이름 공간이 기대는 다른 것은 덤프하지 않는다고 적습니다. 그런 덤프가 빈 데이터베이스에 혼자 복원된다고 장담하지 않습니다. 모양 <code>custom</code>은 <code>pg_restore</code>에 넣을 파일이고, 제 주 버전보다 새 서버에서는 덤프하지 않는다고 적습니다. 더 높은 주 버전이 만든 파일을 낮은 주 버전 서버에 넣는 것은 장담하지 않습니다. 인자 <code>-e</code>(<code>--extension</code>)는 덤프할 확장을 고른다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/app-pgrestore.html">PostgreSQL 17 pg_restore</a></div>확인 2026-09-29 · 문서 17.11 · 파일을 주지 않으면 표준 입력을 읽는다고 적습니다. 기본은 오류를 넘기고 끝에 오류 수를 보인다고 적습니다. 인자 <code>--list</code>는 목차를, <code>--single-transaction</code>은 모두 되거나 하나도 안 되는 복원을 한다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/sql-explain.html">PostgreSQL 17 EXPLAIN</a></div>확인 2026-09-29 · 계획은 표를 어떻게 읽을지 보여 준다고 적습니다. 설정 <code>COSTS</code>는 기본이 참이고, 어림 비용과 줄 수를 넣는다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/runtime-config-query.html">PostgreSQL 17 Planner Method Configuration</a></div>확인 2026-09-29 · 설정 <code>enable_seqscan</code>을 끄면 다른 방법이 있을 때 표를 모두 읽는 계획을 피한다고 적습니다. 이런 설정은 계획을 바꾸는 거친 방법이고, 잠깐 쓰는 용도라고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/sql-createdatabase.html">PostgreSQL 17 CREATE DATABASE</a></div>확인 2026-09-29 · 한 묶음 작업 안에서는 실행할 수 없다고 적습니다. 같은 날 본 <code>DROP DATABASE</code> 문서는 누가 붙어 있으면 지울 수 없다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/libpq-envars.html">PostgreSQL 17 Environment Variables</a></div>확인 2026-09-29 · 환경 변수 <code>PGPASSWORD</code>는 보안 까닭으로 권하지 않고, 비밀번호 파일을 쓰라고 적습니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langgraph/add-memory">LangGraph Memory</a></div>확인 2026-09-29 · PostgreSQL 체크포인터를 처음 쓸 때 <code>setup()</code>을 불러야 한다고 적습니다. 비동기 체크포인터 <code>AsyncPostgresSaver</code>도 적습니다.</li><li><div><a href="https://pypi.org/project/langgraph-checkpoint-postgres/">langgraph-checkpoint-postgres</a></div>확인 2026-09-29 · 문서 3.1.2 · 연결을 직접 만들면 <code>autocommit=True</code>와 <code>row_factory=dict_row</code>를 주라고 적습니다. 체크포인터가 줄을 딕셔너리 모양으로 읽기 때문입니다.</li><li><div><a href="https://www.psycopg.org/psycopg3/docs/advanced/async.html">psycopg 3 Asynchronous operations</a></div>확인 2026-09-29 · 문서 3.3.7.dev1 · 비동기 연결의 조건을 적습니다. Windows에서는 비동기 연결이 기본 이벤트 루프와 맞지 않아, 다른 루프를 쓰라고 적습니다.</li><li><div><a href="https://hub.docker.com/_/postgres">Docker Hub postgres</a></div>확인 2026-09-29 · 이미지는 컨테이너 안에서 붙는 연결에 비밀번호를 묻지 않게 해 둔다고 적습니다.</li><li>설치판 langgraph-checkpoint-postgres 3.0.5 소스 <code>langgraph/checkpoint/postgres/__init__.py</code> 56~75행은 <code>from_conn_string</code>이 연결을 여는 자리입니다. 그 연결에 <code>autocommit=True</code>와 <code>dict_row</code>를 줍니다. 77~102행 <code>setup()</code>은 표 만들기 문장을 차례로 실행하고, 판 번호를 기록 표에 적습니다. <code>base.py</code> 37~85행은 표 넷과 색인 셋을 만드는 문장 열입니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    # 2절 설정 셀은 01절 셀 글에서 드라이버 부분만 다름(「01절 2절의 설정 셀과 드라이버 부분만 다른 셀」 문장의 근거)
    author01_text = AUTHOR01.read_text(encoding="utf-8")
    assert SETTINGS not in author01_text, "SETTINGS가 01절 셀과 글자까지 같습니다"
    assert SETTINGS.replace("postgresql://", "postgresql+asyncpg://") in author01_text, "SETTINGS가 드라이버 부분 말고도 01절 셀과 다릅니다"
    code_count = 0
    for cell in cells():
        if cell["cell_type"] == "code":
            code_count = code_count + 1
    assert 20 <= code_count <= 32, "코드 셀 수가 20~32 밖입니다"
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "05", SLUG, "experiment", cells())
        print("wrote", path, "code cells", code_count)
