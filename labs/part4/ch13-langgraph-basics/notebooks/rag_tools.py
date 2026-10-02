"""Ch 13 LangGraph 기초 — 앞 절과 앞 챕터에서 배운 함수를 모아 둔 도구 파일입니다.

뒤 절 노트북은 이 파일의 함수를 `from rag_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
노트북에서 만든 이름(chunk_ids, chunk_vectors, kiwi, bm25_model 등)을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.

파일은 두 구역으로 나눕니다.
- 01~06절 함수: 이 챕터에서 배운 출력 함수와 노드 가운데 뒤 절이 코드 그대로 다시 쓰는 것
- Ch 12 검색 부품: 07·08절이 가져가는 Ch 12 함수. 본문은 Ch 12 도구 파일(labs/part3/ch12-retrieval-tuning/notebooks/rag_tools.py)과 같고,
  실습 폴더가 달라 그 파일을 바로 가져올 수 없어 여기에 옮겨 두었습니다. 벡터 계산은 NumPy로 합니다.
"""

import numpy as np


# ======================================================================
# 01~06절 함수
# ======================================================================


# 01절에서 배웠습니다 — 상태의 칸 셋(질문·검색어·실행 흔적)을 라벨 줄 아래에 한 줄씩 출력합니다
# 03절부터는 칸 구성이 달라 절마다 그 절 칸에 맞춘 판을 노트북에 새로 적습니다
def print_state(label, state):
    print(label)
    print("질문 칸 |", state["question"])
    print("검색어 칸 |", state["query"])
    print("실행 흔적 칸 |", state["trace"])


# 02절에서 배웠습니다 — 질문 칸의 앞뒤 빈칸을 없애고 실행 흔적에는 자기 이름만 담아 냅니다
# 01절 판은 앞 실행 흔적까지 함께 담아 냈고, 02절부터 칸의 규칙이 이어 붙이도록 이 판을 씁니다
def normalize(state):
    clean_question = state["question"].strip()
    return {"question": clean_question, "trace": ["normalize"]}


# 02절에서 배웠습니다 — 물음표와 맺음말을 지워 검색어를 만들고 실행 흔적에는 자기 이름만 담아 냅니다
def make_query(state):
    without_mark = state["question"].replace("?", "")
    plain = without_mark.replace("인가요", "")
    return {"query": plain.strip(), "trace": ["make_query"]}


# 03절에서 배웠습니다 — 자료가 넉넉할 때 지날 노드로 답 칸과 자기 이름을 담아 냅니다
def make_answer(state):
    return {"answer": "찾은 자료로 답을 만듭니다", "trace": ["make_answer"]}


# 03절에서 배웠습니다 — 자료가 모자랄 때 지날 노드로 답 칸과 자기 이름을 담아 냅니다
# 08절 실습은 답 칸 대신 메시지 칸에 담는 판을 노트북에 따로 적습니다
def ask_more(state):
    return {"answer": "자료를 더 찾아야 합니다", "trace": ["ask_more"]}


# ======================================================================
# Ch 12 검색 부품 (07·08절)
# ======================================================================


# Ch 5 02절에서 배웠습니다 — 두 벡터의 코사인 유사도(점곱을 두 길이의 곱으로 나눈 값)를 NumPy로 계산합니다
def cosine_similarity(first, second):
    first_array = np.array(first)
    second_array = np.array(second)
    # 기호 @는 두 배열의 점곱을, np.linalg.norm(배열)은 벡터의 길이를 계산합니다
    dot = first_array @ second_array
    length_product = np.linalg.norm(first_array) * np.linalg.norm(second_array)
    return dot / length_product


# Ch 12 01절에서 배웠습니다 — 코사인 유사도를 가장 큰 값 1에서 빼 코사인 거리(작을수록 가까움)로 바꿉니다
# Ch 12 01절 판은 바깥 이름 similarity_top을 읽었고, 이 판은 같은 값 1을 함수 안에서 정합니다
def cosine_distance(first, second):
    similarity_top = 1
    similarity = cosine_similarity(first, second)
    return similarity_top - similarity


# Ch 12 01절에서 배웠습니다 — 질문 벡터 하나를 문서 벡터 모두와 코사인 거리로 재어, 거리가 작은 순서로 앞 top_count개를 반환합니다
# 07·08절은 이 함수를 바로 부르지 않고 아래 rank_chunks_by_distance() 안에서만 씁니다
def rank_by_distance(question_vector, doc_vectors, doc_ids, top_count):
    distances = []
    for doc_vector in doc_vectors:
        distances.append(cosine_distance(question_vector, doc_vector))
    hit_list = []
    # np.argsort(목록)는 값이 작은 것부터 그 자리 번호를 차례로 담은 배열을 반환합니다
    for position in np.argsort(distances)[:top_count]:
        hit_list.append({"doc_id": doc_ids[position], "거리": round(distances[position], 2)})
    return hit_list


# Ch 12 04절에서 배웠습니다 — 형태소 분석기로 글을 나눠 남길 품사 표시에 든 형태소만 검색 낱말 목록으로 반환합니다
# Ch 12 04절 판은 바깥 이름 kiwi·keep_tags를 읽었고, 이 판은 분석기를 첫 인자로, 남길 품사 표시 목록을 셋째 인자로 받습니다
def kiwi_terms(kiwi, text, keep_tags):
    terms = []
    for token in kiwi.tokenize(text):
        # 조사와 어미는 품사 표시가 목록에 없어 빠집니다
        if token.tag in keep_tags:
            terms.append(token.form)
    return terms


# Ch 12 04절에서 배웠습니다 — BM25 모델로 질문 검색 낱말의 점수를 내어, 점수가 큰 순서로 앞 top_count개를 반환합니다(점수가 같으면 문서 ID 차례)
# 07·08절은 이 함수를 바로 부르지 않고 아래 rank_chunks_by_bm25() 안에서만 씁니다
def rank_by_bm25(bm25_model, question_terms, doc_ids, top_count):
    scores = bm25_model.get_scores(question_terms)
    pairs = []
    for i in range(len(doc_ids)):
        # 점수에 음수를 붙이면 sorted가 큰 점수를 앞으로 보냅니다
        pairs.append((0 - scores[i], doc_ids[i]))
    hit_list = []
    for pair in sorted(pairs):
        hit_list.append({"doc_id": pair[1], "점수": round(0 - pair[0], 2)})
    return hit_list[:top_count]


# Ch 12 06절에서 배웠습니다 — 순위 목록 여러 개를 받아 문서마다 자리 몫(가중치 ÷ (순위 상수 + 자리))을 더한 합친 점수를 냅니다
# Ch 12 06절 판은 바깥 이름 rank_constant를 읽었고, 이 판은 순위 상수를 셋째 인자로 받습니다
def fuse_scores(ranking_list, weight_list, rank_constant):
    scores = {}
    for list_index in range(len(ranking_list)):
        ranking = ranking_list[list_index]
        # 자리 번호는 1부터 세고 앞자리일수록 나누는 수가 작아 몫이 큽니다
        for position in range(len(ranking)):
            doc_id = ranking[position]
            share = weight_list[list_index] / (rank_constant + position + 1)
            scores[doc_id] = scores.get(doc_id, 0.0) + share
    return scores


# Ch 12 06절에서 배웠습니다 — 합친 점수가 큰 순서로 문서 ID 목록을 만듭니다(합친 점수가 같으면 문서 ID 차례)
# Ch 12 06절 판은 바깥 이름 rank_constant를 읽었고, 이 판은 순위 상수를 셋째 인자로 받아 fuse_scores()에 넘깁니다
def fuse_rank(ranking_list, weight_list, rank_constant):
    scores = fuse_scores(ranking_list, weight_list, rank_constant)
    pairs = []
    for doc_id in scores:
        # 점수에 음수를 붙이면 sorted가 큰 점수를 앞으로 보냅니다
        pairs.append((0 - scores[doc_id], doc_id))
    fused_ids = []
    for pair in sorted(pairs):
        fused_ids.append(pair[1])
    return fused_ids


# Ch 12 01절에서 배웠습니다 — 질문 벡터 하나를 문서 청크 벡터 모두와 코사인 거리로 재어, 거리가 작은 순서로 앞 top_count개를 반환합니다
# Ch 12 07절부터 후보 단위가 문서 청크라 rank_by_distance()로 순위를 매기고 칸 이름만 chunk_id로 바꿉니다
def rank_chunks_by_distance(question_vector, chunk_vectors, chunk_ids, top_count):
    hit_list = []
    for hit in rank_by_distance(question_vector, chunk_vectors, chunk_ids, top_count):
        # 칸 doc_id에 든 값이 문서 청크 ID라 그 값을 칸 chunk_id로 옮깁니다
        hit_list.append({"chunk_id": hit["doc_id"], "거리": hit["거리"]})
    return hit_list


# Ch 12 04절에서 배웠습니다 — BM25 모델로 질문 검색 낱말의 점수를 내어, 점수가 큰 순서로 앞 top_count개를 반환합니다(점수가 같으면 문서 청크 ID 차례)
# Ch 12 07절부터 후보 단위가 문서 청크라 rank_by_bm25()로 순위를 매기고 칸 이름만 chunk_id로 바꿉니다
def rank_chunks_by_bm25(bm25_model, question_terms, chunk_ids, top_count):
    hit_list = []
    for hit in rank_by_bm25(bm25_model, question_terms, chunk_ids, top_count):
        hit_list.append({"chunk_id": hit["doc_id"], "점수": hit["점수"]})
    return hit_list


# Ch 11 01절에서 배웠습니다 — 검색 항목에서 문서 청크 ID를 순서대로 모으고 처음 나온 것만 남긴 목록을 반환합니다
# Ch 11 01절 unique_doc_ids()와 같은 모양이고, Ch 12 07절부터 보는 칸이 chunk_id입니다
def unique_chunk_ids(hit_list):
    found_ids = []
    for hit in hit_list:
        if hit["chunk_id"] not in found_ids:
            found_ids.append(hit["chunk_id"])
    return found_ids


# Ch 12 07절에서 배웠습니다 — 문서 청크 ID 목록을 부모 문서 ID 목록으로 바꾸고 처음 나온 것만 남깁니다
# Ch 12 07절 판은 바깥 이름 parent_by_chunk를 읽었고, 이 판은 문서 청크 ID → 부모 문서 ID 짝을 둘째 인자로 받습니다
def parent_ids_of(found_chunk_ids, parent_by_chunk):
    parent_ids = []
    for chunk_id in found_chunk_ids:
        parent_id = parent_by_chunk[chunk_id]
        # 여러 문서 청크가 같은 부모를 가리키면 처음 나온 자리만 남깁니다
        if parent_id not in parent_ids:
            parent_ids.append(parent_id)
    return parent_ids
