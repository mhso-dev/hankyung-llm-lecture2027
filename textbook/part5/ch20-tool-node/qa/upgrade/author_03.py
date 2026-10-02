"""Ch 20 03절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 author_03.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_03.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
  AUTHOR03_NB_ONLY=1 python3 author_03.py → 노트북만 다시 쓴다
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **paired 형식 유지**(chapter.json).

## 결정 1 — 모델 없이, API 키 셀 없이 (챕터 리드 결정 5·인계 §02→§03 2항)

textbook/part5/qa/check_bundle_execution.py 가 학생 묶음에서 이 노트북을 키 없이 새 커널로 실행한다.
그래서 모델 요청 0번, `nbkit.key_and_model_cells()`의 키 셀도 두지 않는다(Ch 13 01~06절 선례). 준비 셀은 설치·가져오기 둘.
읽는 파일·쓰는 파일 0, 도구 파일(graph_tools.py)도 가져오지 않는다(show_messages·tool_call_names를 쓰지 않음).

## 결정 2 — 그래프 소재: 01절 모양의 두 노드 그래프를 모델 없이

01절 그래프(모델 노드 ↔ 도구 실행 노드 + 되돌아가는 엣지 + 조건 함수)와 같은 모양을 우리가 적은 평범한 노드 둘로 만든다.
고르기 노드 pick_topic(찾은 규정 수로 다음 주제어를 적음, 다 찾으면 빈 글) · 찾기 노드 find_policy(01절 도구 lookup_policy를
.invoke로 직접 부름, 빈 글이면 부르지 않음 — 빈 글은 02절 ValueError). 상태 형식 TopicState(칸 넷, 흔적 칸 operator.add — Ch 13 02).
Before = pick → find 고정 엣지(끝점으로 가는 엣지 없음) → 기본 한도 10007·한도 10에서 GraphRecursionError(받아 출력만, try else 없음).
After = pick 뒤 조건 함수 next_or_end(여러 줄 if + 상수 END) + path_map(01 모양) → 같은 한도 10에서 ['pick', 'find', 'pick'].
값 바꿔 보기 = 한도(3·4)와 주제어 둘(운영·연체, 한도 5·6) — 준비 조사 §5-3 규칙(노드 K번 흐름은 한도 K+1부터).

## 결정 3 — 01절과 같은 셀

POLICY_DATA는 01절과 글자까지 같다. 도구 셀은 01절과 AST가 같고 오류 줄 위 주석 한 줄만 이 절에 맞게 고쳤다(아래 assert).
02절 build_graph(tool_node)는 AgentState·call_model 전용이라 쓰지 않는다 → 도구 파일로 옮기지 않는다.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`sorted`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·튜플 풀기·세미콜론·
`isinstance`·별표 풀기·try `else`·`MessagesState`·`'__end__'` 글자·`Literal`·`perf_counter`·모델·API 키·`stream`·체크포인터.
"""
from __future__ import annotations

import ast
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nbkit import RUN_DATE, code, install_source, md, setup, write_notebook  # noqa: E402
import author_01  # noqa: E402
from author_01 import html_text  # noqa: E402

LAB = ROOT / "labs/part5/ch20-tool-node/notebooks"
SLUG = "03-recursion-limit과-명시적-종료"
SRC = ROOT / "textbook/part5/ch20-tool-node/_src" / (SLUG + ".html")
# 교재 출력을 만든 실행의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답)에서 읽은 값
RUNSEC = os.environ.get("AUTHOR03_RUNSEC", "10초 안에")

INSTALL = install_source(["langgraph==1.2.11", "langchain==1.4.0", "langchain-core==1.6.2"])

IMPORTS = r'''# Ch 13 그래프 이름과 Ch 19 도구 이름에, 한도를 넘었을 때 나는 오류 이름 하나를 더해 가져옵니다
import operator
from typing import Annotated
from typing_extensions import TypedDict

from langchain.tools import tool
from langgraph.graph import END, START, StateGraph
# 실행 한도를 넘으면 그래프가 내는 오류의 이름입니다
from langgraph.errors import GraphRecursionError

print("이 절에서 새로 가져온 이름:", "GraphRecursionError")'''

# 01절과 글자까지 같은 셀(아래 assert)
POLICY_DATA = author_01.POLICY_DATA

# 01절 도구 셀과 AST가 같다(주석 한 줄만 이 절에 맞게 고침 — 아래 assert)
DEF_TOOL = r'''# 주제어 하나로 규정 글 하나를 찾는 도구를 만듭니다(맨 @tool 줄 — Ch 19 01절)
@tool
def lookup_policy(topic: str):
    """교육센터 자료실 규정 하나를 주제어로 찾습니다. topic에는 대출, 운영, 연체 가운데 하나를 넣습니다."""
    # 딕셔너리에 없는 주제어면 오류를 냅니다(02절에서 본 ValueError입니다)
    if topic not in POLICIES:
        raise ValueError("지원하지 않는 주제: " + topic)
    return POLICIES[topic]'''

TRY_EMPTY = r'''# 빈 글을 주제어로 도구를 불러 봅니다(이 셀만 오류를 받아 출력합니다)
try:
    lookup_policy.invoke({"topic": ""})
except ValueError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:", error)'''

STATE = r'''# 찾을 주제어·다음 주제어·찾은 규정·실행 흔적 칸을 둔 상태 형식을 만듭니다(뒤의 두 칸은 Ch 13 02절 규칙)
class TopicState(TypedDict):
    topics: list[str]
    next_topic: str
    found: Annotated[list[str], operator.add]
    trace: Annotated[list[str], operator.add]'''

DEF_PICK = r'''# 찾은 규정 수를 보고, 다음에 찾을 주제어 하나를 칸 next_topic에 적습니다
def pick_topic(state):
    index = len(state["found"])
    # 아직 찾지 않은 주제어가 남았으면 그 차례의 주제어를, 모두 찾았으면 빈 글을 적습니다
    if index < len(state["topics"]):
        return {"next_topic": state["topics"][index], "trace": ["pick"]}
    return {"next_topic": "", "trace": ["pick"]}'''

TRY_PICK = r'''# 고르기 노드를 그래프 없이 직접 불러, 찾은 규정 수에 따라 무엇을 적는지 봅니다
loan_state = {"topics": ["대출"], "next_topic": "", "found": [], "trace": []}
done_state = {"topics": ["대출"], "next_topic": "대출", "found": [POLICIES["대출"]], "trace": ["pick", "find"]}
print("찾은 규정이 없을 때:", pick_topic(loan_state))
print("하나를 찾은 뒤:", pick_topic(done_state))'''

DEF_FIND = r'''# 칸 next_topic의 주제어로 도구를 불러, 찾은 규정 글 하나를 냅니다
def find_policy(state):
    topic = state["next_topic"]
    # 빈 글이면 도구를 부르지 않습니다(2절처럼 ValueError가 나기 때문입니다)
    if topic == "":
        return {"trace": ["find"]}
    policy = lookup_policy.invoke({"topic": topic})
    return {"found": [policy], "trace": ["find"]}'''

TRY_FIND = r'''# 찾기 노드를 그래프 없이 직접 불러, 주제어가 있을 때와 빈 글일 때를 봅니다
ask_state = {"topics": ["대출"], "next_topic": "대출", "found": [], "trace": ["pick"]}
empty_state = {"topics": ["대출"], "next_topic": "", "found": [POLICIES["대출"]], "trace": ["pick", "find", "pick"]}
print("주제어가 대출일 때:", find_policy(ask_state))
print("빈 글일 때:", find_policy(empty_state))'''

BEFORE_BUILD = r'''# Before: 고르기 노드 다음을 늘 찾기 노드로 잇고, 끝점 END로 가는 엣지는 적지 않습니다
before_builder = StateGraph(TopicState)
before_builder.add_node("pick", pick_topic)
before_builder.add_node("find", find_policy)
before_builder.add_edge(START, "pick")
before_builder.add_edge("pick", "find")
before_builder.add_edge("find", "pick")
before_graph = before_builder.compile()
print("고정 엣지로 적은 수:", len(before_builder.edges))
print("조건부 엣지를 적은 노드 수:", len(before_builder.branches))'''

BEFORE_RUN = r'''# Before 그래프를 대출 주제어 하나로, 한도를 적지 않고 실행합니다(이 셀만 올라온 오류를 받아 출력합니다)
try:
    before_graph.invoke(loan_state)
except GraphRecursionError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:")
    print(error)'''

BEFORE_LIMIT = r'''# 설정 딕셔너리에 실행 한도 10을 적어, Before 그래프를 다시 실행합니다(이 셀도 오류를 받아 출력합니다)
limit_config = {"recursion_limit": 10}
print("설정 딕셔너리:", limit_config)
try:
    # 둘째 인자로 넘긴 설정 딕셔너리는 상태에 들어가지 않고, 그래프가 실행 단계를 셀 때 씁니다
    before_graph.invoke(loan_state, limit_config)
except GraphRecursionError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:")
    print(error)'''

DEF_COND = r'''# 칸 next_topic을 보고, 찾을 주제어가 있으면 이름표 "find"를, 빈 글이면 END를 내놓습니다
def next_or_end(state):
    if state["next_topic"] == "":
        return END
    return "find"'''

TRY_COND = r'''# 조건 함수를 그래프 없이 직접 불러, 3절의 두 상태에 어떤 이름표를 내놓는지 봅니다
ask_label = next_or_end(ask_state)
empty_label = next_or_end(empty_state)
print("주제어가 있을 때의 이름표:", ask_label)
print("빈 글일 때의 이름표:", empty_label)
print("END와 같은가:", empty_label == END)'''

PATH_MAP = r'''# 조건 함수의 이름표 둘을 실제로 갈 곳에 잇는 이름표 표를 만듭니다(Ch 13 03절)
path_map = {"find": "find", END: END}
print("이름표와 갈 곳을 이은 표:")
for label in path_map:
    print(label, "->", path_map[label])'''

AFTER_BUILD = r'''# After: 고르기 노드에서 나가는 엣지만 조건부 엣지로 바꿔 그래프를 만듭니다
after_builder = StateGraph(TopicState)
after_builder.add_node("pick", pick_topic)
after_builder.add_node("find", find_policy)
after_builder.add_edge(START, "pick")
after_builder.add_conditional_edges("pick", next_or_end, path_map)
after_builder.add_edge("find", "pick")
after_graph = after_builder.compile()
print("고정 엣지로 적은 수:", len(after_builder.edges))
print("조건부 엣지를 적은 노드 수:", len(after_builder.branches))'''

AFTER_STRUCTURE = r'''# 컴파일한 After 그래프가 스스로 그린 구조 문자열을 받아 옵니다(Ch 13 01절)
after_structure = after_graph.get_graph().draw_mermaid()
print("그래프가 그린 구조:")
print(after_structure)'''

AFTER_RUN = r'''# After 그래프를 3절의 첫 상태와 4절의 설정 딕셔너리(한도 10)로 실행합니다
after_result = after_graph.invoke(loan_state, limit_config)
print("실행 흔적 칸:", after_result["trace"])
print("찾은 규정 수:", len(after_result["found"]))
print("찾은 규정:", after_result["found"][0])
print("칸 next_topic이 빈 글인가:", after_result["next_topic"] == "")'''

AFTER_CHECK = r'''# 노드 실행 수를 세고, 모델 없이 매번 같아야 하는 값을 확인합니다
after_runs = len(after_result["trace"])
print("노드 실행 수:", after_runs)
# 두 노드는 모델을 부르지 않으므로, 차례와 찾은 규정 수가 매번 같아야 합니다
assert after_result["trace"] == ["pick", "find", "pick"], "고르기·찾기·고르기 차례로 끝나야 합니다"
assert len(after_result["found"]) == 1, "대출 규정 글 하나를 찾아야 합니다"'''

DEF_TRY_LIMITS = r'''# 그래프 하나와 첫 상태 하나를 받아, 한도 목록의 값마다 실행해 통과했는지 출력합니다
def try_limits(graph, state, limits):
    for limit in limits:
        config = {"recursion_limit": limit}
        # 한도에 닿으면 그 한도에서 받은 오류 이름만 출력하고, 다음 한도로 넘어갑니다
        try:
            result = graph.invoke(state, config)
            print("한도", limit, "| 통과 | 노드 실행 수:", len(result["trace"]))
        except GraphRecursionError as error:
            print("한도", limit, "| 받은 오류:", type(error).__name__)'''

LIMIT_ONE = r'''# 바꿀 값: 한도를 3과 4로 바꿔, 대출 흐름을 After 그래프로 실행합니다
limits = [3, 4]
try_limits(after_graph, loan_state, limits)'''

TWO_RUN = r'''# 바꿀 값 둘째: 주제어를 운영과 연체 둘로 바꾼 첫 상태를, 한도 10으로 실행합니다
two_state = {"topics": ["운영", "연체"], "next_topic": "", "found": [], "trace": []}
two_result = after_graph.invoke(two_state, limit_config)
print("실행 흔적 칸:", two_result["trace"])
print("찾은 규정 수:", len(two_result["found"]))'''

LIMIT_TWO = r'''# 같은 두 주제어 흐름을 한도 5와 6으로 실행해, 통과하는 한도를 봅니다
limits = [5, 6]
try_limits(after_graph, two_state, limits)'''

COMPARE = r'''# 두 흐름에서 고르기 노드를 지난 수(01절 말로 바퀴 수)와 노드 실행 수를 나란히 봅니다
loan_trace = after_result["trace"]
two_trace = two_result["trace"]
print("대출 | 고르기 노드를 지난 수:", loan_trace.count("pick"), "| 노드 실행 수:", len(loan_trace))
print("운영·연체 | 고르기 노드를 지난 수:", two_trace.count("pick"), "| 노드 실행 수:", len(two_trace))'''


FIG1 = "03-1-끝나는-엣지가-다른-두-그래프"
FIG1_ALT = "왼쪽과 오른쪽에 칸 둘이 나란히 있는 그림입니다. 왼쪽 칸 Before 끝점으로 가는 엣지 없음에는 회색 가상 시작점 START에서 파란 상자 고르기 노드 pick 함수 pick_topic으로, 다시 파란 상자 찾기 노드 find 함수 find_policy로 실선이 가고, 찾기 노드에서 고르기 노드로 되돌아가는 엣지 실선이 돌아옵니다. 오른쪽 칸 After 명시적 종료에는 같은 시작점과 두 노드가 있고, 고르기 노드에서 점선 두 갈래가 나가 주제어 있음 이름표 find는 찾기 노드로, 빈 글 이름표 END는 회색 가상 끝점 END로 갑니다. 찾기 노드에서 고르기 노드로 되돌아가는 엣지 실선이 돌아오는 그림"
FIG1_CAP = "두 그래프는 노드 둘과 되돌아가는 엣지가 같고, 고르기 노드에서 나가는 엣지만 다릅니다."
FIG1_READ = """왼쪽 칸이 Before, 오른쪽 칸이 After이고, 칸 안은 위에서 아래로 읽습니다.
파란 상자는 우리가 적은 노드이고, 회색은 LangGraph의 가상 시작점과 가상 끝점입니다.
왼쪽 칸에는 끝점이 없어, 고르기 노드와 찾기 노드를 오가는 길만 있습니다.
오른쪽 칸은 고르기 노드에서 점선 두 갈래가 나가고, 빈 글이면 끝점으로 갑니다.
오른쪽 칸의 상자 넷과 화살표 넷은 노트북 5절 구조 문자열과 같습니다."""

FIG2 = "03-2-두-노드가-읽고-쓰는-칸"
FIG2_ALT = "위에 초록 상자 상태 형식 TopicState 찾을 주제어 다음 주제어 찾은 규정 실행 흔적이 있고, 거기서 아래 칸 둘로 화살표가 갑니다. 왼쪽 칸 고르기 노드 pick_topic에는 노란 상자 찾은 규정이 없을 때 next_topic 대출 흔적 pick과, 노란 상자 하나를 찾은 뒤 next_topic 빈 글 흔적 pick이 위아래로 있습니다. 오른쪽 칸 찾기 노드 find_policy에는 노란 상자 주제어가 대출일 때 found에 대출 규정 글 하나 1인 5권까지 14일과, 노란 상자 빈 글일 때 도구를 부르지 않고 흔적 find만이 위아래로 있는 그림"
FIG2_CAP = "고르기 노드는 다 찾으면 빈 글을 적고, 찾기 노드는 빈 글이면 도구를 부르지 않습니다."
FIG2_READ = "맨 위 초록 상자는 두 노드가 함께 읽고 쓰는 상태의 칸 넷입니다. 아래 두 칸은 노트북 3절에서 노드를 그래프 없이 직접 부른 결과입니다. 칸 안의 두 노란 상자는 서로 다른 상태를 넣은 결과라 화살표로 잇지 않았습니다. 찾기 노드가 빈 글에서 도구를 부르지 않는 까닭은 노트북 2절의 빈 글 오류입니다."

FIG3 = "03-3-한도에-닿은-Before와-끝난-After"
FIG3_ALT = "위에 초록 상자 같은 첫 상태 loan_state 주제어 대출 하나 찾은 규정 없음이 있고, 아래에 칸 둘이 나란히 있습니다. 왼쪽 칸 Before 끝점으로 가는 엣지 없음에는 빨간 상자 셋이 위아래로 있습니다. 한도를 적지 않음 Recursion limit of 10007 GraphRecursionError, 설정 딕셔너리 한도 10 Recursion limit of 10 GraphRecursionError, invoke가 결과를 내놓지 않음 찾은 규정 글도 받지 못함입니다. 오른쪽 칸 After 조건 함수 next_or_end에는 노란 상자 설정 딕셔너리 한도 10 흔적 pick find pick과, 노란 상자 노드 실행 세 번 찾은 규정 하나 둘째 고르기 뒤 END가 위아래로 있습니다. 맨 아래 회색 상자에 같은 노드 둘 같은 첫 상태 다른 것은 고르기 노드에서 나가는 엣지 하나라고 적힌 그림"
FIG3_CAP = "끝점으로 가는 엣지가 없는 Before는 두 번 모두 한도에 닿아 멈췄고, After는 같은 한도 10 안에서 끝났습니다."
FIG3_READ = "맨 위 초록 상자는 두 칸에 똑같이 넣은 첫 상태입니다. 왼쪽 칸이 Before, 오른쪽 칸이 After이고, 칸 안 상자는 위에서 아래로 읽습니다. 빨간 상자는 Before의 결함 결과이고, 노란 상자는 After 셀의 출력입니다. 칸 안 상자들은 한 셀의 출력을 나눠 적은 것이라 화살표로 잇지 않았습니다. 맨 아래 회색 상자는 두 칸의 코드를 견줘 얻은 사실입니다."

FIG4 = "03-4-노드-실행-수와-한도의-경계"
FIG4_ALT = "위쪽에 칸 둘이 나란히 있는 그림입니다. 왼쪽 칸 주제어 하나 대출 노드 실행 세 번에는 노란 상자 한도 3 GraphRecursionError와 노란 상자 한도 4 통과 노드 실행 수 3이 위아래로 있습니다. 오른쪽 칸 주제어 둘 운영 연체 노드 실행 다섯 번에는 노란 상자 한도 5 GraphRecursionError와 노란 상자 한도 6 통과 노드 실행 수 5가 위아래로 있습니다. 맨 아래 회색 상자에 두 흐름 모두 노드 실행 수보다 하나 큰 한도에서 통과, 소스 확인 단계를 시작할 때 한도를 먼저 봄이라고 적힌 그림"
FIG4_CAP = "노드를 세 번 실행하는 흐름은 한도 4에서, 다섯 번 실행하는 흐름은 한도 6에서 통과했습니다."
FIG4_READ = "위쪽 칸 둘은 값 바꿔 보기에서 실행한 두 흐름입니다. 칸마다 위 상자가 멈춘 한도, 아래 상자가 통과한 한도입니다. 노란 상자는 모두 노트북 6절 출력이고, 값 바꿔 보기에서 받은 오류도 노랑으로 두었습니다. 맨 아래 회색 상자는 두 칸의 출력과 설치판 소스로 확인한 규칙입니다."

FIG5 = "03-5-바퀴-한도와-실행-한도"
FIG5_ALT = "왼쪽과 오른쪽에 칸 둘이 나란히 있는 그림입니다. 왼쪽 칸 Ch 19 05절 우리가 쓴 for 루프에는 파란 상자 바퀴 한도 turn_limit 바퀴 한 번에 모델 요청 한 번과, 회색 상자 01절 대출 흐름이라면 모델 요청 두 번 바퀴 두 번이 위아래로 있습니다. 오른쪽 칸 그래프 실행 한도 recursion_limit에는 회색 상자 단계 수를 셈 이 절 그래프는 단계마다 노드 하나와, 노란 상자 이 절 대출 흐름 고르기 두 번 노드 실행 세 번 한도 4에서 통과가 위아래로 있는 그림"
FIG5_CAP = "바퀴 한도는 모델 요청 수를, 실행 한도는 단계 수를 세어, 대출 흐름에서 바퀴는 두 번이고 단계는 세 번입니다."
FIG5_READ = "왼쪽 칸이 Ch 19 05절 함수 안의 `for` 루프, 오른쪽 칸이 이 절 그래프입니다. 파란 상자는 우리가 적은 코드이고, 회색 상자는 셈과 LangGraph가 정한 사실입니다. 왼쪽 아래 회색 상자는 01절 출력으로 센 값이고, 이 절에서 실행한 값이 아닙니다. 노란 상자는 노트북 6·7절 출력입니다."

ILLU = "03-6-계수기가-다-찬-상자와-창구에-선-상자"
ILLU_ALT = "흰 바탕 그림으로 두 층 자료실 벽을 잘라 보인 모습입니다. 위층 왼쪽에는 긴 나무 창구가, 아래층 왼쪽에는 파란 책이 꽂힌 책장이 있습니다. 벽 속에 옅은 갈색 승강 통로 둘이 떨어져 세로로 나 있고, 두 통로 사이에는 파란 기둥이 서 있습니다. 왼쪽 통로의 나무 상자는 위층 바닥 바로 아래에 멈춰 있고, 흰 카드 한 장이 반쯤 삐져나와 있습니다. 그 옆 판의 둥근 등 넷은 모두 빨갛게 켜져 있습니다. 오른쪽 통로의 같은 상자는 위층 바닥 위에서 작은 나무 받침에 얹혀 있고, 흰 카드 한 장이 반쯤 삐져나와 있습니다. 그 옆 판의 둥근 등 넷 가운데 둘만 노랗게 켜져 있는 그림"
ILLU_CAP = "왼쪽 상자는 계수기 등이 다 켜져 창구 층 아래에서 멈췄고, 오른쪽 상자는 받침에 얹혀 창구 층에 섰습니다."
ILLU_READ = "벽 속 승강 통로는 둘이고, 통로마다 나무 상자 하나와 둥근 등 넷이 달린 계수기 판 하나가 있습니다. 왼쪽 상자는 흰 카드를 실은 채 위층 바닥 바로 아래에 멈춰 있고, 계수기 등 넷이 모두 빨갛게 켜져 있습니다. 오른쪽 상자는 흰 카드를 싣고 위층 바닥 위 나무 받침에 얹혀 있고, 계수기 등은 넷 가운데 둘만 켜져 있습니다. 왼쪽은 실행 한도에 닿아 멈춘 Before, 오른쪽은 받침, 곧 명시적 종료로 창구 층에 선 After입니다. 두 통로 사이의 파란 기둥은 벽의 일부이고, 비유와는 관계가 없습니다."

TITLE = """# recursion_limit과 명시적 종료

**이 노트북에서 할 일**

1. 끝점으로 가는 엣지가 없는 그래프가 실행 한도에 닿아 멈추는 것을 봅니다.
2. 조건 함수가 `END`를 내놓게 해, 같은 한도 안에서 흐름을 끝냅니다.
3. 한도 값을 바꿔, 노드 실행 수와 한도의 경계를 출력으로 확인합니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
그래서 `.env` 파일을 읽는 셀과 키를 확인하는 셀이 없습니다.
모델 답에 따라 되풀이 횟수가 달라지면, 한도에 닿는 장면을 매번 같게 볼 수 없기 때문입니다.
그래서 모델을 부르지 않고, 정해 둔 차례를 따르는 우리 노드 둘로 그래프를 만듭니다.

노트북 안 규정 딕셔너리를 읽기만 하고, 읽는 파일과 새로 쓰는 파일은 없습니다.
교재 출력을 만든 실행에서는 노트북 전체가 """ + RUNSEC + """ 끝났습니다.

**기준 버전** — 첫 셀에서 패키지 셋을 설치합니다.
판은 langgraph 1.2.11, langchain 1.4.0, langchain-core 1.6.2입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3~5절을 읽습니다.
노드 둘을 만들고, 끝나는 엣지가 없는 그래프와 조건 함수로 끝내는 그래프를 견주는 자리입니다.
6·7절은 한도 값을 바꿔 경계를 찾고 바퀴 한도와 견주는 자리이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part5/ch20-tool-node`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

01절과 02절 그래프는 되풀이하는 횟수의 한도를 따로 정하지 않고 실행했습니다.
이 절은 그 한도와, 흐름을 끝내는 조건을 봅니다.
제목의 `recursion_limit`은 실행 한도이고, 뜻은 4절에서 풉니다.

첫 셀은 패키지 세 개를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langgraph: 1.2.11`·`langchain: 1.4.0`·`langchain-core: 1.6.2`가 보입니다.
세 판 모두 실습 폴더 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
그래프와 도구 이름은 01절과 같고, 오류 이름 하나를 더 가져옵니다.
모델을 부르지 않으니 모델과 메시지 이름은 가져오지 않습니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `이 절에서 새로 가져온 이름: GraphRecursionError`가 보입니다.
이 이름은 그래프가 실행 한도를 넘었을 때 내는 오류의 이름입니다.
4절에서 이 오류를 받아 출력합니다.

모델을 부르지 않는 절이라, Ch 13 01~06절처럼 API 키 셀도 없습니다.

## 2. 규정 자료와 도구

자료와 도구는 01절과 같은 코드입니다.
다음 셀은 01절처럼 주제어를 키, 규정 글을 값으로 둔 딕셔너리를 만듭니다."""),
        code(POLICY_DATA),
        md("""**결과 읽기** — 출력 줄 `규정 주제어: ['대출', '운영', '연체']`로 키 셋을 확인합니다.
이 셀은 01절 셀과 글자까지 같습니다.

다음 셀은 01절과 같은 도구 `lookup_policy`를 만듭니다.
코드는 01절과 같고, 오류를 내는 줄 위 주석 한 줄만 이 절에 맞게 고쳤습니다."""),
        code(DEF_TOOL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 절에서는 노드 하나가 이 도구를 코드로 직접 부릅니다.
Ch 19 01절처럼 메서드 `.invoke`에 인자 딕셔너리를 넣는 모양입니다.

다음 셀은 빈 글을 주제어로 도구를 불러 봅니다.
실행 전에 예상해 봅니다.
빈 글도 글자라서 입력 검사는 지나고, 몸통에서 02절의 `ValueError`가 날 것입니다.
이 셀만 그 오류를 받아 출력하고, 셀은 끝까지 갑니다."""),
        code(TRY_EMPTY),
        md("""**결과 읽기** — 출력 줄 `받은 오류: ValueError`처럼 몸통에서 오류가 났습니다.
라벨 `오류 글:` 뒤 `지원하지 않는 주제:` 다음이 비어 있는 것은, 주제어가 빈 글이기 때문입니다.
그래서 3절의 찾기 노드는 주제어가 빈 글이면 도구를 부르지 않습니다.

## 3. 상태 형식과 노드 둘

이 절의 그래프는 01절 그래프와 같은 모양입니다.
노드 둘을 되돌아가는 엣지로 잇고, 한 노드 뒤에서 갈 곳을 고릅니다.
다만 모델 노드와 도구 실행 노드 대신, 우리가 적은 평범한 노드 둘을 씁니다.
한 노드는 다음에 찾을 주제어를 고르고, 다른 노드는 도구로 규정 글을 찾습니다.

다음 셀은 상태 형식입니다.
칸 `topics`는 찾을 주제어 목록, 칸 `next_topic`은 다음에 찾을 주제어입니다.
칸 `found`는 찾은 규정 글, 칸 `trace`는 실행 흔적입니다.
뒤의 두 칸에는 Ch 13 02절처럼 이어 붙이기 규칙 `operator.add`를 적습니다.
칸 구성이 01절 `AgentState`와 달라서, Ch 13 약속대로 새 이름 `TopicState`를 붙입니다."""),
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 `topics`와 `next_topic`은 규칙이 없어, 노드가 낸 값으로 덮어씁니다.
칸 `found`와 `trace`는 노드가 낸 목록을 뒤에 이어 붙입니다.

다음 셀은 다음에 찾을 주제어를 고르는 노드 함수입니다.
찾은 규정 수를 보고, 아직 찾지 않은 주제어가 남았으면 목록에서 그 차례의 주제어를 적습니다.
모두 찾았으면 빈 글을 적습니다.
이 노드는 정해 둔 차례를 따르는 우리 노드이고, 01절 모델 노드처럼 되돌아가는 엣지가 돌아오는 자리에 둡니다."""),
        code(DEF_PICK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `pick_topic`은 칸 `next_topic`과 실행 흔적 `"pick"`만 냅니다.
그래프에는 이름 `"pick"`으로 등록하고, 이 절에서는 고르기 노드라고 부릅니다.

다음 셀은 이 노드를 그래프 없이 직접 불러 봅니다.
Ch 13 03절에서 조건 함수를 직접 불렀던 것처럼, 손으로 만든 상태 둘을 넣습니다.
하나는 규정을 아직 찾지 않은 상태, 다른 하나는 대출 규정을 이미 찾은 상태입니다."""),
        code(TRY_PICK),
        md("""**결과 읽기** — 출력 줄 `찾은 규정이 없을 때: {'next_topic': '대출', 'trace': ['pick']}`입니다.
출력 줄 `하나를 찾은 뒤: {'next_topic': '', 'trace': ['pick']}`로, 모두 찾으면 빈 글을 적습니다.
첫 상태 `loan_state`는 01절 7절 대출 질문처럼 주제어가 대출 하나인 상태입니다.
4절부터 그래프의 첫 상태로 이 값을 그대로 씁니다.

다음 셀은 칸 `next_topic`의 주제어로 규정 글을 찾는 노드 함수입니다.
주제어가 빈 글이면 2절처럼 오류가 나므로, 도구를 부르지 않고 실행 흔적만 남깁니다.
이 노드는 01절 도구 실행 노드 자리에 둡니다."""),
        code(DEF_FIND),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `find_policy`는 그래프에 이름 `"find"`로 등록하고, 이 절에서는 찾기 노드라고 부릅니다.
주제어가 있으면 칸 `found`에 규정 글 하나를, 없으면 실행 흔적만 냅니다.

다음 셀은 이 노드도 그래프 없이 직접 불러 봅니다.
주제어가 대출인 상태와 빈 글인 상태를 손으로 만들어 넣습니다."""),
        code(TRY_FIND),
        md("""**결과 읽기** — 주제어가 대출일 때 칸 `found`에 `일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.`가 담겼습니다.
출력 줄 `빈 글일 때: {'trace': ['find']}`로, 빈 글이면 실행 흔적만 냅니다.
두 노드 모두 모델을 부르지 않아, 같은 상태를 넣으면 매번 같은 값을 냅니다.

## 4. 끝나는 엣지 없이 실행하기 (Before)""", lesson_part="before"),
        md("""먼저 01절처럼 두 노드를 되돌아가는 엣지로 잇습니다.
이번에는 고르기 노드 다음을 늘 찾기 노드로 잇고, 끝점 `END`로 가는 엣지는 적지 않습니다.
고르기 노드는 주제어를 다 찾으면 빈 글을 적지만, 그래프는 그 칸을 보고 멈추지 않습니다.
그래프가 어디로 갈지는 노드 안의 코드가 아니라 엣지가 정하기 때문입니다.
다음 셀은 이 그래프를 만들고, 적어 둔 엣지 수를 봅니다.""", lesson_part="before"),
        code(BEFORE_BUILD, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `고정 엣지로 적은 수: 3`은 시작 엣지·`pick → find`·`find → pick`입니다.
출력 줄 `조건부 엣지를 적은 노드 수: 0`으로, 갈 곳을 고르는 엣지는 없습니다.
속성 `branches`에는 조건부 엣지를 적은 노드가 들어가는데, 이 그래프는 비어 있습니다.
엣지 셋 가운데 끝점으로 가는 것은 없고, `find → pick`이 01절의 되돌아가는 엣지입니다.

다음 셀은 01·02절처럼 한도를 따로 적지 않고, 3절의 첫 상태로 이 그래프를 실행합니다.
실행 전에 예상해 봅니다.
대출 규정은 찾기 노드를 한 번 지나면 찾지만, 그래프는 끝나지 않을 것입니다.
이 셀만 올라온 오류를 받아 출력하고, 셀은 끝까지 갑니다.""", lesson_part="before"),
        code(BEFORE_RUN, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `받은 오류: GraphRecursionError`처럼 그래프가 스스로 멈추지 않았습니다.
오류 글 첫 줄 `Recursion limit of 10007 reached without hitting a stop condition.`을 봅니다.
끝나는 조건에 닿지 못한 채 한도 10007에 닿았다는 뜻입니다.
한도를 적지 않으면 설치한 langgraph의 기본 한도가 쓰이고, 이 판에서는 그 값이 10007입니다.
오류 글 둘째 줄의 주소는 이 오류를 설명하는 공식 문서입니다.

메서드 `invoke`가 결과를 내놓지 않아, 찾은 대출 규정 글도 이 셀에서는 받지 못했습니다.
노트북 밖에서 노드가 실행될 때마다 따로 세어 보니, 두 노드를 합쳐 10007번 실행했습니다.
01절 그래프에서 모델이 요청을 끝없이 보냈다면, 셈으로는 모델 요청이 5천 번 넘게 나갑니다.
그 흐름은 이번에 실행하지 않았습니다.
이것이 Before의 결함입니다.""", lesson_part="before"),
        md("""그래서 한도를 우리가 적어 줍니다.
그래프를 실행할 때 메서드 `invoke`의 둘째 인자로 설정 딕셔너리를 넘깁니다.
설정 딕셔너리는 상태가 아니라, 실행하는 방법을 적은 딕셔너리입니다.
Ch 13 07절의 설정 칸은 상태 안의 칸이었지만, 설정 딕셔너리는 상태 밖에서 넘깁니다.
키 `"recursion_limit"`에 적은 수가 실행 한도입니다.

실행 한도는 그래프가 한 번 실행에서 진행할 수 있는 단계 수의 한도입니다.
단계는 그래프가 실행할 노드를 골라 한 번 실행하는 차례입니다.
이 절 그래프는 단계마다 노드 하나를 실행합니다.
자료실로 치면 상자가 한 층을 들를 때마다 한 칸씩 차는 계수기의 칸 수입니다.

다음 셀은 한도 10을 적은 설정 딕셔너리로 같은 Before 그래프를 다시 실행합니다.
한도 10은 흐름을 보여 주려고 이 절에서 정한 값입니다.
이 셀도 올라온 오류만 받아 출력합니다.""", lesson_part="before"),
        code(BEFORE_LIMIT, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `설정 딕셔너리: {'recursion_limit': 10}`입니다.
오류 글 첫 줄이 `Recursion limit of 10 reached without hitting a stop condition.`으로 바뀌었습니다.
한도를 적자 단계 10에서 멈췄지만, 결과를 받지 못한 것은 앞 셀과 같습니다.
실행 한도는 끝나지 않는 되풀이를 끊어 줄 뿐, 흐름을 제대로 끝내 주지는 않습니다.

노트북 밖에서 같은 그래프를 한도 1~5와 10으로 실행해 노드 실행 수를 세었습니다.
한도가 N이면 노드를 N번 실행한 뒤 멈췄습니다.

## 5. 조건 함수로 흐름 끝내기 (After)""", lesson_part="after"),
        md("""이제 결함을 고칩니다.
고르기 노드 뒤에 조건 함수를 두어, 칸 `next_topic`이 빈 글이면 `END`를 내놓게 합니다.
흐름을 끝낼 때를 이렇게 조건 함수에 적어 두는 것을, 이 절에서는 명시적 종료라고 부릅니다.
자료실로 치면 창구 층에 받침을 달아, 찾을 쪽지가 없으면 상자가 거기서 서게 하는 일입니다.

01절 도구 조건 함수는 요청이 없는 응답에서 `END`를 냈습니다.
이 절의 조건 함수는 빈 글에서 `END`를 냅니다.
Ch 13 03절처럼 여러 줄 `if`로 적고, 조건 함수는 노드로 등록하지 않습니다.""", lesson_part="after"),
        code(DEF_COND, lesson_part="after"),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `next_or_end`는 칸을 읽기만 하고, 상태를 바꾸지 않습니다.
끝 쪽 이름표는 글자 대신 상수 `END`로 적었습니다.

다음 셀은 이 조건 함수를 그래프 없이 직접 불러 봅니다.
3절에서 만든 상태 둘, 곧 주제어가 대출인 상태와 빈 글인 상태를 넣습니다.""", lesson_part="after"),
        code(TRY_COND, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `주제어가 있을 때의 이름표: find`와 `빈 글일 때의 이름표: __end__`입니다.
출력 줄 `END와 같은가: True`로, 글자 `__end__`는 상수 `END`의 값입니다.
01절에서 도구 조건 함수가 내놓은 이름표와 같은 모양입니다.

다음 셀은 이름표 둘을 실제로 갈 곳에 잇는 이름표 표입니다.""", lesson_part="after"),
        code(PATH_MAP, lesson_part="after"),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄 `find -> find`와 `__end__ -> __end__`입니다.
01절 이름표 표와 모양이 같고, 이름표 하나만 `"find"`로 바뀌었습니다.

다음 셀은 After 그래프를 만듭니다.
Before 그래프와 다른 곳은 고르기 노드에서 나가는 엣지 한 줄뿐입니다.
고정 엣지 `pick → find` 대신, 조건 함수와 이름표 표로 조건부 엣지를 적습니다.""", lesson_part="after"),
        code(AFTER_BUILD, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `고정 엣지로 적은 수: 2`와 `조건부 엣지를 적은 노드 수: 1`입니다.
고정 엣지는 시작 엣지와 되돌아가는 엣지 `find → pick`만 남았습니다.
고르기 노드에서 나가는 엣지가 조건부 엣지 하나로 바뀌었습니다.

다음 셀은 그래프가 스스로 그린 구조 문자열을 봅니다.""", lesson_part="after"),
        code(AFTER_STRUCTURE, lesson_part="after"),
        md("""**결과 읽기** — 라벨 줄 `그래프가 그린 구조:` 아래 화살표 줄 넷을 봅니다.
줄 `__start__ --> pick;`이 시작 엣지이고, 줄 `find --> pick;`이 되돌아가는 엣지입니다.
줄 `pick -.-> __end__;`와 `pick -.-> find;`가 조건부 엣지의 두 갈래입니다.
이제 그래프에는 끝점으로 가는 갈래가 있습니다.

다음 셀은 3절의 첫 상태와 4절의 설정 딕셔너리(한도 10)로 After 그래프를 실행합니다.
실행 전에 예상해 봅니다.
고르기·찾기·고르기 차례로 지나고, 둘째 고르기 뒤 조건 함수가 `END`를 내놓을 것입니다.""", lesson_part="after"),
        code(AFTER_RUN, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `실행 흔적 칸: ['pick', 'find', 'pick']`으로 노드를 세 번 지나고 끝났습니다.
출력 줄 `찾은 규정 수: 1`과 규정 글로, Before가 받지 못한 결과를 이번에는 받았습니다.
출력 줄 `칸 next_topic이 빈 글인가: True`는 둘째 고르기 노드가 빈 글을 적었다는 뜻입니다.
조건 함수가 그 빈 글을 보고 `END`를 내놓아, 한도 10에 닿기 전에 끝났습니다.

다음 셀은 노드 실행 수를 세고, 매번 같아야 하는 값을 `assert`로 확인합니다.""", lesson_part="after"),
        code(AFTER_CHECK, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `노드 실행 수: 3`입니다.
이 그래프는 단계마다 노드 하나를 실행하므로, 단계도 3번입니다.
두 `assert`는 모델이 아니라 우리 코드가 정하는 값에 걸었습니다.

## 6. 값 바꿔 보기 · 실행 한도

바꿀 값은 설정 딕셔너리의 한도입니다.
대출 흐름은 노드를 3번 실행하고 끝났습니다.
그렇다면 한도가 3이면 통과할까요?
한도를 3과 4로 바꿔 같은 흐름을 실행해 봅니다.

다음 셀은 한도 목록의 값마다 그래프를 실행해, 통과했는지 출력하는 함수입니다.
통과하면 노드 실행 수를, 한도에 닿으면 받은 오류 이름을 출력합니다.""", lesson_part="after"),
        code(DEF_TRY_LIMITS, lesson_part="after"),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `try_limits`는 한도마다 설정 딕셔너리를 새로 만들어 넘깁니다.
받은 오류는 Ch 2 05절처럼 그 한도에서만 받아 출력하고, 다음 한도로 넘어갑니다.

다음 셀은 대출 흐름을 한도 3과 4로 실행합니다.
실행 전에 예상해 봅니다.
노드 실행 수가 3이니, 한도 3이면 딱 맞게 통과할 것처럼 보입니다.""", lesson_part="after"),
        code(LIMIT_ONE, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `한도 3 | 받은 오류: GraphRecursionError`로, 한도 3에서는 통과하지 못했습니다.
출력 줄 `한도 4 | 통과 | 노드 실행 수: 3`으로, 한도 4에서는 통과했습니다.
노드 실행 수와 같은 한도로는 모자라고, 하나 더 커야 했습니다.

설치한 langgraph 1.2.11 소스에서는 단계를 시작할 때마다 먼저 한도를 봅니다.
그다음에 실행할 노드가 남았는지 보고, 남은 노드가 없으면 끝냅니다.
그래서 마지막 노드 뒤, 남은 노드가 없는지 확인하는 차례까지 한도 안에 들어야 합니다.

다음 셀은 주제어를 01절 9절 질문처럼 운영과 연체 둘로 바꿔, 한도 10으로 실행합니다.
실행 전에 예상해 봅니다.
고르기와 찾기를 두 번 오간 뒤 고르기에서 끝나, 노드 실행이 5번일 것입니다.""", lesson_part="after"),
        code(TWO_RUN, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `실행 흔적 칸: ['pick', 'find', 'pick', 'find', 'pick']`으로 노드 실행은 5번입니다.
출력 줄 `찾은 규정 수: 2`로 운영과 연체 규정을 모두 찾았습니다.

다음 셀은 이 흐름을 한도 5와 6으로 실행합니다.
실행 전에 예상해 봅니다.
앞의 규칙대로라면 한도 5에서는 멈추고, 한도 6에서 통과할 것입니다.""", lesson_part="after"),
        code(LIMIT_TWO, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `한도 5 | 받은 오류: GraphRecursionError`와 `한도 6 | 통과 | 노드 실행 수: 5`입니다.
노드를 3번 실행하는 흐름은 한도 4에서, 5번 실행하는 흐름은 한도 6에서 통과했습니다.
이 절 두 흐름에서는 노드 실행 수에 하나를 더한 한도부터 통과했습니다.

## 7. 바퀴 한도와 실행 한도

Ch 19 05절 함수 `ask_until_answer`에도 한도가 있었습니다.
바퀴 한도 `turn_limit`은 우리가 쓴 `for` 루프가 도는 바퀴 수의 한도였습니다.
그 함수는 바퀴마다 모델 요청을 한 번 보냈으니, 바퀴 한도는 모델 요청 수의 한도입니다.
실행 한도 `recursion_limit`은 그래프가 센 단계 수의 한도라, 세는 것이 다릅니다.

다음 셀은 이 절 두 흐름에서 고르기 노드를 지난 수와 노드 실행 수를 나란히 봅니다.
고르기 노드는 01절 모델 노드 자리라, 고르기 노드를 지난 수가 01절의 바퀴 수에 해당합니다.""", lesson_part="after"),
        code(COMPARE, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `대출 | 고르기 노드를 지난 수: 2 | 노드 실행 수: 3`입니다.
출력 줄 `운영·연체 | 고르기 노드를 지난 수: 3 | 노드 실행 수: 5`입니다.
바퀴로 세면 2번과 3번이지만, 실행 한도는 3번과 5번을 셉니다.

01절 대출 흐름도 모델 노드 두 번과 도구 실행 노드 한 번, 노드 실행 3번이었습니다.
셈으로는 01절 그래프도 한도 4부터 통과하지만, 모델이 낀 흐름에서는 이번에 실행하지 않았습니다.
그래서 바퀴 한도 값을 실행 한도에 그대로 옮겨 적지 않습니다.

## 정리

1. 끝점으로 가는 엣지가 없는 그래프는 규정을 다 찾은 뒤에도 되풀이하다, 실행 한도에서 멈췄습니다.
2. 조건 함수가 빈 글에서 `END`를 내놓게 하자, 같은 한도 10 안에서 노드 3번으로 끝났습니다.
3. 실행 한도는 노드 실행 단계를 세고, 두 흐름 모두 노드 실행 수보다 하나 큰 한도에서 통과했습니다.

04절에서는 코드의 `if`로 도구를 고르는 흐름과, 모델이 도구를 고르는 흐름을 견줍니다.""", lesson_part="after"),
    ]


L_CH2_05 = "../../part1/ch02-python/05-파일과-예외.html"
L_CH13_02 = "../../part4/ch13-langgraph-basics/02-State-갱신.html"
L_CH13_03 = "../../part4/ch13-langgraph-basics/03-조건부-엣지.html"
L_CH13_05 = "../../part4/ch13-langgraph-basics/05-Send-동적-팬아웃.html"
L_CH13_07 = "../../part4/ch13-langgraph-basics/07-RAG-통합과-시각화.html"
L_CH17_03 = "../ch17-agent-overview/03-모델-도구-루프와-정지-조건.html"
L_CH19_01 = "../ch19-model-tools/01-tool과-Ch4-함수-재사용.html"
L_CH19_05 = "../ch19-model-tools/05-bind_tools와-병렬-호출.html"
L_CH23_01 = "../../part6/ch23-persistence/01-체크포인터와-스레드.html"
L_01 = "01-ToolNode와-tools-condition.html"
L_02 = "02-도구-오류와-ToolMessage.html"
L_04 = "04-if-분기와-모델-선택-비교.html"

LOOK_B5 = "노트북 2절 출력 <code>받은 오류: ValueError</code>로, 빈 글이면 도구가 오류를 내는 것을 봅니다. 노트북 3절 출력 <code>하나를 찾은 뒤: {'next_topic': '', 'trace': ['pick']}</code>로, 다 찾으면 고르기 노드가 빈 글을 적는 것을 봅니다. 같은 절 출력 <code>빈 글일 때: {'trace': ['find']}</code>로, 찾기 노드가 도구를 부르지 않는 것을 봅니다."
LOOK_B6 = "노트북 4절 출력 <code>Recursion limit of 10007 reached</code>와 <code>Recursion limit of 10 reached</code>로 Before의 두 실행을 봅니다. 노트북 5절 출력 <code>실행 흔적 칸: ['pick', 'find', 'pick']</code>으로 After가 끝난 차례를 봅니다. 노트북 6절 출력 <code>한도 3 | 받은 오류: GraphRecursionError</code>와 <code>한도 4 | 통과 | 노드 실행 수: 3</code>으로 경계를 봅니다."


def src_html() -> str:
    return """<!--meta: 강의 0.75h | 실습 1h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 4 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>끝점으로 가는 엣지가 없는 그래프가 실행 한도(<code>recursion_limit</code>)에 닿아 멈추는 것을 확인할 수 있습니다.</li>
<li>조건 함수가 <code>END</code>를 내놓게 해, 흐름을 명시적으로 끝낼 수 있습니다.</li>
<li>실행 한도가 세는 단계와 Ch 19 바퀴 한도가 세는 모델 요청을 구별할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_01 + """\">01절</a> 그래프는 모델이 도구 호출 요청 없이 답해야 끝납니다. 도구 조건 함수는 요청이 있는지만 보므로, 모델이 요청을 끝없이 보내면 그래프도 계속 되풀이합니다. 그러면 모델 요청도 계속 나가고, 비용이 커질 수 있습니다. 01절과 <a href=\"""" + L_02 + """\">02절</a>은 이 되풀이의 한도를 따로 정하지 않고 실행했습니다.</p><p>그래프를 멈추는 장치는 두 가지입니다. 하나는 흐름을 끝낼 때를 우리가 조건 함수에 적어 두는 것입니다. 다른 하나는 끝나지 않을 때 그래프를 세우는 한도입니다. 이 절은 두 장치를 모델 없이 봅니다. 모델 답에 따라 되풀이 횟수가 달라지면, 한도에 닿는 장면을 매번 같게 볼 수 없기 때문입니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH13_03 + """\">Ch 13 03절</a>에서는 조건 함수가 내놓은 이름표를 이름표 표(<code>path_map</code>)로 노드에 이었습니다. 끝 쪽 이름표는 상수 <code>END</code>로 적었습니다. <a href=\"""" + L_CH13_02 + """\">02절</a>에서는 칸에 이어 붙이기 규칙을 적고, 노드가 자기 몫만 내게 했습니다. <a href=\"""" + L_CH13_07 + """\">07절</a>에서는 실행의 설정을 상태의 칸, 곧 설정 칸에 담았습니다. 이 절의 설정 딕셔너리는 그 칸과 달리 상태 밖에서 넘깁니다.</p><p><a href=\"""" + L_CH17_03 + """\">Ch 17 03절</a>에서는 정지 조건이 빠지면 모델이 끝을 고를 때까지 루프가 멈추지 않는다고 보았습니다. 그 절은 바퀴 한도를 코드가 세운 정지 조건 가운데 하나로 두었습니다. <a href=\"""" + L_CH19_05 + """\">Ch 19 05절</a> 함수 <code>ask_until_answer</code>는 바퀴 한도 <code>turn_limit</code>까지 <code>for</code> 루프를 돌렸습니다. 그 함수는 바퀴마다 모델 요청을 한 번 보냈습니다.</p><p>01절에서는 모델 노드와 도구 실행 노드를 되돌아가는 엣지로 이었고, 도구 조건 함수가 <code>END</code>를 골랐습니다. 02절에서는 도구가 딕셔너리에 없는 주제어를 받으면 <code>ValueError</code>를 내는 것을 보았습니다. 이 절도 <a href=\"""" + L_CH2_05 + """\">Ch 2 05절</a>의 <code>try/except 오류이름 as error</code>로, 한도를 넘은 오류를 그 셀에서만 받습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절의 두 층 자료실을 다시 떠올립니다. 이번에는 승강 통로마다 딸깍 계수기가 붙어 있습니다. 상자가 한 층을 들를 때마다 계수기 칸이 하나씩 찹니다. 칸이 모두 차면 멈춤 장치가 상자를 그 자리에 세웁니다.</p><p>왼쪽 통로에는 창구 층에서 설 표시가 없습니다. 상자는 대출 카드를 싣고 창구 층을 들러도 서지 않고, 카드를 실은 채 오르내리기를 되풀이합니다. 결국 계수기 칸이 다 차서 창구 층 바로 아래 통로에서 멈추고, 카드는 끝내 창구에 내려지지 않습니다.</p><p>오른쪽 통로에는 창구 층에 받침이 있습니다. 찾을 쪽지가 남지 않으면 상자는 이 받침에 걸려 창구에 섭니다. 그래서 오른쪽 상자는 카드를 싣고 창구에 섰고, 계수기 칸은 다 차지 않았습니다.</p><p>계수기 칸 하나가 단계이고, 칸 수가 실행 한도입니다. 칸 수를 적어 두는 운행표가 설정 딕셔너리입니다. 창구 층의 받침이 명시적 종료입니다. 왼쪽 통로가 이 절의 Before, 오른쪽 통로가 After입니다.</p>
{{img:""" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + """}}
<p class="look"><b>그림 읽기</b> — """ + ILLU_READ + """</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>단계</td><td>그래프가 실행할 노드를 골라 한 번 실행하는 차례입니다. 함께 실행되는 노드는 한 단계에 들어갑니다. 상자가 한 층을 들러 계수기 칸 하나가 차는 것과 같습니다.</td></tr><tr><td>실행 한도(recursion_limit)</td><td>그래프가 한 번 실행에서 진행할 수 있는 단계 수의 한도입니다. 한도에 닿으면 그래프가 <code>GraphRecursionError</code>를 내고 멈춥니다. 계수기의 칸 수와 같습니다.</td></tr><tr><td>설정 딕셔너리</td><td>메서드 <code>invoke</code>의 둘째 인자로 넘기는, 실행하는 방법을 적은 딕셔너리입니다. 상태에는 들어가지 않습니다. 계수기 칸 수를 적어 둔 운행표와 같습니다.</td></tr><tr><td>명시적 종료</td><td>흐름을 끝낼 때를 조건 함수에 적어 두고, 그때 <code>END</code>로 보내는 것입니다. 창구 층에 받침을 달아 상자가 거기서 서게 하는 것과 같습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 설정 딕셔너리는 <code>limit_config = {"recursion_limit": 10}</code>이고, 실행 한도는 그 키의 값 10입니다. 이 절 그래프는 단계마다 노드 하나를 실행해, 실행 흔적 칸에 한 칸씩 남깁니다. 명시적 종료는 조건 함수 <code>next_or_end</code>가 빈 글에서 <code>END</code>를 내놓는 일입니다.</p>
{{mermaid:""" + FIG1 + "|" + FIG1_ALT + "|" + FIG1_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG1_READ) + """</p>
<h3>바퀴 한도와 실행 한도</h3><p>Ch 19 05절의 바퀴 한도 <code>turn_limit</code>은 우리가 쓴 <code>for</code> 루프가 센 모델 요청 수의 한도였습니다. 실행 한도 <code>recursion_limit</code>은 그래프가 센 단계 수의 한도입니다. 이 절의 대출 흐름은 고르기 노드를 두 번, 노드를 모두 세 번 지났습니다. 고르기 노드를 01절 모델 노드 자리로 보면, 바퀴로는 2번이고 단계로는 3번입니다. 그래서 바퀴 한도 값을 실행 한도에 그대로 옮겨 적지 않습니다.</p>
{{mermaid:""" + FIG5 + "|" + FIG5_ALT + "|" + FIG5_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG5_READ) + """</p>
<h3>다른 상황에 적용</h3><p>01절 그래프에도 같은 설정 딕셔너리를 넘길 수 있습니다. <code>graph.invoke(loan_state, {"recursion_limit": 10})</code>처럼 둘째 인자만 더하면 됩니다. 모델이 도구 호출 요청을 끝없이 보내도, 그래프는 단계 10에서 멈춥니다. 셈으로는 모델 노드를 다섯 번까지 지나, 모델 요청이 5번까지 나갑니다. 이 조합은 이번에 실행하지 않았습니다.</p>
<h3>비교와 경계</h3><p>실행 한도는 끝나지 않는 되풀이를 끊어 줄 뿐, 흐름을 제대로 끝내 주지는 않습니다. 한도에 닿으면 메서드 <code>invoke</code>는 실행 결과를 내놓지 않아, 그때까지 찾은 값도 받지 못합니다. 그래서 흐름이 끝나야 할 때는 조건 함수에 적고, 한도는 그 조건이 빠졌을 때 그래프를 세우는 자리에 둡니다. 한도를 크게 올리기 전에, 끝점으로 가는 엣지가 빠지지 않았는지 먼저 봅니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 01절과 같은 규정 딕셔너리와 도구를 만들고, 빈 글로 도구를 불러 봅니다. 그다음 칸 넷을 둔 상태 형식과 노드 둘을 만듭니다. 고르기 노드는 다음에 찾을 주제어를 적고, 찾기 노드는 그 주제어로 도구를 불러 규정 글을 찾습니다. 두 노드는 손으로 만든 상태를 넣어 그래프 없이 직접 불러 봅니다.</p><p>이 절은 모델을 부르지 않아 모델 요청이 0번이고, API 키 없이 실행합니다. 두 노드는 정해 둔 차례를 따르는 우리 노드라서, 같은 상태를 넣으면 매번 같은 값을 냅니다.</p>
{{notebook:""" + SLUG + """|example}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
{{mermaid:""" + FIG2 + "|" + FIG2_ALT + "|" + FIG2_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG2_READ) + """</p>
<h2 id="b6"><span class="no">6</span>실패 확인</h2><p>아래 Before 셀은 고르기 노드 다음을 늘 찾기 노드로 이은 그래프를 두 번 실행합니다. 한 번은 한도를 적지 않고(설치판 기본 한도), 한 번은 한도 10으로 실행합니다. 이어지는 After 셀은 고르기 노드 뒤에 조건 함수를 둔 그래프를 같은 한도로 실행합니다. 마지막 값 바꿔 보기는 한도와 주제어 수를 바꿔 경계를 찾습니다.</p>
{{notebook:""" + SLUG + """|failure}}
{{mermaid:""" + FIG3 + "|" + FIG3_ALT + "|" + FIG3_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG3_READ) + """</p>
<p>Before 그래프는 대출 규정을 찾은 뒤에도 고르기와 찾기를 되풀이했습니다. 한도를 적지 않은 실행은 <code>Recursion limit of 10007 reached</code>로 멈췄습니다. 한도 10을 적은 실행은 <code>Recursion limit of 10 reached</code>로 멈췄습니다. 두 실행 모두 메서드 <code>invoke</code>가 결과를 내놓지 않아, 찾은 규정 글도 받지 못했습니다.</p><p>After 그래프는 같은 첫 상태와 같은 한도 10으로 실행해, 실행 흔적 <code>['pick', 'find', 'pick']</code>을 남기고 끝났습니다. 둘째 고르기 노드가 빈 글을 적자, 조건 함수가 <code>END</code>를 내놓았습니다. 두 그래프에서 다른 곳은 고르기 노드에서 나가는 엣지 하나였습니다. 새 커널로 두 번 실행했을 때 모든 셀의 출력이 두 번 같았습니다.</p><p>값 바꿔 보기에서는 한도를 바꿨습니다. 노드를 3번 실행하는 대출 흐름은 한도 3에서 멈추고 한도 4에서 통과했습니다. 주제어를 운영과 연체 둘로 바꾼 흐름은 노드를 5번 실행했고, 한도 5에서 멈추고 6에서 통과했습니다. 두 흐름 모두 노드 실행 수보다 하나 큰 한도에서 통과했습니다.</p><p>설치한 langgraph 1.2.11 소스에서는 단계를 시작할 때마다 먼저 한도를 봅니다. 그다음에 실행할 노드가 남았는지 봅니다. 그래서 마지막 노드 뒤, 남은 노드가 없는지 확인하는 차례까지 한도 안에 들어야 합니다. 노트북 밖에서 Before 모양 그래프를 한도 1~5와 10으로 실행해 보니, 한도가 N이면 노드를 N번 실행한 뒤 멈췄습니다.</p>
{{mermaid:""" + FIG4 + "|" + FIG4_ALT + "|" + FIG4_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG4_READ) + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>이 절은 모델을 부르지 않아 모델 요청이 0번이고, API 키 없이 실행합니다. 모델이 낀 흐름은 모델 답에 따라 되풀이 횟수가 달라져, 한도에 닿는 장면을 매번 같게 볼 수 없기 때문입니다.</li><li>고르기 노드는 목록 차례대로 주제어를 고르는 우리 노드입니다. 모델을 흉내 내려는 노드가 아니라, 한도와 끝내는 조건만 보려고 정한 노드입니다.</li><li>주제어(대출, 운영과 연체)와 한도 10은 흐름을 보여 주려고 이 절에서 정한 예입니다. 한도 3·4·5·6은 노드 실행 수 둘레에서 고른 값입니다.</li><li>한도에 닿으면 메서드 <code>invoke</code>는 결과를 내놓지 않습니다. 실행 중 상태를 저장해 두는 체크포인터는 <a href=\"""" + L_CH23_01 + """\">Ch 23 01절</a>에서 다룹니다. 한도에 닿은 실행의 상태를 체크포인터로 읽는 일은 이번에 하지 않았습니다.</li><li>이 설치판의 기본 한도는 10007입니다. 설치판 <code>langgraph/_internal/_config.py</code> 32행에서, 환경 변수 <code>LANGGRAPH_DEFAULT_RECURSION_LIMIT</code>로 바뀐다는 것도 확인했습니다. 공식 문서가 적은 기본 한도는 이와 달라, 참고 자료에 적었습니다.</li><li>한 단계에 노드 여럿이 함께 실행되는 그래프(<a href=\"""" + L_CH13_05 + """\">Ch 13 05절</a>)에서는 노드 실행 수와 단계 수가 다를 수 있습니다. 이 절 그래프는 단계마다 노드 하나라 두 수가 같았고, 여럿인 경우는 이번에 실행하지 않았습니다.</li><li>끝점으로 가는 엣지를 하나도 적지 않은 그래프도, 구조 문자열에는 끝점으로 가는 점선 하나가 그려집니다. 설치판 <code>langgraph/pregel/_draw.py</code> 247~256행에서 그림을 그리는 코드가 이 점선을 스스로 더합니다. 그래서 노트북 4절은 구조 문자열 대신 적어 둔 엣지 수로 Before 그래프를 확인했습니다. Before 그래프의 구조 문자열은 노트북 밖에서 확인했습니다.</li><li>실행 한도는 설정 딕셔너리의 맨 위 키로 넘깁니다. 공식 문서도 이 키를 <code>configurable</code> 안에 넣지 말라고 적습니다.</li><li>01·02절 모델 흐름에 이 절 규칙을 대는 것은 셈입니다. 01절 대출 흐름은 셈으로 한도 4부터 통과하지만, 이번에 실행하지 않았습니다.</li><li>셀의 <code>assert</code>는 모델 없이 우리 코드가 정하는 값, 곧 실행 흔적의 차례와 찾은 규정 수에만 걸었습니다.</li><li>걸린 시간은 재지 않았습니다. 준비물의 실행 시간은 노트북 셀 실행 기록에서 읽은 값입니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>끝점으로 가는 엣지가 없는 그래프는 규정을 다 찾은 뒤에도 되풀이하다, 실행 한도에 닿아 <code>GraphRecursionError</code>로 멈췄습니다.</li><li>조건 함수가 빈 글에서 <code>END</code>를 내놓게 하자, 같은 한도 10 안에서 노드 3번으로 끝났습니다.</li><li>실행 한도는 노드 실행 단계를 세고, 두 흐름 모두 노드 실행 수보다 하나 큰 한도에서 통과했습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_04 + """\">04절</a>에서는 코드의 <code>if</code>로 도구를 고르는 흐름과, 모델이 도구를 고르는 흐름을 견줍니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 끝점으로 가는 엣지가 없는 Before 그래프를 한도를 적지 않고 실행하면 어떻게 되었나요?</p><p class="quiz-a">기본 한도 10007에 닿아 <code>GraphRecursionError</code>로 멈췄습니다. 메서드 <code>invoke</code>가 결과를 내놓지 않아, 찾은 규정 글도 받지 못했습니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">2. 실행 한도는 어디에 적나요?</p><p class="quiz-a">메서드 <code>invoke</code>의 둘째 인자인 설정 딕셔너리에, 키 <code>"recursion_limit"</code>로 적습니다. 상태의 칸도 아니고, <code>configurable</code> 안도 아닙니다. 틀렸다면 노트북 4절과 본문 4 「핵심 개념」의 표를 다시 읽습니다.</p><p class="quiz-q">3. 노드를 3번 실행하고 끝나는 흐름은 한도 3에서 통과했나요?</p><p class="quiz-a">아닙니다. 한도 3에서는 <code>GraphRecursionError</code>가 났고, 한도 4에서 통과했습니다. 그래프가 단계를 시작할 때마다 한도를 먼저 보기 때문입니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">4. 바퀴 한도 <code>turn_limit</code>과 실행 한도는 각각 무엇을 세나요?</p><p class="quiz-a">바퀴 한도는 우리가 쓴 <code>for</code> 루프의 바퀴, 곧 모델 요청 수를 셉니다. 실행 한도는 그래프가 노드를 실행하는 단계 수를 셉니다. 이 절 대출 흐름은 바퀴로 2번, 단계로 3번이었습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langgraph/graph-api">LangGraph Graph API</a></div>확인 2026-09-24 · 실행 한도를 한 번 실행에서 진행할 수 있는 단계 수의 한도로 설명합니다. 이 키를 <code>configurable</code> 안에 넣지 말라고도 적습니다. 문서는 1.0.6부터 기본 한도가 1000 단계라고 적지만, 설치판 1.2.11 소스와 노트북 출력은 10007입니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT">GRAPH_RECURSION_LIMIT 오류 안내</a></div>확인 2026-09-24 · 끝나는 조건 없이 노드 사이를 도는 엣지를 흔한 까닭으로 듭니다. 기본 한도 값은 적지 않습니다.</li><li>langgraph 1.2.11 소스 <code>langgraph/pregel/_loop.py</code> 607행과 653행입니다. 단계를 시작할 때 한도를 먼저 보고, 그다음에 남은 노드가 없으면 끝냅니다.</li><li>같은 소스 <code>langgraph/_internal/_config.py</code> 32행 — 기본 한도 10007과 환경 변수 이름.</li><li>같은 소스 <code>langgraph/pregel/main.py</code> 3005행 — 오류 글 첫 줄을 만드는 자리.</li><li>같은 소스 <code>langgraph/pregel/_draw.py</code> 247~256행 — 끝점 엣지가 없을 때 구조 문자열에 점선을 더하는 자리.</li><li>Ch 13 02·03·07절 — 흔적 칸 규칙, 조건 함수와 이름표 표, 설정 칸.</li><li>Ch 17 03절·Ch 19 05절 — 정지 조건과 바퀴 한도, 함수 <code>ask_until_answer</code>.</li><li>01·02절 — 되돌아가는 엣지와 도구 조건 함수, 도구가 내는 <code>ValueError</code>.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


def same_ast(left: str, right: str) -> bool:
    return ast.dump(ast.parse(left)) == ast.dump(ast.parse(right))


if __name__ == "__main__":
    # 01절 셀과 글자까지 같은 셀
    assert POLICY_DATA == author_01.POLICY_DATA
    # 도구 셀은 01절과 AST가 같고 주석 한 줄만 다르다
    assert same_ast(DEF_TOOL, author_01.DEF_TOOL) and DEF_TOOL != author_01.DEF_TOOL
    if os.environ.get("AUTHOR03_NB_ONLY") != "1":
        print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "03", SLUG, "paired", cells())
        print("wrote", path)
