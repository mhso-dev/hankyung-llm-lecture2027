"""Ch 14 RAG 패턴 확장 — 앞 절과 앞 챕터에서 배운 함수를 모아 둔 도구 파일입니다.

뒤 절 노트북은 이 파일의 함수를 `from rag_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
노트북에서 만든 이름(doc_ids, doc_vectors, embedding_model, model 등)을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.

파일은 두 구역으로 나눕니다.
- Ch 12·Ch 11 검색 부품: 01~10절이 가져가는 거리 순위·출력·자리 세기·순위 합치기 함수. 본문은 Ch 12 도구 파일
  (labs/part3/ch12-retrieval-tuning/notebooks/rag_tools.py)과 같고, 실습 폴더가 달라 그 파일을 바로 가져올 수 없어
  여기에 옮겨 두었습니다. 벡터 계산은 NumPy로 합니다.
- 01~06절 함수: 이 챕터에서 배운 함수 가운데 뒤 절이 코드 그대로 다시 쓰는 것
"""

import numpy as np


# ======================================================================
# Ch 12·Ch 11 검색 부품
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


# Ch 12 01절에서 배웠습니다 — 질문 벡터 하나를 문서 벡터 모두와 코사인 거리로 재어, 거리가 작은 순서로 앞 top_count개를 냅니다
# 거리는 소수 둘째 자리까지 남기고, 차례는 반올림하기 전 거리로 정합니다
def rank_by_distance(question_vector, doc_vectors, doc_ids, top_count):
    distances = []
    for doc_vector in doc_vectors:
        distances.append(cosine_distance(question_vector, doc_vector))
    hit_list = []
    # np.argsort(목록)는 값이 작은 것부터 그 자리 번호를 차례로 담은 배열을 냅니다
    for position in np.argsort(distances)[:top_count]:
        hit_list.append({"doc_id": doc_ids[position], "거리": round(distances[position], 2)})
    return hit_list


# Ch 12 05절에서 배웠습니다 — 순위 목록을 순위·문서 ID·값 세 칸으로 출력합니다(값 칸 이름을 인자로 받습니다)
def print_ranked(hit_list, value_name):
    print("순위 | 문서 ID |", value_name)
    for rank_number in range(len(hit_list)):
        row = hit_list[rank_number]
        print(rank_number + 1, "|", row["doc_id"], "|", row[value_name])


# Ch 11 01절에서 배웠습니다 — 검색 항목에서 문서 ID를 순서대로 모으고 처음 나온 것만 남긴 고유 문서 목록을 만듭니다
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


# ======================================================================
# 01~06절 함수
# ======================================================================


# 01절에서 배웠습니다 — 재작성 머리글과 대화 기록과 마지막 질문을 한 글로 이어 붙입니다
# 01절 판은 바깥 이름 rewrite_head를 읽었고, 이 판은 재작성 머리글을 첫 인자로 받습니다
def build_rewrite_prompt(rewrite_head, history_lines, question):
    history_text = ""
    for line in history_lines:
        history_text = history_text + line + "\n"
    prompt_text = rewrite_head + "대화 기록:\n" + history_text
    prompt_text = prompt_text + "\n마지막 질문: " + question
    return prompt_text


# 01절에서 배웠습니다 — 글 안에 찾는 낱말이 있는지만 봅니다(답이 맞는지 재는 함수가 아닙니다)
def keeps_word(sentence, word):
    found = word in sentence
    return found


# 01절에서 배웠습니다 — 앞자리 문서의 원문과 문서 ID를 이어 답 만들기 프롬프트를 만듭니다
# 01절 판은 바깥 이름 answer_head·text_by_doc을 읽었고, 이 판은 답 머리글을 첫 인자로, 문서 ID → 글 짝을 넷째 인자로 받습니다
def build_answer_prompt(answer_head, question, hit_list, text_by_doc):
    material = ""
    for hit in hit_list:
        doc_id = hit["doc_id"]
        material = material + "[" + doc_id + "] " + text_by_doc[doc_id] + "\n"
    prompt_text = answer_head + "질문: " + question + "\n\n자료:\n" + material
    return prompt_text


# 01절에서 배웠습니다 — 실행 한 번을 칸 넷(실행·검색에 쓴 질문·첫 자리 문서·정답 자리)의 기록 한 줄로 만듭니다
# 03절과 05~10절은 견주는 칸이 달라 절마다 그 절 칸에 맞춘 판을 노트북에 새로 적습니다
def run_row(run_name, question_text, found_ids, place):
    row = {"실행": run_name}
    row["검색에 쓴 질문"] = question_text
    row["첫 자리 문서"] = found_ids[0]
    row["정답 자리"] = place
    return row


# 02절에서 배웠습니다 — 모델이 보낸 글을 줄로 나누고 빈 줄을 뺀 목록을 만듭니다
def split_lines(reply_text):
    lines = []
    for line in reply_text.split("\n"):
        clean_line = line.strip()
        if clean_line != "":
            lines.append(clean_line)
    return lines


# 02절에서 배웠습니다 — 질문 하나를 벡터로 바꿔 거리 순서의 고유 문서 ID 목록을 만듭니다(부를 때마다 임베딩 요청 1번)
# 02절 판은 바깥 이름 embedding_model·doc_vectors·doc_ids·top_all을 읽었고, 이 판은 그 넷을 인자로 받습니다
def search_ids(embedding_model, question, doc_vectors, doc_ids, top_count):
    question_vector = embedding_model.embed_query(question)
    hit_list = rank_by_distance(question_vector, doc_vectors, doc_ids, top_count)
    found_ids = unique_doc_ids(hit_list)
    return found_ids


# 02절에서 배웠습니다 — 변형 질문을 받을 머리글 세 줄과 원 질문을 한 글로 이어 붙입니다
# 02절 판은 바깥 이름 variant_count를 읽었고, 이 판은 만들 변형 질문 수를 둘째 인자로 받습니다
def build_variant_prompt(question, variant_count):
    variant_head = "아래 질문과 같은 것을 묻되 표현과 관점을 달리한 검색 질문을 "
    variant_head = variant_head + str(variant_count) + "줄 적으세요.\n"
    variant_head = variant_head + "한 줄에 질문 하나만 적고 번호나 기호를 붙이지 마세요.\n"
    variant_head = variant_head + "질문이 가리키는 대상과 조건은 그대로 두세요.\n\n"
    prompt_text = variant_head + "질문: " + question
    return prompt_text


# 05절에서 배웠습니다 — 줄 목록을 사이에 빈칸 하나를 두고 한 글로 이어 붙입니다
def join_lines(lines):
    joined_text = ""
    for line in lines:
        if joined_text == "":
            joined_text = line
        else:
            joined_text = joined_text + " " + line
    return joined_text


# 05절에서 배웠습니다 — 가상 문서를 받을 머리글 네 줄과 원 질문을 한 글로 이어 붙입니다
# 05절 판은 바깥 이름 doc_sentences를 읽었고, 이 판은 가상 문서의 문장 수를 둘째 인자로 받습니다
def build_hyde_prompt(question, doc_sentences):
    hyde_head = "아래 질문에 답할 법한 도서관 안내문을 지어 쓰세요.\n"
    hyde_head = hyde_head + "물음표로 끝나는 질문이 아니라 안내문 문장으로 " + str(doc_sentences) + "문장 적으세요.\n"
    hyde_head = hyde_head + "지어낸 숫자는 넣지 말고 무엇을 어디에서 하는지만 적으세요.\n"
    hyde_head = hyde_head + "번호나 따옴표를 붙이지 마세요.\n\n"
    prompt_text = hyde_head + "질문: " + question
    return prompt_text


# 06절에서 배웠습니다 — 질문 하나를 벡터로 바꿔 거리 순위 목록(문서 ID와 거리)을 만듭니다(부를 때마다 임베딩 요청 1번)
# 06절 판은 바깥 이름 embedding_model·doc_vectors·doc_ids·top_all을 읽었고, 이 판은 그 넷을 인자로 받습니다
def search_hits(embedding_model, question, doc_vectors, doc_ids, top_count):
    question_vector = embedding_model.embed_query(question)
    hit_list = rank_by_distance(question_vector, doc_vectors, doc_ids, top_count)
    return hit_list


# 06절에서 배웠습니다 — 거리는 작을수록 가까우므로 첫 자리 거리가 기준값보다 크면 다시 검색하기로 정합니다
def needs_retry(top_distance, limit):
    if top_distance > limit:
        return True
    return False


# 06절에서 배웠습니다 — 보정 질문을 받을 머리글 네 줄과 원 질문을 한 글로 이어 붙입니다
# 07절은 답을 고쳐 쓰는 다른 판(답과 근거 두 인자)을 노트북에 따로 적습니다
def build_fix_prompt(question):
    fix_head = "아래 질문을 도서관 안내문에서 찾기 좋은 말로 다시 적으세요.\n"
    fix_head = fix_head + "줄임말과 일상 말을 안내문에서 쓰는 말로 바꾸세요.\n"
    fix_head = fix_head + "새 조건을 보태지 말고 묻는 내용은 그대로 두세요.\n"
    fix_head = fix_head + "물음 한 문장만 적고 번호나 따옴표를 붙이지 마세요.\n\n"
    prompt_text = fix_head + "질문: " + question
    return prompt_text


# 06절에서 배웠습니다 — 다시 검색하기로 한 갈래에서만 모델을 불러 보정 질문을 받고 다시 검색한 횟수를 함께 담습니다
# 06절 판은 바깥 이름 model을 읽었고, 이 판은 답 모델을 첫 인자로 받습니다
def correct_once(model, question, top_distance, limit):
    row = {"보정 질문": question, "다시 검색한 횟수": 0}
    if needs_retry(top_distance, limit):
        fix_prompt = build_fix_prompt(question)
        fix_reply = model.invoke(fix_prompt)
        fix_lines = split_lines(fix_reply.text.strip())
        row["보정 질문"] = fix_lines[0]
        row["다시 검색한 횟수"] = 1
    return row
