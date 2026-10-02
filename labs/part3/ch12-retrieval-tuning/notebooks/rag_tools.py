"""Ch 12 검색 품질과 튜닝 — 앞 절과 앞 챕터에서 배운 함수를 모아 둔 도구 파일입니다.

뒤 절 노트북은 이 파일의 함수를 `from rag_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
노트북에서 만든 이름(doc_ids, doc_vectors, cur, kiwi, bm25_model 등)을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.

파일은 두 구역으로 나눕니다.
- 01~06절 함수: 교육용 문서 12개·질문 8개(core 벌)로 배운 거리·지표·데이터베이스·낱말 검색·순위 합치기 함수
- 07~13절 함수: 문서 청크 175개·질문 30개(advanced 벌)로 배운 함수와, 01~06절 함수를 문서 청크에 쓰는 판,
  07~13절이 가져가는 앞 챕터 함수(Ch 8 조각 수 세기·Ch 11 정밀도와 nDCG)
"""

import math

import numpy as np


# ======================================================================
# 01~06절 함수
# ======================================================================


# Ch 5 02절에서 배웠습니다 — 두 벡터의 코사인 유사도(점곱을 두 길이의 곱으로 나눈 값)를 NumPy로 계산합니다
def cosine_similarity(first, second):
    first_array = np.array(first)
    second_array = np.array(second)
    # 기호 @는 두 배열의 점곱을, np.linalg.norm(배열)은 벡터의 길이를 계산합니다
    dot = first_array @ second_array
    length_product = np.linalg.norm(first_array) * np.linalg.norm(second_array)
    return dot / length_product


# 01절에서 배웠습니다 — 코사인 유사도를 가장 큰 값 1에서 빼 코사인 거리(작을수록 가까움)로 바꿉니다
# 01절 판은 바깥 이름 similarity_top을 읽었고, 이 판은 같은 값 1을 함수 안에서 정합니다
def cosine_distance(first, second):
    similarity_top = 1
    similarity = cosine_similarity(first, second)
    return similarity_top - similarity


# 01절에서 배웠습니다 — 질문 벡터 하나를 문서 벡터 모두와 코사인 거리로 재어, 거리가 작은 순서로 앞 top_count개를 반환합니다
# 01절 판은 문서 ID 목록과 거리 목록을 받아 차례만 매겼고, 이 판은 질문 벡터·문서 벡터 목록·문서 ID 목록을 받아 거리까지 잽니다
def rank_by_distance(question_vector, doc_vectors, doc_ids, top_count):
    distances = []
    for doc_vector in doc_vectors:
        distances.append(cosine_distance(question_vector, doc_vector))
    hit_list = []
    # np.argsort(목록)는 값이 작은 것부터 그 자리 번호를 차례로 담은 배열을 반환합니다
    for position in np.argsort(distances)[:top_count]:
        hit_list.append({"doc_id": doc_ids[position], "거리": round(distances[position], 2)})
    return hit_list


# Ch 11 01절에서 배웠습니다 — 검색 항목에서 문서 ID를 순서대로 모으고 처음 나온 것만 남긴 고유 문서 목록을 반환합니다
def unique_doc_ids(hit_list):
    doc_ids = []
    for hit in hit_list:
        if hit["doc_id"] not in doc_ids:
            doc_ids.append(hit["doc_id"])
    return doc_ids


# Ch 11 01절에서 배웠습니다 — 고유 문서 목록에서 정답 문서 ID가 몇 번째 자리인지 찾습니다(찾지 못하면 0)
def find_gold_rank(doc_ids, gold_doc_ids):
    gold_rank = 0
    for position in range(len(doc_ids)):
        if doc_ids[position] in gold_doc_ids:
            gold_rank = position + 1
            break
    return gold_rank


# Ch 11 02절에서 배웠습니다 — 고유 문서 목록을 자르는 자리에서 자르고 정답 문서가 들어온 비율(재현율)을 냅니다
def recall_at(doc_ids, gold_doc_ids, cutoff):
    top_ids = doc_ids[:cutoff]
    found_count = 0
    for gold_id in gold_doc_ids:
        if gold_id in top_ids:
            found_count = found_count + 1
    return found_count / len(gold_doc_ids)


# Ch 11 02절에서 배웠습니다 — 질문마다 낸 점수를 같은 무게로 평균해 소수 셋째 자리까지 남깁니다
def mean_score(score_list):
    total = 0
    for score in score_list:
        total = total + score
    return round(total / len(score_list), 3)


# 02절에서 배웠습니다 — 검색 SQL로 질문 벡터 하나를 검색해 문서 ID와 코사인 거리 목록을 반환합니다
# 02절 판은 바깥 이름 cur·search_sql을 읽었고, 이 판은 커서와 검색 SQL을 앞의 두 인자로 받습니다
def run_search(cur, search_sql, question_vector, top_count):
    # 벡터를 글로 바꿔 %s 자리에 값으로 넘깁니다
    vector_text = str(question_vector)
    cur.execute(search_sql, (vector_text, vector_text, top_count))
    hit_list = []
    for row in cur.fetchall():
        hit_list.append({"doc_id": row[0], "거리": round(row[1], 2)})
    return hit_list


# 02절에서 배웠습니다 — 검색 결과를 순위·문서 ID·코사인 거리 세 칸으로 출력합니다
def print_hits(hit_list):
    print("순위 | 문서 ID | 코사인 거리")
    for rank_number in range(len(hit_list)):
        row = hit_list[rank_number]
        print(rank_number + 1, "|", row["doc_id"], "|", row["거리"])


# 02절에서 배웠습니다 — SQL과 넘길 값으로 실행 계획을 받아 표를 어떻게 읽는지 적힌 줄만 반환합니다
# 02절 판은 바깥 이름 cur·search_sql을 읽고 질문 벡터 하나를 받았고, 이 판은 커서·SQL·넘길 값을 인자로 받습니다
def find_scan_line(cur, sql_text, value_tuple):
    cur.execute("EXPLAIN " + sql_text, value_tuple)
    scan_line = ""
    for row in cur.fetchall():
        if "Scan" in row[0]:
            scan_line = row[0]
            break
    return scan_line.strip()


# 02절에서 배웠습니다 — 계획기가 순차 스캔을 고를 수 있는지 여부를 바꾸고 바뀐 값을 반환합니다
# 02절 판은 바깥 이름 cur를 읽었고, 이 판은 커서를 첫 인자로 받습니다
def set_seqscan(cur, setting_value):
    # SET 문장에는 자리표시자를 쓸 수 없어 같은 일을 하는 함수로 값을 넘깁니다
    cur.execute("SELECT set_config('enable_seqscan', %s, false)", (setting_value,))
    cur.execute("SHOW enable_seqscan")
    return cur.fetchone()[0]


# 04절에서 배웠습니다 — 형태소 분석기로 글을 나눠 남길 품사 표시에 든 형태소만 검색 낱말 목록으로 반환합니다
# 04절 판은 바깥 이름 kiwi·keep_tags를 읽었고, 이 판은 분석기를 첫 인자로, 남길 품사 표시 목록을 셋째 인자로 받습니다
def kiwi_terms(kiwi, text, keep_tags):
    terms = []
    for token in kiwi.tokenize(text):
        # 조사와 어미는 품사 표시가 목록에 없어 빠집니다
        if token.tag in keep_tags:
            terms.append(token.form)
    return terms


# 04절에서 배웠습니다 — 낱말 하나가 검색 낱말 목록 여러 개 가운데 몇 개에 들어 있는지(그 낱말이 있는 문서 수) 셉니다
# 04절 판은 바깥 이름 kiwi_corpus를 읽었고, 이 판은 검색 낱말 목록의 목록을 첫 인자로 받습니다
def count_docs_with(corpus, term):
    found_count = 0
    for terms in corpus:
        if term in terms:
            found_count = found_count + 1
    return found_count


# 04절에서 배웠습니다 — BM25 모델로 질문 검색 낱말의 점수를 내어, 점수가 큰 순서로 앞 top_count개를 반환합니다(점수가 같으면 문서 ID 차례)
# 04절 판은 정책 이름과 질문 글을 받고 바깥 이름 bm25_models·doc_ids를 읽었고,
# 이 판은 모델·질문의 검색 낱말 목록·문서 ID 목록을 인자로 받습니다(질문 낱말은 kiwi_terms()로 먼저 만듭니다)
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


# 06절에서 배웠습니다 — 순위 목록 여러 개를 받아 문서마다 자리 몫(가중치 ÷ (순위 상수 + 자리))을 더한 합친 점수를 냅니다
# 06절 판은 바깥 이름 rank_constant를 읽었고, 이 판은 순위 상수를 셋째 인자로 받습니다
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


# 06절에서 배웠습니다 — 합친 점수가 큰 순서로 문서 ID 목록을 만듭니다(합친 점수가 같으면 문서 ID 차례)
# 06절 판은 바깥 이름 rank_constant를 읽었고, 이 판은 순위 상수를 셋째 인자로 받아 fuse_scores()에 넘깁니다
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


# ======================================================================
# 07~13절 함수
# ======================================================================


# 01절에서 배웠습니다 — 질문 벡터 하나를 문서 청크 벡터 모두와 코사인 거리로 재어, 거리가 작은 순서로 앞 top_count개를 반환합니다
# 07절부터 후보 단위가 문서 청크라 01절 rank_by_distance()로 순위를 매기고 칸 이름만 chunk_id로 바꿉니다
def rank_chunks_by_distance(question_vector, chunk_vectors, chunk_ids, top_count):
    hit_list = []
    for hit in rank_by_distance(question_vector, chunk_vectors, chunk_ids, top_count):
        # 칸 doc_id에 든 값이 문서 청크 ID라 그 값을 칸 chunk_id로 옮깁니다
        hit_list.append({"chunk_id": hit["doc_id"], "거리": hit["거리"]})
    return hit_list


# 04절에서 배웠습니다 — BM25 모델로 질문 검색 낱말의 점수를 내어, 점수가 큰 순서로 앞 top_count개를 반환합니다(점수가 같으면 문서 청크 ID 차례)
# 07절부터 후보 단위가 문서 청크라 04절 rank_by_bm25()로 순위를 매기고 칸 이름만 chunk_id로 바꿉니다
def rank_chunks_by_bm25(bm25_model, question_terms, chunk_ids, top_count):
    hit_list = []
    for hit in rank_by_bm25(bm25_model, question_terms, chunk_ids, top_count):
        hit_list.append({"chunk_id": hit["doc_id"], "점수": hit["점수"]})
    return hit_list


# Ch 11 01절에서 배웠습니다 — 검색 항목에서 문서 청크 ID를 순서대로 모으고 처음 나온 것만 남긴 목록을 반환합니다
# Ch 11 01절 unique_doc_ids()와 같은 모양이고, 07절부터 보는 칸이 chunk_id입니다
def unique_chunk_ids(hit_list):
    found_ids = []
    for hit in hit_list:
        if hit["chunk_id"] not in found_ids:
            found_ids.append(hit["chunk_id"])
    return found_ids


# 07절에서 배웠습니다 — 문서 청크 ID 목록을 부모 문서 ID 목록으로 바꾸고 처음 나온 것만 남깁니다
# 07절 판은 바깥 이름 parent_by_chunk를 읽었고, 이 판은 문서 청크 ID → 부모 문서 ID 짝을 둘째 인자로 받습니다
def parent_ids_of(found_chunk_ids, parent_by_chunk):
    parent_ids = []
    for chunk_id in found_chunk_ids:
        parent_id = parent_by_chunk[chunk_id]
        # 여러 문서 청크가 같은 부모를 가리키면 처음 나온 자리만 남깁니다
        if parent_id not in parent_ids:
            parent_ids.append(parent_id)
    return parent_ids


# 08절에서 배웠습니다 — 답할 수 있고 정답 부모 문서 ID가 있는 질문만 남깁니다
def eligible_items(subset):
    picked = []
    for item in subset:
        gold_ids = []
        # 같은 정답 ID가 두 번 적혀 있으면 지표의 나누는 수가 달라져 한 번만 둡니다
        for gold_id in item["gold_doc_ids"]:
            if gold_id not in gold_ids:
                gold_ids.append(gold_id)
        item["gold_doc_ids"] = gold_ids
        if item["answerable"] and len(gold_ids) > 0:
            picked.append(item)
    return picked


# 08절에서 배웠습니다 — 앞자리 문서 청크 가운데 정답 부모 문서에서 나온 것을 세어 보고 자리로 나눕니다(문서 청크 정밀도)
# 08절 판은 바깥 이름 parent_by_chunk를 읽었고, 이 판은 그 짝을 넷째 인자로 받습니다
def chunk_precision_at(found_chunk_ids, gold_doc_ids, cutoff, parent_by_chunk):
    top_ids = found_chunk_ids[:cutoff]
    found_count = 0
    for chunk_id in top_ids:
        # 나누는 수가 보고 자리라 자리를 다 채우지 못하면 값이 내려갑니다
        if parent_by_chunk[chunk_id] in gold_doc_ids:
            found_count = found_count + 1
    return found_count / cutoff


# Ch 8 01절에서 배웠습니다 — 토큰화 규칙으로 글을 조각으로 나눠 조각 수를 셉니다
def count_tokens(encoding, text):
    token_ids = encoding.encode(text)
    return len(token_ids)


# 10절에서 배웠습니다 — 후보 하나가 이미 고른 후보들과 가장 많이 닮은 정도(코사인 유사도의 가장 큰 값)를 냅니다
def similarity_to_chosen(candidate_vectors, chosen, index):
    biggest = 0.0
    for chosen_index in chosen:
        similarity = cosine_similarity(candidate_vectors[index], candidate_vectors[chosen_index])
        if similarity > biggest:
            biggest = similarity
    return biggest


# 10절에서 배웠습니다 — 질문과의 유사도에 관련성 비중을 곱하고, 닮은 정도에 나머지 비중을 곱해 뺀 MMR 점수를 냅니다
# 10절 판은 바깥 이름 similarity_top을 읽었고, 이 판은 같은 값 1을 함수 안에서 정합니다
def mmr_score(question_vector, candidate_vectors, chosen, index, relevance_weight):
    similarity_top = 1
    # 두 비중을 더하면 1이 되므로 나머지 비중은 빼서 만듭니다
    diversity_weight = similarity_top - relevance_weight
    relevance = cosine_similarity(question_vector, candidate_vectors[index])
    biggest = similarity_to_chosen(candidate_vectors, chosen, index)
    return relevance_weight * relevance - diversity_weight * biggest


# 10절에서 배웠습니다 — 아직 고르지 않은 후보 가운데 MMR 점수가 가장 큰 자리를 찾습니다
def best_candidate(question_vector, candidate_vectors, chosen, relevance_weight):
    best_index = -1
    best_value = 0.0
    for index in range(len(candidate_vectors)):
        # 이미 고른 자리는 건너뜁니다
        if index not in chosen:
            value = mmr_score(question_vector, candidate_vectors, chosen, index, relevance_weight)
            if best_index == -1 or value > best_value:
                best_index = index
                best_value = value
    return best_index


# 10절에서 배웠습니다 — 고를 수를 채울 때까지 한 자리씩 고르고 고른 자리 번호 목록을 반환합니다
def mmr(question_vector, candidate_vectors, pick_count, relevance_weight):
    chosen = []
    limit = pick_count
    # 후보보다 많이 고를 수는 없습니다
    if len(candidate_vectors) < pick_count:
        limit = len(candidate_vectors)
    while len(chosen) < limit:
        chosen.append(best_candidate(question_vector, candidate_vectors, chosen, relevance_weight))
    return chosen


# 10절에서 배웠습니다 — 후보 문서 청크 ID 목록에서 MMR로 place개를 골라 고른 문서 청크 ID 목록을 반환합니다
# 10절 판은 바깥 이름 vector_by_chunk를 읽었고, 이 판은 문서 청크 ID → 벡터 짝을 다섯째 인자로 받습니다
def mmr_pick(question_vector, found_chunk_ids, place, relevance_weight, vector_by_chunk):
    found_vectors = []
    for chunk_id in found_chunk_ids:
        found_vectors.append(vector_by_chunk[chunk_id])
    chosen = mmr(question_vector, found_vectors, place, relevance_weight)
    picked = []
    for index in chosen:
        picked.append(found_chunk_ids[index])
    return picked


# Ch 11 03절에서 배웠습니다 — 앞부분에 든 정답 문서 자리를 세고 자르는 자리로 나눕니다(정밀도)
def precision_at(doc_ids, gold_doc_ids, cutoff):
    top_ids = doc_ids[:cutoff]
    found_count = 0
    for gold_id in gold_doc_ids:
        if gold_id in top_ids:
            found_count = found_count + 1
    return found_count / cutoff


# Ch 11 04절에서 배웠습니다 — 자리 번호를 받아 그 자리의 무게를 냅니다(자리 1이 가장 크고 뒤로 갈수록 작아집니다)
def rank_weight(rank):
    return 1 / math.log2(rank + 1)


# Ch 11 04절에서 배웠습니다 — 앞 자리부터 정답 문서를 만날 때마다 그 자리의 무게를 더해 무게 합을 냅니다
def dcg_at(doc_ids, gold_doc_ids, cutoff):
    top_ids = doc_ids[:cutoff]
    total = 0
    for position in range(len(top_ids)):
        if top_ids[position] in gold_doc_ids:
            total = total + rank_weight(position + 1)
    return total


# Ch 11 04절에서 배웠습니다 — 정답 문서를 앞자리부터 빈틈없이 놓았을 때의 무게 합을 냅니다
def ideal_dcg(gold_count, cutoff):
    best_count = gold_count
    if best_count > cutoff:
        best_count = cutoff
    total = 0
    for position in range(best_count):
        total = total + rank_weight(position + 1)
    return total


# Ch 11 04절에서 배웠습니다 — 무게 합을 가장 좋은 무게 합으로 나눠 0에서 1 사이 값(nDCG)으로 맞춥니다
def ndcg_at(doc_ids, gold_doc_ids, cutoff):
    found_score = dcg_at(doc_ids, gold_doc_ids, cutoff)
    best_score = ideal_dcg(len(gold_doc_ids), cutoff)
    return found_score / best_score
