"""Ch 14 03절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§3·§6).

사용:
  python3 author_03.py            → 노트북 + _src 본문을 함께 다시 쓴다
  python3 author_03.py --src-only → 본문 HTML만 다시 쓴다(노트북 출력을 지우지 않는다)

이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북과 본문은 qa/upgrade/before/ 에 있다. **experiment 형식 유지**(chapter.json).

## 가져온 함수 일곱 개 (§2-7 리팩터 2026-09-21 — 도구 파일 `notebooks/rag_tools.py`)

준비 셀(import 셀)에서 Ch 12·Ch 11 함수 다섯(`rank_by_distance`·`print_ranked`·`unique_doc_ids`·`find_gold_rank`·
`fuse_rank(…, rank_constant)`)과 02절 `split_lines`·`search_ids(embedding_model, question, doc_vectors, doc_ids, top_count)`를
가져온다. 순위 합치기 값 셀(`rank_constant` 60·`base_weight` 1.0)은 노트북에 남긴다.
리팩터 전에는 이 함수들(+ `dot_product`·`vector_length`·`fuse_scores`)을 준비 셀 여섯에 다시 적었다.

## 이 절이 새로 만든 함수 둘

`build_sub_prompt(question)` — 사실 하나씩만 묻는 하위 질문을 받는 머리글을 만든다.
`run_row(run_name, found_ids, first_place, second_place)` — 실행 한 번을 기록 한 줄로 만든다(칸이 01절 판과 달라 노트북에 둔다).
기록 칸이 01·02절(실행·검색에 쓴 질문·첫 자리 문서·정답 자리)과 다르다. 이 절은 근거 문서가
둘이라 자리도 둘이기 때문이다. 인자 수와 반환 모양(한국어 키 딕셔너리)은 같다.

## 선택한 것과 까닭

1. **사실이 둘 섞인 질문을 자료의 질문 둘을 붙여 만들었다.** 자료의 여덟 질문에는 사실이 둘
   섞인 질문이 없다. 손으로 새 질문을 쓰면 근거 문서가 자료의 정답과 이어지지 않는다. 그래서
   `queries[4]`(`C05`)와 `queries[7]`(`C08`)을 `" 그리고 "`로 이어 붙였다. 근거 문서 둘은
   자료가 적어 둔 `FAC-003`·`ACC-003`이다. 어느 둘을 붙일지는 탐색 실행으로 정했다(아래 §탐색).
2. **하위 질문마다 첫 자리 문서를 모아 근거 문서 목록을 만든다.** 이것이 이 절의 출력이다.
   02절은 목록 넷을 순위 합치기로 하나로 만들었다. 03절 하위 질문은 다른 것을 묻기 때문에
   목록을 합치면 첫 자리에 두 사실의 근거가 아닌 문서가 온다. 합친 뒤 두 근거의 자리는 새 커널
   두 번 실행에서 달라져 결론과 그림에서 뺐고, 두 실행에서 같았던 값만 본문에 적었다.
3. **순위 합치기는 Ch 12 06절 판을 그대로 쓴다.** `fuse_rank`(안에서 `fuse_scores`)를
   도구 파일에서 가져온다(§2-7 리팩터 전에는 02절 판을 준비 셀에 다시 적었다). 순위 상수 `60`·가중치 `1.0`도 같다. 합친 결과가 좋아지지 않았지만
   방법을 바꾸지 않았다. 같은 방법을 두 자리에 써 보아야 차이가 보이기 때문이다.
4. **값 바꿔 보기는 두 사실이 한 문서에 있는 질문이다.** 하위 질문 둘이 같은 문서를 찾아 근거
   문서가 하나에 그친다. 나누는 일이 늘 근거를 늘리지는 않는다는 것을 같은 코드로 보인다.
5. **걸린 시간과 비용 추정을 넣지 않는다.** Ch 12부터 이 과정은 걸린 시간을 한 번도 재지 않았다.
6. **모델 이름을 `gpt-5.4-mini`로 바꿨다**(규격 §6 기준 버전). b10의 옛 모델 단가 줄도 뺐다.
7. **모델 답에 `assert`를 걸지 않는다**(규격 §3). `assert`는 키 확인과 자리 확인 두 곳뿐이다.
8. **쓰지 않은 것**(벡터 계산은 도구 파일 안 NumPy): `lambda`·내포식·제너레이터 식·조건 표현식·f-string·`key=`·`reverse=`·
   `set`·기본값 매개변수·복합 타입힌트·세미콜론·한 줄 다중 대입·클래스 정의·`time`·`enumerate`·
   `zip`·`next`. 부른 내장 이름은 `len`·`open`·`print`·`range`·`round`·`sorted`·`str`뿐이다.

## 탐색 실행에서 확인한 값 (2026-09-19, /tmp/ch14-03/probe1.py~probe7.py)

langchain 1.4.0 · langchain-openai 1.6.1 · Python 3.12.13 · 문서 12건 · 질문 8건.
손으로 쓴 두 사실 질문 열여덟 개와 자료 질문을 둘씩 붙인 스물여덟 개를 모두 재어 보았다.
`C05`+`C08`만 한 번 검색에서 둘째 근거가 자리 여섯으로 앞 세 자리 밖으로 밀렸고, 하위 질문
둘이 각각 자리 하나를 찾았다. 붙여 만든 질문의 한 번 검색은 `FAC-003` 자리 하나·`ACC-003`
자리 여섯이고, 하위 질문 둘의 첫 자리 문서는 `FAC-003`과 `ACC-003`이다. 목록 셋을 합치면
첫 자리에 두 사실의 근거가 아닌 `FAC-004`가 온다. **합친 뒤 두 근거의 자리는 하위 질문 문장에
따라 흔들려** 본문·그림·정리에서 뺐다(새 커널 두 번 실행 기록은 `03-diagnosis.md` §4).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part4/ch14-rag-patterns/notebooks"
SRC = ROOT / "textbook/part4/ch14-rag-patterns/_src/03-질의-분해.html"

INSTALL = install_source([
    "langchain==1.4.0", "langchain-openai==1.6.1", "python-dotenv==1.2.3", "numpy==2.5.3",
])

IMPORTS = r'''# 자료 읽기·폴더 확인과 임베딩·답 모델 이름을 불러옵니다
import json
import os

from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model
# Ch 12 01·05·06절·Ch 11 01절 함수와 02절 함수를 도구 파일에서 가져옵니다
from rag_tools import find_gold_rank, fuse_rank, print_ranked, rank_by_distance
from rag_tools import search_ids, split_lines, unique_doc_ids

print("불러온 이름:", "json", "os", "OpenAIEmbeddings", "init_chat_model")'''

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

VALUES = r'''# Ch 12에서 쓴 값을 그대로 다시 정하고 나눌 하위 질문 개수도 못 박습니다
top_three = 3
top_all = 12
sub_count = 2
print("나란히 볼 상위 문서 수:", top_three)
print("자리를 셀 때 재는 문서 수:", top_all)
print("나눌 하위 질문 수:", sub_count)'''

DOC_TEXTS = r'''# 문서 12개의 제목과 본문을 이어 붙이고 문서 ID 목록도 만듭니다(Ch 12와 같은 제목 + 본문 모양)
doc_texts = []
doc_ids = []
for doc in docs:
    doc_texts.append(doc["title"] + " " + doc["text"])
    doc_ids.append(doc["doc_id"])
print("이어 붙인 글 수:", len(doc_texts))
print("첫 문서 글:", doc_texts[0])
print("문서 ID 목록:")
print(doc_ids)'''


FUSE_VALUES = r'''# Ch 12 06절 순위 합치기에 쓸 값 두 개를 02절과 같게 다시 정합니다
rank_constant = 60
base_weight = 1.0
print("순위 상수:", rank_constant)
print("목록 하나에 줄 가중치:", base_weight)'''


EMBEDDINGS = r'''# Ch 12와 같은 모델로 문서 12개를 벡터로 바꿉니다(임베딩 요청 1번)
embedding_model_name = "text-embedding-3-small"
vector_dimensions = 256
embedding_model = OpenAIEmbeddings(model=embedding_model_name, dimensions=vector_dimensions)
doc_vectors = embedding_model.embed_documents(doc_texts)
print("임베딩 모델 이름:", embedding_model.model)
print("벡터의 숫자 개수 설정:", embedding_model.dimensions)
print("문서 벡터 수:", len(doc_vectors))'''

PICK_QUESTION = r'''# 자료의 질문 둘을 한 문장으로 이어 붙여 사실이 둘 섞인 질문을 만듭니다
first_query = queries[4]
second_query = queries[7]
mixed_question = first_query["question"] + " 그리고 " + second_query["question"]
first_gold = first_query["gold_doc_id"]
second_gold = second_query["gold_doc_id"]
print("이어 붙인 질문 번호:", first_query["qid"], "|", second_query["qid"])
print("만든 질문:", mixed_question)
print("첫째 사실의 근거 문서 ID:", first_gold)
print("둘째 사실의 근거 문서 ID:", second_gold)'''

BASE_SEARCH = r'''# 만든 질문을 한 번만 검색해 순위 표와 두 근거 문서의 자리를 봅니다(임베딩 요청 1번)
mixed_vector = embedding_model.embed_query(mixed_question)
base_hits = rank_by_distance(mixed_vector, doc_vectors, doc_ids, top_all)
base_ids = unique_doc_ids(base_hits)
base_first = find_gold_rank(base_ids, [first_gold])
base_second = find_gold_rank(base_ids, [second_gold])
print_ranked(base_hits[:top_three], "거리")
print("한 번 검색했을 때 첫째 근거 문서의 자리:", base_first)
print("한 번 검색했을 때 둘째 근거 문서의 자리:", base_second)'''

BUILD_SUB_PROMPT = r'''# 머리글 네 줄과 원 질문을 한 글로 이어 붙입니다
def build_sub_prompt(question):
    sub_head = "아래 질문에는 서로 다른 사실이 섞여 있습니다.\n"
    sub_head = sub_head + "사실 하나씩만 묻는 검색 질문을 " + str(sub_count) + "줄 적으세요.\n"
    sub_head = sub_head + "한 줄에 질문 하나만 적고 번호나 기호를 붙이지 마세요.\n"
    sub_head = sub_head + "원 질문에 없는 조건을 새로 넣지 마세요.\n\n"
    prompt_text = sub_head + "질문: " + question
    return prompt_text'''

SUB_CALL = r'''# 만든 글을 모델에 넣어 하위 질문을 받습니다(모델 요청 1번)
sub_prompt = build_sub_prompt(mixed_question)
print("모델에 넣을 글:")
print(sub_prompt)
sub_reply = model.invoke(sub_prompt)
sub_text = sub_reply.text.strip()
print("모델이 쓴 글:")
print(sub_text)'''

SPLIT_CALL = r'''# 모델이 보낸 글을 줄로 나누고 앞에서 정한 개수만 골라 씁니다
sub_lines = split_lines(sub_text)
sub_questions = sub_lines[:sub_count]
print("모델이 보낸 줄 수:", len(sub_lines))
print("쓸 하위 질문 수:", len(sub_questions))
for sub_question in sub_questions:
    print("하위 질문:", sub_question)'''

SUB_SEARCH = r'''# 하위 질문마다 따로 검색해 첫 자리 문서를 모아 근거 문서 목록을 만듭니다(임베딩 요청 2번)
sub_rankings = []
top_hits = []
for sub_question in sub_questions:
    found_ids = search_ids(embedding_model, sub_question, doc_vectors, doc_ids, top_all)
    sub_rankings.append(found_ids)
    top_hits.append({"doc_id": found_ids[0]})
    print("하위 질문 첫 자리 문서:", found_ids[0])
evidence_ids = unique_doc_ids(top_hits)
print("근거 문서 목록:", evidence_ids)'''

FUSE_BUILD = r'''# 원 질문 목록 뒤에 하위 질문 목록 둘을 붙이고 목록마다 같은 가중치를 줍니다
ranking_list = []
weight_list = []
ranking_list.append(base_ids)
weight_list.append(base_weight)
for found_ids in sub_rankings:
    ranking_list.append(found_ids)
    weight_list.append(base_weight)
print("합칠 목록 수:", len(ranking_list))
print("쓴 가중치:", weight_list)'''

FUSE_CALL = r'''# 목록 셋을 순위 합치기로 하나로 만들고 두 근거 문서의 자리를 봅니다
fused_ids = fuse_rank(ranking_list, weight_list, rank_constant)
fused_first = find_gold_rank(fused_ids, [first_gold])
fused_second = find_gold_rank(fused_ids, [second_gold])
print("합친 목록의 앞 세 자리:", fused_ids[:top_three])
print("합친 뒤 첫째 근거 문서의 자리:", fused_first)
print("합친 뒤 둘째 근거 문서의 자리:", fused_second)'''

RUN_ROW = r'''# 실행 한 번을 기록 한 줄로 만듭니다
def run_row(run_name, found_ids, first_place, second_place):
    row = {"실행": run_name}
    row["첫 자리 문서"] = found_ids[0]
    row["첫째 근거 자리"] = first_place
    row["둘째 근거 자리"] = second_place
    return row'''

TABLE = r'''# 네 실행의 기록을 담아 라벨 줄 아래에 한 줄씩 출력합니다
run_rows = []
run_rows.append(run_row("한 번 검색", base_ids, base_first, base_second))
for found_ids in sub_rankings:
    place_one = find_gold_rank(found_ids, [first_gold])
    place_two = find_gold_rank(found_ids, [second_gold])
    run_rows.append(run_row("하위 질문 검색", found_ids, place_one, place_two))
run_rows.append(run_row("세 목록 합치기", fused_ids, fused_first, fused_second))
print("실행 | 첫 자리 문서 | 첫째 근거 자리 | 둘째 근거 자리")
for row in run_rows:
    print(row["실행"], "|", row["첫 자리 문서"], "|", row["첫째 근거 자리"], "|", row["둘째 근거 자리"])'''

SECOND_PICK = r'''# 바꿀 값은 검색에 쓸 질문 하나이고 이번에는 두 사실이 한 문서에 함께 있습니다(임베딩 요청 1번)
second_question = "휴학 중 원격 전자자료를 볼 수 있나요? 그리고 휴학 중 일반 도서를 빌릴 수 있나요?"
second_doc = "ACC-002"
second_ids = search_ids(embedding_model, second_question, doc_vectors, doc_ids, top_all)
second_place = find_gold_rank(second_ids, [second_doc])
print("바꾼 질문:", second_question)
print("두 사실이 함께 있는 문서 ID:", second_doc)
print("한 번 검색했을 때 그 문서의 자리:", second_place)'''

SECOND_SUB = r'''# 같은 머리글로 바꾼 질문을 나누어 하위 질문을 받습니다(모델 요청 1번)
second_prompt = build_sub_prompt(second_question)
second_reply = model.invoke(second_prompt)
second_text = second_reply.text.strip()
second_lines = split_lines(second_text)
second_subs = second_lines[:sub_count]
print("모델이 보낸 줄 수:", len(second_lines))
for sub_question in second_subs:
    print("하위 질문:", sub_question)'''

SECOND_SEARCH = r'''# 바꾼 질문의 하위 질문마다 검색해 같은 방법으로 근거 문서 목록을 만듭니다(임베딩 요청 2번)
second_hits = []
for sub_question in second_subs:
    found_ids = search_ids(embedding_model, sub_question, doc_vectors, doc_ids, top_all)
    second_hits.append({"doc_id": found_ids[0]})
    print("하위 질문 첫 자리 문서:", found_ids[0])
second_evidence = unique_doc_ids(second_hits)
print("근거 문서 목록:", second_evidence)'''

TITLE = """# 질의 분해

**이 노트북에서 할 일**

1. Ch 12에서 쓰던 문서 열두 건과 질문 여덟 개를 그대로 읽습니다.
2. 자료의 질문 둘을 이어 붙여 사실이 둘 섞인 질문을 만듭니다.
3. 그 질문을 한 번만 검색해 두 근거 문서의 자리를 셉니다.
4. 같은 질문을 하위 질문 둘로 나눠 각각 검색하고 근거 문서 목록을 만듭니다.
5. 목록 셋을 Ch 12 순위 합치기로 하나로 만들어 자리를 다시 셉니다.
6. 질문만 바꾸어 같은 일을 다시 하고 두 결과를 견줍니다.

**준비물** — 이 절은 프로젝트 맨 위 폴더의 `.env`에 적어 둔 `OPENAI_API_KEY`를 씁니다.
서비스 요청은 아홉 번입니다(임베딩 일곱 번과 답 모델 두 번).
예상 비용은 미화 0.01달러 아래입니다.
읽어 오는 파일은 이 챕터 폴더의 문서 파일과 질문 파일 둘이고 새로 쓰는 파일은 없습니다.
실행 시간은 2분 안팎이고 첫 셀의 설치가 가장 오래 걸립니다.

**기준 버전** — 첫 셀에서 LangChain 1.4.0과 langchain-openai 1.6.1을 설치합니다.
키를 읽는 python-dotenv 1.2.3과 도구 파일이 쓰는 numpy 2.5.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3절부터 7절까지 읽습니다.
Ch 12 검색 부품과 순위 합치기 부품을 준비하고 사실이 둘 섞인 질문을 만드는 자리입니다.
8절과 9절은 하위 질문을 만들고 근거 문서 목록을 모으는 자리입니다.
10절부터 12절은 목록을 합치고 질문을 바꾸어 다시 재는 자리입니다.

실습 폴더 `labs/part4/ch14-rag-patterns`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""

FIGURE_ALT = ("위에서 아래로 놓인 상자 여섯으로 맨 위에 초록 상자 사실이 둘 섞인 질문이 있고 그 아래 "
              "파란 상자 우리가 적은 나누기 머리글과 보라 상자 답 모델 gpt-5.4-mini를 지나 노란 상자 "
              "하위 질문 두 줄로 이어지며 그 아래 파란 상자 하위 질문마다 거리 검색을 거쳐 맨 아래 "
              "노란 상자 근거 문서 FAC-003과 ACC-003으로 이어지는 그림")

FIGURE_READ = """위에서 아래로 읽습니다.
맨 위 초록 상자가 사람이 적은 질문입니다.
가운데 파란 상자 둘이 우리가 적은 글과 처리이고 보라 상자가 모델입니다.
맨 아래 노란 상자 둘이 출력으로 확인한 값입니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIGURE_ALT + "](attachment:03-1-한-질문에-섞인-사실-둘-나누기.png)\n\n" + FIGURE_READ, html="skip"),
        md("""## 1. 준비

첫 셀은 패키지 네 개를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 판 번호 네 줄이 보입니다.
마지막 줄 `numpy: 2.5.3`은 도구 파일이 벡터 계산에 쓰는 패키지입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이름 네 개를 불러오고 도구 파일에서 함수 일곱 개를 가져옵니다.
앞의 둘은 자료 읽기와 폴더 확인에 씁니다.
뒤의 둘은 Ch 9~13에서 쓴 임베딩과 답 모델 이름입니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.

이 노트북은 Ch 12 01절 `rank_by_distance()`와 05절 `print_ranked()`를 가져옵니다.
Ch 11 01절 `unique_doc_ids()`·`find_gold_rank()`와 Ch 12 06절 `fuse_rank()`도 가져옵니다.
02절에서 만든 `split_lines()`와 `search_ids()`도 함께 가져옵니다.
인자 모양은 5절에서 설명합니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄에 불러온 이름 네 개가 보입니다.
이름 `OpenAIEmbeddings`와 `init_chat_model`은 02절에서 쓴 것과 같습니다.
도구 파일에서 가져온 함수 일곱 개는 출력하지 않습니다.

## 2. 키와 모델 준비"""),
    ] + key_and_model_cells("openai:gpt-5.4-mini") + [
        md("""## 3. 문서와 질문 읽기

이 절은 01·02절과 같은 문서 파일과 질문 파일을 읽습니다.
두 파일은 Ch 12 core 벌 파일과 바이트가 같은 사본입니다.
먼저 노트북을 연 자리에서 프로젝트 맨 위를 찾습니다."""),
        code(ROOT_PATH),
        md("""**결과 읽기** — 출력 줄 `고른 자리` 뒤에 점 하나나 위로 올라가는 표시가 보입니다.
Ch 10~13과 01·02절에서 쓴 방법과 같습니다.
후보 셋 가운데 이 챕터 자료 폴더가 있는 자리를 고릅니다.

다음 셀은 문서 파일과 질문 파일을 읽습니다."""),
        code(LOAD_DATA),
        md("""**결과 읽기** — 출력 줄 `문서 수: 12`와 `질문 수: 8`이 Ch 12 core 벌 그대로입니다.
문서는 도서관 안내 열두 건입니다.

질문 번호는 C01부터 C08까지이고 질문 파일에 적혀 있습니다.
이 절은 그 가운데 둘을 이어 붙여 씁니다.

## 4. 이 절에서 쓸 값 정하기

Ch 12와 01·02절에서 정한 값을 그대로 다시 적습니다.
나눌 하위 질문 개수도 여기서 못 박아 둡니다."""),
        code(VALUES),
        md("""**결과 읽기** — 출력 줄 `나란히 볼 상위 문서 수: 3`은 표로 볼 자리 수입니다.
출력 줄 `자리를 셀 때 재는 문서 수: 12`는 근거 문서의 자리를 끝까지 세려고 둔 값입니다.
출력 줄 `나눌 하위 질문 수: 2`는 이 절이 만들 하위 질문 개수입니다.

개수를 값으로 적어 두면 늘어난 요청 수를 셀 수 있습니다.
하위 질문 하나마다 임베딩 요청이 한 번씩 늘어납니다.

## 5. 앞 절 부품 준비

다음 두 셀은 01·02절에서 이미 본 준비입니다.
읽지 말고 실행만 하고 넘어가도 됩니다.
문서 글을 이어 붙이고 순위 합치기에 쓸 값 둘을 02절과 같게 적습니다.
함수는 준비 셀에서 도구 파일로 가져왔습니다."""),
        code(DOC_TEXTS, lesson_role="setup"),
        code(FUSE_VALUES, lesson_role="setup"),
        md("""준비 셀 두 개를 지났습니다.
함수 `search_ids`는 질문 하나를 벡터로 바꿔 문서 ID 순위 목록을 만듭니다.
부를 때마다 임베딩 요청이 한 번씩 갑니다.
도구 파일 판은 임베딩 모델과 질문과 문서 벡터 목록과 문서 ID 목록과 개수를 받습니다.
함수 `fuse_rank`는 목록과 가중치 목록 뒤에 순위 상수를 셋째 인자로 받습니다.

## 6. 문서를 벡터로 바꾸기

다음 셀은 문서 열두 건을 벡터로 바꿉니다.
이 절에서 서비스에 보내는 첫 요청입니다."""),
        code(EMBEDDINGS),
        md("""**결과 읽기** — 출력 줄 `임베딩 모델 이름: text-embedding-3-small`은 02절과 같은 모델입니다.
출력 줄 `벡터의 숫자 개수 설정: 256`도 Ch 10~13과 같은 값입니다.
출력 줄 `문서 벡터 수: 12`로 문서마다 벡터 하나를 받았습니다.
벡터 안의 숫자는 호출마다 아주 조금씩 달라져 소수 자리까지 같다고 보지 않습니다.

## 7. 사실이 둘 섞인 질문 만들기

자료의 여덟 질문은 저마다 사실 하나만 묻습니다.
그래서 질문 둘을 한 문장으로 이어 붙여 사실이 둘 섞인 질문을 만듭니다.
이어 붙이면 근거 문서 둘도 자료가 적어 둔 값 그대로 쓸 수 있습니다."""),
        code(PICK_QUESTION),
        md("""**결과 읽기** — 출력 줄 `이어 붙인 질문 번호: C05 | C08`로 두 질문을 골랐습니다.
출력 줄 `만든 질문` 뒤에 두 물음이 한 문장으로 이어져 있습니다.
출력 줄 `첫째 사실의 근거 문서 ID: FAC-003`은 운영 시간을 적은 문서입니다.
출력 줄 `둘째 사실의 근거 문서 ID: ACC-003`은 학생증 분실을 적은 문서입니다.

실행 전에 예상해 봅니다.
질문 앞쪽 말이 운영 시간 문서와 가까우니 그쪽으로 쏠릴 것입니다."""),
        code(BASE_SEARCH),
        md("""**결과 읽기** — 순위 표의 차례는 `FAC-003`과 `ACC-002`와 `FAC-004`입니다.
가운데 `ACC-002`는 두 사실 어느 쪽의 근거도 아닙니다.
출력 줄 `한 번 검색했을 때 첫째 근거 문서의 자리: 1`로 앞쪽 사실은 첫 자리를 찾았습니다.
출력 줄 `한 번 검색했을 때 둘째 근거 문서의 자리: 6`으로 뒤쪽 사실은 여섯째 자리였습니다.

순위 표 둘째 줄과 셋째 줄의 거리가 `0.66`으로 같아 보입니다.
줄 세우기는 반올림 전 값으로 했고 그 두 줄의 차례는 결과로 읽지 않습니다.
거리 값은 셋째 자리 아래가 호출마다 달라져 본문과 그림에 넣지 않았습니다.

## 8. 하위 질문으로 나누기

사실 하나씩만 묻는 검색 질문을 두 줄 받습니다.
머리글에 개수와 모양을 적어 한 줄에 질문 하나만 오게 합니다.
원 질문에 없는 조건을 새로 넣지 말라는 줄도 함께 넣습니다."""),
        code(BUILD_SUB_PROMPT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `build_sub_prompt`는 머리글 네 줄을 이어 붙인 뒤 원 질문을 답니다.
머리글의 개수 자리에는 앞에서 정한 값 `sub_count`가 들어갑니다.
값을 바꾸면 머리글과 실제로 쓰는 개수가 함께 바뀝니다.

다음 셀은 그 글을 만들어 모델에 넣습니다."""),
        code(SUB_CALL),
        md("""**결과 읽기** — 라벨 줄 `모델에 넣을 글:` 아래에 머리글 네 줄과 원 질문이 있습니다.
라벨 줄 `모델이 쓴 글:` 아래에는 질문 두 줄이 있습니다.
앞 줄은 닫는 시각만 묻고 뒷줄은 분실한 카드만 묻습니다.
문장은 실행마다 달라질 수 있어 이 값에 `assert`를 걸지 않았습니다.

02절 변형 질문은 모두 같은 것을 물었습니다.
이 절 하위 질문은 서로 다른 것을 묻습니다.

## 9. 하위 질문마다 검색하기

모델이 보낸 글은 줄 하나가 질문 하나입니다.
02절에서 만든 함수로 빈 줄만 빼고 앞의 두 줄을 고릅니다."""),
        code(SPLIT_CALL),
        md("""**결과 읽기** — 출력 줄 `모델이 보낸 줄 수: 2`로 두 줄이 왔습니다.
출력 줄 `쓸 하위 질문 수: 2`는 앞에서 정한 개수와 같습니다.
라벨 줄 `하위 질문:` 두 줄에 실제로 쓸 질문이 있습니다.
받은 줄이 더 많아도 앞의 두 줄만 씁니다.

적게 오면 온 만큼만 씁니다.
그때는 `쓸 하위 질문 수`가 `나눌 하위 질문 수`보다 작게 나옵니다.

다음 셀은 하위 질문마다 따로 검색합니다."""),
        code(SUB_SEARCH),
        md("""**결과 읽기** — 라벨 줄 `하위 질문 첫 자리 문서:` 두 줄에 서로 다른 문서가 있습니다.
출력 줄 `근거 문서 목록: ['FAC-003', 'ACC-003']`이 이 절이 얻으려던 값입니다.
하위 질문 하나마다 근거 문서 하나가 짝지어졌습니다.
사실이 둘이니 근거 문서도 둘입니다.

한 번 검색했을 때는 뒤쪽 사실의 근거가 여섯째 자리였습니다.
나눠서 검색하니 그 문서가 자기 하위 질문의 첫 자리로 왔습니다.

## 10. 목록 셋을 하나로 합치기

02절은 목록 넷을 순위 합치기로 하나로 만들었습니다.
같은 방법을 이 절 목록 셋에도 써 봅니다.
원 질문 목록도 함께 넣어 하위 질문이 빗나갔을 때 기댈 자리를 남깁니다."""),
        code(FUSE_BUILD),
        md("""**결과 읽기** — 출력 줄 `합칠 목록 수: 3`으로 목록이 셋입니다.
출력 줄 `쓴 가중치: [1.0, 1.0, 1.0]`으로 세 목록을 같게 봤습니다.
첫 목록은 원 질문이고 뒤의 둘은 하위 질문입니다.

다음 셀은 세 목록을 하나로 만듭니다."""),
        code(FUSE_CALL),
        md("""**결과 읽기** — 출력 줄 `합친 목록의 앞 세 자리`의 맨 앞은 `FAC-004`입니다.
그 문서는 두 사실 어느 쪽의 근거도 아닙니다.
아래 두 줄에 두 근거 문서가 몇째 자리인지 있습니다.

순위 합치기는 여러 목록에서 고르게 앞자리인 문서를 위로 올립니다.
하위 질문 둘은 다른 것을 물어 서로의 목록에서 뒷자리에 있었습니다.
그래서 고르게 앞자리인 문서가 두 사실과 상관없는 문서였습니다.
다른 것을 묻는 목록에는 하나로 합치기보다 첫 자리 문서를 따로 모으는 쪽이 맞습니다.

이번 새 커널 두 번 실행에서는 합친 뒤 두 근거의 자리가 같았습니다.
다만 하위 질문 문장이 조금 바뀌면 합친 자리도 함께 바뀌어 앞선 새 커널 실행에서는 다른 값이 나왔습니다.
그래서 이 두 숫자는 본문과 그림과 정리에 넣지 않았습니다.

## 11. 네 실행을 기록 한 줄씩으로

실행 하나를 기록 한 줄로 만들어 담아 둡니다.
Ch 9~13과 01·02절에서 쓴 기록 한 줄과 같은 모양입니다.
담는 칸만 이 절에 맞게 근거 자리 둘로 둡니다."""),
        code(RUN_ROW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
담는 칸은 실행 이름과 첫 자리 문서와 근거 자리 둘입니다.
이 절이 견주는 값이 그 넷이기 때문입니다.

다음 셀은 네 실행의 기록을 표로 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 `실행 | 첫 자리 문서 | 첫째 근거 자리 | 둘째 근거 자리` 아래 네 줄이 나옵니다.
첫 줄 `한 번 검색`의 근거 자리는 `1`과 `6`입니다.
가운데 두 줄에서 하위 질문마다 한쪽 근거만 첫 자리로 옵니다.
마지막 줄 `세 목록 합치기`의 첫 자리 문서는 `FAC-004`입니다.

가운데 두 줄의 뒤 숫자와 마지막 줄의 근거 자리 둘은 하위 질문 문장에 따라 달라질 수 있습니다.
그래서 본문과 그림에는 이 값들을 적지 않았습니다.

## 12. 값 바꿔 보기 · 두 사실이 한 문서에 있는 질문

바꿀 값은 검색에 쓸 질문 하나입니다.
머리글도 하위 질문 개수도 그대로 두고 질문만 바꿉니다.
이번 질문의 두 사실은 한 문서에 함께 적혀 있습니다.
실행 전에 예상해 봅니다.
하위 질문 둘이 같은 문서를 찾아 근거 문서가 하나에 그칠 것입니다."""),
        code(SECOND_PICK),
        md("""**결과 읽기** — 출력 줄 `바꾼 질문` 뒤에 두 물음이 한 문장으로 이어져 있습니다.
출력 줄 `두 사실이 함께 있는 문서 ID: ACC-002`는 휴학생 권한을 적은 문서입니다.
출력 줄 `한 번 검색했을 때 그 문서의 자리: 1`로 한 번 검색으로도 첫 자리였습니다.

다음 셀은 같은 머리글로 하위 질문을 다시 받습니다."""),
        code(SECOND_SUB),
        md("""**결과 읽기** — 출력 줄 `모델이 보낸 줄 수: 2`로 이번에도 두 줄이 왔습니다.
라벨 줄 `하위 질문:` 두 줄에 원격 이용과 도서 대출을 묻는 질문이 있습니다.
문장은 실행마다 달라질 수 있습니다.

다음 셀은 하위 질문마다 같은 방법으로 검색합니다."""),
        code(SECOND_SEARCH),
        md("""**결과 읽기** — 라벨 줄 `하위 질문 첫 자리 문서:` 두 줄이 모두 `ACC-002`입니다.
출력 줄 `근거 문서 목록: ['ACC-002']`로 근거 문서가 하나입니다.
두 사실이 한 문서에 함께 적혀 있어 나눠도 근거가 늘지 않았습니다.
나누는 일이 늘 근거를 늘리지는 않습니다.

## 정리

1. 사실이 둘 섞인 질문을 한 번만 검색하니 뒤쪽 사실의 근거가 여섯째 자리였습니다.
2. 하위 질문 둘로 나눠 검색하니 근거 문서 목록에 서로 다른 문서 둘이 담겼습니다.
3. 같은 목록 셋을 순위 합치기로 합치니 첫 자리에 두 사실의 근거가 아닌 문서가 왔습니다.
4. 두 사실이 한 문서에 있는 질문에서는 나눠도 근거 문서가 하나였습니다.

04절에서는 질문을 잘게 나누는 대신 한 단계 넓혀 일반 규칙을 찾습니다.
이 절이 만든 하위 질문은 원 질문보다 좁고 04절 질문은 원 질문보다 넓습니다."""),
    ]


SRC_HTML = """<!--meta: 강의 1h | 실습 2h | 코드 notebooks/03-질의-분해.ipynb | 새 용어 2 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>한 질문에 섞인 사실을 하위 질문 둘로 나눌 수 있습니다.</li>
<li>하위 질문마다 첫 자리 문서를 모아 근거 문서 목록을 만들 수 있습니다.</li>
<li>목록을 하나로 합쳤을 때 첫 자리에 근거가 아닌 문서가 오는 것을 확인할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>사람은 한 번에 두 가지를 묻습니다. 「토요일에 언제 닫나요」와 「분실한 카드를 어떻게 막나요」가 한 문장에 섞입니다. 이런 질문을 그대로 검색하면 한쪽 사실로 쏠립니다. 다른 쪽 사실의 근거 문서는 뒤로 밀립니다.</p><p>Ch 9의 기본 RAG는 검색 한 번과 답 한 번이었습니다. 01절은 검색 앞에서 질문을 바꾸는 단계를 붙였고 02절은 질문을 여러 개로 늘렸습니다. 이 절은 같은 자리에서 질문을 사실별로 나눕니다. 나눈 질문마다 따로 검색하면 사실마다 근거 문서를 짝지을 수 있습니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>02절은 질문 하나를 변형 질문 셋으로 늘렸습니다. 늘린 질문 넷은 모두 같은 것을 물었습니다. 이 절은 같은 자리에서 다른 것을 묻는 질문으로 나눕니다. 문서 열두 건과 질문 여덟 개는 Ch 12 core 벌 사본 그대로입니다.</p><p>거리 순위 함수와 순위 표 출력 함수는 Ch 12 01절과 05절에서 배웠습니다. 문서 ID를 모으는 함수와 자리를 세는 함수는 Ch 11 01절에서 배웠습니다. 01·02절처럼 이 넷을 도구 파일 <code>notebooks/rag_tools.py</code>에서 가져옵니다. 벡터의 숫자 개수 설정 <code>256</code>과 답 모델도 이어 씁니다.</p><p>순위 합치기 함수와 순위 상수 <code>60</code>은 02절에서 쓴 그대로입니다. 모델이 보낸 글을 줄로 나누는 함수와 검색 한 번을 묶은 함수도 02절 것이고 같은 도구 파일에서 가져옵니다. 이 절은 그 부품을 그대로 두고 질문을 나누는 자리만 새로 만듭니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>나무판 한 장에 서로 다른 모양의 구멍 둘이 뚫려 있다고 생각해 봅니다. 둥근 마개 하나로는 네모 구멍을 메우지 못합니다. 구멍마다 모양이 맞는 마개를 따로 만들어야 합니다. 마개 둘을 각자 제 구멍에 끼우면 판이 채워집니다.</p>
{{img:03-5-서로-다른-구멍-둘에-맞는-마개-둘|흰 바탕에 나무판 한 장이 있고 그 판에 둥근 구멍 하나와 네모 구멍 하나가 뚫려 있으며 둥근 나무 마개와 네모 나무 마개가 각각 제 모양에 맞는 구멍에 반쯤 끼워져 있는 그림|서로 다른 모양의 구멍 둘에 모양이 맞는 마개가 하나씩 끼워집니다.}}
<p class="look"><b>그림 읽기</b> — 나무판 한 장에 구멍이 둘 있습니다. 왼쪽 구멍은 둥글고 오른쪽 구멍은 네모입니다. 둥근 마개는 둥근 구멍에, 네모 마개는 네모 구멍에 반쯤 끼워져 있습니다. 마개 하나가 두 구멍을 함께 메우지는 못한다는 것이 보입니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>하위 질문</td><td>한 질문에 섞인 사실을 하나씩만 묻도록 나눈 검색 질문입니다. 이 절에서는 둘입니다.</td></tr><tr><td>근거 문서 목록</td><td>하위 질문마다 첫 자리 문서를 하나씩 모으고 겹치는 문서를 뺀 목록입니다.</td></tr></tbody></table>
<p>아래 네 말은 Ch 11·Ch 12와 02절에서 쓰던 뜻 그대로 이어 씁니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>변형 질문</td><td>원 질문과 같은 것을 묻되 표현을 달리해 만든 검색 질문입니다(02절).</td></tr><tr><td>순위 합치기</td><td>순위 목록 여러 개를 하나로 만드는 일입니다(Ch 12 06절).</td></tr><tr><td>순위 상수</td><td>자리 번호에 더해 몫을 줄이는 값이고 이 절도 <code>60</code>입니다(Ch 12 06절).</td></tr><tr><td>가중치</td><td>목록 하나가 합친 점수에 보태는 몫의 크기입니다(Ch 12 06절).</td></tr></tbody></table>
{{mermaid:03-1-한-질문에-섞인-사실-둘-나누기|위에서 아래로 놓인 상자 여섯으로 맨 위에 초록 상자 사실이 둘 섞인 질문이 있고 그 아래 파란 상자 우리가 적은 나누기 머리글과 보라 상자 답 모델 gpt-5.4-mini를 지나 노란 상자 하위 질문 두 줄로 이어지며 그 아래 파란 상자 하위 질문마다 거리 검색을 거쳐 맨 아래 노란 상자 근거 문서 FAC-003과 ACC-003으로 이어지는 그림|사실이 둘 섞인 질문을 하위 질문 둘로 나눠 검색하면 근거 문서 둘을 얻습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자가 사람이 적은 질문입니다. 파란 상자 둘은 우리가 적은 글과 처리이고 보라 상자가 이번에 부른 모델입니다. 노란 상자 둘은 출력으로 확인한 값입니다.</p>
<h3>같은 것을 묻기와 다른 것을 묻기</h3><p>02절 변형 질문은 표현만 다르고 묻는 것은 같았습니다. 그래서 목록 넷에 같은 문서가 고르게 앞자리로 나타났고 순위 합치기가 그 문서를 위로 올렸습니다. 이 절 하위 질문은 묻는 것 자체가 다릅니다. 한 하위 질문의 근거는 다른 하위 질문의 목록에서 뒷자리에 있습니다.</p><p>그래서 모으는 방법도 달라집니다. 같은 것을 묻는 목록은 하나로 합칩니다. 다른 것을 묻는 목록은 각자의 첫 자리 문서를 따로 모읍니다.</p>
<h3>원 질문을 지우지 않습니다</h3><p>하위 질문은 검색에 넣는 글입니다. 사람이 적은 원 질문도 목록에 그대로 넣습니다. 나눈 결과가 빗나가도 원 질문 목록이 남습니다.</p>
<h3>나눌 개수를 값으로 적어 둡니다</h3><p>하위 질문 하나마다 임베딩 요청이 한 번씩 늘어납니다. 그래서 개수를 코드에 값으로 적고 머리글도 그 값으로 만듭니다. 값 하나를 바꾸면 머리글과 실제로 쓰는 개수가 함께 바뀝니다.</p>
<h3>모델이 만든 하위 질문은 출처가 아닙니다</h3><p>하위 질문은 모델이 쓴 글입니다. 자료에서 확인한 사실이 아니라 검색에 넣으려고 만든 글입니다. 답의 출처로는 찾은 문서의 ID와 원문만 씁니다.</p>
<h3>다른 상황에 적용</h3><p>사내 규정 문의에도 같은 자리가 있습니다. 「법인카드 발급 조건과 분실 신고 방법」은 사실이 둘 섞인 물음입니다. 발급 조건을 묻는 질문과 분실 신고를 묻는 질문으로 나누면 규정 문서를 하나씩 짝지을 수 있습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 문서 열두 건을 벡터로 바꾼 뒤 질문 둘을 각각 세 갈래로 검색합니다. 서비스 요청은 아홉 번이고 임베딩 일곱 번과 답 모델 두 번입니다. 예상 비용은 미화 0.01달러 아래입니다. 새로 쓰는 파일은 없습니다.</p><p>먼저 자료의 질문 둘을 이어 붙여 사실이 둘 섞인 질문을 만듭니다. 그 질문을 한 번만 검색해 두 근거 문서의 자리를 셉니다. 그다음 하위 질문 둘을 받아 각각 검색하고 근거 문서 목록을 만듭니다. 이어서 같은 목록 셋을 순위 합치기로 합쳐 자리를 다시 셉니다. 마지막으로 두 사실이 한 문서에 있는 질문으로 바꾸어 같은 일을 다시 합니다.</p>
{{mermaid:03-2-근거-문서-목록을-만드는-자리|위에서 아래로 놓인 상자 여섯으로 맨 위 초록 상자 하위 질문 두 줄 아래에 파란 상자 하위 질문마다 거리 검색이 있고 거기서 노란 상자 첫 자리 문서 FAC-003과 노란 상자 첫 자리 문서 ACC-003 둘로 갈라졌다가 파란 상자 겹치는 문서 빼기로 다시 모여 맨 아래 노란 상자 근거 문서 목록에 문서 둘로 이어지는 그림|하위 질문마다 첫 자리 문서를 하나씩 모으고 겹치는 문서를 빼면 근거 문서 목록이 됩니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자가 검색에 넣은 하위 질문 둘입니다. 파란 상자 둘은 우리가 적은 처리입니다. 노란 상자 셋은 노트북 9절이 출력한 값입니다.</p>
{{notebook:03-질의-분해}}
<p class="look"><b>확인할 점</b> — 한 번 검색한 출력 줄은 <code>한 번 검색했을 때 둘째 근거 문서의 자리: 6</code>이었습니다. 하위 질문으로 나눈 뒤에는 <code>근거 문서 목록: ['FAC-003', 'ACC-003']</code>이 나왔습니다. 세 목록을 합친 자리에서는 <code>합친 목록의 앞 세 자리</code>의 맨 앞이 <code>FAC-004</code>였습니다. 질문을 바꾼 자리에서는 <code>근거 문서 목록: ['ACC-002']</code>였습니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>이어 붙여 만든 질문을 한 번만 검색했습니다. 앞 세 자리는 <code>FAC-003</code>과 <code>ACC-002</code>와 <code>FAC-004</code>였습니다. 가운데 <code>ACC-002</code>는 두 사실 어느 쪽의 근거도 아닙니다. 앞쪽 사실의 근거는 첫 자리였고 뒤쪽 사실의 근거는 여섯째 자리였습니다.</p><p>하위 질문 둘로 나눠 각각 검색했습니다. 첫 하위 질문의 첫 자리는 <code>FAC-003</code>이고 둘째 하위 질문의 첫 자리는 <code>ACC-003</code>입니다. 두 문서를 모으니 근거 문서 목록에 서로 다른 문서 둘이 담겼습니다. 사실마다 근거 문서가 하나씩 짝지어졌습니다.</p>
{{mermaid:03-3-한-번-검색과-하위-질문-검색|왼쪽부터 오른쪽으로 놓인 칸 두 개와 회색 상자 하나로 왼쪽 칸 제목은 질문 하나로 한 번 검색이고 그 안에 초록 상자 검색에 쓴 질문 하나와 노란 상자 첫 자리 문서 FAC-003과 노란 상자 둘째 근거 ACC-003은 자리 여섯이 있으며 가운데 칸 제목은 하위 질문 둘로 나눠 검색이고 그 안에 초록 상자 검색에 쓴 하위 질문 둘과 노란 상자 첫 자리 문서 FAC-003과 ACC-003과 노란 상자 근거 문서 목록에 문서 둘이 있고 오른쪽에 회색 상자 두 검색 모두 같은 문서 열두 건에서 고름이 놓인 그림|질문 하나로 검색하면 둘째 근거가 자리 여섯이고 하위 질문 둘로 나누면 근거 문서 둘을 얻습니다.}}
<p class="look"><b>도식 읽기</b> — 왼쪽 칸이 질문 하나로 한 번 검색한 자리입니다. 가운데 칸이 하위 질문 둘로 나눠 검색한 자리입니다. 칸마다 맨 위 초록 상자가 넣은 질문이고 그 아래 노란 상자 둘이 나온 값입니다. 오른쪽 회색 상자는 두 칸에 모두 해당하는 사실입니다.</p>
<p>같은 목록 셋을 02절 방법으로 합쳐 보았습니다. 합친 목록의 첫 자리는 <code>FAC-004</code>였습니다. 이 문서는 두 사실 어느 쪽의 근거도 아닙니다. 두 근거는 그 뒤에 흩어져 있었습니다.</p><p>순위 합치기는 여러 목록에서 고르게 앞자리인 문서를 위로 올립니다. 하위 질문 둘은 다른 것을 물어 서로의 목록에서 뒷자리에 있었습니다. 그래서 고르게 앞자리인 문서가 두 사실과 상관없는 문서였습니다. 다른 것을 묻는 목록에는 하나로 합치기보다 첫 자리 문서를 따로 모으는 쪽이 맞습니다.</p><p>합친 뒤 두 근거의 자리는 하위 질문 문장이 조금 바뀌면 함께 바뀝니다. 이번 새 커널 두 번 실행에서는 같았지만 앞선 새 커널 실행에서는 서로 달랐습니다. 지금까지 새 커널 네 번 실행에서 근거 문서 목록은 <code>FAC-003</code>과 <code>ACC-003</code>으로 같았습니다. 그래서 합친 뒤 자리 두 개는 이 절 결론에 넣지 않았습니다.</p>
{{mermaid:03-4-목록-셋을-하나로-합치면|위에서 아래로 놓인 상자 여섯으로 맨 위 초록 상자 합칠 순위 목록 셋 아래에 파란 상자 우리가 적은 순위 합치기가 있고 그 아래 노란 상자 합친 목록 첫 자리 FAC-004와 노란 상자 그 문서는 두 사실의 근거가 아님이 놓이며 맨 아래에 회색 상자 두 하위 질문은 서로의 목록에서 뒷자리와 회색 상자 합친 뒤 두 근거의 자리는 두 실행에서 달라짐이 있는 그림|다른 것을 묻는 목록 셋을 하나로 합치면 첫 자리에 두 사실의 근거가 아닌 문서가 옵니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자가 합칠 순위 목록 셋입니다. 파란 상자는 Ch 12 06절 함수가 하는 일입니다. 위 노란 상자는 노트북 10절이 출력한 값이고 아래 노란 상자는 그 값과 근거 문서 ID를 견줘 내린 판단입니다. 아래 회색 상자 둘은 그 결과가 나온 까닭과 두 실행에서 달라진 값입니다.</p>
<p>질문을 바꾸면 결과가 또 달랐습니다. 두 사실이 한 문서에 함께 적힌 질문에서는 하위 질문 둘이 같은 문서를 찾았습니다. 근거 문서 목록에는 문서 하나만 남았습니다. 나누는 일이 늘 근거를 늘리지는 않습니다.</p><p>여기서 본 것은 질문 두 개입니다. 여덟 질문 모두에서 같은 차이가 나는지는 이번에 확인하지 않았습니다. 여러 질문으로 검색 품질을 재는 일은 Ch 11과 Ch 12 몫입니다. 답이 맞는지 판정하는 일은 Ch 15 몫입니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>자료의 여덟 질문에는 사실이 둘 섞인 질문이 없습니다. 그래서 질문 둘을 한 문장으로 이어 붙여 만들었고 근거 문서 둘도 자료가 적어 둔 값을 그대로 씁니다.</li><li>어느 둘을 이어 붙일지는 탐색 실행으로 정했습니다. 한 번 검색으로 뒤쪽 근거가 앞 세 자리 밖으로 밀리는 짝을 골랐습니다.</li><li>값 바꿔 보기에 쓴 질문도 흐름을 보여 주려고 고른 예입니다. 두 사실이 한 문서에 함께 적힌 자리를 찾아 만들었습니다.</li><li>하위 질문은 모델이 쓴 글이라 실행마다 문장이 달라질 수 있습니다. 그 문장에 <code>assert</code>를 걸지 않았습니다.</li><li>새 커널로 두 번 실행하니 스물세 셀 가운데 스물두 셀의 출력이 글자까지 같았습니다. 달라진 하나는 모델이 쓴 하위 질문 줄 끝의 빈칸입니다.</li><li>합친 뒤 두 근거의 자리는 이번 두 실행에서는 같았지만 앞선 새 커널 실행과는 달랐습니다. 하위 질문 문장에 따라 바뀌는 값이라 그 두 숫자를 본문과 그림과 정리에서 뺐습니다.</li><li>한 번 검색 자리 둘과 하위 질문 첫 자리 문서 둘과 근거 문서 목록은 두 실행에서 같았습니다. 결론은 그 값만 씁니다.</li><li>순위 표 둘째 줄과 셋째 줄의 거리가 소수 둘째 자리까지 같아 보입니다. 줄 세우기는 반올림 전 값으로 했고 그 두 줄의 차례는 결과로 읽지 않습니다.</li><li>거리 값은 셋째 자리 아래가 호출마다 조금씩 달라집니다. 본문과 그림에는 자리 번호와 문서 ID만 적었습니다.</li><li>합친 결과가 좋아지지 않았지만 방법을 바꾸지 않았습니다. 같은 방법을 02절과 이 절에 함께 써 보아야 차이가 보이기 때문입니다.</li><li>하위 질문을 둘 만들면 임베딩 요청이 두 번 늘어납니다. 이 절은 걸린 시간을 재지 않았으므로 빨라졌는지 느려졌는지 적지 않습니다.</li><li>나눈 하위 질문이 원 질문에 없는 조건을 넣으면 다른 문서를 찾습니다. 머리글에 조건을 새로 넣지 말라는 줄을 두었습니다.</li><li>하위 질문마다 찾은 문서 ID를 따로 두어야 어느 사실을 어느 원문이 받치는지 알 수 있습니다. 합친 목록 하나만 남기면 그 짝이 사라집니다.</li><li>이 절은 파일을 쓰지 않습니다. 문서 파일과 질문 파일은 읽기만 합니다.</li><li>준비물에 LangChain 1.4.0과 langchain-openai 1.6.1과 numpy 2.5.3을 적었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>사실이 둘 섞인 질문을 한 번만 검색하니 뒤쪽 사실의 근거가 여섯째 자리였습니다.</li><li>하위 질문 둘로 나눠 검색하니 근거 문서 목록에 서로 다른 문서 둘이 담겼습니다.</li><li>같은 목록 셋을 순위 합치기로 합치니 첫 자리에 두 사실의 근거가 아닌 문서가 왔습니다.</li><li>두 사실이 한 문서에 있는 질문에서는 나눠도 근거 문서가 하나였습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 04절에서는 질문을 잘게 나누는 대신 한 단계 넓혀 일반 규칙을 찾습니다. 이 절의 하위 질문은 원 질문보다 좁고 04절 질문은 원 질문보다 넓습니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 하위 질문의 입력과 출력은 무엇입니까?</p><p class="quiz-a">사실이 둘 섞인 질문 하나를 넣으면 사실 하나씩만 묻는 검색 질문 두 개가 나옵니다. 틀렸다면 「핵심 개념」의 용어 표를 다시 읽습니다.</p><p class="quiz-q">2. 변형 질문과 하위 질문은 무엇이 다릅니까?</p><p class="quiz-a">변형 질문은 표현만 달리해 같은 것을 묻고 하위 질문은 묻는 것 자체가 다릅니다. 틀렸다면 「핵심 개념」의 소제목 「같은 것을 묻기와 다른 것을 묻기」를 다시 읽습니다.</p><p class="quiz-q">3. 목록 셋을 순위 합치기로 합쳤을 때 첫 자리에는 무엇이 왔습니까?</p><p class="quiz-a">두 사실 어느 쪽의 근거도 아닌 문서 <code>FAC-004</code>가 왔습니다. 하위 질문 둘이 서로의 목록에서 뒷자리라 고르게 앞자리인 문서가 그 문서였기 때문입니다. 틀렸다면 「실험 결과 해석」의 둘째 도식을 다시 읽습니다.</p><p class="quiz-q">4. 나눠도 근거 문서가 늘지 않는 경우는 언제입니까?</p><p class="quiz-a">두 사실이 한 문서에 함께 적혀 있을 때입니다. 하위 질문 둘이 같은 문서를 찾아 근거 문서 목록에 하나만 남습니다. 틀렸다면 노트북 12절의 결과 읽기를 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://arxiv.org/abs/2507.00355">Question Decomposition for RAG 논문</a></div>확인 2026-09-19 · 복합 질문을 하위 질문으로 나눠 검색하는 방법의 출처.</li><li><div><a href="https://docs.langchain.com/oss/python/concepts/providers-and-models">LangChain 모델과 provider</a></div>확인 2026-09-19 · LangChain 1.4 기준 · 하위 질문을 만드는 모델을 준비하는 방법.</li><li><div><a href="https://developers.openai.com/api/docs/models/text-embedding-3-small">OpenAI text-embedding-3-small 모델 안내</a></div>확인 2026-09-19 · 문서와 질문을 벡터로 바꿀 때 쓴 모델과 차원 수 설정.</li><li>Ch 12 06절 하이브리드 검색 — 이 절이 이어 쓴 순위 합치기 함수 두 개와 순위 상수가 있는 자리.</li><li>Ch 14 02절 Multi Query — 같은 것을 묻는 변형 질문과 견주어 볼 자리.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(SRC_HTML, encoding="utf-8")
    return SRC


if __name__ == "__main__":
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "03", "03-질의-분해", "experiment", cells())
        print("wrote", path)
