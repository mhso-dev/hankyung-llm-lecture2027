"""Ch 27 02절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 -B author_02.py            → 도구 파일(없거나 이 판일 때만) + 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_02.py --src-only → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_02.py --tools-copy DIR → 디스크의 도구 파일을 DIR에 복사한다(새 커널 사본 실행용 — Ch 26 A-19 교훈)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**.
슬러그 `02-create-deep-agent와-도구` 그대로(Part 6 목차와 01절 b8이 링크), 제목 「create deep agent와 도구」 그대로(강사 확인).

## 결정 1 — M2: 앞 절반 모델 없음 + 뒤 절반 실제 모델 (챕터 리드 결정 1)

nbkit.key_and_model_cells("openai:gpt-5.4-mini") — temperature=0·reasoning_effort="none", 키는 루트 .env에서만(값 출력 없음).
2~4절은 모델을 부르지 않는다(도구만 직접 실행, 조립·백엔드 확인). 6절에서 Deep Agent를 한 번 실행한다(모델 요청 2번 — 도구를 한 번 부를 때).
가짜 채팅 모델 없음(규격 §3). 모델 객체를 create_deep_agent(model=model)에 넘긴다(01절 b7 — 문자열이면 temperature 없는 모델을 새로 만듦).

## 결정 2 — 도구와 소재 (챕터 리드 결정, 인계 3번)

교육센터 자료실 규정 넷(Ch 21 01 POLICIES의 대출·운영·연체 문장 그대로 + Ch 26 01 loan_rules의 연장 두 문장) + @tool lookup_rule(topic: str).
없는 주제어는 오류 대신 정해 둔 글(평범한 함수 — 규격 §3). Ch 21 01 lookup_policy와 이름을 달리해 같은 이름·다른 본문을 피함.

## 결정 3 — 모델에게 가는 도구 목록과 백엔드 (인계 4번)

그래프 도구 열(기본 아홉 + lookup_rule) ↔ 기록 훅(@wrap_model_call, Ch 22 02 모양)이 적은 요청마다 도구 이름 → execute 빠짐.
「백엔드」를 이 절에서 처음 정의. 기본 StateBackend는 supports_execution False(설치판 filesystem.py 1156행 함수), 값 바꿔 보기로
LocalShellBackend를 만들기만 해 True를 본다(에이전트에 넘기지 않음 — 이 컴퓨터에서 명령을 그대로 실행하는 백엔드).

## 결정 4 — 안전 규칙 (가)·(나)와 요청 수 셈 (챕터 공통)

바깥 middleware=[ModelCallLimitMiddleware(run_limit=3, exit_behavior="end"), record_tool_names] +
같은 이름 general-purpose 명세(자기 호출 한도 2, tools 없음 → lookup_rule 물려받음, graph.py 728행).
요청 수 = 이번 실행이 더한 메시지만 잘라 sum_usage(Ch 26 01 방법) = 기록 훅 요청 수. 서브에이전트 요청은 둘 다에 없음(한계 공개).

## 결정 5 — 흔들림 먼저 확인 (qa/upgrade/02-probe.md)

노트북 밖 P1 5번(요청 10번, §0은 첫 요청 전 12:13Z): 구조 값·모델 판단 값(lookup_rule 한 번, task 0, 요청 2) 모두 5/5 → 입력 그대로.
assert는 키 셀뿐(도구 선택·모델 글·요청 수에 없음). 흔들리는 값(도구 메시지 내용·답 글·토큰·비용)은 [[READ_…]] 자리 표시 → 교재 출력(A) 뒤 mdpatch.py.

## 결정 6 — 도구 파일 harness_tools.py를 이 절이 처음 만든다 (챕터 리드 결정 6, B안)

Ch 21 runner_tools.py(f4113158…)에서 이 노트북이 쓰는 앞 챕터 함수 넷(tool_call_names·show_messages·sum_usage·estimate_cost)의 설명 주석과 본문을
글자 그대로 옮기고(Ch 26 delegation_tools.py c3c1709a… 판과도 대조), 01절 노트북 셀의 tool_names·names_only_in을 셀 글 그대로 옮긴다.
import 0. 쓰기 가드: 파일이 없거나 이 판과 같을 때만 쓰고, 뒤 절이 함수를 더한 판(strip_later_imports 뒤 이 판으로 시작)은 건너뜀.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·변수 힌트·대입 풀기·별표 풀기·
`while`·`try`·세미콜론·`isinstance`·클래스. 힌트는 @tool 매개변수 `: str`만, 데코레이터는 @tool과 @wrap_model_call(규격 §2-2 L6, Ch 22 02)만. 호출 깊이 2 이하.
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(HERE))
import author_01  # noqa: E402  01절 셀 글(tool_names·names_only_in)·본문 도우미
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch27-deepagents/notebooks"
FIGS = ROOT / "textbook/part6/ch27-deepagents/figures"
SLUG = "02-create-deep-agent와-도구"
TITLE_TEXT = "create deep agent와 도구"
SRC = ROOT / "textbook/part6/ch27-deepagents/_src" / (SLUG + ".html")
NB01 = LAB / "01-하네스와-일곱-기능.ipynb"
TOOLS_PATH = LAB / "harness_tools.py"
RUNNER = ROOT / "labs/part6/ch21-create-agent/notebooks/runner_tools.py"
RUNNER_SHA = "f4113158c0ccaee1205f0eabe315ef153e14c4dc6bcfd70ae8a9378edda96bdf"
DELEGATION = ROOT / "labs/part6/ch26-delegation/notebooks/delegation_tools.py"
# 전체 마감(2026-09-30)에서 Ch 26 도구 파일 머리 설명 첫 줄만 고쳐 c3c1709a… → 0748a8eb…(함수 본문 같음)
DELEGATION_SHA = "0748a8eb7fa0e0886521a616d373f87d3453a4d405e70f38782e9001bf2d4de4"
html_text = author_01.html_text
table_html = author_01.table_html
mermaid_block = author_01.mermaid_block


def placeholder(name: str) -> str:
    """교재 출력(A) 뒤 mdpatch.py로 채울 자리 표시(흔들리는 값의 둘째 단락·b6 표)."""
    return "[[READ_" + name + "]]"


# ---------------------------------------------------------------- 도구 파일 harness_tools.py (첫 판)
TOOLS_HEAD = '''"""Ch 27 DeepAgents — 앞 챕터와 이 챕터에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from harness_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
이 챕터 노트북이 실제로 쓰는 함수만 담고, 새 함수가 필요한 절이 그때 더합니다.
Ch 21 도구 파일 runner_tools.py에서 옮긴 함수는 설명 주석과 본문을 글자 그대로 옮겼습니다.
Ch 16 도구 파일 guardrails.py에서 옮긴 find_source_marks는 몸통 첫 줄 주석까지 글자 그대로 옮겼습니다.
이 챕터 01절·07절 노트북에서 옮긴 함수는 그 셀의 주석과 본문을 글자 그대로 옮겼습니다.
앞 챕터 도구 파일은 이 챕터 실습 폴더에 없는 패키지(numpy 등)를 가져오거나 그 챕터 폴더에 묶여 있어,
파일째 가져오지 않습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
도구를 만드는 @tool 줄과 에이전트를 만드는 create_deep_agent 줄은 이 파일에 두지 않고 노트북에 둡니다.
"""
'''

RUNNER_NOTES = [
    ("tool_call_names", "Ch 19 04절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다"),
    ("show_messages", "Ch 19 06절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다"),
    ("sum_usage", "Ch 19 05절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다"),
    ("estimate_cost", "Ch 6 06절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다"),
]
NOTE_01 = "Ch 27 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다"
CELLS_01 = [("tool_names", author_01.DEF_TOOL_NAMES), ("names_only_in", author_01.DEF_ONLY_IN)]
TOOL_ORDER = ["tool_call_names", "show_messages", "sum_usage", "estimate_cost", "tool_names", "names_only_in"]


def file_block(text: str, name: str) -> str:
    """도구 파일 글에서 함수 하나의 설명 주석(배운 곳 줄 뺌)과 본문을 글자 그대로 꺼냅니다(Ch 26 author_01과 같은 함수)."""
    lines = text.splitlines()
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            start = node.lineno - 1
            top = start
            while top > 0 and lines[top - 1].startswith("#"):
                top = top - 1
            # 맨 위 한 줄은 「…에서 배웠습니다」 줄이라 빼고, 그 아래 설명 주석부터 가져옵니다
            return "\n".join(lines[top + 1:node.end_lineno])
    raise KeyError(name)


def notebook_code_sources(path: Path) -> list:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    found = []
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            source = cell["source"]
            if isinstance(source, list):
                source = "".join(source)
            found.append(source)
    return found


def tools_text() -> str:
    runner = RUNNER.read_text(encoding="utf-8")
    assert hashlib.sha256(runner.encode("utf-8")).hexdigest() == RUNNER_SHA, "Ch 21 runner_tools.py가 마감 판과 다릅니다"
    text = TOOLS_HEAD
    for name, note in RUNNER_NOTES:
        text = text + "\n\n# " + note + "\n" + file_block(runner, name) + "\n"
    for name, cell_source in CELLS_01:
        text = text + "\n\n# " + NOTE_01 + "\n" + cell_source + "\n"
    return text


TOOLS = tools_text()


def strip_later_imports(text: str) -> str:
    """머리 설명과 첫 함수 주석 사이에 뒤 절이 더한 가져오기 줄이 있으면 빼고 내놓습니다(Ch 25·26 대조 사슬과 같은 줄).

    뒤 절 판이 02절 판을 그대로 이어 쓰는지 볼 때는, 이 가져오기 줄을 빼고 앞머리를 견줍니다.
    """
    if not text.startswith(TOOLS_HEAD):
        return text
    rest = text[len(TOOLS_HEAD):]
    first = rest.find("\n\n# Ch ")
    if first <= 0:
        return text
    return TOOLS_HEAD + rest[first:]


def check_tools() -> None:
    """도구 파일 02절 판의 함수 여섯이 원본(Ch 21 runner_tools.py·Ch 26 delegation_tools.py·01절 노트북 셀)과 글자·AST 모두 같은지 봅니다."""
    runner = RUNNER.read_text(encoding="utf-8")
    delegation = DELEGATION.read_text(encoding="utf-8")
    assert hashlib.sha256(delegation.encode("utf-8")).hexdigest() == DELEGATION_SHA, "Ch 26 delegation_tools.py가 마감 판과 다릅니다"
    tree = ast.parse(TOOLS)
    names = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise AssertionError("02절 판 도구 파일은 아무것도 가져오지 않습니다")
    assert names == TOOL_ORDER, names
    runner_tree = ast.parse(runner)
    for name, note in RUNNER_NOTES:
        block = file_block(runner, name)
        assert ("# " + note + "\n" + block + "\n") in TOOLS
        assert file_block(delegation, name) == block, name + "가 Ch 26 판과 다릅니다"
        mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        theirs = [ast.dump(n) for n in runner_tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        assert mine == theirs and len(mine) == 1, name
    sources_01 = notebook_code_sources(NB01)
    for name, cell_source in CELLS_01:
        assert cell_source in sources_01, name + "가 01절 노트북 셀과 다릅니다"
        assert ("# " + NOTE_01 + "\n" + cell_source + "\n") in TOOLS
        mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        theirs = [ast.dump(n) for n in ast.parse(cell_source).body if isinstance(n, ast.FunctionDef)]
        assert mine == theirs and len(mine) == 1, name


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["deepagents==0.7.0", "langchain==1.4.0", "langchain-openai==1.6.0", "python-dotenv==1.2.3"])

IMPORTS = r'''# Deep Agents(01절)·백엔드(이 절 처음)·미들웨어(Ch 22)·모델(Ch 6 01절)·메시지(Ch 13 04절)·도구(Ch 19 01절) 이름을 가져옵니다
from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend, StateBackend
from deepagents.middleware.filesystem import supports_execution
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_model_call
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain.tools import tool
# 앞 챕터와 01절에서 배운 함수 여섯은 도구 파일에서 가져옵니다
from harness_tools import estimate_cost, names_only_in, show_messages, sum_usage, tool_call_names, tool_names

print("도구 파일에서 가져온 함수:", "estimate_cost, names_only_in, show_messages, sum_usage, tool_call_names, tool_names")'''

RULES = r'''# 도구가 찾을 교재용 규정 글 넷을 주제어마다 정합니다(실제 도서관 규정이 아님)
library_rules = {
    "대출": "일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.",
    "연장": "반납 예정일 전에 한 번, 7일 연장할 수 있습니다. 예약한 사람이 있는 책은 연장할 수 없습니다.",
    "연체": "연체한 일수만큼 새 대출이 제한됩니다.",
    "운영": "평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.",
}
print("규정 주제어:", list(library_rules))'''

DEF_TOOL = r'''# 주제어 하나로 규정 글 하나를 찾는 도구를 만듭니다(맨 @tool 줄 — Ch 19 01절)
@tool
def lookup_rule(topic: str):
    """교육센터 자료실 규정 하나를 주제어로 찾습니다. topic에는 대출, 연장, 연체, 운영 가운데 하나를 넣습니다."""
    # 없는 주제어면 오류 대신 정해 둔 안내 글을 내놓습니다
    if topic in library_rules:
        return library_rules[topic]
    return "그런 주제어의 규정은 없습니다. 대출, 연장, 연체, 운영 가운데 하나를 넣어 주세요."'''

TOOL_INFO = r'''# 모델이 보게 될 도구 이름·설명·인자를 봅니다
print("도구 이름:", lookup_rule.name)
print("도구 설명:", lookup_rule.description)
print("인자:", lookup_rule.args)'''

TOOL_TRY = r'''# 모델 없이 도구만, 있는 주제어와 없는 주제어로 한 번씩 실행합니다(Ch 19 05절 도구.invoke)
print("연장으로 부른 결과:", lookup_rule.invoke({"topic": "연장"}))
print("주차로 부른 결과:", lookup_rule.invoke({"topic": "주차"}))'''

BASE = r'''# 01절처럼 인자 없이 Deep Agent를 만들어, 견줄 기준 도구 목록을 얻습니다(요청은 보내지 않음)
base_agent = create_deep_agent(model=model)
base_tools = tool_names(base_agent)
print("기본 도구 수:", len(base_tools))'''

TOOL_AGENT = r'''# 인자 tools=에 우리 도구 하나를 넘겨 만들고, 도구 수와 이름을 봅니다(요청은 보내지 않음)
tool_agent = create_deep_agent(model=model, tools=[lookup_rule])
tool_list = tool_names(tool_agent)
print("도구 수:", len(tool_list))
print("도구 이름:", tool_list)'''

ADDED = r'''# 기준 목록과 견주어 더해진 도구와 빠진 도구를 봅니다(01절 함수 names_only_in)
added_tools = names_only_in(base_tools, tool_list)
removed_tools = names_only_in(tool_list, base_tools)
print("더해진 도구:", added_tools)
print("빠진 도구:", removed_tools)'''

SAME_NODES = r'''# 두 Deep Agent의 노드 이름이 같은지 봅니다
base_graph = base_agent.get_graph()
tool_graph = tool_agent.get_graph()
print("노드가 같은가:", list(base_graph.nodes) == list(tool_graph.nodes))'''

STATE_BACKEND = r'''# 기본 백엔드를 하나 만들어, 명령 실행을 지원하는지 설치판 함수 supports_execution으로 봅니다
state_backend = StateBackend()
print("백엔드 종류:", type(state_backend).__name__)
print("명령을 실행할 수 있는가:", supports_execution(state_backend))'''

SHELL_BACKEND = r'''# 값 바꿔 보기: 명령을 실행하는 백엔드를 만들기만 하고 같은 함수로 봅니다(에이전트에는 넘기지 않음)
shell_backend = LocalShellBackend()
print("백엔드 종류:", type(shell_backend).__name__)
print("명령을 실행할 수 있는가:", supports_execution(shell_backend))'''

OUTER_LIMIT = r'''# 바깥 에이전트의 모델 요청을 세 번까지로 막는 호출 한도를 만듭니다(01절 6절 모양)
outer_limit = ModelCallLimitMiddleware(run_limit=3, exit_behavior="end")
print("바깥 호출 한도:", outer_limit.run_limit)'''

HELPER_SPEC = r'''# 기본 서브에이전트와 같은 이름의 명세를 만들고, 그 안에 자기 호출 한도 둘을 넣습니다(01절 6절 모양)
helper_limit = ModelCallLimitMiddleware(run_limit=2, exit_behavior="end")
helper_spec = {
    "name": "general-purpose",
    "description": "교재용 도우미입니다. 맡긴 일을 짧게 처리합니다.",
    "system_prompt": "맡긴 일을 두 문장의 한국어로 처리하세요.",
    "middleware": [helper_limit],
}
print("명세의 키:", list(helper_spec))'''

DEF_HOOK = r'''# 모델 요청이 나갈 때마다, 그 요청에 실린 도구 이름을 기록 목록에 붙이는 훅입니다(Ch 22 02절 기록 훅 모양)
@wrap_model_call
def record_tool_names(request, handler):
    names = []
    for item in request.tools:
        names.append(item.name)
    seen_tool_lists.append(names)
    # 기록만 하고, 요청은 그대로 모델에게 보냅니다
    return handler(request)'''

RULE_AGENT = r'''# 우리 도구·호출 한도·기록 훅·명세를 함께 넘겨 Deep Agent를 만듭니다(요청은 아직 보내지 않음)
rule_agent = create_deep_agent(
    model=model,
    tools=[lookup_rule],
    middleware=[outer_limit, record_tool_names],
    subagents=[helper_spec],
)
rule_tools = tool_names(rule_agent)
print("그래프에 등록된 도구 수:", len(rule_tools))
rule_graph = rule_agent.get_graph()
print("노드:", list(rule_graph.nodes))'''

RUN = r'''# 기록 목록을 새로 만들고, 질문 한 줄을 넣어 한 번 실행합니다(우리 도구를 한 번 부르면 모델 요청 2번)
seen_tool_lists = []
question = "교육센터 자료실에서 빌린 책의 반납 날짜를 늘리려면 어떻게 하나요? 두 문장으로 답해 주세요."
first_input = {"messages": [HumanMessage(content=question)]}
result = rule_agent.invoke(first_input)
result_messages = result["messages"]
print("결과 메시지 수:", len(result_messages))'''

SHOW = r'''# 결과 메시지를 차례로 봅니다(Ch 19 06절 함수 show_messages)
print("결과 메시지:")
show_messages(result_messages)'''

FINAL = r'''# 모델이 쓴 마지막 답 글을 봅니다(실행마다 달라질 수 있는 값)
final_answer = result_messages[-1].text
print("마지막 답 글:")
print(final_answer)'''

ASKED = r'''# 넣은 메시지 뒤, 이번 실행이 더한 응답마다 도구 요청 이름을 모읍니다(Ch 19 04절 함수 tool_call_names)
input_count = len(first_input["messages"])
new_messages = result_messages[input_count:]
asked_names = []
for message in new_messages:
    if type(message).__name__ == "AIMessage":
        for name in tool_call_names(message):
            asked_names.append(name)
print("요청한 도구 이름:", asked_names)
print("task를 부른 횟수:", asked_names.count("task"))'''

SEEN = r'''# 기록 훅이 적은 요청 수와, 첫 요청에 실린 도구 이름을 봅니다
print("기록된 모델 요청 수:", len(seen_tool_lists))
first_seen = seen_tool_lists[0]
print("모델이 받은 도구 수:", len(first_seen))
print("모델이 받은 도구 이름:", first_seen)'''

MISSING = r'''# 그래프에 등록된 도구 가운데 모델이 받지 않은 것을 찾고, 요청마다 execute가 있었는지 봅니다
graph_only = names_only_in(first_seen, rule_tools)
print("그래프에만 있는 도구:", graph_only)
for names in seen_tool_lists:
    print("이 요청에 execute가 있는가:", "execute" in names)'''

USAGE = r'''# 이번 실행이 더한 메시지만 Ch 19 05절 함수 sum_usage로 세고, 기록 훅이 센 요청 수와 견줍니다
run_usage = sum_usage(new_messages)
print("응답으로 센 요청 수:", run_usage["requests"])
print("기록 훅이 센 요청 수:", len(seen_tool_lists))
print("입력 토큰:", run_usage["input_tokens"], "| 출력 토큰:", run_usage["output_tokens"])'''

COST = r'''# 2026-09-17 요금표(100만 토큰당 달러)로 이번 실행의 예상 비용을 셉니다(Ch 6 06절 함수 estimate_cost)
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
run_cost = estimate_cost(run_usage, input_rate, cached_input_rate, output_rate)
rounded_cost = round(run_cost, 6)
print("예상 비용(달러):", rounded_cost)'''


def check_same_as_probe() -> None:
    """노트북 셀의 규정 글·도구·명세·훅·에이전트·질문이 흔들림 확인 스크립트(probe02.py)와 같은 글인지 봅니다."""
    probe = (HERE / "probe/probe02.py").read_text(encoding="utf-8")
    pieces = []
    for cell in [RULES, DEF_TOOL, HELPER_SPEC, DEF_HOOK, RULE_AGENT]:
        for line in cell.splitlines():
            if line.startswith("#") or line.startswith("print(") or line.startswith("rule_tools") or line.startswith("rule_graph"):
                continue
            pieces.append(line)
    pieces.append('outer_limit = ModelCallLimitMiddleware(run_limit=3, exit_behavior="end")')
    pieces.append('QUESTION = "교육센터 자료실에서 빌린 책의 반납 날짜를 늘리려면 어떻게 하나요? 두 문장으로 답해 주세요."')
    pieces.append('model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")')
    for piece in pieces:
        assert piece in probe, piece
    assert 'question = "교육센터 자료실에서 빌린 책의 반납 날짜를 늘리려면 어떻게 하나요? 두 문장으로 답해 주세요."' in RUN


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/02-figures.md)
FIG1 = "02-1-우리-도구가-더해진-조립"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 초록 상자 교재용 규정 글 넷에서 파란 상자 도구 lookup_rule로, 거기서 파란 상자 create_deep_agent 인자 tools에 lookup_rule 하나로 화살표가 갑니다. 그 아래 노란 상자 그래프에 등록된 도구 열 기본 아홉과 lookup_rule로 화살표가 갑니다. 그 옆에 노란 상자 기본 백엔드 StateBackend 명령을 실행할 수 있는가 False가 있습니다. 두 노란 상자에서 맨 아래 노란 상자 모델이 받은 도구 아홉 execute만 빠짐으로 화살표가 가는 그림"
FIG1_CAP = "우리 도구 하나를 넘기자 그래프의 도구는 열이 되었고, 모델이 받은 목록에서는 execute 하나만 빠졌습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 우리가 정한 글이고, 파란 상자는 우리가 만든 도구와 부른 함수입니다.
노란 상자는 노트북 출력으로 확인한 값이고, 맨 아래 상자는 6절 기록 훅의 출력입니다.
오른쪽 노란 상자의 백엔드가 명령을 실행하지 못해서, 모델이 받는 목록에서 execute가 빠집니다."""

FIG2 = "02-2-한-번-실행한-차례"
FIG2_ALT = "세로선 셋이 있는 차례 그림입니다. 왼쪽부터 우리 코드, Deep Agent 그래프, 연보라 띠 안의 모델 gpt-5.4-mini입니다. 우리 코드에서 질문 한 줄로 invoke 화살표가 그래프로 갑니다. 그래프에 노란 메모 기록 훅 도구 아홉 execute 없음이 붙고, 요청 1 화살표가 모델로 가고 도구 요청 lookup_rule 점선이 돌아옵니다. 그래프에 노란 메모 도구 실행 노드 ToolMessage 결과 상태 success와 기록 훅 메모가 차례로 붙습니다. 요청 2 화살표가 모델로 가고 도구 요청 없음 점선이 돌아온 뒤, 결과 메시지 넷 점선이 우리 코드로 돌아오는 그림"
FIG2_CAP = "우리 도구를 한 번 부른 실행에서 모델 요청은 두 번이었고, 두 요청 모두 execute가 빠진 도구 아홉을 받았습니다."
FIG2_READ = """위에서 아래로 실행 차례대로 읽고, 세로선은 왼쪽부터 우리 코드, 그래프, 모델입니다.
연보라 띠는 실제로 부른 모델 gpt-5.4-mini의 자리입니다.
노란 메모는 노트북 6절 출력이고, 기록 훅 메모는 요청이 나가기 직전에 적힌 값입니다.
도구는 그래프 안의 도구 실행 노드에서 실행되어, 따로 세로선을 두지 않았습니다.
실선 화살표는 부르는 쪽, 점선 화살표는 내놓은 값이 돌아오는 쪽입니다."""

FIG3 = "02-3-등록된-도구와-받은-도구"
FIG3_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위에 노란 상자 둘이 나란히 있습니다. 왼쪽은 그래프에 등록된 도구 열 파일 도구 일곱 execute task lookup_rule, 오른쪽은 모델이 받은 도구 아홉 파일 도구 일곱 task lookup_rule입니다. 두 상자에서 파란 상자 함수 names_only_in으로 화살표가 가고, 거기서 노란 상자 그래프에만 있는 도구 execute로 화살표가 갑니다. 맨 아래에 회색 상자 general-purpose 서브에이전트가 받는 도구 여덟 파일 도구 일곱과 lookup_rule 소스 확인이 따로 있는 그림"
FIG3_CAP = "그래프에 등록된 도구 열 가운데 모델이 받지 않은 것은 execute 하나였고, 우리 도구는 두 목록 모두에 있었습니다."
FIG3_READ = """위에서 아래로 읽습니다.
위 노란 상자 둘은 같은 에이전트의 두 목록이라 화살표 대신 나란히 두었고, 노트북 5·6절 출력입니다.
파란 상자는 01절에서 배워 도구 파일에서 가져온 함수이고, 그 아래 노란 상자는 6절 출력입니다.
맨 아래 회색 상자는 설치판 소스로 확인한 값이라, 이 노트북에서는 출력하지 않았습니다."""

FIG4 = "02-4-요청-수-두-가지-셈"
FIG4_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위에 초록 상자 둘이 나란히 있습니다. 왼쪽은 바깥 호출 한도 3, 오른쪽은 general-purpose 명세 호출 한도 2입니다. 그 아래 노란 상자 둘이 나란히 있습니다. 왼쪽은 응답으로 센 요청 수 2 sum_usage, 오른쪽은 기록 훅이 센 요청 수 2입니다. 두 노란 상자에서 회색 상자 셈 도구를 요청한 응답 수 1 더하기 1로 화살표가 갑니다. 맨 아래 회색 상자 서브에이전트 요청은 두 셈 모두에 없음이 있는 그림"
FIG4_CAP = "우리 도구를 한 번 부른 실행에서 두 방법으로 센 요청 수는 모두 2였고, 두 호출 한도 안에 들었습니다."
FIG4_READ = """위에서 아래로 읽습니다.
맨 위 초록 상자 둘은 5절에서 정한 두 호출 한도이고, 두 곳에 따로 준 값이라 나란히 두었습니다.
가운데 노란 상자 둘은 노트북 7절 출력이고, 회색 상자는 두 커널과 흔들림 확인에서 모두 맞은 셈입니다.
맨 아래 회색 상자는 이 셈의 한계로, task를 부르면 서브에이전트 요청은 따로 세야 합니다."""

ILLU = "02-5-도구-걸이에-더한-연장"
ILLU_ALT = "흰 바탕에 유리 온실 안을 앞에서 본 그림입니다. 화면 대부분을 차지하는 나무 연장 걸이에 긴 자루 연장이 한 줄로 서 있습니다. 왼쪽부터 초록 자루 갈퀴·괭이·삽·쇠스랑, 검은 전동 예초기, 초록 자루 잎 갈퀴가 서 있습니다. 맨 오른쪽 끝에는 노란 자루 삽이 있습니다. 예초기의 검은 줄은 걸이 고리에 감겨 늘어지고, 줄 끝 플러그 둘은 어디에도 꽂혀 있지 않습니다. 콘센트·사람·글자·숫자·화살표는 없는 그림"
ILLU_CAP = "걸이에 선 연장 줄 오른쪽 끝에 노란 새 삽이 더해졌고, 가운데 전동 예초기는 꽂을 곳이 없어 쓰지 못합니다."
ILLU_READ = "온실 안 나무 걸이에 초록 자루 연장이 한 줄로 서 있고, 오른쪽 끝에 노란 자루 삽이 더해졌습니다. 원래 있던 연장은 모두 제자리에 그대로입니다. 줄 가운데 전동 예초기의 검은 줄 끝 플러그는 매달리거나 바닥에 놓여, 어디에도 꽂혀 있지 않습니다. 걸이의 연장 전체가 그래프에 등록된 도구이고, 노란 삽이 우리 도구, 꽂을 곳 없는 예초기가 <code>execute</code>입니다. 연장 수와 플러그 수는 어떤 값과도 짝짓지 않습니다."

RUNS_SENTENCE = "새 커널로 두 번 실행해 견주자, 코드 셀 스물여섯의 출력이 셀마다 모두 같았습니다. 답 글·토큰·예상 비용이 찍힌 셀도 이번 두 번에서는 같았지만, 모델 출력이라 결론에는 쓰지 않습니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 자료실 규정을 찾는 도구 하나를 만들어 Deep Agent에 더하고, 조립을 모델 없이 봅니다.
2. 그래프에 등록된 도구와 모델에게 가는 도구 목록이 어떻게 다른지, 백엔드와 함께 봅니다.
3. 호출 한도를 두 곳에 준 Deep Agent를 실제 모델로 한 번 실행하고, 도구 선택과 요청 수를 셉니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 6절에서 Deep Agent를 한 번 실행합니다.
모델이 우리 도구를 한 번 부르고 답하면, 모델 요청은 2번입니다.
바깥 호출 한도 3과 서브에이전트 호출 한도 2를 주어, 요청이 끝없이 늘지 않게 막습니다.
요금표로 어림한 예상 비용은 0.004달러 아래이고, 청구 금액이 아닙니다.

모델이 고르는 도구와 답 글은 실행마다 달라질 수 있습니다.
걸린 시간은 재지 않았습니다.
읽거나 쓰는 파일은 없습니다.
앞에서 배운 함수 여섯은 도구 파일 `harness_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 넷을 설치합니다.
판은 deepagents 0.7.0과 langchain 1.4.0입니다.
나머지 둘은 `langchain-openai` 1.6.0과 `python-dotenv` 1.2.3입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~4절을 읽습니다.
우리 도구가 기본 도구에 더해지고, 모델에게 가는 목록에서 `execute`가 빠지는 까닭을 보는 자리입니다.
5~7절은 실제 모델로 실행하고 요청 수를 세는 실습이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch27-deepagents`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def model_cells() -> list[dict]:
    """과정 표준 키·모델 셀(nbkit)에 이 절의 결과 읽기(실행일·요청은 6절에서만)를 붙입니다."""
    cells = key_and_model_cells("openai:gpt-5.4-mini")
    cells[-1] = md("""**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.
모델 요청은 6절 실행 셀에서만 나갑니다.

01절에서 본 것처럼, 함수 `create_deep_agent`에는 이 모델 객체를 그대로 넘깁니다.
모델 이름 글자만 넘기면 temperature 설정이 없는 모델을 새로 만들기 때문입니다.

## 2. 자료실 규정 도구 만들기

Ch 21 01절에서는 교육센터 자료실 규정 셋을 딕셔너리에 담고, 주제어로 찾는 도구를 만들었습니다.
이 절도 같은 규정 글을 쓰고, Ch 26 01절 규정 글의 연장 두 문장을 더합니다.
이 글은 교재용으로 만든 규정이고, 실제 도서관 규정이 아닙니다.
실행 전에 정한 글이고, 결과를 보고 바꾸지 않았습니다.""")
    return cells


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이 절에서는 01절에서 조립만 본 Deep Agent에 우리 도구를 더하고, 실제 모델로 실행합니다.
절 제목의 create deep agent는 함수 `create_deep_agent`의 이름을 띄어 쓴 것입니다.

첫 셀은 패키지 넷을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `deepagents: 0.7.0`과 `langchain: 1.4.0`이 보입니다.
네 판 모두 실습 폴더 잠금과 같은 판입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
백엔드 이름 둘과 함수 `supports_execution`은 이 절에서 처음 쓰고, 뜻은 3·4절에서 풉니다.
함수 `wrap_model_call`은 Ch 22 02절, 미들웨어 `ModelCallLimitMiddleware`는 Ch 22 04절에서 썼습니다.
마지막 가져오기 줄은 앞에서 배운 함수 여섯을 도구 파일 `harness_tools.py`에서 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: estimate_cost, names_only_in, show_messages, sum_usage, tool_call_names, tool_names`가 보입니다.
Ch 19 06절 함수 `show_messages`는 메시지 목록을 한 줄씩 출력합니다.
Ch 19 04절 함수 `tool_call_names`는 응답 하나에 든 도구 요청의 이름을 모읍니다.
Ch 19 05절 함수 `sum_usage`는 목록 안 응답마다 요청 하나로 세고 토큰을 더합니다.
Ch 6 06절 함수 `estimate_cost`는 사용량과 요금표로 예상 비용을 셉니다.

함수 `tool_names`와 `names_only_in`은 01절 3절에서 만든 함수입니다.
앞의 함수는 에이전트 그래프의 도구 이름을, 뒤의 함수는 둘째 목록에만 있는 이름을 모읍니다.

앞에서 배운 함수는 `harness_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다."""),
    ] + model_cells() + [
        code(RULES),
        md("""**결과 읽기** — 출력 줄 `규정 주제어: ['대출', '연장', '연체', '운영']`이 보입니다.
대출·연체·운영 글은 Ch 21 01절 규정 글과 같고, 연장 글은 Ch 26 01절 규정 글의 두 문장입니다.

다음 셀은 이 딕셔너리에서 주제어 하나로 규정 글을 찾는 도구를 만듭니다.
함수 위의 `@tool` 줄은 데코레이터 줄입니다.
데코레이터 줄은 함수 위에 붙여 그 함수를 다른 것으로 감싸는 표시이고, 뜻은 Ch 2 09절에 있습니다.
이 셀에서는 이 줄이 아래 함수를 도구로 등록합니다.
Ch 19 01절처럼 매개변수 `topic: str`은 모델이 채울 인자가 되고, 독스트링은 도구 설명이 됩니다."""),
        code(DEF_TOOL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
Ch 21 01절 도구 `lookup_policy`는 없는 주제어에 오류를 냈습니다.
이 도구는 오류 대신 넣을 수 있는 주제어를 알려 주는 글을 내놓습니다.
모델은 그 글을 보고 주제어를 다시 고를 수 있습니다.
도구 함수는 우리가 쓰는 평범한 Python 함수라서, 정해 둔 글을 내놓아도 됩니다.

다음 셀은 모델이 보게 될 도구 이름과 설명과 인자를 봅니다."""),
        code(TOOL_INFO),
        md("""**결과 읽기** — 출력 줄 `도구 이름: lookup_rule`과 `인자: {'topic': {'title': 'Topic', 'type': 'string'}}`이 보입니다.
도구 설명 줄은 함수의 독스트링과 같은 글입니다.
모델은 이 설명을 읽고, 인자 `topic`에 넣을 주제어를 스스로 고릅니다.

다음 셀은 모델 없이 도구만 두 번 실행합니다.
Ch 19 05절처럼 도구의 `invoke`에 인자 딕셔너리를 넘기면, 모델을 거치지 않고 함수가 실행됩니다."""),
        code(TOOL_TRY),
        md("""**결과 읽기** — 라벨 `연장으로 부른 결과:` 뒤에 연장 규정 두 문장이 보입니다.
라벨 `주차로 부른 결과:` 뒤에는 넣을 수 있는 주제어를 알려 주는 정해 둔 글이 보입니다.
같은 인자를 넣으면 늘 같은 글이 나오는 도구입니다.

## 3. 우리 도구를 더한 조립 보기

01절에서는 인자 없이 만든 Deep Agent의 도구 아홉을 보았습니다.
이번에는 인자 `tools=`에 우리 도구를 넘겨 만들고, 기준과 견줍니다.
먼저 기준이 될 Deep Agent를 01절처럼 만듭니다."""),
        code(BASE),
        md("""**결과 읽기** — 출력 줄 `기본 도구 수: 9`가 보입니다.
01절 3절과 같은 수이고, 이 목록 `base_tools`가 이 절의 기준입니다.

실행 전에 예상해 봅니다.
우리 도구를 넘기면 기본 도구 아홉은 그대로 남을까요, 아니면 우리 도구로 바뀔까요?"""),
        code(TOOL_AGENT),
        md("""**결과 읽기** — 출력 줄 `도구 수: 10`이 보입니다.
라벨 `도구 이름:` 뒤의 목록에 `'lookup_rule'`이 알파벳 차례 자리에 끼어 있습니다.
설치판 `graph.py` 336행 독스트링도 넘긴 도구는 더해지기만 하고, 기본 도구를 빼지 않는다고 적습니다.

다음 셀은 01절 함수 `names_only_in`으로 두 목록의 차이를 양쪽으로 봅니다."""),
        code(ADDED),
        md("""**결과 읽기** — 출력 줄 `더해진 도구: ['lookup_rule']`과 `빠진 도구: []`가 보입니다.
기본 도구 아홉은 모두 남았고, 우리 도구 하나만 더해졌습니다.

다음 셀은 두 Deep Agent의 노드 이름을 견줍니다."""),
        code(SAME_NODES),
        md("""**결과 읽기** — 출력 줄 `노드가 같은가: True`가 보입니다.
우리 도구는 새 노드를 만들지 않고, 이미 있던 도구 실행 노드 `tools`에 들어갔습니다.

그런데 그래프에 등록된 도구가 모두 모델에게 가는 것은 아닙니다.
파일 도구가 파일을 실제로 두는 자리를 정하는 부품을 백엔드(backend)라고 부릅니다.
짐을 맡길 때 사물함에 둘지 창고에 둘지 정하는 보관 방식과 같습니다.
이 절 Deep Agent는 백엔드를 따로 주지 않아, 기본 백엔드 `StateBackend`를 씁니다.
이 백엔드는 파일을 그래프 상태 안에 두고, 디스크에는 쓰지 않습니다.

설치판 `filesystem.py` 2688~2707행에서 `FilesystemMiddleware`는 모델 요청마다 백엔드를 봅니다.
백엔드가 명령을 실행하지 못하면, 모델에게 보내는 도구 목록에서 `execute`를 뺍니다.
다음 셀은 그 판단에 쓰는 설치판 함수 `supports_execution`에 기본 백엔드를 넘겨 봅니다."""),
        code(STATE_BACKEND),
        md("""**결과 읽기** — 출력 줄 `백엔드 종류: StateBackend`와 `명령을 실행할 수 있는가: False`가 보입니다.
기본 백엔드는 명령을 실행하지 못합니다.
그래서 이 Deep Agent의 모델은 `execute`를 받지 못할 것입니다.
모델이 받는 목록은 모델을 불러야 보이므로, 6절 실행에서 확인합니다.

## 4. 값 바꿔 보기: 명령을 실행하는 백엔드

바꿀 값은 함수 `supports_execution`에 넘기는 백엔드입니다.
백엔드 `LocalShellBackend`는 파일을 디스크에 두고, 이 컴퓨터에서 명령도 실행하는 백엔드입니다.
이 셀은 백엔드를 만들기만 하고, 에이전트에는 넘기지 않습니다.
실행 전에 예상해 봅니다.
출력이 `True`로 바뀔 것입니다."""),
        code(SHELL_BACKEND),
        md("""**결과 읽기** — 출력 줄 `백엔드 종류: LocalShellBackend`와 `명령을 실행할 수 있는가: True`가 보입니다.
예상대로 값이 바뀌었습니다.
이런 백엔드를 준 Deep Agent라면, 모델이 받는 목록에 `execute`가 남습니다.
이 판단 자리는 설치판 소스로 확인했고, 이 백엔드로 에이전트를 실행하지는 않았습니다.

이 백엔드는 모델이 고른 명령을 이 컴퓨터에서 막는 장치 없이 실행합니다.
그래서 이 과정에서는 에이전트에 넘기지 않고, 이 셀처럼 만들어 보기만 합니다.

## 5. 호출 한도와 기록 훅 달기

이제 실제 모델로 실행할 Deep Agent를 만듭니다.
01절에서 본 것처럼 바깥 에이전트의 호출 한도는 general-purpose 서브에이전트로 옮겨 가지 않습니다.
그래서 호출 한도를 바깥 에이전트와 서브에이전트 명세, 두 곳에 따로 줍니다.
먼저 바깥 에이전트의 호출 한도를 만듭니다."""),
        code(OUTER_LIMIT),
        md("""**결과 읽기** — 출력 줄 `바깥 호출 한도: 3`이 보입니다.
바깥 에이전트는 한 번 실행에 모델 요청을 세 번까지 보냅니다.
세 번을 채우면 다음 요청 앞에서 실행을 끝냅니다.

다음 셀은 01절 6절처럼 기본 서브에이전트와 같은 이름의 명세를 만듭니다.
이번에는 자기 호출 한도를 0이 아니라 2로 주어, 맡은 일을 마칠 수 있게 합니다."""),
        code(HELPER_SPEC),
        md("""**결과 읽기** — 출력 줄 `명세의 키: ['name', 'description', 'system_prompt', 'middleware']`가 보입니다.
키 `tools`를 적지 않아, 이 서브에이전트는 우리 도구 `lookup_rule`을 물려받습니다.
이 사실은 설치판 `graph.py` 728행으로 확인했고, 이 노트북에서는 실행하지 않았습니다.

다음 셀은 모델 요청마다 그 요청에 실린 도구 이름을 적는 훅을 만듭니다.
함수 위의 `@wrap_model_call` 줄은 아래 함수를 모델 요청을 감싸는 훅으로 등록합니다.
Ch 22 02절에서 모델이 받은 메시지를 적던 기록 훅과 같은 모양입니다.
인자 `request`의 속성 `tools`가 이번 요청에 실리는 도구 목록입니다.
인자 `handler`를 부르는 줄에서 실제 모델이 실행됩니다."""),
        code(DEF_HOOK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
기록 목록 `seen_tool_lists`는 6절 실행 셀에서 새로 만듭니다.
01절 5절에서 본 것처럼, 인자 `middleware=`에 넣은 이 훅은 짝 맞추기 미들웨어 뒤에 붙습니다.
그래서 `FilesystemMiddleware`가 도구 목록을 고친 뒤의 요청을 봅니다.

다음 셀은 우리 도구·바깥 호출 한도·기록 훅·명세를 함께 넘겨 Deep Agent를 만듭니다."""),
        code(RULE_AGENT),
        md("""**결과 읽기** — 출력 줄 `그래프에 등록된 도구 수: 10`이 보입니다.
라벨 `노드:` 뒤에는 `'ModelCallLimitMiddleware.before_model'`과 `'ModelCallLimitMiddleware.after_model'`이 더해졌습니다.
기록 훅은 감싸기형 훅만 있어서, 01절에서 본 요약 미들웨어처럼 노드로 보이지 않습니다.

## 6. 실제 모델로 한 번 실행하기

질문은 Ch 26 01절의 대출 연장 문의에, 도구 설명의 「교육센터 자료실」과 답 길이를 더한 글입니다.
시스템 메시지 글은 주지 않았고, 03절에서 다룹니다.
실행 전에 예상해 봅니다.
모델이 우리 도구를 한 번 부르고 답하면, 결과 메시지는 넷이고 모델 요청은 2번일 것입니다."""),
        code(RUN),
        md("""**결과 읽기** — 출력 줄 `결과 메시지 수: 4`가 보입니다.
넣은 질문 하나 뒤에 메시지 셋이 더해졌습니다.

메시지 수는 모델이 도구를 몇 번 고르는지에 따라 달라질 수 있습니다.
노트북 밖에서 같은 질문을 다섯 번 보냈을 때는 다섯 번 모두 넷이었습니다.

다음 셀은 결과 메시지를 Ch 19 06절 함수 `show_messages`로 한 줄씩 봅니다."""),
        code(SHOW),
        md("""**결과 읽기** — 라벨 줄 아래 둘째 줄이 `AIMessage | 도구 호출 요청: ['lookup_rule']`입니다.
모델이 첫 응답에서 우리 도구를 골랐습니다.
셋째 줄 `ToolMessage`는 도구가 내놓은 규정 글이고, 넷째 줄은 도구 요청이 없는 마지막 응답입니다.

이번 실행에서 셋째 줄의 내용은 연장 규정 두 문장이었습니다.
모델이 인자 `topic`에 주제어 「연장」을 넣었다는 뜻입니다.
모델이 고른 인자라 실행마다 달라질 수 있고, 노트북 밖 다섯 번에서는 모두 같은 주제어였습니다.

다음 셀은 마지막 응답의 글을 봅니다."""),
        code(FINAL),
        md("""**결과 읽기** — 라벨 줄 `마지막 답 글:` 아래는 모델이 도구 메시지를 바탕으로 쓴 답입니다.
답 글은 실행마다 달라질 수 있어, 이 절의 결론에 쓰지 않습니다.

이번 실행에서는 답 글이 도구 메시지의 연장 규정 두 문장과 같은 글이었습니다.
질문에서 두 문장으로 답하라고 적었고, 모델은 규정 글을 그대로 옮겨 답했습니다.

다음 셀은 넣은 메시지 뒤, 이번 실행이 더한 응답에서 도구 요청 이름을 모읍니다.
Ch 26 01절처럼 결과 목록을 넣은 메시지 수만큼 건너뛰고 자릅니다."""),
        code(ASKED),
        md("""**결과 읽기** — 출력 줄 `요청한 도구 이름: ['lookup_rule']`과 `task를 부른 횟수: 0`이 보입니다.
이번 실행에서 모델은 파일 도구도, 도구 `task`도 부르지 않았습니다.
그래서 general-purpose 서브에이전트는 이번 실행에서 한 번도 실행되지 않았습니다.

어느 도구를 몇 번 부를지는 모델이 정하는 값입니다.
노트북 밖에서 같은 질문을 다섯 번 보냈을 때도 다섯 번 모두 `lookup_rule` 하나만 불렀습니다.

다음 셀은 기록 훅이 적은 목록을 봅니다."""),
        code(SEEN),
        md("""**결과 읽기** — 출력 줄 `기록된 모델 요청 수: 2`와 `모델이 받은 도구 수: 9`가 보입니다.
라벨 `모델이 받은 도구 이름:` 뒤의 목록은 요청에 실린 차례이고, 알파벳 차례가 아닙니다.
파일 도구 일곱, `task`, 우리 도구 `lookup_rule` 차례이고, `execute`는 없습니다.

다음 셀은 그래프에 등록된 도구 가운데 모델이 받지 않은 것을 찾습니다.
요청마다 `execute`가 있었는지도 한 줄씩 봅니다."""),
        code(MISSING),
        md("""**결과 읽기** — 출력 줄 `그래프에만 있는 도구: ['execute']`가 보입니다.
아래 두 줄은 모두 `이 요청에 execute가 있는가: False`입니다.
3절에서 본 대로, 명령을 실행하지 못하는 백엔드라서 모델은 `execute`를 받지 못했습니다.
그래프에 등록된 도구는 열이지만, 모델이 고를 수 있는 도구는 아홉이었습니다.

## 7. 요청 수와 예상 비용

이 실행은 도구 `task`를 부르지 않아, 모델 요청은 모두 바깥 에이전트의 것입니다.
그러면 이번 실행이 더한 응답 수가 곧 요청 수이고, 기록 훅이 센 수와 같아야 합니다."""),
        code(USAGE),
        md("""**결과 읽기** — 출력 줄 `응답으로 센 요청 수: 2`와 `기록 훅이 센 요청 수: 2`가 보입니다.
두 방법으로 센 요청 수가 같습니다.
이번 실행은 도구를 요청한 응답 하나에, 도구 요청이 없는 마지막 응답 하나를 더한 2번입니다.

이번 실행에서는 `입력 토큰: 3792 | 출력 토큰: 50`이었습니다.
질문은 짧지만, 요청마다 도구 아홉의 이름과 설명이 함께 실려 입력 토큰이 많아집니다.
도구 설명이 요청에 실린다는 것은 Ch 19 04절에서 보았고, 도구 설명만의 토큰 수는 따로 세지 않았습니다.

다음 셀은 Ch 6 06절 함수 `estimate_cost`로 이번 실행의 예상 비용을 셉니다.
요금은 과정 요금표(2026-09-17)의 100만 토큰당 달러이고, 예상 비용은 청구 금액이 아닙니다."""),
        code(COST),
        md("""**결과 읽기** — 출력 줄 `예상 비용(달러):`에 이번 실행의 어림값이 보입니다.
토큰 수가 실행마다 달라, 이 값도 달라질 수 있습니다.
합친 사용량에는 캐시 입력 칸이 없어, 입력 토큰을 모두 입력 요금으로 셉니다.

이번 실행에서는 `예상 비용(달러): 0.003069`였습니다.
캐시 입력을 빼지 않은 어림이라, 서비스가 입력 일부를 캐시 입력으로 셌다면 청구 금액은 이보다 작습니다.

## 정리

1. 함수 `create_deep_agent`에 넘긴 우리 도구는 기본 도구 아홉에 더해지기만 해서, 그래프의 도구는 열이 되었습니다.
2. 기본 백엔드 `StateBackend`는 명령을 실행하지 못해, 모델이 받은 목록에서는 `execute`가 빠진 아홉이었습니다.
3. 호출 한도를 두 곳에 준 실행에서, 요청 수는 도구를 요청한 응답 수에 1을 더한 값이었습니다.

03절에서는 할 일 목록 미들웨어와 시스템 메시지 글을 더해, 모델이 긴 일을 나눠 적는 장면을 봅니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


L_CH02_09 = "../../part1/ch02-python/09-데코레이터와-컨텍스트-매니저.html"
L_CH06_06 = "../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html"
L_CH19_01 = "../../part5/ch19-model-tools/01-tool과-Ch4-함수-재사용.html"
L_CH19_05 = "../../part5/ch19-model-tools/05-bind_tools와-병렬-호출.html"
L_CH21_01 = "../ch21-create-agent/01-create-agent와-ReAct-루프.html"
L_CH22_02 = "../ch22-middleware/02-PII-마스킹-이식.html"
L_CH22_04 = "../ch22-middleware/04-호출-한도와-재시도-폴백.html"
L_CH26_01 = "../ch26-delegation/01-Subagent-도구-위임.html"
L_01 = "01-하네스와-일곱-기능.html"
L_03 = "03-플래닝과-시스템-프롬프트.html"

RESULT_ROWS = [
    ("그래프에 등록된 도구(우리 도구를 넘김)", "<code>도구 수: 10</code> · <code>빠진 도구: []</code>", "구조 값"),
    ("기본 백엔드가 명령을 실행하는가", "<code>명령을 실행할 수 있는가: False</code>", "구조 값"),
    ("모델이 받은 도구", "<code>모델이 받은 도구 수: 9</code> · <code>그래프에만 있는 도구: ['execute']</code>", "구조 값(요청마다 같음)"),
    ("요청한 도구", "<code>요청한 도구 이름: ['lookup_rule']</code> · <code>task를 부른 횟수: 0</code>", "모델 판단 값"),
    ("모델 요청 수", "<code>응답으로 센 요청 수: 2</code> · <code>기록 훅이 센 요청 수: 2</code>", "모델 판단 값에 따라 셈으로 정해짐"),
    ("토큰과 예상 비용", "<code>입력 토큰: 3792 | 출력 토큰: 50</code> · <code>예상 비용(달러): 0.003069</code>(교재 출력)", "흔들리는 값"),
]

LOOK_B5 = "노트북 3절에서 <code>도구 수: 10</code>과 <code>빠진 도구: []</code>를 확인합니다. 3·4절 백엔드 셀에서 <code>명령을 실행할 수 있는가:</code> 뒤의 <code>False</code>와 <code>True</code>를 견줍니다. 6절에서 <code>모델이 받은 도구 수: 9</code>와 <code>그래프에만 있는 도구: ['execute']</code>를 봅니다. 7절에서 두 방법으로 센 요청 수가 같은지 확인합니다."
LOOK_B6 = "노트북 6절 마지막 셀에서 <code>이 요청에 execute가 있는가:</code> 줄이 모두 <code>False</code>인지 봅니다. 7절 <code>응답으로 센 요청 수:</code>와 <code>기록 훅이 센 요청 수:</code>가 같은 수인지 확인합니다. 교재 출력에서는 <code>입력 토큰: 3792 | 출력 토큰: 50</code>이었고, 다시 실행하면 달라질 수 있습니다."


def src_html() -> str:
    results = table_html(["확인한 것", "교재 출력", "값의 성격"], RESULT_ROWS)
    return """<!--meta: 강의 1h | 실습 2h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 1 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>함수 <code>create_deep_agent</code>에 우리 도구를 넘긴 조립을 출력으로 보고, 도구가 더해지기만 한다고 설명할 수 있습니다.</li>
<li>백엔드가 명령을 실행하지 못하면, 모델이 받는 도구 목록에서 <code>execute</code>가 빠진다는 것을 말할 수 있습니다.</li>
<li>호출 한도를 두 곳에 준 Deep Agent를 실제 모델로 실행하고, 고른 도구와 모델 요청 수를 셀 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_01 + """\">01절</a>에서는 모델을 부르지 않고, Deep Agent에 미리 붙은 노드와 도구만 보았습니다. 실제로 일을 맡기려면 우리 업무 도구를 더하고, 모델이 그 도구를 고르는지 봐야 합니다. 그런데 Deep Agent에는 우리가 넘기지 않은 도구가 이미 아홉 있습니다. 모델이 그 가운데 무엇을 받는지는 그래프 출력만으로는 보이지 않습니다.</p><p>이 절은 앞 절반에서 모델 없이 조립과 백엔드를 보고, 뒤 절반에서 실제 모델로 한 번 실행합니다. 실행에서는 모델 요청마다 실린 도구 이름을 기록해, 그래프의 목록과 견줍니다. 절 제목의 create deep agent는 함수 <code>create_deep_agent</code>의 이름을 띄어 쓴 것입니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH19_01 + """\">Ch 19 01절</a>에서는 함수 위에 <code>@tool</code> 줄을 붙여 도구를 만들었습니다. 매개변수 힌트 <code>: str</code>은 모델이 채울 인자가 되고, 독스트링은 모델이 읽는 도구 설명이 되었습니다. <code>@</code> 줄의 뜻은 <a href=\"""" + L_CH02_09 + """\">Ch 2 09절</a>에 있습니다. <a href=\"""" + L_CH19_05 + """\">05절</a>에서는 도구의 <code>invoke</code>로 모델 없이 도구만 실행했습니다.</p><p><a href=\"""" + L_CH21_01 + """\">Ch 21 01절</a>에서는 교육센터 자료실 규정 셋을 도구 <code>lookup_policy</code>로 찾는 에이전트를 만들었습니다. <a href=\"""" + L_CH26_01 + """\">Ch 26 01절</a>은 같은 규정에 연장 두 문장을 더했습니다. 그 절은 이번 실행이 더한 메시지만 잘라 모델 요청 수를 셌습니다.</p><p><a href=\"""" + L_CH22_02 + """\">Ch 22 02절</a>에서는 모델 요청을 감싸는 훅으로 모델이 받은 메시지를 기록했습니다. <a href=\"""" + L_CH22_04 + """\">04절</a>의 호출 한도는 한도를 붙인 에이전트의 요청만 셌습니다. <a href=\"""" + L_CH06_06 + """\">Ch 6 06절</a>에서는 사용량과 요금표로 예상 비용을 어림했고, 청구 금액과 다르다고 적었습니다.</p><p><a href=\"""" + L_01 + """\">01절</a>에서는 기본 도구 아홉이 미들웨어에서 온다는 것을 보았습니다. general-purpose 서브에이전트가 늘 붙고, 바깥 호출 한도가 그리로 옮겨 가지 않는다는 것도 보았습니다. 모델에게 보내는 도구 목록에서 <code>execute</code>가 빠질 수 있다는 점은 이 절로 넘겼습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>""" + "01절의 유리 온실 안에, 긴 자루 연장을 한 줄로 세워 두는 나무 걸이가 있다고 합시다. 초록 자루의 갈퀴·괭이·삽·쇠스랑이 이미 서 있습니다. 우리는 줄 오른쪽 끝에 노란 자루의 새 삽 하나를 더 세우고, 원래 있던 연장은 하나도 치우지 않습니다. 줄 가운데에는 전기로 도는 예초기도 서 있지만, 이 온실에는 콘센트가 없어 쓰지 못합니다." + """</p><p>""" + "걸이에 선 연장 전체가 그래프에 등록된 도구이고, 노란 삽이 우리가 넘긴 도구 <code>lookup_rule</code>입니다. 콘센트가 없어 못 쓰는 예초기가 명령 실행 도구 <code>execute</code>입니다. 콘센트가 없는 온실은, 뒤에서 풀 기본 백엔드가 명령을 실행하지 못하는 것에 해당합니다. 연장 수는 도구 수와 짝짓지 않습니다." + """</p><p>비유와 다른 점이 있습니다. 온실에서는 쓰지 못하는 연장도 걸이에 그대로 보입니다. 모델에게 가는 목록에서는 <code>execute</code>가 아예 빠져, 모델은 그 도구의 이름도 받지 못합니다.</p>
""" + illustration_block() + """<h3>백엔드와 모델이 받는 도구 목록</h3><p>파일 도구가 파일을 실제로 두는 자리를 정하는 부품을 백엔드(backend)라고 부릅니다. 짐을 맡길 때 사물함에 둘지 창고에 둘지 정하는 보관 방식과 같습니다. 이 절 Deep Agent는 백엔드를 따로 주지 않아, 기본 백엔드 <code>StateBackend</code>를 씁니다. 이 백엔드는 파일을 그래프 상태 안에 두고 디스크에는 쓰지 않으며, 명령은 실행하지 못합니다.</p><p>도구 목록은 두 곳에 있습니다. 하나는 그래프의 도구 실행 노드에 등록된 목록이고, 01절 함수 <code>tool_names</code>가 이 목록을 읽습니다. 다른 하나는 모델 요청마다 실리는 목록이고, 기록 훅의 인자 <code>request.tools</code>로 봅니다. 설치판 <code>filesystem.py</code> 2688~2707행에서 <code>FilesystemMiddleware</code>는 요청마다 백엔드를 보고, 명령을 실행하지 못하면 둘째 목록에서 <code>execute</code>를 뺍니다.</p><p>새 말을 이 절 코드에서 보면 이렇습니다. 기본 백엔드는 <code>백엔드 종류: StateBackend</code>이고, <code>명령을 실행할 수 있는가: False</code>로 출력됩니다. 그 결과 모델이 받은 목록은 <code>모델이 받은 도구 수: 9</code>였습니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>넘긴 도구는 더해지기만 합니다</h3><p>설치판 <code>graph.py</code> 336행 독스트링은 인자 <code>tools=</code>로 넘긴 도구가 기본 도구에 더해지기만 한다고 적습니다. 기본 도구를 빼려면 모델마다 따로 등록하는 설정 묶음(하네스 프로필)이 필요합니다. 한 번 등록하면 같은 모델의 모든 에이전트에 걸리는 설정이라, 이 과정에서는 쓰지 않습니다. 그래서 우리 도구를 넘긴 Deep Agent도 파일 도구와 <code>task</code>를 그대로 가집니다.</p><h3>실제 모델을 부를 때의 안전 설정</h3><p>01절에서 정한 대로, 모델을 부르는 Deep Agent에는 호출 한도를 두 곳에 줍니다. 바깥 에이전트의 인자 <code>middleware=</code>에 호출 한도 3을 넣습니다. 이름이 <code>general-purpose</code>인 명세에도 자기 호출 한도 2를 넣어, 기본 서브에이전트 자리를 바꿉니다. 이렇게 두면 한 번 실행의 모델 요청은 3에, 도구 <code>task</code>를 부른 횟수 × 2를 더한 값을 넘지 않습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 규정 글 넷과 도구 <code>lookup_rule</code>을 만들고, 모델 없이 도구만 두 번 실행합니다. 3절은 우리 도구를 넘긴 Deep Agent와 기준 Deep Agent의 도구·노드를 견주고, 기본 백엔드를 봅니다. 4절은 값 바꿔 보기로, 명령을 실행하는 백엔드를 만들기만 해 같은 함수에 넘깁니다. 5절은 호출 한도 둘과 기록 훅을 달고, 6·7절은 실제 모델로 한 번 실행해 도구와 요청 수를 봅니다.</p><p>모델 요청은 6절 실행 셀에서만 나가고, 우리 도구를 한 번 부르면 2번입니다. 요금표로 어림한 예상 비용은 0.004달러 아래이고, 청구 금액이 아닙니다. 읽거나 쓰는 파일은 없고, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>우리 도구 하나를 넘기자 그래프의 도구는 열이 되었고, 기본 도구는 하나도 빠지지 않았습니다. 노드도 기준 Deep Agent와 같아, 우리 도구는 이미 있던 도구 실행 노드에 들어갔습니다. 기본 백엔드는 명령을 실행하지 못했고, 명령을 실행하는 백엔드로 바꾸자 같은 함수가 <code>True</code>를 냈습니다.</p><p>아래 표는 이 절이 확인한 값과 그 성격입니다. 구조 값은 코드가 정하는 값이고, 모델 판단 값은 모델이 고른 값입니다. 흔들리는 값은 실행마다 달라질 수 있어 결론에 쓰지 않습니다.</p>
""" + results + """
<p>실제 실행에서 모델이 받은 도구는 아홉이었고, 그래프에만 있는 도구는 <code>execute</code> 하나였습니다. 두 요청 모두 같은 목록이었습니다. 모델이 고를 수 있는 도구는 그래프의 목록이 아니라, 미들웨어가 요청마다 고친 목록입니다.</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>흔들림 확인 다섯 번과 두 커널에서 모두, 모델은 첫 응답에서 <code>lookup_rule</code>을 한 번 불렀습니다. 그래서 요청 수는 도구를 요청한 응답 하나에 마지막 응답 하나를 더한 2였습니다. 두 방법 모두 바깥 에이전트의 요청만 셉니다. 이 수가 전체 요청 수와 같은 것은 도구 <code>task</code>를 부르지 않았을 때뿐입니다. 도구 <code>task</code>를 부르면 서브에이전트 요청은 결과 목록에도 기록 훅에도 남지 않아, 따로 세야 합니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>설치판 <code>graph.py</code> 297~299행 독스트링은 명령을 실행하지 못하는 백엔드에서 <code>execute</code>가 오류 글을 낸다고 적습니다. 같은 판의 <code>FilesystemMiddleware</code>는 그 도구를 모델 요청 목록에서 아예 뺍니다. 이 절 출력은 뺀 쪽과 맞았습니다.</li><li>백엔드 <code>LocalShellBackend</code>는 모델이 고른 명령을 이 컴퓨터에서 막는 장치 없이 실행합니다. 공식 백엔드 문서도 통제된 개발 환경에서만 쓰라고 적습니다. 이 절은 만들어 보기만 했고, 에이전트에 넘겨 실행하지 않았습니다.</li><li>설치판 <code>graph.py</code> 728행에서, 명세에 키 <code>tools</code>를 적지 않은 general-purpose 서브에이전트는 우리 도구를 물려받습니다. 노트북 밖에서 모델 없이 확인하니 그 서브에이전트의 요청에는 파일 도구 일곱과 <code>lookup_rule</code>이 실렸습니다. 이 노트북에서는 실행하지 않았습니다.</li><li>기록 훅은 바깥 에이전트의 인자 <code>middleware=</code>에만 넣어, general-purpose 서브에이전트의 요청은 적지 않습니다. 모델이 <code>task</code>를 부르는 절에서는 명세의 미들웨어에도 기록 훅을 넣어 따로 셉니다.</li><li>호출 한도에 닿아 끝난 실행은 마지막 응답이 한도 글이고 사용량이 <code>None</code>입니다. 그러면 함수 <code>sum_usage</code>가 멈출 수 있습니다(Ch 26 01절). 이번 실행은 한도에 닿지 않았습니다.</li><li>""" + "노트북을 쓰기 전에 같은 질문을 노트북 밖에서 다섯 번 보냈습니다. 다섯 번 모두 첫 응답에서 <code>lookup_rule</code>을 한 번 부르고, 모델 요청 2번으로 끝났습니다. 같은 요청도 실행한 때에 따라 고르는 도구가 달라질 수 있어, 이 절은 그 값을 셈과 함께만 씁니다. 입력·출력 토큰도 다섯 번 같았지만, 서비스 쪽 값이라 결론에 쓰지 않습니다." + """</li><li>질문 글은 Ch 26 01절 문의에 도구 설명의 「교육센터 자료실」과 답 길이를 더해, 실행 전에 정했습니다. 흐름을 보여 주려고 정한 예이고, 결과를 보고 바꾸지 않았습니다. 시스템 메시지 글은 주지 않았고, <a href=\"""" + L_03 + """\">03절</a>에서 다룹니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>함수 <code>create_deep_agent</code>에 넘긴 우리 도구는 기본 도구 아홉에 더해지기만 해서, 그래프의 도구는 열이 되었습니다.</li><li>기본 백엔드 <code>StateBackend</code>는 명령을 실행하지 못해, 모델이 받은 목록에서는 <code>execute</code>가 빠진 아홉이었습니다.</li><li>호출 한도를 두 곳에 준 실행에서, 요청 수는 도구를 요청한 응답 수에 1을 더한 값이었습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_03 + """\">03절</a>에서는 할 일 목록 미들웨어와 시스템 메시지 글을 더합니다. 모델이 긴 일을 나눠 적는 장면을 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 우리 도구 하나를 인자 <code>tools=</code>로 넘긴 Deep Agent의 그래프에는 도구가 몇 개 있고, 빠진 기본 도구는 무엇인가요?</p><p class="quiz-a">열 개이고, 빠진 기본 도구는 없습니다. 넘긴 도구는 기본 도구 아홉에 더해지기만 합니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">2. 그래프에 등록된 <code>execute</code>가 모델이 받은 도구 목록에 없던 까닭은 무엇인가요?</p><p class="quiz-a">기본 백엔드 <code>StateBackend</code>가 명령을 실행하지 못해서, <code>FilesystemMiddleware</code>가 요청마다 목록에서 뺐기 때문입니다. 틀렸다면 노트북 3절 끝과 6절을 다시 읽습니다.</p><p class="quiz-q">3. 이 절 실행에서 응답으로 센 요청 수와 기록 훅이 센 요청 수가 같았습니다. 모델이 도구 <code>task</code>를 불렀다면 어떻게 될까요?</p><p class="quiz-a">서브에이전트의 요청은 결과 목록에도, 바깥에만 넣은 기록 훅에도 남지 않습니다. 두 셈 모두 바깥 요청만 세므로, 서브에이전트 요청은 따로 세야 합니다. 틀렸다면 노트북 7절과 본문 「주의할 점」을 다시 읽습니다.</p><p class="quiz-q">4. 동료가 「바깥 호출 한도를 3으로 주었으니, 이 에이전트의 모델 요청은 세 번을 넘지 않는다」고 말합니다. 맞나요?</p><p class="quiz-a">맞지 않습니다. 바깥 호출 한도는 바깥 에이전트의 요청만 셉니다. 도구 <code>task</code>를 부를 때마다 서브에이전트 요청이 명세의 한도 2까지 더 나갈 수 있습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/deepagents/customization">Deep Agents customization</a></div>확인 2026-09-28 · 파일 관리와 서브에이전트 기본 도구에 더해 우리 도구를 넘길 수 있다고 적습니다. 백엔드를 주지 않으면 <code>StateBackend</code>를 쓴다는 설명도 있습니다. 판 번호와 날짜 표시는 없습니다.</li><li><div><a href="https://docs.langchain.com/oss/python/deepagents/backends">Deep Agents backends</a></div>확인 2026-09-28 · 파일 도구가 바꿔 끼울 수 있는 백엔드를 거쳐 일한다고 적습니다. 도구 <code>execute</code>는 명령을 따로 가둬 실행하는 환경(샌드박스)과 <code>LocalShellBackend</code>에만 있다고 적습니다. 이 백엔드는 막는 장치 없이 명령을 실행한다고 경고합니다.</li><li><div><a href="https://github.com/langchain-ai/deepagents/releases/tag/deepagents%3D%3D0.7.0">deepagents 0.7.0 release</a></div>확인 2026-09-28 · 이 과정이 쓰는 판입니다. 도구 <code>delete</code>가 더해졌고, <code>write_file</code>이 있던 파일을 통째로 바꾼다고 적습니다.</li><li>설치판 deepagents 0.7.0 소스 <code>graph.py</code> 336행은 넘긴 도구가 더해지기만 한다는 독스트링입니다. 627행은 기본 백엔드, 728행은 서브에이전트가 도구를 물려받는 자리입니다.</li><li>설치판 deepagents 0.7.0 소스 <code>middleware/filesystem.py</code> 1156~1175행은 함수 <code>supports_execution</code>입니다. 2688~2707행은 모델 요청 목록에서 쓸 수 없는 도구를 빼는 자리입니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    check_tools()
    check_same_as_probe()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "harness_tools.py").write_text(TOOLS_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        # 도구 파일은 없거나 이 판과 같을 때만 쓴다. 뒤 절이 함수를 더한 판이면 덮어쓰지 않는다(Ch 24 마감 A-10·Ch 25·26 교훈).
        current = ""
        if TOOLS_PATH.is_file():
            current = TOOLS_PATH.read_text(encoding="utf-8")
        # 뒤 절 판은 머리 설명 뒤에 가져오기 줄을 더할 수 있으므로, 그 줄을 빼고 02절 판으로 시작하는지 봅니다
        plain = strip_later_imports(current)
        assert current == "" or plain.startswith(TOOLS), "도구 파일이 02절 판으로 시작하지 않습니다"
        if current == "" or current == TOOLS:
            TOOLS_PATH.write_text(TOOLS, encoding="utf-8")
            print("wrote", TOOLS_PATH)
        else:
            print("skip", TOOLS_PATH, "(뒤 절이 함수를 더한 판 — 덮어쓰지 않음)")
        path = write_notebook(LAB, "02", SLUG, "experiment", cells())
        print("wrote", path)
