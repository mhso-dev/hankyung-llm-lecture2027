"""Ch 29 03절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 -B author_03.py              → 도구 파일(가드) + 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_03.py --src-only   → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_03.py --tools-copy DIR → 디스크의 도구 파일을 DIR에 복사한다(새 커널 사본 B 실행용)
  python3 -B author_03.py --try DIR    → 노트북과 이 판 도구 파일을 DIR에만 쓴다(실습 폴더를 건드리지 않는 시험 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**, 슬러그 그대로(「LLM judge」는 제목에만).

## 결정 1 — 앞 절반 모델 없음 + 뒤 절반 실제 모델 (챕터 리드 결정 1)

1절 준비에서 키·과정 표준 모델 객체를 만든다(요청 0). 2·3절(앞 절반)은 요청 0: 01 답만 틀린 궤적을 네 모드로 견주고(모두 True —
모드는 답 글을 보지 않음), 설치판 _format_inputs로 평가 모델이 받는 궤적 글(태그 글)을 출력, 판정 기준 네 줄·요청 글 글자 수,
create_trajectory_llm_as_judge(judge=model, prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE)를 만들기만 한다.
4~6절(뒤 절반)은 도구 둘(평범한 @tool — search_documents는 어떤 검색어에도 tool_results 글, check_source는 LIB-001만 있음)을 붙인
create_agent(model 객체 · 호출 한도 4 · 실행 한도 20)를 한 번 실행 → 결과 messages(시스템 메시지 없음 — assert) → 요청 수 셈 →
02 도구별 덮어쓰기(search_documents ignore) 네 모드 + 평가 모델 판정 → 값 바꿔 보기(마지막 답 글만 01 틀린 답으로) 두 판정.
요청: 에이전트 3 + 평가 모델 2 = 5(교재 출력). 흔들림: qa/upgrade/03-probe.md(§0 02:11:04Z, 첫 요청 02:11:11Z, 5/5 같음 — 평가 모델 점수 True·False 모두 5/5).

## 결정 2 — 흔들리는 값의 자리 (규격 §2-7 9·10번 끝)

결론·그림·정리·복습에는 결정적 값(앞 절반 전부·모드 판정·요청 수 셈)과 5/5·두 커널 같은 모델 판단 값(도구 차례·요청 수 3·네 모드·두 점수)만
「노트북 밖 다섯 번과 새 커널 두 번에서 모두」 한정어와 함께. 검색어·답 글·판정 까닭·토큰·비용은 결과 읽기 둘째 단락·b6 표·b7에만.
모델 판단 값·점수에 assert 없음(assert는 결과 목록에 시스템 메시지가 없음 — 라이브러리 동작 하나).

## 결정 3 — 도구 파일 eval_tools.py 03절 판 (챕터 공통 「도구 파일」·handoff §02 → §03 8번)

02판 뒤에 02절 셀 four_modes(02 노트북 셀 글 그대로, 주석 `# Ch 29 02절에서 배웠습니다 — …`)와
Ch 21 runner_tools.py의 sum_usage·estimate_cost(설명 주석·본문 글자 그대로 — Ch 26·27·28 도구 파일 판과도 대조)를 더한다. 가져오기 줄은 더하지 않는다.
대조 사슬: author_02.check_tools()(안에서 author_01까지) → strip_later_imports(03판).startswith(strip_later_imports(02판)) → 셀 글 해시·02 노트북 디스크 셀·AST →
runner 원본 해시·블록 대조. 쓰기 가드: 없거나 01판·02판·이 판일 때만 쓰고 더 긴 판은 skip. 01·02 생성기가 이 판을 skip하는지 판정만 흉내 낸다.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`.items`·`+=`·기본값 매개변수·반환 힌트·대입 풀기·별표 풀기·`while`·`try`·
세미콜론·`isinstance`·클래스·`async`. 데코레이터는 `@tool` 둘, 힌트는 `@tool` 매개변수 `: str`만(Ch 19 01 선례). 호출 깊이 2 이하.
새로 쓴 이름: 글 메서드 `format`·`startswith`(한 문장씩), 설치판 함수 `_format_inputs`(밑줄 이름 — 평가 모델이 받는 글을 볼 때만).
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(HERE))
import author_01  # noqa: E402  01절 도구 파일 01판·본문 도우미
import author_02  # noqa: E402  02절 셀 글(DEF_FOUR)·도구 파일 02판
from nbkit import KEY, RUN_DATE, code, install_source, md, model_source, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch29-agent-evaluation/notebooks"
FIGS = ROOT / "textbook/part6/ch29-agent-evaluation/figures"
SLUG = "03-LLM-judge로-궤적-평가"
TITLE_TEXT = "LLM judge로 궤적 평가"
SRC = ROOT / "textbook/part6/ch29-agent-evaluation/_src" / (SLUG + ".html")
TOOLS_PATH = LAB / "eval_tools.py"
NB02 = LAB / (author_02.SLUG + ".ipynb")
RUNNER = author_01.RUNNER
RUNNER_SHA = author_01.RUNNER_SHA
DELEGATION = ROOT / "labs/part6/ch26-delegation/notebooks/delegation_tools.py"
PROBE = HERE / "probe/probe03.py"
RUNS_SENTENCE = os.environ.get("AUTHOR03_RUNS_SENTENCE", "새 커널로 두 번 실행해 견주자, 코드 셀 스물여덟 가운데 스물여섯의 출력이 같았습니다. 다른 두 셀은 평가 모델의 판정 까닭 글만 달랐고, 칸 <code>score</code>는 두 번 모두 같았습니다.")
html_text = author_01.html_text
table_html = author_01.table_html


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- 도구 파일 eval_tools.py (03절 판)
NOTE_02 = "Ch 29 02절에서 배웠습니다 — 02절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다"
DEF_FOUR = author_02.DEF_FOUR
DEF_FOUR_SHA = "93067a7bc3da25530c406dae188aba54674cfa3f27ac63b5e35219f058d775a0"
RUNNER_NOTES = [
    ("sum_usage", "Ch 19 05절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다"),
    ("estimate_cost", "Ch 6 06절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다"),
]
TOOL_ORDER = author_02.TOOL_ORDER + ["four_modes", "sum_usage", "estimate_cost"]


def tools_text() -> str:
    runner = RUNNER.read_text(encoding="utf-8")
    assert sha(runner) == RUNNER_SHA, "Ch 21 runner_tools.py가 마감 판과 다릅니다"
    text = author_02.TOOLS + "\n\n# " + NOTE_02 + "\n" + DEF_FOUR + "\n"
    for name, note in RUNNER_NOTES:
        text = text + "\n\n# " + note + "\n" + author_01.file_block(runner, name) + "\n"
    return text


TOOLS = tools_text()


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


def check_tools() -> None:
    """03절 판이 02절 판(대조 사슬)으로 시작하고, 더한 함수가 02 노트북 셀·Ch 21 원본과 글자·AST 모두 같은지 봅니다."""
    author_02.check_tools()
    assert author_01.strip_later_imports(TOOLS).startswith(author_01.strip_later_imports(author_02.TOOLS)), "03절 판이 02절 판으로 시작하지 않습니다"
    assert TOOLS.startswith(author_02.TOOLS)
    tree = ast.parse(TOOLS)
    names = []
    imports = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
    assert names == TOOL_ORDER, names
    assert imports == author_02.IMPORT_LINES, imports
    # 02절 셀 four_modes: 고정 해시 · 02 노트북 디스크 셀 · AST
    assert sha(DEF_FOUR) == DEF_FOUR_SHA, "four_modes 셀 글이 고정 해시와 다릅니다"
    # 전체 마감(2026-09-30)에서 도구 파일 머리 설명 줄만 고쳐 02판 4a3d8143… → 10f26b96…(함수 본문 같음)
    assert sha(author_02.TOOLS) == "10f26b965b0efa2e827794cb88b063abb2ed4955377fef669267ffdc1af869d6", "02판이 기록 해시와 다릅니다"
    assert DEF_FOUR in notebook_code_sources(NB02), "four_modes가 02절 노트북 디스크 셀과 다릅니다"
    assert ("# " + NOTE_02 + "\n" + DEF_FOUR + "\n") in TOOLS
    mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "four_modes"]
    theirs = [ast.dump(n) for n in ast.parse(DEF_FOUR).body if isinstance(n, ast.FunctionDef)]
    assert mine == theirs and len(mine) == 1
    # Ch 21 원본 두 함수: 원본 해시 · 블록 글 · Ch 26·27·28 판과 같음 · AST
    runner = RUNNER.read_text(encoding="utf-8")
    runner_tree = ast.parse(runner)
    harness = author_01.HARNESS.read_text(encoding="utf-8")
    connect = author_01.CONNECT.read_text(encoding="utf-8")
    delegation = DELEGATION.read_text(encoding="utf-8")
    for name, note in RUNNER_NOTES:
        block = author_01.file_block(runner, name)
        assert ("# " + note + "\n" + block + "\n") in TOOLS
        assert author_01.file_block(harness, name) == block, name + "가 Ch 27 판과 다릅니다"
        assert author_01.file_block(connect, name) == block, name + "가 Ch 28 판과 다릅니다"
        assert author_01.file_block(delegation, name) == block, name + "가 Ch 26 판과 다릅니다"
        mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        theirs = [ast.dump(n) for n in runner_tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        assert mine == theirs and len(mine) == 1, name
    # 앞 절 생성기의 쓰기 가드가 이 판을 덮어쓰지 않는지(판정만 흉내 — 실행하지 않음)
    assert author_02.later_version(TOOLS), "02 생성기가 이 판을 skip하지 않습니다"
    plain = author_01.strip_later_imports(TOOLS)
    assert plain.startswith(author_01.TOOLS) and TOOLS != author_01.TOOLS, "01 생성기가 이 판을 skip하지 않습니다"


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
    elif current == "" or current == author_01.TOOLS or current == author_02.TOOLS:
        path.write_text(TOOLS, encoding="utf-8")
        print("wrote", path)
    elif later_version(current):
        print("skip", path, "(뒤 절이 함수를 더한 판 — 덮어쓰지 않음)")
    else:
        raise AssertionError("도구 파일이 01·02·03절 판이 아닙니다")


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["agentevals==0.0.9", "langchain==1.4.0", "langchain-openai==1.6.0", "python-dotenv==1.2.3"])

IMPORT_NAMES = "called_tool_names, estimate_cost, four_modes, make_trajectory, show_messages, sum_usage, tool_call_names, trajectory_pass"
IMPORTS = r'''# 궤적을 맞춰 보는 평가 함수·평가 모델로 판정하는 평가 함수를 만드는 함수와 판정 머리글을 가져옵니다
from agentevals.trajectory.llm import TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE, _format_inputs, create_trajectory_llm_as_judge
from agentevals.trajectory.match import create_trajectory_match_evaluator
# 에이전트·호출 한도·모델·메시지 클래스·도구를 등록하는 줄을 가져옵니다(Ch 6·13·19·21·22)
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage
from langchain.tools import tool
# 앞에서 배운 함수는 도구 파일에서 가져옵니다
from eval_tools import ''' + IMPORT_NAMES + '''

print("도구 파일에서 가져온 함수:", "''' + IMPORT_NAMES + '''")'''

MODEL = model_source("openai:gpt-5.4-mini")

DATA = r'''# 질문과 기준 답, 도구마다 돌아올 결과 글을 정합니다(01절과 같은 글 — 4절의 도구 함수도 이 글을 내놓음)
question = "일반 도서는 며칠 동안 빌릴 수 있나요?"
reference_answer = "일반 도서는 14일 동안 빌릴 수 있습니다."
tool_results = {
    "search_documents": "[LIB-001] 일반 도서는 14일 동안 대출할 수 있습니다. 예약자가 없으면 한 번 연장할 수 있습니다.",
    "check_source": "LIB-001 문서가 있습니다. 제목: 도서 대출 기간",
}
print("질문:", question)
print("기준 답:", reference_answer)
print("결과 글을 정한 도구:", list(tool_results))'''

REFERENCE = r'''# 01절과 같은 도구 요청 둘로 기준 궤적을 만들고, 도구 차례와 메시지 수를 봅니다
search_args = {"query": "도서 대출 기간"}
source_args = {"doc_id": "LIB-001"}
reference_calls = [
    {"name": "search_documents", "args": search_args, "id": "call_1", "type": "tool_call"},
    {"name": "check_source", "args": source_args, "id": "call_2", "type": "tool_call"},
]
reference = make_trajectory(question, reference_calls, tool_results, reference_answer)
print("기준 궤적의 도구 차례:", called_tool_names(reference))
print("메시지 수:", len(reference))'''

WRONG = r'''# 01절처럼 도구 요청은 기준과 같고 답 글만 틀린 궤적을 만듭니다
wrong_text = "일반 도서는 7일 동안 빌릴 수 있습니다."
wrong_answer = make_trajectory(question, reference_calls, tool_results, wrong_text)
print("도구 차례:", called_tool_names(wrong_answer))
print("최종 답:", wrong_answer[-1].content)'''

MAKE_MODES = r'''# 02절처럼 모드 넷마다 궤적을 맞춰 보는 평가 함수를 하나씩 만들어, 모드 이름을 키로 모읍니다
modes = ["strict", "unordered", "subset", "superset"]
evaluators = {}
for mode in modes:
    evaluators[mode] = create_trajectory_match_evaluator(trajectory_match_mode=mode)
print("평가 함수를 만든 모드:", list(evaluators))'''

WRONG_MODES = r'''# 답만 틀린 궤적을 02절 함수 four_modes로 네 모드 모두에 견줍니다
wrong_row = four_modes(wrong_answer, reference, evaluators)
print("답만 틀림:", wrong_row)'''

FORMAT = r'''# 평가 모델이 받을 궤적 글을 만듭니다(설치판 함수 _format_inputs — 실제 궤적 글과 기준 궤적 글을 튜플로 내놓음)
formatted = _format_inputs(wrong_answer, reference)
judge_text = formatted[0]
print("실제 궤적 글:")
print(judge_text)'''

SEE = r'''# 궤적 글에 답 글·검색 결과 글·호출 ID가 들어 있는지 봅니다(모드는 셋 다 견주지 않음)
print("답 글이 들어 있는가:", wrong_text in judge_text)
print("검색 결과 글이 들어 있는가:", tool_results["search_documents"] in judge_text)
print("호출 ID가 들어 있는가:", "call_1" in judge_text)
print("기준 궤적 글에 기준 답이 들어 있는가:", reference_answer in formatted[1])'''

RUBRIC = r'''# 판정 머리글에서 판정 기준 네 줄을 보고, 두 궤적 글을 끼운 요청 글의 글자 수를 셉니다
print("판정 기준:")
for line in TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE.splitlines():
    # 글의 메서드 startswith는 글이 괄호 안의 글로 시작하면 참을 냅니다
    if line.startswith("  - "):
        print(line)
# 글의 메서드 format은 머리글 속 {outputs}·{reference_outputs} 자리에 같은 이름의 인자 값을 채웁니다
request_text = TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE.format(outputs=judge_text, reference_outputs=formatted[1])
print("요청 글의 글자 수:", len(request_text))'''

MAKE_JUDGE = r'''# 모델 객체와 판정 머리글로, 평가 모델이 궤적을 판정하는 평가 함수를 만듭니다(아직 요청은 보내지 않음)
accuracy_judge = create_trajectory_llm_as_judge(judge=model, prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE)
print("평가 함수의 종류:", type(accuracy_judge).__name__)'''

TOOL_SEARCH = r'''# 검색 도구를 만듭니다(교재용 — 어떤 검색어에도 2절 결과 글 딕셔너리의 검색 결과 글을 내놓음)
@tool
def search_documents(query: str):
    """도서관 규정 문서를 검색어로 찾아, 문서 ID를 붙인 글로 내놓습니다."""
    return tool_results["search_documents"]'''

TOOL_CHECK = r'''# 출처 확인 도구를 만듭니다(문서 ID가 LIB-001일 때만 문서가 있다고 내놓음)
@tool
def check_source(doc_id: str):
    """문서 ID로 그 문서가 있는지 확인하고, 있으면 제목을 내놓습니다."""
    if doc_id == "LIB-001":
        return tool_results["check_source"]
    return doc_id + " 문서가 없습니다."'''

TOOL_TRY = r'''# 두 도구를 인자 딕셔너리로 직접 불러 봅니다(모델 요청 없음)
print("검색:", search_documents.invoke({"query": "책 대출 기간"}))
print("출처 확인:", check_source.invoke({"doc_id": "LIB-001"}))
print("없는 문서:", check_source.invoke({"doc_id": "LIB-002"}))'''

AGENT = r'''# 도구 둘·시스템 메시지 글·호출 한도 4로 평가받는 에이전트를 만듭니다(Ch 21 01절·Ch 22 04절 모양)
call_limit = ModelCallLimitMiddleware(run_limit=4, exit_behavior="end")
agent_rule = "도서관 규정 질문에는 먼저 search_documents로 문서를 찾고, 찾은 문서 ID로 check_source를 불러 문서가 있는지 확인한 뒤, 확인한 문서의 글만 근거로 한국어 한 문장으로 답하세요."
library_agent = create_agent(model, tools=[search_documents, check_source], system_prompt=agent_rule, middleware=[call_limit])
# 실행 한도는 Ch 20 03절의 설정 딕셔너리로 줍니다(그래프 단계 수 상한)
run_config = {"recursion_limit": 20}
print("에이전트의 종류:", type(library_agent).__name__)
print("실행 한도:", run_config["recursion_limit"])'''

RUN = r'''# 에이전트를 한 번 실행해 궤적을 만들고, 메시지를 차례대로 봅니다(모델 요청은 여기서 처음 나감)
first_input = {"messages": [HumanMessage(content=question)]}
result = library_agent.invoke(first_input, run_config)
agent_messages = result["messages"]
show_messages(agent_messages)'''

KINDS = r'''# 결과 메시지의 종류를 차례대로 모으고, 시스템 메시지가 들어 있는지 봅니다
kinds = []
for message in agent_messages:
    kinds.append(type(message).__name__)
print("메시지 수:", len(kinds))
print("시스템 메시지가 들어 있는가:", "SystemMessage" in kinds)
# 시스템 메시지 글은 모델에 보낼 때만 앞에 붙고 결과 목록에는 남지 않습니다(라이브러리 동작이라 assert로 확인)
assert "SystemMessage" not in kinds'''

COUNT = r'''# 도구를 요청한 응답 수를 세고, Ch 19 05절 함수 sum_usage로 센 모델 요청 수와 견줍니다
asked_responses = 0
for message in agent_messages:
    if type(message).__name__ == "AIMessage":
        if len(tool_call_names(message)) > 0:
            asked_responses = asked_responses + 1
run_usage = sum_usage(agent_messages)
print("도구를 요청한 응답 수:", asked_responses)
print("모델 요청 수:", run_usage["requests"])
print("모델 요청 수 = 도구를 요청한 응답 수 + 1:", run_usage["requests"] == asked_responses + 1)'''

ARGS = r'''# 에이전트의 도구 차례, 모델이 쓴 도구 인자, 마지막 답 글을 봅니다(인자와 답 글은 실행마다 달라질 수 있음)
print("도구 차례:", called_tool_names(agent_messages))
for message in agent_messages:
    if type(message).__name__ == "AIMessage":
        for call in message.tool_calls:
            print("도구 인자:", call["args"])
print("마지막 답 글:", agent_messages[-1].content)'''

SEARCH_FREE = r'''# 검색 도구의 인자만 보지 않는 평가 함수를 모드 넷마다 만듭니다(02절 7절의 도구별 덮어쓰기)
search_free = {}
for mode in modes:
    search_free[mode] = create_trajectory_match_evaluator(
        trajectory_match_mode=mode,
        tool_args_match_overrides={"search_documents": "ignore"},
    )
print("평가 함수를 만든 모드:", list(search_free))'''

AGENT_MODES = r'''# 에이전트 궤적을 검색어를 빼고 네 모드로 견줍니다(같은 궤적이면 늘 같은 판정)
agent_row = four_modes(agent_messages, reference, search_free)
print("에이전트 궤적:", agent_row)'''

JUDGE_AGENT = r'''# 평가 모델이 에이전트 궤적을 기준 궤적과 견줘 판정합니다(평가 모델 요청 1번)
agent_judged = accuracy_judge(outputs=agent_messages, reference_outputs=reference)
print("칸 key:", agent_judged["key"])
print("칸 score:", agent_judged["score"])
print("판정 까닭:")
print(agent_judged["comment"])'''

WRONG_RUN = r'''# 값 바꿔 보기: 에이전트 궤적을 복사해, 복사본의 마지막 답 글 하나만 01절의 틀린 답으로 바꿉니다
wrong_run = agent_messages.copy()
wrong_run[-1] = AIMessage(content=wrong_text)
print("바꾸기 전 답:", agent_messages[-1].content)
print("바꾼 뒤 답:", wrong_run[-1].content)
print("도구 차례가 같은가:", called_tool_names(wrong_run) == called_tool_names(agent_messages))'''

WRONG_EVAL = r'''# 답 글만 바꾼 궤적을 모드 strict(검색어 뺌)와 평가 모델로 판정합니다(평가 모델 요청 1번)
wrong_strict = trajectory_pass(wrong_run, reference, search_free["strict"])
wrong_judged = accuracy_judge(outputs=wrong_run, reference_outputs=reference)
print("모드 strict:", wrong_strict)
print("평가 모델 칸 score:", wrong_judged["score"])
print("판정 까닭:")
print(wrong_judged["comment"])'''

TABLE = r'''# 두 궤적의 두 판정을 한 표로 봅니다(앞 셀들이 담아 둔 값을 출력만 함 — 새 요청 없음)
print("궤적 | 모드 strict(검색어 뺌) | 평가 모델")
print("에이전트 궤적 |", agent_row["strict"], "|", agent_judged["score"])
print("답 글만 틀림 |", wrong_strict, "|", wrong_judged["score"])'''

COST = r'''# 평가 모델 요청까지 더한 요청 수를 세고, 에이전트 요청의 토큰과 예상 비용을 봅니다(요금표 2026-09-17, 100만 토큰당 달러)
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
agent_cost = estimate_cost(run_usage, input_rate, cached_input_rate, output_rate)
judge_requests = 2
print("에이전트 요청 수:", run_usage["requests"], "| 평가 모델 요청 수:", judge_requests)
print("모두 합한 모델 요청 수:", run_usage["requests"] + judge_requests)
print("에이전트 입력 토큰:", run_usage["input_tokens"], "| 출력 토큰:", run_usage["output_tokens"])
print("에이전트 예상 비용(달러):", round(agent_cost, 6))'''


def check_same_as_probe() -> None:
    """노트북 셀의 모델·자료·도구·에이전트·평가 함수 줄이 흔들림 확인 스크립트(probe03.py)와 같은 글인지 봅니다."""
    probe_lines = []
    for line in PROBE.read_text(encoding="utf-8").splitlines():
        probe_lines.append(line.strip())
    for cell in [MODEL, DATA, REFERENCE, WRONG, MAKE_JUDGE, TOOL_SEARCH, TOOL_CHECK, AGENT, RUN, SEARCH_FREE, WRONG_RUN]:
        for line in cell.splitlines():
            stripped = line.strip()
            if stripped == "" or stripped.startswith("#") or stripped.startswith("print(") or stripped.startswith("@"):
                continue
            if "agent_messages" in stripped or stripped.startswith("wrong_answer") or stripped.startswith("show_messages") or stripped.startswith("search_free = {}") or stripped == "for mode in modes:":
                continue
            assert stripped in probe_lines, "흔들림 확인 스크립트에 없는 줄: " + stripped


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/03-figures.md)
FIG1 = "03-1-모드와-평가-모델이-보는-것"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 둘은 답만 틀린 궤적과 기준 궤적입니다. 답만 틀린 궤적은 도구 요청 둘이 기준과 같고 답 글이 7일, 기준 궤적은 답 글이 14일입니다. 두 상자에서 아래 칸 둘로 화살표가 갑니다. 왼쪽 칸 평가 모델에는 회색 상자 _format_inputs, 메시지마다 태그로 감싼 궤적 글에서 노란 상자 답 글·검색 결과 글·호출 ID 모두 들어 있음 True로 화살표가 갑니다. 그 아래 점선 테두리의 회색 상자 평가 모델, 3절에서 만들기만 함으로 점선 화살표가 이어집니다. 오른쪽 칸 궤적 맞춰 보기에는 파란 상자 모드 넷, 도구 요청의 이름과 인자만 짝지음에서 노란 상자 네 모드 모두 True로 화살표가 가는 그림"
FIG1_CAP = "네 모드는 답만 틀린 궤적을 모두 참으로 봤고, 평가 모델이 받는 궤적 글에는 답 글과 도구 결과 글이 들어 있었습니다."
FIG1_READ = """위에서 아래로 읽습니다.
맨 위 초록 상자 둘은 노트북 2절에서 코드로 적은 두 궤적입니다.
오른쪽 칸은 2절에서 네 모드로 견준 결과이고, 왼쪽 칸은 같은 궤적을 평가 모델이 받는 글로 바꾼 결과입니다.
노란 상자 둘은 2절 셀 출력입니다.
앞 절반에서는 평가 모델을 부르지 않아, 점선 테두리의 회색 상자로 두었습니다."""

FIG2 = "03-2-평가-모델이-받는-요청-글"
FIG2_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 답만 틀린 궤적과 기준 궤적, 메시지 여섯씩에서 회색 상자 _format_inputs 설치판 함수로 화살표가 갑니다. 이어서 노란 상자 궤적 글 둘, user·assistant·tool 태그로 화살표가 가고, 다시 노란 상자 요청 글 하나, 글자 수 1694로 화살표가 갑니다. 회색 상자 판정 머리글, 판정 기준 네 줄과 궤적 글 자리 둘에서도 요청 글 상자로 화살표가 들어옵니다. 요청 글 상자에서 점선 테두리의 회색 상자 평가 모델, 이 칸에서는 부르지 않음으로 점선 화살표가 가고, 다시 회색 상자 결과 딕셔너리, key·score·comment·metadata, 설치판 소스로 본 모양으로 점선 화살표가 가는 그림"
FIG2_CAP = "두 궤적 글을 판정 머리글에 끼우자 글자 수 1694의 요청 글이 되었고, 평가 모델은 이 글과 답할 모양을 함께 받습니다."
FIG2_READ = """위에서 아래로 읽습니다.
초록 상자는 노트북 2절에서 코드로 적은 궤적이고, 회색 상자 셋은 라이브러리가 정한 것입니다.
노란 상자 둘은 2절과 3절 셀 출력이고, 점선 두 개와 점선 테두리 상자는 앞 절반에서 실행하지 않은 차례입니다.
결과 딕셔너리의 칸 이름은 설치판 소스로 본 것이고, 노트북은 5절에서 처음 받습니다.
요청 글과 함께 가는 답할 모양은 따로 그리지 않았고, 그 칸 reasoning이 결과의 칸 comment가 됩니다."""

FIG3 = "03-3-에이전트-궤적과-두-판정"
FIG3_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 파란 상자 평가받는 에이전트, 도구 둘, 호출 한도 4, 실행 한도 20에서 보라 상자 gpt-5.4-mini 에이전트 요청 3번으로 화살표가 갑니다. 이어서 노란 상자 에이전트 궤적, search_documents, check_source, 답, 메시지 여섯으로 화살표가 갑니다. 궤적 상자에서 아래 두 갈래로 화살표가 나뉩니다. 왼쪽은 파란 상자 모드 넷, search_documents 인자만 ignore, 기준 궤적과 견줌에서 노란 상자 네 모드 모두 True로 갑니다. 오른쪽은 보라 상자 평가 모델 gpt-5.4-mini, 판정 머리글, 요청 1번에서 노란 상자 칸 score True로 가는 그림"
FIG3_CAP = "노트북 밖 다섯 번과 두 커널에서 모두, 에이전트 궤적을 검색어를 뺀 네 모드와 평가 모델이 참으로 판정했습니다."
FIG3_READ = """위에서 아래로 읽습니다.
파란 상자는 노트북 4절에서 만든 에이전트이고, 보라 상자 둘은 이 노트북이 실제로 부른 모델입니다.
노란 상자는 4절과 5절 셀 출력입니다.
궤적 상자 아래 두 갈래는 같은 궤적을 서로 다른 방법으로 판정한 것이고, 서로의 차례가 아닙니다.
요청 수·도구 차례·두 판정은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다."""

FIG4 = "03-4-답-글-하나만-바꾸기"
FIG4_ALT = "위에서 아래로 읽는 그림입니다. 맨 위 회색 상자 도구 요청과 도구 결과 글은 에이전트 궤적 그대로에서 아래 칸 둘로 화살표가 갑니다. 왼쪽 칸 에이전트 궤적 그대로에는 노란 상자 답 글, 에이전트가 쓴 답에서 노란 상자 모드 strict True, 평가 모델 True로 화살표가 갑니다. 오른쪽 칸 마지막 답 글만 바꿈에는 파란 상자 답 글, 일반 도서는 7일 동안 빌릴 수 있습니다에서 노란 상자 모드 strict True, 평가 모델 False로 화살표가 가는 그림"
FIG4_CAP = "노트북 밖 다섯 번과 두 커널에서 모두, 마지막 답 글 하나만 바꾸자 모드 strict는 참 그대로였고 평가 모델만 거짓을 냈습니다."
FIG4_READ = """위에서 아래로 읽습니다.
맨 위 회색 상자는 두 칸에 같이 쓴 도구 요청과 도구 결과 글입니다.
오른쪽 칸의 파란 상자가 노트북 6절에서 바꾼 값 하나이고, 노란 상자는 5절과 6절 셀 출력입니다.
모드 strict는 도구 요청 가운데 검색 도구의 인자만 보지 않는 평가 함수입니다.
두 칸은 서로 다른 궤적이라 화살표 없이 나란히 두었고, 두 판정은 노트북 밖 다섯 번과 새 커널 두 번에서 같았습니다."""

ILLU = "03-5-겹쳐-보기와-울려-보기"
ILLU_ALT = "흰 바탕 왼쪽에 크림색 종이띠 둘이 조금 비켜 겹쳐 비스듬히 놓여 있고, 띠마다 둥근 구멍이 한 줄로 뚫려 있어 구멍 줄 둘이 나란히 보입니다. 오른쪽에는 상자 없이 드러난 오르골 기계 둘이 나란히 서 있습니다. 기계마다 금색 틀 안에 원통과 빗 모양 쇠붙이가 있고 옆에 작은 손잡이가 달렸으며, 구멍 뚫린 종이띠가 하나씩 위에서 아래로 기계를 지나갑니다. 사람·귀·손·글자·숫자·음표·화살표는 없는 그림"
ILLU_CAP = "왼쪽에서는 종이띠 둘을 겹쳐 놓고, 오른쪽에서는 종이띠를 하나씩 오르골 기계에 넣어 울립니다."
ILLU_READ = "왼쪽에 종이띠 둘이 조금 비켜 겹쳐 놓였고, 오른쪽에는 띠가 하나씩 지나가는 오르골 기계 둘이 있습니다. 겹쳐 놓은 두 띠는 구멍 자리를 대 보는 궤적 맞춰 보기의 모드이고, 두 기계는 두 궤적 글을 함께 읽는 평가 모델입니다. 오른쪽 두 띠가 실제 궤적과 기준 궤적이고, 기계가 띠를 울려 곡을 내듯 평가 모델은 답 글까지 담은 궤적의 뜻을 봅니다. 구멍의 수, 띠의 기울기와 길이, 짙게 칠한 구멍, 기계의 손잡이는 어떤 값과도 짝짓지 않습니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 01절의 답만 틀린 궤적으로, 모드와 평가 모델이 궤적에서 무엇을 보는지 견줍니다.
2. 도구 둘을 붙인 에이전트를 실제 모델로 한 번 실행해 궤적을 만듭니다.
3. 그 궤적을 02절의 모드와 평가 모델로 함께 판정하고, 답 글 하나만 바꿔 다시 판정합니다.

**준비물** — 프로젝트 폴더의 `.env`에 `OPENAI_API_KEY`가 있어야 합니다.
모델 요청은 4~6절에서만 나갑니다.
교재 출력에서는 에이전트 요청 3번과 평가 모델 요청 2번, 모두 5번이었습니다.
예상 비용은 요금표로 어림해 약 0.003달러이고, 청구 금액과는 다를 수 있습니다.
2~3절은 모델 요청 없이, 코드로 적은 궤적과 라이브러리 함수만 씁니다.

읽는 파일은 `.env`와 같은 폴더의 도구 파일 `eval_tools.py`이고, 쓰는 파일은 없습니다.
걸린 시간은 재지 않았습니다.

**기준 버전** — 첫 셀에서 패키지 넷을 설치합니다.
판은 agentevals 0.0.9와 langchain 1.4.0입니다.
모델을 부르는 langchain-openai는 1.6.0, 키를 읽는 python-dotenv는 1.2.3입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~5절을 읽습니다.
평가 모델이 받는 글을 보고, 실제 에이전트 궤적을 두 방법으로 판정하는 자리입니다.
6~7절은 답 글 하나만 바꿔 다시 판정하고 요청 수를 세는 실습이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch29-agent-evaluation`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

01·02절은 궤적을 코드 규칙으로 맞춰 봤습니다.
이 절은 모델이 궤적을 읽고 판정하는 평가 모델(judge)을 쓰고, 이 챕터에서 처음으로 에이전트를 실제로 실행합니다.
뜻과 구성은 본문 「핵심 개념」에서 풉니다.

첫 셀은 패키지 넷을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `agentevals: 0.0.9`, `langchain: 1.4.0`, `langchain-openai: 1.6.0`, `python-dotenv: 1.2.3`이 보입니다.
넷 모두 실습 폴더 잠금과 같은 판입니다.
패키지 langchain-openai는 모델을 부를 때, python-dotenv는 키를 읽을 때 씁니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
함수 `create_trajectory_llm_as_judge`는 평가 모델로 궤적을 판정하는 평가 함수를 만듭니다.
이름 `TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE`는 라이브러리가 적어 둔 판정 머리글입니다.
함수 `_format_inputs`처럼 밑줄로 시작하는 이름은 라이브러리가 안에서 쓰는 함수입니다.
판이 바뀌면 달라질 수 있어, 이 절은 평가 모델이 받는 글을 볼 때만 씁니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 라벨 `도구 파일에서 가져온 함수:` 뒤에 `four_modes`·`sum_usage`·`estimate_cost` 등 함수 여덟의 이름이 보입니다.
앞에서 배운 함수는 `eval_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.

노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다.

함수 `four_modes(messages, reference, evaluators)`는 02절 노트북에서 처음 적은 함수이고, 이 절부터 도구 파일에서 가져옵니다.
도구 파일에는 02절 셀의 주석과 본문을 글자 그대로 옮겼고, 인자도 02절과 같습니다.
함수 `sum_usage(messages)`와 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`는 Ch 19 05절과 Ch 6 06절에서 배웠습니다.
두 함수는 Ch 21 도구 파일 `runner_tools.py`의 함수와 설명 주석·본문이 같습니다."""),
        md("API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다."),
        setup(KEY),
        md("실습에 쓸 모델을 준비합니다.\ntemperature 값을 0으로 두어 매번 비슷한 답을 고르게 합니다."),
        code(MODEL),
        md("""**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장과 판정이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.
이 모델 객체 하나를 3절의 평가 모델과 4절의 에이전트에 함께 넘깁니다.

## 2. 모드와 평가 모델이 보는 것

01절에서 본 것처럼, 모드 `strict`는 도구 차례가 같고 답 글만 틀린 궤적을 참으로 봤습니다.
이 절의 앞 절반은 모델을 부르지 않고, 같은 궤적을 평가 모델이 어떤 글로 받는지 봅니다.
다음 셀은 01절과 같은 질문·기준 답·결과 글을 정합니다.
4절에서 만들 도구 함수도 이 결과 글을 내놓습니다."""),
        code(DATA),
        md("""**결과 읽기** — 출력 줄 `기준 답: 일반 도서는 14일 동안 빌릴 수 있습니다.`가 보입니다.
라벨 `결과 글을 정한 도구:` 뒤에는 `'search_documents'`와 `'check_source'`가 있습니다.

다음 셀은 01절과 같은 도구 요청 둘로 기준 궤적을 만듭니다.
함수 `make_trajectory`와 `called_tool_names`는 01절에서 처음 적은 함수입니다."""),
        code(REFERENCE),
        md("""**결과 읽기** — 출력 줄 `기준 궤적의 도구 차례: ['search_documents', 'check_source']`와 `메시지 수: 6`이 보입니다.
01·02절의 기준 궤적과 같은 요청이고, 메시지 수도 같습니다.

다음 셀은 01절처럼 도구 요청은 기준과 같고, 답 글만 「7일」로 틀린 궤적을 만듭니다."""),
        code(WRONG),
        md("""**결과 읽기** — 출력 줄 `최종 답: 일반 도서는 7일 동안 빌릴 수 있습니다.`가 보입니다.
라벨 `도구 차례:` 뒤의 목록은 기준 궤적과 같습니다.

다음 셀은 02절처럼 모드 넷마다 평가 함수를 하나씩 만들어, 딕셔너리 `evaluators`에 모읍니다.
02절에서는 답만 틀린 궤적을 네 모드로 견주지 않았습니다."""),
        code(MAKE_MODES),
        md("""**결과 읽기** — 출력 줄 `평가 함수를 만든 모드: ['strict', 'unordered', 'subset', 'superset']`이 보입니다.

다음 셀은 답만 틀린 궤적을 네 모드로 견줍니다.
함수 `four_modes`는 모드 이름을 키로 한 점수 딕셔너리를 내놓습니다.
실행 전에 예상해 봅니다.
답 글이 틀렸다는 것을 잡는 모드가 있을까요?"""),
        code(WRONG_MODES),
        md("""**결과 읽기** — 출력 줄 `답만 틀림: {'strict': True, 'unordered': True, 'subset': True, 'superset': True}`가 보입니다.
네 모드 모두 참이었습니다.

네 모드는 도구 요청의 이름과 인자를 짝지을 뿐, 메시지 글은 견주지 않습니다.
그래서 답이 틀린 궤적도 도구를 기준대로 불렀다면 참입니다.
답 글까지 보려면, 궤적을 글로 읽는 쪽이 있어야 합니다.

다음 셀은 평가 모델이 받을 궤적 글을 만듭니다.
함수 `_format_inputs`에 실제 궤적과 기준 궤적을 넣으면, 두 궤적을 글로 바꾼 값 둘을 튜플로 내놓습니다.
번호 `[0]`이 실제 궤적 글이고, 번호 `[1]`이 기준 궤적 글입니다."""),
        code(FORMAT),
        md("""**결과 읽기** — 라벨 줄 `실제 궤적 글:` 아래가 평가 모델이 받는 궤적 글입니다.
메시지마다 `<user>`·`<assistant>`·`<tool>` 같은 태그로 감쌌습니다.
도구 요청은 `<tool_call>` 안에 이름과 인자를, 도구 메시지는 `<tool_result>` 안에 호출 ID와 글을 담았습니다.
마지막 `<assistant>` 태그 안에는 답 글 `일반 도서는 7일 동안 빌릴 수 있습니다.`가 그대로 있습니다.

이처럼 궤적의 메시지를 태그로 감싸 한 덩어리로 이은 글을, 이 절에서는 궤적 글이라고 부릅니다.
설치판 agentevals 0.0.9 `trajectory/llm.py` 77~95행이 이 함수입니다.
메시지를 태그로 감싸는 줄은 설치판 openevals 0.2.0 `utils.py` 427~454행에 있습니다.

다음 셀은 이 궤적 글에 답 글·검색 결과 글·호출 ID가 들어 있는지 봅니다.
셋 모두 모드 `strict`가 견주지 않는 것입니다."""),
        code(SEE),
        md("""**결과 읽기** — 네 줄 모두 `True`입니다.
출력 줄 `답 글이 들어 있는가: True`와 `검색 결과 글이 들어 있는가: True`가 보입니다.

평가 모델은 도구 요청뿐 아니라 답 글과 도구 결과 글까지 한 글로 받습니다.
그래서 답 글의 「7일」이 검색 결과 글의 「14일」과 맞지 않는다는 것도 글에 드러납니다.
호출 ID도 글에 들어갑니다.
4절 에이전트의 호출 ID는 모델 서비스가 정한 값이라, 실행마다 궤적 글이 조금씩 달라집니다.

## 3. 판정 기준과 평가 모델

Ch 15 02절에서는 판정할 기준을 적은 글을 판정 머리글이라고 불렀습니다.
이름 `TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE`는 라이브러리가 적어 둔 영어 판정 머리글입니다.
머리글 안에는 판정 기준과, 두 궤적 글을 끼울 자리 둘이 있습니다.
다음 셀은 판정 기준 줄을 출력하고, 2절의 두 궤적 글을 끼운 요청 글의 글자 수를 셉니다.
글 메서드 `startswith`와 `format`은 처음 쓰는 이름이라, 셀 주석에 한 줄씩 풀었습니다."""),
        code(RUBRIC),
        md("""**결과 읽기** — 라벨 줄 `판정 기준:` 아래 네 줄이 판정 기준입니다.
출력 줄 `요청 글의 글자 수: 1694`가 보입니다.

네 줄은 차례대로 이렇게 풉니다.
단계와 단계가 논리적으로 이어지는가, 한 단계씩 나아가는가를 봅니다.
완벽하지 않아도 되지만 필요 없는 단계가 적은가, 기준 궤적과 뜻이 같은가도 봅니다.
평가 모델은 이 요청 글을 받아, 네 기준에 맞는지 참·거짓 하나로 판정합니다.

다음 셀은 평가 모델로 궤적을 판정하는 평가 함수를 만듭니다.
인자 `judge=`에는 1절에서 만든 모델 객체를, 인자 `prompt=`에는 판정 머리글을 넣습니다.
이 셀도 평가 함수를 만들기만 하고, 모델 요청은 보내지 않습니다."""),
        code(MAKE_JUDGE),
        md("""**결과 읽기** — 출력 줄 `평가 함수의 종류: function`이 보입니다.
01절의 궤적 맞춰 보기처럼, 만든 것은 부를 수 있는 함수입니다.

설치판 openevals 0.2.0 `llm.py`를 보면, 이 함수를 부를 때마다 모델에 요청을 1번 보냅니다.
모델은 칸 `reasoning`(글)과 칸 `score`(참·거짓)를 담은 JSON 형식으로 답합니다.
이 답할 모양도 요청 글과 함께 모델에 넘어갑니다.
모양의 설명 글에는 칸 `reasoning`을 「Thus, the score should be」로 끝내라는 말이 적혀 있습니다.
그래서 5절 판정 출력의 끝에 그 문장이 보입니다.

평가 함수는 이를 칸 `key`·`score`·`comment`·`metadata`의 딕셔너리로 내놓습니다.
칸 `comment`에 든 글, 곧 평가 모델이 그렇게 판정한 까닭을 판정 까닭이라고 부르겠습니다.
이 모양은 설치판 소스로 본 것이고, 노트북에서는 5절에서 처음 부릅니다.

## 4. 실제 에이전트로 궤적 만들기

지금까지의 궤적은 모두 코드로 적은 메시지 목록이었습니다.
이 절의 뒤 절반은 도구 둘을 붙인 에이전트를 실제 모델로 한 번 실행해, 그 결과를 궤적으로 씁니다.
이처럼 평가할 궤적을 만드는 에이전트를 평가받는 에이전트라고 부르겠습니다.

다음 셀은 검색 도구를 만듭니다.
Ch 19 01절처럼 `@tool` 줄은 아래 함수를 도구로 등록하고, 독스트링은 모델이 읽는 도구 설명이 됩니다.
이 검색 도구는 교재용이라, 어떤 검색어에도 2절 결과 글 딕셔너리의 검색 결과 글을 내놓습니다."""),
        code(TOOL_SEARCH),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
매개변수 뒤의 `: str`은 Ch 19 01절에서 본 힌트로, 도구의 입력이 글이라고 알립니다.

다음 셀은 출처 확인 도구를 만듭니다.
문서 ID가 `LIB-001`이면 2절의 출처 확인 결과 글을, 아니면 그 문서가 없다는 글을 내놓습니다."""),
        code(TOOL_CHECK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 두 도구를 모델 없이 직접 불러 봅니다.
Ch 19 01절처럼 메서드 `invoke`에 인자 딕셔너리를 넣습니다."""),
        code(TOOL_TRY),
        md("""**결과 읽기** — 라벨 `검색:` 뒤에는 검색어 「책 대출 기간」과 상관없이 `[LIB-001]`로 시작하는 검색 결과 글이 있습니다.
출력 줄 `없는 문서: LIB-002 문서가 없습니다.`가 보입니다.
두 도구 모두 정해진 글을 내놓는 평범한 Python 함수라, 다시 실행해도 같은 글이 나옵니다.

다음 셀은 평가받는 에이전트를 만듭니다.
Ch 21 01절처럼 함수 `create_agent`에 모델 객체와 도구 목록, 시스템 메시지 글을 넘깁니다.
Ch 22 04절의 호출 한도 4를 붙여, invoke 한 번에 모델 요청이 4번을 넘지 않게 합니다.
Ch 20 03절의 설정 딕셔너리로 실행 한도 20도 줍니다.
시스템 메시지 글에는 검색한 뒤 출처를 확인하고 답하라는 차례를 적었습니다."""),
        code(AGENT),
        md("""**결과 읽기** — 출력 줄 `에이전트의 종류: CompiledStateGraph`와 `실행 한도: 20`이 보입니다.
Ch 21 01절에서 본 것처럼, 에이전트는 컴파일된 그래프입니다.

호출 한도는 모델 요청 수의 상한이고, 실행 한도는 그래프 단계 수의 상한입니다.
두 한도는 서로 다른 것이고, 둘 다 이 절의 실행에 드는 값보다 조금 크게 잡은 교재용 값입니다.

다음 셀에서 모델 요청이 처음 나갑니다.
질문 한 줄을 넣어 에이전트를 한 번 실행하고, 결과의 칸 `messages`를 궤적으로 씁니다.
Ch 19 06절 함수 `show_messages`로 메시지를 차례대로 봅니다.
실행 전에 예상해 봅니다.
에이전트는 시스템 메시지 글대로 도구 둘을 차례로 부를까요?"""),
        code(RUN),
        md("""**결과 읽기** — 출력 줄 `AIMessage | 도구 호출 요청: ['search_documents']`와 `AIMessage | 도구 호출 요청: ['check_source']`가 보입니다.
두 줄 뒤에는 `ToolMessage | 결과 상태: success`로 시작하는 줄이 하나씩 이어집니다.
마지막 줄 `AIMessage | 도구 호출 요청: []`는 도구를 요청하지 않은 응답, 곧 답입니다.
에이전트는 검색 → 출처 확인 → 답의 차례로 움직였습니다.

도구를 몇 번, 어떤 차례로 부를지는 모델이 고르는 값입니다.
노트북 밖에서 같은 실행을 다섯 번 해 보니 다섯 번 모두 이 차례였고, 새 커널 두 번에서도 같았습니다.

다음 셀은 결과 메시지의 종류를 모아, 시스템 메시지가 들어 있는지 봅니다.
결과에 시스템 메시지가 있으면, 기준 궤적과 메시지 수가 어긋나 모드 `strict`가 거짓이 됩니다."""),
        code(KINDS),
        md("""**결과 읽기** — 출력 줄 `시스템 메시지가 들어 있는가: False`가 보이고, `assert`도 오류 없이 지나갔습니다.
출력 줄 `메시지 수: 6`으로, 메시지 수는 기준 궤적과 같습니다.

함수 `create_agent`는 시스템 메시지 글을 모델에 보낼 때만 메시지 목록 앞에 붙입니다.
설치판 langchain 1.4.0 `agents/factory.py` 1451~1452행이 그 줄이고, 결과 목록에는 남기지 않습니다.
그래서 결과의 칸 `messages`를 기준 궤적과 그대로 견줄 수 있습니다.

Ch 26~28에서는 모델 요청 수를 「도구를 요청한 응답 수 + 1」로 셌습니다.
다음 셀은 도구를 요청한 응답 수를 세고, Ch 19 05절 함수 `sum_usage`로 센 요청 수와 견줍니다."""),
        code(COUNT),
        md("""**결과 읽기** — 출력 줄 `도구를 요청한 응답 수: 2`와 `모델 요청 수: 3`이 보입니다.
출력 줄 `모델 요청 수 = 도구를 요청한 응답 수 + 1: True`로, 셈이 맞았습니다.

도구를 요청한 응답 둘에, 답을 쓴 응답 하나가 더해졌습니다.
호출 한도 4 안이라 실행이 끝까지 갔습니다.
함수 `sum_usage`는 결과 목록의 응답만 세므로, 평가 모델 요청은 이 셈에 들어가지 않습니다.

다음 셀은 도구 차례와 모델이 쓴 도구 인자, 마지막 답 글을 봅니다.
인자와 답 글은 모델이 쓴 값이라 실행마다 달라질 수 있습니다."""),
        code(ARGS),
        md("""**결과 읽기** — 출력 줄 `도구 차례: ['search_documents', 'check_source']`가 보입니다.
라벨 `도구 인자:` 뒤에는 검색어와 문서 ID가, 라벨 `마지막 답 글:` 뒤에는 에이전트가 쓴 답이 있습니다.

교재 출력에서는 검색어가 「""" + "[[QUERY]]" + """」로, 기준 궤적의 「도서 대출 기간」과 달랐습니다.
문서 ID는 `LIB-001`로 기준과 같았고, 답 글은 기준 답과 글자까지 같았습니다.
02절 7절에서 본 것처럼, 인자 비교 방식이 기본값 `exact`면 검색어 하나만 달라도 네 모드 모두 거짓입니다.

## 5. 두 판정: 모드와 평가 모델

검색어는 모델이 고르는 값이라, 기준 궤적의 검색어와 다를 수 있습니다.
그래서 02절 7절의 도구별 덮어쓰기로 검색 도구의 인자만 보지 않고, 차례와 출처 문서 ID는 그대로 견줍니다.
다음 셀은 이런 평가 함수를 모드 넷마다 만들어 딕셔너리 `search_free`에 모읍니다."""),
        code(SEARCH_FREE),
        md("""**결과 읽기** — 출력 줄 `평가 함수를 만든 모드: ['strict', 'unordered', 'subset', 'superset']`이 보입니다.
네 평가 함수 모두 검색 도구 요청의 인자는 보지 않고, 출처 확인 요청의 인자는 기본값 `exact`로 견줍니다.

다음 셀은 에이전트 궤적을 이 네 평가 함수로 견줍니다.
모드 판정은 코드 규칙이라, 같은 궤적이면 늘 같은 판정이 나옵니다."""),
        code(AGENT_MODES),
        md("""**결과 읽기** — 출력 줄 `에이전트 궤적: {'strict': True, 'unordered': True, 'subset': True, 'superset': True}`가 보입니다.
네 모드 모두 참이었습니다.

검색어를 빼고 보면, 에이전트는 기준 궤적과 같은 도구를 같은 차례·같은 횟수로 불렀습니다.
출처 확인의 문서 ID도 기준과 같았습니다.
이 판정은 궤적이 정해지면 늘 같지만, 궤적을 만든 쪽은 모델이라 궤적은 실행마다 달라질 수 있습니다.

다음 셀은 3절에서 만든 평가 함수로 에이전트 궤적을 판정합니다.
평가 모델 요청이 1번 나갑니다.
칸 `key`·`score`는 한 줄씩, 판정 까닭은 라벨 줄 아래에 출력합니다.
실행 전에 예상해 봅니다.
검색어가 기준과 다른 이 궤적을, 평가 모델은 참으로 볼까요?"""),
        code(JUDGE_AGENT),
        md("""**결과 읽기** — 출력 줄 `칸 key: trajectory_accuracy`와 `칸 score: True`가 보입니다.
평가 모델도 에이전트 궤적을 참으로 판정했습니다.

라벨 줄 `판정 까닭:` 아래 글은 평가 모델이 영어로 쓴 판정 까닭입니다.
교재 출력의 판정 까닭은, 검색어 글과 호출 ID는 다르지만 판정에 상관없고 뜻이 같다는 줄거리였습니다.
판정 까닭의 글은 실행마다 조금씩 달라져, 이 절은 결론에 쓰지 않습니다.
점수 `True`는 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.

## 6. 값 바꿔 보기: 답 글 하나만 틀리게

이제 값 하나만 바꿔 봅니다.
바꿀 값은 에이전트 궤적의 마지막 답 글이고, 01절의 틀린 답 「7일」로 바꿉니다.
도구 요청과 도구 결과 글은 그대로 둡니다.
다음 셀은 궤적을 Ch 2 03절에서 배운 목록 메서드 `copy()`로 복사하고, 복사본의 마지막 자리 `[-1]`에 새 `AIMessage`를 넣습니다."""),
        code(WRONG_RUN),
        md("""**결과 읽기** — 출력 줄 `바꾼 뒤 답: 일반 도서는 7일 동안 빌릴 수 있습니다.`와 `도구 차례가 같은가: True`가 보입니다.
라벨 `바꾸기 전 답:` 뒤에는 에이전트가 쓴 답이 있습니다.

복사본만 바꿨으므로, 목록 `agent_messages`의 답 글은 그대로입니다.
다음 셀은 이 궤적을 모드 `strict`(검색어 뺌)와 평가 모델로 판정합니다.
평가 모델 요청이 1번 나갑니다.
실행 전에 예상해 봅니다.
두 판정 가운데 답 글이 바뀐 것을 잡는 쪽은 어느 쪽일까요?"""),
        code(WRONG_EVAL),
        md("""**결과 읽기** — 출력 줄 `모드 strict: True`와 `평가 모델 칸 score: False`가 보입니다.
답 글 하나만 바꾸자, 평가 모델의 판정만 참에서 거짓으로 바뀌었습니다.

모드 `strict`는 2절에서 본 것처럼 답 글을 견주지 않아, 바꾸기 전과 같은 참이었습니다.
평가 모델은 답 글까지 읽고, 기준 궤적과 뜻이 다르다고 판정했습니다.
교재 출력의 판정 까닭은, 도구를 부른 차례는 같지만 답이 14일이 아니라 7일이라 뜻이 맞지 않다는 줄거리였습니다.
점수 `False`는 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.

다음 셀은 5절과 이 절에서 담아 둔 판정을 한 표로 모읍니다.
앞 셀들의 값을 출력만 하므로 새 요청은 없습니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 `궤적 | 모드 strict(검색어 뺌) | 평가 모델` 아래 두 줄이 보입니다.
줄 `에이전트 궤적 | True | True`와 `답 글만 틀림 | True | False`입니다.

두 줄은 답 글만 다르고, 모드는 두 줄을 가르지 못했습니다.
평가 모델만 두 줄을 갈랐습니다.
반대로 모드는 판정 규칙을 코드로 적어, 같은 궤적에는 늘 같은 판정을 냅니다.
두 방법은 서로를 대신하지 않고, 보려는 것에 맞춰 함께 씁니다.

## 7. 요청 수와 예상 비용

이 노트북은 에이전트 실행 한 번과 평가 모델 판정 두 번에서 모델을 불렀습니다.
평가 모델 요청은 에이전트 결과 목록에 남지 않아, 함수 `sum_usage`로 셀 수 없습니다.
설치판 소스대로 판정 한 번을 요청 1번으로 보고, 판정 횟수 2를 손으로 적어 더합니다.
다음 셀은 요청 수를 모두 더하고, 에이전트 요청의 토큰과 예상 비용을 봅니다.
요금은 2026-09-17 요금표의 mini 값(100만 토큰당 달러)을 씁니다."""),
        code(COST),
        md("""**결과 읽기** — 출력 줄 `에이전트 요청 수: 3 | 평가 모델 요청 수: 2`와 `모두 합한 모델 요청 수: 5`가 보입니다.
에이전트 요청 수는 4절에서 센 값과 같습니다.

교재 출력에서는 에이전트 입력 토큰이 [[TIN]], 출력 토큰이 [[TOUT]]이었고, 예상 비용은 [[COST]]달러였습니다.
평가 모델 요청의 토큰은 이 노트북에서 세지 않았습니다.
노트북 밖에서 센 값으로는, 판정 한 번에 입력 679~682토큰, 출력 87~104토큰이었습니다.
토큰과 비용은 실행마다 달라질 수 있고, 청구 금액과도 다를 수 있습니다.

## 정리

1. 네 모드는 답만 틀린 궤적을 모두 참으로 봤습니다. 평가 모델이 받는 궤적 글에는 답 글과 도구 결과 글이 들어 있었습니다.
2. 평가받는 에이전트는 요청 3번으로 검색 → 출처 확인 → 답의 궤적을 만들었습니다. 검색어를 뺀 네 모드와 평가 모델이 모두 참으로 판정했습니다.
3. 답 글 하나만 바꾸자, 모드 `strict`는 참 그대로였고 평가 모델만 거짓을 냈습니다. 2·3번의 값은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.

04절에서는 모델을 부르지 않고, 앞 챕터가 저장한 실행 기록을 읽어 운영 지표를 견줍니다."""),
    ]


# 교재 출력(A 실행)의 흔들리는 값 — 결과 읽기 둘째 단락·b6 표·b7에만 쓰는 값(A 출력과 대조해 채움)
FILL = {
    "[[QUERY]]": "일반 도서 대출 기간 며칠",
    "[[TIN]]": "933",
    "[[TOUT]]": "63",
    "[[COST]]": "0.000983",
}


def filled(text: str) -> str:
    for key in FILL:
        text = text.replace(key, FILL[key])
    return text


def notebook_cells() -> list[dict]:
    result = []
    for cell in cells():
        if cell["cell_type"] == "markdown":
            cell["source"] = filled(cell["source"])
        result.append(cell)
    return result


# ---------------------------------------------------------------- _src 본문
def mermaid_block(name: str, alt: str, caption: str, reading: str) -> str:
    return ("{{mermaid:" + name + "|" + alt + "|" + caption + "}}\n"
            + '<p class="look"><b>도식 읽기</b> — ' + html_text(reading) + "</p>\n")


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


L_01 = "01-에이전트-평가-세-전략.html"
L_02 = author_01.L_02
L_04 = "04-운영-지표와-Ch18-궤적-비교.html"
L_CH06_06 = "../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html"
L_CH15_01 = author_01.L_CH15_01
L_CH15_02 = "../../part4/ch15-evaluation-advanced/02-4대-RAG-평가자.html"
L_CH15_03 = "../../part4/ch15-evaluation-advanced/03-judge-프롬프트와-편향.html"
L_CH18_05 = author_01.L_CH18_05
L_CH19_01 = "../../part5/ch19-model-tools/01-tool과-Ch4-함수-재사용.html"
L_CH19_05 = "../../part5/ch19-model-tools/05-bind_tools와-병렬-호출.html"
L_CH20_03 = "../../part5/ch20-tool-node/03-recursion-limit과-명시적-종료.html"
L_CH21_01 = "../ch21-create-agent/01-create-agent와-ReAct-루프.html"
L_CH21_06 = author_01.L_CH21_06
L_CH22_04 = "../ch22-middleware/04-호출-한도와-재시도-폴백.html"
L_CH27_02 = "../ch27-deepagents/02-create-deep-agent와-도구.html"

TERM_ROWS = [
    ("궤적 글", "궤적의 메시지를 역할 태그로 감싸 한 덩어리로 이은 글입니다. 평가 모델은 궤적을 메시지 목록이 아니라 이 글로 받습니다. 연극 대본에 대사마다 말한 사람의 이름을 붙여 적은 것과 같습니다. 이 절에서는 설치판 함수 <code>_format_inputs</code>가 만든 글을 노트북 2절에서 출력했습니다."),
    ("판정 까닭", "평가 모델이 점수와 함께 적어 내는, 그렇게 판정한 까닭 글입니다. 결과 딕셔너리의 칸 <code>comment</code>에 담깁니다. 시험 채점표에서 점수 옆에 적는 한 줄 평과 같습니다. 이 절의 판정 까닭은 영어로 왔고, 실행마다 글이 조금씩 달라져 결론에 쓰지 않았습니다."),
    ("평가받는 에이전트", "평가할 궤적을 만드는 에이전트입니다. 평가 모델과는 따로 실행되고, 요청 수도 따로 셉니다. 요리 대회에서 요리를 만드는 참가자와 맛을 보는 심사위원을 나누는 것과 같습니다. 이 절에서는 도구 둘과 호출 한도 4를 붙인 <code>library_agent</code>입니다."),
]

T = "<code>True</code>"
F = "<code>False</code>"
VERDICT_ROWS = [
    ("답만 틀린 궤적(코드로 적음)", "네 모드 모두 " + T, "부르지 않음", "노트북 2절"),
    ("에이전트 궤적", "네 모드 모두 " + T + "(검색어 뺌)", T, "노트북 5절"),
    ("에이전트 궤적에서 답 글만 틀리게 바꿈", "모드 <code>strict</code> " + T + "(검색어 뺌)", F, "노트북 6절"),
]
RUN_ROWS = [
    ("도구 차례", "<code>search_documents</code> → <code>check_source</code>", "다섯 번·두 커널 같음"),
    ("모델 요청 수", "<code>3</code> = 도구를 요청한 응답 수 <code>2</code> + 1", "다섯 번·두 커널 같음"),
    ("검색어", "「[[QUERY]]」", "교재 출력(모델이 쓴 값)"),
    ("마지막 답 글", "기준 답과 글자까지 같음", "교재 출력(모델이 쓴 값)"),
    ("에이전트 토큰·예상 비용", "입력 [[TIN]] · 출력 [[TOUT]] · [[COST]]달러", "교재 출력(요금표 어림)"),
    ("평가 모델 토큰(판정 한 번)", "입력 679~682 · 출력 87~104", "노트북 밖 판정 10번"),
]

LOOK_B5 = "노트북 2절에서 <code>답만 틀림: {'strict': True, 'unordered': True, 'subset': True, 'superset': True}</code>와 궤적 글의 태그를 봅니다. 3절에서 <code>요청 글의 글자 수: 1694</code>와 <code>평가 함수의 종류: function</code>을 찾습니다. 4절에서는 <code>시스템 메시지가 들어 있는가: False</code>와 <code>모델 요청 수 = 도구를 요청한 응답 수 + 1: True</code>를 확인합니다."
LOOK_B6 = "노트북 5절에서 <code>칸 score: True</code>를, 6절에서 <code>평가 모델 칸 score: False</code>와 두 줄 표를 확인합니다. 7절에서 <code>모두 합한 모델 요청 수: 5</code>를 봅니다. 판정 까닭 글과 토큰은 다시 실행하면 달라질 수 있습니다."


def runs_paragraph() -> str:
    if not RUNS_SENTENCE:
        return ""
    return "<p>" + RUNS_SENTENCE + "</p>\n"


def src_html() -> str:
    terms = table_html(["말", "뜻"], TERM_ROWS)
    verdict_table = table_html(["궤적", "궤적 맞춰 보기", "평가 모델", "노트북"], VERDICT_ROWS)
    run_table = filled(table_html(["값", "교재 출력", "성격"], RUN_ROWS))
    text = """<!--meta: 강의 0.75h | 실습 1.25h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>궤적 맞춰 보기의 모드와 평가 모델(judge)이 궤적에서 보는 것을 출력으로 견줘 말할 수 있습니다.</li>
<li>평가받는 에이전트를 실제로 실행해 만든 궤적을, 모드와 평가 모델로 함께 판정할 수 있습니다.</li>
<li>답 글 하나만 바꾼 궤적에서 두 판정이 어떻게 갈리는지 설명하고, 모델 요청 수를 셀 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_01 + """\">01절</a>과 <a href=\"""" + L_02 + """\">02절</a>의 궤적 맞춰 보기는 도구 요청의 이름과 인자를 코드 규칙으로 짝지었습니다. 그래서 도구를 기준대로 부르고 답만 틀린 궤적도 참이었습니다. 답이 맞는지, 단계가 뜻이 통하는지는 궤적을 글로 읽어야 판정할 수 있습니다. Ch 15에서 배운 평가 모델이 그 일을 맡습니다.</p><p>이 절은 먼저 모델을 부르지 않고, 평가 모델이 궤적을 어떤 글로 받는지 봅니다. 이어서 이 챕터에서 처음으로 에이전트를 실제 모델로 실행해 궤적을 만듭니다. 그 궤적을 02절의 모드와 평가 모델로 함께 판정하고, 답 글 하나만 바꿔 두 판정을 견줍니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_01 + """\">01절</a>에서는 최종 답 평가·한 단계 평가·궤적 평가를 견줬습니다. 도구 요청이 기준과 같고 답 글만 틀린 궤적은 모드 <code>strict</code>에서 참이었습니다. 01절은 뜻을 보는 판정을 이 절의 평가 모델 몫으로 남겼습니다. <a href=\"""" + L_02 + """\">02절</a>에서는 네 모드와 짝짓기, 인자 비교 방식과 도구별 덮어쓰기를 봤습니다. 이 절은 두 절에서 처음 적은 함수를 도구 파일에서 가져옵니다.</p><p><a href=\"""" + L_CH15_01 + """\">Ch 15 01절</a>에서는 다른 모델이 쓴 답을 읽고 판정하는 모델을 평가 모델이라고 불렀습니다. <a href=\"""" + L_CH15_02 + """\">02절</a>은 판정 기준을 적은 글을 판정 머리글, 판정할 내용을 끼운 글을 판정 요청 글이라고 불렀습니다. <a href=\"""" + L_CH15_03 + """\">03절</a>은 평가 모델의 판정이 치우칠 수 있다는 것을 봤습니다. Ch 15는 판정 머리글을 손으로 적었고, 이 절은 라이브러리가 적어 둔 머리글을 씁니다.</p><p><a href=\"""" + L_CH19_01 + """\">Ch 19 01절</a>에서는 <code>@tool</code> 줄로 도구를 만들고 메서드 <code>invoke</code>로 불렀습니다. <a href=\"""" + L_CH21_01 + """\">Ch 21 01절</a>에서는 함수 <code>create_agent</code>에 모델 객체와 도구 목록을 넘겨 에이전트를 만들었습니다. <a href=\"""" + L_CH22_04 + """\">Ch 22 04절</a>의 호출 한도는 Ch 26~28에서 모델을 부르는 에이전트마다 붙였습니다. <a href=\"""" + L_CH27_02 + """\">Ch 27 02절</a>처럼 요청 수는 「도구를 요청한 응답 수 + 1」로 셉니다. 실행 한도를 주는 설정 딕셔너리는 <a href=\"""" + L_CH20_03 + """\">Ch 20 03절</a>에서 봤습니다.</p><p><a href=\"""" + L_CH21_06 + """\">Ch 21 06절</a>에서는 두 흐름의 답을 평가 모델로 판정했고, 판정 여섯이 모두 1이었습니다. 그 절은 답을 판정했고, 이 절은 도구를 부른 차례까지 담은 궤적을 판정합니다. 요청 수는 <a href=\"""" + L_CH19_05 + """\">Ch 19 05절</a>의 <code>sum_usage</code>로, 예상 비용은 <a href=\"""" + L_CH06_06 + """\">Ch 6 06절</a>의 <code>estimate_cost</code>로 셉니다. 목록을 복사하는 <code>copy()</code>는 <a href=\"../../part1/ch02-python/03-자료구조.html\">Ch 2 03절</a>에서 배웠습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01·02절에서는 오르골 종이띠의 구멍을 기준 띠에 대 봤습니다. 두 띠를 겹쳐 보면, 구멍이 같은 자리에 같은 수만큼 있는지는 바로 보입니다. 그러나 겹쳐 보는 것만으로는 곡이 어떻게 들리는지 모릅니다. 기준 곡과 같은 노래인지 보려면, 띠를 오르골 기계에 넣어 울려 봐야 합니다.</p><p>겹쳐 보는 쪽이 궤적 맞춰 보기의 모드이고, 울려 보는 쪽이 궤적 글을 읽는 평가 모델입니다. 구멍 자리는 도구 요청이고, 울려 나는 곡은 답 글까지 담은 궤적의 뜻입니다. 비유와 다른 점도 있습니다. 오르골은 같은 띠를 넣으면 늘 같은 곡이 나지만, 평가 모델은 같은 궤적에도 판정이 달라질 수 있습니다. 그래서 이 절은 평가 모델의 점수를 노트북 밖에서 다섯 번 더 확인하고 씁니다.</p>
""" + illustration_block() + """<h3>평가 모델이 받는 글</h3><p>평가 모델에 궤적을 넘기면, 라이브러리가 메시지마다 역할 태그로 감싸 한 덩어리 글로 바꿉니다. 도구 요청은 이름과 인자를, 도구 메시지는 호출 ID와 결과 글을, 마지막 응답은 답 글을 그대로 담습니다. 이 글을 이 절에서는 궤적 글이라고 부릅니다. 실제 궤적 글과 기준 궤적 글은 판정 머리글의 두 자리에 끼워져, 요청 글 하나가 됩니다.</p><p>판정 머리글 <code>TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE</code>에는 판정 기준 네 줄이 있습니다. 단계 사이가 논리적으로 이어지는가, 한 단계씩 나아가는가를 봅니다. 완벽하지 않아도 되지만 필요 없는 단계가 적은가, 기준 궤적과 뜻이 같은가도 봅니다. 평가 모델은 이 네 기준으로 참·거짓 하나와 판정 까닭을 냅니다.</p><p>평가 함수를 만들 때 인자 <code>judge=</code>에 모델 객체를 넘겼습니다. 인자 <code>model=</code>에 모델 이름 글만 넘기면, 설치판은 온도·추론 설정 없이 모델을 만듭니다. 설치판 openevals 0.2.0 <code>llm.py</code> 251~254행이 그 줄입니다. 그래서 과정 표준 설정(<code>temperature=0</code>·<code>reasoning_effort="none"</code>)의 모델 객체를 만들어 넘겼습니다.</p>
""" + terms + """
<p>새 말을 이 절 코드에서 보면 이렇습니다. 궤적 글은 <code>_format_inputs(wrong_answer, reference)</code>가 내놓은 튜플의 <code>[0]</code>입니다. 판정 까닭은 평가 함수 결과의 칸 <code>comment</code>이고, 평가받는 에이전트는 <code>library_agent</code>입니다. 평가받는 에이전트의 요청은 <code>sum_usage</code>로 세고, 평가 모델의 요청은 판정을 부른 횟수로 따로 셉니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 01절의 답만 틀린 궤적을 네 모드로 견주고, 같은 궤적의 궤적 글을 출력합니다. 3절은 판정 기준 줄과 요청 글의 글자 수를 보고, 평가 함수를 만들기만 합니다. 4절은 도구 둘을 붙인 에이전트를 실제 모델로 한 번 실행하고, 요청 수를 셉니다. 5절은 그 궤적을 모드와 평가 모델로 판정하고, 6절은 답 글 하나만 바꿔 다시 판정합니다. 7절은 평가 모델 요청까지 더한 요청 수와 예상 비용을 봅니다.</p><p>모델 요청은 4~6절에서만 나갑니다. 교재 출력에서는 에이전트 요청 3번과 평가 모델 요청 2번, 모두 5번이었습니다. 예상 비용은 요금표로 어림해 약 0.003달러이고, 청구 금액과는 다를 수 있습니다. 읽는 파일은 <code>.env</code>와 도구 파일 <code>eval_tools.py</code>이고, 쓰는 파일은 없습니다. 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>답만 틀린 궤적은 네 모드 모두 참이었습니다. 네 모드는 도구 요청의 이름과 인자를 짝지을 뿐, 답 글을 견주지 않기 때문입니다. 같은 궤적의 궤적 글에는 답 글과 도구 결과 글이 모두 들어 있었습니다. 평가 모델은 모드가 보지 않는 글까지 받습니다.</p><p>평가받는 에이전트는 검색 → 출처 확인 → 답의 차례로 움직였고, 모델 요청은 3번이었습니다. 요청 수는 도구를 요청한 응답 수 2에 1을 더한 값과 같았습니다. 검색 도구의 인자만 빼고 보자, 네 모드 모두 이 궤적을 참으로 봤습니다. 평가 모델도 이 궤적을 참으로 판정했습니다. 이 값들은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>에이전트 궤적의 답 글 하나만 01절의 틀린 답으로 바꾸자, 모드 <code>strict</code>는 참 그대로였고 평가 모델만 거짓을 냈습니다. 평가 모델의 이 거짓도 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다. 모드는 규칙을 코드로 적어 같은 궤적에 늘 같은 판정을 내지만, 답 글은 보지 않습니다. 평가 모델은 답 글까지 읽지만, 판정은 모델이 내는 값이라 실행마다 달라질 수 있습니다. 그래서 차례·도구·인자처럼 코드로 적을 수 있는 것은 모드로, 뜻은 평가 모델로 봅니다.</p>
<p>아래 표는 노트북 2·5·6절의 판정을 모은 것입니다.</p>
""" + verdict_table + """
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>아래 표는 에이전트 실행에서 나온 값과, 그 값을 어디까지 믿을 수 있는지입니다. 모델이 쓴 값과 토큰은 결론에 쓰지 않았습니다.</p>
""" + run_table + """
""" + runs_paragraph() + """<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>에이전트의 도구 차례와 평가 모델의 점수는 모델이 내는 값입니다. 노트북에 넣기 전에 같은 실행을 노트북 밖에서 다섯 번 해 보니, 도구 차례·요청 수·네 모드·두 점수가 모두 같았습니다. 그래도 같은 요청이 늘 같은 판정을 낸다고 할 수는 없습니다. 같은 요청도 실행한 때에 따라 판정이 달라질 수 있습니다.</li><li>판정 까닭은 영어로 왔고, 노트북 밖 다섯 번에서도 글이 조금씩 달랐습니다. 이 절은 판정 까닭의 줄거리만 결과 읽기 둘째 단락에 적었고, 결론에는 점수만 썼습니다.</li><li>평가받는 에이전트와 평가 모델은 같은 모델 객체 gpt-5.4-mini를 썼습니다. 제가 만든 궤적을 제가 판정하는 셈이라, Ch 15 03절에서 본 치우침이 끼어들 수 있습니다. 다른 모델로 판정하는 장면은 이 절에서 실행하지 않았습니다.</li><li>검색 도구는 어떤 검색어에도 같은 글을 내놓는 교재용 함수입니다. 시스템 메시지 글에는 검색 뒤 출처를 확인하는 차례를 적었고, 기준 궤적도 그 차례로 정했습니다. 흐름을 보여 주려고 실행 전에 정한 예이고, 결과를 보고 바꾸지 않았습니다.</li><li>호출 한도 4와 실행 한도 20은 요청 3번인 이 절의 실행에 드는 값보다 넉넉히 잡은 값입니다. 이 실행이 그래프 단계를 몇 번 거쳤는지는 이번에 세지 않았습니다. 이 노트북에서 두 한도에 닿은 실행은 없었습니다.</li><li>평가 모델 요청 수 2는 판정을 부른 횟수를 손으로 적은 값입니다. 판정 한 번에 요청 1번이라는 것은 설치판 openevals 0.2.0 <code>llm.py</code> 256~272행으로 봤습니다. 평가 모델 요청의 토큰은 노트북에서 세지 않았습니다. 노트북 밖 판정 10번에서 한 번은 입력 679~682, 출력 87~104토큰이었습니다.</li><li>교재 출력의 에이전트 예상 비용은 [[COST]]달러였습니다. 평가 모델 두 번을 노트북 밖 토큰으로 어림하면 약 0.0019달러라, 노트북 한 번에 약 0.003달러입니다. 요금표는 2026-09-17 mini 값이고, 청구 금액과는 다를 수 있습니다.</li><li>궤적 글에는 호출 ID가 들어갑니다. 에이전트의 호출 ID는 모델 서비스가 정한 값이라 실행마다 달라, 평가 모델이 받는 글도 조금씩 달라집니다. 노트북 밖에서는 평가 모델 입력 토큰도 679~682로 조금씩 달랐습니다.</li><li>함수 <code>_format_inputs</code>처럼 밑줄로 시작하는 이름은 라이브러리가 안에서 쓰는 함수입니다. 판이 바뀌면 이름이나 모양이 바뀔 수 있어, 평가 모델이 받는 글을 보는 데만 썼습니다.</li><li>인자 <code>continuous=True</code>를 주면 점수가 0~1 사이 소수가 되고, 인자 <code>choices</code>를 주면 정한 값 가운데 하나가 됩니다. 기준 궤적 없이 판정하는 머리글 <code>TRAJECTORY_ACCURACY_PROMPT</code>도 있습니다. 셋 모두 설치판 소스와 공식 설명으로 본 것이고, 이 노트북에서는 실행하지 않았습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>네 모드는 답만 틀린 궤적을 모두 참으로 봤습니다. 평가 모델이 받는 궤적 글에는 답 글과 도구 결과 글이 들어 있었습니다.</li><li>평가받는 에이전트는 요청 3번으로 검색 → 출처 확인 → 답의 궤적을 만들었습니다. 검색어를 뺀 네 모드와 평가 모델이 모두 참으로 판정했습니다.</li><li>답 글 하나만 바꾸자, 모드 <code>strict</code>는 참 그대로였고 평가 모델만 거짓을 냈습니다. 둘째·셋째 줄의 값은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_04 + """\">04절</a>에서는 모델을 부르지 않고, 앞 챕터가 저장한 실행 기록을 읽어 운영 지표를 견줍니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 답만 틀린 궤적을 네 모드로 견주면 어떻게 되고, 까닭은 무엇인가요?</p><p class="quiz-a">네 모드 모두 참입니다. 네 모드는 도구 요청의 이름과 인자를 짝지을 뿐, 답 글을 견주지 않습니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">2. 에이전트 궤적에서 답 글 하나만 틀린 글로 바꾸자, 모드 <code>strict</code>와 평가 모델의 판정은 어떻게 되었나요?</p><p class="quiz-a">모드 <code>strict</code>는 참 그대로였고, 평가 모델만 거짓을 냈습니다. 평가 모델은 답 글까지 담은 궤적 글을 읽기 때문입니다. 이 거짓은 노트북 밖 다섯 번과 새 커널 두 번에서 같았지만, 모델이 내는 값이라 늘 같다고 할 수는 없습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">3. 동료가 평가 함수를 <code>model="openai:gpt-5.4-mini"</code>로 만들자고 합니다. 이 절과 무엇이 달라지나요?</p><p class="quiz-a">설치판은 이름 글만 받으면 온도·추론 설정 없이 모델을 만듭니다. 이 절은 <code>temperature=0</code>·<code>reasoning_effort="none"</code>을 준 모델 객체를 인자 <code>judge=</code>로 넘겼습니다. 틀렸다면 본문 「평가 모델이 받는 글」을 다시 읽습니다.</p><p class="quiz-q">4. 에이전트가 도구를 세 번 요청한 뒤 답하고, 그 궤적을 평가 모델로 두 번 판정했다면 모델 요청은 모두 몇 번일까요?</p><p class="quiz-a">6번입니다. 에이전트 요청은 도구를 요청한 응답 셋에 답을 쓴 응답 하나를 더한 4번이고, 평가 모델 요청은 판정 두 번에 2번입니다. 에이전트 요청 4번은 호출 한도 4 안입니다. 틀렸다면 노트북 4절과 7절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langchain/test/evals">LangChain Agent evals</a></div>확인 2026-09-29 · 평가 모델로 궤적을 판정하는 함수 <code>create_trajectory_llm_as_judge</code>를 적습니다. 기준 궤적 없이도 판정할 수 있고, 기준 궤적이 있으면 <code>TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE</code>를 쓴다고 적습니다. 예시는 인자 <code>model=</code>에 모델 이름 글을 넘깁니다.</li><li><div><a href="https://github.com/langchain-ai/agentevals">agentevals (GitHub)</a></div>확인 2026-09-29 · 인자 <code>judge</code>에 LangChain 채팅 모델이나 OpenAI 클라이언트를 넘길 수 있다고 적습니다. 결과 예시의 칸은 <code>key</code>·<code>score</code>·<code>comment</code>입니다.</li><li><div><a href="https://github.com/langchain-ai/openevals">openevals (GitHub)</a></div>확인 2026-09-29 · LangChain 채팅 모델 객체를 <code>judge</code>로 바로 넘길 수 있다고 적습니다. 그 모델은 구조화 출력을 지원해야 합니다. 인자 <code>continuous</code>·<code>choices</code>·<code>use_reasoning</code>의 뜻도 적습니다.</li><li>설치판 agentevals 0.0.9 <code>trajectory/llm.py</code> 27~49행은 기준 궤적을 넣는 판정 머리글이고, 30~36행이 판정 기준입니다. 77~95행은 궤적 글을 만드는 함수, 98~173행은 평가 함수를 만드는 함수입니다.</li><li>설치판 openevals 0.2.0 <code>llm.py</code> 70~117행은 출력 형식(칸 <code>reasoning</code>·<code>score</code>)입니다. 251~254행은 모델 이름 글만 받았을 때 모델을 만드는 줄이고, 256~272행은 요청 한 번입니다. <code>utils.py</code> 427~454행은 메시지를 태그로 감싸는 줄입니다.</li><li>설치판 langchain 1.4.0 <code>agents/factory.py</code> 1451~1452행은 시스템 메시지 글을 요청 때만 앞에 붙이는 줄입니다.</li></ul>
"""
    return filled(text)


def write_src(path: Path) -> Path:
    path.write_text(src_html(), encoding="utf-8")
    return path


if __name__ == "__main__":
    check_tools()
    check_same_as_probe()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "eval_tools.py").write_text(TOOLS_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    if "--try" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--try") + 1])
        write_tools(target / "eval_tools.py")
        print("wrote", write_src(target / "src.html"))
        print("wrote", write_notebook(target, "03", SLUG, "experiment", notebook_cells()))
        raise SystemExit(0)
    print("wrote", write_src(SRC))
    if "--src-only" not in sys.argv:
        # 도구 파일은 없거나 01판·02판·이 판일 때만 쓴다. 뒤 절이 함수를 더한 판이면 덮어쓰지 않는다(Ch 24 마감 A-10·Ch 25~28 교훈).
        write_tools(TOOLS_PATH)
        path = write_notebook(LAB, "03", SLUG, "experiment", notebook_cells())
        print("wrote", path)
