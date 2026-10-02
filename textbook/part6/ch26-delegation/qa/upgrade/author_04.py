"""Ch 26 04절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 -B author_04.py            → 도구 파일(01절 판이거나 04절 판일 때만) + 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_04.py --src-only → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_04.py --tools-copy DIR → 04절 판 도구 파일만 DIR에 쓴다(새 커널 사본 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**.
슬러그 `04-호출-수-비용-종료-조건-비교` 그대로(챕터 리드 결정 7). 제목의 「종료 조건」은 제목에 두고 본문 첫 자리에서 「정지 조건(Ch 17)과 완료 조건」으로 풂.

## 결정 1 — R1: 같은 문의·같은 전문 에이전트로 세 구조를 한 번씩 (챕터 리드 결정, 03 인계 §03 → §04)

실제 모델(nbkit.key_and_model_cells("openai:gpt-5.4-mini") — temperature=0·reasoning_effort="none", 키는 루트 .env에서만).
문의 = 03절 두 분야 문의 그대로. 전문 에이전트 셋 desk_agents = 03절 5절 셀과 같은 코드를 세 구조가 함께 씀.
서브에이전트 = 중앙 에이전트 + 분야 이름을 받는 도구 하나 ask_desk_agent(공식 Subagents 문서의 single dispatch tool 모양 — 01절은 담당마다 도구 하나).
핸드오프 = 안내 담당 front_desk(넘기기 도구 transfer_to_desk 하나, 02절 넘기기 도구 모양에 분야 이름 인자) + 분야 노드 셋(desk_agents 그대로).
라우터 = 03절 5~6절 그래프 그대로(send_to_desks는 도구 파일로 옮김, 나머지 노드는 노트북에 다시 적고 author_03 셀과 문자열 대조).
세 구조의 첫 에이전트는 담당 설명 글 desk_guide(03절 분류 글의 가운데 두 문장)를 함께 씀. 모든 실행에 실행 한도 10.
결론 = 구조가 정하는 요청 수 셈(01~03이 정함)과 이번 판단에서의 값, 끝난 까닭, 완료 조건. 토큰·예상 비용은 둘째 단락·b6 표·b7에만, 순위 없음.

## 결정 2 — 핸드오프는 실제로 난 서비스 오류를 받아 출력 (04-probe.md §0-2)

흔들림 확인 P2 첫 판 5/5: 안내 담당이 한 응답에 넘기기 요청 둘 → 도구 실행 노드가 첫 넘기기만 바깥에 적용(부모행 Command는 Send 목록만 합침)
→ 짝 없는 도구 요청이 받은 담당의 모델 요청에 실려 서비스가 400으로 거절. 입력은 바꾸지 않고(결과를 고르지 않음), 실제 조건의 실패 장면으로 둠.
바깥 그래프에만 InMemorySaver를 붙여 get_state로 멈추기 전 체크포인트를 읽음(Ch 23 01절). 받는 오류는 langchain_core.exceptions.ModelInvalidRequestError.
어느 넘기기가 적용되는지(담당 칸)는 P2b에서 loan 3·facility 2로 갈려 흔들리는 값 — 둘째 단락에만.

## 결정 3 — 종료 조건 장면 (챕터 리드 결정)

① 모델 없는 핑퐁 그래프 + {"recursion_limit": 4} → GraphRecursionError(실행 한도, Ch 20 03 — 요청 0)
② 3절 중앙 에이전트에 ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")(호출 한도, Ch 22 04) → 첫 요청 뒤 도구(담당 둘)는 실행되고 둘째 요청 전에 끝남
③ 완료 조건 is_complete(모인 분야, 필요한 분야, 마지막 답 있음) — 서브에이전트 쪽 완료 조건을 문장으로도 적음(Ch 27 03·06 b3가 참이 되게)
④ 03절 빈 분류는 가리키기만. 「한도로 끝남 ≠ 일이 끝남」.

## 결정 4 — 도구 파일에 함수 넷 더함 (규격 §2-7 3번, 챕터 리드 결정 5)

01절 message_kinds·usage_with_specialists, 02절 writer_names, 03절 send_to_desks(가져오기 줄 `from langgraph.types import Send`를 머리 설명 뒤에 둠).
모두 노트북 전역 이름을 읽지 않아 셀 글 그대로 옮김(check_tools()가 문자열·AST 대조). 쓰기 가드: 파일이 01절 판이면 04절 판으로 바꾸고,
04절 판이면 그대로, strip_later_imports 뒤 04절 판으로 시작하는 뒤 절 판이면 건너뜀, 셋 다 아니면 assert로 멈춤.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`isinstance`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·변수 힌트·대입 풀기·별표 풀기·`getattr`·`join`·
`while`·세미콜론·클래스(상태 형식·양식 클래스 밖). `try`는 오류를 받는 두 셀(핸드오프 실행·핑퐁 실행)만.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(HERE))
import author_01  # noqa: E402  도구 파일 01절 판(TOOLS)·본문 도우미·01절 셀
import author_02  # noqa: E402  02절 셀(writer_names·TeamState·넘기기 도구)
import author_03  # noqa: E402  03절 셀(전문 에이전트·라우터)
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch26-delegation/notebooks"
FIGS = ROOT / "textbook/part6/ch26-delegation/figures"
SLUG = "04-호출-수-비용-종료-조건-비교"
TITLE_TEXT = "호출 수·비용·종료 조건 비교"
SRC = ROOT / "textbook/part6/ch26-delegation/_src" / (SLUG + ".html")
TOOLS_PATH = author_01.TOOLS_PATH
html_text = author_01.html_text
table_html = author_01.table_html
mermaid_block = author_01.mermaid_block
placeholder = author_01.placeholder


# ---------------------------------------------------------------- 도구 파일 04절 판
TOOLS_IMPORT = "# 03절 함수 send_to_desks가 만드는 객체 Send(Ch 13 05절)를 가져옵니다\nfrom langgraph.types import Send\n"
NEW_BLOCKS = [
    ("message_kinds", "Ch 26 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다", author_01.DEF_KINDS),
    ("usage_with_specialists", "Ch 26 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다", author_01.DEF_USAGE),
    ("writer_names", "Ch 26 02절에서 배웠습니다 — 02절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다", author_02.WRITER_DEF),
    ("send_to_desks", "Ch 26 03절에서 배웠습니다 — 03절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다", author_03.SEND_FN),
]


def tools_04_text() -> str:
    head = author_01.TOOLS_HEAD
    text = head + TOOLS_IMPORT + author_01.TOOLS[len(head):]
    for name, note, cell in NEW_BLOCKS:
        text = text + "\n\n# " + note + "\n" + cell + "\n"
    return text


TOOLS_04 = tools_04_text()


def check_tools() -> None:
    """04절 판 도구 파일이 01절 판으로 시작하고, 더한 함수 넷이 01~03절 노트북 셀과 문자열·AST 모두 같은지 봅니다."""
    author_01.check_tools()
    assert TOOLS_04.startswith(author_01.TOOLS_HEAD)
    assert author_01.strip_later_imports(TOOLS_04).startswith(author_01.TOOLS), "04절 판이 01절 판으로 시작하지 않습니다"
    tree = ast.parse(TOOLS_04)
    names = []
    imports = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
    assert names == ["tool_call_names", "show_messages", "sum_usage", "estimate_cost",
                     "message_kinds", "usage_with_specialists", "writer_names", "send_to_desks"], names
    assert imports == ["from langgraph.types import Send"], imports
    for name, note, cell in NEW_BLOCKS:
        assert ("# " + note + "\n" + cell + "\n") in TOOLS_04, name
        mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        theirs = [ast.dump(n) for n in ast.parse(cell).body if isinstance(n, ast.FunctionDef)]
        assert mine == theirs and len(mine) == 1, name


def write_tools() -> None:
    """도구 파일 쓰기 가드: 01절 판이면 04절 판으로 바꾸고, 04절 판이면 그대로, 뒤 절이 더한 판이면 건너뜁니다."""
    current = ""
    if TOOLS_PATH.is_file():
        current = TOOLS_PATH.read_text(encoding="utf-8")
    if current == TOOLS_04:
        print("same", TOOLS_PATH)
        return
    if current == "" or current == author_01.TOOLS:
        TOOLS_PATH.write_text(TOOLS_04, encoding="utf-8")
        print("wrote", TOOLS_PATH, "(04절 판)")
        return
    later = author_01.strip_later_imports(current)
    assert later.startswith(author_01.strip_later_imports(TOOLS_04)), "도구 파일이 01절 판도 04절 판도 아닙니다"
    print("skip", TOOLS_PATH, "(뒤 절이 함수를 더한 판 — 덮어쓰지 않음)")


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["langchain==1.4.0", "langchain-openai==1.6.0", "langgraph==1.2.11", "pydantic==2.13.5", "python-dotenv==1.2.3"])

IMPORTS = r'''# 상태 형식(Ch 13 01·02절)·오류 이름·체크포인터(Ch 23 01절)·그래프와 Command(Ch 13 06절) 이름을 가져옵니다
import operator
from typing_extensions import Annotated, Literal, TypedDict
from langchain_core.exceptions import ModelInvalidRequestError
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph, add_messages
from langgraph.types import Command
# 양식 클래스(Ch 21 02절)·에이전트와 호출 한도(Ch 21 01절·Ch 22 04절)·모델·메시지·도구 이름을 가져옵니다
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.chat_models import init_chat_model
from langchain.messages import AnyMessage, HumanMessage, ToolMessage
from langchain.tools import ToolRuntime, tool
# 앞 절과 앞 챕터에서 배운 함수 여섯은 도구 파일에서 가져옵니다
from delegation_tools import estimate_cost, message_kinds, send_to_desks, sum_usage, usage_with_specialists, writer_names

print("도구 파일에서 가져온 함수:", "estimate_cost, message_kinds, send_to_desks, sum_usage, usage_with_specialists, writer_names")'''

RULES = r'''# 분야 이름 셋과 세 담당의 교재용 규정 글을 정합니다(대출은 01절, 상호대차는 02절, 시설은 03절 글 그대로)
desk_names = ["loan_desk", "interlibrary_desk", "facility_desk"]
loan_rules = "[교재용 대출·반납 규정] 일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다. 반납 예정일 전에 한 번, 7일 연장할 수 있습니다."
loan_rules = loan_rules + " 예약한 사람이 있는 책은 연장할 수 없습니다. 연체한 일수만큼 새 대출이 제한됩니다."
interlibrary_rules = "[교재용 상호대차 규정] 다른 도서관의 책은 자료실 창구에서 상호대차로 신청합니다."
interlibrary_rules = interlibrary_rules + " 신청한 책은 보통 3~5일 뒤에 도착합니다."
interlibrary_rules = interlibrary_rules + " 책이 도착하면 문자로 알리고, 7일 안에 찾아가야 합니다."
facility_rules = "[교재용 시설 규정] 자료실은 평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다."
print("분야 이름:", desk_names)'''

AGENTS = author_03.AGENTS

ASK_TOOL = r'''# 분야 이름과 넘길 글을 받아 그 분야 담당에게 맡기고, 담당의 마지막 답 글을 내놓는 도구 하나입니다
@tool
def ask_desk_agent(desk: str, question: str):
    """문의 가운데 한 분야 부분을 그 분야 담당(loan_desk·interlibrary_desk·facility_desk)에게 맡기고, 담당의 답 글을 받습니다."""
    # 분야 이름으로 담당을 찾고, 담당은 넘긴 글 한 줄만 든 새 메시지 목록으로 일합니다(01절 도구와 같은 모양)
    agent = desk_agents[desk]
    inner_input = {"messages": [HumanMessage(content=question)]}
    inner_result = agent.invoke(inner_input)
    specialist_runs.append(inner_result["messages"])
    return inner_result["messages"][-1].text'''

CENTRAL = r'''# 세 구조가 함께 쓸 담당 설명 글을 정하고, 도구 하나를 가진 중앙 에이전트를 만듭니다(코드 이름 supervisor)
desk_guide = " loan_desk는 대출·반납·연장·연체, interlibrary_desk는 다른 도서관 책을 빌려 오는 상호대차를 맡습니다."
desk_guide = desk_guide + " facility_desk는 자료실 운영 시간과 시설을 맡습니다."
central_text = "도서관 자료실 문의 창구의 안내 도우미입니다. 규정을 묻는 부분은 직접 답하지 말고 ask_desk_agent 도구로 담당에게 맡기세요."
central_text = central_text + desk_guide + " 담당이 준 답을 바탕으로 두 문장의 한국어로 답하세요."
supervisor = create_agent(model, tools=[ask_desk_agent], system_prompt=central_text)
print("도구 인자:", list(ask_desk_agent.args))'''

SUB_RUN = r'''# 세 구조에 보낼 문의를 정하고, 기록 목록을 비운 뒤 서브에이전트 구조(중앙 에이전트)를 실행합니다
question_text = "빌린 책을 연장하려면 어떻게 하나요? 토요일 운영 시간도 알려 주세요."
# 모델이 끝없이 도구를 부르면 요청도 끝없이 나가므로, 실행 한도를 작게 줍니다(Ch 20 03절)
limit_config = {"recursion_limit": 10}
specialist_runs = []
sub_input = {"messages": [HumanMessage(content=question_text)]}
sub_result = supervisor.invoke(sub_input, limit_config)
sub_new = sub_result["messages"][1:]
print("이번 실행이 더한 바깥 메시지:", message_kinds(sub_new))
print("전문 에이전트를 부른 횟수:", len(specialist_runs))'''

DEF_ANSWERED = r'''# 기록 목록의 안쪽 목록마다 마지막 응답을 쓴 담당 이름을 보고, 분야 이름 차례로 모아 내놓습니다
def answered_desks(inner_runs, names):
    desks = []
    for desk in names:
        for inner_list in inner_runs:
            if inner_list[-1].name == desk:
                desks.append(desk)
    return desks'''

SUB_CHECK = r'''# 담당 답이 모인 분야와 모델 요청 수를 세고, 마지막 응답이 도구 요청 없는 모델 응답인지 봅니다
sub_desks = answered_desks(specialist_runs, desk_names)
sub_usage = usage_with_specialists(sub_new, specialist_runs)
sub_last = sub_new[-1]
# 모델 요청으로 받은 응답에는 사용량 기록이 있습니다(01절 6절 — 손으로 적은 응답은 None)
sub_final = sub_last.usage_metadata is not None and len(sub_last.tool_calls) == 0
print("담당 답이 모인 분야:", sub_desks)
print("모델 요청 수(중앙 + 전문):", sub_usage["requests"])
print("마지막 응답이 도구 요청 없는 모델 응답인가:", sub_final)'''

TEAM_STATE = r'''# 메시지 칸(Ch 13 04절 메시지 규칙)과 담당 칸을 둔 상태 형식입니다(02절 5절 상태 형식과 같은 칸)
class TeamState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    active_agent: str'''

TRANSFER = r'''# 분야 이름을 받아, 도구 메시지를 함께 담고 바깥 그래프의 그 분야 노드로 대화를 넘기는 도구입니다
@tool
def transfer_to_desk(desk: str, runtime: ToolRuntime):
    """문의를 맡을 담당 한 명(loan_desk·interlibrary_desk·facility_desk)에게 대화를 넘깁니다."""
    # 02절 넘기기 도구와 같은 모양이고, 가는 노드 이름과 담당 칸 값만 인자 desk로 받습니다
    last_message = runtime.state["messages"][-1]
    transfer_message = ToolMessage(content=desk + " 담당에게 넘겼습니다.", tool_call_id=runtime.tool_call_id)
    update = {"active_agent": desk, "messages": [last_message, transfer_message]}
    return Command(goto=desk, update=update, graph=Command.PARENT)'''

TEAM_BUILD = r'''# 넘기기 도구를 가진 안내 담당과, 분야 노드 셋(2절 전문 에이전트 그대로)으로 바깥 그래프를 만듭니다(출력 없음)
front_text = "도서관 자료실 문의 창구의 안내 담당입니다. 문의에 직접 답하지 말고, 맡을 담당 한 명을 골라 transfer_to_desk 도구로 넘기세요."
front_text = front_text + desk_guide
front_agent = create_agent(model, tools=[transfer_to_desk], system_prompt=front_text, name="front_desk")
team_builder = StateGraph(TeamState)
team_builder.add_node("front_desk", front_agent, destinations=("loan_desk", "interlibrary_desk", "facility_desk"))
for desk in desk_names:
    team_builder.add_node(desk, desk_agents[desk])
    team_builder.add_edge(desk, END)
team_builder.add_edge(START, "front_desk")
team_graph = team_builder.compile(checkpointer=InMemorySaver())'''

HAND_RUN = r'''# 같은 문의로 핸드오프 구조를 스레드 hand-1에서 실행합니다(이 셀만 올라온 오류를 받아 출력합니다)
hand_config = {"configurable": {"thread_id": "hand-1"}, "recursion_limit": 10}
hand_input = {"messages": [HumanMessage(content=question_text)], "active_agent": ""}
try:
    team_graph.invoke(hand_input, hand_config)
    print("오류 없이 끝났습니다")
except ModelInvalidRequestError as error:
    print("받은 오류:", type(error).__name__, "| 상태 코드:", error.status_code)
    error_text = error.body["message"]
    print("오류 글 첫 문장:", error_text.split(". ")[0])'''

HAND_STATE = r'''# 스레드의 마지막 체크포인트를 읽어, 저장된 메시지·넘기기 요청 수·담당 칸·모델 요청 수를 봅니다(Ch 23 01절)
hand_state = team_graph.get_state(hand_config)
hand_new = hand_state.values["messages"][1:]
hand_usage = sum_usage(hand_new)
hand_desks = writer_names(hand_new)
hand_final = hand_new[-1].name == hand_state.values["active_agent"]
print("저장된 메시지:", message_kinds(hand_new))
print("안내 담당 응답의 넘기기 요청 수:", len(hand_new[0].tool_calls))
print("담당 칸:", hand_state.values["active_agent"], "| 다음에 실행할 노드:", hand_state.next)
print("모델 요청 수:", hand_usage["requests"])'''

FORM = author_03.FORM

CLASSIFIER = r'''# 03절과 같은 분류 시스템 메시지 글(가운데 두 문장이 담당 설명 글)로, 양식 클래스를 붙인 분류 모델을 만듭니다
classify_text = "도서관 자료실 문의 창구의 안내 도우미입니다. 문의를 읽고 답할 담당을 모두 고르세요."
classify_text = classify_text + desk_guide + " 맡을 담당이 없으면 빈 목록을 내세요."
# include_raw=True를 주면 결과가 딕셔너리가 되고, 키 raw에 모델 응답이 함께 담깁니다(Ch 6 03절)
classifier = model.with_structured_output(DeskChoice, include_raw=True)
print("분류 모델의 종류:", type(classifier).__name__)'''

MODEL_STATE = author_03.MODEL_STATE
CLASSIFY_MODEL = author_03.CLASSIFY_MODEL
ASK_DESK = author_03.ASK_DESK
JOIN = author_03.JOIN
MODEL_BUILD = author_03.MODEL_BUILD

ROUTE_RUN = r'''# 같은 문의로 라우터 구조를 실행하고, 고른 분야와 답 칸 줄 수, 모델 요청 수를 봅니다
route_input = {"question": question_text, "desks": [], "answers": [], "summary": "", "responses": []}
route_result = model_graph.invoke(route_input, limit_config)
route_usage = sum_usage(route_result["responses"])
route_desks = []
for answer in route_result["answers"]:
    route_desks.append(answer["desk"])
route_final = route_result["summary"] != ""
print("모델이 고른 분야:", route_result["desks"])
print("답 칸 줄 수:", len(route_result["answers"]))
print("모델 요청 수:", route_usage["requests"])'''

COMPARE = r'''# 세 구조의 모델 요청 수·토큰과 예상 비용을 한 줄씩 봅니다(2026-09-17 요금표, 100만 토큰당 달러 — Ch 6 06절 함수)
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
structure_usage = {"서브에이전트": sub_usage, "핸드오프": hand_usage, "라우터": route_usage}
print("구조 | 모델 요청 수 | 입력 토큰 | 출력 토큰 | 예상 비용(달러)")
for name in structure_usage:
    usage = structure_usage[name]
    cost = round(estimate_cost(usage, input_rate, cached_input_rate, output_rate), 6)
    print(name, "|", usage["requests"], "|", usage["input_tokens"], "|", usage["output_tokens"], "|", cost)'''

BOUNCE_DEF = r'''# 모델 없이 담당 칸만 보고 상대 담당에게 넘기기만 하는 노드입니다(두 노드가 이 함수 하나를 함께 씀)
def bounce(state):
    if state["active_agent"] == "loan_desk":
        return Command(goto="facility_desk", update={"active_agent": "facility_desk"})
    return Command(goto="loan_desk", update={"active_agent": "loan_desk"})'''

BOUNCE_RUN = r'''# 두 노드가 서로 넘기기만 하는 그래프를 실행 한도 4로 실행합니다(모델 요청 0 — 이 셀만 오류를 받아 출력)
bounce_builder = StateGraph(TeamState)
bounce_builder.add_node("loan_desk", bounce, destinations=("facility_desk",))
bounce_builder.add_node("facility_desk", bounce, destinations=("loan_desk",))
bounce_builder.add_edge(START, "loan_desk")
try:
    bounce_builder.compile().invoke({"messages": [], "active_agent": "loan_desk"}, {"recursion_limit": 4})
except GraphRecursionError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:")
    print(error)'''

LIMIT_RUN = r'''# 3절 중앙 에이전트와 같은 도구·시스템 메시지 글에 호출 한도 1을 붙여, 같은 문의로 실행합니다(Ch 22 04절)
call_limit = ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")
limited_agent = create_agent(model, tools=[ask_desk_agent], system_prompt=central_text, middleware=[call_limit])
specialist_runs = []
limited_result = limited_agent.invoke(sub_input, limit_config)
limited_new = limited_result["messages"][1:]
limited_last = limited_new[-1]
print("이번 실행이 더한 바깥 메시지:", message_kinds(limited_new))
print("전문 에이전트를 부른 횟수:", len(specialist_runs))
print("마지막 응답 글:", limited_last.text)
print("마지막 응답의 사용량:", limited_last.usage_metadata)'''

DONE_DEF = r'''# 완료 조건 함수입니다. 필요한 분야가 모두 모인 분야에 들어 있고 마지막 답도 있으면 True를 내놓습니다
def is_complete(collected, needed, has_final):
    for desk in needed:
        if desk not in collected:
            return False
    return has_final'''

DONE_APPLY = r'''# 네 실행의 완료 조건을 봅니다. 필요한 분야는 문의가 묻는 두 가지(대출 연장, 토요일 운영 시간)입니다
needed_desks = ["loan_desk", "facility_desk"]
limited_desks = answered_desks(specialist_runs, desk_names)
limited_final = limited_last.usage_metadata is not None and len(limited_last.tool_calls) == 0
print("실행 | 완료 조건")
print("서브에이전트 |", is_complete(sub_desks, needed_desks, sub_final))
print("핸드오프 |", is_complete(hand_desks, needed_desks, hand_final))
print("라우터 |", is_complete(route_desks, needed_desks, route_final))
print("호출 한도 1을 붙인 서브에이전트 |", is_complete(limited_desks, needed_desks, limited_final))'''


def check_same_as_probe() -> None:
    """노트북 셀의 규정 글·에이전트·도구·그래프·한도·완료 조건 줄이 흔들림 확인 스크립트(probe04.py)와 같은지, 앞 절 셀과 같은지 봅니다."""
    probe = (HERE / "probe/probe04.py").read_text(encoding="utf-8")
    skip = ("print(", "sub_", "hand_", "route_", "limited_result", "limited_new", "limited_last", "limited_desks", "limited_final",
            "input_rate", "cached_input_rate", "output_rate", "structure_usage", "for name in", "usage = ", "cost = ", "try:",
            "except ", "error_text", "bounce_builder", "specialist_runs = []", "if state[\"active_agent\"]", "return Command(goto=\"",
            "def bounce", "for answer in route_result", "team_graph.invoke", "@tool")
    cells_to_check = [RULES, AGENTS, ASK_TOOL, CENTRAL, SUB_RUN, DEF_ANSWERED, TEAM_STATE, TRANSFER, TEAM_BUILD, CLASSIFIER,
                      FORM, MODEL_STATE, CLASSIFY_MODEL, ASK_DESK, JOIN, MODEL_BUILD, LIMIT_RUN, DONE_DEF, DONE_APPLY]
    for cell in cells_to_check:
        for line in cell.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith(skip):
                continue
            assert stripped in probe, stripped
    # 앞 절 셀과 같은 코드: 전문 에이전트·양식 클래스·상태 형식·노드·그래프는 03절 셀 글자 그대로(위에서 author_03 값을 그대로 씀)
    for mine, theirs in [(AGENTS, author_03.AGENTS), (FORM, author_03.FORM), (MODEL_STATE, author_03.MODEL_STATE),
                         (CLASSIFY_MODEL, author_03.CLASSIFY_MODEL), (ASK_DESK, author_03.ASK_DESK), (JOIN, author_03.JOIN),
                         (MODEL_BUILD, author_03.MODEL_BUILD)]:
        assert mine == theirs
    # 규정 글 줄은 03절 셀과 같고, 분류 시스템 메시지 글은 이어 붙인 결과가 03절 글과 같습니다
    for line in RULES.splitlines()[2:-1]:
        assert line in author_03.RULES, line
    space = {}
    for line in CENTRAL.splitlines():
        if line.startswith("desk_guide = "):
            exec(line, {}, space)
    for line in CLASSIFIER.splitlines():
        if line.startswith("classify_text = "):
            exec(line, {}, space)
    old = {}
    for line in author_03.CLASSIFIER.splitlines():
        if line.startswith("classify_text = "):
            exec(line, {}, old)
    assert space["classify_text"] == old["classify_text"], "분류 시스템 메시지 글이 03절과 다릅니다"
    # 상태 형식 TeamState의 칸 두 줄은 02절 셀과 같습니다
    for line in TEAM_STATE.splitlines()[1:]:
        assert line in author_02.TEAM_STATE, line
    # 01절 도구의 넘긴 글 줄·기록 줄·내놓는 줄과 02절 넘기기 도구의 줄 모양
    for piece in ['inner_input = {"messages": [HumanMessage(content=question)]}', 'specialist_runs.append(inner_result["messages"])',
                  'return inner_result["messages"][-1].text']:
        assert piece in ASK_TOOL and piece in author_01.DEF_TOOL, piece
    for piece in ['last_message = runtime.state["messages"][-1]', 'return Command(goto=desk, update=update, graph=Command.PARENT)']:
        assert piece in TRANSFER, piece
    assert 'last_message = runtime.state["messages"][-1]' in author_02.TRANSFER
    # 호출 한도는 Ch 22 04절과 같은 인자
    assert 'ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")' in LIMIT_RUN
    # 모델 없는 핑퐁 그래프는 흔들림 확인 밖 탐색(e1_bounce.py)과 같은 모양이라 probe에 없습니다
    assert '{"recursion_limit": 4}' in BOUNCE_RUN


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/04-figures.md)
FIG1 = "04-1-세-구조의-요청-셈"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 같은 문의 글 하나 대출 연장과 토요일 운영 시간에서 화살표 셋이 나란한 파란 상자 셋으로 갑니다. 왼쪽 상자에는 서브에이전트, 중앙 에이전트가 도구로 맡기고 답을 받음, 중앙 = 도구를 요청한 응답 수 + 1, 전문 = 부른 횟수라고 적혀 있습니다. 가운데 상자에는 핸드오프, 안내 담당이 넘기기 도구로 넘김, 넘긴 담당 1 + 받은 담당 1이 적혀 있습니다. 오른쪽 상자에는 라우터, 분류 모델이 고르고 Send로 함께 보냄, 분류 1 + 고른 분야 수가 적혀 있습니다. 세 상자에서 화살표가 맨 아래 회색 상자 전문 에이전트 셋 desk_agents 세 구조가 함께 씀 도구 없음으로 모이는 그림"
FIG1_CAP = "세 구조는 같은 문의와 같은 전문 에이전트를 쓰고, 요청 수를 세는 셈만 구조마다 다릅니다."
FIG1_READ = """위에서 아래로 읽습니다.
파란 상자 셋은 우리가 적은 세 구조이고, 상자 아래쪽 줄이 01~03절에서 정한 요청 수 셈입니다.
왼쪽 상자가 노트북 3절, 가운데가 4절, 오른쪽이 5절의 구조입니다.
맨 아래 회색 상자는 세 구조가 함께 쓴 전문 에이전트 셋입니다.
이 그림에는 이번 실행의 요청 수를 넣지 않았습니다."""

FIG2 = "04-2-이번-실행의-요청-차례"
FIG2_ALT = "칸 둘이 나란히 있는 그림입니다. 왼쪽 칸 서브에이전트 이번 실행에는 보라 상자 셋이 위에서 아래로 이어집니다. 중앙 에이전트 요청 한 응답에 도구 요청 둘, loan_desk · facility_desk 전문 에이전트 요청 하나씩, 중앙 에이전트 요청 도구 요청 없는 최종 답입니다. 오른쪽 칸 라우터 이번 실행에는 보라 상자 분류 모델 요청 두 분야를 고름, 보라 상자 loan_desk · facility_desk 전문 에이전트 요청 하나씩, 파란 상자 종합 노드 join_answers 코드라 요청 없음이 이어집니다. 왼쪽 칸 아래 노란 상자에는 모델 요청 수 4 중앙 2 + 전문 2, 오른쪽 칸 아래 노란 상자에는 모델 요청 수 3 분류 1 + 고른 분야 수 2가 적힌 그림"
FIG2_CAP = "이번 실행에서 서브에이전트는 중앙 2번과 담당 2번, 라우터는 분류 1번과 담당 2번 요청했습니다."
FIG2_READ = """왼쪽 칸이 서브에이전트, 오른쪽 칸이 라우터이고, 칸 안은 위에서 아래로 요청 차례입니다.
보라 상자는 실제로 모델 요청을 보낸 자리이고, 파란 상자는 요청이 없는 종합 노드입니다.
담당 둘의 요청은 한 상자로 묶어 그렸습니다.
노란 상자는 노트북 3절과 5절에서 출력한 모델 요청 수입니다.
두 칸의 맡긴 모양과 고른 분야는 흔들림 확인 다섯 번과 두 커널에서 모두 같았습니다."""

FIG3 = "04-3-넘기기-요청-둘과-빠진-도구-메시지"
FIG3_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 보라 상자 안내 담당 front_desk 요청 1 한 응답에 넘기기 요청 둘에서 회색 상자 넘기기 도구 둘이 저마다 바깥 그래프로 가는 Command를 냄 그 가운데 하나만 바깥 그래프에 적용으로 화살표가 갑니다. 다음 노란 상자 체크포인트에 저장된 메시지 AIMessage · ToolMessage 넘기기 요청 수 2 모델 요청 수 1로 이어지고, 회색 상자 받은 담당의 모델 요청 짝 없는 넘기기 요청이 실림을 거쳐, 맨 아래 노란 상자 받은 오류 OpenAIInvalidRequestError 상태 코드 400으로 끝나는 그림"
FIG3_CAP = "안내 담당이 한 응답에 넘기기 요청 둘을 냈지만 도구 메시지는 하나만 남았고, 받은 담당의 요청이 거절되었습니다."
FIG3_READ = """위에서 아래로 실행 차례대로 읽습니다.
보라 상자는 응답을 받은 안내 담당의 모델 요청이고, 노란 상자는 노트북 4절에서 출력한 값과 받은 오류입니다.
회색 상자 둘은 라이브러리와 서비스 쪽에서 일어난 일입니다.
두 넘기기 가운데 어느 쪽이 남는지는 실행마다 달라, 그림에 담당 이름을 넣지 않았습니다."""

FIG4 = "04-4-한도로-멈춘-실행과-완료-조건"
FIG4_ALT = "위에서 아래로 읽는 그림입니다. 맨 위 파란 상자 완료 조건 is_complete 필요한 두 분야의 담당 답이 모였고 마지막 답이 있는가에서 화살표 둘이 나란한 두 칸으로 갑니다. 왼쪽 칸 완료 조건 False에는 노란 상자 핸드오프 받은 담당 요청이 거절됨과 노란 상자 호출 한도 1 담당 답 둘 마지막 응답은 한도 글이 위아래로 있습니다. 오른쪽 칸 완료 조건 True에는 노란 상자 서브에이전트 담당 답 둘 중앙의 최종 답과 노란 상자 라우터 답 칸 두 줄 종합 칸이 위아래로 있습니다. 왼쪽 칸 아래에는 노란 상자 핑퐁 그래프 실행 한도 4 GraphRecursionError 결과 없음이 화살표 없이 놓인 그림"
FIG4_CAP = "완료 조건은 서브에이전트와 라우터에서 True, 핸드오프와 호출 한도를 붙인 실행에서 False였습니다."
FIG4_READ = """맨 위 파란 상자가 노트북 8절의 완료 조건 함수입니다.
왼쪽 칸은 완료 조건이 False였던 실행, 오른쪽 칸은 True였던 실행이고, 노란 상자는 7절과 8절 출력입니다.
왼쪽 칸 아래 상자는 7절 핑퐁 그래프로, 오류로 멈춰 완료 조건을 볼 결과가 없습니다.
호출 한도를 붙인 실행은 담당 답이 모였어도 마지막 응답이 한도 글이라 False입니다."""

ILLU = "04-5-짐이-다-찬-배와-문에-막힌-배"
ILLU_ALT = "흰 바탕에 파란 물길 두 줄이 위아래로 나란히 있고, 그 사이에 회색 돌 띠가 있는 그림입니다. 위 물길에는 오른쪽을 향한 작은 짐배 한 척이 있고, 갑판의 네모 칸 넷에 나무통 넷이 모두 실려 있습니다. 위 물길의 앞쪽은 막힌 것 없이 열려 있습니다. 아래 물길에는 같은 모양 짐배 한 척이 같은 자리에서 오른쪽을 향하고, 나무통 둘만 실려 네모 칸 둘이 비어 있습니다. 그 배의 뱃머리 바로 앞에 닫힌 나무 문이 아래 물길을 가로막고 있습니다. 글자·숫자·사람·손·화살표는 없는 그림"
ILLU_CAP = "짐이 다 찬 배는 앞이 열려 있고, 짐이 덜 찬 배는 닫힌 문 앞에 멈춰 있습니다."
ILLU_READ = "위 물길의 배는 갑판의 네모 칸 넷에 나무통 넷을 모두 실었고, 앞쪽 물길이 열려 있습니다. 아래 물길의 같은 모양 배는 나무통 둘만 실어 칸 둘이 비었고, 뱃머리 앞을 닫힌 나무 문이 막고 있습니다. 갑판의 칸이 필요한 결과이고, 칸이 다 찼는지 보는 것이 완료 조건입니다. 닫힌 문은 실행 한도나 호출 한도처럼 실행을 멈추게 하는 한도입니다. 칸과 나무통의 수는 이 절의 어떤 값과도 짝짓지 않습니다."


# ---------------------------------------------------------------- 노트북 마크다운
TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 같은 문의 하나를 서브에이전트·핸드오프·라우터 세 구조에 보내고, 구조마다 모델 요청 수와 토큰을 셉니다.
2. 실행 한도와 호출 한도로 멈추는 실행을 실제로 만들어, 한도로 끝난 모양을 봅니다.
3. 필요한 결과가 다 모였는지 보는 완료 조건을 코드로 적고, 네 실행에 대어 봅니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 3·4·5·7절에서 모델을 부릅니다.
노트북 밖에서 먼저 본 대로라면 모델 요청은 노트북 한 번에 11번입니다.
4절에서 서비스가 거절하는 요청 하나는 이 수에 넣지 않았습니다.
요금표로 어림한 예상 비용은 0.005달러 아래이고, 청구 금액이 아닙니다.

모델이 맡기는 모양·넘기는 수·고르는 분야와 답 글은 실행마다 달라질 수 있습니다.
걸린 시간은 재지 않았습니다.

읽거나 쓰는 파일은 없고, 4절의 체크포인트는 프로그램 메모리에만 둡니다.
앞 절과 앞 챕터에서 배운 함수 여섯은 도구 파일 `delegation_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 다섯을 설치합니다.
판은 langchain 1.4.0과 langchain-openai 1.6.0입니다.
langgraph 1.2.11과 pydantic 2.13.5, python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~4절과 8절을 읽습니다.
같은 문의로 두 구조를 실행하고, 완료 조건을 적는 자리입니다.
5절은 03절 라우터를 다시 만드는 자리이고, 6~7절은 요청 수 표와 한도 장면입니다.
이 세 절은 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch26-delegation`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def model_cells() -> list[dict]:
    """과정 표준 키·모델 셀(nbkit)에 이 절의 결과 읽기(실행일·문장이 달라질 수 있음)를 붙입니다."""
    cells = key_and_model_cells("openai:gpt-5.4-mini")
    cells[-1] = md("""**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.
이 절에서 만드는 에이전트와 분류 모델이 모두 이 모델 객체 하나를 함께 씁니다.

## 2. 같은 문의, 같은 전문 에이전트

세 구조를 견주려면 같은 일을 시켜야 합니다.
이 절은 03절의 두 분야 문의 하나를 세 구조에 똑같이 보냅니다.
답하는 전문 에이전트도 03절 5절과 같은 셋을 만들어, 세 구조가 함께 씁니다.
먼저 분야 이름 셋과 세 담당의 규정 글을 정합니다.""")
    return cells


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이 절에서는 01~03절의 세 구조에 같은 문의 하나를 보내, 호출 수와 비용과 종료 조건을 견줍니다.
절 제목의 종료 조건은 이 절에서 두 가지로 나눠 봅니다.
하나는 Ch 17 03절의 정지 조건으로, 실행이 멈추는 까닭입니다.
다른 하나는 이 절이 새로 적는 완료 조건으로, 일이 끝났는지 보는 기준입니다.

첫 셀은 패키지 다섯을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langgraph: 1.2.11`과 `pydantic: 2.13.5`가 보입니다.
다섯 판 모두 실습 폴더 잠금과 같은 판이고, 03절과 같은 다섯 패키지입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
실행 한도를 넘을 때 나는 오류 `GraphRecursionError`는 Ch 20 03절에서 썼습니다.
호출 한도 `ModelCallLimitMiddleware`는 Ch 22 04절, 체크포인터 `InMemorySaver`는 Ch 23 01절에서 썼습니다.
오류 이름 `ModelInvalidRequestError`는 이 절에서 처음 쓰고, 뜻은 4절에서 풉니다.

앞 절들은 `Annotated`·`Literal`을 typing에서, `TypedDict`를 typing_extensions에서 가져왔습니다.
패키지 typing_extensions는 typing과 같은 이름도 함께 내놓아, 이 절은 한 줄로 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: estimate_cost, message_kinds, send_to_desks, sum_usage, usage_with_specialists, writer_names`가 보입니다.
이 가운데 둘은 앞 챕터 함수이고, 넷은 01~03절에서 처음 가르친 함수입니다.

01절의 `message_kinds`·`usage_with_specialists`는 이 절부터 도구 파일에서 가져옵니다.
02절의 `writer_names`, 03절의 `send_to_desks`도 마찬가지입니다.
인자와 본문은 앞 절 노트북 셀과 같습니다.
함수 `send_to_desks`가 쓰는 객체 `Send`를 가져오는 줄 하나가 도구 파일 맨 위에 더해졌습니다.

앞에서 배운 함수는 `delegation_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다."""),
    ] + model_cells() + [
        code(RULES),
        md("""**결과 읽기** — 출력 줄 `분야 이름: ['loan_desk', 'interlibrary_desk', 'facility_desk']`가 보입니다.
분야 이름은 03절과 같고, 4·5절에서는 그래프의 노드 이름으로도 씁니다.
세 규정 글은 앞 절 글 그대로이고, 모두 교재용으로 만든 글이라 실제 도서관 규정이 아닙니다.

다음 셀은 03절 5절 셀과 같은 코드로 도구 없는 전문 에이전트 셋을 만듭니다.
세 구조 모두 이 딕셔너리의 에이전트에게 문의를 맡깁니다."""),
        code(AGENTS),
        md("""**결과 읽기** — 출력 줄 `전문 에이전트: ['loan_desk', 'interlibrary_desk', 'facility_desk']`가 보입니다.
01절에서 본 것처럼, 도구 없는 전문 에이전트는 한 번 부르면 모델 요청이 1번입니다.
시스템 메시지 글이 자기 규정에 해당하는 부분에만 답하라고 적어, 두 분야 문의의 한쪽만 답합니다.

## 3. 서브에이전트 구조

01절의 중앙 에이전트는 담당마다 도구를 하나씩 두었습니다.
담당이 셋이면 도구도 셋이 되므로, 이 절은 공식 문서가 적는 다른 모양을 씁니다.
담당 이름을 인자로 받는 도구 하나를 두고, 그 도구가 이름으로 담당을 찾아 맡기는 모양입니다.
다음 셀이 그 도구이고, 본문의 나머지는 01절 도구와 같습니다."""),
        code(ASK_TOOL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
독스트링에 분야 이름 셋을 적어, 모델이 그 가운데에서 이름을 고르게 했습니다.
인자 `desk`에 딕셔너리에 없는 이름이 오면 `KeyError`가 나고, 이 절에서는 그 경우를 따로 받지 않았습니다.

다음 셀은 세 구조가 함께 쓸 담당 설명 글을 정하고, 이 도구를 가진 중앙 에이전트를 만듭니다.
담당 설명 글 `desk_guide`는 03절 분류 시스템 메시지 글의 가운데 두 문장입니다.
세 구조의 첫 에이전트가 모두 이 글을 받아, 같은 설명을 보고 담당을 고릅니다."""),
        code(CENTRAL),
        md("""**결과 읽기** — 출력 줄 `도구 인자: ['desk', 'question']`이 보입니다.
중앙 에이전트의 모델은 이 두 인자를 채워 도구를 요청합니다.
시스템 메시지 글은 01절 중앙 에이전트 글의 뼈대에 담당 설명 글을 넣은 것입니다.

다음 셀은 세 구조에 보낼 문의를 정하고, 서브에이전트 구조를 실행합니다.
실행 전에 예상해 봅니다.
중앙 에이전트가 두 담당에게 맡기면, 담당의 요청 2번에 중앙 쪽 요청이 더해질 것입니다."""),
        code(SUB_RUN),
        md("""**결과 읽기** — 출력 줄 `이번 실행이 더한 바깥 메시지: ['AIMessage', 'ToolMessage', 'ToolMessage', 'AIMessage']`가 보입니다.
응답 하나 뒤에 도구 메시지 둘이 이어 나와, 중앙 에이전트가 한 응답에서 도구를 두 번 요청했습니다.
출력 줄 `전문 에이전트를 부른 횟수: 2`로 담당이 두 번 불렸습니다.

맡기는 모양은 모델이 정해 실행마다 달라질 수 있습니다.
노트북 밖에서 같은 실행을 다섯 번 보냈을 때는 다섯 번 모두 한 응답에서 두 담당에게 맡겼습니다.
중앙 에이전트가 담당에게 넘긴 글은 실행마다 조금씩 달랐습니다.

다음 셀은 안쪽 목록마다 마지막 응답을 쓴 담당 이름을 모으는 함수입니다.
02절에서 본 것처럼, 이름을 붙여 만든 에이전트의 응답에는 칸 `name`에 그 이름이 들어갑니다.
도구 실행 노드는 한 응답의 도구 요청 여럿을 함께 실행해, 기록 목록에 붙는 차례가 실행마다 바뀔 수 있습니다.
그래서 분야 이름 차례로 모읍니다."""),
        code(DEF_ANSWERED),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
바깥 `for`가 분야 이름 차례를 정하고, 안쪽 `for`가 그 이름이 쓴 안쪽 목록을 찾습니다.
03절 종합 노드가 분야 이름 차례로 답을 엮은 것과 같은 생각입니다.

다음 셀은 담당 답이 모인 분야와 모델 요청 수를 세고, 마지막 응답의 모양을 봅니다.
요청 수는 01절 함수 `usage_with_specialists`로 바깥 목록의 새 메시지와 안쪽 목록을 함께 셉니다.
마지막 응답이 모델 요청으로 받은 응답인지는 사용량 기록이 있는지로 가립니다."""),
        code(SUB_CHECK),
        md("""**결과 읽기** — 출력 줄 `담당 답이 모인 분야: ['loan_desk', 'facility_desk']`가 보입니다.
출력 줄 `모델 요청 수(중앙 + 전문): 4`는 중앙 2번과 담당 2번입니다.
01절에서 본 셈대로 중앙은 도구를 요청한 응답 수 + 1이고, 담당은 부른 횟수입니다.
출력 줄 `마지막 응답이 도구 요청 없는 모델 응답인가: True`로, 중앙 에이전트가 최종 답을 썼습니다.

응답 둘에 나눠 한 번씩 맡겼다면 중앙 3번과 담당 2번으로 요청은 5번이 됩니다.
이 실행은 중앙 에이전트의 모델이 도구 요청 없는 응답을 골라 끝났습니다.
Ch 17 03절의 정지 조건 가운데 모델의 끝 선택입니다.

## 4. 핸드오프 구조

02절의 핸드오프는 첫 담당이 넘기기 도구로 다음 차례의 담당을 바꾸었습니다.
이 절은 문의를 받는 안내 담당 `front_desk`를 두고, 분야 노드 셋에 2절 전문 에이전트를 그대로 넣습니다.
안내 담당은 규정 글이 없어, 문의를 맡을 담당에게 넘기기만 합니다.
먼저 02절 5절과 같은 칸의 상태 형식을 만듭니다."""),
        code(TEAM_STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
메시지 칸에는 Ch 13 04절 메시지 규칙을, 담당 칸에는 넘겨받은 담당 이름을 둡니다.
02절처럼 첫 입력에 담당 칸 빈 글을 넣습니다.

다음 셀은 넘기기 도구입니다.
02절의 넘기기 도구는 상호대차 담당 한 곳으로만 넘겼습니다.
이 도구는 인자 `desk`로 가는 노드 이름과 담당 칸 값을 받고, 나머지는 02절 도구와 같습니다."""),
        code(TRANSFER),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
02절에서 본 것처럼 `graph=Command.PARENT`는 가장 가까운 바깥 그래프의 노드로 가라는 뜻입니다.
도구 메시지를 함께 담아, 넘기기 요청과 그 답이 짝을 이루게 합니다.

다음 셀은 이 도구를 가진 안내 담당과 바깥 그래프를 만듭니다.
공식 문서의 넘기기 도구는 한 응답에 넘기기 요청이 하나라고 가정합니다.
그래서 안내 담당의 시스템 메시지 글에 담당 한 명을 골라 넘기라고 적었습니다.
분야 노드는 저마다 끝점으로 가는 엣지를 두고, 체크포인터를 붙여 컴파일합니다."""),
        code(TEAM_BUILD),
        md("""**결과 읽기** — 설계 객체를 만들고 컴파일만 하는 셀이라 출력이 없습니다.
인자 `destinations`에는 안내 담당의 넘기기 도구가 보낼 수 있는 분야 노드 셋을 적었습니다.
체크포인터는 실행 뒤 저장된 기록을 읽으려고 붙였고, 이 절은 한 차례만 실행합니다.

다음 셀은 같은 문의로 핸드오프 구조를 실행합니다.
실행 전에 예상해 봅니다.
안내 담당이 한 담당에게 넘기면, 요청은 안내 담당 1번과 받은 담당 1번으로 2번일 것입니다.
두 분야를 묻는 문의라, 받은 담당은 자기 분야만 답할 것입니다."""),
        code(HAND_RUN),
        md("""**결과 읽기** — 출력 줄 `받은 오류: OpenAIInvalidRequestError | 상태 코드: 400`이 보입니다.
라벨 `오류 글 첫 문장:` 뒤의 글은 도구 요청이 든 응답 뒤에 요청마다 도구 메시지가 와야 한다는 뜻입니다.
모델 제공자가 요청을 잘못된 요청으로 거절하면, LangChain은 오류 `ModelInvalidRequestError`를 올립니다.
출력된 이름은 그 가운데 OpenAI용 오류 이름입니다.

어느 요청이 왜 거절되었는지는 다음 셀에서 저장된 기록으로 봅니다."""),
        code(HAND_STATE),
        md("""**결과 읽기** — 출력 줄 `저장된 메시지: ['AIMessage', 'ToolMessage']`와 `안내 담당 응답의 넘기기 요청 수: 2`가 보입니다.
안내 담당은 한 응답에서 두 담당에게 넘기려 했지만, 도구 메시지는 하나만 저장되었습니다.
출력 줄 `모델 요청 수: 1`은 안내 담당의 응답 하나이고, 받은 담당의 요청은 거절되어 응답이 없습니다.
받은 담당의 모델 요청에 짝 없는 넘기기 요청이 실려, 서비스가 거절한 것입니다.

이번 실행에서는 출력 줄 `담당 칸: loan_desk | 다음에 실행할 노드: ('loan_desk',)`였습니다.
두 넘기기 가운데 어느 쪽이 남는지는 실행마다 달라질 수 있습니다.
노트북 밖 다섯 번에서는 대출 규정 담당이 셋, 시설 담당이 둘이었습니다.

02절 5절에서는 도구 메시지가 빠진 기록을 모델 없이 만들어 보았고, 서비스 모델은 부르지 않았습니다.
이번에는 그 기록이 실제로 생겨, 공식 문서가 적는 대로 기록이 어긋나 요청이 거절되었습니다.
02절 7절은 한 응답에 넘기기 요청이 하나라 짝이 맞았고, 이번에는 한 응답에 둘이라 어긋났습니다.

핸드오프는 한 차례에 다음 담당 하나를 정하는 구조라, 두 분야 문의를 한 차례에 두 담당이 답하게 하는 데는 맞지 않습니다.
넘기기가 한 담당에게 오류 없이 갔더라도, 모인 분야가 하나라 8절의 완료 조건은 `False`가 됩니다.

## 5. 라우터 구조

라우터는 03절 5~6절 그래프를 같은 코드로 다시 만듭니다.
조건 함수 `send_to_desks`는 이 절부터 도구 파일에서 가져오고, 나머지 노드는 03절 셀 그대로 적습니다.
먼저 분류 모델이 채울 양식 클래스입니다."""),
        code(FORM),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 `desks`는 분야 이름 셋 가운데에서 고른 이름의 목록만 받습니다.

다음 셀은 분류 시스템 메시지 글을 정하고, 모델 객체에 양식 클래스를 붙입니다.
가운데 두 문장을 담당 설명 글로 이어, 글 전체는 03절 글과 같습니다."""),
        code(CLASSIFIER),
        md("""**결과 읽기** — 출력 줄 `분류 모델의 종류: RunnableSequence`가 보입니다.
03절처럼 호출 객체만 만들고, 모델 요청은 아직 보내지 않습니다.

다음 셀은 03절과 같은 상태 형식입니다.
응답 칸 `responses`에 분류 모델과 전문 에이전트의 응답을 모아, 요청 수를 셉니다.
이 5절의 코드 셀 주석에 적힌 「2절」·「뒤 절반」은 03절 노트북의 절을 가리킵니다."""),
        code(MODEL_STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
답 칸과 응답 칸에 이어 붙이기 규칙을 적은 것도 03절과 같습니다.

다음 셀은 모델이 분야를 고르는 분류 노드입니다."""),
        code(CLASSIFY_MODEL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
분류 모델이 고른 이름 목록은 분야 칸에, 결과의 모델 응답은 응답 칸에 냅니다.

다음 셀은 분야 이름으로 전문 에이전트를 찾아 문의를 맡기는 분야 노드입니다."""),
        code(ASK_DESK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
3절 도구처럼 분야 이름으로 담당을 찾지만, 이 함수는 도구가 아니라 그래프의 노드입니다.

다음 셀은 분야 이름 차례로 답을 엮는 종합 노드입니다."""),
        code(JOIN),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
모델을 부르지 않는 보통 함수라, 라우터의 요청 수에 더해지지 않습니다.

다음 셀은 03절과 같은 호출로 라우터 그래프를 만듭니다."""),
        code(MODEL_BUILD),
        md("""**결과 읽기** — 설계 객체를 만들고 컴파일만 하는 셀이라 출력이 없습니다.
조건부 엣지에 넘긴 `send_to_desks`는 도구 파일의 함수이고, 본문은 03절 셀과 같습니다.

다음 셀은 같은 문의로 라우터 구조를 실행합니다.
실행 전에 예상해 봅니다.
03절처럼 두 분야를 고르면, 요청은 분류 1번과 두 담당 2번으로 3번일 것입니다."""),
        code(ROUTE_RUN),
        md("""**결과 읽기** — 출력 줄 `모델이 고른 분야: ['loan_desk', 'facility_desk']`와 `답 칸 줄 수: 2`가 보입니다.
출력 줄 `모델 요청 수: 3`은 03절에서 본 셈 분류 1 + 고른 분야 수와 같습니다.
이 실행은 종합 노드 뒤의 고정 엣지로 끝점에 닿아 끝났습니다.

고른 분야는 모델이 정해 실행마다 달라질 수 있습니다.
노트북 밖에서 같은 실행을 다섯 번 보냈을 때는 다섯 번 모두 이 두 분야를 골랐습니다.

## 6. 세 구조의 요청 수와 비용

세 실행의 요청 수와 토큰을 한 표로 모읍니다.
예상 비용은 Ch 6 06절 함수 `estimate_cost`로 요금표에서 어림한 값이고, 청구 금액이 아닙니다.
요금은 과정의 2026-09-17 요금표이고, 요율은 이름 있는 변수에 담습니다."""),
        code(COMPARE),
        md("""**결과 읽기** — 라벨 줄 `구조 | 모델 요청 수 | 입력 토큰 | 출력 토큰 | 예상 비용(달러)` 아래에 구조마다 한 줄이 있습니다.
모델 요청 수 칸은 서브에이전트 4, 핸드오프 1, 라우터 3입니다.
핸드오프의 1은 안내 담당의 응답이고, 받은 담당의 요청은 거절되어 세지 않았습니다.
요청 수는 구조가 정하는 셈과 모델의 판단이 함께 정합니다.

이번 실행에서는 라벨 줄 아래가 `서브에이전트 | 4 | 989 | 228 | 0.001768`, `핸드오프 | 1 | 265 | 55 | 0.000446`, `라우터 | 3 | 468 | 87 | 0.000742`였습니다.
토큰 수와 예상 비용은 실행마다 달라질 수 있습니다.

이 표로 어느 구조가 싸다고 말할 수는 없습니다.
핸드오프는 일을 끝내지 못했고, 토큰 수는 실행마다 달라지기 때문입니다.
절 제목은 비용 비교를 기대하게 하지만, 이 절이 결론으로 두는 것은 구조마다의 요청 수 셈입니다.

## 7. 한도로 멈춘 실행

Ch 17 03절은 반복을 멈추는 정지 조건 넷을 보았습니다.
모델의 끝 선택, 사람 확인, 같은 도구를 다시 고름, 바퀴 한도입니다.
3절 서브에이전트는 모델의 끝 선택으로, 5절 라우터는 고정 엣지로 끝났습니다.
이번에는 한도에 닿아 멈추는 실행 둘을 실제로 만듭니다.

한도를 가리키는 말은 셋이고, 세는 것이 서로 다릅니다.
실행 한도(Ch 20 03절)는 그래프가 진행한 단계 수를 셉니다.
호출 한도(Ch 16 04절·Ch 22 04절)는 한도를 붙인 에이전트의 모델 요청 수를 셉니다.
바퀴 한도(Ch 17 03절)는 루프가 돈 바퀴 수를 셉니다.

먼저 모델 없이, 두 담당이 서로 넘기기만 하는 노드를 만듭니다."""),
        code(BOUNCE_DEF),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
담당 칸이 대출 규정 담당이면 시설 담당으로, 아니면 대출 규정 담당으로 넘깁니다.
끝점으로 가는 갈래가 없어, 이 노드 둘만으로는 그래프가 끝나지 않습니다.

다음 셀은 이 함수를 두 노드에 쓴 그래프를 실행 한도 4로 실행합니다.
실행 전에 예상해 봅니다.
두 노드가 번갈아 돌다가, 멈출 조건에 닿지 못한 채 실행 한도에 닿을 것입니다."""),
        code(BOUNCE_RUN),
        md("""**결과 읽기** — 출력 줄 `받은 오류: GraphRecursionError`가 보입니다.
라벨 줄 아래 `Recursion limit of 4 reached without hitting a stop condition.`은 멈출 조건에 닿지 않은 채 한도 4에 닿았다는 뜻입니다.
Ch 20 03절에서 본 실행 한도의 오류와 같은 모양입니다.
모델을 부르지 않는 그래프라 요청은 0번입니다.

두 담당이 저마다 넘기기 도구를 가지면, 모델 판단으로 이런 반복이 일어날 수 있습니다.
그래서 이 절의 모델 그래프에는 모두 실행 한도 10을 함께 주었습니다.

다음 셀은 3절 중앙 에이전트와 같은 도구와 시스템 메시지 글에 호출 한도 1을 붙여 실행합니다.
인자 `run_limit`은 한 번 실행 안에서 보낼 수 있는 모델 요청 수입니다.
인자 `exit_behavior="end"`는 한도에 닿으면 끝으로 가라는 뜻입니다.
실행 전에 예상해 봅니다.
첫 요청은 나가고, 도구를 부른 뒤 최종 답을 쓰려는 둘째 요청 전에 멈출 것입니다."""),
        code(LIMIT_RUN),
        md("""**결과 읽기** — 출력 줄 `이번 실행이 더한 바깥 메시지: ['AIMessage', 'ToolMessage', 'ToolMessage', 'AIMessage']`가 보입니다.
출력 줄 `전문 에이전트를 부른 횟수: 2`로, 첫 응답의 도구 요청대로 두 담당은 실행되었습니다.
출력 줄 `마지막 응답 글: Model call limits exceeded: run limit (1/1)`은 호출 한도가 적어 넣은 글입니다.
출력 줄 `마지막 응답의 사용량: None`으로, 이 응답은 모델 요청으로 받은 것이 아닙니다.

설치판 소스에서 호출 한도는 모델 요청 전에 요청 수를 보고, 한도에 닿았으면 이 글을 넣고 끝으로 건너뜁니다.
그래서 모델 요청은 중앙 1번과 담당 2번이었고, 중앙 에이전트의 최종 답은 없습니다.
호출 한도는 한도를 붙인 중앙 에이전트의 요청만 세고, 도구 안에서 부른 담당의 요청은 세지 않았습니다.
바깥 목록의 종류만 보면 3절과 같지만, 마지막 응답이 다릅니다.

## 8. 완료 조건

한도에 닿아 멈춘 실행도 오류 없이 끝나거나 마지막 응답을 남길 수 있습니다.
그래서 멈춘 까닭만 보고는 일이 끝났는지 가릴 수 없고, 따로 기준이 필요합니다.
완료 조건(completion condition)은 필요한 결과가 다 모였는지 보는 기준입니다.
이사 트럭이 약속한 시간에 떠나도, 짐이 다 실렸는지는 짐 목록을 보고 따로 따지는 것과 같습니다.
정지 조건은 실행이 멈추는 까닭이고, 완료 조건은 멈춘 뒤 일이 끝났는지 보는 기준입니다.

구조마다 완료 조건을 문장으로 적으면 이렇습니다.
서브에이전트의 완료 조건은 두 가지입니다.
맡긴 분야마다 전문 에이전트의 답 글이 도구 메시지로 돌아와야 합니다.
그 뒤 중앙 에이전트가 도구 요청 없는 최종 답을 모델 응답으로 써야 합니다.

핸드오프는 넘겨받은 담당이 이번 차례의 마지막 응답을 쓰고, 필요한 분야가 모두 그 답에 들어야 끝입니다.
라우터는 필요한 분야의 답이 답 칸에 모이고, 종합 칸이 빈 글이 아니어야 끝입니다.
이 절은 세 구조를 한 함수로 보려고, 모인 분야 이름과 마지막 답이 있는지를 인자로 받습니다.
다음 셀이 그 함수입니다."""),
        code(DONE_DEF),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
필요한 분야 하나라도 모인 분야에 없으면 `False`를 내놓고, 모두 있으면 마지막 답이 있는지를 내놓습니다.
모인 분야와 마지막 답을 어떻게 셀지는 구조마다 3~5절 셀과 다음 셀에서 정했습니다.

다음 셀은 네 실행에 이 함수를 대어 봅니다.
필요한 분야는 문의가 묻는 대출 연장과 토요일 운영 시간의 두 담당이고, 문의 글을 보고 실행 전에 정했습니다.
실행 전에 예상해 봅니다.
서브에이전트와 라우터는 `True`, 핸드오프와 호출 한도를 붙인 실행은 `False`일 것입니다."""),
        code(DONE_APPLY),
        md("""**결과 읽기** — 라벨 줄 아래 `서브에이전트 | True`와 `라우터 | True`가 보입니다.
출력 줄 `핸드오프 | False`와 `호출 한도 1을 붙인 서브에이전트 | False`도 보입니다.
호출 한도를 붙인 실행은 두 담당의 답이 모였지만, 마지막 응답이 한도 글이라 `False`입니다.
핸드오프는 받은 담당의 요청이 거절되어 담당 답이 하나도 모이지 않았습니다.

한도로 끝난 실행과 일이 끝난 실행은 다릅니다.
실행 한도에 닿은 7절 핑퐁 그래프는 오류로 멈춰 결과가 없었습니다.
호출 한도에 닿은 실행은 오류 없이 끝났지만, 일은 끝나지 않았습니다.
03절 4절의 빈 분류처럼 조용히 끝나는 실행도, 완료 조건으로 보면 끝나지 않은 일을 가릴 수 있습니다.

## 정리

1. 서브에이전트의 요청은 중앙(도구를 요청한 응답 수 + 1)과 전문(부른 횟수)의 합이었습니다. 라우터의 요청은 분류 1 + 고른 분야 수였습니다.
2. 핸드오프에서는 흔들림 확인 다섯 번과 두 커널 모두, 안내 담당이 한 응답에 넘기기 요청 둘을 냈습니다. 넘기기 하나만 적용되어 기록이 어긋났고, 받은 담당의 요청이 거절되었습니다. 넘기기가 한 담당에게 오류 없이 갔더라도, 모인 분야가 하나라 완료 조건은 `False`였을 것입니다.
3. 실행 한도와 호출 한도로 멈춘 실행은 완료 조건을 채우지 못했고, 한도로 끝남과 일이 끝남은 다릅니다.

05절은 이 챕터의 실습으로, 01절 요청 수 셈으로 호출 한도를 정하고 완료 조건으로 일이 끝났는지 확인합니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


L_01 = "01-Subagent-도구-위임.html"
L_02 = "02-Handoff-상태-전환.html"
L_03 = "03-Router-분류와-병렬-실행.html"
L_CH06_06 = "../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html"
L_CH16_04 = "../../part4/ch16-guardrails/04-호출-한도와-비용-상한.html"
L_CH17_03 = "../../part5/ch17-agent-overview/03-모델-도구-루프와-정지-조건.html"
L_CH20_03 = "../../part5/ch20-tool-node/03-recursion-limit과-명시적-종료.html"
L_CH22_04 = "../ch22-middleware/04-호출-한도와-재시도-폴백.html"
L_CH23_01 = "../ch23-persistence/01-체크포인터와-스레드.html"
L_CH27_01 = "../ch27-deepagents/01-하네스와-일곱-기능.html"

TERM_ROWS = [
    ("완료 조건(completion condition)", "필요한 결과가 다 모였는지 보는 기준입니다. 이사 트럭이 약속한 시간에 떠나도, 짐이 다 실렸는지는 짐 목록을 보고 따로 따지는 것과 같습니다. 이 절에서 새로 적는 말입니다.", "함수 <code>is_complete</code> — 필요한 두 분야의 담당 답이 모였고 마지막 답이 있는가"),
    ("정지 조건", "반복을 멈추는 조건입니다(Ch 17 03절). 모델의 끝 선택, 사람 확인, 같은 도구를 다시 고름, 바퀴 한도 넷입니다.", "3절 서브에이전트는 모델의 끝 선택으로 멈춤"),
    ("실행 한도", "그래프가 한 번 실행에서 진행할 수 있는 단계 수의 한도입니다(Ch 20 03절).", "7절 핑퐁 그래프 <code>{\"recursion_limit\": 4}</code>, 모델 그래프는 모두 10"),
    ("호출 한도", "한도를 붙인 에이전트가 한 번 실행에서 보낼 수 있는 모델 요청 수의 상한입니다(Ch 16 04절·Ch 22 04절).", "7절 <code>ModelCallLimitMiddleware(run_limit=1, exit_behavior=\"end\")</code>"),
    ("바퀴 한도", "루프가 돌 수 있는 바퀴 수의 상한입니다(Ch 17 03절).", "이 절에서는 쓰지 않음"),
]

RESULT_ROWS = [
    ("서브에이전트(3절)", "4(중앙 2 + 전문 2)", "중앙 = 도구를 요청한 응답 수 + 1, 전문 = 부른 횟수", "중앙 에이전트가 도구 요청 없는 응답을 씀(모델의 끝 선택)", "True"),
    ("핸드오프(4절)", "1(안내 담당만, 받은 담당 요청은 거절)", "넘긴 담당 1 + 받은 담당 1", "받은 담당의 모델 요청이 서비스 오류로 거절됨", "False"),
    ("라우터(5절)", "3(분류 1 + 전문 2)", "분류 1 + 고른 분야 수", "종합 노드 뒤 고정 엣지로 끝점", "True"),
    ("호출 한도 1(7절)", "3(중앙 1 + 전문 2 — 출력의 부른 횟수 2와 사용량 있는 중앙 응답 하나로 셈)", "중앙 = 사용량 있는 응답 수, 전문 = 부른 횟수(한도는 중앙 요청만 셈)", "호출 한도가 둘째 요청 전에 끝냄", "False"),
    ("핑퐁 그래프(7절)", "0(모델 없음)", "—", "실행 한도 4에 닿아 <code>GraphRecursionError</code>", "결과 없음"),
]

TOKEN_ROWS = [
    ("서브에이전트", "989", "228", "0.001768"),
    ("핸드오프", "265", "55", "0.000446"),
    ("라우터", "468", "87", "0.000742"),
]

LOOK_B5 = "노트북 3절에서 <code>전문 에이전트를 부른 횟수: 2</code>와 <code>모델 요청 수(중앙 + 전문): 4</code>를 봅니다. 4절에서 <code>안내 담당 응답의 넘기기 요청 수: 2</code>와 저장된 메시지 두 줄을 견줍니다. 5절에서 <code>모델 요청 수: 3</code>이 분류 1 + 고른 분야 수와 같은지 봅니다. 맡기는 모양·넘기는 수·고르는 분야는 모델이 정하므로, 다시 실행하면 달라질 수 있습니다."
LOOK_B6 = "노트북 7절에서 <code>받은 오류: GraphRecursionError</code>와 <code>마지막 응답의 사용량: None</code>을 봅니다. 8절의 네 줄에서 호출 한도를 붙인 실행이 <code>False</code>인지 봅니다. 교재 출력의 토큰 수와 예상 비용, 4절의 담당 칸은 다시 실행하면 달라질 수 있어, 이 절의 결론에 쓰지 않았습니다."


def src_html() -> str:
    terms = table_html(["말", "뜻", "이 절에서"], TERM_ROWS)
    table = table_html(["실행", "이번 실행의 모델 요청 수", "요청 수 셈", "끝난 까닭", "완료 조건"], RESULT_ROWS)
    tokens = table_html(["구조", "입력 토큰(교재 출력)", "출력 토큰(교재 출력)", "예상 비용(교재 출력, 달러)"], TOKEN_ROWS)
    return """<!--meta: 강의 1h | 실습 1h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 1 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>같은 문의를 서브에이전트·핸드오프·라우터에 보내고, 구조마다 모델 요청 수를 셈으로 설명할 수 있습니다.</li>
<li>실행 한도와 호출 한도로 멈춘 실행을 만들고, 멈춘 까닭을 출력에서 읽을 수 있습니다.</li>
<li>필요한 결과가 다 모였는지 보는 완료 조건을 구조마다 문장과 코드로 적을 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_01 + """\">01절</a>부터 <a href=\"""" + L_03 + """\">03절</a>까지 위임 구조 셋을 차례로 만들었습니다. 구조를 고를 때는 요청이 몇 번 나가는지와 언제 끝나는지를 함께 따져야 합니다. 그런데 구조마다 다른 문의로 실행했기 때문에, 같은 일을 시켰을 때 무엇이 다른지는 아직 보지 못했습니다. 이 절은 같은 문의와 같은 전문 에이전트로 세 구조를 한 번씩 실행해 견줍니다.</p><p>절 제목의 종료 조건은 두 가지로 나눠 봅니다. 하나는 Ch 17 03절의 정지 조건으로, 실행이 멈추는 까닭입니다. 다른 하나는 이 절이 새로 적는 완료 조건으로, 일이 끝났는지 보는 기준입니다. 한도에 닿아 멈춘 실행은 멈추기는 했어도 일을 끝내지 못했을 수 있습니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_01 + """\">01절</a>에서는 중앙 에이전트가 도구로 전문 에이전트에게 일을 맡겼습니다. 요청 수는 중앙 = 도구를 요청한 응답 수 + 1, 전문 = 부른 횟수로 셌습니다. <a href=\"""" + L_02 + """\">02절</a>의 핸드오프는 넘긴 차례에 첫 담당 1번과 받은 담당 1번 요청했습니다. 02절 5절에서는 도구 메시지가 빠진 넘기기 기록을 모델 없이 보았습니다. <a href=\"""" + L_03 + """\">03절</a>의 라우터는 분류 1 + 고른 분야 수만큼 요청했고, 걸리는 분야가 없으면 조용히 끝났습니다.</p><p><a href=\"""" + L_CH17_03 + """\">Ch 17 03절</a>에서는 반복을 멈추는 정지 조건 넷을 보았습니다. 모델의 끝 선택, 사람 확인, 같은 도구를 다시 고름, 바퀴 한도입니다. <a href=\"""" + L_CH20_03 + """\">Ch 20 03절</a>의 실행 한도는 그래프가 진행한 단계 수의 한도였고, 넘으면 <code>GraphRecursionError</code>가 났습니다. <a href=\"""" + L_CH22_04 + """\">Ch 22 04절</a>에서는 <code>ModelCallLimitMiddleware</code>로 모델 요청을 1번으로 묶는 호출 한도를 붙였습니다. 호출 한도라는 말은 <a href=\"""" + L_CH16_04 + """\">Ch 16 04절</a>에서 처음 썼습니다.</p><p><a href=\"""" + L_CH06_06 + """\">Ch 6 06절</a>의 예상 비용은 요금표로 어림한 값이고, 청구 금액이 아닙니다. <a href=\"""" + L_CH23_01 + """\">Ch 23 01절</a>에서는 체크포인터에 저장된 상태를 <code>get_state</code>로 읽었습니다. 앞 절에서 처음 가르친 함수 넷은 이 절부터 도구 파일 <code>delegation_tools.py</code>에서 가져옵니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>나란한 물길 두 줄에 같은 모양 짐배가 한 척씩 떠 있습니다. 두 배의 갑판에는 짐을 실을 칸이 똑같이 그려져 있습니다. 위 배는 칸이 모두 찼고, 앞쪽 물길도 열려 있습니다. 아래 배는 칸이 반만 찼는데, 뱃머리 앞을 닫힌 문이 막아 멈춰 있습니다.</p><p>갑판의 칸이 필요한 결과이고, 칸이 다 찼는지 보는 것이 완료 조건입니다. 닫힌 문은 실행 한도나 호출 한도처럼 실행을 멈추게 하는 한도입니다. 아래 배는 멈췄지만 짐은 덜 찼습니다. 한도로 멈춘 것과 일이 끝난 것은 다릅니다.</p><p>비유와 다른 점이 있습니다. 짐배는 문이 열릴 때까지 기다릴 수 있지만, 한도에 닿은 실행은 그 자리에서 끝납니다. 또 이 절의 완료 조건은 짐의 수가 아니라, 필요한 분야 이름이 담당 답으로 모였는지를 봅니다.</p>
""" + illustration_block() + terms + """
<p>새 말을 이 절 코드에서 보면 이렇습니다. 노트북 8절 출력 <code>서브에이전트 | True</code>는 완료 조건을 채운 실행입니다. 같은 셀의 <code>호출 한도 1을 붙인 서브에이전트 | False</code>는 한도로 멈춰 완료 조건을 채우지 못한 실행입니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>세 구조의 요청 수는 구조가 정하는 셈을 따릅니다</h3><p>서브에이전트는 중앙 에이전트가 도구로 맡기고 답을 받아, 최종 답을 한 번 더 씁니다. 그래서 중앙 쪽은 도구를 요청한 응답 수 + 1이고, 담당 쪽은 부른 횟수입니다. 핸드오프는 넘긴 담당 1번과 받은 담당 1번이고, 라우터는 분류 1번에 고른 분야 수를 더합니다. 셈은 구조가 정하고, 맡기는 수와 고르는 분야는 모델이 정합니다.</p>
<h3>같은 전문 에이전트, 다른 첫 에이전트</h3><p>세 구조는 03절의 도구 없는 전문 에이전트 셋을 함께 씁니다. 다른 것은 문의를 처음 받는 쪽입니다. 서브에이전트는 중앙 에이전트, 핸드오프는 넘기기만 하는 안내 담당, 라우터는 분류 모델이 처음 받습니다. 세 쪽 모두 같은 담당 설명 글을 받아, 같은 설명을 보고 담당을 고릅니다.</p><p>01절은 담당마다 도구 하나를 두었습니다. 이 절의 중앙 에이전트는 담당 이름을 인자로 받는 도구 하나로 셋 가운데 누구에게든 맡깁니다. 공식 Subagents 문서도 담당마다 도구를 두는 모양과, 이름을 받는 도구 하나로 보내는 모양을 함께 적습니다.</p>
<h3>서브에이전트의 완료 조건</h3><p>서브에이전트의 완료 조건은 두 가지입니다. 맡긴 분야마다 전문 에이전트의 답 글이 도구 메시지로 돌아와야 합니다. 그 뒤 중앙 에이전트가 도구 요청 없는 최종 답을 모델 응답으로 써야 합니다. 도구 메시지가 모두 돌아와도 최종 답이 없으면, 중앙 에이전트는 일을 끝내지 못한 것입니다.</p><p>핸드오프는 넘겨받은 담당이 이번 차례의 마지막 응답을 쓰고, 필요한 분야가 모두 그 답에 들어야 끝입니다. 라우터는 필요한 분야의 답이 답 칸에 모이고, 종합 칸이 빈 글이 아니어야 끝입니다. 이 절은 이 문장들을 함수 <code>is_complete</code> 하나로 적고, 모인 분야와 마지막 답은 구조마다 따로 셉니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 03절과 같은 문의 글과 전문 에이전트 셋을 준비합니다. 3~5절은 그 문의를 서브에이전트·핸드오프·라우터에 한 번씩 보내고, 6절은 요청 수와 토큰을 한 표로 모읍니다. 7절은 모델 없는 핑퐁 그래프를 실행 한도 4로, 3절 중앙 에이전트를 호출 한도 1로 실행합니다. 8절은 완료 조건 함수를 네 실행에 대어 봅니다.</p><p>실제 OpenAI 모델 <code>gpt-5.4-mini</code>를 temperature 0으로 부르고, 모든 에이전트가 모델 객체 하나를 함께 씁니다. 모델 요청은 노트북 한 번에 11번이고, 4절에서 서비스가 거절한 요청 하나는 이 수에 넣지 않았습니다. 요금표로 어림한 예상 비용은 0.005달러 아래이고, 청구 금액이 아닙니다. 읽거나 쓰는 파일은 없고, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>서브에이전트는 이번 실행에서 한 응답에 두 담당을 맡겨, 요청이 중앙 2번과 담당 2번이었습니다. 라우터는 두 분야를 골라 분류 1번과 담당 2번이었습니다. 두 실행 모두 요청 수가 구조의 셈과 맞았고, 필요한 두 분야의 답이 모였습니다. 맡긴 모양과 고른 분야는 흔들림 확인 다섯 번과 두 커널에서 모두 같았습니다.</p>
""" + table + """
<p>핸드오프는 이번 실행에서 일을 끝내지 못했습니다. 안내 담당이 한 응답에서 두 담당에게 넘기려 했지만, 바깥 그래프에는 넘기기 하나만 적용되었습니다. 저장된 기록에는 넘기기 요청 둘에 도구 메시지 하나만 남았습니다. 받은 담당의 모델 요청에 짝 없는 넘기기 요청이 실려, 서비스가 잘못된 요청으로 거절했습니다. 한 응답의 넘기기 요청 둘은 흔들림 확인 다섯 번과 두 커널에서 모두 같았습니다.</p><p>공식 Handoffs 문서는 넘기기 도구가 한 응답에 하나만 불린다고 가정합니다. 도구 메시지가 없으면 기록이 어긋난다고도 적습니다. 이 절은 두 문장이 가리키는 일을 실제 실행으로 만났습니다. 이 거절은 이번 넘기기 도구 모양에, 안내 담당이 한 응답에 넘기기 요청 둘을 낸 모델 판단이 겹쳐 난 일입니다. 02절 7절은 한 응답에 넘기기 요청이 하나라, 도구 메시지가 그 요청의 답으로 짝이 맞았습니다.</p><p>핸드오프는 한 차례에 다음 담당 하나를 정하는 구조라, 두 분야 문의를 한 차례에 두 담당이 답하게 하는 데는 맞지 않습니다. 필요한 분야는 둘인데 받은 담당은 자기 분야만 답합니다. 그래서 넘기기가 한 담당에게 오류 없이 갔더라도, 모인 분야가 하나라 완료 조건은 <code>False</code>가 됩니다.</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>한도로 멈춘 두 실행은 멈춘 모양이 달랐습니다. 모델 없는 핑퐁 그래프는 실행 한도 4에 닿아 <code>GraphRecursionError</code>로 멈췄고, 남은 결과가 없습니다. 호출 한도 1을 붙인 중앙 에이전트는 오류 없이 끝났고, 두 담당의 답도 모였습니다. 그러나 마지막 응답은 호출 한도가 적어 넣은 글이라, 완료 조건은 <code>False</code>였습니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>아래 표는 세 구조의 교재 출력 토큰과 예상 비용입니다. 핸드오프는 안내 담당의 응답 하나만 센 값입니다. 토큰 수와 예상 비용은 다시 실행하면 달라질 수 있습니다.</p>
""" + tokens + """
<p>이 표로 어느 구조가 싸다고 말할 수는 없습니다. 핸드오프는 일을 끝내지 못했고, 세 실행이 끝낸 일이 같지 않습니다. 절 제목은 비용 비교를 기대하게 하지만, 이 절의 결론은 구조마다의 요청 수 셈과 완료 조건입니다.</p><p>공식 문서 multi-agent 개요도 구조별 모델 요청 수를 예로 적습니다. 커피 주문 한 번은 서브에이전트 4번, 핸드오프와 라우터 3번입니다. 세 언어를 견주는 여러 분야 요청은 서브에이전트와 라우터 5번, 핸드오프 7번 이상입니다. 문서는 서브에이전트의 결과가 중앙 에이전트를 거쳐 오느라 요청이 하나 더 든다고 적습니다. 핸드오프는 차례대로 실행되어 세 언어를 함께 조사할 수 없다고도 적습니다.</p><p>문서의 수를 이 절의 결과처럼 쓰지는 않습니다. 문서의 예에서는 전문 에이전트가 커피 주문 도구를 부르고, 이 절의 담당은 도구가 없습니다. 분야 수도 문서는 셋, 이 절은 둘입니다. 문서는 요청을 분류·에이전트·도구·종합으로 나눠 적지 않아, 이 절은 문서의 수를 이 절의 셈으로 풀어 맞춰 보지 않았습니다.</p>
<p>새 커널로 두 번 실행해 견주자, 서른 셀 가운데 스물아홉 셀의 출력이 같았습니다. 달랐던 한 셀은 6절 요청 수 표이고, 서브에이전트와 라우터의 토큰과 예상 비용이 달랐습니다. 모델 요청 수 칸과 4절의 담당 칸을 포함한 나머지 값은 두 번 모두 같았습니다. 그래도 담당 칸은 노트북 밖 확인에서 실행마다 갈렸으므로, 결론에 쓰지 않았습니다.</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>맡기는 모양, 넘기는 수, 고르는 분야는 모델이 정합니다. 노트북 밖에서 세 구조를 다섯 번씩 실행하자 다섯 번 모두 같은 모양이었습니다. 그래도 같은 요청이 실행한 때에 따라 달라질 수 있습니다. 중앙 에이전트가 응답 둘에 나눠 맡기면 요청은 5번, 라우터가 한 분야만 고르면 2번이 됩니다.</li><li>핸드오프는 노트북 밖에서 열 번 실행해 열 번 모두 같은 오류로 거절되었습니다. 기록을 읽은 다섯 번은 모두 넘기기 요청이 둘이었습니다. 바깥 그래프에 적용된 넘기기는 대출 규정 담당 셋, 시설 담당 둘로 갈렸고, 그래서 4절의 담당 칸은 결론에 쓰지 않았습니다.</li><li>설치판 langchain 1.4.0 <code>agents/factory.py</code> 1964행은 한 응답의 도구 요청마다 도구 실행 노드를 따로 부릅니다. 그래서 넘기기 도구 둘은 저마다 바깥 그래프로 가는 <code>Command</code>를 올려 보냈습니다. langgraph 1.2.11 <code>graph/state.py</code> 1762행이 그 <code>Command</code>를 올려 보내는 자리입니다. 두 작업이 끝나면 같은 판 <code>pregel/_runner.py</code> 650~690행이 그 가운데 하나만 골라 바깥으로 넘깁니다. 어느 쪽이 남는지는 실행마다 달라, 도구 요청 차례가 같아도 담당 칸이 대출 셋·시설 둘로 갈렸습니다.</li><li>넘기기 요청을 한 응답에 하나로 묶는 설정이나, 두 분야를 차례로 넘기는 방법은 이 절에서 실행하지 않았습니다. 안내 담당의 시스템 메시지 글에 담당 한 명을 적었지만, 이번 실행에서는 그 글만으로 한 번에 하나를 넘기게 되지 않았습니다.</li><li>설치판 langchain 1.4.0 <code>agents/middleware/model_call_limit.py</code> 168~208행은 모델 요청 전에 요청 수를 봅니다. 한도에 닿았으면 한도 글을 담은 응답을 넣고 끝으로 건너뜁니다. 236~250행은 모델 요청 뒤에 수를 늘립니다. 그래서 첫 요청의 도구는 실행되고, 둘째 요청 전에 끝났습니다.</li><li>호출 한도는 한도를 붙인 에이전트의 요청만 셉니다. 이번 실행에서 한도는 <code>(1/1)</code>이었지만, 도구 안에서 부른 담당의 요청 2번이 더 나갔습니다. 요금을 묶으려면 담당 에이전트에도 한도를 따로 붙여야 하고, 이 절에서는 실행하지 않았습니다.</li><li>분야 이름을 받는 도구에 없는 이름이 오면 <code>KeyError</code>가 납니다. 도구 실행 노드는 이 오류를 받지 않고 올려 보내 실행이 멈춥니다. 이번 실행과 흔들림 확인에서는 모델이 늘 셋 가운데 이름을 골라, 이 경우는 실행하지 않았습니다.</li><li>필요한 분야 둘은 문의 글을 보고 실행 전에 정했습니다. 모델이 고른 값이 아니라, 흐름을 보여 주려고 정한 기준입니다. 규정 글은 모두 교재용이고, 실제 도서관 규정이 아닙니다.</li><li>토큰 수와 예상 비용은 2026-09-17 과정 요금표로 어림했고, 청구 금액이 아닙니다. 걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>서브에이전트의 요청은 중앙(도구를 요청한 응답 수 + 1)과 전문(부른 횟수)의 합이었습니다. 라우터의 요청은 분류 1 + 고른 분야 수였습니다.</li><li>핸드오프에서는 흔들림 확인 다섯 번과 두 커널 모두, 안내 담당이 한 응답에 넘기기 요청 둘을 냈습니다. 넘기기 하나만 적용되어 기록이 어긋났고, 받은 담당의 요청이 거절되었습니다. 넘기기가 한 담당에게 오류 없이 갔더라도, 모인 분야가 하나라 완료 조건은 <code>False</code>였을 것입니다.</li><li>실행 한도와 호출 한도로 멈춘 실행은 완료 조건을 채우지 못했고, 한도로 끝남과 일이 끝남은 다릅니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"05-위임-구조-실습.html\">05절</a>은 이 챕터의 실습입니다. 01절 요청 수 셈으로 호출 한도를 정하고, 완료 조건으로 일이 끝났는지 확인합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 서브에이전트 실행에서 모델 요청이 4번이었습니다. 이 수를 셈으로 풀어 보세요.</p><p class="quiz-a">중앙 에이전트는 도구를 요청한 응답 하나에 최종 답 하나를 더해 2번입니다. 한 응답에서 두 담당에게 맡겨, 담당 쪽은 부른 횟수인 2번입니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">2. 핸드오프 실행에서 받은 담당의 모델 요청이 거절된 까닭은 무엇인가요?</p><p class="quiz-a">안내 담당이 한 응답에 넘기기 요청 둘을 냈지만, 바깥 그래프에는 넘기기 하나와 도구 메시지 하나만 남았습니다. 짝 없는 넘기기 요청이 받은 담당의 요청에 실려, 서비스가 잘못된 요청으로 거절했습니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">3. 호출 한도 1을 붙인 실행은 두 담당의 답이 모였는데도 완료 조건이 False였습니다. 왜 그런가요?</p><p class="quiz-a">마지막 응답이 중앙 에이전트가 쓴 최종 답이 아니라, 호출 한도가 적어 넣은 글이기 때문입니다. 그 응답은 모델 요청으로 받은 것이 아니라 사용량이 <code>None</code>입니다. 틀렸다면 노트북 7절과 8절을 다시 읽습니다.</p><p class="quiz-q">4. 동료가 「실행이 오류 없이 멈췄으니 일도 끝난 것」이라고 말합니다. 이 절의 결과로는 어떻게 답하나요?</p><p class="quiz-a">멈춘 까닭과 일이 끝났는지는 따로 봐야 합니다. 호출 한도로 멈춘 실행은 오류 없이 끝났지만 완료 조건은 <code>False</code>였습니다. 필요한 결과가 모였는지를 완료 조건으로 따로 봅니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langchain/multi-agent">LangChain Multi-agent</a></div>확인 2026-09-28 · 서브에이전트·핸드오프·스킬·라우터의 모델 요청 수를 세 예로 적습니다. 예는 커피 주문 한 번, 같은 요청 두 번, 여러 분야 요청입니다. 요청을 단계마다 나눠 적지는 않습니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langchain/multi-agent/subagents">LangChain Subagents</a></div>확인 2026-09-28 · 담당마다 도구를 두는 모양과, 담당 이름을 인자로 받는 도구 하나로 보내는 모양을 표로 견줍니다. 이 절의 도구 <code>ask_desk_agent</code>는 뒤의 모양입니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs">LangChain Handoffs</a></div>확인 2026-09-28 · 넘기기 도구 예가 한 응답에 넘기기 요청이 하나라고 가정한다고 적습니다. 짝 맞는 도구 메시지가 없으면 대화 기록이 어긋난다고도 적습니다.</li><li><div><a href="https://github.com/langchain-ai/langgraph-supervisor-py">langgraph-supervisor README</a></div>확인 2026-09-28 · 대부분의 경우 이 라이브러리보다 도구로 중앙 에이전트 모양을 직접 만들기를 권한다고 적습니다. 최신 판은 0.0.31(2025-11-19)이고, 이 과정의 설치 잠금에 없어 실행하지 않은 라이브러리입니다.</li><li>langchain 1.4.0 소스 <code>agents/middleware/model_call_limit.py</code> 168~208행과 236~250행은 호출 한도가 요청 수를 보고 늘리는 자리입니다. langchain 1.4.0 소스 <code>agents/factory.py</code> 1964행은 도구 요청마다 도구 실행 노드를 따로 부르는 자리입니다. langgraph 1.2.11 소스 <code>graph/state.py</code> 1762행은 바깥 그래프로 가는 <code>Command</code>를 올려 보내는 자리입니다. 같은 판 <code>pregel/_runner.py</code> 650~690행은 함께 끝난 작업들이 올려 보낸 것 가운데 하나만 넘기는 자리입니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    check_tools()
    check_same_as_probe()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "delegation_tools.py").write_text(TOOLS_04, encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        write_tools()
        path = write_notebook(LAB, "04", SLUG, "experiment", cells())
        print("wrote", path)
