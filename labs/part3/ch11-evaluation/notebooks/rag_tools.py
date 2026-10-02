"""Ch 11 평가 기초 — 앞 절과 앞 챕터에서 배운 함수를 모아 둔 도구 파일입니다.

뒤 절 노트북은 이 파일의 함수를 `from rag_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
노트북에서 만든 이름(store, candidate_count 등)을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""

import math

from pypdf import PdfReader
from langchain_core.documents import Document


# Ch 9 02절에서 배웠습니다 — PDF 경로와 문서 이름을 받아, 쪽마다 본문과 메타데이터를 담은 Document 목록을 반환합니다
def load_pdf_pages(pdf_path, doc_id):
    reader = PdfReader(pdf_path)
    page_documents = []
    page_number = 1
    for page in reader.pages:
        metadata = {"doc_id": doc_id, "page": page_number, "source": doc_id + ".pdf"}
        page_document = Document(page_content=page.extract_text(), metadata=metadata)
        page_documents.append(page_document)
        page_number = page_number + 1
    return page_documents


# 01절에서 배웠습니다 — 검색 항목에서 문서 ID를 순서대로 모으고 처음 나온 것만 남긴 고유 문서 목록을 반환합니다
def unique_doc_ids(hit_list):
    doc_ids = []
    for hit in hit_list:
        if hit["doc_id"] not in doc_ids:
            doc_ids.append(hit["doc_id"])
    return doc_ids


# 01절에서 배웠습니다 — 고유 문서 목록에서 정답 문서 ID가 몇 번째 자리인지 찾습니다(찾지 못하면 0)
def find_gold_rank(doc_ids, gold_doc_ids):
    gold_rank = 0
    for position in range(len(doc_ids)):
        if doc_ids[position] in gold_doc_ids:
            gold_rank = position + 1
            break
    return gold_rank


# 02절에서 배웠습니다 — 고유 문서 목록을 자르는 자리에서 자르고 정답 문서가 들어온 비율(재현율)을 냅니다
def recall_at(doc_ids, gold_doc_ids, cutoff):
    top_ids = doc_ids[:cutoff]
    found_count = 0
    for gold_id in gold_doc_ids:
        if gold_id in top_ids:
            found_count = found_count + 1
    return found_count / len(gold_doc_ids)


# 02절에서 배웠습니다 — 질문마다 낸 점수를 같은 무게로 평균해 소수 셋째 자리까지 남깁니다
def mean_score(score_list):
    total = 0
    for score in score_list:
        total = total + score
    return round(total / len(score_list), 3)


# 02절에서 배웠습니다 — 검색 결과를 순위·문서 ID·쪽 세 칸의 후보 목록으로 바꿉니다
def make_candidate_list(hit_documents):
    candidates = []
    rank_number = 1
    for hit in hit_documents:
        candidates.append({"doc_id": hit.metadata["doc_id"], "page": hit.metadata["page"], "rank": rank_number})
        rank_number = rank_number + 1
    return candidates


# 03절에서 배웠습니다 — 앞부분에 든 정답 문서 자리를 세고 자르는 자리로 나눕니다(정밀도)
def precision_at(doc_ids, gold_doc_ids, cutoff):
    top_ids = doc_ids[:cutoff]
    found_count = 0
    for gold_id in gold_doc_ids:
        if gold_id in top_ids:
            found_count = found_count + 1
    return found_count / cutoff


# 04절에서 배웠습니다 — 자리 번호를 받아 그 자리의 무게를 냅니다(자리 1이 가장 크고 뒤로 갈수록 작아집니다)
def rank_weight(rank):
    return 1 / math.log2(rank + 1)


# 04절에서 배웠습니다 — 앞 자리부터 정답 문서를 만날 때마다 그 자리의 무게를 더해 무게 합을 냅니다
def dcg_at(doc_ids, gold_doc_ids, cutoff):
    top_ids = doc_ids[:cutoff]
    total = 0
    for position in range(len(top_ids)):
        if top_ids[position] in gold_doc_ids:
            total = total + rank_weight(position + 1)
    return total


# 04절에서 배웠습니다 — 정답 문서를 앞자리부터 빈틈없이 놓았을 때의 무게 합을 냅니다
def ideal_dcg(gold_count, cutoff):
    best_count = gold_count
    if best_count > cutoff:
        best_count = cutoff
    total = 0
    for position in range(best_count):
        total = total + rank_weight(position + 1)
    return total


# 04절에서 배웠습니다 — 무게 합을 가장 좋은 무게 합으로 나눠 0에서 1 사이 값(nDCG)으로 맞춥니다
def ndcg_at(doc_ids, gold_doc_ids, cutoff):
    found_score = dcg_at(doc_ids, gold_doc_ids, cutoff)
    best_score = ideal_dcg(len(gold_doc_ids), cutoff)
    return found_score / best_score


# 05절에서 배웠습니다 — 질문을 검색해 문서 ID 중복을 뺀 뒤 앞에서 count개만 남긴 목록을 냅니다
# 05절 판은 바깥 이름 store·candidate_count를 읽었고, 이 판은 벡터스토어를 첫 인자로, 후보 개수를 넷째 인자로 받습니다
def search(store, question, count, candidate_count):
    hit_documents = store.similarity_search(question, k=candidate_count)
    candidate_list = make_candidate_list(hit_documents)
    doc_ids = unique_doc_ids(candidate_list)
    picked = []
    for doc_id in doc_ids[:count]:
        picked.append({"doc_id": doc_id})
    return picked


# 05절에서 배웠습니다 — 담아 둔 줄에서 지표 한 칸만 꺼내 질문 평균을 냅니다
def group_mean(rows, metric):
    scores = []
    for row in rows:
        scores.append(row[metric])
    return mean_score(scores)
