"""Ch 12 02절 품질 개선본 노트북 생성기 (QUALITY-UPGRADE.md §2·§3·§6).

사용: python3 author_02.py  → labs/part3/ch12-retrieval-tuning/notebooks/02-pgvector와-HNSW.ipynb 를 새로 쓴다(출력 없음).
이후 run_section.sh 가 pre_exec.sh(pgvector 서버) → 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북은 qa/upgrade/before/notebooks/ 에 있다. experiment 형식 유지.

## 01절에서 그대로 이어 쓴 것 (handoff.md 「§01 → §02」)

- 자료: `core-documents.json`(12개) · `core-queries.json`(8개, 정답 문서 ID 칸이 글 하나인 `gold_doc_id`).
- 차원 수 256(`check_course_continuity.py` 219행 계약). `OpenAIEmbeddings(model=, dimensions=)` 와 속성 두 개.
- 경로 후보 `candidates = [".", "../../..", "../../../.."]` + for/break(Ch 10 01·Ch 11 01·Ch 12 01절과 같은 코드).
- 앞에서 배운 함수 다섯 개는 도구 파일 `notebooks/rag_tools.py` 에서 가져온다(§2-7 리팩터, 2026-09-21 작업자 A):
  `cosine_distance`(01절, NumPy 판) · `unique_doc_ids` · `find_gold_rank`(Ch 11 01절) · `recall_at` · `mean_score`(Ch 11 02절).
  리팩터 전에는 Ch 9 03절 반복문 판 거리 함수 세 개와 01절·Ch 11 함수 다섯 개를 노트북에 다시 적었다.
  5절 「01절 거리 함수 이어 쓰기」는 코드 셀 없는 설명 소절로 남겨 절 번호를 지켰다.
- 이 절이 처음 가르친 `run_search` · `print_hits` · `find_scan_line` · `set_seqscan` 은 노트북에 남긴다.
  도구 파일에는 커서·SQL을 인자로 받는 판이 있고 03절부터 가져간다.
- 거리는 소수 둘째 자리까지만 출력한다(01절 탐색에서 셋째 자리가 흔들렸다). 그림 라벨에 거리 값을 넣지 않는다.

## 이 절이 새로 가르치는 것

- `psycopg.connect(url, autocommit=True)` · `conn.cursor()` · `cur.execute(sql, 값들)` · `cur.fetchone()` · `cur.fetchall()` · `conn.close()`.
  Ch 4 03절 sqlite3(`connect`·`execute(sql, [값])`·`fetchall`)와 이어 쓴다. 자리표시자가 `?` 에서 `%s` 로 바뀌는 점을 본문·노트북에 적었다.
- SQL: `CREATE EXTENSION` · `DROP TABLE IF EXISTS` · `CREATE TABLE ... vector(256)` · `INSERT` · `count(*)` ·
  `ORDER BY ... LIMIT` · `CREATE INDEX ... USING hnsw (embedding vector_cosine_ops)` · `EXPLAIN` · `set_config()` · `SHOW`.
  `LIMIT` 은 Part 1~2 에서 가르치지 않아(과정 요약 §2) 처음 쓰는 자리에서 뜻을 풀었다.
- 거리 연산자 `<=>`(코사인 거리). 01절 파이썬 계산값과 같은 값이 나오는지 대조한다.

## 선택한 것과 까닭

1. **pgvector 파이썬 패키지를 쓰지 않는다**(numpy 는 도구 파일이 쓰므로 설치 목록에만 넣는다). 개선 전 셀은 `np.array(..., dtype=np.float32)` 와
   `register_vector(conn)` 를 썼고 numpy 는 Part 1~3 에서 가르친 적이 없다. 탐색 실행에서 벡터를
   `str(목록)` 으로 넘기면 pgvector 의 글 모양(`[0.1,0.2,...]`)과 같아 `INSERT` 와 `<=>` 가 모두 그대로 동작했다.
   그래서 설치 목록도 psycopg·python-dotenv·langchain-openai 세 개로 줄였다(실습 폴더 잠금은 고치지 않았다).
2. **`Decimal` 을 쓰지 않는다.** 개선 전은 `round((embedding <=> %s)::numeric, 4)` 로 `Decimal('0.4324')` 를 출력했다.
   01절이 파이썬 `round(값, 2)` 로 거리를 출력하므로 SQL 은 거리를 그대로 받고 `round(row[1], 2)` 로 맞췄다(handoff 결정 항목).
3. **`SET` 대신 `set_config()`.** `SET` 문장에는 자리표시자를 쓸 수 없어 개선 전 셀은 `%` 서식과 f-string 으로 SQL 을 만들었다.
   Ch 4 03절이 「입력 값은 자리표시자로 넘긴다」를 가르쳤으므로 같은 일을 하는 함수 `set_config(이름, 값, false)` 로 값을 넘긴다.
4. **「언제 색인을 타는가」를 `EXPLAIN` 으로 보인다.** 개선 전은 `enable_seqscan`·`enable_indexscan` 을 강제로 바꿔
   두 경로를 만들었을 뿐이고 계획기가 무엇을 골랐는지는 보여 주지 않았다. 탐색 실행에서 색인을 만든 뒤에도
   12행짜리 표에서는 계획이 `Seq Scan` 이었다. 이 사실이 이 절의 결론이다(시간은 재지 않았다).
5. **파일을 쓰지 않는다.** 개선 전 마지막 셀은 `runs/core-02-hnsw.json` 을 덮어쓰고 `runs/core-history/` 에 보존본을 남겼다.
   `Path`·`hashlib`·`datetime`·세미콜론·한 줄 복합문을 쓰고 이 절 주제와 무관하다. 읽는 쪽은
   `check_course_continuity.py` 187~196행 하나이고 바이트만 본다. 정본 `core-02-hnsw.json` 은
   2026-09-18 현재 `e007a959899e…` 이고 `runs/core-history/before-e007a959899e-core-02-hnsw.json` 과 바이트가 같다.
   그래서 파일을 쓰지 않는 쪽이 가장 안전하다(Ch 9 07·Ch 10 09·Ch 11 07·Ch 12 01절 선례).
6. **2001차원 한계 실험은 남긴다.** 이 챕터가 `vector(256)` 을 쓰는 까닭을 실행으로 보여 준다.
   받아 출력한 오류라 그림에서 노랑이다(규격 §5-3, Ch 6 검토 02-1).

## 탐색 실행에서 확인한 값 (2026-09-18, /tmp/ch12-02/probe3.py·probe4.py)

PostgreSQL 17.11 · pgvector 0.8.1. 첫 질문 `C01` 상위 3개는 `LIB-004` 0.43 · `LIB-001` 0.56 · `LIB-003` 0.62 로
01절 파이썬 계산값과 같았다. 색인을 만든 뒤에도 계획기 기본 계획은 `Seq Scan` 이었고 `enable_seqscan` 을 off 로
바꾸면 `Index Scan using ch12_core_hnsw_idx` 였다. `hnsw.ef_search` 4와 40에서 상위 3개가 같았다.
질문 8개를 두 경로로 재니 정답 자리(C01 2 · C02 7 · 나머지 1)와 질문 평균 재현율(자리 1 0.75 · 자리 2 0.875 ·
자리 3 0.875)이 두 경로에서 같고 01절 값과도 같았다. `vector(2001)` HNSW 색인은
`column cannot have more than 2000 dimensions for hnsw index`, `halfvec(2001)` 은 성공이었다.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import KEY, RUN_DATE, code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part3/ch12-retrieval-tuning/notebooks"

INSTALL = install_source(["psycopg[binary]==3.3.5", "python-dotenv==1.2.3", "langchain-openai==1.6.1", "numpy==2.5.3"])

IMPORTS = r'''# 자료 파일 읽기·데이터베이스 접속·임베딩에 쓸 이름을 불러옵니다
import json

import psycopg
from langchain_openai import OpenAIEmbeddings
# 01절과 Ch 11 01·02절 함수 다섯 개를 도구 파일에서 가져옵니다
from rag_tools import cosine_distance, find_gold_rank, mean_score
from rag_tools import recall_at, unique_doc_ids

print("불러온 이름:", "json", "psycopg", "OpenAIEmbeddings")'''

FIND_ROOT = r'''# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part3/ch12-retrieval-tuning/data"):
        root_path = candidate
        break
print("고른 경로:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

LOAD_DATA = r'''# 01절과 같은 문서 파일과 질문 파일을 불러옵니다
data_path = root_path + "/labs/part3/ch12-retrieval-tuning/data"
with open(data_path + "/core-documents.json", encoding="utf-8") as file:
    docs = json.loads(file.read())
with open(data_path + "/core-queries.json", encoding="utf-8") as file:
    queries = json.loads(file.read())
print("문서 수:", len(docs))
print("질문 수:", len(queries))'''

DB_NAMES = r'''# 데이터베이스 접속 글과 이 절에서 쓸 표·색인 이름을 정합니다
database_url = "postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab"
table_name = "ch12_core_hnsw"
index_name = "ch12_core_hnsw_idx"
print("표 이름:", table_name)
print("색인 이름:", index_name)'''

VALUES = r'''# 이 절에서 되풀이해 쓸 값에 이름을 붙입니다
vector_dimensions = 256
top_three = 3
top_all = 12
cutoff_values = [1, 2, 3]
print("벡터의 숫자 개수:", vector_dimensions)
print("받아 올 문서 수 두 가지:", top_three, top_all)
print("자르는 자리 세 가지:", cutoff_values)'''

CONNECT = r'''# 데이터베이스에 붙어 pgvector 확장을 켜고 두 판 번호를 봅니다
conn = psycopg.connect(database_url, autocommit=True)
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
cur.execute("SELECT current_setting('server_version')")
print("PostgreSQL 판:", cur.fetchone()[0])
cur.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
print("pgvector 확장 판:", cur.fetchone()[0])'''

MODEL = r'''# 01절과 같은 임베딩 모델과 벡터의 숫자 개수를 씁니다(요청은 아직 보내지 않습니다)
embedding_model_name = "text-embedding-3-small"
embedding_model = OpenAIEmbeddings(model=embedding_model_name, dimensions=vector_dimensions)
print("임베딩 모델 이름:", embedding_model.model)
print("벡터의 숫자 개수 설정:", embedding_model.dimensions)'''

DOC_VECTORS = r'''# 문서 12개의 제목과 본문을 이어 붙여 한 번에 임베딩합니다(임베딩 요청 1번)
doc_texts = []
doc_ids = []
for doc in docs:
    doc_texts.append(doc["title"] + " " + doc["text"])
    doc_ids.append(doc["doc_id"])
doc_vectors = embedding_model.embed_documents(doc_texts)
print("문서 벡터 수:", len(doc_vectors))
print("첫 문서 벡터의 숫자 개수:", len(doc_vectors[0]))'''

CREATE_TABLE = r'''# 벡터 칸이 있는 표를 새로 만듭니다(같은 이름의 옛 표는 먼저 지웁니다)
cur.execute("DROP TABLE IF EXISTS " + table_name)
create_sql = "CREATE TABLE " + table_name + " (doc_id text PRIMARY KEY, category text,"
create_sql = create_sql + " embedding vector(" + str(vector_dimensions) + "))"
cur.execute(create_sql)
print("표 만들기 SQL:")
print(create_sql)'''

INSERT = r'''# 문서 벡터를 글로 바꿔 표에 한 줄씩 넣고 들어간 행 수를 셉니다
insert_sql = "INSERT INTO " + table_name + " VALUES (%s, %s, %s)"
for i in range(len(docs)):
    vector_text = str(doc_vectors[i])
    cur.execute(insert_sql, (docs[i]["doc_id"], docs[i]["category"], vector_text))
cur.execute("SELECT count(*) FROM " + table_name)
print("표에 들어간 행 수:", cur.fetchone()[0])'''

QUERY_VECTORS = r'''# 질문 8개를 하나씩 임베딩해 질문 벡터 목록을 만듭니다(임베딩 요청 8번)
query_vectors = []
for query in queries:
    query_vectors.append(embedding_model.embed_query(query["question"]))
first_question_vector = query_vectors[0]
print("질문 벡터 수:", len(query_vectors))
print("첫 질문:", queries[0]["qid"], "|", queries[0]["question"])
print("첫 질문의 정답 문서 ID:", queries[0]["gold_doc_id"])'''

PY_DISTANCE = r'''# 01절 함수로 첫 질문과 첫 문서 사이의 코사인 거리를 미리 계산해 둡니다
first_doc_vector = doc_vectors[0]
python_distance = cosine_distance(first_question_vector, first_doc_vector)
print("첫 문서 ID:", doc_ids[0])
print("파이썬으로 낸 코사인 거리:", round(python_distance, 2))'''

SEARCH_SQL = r'''# 코사인 거리가 작은 문서부터 받아 오는 SQL 문장을 만듭니다
search_sql = "SELECT doc_id, embedding <=> %s FROM " + table_name
search_sql = search_sql + " ORDER BY embedding <=> %s LIMIT %s"
print("검색 SQL:")
print(search_sql)'''

RUN_SEARCH = r'''# 질문 벡터 하나로 표를 검색해 문서 ID와 코사인 거리 목록을 반환합니다
def run_search(question_vector, top_count):
    # 벡터를 글로 바꿔 %s 자리에 값으로 넘깁니다
    vector_text = str(question_vector)
    cur.execute(search_sql, (vector_text, vector_text, top_count))
    hit_list = []
    for row in cur.fetchall():
        hit_list.append({"doc_id": row[0], "거리": round(row[1], 2)})
    return hit_list'''

PRINT_HITS = r'''# 검색 결과를 순위·문서 ID·코사인 거리 세 칸으로 출력합니다
def print_hits(hit_list):
    print("순위 | 문서 ID | 코사인 거리")
    for rank_number in range(len(hit_list)):
        row = hit_list[rank_number]
        print(rank_number + 1, "|", row["doc_id"], "|", row["거리"])'''

SCAN_LINE = r'''# 실행 계획에서 표를 어떻게 읽는지 적힌 줄만 골라 반환합니다
def find_scan_line(question_vector):
    vector_text = str(question_vector)
    cur.execute("EXPLAIN " + search_sql, (vector_text, vector_text, top_three))
    scan_line = ""
    for row in cur.fetchall():
        if "Scan" in row[0]:
            scan_line = row[0]
            break
    return scan_line.strip()'''

SET_SCAN = r'''# 계획기가 순차 스캔을 고를 수 있는지 여부를 바꾸고 바뀐 값을 반환합니다
def set_seqscan(setting_value):
    # SET 문장에는 자리표시자를 쓸 수 없어 같은 일을 하는 함수로 값을 넘깁니다
    cur.execute("SELECT set_config('enable_seqscan', %s, false)", (setting_value,))
    cur.execute("SHOW enable_seqscan")
    return cur.fetchone()[0]'''

RUN_ONE = r'''# 실행 1: 색인이 없는 표에서 첫 질문을 검색하고 실행 계획도 봅니다
print("이 표의 색인:", "없음")
print("실행 계획의 읽기 방법 줄:")
print(find_scan_line(first_question_vector))
no_index_hits = run_search(first_question_vector, top_three)
print_hits(no_index_hits)'''

CREATE_INDEX = r'''# 코사인 거리에 맞는 연산자 클래스로 HNSW 색인을 만듭니다
index_sql = "CREATE INDEX " + index_name + " ON " + table_name
index_sql = index_sql + " USING hnsw (embedding vector_cosine_ops)"
cur.execute(index_sql)
print("색인 만들기 SQL:")
print(index_sql)'''

RUN_TWO = r'''# 실행 2: 색인이 있는 표에서 같은 SQL을 실행하고 계획을 다시 봅니다
print("이 표의 색인:", index_name)
print("실행 계획의 읽기 방법 줄:")
print(find_scan_line(first_question_vector))
with_index_hits = run_search(first_question_vector, top_three)
print_hits(with_index_hits)'''

RUN_THREE = r'''# 실행 3: 설정 enable_seqscan만 off로 바꿔 색인 경로를 고르게 합니다
print("enable_seqscan 설정:", set_seqscan("off"))
print("실행 계획의 읽기 방법 줄:")
print(find_scan_line(first_question_vector))
index_path_hits = run_search(first_question_vector, top_three)
print_hits(index_path_hits)'''

EF_SEARCH = r'''# 색인 경로에서 ef_search만 4와 40으로 바꿔 상위 3개를 견줍니다
ef_values = [4, 40]
ef_rows = []
for ef_value in ef_values:
    cur.execute("SELECT set_config('hnsw.ef_search', %s, false)", (str(ef_value),))
    hit_list = run_search(first_question_vector, top_three)
    ef_rows.append({"ef_search": ef_value, "문서 ID": unique_doc_ids(hit_list)})
print("ef_search | 상위 3개 문서 ID")
for row in ef_rows:
    print(row["ef_search"], "|", row["문서 ID"])'''

DIM_TRY = r'''# 자료형과 차원 수를 받아 HNSW 색인을 만들어 보고 결과 글을 반환합니다
def try_hnsw_index(type_name, dimension_count):
    # 표 이름과 자료형 이름은 값이 아니라 문장의 일부라 자리표시자로 넘길 수 없습니다
    dim_table = "ch12_dim_" + type_name
    cur.execute("DROP TABLE IF EXISTS " + dim_table)
    cur.execute("CREATE TABLE " + dim_table + " (embedding " + type_name + "(" + str(dimension_count) + "))")
    try:
        cur.execute("CREATE INDEX ON " + dim_table + " USING hnsw (embedding " + type_name + "_cosine_ops)")
        return "색인을 만들었습니다"
    except psycopg.Error as error:
        return error.diag.message_primary'''

DIM_RUN = r'''# vector와 halfvec에 2001차원 칸을 만들어 색인 한도를 확인합니다
dimension_count = 2001
dimension_rows = []
for type_name in ["vector", "halfvec"]:
    outcome_text = try_hnsw_index(type_name, dimension_count)
    dimension_rows.append({"자료형": type_name, "결과": outcome_text})
print("자료형 | 차원 수 | 색인 결과")
for row in dimension_rows:
    print(row["자료형"], "|", dimension_count, "|", row["결과"])'''

SCORE_ONE = r'''# 질문 하나를 한 경로로 검색해 기록 한 줄을 만듭니다
def score_one(query_index, path_name):
    query = queries[query_index]
    gold_doc_ids = [query["gold_doc_id"]]
    hit_list = run_search(query_vectors[query_index], top_all)
    found_ids = unique_doc_ids(hit_list)
    row = {"경로": path_name, "질문": query["qid"]}
    row["정답 자리"] = find_gold_rank(found_ids, gold_doc_ids)
    for cutoff in cutoff_values:
        row["자리 " + str(cutoff)] = recall_at(found_ids, gold_doc_ids, cutoff)
    return row'''

SCORE_ALL = r'''# 질문 여덟 개를 두 경로로 모두 검색해 기록 줄을 담습니다(임베딩 요청은 더 보내지 않습니다)
score_rows = []
for path_name in ["순차 스캔", "색인"]:
    if path_name == "색인":
        set_seqscan("off")
    else:
        set_seqscan("on")
    for query_index in range(len(queries)):
        score_rows.append(score_one(query_index, path_name))
print("담은 기록 줄 수:", len(score_rows))'''

TABLE = r'''# 경로·질문·정답 자리·자리 1·자리 3 다섯 칸을 라벨 줄 아래에 차례로 출력합니다
print("경로 | 질문 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율")
for row in score_rows:
    print(row["경로"], "|", row["질문"], "|", row["정답 자리"], "|", row["자리 1"], "|", row["자리 3"])'''

MEANS = r'''# 두 경로의 질문 평균 재현율을 자르는 자리마다 견줍니다
print("경로 | 자르는 자리 | 질문 평균 재현율")
for path_name in ["순차 스캔", "색인"]:
    picked = []
    for row in score_rows:
        if row["경로"] == path_name:
            picked.append(row)
    for cutoff in cutoff_values:
        scores = []
        for row in picked:
            scores.append(row["자리 " + str(cutoff)])
        print(path_name, "|", cutoff, "|", mean_score(scores))'''

CLOSE = r'''# 차원 한도를 보려고 만든 표 두 개를 지우고 연결을 닫습니다
cur.execute("DROP TABLE IF EXISTS ch12_dim_vector")
cur.execute("DROP TABLE IF EXISTS ch12_dim_halfvec")
set_seqscan("on")
conn.close()
print("연결 닫힘:", conn.closed)'''

TITLE = """# pgvector와 HNSW

**이 노트북에서 할 일**

1. 01절과 같은 문서 12개 벡터를 PostgreSQL 표의 벡터 칸에 넣습니다.
2. 거리 연산자로 가까운 문서를 받아 01절 정확 검색 순위와 대조합니다.
3. HNSW 색인을 만들고 실행 계획이 어느 읽기 방법을 고르는지 봅니다.
4. 설정 하나만 바꿔 색인 경로로 검색하고 두 경로의 결과를 견줍니다.

**준비물** — 프로젝트 맨 위 `.env` 파일의 `OPENAI_API_KEY`가 필요합니다.
pgvector 확장이 든 PostgreSQL이 `127.0.0.1:55432`에서 켜져 있어야 합니다.
실습 폴더 `README.md`의 Docker 명령으로 데이터베이스를 먼저 켭니다.
읽는 자료는 01절과 같은 문서 파일과 질문 파일 두 개입니다.

임베딩 요청은 문서 한 번과 질문 여덟 번으로 모두 아홉 번입니다.
보내는 글은 900자 아래이고 예상 비용은 0.01달러 아래입니다.
실행 시간은 40초 안팎입니다.

**데이터** — 두 파일 모두 실습 묶음에 들어 있습니다.

- 문서 `labs/part3/ch12-retrieval-tuning/data/core-documents.json`(12개)
- 질문 `labs/part3/ch12-retrieval-tuning/data/core-queries.json`(8개)

**강의와 실습 범위** — 강의 시간에는 2~4절과 9~11절을 읽습니다.
데이터베이스에 붙기, 표 만들기, 행 넣기, 실행 1과 색인 만들기, 실행 2입니다.
5절은 도구 파일에서 가져온 01절 함수를 소개하고 6절은 실행만 하고 넘어갑니다.
7·8절과 12~14절은 함께 실행하고 실습 시간에 다시 읽습니다.

**기준 버전** — 첫 셀에서 psycopg 3.3.5와 python-dotenv 1.2.3을 설치합니다.
패키지 langchain-openai 1.6.1과 numpy 2.5.3도 함께 설치합니다.
데이터베이스는 pgvector 확장이 든 PostgreSQL 17을 씁니다.
필수 최소는 pgvector 0.7.0입니다. 자료형 `halfvec`이 그 판에서 생겼습니다.

교재 출력은 PostgreSQL 17.11과 pgvector 0.8.1에서 만들었습니다.
실습 폴더 안내대로 Docker 이미지를 쓰면 확장 판 번호가 0.8.2로 나옵니다.
참고 자료로 적은 공식 문서는 v0.8.6 기준입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 버전과 Windows·macOS에서는 이번에 실행하지 않았습니다.

실습 폴더 `labs/part3/ch12-retrieval-tuning`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""

FIGURE_ALT = ("나란히 놓인 두 칸의 흐름도로 맨 위 초록 상자 질문 벡터 1개에서 왼쪽 칸 순차 스캔 경로의 파란 상자 "
              "표의 행 12개를 차례로 읽기와 파란 상자 거리 12개를 작은 값부터 정렬로 내려가고 오른쪽 칸 색인 경로의 "
              "파란 상자 이웃 그래프 따라가기와 파란 상자 살펴본 후보에서 고르기로 내려가며 두 칸이 아래 노란 상자 "
              "두 경로의 상위 3개가 같았음으로 모이는 그림")

FIGURE_READ = """왼쪽 칸은 표의 행을 처음부터 끝까지 읽는 순차 스캔이고 오른쪽 칸은 HNSW 색인을 따라가는 경로입니다.
두 칸 모두 위에서 아래로 읽습니다.
맨 아래 노란 상자는 이 노트북의 출력으로 확인한 값입니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIGURE_ALT + "](attachment:02-1-두-읽기-방법.png)\n\n" + FIGURE_READ, html="skip"),
        md("""## 1. 준비

첫 셀은 패키지 네 개를 설치하고 설치된 버전을 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 `psycopg: 3.3.5`와 `python-dotenv: 1.2.3`이 보입니다.
출력에는 `langchain-openai: 1.6.1`과 `numpy: 2.5.3`도 함께 보입니다. 네 줄이 모두 보이면 다음 셀로 넘어갑니다.
패키지 NumPy는 도구 파일이 코사인 거리를 계산할 때 씁니다.

다음 셀은 이 절에서 쓸 이름을 불러옵니다.
이름 `psycopg`는 PostgreSQL에 붙는 패키지입니다.
Ch 4 03절에서 쓴 `sqlite3`와 하는 일이 같고 붙는 데이터베이스만 다릅니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
이 노트북은 01절 `cosine_distance()`와 Ch 11 지표 함수 네 개를 가져옵니다.
Ch 11 01절 `unique_doc_ids()`·`find_gold_rank()`, 02절 `recall_at()`·`mean_score()`입니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄은 `불러온 이름: json psycopg OpenAIEmbeddings` 하나입니다.
이름 `json`은 Python에 들어 있어 설치가 필요 없습니다.
도구 파일에서 가져온 함수 다섯 개는 출력하지 않습니다.

다음 셀은 API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다."""),
        setup(KEY),
        md("""**결과 읽기** — 출력 줄은 `OPENAI_API_KEY 설정 여부: True`입니다.
키 값은 출력하지 않습니다.

다음 셀은 프로젝트 맨 위 폴더를 찾습니다.
01절과 같은 코드입니다. 후보 경로를 차례로 보고 자료 폴더가 있는 곳에서 멈춥니다."""),
        setup(FIND_ROOT),
        md("""**결과 읽기** — 출력 줄은 `고른 경로: .`입니다. `assert`도 통과했습니다.
교재 출력은 프로젝트 맨 위를 작업 폴더로 삼아 실행해서 첫째 후보를 골랐습니다.

다음 셀은 01절이 쓴 문서 파일과 질문 파일을 그대로 읽습니다."""),
        setup(LOAD_DATA),
        md("""**결과 읽기** — `문서 수: 12`와 `질문 수: 8`이 보입니다.
01절과 같은 자료라 이 절의 결과를 01절 순위와 그대로 견줄 수 있습니다.

## 2. 데이터베이스에 붙기

접속 글에는 사용자 이름과 암호, 서버 주소와 문가름 번호, 데이터베이스 이름이 들어갑니다.
이 암호는 수업 전용이라 다른 곳에 쓰지 않습니다. 접속 글은 출력하지 않습니다."""),
        code(DB_NAMES),
        md("""**결과 읽기** — `표 이름: ch12_core_hnsw`와 `색인 이름: ch12_core_hnsw_idx`가 보입니다.
표 이름을 변수에 담아 두면 SQL 문장을 만들 때 같은 이름을 되풀이해 적지 않습니다.

다음 셀은 이 절에서 되풀이해 쓸 값에 이름을 붙입니다.
숫자 `256`은 01절과 같은 벡터의 숫자 개수입니다."""),
        code(VALUES),
        md("""**결과 읽기** — `벡터의 숫자 개수: 256`과 `자르는 자리 세 가지: [1, 2, 3]`이 보입니다.
`받아 올 문서 수 두 가지: 3 12` 줄의 앞 값은 상위 3개를 볼 때, 뒤 값은 자리를 끝까지 볼 때 씁니다.

다음 셀은 데이터베이스에 붙습니다.
함수 `psycopg.connect(접속 글)`은 연결 객체를 반환합니다.
인자 `autocommit=True`를 주면 문장마다 결과를 바로 확정합니다."""),
        code(CONNECT),
        md("""**결과 읽기** — `PostgreSQL 판: 17.11`과 `pgvector 확장 판: 0.8.1`이 보입니다.
문장 `CREATE EXTENSION IF NOT EXISTS vector`는 pgvector를 이 데이터베이스에서 쓰게 켭니다.
확장이 이미 켜져 있으면 아무 일도 하지 않습니다.

교재 출력을 만든 데이터베이스의 확장 판은 위 줄에 보이는 번호입니다.
실습 폴더 안내대로 Docker 이미지를 쓰면 확장 판 번호가 0.8.2로 나옵니다.
판 번호가 달라도 이 절에서 쓰는 기능은 같습니다.

## 3. 문서를 벡터로 바꾸기

01절과 같은 모델과 같은 숫자 개수로 벡터를 만듭니다.
같은 벡터를 써야 01절 순위와 대조할 수 있습니다."""),
        code(MODEL),
        md("""**결과 읽기** — `임베딩 모델 이름: text-embedding-3-small`과 `벡터의 숫자 개수 설정: 256`이 보입니다.
이 셀은 객체만 만들므로 요청을 보내지 않습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.

다음 셀은 문서 12개를 한 번에 임베딩합니다."""),
        code(DOC_VECTORS),
        md("""**결과 읽기** — `문서 벡터 수: 12`와 `첫 문서 벡터의 숫자 개수: 256`이 보입니다.
문서 열두 개를 한 번에 보냈으므로 임베딩 요청은 한 번입니다.

## 4. 표에 넣기

벡터를 담을 칸의 자료형은 `vector(256)`입니다.
숫자 개수가 다른 벡터는 이 칸에 들어가지 않습니다.
문장 `DROP TABLE IF EXISTS`는 같은 이름의 표가 있으면 지우고 없으면 넘어갑니다."""),
        code(CREATE_TABLE),
        md("""**결과 읽기** — 라벨 줄 아래에 `CREATE TABLE ch12_core_hnsw (doc_id text PRIMARY KEY, category text, embedding vector(256))`가 보입니다.
칸 `doc_id`는 기본 키라 같은 문서 ID를 두 번 넣을 수 없습니다.
Ch 4 03절에서 sqlite3로 만든 표와 문장 모양이 같습니다.

다음 셀은 문서 12개를 표에 넣습니다.
pgvector 확장은 벡터를 `[0.1,0.2]`처럼 대괄호로 묶은 글로 읽습니다.
그래서 `str(목록)`으로 바꾼 글을 값으로 넘깁니다."""),
        code(INSERT),
        md("""**결과 읽기** — `표에 들어간 행 수: 12`가 보입니다.
SQL 함수 `count(*)`는 표의 행 수를 셉니다.
값을 넘기는 자리표시자가 Ch 4 03절 sqlite3의 `?`에서 `%s`로 바뀌었습니다.
자리표시자를 쓰는 까닭은 Ch 4 03절과 같습니다. 입력 글이 문장의 뜻을 바꾸지 못하게 막습니다.

## 5. 01절 거리 함수 이어 쓰기

01절에서 만든 함수 `cosine_distance()`를 준비 셀에서 가져왔습니다.
코사인 유사도를 가장 큰 값 1에서 뺀 값이고 작을수록 가깝습니다.
이 절에서 쓸 pgvector의 `<=>` 연산자가 내는 값도 같은 코사인 거리입니다.
6절에서 이 함수로 낸 값과 데이터베이스가 낸 값을 견줍니다.

## 6. 질문 벡터와 파이썬 계산값

질문 8개를 하나씩 임베딩합니다.
뒤에서 질문마다 순위를 낼 때 다시 쓰므로 목록에 모두 담아 둡니다."""),
        code(QUERY_VECTORS),
        md("""**결과 읽기** — `질문 벡터 수: 8`이 보입니다.
`첫 질문: C01 | 책을 빌릴 수 있는 기간은 며칠인가요?`이고 정답 문서 ID는 `LIB-001`입니다.
질문은 하나씩 보내므로 요청이 여덟 번입니다. 여기까지 요청은 모두 아홉 번입니다.

다음 셀은 첫 질문과 첫 문서 사이의 거리를 파이썬으로 먼저 계산합니다.
데이터베이스가 낸 값과 견줄 값입니다."""),
        code(PY_DISTANCE),
        md("""**결과 읽기** — `첫 문서 ID: LIB-001`이고 `파이썬으로 낸 코사인 거리: 0.56`입니다.
01절에서 같은 함수로 낸 값과 같습니다.
소수 셋째 자리 아래는 실행마다 조금 달라지므로 둘째 자리까지만 출력했습니다.

## 7. 거리 연산자로 검색하기

연산자 `<=>`는 두 벡터의 코사인 거리를 냅니다.
낱말 `ORDER BY`는 그 값이 작은 행부터 정렬합니다.
낱말 `LIMIT`은 앞에서 몇 줄만 받을지 정하고 이 절에서 처음 나옵니다."""),
        code(SEARCH_SQL),
        md("""**결과 읽기** — 라벨 줄 아래에 `SELECT doc_id, embedding <=> %s FROM ch12_core_hnsw ORDER BY embedding <=> %s LIMIT %s`가 보입니다.
자리표시자가 세 개입니다. 앞 두 개는 질문 벡터이고 마지막은 받아 올 줄 수입니다.
같은 질문 벡터를 두 자리에 넘겨 고른 값과 정렬 기준을 맞춥니다.

다음 셀은 이 SQL을 실행해 목록으로 돌려주는 함수입니다."""),
        code(RUN_SEARCH),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
메서드 `cur.fetchall()`은 받은 줄을 튜플 목록으로 냅니다. 각 튜플의 앞 값이 문서 ID입니다.

다음 셀은 검색 결과를 표 모양으로 출력하는 함수입니다."""),
        code(PRINT_HITS),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

## 8. 실행 계획 보기

데이터베이스는 같은 SQL을 여러 방법으로 읽을 수 있습니다.
문장 앞에 `EXPLAIN`을 붙이면 어떤 방법을 골랐는지 알려 줍니다.
계획은 여러 줄이라 표를 어떻게 읽는지 적힌 줄만 골라 봅니다."""),
        code(SCAN_LINE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 설정 `enable_seqscan`을 바꾸는 함수입니다.
이 설정을 off로 두면 계획기가 순차 스캔을 고르지 못합니다."""),
        code(SET_SCAN),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

## 9. 실행 1 — 색인 없는 표

실행 전에 예상해 봅니다. 색인이 없으니 표의 행을 처음부터 끝까지 읽을 것입니다.
상위 3개는 01절 정확 검색과 같기를 바랍니다."""),
        code(RUN_ONE),
        md("""**결과 읽기** — `이 표의 색인: 없음`이고 계획 줄에 `Seq Scan on ch12_core_hnsw`가 적혀 있습니다.
줄 앞의 화살표 표시는 계획이 여러 층일 때 아래 층을 가리킵니다.
괄호 안의 비용 어림 값과 행 수 어림은 실행 환경에 따라 달라집니다.

라벨 줄 아래 세 줄은 `1 | LIB-004 | 0.43`, `2 | LIB-001 | 0.56`, `3 | LIB-003 | 0.62`입니다.
01절 정확 검색의 상위 3개와 문서 ID·순서·거리 값이 모두 같습니다.
둘째 줄의 `0.56`은 6절에서 파이썬으로 낸 값과도 같습니다.

## 10. 색인 만들기

이제 HNSW 색인을 만듭니다.
연산자 클래스 `vector_cosine_ops`는 색인이 코사인 거리로 정렬한다는 뜻입니다.
검색 SQL의 연산자와 색인의 연산자 클래스가 맞아야 색인을 쓸 수 있습니다."""),
        code(CREATE_INDEX),
        md("""**결과 읽기** — 라벨 줄 아래에 `CREATE INDEX ch12_core_hnsw_idx ON ch12_core_hnsw USING hnsw (embedding vector_cosine_ops)`가 보입니다.
문장을 실행하는 동안 pgvector가 벡터 12개를 이웃 그래프로 잇습니다.

## 11. 실행 2 — 색인 있는 표

실행 전에 예상해 봅니다. 색인을 만들었으니 계획이 색인 경로로 바뀔 것 같습니다."""),
        code(RUN_TWO),
        md("""**결과 읽기** — `이 표의 색인: ch12_core_hnsw_idx`인데 계획 줄에 여전히 `Seq Scan on ch12_core_hnsw`가 적혀 있습니다.
예상과 달랐습니다. 색인을 만들어도 계획기가 색인 경로를 고른다고 보장하지 않습니다.
상위 3개는 실행 1과 같은 `1 | LIB-004 | 0.43`, `2 | LIB-001 | 0.56`, `3 | LIB-003 | 0.62`입니다.

괄호 안 `rows` 값은 계획기가 어림한 행 수입니다.
색인을 만든 뒤에는 그 값이 12이고 실행 1에서는 650이었습니다.
이 표는 행이 12개뿐이라 계획기가 차례로 읽는 쪽의 비용을 더 작게 어림했습니다.

## 12. 값 바꿔 보기 — 색인 경로로 읽게 하기

바꿀 값은 설정 `enable_seqscan` 하나입니다. on에서 off로 바꿉니다.
실행 전에 예상해 봅니다. 계획이 색인 경로로 바뀌고 상위 3개는 그대로일 것입니다."""),
        code(RUN_THREE),
        md("""**결과 읽기** — `enable_seqscan 설정: off`이고 계획 줄이 `Index Scan using ch12_core_hnsw_idx`로 바뀌었습니다.
이제 HNSW 색인의 이웃 그래프를 따라가 후보를 고릅니다.
상위 3개는 `1 | LIB-004 | 0.43`, `2 | LIB-001 | 0.56`, `3 | LIB-003 | 0.62`로 실행 1·2와 같습니다.
이번 실행에서는 색인 경로가 정확 검색과 같은 세 문서를 같은 순서로 냈습니다.

다음 셀은 색인 경로에서 `ef_search` 값만 바꿔 봅니다.
이 값은 색인을 따라갈 때 살펴볼 후보 목록의 크기이고 기본값은 40입니다.
결과에서 문서 ID만 뽑는 일은 준비 셀에서 가져온 함수 `unique_doc_ids()`가 맡습니다."""),
        code(EF_SEARCH),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄에서 `ef_search`가 `4`일 때와 `40`일 때 상위 3개가 같습니다.
두 줄 모두 `['LIB-004', 'LIB-001', 'LIB-003']`입니다.
문서가 12개뿐이라 후보를 4개만 살펴도 같은 세 문서에 닿았습니다.

반복이 끝난 뒤 설정 값은 기본값과 같은 40입니다.
큰 자료에서 값을 줄이면 결과가 달라질 수 있습니다. 이번에 그 경우는 실행하지 않았습니다.

## 13. 차원 수와 색인 한도

이 챕터가 벡터의 숫자 개수를 256으로 둔 까닭을 확인합니다.
자료형 `vector`와 `halfvec`에 2001차원 칸을 만들고 색인을 만들어 봅니다.
자료형 `halfvec`은 숫자 하나를 절반 크기로 저장해 정밀도가 낮은 대신 한도가 넓습니다."""),
        code(DIM_TRY),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
문장 `try`로 오류를 받아 결과 글로 바꿉니다. 셀은 끝까지 실행됩니다.
속성 `error.diag.message_primary`는 데이터베이스가 보낸 오류 한 줄입니다.

다음 셀은 두 자료형에 같은 차원 수로 색인을 만들어 봅니다."""),
        code(DIM_RUN),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄이 나옵니다.
자료형 `vector`는 `column cannot have more than 2000 dimensions for hnsw index`를 냈습니다.
자료형 `halfvec`은 `색인을 만들었습니다`입니다.

이 절이 쓰는 벡터의 숫자 개수 256은 2000이라는 한도 안에 있습니다.
차원 수를 더 늘리려면 자료형을 바꿔야 한다는 점을 여기서 확인했습니다.

## 14. 질문 여덟 개로 두 경로 견주기

질문 하나로는 두 경로가 같다고 말할 수 없습니다.
준비 셀에서 가져온 Ch 11 지표 함수 네 개로 질문 여덟 개를 두 경로에서 모두 잽니다.
정답 자리는 `find_gold_rank()`, 재현율은 `recall_at()`, 질문 평균은 `mean_score()`가 냅니다.

다음 셀은 질문 하나를 한 경로로 재어 기록 한 줄을 만드는 함수입니다.
받아 올 문서 수를 12로 두어 정답 문서의 자리를 끝까지 봅니다."""),
        code(SCORE_ONE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 질문 여덟 개를 두 경로로 모두 잽니다.
질문 벡터를 이미 만들어 두었으므로 임베딩 요청이 늘지 않습니다."""),
        code(SCORE_ALL),
        md("""**결과 읽기** — `담은 기록 줄 수: 16`이 보입니다. 질문 여덟 개에 경로 두 가지를 곱한 수입니다.

다음 셀은 담은 줄을 표로 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 열여섯 줄에서 정답 자리가 대부분 `1`입니다.
질문 `C01`은 두 경로 모두 정답 자리 `2`입니다.
질문 `C02`는 두 경로 모두 정답 자리 `7`이라 자리 3 재현율이 `0.0`입니다.
같은 질문 줄에서 순차 스캔과 색인의 네 칸이 모두 같습니다.
이 값들은 01절 표의 같은 질문 줄과도 같습니다.

다음 셀은 자르는 자리마다 질문 평균 재현율을 견줍니다."""),
        code(MEANS),
        md("""**결과 읽기** — 라벨 줄 아래 여섯 줄이 나옵니다.
순차 스캔은 자리 1에서 `0.75`, 자리 2에서 `0.875`, 자리 3에서 `0.875`입니다.
색인 경로도 세 값이 같습니다.
01절 정확 검색의 질문 평균과도 같은 값입니다.

다음 셀은 실습에서 만든 표 가운데 차원 한도용 두 개를 지우고 연결을 닫습니다.
검색에 쓴 표 `ch12_core_hnsw`는 지우지 않고 그대로 남깁니다."""),
        code(CLOSE),
        md("""**결과 읽기** — `연결 닫힘: True`가 보입니다.
연결을 닫으면 이 노트북에서 만든 커서도 함께 쓸 수 없게 됩니다.

## 정리

1. pgvector 표의 `vector(256)` 칸에 벡터를 넣고 `<=>` 연산자로 코사인 거리 순서를 받았습니다.
2. 색인을 만들어도 계획기가 색인 경로를 고른다고 보장하지 않습니다. 이 표에서는 `EXPLAIN`이 순차 스캔을 보여 주었습니다.
3. 이번 실행에서는 두 경로의 상위 3개와 질문 평균 재현율이 01절 정확 검색과 모두 같았습니다.

03절에서는 범주 칸이 있는 표를 새로 만들고 메타데이터 필터를 함께 걸어 검색합니다.
필터를 걸면 받아 온 줄 수가 받아 올 줄 수보다 적어질 수 있습니다."""),
    ]


if __name__ == "__main__":
    path = write_notebook(LAB, "02", "02-pgvector와-HNSW", "experiment", cells())
    print("wrote", path)
