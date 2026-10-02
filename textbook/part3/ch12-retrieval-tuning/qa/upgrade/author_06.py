"""Ch 12 06절 품질 개선본 노트북 생성기 (QUALITY-UPGRADE.md §2·§3·§6).

사용: python3 author_06.py  → labs/part3/ch12-retrieval-tuning/notebooks/06-RRF-하이브리드-검색.ipynb 를 새로 쓴다(출력 없음).
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북은 qa/upgrade/before/notebooks/ 에 있다. **experiment 형식 유지**(chapter.json).

## 01~05절에서 그대로 이어 쓴 것 (handoff.md 「§05 → §06」)

- 자료: `core-documents.json`(12개) · `core-queries.json`(8개, `gold_doc_id`·`kind`). 한 글자도 고치지 않는다.
- 경로 후보 `candidates = [".", "../../..", "../../../.."]` + for/break, `nbkit.KEY` 셀.
- §2-7 리팩터(2026-09-21, 작업자 A): 앞 절·Ch 11 함수 일곱 개는 도구 파일 `notebooks/rag_tools.py` 에서 가져온다.
  01절 `rank_by_distance(question_vector, doc_vectors, doc_ids, top_count)`(칸 `거리`),
  04절 `kiwi_terms(kiwi, text, keep_tags)` · `rank_by_bm25(bm25_model, question_terms, doc_ids, top_count)`(칸 `점수`),
  Ch 11 `unique_doc_ids` · `find_gold_rank` · `recall_at` · `mean_score`.
  리팩터 전에는 01절 거리 함수 넷·05절 순위 함수 둘·`kiwi_terms`·Ch 11 함수 넷을 노트북에 다시 적었다.
- 이 절이 처음 가르친 `fuse_scores` · `fuse_rank`(바깥 이름 `rank_constant` 를 읽음)와 `score_one` 은 노트북에 남긴다.
  도구 파일에는 순위 상수를 셋째 인자로 받는 `fuse_scores`·`fuse_rank` 판이 있고 07~13절이 가져갈 몫이다.
- 04·05절 정렬 모양(점수에 음수를 붙여 `sorted`), 기록 한 줄 → 표 → 질문 평균 순서, 자르는 자리 `[1, 2, 3]`.
- 노트북은 numpy 를 직접 쓰지 않는다(도구 파일이 쓴다). `lambda`·내포식·`key=`·`reverse=`·f-string·세미콜론·한 줄 복합문을 쓰지 않는다.

## 이 절이 새로 가르치는 것

- 값을 더하지 않고 **자리 번호만** 써서 두 순위를 하나로 합치기(`weight / (rank_constant + 자리)`).
- 가중치 하나만 올려 같은 두 순위 목록에서 합친 순위가 어떻게 달라지는지 보기.
- 합친 결과를 앞 두 방법과 같은 지표 함수로 재고 결론을 실제 값으로 한정하기.

## 선택한 것과 까닭

1. **세 방법 모두 `top_all = 12`로 잰다.** 05절이 두 방법을 1~12 범위로 맞춰 두었다(handoff 「§05 → §06」
   「후보 수와 자르는 자리를 분명히 두세요」). 개선 전 06은 후보를 여섯 개로 잘라 RRF 쪽 자리 범위가
   달라졌다. 문서 12개를 끝까지 넣으면 세 방법의 `정답 자리`가 모두 1~12라 한 표에 담을 수 있다.
   두 목록에 같은 문서 열두 건이 모두 있으므로 「한쪽 목록에만 있는 문서」 장면은 이번에 나오지 않는다.
2. **합치는 재료는 순위대로 된 문서 ID 목록이다.** `unique_doc_ids(rank_by_distance(...))`가 그 목록을
   낸다(handoff 권고). 거리·점수 값은 합치는 함수에 넘기지 않는다 — 자리 번호만 쓴다는 것이 이 절의 요점.
3. **값 바꿔 보기는 가중치 하나다.** 후보 수·순위 상수·질문·문서를 모두 그대로 두고 낱말 겹침 쪽만
   `1.0` → `1.5`로 올린다(개선 전 06의 값 바꿔 보기와 같은 값). 규격 §4가 이 절을 예로 든 가중치 문장을
   이 챕터 말로 바꿔 7절 결과 읽기와 본문 b6에 적었다.
4. **실행 1은 `C01`이다.** 05절 실행 1과 같은 질문이라 두 순위를 그대로 이어 볼 수 있고, 합친 점수가
   같은 문서 두 건이 나와 「점수가 같은 자리는 결과로 읽지 않는다」(04·05절)를 다시 확인할 수 있다.
5. **파일을 쓰지 않는다.** 개선 전 마지막 두 셀은 `runs/core-06-rrf.json`을 덮어썼다(`Path`·`hashlib`·
   `datetime`·세미콜론·한 줄 복합문). 읽는 쪽은 `check_course_continuity.py` 187~196행 하나이고 바이트만
   본다(Ch 9 07·Ch 10 09·Ch 11 07·Ch 12 01~05절 선례).
6. **`score_one()`이 문서 ID 목록을 바로 받는다.** 05절 판은 순위 목록(딕셔너리 목록)을 받아 함수 안에서
   `unique_doc_ids()`를 불렀다. 06절은 합친 순위가 이미 ID 목록이라 세 방법의 인자 모양을 ID 목록으로
   맞췄다. 인자 이름은 `found_ids`다.
7. **`find_gold_rank()`를 문서 하나의 자리를 찾는 데도 쓴다.** 목록에서 찾는 ID가 몇 번째인지 세는 함수라
   `find_gold_rank(목록, [문서 ID])`로 부르면 그 문서의 자리가 나온다. 셀 하나를 줄이려고 같은 함수를 썼고
   노트북 4절 설명 셀과 본문 b5에 그 사실을 적었다.

## 탐색 실행에서 확인한 값 (2026-09-18, /tmp/ch12-06/probe.py)

같은 코드를 세 번 돌려 모든 출력이 같았다(`out2.txt`·`out3.txt` 동일). 질문 평균 재현율은 벡터 거리
`0.75`·`0.875`·`0.875`(01·05절과 같음), 낱말 겹침 `0.875`·`0.875`·`1.0`(04·05절과 같음), 순위 합치기
`0.75`·`0.875`·`1.0`. 정답 자리는 순위 합치기 `C01` 2 · `C02` 3 · 나머지 1이다. 가중치를 `1.5`로 올리면
`C01`만 2에서 3으로 내려가고 나머지 일곱 질문은 그대로다. `C01`에서 `LIB-001`과 `LIB-003`의 합친 점수가
`0.032`로 같아 문서 ID 차례가 자리를 정했다.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import KEY, RUN_DATE, code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part3/ch12-retrieval-tuning/notebooks"

INSTALL = install_source([
    "langchain-openai==1.6.1", "python-dotenv==1.2.3", "kiwipiepy==0.23.2", "rank-bm25==0.2.2", "numpy==2.5.3",
])

IMPORTS = r'''# 자료 읽기·임베딩·형태소 분석·낱말 점수에 쓸 이름을 불러옵니다
import json

from kiwipiepy import Kiwi
from langchain_openai import OpenAIEmbeddings
from rank_bm25 import BM25Okapi
# 01·04절과 Ch 11 01·02절 함수 일곱 개를 도구 파일에서 가져옵니다
from rag_tools import find_gold_rank, kiwi_terms, mean_score, rank_by_bm25
from rag_tools import rank_by_distance, recall_at, unique_doc_ids

print("불러온 이름:", "json", "Kiwi", "OpenAIEmbeddings", "BM25Okapi")'''

FIND_ROOT = r'''# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part3/ch12-retrieval-tuning/data"):
        root_path = candidate
        break
print("고른 경로:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

LOAD_DATA = r'''# 01~05절과 같은 문서 파일과 질문 파일을 불러옵니다
data_path = root_path + "/labs/part3/ch12-retrieval-tuning/data"
with open(data_path + "/core-documents.json", encoding="utf-8") as file:
    docs = json.loads(file.read())
with open(data_path + "/core-queries.json", encoding="utf-8") as file:
    queries = json.loads(file.read())
print("문서 수:", len(docs))
print("질문 수:", len(queries))'''

VALUES = r'''# 05절에서 쓴 값을 그대로 다시 정하고 견줄 방법 이름을 셋으로 늘립니다
top_three = 3
top_all = 12
cutoff_values = [1, 2, 3]
keep_tags = ["NNG", "NNP", "NNB", "NR", "VV", "VA", "MAG", "SN", "SL"]
method_names = ["벡터 거리", "낱말 겹침", "순위 합치기"]
print("나란히 볼 상위 문서 수:", top_three)
print("자리를 셀 때 재는 문서 수:", top_all)
print("자르는 자리 세 가지:", cutoff_values)
print("남길 품사 표시:", keep_tags)
print("견줄 방법 세 가지:", method_names)'''

FUSE_VALUES = r'''# 자리 번호를 몫으로 바꾸는 식에 쓸 값을 정하고 앞자리 세 곳의 몫을 봅니다
rank_constant = 60
base_weight = 1.0
raised_weight = 1.5
equal_weights = [base_weight, base_weight]
sparse_up_weights = [base_weight, raised_weight]
print("순위 상수:", rank_constant)
print("같은 가중치:", equal_weights)
print("낱말 겹침 쪽만 올린 가중치:", sparse_up_weights)
print("자리 | 기본 가중치가 주는 몫")
for position in range(top_three):
    share = base_weight / (rank_constant + position + 1)
    print(position + 1, "|", round(share, 4))'''

DOC_TEXTS = r'''# 문서 12개의 제목과 본문을 이어 붙이고 문서 ID 목록도 만듭니다(01~05절과 같은 모양)
doc_texts = []
doc_ids = []
for doc in docs:
    doc_texts.append(doc["title"] + " " + doc["text"])
    doc_ids.append(doc["doc_id"])
print("이어 붙인 글 수:", len(doc_texts))
print("첫 문서 글:", doc_texts[0])
print("문서 ID 목록:")
print(doc_ids)'''

EMBEDDINGS = r'''# 01~03절·05절과 같은 모델로 문서 12개와 질문 8개를 벡터로 바꿉니다(임베딩 요청 9번)
embedding_model_name = "text-embedding-3-small"
vector_dimensions = 256
embedding_model = OpenAIEmbeddings(model=embedding_model_name, dimensions=vector_dimensions)
doc_vectors = embedding_model.embed_documents(doc_texts)
query_vectors = []
for query in queries:
    query_vectors.append(embedding_model.embed_query(query["question"]))
print("임베딩 모델 이름:", embedding_model.model)
print("벡터의 숫자 개수 설정:", embedding_model.dimensions)
print("문서 벡터 수:", len(doc_vectors))
print("질문 벡터 수:", len(query_vectors))'''

BM25_MODEL = r'''# 04·05절과 같은 형태소 분석기로 문서 12개의 검색 낱말 목록을 만들고 BM25 모델을 만듭니다
kiwi = Kiwi()
kiwi_corpus = []
for text in doc_texts:
    kiwi_corpus.append(kiwi_terms(kiwi, text, keep_tags))
bm25_model = BM25Okapi(kiwi_corpus)
print("검색 낱말 목록 수:", len(kiwi_corpus))
print("BM25 모델이 본 문서 수:", bm25_model.corpus_size)
print("문서 하나의 평균 검색 낱말 수:", round(bm25_model.avgdl, 2))'''

ID_LISTS = r'''# 질문 여덟 개마다 두 방법의 순위 목록을 문서 ID 차례로 미리 만들어 둡니다
distance_id_lists = []
score_id_lists = []
for query_index in range(len(queries)):
    distance_hits = rank_by_distance(query_vectors[query_index], doc_vectors, doc_ids, top_all)
    question_terms = kiwi_terms(kiwi, queries[query_index]["question"], keep_tags)
    score_hits = rank_by_bm25(bm25_model, question_terms, doc_ids, top_all)
    distance_id_lists.append(unique_doc_ids(distance_hits))
    score_id_lists.append(unique_doc_ids(score_hits))
print("만든 순위 목록 쌍 수:", len(distance_id_lists))
print("목록 하나의 문서 수:", len(distance_id_lists[0]))
print("첫 질문의 벡터 거리 순위 앞 세 개:", distance_id_lists[0][:top_three])
print("첫 질문의 낱말 겹침 순위 앞 세 개:", score_id_lists[0][:top_three])'''

FUSE_SCORES = r'''# 순위 목록 여러 개를 받아 문서마다 자리 몫을 더한 합친 점수를 냅니다
def fuse_scores(ranking_list, weight_list):
    scores = {}
    for list_index in range(len(ranking_list)):
        ranking = ranking_list[list_index]
        weight = weight_list[list_index]
        # 자리 번호는 1부터 세고 앞자리일수록 나누는 수가 작아 몫이 큽니다
        for position in range(len(ranking)):
            doc_id = ranking[position]
            share = weight / (rank_constant + position + 1)
            scores[doc_id] = scores.get(doc_id, 0.0) + share
    return scores'''

FUSE_RANK = r'''# 합친 점수가 큰 순서로 문서 ID 목록을 만듭니다(04·05절과 같은 음수 붙이기)
def fuse_rank(ranking_list, weight_list):
    scores = fuse_scores(ranking_list, weight_list)
    pairs = []
    for doc_id in scores:
        # 점수에 음수를 붙이면 sorted가 큰 점수를 앞으로 보냅니다
        pairs.append((0 - scores[doc_id], doc_id))
    fused_ids = []
    for pair in sorted(pairs):
        fused_ids.append(pair[1])
    return fused_ids'''

RUN_ONE = r'''# 실행 1: 첫 질문의 두 순위 목록을 같은 가중치로 합칩니다
first_query = queries[0]
first_ranking_list = [distance_id_lists[0], score_id_lists[0]]
first_scores = fuse_scores(first_ranking_list, equal_weights)
first_fused_ids = fuse_rank(first_ranking_list, equal_weights)
print("고른 질문:", first_query["qid"], "|", first_query["question"])
print("그 질문의 정답 문서 ID:", first_query["gold_doc_id"])
print("순위 | 문서 ID | 벡터 거리 자리 | 낱말 겹침 자리 | 합친 점수")
for position in range(top_three):
    doc_id = first_fused_ids[position]
    distance_place = find_gold_rank(distance_id_lists[0], [doc_id])
    score_place = find_gold_rank(score_id_lists[0], [doc_id])
    print(position + 1, "|", doc_id, "|", distance_place, "|", score_place, "|", round(first_scores[doc_id], 5))'''

RUN_TWO = r'''# 값 바꿔 보기: 같은 두 순위 목록에서 낱말 겹침 쪽 가중치만 올립니다
second_scores = fuse_scores(first_ranking_list, sparse_up_weights)
second_fused_ids = fuse_rank(first_ranking_list, sparse_up_weights)
print("쓴 가중치:", sparse_up_weights)
print("순위 | 문서 ID | 벡터 거리 자리 | 낱말 겹침 자리 | 합친 점수")
for position in range(top_three):
    doc_id = second_fused_ids[position]
    distance_place = find_gold_rank(distance_id_lists[0], [doc_id])
    score_place = find_gold_rank(score_id_lists[0], [doc_id])
    print(position + 1, "|", doc_id, "|", distance_place, "|", score_place, "|", round(second_scores[doc_id], 5))'''

SCORE_ONE = r'''# 문서 ID 목록 하나를 받아 정답 자리와 자르는 자리별 재현율을 기록 한 줄로 만듭니다
def score_one(query_index, method_name, found_ids):
    query = queries[query_index]
    gold_doc_ids = [query["gold_doc_id"]]
    row = {"방법": method_name, "질문": query["qid"], "갈래": query["kind"]}
    row["정답 자리"] = find_gold_rank(found_ids, gold_doc_ids)
    for cutoff in cutoff_values:
        row["자리 " + str(cutoff)] = recall_at(found_ids, gold_doc_ids, cutoff)
    return row'''

SCORE_ALL = r'''# 질문 여덟 개를 세 방법으로 모두 재어 기록 줄을 담습니다(임베딩 요청은 더 보내지 않습니다)
score_rows = []
for method_name in method_names:
    for query_index in range(len(queries)):
        # 세 방법이 갈리는 곳은 이 조건 세 갈래뿐입니다
        if method_name == method_names[0]:
            found_ids = distance_id_lists[query_index]
        elif method_name == method_names[1]:
            found_ids = score_id_lists[query_index]
        else:
            ranking_list = [distance_id_lists[query_index], score_id_lists[query_index]]
            found_ids = fuse_rank(ranking_list, equal_weights)
        score_rows.append(score_one(query_index, method_name, found_ids))
print("담은 기록 줄 수:", len(score_rows))'''

TABLE = r'''# 방법·질문·갈래·정답 자리·자리 1·자리 3을 라벨 줄 아래에 차례로 출력합니다
print("방법 | 질문 | 갈래 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율")
for row in score_rows:
    print(row["방법"], "|", row["질문"], "|", row["갈래"], "|", row["정답 자리"], "|", row["자리 1"], "|", row["자리 3"])'''

MEANS = r'''# 세 방법의 질문 평균 재현율을 자르는 자리마다 견줍니다
print("방법 | 자르는 자리 | 질문 평균 재현율")
for method_name in method_names:
    picked = []
    for row in score_rows:
        if row["방법"] == method_name:
            picked.append(row)
    for cutoff in cutoff_values:
        picked_scores = []
        for row in picked:
            picked_scores.append(row["자리 " + str(cutoff)])
        print(method_name, "|", cutoff, "|", mean_score(picked_scores))'''

WEIGHT_COMPARE = r'''# 가중치만 올린 합친 순위를 질문 여덟 개에서 다시 재어 정답 자리를 견줍니다
print("질문 | 같은 가중치 자리 | 낱말 겹침 1.5 자리")
for query_index in range(len(queries)):
    ranking_list = [distance_id_lists[query_index], score_id_lists[query_index]]
    equal_ids = fuse_rank(ranking_list, equal_weights)
    raised_ids = fuse_rank(ranking_list, sparse_up_weights)
    gold_doc_ids = [queries[query_index]["gold_doc_id"]]
    equal_place = find_gold_rank(equal_ids, gold_doc_ids)
    raised_place = find_gold_rank(raised_ids, gold_doc_ids)
    print(queries[query_index]["qid"], "|", equal_place, "|", raised_place)'''

TITLE = """# RRF 하이브리드 검색

**이 노트북에서 할 일**

1. 05절과 같은 두 검색 방법의 순위 목록을 다시 만듭니다.
2. 자리 번호만 써서 두 순위를 하나로 합치는 함수를 만듭니다.
3. 가중치 하나만 올려 합친 순위가 어떻게 달라지는지 봅니다.
4. 질문 여덟 개에서 세 방법의 정답 자리와 재현율을 견줍니다.

**준비물** — 프로젝트 폴더의 `.env`에 `OPENAI_API_KEY`가 있어야 합니다.
임베딩 요청은 문서 1번과 질문 8번으로 모두 아홉 번입니다.
예상 비용은 미화 0.01달러 아래이고 답을 쓰는 모델은 부르지 않습니다.
실행 시간은 1분 안팎이고 첫 셀의 설치가 가장 오래 걸립니다.

**데이터** — 두 파일 모두 실습 묶음에 들어 있습니다.

- 문서 `labs/part3/ch12-retrieval-tuning/data/core-documents.json`(12개)
- 질문 `labs/part3/ch12-retrieval-tuning/data/core-queries.json`(8개)

**강의와 실습 범위** — 강의 시간에는 2절과 5~7절, 9절을 읽습니다.
합치는 식을 정하고 함수 두 개를 만드는 자리가 5절입니다.
6~7절은 실행 1과 값 바꿔 보기이고 9절은 세 방법 비교입니다.
1·3·4·8절은 함께 실행하고 실습 시간에 다시 읽습니다.

**기준 버전** — 첫 셀에서 다섯 패키지를 고정한 판으로 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

실습 폴더 `labs/part3/ch12-retrieval-tuning`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""

FIGURE_ALT = ("위에서 아래로 내려가는 흐름도로 맨 위 초록 상자 질문 C01 정답 LIB-001에서 두 갈래로 갈려 "
              "왼쪽 갈래는 노란 상자 벡터 거리 순위 LIB-004 LIB-001 LIB-003으로 이어지고 오른쪽 갈래는 "
              "노란 상자 낱말 겹침 순위 LIB-004 LIB-003 LIB-001로 이어진 뒤 두 순위가 파란 상자 자리마다 "
              "몫 내기로 모이고 파란 상자 문서마다 몫 더하기를 지나 맨 아래 노란 상자 합친 순위 LIB-004 "
              "LIB-001 LIB-003으로 끝나는 그림")

FIGURE_READ = """맨 위 초록 상자가 이 절에서 자세히 볼 질문과 그 정답 문서입니다.
거기서 두 갈래로 갈리고 왼쪽이 벡터 거리, 오른쪽이 낱말 겹침입니다.
두 갈래의 노란 상자는 05절에서 만든 순위입니다.
가운데 파란 상자 두 개가 이 절에서 새로 만드는 처리입니다.
맨 아래 노란 상자가 합친 순위이고 이 노트북 6절의 출력입니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIGURE_ALT + "](attachment:06-1-두-순위를-자리로-합치기.png)\n\n" + FIGURE_READ, html="skip"),
        md("""## 1. 준비

첫 셀은 패키지 다섯 개를 설치하고 설치된 버전을 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 `langchain-openai: 1.6.1`과 `rank-bm25: 0.2.2`가 보입니다.
다섯 줄이 모두 보이면 다음 셀로 넘어갑니다.
05절과 같은 다섯 패키지입니다.

다음 셀은 이 절에서 쓸 이름 네 개를 불러옵니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.

이 노트북은 01·04절 함수 세 개와 Ch 11 지표 함수 네 개를 가져옵니다.
01절 `rank_by_distance()`, 04절 `kiwi_terms()`·`rank_by_bm25()`입니다.
Ch 11 함수는 `unique_doc_ids()`·`find_gold_rank()`·`recall_at()`·`mean_score()`입니다.
인자 모양은 05절에서 쓴 것과 같습니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄은 `불러온 이름:` 뒤에 이름 네 개가 붙은 한 줄입니다.
이름 `OpenAIEmbeddings`는 글을 벡터로 바꾸는 도구입니다.
이름 `Kiwi`와 `BM25Okapi`는 낱말 겹침 쪽에서 쓰는 두 도구입니다.
도구 파일에서 가져온 함수 일곱 개는 출력하지 않습니다.

다음 셀은 API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다."""),
        setup(KEY),
        md("""**결과 읽기** — 출력 줄은 `OPENAI_API_KEY 설정 여부: True` 하나입니다.
키 값은 출력하지 않습니다.

다음 셀은 프로젝트 맨 위 폴더를 찾습니다. 01~05절과 같은 코드입니다."""),
        setup(FIND_ROOT),
        md("""**결과 읽기** — 출력 줄은 `고른 경로: .`입니다. `assert`도 통과했습니다.

다음 셀은 01~05절이 쓴 문서 파일과 질문 파일을 그대로 읽습니다."""),
        setup(LOAD_DATA),
        md("""**결과 읽기** — `문서 수: 12`와 `질문 수: 8`이 보입니다.
01~05절과 같은 교육용 자료입니다.
같은 자료를 써야 05절에서 만든 두 순위를 그대로 합칠 수 있습니다.

## 2. 이 절에서 쓸 값 정하기

05절에서 쓴 값 다섯 개를 그대로 다시 정합니다.
이름 `top_all`은 자리를 셀 때 재는 문서 수입니다.
이름 `method_names`에 담을 방법이 05절 둘에서 셋으로 늘었습니다."""),
        code(VALUES),
        md("""**결과 읽기** — `자리를 셀 때 재는 문서 수: 12`가 보입니다.
출력 줄 `자르는 자리 세 가지: [1, 2, 3]`은 01~05절과 같은 값입니다.
줄 `견줄 방법 세 가지: ['벡터 거리', '낱말 겹침', '순위 합치기']`의 세 이름으로 기록을 나눕니다.
라벨 줄 `남길 품사 표시:` 뒤에는 이름 아홉 개가 있습니다.

다음 셀은 자리 번호를 몫으로 바꾸는 식에 쓸 값을 정합니다.
앞자리일수록 큰 몫을 주려고 자리 번호를 나누는 수에 넣습니다.
식은 `가중치 / (순위 상수 + 자리)`입니다."""),
        code(FUSE_VALUES),
        md("""**결과 읽기** — 라벨 줄 아래 세 줄이 자리 1·2·3의 몫입니다.
자리 1은 `1 | 0.0164`이고 자리 3은 `3 | 0.0159`입니다.
자리가 하나 뒤로 갈 때마다 몫이 조금씩 줄어듭니다.
줄 `순위 상수: 60`의 60은 앞자리 사이의 차이를 줄이려고 더하는 수입니다.
출력 줄 `낱말 겹침 쪽만 올린 가중치: [1.0, 1.5]`는 7절에서 쓸 값입니다.

## 3. 두 방법이 볼 재료 만들기

두 방법은 같은 글에서 서로 다른 재료를 만듭니다.
먼저 문서 12개의 제목과 본문을 이어 붙여 글 열두 개로 만듭니다."""),
        code(DOC_TEXTS),
        md("""**결과 읽기** — `이어 붙인 글 수: 12`가 보입니다.
출력 줄 `첫 문서 글:` 뒤에는 제목 `도서 대출 기간`과 본문이 이어져 있습니다.
라벨 줄 `문서 ID 목록:` 아래 줄에 `LIB-001`부터 열두 개가 있습니다.

다음 셀은 벡터 거리 쪽 재료를 만듭니다.
01~03절·05절과 같은 모델과 같은 숫자 개수를 씁니다."""),
        code(EMBEDDINGS),
        md("""**결과 읽기** — `벡터의 숫자 개수 설정: 256`과 `문서 벡터 수: 12`가 보입니다.
출력 줄 `질문 벡터 수: 8`까지 나오면 임베딩 요청 아홉 번이 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.

다음 셀은 낱말 겹침 쪽 재료를 만듭니다.
검색 낱말은 05절처럼 도구 파일의 `kiwi_terms()`에 분석기와 남길 품사 표시를 넘겨 만듭니다.
분석기를 만드는 줄 `kiwi = Kiwi()`는 1초 안팎 걸립니다."""),
        code(BM25_MODEL),
        md("""**결과 읽기** — `검색 낱말 목록 수: 12`와 `BM25 모델이 본 문서 수: 12`가 보입니다.
출력 줄 `문서 하나의 평균 검색 낱말 수: 15.33`은 04·05절과 같은 값입니다.

## 4. 두 방법의 순위 목록 만들기

두 방법의 순위는 05절처럼 도구 파일의 `rank_by_distance()`와 `rank_by_bm25()`로 만듭니다.
값 칸 이름은 `거리`와 `점수`로 뜻이 반대입니다.
두 순위 목록에서 문서 ID만 차례로 모으는 일은 `unique_doc_ids()`가 맡습니다.
합치는 함수에 넣을 재료가 바로 이 문서 ID 목록입니다.

다음 셀은 질문 여덟 개마다 두 방법의 순위 목록을 미리 만듭니다.
문서 12개를 끝까지 재므로 목록 하나에 문서 ID가 열두 개 들어갑니다."""),
        code(ID_LISTS),
        md("""**결과 읽기** — `만든 순위 목록 쌍 수: 8`과 `목록 하나의 문서 수: 12`가 보입니다.
줄 `첫 질문의 벡터 거리 순위 앞 세 개: ['LIB-004', 'LIB-001', 'LIB-003']`은 05절 실행 1과 같습니다.
낱말 겹침 쪽은 `['LIB-004', 'LIB-003', 'LIB-001']`로 둘째와 셋째가 서로 바뀌어 있습니다.

## 5. 자리 번호로 합치는 함수 만들기

두 목록에는 값이 아니라 문서 ID만 들어 있습니다.
합치는 함수는 그 목록에서 자리 번호만 보고 몫을 냅니다.
그래서 거리와 점수의 크기가 달라도 두 결과를 함께 쓸 수 있습니다."""),
        code(FUSE_SCORES),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
인자 `ranking_list`에 순위 목록 두 개를 담아 넘깁니다.
줄 `scores.get(doc_id, 0.0) + share`는 아직 없는 문서 ID의 몫을 0에서 시작합니다.

다음 셀은 합친 점수가 큰 순서로 문서 ID 목록을 만듭니다.
점수는 클수록 앞이라 04·05절처럼 점수에 음수를 붙여 정렬합니다."""),
        code(FUSE_RANK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
합친 점수가 같은 문서가 있으면 문서 ID 차례가 자리를 정합니다.

## 6. 실행 1 — 두 순위를 같은 가중치로 합치기

첫 질문의 두 순위 목록을 같은 가중치로 합칩니다.
합친 순위 앞자리 문서가 두 순위에서 몇 번째였는지는 `find_gold_rank()`로 찾습니다.
목록에서 찾는 ID가 몇 번째인지 세는 함수라 정답 문서가 아닌 문서에도 쓸 수 있습니다.
실행 전에 예상해 봅니다.
두 방법이 모두 자리 1에 둔 `LIB-004`가 합친 순위에서도 1위일 것입니다."""),
        code(RUN_ONE),
        md("""**결과 읽기** — 라벨 줄 아래 첫 줄은 `1 | LIB-004 | 1 | 1 | 0.03279`입니다.
그 문서는 두 방법에서 모두 자리 1이라 가장 큰 몫을 두 번 받았습니다.
둘째 줄 `2 | LIB-001 | 2 | 3 | 0.032`와 셋째 줄 `3 | LIB-003 | 3 | 2 | 0.032`는 합친 점수가 같습니다.
두 문서의 자리 번호가 2와 3으로 서로 바뀐 짝이라 몫의 합이 같아졌습니다.

정답 문서 `LIB-001`의 자리는 2입니다.
합친 점수가 같을 때 자리를 정하는 것은 이 코드의 정렬 규칙입니다.
04절에서 본 대로 점수가 같은 자리는 결과로 읽지 않습니다.

## 7. 값 바꿔 보기 — 가중치 하나만 올리기

바꿀 값은 낱말 겹침 쪽 가중치 하나입니다.
문서와 질문, 순위 상수, 두 순위 목록은 그대로 둡니다.
실행 전에 예상해 봅니다. 낱말 겹침이 앞에 둔 문서가 위로 올라올 것입니다."""),
        code(RUN_TWO),
        md("""**결과 읽기** — 출력 줄 `쓴 가중치: [1.0, 1.5]` 아래 표에서 둘째와 셋째가 서로 바뀌었습니다.
둘째 줄은 `2 | LIB-003 | 3 | 2 | 0.04007`이고 셋째 줄은 `3 | LIB-001 | 2 | 3 | 0.03994`입니다.
정답 문서 `LIB-001`의 자리가 2에서 3으로 내려갔습니다.

낱말 겹침 쪽 몫이 한 배 반이 되면서 같았던 두 점수가 갈렸습니다.
낱말 겹침 순위에서 앞자리였던 `LIB-003`이 위로 올라갔습니다.
가중치를 올려도 BM25 점수 자체는 바뀌지 않습니다.
합친 점수에서 낱말 겹침 순위가 차지하는 몫만 커집니다.

## 8. 질문 여덟 개를 잴 함수 준비

질문 하나로는 세 방법의 차이를 말할 수 없습니다.
재현율과 질문 평균은 준비 셀에서 가져온 Ch 11 함수 `recall_at()`과 `mean_score()`로 냅니다.

다음 셀은 문서 ID 목록 하나를 받아 기록 한 줄을 만듭니다.
값 칸을 두지 않아 세 방법을 한 표에 담을 수 있습니다."""),
        code(SCORE_ONE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
인자 `found_ids`를 밖에서 받으므로 이 함수는 어느 방법인지 보지 않습니다.

## 9. 세 방법의 재현율 견주기

질문 여덟 개를 세 방법으로 모두 잽니다.
순위 목록을 미리 만들어 두었으므로 요청은 더 보내지 않습니다."""),
        code(SCORE_ALL),
        md("""**결과 읽기** — `담은 기록 줄 수: 24`가 보입니다.
질문 여덟 개에 방법 세 가지를 곱한 수입니다.

다음 셀은 담은 줄을 표로 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 앞 여덟 줄이 벡터 거리이고 그다음 여덟 줄이 낱말 겹침입니다.
마지막 여덟 줄이 순위 합치기이고 그 가운데 `순위 합치기 | C02 | semantic | 3 | 0.0 | 1.0` 줄이 있습니다.
같은 질문에서 벡터 거리는 `벡터 거리 | C02 | semantic | 7 | 0.0 | 0.0`이고 낱말 겹침은 자리 1입니다.
합친 자리 3은 두 방법의 자리 7과 1 사이입니다.

앞 열여섯 줄은 05절 표와 같은 값입니다.
세 방법 모두 문서 12개를 끝까지 재어 자리가 1에서 12까지 나옵니다.

다음 셀은 자르는 자리마다 질문 평균 재현율을 견줍니다."""),
        code(MEANS),
        md("""**결과 읽기** — 라벨 줄 아래 아홉 줄이 나옵니다.
벡터 거리는 `벡터 거리 | 1 | 0.75`이고 낱말 겹침은 `낱말 겹침 | 1 | 0.875`입니다.
순위 합치기는 `순위 합치기 | 1 | 0.75`로 벡터 거리와 같습니다.
자리 3에서는 `순위 합치기 | 3 | 1.0`으로 낱말 겹침과 같습니다.
세 방법의 자리 2 값은 모두 `0.875`입니다.

합친 값이 두 방법보다 높은 자리는 세 자리 가운데 없었습니다.
합쳤다고 해서 좋아지지는 않았습니다.

다음 셀은 가중치만 올린 합친 순위의 정답 자리를 견줍니다."""),
        code(WEIGHT_COMPARE),
        md("""**결과 읽기** — 라벨 줄 아래 여덟 줄 가운데 값이 다른 줄은 `C01 | 2 | 3` 하나입니다.
질문 `C02`는 `C02 | 3 | 3`으로 두 가중치에서 자리가 같습니다.
나머지 여섯 질문은 두 가중치 모두 자리 1입니다.
가중치를 올려 자리가 앞으로 온 질문은 이번 실행에 없었습니다.

## 정리

1. 자리 번호만 써서 두 순위를 하나로 합치는 함수를 만들었습니다.
2. 질문 `C01`에서 합친 순위의 정답 자리는 2였고 가중치를 올리니 3이 되었습니다.
3. 이번 실행에서 합친 값이 두 방법보다 높은 자리는 없었습니다.

07절에서는 후보 목록을 고정해 두고 질문과 후보 본문을 함께 읽어 순서를 다시 정합니다.
그 절부터 쓰는 문서와 질문 묶음이 바뀝니다."""),
    ]


if __name__ == "__main__":
    path = write_notebook(LAB, "06", "06-RRF-하이브리드-검색", "experiment", cells())
    print("wrote", path)
