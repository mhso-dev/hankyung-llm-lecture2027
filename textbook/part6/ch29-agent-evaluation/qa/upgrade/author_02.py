"""Ch 29 02절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 -B author_02.py              → 도구 파일(가드) + 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_02.py --src-only   → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_02.py --tools-copy DIR → 디스크의 도구 파일을 DIR에 복사한다(새 커널 사본 B 실행용)
  python3 -B author_02.py --try DIR    → 노트북과 이 판 도구 파일을 DIR에만 쓴다(실습 폴더를 건드리지 않는 시험 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**, 슬러그 그대로.

## 결정 1 — 모델 없음 (챕터 리드 결정 1)

궤적은 모두 코드로 적은 메시지 목록(Ch 20 01 손으로 만든 AIMessage 선례). 모델 요청 0, 키 셀·dotenv 없음.
설치판 궤적 맞춰 보기는 결정적이라 새 커널 두 번 셀별 출력이 같아야 한다(노트북 밖 /tmp/ch29-02/exp/p1.py 두 번 같음).

## 결정 2 — 네 모드를 같은 기준 궤적과 견준다 (01 인계 1~9)

기준 궤적 = 01절과 같은 search_documents(query) → check_source(doc_id) → 답. 비교 궤적:
차례 바꿈(strict F, 나머지 T) · 한 응답에 요청 둘(strict F — 메시지 수 5 ≠ 6, 나머지 T) · 검색만(subset만 T) ·
예약을 더함(reserve_book — superset만 T) · 검색 세 번(01 wasteful, superset만 T — 짝짓기는 횟수까지 셈).
모드 셋(unordered·subset·superset)의 본문 말은 이 절이 첫 자리에서 정의한다. 「짝짓기」도 이 절의 새 말.
이름만 보는 교재용 함수 unpaired_names로 두 방향 짝 없는 이름을 보여 주고, 표로 모드 판정과 맞는지 견준다.

## 결정 3 — 값 바꿔 보기 = 인자 비교 방식 (01 인계 7)

인자만 다른 궤적 셋(검색어가 다름·인자를 더함 top_k·인자가 빠짐)은 기본 exact에서 네 모드 모두 F.
값 하나 tool_args_match_mode exact → ignore(모드 strict)로 T. 이어 인자 비교 방식 넷 × 궤적 셋 표(모드 strict만 —
설치판은 모드 subset에서 짝짓기 방향을 바꾸고 unordered에서 두 방향이라 인자 subset·superset 결과가 모드마다 다름:
노트북 밖에서만 봄, b7). 도구별 덮어쓰기 {"search_documents": "ignore"}: 검색어가 다름 T · 출처 문서가 다름 F.

## 결정 4 — assert는 모드에 따라 갈린 결정적 값에만 (01 인계 8)

차례 바꿈·검색만·예약을 더함·검색 세 번·값 바꿔 보기에 두 줄씩(열 줄). 자기 자신과 견준 참처럼 만든 대로 늘 참인 값에는 걸지 않는다.

## 결정 5 — 도구 파일 eval_tools.py 02절 판 (01 인계 10, 챕터 공통 「도구 파일」)

01절 셀 셋(make_trajectory·called_tool_names·trajectory_pass)을 01 노트북 셀의 주석과 본문 글자 그대로 더한다
(주석 `# Ch 29 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다`). make_trajectory가 메시지 클래스를 써서
가져오기 줄 하나(langchain.messages)를 머리 설명과 첫 `# Ch` 주석 사이에 둔다(author_01.strip_later_imports가 빼고 견줌).
대조 사슬: author_01.check_tools() → strip_later_imports(02판).startswith(author_01.TOOLS) → 셀 글 해시 고정 → 01 노트북 디스크 셀과 같음 → AST 같음.
쓰기 가드: 없거나 01판·이 판일 때만 쓰고, 뒤 절이 더한 판(가져오기 줄을 뺀 글이 이 판으로 시작)은 skip. 01 노트북은 다시 실행하지 않는다
(01이 가져오는 show_messages·tool_call_names는 그대로 — 01 설치 셀에 langchain이 있어 새 가져오기 줄도 만족, 규격 §2-7 6번).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`.items`·`+=`·기본값 매개변수·힌트·대입 풀기·별표 풀기·`while`·`try`·
세미콜론·`isinstance`·클래스·데코레이터·`async`. 호출 깊이 2 이하. 새로 쓴 목록 메서드 `count`·`remove`(한 문장씩), 목록 `copy()`는 Ch 2 03·딕셔너리 `copy()`는 Ch 18 05(마감 A-3·A-7).
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
import author_01  # noqa: E402  01절 셀 글·도구 파일 01판·본문 도우미
from nbkit import code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch29-agent-evaluation/notebooks"
FIGS = ROOT / "textbook/part6/ch29-agent-evaluation/figures"
SLUG = "02-궤적-매칭-네-모드"
TITLE_TEXT = "궤적 매칭 네 모드"
SRC = ROOT / "textbook/part6/ch29-agent-evaluation/_src" / (SLUG + ".html")
TOOLS_PATH = LAB / "eval_tools.py"
NB01 = LAB / (author_01.SLUG + ".ipynb")
RUNS_SENTENCE = os.environ.get("AUTHOR02_RUNS_SENTENCE", "새 커널로 두 번 실행해 견주자, 코드 셀 스물일곱의 출력이 셀마다 모두 같았습니다. 모델을 부르지 않아, 이 절의 판정은 코드로 적은 궤적과 모드의 규칙으로 정해집니다.")
html_text = author_01.html_text
table_html = author_01.table_html


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- 도구 파일 eval_tools.py (02절 판)
TOOLS_HEAD = author_01.TOOLS_HEAD
TOOLS_IMPORTS = ("# 01절에서 옮긴 함수 make_trajectory가 만드는 메시지 클래스 셋(Ch 13 04절·Ch 19 05절)을 가져옵니다\n"
                 "from langchain.messages import AIMessage, HumanMessage, ToolMessage\n")
NOTE_01 = "Ch 29 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다"
CELLS_01 = [
    ("make_trajectory", author_01.DEF_MAKE, "0d16e83782ce0c92d38408415a42c5d03e5edd95febd1ea028be3ca1a8151e57"),
    ("called_tool_names", author_01.DEF_CALLED, "e360d145b946c73a47ca4b724ff208cec393fe8efa1d2bc363ecbc7260f44479"),
    ("trajectory_pass", author_01.DEF_TRAJ, "bc6987c9ce7e85c1016516e3a2ee06649da7fa84558a64ea94a06660e19e3d3c"),
]
TOOL_ORDER = ["tool_call_names", "show_messages", "make_trajectory", "called_tool_names", "trajectory_pass"]
IMPORT_LINES = ["from langchain.messages import AIMessage, HumanMessage, ToolMessage"]


def tools_text() -> str:
    text = TOOLS_HEAD + TOOLS_IMPORTS + author_01.TOOLS[len(TOOLS_HEAD):]
    for name, cell_source, cell_sha in CELLS_01:
        text = text + "\n\n# " + NOTE_01 + "\n" + cell_source + "\n"
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
    """02절 판이 01절 판(대조 사슬)으로 시작하고, 더한 함수 셋이 01 노트북 셀과 글자·AST 모두 같은지 봅니다."""
    author_01.check_tools()
    assert author_01.strip_later_imports(TOOLS).startswith(author_01.TOOLS), "02절 판이 01절 판으로 시작하지 않습니다"
    tree = ast.parse(TOOLS)
    names = []
    imports = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
    assert names == TOOL_ORDER, names
    assert imports == IMPORT_LINES, imports
    nb01 = notebook_code_sources(NB01)
    for name, cell_source, cell_sha in CELLS_01:
        assert sha(cell_source) == cell_sha, name + " 셀 글이 고정 해시와 다릅니다"
        assert cell_source in nb01, name + "가 01절 노트북 디스크 셀과 다릅니다"
        assert ("# " + NOTE_01 + "\n" + cell_source + "\n") in TOOLS
        mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        theirs = [ast.dump(n) for n in ast.parse(cell_source).body if isinstance(n, ast.FunctionDef)]
        assert mine == theirs and len(mine) == 1, name


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
    elif current == "" or current == author_01.TOOLS:
        path.write_text(TOOLS, encoding="utf-8")
        print("wrote", path)
    elif later_version(current):
        print("skip", path, "(뒤 절이 함수를 더한 판 — 덮어쓰지 않음)")
    else:
        raise AssertionError("도구 파일이 01절 판도 02절 판도 아닙니다")


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["agentevals==0.0.9", "langchain==1.4.0"])

IMPORTS = r'''# 궤적을 맞춰 보는 평가 함수를 만드는 함수와, 메시지 클래스 셋(Ch 13 04절·Ch 19 05절)을 가져옵니다
from agentevals.trajectory.match import create_trajectory_match_evaluator
from langchain.messages import AIMessage, HumanMessage, ToolMessage
# 01절에서 배운 함수 셋은 도구 파일에서 가져옵니다
from eval_tools import called_tool_names, make_trajectory, trajectory_pass

print("도구 파일에서 가져온 함수:", "called_tool_names, make_trajectory, trajectory_pass")'''

DATA = r'''# 질문과 기준 답, 도구마다 돌아올 결과 글을 정합니다(01절과 같은 글에 예약 도구의 글 하나를 더함)
question = "일반 도서는 며칠 동안 빌릴 수 있나요?"
reference_answer = "일반 도서는 14일 동안 빌릴 수 있습니다."
tool_results = {
    "search_documents": "[LIB-001] 일반 도서는 14일 동안 대출할 수 있습니다. 예약자가 없으면 한 번 연장할 수 있습니다.",
    "check_source": "LIB-001 문서가 있습니다. 제목: 도서 대출 기간",
    "reserve_book": "B-102 도서를 예약했습니다.",
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
reference_names = called_tool_names(reference)
print("기준 궤적의 도구 차례:", reference_names)
print("메시지 수:", len(reference))'''

MAKE_MODES = r'''# 모드 넷마다 궤적을 맞춰 보는 평가 함수를 하나씩 만들어, 모드 이름을 키로 딕셔너리에 모읍니다
modes = ["strict", "unordered", "subset", "superset"]
evaluators = {}
for mode in modes:
    evaluators[mode] = create_trajectory_match_evaluator(trajectory_match_mode=mode)
print("평가 함수를 만든 모드:", list(evaluators))'''

SELF_CHECK = r'''# 기준 궤적을 자기 자신과 견줘, 모드마다 결과 딕셔너리의 칸 key와 score를 봅니다
for mode in evaluators:
    result = evaluators[mode](outputs=reference, reference_outputs=reference)
    print(mode, "|", result["key"], "|", result["score"])'''

DEF_FOUR = r'''# 한 궤적을 네 모드의 평가 함수로 모두 견줘, 모드 이름을 키로 한 점수 딕셔너리로 내놓습니다
def four_modes(messages, reference, evaluators):
    row = {}
    for mode in evaluators:
        # 01절 함수 trajectory_pass가 결과 딕셔너리에서 칸 score만 꺼냅니다
        row[mode] = trajectory_pass(messages, reference, evaluators[mode])
    return row'''

REVERSED = r'''# 출처 확인을 먼저 하고 검색을 뒤에 하는, 차례를 바꾼 궤적을 만듭니다(01절의 차례 바꿈과 같은 요청)
reversed_calls = [
    {"name": "check_source", "args": source_args, "id": "call_1", "type": "tool_call"},
    {"name": "search_documents", "args": search_args, "id": "call_2", "type": "tool_call"},
]
reversed_order = make_trajectory(question, reversed_calls, tool_results, reference_answer)
print("도구 차례:", called_tool_names(reversed_order))'''

REVERSED_EVAL = r'''# 차례를 바꾼 궤적을 네 모드로 견줍니다
reversed_row = four_modes(reversed_order, reference, evaluators)
print("차례 바꿈:", reversed_row)
# 모드에 따라 갈린 두 값이 다시 실행해도 같은지 assert로 확인합니다
assert not reversed_row["strict"]
assert reversed_row["unordered"]'''

TWO_IN_ONE = r'''# 모델 응답 하나가 검색과 출처 확인을 함께 요청한 궤적을 손으로 만듭니다(한 응답에 도구 호출 요청 둘)
both_calls = AIMessage(content="", tool_calls=reference_calls)
two_in_one = [HumanMessage(content=question), both_calls]
# 도구 메시지 둘은 요청과 같은 호출 ID를 달고 차례대로 붙입니다
two_in_one.append(ToolMessage(content=tool_results["search_documents"], tool_call_id="call_1"))
two_in_one.append(ToolMessage(content=tool_results["check_source"], tool_call_id="call_2"))
two_in_one.append(AIMessage(content=reference_answer))
print("도구 차례:", called_tool_names(two_in_one), "| 메시지 수:", len(two_in_one))'''

TWO_EVAL = r'''# 한 응답에 요청 둘인 궤적을 네 모드로 견줍니다
two_row = four_modes(two_in_one, reference, evaluators)
print("한 응답에 요청 둘:", two_row)'''

SHORT = r'''# 검색만 하고 출처 확인은 하지 않은 궤적을 만듭니다(답은 기준과 같은 글)
short_calls = [reference_calls[0]]
short = make_trajectory(question, short_calls, tool_results, reference_answer)
print("도구 차례:", called_tool_names(short))'''

SHORT_EVAL = r'''# 검색만 한 궤적을 네 모드로 견줍니다
short_row = four_modes(short, reference, evaluators)
print("검색만:", short_row)
# 모드에 따라 갈린 두 값을 assert로 확인합니다
assert short_row["subset"]
assert not short_row["superset"]'''

EXTRA = r'''# 검색·출처 확인 뒤에, 묻지 않은 도서 예약까지 요청한 궤적을 만듭니다(답은 기준과 같은 글)
reserve_call = {
    "name": "reserve_book",
    "args": {"book_id": "B-102"},
    "id": "call_3",
    "type": "tool_call",
}
extra_calls = [reference_calls[0], reference_calls[1], reserve_call]
extra = make_trajectory(question, extra_calls, tool_results, reference_answer)
print("도구 차례:", called_tool_names(extra))'''

EXTRA_EVAL = r'''# 예약을 더한 궤적을 네 모드로 견줍니다
extra_row = four_modes(extra, reference, evaluators)
print("예약을 더함:", extra_row)
# 검색만 한 궤적과 반대로 갈린 두 값을 assert로 확인합니다
assert not extra_row["subset"]
assert extra_row["superset"]'''

WASTEFUL = r'''# 01절처럼 같은 검색어로 검색을 세 번 한 뒤 출처를 확인하는 궤적을 만듭니다(답은 기준과 같은 글)
wasteful_calls = [
    {"name": "search_documents", "args": search_args, "id": "call_1", "type": "tool_call"},
    {"name": "search_documents", "args": search_args, "id": "call_2", "type": "tool_call"},
    {"name": "search_documents", "args": search_args, "id": "call_3", "type": "tool_call"},
    {"name": "check_source", "args": source_args, "id": "call_4", "type": "tool_call"},
]
wasteful = make_trajectory(question, wasteful_calls, tool_results, reference_answer)
wasteful_names = called_tool_names(wasteful)
print("도구 차례:", wasteful_names)'''

WASTEFUL_EVAL = r'''# 검색 세 번 궤적을 네 모드로 견줍니다
wasteful_row = four_modes(wasteful, reference, evaluators)
print("검색 세 번:", wasteful_row)
# 도구 이름은 모두 기준에 있는데도 갈린 두 값을 assert로 확인합니다
assert not wasteful_row["subset"]
assert wasteful_row["superset"]'''

NAMES_IN = r'''# 검색 세 번 궤적의 도구 이름이 기준 도구 차례에 있는 이름인지만 하나씩 봅니다(횟수는 세지 않음)
for name in wasteful_names:
    print(name, "| 기준에 있는 이름인가:", name in reference_names)
# 목록의 count는 괄호 안의 값이 목록에 몇 번 들어 있는지 세어 내놓습니다
actual_count = wasteful_names.count("search_documents")
reference_count = reference_names.count("search_documents")
print("검색 요청 수 | 실제:", actual_count, "| 기준:", reference_count)'''

DEF_UNPAIRED = r'''# 이름 목록 names의 이름마다 상대 목록의 같은 이름 하나와 짝을 짓고, 짝이 없는 이름을 모아 내놓습니다
def unpaired_names(names, other_names):
    # 상대 목록을 복사해 두고, 짝을 지은 이름은 복사본에서 하나씩 지웁니다
    remaining = other_names.copy()
    unpaired = []
    for name in names:
        if name in remaining:
            remaining.remove(name)
        else:
            unpaired.append(name)
    return unpaired'''

UNPAIRED_WASTE = r'''# 검색 세 번 궤적과 기준 궤적의 도구 이름을 두 방향으로 짝지어 봅니다
print("기준과 짝이 없는 실제 요청:", unpaired_names(wasteful_names, reference_names))
print("실제와 짝이 없는 기준 요청:", unpaired_names(reference_names, wasteful_names))'''

TABLE = r'''# 견줄 궤적 다섯을 이름과 함께 모으고, 궤적마다 네 모드의 점수를 한 줄씩 출력합니다
trajectories = {
    "차례 바꿈": reversed_order,
    "한 응답에 요청 둘": two_in_one,
    "검색만": short,
    "예약을 더함": extra,
    "검색 세 번": wasteful,
}
print("궤적 | strict | unordered | subset | superset")
for name in trajectories:
    row = four_modes(trajectories[name], reference, evaluators)
    print(name, "|", row["strict"], "|", row["unordered"], "|", row["subset"], "|", row["superset"])'''

UNPAIRED_TABLE = r'''# 궤적마다 두 방향으로 짝이 없는 도구 이름을 출력합니다(이름만 보고 짝을 지음)
print("궤적 | 기준과 짝이 없는 실제 요청 | 실제와 짝이 없는 기준 요청")
for name in trajectories:
    names = called_tool_names(trajectories[name])
    print(name, "|", unpaired_names(names, reference_names), "|", unpaired_names(reference_names, names))'''

ARG_BUILD = r'''# 검색 요청의 인자만 기준과 다른 궤적 셋을 만듭니다(출처 확인 요청과 답 글은 기준과 같음)
arg_variants = {
    "검색어가 다름": {"query": "책 빌리는 기간"},
    "인자를 더함": {"query": "도서 대출 기간", "top_k": 3},
    "인자가 빠짐": {},
}
arg_trajectories = {}
for name in arg_variants:
    # 기준 검색 요청을 딕셔너리 메서드 copy()로 복사하고, 칸 args만 바꿉니다
    search_call = reference_calls[0].copy()
    search_call["args"] = arg_variants[name]
    calls = [search_call, reference_calls[1]]
    arg_trajectories[name] = make_trajectory(question, calls, tool_results, reference_answer)
print("인자만 다른 궤적:", list(arg_trajectories))'''

ARG_DEFAULT = r'''# 인자만 다른 궤적 셋을 네 모드로 견줍니다(인자 비교 방식은 기본값 exact)
for name in arg_trajectories:
    row = four_modes(arg_trajectories[name], reference, evaluators)
    print(name, "|", row)'''

VALUE_CHANGE = r'''# 값 바꿔 보기: 인자 비교 방식 하나만 exact에서 ignore로 바꾼 strict 평가 함수를 만듭니다
strict_ignore = create_trajectory_match_evaluator(
    trajectory_match_mode="strict",
    tool_args_match_mode="ignore",
)
other_query = arg_trajectories["검색어가 다름"]
exact_score = trajectory_pass(other_query, reference, evaluators["strict"])
ignore_score = trajectory_pass(other_query, reference, strict_ignore)
print("검색어가 다름 | exact:", exact_score, "| ignore:", ignore_score)
# 인자 비교 방식에 따라 갈린 두 값을 assert로 확인합니다
assert not exact_score
assert ignore_score'''

ARG_MODES = r'''# 인자 비교 방식 넷으로 strict 평가 함수를 하나씩 만들어, 인자만 다른 궤적 셋을 견줍니다
print("인자 비교 방식 | 검색어가 다름 | 인자를 더함 | 인자가 빠짐")
for arg_mode in ["exact", "ignore", "subset", "superset"]:
    evaluator = create_trajectory_match_evaluator(
        trajectory_match_mode="strict",
        tool_args_match_mode=arg_mode,
    )
    scores = []
    for name in arg_trajectories:
        scores.append(trajectory_pass(arg_trajectories[name], reference, evaluator))
    print(arg_mode, "|", scores[0], "|", scores[1], "|", scores[2])'''

OVERRIDE = r'''# 도구별 덮어쓰기: 검색 도구의 인자만 보지 않는 strict 평가 함수를 만듭니다
search_ignored = create_trajectory_match_evaluator(
    trajectory_match_mode="strict",
    tool_args_match_overrides={"search_documents": "ignore"},
)
# 출처 확인의 문서 ID만 기준과 다른 궤적도 만듭니다(기준 요청을 copy()로 복사해 칸 args만 바꾸고, 도구 결과 글은 그대로 둠)
other_source_call = reference_calls[1].copy()
other_source_call["args"] = {"doc_id": "LIB-002"}
source_calls = [reference_calls[0], other_source_call]
other_source = make_trajectory(question, source_calls, tool_results, reference_answer)
print("검색어가 다름:", trajectory_pass(other_query, reference, search_ignored))
print("출처 문서가 다름:", trajectory_pass(other_source, reference, search_ignored))'''


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/02-figures.md)
FIG1 = "02-1-네-모드가-보는-것"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 둘은 기준 궤적의 도구 요청 search_documents와 check_source, 그리고 실제 궤적의 도구 요청입니다. 두 상자에서 아래 칸 둘로 화살표가 갑니다. 왼쪽 칸 메시지를 하나씩 견줌에는 파란 상자 strict, 메시지 수와 차례, 도구 요청이 모두 같아야 참이 있습니다. 오른쪽 칸 도구 요청만 모아 짝지음에는 파란 상자 셋이 위아래로 놓입니다. unordered 두 쪽 요청이 모두 짝을 찾으면 참, subset 실제 요청이 모두 짝을 찾으면 참, superset 기준 요청이 모두 짝을 찾으면 참인 그림"
FIG1_CAP = "모드 strict는 메시지를 하나씩 견주고, 나머지 셋은 도구 요청만 모아 어느 쪽이 모두 짝을 찾는지 봅니다."
FIG1_READ = """위에서 아래로 읽습니다.
맨 위 초록 상자 둘은 노트북 2절의 기준 궤적과, 3~5절에서 코드로 적은 실제 궤적의 도구 요청입니다.
아래 칸 둘의 파란 상자 넷은 2절에서 모드마다 만든 평가 함수이고, 상자 안 글은 참이 되는 조건입니다.
짝을 짓는 칸의 세 상자는 서로 다른 모드라 화살표 없이 위아래로 두었습니다."""

FIG2 = "02-2-검색-세-번의-짝짓기"
FIG2_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 둘은 기준 요청 둘 search_documents와 check_source, 그리고 실제 요청 넷 search_documents 셋과 check_source 하나입니다. 두 상자에서 파란 상자 unpaired_names 두 방향으로 이름 짝짓기로 화살표가 모입니다. 파란 상자에서 노란 상자 둘로 화살표가 갈라집니다. 기준과 짝이 없는 실제 요청 search_documents 둘, 실제와 짝이 없는 기준 요청 빈 목록입니다. 두 노란 상자 아래에는 점선으로 노란 상자 모드 subset False와 모드 superset True가 하나씩 이어진 그림"
FIG2_CAP = "검색 세 번 궤적은 실제 검색 요청 둘이 짝 없이 남아, 모드 subset은 거짓, 모드 superset은 참이었습니다."
FIG2_READ = """위에서 아래로 읽습니다.
맨 위 초록 상자 둘은 노트북 2절 기준 궤적과 5절 검색 세 번 궤적의 도구 요청입니다.
파란 상자는 5절에서 정의한 함수이고, 노란 상자 넷은 5절 셀 출력입니다.
점선은 짝 없는 이름이 남은 쪽과, 그쪽을 보는 모드의 판정을 짝지은 것입니다."""

FIG3 = "02-3-궤적-다섯의-네-모드"
FIG3_ALT = "위에서 아래로 읽는 그림입니다. 맨 위 회색 상자 기준 궤적과 모드 넷의 평가 함수, 다섯 궤적 모두 같은 것과 견줌에서 아래 칸 셋으로 화살표가 갑니다. 왼쪽 칸 모드 strict만 거짓에는 노란 상자 차례 바꿈과 한 응답에 요청 둘이 위아래로 놓이고, 둘 다 strict False, unordered True, subset True, superset True입니다. 가운데 칸 모드 subset만 참에는 노란 상자 검색만, strict False, unordered False, subset True, superset False가 있습니다. 오른쪽 칸 모드 superset만 참에는 노란 상자 예약을 더함과 검색 세 번이 위아래로 놓이고, 둘 다 strict False, unordered False, subset False, superset True인 그림"
FIG3_CAP = "다섯 궤적 모두 모드 strict는 거짓이었고, 검색만은 모드 subset만, 예약을 더함과 검색 세 번은 모드 superset만 참이었습니다."
FIG3_READ = """맨 위 회색 상자에서 아래 칸 셋으로 읽습니다.
회색 상자는 다섯 궤적 모두에 같이 쓴 기준 궤적과 평가 함수입니다.
노란 상자 다섯은 노트북 6절 첫 셀의 출력 다섯 줄이고, 판정이 같은 궤적끼리 한 칸에 모았습니다.
칸 제목은 그 칸 궤적들의 판정을 줄인 말입니다.
같은 칸의 두 상자는 서로 다른 궤적이라 화살표 없이 위아래로 두었습니다."""

FIG4 = "02-4-인자-비교-방식-바꿔-보기"
FIG4_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 검색어가 다른 궤적, 검색어 책 빌리는 기간, 나머지는 기준과 같음에서 아래 칸 둘로 화살표가 갑니다. 기본값 그대로 칸에는 회색 상자 인자 비교 방식 exact에서 노란 상자 모드 strict False로 화살표가 갑니다. 값 하나만 바꿈 칸에는 파란 상자 인자 비교 방식 ignore에서 노란 상자 모드 strict True로 화살표가 가는 그림"
FIG4_CAP = "인자 비교 방식 하나만 exact에서 ignore로 바꾸자, 검색어가 다른 궤적의 모드 strict 판정이 거짓에서 참이 되었습니다."
FIG4_READ = """위에서 아래로 읽습니다.
맨 위 초록 상자는 노트북 7절 첫 셀에서 만든 궤적 셋 가운데 하나입니다.
아래 칸 둘은 같은 궤적을 서로 다른 설정으로 견준 것이고, 파란 상자가 바꾼 값입니다.
노란 상자 둘은 7절 셋째 셀의 출력입니다."""

ILLU = "02-5-기준-띠에-대-보기"
ILLU_ALT = "흰 바탕에 긴 종이띠 다섯 개가 위아래로 고르게 놓여 있고, 왼쪽 끝이 모두 맞춰져 있습니다. 맨 위 띠만 연한 파란색이고 아래 넷은 크림색입니다. 맨 위 띠와 둘째 띠에는 왼쪽부터 둥근 구멍 하나와 네모 구멍 하나가 같은 자리에 뚫려 있습니다. 셋째 띠는 네모 구멍이 먼저, 둥근 구멍이 뒤에 있습니다. 넷째 띠에는 둥근 구멍 하나만 있고, 다섯째 띠에는 둥근 구멍, 네모 구멍, 세모 구멍이 차례로 있습니다. 사람·글자·숫자·음표·화살표는 없는 그림"
ILLU_CAP = "맨 위 기준 띠에 아래 띠 넷을 대 보면, 같은 차례·뒤바뀐 차례·빠진 구멍·더한 구멍이 보입니다."
ILLU_READ = "흰 바탕에 종이띠 다섯이 위아래로 놓였고, 맨 위 연한 파란 띠가 기준 궤적입니다. 둥근 구멍은 검색, 네모 구멍은 출처 확인, 세모 구멍은 예약 요청이고, 왼쪽부터 읽는 구멍 차례가 도구 차례입니다. 둘째 띠는 기준과 같고, 셋째 띠는 차례가 뒤바뀌어 네 모드 가운데 모드 strict만 맞지 않다고 봅니다. 넷째 띠는 네모 구멍이 빠져 모드 subset만, 다섯째 띠는 세모 구멍이 더 있어 모드 superset만 맞다고 봅니다. 띠 오른쪽의 빈 부분과 띠 끝의 길이 차이는 어떤 값과도 짝짓지 않습니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 01절의 기준 궤적을 다시 만들고, 궤적 맞춰 보기 모드 넷으로 평가 함수를 하나씩 만듭니다.
2. 차례를 바꾼 궤적, 요청이 빠지거나 더해진 궤적, 검색을 세 번 한 궤적을 네 모드로 견줍니다.
3. 인자만 다른 궤적으로 인자 비교 방식 하나만 바꿔 보고, 도구별 덮어쓰기도 봅니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
예상 비용도 0달러입니다.
궤적은 모두 코드로 적은 메시지 목록이라, 다시 실행해도 같은 값이 나와야 합니다.

읽는 파일은 같은 폴더의 도구 파일 `eval_tools.py` 하나이고, 쓰는 파일은 없습니다.
걸린 시간은 재지 않았습니다.

**기준 버전** — 첫 셀에서 패키지 둘을 설치합니다.
판은 agentevals 0.0.9와 langchain 1.4.0입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~4절을 읽습니다.
네 모드를 만들고, 차례와 빠진 요청·더한 요청을 모드마다 어떻게 보는지 다루는 자리입니다.
5~7절은 짝짓기와 인자 비교를 궤적을 바꿔 가며 견주는 실습이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch29-agent-evaluation`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

01절에서는 궤적 맞춰 보기의 모드 `strict` 하나로 궤적을 평가했습니다.
이 절은 모드 셋을 더 보고, 네 모드가 같은 궤적을 어떻게 달리 판정하는지 견줍니다.
뜻과 구성은 본문 「핵심 개념」에서 풉니다.

첫 셀은 패키지 둘을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `agentevals: 0.0.9`와 `langchain: 1.4.0`이 보입니다.
둘 다 실습 폴더 잠금과 같은 판이고, 01절과 같은 패키지입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
함수 `create_trajectory_match_evaluator`는 01절에서 본 것처럼 모드 이름을 받아 평가 함수를 만들어 내놓습니다.
메시지 클래스 셋은 3절에서 궤적 하나를 손으로 만들 때 씁니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: called_tool_names, make_trajectory, trajectory_pass`가 보입니다.
앞에서 배운 함수는 `eval_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.

노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다.

세 함수는 01절 노트북에서 처음 적은 함수이고, 이 절부터 도구 파일에서 가져옵니다.
도구 파일에는 01절 셀의 주석과 본문을 글자 그대로 옮겼고, 인자도 01절과 같습니다.
함수 `make_trajectory(question, calls, results, answer)`는 질문·도구 요청 목록·결과 글·답 글로 궤적을 만듭니다.
함수 `called_tool_names(messages)`는 도구 차례를, `trajectory_pass(messages, reference, evaluator)`는 칸 `score`를 내놓습니다.

## 2. 기준 궤적과 네 모드의 평가 함수

01절에서 본 것처럼, 이 챕터는 에이전트가 질문에서 최종 답까지 밟은 단계의 차례를 궤적이라고 부릅니다.
이 절도 에이전트를 실행하지 않고, 질문에서 답까지의 메시지 목록을 코드로 적어 궤적으로 씁니다.
다음 셀은 01절과 같은 질문·기준 답·결과 글을 정합니다.
4절에서 쓸 예약 도구 `reserve_book`의 결과 글도 하나 더합니다.
도구 셋의 함수는 만들지 않고, 결과 글만 정해 둡니다."""),
        code(DATA),
        md("""**결과 읽기** — 출력 줄 `기준 답: 일반 도서는 14일 동안 빌릴 수 있습니다.`가 보입니다.
라벨 `결과 글을 정한 도구:` 뒤에는 `'search_documents'`·`'check_source'`·`'reserve_book'`이 있습니다.

도구 `reserve_book`은 도서를 예약하는 도구로, Ch 19 06절에서 본 쓰기 도구에 해당합니다.
질문은 대출 기간만 물었으므로, 예약은 누구도 부탁하지 않은 일입니다.

다음 셀은 01절과 같은 도구 요청 둘로 기준 궤적을 만듭니다.
기준 궤적은 문서를 한 번 검색하고, 찾은 문서가 있는지 한 번 확인한 뒤 답하는 차례입니다."""),
        code(REFERENCE),
        md("""**결과 읽기** — 출력 줄 `기준 궤적의 도구 차례: ['search_documents', 'check_source']`와 `메시지 수: 6`이 보입니다.
01절의 기준 궤적과 같은 요청이고, 메시지 수도 같습니다.
목록 `reference_names`는 5절에서 다른 궤적의 도구 이름과 견줄 때 다시 씁니다.

다음 셀은 모드 넷마다 평가 함수를 하나씩 만듭니다.
모드 이름 넷을 목록에 담고, 반복문으로 인자 `trajectory_match_mode`에 하나씩 넣습니다.
만든 평가 함수는 모드 이름을 키로 한 딕셔너리에 모읍니다."""),
        code(MAKE_MODES),
        md("""**결과 읽기** — 출력 줄 `평가 함수를 만든 모드: ['strict', 'unordered', 'subset', 'superset']`이 보입니다.
딕셔너리 `evaluators`에서 모드 이름으로 평가 함수를 꺼내 씁니다.
예를 들어 `evaluators["subset"]`은 모드 `subset`으로 만든 평가 함수입니다.

다음 셀은 기준 궤적을 자기 자신과 견줘, 모드마다 결과 딕셔너리의 칸 둘을 봅니다.
칸 `key`는 결과의 이름이고, 칸 `score`는 판정입니다."""),
        code(SELF_CHECK),
        md("""**결과 읽기** — 네 줄 모두 칸 `score`가 `True`입니다.
줄 `unordered | trajectory_unordered_match | True`처럼, 칸 `key`에는 모드 이름이 들어갑니다.
같은 궤적끼리는 네 모드 모두 참이라, 자기 자신과 견준 판정으로는 모드를 가를 수 없습니다.

모드 넷은 기준 궤적과 무엇이 같아야 참인지가 다릅니다.
모드 `strict`는 01절에서 본 것처럼 메시지를 하나씩 견줍니다.
나머지 셋은 궤적 전체에서 도구 요청만 모아, 기준 궤적의 도구 요청과 하나씩 짝을 짓습니다.
이름이 같고 인자가 맞는 요청끼리 짝이 되며, 이렇게 짝을 짓는 일을 짝짓기라고 부르겠습니다.
어느 쪽 요청이 모두 짝을 찾아야 하는지가 모드마다 다르고, 3~5절에서 하나씩 봅니다.

다음 셀은 한 궤적을 네 모드로 한꺼번에 견주는 함수를 정의합니다.
평가 함수마다 01절 함수 `trajectory_pass`로 칸 `score`만 꺼내, 모드 이름을 키로 모읍니다."""),
        code(DEF_FOUR),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
내놓는 딕셔너리는 키가 모드 이름 넷이고, 값은 참·거짓 값입니다.

## 3. 차례를 바꾼 궤적: 모드 strict와 unordered

먼저 볼 모드는 `unordered`입니다.
모드 `unordered`는 기준 요청과 실제 요청이 모두 서로 짝을 찾으면 참을 냅니다.
짝을 지을 때 차례는 보지 않습니다.

다음 셀은 01절의 차례 바꿈과 같은 궤적을 만듭니다.
출처 확인을 먼저 하고 검색을 뒤에 하며, 답은 기준과 같은 글입니다."""),
        code(REVERSED),
        md("""**결과 읽기** — 출력 줄 `도구 차례: ['check_source', 'search_documents']`가 보입니다.
도구 둘은 기준 궤적과 같고, 차례만 거꾸로입니다.

다음 셀은 이 궤적을 네 모드로 견줍니다.
실행 전에 예상해 봅니다.
차례를 보는 모드와 보지 않는 모드의 판정이 갈릴까요?
마지막 두 줄의 `assert`는 모드에 따라 갈린 값이 다시 실행해도 같은지 확인합니다."""),
        code(REVERSED_EVAL),
        md("""**결과 읽기** — 출력 줄 `차례 바꿈: {'strict': False, 'unordered': True, 'subset': True, 'superset': True}`가 보입니다.
모드 `strict`만 거짓이고, 나머지 셋은 참입니다.
두 줄의 `assert`도 오류 없이 지나갔습니다.

모드 `strict`는 메시지를 하나씩 견주므로, 첫 모델 응답의 도구 요청부터 기준과 달랐습니다.
나머지 셋은 도구 요청을 모아 짝을 지었고, 기준 요청 둘과 실제 요청 둘이 모두 짝을 찾았습니다.
검색과 출처 확인의 차례가 상관없는 일이라면, 모드 `unordered`로 맞춰 볼 수 있습니다.

다음 셀은 모델 응답 하나가 검색과 출처 확인을 함께 요청한 궤적을 손으로 만듭니다.
Ch 19 05절에서 본 것처럼, 모델은 한 응답에 도구 호출 요청을 여럿 담을 수 있습니다.
Ch 20 01절처럼 모델 없이, `AIMessage`의 인자 `tool_calls`에 요청 둘을 함께 넣습니다."""),
        code(TWO_IN_ONE),
        md("""**결과 읽기** — 출력 줄 `도구 차례: ['search_documents', 'check_source'] | 메시지 수: 5`가 보입니다.
도구 차례는 기준 궤적과 같지만, 메시지는 기준보다 하나 적은 다섯 개입니다.
요청 둘을 한 응답에 담아, 모델 응답이 하나 줄었기 때문입니다.

다음 셀은 이 궤적을 네 모드로 견줍니다."""),
        code(TWO_EVAL),
        md("""**결과 읽기** — 출력 줄 `한 응답에 요청 둘: {'strict': False, 'unordered': True, 'subset': True, 'superset': True}`가 보입니다.
도구 차례가 기준과 같은데도 모드 `strict`는 거짓을 냈습니다.

모드 `strict`는 메시지 수부터 견주고, 이 궤적은 메시지가 다섯이라 기준의 여섯과 다릅니다.
나머지 셋은 메시지가 몇 개인지 보지 않고, 궤적 전체에서 모은 도구 요청만 짝지었습니다.
설치판 agentevals 0.0.9 소스 `trajectory/strict.py` 34행이 메시지 수를 먼저 견주는 줄입니다.
LangChain 문서 표는 모드 `unordered`도 메시지 구조가 같아야 한다고 적지만, 설치판 출력은 참이었습니다.

## 4. 빠진 요청과 더한 요청: 모드 subset과 superset

모드 `subset`은 실제 요청이 모두 기준 요청과 짝을 찾으면 참을 냅니다.
기준 요청이 남는 것, 곧 기준에 있는 요청을 빠뜨린 것은 봐줍니다.
모드 `superset`은 반대로 기준 요청이 모두 실제 요청과 짝을 찾으면 참을 냅니다.
실제 요청이 남는 것, 곧 기준에 없는 요청을 더한 것은 봐줍니다.

다음 셀은 검색만 하고 출처 확인은 하지 않은 궤적을 만듭니다."""),
        code(SHORT),
        md("""**결과 읽기** — 출력 줄 `도구 차례: ['search_documents']`가 보입니다.
기준 요청 둘 가운데 출처 확인이 빠졌습니다.

다음 셀은 이 궤적을 네 모드로 견줍니다.
실행 전에 예상해 봅니다.
빠진 요청을 봐주는 모드는 어느 쪽일까요?"""),
        code(SHORT_EVAL),
        md("""**결과 읽기** — 출력 줄 `검색만: {'strict': False, 'unordered': False, 'subset': True, 'superset': False}`가 보입니다.
네 모드 가운데 모드 `subset`만 참입니다.

실제의 검색 요청은 기준 요청과 짝을 찾았고, 기준의 출처 확인 요청은 짝 없이 남았습니다.
모드 `subset`은 실제 요청만 모두 짝을 찾으면 되므로 참입니다.
모드 `superset`과 `unordered`는 기준 요청이 모두 짝을 찾아야 해서 거짓입니다.
그래서 모드 `subset`이 참이어도, 필요한 도구를 다 불렀다는 뜻은 아닙니다.

다음 셀은 반대로, 기준 요청 둘 뒤에 도서 예약 요청을 하나 더한 궤적을 만듭니다."""),
        code(EXTRA),
        md("""**결과 읽기** — 출력 줄 `도구 차례: ['search_documents', 'check_source', 'reserve_book']`가 보입니다.
기준 요청 둘 뒤에, 질문과 상관없는 예약 요청이 하나 붙었습니다.

다음 셀은 이 궤적을 네 모드로 견줍니다.
실행 전에 예상해 봅니다.
더한 요청을 봐주는 모드는 어느 쪽일까요?"""),
        code(EXTRA_EVAL),
        md("""**결과 읽기** — 출력 줄 `예약을 더함: {'strict': False, 'unordered': False, 'subset': False, 'superset': True}`가 보입니다.
이번에는 모드 `superset`만 참이고, 검색만 한 궤적과 반대입니다.

기준 요청 둘은 모두 짝을 찾았고, 실제의 예약 요청이 짝 없이 남았습니다.
모드 `superset`은 기준 요청만 모두 짝을 찾으면 되므로, 묻지 않은 예약을 한 궤적도 참으로 봤습니다.
예약처럼 무언가를 바꾸는 쓰기 도구를 막아야 한다면, 모드 `superset`만으로는 잡지 못합니다.
모드 `subset`은 이 예약 요청을 거짓으로 잡았습니다.

## 5. 짝짓기는 횟수까지 셉니다

다음 셀은 01절처럼 같은 검색어로 검색을 세 번 한 뒤 출처를 확인하는 궤적을 만듭니다.
도구 이름만 보면 두 가지 모두 기준에 있는 도구입니다."""),
        code(WASTEFUL),
        md("""**결과 읽기** — 라벨 `도구 차례:` 뒤에 `'search_documents'`가 셋, `'check_source'`가 하나 있습니다.
01절에서 궤적 평가만 거짓을 낸 검색 세 번 궤적과 같은 요청입니다.

다음 셀은 이 궤적을 네 모드로 견줍니다.
실행 전에 예상해 봅니다.
실제 요청의 이름이 모두 기준에 있으니, 모드 `subset`은 참이 될까요?"""),
        code(WASTEFUL_EVAL),
        md("""**결과 읽기** — 출력 줄 `검색 세 번: {'strict': False, 'unordered': False, 'subset': False, 'superset': True}`가 보입니다.
모드 `subset`도 거짓이고, 모드 `superset`만 참입니다.

도구 이름이 모두 기준에 있어도 모드 `subset`은 참을 내지 않았습니다.
다음 셀들에서 까닭을 이름과 횟수로 나눠 봅니다.
먼저 도구 이름이 기준에 있는지만 보고, 검색 요청이 몇 번인지 셉니다.
목록의 `count`는 괄호 안의 값이 목록에 몇 번 들어 있는지 세어 내놓습니다."""),
        code(NAMES_IN),
        md("""**결과 읽기** — 네 줄 모두 `기준에 있는 이름인가: True`입니다.
출력 줄 `검색 요청 수 | 실제: 3 | 기준: 1`로, 검색 요청은 기준보다 둘 많습니다.

이름만 보면 실제 요청이 모두 기준 도구 안에 있습니다.
그런데 짝짓기는 기준 요청 하나에 실제 요청 하나만 짝을 짓습니다.
설치판 `trajectory/utils.py` 90~134행을 보면, 한 번 짝을 지은 실제 요청은 다시 쓰지 않습니다.

다음 셀은 이 짝짓기를 도구 이름만으로 흉내 내는 함수를 정의합니다.
이름 목록 `names`의 이름마다 상대 목록에서 같은 이름을 하나 찾아 짝을 짓고, 짝을 찾지 못한 이름을 모읍니다.
짝을 지은 이름은 상대 목록의 복사본에서 `remove`로 하나씩 지워, 같은 이름과 두 번 짝을 짓지 않게 합니다.
복사본은 Ch 2 03절에서 배운 목록 메서드 `copy()`로 만듭니다.
라이브러리는 인자까지 견주지만, 이 함수는 이름만 봅니다."""),
        code(DEF_UNPAIRED),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
인자 차례를 바꿔 부르면 짝을 찾는 방향이 바뀝니다.
실제 이름을 앞에 넣으면 기준과 짝이 없는 실제 요청이, 기준 이름을 앞에 넣으면 실제와 짝이 없는 기준 요청이 나옵니다.

다음 셀은 검색 세 번 궤적을 두 방향으로 짝지어 봅니다."""),
        code(UNPAIRED_WASTE),
        md("""**결과 읽기** — 출력 줄 `기준과 짝이 없는 실제 요청: ['search_documents', 'search_documents']`가 보입니다.
출력 줄 `실제와 짝이 없는 기준 요청: []`는 빈 목록입니다.

기준의 검색 요청 하나가 실제 검색 요청 하나와 짝을 지었고, 남은 실제 검색 요청 둘은 짝이 없습니다.
모드 `subset`은 실제 요청이 모두 짝을 찾아야 참이라 거짓이었습니다.
모드 `superset`은 기준 요청이 모두 짝을 찾았으므로 참이었습니다.
그래서 「기준 도구 안에 있으면 참」이 아니라, 요청 하나하나가 짝을 찾아야 참입니다.

## 6. 네 모드 판정 표

다음 셀은 3~5절의 궤적 다섯을 모아, 네 모드의 점수를 한 표로 출력합니다.
실행 전에 앞 셀들의 결과로 표를 예상해 봅니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 `궤적 | strict | unordered | subset | superset` 아래 다섯 줄이 궤적마다 네 모드의 점수입니다.
줄 `차례 바꿈 | False | True | True | True`와 `한 응답에 요청 둘 | False | True | True | True`는 모드 `strict`만 거짓입니다.
줄 `검색만 | False | False | True | False`는 모드 `subset`만 참입니다.
줄 `예약을 더함 | False | False | False | True`와 `검색 세 번 | False | False | False | True`는 모드 `superset`만 참입니다.

다섯 궤적 모두 모드 `strict`는 거짓이었습니다.
모드 `unordered`가 참인 궤적은 도구 요청이 기준과 모두 짝이 맞는 둘뿐입니다.
모드 `subset`과 `superset`은 빠진 요청과 더한 요청을 서로 반대로 봤습니다.

다음 셀은 같은 궤적 다섯을 5절의 함수 `unpaired_names`로 두 방향 짝지어 봅니다.
실행 전에 예상해 봅니다.
짝이 없는 이름이 어느 쪽에 남는지가 위 표의 참·거짓과 맞을까요?"""),
        code(UNPAIRED_TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 다섯 줄에서, 줄 `검색만 | [] | ['check_source']`는 기준 쪽에만 짝이 없는 이름이 남았습니다.
줄 `예약을 더함 | ['reserve_book'] | []`와 `검색 세 번 | ['search_documents', 'search_documents'] | []`는 실제 쪽에만 남았습니다.
줄 `차례 바꿈 | [] | []`와 `한 응답에 요청 둘 | [] | []`는 두 쪽 모두 빈 목록입니다.

위 표와 견주면 규칙이 보입니다.
실제 쪽 목록이 비면 모드 `subset`이, 기준 쪽 목록이 비면 모드 `superset`이 참이었습니다.
두 목록이 모두 비면 모드 `unordered`가 참이었고, 모드 `strict`는 여기에 더해 메시지를 하나씩 견줬습니다.
이 함수는 이름만 보므로, 인자가 다른 요청은 7절에서 라이브러리로 봅니다.

## 7. 값 바꿔 보기: 인자 비교 방식

지금까지 궤적은 모두 인자가 기준과 같은 요청만 썼습니다.
짝을 지을 때 인자를 어떻게 견줄지는 인자 `tool_args_match_mode`로 정하고, 이 챕터는 이를 인자 비교 방식이라고 부릅니다.
기본값은 `exact`이고, 두 요청의 인자 딕셔너리가 똑같아야 짝이 됩니다.

다음 셀은 검색 요청의 인자만 기준과 다른 궤적 셋을 만듭니다.
검색어를 다르게 쓴 궤적, 인자 `top_k`를 하나 더한 궤적, 인자를 모두 뺀 궤적입니다.
출처 확인 요청과 답 글은 기준과 같습니다.
검색 요청은 기준 검색 요청을 딕셔너리 메서드 `copy()`로 복사한 뒤, 칸 `args`만 바꿔 만듭니다.
딕셔너리 `copy()`는 Ch 18 05절에서 설정 딕셔너리를 복사할 때 쓴 메서드입니다."""),
        code(ARG_BUILD),
        md("""**결과 읽기** — 출력 줄 `인자만 다른 궤적: ['검색어가 다름', '인자를 더함', '인자가 빠짐']`이 보입니다.
세 궤적 모두 검색 요청의 인자만 기준과 다릅니다.

검색어 「책 빌리는 기간」은 기준의 「도서 대출 기간」과 뜻이 비슷한 다른 글입니다.
인자 `top_k`는 검색 결과를 몇 개 받을지 적는 자리로 넣은 교재용 인자입니다.

다음 셀은 이 세 궤적을 지금까지 쓴 네 모드로 견줍니다.
인자 비교 방식은 기본값 `exact` 그대로입니다."""),
        code(ARG_DEFAULT),
        md("""**결과 읽기** — 줄 `검색어가 다름 | {'strict': False, 'unordered': False, 'subset': False, 'superset': False}`처럼 세 줄 모두 네 모드가 거짓입니다.
도구 차례는 기준과 같은데도 판정은 모두 거짓이었습니다.

기본값 `exact`에서는 인자가 조금만 달라도 검색 요청끼리 짝이 되지 않습니다.
검색 요청이 기준과 맞지 않아, 네 모드 모두 거짓이 되었습니다.

이제 값 하나만 바꿔 봅니다.
바꿀 값은 인자 비교 방식이고, 기본값 `exact`를 `ignore`로 바꿔 모드 `strict`의 평가 함수를 새로 만듭니다.
궤적과 모드는 그대로 둡니다.
실행 전에 예상해 봅니다.
검색어만 다른 궤적은 참이 될까요?"""),
        code(VALUE_CHANGE),
        md("""**결과 읽기** — 출력 줄 `검색어가 다름 | exact: False | ignore: True`가 보입니다.
인자 비교 방식 하나만 바꾸자, 같은 궤적의 판정이 거짓에서 참으로 바뀌었습니다.
두 줄의 `assert`도 오류 없이 지나갔습니다.

값 `ignore`는 이름이 같은 도구 요청이면 인자를 보지 않고 짝을 짓습니다.
검색어를 어떻게 쓰든 괜찮은 평가라면 이 값을 쓸 수 있지만, 검색어가 틀린 요청도 함께 통과합니다.
인자를 얼마나 느슨하게 볼지는 평가를 설계하는 사람이 정할 일입니다.

다음 셀은 인자 비교 방식 넷을 모두 써서, 인자만 다른 궤적 셋을 모드 `strict`로 견줍니다.
값 `subset`은 실제 인자가 모두 기준 인자에 있어야 짝이 됩니다.
값 `superset`은 기준 인자가 모두 실제 인자에 있어야 짝이 됩니다."""),
        code(ARG_MODES),
        md("""**결과 읽기** — 라벨 줄 아래 네 줄이 인자 비교 방식마다 세 궤적의 판정입니다.
줄 `exact | False | False | False`는 셋 모두 거짓이고, 줄 `ignore | True | True | True`는 셋 모두 참입니다.
줄 `subset | False | False | True`는 인자가 빠진 궤적만, 줄 `superset | False | True | False`는 인자를 더한 궤적만 참입니다.

인자를 모두 뺀 요청은 기준 인자 밖의 인자가 하나도 없어, 값 `subset`에서 짝이 되었습니다.
인자 `top_k`를 더한 요청은 기준 인자를 모두 담고 있어, 값 `superset`에서 짝이 되었습니다.
검색어가 다른 요청은 값 `ignore`에서만 짝이 되었습니다.

다음 셀은 도구별 덮어쓰기를 봅니다.
인자 `tool_args_match_overrides`에 도구 이름과 인자 비교 방식을 짝지은 딕셔너리를 주면, 그 도구만 그 방식으로 견줍니다.
검색 도구만 인자를 보지 않게 하고, 출처 확인의 문서 ID만 다른 궤적도 함께 봅니다.
그 궤적의 출처 확인 요청도 기준 요청을 `copy()`로 복사해 칸 `args`만 바꿉니다."""),
        code(OVERRIDE),
        md("""**결과 읽기** — 출력 줄 `검색어가 다름: True`와 `출처 문서가 다름: False`가 보입니다.
검색 요청의 인자는 보지 않았고, 출처 확인 요청의 인자는 기본값 `exact`로 견줬습니다.

도구별 덮어쓰기는 적어 둔 도구에만 다른 인자 비교 방식을 씁니다.
검색어는 자유롭게 쓰게 두고, 확인할 문서 ID는 글자까지 맞게 요구할 때 쓸 수 있습니다.
출처 확인의 도구 결과 글은 기준 그대로 두었지만, 01절에서 본 것처럼 모드 `strict`는 메시지 글을 견주지 않습니다.
설치판은 덮어쓰기 값으로 함수나 인자 이름 목록도 받지만, 이 절에서는 실행하지 않았습니다.

## 정리

1. 차례를 바꾼 궤적과 한 응답에 요청 둘인 궤적은 모드 `strict`만 거짓이었고, 나머지 셋은 참이었습니다.
2. 검색만 한 궤적은 모드 `subset`만, 예약을 더한 궤적과 검색 세 번 궤적은 모드 `superset`만 참이었습니다. 짝짓기는 요청 횟수까지 셉니다.
3. 인자만 다른 궤적은 네 모드 모두 거짓이었고, 인자 비교 방식을 `ignore`로 바꾸자 모드 `strict`도 참이 되었습니다.

03절에서는 코드 규칙 대신 평가 모델(judge)이 궤적을 읽고 판정합니다."""),
    ]


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
L_03 = author_01.L_03
L_CH17_04 = author_01.L_CH17_04
L_CH18_05 = author_01.L_CH18_05
L_CH19_04 = author_01.L_CH19_04
L_CH19_05 = "../../part5/ch19-model-tools/05-bind_tools와-병렬-호출.html"
L_CH19_06 = author_01.L_CH19_06
L_CH20_01 = author_01.L_CH20_01

TERM_ROWS = [
    ("모드 <code>unordered</code>", "궤적 전체의 도구 요청을 모아, 기준 요청과 실제 요청이 모두 짝을 찾으면 참을 내는 모드입니다. 차례는 보지 않지만, 요청의 수는 맞아야 합니다. 장보기 목록의 물건을 빠짐없이 같은 수만큼 샀는지만 보고, 어느 것부터 샀는지는 보지 않는 것과 같습니다. 이 절에서는 차례를 바꾼 궤적이 이 모드에서 참이었습니다."),
    ("모드 <code>subset</code>", "실제 궤적의 도구 요청이 모두 기준 요청과 짝을 찾으면 참을 내는 모드입니다. 기준에 없는 요청을 더하면 거짓이고, 기준 요청이 빠진 것은 봐줍니다. 장보기 목록에 없는 물건을 사지 않았는지만 보는 것과 같습니다. 이 절에서는 검색만 한 궤적이 이 모드에서만 참이었습니다."),
    ("모드 <code>superset</code>", "기준 궤적의 도구 요청이 모두 실제 요청과 짝을 찾으면 참을 내는 모드입니다. 기준 요청이 빠지면 거짓이고, 요청을 더한 것은 봐줍니다. 장보기 목록의 물건을 모두 샀는지만 보고, 더 산 물건은 따지지 않는 것과 같습니다. 이 절에서는 예약을 더한 궤적과 검색 세 번 궤적이 이 모드에서만 참이었습니다."),
    ("짝짓기", "기준 궤적과 실제 궤적의 도구 요청을 하나씩 짝지어 가는 일입니다. 이름이 같고 인자가 맞아야 짝이 되고, 한 번 짝이 된 요청은 다시 쓰지 않습니다. 목록의 우유 한 줄을 산 우유 하나와 짝지으면, 우유를 세 개 샀을 때 둘이 남는 것과 같습니다. 이 절의 함수 <code>unpaired_names</code>는 이름만으로 짝을 지어, 짝이 없는 요청을 보여 줍니다."),
    ("인자 비교 방식(<code>tool_args_match_mode</code>)", "짝을 지을 때 두 요청의 인자 딕셔너리를 어떻게 견줄지 정하는 인자입니다. 기본값 <code>exact</code>는 두 딕셔너리가 똑같아야 짝이 되고, 값 <code>ignore</code>는 인자를 보지 않습니다. 모드 <code>strict</code>·<code>superset</code>에서 값 <code>subset</code>은 실제 인자가 모두 기준 인자에, 값 <code>superset</code>은 기준 인자가 모두 실제 인자에 있어야 짝이 됩니다. 같은 주소인지 볼 때 도로명과 번지까지 볼지, 동네 이름만 볼지 정하는 것과 같습니다. 이 절에서는 검색어가 다른 궤적이 값 <code>ignore</code>에서만 참이었습니다."),
    ("도구별 덮어쓰기(<code>tool_args_match_overrides</code>)", "도구 이름마다 인자 비교 방식을 따로 정하는 인자입니다. 적어 둔 도구만 그 방식으로 견주고, 나머지 도구는 인자 비교 방식을 그대로 따릅니다. 같은 서류에서 이름 칸은 글자까지 보고, 메모 칸은 보지 않는 것과 같습니다. <a href=\"../../part4/ch13-langgraph-basics/02-State-갱신.html\">Ch 13 02절</a>에서 상태 값을 새 값으로 바꾸던 덮어쓰기와는 다른 말입니다. 이 절에서는 <code>{\"search_documents\": \"ignore\"}</code>로 검색 도구의 인자만 보지 않았습니다."),
]

F = "<code>False</code>"
T = "<code>True</code>"
MODE_ROWS = [
    ("차례 바꿈", "<code>check_source</code> → <code>search_documents</code>", F, T, T, T),
    ("한 응답에 요청 둘", "<code>search_documents</code>·<code>check_source</code>를 한 응답에", F, T, T, T),
    ("검색만", "<code>search_documents</code>", F, F, T, F),
    ("예약을 더함", "<code>search_documents</code> → <code>check_source</code> → <code>reserve_book</code>", F, F, F, T),
    ("검색 세 번", "<code>search_documents</code> 셋 → <code>check_source</code>", F, F, F, T),
]
ARG_ROWS = [
    ("<code>exact</code>(기본값)", F, F, F),
    ("<code>ignore</code>", T, T, T),
    ("<code>subset</code>", F, F, T),
    ("<code>superset</code>", F, T, F),
]

LOOK_B5 = "노트북 2절에서 <code>메시지 수: 6</code>과, 자기 자신과 견준 네 모드가 모두 <code>True</code>인 것을 봅니다. 3절에서 <code>차례 바꿈: {'strict': False, 'unordered': True, 'subset': True, 'superset': True}</code>와 <code>메시지 수: 5</code>를 찾습니다. 4절에서는 검색만 한 궤적과 예약을 더한 궤적의 <code>subset</code>·<code>superset</code> 값이 서로 반대인지 확인합니다. 5절에서 <code>검색 요청 수 | 실제: 3 | 기준: 1</code>과 짝이 없는 이름 목록을 봅니다."
LOOK_B6 = "노트북 6절 첫 셀에서 다섯 줄의 <code>True</code>·<code>False</code>를 확인합니다. 7절에서 <code>검색어가 다름 | exact: False | ignore: True</code>와, 인자 비교 방식 네 줄을 봅니다. 모델을 부르지 않으므로, 다시 실행해도 같은 값이 나와야 합니다."


def runs_paragraph() -> str:
    if not RUNS_SENTENCE:
        return ""
    return "<p>" + RUNS_SENTENCE + "</p>\n"


def src_html() -> str:
    terms = table_html(["말", "뜻"], TERM_ROWS)
    modes_table = table_html(["궤적", "도구 차례", "strict", "unordered", "subset", "superset"], MODE_ROWS)
    args_table = table_html(["인자 비교 방식", "검색어가 다름", "인자를 더함", "인자가 빠짐"], ARG_ROWS)
    return """<!--meta: 강의 0.75h | 실습 1.25h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 6 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>모드 <code>unordered</code>·<code>subset</code>·<code>superset</code>이 참이 되는 조건을 모드 <code>strict</code>와 견줘 말할 수 있습니다.</li>
<li>차례를 바꾼 궤적과 요청이 빠지거나 더해진 궤적을 네 모드가 어떻게 판정하는지 출력으로 설명할 수 있습니다.</li>
<li>짝짓기가 요청 횟수까지 센다는 것과, 인자 비교 방식에 따라 판정이 바뀐다는 것을 말할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_01 + """\">01절</a>에서는 궤적 맞춰 보기의 모드 <code>strict</code> 하나로 궤적을 평가했습니다. 모드 <code>strict</code>는 도구 차례가 조금만 달라도 거짓을 냅니다. 그런데 도구 둘의 차례가 상관없는 일도 있고, 기준에 없는 도구를 더 불렀는지만 막고 싶은 일도 있습니다. 이 절은 모드 셋을 더 보고, 네 모드가 차례와 빠진 요청·더한 요청을 어떻게 달리 보는지 견줍니다.</p><p>어느 모드가 맞는지는 평가로 무엇을 봐줄지에 달렸습니다. 이 절은 같은 기준 궤적에 여러 궤적을 대 보며, 모드마다 참이 되는 조건을 출력으로 확인합니다. 이 절도 모델을 부르지 않고 궤적을 코드로 적어, 같은 궤적에는 늘 같은 판정이 나옵니다. 끝으로 인자 비교 방식 하나만 바꿔, 인자를 얼마나 엄격하게 볼지도 정해 봅니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_01 + """\">01절</a>에서는 최종 답 평가·한 단계 평가·궤적 평가를 같은 기준 궤적과 견줬습니다. 궤적 평가에는 궤적 맞춰 보기의 모드 <code>strict</code>를 썼습니다. 모드 <code>strict</code>는 메시지의 수·역할·차례와 도구 요청의 이름·인자를 보고, 메시지 글은 견주지 않았습니다. 이 절은 01절의 기준 궤적을 다시 만들고, 01절에서 처음 적은 함수 셋을 도구 파일에서 가져옵니다.</p><p><a href=\"""" + L_CH17_04 + """\">Ch 17 04절</a>은 실행 기록의 단계를 일어난 차례대로 늘어놓은 것을 단계 차례(궤적)라고 불렀습니다. 그 절은 단계 차례를 맞춰 보며 평가하는 방법을 이 절에서 다룬다고 예고했습니다. 이 절의 네 모드가 그 방법이고, 차례를 볼지와 빠진 요청·더한 요청을 봐줄지가 모드마다 다릅니다.</p><p><a href=\"""" + L_CH19_04 + """\">Ch 19 04절</a>에서는 도구 호출 요청의 칸 넷(<code>name</code>·<code>args</code>·<code>id</code>·<code>type</code>)을 봤습니다. <a href=\"""" + L_CH19_05 + """\">05절</a>에서는 한 응답에 도구 호출 요청이 여럿 오는 경우를 봤습니다. <a href=\"""" + L_CH19_06 + """\">06절</a>에서는 무언가를 바꾸는 쓰기 도구를 읽기 도구와 나눴습니다. 이 절의 궤적에도 한 응답에 요청 둘인 궤적과, 묻지 않은 예약을 하는 쓰기 도구 요청이 나옵니다. 한 응답에 요청 둘인 궤적은 <a href=\"""" + L_CH20_01 + """\">Ch 20 01절</a>처럼 모델 없이 손으로 만듭니다.</p><p>목록을 복사하는 <code>copy()</code>는 <a href=\"../../part1/ch02-python/03-자료구조.html\">Ch 2 03절</a>에서 배웠습니다. <a href=\"""" + L_CH18_05 + """\">Ch 18 05절</a>은 같은 이름의 메서드로 딕셔너리를 복사했고, 이 절은 7절에서 도구 요청 딕셔너리를 복사합니다. 이 절은 목록 메서드 <code>count</code>와 <code>remove</code>를 새로 쓰고, 처음 쓰는 자리에서 한 문장씩 풉니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>오르골 종이띠에는 곡의 차례대로 구멍이 뚫려 있습니다. 악보대로 뚫은 기준 띠에 다른 띠를 대 보는 방법은 여럿입니다. 구멍의 모양과 자리가 모두 같아야 맞다고 볼 수 있습니다. 같은 모양의 구멍이 같은 수만큼 있으면, 자리는 따지지 않을 수도 있습니다. 기준 띠에 없는 구멍만 없으면 된다고 볼 수도 있고, 기준 띠의 구멍이 모두 있기만 하면 된다고 볼 수도 있습니다.</p><p>기준 띠가 기준 궤적이고, 구멍 하나가 도구 요청 하나이며, 구멍 모양이 도구 이름입니다. 네 방법이 차례대로 모드 <code>strict</code>·<code>unordered</code>·<code>subset</code>·<code>superset</code>입니다. 비유와 다른 점도 있습니다. 궤적 맞춰 보기는 도구 이름뿐 아니라 인자까지 보고, 모드 <code>strict</code>는 메시지가 몇 개인지도 봅니다. 또 이 절의 궤적은 에이전트가 만든 것이 아니라 코드로 적은 것입니다.</p>
""" + illustration_block() + """<h3>네 모드와 짝짓기</h3><p>모드 넷은 기준 궤적과 무엇이 같아야 참인지가 다릅니다. 모드 <code>strict</code>는 01절에서 본 것처럼 메시지를 하나씩 견주므로, 도구 요청이 든 메시지의 차례까지 같아야 참입니다. 나머지 셋은 메시지를 하나씩 견주지 않고, 궤적 전체에서 도구 요청만 모아 기준 궤적의 도구 요청과 짝을 짓습니다. 이름이 같고 인자가 맞는 요청끼리 하나씩 짝이 되며, 이 일을 짝짓기라고 부릅니다.</p><p>모드 <code>unordered</code>는 두 쪽 요청이 모두 짝을 찾아야 참입니다. 모드 <code>subset</code>은 실제 요청이 모두 짝을 찾아야 참이고, 짝 없는 기준 요청은 남아도 됩니다. 모드 <code>superset</code>은 기준 요청이 모두 짝을 찾아야 참이고, 짝 없는 실제 요청은 남아도 됩니다. 곧 모드 <code>subset</code>은 빠진 요청을, 모드 <code>superset</code>은 더한 요청을 봐줍니다.</p>
""" + terms + """
<p>새 말을 이 절 코드에서 보면 이렇습니다. 네 모드의 평가 함수는 딕셔너리 <code>evaluators</code>에 모드 이름을 키로 모였습니다. 함수 <code>four_modes</code>는 한 궤적을 네 평가 함수로 견줘 <code>{'strict': False, 'unordered': True, 'subset': True, 'superset': True}</code>처럼 내놓습니다. 짝이 없는 요청은 함수 <code>unpaired_names</code>로 보고, 인자 비교 방식과 도구별 덮어쓰기는 평가 함수를 만들 때 인자로 줍니다.</p>
<h3>짝짓기는 횟수까지 셉니다</h3><p>설치판 agentevals 0.0.9 <code>trajectory/utils.py</code> 90~134행을 보면, 기준 요청마다 아직 짝이 없는 실제 요청을 하나씩 찾습니다. 한 번 짝을 지은 실제 요청은 다시 쓰지 않습니다. 그래서 같은 도구를 여러 번 부르면, 이름이 기준에 있어도 짝 없는 요청이 남습니다. 모드 <code>unordered</code>는 이 짝짓기를 두 방향으로 모두 하고, 모드 <code>subset</code>은 방향을 바꿔 합니다.</p><p>짝을 지을 때 인자를 견주는 규칙은 인자 비교 방식으로 정합니다. 기본값 <code>exact</code>는 두 요청의 인자 딕셔너리가 똑같아야 짝이 됩니다. 값 <code>ignore</code>는 인자를 보지 않고, 값 <code>subset</code>·<code>superset</code>은 한쪽 인자가 다른 쪽 인자를 모두 담으면 짝이 됩니다. 도구마다 다른 규칙을 쓰려면 도구별 덮어쓰기를 줍니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 01절과 같은 기준 궤적을 만들고, 모드 넷으로 평가 함수를 하나씩 만듭니다. 3절은 차례를 바꾼 궤적과 한 응답에 요청 둘인 궤적을 견줍니다. 4절은 검색만 한 궤적과 예약을 더한 궤적을 견줍니다. 5절은 검색 세 번 궤적으로 짝짓기가 횟수까지 세는지 보고, 6절은 궤적 다섯의 판정을 한 표로 모읍니다. 7절은 인자만 다른 궤적으로 인자 비교 방식 하나만 바꿔 봅니다.</p><p>모델 요청은 0번이고, API 키 없이 실행합니다. 궤적은 모두 코드로 적은 메시지 목록이라, 다시 실행해도 같은 판정이 나옵니다. 읽는 파일은 도구 파일 <code>eval_tools.py</code> 하나이고 쓰는 파일은 없습니다. 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>같은 기준 궤적에 궤적 다섯을 대 보자, 모드마다 참이 된 궤적이 달랐습니다. 차례를 바꾼 궤적과 한 응답에 요청 둘인 궤적은 모드 <code>strict</code>만 거짓이었습니다. 검색만 한 궤적은 모드 <code>subset</code>만 참이었습니다. 예약을 더한 궤적과 검색 세 번 궤적은 모드 <code>superset</code>만 참이었습니다. 다섯 궤적 모두 모드 <code>strict</code>로는 거짓이었습니다.</p>
<p>아래 표는 노트북 3~6절 출력을 모은 것입니다.</p>
""" + modes_table + """
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>검색 세 번 궤적은 도구 이름이 모두 기준에 있는데도 모드 <code>subset</code>이 거짓이었습니다. 두 방향으로 짝지어 보니, 실제 검색 요청 둘이 짝 없이 남았습니다. 짝짓기는 요청의 이름만이 아니라 횟수까지 세기 때문입니다. 짝 없는 이름이 어느 쪽에 남는지는 다섯 궤적 모두에서 세 모드의 판정과 맞았습니다.</p><p>인자만 다른 궤적 셋은 기본값 <code>exact</code>에서 네 모드 모두 거짓이었습니다. 인자 비교 방식 하나만 <code>ignore</code>로 바꾸자, 검색어가 다른 궤적도 모드 <code>strict</code>에서 참이 되었습니다. 값 <code>subset</code>은 인자가 빠진 궤적만, 값 <code>superset</code>은 인자를 더한 궤적만 참이었습니다. 검색 도구만 덮어쓴 평가 함수는 검색어가 다른 궤적을 참으로, 출처 문서가 다른 궤적을 거짓으로 봤습니다.</p>
<p>아래 표는 노트북 7절에서 모드 <code>strict</code>로 견준 출력입니다.</p>
""" + args_table + """
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>어느 모드와 어느 인자 비교 방식이 맞는지는 평가로 무엇을 봐줄지에 달렸습니다. 차례가 상관없으면 모드 <code>unordered</code>를, 필요한 도구를 모두 불렀는지만 보면 모드 <code>superset</code>을 고를 수 있습니다. 다만 모드 <code>superset</code>은 묻지 않은 예약 요청도 참으로 봤습니다. 기준에 없는 요청을 막으려면 모드 <code>subset</code>이나 <code>strict</code>의 판정도 함께 봅니다.</p>
""" + runs_paragraph() + """<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>이 절의 궤적은 모두 코드로 적은 메시지 목록입니다. 도구 <code>search_documents</code>·<code>check_source</code>·<code>reserve_book</code>의 함수는 만들지 않았고, 결과 글도 이 절이 정했습니다. 실제 에이전트를 실행해 만든 궤적은 03절에서 봅니다.</li><li>견줄 궤적과 인자 <code>top_k</code>는 모드마다 판정이 갈리는 장면을 보여 주려고 정한 예입니다. 실제 에이전트가 이런 궤적을 얼마나 자주 만드는지는 이 절이 보여 주지 않습니다.</li><li>함수 <code>unpaired_names</code>는 도구 이름만으로 짝을 짓는 교재용 함수입니다. 라이브러리는 이름이 같고 인자가 맞아야 짝을 짓습니다. 이 절의 다섯 궤적은 인자가 모두 기준과 같아, 두 방식으로 본 결과가 맞았습니다.</li><li>LangChain 문서 표는 모드 <code>unordered</code>를 메시지 구조가 같고 도구 요청의 차례만 달라도 되는 모드로 적습니다. 설치판 agentevals 0.0.9는 도구 요청만 모아 견주고, 메시지 수는 보지 않았습니다. 한 응답에 요청 둘인 궤적이 이 모드에서 참이었던 것이 그 예입니다.</li><li>모드 <code>strict</code>가 보는 차례는 응답 사이의 차례이고, 한 응답에 함께 담긴 요청끼리의 차례는 보지 않습니다. 설치판 <code>trajectory/strict.py</code> 53~75행에서 봤고, 노트북에서는 실행하지 않았습니다.</li><li>인자 비교 방식은 방향이 바뀌는 모드를 섞지 않으려고 모드 <code>strict</code>에서만 견줬습니다. 노트북 밖에서 모드 <code>subset</code>과 함께 쓰자, 값 <code>subset</code>·<code>superset</code>의 결과가 모드 <code>strict</code>와 거꾸로였습니다. 모드 <code>unordered</code>와 함께 쓰자, 인자를 더한 궤적과 인자가 빠진 궤적이 두 값에서 모두 거짓이었습니다. 설치판이 모드 <code>subset</code>에서는 짝짓기 방향을 바꾸고, 모드 <code>unordered</code>에서는 두 방향으로 모두 짝짓기 때문입니다. 이 장면은 노트북에서는 실행하지 않았습니다.</li><li>모드 이름을 잘못 적으면 설치판 <code>trajectory/match.py</code> 80~83행이 <code>ValueError</code>를 냅니다. 인자 비교 방식 이름도 85~88행에서 같게 검사합니다. 둘 다 노트북에서는 실행하지 않았습니다.</li><li>설치판 <code>trajectory/utils.py</code> 194~212행을 보면, 도구별 덮어쓰기 값으로 함수나 인자 이름 목록도 줄 수 있습니다. 이 절은 인자 비교 방식 이름만 썼습니다.</li><li>이 절은 다섯 셀에 두 줄씩 <code>assert</code>를 두었고, 모두 모드나 인자 비교 방식에 따라 갈린 값에만 걸었습니다. 기준 궤적을 자기 자신과 견준 참처럼, 만든 대로 늘 참인 값에는 걸지 않았습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>차례를 바꾼 궤적과 한 응답에 요청 둘인 궤적은 모드 <code>strict</code>만 거짓이었고, 나머지 셋은 참이었습니다.</li><li>검색만 한 궤적은 모드 <code>subset</code>만, 예약을 더한 궤적과 검색 세 번 궤적은 모드 <code>superset</code>만 참이었습니다. 짝짓기는 요청 횟수까지 셉니다.</li><li>인자만 다른 궤적은 네 모드 모두 거짓이었고, 인자 비교 방식을 <code>ignore</code>로 바꾸자 모드 <code>strict</code>도 참이 되었습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_03 + """\">03절</a>에서는 코드 규칙 대신 평가 모델(judge)이 궤적을 읽고 판정합니다. 실제 에이전트를 한 번 실행해 만든 궤적도, 이 절의 모드와 평가 모델로 함께 판정합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 차례를 바꾼 궤적에서 거짓을 낸 모드는 무엇이고, 까닭은 무엇인가요?</p><p class="quiz-a">모드 <code>strict</code>만 거짓이었습니다. 메시지를 하나씩 견줘, 첫 모델 응답의 도구 요청부터 기준과 달랐기 때문입니다. 나머지 셋은 도구 요청만 모아 짝을 지어, 차례를 보지 않았습니다. 틀렸다면 노트북 3절 둘째 셀을 다시 읽습니다.</p><p class="quiz-q">2. 검색만 한 궤적과 예약을 더한 궤적에서 참을 낸 모드는 각각 무엇인가요?</p><p class="quiz-a">검색만 한 궤적은 모드 <code>subset</code>, 예약을 더한 궤적은 모드 <code>superset</code>입니다. 모드 <code>subset</code>은 빠진 요청을, 모드 <code>superset</code>은 더한 요청을 봐줍니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">3. 동료가 「실제 요청의 도구 이름이 모두 기준에 있으니 모드 <code>subset</code>은 참」이라고 말합니다. 검색 세 번 궤적에서 맞는 말인가요?</p><p class="quiz-a">맞지 않습니다. 이 궤적에서 모드 <code>subset</code>은 거짓이었습니다. 짝짓기는 기준 요청 하나에 실제 요청 하나만 짝지어, 남은 실제 검색 요청 둘이 짝을 찾지 못했습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">4. 검색어만 다른 궤적을 모드 <code>strict</code>에서 참이 되게 하려면 무엇을 바꾸면 되고, 그때 무엇을 조심해야 하나요?</p><p class="quiz-a">인자 비교 방식을 <code>ignore</code>로 바꾸거나, 검색 도구만 도구별 덮어쓰기로 인자를 보지 않게 합니다. 값 <code>ignore</code>는 검색어가 틀린 요청도 통과시키므로, 어느 도구의 인자를 느슨하게 볼지 정해야 합니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langchain/test/evals">LangChain Agent evals</a></div>확인 2026-09-29 · 궤적 맞춰 보기 모드 넷을 표로 적습니다. 모드 <code>subset</code>은 「no extras」, 모드 <code>superset</code>은 「extras allowed」로 적습니다. 모드 <code>unordered</code>는 메시지 구조가 같고 도구 요청의 차례만 달라도 된다고 적습니다.</li><li><div><a href="https://docs.langchain.com/langsmith/trajectory-evals">LangSmith Trajectory evals</a></div>확인 2026-09-29 · 기본으로는 같은 도구에 같은 인자를 준 요청만 같다고 봅니다. 인자 비교 방식과 도구별 덮어쓰기로 이 기준을 바꿀 수 있다고 적습니다.</li><li><div><a href="https://github.com/langchain-ai/agentevals">agentevals (GitHub)</a></div>확인 2026-09-29 · 인자 비교 방식 넷과 도구별 덮어쓰기 값의 모양(방식 이름·인자 이름 목록·함수)을 적습니다.</li><li><div><a href="https://pypi.org/project/agentevals/">agentevals (PyPI)</a></div>확인 2026-09-29 · 가장 새 판이 0.0.9(2025-07-24)입니다. 이 절의 잠금 판과 같습니다.</li><li>설치판 agentevals 0.0.9 소스 <code>trajectory/match.py</code> 72~88행은 모드와 인자 비교 방식 이름을 고르고 검사하는 줄입니다. <code>trajectory/strict.py</code> 34행은 메시지 수를 먼저 견주는 줄입니다.</li><li>같은 설치판 <code>trajectory/unordered.py</code> 33~37행은 두 방향 짝짓기입니다. <code>subset.py</code> 28~30행은 방향을 바꾼 짝짓기, <code>superset.py</code> 33~35행은 한 방향 짝짓기입니다. <code>utils.py</code> 90~134행은 짝짓기, 137~171행은 인자 비교 방식 넷, 194~212행은 도구별 덮어쓰기입니다.</li></ul>
"""


def write_src(path: Path) -> Path:
    path.write_text(src_html(), encoding="utf-8")
    return path


if __name__ == "__main__":
    check_tools()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "eval_tools.py").write_text(TOOLS_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    if "--try" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--try") + 1])
        write_tools(target / "eval_tools.py")
        print("wrote", write_src(target / "src.html"))
        print("wrote", write_notebook(target, "02", SLUG, "experiment", cells()))
        raise SystemExit(0)
    print("wrote", write_src(SRC))
    if "--src-only" not in sys.argv:
        # 도구 파일은 없거나 01판·이 판일 때만 쓴다. 뒤 절이 함수를 더한 판이면 덮어쓰지 않는다(Ch 24 마감 A-10·Ch 25~28 교훈).
        write_tools(TOOLS_PATH)
        path = write_notebook(LAB, "02", SLUG, "experiment", cells())
        print("wrote", path)
