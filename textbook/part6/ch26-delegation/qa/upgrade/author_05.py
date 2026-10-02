"""Ch 26 05절(챕터 끝 실습 절) 생성기 (QUALITY-UPGRADE.md §7-2·§2·§2-7·§3·§4·§6).

사용:
  python3 -B author_05.py            → 도구 파일(04절 판이거나 05절 판일 때만) + 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_05.py --src-only → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_05.py --tools-copy DIR → 05절 판 도구 파일만 DIR에 쓴다(새 커널 사본 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
새로 만든 절이라 qa/upgrade/before/ 에 원본이 없다. **experiment 형식**(chapter.json), lesson_part 없음.
슬러그 `05-위임-구조-실습`(규격 §7-2 `{NN+1}-{챕터 이름}-실습` — 챕터 제목의 한국어 머리말, 인계 후보).

## 결정 1 — 붙인 앞 절 기능 셋 (인계 「§04 → 실습(05)」 3항 (나))

01절 서브에이전트 모양과 요청 수 셈(message_kinds·usage_with_specialists — 중앙 에이전트는 04절 3절 판: 분야 이름을 받는 도구 ask_desk_agent 하나) +
04절 호출 한도(ModelCallLimitMiddleware(run_limit=…, exit_behavior="end")) + 04절 완료 조건(answered_desks·is_complete).
작은 과제: 자료실 문의 창구의 중앙 에이전트에 요금 사고를 막는 호출 한도를 붙이되, 한도 값은 01절 셈으로 정하고, 일이 끝났는지는 완료 조건으로 본다.
실행 1 = 호출 한도 2(한 번 맡길 때 중앙 요청 수 — 셈으로 실행 전에 정함) · 실행 2 = 호출 한도 1(값 하나). 문의 = 01절 문의 글 그대로(한 분야).
뺀 것: 03절 분류 모델(인계 3항 (가) — 05-probe.md §0에서 맡을 분야가 없는 두 문의가 열 번 모두 시설 담당으로 분류되어 빈 목록 갈래를 보일 수 없었고,
분류 요청이 더해져 요청 3~5번을 넘음) · 02절 핸드오프(두 분야 문의에서 서비스 오류로 멈춤 — 04절 4절) · 03절 Send 그래프 ·
04절 핑퐁 그래프(모델 없음, 04절 7절 되풀이) · 체크포인터(한 차례만).

## 결정 2 — 흔들림 먼저 확인 (qa/upgrade/05-probe.md)

§0 분류 모델 흐름(A1·A2·B2 다섯 번씩, 요청 60) → 실행 2 후보 둘 모두 규칙을 채우지 못해 §0-2에서 설계를 바꾸고 새 요청 전에 규칙을 적음 →
L2·L1 다섯 번씩(요청 25): 열 번 모두 첫 응답에서 loan_desk에 한 번 맡김 · 요청 3·2 · 완료 조건 True·False → 입력 그대로.

## 결정 3 — 결론은 코드가 정하는 값

요청 수 셈(중앙 = 도구를 요청한 응답 수 + 1, 전문 = 부른 횟수 — 한도에 닿으면 중앙 쪽이 한도 값에서 멈춤) · 마지막 응답이 한도 글인가 · 완료 조건.
토큰·예상 비용은 8절 둘째 단락·b6 표·b7에만([[…]] 자리 표시 → 교재 출력 실행 뒤 fillph05.py). assert는 키 셀 하나뿐.

## 결정 4 — 도구 파일 (§2-7) — 04절 함수 둘을 옮김

04절 노트북에만 있던 answered_desks(3절)·is_complete(8절)를 04절 셀 글 그대로 도구 파일 끝에 옮긴다(check_tools()가 author_04 셀과 문자열·AST 대조).
노트북 전역(desk_agents·specialist_runs·model·central_text·limit_config)에 기대는 도구·조립 함수·기록 장치는 노트북에 둔다.
해시 사슬 91512d6a…(04절 판) → 05절 판. 쓰기 가드: 04절 판이면 05절 판으로, 05절 판이면 그대로, 뒤 절 판이면 건너뜀, 아니면 assert.

## 모델 요청

노트북 한 번 **5번**(6절 실행 1 = 중앙 2 + 전문 1, 7절 실행 2 = 중앙 1 + 전문 1). 읽는 파일·쓰는 파일 0, 체크포인터 없음.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`isinstance`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·변수 힌트·대입 풀기·별표 풀기·`getattr`·`join`·
`while`·`try`·세미콜론·`>`·`<`·클래스·`Command`·`Send`·그래프 만들기·체크포인터·분류 모델.
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
import author_01  # noqa: E402  도구 파일 01절 판·본문 도우미·설치 셀
import author_03  # noqa: E402  03절 셀(전문 에이전트)
import author_04  # noqa: E402  04절 셀(규정 글·도구·중앙 에이전트 글·완료 조건)·도구 파일 04절 판
from nbkit import RUN_DATE, code, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch26-delegation/notebooks"
FIGS = ROOT / "textbook/part6/ch26-delegation/figures"
SLUG = "05-위임-구조-실습"
TITLE_TEXT = "위임 구조 실습: 요청 수 셈으로 호출 한도를 정하고 완료 조건으로 확인하기"
SRC = ROOT / "textbook/part6/ch26-delegation/_src" / (SLUG + ".html")
TOOLS_PATH = author_01.TOOLS_PATH
html_text = author_01.html_text
table_html = author_01.table_html
placeholder = author_01.placeholder


# ---------------------------------------------------------------- 도구 파일 05절 판 (04절 판 + 04절 함수 둘)
NOTE_04 = "Ch 26 04절에서 배웠습니다 — 04절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다"
NEW_BLOCKS_05 = [
    ("answered_desks", NOTE_04, author_04.DEF_ANSWERED),
    ("is_complete", NOTE_04, author_04.DONE_DEF),
]


def tools_05_text() -> str:
    text = author_04.TOOLS_04
    for name, note, cell in NEW_BLOCKS_05:
        text = text + "\n\n# " + note + "\n" + cell + "\n"
    return text


TOOLS_05 = tools_05_text()


def check_tools() -> None:
    """05절 판 도구 파일이 04절 판으로 시작하고, 더한 함수 둘이 04절 노트북 셀과 문자열·AST 모두 같은지 봅니다."""
    author_04.check_tools()
    assert TOOLS_05.startswith(author_04.TOOLS_04), "05절 판이 04절 판으로 시작하지 않습니다"
    assert author_01.strip_later_imports(TOOLS_05).startswith(author_01.TOOLS), "05절 판이 01절 판으로 시작하지 않습니다"
    tree = ast.parse(TOOLS_05)
    names = []
    imports = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
    assert names == ["tool_call_names", "show_messages", "sum_usage", "estimate_cost", "message_kinds", "usage_with_specialists",
                     "writer_names", "send_to_desks", "answered_desks", "is_complete"], names
    assert imports == ["from langgraph.types import Send"], imports
    for name, note, cell in NEW_BLOCKS_05:
        assert ("# " + note + "\n" + cell + "\n") in TOOLS_05, name
        mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        theirs = [ast.dump(n) for n in ast.parse(cell).body if isinstance(n, ast.FunctionDef)]
        assert mine == theirs and len(mine) == 1, name


def write_tools() -> None:
    """도구 파일 쓰기 가드: 04절 판이면 05절 판으로 바꾸고, 05절 판이면 그대로, 뒤 절이 더한 판이면 건너뜁니다."""
    current = ""
    if TOOLS_PATH.is_file():
        current = TOOLS_PATH.read_text(encoding="utf-8")
    if current == TOOLS_05:
        print("same", TOOLS_PATH)
        return
    if current == "" or current == author_04.TOOLS_04:
        TOOLS_PATH.write_text(TOOLS_05, encoding="utf-8")
        print("wrote", TOOLS_PATH, "(05절 판)")
        return
    later = author_01.strip_later_imports(current)
    assert later.startswith(author_01.strip_later_imports(TOOLS_05)), "도구 파일이 04절 판도 05절 판도 아닙니다"
    print("skip", TOOLS_PATH, "(뒤 절이 함수를 더한 판 — 덮어쓰지 않음)")


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = author_01.INSTALL

IMPORTS = r'''# 에이전트와 호출 한도(Ch 21 01절·Ch 22 04절)·모델(Ch 6 01절)·메시지(Ch 13 04절)·도구(Ch 19 01절) 이름을 가져옵니다
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain.tools import tool
# 앞 절에서 배운 함수 넷과 앞 챕터에서 배운 함수 하나는 도구 파일에서 가져옵니다
from delegation_tools import answered_desks, estimate_cost, is_complete, message_kinds, usage_with_specialists

print("도구 파일에서 가져온 함수:", "answered_desks, estimate_cost, is_complete, message_kinds, usage_with_specialists")'''

QUESTION = r'''# 두 실행에 보낼 문의 글과, 완료 조건에 쓸 필요한 분야를 실행 전에 정하고 출처와 함께 출력합니다
question_text = "빌린 책의 반납 날짜를 늘리려면 어떻게 하나요?"
needed_desks = ["loan_desk"]
print("문의 글:", question_text)
print("출처: 01절 문의 글 그대로")
print("필요한 분야:", needed_desks)
print("출처: 문의 글이 묻는 것은 대출 연장 하나")'''

RULES = author_04.RULES
AGENTS = author_03.AGENTS
ASK_TOOL = author_04.ASK_TOOL

CENTRAL_TEXT = r'''# 04절 3절과 같은 담당 설명 글과 중앙 에이전트의 시스템 메시지 글, 에이전트에 줄 실행 한도를 정합니다
desk_guide = " loan_desk는 대출·반납·연장·연체, interlibrary_desk는 다른 도서관 책을 빌려 오는 상호대차를 맡습니다."
desk_guide = desk_guide + " facility_desk는 자료실 운영 시간과 시설을 맡습니다."
central_text = "도서관 자료실 문의 창구의 안내 도우미입니다. 규정을 묻는 부분은 직접 답하지 말고 ask_desk_agent 도구로 담당에게 맡기세요."
central_text = central_text + desk_guide + " 담당이 준 답을 바탕으로 두 문장의 한국어로 답하세요."
# 모델이 끝없이 도구를 부르면 요청도 끝없이 나가므로, 실행 한도를 작게 줍니다(Ch 20 03절)
limit_config = {"recursion_limit": 10}
print("도구 인자:", list(ask_desk_agent.args))'''

DEF_COUNT = r'''# 이번 실행의 모델 요청 수와 토큰을 셉니다. 호출 한도가 적어 넣은 마지막 응답(사용량 None)은 빼고 셉니다
def count_run_usage(new_messages, inner_runs):
    counted = new_messages
    if new_messages[-1].usage_metadata is None:
        # 자르기 [:-1]은 맨 끝 하나를 뺀 앞부분입니다
        counted = new_messages[:-1]
    # 바깥 목록의 새 메시지와 안쪽 목록의 응답을 함께 셉니다(01절 함수)
    return usage_with_specialists(counted, inner_runs)'''

DEF_SUMMARY = r'''# 기록 장치입니다. 한 번의 실행에서 모인 분야·마지막 답·모델 요청 수·완료 조건을 모아 딕셔너리로 내놓습니다
def summarize_run(new_messages, inner_runs, needed):
    collected = answered_desks(inner_runs, desk_names)
    last = new_messages[-1]
    # 모델 요청으로 받은 응답에는 사용량 기록이 있습니다(04절 3절과 같은 판단)
    has_final = last.usage_metadata is not None and len(last.tool_calls) == 0
    usage = count_run_usage(new_messages, inner_runs)
    done = is_complete(collected, needed, has_final)
    return {"collected": collected, "final": has_final, "usage": usage, "complete": done}'''

DEF_FLOW = r'''# 조립 함수입니다. 호출 한도를 붙인 중앙 에이전트를 만들어 문의 하나를 맡기고, 이번 실행이 더한 바깥 메시지를 내놓습니다
def handle_inquiry(limit, question):
    # 04절 7절: 한 번 실행 안에서 보낼 수 있는 모델 요청 수를 limit으로 묶고, 닿으면 끝으로 갑니다
    call_limit = ModelCallLimitMiddleware(run_limit=limit, exit_behavior="end")
    # 04절 3절: 분야 이름을 받는 도구 하나를 가진 중앙 에이전트(01절 서브에이전트 모양)
    center = create_agent(model, tools=[ask_desk_agent], system_prompt=central_text, middleware=[call_limit])
    center_input = {"messages": [HumanMessage(content=question)]}
    center_result = center.invoke(center_input, limit_config)
    return center_result["messages"][1:]'''

LIMIT = r'''# 실행 1의 호출 한도를 01절 셈으로 정합니다. 한 번 맡기면 중앙 요청은 도구를 요청한 응답 1 + 최종 답 1입니다
tool_responses = 1
first_limit = tool_responses + 1
print("실행 1의 호출 한도:", first_limit)
print("출처: 01절 셈 중앙 = 도구를 요청한 응답 수 + 1")'''

RUN1 = r'''# 실행 1: 기록 목록을 비우고, 호출 한도 2를 붙인 중앙 에이전트로 문의를 처리합니다(모델 요청 3번 예상)
specialist_runs = []
first_new = handle_inquiry(first_limit, question_text)
print("이번 실행이 더한 바깥 메시지:", message_kinds(first_new))
print("전문 에이전트를 부른 횟수:", len(specialist_runs))'''

DETAIL1 = r'''# 실행 1에서 중앙 에이전트 첫 응답의 도구 요청과, 담당의 안쪽 목록 줄 수를 봅니다
first_calls = first_new[0].tool_calls
print("첫 응답의 도구 요청 수:", len(first_calls))
print("도구 인자의 분야 이름:", first_calls[0]["args"]["desk"])
print("안쪽 목록의 줄 수:", len(specialist_runs[0]))'''

SUM1 = r'''# 실행 1을 기록 장치로 모아, 모인 분야·마지막 답·모델 요청 수·완료 조건을 봅니다
first_summary = summarize_run(first_new, specialist_runs, needed_desks)
print("담당 답이 모인 분야:", first_summary["collected"])
print("마지막 응답이 도구 요청 없는 모델 응답인가:", first_summary["final"])
print("모델 요청 수(중앙 + 전문):", first_summary["usage"]["requests"])
print("완료 조건:", first_summary["complete"])'''

RUN2 = r'''# 실행 2: 값 하나만 바꿉니다. 호출 한도를 1로 줄이고, 기록 목록을 비운 뒤 같은 문의를 처리합니다
second_limit = 1
specialist_runs = []
second_new = handle_inquiry(second_limit, question_text)
print("이번 실행이 더한 바깥 메시지:", message_kinds(second_new))
print("전문 에이전트를 부른 횟수:", len(specialist_runs))'''

DETAIL2 = r'''# 실행 2의 마지막 응답 글과 사용량, 첫 응답의 도구 요청 수를 봅니다(호출 한도가 적어 넣은 응답인지)
second_last = second_new[-1]
print("마지막 응답 글:", second_last.text)
print("마지막 응답의 사용량:", second_last.usage_metadata)
print("첫 응답의 도구 요청 수:", len(second_new[0].tool_calls))'''

SUM2 = r'''# 실행 2를 같은 기록 장치로 모아, 모인 분야·마지막 답·모델 요청 수·완료 조건을 봅니다
second_summary = summarize_run(second_new, specialist_runs, needed_desks)
print("담당 답이 모인 분야:", second_summary["collected"])
print("마지막 응답이 도구 요청 없는 모델 응답인가:", second_summary["final"])
print("모델 요청 수(중앙 + 전문):", second_summary["usage"]["requests"])
print("완료 조건:", second_summary["complete"])'''

COMPARE = r'''# 두 실행의 호출 한도·모인 분야·마지막 답·모델 요청 수·완료 조건을 한 줄씩 견줍니다
run_limits = {"실행 1": first_limit, "실행 2": second_limit}
run_summaries = {"실행 1": first_summary, "실행 2": second_summary}
print("실행 | 호출 한도 | 모인 분야 | 마지막 답 | 모델 요청 수 | 완료 조건")
for name in run_summaries:
    summary = run_summaries[name]
    print(name, "|", run_limits[name], "|", summary["collected"], "|", summary["final"], "|", summary["usage"]["requests"], "|", summary["complete"])'''

COST = r'''# 두 실행의 토큰과 예상 비용을 봅니다(2026-09-17 요금표, 100만 토큰당 달러 — Ch 6 06절 함수)
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
print("실행 | 입력 토큰 | 출력 토큰 | 예상 비용(달러)")
for name in run_summaries:
    usage = run_summaries[name]["usage"]
    cost = round(estimate_cost(usage, input_rate, cached_input_rate, output_rate), 6)
    print(name, "|", usage["input_tokens"], "|", usage["output_tokens"], "|", cost)'''


def check_same_as_probe() -> None:
    """노트북 셀의 재료·도구·조립 함수·기록 장치 줄이 흔들림 확인 스크립트(probe05.py)와 같은지, 앞 절 셀과 같은지 봅니다."""
    probe = (HERE / "probe/probe05.py").read_text(encoding="utf-8")
    skip = ("print(", "def ", "@tool", "first_", "second_", "specialist_runs = []", "tool_responses", "run_limits", "run_summaries", "question_text = ",
            "for name in", "summary = ", "usage = run_summaries", "cost = ", "input_rate", "cached_input_rate", "output_rate")
    for cell in [QUESTION, RULES, AGENTS, ASK_TOOL, CENTRAL_TEXT, DEF_COUNT, DEF_SUMMARY, DEF_FLOW]:
        for line in cell.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith(skip):
                continue
            assert stripped in probe, stripped
    # 문의 글은 흔들림 확인 후보 A1과 같은 글(probe05.py의 QUESTIONS["A1"])
    assert '"A1": "빌린 책의 반납 날짜를 늘리려면 어떻게 하나요?"' in probe
    # 앞 절 셀과 같은 코드: 규정 글·도구는 04절 셀, 전문 에이전트는 03절 셀 글자 그대로(위에서 앞 절 값을 그대로 씀)
    assert RULES == author_04.RULES and ASK_TOOL == author_04.ASK_TOOL and AGENTS == author_03.AGENTS
    # 담당 설명 글·중앙 에이전트 글 네 줄과 실행 한도 줄은 04절 3절 셀과 같습니다
    for line in CENTRAL_TEXT.splitlines()[1:]:
        if not line.startswith("#"):
            assert line in author_04.CENTRAL or line in author_04.SUB_RUN, line
    # 조립 함수의 중앙 에이전트·호출 한도 줄은 04절 7절 셀과 같은 인자입니다(한도 값만 인자 limit)
    assert "create_agent(model, tools=[ask_desk_agent], system_prompt=central_text, middleware=[call_limit])" in author_04.LIMIT_RUN
    assert 'ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")' in author_04.LIMIT_RUN
    # 마지막 답 판단 식은 04절 3절 셀과 같은 식입니다
    assert "usage_metadata is not None and len(sub_last.tool_calls) == 0" in author_04.SUB_CHECK
    # 문의 글은 01절 문의 글 그대로
    assert 'question_text = "빌린 책의 반납 날짜를 늘리려면 어떻게 하나요?"' in (HERE / "author_01.py").read_text(encoding="utf-8")


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/05-figures.md)
FIG1 = "05-1-셈으로-정한-호출-한도를-붙인-창구"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 둘, 문의 글 한 줄 대출 연장 필요한 분야 loan_desk와 호출 한도 값 실행 1은 2 실행 2는 1에서 화살표가 파란 상자 조립 함수 handle_inquiry 04절 호출 한도를 붙여 04절 중앙 에이전트를 만듦으로 모입니다. 그 아래 회색 상자 중앙 에이전트 도구 ask_desk_agent 하나 01절 서브에이전트 모양에서, 도구로 맡김이라고 적힌 화살표가 오른쪽 아래 회색 상자 전문 에이전트 loan_desk 03절 desk_agents 도구 없음으로 갑니다. 중앙 에이전트에서 바깥 목록, 전문 에이전트에서 안쪽 목록이라고 적힌 화살표가 파란 상자 기록 장치 summarize_run 01절 요청 수 셈 04절 완료 조건으로 모이고, 맨 아래 노란 상자 출력 모인 분야 마지막 답 모델 요청 수 완료 조건으로 이어지는 그림"
FIG1_CAP = "01절 요청 수 셈으로 정한 호출 한도를 04절 중앙 에이전트에 붙이고, 기록 장치가 요청 수와 완료 조건을 모읍니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자 둘은 실행 전에 정한 값이고, 호출 한도 값만 두 실행에서 다릅니다.
파란 상자는 이 노트북에 적은 함수이고, 회색 상자는 create_agent로 만든 에이전트입니다.
기록 장치는 바깥 목록과 안쪽 목록을 함께 읽어 요청 수를 세고, 완료 조건을 봅니다.
이 그림에는 실행 결과의 값을 넣지 않았습니다."""

FIG2 = "05-2-실행-1의-요청-차례"
FIG2_ALT = "위에서 아래로 상자 다섯이 화살표로 이어진 흐름도입니다. 맨 위 초록 상자 실행 1 이번 실행 문의 글 한 줄 호출 한도 2에서, 보라 상자 중앙 에이전트 요청 1 도구 요청 하나 loan_desk, 보라 상자 loan_desk 전문 에이전트 요청 1 안쪽 목록 두 줄, 보라 상자 중앙 에이전트 요청 2 도구 요청 없는 최종 답 차례로 내려갑니다. 맨 아래 노란 상자에는 모델 요청 수 3 중앙 2 + 전문 1 완료 조건 True가 적힌 그림"
FIG2_CAP = "이번 실행 1에서는 중앙 에이전트가 한 번 맡기고 최종 답까지 써서, 모델 요청이 3번이었습니다."
FIG2_READ = """위에서 아래로 실행 1의 요청 차례대로 읽습니다.
보라 상자는 실제로 응답을 받은 모델 요청이고, 노란 상자는 노트북 6절에서 출력한 값입니다.
중앙 에이전트의 요청은 담당 요청을 사이에 두고 두 번이며, 호출 한도 2와 같은 수입니다.
맡긴 모양은 흔들림 확인 다섯 번과 두 커널에서 모두 같았습니다."""

FIG3 = "05-3-호출-한도-2와-1의-두-실행"
FIG3_ALT = "맨 위 회색 상자 두 실행 같음 같은 문의 같은 도구 같은 시스템 메시지 글 필요한 분야 loan_desk에서 나란한 두 칸으로 화살표가 갑니다. 왼쪽 칸 실행 1 호출 한도 2 이번 실행에서는 초록 상자 호출 한도 2가 노란 상자 loan_desk에 한 번 맡김 마지막 응답은 최종 답 모델 요청 수 3 완료 조건 True로 이어집니다. 오른쪽 칸 실행 2 호출 한도 1 이번 실행에서는 초록 상자 호출 한도 1이 노란 상자 loan_desk에 한 번 맡김 마지막 응답은 한도 글 모델 요청 수 2 완료 조건 False로 이어집니다. 두 칸 아래 가운데 노란 상자에는 두 실행 모두 바깥 메시지는 AIMessage ToolMessage AIMessage라고 적혀 있고, 칸과 화살표로 잇지 않은 그림"
FIG3_CAP = "호출 한도 하나만 바꾸자 마지막 응답과 모델 요청 수, 완료 조건이 달라졌습니다."
FIG3_READ = """맨 위 회색 상자는 두 실행에 같게 둔 조건입니다.
왼쪽 칸이 실행 1, 오른쪽 칸이 실행 2이고, 초록 상자가 바꾼 값인 호출 한도입니다.
노란 상자는 노트북 6~8절 출력이고, 맨 아래 상자는 두 실행의 출력에 모두 있던 값입니다.
두 칸 모두 담당에게 한 번 맡겼고, 달라진 것은 마지막 응답 하나입니다."""

ILLU = "05-4-항아리를-내려놓은-기중기와-멈춘-기중기"
ILLU_ALT = "흰 바탕 아래쪽에 회색 부두와 파란 물결선이 있는 그림입니다. 부두 양쪽 끝에 같은 모양의 노란 기중기 둘이 서서 팔을 가운데 쪽으로 뻗고 있습니다. 두 기중기 아래에는 같은 모양의 나무 손수레가 하나씩 있습니다. 왼쪽 수레 위에는 갈색 항아리 하나가 놓여 있고, 왼쪽 기중기의 갈고리는 항아리 바로 위에 비어 있습니다. 오른쪽 기중기의 갈고리는 같은 모양 항아리 하나를 매단 채 허공에 멈춰 있고, 그 아래 오른쪽 수레는 비어 있습니다. 글자·숫자·사람·손·화살표는 없는 그림"
ILLU_CAP = "같은 기중기 둘 가운데 왼쪽은 항아리를 수레에 내려놓았고, 오른쪽은 빈 수레 위에서 항아리를 든 채 멈췄습니다."
ILLU_READ = "부두 양쪽 끝에 같은 모양의 기중기 둘이 팔을 가운데로 뻗고 있습니다. 왼쪽 기중기는 항아리를 수레 위에 내려놓았고, 갈고리는 항아리 위에 비어 있습니다. 오른쪽 기중기는 같은 모양 항아리를 갈고리에 매단 채 멈췄고, 그 아래 수레는 비어 있습니다. 들어 올린 항아리는 두 실행이 모두 받아 둔 담당의 답이고, 수레에 내려놓는 일이 최종 답입니다. 기중기와 수레가 둘인 것은 두 실행의 짝이고, 다른 값과 짝짓지 않습니다."


def figure_ready(name: str) -> bool:
    return (FIGS / (name + ".png")).is_file()


def mermaid_block(name: str, alt: str, caption: str, reading: str) -> str:
    """그림 파일(SVG)과 글이 있을 때만 본문에 넣습니다(그림을 그리기 전 첫 실행 때 빌드가 멈추지 않게)."""
    if not (FIGS / (name + ".svg")).is_file() or not alt or not reading:
        return ""
    return author_01.mermaid_block(name, alt, caption, reading)


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다."""
    if not figure_ready(ILLU) or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


def todays_figure() -> str:
    """노트북 「오늘 볼 그림」 셀 — 조립도 PNG가 있을 때만 첨부를 넣습니다(셀 수는 그림과 무관하게 같음)."""
    if figure_ready(FIG1):
        return "## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ
    return "## 오늘 볼 그림\n\n조립도는 그림을 그린 뒤 이 자리에 붙습니다."


# ---------------------------------------------------------------- 노트북 마크다운
TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 01절 요청 수 셈, 04절 호출 한도, 04절 완료 조건을 자료실 문의 창구 흐름 하나에 모읍니다.
2. 셈으로 정한 호출 한도 2를 붙여 문의 하나를 처리하고, 일이 끝났는지 완료 조건으로 봅니다.
3. 호출 한도 하나만 1로 줄여 다시 처리하고, 두 실행을 견줍니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 모델 요청은 6절에서 3번, 7절에서 2번, 모두 5번입니다.
요금표로 어림한 예상 비용은 두 실행을 합쳐 0.002달러 아래이고, 청구 금액이 아닙니다.
맡기는 모양과 답 글, 토큰 수는 실행마다 달라질 수 있습니다.
걸린 시간은 재지 않았습니다.

읽거나 쓰는 파일은 없고, 체크포인터도 쓰지 않습니다.
앞에서 배운 함수 다섯은 도구 파일 `delegation_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 넷을 설치합니다.
판은 langchain 1.4.0과 langchain-openai 1.6.0입니다.
langgraph 1.2.11과 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**실습 범위** — 이 절은 챕터 끝 실습 절이고 30분 안에 끝나는 분량입니다.
강사와 함께 첫 셀부터 차례로 실행하고, 따로 내는 과제는 없습니다.
01~04절에서 쓴 이름과 Ch 2에서 배운 문법만 씁니다.
실행 셀 하나만 다시 실행하면 모델 요청이 더 나가고, 토큰 수가 달라질 수 있습니다.

실습 폴더 `labs/part6/ch26-delegation`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def model_cells() -> list[dict]:
    """과정 표준 키·모델 셀(nbkit)에 이 절의 결과 읽기(실행일·문장이 달라질 수 있음)와 2절 머리말을 붙입니다."""
    cells = key_and_model_cells("openai:gpt-5.4-mini")
    cells[-1] = md("""**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.
중앙 에이전트와 전문 에이전트가 모두 이 모델 객체 하나를 함께 씁니다.

## 2. 오늘 처리할 문의

자료실 문의 창구에 이용자의 문의가 하나 들어왔다고 합시다.
창구의 중앙 에이전트는 문의를 담당에게 맡기고, 받은 답으로 최종 답을 씁니다.
그런데 모델이 도구를 끝없이 부르면, 요청과 요금도 끝없이 늘어납니다.
그래서 이번 실습은 중앙 에이전트에 호출 한도를 붙이고, 일이 끝났는지 따로 확인합니다.
다음 셀은 오늘 처리할 문의 글과 필요한 분야를 정하고, 출처와 함께 출력합니다.""")
    return cells


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md(todays_figure(), html="skip"),
        md("""## 1. 준비

이번 절은 이 챕터의 실습입니다.
01절 요청 수 셈, 04절 호출 한도, 04절 완료 조건을 문의 창구 흐름 하나에 모읍니다.
첫 셀은 01절과 같은 패키지 넷을 설치하고, 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langchain: 1.4.0`과 `langgraph: 1.2.11`이 보입니다.
네 판 모두 실습 폴더 잠금과 같은 판입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
에이전트를 만드는 함수 `create_agent`는 Ch 21 01절에서 썼습니다.
호출 한도 `ModelCallLimitMiddleware`는 Ch 22 04절에서 썼고, 04절 7절에서도 붙여 보았습니다.
마지막 가져오기 줄은 앞에서 배운 함수 다섯을 도구 파일에서 가져옵니다.
이 절에서 새로 배우는 이름은 없습니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: answered_desks, estimate_cost, is_complete, message_kinds, usage_with_specialists`가 보입니다.
함수 `message_kinds`·`usage_with_specialists`는 01절 노트북 4·5절에서 처음 적었습니다.
함수 `answered_desks`·`is_complete`는 04절 노트북 3·8절에서 처음 적었습니다.
함수 `estimate_cost`는 Ch 6 06절 함수입니다.

04절 함수 둘은 이 절에서 도구 파일로 옮겼고, 설명 주석과 본문은 04절 셀 글 그대로입니다.
인자도 04절 셀과 같아, 04절에서 부른 모양 그대로 부르면 됩니다.

앞에서 배운 함수는 `delegation_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다."""),
    ] + model_cells() + [
        code(QUESTION),
        md("""**결과 읽기** — 출력 줄 `문의 글: 빌린 책의 반납 날짜를 늘리려면 어떻게 하나요?`가 보입니다.
문의 글은 01절 문의 글 그대로이고, 대출 연장 하나만 묻습니다.
그래서 출력 줄 `필요한 분야: ['loan_desk']`처럼, 필요한 분야를 대출 규정 담당 하나로 정했습니다.
두 값은 실행 전에 정했고, 결과를 보고 바꾸지 않았습니다.

## 3. 재료 만들기

재료는 04절과 같은 분야 이름, 규정 글, 전문 에이전트, 도구입니다.
먼저 분야 이름 셋과 세 담당의 교재용 규정 글을 정합니다."""),
        code(RULES),
        md("""**결과 읽기** — 출력 줄 `분야 이름: ['loan_desk', 'interlibrary_desk', 'facility_desk']`가 보입니다.
분야 이름과 세 규정 글은 04절 2절 셀과 같습니다.
규정 글은 모두 교재용으로 만든 글이라 실제 도서관 규정이 아닙니다.

다음 셀은 03절 5절 셀과 같은 코드로, 도구 없는 전문 에이전트 셋을 만듭니다."""),
        code(AGENTS),
        md("""**결과 읽기** — 출력 줄 `전문 에이전트: ['loan_desk', 'interlibrary_desk', 'facility_desk']`가 보입니다.
01절에서 본 것처럼, 도구 없는 전문 에이전트는 한 번 부르면 모델 요청이 1번입니다.

다음 셀은 04절 3절과 같은 도구입니다.
분야 이름을 받아 그 담당에게 넘긴 글을 맡기고, 담당의 마지막 답 글을 내놓습니다.
담당이 받고 쓴 메시지 목록인 안쪽 목록은 기록 목록 `specialist_runs`에 붙습니다."""),
        code(ASK_TOOL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
줄 `@tool`은 01절 3절에서 본 것처럼 아래 함수를 도구로 등록합니다.
기록 목록 `specialist_runs`는 실행 셀마다 빈 목록으로 새로 만듭니다.

다음 셀은 04절 3절과 같은 담당 설명 글과 중앙 에이전트의 시스템 메시지 글을 정합니다.
중앙 에이전트는 호출 한도를 붙여 만들어야 하므로, 이 셀이 아니라 5절 조립 함수에서 만듭니다.
모델이 도는 에이전트에 줄 실행 한도도 이 셀에서 정합니다."""),
        code(CENTRAL_TEXT),
        md("""**결과 읽기** — 출력 줄 `도구 인자: ['desk', 'question']`이 보입니다.
중앙 에이전트의 모델은 이 두 인자를 채워 도구를 요청합니다.
04절 7절에서 본 것처럼, 실행 한도는 그래프의 단계 수를 세고 호출 한도는 모델 요청 수를 셉니다.
실행 한도 10은 두 실행에 같게 주는 값입니다.

## 4. 결과를 볼 기록 장치

실행이 끝난 뒤 일이 끝났는지 보려면, 실행 기록을 읽어 값을 모으는 장치가 있어야 합니다.
먼저 모델 요청 수를 세는 함수입니다.
01절 함수 `usage_with_specialists`는 바깥 목록의 새 메시지와 안쪽 목록의 응답을 함께 셉니다.
그런데 호출 한도가 적어 넣은 응답은 모델 요청이 아니어서, 사용량이 `None`입니다.
01절 6절에서 본 것처럼, 사용량이 `None`인 응답을 넘기면 토큰 수를 꺼내다 멈춥니다."""),
        code(DEF_COUNT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
마지막 응답의 사용량이 `None`이면, 자르기 `[:-1]`로 그 응답만 빼고 셉니다.
자리 `-1`이 맨 끝 자리이니, `[:-1]`은 맨 끝 하나를 뺀 앞부분입니다.

다음 셀은 한 번의 실행에서 모인 분야, 마지막 답, 요청 수, 완료 조건을 모으는 함수입니다.
모인 분야는 04절 함수 `answered_desks`로, 완료 조건은 04절 함수 `is_complete`로 봅니다.
마지막 답이 있는지는 04절 3절과 같은 식으로, 마지막 응답의 사용량과 도구 요청을 봅니다."""),
        code(DEF_SUMMARY),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 안에서 앞 셀의 `count_run_usage`를 부르므로, 앞 셀을 먼저 실행해 두어야 합니다.
토큰 수는 딕셔너리의 키 `usage` 안에 함께 담기고, 8절에서만 출력합니다.

## 5. 조립

이제 앞 절의 기능을 조립 함수 하나로 붙입니다.
조립 함수는 호출 한도 값과 문의 글을 받아, 한도를 붙인 중앙 에이전트를 만들고 문의를 맡깁니다.
호출 한도에는 04절 7절처럼 `exit_behavior="end"`를 주어, 한도에 닿으면 오류 없이 끝나게 합니다.
중앙 에이전트는 04절 3절과 같은 도구와 시스템 메시지 글로 만듭니다.
조립 함수는 이번 실행이 더한 바깥 메시지만 잘라 내놓습니다."""),
        code(DEF_FLOW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 안 주석에 각 줄이 어느 절에서 배운 것인지 적었습니다.
중앙 에이전트를 실행할 때 실행 한도 `limit_config`도 함께 줍니다.

다음 셀은 실행 1에 줄 호출 한도를 01절 셈으로 정합니다.
01절에서 본 셈대로, 중앙 에이전트의 요청 수는 도구를 요청한 응답 수 + 1입니다.
한 분야 문의를 한 번 맡기면, 중앙 요청은 도구를 요청한 응답 1번과 최종 답 1번입니다."""),
        code(LIMIT),
        md("""**결과 읽기** — 출력 줄 `실행 1의 호출 한도: 2`가 보입니다.
이 값은 실행 전에 셈으로 정했고, 결과를 보고 바꾸지 않았습니다.
04절 7절에서 본 대로, 호출 한도는 한도를 붙인 중앙 에이전트의 요청만 셉니다.
그래서 담당의 요청은 한도 값에 넣지 않았습니다.

## 6. 실행 1 · 호출 한도 2

실행 1은 셈으로 정한 호출 한도 2를 붙여 문의를 처리합니다.
실행 전에 예상해 봅니다.
중앙 에이전트가 담당에게 한 번 맡기면, 한도에 닿기 전에 최종 답까지 쓸 것입니다.
그러면 모델 요청은 중앙 2번과 담당 1번으로 3번일 것입니다."""),
        code(RUN1),
        md("""**결과 읽기** — 출력 줄 `이번 실행이 더한 바깥 메시지: ['AIMessage', 'ToolMessage', 'AIMessage']`가 보입니다.
응답 하나 뒤에 도구 메시지 하나가 오고, 마지막에 응답이 하나 더 있습니다.
출력 줄 `전문 에이전트를 부른 횟수: 1`로 담당이 한 번 불렸습니다.

맡기는 모양은 모델이 정해 실행마다 달라질 수 있습니다.
노트북 밖에서 같은 실행을 다섯 번 보냈을 때는 다섯 번 모두 첫 응답에서 한 번 맡겼습니다.

다음 셀은 중앙 에이전트 첫 응답의 도구 요청과, 담당의 안쪽 목록을 봅니다."""),
        code(DETAIL1),
        md("""**결과 읽기** — 출력 줄 `첫 응답의 도구 요청 수: 1`과 `도구 인자의 분야 이름: loan_desk`가 보입니다.
중앙 에이전트의 모델이 도구 인자에 대출 규정 담당의 이름을 적었습니다.
출력 줄 `안쪽 목록의 줄 수: 2`는 01절에서 본 것처럼, 넘긴 글 한 줄과 담당의 답 한 줄입니다.

다음 셀은 앞에서 만든 기록 장치로 실행 1을 모읍니다."""),
        code(SUM1),
        md("""**결과 읽기** — 출력 줄 `담당 답이 모인 분야: ['loan_desk']`와 `마지막 응답이 도구 요청 없는 모델 응답인가: True`가 보입니다.
출력 줄 `모델 요청 수(중앙 + 전문): 3`은 예상대로 중앙 2번과 담당 1번입니다.
출력 줄 `완료 조건: True`로, 필요한 분야의 답이 모였고 최종 답도 있습니다.
호출 한도는 모델 요청 전에 센 수를 보므로, 둘째 요청 전의 수 1은 한도 2에 닿지 않았습니다.
이 실행은 중앙 에이전트의 모델이 도구 요청 없는 응답을 골라 끝났습니다.

## 7. 실행 2 · 호출 한도 1

값 하나만 바꿔 봅니다.
바꿀 값은 호출 한도이고, 2를 1로 줄입니다.
문의 글, 필요한 분야, 도구, 시스템 메시지 글, 실행 한도는 실행 1과 같습니다.
실행 전에 예상해 봅니다.
첫 요청에서 담당에게 맡긴 뒤, 최종 답을 쓸 둘째 요청 전에 한도에 닿아 끝날 것입니다."""),
        code(RUN2),
        md("""**결과 읽기** — 출력 줄 `이번 실행이 더한 바깥 메시지: ['AIMessage', 'ToolMessage', 'AIMessage']`가 보입니다.
바깥 메시지의 종류와 수는 실행 1과 같습니다.
출력 줄 `전문 에이전트를 부른 횟수: 1`로, 이번에도 담당은 한 번 불렸습니다.

다음 셀은 마지막 응답이 무엇인지 봅니다."""),
        code(DETAIL2),
        md("""**결과 읽기** — 출력 줄 `마지막 응답 글: Model call limits exceeded: run limit (1/1)`은 호출 한도가 적어 넣은 글입니다.
출력 줄 `마지막 응답의 사용량: None`으로, 이 응답은 모델 요청으로 받은 것이 아닙니다.
출력 줄 `첫 응답의 도구 요청 수: 1`이라, 첫 응답의 도구 요청대로 담당은 실행되었습니다.
바깥 목록의 종류만 보면 실행 1과 같지만, 마지막 응답이 다릅니다.

다음 셀은 같은 기록 장치로 실행 2를 모읍니다."""),
        code(SUM2),
        md("""**결과 읽기** — 출력 줄 `담당 답이 모인 분야: ['loan_desk']`는 실행 1과 같습니다.
출력 줄 `마지막 응답이 도구 요청 없는 모델 응답인가: False`와 `완료 조건: False`가 보입니다.
출력 줄 `모델 요청 수(중앙 + 전문): 2`는 중앙 1번과 담당 1번입니다.
담당의 답은 받아 두었지만, 그 답으로 최종 답을 쓰는 요청이 나가지 못했습니다.
한도에 닿아 오류 없이 끝났어도, 완료 조건으로 보면 일은 끝나지 않았습니다.

## 8. 두 실행 견주기

두 실행을 한 표로 놓고, 한도 값을 바꾼 탓으로 달라진 값을 봅니다.
다음 셀은 두 실행의 호출 한도, 모인 분야, 마지막 답, 요청 수, 완료 조건을 한 줄씩 출력합니다."""),
        code(COMPARE),
        md("""**결과 읽기** — 라벨 줄 `실행 | 호출 한도 | 모인 분야 | 마지막 답 | 모델 요청 수 | 완료 조건` 아래 두 줄이 두 실행입니다.
줄 `실행 1 | 2 | ['loan_desk'] | True | 3 | True`와 `실행 2 | 1 | ['loan_desk'] | False | 2 | False`가 보입니다.
모인 분야는 같고, 마지막 답과 모델 요청 수, 완료 조건이 달라졌습니다.
두 실행의 요청 수 차이 1은 최종 답을 쓰는 중앙 요청 하나입니다.

다음 셀은 두 실행의 토큰 수와 예상 비용을 봅니다.
예상 비용은 Ch 6 06절 함수 `estimate_cost`로 요금표에서 어림한 값이고, 청구 금액이 아닙니다."""),
        code(COST),
        md("""**결과 읽기** — 라벨 줄 `실행 | 입력 토큰 | 출력 토큰 | 예상 비용(달러)` 아래 두 줄이 두 실행입니다.
토큰 수와 예상 비용은 실행마다 달라질 수 있어, 이 절의 결론에 쓰지 않습니다.

이번 실행에서는 라벨 줄 아래가 `실행 1 | 796 | 112 | 0.001101`와 `실행 2 | 426 | 71 | 0.000639`였습니다.
이번 실행에서는 실행 2의 입력 토큰과 출력 토큰이 모두 실행 1보다 적었습니다.

## 정리

1. 01절 요청 수 셈, 04절 호출 한도, 04절 완료 조건을 자료실 문의 창구 흐름 하나에 모았습니다.
2. 한 번 맡기면 중앙 요청은 2번이라, 셈으로 정한 호출 한도 2에서는 최종 답까지 써서 완료 조건을 채웠습니다.
3. 호출 한도를 1로 줄이자 담당의 답을 받고도 최종 답 전에 끝나, 완료 조건을 채우지 못했습니다.

이 절로 Ch 26이 끝납니다.
Ch 27 01절에서는 긴 작업에 자주 쓰는 기능을 미리 묶어 둔 DeepAgents를 봅니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
L_01 = "01-Subagent-도구-위임.html"
L_02 = "02-Handoff-상태-전환.html"
L_03 = "03-Router-분류와-병렬-실행.html"
L_04 = "04-호출-수-비용-종료-조건-비교.html"
L_CH06_06 = "../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html"
L_CH20_03 = "../../part5/ch20-tool-node/03-recursion-limit과-명시적-종료.html"
L_CH22_04 = "../ch22-middleware/04-호출-한도와-재시도-폴백.html"
L_CH27_01 = "../ch27-deepagents/01-하네스와-일곱-기능.html"


def link(href: str, label: str) -> str:
    return '<a href="' + href + '">' + label + "</a>"


LEARNED_ROWS = [
    (link(L_01, "01절"), "중앙 에이전트가 도구로 전문 에이전트에게 일을 맡기는 서브에이전트, 요청 수 셈(중앙 = 도구를 요청한 응답 수 + 1, 전문 = 부른 횟수), 함수 <code>message_kinds</code>·<code>usage_with_specialists</code>(도구 파일)",
     "2절 문의 글, 5절 실행 1의 호출 한도 2, 기록 장치의 요청 수, 실행 셀의 바깥 메시지 종류"),
    (link(L_03, "03절"), "도구 없는 전문 에이전트 셋 <code>desk_agents</code>와 분야 이름 셋", "3절 재료"),
    (link(L_04, "04절"), "분야 이름을 받는 도구 <code>ask_desk_agent</code>와 중앙 에이전트, 호출 한도 <code>ModelCallLimitMiddleware</code>, 완료 조건 함수 <code>answered_desks</code>·<code>is_complete</code>(이 절에서 도구 파일로 옮김)",
     "3절 도구, 5절 조립 함수, 두 실행의 한도 값, 기록 장치의 완료 조건"),
    (link(L_CH20_03, "Ch 20 03절") + "·" + link(L_CH22_04, "Ch 22 04절"), "그래프 단계 수를 세는 실행 한도, 모델 요청 수를 세는 호출 한도",
     "두 실행에 같게 준 실행 한도 10, 조립 함수의 호출 한도"),
    (link(L_CH06_06, "Ch 6 06절"), "요금표로 어림한 예상 비용, 함수 <code>estimate_cost</code>(도구 파일)", "8절 토큰과 예상 비용 표"),
]

RESULT_ROWS = [
    ("실행 1", "2", "1", "중앙 에이전트의 최종 답", "3(중앙 2 + 전문 1)", "True"),
    ("실행 2", "1", "1", "호출 한도가 적어 넣은 글", "2(중앙 1 + 전문 1)", "False"),
]

TOKEN_ROWS = [
    ("실행 1", "796", "112", "0.001101"),
    ("실행 2", "426", "71", "0.000639"),
]

LOOK_B5 = "노트북 6절에서 <code>모델 요청 수(중앙 + 전문): 3</code>과 <code>완료 조건: True</code>를 봅니다. 7절에서 <code>마지막 응답의 사용량: None</code>과 <code>완료 조건: False</code>를 확인합니다. 맡기는 모양은 모델이 정하므로, 다시 실행하면 달라질 수 있습니다."
LOOK_B6 = "노트북 8절 첫 표에서 두 줄의 모인 분야가 같고, 마지막 답과 모델 요청 수, 완료 조건만 다른지 봅니다. 교재 출력의 토큰 수와 예상 비용은 다시 실행하면 달라질 수 있어, 이 절의 결론에 쓰지 않았습니다."
RUNS_B6 = "새 커널로 두 번 실행해 견주자, 스물한 셀의 출력이 두 번 모두 같았습니다. 토큰 수와 예상 비용이 찍힌 8절 둘째 셀도 이번 두 번에서는 같았습니다. 노트북 밖 확인에서는 실행 1의 출력 토큰이 102와 112로 달랐으므로, 토큰과 비용은 결론에 쓰지 않았습니다."


def src_html() -> str:
    learned = table_html(["절", "배운 것", "실습에서 쓰는 곳"], LEARNED_ROWS)
    results = table_html(["실행", "호출 한도", "담당을 부른 횟수", "마지막 응답", "모델 요청 수", "완료 조건"], RESULT_ROWS)
    tokens = table_html(["실행", "입력 토큰(교재 출력)", "출력 토큰(교재 출력)", "예상 비용(교재 출력, 달러)"], TOKEN_ROWS)
    return """<!--meta: 실습 30분 | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 0 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>요청 수 셈·호출 한도·완료 조건을 한 흐름에 모아, 자료실 문의 하나를 처리할 수 있습니다.</li>
<li>01절 요청 수 셈으로 중앙 에이전트의 호출 한도 값을 정할 수 있습니다.</li>
<li>한도 값 하나를 바꾼 두 실행을 견주어, 한도로 멈춘 실행과 일이 끝난 실행을 완료 조건으로 가를 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>이 챕터에서는 위임 구조를 절마다 따로 익혔습니다. """ + link(L_01, "01절") + """은 중앙 에이전트가 도구로 전문 에이전트에게 일을 맡기고, 요청 수를 셈으로 세었습니다. """ + link(L_04, "04절") + """은 분야 이름을 받는 도구 하나로 맡기는 중앙 에이전트를 만들고, 호출 한도와 완료 조건을 적었습니다. 실제 문의 창구에서는 이 일들이 한 흐름 안에서 함께 일어납니다.</p>
<p>이번 실습은 자료실 문의 하나를 처리하는 중앙 에이전트에 호출 한도를 붙이고, 한도 값을 01절 셈으로 정합니다. 그다음 한도 값 하나만 줄여 다시 처리합니다. """ + link(L_04, "04절") + """은 한도를 붙이지 않은 3절 실행과 한도 1을 붙인 7절 실행을 견주었습니다.</p>
<p>실행 2의 한도 1은 04절 7절과 같은 값입니다. 04절 7절은 두 분야 문의에 한도 1을 붙여, 최종 답이 빠지는 끝 모양을 이미 보였습니다. 이번에 새로 볼 것은 요청 수 셈으로 정한 한도 2면 완료 조건이 <code>True</code>이고, 하나 모자라면 <code>False</code>가 되는지입니다. 셈과 한도와 완료 조건이 한 흐름에서 이어지는지를 봅니다.</p>
<p>이번 절은 이 챕터의 실습입니다. 01~04절에서 쓴 이름과 Ch 2에서 배운 문법만 쓰고, 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p>
<p><strong>이 절의 질문</strong> — 호출 한도를 요청 수 셈으로 정하면, 문의 하나를 끝까지 처리할 수 있을까요? 한도를 하나 줄이면, 실행은 어디서 멈추고 완료 조건은 무엇을 내놓을까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>이번 실습은 아래 절에서 배운 이름을 그대로 씁니다. 함수는 도구 파일 <code>delegation_tools.py</code>에서 가져오고, 도구·조립 함수·기록 장치는 노트북에 적습니다.</p>
""" + learned + """
<p>붙인 기능은 01절 서브에이전트 모양과 요청 수 셈, 04절 호출 한도, 04절 완료 조건 셋입니다. 셋이 모두 흐름 안에서 일하도록, 호출 한도 값을 01절 셈으로 정하고 두 실행 모두 완료 조건으로 확인했습니다. 요청 수 셈은 실행 1의 한도 값과 기록 장치의 요청 수에 쓰이고, 완료 조건은 두 실행의 결과를 가릅니다.</p>
<p>""" + link(L_02, "02절") + """ 핸드오프는 붙이지 않았습니다. """ + link(L_04, "04절") + """ 4절에서 한 응답에 넘기기 요청 둘이 나오자, 받은 담당의 요청이 거절되어 실행이 멈췄기 때문입니다. """ + link(L_03, "03절") + """ 분류 모델도 붙이지 않았습니다. 분류 요청이 하나 더 들어 두 실행의 요청이 3~5번을 넘고, 노트북 밖에서 본 까닭은 아래 주의할 점에 적었습니다. 04절 핑퐁 그래프와 체크포인터는 04절 실험을 되풀이하게 되어 뺐습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절부터 항구의 배로 위임 구조를 보았습니다. 이번에는 부두에 같은 모양의 기중기 둘이 서 있습니다. 두 기중기는 똑같이 항아리 하나씩을 들어 올렸습니다. 왼쪽 기중기는 항아리를 수레 위에 내려놓았고, 오른쪽 기중기는 수레 위에서 항아리를 든 채 멈췄습니다.</p>
""" + illustration_block() + """<p>기중기가 중앙 에이전트이고, 들어 올린 항아리가 담당에게서 받은 답입니다. 항아리를 수레에 내려놓는 일이 문의한 사람에게 최종 답을 건네는 일입니다. 오른쪽 기중기는 마지막 한 번을 움직이지 못하고 멈췄고, 호출 한도가 하나 모자란 실행 2와 같습니다.</p><p>비유와 다른 점이 있습니다. 멈춘 기중기는 나중에 다시 움직일 수 있지만, 한도에 닿은 실행은 그 자리에서 끝납니다. 또 그림에는 담당이 항아리를 가져오는 장면이 없고, 실행에서는 담당의 모델 요청이 따로 나갑니다.</p>
<h3>실습 조립의 구성</h3>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>호출 한도를 요청 수 셈으로 정하기</h3><p>호출 한도는 한도를 붙인 에이전트가 한 번 실행에서 보낼 수 있는 모델 요청 수입니다. 한도를 너무 크게 두면 요금 사고를 막지 못하고, 너무 작게 두면 일을 끝내기 전에 멈춥니다. 01절 셈으로, 최종 답까지 쓰는 실행에서 중앙 에이전트의 요청 수는 도구를 요청한 응답 수 + 1입니다. 한 분야 문의를 한 번 맡기면 1 + 1로 2번이니, 이 절은 실행 1의 한도를 2로 둡니다.</p><p>""" + link(L_04, "04절") + """ 7절에서 본 대로, 호출 한도는 모델 요청 전에 센 수를 봅니다. 한도 2에서는 둘째 요청 전의 수가 1이라 요청이 나가고, 한도 1에서는 둘째 요청 전에 끝납니다. 담당의 요청은 도구 안에서 따로 나가므로 이 한도에 세지 않습니다. 그래서 한 번 맡기는 실행이면 한도 1에서도 담당은 불리고, 빠지는 것은 중앙 에이전트의 최종 답입니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 오늘 처리할 문의 글과 필요한 분야를 정합니다. 04절과 같은 재료를 만들고, 요청 수와 완료 조건을 모으는 기록 장치 함수 둘을 적습니다. 조립 함수가 호출 한도를 붙인 중앙 에이전트를 만들고, 실행 1은 한도 2, 실행 2는 한도 1로 같은 문의를 처리합니다. 8절에서 두 실행을 견줍니다.</p><p>실제 OpenAI 모델 <code>gpt-5.4-mini</code>를 temperature 0으로 부릅니다. 모델 요청은 6절에서 3번, 7절에서 2번, 모두 5번입니다. 요금표로 어림한 예상 비용은 0.002달러 아래이고, 청구 금액이 아닙니다. 읽거나 쓰는 파일은 없고, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
<h3>실행 1의 실제 순서</h3>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>두 실행은 문의 글·필요한 분야·도구·시스템 메시지 글이 같고, 호출 한도만 실행 2에서 달랐습니다. 아래 표는 노트북 6~8절 출력에서 코드가 정하는 값과, 모델이 맡긴 모양을 모은 것입니다.</p>
""" + results + """
<p>두 실행 모두 중앙 에이전트는 첫 응답에서 대출 규정 담당에게 한 번 맡겼습니다. 이 모양은 흔들림 확인 다섯 번과 두 커널에서 모두 같았습니다. 실행 1은 한도와 같은 2번의 중앙 요청으로 최종 답까지 썼습니다. 실행 2는 담당의 답을 받은 뒤, 최종 답을 쓸 요청 전에 한도에 닿아 끝났습니다.</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>두 실행의 바깥 메시지는 종류와 수가 같았고, 모인 분야도 같았습니다. 달라진 것은 마지막 응답 하나이고, 그 차이가 완료 조건을 True와 False로 갈랐습니다. 실행 2는 오류 없이 끝났지만, 문의한 사람에게 건넬 최종 답이 없습니다. 멈춘 까닭만 보고는 일이 끝났는지 가릴 수 없다는 04절 8절의 말을, 한 흐름 안에서 다시 본 셈입니다.</p><p>요청 수의 차이 1은 최종 답을 쓰는 중앙 요청 하나였습니다. 한 번 맡기는 실행에서 중앙 요청은 셈대로 2번이 필요하고, 한도가 그보다 작으면 최종 답이 빠집니다. 문의가 두 분야를 묻거나 모델이 응답 둘에 나눠 맡기면, 셈이 달라집니다. 응답 둘에 나눠 한 번씩 맡기면 중앙 요청은 3번이 필요해, 한도 2로는 모자랍니다.</p>
<p>아래 표는 두 실행의 교재 출력 토큰과 예상 비용입니다. 토큰 수와 예상 비용은 다시 실행하면 달라질 수 있습니다.</p>
""" + tokens + """
<p>""" + RUNS_B6 + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>문의 글은 01절 문의 글 그대로입니다. 필요한 분야와 실행 1의 호출 한도 2는 실행 전에 정했습니다. 필요한 분야는 문의 글이 묻는 것을 보고 정한 값이고, 모델이 고른 값이 아닙니다. 한도 2는 흐름을 보여 주려고 01절 셈으로 정한 예입니다.</li><li>노트북을 쓰기 전에 문의와 판단 규칙을 적어 두고, 노트북 밖에서 두 설정을 다섯 번씩 보냈습니다. 열 번 모두 중앙 에이전트가 첫 응답에서 대출 규정 담당에게 한 번 맡겼습니다. 그래도 같은 요청이 실행한 때에 따라 달라질 수 있습니다.</li><li>03절 분류 모델을 창구 맨 앞에 두는 흐름은, 노트북 밖 확인에서 맡을 분야가 없는 문의도 시설 담당으로 분류되어 뺐습니다.</li><li>분류 모델이 고른 분야를 완료 조건의 필요한 분야로 쓸 때는 조심해야 합니다. 위 확인에서는 우산을 두고 온 문의도 시설 담당의 답이 모여 완료 조건을 채웠습니다. 필요한 분야를 무엇으로 정하느냐에 따라, 완료 조건이 True여도 문의에 답하지 못했을 수 있습니다.</li><li>호출 한도는 한도를 붙인 중앙 에이전트의 요청만 셉니다. 담당 에이전트의 요청까지 묶으려면 담당에도 한도를 따로 붙여야 하고, 이 절에서는 실행하지 않았습니다.</li><li>한도 1의 실행은 오류 없이 끝나서, 마지막 응답 글을 읽지 않으면 멈춘 것을 놓치기 쉽습니다. 이 절은 마지막 응답의 사용량과 도구 요청으로 최종 답이 있는지를 따로 보았습니다.</li><li>한도를 셈보다 크게 둔 실행과, 두 분야 문의에 한도 2를 붙인 실행은 이번에 실행하지 않았습니다. 이 노트북의 <code>assert</code>는 키 확인 셀 하나뿐이고, 모델이 맡긴 모양과 완료 조건에는 걸지 않았습니다.</li><li>토큰 수와 예상 비용은 2026-09-17 과정 요금표로 어림했고, 청구 금액이 아닙니다. 걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>01절 요청 수 셈, 04절 호출 한도, 04절 완료 조건을 자료실 문의 창구 흐름 하나에 모았습니다.</li><li>한 번 맡기면 중앙 요청은 2번이라, 셈으로 정한 호출 한도 2에서는 최종 답까지 써서 완료 조건을 채웠습니다.</li><li>호출 한도를 1로 줄이자 담당의 답을 받고도 최종 답 전에 끝나, 완료 조건을 채우지 못했습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 26이 끝납니다. """ + link(L_CH27_01, "Ch 27 01절") + """에서는 긴 작업에 자주 쓰는 기능을 미리 묶어 둔 DeepAgents를 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. [하] 실행 1의 호출 한도를 2로 정한 까닭은 무엇인가요?</p><p class="quiz-a">01절 셈으로, 최종 답까지 쓰는 실행에서 중앙 에이전트의 요청 수는 도구를 요청한 응답 수 + 1입니다. 한 분야 문의를 한 번 맡기면 1 + 1로 2번이라, 한도를 2로 두었습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">2. [중] 실행 2에서 담당은 불렸는데 완료 조건이 False였습니다. 왜 그런가요?</p><p class="quiz-a">호출 한도는 중앙 에이전트의 요청만 세서, 첫 요청의 도구 요청대로 담당은 실행되었습니다. 그러나 최종 답을 쓸 둘째 요청 전에 한도에 닿아, 마지막 응답이 한도 글이 되었습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">3. [중] 두 실행의 모델 요청 수가 3과 2로 1 차이 난 까닭을 셈으로 설명해 보세요.</p><p class="quiz-a">두 실행 모두 담당 요청은 1번이었습니다. 중앙 요청은 실행 1이 도구를 요청한 응답 1번과 최종 답 1번으로 2번이고, 실행 2는 최종 답이 빠져 1번이었습니다. 틀렸다면 노트북 8절 첫 표를 다시 봅니다.</p><p class="quiz-q">4. [상] 문의가 두 분야를 묻는다면, 실행 1의 호출 한도 2로 충분할까요?</p><p class="quiz-a">한 응답에서 두 담당에게 함께 맡기면 중앙 요청은 1 + 1로 2번이라 충분합니다. 응답 둘에 나눠 한 번씩 맡기면 2 + 1로 3번이 필요해, 한도 2로는 최종 답 전에 멈춥니다. 04절 3절의 두 분야 문의는 한 응답에서 두 담당에게 맡겼지만, 이 절은 두 분야 문의에 한도를 붙여 실행하지 않았습니다. 틀렸다면 노트북 5절과 04절 노트북 3절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li>01절 — 서브에이전트와 요청 수 셈, 함수 <code>message_kinds</code>·<code>usage_with_specialists</code>.</li><li>04절 — 분야 이름을 받는 도구, 호출 한도, 완료 조건, 함수 <code>answered_desks</code>·<code>is_complete</code>.</li><li>Ch 22 04절 — 호출 한도 <code>ModelCallLimitMiddleware</code>와 인자 <code>exit_behavior</code>.</li><li><div><a href="https://docs.langchain.com/oss/python/langchain/multi-agent/subagents">LangChain Subagents</a></div>04절 참고 자료와 같은 문서입니다. 담당 이름을 인자로 받는 도구 하나로 보내는 모양을 적습니다.</li><li>langchain 1.4.0 소스 <code>agents/middleware/model_call_limit.py</code> 168~208행과 236~250행은 호출 한도가 요청 수를 보고 늘리는 자리입니다.</li><li>기준 버전은 노트북 1절 첫 셀에서 설치한 패키지 넷의 판입니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    check_tools()
    check_same_as_probe()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "delegation_tools.py").write_text(TOOLS_05, encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        write_tools()
        path = write_notebook(LAB, "05", SLUG, "experiment", cells())
        print("wrote", path)
