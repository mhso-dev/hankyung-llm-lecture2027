"""Ch 20 01절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 author_01.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_01.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
  AUTHOR01_NB_ONLY=1 python3 author_01.py → 노트북만 다시 쓴다
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**(chapter.json).

## 결정 1 — 상태 형식과 문법 범위 (챕터 리드 결정 3)

상태 형식은 Ch 13 04절 모양(`class …(TypedDict)` + 메시지 칸 `Annotated[list[AnyMessage], add_messages]`)에 Ch 13 02절
흔적 칸 규칙 `Annotated[list[str], operator.add]`를 더한 `AgentState`. 노드는 자기 몫만 낸다(`{"trace": ["model"]}`).
`MessagesState`는 쓰지 않는다(Ch 13이 가르치지 않음). 게이트 G1은 필드만 적은 `TypedDict` 클래스를 허용한다(Ch 13 선례,
`upgrade_allow` 없음). 노드·도움 함수 타입힌트 0, 반환 힌트 0, `@tool` 매개변수 `: str`만(Ch 19 결정). 조건 함수는 라이브러리
`tools_condition`을 쓰고, 이름표 표 `path_map = {"tools": "tools", END: END}`(Ch 13 03 모양, `'__end__'` 글자 대신 상수).

## 결정 2 — 도구 파일 B안 (챕터 리드 결정 1)

`labs/part5/ch20-tool-node/notebooks/graph_tools.py`를 이 절이 만든다. Ch 19 `order_tools.py`에서 이 절이 쓰는
`tool_call_names`(Ch 19 04)·`show_messages`(Ch 19 06) 둘만 본문을 글자 그대로 옮겼다(AST 소스 조각 대조). import 0.
`sum_usage`·`estimate_cost`는 이 절이 쓰지 않아 넣지 않았다(처음 쓰는 절이 더함 — handoff). 노드 함수는 노트북에 둔다.

## 결정 3 — 흔들림 먼저 확인 (챕터 리드 결정 6, qa/upgrade/01-probe.md)

노트북 밖에서 L(대출)·G(인사)·T(운영·연체) 세 질문을 5번씩(30요청) 보냈다. 흔적·도구 이름·인자·도구 메시지 수·호출 ID 짝이
15/15 같아 입력을 그대로 쓴다. 모델 답에 건 assert는 뺐고, assert는 도구 실행 노드가 옮겨 적는 호출 ID 짝에만 건다.
도구 조건 함수의 동작은 손으로 만든 AIMessage 둘로 모델 없이 보인다(Ch 13 03 「조건 함수만 직접 불러」 모양).

## 모델 요청

노트북 한 번 **6번**(7절 2 · 8절 1 · 9절 3, 모델이 도구를 부르는 수에 따름). 읽는 파일·쓰는 파일 0. 걸린 시간·토큰은 재지 않는다
(주제 아님 — 챕터 리드 결정 5).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`sorted`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·튜플 풀기·세미콜론·
`isinstance`·별표 풀기·`try`·`MessagesState`·`'__end__'` 글자·`recursion_limit`·`perf_counter`·시스템 메시지·`tool_choice`.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part5/ch20-tool-node/notebooks"
SLUG = "01-ToolNode와-tools-condition"
SRC = ROOT / "textbook/part5/ch20-tool-node/_src" / (SLUG + ".html")
# 교재 출력을 만든 실행의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답)에서 읽은 값
RUNSEC = os.environ.get("AUTHOR01_RUNSEC", "10초 안에")

INSTALL = install_source([
    "langgraph==1.2.11", "langchain==1.4.0", "langchain-core==1.6.2", "langchain-openai==1.6.0", "python-dotenv==1.2.3",
])

IMPORTS = r'''# Ch 13 그래프 이름과 Ch 19 도구 이름에, 이 절의 새 이름 둘과 도구 파일 함수 둘을 더해 가져옵니다
import operator
from typing import Annotated
from typing_extensions import TypedDict

from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, AnyMessage, HumanMessage
from langchain.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
# 도구 실행 노드와 도구 조건 함수는 LangGraph가 미리 만들어 둔 부품입니다
from langgraph.prebuilt import ToolNode, tools_condition

from graph_tools import show_messages, tool_call_names

print("이 절에서 새로 가져온 이름:", "ToolNode", "tools_condition")'''

POLICY_DATA = r'''# 교육센터 자료실 규정 셋을, 주제어를 키로 한 딕셔너리에 담습니다(도구가 읽기만 하는 자료)
POLICIES = {
    "대출": "일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.",
    "운영": "평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.",
    "연체": "연체한 일수만큼 새 대출이 제한됩니다.",
}
topics = list(POLICIES.keys())
print("규정 주제어:", topics)'''

DEF_TOOL = r'''# 주제어 하나로 규정 글 하나를 찾는 도구를 만듭니다(맨 @tool 줄 — Ch 19 01절)
@tool
def lookup_policy(topic: str):
    """교육센터 자료실 규정 하나를 주제어로 찾습니다. topic에는 대출, 운영, 연체 가운데 하나를 넣습니다."""
    # 딕셔너리에 없는 주제어면 오류를 냅니다(이 오류를 다루는 법은 02절에서 봅니다)
    if topic not in POLICIES:
        raise ValueError("지원하지 않는 주제: " + topic)
    return POLICIES[topic]'''

TRY_TOOL = r'''# 모델 없이 도구를 인자 딕셔너리로 한 번 불러 봅니다(Ch 19 01절처럼 .invoke)
print("도구 이름:", lookup_policy.name)
print("입력 형식:", lookup_policy.args)
loan_policy = lookup_policy.invoke({"topic": "대출"})
print("대출 규정:", loan_policy)'''

BIND = r'''# 도구 목록을 모델에게 알려 줍니다(Ch 19 04절 bind_tools, 요청은 아직 보내지 않음)
tools = [lookup_policy]
# 한 응답에 도구 호출 요청을 하나까지만 받게 합니다(Ch 19 06절과 같은 값)
bound_model = model.bind_tools(tools, parallel_tool_calls=False)
print("실어 보낼 명세 수:", len(bound_model.kwargs["tools"]))
print("여럿 담기:", bound_model.kwargs["parallel_tool_calls"])'''

STATE = r'''# 메시지 칸과 실행 흔적 칸에 각각 규칙을 적은 상태 형식을 만듭니다(Ch 13 04절 모양)
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    trace: Annotated[list[str], operator.add]'''

CALL_MODEL = r'''# 메시지 칸 전체를 도구를 알려 준 모델에 보내고, 응답 하나와 노드 이름만 냅니다
def call_model(state):
    response = bound_model.invoke(state["messages"])
    return {"messages": [response], "trace": ["model"]}'''

TOOL_NODE = r'''# 도구 목록으로 도구 실행 노드를 만듭니다(아직 그래프에 넣지 않음)
tool_node = ToolNode(tools)
print("만든 것의 종류:", type(tool_node).__name__)
# 속성 tools_by_name은 Ch 19 05절의 도구 찾기 표와 같은 모양입니다
table_keys = list(tool_node.tools_by_name.keys())
print("안에 든 도구 찾기 표의 키:", table_keys)'''

HAND = r'''# 모델을 부르지 않고, 도구 조건 함수에 넣어 볼 응답 두 개를 손으로 만듭니다
plain_answer = AIMessage(content="규정을 찾지 않고 바로 답합니다.")
# 둘째 응답에는 Ch 19 04절의 칸 넷을 담은 도구 호출 요청 하나를 넣습니다
hand_call = {"name": "lookup_policy", "args": {"topic": "대출"}, "id": "hand_call_1", "type": "tool_call"}
hand_request = AIMessage(content="", tool_calls=[hand_call])
print("첫 응답의 도구 호출 요청:", tool_call_names(plain_answer))
print("둘째 응답의 도구 호출 요청:", tool_call_names(hand_request))'''

CONDITION = r'''# 도구 조건 함수를 그래프 없이 직접 불러, 두 응답에 어떤 이름표를 내놓는지 봅니다
plain_label = tools_condition({"messages": [plain_answer]})
request_label = tools_condition({"messages": [hand_request]})
print("요청이 없는 응답의 이름표:", plain_label)
print("요청이 있는 응답의 이름표:", request_label)
print("END와 같은가:", plain_label == END)'''

PATH_MAP = r'''# 도구 조건 함수의 이름표 둘을 실제로 갈 곳에 잇는 이름표 표를 만듭니다(Ch 13 03절)
path_map = {"tools": "tools", END: END}
print("이름표와 갈 곳을 이은 표:")
for label in path_map:
    print(label, "->", path_map[label])'''

NODES = r'''# 설계 객체를 만들고 모델 노드와 도구 실행 노드를 등록합니다
builder = StateGraph(AgentState)
builder.add_node("model", call_model)
builder.add_node("tools", tool_node)
print("등록한 노드:", list(builder.nodes))'''

EDGES = r'''# 시작 엣지, 조건부 엣지, 되돌아가는 엣지를 적고 컴파일합니다
builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition, path_map)
# 도구 실행 노드가 끝나면 앞에 있는 모델 노드로 다시 갑니다
builder.add_edge("tools", "model")
graph = builder.compile()
print("고정 엣지로 적은 수:", len(builder.edges))
print("컴파일 결과의 종류:", type(graph).__name__)'''

STRUCTURE = r'''# 컴파일한 그래프가 스스로 그린 구조 문자열을 받아 옵니다(Ch 13 01절)
structure_text = graph.get_graph().draw_mermaid()
print("그래프가 그린 구조:")
print(structure_text)'''

LOAN_RUN = r'''# 규정을 찾아야 답할 수 있는 질문으로 그래프를 실행합니다(모델 노드를 지날 때마다 모델 요청 1번)
loan_question = "자료실에서 일반 도서를 며칠 빌릴 수 있나요?"
loan_state = {"messages": [HumanMessage(content=loan_question)], "trace": []}
loan_result = graph.invoke(loan_state)
print("실행 흔적 칸:", loan_result["trace"])
print("메시지 칸의 메시지 수:", len(loan_result["messages"]))'''

LOAN_SHOW = r'''# 메시지 칸을 차례로 출력합니다(Ch 19 06절 함수 show_messages)
print("메시지 칸:")
show_messages(loan_result["messages"])'''

LOAN_ARGS = r'''# 둘째 메시지(첫 응답)에 담긴 도구 호출 요청의 이름과 인자를 봅니다
first_response = loan_result["messages"][1]
for call in first_response.tool_calls:
    print("도구 이름:", call["name"], "| 인자:", call["args"])'''

DEF_IDS = r'''# 메시지 목록에서 도구 호출 요청의 id 목록과 도구 메시지의 호출 ID 목록을 모아 내놓습니다
def call_id_lists(messages):
    lists = {"요청 id": [], "호출 ID": []}
    for message in messages:
        if type(message).__name__ == "AIMessage":
            for call in message.tool_calls:
                lists["요청 id"].append(call["id"])
        if type(message).__name__ == "ToolMessage":
            lists["호출 ID"].append(message.tool_call_id)
    return lists'''

LOAN_IDS = r'''# 대출 질문 흐름에서 요청 id 목록과 호출 ID 목록이 같은 차례로 짝이 맞는지 봅니다
loan_ids = call_id_lists(loan_result["messages"])
print("요청 id 수:", len(loan_ids["요청 id"]))
print("호출 ID 수:", len(loan_ids["호출 ID"]))
print("짝이 맞는가:", loan_ids["요청 id"] == loan_ids["호출 ID"])
# 도구 실행 노드가 옮겨 적는 값이라 매번 같아야 합니다
assert loan_ids["요청 id"] == loan_ids["호출 ID"], "도구 메시지마다 같은 차례의 요청 id가 옮겨져야 합니다"'''

LOAN_ANSWER = r'''# 메시지 칸의 마지막 응답을 봅니다(도구 호출 요청 수와 답 글)
last_message = loan_result["messages"][-1]
print("마지막 응답의 도구 호출 요청 수:", len(last_message.tool_calls))
print("답 글:")
print(last_message.content)'''

GREET_RUN = r'''# 규정을 찾을 까닭이 없는 인사 질문으로 같은 그래프를 실행합니다(모델 요청 1번 예상)
greet_question = "안녕하세요. 한 문장으로 인사해 주세요."
greet_state = {"messages": [HumanMessage(content=greet_question)], "trace": []}
greet_result = graph.invoke(greet_state)
print("실행 흔적 칸:", greet_result["trace"])
print("메시지 칸:")
show_messages(greet_result["messages"])
print("답 글:", greet_result["messages"][-1].content)'''

TWO_RUN = r'''# 바꿀 값: 질문 하나만, 규정 두 가지가 필요한 질문으로 바꿔 같은 그래프를 실행합니다
two_question = "자료실 운영 시간과 연체 규정을 함께 알려 주세요."
two_state = {"messages": [HumanMessage(content=two_question)], "trace": []}
two_result = graph.invoke(two_state)
print("실행 흔적 칸:", two_result["trace"])
print("메시지 칸:")
show_messages(two_result["messages"])'''

TWO_ARGS = r'''# 응답마다 도구 호출 요청 수와 인자를 차례로 보고, 호출 ID 짝을 셉니다
for message in two_result["messages"]:
    if type(message).__name__ == "AIMessage":
        print("응답 | 도구 호출 요청 수:", len(message.tool_calls))
        for call in message.tool_calls:
            print("  인자:", call["args"])
two_ids = call_id_lists(two_result["messages"])
print("호출 ID 짝이 맞는가:", two_ids["요청 id"] == two_ids["호출 ID"])'''

DEF_ROW = r'''# 실행 결과 하나를 기록 한 줄로 만듭니다(모델 요청 수 = 실행 흔적 칸의 길이)
def run_row(question_name, result):
    ids = call_id_lists(result["messages"])
    row = {"질문": question_name}
    row["실행 흔적"] = result["trace"]
    row["모델 요청 수"] = len(result["trace"])
    row["도구 메시지 수"] = len(ids["호출 ID"])
    row["호출 ID 짝"] = ids["요청 id"] == ids["호출 ID"]
    return row'''

TABLE = r'''# 세 질문의 기록을 모아 라벨 줄 아래에 한 줄씩 출력합니다
run_rows = []
run_rows.append(run_row("대출 질문", loan_result))
run_rows.append(run_row("인사 질문", greet_result))
run_rows.append(run_row("운영·연체 질문", two_result))
print("질문 | 실행 흔적 | 모델 요청 수 | 도구 메시지 수 | 호출 ID 짝")
for row in run_rows:
    print(row["질문"], "|", row["실행 흔적"], "|", row["모델 요청 수"], "|", row["도구 메시지 수"], "|", row["호출 ID 짝"])'''


FIG1 = "01-1-모델과-도구를-오가는-그래프"
FIG1_ALT = "위에서 아래로 읽는 그림으로 맨 위 회색 가상 시작점 START에서 파란 상자 모델 노드 model 함수 call_model로 화살표가 가고, 모델 노드에서 점선 두 갈래가 나갑니다. 한 갈래는 도구 호출 요청 있음 이름표 tools를 달고 회색 상자 도구 실행 노드 tools ToolNode로, 다른 갈래는 도구 호출 요청 없음 이름표 END를 달고 회색 가상 끝점 END로 갑니다. 도구 실행 노드에서 모델 노드로 되돌아가는 엣지라고 적힌 실선 화살표가 올라가는 그림"
FIG1_CAP = "모델 노드에서 나가는 두 점선 갈래는 도구 조건 함수가 고르고, 도구 실행 노드에서는 되돌아가는 엣지로 모델 노드에 다시 갑니다."
FIG1_READ = """위에서 아래로 읽고, 상자 넷은 노트북 6절 구조 문자열의 상자 넷과 같습니다.
파란 상자는 우리가 적은 모델 노드, 회색 상자는 LangGraph가 준 도구 실행 노드와 가상 시작점·끝점입니다.
모델 노드에서 나가는 점선 두 갈래는 도구 조건 함수가 고르고, 이 함수는 노드가 아니라 상자로 그리지 않았습니다.
도구 실행 노드에서 모델 노드로 올라가는 실선이 되돌아가는 엣지입니다."""

FIG2 = "01-2-대출-질문의-실제-차례"
FIG2_ALT = "세로선 셋이 있는 차례 그림으로 왼쪽부터 노트북 코드 graph.invoke, 연보라 띠 안의 모델 노드 model gpt-5.4-mini, 도구 실행 노드 tools입니다. 노트북 코드가 모델 노드에 질문 하나와 빈 흔적을 보내고, 노란 메모 요청 1 도구 호출 요청 lookup_policy 주제어 대출이 붙습니다. 모델 노드에서 도구 실행 노드로 tools_condition 이름표 tools 화살표가 가고, 노란 메모 도구 메시지 success 1인 5권까지 14일이 붙습니다. 도구 실행 노드에서 모델 노드로 되돌아가는 엣지가 오고, 노란 메모 요청 2 도구 호출 요청 0건 뒤에 모델 노드에서 노트북 코드로 tools_condition END 점선이 가며, 마지막 노란 메모에 흔적 model 두 번, 메시지 넷, 호출 ID 짝 True가 적힌 그림"
FIG2_CAP = "대출 질문에서 그래프는 모델 노드, 도구 실행 노드, 모델 노드 차례로 지나고 두 번째 응답에서 끝났습니다."
FIG2_READ = "위에서 아래로 읽고, 세로선은 왼쪽부터 노트북 코드, 모델 노드, 도구 실행 노드입니다. 연보라 띠는 실제로 부른 모델 `gpt-5.4-mini`가 있는 자리입니다. 요청 1의 응답에 도구 호출 요청이 있어, 도구 조건 함수가 도구 실행 노드로 보냅니다. 되돌아가는 엣지로 모델 노드에 온 뒤, 요청 2의 응답에는 요청이 없어 끝납니다. 노란 메모는 모두 노트북 7절 출력입니다."

FIG3 = "01-3-세-질문의-흔적과-도구-메시지"
FIG3_ALT = "위쪽에 칸 셋이 나란히 있는 그림으로 왼쪽 칸 대출 질문에는 초록 상자 자료실에서 일반 도서를 며칠 빌릴 수 있나요에서 노란 상자 흔적 model 두 번, 모델 요청 두 번, 도구 메시지 하나 대출로 화살표가 갑니다. 가운데 칸 인사 질문에는 초록 상자 안녕하세요 한 문장으로 인사해 주세요에서 노란 상자 흔적 model 한 번, 모델 요청 한 번, 도구 메시지 없음으로 갑니다. 오른쪽 칸 바꾼 값 운영·연체 질문에는 초록 상자 자료실 운영 시간과 연체 규정을 함께 알려 주세요에서 노란 상자 흔적 model 세 번, 모델 요청 세 번, 도구 메시지 둘, 운영 다음 연체로 갑니다. 맨 아래 회색 상자에 세 질문 공통, 같은 그래프, 호출 ID 짝 True, 모델 요청이 도구 메시지보다 하나 많음이 적힌 그림"
FIG3_CAP = "같은 그래프에 질문만 바꾸자 모델 요청은 두 번·한 번·세 번, 도구 메시지는 하나·없음·둘이었습니다."
FIG3_READ = "위쪽 칸 셋은 왼쪽부터 대출·인사·운영과 연체 질문입니다. 초록 상자가 질문이고, 노란 상자가 노트북 10절 출력입니다. 오른쪽 칸이 값 바꿔 보기로 바꾼 질문입니다. 맨 아래 회색 상자는 세 칸 출력에서 모두 확인한 공통점이고, 칸끼리는 화살표로 잇지 않았습니다. 인사 칸의 호출 ID 짝 `True`는 두 목록이 모두 비어 나온 값입니다."

FIG4 = "01-4-for-루프와-그래프"
FIG4_ALT = "위아래 칸 둘이 있는 그림으로 위 칸 Ch 19 05절 우리가 쓴 for 루프에는 파란 상자 bound_model.invoke 모델 요청에서 점선 요청 있음으로 파란 상자 run_tool_calls 도구 실행, 점선 요청 없음으로 파란 둥근 상자 요청이 없으면 break가 나가고, run_tool_calls에서 다음 바퀴 turn_limit까지라는 실선이 모델 요청 상자로 돌아옵니다. 아래 칸 이 절 상태 그래프에는 파란 상자 모델 노드 call_model에서 점선 tools_condition tools로 회색 상자 도구 실행 노드 ToolNode, 점선 tools_condition END로 회색 둥근 상자 가상 끝점 END가 나가고, 도구 실행 노드에서 되돌아가는 엣지 실선이 모델 노드로 오는 그림"
FIG4_CAP = "우리가 쓴 for 루프의 세 자리를 그래프에서는 모델 노드, 도구 실행 노드, 도구 조건 함수와 되돌아가는 엣지가 나눠 맡습니다."
FIG4_READ = "위 칸이 Ch 19 05절 함수 안의 `for` 루프이고, 아래 칸이 이 절 그래프입니다. 두 칸에서 같은 자리에 놓인 상자가 같은 일을 맡습니다. 파란 상자는 우리가 적은 코드이고, 회색은 LangGraph가 준 것입니다. 그래프가 되풀이하는 횟수의 한도는 바퀴 한도 `turn_limit`과 세는 것이 달라, 아래 칸에 그리지 않고 03절에서 봅니다."

ILLU = "01-5-쪽지가-든-승강-상자"
ILLU_ALT = "흰 바탕 그림으로 두 층 자료실 벽을 잘라 보인 모습입니다. 위층에는 긴 나무 창구가 있고, 아래층 왼쪽에는 파란 책이 꽂힌 책장이 있습니다. 벽 속에 회색 승강 통로 둘이 나란히 세로로 나 있습니다. 왼쪽 통로의 나무 상자는 아래층 책장 옆까지 내려가 있고, 상자 위로 흰 종이 쪽지가 반쯤 삐져나와 있으며 파란 책 한 권이 들어 있습니다. 오른쪽 통로의 같은 모양 나무 상자는 위층 창구 앞에 빈 채로 있는 그림"
ILLU_CAP = "쪽지가 든 왼쪽 상자는 서고로 내려가 책을 받았고, 쪽지가 없는 오른쪽 상자는 창구에 그대로 있습니다."
ILLU_READ = "위층에는 긴 나무 창구, 아래층 왼쪽에는 파란 책이 꽂힌 책장이 있습니다. 벽 속 승강 통로 둘 가운데 왼쪽 통로의 상자는 아래층까지 내려가 있습니다. 그 상자에는 흰 쪽지가 반쯤 삐져나와 있고, 파란 책 한 권이 들어 있습니다. 오른쪽 통로의 같은 상자는 위층 창구 앞에 빈 채로 있습니다. 쪽지는 도구 호출 요청, 책은 도구 메시지, 빈 상자는 요청이 없어 끝나는 흐름입니다."

TITLE = """# ToolNode와 tools_condition

**이 노트북에서 할 일**

1. 모델 노드와 도구 실행 노드(`ToolNode`)를 한 그래프에 넣고, 도구 조건 함수(`tools_condition`)로 잇습니다.
2. 규정을 찾아야 하는 질문과 인사 질문을 보내, 그래프가 어느 쪽으로 가는지 봅니다.
3. 규정 두 가지를 묻는 질문으로 바꿔, 그래프가 도구 쪽을 몇 번 다녀오는지 셉니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 교재 출력에서 모델 요청은 모두 6번입니다.
7절에서 2번, 8절에서 1번, 9절에서 3번을 보냈습니다.
모델이 도구를 몇 번 부르느냐에 따라 요청 수가 달라질 수 있습니다.
요금표로 어림한 예상 비용은 모두 합쳐 0.01달러 아래이고, 청구 금액이 아닙니다.

도구는 노트북 안 규정 딕셔너리를 읽기만 하고, 읽는 파일과 새로 쓰는 파일은 없습니다.
Ch 19 함수 둘은 도구 파일 `graph_tools.py`에서 가져옵니다.
교재 출력을 만든 실행에서는 노트북 전체가 """ + RUNSEC + """ 끝났습니다.
모델 응답을 기다리는 시간은 네트워크와 실행 때에 따라 달라집니다.

**기준 버전** — 첫 셀에서 패키지 다섯을 설치합니다.
판은 langgraph 1.2.11, langchain 1.4.0, langchain-core 1.6.2입니다.
langchain-openai 1.6.0과 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3~7절을 읽습니다.
도구와 상태 형식과 두 노드를 만들고, 그래프를 조립해 첫 질문을 보내는 자리입니다.
8~10절은 질문을 바꿔 보내고 세 질문을 견주는 자리이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part5/ch20-tool-node`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""

MAP_TABLE = """- 모델에게 묻는 줄 `bound_model.invoke(messages)`는 모델 노드 `call_model`이 맡습니다.
- 도구를 실행하는 함수 `run_tool_calls`는 도구 실행 노드 `ToolNode(tools)`가 맡습니다.
- 요청이 없으면 멈추는 `break`는 도구 조건 함수가 `END`를 내놓는 일이 맡습니다.
- 목록에 붙이는 `messages.append`는 메시지 칸의 메시지 리듀서 `add_messages`가 맡습니다.
- 되풀이하는 `for` 루프는 되돌아가는 엣지 `tools → model`이 맡고, 한도는 03절에서 봅니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

Ch 19 05절에서는 도구 호출 요청을 실행하고 다시 묻는 일을 우리가 쓴 함수 `ask_until_answer`가 했습니다.
이 절에서는 같은 일을 Ch 13의 상태 그래프가 맡습니다.
제목의 `ToolNode`는 도구 실행 노드, `tools_condition`은 도구 조건 함수이고, 뜻은 5절에서 풉니다.

첫 셀은 패키지 다섯 개를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langgraph: 1.2.11`·`langchain: 1.4.0`·`langchain-core: 1.6.2`가 보입니다.
출력 줄 `langchain-openai: 1.6.0`과 `python-dotenv: 1.2.3`도 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
상태 형식·메시지·그래프 이름은 Ch 13 04절, 모델과 `tool`은 Ch 19에서 쓴 이름입니다.
새 이름은 모듈 `langgraph.prebuilt`에서 가져오는 `ToolNode`와 `tools_condition` 둘입니다.
도구 파일에서는 Ch 19 함수 `show_messages`와 `tool_call_names`를 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `이 절에서 새로 가져온 이름: ToolNode tools_condition`이 보입니다.
모듈 `langgraph.prebuilt`는 LangGraph가 미리 만들어 둔 부품을 모아 둔 곳입니다.

앞에서 배운 함수는 `graph_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.

이 파일은 Ch 19 도구 파일 `order_tools.py`와 다른 파일입니다.
이 챕터 노트북이 쓰는 Ch 19 함수만 본문을 글자 그대로 옮겼습니다.
함수 `tool_call_names`는 Ch 19 04절, 함수 `show_messages`는 Ch 19 06절에서 배웠습니다.
이 절에서 만드는 함수 `call_id_lists`·`run_row`도 뒤 절이 쓰도록, 본문을 글자 그대로 이 파일에 옮겨 두었습니다.

## 2. 키와 모델 준비

모델은 Ch 19와 같은 `gpt-5.4-mini`이고, 과정의 같은 설정으로 부릅니다."""),
    ] + key_and_model_cells(
        "openai:gpt-5.4-mini",
        "temperature 값을 0으로 두어도, 모델이 도구 호출 요청을 보낼지가 매번 같다고 보장하지는 않습니다.",
    ) + [
        md("""## 3. 규정 자료와 도구

이 챕터는 교육센터 자료실 규정을 소재로 씁니다.
규정은 대출·운영·연체 세 가지이고, 노트북 안 딕셔너리에 적어 둡니다.
다음 셀은 주제어를 키, 규정 글을 값으로 둔 딕셔너리를 만듭니다."""),
        code(POLICY_DATA),
        md("""**결과 읽기** — 출력 줄 `규정 주제어: ['대출', '운영', '연체']`로 키 셋을 확인합니다.
도구는 이 딕셔너리를 읽기만 하고 바꾸지 않으므로, Ch 19 06절 말로 읽기 도구입니다.

다음 셀은 주제어 하나로 규정 글 하나를 찾는 도구를 만듭니다.
맨 `@tool` 줄과 독스트링, 매개변수의 `: str` 표시는 Ch 19 01절에서 배운 모양입니다.
딕셔너리에 없는 주제어면 Ch 16 01절처럼 `raise`로 오류를 냅니다.
이 오류를 그래프 안에서 어떻게 다루는지는 02절에서 봅니다."""),
        code(DEF_TOOL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
독스트링은 도구 설명이 되어 모델 요청에 실립니다.
설명에 주제어 셋을 적어, 모델이 인자에 무엇을 넣을지 알게 했습니다.

다음 셀은 모델 없이 도구를 한 번 불러 봅니다.
Ch 19 01절처럼 메서드 `.invoke`에 인자 딕셔너리를 넣습니다."""),
        code(TRY_TOOL),
        md("""**결과 읽기** — 출력 줄 `도구 이름: lookup_policy`는 함수 이름에서 왔습니다.
라벨 `입력 형식:` 뒤 딕셔너리에서 인자 `topic`의 자료형은 `string`입니다.
출력 줄 `대출 규정: 일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.`로 도구가 규정 글을 내놓았습니다.

다음 셀은 도구 목록을 메서드 `bind_tools`로 모델에게 알려 줍니다.
인자 `parallel_tool_calls=False`는 한 응답에 도구 호출 요청을 하나까지만 받게 합니다.
Ch 19 06절과 같은 값이고, 규정을 둘 찾아야 할 때의 흐름은 9절에서 봅니다."""),
        code(BIND),
        md("""**결과 읽기** — 출력 줄 `실어 보낼 명세 수: 1`은 도구 하나의 명세가 요청마다 실린다는 뜻입니다.
출력 줄 `여럿 담기: False`처럼 여럿 담기를 끈 값도 함께 실립니다.
아직 모델 요청은 보내지 않았습니다.

## 4. 상태 형식과 모델 노드

그래프에 넣을 상태 형식을 정합니다.
메시지 칸에는 Ch 13 04절처럼 메시지 리듀서 `add_messages`를 적습니다.
실행 흔적 칸에는 Ch 13 02절처럼 이어 붙이기 규칙 `operator.add`를 적습니다.
두 칸 모두 규칙이 있으므로, 노드는 자기 몫만 내면 됩니다.
칸 구성이 Ch 13 04절 `ChatState`와 달라서 새 이름 `AgentState`를 붙입니다."""),
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
메시지 칸 `messages`에는 질문·응답·도구 메시지가 차례로 쌓입니다.
실행 흔적 칸 `trace`에는 노드가 낸 이름이 뒤에 붙습니다.

다음 셀은 모델 노드 함수입니다.
모델 노드는 메시지 칸 전체를 모델에 보내고, 받은 응답을 메시지 칸에 더하는 노드입니다.
함수는 응답 하나와 노드 이름 `"model"`만 담은 딕셔너리를 냅니다.
그래프는 노드 함수에 상태 하나만 넘기므로, 모델은 앞 셀의 `bound_model`을 그대로 씁니다."""),
        code(CALL_MODEL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 노드를 한 번 지날 때마다 모델 요청이 한 번 나갑니다.
그래서 실행 흔적 칸에 붙은 `model`의 수가 곧 모델 요청 수입니다.

## 5. 도구 실행 노드와 도구 조건 함수

Ch 19 05절에서는 도구 호출 요청을 우리가 쓴 함수 `run_tool_calls`로 실행했습니다.
이 절에서는 그 일을 LangGraph가 미리 만들어 둔 노드가 맡습니다.
도구 실행 노드(`ToolNode`)는 마지막 응답의 도구 호출 요청을 실행하는 노드입니다.
실행 결과는 도구 메시지로 만들어 메시지 칸에 더합니다.
다음 셀은 도구 목록으로 도구 실행 노드를 만듭니다."""),
        code(TOOL_NODE),
        md("""**결과 읽기** — 출력 줄 `만든 것의 종류: ToolNode`입니다.
출력 줄 `안에 든 도구 찾기 표의 키: ['lookup_policy']`처럼, 노드 안에 도구 찾기 표가 들어 있습니다.
Ch 19 05절에서 우리가 만든 표 `tools_by_name`과 같은 모양입니다.

다음은 조건부 엣지에 넣을 조건 함수입니다.
도구 조건 함수(`tools_condition`)는 LangGraph가 미리 만들어 둔 조건 함수입니다.
마지막 응답에 도구 호출 요청이 있으면 이름표 `"tools"`를, 없으면 가상 끝점 `END`를 내놓습니다.
Ch 13 03절 조건 함수처럼 노드로 등록하지 않고 조건부 엣지에 넣습니다.

그래프 없이 이 함수를 불러 보려고, 다음 셀은 응답 두 개를 손으로 만듭니다.
Ch 13 04절처럼 `AIMessage`를 직접 만들고, 둘째 응답에만 도구 호출 요청을 넣습니다."""),
        code(HAND),
        md("""**결과 읽기** — 출력 줄 `첫 응답의 도구 호출 요청: []`은 요청이 없는 응답이라는 뜻입니다.
출력 줄 `둘째 응답의 도구 호출 요청: ['lookup_policy']`는 요청 하나를 담은 응답입니다.
두 응답은 우리가 손으로 만든 것이고, 모델이 쓴 응답이 아닙니다.

다음 셀은 도구 조건 함수에 두 응답을 하나씩 넣어, 내놓는 이름표를 봅니다.
그래프의 상태처럼 키 `messages`에 메시지 목록을 담아 넘깁니다."""),
        code(CONDITION),
        md("""**결과 읽기** — 출력 줄 `요청이 없는 응답의 이름표: __end__`입니다.
출력 줄 `요청이 있는 응답의 이름표: tools`입니다.
출력 줄 `END와 같은가: True`로, 글자 `__end__`가 가상 끝점 `END`의 값임을 확인합니다.
이 함수는 질문의 낱말이나 답의 내용은 보지 않고, 마지막 응답의 도구 호출 요청이 있는지만 봅니다.
설치한 langgraph-prebuilt 1.1.0 소스도 요청의 개수가 0보다 큰지만 봅니다.

다음 셀은 두 이름표를 실제로 갈 곳에 잇는 이름표 표(`path_map`)를 만듭니다.
Ch 13 03절처럼 딕셔너리로 적고, 끝 쪽에는 글자 대신 상수 `END`를 씁니다."""),
        code(PATH_MAP),
        md("""**결과 읽기** — 라벨 줄 `이름표와 갈 곳을 이은 표:` 아래 두 줄입니다.
출력 줄 `tools -> tools`는 이름표 `"tools"`가 오면 이름이 `tools`인 노드로 간다는 뜻입니다.
출력 줄 `__end__ -> __end__`는 `END`가 오면 가상 끝점으로 가서 끝난다는 뜻입니다.
그래서 도구 실행 노드는 다음 셀에서 이름 `"tools"`로 등록합니다.

## 6. 그래프 조립과 되돌아가는 엣지

다음 셀은 설계 객체를 만들고 노드 둘을 등록합니다.
모델 노드는 이름 `"model"`, 도구 실행 노드는 이름 `"tools"`입니다."""),
        code(NODES),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['model', 'tools']`입니다.
도구 조건 함수는 노드가 아니므로 이 목록에 없습니다.

다음 셀은 엣지 셋을 적고 컴파일합니다.
시작 엣지와 조건부 엣지는 Ch 13 01·03절에서 배운 모양입니다.
셋째 줄 `builder.add_edge("tools", "model")`은 이 과정에서 처음 보는 모양입니다.
지금까지 엣지는 앞 노드에서 뒤 노드로만 갔습니다.
이 엣지는 뒤에 있는 도구 실행 노드에서 앞의 모델 노드로 되돌아가, 모델 노드를 다시 지나게 합니다."""),
        code(EDGES),
        md("""**결과 읽기** — 출력 줄 `고정 엣지로 적은 수: 2`는 시작 엣지와 셋째 줄 엣지입니다.
조건부 엣지는 이 수에 들어가지 않고 따로 적힙니다.
출력 줄 `컴파일 결과의 종류: CompiledStateGraph`로 컴파일이 끝났습니다.
셋째 줄 엣지처럼 뒤 노드에서 앞 노드로 다시 가는 엣지를, 이 절에서는 되돌아가는 엣지라고 부릅니다.

다음 셀은 Ch 13 01절처럼 그래프가 스스로 그린 구조 문자열을 받아 옵니다."""),
        code(STRUCTURE),
        md("""**결과 읽기** — 라벨 줄 `그래프가 그린 구조:` 아래에서 화살표 줄 넷을 봅니다.
줄 `model -.-> __end__`와 `model -.-> tools`는 조건부 엣지의 두 갈래라 점선입니다.
줄 `tools --> model`이 되돌아가는 엣지이고, 실선입니다.
도구 조건 함수는 상자가 아니라 모델 노드에서 나가는 점선 두 줄로만 나타납니다.

## 7. 도구가 필요한 질문

첫 질문은 자료실 규정을 찾아야 답할 수 있는 질문입니다.
상태에는 메시지 칸에 질문 하나, 실행 흔적 칸에 빈 목록을 넣습니다.
실행 전에 예상해 봅니다.
모델이 대출 규정을 찾는 요청을 보내면, 흐름은 모델 노드 → 도구 실행 노드 → 모델 노드일 것입니다."""),
        code(LOAN_RUN),
        md("""**결과 읽기** — 출력 줄 `실행 흔적 칸: ['model', 'model']`로 모델 노드를 두 번 지났습니다.
그래서 이 질문의 모델 요청은 2번입니다.
출력 줄 `메시지 칸의 메시지 수: 4`입니다.
도구 실행 노드는 실행 흔적 칸을 쓰지 않으므로, 도구 실행은 메시지 칸에서 봅니다.

다음 셀은 Ch 19 06절 함수 `show_messages`로 메시지 칸을 차례로 출력합니다."""),
        code(LOAN_SHOW),
        md("""**결과 읽기** — 라벨 줄 `메시지 칸:` 아래 네 줄이 메시지 칸의 차례입니다.
질문 다음 줄은 `AIMessage | 도구 호출 요청: ['lookup_policy']`입니다.
셋째 줄 도구 메시지는 결과 상태가 `success`이고, 내용은 대출 규정 글입니다.
넷째 줄 `AIMessage | 도구 호출 요청: []`는 요청이 없는 응답이라, 도구 조건 함수가 `END`로 보냈습니다.
도구 메시지가 더해진 뒤 되돌아가는 엣지로 모델 노드에 다시 간 것입니다.

다음 셀은 첫 응답에 담긴 도구 호출 요청의 이름과 인자를 봅니다."""),
        code(LOAN_ARGS),
        md("""**결과 읽기** — 출력 줄 `도구 이름: lookup_policy | 인자: {'topic': '대출'}`입니다.
모델이 질문을 읽고 주제어 `대출`을 골라 인자에 넣었습니다.
도구를 부를지와 인자는 모델이 정했고, 도구를 실행한 것은 도구 실행 노드입니다.

다음 셀은 메시지 목록에서 요청 id 목록과 호출 ID 목록을 모으는 함수입니다.
호출 ID는 Ch 19 05절에서 본, 도구 메시지가 어느 요청의 결과인지 알리는 번호입니다.
Ch 19 05절은 이 짝을 셀 안에서 견줬고, 여기서는 세 질문에 쓰려고 함수로 만듭니다."""),
        code(DEF_IDS),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `call_id_lists`는 키 둘(`요청 id`·`호출 ID`)에 목록을 담은 딕셔너리를 내놓습니다.
응답이면 도구 호출 요청마다 칸 `id`를, 도구 메시지면 칸 `tool_call_id`를 모읍니다.

다음 셀은 대출 질문 흐름에서 두 목록의 짝이 맞는지 봅니다.
이 목록은 도구 실행 노드가 옮겨 적은 값이라, 모델이 요청을 몇 건 보내든 짝이 맞아야 합니다.
그래서 셀 끝에서 `assert`로 확인합니다."""),
        code(LOAN_IDS),
        md("""**결과 읽기** — 출력 줄 `요청 id 수: 1`과 `호출 ID 수: 1`입니다.
출력 줄 `짝이 맞는가: True`로, 도구 실행 노드가 요청 `id`를 도구 메시지에 옮겨 적었습니다.
Ch 19 05절에서 우리가 도구에 요청을 통째로 넣어 하던 일과 같습니다.
칸 `id`의 값은 요청마다 새로 붙어 실행마다 다르므로, 여기에 옮겨 적지 않습니다.

다음 셀은 메시지 칸의 마지막 응답을 봅니다."""),
        code(LOAN_ANSWER),
        md("""**결과 읽기** — 출력 줄 `마지막 응답의 도구 호출 요청 수: 0`입니다.
라벨 줄 `답 글:` 아래가 모델이 도구 메시지를 읽고 쓴 최종 답입니다.

답 글의 문장은 실행마다 달라질 수 있어, 결론에 쓰지 않습니다.
이번 실행에서는 답 글에 도구 메시지의 `5권`과 `14일`이 들어 있었습니다.
답 글의 별표 두 개(`**`)는 모델이 굵은 글씨를 표시하려고 붙인 기호입니다.

## 8. 도구가 필요 없는 질문

둘째 질문은 규정을 찾을 까닭이 없는 인사입니다.
같은 그래프에 질문만 바꿔 넣습니다.
실행 전에 예상해 봅니다.
모델이 도구 호출 요청 없이 바로 답하면, 흐름은 모델 노드 한 번으로 끝날 것입니다."""),
        code(GREET_RUN),
        md("""**결과 읽기** — 출력 줄 `실행 흔적 칸: ['model']`로 모델 노드를 한 번만 지났습니다.
라벨 줄 `메시지 칸:` 아래는 `HumanMessage`와 `AIMessage | 도구 호출 요청: []` 두 줄입니다.
첫 응답에 요청이 없어, 도구 조건 함수가 바로 `END`로 보냈습니다.
도구 실행 노드는 한 번도 실행되지 않았고, 모델 요청은 1번입니다.

답 글은 실행마다 달라질 수 있습니다.
이번 실행에서는 `안녕하세요, 반갑습니다!`였습니다.
노트북 밖에서 이 질문을 다섯 번 보냈을 때도 다섯 번 모두 도구 호출 요청이 없었습니다.
답 글은 문장부호만 조금씩 달랐습니다.

## 9. 값 바꿔 보기 · 규정 두 가지를 묻는 질문

바꿀 값은 질문 하나입니다.
운영 시간과 연체 규정을 함께 묻는, 규정 두 가지가 필요한 질문으로 바꿉니다.
그래프와 도구, 여럿 담기를 끈 설정은 그대로입니다.
실행 전에 예상해 봅니다.
응답마다 요청이 하나까지만 오므로, 도구 쪽을 두 번 다녀오고 모델 요청은 3번일 것입니다."""),
        code(TWO_RUN),
        md("""**결과 읽기** — 출력 줄 `실행 흔적 칸: ['model', 'model', 'model']`로 모델 노드를 세 번 지났습니다.
라벨 줄 `메시지 칸:` 아래 여섯 줄에서 응답과 도구 메시지가 번갈아 나옵니다.
도구 메시지 둘은 모두 결과 상태가 `success`입니다.
되돌아가는 엣지를 두 번 지났고, 모델 요청이 세 번이라 Ch 19 05절 말로 바퀴가 세 번 돌았습니다.

다음 셀은 응답마다 도구 호출 요청 수와 인자를 보고, 호출 ID 짝을 셉니다."""),
        code(TWO_ARGS),
        md("""**결과 읽기** — 첫 응답은 요청 한 건이고, 인자는 `{'topic': '운영'}`입니다.
둘째 응답도 한 건이고, 인자는 `{'topic': '연체'}`입니다.
셋째 응답은 `응답 | 도구 호출 요청 수: 0`이라 최종 답입니다.
출력 줄 `호출 ID 짝이 맞는가: True`로, 두 도구 메시지 모두 짝이 맞았습니다.

Ch 19 05절 하나씩 흐름처럼, 요청이 응답마다 한 건씩 나뉘어 왔습니다.
그때는 바퀴 한도 `turn_limit`를 둔 `for` 루프가 되풀이를 맡았습니다.
이 그래프에는 그런 `for`가 없고, 도구 조건 함수가 `END`를 고를 때까지 그래프가 스스로 되풀이합니다.
그래프가 되풀이하는 횟수에도 한도가 있고, 그 한도는 03절에서 다룹니다.

## 10. 세 질문 견주기

다음 셀은 실행 결과 하나를 기록 한 줄로 만드는 함수입니다.
모델 요청 수는 실행 흔적 칸의 길이로, 도구 메시지 수는 호출 ID 목록의 길이로 셉니다."""),
        code(DEF_ROW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `run_row`는 칸 다섯을 담은 딕셔너리를 내놓습니다.
칸은 질문·실행 흔적·모델 요청 수·도구 메시지 수·호출 ID 짝입니다.

다음 셀은 세 질문의 기록을 모아 한 줄씩 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 세 줄입니다.
대출 질문은 `대출 질문 | ['model', 'model'] | 2 | 1 | True`입니다.
인사 질문은 `인사 질문 | ['model'] | 1 | 0 | True`입니다.
바꾼 질문은 `운영·연체 질문 | ['model', 'model', 'model'] | 3 | 2 | True`입니다.

인사 질문의 짝 `True`는 요청 id 목록과 호출 ID 목록이 모두 비어 있어 나온 값입니다.
세 질문 모두 모델 요청 수가 도구 메시지 수보다 하나 많았습니다.
여럿 담기를 꺼서, 도구 호출 요청이 있는 응답마다 도구 메시지가 하나였습니다.
마지막 응답은 늘 도구 호출 요청이 없는 응답이라, 그 요청 한 번만큼 많습니다.

세 흐름은 같은 그래프였고, 도구 쪽으로 몇 번 갈지는 모델의 응답이 정했습니다.
노트북 밖에서 세 질문을 다섯 번씩 보냈을 때도 세 줄의 값이 모두 같았습니다.

Ch 19 05절 함수 `ask_until_answer`의 줄마다 이 그래프에서 맡는 곳은 아래와 같습니다.

""" + MAP_TABLE + """

## 정리

1. 도구 조건 함수는 마지막 응답에 도구 호출 요청이 있으면 도구 실행 노드로, 없으면 `END`로 보냈습니다.
2. 도구 실행 노드가 도구 메시지를 더하면, 되돌아가는 엣지로 모델 노드에 다시 갔습니다.
3. 대출·인사·운영과 연체 질문의 모델 요청은 2·1·3번, 도구 메시지는 1·0·2개였습니다.

02절에서는 도구 실행 노드가 실행한 도구가 오류를 낼 때를 봅니다.
Ch 19 06절에서 도구 속성으로 하던 일을 도구 실행 노드 쪽에서 다룹니다."""),
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


L_CH13_01 = "../../part4/ch13-langgraph-basics/01-StateGraph와-노드-엣지.html"
L_CH13_02 = "../../part4/ch13-langgraph-basics/02-State-갱신.html"
L_CH13_03 = "../../part4/ch13-langgraph-basics/03-조건부-엣지.html"
L_CH13_04 = "../../part4/ch13-langgraph-basics/04-add_messages-리듀서.html"
L_CH17_03 = "../ch17-agent-overview/03-모델-도구-루프와-정지-조건.html"
L_CH18_01 = "../ch18-workflow-patterns/01-게이트가-있는-프롬프트-체이닝.html"
L_CH19_01 = "../ch19-model-tools/01-tool과-Ch4-함수-재사용.html"
L_CH19_04 = "../ch19-model-tools/04-설명만으로-도구-선택하기.html"
L_CH19_05 = "../ch19-model-tools/05-bind_tools와-병렬-호출.html"
L_CH19_06 = "../ch19-model-tools/06-오류와-읽기-쓰기-분리.html"
L_02 = "02-도구-오류와-ToolMessage.html"
L_03 = "03-recursion-limit과-명시적-종료.html"

READ_LOAN_ANSWER_SRC = "답 글은 실행마다 달라질 수 있어 결론에 쓰지 않았습니다. 교재 출력에서는 대출 답 글에 규정 글의 5권과 14일이 들어 있었습니다."


def map_table_html() -> str:
    rows = [
        ("<code>bound_model.invoke(messages)</code>로 모델 요청", "모델 노드 <code>call_model</code>"),
        ("<code>run_tool_calls(response, tools_by_name)</code>로 도구 실행", "도구 실행 노드 <code>ToolNode(tools)</code>"),
        ("도구 호출 요청이 없으면 <code>break</code>", "도구 조건 함수 <code>tools_condition</code>이 <code>END</code>를 내놓음"),
        ("<code>messages.append(…)</code>로 목록에 붙이기", "메시지 칸의 메시지 리듀서 <code>add_messages</code>"),
        ("<code>for turn in range(turn_limit)</code>로 되풀이", "되돌아가는 엣지 <code>tools → model</code>(한도는 03절)"),
    ]
    body = ""
    for left, right in rows:
        body = body + "<tr><td>" + left + "</td><td>" + right + "</td></tr>"
    return ("<table><thead><tr><th>Ch 19 05절 함수 <code>ask_until_answer</code></th><th>이 절 그래프</th></tr></thead><tbody>"
            + body + "</tbody></table>")


def src_html() -> str:
    return """<!--meta: 강의 1h | 실습 1.5h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 4 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>모델 노드와 도구 실행 노드(<code>ToolNode</code>)를 한 상태 그래프에 등록하고, 도구 조건 함수(<code>tools_condition</code>)로 이을 수 있습니다.</li>
<li>도구 조건 함수가 마지막 응답의 무엇을 보고 다음 갈 곳을 고르는지 설명할 수 있습니다.</li>
<li>실행 흔적 칸과 메시지 칸으로, 그래프가 도구 쪽을 몇 번 다녀왔는지 셀 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_CH19_05 + """\">Ch 19 05절</a>에서는 도구 호출 요청을 실행하고 모델에게 다시 묻는 일을 우리가 쓴 함수로 했습니다. 함수 <code>ask_until_answer</code> 안의 <code>for</code> 루프가 응답마다 요청이 있는지 보고, 있으면 도구를 실행했습니다. 요청이 없는 응답이 오면 <code>break</code>로 멈췄습니다.</p><p><a href=\"""" + L_CH13_01 + """\">Ch 13</a>에서는 노드와 엣지로 흐름을 그래프에 적었습니다. 그런데 Ch 13의 그래프는 앞에서 뒤로만 흘렀고, 같은 노드를 다시 지나지 않았습니다. <a href=\"""" + L_CH18_01 + """\">Ch 18</a>의 다섯 패턴에서도 다음 단계를 고른 쪽은 늘 코드였습니다.</p><p>이 절은 Ch 19 05절의 되풀이를 상태 그래프로 옮깁니다. 모델이 도구 호출 요청을 보내면 그래프가 도구를 실행하러 가고, 보내지 않으면 끝납니다. 어느 쪽으로 갈지는 모델의 응답이 정합니다. Ch 21에서는 <code>create_agent</code> 호출 한 줄로 같은 되풀이 구조를 만듭니다. 그 안에서 무엇이 도는지 읽으려면 이 절의 그래프를 알아야 합니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH13_01 + """\">Ch 13 01절</a>에서는 상태 형식·노드·엣지로 상태 그래프를 만들고, 구조 문자열을 받아 보았습니다. <a href=\"""" + L_CH13_02 + """\">02절</a>에서는 칸에 이어 붙이기 규칙을 적고, 노드가 자기 몫만 내게 했습니다. <a href=\"""" + L_CH13_03 + """\">03절</a>에서는 조건 함수가 내놓은 이름표를 이름표 표(<code>path_map</code>)로 노드에 이었습니다. <a href=\"""" + L_CH13_04 + """\">04절</a>에서는 메시지 칸에 메시지 리듀서 <code>add_messages</code>를 적었습니다. 이 절의 상태 형식은 04절 모양에 02절 흔적 칸 규칙을 더한 것입니다.</p><p><a href=\"""" + L_CH17_03 + """\">Ch 17 03절</a>에서는 모델이 도구를 고르고 코드가 실행하는 일을 되풀이하는 루프를 보았습니다. 루프가 한 번 도는 것을 바퀴, 루프를 멈추는 조건을 정지 조건이라고 불렀습니다. 이 절의 그래프는 모델이 도구 호출 요청 없이 답하면 멈춥니다. Ch 17 03절 정지 조건 가운데 「모델의 끝 선택」에 해당합니다.</p><p><a href=\"""" + L_CH19_01 + """\">Ch 19 01절</a>에서는 <code>@tool</code>로 도구를 만들었고, <a href=\"""" + L_CH19_04 + """\">04절</a>에서는 <code>bind_tools</code>로 도구를 모델에게 알려 주었습니다. 05절에서는 도구 호출 요청을 실행해 도구 메시지를 만들고, 호출 ID로 짝을 맞췄습니다. <a href=\"""" + L_CH19_06 + """\">06절</a>에서는 도구 메시지의 결과 상태를 보았고, 함수 <code>show_messages</code>로 메시지를 읽었습니다. 이 절은 그 함수와 04절 함수 <code>tool_call_names</code>를 도구 파일 <code>graph_tools.py</code>에서 가져옵니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>두 층으로 된 자료실을 떠올려 봅니다. 위층 창구에서는 사서가 질문을 받고, 아래층 서고에는 규정 책이 있습니다. 두 층은 벽 속의 작은 승강 상자로 이어져 있습니다. 음식이나 물건을 층 사이로 올리고 내리는 작은 승강기입니다.</p><p>사서는 규정을 찾아야 하면 요청 쪽지를 적어 상자에 넣습니다. 쪽지가 든 상자는 서고로 내려가고, 서고에서는 쪽지대로 규정 책을 찾아 상자에 실어 올려 보냅니다. 찾을 것이 없으면 사서는 쪽지를 넣지 않고 바로 답하고, 상자는 창구에 그대로 있습니다.</p><p>사서는 모델이고, 창구는 모델 노드입니다. 요청 쪽지는 도구 호출 요청, 서고는 도구 실행 노드, 올라온 책은 도구 메시지입니다. 쪽지가 있는지 보고 상자를 내려보낼지 정하는 일이 도구 조건 함수입니다. 상자가 다시 창구로 올라오는 길이 되돌아가는 엣지입니다. Ch 19의 식당에서는 우리가 전표를 들고 주방을 오갔지만, 이 자료실에서는 승강 상자가 그 오가기를 맡습니다.</p>
{{img:""" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + """}}
<p class="look"><b>그림 읽기</b> — """ + ILLU_READ + """</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>모델 노드</td><td>도구를 알려 준 모델에 메시지 칸 전체를 보내고, 받은 응답을 메시지 칸에 더하는 노드입니다. 자료실의 창구와 같습니다.</td></tr><tr><td>도구 실행 노드(ToolNode)</td><td>마지막 응답의 도구 호출 요청을 실행하고, 결과를 도구 메시지로 메시지 칸에 더하는 노드입니다. LangGraph가 미리 만들어 둔 노드입니다. 아래층 서고와 같습니다.</td></tr><tr><td>도구 조건 함수(tools_condition)</td><td>마지막 응답에 도구 호출 요청이 있으면 이름표 <code>"tools"</code>를, 없으면 <code>END</code>를 내놓는 조건 함수입니다. LangGraph가 미리 만들어 둔 함수입니다. 쪽지가 있는지 보고 상자를 내려보낼지 정하는 일과 같습니다.</td></tr><tr><td>되돌아가는 엣지</td><td>뒤에 있는 노드에서 앞의 노드로 다시 가는 엣지입니다. 그래프가 같은 노드를 다시 지나게 합니다. 상자가 창구로 다시 올라오는 길과 같습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 모델 노드는 함수 <code>call_model</code>이고, 이름 <code>"model"</code>로 등록합니다. 도구 실행 노드는 <code>ToolNode(tools)</code>로 만들어 이름 <code>"tools"</code>로 등록합니다. 도구 조건 함수는 <code>builder.add_conditional_edges("model", tools_condition, path_map)</code>에 들어갑니다. 되돌아가는 엣지는 <code>builder.add_edge("tools", "model")</code> 한 줄입니다.</p>
{{mermaid:""" + FIG1 + "|" + FIG1_ALT + "|" + FIG1_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG1_READ) + """</p>
<h3>Ch 19 05절의 되풀이와 견주기</h3><p>이 그래프는 Ch 19 05절 함수 <code>ask_until_answer</code>가 하던 일을 나눠 맡습니다. 아래 표의 왼쪽이 그 함수의 줄이고, 오른쪽이 이 절 그래프에서 같은 일을 맡은 부분입니다.</p>
""" + map_table_html() + """
{{mermaid:""" + FIG4 + "|" + FIG4_ALT + "|" + FIG4_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG4_READ) + """</p>
<h3>다른 상황에 적용</h3><p>Ch 19의 주문 도구를 넣는다면, 도구 목록을 바꿔 모델에게 다시 알리고 도구 실행 노드를 새로 만들면 됩니다. 그래프 모양은 그대로입니다. 모델이 주문 번호가 든 질문에 요청을 보내면 도구 실행 노드가 주문을 찾고, 모델이 도구 메시지를 읽고 답합니다. 이 조합은 이번에 실행하지 않았습니다.</p>
<h3>비교와 경계</h3><p>도구 조건 함수는 답이 맞는지 보지 않습니다. 마지막 응답에 도구 호출 요청이 있는지만 봅니다. 그래서 모델이 요청을 끝없이 보내면 그래프도 계속 되풀이됩니다. 그래프가 되풀이하는 횟수의 한도는 <a href=\"""" + L_03 + """\">03절</a>에서, 도구가 오류를 낼 때는 <a href=\"""" + L_02 + """\">02절</a>에서 봅니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 규정 딕셔너리와 도구를 만들고, 도구를 모델에게 알려 줍니다. 상태 형식과 모델 노드를 정의하고, 도구 실행 노드와 도구 조건 함수를 따로 불러 봅니다. 그래프를 조립한 뒤 대출 질문과 인사 질문을 보내고, 값 바꿔 보기로 운영과 연체를 함께 묻는 질문을 보냅니다. 마지막으로 세 질문의 실행 흔적과 도구 메시지 수를 견줍니다.</p><p>모델은 <code>gpt-5.4-mini</code>이고, temperature 0과 추론 끔(<code>reasoning_effort="none"</code>)으로 부릅니다. 교재 출력에서 모델 요청은 모두 6번입니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — 노트북 7절 출력 <code>실행 흔적 칸: ['model', 'model']</code>과 메시지 네 줄로, 도구 쪽을 한 번 다녀왔는지 봅니다. 노트북 8절 출력 <code>실행 흔적 칸: ['model']</code>로, 도구 없이 끝났는지 봅니다. 노트북 10절 표에서 세 질문의 모델 요청 수와 도구 메시지 수를 견줍니다. """ + READ_LOAN_ANSWER_SRC + """</p>
{{mermaid:""" + FIG2 + "|" + FIG2_ALT + "|" + FIG2_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG2_READ) + """</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>실험에서 바꾼 것은 질문 하나이고, 그래프·도구·모델 설정은 그대로였습니다. 결과는 아래 표와 같았습니다.</p>
<table><thead><tr><th>질문</th><th>실행 흔적</th><th>모델 요청 수</th><th>도구 메시지 수</th><th>도구 호출 요청의 인자</th><th>호출 ID 짝</th></tr></thead><tbody><tr><td>대출</td><td><code>['model', 'model']</code></td><td>2</td><td>1</td><td><code>{'topic': '대출'}</code></td><td>True</td></tr><tr><td>인사</td><td><code>['model']</code></td><td>1</td><td>0</td><td>요청 없음</td><td>True</td></tr><tr><td>운영·연체(바꾼 값)</td><td><code>['model', 'model', 'model']</code></td><td>3</td><td>2</td><td><code>{'topic': '운영'}</code> → <code>{'topic': '연체'}</code></td><td>True</td></tr></tbody></table>
{{mermaid:""" + FIG3 + "|" + FIG3_ALT + "|" + FIG3_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG3_READ) + """</p>
<p>세 흐름은 모두 같은 그래프였습니다. 도구 쪽으로 몇 번 갈지는 모델의 응답이 정했고, 도구 조건 함수는 그 응답에 요청이 있는지만 보았습니다.</p><p>세 질문 모두 모델 요청 수가 도구 메시지 수보다 하나 많았습니다. 여럿 담기를 꺼서, 요청이 있는 응답마다 도구 메시지가 하나였습니다. 그리고 마지막 응답은 늘 요청이 없는 응답이었습니다.</p><p>새 커널로 두 번 실행했을 때 표의 값은 두 번 모두 같았습니다. 노트북 밖에서 세 질문을 다섯 번씩 보냈을 때도 같았습니다. 답 글의 문장은 실행마다 달랐고, 이 표에 넣지 않았습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>노트북을 실행하기 전에 노트북 밖에서 세 질문을 다섯 번씩 보냈습니다. 실행 흔적, 도구 이름과 인자, 도구 메시지 수가 다섯 번 모두 같았습니다. 같은 요청도 실행한 때에 따라 모델이 도구를 부를지가 달라질 수 있습니다.</li><li>질문 셋은 흐름을 보여 주려고 이 절에서 정한 예입니다. 운영·연체 질문은 규정 두 가지가 필요하도록 값 바꿔 보기로 정했습니다.</li><li>도구를 부를지와 그 인자에는 <code>assert</code>를 걸지 않았습니다. 모델이 정하는 값이기 때문입니다. 셀의 <code>assert</code>는 도구 실행 노드가 옮겨 적는 호출 ID 짝에만 걸었습니다.</li><li>도구 조건 함수의 동작은 손으로 만든 응답 두 개로 모델 없이 확인했습니다. 설치한 langgraph-prebuilt 1.1.0 소스도 도구 호출 요청의 개수가 0보다 큰지만 봅니다.</li><li>여럿 담기를 끈 채 도구를 알려 주었습니다. 한 응답에 담긴 요청 여럿을 도구 실행 노드가 실행하는 장면은 이 절에서 보지 않았습니다. 설치판 소스에서는 요청 여럿을 스레드로 한꺼번에 실행하고, 도구 메시지는 요청 차례대로 둡니다. 요청 여럿이 한 응답에 오면, 모델 요청 수와 도구 메시지 수의 셈은 달라질 수 있습니다.</li><li>도구 실행 노드는 이 절의 실행 흔적 칸을 쓰지 않습니다. 도구 실행은 메시지 칸의 도구 메시지로 읽었습니다.</li><li>그래프가 되풀이하는 횟수의 한도는 따로 정하지 않고 실행했습니다. 그 한도는 03절에서 다룹니다.</li><li>걸린 시간과 토큰은 재지 않았습니다. 모델 요청 수는 실행 흔적 칸의 길이로 셌습니다.</li><li>도구는 딕셔너리를 읽기만 합니다. 무언가를 바꾸는 쓰기 도구라면, Ch 19 06절처럼 사람 확인 값으로 알려 줄 도구를 먼저 고릅니다.</li><li>이 절이 도구 파일 <code>graph_tools.py</code>에서 가져오는 두 함수는 Ch 19 <code>order_tools.py</code>의 본문을 글자 그대로 옮긴 것입니다.</li><li>예상 비용은 2026-09-17 요금표로 어림하면 노트북 한 번에 0.01달러 아래이고, 청구 금액이 아닙니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>도구 조건 함수는 마지막 응답에 도구 호출 요청이 있으면 도구 실행 노드로, 없으면 <code>END</code>로 보냈습니다.</li><li>도구 실행 노드가 도구 메시지를 더하면, 되돌아가는 엣지로 모델 노드에 다시 갔습니다.</li><li>대출·인사·운영과 연체 질문의 모델 요청은 2·1·3번, 도구 메시지는 1·0·2개였습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_02 + """\">02절</a>에서는 도구 실행 노드가 실행한 도구가 오류를 낼 때를 봅니다. <a href=\"""" + L_CH19_06 + """\">Ch 19 06절</a>에서는 도구마다 오류 담기 설정(<code>handle_tool_error</code>)을 켜서 도구 오류를 도구 메시지에 담았습니다. 02절은 같은 일을 도구 실행 노드 쪽에서 다룹니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 도구 조건 함수는 무엇을 보고 이름표를 고르나요?</p><p class="quiz-a">메시지 칸의 마지막 응답에 도구 호출 요청이 있는지만 봅니다. 있으면 <code>"tools"</code>, 없으면 <code>END</code>를 내놓습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">2. 대출 질문의 실행 흔적 칸에는 <code>model</code>만 두 번 있습니다. 도구가 실행된 것은 어디서 확인하나요?</p><p class="quiz-a">메시지 칸의 도구 메시지로 확인합니다. 도구 실행 노드는 실행 흔적 칸을 쓰지 않고, 결과 상태 <code>success</code>인 도구 메시지를 메시지 칸에 더했습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">3. 되돌아가는 엣지는 무엇을 하나요?</p><p class="quiz-a">도구 실행 노드가 끝난 뒤 모델 노드로 다시 가게 합니다. 그래서 모델이 도구 메시지를 읽고 답하거나 다음 요청을 보낼 수 있습니다. 운영·연체 질문에서는 이 엣지를 두 번 지났습니다. 틀렸다면 노트북 6절과 9절을 다시 읽습니다.</p><p class="quiz-q">4. Ch 19 05절 함수 <code>ask_until_answer</code>의 <code>run_tool_calls</code>와 <code>break</code>는 이 그래프에서 무엇이 맡나요?</p><p class="quiz-a">함수 <code>run_tool_calls</code>는 도구 실행 노드가 맡고, <code>break</code>는 도구 조건 함수가 <code>END</code>를 내놓는 것이 맡습니다. 틀렸다면 본문 4 「핵심 개념」의 표를 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langgraph/graph-api">LangGraph Graph API</a></div>확인 2026-09-24 · 조건부 엣지에 조건 함수의 출력을 다음 노드 이름에 잇는 딕셔너리를 줄 수 있다고 적습니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langgraph/workflows-agents">LangGraph Workflows and agents</a></div>확인 2026-09-24 · 에이전트 예에서 도구 노드에서 모델 노드로 가는 엣지를 더합니다. 모델이 도구를 부르지 않으면 <code>END</code>로 갑니다.</li><li><div><a href="https://reference.langchain.com/python/langgraph.prebuilt/tool_node/ToolNode">ToolNode API 참조</a></div>확인 2026-09-24 · 인자 이름과 기본값을 적은 참조 페이지입니다. 동작은 설치판 소스로 확인했습니다.</li><li><div><a href="https://reference.langchain.com/python/langgraph.prebuilt/tool_node/tools_condition">tools_condition API 참조</a></div>확인 2026-09-24 · 인자 이름과 기본값만 보입니다.</li><li>langgraph-prebuilt 1.1.0 소스 <code>langgraph/prebuilt/tool_node.py</code> 1657~1659행입니다. 함수 <code>tools_condition</code>은 요청이 하나 이상이면 <code>"tools"</code>, 아니면 <code>"__end__"</code>를 내놓습니다.</li><li>같은 소스 — 속성 <code>tools_by_name</code>(789행), 요청 여럿을 스레드로 한꺼번에 실행하는 자리(823행).</li><li>Ch 13 02·03·04절 — 흔적 칸 규칙, 이름표 표, 메시지 리듀서.</li><li>Ch 17 03절 — 루프·바퀴·정지 조건.</li><li>Ch 19 05·06절 — 도구 실행과 호출 ID, 결과 상태와 함수 <code>show_messages</code>.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    if os.environ.get("AUTHOR01_NB_ONLY") != "1":
        print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "01", SLUG, "experiment", cells())
        print("wrote", path)
