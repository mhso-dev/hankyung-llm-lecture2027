"""Ch 12 03절 품질 개선본 노트북 생성기 (QUALITY-UPGRADE.md §2·§3·§6).

사용: python3 author_03.py  → labs/part3/ch12-retrieval-tuning/notebooks/03-메타데이터-필터와-iterative-scan.ipynb 를 새로 쓴다(출력 없음).
이후 run_section.sh 가 pre_exec.sh(pgvector 서버) → 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북은 qa/upgrade/before/notebooks/ 에 있다. **paired 형식 유지**(이 챕터에서 유일한 paired, chapter.json).

## 01·02절에서 그대로 이어 쓴 것 (handoff.md 「§01 → §02」·「§02 → §03」)

- 자료: `core-documents.json`(12개, 범주 `library`·`facility`·`account` 넷씩) · `core-queries.json`(8개, `gold_doc_id`).
- 차원 수 256(`check_course_continuity.py` 219행 계약). `OpenAIEmbeddings(model=, dimensions=)`.
- 경로 후보 `candidates = [".", "../../..", "../../../.."]` + for/break.
- 01절과 같은 코드로 다시 정의한 함수 여덟 개: `dot_product` · `vector_length` · `cosine_similarity` ·
  `cosine_distance` · `unique_doc_ids` · `find_gold_rank` · `recall_at` · `mean_score`.
- 02절과 같은 코드: `run_search` · `print_hits` · `set_seqscan`. `find_scan_line` 은 SQL 을 인자로 받게 한 판이다.
- psycopg 자리표시자 `%s`, `SET` 대신 `set_config()`(02절 결정), 거리는 소수 둘째 자리까지만 출력.
- numpy·`register_vector`·`Decimal`·`::numeric` 을 쓰지 않는다. 벡터는 `str(목록)` 으로 값에 넘긴다.

## 이 절이 새로 가르치는 것

- SQL: `WHERE category = %s` 를 거리 정렬과 함께 쓰기(Ch 4 03절 `WHERE` 와 02절 `ORDER BY ... LIMIT` 을 합침).
- 설정 `hnsw.iterative_scan`(`off`·`strict_order`·`relaxed_order`), 관찰용으로 `hnsw.max_scan_tuples` 출력.
- 파이썬 `%`(나눈 뒤 남는 값), `목록.copy()`(Ch 2 03절), 튜플 목록 `sorted()`(01절)로 범주 안 순위 만들기.

## 선택한 것과 까닭

1. **합성 자료를 numpy 없이 만든다** — handoff 「§02 → §03」의 갈래 1(규칙으로 만든 벡터)을 골랐다.
   질문 벡터 하나를 `copy()` 한 뒤 숫자 한 개만 반복 번호에 따라 조금 키운다(`shift_base`·`shift_step`).
   난수를 쓰지 않아 재현성이 확실하고 `random`·`numpy` 가 모두 필요 없다. 갈래 2(`INSERT ... SELECT` +
   `generate_series`)는 새 SQL 낱말이 늘고 값이 난수면 재현성을 따로 맞춰야 해서 쓰지 않았다.
2. **채움 행을 질문마다 50개씩 만든다**(모두 400개). 한 질문 벡터에서만 만들면 다른 질문에서는 채움 행이
   문서보다 멀어져 나중 걸러 내기가 재현되지 않았다(탐색 실행에서 확인). 질문마다 만들면 여덟 질문 모두
   초기 후보가 채움 행으로 찬다.
3. **개선 전의 8차원·3000행 대신 256차원·412행**. 이 챕터가 `vector(256)` 으로 고정돼 있고(01·02·05·06·12절),
   교육용 문서 12개를 그대로 넣어 01·02절 상위 세 개와 대조할 수 있다.
4. **`enable_seqscan` 을 off 로 두고 색인 경로를 본다**(02절이 가르친 방법). 412행 표에서도 계획기 기본 계획은
   `Seq Scan` 이었다. 02절 결론과 이어지는 사실이라 본문에 한 문장으로 적었다.
5. **질문 여덟 개 비교는 「정확 검색」 대 「색인 경로」** 로 한다. 정확 검색은 01절 거리 함수로 파이썬에서 내므로
   데이터베이스 계획과 무관하게 늘 같다. 반복 탐색을 켠 채로 질문 여덟 개를 재는 일은 **하지 않는다**:
   탐색 실행 다섯 번에서 `strict_order` 의 받아 온 줄 수가 질문에 따라 0~3으로 흔들렸다(색인을 다시 만들 때마다
   달라진다). 반복 탐색은 첫 질문 하나로만 확인하고 그 사실을 b7에 적었다.
6. **`enable_seqscan` 을 절 안에서 다시 켜지 않는다.** psycopg 는 같은 SQL 을 다섯 번 넘게 실행하면 준비된 문장으로
   바꾸고 그때의 계획을 다시 쓴다. 필터 검색 SQL 을 켠 상태와 끈 상태에서 섞어 실행하면 결과가 달라졌다
   (탐색 실행에서 확인). 그래서 필터 검색은 처음부터 끝까지 off 상태에서만 실행한다.
7. **파일을 쓰지 않는다.** 개선 전 마지막 두 셀은 `runs/core-03-iterative-scan.json` 을 덮어쓰고
   `runs/core-history/` 에 보존본을 남겼다. `Path`·`hashlib`·`datetime`·세미콜론·한 줄 복합문을 쓰고 이 절 주제와
   무관하다. 읽는 쪽은 `check_course_continuity.py` 187~196행 하나이고 바이트만 본다
   (Ch 9 07·Ch 10 09·Ch 11 07·Ch 12 01·02절 선례).
8. **`ANALYZE` 를 쓰지 않는다.** 개선 전은 표를 만든 뒤 `ANALYZE` 를 불렀다. `enable_seqscan` 을 off 로 두면
   색인 경로를 고르므로 필요 없고, 새 낱말을 하나 덜 가르친다.

## 탐색 실행에서 확인한 값 (2026-09-18, /tmp/ch12-03/probe2~7.py)

PostgreSQL 17.11 · pgvector 0.8.1. 표 412행(`other` 400 · `library`·`facility`·`account` 4씩).
필터 없는 검색 상위 3개는 `OTH-1`·`OTH-2`·`OTH-3` 이고 거리가 모두 `0.0`(소수 둘째 자리).
`enable_seqscan` off 뒤 필터 검색 계획은 `Index Scan using ch12_core_filter_idx`.
반복 탐색 off 에서 첫 질문 `C01` × 범주 `library` 는 **0줄**, `strict_order` 와 `relaxed_order` 는 **3줄**
(`LIB-004` 0.43 · `LIB-001` 0.56 · `LIB-003` 0.62 = 01·02절 상위 세 개와 같은 값).
질문 여덟 개 질문 평균 재현율은 정확 검색 `0.75`·`0.875`·`0.875`, 색인 경로 세 자리 모두 `0.375`.
같은 protocol 로 색인을 다섯 번 다시 만들어 위 값이 모두 같았다(`/tmp/ch12-03/p6-1~5.txt` 동일).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import KEY, RUN_DATE, code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part3/ch12-retrieval-tuning/notebooks"

INSTALL = install_source(["psycopg[binary]==3.3.5", "python-dotenv==1.2.3", "langchain-openai==1.6.1"])

IMPORTS = r'''# 자료 파일 읽기·제곱근 계산·데이터베이스 접속·임베딩에 쓸 이름을 불러옵니다
import json
import math

import psycopg
from langchain_openai import OpenAIEmbeddings

print("불러온 이름:", "json", "math", "psycopg", "OpenAIEmbeddings")'''

FIND_ROOT = r'''# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part3/ch12-retrieval-tuning/data"):
        root_path = candidate
        break
print("고른 경로:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

LOAD_DATA = r'''# 01·02절과 같은 문서 파일과 질문 파일을 불러옵니다
data_path = root_path + "/labs/part3/ch12-retrieval-tuning/data"
with open(data_path + "/core-documents.json", encoding="utf-8") as file:
    docs = json.loads(file.read())
with open(data_path + "/core-queries.json", encoding="utf-8") as file:
    queries = json.loads(file.read())
print("문서 수:", len(docs))
print("질문 수:", len(queries))'''

DB_NAMES = r'''# 데이터베이스 접속 글과 이 절에서 쓸 표·색인 이름을 정합니다
database_url = "postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab"
table_name = "ch12_core_filter"
index_name = "ch12_core_filter_idx"
print("표 이름:", table_name)
print("색인 이름:", index_name)'''

VALUES_ONE = r'''# 벡터의 숫자 개수와 받아 올 줄 수, 자르는 자리를 정합니다
vector_dimensions = 256
similarity_top = 1
top_three = 3
cutoff_values = [1, 2, 3]
print("벡터의 숫자 개수:", vector_dimensions)
print("받아 올 줄 수:", top_three)
print("자르는 자리 세 가지:", cutoff_values)'''

VALUES_TWO = r'''# 채움 행을 만드는 규칙과 범주 이름·경로 이름을 정합니다
filler_per_query = 50
shift_base = 0.02
shift_step = 0.0001
filler_category = "other"
category_names = ["library", "facility", "account", "other"]
path_names = ["정확 검색", "색인 경로"]
print("질문마다 만드는 채움 행 수:", filler_per_query)
print("채움 행의 숫자를 바꿀 기준과 간격:", shift_base, shift_step)
print("범주 이름 네 가지:", category_names)
print("견줄 경로 두 가지:", path_names)'''

CONNECT = r'''# 데이터베이스에 붙어 pgvector 확장을 켜고 두 판 번호를 봅니다
conn = psycopg.connect(database_url, autocommit=True)
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
cur.execute("SELECT current_setting('server_version')")
print("PostgreSQL 판:", cur.fetchone()[0])
cur.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
print("pgvector 확장 판:", cur.fetchone()[0])'''

MODEL = r'''# 01·02절과 같은 임베딩 모델과 벡터의 숫자 개수를 씁니다(요청은 아직 보내지 않습니다)
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

QUERY_VECTORS = r'''# 질문 8개를 하나씩 임베딩해 질문 벡터 목록을 만듭니다(임베딩 요청 8번)
query_vectors = []
for query in queries:
    query_vectors.append(embedding_model.embed_query(query["question"]))
first_question_vector = query_vectors[0]
print("질문 벡터 수:", len(query_vectors))
print("첫 질문:", queries[0]["qid"], "|", queries[0]["question"])'''

DOT = r'''# 두 벡터의 점곱(같은 자리 숫자끼리 곱해 모두 더한 값)을 반환하는 함수를 정의합니다
def dot_product(first, second):
    total = 0
    # 반복 번호 i로 두 벡터의 같은 자리 숫자를 짝지어 곱하고 더합니다
    for i in range(len(first)):
        total = total + first[i] * second[i]
    return total'''

LENGTH = r'''# 벡터의 길이(자기 자신과의 점곱에 제곱근을 씌운 값)를 반환하는 함수를 정의합니다
def vector_length(vector):
    # 자기 자신과의 점곱은 숫자마다 제곱해 더한 값입니다
    squared_sum = dot_product(vector, vector)
    return math.sqrt(squared_sum)'''

COSINE = r'''# 두 벡터의 코사인 유사도(점곱을 두 길이의 곱으로 나눈 값)를 반환하는 함수를 정의합니다
def cosine_similarity(first, second):
    dot = dot_product(first, second)
    # 두 길이를 곱한 값으로 나누면 화살표 길이와 관계없이 방향만 비교합니다
    length_product = vector_length(first) * vector_length(second)
    return dot / length_product'''

COS_DIST = r'''# 코사인 유사도를 코사인 거리로 바꾸는 함수를 정의합니다(01·02절과 같은 코드)
def cosine_distance(first, second):
    similarity = cosine_similarity(first, second)
    # 가장 큰 값 1에서 빼면 값이 작을수록 가까운 자가 됩니다
    return similarity_top - similarity'''

FIND_CATEGORY = r'''# 문서 ID를 받아 그 문서의 범주 이름을 반환하는 함수를 정의합니다
def find_category(doc_id):
    category_name = ""
    for doc in docs:
        if doc["doc_id"] == doc_id:
            category_name = doc["category"]
            break
    return category_name'''

FIRST_CATEGORY = r'''# 첫 질문의 정답 문서가 어느 범주에 있는지 찾습니다
first_gold_doc_id = queries[0]["gold_doc_id"]
first_category = find_category(first_gold_doc_id)
print("첫 질문의 정답 문서 ID:", first_gold_doc_id)
print("그 문서의 범주:", first_category)'''

MAKE_FILLER = r'''# 질문 벡터 하나에서 아주 가까운 채움 벡터를 규칙으로 만들어 목록으로 반환합니다
def make_filler_vectors(base_vector, count):
    vectors = []
    for number in range(count):
        vector = base_vector.copy()
        # 반복 번호를 숫자 개수로 나눈 나머지 자리 하나만 조금 키웁니다
        position = number % vector_dimensions
        vector[position] = vector[position] + shift_base + shift_step * number
        vectors.append(vector)
    return vectors'''

BUILD_FILLER = r'''# 질문 여덟 개마다 채움 벡터 50개를 만들어 한 목록에 모읍니다
filler_vectors = []
for query_index in range(len(queries)):
    made_vectors = make_filler_vectors(query_vectors[query_index], filler_per_query)
    for vector in made_vectors:
        filler_vectors.append(vector)
print("채움 벡터 수:", len(filler_vectors))
print("첫 채움 벡터의 숫자 개수:", len(filler_vectors[0]))'''

PY_DISTANCE = r'''# 첫 질문에서 채움 벡터와 문서 벡터가 얼마나 떨어져 있는지 파이썬으로 잽니다
filler_distance = cosine_distance(first_question_vector, filler_vectors[0])
first_doc_vector = doc_vectors[0]
doc_distance = cosine_distance(first_question_vector, first_doc_vector)
print("첫 채움 벡터의 코사인 거리:", round(filler_distance, 2))
print("첫 문서 ID:", doc_ids[0])
print("첫 문서의 코사인 거리:", round(doc_distance, 2))'''

CREATE_TABLE = r'''# 범주 칸과 벡터 칸이 있는 표를 새로 만듭니다(같은 이름의 옛 표는 먼저 지웁니다)
cur.execute("DROP TABLE IF EXISTS " + table_name)
create_sql = "CREATE TABLE " + table_name + " (doc_id text PRIMARY KEY, category text,"
create_sql = create_sql + " embedding vector(" + str(vector_dimensions) + "))"
cur.execute(create_sql)
print("표 만들기 SQL:")
print(create_sql)'''

INSERT = r'''# 채움 행 400개와 문서 12개를 표에 한 줄씩 넣고 들어간 행 수를 셉니다
insert_sql = "INSERT INTO " + table_name + " VALUES (%s, %s, %s)"
for i in range(len(filler_vectors)):
    filler_id = "OTH-" + str(i + 1)
    cur.execute(insert_sql, (filler_id, filler_category, str(filler_vectors[i])))
for i in range(len(docs)):
    cur.execute(insert_sql, (docs[i]["doc_id"], docs[i]["category"], str(doc_vectors[i])))
cur.execute("SELECT count(*) FROM " + table_name)
print("표에 들어간 행 수:", cur.fetchone()[0])'''

CATEGORY_COUNTS = r'''# 범주마다 몇 행인지 세어 조건을 통과하는 행의 비율을 봅니다
print("범주 | 행 수")
for category_name in category_names:
    cur.execute("SELECT count(*) FROM " + table_name + " WHERE category = %s", (category_name,))
    print(category_name, "|", cur.fetchone()[0])'''

CREATE_INDEX = r'''# 코사인 거리에 맞는 연산자 클래스로 HNSW 색인을 만듭니다(02절과 같은 문장)
index_sql = "CREATE INDEX " + index_name + " ON " + table_name
index_sql = index_sql + " USING hnsw (embedding vector_cosine_ops)"
cur.execute(index_sql)
print("색인 만들기 SQL:")
print(index_sql)'''

SQL_STRINGS = r'''# 필터 없는 검색 SQL과 범주 조건을 붙인 검색 SQL을 만듭니다
search_sql = "SELECT doc_id, embedding <=> %s FROM " + table_name
search_sql = search_sql + " ORDER BY embedding <=> %s LIMIT %s"
filter_sql = "SELECT doc_id, embedding <=> %s FROM " + table_name + " WHERE category = %s"
filter_sql = filter_sql + " ORDER BY embedding <=> %s LIMIT %s"
print("필터 없는 검색 SQL:")
print(search_sql)
print("범주 조건을 붙인 검색 SQL:")
print(filter_sql)'''

RUN_SEARCH = r'''# 질문 벡터 하나로 표를 검색해 문서 ID와 코사인 거리 목록을 반환합니다(02절과 같은 코드)
def run_search(question_vector, top_count):
    # 벡터를 글로 바꿔 %s 자리에 값으로 넘깁니다
    vector_text = str(question_vector)
    cur.execute(search_sql, (vector_text, vector_text, top_count))
    hit_list = []
    for row in cur.fetchall():
        hit_list.append({"doc_id": row[0], "거리": round(row[1], 2)})
    return hit_list'''

PRINT_HITS = r'''# 검색 결과를 순위·문서 ID·코사인 거리 세 칸으로 출력합니다(02절과 같은 코드)
def print_hits(hit_list):
    print("순위 | 문서 ID | 코사인 거리")
    for rank_number in range(len(hit_list)):
        row = hit_list[rank_number]
        print(rank_number + 1, "|", row["doc_id"], "|", row["거리"])'''

SCAN_LINE = r'''# SQL과 넘길 값을 받아 실행 계획에서 표를 어떻게 읽는지 적힌 줄만 반환합니다
def find_scan_line(sql_text, value_tuple):
    cur.execute("EXPLAIN " + sql_text, value_tuple)
    scan_line = ""
    for row in cur.fetchall():
        if "Scan" in row[0]:
            scan_line = row[0]
            break
    return scan_line.strip()'''

BASELINE = r'''# 실행 1: 필터를 걸지 않고 첫 질문에 가까운 행 세 개를 받아 옵니다
first_vector_text = str(first_question_vector)
print("실행 계획의 읽기 방법 줄:")
print(find_scan_line(search_sql, (first_vector_text, first_vector_text, top_three)))
no_filter_hits = run_search(first_question_vector, top_three)
print("받아 온 줄 수:", len(no_filter_hits))
print_hits(no_filter_hits)'''

SET_SEQSCAN = r'''# 계획기가 순차 스캔을 고를 수 있는지 여부를 바꾸고 바뀐 값을 반환합니다(02절과 같은 코드)
def set_seqscan(setting_value):
    # SET 문장에는 자리표시자를 쓸 수 없어 같은 일을 하는 함수로 값을 넘깁니다
    cur.execute("SELECT set_config('enable_seqscan', %s, false)", (setting_value,))
    cur.execute("SHOW enable_seqscan")
    return cur.fetchone()[0]'''

PLAN_CHECK = r'''# 색인 경로로 읽게 설정을 바꾸고 색인 설정 두 개와 계획 줄을 봅니다
print("enable_seqscan 설정:", set_seqscan("off"))
cur.execute("SHOW hnsw.ef_search")
print("후보 목록 크기:", cur.fetchone()[0])
cur.execute("SHOW hnsw.max_scan_tuples")
print("반복 탐색이 볼 줄 수 한도:", cur.fetchone()[0])
print("실행 계획의 읽기 방법 줄:")
print(find_scan_line(filter_sql, (first_vector_text, first_category, first_vector_text, top_three)))'''

RANK_IN_CATEGORY = r'''# 문서 12개 가운데 한 범주만 남겨 코사인 거리가 가까운 순서로 반환합니다
def rank_in_category(question_vector, category_name, top_count):
    pairs = []
    for i in range(len(docs)):
        if docs[i]["category"] == category_name:
            distance = cosine_distance(question_vector, doc_vectors[i])
            pairs.append((distance, docs[i]["doc_id"]))
    hit_list = []
    for pair in sorted(pairs):
        hit_list.append({"doc_id": pair[1], "거리": round(pair[0], 2)})
    return hit_list[:top_count]'''

EXACT_TOP = r'''# 첫 질문과 그 범주로 정확 검색 상위 세 개를 내어 받아야 하는 답을 정합니다
exact_hits = rank_in_category(first_question_vector, first_category, top_three)
print("걸 범주:", first_category)
print_hits(exact_hits)'''

UNIQUE = r'''# 순위 목록에서 문서 ID를 차례로 모으고 처음 나온 것만 남깁니다(Ch 11 01절과 같은 코드)
def unique_doc_ids(hit_list):
    doc_ids = []
    for hit in hit_list:
        if hit["doc_id"] not in doc_ids:
            doc_ids.append(hit["doc_id"])
    return doc_ids'''

GOLD_RANK = r'''# 고유 문서 목록에서 정답 문서 ID가 몇 번째 자리인지 찾습니다(Ch 11 01절과 같은 코드)
def find_gold_rank(doc_ids, gold_doc_ids):
    gold_rank = 0
    for position in range(len(doc_ids)):
        if doc_ids[position] in gold_doc_ids:
            gold_rank = position + 1
            break
    return gold_rank'''

RECALL = r'''# 고유 문서 목록을 자르는 자리에서 자르고 정답 문서가 들어온 비율을 냅니다(Ch 11 02절과 같은 코드)
def recall_at(doc_ids, gold_doc_ids, cutoff):
    top_ids = doc_ids[:cutoff]
    found_count = 0
    for gold_id in gold_doc_ids:
        if gold_id in top_ids:
            found_count = found_count + 1
    return found_count / len(gold_doc_ids)'''

MEAN = r'''# 질문마다 낸 점수를 같은 무게로 평균해 소수 셋째 자리까지 남깁니다(Ch 11 02절과 같은 코드)
def mean_score(score_list):
    total = 0
    for score in score_list:
        total = total + score
    return round(total / len(score_list), 3)'''

RUN_FILTERED = r'''# 질문 벡터와 범주 이름으로 표를 검색해 문서 ID와 코사인 거리 목록을 반환합니다
def run_filtered_search(question_vector, category_name, top_count):
    # 벡터와 범주 이름을 모두 %s 자리에 값으로 넘깁니다
    vector_text = str(question_vector)
    cur.execute(filter_sql, (vector_text, category_name, vector_text, top_count))
    hit_list = []
    for row in cur.fetchall():
        hit_list.append({"doc_id": row[0], "거리": round(row[1], 2)})
    return hit_list'''

SET_ITERATIVE = r'''# 반복 탐색 설정을 바꾸고 바뀐 값을 반환합니다
def set_iterative_scan(setting_value):
    cur.execute("SELECT set_config('hnsw.iterative_scan', %s, false)", (setting_value,))
    cur.execute("SHOW hnsw.iterative_scan")
    return cur.fetchone()[0]'''

ITERATIVE_OFF = r'''# 반복 탐색을 기본값 off로 두고 시작합니다
print("반복 탐색 설정:", set_iterative_scan("off"))'''

PICK_HITS = r'''# 질문 하나를 한 경로로 검색해 앞 세 자리 목록을 반환합니다
def pick_hits(query_index, path_name):
    question_vector = query_vectors[query_index]
    gold_doc_id = queries[query_index]["gold_doc_id"]
    category_name = find_category(gold_doc_id)
    if path_name == path_names[0]:
        hit_list = rank_in_category(question_vector, category_name, top_three)
    else:
        hit_list = run_filtered_search(question_vector, category_name, top_three)
    return hit_list'''

SCORE_ONE = r'''# 질문 하나를 한 경로로 재어 기록 한 줄을 만듭니다
def score_one(query_index, path_name):
    query = queries[query_index]
    gold_doc_ids = [query["gold_doc_id"]]
    hit_list = pick_hits(query_index, path_name)
    found_ids = unique_doc_ids(hit_list)
    row = {"경로": path_name, "질문": query["qid"]}
    row["받아 온 줄 수"] = len(found_ids)
    row["정답 자리"] = find_gold_rank(found_ids, gold_doc_ids)
    for cutoff in cutoff_values:
        row["자리 " + str(cutoff)] = recall_at(found_ids, gold_doc_ids, cutoff)
    return row'''

SCORE_ALL = r'''# 질문 여덟 개를 두 경로로 모두 재어 기록 줄을 담습니다(임베딩 요청은 더 보내지 않습니다)
score_rows = []
for path_name in path_names:
    for query_index in range(len(queries)):
        score_rows.append(score_one(query_index, path_name))
print("담은 기록 줄 수:", len(score_rows))'''

TABLE = r'''# 경로·질문·받아 온 줄 수·정답 자리·자리 1·자리 3을 라벨 줄 아래에 차례로 출력합니다
print("경로 | 질문 | 받아 온 줄 수 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율")
for row in score_rows:
    print(row["경로"], "|", row["질문"], "|", row["받아 온 줄 수"], "|", row["정답 자리"], "|", row["자리 1"], "|", row["자리 3"])'''

MEANS = r'''# 두 경로의 질문 평균 재현율을 자르는 자리마다 견줍니다
print("경로 | 자르는 자리 | 질문 평균 재현율")
for path_name in path_names:
    picked = []
    for row in score_rows:
        if row["경로"] == path_name:
            picked.append(row)
    for cutoff in cutoff_values:
        scores = []
        for row in picked:
            scores.append(row["자리 " + str(cutoff)])
        print(path_name, "|", cutoff, "|", mean_score(scores))'''

BEFORE_SHOW = r'''# 반복 탐색이 꺼져 있는지 확인하고 이 검색의 조건을 다시 적습니다
cur.execute("SHOW hnsw.iterative_scan")
print("반복 탐색 설정:", cur.fetchone()[0])
print("받아 올 줄 수:", top_three)
print("걸 범주:", first_category)'''

BEFORE_RUN = r'''# 반복 탐색을 끈 채로 첫 질문에 범주 조건을 붙여 검색합니다
before_hits = run_filtered_search(first_question_vector, first_category, top_three)
print("받아 온 줄 수:", len(before_hits))
print_hits(before_hits)'''

AFTER_RUN = r'''# 설정 하나만 strict_order로 바꿔 같은 검색을 다시 실행합니다
print("반복 탐색 설정:", set_iterative_scan("strict_order"))
after_hits = run_filtered_search(first_question_vector, first_category, top_three)
print("받아 온 줄 수:", len(after_hits))
print_hits(after_hits)
assert len(after_hits) >= len(before_hits)'''

RELAXED_RUN = r'''# 반복 탐색 값만 relaxed_order로 바꿔 한 번 더 실행합니다
print("반복 탐색 설정:", set_iterative_scan("relaxed_order"))
relaxed_hits = run_filtered_search(first_question_vector, first_category, top_three)
print("받아 온 줄 수:", len(relaxed_hits))
print_hits(relaxed_hits)'''

CLOSE = r'''# 바꾼 설정 두 개를 기본값으로 되돌리고 연결을 닫습니다
print("반복 탐색 설정:", set_iterative_scan("off"))
print("enable_seqscan 설정:", set_seqscan("on"))
conn.close()
print("연결 닫힘:", conn.closed)'''

TITLE = """# 메타데이터 필터와 iterative scan

**이 노트북에서 할 일**

1. 01절과 같은 문서 12개와 규칙으로 만든 채움 행 400개를 한 표에 넣습니다.
2. 범주 조건을 붙인 검색이 받아 올 줄 수를 채우지 못하는 장면을 봅니다.
3. 질문 여덟 개를 정확 검색과 색인 경로로 재어 재현율을 견줍니다.
4. 설정 `hnsw.iterative_scan`만 바꿔 같은 검색을 다시 실행합니다.

**준비물** — 프로젝트 맨 위 `.env` 파일의 `OPENAI_API_KEY`가 필요합니다.
pgvector 확장이 든 PostgreSQL이 `127.0.0.1:55432`에서 켜져 있어야 합니다.
실습 폴더 `README.md`의 Docker 명령으로 데이터베이스를 먼저 켭니다.
읽는 자료는 01·02절과 같은 문서 파일과 질문 파일 두 개입니다.

임베딩 요청은 문서 한 번과 질문 여덟 번으로 모두 아홉 번입니다.
보내는 글은 900자 아래이고 예상 비용은 0.01달러 아래입니다.
실행 시간은 60초 안팎입니다.

**데이터** — 두 파일 모두 실습 묶음에 들어 있습니다.

- 문서 `labs/part3/ch12-retrieval-tuning/data/core-documents.json`(12개)
- 질문 `labs/part3/ch12-retrieval-tuning/data/core-queries.json`(8개)

**강의와 실습 범위** — 강의 시간에는 5~7절과 9~11절, 14~16절을 읽습니다.
정답 문서의 범주 찾기, 채움 행 만들기, 표에 넣고 색인 만들기입니다.
이어서 실행 1과 색인 경로 설정, 정확 검색 상위 세 개를 봅니다.
14~16절은 Before와 After, 값 바꿔 보기입니다.
2~4절과 8절, 12~13절은 함께 실행하고 실습 시간에 다시 읽습니다.

**기준 버전** — 첫 셀에서 psycopg 3.3.5와 python-dotenv 1.2.3을 설치합니다.
패키지 langchain-openai 1.6.1도 함께 설치합니다.
데이터베이스는 pgvector 확장이 든 PostgreSQL 17을 씁니다.
필수 최소는 pgvector 0.8.0입니다. 반복 탐색 설정이 그 판에서 생겼습니다.

교재 출력은 PostgreSQL 17.11과 pgvector 0.8.1에서 만들었습니다.
실습 폴더 안내대로 Docker 이미지를 쓰면 확장 판 번호가 0.8.2로 나옵니다.
참고 자료로 적은 공식 문서는 v0.8.6 기준입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 버전과 Windows·macOS에서는 이번에 실행하지 않았습니다.

실습 폴더 `labs/part3/ch12-retrieval-tuning`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""

FIGURE_ALT = ("위에서 아래로 내려가는 흐름도로 초록 상자 표 ch12_core_filter 412행에서 파란 상자 색인이 "
              "가까운 후보부터 고르기 후보 목록 크기 40과 파란 상자 범주 조건을 나중에 검사와 파란 상자 "
              "조건을 통과한 줄만 남기기를 지나 맨 아래 노란 상자 받아 온 줄 수가 받아 올 줄 수보다 "
              "적어짐으로 이어지는 그림")

FIGURE_READ = """맨 위 초록 상자가 이 절에서 만드는 표이고 파란 상자 세 개가 색인 경로의 처리 순서입니다.
위에서 아래로 읽습니다. 조건 검사가 후보를 고른 다음에 옵니다.
맨 아래 노란 상자는 이 노트북의 출력으로 확인한 결과입니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIGURE_ALT + "](attachment:03-1-후보를-고른-뒤-조건-검사.png)\n\n" + FIGURE_READ, html="skip"),
        md("""## 1. 준비

첫 셀은 패키지 세 개를 설치하고 설치된 버전을 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 `psycopg: 3.3.5`와 `python-dotenv: 1.2.3`이 보입니다.
`langchain-openai: 1.6.1`도 함께 보입니다. 세 줄이 모두 보이면 다음 셀로 넘어갑니다.

다음 셀은 이 절에서 쓸 이름을 불러옵니다. 02절과 같은 네 이름입니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄은 `불러온 이름: json math psycopg OpenAIEmbeddings` 하나입니다.

다음 셀은 API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다."""),
        setup(KEY),
        md("""**결과 읽기** — 출력 줄은 `OPENAI_API_KEY 설정 여부: True`입니다.
키 값은 출력하지 않습니다.

다음 셀은 프로젝트 맨 위 폴더를 찾습니다. 01·02절과 같은 코드입니다."""),
        setup(FIND_ROOT),
        md("""**결과 읽기** — 출력 줄은 `고른 경로: .`입니다. `assert`도 통과했습니다.

다음 셀은 01·02절이 쓴 문서 파일과 질문 파일을 그대로 읽습니다."""),
        setup(LOAD_DATA),
        md("""**결과 읽기** — `문서 수: 12`와 `질문 수: 8`이 보입니다.
문서 열두 개는 범주가 세 가지이고 범주마다 네 건입니다.
이 절은 그 범주 칸을 검색 조건으로 씁니다.

## 2. 데이터베이스에 붙기

접속 글에는 사용자 이름과 암호, 서버 주소와 포트, 데이터베이스 이름이 들어갑니다.
이 암호는 수업 전용이라 다른 곳에 쓰지 않습니다. 접속 글은 출력하지 않습니다.
표 이름은 02절 표와 다른 `ch12_core_filter`입니다. 이 절은 새 표를 따로 만듭니다."""),
        code(DB_NAMES),
        md("""**결과 읽기** — `표 이름: ch12_core_filter`와 `색인 이름: ch12_core_filter_idx`가 보입니다.
이 절은 새 표를 만들고 02절 표는 건드리지 않습니다.

다음 셀은 벡터의 숫자 개수와 받아 올 줄 수, 자르는 자리를 정합니다.
숫자 `256`은 01·02절과 같은 벡터의 숫자 개수입니다."""),
        code(VALUES_ONE),
        md("""**결과 읽기** — `벡터의 숫자 개수: 256`과 `받아 올 줄 수: 3`이 보입니다.
출력 줄 `자르는 자리 세 가지: [1, 2, 3]`의 값은 뒤에서 재현율을 낼 때 씁니다.

다음 셀은 채움 행을 만드는 규칙과 이름을 정합니다.
채움 행은 필터가 걸리는 순서를 보려고 규칙으로 만드는 행입니다.
값 `0.02`와 `0.0001`은 채움 벡터의 숫자 하나를 얼마나 바꿀지 정한 기준입니다."""),
        code(VALUES_TWO),
        md("""**결과 읽기** — `질문마다 만드는 채움 행 수: 50`이 보입니다.
`범주 이름 네 가지: ['library', 'facility', 'account', 'other']` 줄에서 앞 세 가지가 문서의 범주입니다.
마지막 `other`는 채움 행에 붙일 범주입니다.
`견줄 경로 두 가지: ['정확 검색', '색인 경로']` 줄의 두 이름으로 뒤에서 기록을 나눕니다.

다음 셀은 데이터베이스에 붙습니다. 02절과 같은 방법입니다."""),
        code(CONNECT),
        md("""**결과 읽기** — `PostgreSQL 판: 17.11`과 `pgvector 확장 판: 0.8.1`이 보입니다.
교재 출력을 만든 데이터베이스의 확장 판은 위 줄에 보이는 번호입니다.
실습 폴더 안내대로 Docker 이미지를 쓰면 확장 판 번호가 0.8.2로 나옵니다.
판 번호가 달라도 이 절에서 쓰는 기능은 같습니다.

## 3. 문서와 질문을 벡터로 바꾸기

01·02절과 같은 모델과 같은 숫자 개수로 벡터를 만듭니다.
같은 벡터를 써야 01·02절 순위와 대조할 수 있습니다."""),
        code(MODEL),
        md("""**결과 읽기** — `임베딩 모델 이름: text-embedding-3-small`과 `벡터의 숫자 개수 설정: 256`이 보입니다.
이 셀은 객체만 만들므로 요청을 보내지 않습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.

다음 셀은 문서 12개를 한 번에 임베딩합니다."""),
        code(DOC_VECTORS),
        md("""**결과 읽기** — `문서 벡터 수: 12`와 `첫 문서 벡터의 숫자 개수: 256`이 보입니다.
문서 열두 개를 한 번에 보냈으므로 임베딩 요청은 한 번입니다.

다음 셀은 질문 8개를 하나씩 임베딩합니다.
질문 벡터는 채움 행을 만들 때와 검색할 때 모두 씁니다."""),
        code(QUERY_VECTORS),
        md("""**결과 읽기** — `질문 벡터 수: 8`이 보입니다.
`첫 질문: C01 | 책을 빌릴 수 있는 기간은 며칠인가요?`도 보입니다.
질문은 하나씩 보내므로 요청이 여덟 번입니다. 여기까지 요청은 모두 아홉 번입니다.

## 4. 01절 거리 함수 이어 쓰기

먼저 점곱을 만듭니다. Ch 9 03절과 01·02절에서 쓴 코드와 같습니다."""),
        code(DOT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

벡터 길이는 자기 자신과의 점곱에 제곱근을 씌운 값입니다."""),
        code(LENGTH),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

코사인 유사도는 점곱을 두 길이의 곱으로 나눈 값입니다."""),
        code(COSINE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

코사인 거리는 유사도를 가장 큰 값 1에서 뺀 값이고 작을수록 가깝습니다.
이 절에서 쓸 pgvector의 `<=>` 연산자가 내는 값도 같은 코사인 거리입니다."""),
        code(COS_DIST),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

## 5. 정답 문서의 범주 찾기

질문 파일은 정답 문서 ID만 적고 범주는 적지 않습니다.
그래서 문서 파일에서 그 문서를 찾아 범주 이름을 읽습니다.
이 범주가 검색에 걸 조건이 됩니다."""),
        code(FIND_CATEGORY),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
빈 글로 시작해 문서를 찾으면 바꾸고 `break`로 멈춥니다. Ch 11 01절과 같은 모양입니다.

다음 셀은 첫 질문의 정답 문서와 그 범주를 봅니다."""),
        code(FIRST_CATEGORY),
        md("""**결과 읽기** — `첫 질문의 정답 문서 ID: LIB-001`과 `그 문서의 범주: library`가 보입니다.
첫 질문에 답하는 문서가 범주 `library`에 있다는 뜻입니다.
이 절은 그 질문에 `library` 조건을 붙여 검색합니다.

## 6. 채움 행 만들기

나중 걸러 내기를 보려면 조건에 맞지 않는 행이 질문에 더 가까워야 합니다.
그래서 질문 벡터를 본떠 아주 가까운 벡터를 규칙으로 만듭니다.
메서드 `copy()`는 목록을 하나 더 만듭니다. Ch 2 03절에서 배운 이름입니다.
기호 `%`는 나눈 뒤 남는 값을 내고 숫자 개수보다 큰 번호도 칸 번호로 바꿉니다."""),
        code(MAKE_FILLER),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
난수를 쓰지 않으므로 다시 실행해도 같은 채움 벡터가 나옵니다.

다음 셀은 질문 여덟 개마다 채움 벡터를 만들어 한 목록에 모읍니다.
질문마다 만드는 까닭은 질문이 바뀌어도 가까운 채움 행이 있게 하려는 것입니다."""),
        code(BUILD_FILLER),
        md("""**결과 읽기** — `채움 벡터 수: 400`이 보입니다. 질문 여덟 개에 50을 곱한 수입니다.
`첫 채움 벡터의 숫자 개수: 256`도 보입니다. 문서 벡터와 숫자 개수가 같습니다.

다음 셀은 채움 벡터가 문서 벡터보다 첫 질문에 가까운지 파이썬으로 확인합니다."""),
        code(PY_DISTANCE),
        md("""**결과 읽기** — `첫 채움 벡터의 코사인 거리: 0.0`이고 `첫 문서의 코사인 거리: 0.56`입니다.
`첫 문서 ID: LIB-001` 줄의 문서는 01·02절에서도 같은 거리 값이었습니다.
채움 행이 훨씬 가깝기 때문에 색인은 채움 행을 먼저 고릅니다.
이 합성 자료는 걸러 내는 순서를 보려고 만든 것이고 임베딩 품질을 나타내지 않습니다.

## 7. 표에 넣고 색인 만들기

표에는 문서 ID 칸과 범주 칸, 벡터 칸을 둡니다.
02절 표와 칸 이름이 같고 표 이름만 다릅니다."""),
        code(CREATE_TABLE),
        md("""**결과 읽기** — 라벨 줄 아래에 `CREATE TABLE ch12_core_filter (doc_id text PRIMARY KEY, category text, embedding vector(256))`가 보입니다.
칸 `category`에 넣는 값이 이 절의 검색 조건입니다.

다음 셀은 채움 행과 문서를 표에 넣습니다.
채움 행의 문서 ID는 `OTH-`와 번호를 이어 만듭니다."""),
        code(INSERT),
        md("""**결과 읽기** — `표에 들어간 행 수: 412`가 보입니다. 채움 행 400개와 문서 12개를 더한 수입니다.
값을 넘기는 자리표시자는 02절과 같은 `%s`입니다.
벡터는 `str(목록)`으로 바꾼 글을 값으로 넘깁니다.

다음 셀은 범주마다 행이 몇 개인지 셉니다."""),
        code(CATEGORY_COUNTS),
        md("""**결과 읽기** — 라벨 줄 아래 네 줄에서 `library | 4`와 `other | 400`이 보입니다.
범주 `facility`와 `account`도 각각 4입니다.
조건 `library`를 통과하는 행은 412개 가운데 4개뿐입니다.
이렇게 통과 비율이 낮을 때 나중 걸러 내기가 문제가 됩니다.

다음 셀은 벡터 칸에 HNSW 색인을 만듭니다."""),
        code(CREATE_INDEX),
        md("""**결과 읽기** — 라벨 줄 아래에 `CREATE INDEX ch12_core_filter_idx ON ch12_core_filter USING hnsw (embedding vector_cosine_ops)`가 보입니다.
02절과 같은 연산자 클래스라 검색 SQL의 `<=>`와 짝이 맞습니다.

## 8. 검색 SQL 두 가지

첫 SQL은 02절과 같은 필터 없는 검색입니다.
둘째 SQL은 그 문장에 `WHERE category = %s`를 더한 것입니다.
조건 값도 자리표시자로 넘깁니다. Ch 4 03절에서 배운 규칙과 같습니다."""),
        code(SQL_STRINGS),
        md("""**결과 읽기** — 첫 라벨 줄 아래에 `SELECT doc_id, embedding <=> %s FROM ch12_core_filter ORDER BY embedding <=> %s LIMIT %s`가 보입니다.
둘째 라벨 줄 아래 문장에는 `WHERE category = %s`가 더 있습니다.
둘째 문장의 자리표시자는 네 개이고 순서는 벡터·범주·벡터·줄 수입니다.

다음 셀은 필터 없는 검색을 실행하는 함수입니다. 02절과 같은 코드입니다."""),
        code(RUN_SEARCH),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 검색 결과를 표 모양으로 출력하는 함수입니다. 02절과 같은 코드입니다."""),
        code(PRINT_HITS),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 실행 계획에서 읽기 방법 줄만 고르는 함수입니다.
02절 판과 달리 SQL과 넘길 값을 인자로 받습니다. 이 절은 SQL이 두 가지이기 때문입니다."""),
        code(SCAN_LINE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

## 9. 실행 1 — 필터 없는 검색

실행 전에 예상해 봅니다. 채움 행이 질문에 가장 가까우니 상위 세 개가 모두 채움 행일 것입니다."""),
        code(BASELINE),
        md("""**결과 읽기** — 계획 줄에 `Seq Scan on ch12_core_filter`가 적혀 있습니다.
행이 412개뿐이라 계획기가 차례로 읽는 쪽을 골랐습니다. 02절 12행 표에서도 같았습니다.
괄호 안의 비용 어림 값과 행 수 어림은 실행 환경에 따라 달라집니다.

`받아 온 줄 수: 3`이고 라벨 줄 아래 세 줄은 `1 | OTH-1 | 0.0`, `2 | OTH-2 | 0.0`, `3 | OTH-3 | 0.0`입니다.
문서 열두 건은 한 건도 앞자리에 오지 않았습니다.
채움 행의 거리가 문서보다 작기 때문입니다.

## 10. 색인 경로로 읽게 하기

이 절은 색인이 후보를 고르는 순서를 보려고 색인 경로로 읽게 합니다.
02절에서 쓴 설정 `enable_seqscan`을 off로 두면 계획기가 순차 스캔을 고르지 못합니다."""),
        code(SET_SEQSCAN),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 설정을 바꾸고 색인 설정 두 개와 계획 줄을 봅니다.
설정 `hnsw.max_scan_tuples`는 반복 탐색이 볼 수 있는 줄 수 한도입니다."""),
        code(PLAN_CHECK),
        md("""**결과 읽기** — `enable_seqscan 설정: off`이고 `후보 목록 크기: 40`입니다.
`반복 탐색이 볼 줄 수 한도: 20000`도 보입니다. 두 값은 모두 기본값입니다.
계획 줄이 `Index Scan using ch12_core_filter_idx`로 바뀌었습니다.
이제 범주 조건을 붙인 검색이 색인 경로로 읽습니다.

## 11. 받아야 하는 답 — 정확 검색

색인 경로의 결과를 견줄 답이 필요합니다.
01절 정확 검색을 범주 하나에만 적용해 파이썬으로 순위를 냅니다.
문서가 열두 건뿐이라 모두 재도 값이 금방 나옵니다."""),
        code(RANK_IN_CATEGORY),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
튜플을 목록에 담아 `sorted()`로 정렬하고 `pair[1]`로 문서 ID를 꺼냅니다. 01절과 같은 모양입니다.

다음 셀은 첫 질문과 범주 `library`로 정확 검색 상위 세 개를 냅니다."""),
        code(EXACT_TOP),
        md("""**결과 읽기** — `걸 범주: library`이고 라벨 줄 아래 세 줄은 `1 | LIB-004 | 0.43`, `2 | LIB-001 | 0.56`, `3 | LIB-003 | 0.62`입니다.
01·02절 상위 세 개와 문서 ID·순서·거리 값이 모두 같습니다.
이 질문에서는 범주 `library` 밖 문서가 앞 세 자리에 없었기 때문입니다.
이 세 줄이 색인 경로가 받아 오기를 바라는 답입니다.

## 12. 질문 여덟 개를 잴 함수 준비

질문 하나로는 두 경로의 차이를 말할 수 없습니다.
Ch 11과 01·02절에서 쓴 지표 함수 네 개를 그대로 이어 씁니다."""),
        code(UNIQUE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

정답 자리는 고유 문서 목록에서 정답 문서가 몇 번째인지 센 값입니다."""),
        code(GOLD_RANK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

재현율은 자르는 자리까지 자른 목록에 정답 문서가 들어온 비율입니다."""),
        code(RECALL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

질문마다 낸 점수를 같은 무게로 평균하는 함수입니다."""),
        code(MEAN),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 범주 조건을 붙인 검색을 실행하는 함수입니다.
02절 `run_search()`와 모양이 같고 범주 이름을 하나 더 받습니다."""),
        code(RUN_FILTERED),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 반복 탐색 설정을 바꾸는 함수입니다.
설정 `hnsw.iterative_scan`은 값이 `off`·`strict_order`·`relaxed_order` 세 가지입니다."""),
        code(SET_ITERATIVE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
02절 `set_seqscan()`과 같은 모양이고 바꾸는 설정 이름만 다릅니다.

다음 셀은 반복 탐색을 기본값 off로 두고 시작합니다."""),
        code(ITERATIVE_OFF),
        md("""**결과 읽기** — `반복 탐색 설정: off`가 보입니다. 이 값이 pgvector 기본값입니다.
14절에서 이 값을 바꿔 같은 검색을 다시 실행합니다.

다음 셀은 질문 하나를 한 경로로 검색해 앞 세 자리를 내는 함수입니다."""),
        code(PICK_HITS),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
경로 이름이 `정확 검색`이면 파이썬으로, 아니면 데이터베이스로 검색합니다.

다음 셀은 그 결과로 기록 한 줄을 만드는 함수입니다.
받아 온 줄 수를 칸으로 둔 점이 02절 기록과 다릅니다."""),
        code(SCORE_ONE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

## 13. 두 경로의 재현율 견주기

질문 여덟 개를 두 경로로 모두 잽니다.
질문 벡터를 이미 만들어 두었으므로 임베딩 요청이 늘지 않습니다."""),
        code(SCORE_ALL),
        md("""**결과 읽기** — `담은 기록 줄 수: 16`이 보입니다. 질문 여덟 개에 경로 두 가지를 곱한 수입니다.

다음 셀은 담은 줄을 표로 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 앞 여덟 줄이 정확 검색이고 받아 온 줄 수가 모두 `3`입니다.
뒤 여덟 줄은 색인 경로이고 받아 온 줄 수가 `0` 또는 `1`입니다.
질문 `C05`·`C06`·`C08`만 한 줄을 받았고 그 한 줄이 정답 문서였습니다.
질문 `C02`는 두 경로 모두 정답 자리가 `0`입니다.

질문 `C02`의 정답 문서 `LIB-002`는 범주 안 넷 가운데 넷째라 앞 세 자리에 들어오지 않았습니다.
다음 셀은 자르는 자리마다 질문 평균 재현율을 견줍니다."""),
        code(MEANS),
        md("""**결과 읽기** — 라벨 줄 아래 여섯 줄이 나옵니다.
정확 검색은 자리 1에서 `0.75`, 자리 2와 자리 3에서 `0.875`입니다.
색인 경로는 세 자리 모두 `0.375`입니다.
받아 온 줄이 없으면 자르는 자리를 늘려도 재현율이 오르지 않습니다."""),

        md("""## 14. 반복 탐색을 끈 채로 검색하기

Before 셀은 「조건에 맞는 문서가 네 건 있으니 세 줄은 받을 것」이라고 보는 자리입니다.
첫 질문에 범주 `library` 조건을 붙여 한 번 더 검색합니다.
표에 조건을 통과하는 행이 네 개 있는 것은 7절에서 확인했습니다.""", lesson_part="before"),
        code(BEFORE_SHOW, lesson_part="before"),
        md("""**결과 읽기** — `반복 탐색 설정: off`이고 `받아 올 줄 수: 3`, `걸 범주: library`입니다.
세 값은 13절 색인 경로를 잴 때와 같습니다.

다음 셀은 이 설정으로 첫 질문을 검색합니다.""", lesson_part="before"),
        code(BEFORE_RUN, lesson_part="before"),
        md("""**결과 읽기** — `받아 온 줄 수: 0`이고 라벨 줄 아래에 결과 줄이 한 줄도 없습니다.
조건을 통과하는 문서가 네 건 있는데도 한 줄도 받지 못했습니다.
색인이 먼저 고른 후보 40개가 모두 채움 행이었고, 그 뒤에 범주 조건을 검사했기 때문입니다.
받아 온 줄 수가 0이라고 조건에 맞는 문서가 없다고 볼 수 없습니다.""", lesson_part="before"),

        md("""## 15. 설정 하나만 바꿔 다시 실행하기

바꿀 것은 설정 `hnsw.iterative_scan` 하나입니다. off에서 `strict_order`로 바꿉니다.
이 값은 필요한 줄을 얻거나 볼 줄 수 한도에 이를 때까지 색인을 더 살펴보게 합니다.
값 `strict_order`는 받아 온 줄을 거리 순서대로 냅니다.

자료·질문·조건·받아 올 줄 수·후보 목록 크기는 그대로 둡니다.
실행 전에 예상해 봅니다. 세 줄을 받고 그 세 줄이 정확 검색 상위 세 개와 같을 것입니다.""", lesson_part="after"),
        code(AFTER_RUN, lesson_part="after"),
        md("""**결과 읽기** — `반복 탐색 설정: strict_order`이고 `받아 온 줄 수: 3`입니다.
라벨 줄 아래 세 줄은 `1 | LIB-004 | 0.43`, `2 | LIB-001 | 0.56`, `3 | LIB-003 | 0.62`입니다.
11절 정확 검색 상위 세 개와 문서 ID·순서·거리 값이 모두 같습니다. `assert`도 통과했습니다.
받지 못한 까닭이 자료가 아니라 후보를 고르는 폭이었다는 뜻입니다.

## 16. 값 바꿔 보기 — relaxed_order

바꿀 값은 반복 탐색 설정 하나입니다. `strict_order`에서 `relaxed_order`로 바꿉니다.
값 `relaxed_order`는 거리 순서가 조금 달라질 수 있는 대신 줄을 더 받을 수 있습니다.
실행 전에 예상해 봅니다. 받아 온 줄 수는 세 줄일 것이고 순서는 알 수 없습니다.""", lesson_part="after"),
        code(RELAXED_RUN, lesson_part="after"),
        md("""**결과 읽기** — `반복 탐색 설정: relaxed_order`이고 `받아 온 줄 수: 3`입니다.
라벨 줄 아래 세 줄은 `1 | LIB-004 | 0.43`, `2 | LIB-001 | 0.56`, `3 | LIB-003 | 0.62`입니다.
이번 실행에서는 `strict_order`와 순서까지 같았습니다.
조건에 맞는 문서가 네 건뿐이라 두 값의 차이가 드러나지 않았습니다.
큰 자료에서 두 값을 견주는 일은 이번에 실행하지 않았습니다.

다음 셀은 바꾼 설정 두 개를 기본값으로 되돌리고 연결을 닫습니다.""", lesson_part="after"),
        code(CLOSE, lesson_part="after"),
        md("""**결과 읽기** — `반복 탐색 설정: off`와 `enable_seqscan 설정: on`이 보입니다.
마지막 줄 `연결 닫힘: True`는 연결이 닫혔다는 뜻입니다.

검색에 쓴 표 `ch12_core_filter`는 지우지 않고 그대로 남깁니다.

## 정리

1. 범주 조건을 붙인 색인 경로 검색이 첫 질문에서 `0`줄을 냈습니다. 조건을 통과하는 문서는 네 건 있었습니다.
2. 질문 여덟 개 질문 평균 재현율은 정확 검색 자리 1에서 `0.75`인데 색인 경로는 세 자리 모두 `0.375`였습니다.
3. 설정 `hnsw.iterative_scan`만 `strict_order`로 바꾸니 세 줄을 받고 정확 검색 상위 세 개와 같았습니다.

04절에서는 벡터 거리가 아니라 한국어 낱말로 문서를 찾습니다.
형태소 분석기로 낱말을 가르고 낱말이 겹치는 정도로 순위를 냅니다.""", lesson_part="after"),
    ]


if __name__ == "__main__":
    path = write_notebook(LAB, "03", "03-메타데이터-필터와-iterative-scan", "paired", cells())
    print("wrote", path)
