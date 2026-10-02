"""Ch 14 02절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§3·§6).

사용:
  python3 author_02.py            → 노트북 + _src 본문을 함께 다시 쓴다
  python3 author_02.py --src-only → 본문 HTML만 다시 쓴다(노트북 출력을 지우지 않는다)

이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북과 본문은 qa/upgrade/before/ 에 있다. **experiment 형식 유지**(chapter.json).

## 가져온 함수 여섯 개 (§2-7 리팩터 2026-09-21 — 도구 파일 `notebooks/rag_tools.py`)

준비 셀(import 셀)에서 Ch 12·Ch 11 함수 다섯(`rank_by_distance`·`print_ranked`·`unique_doc_ids`·`find_gold_rank`·
`fuse_rank`)과 01절 `run_row`를 가져온다. `rank_by_distance(question_vector, doc_vectors, doc_ids, top_count)`는
NumPy 판이고, `fuse_rank(ranking_list, weight_list, rank_constant)`는 Ch 12 도구 파일 판(순위 상수를 셋째 인자로,
안에서 `fuse_scores`를 부름)이다. 순위 상수 `60`·기본 가중치 `1.0`은 Ch 12 06절과 같다.
리팩터 전에는 거리 함수 넷·순위 함수·자리 함수 둘·출력 함수(준비 셀 넷)와 `fuse_scores`·`fuse_rank`(준비 셀 둘),
`run_row`(01절과 AST 같음) 정의 셀을 노트북에 다시 적었다. 01절은 목록이 하나뿐이라 순위 합치기를 쓰지 않았다.

## 이 절이 새로 만든 함수 셋

`build_variant_prompt(question)` · `split_lines(reply_text)` · `search_ids(question)`.
기록 한 줄 함수 `run_row(run_name, question_text, found_ids, place)`는 01절 판을 도구 파일에서 가져온다.

## 선택한 것과 까닭

1. **여러 목록을 하나로 만드는 일은 Ch 12 06절 「순위 합치기」로 한다.** 개선 전 02절은 문서별 최고
   유사도를 남겨 `sorted(key=…, reverse=True)`로 줄 세웠다. `key=`·`reverse=`·`lambda`는 이 과정이
   가르치지 않았고(과정 요약 §2-3), 같은 일을 Ch 12 06절이 이미 함수 두 개로 가르쳤다. 그래서 그
   함수를 도구 파일에서 가져온다. 순위 상수는 `60`, 가중치는 목록마다 `1.0`이다.
2. **검색에 쓸 질문을 `C01`로 골랐다.** 01절이 만든 독립 질문 「스터디룸에 늦게 가면 어떻게 되나요?」는
   한 번 검색으로도 정답 문서가 첫 자리라 늘린 효과가 보이지 않는다(탐색 실행 probe1). 질문 `C01`은
   01절이 Ch 12 05절과 대조할 때 쓴 질문이고 그때 정답 문서가 둘째 자리였다. 같은 질문을 이어 쓰면
   01절 출력과 바로 견줄 수 있다(probe4·probe5).
3. **값 바꿔 보기는 질문 `C02`다.** 늘려도 정답 문서가 앞으로 오지 않는 질문을 함께 보여 준다.
   여덟 질문을 모두 재어 보니 `C01`만 자리가 둘에서 하나로 오고 `C02`는 일곱에서 넷에 머물렀다(probe4).
4. **걸린 시간과 비용 추정을 넣지 않는다.** 개선 전은 `time.perf_counter()`로 ms를 재고
   `usage_metadata`로 달러를 추정했다. Ch 12부터 이 과정은 걸린 시간을 한 번도 재지 않았다.
5. **모델 이름을 `gpt-5.4-mini`로 바꿨다**(규격 §6 기준 버전). 개선 전은 `gpt-4.1-mini`였고
   b10에 그 모델 단가 줄이 있었다.
6. **벡터 계산은 도구 파일 안에서 NumPy로 한다**(규격 §2-7). 노트북은 `numpy`를 직접 부르지 않는다.
7. **모델이 보낸 글을 줄로 나눌 때 글자 집합을 깎지 않는다.** 개선 전은
   `[x.lstrip("-123. ") for x in text.splitlines() if x.strip()][:3]`이었다. `lstrip`은 글자 집합을
   깎아 「3권까지」 같은 머리 글자도 함께 없앤다. 이름 있는 함수 `split_lines`로 빈 줄만 빼고,
   실제로 몇 줄이 왔는지 출력으로 보인다.
8. **모델 답에 `assert`를 걸지 않는다**(규격 §3). `assert`는 키 확인과 자리 확인 두 곳뿐이다.
9. **쓰지 않은 것**: `lambda`·내포식·제너레이터 식·조건 표현식·f-string·`key=`·`reverse=`·`set`·
   기본값 매개변수·복합 타입힌트·세미콜론·한 줄 다중 대입·클래스 정의·`enumerate`·`zip`·`next`·`time`.
   부른 내장 이름은 `len`·`open`·`print`·`range`·`round`·`sorted`·`str`뿐이다.

## 탐색 실행에서 확인한 값 (2026-09-19, /tmp/ch14-02/probe1.py~probe5.py)

langchain 1.4.0 · langchain-openai 1.6.1 · Python 3.12.13 · 문서 12건 · 질문 8건.
질문 `C01` 거리 상위 셋은 `LIB-004` 0.43 · `LIB-001` 0.56 · `LIB-003` 0.62로 01절·Ch 12 05절과 같다.
`C01` 한 번 검색 정답 자리 둘 → 변형 셋 모두 자리 하나 → 합친 목록 자리 하나(두 번 모두 같음).
`C02` 한 번 검색 정답 자리 일곱 → 합친 목록 자리 넷(두 번 모두 같음). 변형 하나만 자리 하나였다.
변형 질문 문장과 변형별 정답 자리(`C02`의 둘째·셋째)는 실행마다 달라진다.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part4/ch14-rag-patterns/notebooks"
SRC = ROOT / "textbook/part4/ch14-rag-patterns/_src/02-Multi-Query.html"

INSTALL = install_source([
    "langchain==1.4.0", "langchain-openai==1.6.1", "python-dotenv==1.2.3", "numpy==2.5.3",
])

IMPORTS = r'''# 자료 읽기·경로 확인과 임베딩·답 모델 이름을 불러옵니다
import json
import os

from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model
# Ch 12 01·05·06절과 Ch 11 01절 함수, 01절 기록 함수를 도구 파일에서 가져옵니다
from rag_tools import find_gold_rank, fuse_rank, print_ranked, rank_by_distance, run_row
from rag_tools import unique_doc_ids

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

VALUES = r'''# Ch 12에서 쓴 값을 그대로 다시 정하고 늘릴 질문 개수도 못 박습니다
top_three = 3
top_all = 12
variant_count = 3
print("나란히 볼 상위 문서 수:", top_three)
print("자리를 셀 때 재는 문서 수:", top_all)
print("만들 변형 질문 수:", variant_count)'''

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


EMBEDDINGS = r'''# Ch 12와 같은 모델로 문서 12개를 벡터로 바꿉니다(임베딩 요청 1번)
embedding_model_name = "text-embedding-3-small"
vector_dimensions = 256
embedding_model = OpenAIEmbeddings(model=embedding_model_name, dimensions=vector_dimensions)
doc_vectors = embedding_model.embed_documents(doc_texts)
print("임베딩 모델 이름:", embedding_model.model)
print("벡터의 숫자 개수 설정:", embedding_model.dimensions)
print("문서 벡터 수:", len(doc_vectors))'''

FUSE_VALUES = r'''# 자리 번호를 몫으로 바꾸는 식에 쓸 값을 정하고 앞자리 세 곳의 몫을 봅니다
rank_constant = 60
base_weight = 1.0
print("순위 상수:", rank_constant)
print("목록 하나에 줄 가중치:", base_weight)
print("자리 | 기본 가중치가 주는 몫")
for position in range(top_three):
    share = base_weight / (rank_constant + position + 1)
    print(position + 1, "|", round(share, 4))'''


PICK_QUESTION = r'''# 01절이 Ch 12와 대조할 때 쓴 첫 질문을 그대로 골라 정답 문서 ID도 적어 둡니다
base_query = queries[0]
base_question = base_query["question"]
gold_doc_id = base_query["gold_doc_id"]
print("고른 질문:", base_query["qid"], "|", base_question)
print("그 질문의 정답 문서 ID:", gold_doc_id)'''

BASE_SEARCH = r'''# 고른 질문을 한 번만 검색해 앞 세 자리와 정답 문서의 자리를 봅니다(임베딩 요청 1번)
base_vector = embedding_model.embed_query(base_question)
base_hits = rank_by_distance(base_vector, doc_vectors, doc_ids, top_all)
base_ids = unique_doc_ids(base_hits)
base_place = find_gold_rank(base_ids, [gold_doc_id])
print_ranked(base_hits[:top_three], "거리")
print("한 번만 검색했을 때 정답 문서의 자리:", base_place)'''

BUILD_VARIANT = r'''# 머리글 세 줄과 원 질문을 한 글로 이어 붙입니다
def build_variant_prompt(question):
    variant_head = "아래 질문과 같은 것을 묻되 표현과 관점을 달리한 검색 질문을 "
    variant_head = variant_head + str(variant_count) + "줄 적으세요.\n"
    variant_head = variant_head + "한 줄에 질문 하나만 적고 번호나 기호를 붙이지 마세요.\n"
    variant_head = variant_head + "질문이 가리키는 대상과 조건은 그대로 두세요.\n\n"
    prompt_text = variant_head + "질문: " + question
    return prompt_text'''

VARIANT_CALL = r'''# 만든 글을 모델에 넣어 변형 질문을 받습니다(모델 요청 1번)
variant_prompt = build_variant_prompt(base_question)
print("모델에 넣을 글:")
print(variant_prompt)
variant_reply = model.invoke(variant_prompt)
variant_text = variant_reply.text.strip()
print("모델이 쓴 글:")
print(variant_text)'''

SPLIT_LINES = r'''# 글을 줄로 나누고 빈 줄을 뺀 목록을 만듭니다
def split_lines(reply_text):
    lines = []
    for line in reply_text.split("\n"):
        clean_line = line.strip()
        if clean_line != "":
            lines.append(clean_line)
    return lines'''

SPLIT_CALL = r'''# 모델이 보낸 글을 줄로 나누고 앞에서 정한 개수만 골라 씁니다
variant_lines = split_lines(variant_text)
variants = variant_lines[:variant_count]
print("모델이 보낸 줄 수:", len(variant_lines))
print("쓸 변형 질문 수:", len(variants))
for variant in variants:
    print("변형 질문:", variant)'''

SEARCH_IDS = r'''# 질문 하나를 벡터로 바꿔 문서 ID 순위 목록을 만듭니다(부를 때마다 임베딩 요청 1번)
def search_ids(question):
    question_vector = embedding_model.embed_query(question)
    hit_list = rank_by_distance(question_vector, doc_vectors, doc_ids, top_all)
    found_ids = unique_doc_ids(hit_list)
    return found_ids'''

VARIANT_SEARCH = r'''# 원 질문 목록 뒤에 변형 질문 목록 셋을 이어 붙입니다(임베딩 요청 3번)
ranking_list = []
ranking_list.append(base_ids)
for variant in variants:
    ranking_list.append(search_ids(variant))
print("합칠 목록 수:", len(ranking_list))
print("첫 자리 문서 | 정답 문서의 자리")
for found_ids in ranking_list:
    print(found_ids[0], "|", find_gold_rank(found_ids, [gold_doc_id]))'''

FUSE_CALL = r'''# 목록마다 같은 가중치를 주고 자리 몫을 더해 하나로 합칩니다
weight_list = []
for found_ids in ranking_list:
    weight_list.append(base_weight)
fused_ids = fuse_rank(ranking_list, weight_list, rank_constant)
fused_place = find_gold_rank(fused_ids, [gold_doc_id])
print("쓴 가중치:", weight_list)
print("합친 목록의 앞 세 자리:", fused_ids[:top_three])
print("합친 뒤 정답 문서의 자리:", fused_place)'''

SECOND_PICK = r'''# 바꿀 값은 검색에 쓸 질문 하나입니다(임베딩 요청 1번)
second_query = queries[1]
second_question = second_query["question"]
second_gold = second_query["gold_doc_id"]
second_ids = search_ids(second_question)
second_place = find_gold_rank(second_ids, [second_gold])
print("바꾼 질문:", second_query["qid"], "|", second_question)
print("그 질문의 정답 문서 ID:", second_gold)
print("한 번만 검색했을 때 정답 문서의 자리:", second_place)'''

SECOND_VARIANT = r'''# 바꾼 질문으로 같은 머리글을 써서 변형 질문을 받습니다(모델 요청 1번)
second_prompt = build_variant_prompt(second_question)
second_reply = model.invoke(second_prompt)
second_text = second_reply.text.strip()
second_lines = split_lines(second_text)
second_variants = second_lines[:variant_count]
print("모델이 보낸 줄 수:", len(second_lines))
for variant in second_variants:
    print("변형 질문:", variant)'''

SECOND_FUSE = r'''# 바꾼 질문도 목록 넷을 모아 앞에서 쓴 가중치 그대로 합칩니다(임베딩 요청 3번)
second_ranking_list = []
second_ranking_list.append(second_ids)
for variant in second_variants:
    second_ranking_list.append(search_ids(variant))
second_fused = fuse_rank(second_ranking_list, weight_list, rank_constant)
second_fused_place = find_gold_rank(second_fused, [second_gold])
print("첫 자리 문서 | 정답 문서의 자리")
for found_ids in second_ranking_list:
    print(found_ids[0], "|", find_gold_rank(found_ids, [second_gold]))
print("합친 뒤 정답 문서의 자리:", second_fused_place)'''


TABLE = r'''# 네 실행의 기록을 담아 라벨 줄 아래에 한 줄씩 출력합니다
run_rows = []
run_rows.append(run_row("C01 한 번 검색", base_question, base_ids, base_place))
run_rows.append(run_row("C01 합친 목록", base_question, fused_ids, fused_place))
run_rows.append(run_row("C02 한 번 검색", second_question, second_ids, second_place))
run_rows.append(run_row("C02 합친 목록", second_question, second_fused, second_fused_place))
print("실행 | 검색에 쓴 질문 | 첫 자리 문서 | 정답 자리")
for row in run_rows:
    print(row["실행"], "|", row["검색에 쓴 질문"], "|", row["첫 자리 문서"], "|", row["정답 자리"])'''

TITLE = """# Multi Query

**이 노트북에서 할 일**

1. Ch 12에서 쓰던 문서 열두 건과 질문 여덟 개를 그대로 읽습니다.
2. 질문 하나를 한 번만 검색해 정답 문서의 자리를 셉니다.
3. 같은 질문을 변형 질문 세 개로 늘려 각각 검색합니다.
4. 네 목록을 Ch 12 순위 합치기로 하나로 만들어 자리를 다시 셉니다.
5. 질문만 바꾸어 같은 일을 다시 하고 두 결과를 견줍니다.

**준비물** — 이 절은 프로젝트 맨 위 폴더의 `.env`에 적어 둔 `OPENAI_API_KEY`를 씁니다.
서비스 요청은 열한 번입니다(임베딩 아홉 번과 답 모델 두 번).
예상 비용은 미화 0.01달러 아래입니다.
읽어 오는 파일은 이 챕터 폴더의 문서 파일과 질문 파일 둘이고 새로 쓰는 파일은 없습니다.
실행 시간은 2분 안팎이고 첫 셀의 설치가 가장 오래 걸립니다.

**기준 버전** — 첫 셀에서 LangChain 1.4.0과 langchain-openai 1.6.1을 설치합니다.
키를 읽는 python-dotenv 1.2.3과 도구 파일이 쓰는 numpy 2.5.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3절부터 7절까지 읽습니다.
Ch 12 검색 부품과 순위 합치기 부품을 준비하고 질문 하나를 한 번 검색하는 자리입니다.
8절과 9절은 변형 질문을 만들고 목록 넷을 모으는 자리입니다.
10절부터 12절은 목록을 합치고 질문을 바꾸어 다시 재는 자리입니다.

실습 폴더 `labs/part4/ch14-rag-patterns`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""

FIGURE_ALT = ("위에서 아래로 놓인 상자 일곱으로 맨 위에 초록 상자 원 질문 C01 책을 빌릴 수 있는 기간은 "
              "며칠인가요가 있고 그 아래 파란 상자 우리가 적은 변형 프롬프트와 보라 상자 답 모델 "
              "gpt-5.4-mini를 지나 노란 상자 변형 질문 세 줄로 이어지며 원 질문과 변형 질문이 모두 파란 "
              "상자 우리가 적은 거리 검색 네 번으로 모여 파란 상자 우리가 적은 순위 합치기를 거쳐 맨 "
              "아래 노란 상자 정답 문서 LIB-001이 자리 하나로 이어지는 그림")

FIGURE_READ = """위에서 아래로 읽습니다.
맨 위 초록 상자가 사람이 적은 원 질문입니다.
가운데 파란 상자 셋이 우리가 적은 글과 처리이고 보라 상자가 모델입니다.
맨 아래 노란 상자 둘이 출력으로 확인한 값입니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIGURE_ALT + "](attachment:02-1-질문-하나를-여러-갈래로-늘리기.png)\n\n" + FIGURE_READ, html="skip"),
        md("""## 1. 준비

첫 셀은 패키지 네 개를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 판 번호 네 줄이 보입니다.
마지막 줄 `numpy: 2.5.3`은 도구 파일이 벡터 계산에 쓰는 패키지입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이름 네 개를 불러오고 도구 파일에서 함수 여섯 개를 가져옵니다.
앞의 둘은 자료 읽기와 폴더 확인에 씁니다.
뒤의 둘은 Ch 9~13에서 쓴 임베딩과 답 모델 이름입니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.

이 노트북은 Ch 12 01절 `rank_by_distance()`와 05절 `print_ranked()`를 가져옵니다.
Ch 11 01절 `unique_doc_ids()`·`find_gold_rank()`와 Ch 12 06절 `fuse_rank()`도 가져옵니다.
기록 한 줄을 만드는 01절 `run_row()`도 함께 가져옵니다.
인자 모양은 쓰는 자리에서 설명합니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄에 불러온 이름 네 개가 보입니다.
이름 `OpenAIEmbeddings`와 `init_chat_model`은 01절에서 쓴 것과 같습니다.
도구 파일에서 가져온 함수 여섯 개는 출력하지 않습니다.

## 2. 키와 모델 준비"""),
    ] + key_and_model_cells("openai:gpt-5.4-mini") + [
        md("""## 3. 문서와 질문 읽기

이 절은 01절과 같은 문서 파일과 질문 파일을 읽습니다.
두 파일은 Ch 12 core 벌 파일과 바이트가 같은 사본입니다.
먼저 노트북을 연 자리에서 프로젝트 맨 위를 찾습니다."""),
        code(ROOT_PATH),
        md("""**결과 읽기** — 출력 줄 `고른 자리` 뒤에 점 하나나 위로 올라가는 표시가 보입니다.
Ch 10~13과 01절에서 쓴 방법과 같습니다.
후보 셋 가운데 이 챕터 자료 폴더가 있는 자리를 고릅니다.

다음 셀은 문서 파일과 질문 파일을 읽습니다."""),
        code(LOAD_DATA),
        md("""**결과 읽기** — 출력 줄 `문서 수: 12`와 `질문 수: 8`이 Ch 12 core 벌 그대로입니다.
문서는 도서관 안내 열두 건입니다.

질문 번호는 C01부터 C08까지이고 질문 파일에 적혀 있습니다.
이 절은 그 가운데 둘을 씁니다.

## 4. 이 절에서 쓸 값 정하기

Ch 12와 01절에서 정한 값을 그대로 다시 적습니다.
늘릴 변형 질문 개수도 여기서 못 박아 둡니다."""),
        code(VALUES),
        md("""**결과 읽기** — 출력 줄 `나란히 볼 상위 문서 수: 3`은 표로 볼 자리 수입니다.
출력 줄 `자리를 셀 때 재는 문서 수: 12`는 정답 자리를 끝까지 세려고 둔 값입니다.
출력 줄 `만들 변형 질문 수: 3`은 이 절이 늘릴 질문 개수입니다.

개수를 값으로 적어 두면 늘어난 요청 수를 셀 수 있습니다.
변형 질문 하나마다 임베딩 요청이 한 번씩 늘어납니다.

## 5. Ch 12 검색 부품 준비

다음 셀은 01절과 같은 방법으로 문서 열두 건의 제목과 본문을 이어 붙입니다.
읽지 말고 실행만 하고 넘어가도 됩니다.
거리 순위와 자리 세기와 출력 함수는 준비 셀에서 도구 파일로 가져왔습니다."""),
        code(DOC_TEXTS, lesson_role="setup"),
        md("""준비 셀 하나를 지났습니다.
다음 셀은 문서 열두 건을 벡터로 바꿉니다.
이 절에서 서비스에 보내는 첫 요청입니다."""),
        code(EMBEDDINGS),
        md("""**결과 읽기** — 출력 줄 `임베딩 모델 이름: text-embedding-3-small`은 01절과 같은 모델입니다.
출력 줄 `벡터의 숫자 개수 설정: 256`도 Ch 10~13과 같은 값입니다.
출력 줄 `문서 벡터 수: 12`로 문서마다 벡터 하나를 받았습니다.
벡터 안의 숫자는 호출마다 아주 조금씩 달라져 소수 자리까지 같다고 보지 않습니다.

## 6. 순위 합치기 부품 준비

이 절은 순위 목록 네 개를 하나로 만들어야 합니다.
그 일은 Ch 12 06절에서 「순위 합치기」로 배웠습니다.
먼저 자리 번호를 몫으로 바꾸는 식에 쓸 값 두 개를 정합니다."""),
        code(FUSE_VALUES),
        md("""**결과 읽기** — 출력 줄 `순위 상수: 60`은 Ch 12 06절에서 정한 값 그대로입니다.
출력 줄 `목록 하나에 줄 가중치: 1.0`으로 네 목록을 같은 크기로 봅니다.
라벨 줄 `자리 | 기본 가중치가 주는 몫` 아래 세 줄에 앞자리 몫이 있습니다.
첫 자리가 받는 몫은 `0.0164`이고 셋째 자리는 `0.0159`입니다.

앞자리일수록 나누는 수가 작아 몫이 큽니다.
여러 목록에서 고르게 앞자리에 있는 문서가 몫을 많이 모읍니다.

순위 합치기 함수 `fuse_rank()`는 준비 셀에서 도구 파일로 가져왔습니다.
안에서 Ch 12 06절 `fuse_scores()`로 목록마다 자리 몫을 더해 문서별 합친 점수를 냅니다.
그 점수가 큰 순서로 문서 ID 목록을 만듭니다.
도구 파일 판은 순위 상수를 셋째 인자로 받습니다.

## 7. 질문 하나로 한 번 검색하기

먼저 질문 하나를 그대로 검색해 기준이 될 자리를 잽니다.
01절이 Ch 12 05절과 대조할 때 쓴 첫 질문을 그대로 고릅니다."""),
        code(PICK_QUESTION),
        md("""**결과 읽기** — 출력 줄 `고른 질문: C01` 뒤에 질문 한 줄이 있습니다.
출력 줄 `그 질문의 정답 문서 ID: LIB-001`은 자료 파일에 적힌 정답입니다.

실행 전에 예상해 봅니다.
질문에 「빌릴 수 있는 기간」이 있으니 대출을 다룬 문서가 앞으로 올 것입니다."""),
        code(BASE_SEARCH),
        md("""**결과 읽기** — 순위 표의 차례는 `LIB-004`와 `LIB-001`과 `LIB-003`입니다.
01절이 Ch 12 05절과 대조한 표와 같습니다.
출력 줄 `한 번만 검색했을 때 정답 문서의 자리: 2`로 정답 문서는 둘째 자리였습니다.
전자책 문서가 첫 자리에 오고 일반 도서 대출 문서가 그 뒤에 왔습니다.

거리 값은 소수 둘째 자리까지만 읽습니다.
셋째 자리 아래는 호출마다 조금씩 달라져 본문과 그림에 넣지 않았습니다.

## 8. 변형 질문 만들기

같은 것을 묻는 질문을 표현만 달리해 세 줄 더 만듭니다.
머리글에 개수와 모양을 적어 한 줄에 질문 하나만 오게 합니다.
대상과 조건을 그대로 두라는 줄도 함께 넣습니다."""),
        code(BUILD_VARIANT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `build_variant_prompt`는 머리글 세 줄을 이어 붙인 뒤 원 질문을 답니다.
머리글의 개수 자리에는 앞에서 정한 값 `variant_count`가 들어갑니다.
값을 바꾸면 머리글과 실제로 쓰는 개수가 함께 바뀝니다.

다음 셀은 그 글을 만들어 모델에 넣습니다."""),
        code(VARIANT_CALL),
        md("""**결과 읽기** — 라벨 줄 `모델에 넣을 글:` 아래에 머리글 세 줄과 원 질문이 있습니다.
라벨 줄 `모델이 쓴 글:` 아래에는 질문 세 줄이 있습니다.
세 줄 모두 빌리는 기간을 묻고 표현만 다릅니다.
문장은 실행마다 달라질 수 있어 이 값에 `assert`를 걸지 않았습니다.

## 9. 변형 질문마다 검색하기

모델이 보낸 글은 줄 하나가 질문 하나입니다.
줄로 나눌 때 글자를 깎지 않고 빈 줄만 뺍니다.
먼저 그 일을 하는 함수를 만듭니다."""),
        code(SPLIT_LINES),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `split_lines`는 글을 줄 단위로 나눈 뒤 빈 줄을 뺀 목록을 만듭니다.
줄 앞뒤 공백만 없애고 글자는 그대로 둡니다.

다음 셀은 그 목록에서 앞의 세 줄만 고릅니다."""),
        code(SPLIT_CALL),
        md("""**결과 읽기** — 출력 줄 `모델이 보낸 줄 수: 3`으로 세 줄이 왔습니다.
출력 줄 `쓸 변형 질문 수: 3`은 앞에서 정한 개수와 같습니다.
라벨 줄 `변형 질문:` 세 줄에 실제로 쓸 질문이 있습니다.
받은 줄이 더 많아도 앞의 세 줄만 씁니다.

적게 오면 온 만큼만 씁니다.
그때는 `쓸 변형 질문 수`가 `만들 변형 질문 수`보다 작게 나옵니다.

다음 셀은 검색 한 번을 함수 하나로 묶습니다."""),
        code(SEARCH_IDS),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `search_ids`는 질문 하나를 벡터로 바꾸고 문서 ID 순위 목록을 만듭니다.
부를 때마다 임베딩 요청이 한 번씩 갑니다.
자리를 끝까지 세려고 문서 열두 건을 모두 담습니다.

다음 셀은 원 질문 목록 뒤에 변형 질문 목록 셋을 붙입니다."""),
        code(VARIANT_SEARCH),
        md("""**결과 읽기** — 출력 줄 `합칠 목록 수: 4`로 목록이 넷입니다.
라벨 줄 `첫 자리 문서 | 정답 문서의 자리` 아래 네 줄이 있습니다.
첫 줄은 원 질문이고 첫 자리 문서가 `LIB-004`이며 정답 자리가 `2`입니다.
아래 세 줄은 변형 질문이고 그 가운데 하나만 첫 자리 문서가 `LIB-001`입니다.

변형 질문 문장은 실행마다 달라질 수 있습니다.
문장이 달라지면 이 표의 자리도 함께 달라집니다.
그래서 목록별 자리는 본문 결론에 넣지 않았습니다.

## 10. 네 목록을 하나로 합치기

이제 목록 넷을 순위 합치기로 하나로 만듭니다.
목록마다 같은 가중치를 주어 어느 한 갈래에 치우치지 않게 합니다."""),
        code(FUSE_CALL),
        md("""**결과 읽기** — 출력 줄 `쓴 가중치: [1.0, 1.0, 1.0, 1.0]`으로 네 목록을 같게 봤습니다.
출력 줄 `합친 목록의 앞 세 자리`의 맨 앞은 `LIB-001`입니다.
출력 줄 `합친 뒤 정답 문서의 자리: 1`로 정답 문서가 첫 자리로 왔습니다.
한 번만 검색했을 때의 둘째 자리에서 한 자리 올라왔습니다.

합친 목록의 앞 세 자리는 새 커널로 두 번 실행했을 때 같았습니다.
변형 질문 문장이 달라지면 뒷자리는 달라질 수 있습니다.

## 11. 값 바꿔 보기 · 질문을 바꾸기

바꿀 값은 검색에 쓸 질문 하나입니다.
머리글도 변형 개수도 가중치도 그대로 두고 질문만 `C02`로 바꿉니다.
실행 전에 예상해 봅니다.
질문에 「돈」이 있고 문서에는 그 말이 없어 정답 문서가 뒤로 밀릴 것입니다."""),
        code(SECOND_PICK),
        md("""**결과 읽기** — 출력 줄 `바꾼 질문: C02` 뒤에 질문 한 줄이 있습니다.
출력 줄 `그 질문의 정답 문서 ID: LIB-002`는 연체를 다룬 문서입니다.
출력 줄 `한 번만 검색했을 때 정답 문서의 자리: 7`로 일곱째 자리였습니다.
질문의 말과 문서의 말이 멀어 앞자리에 오지 못했습니다.

다음 셀은 같은 머리글로 변형 질문을 다시 받습니다."""),
        code(SECOND_VARIANT),
        md("""**결과 읽기** — 출력 줄 `모델이 보낸 줄 수: 3`으로 이번에도 세 줄이 왔습니다.
라벨 줄 `변형 질문:` 세 줄에 연체료와 벌금과 추가 비용을 묻는 질문이 있습니다.
문장은 실행마다 달라집니다.

다음 셀은 목록 넷을 모아 앞에서 쓴 가중치 그대로 합칩니다."""),
        code(SECOND_FUSE),
        md("""**결과 읽기** — 라벨 줄 `첫 자리 문서 | 정답 문서의 자리` 아래 네 줄이 있습니다.
네 줄 가운데 한 줄만 정답 문서를 첫 자리에 두었습니다.
출력 줄 `합친 뒤 정답 문서의 자리: 4`로 넷째 자리에 그쳤습니다.
자리는 일곱에서 넷으로 올라왔지만 앞 세 자리 안에는 들지 못했습니다.

순위 합치기는 여러 목록에서 고르게 앞자리인 문서를 위로 올립니다.
한 목록에서만 앞자리인 문서는 몫을 한 번밖에 모으지 못합니다.
목록별 첫 자리 문서는 실행마다 달라져 결론에 넣지 않았습니다.

## 12. 네 실행을 기록 한 줄씩으로

실행 하나를 기록 한 줄로 만들어 담아 둡니다.
기록 한 줄은 준비 셀에서 도구 파일로 가져온 01절 `run_row()`로 만듭니다.
담는 칸은 실행 이름과 검색에 쓴 질문과 첫 자리 문서와 정답 자리 넷입니다.
이 절이 견주는 값도 그 넷입니다.

다음 셀은 네 실행의 기록을 표로 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 `실행 | 검색에 쓴 질문 | 첫 자리 문서 | 정답 자리` 아래 네 줄이 나옵니다.
질문 `C01`은 합친 뒤 정답 자리가 `1`로 올라왔습니다.
질문 `C02`는 합친 뒤에도 정답 자리가 `4`였습니다.
같은 방법을 써도 질문에 따라 결과가 달랐습니다.

## 정리

1. 질문 하나만으로 검색하니 질문 `C01`의 정답 문서는 둘째 자리였습니다.
2. 변형 질문 셋을 더해 네 목록을 합치니 정답 문서가 첫 자리로 왔습니다.
3. 질문 `C02`에서는 같은 방법을 써도 정답 문서가 앞 세 자리 안에 들지 못했습니다.

03절에서는 한 질문 안에 섞인 여러 사실을 하위 질문으로 나눕니다.
이 절이 만든 변형 질문은 같은 것을 묻는 질문이고 03절은 다른 것을 묻는 질문을 만듭니다."""),
    ]


SRC_HTML = """<!--meta: 강의 1h | 실습 2h | 코드 notebooks/02-Multi-Query.ipynb | 새 용어 2 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>질문 하나를 뜻이 같은 변형 질문 여러 개로 늘릴 수 있습니다.</li>
<li>변형 질문마다 얻은 순위 목록을 Ch 12 순위 합치기로 하나로 만들 수 있습니다.</li>
<li>늘려도 정답 문서가 앞으로 오지 않는 질문이 있다는 것을 자리로 확인할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>같은 일을 사람마다 다른 말로 묻습니다. 어떤 사람은 「대출 기간」이라 적고 어떤 사람은 「며칠 빌리나요」라고 적습니다. 문서에 적힌 말과 질문에 쓴 말이 멀면 그 문서는 뒤로 밀립니다. 질문을 여러 갈래로 늘려 각각 검색하면 그 가운데 하나가 문서의 말과 가까울 수 있습니다.</p><p>Ch 9의 기본 RAG는 검색 한 번과 답 한 번이었습니다. 이 챕터는 그 앞뒤에 단계를 하나씩 붙입니다. 01절은 검색 앞에서 질문을 바꾸는 단계를 붙였습니다. 이 절은 같은 자리에서 질문 하나를 여러 개로 늘립니다. 늘릴 개수는 우리가 코드에 적은 값으로 정합니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>01절은 대화 기록을 넣어 혼자서도 뜻이 통하는 질문을 만들었습니다. 이 절은 그렇게 뜻이 통하는 질문 하나를 입력으로 받습니다. 쓰는 질문은 01절이 Ch 12와 대조할 때 쓴 질문 <code>C01</code>입니다. 문서 열두 건과 질문 여덟 개는 Ch 12 core 벌 사본 그대로입니다.</p><p>거리 순위 함수와 순위 표 출력 함수는 Ch 12 01절과 05절에서 배웠습니다. 문서 ID를 모으는 함수와 정답 자리를 세는 함수는 Ch 11 01절에서 배웠습니다. 01절처럼 이 넷을 도구 파일 <code>notebooks/rag_tools.py</code>에서 가져옵니다. 기록 한 줄을 만드는 01절 함수도 같은 파일에서 가져옵니다. 값도 같아서 벡터의 숫자 개수 설정 <code>256</code>과 답 모델을 이어 씁니다.</p><p>순위 목록 여러 개를 하나로 만드는 일은 Ch 12 06절에서 배웠습니다. 그 절의 순위 합치기 함수도 도구 파일에서 가져오고 순위 상수 <code>60</code>을 그대로 씁니다. 01절은 목록 하나만 다뤄 이 함수를 쓰지 않았습니다. 이 절에서 목록이 넷으로 늘어 처음 씁니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>나무판 한 장으로 빈자리를 메운다고 생각해 봅니다. 판 한 장이 안 맞으면 같은 모양 판을 여러 장 만듭니다. 여러 장을 나란히 두고 어느 장이 잘 맞는지 살핍니다. 마지막에는 네 장을 다시 한 묶음으로 포개어 하나로 씁니다.</p>
{{img:02-5-한-장에서-네-장으로-늘린-나무판|흰 바탕에 왼쪽에는 나무판 한 장이 있고 가운데에는 같은 모양 나무판 네 장이 부채처럼 나란히 펼쳐져 있으며 오른쪽에는 그 네 장이 다시 한 묶음으로 가지런히 포개져 있는 그림|왼쪽 판 한 장이 가운데에서 네 장으로 늘었다가 오른쪽에서 다시 한 묶음으로 포개집니다.}}
<p class="look"><b>그림 읽기</b> — 왼쪽에 나무판 한 장이 놓여 있습니다. 가운데에는 같은 모양 판 네 장이 부채처럼 펼쳐져 있습니다. 오른쪽에는 그 네 장이 다시 한 묶음으로 포개져 있습니다. 세 자리를 왼쪽부터 오른쪽으로 읽으면 하나에서 넷으로 늘었다가 다시 하나로 모이는 차례가 보입니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>변형 질문</td><td>원 질문과 같은 것을 묻되 표현을 달리해 만든 검색 질문입니다. 이 절에서는 세 개입니다.</td></tr><tr><td>합친 목록</td><td>순위 목록 여러 개를 자리 몫으로 더해 하나로 만든 목록입니다.</td></tr></tbody></table>
<p>아래 네 말은 Ch 11·Ch 12에서 쓰던 뜻 그대로 이어 씁니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>순위 합치기</td><td>순위 목록 여러 개를 하나로 만드는 일입니다(Ch 12 06절).</td></tr><tr><td>순위 상수</td><td>자리 번호에 더해 몫을 줄이는 값이고 이 절도 <code>60</code>입니다(Ch 12 06절).</td></tr><tr><td>가중치</td><td>목록 하나가 합친 점수에 보태는 몫의 크기입니다(Ch 12 06절).</td></tr><tr><td>정답 자리</td><td>순위 목록에서 정답 문서가 몇째 자리인지 센 값입니다(Ch 11 01절).</td></tr></tbody></table>
{{mermaid:02-1-질문-하나를-여러-갈래로-늘리기|위에서 아래로 놓인 상자 일곱으로 맨 위에 초록 상자 원 질문 C01 책을 빌릴 수 있는 기간은 며칠인가요가 있고 그 아래 파란 상자 우리가 적은 변형 프롬프트와 보라 상자 답 모델 gpt-5.4-mini를 지나 노란 상자 변형 질문 세 줄로 이어지며 원 질문과 변형 질문이 모두 파란 상자 우리가 적은 거리 검색 네 번으로 모여 파란 상자 우리가 적은 순위 합치기를 거쳐 맨 아래 노란 상자 정답 문서 LIB-001이 자리 하나로 이어지는 그림|질문 하나를 변형 질문 셋으로 늘려 네 목록을 합치면 정답 문서가 자리 하나로 올라옵니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자가 사람이 적은 원 질문입니다. 파란 상자 셋은 우리가 적은 글과 처리이고 보라 상자가 이번에 부른 모델입니다. 노란 상자 둘은 출력으로 확인한 값입니다. 원 질문은 변형 프롬프트로도 가고 거리 검색으로도 갑니다.</p>
<h3>원 질문을 지우지 않습니다</h3><p>변형 질문은 검색에 넣는 글입니다. 사람이 적은 원 질문도 목록에 그대로 넣습니다. 원 질문 목록까지 합쳐야 변형이 빗나갔을 때 기댈 자리가 남습니다.</p>
<h3>모델이 만든 질문은 출처가 아닙니다</h3><p>변형 질문은 모델이 쓴 글입니다. 자료에서 확인한 사실이 아니라 검색에 넣으려고 만든 글입니다. 답의 출처로는 찾은 문서의 ID와 원문만 씁니다.</p>
<h3>늘리는 개수를 값으로 적어 둡니다</h3><p>변형 질문 하나마다 임베딩 요청이 한 번씩 늘어납니다. 그래서 개수를 코드에 값으로 적고 머리글도 그 값으로 만듭니다. 값 하나를 바꾸면 머리글과 실제로 쓰는 개수가 함께 바뀝니다.</p>
<h3>다른 상황에 적용</h3><p>고객 문의에도 같은 자리가 있습니다. 「환불되나요」라는 물음을 「반품 규정」과 「결제 취소 절차」로 늘려 봅니다. 늘린 질문마다 찾은 목록을 합치면 한 갈래로 찾지 못한 문서가 앞으로 올 수 있습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 문서 열두 건을 벡터로 바꾼 뒤 질문 두 개를 각각 네 갈래로 검색합니다. 서비스 요청은 열한 번이고 임베딩 아홉 번과 답 모델 두 번입니다. 예상 비용은 미화 0.01달러 아래입니다. 새로 쓰는 파일은 없습니다.</p><p>먼저 질문 <code>C01</code>을 한 번만 검색해 정답 문서의 자리를 셉니다. 그다음 변형 질문 셋을 만들고 네 목록을 모읍니다. 이어서 네 목록을 순위 합치기로 하나로 만들어 자리를 다시 셉니다. 마지막으로 질문만 <code>C02</code>로 바꾸어 같은 일을 다시 합니다.</p>
{{mermaid:02-2-자리-번호를-몫으로-바꾸기|위에서 아래로 놓인 상자 다섯으로 맨 위 초록 상자 순위 목록 네 개 아래에 파란 상자 목록마다 자리 번호 세기와 파란 상자 몫은 가중치를 60 더하기 자리 번호로 나눈 값과 파란 상자 문서마다 몫을 모두 더하기가 차례로 이어지고 맨 아래 노란 상자 첫 자리가 받는 몫은 0.0164로 이어지는 그림|자리 번호를 몫으로 바꾸어 문서마다 더하면 여러 목록에서 앞자리인 문서가 위로 올라옵니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자가 합칠 순위 목록 넷입니다. 파란 상자 셋은 Ch 12 06절 함수가 하는 일을 차례로 적은 것입니다. 맨 아래 노란 상자는 노트북 6절이 출력한 첫 자리 몫입니다.</p>
{{notebook:02-Multi-Query}}
<p class="look"><b>확인할 점</b> — 질문 <code>C01</code> 순위 표의 세 문서가 01절 표와 같은지 봅니다. 한 번만 검색한 출력 줄은 <code>한 번만 검색했을 때 정답 문서의 자리: 2</code>였습니다. 네 목록을 합친 뒤에는 <code>합친 뒤 정답 문서의 자리: 1</code>이었습니다. 질문을 바꾼 자리에서는 같은 줄이 <code>합친 뒤 정답 문서의 자리: 4</code>였습니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>질문 <code>C01</code>을 한 번만 검색하니 첫 자리가 <code>LIB-004</code>였습니다. 전자책을 다룬 문서이고 이 질문의 정답 문서가 아닙니다. 정답 문서 <code>LIB-001</code>은 둘째 자리였습니다. 거리 상위 셋은 01절이 Ch 12 05절과 대조한 표와 같았습니다.</p><p>변형 질문 셋을 더해 목록이 넷이 되었습니다. 네 목록을 순위 합치기로 합치니 정답 문서가 첫 자리로 왔습니다. 같은 문서 열두 건에서 질문 수만 늘렸는데 자리가 한 칸 올라왔습니다. 목록마다 정답 문서가 몇째였는지는 실행마다 달라져 여기에 적지 않았습니다.</p>
{{mermaid:02-3-한-번-검색과-합친-목록|왼쪽부터 오른쪽으로 놓인 칸 두 개와 회색 상자 하나로 왼쪽 칸 제목은 질문 하나로 한 번 검색이고 그 안에 초록 상자 검색에 쓴 질문 하나와 노란 상자 첫 자리 문서 LIB-004와 노란 상자 정답 문서 LIB-001은 자리 둘이 있으며 가운데 칸 제목은 네 목록을 합친 뒤이고 그 안에 초록 상자 검색에 쓴 질문 넷과 노란 상자 첫 자리 문서 LIB-001과 노란 상자 정답 문서 LIB-001은 자리 하나가 있고 오른쪽에 회색 상자 두 검색 모두 같은 문서 열두 건에서 고름이 놓인 그림|같은 문서 열두 건에서 질문 하나로 검색하면 정답 문서가 자리 둘이고 네 목록을 합치면 자리 하나입니다.}}
<p class="look"><b>도식 읽기</b> — 왼쪽 칸이 질문 하나로 한 번 검색한 자리입니다. 가운데 칸이 변형 질문을 더해 네 목록을 합친 자리입니다. 칸마다 맨 위 초록 상자가 넣은 질문이고 그 아래 노란 상자 둘이 나온 값입니다. 오른쪽 회색 상자는 두 칸에 모두 해당하는 사실입니다.</p>
<p>질문을 <code>C02</code>로 바꾸면 결과가 달랐습니다. 한 번만 검색했을 때 정답 문서 <code>LIB-002</code>는 일곱째 자리였습니다. 목록 넷 가운데 하나만 그 문서를 첫 자리에 두었습니다.</p><p>네 목록을 같은 방법으로 합쳤더니 정답 문서는 넷째 자리였습니다. 자리는 일곱에서 넷으로 올라왔지만 앞 세 자리 안에는 들지 못했습니다. 순위 합치기는 여러 목록에서 고르게 앞자리인 문서를 위로 올립니다. 한 목록에서만 앞자리인 문서는 몫을 한 번밖에 모으지 못합니다.</p>
{{mermaid:02-4-늘려도-앞으로-오지-않는-질문|왼쪽부터 오른쪽으로 놓인 칸 두 개와 회색 상자 하나로 왼쪽 칸 제목은 질문 하나로 한 번 검색이고 그 안에 초록 상자 검색에 쓴 질문 하나와 노란 상자 정답 문서 LIB-002는 자리 일곱이 있으며 가운데 칸 제목은 네 목록을 합친 뒤이고 그 안에 초록 상자 검색에 쓴 질문 넷과 노란 상자 목록 하나만 정답 문서를 첫 자리에 둠과 노란 상자 정답 문서는 자리 넷이 있고 오른쪽에 회색 상자 C01과 C02에 같은 머리글과 같은 가중치를 씀이 놓인 그림|한 목록에서만 앞자리인 문서는 몫을 한 번밖에 모으지 못해 합친 뒤에도 자리 넷에 머뭅니다.}}
<p class="look"><b>도식 읽기</b> — 왼쪽 칸이 바꾼 질문을 한 번만 검색한 자리입니다. 가운데 칸이 같은 질문을 네 갈래로 늘려 합친 자리입니다. 칸마다 맨 위 초록 상자가 넣은 질문이고 그 아래 노란 상자가 출력으로 확인한 값입니다. 오른쪽 회색 상자는 질문 C01과 C02에서 같게 둔 것입니다.</p>
<p>여기서 본 것은 질문 두 개입니다. 여덟 질문 모두에서 같은 차이가 나는지는 이번에 확인하지 않았습니다. 여러 질문으로 검색 품질을 재는 일은 Ch 11과 Ch 12 몫입니다. 답이 맞는지 판정하는 일은 Ch 15 몫입니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>질문 두 개는 흐름을 보여 주려고 고른 예입니다. 여덟 질문을 모두 재어 본 뒤 앞 세 자리 안으로 들어오는 질문과 들어오지 못하는 질문을 하나씩 골랐습니다.</li><li>01절이 만든 독립 질문은 한 번 검색으로도 정답 문서가 첫 자리였습니다. 늘린 효과를 보이려고 01절이 Ch 12와 대조한 질문 <code>C01</code>을 이어 썼습니다.</li><li>변형 질문은 모델이 쓴 글이라 실행마다 문장이 달라집니다. 그 문장에 <code>assert</code>를 걸지 않았습니다.</li><li>새 커널로 두 번 실행하니 변형 질문 문장 셋이 달라졌습니다. 두 질문의 한 번 검색 자리와 합친 뒤 자리는 두 실행에서 같았습니다.</li><li>목록별 첫 자리 문서는 한 줄이 두 실행에서 달랐습니다. 어느 목록이 어떤 문서를 앞에 두었는지는 그림과 정리에 넣지 않았습니다.</li><li>모델이 보낸 글을 줄로 나눌 때 글자를 깎지 않았습니다. 빈 줄만 빼고 앞의 세 줄만 골라 씁니다.</li><li>변형 질문을 셋 만들면 임베딩 요청이 세 번 늘어납니다. 이 절은 걸린 시간을 재지 않았으므로 빨라졌는지 느려졌는지 적지 않습니다.</li><li>늘린 질문이 대상이나 조건을 바꾸면 검색이 다른 문서를 찾습니다. 머리글에 대상과 조건을 그대로 두라는 줄을 넣었습니다.</li><li>모델이 만든 변형 질문은 검색에 넣는 글일 뿐이라 출처로 쓰지 않습니다. 출처는 찾은 문서의 ID와 원문입니다.</li><li>거리 값은 셋째 자리 아래가 호출마다 조금씩 달라집니다. 본문과 그림에는 자리 번호와 문서 ID만 적었습니다.</li><li>이 절은 파일을 쓰지 않습니다. 문서 파일과 질문 파일은 읽기만 합니다.</li><li>준비물에 LangChain 1.4.0과 langchain-openai 1.6.1과 numpy 2.5.3을 적었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>질문 하나만으로 검색하니 질문 <code>C01</code>의 정답 문서는 둘째 자리였습니다.</li><li>변형 질문 셋을 더해 네 목록을 합치니 정답 문서가 첫 자리로 왔습니다.</li><li>질문 <code>C02</code>에서는 같은 방법을 써도 정답 문서가 앞 세 자리 안에 들지 못했습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 03절에서는 한 질문 안에 섞인 여러 사실을 하위 질문으로 나눕니다. 이 절의 변형 질문은 같은 것을 묻고 03절의 하위 질문은 다른 것을 묻습니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 변형 질문의 입력과 출력은 무엇입니까?</p><p class="quiz-a">질문 하나를 넣으면 같은 것을 묻되 표현이 다른 검색 질문 세 개가 나옵니다. 틀렸다면 「핵심 개념」의 용어 표를 다시 읽습니다.</p><p class="quiz-q">2. 질문 <code>C01</code>에서 합치기 전과 뒤에 무엇이 달라졌습니까?</p><p class="quiz-a">정답 문서 <code>LIB-001</code>의 자리가 둘에서 하나로 올라왔습니다. 첫 자리 문서도 <code>LIB-004</code>에서 <code>LIB-001</code>로 바뀌었습니다. 틀렸다면 「실험 결과 해석」의 첫 비교 도식을 다시 읽습니다.</p><p class="quiz-q">3. 질문 <code>C02</code>에서는 왜 정답 문서가 앞 세 자리 안에 들지 못했습니까?</p><p class="quiz-a">목록 넷 가운데 하나만 그 문서를 첫 자리에 두었기 때문입니다. 순위 합치기는 여러 목록에서 고르게 앞자리인 문서를 위로 올립니다. 틀렸다면 「실험 결과 해석」의 둘째 비교 도식을 다시 읽습니다.</p><p class="quiz-q">4. 변형 질문을 늘릴 개수를 코드에 값으로 적어 두는 까닭은 무엇입니까?</p><p class="quiz-a">머리글과 실제로 쓰는 개수를 한 자리에서 맞추고 늘어난 요청 수를 셀 수 있기 때문입니다. 틀렸다면 「핵심 개념」의 마지막 소제목을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/concepts/providers-and-models">LangChain 모델과 provider</a></div>확인 2026-09-19 · LangChain 1.4 기준 · 변형 질문을 만드는 모델을 준비하는 방법.</li><li><div><a href="https://developers.openai.com/api/docs/models/text-embedding-3-small">OpenAI text-embedding-3-small 모델 안내</a></div>확인 2026-09-19 · 문서와 질문을 벡터로 바꿀 때 쓴 모델과 차원 수 설정.</li><li><div><a href="https://arxiv.org/abs/2402.03367">RAG-Fusion 논문</a></div>확인 2026-09-19 · 질문을 여러 개로 늘려 검색하고 순위를 합치는 방법의 출처.</li><li>Ch 12 06절 하이브리드 검색 — 이 절이 이어 쓴 순위 합치기 함수 두 개와 순위 상수가 있는 자리.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(SRC_HTML, encoding="utf-8")
    return SRC


if __name__ == "__main__":
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "02", "02-Multi-Query", "experiment", cells())
        print("wrote", path)
