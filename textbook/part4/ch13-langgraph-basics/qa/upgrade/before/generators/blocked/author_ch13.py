# 옛 생성기 — 실행하지 마세요 (QUALITY-UPGRADE.md §8, PLAYBOOK §2-1).
# 이 파일은 품질 개선 전 Ch 13 노트북 일곱 개를 한 번에 쓰던 생성기입니다.
# 지금은 절마다 qa/upgrade/author_NN.py 가 그 절 노트북 하나만 씁니다.
# 이 파일을 실행하면 개선된 노트북이 옛 판으로 덮어써지므로 아래 줄로 실행을 막습니다.
# 02~07절 작업자는 이 파일을 **읽기 자료로만** 쓰고(학습 질문·데이터·형식 유지),
# 새 생성기는 qa/upgrade/author_NN.py 로 만듭니다.
# 챕터 마감 때 qa/upgrade/before/generators/ 로 mv -n 합니다(삭제 아님).

from __future__ import annotations

raise SystemExit("옛 생성기입니다. 절 생성기 qa/upgrade/author_NN.py 를 쓰세요.")

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHAPTER = ROOT / "textbook/part4/ch13-langgraph-basics"
LAB = ROOT / "labs/part4/ch13-langgraph-basics"
sys.path.insert(0, str(LAB.parent))
from notebook_guidance import inject_guidance
DEPTH_NOTES = json.loads((CHAPTER / "qa/depth-notes.json").read_text(encoding="utf-8"))


def depth_html(slug: str) -> str:
    note = DEPTH_NOTES[slug]
    return (
        f"<h3>호출 표기와 실행 시점</h3><p>{note['mechanics']}</p>"
        f"<h3>다른 상황에 적용</h3><p>{note['transfer']}</p>"
        f"<h3>비교와 경계</h3><p>{note['boundary']}</p>"
    )


def depth_markdown(slug: str) -> dict:
    note = DEPTH_NOTES[slug]
    text = (
        "## 개념을 코드에 연결하기\n\n"
        f"**호출 표기와 실행 시점.** {note['mechanics']}\n\n"
        f"**다른 상황에 적용.** {note['transfer']}\n\n"
        f"**비교와 경계.** {note['boundary']}\n"
    )
    return {"cell_type": "markdown", "id": "concept-depth", "metadata": {}, "source": text.splitlines(keepends=True)}

DOCS = [
    ("LangGraph Graph API 안내", "https://docs.langchain.com/oss/python/langgraph/graph-api"),
    ("LangGraph Graph API 사용법", "https://docs.langchain.com/oss/python/langgraph/use-graph-api"),
    ("StateGraph API", "https://reference.langchain.com/python/langgraph/graph/state/StateGraph"),
]

DOCS_BY_SLUG = {
    "04-add_messages-리듀서": [("add_messages API", "https://reference.langchain.com/python/langgraph/graph/message/add_messages")],
    "05-Send-동적-팬아웃": [("Send API", "https://reference.langchain.com/python/langgraph/types/Send")],
    "06-Command-갱신과-이동": [("Command API", "https://reference.langchain.com/python/langgraph/types/Command")],
    "07-RAG-통합과-시각화": [("LangGraph Graph API 사용법", "https://docs.langchain.com/oss/python/langgraph/use-graph-api"), ("LangChain 모델 초기화", "https://docs.langchain.com/oss/python/concepts/providers-and-models")],
}


def md(source: str) -> dict:
    return {"cell_type": "markdown", "id": "", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "id": "", "metadata": {}, "outputs": [], "source": source.splitlines(keepends=True)}


RETURN_HINTS = {
    "normalize": "dict",
    "make_query": "dict",
    "expand": "dict",
    "inspect_score": "dict",
    "generate": "dict",
    "request_more": "dict",
    "reply": "dict",
    "dispatch": "list[Send]",
    "inspect_document": "dict",
    "load_pages": "dict",
    "dense_search": "dict",
    "sparse_search": "dict",
    "rrf_pair": "list[int]",
    "fuse": "dict",
    "rerank": "dict",
}


def add_return_hints(source: str) -> str:
    def replace(match: re.Match[str]) -> str:
        name, arguments = match.group(1), match.group(2)
        return f"def {name}({arguments}) -> {RETURN_HINTS.get(name, 'dict')}:"
    return re.sub(r"^def ([A-Za-z_][A-Za-z0-9_]*)\(([^\n]*)\):$", replace, source, flags=re.MULTILINE)


def cell_note(heading: str) -> str:
    if "설치" in heading or "환경 준비" in heading:
        return "필요한 패키지를 고정 버전으로 설치합니다. 출력에서 LangGraph 버전 또는 API 키의 존재 여부만 확인합니다."
    if "정의" in heading:
        return f"다음 코드에서 {heading}에 필요한 형식과 함수를 선언합니다. 이 셀은 정의를 준비하며, 값은 이어지는 실행 셀에서 확인합니다."
    if "시각화" in heading or "Mermaid" in heading:
        return "컴파일한 그래프에서 Mermaid 문자열을 생성합니다. 출력에서 노드 이름과 연결 방향을 확인합니다."
    if "저장" in heading:
        return "실제 실행 결과를 다음 챕터가 읽을 JSON 파일로 저장합니다. 출력에서 저장 경로와 실행 시간을 확인합니다."
    if "비교" in heading or "바꿔" in heading:
        return f"{heading} 조건으로 값을 하나만 변경합니다. 나란히 출력된 두 결과에서 달라진 항목을 확인합니다."
    if "컴파일" in heading:
        return "노드와 엣지를 연결한 뒤 실행 가능한 그래프로 컴파일합니다. 다음 셀에서 이 그래프를 호출합니다."
    return f"{heading} 단계를 실행합니다. 출력된 상태 값과 코드에서 반환한 키를 서로 대조합니다."


def cell_comment(heading: str) -> str:
    if "정의" in heading:
        return f"{heading}에 사용할 상태 형식과 함수를 선언합니다."
    if "설치" in heading or "환경 준비" in heading:
        return "노트북을 독립 실행할 수 있도록 패키지와 환경을 준비합니다."
    if "시각화" in heading or "Mermaid" in heading:
        return "컴파일된 그래프의 실제 노드와 엣지를 Mermaid 문자열로 확인합니다."
    if "저장" in heading:
        return "검색·생성 결과와 실행 정보를 재사용할 JSON 파일로 저장합니다."
    if "비교" in heading or "바꿔" in heading:
        return "한 조건만 바꾸고 나머지 입력을 유지해 결과 차이를 비교합니다."
    return f"{heading} 단계의 연산을 실행하고 반환된 상태 값을 확인합니다."


def notebook(title: str, question: str, cells: list[tuple[str, str]]) -> dict:
    items = [md(f"# {title}\n\n{question}"), md("## 실행 환경 준비\n\nPython 3.12 새 커널에서 첫 셀부터 실행합니다. 설치 셀은 이 노트북에 필요한 버전을 고정합니다.")]
    for heading, source in cells:
        commented = f"# {cell_comment(heading)}\n{add_return_hints(source)}"
        items.extend([md(f"## {heading}\n\n{cell_note(heading)}"), code(commented)])
    for index, cell in enumerate(items, 1):
        cell["id"] = f"cell-{index:02d}"
    return {
        "cells": items,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "lesson_format": "experiment",
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


INSTALL = "%pip install -q langgraph==1.2.11 langchain==1.4.0 langchain-openai==1.6.1 python-dotenv==1.2.3 scikit-learn==1.9.0\nfrom importlib.metadata import version\nprint('Python 패키지 준비 완료')\nprint('langgraph', version('langgraph'))"


LESSONS = {
"01-StateGraph와-노드-엣지": {
"title": "StateGraph와 노드·엣지",
"question": "파이썬 함수 나열을 상태 그래프로 옮기면 실행 순서를 어떻게 읽을 수 있을까요?",
"goals": ["StateGraph의 상태, 노드, 엣지를 코드에서 구분할 수 있습니다.", "START와 END를 포함한 순차 그래프를 컴파일하고 실행할 수 있습니다.", "실행 흔적과 Mermaid 문자열을 읽어 실제 실행 순서를 확인할 수 있습니다."],
"why": "Part 3에서 만든 RAG는 문서 읽기, 검색, 병합, 재정렬, 생성 함수를 차례로 호출했습니다. 단계가 두세 개일 때는 함수 나열도 읽을 수 있습니다. 조건에 따라 건너뛰거나 되돌아가는 단계가 생기면 호출 순서가 여러 곳에 흩어집니다. LangGraph는 상태와 실행 순서를 하나의 그래프로 선언해 이 문제를 다룹니다.",
"prior": "Ch12의 통합 실습은 질문을 받고 검색 결과와 출처를 만든 뒤 답변을 생성했습니다. 이번 절은 그 처리 단계에서 모델 호출을 제외하고, 질문 정리와 검색어 작성이라는 두 함수를 그래프에 배치합니다. 앞 노트북의 변수에는 의존하지 않습니다.",
"concept": "지하철 노선도에서 역은 작업이고 선은 이동 순서입니다. LangGraph의 상태(State)는 그래프 실행 동안 노드들이 함께 읽고 갱신하는 데이터입니다. 노드(node)는 상태를 읽어 일부 값을 반환하는 함수이고, 엣지(edge)는 다음 노드를 정하는 연결입니다. StateGraph는 이 세 요소를 모아 실행 가능한 그래프를 만드는 빌더입니다. START는 입력이 들어오는 가상 시작점이고 END는 더 실행할 노드가 없음을 나타내는 가상 끝점입니다. compile()은 선언한 노드 이름과 연결을 확인하고 invoke()할 수 있는 실행 객체를 반환합니다.",
"observe": "실행 결과의 trace에는 normalize와 make_query가 차례로 남습니다. Mermaid 출력에서도 START에서 normalize, make_query, END로 이어지는 화살표가 나타납니다. 노드를 등록한 순서가 실행 순서를 정하는 것이 아니라 add_edge로 선언한 연결이 실행 순서를 정합니다.",
"notes": ["노드는 전체 상태를 복사해 반환하지 않고 바꿀 키만 반환할 수 있습니다.", "compile() 전의 객체는 설계도이며 compile() 결과가 실행 객체입니다.", "이 절의 그래프는 모델이 경로를 정하지 않습니다. 코드로 적은 고정 엣지가 경로를 정합니다."],
"next": "다음 절에서는 각 노드가 반환한 일부 값이 기존 상태에 어떻게 반영되는지 확인합니다.",
"quiz": [("노드와 엣지는 각각 무엇인가요?", "노드는 상태를 읽고 갱신을 반환하는 함수이며, 엣지는 다음에 실행할 노드를 정하는 연결입니다."), ("compile()은 왜 필요한가요?", "그래프 구조를 확인하고 invoke()할 실행 객체를 만들기 위해 필요합니다."), ("노드 등록 순서가 실행 순서인가요?", "아닙니다. 실행 순서는 START부터 이어진 엣지가 정합니다.")],
"cells": [
 ("패키지 설치와 버전 확인", INSTALL),
 ("상태와 두 노드 정의", "from typing_extensions import TypedDict\nfrom langgraph.graph import StateGraph, START, END\n\nclass FlowState(TypedDict):\n    question: str\n    query: str\n    trace: list[str]\n\ndef normalize(state: FlowState):\n    return {'question': state['question'].strip(), 'trace': ['normalize']}\n\ndef make_query(state: FlowState):\n    query = state['question'].replace('?', '').replace('요', '')\n    return {'query': query, 'trace': state['trace'] + ['make_query']}\nprint('노드 2개 정의 완료')"),
 ("그래프 조립과 컴파일", "builder = StateGraph(FlowState)\nbuilder.add_node('normalize', normalize)\nbuilder.add_node('make_query', make_query)\nbuilder.add_edge(START, 'normalize')\nbuilder.add_edge('normalize', 'make_query')\nbuilder.add_edge('make_query', END)\ngraph = builder.compile()\nprint('컴파일 완료')"),
 ("실행 결과 관찰", "result = graph.invoke({'question': '  대출 기간은 며칠인가요?  ', 'query': '', 'trace': []})\nprint('질문:', result['question'])\nprint('검색어:', result['query'])\nprint('실행 흔적:', result['trace'])\nassert result['trace'] == ['normalize', 'make_query']"),
 ("질문 하나를 바꿔 비교", "second = graph.invoke({'question': '  운영 시간은 언제인가요?  ', 'query': '', 'trace': []})\nprint('첫 검색어:', result['query'])\nprint('바꾼 검색어:', second['query'])\nprint('같은 실행 흔적:', second['trace'])\nassert second['query'] != result['query']\nassert second['trace'] == result['trace']"),
 ("Mermaid로 구조 확인", "mermaid = graph.get_graph().draw_mermaid()\nprint(mermaid)\nassert 'normalize' in mermaid and 'make_query' in mermaid")],
},
"02-State-갱신": {
"title": "State 갱신과 리듀서",
"question": "노드가 같은 상태 키를 여러 번 반환하면 값은 덮어쓸까요, 누적할까요?",
"goals": ["상태 스키마가 노드 입력과 출력의 키·값 형식을 정의하는 방식을 설명할 수 있습니다.", "기본 덮어쓰기와 리듀서 누적의 차이를 실행 결과로 비교할 수 있습니다.", "노드가 일부 키만 반환하는 갱신 방식을 적용할 수 있습니다."],
"why": "검색 단계는 documents를 만들고 생성 단계는 answer를 만듭니다. 모든 함수가 전체 딕셔너리를 다시 만들면 빠진 키나 오래된 값을 섞기 쉽습니다. LangGraph의 노드는 자신이 맡은 키의 갱신값만 반환합니다. 같은 키에 여러 갱신이 모일 때는 리듀서가 합치는 규칙을 담당합니다.",
"prior": "앞 절에서 StateGraph, 노드, 엣지, compile(), invoke()를 사용했습니다. 이번 절도 같은 순차 그래프를 사용하지만 상태 키별 갱신 규칙에 초점을 맞춥니다.",
"concept": "공용 화이트보드의 칸마다 쓰기 규칙이 다르다고 생각해 봅니다. query 키는 새 값으로 교체하고 log 키는 새 항목을 뒤에 붙이도록 선언합니다. TypedDict는 상태에 어떤 키와 값 형식이 있는지 표현합니다. 리듀서(reducer)는 한 상태 키의 기존 값과 새 갱신값을 받아 최종 값을 만드는 함수입니다. Annotated[list[str], operator.add]는 두 목록을 이어 붙이도록 지정하므로 각 노드가 반환한 목록이 누적됩니다. 리듀서가 없는 키는 기본적으로 새 값이 기존 값을 덮어씁니다.",
"observe": "첫 노드는 query를 '도서 대출 기간'으로 바꾸고 log에 normalize를 보냅니다. 둘째 노드는 query를 '도서 대출 기간 정책'으로 다시 바꾸고 log에 expand를 보냅니다. 최종 query에는 마지막 값만 남지만 log에는 두 항목이 모두 남습니다. 키마다 규칙이 독립적으로 적용된다는 증거입니다.",
"notes": ["리듀서는 상태 전체가 아니라 Annotated로 표시한 키 하나에 적용됩니다.", "목록을 누적할 때 노드가 기존 목록을 다시 포함하면 항목이 중복될 수 있습니다.", "동시에 실행되는 노드가 같은 비리듀서 키를 갱신하면 충돌이 발생할 수 있으므로 병렬 구조에서는 합치는 규칙을 먼저 정합니다."],
"next": "다음 절에서는 상태의 점수에 따라 서로 다른 노드로 이동하는 조건부 엣지를 만듭니다.",
"quiz": [("리듀서가 없는 키는 어떻게 갱신되나요?", "새 갱신값이 기존 값을 덮어씁니다."), ("operator.add 리듀서를 쓴 목록은 어떻게 되나요?", "기존 목록과 새 목록을 이어 붙여 누적합니다."), ("노드가 전체 상태를 반환해야 하나요?", "아닙니다. 자신이 바꾸는 키만 반환할 수 있습니다.")],
"cells": [
 ("패키지 설치와 버전 확인", INSTALL),
 ("서로 다른 갱신 규칙 선언", "import operator\nfrom typing import Annotated\nfrom typing_extensions import TypedDict\nfrom langgraph.graph import StateGraph, START, END\n\nclass UpdateState(TypedDict):\n    query: str\n    log: Annotated[list[str], operator.add]\n\ndef normalize(state: UpdateState):\n    return {'query': state['query'].strip(), 'log': ['normalize']}\n\ndef expand(state: UpdateState):\n    return {'query': state['query'] + ' 정책', 'log': ['expand']}") ,
 ("순차 그래프 컴파일", "builder = StateGraph(UpdateState)\nbuilder.add_node('normalize', normalize)\nbuilder.add_node('expand', expand)\nbuilder.add_edge(START, 'normalize')\nbuilder.add_edge('normalize', 'expand')\nbuilder.add_edge('expand', END)\ngraph = builder.compile()\nprint('갱신 그래프 준비 완료')"),
 ("덮어쓰기와 누적 비교", "result = graph.invoke({'query': '  도서 대출 기간  ', 'log': []})\nprint('최종 query:', result['query'])\nprint('누적 log:', result['log'])\nassert result['query'] == '도서 대출 기간 정책'\nassert result['log'] == ['normalize', 'expand']"),
 ("초기 기록을 포함해 다시 실행", "second = graph.invoke({'query': '운영 시간', 'log': ['input']})\nprint(second)\nassert second['log'] == ['input', 'normalize', 'expand']")],
},
"03-조건부-엣지": {
"title": "조건부 엣지로 경로 선택",
"question": "검색 점수가 기준을 넘는지에 따라 답변 생성과 추가 자료 요청 중 어느 노드로 이동하게 할까요?",
"goals": ["조건 함수와 작업 노드의 역할을 구분할 수 있습니다.", "add_conditional_edges로 코드가 정한 분기를 구성할 수 있습니다.", "같은 그래프에 두 입력을 넣어 서로 다른 경로를 확인할 수 있습니다."],
"why": "RAG에서는 검색 결과가 충분할 때 답을 만들고 부족할 때 추가 자료를 요청해야 합니다. if문을 호출 코드 여러 곳에 두면 경로를 한눈에 보기 어렵습니다. 조건부 엣지는 상태를 읽는 조건 함수를 그래프의 연결 규칙으로 등록합니다.",
"prior": "Ch11에서 검색 품질을 점수로 측정했고 Ch12에서 후보를 재정렬했습니다. 이번 절은 검색을 다시 구현하지 않고 0과 1 사이의 rerank_score가 이미 상태에 있다고 가정합니다. 경로 판단은 모델이 아니라 코드의 임계값 비교가 담당합니다.",
"concept": "택배 분류대는 송장 값을 읽고 상자를 서로 다른 컨베이어로 보냅니다. 조건부 엣지(conditional edge)는 한 노드가 끝난 뒤 상태를 읽어 다음 노드 이름을 반환하는 연결입니다. add_conditional_edges(source, path, path_map)는 source 뒤에서 path 함수를 호출하고 그 반환값을 실제 노드 이름으로 대응시킵니다. Literal 반환형이나 path_map을 적으면 시각화할 때도 가능한 목적지가 분명하게 표시됩니다.",
"observe": "점수 0.82는 generate 경로를 지나 '근거로 답변 생성'을 반환합니다. 점수 0.41은 request_more 경로를 지나 '추가 자료 요청'을 반환합니다. 같은 그래프와 같은 임계값을 사용하고 점수 하나만 바꾸었으므로 경로 차이는 조건 함수의 비교 결과에서 생겼습니다.",
"notes": ["조건 함수는 상태를 갱신하지 않고 다음 경로를 고르는 데 집중합니다.", "가능한 목적지를 path_map이나 Literal로 제한하면 구조 검사와 그림 해석이 쉬워집니다.", "이 절의 분기는 사람이 작성한 score >= 0.7 조건입니다. 모델 자율 판단이나 도구 호출은 포함하지 않습니다."],
"next": "다음 절에서는 대화 메시지를 상태에 보존하는 add_messages 리듀서를 다룹니다.",
"quiz": [("조건 함수는 무엇을 반환하나요?", "다음 경로를 나타내는 값이나 노드 이름을 반환합니다."), ("분기 기준은 누가 정하나요?", "이 절에서는 코드에 작성한 임계값 비교가 정합니다."), ("두 실행에서 바꾼 값은 무엇인가요?", "rerank_score 하나만 0.82와 0.41로 바꿨습니다.")],
"cells": [
 ("패키지 설치와 버전 확인", INSTALL),
 ("상태와 분기 함수 정의", "from typing import Literal\nfrom typing_extensions import TypedDict\nfrom langgraph.graph import StateGraph, START, END\n\nclass RouteState(TypedDict):\n    rerank_score: float\n    route: str\n    answer: str\n\ndef inspect_score(state: RouteState):\n    return {'route': 'checked'}\n\ndef choose(state: RouteState) -> Literal['generate', 'request_more']:\n    return 'generate' if state['rerank_score'] >= 0.7 else 'request_more'") ,
 ("두 목적지 노드 정의", "def generate(state: RouteState):\n    return {'route': 'generate', 'answer': '근거로 답변 생성'}\n\ndef request_more(state: RouteState):\n    return {'route': 'request_more', 'answer': '추가 자료 요청'}\n\nbuilder = StateGraph(RouteState)\nbuilder.add_node('inspect_score', inspect_score)\nbuilder.add_node('generate', generate)\nbuilder.add_node('request_more', request_more)"),
 ("조건부 엣지 연결", "builder.add_edge(START, 'inspect_score')\nbuilder.add_conditional_edges('inspect_score', choose)\nbuilder.add_edge('generate', END)\nbuilder.add_edge('request_more', END)\ngraph = builder.compile()\nprint(graph.get_graph().draw_mermaid())"),
 ("점수 하나를 바꿔 경로 비교", "base = {'route': '', 'answer': ''}\nhigh = graph.invoke({**base, 'rerank_score': 0.82})\nlow = graph.invoke({**base, 'rerank_score': 0.41})\nprint('0.82:', high['route'], high['answer'])\nprint('0.41:', low['route'], low['answer'])\nassert high['route'] == 'generate'\nassert low['route'] == 'request_more'")],
},
"04-add_messages-리듀서": {
"title": "add_messages 메시지 리듀서",
"question": "사람과 모델의 메시지를 객체 형식으로 누적하면서 기존 메시지를 어떻게 수정할까요?",
"goals": ["add_messages가 새 메시지를 추가하고 같은 ID의 메시지를 교체하는 방식을 설명할 수 있습니다.", "HumanMessage와 AIMessage를 그래프 상태에 저장할 수 있습니다.", "AIMessage.text로 텍스트를 읽을 수 있습니다."],
"why": "대화형 RAG는 현재 질문만으로 검색어를 만들기 어려울 때 이전 대화를 참고합니다. 문자열 목록만 이어 붙이면 메시지 역할과 ID를 잃기 쉽습니다. add_messages는 LangChain 메시지 객체를 상태에 유지하고, 같은 ID로 수정된 메시지는 기존 항목을 교체합니다.",
"prior": "02절에서 리듀서가 상태 키의 갱신값을 합친다는 원리를 확인했습니다. 이번 절은 메시지 목록에 맞춘 내장 리듀서 add_messages를 사용합니다. 모델 API를 호출하지 않고 AIMessage 객체를 직접 만들어 상태 처리만 관찰합니다.",
"concept": "회의록에 발언을 시간순으로 추가하되 잘못 적힌 발언은 발언 번호로 찾아 고친다고 생각해 봅니다. add_messages는 새 ID의 메시지를 뒤에 추가하고 기존 메시지와 ID가 같은 메시지가 들어오면 그 위치의 메시지를 교체합니다. HumanMessage는 사용자의 발언, AIMessage는 모델의 응답을 나타냅니다. AnyMessage는 이 메시지들의 공통 형식을 표현합니다. AIMessage.text는 content가 문자열이나 콘텐츠 블록이어도 텍스트 부분을 읽기 위한 속성입니다.",
"observe": "첫 그래프 실행 결과에는 human과 ai 두 메시지가 있습니다. 이어서 add_messages 리듀서를 직접 호출해 같은 ID의 수정 메시지를 합치면 기존 human 메시지가 교체됩니다. 총 메시지 수는 둘로 유지되고 첫 내용만 달라집니다.",
"notes": ["operator.add는 같은 ID도 단순히 뒤에 추가하지만 add_messages는 ID를 보고 교체할 수 있습니다.", "메시지 내용은 점 표기법인 message.content 또는 AIMessage.text로 읽습니다.", "이번 절의 AIMessage는 상태 처리를 보기 위한 로컬 객체이며 실제 모델 응답이 아닙니다."],
"next": "다음 절에서는 입력 항목 수만큼 작업을 동적으로 만들어 병렬로 보내는 Send를 사용합니다.",
"quiz": [("add_messages가 단순 목록 덧셈과 다른 점은 무엇인가요?", "같은 ID의 메시지를 기존 위치에서 교체할 수 있습니다."), ("AIMessage.text는 무엇을 반환하나요?", "AIMessage의 텍스트 내용을 반환합니다."), ("이번 절은 모델 API를 호출했나요?", "아닙니다. 메시지 상태 처리만 확인하기 위해 객체를 직접 만들었습니다.")],
"cells": [
 ("패키지 설치와 버전 확인", INSTALL),
 ("메시지 상태와 응답 노드 정의", "from typing import Annotated\nfrom typing_extensions import TypedDict\nfrom langchain.messages import AnyMessage, HumanMessage, AIMessage\nfrom langgraph.graph import StateGraph, START, END\nfrom langgraph.graph.message import add_messages\n\nclass ChatState(TypedDict):\n    messages: Annotated[list[AnyMessage], add_messages]\n\ndef reply(state: ChatState):\n    question = state['messages'][-1].content\n    return {'messages': [AIMessage(content=f'확인한 질문: {question}', id='a1')]}") ,
 ("메시지 그래프 실행", "builder = StateGraph(ChatState)\nbuilder.add_node('reply', reply)\nbuilder.add_edge(START, 'reply')\nbuilder.add_edge('reply', END)\ngraph = builder.compile()\nfirst = graph.invoke({'messages': [HumanMessage(content='대출 기간?', id='h1')]})\nfor message in first['messages']:\n    print(message.type, message.id, message.content)"),
 ("AIMessage.text 확인", "answer_message = first['messages'][-1]\nprint('AIMessage.text:', answer_message.text)\nassert answer_message.text == '확인한 질문: 대출 기간?'"),
 ("같은 ID 메시지 교체 비교", "revised = add_messages(\n    first['messages'],\n    [HumanMessage(content='도서 대출 기간은?', id='h1')],\n)\nfor message in revised:\n    print(message.type, message.id, message.content)\nassert len(revised) == 2\nassert revised[0].content == '도서 대출 기간은?'")],
},
"05-Send-동적-팬아웃": {
"title": "Send로 동적 팬아웃",
"question": "검색된 문서 수가 실행할 때마다 달라도 각 문서를 같은 노드로 보내고 결과를 모을 수 있을까요?",
"goals": ["Send가 목적지 노드와 그 노드에 전달할 상태를 함께 지정한다는 점을 설명할 수 있습니다.", "입력 개수에 따라 동적으로 늘어나는 맵(map) 단계를 구성할 수 있습니다.", "리듀서로 팬아웃 결과를 하나의 상태에 모을 수 있습니다."],
"why": "검색 결과가 세 건이면 세 문서를 확인하고 다섯 건이면 다섯 문서를 확인해야 합니다. 문서 수만큼 노드를 미리 등록할 수는 없습니다. Send는 조건부 엣지에서 같은 노드를 서로 다른 입력으로 여러 번 호출해 동적인 맵-리듀스(map-reduce) 흐름을 만듭니다.",
"prior": "Ch12에서는 여러 검색 후보를 RRF로 합친 뒤 재정렬했습니다. 이번 절은 세 개의 짧은 문서 조각을 입력으로 사용해 각 조각의 글자 수와 ID를 병렬 작업으로 계산합니다. 실제 검색은 7절에서 연결합니다.",
"concept": "우체국이 편지 묶음을 주소별 배달원에게 나눠 주고 완료 보고를 다시 모으는 상황과 같습니다. 팬아웃(fan out)은 한 흐름을 여러 작업으로 나누는 구조입니다. Send(node, arg)는 실행할 노드 이름과 그 실행에만 전달할 상태를 담습니다. 조건 함수가 Send 목록을 반환하면 항목 수만큼 노드 실행이 만들어집니다. 여러 실행이 같은 results 키를 갱신하므로 operator.add 리듀서가 결과 목록을 합칩니다.",
"observe": "문서 세 건을 입력하면 inspect_document 노드가 세 번 실행되고 results에 세 딕셔너리가 모입니다. 문서 한 건으로 다시 실행하면 결과도 한 건입니다. 그래프의 노드 수는 바뀌지 않았지만 실행 작업 수가 입력 길이에 따라 달라졌습니다.",
"notes": ["Send에 전달하는 arg는 목적지 노드가 읽을 수 있는 키를 포함해야 합니다.", "결과를 ID로 정렬하면 병렬 실행 결과의 순서가 달라도 같은 항목끼리 비교할 수 있습니다.", "동시에 같은 키를 갱신할 때는 합칠 리듀서가 필요합니다."],
"next": "다음 절에서는 한 노드가 상태를 갱신하면서 다음 목적지까지 함께 반환하는 Command를 사용합니다.",
"quiz": [("Send의 두 인자는 무엇인가요?", "목적지 노드 이름과 그 노드에 전달할 상태입니다."), ("작업 수는 무엇이 정하나요?", "조건 함수가 반환한 Send 객체의 수가 정합니다."), ("results에 리듀서가 필요한 이유는 무엇인가요?", "여러 실행이 반환한 목록을 하나로 합쳐야 하기 때문입니다.")],
"cells": [
 ("패키지 설치와 버전 확인", INSTALL),
 ("전체 상태와 작업 상태 정의", "import operator\nfrom typing import Annotated\nfrom typing_extensions import TypedDict\nfrom langgraph.graph import StateGraph, START, END\nfrom langgraph.types import Send\n\nclass OverallState(TypedDict):\n    documents: list[dict]\n    results: Annotated[list[dict], operator.add]\n\nclass DocumentState(TypedDict):\n    document: dict"),
 ("Send 목록과 작업 노드 정의", "def dispatch(state: OverallState):\n    return [Send('inspect_document', {'document': doc}) for doc in state['documents']]\n\ndef inspect_document(state: DocumentState):\n    doc = state['document']\n    return {'results': [{'id': doc['id'], 'length': len(doc['text'])}]}\n\nbuilder = StateGraph(OverallState)\nbuilder.add_node('inspect_document', inspect_document)\nbuilder.add_conditional_edges(START, dispatch)\nbuilder.add_edge('inspect_document', END)\ngraph = builder.compile()"),
 ("세 문서로 팬아웃", "documents = [\n    {'id': 'E01', 'text': '대출은 7권까지 가능합니다.'},\n    {'id': 'E02', 'text': '대출 기간은 14일입니다.'},\n    {'id': 'E03', 'text': '반납함은 출입구에 있습니다.'},\n]\nresult = graph.invoke({'documents': documents, 'results': []})\nordered = sorted(result['results'], key=lambda item: item['id'])\nprint(ordered)\nassert len(ordered) == 3"),
 ("입력 수 하나로 비교", "single = graph.invoke({'documents': documents[:1], 'results': []})\nprint(single['results'])\nassert len(single['results']) == 1")],
},
"06-Command-갱신과-이동": {
"title": "Command로 상태 갱신과 이동",
"question": "한 노드가 판정 결과를 상태에 기록하면서 다음 노드까지 함께 정할 수 있을까요?",
"goals": ["Command의 update와 goto 역할을 구분할 수 있습니다.", "Command 반환형에 가능한 목적지를 표시할 수 있습니다.", "조건부 엣지와 Command를 사용할 상황을 구분할 수 있습니다."],
"why": "어떤 노드는 다음 경로를 고를 때 그 판단 근거도 상태에 남겨야 합니다. 조건 함수와 갱신 노드를 따로 두면 같은 조건을 두 번 계산할 수 있습니다. Command는 노드가 상태 갱신과 이동 지시를 하나의 반환값으로 표현하게 합니다.",
"prior": "3절의 조건부 엣지는 inspect_score 노드 뒤에서 별도의 choose 함수가 목적지를 골랐습니다. 이번 절은 같은 점수 기준을 route 노드 안에서 계산하고, 선택한 이유와 목적지를 함께 반환합니다.",
"concept": "심사 담당자가 서류에 판정 이유를 기록하고 다음 담당 부서로 직접 보내는 상황과 같습니다. Command(update=..., goto=...)는 상태에 적용할 갱신과 다음에 실행할 노드를 함께 담습니다. Command[Literal['generate', 'request_more']] 반환형은 그래프 시각화 도구가 가능한 목적지를 표시하게 합니다. update는 일반 노드 반환 딕셔너리와 같은 방식으로 리듀서의 적용을 받습니다.",
"observe": "점수 0.82에서는 decision이 sufficient로 갱신되고 generate로 이동합니다. 점수 0.41에서는 decision이 insufficient로 갱신되고 request_more로 이동합니다. 최종 상태에는 경로뿐 아니라 판단 결과가 함께 남습니다.",
"notes": ["이동만 필요하면 조건부 엣지가 구조를 더 분명하게 보여 줄 수 있습니다.", "상태 갱신과 이동을 하나의 판단 단계에서 만들 때 Command가 중복 계산을 줄입니다.", "반환형의 Literal에 가능한 목적지를 적어야 시각화가 목적지를 정확히 표시합니다."],
"next": "마지막 절에서는 Ch12의 실제 데이터와 통합 로그를 읽어 검색, 병합, 재정렬, 생성을 그래프로 연결하고 Mermaid 구조를 확인합니다.",
"quiz": [("update는 무엇을 담나요?", "현재 상태에 적용할 키별 갱신값을 담습니다."), ("goto는 무엇을 담나요?", "다음에 실행할 노드 이름이나 Send를 담습니다."), ("조건부 엣지 대신 Command가 알맞은 경우는 언제인가요?", "하나의 판단 단계에서 상태 갱신과 다음 이동을 함께 정할 때 알맞습니다.")],
"cells": [
 ("패키지 설치와 버전 확인", INSTALL),
 ("상태와 Command 노드 정의", "from typing import Literal\nfrom typing_extensions import TypedDict\nfrom langgraph.graph import StateGraph, START, END\nfrom langgraph.types import Command\n\nclass DecisionState(TypedDict):\n    score: float\n    decision: str\n    answer: str\n\ndef route(state: DecisionState) -> Command[Literal['generate', 'request_more']]:\n    enough = state['score'] >= 0.7\n    return Command(\n        update={'decision': 'sufficient' if enough else 'insufficient'},\n        goto='generate' if enough else 'request_more',\n    )"),
 ("목적지 노드와 그래프 정의", "def generate(state: DecisionState):\n    return {'answer': '선택한 근거로 답변을 생성합니다.'}\n\ndef request_more(state: DecisionState):\n    return {'answer': '답변 전에 자료를 추가로 확인합니다.'}\n\nbuilder = StateGraph(DecisionState)\nbuilder.add_node('route', route)\nbuilder.add_node('generate', generate)\nbuilder.add_node('request_more', request_more)\nbuilder.add_edge(START, 'route')\nbuilder.add_edge('generate', END)\nbuilder.add_edge('request_more', END)\ngraph = builder.compile()"),
 ("두 경로 실행", "base = {'decision': '', 'answer': ''}\nhigh = graph.invoke({**base, 'score': 0.82})\nlow = graph.invoke({**base, 'score': 0.41})\nprint('0.82:', high['decision'], high['answer'])\nprint('0.41:', low['decision'], low['answer'])\nassert high['decision'] == 'sufficient'\nassert low['decision'] == 'insufficient'"),
 ("가능한 이동 시각화", "mermaid = graph.get_graph().draw_mermaid()\nprint(mermaid)\nassert 'generate' in mermaid and 'request_more' in mermaid")],
},
"07-RAG-통합과-시각화": {
"title": "Ch12 RAG 통합과 시각화",
"question": "Ch12의 실제 문서와 통합 로그를 읽어 검색, 병합, 재정렬, 생성을 하나의 그래프로 연결할 수 있을까요?",
"goals": ["Ch12 통합 로그의 질문과 출처를 입력으로 이어받을 수 있습니다.", "실제 문서 검색, 두 순위의 RRF 병합, 후보 재정렬, 모델 생성을 노드로 연결할 수 있습니다.", "get_graph().draw_mermaid() 출력과 실행 trace를 대조할 수 있습니다."],
"why": "앞 여섯 절에서는 작은 데이터로 그래프 구성 요소를 하나씩 확인했습니다. 이제 Part 3에서 만든 RAG 흐름을 그대로 가져와 각 함수를 노드에 대응시킵니다. 저장된 Ch12 답변을 출력하는 방식으로는 그래프가 실제 생성을 수행했는지 확인할 수 없습니다. 따라서 통합 로그에서는 질문과 이전 출처만 읽고, 이번 그래프가 문서 검색부터 답변 생성까지 다시 실행합니다.",
# 2026-09-19 Ch 12 인계 처리(Ch 12 요약 §13-2): 아래 prior의 「검색된 E01·E02 쪽」이 사실과 달라 고쳤습니다.
# 실제 기록의 retrieved는 E01-P03-C02·E01-P03-C01·E01-P03-C06 세 건(부모가 모두 E01)이고,
# settings.reranker는 null, settings.context_selection은 matched-chunk-text(쪽이 아니라 문서 청크 본문)입니다.
# 개선본 문장은 qa/upgrade/author_07.py 와 _src/07-RAG-통합과-시각화.html b3 에 있습니다.
"prior": "Ch12의 runs/advanced-continuity-integrated-result.json에는 Q002 질문, 그 실행이 모델에 넣은 문서 청크 세 건(E01-P03-C02·E01-P03-C01·E01-P03-C06, 부모가 모두 E01), 실제 모델 응답, 고정 설정이 있습니다. 그 설정의 reranker는 null이고 context_selection은 matched-chunk-text라 넣은 것은 쪽이 아니라 문서 청크 본문입니다. data/advanced-documents.json에는 제공 PDF에서 만든 부모 문서와 문서 청크가 있습니다. 배포 묶음에 포함된 이 두 Ch12 파일을 상대 경로로 읽으므로 개인 경로가 필요하지 않습니다.",
"concept": "공장 공정표에서 원료가 어느 기계를 거치고 어떤 검사 결과가 다음 단계로 전달되는지 표시하는 것과 같습니다. load_pages는 Ch12 문서 목록으로 제공 PDF를 읽습니다. dense_search는 OpenAI 임베딩, sparse_search는 Kiwi BM25 점수를 실제로 계산합니다. fuse는 두 순위를 reciprocal rank fusion(RRF)으로 합칩니다. rerank는 CrossEncoder로 상위 후보를 다시 정렬합니다. generate는 선택한 본문과 출처를 메시지에 넣고 init_chat_model().invoke()를 실제 호출한 뒤 AIMessage.text를 상태에 저장합니다. 각 노드는 하나의 처리 단계만 맡고 필요한 상태 값만 갱신합니다.",
"observe": "화면 출력에서 입력 질문이 Ch12 Q002와 같은지, 융합 뒤 선택된 문서 순서와 재정렬된 E01 본문에 7권과 14일이 포함되는지 확인합니다. RRF 점수는 함수 내부 계산에만 사용하고 화면에 출력하지 않습니다. 모델 출력은 실행 시점에 달라질 수 있으므로 저장된 Ch12 response와 글자가 같은지를 성공 조건으로 삼지 않습니다. 대신 생성 노드가 선택한 실제 본문과 [E01 p.3] 출처를 전달하고 새 AIMessage.text를 반환했는지 확인합니다. trace와 Mermaid에는 load_pages, dense_search, sparse_search, fuse, rerank, generate 순서가 모두 나타납니다.",
"notes": ["모델 출력은 실행할 때마다 문장 표현이 달라질 수 있습니다. 선택 문서에 E01 3쪽이 있고 답변에 [E01 p.3]이 있는지 별도로 검사합니다.", "OpenAI 임베딩 점수와 Kiwi BM25 점수의 크기는 직접 비교하지 않고 각각의 순위만 RRF 입력으로 사용합니다.", "RRF와 재정렬 후보가 적은 한 질문의 스모크 실행입니다. 검색 품질과 생성 품질의 전체 평가는 Ch11·Ch15 지표로 따로 수행합니다.", "OPENAI_API_KEY는 상위 .env에서 읽고 존재 여부만 확인하며 값은 출력하지 않습니다."],
"next": "Ch14에서는 이 그래프에 대화형 질문 재작성, 다중 질문, 자기 교정 분기를 추가하되 판단은 여전히 코드의 조건으로 작성합니다.",
"quiz": [("저장된 Ch12 답변을 그대로 출력하지 않는 이유는 무엇인가요?", "이번 그래프의 generate 노드가 실제 모델 호출을 수행했다는 증거가 되지 않기 때문입니다."), ("RRF는 무엇을 합치나요?", "서로 다른 검색 방법이 만든 순위의 역순위 점수를 합칩니다."), ("Mermaid와 trace를 함께 보는 이유는 무엇인가요?", "선언한 구조와 실제 실행 순서가 서로 맞는지 확인하기 위해서입니다."), ("이번 결과만으로 검색 품질이 좋아졌다고 말할 수 있나요?", "아닙니다. 한 질문의 통합 스모크 실행이며 전체 품질 평가는 별도 평가셋과 지표가 필요합니다.")],
"cells": [
 ("패키지 설치와 환경 준비", INSTALL + "\nimport os\nfrom pathlib import Path\nfrom dotenv import load_dotenv\nfor folder in [Path.cwd(), *Path.cwd().parents]:\n    if (folder / '.env').is_file():\n        load_dotenv(folder / '.env'); break\nassert os.getenv('OPENAI_API_KEY'), 'OPENAI_API_KEY가 필요합니다.'\nprint('API 키 존재 여부 확인 완료')"),
 ("Ch12 입력과 문서 읽기", "import json\nfrom pathlib import Path\nBASE = Path('labs/part3/ch12-retrieval-tuning')\nrun = json.loads((BASE / 'runs/advanced-continuity-integrated-result.json').read_text())\ndataset = json.loads((BASE / 'data/advanced-documents.json').read_text())\nquestion = run['question']\ndocuments = dataset['chunks']\nprint('질문:', question)\nprint('문서 청크:', len(documents), '이전 검색:', [x['doc_id'] for x in run['retrieved']])"),
 ("검색과 병합 함수 정의", "import re\nfrom sklearn.feature_extraction.text import TfidfVectorizer\n\ndef tokens(text):\n    return set(re.findall(r'[가-힣A-Za-z0-9]+', text.lower()))\n\ndef rank_docs(question, docs):\n    texts = [d['text'] for d in docs]\n    matrix = TfidfVectorizer(analyzer='char', ngram_range=(2, 4)).fit_transform([question, *texts])\n    dense = (matrix[1:] @ matrix[0].T).toarray().ravel()\n    sparse = [len(tokens(question) & tokens(text)) for text in texts]\n    dense_rank = sorted(range(len(docs)), key=lambda i: dense[i], reverse=True)[:8]\n    sparse_rank = sorted(range(len(docs)), key=lambda i: sparse[i], reverse=True)[:8]\n    return dense_rank, sparse_rank\n\ndef rrf(*rankings, k=60):\n    scores = {}\n    for ranking in rankings:\n        for rank, index in enumerate(ranking, 1): scores[index] = scores.get(index, 0) + 1 / (k + rank)\n    return sorted(scores, key=scores.get, reverse=True), scores"),
 ("RAG 그래프 노드 정의", "from typing_extensions import TypedDict\nfrom langgraph.graph import StateGraph, START, END\nfrom langchain.chat_models import init_chat_model\nfrom langchain.messages import HumanMessage, SystemMessage\n\nclass RAGState(TypedDict):\n    question: str; docs: list[dict]; dense: list[int]; sparse: list[int]\n    fused: list[int]; selected: list[dict]; answer: str; trace: list[str]\n\ndef search(state):\n    dense, sparse = rank_docs(state['question'], state['docs'])\n    return {'dense': dense, 'sparse': sparse, 'trace': state['trace'] + ['search']}\n\ndef fuse(state):\n    fused, _ = rrf(state['dense'], state['sparse'])\n    return {'fused': fused, 'trace': state['trace'] + ['fuse']}\n\ndef rerank(state):\n    q = tokens(state['question'])\n    docs = [state['docs'][i] for i in state['fused'][:8]]\n    docs.sort(key=lambda d: len(q & tokens(d['text'])), reverse=True)\n    return {'selected': docs[:2], 'trace': state['trace'] + ['rerank']}"),
 ("실제 모델 생성과 그래프 실행", "def generate(state):\n    context = '\\n\\n'.join(f\"[{d['parent_id']} p.{d['page']}] {d['text']}\" for d in state['selected'])\n    model = init_chat_model('gpt-5.4-mini', model_provider='openai')\n    reply = model.invoke([SystemMessage('근거만 사용하고 문장 끝에 출처를 적습니다.'), HumanMessage(f\"질문: {state['question']}\\n근거:\\n{context}\")])\n    return {'answer': reply.text, 'trace': state['trace'] + ['generate']}\n\nb = StateGraph(RAGState)\nfor name, fn in [('search', search), ('fuse', fuse), ('rerank', rerank), ('generate', generate)]: b.add_node(name, fn)\nb.add_edge(START, 'search'); b.add_edge('search', 'fuse'); b.add_edge('fuse', 'rerank'); b.add_edge('rerank', 'generate'); b.add_edge('generate', END)\ngraph = b.compile()\nresult = graph.invoke({'question': question, 'docs': documents, 'dense': [], 'sparse': [], 'fused': [], 'selected': [], 'answer': '', 'trace': ['load_input']})\nprint('선택:', [(d['parent_id'], d['page']) for d in result['selected']])\nprint('답변:', result['answer']); print('실행 흔적:', result['trace'])\nassert result['answer'] and result['trace'][-1] == 'generate'"),
 ("질문 하나를 바꿔 검색 순위 비교", "changed_question = '주말 운영 시간은 언제인가요?'\nchanged_dense, changed_sparse = rank_docs(changed_question, documents)\nprint('원 질문 dense 1위:', result['docs'][result['dense'][0]]['chunk_id'])\nprint('변경 질문 dense 1위:', documents[changed_dense[0]]['chunk_id'])\nprint('변경 질문 sparse 1위:', documents[changed_sparse[0]]['chunk_id'])\nassert changed_dense and changed_sparse"),
 ("실제 실행 순서 시각화", "mermaid = graph.get_graph().draw_mermaid()\nprint(mermaid)\nfor node in ['search', 'fuse', 'rerank', 'generate']:\n    assert node in mermaid")],
},
}


# Ch12의 통합 설정을 축약하지 않고 실제 검색·병합·재정렬·생성 노드로 옮깁니다.
LESSONS["07-RAG-통합과-시각화"]["cells"] = [
    ("패키지 설치와 환경 준비", "%pip install -q langgraph==1.2.11 langchain==1.4.0 langchain-openai==1.6.1 python-dotenv==1.2.3 numpy==2.5.3 scikit-learn==1.9.0 pypdf==6.18.0 kiwipiepy==0.23.2 rank-bm25==0.2.2 sentence-transformers==6.0.1\nimport os\nfrom pathlib import Path\nfrom dotenv import load_dotenv\nfor folder in [Path.cwd(), *Path.cwd().parents]:\n    if (folder / '.env').is_file():\n        load_dotenv(folder / '.env'); break\nassert os.getenv('OPENAI_API_KEY'), 'OPENAI_API_KEY가 필요합니다.'\nprint('API 키 존재 여부 확인 완료')"),
    ("Ch12 질문과 문서 목록 읽기", "import json\nfrom importlib.metadata import version\nBASE = Path('labs/part3/ch12-retrieval-tuning')\nrun = json.loads((BASE / 'runs/advanced-continuity-integrated-result.json').read_text())\ndataset = json.loads((BASE / 'data/advanced-documents.json').read_text())\nquestion = run['question']\nparents = dataset['parents']\nprint('langgraph', version('langgraph'))\nprint('질문:', question, 'PDF:', len(parents))"),
    ("상태와 PDF 로딩 노드 정의", "from typing_extensions import TypedDict\nfrom langgraph.graph import StateGraph, START, END\nfrom pypdf import PdfReader\n\nclass RAGState(TypedDict):\n    question: str; parents: list[dict]; chunks: list[dict]\n    dense_scores: list[float]; sparse_scores: list[float]\n    candidates: list[int]; selected: list[dict]; answer: str; trace: list[str]\n\ndef load_pages(state: RAGState):\n    chunks = []\n    for parent in state['parents']:\n        pdf = Path('labs/data/rag-corpus') / parent['source']\n        for page, obj in enumerate(PdfReader(pdf).pages, 1):\n            chunks.append({'chunk_id': f\"{parent['doc_id']}-P{page:02d}-C01\", 'parent_id': parent['doc_id'], 'page': page, 'text': obj.extract_text() or ''})\n    return {'chunks': chunks, 'trace': state['trace'] + ['load_pages']}"),
    ("OpenAI 임베딩 검색 노드 정의", "import numpy as np\nfrom langchain_openai import OpenAIEmbeddings\nfrom sklearn.metrics.pairwise import cosine_similarity\n\ndef dense_search(state: RAGState):\n    embedding = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=256)\n    texts = [item['text'] for item in state['chunks']]\n    doc_vectors = np.array(embedding.embed_documents(texts))\n    query_vector = np.array(embedding.embed_query(state['question']))\n    scores = cosine_similarity([query_vector], doc_vectors)[0]\n    assert doc_vectors.shape == (len(texts), 256)\n    return {'dense_scores': scores.tolist(), 'trace': state['trace'] + ['dense_search']}"),
    ("Kiwi BM25 검색 노드 정의", "from kiwipiepy import Kiwi\nfrom rank_bm25 import BM25Okapi\n\ndef sparse_search(state: RAGState):\n    kiwi = Kiwi()\n    tokenized = [[token.form for token in kiwi.tokenize(item['text'])] for item in state['chunks']]\n    bm25 = BM25Okapi(tokenized)\n    query_tokens = [token.form for token in kiwi.tokenize(state['question'])]\n    scores = bm25.get_scores(query_tokens)\n    return {'sparse_scores': scores.tolist(), 'trace': state['trace'] + ['sparse_search']}"),
    ("RRF 병합 노드 정의", "def rrf_pair(first, second, rank_constant=60):\n    scores = {}\n    for ranking in (first, second):\n        for rank, index in enumerate(ranking, 1):\n            scores[index] = scores.get(index, 0.0) + 1 / (rank_constant + rank)\n    return sorted(scores, key=scores.get, reverse=True)\n\ndef fuse(state: RAGState):\n    dense_rank = list(np.argsort(-np.array(state['dense_scores']))[:50])\n    sparse_rank = list(np.argsort(-np.array(state['sparse_scores']))[:50])\n    candidates = rrf_pair(dense_rank, sparse_rank)[:10]\n    return {'candidates': candidates, 'trace': state['trace'] + ['fuse']}"),
    ("CrossEncoder 재정렬 노드 정의", "from sentence_transformers import CrossEncoder\n\ndef rerank(state: RAGState):\n    model = CrossEncoder('BAAI/bge-reranker-v2-m3', max_length=256, device='cpu')\n    pairs = [(state['question'], state['chunks'][i]['text']) for i in state['candidates']]\n    scores = model.predict(pairs, show_progress_bar=False)\n    ordered = [state['candidates'][pos] for pos in np.argsort(-scores)]\n    selected, seen = [], set()\n    for index in ordered:\n        item = state['chunks'][index]\n        if item['parent_id'] in seen: continue\n        selected.append(item); seen.add(item['parent_id'])\n        if len(selected) == 2: break\n    return {'selected': selected, 'trace': state['trace'] + ['rerank']}"),
    ("근거 기반 생성 노드 정의", "from langchain.chat_models import init_chat_model\n\ndef generate(state: RAGState):\n    context = '\\n\\n'.join(f\"[{d['parent_id']} p.{d['page']} {d['chunk_id']}]\\n{d['text']}\" for d in state['selected'])\n    prompt = f\"\"\"아래 자료만 사용해 질문에 한국어로 답하세요.\n답 끝에 [doc_id p.쪽] 형식으로 출처를 표시하세요.\n\n질문: {state['question']}\n\n자료:\n{context}\"\"\"\n    model = init_chat_model('openai:gpt-5.4-mini', temperature=0)\n    answer = model.invoke(prompt).text.strip()\n    return {'answer': answer, 'trace': state['trace'] + ['generate']}"),
    ("RAG 그래프 컴파일과 실제 실행", "builder = StateGraph(RAGState)\nfor name, fn in [('load_pages', load_pages), ('dense_search', dense_search), ('sparse_search', sparse_search), ('fuse', fuse), ('rerank', rerank), ('generate', generate)]:\n    builder.add_node(name, fn)\nbuilder.add_edge(START, 'load_pages'); builder.add_edge('load_pages', 'dense_search')\nbuilder.add_edge('dense_search', 'sparse_search'); builder.add_edge('sparse_search', 'fuse')\nbuilder.add_edge('fuse', 'rerank'); builder.add_edge('rerank', 'generate'); builder.add_edge('generate', END)\ngraph = builder.compile()\ninitial = {'question': question, 'parents': parents, 'chunks': [], 'dense_scores': [], 'sparse_scores': [], 'candidates': [], 'selected': [], 'answer': '', 'trace': []}\nresult = graph.invoke(initial)\nprint('선택:', [(d['parent_id'], d['page'], d['chunk_id']) for d in result['selected']])\nprint('답변:', result['answer']); print('실행 흔적:', result['trace'])\nassert any(d['parent_id'] == 'E01' and d['page'] == 3 for d in result['selected'])\nassert '[E01 p.3]' in result['answer']"),
    ("RRF 상수 하나를 바꿔 비교", "dense_rank = list(np.argsort(-np.array(result['dense_scores']))[:50])\nsparse_rank = list(np.argsort(-np.array(result['sparse_scores']))[:50])\nk60 = rrf_pair(dense_rank, sparse_rank, rank_constant=60)[:3]\nk40 = rrf_pair(dense_rank, sparse_rank, rank_constant=40)[:3]\nprint('k=60:', [result['chunks'][i]['chunk_id'] for i in k60])\nprint('k=40:', [result['chunks'][i]['chunk_id'] for i in k40])"),
    ("실제 실행 순서 시각화", "mermaid = graph.get_graph().draw_mermaid()\nprint(mermaid)\nfor node in ['load_pages', 'dense_search', 'sparse_search', 'fuse', 'rerank', 'generate']:\n    assert node in mermaid"),
]

rag_cells = LESSONS["07-RAG-통합과-시각화"]["cells"]

def replace_rag_cell(heading: str, source: str) -> None:
    index = next(i for i, (name, _) in enumerate(rag_cells) if name == heading)
    rag_cells[index] = (heading, source)

replace_rag_cell("패키지 설치와 환경 준비", """%pip install -q langgraph==1.2.11 langchain==1.4.0 langchain-openai==1.6.1 python-dotenv==1.2.3 numpy==2.5.3 scikit-learn==1.9.0 pypdf==6.18.0 kiwipiepy==0.23.2 rank-bm25==0.2.2 sentence-transformers==6.0.1
import os
from pathlib import Path
from dotenv import load_dotenv

for folder in [Path.cwd(), *Path.cwd().parents]:
    if (folder / '.env').is_file():
        load_dotenv(folder / '.env')
        break
assert os.getenv('OPENAI_API_KEY'), 'OPENAI_API_KEY가 필요합니다.'
print('API 키 존재 여부 확인 완료')""")

replace_rag_cell("상태와 PDF 로딩 노드 정의", """from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from pypdf import PdfReader

class RAGState(TypedDict):
    question: str
    parents: list[dict]
    chunks: list[dict]
    dense_scores: list[float]
    sparse_scores: list[float]
    candidates: list[int]
    selected: list[dict]
    answer: str
    usage: dict
    trace: list[str]

def load_pages(state: RAGState):
    chunks = []
    for parent in state['parents']:
        pdf = Path('labs/data/rag-corpus') / parent['source']
        for page, obj in enumerate(PdfReader(pdf).pages, 1):
            chunks.append({'chunk_id': f"{parent['doc_id']}-P{page:02d}-C01", 'parent_id': parent['doc_id'], 'page': page, 'text': obj.extract_text() or ''})
    return {'chunks': chunks, 'trace': state['trace'] + ['load_pages']}""")

replace_rag_cell("근거 기반 생성 노드 정의", '''from langchain.chat_models import init_chat_model

def generate(state: RAGState):
    context = '\\n\\n'.join(f"[{d['parent_id']} p.{d['page']} {d['chunk_id']}]\\n{d['text']}" for d in state['selected'])
    prompt = f"""아래 자료만 사용해 질문에 한국어로 답하세요.
답 끝에 [doc_id p.쪽] 형식으로 출처를 표시하세요.

질문: {state['question']}

자료:
{context}"""
    model = init_chat_model('openai:gpt-5.4-mini', temperature=0)
    reply = model.invoke(prompt)
    return {'answer': reply.text.strip(), 'usage': reply.usage_metadata or {}, 'trace': state['trace'] + ['generate']}''')

replace_rag_cell("CrossEncoder 재정렬 노드 정의", """from sentence_transformers import CrossEncoder

def rerank(state: RAGState):
    model = CrossEncoder('BAAI/bge-reranker-v2-m3', max_length=256, device='cpu')
    pairs = [(state['question'], state['chunks'][i]['text']) for i in state['candidates']]
    scores = model.predict(pairs, show_progress_bar=False)
    ordered = [state['candidates'][pos] for pos in np.argsort(-scores)]
    selected, seen = [], set()
    for index in ordered:
        item = state['chunks'][index]
        if item['parent_id'] in seen:
            continue
        selected.append(item)
        seen.add(item['parent_id'])
        if len(selected) == 2:
            break
    return {'selected': selected, 'trace': state['trace'] + ['rerank']}""")

replace_rag_cell("RAG 그래프 컴파일과 실제 실행", """from time import perf_counter
builder = StateGraph(RAGState)
for name, fn in [('load_pages', load_pages), ('dense_search', dense_search), ('sparse_search', sparse_search), ('fuse', fuse), ('rerank', rerank), ('generate', generate)]:
    builder.add_node(name, fn)
builder.add_edge(START, 'load_pages')
builder.add_edge('load_pages', 'dense_search')
builder.add_edge('dense_search', 'sparse_search')
builder.add_edge('sparse_search', 'fuse')
builder.add_edge('fuse', 'rerank')
builder.add_edge('rerank', 'generate')
builder.add_edge('generate', END)
graph = builder.compile()
initial = {'question': question, 'parents': parents, 'chunks': [], 'dense_scores': [], 'sparse_scores': [], 'candidates': [], 'selected': [], 'answer': '', 'usage': {}, 'trace': []}
started = perf_counter()
result = graph.invoke(initial)
duration_ms = round((perf_counter() - started) * 1000, 2)
print('선택:', [(d['parent_id'], d['page'], d['chunk_id']) for d in result['selected']])
print('답변:', result['answer'])
print('실행 흔적:', result['trace'])
assert any(d['parent_id'] == 'E01' and d['page'] == 3 for d in result['selected'])
assert '[E01 p.3]' in result['answer']""")

save_cell = ("통합 실행 결과 저장", """run_payload = {
    'qid': run['qid'], 'question': question, 'input_ch12_run_id': run['run_id'],
    'retrieved': [{'doc_id': d['parent_id'], 'page': d['page'], 'chunk_id': d['chunk_id']} for d in result['selected']],
    'node_trace': result['trace'], 'response': result['answer'],
    'models': {'embedding': 'text-embedding-3-small', 'dimensions': 256, 'sparse': 'Kiwi+BM25', 'fusion': 'RRF(k=60)', 'reranker': 'BAAI/bge-reranker-v2-m3', 'chat': 'gpt-5.4-mini'},
    'usage': result['usage'], 'duration_ms': duration_ms,
}
run_dir = Path('labs/part4/ch13-langgraph-basics/runs')
run_dir.mkdir(exist_ok=True)
run_path = run_dir / 'graph-integrated-result.json'
run_path.write_text(json.dumps(run_payload, ensure_ascii=False, indent=2))
print('저장:', run_path, '시간:', duration_ms, 'ms')""")
rag_cells.insert(next(i for i, (name, _) in enumerate(rag_cells) if name == "RRF 상수 하나를 바꿔 비교"), save_cell)


def render_source(slug: str, item: dict) -> str:
    goals = "".join(f"<li>{x}</li>" for x in item["goals"])
    notes = "".join(f"<li>{x}</li>" for x in item["notes"])
    quizzes = "\n".join(
        f'<details class="quiz"><summary>{i}. 이해 확인</summary><p class="quiz-q">{q}</p><p class="quiz-a">{a} <b>오답 시 다시 볼 곳:</b> 이 페이지의 핵심 개념과 실험 결과 해석</p></details>'
        for i, (q, a) in enumerate(item["quiz"], 1)
    )
    references = "".join(f'<li><a href="{url}">{name}</a> · 확인 2026-09-10 · LangGraph 1.2.11</li>' for name, url in DOCS_BY_SLUG.get(slug, DOCS))
    figure = slug.split('-', 1)[0] + "-흐름"
    diagram_reading = {
        "01-StateGraph와-노드-엣지": "입력 상태에서 normalize와 make_query를 차례로 지나 최종 상태로 이동합니다. 두 화살표는 add_edge로 선언한 고정 순서입니다.",
        "02-State-갱신": "normalize와 expand가 같은 query 키를 차례로 갱신하고 log 키에는 두 기록이 누적됩니다. query와 log의 결과가 서로 다른 갱신 규칙을 보여 줍니다.",
        "03-조건부-엣지": "inspect_score 뒤의 화살표가 generate와 request_more로 갈라집니다. 0.7이라는 코드 기준에 따라 두 목적지 중 하나만 실행됩니다.",
        "04-add_messages-리듀서": "HumanMessage 입력 뒤에 reply 노드가 AIMessage를 추가합니다. 같은 h1 ID를 다시 넣으면 첫 메시지가 교체되고 전체 길이는 유지됩니다.",
        "05-Send-동적-팬아웃": "documents 목록의 각 항목이 inspect_document로 전달됩니다. 입력 3건은 실행 3건과 results 3건으로 이어집니다.",
        "06-Command-갱신과-이동": "route 노드에서 generate와 request_more로 화살표가 갈라집니다. Command가 decision을 갱신하면서 선택한 목적지로 이동합니다.",
        "07-RAG-통합과-시각화": "Ch12 질문과 문서 청크가 search, fuse, rerank, generate를 차례로 지나갑니다. 마지막 상태에는 선택 문서, 새 답변, 실행 흔적이 남습니다.",
    }[slug]
    deepening = {
        "01-StateGraph와-노드-엣지": "코드는 상태 형식을 먼저 선언한 뒤 노드 함수를 정의합니다. 각 함수의 state 매개변수는 현재 상태를 읽고, 반환 딕셔너리는 다음 상태에 반영할 값만 담습니다. 이어서 add_node로 이름과 함수를 연결하고 add_edge로 START부터 END까지의 순서를 적습니다. compile() 뒤 invoke()에 입력 상태를 전달하면 엣지를 따라 노드가 실행됩니다. trace 값과 Mermaid의 화살표를 함께 보면 파이썬 함수 이름, 그래프 노드 이름, 실제 실행 순서를 하나씩 대응할 수 있습니다.",
        "02-State-갱신": "UpdateState에서 query에는 리듀서가 없고 log에는 operator.add가 붙어 있습니다. normalize와 expand는 모두 두 키를 갱신하지만 처리 방식은 키 선언에 따라 달라집니다. query는 두 번째 노드가 반환한 값으로 교체되고 log는 입력의 ['input']과 두 노드의 새 목록이 이어집니다. 이 구조에서는 각 노드가 이전 log 전체를 복사할 필요가 없습니다. 새 기록만 목록으로 반환해야 중복 없이 누적됩니다.",
        "03-조건부-엣지": "inspect_score는 route에 checked를 기록하고 실행을 마칩니다. 그 다음 choose 함수가 같은 상태의 rerank_score를 읽습니다. 점수가 0.7 이상이면 generate라는 노드 이름을, 미만이면 request_more를 반환합니다. add_conditional_edges는 이 반환값을 실제 목적지와 연결합니다. 두 목적지 노드는 모두 END로 이어지므로 한 입력에서 두 노드가 함께 실행되지 않습니다. 점수 하나만 바꾼 두 출력을 비교하면 분기 기준과 선택 결과를 분리해 읽을 수 있습니다.",
        "04-add_messages-리듀서": "ChatState의 messages 키는 add_messages를 리듀서로 사용합니다. HumanMessage가 입력되면 reply 노드는 기존 목록 전체가 아니라 새 AIMessage 하나만 반환합니다. 그래프 런타임은 리듀서를 호출해 두 메시지를 합칩니다. 다음 셀은 같은 h1 ID를 가진 HumanMessage를 add_messages에 직접 전달합니다. 첫 메시지의 위치는 유지되지만 content가 바뀌므로, 새 메시지 추가와 기존 메시지 교체라는 두 규칙을 한 출력에서 구분할 수 있습니다.",
        "05-Send-동적-팬아웃": "dispatch는 documents 목록을 순회해 문서마다 Send 객체 하나를 만듭니다. 각 객체의 node에는 inspect_document를, arg에는 그 실행이 읽을 document를 넣습니다. 세 Send는 같은 함수를 호출하지만 서로 다른 작은 상태를 받습니다. 각 실행은 results에 딕셔너리 하나가 든 목록을 반환하고 operator.add가 이 목록들을 합칩니다. 마지막에 ID로 정렬하면 실행 완료 순서가 달라도 입력 문서와 결과를 안정적으로 대응할 수 있습니다.",
        "06-Command-갱신과-이동": "route 함수는 score를 한 번 비교해 enough 값을 만듭니다. 그 값으로 decision 갱신값과 goto 목적지를 동시에 선택합니다. 반환형의 Literal은 generate와 request_more 두 목적지만 가능하다는 정보를 제공합니다. 각 목적지 노드는 answer만 갱신하고 END로 이어집니다. 최종 상태에서 decision과 answer를 함께 보면 판단 기록과 실제 이동이 일치했는지 확인할 수 있습니다. 이동만 필요할 때는 조건부 엣지, 갱신도 함께 남길 때는 Command라는 기준으로 구분합니다.",
        "07-RAG-통합과-시각화": "그래프 입력에는 Ch12 Q002와 여섯 PDF의 파일 정보가 들어갑니다. load_pages는 PDF 35쪽을 텍스트 청크로 만들고, dense_search는 256차원 OpenAI 임베딩의 코사인 유사도를 계산합니다. sparse_search는 Kiwi 형태소로 나눈 토큰을 BM25에 넣습니다. fuse는 두 점수의 크기를 섞지 않고 각 순위의 역순위 점수를 더합니다. rerank는 상위 열 개만 CrossEncoder로 비교하고 부모 문서가 겹치지 않게 두 건을 고릅니다. generate는 이 본문과 출처를 실제 모델에 전달합니다.",
    }[slug]
    evidence = {
        "01-StateGraph와-노드-엣지": "질문을 바꾼 두 실행에서 검색어는 달라졌지만 trace는 같은 두 노드를 기록했습니다. 고정 엣지가 입력 내용과 무관하게 같은 실행 순서를 만든 결과입니다.",
        "02-State-갱신": "두 번째 입력에 넣은 input 기록까지 유지되어 최종 log에는 세 항목이 남았습니다. 반면 query에는 expand가 만든 마지막 문자열 하나만 남았습니다.",
        "03-조건부-엣지": "두 최종 상태의 route와 answer가 함께 달라졌습니다. 조건 함수의 반환값이 실제 목적지 노드 실행으로 이어졌음을 두 필드로 확인했습니다.",
        "04-add_messages-리듀서": "AIMessage.text 출력은 reply 노드가 만든 문장을 그대로 보여 줍니다. 교체 뒤에도 AIMessage의 ID와 내용은 유지되어 수정 범위가 h1 메시지 하나였음을 알 수 있습니다.",
        "05-Send-동적-팬아웃": "문서 세 건과 한 건을 넣은 실행에서 결과 개수가 각각 3과 1이었습니다. 등록한 그래프 구조는 같고 Send 목록 길이만 달라진 비교입니다.",
        "06-Command-갱신과-이동": "두 점수에서 decision과 answer의 조합이 각각 sufficient·생성, insufficient·추가 확인으로 맞았습니다. update와 goto가 같은 판단에서 만들어진 결과입니다.",
        "07-RAG-통합과-시각화": "실제 통합 실행은 E01 3쪽과 E02 3쪽을 선택하고 E01의 7권·14일을 답했습니다. 화면에는 여섯 노드의 실행 순서가 나타나며, 1,230개의 총 토큰 사용량은 마지막 셀이 저장한 graph-integrated-result.json의 usage 필드에서 확인합니다.",
    }[slug]
    execution_guides = {
        "01-StateGraph와-노드-엣지": "첫 셀에서 LangGraph 1.2.11을 준비한 뒤 상태 형식과 두 노드를 정의합니다. 두 질문으로 그래프를 실행해 trace가 normalize와 make_query 순서로 유지되는지 비교합니다. 마지막 Mermaid 출력에서는 START부터 END까지 이어지는 고정 엣지를 확인합니다.",
        "02-State-갱신": "UpdateState의 query와 log 키를 선언하고 두 갱신 노드를 연결합니다. 실행 결과에서 query가 마지막 문자열로 교체되고 log는 세 기록을 이어 붙였는지 확인합니다. 입력 log를 바꾼 비교 실행으로 리듀서가 기존 목록을 보존하는지도 살펴봅니다.",
        "03-조건부-엣지": "점수를 기록하는 노드와 목적지를 고르는 조건 함수를 정의합니다. 0.82와 0.41을 각각 입력해 generate와 request_more 중 하나만 실행되는지 확인합니다. Mermaid 출력에서는 inspect_score 뒤에 두 경로가 선언됐는지 대조합니다.",
        "04-add_messages-리듀서": "HumanMessage를 입력하고 reply 노드가 AIMessage를 추가하는 그래프를 실행합니다. 출력에서 두 메시지의 순서와 AIMessage.text를 확인합니다. 이어서 h1과 같은 ID의 메시지를 직접 병합해 목록 길이는 유지되고 내용만 교체되는지 비교합니다.",
        "05-Send-동적-팬아웃": "문서마다 Send를 만드는 dispatch와 길이를 검사하는 inspect_document를 정의합니다. 문서 세 건을 입력했을 때 결과가 세 건인지 확인한 뒤, 입력을 한 건으로 줄여 결과 수도 한 건이 되는지 비교합니다. 결과는 ID 순으로 정렬해 입력 문서와 대응합니다.",
        "06-Command-갱신과-이동": "route 노드가 decision 갱신과 goto 목적지를 함께 반환하도록 정의합니다. 0.82와 0.41을 입력해 sufficient·generate와 insufficient·request_more 조합이 각각 나타나는지 확인합니다. Mermaid 출력에서는 Literal에 적은 두 목적지가 표시되는지 살펴봅니다.",
        "07-RAG-통합과-시각화": "Ch12의 Q002와 여섯 PDF 정보를 읽고 PDF 로딩, 임베딩 검색, BM25 검색, RRF 병합, 재정렬, 생성을 차례로 실행합니다. 선택된 E01·E02 문서와 새 답변의 출처, 여섯 노드 trace를 확인합니다. 마지막 셀은 실행 정보와 사용량을 graph-integrated-result.json에 저장합니다.",
    }[slug]
    experiment_limits = {
        "01-StateGraph와-노드-엣지": "이번 실행은 엣지로 고정한 두 노드의 순서만 확인했습니다. 노드가 늘어나거나 분기가 생긴 그래프의 실행 특성은 뒤 절에서 따로 확인합니다.",
        "02-State-갱신": "이번 실행은 두 노드가 순서대로 한 상태를 갱신하는 경우만 확인했습니다. 여러 노드가 동시에 같은 키를 갱신하는 경우에는 해당 키의 리듀서 규칙을 추가로 검토해야 합니다.",
        "03-조건부-엣지": "점수 0.82와 0.41은 분기를 관찰하려고 코드에 넣은 값이며 0.7도 이 실습에서 정한 기준입니다. 실제 서비스에서는 평가 데이터로 점수 계산법과 임계값을 별도로 검증해야 합니다.",
        "04-add_messages-리듀서": "이번 실행은 로컬에서 만든 HumanMessage와 AIMessage 객체의 추가·교체 규칙만 확인했습니다. 채팅 모델은 호출하지 않았으므로 모델 응답 품질이나 비용을 평가한 결과가 아닙니다.",
        "05-Send-동적-팬아웃": "이번 실행은 입력 문서 수에 따라 Send 작업과 결과 수가 달라지는지만 확인했습니다. 작업 시간과 동시 실행 정도를 측정하지 않았으므로 병렬 처리의 성능 향상을 판단할 수 없습니다.",
        "06-Command-갱신과-이동": "두 경로는 코드에 작성한 점수 조건으로 선택됐습니다. 모델이 판단한 결과가 아니며, 실제 판단 규칙을 적용하려면 입력 점수의 생성 과정과 기준을 따로 검증해야 합니다.",
        "07-RAG-통합과-시각화": "Q002 한 건으로 실제 검색부터 생성까지 이어지는지만 확인한 스모크 실행입니다. 전체 질문에서 검색 품질과 답변 품질이 유지되는지는 별도 평가셋과 지표로 측정해야 합니다.",
    }[slug]
    summaries = {
        "01-StateGraph와-노드-엣지": ["두 질문 모두 normalize와 make_query를 같은 순서로 실행했습니다.", "노드는 상태 갱신을 반환하고 엣지는 실행 순서를 정했습니다.", "Mermaid에서 START부터 END까지의 고정 연결을 확인했습니다."],
        "02-State-갱신": ["query 키는 마지막 값으로 교체됐습니다.", "log 키는 operator.add 리듀서로 세 기록을 누적했습니다.", "노드는 자신이 바꿀 키와 새 값만 반환했습니다."],
        "03-조건부-엣지": ["0.82는 generate, 0.41은 request_more 경로를 선택했습니다.", "분기 기준은 코드에 작성한 0.7 임계값이었습니다.", "한 입력에서는 선택된 목적지 노드 하나만 실행됐습니다."],
        "04-add_messages-리듀서": ["첫 실행에서 HumanMessage와 AIMessage가 순서대로 저장됐습니다.", "같은 h1 ID의 메시지는 기존 위치에서 내용이 교체됐습니다.", "AIMessage.text로 모델 메시지의 텍스트를 읽었습니다."],
        "05-Send-동적-팬아웃": ["문서 3건은 Send 작업 3개와 결과 3건을 만들었습니다.", "문서 1건으로 바꾸면 같은 그래프에서 결과도 1건이 됐습니다.", "results 리듀서가 각 작업의 목록을 하나로 합쳤습니다."],
        "06-Command-갱신과-이동": ["Command는 decision 갱신과 다음 목적지를 함께 반환했습니다.", "0.82와 0.41에서 판단 기록과 실제 답변 경로가 일치했습니다.", "Literal 반환형으로 가능한 두 목적지를 시각화했습니다."],
        "07-RAG-통합과-시각화": ["여섯 노드가 PDF 로딩부터 실제 답변 생성까지 차례로 실행됐습니다.", "재정렬 결과 E01 3쪽과 E02 3쪽을 선택하고 7권·14일 답변을 생성했습니다.", "저장 JSON의 usage에는 1,230개의 토큰이 기록됐으며 Q002 한 건의 스모크 실행이므로 전체 품질은 별도로 평가해야 합니다."],
    }[slug]
    summary_html = "".join(f"<li>{summary}</li>" for summary in summaries)
    lesson_hours = "강의 2h | 실습 2h" if slug == "07-RAG-통합과-시각화" else "강의 1h | 실습 1h"
    new_terms = {
        "01-StateGraph와-노드-엣지": 7,
        "02-State-갱신": 4,
        "03-조건부-엣지": 3,
        "04-add_messages-리듀서": 4,
        "05-Send-동적-팬아웃": 3,
        "06-Command-갱신과-이동": 3,
        "07-RAG-통합과-시각화": 5,
    }[slug]
    concept_parts = item["concept"].split(". ")
    definition = ". ".join(concept_parts[1:]) if len(concept_parts) > 1 else item["concept"]
    return f'''<!--meta: {lesson_hours} | 코드 Jupyter Notebook | 새 용어 {new_terms} -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>{goals}</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>{item['why']}</p><p>이번 절의 질문은 “{item['question']}”입니다. 노트북 출력과 그래프 그림을 함께 읽어 답합니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>{item['prior']}</p><p>각 노트북은 Python 3.12 새 커널에서 독립 실행되며 이전 절의 메모리나 개인 경로를 사용하지 않습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>쉬운 예</h3><p>{concept_parts[0]}.</p><h3>정의</h3><p>{definition}</p><h3>코드에서 읽는 순서</h3><p>{deepening}</p>{depth_html(slug)}<h3>도식 읽기</h3>{{{{svg:{figure}}}}}<p>도식은 위에서 아래로 읽습니다. {diagram_reading} 초록은 자료, 파랑은 코드로 정한 처리, 보라는 모델 계산, 노랑은 측정·평가, 빨강은 오류·격리를 나타냅니다. 노트북의 Mermaid 출력에서도 같은 노드 이름을 찾아 선언한 구조를 대조합니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>{execution_guides}</p>{{{{notebook:{slug}}}}}<p class="look"><b>확인할 점</b> — {item['question']} 출력에 나타난 상태 필드와 경로를 근거로 답해 봅니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>{item['observe']}</p><p>{evidence}</p><p>{experiment_limits}</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul>{notes}</ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul>{summary_html}</ul><p><strong>다음 학습과 이어지는 지점</strong> — {item['next']}</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>{quizzes}
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul>{references}</ul>
'''


def main() -> None:
    for slug, item in LESSONS.items():
        (CHAPTER / "_src" / f"{slug}.html").write_text(render_source(slug, item), encoding="utf-8")
        nb = notebook(item["title"], item["question"], item["cells"])
        nb["cells"].insert(1, depth_markdown(slug))
        inject_guidance(nb)
        notebook_path = LAB / "notebooks" / f"{slug}.ipynb"
        notebook_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
