"""Ch 21 05절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 author_05.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_05.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**(chapter.json).

## 결정 1 — Ch 9~14에서 배운 임베딩 검색을 도구로 감싼다 (챕터 리드 결정)

자료는 Ch 14 `documents.json`(12건)·`queries.json`(8건)을 읽기만 한다(보호 파일). 임베딩은 Ch 14 06절 설정
`OpenAIEmbeddings(model="text-embedding-3-small", dimensions=256)` 그대로, 문서 글은 Ch 12·14의 「제목 + 빈칸 + 본문」.
Ch 14 실습 폴더에 저장된 문서 임베딩 파일이 없어(05-probe.md §0-1) 문서 벡터는 노트북 안에서 한 번 만들고 파일로 쓰지 않는다.
검색 함수는 Ch 14 도구 파일 `rag_tools.py`의 `search_hits`·`rank_by_distance`·`cosine_distance`·`cosine_similarity`·`print_ranked`를
본문 글자 그대로 `runner_tools.py`로 옮겼다(check_same_as_before()가 AST·글자 대조). NumPy import는 도구 파일에만.

## 결정 2 — 검색 도구의 이름·인자·내놓는 모양 (06절이 그대로 쓸 수 있게)

`@tool def search_documents(query: str)` — 몸통은 `search_hits(embedding_model, query, doc_vectors, doc_ids, top_count)` 한 번
(임베딩 요청 1번)과 「[문서 ID] 제목 본문」 줄 `top_count`(=3)개. 거리는 도구 메시지에 넣지 않는다(끝자리 흔들림이 글에 들어가지 않게).

## 결정 3 — 흔들림 먼저 확인 (qa/upgrade/05-probe.md)

노트북 밖에서 S5(C05)·SP(주차) 다섯 번씩. 메시지 모양·응답마다 요청 수·검색어·문서 ID·입력 토큰이 10/10 같았다.
assert는 도구 메시지마다 문서 줄 수(top_count — 도구 몸통이 정함)와 호출 ID 짝(코드가 옮김)에만 건다.
같은 검색어 다시 부르기(15/15 같은 글)는 출력만 하고 assert하지 않는다(임베딩 서비스 값에 기대므로).
시스템 메시지 글의 「한 번만 더 검색」은 모델에게 적은 규칙이고 코드 제한이 아니다(그래프에 세는 줄 없음, create_agent에 한도 인자 없음).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`sorted`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·튜플 풀기·세미콜론·
`isinstance`·별표 풀기·`try`·클래스 정의·`draw_mermaid_png`·`stream`·`perf_counter`·`as_retriever`·벡터스토어.
"""
from __future__ import annotations

import ast
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch21-create-agent/notebooks"
FIGS = ROOT / "textbook/part6/ch21-create-agent/figures"
UPGRADE = ROOT / "textbook/part6/ch21-create-agent/qa/upgrade"
CH14 = ROOT / "labs/part4/ch14-rag-patterns"
SLUG = "05-retriever를-도구로-전환"
SRC = ROOT / "textbook/part6/ch21-create-agent/_src" / (SLUG + ".html")
# 교재 출력을 만든 실행의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답)에서 읽은 값
RUNSEC = os.environ.get("AUTHOR05_RUNSEC", "10초 안에")

INSTALL = install_source([
    "langchain==1.4.0", "langchain-core==1.6.2", "langchain-openai==1.6.0", "langgraph==1.2.11", "numpy==2.5.3",
    "python-dotenv==1.2.3",
])

IMPORTS = r'''# 문서 파일을 읽을 이름, 임베딩 모델, 에이전트와 도구를 만드는 이름을 가져옵니다
import json
import os

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_openai import OpenAIEmbeddings

# 앞에서 배운 함수는 도구 파일에서 가져옵니다(search_hits·print_ranked는 이 절부터 가져옵니다)
from runner_tools import agent_row, estimate_cost, print_branches, print_ranked
from runner_tools import search_hits, show_messages, sum_usage

print("이 챕터에서 처음 가져온 이름:", "OpenAIEmbeddings", "search_hits", "print_ranked")'''

# Ch 14 06절 노트북 셀과 글자까지 같은 셀(check_same_as_before()가 대조)
ROOT_FIND = r'''# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part4/ch14-rag-patterns/data"):
        root_path = candidate
        break
print("고른 자리:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

# 코드 줄은 Ch 14 06절 셀과 같고 첫 줄 주석만 다름(check_same_as_before()가 대조)
READ_DATA = r'''# Ch 14 폴더의 문서 파일과 질문 파일을 읽습니다(읽기만 하고 고치지 않습니다)
data_path = root_path + "/labs/part4/ch14-rag-patterns/data"
with open(data_path + "/documents.json", encoding="utf-8") as file:
    docs = json.loads(file.read())
with open(data_path + "/queries.json", encoding="utf-8") as file:
    queries = json.loads(file.read())
print("문서 수:", len(docs))
print("질문 수:", len(queries))'''

DOC_TEXTS = r'''# 문서 12건의 제목과 본문을 이어 붙이고, 문서 ID 목록과 문서 ID로 글을 찾는 딕셔너리를 만듭니다
doc_texts = []
doc_ids = []
text_by_doc = {}
for doc in docs:
    # Ch 12·14와 같은 「제목 + 빈칸 + 본문」 모양입니다
    doc_text = doc["title"] + " " + doc["text"]
    doc_texts.append(doc_text)
    doc_ids.append(doc["doc_id"])
    text_by_doc[doc["doc_id"]] = doc_text
print("문서 ID 목록:")
print(doc_ids)'''

PICK = r'''# 질문 파일에서 C05 질문과 그 정답 문서 ID를 고르고, 정답 문서의 글을 봅니다
c05_question = ""
gold_doc_id = ""
for query in queries:
    if query["qid"] == "C05":
        c05_question = query["question"]
        gold_doc_id = query["gold_doc_id"]
print("질문:", c05_question)
print("정답 문서 ID:", gold_doc_id)
print("정답 문서의 글:", text_by_doc[gold_doc_id])'''

# 코드 줄은 Ch 14 06절 셀과 같고 첫 줄 주석만 다름(check_same_as_before()가 대조)
EMBED_DOCS = r'''# Ch 14 06절과 같은 임베딩 모델과 벡터 크기로 문서 12건을 벡터로 바꿉니다(임베딩 요청 1번)
embedding_model_name = "text-embedding-3-small"
vector_dimensions = 256
embedding_model = OpenAIEmbeddings(model=embedding_model_name, dimensions=vector_dimensions)
doc_vectors = embedding_model.embed_documents(doc_texts)
print("임베딩 모델 이름:", embedding_model.model)
print("벡터의 숫자 개수 설정:", embedding_model.dimensions)
print("문서 벡터 수:", len(doc_vectors))'''

DIRECT = r'''# Ch 14처럼 질문 글을 그대로 검색 함수에 넣어, 거리가 가까운 문서 세 건을 봅니다(임베딩 요청 1번)
top_count = 3
question_hits = search_hits(embedding_model, c05_question, doc_vectors, doc_ids, top_count)
print("질문 글을 그대로 검색한 순위:")
print_ranked(question_hits, "거리")'''

DEF_SEARCH = r'''# 검색 함수 search_hits를 도구로 감쌉니다(맨 @tool 줄 — Ch 19 01절, 부를 때마다 임베딩 요청 1번)
@tool
def search_documents(query: str):
    """교육센터 자료실 안내 문서 열두 건에서 검색어와 가까운 문서 세 건을 찾습니다. query에는 찾을 내용을 짧은 검색어로 넣습니다."""
    hit_list = search_hits(embedding_model, query, doc_vectors, doc_ids, top_count)
    # 문서마다 [문서 ID]와 글을 한 줄로 이어, 도구 메시지가 될 글을 만듭니다(Ch 14 01절 자료 줄과 같은 모양)
    found_text = ""
    for hit in hit_list:
        doc_id = hit["doc_id"]
        found_text = found_text + "[" + doc_id + "] " + text_by_doc[doc_id] + "\n"
    return found_text'''

SPEC = r'''# 도구 이름, 모델이 채울 인자(입력 형식), 모델 요청에 실릴 도구 명세의 인자를 봅니다(Ch 19 01절)
arg_names = list(search_documents.args.keys())
tool_spec = convert_to_openai_tool(search_documents)
spec_args = tool_spec["function"]["parameters"]["properties"]
spec_names = list(spec_args.keys())
print("도구 이름:", search_documents.name)
print("입력 형식의 인자:", arg_names)
print("명세의 인자:", spec_names)'''

AGENT = r'''# 모델 객체·검색 도구·시스템 메시지 글을 넘겨 에이전트 그래프를 만듭니다(요청은 아직 보내지 않음)
system_text = "교육센터 자료실 안내 도우미입니다. 자료실 이용을 묻는 질문에는 search_documents 도구로 찾은 문서 글에 근거해 답하세요. 찾은 문서에 답이 없으면 검색어를 바꿔 한 번만 더 검색하고, 그래도 없으면 문서에서 찾지 못했다고 답하세요."
agent = create_agent(model, tools=[search_documents], system_prompt=system_text)
print("만든 것의 종류:", type(agent).__name__)'''

SHAPE = r'''# 검색 도구를 넣은 에이전트 그래프의 노드와 조건 함수를 봅니다(02절 함수 print_branches — 도구 파일)
print("등록된 노드:", list(agent.builder.nodes))
print_branches(agent)'''

RUN_C05 = r'''# C05 질문을 에이전트 그래프에 보냅니다(모델 노드마다 모델 요청 1번, 검색 도구마다 임베딩 요청 1번)
c05_state = {"messages": [HumanMessage(content=c05_question)]}
c05_result = agent.invoke(c05_state)
print("메시지 칸의 메시지 수:", len(c05_result["messages"]))
print("메시지 칸:")
show_messages(c05_result["messages"])'''

ARGS_C05 = r'''# 둘째 메시지(첫 응답)에 담긴 검색 도구 호출 요청의 이름과, 모델이 채운 인자(검색어)를 봅니다
c05_first = c05_result["messages"][1]
for call in c05_first.tool_calls:
    print("도구 이름:", call["name"], "| 인자:", call["args"])'''

AGAIN = r'''# 첫 응답의 도구 호출 요청을 도구에 그대로 다시 보내, 같은 검색어면 같은 글이 나오는지 봅니다(임베딩 요청 1번)
first_call = c05_first.tool_calls[0]
again_message = search_documents.invoke(first_call)
c05_tool_message = c05_result["messages"][2]
print("다시 받은 메시지의 종류:", type(again_message).__name__)
print("도구 메시지 글과 같은가:", again_message.content == c05_tool_message.content)'''

ANSWER_C05 = r'''# 메시지 칸의 마지막 응답을 봅니다(도구 호출 요청 수와 답 글)
c05_last = c05_result["messages"][-1]
print("마지막 응답의 도구 호출 요청 수:", len(c05_last.tool_calls))
print("답 글:")
print(c05_last.content)'''

RUN_PARK = r'''# 바꿀 값: 질문 하나만, 문서 12건에 답이 없는 질문으로 바꿔 같은 에이전트 그래프에 보냅니다
parking_question = "자료실 주차 요금은 얼마인가요?"
parking_state = {"messages": [HumanMessage(content=parking_question)]}
parking_result = agent.invoke(parking_state)
print("메시지 칸의 메시지 수:", len(parking_result["messages"]))
print("메시지 칸:")
show_messages(parking_result["messages"])'''

ARGS_PARK = r'''# 응답마다 검색 도구 호출 요청 수와, 모델이 채운 인자(검색어)를 차례로 봅니다
for message in parking_result["messages"]:
    if type(message).__name__ == "AIMessage":
        print("응답 | 도구 호출 요청 수:", len(message.tool_calls))
        for call in message.tool_calls:
            print("  인자:", call["args"])'''

ANSWER_PARK = r'''# 바꾼 질문의 마지막 응답을 봅니다(도구 호출 요청 수와 답 글)
parking_last = parking_result["messages"][-1]
print("마지막 응답의 도구 호출 요청 수:", len(parking_last.tool_calls))
print("답 글:")
print(parking_last.content)'''

DOC_LINES = r'''# 두 결과의 도구 메시지마다, [로 시작하는 줄에서 문서 ID를 꺼내 셉니다
for result in [c05_result, parking_result]:
    for message in result["messages"]:
        if type(message).__name__ == "ToolMessage":
            found_ids = []
            for line in message.content.split("\n"):
                if line.startswith("["):
                    found_ids.append(line.split("]")[0][1:])
            print("도구 메시지의 문서 ID:", found_ids)
            # 줄 수는 도구 몸통이 top_count로 정하는 값이라, 모델이 무엇을 검색해도 같아야 합니다
            assert len(found_ids) == top_count, "도구 메시지마다 문서 줄이 top_count개여야 합니다"'''

TABLE = r'''# 두 질문의 기록을 한 줄씩 적어 출력합니다(01절 10절 함수 agent_row — 도구 파일)
run_rows = []
run_rows.append(agent_row("C05 질문", c05_result))
run_rows.append(agent_row("주차 질문", parking_result))
print("질문 | 모델 요청 수 | 도구 메시지 수 | 호출 ID 짝")
for row in run_rows:
    print(row["질문"], "|", row["모델 요청 수"], "|", row["도구 메시지 수"], "|", row["호출 ID 짝"])
    # 도구 메시지마다 요청 id를 옮겨 적는 것은 코드가 하는 일이라, 짝은 매번 맞아야 합니다
    assert row["호출 ID 짝"], "도구 메시지마다 같은 차례의 요청 id가 옮겨져야 합니다"'''

EMBED_COUNT = r'''# 이 노트북이 보낸 임베딩 요청을 셉니다(도구 메시지 하나 = 도구 안 검색 한 번 = 임베딩 요청 1번)
doc_requests = 1
direct_requests = 2
tool_requests = run_rows[0]["도구 메시지 수"] + run_rows[1]["도구 메시지 수"]
embed_total = doc_requests + direct_requests + tool_requests
print("문서 벡터를 만든 요청:", doc_requests)
print("검색 함수를 직접 부른 요청(4절·7절):", direct_requests)
print("검색 도구 안에서 보낸 요청:", tool_requests)
print("임베딩 요청 합계:", embed_total)'''

USAGE = r'''# 두 결과의 모델 요청 수와 입력·출력 토큰을 더합니다(Ch 19 05절 함수 sum_usage)
c05_usage = sum_usage(c05_result["messages"])
parking_usage = sum_usage(parking_result["messages"])
print("C05 질문 사용량:", c05_usage)
print("주차 질문 사용량:", parking_usage)'''

COST = r'''# 2026-09-17 요금표(100만 토큰당 달러)로 두 결과의 모델 몫 예상 비용을 셉니다(Ch 6 06절 함수 estimate_cost)
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
c05_cost = round(estimate_cost(c05_usage, input_rate, cached_input_rate, output_rate), 6)
parking_cost = round(estimate_cost(parking_usage, input_rate, cached_input_rate, output_rate), 6)
print("C05 질문 예상 비용(달러):", c05_cost)
print("주차 질문 예상 비용(달러):", parking_cost)'''


def string_constants(path: Path) -> dict:
    """생성기 파일에서 글 상수(이름 = r'''…''')를 모읍니다."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            found[node.targets[0].id] = node.value.value
    return found


def code_lines(source: str) -> list:
    return [line for line in source.splitlines() if not line.strip().startswith("#")]


def check_same_as_before() -> None:
    """Ch 14 06절 셀·도구 파일, 01·02절 생성기, 노트북 밖 확인 코드와 대조합니다(본문의 「같은 코드」는 이 대조가 근거)."""
    ch01 = string_constants(UPGRADE / "author_01.py")
    ch02 = string_constants(UPGRADE / "author_02.py")
    nb14 = json.loads((CH14 / "notebooks/06-CRAG.ipynb").read_text(encoding="utf-8"))
    cells14 = []
    for cell in nb14["cells"]:
        if cell["cell_type"] == "code":
            source = cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
            cells14.append(source)
    assert ROOT_FIND in cells14, "자리 찾기 셀이 Ch 14 06절과 다릅니다"
    read14 = [s for s in cells14 if "documents.json" in s][0]
    assert code_lines(READ_DATA) == code_lines(read14), "파일 읽기 셀의 코드 줄이 Ch 14 06절과 다릅니다"
    embed14 = [s for s in cells14 if "embed_documents" in s][0]
    assert code_lines(EMBED_DOCS) == code_lines(embed14), "임베딩 셀의 코드 줄이 Ch 14 06절과 다릅니다"
    # 도구 파일의 검색 함수 다섯은 Ch 14 도구 파일과 본문 글자·AST가 같아야 합니다
    src14 = (CH14 / "notebooks/rag_tools.py").read_text(encoding="utf-8")
    mine = (LAB / "runner_tools.py").read_text(encoding="utf-8")
    trees = {}
    for label, text in [("14", src14), ("21", mine)]:
        lines = text.splitlines()
        for node in ast.parse(text).body:
            if isinstance(node, ast.FunctionDef):
                trees[(label, node.name)] = (ast.dump(node), "\n".join(lines[node.lineno - 1:node.end_lineno]))
    for name in ["cosine_similarity", "cosine_distance", "rank_by_distance", "print_ranked", "search_hits"]:
        assert trees[("21", name)] == trees[("14", name)], name + "가 Ch 14 도구 파일과 다릅니다"
    assert trees[("21", "agent_row")][0] == ast.dump(ast.parse(ch01["DEF_ROW"]).body[0]), "agent_row가 01절과 다릅니다"
    assert trees[("21", "print_branches")][0] == ast.dump(ast.parse(ch02["DEF_BRANCHES"]).body[0]), "print_branches가 02절과 다릅니다"
    # 시스템 메시지 글은 01절 글과 첫 문장이 같습니다
    system01 = [line for line in ch01["AGENT"].splitlines() if line.startswith("system_text = ")][0]
    system05 = [line for line in AGENT.splitlines() if line.startswith("system_text = ")][0]
    assert system01.split(". ")[0] == system05.split(". ")[0], "시스템 메시지 글 첫 문장이 01절과 다릅니다"
    # 노트북 밖 확인(probe05.py)과 시스템 메시지 글·도구 코드가 같아야 합니다
    probe = ast.parse((UPGRADE / "probe/probe05.py").read_text(encoding="utf-8"))
    probe_system = None
    probe_tool = None
    for node in probe.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "SYSTEM_TEXT":
            probe_system = ast.literal_eval(node.value)
        if isinstance(node, ast.FunctionDef) and node.name == "search_documents":
            probe_tool = ast.dump(node)
    assert ast.literal_eval(system05.split(" = ", 1)[1]) == probe_system, "시스템 메시지 글이 노트북 밖 확인과 다릅니다"
    assert ast.dump(ast.parse(DEF_SEARCH).body[0]) == probe_tool, "검색 도구가 노트북 밖 확인과 다릅니다"


FIG1 = "05-1-검색-함수를-도구로-감싼-자리"
FIG1_ALT = os.environ.get("AUTHOR05_FIG1_ALT", "위에서 아래로 한 줄로 이어지는 그림으로 맨 위 초록 상자 Ch 14 문서 열두 건 documents.json 읽기만에서 보라 상자 임베딩 모델 text-embedding-3-small 벡터 크기 256 문서 벡터 열두 개 임베딩 요청 한 번으로 화살표가 갑니다. 이어서 파란 상자 검색 함수 search_hits Ch 14 06절 도구 파일, 파란 상자 검색 도구 search_documents 인자 query 문서 세 건의 글, 회색 상자 create_agent 모델 객체 도구 하나 시스템 메시지 글이 차례로 이어지고, 맨 아래 회색 상자 에이전트 그래프 모델 노드와 도구 실행 노드 01절과 같은 모양으로 끝나는 그림")
FIG1_CAP = "Ch 14 문서 벡터와 검색 함수 search_hits를 도구 search_documents로 감싸 create_agent에 넘겨도, 에이전트 그래프의 모양은 01절과 같습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 Ch 14 문서 파일이고, 보라 상자는 실제로 부른 임베딩 모델입니다.
파란 상자 둘은 우리가 적은 코드로, 검색 함수를 도구로 감싸는 차례입니다.
회색 상자 둘은 라이브러리가 준 함수 create_agent와, 그 함수가 만든 그래프입니다.
노트북 6절 출력으로 01절과 같은 모양임을 확인했습니다."""

FIG2 = "05-2-검색어와-횟수를-정하는-쪽"
FIG2_ALT = os.environ.get("AUTHOR05_FIG2_ALT", "위아래 칸 둘이 있는 그림으로 위 칸 Ch 14 06절 흐름 코드가 정함에는 회색 상자 첫 검색어 질문 글 그대로와 회색 상자 다시 검색할지 첫 자리 거리를 기준값과 견주어 코드가 정함 다시 검색 상한 한 번을 코드로 확인이 위아래로 놓여 있습니다. 아래 칸 이 절 흐름 모델이 고름에는 보라 상자 검색어 모델이 인자 query에 적음, 초록 상자 다시 검색 시스템 메시지 글 한 번만 더 검색 세거나 막는 코드 없음, 노란 상자 C05 질문 검색 한 번 주차 질문 검색 두 번이 위아래로 놓여 있는 그림")
FIG2_CAP = "Ch 14 06절에서는 다시 검색할지와 그 상한을 코드가 정했고, 이 절에서는 검색어와 검색 횟수를 모델이 고릅니다."
FIG2_READ = """위 칸이 Ch 14 06절 흐름, 아래 칸이 이 절 흐름입니다.
위 칸 회색 상자는 다른 챕터 노트북의 코드와 출력입니다.
아래 칸 보라 상자는 실제로 부른 모델이 고르는 자리이고, 초록 상자는 우리가 적은 시스템 메시지 글입니다.
노란 상자는 노트북 7·8절 출력입니다.
두 칸은 나란히 견주는 것이라 화살표로 잇지 않았습니다."""

FIG3 = "05-3-C05-질문의-차례"
FIG3_ALT = os.environ.get("AUTHOR05_FIG3_ALT", "세로선 넷이 있는 차례 그림으로 왼쪽부터 노트북 코드 agent.invoke, 연보라 띠 안의 모델 노드 gpt-5.4-mini, 도구 실행 노드 search_documents, 연보라 띠 안의 임베딩 모델 text-embedding-3-small입니다. 노트북 코드가 모델 노드에 C05 질문 하나를 보내고 노란 메모 요청 1 도구 호출 요청 search_documents 인자 query가 붙습니다. 모델 노드에서 도구 실행 노드로 model_to_tools 화살표가 가고, 도구 실행 노드에서 임베딩 모델로 search_hits 화살표, 임베딩 모델에서 도구 실행 노드로 임베딩 요청 1번 점선이 돌아옵니다. 노란 메모 도구 메시지 success 문서 세 줄 FAC-003 LIB-002 ACC-004가 붙고, 도구 실행 노드에서 모델 노드로 tools_to_model 화살표, 노란 메모 요청 2 도구 호출 요청 0건, 모델 노드에서 노트북 코드로 END 점선이 갑니다. 마지막 노란 메모에 메시지 넷 모델 요청 두 번 임베딩 요청 한 번 호출 ID 짝 True가 적힌 그림")
FIG3_CAP = "C05 질문에서 모델은 검색 도구를 한 번 불렀고, 도구 실행 노드의 검색 한 번에 임베딩 요청이 한 번 나갔습니다."
FIG3_READ = "위에서 아래로 읽고, 세로선은 왼쪽부터 노트북 코드, 모델 노드, 도구 실행 노드, 임베딩 모델입니다. 연보라 띠 둘은 실제로 부른 모델 `gpt-5.4-mini`와 `text-embedding-3-small`이 있는 자리입니다. 노란 메모는 모두 노트북 7절과 9절 출력입니다. 임베딩 요청은 도구 실행 노드 안에서 검색 함수가 보냈고, 모델 노드는 도구 메시지 글만 받았습니다."

FIG4 = "05-4-질문만-바꾼-두-실행"
FIG4_ALT = os.environ.get("AUTHOR05_FIG4_ALT", "맨 위 초록 상자 같은 에이전트 그래프 같은 시스템 메시지 글 바꾼 것은 질문 하나에서 칸 둘로 화살표가 갑니다. 왼쪽 칸 C05 질문 토요일 폐관 시각의 노란 상자에는 검색 한 번 도구 메시지 하나 첫 줄 FAC-003 모델 요청 두 번 입력 토큰 638, 오른쪽 칸 바꾼 값 주차 요금 질문의 노란 상자에는 검색 두 번 다시 검색 한 번 도구 메시지 둘 첫 줄 FAC-002와 FAC-004 모델 요청 세 번 입력 토큰 1189가 적혀 있습니다. 맨 아래 회색 상자에는 두 질문 공통 도구 메시지마다 문서 세 건 응답마다 도구 호출 요청 한 건 이하 호출 ID 짝 True가 적힌 그림")
FIG4_CAP = "질문 하나만 바꾸자 검색은 한 번에서 두 번으로, 모델 요청은 두 번에서 세 번으로 늘었고, 도구 메시지마다 문서는 세 건이었습니다."
FIG4_READ = "맨 위 초록 상자는 두 실행에 같았던 조건입니다. 아래 칸 둘은 왼쪽이 7절 실행, 오른쪽이 8절 값 바꿔 보기입니다. 노란 상자는 노트북 7~9절 출력입니다. 맨 아래 회색 상자는 두 칸 출력에서 모두 확인한 공통점입니다. 칸끼리는 화살표로 잇지 않았습니다."

ILLU = "05-5-세제-통을-꽂아-둔-세탁기"
ILLU_ALT = os.environ.get("AUTHOR05_ILLU_ALT", "옅은 베이지 벽과 바닥이 보이는 방을 그린 그림입니다. 가운데에 흰 앞문형 세탁기 한 대가 크게 서 있고, 앞면 위쪽 띠의 오른쪽에 둥근 버튼 하나, 앞면에 둥근 유리문 하나가 있습니다. 유리문 안에서 빨래와 옅은 파란 거품이 돕니다. 세탁기 윗면 왼쪽의 둥근 구멍에 연녹색 세제 통 한 개가 거꾸로 기울어 꽂혀 있습니다. 세탁기 왼쪽 바닥에는 빈 연녹색 계량컵 한 개가 기계와 떨어져 놓여 있는 그림")
ILLU_CAP = "바닥의 빈 계량컵은 쓰이지 않고, 세제는 세탁기에 꽂아 둔 통에서 세탁기가 끌어 씁니다."
ILLU_READ = os.environ.get("AUTHOR05_ILLU_READ", "가운데에 흰 세탁기 한 대가 있고, 둥근 버튼 하나와 둥근 유리문 하나가 있습니다. 윗면 왼쪽 구멍에는 연녹색 세제 통 한 개가 거꾸로 꽂혀 있고, 유리문 안에는 옅은 파란 거품이 보입니다. 왼쪽 바닥의 빈 계량컵 하나는 기계와 떨어져, 쓰이지 않은 채 놓여 있습니다. 꽂혀 있는 세제 통이 검색 도구로 감싼 검색 함수이고, 세탁기가 필요할 때 끌어 씁니다. 빈 계량컵은 사람이 매번 먼저 붓는 방법, 곧 Ch 14처럼 코드가 검색을 먼저 하는 흐름입니다.")

TITLE = """# retriever를 도구로 전환

**이 노트북에서 할 일**

1. Ch 14 06절 검색 함수 `search_hits`로 질문 하나를 검색해, 거리 순위를 먼저 봅니다.
2. 그 검색 함수를 `@tool` 도구로 감싸 `create_agent`에 넘기고, 모델이 채운 검색어와 도구 메시지를 봅니다.
3. 질문 하나만 문서에 답이 없는 질문으로 바꿔, 모델이 다시 검색하는지 셉니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 교재 출력에서 모델 요청은 모두 5번입니다.
7절에서 2번, 8절에서 3번을 보냈습니다.
임베딩 모델은 `text-embedding-3-small`이고, 임베딩 요청은 모두 6번입니다.

모델이 검색 도구를 부르는 횟수가 달라지면, 모델 요청 수와 임베딩 요청 수가 함께 달라집니다.
요금표로 어림한 예상 비용은 모두 합쳐 0.01달러 아래이고, 청구 금액이 아닙니다.
읽는 파일은 Ch 14 실습 폴더의 `documents.json`과 `queries.json` 둘이고, 읽기만 합니다.
문서 벡터는 이 노트북에서 한 번 만들고, 파일로 쓰지 않습니다.

앞에서 배운 함수 일곱은 도구 파일 `runner_tools.py`에서 가져옵니다.
교재 출력을 만든 실행에서는 노트북 전체가 """ + RUNSEC + """ 끝났습니다.
모델과 임베딩 응답을 기다리는 시간은 네트워크와 실행 때에 따라 달라집니다.

**기준 버전** — 첫 셀에서 패키지 여섯을 설치합니다.
판은 langchain 1.4.0, langchain-core 1.6.2, langchain-openai 1.6.0입니다.
langgraph 1.2.11, numpy 2.5.3, python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3~6절을 읽습니다.
문서와 검색 함수를 준비하고, 검색 함수를 도구로 감싸 에이전트 그래프에 넣는 자리입니다.
7~9절은 질문을 보내고 질문 하나를 바꿔 보는 자리이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch21-create-agent`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

01~04절의 에이전트 그래프는 노트북 안 규정 딕셔너리를 찾는 도구를 썼습니다.
이 절에서는 Ch 14에서 쓴 문서 열두 건과 검색 함수를 가져와, 그 검색을 도구로 바꿉니다.
제목의 retriever는 질문을 받아 가까운 문서를 찾아 주는 검색 부분을 가리키는 영어 말입니다.
이 노트북에서는 Ch 14 06절 검색 함수 `search_hits`가 그 일을 합니다.

첫 셀은 패키지 여섯 개를 설치하고 설치된 판 번호를 출력합니다.
01~04절처럼 numpy도 함께 설치합니다.
이 절부터는 도구 파일의 거리 계산 함수가 NumPy로 벡터를 계산합니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langchain: 1.4.0`·`langchain-core: 1.6.2`·`langchain-openai: 1.6.0`이 보입니다.
출력 줄 `langgraph: 1.2.11`·`numpy: 2.5.3`·`python-dotenv: 1.2.3`도 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
임베딩 모델 `OpenAIEmbeddings`는 Ch 9 01절에서 처음 썼습니다.
함수 `convert_to_openai_tool`은 Ch 19 01절에서 도구 명세를 볼 때 썼습니다.
모듈 `json`과 `os`는 Ch 14에서 문서 파일을 읽고 폴더를 찾을 때 썼습니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `이 챕터에서 처음 가져온 이름: OpenAIEmbeddings search_hits print_ranked`가 보입니다.
Ch 9~14에서 쓴 이름이지만, 이 챕터에서는 처음 가져옵니다.

앞에서 배운 함수는 `runner_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.

함수 `search_hits`는 Ch 14 06절, `print_ranked`는 Ch 12 05절에서 배웠습니다.
함수 `search_hits`가 안에서 부르는 `rank_by_distance`·`cosine_distance`·`cosine_similarity`도 함께 옮겼습니다.
다섯 함수 모두 Ch 14 도구 파일에서 본문을 글자 그대로 옮겼고, 인자 모양도 Ch 14와 같습니다.
거리 계산은 Ch 5 02절처럼 NumPy로 합니다.
나머지 다섯 이름은 01~03절에서 이 도구 파일로 옮긴 함수입니다.

## 2. 키와 모델 준비

모델은 01절과 같은 `gpt-5.4-mini`이고, 과정의 같은 설정으로 부릅니다.
이렇게 만든 모델 객체를 이 절의 에이전트 그래프에 넘깁니다."""),
    ] + key_and_model_cells(
        "openai:gpt-5.4-mini",
        "temperature 값을 0으로 두어도, 모델이 쓰는 답 글과 검색어가 매번 같다고 보장하지는 않습니다.",
    ) + [
        md("""## 3. Ch 14 문서와 질문

05절부터는 Ch 14 실습 폴더의 문서 모음을 씁니다.
Ch 14에서 검색에 쓴 문서 열두 건과 질문 여덟 건입니다.
두 파일이 Ch 14 폴더에 있으므로, 다음 셀은 먼저 프로젝트 맨 위 폴더를 찾습니다.
다음 셀은 Ch 14 06절 셀과 글자까지 같은 코드입니다."""),
        setup(ROOT_FIND),
        md("""**결과 읽기** — 출력 줄 `고른 자리: .`은 교재 출력을 프로젝트 맨 위에서 실행했다는 뜻입니다.
교재 출력은 실행 도구에 도구 파일 폴더를 따로 알려 준 실행이라 `.`이 찍혔습니다.
노트북을 `notebooks/` 폴더에서 열면 이 줄에 `../../../..`가 찍힙니다.

다음 셀은 두 파일을 읽습니다.
코드 줄은 Ch 14 06절과 같고, 첫 줄 주석만 이 절에 맞게 고쳤습니다."""),
        code(READ_DATA),
        md("""**결과 읽기** — 출력 줄 `문서 수: 12`와 `질문 수: 8`로, Ch 14와 같은 자료입니다.
두 파일은 Ch 14 실습 폴더의 파일이라, 이 노트북은 읽기만 합니다.

다음 셀은 Ch 14처럼 문서마다 제목과 본문을 빈칸 하나로 이어 붙입니다.
문서 ID로 그 글을 찾는 딕셔너리 `text_by_doc`도 함께 만듭니다.
5절 검색 도구가 찾은 문서의 글을 이 딕셔너리에서 꺼냅니다."""),
        code(DOC_TEXTS),
        md("""**결과 읽기** — 라벨 줄 `문서 ID 목록:` 아래에 `LIB-001`부터 `ACC-004`까지 열두 개가 보입니다.
Ch 14 06절 출력과 같은 차례입니다.

다음 셀은 질문 파일에서 `C05` 질문을 고릅니다.
질문마다 적힌 정답 문서 ID(Ch 11 01절 말)도 함께 꺼내, 그 문서의 글을 봅니다."""),
        code(PICK),
        md("""**결과 읽기** — 출력 줄 `질문: 토요일 자료실 폐관 시각은?`과 `정답 문서 ID: FAC-003`입니다.
출력 줄 `정답 문서의 글:` 뒤에 운영 시간 문서의 글이 보입니다.
이 문서는 평일 자료실을 오전 9시부터 오후 9시까지 연다고 적습니다.

01절 규정 딕셔너리는 평일 운영을 09:00~20:00으로 적었습니다.
두 글은 서로 다른 자료라, 이 절은 01절 딕셔너리를 쓰지 않고 고치지도 않습니다.
토요일에 닫는 시각은 두 자료 모두 오후 5시(17:00)입니다.

## 4. 문서 벡터와 검색 함수

다음 셀은 Ch 14 06절과 같은 임베딩 모델과 벡터 크기로 문서 열두 건을 벡터로 바꿉니다.
벡터 크기 인자 `dimensions`는 Ch 10 07절에서 배웠습니다.
메서드 `embed_documents`는 글 목록을 받아 벡터 목록을 내놓고, 이 셀의 임베딩 요청은 1번입니다.
Ch 14 폴더에는 저장해 둔 문서 벡터 파일이 없어, 이 노트북에서 만들고 파일로 쓰지 않습니다."""),
        code(EMBED_DOCS),
        md("""**결과 읽기** — 출력 줄 `임베딩 모델 이름: text-embedding-3-small`과 `벡터의 숫자 개수 설정: 256`입니다.
출력 줄 `문서 벡터 수: 12`로, 문서마다 벡터가 하나씩 생겼습니다.
설정 둘은 Ch 14 06절 출력과 같습니다.

다음 셀은 Ch 14 06절처럼 질문 글을 그대로 검색 함수에 넣습니다.
함수 `search_hits`는 질문 글을 벡터로 바꾸고, 거리가 작은 차례로 문서 `top_count`건을 내놓습니다.
부를 때마다 임베딩 요청이 1번 나갑니다.
자를 개수 `top_count`는 Ch 14에서 나란히 볼 때 쓴 3으로 둡니다."""),
        code(DIRECT),
        md("""**결과 읽기** — 라벨 줄 `질문 글을 그대로 검색한 순위:` 아래 표의 첫 줄이 `1 | FAC-003 | 0.6`입니다.
정답 문서 `FAC-003`이 첫 자리에 왔고, 둘째 자리는 `LIB-002`입니다.
거리는 작을수록 가깝고, Ch 12 01절처럼 소수 둘째 자리까지 남긴 값입니다.

임베딩 값은 요청마다 아주 조금 달라질 수 있어, 거리의 끝자리가 바뀔 수 있습니다.
이번 실행에서는 셋째 자리가 `FAC-004`, 거리는 `0.72`였습니다.

## 5. 검색 함수를 도구로 감싸기

검색 함수를 도구로 감싸면, 모델이 도구 호출 요청으로 검색을 부를 수 있습니다.
도구의 매개변수 `query`에는 모델이 적은 검색어가 들어옵니다.
도구 몸통은 그 검색어로 `search_hits`를 부르고, 찾은 문서마다 문서 ID와 글을 한 줄씩 잇습니다.
이어 붙인 글이 도구 메시지가 되어, 다음 모델 요청에 실립니다.

도구 안에서 쓰는 `doc_vectors`·`doc_ids`·`text_by_doc`는 이 노트북에서 만든 이름입니다.
01절 도구가 딕셔너리 `POLICIES`를 읽은 것과 같은 모양입니다.
도구 메시지에는 거리를 넣지 않고, 문서 ID와 글만 적습니다."""),
        code(DEF_SEARCH),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
도구 이름은 함수 이름 `search_documents`이고, 모델이 읽는 설명 글은 독스트링입니다.
이 도구를 부를 때마다 몸통의 `search_hits`가 임베딩 요청을 1번 보냅니다.

다음 셀은 Ch 19 01절처럼 도구 이름과 입력 형식, 도구 명세의 인자를 봅니다."""),
        code(SPEC),
        md("""**결과 읽기** — 출력 줄 `도구 이름: search_documents`와 `입력 형식의 인자: ['query']`입니다.
출력 줄 `명세의 인자: ['query']`로, 모델에게 보이는 인자는 `query` 하나입니다.
모델이 채울 값은 검색어뿐이고, 문서 벡터와 자를 개수는 노트북이 정해 둔 값입니다.

## 6. 검색 도구를 넣은 에이전트 그래프

시스템 메시지 글의 첫 문장은 01절 4절 글과 같습니다.
둘째 문장은 도구 이름과 근거를 이 절 도구에 맞게 고쳤습니다.
셋째 문장은 찾은 문서에 답이 없을 때 검색어를 바꿔 한 번만 더 검색하라는 규칙입니다.
이 규칙은 모델에게 적은 글이고, 검색 횟수를 세거나 막는 코드는 없습니다.

다음 셀은 01절처럼 모델 객체·도구 목록·시스템 메시지 글을 넘겨 에이전트 그래프를 만듭니다."""),
        code(AGENT),
        md("""**결과 읽기** — 출력 줄 `만든 것의 종류: CompiledStateGraph`로, 01절과 같은 종류의 그래프입니다.
이 줄에서는 모델 요청도 임베딩 요청도 나가지 않습니다.

다음 셀은 02절 함수 `print_branches`로 노드와 조건 함수를 봅니다."""),
        code(SHAPE),
        md("""**결과 읽기** — 출력 줄 `등록된 노드: ['model', 'tools']`는 01절과 같습니다.
출력 줄 `tools | 조건 함수: tools_to_model | 갈 수 있는 곳: ['model']`도 01절과 같습니다.
출력 줄 `model | 조건 함수: model_to_tools | 갈 수 있는 곳: ['tools', '__end__']`도 01절과 같습니다.
도구를 검색 도구로 바꿔도 에이전트 그래프의 모양은 바뀌지 않았습니다.

## 7. C05 질문 보내기

실행 전에 예상해 봅니다.
모델이 검색 도구를 한 번 부르고, 도구 메시지 첫 줄에 정답 문서 `FAC-003`이 올 것입니다.
그러면 모델 요청은 2번, 도구 안 임베딩 요청은 1번입니다.
메시지 칸에는 메시지 넷이 남을 것입니다."""),
        code(RUN_C05),
        md("""**결과 읽기** — 출력 줄 `메시지 칸의 메시지 수: 4`입니다.
라벨 줄 `메시지 칸:` 아래 둘째 줄 `AIMessage | 도구 호출 요청: ['search_documents']`에서 검색 도구를 불렀습니다.
셋째 줄 도구 메시지의 내용은 문서 세 줄이고, 첫 줄이 `[FAC-003]`으로 시작합니다.
마지막 줄 `AIMessage | 도구 호출 요청: []`에서 요청이 없어 흐름이 끝났습니다.

다음 셀은 첫 응답에서 모델이 도구 호출 요청에 채운 인자를 봅니다."""),
        code(ARGS_C05),
        md("""**결과 읽기** — 출력 줄은 `도구 이름: search_documents | 인자:`로 시작합니다.
인자 딕셔너리의 키는 `query` 하나입니다.
Ch 14 06절에서는 코드가 질문 글을 그대로 검색에 넣었습니다.
이 흐름에서는 검색에 넣을 글을 모델이 인자로 적습니다.

검색어는 모델이 쓴 글이라 실행마다 달라질 수 있습니다.
이번 실행에서는 `{'query': '토요일 자료실 폐관 시각'}`으로, 질문 글 끝의 「은?」만 뺀 글이었습니다.
그래서 도구 메시지 셋째 줄이 4절 순위의 셋째 자리와 달랐습니다.

같은 검색어로 검색하면 같은 문서가 나오는지 봅니다.
다음 셀은 첫 응답의 도구 호출 요청을 Ch 19 05절처럼 도구에 그대로 다시 보냅니다.
도구 호출 요청을 통째로 넘기면 도구 메시지가 나오고, 임베딩 요청이 1번 더 나갑니다."""),
        code(AGAIN),
        md("""**결과 읽기** — 출력 줄 `다시 받은 메시지의 종류: ToolMessage`입니다.
출력 줄 `도구 메시지 글과 같은가: True`로, 같은 검색어가 같은 문서 셋을 같은 차례로 내놓았습니다.
검색어가 같으면 거리 순위는 검색 함수의 계산으로 정해집니다.

이 비교에는 `assert`를 걸지 않았습니다.
임베딩 값이 요청마다 아주 조금 달라질 수 있어, 거리가 거의 같은 두 문서는 차례가 바뀔 수 있기 때문입니다.

다음 셀은 메시지 칸의 마지막 응답을 봅니다."""),
        code(ANSWER_C05),
        md("""**결과 읽기** — 출력 줄 `마지막 응답의 도구 호출 요청 수: 0`입니다.
라벨 줄 `답 글:` 아래가 모델이 도구 메시지를 보고 쓴 답입니다.

답 글은 모델이 쓴 글이라 실행마다 글자가 달라질 수 있습니다.
이번 실행에서는 토요일 폐관 시각을 오후 5시로 답했고, 문서 `FAC-003`의 글과 같은 시각입니다.

## 8. 값 바꿔 보기 · 문서에 없는 질문

바꿀 값은 질문 하나이고, 에이전트 그래프와 시스템 메시지 글은 그대로 둡니다.
문서 열두 건에 주차 이야기가 없는 질문으로 바꿉니다.
실행 전에 예상해 봅니다.
검색 도구는 관련 문서가 없어도 거리가 가까운 문서 세 건을 내놓을 것입니다.
모델이 규칙대로 한 번 더 검색하면, 모델 요청은 3번이고 도구 메시지는 둘일 것입니다."""),
        code(RUN_PARK),
        md("""**결과 읽기** — 출력 줄 `메시지 칸의 메시지 수: 6`입니다.
라벨 줄 `메시지 칸:` 아래에 `AIMessage | 도구 호출 요청: ['search_documents']`가 두 번 보입니다.
도구 메시지도 둘이고, 두 도구 메시지 모두 문서 세 줄을 담았습니다.
첫 도구 메시지의 첫 줄은 `[FAC-002]`로, 주차가 아니라 프린터 이용 요금 문서입니다.
검색 함수는 거리가 가까운 차례로 늘 `top_count`건을 내놓으므로, 관련 문서가 없어도 문서가 나옵니다.

다음 셀은 응답마다 도구 호출 요청 수와 검색어를 봅니다."""),
        code(ARGS_PARK),
        md("""**결과 읽기** — 라벨이 `응답 | 도구 호출 요청 수:`인 줄이 셋이고, 값은 차례로 `1`·`1`·`0`입니다.
응답마다 검색 요청을 하나씩 보내, 검색을 두 응답에 걸쳐 두 번 했습니다.
시스템 메시지 글의 「한 번만 더 검색」대로, 다시 검색은 한 번이었습니다.
그래프에는 검색 횟수를 세거나 막는 줄이 없고, 세 번째 검색을 고른 실행은 이번에 없었습니다.

검색어는 실행마다 달라질 수 있습니다.
이번 실행에서는 첫 검색어가 `{'query': '주차 요금'}`, 둘째가 `{'query': '주차'}`였습니다.

다음 셀은 바꾼 질문의 마지막 응답을 봅니다."""),
        code(ANSWER_PARK),
        md("""**결과 읽기** — 출력 줄 `마지막 응답의 도구 호출 요청 수: 0`입니다.
라벨 줄 `답 글:` 아래가 모델이 도구 메시지 둘을 보고 쓴 답입니다.

답 글은 실행마다 글자가 달라질 수 있습니다.
이번 실행에서는 문서에서 주차 요금을 찾지 못했다는 뜻의 한 문장이었습니다.

## 9. 요청 수와 예상 비용

다음 셀은 두 결과의 도구 메시지마다 문서 ID를 꺼내 셉니다.
도구 몸통은 줄 머리에 대괄호로 문서 ID를 적으므로, 대괄호로 시작하는 줄이 문서 한 건입니다.
메서드 `split`으로 줄을 나누고, `]` 앞 글자에서 첫 글자를 빼면 문서 ID가 남습니다."""),
        code(DOC_LINES),
        md("""**결과 읽기** — 라벨이 `도구 메시지의 문서 ID:`인 줄이 셋입니다.
첫 줄 `['FAC-003', 'LIB-002', 'ACC-004']`는 7절, 둘째·셋째 줄은 8절의 도구 메시지입니다.
세 줄 모두 문서 ID가 셋이고, 셀의 `assert`는 이 개수에만 걸었습니다.
개수는 도구 몸통이 `top_count`로 정하는 값이라, 모델이 무엇을 검색해도 같습니다.

8절 두 도구 메시지는 이번 실행에서 `['FAC-002', 'ACC-004', 'ACC-001']`과 `['FAC-004', 'ACC-004', 'FAC-002']`였습니다.
검색어가 달라지면 이 차례도 달라질 수 있습니다.

다음 셀은 01절 10절 함수 `agent_row`로 두 질문을 한 줄씩 적습니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄이 `C05 질문 | 2 | 1 | True`와 `주차 질문 | 3 | 2 | True`입니다.
두 질문 모두 모델 요청 수가 도구 메시지 수보다 1 많았습니다.
01절에서 본 것처럼, 이 셈은 응답마다 요청을 하나씩 받을 때만 맞습니다.
호출 ID 짝은 두 질문 모두 맞았고, 셀의 `assert`로 확인했습니다.

검색 도구는 부를 때마다 임베딩 요청을 1번 보냅니다.
그래서 도구 메시지 수가 곧 도구 안 임베딩 요청 수입니다.
다음 셀은 이 노트북이 보낸 임베딩 요청을 셉니다.
검색 함수를 직접 부른 곳은 4절 질문 글 검색과 7절 다시 부르기, 두 곳입니다."""),
        code(EMBED_COUNT),
        md("""**결과 읽기** — 출력 줄 `검색 도구 안에서 보낸 요청: 3`과 `임베딩 요청 합계: 6`입니다.
문서 벡터를 만든 요청 1번과 직접 부른 요청 2번을 더한 값입니다.
모델이 검색을 더 고르면 도구 안 요청과 합계가 함께 늘어납니다.

다음 셀은 Ch 19 05절 함수 `sum_usage`로 두 결과의 모델 요청 수와 토큰을 더합니다."""),
        code(USAGE),
        md("""**결과 읽기** — `C05 질문 사용량:`은 `'requests': 2`, `주차 질문 사용량:`은 `'requests': 3`입니다.
입력 토큰은 C05 질문 `'input_tokens': 638`, 주차 질문 `'input_tokens': 1189`입니다.
주차 질문은 모델 요청이 한 번 더 있어, 입력 토큰 합이 더 컸습니다.
요청마다 어느 몫이 몇 토큰인지는 나눠 세지 않았습니다.

출력 토큰은 모델이 쓴 글에 따라 실행마다 달라질 수 있습니다.
이번 실행에서는 C05 질문 `'output_tokens': 44`, 주차 질문 `'output_tokens': 59`였습니다.

다음 셀은 Ch 6 06절 함수 `estimate_cost`로 두 사용량의 예상 비용을 셉니다.
요금은 2026-09-17 요금표의 100만 토큰당 달러입니다."""),
        code(COST),
        md("""**결과 읽기** — 라벨 `C05 질문 예상 비용(달러):`와 `주차 질문 예상 비용(달러):` 뒤 값이 모델 몫의 예상 비용입니다.
요금표로 어림한 값이고, 청구 금액이 아닙니다.
임베딩 요금은 넣지 않았습니다.
이 노트북은 임베딩 요청의 토큰 수를 세지 않기 때문입니다.

출력 토큰이 실행마다 달라질 수 있어, 이 값도 달라질 수 있습니다.
이번 실행에서는 C05 질문 `0.000677`달러, 주차 질문 `0.001157`달러였습니다.

## 정리

1. Ch 14 06절 검색 함수 `search_hits`를 `@tool` 도구로 감싸자, 모델이 인자 `query`에 검색어를 적어 검색을 불렀습니다.
2. 같은 검색어로 도구를 다시 부르면 같은 문서 셋이 같은 차례로 나왔고, 도구 메시지마다 문서는 `top_count`건이었습니다.
3. 문서에 답이 없는 질문에서 모델은 검색을 두 번 했고, 「한 번만 더」는 시스템 메시지 글일 뿐 코드 제한이 아니었습니다.

06절에서는 같은 평가 질문을 두 흐름으로 보내 견줍니다.
검색을 먼저 하는 흐름과, 검색 도구를 쓰는 에이전트 흐름입니다."""),
    ]


def html_text(text: str) -> str:
    """노트북용 마크다운 한 단락(백틱·줄바꿈)을 _src 문단 글로 바꿉니다."""
    parts = text.replace("\n", " ").split("`")
    out = ""
    for index in range(len(parts)):
        if index % 2 == 1:
            out = out + "<code>" + parts[index] + "</code>"
        else:
            out = out + parts[index]
    return out


L_CH05_02 = "../../part1/ch05-llm-principles/02-임베딩과-의미-유사도.html"
L_CH06_06 = "../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html"
L_CH09_01 = "../../part3/ch09-rag-first-run/01-RAG-지도.html"
L_CH10_07 = "../../part3/ch10-document-processing/07-한국어-임베딩과-캐시.html"
L_CH11_01 = "../../part3/ch11-evaluation/01-질의셋과-정답-문서-ID.html"
L_CH12_01 = "../../part3/ch12-retrieval-tuning/01-벡터-거리와-정확-검색.html"
L_CH12_05 = "../../part3/ch12-retrieval-tuning/05-dense와-sparse-비교.html"
L_CH14_01 = "../../part4/ch14-rag-patterns/01-대화-히스토리와-질문-재작성.html"
L_CH14_06 = "../../part4/ch14-rag-patterns/06-CRAG.html"
L_CH19_01 = "../../part5/ch19-model-tools/01-tool과-Ch4-함수-재사용.html"
L_CH19_05 = "../../part5/ch19-model-tools/05-bind_tools와-병렬-호출.html"
L_CH20_03 = "../../part5/ch20-tool-node/03-recursion-limit과-명시적-종료.html"
L_CH22_04 = "../ch22-middleware/04-호출-한도와-재시도-폴백.html"
L_01 = "01-create-agent와-ReAct-루프.html"
L_02 = "02-구조화-출력-두-전략.html"
L_04 = "04-0x에서-1x로-마이그레이션.html"
L_06 = "06-같은-평가셋으로-RAG-비교.html"

RESULT_ROWS = [
    ("C05 질문(7절)", "4", "2", "1", "<code>FAC-003</code>·<code>LIB-002</code>·<code>ACC-004</code>", "1", "638"),
    ("주차 질문(8절, 바꾼 값)", "6", "3", "2",
     "첫째 <code>FAC-002</code>·<code>ACC-004</code>·<code>ACC-001</code> / 둘째 <code>FAC-004</code>·<code>ACC-004</code>·<code>FAC-002</code>",
     "2", "1189"),
]


def result_table_html() -> str:
    body = ""
    for row in RESULT_ROWS:
        cells_html = ""
        for value in row:
            cells_html = cells_html + "<td>" + value + "</td>"
        body = body + "<tr>" + cells_html + "</tr>"
    head = ("<tr><th>실행</th><th>메시지 수</th><th>응답 수(모델 요청)</th><th>도구 메시지 수</th>"
            "<th>도구 메시지의 문서 ID</th><th>도구 안 임베딩 요청</th><th>입력 토큰</th></tr>")
    return "<table><thead>" + head + "</thead><tbody>" + body + "</tbody></table>"


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


def src_html() -> str:
    return """<!--meta: 강의 1h | 실습 2h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>Ch 14 06절 검색 함수 <code>search_hits</code>를 <code>@tool</code> 도구로 감싸 <code>create_agent</code>에 넘길 수 있습니다.</li>
<li>모델이 채운 검색어와 도구 메시지의 문서 ID를 출력으로 읽고, 같은 검색어면 같은 문서가 나오는지 확인할 수 있습니다.</li>
<li>다시 검색을 시스템 메시지 글로만 정했을 때, 검색 횟수가 코드 제한이 아니라 모델 선택임을 설명할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>제목의 retriever는 질문을 받아 가까운 문서를 찾아 주는 검색 부분을 가리키는 영어 말입니다. 이 과정에서는 <a href=\"""" + L_CH14_06 + """\">Ch 14 06절</a> 검색 함수 <code>search_hits</code>가 그 일을 했습니다. 이 절은 그 검색 함수를 에이전트 그래프의 도구로 바꿉니다.</p><p>Ch 14 06절에서는 코드가 질문 글을 그대로 검색에 넣어 먼저 한 번 검색했습니다. 다시 검색할지도 코드가 첫 자리 거리를 기준값과 견주어 정했습니다. Ch 14의 다른 절에서 모델이 질문을 고쳐 썼을 때도, 검색을 부르는 때는 코드가 정했습니다. 검색 함수를 도구로 감싸면, 검색할지와 무엇으로 검색할지를 모델이 고릅니다.</p><p>모델이 고르는 값은 편리하지만 흔들릴 수 있습니다. 그래서 이 절은 모델이 고른 값과 코드가 정한 값을 출력에서 나눠 셉니다. 검색어와 검색 횟수는 모델 쪽이고, 도구 메시지의 문서 개수와 호출 ID 짝은 코드 쪽입니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH09_01 + """\">Ch 9 01절</a>에서 임베딩 모델 <code>OpenAIEmbeddings</code>로 글을 벡터로 바꿨고, <a href=\"""" + L_CH10_07 + """\">Ch 10 07절</a>에서 벡터 크기 인자 <code>dimensions</code>를 보았습니다. <a href=\"""" + L_CH05_02 + """\">Ch 5 02절</a>에서는 코사인 유사도를 NumPy로 계산했습니다. <a href=\"""" + L_CH12_01 + """\">Ch 12 01절</a>에서는 코사인 거리와 거리 순위 함수를, <a href=\"""" + L_CH12_05 + """\">05절</a>에서는 순위 출력 함수 <code>print_ranked</code>를 적었습니다.</p><p><a href=\"""" + L_CH14_06 + """\">Ch 14 06절</a>은 질문 하나를 벡터로 바꿔 거리 순위를 만드는 <code>search_hits</code>를 적었습니다. 같은 절은 첫 자리 거리가 기준값보다 크면 한 번만 다시 검색하게 했고, 그 상한을 코드로 확인했습니다. 문서 모음은 Ch 12와 같은 문서 열두 건과 질문 여덟 건입니다. 질문마다 <a href=\"""" + L_CH11_01 + """\">Ch 11 01절</a>의 정답 문서 ID가 적혀 있습니다.</p><p><a href=\"""" + L_CH19_01 + """\">Ch 19 01절</a>에서는 맨 <code>@tool</code>로 도구를 만들고 도구 명세를 보았습니다. <a href=\"""" + L_CH19_05 + """\">Ch 19 05절</a>에서는 도구 호출 요청을 도구에 넘겨 도구 메시지를 받았습니다. <a href=\"""" + L_01 + """\">01절</a>에서는 함수 <code>create_agent</code>와 함수 <code>agent_row</code>를, <a href=\"""" + L_02 + """\">02절</a>에서는 함수 <code>print_branches</code>를 보았습니다.</p><p>05절부터는 Ch 14 문서 모음을 씁니다. Ch 14 운영 시간 문서는 평일 운영을 오전 9시부터 오후 9시까지로 적습니다. 01~04절 규정 딕셔너리는 평일 09:00~20:00으로 적었습니다. 두 글은 서로 다른 자료이고, 이 절은 01절 자료를 고치지 않습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절에서는 에이전트 그래프를 버튼 하나로 도는 세탁기에 견주었습니다. 이번에는 세제를 넣는 두 방법을 떠올려 봅니다. 하나는 빨래를 넣을 때마다 사람이 세제를 한 컵씩 먼저 붓는 방법입니다. 다른 하나는 세제 통을 세탁기에 꽂아 두고, 세탁기가 필요할 때 끌어 쓰게 하는 방법입니다.</p><p>Ch 14의 흐름은 앞의 방법처럼, 코드가 질문마다 검색을 먼저 한 번 했습니다. 이 절의 흐름은 뒤의 방법입니다. 세제 통이 검색 함수이고, 통을 꽂는 자리가 검색 도구입니다. 세탁기인 에이전트 그래프 안에서 모델이 필요할 때 검색을 부릅니다.</p>
""" + illustration_block() + """<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>검색 함수(retriever)</td><td>질문 글을 받아 가까운 문서를 거리 차례로 찾아 내놓는 함수입니다. 제목의 retriever가 이 일을 하는 부분을 가리키고, 이 절에서는 Ch 14 06절 <code>search_hits</code>입니다. 비유에서 세제 통과 같습니다.</td></tr><tr><td>검색 도구</td><td>검색 함수를 <code>@tool</code>로 감싼 도구입니다. 모델이 도구 호출 요청을 보낼 때만 실행되고, 찾은 문서의 글을 도구 메시지로 내놓습니다. 비유에서 세제 통을 꽂는 자리와 같습니다.</td></tr><tr><td>검색어(query)</td><td>모델이 검색 도구의 인자 <code>query</code>에 적은 글입니다. 질문 글과 같을 수도 다를 수도 있고, 실행마다 달라질 수 있습니다. 비유에서 세탁기가 그때그때 정하는 세제의 양과 같습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 검색 함수는 노트북 4절 <code>search_hits(embedding_model, c05_question, …)</code> 줄입니다. 검색 도구는 5절 <code>@tool</code> 아래 <code>search_documents</code>이고, 6절에서 <code>tools=[search_documents]</code>로 넘깁니다. 검색어는 7절 출력의 인자 <code>{'query': …}</code>입니다.</p>
{{mermaid:""" + FIG1 + "|" + FIG1_ALT + "|" + FIG1_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG1_READ) + """</p>
<h3>검색어와 검색 횟수를 정하는 쪽</h3><p>Ch 14 06절에서는 첫 검색어가 질문 글 그대로였습니다. 다시 검색할지는 첫 자리 거리를 기준값과 견주어 코드가 정했고, 다시 검색은 한 번까지였습니다. 이 절에서는 검색어를 모델이 인자로 적습니다. 다시 검색하라는 규칙은 시스템 메시지 글에만 있고, 그 횟수를 세거나 막는 코드는 없습니다.</p>
{{mermaid:""" + FIG2 + "|" + FIG2_ALT + "|" + FIG2_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG2_READ) + """</p>
<h3>다른 상황에 적용</h3><p>Ch 19의 주문 조회 흐름에 사내 안내 문서 검색을 더한다면, 같은 방법으로 검색 함수를 도구 하나로 감쌀 수 있습니다. 모델은 주문 질문에는 주문 도구를, 안내 질문에는 검색 도구를 고를 것입니다. 이 조합은 이번에 실행하지 않았습니다.</p>
<h3>비교와 경계</h3><p>LangChain에는 벡터스토어를 검색 객체로 바꾸는 <code>as_retriever()</code>도 있지만, 과정에서 쓰지 않았고 이번에도 실행하지 않았습니다. 이 절의 검색 도구는 Ch 14에서 적은 평범한 함수를 감싼 것입니다. 검색을 늘 먼저 하는 흐름과 이 흐름을 같은 질문으로 견주는 일은 <a href=\"""" + L_06 + """\">06절</a>에서 합니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 Ch 14 문서 파일과 질문 파일을 읽고, 문서 열두 건을 벡터로 바꿉니다. 질문 글을 그대로 검색 함수에 넣어 거리 순위를 본 뒤, 검색 함수를 도구로 감싸 에이전트 그래프에 넣습니다. <code>C05</code> 질문을 보내고, 같은 검색어로 도구를 다시 불러 봅니다. 값 바꿔 보기로 질문 하나만 문서에 없는 주차 질문으로 바꿉니다.</p><p>모델은 01절과 같은 <code>gpt-5.4-mini</code>이고, temperature 0과 추론 끔(<code>reasoning_effort="none"</code>)으로 부릅니다. 임베딩 모델은 Ch 14와 같은 <code>text-embedding-3-small</code>이고 벡터 크기는 256입니다. 교재 출력에서 모델 요청은 모두 5번, 임베딩 요청은 모두 6번입니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — 노트북 5절에서 명세의 인자가 <code>['query']</code> 하나인지 봅니다. 노트북 7절에서 도구 메시지가 문서 세 줄이고, 같은 검색어로 다시 부른 글이 같은지 확인합니다. 8절에서 응답마다 도구 호출 요청 수가 <code>1</code>·<code>1</code>·<code>0</code>인지 봅니다. 검색어와 답 글은 실행마다 달라질 수 있어 결론에 쓰지 않았습니다.</p>
{{mermaid:""" + FIG3 + "|" + FIG3_ALT + "|" + FIG3_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG3_READ) + """</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>실험에서 바꾼 것은 질문 하나입니다. 모델·검색 도구·시스템 메시지 글·문서 벡터·<code>top_count</code>는 그대로였습니다.</p>
""" + result_table_html() + """
{{mermaid:""" + FIG4 + "|" + FIG4_ALT + "|" + FIG4_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG4_READ) + """</p>
<p>두 질문 모두 도구 메시지마다 문서는 세 건이었습니다. 이 개수는 도구 몸통이 <code>top_count</code>로 정하는 값입니다. 주차 질문처럼 관련 문서가 없어도 거리가 가까운 문서 세 건이 나왔고, 답이 없다는 판단은 모델이 글을 읽고 내렸습니다.</p><p>검색 횟수는 <code>C05</code> 질문 한 번, 주차 질문 두 번이었습니다. 주차 질문의 두 번째 검색은 시스템 메시지 글의 「한 번만 더 검색」과 맞았습니다. 규칙 문장을 뺀 실행은 하지 않아, 규칙 때문인지는 확인하지 않았습니다. 코드가 횟수를 막은 것이 아니므로, 모델이 달리 고르면 모델 요청 수와 임베딩 요청 수가 함께 달라집니다.</p><p>새 커널로 두 번 실행했을 때 표의 값은 두 번 모두 같았습니다. 노트북 밖에서 두 질문을 다섯 번씩 보냈을 때도 같았습니다. 같은 검색어로 다시 부른 결과는 노트북 7절과 노트북 밖 확인 열다섯 번에서 모두 같은 글이었습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>노트북을 실행하기 전에 노트북 밖에서 두 질문을 다섯 번씩 보냈습니다. 메시지 종류와 차례, 응답마다 요청 수, 검색어, 도구 메시지의 문서 ID, 입력 토큰이 다섯 번 모두 같았습니다. 같은 요청도 실행한 때에 따라 모델이 고르는 검색어와 검색 횟수가 달라질 수 있습니다. 그때는 도구 메시지 수·모델 요청 수·임베딩 요청 수가 함께 달라집니다.</li><li>시스템 메시지 글의 「한 번만 더 검색」은 모델에게 적은 규칙입니다. 그래프에는 검색 횟수를 세거나 막는 줄이 없고, 함수 <code>create_agent</code>에는 모델 요청 수 한도 인자가 없습니다. 호출 수를 코드로 막는 미들웨어는 <a href=\"""" + L_CH22_04 + """\">Ch 22 04절</a>에서 배웁니다. <a href=\"""" + L_CH20_03 + """\">Ch 20 03절</a>의 실행 한도는 그래프 단계 수라, 검색 횟수와 같은 값이 아닙니다.</li><li>모델이 규칙을 넘겨 세 번 검색하는 실행은 이번에 없었고, 실행하지 않았습니다. 모델이 검색 도구를 부르지 않는 경우와 도구 안에서 오류가 나는 경우도 이번에 실행하지 않았습니다.</li><li>셀의 <code>assert</code>는 도구 메시지마다 문서 개수와 호출 ID 짝에만 걸었습니다. 검색어와 답 글은 모델이 쓴 글이라 <code>assert</code>하지 않았고 결론에도 쓰지 않았습니다.</li><li>같은 검색어로 다시 부른 결과가 같은지는 출력으로만 보았습니다. 임베딩 값은 요청마다 소수 끝자리에서 아주 조금 달라질 수 있어, 거리가 거의 같은 두 문서는 차례가 바뀔 수 있습니다. 그래서 이 비교에는 <code>assert</code>를 걸지 않았습니다.</li><li>Ch 14 실습 폴더에는 저장해 둔 문서 벡터 파일이 없습니다. 그래서 문서 벡터를 노트북마다 한 번 만들고, 파일로 쓰지 않았습니다.</li><li>Ch 14 운영 시간 문서는 평일 운영을 오전 9시~오후 9시로 적습니다. 01절 규정 딕셔너리는 평일 09:00~20:00으로 적었고, 두 글은 서로 다른 자료입니다. 이 절은 01절 자료를 고치지 않았습니다.</li><li><code>C05</code> 질문, 주차 질문, 도구 글, 시스템 메시지 글, <code>top_count</code> 3은 흐름을 보여 주려고 정한 예입니다. 모두 노트북 밖 확인 전에 정했습니다.</li><li>함수 <code>search_hits</code>·<code>print_ranked</code>와 거리 함수 셋은 Ch 14 도구 파일에서 본문을 글자 그대로 옮겼습니다. 함수 <code>estimate_cost</code>는 <a href=\"""" + L_CH06_06 + """\">Ch 6 06절</a>에서 배웠습니다.</li><li>예상 비용은 모델 몫만 2026-09-17 요금표로 어림했고, 노트북 한 번에 0.01달러 아래이며 청구 금액이 아닙니다. 임베딩 요금(100만 토큰당 0.02달러)은 토큰 수를 세지 않아 넣지 않았습니다. 걸린 시간은 재지 않았습니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>Ch 14 06절 검색 함수 <code>search_hits</code>를 <code>@tool</code> 도구로 감싸자, 모델이 인자 <code>query</code>에 검색어를 적어 검색을 불렀습니다.</li><li>같은 검색어로 도구를 다시 부르면 같은 문서 셋이 같은 차례로 나왔고, 도구 메시지마다 문서는 <code>top_count</code>건이었습니다.</li><li>문서에 답이 없는 질문에서 모델은 검색을 두 번 했고, 「한 번만 더」는 시스템 메시지 글일 뿐 코드 제한이 아니었습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_06 + """\">06절</a>에서는 같은 평가 질문을 두 흐름으로 보내 견줍니다. 검색을 먼저 하는 흐름과, 검색 도구를 쓰는 에이전트 흐름입니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 검색 도구 <code>search_documents</code>의 도구 명세에 실린 인자는 무엇이고, 그 값은 누가 채웠나요?</p><p class="quiz-a">인자는 <code>query</code> 하나이고, 모델이 검색어를 적어 채웠습니다. 문서 벡터와 자를 개수는 노트북이 정해 둔 값이라 명세에 없습니다. 틀렸다면 노트북 5절과 7절을 다시 읽습니다.</p><p class="quiz-q">2. 첫 응답의 도구 호출 요청을 도구에 다시 보냈을 때 무엇이 같았고, 왜 <code>assert</code>를 걸지 않았나요?</p><p class="quiz-a">다시 받은 도구 메시지 글이 처음 도구 메시지 글과 같았습니다. 같은 검색어면 같은 문서 셋이 같은 차례로 나옵니다. 다만 임베딩 값이 요청마다 아주 조금 달라질 수 있어 <code>assert</code>는 걸지 않았습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">3. 주차 질문에서 검색 도구는 관련 문서가 없는데도 무엇을 내놓았나요?</p><p class="quiz-a">거리가 가까운 차례로 문서 세 건을 내놓았고, 첫 도구 메시지의 첫 줄은 프린터 이용 문서 <code>FAC-002</code>였습니다. 답이 없다는 판단은 모델이 도구 메시지 글을 읽고 내렸습니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p><p class="quiz-q">4. 「한 번만 더 검색」 규칙은 어디에 적혀 있고, 이번 검색 횟수는 무엇이 정했나요?</p><p class="quiz-a">규칙은 시스템 메시지 글에만 있고, 검색 횟수는 모델이 골랐습니다. 그래프에는 횟수를 세거나 막는 코드가 없습니다. Ch 14 06절은 다시 검색의 상한을 코드로 정했다는 점이 다릅니다. 틀렸다면 노트북 6절과 8절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langchain/retrieval">LangChain Retrieval</a></div>확인 2026-09-25 · 검색을 늘 먼저 하는 흐름과 에이전트가 검색 시점을 고르는 흐름을 나눠 설명합니다.</li><li>langchain 1.4.0 소스 <code>langchain/agents/factory.py</code> 840~858행 — 함수 <code>create_agent</code>의 인자 목록이고, 모델 요청 수 한도 인자는 없습니다.</li><li>langchain-openai 1.6.0 소스 <code>langchain_openai/embeddings/base.py</code> 260행 — 한 요청에 담는 글 수의 기본값 1000입니다.</li><li>같은 소스 577~620행은 글 목록을 요청 단위로 묶는 자리입니다.</li><li>같은 소스 796~807행은 질문 한 줄을 벡터로 바꾸는 <code>embed_query</code>입니다.</li><li>Ch 14 06절에서 검색 함수 <code>search_hits</code>와 다시 검색의 상한을, Ch 12 01절에서 코사인 거리를 보았습니다.</li><li>Ch 19 01·05절에서 도구 명세와 도구 호출 요청을 도구에 넘기는 법을 보았습니다.</li><li>01절에서 함수 <code>create_agent</code>와 <code>agent_row</code>를, 02절에서 함수 <code>print_branches</code>를 보았습니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    check_same_as_before()
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "05", SLUG, "experiment", cells())
        print("wrote", path)
