"""Ch 12 05절 품질 개선본 노트북 생성기 (QUALITY-UPGRADE.md §2·§3·§6).

사용: python3 author_05.py  → labs/part3/ch12-retrieval-tuning/notebooks/05-dense와-sparse-비교.ipynb 를 새로 쓴다(출력 없음).
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북은 qa/upgrade/before/notebooks/ 에 있다. **experiment 형식 유지**(chapter.json).

## 01~04절에서 그대로 이어 쓴 것 (handoff.md 「§04 → §05」)

- 자료: `core-documents.json`(12개) · `core-queries.json`(8개, `gold_doc_id`·`kind`). 한 글자도 고치지 않는다.
- 경로 후보 `candidates = [".", "../../..", "../../../.."]` + for/break, `nbkit.KEY` 셀(04절은 없었다).
- §2-7 리팩터(2026-09-21, 작업자 A): 앞 절·Ch 11 함수 여덟 개는 도구 파일 `notebooks/rag_tools.py` 에서 가져온다.
  01절 `rank_by_distance(question_vector, doc_vectors, doc_ids, top_count)`(NumPy `np.argsort`, 거리는 `cosine_distance`),
  04절 `kiwi_terms(kiwi, text, keep_tags)` · `count_docs_with(corpus, term)` ·
  `rank_by_bm25(bm25_model, question_terms, doc_ids, top_count)`, Ch 11 `unique_doc_ids` · `find_gold_rank` · `recall_at` · `mean_score`.
  리팩터 전에는 01절 거리 함수 넷(Ch 9 03절 반복문 판 포함)·순위 함수 둘(05절 판: 바깥 이름 `doc_ids`·`doc_vectors`·
  `bm25_model` 을 읽음)·`kiwi_terms`·Ch 11 함수 넷을 노트북에 다시 적었다. 4절 「벡터 거리로 순위 만들기」는 코드 셀 없는
  설명 소절로 남겨 절 번호를 지켰다(뒤 절·Ch 13·Ch 14가 「05절 N절」을 인용한다).
- 이 절이 처음 가르친 `print_ranked(hit_list, value_name)` 과 `score_one` 은 노트북에 남긴다.
- `BM25Okapi(목록의 목록)`, 점수에 음수를 붙여 `sorted` 는 04절과 같다(도구 파일 `rank_by_bm25` 안).
- 기록 한 줄 → 표 → 질문 평균 순서(01~04절과 같은 모양). 자르는 자리 `[1, 2, 3]`.
- 노트북은 numpy 를 직접 쓰지 않는다(도구 파일이 쓴다). `lambda`·내포식·`key=`·`reverse=`·f-string 안 계산·세미콜론·한 줄 복합문을 쓰지 않는다.

## 이 절이 새로 가르치는 것

- 같은 자료·같은 자르는 자리·같은 지표 함수로 두 검색 방법을 나란히 놓기.
- 거리(작을수록 가까움)와 점수(클수록 관련 있음)의 방향이 반대인 것을 한 노트북에서 가르기.
- 두 방법의 정답 자리가 다른 질문을 찾아 검색 낱말로 확인하기.

## 선택한 것과 까닭

1. **두 방법 모두 문서 12개를 끝까지 재고 정답 자리를 1~12로 센다.** 03·04절 기록은 상위 3개만 담아
   자리가 0~3이었다(handoff 「§04 → §05」 「정답 자리 칸 범위 차이」). 두 방법을 한 표에 담으려면 범위가
   같아야 하고, 그렇게 재면 벡터 거리 쪽 자리가 01절 표와, 낱말 겹침 쪽 자리가 04절 표와 그대로 맞는다.
   `top_all = 12`로 재고 `top_three = 3`은 나란히 볼 상위 문서 수로만 쓴다.
2. **칸 이름을 `거리`와 `점수`로 가른다.** 한 표에 두 값을 섞지 않으려고 기록 표에서는 값 칸을 빼고
   `방법`·`질문`·`갈래`·`정답 자리`·자르는 자리 세 칸만 둔다. 상위 3개 출력은 `print_ranked(목록, 칸 이름)`
   하나로 두 칸 이름을 모두 쓴다(02·03절 `print_hits`와 04절 `print_scores`를 합친 모양).
3. **실행 1은 `C01`, 값 바꿔 보기는 `C02`다.** 두 질문에서 이긴 방법이 서로 다르다(탐색 실행에서 확인).
   `C01`은 벡터 거리 쪽 정답 자리가 2이고 낱말 겹침 쪽이 3이다. `C02`는 벡터 거리 쪽이 7이고 낱말
   겹침 쪽이 1이다. 두 질문의 `kind`가 모두 `semantic`이라 「말 바꾼 질문은 벡터 거리가 낫다」로 쓸 수 없다.
4. **`C02`가 갈린 까닭을 낱말로 확인한다.** 질문 낱말과 정답 문서 낱말에 함께 있는 낱말이 `반납` 하나이고
   그 낱말은 문서 12개 가운데 한 건에만 있다. 04절이 가르친 「그 낱말이 있는 문서 수」를 다시 세어 출력으로
   보인다. 벡터 거리 쪽이 왜 7이었는지는 모델 안을 볼 수 없으므로 원인을 적지 않는다.
5. **공백 분리 정책을 다시 싣지 않는다.** 이 절에서 견줄 것은 벡터 거리 검색과 낱말 겹침 검색이다
   (handoff 「§04 → §05」). `bm25_models` 딕셔너리도 빼고 모델 하나만 만든다.
6. **거리는 그림 라벨에 넣지 않는다.** 소수 셋째 자리가 실행마다 흔들린다(01절). 점수는 두 실행에서
   같았으므로(04절) 그림에는 문서 ID와 점수, 정답 자리만 넣는다.
7. **파일을 쓰지 않는다.** 개선 전 마지막 두 셀은 `runs/core-05-dense-sparse.json`을 덮어썼다(`Path`·
   `hashlib`·`datetime`·세미콜론·한 줄 복합문). 읽는 쪽은 `check_course_continuity.py` 187~196행 하나이고
   바이트만 본다(Ch 9 07·Ch 10 09·Ch 11 07·Ch 12 01~04절 선례).
8. **셀 수를 30개로 줄인다.** 03절이 51셀로 커졌다. 형태소 분석기 준비와 `kiwi_terms` 정의를 한 셀에
   두고, 순위를 고르는 `if`를 기록 반복문에 두어 `pick_hits` 셀을 없앴다(`score_one`이 순위 목록을 받는다).

## 탐색 실행에서 확인한 값 (2026-09-18, /tmp/ch12-05/probe.py·probe2.py)

같은 코드를 세 번 돌려 모든 출력이 같았다(`out2.txt`·`out3.txt` 동일). 질문 평균 재현율은 벡터 거리
`0.75`·`0.875`·`0.875`(01절과 같음), 낱말 겹침 `0.875`·`0.875`·`1.0`(04절과 같음). 정답 자리가 다른 질문은
`C01`(2 대 3)과 `C02`(7 대 1) 둘이다. `C01`에서 두 방법의 상위 3개는 같은 문서 세 건이고 순서만 다르다.
`C02`에서 벡터 거리 상위 3개에는 정답 문서가 없다. 함께 있는 낱말은 `반납` 하나이고 문서 한 건에만 있다.
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
# 01·04절과 Ch 11 01·02절 함수 여덟 개를 도구 파일에서 가져옵니다
from rag_tools import count_docs_with, find_gold_rank, kiwi_terms, mean_score
from rag_tools import rank_by_bm25, rank_by_distance, recall_at, unique_doc_ids

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

LOAD_DATA = r'''# 01~04절과 같은 문서 파일과 질문 파일을 불러옵니다
data_path = root_path + "/labs/part3/ch12-retrieval-tuning/data"
with open(data_path + "/core-documents.json", encoding="utf-8") as file:
    docs = json.loads(file.read())
with open(data_path + "/core-queries.json", encoding="utf-8") as file:
    queries = json.loads(file.read())
print("문서 수:", len(docs))
print("질문 수:", len(queries))'''

VALUES = r'''# 이 절에서 되풀이해 쓸 값과 견줄 방법 이름을 정합니다
top_three = 3
top_all = 12
cutoff_values = [1, 2, 3]
keep_tags = ["NNG", "NNP", "NNB", "NR", "VV", "VA", "MAG", "SN", "SL"]
method_names = ["벡터 거리", "낱말 겹침"]
print("나란히 볼 상위 문서 수:", top_three)
print("자리를 셀 때 재는 문서 수:", top_all)
print("자르는 자리 세 가지:", cutoff_values)
print("남길 품사 표시:", keep_tags)
print("견줄 방법 두 가지:", method_names)'''

DOC_TEXTS = r'''# 문서 12개의 제목과 본문을 이어 붙이고 문서 ID 목록도 만듭니다(01~04절과 같은 모양)
doc_texts = []
doc_ids = []
for doc in docs:
    doc_texts.append(doc["title"] + " " + doc["text"])
    doc_ids.append(doc["doc_id"])
print("이어 붙인 글 수:", len(doc_texts))
print("첫 문서 글:", doc_texts[0])
print("문서 ID 목록:")
print(doc_ids)'''

EMBEDDINGS = r'''# 01~03절과 같은 모델로 문서 12개와 질문 8개를 벡터로 바꿉니다(임베딩 요청 9번)
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

BM25_MODEL = r'''# 04절과 같은 형태소 분석기로 문서 12개의 검색 낱말 목록을 만들고 BM25 모델을 만듭니다
kiwi = Kiwi()
kiwi_corpus = []
for text in doc_texts:
    kiwi_corpus.append(kiwi_terms(kiwi, text, keep_tags))
bm25_model = BM25Okapi(kiwi_corpus)
print("검색 낱말 목록 수:", len(kiwi_corpus))
print("BM25 모델이 본 문서 수:", bm25_model.corpus_size)
print("문서 하나의 평균 검색 낱말 수:", round(bm25_model.avgdl, 2))'''

PRINT_RANKED = r'''# 순위 목록을 순위·문서 ID·값 세 칸으로 출력합니다(값 칸 이름을 인자로 받습니다)
def print_ranked(hit_list, value_name):
    print("순위 | 문서 ID |", value_name)
    for rank_number in range(len(hit_list)):
        row = hit_list[rank_number]
        print(rank_number + 1, "|", row["doc_id"], "|", row[value_name])'''

RUN_ONE = r'''# 실행 1: 첫 질문을 두 방법으로 재어 상위 세 문서를 나란히 봅니다
first_query = queries[0]
first_terms = kiwi_terms(kiwi, first_query["question"], keep_tags)
first_distance_hits = rank_by_distance(query_vectors[0], doc_vectors, doc_ids, top_three)
first_score_hits = rank_by_bm25(bm25_model, first_terms, doc_ids, top_three)
print("고른 질문:", first_query["qid"], "|", first_query["question"])
print("그 질문의 정답 문서 ID:", first_query["gold_doc_id"])
print("질문의 갈래:", first_query["kind"])
print("질문의 검색 낱말:", first_terms)
print_ranked(first_distance_hits, "거리")
print_ranked(first_score_hits, "점수")'''

RUN_TWO = r'''# 값 바꿔 보기: 질문 하나만 바꿔 같은 두 방법으로 다시 잽니다
second_query = queries[1]
second_terms = kiwi_terms(kiwi, second_query["question"], keep_tags)
second_distance_hits = rank_by_distance(query_vectors[1], doc_vectors, doc_ids, top_three)
second_score_hits = rank_by_bm25(bm25_model, second_terms, doc_ids, top_three)
print("고른 질문:", second_query["qid"], "|", second_query["question"])
print("그 질문의 정답 문서 ID:", second_query["gold_doc_id"])
print("질문의 갈래:", second_query["kind"])
print("질문의 검색 낱말:", second_terms)
print_ranked(second_distance_hits, "거리")
print_ranked(second_score_hits, "점수")'''

SHARED_TERMS = r'''# 값 바꿔 보기 질문과 그 정답 문서에 함께 있는 검색 낱말을 찾습니다
second_gold_terms = []
for i in range(len(doc_ids)):
    if doc_ids[i] == second_query["gold_doc_id"]:
        second_gold_terms = kiwi_corpus[i]
        break
shared_terms = []
for term in second_terms:
    if term in second_gold_terms:
        shared_terms.append(term)
print("정답 문서의 검색 낱말:", second_gold_terms)
print("질문과 정답 문서에 함께 있는 낱말:", shared_terms)'''

TERM_DOC_COUNT = r'''# 함께 있는 낱말이 문서 12개 가운데 몇 건에 있는지 04절 함수로 셉니다
print("함께 있는 낱말 | 그 낱말이 있는 문서 수")
for term in shared_terms:
    print(term, "|", count_docs_with(kiwi_corpus, term))'''

SCORE_ONE = r'''# 순위 목록 하나를 받아 정답 자리와 자르는 자리별 재현율을 기록 한 줄로 만듭니다
def score_one(query_index, method_name, hit_list):
    query = queries[query_index]
    gold_doc_ids = [query["gold_doc_id"]]
    found_ids = unique_doc_ids(hit_list)
    row = {"방법": method_name, "질문": query["qid"], "갈래": query["kind"]}
    row["정답 자리"] = find_gold_rank(found_ids, gold_doc_ids)
    for cutoff in cutoff_values:
        row["자리 " + str(cutoff)] = recall_at(found_ids, gold_doc_ids, cutoff)
    return row'''

SCORE_ALL = r'''# 질문 여덟 개를 두 방법으로 모두 재어 기록 줄을 담습니다(임베딩 요청은 더 보내지 않습니다)
score_rows = []
for method_name in method_names:
    for query_index in range(len(queries)):
        # 두 방법이 갈리는 곳은 이 조건 하나입니다
        if method_name == method_names[0]:
            hit_list = rank_by_distance(query_vectors[query_index], doc_vectors, doc_ids, top_all)
        else:
            question_terms = kiwi_terms(kiwi, queries[query_index]["question"], keep_tags)
            hit_list = rank_by_bm25(bm25_model, question_terms, doc_ids, top_all)
        score_rows.append(score_one(query_index, method_name, hit_list))
print("담은 기록 줄 수:", len(score_rows))'''

TABLE = r'''# 방법·질문·갈래·정답 자리·자리 1·자리 3을 라벨 줄 아래에 차례로 출력합니다
print("방법 | 질문 | 갈래 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율")
for row in score_rows:
    print(row["방법"], "|", row["질문"], "|", row["갈래"], "|", row["정답 자리"], "|", row["자리 1"], "|", row["자리 3"])'''

MEANS = r'''# 두 방법의 질문 평균 재현율을 자르는 자리마다 견줍니다
print("방법 | 자르는 자리 | 질문 평균 재현율")
for method_name in method_names:
    picked = []
    for row in score_rows:
        if row["방법"] == method_name:
            picked.append(row)
    for cutoff in cutoff_values:
        scores = []
        for row in picked:
            scores.append(row["자리 " + str(cutoff)])
        print(method_name, "|", cutoff, "|", mean_score(scores))'''

DIFF = r'''# 두 방법의 정답 자리가 다른 질문만 골라 라벨 줄 아래에 출력합니다
print("질문 | 벡터 거리 자리 | 낱말 겹침 자리")
for query_index in range(len(queries)):
    qid = queries[query_index]["qid"]
    places = []
    for row in score_rows:
        if row["질문"] == qid:
            places.append(row["정답 자리"])
    if places[0] != places[1]:
        print(qid, "|", places[0], "|", places[1])'''

TITLE = """# dense와 sparse 비교

**이 노트북에서 할 일**

1. 같은 문서 12개와 질문 8개로 두 검색 방법의 재료를 만듭니다.
2. 질문 하나를 두 방법으로 재어 상위 세 문서를 나란히 봅니다.
3. 질문만 바꿔 두 방법의 1위가 어떻게 달라지는지 봅니다.
4. 질문 여덟 개의 정답 자리와 재현율을 한 표에서 견줍니다.

**준비물** — 프로젝트 폴더의 `.env`에 `OPENAI_API_KEY`가 있어야 합니다.
임베딩 요청은 문서 1번과 질문 8번으로 모두 아홉 번입니다.
예상 비용은 미화 0.01달러 아래이고 답을 쓰는 모델은 부르지 않습니다.
실행 시간은 1분 안팎이고 첫 셀의 설치가 가장 오래 걸립니다.

**데이터** — 두 파일 모두 실습 묶음에 들어 있습니다.

- 문서 `labs/part3/ch12-retrieval-tuning/data/core-documents.json`(12개)
- 질문 `labs/part3/ch12-retrieval-tuning/data/core-queries.json`(8개)

**강의와 실습 범위** — 강의 시간에는 3~5절과 6~7절, 9절을 읽습니다.
두 방법의 재료를 만들고 가져온 순위 함수 두 개의 인자를 확인하는 자리입니다.
6~7절은 실행 1과 값 바꿔 보기이고 9절은 질문 여덟 개 비교입니다.
1~2절과 8절은 함께 실행하고 실습 시간에 다시 읽습니다.

**기준 버전** — 첫 셀에서 다섯 패키지를 고정한 판으로 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

실습 폴더 `labs/part3/ch12-retrieval-tuning`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""

FIGURE_ALT = ("위에서 아래로 내려가는 흐름도로 맨 위 초록 상자 문서 12개와 질문 8개에서 두 갈래로 갈려 "
              "왼쪽 갈래는 파란 상자 벡터로 바꿔 코사인 거리 재기에서 노란 상자 거리가 작은 순서로 순위로 "
              "이어지고 오른쪽 갈래는 파란 상자 검색 낱말로 바꿔 BM25 점수 내기에서 노란 상자 점수가 큰 "
              "순서로 순위로 이어진 뒤 두 순위가 파란 상자 같은 지표 함수로 정답 자리와 재현율로 모이고 "
              "맨 아래 노란 상자 질문 평균 재현율 여섯 값으로 끝나는 그림")

FIGURE_READ = """맨 위 초록 상자가 두 방법이 함께 보는 자료입니다.
거기서 두 갈래로 갈리고 파란 상자는 우리가 정한 처리입니다.
두 갈래의 노란 상자는 값의 방향이 서로 반대입니다.
아래에서 두 순위가 같은 지표 함수로 모입니다.
맨 아래 노란 상자가 이 노트북의 마지막 출력입니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIGURE_ALT + "](attachment:05-1-같은-자료-두-갈래-순위.png)\n\n" + FIGURE_READ, html="skip"),
        md("""## 1. 준비

첫 셀은 패키지 다섯 개를 설치하고 설치된 버전을 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 `langchain-openai: 1.6.1`과 `kiwipiepy: 0.23.2`가 보입니다.
마지막 줄 `numpy: 2.5.3`은 도구 파일이 벡터 계산에 쓰는 패키지입니다. 다섯 줄이 모두 보이면 다음 셀로 넘어갑니다.
01~03절은 앞 두 패키지를 썼고 04절은 셋째와 넷째 패키지를 썼습니다.

다음 셀은 이 절에서 쓸 이름 네 개를 불러옵니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.

이 노트북은 01·04절 함수 네 개와 Ch 11 지표 함수 네 개를 가져옵니다.
01절 `rank_by_distance()`, 04절 `kiwi_terms()`·`count_docs_with()`·`rank_by_bm25()`입니다.
Ch 11 함수는 `unique_doc_ids()`·`find_gold_rank()`·`recall_at()`·`mean_score()`입니다.
인자 모양이 앞 절 판과 다른 함수는 쓰는 자리에서 설명합니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄은 `불러온 이름:` 뒤에 이름 네 개가 붙은 한 줄입니다.
이름 `OpenAIEmbeddings`는 글을 벡터로 바꾸는 도구입니다.
이름 `Kiwi`와 `BM25Okapi`는 04절에서 쓴 두 도구입니다.
도구 파일에서 가져온 함수 여덟 개는 출력하지 않습니다.

다음 셀은 API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다."""),
        setup(KEY),
        md("""**결과 읽기** — 출력 줄은 `OPENAI_API_KEY 설정 여부: True` 하나입니다.
키 값은 출력하지 않습니다.
04절은 임베딩을 쓰지 않아 이 셀이 없었습니다.

다음 셀은 프로젝트 맨 위 폴더를 찾습니다. 01~04절과 같은 코드입니다."""),
        setup(FIND_ROOT),
        md("""**결과 읽기** — 출력 줄은 `고른 경로: .`입니다. `assert`도 통과했습니다.

다음 셀은 01~04절이 쓴 문서 파일과 질문 파일을 그대로 읽습니다."""),
        setup(LOAD_DATA),
        md("""**결과 읽기** — `문서 수: 12`와 `질문 수: 8`이 보입니다.
01~04절과 같은 교육용 자료입니다.
같은 자료를 써야 두 방법의 값을 나란히 놓을 수 있습니다.

## 2. 이 절에서 쓸 값 정하기

값 다섯 개를 먼저 정합니다.
이름 `top_all`은 정답 자리를 셀 때 재는 문서 수입니다.
문서 12개를 끝까지 재면 정답 자리가 1에서 12 사이로 나옵니다.
남길 품사 표시 아홉 가지는 04절에서 정한 목록과 같습니다."""),
        code(VALUES),
        md("""**결과 읽기** — `나란히 볼 상위 문서 수: 3`과 `자리를 셀 때 재는 문서 수: 12`가 보입니다.
출력 줄 `자르는 자리 세 가지: [1, 2, 3]`은 01~04절과 같은 값입니다.
`견줄 방법 두 가지: ['벡터 거리', '낱말 겹침']` 줄의 두 이름으로 뒤에서 기록을 나눕니다.
라벨 줄 `남길 품사 표시:` 뒤에는 이름 아홉 개가 있습니다.

## 3. 두 방법이 볼 재료 만들기

두 방법은 같은 글에서 서로 다른 재료를 만듭니다.
먼저 문서 12개의 제목과 본문을 이어 붙여 글 열두 개로 만듭니다.
이 글이 벡터로도 바뀌고 검색 낱말로도 바뀝니다."""),
        code(DOC_TEXTS),
        md("""**결과 읽기** — `이어 붙인 글 수: 12`가 보입니다.
출력 줄 `첫 문서 글:` 뒤에는 제목 `도서 대출 기간`과 본문이 이어져 있습니다.
라벨 줄 `문서 ID 목록:` 아래 줄에 `LIB-001`부터 열두 개가 있습니다.
이 순서가 뒤에서 순위를 만들 때 문서를 가리키는 차례입니다.

다음 셀은 벡터 거리 쪽 재료를 만듭니다.
01~03절과 같은 모델과 같은 숫자 개수를 씁니다."""),
        code(EMBEDDINGS),
        md("""**결과 읽기** — `벡터의 숫자 개수 설정: 256`과 `문서 벡터 수: 12`가 보입니다.
출력 줄 `질문 벡터 수: 8`까지 나오면 임베딩 요청 아홉 번이 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.

다음 셀은 낱말 겹침 쪽 재료를 만듭니다.
검색 낱말은 준비 셀에서 가져온 04절 함수 `kiwi_terms()`로 만듭니다.
도구 파일 판은 04절 판이 바로 읽던 분석기와 남길 품사 표시를 인자로 받습니다.
분석기를 만드는 줄 `kiwi = Kiwi()`는 1초 안팎 걸립니다."""),
        code(BM25_MODEL),
        md("""**결과 읽기** — `검색 낱말 목록 수: 12`와 `BM25 모델이 본 문서 수: 12`가 보입니다.
출력 줄 `문서 하나의 평균 검색 낱말 수: 15.33`은 04절과 같은 값입니다.
같은 글에서 같은 함수로 만든 목록이라 04절 색인과 같습니다.

## 4. 벡터 거리로 순위 만들기

벡터 거리 쪽 순위는 준비 셀에서 가져온 `rank_by_distance()`가 만듭니다.
질문 벡터를 문서 벡터 모두와 01절 코사인 거리로 재고, 거리가 작은 순서로 앞 몇 개를 남깁니다.
인자는 질문 벡터, 문서 벡터 목록, 문서 ID 목록, 남길 개수 네 가지입니다. 값 칸 이름은 `거리`입니다.
03절에서 범주 하나에 쓴 함수와 같은 판입니다.

## 5. 낱말 겹침으로 순위 만들기

낱말 겹침 쪽 순위는 04절 함수 `rank_by_bm25()`를 가져와 만듭니다.
도구 파일 판은 모델 하나와 질문의 검색 낱말 목록, 문서 ID 목록, 남길 개수를 받습니다.
04절 판은 정책 이름과 질문 글을 받아 함수 안에서 검색 낱말을 만들었습니다.
점수는 클수록 관련 있어 점수에 음수를 붙여 `sorted()`로 정렬하는 방법은 04절과 같습니다.

값 칸 이름은 `점수`입니다. 앞 함수의 `거리`와 뜻이 반대라 이름을 갈랐습니다.
다음 셀은 순위 목록을 표 모양으로 출력하는 함수입니다.
값 칸 이름을 인자로 받아 두 방법에 모두 씁니다."""),
        code(PRINT_RANKED),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

## 6. 실행 1 — 같은 질문을 두 방법으로

첫 질문을 두 방법으로 재어 상위 세 문서를 나란히 봅니다.
실행 전에 예상해 봅니다.
질문이 `책을 빌릴 수 있는 기간은 며칠인가요?`이므로 대출 기간 문서가 앞에 올 것입니다."""),
        code(RUN_ONE),
        md("""**결과 읽기** — 라벨 줄 `순위 | 문서 ID | 거리` 아래 첫 줄은 `1 | LIB-004 | 0.43`입니다.
정답 문서 `LIB-001`은 `2 | LIB-001 | 0.56` 줄에 있습니다.
라벨 줄 `순위 | 문서 ID | 점수` 아래 첫 줄은 `1 | LIB-004 | 3.37`이고 정답 문서는 `3 | LIB-001 | 2.01` 줄입니다.
두 방법의 상위 세 문서는 같은 세 건이고 순서만 다릅니다.
정답 문서가 1위인 방법은 없고 자리는 벡터 거리 2와 낱말 겹침 3입니다.

두 방법 모두 1위로 `LIB-004`를 골랐습니다.
그 문서는 전자책 대출 기간을 다루고 정답 문서는 일반 도서 대출 기간을 다룹니다.
출력 줄 `질문의 갈래: semantic`은 질문 파일이 「말을 바꾼 질문」으로 적어 둔 표시입니다.

## 7. 값 바꿔 보기 — 질문 하나만 바꾸기

바꿀 값은 질문 하나입니다.
문서와 재는 방법, 상위 문서 수는 그대로 둡니다.
실행 전에 예상해 봅니다. 두 방법이 같은 문서를 1위로 고를 것입니다."""),
        code(RUN_TWO),
        md("""**결과 읽기** — 예상과 달랐습니다.
라벨 줄 `순위 | 문서 ID | 거리` 아래 세 줄에 정답 문서 `LIB-002`가 없습니다.
첫 줄은 `1 | LIB-003 | 0.56`입니다.
라벨 줄 `순위 | 문서 ID | 점수` 아래 첫 줄은 `1 | LIB-002 | 2.26`으로 정답 문서입니다.
이 질문의 갈래도 `semantic`인데 앞 질문과 이긴 방법이 다릅니다.

다음 셀은 낱말 겹침 쪽이 정답 문서를 1위로 고른 자리를 찾습니다.
질문의 검색 낱말과 정답 문서의 검색 낱말을 견줍니다."""),
        code(SHARED_TERMS),
        md("""**결과 읽기** — 출력 줄 `정답 문서의 검색 낱말:` 뒤에 낱말 열두 개가 보입니다.
출력 줄 `질문과 정답 문서에 함께 있는 낱말: ['반납']`에서 겹치는 낱말이 하나입니다.
낱말 `돈`과 `연체료`는 뜻이 이어지지만 글자가 달라 겹치지 않습니다.

다음 셀은 그 낱말이 문서 몇 건에 있는지 셉니다.
04절 함수 `count_docs_with()`를 가져와 씁니다. 도구 파일 판은 검색 낱말 목록의 목록을 첫 인자로 받습니다."""),
        code(TERM_DOC_COUNT),
        md("""**결과 읽기** — 라벨 줄 아래 한 줄 `반납 | 1`이 보입니다.
낱말 `반납`은 문서 열두 건 가운데 한 건에만 있습니다.
04절에서 본 대로 드문 낱말은 그 문서를 가리키는 힘이 셉니다.
벡터 거리 쪽이 왜 이 문서를 뒤로 두었는지는 모델 안을 볼 수 없어 적지 않습니다.

## 8. 질문 여덟 개를 잴 함수 준비

질문 두 개로는 두 방법의 차이를 말할 수 없습니다.
지표 함수 네 개는 준비 셀에서 가져온 Ch 11 함수를 그대로 씁니다.
함수 `unique_doc_ids()`가 보는 키는 `doc_id` 하나여서 두 방법의 순위 목록에 모두 씁니다.

다음 셀은 순위 목록 하나를 받아 기록 한 줄을 만듭니다.
값 칸을 빼고 자리와 재현율만 담아 두 방법을 한 표에 둡니다."""),
        code(SCORE_ONE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
인자 `hit_list`를 밖에서 받으므로 이 함수는 어느 방법인지 보지 않습니다.

## 9. 두 방법의 재현율 견주기

질문 여덟 개를 두 방법으로 모두 잽니다.
벡터와 BM25 모델을 미리 만들어 두었으므로 요청은 더 보내지 않습니다."""),
        code(SCORE_ALL),
        md("""**결과 읽기** — `담은 기록 줄 수: 16`이 보입니다. 질문 여덟 개에 방법 두 가지를 곱한 수입니다.

다음 셀은 담은 줄을 표로 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 앞 여덟 줄이 벡터 거리입니다.
줄 `벡터 거리 | C02 | semantic | 7 | 0.0 | 0.0`에서 정답 자리가 7입니다.
자리 3 재현율이 `0.0`이므로 상위 세 자리 안에 정답 문서가 없었습니다.
뒤 여덟 줄은 낱말 겹침이고 `낱말 겹침 | C02 | semantic | 1 | 1.0 | 1.0` 줄이 같은 질문입니다.
줄 `낱말 겹침 | C01 | semantic | 3 | 0.0 | 1.0`은 정답 문서가 셋째 자리였던 질문입니다.

벡터 거리 쪽 여덟 줄의 정답 자리는 01절 표의 값과 같습니다.
낱말 겹침 쪽 여덟 줄의 정답 자리는 04절 표의 값과 같습니다.
03·04절 표는 상위 3개만 담아 자리가 0에서 3까지였습니다.
이 표는 문서 12개를 끝까지 재어 자리가 1에서 12까지 나옵니다.

다음 셀은 자르는 자리마다 질문 평균 재현율을 견줍니다."""),
        code(MEANS),
        md("""**결과 읽기** — 라벨 줄 아래 여섯 줄이 나옵니다.
벡터 거리는 자리 1에서 `0.75`이고 자리 3에서 `0.875`입니다.
낱말 겹침은 자리 1에서 `0.875`이고 자리 3에서 `1.0`입니다.
앞 세 줄은 01절 질문 평균과 같고 뒤 세 줄은 04절 질문 평균과 같습니다.

다음 셀은 정답 자리가 다른 질문만 골라 봅니다."""),
        code(DIFF),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄 `C01 | 2 | 3`과 `C02 | 7 | 1`이 보입니다.
질문 `C01`에서는 벡터 거리 쪽 자리가 앞이고 `C02`에서는 낱말 겹침 쪽 자리가 앞입니다.
두 질문 모두 갈래가 `semantic`이라 갈래로 방법을 고를 수 없습니다.
나머지 여섯 질문은 두 방법의 정답 자리가 같았습니다.

## 정리

1. 같은 문서 12개와 질문 8개를 두 방법에 넣어 순위를 나란히 놓았습니다.
2. 질문 `C01`은 벡터 거리 쪽 자리가 2이고 낱말 겹침 쪽이 3이었습니다.
3. 질문 `C02`는 벡터 거리 쪽 자리가 7이고 낱말 겹침 쪽이 1이었습니다.

06절에서는 두 순위를 하나로 합칩니다.
점수를 더하지 않고 자리 번호만 써서 합치는 방법을 씁니다."""),
    ]


if __name__ == "__main__":
    path = write_notebook(LAB, "05", "05-dense와-sparse-비교", "experiment", cells())
    print("wrote", path)
