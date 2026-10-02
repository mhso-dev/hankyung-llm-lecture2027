"""Ch 12 12절 품질 개선본 노트북 생성기 (QUALITY-UPGRADE.md §2·§3·§6).

사용: python3 author_12.py  → labs/part3/ch12-retrieval-tuning/notebooks/12-종합-튜닝과-실험-로그.ipynb 를 새로 쓴다(출력 없음).
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북은 qa/upgrade/before/notebooks/ 에 있다. **experiment 형식 유지**(chapter.json).

## 01~11절에서 그대로 이어 쓴 것 (handoff.md 「§11 → §12」)

- 경로 후보 `candidates = [".", "../../..", "../../../.."]` + for/break, `nbkit.KEY`, `nbkit.key_and_model_cells`.
- 자료: `advanced-documents.json`(부모 6 · 문서 청크 175) · `advanced-queries.json`(30, 개발 15 / 시험 15).
- §2-7 리팩터(2026-09-21, 작업자 B): 앞 절·Ch 11 함수 열두 개는 도구 파일 `notebooks/rag_tools.py` 에서 가져온다.
  `eligible_items`·`chunk_precision_at(…, parent_by_chunk)`(08) · `kiwi_terms(kiwi, text, keep_tags)`(04) · 문서 청크 판
  `rank_chunks_by_distance`·`rank_chunks_by_bm25`·`unique_chunk_ids` · `parent_ids_of(…, parent_by_chunk)`(07) ·
  `fuse_rank(…, rank_constant)`(06) · `mmr_pick(…, vector_by_chunk)`(10, 안에서 `mmr`·`best_candidate`·`mmr_score`·
  `similarity_to_chosen`·Ch 5 `cosine_similarity` 를 부름) · `recall_at`(Ch 11 02) · `precision_at`(Ch 11 03) ·
  `ndcg_at`(Ch 11 04, 안에서 `dcg_at`·`ideal_dcg(gold_count, cutoff)`·`rank_weight(rank)` — Ch 11 도구 파일 판).
  리팩터 전에는 준비 셀 열여섯 개에 함수 스물네 개를 다시 적었다(Ch 11 04절 함수는 0부터 세는 `rank_weight(position)`·
  `ideal_dcg(gold_doc_ids, cutoff)` 판이었고 값은 Ch 11 판과 같다).
- 값: `keep_tags`·`rank_constant`(60)·`candidate_count`(8)·`recall_place`(3)·`report_place`(5).
- 노트북은 numpy·sklearn 을 직접 쓰지 않는다(도구 파일이 numpy 를 쓴다). `lambda`·내포식·제너레이터 식·조건 표현식·`key=`·`reverse=`·기본값 매개변수·f-string·
  세미콜론·한 줄 복합문·`enumerate`·`zip`·`sum`·`max`·`min`·`set`·`next`·`목록.index`·클래스·`+=`를 쓰지 않는다.

## 이 절이 새로 가르치는 것

- **설정 묶음**: 06절 가중치 여섯 가지 × 10절 관련성 비중 여섯 가지 = 서른여섯 벌.
- **기록 한 줄**: 실행 이름·날짜·입력 지문·설정·지표·난이도 갈래·질문별 결과를 한 줄에 담아 파일로 남긴다.
- **개발로 고르고 시험은 한 번**: Ch 11이 정한 약속. 시험 15문항은 이 절 9절에서 처음 연다.
- **끝까지 이어 붙인 실행 한 번**: 고른 설정으로 찾은 글을 답을 쓰는 모델에 넣고 기록을 남긴다.

## 산출 파일 계약 (읽는 쪽을 실제 파일에서 확인함, 12-diagnosis.md §3)

`runs/advanced-continuity-experiment-log.jsonl`(36줄) · `advanced-continuity-test-result.json` ·
`advanced-continuity-integrated-result.json` 과 `runs/continuity/<session_id>/` 사본 세 개를 쓴다.
읽는 쪽은 `labs/part3/ch12-retrieval-tuning/tests/test_continuity.py` · `textbook/part3/qa/check_continuity.py` 81~137행 ·
`textbook/qa/check_course_continuity.py` 113~219행 · `textbook/part4/ch13-langgraph-basics/qa/author_ch13.py` ·
`textbook/part4/ch15-evaluation-advanced/_author.py` 다섯 곳이다.
지표 칸 이름 네 개(`recall_at_5`·`recall_at_50`·`precision_at_5`·`ndcg_at_5`)와 계산식은 검사 스크립트가 다시 계산해
대조하므로 **반올림하지 않고** 그대로 저장한다. 08~11절이 쓰던 두 칸(`recall_at_3`·`chunk_precision_at_5`)을 더했다.

## 선택한 것과 까닭

1. **손잡이 두 개**(가중치·관련성 비중)로 서른여섯 벌을 만든다. 순위 상수는 06절 값 60 그대로 둔다.
   (§2-7 전에는 「순위 상수를 손잡이로 두면 06절 `fuse_scores()`의 모양을 바꿔야 한다」가 까닭이었다. 도구 파일 판은
   순위 상수를 인자로 받으므로 그 까닭은 없어졌고 b7 문장도 「06절 값 60을 모든 설정에 그대로 썼다」로 고쳤다.)
2. **설정은 문서 청크 정밀도 자리 5로 고른다.** 탐색 실행(/tmp/ch12-12/probe4.py, 2026-09-18)에서 계약 네 칸이
   서른여섯 줄 모두 같은 값(천장)이었다. 노트북 7절이 그 사실을 출력으로 먼저 보이고 고른다(규격 §3).
3. **리랭커를 쓰지 않는다.** 서른여섯 벌에 리랭커를 넣으면 리랭킹 호출이 540번이고, 통합 실행에만 넣으면
   「고른 설정」과 「실제로 돌린 것」이 달라진다. 08절이 「어느 리랭커가 낫다고 말할 수 없다」로 끝난 것도 함께 적는다.
4. **통합 실행은 개발 질문 `Q002` 하나**다. 개선 전 12절과 같은 질문이라 Ch 13이 읽는 `question`·`retrieved` 칸이 이어진다.
5. **실습 폴더 테스트를 고쳤다**(12-diagnosis.md §8). 08·10절 선례대로 `load_notebook_namespace()`로 바꿨다.
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

IMPORTS = r'''# 자료 읽기·지문 만들기·폴더 만들기·시간 적기와 검색 도구를 불러옵니다
import hashlib
import json
import os
import time

from kiwipiepy import Kiwi
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from rank_bm25 import BM25Okapi
# 04·06·07·08·10절과 Ch 11 함수, 문서 청크 판 순위 함수 열두 개를 도구 파일에서 가져옵니다
from rag_tools import chunk_precision_at, eligible_items, fuse_rank, kiwi_terms, mmr_pick
from rag_tools import ndcg_at, parent_ids_of, precision_at, rank_chunks_by_bm25
from rag_tools import rank_chunks_by_distance, recall_at, unique_chunk_ids

print("불러온 이름:", "hashlib", "json", "os", "time", "Kiwi", "init_chat_model", "OpenAIEmbeddings", "BM25Okapi")'''

FIND_ROOT = r'''# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part3/ch12-retrieval-tuning/data"):
        root_path = candidate
        break
print("고른 경로:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

LOAD_DATA = r'''# 07~11절과 같은 파일 두 벌을 읽습니다
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

FILE_HELPERS = r'''# 파일 하나의 지문을 만드는 함수와 글을 파일로 쓰는 함수입니다(Ch 11 01절·Ch 2 05절 코드)
def file_fingerprint(path):
    with open(path, "rb") as file:
        file_bytes = file.read()
    return hashlib.sha256(file_bytes).hexdigest()


def write_text(path, text_value):
    with open(path, "w", encoding="utf-8") as file:
        file.write(text_value)'''

FINGERPRINTS = r'''# Ch 11 원본 질문 파일과 이 챕터 복제본이 같은지 보고 두 입력의 지문을 만듭니다
query_source = "labs/part3/ch11-evaluation/data/evaluation-queries.jsonl"
with open(root_path + "/" + query_source, encoding="utf-8") as file:
    source_lines = file.read().splitlines()
source_queries = []
for line in source_lines:
    source_queries.append(json.loads(line))
corpus_fingerprint = file_fingerprint(data_path + "/advanced-documents.json")
query_fingerprint = file_fingerprint(root_path + "/" + query_source)
print("Ch 11 원본 질문 줄 수:", len(source_queries))
print("이 챕터 복제본과 같은가:", source_queries == queries)
print("문서 지문 앞 열 글자:", corpus_fingerprint[:10])
assert source_queries == queries, "Ch 11 원본 질문과 이 챕터 복제본이 다릅니다."'''

VALUES_A = r'''# 01~11절에서 쓴 값을 그대로 다시 정합니다
keep_tags = ["NNG", "NNP", "NNB", "NR", "VV", "VA", "MAG", "SN", "SL"]
rank_constant = 60
candidate_count = 8
recall_place = 3
report_place = 5
print("남길 품사 표시 수:", len(keep_tags))
print("순위 상수:", rank_constant, "| 후보 수:", candidate_count)
print("부모 문서 재현율을 재는 자리:", recall_place, "| 보고 자리:", report_place)'''

VALUES_B = r'''# 이 절에서 바꿔 볼 손잡이 두 가지와 기록에 남길 지표 칸 이름을 정합니다
weight_choices = [[1.0, 0.0], [3.0, 1.0], [2.0, 1.0], [1.0, 1.0], [1.0, 2.0], [0.0, 1.0]]
relevance_choices = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]
metric_names = ["recall_at_3", "recall_at_5", "recall_at_50", "precision_at_5", "ndcg_at_5", "chunk_precision_at_5"]
select_name = "chunk_precision_at_5"
print("가중치 여섯 가지:", weight_choices)
print("관련성 비중 여섯 가지:", relevance_choices)
print("만들 설정 수:", len(weight_choices) * len(relevance_choices))
print("기록에 남길 지표 칸 수:", len(metric_names))
print("설정을 고를 칸:", select_name)'''

CHUNK_TEXTS = r'''# 문서 청크마다 제목과 본문을 이어 붙여 글 하나로 만듭니다(07~11절과 같은 코드)
chunk_texts = []
chunk_ids = []
for chunk in chunks:
    chunk_text = chunk["title"] + " " + chunk["text"]
    chunk_texts.append(chunk_text)
    chunk_ids.append(chunk["chunk_id"])
all_chunk_count = len(chunk_ids)
print("이어 붙인 글 수:", len(chunk_texts))
print("첫 문서 청크 ID:", chunk_ids[0])'''

CHUNK_MAPS = r'''# 문서 청크 ID로 부모 문서 ID와 쪽 번호와 본문을 바로 찾게 짝을 만듭니다
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

EMBEDDINGS = r'''# 01~11절과 같은 모델로 문서 청크를 벡터로 바꿉니다(임베딩 요청 1번)
embedding_model_name = "text-embedding-3-small"
vector_dimensions = 256
embedding_model = OpenAIEmbeddings(model=embedding_model_name, dimensions=vector_dimensions)
chunk_vectors = embedding_model.embed_documents(chunk_texts)
vector_by_chunk = {}
for i in range(len(chunk_ids)):
    vector_by_chunk[chunk_ids[i]] = chunk_vectors[i]
print("임베딩 모델 이름:", embedding_model.model)
print("벡터의 숫자 개수 설정:", embedding_model.dimensions)
print("문서 청크 벡터 수:", len(chunk_vectors))'''

BM25_MODEL = r'''# 04~11절과 같은 형태소 분석기로 문서 청크마다 검색 낱말 목록을 만들고 BM25 모델을 만듭니다
kiwi = Kiwi()
kiwi_corpus = []
for text in chunk_texts:
    kiwi_corpus.append(kiwi_terms(kiwi, text, keep_tags))
bm25_model = BM25Okapi(kiwi_corpus)
print("검색 낱말 목록 수:", len(kiwi_corpus))
print("BM25 모델이 본 문서 청크 수:", bm25_model.corpus_size)
print("문서 청크 하나의 평균 검색 낱말 수:", round(bm25_model.avgdl, 2))'''

DEV_QUERIES = r'''# 질문 30개에서 개발 묶음만 고르고 질문 ID로 찾을 수 있게 짝지어 둡니다
dev_all = []
for query in queries:
    if query["split"] == "dev":
        dev_all.append(query)
dev_queries = eligible_items(dev_all)
question_count = len(dev_queries)
item_by_qid = {}
for item in dev_queries:
    item_by_qid[item["qid"]] = item
print("개발 질문 수:", question_count)
print("시험 질문 수:", len(queries) - len(dev_all))
print("첫 개발 질문:", dev_queries[0]["qid"], "|", dev_queries[0]["question"])'''

SEARCH_FUNCS = r'''# 질문 하나로 순위 목록 두 개를 만들고 설정대로 앞자리를 후보로 자릅니다
def question_lists(question_vector, question):
    distance_hits = rank_chunks_by_distance(question_vector, chunk_vectors, chunk_ids, all_chunk_count)
    question_terms = kiwi_terms(kiwi, question, keep_tags)
    score_hits = rank_chunks_by_bm25(bm25_model, question_terms, chunk_ids, all_chunk_count)
    return [unique_chunk_ids(distance_hits), unique_chunk_ids(score_hits)]


def candidates_of(question_id, config):
    fused_ids = fuse_rank(lists_by_qid[question_id], config["weights"], rank_constant)
    return fused_ids[:config["candidate_k"]]'''

PREPARE_DEV = r'''# 개발 질문 열다섯 개를 벡터로 바꾸고 순위 목록 두 개씩 미리 만듭니다(임베딩 요청 15번)
vector_by_qid = {}
lists_by_qid = {}
for item in dev_queries:
    question_vector = embedding_model.embed_query(item["question"])
    vector_by_qid[item["qid"]] = question_vector
    lists_by_qid[item["qid"]] = question_lists(question_vector, item["question"])
first_id = dev_queries[0]["qid"]
print("질문 벡터 수:", len(vector_by_qid))
print("질문 하나의 순위 목록 수:", len(lists_by_qid[first_id]))
print("순위 목록 하나의 문서 청크 수:", len(lists_by_qid[first_id][0]))'''

METRICS = r'''# 보고한 부모 문서와 문서 청크에서 기록에 남길 값 여섯 개를 냅니다
def metrics(candidate_doc_ids, top_doc_ids, gold_doc_ids, picked_chunk_ids):
    narrow = recall_at(top_doc_ids, gold_doc_ids, recall_place)
    wide = recall_at(top_doc_ids, gold_doc_ids, report_place)
    inside = recall_at(candidate_doc_ids, gold_doc_ids, candidate_count)
    doc_precision = precision_at(top_doc_ids, gold_doc_ids, report_place)
    gain = ndcg_at(top_doc_ids, gold_doc_ids, report_place)
    chunk_precision = chunk_precision_at(picked_chunk_ids, gold_doc_ids, report_place, parent_by_chunk)
    return narrow, wide, inside, doc_precision, gain, chunk_precision


# 고른 문서 청크를 기록 모양(문서 ID·쪽·청크 ID·자리)으로 바꿉니다
def top_results_of(picked_chunk_ids):
    hits = []
    for chunk_id in picked_chunk_ids:
        hit = {"doc_id": parent_by_chunk[chunk_id], "page": page_by_chunk[chunk_id], "chunk_id": chunk_id}
        hit["rank"] = len(hits) + 1
        hits.append(hit)
    return hits'''

SUMMARY = r'''# 기록 줄 여러 개에서 지표 칸마다 질문 평균을 냅니다
def metric_summary(rows):
    summary = {}
    for name in metric_names:
        total = 0.0
        for row in rows:
            total = total + row[name]
        summary[name] = total / len(rows)
    return summary'''

RESULT_ROW = r'''# 질문 하나의 결과를 기록 한 줄로 만듭니다
def result_row(item, hits, candidate_doc_ids, scores):
    row = {"qid": item["qid"], "tier": item["tier"], "split": item["split"]}
    row["gold_doc_ids"] = item["gold_doc_ids"]
    row["returned_count"] = len(hits)
    row["candidate_doc_ids"] = candidate_doc_ids
    row["top_results"] = hits
    for index in range(len(metric_names)):
        row[metric_names[index]] = scores[index]
    return row'''

SLICES = r'''# 난이도 갈래마다 기록 줄을 모아 갈래별 질문 평균을 냅니다
def slice_summary(rows):
    groups = {}
    for row in rows:
        tier = row["tier"]
        if tier not in groups:
            groups[tier] = []
        groups[tier].append(row)
    summary = {}
    for tier in groups:
        summary[tier] = metric_summary(groups[tier])
    return summary'''

EVALUATE = r'''# 설정 하나로 질문 하나를 재어 기록 한 줄을 만듭니다
def evaluate_item(config, item):
    found_ids = candidates_of(item["qid"], config)
    picked_ids = mmr_pick(vector_by_qid[item["qid"]], found_ids, config["report_k"], config["relevance_weight"], vector_by_chunk)
    candidate_doc_ids = parent_ids_of(found_ids, parent_by_chunk)
    scores = metrics(candidate_doc_ids, parent_ids_of(picked_ids, parent_by_chunk), item["gold_doc_ids"], picked_ids)
    return result_row(item, top_results_of(picked_ids), candidate_doc_ids, scores)


# 설정 하나를 질문 묶음 전체에 적용해 평균·갈래 평균·질문별 줄을 냅니다
def evaluate_config(config, items):
    picked_items = eligible_items(items)
    if len(picked_items) == 0:
        raise ValueError("평가 가능한 문항이 없습니다")
    rows = []
    for item in picked_items:
        rows.append(evaluate_item(config, item))
    return metric_summary(rows), slice_summary(rows), rows'''

RUN_NAMES = r'''# 실행 이름과 모든 기록 줄에 똑같이 들어갈 칸을 미리 만듭니다
session_id = time.strftime("%Y%m%dT%H%M%S")
run_prefix = "advanced-continuity-" + session_id
fixed_fields = {"run_date": time.strftime("%Y-%m-%d"), "source_chapter": "ch12"}
fixed_fields["query_source_chapter"] = "ch11"
fixed_fields["query_source"] = query_source
fixed_fields["corpus_fingerprint"] = corpus_fingerprint
fixed_fields["query_fingerprint"] = query_fingerprint
fixed_fields["evaluation_unit"] = "unique-parent-document"
fixed_fields["metrics_policy"] = "chunk-candidate-unique-parent-macro-v1"
fixed_fields["query_count"] = question_count
fixed_fields["excluded_query_count"] = 0
print("고정으로 넣을 칸 수:", len(fixed_fields))
print("고정 칸 이름:", sorted(fixed_fields))'''

LOG_ROW = r'''# 설정 하나를 질문 묶음에 적용해 기록 한 줄을 완성합니다
def log_row(run_id, config, split_name, policy, items):
    summary, slices, rows = evaluate_config(config, items)
    row = fixed_fields.copy()
    row["run_id"] = run_id
    row["settings"] = config
    row["split"] = split_name
    row["comparison_policy"] = policy
    row["metrics"] = summary
    row["slices"] = slices
    row["results"] = rows
    return row'''

CONFIGS = r'''# 손잡이 두 가지를 곱해 설정 서른여섯 벌을 만듭니다
configs = []
for weights in weight_choices:
    for relevance_weight in relevance_choices:
        config = {"weights": weights, "relevance_weight": relevance_weight}
        config["rank_constant"] = rank_constant
        config["candidate_k"] = candidate_count
        config["candidate_unit"] = "chunk"
        config["report_k"] = report_place
        config["report_unit"] = "unique-parent-document"
        configs.append(config)
print("설정 수:", len(configs))
print("첫 설정:", configs[0])'''

RUN_DEV = r'''# 설정 서른여섯 벌을 개발 열다섯 문항에 차례로 적용합니다
dev_policy = "compare-only-pairs-that-differ-by-one-setting"
dev_rows = []
for index in range(len(configs)):
    run_id = run_prefix + "-dev-" + str(index + 1).zfill(2)
    dev_rows.append(log_row(run_id, configs[index], "dev", dev_policy, dev_queries))
print("개발 기록 줄 수:", len(dev_rows))
print("한 줄에 담긴 질문 결과 수:", len(dev_rows[0]["results"]))
print("첫 줄의 문서 청크 정밀도 자리 5:", round(dev_rows[0]["metrics"][select_name], 4))
assert len(dev_rows) == len(configs), "설정마다 기록이 한 줄씩 있어야 합니다."'''

SAVE_DEV = r'''# 개발 기록 서른여섯 줄을 한 줄에 하나씩 파일로 쓰고 사본도 남깁니다
run_dir = root_path + "/labs/part3/ch12-retrieval-tuning/runs"
session_dir = run_dir + "/continuity/" + session_id
os.makedirs(session_dir)
experiment_text = ""
for row in dev_rows:
    experiment_text = experiment_text + json.dumps(row, ensure_ascii=False) + "\n"
write_text(run_dir + "/advanced-continuity-experiment-log.jsonl", experiment_text)
write_text(session_dir + "/advanced-continuity-experiment-log.jsonl", experiment_text)
print("기록 파일에 쓴 줄 수:", len(dev_rows))
print("기록 한 줄의 칸 수:", len(dev_rows[0]))'''

COLUMN_VALUES = r'''# 지표 칸마다 서른여섯 줄에 나온 서로 다른 값을 모아 봅니다
print("기록 칸 | 서른여섯 줄에 나온 서로 다른 값")
for name in metric_names:
    seen_values = []
    for row in dev_rows:
        value = round(row["metrics"][name], 4)
        if value not in seen_values:
            seen_values.append(value)
    print(name, "|", sorted(seen_values))'''

KNOB_FUNCS = r'''# 손잡이 값 하나를 가진 줄만 모아 지표 칸의 평균을 냅니다
def knob_mean(name, value, metric_name):
    total = 0.0
    count = 0
    for row in dev_rows:
        if row["settings"][name] == value:
            total = total + row["metrics"][metric_name]
            count = count + 1
    return round(total / count, 4)


# 손잡이 하나의 값들을 한 줄씩 출력합니다
def print_knob_rows(label, name, values):
    for value in values:
        chunk_precision = knob_mean(name, value, select_name)
        gain = knob_mean(name, value, "ndcg_at_5")
        print(label, "|", value, "|", chunk_precision, "|", gain)'''

KNOB_TABLE = r'''# 손잡이별 평균을 한 표로 냅니다
print("손잡이 | 값 | 문서 청크 정밀도 자리 5 평균 | nDCG 자리 5 평균")
print_knob_rows("가중치", "weights", weight_choices)
print_knob_rows("관련성 비중", "relevance_weight", relevance_choices)'''

PICK_BEST = r'''# 문서 청크 정밀도 자리 5가 가장 큰 줄을 고릅니다(값이 같으면 앞 줄을 둡니다)
best_row = dev_rows[0]
for row in dev_rows:
    if row["metrics"][select_name] > best_row["metrics"][select_name]:
        best_row = row
best_config = best_row["settings"]
print("고른 가중치:", best_config["weights"])
print("고른 관련성 비중:", best_config["relevance_weight"])
print("그 줄의 문서 청크 정밀도 자리 5:", round(best_row["metrics"][select_name], 4))
print("그 줄의 nDCG 자리 5:", round(best_row["metrics"]["ndcg_at_5"], 4))'''

PREPARE_TEST = r'''# 시험 열다섯 문항을 이제 처음 열어 벡터와 순위 목록을 만듭니다(임베딩 요청 15번)
test_all = []
for query in queries:
    if query["split"] == "test":
        test_all.append(query)
test_queries = eligible_items(test_all)
for item in test_queries:
    question_vector = embedding_model.embed_query(item["question"])
    vector_by_qid[item["qid"]] = question_vector
    lists_by_qid[item["qid"]] = question_lists(question_vector, item["question"])
print("시험 질문 수:", len(test_queries))
print("첫 시험 질문:", test_queries[0]["qid"], "|", test_queries[0]["question"])'''

RUN_TEST = r'''# 고른 설정 한 벌만 시험 문항에 한 번 적용하고 기록을 저장합니다
test_policy = "selected-on-dev-then-evaluate-test-once"
test_row = log_row(run_prefix + "-test-01", best_config, "test", test_policy, test_queries)
test_row["selected_run_id"] = best_row["run_id"]
test_text = json.dumps(test_row, ensure_ascii=False, indent=2)
write_text(run_dir + "/advanced-continuity-test-result.json", test_text)
write_text(session_dir + "/advanced-continuity-test-result.json", test_text)
print("기록 칸 | 개발 | 시험")
for name in metric_names:
    print(name, "|", round(best_row["metrics"][name], 4), "|", round(test_row["metrics"][name], 4))'''

SMOKE_SEARCH = r'''# 고른 설정으로 개발 질문 하나를 검색해 봅니다
smoke_id = "Q002"
smoke_item = item_by_qid[smoke_id]
smoke_found = candidates_of(smoke_id, best_config)
smoke_picked = mmr_pick(vector_by_qid[smoke_id], smoke_found, report_place, best_config["relevance_weight"], vector_by_chunk)
smoke_hits = top_results_of(smoke_picked)
print("고른 질문:", smoke_id, "|", smoke_item["question"])
print("그 질문의 정답 부모 문서 ID:", smoke_item["gold_doc_ids"])
print("보고 자리 다섯 개의 문서 청크 ID:", smoke_picked)
print("그 문서 청크의 부모 문서 차례:", parent_ids_of(smoke_picked, parent_by_chunk))'''

SMOKE_CONTEXT = r'''# 앞자리 세 개의 본문과 출처 표시를 이어 붙여 모델에 넣을 글을 만듭니다
context_count = 3
context_hits = smoke_hits[:context_count]
context_text = ""
for hit in context_hits:
    source_label = "[" + hit["doc_id"] + " p." + str(hit["page"]) + "]"
    context_text = context_text + source_label + "\n" + text_by_chunk[hit["chunk_id"]] + "\n\n"
print("넣을 자리 수:", len(context_hits))
print("첫 출처 표시:", "[" + context_hits[0]["doc_id"] + " p." + str(context_hits[0]["page"]) + "]")
print("넣을 글의 길이:", len(context_text))'''

SMOKE_ANSWER = r'''# 넣은 글만 보고 답을 쓰게 하고 출처 표시를 붙이도록 부탁합니다(모델 요청 1번)
prompt = "아래 자료만 보고 질문에 한국어로 답하세요.\n"
prompt = prompt + "답 끝에 [문서ID p.쪽] 모양으로 출처를 적으세요.\n\n"
prompt = prompt + "질문: " + smoke_item["question"] + "\n\n"
prompt = prompt + "자료:\n" + context_text
answer = model.invoke(prompt)
answer_text = answer.text.strip()
print("보낸 글의 길이:", len(prompt))
print("답:", answer_text)'''

SMOKE_SETTINGS = r'''# 통합 실행의 설정을 적습니다(벡터의 숫자 개수는 실제 벡터에서 읽습니다)
smoke_settings = {"input": "advanced-documents.json chunk text"}
smoke_settings["dense"] = embedding_model_name
smoke_settings["sparse"] = "Kiwi+BM25"
smoke_settings["fusion"] = "RRF(k=" + str(rank_constant) + ")"
smoke_settings["weights"] = best_config["weights"]
smoke_settings["relevance_weight"] = best_config["relevance_weight"]
smoke_settings["reranker"] = None
smoke_settings["context_selection"] = "matched-chunk-text"
smoke_settings["chat"] = model.model_name
smoke_settings["dimensions"] = len(chunk_vectors[0])
print("통합 실행 설정:", smoke_settings)'''

SMOKE_SAVE = r'''# 통합 실행 한 번을 기록 파일로 남깁니다(지표는 재지 않았습니다)
integrated = {"run_id": run_prefix + "-integrated-01", "run_type": "generation_smoke_test"}
integrated["qid"] = smoke_id
integrated["split"] = smoke_item["split"]
integrated["question"] = smoke_item["question"]
integrated["gold_doc_ids"] = smoke_item["gold_doc_ids"]
integrated["retrieved"] = context_hits
integrated["response"] = answer_text
integrated["retrieval_metrics"] = None
integrated["generation_evaluation"] = {"status": "not_evaluated", "next_chapter": "Ch15"}
integrated["settings"] = smoke_settings
integrated_text = json.dumps(integrated, ensure_ascii=False, indent=2)
write_text(run_dir + "/advanced-continuity-integrated-result.json", integrated_text)
write_text(session_dir + "/advanced-continuity-integrated-result.json", integrated_text)
print("기록한 칸 수:", len(integrated))'''

TITLE = """# 종합 튜닝과 실험 로그

**이 노트북에서 할 일**

1. 06절 가중치와 10절 관련성 비중을 곱해 설정 서른여섯 벌을 만듭니다.
2. 개발 열다섯 문항으로 서른여섯 벌을 재고 기록 파일에 남깁니다.
3. 기록을 보고 설정 한 벌을 고른 뒤 시험 열다섯 문항에 한 번만 적용합니다.
4. 고른 설정으로 찾은 글을 모델에 넣어 답을 쓰고 마지막 기록을 남깁니다.

**준비물** — 프로젝트 폴더의 `.env`에 `OPENAI_API_KEY`가 있어야 합니다.
임베딩 요청은 문서 청크 1번과 질문 30번으로 모두 서른한 번입니다.
답을 쓰는 모델 요청은 통합 실행 한 번뿐입니다.
예상 비용은 미화 0.01달러 아래이고 실행 시간은 2분 안팎입니다.

**쓰는 파일** — 이 절은 이 챕터에서 처음으로 파일을 씁니다.
실습 폴더 `runs/` 아래에 기록 파일 세 개와 같은 내용의 사본 세 개를 만듭니다.
사본 폴더 이름에는 실행한 시각이 들어가므로 실행할 때마다 새로 생깁니다.

**데이터** — 세 파일 모두 실습 묶음에 들어 있습니다.

- 문서 `labs/part3/ch12-retrieval-tuning/data/advanced-documents.json`(부모 6건·문서 청크 175개)
- 질문 `labs/part3/ch12-retrieval-tuning/data/advanced-queries.json`(30개)
- Ch 11 원본 질문 `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl`(30줄)

**강의와 실습 범위** — 강의 시간에는 5~10절을 읽습니다.
지표와 기록 한 줄을 만드는 자리가 5절이고 설정 서른여섯 벌이 6절입니다.
7절이 개발 결과 읽기, 8절이 설정 고르기, 9절이 시험 한 번입니다.
1~4절은 함께 실행하고 10절은 실습 시간에 다시 읽습니다.

**기준 버전** — 첫 셀에서 여섯 패키지를 고정한 판으로 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

실습 폴더 `labs/part3/ch12-retrieval-tuning`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""

FIGURE_ALT = ("위에서 아래로 내려가는 흐름도로 맨 위 초록 상자 문서 청크 175개와 질문 30개가 파란 상자 "
              "설정 36벌로 이어지고 그 아래 파란 상자 개발 15문항 실행 36번과 노란 상자 기록 36줄을 지나 "
              "파란 상자 설정 한 벌 고르기로 모이며 거기서 왼쪽 파란 상자 시험 15문항 실행 1번 "
              "기록 1줄과 오른쪽 보라 상자 답 쓰기 1번 gpt-5.4-mini 기록 1줄로 갈라지는 그림")

FIGURE_READ = """맨 위 초록 상자가 07~11절과 같은 자료입니다.
그 아래 파란 상자에서 손잡이 두 개를 곱해 설정 서른여섯 벌을 만듭니다.
개발 열다섯 문항으로 서른여섯 번 재고 노란 상자에 기록 서른여섯 줄을 남깁니다.
그 기록을 보고 설정 한 벌을 고른 뒤에야 시험 열다섯 문항을 한 번 엽니다.
맨 아래 오른쪽 보라 상자가 이 절에서 답을 쓰는 모델을 부르는 한 자리입니다."""


def prep(source: str) -> dict:
    """앞 절 함수를 다시 정의하는 준비 셀(셀 하나에 함수 둘 이상 허용)."""
    return code(source, lesson_role="setup", upgrade_allow=["multiple_defs_in_cell"])


def new_funcs(source: str) -> dict:
    """이 절에서 새로 만드는 함수 둘을 한 셀에 담습니다."""
    return code(source, upgrade_allow=["multiple_defs_in_cell"])


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIGURE_ALT + "](attachment:12-1-설정-서른여섯-벌과-두-번의-실행.png)\n\n" + FIGURE_READ, html="skip"),
        md("""## 1. 준비

첫 셀은 패키지 여섯 개를 설치하고 설치된 버전을 출력합니다.
11절과 같은 여섯 개입니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 `langchain: 1.4.0`과 `rank-bm25: 0.2.2`가 보입니다.
마지막 줄 `numpy: 2.5.3`은 도구 파일이 벡터 계산에 쓰는 패키지입니다. 여섯 줄이 모두 보이면 다음 셀로 넘어갑니다.

다음 셀은 이 절에서 쓸 이름 여덟 개를 불러옵니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.

이 노트북은 04·06·07·08·10절 함수 여섯 개와 Ch 11 지표 함수 세 개를 가져옵니다.
04절 `kiwi_terms()`, 06절 `fuse_rank()`, 07절 `parent_ids_of()`, 10절 `mmr_pick()`입니다.
08절 `eligible_items()`·`chunk_precision_at()`, Ch 11 `recall_at()`·`precision_at()`·`ndcg_at()`도 가져옵니다.
07~11절과 같은 문서 청크 판 순위 함수 세 개도 함께 가져옵니다.
인자 모양은 4절에서 정리합니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄은 `불러온 이름:` 뒤에 이름 여덟 개가 붙은 한 줄입니다.
이름 `hashlib`과 `time`이 07~11절에는 없던 것입니다.
지문을 만들 때 `hashlib`을 쓰고 실행 이름에 시각을 적을 때 `time`을 씁니다.
도구 파일에서 가져온 함수 열두 개는 출력하지 않습니다."""),
    ] + key_and_model_cells(
        "openai:gpt-5.4-mini",
        "temperature 값을 0으로 두어 매번 비슷한 문장을 고르게 합니다.\n"
        "설정 `reasoning_effort=\"none\"`은 답을 쓰기 전에 따로 생각하는 단계를 두지 않게 합니다.",
    ) + [
        md("""다음 셀은 프로젝트 맨 위 폴더를 찾습니다. 01~11절과 같은 코드입니다."""),
        setup(FIND_ROOT),
        md("""**결과 읽기** — 출력 줄은 `고른 경로: .`입니다. 확인 줄도 통과했습니다.

다음 셀은 07~11절과 같은 자료 두 벌을 읽습니다."""),
        setup(LOAD_DATA),
        md("""**결과 읽기** — `부모 문서 수: 6`과 `문서 청크 수: 175`, `질문 수: 30`이 보입니다.
07~11절과 같은 파일이라 세 값도 같습니다.

## 2. 입력 지문과 값 정하기

기록에는 어떤 입력으로 잰 값인지도 함께 남깁니다.
파일 내용이 한 글자만 달라져도 값이 달라지는 짧은 글을 지문이라고 부릅니다.
다음 셀은 지문을 만드는 함수와 글을 파일로 쓰는 함수를 정의합니다."""),
        prep(FILE_HELPERS),
        md("""정의 셀이라 출력이 없습니다.
첫 함수는 파일을 바이트로 읽어 SHA-256 지문을 냅니다. Ch 11 01절과 같은 코드입니다.
둘째 함수는 글 하나를 파일로 씁니다. Ch 2 05절에서 배운 모양입니다.

다음 셀은 Ch 11 원본 질문 파일과 이 챕터 복제본이 같은지 보고 지문 두 개를 만듭니다."""),
        code(FINGERPRINTS),
        md("""**결과 읽기** — `Ch 11 원본 질문 줄 수: 30`과 `이 챕터 복제본과 같은가: True`가 보입니다.
줄 `문서 지문 앞 열 글자:` 뒤의 값은 문서 파일의 지문입니다.
지문은 실행마다 같지만 파일을 고치면 달라지므로 본문에 인용하지 않습니다.

다음 셀은 01~11절에서 쓴 값을 그대로 다시 정합니다."""),
        code(VALUES_A),
        md("""**결과 읽기** — 줄 `순위 상수: 60 | 후보 수: 8`은 06~11절과 같은 값입니다.
줄 `부모 문서 재현율을 재는 자리: 3 | 보고 자리: 5`도 08~11절과 같습니다.

다음 셀은 이 절에서 바꿔 볼 손잡이 두 가지를 정합니다.
가중치는 06절에서 순위 두 개를 합칠 때 준 몫이고 여섯 가지를 봅니다.
관련성 비중은 10절에서 다양성과 관련성을 맞바꾸던 값이고 여섯 가지를 봅니다."""),
        code(VALUES_B),
        md("""**결과 읽기** — 줄 `만들 설정 수: 36`이 여섯 곱하기 여섯입니다.
줄 `기록에 남길 지표 칸 수: 6` 가운데 넷은 Ch 11 도구가 쓰는 칸 이름입니다.
줄 `설정을 고를 칸: chunk_precision_at_5`가 08~11절에서 쓰던 문서 청크 정밀도입니다.
왜 이 칸으로 고르는지는 7절에서 출력을 보고 정합니다.

## 3. 검색에 쓸 재료 만들기

문서 청크마다 제목과 본문을 이어 붙여 글 하나로 만듭니다."""),
        code(CHUNK_TEXTS),
        md("""**결과 읽기** — `이어 붙인 글 수: 175`가 보입니다.
줄 `첫 문서 청크 ID: E01-P01-C01`의 이름 앞머리가 그 문서 청크의 부모 문서 ID입니다.

기록에는 문서 ID와 쪽 번호도 함께 남깁니다.
다음 셀은 문서 청크 ID로 부모·쪽·본문을 바로 찾을 수 있게 짝을 만듭니다."""),
        code(CHUNK_MAPS),
        md("""**결과 읽기** — `짝지은 문서 청크 수: 175`가 보입니다.
줄 `첫 문서 청크의 부모 문서 ID: E01`과 `첫 문서 청크의 쪽 번호: 1`이 기록에 들어갈 값입니다.

다음 셀은 문서 청크를 벡터로 바꿉니다. 01~11절과 같은 모델을 씁니다."""),
        code(EMBEDDINGS),
        md("""**결과 읽기** — `벡터의 숫자 개수 설정: 256`과 `문서 청크 벡터 수: 175`가 보입니다.
여기까지 임베딩 요청은 한 번입니다.

## 4. 앞 절 함수의 인자 확인하기

앞 절과 Ch 11 함수 열두 개는 준비 셀에서 도구 파일로부터 가져왔습니다.
두 순위와 합치기는 11절과 같은 판입니다. 합치기 `fuse_rank()`는 순위 상수를 셋째 인자로 받습니다.

07절 `parent_ids_of()`와 08절 `chunk_precision_at()`은 짝 사전 `parent_by_chunk`를 인자로 받습니다.
10절 `mmr_pick()`은 도구 파일 판이라 짝 사전 `vector_by_chunk`를 다섯째 인자로 받습니다.
MMR 점수를 내는 10절 함수 네 개는 이 함수 안에서 불립니다.

두 가지만 짚고 넘어갑니다.
Ch 11 04절 `ndcg_at()`은 01~11절에서 쓰지 않았고 이 절에서 처음 다시 씁니다.
기록 파일의 칸 이름이 Ch 11 도구 이름이라 그 계산을 그대로 써야 하기 때문입니다.
정밀도는 이름이 둘입니다. 부모 문서를 세는 쪽이 Ch 11 03절 `precision_at()`이고 문서 청크를 세는 쪽이 08절 `chunk_precision_at()`입니다.

다음 셀은 문서 청크의 검색 낱말 목록으로 BM25 모델을 만듭니다.
분석기를 만드는 줄 `kiwi = Kiwi()`는 1초 안팎 걸립니다."""),
        code(BM25_MODEL),
        md("""**결과 읽기** — `검색 낱말 목록 수: 175`와 `BM25 모델이 본 문서 청크 수: 175`가 보입니다.
줄 `문서 청크 하나의 평균 검색 낱말 수: 44.01`은 07~11절과 같은 값입니다.

다음 셀은 개발 묶음을 가릅니다.
Ch 11이 정한 약속은 개발 15문항으로 설정을 고르는 것입니다.
시험 15문항은 설정을 다 고른 뒤 9절에서 한 번만 엽니다."""),
        code(DEV_QUERIES),
        md("""**결과 읽기** — `개발 질문 수: 15`와 `시험 질문 수: 15`가 보입니다.
줄 `첫 개발 질문:` 뒤에 질문 ID와 질문 글이 있습니다.

다음 셀은 질문 하나를 후보 목록으로 바꾸는 함수 둘입니다. 11절과 같은 얼개입니다."""),
        new_funcs(SEARCH_FUNCS),
        md("""정의 셀이라 출력이 없습니다.
첫 함수는 벡터 거리 순위와 낱말 겹침 순위 두 개를 목록에 담아 냅니다.
둘째 함수는 그 두 목록을 설정의 가중치로 합쳐 앞자리 여덟 개를 자릅니다.
11절과 다른 점은 가중치를 설정에서 꺼내 쓴다는 것뿐입니다.

다음 셀은 개발 질문마다 벡터와 순위 목록을 미리 만들어 둡니다.
설정이 바뀌어도 이 두 가지는 그대로라 한 번만 만들면 됩니다."""),
        code(PREPARE_DEV),
        md("""**결과 읽기** — `질문 벡터 수: 15`와 `질문 하나의 순위 목록 수: 2`가 보입니다.
줄 `순위 목록 하나의 문서 청크 수: 175`는 문서 청크를 모두 줄 세웠다는 뜻입니다.
여기까지 임베딩 요청은 열여섯 번입니다.

## 5. 지표와 기록 한 줄 만들기

기록에 남길 값은 여섯 개입니다. 앞의 네 개는 Ch 11 도구가 쓰는 칸 이름입니다.
다음 셀은 값 여섯 개를 내는 함수와 보고 자리를 기록 모양으로 바꾸는 함수입니다."""),
        new_funcs(METRICS),
        md("""정의 셀이라 출력이 없습니다.
칸 `recall_at_3`과 `recall_at_5`는 보고한 부모 문서 차례에서 자리만 다르게 잰 재현율입니다.
칸 `recall_at_50`은 후보 여덟 개의 부모 문서에서 잰 재현율입니다.
이름에 50이 붙은 것은 Ch 11 도구가 정한 이름이라 그대로 두었기 때문입니다.
이름을 바꾸면 과정 검사 스크립트가 이 칸을 찾지 못해 멈춥니다.

칸 `precision_at_5`는 부모 문서를 세고 `chunk_precision_at_5`는 문서 청크를 셉니다.
둘 다 나누는 수는 보고 자리 5로 고정입니다. Ch 11 03절에서 배운 고정 분모입니다.
둘째 함수는 고른 문서 청크마다 문서 ID·쪽·청크 ID·자리 번호를 적습니다.

다음 셀은 기록 줄 여러 개의 평균을 내는 함수와 질문 한 개의 줄을 만드는 함수입니다."""),
        code(SUMMARY),
        md("""정의 셀이라 출력이 없습니다.
칸 이름마다 질문 평균을 냅니다. 여기서는 반올림하지 않습니다.
검사 스크립트가 같은 평균을 다시 계산해 대조하기 때문입니다.

다음 셀은 질문 하나의 결과를 기록 한 줄로 만드는 함수입니다."""),
        code(RESULT_ROW),
        md("""정의 셀이라 출력이 없습니다.
질문 ID·난이도·분할·정답 부모·보고한 자리·지표 여섯 칸을 한 딕셔너리에 담습니다.
칸 `returned_count`는 실제로 보고한 자리 수입니다.

다음 셀은 난이도 갈래마다 평균을 따로 내는 함수입니다.
질문 서른 개는 쉬움·보통·어려움 세 갈래로 나뉘어 있습니다."""),
        new_funcs(SLICES),
        md("""정의 셀이라 출력이 없습니다.
갈래 이름은 질문 파일의 `tier` 칸에 적혀 있고 그대로 씁니다.
갈래마다 줄을 모은 뒤 앞 함수로 같은 평균을 냅니다.

다음 셀은 설정 하나를 질문 하나에 적용하는 함수와 묶음 전체에 적용하는 함수입니다."""),
        new_funcs(EVALUATE),
        md("""정의 셀이라 출력이 없습니다.
첫 함수의 차례는 후보 자르기, MMR로 고르기, 부모 차례 만들기, 값 여섯 개 재기입니다.
07~11절에서 하나씩 배운 단계를 한 줄씩 이어 붙인 것입니다.
둘째 함수는 답할 수 있는 질문만 남기고 하나도 없으면 실행을 멈춥니다.

다음 셀은 실행 이름과 모든 기록 줄에 똑같이 들어갈 칸을 만듭니다."""),
        code(RUN_NAMES),
        md("""**결과 읽기** — `고정으로 넣을 칸 수: 10`이 보입니다.
줄 `고정 칸 이름:` 아래에 이름 열 개가 차례로 나옵니다.
실행 이름에는 시각이 들어가 실행할 때마다 달라지므로 본문에 인용하지 않습니다.

다음 셀은 설정 하나를 재어 기록 한 줄로 만드는 함수입니다."""),
        code(LOG_ROW),
        md("""정의 셀이라 출력이 없습니다.
고정 칸을 복사한 뒤 실행 이름·설정·분할·비교 규칙·지표·갈래·질문별 결과를 더합니다.
칸 `comparison_policy`는 이 실행을 어떻게 견줄 수 있는지 적어 두는 자리입니다.

## 6. 설정 서른여섯 벌 만들고 실행하기

손잡이 두 가지를 곱합니다. 가중치 여섯 가지에 관련성 비중 여섯 가지입니다."""),
        code(CONFIGS),
        md("""**결과 읽기** — `설정 수: 36`이 보입니다.
줄 `첫 설정:` 뒤의 딕셔너리에 손잡이 두 개와 고정 값 다섯 개가 함께 있습니다.
칸 `candidate_unit`과 `report_unit`은 값이 무엇을 세는 단위인지 적어 둔 것입니다.

다음 셀이 설정 서른여섯 벌을 개발 열다섯 문항에 차례로 적용합니다.
실행 전에 예상해 봅니다. 관련성 비중을 낮추면 문서 청크 정밀도가 내려갈 것입니다."""),
        code(RUN_DEV),
        md("""**결과 읽기** — `개발 기록 줄 수: 36`과 `한 줄에 담긴 질문 결과 수: 15`가 보입니다.
줄 `첫 줄의 문서 청크 정밀도 자리 5: 0.76`이 첫 설정의 값입니다.
확인 줄은 설정 수와 기록 줄 수가 같은지만 봅니다.

다음 셀이 기록 서른여섯 줄을 파일로 씁니다. 사본도 함께 남깁니다."""),
        code(SAVE_DEV),
        md("""**결과 읽기** — `기록 파일에 쓴 줄 수: 36`과 `기록 한 줄의 칸 수: 17`이 보입니다.
사본 폴더 이름에는 실행한 시각이 들어가므로 본문에 인용하지 않습니다.
사본을 남기면 나중에 파일을 덮어써도 그때 잰 값이 그대로 남습니다.

## 7. 개발 결과 읽기

먼저 어느 칸이 설정을 가르는지 봅니다.
서른여섯 줄에서 값이 한 가지뿐인 칸은 설정을 고르는 데 쓸 수 없습니다."""),
        code(COLUMN_VALUES),
        md("""**결과 읽기** — 라벨 줄 아래 칸 여섯 개가 한 줄씩 나옵니다.
줄 `recall_at_3`·`recall_at_5`·`recall_at_50`은 값이 `[1.0]` 하나뿐입니다.
줄 `precision_at_5`도 값이 `[0.2]` 하나뿐입니다.
질문마다 정답 부모가 한 건이라 보고 자리 5 정밀도의 가장 큰 값이 0.2입니다.
줄 `ndcg_at_5`는 값이 세 가지이고 `chunk_precision_at_5`는 열 가지가 넘습니다.

값이 한 가지인 칸으로는 설정을 고를 수 없습니다.
nDCG 자리 5에서 가장 큰 값 1.0을 가진 줄은 서른여섯 줄 가운데 열 줄입니다.
그래서 값이 가장 잘게 갈린 문서 청크 정밀도 자리 5로 고릅니다.

다음 셀은 손잡이 값별로 평균을 내는 함수 둘입니다."""),
        new_funcs(KNOB_FUNCS),
        md("""정의 셀이라 출력이 없습니다.
첫 함수는 손잡이 값이 같은 줄만 모아 지표 칸의 평균을 냅니다.
가중치 여섯 가지는 각각 여섯 줄씩이고 관련성 비중도 마찬가지입니다.
둘째 함수는 손잡이 하나의 값들을 한 줄씩 출력합니다.

다음 셀이 손잡이별 평균을 한 표로 냅니다."""),
        code(KNOB_TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 열두 줄이 나옵니다. 위 여섯 줄이 가중치입니다.
줄 `가중치 | [1.0, 0.0]`이 뜻 검색만 쓴 줄이고 정밀도 평균이 여섯 줄 가운데 가장 낮습니다.
그 줄의 nDCG 자리 5 평균 `0.9681`도 여섯 줄 가운데 가장 낮습니다.
맨 아래 `가중치 | [0.0, 1.0]` 줄은 nDCG 자리 5 평균이 `1.0`입니다.

아래 여섯 줄이 관련성 비중입니다. 비중이 내려갈수록 정밀도 평균도 내려갑니다.
줄 `관련성 비중 | 1.0`이 가장 높고 `관련성 비중 | 0.0`이 가장 낮습니다.
왼쪽 정밀도 칸의 값은 실행마다 소수 둘째 자리에서 조금 흔들립니다.

## 8. 설정 한 벌 고르기

이제 문서 청크 정밀도 자리 5가 가장 큰 줄을 고릅니다.
값이 같은 줄이 여럿이면 앞에 있는 줄을 둡니다. 코드가 정한 규칙입니다."""),
        code(PICK_BEST),
        md("""**결과 읽기** — `고른 가중치: [0.0, 1.0]`과 `고른 관련성 비중: 1.0`이 보입니다.
줄 `그 줄의 문서 청크 정밀도 자리 5:` 뒤의 값이 서른여섯 줄 가운데 가장 큽니다.
줄 `그 줄의 nDCG 자리 5: 1.0`은 열다섯 질문 모두 정답 부모가 1위였다는 뜻입니다.
가중치 `[0.0, 1.0]`은 1차 후보를 낱말 검색 순위만으로 골랐다는 뜻입니다.
관련성 비중 `1.0`은 MMR이 닮음을 빼지 않고 질문과의 유사도만 봤다는 뜻입니다.

## 9. 시험 열다섯 문항 한 번

여기까지 시험 문항은 한 번도 열지 않았습니다.
설정을 다 골랐으니 이제 한 번 엽니다.
실행 전에 예상해 봅니다. 개발에서 잰 값보다 조금 낮을 것입니다."""),
        code(PREPARE_TEST),
        md("""**결과 읽기** — `시험 질문 수: 15`가 보이고 첫 시험 질문이 한 줄 나옵니다.
여기까지 임베딩 요청은 서른한 번입니다.

다음 셀이 고른 설정 한 벌만 시험 문항에 적용하고 기록을 저장합니다."""),
        code(RUN_TEST),
        md("""**결과 읽기** — 라벨 줄 아래 칸 여섯 개가 한 줄씩 나옵니다.
줄 `ndcg_at_5 | 1.0 | 0.9754`에서 시험 값이 개발 값보다 낮습니다.
개발 값 `1.0`은 열다섯 질문 모두 정답 부모가 1위라는 뜻입니다.
줄 `chunk_precision_at_5`도 시험 쪽이 조금 낮습니다.
재현율 세 칸과 `precision_at_5`는 두 묶음에서 같은 값입니다.

개발 열다섯 문항에 맞춰 고른 설정이 새 문항에서 그대로 나오지는 않았습니다.
시험 값 `0.9754`는 한 질문에서 정답 부모가 2위로 내려갔을 때 나오는 값입니다.
이것이 시험 문항을 마지막까지 열지 않는 까닭입니다.

## 10. 끝까지 이어 붙인 실행 한 번

마지막으로 고른 설정으로 찾은 글을 모델에 넣어 답을 씁니다.
질문은 개발 문항 `Q002` 하나입니다.
이 한 번은 단계가 이어지는지 보는 실행이고 답 품질은 재지 않습니다."""),
        code(SMOKE_SEARCH),
        md("""**결과 읽기** — 줄 `고른 질문: Q002`와 그 질문의 정답 부모 문서 ID가 나옵니다.
줄 `보고 자리 다섯 개의 문서 청크 ID:` 아래 다섯 개가 모두 `E01`로 시작합니다.
줄 `그 문서 청크의 부모 문서 차례: ['E01']`이라 부모는 한 건뿐입니다.

다음 셀은 앞자리 세 개의 본문과 출처 표시를 이어 붙입니다."""),
        code(SMOKE_CONTEXT),
        md("""**결과 읽기** — `넣을 자리 수: 3`과 `첫 출처 표시: [E01 p.3]`이 보입니다.
줄 `넣을 글의 길이: 490`은 모델에 넣을 글의 글자 수입니다.
출처 표시는 Ch 8에서 쓴 `[문서ID p.쪽]` 모양 그대로입니다.

다음 셀이 이 챕터에서 답을 쓰는 모델을 부르는 한 자리입니다."""),
        code(SMOKE_ANSWER),
        md("""**결과 읽기** — 줄 `답:` 뒤에 한국어 답 한 문단과 출처 표시가 나옵니다.
답에 적힌 출처가 넣은 자리 안에 있는지 눈으로 확인합니다.
모델이 쓴 문장은 실행마다 달라질 수 있어 낱말을 확인 줄로 보지 않았습니다.

다음 셀은 이 실행의 설정을 적습니다."""),
        code(SMOKE_SETTINGS),
        md("""**결과 읽기** — 줄 `통합 실행 설정:` 뒤에 칸 열 개가 나옵니다.
칸 `dimensions`는 `256`이고 실제 벡터의 숫자 개수를 센 값입니다.
칸 `chat`은 `gpt-5.4-mini`이고 칸 `reranker`는 `None`입니다.
이 실행에서는 07·08절 리랭커를 쓰지 않았습니다.

다음 셀이 마지막 기록 파일을 씁니다."""),
        code(SMOKE_SAVE),
        md("""**결과 읽기** — `기록한 칸 수: 11`이 보입니다.
칸 `retrieval_metrics`에 `None`을 적어 검색 지표를 재지 않았음을 남깁니다.
칸 `generation_evaluation`에는 아직 평가하지 않았다는 표시와 다음 챕터 이름을 적습니다.

## 정리

1. 설정 서른여섯 벌에서 지표 칸 여섯 개 가운데 넷은 값이 한 가지뿐이었습니다.
2. 고른 설정의 nDCG 자리 5는 개발에서 1.0이었고 시험에서 0.9754였습니다.
3. 기록 파일 세 개와 사본 세 개를 남겨 어떤 입력·설정으로 잰 값인지 다시 볼 수 있습니다.

다음 13절은 이 챕터의 실습입니다.
여기서 만든 함수들을 한 상황에 모으고 가중치 한 자리만 바꿔 함께 실행합니다."""),
    ]


if __name__ == "__main__":
    path = write_notebook(LAB, "12", "12-종합-튜닝과-실험-로그", "experiment", cells())
    print("wrote", path)
