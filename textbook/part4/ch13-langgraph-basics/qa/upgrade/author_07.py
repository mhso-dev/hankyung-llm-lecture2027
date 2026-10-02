"""Ch 13 07절 품질 개선본 노트북 생성기 (QUALITY-UPGRADE.md §2·§3·§6·§7-2).

사용: python3 author_07.py → labs/part4/ch13-langgraph-basics/notebooks/07-RAG-통합과-시각화.ipynb 를 새로 쓴다.
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북은 qa/upgrade/before/notebooks/ 에 있다. **experiment 형식 유지**(chapter.json).

## 01~06절에서 그대로 이어받은 것 (qa/upgrade/handoff.md 「§06 → §07」)

- 02절이 정한 규칙 `Annotated[list[str], operator.add]`와 「규칙을 적은 칸에는 노드가 자기 몫만 낸다」.
- 출력 함수 `print_state(label, state)`(그 절 칸 수에 맞춤), 기록 함수 `run_row(...)`, 처음 상태 함수 `new_state(...)`.
- 용어 「칸」·「갱신」·「실행 흔적」·「노드」·「엣지」·「상태 그래프」·「컴파일」(01절), 「리듀서」·「이어 붙이기」(02절).
- 「조각」은 Ch 5 토큰 뜻 전용, 한정어 없는 「청크」 금지 → 「문서 청크」(Ch 12 요약 §9).
- 「분기」 대신 「갈래」, 「경로」 대신 「길」, 「반환」 대신 「내놓다」. 게이트 금지어 「돌려줍니다」·「돌려 보」·「재 보」.

## Ch 12에서 가져온 함수 (§2-7 리팩터 2026-09-21 — 도구 파일 `notebooks/rag_tools.py`)

준비 셀(import 셀)에서 여섯 개를 가져온다. 본문은 Ch 12 도구 파일과 같고 벡터 계산은 NumPy다.
`kiwi_terms(kiwi, text, keep_tags)`(Ch 12 04절), `fuse_rank(ranking_list, weight_list, rank_constant)`(06절),
`unique_chunk_ids(hit_list)`·`parent_ids_of(found_chunk_ids, parent_by_chunk)`(07절),
문서 청크 판 `rank_chunks_by_distance(question_vector, chunk_vectors, chunk_ids, top_count)`·
`rank_chunks_by_bm25(bm25_model, question_terms, chunk_ids, top_count)`(Ch 12 07~13절이 쓴 판).
리팩터 전에는 준비 셀 일곱 개에 Ch 12 함수 열한 개(반복문 판 점곱·길이 포함)를 다시 정의했고,
`kiwi_terms(text)`·`rank_by_distance(question_vector, top_count)`·`rank_by_bm25(question, top_count)`처럼
바깥 이름을 읽는 판이었다. 5절은 문서 청크 짝 셀과 인자 설명만 남겨 절 번호를 지켰다.
값도 같다: `keep_tags` 아홉 개 · `rank_constant` 60 · `candidate_count` 8 ·
`report_place` 5 · `context_count` 3. 「1차 검색 = 두 순위를 `fuse_rank()`로 합친 앞 여덟 개」(Ch 12 07~13절 공통).

## 선택한 것과 까닭

1. **상태 형식 이름 `RagState`.** 옛 07절 `RAGState`를 01~06절 이름 모양(`FlowState`·`DecisionState`)에 맞췄다.
   칸은 여덟이다(`question`·`weights`·`distance_ids`·`word_ids`·`candidate_ids`·`picked_ids`·`answer`·`trace`).
2. **노드는 다섯, 고정 엣지는 여섯.** `search_distance`·`search_words`·`fuse`·`pick_report`·`make_reply`.
   갈래도 `Send`도 `Command`도 쓰지 않는다. 이 절은 부품을 한 줄기로 잇는 자리다.
3. **노드 `normalize`를 넣지 않았다.** 질문이 Ch 12 `Q002`라 앞뒤 빈칸이 없다(handoff 2항). 그 사실을 b3에 적었다.
4. **리랭커를 쓰지 않는다.** 기기 메모리가 3.8GB이고 `BAAI/bge-reranker-v2-m3`는 최대 RSS 약 3.1GB다.
   Ch 12 12·13절이 고른 설정도 `reranker: null`이다(contracts §7, Ch 12 요약 §6). b7에 적었다.
5. **PDF를 다시 읽지 않는다.** Ch 12 기록의 `settings.input`이 `advanced-documents.json chunk text`이고
   `context_selection`이 `matched-chunk-text`다. 옛 07절은 `pypdf`로 PDF 여섯 건을 다시 읽어 쪽 단위 문서 청크를
   따로 만들었는데, 그러면 Ch 12 문서 청크 ID와 다른 값이 생긴다. 이 절은 Ch 12 문서 청크 175개를 그대로 쓴다.
6. **노트북은 `numpy`·`sklearn`을 부르지 않는다.** 벡터 계산은 도구 파일 안에서 NumPy로 한다
   (규격 §2-7, 설치 셀에 `numpy==2.5.3` — 실습 폴더 잠금과 같은 판).
7. **값 바꿔 보기는 가중치 한 자리.** 실행 1은 `[1.0, 1.0]`, 실행 2는 `[1.0, 0.0]`이다. 설정을 상태의 칸에
   담았으므로 같은 그래프를 그대로 두고 넣는 값만 바꾼다.
8. **파일을 쓰지 않는다.** 옛 07절은 `runs/graph-integrated-result.json`을 다시 썼다. Part 3 실습 절 넷 선례대로
   기록을 쓰지 않는 쪽이 안전하고(contracts §3 마지막 줄), 이 절이 가르치는 것은 그래프 조립이다.
   옛 파일은 지우지 않고 그대로 둔다(묶음 허용 목록이 그 파일을 담고 있음).
9. **모델 답에 `assert`를 걸지 않는다**(규격 §3). `assert`는 경로 확인 한 곳뿐이다.
10. **쓰지 않은 것**: `lambda`·내포식·조건 표현식·f-string·`key=`·`reverse=`·`Literal`·세미콜론·
    한 줄 복합문·클래스 상속·`enumerate`·`zip`·`set`·`next`. 부른 내장 이름은 `len`·`print`·`open`·`range`·
    `round`·`str`·`sorted`·`type`뿐이다.

## 탐색 실행에서 확인한 값 (2026-09-19, /tmp/ch13-07/probe1.py~probe3.py)

langgraph 1.2.11 · langchain 1.4.0 · langchain-openai 1.6.1 · kiwipiepy 0.23.2 · rank-bm25 0.2.2 · Python 3.12.13.
부모 문서 6건 · 문서 청크 175개 · 질문 `Q002` · 정답 부모 `['E01']`.
앞 기록이 넣은 문서 청크는 `E01-P03-C02`·`E01-P03-C01`·`E01-P03-C06` 셋이고 리랭커 설정은 `None`이다.
실행 1 보고 자리 다섯은 모두 `E01`이고 부모 차례는 `['E01']`, 답에 7권과 14일이 있었다.
실행 2 보고 자리 다섯 가운데 셋이 `E02`로 바뀌고 부모 차례는 `['E01', 'E02']`, 답은 자료에서 찾지 못했다고 했다.
구조 문자열의 화살표 줄은 여섯이고 줄 차례는 실행 차례와 다르다.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import KEY, RUN_DATE, code, install_source, md, model_source, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part4/ch13-langgraph-basics/notebooks"

INSTALL = install_source([
    "langgraph==1.2.11", "langchain==1.4.0", "langchain-openai==1.6.1",
    "python-dotenv==1.2.3", "kiwipiepy==0.23.2", "rank-bm25==0.2.2", "numpy==2.5.3",
])

IMPORTS = r'''# 자료 읽기·경로 확인과 그래프 이름과 Ch 12 검색 도구를 불러옵니다
import json
import operator
import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from kiwipiepy import Kiwi
from rank_bm25 import BM25Okapi
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model
# Ch 12 04·06·07절 함수와 순위 함수의 문서 청크 판을 도구 파일에서 가져옵니다
from rag_tools import fuse_rank, kiwi_terms, parent_ids_of, rank_chunks_by_bm25
from rag_tools import rank_chunks_by_distance, unique_chunk_ids

print("이 챕터에서 처음 부르는 이름:", "OpenAIEmbeddings", "BM25Okapi", "Kiwi")'''

ROOT_PATH = r'''# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part3/ch12-retrieval-tuning/data"):
        root_path = candidate
        break
print("고른 경로:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

LOAD_DATA = r'''# Ch 12가 남긴 문서 파일과 통합 기록 파일을 읽습니다(읽기만 하고 고치지 않습니다)
chapter12_path = root_path + "/labs/part3/ch12-retrieval-tuning"
with open(chapter12_path + "/data/advanced-documents.json", encoding="utf-8") as file:
    documents = json.loads(file.read())
with open(chapter12_path + "/runs/advanced-continuity-integrated-result.json", encoding="utf-8") as file:
    prior_record = json.loads(file.read())
parents = documents["parents"]
chunks = documents["chunks"]
print("부모 문서 수:", len(parents))
print("문서 청크 수:", len(chunks))'''

PRIOR = r'''# 통합 기록에서 이 절이 쓸 질문과 정답 부모 문서 ID와 앞 실행 설정을 꺼냅니다
question = prior_record["question"]
gold_doc_ids = prior_record["gold_doc_ids"]
prior_chunk_ids = []
for item in prior_record["retrieved"]:
    prior_chunk_ids.append(item["chunk_id"])
print("질문 번호:", prior_record["qid"])
print("질문:", question)
print("정답 부모 문서 ID:", gold_doc_ids)
print("앞 기록이 넣은 문서 청크:", prior_chunk_ids)
print("앞 기록의 리랭커 설정:", prior_record["settings"]["reranker"])
print("앞 기록이 넣은 것:", prior_record["settings"]["context_selection"])'''

VALUES = r'''# Ch 12 04~08절에서 쓴 값을 그대로 다시 정하고 이번에 바꿔 볼 가중치 두 벌을 적습니다
keep_tags = ["NNG", "NNP", "NNB", "NR", "VV", "VA", "MAG", "SN", "SL"]
rank_constant = 60
candidate_count = 8
report_place = 5
context_count = 3
equal_weights = [1.0, 1.0]
distance_only_weights = [1.0, 0.0]
prompt_head = "아래 자료만 보고 질문에 한국어로 답하세요.\n"
prompt_head = prompt_head + "답 끝에 [문서ID p.쪽] 모양으로 출처를 적으세요.\n\n"
print("순위 상수:", rank_constant, "| 후보 수:", candidate_count, "| 보고 자리:", report_place)
print("모델에 넣을 자리 수:", context_count)
print("실행 1 가중치:", equal_weights, "| 실행 2 가중치:", distance_only_weights)'''

CHUNK_PREP = r'''# 문서 청크마다 제목과 본문을 이어 붙이고 ID로 부모와 쪽과 본문을 찾을 짝을 만듭니다
chunk_texts = []
chunk_ids = []
parent_by_chunk = {}
page_by_chunk = {}
text_by_chunk = {}
for chunk in chunks:
    chunk_text = chunk["title"] + " " + chunk["text"]
    chunk_texts.append(chunk_text)
    chunk_ids.append(chunk["chunk_id"])
    parent_by_chunk[chunk["chunk_id"]] = chunk["parent_id"]
    page_by_chunk[chunk["chunk_id"]] = chunk["page"]
    text_by_chunk[chunk["chunk_id"]] = chunk_text
all_chunk_count = len(chunk_ids)
print("이어 붙인 글 수:", all_chunk_count)'''

BM25_MODEL = r'''# 형태소 분석기를 만들고 문서 청크마다 검색 낱말 목록을 만들어 BM25 모델을 만듭니다
kiwi = Kiwi()
kiwi_corpus = []
for text_value in chunk_texts:
    kiwi_corpus.append(kiwi_terms(kiwi, text_value, keep_tags))
bm25_model = BM25Okapi(kiwi_corpus)
print("검색 낱말 목록 수:", len(kiwi_corpus))
print("BM25 모델이 본 문서 청크 수:", bm25_model.corpus_size)'''

EMBEDDINGS = r'''# Ch 12와 같은 모델로 문서 청크를 벡터로 바꿉니다(임베딩 요청 1번)
embedding_model_name = "text-embedding-3-small"
vector_dimensions = 256
embedding_model = OpenAIEmbeddings(model=embedding_model_name, dimensions=vector_dimensions)
chunk_vectors = embedding_model.embed_documents(chunk_texts)
print("임베딩 모델 이름:", embedding_model.model)
print("벡터의 숫자 개수 설정:", embedding_model.dimensions)
print("문서 청크 벡터 수:", len(chunk_vectors))'''

RAG_STATE = r'''# 이 절 그래프가 쓸 상태 형식을 칸 여덟 개로 적습니다
class RagState(TypedDict):
    question: str
    weights: list[float]
    distance_ids: list[str]
    word_ids: list[str]
    candidate_ids: list[str]
    picked_ids: list[str]
    answer: str
    trace: Annotated[list[str], operator.add]'''

PRINT_STATE = r'''# 상태의 칸 여덟 개를 라벨 줄 아래에 적고 여러 줄로 나오는 값은 개수만 적습니다
def print_state(label, state):
    print(label)
    print("질문 칸 |", state["question"])
    print("가중치 칸 |", state["weights"])
    print("거리 순위 칸의 문서 청크 수 |", len(state["distance_ids"]))
    print("낱말 순위 칸의 문서 청크 수 |", len(state["word_ids"]))
    print("후보 칸 |", state["candidate_ids"])
    print("보고 자리 칸 |", state["picked_ids"])
    print("답 칸의 글자 수 |", len(state["answer"]))
    print("실행 흔적 칸 |", state["trace"])'''

NEW_STATE = r'''# 가중치 칸만 다른 처음 상태를 만들어 냅니다
def new_state(weight_list):
    state = {"question": question, "weights": weight_list}
    state["distance_ids"] = []
    state["word_ids"] = []
    state["candidate_ids"] = []
    state["picked_ids"] = []
    state["answer"] = ""
    state["trace"] = []
    return state'''

SEARCH_DISTANCE = r'''# 질문을 벡터로 바꿔 거리가 가까운 차례로 문서 청크 ID 목록을 냅니다(임베딩 요청 1번)
def search_distance(state):
    question_vector = embedding_model.embed_query(state["question"])
    hit_list = rank_chunks_by_distance(question_vector, chunk_vectors, chunk_ids, all_chunk_count)
    return {"distance_ids": unique_chunk_ids(hit_list), "trace": ["search_distance"]}'''

SEARCH_WORDS = r'''# 질문의 검색 낱말로 겹침 점수가 큰 차례로 문서 청크 ID 목록을 냅니다
def search_words(state):
    question_terms = kiwi_terms(kiwi, state["question"], keep_tags)
    hit_list = rank_chunks_by_bm25(bm25_model, question_terms, chunk_ids, all_chunk_count)
    return {"word_ids": unique_chunk_ids(hit_list), "trace": ["search_words"]}'''

FUSE_NODE = r'''# 두 순위 목록을 가중치 칸대로 합쳐 앞자리 여덟 개를 후보로 남깁니다
def fuse(state):
    ranking_list = [state["distance_ids"], state["word_ids"]]
    fused_ids = fuse_rank(ranking_list, state["weights"], rank_constant)
    return {"candidate_ids": fused_ids[:candidate_count], "trace": ["fuse"]}'''

PICK_REPORT = r'''# 후보 앞에서 보고 자리 다섯 개만 남깁니다
def pick_report(state):
    picked_ids = state["candidate_ids"][:report_place]
    return {"picked_ids": picked_ids, "trace": ["pick_report"]}'''

MAKE_REPLY = r'''# 보고 자리 앞 세 개의 본문과 출처 표시를 넣어 모델에게 답을 받습니다(모델 요청 1번)
def make_reply(state):
    context_text = ""
    for chunk_id in state["picked_ids"][:context_count]:
        source_label = "[" + parent_by_chunk[chunk_id] + " p." + str(page_by_chunk[chunk_id]) + "]"
        context_text = context_text + source_label + "\n" + text_by_chunk[chunk_id] + "\n\n"
    prompt_text = prompt_head + "질문: " + state["question"] + "\n\n자료:\n" + context_text
    reply = model.invoke(prompt_text)
    return {"answer": reply.text.strip(), "trace": ["make_reply"]}'''

BUILD_NODES = r'''# 설계 객체를 만들고 노드 다섯 개를 등록합니다
builder = StateGraph(RagState)
builder.add_node("search_distance", search_distance)
builder.add_node("search_words", search_words)
builder.add_node("fuse", fuse)
builder.add_node("pick_report", pick_report)
builder.add_node("make_reply", make_reply)
print("등록한 노드 수:", len(builder.nodes))'''

BUILD_EDGES = r'''# 고정 엣지 여섯 개로 노드 다섯을 한 줄기로 잇고 컴파일합니다
builder.add_edge(START, "search_distance")
builder.add_edge("search_distance", "search_words")
builder.add_edge("search_words", "fuse")
builder.add_edge("fuse", "pick_report")
builder.add_edge("pick_report", "make_reply")
builder.add_edge("make_reply", END)
graph = builder.compile()
print("고정 엣지로 적은 수:", len(builder.edges))
print("컴파일 결과의 종류:", type(graph))'''

STRUCTURE = r'''# 그래프가 스스로 그린 구조 문자열에서 화살표가 있는 줄만 골라 출력합니다
structure_text = graph.get_graph().draw_mermaid()
print("구조 문자열에서 화살표가 있는 줄")
for line in structure_text.split("\n"):
    if "-->" in line:
        print(line.strip())'''

RUN_ONE = r'''# 가중치 두 개가 모두 1.0인 설정을 넣고 그래프를 실행합니다(임베딩 1번·모델 1번)
run1_state = new_state(equal_weights)
run1_result = graph.invoke(run1_state)
print_state("실행 1 결과", run1_result)
run1_parents = parent_ids_of(run1_result["picked_ids"], parent_by_chunk)
print("보고 자리의 부모 문서 차례:", run1_parents)
print("실행 1의 답:")
print(run1_result["answer"])'''

RUN_TWO = r'''# 가중치 한 자리만 0.0으로 바꿔 같은 그래프를 다시 실행합니다(임베딩 1번·모델 1번)
run2_state = new_state(distance_only_weights)
run2_result = graph.invoke(run2_state)
print_state("실행 2 결과", run2_result)
run2_parents = parent_ids_of(run2_result["picked_ids"], parent_by_chunk)
print("보고 자리의 부모 문서 차례:", run2_parents)
print("실행 2의 답:")
print(run2_result["answer"])'''

RUN_ROW = r'''# 실행 한 번을 기록 한 줄로 만듭니다
def run_row(run_name, state, parent_ids):
    row = {"실행": run_name}
    row["가중치"] = state["weights"]
    row["부모 문서 차례"] = parent_ids
    row["보고 자리 수"] = len(state["picked_ids"])
    row["답의 글자 수"] = len(state["answer"])
    return row'''

TABLE = r'''# 두 실행의 기록을 담아 라벨 줄 아래에 한 줄씩 출력합니다
run_rows = []
run_rows.append(run_row("실행 1", run1_result, run1_parents))
run_rows.append(run_row("실행 2", run2_result, run2_parents))
print("실행 | 가중치 | 부모 문서 차례 | 보고 자리 수 | 답의 글자 수")
for row in run_rows:
    print(row["실행"], "|", row["가중치"], "|", row["부모 문서 차례"], "|", row["보고 자리 수"], "|", row["답의 글자 수"])
print("두 실행의 보고 자리 칸이 같은가:", run1_result["picked_ids"] == run2_result["picked_ids"])
print("두 실행의 실행 흔적 칸이 같은가:", run1_result["trace"] == run2_result["trace"])'''

TITLE = """# Ch 12 검색을 그래프로 잇기

**이 노트북에서 할 일**

1. Ch 12가 남긴 문서 청크와 통합 기록에서 질문 하나를 가져옵니다.
2. 거리 검색과 낱말 검색과 순위 합치기와 답 쓰기를 노드 다섯으로 나눠 잇습니다.
3. 그래프가 그린 구조와 실행 흔적 칸을 견줍니다.
4. 가중치 한 자리만 바꿔 다시 실행하고 두 결과를 나란히 봅니다.

**준비물** — 이 절은 프로젝트 맨 위 폴더의 `.env`에 적어 둔 `OPENAI_API_KEY`를 씁니다.
서비스 요청은 다섯 번입니다(임베딩 세 번과 답을 쓰는 모델 두 번).
예상 비용은 미화 0.01달러 아래입니다.
읽어 오는 파일은 Ch 12 파일 두 개이고 새로 쓰는 파일은 없습니다.
실행 시간은 2분 안팎이고 첫 셀의 설치가 가장 오래 걸립니다.

**기준 버전** — 첫 셀에서 LangGraph 1.2.11과 LangChain 1.4.0을 설치합니다.
Ch 12 임베딩에 쓰는 langchain-openai 1.6.1과 도구 파일이 쓰는 numpy 2.5.3도 설치합니다.
낱말 검색에 쓰는 kiwipiepy 0.23.2와 rank-bm25 0.2.2도 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3~8절을 읽습니다.
Ch 12 자료를 읽고 검색 재료를 만든 뒤 노드 다섯을 만들어 붙이는 자리입니다.
9절과 10절은 같은 그래프에 넣는 값 하나만 바꿔 보는 자리입니다.
11절은 두 실행을 기록 한 줄씩으로 만들어 표로 견주는 자리입니다.
준비부터 끝까지 함께 실행하고 실습 시간에 다시 읽습니다.

실습 폴더 `labs/part4/ch13-langgraph-basics`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""

FIGURE_ALT = ("위에서 아래로 놓인 상자 일곱으로 맨 위 회색 상자 가상 시작점 START에서 화살표가 파란 상자 "
              "노드 search_distance 거리 순위 칸으로 이어지고 차례로 파란 상자 노드 search_words 낱말 순위 칸과 "
              "파란 상자 노드 fuse 후보 칸과 파란 상자 노드 pick_report 보고 자리 칸과 파란 상자 노드 "
              "make_reply 답 칸을 지나 맨 아래 회색 상자 가상 끝점 END로 이어지는 그림")

FIGURE_READ = """맨 위 회색 상자가 입력이 들어오는 자리입니다.
그 아래 파란 상자 다섯이 이 절에서 만들 노드입니다.
상자마다 그 노드가 채우는 칸 이름이 함께 적혀 있습니다.
맨 아래 회색 상자에서 한 줄기가 끝납니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIGURE_ALT + "](attachment:07-1-부품-다섯을-한-줄기로.png)\n\n" + FIGURE_READ, html="skip"),
        md("""## 1. 준비

첫 셀은 패키지 일곱 개를 설치하고 설치된 판 번호를 출력합니다.
01~06절보다 설치가 길어 몇 분이 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 판 번호 일곱 줄이 보입니다.
마지막 줄 `numpy: 2.5.3`은 도구 파일이 벡터 계산에 쓰는 패키지입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이름 열두 개를 불러오고 도구 파일에서 함수 여섯 개를 가져옵니다.
그래프 이름 여섯은 01~06절에서 쓴 것과 같습니다.
나머지 여섯은 파일과 경로를 다루는 둘과 Ch 6~12에서 쓴 모델·검색 도구 넷입니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.

이 노트북은 Ch 12 함수 여섯 개를 가져옵니다.
04절 `kiwi_terms()`, 06절 `fuse_rank()`, 07절 `unique_chunk_ids()`·`parent_ids_of()`입니다.
거리 순위와 낱말 순위는 Ch 12 07~13절이 쓴 문서 청크 판 두 개를 가져옵니다.
인자 모양은 5절에서 설명합니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄에 이 챕터에서 처음 부르는 이름 셋이 보입니다.
임베딩을 만드는 `OpenAIEmbeddings`와 낱말 겹침 점수를 내는 `BM25Okapi`와 형태소 분석기 `Kiwi`입니다.
셋 다 Ch 12에서 쓴 것과 같은 이름입니다.
도구 파일에서 가져온 함수 여섯 개는 출력하지 않습니다.

## 2. 키와 모델 준비

API 키가 있는지 확인합니다.
`True` 값이 나오면 다음으로 넘어갑니다."""),
        setup(KEY),
        md("""답을 쓸 모델을 준비합니다.
temperature 값을 0으로 두어 매번 비슷한 답을 고르게 합니다."""),
        code(model_source("openai:gpt-5.4-mini")),
        md("""**결과 읽기** — 출력 줄 `모델 이름: gpt-5.4-mini`와 `temperature: 0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.
temperature 값이 0이어도 답 문장이 매번 같다고 보장하지 않습니다.

## 3. Ch 12 자료 읽기

이 절은 Ch 12가 만든 문서 청크와 통합 기록을 읽습니다.
두 파일 모두 읽기만 하고 고치지 않습니다.
먼저 노트북을 연 자리에서 프로젝트 맨 위를 찾습니다."""),
        code(ROOT_PATH),
        md("""**결과 읽기** — 출력 줄 `고른 경로` 뒤에 점 하나나 위로 올라가는 경로가 보입니다.
Ch 10~12에서 쓴 경로 찾기와 같은 코드입니다.
후보 셋 가운데 Ch 12 자료 폴더가 있는 자리를 고릅니다.

다음 셀은 Ch 12 파일 두 개를 읽습니다."""),
        code(LOAD_DATA),
        md("""**결과 읽기** — 출력 줄 `부모 문서 수: 6`과 `문서 청크 수: 175`가 Ch 12 advanced 벌 그대로입니다.
Ch 12 07~13절이 쓴 자료와 같은 파일입니다.
문서 청크 ID는 부모 문서 ID와 쪽 번호와 차례 번호를 이은 모양입니다.

다음 셀은 통합 기록에서 이 절이 쓸 값을 꺼냅니다."""),
        code(PRIOR),
        md("""**결과 읽기** — 출력 줄 `질문 번호: Q002`가 이 절이 쓸 질문 하나입니다.
출력 줄 `정답 부모 문서 ID: ['E01']`이 그 질문의 정답 부모 문서입니다.
출력 줄의 `앞 기록이 넣은 문서 청크: ['E01-P03-C02', 'E01-P03-C01', 'E01-P03-C06']`은 세 건 모두 부모가 `E01`입니다.
출력 줄 `앞 기록의 리랭커 설정: None`은 Ch 12가 리랭커를 쓰지 않았다는 뜻입니다.
출력 줄 `앞 기록이 넣은 것: matched-chunk-text`는 모델에 넣은 것이 쪽이 아니라 문서 청크 본문이라는 뜻입니다.

이 절은 저장된 답을 쓰지 않습니다.
질문과 정답 부모 문서 ID만 가져오고 검색부터 답까지 다시 실행합니다.

## 4. 이 절에서 쓸 값 정하기

Ch 12 04~08절에서 정한 값을 그대로 다시 적습니다.
같은 값을 써야 Ch 12 결과와 이 절 결과를 견줄 수 있습니다.
마지막 두 줄이 이번에 바꿔 볼 가중치 두 벌입니다."""),
        code(VALUES),
        md("""**결과 읽기** — 출력 줄 `순위 상수: 60`은 Ch 12 06절에서 정한 값입니다.
같은 줄의 후보 수 8과 보고 자리 5도 Ch 12 07·08절 값입니다.
출력 줄 `모델에 넣을 자리 수: 3`은 보고 자리 앞에서 모델에 넣을 문서 청크 수입니다.
출력 줄의 `실행 1 가중치: [1.0, 1.0]`은 두 순위를 같은 몫으로 합친다는 뜻입니다.
같은 줄의 `실행 2 가중치: [1.0, 0.0]`은 낱말 순위 몫을 0으로 둔다는 뜻입니다.

## 5. 문서 청크 짝과 가져온 함수의 인자

다음 셀은 문서 청크마다 제목과 본문을 이어 붙입니다.
문서 청크 ID로 부모 문서와 쪽과 본문을 찾을 짝도 함께 만듭니다."""),
        code(CHUNK_PREP, lesson_role="setup"),
        md("""**결과 읽기** — 출력 줄 `이어 붙인 글 수: 175`가 문서 청크 수와 같습니다.
짝 셋은 문서 청크 ID로 부모 문서 ID와 쪽 번호와 이어 붙인 글을 찾습니다.

준비 셀에서 가져온 함수는 Ch 12 도구 파일과 같은 판입니다.
노트북에서 만든 값은 함수 안에서 읽지 않고 인자로 넘깁니다.
함수 `kiwi_terms()`는 형태소 분석기, 글, 남길 품사 표시 목록을 받습니다.
함수 `rank_chunks_by_distance()`는 질문 벡터, 문서 청크 벡터 목록, 문서 청크 ID 목록, 남길 개수를 받습니다.
함수 `rank_chunks_by_bm25()`는 BM25 모델, 질문의 검색 낱말 목록, 문서 청크 ID 목록, 남길 개수를 받습니다.

두 순위 함수는 Ch 12 01·04절 순위 함수를 문서 청크에 쓰는 판이고 계산은 같습니다.
함수 `fuse_rank()`는 순위 상수를 셋째 인자로, `parent_ids_of()`는 방금 만든 짝 `parent_by_chunk`를 둘째 인자로 받습니다.

다음 셀은 형태소 분석기를 만들고 문서 청크마다 검색 낱말 목록을 만듭니다.
그 목록으로 낱말 겹침 점수를 낼 BM25 모델을 만듭니다."""),
        code(BM25_MODEL),
        md("""**결과 읽기** — 출력 줄 `BM25 모델이 본 문서 청크 수: 175`가 문서 청크 수와 같습니다.
문서 청크 하나마다 검색 낱말 목록 하나를 만들었습니다.
이 셀은 서비스 요청을 보내지 않습니다.

다음 셀은 문서 청크를 벡터로 바꿉니다.
이 절에서 서비스에 보내는 첫 요청입니다."""),
        code(EMBEDDINGS),
        md("""**결과 읽기** — 출력 줄 `임베딩 모델 이름: text-embedding-3-small`은 Ch 9~12가 쓴 모델과 같습니다.
출력 줄 `벡터의 숫자 개수 설정: 256`도 Ch 10~12와 같은 값입니다.
출력 줄 `문서 청크 벡터 수: 175`로 문서 청크마다 벡터 하나를 받았습니다.
벡터 안의 숫자는 호출마다 아주 조금씩 달라져 소수 자리까지 같다고 보지 않습니다.

## 6. 상태 형식과 출력 함수

이 절 상태에는 검색 중간 결과를 담을 칸이 여럿 필요합니다.
칸 구성이 01~06절과 달라 형식 이름도 새로 붙입니다.
실행 흔적 칸에는 02절에서 쓴 규칙을 그대로 적습니다."""),
        code(RAG_STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 `weights`가 이 절에서 바꿔 볼 설정 자리입니다.
칸 `distance_ids`와 `word_ids`는 검색 두 가지가 각각 채웁니다.
칸 `trace`에만 규칙을 적었고 나머지 일곱 칸은 덮어쓰기가 됩니다.

다음 셀은 01절부터 쓴 출력 함수를 이 절 칸에 맞춘 판입니다."""),
        code(PRINT_STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
순위 두 칸은 문서 청크 175개가 들어 있어 값 대신 개수만 적습니다.
답 칸도 여러 줄로 나올 수 있어 글자 수만 적고 따로 출력합니다.
후보 칸과 보고 자리 칸은 한 줄로 나와 값을 그대로 적습니다.

다음 셀은 가중치만 바꿔 처음 상태를 만드는 함수입니다."""),
        code(NEW_STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
질문 칸에는 Ch 12 기록에서 꺼낸 질문을 넣습니다.
나머지 칸은 빈 목록과 빈 글로 두고 노드가 채우게 합니다.
03절과 06절에서 쓴 처음 상태 함수와 같은 모양입니다.

## 7. 노드 다섯 만들기

부품 하나를 노드 하나로 옮깁니다.
노드마다 자기가 채울 칸과 실행 흔적 칸에 자기 이름만 담아 냅니다.
02절이 정한 약속을 다섯 노드가 모두 지킵니다.
첫 노드는 질문을 벡터로 바꿔 거리 순위를 만듭니다."""),
        code(SEARCH_DISTANCE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 노드 안에서 질문 하나를 벡터로 바꾸는 요청이 한 번 나갑니다.
가져온 함수 `rank_chunks_by_distance()`로 문서 청크 175개 모두의 차례를 매깁니다.
받은 순위 목록에서 문서 청크 ID만 뽑아 칸에 담습니다.

다음 노드는 낱말 겹침 점수로 순위를 만듭니다."""),
        code(SEARCH_WORDS),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 노드는 서비스 요청을 보내지 않습니다.
질문의 검색 낱말은 노드 안에서 `kiwi_terms()`로 만듭니다.
그 낱말로 5절에서 만든 BM25 모델이 점수를 냅니다.
두 노드가 서로 다른 칸에 담으므로 값이 섞이지 않습니다.

다음 노드는 두 순위를 가중치대로 합칩니다."""),
        code(FUSE_NODE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
합칠 때 쓰는 가중치를 상태의 칸에서 읽습니다.
그래서 그래프를 다시 만들지 않고 넣는 값만 바꿀 수 있습니다.
Ch 12 07~13절 약속대로 앞자리 여덟 개까지만 후보로 남깁니다.

다음 노드는 후보에서 보고 자리만 남깁니다."""),
        code(PICK_REPORT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
Ch 12 08절에서 정한 보고 자리 다섯 개를 그대로 씁니다.
자르는 자리를 노드 하나로 떼어 두면 그 자리만 바꿔 보기 좋습니다.

마지막 노드가 모델에게 답을 받습니다."""),
        code(MAKE_REPLY),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
보고 자리 앞 세 개의 본문과 출처 표시를 이어 붙여 넣습니다.
넣는 것은 쪽 전체가 아니라 문서 청크 본문입니다.
이 노드 안에서 답을 쓰는 요청이 한 번 나갑니다.

## 8. 조립과 구조 확인

설계 객체를 만들고 노드 다섯을 등록합니다.
이 절에는 갈래가 없어 조건 함수도 `Send`도 `Command`도 쓰지 않습니다."""),
        code(BUILD_NODES),
        md("""**결과 읽기** — 출력 줄 `등록한 노드 수: 5`가 보입니다.
01·02절은 둘, 03·06절은 넷, 04절은 셋, 05절은 둘이었습니다.
이 절이 이 챕터에서 노드가 가장 많은 그래프입니다.

다음 셀은 고정 엣지만 적고 컴파일합니다."""),
        code(BUILD_EDGES),
        md("""**결과 읽기** — 출력 줄 `고정 엣지로 적은 수: 6`이 보입니다.
노드 다섯을 한 줄기로 이으면 가상 시작점과 가상 끝점까지 엣지가 여섯입니다.
출력 줄의 종류 이름 `CompiledStateGraph`는 01절부터 같습니다.

다음 셀은 그래프가 스스로 그린 구조 문자열을 봅니다.
줄이 많아 화살표가 있는 줄만 골라 출력합니다."""),
        code(STRUCTURE),
        md("""**결과 읽기** — 라벨 줄 아래 여섯 줄이 나옵니다.
줄 `__start__ --> search_distance;`가 가상 시작점에서 첫 노드로 가는 엣지입니다.
줄 `make_reply --> __end__;`가 마지막 노드에서 가상 끝점으로 가는 엣지입니다.
여섯 줄이 모두 있지만 줄이 나온 차례는 실행 차례가 아닙니다.
실제로 지난 차례는 아래 실행의 실행 흔적 칸에서 봅니다.

## 9. 실행 1 · 두 몫을 같게

실행 전에 예상해 봅니다.
낱말 순위가 정답 문서 청크를 앞에 두므로 보고 자리가 `E01`로 채워질 것입니다.
그러면 답에 대출 권수와 기간이 들어갈 것입니다."""),
        code(RUN_ONE),
        md("""**결과 읽기** — 줄 `거리 순위 칸의 문서 청크 수 | 175`와 낱말 순위 칸 줄이 같은 수입니다.
줄 `실행 흔적 칸 | ['search_distance', 'search_words', 'fuse', 'pick_report', 'make_reply']`에 이름이 다섯 남았습니다.
출력 줄 `보고 자리의 부모 문서 차례: ['E01']`로 보고 자리 다섯이 모두 한 부모에서 왔습니다.
라벨 줄 `실행 1의 답:` 아래에 모델이 쓴 답과 출처 표시가 있습니다.
답에는 대출 권수와 기간이 들어 있고 끝에 출처 표시가 붙었습니다.

## 10. 값 바꿔 보기 · 낱말 순위 몫을 0으로

바꿀 값은 가중치 한 자리입니다.
그래프도 노드도 그대로 두고 상태의 가중치 칸만 바꿉니다.
실행 전에 예상해 봅니다.
낱말 순위 몫이 사라지면 거리 순위만 남아 보고 자리가 달라질 것입니다."""),
        code(RUN_TWO),
        md("""**결과 읽기** — 줄 `실행 흔적 칸 | ['search_distance', 'search_words', 'fuse', 'pick_report', 'make_reply']`은 실행 1과 같습니다.
지나간 노드는 같고 노드가 쓴 값만 달라졌습니다.
출력 줄 `보고 자리의 부모 문서 차례: ['E01', 'E02']`로 다른 부모 문서가 섞였습니다.
라벨 줄 `실행 2의 답:` 아래 답은 자료에서 찾지 못했다는 뜻입니다.
넣은 문서 청크가 달라지자 답도 달라졌습니다.

## 11. 두 실행을 기록 한 줄씩으로

실행 하나를 기록 한 줄로 만들어 담아 둡니다.
Ch 9~12와 01~06절에서 쓴 기록 한 줄과 같은 모양입니다."""),
        code(RUN_ROW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
06절 판과 견주면 담는 칸에 가중치와 부모 문서 차례가 들어왔습니다.
이 절이 견주는 값이 그 둘이기 때문입니다.

다음 셀은 두 실행의 기록을 표로 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄이 나옵니다.
두 줄의 보고 자리 수는 같고 가중치와 부모 문서 차례가 갈렸습니다.
출력 줄 `두 실행의 보고 자리 칸이 같은가: False`가 갈린 자리입니다.
출력 줄 `두 실행의 실행 흔적 칸이 같은가: True`는 같은 그래프를 지났다는 뜻입니다.

## 정리

1. Ch 12 검색 부품을 노드 다섯으로 나눠 고정 엣지 여섯으로 이었습니다.
2. 그래프가 그린 구조의 여섯 줄과 실행 흔적 칸의 이름 다섯이 서로 맞았습니다.
3. 설정을 상태의 칸에 담아 두어 같은 그래프에 값 하나만 바꿔 다시 실행했습니다.

08절은 이 챕터의 실습입니다.
이 절에서 만든 검색 노드에 06절 이동과 04절 메시지 칸을 함께 붙입니다."""),
    ]


if __name__ == "__main__":
    path = write_notebook(LAB, "07", "07-RAG-통합과-시각화", "experiment", cells())
    print("wrote", path)
