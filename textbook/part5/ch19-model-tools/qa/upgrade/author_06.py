"""Ch 19 06절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 author_06.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_06.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
  AUTHOR06_NB_ONLY=1 python3 author_06.py → 노트북만 다시 쓴다
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **paired 형식 유지**(chapter.json).
이 챕터 본문의 마지막 절이다(07 실습 절은 다음 작업자 몫).

## 결정 1 — 한 흐름에 결함 둘 (인계 §05→§06 5항)

Before는 05절 방식 그대로다: 읽기 도구 get_order_by_id와 쓰기 도구 cancel_order(이 절의 흉내 — 파일을 바꾸지 않음)를
한 목록으로 bind_tools에 넘기고, 읽기 도구의 handle_tool_error는 기본값 False로 둔다. 질문 둘 —
「O101 주문을 취소해 줘.」(첫 응답만 보고 도구는 실행하지 않음)와 「O999 주문의 금액을 알려 줘.」(05 ask_until_answer로
끝까지 → 도구 안 ToolException이 루프를 뚫고 올라와 멈춤, 메시지 2). After는 같은 도구의 handle_tool_error = True
(속성 — @tool(handle_tool_error=True)는 TypeError) + pick_tools(읽기, 쓰기, person_confirmed=False)로 나눈 목록.
값 바꿔 보기는 person_confirmed 하나만 True로. 전역 확인 상태를 도구가 읽지 않고, 확인 값이 도구 목록 구성을 정한다.

## 결정 2 — 흔들림 먼저 확인 (규격 §2-7 10번 끝, qa/upgrade/06-probe.md)

같은 첫 요청(한 목록 + 취소 질문) 11번 가운데 10번 cancel_order, 1번 get_order_by_id(V 4회차)라 Before 쓰기 결함은
코드 쪽 사실(명세에 cancel_order가 실림 — spec_names 출력)로 세우고, 첫 응답의 도구 이름은 결과 읽기 둘째 단락·b7에만.
O999 첫 요청은 10/10 get_order_by_id(O999) → 오류 장면은 모델 요청으로. After 두 흐름의 표지는 5/5 같음.

## 결정 3 — assert·도구 파일

assert는 준비 셀 둘과 CSV에서 정해지는 O101 상태에만 건다(모델 출력 0). 이 절에서 처음 가르친 평범한 함수 넷
(pick_tools·make_tools_table·spec_names·show_messages)은 같은 본문을 도구 파일에 옮긴다(`# Ch 19 06절에서 배웠습니다`).
@tool 감싸기와 handle_tool_error 설정은 노트북에 남는다.

## 모델 요청

노트북 한 번 **8~9번**(6절 2 · 7절 4 · 8절 2~3). 읽는 파일 orders.csv(읽기 도구 몸통·8절 확인), 쓰는 파일 0.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`sorted`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·튜플 풀기·세미콜론·
`isinstance`·클래스·try `else`·별표 풀기·`tool_choice`·시스템 메시지·`ToolNode`·`ToolMessage(…)` 직접 만들기.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402
import author_03  # noqa: E402
from author_05 import html_text  # noqa: E402

LAB = ROOT / "labs/part5/ch19-model-tools/notebooks"
SLUG = "06-오류와-읽기-쓰기-분리"
SRC = ROOT / "textbook/part5/ch19-model-tools/_src" / (SLUG + ".html")
# 교재 출력을 만든 실행의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답)에서 읽은 값
RUNSEC = os.environ.get("AUTHOR06_RUNSEC", "10초 안에")

# 흔들림 확인(06-probe.md)에 쓴 설명과 글자까지 같다(아래 assert)
READ_DOC = "주문 번호로 주문 한 건을 찾습니다. 질문에 O103 같은 주문 번호가 있을 때 씁니다. 인자 order_id는 찾을 주문 번호입니다. 그 주문 한 줄을 딕셔너리로 내놓고, 없으면 오류를 냅니다."
WRITE_DOC = "주문 번호로 주문 취소 요청을 등록합니다. 손님이 주문을 취소해 달라고 할 때 씁니다. 인자 order_id는 취소할 주문 번호입니다. 등록한 주문 번호를 딕셔너리로 내놓습니다."

INSTALL = install_source([
    "langchain==1.4.0", "langchain-core==1.6.2", "langchain-openai==1.6.0", "pandas==3.0.5", "python-dotenv==1.2.3",
])
IMPORTS = r'''# 모델·도구·도구 오류·메시지를 만드는 이름과 도구 파일의 함수 여섯을 가져옵니다
import os

from langchain.chat_models import init_chat_model
from langchain.tools import ToolException, tool
from langchain_core.messages import HumanMessage

from order_tools import ask_until_answer, estimate_cost, find_order, run_tool_calls, sum_usage, tool_call_names

print("가져온 이름:", "os", "init_chat_model", "ToolException", "tool", "HumanMessage")'''

# 01~05절 자리 찾기 셀과 글자까지 같다(아래 assert)
PATH = author_03.PATH

DEF_READ = r'''# 주문 한 건을 찾는 읽기 도구를 만들고, 없는 주문이면 도구 오류를 냅니다
@tool
def get_order_by_id(order_id: str):
    """''' + READ_DOC + r'''"""
    order = find_order(csv_path, order_id)
    # 찾지 못하면 None 대신 도구 오류를 내서, 무엇이 잘못됐는지 글로 알립니다
    if order is None:
        raise ToolException("주문 번호 " + order_id + "에 맞는 주문이 없습니다. 주문 번호를 다시 확인해 주세요.")
    return order'''

READ_OK = r'''# 있는 주문 O101을 읽기 도구로 찾고, 오류 담기 설정의 기본값을 봅니다(모델 요청 없음)
found = get_order_by_id.invoke({"order_id": "O101"})
print("찾은 주문:", found)
print("오류 담기 설정(handle_tool_error):", get_order_by_id.handle_tool_error)'''

READ_MISSING = r'''# 없는 주문 O999를 넣어 도구 오류가 올라오는지 봅니다(이 셀만 그 오류를 받아 출력합니다)
try:
    get_order_by_id.invoke({"order_id": "O999"})
except ToolException as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:", error)'''

DEF_WRITE = r'''# 주문 취소 요청을 등록하는 쓰기 도구를 만듭니다(이 절의 흉내라 아무 파일도 바꾸지 않습니다)
@tool
def cancel_order(order_id: str):
    """''' + WRITE_DOC + r'''"""
    # 실제 서비스라면 여기서 주문 상태가 바뀝니다. 이 절에서는 받은 번호만 적어 내놓습니다
    return {"order_id": order_id, "cancel_requested": True}'''

SPLIT = r'''# 도구를 읽기 도구 목록과 쓰기 도구 목록으로 나눠 담습니다
read_tools = [get_order_by_id]
write_tools = [cancel_order]
print("읽기 도구:", read_tools[0].name)
print("쓰기 도구:", write_tools[0].name)'''

DEF_PICK = r'''# 사람 확인 값에 따라 모델에게 알려 줄 도구 목록을 만듭니다
def pick_tools(read_tools, write_tools, person_confirmed):
    # 읽기 도구는 늘 담고, 원래 목록을 건드리지 않게 새 목록으로 복사합니다
    tools = list(read_tools)
    # 사람이 확인한 뒤에만 쓰기 도구를 목록에 더합니다
    if person_confirmed:
        tools = tools + write_tools
    return tools'''

PICK_TRY = r'''# 확인 전(False)과 확인 뒤(True)에 목록에 들어가는 도구 이름을 봅니다(모델 요청 없음)
for person_confirmed in [False, True]:
    picked = pick_tools(read_tools, write_tools, person_confirmed)
    names = []
    for one_tool in picked:
        names.append(one_tool.name)
    print("사람 확인:", person_confirmed, "| 도구:", names)'''

DEF_TABLE = r'''# 도구 목록으로 도구 찾기 표를 만듭니다(05절 4절 셀을 함수로 옮긴 것)
def make_tools_table(tools):
    tools_by_name = {}
    for one_tool in tools:
        tools_by_name[one_tool.name] = one_tool
    return tools_by_name'''

DEF_SPEC = r'''# 도구를 알려 준 모델이 요청마다 싣는 명세에서 도구 이름만 모읍니다
def spec_names(bound_model):
    names = []
    for spec in bound_model.kwargs["tools"]:
        # 명세 한 건은 04절에서 본 모양이고, 도구 이름은 칸 function 안에 있습니다
        names.append(spec["function"]["name"])
    return names'''

BEFORE_BIND = r'''# Before: 05절처럼 읽기 도구와 쓰기 도구를 한 목록으로 모델에게 알려 줍니다(요청은 아직 없음)
before_tools = [get_order_by_id, cancel_order]
# 04절처럼 한 응답에 도구 호출 요청을 하나까지만 받습니다
before_model = model.bind_tools(before_tools, parallel_tool_calls=False)
print("실어 보낼 도구 이름:", spec_names(before_model))'''

BEFORE_WRITE = r'''# 주문을 취소해 달라는 질문을 한 번 보내고, 첫 응답의 도구 호출 요청만 봅니다(모델 요청 1번)
write_question = "O101 주문을 취소해 줘."
first_messages = [HumanMessage(content=write_question)]
before_response = before_model.invoke(first_messages)
print("응답 글의 길이:", len(before_response.content))
print("도구 호출 요청:", tool_call_names(before_response))
for call in before_response.tool_calls:
    print("인자:", call["args"])'''

BEFORE_ERROR = r'''# 없는 주문의 금액을 묻고, 05절 함수 ask_until_answer로 끝까지 처리해 봅니다(모델 요청 1번)
error_question = "O999 주문의 금액을 알려 줘."
turn_limit = 5
before_table = make_tools_table(before_tools)
before_messages = [HumanMessage(content=error_question)]
try:
    ask_until_answer(before_model, before_messages, before_table, turn_limit)
except ToolException as error:
    print("받은 오류:", type(error).__name__, "|", error)
print("메시지 수:", len(before_messages))'''

SET_HANDLE = r'''# After ①: 오류 담기 설정을 True로 바꾸고, Before에서 멈춘 요청을 다시 실행합니다(모델 요청 없음)
get_order_by_id.handle_tool_error = True
read_table = make_tools_table(read_tools)
stopped_response = before_messages[-1]
error_message = run_tool_calls(stopped_response, read_table)[0]
print("내놓은 값의 종류:", type(error_message).__name__)
print("결과 상태(status):", error_message.status)
print("내용:", error_message.content)
print("호출 ID가 요청 id와 같은가:", error_message.tool_call_id == stopped_response.tool_calls[0]["id"])'''

AFTER_BIND = r'''# After ②: 사람 확인 전이라 읽기 도구만 담은 목록을 모델에게 알려 줍니다(요청은 아직 없음)
person_confirmed = False
after_tools = pick_tools(read_tools, write_tools, person_confirmed)
after_model = model.bind_tools(after_tools, parallel_tool_calls=False)
# 도구 찾기 표도 알려 준 목록으로 만들어, 알려 주지 않은 도구는 실행할 수 없게 합니다
after_table = make_tools_table(after_tools)
print("실어 보낼 도구 이름:", spec_names(after_model))'''

DEF_SHOW = r'''# 메시지 목록을 차례로 보며, 응답의 도구 호출 요청과 도구 메시지의 결과 상태를 출력합니다
def show_messages(messages):
    for message in messages:
        kind = type(message).__name__
        if kind == "HumanMessage":
            print(kind)
        if kind == "AIMessage":
            print(kind, "| 도구 호출 요청:", tool_call_names(message))
        if kind == "ToolMessage":
            print(kind, "| 결과 상태:", message.status, "| 내용:", message.content)'''

AFTER_WRITE = r'''# 같은 취소 질문을 읽기 도구만 아는 모델로 끝까지 처리합니다(모델 요청 2번 안팎)
write_messages = [HumanMessage(content=write_question)]
write_messages = ask_until_answer(after_model, write_messages, after_table, turn_limit)
show_messages(write_messages)
print("답 글:")
print(write_messages[-1].content)'''

AFTER_ERROR = r'''# 같은 O999 질문을 오류 담기 설정을 켠 읽기 도구로 끝까지 처리합니다(모델 요청 2번 안팎)
error_messages = [HumanMessage(content=error_question)]
error_messages = ask_until_answer(after_model, error_messages, after_table, turn_limit)
show_messages(error_messages)
print("답 글에 O999가 있는가:", "O999" in error_messages[-1].content)
print("답 글:")
print(error_messages[-1].content)'''

CONFIRM_BIND = r'''# 바꿀 값: person_confirmed를 True로 바꿔, 사람이 취소를 확인한 뒤의 목록을 알려 줍니다
person_confirmed = True
confirmed_tools = pick_tools(read_tools, write_tools, person_confirmed)
confirmed_model = model.bind_tools(confirmed_tools, parallel_tool_calls=False)
confirmed_table = make_tools_table(confirmed_tools)
print("실어 보낼 도구 이름:", spec_names(confirmed_model))'''

CONFIRM_RUN = r'''# 같은 취소 질문을 확인 뒤 목록으로 끝까지 처리합니다(쓰기 도구는 이 절의 흉내, 모델 요청 2번 안팎)
confirmed_messages = [HumanMessage(content=write_question)]
confirmed_messages = ask_until_answer(confirmed_model, confirmed_messages, confirmed_table, turn_limit)
show_messages(confirmed_messages)
print("답 글:")
print(confirmed_messages[-1].content)'''

CSV_CHECK = r'''# 쓰기 도구가 흉내였는지, 주문 CSV에서 O101의 상태를 다시 읽어 봅니다(모델 요청 없음)
order_after = find_order(csv_path, "O101")
print("CSV의 O101 상태:", order_after["status"])
# CSV 파일에서 정해지는 값이라 assert로 확인할 수 있습니다
assert order_after["status"] == "paid", "쓰기 도구는 흉내라 CSV를 바꾸지 않아야 합니다"'''

COST = r'''# 이 노트북의 모델 응답을 모두 모아 요청 수·토큰과 예상 비용을 셉니다(요청 없음)
all_messages = [before_response] + before_messages + write_messages + error_messages + confirmed_messages
total_usage = sum_usage(all_messages)
pricing_date = "2026-09-17"
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
total_cost = estimate_cost(total_usage, input_rate, cached_input_rate, output_rate)
print("요금 확인 날짜:", pricing_date)
print("모두 합친 사용량:", total_usage)
print("예상 비용(달러):", round(total_cost, 6))'''


FIG1 = "06-1-확인-전-목록과-오류-메시지"
FIG1_ALT = "위에서 아래로 한 줄로 이어지는 그림으로 파란 상자 확인 전 목록 pick_tools 사람 확인 False 읽기 도구 하나 get_order_by_id에서 시작해 보라 상자 gpt-5.4-mini 요청 1 O999 주문의 금액을 알려 줘, 노란 상자 도구 호출 요청 get_order_by_id O999, 회색 상자 ToolException 오류 담기 설정 True, 노란 상자 도구 메시지 결과 상태 error 내용 오류 글, 보라 상자 gpt-5.4-mini 요청 2 질문 첫 응답 도구 메시지를 차례로 거쳐 노란 상자 최종 답 도구 호출 요청 0건 답 글에 O999 있음으로 끝나는 그림"
FIG1_CAP = "확인 전 목록으로 없는 주문을 묻자, 도구 오류가 도구 메시지로 모델에게 가고 모델이 글로 답했습니다."
FIG1_READ = """위에서 아래로 읽습니다.
맨 위 파란 상자는 사람 확인 전이라 읽기 도구만 담은 목록입니다.
노란 도구 호출 요청이 회색 상자에서 도구 오류를 만나고, 오류 담기 설정이 켜져 있어 도구 메시지가 됩니다.
보라 모델은 그 도구 메시지를 받고 도구 없이 최종 답을 적습니다.
노란 상자는 노트북 7절 출력입니다."""

FIG2 = "06-2-사람-확인이-정하는-목록"
FIG2_ALT = "위에서 아래로 읽는 그림으로 초록 상자 읽기 도구 목록 get_order_by_id와 초록 상자 쓰기 도구 목록 cancel_order 흉내가 파란 상자 pick_tools 사람 확인 값으로 목록 만들기로 모이고, 점선 두 갈래가 노란 상자 사람 확인 False 도구 get_order_by_id와 노란 상자 사람 확인 True 도구 get_order_by_id cancel_order로 가는 그림"
FIG2_CAP = "같은 두 목록에서 사람 확인 값 하나로 알려 줄 도구가 하나와 둘로 갈렸습니다."
FIG2_READ = "위에서 아래로 읽습니다. 초록 상자 둘은 노트북 4절에서 나눠 담은 두 목록입니다. 파란 함수가 사람 확인 값에 따라 목록을 만들고, 점선 두 갈래는 그 값이 거짓일 때와 참일 때입니다. 노란 상자 둘은 4절 출력이고, 거짓이면 읽기 도구만 남습니다."

FIG3 = "06-3-한-목록과-나눈-목록"
FIG3_ALT = "위에 초록 상자 같은 질문 둘 O101 주문을 취소해 줘와 O999 주문의 금액을 알려 줘가 있고 아래에 칸 둘이 나란히 있는 그림으로 왼쪽 칸 Before 한 목록 오류 담기 False에는 빨간 상자 명세 둘 get_order_by_id cancel_order 확인 없이 쓰기 도구를 고를 수 있음과 빨간 상자 O999 요청에서 ToolException 흐름이 멈춤 메시지 수 2가 있고, 오른쪽 칸 After 나눈 목록 오류 담기 True에는 노란 상자 명세 하나 get_order_by_id 흐름에 cancel_order 요청 없음과 노란 상자 O999 요청이 도구 메시지로 결과 상태 error 최종 답 요청 0건이 있는 그림"
FIG3_CAP = "한 목록의 두 결함은 나눈 목록과 오류 담기로 고쳐져, 쓰기 도구는 명세에서 빠지고 도구 오류는 도구 메시지가 되었습니다."
FIG3_READ = "맨 위 초록 상자는 두 칸에 똑같이 보낸 질문 둘입니다. 왼쪽 칸이 Before, 오른쪽 칸이 After이고, 칸마다 위 상자는 취소 질문, 아래 상자는 O999 질문의 결과입니다. 빨간 상자는 Before의 결함 결과이고, 노란 상자는 After 셀의 출력입니다. 칸 안의 두 상자는 서로 다른 질문이라 화살표로 잇지 않았습니다."

FIG4 = "06-4-확인-뒤-쓰기-도구"
FIG4_ALT = "위에서 아래로 한 줄로 이어지는 그림으로 초록 상자 바꾼 값 person_confirmed True에서 노란 상자 명세 둘 get_order_by_id cancel_order, 보라 상자 gpt-5.4-mini O101 주문을 취소해 줘, 노란 상자 cancel_order 실행 도구 메시지 결과 상태 success cancel_requested true를 거쳐 노란 상자 CSV의 O101 상태 paid 흉내라 파일은 그대로로 끝나는 그림"
FIG4_CAP = "사람 확인 값을 참으로 바꾸자 쓰기 도구가 목록에 들어가 실행되었고, 흉내라 CSV는 그대로였습니다."
FIG4_READ = "위에서 아래로 읽습니다. 맨 위 초록 상자가 값 바꿔 보기에서 바꾼 값 하나입니다. 노란 상자 셋은 노트북 8절 출력이고, 명세에 쓰기 도구가 들어가자 흐름 안에서 그 도구가 실행되었습니다. 맨 아래 상자는 쓰기 도구가 흉내라 주문 CSV가 바뀌지 않았다는 확인입니다."

ILLU = "06-5-열린-창과-걸쇠-건-서랍"
ILLU_ALT = "흰 바탕 그림으로 연초록 벽 왼쪽에 유리도 덧문도 없이 뚫린 나무 틀 창이 하나 있고, 창턱 위에 국수가 담긴 흰 그릇 하나가 놓여 있으며, 창 안쪽 오른쪽 나무 걸이에 국자 하나가 걸려 있고, 벽 아래 긴 나무 카운터의 오른쪽에 둥근 손잡이가 달린 서랍 하나가 닫혀 있으며, 카운터 가장자리의 고리에서 내려온 쇠 걸쇠가 서랍 앞면을 걸어 붙들고 있는 그림"
ILLU_CAP = "열린 창으로는 음식을 내어 주고, 칼을 넣은 서랍은 걸쇠로 닫아 두었습니다."
ILLU_READ = "연초록 벽 왼쪽에 유리도 덧문도 없이 뚫린 나무 틀 창이 하나 있습니다. 창턱에는 국수가 담긴 흰 그릇 하나가 있고, 창 안쪽 걸이에 국자 하나가 걸려 있습니다. 벽 아래 긴 카운터 오른쪽에는 둥근 손잡이가 달린 서랍 하나가 닫혀 있습니다. 카운터 가장자리의 고리에서 내려온 쇠 걸쇠가 서랍 앞면을 걸어 붙들고 있습니다. 열린 창은 읽기 도구, 걸쇠를 건 서랍은 쓰기 도구입니다."

TITLE = """# 오류와 읽기 쓰기 분리

**이 노트북에서 할 일**

1. 없는 주문을 찾던 도구가 오류를 내면, 모델과 주고받던 흐름이 어떻게 되는지 봅니다.
2. 도구 오류를 도구 메시지에 담아 모델에게 보내고, 모델이 도구 없이 답하는지 봅니다.
3. 쓰기 도구를 사람 확인 뒤에만 목록에 넣어, 모델이 고를 수 있는 도구를 나눕니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 모델 요청은 모두 8~9번입니다.
6절에서 2번, 7절에서 4번, 8절에서 2~3번을 보냅니다.
요금표로 센 예상 비용은 모두 합쳐 0.01달러 아래이고, 청구 금액이 아닙니다.

도구는 둘입니다.
읽기 도구는 실습 폴더의 주문 CSV를 읽기만 합니다.
쓰기 도구는 이 절에서 만든 흉내라 아무 파일도 바꾸지 않습니다.
앞 절 함수와 Ch 6 06절 함수는 도구 파일 `order_tools.py`에서 가져옵니다.
교재 출력을 만든 실행에서는 노트북 전체가 """ + RUNSEC + """ 끝났습니다.

**기준 버전** — 첫 셀에서 패키지 다섯을 설치합니다.
판은 langchain 1.4.0, langchain-core 1.6.2, langchain-openai 1.6.0입니다.
pandas 3.0.5와 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3~7절을 읽습니다.
두 도구를 만들고, 05절 방식(Before)과 고친 방식(After)을 견주는 자리입니다.
8~9절은 사람 확인 값을 바꿔 보고 요청 수를 세는 자리이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part5/ch19-model-tools`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

05절에서는 모델이 적어 보낸 도구 호출 요청을 프로그램이 실행하고, 도구 메시지를 모델에게 보냈습니다.
그 절의 도구는 있는 주문만 찾았고, 주문을 읽기만 했습니다.
이 절은 도구가 일을 끝내지 못하는 경우와, 무언가를 바꾸는 도구를 다룹니다.

첫 셀은 패키지 다섯 개를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langchain: 1.4.0`·`langchain-core: 1.6.2`·`langchain-openai: 1.6.0`이 보입니다.
출력 줄 `pandas: 3.0.5`와 `python-dotenv: 1.2.3`도 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

앞에서 배운 함수는 `order_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
오류 이름 `ToolException`은 LangChain이 도구 오류에 쓰는 이름이고, 이 절에서 처음 씁니다.
도구 파일에서는 03절 몸통 함수 `find_order`와 04·05절 함수 넷을 가져옵니다.
Ch 6 06절 함수 `estimate_cost`도 함께 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄에 가져온 이름 다섯이 보입니다.
도구 파일에서 가져온 함수 여섯은 셀의 `from order_tools import …` 줄에 적혀 있습니다.
함수 `ask_until_answer`는 05절 값 바꿔 보기의 루프이고, 바퀴 한도까지 도구를 실행하며 다시 묻습니다.

다음 셀은 01~05절과 같은 방법으로 주문 CSV가 있는 프로젝트 맨 위 폴더를 찾습니다.
읽기 도구의 몸통이 이 CSV 파일을 읽습니다."""),
        setup(PATH),
        md("""**결과 읽기** — 출력 줄 `찾은 프로젝트 맨 위: .`은 교재 출력을 프로젝트 맨 위에서 실행했다는 뜻입니다.
교재 출력은 실행 도구에 도구 파일 폴더를 따로 알려 준 실행이라 `.`이 찍혔습니다.
노트북을 `notebooks/` 폴더에서 열면 이 줄에 `../../../..`가 찍힙니다.
셀 안의 안내 글은 실습 폴더 맨 위도 적었지만, 도구 파일을 가져오려면 `notebooks/` 폴더에서 열어야 합니다.

## 2. 키와 모델 준비

모델은 04·05절과 같은 `gpt-5.4-mini`이고, 과정의 같은 설정으로 부릅니다."""),
    ] + key_and_model_cells(
        "openai:gpt-5.4-mini",
        "temperature 값을 0으로 두어도, 모델이 고르는 도구가 매번 같다고 보장하지는 않습니다.",
    ) + [
        md("""## 3. 읽기 도구와 도구 오류

이 절의 도구는 둘이고, 하나는 주문을 찾아 읽기만 합니다.
자료를 읽기만 하고 아무것도 바꾸지 않는 도구를 읽기 도구라고 부릅니다.
식당으로 치면 열린 창으로 음식을 내어 주기만 하는 일입니다.

다음 셀은 05절의 한 건 도구를 고쳐 읽기 도구로 만듭니다.
설명은 03절 자세한 판과 같고, 넷째 문장 끝만 「없으면 오류를 냅니다」로 바꿨습니다.
찾지 못하면 None 대신 오류를 내고, 오류 이름으로 `ToolException`을 씁니다.
Ch 16 01절에서 `raise`로 오류를 일부러 낸 것과 같은 모양입니다."""),
        code(DEF_READ),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
도구 이름은 05절과 같은 `get_order_by_id`입니다.
몸통은 도구 파일의 `find_order`로 주문을 찾고, 찾지 못하면 `raise` 줄로 오류를 냅니다.
오류 글에는 무엇이 잘못됐는지와 다음에 할 일을 함께 적었습니다.

다음 셀은 있는 주문 O101을 이 도구로 찾습니다.
도구 객체의 속성 `handle_tool_error`의 값도 함께 봅니다."""),
        code(READ_OK),
        md("""**결과 읽기** — 라벨 `찾은 주문:` 뒤 딕셔너리는 주문 O101 한 줄이고, 금액은 `32000`입니다.
출력 줄 `오류 담기 설정(handle_tool_error): False`는 이 속성의 기본값입니다.
이 속성은 도구 오류를 받아 도구 메시지에 담을지 정하고, 이 절에서는 오류 담기 설정이라고 부릅니다.
값이 `False`이면 도구 오류를 받지 않고 그대로 위로 올려 보냅니다.

다음 셀은 없는 주문 O999를 넣어 봅니다.
실행 전에 예상해 봅니다.
설정이 `False`이니 도구 오류가 셀까지 올라올 것입니다.
이 셀만 그 오류를 받아 출력하고, 셀은 끝까지 갑니다."""),
        code(READ_MISSING),
        md("""**결과 읽기** — 출력 줄 `받은 오류: ToolException`처럼 도구 오류가 셀까지 올라왔습니다.
라벨 `오류 글:` 뒤 글은 몸통의 `raise` 줄에 적은 글 그대로입니다.
도구 오류(ToolException)는 도구가 일을 끝내지 못했다고 알리려고 몸통에서 내는 오류입니다.
식당으로 치면 주방이 재료가 없다고 알리는 일입니다.

오류를 받지 않는 실제 프로그램이라면 여기서 멈춥니다.
모델이 부른 도구가 이렇게 멈추면, 모델은 무엇이 잘못됐는지 듣지 못합니다.
그 장면은 6절에서 모델과 함께 봅니다.

## 4. 쓰기 도구와 사람 확인

둘째 도구는 주문 취소 요청을 등록합니다.
주문 상태처럼 무언가를 바꾸는 도구를 쓰기 도구라고 부릅니다.
Ch 17 02절에서 본 부작용이 있는 도구이고, 식당으로 치면 칼을 넣어 둔 서랍입니다.

다음 셀의 쓰기 도구는 이 절에서 만든 흉내입니다.
몸통은 받은 주문 번호를 딕셔너리에 적어 내놓기만 하고, CSV도 다른 파일도 바꾸지 않습니다.
실제 서비스라면 이 자리에서 주문 상태가 바뀝니다."""),
        code(DEF_WRITE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
도구 이름 `cancel_order`는 하는 일을 뜻하는 동사 cancel을 앞에 두었습니다.
설명은 03절 자세한 판처럼 하는 일·사용 조건·인자·내놓는 값의 네 문장입니다.

다음 셀은 두 도구를 읽기 도구 목록과 쓰기 도구 목록에 따로 담습니다."""),
        code(SPLIT),
        md("""**결과 읽기** — 출력 줄 `읽기 도구: get_order_by_id`와 `쓰기 도구: cancel_order`가 보입니다.
목록마다 도구가 하나씩이지만, 도구가 늘어도 같은 방법으로 나눠 담습니다.

Ch 17 03절 루프는 부작용이 있는 도구 앞에서 멈추고 사람 확인을 받았습니다.
이 절은 사람이 확인하기 전에는 쓰기 도구를 모델에게 아예 알려 주지 않습니다.
다음 셀은 사람 확인 값에 따라 알려 줄 목록을 만드는 함수입니다."""),
        code(DEF_PICK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `pick_tools`는 읽기 도구 목록을 새 목록으로 복사해 먼저 담습니다.
인자 `person_confirmed`가 참일 때만 쓰기 도구 목록을 뒤에 더합니다.
사람 확인 값은 노트북이 정해 넘기고, 모델이 채우는 인자가 아닙니다.

다음 셀은 확인 전과 확인 뒤에 목록에 들어가는 도구 이름을 봅니다.
모델 요청은 없습니다."""),
        code(PICK_TRY),
        md("""**결과 읽기** — 출력 줄 `사람 확인: False | 도구: ['get_order_by_id']`는 확인 전 목록입니다.
출력 줄 `사람 확인: True | 도구: ['get_order_by_id', 'cancel_order']`는 확인 뒤 목록입니다.
같은 두 목록에서 사람 확인 값 하나로 알려 줄 도구가 달라졌습니다.

## 5. 도구 찾기 표와 명세 이름

다음 셀은 도구 목록으로 도구 찾기 표를 만드는 함수입니다.
05절 노트북 4절에서 셀로 만든 표를, 이 절은 목록이 여럿이라 함수로 옮겼습니다."""),
        code(DEF_TABLE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `make_tools_table`은 공개 이름을 키, 도구를 값으로 둔 딕셔너리를 내놓습니다.
모델에게 알려 준 목록으로 표를 만들면, 알려 주지 않은 도구는 표에도 없습니다.

다음 셀은 도구를 알려 준 모델이 요청마다 싣는 명세에서 도구 이름만 모으는 함수입니다.
04절에서 본 속성 `kwargs["tools"]`의 명세마다 칸 `function` 안의 `name`을 꺼냅니다."""),
        code(DEF_SPEC),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `spec_names`는 모델에게 실어 보낼 도구 이름을 목록으로 내놓습니다.
요청은 보내지 않고, 모델 객체에 붙은 값만 읽습니다.

## 6. 05절 방식 그대로 보내기 (Before)""", lesson_part="before"),
        md("""먼저 05절 방식 그대로 두 도구를 한 목록으로 모델에게 알려 줍니다.
읽기 도구의 오류 담기 설정도 기본값 `False` 그대로 둡니다.
질문은 둘이고, 하나는 O101 주문 취소, 하나는 없는 주문 O999의 금액입니다.

다음 셀은 한 목록을 알려 준 모델을 만들고, 실어 보낼 도구 이름을 봅니다.
04절처럼 인자 `parallel_tool_calls=False`로 한 응답에 도구 호출 요청을 하나까지만 받습니다.
흐름을 한 건씩 읽기 위해서입니다.""", lesson_part="before"),
        code(BEFORE_BIND, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `실어 보낼 도구 이름: ['get_order_by_id', 'cancel_order']`입니다.
쓰기 도구의 명세도 요청마다 함께 실립니다.
그래서 모델은 사람이 확인하지 않았어도 쓰기 도구를 고를 수 있습니다.

다음 셀은 O101 주문을 취소해 달라는 질문을 한 번 보냅니다.
첫 응답의 도구 호출 요청만 보고, 도구는 실행하지 않습니다.
실행 전에 예상해 봅니다.
목록에 취소 도구가 있으니, 모델이 그 도구를 요청할 수 있습니다.""", lesson_part="before"),
        code(BEFORE_WRITE, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `응답 글의 길이: 0`은 모델이 글로 답하지 않고 도구 호출 요청을 적었다는 뜻입니다.
라벨 `도구 호출 요청:` 뒤 목록이 첫 응답에서 고른 도구입니다.

이번 실행에서는 첫 응답에 쓰기 도구 `cancel_order` 요청이 왔고, 인자는 O101입니다.
이 요청을 05절 함수 `run_tool_calls`에 넘기면 사람 확인 없이 그대로 실행되지만, 이번에는 실행하지 않았습니다.
노트북 밖에서 같은 요청을 11번 보냈을 때는 10번이 이 모양이었습니다.
나머지 1번은 읽기 도구를 먼저 불렀고, 다음 응답에서 쓰기 도구를 요청했습니다.
그래서 이 셀의 결함은 첫 응답의 도구 이름이 아니라, 쓰기 도구가 목록에 있다는 점입니다.

다음 셀은 없는 주문 O999의 금액을 묻고, 05절 함수 `ask_until_answer`로 끝까지 처리해 봅니다.
실행 전에 예상해 봅니다.
읽기 도구가 도구 오류를 내면, 함수 안의 `run_tool_calls`가 그 오류를 받지 않아 흐름이 멈출 것입니다.
이 셀만 그 오류를 받아 출력하고, 메시지 목록에 남은 수를 셉니다.""", lesson_part="before"),
        code(BEFORE_ERROR, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `받은 오류: ToolException`처럼 도구 오류가 함수 밖 셀까지 올라왔습니다.
출력 줄 `메시지 수: 2`는 목록에 질문과 첫 응답만 남았다는 뜻입니다.

05절 함수 `ask_until_answer`는 넘겨받은 목록에 응답을 바로 이어 붙입니다.
그래서 오류로 함수가 끝나지 못해도, `before_messages`에는 셀이 넣은 질문과 그때까지 붙인 첫 응답이 남습니다.
첫 응답은 O999로 읽기 도구를 요청했지만, 그 결과는 도구 메시지가 되지 못했습니다.
오류를 받지 않는 실제 프로그램이라면 여기서 멈추고, 모델은 주문이 없다는 것을 듣지 못합니다.

두 질문 모두 셀은 끝까지 갔지만, 이 프로그램에는 결함이 둘 있습니다.
쓰기 도구가 사람 확인 없이 모델에게 알려졌고, 도구 오류가 흐름을 멈췄습니다.

## 7. 목록을 나누고 오류를 담기 (After)""", lesson_part="after"),
        md("""이제 두 결함을 하나씩 고칩니다.
먼저 읽기 도구의 오류 담기 설정을 `True`로 바꿉니다.
도구를 만드는 `@tool` 줄은 괄호 안에 이 설정을 받지 않습니다.
그래서 만든 도구 객체의 속성에 값을 넣습니다.
식당으로 치면 요리를 못 만들 때 문을 닫지 않고, 재료가 없다는 쪽지를 창으로 내보내는 일입니다.

다음 셀은 설정을 바꾼 뒤, Before에서 멈춘 첫 응답의 요청을 다시 실행합니다.
모델 요청은 없고, 요청을 받아 도구를 실행하는 05절 함수 `run_tool_calls`만 씁니다.""", lesson_part="after"),
        code(SET_HANDLE, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `내놓은 값의 종류: ToolMessage`처럼 이번에는 도구 메시지가 나왔습니다.
출력 줄 `결과 상태(status): error`는 이 도구 메시지가 오류를 담았다는 표시입니다.
라벨 `내용:` 뒤 글은 몸통의 `raise` 줄에 적은 오류 글 그대로입니다.
출력 줄 `호출 ID가 요청 id와 같은가: True`로 짝도 05절처럼 맞습니다.

도구 메시지의 칸 `status`를 이 절에서는 결과 상태라고 부릅니다.
도구가 결과를 내놓으면 `success`, 도구 오류를 담으면 `error`가 적힙니다.
식당으로 치면 창으로 나온 것이 요리인지 쪽지인지 알리는 표시입니다.
이 설정은 `ToolException`만 받고, `ValueError` 같은 다른 오류는 그대로 올라옵니다.
이것은 노트북 밖에서 확인했습니다.

다음 셀은 둘째 결함을 고칩니다.
사람 확인 전이라 `person_confirmed`를 `False`로 두고, 함수 `pick_tools`로 알려 줄 목록을 만듭니다.
도구 찾기 표도 같은 목록으로 만듭니다.""", lesson_part="after"),
        code(AFTER_BIND, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `실어 보낼 도구 이름: ['get_order_by_id']`입니다.
쓰기 도구의 이름과 설명이 요청에 실리지 않고, 도구 찾기 표에도 쓰기 도구가 없습니다.
05절에서 본 것처럼, 모델에게 보이는 도구는 `bind_tools`에 넘긴 목록뿐입니다.

다음 셀은 메시지 목록을 차례로 보며 무엇이 오갔는지 출력하는 함수입니다.
응답이면 도구 호출 요청을, 도구 메시지면 결과 상태와 내용을 출력합니다.""", lesson_part="after"),
        code(DEF_SHOW, lesson_part="after"),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `show_messages`는 메시지마다 종류 이름을 먼저 출력합니다.
최종 답이면 도구 호출 요청이 빈 목록 `[]`으로 찍힙니다.

다음 셀은 6절과 같은 취소 질문을, 읽기 도구만 아는 모델로 끝까지 처리합니다.
실행 전에 예상해 봅니다.
쓰기 도구가 목록에 없으니, 흐름 어디에도 `cancel_order` 요청은 없을 것입니다.""", lesson_part="after"),
        code(AFTER_WRITE, lesson_part="after"),
        md("""**결과 읽기** — 응답 줄은 `AIMessage | 도구 호출 요청: ['get_order_by_id']`와 `AIMessage | 도구 호출 요청: []`입니다.
흐름 어디에도 `cancel_order` 요청이 없고, 모델은 읽기 도구로 주문을 찾은 뒤 글로 답했습니다.
도구 메시지 줄은 `결과 상태: success`이고, 내용은 주문 O101 한 줄입니다.

라벨 줄 `답 글:` 아래가 모델이 적은 최종 답이고, 문장은 실행마다 달라질 수 있습니다.
이번 실행에서는 답 글이 주문 상태를 알려 주었고, 취소했다고 적지는 않았습니다.
모델에게는 취소를 요청할 도구가 알려지지 않았습니다.

다음 셀은 O999 질문을 같은 모델로 끝까지 처리합니다.
이번에는 읽기 도구의 오류 담기 설정이 `True`입니다.
실행 전에 예상해 봅니다.
도구 오류가 결과 상태 `error`인 도구 메시지로 모델에게 가고, 모델이 글로 답할 것입니다.""", lesson_part="after"),
        code(AFTER_ERROR, lesson_part="after"),
        md("""**결과 읽기** — 도구 메시지 줄은 `결과 상태: error`이고, 내용은 몸통에 적은 오류 글입니다.
마지막 응답 줄 `AIMessage | 도구 호출 요청: []`처럼 모델이 도구 없이 글로 답했습니다.
출력 줄 `답 글에 O999가 있는가: True`로, 최종 답이 없는 주문 번호를 적었습니다.
앞의 Before 셀에서는 같은 요청에서 흐름이 멈췄지만, 이번에는 모델이 오류를 듣고 답했습니다.

라벨 줄 `답 글:` 아래 문장은 실행마다 달라질 수 있어, 여기에 옮겨 적지 않습니다.
노트북 밖에서 같은 흐름을 다섯 번 보냈을 때도, 다섯 번 모두 답 글에 O999가 있었습니다.

## 8. 값 바꿔 보기 · 사람이 확인한 뒤

바꿀 값은 `person_confirmed` 하나이고, `False`를 `True`로 바꿉니다.
사람이 취소를 확인했다고 노트북이 기록한 경우입니다.
질문과 도구, 오류 담기 설정은 그대로입니다.

다음 셀은 확인 뒤 목록을 알려 준 모델을 만들고, 실어 보낼 도구 이름을 봅니다.
실행 전에 예상해 봅니다.
4절에서 본 것처럼 쓰기 도구가 목록에 들어갈 것입니다.""", lesson_part="after"),
        code(CONFIRM_BIND, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `실어 보낼 도구 이름: ['get_order_by_id', 'cancel_order']`입니다.
한 목록으로 알려 준 6절과 같은 두 도구가 실리지만, 이번에는 사람 확인 값이 목록을 정했습니다.

다음 셀은 같은 취소 질문을 이 모델로 끝까지 처리합니다.
쓰기 도구는 이 절의 흉내라, 실행돼도 받은 번호만 적어 내놓습니다.
실행 전에 예상해 봅니다.
이번에는 흐름 안에 `cancel_order` 요청이 오고, 프로그램이 그 도구를 실행할 것입니다.""", lesson_part="after"),
        code(CONFIRM_RUN, lesson_part="after"),
        md("""**결과 읽기** — 도구 메시지 줄 `ToolMessage | 결과 상태: success | 내용: {"order_id": "O101", "cancel_requested": true}`가 보입니다.
쓰기 도구가 실행되어, 받은 주문 번호를 적어 내놓았습니다.
마지막 응답 줄은 `AIMessage | 도구 호출 요청: []`으로, 모델이 글로 답했습니다.

이번 실행에서는 첫 응답이 곧바로 `cancel_order`를 요청해, 이 흐름의 모델 요청이 2번이었습니다.
노트북 밖에서 다섯 번 보냈을 때는 한 번, 읽기 도구를 먼저 부른 뒤 쓰기 도구를 요청했습니다.
그때는 모델 요청이 3번이었고, 그때도 쓰기 도구는 실행되었습니다.
답 글 문장은 실행마다 달라질 수 있습니다.

다음 셀은 쓰기 도구가 흉내였는지, 주문 CSV에서 O101의 상태를 다시 읽어 봅니다.""", lesson_part="after"),
        code(CSV_CHECK, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `CSV의 O101 상태: paid`로, 주문 CSV는 그대로입니다.
쓰기 도구가 흉내라 파일을 바꾸지 않았다는 것을 코드로 확인했습니다.
이 값은 CSV 파일에서 정해져서, 셀 끝의 `assert`로도 확인했습니다.
실제 쓰기 도구였다면, 사람 확인 뒤 이 자리에서 주문 상태가 바뀌었을 것입니다.

## 9. 요청 수와 예상 비용

다음 셀은 이 노트북의 모델 응답을 모두 모아, 요청 수와 토큰을 셉니다.
05절 함수 `sum_usage`로 더하고, Ch 6 06절 요금표로 예상 비용을 셉니다.""", lesson_part="after"),
        code(COST, lesson_part="after"),
        md("""**결과 읽기** — 출력 줄 `요금 확인 날짜: 2026-09-17`은 Ch 6 06절 요금표를 확인한 날짜입니다.
라벨 `모두 합친 사용량:` 뒤 딕셔너리의 칸 `requests`가 모델 요청 수입니다.
예상 비용은 요금표로 어림한 값이고 청구 금액이 아닙니다.

이번 실행에서는 칸 `requests`가 8이고, 예상 비용은 0.002376달러였습니다.
새 커널로 한 번 더 실행했을 때는 출력 토큰 합이 달라, 예상 비용도 달랐습니다.
7절 취소 질문의 답 글 길이가 실행마다 달랐기 때문입니다.
값 바꿔 보기 흐름이 요청 3번이 되면, 모두 합친 요청 수는 9가 됩니다.

## 정리

1. 한 목록으로 알려 준 쓰기 도구는 사람 확인 없이 모델이 고를 수 있었고, 도구 오류는 흐름을 멈췄습니다.
2. 오류 담기 설정을 켜자, 도구 오류가 결과 상태 `error`인 도구 메시지로 모델에게 갔습니다.
3. 사람 확인 값이 알려 줄 목록을 정해, 확인 전에는 쓰기 도구의 명세가 요청에 실리지 않았습니다.

07절 실습에서는 이 챕터에서 만든 도구와 함수를 모아, 주문 문의 하나를 처리합니다.""", lesson_part="after"),
    ]


L_CH2_05 = "../../part1/ch02-python/05-파일과-예외.html"
L_CH16_01 = "../../part4/ch16-guardrails/01-입출력-출처-검증.html"
L_CH17_02 = "../ch17-agent-overview/02-워크플로우가-충분한-조건.html"
L_CH17_03 = "../ch17-agent-overview/03-모델-도구-루프와-정지-조건.html"
L_CH20_02 = "../ch20-tool-node/02-도구-오류와-ToolMessage.html"
L03 = "03-좋은-도구-이름과-설명.html"
L04 = "04-설명만으로-도구-선택하기.html"
L05 = "05-bind_tools와-병렬-호출.html"
L_CH6 = "../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html"

B6_STABLE = "새 커널로 두 번 실행했을 때 명세 이름과 도구 오류, 결과 상태, 마지막 응답의 요청 0건은 두 번 모두 같았습니다."
LOOK_B6 = "노트북 6절 출력 <code>실어 보낼 도구 이름: ['get_order_by_id', 'cancel_order']</code>와 <code>메시지 수: 2</code>로 Before의 두 결함을 봅니다. 노트북 7절 출력 <code>결과 상태(status): error</code>와 <code>실어 보낼 도구 이름: ['get_order_by_id']</code>로 After를 봅니다. 교재 출력에서는 9절의 모델 요청이 8번, 예상 비용이 0.002376달러였습니다. 이 비용은 답 글 길이에 따라 실행마다 달라집니다."


def src_html() -> str:
    return """<!--meta: 강의 1h | 실습 1h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 5 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>도구 몸통에서 도구 오류(<code>ToolException</code>)를 내고, 오류 담기 설정으로 도구 메시지에 담을 수 있습니다.</li>
<li>결과 상태가 <code>error</code>인 도구 메시지를 모델에게 보내, 모델이 도구 없이 답하는 흐름을 확인할 수 있습니다.</li>
<li>사람 확인 값으로 알려 줄 도구 목록을 나눠, 확인 전에는 쓰기 도구를 모델에게 알리지 않을 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>05절의 도구는 있는 주문만 찾았고, 주문을 읽기만 했습니다. 실제 도구는 일을 끝내지 못할 때가 있습니다. 없는 주문 번호를 받으면 찾을 주문이 없습니다. 이때 프로그램이 멈추면, 모델은 무엇이 잘못됐는지 듣지 못하고 답도 적지 못합니다.</p><p>도구 가운데에는 무언가를 바꾸는 도구도 있습니다. 주문 취소처럼 한 번 실행하면 되돌리기 어려운 일입니다. 모델은 알려 준 도구라면 무엇이든 고를 수 있습니다. 그래서 그런 도구는 사람이 확인하기 전에는 모델에게 알려 주지 않는 편이 안전합니다.</p><p>제목의 「오류」는 도구가 일을 끝내지 못한 경우입니다. 「읽기 쓰기 분리」는 읽기만 하는 도구와 무언가를 바꾸는 도구를 나눠 알려 주는 일입니다. <a href=\"""" + L_CH20_02 + """\">Ch 20 02절</a>에서는 <code>ToolNode</code>가 도구를 실행하며 도구 오류를 다룹니다. 그 전에 도구 하나와 도구 목록에서 이 일을 먼저 해 봅니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L05 + """\">05절</a>은 모델이 적어 보낸 도구 호출 요청을 프로그램이 실행하고, 도구 메시지를 모델에게 보냈습니다. 함수 <code>run_tool_calls</code>·<code>ask_until_answer</code>·<code>sum_usage</code>는 그 절에서 도구 파일에 옮긴 것을 가져옵니다. 05절은 도구가 오류를 내는 경우를 보지 않았습니다. 이 절은 그 경우에 두 함수가 어떻게 되는지부터 봅니다.</p><p><a href=\"""" + L03 + """\">03절</a>의 몸통 함수 <code>find_order</code>는 없는 주문에 None을 내놓았습니다. 이 절의 읽기 도구는 None 대신 도구 오류를 냅니다. <a href=\"""" + L_CH16_01 + """\">Ch 16 01절</a>에서 <code>raise</code>로 오류를 일부러 낸 것과 같은 모양이고, 오류 이름만 LangChain의 <code>ToolException</code>입니다. 오류는 <a href=\"""" + L_CH2_05 + """\">Ch 2 05절</a>처럼 <code>try/except 오류이름 as error</code>로 그 셀에서만 받습니다.</p><p><a href=\"""" + L_CH17_02 + """\">Ch 17 02절</a>은 프로그램 바깥의 상태를 바꾸는 동작을 부작용이라고 불렀습니다. <a href=\"""" + L_CH17_03 + """\">Ch 17 03절</a> 루프는 부작용이 있는 도구 앞에서 멈추고 사람 확인을 받았습니다. 이 절은 확인 전에는 그런 도구를 모델에게 아예 알려 주지 않는 방법을 봅니다. <a href=\"""" + L04 + """\">04절</a>과 05절에서 본 것처럼, 모델에게 보이는 도구는 <code>bind_tools</code>에 넘긴 목록뿐입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절부터 이어 온 식당을 다시 떠올립니다. 창은 열려 있고, 주방은 손님이 주문한 요리를 창으로 내어 줍니다. 창 아래쪽 카운터에는 칼을 넣어 둔 서랍이 있고, 걸쇠를 걸어 닫아 두었습니다. 주인이 확인한 뒤에만 걸쇠를 풉니다.</p><p>열린 창은 읽기 도구이고, 걸쇠를 건 서랍은 쓰기 도구입니다. 서랍을 여는 것은 손님인 모델이 아니라, 사람 확인을 기록한 프로그램입니다. 재료가 없어 요리를 못 만들면, 주방은 문을 닫지 않고 재료가 없다는 쪽지를 창으로 내보냅니다. 이 쪽지가 결과 상태가 오류인 도구 메시지입니다.</p>
{{img:""" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + """}}
<p class="look"><b>그림 읽기</b> — """ + ILLU_READ + """</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>읽기 도구</td><td>자료를 찾아 읽기만 하고 아무것도 바꾸지 않는 도구입니다. 열린 창으로 음식을 내어 주는 일과 같습니다.</td></tr><tr><td>쓰기 도구</td><td>주문 상태처럼 무언가를 바꾸는 도구이고, 부작용이 있습니다. 걸쇠를 걸어 둔 칼 서랍과 같습니다.</td></tr><tr><td>도구 오류(ToolException)</td><td>도구가 일을 끝내지 못했다고 알리려고 몸통에서 내는 오류입니다. 주방이 재료가 없다고 알리는 일과 같습니다.</td></tr><tr><td>오류 담기 설정(handle_tool_error)</td><td>도구 오류를 받아 도구 메시지에 담을지 정하는 도구의 속성이고, 기본값은 <code>False</code>입니다. 문을 닫는 대신 쪽지를 내보낼지 정하는 일과 같습니다.</td></tr><tr><td>결과 상태(status)</td><td>도구 메시지의 칸이고, 결과면 <code>success</code>, 도구 오류면 <code>error</code>가 적힙니다. 창으로 나온 것이 요리인지 쪽지인지 알리는 표시와 같습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 읽기 도구는 <code>get_order_by_id</code>이고, 쓰기 도구는 흉내로 만든 <code>cancel_order</code>입니다. 도구 오류는 몸통의 <code>raise ToolException(…)</code> 줄에서 납니다. 오류 담기 설정은 <code>get_order_by_id.handle_tool_error = True</code> 한 줄로 켭니다. 결과 상태는 도구 메시지의 칸 <code>status</code>입니다.</p>
{{mermaid:""" + FIG1 + "|" + FIG1_ALT + "|" + FIG1_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG1_READ) + """</p>
<h3>사람 확인 값이 목록을 정합니다</h3><p>모델은 알려 준 도구 가운데서 고릅니다. 그래서 쓰기 도구를 막는 맨 앞자리는 알려 줄 목록입니다. 이 절의 함수 <code>pick_tools</code>는 사람 확인 값이 참일 때만 쓰기 도구를 목록에 더합니다. 사람 확인 값은 노트북이 정하고, 모델이 채우는 인자로 받지 않습니다. 모델이 적은 글은 사람이 확인했다는 증거가 될 수 없기 때문입니다.</p>
<h3>다른 상황에 적용</h3><p>메일 도우미라면 메일 찾기는 읽기 도구이고, 메일 보내기는 쓰기 도구입니다. 사용자가 받는 사람과 본문을 확인하기 전에는 찾기 도구만 알려 줍니다. 찾을 메일이 없으면 찾기 도구가 도구 오류를 내고, 모델은 그 글을 읽고 다른 검색어를 물을 수 있습니다.</p>
<h3>비교와 경계</h3><p>오류 담기 설정은 <code>ToolException</code>만 도구 메시지로 바꿉니다. <code>ValueError</code> 같은 다른 오류는 설정을 켜도 그대로 올라옵니다. 이 절의 사람 확인 값은 참과 거짓 하나라서, 어느 주문을 확인했는지는 가리지 않습니다. 확인한 주문 번호만 받게 하는 방법은 이 절에서 다루지 않았습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 읽기 도구를 만들고, 있는 주문과 없는 주문을 넣어 봅니다. 없는 주문에서는 도구 오류가 셀까지 올라옵니다. 그다음 쓰기 도구를 흉내로 만들고, 두 도구를 읽기 목록과 쓰기 목록에 나눠 담습니다. 사람 확인 값에 따라 알려 줄 목록을 만드는 함수와, 도구 찾기 표·명세 이름을 다룰 함수도 만듭니다.</p><p>예시 부분은 모델을 부르지 않습니다. 모델은 6절부터 <code>gpt-5.4-mini</code>를 temperature 0과 추론 끔(<code>reasoning_effort="none"</code>)으로 부릅니다. 모델 요청은 모두 8~9번입니다.</p>
{{notebook:""" + SLUG + """|example}}
<p class="look"><b>확인할 점</b> — 노트북 3절 출력 <code>오류 담기 설정(handle_tool_error): False</code>로 설정의 기본값을 봅니다. 같은 절 출력 <code>받은 오류: ToolException</code>으로 도구 오류가 셀까지 올라왔는지 봅니다. 노트북 4절 출력 <code>사람 확인: False | 도구: ['get_order_by_id']</code>로 확인 전 목록을 봅니다.</p>
{{mermaid:""" + FIG2 + "|" + FIG2_ALT + "|" + FIG2_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG2_READ) + """</p>
<h2 id="b6"><span class="no">6</span>실패 확인</h2><p>아래 Before 셀은 05절 방식 그대로 두 도구를 한 목록으로 알려 주고, 오류 담기 설정도 기본값으로 둡니다. 이어지는 After 셀은 오류 담기 설정을 켜고, 사람 확인 전 목록으로 같은 두 질문을 보냅니다. 마지막 값 바꿔 보기는 사람 확인 값만 바꿉니다.</p>
{{notebook:""" + SLUG + """|failure}}
{{mermaid:""" + FIG3 + "|" + FIG3_ALT + "|" + FIG3_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG3_READ) + """</p>
<p>한 목록으로 알려 준 Before에서는 실어 보낼 명세에 쓰기 도구 <code>cancel_order</code>도 들어갔습니다. 그래서 모델은 사람이 확인하지 않았어도 쓰기 도구를 고를 수 있었습니다. 없는 주문 O999를 묻자 읽기 도구가 도구 오류를 냈고, 오류가 루프 밖까지 올라와 흐름이 멈췄습니다.</p><p>메시지 목록에는 질문과 첫 응답만 남아, 모델은 주문이 없다는 것을 듣지 못했습니다. 05절 함수 <code>ask_until_answer</code>는 넘겨받은 목록에 응답을 바로 이어 붙입니다. 그래서 함수가 오류로 끝나지 못해도 그때까지 붙인 첫 응답이 목록에 남았습니다.</p><p>고친 After에서는 사람 확인 전 목록에 읽기 도구만 들어가, 실어 보낼 명세가 하나였습니다. 같은 취소 질문의 흐름에는 쓰기 도구 요청이 없었습니다. 오류 담기 설정을 켜자 O999 요청의 도구 오류가 결과 상태 <code>error</code>인 도구 메시지가 되었습니다. 모델은 그 메시지를 받고 도구 없이 최종 답을 적었습니다. """ + B6_STABLE + """</p>
<p>값 바꿔 보기는 사람 확인 값만 <code>True</code>로 바꿉니다. 목록에 쓰기 도구가 들어가자, 흐름 안에 <code>cancel_order</code> 요청이 오고 프로그램이 그 도구를 실행했습니다. 쓰기 도구는 흉내라 주문 CSV의 O101 상태는 <code>paid</code> 그대로였습니다.</p>
{{mermaid:""" + FIG4 + "|" + FIG4_ALT + "|" + FIG4_CAP + """}}
<p class="look"><b>도식 읽기</b> — """ + html_text(FIG4_READ) + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>노트북을 실행하기 전에 노트북 밖에서 질문마다 다섯 번씩 보냈습니다. 고친 판(After)의 두 흐름과 값 바꿔 보기에서, 마지막 응답에 도구 호출 요청이 없었다는 것은 다섯 번 모두 같았습니다.</li><li>두 도구를 한 목록으로 알려 주고 취소 질문을 보낸 첫 요청은 노트북 밖에서 모두 11번 보냈습니다. 첫 응답이 쓰기 도구 <code>cancel_order</code>인 것이 10번, 읽기 도구를 먼저 부른 것이 1번이었습니다. 그 1번도 다음 응답에서 쓰기 도구를 요청했습니다.</li><li>그래서 Before의 결함은 쓰기 도구의 명세가 요청에 실린다는 코드 쪽 사실로 적었습니다. 첫 응답의 도구 이름은 실행마다 달라질 수 있습니다.</li><li>가능 여부만 묻는 질문 「O101 주문을 취소할 수 있는지 알려 줘.」도 노트북 밖에서 다섯 번 보냈습니다. 다섯 번 모두 첫 응답이 읽기 도구였습니다. 첫 응답만 봤고, 그 뒤 흐름은 보지 않았습니다.</li><li>질문 둘과 도구 둘은 흐름을 보여 주려고 이 절에서 정한 예입니다. 인자 <code>parallel_tool_calls=False</code>도 흐름을 한 건씩 읽으려고 정했습니다.</li><li>쓰기 도구 <code>cancel_order</code>는 이 절의 흉내입니다. 받은 번호만 적어 내놓고, 주문 CSV와 다른 파일을 바꾸지 않습니다.</li><li>모델이 정하는 값, 곧 도구 호출 요청과 답 글에는 <code>assert</code>를 걸지 않았습니다. 준비 셀 둘 밖의 <code>assert</code>는 CSV에서 정해지는 O101 상태에만 걸었습니다.</li><li>도구를 만드는 <code>@tool</code> 줄에 오류 담기 설정을 넣으면 <code>TypeError</code>가 납니다. 설치한 langchain 1.4.0으로 노트북 밖에서 확인했고, 그래서 도구 객체의 속성에 값을 넣었습니다.</li><li>오류 담기 설정을 켜도 <code>ValueError</code> 같은 다른 오류는 그대로 올라옵니다. 설치한 langchain-core 1.6.2로 노트북 밖에서 확인했고, 노트북에서는 실행하지 않았습니다.</li><li>사람 확인 값은 참과 거짓 하나라, 확인하지 않은 다른 주문의 취소 요청은 막지 못합니다. 쓰기 도구 안에서 주문 번호를 다시 검사하는 방법은 다루지 않았습니다.</li><li>모델 서비스 쪽 오류, 곧 요청 한도 초과·서버 오류·시간 제한은 이 절에서 다루지 않았습니다. 이 절의 오류는 도구 안에서 낸 도구 오류뿐입니다.</li><li>답 글은 모델이 적은 문장이라 실행마다 달라질 수 있습니다. 결론에는 도구 호출 요청의 이름과 결과 상태처럼 코드로 센 표지만 썼습니다.</li><li>예상 비용은 2026-09-17 요금표로 어림한 값이고 청구 금액이 아닙니다. 걸린 시간은 재지 않았습니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>한 목록으로 알려 준 쓰기 도구는 사람 확인 없이 모델이 고를 수 있었고, 도구 오류는 흐름을 멈췄습니다.</li><li>오류 담기 설정을 켜자, 도구 오류가 결과 상태 <code>error</code>인 도구 메시지로 모델에게 갔습니다.</li><li>사람 확인 값이 알려 줄 목록을 정해, 확인 전에는 쓰기 도구의 명세가 요청에 실리지 않았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 07절 실습에서는 이 챕터에서 만든 도구와 함수를 모아, 주문 문의 하나를 처리합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. Before에서 없는 주문 O999를 물었을 때 흐름은 어떻게 되었고, 그것이 왜 결함인가요?</p><p class="quiz-a">도구 오류가 함수 <code>ask_until_answer</code> 밖으로 올라와 흐름이 멈췄고, 메시지 목록에는 질문과 첫 응답만 남았습니다. 모델은 주문이 없다는 것을 듣지 못해 답을 적지 못합니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">2. 오류 담기 설정을 켜면 도구 오류는 무엇이 되나요?</p><p class="quiz-a">결과 상태가 <code>error</code>인 도구 메시지가 됩니다. 내용은 몸통에 적은 오류 글이고, 호출 ID는 요청의 <code>id</code>와 같습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">3. 사람 확인 전에 모델이 쓰기 도구를 고르지 못하게 한 방법은 무엇인가요?</p><p class="quiz-a">함수 <code>pick_tools</code>가 확인 전에는 쓰기 도구를 목록에 넣지 않았습니다. 명세에 읽기 도구 하나만 실려, 모델은 쓰기 도구를 알 수 없었습니다. 틀렸다면 본문 4 「핵심 개념」의 「사람 확인 값이 목록을 정합니다」와 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">4. 사람 확인을 모델이 채우는 인자로 받지 않은 까닭은 무엇인가요?</p><p class="quiz-a">모델이 적은 글은 사람이 확인했다는 증거가 될 수 없기 때문입니다. 그래서 확인 값은 노트북이 정하고, 그 값이 알려 줄 목록을 정합니다. 틀렸다면 본문 4 「핵심 개념」을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langchain/tools">LangChain Tools</a></div>확인 2026-09-24 · 권한에 따라 모델에게 넘길 도구를 거르는 예가 있고, 보는 사람에게는 읽기 도구만 줍니다. 도구 오류를 도구 메시지로 바꾸는 예도 있습니다. 두 예 모두 미들웨어를 쓰고, 이 절은 미들웨어 없이 <code>bind_tools</code> 앞에서 목록을 고릅니다.</li><li>langchain-core 1.6.2 소스 <code>tools/base.py</code> — 속성 <code>handle_tool_error</code>의 기본값은 <code>False</code>입니다(527행).</li><li>langchain-core 1.6.2 소스 <code>tools/base.py</code>(1121~1126행) — 설정이 참이면 도구 오류의 글을 내용으로 담습니다. 결과 상태는 <code>error</code>로 둡니다.</li><li>langchain-core 1.6.2 소스 <code>tools/base.py</code> — 그 밖의 오류는 설정과 상관없이 다시 올립니다(1127행).</li><li>05절 — 도구 실행과 도구 메시지, 함수 <code>ask_until_answer</code>.</li><li>03절 — 몸통 함수 <code>find_order</code>와 자세한 판 설명.</li><li>Ch 16 01절 — <code>raise</code>로 오류 내기.</li><li>Ch 17 02·03절 — 부작용과 사람 확인.</li><li><a href=\"""" + L_CH6 + """\">Ch 6 06절</a> — 요금표와 예상 비용.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    # 자리 찾기 셀은 01~05절과 글자까지 같다
    assert PATH == author_03.PATH
    # 읽기 도구 설명은 03절 자세한 판에서 넷째 문장 끝만 다르다
    assert READ_DOC.rsplit(", ", 1)[0] == author_03.GOOD_GET_DOC.rsplit(", ", 1)[0]
    if os.environ.get("AUTHOR06_NB_ONLY") != "1":
        print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "06", SLUG, "paired", cells())
        print("wrote", path)
