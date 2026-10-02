"""Ch 20 05절(챕터 끝 실습 절) 생성기 (QUALITY-UPGRADE.md §7-2·§2·§2-7·§3·§4·§6).

사용:
  python3 author_05.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_05.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
  AUTHOR05_NB_ONLY=1 python3 author_05.py → 노트북만 다시 쓴다
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
새로 만든 절이라 qa/upgrade/before/ 에 원본이 없다. **experiment 형식**(chapter.json), lesson_part 없음.

## 결정 1 — 붙인 앞 절 기능 (인계 「§04 → 실습(05)」 6항)

01절 그래프(모델 노드·도구 실행 노드·도구 조건 함수·되돌아가는 엣지, 셀 글자 그대로) + 02절 오류 처리 함수
(handle_policy_error, 02절 7절 셀 글자 그대로 — 받을 오류 표시 error: ValueError는 02절 판 그대로라 허용)를 넘긴 도구 실행 노드
+ 03절 설정 딕셔너리(실행 한도). 실행 1 = 한도 10(03절 limit_config와 같은 값), 실행 2 = 한도 하나만 실행 1에서 센
노드 실행 수와 같게. 04절 두 그래프 견주기·02절 Before·03절 Before는 되풀이하지 않는다(b3).

## 결정 2 — 문의는 흔들림 확인 규칙으로 정함 (qa/upgrade/05-probe.md)

§0에 적은 후보 A(02절 주차 질문)·B(주제어 주차)·C(01절 대출 질문) 차례. A는 모델이 주제어 운영을 적거나 도구를 부르지 않았고,
B는 도구를 부르지 않아 조건을 못 채움 → C. 그래서 오류 처리 함수는 붙여 두기만 한 설계(b3·b7에 밝힘). 오류 처리 함수가 내놓는 글은
02절 7절처럼 그래프 없이 한 번 불러 보인다(모델 요청 없음).

## 결정 3 — 결론은 코드로 세는 값만

실행 흔적·도구 인자·결과 상태·모델 요청 수·도구 메시지 수·호출 ID 짝(01절 run_row)·노드 실행 수(모델 요청 수 + 도구 메시지 수)·
받은 오류 이름·셈한 통과 한도. 실행 2의 모델 요청 수는 노트북에서 셀 수 없어 「노트북 밖 다섯 번에서 센 값」으로만.
답 글·출력 토큰·예상 비용은 결과 읽기 둘째 단락·「확인할 점」·b7에만. 걸린 시간은 재지 않는다. 모델 답에 assert 0.

## 결정 4 — 도구 파일 (§2-7)

01절 노트북 함수 call_id_lists(7절)·run_row(10절)를 graph_tools.py에 본문 글자 그대로 옮김(`# Ch 20 01절에서 배웠습니다`).
run_row가 call_id_lists를 부르므로 둘을 함께. 노드(call_model)·도구(@tool)·오류 처리 함수는 노트북에(챕터 리드 결정 1).

## 모델 요청

노트북 한 번 **4번**(실행 1 두 번 · 실행 2 두 번 — 실행 2는 한도에 닿아 결과가 없어 노트북 밖에서 셈). 읽는 파일·쓰는 파일 0.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`sorted`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·튜플 풀기·세미콜론·
`isinstance`·별표 풀기·try `else`·`MessagesState`·`'__end__'` 글자·`Literal`·`perf_counter`·시스템 메시지·`tool_choice`·
`ToolMessage(…)` 직접 만들기·체크포인터·`create_agent`·미들웨어·`interrupt`.
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
import author_02  # noqa: E402
import author_03  # noqa: E402
from author_01 import html_text  # noqa: E402

LAB = ROOT / "labs/part5/ch20-tool-node/notebooks"
SLUG = "05-ToolNode-실습"
SRC = ROOT / "textbook/part5/ch20-tool-node/_src" / (SLUG + ".html")

# 01절과 글자까지 같은 셀(아래 assert)
INSTALL = author_01.INSTALL
POLICY_DATA = author_01.POLICY_DATA
BIND = author_01.BIND
STATE = author_01.STATE
CALL_MODEL = author_01.CALL_MODEL
PATH_MAP = author_01.PATH_MAP
STRUCTURE = author_01.STRUCTURE
# 03·04절 도구 셀 그대로(01절과 AST가 같고 오류 줄 위 주석 한 줄만 다름)
DEF_TOOL = author_03.DEF_TOOL
# 02절 7절 오류 처리 함수 셀 그대로
DEF_HANDLER = author_02.DEF_HANDLER

IMPORTS = r'''# 01절 그래프 이름에 03절 오류 이름 하나를 더하고, 도구 파일의 함수 넷을 가져옵니다
import operator
from typing import Annotated
from typing_extensions import TypedDict

from langchain.chat_models import init_chat_model
from langchain.messages import AnyMessage, HumanMessage
from langchain.tools import tool
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from graph_tools import estimate_cost, run_row, show_messages, sum_usage

print("이 절에서 도구 파일에 더한 함수:", "call_id_lists", "run_row")'''

INQUIRY = r'''# 오늘 처리할 자료실 문의 하나로 첫 상태를 만듭니다(01절 7절 대출 질문과 같은 글)
inquiry = "자료실에서 일반 도서를 며칠 빌릴 수 있나요?"
inquiry_state = {"messages": [HumanMessage(content=inquiry)], "trace": []}
print("문의:", inquiry)
print("출처: 01절 7절 대출 질문 그대로, 이 절에서 실행 전에 정함")
state_keys = list(inquiry_state.keys())
print("첫 상태의 칸:", state_keys)'''

# 02절 7절 셀과 코드가 같고 첫 줄 주석만 다름(아래 assert)
TRY_HANDLER = r'''# 02절 7절처럼 ValueError 하나를 직접 만들어, 도구 실행 노드 없이 오류 처리 함수에 넣어 봅니다
sample_error = ValueError("지원하지 않는 주제: 주차")
guide_text = handle_policy_error(sample_error)
print("내놓은 글:", guide_text)'''

POLICY_NODE = r'''# 02절 7절처럼 오류 처리 함수를 넘겨 도구 실행 노드를 만듭니다(아직 그래프에 넣지 않음)
policy_node = ToolNode(tools, handle_tool_errors=handle_policy_error)
print("만든 것의 종류:", type(policy_node).__name__)
# 속성 tools_by_name은 01절에서 본 도구 찾기 표입니다
table_keys = list(policy_node.tools_by_name.keys())
print("안에 든 도구 찾기 표의 키:", table_keys)'''

BUILD = r'''# 01절 6절과 같은 노드와 엣지로 그래프를 조립합니다(도구 실행 노드 자리만 policy_node)
builder = StateGraph(AgentState)
builder.add_node("model", call_model)
builder.add_node("tools", policy_node)
builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition, path_map)
builder.add_edge("tools", "model")
graph = builder.compile()
print("등록한 노드:", list(builder.nodes))'''

RUN_ONE = r'''# 실행 1: 03절과 같은 설정 딕셔너리(한도 10)로 문의를 처리합니다(모델 요청 2번 예상)
limit_config = {"recursion_limit": 10}
print("설정 딕셔너리:", limit_config)
one_result = graph.invoke(inquiry_state, limit_config)
print("실행 흔적 칸:", one_result["trace"])
print("메시지 칸의 메시지 수:", len(one_result["messages"]))'''

ONE_SHOW = r'''# 메시지 칸을 차례로 출력합니다(Ch 19 06절 함수 show_messages)
print("메시지 칸:")
show_messages(one_result["messages"])'''

ONE_CHECK = r'''# 첫 응답의 도구 호출 요청 인자와, 셋째 메시지(도구 메시지)의 결과 상태를 봅니다
first_response = one_result["messages"][1]
for call in first_response.tool_calls:
    print("도구 이름:", call["name"], "| 인자:", call["args"])
tool_message = one_result["messages"][2]
print("셋째 메시지의 결과 상태:", tool_message.status)'''

ONE_ROW = r'''# 실행 결과를 기록 한 줄로 만들고, 노드 실행 수를 셉니다(01절 10절 함수 run_row)
one_row = run_row("대출 문의", one_result)
print("기록 한 줄:", one_row)
# 도구 실행 노드는 흔적 칸을 쓰지 않으므로, 도구 메시지 수를 더해 노드 실행 수를 셉니다
one_steps = one_row["모델 요청 수"] + one_row["도구 메시지 수"]
print("노드 실행 수:", one_steps)'''

ONE_ANSWER = r'''# 마지막 응답의 도구 호출 요청 수와 답 글을 봅니다
last_message = one_result["messages"][-1]
print("마지막 응답의 도구 호출 요청 수:", len(last_message.tool_calls))
print("답 글:")
print(last_message.content)'''

TIGHT = r'''# 바꿀 값: 실행 한도를 실행 1의 노드 실행 수와 같게 줄인 설정 딕셔너리를 만듭니다
tight_config = {"recursion_limit": one_steps}
print("실행 1의 설정 딕셔너리:", limit_config)
print("실행 2의 설정 딕셔너리:", tight_config)'''

RUN_TWO = r'''# 실행 2: 같은 첫 상태를 줄인 한도로 실행합니다(이 셀만 올라온 오류를 받아 출력합니다)
try:
    two_result = graph.invoke(inquiry_state, tight_config)
    print("끝까지 실행 | 실행 흔적 칸:", two_result["trace"])
except GraphRecursionError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:")
    print(error)'''

COMPARE = r'''# 03절 6절 규칙(노드 실행 수보다 하나 큰 한도부터 통과)으로 통과 한도를 셈하고, 두 한도와 견줍니다
one_more = 1
pass_limit = one_steps + one_more
print("셈으로 통과하는 가장 작은 한도:", pass_limit)
print("실행 1 한도가 그 값보다 작은가:", limit_config["recursion_limit"] < pass_limit)
print("실행 2 한도가 그 값보다 작은가:", tight_config["recursion_limit"] < pass_limit)'''

COST = r'''# 실행 1의 사용량을 더하고, 2026-09-17 요금표로 예상 비용을 셉니다(Ch 19 05절 sum_usage·Ch 6 06절 estimate_cost)
one_usage = sum_usage(one_result["messages"])
print("실행 1 사용량:", one_usage)
pricing_date = "2026-09-17"
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
one_cost = estimate_cost(one_usage, input_rate, cached_input_rate, output_rate)
print("요금 확인 날짜:", pricing_date)
print("실행 1 예상 비용(달러):", round(one_cost, 6))'''


FIG1 = "05-1-오류-처리-함수와-한도를-붙인-그래프"
FIG1_ALT = "위에서 아래로 읽는 그림으로 맨 위에 초록 상자 둘이 나란히 있습니다. 왼쪽은 첫 상태 대출 문의 하나, 오른쪽은 설정 딕셔너리 03절 recursion_limit 10입니다. 두 상자에서 invoke 첫째 인자와 둘째 인자 화살표가 아래 01절 그래프 모양 칸으로 갑니다. 칸 안에서 회색 가상 시작점 START가 보라 상자 모델 노드 model로 가고, 모델 노드에서 점선 두 갈래가 나갑니다. 요청 있음 이름표 tools 갈래는 회색 상자 도구 실행 노드 tools ToolNode로, 요청 없음 명시적 종료 갈래는 회색 가상 끝점 END로 갑니다. 도구 실행 노드에서 되돌아가는 엣지 실선이 모델 노드로 오고, 도구 실행 노드와 선으로 이은, 양옆에 세로줄이 한 줄씩 더 있는 파란 상자 오류 처리 함수 02절 handle_policy_error 이번 흐름에서 쓰이지 않음이 있는 그림"
FIG1_CAP = "01절 그래프에 02절 오류 처리 함수와 03절 실행 한도를 붙였고, 오류 처리 함수는 이번 두 실행에서 쓰이지 않았습니다."
FIG1_READ = """위에서 아래로 읽습니다. 아래 칸에서 오류 처리 함수를 뺀 상자 넷과 화살표 넷은 노트북 5절 구조 문자열과 같습니다.
보라 상자는 모델에 요청을 보내는 모델 노드이고, 회색은 LangGraph가 준 것입니다.
오류 처리 함수는 노드가 아니라서 양옆에 세로줄이 더 있는 파란 상자로 그렸고, 이번 두 실행에서는 쓰이지 않았습니다.
맨 위 초록 상자 둘은 메서드 `invoke`에 넘기는 두 인자이고, 실행 2에서는 오른쪽 한도만 바꿉니다."""

FIG2 = "05-2-실행-1이-지난-단계-셋"
FIG2_ALT = "세로선 셋이 있는 차례 그림으로 왼쪽부터 노트북 코드 graph.invoke, 연보라 띠 안의 모델 노드 model gpt-5.4-mini, 도구 실행 노드 policy_node입니다. 노트북 코드가 모델 노드에 첫 상태 한도 10을 보내고, 노란 메모 단계 1 요청 1 lookup_policy 인자 대출이 붙습니다. 모델 노드에서 도구 실행 노드로 tools_condition tools 화살표가 가고, 노란 메모 단계 2 도구 메시지 success 오류 처리 함수 쓰이지 않음이 붙습니다. 도구 실행 노드에서 모델 노드로 되돌아가는 엣지가 오고, 노란 메모 단계 3 요청 2 도구 호출 요청 0건 뒤에 모델 노드에서 노트북 코드로 tools_condition END 점선이 갑니다. 마지막 노란 메모에 명시적 종료 한도 10에 닿지 않음, 흔적 model 두 번 노드 실행 수 3, 호출 ID 짝 True가 적힌 그림"
FIG2_CAP = "실행 1은 모델 노드, 도구 실행 노드, 모델 노드의 세 단계를 지나 한도 10에 닿기 전에 END로 끝났습니다."
FIG2_READ = "위에서 아래로 읽고, 세로선은 왼쪽부터 노트북 코드, 모델 노드, 도구 실행 노드입니다. 연보라 띠는 실제로 부른 모델 `gpt-5.4-mini`가 있는 자리입니다. 노란 메모의 단계 번호는 노드를 실행한 차례이고, 세 번째 단계 뒤 도구 조건 함수가 END를 내놓았습니다. 노란 메모는 모두 노트북 6절 출력입니다."

FIG3 = "05-3-한도-하나만-바꾼-두-실행"
FIG3_ALT = "맨 위 초록 상자 같은 첫 상태 대출 문의 같은 그래프 같은 모델 설정에서 아래 칸 둘로 화살표가 갑니다. 왼쪽 칸 실행 1 한도 10에는 노란 상자 흔적 model 두 번 노드 실행 수 3 도구 메시지 success 하나와, 노란 상자 마지막 응답 요청 0건 END로 끝나 결과를 받음이 위아래로 있습니다. 오른쪽 칸 실행 2 바꾼 값 한도 3에는 노란 상자 GraphRecursionError Recursion limit of 3, 노란 상자 invoke가 결과를 내놓지 않음 흔적 답 글 사용량 없음, 회색 상자 노트북 밖 다섯 번에서 센 값 모델 요청 두 번 뒤 멈춤이 위아래로 있습니다. 맨 아래 회색 상자에 셈 03절 규칙 노드 실행 수 3이면 한도 4부터 통과가 적힌 그림"
FIG3_CAP = "한도만 노드 실행 수와 같은 3으로 줄인 실행 2는 GraphRecursionError로 멈춰, 실행 흔적도 답 글도 받지 못했습니다."
FIG3_READ = "맨 위 초록 상자는 두 칸에 똑같이 넣은 첫 상태입니다. 왼쪽 칸이 실행 1, 오른쪽 칸이 한도만 바꾼 실행 2이고, 칸 안 상자들은 화살표로 잇지 않았습니다. 노란 상자는 노트북 6·7절 출력이고, 실행 2에서 받아 출력한 오류도 노랑입니다. 회색 상자 둘은 노트북 밖에서 센 값과 03절 규칙으로 한 셈입니다."

ILLU = "05-4-받침에-선-상자와-빈-카드-주머니"
ILLU_ALT = "흰 바탕 그림으로 두 층 자료실 벽을 잘라 보인 모습입니다. 가운데에 회색 승강 통로 하나가 아래층부터 위층까지 세로로 나 있습니다. 위층 왼쪽에는 긴 나무 창구가, 아래층 왼쪽에는 파란 책이 꽂힌 책장이 있습니다. 통로 안 위층 높이의 나무 받침 위에 나무 상자 하나가 얹혀 있고, 상자 위로 흰 쪽지 한 장과 파란 책 한 권이 반쯤 나와 있습니다. 위층 통로 오른쪽 벽에는 둥근 등 여섯이 세로로 달린 판이 있고, 위의 셋은 꺼진 회색, 아래 셋은 노랗게 켜져 있습니다. 아래층 통로 오른쪽 벽에는 빈 회색 카드 여러 장이 꽂힌 나무 주머니가 있는 그림"
ILLU_CAP = "상자는 계수기 등이 셋만 켜진 채 창구 층 받침에 섰고, 빈 카드 주머니는 쓰이지 않았습니다."
ILLU_READ = "가운데 승강 통로는 하나이고, 위층 높이의 나무 받침 위에 상자 하나가 얹혀 있습니다. 상자에는 흰 쪽지 한 장과 파란 책 한 권이 반쯤 나와 있습니다. 통로 오른쪽 위층 벽의 판에는 둥근 등 여섯이 있고, 아래 셋만 노랗게 켜져 있습니다. 아래층 오른쪽 벽의 주머니에는 빈 회색 카드가 여러 장 꽂혀 있습니다."

TITLE = """# ToolNode 실습: 자료실 문의 그래프에 오류 처리 함수와 실행 한도 붙이기

**이 노트북에서 할 일**

1. 01절 그래프에 02절 오류 처리 함수와 03절 실행 한도를 붙여, 자료실 문의 하나를 처리합니다.
2. 도구 메시지의 결과 상태로 오류 처리 함수가 쓰였는지 보고, 그 흐름의 노드 실행 수를 셉니다.
3. 실행 한도 하나만 노드 실행 수와 같게 줄여 다시 실행하고, 두 실행을 견줍니다.

**준비물** — 프로젝트 맨 위 폴더의 `.env`에 적어 둔 `OPENAI_API_KEY`를 씁니다.
모델은 `gpt-5.4-mini`이고, 교재 출력에서 실행 1의 모델 요청은 2번입니다.
실행 2는 한도에 닿아 결과를 받지 못해, 노트북 안에서는 그 요청 수를 셀 수 없습니다.
노트북 밖에서 같은 흐름을 다섯 번 보냈을 때 실행 2도 2번이어서, 모두 4번으로 어림합니다.

모델이 도구를 몇 번 부르느냐에 따라 요청 수는 달라질 수 있습니다.
요금표로 어림한 예상 비용은 0.01달러 아래이고, 청구 금액이 아닙니다.
도구는 노트북 안 규정 딕셔너리를 읽기만 하고, 읽는 파일과 새로 쓰는 파일은 없습니다.

앞에서 배운 함수 넷은 도구 파일 `graph_tools.py`에서 가져옵니다.
걸린 시간은 재지 않습니다. 교재 출력을 만든 실행에서는 노트북 전체가 10초 안에 끝났습니다.

**기준 버전** — 첫 셀에서 패키지 다섯을 설치합니다.
판은 langgraph 1.2.11, langchain 1.4.0, langchain-core 1.6.2입니다.
langchain-openai 1.6.0과 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**실습 범위** — 이 절은 챕터 끝 실습 절이고 30분 안에 끝나는 분량입니다.
강사와 함께 첫 셀부터 차례로 실행하고, 따로 내는 과제는 없습니다.
01~04절에서 쓴 이름과 문법만 씁니다.

실습 폴더 `labs/part5/ch20-tool-node`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이번 절은 이 챕터의 실습입니다.
01절 그래프에 02절 오류 처리 함수와 03절 실행 한도를 붙여, 자료실 문의 하나를 처리합니다.
첫 셀은 패키지 다섯 개를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langgraph: 1.2.11`·`langchain: 1.4.0`·`langchain-core: 1.6.2`가 보입니다.
출력 줄 `langchain-openai: 1.6.0`과 `python-dotenv: 1.2.3`도 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
그래프와 메시지 이름은 01절과 같고, 03절에서 본 오류 이름 `GraphRecursionError`를 더합니다.
도구 파일에서는 함수 넷을 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `이 절에서 도구 파일에 더한 함수: call_id_lists run_row`가 보입니다.

앞에서 배운 함수는 `graph_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.

이 절에서 도구 파일에 01절 함수 둘을 더했습니다.
함수 `run_row`는 실행 결과 하나를 기록 한 줄로 만들고, 안에서 함수 `call_id_lists`를 부릅니다.
두 함수 모두 01절 노트북의 본문을 글자 그대로 옮겼습니다.
함수 `show_messages`는 Ch 19 06절, `sum_usage`는 Ch 19 05절, `estimate_cost`는 Ch 6 06절에서 배웠습니다.

## 2. 키와 모델 준비

모델은 01절과 같은 `gpt-5.4-mini`이고, 과정의 같은 설정으로 부릅니다."""),
    ] + key_and_model_cells(
        "openai:gpt-5.4-mini",
        "temperature 값을 0으로 두어도, 모델이 도구 호출 요청을 보낼지가 매번 같다고 보장하지는 않습니다.",
    ) + [
        md("""## 3. 오늘 처리할 문의

이번 실습은 자료실 창구에 들어온 문의 하나를 그래프로 처리합니다.
문의 글은 01절 7절 대출 질문 그대로이고, 이 절에서 실행 전에 정했습니다.
다음 셀은 문의 글로 첫 상태를 만듭니다.
이 첫 상태를 실행 1과 실행 2에 똑같이 넣습니다."""),
        code(INQUIRY),
        md("""**결과 읽기** — 출력 줄 `첫 상태의 칸: ['messages', 'trace']`로 메시지 칸과 실행 흔적 칸을 확인합니다.
메시지 칸에는 문의 하나를 담고, 흔적 칸은 빈 목록으로 두었습니다.
출력 줄 `출처:`는 이 문의가 어디서 왔는지 적은 줄입니다.

## 4. 재료 · 자료와 도구와 오류 처리 함수

다음 셀은 01절과 글자까지 같은 셀로, 주제어를 키로 한 규정 딕셔너리를 만듭니다."""),
        code(POLICY_DATA),
        md("""**결과 읽기** — 출력 줄 `규정 주제어: ['대출', '운영', '연체']`로 키 셋을 확인합니다.
오늘 문의는 대출 규정을 찾아야 답할 수 있는 질문입니다.

다음 셀은 03·04절과 글자까지 같은 도구 셀입니다.
01절 도구와 코드가 같고, 오류 줄 위 주석 한 줄만 「02절에서 본 ValueError」로 적었습니다."""),
        code(DEF_TOOL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
딕셔너리에 없는 주제어를 받으면, 도구는 `ValueError`를 냅니다.

다음 셀은 01절과 글자까지 같은 셀로, 도구 목록을 모델에게 알려 준 `bound_model`을 만듭니다."""),
        code(BIND),
        md("""**결과 읽기** — 출력 줄 `실어 보낼 명세 수: 1`과 `여럿 담기: False`는 01절과 같습니다.
한 응답에는 도구 호출 요청이 하나까지만 담깁니다.
그래서 요청이 든 응답마다 도구 실행 노드가 한 번 실행되고, 도구 메시지가 하나 생깁니다.

다음 셀은 02절 7절과 글자까지 같은 오류 처리 함수입니다.
도구 실행 노드가 넘긴 `ValueError` 하나로, 도구 메시지에 담을 안내 글을 만들어 내놓습니다.
첫 매개변수 뒤 `: ValueError`는 02절에서 본 받을 오류 표시이고, 라이브러리가 이 표시를 읽습니다."""),
        code(DEF_HANDLER),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
02절에서 본 설치판 소스대로면, 받을 오류 표시가 `ValueError`인 이 함수에는 다른 종류의 오류가 넘어오지 않습니다.

다음 셀은 이 함수를 그래프 없이 한 번 불러, 어떤 글을 내놓는지 봅니다.
02절 7절 셀과 코드가 같고, 첫 줄 주석만 이 절에 맞게 적었습니다."""),
        code(TRY_HANDLER),
        md("""**결과 읽기** — 라벨 `내놓은 글:` 뒤에 안내 글 한 줄이 보입니다.
괄호 안 `지원하지 않는 주제: 주차`가 오류의 글이고, 괄호 뒤 문장이 주제어 안내입니다.
조립한 그래프에서 도구가 이 오류를 내면, 이 글이 도구 메시지의 내용이 됩니다.

## 5. 조립 · 01절 그래프에 오류 처리 함수 붙이기

조립에 쓰는 상태 형식과 모델 노드는 01절 셀 그대로입니다.
다음 셀은 01절과 글자까지 같은 상태 형식입니다."""),
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
메시지 칸에는 메시지 리듀서, 실행 흔적 칸에는 이어 붙이기 규칙을 적었습니다.

다음 셀은 01절과 글자까지 같은 모델 노드입니다."""),
        code(CALL_MODEL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 노드를 지날 때마다 모델 요청이 한 번 나가고, 실행 흔적 칸에 `model`이 붙습니다.

다음 셀은 02절 7절처럼 오류 처리 함수를 넘겨 도구 실행 노드를 만듭니다.
오류 처리 인자 `handle_tool_errors`에 4절의 함수를 넘깁니다."""),
        code(POLICY_NODE),
        md("""**결과 읽기** — 출력 줄 `만든 것의 종류: ToolNode`와 `안에 든 도구 찾기 표의 키: ['lookup_policy']`입니다.
01절 도구 실행 노드와 다른 것은 오류 처리 인자 하나입니다.

다음 셀은 01절과 글자까지 같은 이름표 표입니다."""),
        code(PATH_MAP),
        md("""**결과 읽기** — 라벨 줄 아래 `tools -> tools`와 `__end__ -> __end__` 두 줄입니다.
도구 조건 함수가 `END`를 내놓으면 가상 끝점으로 갑니다.
03절에서 본 명시적 종료를, 이 그래프에서는 01절 도구 조건 함수가 맡습니다.

다음 셀은 01절 6절과 같은 노드와 엣지로 그래프를 조립합니다.
도구 실행 노드 자리에만 `policy_node`를 넣습니다."""),
        code(BUILD),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['model', 'tools']`입니다.
시작 엣지·조건부 엣지·되돌아가는 엣지는 01절과 같은 세 줄입니다.

다음 셀은 01절 6절과 글자까지 같은 셀로, 그래프가 스스로 그린 구조 문자열을 받아 옵니다."""),
        code(STRUCTURE),
        md("""**결과 읽기** — 라벨 줄 `그래프가 그린 구조:` 아래에서 화살표 줄 넷을 봅니다.
줄 `__start__ --> model`·`model -.-> __end__`·`model -.-> tools`·`tools --> model`입니다.
01절 6절 출력과 같은 넷이라, 오류 처리 함수를 넘겨도 그래프 모양은 그대로입니다.
오류 처리 함수는 노드가 아니라 도구 실행 노드 안에서 쓰여, 구조 문자열에 나오지 않습니다.

## 6. 실행 1 · 한도 10으로 문의 처리하기

첫 실행은 03절 4절과 같은 설정 딕셔너리로 합니다.
실행 한도는 그래프가 한 번 실행에서 진행할 수 있는 단계 수의 한도입니다.
실행 전에 예상해 봅니다.
01절 7절처럼 모델 노드·도구 실행 노드·모델 노드를 지나 끝나고, 모델 요청은 2번일 것입니다.
대출은 딕셔너리에 있는 주제어라, 오류 처리 함수는 쓰이지 않을 것입니다."""),
        code(RUN_ONE),
        md("""**결과 읽기** — 출력 줄 `설정 딕셔너리: {'recursion_limit': 10}`과 `실행 흔적 칸: ['model', 'model']`입니다.
출력 줄 `메시지 칸의 메시지 수: 4`입니다.
모델 노드를 두 번 지났으니, 모델 요청이 2번 나갔습니다.
한도 10에 닿지 않고, 메서드 `invoke`가 결과를 내놓았습니다.

다음 셀은 메시지 칸을 차례로 출력합니다."""),
        code(ONE_SHOW),
        md("""**결과 읽기** — 라벨 줄 아래 네 줄이 메시지 칸입니다.
둘째 줄은 `AIMessage | 도구 호출 요청: ['lookup_policy']`, 넷째 줄은 `AIMessage | 도구 호출 요청: []`입니다.
셋째 줄 도구 메시지는 결과 상태 `success`에 대출 규정 글입니다.
도구가 오류를 내지 않아, 이번 흐름에서 오류 처리 함수는 쓰이지 않았습니다.

다음 셀은 첫 응답에 담긴 요청의 인자와, 도구 메시지의 결과 상태를 봅니다."""),
        code(ONE_CHECK),
        md("""**결과 읽기** — 출력 줄 `도구 이름: lookup_policy | 인자: {'topic': '대출'}`입니다.
출력 줄 `셋째 메시지의 결과 상태: success`입니다.
모델이 딕셔너리에 있는 주제어 `대출`을 골라, 도구가 규정 글을 찾았습니다.
주제어는 모델이 정한 값이라, 실행한 때에 따라 달라질 수 있습니다.

다음 셀은 01절 10절 함수 `run_row`로 실행 결과를 기록 한 줄로 만들고, 노드 실행 수를 셉니다.
01절에서 본 것처럼 도구 실행 노드는 실행 흔적 칸을 쓰지 않습니다.
그래서 모델 노드를 지난 수, 곧 모델 요청 수에 도구 메시지 수를 더합니다."""),
        code(ONE_ROW),
        md("""**결과 읽기** — 라벨 `기록 한 줄:` 뒤 딕셔너리에서 `'모델 요청 수': 2`와 `'도구 메시지 수': 1`을 봅니다.
칸 `'호출 ID 짝': True`로, 도구 메시지에 요청 id가 옮겨진 것도 확인합니다.
출력 줄 `노드 실행 수: 3`은 모델 노드 두 번과 도구 실행 노드 한 번입니다.
이 그래프는 단계마다 노드 하나를 실행하므로, 실행 1은 단계 셋을 지났습니다.

다음 셀은 마지막 응답을 봅니다."""),
        code(ONE_ANSWER),
        md("""**결과 읽기** — 출력 줄 `마지막 응답의 도구 호출 요청 수: 0`입니다.
그래서 도구 조건 함수가 `END`를 내놓아 흐름이 끝났습니다.
03절 말로 명시적 종료이고, 실행 한도에 닿기 전에 일어났습니다.
라벨 줄 `답 글:` 아래는 모델이 도구 메시지를 읽고 쓴 답입니다.

이번 실행에서는 답 글이 도구 메시지의 1인 5권과 14일을 옮겨 적었습니다.
새 커널로 한 번 더 실행했을 때는 답 글의 쉼표 하나가 달랐습니다.
답 글은 실행마다 문장이 달라질 수 있어, 결론에 쓰지 않습니다.

## 7. 실행 2 · 바꿀 값은 실행 한도

바꿀 값은 실행 한도 하나입니다.
한도를 실행 1에서 센 노드 실행 수와 같게 줄이고, 첫 상태·그래프·모델 설정은 그대로 둡니다.
03절 6절에서는 노드를 세 번 실행하는 흐름이 한도 3에서 멈추고 한도 4에서 통과했습니다.
그때는 모델 없는 그래프였고, 이번에는 모델 요청이 든 흐름에서 그 경계의 멈추는 쪽을 봅니다.

다음 셀은 줄인 한도를 담은 설정 딕셔너리를 만듭니다."""),
        code(TIGHT),
        md("""**결과 읽기** — 출력 줄 `실행 2의 설정 딕셔너리: {'recursion_limit': 3}`입니다.
실행 1의 한도 10에서, 한도 하나만 3으로 바뀌었습니다.

다음 셀은 같은 첫 상태를 이 설정으로 실행합니다.
실행 전에 예상해 봅니다.
03절 규칙대로면 한도 3에서는 `GraphRecursionError`가 날 것입니다.
한도에 닿으면 오류가 올라오므로, 이 셀만 그 오류를 받아 출력합니다."""),
        code(RUN_TWO),
        md("""**결과 읽기** — 출력 줄 `받은 오류: GraphRecursionError`입니다.
라벨 줄 `오류 글:` 아래 첫 줄은 `Recursion limit of 3 reached without hitting a stop condition.`로 시작합니다.
한도 3에 닿아, 메서드 `invoke`가 결과를 내놓지 않았습니다.
그래서 이 셀에서는 실행 흔적도, 답 글도, 사용량도 받지 못했습니다.
이 오류는 도구가 낸 오류가 아니라서, 오류 처리 함수가 받지 않았습니다.

노트북 밖에서 같은 흐름을 다섯 번 보냈을 때는, 실행 2도 모두 모델 노드를 두 번 지난 뒤 멈췄습니다.
둘째 요청은 답 글까지 만들었지만, 그 답은 받지 못했습니다.
노트북의 모델 노드는 01절 셀 그대로라, 부른 횟수를 따로 적지 않습니다.

## 8. 두 실행 견주기

다음 셀은 03절 6절 규칙으로, 실행 1의 흐름이 통과하는 가장 작은 한도를 셈합니다.
노드 실행 수보다 하나 큰 값입니다.
그 값을 두 실행의 한도와 견줍니다."""),
        code(COMPARE),
        md("""**결과 읽기** — 출력 줄 `셈으로 통과하는 가장 작은 한도: 4`입니다.
출력 줄 `실행 1 한도가 그 값보다 작은가: False`와 `실행 2 한도가 그 값보다 작은가: True`입니다.
셈으로는 한도가 그 값보다 작은 실행만 멈춥니다.
한도 10인 실행 1은 끝까지 갔고, 한도 3인 실행 2는 멈춰 셈과 맞았습니다.
한도 4로는 이번에 실행하지 않았습니다.

## 9. 요청 수와 예상 비용

다음 셀은 실행 1의 모델 응답 사용량을 더하고, 04절과 같은 요금표로 예상 비용을 셉니다.
예상 비용은 요금표로 어림한 값이라 청구 금액이 아닙니다.
실행 2는 결과를 받지 못해, 같은 방법으로 사용량을 셀 수 없습니다."""),
        code(COST),
        md("""**결과 읽기** — 출력 줄은 `실행 1 사용량: {'requests': 2, 'input_tokens': 378`로 시작합니다.
모델 요청 2번에 입력 토큰 378입니다.
출력 줄 `요금 확인 날짜: 2026-09-17`은 요금표를 확인한 날짜입니다.

칸 `output_tokens`와 예상 비용은 답 글 길이에 따라 실행마다 달라질 수 있습니다.
이번 실행에서는 출력 토큰 46, 예상 비용 0.000491달러였습니다.
새 커널로 한 번 더 실행했을 때는 출력 토큰이 45라 예상 비용도 달랐습니다.
실행 2에서 나간 요청은 사용량을 받지 못해, 이 예상 비용에 들어 있지 않습니다.

## 정리

1. 01절 그래프에 02절 오류 처리 함수와 03절 설정 딕셔너리를 붙여, 대출 문의를 처리했습니다.
2. 실행 1은 노드를 세 번 실행하고 `END`로 끝났고, 도구 오류가 없어 오류 처리 함수는 쓰이지 않았습니다.
3. 한도만 3으로 줄인 실행 2는 `GraphRecursionError`로 멈춰, 실행 흔적도 답 글도 받지 못했습니다.

이 절로 Ch 20이 끝납니다.
Ch 21 01절은 이 챕터에서 직접 이은 반복 구조를 함수 `create_agent` 한 줄로 얻는 법을 다룹니다."""),
    ]


L_01 = "01-ToolNode와-tools-condition.html"
L_02 = "02-도구-오류와-ToolMessage.html"
L_03 = "03-recursion-limit과-명시적-종료.html"
L_04 = "04-if-분기와-모델-선택-비교.html"
L_CH6_06 = "../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html"
L_CH19_05 = "../ch19-model-tools/05-bind_tools와-병렬-호출.html"
L_CH19_06 = "../ch19-model-tools/06-오류와-읽기-쓰기-분리.html"
STYLE = "<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>"


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


LEARNED_TABLE = rows_html([
    [link(L_01, "01절"), "모델 노드·도구 실행 노드(" + c("ToolNode") + ")·도구 조건 함수(" + c("tools_condition") + ")·되돌아가는 엣지, 상태 형식 " + c("AgentState") + ", 함수 " + c("call_id_lists") + "·" + c("run_row"), "그래프 조립, 구조 문자열, 실행 1의 기록 한 줄"],
    [link(L_02, "02절"), "오류 처리 인자(" + c("handle_tool_errors") + ")·오류 처리 함수 " + c("handle_policy_error") + "·받을 오류 표시", "도구 실행 노드 " + c("policy_node") + ", 오류 처리 함수를 그래프 없이 불러 보는 셀 · 흐름에서는 쓰이지 않음(결과 상태 " + c("success") + "로 확인)"],
    [link(L_03, "03절"), "설정 딕셔너리·실행 한도(" + c("recursion_limit") + ")·단계·명시적 종료, 오류 " + c("GraphRecursionError") + ", 노드 실행 수보다 하나 큰 한도부터 통과", "실행 1·2의 설정, 실행 2의 오류 받기, 두 실행 견주기"],
    [link(L_04, "04절"), "도구 파일에 더한 함수 " + c("sum_usage") + "(" + link(L_CH19_05, "Ch 19 05절") + ")·" + c("estimate_cost") + "(" + link(L_CH6_06, "Ch 6 06절") + ")와 요금 변수", "실행 1의 요청 수와 예상 비용"],
    [link(L_CH19_06, "Ch 19 06절"), "함수 " + c("show_messages") + "와 결과 상태", "메시지 칸 출력"],
], ["절", "배운 것", "실습에서 쓰는 곳"])

FUNC_TABLE = rows_html([
    [c("call_model") + "·" + c("path_map") + "·" + c("tools_condition"), "모델 노드, 이름표 표, 도구 조건 함수(그래프 모양)", "01절 셀 그대로"],
    [c("policy_node"), "오류 처리 함수를 넘긴 도구 실행 노드", "02절 7절 모양"],
    [c("limit_config") + "·" + c("tight_config"), "실행 1·2의 설정 딕셔너리(한도 10·노드 실행 수)", "03절 4절 모양"],
    [c("run_row()") + "·" + c("show_messages()"), "실행 결과를 기록 한 줄로 만들기, 메시지 칸 출력", "도구 파일(01절·Ch 19 06절)"],
    [c("sum_usage()") + "·" + c("estimate_cost()"), "요청 수와 토큰 더하기, 예상 비용", "도구 파일(Ch 19 05절·Ch 6 06절)"],
], ["이름", "하는 일", "가져온 곳"])

RESULT_TABLE = rows_html([
    ["실행 1", c("{'recursion_limit': 10}"), "예, " + c("END") + "로 끝남", c("['model', 'model']"), c("success") + " 하나", "3", "2"],
    ["실행 2", c("{'recursion_limit': 3}"), "아니요, " + c("GraphRecursionError"), "받지 못함", "받지 못함", "셀 수 없음", "노트북에서 셀 수 없음(밖에서 2)"],
], ["실행", "설정 딕셔너리", "끝까지 갔는가", "실행 흔적", "도구 메시지", "노드 실행 수", "모델 요청 수"])

LOOK_B5 = ("노트북 6절 출력 <code>실행 흔적 칸: ['model', 'model']</code>과 <code>노드 실행 수: 3</code>으로 실행 1의 흐름을 봅니다. "
           "노트북 7절 출력 <code>받은 오류: GraphRecursionError</code>로 실행 2가 멈춘 것을 봅니다. "
           "노트북 8절 출력 <code>실행 2 한도가 그 값보다 작은가: True</code>로 셈과 결과를 맞춰 봅니다. "
           "답 글 문장과 출력 토큰은 여러분의 실행에서 교재 출력과 다를 수 있습니다.")


def src_html() -> str:
    return ("""<!--meta: 실습 30분 | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 0 -->
""" + STYLE + """
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>01절 그래프에 02절 오류 처리 함수와 03절 설정 딕셔너리를 붙여, 자료실 문의 하나를 처리할 수 있습니다.</li>
<li>붙여 둔 오류 처리 함수가 이번 흐름에서 쓰였는지, 도구 메시지의 결과 상태로 확인할 수 있습니다.</li>
<li>실행 흔적과 도구 메시지 수로 노드 실행 수를 세고, 실행 한도와 견줄 수 있습니다.</li>
<li>실행 한도 하나만 노드 실행 수와 같게 줄여 다시 실행하고, 두 실행의 결과를 견줄 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>이 챕터에서는 그래프 부품을 절마다 따로 익혔습니다. """ + link(L_01, "01절") + """은 모델 노드와 도구 실행 노드를 되돌아가는 엣지로 이었습니다. """ + link(L_02, "02절") + """은 도구가 낸 오류를 도구 메시지로 바꾸는 오류 처리 함수를 봤습니다. """ + link(L_03, "03절") + """은 실행 한도와 명시적 종료를 봤습니다. 실제 창구에서는 이 부품들이 한 그래프 안에서 함께 일합니다.</p>
<p>이번 실습은 01절 그래프에 오류 처리 함수와 실행 한도를 붙여, 자료실 문의 하나를 처리합니다. 실행 한도 하나만 바꿔 한 번 더 실행하고, 두 실행을 견줍니다. 실행 1은 01절 대출 흐름과 같은 차례입니다. 새로 볼 것은 한도를 그 흐름의 노드 실행 수와 같게 줄인 실행 2입니다. 03절은 이 경계를 모델 없는 그래프에서만 실행했습니다.</p>
<p>오류 처리 함수는 붙여 두었지만, 이번 두 실행에서는 쓰이지 않았습니다. 실행 1에서는 도구 메시지의 결과 상태 <code>success</code>로 그 사실을 확인합니다.</p>
<p>이번 절은 이 챕터의 실습입니다. 01~04절에서 쓴 이름과 문법만 쓰고 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p>
<p><strong>이 절의 질문</strong> — 모델이 도구를 부르는 그래프에서, 실행 한도를 노드 실행 수와 같게 두면 어떻게 될까요? 한도에 닿은 실행에서 우리는 무엇을 받지 못할까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>이번 실습은 아래 절에서 배운 이름을 그대로 씁니다. 함수는 도구 파일 <code>graph_tools.py</code>에서 가져오고, 도구와 노드와 오류 처리 함수는 노트북에 적습니다.</p>
""" + LEARNED_TABLE + """
<p>세 절의 기능을 고른 까닭은, 이 챕터의 그래프 하나에 모두 붙일 수 있기 때문입니다. 오류 처리 함수는 도구 실행 노드를 만드는 줄에 붙습니다. 실행 한도는 메서드 <code>invoke</code>의 둘째 인자에 붙습니다. 그래프 모양은 01절과 같아, 두 실행에서 바뀌는 것은 한도 하나뿐입니다. 요청 수는 모델이 도구를 부른 수에 마지막 답 하나를 더한 수라, 실행 전에 범위로 어림할 수 있습니다.</p>
<p>오류 처리 함수는 붙여 두었지만, 이번 두 실행에서는 쓰이지 않았습니다. 문의에 든 대출이 딕셔너리에 있는 주제어라, 도구가 오류를 내지 않았기 때문입니다. 딕셔너리에 없는 주제를 묻는 문의는 노트북 밖에서 먼저 보내 봤습니다. 모델이 그 주제어를 도구에 넣지 않아, 실습 문의로 쓰지 않았습니다. 그 결과는 본문 7에 적었습니다.</p>
<p>04절 두 그래프 견주기는 04절 실험을 되풀이하게 되어 뺐습니다. 02절 Before의 기본값 도구 실행 노드와 03절 Before의 끝나는 엣지가 없는 그래프도 뺐습니다. 두 장면은 앞 절에서 결함으로 이미 봤고, 이번에는 제대로 조립한 그래프에 한도 하나만 바꿉니다. 01절의 인사 질문과 운영·연체 질문은 요청 수를 늘려 뺐습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절부터 이어 온 두 층 자료실에, 앞 절 소품을 승강 통로 하나에 모아 붙여 봅니다. 서고 옆 벽에는 02절의 빈 카드를 꽂아 둔 주머니가 있습니다. 쪽지에 적힌 책이 서고에 없으면, 서고는 책 대신 이 주머니의 빈 카드를 상자에 싣습니다. 통로 옆 벽에는 03절 계수기 판이 있어, 상자가 한 층을 들를 때마다 등이 하나씩 켜집니다. 창구 층에는 03절 받침이 있어, 찾을 쪽지가 남지 않으면 상자가 거기에 섭니다.</p>
{{img:""" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + """}}
<p class="look"><b>그림 읽기</b> — """ + ILLU_READ + """</p>
<p class="look">쪽지는 도구 호출 요청, 파란 책은 결과 상태 <code>success</code>인 도구 메시지입니다. 빈 카드 주머니는 오류 처리 함수, 계수기 판은 실행 한도, 받침은 명시적 종료입니다. 계수기 판은 한도 10을 등 여섯으로 줄여 그렸고, 켜진 등 셋만 실행 1이 지난 단계 셋입니다. 대출 쪽지라 책이 서고에 있어, 빈 카드는 쓰이지 않았습니다. 계수기 칸 수를 셋으로 줄인 실행 2에서는, 등 셋이 켜질 때 칸이 다 차서 상자가 받침에 얹히기 전에 멈춥니다.</p>
<h3>실습 조립의 구성</h3>
{{mermaid:""" + FIG1 + "|" + FIG1_ALT + "|" + FIG1_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG1_READ) + """</p>
""" + FUNC_TABLE + """
<h3>두 번의 실행</h3><p>실행 1은 03절과 같은 한도 10으로 실행합니다. 실행 2는 한도 하나만 실행 1에서 센 노드 실행 수와 같게 줄입니다. 첫 상태·그래프·모델 설정은 두 실행이 같습니다.</p><p>노드 실행 수는 실행 흔적 칸의 <code>model</code> 수에 도구 메시지 수를 더해 셉니다. 01절에서 본 것처럼 도구 실행 노드는 흔적 칸을 쓰지 않기 때문입니다. 한 응답에 요청을 하나까지만 받게 해, 도구 실행 노드가 한 번 실행될 때 도구 메시지가 하나 생깁니다.</p>
<h3>비교와 경계</h3><p>도구가 낸 <code>ValueError</code>는 오류 처리 함수가 받아 도구 메시지로 바꾸고, 흐름은 모델 노드로 이어집니다. 02절에서 본 장면입니다. 실행 한도에 닿아 난 <code>GraphRecursionError</code>는 도구가 낸 오류가 아닙니다. 오류 처리 함수는 이 오류를 받지 않고, 오류는 메서드 <code>invoke</code> 밖으로 올라옵니다. 그러면 그때까지 쌓인 메시지도 결과로 받지 못합니다.</p><p>이 오류 처리 함수의 받을 오류 표시는 <code>ValueError</code> 하나입니다. 02절 값 바꿔 보기의 인자 이름이 틀린 요청처럼, 입력 검사에서 걸린 오류는 받지 않아 흐름이 멈춥니다. 02절에서 본 장면이고, 이번에는 실행하지 않았습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 문의 글로 첫 상태를 만들고, 01~03절 셀로 자료·도구·모델·오류 처리 함수를 준비합니다. 오류 처리 함수는 그래프 없이 한 번 불러, 내놓는 글을 봅니다. 그다음 01절 그래프에 오류 처리 함수를 넘긴 도구 실행 노드를 넣어 조립합니다. 실행 1은 한도 10으로, 실행 2는 한도만 노드 실행 수와 같게 줄여 실행합니다. 마지막에 두 실행을 견주고, 실행 1의 요청 수와 예상 비용을 셉니다.</p><p>실제 OpenAI 모델을 부릅니다. 교재 출력은 """ + RUN_DATE + """에 실행한 결과입니다. 모델은 <code>gpt-5.4-mini</code>이고 temperature 0과 추론 끔(<code>reasoning_effort="none"</code>)으로 부릅니다.</p><p>교재 출력에서 모델 요청은 실행 1이 2번이었습니다. 실행 2는 결과를 받지 못해 노트북에서는 셀 수 없고, 노트북 밖 다섯 번에서는 2번이었습니다. 그래서 모델 요청은 모두 4번으로 어림합니다.</p><p>요금표로 어림한 예상 비용은 0.01달러 아래이고, 청구 금액과는 다를 수 있습니다. 새로 쓰는 파일은 없습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
<h3>실행 1의 실제 순서</h3>
{{mermaid:""" + FIG2 + "|" + FIG2_ALT + "|" + FIG2_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG2_READ) + """</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>두 실행은 실행 한도 하나만 달랐습니다. 결과는 아래 표와 같았습니다.</p>
""" + RESULT_TABLE + """
{{mermaid:""" + FIG3 + "|" + FIG3_ALT + "|" + FIG3_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG3_READ) + """</p>
<p>실행 1은 모델 노드·도구 실행 노드·모델 노드를 지나, 도구 조건 함수의 <code>END</code>로 끝났습니다. 노드 실행 수는 3이고, 한도 10에 닿지 않았습니다. 모델은 딕셔너리에 있는 주제어 대출을 적었고, 도구 메시지의 결과 상태는 <code>success</code>였습니다. 도구 오류가 없어 오류 처리 함수는 쓰이지 않았습니다.</p>
<p>실행 2는 한도를 3으로만 바꿨고, <code>GraphRecursionError</code>로 멈췄습니다. 메서드 <code>invoke</code>가 결과를 내놓지 않아, 실행 흔적·답 글·사용량을 하나도 받지 못했습니다. 노트북 밖 다섯 번에서는 실행 2도 모델 노드를 두 번 지났고, 둘째 요청은 답까지 만든 뒤 멈췄습니다. 요청은 나갔지만 답은 받지 못한 셈입니다.</p>
<p>03절 6절에서 모델 없는 그래프는 노드를 세 번 실행하면 한도 3에서 멈추고 한도 4에서 통과했습니다. 이번 모델 흐름도 노드 실행 수 3과 같은 한도에서 멈춰, 03절 경계의 멈추는 쪽과 같았습니다. 한도 4로는 이번에 실행하지 않았습니다.</p>
<p>모델 흐름의 노드 실행 수는 모델이 도구를 몇 번 부르느냐에 달려 있습니다. 실행 2처럼 노드 실행 수와 같은 한도로는 같은 흐름도 멈췄습니다. 통과하는 가장 작은 한도(노드 실행 수 + 1)에 맞춰도, 도구를 한 번 더 부르는 실행은 셈으로 한도에 닿습니다.</p>
<p>노트북 6~8절의 실행 흔적·도구 메시지·노드 실행 수·받은 오류는 새 커널 두 번에서 모두 같았습니다. 노트북 밖에서 같은 두 실행을 다섯 번 보냈을 때도 같았습니다. 두 번에서 달랐던 것은 답 글의 쉼표 하나와 출력 토큰, 그 토큰이 든 예상 비용이었고 결론에 쓰지 않았습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>문의 글은 01절 7절 대출 질문 그대로이고, 실행 전에 정했습니다. 실제 이용자가 보낸 글이 아닙니다.</li><li>노트북을 실행하기 전에 문의 후보를 차례로 정해 두고, 노트북 밖에서 후보마다 두 실행을 다섯 번씩 보냈습니다. 첫 후보는 02절 주차 질문 「자료실 주차 규정을 알려 주세요.」였습니다.</li><li>주차 질문의 첫 요청 열 번 가운데 여덟 번은 모델이 주제어 운영을 적었고, 두 번은 도구를 부르지 않았습니다. 실행 1의 다섯 번은 모두 오류 없이 운영 시간을 답해, 물음과 어긋난 답이 되었습니다.</li><li>둘째 후보 「주제어 주차로 자료실 규정을 찾아 주세요.」는 다섯 번 모두 도구를 부르지 않았습니다. 두 후보 모두 주차를 도구에 넣은 적이 없어, 오류 처리 함수가 쓰이는 장면이 나오지 않았습니다.</li><li>그래서 셋째 후보인 대출 문의를 실습 문의로 썼습니다. 흐름을 보여 주려고 정한 예이고, 후보와 차례는 첫 요청 전에 적어 두었습니다.</li><li>오류 처리 함수는 02절 판 그대로, 도구 몸통이 낸 <code>ValueError</code>만 받도록 좁힌 설계입니다. 딕셔너리에 없는 주제어가 도구에 들어올 때만 일하고, 입력 검사 오류까지 받는 방법은 이번에 실행하지 않았습니다. 모델이 비슷한 다른 주제어로 바꿔 찾으면 오류가 나지 않아, 이 함수로는 어긋난 답을 막지 못합니다.</li><li>대출 문의를 다섯 번씩 보냈을 때, 실행 1은 모두 흔적 <code>['model', 'model']</code>과 노드 실행 수 3이었습니다. 실행 2는 모두 <code>GraphRecursionError</code>였습니다. 같은 요청도 실행한 때에 따라 모델이 도구를 부를지가 달라질 수 있습니다.</li><li>실행 2의 한도는 실행 1에서 센 노드 실행 수를 그대로 쓴 값입니다. 실행 1에서 모델이 도구를 다른 수만큼 부르면, 실행 2의 한도도 함께 달라집니다.</li><li>실행 2의 모델 요청 수 2는 노트북 밖에서 모델 노드를 부른 횟수를 적어 센 값입니다. 노트북의 모델 노드는 01절 셀 그대로라 그 기록이 없습니다.</li><li>인자 <code>parallel_tool_calls=False</code>는 01절 그대로입니다. 한 응답에 요청 여럿을 받으면 도구 실행 노드 한 번에 도구 메시지가 여럿 생겨, 이 절의 노드 실행 수 셈이 맞지 않습니다. 이 조합은 이번에 실행하지 않았습니다.</li><li>모델이 정하는 값, 곧 도구 호출 요청과 답 글에는 <code>assert</code>를 걸지 않았습니다. 이 노트북의 <code>assert</code>는 키 확인 셀 하나뿐입니다.</li><li>이 절은 파일을 쓰지 않습니다. 걸린 시간은 재지 않았습니다.</li><li>예상 비용은 2026-09-17 요금표로 어림한 값이고 청구 금액이 아닙니다. 실행 2에서 나간 요청은 사용량을 받지 못해 예상 비용에 들어 있지 않습니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>01절 그래프에 02절 오류 처리 함수와 03절 설정 딕셔너리를 붙여, 대출 문의를 처리했습니다.</li><li>실행 1은 노드를 세 번 실행하고 <code>END</code>로 끝났고, 도구 오류가 없어 오류 처리 함수는 쓰이지 않았습니다.</li><li>한도만 3으로 줄인 실행 2는 <code>GraphRecursionError</code>로 멈춰, 실행 흔적도 답 글도 받지 못했습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 20이 끝납니다. Ch 21 01절은 이 챕터에서 직접 이은 반복 구조를 함수 <code>create_agent</code> 한 줄로 얻는 법을 다룹니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. [하] 두 실행에서 바꾼 값은 무엇입니까?</p><p class="quiz-a">설정 딕셔너리의 실행 한도 하나입니다. 실행 1은 10, 실행 2는 실행 1의 노드 실행 수와 같은 3이었습니다. 첫 상태와 그래프와 모델 설정은 같게 두었습니다.</p><p class="quiz-q">2. [중] 실행 1의 노드 실행 수를 실행 흔적 칸의 길이만으로 세지 않은 까닭은 무엇입니까?</p><p class="quiz-a">도구 실행 노드는 흔적 칸을 쓰지 않아, 흔적 칸에는 모델 노드만 남기 때문입니다. 그래서 도구 메시지 수를 더해 3을 얻었습니다. 틀렸다면 노트북 6절과 01절을 다시 읽습니다.</p><p class="quiz-q">3. [중] 실행 2에서 우리가 받지 못한 것은 무엇이고, 까닭은 무엇입니까?</p><p class="quiz-a">실행 흔적·답 글·사용량을 받지 못했습니다. 한도 3이 노드 실행 수 3과 같아 <code>GraphRecursionError</code>가 났고, 메서드 <code>invoke</code>가 결과를 내놓지 않았기 때문입니다. 틀렸다면 노트북 7절과 03절을 다시 읽습니다.</p><p class="quiz-q">4. [상] 동료가 「오류 처리 함수를 붙였으니 이 그래프는 오류로 멈추지 않는다」고 말합니다. 이 절 결과로 무엇이라고 답하나요?</p><p class="quiz-a">이 오류 처리 함수는 도구 몸통이 낸 <code>ValueError</code>만 받도록 좁힌 설계라고 답합니다. 실행 2의 한도 오류는 받지 않아 흐름이 멈췄습니다. 02절 8절에서 본 입력 검사 오류도 받지 않습니다. 틀렸다면 노트북 7절과 02절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li>01절 — 모델 노드·도구 실행 노드·도구 조건 함수·되돌아가는 엣지, 함수 <code>run_row</code>.</li><li>02절 — 오류 처리 인자와 오류 처리 함수, 받을 오류 표시.</li><li>03절 — 설정 딕셔너리와 실행 한도, 노드 실행 수와 통과하는 한도의 경계.</li><li>04절 — 도구 파일에 더한 사용량·예상 비용 함수.</li><li>Ch 19 06절 — 함수 <code>show_messages</code>와 결과 상태.</li><li>Ch 6 06절 — 요금표와 예상 비용.</li><li>기준 버전은 노트북 1절 첫 셀에서 설치한 패키지 다섯의 판입니다. 그래프는 langgraph 1.2.11로 만들었습니다.</li></ul>
""")


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


def same_ast(left: str, right: str) -> bool:
    return ast.dump(ast.parse(left)) == ast.dump(ast.parse(right))


if __name__ == "__main__":
    # 01절 셀과 글자까지 같은 셀
    for name in ["INSTALL", "POLICY_DATA", "BIND", "STATE", "CALL_MODEL", "PATH_MAP", "STRUCTURE"]:
        assert globals()[name] == getattr(author_01, name), name
    # 도구 셀은 03절 셀과 글자까지 같고, 01절과 AST가 같다
    assert DEF_TOOL == author_03.DEF_TOOL and same_ast(DEF_TOOL, author_01.DEF_TOOL)
    # 오류 처리 함수는 02절 셀과 글자까지 같고, 불러 보는 셀은 02절 셀과 AST가 같다(첫 줄 주석만 다름)
    assert DEF_HANDLER == author_02.DEF_HANDLER
    assert same_ast(TRY_HANDLER, author_02.TRY_HANDLER) and TRY_HANDLER != author_02.TRY_HANDLER
    # 오류 처리 함수의 안내 글은 흔들림 확인(probe05.py)과 같다
    assert author_02.HANDLER_TEXT in (Path(__file__).resolve().parent / "probe/probe05.py").read_text(encoding="utf-8")
    if os.environ.get("AUTHOR05_NB_ONLY") != "1":
        print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "05", SLUG, "experiment", cells())
        print("wrote", path)
