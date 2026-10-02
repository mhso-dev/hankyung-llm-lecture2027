"""Ch 14 05절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§3·§6).

사용:
  python3 author_05.py            → 노트북 + _src 본문을 함께 다시 쓴다
  python3 author_05.py --src-only → 본문 HTML만 다시 쓴다(노트북 출력을 지우지 않는다)

이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북과 본문은 qa/upgrade/before/ 에 있다. **experiment 형식 유지**(chapter.json).

## 가져온 함수 여섯 개 (§2-7 리팩터 2026-09-21 — 도구 파일 `notebooks/rag_tools.py`)

준비 셀(import 셀)에서 Ch 12·Ch 11 함수 넷(`rank_by_distance`·`print_ranked`·`unique_doc_ids`·`find_gold_rank`)과
02절 `split_lines`·`search_ids(embedding_model, question, doc_vectors, doc_ids, top_count)`를 가져온다.
리팩터 전에는 이 함수들(+ `dot_product`·`vector_length`)을 준비 셀 다섯에 다시 적었다.
Ch 12 06절 순위 합치기는 04절에 이어 가져오지 않는다(목록을 합치지 않음).

## 이 절이 새로 만든 함수 둘

`build_hyde_prompt(question)` — 질문에 답할 법한 안내문을 지어 쓰게 하는 머리글을 만든다.
`join_lines(lines)` — 모델이 두 줄로 보낸 글을 한 글로 이어 붙인다(handoff §04→§05 2번이 물은 자리).
기록 함수 `run_row(run_name, search_text, found_ids, place)`는 01·02·04절 판과 인자 모양이 같고
**칸 이름 하나만 다르다**: 「검색에 쓴 질문」 → 「검색에 넣은 글」. 이 절은 질문이 아닌 글도 넣는다.

## 선택한 것과 까닭

1. **개선 전 05절 질문을 잇지 않았다.** 개선 전 질문의 정답 문서 `ACC-003`은 03절이 둘째 근거로
   이미 쓴다. 정답 문서가 겹치지 않도록 01~04절이 쓰지 않은 `LIB-004`로 바꿨다.
   질문은 짧게 적은 「폰으로 보는 건 며칠이에요?」다(탐색 실행으로 고름, 아래 §탐색).
2. **가상 문서의 문장 수를 코드 상수 `doc_sentences = 2`로 못 박았다.** 머리글도 `str(doc_sentences)`로
   만들어 값 하나를 바꾸면 머리글과 실제로 받는 문장 수가 함께 바뀐다.
3. **줄을 이어 붙여 한 글로 쓴다.** 두 문장이 한 줄로 올 때도 두 줄로 올 때도 있어
   `split_lines`로 빈 줄을 뺀 뒤 `join_lines`로 이어 붙인다. 앞 줄만 쓰면 둘째 문장이 사라진다.
4. **머리글에 지어낸 숫자를 넣지 말라는 줄을 두었다.** 숫자를 지어내게 두면 그 숫자가 실행마다
   달라져 검색 결과와 정답 자리까지 흔들렸다(탐색 실행 probe5·probe6). 지어낸 숫자를 답에 쓰지
   않는다는 이 절의 태도와도 맞는다.
5. **목록을 합치지 않는다.** 04절과 같이 두 검색의 첫 자리 문서를 모으고 `unique_doc_ids`로
   겹치는 문서를 뺀 「근거 문서 목록」(03절 용어)을 이어 쓴다.
6. **값 바꿔 보기는 정답 문서를 그대로 두고 질문만 바꾼다.** 바꾼 질문의 가상 문서는 일반 도서
   대출 쪽으로 기울어 정답 문서가 앞 세 자리 밖으로 밀렸다. 나빠진 결과를 그대로 싣는다.
7. **걸린 시간과 비용 추정을 넣지 않는다.** Ch 12부터 이 과정은 걸린 시간을 한 번도 재지 않았다.
8. **모델 이름을 `gpt-5.4-mini`로 바꿨다**(규격 §6 기준 버전). b10의 옛 모델 단가 줄도 뺐다.
9. **모델 답에 `assert`를 걸지 않는다**(규격 §3). `assert`는 키 확인과 자리 확인 두 곳뿐이다.
10. **답을 만들지 않는다.** 이 절의 학습 질문은 검색에 넣을 글을 바꾸는 자리까지다.
11. **쓰지 않은 것**(벡터 계산은 도구 파일 안 NumPy): `lambda`·내포식·제너레이터 식·조건 표현식·f-string·`key=`·`reverse=`·
    `set`·기본값 매개변수·복합 타입힌트·세미콜론·한 줄 다중 대입·클래스 정의·`time`·`enumerate`·
    `zip`·`next`·`join`. 부른 내장 이름은 `len`·`open`·`print`·`range`·`round`·`sorted`·`str`뿐이다.

## 탐색 실행에서 확인한 값 (2026-09-19, /tmp/ch14-05/probe1.py~probe9.py)

langchain 1.4.0 · langchain-openai 1.6.1 · Python 3.12.13 · 문서 12건 · 질문 8건.
짧게 적은 질문 스물여섯 개의 한 번 검색 자리를 재어 보고, 그 가운데 정답 문서가 앞 세 자리 밖인
질문 넷을 골라 가상 문서를 각각 두세 번 지어 보았다. 숫자를 지어내도 좋다고 둔 머리글에서는
같은 질문에서도 정답 자리가 하나와 둘로 갈렸다. 숫자를 넣지 말라는 줄을 더하니 세 번 모두
자리가 하나였다. 바꾼 질문 쪽은 세 번 모두 앞 세 자리 밖이었다.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part4/ch14-rag-patterns/notebooks"
SRC = ROOT / "textbook/part4/ch14-rag-patterns/_src/05-HyDE.html"

INSTALL = install_source([
    "langchain==1.4.0", "langchain-openai==1.6.1", "python-dotenv==1.2.3", "numpy==2.5.3",
])

IMPORTS = r'''# 자료 읽기·폴더 확인과 임베딩·답 모델 이름을 불러옵니다
import json
import os

from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model
# Ch 12 01·05절·Ch 11 01절 함수와 02절 함수를 도구 파일에서 가져옵니다
from rag_tools import find_gold_rank, print_ranked, rank_by_distance, search_ids
from rag_tools import split_lines, unique_doc_ids

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

VALUES = r'''# Ch 12에서 쓴 값을 그대로 다시 정하고 지어낼 가상 문서의 문장 수도 못 박습니다
top_three = 3
top_all = 12
doc_sentences = 2
print("나란히 볼 상위 문서 수:", top_three)
print("자리를 셀 때 재는 문서 수:", top_all)
print("가상 문서의 문장 수:", doc_sentences)'''

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

PICK_QUESTION = r'''# 일상에서 말하듯 짧게 적은 원 질문과 그 질문의 정답 문서를 정합니다
base_question = "폰으로 보는 건 며칠이에요?"
gold_doc_id = "LIB-004"
gold_title = ""
for doc in docs:
    if doc["doc_id"] == gold_doc_id:
        gold_title = doc["title"]
print("원 질문:", base_question)
print("이 질문의 정답 문서 ID:", gold_doc_id)
print("그 문서의 제목:", gold_title)'''

BASE_SEARCH = r'''# 원 질문을 한 번만 검색해 순위 표와 정답 문서의 자리를 봅니다(임베딩 요청 1번)
base_vector = embedding_model.embed_query(base_question)
base_hits = rank_by_distance(base_vector, doc_vectors, doc_ids, top_all)
base_ids = unique_doc_ids(base_hits)
base_place = find_gold_rank(base_ids, [gold_doc_id])
print_ranked(base_hits[:top_three], "거리")
print("원 질문으로 검색했을 때 정답 문서의 자리:", base_place)'''

BUILD_HYDE_PROMPT = r'''# 머리글 네 줄과 원 질문을 한 글로 이어 붙입니다
def build_hyde_prompt(question):
    hyde_head = "아래 질문에 답할 법한 도서관 안내문을 지어 쓰세요.\n"
    hyde_head = hyde_head + "물음표로 끝나는 질문이 아니라 안내문 문장으로 " + str(doc_sentences) + "문장 적으세요.\n"
    hyde_head = hyde_head + "지어낸 숫자는 넣지 말고 무엇을 어디에서 하는지만 적으세요.\n"
    hyde_head = hyde_head + "번호나 따옴표를 붙이지 마세요.\n\n"
    prompt_text = hyde_head + "질문: " + question
    return prompt_text'''

HYDE_CALL = r'''# 만든 글을 모델에 넣어 답처럼 보이는 안내문을 받습니다(모델 요청 1번)
hyde_prompt = build_hyde_prompt(base_question)
print("모델에 넣을 글:")
print(hyde_prompt)
hyde_reply = model.invoke(hyde_prompt)
hyde_text = hyde_reply.text.strip()
print("모델이 쓴 글:")
print(hyde_text)'''

JOIN_LINES = r'''# 줄 목록을 사이에 빈칸 하나를 두고 한 글로 이어 붙입니다
def join_lines(lines):
    joined_text = ""
    for line in lines:
        if joined_text == "":
            joined_text = line
        else:
            joined_text = joined_text + " " + line
    return joined_text'''

MAKE_DOC = r'''# 모델이 보낸 글에서 빈 줄을 빼고 줄을 이어 붙여 가상 문서 한 글로 만듭니다
hyde_lines = split_lines(hyde_text)
hyde_doc = join_lines(hyde_lines)
print("모델이 보낸 줄 수:", len(hyde_lines))
print("가상 문서:")
print(hyde_doc)'''

HYDE_SEARCH = r'''# 질문 대신 가상 문서를 검색에 넣어 순위 표와 정답 문서의 자리를 봅니다(임베딩 요청 1번)
hyde_vector = embedding_model.embed_query(hyde_doc)
hyde_hits = rank_by_distance(hyde_vector, doc_vectors, doc_ids, top_all)
hyde_ids = unique_doc_ids(hyde_hits)
hyde_place = find_gold_rank(hyde_ids, [gold_doc_id])
print_ranked(hyde_hits[:top_three], "거리")
print("가상 문서로 검색했을 때 정답 문서의 자리:", hyde_place)'''

EVIDENCE = r'''# 두 검색의 첫 자리 문서를 모으고 겹치는 문서를 빼 근거 문서 목록을 만듭니다
top_hits = []
top_hits.append({"doc_id": base_ids[0]})
top_hits.append({"doc_id": hyde_ids[0]})
evidence_ids = unique_doc_ids(top_hits)
print("원 질문 첫 자리 문서:", base_ids[0])
print("가상 문서 첫 자리 문서:", hyde_ids[0])
print("근거 문서 목록:", evidence_ids)'''

SECOND_PICK = r'''# 바꿀 값은 검색에 넣을 원 질문 하나이고 정답 문서는 앞과 같은 문서로 둡니다(임베딩 요청 1번)
second_question = "한 번에 몇 권까지 되나요?"
second_ids = search_ids(embedding_model, second_question, doc_vectors, doc_ids, top_all)
second_place = find_gold_rank(second_ids, [gold_doc_id])
print("바꾼 질문:", second_question)
print("정답 문서는 앞과 같은 ID:", gold_doc_id)
print("바꾼 질문으로 한 번 검색했을 때 정답 문서의 자리:", second_place)'''

SECOND_CALL = r'''# 같은 머리글로 바꾼 질문의 가상 문서도 지어 봅니다(모델 요청 1번)
second_prompt = build_hyde_prompt(second_question)
second_reply = model.invoke(second_prompt)
second_lines = split_lines(second_reply.text.strip())
second_doc = join_lines(second_lines)
print("모델이 보낸 줄 수:", len(second_lines))
print("가상 문서:")
print(second_doc)'''

SECOND_SEARCH = r'''# 바꾼 질문의 가상 문서로 검색해 같은 방법으로 근거 문서 목록을 만듭니다(임베딩 요청 1번)
second_doc_ids = search_ids(embedding_model, second_doc, doc_vectors, doc_ids, top_all)
second_doc_place = find_gold_rank(second_doc_ids, [gold_doc_id])
second_hits = []
second_hits.append({"doc_id": second_ids[0]})
second_hits.append({"doc_id": second_doc_ids[0]})
second_evidence = unique_doc_ids(second_hits)
print("가상 문서 첫 자리 문서:", second_doc_ids[0])
print("가상 문서로 검색했을 때 정답 문서의 자리:", second_doc_place)
print("근거 문서 목록:", second_evidence)'''

RUN_ROW = r'''# 실행 한 번을 기록 한 줄로 만듭니다
def run_row(run_name, search_text, found_ids, place):
    row = {"실행": run_name}
    row["검색에 넣은 글"] = search_text
    row["첫 자리 문서"] = found_ids[0]
    row["정답 자리"] = place
    return row'''

TABLE = r'''# 네 실행의 기록을 담아 라벨 줄 아래에 한 줄씩 출력합니다
run_rows = []
run_rows.append(run_row("원 질문 한 번 검색", base_question, base_ids, base_place))
run_rows.append(run_row("가상 문서로 검색", hyde_doc, hyde_ids, hyde_place))
run_rows.append(run_row("바꾼 질문 한 번 검색", second_question, second_ids, second_place))
run_rows.append(run_row("바꾼 질문의 가상 문서", second_doc, second_doc_ids, second_doc_place))
print("실행 | 첫 자리 문서 | 정답 자리")
for row in run_rows:
    print(row["실행"], "|", row["첫 자리 문서"], "|", row["정답 자리"])
    print("  검색에 넣은 글:", row["검색에 넣은 글"])'''

TITLE = """# HyDE

**이 노트북에서 할 일**

1. Ch 12에서 쓰던 문서 열두 건과 질문 여덟 개를 그대로 읽습니다.
2. 일상에서 말하듯 짧게 적은 원 질문을 하나 정합니다.
3. 그 질문을 한 번만 검색해 정답 문서의 자리를 셉니다.
4. 같은 질문에 답할 법한 안내문을 모델에게 지어 받습니다.
5. 질문 대신 그 글을 검색에 넣어 정답 문서의 자리를 다시 셉니다.
6. 질문만 바꾸어 같은 일을 다시 하고 두 결과를 견줍니다.

**준비물** — 이 절은 프로젝트 맨 위 폴더의 `.env`에 적어 둔 `OPENAI_API_KEY`를 씁니다.
서비스 요청은 일곱 번입니다(임베딩 다섯 번과 답 모델 두 번).
예상 비용은 미화 0.01달러 아래입니다.
읽어 오는 파일은 이 챕터 폴더의 문서 파일과 질문 파일 둘이고 새로 쓰는 파일은 없습니다.
실행 시간은 2분 안팎이고 첫 셀의 설치가 가장 오래 걸립니다.

**기준 버전** — 첫 셀에서 LangChain 1.4.0과 langchain-openai 1.6.1을 설치합니다.
키를 읽는 python-dotenv 1.2.3과 도구 파일이 쓰는 numpy 2.5.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3절부터 7절까지 읽습니다.
Ch 12 검색 부품을 준비하고 짧게 적은 원 질문을 고르는 자리입니다.
8절과 9절은 가상 문서를 지어 그 글로 검색하는 자리입니다.
10절과 11절은 질문을 바꾸어 같은 일을 한 번 더 하고 네 실행을 표로 보는 자리입니다.

실습 폴더 `labs/part4/ch14-rag-patterns`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""

FIGURE_ALT = ("위에서 아래로 놓인 상자 여섯으로 맨 위에 초록 상자 일상 말로 짧게 적은 원 질문이 있고 "
              "그 아래 파란 상자 우리가 적은 안내문 머리글과 보라 상자 답 모델 gpt-5.4-mini를 지나 노란 상자 "
              "가상 문서 두 문장으로 이어지며 그 아래 파란 상자 가상 문서로 거리 검색을 거쳐 맨 아래 노란 상자 "
              "정답 문서 LIB-004가 첫 자리로 이어지는 그림")

FIGURE_READ = """위에서 아래로 읽습니다.
맨 위 초록 상자가 사람이 적은 질문입니다.
가운데 파란 상자 둘이 우리가 적은 글과 처리이고 보라 상자가 모델입니다.
노란 상자 둘이 출력으로 확인한 값입니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIGURE_ALT + "](attachment:05-1-질문-대신-가상-문서로-검색하기.png)\n\n" + FIGURE_READ, html="skip"),
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
Ch 11 01절 `unique_doc_ids()`·`find_gold_rank()`도 가져옵니다.
02절에서 만든 `split_lines()`와 `search_ids()`도 함께 가져옵니다.
인자 모양은 5절에서 설명합니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄에 불러온 이름 네 개가 보입니다.
이름 `OpenAIEmbeddings`와 `init_chat_model`은 04절에서 쓴 것과 같습니다.
도구 파일에서 가져온 함수 여섯 개는 출력하지 않습니다.

## 2. 키와 모델 준비"""),
    ] + key_and_model_cells("openai:gpt-5.4-mini") + [
        md("""## 3. 문서와 질문 읽기

이 절은 01~04절과 같은 문서 파일과 질문 파일을 읽습니다.
두 파일은 Ch 12 core 벌 파일과 바이트가 같은 사본입니다.
먼저 노트북을 연 자리에서 프로젝트 맨 위를 찾습니다."""),
        code(ROOT_PATH),
        md("""**결과 읽기** — 출력 줄 `고른 자리` 뒤에 점 하나나 위로 올라가는 표시가 보입니다.
Ch 10~13과 01~04절에서 쓴 방법과 같습니다.
후보 셋 가운데 이 챕터 자료 폴더가 있는 자리를 고릅니다.

다음 셀은 문서 파일과 질문 파일을 읽습니다."""),
        code(LOAD_DATA),
        md("""**결과 읽기** — 출력 줄 `문서 수: 12`와 `질문 수: 8`이 Ch 12 core 벌 그대로입니다.
문서는 도서관 안내 열두 건입니다.

질문 번호는 C01부터 C08까지이고 질문 파일에 적혀 있습니다.
이 절이 쓸 질문은 그 여덟 개에 없어 아래에서 손으로 적습니다.

## 4. 이 절에서 쓸 값 정하기

Ch 12와 01~04절에서 정한 값을 그대로 다시 적습니다.
지어낼 가상 문서의 문장 수도 여기서 못 박아 둡니다."""),
        code(VALUES),
        md("""**결과 읽기** — 출력 줄 `나란히 볼 상위 문서 수: 3`은 표로 볼 자리 수입니다.
출력 줄 `자리를 셀 때 재는 문서 수: 12`는 정답 문서의 자리를 끝까지 세려고 둔 값입니다.
출력 줄 `가상 문서의 문장 수: 2`는 모델에게 받을 문장 수입니다.

04절은 이 자리에 만들 넓힌 질문 개수 하나를 두었습니다.
이 절은 질문이 아니라 두 문장짜리 글을 받으므로 값의 뜻이 다릅니다.

## 5. 앞 절 부품 준비

다음 셀은 01~04절과 같은 방법으로 문서 열두 건의 제목과 본문을 이어 붙입니다.
읽지 말고 실행만 하고 넘어가도 됩니다.
함수는 준비 셀에서 도구 파일로 가져왔습니다.
02절 `search_ids()`의 도구 파일 판은 임베딩 모델과 질문과 문서 벡터 목록과 문서 ID 목록과 개수를 받습니다."""),
        code(DOC_TEXTS, lesson_role="setup"),
        md("""준비 셀 하나를 지났습니다.
02·03절이 쓴 순위 합치기 함수는 04절에 이어 이 절에서도 가져오지 않았습니다.
이 절도 목록 여러 개를 하나로 합치지 않기 때문입니다.

## 6. 문서를 벡터로 바꾸기

다음 셀은 문서 열두 건을 벡터로 바꿉니다.
이 절에서 서비스에 보내는 첫 요청입니다."""),
        code(EMBEDDINGS),
        md("""**결과 읽기** — 출력 줄 `임베딩 모델 이름: text-embedding-3-small`은 04절과 같은 모델입니다.
출력 줄 `벡터의 숫자 개수 설정: 256`도 Ch 10~13과 같은 값입니다.
출력 줄 `문서 벡터 수: 12`로 문서마다 벡터 하나를 받았습니다.
벡터 안의 숫자는 호출마다 아주 조금씩 달라져 소수 자리까지 같다고 보지 않습니다.

## 7. 짧게 적은 원 질문

자료의 문서는 안내문 문장으로 적혀 있습니다.
사람이 묻는 말은 그보다 짧고 쓰는 낱말도 다릅니다.
그런 질문을 하나 적고 판단에 쓸 정답 문서도 함께 정합니다."""),
        code(PICK_QUESTION),
        md("""**결과 읽기** — 출력 줄 `원 질문` 뒤에 아홉 글자짜리 짧은 물음이 있습니다.
출력 줄 `이 질문의 정답 문서 ID: LIB-004`는 전자책 이용을 적은 문서입니다.
출력 줄 `그 문서의 제목: 전자책 이용`으로 제목을 확인했습니다.

실행 전에 예상해 봅니다.
질문에 전자책이라는 말이 없으니 다른 문서가 먼저 걸릴 것입니다."""),
        code(BASE_SEARCH),
        md("""**결과 읽기** — 순위 표의 차례는 `FAC-003`과 `ACC-001`과 `FAC-002`입니다.
세 문서 모두 이 물음의 정답 문서가 아닙니다.
출력 줄 `원 질문으로 검색했을 때 정답 문서의 자리: 4`로 정답 문서는 넷째였습니다.

거리 값은 셋째 자리 아래가 호출마다 달라져 본문과 그림에 넣지 않았습니다.
짧은 물음에는 자료가 쓰는 낱말이 거의 들어 있지 않습니다.

## 8. 답처럼 보이는 글 지어내기

01절부터 04절까지는 질문을 질문으로 바꿔 검색했습니다.
이 절은 질문 대신 답처럼 보이는 글을 지어 검색에 넣습니다.
머리글에 문장 수와 모양을 적고 지어낸 숫자를 넣지 말라는 줄도 함께 넣습니다."""),
        code(BUILD_HYDE_PROMPT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `build_hyde_prompt`는 머리글 네 줄을 이어 붙인 뒤 원 질문을 답니다.
머리글의 문장 수 자리에는 앞에서 정한 값 `doc_sentences`가 들어갑니다.
숫자를 넣지 말라고 적은 까닭은 지어낸 숫자를 답에 쓸 수 없기 때문입니다.

다음 셀은 그 글을 만들어 모델에 넣습니다."""),
        code(HYDE_CALL),
        md("""**결과 읽기** — 라벨 줄 `모델에 넣을 글:` 아래에 머리글 네 줄과 원 질문이 있습니다.
라벨 줄 `모델이 쓴 글:` 아래에는 물음표가 없는 안내문이 있습니다.
04절까지는 이 자리에 늘 질문이 나왔습니다.

이 글은 자료에서 확인한 사실이 아닙니다.
문장은 실행마다 달라질 수 있어 이 값에 `assert`를 걸지 않았습니다."""),
        code(JOIN_LINES),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `join_lines`는 줄 목록을 받아 사이에 빈칸 하나를 두고 이어 붙입니다.
두 문장이 한 줄로 올 때도 있고 두 줄로 나뉘어 올 때도 있습니다.
앞 줄만 쓰면 둘째 문장이 사라지므로 모두 이어 붙입니다.

다음 셀은 빈 줄을 뺀 뒤 그 함수로 가상 문서를 만듭니다."""),
        code(MAKE_DOC),
        md("""**결과 읽기** — 라벨 줄 `가상 문서:` 아래에 검색에 넣을 글 한 덩이가 있습니다.
출력 줄 `모델이 보낸 줄 수` 뒤의 수는 하나일 때도 둘일 때도 있습니다.
어느 쪽이든 이어 붙인 뒤 글은 하나입니다.

## 9. 가상 문서로 검색하기

이번에는 질문이 아니라 방금 지은 글을 검색에 넣습니다.
글의 길이와 문체가 자료의 문서와 더 가깝습니다."""),
        code(HYDE_SEARCH),
        md("""**결과 읽기** — 순위 표의 첫 자리는 `LIB-004`입니다.
출력 줄 `가상 문서로 검색했을 때 정답 문서의 자리: 1`로 정답 문서가 맨 앞에 왔습니다.
같은 문서가 원 질문에서는 넷째 자리였습니다.

가상 문서에는 전자책과 이용 기간 같은 말이 들어 있습니다.
그래서 전자책 이용을 적은 문서와 가까워졌습니다.
순위 표의 거리 값은 새 커널로 다시 실행하면 달라집니다.
모델이 쓴 문장이 바뀌면 거리도 함께 바뀌기 때문입니다."""),
        code(EVIDENCE),
        md("""**결과 읽기** — 출력 줄 `근거 문서 목록: ['FAC-003', 'LIB-004']`가 이 절이 얻으려던 값입니다.
앞의 문서는 원 질문이 찾은 문서이고 정답 문서가 아닙니다.
뒤의 문서는 가상 문서가 찾은 정답 문서입니다.

목록에 담긴 것은 자료에 있는 실제 문서의 ID입니다.
모델이 지어낸 글은 이 목록에 들어가지 않습니다.

## 10. 값 바꿔 보기 · 여러 문서에 걸치는 질문

바꿀 값은 검색에 넣을 원 질문 하나입니다.
머리글도 문장 수도 그대로 두고 질문만 바꿉니다.
정답 문서도 앞과 같은 문서로 둡니다.
실행 전에 예상해 봅니다.
권수를 묻는 말은 일반 도서 쪽에도 걸려 다른 문서가 앞설 것입니다."""),
        code(SECOND_PICK),
        md("""**결과 읽기** — 출력 줄 `바꾼 질문` 뒤에 권수를 묻는 짧은 물음이 있습니다.
출력 줄 `정답 문서는 앞과 같은 ID: LIB-004`로 좇는 문서는 그대로입니다.
출력 줄 `바꾼 질문으로 한 번 검색했을 때 정답 문서의 자리: 3`으로 셋째였습니다.

다음 셀은 같은 머리글로 이 질문의 가상 문서도 지어 봅니다."""),
        code(SECOND_CALL),
        md("""**결과 읽기** — 라벨 줄 `가상 문서:` 아래에 모델이 지은 안내문이 있습니다.
이번 실행에서 이 글에는 전자책이라는 말이 없고 대출과 반납만 적혀 있습니다.
질문에 전자책이라는 말이 없어 모델이 일반 안내를 적었습니다.

다음 셀은 그 글로 같은 방법으로 검색합니다."""),
        code(SECOND_SEARCH),
        md("""**결과 읽기** — 출력 줄 `가상 문서 첫 자리 문서: LIB-001`은 정답 문서가 아닙니다.
출력 줄 `근거 문서 목록: ['LIB-001']`로 근거 문서가 하나입니다.
두 검색이 같은 문서를 첫 자리에 두어 목록에 하나만 남았습니다.

출력 줄 `가상 문서로 검색했을 때 정답 문서의 자리` 뒤의 수는 실행마다 달라집니다.
두 실행에서 모두 앞 세 자리 밖이었습니다.
한 번 검색에서는 셋째 자리였으므로 가상 문서가 정답 문서를 뒤로 밀었습니다.
지어낸 글이 다른 문서 쪽으로 기울면 이런 일이 생깁니다.

## 11. 네 실행을 기록 한 줄씩으로

실행 하나를 기록 한 줄로 만들어 담아 둡니다.
Ch 9~13과 01·02·04절에서 쓴 기록 한 줄과 같은 모양입니다.
칸 이름 하나만 「검색에 넣은 글」로 바꿨습니다.
이 절은 질문이 아닌 글도 검색에 넣기 때문입니다."""),
        code(RUN_ROW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
담는 칸은 실행 이름과 검색에 넣은 글과 첫 자리 문서와 정답 자리 넷입니다.
이 절이 견주는 값이 그 넷이기 때문입니다.

다음 셀은 네 실행의 기록을 표로 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 `실행 | 첫 자리 문서 | 정답 자리` 아래에 실행마다 두 줄씩 나옵니다.
첫 줄은 `원 질문 한 번 검색 | FAC-003 | 4`입니다.
둘째 실행은 `가상 문서로 검색 | LIB-004 | 1`입니다.
셋째 실행은 `바꾼 질문 한 번 검색 | LIB-001 | 3`입니다.

넷째 실행의 정답 자리는 새 커널로 다시 실행하면 달라집니다.
두 실행에서 모두 앞 세 자리 밖이었습니다.

## 정리

1. 짧게 적은 원 질문으로 한 번 검색하니 정답 문서가 넷째 자리였습니다.
2. 같은 질문으로 가상 문서를 지어 검색하니 정답 문서가 첫 자리로 왔습니다.
3. 두 검색의 첫 자리 문서를 모으니 근거 문서 목록에 문서 둘이 담겼습니다.
4. 질문을 바꾼 자리에서는 가상 문서가 정답 문서를 앞 세 자리 밖으로 밀었습니다.

06절에서는 첫 검색의 첫 자리 거리가 기준값보다 클 때만 한 번 더 검색합니다.
이 절은 검색에 넣을 글을 바꿨고 06절은 검색 뒤 결과를 보고 다시 검색할지 정합니다."""),
    ]


SRC_HTML = """<!--meta: 강의 1h | 실습 2h | 코드 notebooks/05-HyDE.ipynb | 새 용어 1 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>질문에 답할 법한 글을 모델에게 지어 받아 검색에 넣을 수 있습니다.</li>
<li>질문으로 검색할 때와 지어낸 글로 검색할 때 정답 문서의 자리를 견줄 수 있습니다.</li>
<li>지어낸 글이 정답 문서를 뒤로 미는 경우가 있다는 것을 같은 코드로 확인할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>사람이 묻는 말은 짧습니다. 「폰으로 보는 건 며칠이에요」에는 자료가 쓰는 낱말이 거의 없습니다. 자료의 문서는 안내문 문장으로 길게 적혀 있습니다. 짧은 물음과 긴 안내문은 생김새부터 다릅니다.</p><p>Ch 9의 기본 RAG는 검색 한 번과 답 한 번이었습니다. 01절부터 04절까지는 검색 앞에서 질문을 질문으로 바꿨습니다. 재작성과 늘리기와 좁히기와 넓히기가 모두 그 자리였습니다. 이 절은 처음으로 질문이 아닌 글을 검색에 넣습니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>04절은 한 사례의 세부가 담긴 질문을 한 단계 넓혔습니다. 넓힌 것도 여전히 질문이었습니다. 이 절은 같은 자리에서 답처럼 보이는 글을 지어 넣습니다. 문서 열두 건과 질문 여덟 개는 Ch 12 core 벌 사본 그대로입니다.</p><p>거리 순위 함수와 순위 표 출력 함수는 Ch 12 01절과 05절에서 배웠습니다. 문서 ID를 모으는 함수와 자리를 세는 함수는 Ch 11 01절에서 배웠습니다. 01~04절처럼 이 넷을 도구 파일 <code>notebooks/rag_tools.py</code>에서 가져옵니다. 벡터의 숫자 개수 설정 <code>256</code>과 답 모델도 이어 씁니다.</p><p>모델이 보낸 글을 줄로 나누는 함수와 검색 한 번을 묶은 함수는 02절에서 만들었고 같은 도구 파일에서 가져옵니다. 04절은 그 가운데 맨 앞 한 줄만 썼습니다. 이 절은 두 문장을 모두 쓰므로 줄을 이어 붙이는 함수를 하나 더 만듭니다. 순위 합치기 함수는 04절에 이어 이 절도 쓰지 않습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>나무판에 물결 모양 구멍이 하나 있다고 생각해 봅니다. 구멍을 말로 설명하는 것보다 그 모양대로 얇은 종이를 오려 두는 편이 빠릅니다. 종이는 구멍을 막는 물건이 아니라 모양을 알려 주는 본입니다. 본과 같은 모양의 진짜 판을 찾아 끼우면 자리가 채워집니다.</p>
{{img:05-5-본뜬-판과-진짜-판|흰 바탕에 나무판 두 장이 나란히 놓여 있고 왼쪽 판에는 물결 모양 구멍이 비어 있으며 그 옆에 같은 물결 모양으로 오린 흰 종이 한 장이 판 위에 납작하게 놓여 있고 오른쪽 판에는 같은 물결 모양의 두꺼운 나무 판 한 장이 구멍 안에 꼭 맞게 들어가 있는 그림|같은 모양으로 오린 얇은 본이 구멍 모양을 알려 주고 그 모양에 맞는 진짜 판이 자리를 채웁니다.}}
<p class="look"><b>그림 읽기</b> — 나무판 두 장이 나란히 놓여 있습니다. 둘 다 같은 물결 모양 구멍이 하나씩 있습니다. 왼쪽 판의 구멍은 비어 있고 그 옆에 같은 모양으로 오린 흰 종이가 있습니다. 오른쪽 판에는 같은 모양의 두꺼운 나무 판이 구멍 안에 들어가 있습니다. 종이는 모양을 알려 주는 본이고 자리를 채우는 것은 나무 판입니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>가상 문서</td><td>질문에 답할 법한 글을 모델에게 지어 받은 것입니다. 검색에 넣을 글로만 쓰고 답의 출처로는 쓰지 않습니다.</td></tr></tbody></table>
<p>아래 다섯 말은 Ch 11·Ch 12와 02·03·04절에서 쓰던 뜻 그대로 이어 씁니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>변형 질문</td><td>원 질문과 같은 것을 묻되 표현을 달리해 만든 검색 질문입니다(02절).</td></tr><tr><td>하위 질문</td><td>한 질문에 섞인 사실을 하나씩만 묻도록 나눈 검색 질문입니다(03절).</td></tr><tr><td>넓힌 질문</td><td>한 사례의 세부를 빼고 일반 규칙만 묻도록 만든 검색 질문입니다(04절).</td></tr><tr><td>근거 문서 목록</td><td>검색마다 첫 자리 문서를 하나씩 모으고 겹치는 문서를 뺀 목록입니다(03절).</td></tr><tr><td>정답 문서 ID</td><td>그 물음에 답할 내용이 적힌 문서의 ID입니다(Ch 11 01절).</td></tr></tbody></table>
{{mermaid:05-1-질문-대신-가상-문서로-검색하기|위에서 아래로 놓인 상자 여섯으로 맨 위에 초록 상자 일상 말로 짧게 적은 원 질문이 있고 그 아래 파란 상자 우리가 적은 안내문 머리글과 보라 상자 답 모델 gpt-5.4-mini를 지나 노란 상자 가상 문서 두 문장으로 이어지며 그 아래 파란 상자 가상 문서로 거리 검색을 거쳐 맨 아래 노란 상자 정답 문서 LIB-004가 첫 자리로 이어지는 그림|질문 대신 답처럼 보이는 글을 지어 검색에 넣으면 문체가 비슷한 문서가 앞으로 옵니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자가 사람이 적은 질문입니다. 파란 상자 둘은 우리가 적은 글과 처리이고 보라 상자가 이번에 부른 모델입니다. 노란 상자 둘은 출력으로 확인한 값입니다.</p>
<h3>질문 바꾸기와 문서 지어내기</h3><p>02절 변형 질문과 03절 하위 질문과 04절 넓힌 질문은 모두 질문이었습니다. 바꾼 것은 묻는 범위였고 모양은 그대로였습니다. 이 절은 모양을 바꿉니다. 검색에 넣는 글이 물음표가 없는 안내문입니다.</p>
{{mermaid:05-2-질문-바꾸기와-문서-지어내기|위에서 아래로 놓인 상자 다섯으로 맨 위 초록 상자 원 질문 하나에서 아래로 갈라져 회색 상자 질문을 질문으로 바꾸기와 파란 상자 답처럼 보이는 글 지어내기 둘이 나란히 놓이고 파란 상자 아래에 노란 상자 가상 문서 두 문장과 노란 상자 정답 문서 LIB-004가 첫 자리가 차례로 이어지는 그림|앞 네 절은 질문을 질문으로 바꿨고 이 절은 질문을 문서 모양으로 바꿉니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자가 사람이 적은 원 질문입니다. 가운데 두 상자가 검색에 넣을 글을 만드는 두 갈래입니다. 회색은 01절부터 04절까지 본 갈래이고 이 노트북에서 실행하지 않았습니다. 파란 상자와 그 아래 노란 상자 둘만 이번에 실행한 자리입니다.</p>
<h3>지어낸 글은 출처가 아닙니다</h3><p>가상 문서는 모델이 지어낸 글입니다. 자료에서 확인한 사실이 아니라 검색에 넣으려고 만든 중간 값입니다. 답의 근거로는 찾은 문서의 ID와 원문만 씁니다. 노트북의 근거 문서 목록에도 실제 문서의 ID만 담습니다.</p>
<h3>지어낸 숫자를 막아 둡니다</h3><p>머리글에 지어낸 숫자를 넣지 말라는 줄을 두었습니다. 숫자를 지어내게 두면 그 숫자가 실행마다 달라집니다. 달라진 숫자는 검색 결과와 정답 자리까지 흔듭니다. 답에 쓸 수 없는 값을 굳이 만들 까닭도 없습니다.</p>
<h3>문장 수를 값으로 적어 둡니다</h3><p>가상 문서 하나마다 모델 요청과 임베딩 요청이 한 번씩 늘어납니다. 문장 수는 코드에 값으로 적고 머리글도 그 값으로 만듭니다. 값 하나를 바꾸면 머리글과 실제로 받는 문장 수가 함께 바뀝니다.</p>
<h3>다른 상황에 적용</h3><p>사내 규정 문의에도 같은 자리가 있습니다. 「출장비 언제까지 올려요」는 규정 문서와 낱말이 겹치지 않습니다. 「경비 청구 기한은 정산 규정에 따릅니다」 같은 안내문을 지어 넣으면 문체가 가까워집니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 문서 열두 건을 벡터로 바꾼 뒤 질문 둘을 각각 두 갈래로 검색합니다. 서비스 요청은 일곱 번이고 임베딩 다섯 번과 답 모델 두 번입니다. 예상 비용은 미화 0.01달러 아래입니다. 새로 쓰는 파일은 없습니다.</p><p>먼저 일상 말로 짧게 적은 원 질문을 손으로 적습니다. 그 질문을 한 번만 검색해 정답 문서의 자리를 셉니다. 그다음 같은 질문에 답할 법한 안내문을 지어 그 글로 검색합니다. 두 검색의 첫 자리 문서를 모아 근거 문서 목록을 만듭니다. 마지막으로 질문을 바꾸어 같은 일을 다시 합니다.</p>
{{mermaid:05-3-두-검색의-첫-자리-문서를-모으기|위에서 아래로 놓인 상자 일곱으로 맨 위에 초록 상자 원 질문과 노란 상자 가상 문서 둘이 나란히 있고 그 아래 파란 상자 글마다 거리 검색을 지나 노란 상자 첫 자리 문서 FAC-003과 노란 상자 첫 자리 문서 LIB-004 둘로 갈라졌다가 파란 상자 겹치는 문서 빼기로 다시 모여 맨 아래 노란 상자 근거 문서 목록에 문서 둘로 이어지는 그림|두 검색의 첫 자리 문서를 하나씩 모으고 겹치는 문서를 빼면 근거 문서 목록이 됩니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 왼쪽 초록 상자가 사람이 적은 질문이고 오른쪽 노란 상자가 모델이 지은 글입니다. 파란 상자 둘은 우리가 적은 처리입니다. 노란 상자 넷은 노트북 8절과 9절이 출력한 값입니다.</p>
{{notebook:05-HyDE}}
<p class="look"><b>확인할 점</b> — 원 질문으로 한 번 검색한 출력 줄은 <code>원 질문으로 검색했을 때 정답 문서의 자리: 4</code>였습니다. 가상 문서로 검색한 뒤에는 <code>가상 문서로 검색했을 때 정답 문서의 자리: 1</code>이 나왔습니다. 두 검색의 첫 자리 문서를 모은 자리에서는 <code>근거 문서 목록: ['FAC-003', 'LIB-004']</code>였습니다. 질문을 바꾼 자리에서는 <code>근거 문서 목록: ['LIB-001']</code>였습니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>일상 말로 짧게 적은 원 질문을 한 번만 검색했습니다. 앞 세 자리는 <code>FAC-003</code>과 <code>ACC-001</code>과 <code>FAC-002</code>였습니다. 세 문서 모두 이 물음의 정답 문서가 아닙니다. 정답 문서 <code>LIB-004</code>는 넷째 자리였습니다.</p><p>짧은 물음에는 전자책이라는 말도 이용 기간이라는 말도 없습니다. 그래서 낱말이 겹치는 문서가 앞자리를 차지했습니다.</p><p>같은 질문에 답할 법한 안내문을 지어 그 글로 다시 검색했습니다. 가상 문서 검색의 첫 자리는 <code>LIB-004</code>였습니다. 정답 문서가 넷째 자리에서 첫 자리로 왔습니다. 지어낸 글에는 전자책과 이용 기간 같은 말이 들어 있었습니다.</p>
{{mermaid:05-4-원-질문-검색과-가상-문서-검색|왼쪽부터 오른쪽으로 놓인 칸 두 개와 회색 상자 하나로 왼쪽 칸 제목은 원 질문으로 한 번 검색이고 그 안에 초록 상자 검색에 넣은 원 질문과 노란 상자 첫 자리 문서 FAC-003과 노란 상자 정답 문서 LIB-004는 자리 넷이 있으며 가운데 칸 제목은 가상 문서로 검색이고 그 안에 노란 상자 검색에 넣은 가상 문서와 노란 상자 첫 자리 문서 LIB-004와 노란 상자 정답 문서는 자리 하나가 있고 오른쪽에 회색 상자 두 검색 모두 같은 문서 열두 건에서 고름이 놓인 그림|원 질문으로 검색하면 정답 문서가 자리 넷이고 가상 문서로 검색하면 첫 자리로 옵니다.}}
<p class="look"><b>도식 읽기</b> — 왼쪽 칸이 원 질문으로 한 번 검색한 자리입니다. 가운데 칸이 가상 문서로 검색한 자리입니다. 왼쪽 칸 맨 위 초록 상자는 사람이 적은 질문이고 가운데 칸 맨 위 노란 상자는 모델이 지은 글입니다. 칸마다 아래 노란 상자 둘이 나온 값입니다. 오른쪽 회색 상자는 두 칸에 모두 해당하는 사실입니다.</p>
<p>두 검색의 첫 자리 문서를 모아 근거 문서 목록을 만들었습니다. 목록에는 문서 둘이 담겼습니다. 앞의 문서는 원 질문이 찾은 <code>FAC-003</code>이고 정답 문서가 아닙니다. 목록에 담긴 것은 모두 자료에 있는 실제 문서의 ID입니다. 모델이 지어낸 글은 목록에 들어가지 않습니다.</p><p>질문을 바꾸면 결과가 달랐습니다. 권수를 묻는 짧은 물음은 한 번 검색에서 정답 문서가 셋째 자리였습니다. 이번 실행에서 같은 머리글로 지은 가상 문서에는 전자책이라는 말이 없고 대출과 반납만 적혀 있었습니다. 그 글로 검색하니 첫 자리가 <code>LIB-001</code>이 되고 정답 문서는 앞 세 자리 밖으로 밀렸습니다.</p><p>근거 문서 목록에는 <code>LIB-001</code> 하나만 남았습니다. 두 검색이 같은 문서를 첫 자리에 두었기 때문입니다. 지어낸 글이 다른 문서 쪽으로 기울면 자리가 뒤로 갈 수 있습니다. 가상 문서를 넣는다고 늘 앞으로 오지는 않습니다.</p><p>여기서 본 것은 질문 두 개입니다. 여덟 질문 모두에서 같은 차이가 나는지는 이번에 확인하지 않았습니다. 여러 질문으로 검색 품질을 재는 일은 Ch 11과 Ch 12 몫입니다. 답이 맞는지 판정하는 일은 Ch 15 몫입니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>자료의 여덟 질문은 저마다 문서와 낱말이 겹칩니다. 그래서 일상 말로 짧게 적은 질문을 손으로 적었고 그 질문의 정답 문서도 손으로 골랐습니다.</li><li>어느 물음을 쓸지는 탐색 실행으로 정했습니다. 한 번 검색으로 정답 문서가 앞 세 자리 밖으로 밀리는 물음을 골랐습니다.</li><li>값 바꿔 보기에 쓴 질문도 흐름을 보여 주려고 고른 예입니다. 정답 문서는 그대로 두고 묻는 말만 바꿨습니다.</li><li>권수를 적은 문서가 자료에 둘이라 이 물음은 문서 하나로 갈리지 않습니다. 정답 문서는 앞 갈래와 같은 <code>LIB-004</code>로 두었습니다.</li><li>정답 문서는 01절부터 04절까지 좇지 않은 문서로 골랐습니다. 절마다 다른 문서를 좇아야 결과를 나란히 놓고 보기 좋습니다.</li><li>가상 문서는 모델이 지은 글이라 실행마다 문장이 달라질 수 있습니다. 그 문장에 <code>assert</code>를 걸지 않았습니다.</li><li>머리글에 지어낸 숫자를 넣지 말라는 줄을 두었습니다. 숫자를 지어내게 둔 머리글에서는 같은 질문에서도 정답 자리가 갈렸습니다.</li><li>새 커널로 두 번 실행하니 스물두 셀 가운데 열여섯 셀의 출력이 글자까지 같았습니다. 달라진 여섯은 모델이 지은 글과 거기서 이어지는 셀입니다.</li><li>정답 자리 셋과 첫 자리 문서 넷은 두 실행에서 같았습니다. 결론은 그 값만 씁니다.</li><li>바꾼 질문의 가상 문서 검색에서는 정답 자리가 두 실행에서 달랐습니다. 본문에는 앞 세 자리 밖이라는 사실과 첫 자리 문서만 적었습니다.</li><li>거리 값은 호출마다 달라집니다. 본문과 그림에는 자리 번호와 문서 ID만 적었습니다.</li><li>가상 문서 하나를 지으면 모델 요청 한 번과 임베딩 요청 한 번이 늘어납니다. 이 절은 걸린 시간을 재지 않았으므로 빨라졌는지 느려졌는지 적지 않습니다.</li><li>지어낸 글은 검색에 넣으려고 만든 중간 값입니다. 답의 출처로는 찾은 문서의 ID와 원문만 씁니다.</li><li>모델이 두 문장을 한 줄로 보낼 때도 있고 두 줄로 보낼 때도 있습니다. 앞 줄만 쓰면 둘째 문장이 사라져 줄을 모두 이어 붙였습니다.</li><li>이 절은 목록을 하나로 합치지 않습니다. 02절과 03절이 쓴 순위 합치기 함수 둘은 04절에 이어 이 절에도 없습니다.</li><li>이 절은 파일을 쓰지 않습니다. 문서 파일과 질문 파일은 읽기만 합니다.</li><li>준비물에 LangChain 1.4.0과 langchain-openai 1.6.1과 numpy 2.5.3을 적었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>짧게 적은 원 질문으로 한 번 검색하니 정답 문서가 넷째 자리였습니다.</li><li>같은 질문으로 가상 문서를 지어 검색하니 정답 문서가 첫 자리로 왔습니다.</li><li>두 검색의 첫 자리 문서를 모으니 근거 문서 목록에 문서 둘이 담겼습니다.</li><li>질문을 바꾼 자리에서는 가상 문서가 정답 문서를 앞 세 자리 밖으로 밀었습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 06절에서는 첫 검색의 첫 자리 거리가 기준값보다 클 때만 한 번 더 검색합니다. 이 절은 검색에 넣을 글을 바꿨고 06절은 검색 뒤 결과를 보고 다시 검색할지 정합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 가상 문서의 입력과 출력은 무엇입니까?</p><p class="quiz-a">짧게 적은 질문 하나를 넣으면 답처럼 보이는 안내문 두 문장이 나옵니다. 틀렸다면 「핵심 개념」의 용어 표를 다시 읽습니다.</p><p class="quiz-q">2. 넓힌 질문과 가상 문서는 무엇이 다릅니까?</p><p class="quiz-a">넓힌 질문은 여전히 질문이고 가상 문서는 물음표가 없는 안내문입니다. 틀렸다면 「핵심 개념」의 소제목 「질문 바꾸기와 문서 지어내기」를 다시 읽습니다.</p><p class="quiz-q">3. 원 질문 검색과 가상 문서 검색에서 정답 문서의 자리는 각각 몇이었습니까?</p><p class="quiz-a">원 질문에서는 넷째 자리였고 가상 문서에서는 첫 자리였습니다. 지어낸 글에 자료와 같은 낱말이 들어와 가까워졌기 때문입니다. 틀렸다면 「실험 결과 해석」의 도식을 다시 읽습니다.</p><p class="quiz-q">4. 모델이 지어낸 글을 답의 출처로 쓰면 안 되는 까닭은 무엇입니까?</p><p class="quiz-a">그 글은 자료에서 확인한 사실이 아니라 검색에 넣으려고 만든 중간 값입니다. 답의 출처로는 찾은 문서의 ID와 원문만 씁니다. 틀렸다면 「핵심 개념」의 소제목 「지어낸 글은 출처가 아닙니다」를 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://arxiv.org/abs/2212.10496">Precise Zero-Shot Dense Retrieval without Relevance Labels 논문</a></div>확인 2026-09-19 · 질문 대신 지어낸 글로 검색하는 방법의 출처.</li><li><div><a href="https://docs.langchain.com/oss/python/concepts/providers-and-models">LangChain 모델과 provider</a></div>확인 2026-09-19 · LangChain 1.4 기준 · 가상 문서를 짓는 모델을 준비하는 방법.</li><li><div><a href="https://developers.openai.com/api/docs/models/text-embedding-3-small">OpenAI text-embedding-3-small 모델 안내</a></div>확인 2026-09-19 · 문서와 글을 벡터로 바꿀 때 쓴 모델과 차원 수 설정.</li><li>Ch 14 04절 Step back — 질문을 질문으로 바꾸는 마지막 자리와 견주어 볼 곳.</li><li>Ch 12 05절 dense와 sparse 비교 — 이 절이 이어 쓴 거리 순위 부품과 출력 함수가 있는 자리.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(SRC_HTML, encoding="utf-8")
    return SRC


if __name__ == "__main__":
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "05", "05-HyDE", "experiment", cells())
        print("wrote", path)
