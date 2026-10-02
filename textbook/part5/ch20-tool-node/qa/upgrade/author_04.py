"""Ch 20 04절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 author_04.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_04.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
  AUTHOR04_NB_ONLY=1 python3 author_04.py → 노트북만 다시 쓴다
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**(chapter.json). 본문 마지막 절.

## 결정 1 — 같은 질문으로 두 그래프 (챕터 리드 결정)

(가) 규칙 갈래 그래프: 규칙 함수 keyword_topic(여러 줄 if, 딕셔너리 키 차례 대출 → 운영 → 연체, 먼저 맞은 하나, 없으면 빈 글)
+ 조건 함수 pick_by_rule(Ch 13 03 모양, 시작점 START 뒤 조건부 엣지 — 공식 문서 「conditional entry point」) + 이름표 표
{"request": "request", "answer": "answer"} + 요청 노드 make_rule_request(01절 5절 모양 손 요청, id rule_call_1)
+ 01절 도구 실행 노드 + 답 노드 call_answer(도구를 알려 주지 않은 model). 되돌아가는 엣지 없음, 모델 요청은 답 노드에서만.
(나) 모델 선택 그래프: 01절 그래프 그대로(call_model·path_map·tools_condition·tools → model). 도구 실행 노드 하나를 두 그래프가 함께 씀.
상태 형식은 01절 AgentState 그대로(MessagesState 없음).

## 결정 2 — 결론은 코드로 세는 값만, 걸린 시간은 재지 않음

결론 = 질문마다 실행 흔적·모델 요청 수(sum_usage의 requests)·도구 인자(called_topics)·입력 토큰·입력 몫 예상 비용.
출력 토큰·예상 비용 합·답 글은 결과 읽기 둘째 단락·「확인할 점」·b6 「이번 실행에서는」에만. 「결과 편차」(Ch 17 05 약속)는
노트북 밖 다섯 번과 새 커널 두 번에서 달라진 것을 센 값으로 b6·b7에. 걸린 시간은 재지 않는다(perf_counter 0).

## 결정 3 — 흔들림 먼저 확인 (qa/upgrade/04-probe.md)

노트북 밖에서 네 질문 × 두 그래프 × 다섯 번(60요청). 모델 쪽 흔적·도구 인자·요청 수·입력 토큰 40/40 같음 → 입력 그대로.
질문 글에 옛 판의 강제 문구(「반드시 … 도구로 확인한 뒤」)를 넣지 않는다. 모델 답에 assert 0, assert는 규칙 함수 값에만.

## 결정 4 — 비용은 도구 파일 (§2-7)

Ch 19 order_tools.py의 sum_usage(Ch 19 05)·estimate_cost(Ch 6 06)를 graph_tools.py에 본문 글자 그대로 더함(AST 소스 조각 대조).
손으로 만든 요청은 AIMessage이지만 usage_metadata가 None이라 sum_usage에 그대로 넘기면 TypeError → 노트북 함수 model_responses로
사용량이 있는 응답만 골라 넘긴다. 요금은 이름 있는 변수(Ch 19 06과 같은 값·pricing_date). 입력 몫은 output_rate 자리에 0.

## 모델 요청

노트북 한 번 **12번**(8절 3 · 9절 6 · 11절 3, 모델 선택 쪽은 모델이 도구를 부르는 수에 따름). 읽는 파일·쓰는 파일 0.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`sorted`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·튜플 풀기·세미콜론·
`isinstance`·별표 풀기·`try`·`MessagesState`·`'__end__'` 글자·`recursion_limit`·`perf_counter`·시스템 메시지·`tool_choice`.
"""
from __future__ import annotations

import ast
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nbkit import RUN_DATE, code, key_and_model_cells, md, setup, write_notebook  # noqa: E402
import author_01  # noqa: E402
import author_03  # noqa: E402
from author_01 import html_text  # noqa: E402

LAB = ROOT / "labs/part5/ch20-tool-node/notebooks"
SLUG = "04-if-분기와-모델-선택-비교"
SRC = ROOT / "textbook/part5/ch20-tool-node/_src" / (SLUG + ".html")
# 교재 출력을 만든 실행의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답)에서 읽은 값
RUNSEC = os.environ.get("AUTHOR04_RUNSEC", "15초 안에")

# 01절과 글자까지 같은 셀(아래 assert)
INSTALL = author_01.INSTALL
POLICY_DATA = author_01.POLICY_DATA
BIND = author_01.BIND
STATE = author_01.STATE
TOOL_NODE = author_01.TOOL_NODE
CALL_MODEL = author_01.CALL_MODEL
# 03절 도구 셀 그대로(01절과 AST가 같고 오류 줄 위 주석 한 줄만 다름 — 아래 assert)
DEF_TOOL = author_03.DEF_TOOL

IMPORTS = r'''# 01절과 같은 그래프 이름에, 도구 파일의 함수 셋을 가져옵니다
import operator
from typing import Annotated
from typing_extensions import TypedDict

from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, AnyMessage, HumanMessage
from langchain.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from graph_tools import estimate_cost, show_messages, sum_usage

print("도구 파일에서 새로 가져온 함수:", "estimate_cost", "sum_usage")'''

DEF_RULE = r'''# 질문에 규정 주제어가 글자 그대로 있는지 차례로 보고, 먼저 맞은 주제어 하나를 내놓습니다(없으면 빈 글)
def keyword_topic(question):
    if "대출" in question:
        return "대출"
    if "운영" in question:
        return "운영"
    if "연체" in question:
        return "연체"
    return ""'''

RULE_TRY = r'''# 이 절의 질문 셋을 정하고, 모델 없이 규칙 함수에 하나씩 넣어 봅니다
loan_question = "자료실에서 일반 도서를 며칠 대출할 수 있나요?"
greet_question = "안녕하세요. 한 문장으로 인사해 주세요."
two_question = "자료실 운영 시간과 연체 규정을 함께 알려 주세요."
rule_picks = [keyword_topic(loan_question), keyword_topic(greet_question), keyword_topic(two_question)]
print("규칙 함수가 내놓은 값(대출·인사·운영·연체 질문 차례):", rule_picks)
# 모델 없이 코드가 정하는 값이라 매번 같아야 합니다
assert rule_picks == ["대출", "", "운영"], "규칙 함수는 적어 둔 차례대로 주제어를 골라야 합니다"'''

DEF_PICK = r'''# 질문을 규칙 함수에 넣어, 요청 노드와 답 노드 가운데 갈 곳의 이름표를 고릅니다(모델을 부르지 않음)
def pick_by_rule(state):
    question = state["messages"][0].content
    if keyword_topic(question) == "":
        return "answer"
    return "request"'''

PICK_TRY = r'''# 대출·인사 질문으로 첫 상태를 만들고, 조건 함수를 그래프 없이 직접 불러 봅니다(Ch 13 03절)
loan_state = {"messages": [HumanMessage(content=loan_question)], "trace": []}
greet_state = {"messages": [HumanMessage(content=greet_question)], "trace": []}
print("대출 질문의 이름표:", pick_by_rule(loan_state))
print("인사 질문의 이름표:", pick_by_rule(greet_state))
# 이름표 둘을 같은 이름의 노드에 잇습니다(끝점으로 가는 이름표는 없음)
rule_path_map = {"request": "request", "answer": "answer"}
print("규칙 갈래의 이름표 표:", rule_path_map)'''

DEF_REQUEST = r'''# 규칙이 고른 주제어로 도구 호출 요청을 손으로 만들어 메시지 칸에 더합니다(01절 5절 모양, 모델 요청 없음)
def make_rule_request(state):
    question = state["messages"][0].content
    topic = keyword_topic(question)
    rule_call = {"name": "lookup_policy", "args": {"topic": topic}, "id": "rule_call_1", "type": "tool_call"}
    request = AIMessage(content="", tool_calls=[rule_call])
    return {"messages": [request], "trace": ["request"]}'''

DEF_ANSWER = r'''# 도구를 알려 주지 않은 모델에 메시지 칸 전체를 보내고, 답 하나와 노드 이름만 냅니다
def call_answer(state):
    response = model.invoke(state["messages"])
    return {"messages": [response], "trace": ["answer"]}'''

RULE_BUILD = r'''# 규칙 갈래 그래프를 조립합니다(조건부 엣지를 시작점 START 뒤에 둡니다)
rule_builder = StateGraph(AgentState)
rule_builder.add_node("request", make_rule_request)
rule_builder.add_node("tools", tool_node)
rule_builder.add_node("answer", call_answer)
rule_builder.add_conditional_edges(START, pick_by_rule, rule_path_map)
rule_builder.add_edge("request", "tools")
rule_builder.add_edge("tools", "answer")
rule_builder.add_edge("answer", END)
rule_graph = rule_builder.compile()'''

RULE_STRUCTURE = r'''# 규칙 갈래 그래프가 스스로 그린 구조 문자열을 받아 옵니다(Ch 13 01절)
rule_structure = rule_graph.get_graph().draw_mermaid()
print("등록한 노드:", list(rule_builder.nodes))
print("그래프가 그린 구조:")
print(rule_structure)'''

MODEL_BUILD = r'''# 01절 5·6절과 같은 이름표 표와 엣지로 모델 선택 그래프를 조립합니다
path_map = {"tools": "tools", END: END}
model_builder = StateGraph(AgentState)
model_builder.add_node("model", call_model)
model_builder.add_node("tools", tool_node)
model_builder.add_edge(START, "model")
model_builder.add_conditional_edges("model", tools_condition, path_map)
model_builder.add_edge("tools", "model")
model_graph = model_builder.compile()
print("등록한 노드:", list(model_builder.nodes))'''

RUN_LOAN = r'''# 대출 질문을 두 그래프에 한 번씩 보냅니다(모델 요청은 규칙 갈래 1번, 모델 선택 2번 예상)
loan_rule = rule_graph.invoke(loan_state)
loan_model = model_graph.invoke(loan_state)
print("규칙 갈래 | 실행 흔적 칸:", loan_rule["trace"])
print("모델 선택 | 실행 흔적 칸:", loan_model["trace"])'''

LOAN_SHOW = r'''# 두 그래프의 메시지 칸을 차례로 출력합니다(Ch 19 06절 함수 show_messages)
print("규칙 갈래 그래프의 메시지 칸:")
show_messages(loan_rule["messages"])
print("모델 선택 그래프의 메시지 칸:")
show_messages(loan_model["messages"])'''

REQUEST_USAGE = r'''# 두 흐름의 둘째·넷째 메시지에 붙은 사용량을 봅니다(요청 없음, 손으로 만든 요청은 None)
print("규칙 갈래 | 둘째 메시지(요청)의 사용량:", loan_rule["messages"][1].usage_metadata)
print("규칙 갈래 | 넷째 메시지(답)의 입력 토큰:", loan_rule["messages"][3].usage_metadata["input_tokens"])
print("모델 선택 | 둘째 메시지(첫 응답)의 입력 토큰:", loan_model["messages"][1].usage_metadata["input_tokens"])
print("모델 선택 | 넷째 메시지(둘째 응답)의 입력 토큰:", loan_model["messages"][3].usage_metadata["input_tokens"])'''

DEF_RESPONSES = r'''# 메시지 목록에서 모델이 쓴 응답만 골라 새 목록으로 내놓습니다(사용량이 None인 손 요청은 뺍니다)
def model_responses(messages):
    responses = []
    for message in messages:
        if type(message).__name__ == "AIMessage":
            if message.usage_metadata is not None:
                responses.append(message)
    return responses'''

DEF_TOPICS = r'''# 메시지 목록의 도구 호출 요청에서 주제어 인자만 차례로 모아 내놓습니다(누가 만든 요청이든)
def called_topics(messages):
    asked_topics = []
    for message in messages:
        if type(message).__name__ == "AIMessage":
            for call in message.tool_calls:
                asked_topics.append(call["args"]["topic"])
    return asked_topics'''

DEF_ROW = r'''# 실행 결과 하나를 견주기 한 줄로 만듭니다(모델 요청 수와 입력 토큰은 모델 응답에서 셉니다)
def compare_row(graph_name, result):
    responses = model_responses(result["messages"])
    usage = sum_usage(responses)
    row = {"그래프": graph_name, "실행 흔적": result["trace"]}
    row["모델 요청 수"] = usage["requests"]
    row["도구 인자"] = called_topics(result["messages"])
    row["입력 토큰"] = usage["input_tokens"]
    return row'''

RUN_REST = r'''# 인사·운영·연체 질문을 두 그래프에 한 번씩 보냅니다(모델 요청은 규칙 갈래 2번, 모델 선택 4번 예상)
two_state = {"messages": [HumanMessage(content=two_question)], "trace": []}
greet_rule = rule_graph.invoke(greet_state)
greet_model = model_graph.invoke(greet_state)
two_rule = rule_graph.invoke(two_state)
two_model = model_graph.invoke(two_state)
print("인사 질문 | 규칙 갈래:", greet_rule["trace"], "| 모델 선택:", greet_model["trace"])
print("운영·연체 질문 | 규칙 갈래:", two_rule["trace"], "| 모델 선택:", two_model["trace"])'''

TABLE = r'''# 세 질문의 두 그래프 결과를 견주기 줄로 만들어, 라벨 줄 아래에 한 줄씩 출력합니다
main_runs = [["대출", loan_rule, loan_model], ["인사", greet_rule, greet_model], ["운영·연체", two_rule, two_model]]
print("질문 | 그래프 | 실행 흔적 | 모델 요청 수 | 도구 인자 | 입력 토큰")
for run in main_runs:
    rule_row = compare_row("규칙 갈래", run[1])
    model_row = compare_row("모델 선택", run[2])
    for row in [rule_row, model_row]:
        print(run[0], "|", row["그래프"], "|", row["실행 흔적"], "|", row["모델 요청 수"], "|", row["도구 인자"], "|", row["입력 토큰"])'''

USAGE = r'''# 세 질문에서 그래프마다 모델 응답을 모두 모아 요청 수와 토큰을 더합니다(Ch 19 05절 함수 sum_usage)
rule_responses = []
model_side_responses = []
for run in main_runs:
    rule_responses = rule_responses + model_responses(run[1]["messages"])
    model_side_responses = model_side_responses + model_responses(run[2]["messages"])
rule_usage = sum_usage(rule_responses)
model_usage = sum_usage(model_side_responses)
print("규칙 갈래 그래프:", rule_usage)
print("모델 선택 그래프:", model_usage)'''

COST = r'''# 2026-09-17 요금표(100만 토큰당 달러)로 두 그래프의 예상 비용을 셉니다(Ch 6 06절 함수 estimate_cost)
pricing_date = "2026-09-17"
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
rule_cost = estimate_cost(rule_usage, input_rate, cached_input_rate, output_rate)
model_cost = estimate_cost(model_usage, input_rate, cached_input_rate, output_rate)
print("요금 확인 날짜:", pricing_date)
print("규칙 갈래 예상 비용(달러):", round(rule_cost, 6))
print("모델 선택 예상 비용(달러):", round(model_cost, 6))'''

INPUT_COST = r'''# 출력 요금 자리에 0을 넣어, 예상 비용 가운데 입력 토큰 몫만 셉니다
no_output_rate = 0
rule_input_cost = estimate_cost(rule_usage, input_rate, cached_input_rate, no_output_rate)
model_input_cost = estimate_cost(model_usage, input_rate, cached_input_rate, no_output_rate)
print("규칙 갈래 입력 몫(달러):", round(rule_input_cost, 6))
print("모델 선택 입력 몫(달러):", round(model_input_cost, 6))'''

VALUE_CHANGE = r'''# 바꿀 값: 대출 질문의 「대출할」만 「빌릴」로 바꿔 두 그래프에 한 번씩 보냅니다(모델 요청 3번 예상)
borrow_question = "자료실에서 일반 도서를 며칠 빌릴 수 있나요?"
borrow_state = {"messages": [HumanMessage(content=borrow_question)], "trace": []}
borrow_rule = rule_graph.invoke(borrow_state)
borrow_model = model_graph.invoke(borrow_state)
print("규칙 함수가 내놓은 값이 빈 글인가:", keyword_topic(borrow_question) == "")
print("그래프 | 실행 흔적 | 모델 요청 수 | 도구 인자 | 입력 토큰")
for row in [compare_row("규칙 갈래", borrow_rule), compare_row("모델 선택", borrow_model)]:
    print(row["그래프"], "|", row["실행 흔적"], "|", row["모델 요청 수"], "|", row["도구 인자"], "|", row["입력 토큰"])'''

VALUE_ANSWERS = r'''# 빌림 질문에서 두 그래프의 마지막 응답(답 글)을 라벨 줄 아래에 출력합니다
print("규칙 갈래 답 글:")
print(borrow_rule["messages"][-1].content)
print("모델 선택 답 글:")
print(borrow_model["messages"][-1].content)'''


FIG1 = "04-1-도구를-고르는-두-그래프"
FIG1_ALT = "칸 둘이 나란히 있는 그림으로 왼쪽 (가) 규칙 갈래 그래프 칸에서는 회색 가상 시작점 START에서 점선 두 갈래가 나갑니다. 주제어 있음 갈래는 파란 상자 요청 노드 request 규칙이 요청을 만듦으로, 주제어 없음 갈래는 보라 상자 답 노드 answer 도구를 모르는 모델로 갑니다. 요청 노드에서 회색 상자 도구 실행 노드 tools, 답 노드, 회색 가상 끝점 END로 실선이 차례로 이어집니다. 오른쪽 (나) 모델 선택 그래프 01절 칸에서는 시작점에서 보라 상자 모델 노드 model 도구를 아는 모델로 가고, 요청 있음 점선은 회색 도구 실행 노드로, 요청 없음 점선은 가상 끝점으로 갑니다. 도구 실행 노드에서 되돌아가는 엣지 실선이 모델 노드로 올라가는 그림"
FIG1_CAP = "왼쪽은 시작점의 조건 함수가 질문 낱말로 갈래를 고르고, 오른쪽은 모델 노드의 응답이 도구 쪽으로 갈지 정합니다."
FIG1_READ = """왼쪽 칸이 규칙 갈래 그래프, 오른쪽 칸이 01절과 같은 모델 선택 그래프입니다.
왼쪽 시작점의 점선 두 갈래는 조건 함수 `pick_by_rule`이, 오른쪽 모델 노드의 점선 두 갈래는 도구 조건 함수가 고릅니다.
두 조건 함수는 노드가 아니라서 상자로 그리지 않았습니다.
파란 상자는 우리 코드가 요청을 만드는 노드, 보라 상자는 모델에 요청을 보내는 노드, 회색은 LangGraph가 준 것입니다.
왼쪽에는 되돌아가는 엣지가 없어, 도구 쪽은 많아야 한 번 다녀옵니다."""

FIG2 = "04-2-대출-질문의-두-흐름"
FIG2_ALT = "위에서 아래로 읽는 그림으로 맨 위 초록 상자 같은 첫 상태 대출 질문 자료실에서 일반 도서를 며칠 대출할 수 있나요에서 칸 둘로 화살표가 갑니다. 왼쪽 (가) 규칙 갈래 칸은 파란 상자 요청 노드 손으로 만든 요청 lookup_policy 대출 사용량 None, 노란 상자 도구 메시지 success 대출 규정 글, 보라 상자 답 노드 모델 요청 한 번 입력 토큰 72, 노란 상자 흔적 request · answer 차례로 이어집니다. 오른쪽 (나) 모델 선택 칸은 보라 상자 모델 노드 첫 요청 입력 토큰 164 요청 lookup_policy 대출, 노란 상자 도구 메시지 success 대출 규정 글, 보라 상자 모델 노드 둘째 요청 입력 토큰 214 요청 0건, 노란 상자 흔적 model 두 번 차례로 이어지는 그림"
FIG2_CAP = "같은 대출 질문에서 규칙 갈래는 모델 요청 한 번, 모델 선택은 두 번으로 대출 규정을 찾았습니다."
FIG2_READ = """위에서 아래로 읽고, 왼쪽 칸이 규칙 갈래, 오른쪽 칸이 모델 선택입니다.
두 칸 모두 도구 메시지는 결과 상태 `success`의 대출 규정 글입니다.
왼쪽 요청은 우리 코드가 만들어 사용량이 `None`이고, 모델 요청은 답 노드의 한 번뿐입니다.
오른쪽은 요청을 만드는 데에도 모델 요청이 한 번 들었습니다.
노란 상자와 보라 상자의 값은 노트북 8절 출력입니다."""

FIG3 = "04-3-세-질문의-요청-수와-입력-토큰"
FIG3_ALT = "위쪽에 칸 셋이 나란히 있고 칸마다 노란 상자 둘이 위아래로 놓인 그림입니다. 대출 질문 칸은 규칙 갈래 요청 한 번 인자 대출 입력 토큰 72와 모델 선택 요청 두 번 인자 대출 입력 토큰 378입니다. 인사 질문 칸은 규칙 갈래 요청 한 번 도구 없음 입력 토큰 18과 모델 선택 요청 한 번 도구 없음 입력 토큰 160입니다. 운영·연체 질문 칸은 규칙 갈래 요청 한 번 인자 운영 입력 토큰 75와 모델 선택 요청 세 번 인자 운영 다음 연체 입력 토큰 638입니다. 맨 아래 노란 상자에 세 질문 합 규칙 갈래 요청 세 번 입력 토큰 165, 모델 선택 요청 여섯 번 입력 토큰 1176이 적힌 그림"
FIG3_CAP = "세 질문을 합치면 규칙 갈래는 모델 요청 세 번과 입력 토큰 165, 모델 선택은 여섯 번과 1176이었습니다."
FIG3_READ = """위쪽 칸 셋은 왼쪽부터 대출·인사·운영과 연체 질문입니다.
칸마다 위 상자가 규칙 갈래, 아래 상자가 모델 선택이고, 같은 질문의 두 결과라 화살표로 잇지 않았습니다.
맨 아래 상자는 세 질문을 더한 값입니다.
칸 안의 값은 노트북 9절 표, 맨 아래 값은 10절 출력입니다."""

FIG4 = "04-4-낱말-하나를-바꾼-질문"
FIG4_ALT = "칸 둘이 나란히 있는 그림으로 왼쪽 바꾸기 전 대출할 칸에는 위에서부터 초록 상자 자료실에서 일반 도서를 며칠 대출할 수 있나요, 노란 상자 규칙 갈래 주제어 대출 request 요청 한 번 입력 토큰 72, 노란 상자 모델 선택 인자 대출 요청 두 번 입력 토큰 378이 놓여 있습니다. 오른쪽 바꾼 값 빌릴 칸에는 위에서부터 초록 상자 자료실에서 일반 도서를 며칠 빌릴 수 있나요, 노란 상자 규칙 갈래 빈 글 answer 도구 없음 요청 한 번 입력 토큰 22, 노란 상자 모델 선택 인자 대출 요청 두 번 입력 토큰 378이 놓인 그림"
FIG4_CAP = "「대출할」을 「빌릴」로 바꾸자 규칙 갈래는 도구 쪽에 가지 않았고, 모델 선택은 그대로 대출 규정을 찾았습니다."
FIG4_READ = """왼쪽 칸이 바꾸기 전, 오른쪽 칸이 바꾼 값이고, 두 질문은 낱말 하나만 다릅니다.
칸마다 위에서부터 질문, 규칙 갈래 결과, 모델 선택 결과이고, 화살표로 잇지 않았습니다.
규칙 갈래 상자는 두 칸이 다르고, 모델 선택 상자는 두 칸이 같습니다.
오른쪽 값은 노트북 11절 출력이고, 왼쪽 값은 9절 표의 대출 질문 두 줄입니다."""

ILLU = "04-5-손잡이로-내린-상자와-쪽지로-내린-상자"
ILLU_ALT = "흰 바탕 그림으로 두 층 자료실 벽을 잘라 보인 모습입니다. 위층 가운데에는 긴 나무 창구가, 아래층 가운데에는 파란 책이 꽂힌 책장이 있고, 그 양옆에 회색 승강 통로 둘이 세로로 나 있습니다. 두 통로의 나무 상자는 모두 아래층에 내려가 있고, 상자마다 파란 책 한 권이 들어 있습니다. 왼쪽 통로 입구 위에는 빨강·초록·파랑 둥근 점 셋이 찍힌 작은 나무 판이, 통로 왼쪽 벽에는 아래로 내려간 놋쇠 손잡이가 있고, 왼쪽 상자에는 종이가 없습니다. 오른쪽 통로에는 손잡이와 판이 없고, 상자 앞 오른쪽에 흰 쪽지 한 장이 반쯤 밖으로 나와 있는 그림"
ILLU_CAP = "왼쪽 상자는 색 점 판과 손잡이로, 오른쪽 상자는 쪽지로 내려가 둘 다 책을 받았습니다."
ILLU_READ = "위층 가운데에는 긴 나무 창구, 아래층 가운데에는 파란 책 책장이 있습니다. 그 양옆 승강 통로 둘의 상자는 모두 아래층에 내려가 파란 책을 한 권씩 받았습니다. 왼쪽 통로에는 입구 위에 색 점 셋이 찍힌 판과, 벽에 아래로 내려간 손잡이가 있고 상자에 종이가 없습니다. 오른쪽 상자에는 흰 쪽지 한 장이 반쯤 밖으로 나와 있고, 손잡이와 판은 없습니다. 색 점 판과 손잡이는 규칙 함수와 조건 함수, 쪽지는 모델이 쓴 도구 호출 요청입니다."

TITLE = """# if 분기와 모델 선택 비교

**이 노트북에서 할 일**

1. 질문 낱말을 보고 우리 규칙이 도구를 고르는 그래프를 만들어, 01절 그래프와 나란히 둡니다.
2. 같은 질문 셋을 두 그래프에 보내, 모델 요청 수·실행 흔적·도구 인자·입력 토큰을 견줍니다.
3. 규칙에 없는 낱말로 같은 뜻을 묻는 질문으로 바꿔, 두 그래프가 어떻게 갈리는지 봅니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 교재 출력에서 모델 요청은 모두 12번입니다.
8절에서 3번, 9절에서 6번, 11절에서 3번을 보냈습니다.
모델이 도구를 몇 번 부르느냐에 따라 요청 수가 달라질 수 있습니다.
요금표로 어림한 예상 비용은 모두 합쳐 0.01달러 아래이고, 청구 금액이 아닙니다.

도구는 노트북 안 규정 딕셔너리를 읽기만 하고, 읽는 파일과 새로 쓰는 파일은 없습니다.
앞에서 배운 함수 셋은 도구 파일 `graph_tools.py`에서 가져옵니다.
교재 출력을 만든 실행에서는 노트북 전체가 """ + RUNSEC + """ 끝났습니다.
이 절은 두 그래프의 걸린 시간을 재어 견주지 않습니다.

**기준 버전** — 첫 셀에서 패키지 다섯을 설치합니다.
판은 langgraph 1.2.11, langchain 1.4.0, langchain-core 1.6.2입니다.
langchain-openai 1.6.0과 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3~7절을 읽습니다.
두 그래프가 함께 쓰는 부품을 만들고, 규칙 갈래 그래프와 모델 선택 그래프를 조립하는 자리입니다.
8~11절은 질문을 보내 두 그래프를 견주는 자리이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part5/ch20-tool-node`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이 절은 도구를 고르는 두 방법을 같은 질문으로 견줍니다.
하나는 우리 코드의 `if`가 질문 낱말을 보고 고르는 방법이고, 다른 하나는 01절처럼 모델이 고르는 방법입니다.
제목에 적은 두 방법이 이 둘이고, 코드가 고르는 쪽을 이 절에서는 규칙 갈래라고 부릅니다.

첫 셀은 패키지 다섯 개를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langgraph: 1.2.11`·`langchain: 1.4.0`·`langchain-core: 1.6.2`가 보입니다.
출력 줄 `langchain-openai: 1.6.0`과 `python-dotenv: 1.2.3`도 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
그래프와 메시지 이름은 01절과 같고, 새로 가져오는 라이브러리 이름은 없습니다.
도구 파일에서는 01절에서 쓴 `show_messages`와, 이 절에서 더한 함수 둘을 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 새로 가져온 함수: estimate_cost sum_usage`가 보입니다.

앞에서 배운 함수는 `graph_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.

이 절에서 도구 파일에 함수 둘을 더했습니다.
함수 `sum_usage`는 Ch 19 05절, 함수 `estimate_cost`는 Ch 6 06절에서 배웠습니다.
두 함수 모두 Ch 19 도구 파일 `order_tools.py`의 본문을 글자 그대로 옮겼습니다.

## 2. 키와 모델 준비

모델은 01절과 같은 `gpt-5.4-mini`이고, 과정의 같은 설정으로 부릅니다.
이 절은 이 모델을 두 가지로 씁니다.
규칙 갈래 그래프에서는 도구를 알려 주지 않은 채 답만 받습니다.
모델 선택 그래프에서는 01절처럼 도구를 알려 준 모델이 도구를 고릅니다."""),
    ] + key_and_model_cells(
        "openai:gpt-5.4-mini",
        "temperature 값을 0으로 두어도, 모델이 도구 호출 요청을 보낼지가 매번 같다고 보장하지는 않습니다.",
    ) + [
        md("""## 3. 규정 자료와 도구

이 절도 교육센터 자료실 규정 셋을 소재로 씁니다.
다음 셀은 01절과 글자까지 같은 셀로, 주제어를 키로 한 규정 딕셔너리를 만듭니다."""),
        code(POLICY_DATA),
        md("""**결과 읽기** — 출력 줄 `규정 주제어: ['대출', '운영', '연체']`로 키 셋을 확인합니다.
이 세 주제어는 뒤에서 우리 규칙이 질문 속에서 찾을 낱말이기도 합니다.

다음 셀은 01절 도구와 코드가 같은 도구를 만듭니다.
오류 줄 위 주석 한 줄만 03절 판처럼 「02절에서 본 ValueError」로 적었습니다."""),
        code(DEF_TOOL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
도구 설명(독스트링)은 도구를 알려 준 요청에만 실립니다.

다음 셀은 01절과 글자까지 같은 셀로, 도구 목록을 모델에게 알려 준 `bound_model`을 만듭니다.
이 모델은 모델 선택 그래프에서만 씁니다."""),
        code(BIND),
        md("""**결과 읽기** — 출력 줄 `실어 보낼 명세 수: 1`과 `여럿 담기: False`는 01절과 같습니다.
규칙 갈래 그래프의 답 노드는 이 모델이 아니라 2절에서 만든 `model`을 씁니다.
그래서 규칙 갈래 쪽 요청에는 도구 명세가 실리지 않습니다.

## 4. 두 그래프가 함께 쓰는 부품

두 그래프는 상태 형식과 도구 실행 노드를 함께 씁니다.
상태 형식은 01절과 같은 `AgentState`입니다.
메시지 칸에는 메시지 리듀서, 실행 흔적 칸에는 이어 붙이기 규칙을 적습니다."""),
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
01절 셀과 글자까지 같고, 칸 구성이 같아 새 이름을 붙이지 않았습니다.

다음 셀은 01절 5절과 글자까지 같은 셀로 도구 실행 노드를 만듭니다.
이 노드 하나를 두 그래프에 함께 등록합니다."""),
        code(TOOL_NODE),
        md("""**결과 읽기** — 출력 줄 `만든 것의 종류: ToolNode`와 `안에 든 도구 찾기 표의 키: ['lookup_policy']`입니다.
두 그래프 모두 도구 실행은 이 노드가 맡습니다.
그래서 도구를 실행하는 쪽은 같고, 도구 호출 요청을 누가 만드느냐만 다릅니다.

## 5. 우리 규칙이 고르는 갈래

규칙 갈래 그래프에서는 우리 코드가 도구를 고릅니다.
규칙은 이렇게 정합니다. 질문에 규정 주제어가 글자 그대로 있으면, 그 주제어로 규정을 찾습니다.
주제어가 여럿이면 딕셔너리 키 차례대로 먼저 맞은 하나만 찾고, 하나도 없으면 찾지 않습니다.

다음 셀은 이 규칙을 여러 줄 `if`로 적은 함수입니다.
글 `A in B`는 글 A가 글 B 안에 들어 있으면 `True`입니다.
맞은 `if`에서 바로 주제어를 내놓으므로, 그 뒤의 `if`는 보지 않습니다."""),
        code(DEF_RULE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `keyword_topic`은 주제어 하나나 빈 글을 내놓습니다.
빈 글은 03절에서처럼 「찾을 주제어가 없음」을 뜻합니다.

다음 셀은 이 절에서 쓸 질문 셋을 정하고, 모델 없이 규칙 함수에 넣어 봅니다.
대출 질문은 01절 대출 질문의 「빌릴」을 규정 주제어가 든 「대출할」로 바꾼 글입니다.
인사 질문과 운영·연체 질문은 01절 글 그대로입니다."""),
        code(RULE_TRY),
        md("""**결과 읽기** — 출력 줄 끝의 목록 `['대출', '', '운영']`이 세 질문에 대한 규칙 함수의 값입니다.
대출 질문은 `대출`이고, 인사 질문은 빈 글입니다.
운영·연체 질문에는 주제어가 둘 있지만, 먼저 맞은 `운영` 하나만 나왔습니다.
모델 없이 코드가 정하는 값이라, 셀 끝 `assert`로 확인했습니다.

다음은 조건부 엣지에 넣을 조건 함수입니다.
Ch 13 03절 조건 함수처럼 상태를 받아 이름표를 내놓습니다.
첫 메시지인 질문에 규칙을 대어, 주제어가 없으면 `"answer"`, 있으면 `"request"`를 내놓습니다.
Ch 18 02절 라우팅에서는 모델이 쓴 문의 종류를 보고 코드가 갈래를 골랐습니다.
이 조건 함수는 모델에게 묻지 않고, 질문에 든 낱말만 봅니다."""),
        code(DEF_PICK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 함수도 노드로 등록하지 않고 조건부 엣지에 넣습니다.
01절 도구 조건 함수가 모델의 응답을 보았다면, 이 함수는 질문을 봅니다.

다음 셀은 대출 질문과 인사 질문으로 첫 상태를 만들어, 조건 함수를 그래프 없이 불러 봅니다.
두 이름표를 실제로 갈 노드에 잇는 이름표 표도 함께 만듭니다."""),
        code(PICK_TRY),
        md("""**결과 읽기** — 출력 줄 `대출 질문의 이름표: request`와 `인사 질문의 이름표: answer`입니다.
라벨 `규칙 갈래의 이름표 표:` 뒤 딕셔너리는 두 이름표를 같은 이름의 노드에 잇습니다.
이 표에는 끝점으로 가는 이름표가 없습니다.
어느 갈래로 가든, 끝으로 가는 일은 답 노드 뒤의 엣지가 맡습니다.

## 6. 규칙 갈래 그래프 조립

요청 노드는 규칙이 고른 주제어로 도구 호출 요청을 손으로 만듭니다.
01절 5절에서 손으로 만든 응답과 같은 모양이고, 칸 넷(`name`·`args`·`id`·`type`)을 적습니다.
모델을 부르지 않으므로 이 노드에서는 모델 요청이 나가지 않습니다.
만든 요청은 도구 실행 노드가 받아 실행합니다."""),
        code(DEF_REQUEST),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
요청의 호출 ID는 글 `rule_call_1`로 정해 두었습니다.
도구 실행 노드가 이 값을 도구 메시지에 옮겨 적습니다.

다음 셀은 답 노드입니다.
01절 모델 노드와 모양이 같지만, 도구를 알려 주지 않은 `model`을 부릅니다.
고르는 일은 규칙이 이미 했으므로, 모델은 받은 메시지를 읽고 답만 씁니다."""),
        code(DEF_ANSWER),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 노드를 지날 때마다 모델 요청이 한 번 나가고, 실행 흔적 칸에 `answer`가 붙습니다.
규칙 갈래 그래프에서 모델 요청이 나가는 곳은 이 노드뿐입니다.

다음 셀은 노드 셋을 등록하고 엣지를 적어 컴파일합니다.
이번에는 조건부 엣지를 시작점 `START` 뒤에 둡니다.
그래프가 시작하자마자 조건 함수가 질문을 보고 첫 노드를 고르는 모양입니다."""),
        code(RULE_BUILD),
        md("""**결과 읽기** — 이 셀은 조립만 하고 출력이 없습니다.
요청 노드 다음은 도구 실행 노드, 그다음은 답 노드로 가는 고정 엣지입니다.
규칙 갈래 그래프에는 되돌아가는 엣지가 없어서, 도구 쪽은 많아야 한 번 다녀옵니다.

다음 셀은 이 그래프가 스스로 그린 구조 문자열을 받아 옵니다."""),
        code(RULE_STRUCTURE),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['request', 'tools', 'answer']`입니다.
라벨 줄 `그래프가 그린 구조:` 아래에서 화살표 줄 다섯을 봅니다.
줄 `__start__ -.-> answer`와 `__start__ -.-> request`는 시작점 뒤 조건부 엣지의 두 갈래라 점선입니다.
나머지 세 줄은 실선이고, 뒤 노드에서 앞 노드로 되돌아가는 줄은 없습니다.

## 7. 모델 선택 그래프

모델 선택 그래프는 01절 그래프를 그대로 다시 조립합니다.
다음 셀은 01절 모델 노드와 글자까지 같은 셀입니다.
모델 노드는 도구를 알려 준 `bound_model`에 메시지 칸 전체를 보냅니다."""),
        code(CALL_MODEL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 노드를 지날 때마다 모델 요청이 한 번 나가고, 실행 흔적 칸에 `model`이 붙습니다.
도구를 부를지와 어떤 인자를 넣을지는 이 요청의 응답이 정합니다.

다음 셀은 01절 5·6절과 같은 이름표 표와 엣지로 그래프를 조립합니다.
도구 실행 노드는 4절에서 만든 `tool_node`를 다시 씁니다."""),
        code(MODEL_BUILD),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['model', 'tools']`입니다.
도구 조건 함수, 이름표 표, 되돌아가는 엣지 `tools → model`은 01절과 같습니다.
두 그래프 모두 같은 도구 실행 노드를 등록했습니다.

## 8. 대출 질문을 두 그래프에

첫 질문은 규정 주제어 「대출」이 든 대출 질문입니다.
5절에서 만든 첫 상태 `loan_state`를 두 그래프에 한 번씩 넣습니다.
실행 전에 예상해 봅니다.
규칙 갈래는 요청 노드·도구 실행 노드·답 노드를 지나고, 모델 요청은 1번일 것입니다.
모델 선택은 01절처럼 모델 노드를 두 번 지나, 모델 요청이 2번일 것입니다."""),
        code(RUN_LOAN),
        md("""**결과 읽기** — 출력 줄 `규칙 갈래 | 실행 흔적 칸: ['request', 'answer']`입니다.
출력 줄 `모델 선택 | 실행 흔적 칸: ['model', 'model']`입니다.
도구 실행 노드는 01절에서 본 것처럼 흔적 칸을 쓰지 않아, 두 흔적 모두 도구 실행이 보이지 않습니다.
모델 요청은 규칙 갈래가 `answer` 한 번, 모델 선택이 `model` 두 번입니다.

다음 셀은 Ch 19 06절 함수 `show_messages`로 두 메시지 칸을 차례로 출력합니다."""),
        code(LOAN_SHOW),
        md("""**결과 읽기** — 라벨 줄 두 개 아래 네 줄씩이, 두 그래프의 메시지 칸입니다.
두 칸 모두 둘째 줄이 `AIMessage | 도구 호출 요청: ['lookup_policy']`입니다.
셋째 줄 도구 메시지도 두 칸 모두 결과 상태 `success`에 대출 규정 글입니다.
메시지 모양만으로는 둘째 줄의 요청을 누가 만들었는지 가를 수 없습니다.

다음 셀은 메시지마다 붙은 사용량을 봅니다.
사용량(`usage_metadata`)은 Ch 6에서 본, 모델 응답에 붙는 토큰 수입니다."""),
        code(REQUEST_USAGE),
        md("""**결과 읽기** — 출력 줄 `규칙 갈래 | 둘째 메시지(요청)의 사용량: None`입니다.
규칙 갈래의 요청은 우리 코드가 만들어, 모델 요청이 아니므로 사용량이 없습니다.
규칙 갈래 답 요청의 입력 토큰은 출력 줄 끝의 `72`입니다.
모델 선택의 첫 요청은 `164`, 둘째 요청은 `214`입니다.

규칙 갈래의 답 요청과 모델 선택의 둘째 요청은 모두 질문·요청·도구 메시지 셋을 보냅니다.
셈으로는 두 요청의 입력 토큰 차이가 142이고, 모델 선택 쪽에만 도구를 알려 주었습니다.
이 차이는 9절 인사 질문에서 한 번 더 봅니다.

## 9. 세 질문 견주기

인사 질문과 운영·연체 질문도 두 그래프에 보내, 세 질문을 한 표로 견줍니다.
먼저 표를 만들 함수 셋을 정의합니다.
도구 파일 함수 `sum_usage`는 `AIMessage`를 모두 모델 응답으로 보고 사용량을 더합니다.
규칙 갈래의 요청도 `AIMessage`라, 그대로 넘기면 사용량 `None`에서 오류가 납니다.
그래서 첫 함수는 사용량이 있는 응답만 골라 새 목록에 담습니다."""),
        code(DEF_RESPONSES),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `model_responses`는 `AIMessage`이면서 사용량이 `None`이 아닌 메시지만 담습니다.
받은 목록은 고치지 않고, 새 목록을 내놓습니다.

다음 셀은 메시지 목록에서 도구 호출 요청의 주제어 인자만 차례로 모으는 함수입니다.
요청을 모델이 만들었든 우리 규칙이 만들었든 함께 모읍니다."""),
        code(DEF_TOPICS),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `called_topics`는 응답마다 도구 호출 요청의 칸 `args`에서 `topic` 값을 꺼냅니다.
요청이 하나도 없으면 빈 목록을 내놓습니다.

다음 셀은 실행 결과 하나를 견주기 한 줄로 만드는 함수입니다.
모델 요청 수와 입력 토큰은 모델 응답만 골라 `sum_usage`로 셉니다."""),
        code(DEF_ROW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `compare_row`는 칸 다섯을 담은 딕셔너리를 내놓습니다.
칸은 그래프·실행 흔적·모델 요청 수·도구 인자·입력 토큰입니다.

다음 셀은 인사 질문과 운영·연체 질문을 두 그래프에 한 번씩 보냅니다.
실행 전에 예상해 봅니다.
규칙 갈래는 두 질문 모두 모델 요청 1번이고, 인사 질문에서는 도구 쪽에 가지 않을 것입니다.
모델 선택은 01절처럼 인사 질문 1번, 운영·연체 질문 3번일 것입니다."""),
        code(RUN_REST),
        md("""**결과 읽기** — 출력 줄 `인사 질문 | 규칙 갈래: ['answer'] | 모델 선택: ['model']`입니다.
인사 질문은 두 그래프 모두 도구 쪽에 가지 않았습니다.
출력 줄 `운영·연체 질문 | 규칙 갈래: ['request', 'answer'] | 모델 선택: ['model', 'model', 'model']`입니다.
운영·연체 질문에서 모델 선택 그래프는 모델 노드를 세 번 지났습니다.

다음 셀은 세 질문의 결과를 견주기 줄로 만들어 한 줄씩 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 여섯 줄이 질문마다 규칙 갈래와 모델 선택 한 줄씩입니다.
대출 질문은 `대출 | 규칙 갈래 | ['request', 'answer'] | 1 | ['대출'] | 72`와 `대출 | 모델 선택 | ['model', 'model'] | 2 | ['대출'] | 378`입니다.
인사 질문은 `인사 | 규칙 갈래 | ['answer'] | 1 | [] | 18`과 `인사 | 모델 선택 | ['model'] | 1 | [] | 160`입니다.
운영·연체 질문은 `1 | ['운영'] | 75`와 `3 | ['운영', '연체'] | 638`입니다.
규칙 갈래는 세 질문 모두 모델 요청이 1번이었고, 운영·연체 질문에서 운영 규정 하나만 찾았습니다.

인사 질문은 두 그래프가 같은 메시지 하나를 보냈고, 입력 토큰 차이는 142입니다.
두 요청은 도구를 알려 주었는지만 다르므로, 이 차이는 도구 명세가 실린 몫입니다.
8절 대출 질문에서 본 차이 142와 같습니다.
모델 선택 그래프는 모델 요청마다 이만큼을 더 보냅니다.

## 10. 요청 수와 예상 비용

Ch 17 05절 자율성 진단표는 두 흐름의 호출 수·비용·결과 편차를 견주라고 적어 두었습니다.
이 절에서 호출 수는 모델 요청 수로, 비용은 예상 비용으로 셉니다.
결과 편차는 같은 질문을 여러 번 보내야 셀 수 있어, 노트북 밖에서 세어 본문 6에 적었습니다.
다음 셀은 세 질문의 모델 응답을 그래프마다 모아 `sum_usage`로 더합니다."""),
        code(USAGE),
        md("""**결과 읽기** — 출력 줄은 `규칙 갈래 그래프: {'requests': 3, 'input_tokens': 165`로 시작합니다.
다음 출력 줄은 `모델 선택 그래프: {'requests': 6, 'input_tokens': 1176`로 시작합니다.
모델 요청은 3번과 6번, 입력 토큰은 165와 1176입니다.
모델 선택 그래프는 도구를 고르는 요청이 더 있고, 요청마다 도구 명세가 실렸습니다.

칸 `output_tokens`는 답 글 길이에 따라 실행마다 달라질 수 있습니다.
이번 실행에서는 출력 토큰이 규칙 갈래 135, 모델 선택 151이었습니다.
새 커널로 한 번 더 실행했을 때는 규칙 갈래 쪽 값이 달랐습니다.

다음 셀은 Ch 6 06절 요금표로 두 그래프의 예상 비용을 셉니다.
요금은 Ch 19 06절과 같은 2026-09-17 값이고, 이름 있는 변수로 둡니다.
예상 비용은 요금표로 어림한 값이고, 청구 금액이 아닙니다."""),
        code(COST),
        md("""**결과 읽기** — 출력 줄 `요금 확인 날짜: 2026-09-17`은 요금표를 확인한 날짜입니다.
라벨 `규칙 갈래 예상 비용(달러):`과 `모델 선택 예상 비용(달러):` 뒤가 두 그래프의 예상 비용입니다.
예상 비용에는 출력 토큰 몫도 들어 있어, 실행마다 조금씩 달라질 수 있습니다.

이번 실행에서는 규칙 갈래 0.000731달러, 모델 선택 0.001561달러였습니다.
새 커널로 한 번 더 실행했을 때는 규칙 갈래 쪽 값이 달라, 예상 비용 합은 결론에 쓰지 않습니다.

출력 토큰은 답 글 길이에 따라 달라지지만, 입력 토큰은 같은 요청이면 같았습니다.
그래서 다음 셀은 출력 요금 자리에 0을 넣어, 예상 비용 가운데 입력 토큰 몫만 셉니다.
함수는 그대로 두고, 0을 담은 변수를 인자 `output_rate` 자리에 넘깁니다."""),
        code(INPUT_COST),
        md("""**결과 읽기** — 출력 줄 `규칙 갈래 입력 몫(달러): 0.000124`와 `모델 선택 입력 몫(달러): 0.000882`입니다.
세 질문에서 모델 선택 그래프의 입력 몫이 규칙 갈래보다 컸습니다.
모델 요청이 두 배였고, 요청마다 도구 명세가 실렸습니다.
운영·연체 질문에서 규칙 갈래가 규정 하나만 찾은 차이도 이 값에 들어 있습니다.

## 11. 값 바꿔 보기 · 규칙에 없는 낱말로 묻기

바꿀 값은 질문 하나입니다.
대출 질문의 「대출할」만 「빌릴」로 바꿔, 뜻은 같고 규정 주제어는 없는 질문을 만듭니다.
이 글은 01절 대출 질문 그대로입니다.
실행 전에 예상해 봅니다.
규칙 갈래는 주제어를 찾지 못해 도구 쪽에 가지 않고, 모델 선택은 대출 규정을 찾을 것입니다."""),
        code(VALUE_CHANGE),
        md("""**결과 읽기** — 출력 줄 `규칙 함수가 내놓은 값이 빈 글인가: True`입니다.
라벨 줄 아래 첫 줄은 `규칙 갈래 | ['answer'] | 1 | [] | 22`입니다.
규칙 갈래는 조건 함수가 이름표 `answer`를 골라, 도구 쪽에 가지 않았습니다.
둘째 줄은 `모델 선택 | ['model', 'model'] | 2 | ['대출'] | 378`입니다.
모델은 「빌릴」로 물어도 주제어 `대출`을 골라 규정을 찾았습니다.

모델 쪽 결과는 모델이 정한 값이라 실행마다 달라질 수 있습니다.
노트북 밖에서 이 질문을 다섯 번 보냈을 때는 다섯 번 모두 이 줄과 같았습니다.

다음 셀은 두 그래프의 답 글을 봅니다.
규칙 갈래의 답 노드는 규정 글을 받지 못한 채 답을 썼습니다."""),
        code(VALUE_ANSWERS),
        md("""**결과 읽기** — 라벨 줄 `규칙 갈래 답 글:` 아래는 규정 글 없이 모델이 쓴 답입니다.
라벨 줄 `모델 선택 답 글:` 아래는 도구 메시지의 규정 글을 읽고 쓴 답입니다.
답 글은 실행마다 달라질 수 있어, 결론에 쓰지 않습니다.

이번 실행에서는 규칙 갈래 답 글이 대출 기간을 「보통 14일(2주)」로 적고, 자료실마다 다를 수 있다고 덧붙였습니다.
규정 글을 읽고 쓴 답이 아니어서, 기간이 규정과 같아도 규정에서 온 값이 아닙니다.
모델 선택 답 글은 도구 메시지의 「1인 5권까지 14일 동안」을 옮겨 적었습니다.

## 정리

1. 규칙 갈래 그래프는 질문 낱말을 보고 코드가 갈래를 골라, 세 질문 모두 모델 요청이 1번이었습니다.
2. 모델 선택 그래프는 모델이 도구를 골라 모델 요청이 2·1·3번이었고, 요청마다 도구 명세가 실렸습니다.
3. 규칙에 없는 낱말로 묻자 규칙 갈래는 도구 쪽에 가지 않았고, 모델 선택은 대출 규정을 찾았습니다.

05절 실습에서는 이 챕터에서 만든 그래프와 함수를 모아, 자료실 문의 하나를 처리합니다."""),
    ]


L_CH6_06 = "../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html"
L_CH13_03 = "../../part4/ch13-langgraph-basics/03-조건부-엣지.html"
L_CH17_01 = "../ch17-agent-overview/01-워크플로우와-에이전트-경계.html"
L_CH17_04 = "../ch17-agent-overview/04-자율성의-대가.html"
L_CH17_05 = "../ch17-agent-overview/05-제품-트레이스와-자율성-진단.html"
L_CH18_02 = "../ch18-workflow-patterns/02-실패를-처리하는-라우팅.html"
L_CH19_05 = "../ch19-model-tools/05-bind_tools와-병렬-호출.html"
L_CH19_06 = "../ch19-model-tools/06-오류와-읽기-쓰기-분리.html"
L_01 = "01-ToolNode와-tools-condition.html"
L_03 = "03-recursion-limit과-명시적-종료.html"


def link(url: str, label: str) -> str:
    return '<a href="' + url + '">' + label + "</a>"


def rows_html(rows: list[list[str]], head: list[str]) -> str:
    out = "<table><thead><tr>"
    for cell in head:
        out = out + "<th>" + cell + "</th>"
    out = out + "</tr></thead><tbody>"
    for row in rows:
        out = out + "<tr>"
        for cell in row:
            out = out + "<td>" + cell + "</td>"
        out = out + "</tr>"
    return out + "</tbody></table>"


def c(text: str) -> str:
    return "<code>" + text + "</code>"


RESULT_TABLE = rows_html([
    ["대출", "규칙 갈래", c("['request', 'answer']"), "1", c("['대출']"), "72"],
    ["대출", "모델 선택", c("['model', 'model']"), "2", c("['대출']"), "378"],
    ["인사", "규칙 갈래", c("['answer']"), "1", c("[]"), "18"],
    ["인사", "모델 선택", c("['model']"), "1", c("[]"), "160"],
    ["운영·연체", "규칙 갈래", c("['request', 'answer']"), "1", c("['운영']"), "75"],
    ["운영·연체", "모델 선택", c("['model', 'model', 'model']"), "3", c("['운영', '연체']"), "638"],
    ["빌림(바꾼 값)", "규칙 갈래", c("['answer']"), "1", c("[]"), "22"],
    ["빌림(바꾼 값)", "모델 선택", c("['model', 'model']"), "2", c("['대출']"), "378"],
], ["질문", "그래프", "실행 흔적", "모델 요청 수", "도구 인자", "입력 토큰"])

SPREAD_TABLE = rows_html([
    ["대출", "0/5", "0/5", "1", "1"],
    ["인사", "0/5", "0/5", "3", "2"],
    ["운영·연체", "0/5", "0/5", "4", "2"],
    ["빌림(바꾼 값)", "0/5", "0/5", "5", "4"],
], ["질문", "흔적·요청 수·도구 인자가 달라진 회차(두 그래프)", "입력 토큰이 달라진 회차(두 그래프)", "답 글 종류 수(규칙 갈래)", "답 글 종류 수(모델 선택)"])

LOOK_B5 = ("노트북 8절 출력 <code>규칙 갈래 | 실행 흔적 칸: ['request', 'answer']</code>와 "
           "<code>모델 선택 | 실행 흔적 칸: ['model', 'model']</code>로 두 흐름을 봅니다. "
           "같은 절 출력 <code>규칙 갈래 | 둘째 메시지(요청)의 사용량: None</code>으로, 규칙 갈래의 요청이 모델 요청이 아님을 봅니다. "
           "노트북 9절 표에서 세 질문의 모델 요청 수와 입력 토큰을 견줍니다.")


def src_html() -> str:
    return ("""<!--meta: 강의 0.5h | 실습 1.25h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>질문 낱말을 보는 조건 함수로 도구 쪽 갈래를 고르는 그래프를 만들 수 있습니다.</li>
<li>같은 질문을 두 그래프에 보내, 모델 요청 수·실행 흔적·도구 인자·입력 토큰을 코드로 세어 견줄 수 있습니다.</li>
<li>매번 같은 값과 실행마다 달라지는 값을 가르고, 결과 편차를 달라진 수로 적을 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>""" + link(L_01, "01절") + """ 그래프에서는 모델이 도구를 골랐습니다. 모델은 질문을 읽고 도구 호출 요청을 보낼지, 인자에 어떤 주제어를 넣을지 정했습니다. 그런데 도구를 고르는 일은 우리 코드의 <code>if</code>로도 할 수 있습니다. """ + link(L_CH18_02, "Ch 18 02절") + """ 라우팅처럼 코드가 갈래를 고르는 방법입니다.</p><p>제목에 적은 두 방법이 이 둘이고, 코드가 고르는 쪽을 이 절에서는 규칙 갈래라고 부릅니다. 코드가 고르면 도구를 고르려고 모델에게 묻는 요청이 없습니다. 대신 규칙에 적지 않은 낱말로 물으면 놓칠 수 있습니다. 모델이 고르면 낱말을 바꿔 물어도 맞는 도구를 고를 수 있지만, 고를 때마다 모델 요청이 나갑니다.</p><p>""" + link(L_CH17_05, "Ch 17 05절") + """ 자율성 진단표의 칸 <code>next_measurement</code>는 이 챕터에서 두 흐름의 호출 수·비용·결과 편차를 견주라고 적었습니다. 이 절이 그 비교입니다. 같은 질문을 두 그래프에 보내고, 차이를 코드로 셉니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>""" + link(L_CH13_03, "Ch 13 03절") + """에서는 조건 함수가 상태를 보고 이름표를 내놓고, 이름표 표가 그 이름표를 노드에 이었습니다. 이 절의 규칙 갈래 그래프도 같은 모양이고, 조건 함수가 질문 낱말을 봅니다. Ch 18 02절 라우팅에서는 모델이 쓴 문의 종류를 보고 코드가 갈래를 골랐습니다. 이 절의 조건 함수는 모델에게 묻지 않고 질문에 든 낱말만 봅니다.</p><p>""" + link(L_CH17_01, "Ch 17 01절") + """은 다음 단계를 고른 쪽을 결정 주체라고 불렀습니다. """ + link(L_CH17_04, "04절") + """에서는 워크플로우와 모델이 고르는 루프를 같은 문의로 실행해, 모델 요청 수와 토큰 수를 셌습니다. 그 절은 결론을 요청 수와 입력 토큰처럼 매번 같은 값으로만 냈고, 이 절도 같은 기준을 씁니다. 05절 자율성 진단표는 이 비교를 다음에 잴 것으로 적어 두었습니다.</p><p>01절에서는 모델 노드·도구 실행 노드·도구 조건 함수·되돌아가는 엣지로 그래프를 만들었습니다. 01절 5절에서는 도구 호출 요청을 담은 응답을 손으로 만들었고, """ + link(L_03, "03절") + """에서는 빈 글을 「찾을 주제어가 없음」으로 썼습니다. 비용은 """ + link(L_CH6_06, "Ch 6 06절") + """ 함수 <code>estimate_cost</code>로, 사용량은 """ + link(L_CH19_05, "Ch 19 05절") + """ 함수 <code>sum_usage</code>로 셉니다. 두 함수는 이 절에서 도구 파일 <code>graph_tools.py</code>에 더했습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절의 두 층 자료실을 다시 떠올립니다. 이번에는 창구와 서고 사이에 승강 통로가 둘 있습니다. 두 통로의 상자는 모두 서고로 내려가 규정 책을 싣고 올라옵니다. 다른 것은 상자를 내려보낼지 누가 정하느냐입니다.</p><p>왼쪽 통로 입구 위에는 색 점 셋이 찍힌 작은 판이 있고, 통로 옆 벽에는 손잡이가 있습니다. 색 점 셋은 미리 정해 둔 낱말 대출·운영·연체입니다. 질문에 그 낱말이 보이면 손잡이를 내려 상자를 보내고, 보이지 않으면 보내지 않습니다. 사서에게 묻지 않고, 정해 둔 규칙이 고르는 방식입니다.</p><p>오른쪽 통로는 01절과 같습니다. 사서가 질문을 읽고 요청 쪽지를 적어 넣으면 상자가 내려갑니다. 왼쪽의 손잡이와 색 점 판은 규칙 갈래 그래프의 조건 함수와 규칙 함수입니다. 오른쪽 쪽지는 모델 선택 그래프의 도구 호출 요청입니다. 「빌릴」처럼 판에 없는 낱말로 물으면, 왼쪽 상자는 내려가지 않습니다.</p>
{{img:""" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + """}}
<p class="look"><b>그림 읽기</b> — """ + ILLU_READ + """</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>규칙 갈래 그래프</td><td>우리 코드의 조건 함수가 질문 낱말을 보고 도구 쪽으로 갈지 정하는 그래프입니다. 도구 호출 요청은 요청 노드가 손으로 만들고, 모델은 답만 씁니다. 왼쪽 통로의 손잡이와 같습니다.</td></tr><tr><td>모델 선택 그래프</td><td>도구를 알려 준 모델이 도구 호출 요청으로 도구를 고르는 그래프입니다. 01절 그래프와 같습니다. 오른쪽 통로의 쪽지와 같습니다.</td></tr><tr><td>결과 편차</td><td>같은 질문을 여러 번 보냈을 때 결과가 달라진 정도입니다. 이 절은 달라진 회차 수와 답 글 종류 수로 셉니다. 같은 쪽지를 다섯 번 보냈을 때 사서의 답이 몇 번 달랐는지 세는 것과 같습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 규칙 갈래 그래프는 <code>rule_graph</code>이고, 조건 함수 <code>pick_by_rule</code>을 시작점 뒤 조건부 엣지에 넣습니다. 모델 선택 그래프는 <code>model_graph</code>이고, 01절처럼 모델 노드 뒤에 도구 조건 함수를 둡니다. 결과 편차는 노트북 밖에서 같은 질문을 다섯 번씩 보내 셉니다.</p>
{{mermaid:""" + FIG1 + "|" + FIG1_ALT + "|" + FIG1_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG1_READ) + """</p>
<h3>다른 상황에 적용</h3><p>주제어가 몇 개로 정해져 있고 묻는 사람이 그 낱말을 그대로 쓰는 창구라면, 규칙 갈래로도 고를 수 있습니다. 예를 들어 자료실 안내 화면에 「대출」·「운영」·「연체」 버튼을 둔다고 해 봅니다. 누른 버튼 이름을 질문에 붙이면, 버튼 이름이 곧 주제어가 됩니다. 이 조합은 이번에 실행하지 않았습니다.</p>
<h3>비교와 경계</h3><p>이 절의 비교는 질문 넷과 도구 하나로 한 것입니다. 그래서 어느 방법이 낫다고 넓혀 말하지 않고, 이 질문들에서 센 값만 적습니다. 규칙 갈래는 규칙에 적은 낱말만 보고, 모델 선택은 모델이 고른 뒤에야 요청 수가 정해집니다. 규칙이 먼저 고르고 못 고르면 모델에게 묻는 섞은 설계는 이번에 실행하지 않았습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 01절과 같은 규정 딕셔너리·도구·상태 형식·도구 실행 노드를 만듭니다. 그다음 규칙 함수와 조건 함수를 그래프 없이 불러 보고, 규칙 갈래 그래프를 조립합니다. 모델 선택 그래프는 01절 그래프를 그대로 다시 조립합니다. 대출 질문을 두 그래프에 보낸 뒤, 인사 질문과 운영·연체 질문도 보내 한 표로 견줍니다. 마지막으로 요청 수와 예상 비용을 세고, 값 바꿔 보기로 「빌릴」 질문을 보냅니다.</p><p>모델은 <code>gpt-5.4-mini</code>이고, temperature 0과 추론 끔(<code>reasoning_effort="none"</code>)으로 부릅니다. 교재 출력에서 모델 요청은 모두 12번입니다. 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
{{mermaid:""" + FIG2 + "|" + FIG2_ALT + "|" + FIG2_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG2_READ) + """</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>실험에서 같게 둔 것은 질문·자료·도구·모델 설정이고, 바꾼 것은 도구를 고르는 쪽입니다. 그에 따라 규칙 갈래는 답 노드에 도구를 알려 주지 않았고, 되돌아가는 엣지도 없습니다. 이 두 차이도 아래 표의 입력 토큰 차이에 들어 있습니다.</p>
""" + RESULT_TABLE + """
{{mermaid:""" + FIG3 + "|" + FIG3_ALT + "|" + FIG3_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG3_READ) + """</p>
<p>규칙 갈래 그래프는 세 질문 모두 모델 요청이 1번이었습니다. 모델 선택 그래프는 도구를 부를 때마다 요청이 하나씩 늘어 2·1·3번이었습니다. 세 질문을 합치면 모델 요청은 3번과 6번, 입력 토큰은 165와 1176이었습니다. 입력 토큰 몫의 예상 비용은 0.000124달러와 0.000882달러였습니다.</p><p>인사 질문은 두 그래프가 같은 메시지 하나를 보냈고, 입력 토큰은 18과 160이었습니다. 두 요청은 도구를 알려 주었는지만 달라서, 차이 142는 도구 명세가 실린 몫입니다. 대출 질문에서도 규칙 갈래의 답 요청 72와 모델 선택의 둘째 요청 214가 같은 만큼 달랐습니다.</p><p>운영·연체 질문에서 규칙 갈래는 먼저 맞은 운영 규정 하나만 찾았습니다. 모델 선택은 운영과 연체를 차례로 찾았습니다. 규칙 쪽 값은 코드에 적은 차례대로라 매번 같고, 모델 쪽 값은 모델이 정한 값입니다.</p><p>값 바꿔 보기에서는 「대출할」을 「빌릴」로만 바꿨습니다. 규칙 갈래는 주제어를 찾지 못해 도구 쪽에 가지 않았고, 모델 요청 1번으로 끝났습니다. 모델 선택은 주제어 대출을 골라 규정을 찾았고, 모델 요청은 2번이었습니다. 뜻이 같은 질문이라도 규칙 갈래의 갈래는 낱말 하나로 바뀌었습니다.</p>
{{mermaid:""" + FIG4 + "|" + FIG4_ALT + "|" + FIG4_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG4_READ) + """</p>
<h3>결과 편차</h3><p>Ch 17 05절이 적은 결과 편차는 노트북 밖에서 네 질문을 두 그래프에 다섯 번씩 보내 셌습니다. 아래 표는 달라진 것을 센 값이고, 달라진 답 글 자체는 결론에 쓰지 않았습니다. 두 그래프의 결과 차이, 곧 같은 질문에서 달라진 도구 인자와 모델 요청 수는 위 실험 결과 표에 함께 있습니다.</p>
""" + SPREAD_TABLE + """
<p>실행 흔적·모델 요청 수·도구 인자·입력 토큰은 40번 모두 같았습니다. 답 글은 문장부호·굵은 글씨·목록 모양이 달라져, 질문과 그래프에 따라 종류 수가 1에서 5까지였습니다. 빌림 질문의 규칙 갈래 답 글은 이번 다섯 번에서 모두 달랐습니다. 새 커널 두 번 실행에서는 코드 셀 32개 가운데 29개의 출력이 글자까지 같았습니다. 달라진 셋은 규칙 갈래의 출력 토큰 합과 그 예상 비용, 규칙 갈래 빌림 질문의 답 글이었습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>노트북을 실행하기 전에 노트북 밖에서 네 질문을 두 그래프에 다섯 번씩, 모델 요청 60번을 보냈습니다. 모델 선택 쪽 실행 흔적·도구 인자·모델 요청 수·입력 토큰이 다섯 번 모두 같았습니다. 같은 요청도 실행한 때에 따라 모델이 도구를 부를지가 달라질 수 있습니다.</li><li>질문 넷은 실행 전에 이 절에서 정한 예이고, 결과를 보고 바꾸지 않았습니다. 인사 질문·운영과 연체 질문·빌림 질문은 01절 글 그대로입니다. 대출 질문은 01절 대출 질문의 「빌릴」만 「대출할」로 바꾼 글입니다.</li><li>규칙 함수의 낱말 셋과 차례(대출 → 운영 → 연체)도 실행 전에 정한 예입니다. 차례를 바꿔 적으면 운영·연체 질문에서 찾는 규정이 달라지지만, 이번에 실행하지 않았습니다.</li><li>질문 글에 「반드시 도구로 확인한 뒤 답하라」 같은 지시는 붙이지 않았습니다. 그런 지시를 붙이면 모델이 도구를 부르지 않는 선택을 볼 수 없기 때문입니다.</li><li>모델이 정하는 값, 곧 도구를 부를지와 인자, 답 글에는 <code>assert</code>를 걸지 않았습니다. 셀의 <code>assert</code>는 규칙 함수가 내놓는 값처럼 우리 코드가 정하는 값에만 걸었습니다.</li><li>규칙 갈래의 답 노드에는 도구를 알려 주지 않았습니다. 그래서 운영·연체 질문에서 규칙 갈래의 모델은 연체 규정을 더 찾을 수 없었습니다.</li><li>함수 <code>sum_usage</code>에 손으로 만든 요청을 그대로 넘기면 사용량 <code>None</code>에서 <code>TypeError</code>가 납니다. 노트북 밖에서 확인했고, 노트북에서는 모델 응답만 골라 넘겼습니다.</li><li>규칙 갈래의 빌림 질문 답 글은 규정 글 없이 쓴 답입니다. 노트북 밖 다섯 번 가운데 한 번은 대출 기간을 규정 글과 다르게 적었습니다. 기간이 규정과 같게 적힌 답도 규정을 읽고 쓴 것은 아닙니다.</li><li>걸린 시간은 재지 않았습니다. 그래서 두 그래프 가운데 어느 쪽이 빠른지는 이 절에서 말하지 않습니다. 준비물의 실행 시간은 노트북 셀 실행 기록에서 읽은 값입니다.</li><li>예상 비용은 2026-09-17 요금표로 어림한 값이고 청구 금액이 아닙니다. 출력 토큰 몫이 들어 있어 실행마다 조금씩 달라지므로, 결론에는 입력 토큰 몫만 썼습니다.</li><li>도구 파일 <code>graph_tools.py</code>에 더한 두 함수는 Ch 19 <code>order_tools.py</code>의 본문을 글자 그대로 옮긴 것입니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>규칙 갈래 그래프는 질문 낱말을 보고 코드가 갈래를 골라, 세 질문 모두 모델 요청이 1번이었습니다.</li><li>모델 선택 그래프는 모델이 도구를 골라 모델 요청이 2·1·3번이었고, 요청마다 도구 명세가 실렸습니다.</li><li>규칙에 없는 낱말로 묻자 규칙 갈래는 도구 쪽에 가지 않았고, 모델 선택은 대출 규정을 찾았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href="05-ToolNode-실습.html">05절</a> 실습에서는 이 챕터에서 만든 그래프와 함수를 모아, 자료실 문의 하나를 처리합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 규칙 갈래 그래프에서 모델 요청이 나가는 노드는 어디인가요?</p><p class="quiz-a">답 노드 <code>answer</code> 하나뿐입니다. 요청 노드는 도구 호출 요청을 손으로 만들어, 모델 요청이 나가지 않습니다. 그래서 대출 질문의 모델 요청은 1번이었습니다. 틀렸다면 노트북 6절과 8절을 다시 읽습니다.</p><p class="quiz-q">2. 인사 질문의 입력 토큰이 두 그래프에서 18과 160으로 달랐던 까닭은 무엇인가요?</p><p class="quiz-a">두 요청 모두 같은 질문 메시지 하나를 보냈고, 모델 선택 그래프만 도구를 알려 주었습니다. 그 요청에 도구 명세가 실린 만큼 입력 토큰이 늘었습니다. 틀렸다면 노트북 9절 표를 다시 읽습니다.</p><p class="quiz-q">3. 「빌릴」로 물었을 때 두 그래프는 어떻게 달랐나요?</p><p class="quiz-a">규칙 갈래는 규칙 함수가 빈 글을 내놓아 답 노드로 바로 갔고, 도구를 부르지 않았습니다. 모델 선택은 주제어 대출을 골라 규정을 찾았습니다. 틀렸다면 노트북 11절을 다시 읽습니다.</p><p class="quiz-q">4. 이 절에서 결론에 쓴 값과 쓰지 않은 값은 무엇인가요?</p><p class="quiz-a">실행 흔적·모델 요청 수·도구 인자·입력 토큰은 새 커널 두 번과 노트북 밖 다섯 번에서 모두 같아 결론에 썼습니다. 답 글·출력 토큰·출력 몫이 든 예상 비용은 실행마다 달라, 결과 편차로 세기만 했습니다. 틀렸다면 본문 6 「실험 결과 해석」을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langgraph/graph-api">LangGraph Graph API</a></div>확인 2026-09-24 · 조건부 엣지를 시작점 <code>START</code>에 두는 모양을 적습니다. 조건 함수의 출력을 다음 노드 이름에 잇는 딕셔너리도 줄 수 있습니다.</li><li>langgraph-prebuilt 1.1.0 소스 <code>langgraph/prebuilt/tool_node.py</code> 1657~1659행입니다. 도구 조건 함수는 마지막 응답의 도구 호출 요청이 하나 이상이면 <code>"tools"</code>를 내놓습니다.</li><li>Ch 13 03절 — 조건 함수와 이름표 표.</li><li>Ch 17 01·04·05절 — 결정 주체, 자율성의 대가, 자율성 진단표.</li><li>Ch 18 02절 — 코드가 갈래를 고르는 라우팅.</li><li>""" + link(L_CH19_06, "Ch 19 06절") + """ — 함수 <code>show_messages</code>와 결과 상태, 요금 변수.</li><li>Ch 6 06절 — 요금표와 예상 비용.</li></ul>
""")


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


def same_ast(left: str, right: str) -> bool:
    return ast.dump(ast.parse(left)) == ast.dump(ast.parse(right))


if __name__ == "__main__":
    # 01절 셀과 글자까지 같은 셀
    for name in ["INSTALL", "POLICY_DATA", "BIND", "STATE", "TOOL_NODE", "CALL_MODEL"]:
        assert globals()[name] == getattr(author_01, name), name
    # 도구 셀은 03절 셀과 글자까지 같고, 01절과 AST가 같다
    assert DEF_TOOL == author_03.DEF_TOOL and same_ast(DEF_TOOL, author_01.DEF_TOOL)
    if os.environ.get("AUTHOR04_NB_ONLY") != "1":
        print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "04", SLUG, "experiment", cells())
        print("wrote", path)
