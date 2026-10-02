"""Ch 29 01절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 -B author_01.py            → 도구 파일(없거나 이 판일 때만) + 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_01.py --src-only → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_01.py --tools-copy DIR → 디스크의 도구 파일을 DIR에 복사한다(새 커널 사본 B 실행용 — Ch 26 A-19 교훈)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**.
슬러그 `01-에이전트-평가-세-전략` 고정(Ch 28 06 b8이 링크 — 「Ch 29 01절은 평가 방법 세 가지를 견줍니다」).

## 결정 1 — 모델 M2의 01 몫: 모델 없음 (챕터 리드 결정 1)

궤적은 모두 코드로 적은 메시지 목록(Ch 20 01 손으로 만든 AIMessage 선례). 모델 요청 0, 키 셀·dotenv 없음.
결정적이라 새 커널 두 번 셀별 출력이 같아야 한다. 흔들림 확인(NN-probe.md)은 모델 판단이 없어 두지 않는다.

## 결정 2 — 세 전략을 같은 기준 궤적과 견준다 (챕터 리드 결정 2)

최종 답 평가 = 마지막 글이 기준 답과 글자까지 같은가(코드 규칙, Ch 18 05 코드 검사 선례) ·
한 단계 평가 = 첫 모델 응답(메시지 번호 1)이 요청한 도구 이름 목록이 기준과 같은가(Ch 19 04 tool_call_names) ·
궤적 평가 = agentevals create_trajectory_match_evaluator(trajectory_match_mode="strict")의 score.
궤적 넷: 기준과 같음 / 검색 세 번(낭비) / 답만 틀림 / 차례 바꿈. 값 바꿔 보기 = 답만 틀린 궤적의 답 글 하나만 뜻이 맞는 다른 글로.
네 모드 비교·횟수 짝짓기·인자 비교는 02 몫이라 쓰지 않는다(모드는 strict 하나만 첫 정의).
설치판 사실(노트북 밖 /tmp/ch29-01/exp/x1.py, 다섯 번 같음): strict는 메시지 수·역할·도구 요청(이름·인자)만 보고 글을 보지 않음 —
질문 글·도구 결과 글·호출 ID만 바꾼 궤적도 True(노트북에서는 실행하지 않음 — b7에 「노트북 밖」).
만든 대로 늘 참인 assert는 두지 않는다(옛 c10). 라이브러리 점수에도 assert를 두지 않았다(02가 허용 여부 판단).

## 결정 3 — 도구 파일 eval_tools.py 첫 판 (챕터 리드 결정 5)

이 노트북이 쓰는 앞 챕터 함수 둘(tool_call_names Ch 19 04 · show_messages Ch 19 06)을 Ch 21 runner_tools.py(f4113158…)에서
설명 주석과 본문을 글자 그대로 옮긴다(Ch 27 harness_tools.py·Ch 28 connect_tools.py 판과도 대조). import 0.
01이 처음 가르친 함수(make_trajectory·called_tool_names·final_answer_pass·first_step_pass·trajectory_pass·three_results)는
01 노트북에 둔다 — 02·03이 다시 쓰면 그 절이 셀 글 그대로 도구 파일로 옮긴다(대조 사슬 — strip_later_imports·쓰기 가드).
쓰기 가드: 파일이 없거나 이 판과 같을 때만 쓰고, 뒤 절이 함수를 더한 판(strip_later_imports 뒤 이 판으로 시작)은 건너뜀.

## 결정 4 — 소재 (Ch 14·21 이음)

질문 「일반 도서는 며칠 동안 빌릴 수 있나요?」 · 기준 답 「일반 도서는 14일 동안 빌릴 수 있습니다.」 ·
도구 이름 search_documents(인자 query — Ch 21 05 검색 도구 이름)·check_source(인자 doc_id) — 함수는 만들지 않고 결과 글만 정함 ·
검색 결과 글은 Ch 14 documents.json LIB-001 글에 [문서 ID]를 붙인 모양(Ch 21 05 도구 메시지 모양).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·힌트·대입 풀기·별표 풀기·`while`·`try`·
세미콜론·`isinstance`·클래스·데코레이터·`async`. 호출 깊이 2 이하. 음수 번호 `[-1]`(Ch 16 03 음수 슬라이스 이음 — 첫 자리 한 문장).
"""
from __future__ import annotations

import ast
import hashlib
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch29-agent-evaluation/notebooks"
FIGS = ROOT / "textbook/part6/ch29-agent-evaluation/figures"
SLUG = "01-에이전트-평가-세-전략"
TITLE_TEXT = "에이전트 평가 세 전략"
SRC = ROOT / "textbook/part6/ch29-agent-evaluation/_src" / (SLUG + ".html")
TOOLS_PATH = LAB / "eval_tools.py"
RUNNER = ROOT / "labs/part6/ch21-create-agent/notebooks/runner_tools.py"
RUNNER_SHA = "f4113158c0ccaee1205f0eabe315ef153e14c4dc6bcfd70ae8a9378edda96bdf"
HARNESS = ROOT / "labs/part6/ch27-deepagents/notebooks/harness_tools.py"
# 전체 마감(2026-09-30)에서 Ch 27 도구 파일 머리 설명 줄만 고쳐 7a40d994… → ed5c4240…(함수 본문 같음)
HARNESS_SHA = "ed5c424006c2b41dd40c3d4861555fbe4180b8df7de2144febd7ef4f9a3f5b2c"
CONNECT = ROOT / "labs/part6/ch28-mcp/notebooks/connect_tools.py"
CONNECT_SHA = "570ed3cc607871a374ac1d5d7fc3ba6435908669ae79f48908535787d16f204c"
RUNS_SENTENCE = os.environ.get("AUTHOR01_RUNS_SENTENCE", "새 커널로 두 번 실행해 견주자, 코드 셀 스물셋의 출력이 셀마다 모두 같았습니다. 모델을 부르지 않아, 이 절의 판정은 코드로 적은 궤적과 규칙으로 정해집니다.")

# ---------------------------------------------------------------- 도구 파일 eval_tools.py (첫 판)
TOOLS_HEAD = '''"""Ch 29 Agent 평가 — 앞 챕터와 이 챕터에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from eval_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
이 챕터 노트북이 실제로 쓰는 함수만 담고, 새 함수가 필요한 절이 그때 더합니다.
Ch 21 도구 파일 runner_tools.py에서 옮긴 함수는 설명 주석과 본문을 글자 그대로 옮겼습니다.
Ch 15 06절 노트북 셀에서 옮긴 함수(average·nearest_rank)도 그 셀의 주석과 본문을 글자 그대로 옮겼습니다.
이 챕터 앞 절 노트북에서 처음 적은 함수를 옮길 때는, 그 셀의 주석과 본문을 글자 그대로 옮깁니다.
앞 챕터 도구 파일은 이 챕터 실습 폴더에 없는 패키지(numpy 등)를 가져오거나 그 챕터 폴더에 묶여 있어,
파일째 가져오지 않습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
평가 함수를 만드는 줄(create_trajectory_match_evaluator 등)은 이 파일에 두지 않고 노트북에 둡니다.
"""
'''

RUNNER_NOTES = [
    ("tool_call_names", "Ch 19 04절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다"),
    ("show_messages", "Ch 19 06절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다"),
]
TOOL_ORDER = ["tool_call_names", "show_messages"]


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_block(text: str, name: str) -> str:
    """도구 파일 글에서 함수 하나의 설명 주석(배운 곳 줄 뺌)과 본문을 글자 그대로 꺼냅니다(Ch 27 author_02와 같은 함수)."""
    lines = text.splitlines()
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            start = node.lineno - 1
            top = start
            while top > 0 and lines[top - 1].startswith("#"):
                top = top - 1
            return "\n".join(lines[top + 1:node.end_lineno])
    raise KeyError(name)


def tools_text() -> str:
    runner = RUNNER.read_text(encoding="utf-8")
    assert sha(runner) == RUNNER_SHA, "Ch 21 runner_tools.py가 마감 판과 다릅니다"
    text = TOOLS_HEAD
    for name, note in RUNNER_NOTES:
        text = text + "\n\n# " + note + "\n" + file_block(runner, name) + "\n"
    return text


TOOLS = tools_text()


def strip_later_imports(text: str) -> str:
    """머리 설명과 첫 함수 주석 사이에 뒤 절이 더한 가져오기 줄이 있으면 빼고 내놓습니다(Ch 25~28 대조 사슬과 같은 줄)."""
    if not text.startswith(TOOLS_HEAD):
        return text
    rest = text[len(TOOLS_HEAD):]
    first = rest.find("\n\n# Ch ")
    if first <= 0:
        return text
    return TOOLS_HEAD + rest[first:]


def check_tools() -> None:
    """도구 파일 01절 판의 함수 둘이 원본(Ch 21 runner_tools.py)과 글자·AST 모두 같고, Ch 27·28 판과도 본문이 같은지 봅니다."""
    runner = RUNNER.read_text(encoding="utf-8")
    harness = HARNESS.read_text(encoding="utf-8")
    connect = CONNECT.read_text(encoding="utf-8")
    assert sha(harness) == HARNESS_SHA, "Ch 27 harness_tools.py가 마감 판과 다릅니다"
    assert sha(connect) == CONNECT_SHA, "Ch 28 connect_tools.py가 마감 판과 다릅니다"
    tree = ast.parse(TOOLS)
    names = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise AssertionError("01절 판 도구 파일은 아무것도 가져오지 않습니다")
    assert names == TOOL_ORDER, names
    runner_tree = ast.parse(runner)
    for name, note in RUNNER_NOTES:
        block = file_block(runner, name)
        assert ("# " + note + "\n" + block + "\n") in TOOLS
        assert file_block(harness, name) == block, name + "가 Ch 27 판과 다릅니다"
        mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        theirs = [ast.dump(n) for n in runner_tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        assert mine == theirs and len(mine) == 1, name
    assert file_block(connect, "tool_call_names") == file_block(runner, "tool_call_names"), "Ch 28 판과 다릅니다"


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["agentevals==0.0.9", "langchain==1.4.0"])

IMPORTS = r'''# 궤적을 맞춰 보는 평가 함수를 만드는 함수와, 메시지 클래스 셋(Ch 13 04절·Ch 19 05절)을 가져옵니다
from agentevals.trajectory.match import create_trajectory_match_evaluator
from langchain.messages import AIMessage, HumanMessage, ToolMessage
# 앞 챕터에서 배운 함수 둘은 도구 파일에서 가져옵니다(Ch 19 04절·06절)
from eval_tools import show_messages, tool_call_names

print("도구 파일에서 가져온 함수:", "show_messages, tool_call_names")'''

DATA = r'''# 질문과 기준 답, 도구마다 돌아올 결과 글을 정합니다(교재용 글 — 검색 결과는 Ch 14 문서 LIB-001의 글)
question = "일반 도서는 며칠 동안 빌릴 수 있나요?"
reference_answer = "일반 도서는 14일 동안 빌릴 수 있습니다."
tool_results = {
    "search_documents": "[LIB-001] 일반 도서는 14일 동안 대출할 수 있습니다. 예약자가 없으면 한 번 연장할 수 있습니다.",
    "check_source": "LIB-001 문서가 있습니다. 제목: 도서 대출 기간",
}
print("질문:", question)
print("기준 답:", reference_answer)
print("결과 글을 정한 도구:", list(tool_results))'''

DEF_MAKE = r'''# 질문·도구 요청 목록·결과 글·답 글로, 질문에서 답까지의 메시지 목록(궤적)을 만들어 내놓습니다
def make_trajectory(question, calls, results, answer):
    messages = [HumanMessage(content=question)]
    # 도구 요청 하나마다, 그 요청을 담은 모델 응답과 같은 호출 ID의 도구 메시지를 한 쌍씩 붙입니다
    for call in calls:
        messages.append(AIMessage(content="", tool_calls=[call]))
        messages.append(ToolMessage(content=results[call["name"]], tool_call_id=call["id"]))
    # 마지막에는 도구를 요청하지 않는 모델 응답, 곧 최종 답을 붙입니다
    messages.append(AIMessage(content=answer))
    return messages'''

REFERENCE = r'''# 기준 궤적의 도구 요청 둘을 정하고 궤적을 만듭니다(칸 넷은 Ch 19 04절 도구 호출 요청과 같은 모양)
search_args = {"query": "도서 대출 기간"}
source_args = {"doc_id": "LIB-001"}
reference_calls = [
    {"name": "search_documents", "args": search_args, "id": "call_1", "type": "tool_call"},
    {"name": "check_source", "args": source_args, "id": "call_2", "type": "tool_call"},
]
reference = make_trajectory(question, reference_calls, tool_results, reference_answer)
print("기준 궤적의 메시지 수:", len(reference))'''

SHOW_REF = r'''# 기준 궤적의 메시지를 차례대로 보고, 마지막 메시지의 글(최종 답)도 봅니다
print("기준 궤적:")
show_messages(reference)
# 번호 -1은 목록의 마지막 자리입니다
print("최종 답:", reference[-1].content)'''

DEF_CALLED = r'''# 궤적의 모델 응답마다 요청한 도구 이름을 차례대로 모아, 목록 하나로 내놓습니다
def called_tool_names(messages):
    names = []
    for message in messages:
        # 도구 호출 요청은 모델 응답(AIMessage)에만 있습니다
        if type(message).__name__ == "AIMessage":
            for name in tool_call_names(message):
                names.append(name)
    return names'''

REF_NAMES = r'''# 기준 궤적의 도구 차례와 도구 요청 수를 봅니다
reference_names = called_tool_names(reference)
print("기준 궤적의 도구 차례:", reference_names)
print("도구 요청 수:", len(reference_names))'''

DEF_FINAL = r'''# 최종 답 평가: 마지막 메시지의 글이 기준 궤적의 마지막 글과 글자까지 같은지 봅니다
def final_answer_pass(messages, reference):
    actual_text = messages[-1].content
    expected_text = reference[-1].content
    return actual_text == expected_text'''

DEF_STEP = r'''# 한 단계 평가: 첫 모델 응답(메시지 목록의 1번 자리)이 요청한 도구 이름이 기준과 같은지 봅니다
def first_step_pass(messages, reference):
    actual_names = tool_call_names(messages[1])
    expected_names = tool_call_names(reference[1])
    return actual_names == expected_names'''

MAKE_STRICT = r'''# 궤적을 맞춰 보는 평가 함수를 strict 모드로 만듭니다(모드 이름을 넣으면 평가 함수를 내놓습니다)
strict_match = create_trajectory_match_evaluator(trajectory_match_mode="strict")
# 평가 함수에 실제 궤적(outputs)과 기준 궤적(reference_outputs)을 넣으면 결과 딕셔너리를 내놓습니다
self_result = strict_match(outputs=reference, reference_outputs=reference)
print("평가 함수의 종류:", type(strict_match).__name__)
print("결과 딕셔너리:", self_result)'''

DEF_TRAJ = r'''# 궤적 평가: 평가 함수로 실제 궤적을 기준 궤적과 견주고, 결과 딕셔너리의 칸 score만 꺼냅니다
def trajectory_pass(messages, reference, evaluator):
    result = evaluator(outputs=messages, reference_outputs=reference)
    return result["score"]'''

DEF_THREE = r'''# 세 평가를 한 궤적에 모두 적용해, 한국어 키 딕셔너리 한 줄로 내놓습니다
def three_results(messages, reference, evaluator):
    row = {
        "최종 답": final_answer_pass(messages, reference),
        "한 단계": first_step_pass(messages, reference),
        "궤적": trajectory_pass(messages, reference, evaluator),
    }
    return row'''

SAME = r'''# 기준 궤적과 같은 요청·답으로 실제 궤적을 하나 새로 만듭니다(모든 평가가 참이어야 할 줄)
same = make_trajectory(question, reference_calls, tool_results, reference_answer)
same_names = called_tool_names(same)
print("도구 차례:", same_names)
print("최종 답:", same[-1].content)'''

WASTEFUL = r'''# 같은 검색어로 검색을 세 번 한 뒤 출처를 확인하는 궤적을 만듭니다(답은 기준과 같은 글)
wasteful_calls = [
    {"name": "search_documents", "args": search_args, "id": "call_1", "type": "tool_call"},
    {"name": "search_documents", "args": search_args, "id": "call_2", "type": "tool_call"},
    {"name": "search_documents", "args": search_args, "id": "call_3", "type": "tool_call"},
    {"name": "check_source", "args": source_args, "id": "call_4", "type": "tool_call"},
]
wasteful = make_trajectory(question, wasteful_calls, tool_results, reference_answer)
wasteful_names = called_tool_names(wasteful)
print("도구 차례:", wasteful_names)
print("도구 요청 수:", len(wasteful_names), "| 메시지 수:", len(wasteful))'''

WRONG = r'''# 도구 요청은 기준과 같고 답 글만 틀린 궤적을 만듭니다
wrong_text = "일반 도서는 7일 동안 빌릴 수 있습니다."
wrong_answer = make_trajectory(question, reference_calls, tool_results, wrong_text)
wrong_names = called_tool_names(wrong_answer)
print("도구 차례:", wrong_names)
print("최종 답:", wrong_answer[-1].content)'''

REVERSED = r'''# 출처 확인을 먼저 하고 검색을 뒤에 하는, 차례를 바꾼 궤적을 만듭니다(답은 기준과 같은 글)
reversed_calls = [
    {"name": "check_source", "args": source_args, "id": "call_1", "type": "tool_call"},
    {"name": "search_documents", "args": search_args, "id": "call_2", "type": "tool_call"},
]
reversed_order = make_trajectory(question, reversed_calls, tool_results, reference_answer)
reversed_names = called_tool_names(reversed_order)
print("도구 차례:", reversed_names)'''

TABLE = r'''# 궤적 넷을 이름과 함께 모으고, 궤적마다 세 평가 결과를 한 줄씩 출력합니다
trajectories = {"기준과 같음": same, "검색 세 번": wasteful, "답만 틀림": wrong_answer, "차례 바꿈": reversed_order}
print("궤적 | 최종 답 평가 | 한 단계 평가 | 궤적 평가")
for name in trajectories:
    row = three_results(trajectories[name], reference, strict_match)
    print(name, "|", row["최종 답"], "|", row["한 단계"], "|", row["궤적"])'''

FAILED = r'''# 궤적마다 거짓(False)을 낸 평가의 이름만 모아 출력합니다
for name in trajectories:
    row = three_results(trajectories[name], reference, strict_match)
    failed = []
    for strategy in row:
        if not row[strategy]:
            failed.append(strategy)
    print(name, "| 거짓을 낸 평가:", failed)'''

FIRST_STEPS = r'''# 궤적 넷의 첫 모델 응답(1번 자리)이 요청한 도구 이름만 봅니다(한 단계 평가가 보는 자리)
for name in trajectories:
    first_names = tool_call_names(trajectories[name][1])
    print(name, "| 첫 응답의 도구 요청:", first_names)'''

WHY_WRONG = r'''# 답만 틀린 궤적을 기준 궤적과 견줘, 무엇이 같고 무엇이 다른지 봅니다
print("메시지 수가 같은가:", len(wrong_answer) == len(reference))
print("도구 차례가 같은가:", wrong_names == reference_names)
print("최종 답이 같은가:", wrong_answer[-1].content == reference[-1].content)'''

REWORDED = r'''# 값 바꿔 보기: 답만 틀린 궤적에서 답 글 하나만, 뜻이 맞는 다른 글로 바꾼 궤적을 만듭니다
reworded_text = "14일 동안 빌릴 수 있습니다."
reworded = make_trajectory(question, reference_calls, tool_results, reworded_text)
print("기준 답:", reference[-1].content)
print("바꾼 답:", reworded[-1].content)'''

COMPARE = r'''# 답만 틀린 궤적과 답 글을 바꾼 궤적의 세 평가 결과를 나란히 봅니다
wrong_row = three_results(wrong_answer, reference, strict_match)
reworded_row = three_results(reworded, reference, strict_match)
print("답만 틀림:", wrong_row)
print("답 글을 바꿈:", reworded_row)
print("두 줄이 같은가:", wrong_row == reworded_row)'''


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/01-figures.md)
FIG1 = "01-1-세-평가가-보는-자리"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 기준 궤적 메시지 여섯이라는 칸 안에 초록 상자 넷이 화살표로 이어집니다. 질문 HumanMessage, 첫 모델 응답 도구 요청 search_documents, 도구 결과와 둘째 응답 도구 요청 check_source와 도구 결과, 마지막 모델 응답 최종 답 글입니다. 칸 위의 파란 상자 궤적 평가 strict 모드 평가 함수에서 칸 전체로 점선 화살표가 갑니다. 칸 오른쪽 파란 상자 둘에서도 점선 화살표가 나갑니다. 한 단계 평가 first_step_pass는 첫 모델 응답 상자로, 최종 답 평가 final_answer_pass는 마지막 모델 응답 상자로 가는 그림"
FIG1_CAP = "한 단계 평가는 첫 모델 응답을, 궤적 평가는 메시지 여섯 전체를, 최종 답 평가는 마지막 글을 봅니다."
FIG1_READ = """칸 안의 화살표를 따라 위에서 아래로 읽습니다.
칸 안 초록 상자 넷은 노트북 2절에서 코드로 적은 기준 궤적이고, 셋째 상자에는 메시지 셋이 들어 있습니다.
칸 위의 파란 상자와 칸 오른쪽의 파란 상자 둘은 3절에서 정의하거나 만든 평가 함수입니다.
점선 화살표는 평가마다 보는 자리를 가리키고, 칸 위 궤적 평가의 점선만 칸 전체로 갑니다."""

FIG2 = "01-2-궤적을-만드는-함수"
FIG2_ALT = "위에서 아래로 읽는 흐름도입니다. 초록 상자 셋 질문과 기준 답 글, 도구 요청 목록 reference_calls 둘, 도구 결과 글 tool_results에서 파란 상자 make_trajectory 요청마다 응답과 도구 메시지 한 쌍으로 화살표가 모입니다. 이어서 노란 상자 기준 궤적 reference 메시지 수 6, 파란 상자 called_tool_names, 노란 상자 도구 차례 search_documents와 check_source 도구 요청 수 2로 화살표가 이어지는 그림"
FIG2_CAP = "함수 make_trajectory가 도구 요청 둘로 메시지 여섯의 기준 궤적을 만들고, called_tool_names가 도구 차례를 꺼냈습니다."
FIG2_READ = """위에서 아래로 읽습니다.
맨 위 초록 상자 셋은 노트북 2절 첫 셀과 셋째 셀에서 정한 글과 목록입니다.
파란 상자 둘은 이 절에서 정의한 함수이고, 노란 상자 둘은 셀 출력입니다.
도구 요청 하나가 메시지 둘이 되어, 요청 둘에 질문과 최종 답을 더하면 메시지가 여섯입니다."""

FIG3 = "01-3-궤적-넷의-세-평가"
FIG3_ALT = "위에서 아래로 읽는 그림입니다. 맨 위 회색 상자 기준 궤적과 strict 모드 평가 함수 네 궤적 모두 같은 것과 견줌에서 궤적마다 세 평가 결과라는 칸으로 화살표가 갑니다. 칸 안에 노란 상자 넷이 위아래로 놓입니다. 기준과 같음 최종 답 True 한 단계 True 궤적 True, 검색 세 번 최종 답 True 한 단계 True 궤적 False, 답만 틀림 최종 답 False 한 단계 True 궤적 True, 차례 바꿈 최종 답 True 한 단계 False 궤적 False인 그림"
FIG3_CAP = "같은 기준 궤적과 견주자, 검색 세 번은 궤적 평가만, 답만 틀림은 최종 답 평가만 거짓이었습니다."
FIG3_READ = """맨 위 회색 상자에서 아래 칸으로 읽습니다.
회색 상자는 네 궤적 모두에 같이 쓴 기준 궤적과 평가 함수입니다.
칸 안 노란 상자 넷은 노트북 5절 첫 셀의 출력 네 줄입니다.
네 궤적은 서로 다른 조건이라 화살표 없이 위아래로 두었습니다."""

FIG4 = "01-4-답-글만-바꾼-궤적"
FIG4_ALT = "위에서 아래로 읽는 그림입니다. 맨 위 회색 상자에 도구 요청은 기준 궤적과 같음, 기준 답 일반 도서는 14일 동안 빌릴 수 있습니다가 있습니다. 그 아래 답만 틀림 칸에는 초록 상자 최종 답 글 일반 도서는 7일 동안 빌릴 수 있습니다에서 노란 상자 최종 답 False 한 단계 True 궤적 True로 화살표가 갑니다. 다음 답 글을 바꿈 칸에는 파란 상자 최종 답 글 14일 동안 빌릴 수 있습니다에서 노란 상자 최종 답 False 한 단계 True 궤적 True로 화살표가 갑니다. 맨 아래 노란 상자는 두 줄이 같은가 True인 그림"
FIG4_CAP = "답 글을 뜻이 맞는 다른 글로 바꿔도, 최종 답 평가는 답이 틀린 궤적과 같은 거짓을 냈습니다."
FIG4_READ = """위에서 아래로 읽습니다.
맨 위 회색 상자는 두 궤적에 공통인 도구 요청과 기준 답입니다.
위 칸의 초록 상자는 4절에서 적은 틀린 답이고, 아래 칸의 파란 상자는 6절에서 바꾼 답입니다.
노란 상자 셋은 6절 마지막 셀의 출력이고, 두 칸의 노란 상자 글이 같습니다."""

ILLU = "01-5-오르골-종이띠"
ILLU_ALT = "흰 바탕 왼쪽에 옆면에 손잡이가 달린 닫힌 나무 오르골 상자 하나가 있고, 상자 옆 틈에서 둥근 구멍이 한 줄로 뚫린 연한 종이띠 하나가 오른쪽으로 뻗어 있습니다. 이 띠의 첫 구멍 위와 오른쪽 끝 위에 작은 돋보기가 하나씩 놓여 있습니다. 그 아래에는 같은 모양의 구멍이 한 줄로 뚫린 종이띠 하나가 상자와 떨어진 채 나란히 놓여 있습니다. 사람·글자·숫자·음표·화살표는 없는 그림"
ILLU_CAP = "오르골 상자에서 나온 띠의 처음과 끝에 돋보기가 하나씩 있고, 그 아래에 기준 띠가 나란히 놓여 있습니다."
ILLU_READ = "흰 바탕 왼쪽에 닫힌 나무 오르골 상자가 있고, 옆 틈에서 구멍 뚫린 종이띠 하나가 뻗어 나옵니다. 이 띠의 첫 구멍 위와 끝 위에 돋보기가 하나씩 있고, 아래에는 상자와 떨어진 띠 하나가 나란히 놓여 있습니다. 상자가 에이전트, 위 띠가 실제 궤적, 아래 띠가 기준 궤적이고, 두 띠를 나란히 둔 모습이 궤적 평가입니다. 첫 구멍의 돋보기는 한 단계 평가, 끝의 돋보기는 최종 답 평가입니다. 구멍의 수, 띠의 길이와 기울기, 상자의 손잡이는 어떤 값과도 짝짓지 않고, 두 띠가 같은 궤적인지도 나타내지 않습니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 에이전트가 질문에서 답까지 밟은 단계의 차례(궤적)를 모델 없이 메시지 목록으로 적고, 기준 궤적을 하나 정합니다.
2. 최종 답 평가·한 단계 평가·궤적 평가를 함수로 만들어, 궤적 넷을 같은 기준 궤적과 견줍니다.
3. 어느 평가가 어느 궤적을 거짓으로 보는지 확인하고, 답 글 하나만 바꿔 다시 견줍니다.

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

**강의와 실습 범위** — 강의 시간에는 2·3절을 읽습니다.
궤적을 적는 방법과, 세 평가가 궤적의 어느 자리를 보는지 다루는 자리입니다.
4~6절은 궤적을 바꿔 가며 견주는 실습이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch29-agent-evaluation`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

에이전트는 답을 내기 전에 도구를 고르고 부르는 일을 여러 번 합니다.
이 절은 그 과정을 평가하는 방법 세 가지를 견줍니다.
뜻과 구성은 본문 「핵심 개념」에서 풉니다.

첫 셀은 패키지 둘을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `agentevals: 0.0.9`와 `langchain: 1.4.0`이 보입니다.
둘 다 실습 폴더 잠금과 같은 판입니다.
패키지 agentevals는 에이전트의 궤적을 평가하는 함수를 모은 라이브러리입니다.
패키지 langchain에서는 메시지 클래스 셋을 가져옵니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
함수 `create_trajectory_match_evaluator`는 궤적을 맞춰 보는 평가 함수를 만들어 내놓는 함수이고, 3절에서 씁니다.
메시지 클래스 셋은 Ch 13 04절·Ch 19 05절에서 쓴 `HumanMessage`·`AIMessage`·`ToolMessage`입니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: show_messages, tool_call_names`가 보입니다.
앞에서 배운 함수는 `eval_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.

노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다.

함수 `tool_call_names`는 Ch 19 04절에서 배운 함수로, 모델 응답 하나가 요청한 도구 이름을 목록으로 내놓습니다.
함수 `show_messages`는 Ch 19 06절에서 배운 함수로, 메시지 목록을 한 줄에 하나씩 출력합니다.
이 노트북에는 API 키를 확인하는 셀이 없습니다.
모델을 부르지 않기 때문입니다.

## 2. 기준 궤적 만들기

에이전트가 질문에서 최종 답까지 밟은 단계의 차례를 궤적(trajectory)이라고 부릅니다.
Ch 17 04절은 실행 기록의 단계를 차례대로 늘어놓은 것을 단계 차례(궤적)라고 불렀고, 이 챕터는 그 말을 이어 씁니다.
이 절은 에이전트를 실제로 돌리지 않고, 질문·도구 호출 요청·도구 결과·답이 오간 메시지 목록을 코드로 적어 궤적으로 씁니다.

다음 셀은 궤적에 들어갈 글을 정합니다.
질문과 기준 답, 그리고 도구 둘이 내놓을 결과 글입니다.
도구 `search_documents`는 자료실 문서를 찾는 도구이고, `check_source`는 찾은 문서가 실제로 있는지 확인하는 도구입니다.
두 도구의 함수는 만들지 않고, 결과 글만 정해 둡니다."""),
        code(DATA),
        md("""**결과 읽기** — 출력 줄 `질문: 일반 도서는 며칠 동안 빌릴 수 있나요?`와 `기준 답: 일반 도서는 14일 동안 빌릴 수 있습니다.`가 보입니다.
라벨 `결과 글을 정한 도구:` 뒤에는 `'search_documents'`와 `'check_source'`가 있습니다.

검색 결과 글은 Ch 14 문서 LIB-001의 글 앞에 문서 ID를 대괄호로 붙인 모양입니다.
도구 이름과 이 모양은 Ch 21 05절에서 만든 검색 도구를 빌렸습니다.

다음 셀은 질문·도구 요청 목록·결과 글·답 글을 받아 궤적을 만드는 함수를 정의합니다.
도구 요청 하나는 Ch 19 04절에서 본 칸 넷(`name`·`args`·`id`·`type`)을 가진 딕셔너리입니다.
요청마다 그 요청을 담은 모델 응답(`AIMessage`)과, 같은 호출 ID를 단 도구 메시지(`ToolMessage`)를 한 쌍씩 붙입니다.
Ch 20 01절에서 모델 없이 도구 호출 요청을 손으로 만든 것과 같은 방법입니다."""),
        code(DEF_MAKE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
도구 요청이 둘이면 메시지는 질문 하나, 쌍 둘, 최종 답 하나로 모두 여섯 개가 됩니다.
도구 메시지의 글은 인자 `results`에서 도구 이름으로 찾습니다.

다음 셀은 기준 궤적을 만듭니다.
기준 궤적(reference trajectory)은 좋은 에이전트라면 밟을 것이라고 사람이 미리 적어 둔 궤적입니다.
이 절의 기준은 문서를 한 번 검색하고, 찾은 문서가 있는지 한 번 확인한 뒤 답하는 차례입니다.
이 차례는 흐름을 보여 주려고 이 절이 정한 예입니다."""),
        code(REFERENCE),
        md("""**결과 읽기** — 출력 줄 `기준 궤적의 메시지 수: 6`이 보입니다.
질문 하나, 도구 요청과 결과의 쌍 둘, 최종 답 하나입니다.
인자 딕셔너리 `search_args`와 `source_args`는 4절에서 다른 궤적을 만들 때 다시 씁니다.

다음 셀은 기준 궤적을 함수 `show_messages`로 한 줄씩 봅니다.
이 함수는 최종 답의 글을 출력하지 않으므로, 마지막 메시지의 글을 따로 출력합니다.
번호 `-1`은 Ch 16 03절의 음수 슬라이스처럼 뒤에서 센 자리이고, 목록의 마지막을 가리킵니다."""),
        code(SHOW_REF),
        md("""**결과 읽기** — 라벨 `기준 궤적:` 아래 여섯 줄이 메시지 여섯의 종류입니다.
둘째 줄 `AIMessage | 도구 호출 요청: ['search_documents']`가 첫 모델 응답이고, 넷째 줄이 `check_source`를 요청한 둘째 응답입니다.
도구 메시지 두 줄은 결과 상태가 `success`이고, 내용은 앞 셀에서 정한 결과 글입니다.
마지막 `AIMessage` 줄은 도구 호출 요청이 빈 목록 `[]`이고, 출력 줄 `최종 답: 일반 도서는 14일 동안 빌릴 수 있습니다.`가 그 응답의 글입니다.

다음 셀은 궤적 전체에서 요청한 도구 이름을 차례대로 모으는 함수를 정의합니다.
모델 응답마다 함수 `tool_call_names`로 이름을 꺼내, 한 목록에 이어 붙입니다."""),
        code(DEF_CALLED),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
클래스 이름을 글로 꺼내는 `type(message).__name__`은 Ch 19 06절의 `show_messages`에도 있는 줄입니다.
질문과 도구 메시지는 건너뛰고 모델 응답만 봅니다.

다음 셀은 기준 궤적의 도구 차례와 도구 요청 수를 봅니다."""),
        code(REF_NAMES),
        md("""**결과 읽기** — 출력 줄 `기준 궤적의 도구 차례: ['search_documents', 'check_source']`와 `도구 요청 수: 2`가 보입니다.
기준 궤적은 검색 한 번, 출처 확인 한 번으로 도구를 두 번 요청합니다.
이 목록은 도구 이름만 모은 도구 차례이고, 궤적은 도구 결과와 답까지 든 메시지 목록 전체입니다.

## 3. 세 평가 함수

LangSmith 문서는 에이전트를 평가하는 방법을 셋으로 나눕니다.
마지막 답만 보는 최종 답 평가, 한 단계만 떼어 보는 한 단계 평가, 모든 단계를 보는 궤적 평가입니다.
이 절은 셋을 함수 하나씩으로 적고, 세 함수 모두 실제 궤적과 기준 궤적을 인자로 받게 합니다.

다음 셀은 최종 답 평가(final response)를 정의합니다.
마지막 메시지의 글이 기준 궤적의 마지막 글과 글자까지 같으면 `True`를 내놓습니다.
Ch 18 05절의 코드 검사처럼, 모델을 부르지 않고 코드 규칙으로 판정합니다."""),
        code(DEF_FINAL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
글자가 하나라도 다르면 `False`입니다.
뜻이 같은지까지는 보지 않으며, 이 한계는 6절에서 다시 봅니다.

다음 셀은 한 단계 평가(single step)를 정의합니다.
이 절에서 볼 한 단계는 첫 모델 응답이고, 메시지 목록의 1번 자리에 있습니다.
그 응답이 요청한 도구 이름 목록이 기준 궤적의 첫 응답과 같으면 `True`를 내놓습니다."""),
        code(DEF_STEP),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
첫 응답 뒤의 단계는 이 함수가 보지 않습니다.
LangSmith 문서도 한 단계 평가는 빠르지만, 에이전트 전체가 아니라 한 단계만 본다고 적습니다.

다음 셀은 궤적 평가(trajectory)에 쓸 평가 함수를 라이브러리로 만듭니다.
함수 `create_trajectory_match_evaluator`는 실제 궤적을 기준 궤적과 코드 규칙으로 맞춰 보는 평가 함수를 만들어 내놓습니다.
이 챕터는 이렇게 맞춰 보는 방법을 궤적 맞춰 보기(trajectory match)라고 부릅니다.

맞춰 보는 규칙(모드)은 인자 `trajectory_match_mode`로 고르고, 이 절은 `"strict"` 하나만 씁니다.
모드 `strict`는 메시지 수와 차례, 도구 요청의 이름과 인자가 기준과 모두 같아야 참을 냅니다.
모드는 셋이 더 있고, 02절에서 넷을 견줍니다."""),
        code(MAKE_STRICT),
        md("""**결과 읽기** — 출력 줄 `평가 함수의 종류: function`이 보입니다.
만든 평가 함수는 평범한 파이썬 함수처럼 부를 수 있습니다.
라벨 `결과 딕셔너리:` 뒤에 `'key': 'trajectory_strict_match'`와 `'score': True`가 있습니다.
칸 `score`가 판정이고, 기준 궤적을 자기 자신과 견줬으니 참입니다.

칸 `comment`와 `metadata`는 `None`입니다.
LangChain 문서의 예시 결과에는 칸 셋만 있고, 설치판 출력에는 칸 `metadata`가 더 있습니다.
이 절은 칸 `score`만 꺼내 씁니다.

다음 셀은 이 평가 함수로 궤적 평가를 하는 함수를 정의합니다."""),
        code(DEF_TRAJ),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
평가 함수를 인자 `evaluator`로 받아, 다른 모드로 만든 평가 함수도 넘길 수 있게 했습니다.

다음 셀은 세 평가를 한 궤적에 모두 적용하는 함수를 정의합니다.
결과는 Ch 17 01절처럼 한국어 키 딕셔너리 한 줄입니다."""),
        code(DEF_THREE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
키 셋은 `최종 답`·`한 단계`·`궤적`이고, 값은 모두 참·거짓 값입니다.

## 4. 견줄 궤적 넷 만들기

이제 기준 궤적과 견줄 실제 궤적 넷을 만듭니다.
모두 코드로 적은 궤적이고, 실제 에이전트가 만든 궤적은 03절에서 봅니다.
첫째는 기준 궤적과 같은 요청·답으로 만든 궤적입니다.
나머지 셋과 견줄 때, 모든 평가가 참인 줄이 되는지 봅니다."""),
        code(SAME),
        md("""**결과 읽기** — 출력 줄 `도구 차례: ['search_documents', 'check_source']`와 `최종 답: 일반 도서는 14일 동안 빌릴 수 있습니다.`가 보입니다.
기준 궤적과 같은 요청·답으로 만든 새 목록입니다.

다음 셀은 검색을 세 번 한 궤적을 만듭니다.
같은 검색어로 문서를 세 번 찾은 뒤 출처를 확인하고, 답은 기준과 같은 글입니다.
도구를 필요 없이 더 부른 낭비 장면입니다."""),
        code(WASTEFUL),
        md("""**결과 읽기** — 라벨 `도구 차례:` 뒤에 `'search_documents'`가 셋, `'check_source'`가 하나 있습니다.
출력 줄 `도구 요청 수: 4 | 메시지 수: 10`으로, 기준 궤적보다 도구 요청이 둘, 메시지가 넷 늘었습니다.

다음 셀은 도구 요청은 기준과 같고 답 글만 틀린 궤적을 만듭니다.
답 글에는 14일이 아니라 7일이라고 적습니다."""),
        code(WRONG),
        md("""**결과 읽기** — 출력 줄 `도구 차례: ['search_documents', 'check_source']`는 기준 궤적과 같습니다.
출력 줄 `최종 답: 일반 도서는 7일 동안 빌릴 수 있습니다.`는 기준 답과 다릅니다.
도구를 바르게 부르고도 답을 틀리게 쓴 장면입니다.

다음 셀은 도구 차례를 바꾼 궤적을 만듭니다.
출처 확인을 먼저 하고 검색을 뒤에 하며, 답은 기준과 같은 글입니다."""),
        code(REVERSED),
        md("""**결과 읽기** — 출력 줄 `도구 차례: ['check_source', 'search_documents']`가 보입니다.
도구 둘은 기준 궤적과 같고, 차례만 거꾸로입니다.

## 5. 세 평가로 궤적 넷 견주기

다음 셀은 궤적 넷을 이름과 함께 딕셔너리에 모으고, 궤적마다 세 평가 결과를 한 줄씩 출력합니다.
네 궤적 모두 같은 기준 궤적, 같은 평가 함수와 견줍니다.
실행 전에 예상해 봅니다.
어느 궤적에서 어느 평가가 거짓을 낼까요?"""),
        code(TABLE),
        md("""**결과 읽기** — 줄 `기준과 같음 | True | True | True`는 세 평가가 모두 참입니다.
줄 `검색 세 번 | True | True | False`에서는 궤적 평가만 거짓입니다.
줄 `답만 틀림 | False | True | True`에서는 최종 답 평가만 거짓입니다.
줄 `차례 바꿈 | True | False | False`에서는 한 단계 평가와 궤적 평가가 거짓입니다.

세 평가가 거짓을 낸 궤적이 서로 다릅니다.
답만 보는 평가는 낭비와 차례를 보지 못했고, 차례를 보는 평가는 틀린 답을 보지 못했습니다.

다음 셀은 이 결과를 궤적 쪽에서 다시 읽습니다.
궤적마다 거짓을 낸 평가의 이름만 모읍니다."""),
        code(FAILED),
        md("""**결과 읽기** — 줄 `검색 세 번 | 거짓을 낸 평가: ['궤적']`과 `답만 틀림 | 거짓을 낸 평가: ['최종 답']`이 보입니다.
이 두 궤적은 평가 하나만 문제를 찾았습니다.
그 평가를 빼면 두 궤적의 문제는 판정에 드러나지 않습니다.
줄 `차례 바꿈 | 거짓을 낸 평가: ['한 단계', '궤적']`에서는 두 평가가 함께 찾았습니다.

다음 셀은 한 단계 평가가 본 자리, 곧 궤적마다 첫 모델 응답의 도구 요청만 꺼내 봅니다.
메시지 목록의 1번 자리가 첫 모델 응답입니다."""),
        code(FIRST_STEPS),
        md("""**결과 읽기** — 줄 `차례 바꿈 | 첫 응답의 도구 요청: ['check_source']`만 기준과 다르고, 나머지 세 줄은 `['search_documents']`입니다.
검색 세 번 궤적도 첫 응답은 기준과 같아, 한 단계 평가는 참을 냈습니다.
낭비는 둘째·셋째 응답에서 일어났고, 이 함수는 그 자리를 보지 않습니다.

이 네 궤적에서는 한 단계 평가가 거짓이면 궤적 평가도 거짓이었습니다.
모드 `strict`는 첫 응답의 도구 요청까지 기준과 견주기 때문입니다.
대신 한 단계 평가는 문제가 난 자리가 첫 응답이라는 것을 짚어 줍니다.

다음 셀은 답만 틀린 궤적을 기준 궤적과 견줘, 궤적 평가가 왜 참을 냈는지 봅니다.
메시지 수, 도구 차례, 최종 답을 차례로 견줍니다."""),
        code(WHY_WRONG),
        md("""**결과 읽기** — 출력 줄 `메시지 수가 같은가: True`와 `도구 차례가 같은가: True`, `최종 답이 같은가: False`가 보입니다.
두 궤적은 마지막 메시지의 글만 다릅니다.
모드 `strict`는 메시지 수와 역할, 도구 요청을 견주고, 메시지 글은 견주지 않습니다.
그래서 틀린 답을 쓴 궤적도 궤적 평가를 통과했습니다.

설치판 agentevals 0.0.9 소스 `trajectory/strict.py` 20~76행에도 메시지 글을 견주는 줄이 없습니다.
LangChain 문서도 이 모드에서 메시지 글은 달라도 된다고 적습니다.

## 6. 값 바꿔 보기: 답 글 하나만 바꾸기

값 하나만 바꿔 봅니다.
바꿀 값은 답만 틀린 궤적의 답 글이고, 뜻이 맞는 다른 글 「14일 동안 빌릴 수 있습니다.」를 넣습니다.
도구 요청 목록은 그대로 둡니다.
실행 전에 예상해 봅니다.
답이 맞게 바뀌었으니 최종 답 평가는 참이 될까요?"""),
        code(REWORDED),
        md("""**결과 읽기** — 출력 줄 `기준 답: 일반 도서는 14일 동안 빌릴 수 있습니다.`와 `바꾼 답: 14일 동안 빌릴 수 있습니다.`가 보입니다.
뜻은 같지만 앞의 「일반 도서는」이 빠져 글자가 다릅니다.

다음 셀은 바꾼 궤적과 답만 틀린 궤적의 세 평가 결과를 나란히 봅니다."""),
        code(COMPARE),
        md("""**결과 읽기** — 라벨 `답 글을 바꿈:` 뒤 딕셔너리에서도 `'최종 답': False`입니다.
출력 줄 `두 줄이 같은가: True`로, 답이 틀린 궤적과 뜻이 맞는 궤적의 세 판정이 같았습니다.
최종 답 평가는 글자로 견줘서, 틀린 답과 말만 다른 맞는 답을 가르지 못했습니다.
나머지 두 평가는 답 글을 보지 않아 두 궤적 모두 참입니다.

뜻이 같은지 보려면 코드 규칙 대신 글을 읽고 판정하는 쪽이 필요합니다.
Ch 15 01절의 평가 모델(judge)이 그런 쪽이고, 03절에서 궤적을 평가 모델로 판정합니다.

## 정리

1. 같은 기준 궤적과 견줘도, 검색 세 번은 궤적 평가만, 답만 틀림은 최종 답 평가만 거짓을 냈습니다.
2. 차례 바꿈은 한 단계 평가와 궤적 평가가 함께 거짓을 냈고, 한 단계 평가는 문제가 첫 응답에 있음을 짚었습니다.
3. 모드 `strict`는 메시지 글을 보지 않고, 글자로 견주는 최종 답 평가는 뜻이 같은 다른 글을 거짓으로 봤습니다.

02절에서는 모드 `strict` 말고 모드 셋을 더 보고, 네 모드가 차례와 빠진 요청·더한 요청을 어떻게 달리 보는지 견줍니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
def table_html(head: list, rows: list) -> str:
    head_html = ""
    for value in head:
        head_html = head_html + "<th>" + value + "</th>"
    body = ""
    for row in rows:
        cells_html = ""
        for value in row:
            cells_html = cells_html + "<td>" + value + "</td>"
        body = body + "<tr>" + cells_html + "</tr>"
    return "<table><thead><tr>" + head_html + "</tr></thead><tbody>" + body + "</tbody></table>"


def html_text(text: str) -> str:
    """노트북용 마크다운 한 단락(백틱·줄바꿈)을 _src 문단 글로 바꿉니다(Ch 27·28 생성기와 같은 함수)."""
    parts = text.replace("\n", " ").split("`")
    out = ""
    for index in range(len(parts)):
        if index % 2 == 1:
            out = out + "<code>" + parts[index] + "</code>"
        else:
            out = out + parts[index]
    return out


def mermaid_block(name: str, alt: str, caption: str, reading: str) -> str:
    return ("{{mermaid:" + name + "|" + alt + "|" + caption + "}}\n"
            + '<p class="look"><b>도식 읽기</b> — ' + html_text(reading) + "</p>\n")


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


L_CH15_01 = "../../part4/ch15-evaluation-advanced/01-실패-로그와-평가-대상.html"
L_CH16_03 = "../../part4/ch16-guardrails/03-히스토리-트리밍과-요약.html"
L_CH17_04 = "../../part5/ch17-agent-overview/04-자율성의-대가.html"
L_CH18_05 = "../../part5/ch18-workflow-patterns/05-생성자-평가자와-정지-조건.html"
L_CH19_04 = "../../part5/ch19-model-tools/04-설명만으로-도구-선택하기.html"
L_CH19_06 = "../../part5/ch19-model-tools/06-오류와-읽기-쓰기-분리.html"
L_CH20_01 = "../../part5/ch20-tool-node/01-ToolNode와-tools-condition.html"
L_CH21_05 = "../ch21-create-agent/05-retriever를-도구로-전환.html"
L_CH21_06 = "../ch21-create-agent/06-같은-평가셋으로-RAG-비교.html"
L_CH28_06 = "../ch28-mcp/06-MCP-실습.html"
L_02 = "02-궤적-매칭-네-모드.html"
L_03 = "03-LLM-judge로-궤적-평가.html"

TERM_ROWS = [
    ("궤적(trajectory)", "에이전트가 질문에서 최종 답까지 밟은 단계의 차례입니다. <a href=\"" + L_CH17_04 + "\">Ch 17 04절</a>의 단계 차례(궤적)를 이어 쓰는 말입니다. 시험 풀이 과정처럼, 답에 닿기까지 무엇을 어떤 차례로 했는지 남은 기록입니다. 이 절에서는 도구 호출 요청·도구 결과·답까지 든 메시지 목록이고, 도구 이름만 모은 도구 차례는 <code>['search_documents', 'check_source']</code>처럼 꺼냅니다."),
    ("기준 궤적(reference trajectory)", "좋은 에이전트라면 밟을 것이라고 사람이 미리 적어 둔 궤적입니다. 시험의 모범 풀이와 같습니다. 이 절에서는 검색 한 번, 출처 확인 한 번 뒤에 답하는 목록 <code>reference</code>이고, 메시지는 여섯입니다."),
    ("최종 답 평가(final response)", "에이전트 안에서 일어난 일은 보지 않고 마지막 답만 판정합니다. 시험지의 마지막 답 칸만 채점하는 것과 같습니다. 이 절에서는 함수 <code>final_answer_pass</code>가 마지막 글이 기준 답과 글자까지 같은지 봅니다."),
    ("한 단계 평가(single step)", "궤적의 한 단계만 떼어 판정합니다. 풀이의 첫 줄만 맞았는지 보는 것과 같습니다. 이 절에서는 함수 <code>first_step_pass</code>가 첫 모델 응답이 요청한 도구 이름을 기준과 견줍니다."),
    ("궤적 평가(trajectory)", "에이전트가 밟은 모든 단계를 판정합니다. 풀이 과정 전체를 모범 풀이와 줄마다 견주는 것과 같습니다. 이 절에서는 함수 <code>trajectory_pass</code>가 궤적 맞춰 보기 평가 함수에 판정을 맡깁니다."),
    ("궤적 맞춰 보기(trajectory match) · 모드 <code>strict</code>", "실제 궤적을 기준 궤적과 코드 규칙으로 맞춰 보는 방법이고, 궤적 가운데 도구 호출 요청을 견줍니다. 모드 <code>strict</code>는 메시지의 수·역할·차례와 도구 요청의 이름·인자가 모두 같아야 참이고, 메시지 글은 견주지 않습니다. 두 풀이의 줄 수와 줄마다 쓴 공식은 보되, 계산해 적은 값은 보지 않는 채점과 같습니다. 이 절에서는 인자 <code>trajectory_match_mode=\"strict\"</code>로 만든 <code>strict_match</code>입니다."),
]

RESULT_ROWS = [
    ("기준과 같음", "<code>search_documents</code> → <code>check_source</code>", "기준과 같은 글", "<code>True</code>", "<code>True</code>", "<code>True</code>"),
    ("검색 세 번", "<code>search_documents</code> 셋 → <code>check_source</code>", "기준과 같은 글", "<code>True</code>", "<code>True</code>", "<code>False</code>"),
    ("답만 틀림", "<code>search_documents</code> → <code>check_source</code>", "「일반 도서는 7일 동안 빌릴 수 있습니다.」", "<code>False</code>", "<code>True</code>", "<code>True</code>"),
    ("차례 바꿈", "<code>check_source</code> → <code>search_documents</code>", "기준과 같은 글", "<code>True</code>", "<code>False</code>", "<code>False</code>"),
    ("답 글을 바꿈(값 바꿔 보기)", "<code>search_documents</code> → <code>check_source</code>", "「14일 동안 빌릴 수 있습니다.」", "<code>False</code>", "<code>True</code>", "<code>True</code>"),
]

LOOK_B5 = "노트북 2절에서 <code>기준 궤적의 메시지 수: 6</code>과 <code>도구 요청 수: 2</code>를 봅니다. 3절에서 결과 딕셔너리의 <code>'score': True</code>를 확인합니다. 4절에서는 <code>도구 요청 수: 4 | 메시지 수: 10</code>과 <code>최종 답: 일반 도서는 7일 동안 빌릴 수 있습니다.</code>를 찾습니다. 5절 첫 셀에서 네 줄의 <code>True</code>·<code>False</code>를 확인합니다."
LOOK_B6 = "노트북 5절 둘째 셀에서 <code>검색 세 번 | 거짓을 낸 평가: ['궤적']</code>과 <code>답만 틀림 | 거짓을 낸 평가: ['최종 답']</code>을 확인합니다. 6절 마지막 셀에서 <code>두 줄이 같은가: True</code>를 봅니다. 모델을 부르지 않으므로, 다시 실행해도 같은 값이 나와야 합니다."


def runs_paragraph() -> str:
    if not RUNS_SENTENCE:
        return ""
    return "<p>" + RUNS_SENTENCE + "</p>\n"


def src_html() -> str:
    terms = table_html(["말", "뜻"], TERM_ROWS)
    results = table_html(["궤적", "도구 차례", "최종 답 글", "최종 답 평가", "한 단계 평가", "궤적 평가"], RESULT_ROWS)
    return """<!--meta: 강의 0.75h | 실습 1.25h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 5 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>최종 답 평가·한 단계 평가·궤적 평가가 궤적의 어느 자리를 보는지 말할 수 있습니다.</li>
<li>같은 기준 궤적과 견준 궤적 넷에서, 평가마다 거짓을 낸 궤적이 다름을 출력으로 설명할 수 있습니다.</li>
<li>모드 <code>strict</code>는 메시지 글을 보지 않고, 글자로 견주는 최종 답 평가는 뜻을 가르지 못함을 말할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_CH28_06 + """\">Ch 28 06절</a> 끝에서 예고한 것처럼, 이 챕터는 에이전트를 평가하는 방법을 배웁니다. 에이전트는 답을 내기 전에 도구를 여러 번 고르고 부릅니다. 그래서 답이 맞아도 도구를 필요 없이 더 불렀을 수 있고, 도구 차례가 맞아도 답이 틀릴 수 있습니다. 이 절은 평가 방법 세 가지를 견주고, 어느 하나가 다른 둘을 대신하지 못하는 장면을 출력으로 봅니다.</p><p>세 방법은 LangSmith 문서가 에이전트 평가 방법으로 적은 최종 답 평가·한 단계 평가·궤적 평가입니다. 이 절은 모델을 부르지 않고, 에이전트가 도구를 부른 것처럼 메시지 목록을 코드로 적습니다. 그래서 같은 궤적에는 늘 같은 판정이 나옵니다. 실제 에이전트를 실행해 만든 궤적은 <a href=\"""" + L_03 + """\">03절</a>에서 평가합니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH17_04 + """\">Ch 17 04절</a>에서는 실행 기록에 적힌 단계를 일어난 차례대로 늘어놓은 것을 단계 차례(궤적)라고 불렀습니다. 그 절은 단계 차례를 맞춰 보는 평가를 이 챕터 02절에서 다룬다고 예고했습니다. 이 절은 그 앞에서, 궤적을 포함한 평가 방법 셋을 먼저 견줍니다.</p><p><a href=\"""" + L_CH19_04 + """\">Ch 19 04절</a>에서는 모델 응답의 도구 호출 요청이 칸 넷(<code>name</code>·<code>args</code>·<code>id</code>·<code>type</code>)을 가진다는 것을 봤습니다. 같은 절에서 함수 <code>tool_call_names</code>로 도구 이름을 꺼냈습니다. <a href=\"""" + L_CH19_06 + """\">06절</a>에서는 함수 <code>show_messages</code>로 메시지 목록을 한 줄씩 봤습니다. <a href=\"""" + L_CH20_01 + """\">Ch 20 01절</a>에서는 모델을 부르지 않고 도구 호출 요청을 담은 모델 응답을 손으로 만들었습니다. 이 절의 궤적도 같은 방법으로 적고, 두 함수는 도구 파일에서 가져옵니다.</p><p><a href=\"""" + L_CH15_01 + """\">Ch 15 01절</a>에서는 다른 모델이 쓴 답을 읽고 판정하는 평가 모델(judge)을 배웠습니다. <a href=\"""" + L_CH18_05 + """\">Ch 18 05절</a>에서는 모델을 부르지 않고 코드 규칙으로 초안을 가리는 코드 검사를 썼습니다. 이 절의 세 평가는 모두 코드 규칙이고, 평가 모델은 03절에서 씁니다.</p><p><a href=\"""" + L_CH21_06 + """\">Ch 21 06절</a>에서는 고정 흐름과 에이전트 흐름의 답을 판정했습니다. 근거 충실도 판정이 여섯 사례 모두 1이라, 그 조건에서는 판정으로 두 흐름을 가를 수 없었습니다. 답을 보는 판정만으로는 말할 수 없는 것이 있을 수 있어, 이 절은 궤적의 다른 자리를 보는 평가를 함께 봅니다. 도구 이름 <code>search_documents</code>는 <a href=\"""" + L_CH21_05 + """\">Ch 21 05절</a>의 검색 도구 이름을 빌렸습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>오르골은 종이띠에 뚫린 구멍을 차례대로 읽어 곡을 냅니다. 곡이 맞게 나오는지 보는 방법은 여럿입니다. 곡의 끝 소리만 들어 볼 수도 있고, 띠의 첫 구멍만 확인할 수도 있습니다. 악보대로 뚫은 기준 띠를 옆에 두고, 띠 전체를 나란히 대 볼 수도 있습니다.</p><p>구멍을 차례대로 읽어 끝 소리까지 내는 띠 한 줄이 궤적이고, 곡의 끝 소리가 최종 답입니다. 끝 소리만 듣는 것이 최종 답 평가, 첫 구멍만 보는 것이 한 단계 평가입니다. 기준 띠와 나란히 대 보는 것이 궤적 평가입니다. 구멍이 몇 개 더 뚫려 있어도 끝 소리는 같을 수 있어서, 끝 소리만 들어서는 띠의 차이를 모릅니다.</p><p>비유와 다른 점이 있습니다. 오르골은 구멍이 같으면 소리도 같지만, 에이전트는 도구를 같은 차례로 불러도 답 글을 다르게 쓸 수 있습니다. 이 절의 「답만 틀림」 궤적이 그런 경우입니다. 또 이 절의 궤적은 에이전트가 만든 것이 아니라 코드로 적은 것입니다.</p>
""" + illustration_block() + """<h3>궤적과 기준 궤적</h3><p>에이전트가 질문에서 최종 답까지 밟은 단계의 차례를 궤적이라고 부릅니다. 이 챕터는 질문·모델 응답·도구 결과·마지막 답을 일어난 차례대로 담은 메시지 목록으로 궤적을 적습니다. 모델 응답 안의 도구 호출 요청에서 도구 이름만 차례대로 모은 목록은 도구 차례라고 부릅니다. 궤적 맞춰 보기의 모드는 이 메시지 목록 가운데 도구 호출 요청을 견줍니다.</p><p>기준 궤적은 좋은 에이전트라면 밟을 것이라고 사람이 미리 적어 둔 궤적입니다. 궤적을 평가할 때는 실제 궤적을 이 기준과 견줍니다. 이 절의 기준 궤적은 문서를 한 번 검색하고 출처를 한 번 확인한 뒤 답하는 차례이고, 흐름을 보여 주려고 정한 예입니다.</p>
""" + terms + """
<p>새 말을 이 절 코드에서 보면 이렇습니다. 기준 궤적은 <code>기준 궤적의 도구 차례: ['search_documents', 'check_source']</code>로 출력됩니다. 세 평가는 함수 <code>final_answer_pass</code>·<code>first_step_pass</code>·<code>trajectory_pass</code>이고, 셋 모두 <code>True</code>나 <code>False</code>를 내놓습니다.</p>
<h3>세 평가가 보는 자리</h3><p>LangSmith 문서는 에이전트 평가 방법을 셋으로 적습니다. 최종 답 평가는 에이전트 안에서 일어난 일은 보지 않고 마지막 답만 봅니다. 문서는 이 방법이 과제를 해냈는지 바로 보지만, 실패했을 때 원인을 찾기 어렵다고 적습니다. 한 단계 평가는 도구를 맞게 골랐는지처럼 한 단계만 떼어 봅니다. 빠르고 문제 자리를 짚지만, 에이전트 전체를 보지는 않습니다.</p><p>궤적 평가는 에이전트가 밟은 모든 단계를 봅니다. 이 절은 궤적 평가에 설치판 agentevals의 궤적 맞춰 보기를 쓰고, 모드는 <code>strict</code> 하나만 씁니다. 모드 <code>strict</code>는 메시지의 수·역할·차례와 도구 요청의 이름·인자가 모두 기준과 같아야 참을 냅니다. 메시지 글은 견주지 않습니다. 모드는 셋이 더 있고, <a href=\"""" + L_02 + """\">02절</a>에서 넷을 견줍니다.</p><p>최종 답 평가는 흔히 평가 모델이 답을 읽고 판정합니다. 이 절은 모델을 부르지 않으므로, 마지막 글이 기준 답과 글자까지 같은지를 코드로 봅니다. 한 단계 평가도 첫 모델 응답이 요청한 도구 이름만 코드로 견줍니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 질문·기준 답·도구 결과 글을 정하고, 궤적을 만드는 함수로 기준 궤적을 만듭니다. 3절은 세 평가 함수를 정의하고, 라이브러리로 모드 <code>strict</code>의 평가 함수를 만듭니다. 4절은 견줄 궤적 넷을 만들고, 5절은 넷을 세 평가로 견줍니다. 6절은 답 글 하나만 바꾼 궤적으로 다시 견줍니다.</p><p>모델 요청은 0번이고, API 키 없이 실행합니다. 궤적은 모두 코드로 적은 메시지 목록이라, 다시 실행해도 같은 판정이 나옵니다. 읽는 파일은 도구 파일 <code>eval_tools.py</code> 하나이고 쓰는 파일은 없습니다. 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>궤적 넷을 같은 기준 궤적과 견주자, 평가마다 거짓을 낸 궤적이 달랐습니다. 검색 세 번 궤적은 궤적 평가만, 답만 틀린 궤적은 최종 답 평가만 거짓이었습니다. 차례를 바꾼 궤적은 한 단계 평가와 궤적 평가가 함께 거짓이었습니다. 기준과 같은 궤적은 세 평가 모두 참이었습니다.</p>
<p>아래 표는 노트북 4~6절 출력을 모은 것입니다. 맨 아래 줄은 6절에서 답 글 하나만 바꾼 궤적입니다.</p>
""" + results + """
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>한 평가만 문제를 찾은 궤적이 둘이었습니다. 그 평가를 빼면 두 궤적의 문제는 판정에 드러나지 않습니다. 그래서 세 평가는 서로를 대신하지 못하고, 찾으려는 실패에 맞춰 함께 씁니다. 이 네 궤적에서는 한 단계 평가가 거짓이면 궤적 평가도 거짓이었습니다. 그래도 한 단계 평가는 문제가 첫 응답에 있다는 자리를 짚었습니다.</p><p>답 글 하나만 뜻이 맞는 다른 글로 바꾸자, 최종 답 평가는 여전히 거짓이었습니다. 틀린 답과 말만 다른 맞는 답을 글자 규칙이 가르지 못한 것입니다. 나머지 두 평가는 답 글을 보지 않아 두 궤적 모두 참이었습니다. 뜻을 보는 판정은 03절의 평가 모델 몫입니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + runs_paragraph() + """<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>이 절의 궤적은 모두 코드로 적은 메시지 목록입니다. 도구 <code>search_documents</code>·<code>check_source</code>의 함수는 만들지 않았고, 결과 글도 이 절이 정했습니다. 실제 에이전트가 만든 궤적을 평가하는 장면은 03절에서 봅니다.</li><li>기준 궤적과 견줄 궤적 넷은 세 평가의 차이를 보여 주려고 정한 예입니다. 실제 에이전트가 이런 궤적을 얼마나 자주 만드는지는 이 절이 보여 주지 않습니다.</li><li>모드 <code>strict</code>가 메시지 글을 견주지 않는다는 것은 5절 출력과 설치판 소스로 확인했습니다. 노트북 밖에서는 질문 글, 도구 결과 글, 호출 ID만 바꾼 궤적도 참이 나오는 것을 봤습니다. 이 셋은 노트북에서는 실행하지 않았습니다.</li><li>최종 답을 글자로 견주면, 뜻이 같은 다른 글도 거짓이 됩니다. 이 절은 모델 없이 차이를 보이려고 이 규칙을 골랐습니다. LangSmith 문서는 최종 답 평가에 알맞은 판정 기준을 정하기 어려울 때가 있다고 적습니다.</li><li>한 단계 평가는 이 절에서 첫 모델 응답의 도구 이름만 봤습니다. 다른 단계나 도구 인자를 보는 한 단계 평가도 만들 수 있지만, 이 절에서는 실행하지 않았습니다.</li><li>LangChain 문서의 결과 딕셔너리 예시에는 칸이 셋입니다. 설치판 agentevals 0.0.9 출력에는 칸 <code>metadata</code>가 하나 더 있습니다. 이 절은 칸 <code>score</code>만 썼습니다.</li><li>설치판 평가 함수는 openevals <code>utils.py</code> 203행에서 LangSmith 기록 장치로 감싸여 있습니다. 교재 출력을 만든 환경에는 LangSmith 설정 환경 변수가 없었고, 이 절은 LangSmith 기록을 다루지 않습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>같은 기준 궤적과 견줘도, 검색 세 번은 궤적 평가만, 답만 틀림은 최종 답 평가만 거짓을 냈습니다.</li><li>차례 바꿈은 한 단계 평가와 궤적 평가가 함께 거짓을 냈고, 한 단계 평가는 문제가 첫 응답에 있음을 짚었습니다.</li><li>모드 <code>strict</code>는 메시지 글을 보지 않고, 글자로 견주는 최종 답 평가는 뜻이 같은 다른 글을 거짓으로 봤습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_02 + """\">02절</a>에서는 모드 <code>strict</code> 말고 모드 셋을 더 봅니다. 네 모드가 차례와 빠진 요청·더한 요청을 어떻게 달리 보는지 견줍니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 검색 세 번 궤적에서 거짓을 낸 평가는 무엇이고, 최종 답 평가는 왜 참이었나요?</p><p class="quiz-a">궤적 평가만 거짓이었습니다. 답 글이 기준과 같았고, 최종 답 평가는 마지막 글만 보기 때문입니다. 틀렸다면 노트북 5절 첫 셀을 다시 읽습니다.</p><p class="quiz-q">2. 답만 틀린 궤적을 모드 <code>strict</code>가 참으로 본 까닭은 무엇인가요?</p><p class="quiz-a">메시지 수와 도구 차례가 기준과 같았고, 이 모드는 메시지 글을 견주지 않기 때문입니다. 틀렸다면 노트북 5절 넷째 셀을 다시 읽습니다.</p><p class="quiz-q">3. 차례 바꿈 궤적에서 한 단계 평가가 거짓을 낸 까닭은 무엇이고, 그 판정은 무엇을 알려 주나요?</p><p class="quiz-a">첫 모델 응답이 <code>search_documents</code>가 아니라 <code>check_source</code>를 요청했기 때문입니다. 문제가 난 자리가 첫 응답이라는 것을 알려 줍니다. 틀렸다면 노트북 5절 셋째 셀을 다시 읽습니다.</p><p class="quiz-q">4. 동료가 「최종 답 평가가 거짓이면 답이 틀린 것」이라고 말합니다. 이 절의 최종 답 평가에서 맞는 말인가요?</p><p class="quiz-a">맞지 않습니다. 6절에서 뜻이 맞는 「14일 동안 빌릴 수 있습니다.」도 글자가 달라 거짓이었습니다. 이 규칙은 글자를 견줄 뿐 뜻을 보지 않습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/langsmith/evaluation-approaches">LangSmith Evaluation approaches</a></div>확인 2026-09-29 · 에이전트 평가 방법 셋(최종 답·한 단계·궤적)의 입력·출력과 장단점을 적습니다. 최종 답 평가는 안쪽을 보지 않아 실패 원인을 찾기 어렵다고 적습니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langchain/test/evals">LangChain Agent evals</a></div>확인 2026-09-29 · 궤적 맞춰 보기 모드 넷과 결과 딕셔너리 예시를 적습니다. 모드 <code>strict</code>는 메시지 글이 달라도 된다고 적습니다.</li><li><div><a href="https://docs.langchain.com/langsmith/trajectory-evals">LangSmith Trajectory evals</a></div>확인 2026-09-29 · 모드 <code>strict</code>가 같은 차례·같은 도구 요청을 보되 메시지 글의 차이는 허용한다고 적습니다. 기본으로는 같은 도구에 같은 인자를 준 요청만 같다고 봅니다.</li><li><div><a href="https://pypi.org/project/agentevals/">agentevals (PyPI)</a></div>확인 2026-09-29 · 가장 새 판이 0.0.9(2025-07-24)입니다. 이 절의 잠금 판과 같습니다.</li><li>설치판 agentevals 0.0.9 소스 <code>trajectory/match.py</code> 24~109행은 평가 함수를 만드는 함수이고, 기본 모드는 <code>strict</code>입니다. <code>trajectory/strict.py</code> 20~76행은 메시지 수·역할·도구 요청을 견주는 규칙이고, 메시지 글을 견주는 줄은 없습니다.</li><li>설치판 openevals 0.2.0 소스 <code>utils.py</code> 203행은 평가 함수를 LangSmith 기록 장치로 감싸는 줄입니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    check_tools()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "eval_tools.py").write_text(TOOLS_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        # 도구 파일은 없거나 이 판과 같을 때만 쓴다. 뒤 절이 함수를 더한 판이면 덮어쓰지 않는다(Ch 24 마감 A-10·Ch 25~28 교훈).
        current = ""
        if TOOLS_PATH.is_file():
            current = TOOLS_PATH.read_text(encoding="utf-8")
        plain = strip_later_imports(current)
        assert current == "" or plain.startswith(TOOLS), "도구 파일이 01절 판으로 시작하지 않습니다"
        if current == "" or current == TOOLS:
            TOOLS_PATH.write_text(TOOLS, encoding="utf-8")
            print("wrote", TOOLS_PATH)
        else:
            print("skip", TOOLS_PATH, "(뒤 절이 함수를 더한 판 — 덮어쓰지 않음)")
        path = write_notebook(LAB, "01", SLUG, "experiment", cells())
        print("wrote", path)
