"""Ch 12 13절(챕터 끝 실습 절) 노트북 생성기 (QUALITY-UPGRADE.md §2·§3·§6·§7-2).

사용: python3 author_13.py  → labs/part3/ch12-retrieval-tuning/notebooks/13-검색-품질-실습.ipynb 를 새로 쓴다(출력 없음).
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
새 절이라 수정 전 원본은 없다. 설명만 고칠 때는 mdpatch.py → run_section.sh --no-exec.

주제: 개발 앞 두 문항에서 06절 가중치 하나만 바꿔 보고 자리 다섯 개와 답이 함께 달라지는 것을 본다.
05절 순위 둘 + 06절 합치기 + 08절 보고 자리와 두 지표 + 12절 답 쓰기를 한 줄기로 잇는다.
실행 1: 가중치 [1.0, 1.0](06절 기본) → 두 질문 모두 문서 청크 정밀도 자리 5가 1.0.
실행 2: 가중치 [1.0, 0.0](뜻 검색만, 바꾸는 값 하나) → Q002가 0.4로 내려가고 답이 「자료에 없다」로 바뀐다.

## 요청 수 — 다섯 번 (규격 §7-2 「모델 호출 3~5번」)

임베딩 3번(문서 청크 1 + 질문 2) + 답을 쓰는 모델 2번(실행마다 한 번). 12절은 임베딩 31번·모델 1번이었다.
질문을 개발 앞 두 문항으로 줄여 30분 안에 끝나게 했다(handoff `## §12 → 실습`: 질문 두세 개면 넉넉함).
두 실행은 5절에서 만들어 둔 같은 순위 목록을 다시 쓰므로 실행이 두 번이어도 임베딩 요청이 늘지 않는다.
리랭커는 부르지 않는다(07·08절 모델을 올리면 메모리 3.8GB와 30분 수업 시간에 맞지 않음).
01~03절 pgvector도 쓰지 않는다(Docker가 필요해 준비물이 커짐, handoff 권고).

## 건드리지 않는 파일 (handoff `## §12 → 실습`)

**이 노트북은 파일을 쓰지 않는다**(Ch 9 07·Ch 10 09·Ch 11 07 실습 절 선례). 그래서 12절이 남긴
`runs/advanced-continuity-experiment-log.jsonl`(9b447a41…)·`advanced-continuity-test-result.json`(f9b16717…)·
`advanced-continuity-integrated-result.json`(ce76d3d8…)과 사본 폴더의 바이트가 그대로다.
(§2-7 리팩터(2026-09-21)에서 12절을 다시 실행해 세 파일은 지금 f16aa358…·7b9b9db7…·7b142cd5…이고, 13절은 그때도 파일을 쓰지 않았다.)
`data/advanced-*.json`·`pyproject.toml`·`uv.lock`도 읽기만 한다. Ch 9·10·11 기록과 Ch 6~8 사슬은 열지 않는다.
실습 폴더 `tests/test_continuity.py`가 보는 08·10·12절 노트북 이름(`eligible_items`·`mmr`·`evaluate_config` 등)도
이 절이 건드리지 않는다. 이 노트북은 그 이름 가운데 어느 것도 다시 정의하지 않는다.

## 01~12절에서 그대로 이어 쓴 것 (새 API·새 문법 0개)

§2-7 리팩터(2026-09-21, 작업자 B): 앞 절·Ch 11 함수 여덟 개는 도구 파일 `notebooks/rag_tools.py` 에서 가져온다.
`kiwi_terms(kiwi, text, keep_tags)`(04절), `fuse_rank(…, rank_constant)`(06절), 문서 청크 판
`rank_chunks_by_distance`·`rank_chunks_by_bm25`·`unique_chunk_ids`, `parent_ids_of(…, parent_by_chunk)`(07절),
`recall_at`(Ch 11 02절), `chunk_precision_at(…, parent_by_chunk)`(08절).
리팩터 전에는 준비 셀 여덟 개에 함수 열세 개(01절 거리 넷·05절 순위 둘·06절 합치기 둘 포함)를 다시 적었다.
값도 같다: `keep_tags` 아홉 개 · `rank_constant` 60 · `candidate_count` 8 ·
`recall_place` 3 · `report_place` 5 · 넣을 자리 수 3(12절 `context_count`).
이 절에서 처음 만드는 함수는 다섯 개다: `print_rows`·`column_mean`(기록 장치),
`context_of`(모델에 넣을 글), `score_row`(조립), `run_weights`(설정 한 벌을 두 질문에 적용).

## 결론을 넓히지 않은 자리

질문이 두 개뿐이고 둘 다 난이도 `easy`에 정답 부모가 `E01` 하나다. 12절 열다섯 문항 값과 나란히 놓지 않는다.
부모 문서 재현율 자리 3은 네 줄이 모두 `1.0`이라 이 조건에서는 두 실행을 가르지 못한다(07~12절과 같은 천장).
모델 답은 실행마다 달라질 수 있어 `assert`를 걸지 않고 그림 라벨에도 넣지 않는다.
어느 가중치가 낫다고 판정하지 않는다.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import KEY, RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part3/ch12-retrieval-tuning/notebooks"

INSTALL = install_source([
    "langchain==1.4.0", "langchain-openai==1.6.1", "python-dotenv==1.2.3",
    "kiwipiepy==0.23.2", "rank-bm25==0.2.2", "numpy==2.5.3",
])

IMPORTS = r'''# 자료 읽기·경로 확인과 이 절에서 쓸 검색 도구를 불러옵니다
import json
import os

from kiwipiepy import Kiwi
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from rank_bm25 import BM25Okapi
# 04·06·07·08절과 Ch 11 함수, 문서 청크 판 순위 함수 여덟 개를 도구 파일에서 가져옵니다
from rag_tools import chunk_precision_at, fuse_rank, kiwi_terms, parent_ids_of
from rag_tools import rank_chunks_by_bm25, rank_chunks_by_distance, recall_at, unique_chunk_ids

print("불러온 이름:", "json", "os", "Kiwi", "init_chat_model", "OpenAIEmbeddings", "BM25Okapi")'''

FIND_ROOT = r'''# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part3/ch12-retrieval-tuning/data"):
        root_path = candidate
        break
print("고른 경로:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

LOAD_DATA = r'''# 07~12절과 같은 파일 두 벌을 읽습니다
data_path = root_path + "/labs/part3/ch12-retrieval-tuning/data"
with open(data_path + "/advanced-documents.json", encoding="utf-8") as file:
    documents = json.loads(file.read())
with open(data_path + "/advanced-queries.json", encoding="utf-8") as file:
    queries = json.loads(file.read())
parents = documents["parents"]
chunks = documents["chunks"]
print("부모 문서 수:", len(parents))
print("문서 청크 수:", len(chunks))
print("질문 수:", len(queries))'''

VALUES = r'''# 01~12절에서 쓴 값을 그대로 다시 정하고 이번에 바꿔 볼 가중치 두 벌을 적습니다
keep_tags = ["NNG", "NNP", "NNB", "NR", "VV", "VA", "MAG", "SN", "SL"]
rank_constant = 60
candidate_count = 8
recall_place = 3
report_place = 5
context_count = 3
question_take = 2
equal_weights = [1.0, 1.0]
dense_only_weights = [1.0, 0.0]
print("순위 상수:", rank_constant, "| 후보 수:", candidate_count, "| 보고 자리:", report_place)
print("재현율을 재는 자리:", recall_place, "| 모델에 넣을 자리 수:", context_count)
print("실행 1 가중치:", equal_weights, "| 실행 2 가중치:", dense_only_weights)'''

CHUNK_TEXTS = r'''# 문서 청크마다 제목과 본문을 이어 붙여 글 하나로 만듭니다(07~12절과 같은 코드)
chunk_texts = []
chunk_ids = []
for chunk in chunks:
    chunk_text = chunk["title"] + " " + chunk["text"]
    chunk_texts.append(chunk_text)
    chunk_ids.append(chunk["chunk_id"])
all_chunk_count = len(chunk_ids)
print("이어 붙인 글 수:", len(chunk_texts))
print("첫 문서 청크 ID:", chunk_ids[0])'''

CHUNK_MAPS = r'''# 문서 청크 ID로 부모 문서 ID와 쪽 번호와 본문을 바로 찾게 짝을 만듭니다(12절과 같은 코드)
parent_by_chunk = {}
page_by_chunk = {}
text_by_chunk = {}
for i in range(len(chunks)):
    chunk_id = chunk_ids[i]
    parent_by_chunk[chunk_id] = chunks[i]["parent_id"]
    page_by_chunk[chunk_id] = chunks[i]["page"]
    text_by_chunk[chunk_id] = chunk_texts[i]
print("짝지은 문서 청크 수:", len(parent_by_chunk))
print("첫 문서 청크의 부모 문서 ID:", parent_by_chunk[chunk_ids[0]])
print("첫 문서 청크의 쪽 번호:", page_by_chunk[chunk_ids[0]])'''

EMBEDDINGS = r'''# 01~12절과 같은 모델로 문서 청크를 벡터로 바꿉니다(임베딩 요청 1번)
embedding_model_name = "text-embedding-3-small"
vector_dimensions = 256
embedding_model = OpenAIEmbeddings(model=embedding_model_name, dimensions=vector_dimensions)
chunk_vectors = embedding_model.embed_documents(chunk_texts)
print("임베딩 모델 이름:", embedding_model.model)
print("벡터의 숫자 개수 설정:", embedding_model.dimensions)
print("문서 청크 벡터 수:", len(chunk_vectors))'''

BM25_MODEL = r'''# 04~12절과 같은 형태소 분석기로 문서 청크마다 검색 낱말 목록을 만들고 BM25 모델을 만듭니다
kiwi = Kiwi()
kiwi_corpus = []
for text_value in chunk_texts:
    kiwi_corpus.append(kiwi_terms(kiwi, text_value, keep_tags))
bm25_model = BM25Okapi(kiwi_corpus)
print("검색 낱말 목록 수:", len(kiwi_corpus))
print("BM25 모델이 본 문서 청크 수:", bm25_model.corpus_size)
print("문서 청크 하나의 평균 검색 낱말 수:", round(bm25_model.avgdl, 2))'''

PICK_QUESTIONS = r'''# 개발 묶음에서 앞 두 문항만 골라 질문 글과 정답 부모 문서 ID를 짝지어 둡니다
dev_queries = []
for query in queries:
    if query["split"] == "dev":
        dev_queries.append(query)
practice_items = dev_queries[:question_take]
question_ids = []
gold_by_qid = {}
question_by_qid = {}
for item in practice_items:
    question_ids.append(item["qid"])
    gold_by_qid[item["qid"]] = item["gold_doc_ids"]
    question_by_qid[item["qid"]] = item["question"]
print("개발 질문 수:", len(dev_queries), "| 이번에 쓸 질문 수:", len(question_ids))
print("고른 질문 ID:", question_ids)'''

PREPARE_Q = r'''# 고른 질문마다 벡터와 순위 목록 두 개를 미리 만듭니다(임베딩 요청 2번)
lists_by_qid = {}
for question_id in question_ids:
    question = question_by_qid[question_id]
    question_vector = embedding_model.embed_query(question)
    distance_hits = rank_chunks_by_distance(question_vector, chunk_vectors, chunk_ids, all_chunk_count)
    question_terms = kiwi_terms(kiwi, question, keep_tags)
    score_hits = rank_chunks_by_bm25(bm25_model, question_terms, chunk_ids, all_chunk_count)
    lists_by_qid[question_id] = [unique_chunk_ids(distance_hits), unique_chunk_ids(score_hits)]
first_id = question_ids[0]
print("질문 하나의 순위 목록 수:", len(lists_by_qid[first_id]))
print("순위 목록 하나의 문서 청크 수:", len(lists_by_qid[first_id][0]))
print("거리 순위 1위 문서 청크:", lists_by_qid[first_id][0][0])
print("낱말 순위 1위 문서 청크:", lists_by_qid[first_id][1][0])'''

PRINT_ROWS = r'''# 질문별 줄을 라벨 줄 아래에 한 줄씩 적고 지표 칸의 질문 평균을 냅니다
def print_rows(rows):
    print("질문 | 부모 문서 차례 | 재현율 자리 3 | 문서 청크 정밀도 자리 5")
    for row in rows:
        print(row["질문"], "|", row["부모 문서 차례"], "|", row["재현율 자리 3"], "|", row["문서 청크 정밀도 자리 5"])


def column_mean(rows, name):
    total = 0.0
    for row in rows:
        total = total + row[name]
    return round(total / len(rows), 2)'''

CONTEXT_FUNC = r'''# 고른 문서 청크의 앞자리 본문과 출처 표시를 이어 붙여 모델에 넣을 글을 만듭니다(12절과 같은 모양)
def context_of(picked_ids):
    context_ids = picked_ids[:context_count]
    context_text = ""
    for chunk_id in context_ids:
        source_label = "[" + parent_by_chunk[chunk_id] + " p." + str(page_by_chunk[chunk_id]) + "]"
        context_text = context_text + source_label + "\n" + text_by_chunk[chunk_id] + "\n\n"
    return context_text'''

SCORE_ROW = r'''# 질문 하나를 가중치대로 검색해 고른 자리와 지표 두 개를 한 줄로 만듭니다
def score_row(question_id, weight_list):
    # 06절: 순위 목록 두 개를 가중치로 합쳐 앞자리 여덟 개를 후보로 자릅니다
    fused_ids = fuse_rank(lists_by_qid[question_id], weight_list, rank_constant)
    found_ids = fused_ids[:candidate_count]
    # 08절: 후보 앞에서 보고 자리 다섯 개만 남깁니다
    picked_ids = found_ids[:report_place]
    # 07절: 고른 문서 청크를 부모 문서 차례로 바꿉니다
    parent_ids = parent_ids_of(picked_ids, parent_by_chunk)
    gold_ids = gold_by_qid[question_id]
    row = {"질문": question_id, "고른 문서 청크": picked_ids, "부모 문서 차례": parent_ids}
    # Ch 11 02절 재현율과 08절 문서 청크 정밀도
    row["재현율 자리 3"] = recall_at(parent_ids, gold_ids, recall_place)
    row["문서 청크 정밀도 자리 5"] = chunk_precision_at(picked_ids, gold_ids, report_place, parent_by_chunk)
    return row'''

RUN_WEIGHTS = r'''# 가중치 한 벌을 고른 질문 모두에 적용해 줄 목록을 냅니다
def run_weights(weight_list):
    rows = []
    for question_id in question_ids:
        rows.append(score_row(question_id, weight_list))
    return rows'''

RUN_ONE = r'''# 실행 1: 06절 기본 가중치로 두 질문을 재고 표로 봅니다
run1_rows = run_weights(equal_weights)
print_rows(run1_rows)
print("실행 1 재현율 자리 3 평균:", column_mean(run1_rows, "재현율 자리 3"))
print("실행 1 문서 청크 정밀도 자리 5 평균:", column_mean(run1_rows, "문서 청크 정밀도 자리 5"))
print("실행 1이 Q002에서 고른 문서 청크:", run1_rows[1]["고른 문서 청크"])'''

ANSWER_HEAD = r'''# 두 실행에서 똑같이 쓸 부탁 글과 답을 쓸 질문을 정합니다
prompt_head = "아래 자료만 보고 질문에 한국어로 답하세요.\n"
prompt_head = prompt_head + "답 끝에 [문서ID p.쪽] 모양으로 출처를 적으세요.\n\n"
answer_qid = question_ids[1]
answer_question = question_by_qid[answer_qid]
print("답을 쓸 질문:", answer_qid, "|", answer_question)
print("그 질문의 정답 부모 문서 ID:", gold_by_qid[answer_qid])'''

RUN_ONE_ANSWER = r'''# 실행 1이 고른 앞 세 자리 본문으로 답을 씁니다(모델 요청 1번)
run1_context = context_of(run1_rows[1]["고른 문서 청크"])
run1_prompt = prompt_head + "질문: " + answer_question + "\n\n자료:\n" + run1_context
run1_answer = model.invoke(run1_prompt)
run1_text = run1_answer.text.strip()
print("넣은 글의 길이:", len(run1_context))
print("실행 1의 답:", run1_text)'''

RUN_TWO = r'''# 실행 2: 가중치만 [1.0, 0.0]으로 바꿔 같은 순위 목록을 다시 씁니다
run2_rows = run_weights(dense_only_weights)
print_rows(run2_rows)
print("실행 2 재현율 자리 3 평균:", column_mean(run2_rows, "재현율 자리 3"))
print("실행 2 문서 청크 정밀도 자리 5 평균:", column_mean(run2_rows, "문서 청크 정밀도 자리 5"))
print("실행 2가 Q002에서 고른 문서 청크:", run2_rows[1]["고른 문서 청크"])'''

RUN_TWO_ANSWER = r'''# 실행 2가 고른 앞 세 자리 본문으로 같은 질문에 답을 씁니다(모델 요청 1번)
run2_context = context_of(run2_rows[1]["고른 문서 청크"])
run2_prompt = prompt_head + "질문: " + answer_question + "\n\n자료:\n" + run2_context
run2_answer = model.invoke(run2_prompt)
run2_text = run2_answer.text.strip()
print("넣은 글의 길이:", len(run2_context))
print("실행 2의 답:", run2_text)'''

COMPARE = r'''# 두 실행의 질문 평균을 한 표로 모아 나란히 봅니다
compare_rows = [["실행 1", equal_weights, run1_rows], ["실행 2", dense_only_weights, run2_rows]]
print("실행 | 가중치 | 재현율 자리 3 평균 | 문서 청크 정밀도 자리 5 평균")
for entry in compare_rows:
    recall_mean = column_mean(entry[2], "재현율 자리 3")
    chunk_mean = column_mean(entry[2], "문서 청크 정밀도 자리 5")
    print(entry[0], "|", entry[1], "|", recall_mean, "|", chunk_mean)'''

TITLE = """# 검색 품질 실습: 가중치 하나를 바꿔 답까지 보기

**이 노트북에서 할 일**

1. 05절 순위 두 개를 06절 가중치로 합쳐 개발 질문 두 개의 보고 자리를 만듭니다.
2. 08절 두 지표를 재고 앞 세 자리 본문으로 답을 씁니다.
3. 가중치 하나만 바꿔 다시 실행하고 두 결과를 나란히 견줍니다.

**준비물** — 프로젝트 맨 위 폴더의 `.env`에 `OPENAI_API_KEY`가 있어야 합니다.
서비스 요청은 모두 다섯 번입니다.
임베딩은 문서 청크 한 번과 질문 두 번이고 답을 쓰는 모델은 실행마다 한 번씩입니다.
예상 비용은 다섯 번을 합쳐 미화 0.01달러 아래입니다.
실행 시간은 패키지 설치를 빼면 1분 안팎입니다.

두 실행은 5절에서 만들어 둔 같은 순위 목록을 다시 씁니다.
그래서 실행이 두 번이어도 임베딩 요청은 늘지 않습니다.

**데이터** — 읽는 파일은 07~12절과 같고 둘 다 실습 묶음에 들어 있습니다.

- 문서 `labs/part3/ch12-retrieval-tuning/data/advanced-documents.json`(부모 6건·문서 청크 175개)
- 질문 `labs/part3/ch12-retrieval-tuning/data/advanced-queries.json`(30개)

**이 노트북은 파일을 쓰지 않습니다** — 12절이 `runs` 폴더에 남긴 기록 세 개는 읽지도 고치지도 않습니다.
이번 결과는 화면에만 냅니다.
파일로 남기는 방법은 12절 6절과 9절에서 보았습니다.

**강의와 실습 범위** — 이 절은 이 챕터의 실습입니다.
강사와 함께 첫 셀부터 차례로 실행하고 따로 내는 과제는 없습니다.
함수를 만드는 셀은 네 개이고 모두 이 절에서 처음 만드는 함수입니다.
01~12절 함수는 도구 파일에서 가져옵니다.
7~9절의 표와 답 두 개를 함께 읽습니다.

**기준 버전** — 첫 셀에서 여섯 패키지를 고정한 판으로 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

실습 폴더 `labs/part3/ch12-retrieval-tuning`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""

FIGURE_ALT = ("위에서 아래로 내려가는 흐름도로 맨 위 초록 상자 문서 청크 175개와 초록 상자 개발 앞 두 문항이 "
              "파란 상자 순위 목록 둘 거리와 낱말로 모이고 파란 상자 가중치로 합쳐 후보 여덟 개와 "
              "파란 상자 보고 자리 다섯 개를 지나 왼쪽 노란 상자 지표 두 칸과 오른쪽 보라 상자 답 쓰기 한 번으로 "
              "갈라진 뒤 맨 아래 노란 상자 실행 1 가중치 같게와 노란 상자 실행 2 뜻 검색만으로 내려가는 그림")

FIGURE_READ = """위에서 아래로 읽습니다. 맨 위 초록 상자는 노트북 3·5절에서 만드는 재료입니다.

파란 상자 네 개는 05~08절에서 배운 검색 단계이고 이 노트북은 그 함수를 도구 파일에서 가져옵니다.
그 가운데 「바꿀 값」 상자가 이번 실습에서 손대는 자리입니다.
맨 아래 왼쪽 노란 상자는 지표 두 칸이고 오른쪽 보라 상자는 답을 쓰는 모델입니다."""


def new_funcs(source: str) -> dict:
    """이 절에서 새로 만드는 함수 둘을 한 셀에 담습니다."""
    return code(source, upgrade_allow=["multiple_defs_in_cell"])


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIGURE_ALT + "](attachment:13-1-조립도.png)\n\n" + FIGURE_READ, html="skip"),
        md("""## 1. 준비

첫 셀은 패키지 여섯 개를 설치하고 설치된 버전을 출력합니다.
11·12절과 같은 여섯 개입니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 `langchain: 1.4.0`과 `rank-bm25: 0.2.2`가 보입니다.
마지막 줄 `numpy: 2.5.3`은 도구 파일이 벡터 계산에 쓰는 패키지입니다. 여섯 줄이 모두 보이면 다음 셀로 넘어갑니다.

다음 셀은 이 절에서 쓸 이름 여섯 개를 불러옵니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.

이 노트북은 04·06·07·08절 함수 네 개와 Ch 11 `recall_at()`을 가져옵니다.
04절 `kiwi_terms()`, 06절 `fuse_rank()`, 07절 `parent_ids_of()`, 08절 `chunk_precision_at()`입니다.
07~12절과 같은 문서 청크 판 순위 함수 세 개도 함께 가져옵니다.
인자 모양은 4절에서 정리합니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄은 `불러온 이름:` 뒤에 이름 여섯 개가 붙은 한 줄입니다.
12절이 쓰던 `hashlib`과 `time`은 부르지 않습니다.
이 절은 지문을 만들지 않고 파일도 쓰지 않기 때문입니다.
도구 파일에서 가져온 함수 여덟 개는 출력하지 않습니다."""),
    ] + key_and_model_cells(
        "openai:gpt-5.4-mini",
        "temperature 값을 0으로 두어 매번 비슷한 문장을 고르게 합니다.\n"
        "설정 `reasoning_effort=\"none\"`은 답을 쓰기 전에 따로 생각하는 단계를 두지 않게 합니다.",
    ) + [
        md("""다음 셀은 프로젝트 맨 위 폴더를 찾습니다. 01~12절과 같은 코드입니다."""),
        setup(FIND_ROOT),
        md("""**결과 읽기** — 출력 줄은 `고른 경로: .`입니다. 확인 줄도 통과했습니다.

다음 셀은 07~12절과 같은 자료 두 벌을 읽습니다."""),
        setup(LOAD_DATA),
        md("""**결과 읽기** — `부모 문서 수: 6`과 `문서 청크 수: 175`, `질문 수: 30`이 보입니다.
07~12절과 같은 파일이라 세 값도 같습니다.

## 2. 실습 주제 — 가중치 하나를 바꿔 답까지 보기

작은 안내 창구의 검색기를 손보는 일을 맡았다고 봅니다.
06절에서 뜻 검색 순위와 낱말 검색 순위를 가중치로 합쳤고, 08절에서 보고 자리를 다섯으로 정했습니다.
12절에서는 그 보고 자리의 본문을 모델에 넣어 답을 한 번 썼습니다.

이번 실습은 그 단계를 한 줄기로 잇고 **가중치 한 자리만** 바꿉니다.
실행 1은 두 검색에 같은 몫을 주고, 실행 2는 낱말 검색 쪽 몫을 0으로 내립니다.
바뀌는 값은 그 하나뿐이고 질문·문서·후보 수·보고 자리·모델은 모두 같게 둡니다.

## 3. 재료 만들기 — 값과 문서 청크 벡터

먼저 01~12절에서 쓴 값을 그대로 다시 정합니다."""),
        code(VALUES),
        md("""**결과 읽기** — 줄 `순위 상수: 60 | 후보 수: 8 | 보고 자리: 5`는 06~12절과 같은 값입니다.
줄 `실행 1 가중치: [1.0, 1.0] | 실행 2 가중치: [1.0, 0.0]`이 이번에 바꿀 자리입니다.
앞 숫자가 뜻 검색 몫이고 뒤 숫자가 낱말 검색 몫입니다.

다음 셀은 문서 청크마다 제목과 본문을 이어 붙입니다."""),
        code(CHUNK_TEXTS),
        md("""**결과 읽기** — `이어 붙인 글 수: 175`가 보입니다.
줄 `첫 문서 청크 ID: E01-P01-C01`의 이름 앞머리가 그 문서 청크의 부모 문서 ID입니다.

다음 셀은 문서 청크 ID로 부모와 쪽과 본문을 바로 찾을 수 있게 짝을 만듭니다."""),
        code(CHUNK_MAPS),
        md("""**결과 읽기** — `짝지은 문서 청크 수: 175`가 보입니다.
줄 `첫 문서 청크의 부모 문서 ID: E01`과 `첫 문서 청크의 쪽 번호: 1`은 출처 표시에 쓸 값입니다.

다음 셀은 문서 청크를 벡터로 바꿉니다. 01~12절과 같은 모델과 같은 차원 수입니다."""),
        code(EMBEDDINGS),
        md("""**결과 읽기** — `벡터의 숫자 개수 설정: 256`과 `문서 청크 벡터 수: 175`가 보입니다.
여기까지 임베딩 요청은 한 번입니다.

## 4. 앞 절 함수의 인자 확인하기

앞 절 함수는 준비 셀에서 도구 파일로부터 가져왔습니다.
두 순위는 07~12절과 같은 문서 청크 판 `rank_chunks_by_distance()`와 `rank_chunks_by_bm25()`가 만듭니다.
06절 `fuse_rank()`는 순위 상수를 셋째 인자로 받습니다.
07절 `parent_ids_of()`와 08절 `chunk_precision_at()`은 짝 사전 `parent_by_chunk`를 인자로 받습니다.

리랭커와 MMR은 이 실습에서 쓰지 않아 가져오지 않았습니다.
보고 자리 다섯 개는 합친 순위의 앞자리를 그대로 씁니다.

## 5. 검색 재료 마무리 — BM25 모델과 질문 두 개

다음 셀은 문서 청크의 검색 낱말 목록으로 BM25 모델을 만듭니다.
분석기를 만드는 줄 `kiwi = Kiwi()`는 1초 안팎 걸립니다."""),
        code(BM25_MODEL),
        md("""**결과 읽기** — `검색 낱말 목록 수: 175`와 `BM25 모델이 본 문서 청크 수: 175`가 보입니다.
줄 `문서 청크 하나의 평균 검색 낱말 수: 44.01`은 07~12절과 같은 값입니다.

다음 셀은 개발 묶음에서 앞 두 문항만 고릅니다.
Ch 11이 정한 약속대로 시험 15문항은 이 절에서도 열지 않습니다.
질문을 둘로 줄인 까닭은 요청을 다섯 번 안으로 두기 위해서입니다."""),
        code(PICK_QUESTIONS),
        md("""**결과 읽기** — `개발 질문 수: 15 | 이번에 쓸 질문 수: 2`가 보입니다.
줄 `고른 질문 ID: ['Q001', 'Q002']`가 이번 실습의 질문 두 개입니다.
두 질문은 07~12절에서도 쓰던 개발 묶음 앞자리 문항입니다.

다음 셀은 질문마다 벡터와 순위 목록 두 개를 미리 만듭니다.
가중치가 바뀌어도 이 두 목록은 그대로라 한 번만 만들면 됩니다."""),
        code(PREPARE_Q),
        md("""**결과 읽기** — `질문 하나의 순위 목록 수: 2`와 `순위 목록 하나의 문서 청크 수: 175`가 보입니다.
두 줄 아래 `거리 순위 1위 문서 청크: E01-P02-C04`와 `낱말 순위 1위 문서 청크: E01-P02-C04`는 첫 질문 값입니다.
첫 질문에서는 두 순위의 1위가 같았습니다.
여기까지 임베딩 요청은 세 번입니다.

## 6. 결과를 볼 기록 장치

실행마다 무엇을 볼지 먼저 정합니다.
질문별로 부모 문서 차례와 지표 두 칸을 한 줄씩 적고, 그 아래에 질문 평균을 냅니다."""),
        new_funcs(PRINT_ROWS),
        md("""정의 셀이라 출력이 없습니다.
첫 함수는 라벨 줄을 먼저 내고 질문마다 한 줄씩 적습니다.
둘째 함수는 줄 목록에서 지표 칸만 모아 질문 평균을 소수 둘째 자리까지 냅니다.

다음 셀은 고른 문서 청크를 모델에 넣을 글로 바꾸는 함수입니다.
출처 표시는 Ch 8과 12절에서 쓴 `[문서ID p.쪽]` 모양 그대로입니다."""),
        code(CONTEXT_FUNC),
        md("""정의 셀이라 출력이 없습니다.
앞 세 자리만 넣습니다. 보고 자리는 다섯이지만 수업 시간에 눈으로 읽을 만큼만 넣습니다.
자리마다 출처 표시 한 줄과 본문 한 줄을 붙이고 빈 줄로 나눕니다.

## 7. 조립 — 배운 단계를 한 함수로 잇기

다음 셀이 이 실습의 조립 함수입니다.
주석에 어느 절에서 배운 단계인지 적었습니다."""),
        code(SCORE_ROW),
        md("""정의 셀이라 출력이 없습니다.
차례는 네 단계입니다. 순위 합치기, 후보 자르기, 보고 자리 남기기, 지표 두 칸 재기입니다.
07~12절에서 하나씩 배운 단계를 한 줄씩 이어 붙인 것입니다.

다음 셀은 가중치 한 벌을 질문 두 개 모두에 적용합니다."""),
        code(RUN_WEIGHTS),
        md("""정의 셀이라 출력이 없습니다.
받는 값은 가중치 목록 하나뿐입니다. 질문 묶음과 나머지 설정은 바깥에 정해 둔 값을 씁니다.
그래서 두 실행이 가중치 말고는 같은 조건이 됩니다.

## 8. 실행 1 — 두 검색에 같은 몫

첫 실행은 06절 기본 가중치입니다. 뜻 검색과 낱말 검색에 같은 몫을 줍니다.

실행 전에 예상합니다. 두 질문 모두 정답 부모가 `E01` 하나라 부모 문서 차례가 짧을 것입니다."""),
        code(RUN_ONE),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄이 나옵니다.
줄 `Q001 | ['E01'] | 1.0 | 1.0`과 `Q002 | ['E01'] | 1.0 | 1.0`입니다.
두 질문 모두 보고 자리 다섯 개가 전부 정답 부모의 문서 청크였습니다.

평균 두 줄도 `1.0`입니다.
맨 아래 줄 `실행 1이 Q002에서 고른 문서 청크:` 뒤 다섯 개가 모두 `E01`로 시작합니다.

다음 셀은 두 실행에서 똑같이 쓸 부탁 글과 답을 쓸 질문을 정합니다."""),
        code(ANSWER_HEAD),
        md("""**결과 읽기** — 줄 `답을 쓸 질문: Q002 | 도서는 한 번에 몇 권까지, 며칠 동안 빌릴 수 있나요?`가 보입니다.
줄 `그 질문의 정답 부모 문서 ID: ['E01']`도 함께 나옵니다.
부탁 글은 「넣은 자료만 보고 답하고 끝에 출처를 적으라」는 두 문장입니다.

다음 셀이 실행 1의 답을 씁니다. 이 챕터에서 답을 쓰는 모델을 부르는 자리입니다."""),
        code(RUN_ONE_ANSWER),
        md("""**결과 읽기** — 줄 `넣은 글의 길이: 432`는 모델에 넣은 글의 글자 수입니다.
줄 `실행 1의 답:` 뒤에 한 문장과 출처 표시가 나옵니다.
답에 적힌 출처가 넣은 자리 안에 있는지 눈으로 확인합니다.
모델이 쓴 문장은 실행마다 달라질 수 있어 낱말을 확인 줄로 보지 않았습니다.

## 9. 실행 2 — 낱말 검색 몫을 0으로

이제 값 하나만 바꿉니다. 가중치를 `[1.0, 0.0]`으로 두어 뜻 검색 순위만 씁니다.
질문 묶음과 문서, 후보 수 8, 보고 자리 5, 모델은 실행 1과 같습니다.

실행 전에 예상합니다. 낱말이 그대로 겹치던 문서 청크가 앞에서 밀려나 정밀도가 내려갈 것입니다."""),
        code(RUN_TWO),
        md("""**결과 읽기** — 라벨 줄 아래 첫 줄 `Q001 | ['E01'] | 1.0 | 1.0`은 실행 1과 같습니다.
둘째 줄은 `Q002 | ['E01', 'E02'] | 1.0 | 0.4`로 바뀌었습니다.
질문 `Q002`의 보고 자리 다섯 가운데 세 자리가 다른 부모 문서 `E02`의 문서 청크입니다.

줄 `실행 2 문서 청크 정밀도 자리 5 평균: 0.7`이 실행 1보다 낮습니다.
재현율 자리 3 평균은 두 실행 모두 `1.0`입니다.

다음 셀이 실행 2가 고른 자리로 같은 질문에 답을 씁니다."""),
        code(RUN_TWO_ANSWER),
        md("""**결과 읽기** — 줄 `넣은 글의 길이: 302`는 실행 1보다 짧습니다.
줄 `실행 2의 답:` 뒤 문장은 자료에서 권수와 기간을 찾지 못했다는 내용입니다.
넣은 세 자리 가운데 대출 권수와 기간이 적힌 자리가 없었기 때문입니다.
답 끝에는 출처 표시가 그대로 붙어 있습니다. 이 한 번만 본 모습입니다.

## 10. 두 실행 비교

마지막으로 두 실행의 질문 평균을 한 표로 모읍니다.

실행 전에 예상합니다. 재현율은 같고 문서 청크 정밀도만 갈릴 것입니다."""),
        code(COMPARE),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄이 나옵니다.
위 줄은 `실행 1 | [1.0, 1.0] | 1.0 | 1.0`이고 아래 줄은 `실행 2 | [1.0, 0.0] | 1.0 | 0.7`입니다.
가중치 한 자리를 바꾸자 문서 청크 정밀도 평균만 내려갔습니다.

재현율 자리 3은 두 줄이 모두 `1.0`이라 이 조건에서는 두 실행을 가르지 못합니다.
07~12절에서 본 천장이 질문 두 개에서도 그대로였습니다.

## 정리

1. 순위 합치기와 보고 자리와 지표와 답 쓰기를 한 함수 줄기로 이었습니다.
2. 가중치 한 자리만 바꾸자 `Q002`의 보고 자리 다섯 가운데 세 자리가 다른 부모 문서로 바뀌었습니다.
3. 넣은 자료가 달라지자 같은 질문에 대한 답도 달라졌습니다.

이 절로 Ch 12가 끝납니다. Ch 13에서는 이 챕터가 남긴 통합 기록을 읽어 흐름도로 잇습니다."""),
    ]


if __name__ == "__main__":
    path = write_notebook(LAB, "13", "13-검색-품질-실습", "experiment", cells())
    print("wrote", path)
