"""Ch 29 05절(챕터 끝 실습 절) 생성기 (QUALITY-UPGRADE.md §7-2·§2·§2-7·§3·§4·§6).

사용:
  python3 -B author_05.py                  → 도구 파일(가드) + 노트북 + _src 본문을 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_05.py --src-only       → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_05.py --tools-copy DIR → 디스크의 도구 파일을 DIR에 복사한다(새 커널 사본 B 실행용)
  python3 -B author_05.py --try DIR        → 노트북과 이 판 도구 파일을 DIR에만 쓴다(실습 폴더를 건드리지 않는 시험 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
새로 만든 절이라 qa/upgrade/before/ 에 원본이 없다. **experiment 형식**(chapter.json), lesson_part 없음.
슬러그 `05-Agent-평가-실습`(규격 §7-2 `{NN+1}-{챕터 이름}-실습` — 챕터 짧은 이름 「Agent 평가」, `_notebook/build_index.py` 62행 ·
선례 `06-Agent-개요-실습`·`07-create-agent-실습`·`05-위임-구조-실습`·`09-DeepAgents-실습`·`06-MCP-실습`).

## 결정 1 — 붙인 앞 절 기능 셋 (handoff 「§04 → 실습(05)」 3·4번 안 B, 05-probe.md §0)

03절 평가받는 에이전트(@tool 둘 — 03 셀 글 그대로 · create_agent · 호출 한도 · 실행 한도 20 · show_messages · sum_usage ·
셈 「요청 수 = 도구를 요청한 응답 수 + 1」 — 두 실행) + 02절 네 모드와 도구별 덮어쓰기(four_modes · search_documents ignore — 두 궤적 판정) +
04절 공통 칸(칸 여섯 · show_row — 두 실행을 한 표에 · 점수와 셈으로 실행 수 세기, 04 5절 모양).
실행 1 = 호출 한도 4(03과 같은 값) · 실행 2 = 호출 한도 2(값 하나 — 03 셈으로 드는 요청 3보다 하나 모자람).
앞 절 값 바꿔 보기(01 답 글 · 03 답 글 · 04 백분위)와 다른 값. 한도에 닿은 끝 모양은 Ch 22 04 · 사용량 None은 Ch 26 04·05가 이미 보임 →
b2 「새로 볼 것」은 이 챕터의 평가(네 모드 · 공통 칸 · 셈)가 그 실행을 어떻게 판정하는지로 한정(Ch 26 B-7 교훈).
뺀 것: 03 평가 모델(두 실행에 한 번씩이면 요청 7 — §7-2 3~5를 넘음) · 01 최종 답 평가(실행 1 답 글이 기준 답과 글자까지 같은지는 모델 글이라 흔들림) ·
04 95 백분위수(줄 둘이면 늘 가장 큰 값) · 03 궤적 글(_format_inputs — 평가 모델을 부르지 않아 쓸 곳 없음).

## 결정 2 — 흔들림 먼저 확인 (qa/upgrade/05-probe.md)

§0 03:28:07Z(본문 03:27:54Z) → 첫 요청 03:28:14Z. 5회차 × (실행 1 = 3 + 실행 2 = 2) = 25요청, 모든 칸 5/5 같음 → 후보 1(한도 4 → 2) 그대로.

## 결정 3 — 결론은 셈·모드 판정·공통 칸의 세는 칸

실행 1 요청 3 · 도구를 요청한 응답 2 · 셈 True / 실행 2 요청 2 · 2 · 셈 False(끝 메시지 `Model call limits exceeded: run limit (2/2)`, 사용량 None) ·
두 실행 모두 네 모드 True · 점수 1.0 · 「점수가 1.0인 실행 2 | 셈이 맞은 실행 1」. 모델 판단 값은 「노트북 밖 다섯 번과 새 커널 두 번에서 모두」.
답 글·토큰 수는 둘째 단락·b6 표·b7에만([[…]] 자리 표시 — 생성기에 글자 그대로, mdpatch.py가 생성기까지 고침). assert는 키 셀뿐.

## 결정 4 — 도구 파일 eval_tools.py 05절 판 (규격 §2-7, handoff 「§04 → 실습(05)」 5번)

04판(`223881ec…`) 뒤에 04절 노트북 셀 show_row를 셀의 주석과 본문 글자 그대로 더한다(주석 `# Ch 29 04절에서 배웠습니다 — …`).
가져오기 줄은 더하지 않는다(show_row는 print만 씀) → 01~04 노트북 설치 셀 변경 없음, 05 설치 셀에 langchain==1.4.0 있음.
대조 사슬: author_04.check_tools()(안에서 03·02·01까지) → 04판 해시 고정 → strip_later_imports(05판).startswith(strip_later_imports(04판)) →
셀 글 해시·04 노트북 디스크 셀·AST. 쓰기 가드: 없거나 01~04판·이 판일 때만 쓰고 더 긴 판은 skip. 01~04 생성기가 이 판을 skip하는지 판정만 흉내 낸다.
이 절이 처음 적은 함수(노트북에): 조립 run_agent(limit) · 셈 count_asked(messages) · 끝 메시지 빼기 model_part(messages) · 공통 칸 한 줄 run_row(name, messages, usage, score)
(run_agent는 노트북 전역 이름을 읽고, 넷 모두 이 절에서만 써서 노트북에 둠 — Ch 27 09·Ch 28 06 선례).

## 모델 요청

노트북 한 번 **5번**(실행 1 = 3 · 실행 2 = 2, 호출 한도 4 + 2 = 상한 6). 평가 모델 0. 디스크 쓰기 0.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`else`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`range`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`.items`·`+=`·기본값 매개변수·반환 힌트·대입 풀기·별표 풀기·`while`·`try`·세미콜론·
`isinstance`·클래스·`async`. 데코레이터는 @tool 둘(03 셀 글 — 매개변수 `: str`). 호출 깊이 2 이하.
01~04 노트북·도구 파일에 없는 내장 이름·속성·키워드 인자·연산자·가져오기 0(/tmp/ch29-05/tools/inventory29.py).
"""
from __future__ import annotations

import ast
import hashlib
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(HERE))
import author_01  # noqa: E402  본문 도우미·도구 파일 01판·strip_later_imports
import author_02  # noqa: E402  도구 파일 02판 가드
import author_03  # noqa: E402  03절 셀 글(설치·기준 궤적·도구 둘)·노트북 코드 셀 읽기·도구 파일 03판 가드
import author_04  # noqa: E402  04절 셀 글(show_row)·도구 파일 04판과 대조 사슬
from nbkit import RUN_DATE, code, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch29-agent-evaluation/notebooks"
FIGS = ROOT / "textbook/part6/ch29-agent-evaluation/figures"
SLUG = "05-Agent-평가-실습"
TITLE_TEXT = "Agent 평가 실습: 호출 한도를 줄인 실행을 궤적과 운영 지표로 견주기"
SRC = ROOT / "textbook/part6/ch29-agent-evaluation/_src" / (SLUG + ".html")
TOOLS_PATH = LAB / "eval_tools.py"
NB03 = LAB / (author_03.SLUG + ".ipynb")
NB04 = LAB / (author_04.SLUG + ".ipynb")
PROBE = HERE / "probe/probe05.py"
html_text = author_01.html_text
table_html = author_01.table_html


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- 도구 파일 eval_tools.py (05절 판)
NOTE_04 = "Ch 29 04절에서 배웠습니다 — 04절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다"
DEF_SHOW = author_04.DEF_SHOW
DEF_SHOW_SHA = "4ea696a3b60ae71b49c2daededc3a6aa552bae5a869bbd2569cb01783e3b6ec5"
TOOL_ORDER = author_04.TOOL_ORDER + ["show_row"]
# 전체 마감(2026-09-30)에서 도구 파일 머리 설명 줄만 고쳐 04판 223881ec… → 14dc76c9…(함수 본문 같음)
TOOLS_04_SHA = "14dc76c9b76c899a254eaa767c9f301acd538f7e685d4b310592ba0f67e6994b"
TOOLS = author_04.TOOLS + "\n\n# " + NOTE_04 + "\n" + DEF_SHOW + "\n"


def check_tools() -> None:
    """05절 판이 04절 판(대조 사슬)으로 시작하고, 더한 함수 show_row가 04 노트북 셀과 글자·AST 모두 같은지 봅니다."""
    author_04.check_tools()
    strip = author_01.strip_later_imports
    assert sha(author_04.TOOLS) == TOOLS_04_SHA, "04판이 기록 해시와 다릅니다"
    assert strip(TOOLS).startswith(strip(author_04.TOOLS)), "05절 판이 04절 판으로 시작하지 않습니다"
    assert TOOLS.startswith(author_04.TOOLS)
    tree = ast.parse(TOOLS)
    names = []
    imports = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
    assert names == TOOL_ORDER, names
    assert imports == author_04.IMPORT_LINES, imports
    # 04절 셀 show_row: 고정 해시 · 04 노트북 디스크 셀 · AST
    assert sha(DEF_SHOW) == DEF_SHOW_SHA, "show_row 셀 글이 고정 해시와 다릅니다"
    assert DEF_SHOW in author_03.notebook_code_sources(NB04), "show_row가 04절 노트북 디스크 셀과 다릅니다"
    assert ("# " + NOTE_04 + "\n" + DEF_SHOW + "\n") in TOOLS
    mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "show_row"]
    theirs = [ast.dump(n) for n in ast.parse(DEF_SHOW).body if isinstance(n, ast.FunctionDef)]
    assert mine == theirs and len(mine) == 1
    # 앞 절 생성기의 쓰기 가드가 이 판을 덮어쓰지 않는지(판정만 흉내 — 실행하지 않음)
    assert author_04.later_version(TOOLS), "04 생성기가 이 판을 skip하지 않습니다"
    assert author_03.later_version(TOOLS), "03 생성기가 이 판을 skip하지 않습니다"
    assert author_02.later_version(TOOLS), "02 생성기가 이 판을 skip하지 않습니다"
    assert strip(TOOLS).startswith(author_01.TOOLS) and TOOLS != author_01.TOOLS, "01 생성기가 이 판을 skip하지 않습니다"


def later_version(current: str) -> bool:
    """뒤 절이 함수·가져오기 줄을 더한 판인지: 가져오기 줄을 뺀 글이 이 판(가져오기 줄을 뺀 글)으로 시작하면 참."""
    plain = author_01.strip_later_imports(current)
    return current != TOOLS and plain.startswith(author_01.strip_later_imports(TOOLS))


def write_tools(path: Path) -> None:
    current = ""
    if path.is_file():
        current = path.read_text(encoding="utf-8")
    if current == TOOLS:
        print("same", path)
    elif current in ("", author_01.TOOLS, author_02.TOOLS, author_03.TOOLS, author_04.TOOLS):
        path.write_text(TOOLS, encoding="utf-8")
        print("wrote", path)
    elif later_version(current):
        print("skip", path, "(뒤 판이 함수를 더한 판 — 덮어쓰지 않음)")
    else:
        raise AssertionError("도구 파일이 01~05절 판이 아닙니다")


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = author_03.INSTALL

IMPORT_NAMES = "called_tool_names, four_modes, make_trajectory, show_messages, show_row, sum_usage, tool_call_names"
IMPORTS = r'''# 궤적을 맞춰 보는 평가 함수를 만드는 함수와, 에이전트·호출 한도·모델·메시지·도구 이름을 가져옵니다(Ch 6·13·19·21·22)
from agentevals.trajectory.match import create_trajectory_match_evaluator
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain.tools import tool
# 앞에서 배운 함수는 도구 파일에서 가져옵니다
from eval_tools import ''' + IMPORT_NAMES + '''

print("도구 파일에서 가져온 함수:", "''' + IMPORT_NAMES + '''")'''

DATA = r'''# 질문과 기준 답, 도구마다 돌아올 결과 글을 정합니다(03절 2절과 같은 값 — 아래 도구 함수도 이 글을 내놓음)
question = "일반 도서는 며칠 동안 빌릴 수 있나요?"
reference_answer = "일반 도서는 14일 동안 빌릴 수 있습니다."
tool_results = {
    "search_documents": "[LIB-001] 일반 도서는 14일 동안 대출할 수 있습니다. 예약자가 없으면 한 번 연장할 수 있습니다.",
    "check_source": "LIB-001 문서가 있습니다. 제목: 도서 대출 기간",
}
print("질문:", question)
print("기준 답:", reference_answer)
print("결과 글을 정한 도구:", list(tool_results))'''

REFERENCE = author_03.REFERENCE
TOOL_SEARCH = author_03.TOOL_SEARCH
TOOL_CHECK = author_03.TOOL_CHECK

SEARCH_FREE = r'''# 검색 도구의 인자만 보지 않는 평가 함수를 모드 넷마다 만듭니다(03절 5절 — 02절 7절의 도구별 덮어쓰기)
modes = ["strict", "unordered", "subset", "superset"]
search_free = {}
for mode in modes:
    search_free[mode] = create_trajectory_match_evaluator(
        trajectory_match_mode=mode,
        tool_args_match_overrides={"search_documents": "ignore"},
    )
print("평가 함수를 만든 모드:", list(search_free))'''

TEXTS = r'''# 두 실행에 같게 쓸 시스템 메시지 글과 실행 한도를 정합니다(03절 4절 에이전트 셀과 같은 글·같은 값)
agent_rule = "도서관 규정 질문에는 먼저 search_documents로 문서를 찾고, 찾은 문서 ID로 check_source를 불러 문서가 있는지 확인한 뒤, 확인한 문서의 글만 근거로 한국어 한 문장으로 답하세요."
run_config = {"recursion_limit": 20}
print("시스템 메시지 글:", agent_rule)
print("실행 한도:", run_config["recursion_limit"])
print("두 값의 출처: 03절 4절 에이전트 셀(실행 전에 정함)")'''

DEF_RUN = r'''# 조립 함수입니다. 호출 한도 하나를 받아 평가받는 에이전트를 만들고, 질문 한 줄로 한 번 실행해 결과 메시지를 내놓습니다
def run_agent(limit):
    # Ch 22 04절: 한 번 실행에서 보낼 모델 요청 수를 limit으로 묶고, 닿으면 끝으로 갑니다
    call_limit = ModelCallLimitMiddleware(run_limit=limit, exit_behavior="end")
    # 03절 4절: 도구 둘·시스템 메시지 글을 붙인 에이전트를 만들어, 실행 한도를 주고 한 번 실행합니다
    agent = create_agent(model, tools=[search_documents, check_source], system_prompt=agent_rule, middleware=[call_limit])
    first_input = {"messages": [HumanMessage(content=question)]}
    result = agent.invoke(first_input, run_config)
    return result["messages"]'''

DEF_COUNT = r'''# 결과 메시지에서 도구 호출 요청이 하나라도 있는 모델 응답의 수를 세어 내놓습니다
def count_asked(messages):
    asked = 0
    for message in messages:
        if type(message).__name__ == "AIMessage":
            if len(tool_call_names(message)) > 0:
                asked = asked + 1
    return asked'''

DEF_PART = r'''# 마지막 메시지에 사용량 기록이 없으면(호출 한도가 끼운 글) 그 하나를 빼고, 모델이 쓴 응답까지의 목록을 내놓습니다
def model_part(messages):
    if messages[-1].usage_metadata is None:
        # 자르기 [:-1]은 맨 끝 하나를 뺀 앞부분입니다(Ch 26 05절)
        return messages[:-1]
    return messages'''

DEF_ROW = r'''# 실행 한 번의 값을 04절 공통 칸 딕셔너리로 옮겨 담아 내놓습니다(걸린 초는 재지 않아 None, 점수는 참이면 1.0)
def run_row(name, messages, usage, score):
    return {
        "이름": name,
        "요청 수": usage["requests"],
        "도구 요청 수": len(called_tool_names(messages)),
        "토큰 수": usage["input_tokens"] + usage["output_tokens"],
        "걸린 초": None,
        "점수": float(score),
    }'''

RUN1 = r'''# 실행 1: 호출 한도 4로 에이전트를 한 번 실행하고, 메시지를 차례대로 봅니다(모델 요청은 여기서 처음 나감)
first_limit = 4
first_messages = run_agent(first_limit)
print("호출 한도:", first_limit)
show_messages(first_messages)'''

LAST1 = r'''# 실행 1의 마지막 메시지 글과, 그 메시지에 사용량 기록이 없는지 봅니다(모델이 쓴 응답이면 기록이 있음)
first_last = first_messages[-1]
print("마지막 메시지 글:", first_last.content)
print("사용량 기록이 없는가:", first_last.usage_metadata is None)'''

CHECK1 = r'''# 실행 1에서 끝 메시지를 뺀 목록으로 모델 요청 수(Ch 19 05절 함수 sum_usage)를 세고, 03절 셈과 견줍니다
first_kept = model_part(first_messages)
first_usage = sum_usage(first_kept)
first_asked = count_asked(first_messages)
first_formula = first_usage["requests"] == first_asked + 1
print("끝에서 뺀 메시지 수:", len(first_messages) - len(first_kept))
print("도구를 요청한 응답 수:", first_asked)
print("모델 요청 수:", first_usage["requests"])
print("모델 요청 수 = 도구를 요청한 응답 수 + 1:", first_formula)'''

MODES1 = r'''# 실행 1의 궤적을 검색어를 빼고 네 모드로 기준 궤적과 견줍니다(02절 함수 four_modes)
first_modes = four_modes(first_messages, reference, search_free)
print("실행 1:", first_modes)'''

RUN2 = r'''# 실행 2: 값 하나만 바꿉니다. 호출 한도를 2로 줄여 같은 질문으로 한 번 실행하고, 메시지를 차례대로 봅니다
second_limit = 2
second_messages = run_agent(second_limit)
print("호출 한도:", second_limit)
show_messages(second_messages)'''

LAST2 = r'''# 실행 2의 마지막 메시지 글과, 그 메시지에 사용량 기록이 없는지 봅니다
second_last = second_messages[-1]
print("마지막 메시지 글:", second_last.content)
print("사용량 기록이 없는가:", second_last.usage_metadata is None)'''

CHECK2 = r'''# 실행 2에서도 끝 메시지를 뺀 목록으로 모델 요청 수를 세고, 03절 셈과 견줍니다
second_kept = model_part(second_messages)
second_usage = sum_usage(second_kept)
second_asked = count_asked(second_messages)
second_formula = second_usage["requests"] == second_asked + 1
print("끝에서 뺀 메시지 수:", len(second_messages) - len(second_kept))
print("도구를 요청한 응답 수:", second_asked)
print("모델 요청 수:", second_usage["requests"])
print("모델 요청 수 = 도구를 요청한 응답 수 + 1:", second_formula)'''

MODES2 = r'''# 실행 2의 궤적도 실행 1과 같은 네 평가 함수로 기준 궤적과 견줍니다
second_modes = four_modes(second_messages, reference, search_free)
print("실행 2:", second_modes)'''

ROWS = r'''# 두 실행을 04절 공통 칸 두 줄로 옮겨 담고, 04절 함수 show_row로 한 표에 출력합니다(점수 칸은 모드 strict 판정)
first_row = run_row("실행 1(한도 4)", first_messages, first_usage, first_modes["strict"])
second_row = run_row("실행 2(한도 2)", second_messages, second_usage, second_modes["strict"])
rows = [first_row, second_row]
print("이름 | 요청 수 | 도구 요청 수 | 토큰 수 | 걸린 초 | 점수")
for row in rows:
    show_row(row)'''

TALLY = r'''# 두 실행 가운데 점수 칸이 1.0인 실행과, 03절 셈이 맞은 실행을 셉니다(04절 5절처럼 세는 값으로 읽기)
score_count = 0
for row in rows:
    if row["점수"] == 1.0:
        score_count = score_count + 1
formula_count = 0
for formula in [first_formula, second_formula]:
    if formula:
        formula_count = formula_count + 1
print("점수가 1.0인 실행:", score_count, "| 셈이 맞은 실행:", formula_count, "| 전체 실행:", len(rows))'''


def check_same_as_prev() -> None:
    """앞 절 셀과 같은 글·같은 값이라고 적는 셀이 디스크 노트북 셀에 그대로 있는지 봅니다."""
    sources_03 = author_03.notebook_code_sources(NB03)
    joined_03 = "\n".join(sources_03)
    # 설치·기준 궤적·도구 둘은 03절 셀 글 그대로
    for cell in [INSTALL, REFERENCE, TOOL_SEARCH, TOOL_CHECK]:
        assert cell in sources_03, cell.splitlines()[0]
    # 질문·기준 답·결과 글, 모드 이름·덮어쓰기 평가 함수, 시스템 메시지 글·실행 한도는 03절 셀과 같은 줄
    for cell in [DATA, SEARCH_FREE, TEXTS]:
        for line in cell.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("print(") or stripped == "":
                continue
            assert line in joined_03, line
    # 조립 함수의 호출 한도·에이전트 줄은 03절 4절 셀의 같은 줄에서 한도 값만 인자로 바꾼 모양
    assert 'call_limit = ModelCallLimitMiddleware(run_limit=4, exit_behavior="end")' in joined_03
    assert "library_agent = create_agent(model, tools=[search_documents, check_source], system_prompt=agent_rule, middleware=[call_limit])" in joined_03
    assert 'first_input = {"messages": [HumanMessage(content=question)]}' in joined_03


def check_same_as_probe() -> None:
    """노트북 셀의 모델·자료·도구·평가 함수·글·조립 함수·셈 함수 줄이 흔들림 확인 스크립트(probe05.py)에 같은 글로 있는지 봅니다."""
    probe_lines = []
    for line in PROBE.read_text(encoding="utf-8").splitlines():
        probe_lines.append(line.strip())
    model_cell = key_and_model_cells("openai:gpt-5.4-mini")[3]["source"]
    for cell in [model_cell, DATA, REFERENCE, TOOL_SEARCH, TOOL_CHECK, SEARCH_FREE, TEXTS, DEF_RUN, DEF_COUNT, DEF_PART, DEF_ROW]:
        for line in cell.splitlines():
            stripped = line.strip()
            if stripped == "" or stripped.startswith("#") or stripped.startswith("print(") or stripped.startswith("@"):
                continue
            assert stripped in probe_lines, "흔들림 확인 스크립트에 없는 줄: " + stripped
    probe_text = PROBE.read_text(encoding="utf-8")
    for piece in ["first_messages = run_agent(4)", "second_messages = run_agent(2)",
                  "from eval_tools import called_tool_names, four_modes, make_trajectory, show_messages, sum_usage, tool_call_names"]:
        assert piece in probe_text, piece


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/05-figures.md)
FIG1 = "05-1-평가받는-에이전트와-두-평가의-조립"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 왼쪽 초록 상자 재료 03절과 같음, 질문 · 기준 궤적 · 도구 둘 · 시스템 메시지 글과, 오른쪽 파란 상자 바꾸는 값 호출 한도, 실행 1은 4 · 실행 2는 2에서 화살표가 파란 상자 조립 함수 run_agent, create_agent · 실행 한도 20 · invoke 한 번으로 모입니다. 이어서 보라 상자 gpt-5.4-mini 에이전트 요청, 노란 상자 결과 메시지 실행마다 궤적 하나로 화살표가 갑니다. 결과 메시지 상자에서 화살표 둘이 아래 파란 상자 둘로 갈라집니다. 왼쪽은 02절 four_modes 검색어를 뺀 모드 넷, 오른쪽은 count_asked · model_part · run_row · 04절 show_row, 03절 셈 · 공통 칸 한 줄인 그림"
FIG1_CAP = "03절의 평가받는 에이전트에 호출 한도 하나만 바꿔 넣고, 두 실행의 결과를 02절의 네 모드와 04절의 공통 칸으로 함께 봅니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 03절과 같은 재료이고, 파란 상자는 바꾸는 값과 우리가 적거나 가져온 함수입니다.
보라 상자는 이 노트북이 실제로 부른 모델이고, 평가 모델은 부르지 않아 그리지 않았습니다.
노란 상자는 5절과 6절에서 함수 show_messages로 출력한 결과 메시지입니다.
아래 두 파란 상자는 같은 결과 메시지를 서로 다른 방법으로 보는 갈래이고, 서로의 차례가 아닙니다."""

FIG2 = "05-2-실행-1의-실제-순서"
FIG2_ALT = "세로선 넷이 있는 차례 그림입니다. 왼쪽부터 우리 코드 run_agent · 한도 4, 에이전트 그래프, 연보라 띠 안의 모델 gpt-5.4-mini, 도구 둘입니다. 우리 코드에서 invoke 질문 한 줄 화살표가 그래프로 갑니다. 그래프에서 요청 1 화살표가 모델로 가고 search_documents 요청 점선이 돌아오며, search_documents 실행 화살표가 도구로 가고 도구 메시지 success 점선이 돌아옵니다. 요청 2와 check_source도 같은 모양으로 이어집니다. 요청 3 화살표가 모델로 가고 도구 요청 없는 답 점선이 돌아온 뒤, 결과 메시지 점선이 우리 코드로 돌아옵니다. 맨 아래 우리 코드와 그래프에 걸친 노란 메모에 요청 수 3 = 도구를 요청한 응답 수 2 + 1이 적힌 그림"
FIG2_CAP = "노트북 밖 다섯 번과 두 커널에서 모두, 실행 1은 도구 둘을 차례로 부른 뒤 답해 모델 요청이 3번이었습니다."
FIG2_READ = "위에서 아래로 실행 차례대로 읽고, 세로선은 왼쪽부터 우리 코드, 그래프, 모델, 도구 둘입니다. 연보라 띠는 실제로 부른 모델 gpt-5.4-mini의 자리이고, 실선은 부르는 쪽, 점선은 돌아오는 쪽입니다. 도구 이름과 결과 상태는 노트북 5절 첫 셀 출력이고, 맨 아래 노란 메모는 셋째 셀 출력입니다. 요청마다 수를 세는 호출 한도는 이 그림에 따로 그리지 않았습니다. 요청의 차례는 노트북 밖 다섯 번과 새 커널 두 번에서 같았을 때만 그렸습니다."

FIG3 = "05-3-호출-한도-4와-2의-두-실행"
FIG3_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 회색 상자 두 실행에 같게 둔 것, 질문 · 도구 둘 · 시스템 메시지 글 · 실행 한도 20 · run_agent에서 점선 둘이 나란한 파란 상자 둘로 갑니다. 왼쪽 파란 상자 실행 1 · 호출 한도 4 아래 노란 상자에는 요청 3 · 도구를 요청한 응답 2, 03절 셈 True, 끝은 모델이 쓴 답, 네 모드 모두 True · 점수 1.0이 있습니다. 오른쪽 파란 상자 실행 2 · 호출 한도 2 아래 노란 상자에는 요청 2 · 도구를 요청한 응답 2, 03절 셈 False, 끝은 한도가 끼운 글 Model call limits exceeded, 사용량 None, 네 모드 모두 True · 점수 1.0이 있습니다. 두 노란 상자는 맨 아래 노란 상자 점수가 1.0인 실행 둘, 03절 셈이 맞은 실행 하나로 모이는 그림"
FIG3_CAP = "노트북 밖 다섯 번과 두 커널에서 모두, 두 실행은 네 모드가 참이었고 03절 셈은 한도 4 실행에서만 맞았습니다."
FIG3_READ = """위에서 아래로 읽습니다.
맨 위 회색 상자는 두 실행에 같게 둔 조건이고, 파란 상자가 바꾼 값 호출 한도입니다.
왼쪽 칸이 실행 1, 오른쪽 칸이 실행 2이고, 노란 상자는 노트북 5·6·7절 출력입니다.
두 칸의 마지막 줄은 같고, 요청 수와 03절 셈, 끝 메시지만 다릅니다.
두 칸의 값은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다."""

ILLU = "05-4-끝이-다른-두-띠"
ILLU_ALT = "흰 바탕에 밝은 나무판 둘이 위아래로 가로놓여 있습니다. 판마다 크림색 종이띠 하나가 핀 여섯 개로 길게 고정되어 있고, 띠마다 둥근 구멍이 한 줄로 뚫려 있습니다. 두 띠는 길이가 같고, 앞부분은 같은 자리에 구멍이 이어집니다. 위 띠는 오른쪽 끝까지 구멍이 이어지고, 맨 끝에 구멍 세 개가 모여 있습니다. 아래 띠는 오른쪽 끝 부분이 구멍 없는 회색 종이입니다. 판마다 왼쪽 위에 흰 카드가 한 장씩 있고, 위 카드에는 검은 점 셋, 아래 카드에는 검은 점 둘이 찍혀 있습니다. 사람·손·글자·숫자·음표·화살표·오르골 기계는 없는 그림"
ILLU_CAP = "같은 길이의 종이띠 둘 가운데 위 띠는 구멍 무리로, 아래 띠는 구멍 없는 회색 종이로 끝나고, 카드의 점은 셋과 둘입니다."
ILLU_READ = "나무판 둘에 같은 길이의 종이띠가 하나씩 붙어 있고, 앞부분은 같은 자리에 구멍이 뚫려 있습니다. 끝 부분은 위 띠에서 구멍 무리로 끝나고, 아래 띠에서는 구멍 없는 회색 종이입니다. 띠가 궤적, 앞부분 구멍이 도구 요청이고, 끝 부분은 위 띠에서 모델이 쓴 답, 아래 띠에서 한도가 끼운 끝 메시지입니다. 판 왼쪽 카드는 공통 칸 한 줄이고, 점 셋과 둘은 모델 요청 수 3과 2입니다. 구멍의 수, 핀, 판의 나뭇결은 어떤 값과도 짝짓지 않습니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 03절의 평가받는 에이전트, 02절의 네 모드, 04절의 공통 칸을 한 흐름에 모읍니다.
2. 호출 한도 4인 실행 1과, 그 값 하나만 2로 줄인 실행 2를 차례로 실행합니다.
3. 두 실행을 네 모드와 공통 칸 두 줄로 견주어, 한도에 닿은 실행을 무엇이 가려내는지 봅니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 실행 1과 실행 2에서 에이전트를 한 번씩 실행합니다.
노트북 밖에서 두 실행을 다섯 번씩 보냈을 때, 요청은 실행 1이 3번, 실행 2가 2번이었습니다.
그래서 이 노트북의 모델 요청은 모두 5번으로 어림하고, 평가 모델은 부르지 않습니다.
호출 한도를 붙여, 한 실행의 요청이 한도를 넘지 않게 막습니다.

요금표로 어림한 예상 비용은 두 실행을 합쳐 0.002달러 아래이고, 청구 금액이 아닙니다.
읽는 파일은 `.env`와 같은 폴더의 도구 파일 `eval_tools.py`이고, 쓰는 파일은 없습니다.
모델이 쓰는 답 글과 토큰 수는 실행마다 달라질 수 있고, 걸린 시간은 재지 않았습니다.
앞에서 배운 함수 일곱은 도구 파일에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 넷을 설치합니다.
판은 agentevals 0.0.9와 langchain 1.4.0입니다.
모델을 부르는 langchain-openai는 1.6.0, 키를 읽는 python-dotenv는 1.2.3입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**실습 범위** — 이 절은 이 챕터의 실습이고, 30분 안팎입니다.
따로 내는 과제는 없고, 강사와 함께 첫 셀부터 차례로 실행합니다.

실습 폴더 `labs/part6/ch29-agent-evaluation`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def model_cells() -> list[dict]:
    """과정 표준 키·모델 셀(nbkit)에 이 절의 결과 읽기(실행일·요청은 5·6절 실행 셀에서만)와 2절 첫 설명을 붙입니다."""
    found = key_and_model_cells("openai:gpt-5.4-mini")
    found[-1] = md("""**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.
모델 요청은 5절과 6절의 실행 셀에서만 나갑니다.

## 2. 재료: 질문·기준 궤적·도구 둘

실습 재료는 03절과 같은 질문·기준 궤적·도구 둘입니다.
다음 셀은 03절 2절과 같은 질문·기준 답·결과 글을 정합니다.
아래에서 만들 도구 함수도 이 결과 글을 내놓습니다.""")
    return found


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이 절은 Ch 29의 실습입니다.
01~04절에서 하나씩 본 기능 가운데 셋을, 도서관 규정에 답하는 에이전트 하나에 모읍니다.
03절의 평가받는 에이전트, 02절의 네 모드와 도구별 덮어쓰기, 04절의 공통 칸입니다.
그다음 호출 한도 하나만 바꿔 두 번 실행하고, 두 결과를 견줍니다.

첫 셀은 패키지 넷을 설치하고 설치된 판 번호를 출력합니다.
03절과 같은 넷이고, 설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `agentevals: 0.0.9`, `langchain: 1.4.0`, `langchain-openai: 1.6.0`, `python-dotenv: 1.2.3`이 보입니다.
넷 모두 실습 폴더 잠금과 같은 판입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
03절처럼 평가 함수를 만드는 함수와, 에이전트·호출 한도·모델·메시지·도구 이름을 가져옵니다.
마지막 가져오기 줄은 앞에서 배운 함수 일곱을 도구 파일에서 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 라벨 `도구 파일에서 가져온 함수:` 뒤에 `show_row`·`four_modes`·`sum_usage` 등 함수 일곱의 이름이 보입니다.
앞에서 배운 함수는 `eval_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.

노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다.

함수 `show_row(row)`는 04절 노트북에서 처음 적은 함수이고, 이 절부터 도구 파일에서 가져옵니다.
도구 파일에는 04절 셀의 주석과 본문을 글자 그대로 옮겼고, 인자도 04절과 같습니다.
나머지 여섯은 03절에서도 가져온 이름입니다.
함수 `make_trajectory`·`called_tool_names`는 01절, `four_modes`는 02절에서 배웠습니다.
함수 `tool_call_names`·`sum_usage`·`show_messages`는 Ch 19 04~06절에서 배웠습니다."""),
    ] + model_cells() + [
        code(DATA),
        md("""**결과 읽기** — 출력 줄 `기준 답: 일반 도서는 14일 동안 빌릴 수 있습니다.`가 보입니다.
라벨 `결과 글을 정한 도구:` 뒤에는 `'search_documents'`와 `'check_source'`가 있습니다.

다음 셀은 03절 2절과 같은 셀로, 도구 요청 둘로 기준 궤적을 만듭니다."""),
        code(REFERENCE),
        md("""**결과 읽기** — 출력 줄 `기준 궤적의 도구 차례: ['search_documents', 'check_source']`와 `메시지 수: 6`이 보입니다.
검색한 뒤 출처를 확인하고 답하는, 01~03절과 같은 기준 궤적입니다.

다음 셀은 03절 4절과 같은 셀로, 검색 도구를 만듭니다.
03절처럼 `@tool` 줄은 아래 함수를 도구로 등록하고, 독스트링은 모델이 읽는 도구 설명이 됩니다."""),
        code(TOOL_SEARCH),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 검색 도구는 교재용이라, 어떤 검색어에도 같은 검색 결과 글을 내놓습니다.

다음 셀도 03절 4절과 같은 셀로, 출처 확인 도구를 만듭니다."""),
        code(TOOL_CHECK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
문서 ID가 `LIB-001`이면 출처 확인 결과 글을, 아니면 그 문서가 없다는 글을 내놓습니다.

검색어는 모델이 고르는 값이라, 기준 궤적의 검색어와 다를 수 있습니다.
그래서 03절 5절처럼 검색 도구의 인자만 보지 않는 평가 함수를 모드 넷마다 만듭니다.
02절 7절에서 본 도구별 덮어쓰기입니다."""),
        code(SEARCH_FREE),
        md("""**결과 읽기** — 출력 줄 `평가 함수를 만든 모드: ['strict', 'unordered', 'subset', 'superset']`이 보입니다.
네 평가 함수 모두 검색 도구 요청의 인자는 보지 않고, 출처 확인 요청의 인자는 그대로 견줍니다.
두 실행 모두 이 평가 함수 넷으로 판정합니다.

## 3. 조립하기

조립에는 03절 4절의 평가받는 에이전트를 씁니다.
다음 셀은 03절 4절과 같은 시스템 메시지 글과 실행 한도를 정합니다.
두 값은 두 실행에 같게 씁니다."""),
        code(TEXTS),
        md("""**결과 읽기** — 라벨 `시스템 메시지 글:` 뒤에 검색한 뒤 출처를 확인하고 답하라는 글이 보입니다.
출력 줄 `실행 한도: 20`도 보입니다.
라벨 `두 값의 출처:` 뒤의 글은 두 값을 가져온 곳을 적어 둔 글이고, 코드가 견준 값은 아닙니다.
두 값은 실행 전에 정했고, 결과를 보고 바꾸지 않았습니다.

다음 셀은 호출 한도 하나를 받아, 에이전트를 만들고 한 번 실행하는 조립 함수입니다.
03절 4절의 에이전트 셀과 실행 셀을 한 함수로 모았습니다.
호출 한도만 인자로 받으므로, 두 실행 사이에 달라지는 것은 이 값 하나뿐입니다."""),
        code(DEF_RUN),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 안에서 Ch 22 04절의 호출 한도를 실행마다 새로 만듭니다.
인자 `exit_behavior="end"`는 한도에 닿으면 오류 없이 끝으로 가게 합니다.
모델·도구 둘·시스템 메시지 글·질문·실행 한도는 앞 셀에서 만든 이름을 그대로 씁니다.

## 4. 결과를 볼 함수

두 실행을 같은 잣대로 보려고, 결과 메시지에서 값을 세는 함수 셋을 먼저 적습니다.
첫째 함수 `count_asked`는 도구를 요청한 응답 수를 셉니다.
03절 4절에서 셈 「요청 수 = 도구를 요청한 응답 수 + 1」을 확인한 셀의 반복문을 함수로 옮긴 모양입니다."""),
        code(DEF_COUNT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
응답(`AIMessage`)마다 도구 호출 요청의 이름을 모아, 하나라도 있으면 셉니다.

둘째 함수 `model_part`는 모델이 쓴 응답까지만 남긴 목록을 내놓습니다.
Ch 22 04절에서 본 것처럼, 호출 한도에 닿은 실행은 한도가 끼운 글로 끝납니다.
Ch 26 04절에서 본 것처럼, 그 끝 메시지는 모델 요청으로 받은 응답이 아니라 사용량 기록이 `None`입니다.
도구 파일 함수 `sum_usage`는 응답마다 사용량 기록을 더하므로, 이 메시지를 빼고 넘겨야 합니다."""),
        code(DEF_PART),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
마지막 메시지의 사용량 기록이 `None`이면 그 하나를 빼고, 아니면 목록을 그대로 내놓습니다.
자르기 `[:-1]`은 Ch 26 05절에서 본 대로 맨 끝 하나를 뺀 앞부분입니다.

셋째 함수 `run_row`는 실행 한 번의 값을 04절 공통 칸 딕셔너리로 옮겨 담습니다.
칸 이름은 04절과 같은 여섯, 이름·요청 수·도구 요청 수·토큰 수·걸린 초·점수입니다.
걸린 초는 재지 않아, 04절에서 기록에 없는 칸을 둔 것처럼 모르는 값 `None`으로 둡니다.
점수 칸에는 두 실행 모두 같은 잣대인 모드 `strict`(검색어 뺌)의 판정을, 참이면 1.0으로 담습니다."""),
        code(DEF_ROW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
04절 함수 `ch21_row`와 같은 모양으로, 칸 이름을 키로 한 딕셔너리를 내놓습니다.
도구 요청 수는 01절 함수 `called_tool_names`가 모은 도구 이름의 수입니다.
04절의 두 기록은 점수 칸의 잣대가 달라 견주지 않았지만, 이 절의 두 줄은 잣대가 같습니다.

## 5. 실행 1: 호출 한도 4

이제 실행 1을 합니다.
호출 한도는 03절과 같은 4이고, 03절 셈으로 이 궤적에 드는 요청 3번보다 한 번 여유가 있습니다.
실행 전에 예상해 봅니다.
03절과 같은 에이전트라면, 도구를 어떤 차례로 부르고 요청은 몇 번일까요?"""),
        code(RUN1),
        md("""**결과 읽기** — 출력 줄 `호출 한도: 4`가 보입니다.
그 아래 `AIMessage | 도구 호출 요청: ['search_documents']`와 `AIMessage | 도구 호출 요청: ['check_source']`가 차례로 보입니다.
두 줄 뒤에는 `ToolMessage | 결과 상태: success`로 시작하는 줄이 하나씩 이어집니다.
마지막 줄 `AIMessage | 도구 호출 요청: []`는 도구를 요청하지 않은 응답입니다.

에이전트는 03절처럼 검색 → 출처 확인 → 마지막 응답의 차례로 움직였습니다.
도구를 부른 차례는 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.

다음 셀은 마지막 메시지의 글과, 그 메시지에 사용량 기록이 없는지 봅니다."""),
        code(LAST1),
        md("""**결과 읽기** — 출력 줄 `사용량 기록이 없는가: False`가 보입니다.
라벨 `마지막 메시지 글:` 뒤에는 모델이 쓴 답이 있습니다.
사용량 기록이 있으니, 마지막 메시지는 모델 요청으로 받은 응답입니다.

이번 실행에서는 답 글이 기준 답 「일반 도서는 14일 동안 빌릴 수 있습니다」와 글자까지 같았습니다.
답 글은 모델이 쓴 글이라 실행마다 달라질 수 있어, 결론에 쓰지 않습니다.

다음 셀은 함수 `model_part`로 끝 메시지를 뺀 목록을 받아 모델 요청 수를 세고, 03절 셈과 견줍니다.
실행 1은 마지막 메시지에 사용량 기록이 있어, 뺄 메시지가 없을 것입니다."""),
        code(CHECK1),
        md("""**결과 읽기** — 출력 줄 `끝에서 뺀 메시지 수: 0`, `도구를 요청한 응답 수: 2`, `모델 요청 수: 3`이 보입니다.
출력 줄 `모델 요청 수 = 도구를 요청한 응답 수 + 1: True`로, 03절 셈이 맞았습니다.
도구를 요청한 응답 둘에, 답을 쓴 응답 하나가 더해졌습니다.
요청 3번은 호출 한도 4 안이라, 실행이 답까지 갔습니다.

다음 셀은 실행 1의 궤적을 검색어를 빼고 네 모드로 견줍니다."""),
        code(MODES1),
        md("""**결과 읽기** — 출력 줄 `실행 1: {'strict': True, 'unordered': True, 'subset': True, 'superset': True}`가 보입니다.
03절 5절처럼 네 모드 모두 참이었습니다.
검색어를 빼고 보면, 실행 1은 기준 궤적과 같은 도구를 같은 차례로 불렀습니다.

## 6. 실행 2: 호출 한도 2

실행 2는 값 하나만 바꿉니다.
호출 한도를 4에서 2로 줄이고, 질문·도구·시스템 메시지 글·실행 한도·조립 함수는 실행 1과 같게 둡니다.
03절 셈으로 이 궤적에는 요청이 3번 듭니다.
Ch 22 04절에서 본 것처럼 호출 한도는 모델 요청 전에 센 수를 보므로, 한도 2면 셋째 요청 전에 멈춥니다.

실행 전에 예상해 봅니다.
메시지를 차례대로 보는 출력은 실행 1과 어떻게 다를까요?
네 모드의 판정은 실행 1과 같을까요, 달라질까요?"""),
        code(RUN2),
        md("""**결과 읽기** — 출력 줄 `호출 한도: 2`가 보입니다.
그 아래 줄은 실행 1의 출력과 한 줄도 다르지 않습니다.
도구 호출 요청 두 줄과 도구 메시지 두 줄이 같은 차례로 있고, 마지막 줄도 `AIMessage | 도구 호출 요청: []`입니다.

함수 `show_messages`는 메시지의 종류와 도구 요청, 도구 결과만 보여 줍니다.
그래서 이 출력만으로는 실행 2가 한도에 닿았는지 보이지 않습니다.
도구 요청 둘은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 실행 1과 같았습니다.

다음 셀은 실행 1처럼 마지막 메시지의 글과 사용량 기록을 봅니다."""),
        code(LAST2),
        md("""**결과 읽기** — 출력 줄 `마지막 메시지 글: Model call limits exceeded: run limit (2/2)`와 `사용량 기록이 없는가: True`가 보입니다.
마지막 메시지는 모델이 쓴 답이 아니라, 호출 한도가 끼운 글입니다.
글 끝의 `(2/2)`는 센 요청 수 2가 한도 2에 닿았다는 뜻입니다.

이 끝 메시지는 설치판 langchain 1.4.0 `agents/middleware/model_call_limit.py` 37~60행이 만듭니다.
에이전트는 출처 확인 결과까지 받았지만, 그 결과를 읽고 답할 셋째 요청은 나가지 않았습니다.

다음 셀은 실행 2에서도 요청 수를 세어 03절 셈과 견줍니다.
함수 `model_part`가 끝 메시지를 빼고 함수 `sum_usage`에 넘깁니다."""),
        code(CHECK2),
        md("""**결과 읽기** — 출력 줄 `끝에서 뺀 메시지 수: 1`이 보입니다.
출력 줄 `도구를 요청한 응답 수: 2`와 `모델 요청 수: 2`도 보입니다.
출력 줄 `모델 요청 수 = 도구를 요청한 응답 수 + 1: False`로, 03절 셈이 맞지 않았습니다.
답을 쓴 응답이 없어, 요청 수가 도구를 요청한 응답 수와 같습니다.

03절 셈은 답까지 간 실행에서 맞는 셈이고, 한도에 닿은 이 실행에서는 1이 모자랐습니다.
요청 수와 셈은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.

다음 셀은 실행 2의 궤적을 실행 1과 같은 네 모드로 견줍니다."""),
        code(MODES2),
        md("""**결과 읽기** — 출력 줄 `실행 2: {'strict': True, 'unordered': True, 'subset': True, 'superset': True}`가 보입니다.
답을 쓰지 못한 실행 2도 네 모드 모두 참이었습니다.

01·02절에서 본 것처럼, 네 모드는 도구 요청을 견주고 메시지 글은 견주지 않습니다.
모드 `strict`는 메시지 수·역할·차례까지 보지만, 실행 2는 끝 메시지도 도구를 요청하지 않는 응답이라 그것까지 같습니다.
그래서 호출 한도가 끼운 끝 메시지도 모드에게는 기준 궤적의 답과 같은 자리의 응답으로 보입니다.
이 판정도 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.

## 7. 두 실행 견주기

마지막으로 두 실행을 04절 공통 칸 두 줄로 옮겨 담아 한 표로 봅니다.
04절 함수 `show_row`는 공통 칸 딕셔너리 한 줄을 「|」로 이어 출력합니다."""),
        code(ROWS),
        md("""**결과 읽기** — 라벨 줄 `이름 | 요청 수 | 도구 요청 수 | 토큰 수 | 걸린 초 | 점수` 아래 두 줄이 보입니다.
두 줄 모두 도구 요청 수 칸이 `2`, 걸린 초 칸이 `None`, 점수 칸이 `1.0`입니다.
요청 수 칸만 실행 1이 `3`, 실행 2가 `2`로 다릅니다.
점수 칸만 보면 두 실행은 같은 줄로 보입니다.

이번 실행에서는 토큰 수 칸이 실행 1 996, 실행 2 615였습니다.
실행 2에는 셋째 요청이 없어 토큰 수가 적었습니다.
토큰 수는 실행마다 달라질 수 있어 결론에 쓰지 않습니다.

다음 셀은 두 실행 가운데 점수가 1.0인 실행과, 03절 셈이 맞은 실행을 셉니다.
04절 5절에서 잘됐다고 적은 줄을 센 것과 같은 모양입니다."""),
        code(TALLY),
        md("""**결과 읽기** — 출력 줄 `점수가 1.0인 실행: 2 | 셈이 맞은 실행: 1 | 전체 실행: 2`가 보입니다.
궤적 맞춰 보기로는 두 실행이 모두 통과했지만, 03절 셈이 맞은 것은 답까지 간 실행 1뿐입니다.

모드는 도구를 기준대로 불렀는지를 봅니다.
요청 수 셈과 끝 메시지는 실행이 어떻게 끝났는지를 봅니다.
도구를 모두 부른 뒤 한도에 닿은 실행은, 궤적 맞춰 보기와 함께 운영 지표를 봐야 가려낼 수 있습니다.
두 수는 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.

## 정리

1. 03절의 평가받는 에이전트, 02절의 네 모드와 도구별 덮어쓰기, 04절의 공통 칸을 한 흐름에 모았습니다.
2. 호출 한도를 4에서 2로 줄이자, 실행 2는 도구 둘을 부른 뒤 한도가 끼운 글로 끝났고 03절 셈이 `False`였습니다.
3. 두 실행 모두 네 모드가 참이었고, 한도에 닿은 실행은 요청 수 셈과 끝 메시지로 가려냈습니다. 2·3번의 값은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.

이 절로 Ch 29와 Part 6이 끝납니다.
다음 학습은 Part 7 Ch 30 01절입니다. 그 절에서는 웹 서비스가 받을 요청과 내놓을 응답의 모양을 정합니다."""),
    ]


def notebook_cells() -> list[dict]:
    return cells()


# ---------------------------------------------------------------- _src 본문
def mermaid_block(name: str, alt: str, caption: str, reading: str) -> str:
    """.mmd와 글이 있을 때만 본문에 넣습니다(새 커널 A·B를 그림보다 먼저 돌릴 때 빌드가 멈추지 않게)."""
    if not (FIGS / (name + ".mmd")).is_file() or reading.startswith("[["):
        return ""
    return ("{{mermaid:" + name + "|" + alt + "|" + caption + "}}\n"
            + '<p class="look"><b>도식 읽기</b> — ' + html_text(reading) + "</p>\n")


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or ILLU_READ.startswith("[["):
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


def link(url: str, label: str) -> str:
    return '<a href="' + url + '">' + label + "</a>"


L_01 = "01-에이전트-평가-세-전략.html"
L_02 = author_01.L_02
L_03 = author_01.L_03
L_04 = "04-운영-지표와-Ch18-궤적-비교.html"
L_CH19_04 = "../../part5/ch19-model-tools/04-설명만으로-도구-선택하기.html"
L_CH19_05 = author_03.L_CH19_05
L_CH19_06 = "../../part5/ch19-model-tools/06-오류와-읽기-쓰기-분리.html"
L_CH22_04 = author_03.L_CH22_04
L_CH26_04 = "../ch26-delegation/04-호출-수-비용-종료-조건-비교.html"
L_CH26_05 = "../ch26-delegation/05-위임-구조-실습.html"
L_CH30_01 = author_04.L_CH30_01

LEARNED_ROWS = [
    (link(L_01, "01절"), "기준 궤적을 만드는 함수 <code>make_trajectory</code> · 도구 차례를 모으는 함수 <code>called_tool_names</code> · 모드 <code>strict</code>는 메시지 글을 견주지 않음", "기준 궤적 · 공통 칸의 도구 요청 수 · 실행 2의 모드 판정 읽기"),
    (link(L_02, "02절"), "네 모드 · 도구별 덮어쓰기 · 함수 <code>four_modes</code>", "검색어를 뺀 네 모드로 두 궤적 판정"),
    (link(L_03, "03절"), "평가받는 에이전트(<code>@tool</code> 둘 · <code>create_agent</code> · 호출 한도 4 · 실행 한도 20) · 셈 「요청 수 = 도구를 요청한 응답 수 + 1」", "조립 함수 <code>run_agent</code> · 함수 <code>count_asked</code> · 두 실행의 셈"),
    (link(L_04, "04절"), "운영 지표 · 공통 칸 여섯 · 함수 <code>show_row</code> · 세는 값으로 읽기", "함수 <code>run_row</code> · 공통 칸 두 줄 표 · 점수와 셈으로 센 실행 수"),
    (link(L_CH19_04, "Ch 19 04") + "~" + link(L_CH19_06, "06절"), "함수 <code>tool_call_names</code>·<code>sum_usage</code>·<code>show_messages</code>", "도구를 요청한 응답 세기 · 모델 요청 수 · 두 실행의 메시지 보기"),
    (link(L_CH22_04, "Ch 22 04절"), "호출 한도 <code>ModelCallLimitMiddleware</code> · 한도에 닿으면 한도가 끼운 글로 끝남", "실행 2의 호출 한도 2"),
    (link(L_CH26_04, "Ch 26 04") + "·" + link(L_CH26_05, "05절"), "한도가 끼운 끝 메시지는 사용량이 <code>None</code> · 자르기 <code>[:-1]</code> · 한도를 하나 줄인 실행과 완료 조건(05)", "함수 <code>model_part</code>"),
]

RESULT_ROWS = [
    ("호출 한도", "4", "2", "바꾼 값"),
    ("메시지를 차례대로 본 출력", "도구 요청 <code>search_documents</code> → <code>check_source</code> · 마지막 응답은 도구 요청 없음", "실행 1과 한 줄도 다르지 않음", "모델 판단 값(다섯 번·두 커널 같음)"),
    ("마지막 메시지", "모델이 쓴 답 · 사용량 기록 있음", "<code>Model call limits exceeded: run limit (2/2)</code> · 사용량 기록 <code>None</code>", "한도에 닿으면 라이브러리가 정하는 값"),
    ("요청 수 · 도구를 요청한 응답 수 · 03절 셈", "<code>3</code> · <code>2</code> · <code>True</code>", "<code>2</code> · <code>2</code> · <code>False</code>", "모델 판단 값(다섯 번·두 커널 같음)"),
    ("네 모드(검색어 뺌)", "모두 <code>True</code>", "모두 <code>True</code>", "같은 궤적이면 늘 같은 판정"),
    ("공통 칸 도구 요청 수 · 걸린 초 · 점수", "<code>2</code> · <code>None</code> · <code>1.0</code>", "<code>2</code> · <code>None</code> · <code>1.0</code>", "세는 값 · 재지 않음 · 모드 <code>strict</code> 판정"),
    ("답 글 · 토큰 수", "5절 둘째 셀 · 7절 첫 셀 출력", "7절 첫 셀 출력", "흔들리는 값 — 아래 표"),
]

TOKEN_ROWS = [
    ("실행 1(호출 한도 4)", "996"),
    ("실행 2(호출 한도 2)", "615"),
]

B4_ANALOGY = "<p>01절부터 쓴 오르골 종이띠 비유를 이어 갑니다. 이번에는 곡 하나를 울린 띠를 나무판에 펴 붙이고, 판 왼쪽에 카드를 한 장 둡니다. 카드에는 기계를 몇 번 돌렸는지를 점으로 찍습니다. 기계에 멈춤쇠를 걸어 두면, 정해 둔 만큼 돌린 뒤 기계가 서고 띠 끝에 구멍 없는 회색 종이가 붙어 나온다고 해 봅니다. 띠와 카드를 한 판에 붙여 함께 보는 것이 이 절의 조립입니다.</p><p>두 띠를 구멍 자리만 대 보면, 앞부분 구멍은 같고 길이도 같습니다. 끝을 보면 위 띠는 구멍 무리로 끝나고, 아래 띠는 회색 종이로 끝납니다. 카드의 점도 위는 셋, 아래는 둘입니다. 띠가 궤적, 앞부분 구멍이 도구 요청, 회색 종이가 호출 한도가 끼운 끝 메시지입니다. 멈춤쇠가 호출 한도이고, 카드가 공통 칸 한 줄입니다.</p><p>비유와 다른 점도 있습니다. 오르골 띠는 기계에 넣기 전에 구멍을 뚫어 두지만, 궤적은 에이전트를 실행하면서 만들어집니다. 또 그림에는 멈춤쇠와 오르골 기계가 없고, 판에 붙인 띠와 카드만 있습니다.</p>"

LOOK_B5 = "노트북 5절과 6절 첫 셀에서 메시지를 차례대로 본 출력이 호출 한도 줄 말고는 같은지 봅니다. 두 실행의 둘째 셀에서 <code>사용량 기록이 없는가:</code> 뒤의 값을 견줍니다. 셋째 셀에서 03절 셈이 <code>True</code>와 <code>False</code>로 갈리는지 확인합니다."
LOOK_B6 = "노트북 7절 첫 셀에서 두 줄의 요청 수 칸과 점수 칸을 봅니다. 둘째 셀에서 <code>점수가 1.0인 실행: 2 | 셈이 맞은 실행: 1 | 전체 실행: 2</code>를 확인합니다. 교재 출력의 토큰 수는 다시 실행하면 달라질 수 있습니다."

B7_ITEMS = [
    "질문·기준 궤적·도구 둘·시스템 메시지 글·실행 한도는 03절과 같은 값으로 실행 전에 정했습니다. 호출 한도 4와 2도 실행 전에 정했습니다. 4는 03절과 같은 값이고, 2는 03절 셈으로 드는 요청 3보다 하나 모자란 값입니다. 흐름을 보여 주려고 정한 예이고, 결과를 보고 바꾸지 않았습니다.",
    "노트북을 쓰기 전에 두 실행을 노트북 밖에서 다섯 번씩 보냈습니다. 두 실행 모두 다섯 번 다 모델은 도구 둘을 같은 차례로 불렀고, 실행 2는 다섯 번 모두 한도에 닿았습니다. 그래도 같은 요청이 늘 같은 도구를 고른다고 할 수는 없습니다. 같은 요청도 실행한 때에 따라 모델이 고르는 도구가 달라질 수 있습니다.",
    "실행 2는 도구 둘을 모두 부른 뒤 한도에 닿아, 궤적의 메시지 수가 기준과 같았습니다. 한도를 1로 두고 모델이 먼저 검색을 요청하면, 검색 뒤에 멈춰 궤적이 짧아집니다. 02절 4절의 검색만 한 궤적과 같은 모양이라, 네 모드의 뜻대로라면 모드 <code>subset</code>만 참이 될 것입니다. 이 장면은 이번에 실행하지 않았습니다.",
    "03절의 평가 모델과 01절의 최종 답 평가는 붙이지 않았습니다. 두 실행에 평가 모델을 한 번씩 부르면 요청이 7번이 됩니다. 최종 답 평가는 실행 1의 답 글이 기준 답과 글자까지 같아야 참이라, 모델이 쓴 글에 따라 흔들립니다. 최종 답 평가는 마지막 글을 기준 답과 글자로 견주므로, 실행 2의 끝 메시지 글이면 거짓이 될 것입니다. 두 방법이 실행 2를 어떻게 판정하는지는 이번에 실행하지 않았습니다.",
    "공통 칸의 도구 요청 수는 도구 이름의 수이고, 03절 셈에는 도구를 요청한 응답 수를 넣었습니다. 이번 두 실행은 응답마다 도구를 하나씩 요청해 두 수가 같았습니다. 한 응답이 도구를 여럿 요청하면 두 수가 달라지니, 04절에서 본 것처럼 셈에는 응답 수를 넣습니다.",
    "함수 <code>model_part</code>는 마지막 메시지의 사용량 기록이 <code>None</code>인지로 끝 메시지를 가려냅니다. 끝 메시지의 글은 설치판 langchain 1.4.0이 정한 영어 글이라, 판이 바뀌면 달라질 수 있습니다. 도구 파일 88~96행의 함수 <code>sum_usage</code>는 응답마다 사용량 칸을 바로 읽어, 사용량이 <code>None</code>인 끝 메시지를 넘기면 <code>TypeError</code>로 멈춥니다. 그래서 함수 <code>model_part</code>로 끝 메시지를 뺐습니다.",
    "점수 칸에는 두 실행 모두 모드 <code>strict</code>(검색어 뺌)의 판정을 담았습니다. 04절의 두 기록은 점수 칸의 잣대가 달랐지만, 이 절의 두 줄은 같은 잣대입니다. 이번에는 네 모드가 모두 참이라, 다른 모드를 담았어도 두 줄 모두 1.0입니다.",
    "호출 한도는 조립 함수 안에서 실행마다 새로 만들었고, 03절처럼 invoke 한 번마다 셉니다. 실행 한도 20에는 두 실행 모두 닿지 않았습니다. 이 노트북의 <code>assert</code>는 키 확인 셀뿐이고, 모델이 고른 값에는 걸지 않았습니다.",
    "교재 출력의 토큰 수는 실행 1 996, 실행 2 615였습니다. 노트북 밖 다섯 번의 토큰으로 요금표를 어림하면, 두 실행을 합쳐 약 0.0016달러입니다. 요금표는 2026-09-17 mini 값이고, 청구 금액이 아닙니다.",
    "교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다. 걸린 시간은 재지 않았습니다.",
]

QUIZ = [
    ("[하] 실행 2에서 바꾼 값은 무엇이고, 메시지를 차례대로 본 출력은 실행 1과 어떻게 달랐나요?",
     "호출 한도를 4에서 2로 바꿨습니다. 메시지를 차례대로 본 출력은 호출 한도 줄 말고는 실행 1과 한 줄도 다르지 않았습니다. 차이는 마지막 메시지의 글과 사용량 기록에서 보였습니다. 틀렸다면 노트북 6절 첫 셀과 둘째 셀을 다시 읽습니다."),
    ("[중] 실행 2의 모델 요청 수와 도구를 요청한 응답 수는 몇이었고, 03절 셈은 어떻게 되었나요?",
     "둘 다 2였고, 셈 「요청 수 = 도구를 요청한 응답 수 + 1」은 <code>False</code>였습니다. 셋째 요청 전에 호출 한도에 닿아, 답을 쓴 응답이 없었기 때문입니다. 노트북 밖 다섯 번과 새 커널 두 번에서 같은 값이었습니다. 틀렸다면 노트북 6절 셋째 셀을 다시 읽습니다."),
    ("[중] 답을 쓰지 못한 실행 2를, 검색어를 뺀 네 모드가 모두 참으로 본 까닭은 무엇인가요?",
     "네 모드는 도구 요청을 견주고, 메시지 글은 견주지 않습니다. 실행 2는 도구 요청 둘이 기준과 같았습니다. 모드 <code>strict</code>가 보는 메시지 수·역할·차례도, 끝 메시지가 도구를 요청하지 않는 응답이라 기준과 같았습니다. 틀렸다면 노트북 6절 넷째 셀을 다시 읽습니다."),
    ("[상] 같은 에이전트에 호출 한도 3을 주면, 모델 요청 수와 03절 셈, 네 모드는 어떻게 될 것으로 어림하나요?",
     "호출 한도는 모델 요청 전에 센 수를 봅니다. 셋째 요청 전에 센 수는 2라 한도 3 안이어서, 셋째 요청이 나가 답까지 갈 것입니다. 그러면 실행 1처럼 요청 3·셈 <code>True</code>·네 모드 <code>True</code>로 어림합니다. 다만 모델이 도구 둘을 같은 차례로 부를 때의 어림이고, 한도 3은 이번에 실행하지 않았습니다. 틀렸다면 노트북 6절 첫 설명과 본문 「한도에 닿은 실행의 끝」을 다시 읽습니다."),
]


def quiz_html() -> str:
    parts = ['<details class="quiz" open><summary>문제 4개 · 해설 포함</summary>']
    number = 1
    for question, answer in QUIZ:
        parts.append('<p class="quiz-q">' + str(number) + ". " + question + '</p><p class="quiz-a">' + answer + "</p>")
        number = number + 1
    parts.append("</details>")
    return "".join(parts)


def runs_paragraph() -> str:
    return "<p>새 커널로 두 번 실행해 견주자, 코드 셀 스물넷의 출력이 셀마다 모두 같았습니다. 답 글과 토큰 수도 두 번 같았고, 노트북 밖 다섯 번의 값과도 같았습니다. 그래도 둘은 모델과 서비스가 정한 값이라, 셈·모드 판정·세는 칸만 결론과 그림에 썼습니다.</p>\n"


def src_html() -> str:
    learned = table_html(["절", "배운 것", "실습에서 쓰는 곳"], LEARNED_ROWS)
    results = table_html(["확인한 것", "실행 1(호출 한도 4)", "실행 2(호출 한도 2)", "값의 성격"], RESULT_ROWS)
    tokens = table_html(["실행", "공통 칸 토큰 수(교재 출력)"], TOKEN_ROWS)
    b7 = ""
    for item in B7_ITEMS:
        b7 = b7 + "<li>" + item + "</li>"
    return ("""<!--meta: 실습 30분 | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 0 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>평가받는 에이전트·네 모드·공통 칸을 한 흐름에 모아, 에이전트를 실행하고 두 방법으로 평가할 수 있습니다.</li>
<li>호출 한도 하나만 바꾼 두 실행을 네 모드와 공통 칸 두 줄로 견줄 수 있습니다.</li>
<li>네 모드가 가려내지 못한, 한도에 닿은 실행을 요청 수 셈과 끝 메시지로 가려낼 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>이 챕터에서는 에이전트를 평가하는 방법을 절마다 따로 익혔습니다. """ + link(L_01, "01절") + "·" + link(L_02, "02절") + """은 궤적 맞춰 보기, """ + link(L_03, "03절") + """은 실제 에이전트와 평가 모델, """ + link(L_04, "04절") + """은 운영 지표를 봤습니다. 서비스에서는 에이전트가 늘 답까지 가지는 않습니다. 요금을 막으려고 붙인 호출 한도에 닿아, 답을 쓰기 전에 멈추는 실행도 생깁니다.</p>
<p>이번 실습은 03절의 평가받는 에이전트를 호출 한도 4와 2로 한 번씩 실행하고, 두 실행을 평가합니다. 한도에 닿은 실행은 """ + link(L_CH22_04, "Ch 22 04절") + """에서 본 안내 메시지로 끝납니다. """ + link(L_CH26_04, "Ch 26 04절") + """은 이 메시지를 「호출 한도가 적어 넣은 글」이라고 불렀고, 이 절에서는 한도가 끼운 끝 메시지라고 부릅니다.</p>
<p>그 끝 메시지의 사용량 기록이 <code>None</code>이라는 것은 Ch 26 04절에서 봤습니다. """ + link(L_CH26_05, "Ch 26 05절") + """도 호출 한도를 하나 줄여 완료 조건이 <code>False</code>가 되는 것을 봤습니다. 새로 볼 것은 이 챕터의 평가 방법, 곧 네 모드와 공통 칸·요청 수 셈이 그런 실행을 어떻게 판정하는지입니다.</p>
<p>이번 절은 이 챕터의 실습입니다. 01~04절과 앞 챕터에서 쓴 이름만 쓰고, 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p>
<p><strong>이 절의 질문</strong> — 호출 한도에 닿아 답을 쓰지 못한 실행을, 궤적 맞춰 보기의 네 모드는 거짓으로 판정할까요? 판정하지 못한다면 무엇으로 가려낼 수 있을까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>이번 실습은 아래 절에서 배운 이름을 그대로 씁니다. 함수는 도구 파일 <code>eval_tools.py</code>에서 가져오고, 조립 함수와 결과를 볼 함수 셋은 노트북에 적습니다.</p>
""" + learned + """
<p>붙인 기능은 03절의 평가받는 에이전트, 02절의 네 모드와 도구별 덮어쓰기, 04절의 공통 칸 셋입니다. 셋이 모두 흐름 안에서 일하도록 했습니다. 03절의 조립과 셈은 두 실행 모두에 쓰고, 02절의 네 모드는 두 궤적을 판정합니다. 04절의 공통 칸은 두 실행을 한 표에 모으고, 점수와 셈으로 실행 수를 셉니다.</p>
<p>03절의 평가 모델은 붙이지 않았습니다. 두 실행에 한 번씩 부르면 요청이 7번이 되어, 실습의 요청 수 3~5번을 넘기 때문입니다. 01절의 최종 답 평가도 붙이지 않았습니다. 실행 1의 답 글은 모델이 쓴 글이라, 기준 답과 글자까지 같다고 늘 말할 수 없기 때문입니다. 04절의 95 백분위수는 줄이 둘이면 늘 가장 큰 값이라 쓰지 않았습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3>""" + B4_ANALOGY + """
""" + illustration_block() + """<h3>실습 조립의 구성</h3><p>조립 함수 <code>run_agent</code>는 호출 한도 하나만 인자로 받습니다. 모델·도구 둘·시스템 메시지 글·질문·실행 한도는 앞 셀에서 만든 이름을 두 실행이 그대로 씁니다. 결과 메시지는 함수 <code>four_modes</code>와 <code>count_asked</code>·<code>model_part</code>·<code>run_row</code>가 두 실행 모두 같은 모양으로 봅니다. 공통 칸 한 줄은 04절 함수 <code>show_row</code>로 출력합니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>한도에 닿은 실행의 끝</h3><p>""" + link(L_CH22_04, "Ch 22 04절") + """에서 본 것처럼, 호출 한도는 모델 요청 전에 그때까지 센 요청 수를 봅니다. 센 수가 한도에 닿았으면 모델을 부르지 않고, 한도가 적은 글 하나를 응답으로 끼운 뒤 실행을 끝냅니다. 설치판 langchain 1.4.0 <code>agents/middleware/model_call_limit.py</code> 37~60행이 그 글을 만들고, 168~208행이 끝으로 보냅니다. """ + link(L_CH26_04, "Ch 26 04절") + """에서 본 것처럼, 이 끝 메시지는 모델 요청으로 받은 응답이 아니라 사용량 기록이 <code>None</code>입니다.</p><p>이 절의 궤적에는 요청이 3번 듭니다. 호출 한도가 2면 셋째 요청 전에 센 수가 2라, 셋째 요청이 나가지 않습니다. 그러면 궤적은 도구 요청 둘과 도구 메시지 둘 뒤에 끝 메시지가 붙은 모양이 됩니다. 이 모양을 네 모드와 공통 칸이 어떻게 판정하는지는 노트북 6·7절에서 봅니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 03절과 같은 질문·기준 궤적·도구 둘과, 검색어를 뺀 평가 함수 넷을 만듭니다. 3절은 시스템 메시지 글·실행 한도와 조립 함수를, 4절은 결과를 볼 함수 셋을 적습니다. 5절은 호출 한도 4인 실행 1을, 6절은 호출 한도만 2로 바꾼 실행 2를 실행하고 판정합니다. 7절에서 두 실행을 공통 칸 두 줄로 모아 셉니다.</p><p>실제 OpenAI 모델 <code>gpt-5.4-mini</code>를 temperature 0으로 부르고, 평가 모델은 부르지 않습니다. 모델 요청은 5절에서 3번, 6절에서 2번, 모두 5번이었고, 노트북 밖 다섯 번과 새 커널 두 번에서 같았습니다. 요금표로 어림한 예상 비용은 두 실행을 합쳐 0.002달러 아래이고, 청구 금액이 아닙니다. 읽는 파일은 <code>.env</code>와 도구 파일 <code>eval_tools.py</code>이고, 쓰는 파일은 없습니다. 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
<h3>실행 1의 실제 순서</h3>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>두 실행은 질문·도구·시스템 메시지 글·실행 한도·조립 함수가 같고, 호출 한도만 달랐습니다. 아래 표는 노트북 5·6·7절 출력에서 코드가 정하는 값과, 모델이 정한 값을 모은 것입니다.</p>
""" + results + """
<p>노트북 밖 다섯 번과 두 커널에서 모두, 두 실행은 도구 둘을 같은 차례로 불렀습니다. 실행 1은 셋째 요청에서 답을 썼고, 요청 수 3은 도구를 요청한 응답 수 2에 1을 더한 값과 같았습니다. 실행 2는 셋째 요청 전에 호출 한도에 닿아, 한도가 끼운 끝 메시지로 끝났습니다. 요청 수 2는 도구를 요청한 응답 수와 같았고, 03절 셈은 맞지 않았습니다.</p>
<p>그런데 두 실행 모두 네 모드가 참이었습니다. 네 모드는 도구 요청을 견주고, 메시지 글은 견주지 않습니다. 모드 <code>strict</code>는 메시지 수·역할·차례까지 봅니다. 실행 2의 끝 메시지는 도구를 요청하지 않는 응답이라, 기준 궤적의 답과 같은 자리로 보였습니다. 그래서 공통 칸의 점수 칸은 두 줄 모두 1.0이었고, 요청 수 칸만 두 줄을 갈랐습니다.</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>도구를 모두 부른 뒤 한도에 닿은 실행은, 답을 쓰지 못했어도 네 모드로는 통과했습니다. Ch 26 05절의 완료 조건처럼, 그 실행을 가려낸 것은 요청 수 셈과 끝 메시지의 사용량 기록이었습니다. 궤적 맞춰 보기는 도구를 기준대로 불렀는지를, 운영 지표는 실행이 어떻게 끝났는지를 봅니다. 두 방법을 함께 봐야 두 실행의 차이가 드러납니다.</p>
<p>아래 표는 두 실행의 교재 출력 토큰 수입니다. 실행 2에는 셋째 요청이 없어 토큰 수가 적었지만, 토큰 수는 다시 실행하면 달라질 수 있어 결론에 쓰지 않았습니다.</p>
""" + tokens + """
""" + runs_paragraph() + """<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul>""" + b7 + """</ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>03절의 평가받는 에이전트, 02절의 네 모드와 도구별 덮어쓰기, 04절의 공통 칸을 한 흐름에 모았습니다.</li><li>호출 한도를 4에서 2로 줄이자, 실행 2는 도구 둘을 부른 뒤 한도가 끼운 글로 끝났고 03절 셈이 <code>False</code>였습니다.</li><li>두 실행 모두 네 모드가 참이었고, 한도에 닿은 실행은 요청 수 셈과 끝 메시지로 가려냈습니다. 둘째·셋째 줄의 값은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 29와 Part 6이 끝납니다. """ + link(L_CH30_01, "Part 7 Ch 30 01절") + """에서는 웹 서비스가 받을 요청과 내놓을 응답의 모양을 정합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>""" + quiz_html() + """
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li>""" + link(L_03, "03절") + """ — 평가받는 에이전트, 호출 한도 4와 실행 한도 20, 셈 「요청 수 = 도구를 요청한 응답 수 + 1」.</li><li>""" + link(L_02, "02절") + """과 """ + link(L_04, "04절") + """ — 네 모드와 도구별 덮어쓰기, 운영 지표와 공통 칸.</li><li>설치판 langchain 1.4.0 <code>agents/middleware/model_call_limit.py</code> 37~60행은 한도가 끼우는 끝 메시지의 글을 만듭니다. 168~208행은 모델 요청 전에 센 수를 보고 끝으로 보내고, 236~251행은 요청 뒤에 수를 더합니다.</li><li>""" + link(L_CH22_04, "Ch 22 04절") + """ — 호출 한도 <code>ModelCallLimitMiddleware</code>와 한도에 닿은 실행의 끝.</li><li>""" + link(L_CH26_04, "Ch 26 04") + "·" + link(L_CH26_05, "05절") + """ — 한도가 끼운 끝 메시지의 사용량 기록과, 그 메시지를 빼고 세는 자르기.</li><li>기준 버전은 노트북 1절 첫 셀에서 설치한 패키지 넷의 판입니다.</li></ul>
""")


def write_src(path: Path) -> Path:
    path.write_text(src_html(), encoding="utf-8")
    return path


if __name__ == "__main__":
    author_04.check_contracts()
    check_tools()
    check_same_as_prev()
    check_same_as_probe()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "eval_tools.py").write_text(TOOLS_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    if "--try" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--try") + 1])
        write_tools(target / "eval_tools.py")
        print("wrote", write_notebook(target, "05", SLUG, "experiment", notebook_cells()))
        print("wrote", write_src(target / "src.html"))
        raise SystemExit(0)
    print("wrote", write_src(SRC))
    if "--src-only" not in sys.argv:
        # 도구 파일은 없거나 01~04판·이 판일 때만 쓴다. 뒤 판이 함수를 더한 판이면 덮어쓰지 않는다(Ch 24 마감 A-10·Ch 25~28 교훈).
        write_tools(TOOLS_PATH)
        path = write_notebook(LAB, "05", SLUG, "experiment", notebook_cells())
        print("wrote", path)
