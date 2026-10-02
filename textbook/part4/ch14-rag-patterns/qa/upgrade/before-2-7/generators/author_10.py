"""Ch 14 10절(챕터 끝 실습 절) 노트북 + 본문 생성기 (QUALITY-UPGRADE.md §2·§3·§6·§7-2).

사용:
  python3 author_10.py            → 노트북 + _src 본문을 함께 쓴다
  python3 author_10.py --src-only → 본문 HTML만 다시 쓴다(노트북 출력을 지우지 않는다)

이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
새 절이라 수정 전 원본이 없다. 설명만 고칠 때는 mdpatch.py → run_section.sh --no-exec.

주제: 도서관 상담 창구 한 흐름. 대화 기록 두 줄이 있는 후속 질문 하나를 독립 질문으로 바꾸고,
검색한 뒤 첫 자리 거리가 기준값보다 멀면 한 번만 보정 질문으로 다시 검색하고, 앞 세 자리 원문으로 답을 만든다.
실행 1과 실행 2는 후속 질문 하나만 다르고 대화 기록·기준값·문서·정답 문서·모델이 모두 같다.

## 함께 붙인 앞 절 기능 세 가지 (규격 §7-2 「앞 절 기능 2~3개」, handoff §09→실습 후보 A)

1. 01절 질문 재작성 — `build_rewrite_prompt`와 재작성 머리글(검색 앞을 손봄).
2. 06절 보정 검색 — `needs_retry`·`build_fix_prompt`·`correct_once`와 반복 상한(검색 뒤를 손봄).
3. 01절 답 만들기 — `build_answer_prompt`·답 머리글·`keeps_word`(답을 만드는 자리).
바탕은 Ch 12 01·05절 거리 검색과 Ch 11 01절 자리 세기다.

## 뺀 것과 까닭

- 후보 B(05절 가상 문서 + 07절 근거 검사)를 뺐다. 답 품질 판정이 Ch 15 주제와 가까워 실습 절이
  Ch 15를 앞당겨 가르치는 것처럼 읽힌다. 후보 A는 손보는 자리가 검색 앞과 검색 뒤로 갈라져
  09절 b4 소제목 「어느 자리를 손보는 패턴인가」와 그대로 맞는다.
- 후보 C(02절 변형 질문 + 08절 한 단계 요약)를 뺐다. 요약 셋을 먼저 만들어야 해서 답 모델 요청이
  넷이 되고, 두 기능이 「검색에 넣을 글」과 「자료 미리 묶기」로 성격이 멀어 한 상황으로 묶기 어렵다.
- 03절 하위 질문·04절 넓힌 질문·02절 변형 질문은 모두 01절 재작성과 같은 「검색 앞」 자리라 함께 붙여도
  흐름이 길어지기만 한다. 08절 갈래 요약은 질문을 받기 전 자리라 이 흐름에 들어갈 자리가 없다.
- 09절이 견준 세 패턴(기준선·변형 질문·가상 문서)을 되풀이하지 않는다. 09절은 같은 질문 벌로 셋을
  나란히 견줬고 이 절은 기능 셋을 한 흐름으로 잇는다.

## 요청 수 — 답 모델 다섯 번 · 임베딩 다섯 번 (규격 §7-2 「모델 호출 3~5번」)

실행 1: 재작성 1 + 보정 질문 1 + 답 1 = 답 모델 세 번, 임베딩 두 번.
실행 2: 재작성 1 + 답 1 = 답 모델 두 번, 임베딩 두 번(보정 갈래로 가지 않음).
문서 임베딩 한 번을 더해 서비스 요청은 모두 열 번이다. 예상 비용은 미화 0.01달러 아래다.

## 01~09절에서 그대로 가져온 함수 (이름·인자·코드가 같음)

`dot_product`·`vector_length`·`cosine_similarity`·`cosine_distance`(Ch 12 01절) ·
`rank_by_distance`(Ch 12 05절) · `unique_doc_ids`·`find_gold_rank`(Ch 11 01절) — `author_09.py` 판.
`search_hits`·`needs_retry`·`build_fix_prompt`·`correct_once` — `author_06.py` 판.
`build_rewrite_prompt`·`build_answer_prompt`·`keeps_word`와 머리글 둘 — `author_01.py` 판.
`split_lines` — `author_09.py`(02절) 판. 값도 같다: `similarity_top` 1 · `top_three` 3 · `top_all` 12 ·
`dimensions` 256 · 반복 상한 1 · 답 모델 `gpt-5.4-mini`(`temperature=0`·`reasoning_effort="none"`).

## 가져오지 않은 것

`print_ranked`(순위 표를 보이지 않는다) · `fuse_scores`·`fuse_rank`(목록이 하나라 합칠 것이 없다) ·
`join_lines` · 02·03·04·05절 머리글 넷 · 07절 점수 함수 다섯 · 08절 갈래 함수 넷 ·
09절 패턴 함수 넷. 파일을 쓰지 않으므로 `hashlib`도 쓰지 않는다.

## 이 절이 새로 만든 함수 다섯

`rewrite_question(history_lines, question)` · `write_answer(search_text, hit_list)` —
01절 부품을 함수 하나로 묶은 것. `prepare_search(history_lines, question)`(재작성 → 검색 → 판정 → 보정) ·
`answer_once(history_lines, question)`(마지막 검색 → 답)로 조립 함수를 둘로 나눴다(함수 본문 8줄 상한).
기록 함수 `run_row(run_name, follow_up, result)`는 06절 판에 자리 칸 둘을 더한 것이다.

## 선택한 것과 까닭

1. **거리 기준값을 `0.5`로 다시 잡았다.** 06절 값은 `0.65`였다. 06절은 자료 여덟 질문의 첫 자리 거리
   (탐색 실행에서 0.28~0.60)를 보고 그보다 조금 큰 값을 잡았다. 이 절은 **재작성한 질문**으로 검색하므로
   거리 범위가 다르다. 탐색 실행에서 두 재작성 질문의 첫 자리 거리가 `0.64`와 `0.41`이어서 그 사이인
   `0.5`로 잡았다. 흐름의 두 갈래가 모두 보이게 정한 예이고 무엇을 재서 얻은 기준이 아니다(b4·b7에 적음).
2. **값 바꿔 보기는 후속 질문 하나다.** 기준값을 `0.65`에서 `0.8`로 바꾸는 것은 06절이 이미 한 방법이고
   대화 기록을 빈 목록으로 두는 것은 01절이 이미 한 방법이라 둘 다 겹친다(handoff §09→실습 ②-5).
3. **질문을 손으로 적었다**(규격 §3). 자료의 여덟 질문은 모두 혼자서도 뜻이 통하는 질문이라 대화 기록이
   필요한 후속 질문이 없다. 아직 쓰이지 않은 자료 질문 `C04`·`C07`도 마찬가지다. 그래서 대화 두 줄과
   후속 질문 둘을 손으로 적고 정답 문서는 자료의 `LIB-002`로 잡았다. 고른 과정을 b7에 적었다.
4. **마지막 검색을 갈래와 상관없이 한 번 한다.** 보정으로 가지 않은 갈래에서는 같은 글을 다시 검색하므로
   첫 자리 거리가 같게 나온다. 갈래마다 코드가 달라지지 않아 흐름이 한 줄로 읽힌다.
5. **자리를 두 번 센다.** 첫 검색의 정답 자리와 마지막 검색의 정답 자리를 함께 적어 보정 검색이 한 일이
   보이게 했다. 06절은 실행을 나눠 두 줄로 적었고 이 절은 한 실행 안에서 두 자리를 적는다.
6. **파일을 쓰지 않는다.** 09절이 이 챕터에서 파일을 쓰는 유일한 절이다(handoff §09→실습 ③).
7. **모델 답에 `assert`를 걸지 않는다**(규격 §3). `assert`는 키 확인·요청 수·반복 상한 셋뿐이다.
8. **걸린 시간·토큰·비용을 재지 않는다.** Ch 12부터 한 번도 재지 않았다.
9. **쓰지 않은 것**: `numpy`·`re`·`time`·`hashlib`·`lambda`·내포식·제너레이터 식·조건 표현식·f-string·
   `key=`·`reverse=`·`set`·`setdefault`·기본값 매개변수·복합 타입힌트·세미콜론·한 줄 다중 대입·
   한 줄 복합문·클래스 정의·`enumerate`·`zip`·`next`·`join`·`max`·`min`·`float`. 부른 내장 이름은
   `len`·`open`·`print`·`range`·`round`·`sorted`·`str`뿐이다(`str`은 쓰지 않아 여섯).

## 탐색 실행과 새 커널 두 번 실행 (2026-09-19~20, /tmp/ch14-10/probe1.py~probe4.py)

langchain 1.4.0 · langchain-openai 1.6.1 · Python 3.12.13 · 문서 12건 · 질문 8건.
probe1은 자료 여덟 질문의 첫 자리 거리를 재었다(0.28~0.60). probe3은 대화 기록 셋과 후속 질문 여덟을
재작성해 첫 자리 거리를 보았다(0.26~0.71). probe4는 고른 후속 질문 둘을 세 번씩 흐름 끝까지 돌렸다.
탐색 실행 합계는 임베딩 33번·답 모델 26번이다.

**새 커널 두 번 실행(2026-09-20)에서 30/30 셀의 출력이 글자까지 같았다.** 교재 숫자는 그 출력이다.
**다만 하루 전 probe4와는 갈린 값이 있다**: 보정 질문의 문장과 실행 1의 마지막 검색 값들
(probe4는 `LIB-002`가 첫 자리·정답 자리 1, 본 실행은 `LIB-001`이 첫 자리·정답 자리 5),
실행 2의 재작성 문장과 첫 자리 거리(0.41 ↔ 0.44, 갈래는 두 번 다 같음). 같은 프롬프트에서도
답 모델 문장이 날마다 달라진다는 뜻이다. 그래서 **보정 뒤 자리는 결론·정리·복습에서 한 번 본 결과로
한정**했고, 그림 라벨에는 새 커널 두 번 실행에서 같았던 값만 넣었다(10-diagnosis.md §4).

"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part4/ch14-rag-patterns/notebooks"
SRC = ROOT / "textbook/part4/ch14-rag-patterns/_src/10-RAG-패턴-실습.html"

INSTALL = install_source([
    "langchain==1.4.0", "langchain-openai==1.6.1", "python-dotenv==1.2.3",
])

IMPORTS = r'''# 자료 읽기·제곱근·폴더 확인과 임베딩·답 모델 이름을 불러옵니다
import json
import math
import os

from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model

print("불러온 이름:", "json", "math", "os", "OpenAIEmbeddings", "init_chat_model")'''

ROOT_PATH = r'''# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part4/ch14-rag-patterns/data"):
        root_path = candidate
        break
print("고른 자리:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

LOAD_DATA = r'''# 이 챕터 폴더의 문서 파일과 질문 파일을 읽습니다(읽기만 하고 고치지 않습니다)
data_path = root_path + "/labs/part4/ch14-rag-patterns/data"
with open(data_path + "/documents.json", encoding="utf-8") as file:
    docs = json.loads(file.read())
with open(data_path + "/queries.json", encoding="utf-8") as file:
    queries = json.loads(file.read())
print("문서 수:", len(docs))
print("질문 수:", len(queries))'''

VALUES = r'''# 01~09절에서 쓰던 값 셋을 그대로 적습니다
similarity_top = 1
top_three = 3
top_all = 12
print("코사인 유사도의 가장 큰 값:", similarity_top)
print("답에 넣을 상위 문서 수:", top_three)
print("자리를 셀 때 재는 문서 수:", top_all)'''

LIMITS = r'''# 06절 보정 검색에 쓸 값 둘과 미리 세어 둔 요청 수를 적습니다
distance_limit = 0.5
retry_limit = 1
expected_calls = 10
print("거리 기준값:", distance_limit)
print("다시 검색할 수 있는 횟수 상한:", retry_limit)
print("미리 세어 둔 서비스 요청 수:", expected_calls)'''

CONVERSATION = r'''# 상담 대화 두 줄과 말이 빠진 후속 질문 둘을 정합니다
history_lines = []
history_lines.append("사용자: 일반 도서는 며칠 동안 빌릴 수 있나요?")
history_lines.append("도우미: 일반 도서는 14일 동안 대출할 수 있습니다.")
first_follow_up = "늦으면 어떻게 되나요?"
second_follow_up = "그날 못 가져오면 돈 내야 하나요?"
gold_doc_id = "LIB-002"
print("대화 기록 줄 수:", len(history_lines))
print("실행 1의 후속 질문:", first_follow_up)
print("실행 2의 후속 질문:", second_follow_up)
print("두 후속 질문의 정답 문서 ID:", gold_doc_id)'''

DOC_TEXTS = r'''# 문서 12개의 제목과 본문을 이어 붙이고 문서 ID로 그 글을 찾을 짝도 만듭니다
doc_texts = []
doc_ids = []
for doc in docs:
    doc_texts.append(doc["title"] + " " + doc["text"])
    doc_ids.append(doc["doc_id"])
text_by_doc = {}
for i in range(len(doc_ids)):
    text_by_doc[doc_ids[i]] = doc_texts[i]
print("이어 붙인 글 수:", len(doc_texts))
print("문서 ID와 글의 짝 수:", len(text_by_doc))'''

VECTOR_FUNCS = r'''# Ch 12 01절 점곱·길이·코사인 유사도·코사인 거리를 같은 코드로 다시 정의합니다
def dot_product(first, second):
    total = 0
    # 반복 번호 i로 두 벡터의 같은 자리 숫자를 짝지어 곱하고 더합니다
    for i in range(len(first)):
        total = total + first[i] * second[i]
    return total


def vector_length(vector):
    squared_sum = dot_product(vector, vector)
    return math.sqrt(squared_sum)


def cosine_similarity(first, second):
    dot = dot_product(first, second)
    length_product = vector_length(first) * vector_length(second)
    return dot / length_product


def cosine_distance(first, second):
    similarity = cosine_similarity(first, second)
    return similarity_top - similarity'''

RANK_AND_SEARCH = r'''# Ch 12 05절 거리 순위 만들기와 06절 검색 한 번 묶기를 같은 코드로 다시 정의합니다
def rank_by_distance(question_vector, top_count):
    pairs = []
    for i in range(len(doc_ids)):
        distance = cosine_distance(question_vector, doc_vectors[i])
        pairs.append((distance, doc_ids[i]))
    hit_list = []
    # sorted(목록)는 튜플의 첫 값인 거리를 작은 값부터 정렬합니다
    for pair in sorted(pairs):
        hit_list.append({"doc_id": pair[1], "거리": round(pair[0], 2)})
    return hit_list[:top_count]


def search_hits(question):
    question_vector = embedding_model.embed_query(question)
    hit_list = rank_by_distance(question_vector, top_all)
    return hit_list'''

UNIQUE_AND_GOLD = r'''# Ch 11 01절 문서 ID 모으기와 정답 자리 세기를 같은 코드로 다시 정의합니다
def unique_doc_ids(hit_list):
    doc_ids = []
    for hit in hit_list:
        if hit["doc_id"] not in doc_ids:
            doc_ids.append(hit["doc_id"])
    return doc_ids


def find_gold_rank(doc_ids, gold_doc_ids):
    gold_rank = 0
    for position in range(len(doc_ids)):
        if doc_ids[position] in gold_doc_ids:
            gold_rank = position + 1
            break
    return gold_rank'''

HEADS_AND_KEEPS = r'''# 01절 머리글 둘과 낱말 찾기 함수를 같은 코드로 다시 적습니다
rewrite_head = "아래 대화 기록을 보고 마지막 질문을 혼자서도 뜻이 통하는 검색 질문 한 문장으로 바꾸세요.\n"
rewrite_head = rewrite_head + "새 조건을 보태지 말고 질문 한 문장만 적으세요.\n\n"
answer_head = "아래 자료만 보고 질문에 한국어로 한 문장으로 답하세요.\n"
answer_head = answer_head + "답 끝에 [문서ID] 모양으로 출처를 적으세요.\n\n"


def keeps_word(sentence, word):
    found = word in sentence
    return found


print("재작성 머리글:")
print(rewrite_head)
print("답 만들기 머리글:")
print(answer_head)'''

BUILD_PROMPTS = r'''# 01절 재작성 프롬프트 만들기와 답 프롬프트 만들기를 같은 코드로 다시 정의합니다
def build_rewrite_prompt(history_lines, question):
    history_text = ""
    for line in history_lines:
        history_text = history_text + line + "\n"
    prompt_text = rewrite_head + "대화 기록:\n" + history_text
    prompt_text = prompt_text + "\n마지막 질문: " + question
    return prompt_text


def build_answer_prompt(question, hit_list):
    material = ""
    for hit in hit_list:
        doc_id = hit["doc_id"]
        material = material + "[" + doc_id + "] " + text_by_doc[doc_id] + "\n"
    prompt_text = answer_head + "질문: " + question + "\n\n자료:\n" + material
    return prompt_text'''

SPLIT_AND_FIX = r'''# 02절 줄 나누기와 06절 보정 질문 머리글 만들기를 같은 코드로 다시 정의합니다
def split_lines(reply_text):
    lines = []
    for line in reply_text.split("\n"):
        clean_line = line.strip()
        if clean_line != "":
            lines.append(clean_line)
    return lines


def build_fix_prompt(question):
    fix_head = "아래 질문을 도서관 안내문에서 찾기 좋은 말로 다시 적으세요.\n"
    fix_head = fix_head + "줄임말과 일상 말을 안내문에서 쓰는 말로 바꾸세요.\n"
    fix_head = fix_head + "새 조건을 보태지 말고 묻는 내용은 그대로 두세요.\n"
    fix_head = fix_head + "물음 한 문장만 적고 번호나 따옴표를 붙이지 마세요.\n\n"
    prompt_text = fix_head + "질문: " + question
    return prompt_text'''

RETRY_AND_CORRECT = r'''# 06절 판정 규칙과 보정 검색 규칙을 같은 코드로 다시 정의합니다
def needs_retry(top_distance, limit):
    if top_distance > limit:
        return True
    return False


def correct_once(question, top_distance, limit):
    row = {"보정 질문": question, "다시 검색한 횟수": 0}
    if needs_retry(top_distance, limit):
        fix_prompt = build_fix_prompt(question)
        fix_reply = model.invoke(fix_prompt)
        fix_lines = split_lines(fix_reply.text.strip())
        row["보정 질문"] = fix_lines[0]
        row["다시 검색한 횟수"] = 1
    return row'''

EMBEDDINGS = r'''# Ch 12와 같은 모델로 문서 12개를 벡터로 바꿉니다(임베딩 요청 1번)
embedding_model_name = "text-embedding-3-small"
vector_dimensions = 256
embedding_model = OpenAIEmbeddings(model=embedding_model_name, dimensions=vector_dimensions)
doc_vectors = embedding_model.embed_documents(doc_texts)
print("임베딩 모델 이름:", embedding_model.model)
print("벡터의 숫자 개수 설정:", embedding_model.dimensions)
print("문서 벡터 수:", len(doc_vectors))'''

REWRITE_FUNC = r'''# 01절 질문 재작성을 함수 하나로 묶습니다(부를 때마다 답 모델 요청 1번)
def rewrite_question(history_lines, question):
    rewrite_prompt = build_rewrite_prompt(history_lines, question)
    rewrite_reply = model.invoke(rewrite_prompt)
    rewritten = rewrite_reply.text.strip()
    return rewritten'''

WRITE_ANSWER = r'''# 01절 답 만들기를 함수 하나로 묶습니다(부를 때마다 답 모델 요청 1번)
def write_answer(search_text, hit_list):
    answer_prompt = build_answer_prompt(search_text, hit_list[:top_three])
    answer_reply = model.invoke(answer_prompt)
    answer = answer_reply.text.strip()
    return answer'''

PREPARE_SEARCH = r'''# 01절 재작성과 06절 보정 검색을 앞 흐름 하나로 잇습니다
def prepare_search(history_lines, question):
    rewritten = rewrite_question(history_lines, question)
    first_hits = search_hits(rewritten)
    first_ids = unique_doc_ids(first_hits)
    row = correct_once(rewritten, first_hits[0]["거리"], distance_limit)
    row["재작성한 질문"] = rewritten
    row["첫 검색의 첫 자리 거리"] = first_hits[0]["거리"]
    row["첫 검색의 정답 자리"] = find_gold_rank(first_ids, [gold_doc_id])
    return row'''

ANSWER_ONCE = r'''# 앞 흐름이 고른 글로 다시 검색하고 01절 답 만들기까지 잇습니다
def answer_once(history_lines, question):
    row = prepare_search(history_lines, question)
    final_hits = search_hits(row["보정 질문"])
    final_ids = unique_doc_ids(final_hits)
    row["마지막 검색의 첫 자리 문서"] = final_ids[0]
    row["마지막 검색의 첫 자리 거리"] = final_hits[0]["거리"]
    row["마지막 검색의 정답 자리"] = find_gold_rank(final_ids, [gold_doc_id])
    row["답"] = write_answer(row["보정 질문"], final_hits)
    return row'''

RUN_ROW = r'''# 실행 한 번을 기록 한 줄로 만듭니다(06절 기록 판에서 자리 칸을 둘로 나누고 첫 자리 문서 칸을 뺐습니다)
def run_row(run_name, follow_up, result):
    row = {"실행": run_name}
    row["후속 질문"] = follow_up
    row["첫 검색의 첫 자리 거리"] = result["첫 검색의 첫 자리 거리"]
    row["다시 검색한 횟수"] = result["다시 검색한 횟수"]
    row["첫 검색의 정답 자리"] = result["첫 검색의 정답 자리"]
    row["마지막 검색의 정답 자리"] = result["마지막 검색의 정답 자리"]
    return row'''

RUN1 = r'''# 실행 1은 대화 기록 두 줄과 첫 후속 질문으로 흐름 전체를 지납니다(서비스 요청 다섯 번)
run1 = answer_once(history_lines, first_follow_up)
print("후속 질문:", first_follow_up)
print("재작성한 질문:", run1["재작성한 질문"])
print("첫 검색의 첫 자리 거리:", run1["첫 검색의 첫 자리 거리"])
print("거리 기준값:", distance_limit)
print("다시 검색한 횟수:", run1["다시 검색한 횟수"])
print("검색에 넣은 마지막 글:", run1["보정 질문"])'''

RUN1_RESULT = r'''# 실행 1의 마지막 검색 결과와 모델이 쓴 답을 봅니다
print("마지막 검색의 첫 자리 문서:", run1["마지막 검색의 첫 자리 문서"])
print("마지막 검색의 첫 자리 거리:", run1["마지막 검색의 첫 자리 거리"])
print("첫 검색의 정답 자리:", run1["첫 검색의 정답 자리"])
print("마지막 검색의 정답 자리:", run1["마지막 검색의 정답 자리"])
print("답에 정답 문서 ID 표시가 있는가:", keeps_word(run1["답"], gold_doc_id))
print("모델이 쓴 답:")
print(run1["답"])'''

RUN2 = r'''# 실행 2는 후속 질문만 바꾸고 대화 기록과 기준값은 그대로 둡니다(서비스 요청 네 번)
run2 = answer_once(history_lines, second_follow_up)
print("후속 질문:", second_follow_up)
print("재작성한 질문:", run2["재작성한 질문"])
print("첫 검색의 첫 자리 거리:", run2["첫 검색의 첫 자리 거리"])
print("거리 기준값:", distance_limit)
print("다시 검색한 횟수:", run2["다시 검색한 횟수"])
print("검색에 넣은 마지막 글:", run2["보정 질문"])'''

RUN2_RESULT = r'''# 실행 2의 마지막 검색 결과와 모델이 쓴 답을 봅니다
print("마지막 검색의 첫 자리 문서:", run2["마지막 검색의 첫 자리 문서"])
print("마지막 검색의 첫 자리 거리:", run2["마지막 검색의 첫 자리 거리"])
print("첫 검색의 정답 자리:", run2["첫 검색의 정답 자리"])
print("마지막 검색의 정답 자리:", run2["마지막 검색의 정답 자리"])
print("답에 정답 문서 ID 표시가 있는가:", keeps_word(run2["답"], gold_doc_id))
print("모델이 쓴 답:")
print(run2["답"])'''

TABLE = r'''# 두 실행의 기록을 담아 라벨 줄 아래에 한 줄씩 출력합니다
run_rows = []
run_rows.append(run_row("실행 1", first_follow_up, run1))
run_rows.append(run_row("실행 2", second_follow_up, run2))
print("실행 | 첫 자리 거리 | 다시 검색한 횟수 | 첫 검색 정답 자리 | 마지막 검색 정답 자리")
for row in run_rows:
    print(row["실행"], "|", row["첫 검색의 첫 자리 거리"], "|", row["다시 검색한 횟수"], "|", row["첫 검색의 정답 자리"], "|", row["마지막 검색의 정답 자리"])
    print("  후속 질문:", row["후속 질문"])'''

DIFF = r'''# 값이 갈린 칸 수를 세고 다시 검색 상한을 넘지 않았는지 확인합니다
column_names = ["첫 검색의 첫 자리 거리", "다시 검색한 횟수", "첫 검색의 정답 자리", "마지막 검색의 정답 자리"]
changed_count = 0
for name in column_names:
    if run1[name] != run2[name]:
        changed_count = changed_count + 1
print("견준 칸 수:", len(column_names))
print("값이 갈린 칸 수:", changed_count)
assert run1["다시 검색한 횟수"] <= retry_limit, "실행 1이 다시 검색 상한을 넘었습니다."
assert run2["다시 검색한 횟수"] <= retry_limit, "실행 2가 다시 검색 상한을 넘었습니다."'''

CALLS = r'''# 두 실행이 서비스에 보낸 요청 수를 세어 미리 세어 둔 수와 견줍니다
doc_calls = 1
base_calls = 4
run1_calls = base_calls + run1["다시 검색한 횟수"]
run2_calls = base_calls + run2["다시 검색한 횟수"]
total_calls = doc_calls + run1_calls + run2_calls
print("실행 1의 서비스 요청 수:", run1_calls)
print("실행 2의 서비스 요청 수:", run2_calls)
print("실제로 센 서비스 요청 수:", total_calls)
assert total_calls == expected_calls, "미리 세어 둔 요청 수와 다릅니다."'''


TITLE = """# RAG 패턴 실습: 후속 질문 하나를 상담 흐름으로 잇기

**이 노트북에서 할 일**

1. 대화 기록 두 줄이 있는 후속 질문을 혼자서도 뜻이 통하는 질문으로 바꿉니다.
2. 그 질문으로 검색하고 첫 자리 거리가 기준값보다 멀면 한 번만 다시 검색합니다.
3. 마지막 검색의 앞 세 자리 원문으로 답을 만들고 두 실행을 견줍니다.

**준비물** — 이 절은 프로젝트 맨 위 폴더의 `.env`에 적어 둔 `OPENAI_API_KEY`를 씁니다.
읽어 오는 파일은 이 챕터 폴더의 문서 파일과 질문 파일 둘입니다.
새로 쓰는 파일은 없습니다.

서비스 요청은 열 번이고 답 모델 다섯 번과 임베딩 다섯 번입니다.
답 모델 요청은 실행 1이 세 번이고 실행 2가 두 번입니다.
임베딩 요청은 문서 한 번과 실행마다 두 번입니다.
예상 비용은 미화 0.01달러 아래이고 실행 시간은 3분 안팎입니다.

**기준 버전** — 첫 셀에서 LangChain 1.4.0과 langchain-openai 1.6.1을 설치합니다.
키를 읽는 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 4절부터 9절까지 읽습니다.
값을 정하고 대화와 후속 질문을 적고 함수 다섯을 만드는 자리입니다.
10절과 11절은 실행 1과 실행 2를 지나며 갈래가 갈리는 자리입니다.
12절은 두 실행을 표로 모으고 요청 수를 세는 자리입니다.

실습 폴더 `labs/part4/ch14-rag-patterns`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""

FIGURE_ALT = "위에서 아래로 놓인 상자 일곱으로 맨 위 초록 상자 대화 기록 두 줄과 후속 질문에서 보라 상자 답 모델이 질문 재작성으로 이어지고 파란 상자 재작성한 질문으로 검색하고 첫 자리 거리 보기를 지나 점선 둘로 갈라져 오른쪽 보라 상자 답 모델이 보정 질문 쓰기와 왼쪽으로 내려가는 파란 상자 검색에 넣을 마지막 글로 다시 검색으로 가며 보라 상자 답 모델이 앞 세 자리 원문으로 답 쓰기를 지나 맨 아래 노란 상자 기록 한 줄로 이어지는 그림"

FIGURE_READ = """위에서 아래로 읽습니다.
맨 위 초록 상자가 우리가 넣는 재료이고 맨 아래 노란 상자가 출력으로 확인하는 값입니다.
보라 상자 셋이 답 모델을 부르는 자리이고 파란 상자 둘이 코드가 하는 일입니다.
가운데에서 점선 둘로 갈라지는데 오른쪽 갈래만 답 모델을 한 번 더 부릅니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIGURE_ALT + "](attachment:10-1-앞-절-기능-셋을-한-흐름으로-잇기.png)\n\n" + FIGURE_READ, html="skip"),
        md("""## 1. 준비

이번 절은 이 챕터의 실습입니다.
01~09절에서 쓴 이름과 문법만 쓰고 따로 내는 과제는 없습니다.
첫 셀은 패키지 세 개를 설치하고 설치된 판 번호를 출력합니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 판 번호 세 줄이 보입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이름 다섯 개를 불러옵니다.
앞의 셋은 자료 읽기와 제곱근과 폴더 확인에 씁니다.
뒤의 둘은 01~09절에서 쓴 임베딩과 답 모델 이름입니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄에 불러온 이름 다섯 개가 보입니다.
09절과 달리 `hashlib`이 없습니다.
이 절은 파일을 쓰지 않기 때문입니다.

## 2. 키와 모델 준비"""),
    ] + key_and_model_cells("openai:gpt-5.4-mini") + [
        md("""## 3. 문서와 질문 읽기

이 절은 01~09절과 같은 문서 파일과 질문 파일을 읽습니다.
먼저 노트북을 연 자리에서 프로젝트 맨 위를 찾습니다."""),
        code(ROOT_PATH),
        md("""**결과 읽기** — 출력 줄 `고른 자리` 뒤에 점 하나나 위로 올라가는 표시가 보입니다.
01~09절에서 쓴 코드와 같습니다.

다음 셀은 문서 파일과 질문 파일을 읽습니다."""),
        code(LOAD_DATA),
        md("""**결과 읽기** — 출력 줄 `문서 수: 12`와 `질문 수: 8`이 01~09절과 같습니다.

자료의 질문 여덟 개는 모두 혼자서도 뜻이 통하는 질문입니다.
그래서 대화 기록이 있어야 뜻이 정해지는 후속 질문이 자료에 없습니다.
이 실습은 상담 대화 두 줄과 후속 질문 둘을 손으로 적습니다.
정답 문서는 자료에 있는 문서에서 고릅니다.

## 4. 값 정하기

다음 셀은 01~09절에서 쓰던 값 셋을 그대로 적는 준비 셀입니다.
읽지 말고 실행만 하고 넘어가도 됩니다."""),
        setup(VALUES),
        md("""다음 셀은 06절 보정 검색에 쓸 값 둘과 미리 세어 둔 요청 수를 적습니다.
거리 기준값은 06절에서 `0.65`였고 이 실습은 `0.5`로 다시 잡았습니다.
06절은 자료 질문을 그대로 검색했고 이 실습은 재작성한 질문으로 검색합니다.
두 갈래가 모두 보이도록 탐색 실행 뒤에 정한 값입니다."""),
        code(LIMITS),
        md("""**결과 읽기** — 출력 줄 `거리 기준값: 0.5`가 다시 검색할지 가르는 값입니다.
출력 줄 `다시 검색할 수 있는 횟수 상한: 1`은 06절 값 그대로입니다.
출력 줄 `미리 세어 둔 서비스 요청 수: 10`은 마지막 셀에서 실제로 센 수와 견줍니다.

거리는 작을수록 가깝습니다.
첫 자리 거리가 기준값보다 크면 한 번만 다시 검색합니다.

## 5. 상담 대화와 후속 질문 정하기

이용자가 도우미와 두 줄을 주고받은 뒤에 짧게 묻는 상황입니다.
두 후속 질문은 모두 반납이 늦을 때 무슨 일이 생기는지 묻습니다.
그래서 정답 문서는 둘 다 같습니다."""),
        code(CONVERSATION),
        md("""**결과 읽기** — 출력 줄 `대화 기록 줄 수: 2`로 앞선 대화가 두 줄입니다.
출력 줄 `실행 1의 후속 질문: 늦으면 어떻게 되나요?`에는 무엇이 늦는지가 없습니다.
출력 줄 `실행 2의 후속 질문: 그날 못 가져오면 돈 내야 하나요?`에는 그날이 어느 날인지가 없습니다.
출력 줄 `두 후속 질문의 정답 문서 ID: LIB-002`가 두 실행에서 같게 두는 정답입니다.

둘 다 대화 기록을 봐야 뜻이 정해지는 후속 질문입니다.
다만 실행 2의 질문에는 돈이라는 말이 들어 있어 묻는 내용이 더 좁습니다.

## 6. 앞 절 부품 준비

다음 여덟 셀은 01~09절에서 이미 읽은 코드입니다.
읽지 말고 실행만 하고 넘어가도 됩니다.
문서 글과 짝 만들기, 거리 함수 넷, 순위 함수와 검색 묶기, 자리 세기 둘이 있습니다.
01절 머리글 둘과 프롬프트 함수 둘, 06절 보정 부품 넷도 같은 코드로 다시 정의합니다."""),
        setup(DOC_TEXTS),
        code(VECTOR_FUNCS, lesson_role="setup", upgrade_allow=["multiple_defs_in_cell"]),
        code(RANK_AND_SEARCH, lesson_role="setup", upgrade_allow=["multiple_defs_in_cell"]),
        code(UNIQUE_AND_GOLD, lesson_role="setup", upgrade_allow=["multiple_defs_in_cell"]),
        setup(HEADS_AND_KEEPS),
        code(BUILD_PROMPTS, lesson_role="setup", upgrade_allow=["multiple_defs_in_cell"]),
        code(SPLIT_AND_FIX, lesson_role="setup", upgrade_allow=["multiple_defs_in_cell"]),
        code(RETRY_AND_CORRECT, lesson_role="setup", upgrade_allow=["multiple_defs_in_cell"]),
        md("""준비 셀 여덟 개를 지났습니다.
머리글 셋은 01절과 06절에서 쓴 글자 그대로입니다.
같은 머리글을 써야 앞 절과 같은 조건이 됩니다.
02절 변형 질문과 05절 가상 문서와 07절 근거 검사와 08절 갈래 요약은 가져오지 않았습니다.

## 7. 문서를 벡터로 바꾸기

다음 셀은 문서 열두 건을 벡터로 바꿉니다.
이 절에서 서비스에 보내는 첫 요청입니다."""),
        code(EMBEDDINGS),
        md("""**결과 읽기** — 출력 줄 `임베딩 모델 이름: text-embedding-3-small`은 01~09절과 같은 모델입니다.
출력 줄 `벡터의 숫자 개수 설정: 256`도 Ch 10~13과 같은 값입니다.
출력 줄 `문서 벡터 수: 12`로 문서마다 벡터 하나를 받았습니다.

문서 벡터는 한 번만 만들어 두 실행이 함께 씁니다.

## 8. 앞 절 기능을 함수로 묶기

앞 절 기능 둘을 함수 하나씩으로 묶습니다.
첫 함수는 01절 질문 재작성입니다."""),
        code(REWRITE_FUNC),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `rewrite_question`은 대화 기록과 마지막 질문을 한 글로 이어 답 모델에 넣습니다.
받은 답에서 앞뒤 빈칸을 없앤 글이 재작성한 질문입니다.
01절과 같은 머리글을 쓰므로 01절과 같은 조건입니다.

다음 셀은 01절 답 만들기입니다."""),
        code(WRITE_ANSWER),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `write_answer`는 검색한 목록에서 앞 세 자리만 골라 원문을 넣습니다.
답 머리글이 답 끝에 문서 ID 표시를 붙이라고 적고 있습니다.
드는 서비스 요청은 답 모델 한 번입니다.

## 9. 흐름 하나로 잇기

이제 두 함수와 06절 보정 검색을 한 흐름으로 잇습니다.
앞 흐름은 재작성과 검색과 판정과 보정까지입니다."""),
        code(PREPARE_SEARCH),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `prepare_search`는 재작성한 질문으로 한 번 검색하고 첫 자리 거리를 봅니다.
그 거리를 06절 규칙에 넣어 다시 검색할지 정합니다.
멀다고 나온 갈래에서만 답 모델이 보정 질문을 씁니다.
첫 검색의 정답 자리도 함께 적어 두어 뒤에서 견줄 수 있게 합니다.

다음 셀은 뒤 흐름입니다."""),
        code(ANSWER_ONCE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `answer_once`는 앞 흐름이 고른 마지막 글로 다시 검색합니다.
보정으로 가지 않은 갈래에서는 같은 글을 다시 검색하므로 결과가 같습니다.
갈래마다 코드가 달라지지 않아 흐름이 한 줄로 읽힙니다.
마지막으로 앞 세 자리 원문을 넣어 답을 받습니다.

다음 셀은 실행 한 번을 표 한 줄로 만드는 기록 장치입니다."""),
        code(RUN_ROW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `run_row`는 06절 기록 판에서 자리 칸을 둘로 나누고 첫 자리 문서 칸을 뺀 것입니다.
칸은 실행 이름과 후속 질문과 첫 자리 거리와 다시 검색한 횟수입니다.
거기에 첫 검색의 정답 자리와 마지막 검색의 정답 자리를 더합니다.

## 10. 실행 1

실행 전에 예상해 봅니다.
후속 질문이 짧아 재작성한 질문도 넓게 나올 것입니다.
그러면 첫 자리 거리가 기준값보다 멀어 한 번 더 검색할 것입니다."""),
        code(RUN1),
        md("""**결과 읽기** — 출력 줄 `첫 검색의 첫 자리 거리: 0.64`가 기준값 `0.5`보다 큽니다.
그래서 출력 줄 `다시 검색한 횟수: 1`이 되었습니다.
출력 줄 `검색에 넣은 마지막 글` 뒤에 답 모델이 쓴 보정 질문이 있습니다.

보정 질문에서는 늦게라는 일상 말이 기한이라는 안내문 말로 바뀌었습니다.
재작성한 질문과 보정 질문의 문장은 실행마다 달라질 수 있습니다.
다음 셀은 이 실행의 마지막 검색 결과와 답을 봅니다."""),
        code(RUN1_RESULT),
        md("""**결과 읽기** — 출력 줄 `첫 검색의 정답 자리: 2`가 보정 전 자리입니다.
출력 줄 `마지막 검색의 정답 자리: 5`가 보정 뒤 자리입니다.
이번 실행에서는 자리 숫자가 커졌습니다.

출력 줄 `마지막 검색의 첫 자리 거리: 0.6`은 첫 검색보다 작습니다.
그런데 출력 줄 `마지막 검색의 첫 자리 문서: LIB-001`은 정답 문서가 아닙니다.
거리가 줄어도 정답 문서가 앞으로 온다고 볼 수 없는 자리입니다.
하루 전 탐색 실행에서는 같은 후속 질문의 보정 뒤 정답 문서가 첫 자리였습니다.
보정 질문 문장이 달라져서이고 이 자리 번호는 한 번 본 값입니다.

출력 줄 `답에 정답 문서 ID 표시가 있는가: False`도 이번 실행의 결과입니다.
모델이 쓴 답은 대출 기간을 알려 주고 있어 물음과 맞지 않습니다.

## 11. 실행 2

바꾸는 값은 후속 질문 하나입니다.
대화 기록과 거리 기준값과 문서와 정답 문서와 모델은 그대로 둡니다.
실행 전에 예상해 봅니다.
질문에 돈이라는 말이 있어 재작성한 질문이 더 좁아질 것입니다."""),
        code(RUN2),
        md("""**결과 읽기** — 출력 줄 `첫 검색의 첫 자리 거리: 0.44`가 기준값 `0.5`보다 작습니다.
그래서 출력 줄 `다시 검색한 횟수: 0`이 되었습니다.
출력 줄 `검색에 넣은 마지막 글` 뒤에 재작성한 질문이 그대로 있습니다.

보정 갈래로 가지 않아 답 모델 요청이 한 번 줄었습니다.
다음 셀은 이 실행의 마지막 검색 결과와 답을 봅니다."""),
        code(RUN2_RESULT),
        md("""**결과 읽기** — 출력 줄 `첫 검색의 정답 자리: 1`과 `마지막 검색의 정답 자리: 1`이 같습니다.
보정으로 가지 않아 같은 글을 다시 검색했기 때문입니다.
출력 줄 `마지막 검색의 첫 자리 거리: 0.44`도 첫 검색과 같습니다.

출력 줄 `답에 정답 문서 ID 표시가 있는가: True`로 실행 1과 달랐습니다.
답 문장은 실행마다 달라질 수 있어 낱말을 확인 줄로 보지 않습니다.

## 12. 두 실행 견주기

마지막으로 두 실행의 기록을 한 표로 모읍니다.
실행 전에 예상해 봅니다.
한 번 더 검색한 실행 1의 자리가 앞으로 올 것이라고 기대하기 쉽습니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄이 나옵니다.
첫 줄은 `실행 1 | 0.64 | 1 | 2 | 5`이고 둘째 줄은 `실행 2 | 0.44 | 0 | 1 | 1`입니다.
마지막 칸은 실행 1이 `5`이고 실행 2가 `1`입니다.

한 번 더 검색한 실행 1의 자리가 오히려 뒤였습니다.
앞의 예상과 다른 결과입니다.
다음 셀은 갈린 칸 수를 세고 반복 상한을 확인합니다."""),
        code(DIFF),
        md("""**결과 읽기** — 출력 줄 `견준 칸 수: 4`와 `값이 갈린 칸 수: 4`가 보입니다.
네 칸이 모두 갈렸습니다.
확인 줄 둘은 두 실행 모두 반복 상한을 넘지 않았을 때 조용히 지나갑니다.

다음 셀은 서비스에 보낸 요청 수를 셉니다."""),
        code(CALLS),
        md("""**결과 읽기** — 출력 줄 `실행 1의 서비스 요청 수: 5`와 `실행 2의 서비스 요청 수: 4`가 보입니다.
출력 줄 `실제로 센 서비스 요청 수: 10`이 미리 세어 둔 수와 같아 확인 줄이 지나갔습니다.
이 수는 고정 네 번에 실행마다 다시 검색한 횟수를 더해 센 값입니다.
차이 한 번은 실행 1이 보정 질문을 받으려고 답 모델을 한 번 더 부른 것입니다.

## 정리

1. 01절 질문 재작성과 06절 보정 검색과 01절 답 만들기를 한 흐름으로 이었습니다.
2. 후속 질문 하나만 바꾸자 지나는 갈래와 서비스 요청 수가 달라졌습니다.
3. 요청을 한 번 더 쓴 실행에서도 이번에는 정답 문서가 첫 자리로 오지 않았습니다.

이 결과는 문서 열두 건과 후속 질문 둘과 기준값 하나에서 한 번 본 것입니다.
답이 맞는지 판정하는 일은 Ch 15에서 따로 봅니다."""),
    ]


SRC_HTML = """<!--meta: 실습 30분 | 코드 notebooks/10-RAG-패턴-실습.ipynb | 새 용어 0 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>이 절을 마치면 01절 질문 재작성과 06절 보정 검색과 답 만들기를 한 흐름으로 이을 수 있습니다.</li>
<li>첫 자리 거리를 기준값과 견주어 다시 검색할지 코드가 정하게 만들 수 있습니다.</li>
<li>후속 질문 하나만 바꿔 같은 흐름을 다시 실행할 수 있습니다.</li>
<li>기능을 더 붙인 실행이 늘 나아지지는 않는다는 것을 출력으로 확인할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>01절부터 09절까지 패턴을 하나씩 익혔습니다. 검색 앞에서 넣을 글을 바꾸는 자리와 검색 뒤에 다시 검색하는 자리를 따로 보았습니다. 마지막 절에서는 같은 질문 벌로 패턴 셋을 나란히 견주었습니다.</p>
<p>실제 상담 창구를 만들면 이 자리들이 한 흐름 안에 함께 들어갑니다. 이용자는 앞 대화를 이어 짧게 묻고 창구는 그 말을 검색할 수 있는 질문으로 바꿉니다. 찾은 것이 멀면 한 번 더 찾고 마지막에 답을 만듭니다.</p>
<p>이번 실습은 그 세 자리를 한 번에 잇습니다. 01절 재작성과 06절 보정 검색과 01절 답 만들기입니다.</p>
<p>이번 절은 이 챕터의 실습입니다. 01~09절에서 쓴 이름과 문법만 쓰고 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p>
<p><strong>이 절의 질문</strong> — 대화 기록을 그대로 두고 후속 질문 하나만 바꾸면 흐름은 어느 갈래로 갈까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>이번 실습은 아래 절에서 배운 것을 그대로 가져옵니다.</p>
<table><thead><tr><th>절</th><th>배운 것</th><th>실습에서 쓰는 곳</th></tr></thead><tbody>
<tr><td>01절</td><td>대화 기록과 후속 질문, 재작성 머리글과 <code>build_rewrite_prompt()</code></td><td>노트북 6절 부품, 8절 <code>rewrite_question()</code></td></tr>
<tr><td>01절</td><td>답 머리글과 <code>build_answer_prompt()</code>·<code>keeps_word()</code>·문서 ID와 글의 짝</td><td>노트북 6절 부품, 8절 <code>write_answer()</code></td></tr>
<tr><td>06절</td><td>첫 자리 거리와 기준값 견주기, <code>needs_retry()</code>·<code>correct_once()</code></td><td>노트북 6절 부품, 9절 <code>prepare_search()</code></td></tr>
<tr><td>06절</td><td>검색 한 번 묶기 <code>search_hits()</code>와 다시 검색 횟수 상한</td><td>노트북 6절 부품, 9절과 12절 확인 줄</td></tr>
<tr><td>02절</td><td>모델 답을 줄 단위로 나누는 <code>split_lines()</code></td><td>노트북 6절 부품, 보정 질문 고르기</td></tr>
<tr><td>Ch 12 01·05절</td><td>코사인 거리 함수 넷과 거리 순위 만들기</td><td>노트북 6절 부품, 검색 자리</td></tr>
<tr><td>Ch 11 01절</td><td>문서 ID 모으기와 정답 자리 세기</td><td>노트북 6절 부품, 9절 자리 칸 둘</td></tr>
</tbody></table>
<p>읽는 파일은 01~09절과 같은 문서 파일과 질문 파일입니다. 문서 열두 건을 그대로 쓰고 이번 실습에서 새로 만든 자료는 없습니다. 이 절은 파일을 쓰지도 않습니다.</p>
<p>02절 변형 질문과 03·04절 질문 바꾸기와 05절 가상 문서는 이번 실습에서 쓰지 않습니다. 모두 검색 앞을 손보는 자리라 함께 붙이면 흐름만 길어집니다. 07절 근거 검사도 빼서 답 품질 판정을 Ch 15 몫으로 남겼습니다.</p>
<p>08절 한 단계 요약도 쓰지 않습니다. 질문을 받기 전에 요약을 만들어 두는 자리라 이 흐름에 들어갈 자리가 없습니다. 09절이 견준 패턴 셋도 그대로 되풀이하지 않습니다.</p>
<p>06절과 다른 점은 검색에 넣는 글입니다. 06절은 이용자가 적은 질문을 그대로 검색했습니다. 이번 실습은 재작성한 질문을 검색하므로 거리 범위가 달라집니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3>
<p>01절부터 쓴 나무판을 그대로 씁니다. 지금까지는 구멍 하나에 마개 하나를 대 보거나 여러 마개를 차례로 대 보았습니다.</p>
<p>이번에는 한 판 위에 부품 셋을 나란히 세웁니다. 부품마다 하는 일이 다르고 짧은 막대가 옆 부품과 이어 줍니다. 그래서 셋이 따로 놓인 것이 아니라 한 줄로 읽힙니다.</p>
{{img:10-4-한-판에-부품-셋을-이어-끼우기|흰 바탕에 긴 나무판 하나가 비스듬히 위에서 본 모양으로 놓여 있고 그 위 한 줄에 같은 크기 둥근 나무 마개 셋이 서 있으며 짧은 나무 막대 둘이 첫 마개와 둘째 마개를 또 둘째 마개와 셋째 마개를 이어 주는 그림|한 판 위에 부품 셋을 세우고 막대 둘로 이어 한 줄로 만듭니다.}}
<p class="look"><b>그림 읽기</b> — 먼저 가운데 나무판을 봅니다. 긴 판 하나가 비스듬히 위에서 본 모양으로 놓여 있습니다. 판 위에 둥근 마개 셋이 한 줄로 서 있습니다.</p>
<p class="look">다음으로 마개 사이를 봅니다. 짧은 나무 막대 둘이 마개와 마개를 이어 줍니다. 막대가 있어 셋이 따로가 아니라 이어진 한 줄로 읽힙니다.</p>
<p class="look">마개 셋은 질문 재작성과 보정 검색과 답 만들기입니다. 막대 둘은 앞 부품이 낸 글을 다음 부품에 넘기는 자리입니다.</p>
<h3>실습 조립의 구성</h3>
{{mermaid:10-1-앞-절-기능-셋을-한-흐름으로-잇기|위에서 아래로 놓인 상자 일곱으로 맨 위 초록 상자 대화 기록 두 줄과 후속 질문에서 보라 상자 답 모델이 질문 재작성으로 이어지고 파란 상자 재작성한 질문으로 검색하고 첫 자리 거리 보기를 지나 점선 둘로 갈라져 오른쪽 보라 상자 답 모델이 보정 질문 쓰기와 왼쪽으로 내려가는 파란 상자 검색에 넣을 마지막 글로 다시 검색으로 가며 보라 상자 답 모델이 앞 세 자리 원문으로 답 쓰기를 지나 맨 아래 노란 상자 기록 한 줄로 이어지는 그림|앞 절 기능 셋을 한 흐름으로 잇고 가운데에서 갈래가 갈립니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자가 우리가 넣는 재료이고 맨 아래 노란 상자가 출력으로 확인하는 값입니다.</p>
<p class="look">보라 상자 셋이 답 모델을 부르는 자리입니다. 파란 상자 둘은 우리가 코드에 적은 처리입니다.</p>
<p class="look">가운데 파란 상자에서 점선 둘이 갈라집니다. 오른쪽 점선은 첫 자리 거리가 기준값보다 멀 때 가는 갈래입니다. 왼쪽 점선은 멀지 않을 때 보정을 건너뛰는 갈래입니다.</p>
<table><thead><tr><th>함수</th><th>하는 일</th><th>가져온 곳</th></tr></thead><tbody>
<tr><td><code>rewrite_question()</code></td><td>대화 기록과 후속 질문을 넣어 독립 질문을 받음</td><td>01절 머리글과 프롬프트 함수</td></tr>
<tr><td><code>prepare_search()</code></td><td>재작성한 질문으로 검색하고 다시 검색할지 정함</td><td>06절 판정과 보정 규칙</td></tr>
<tr><td><code>answer_once()</code></td><td>마지막 글로 다시 검색하고 답까지 받음</td><td>이 절이 새로 묶은 조립 함수</td></tr>
<tr><td><code>write_answer()</code></td><td>앞 세 자리 원문을 넣어 답 한 문장을 받음</td><td>01절 답 머리글과 프롬프트 함수</td></tr>
<tr><td><code>run_row()</code></td><td>실행 한 번을 표 한 줄로 만듦</td><td>06절 기록 판에서 자리 칸을 둘로 나누고 첫 자리 문서 칸을 뺌</td></tr>
</tbody></table>
<h3>거리 기준값을 다시 잡은 까닭</h3>
<p>06절 거리 기준값은 <code>0.65</code>였습니다. 06절은 자료 여덟 질문의 첫 자리 거리를 먼저 보고 그보다 조금 큰 값을 잡았습니다.</p>
<p>이번 실습은 재작성한 질문으로 검색합니다. 재작성한 질문은 대화 기록의 말을 담아 문서에 더 가깝습니다. 그래서 첫 자리 거리가 06절보다 작게 나옵니다.</p>
<p>탐색 실행에서 두 재작성 질문의 첫 자리 거리가 <code>0.5</code>의 위와 아래로 갈렸습니다. 그래서 기준값을 <code>0.5</code>로 잡았습니다. 두 갈래가 모두 보이게 하려고 정한 예이고 무엇을 재서 얻은 기준이 아닙니다.</p>
<h3>두 번의 실행</h3>
<p>실행 1의 후속 질문은 <code>늦으면 어떻게 되나요?</code>입니다. 실행 2는 후속 질문만 <code>그날 못 가져오면 돈 내야 하나요?</code>로 바꿉니다.</p>
<p>두 실행에서 같게 둔 것은 일곱입니다. 대화 기록 두 줄과 문서 열두 건과 정답 문서 <code>LIB-002</code>입니다. 거기에 거리 기준값 <code>0.5</code>와 다시 검색 횟수 상한을 더합니다. 답에 넣을 자리 셋과 답 모델도 같습니다.</p>
<p>후속 질문은 함수에 넣는 값이라 흐름을 고치지 않습니다. 두 질문 모두 반납이 늦을 때 무슨 일이 생기는지 묻습니다. 그래서 정답 문서도 같습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2>
<p>노트북은 먼저 자료를 읽고 값을 정하고 대화와 후속 질문을 적습니다. 그다음 앞 절 부품을 준비 셀 여덟 개로 다시 정의하고 문서를 벡터로 바꿉니다. 마지막으로 함수 다섯을 만들고 실행 1과 실행 2와 두 실행 견주기를 차례로 합니다.</p>
<p>정의 셀은 열셋이고 그 가운데 여덟이 앞 절과 같은 코드입니다. 그 여덟 셀에 앞 절 함수 열다섯이 들어 있습니다. 나머지 다섯이 이 절에서 만드는 함수입니다. 정의 셀은 실행만 하고 넘어갑니다.</p>
<p>실제 OpenAI 모델을 부릅니다. 이 페이지의 출력은 2026-09-20에 실행한 결과입니다. 서비스 요청은 모두 열 번이고 답 모델 다섯 번과 임베딩 다섯 번입니다. 답 모델 요청은 실행 1이 세 번이고 실행 2가 두 번입니다. 예상 비용은 열 번을 합쳐 미화 0.01달러 아래입니다.</p>
{{notebook:10-RAG-패턴-실습}}
<p class="look"><b>확인할 점</b> — 실행 1의 출력 줄 <code>첫 검색의 첫 자리 거리: 0.64</code>와 <code>다시 검색한 횟수: 1</code>을 봅니다. 실행 2의 같은 자리는 <code>0.44</code>와 <code>0</code>입니다. 두 실행의 <code>마지막 검색의 정답 자리</code> 줄을 견주고 견주기 표에서 네 칸을 함께 읽습니다. 출력 줄 <code>실제로 센 서비스 요청 수: 10</code>으로 요청 수를 확인합니다.</p>
<h3>실행 1의 실제 순서</h3>
{{mermaid:10-2-실행-1의-실제-순서|위에서 아래로 내려가는 흐름도로 맨 위 초록 상자 후속 질문 늦으면 어떻게 되나요와 그 아래 보라 상자 답 모델이 쓴 재작성한 질문이 있고 그 아래 노란 상자 첫 검색의 첫 자리 거리 0.64와 첫 검색의 정답 자리 2가 있으며 오른쪽 파란 상자 거리 기준값 0.5가 같은 자리로 모이고 점선으로 보라 상자 답 모델이 쓴 보정 질문과 다시 검색한 횟수 1로 내려간 뒤 파란 상자 보정 질문으로 다시 검색과 맨 아래 보라 상자 답 모델이 앞 세 자리 원문으로 답 쓰기로 이어지는 그림|첫 자리 거리 0.64가 기준값 0.5보다 멀어 보정 갈래로 가서 다시 검색한 뒤 답을 만들었습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자가 이용자가 적은 후속 질문이고 그 아래 왼쪽 보라 상자가 답 모델이 쓴 재작성한 질문입니다.</p>
<p class="look">가운데 노란 상자로 화살표 둘이 모입니다. 하나는 왼쪽 위 보라 상자에서 오고 하나는 오른쪽 파란 상자에서 옵니다. 그 파란 상자가 우리가 코드에 적은 거리 기준값입니다.</p>
<p class="look">그 아래 점선이 보정 갈래입니다. 파란 상자에서 보정 질문으로 다시 검색하고 맨 아래 보라 상자에서 답을 만듭니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2>
<p>두 실행은 가는 길이 달랐고 자리도 달랐습니다. 실행 1은 첫 자리 거리가 기준값보다 멀어 한 번 더 검색했습니다. 실행 2는 멀지 않아 보정을 건너뛰었습니다.</p>
<table><thead><tr><th>실행</th><th>후속 질문</th><th>첫 자리 거리</th><th>다시 검색한 횟수</th><th>첫 검색 정답 자리</th><th>마지막 검색 정답 자리</th><th>서비스 요청 수</th></tr></thead><tbody>
<tr><td>실행 1</td><td><code>늦으면 어떻게 되나요?</code></td><td>0.64</td><td>1</td><td>2</td><td>5</td><td>5</td></tr>
<tr><td>실행 2</td><td><code>그날 못 가져오면 돈 내야 하나요?</code></td><td>0.44</td><td>0</td><td>1</td><td>1</td><td>4</td></tr>
</tbody></table>
<p>견준 네 칸이 모두 갈렸습니다. 요청을 한 번 더 쓴 실행 1에서도 이번에는 정답 문서가 첫 자리로 오지 않았습니다. 보정 뒤 자리 번호는 하루 전 탐색 실행과 달라 아래 표에만 두고 결론과 그림 라벨에는 넣지 않았습니다.</p>
<p>실행 1의 마지막 검색에서 첫 자리 거리는 <code>0.6</code>으로 줄었습니다. 그런데 첫 자리에 선 문서는 정답이 아닌 <code>LIB-001</code>이었습니다. 거리가 줄어도 정답 문서가 앞으로 온다고 볼 수 없는 자리입니다. 거리와 함께 정답 문서의 자리를 세어야 무엇이 달라졌는지 보입니다.</p>
<p>그 결과가 답에도 이어졌습니다. 실행 1의 답에는 정답 문서 ID 표시가 없었고 실행 2의 답에는 있었습니다. 다만 모델이 쓴 문장은 실행마다 달라질 수 있어 한 번 본 결과로 적습니다.</p>
{{mermaid:10-3-두-실행-비교|위에서 아래로 놓인 칸 두 개와 회색 상자 하나로 위 칸 제목은 실행 1이고 그 안에 초록 상자 후속 질문 늦으면 어떻게 되나요와 노란 상자 첫 자리 거리 0.64와 노란 상자 다시 검색한 횟수 1이 있으며 아래 칸 제목은 실행 2이고 그 안에 초록 상자 후속 질문 그날 못 가져오면 돈 내야 하나요와 노란 상자 첫 자리 거리 0.44와 노란 상자 다시 검색한 횟수 0이 있고 맨 아래 회색 상자 두 실행 모두 같은 대화 기록 두 줄과 같은 거리 기준값 0.5와 같은 정답 문서 LIB-002가 놓인 그림|후속 질문 하나만 바꿨더니 첫 자리 거리와 다시 검색한 횟수가 달라졌습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 위 칸이 실행 1이고 아래 칸이 실행 2입니다. 칸마다 맨 위 초록 상자가 우리가 바꾼 값입니다.</p>
<p class="look">그 아래 노란 상자 둘이 출력으로 확인한 값입니다. 두 칸에서 두 상자가 모두 갈렸습니다.</p>
<p class="look">맨 아래 회색 상자는 두 칸에서 모두 같게 둔 조건입니다. 한 실행의 결과가 아니라서 어느 칸에도 넣지 않았습니다.</p>
<p>요청 수는 실행 1이 다섯이고 실행 2가 넷이었습니다. 차이 한 번은 보정 질문을 받으려고 답 모델을 한 번 더 부른 것입니다. 답 모델 요청만 세면 셋과 둘입니다.</p>
<p>여기서 본 것은 문서 열두 건과 후속 질문 둘과 기준값 하나의 결과입니다. 보정 검색이 늘 자리를 뒤로 민다고 읽으면 안 됩니다. 06절은 같은 규칙으로 정답 문서를 첫 자리로 올렸습니다. 기능을 붙인 뒤에는 자리를 다시 세어 확인해야 한다는 것이 이 실습의 결론입니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2>
<ul>
<li><strong>후속 질문 둘은 탐색 실행 뒤에 골랐습니다.</strong> 자료의 여덟 질문은 모두 혼자서도 뜻이 통해 대화 기록이 필요 없습니다. 그래서 대화 두 줄과 후속 질문 둘을 손으로 적었습니다. 흐름의 두 갈래가 모두 보이게 고른 예입니다.</li>
<li><strong>거리 기준값 <code>0.5</code>도 탐색 실행 뒤에 정한 예입니다.</strong> 재작성한 질문의 첫 자리 거리를 먼저 보고 그 사이로 잡았습니다. 무엇을 재서 얻은 기준이 아닙니다.</li>
<li><strong>거리는 검색이 맞았는지 재는 값이 아닙니다.</strong> 실행 1은 보정 뒤에 거리가 줄었는데 정답 문서는 뒤로 밀렸습니다. 거리와 함께 정답 문서의 자리를 봐야 합니다.</li>
<li><strong>한 번 더 검색한다고 좋아지지 않습니다.</strong> 이 질문에서는 보정 질문이 대출 기간 문서 쪽으로 기울었습니다. 06절 결과와 반대 방향이고 둘 다 한 번씩 본 결과입니다.</li><li><strong>보정 뒤 정답 문서의 자리는 실행마다 달랐습니다.</strong> 하루 전 탐색 실행에서는 같은 후속 질문의 보정 뒤 정답 문서가 첫 자리였고 이번 실행에서는 첫 자리 밖이었습니다. 보정 질문 문장이 달라졌기 때문입니다. 그래서 보정 뒤 자리 번호는 본문 결론과 그림 라벨에 넣지 않았습니다.</li>
<li><strong>보정 갈래로 가지 않아도 검색은 두 번 합니다.</strong> 실행 2는 같은 글을 다시 검색하므로 결과가 같습니다. 갈래마다 코드를 나누지 않으려고 이렇게 두었습니다.</li>
<li><strong>모델이 쓴 문장은 실행마다 달라질 수 있습니다.</strong> 재작성한 질문과 보정 질문과 답이 모두 그렇습니다. 그래서 모델이 쓴 글에는 <code>assert</code>를 걸지 않았습니다.</li>
<li><strong>답에 붙은 문서 ID 표시는 한 번 본 결과입니다.</strong> 표시가 있는지와 답이 맞는지는 다른 물음입니다. 답 정확성 판정은 Ch 15 몫입니다.</li>
<li><strong>다시 검색 횟수 상한은 하나입니다.</strong> 보정 뒤에도 거리가 멀 수 있지만 이 실습은 더 검색하지 않습니다. 상한을 넘지 않았는지는 확인 줄로 봅니다.</li>
<li><strong>이 실습은 파일을 쓰지 않습니다.</strong> 자료 파일 둘은 읽기만 하고 고치지 않았습니다. 09절이 쓴 산출 파일도 건드리지 않았습니다.</li>
<li><strong>걸린 시간과 토큰과 비용은 이번에 재지 않았습니다.</strong> 서비스 요청 수만 코드로 셌습니다. 그래서 어느 갈래가 빠른지 적지 않습니다.</li>
<li><strong>임베딩 값은 호출마다 조금씩 달라집니다.</strong> 소수 둘째 자리까지 반올림해 보았고 그보다 작은 차이는 읽지 않았습니다.</li>
<li><strong>문서가 열두 건뿐입니다.</strong> 자리를 셀 때 재는 문서 수가 열둘이라 눈금이 성깁니다. 자료가 커지면 같은 기준값이 맞지 않을 수 있습니다.</li>
<li><strong>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.</strong> 패키지는 langchain 1.4.0과 langchain-openai 1.6.1, python-dotenv 1.2.3입니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li>
</ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2>
<ul>
<li>01절 질문 재작성과 06절 보정 검색과 01절 답 만들기를 한 흐름으로 이었습니다.</li>
<li>함수 다섯으로 나눠 묶었고 갈래는 첫 자리 거리와 기준값을 견주어 코드가 정했습니다.</li>
<li>실행 1은 첫 자리 거리가 <code>0.64</code>여서 보정 갈래로 갔고 답 모델을 세 번 불렀습니다.</li>
<li>실행 2는 후속 질문만 바꾸자 첫 자리 거리가 <code>0.44</code>가 되어 보정을 건너뛰었습니다.</li>
<li>견준 네 칸이 모두 갈렸고 요청을 한 번 더 쓴 실행에서도 이번에는 정답 문서가 첫 자리로 오지 않았습니다.</li>
<li>서비스 요청은 모두 열 번이었고 코드가 센 수와 미리 세어 둔 수가 같았습니다.</li>
</ul>
<p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 14가 끝납니다. Ch 15에서는 답이 맞는지와 근거가 있는지를 판정하는 방법을 배웁니다. 이 실습이 만든 답의 품질은 이번에 재지 않았습니다.</p>
<p>이 실습에서 고른 것은 검색에 넣을 글과 갈래입니다. 답 정확성과 근거 표시가 옳은지는 Ch 15 몫입니다. 들어온 글과 나가는 글을 막는 일은 Ch 16 몫입니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>
<details class="quiz" open><summary>문제 5개 · 해설 포함</summary>
<p class="quiz-q">1. [하] 두 실행에서 바꾼 값은 무엇입니까?</p>
<p class="quiz-a">후속 질문 하나입니다. 실행 1은 <code>늦으면 어떻게 되나요?</code>이고 실행 2는 <code>그날 못 가져오면 돈 내야 하나요?</code>입니다. 대화 기록과 거리 기준값과 문서와 정답 문서와 모델은 같게 두었습니다.</p>
<p class="quiz-q">2. [중] 다시 검색할지는 무엇을 보고 정합니까?</p>
<p class="quiz-a">재작성한 질문으로 검색한 첫 자리 거리를 거리 기준값과 견주어 정합니다. 거리가 기준값보다 크면 보정 질문을 받아 한 번 더 검색합니다. 06절 규칙을 그대로 가져온 자리입니다.</p>
<p class="quiz-q">3. [중] 거리 기준값을 06절 <code>0.65</code>에서 <code>0.5</code>로 바꾼 까닭은 무엇입니까?</p>
<p class="quiz-a">이 실습은 재작성한 질문으로 검색해 첫 자리 거리가 06절보다 작게 나오기 때문입니다. 탐색 실행에서 두 값이 <code>0.5</code>의 위와 아래로 갈려 그 사이로 잡았습니다. 두 갈래가 모두 보이게 하려고 정한 예입니다.</p>
<p class="quiz-q">4. [중] 실행 1에서 보정 뒤에 거리가 줄었는데 무엇이 나빠졌습니까?</p>
<p class="quiz-a">이번 실행에서는 정답 문서가 첫 자리로 오지 않았습니다. 첫 자리에 선 문서도 정답이 아니었습니다. 거리 하나만 보면 이 변화가 보이지 않습니다. 보정 뒤 자리 번호는 실행마다 달라져 여기에 적지 않습니다.</p>
<p class="quiz-q">5. [상] 동료가 「보정 검색을 붙이면 검색이 더 좋아진다」라고 적었습니다. 이 절 출력으로 무엇이라고 답하나요?</p>
<p class="quiz-a">이번 실행에서는 정답 문서가 첫 자리로 오지 않았다고 답합니다. 06절 질문에서는 같은 규칙이 정답 문서를 첫 자리로 올렸습니다. 같은 후속 질문도 하루 전 탐색 실행에서는 반대 방향이었습니다. 기능을 붙인 뒤에는 정답 문서의 자리를 다시 세어 확인해야 합니다.</p>
</details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2>
<ul>
<li><div><a href="https://docs.langchain.com/oss/python/concepts/providers-and-models">LangChain 모델과 provider</a></div>확인 2026-09-20 · LangChain 1.4 기준 · 재작성과 보정과 답을 받을 모델을 준비하는 방법.</li>
<li><div><a href="https://developers.openai.com/api/docs/models/text-embedding-3-small">OpenAI text-embedding-3-small 모델 안내</a></div>확인 2026-09-20 · 문서와 질문을 벡터로 바꿀 때 쓴 모델과 차원 수 설정.</li>
<li>Ch 14 01절 대화 히스토리와 질문 재작성 — 이 실습이 이어 쓴 재작성 머리글과 답 머리글이 있는 자리.</li>
<li>Ch 14 06절 CRAG — 이 실습이 이어 쓴 판정 규칙과 보정 검색 규칙이 있는 자리.</li>
<li>Ch 12 01·05절 — 이 실습이 이어 쓴 코사인 거리 함수와 거리 순위 만들기가 있는 자리.</li>
<li>기준 버전은 langchain 1.4.0과 langchain-openai 1.6.1, python-dotenv 1.2.3입니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.</li>
</ul>
"""


def write_src() -> Path:
    SRC.write_text(SRC_HTML, encoding="utf-8")
    return SRC


if __name__ == "__main__":
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "10", "10-RAG-패턴-실습", "experiment", cells())
        print("wrote", path)
