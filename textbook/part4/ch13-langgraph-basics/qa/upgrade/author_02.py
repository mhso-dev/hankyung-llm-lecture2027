"""Ch 13 02절 품질 개선본 노트북 생성기 (QUALITY-UPGRADE.md §2·§3·§6).

사용: python3 author_02.py → labs/part4/ch13-langgraph-basics/notebooks/02-State-갱신.ipynb 를 새로 쓴다.
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북은 qa/upgrade/before/notebooks/ 에 있다. **experiment 형식 유지**(chapter.json).

## §2-7 리팩터 (2026-09-21)

- 01절 출력 함수 `print_state`는 다시 정의하지 않고 도구 파일 `notebooks/rag_tools.py`에서 가져온다(규격 §2-7).
  도구 파일이 NumPy를 불러오므로 설치 셀에 `numpy==2.5.3`(실습 폴더 잠금과 같은 판)을 더했다.
- 상태 형식 `FlowState`는 7절 `RuleState`와 나란히 견주는 이 절의 학습 내용이라 노트북에 그대로 둔다.
- 노드 `normalize`·`make_query`는 이 절이 처음 가르치는 판(자기 이름만 냄)이라 노트북에 둔다. 03·06·08절은 도구 파일에서 가져간다.

## 01절에서 그대로 이어받은 것 (qa/upgrade/handoff.md 「§01 → §02」)

- 상태 형식 이름 `FlowState`, 칸 `question`·`query`·`trace`, 노드 이름 `normalize`·`make_query`.
- 질문 `"  대출 기간은 며칠인가요?  "`(글자 수 17), 검색어 칸 결과 `대출 기간은 며칠`.
- 출력 함수 `print_state(label, state)`(라벨 줄 + 칸 세 줄), 기록 함수 `run_row(run_name, state)`.
- 01절 b7·노트북 정리가 넘긴 약속: 「칸마다 합치는 규칙을 상태에 적어 두는 방법은 02절에서 배웁니다」.
- 용어 「칸」(Ch 9~12에서 이어 씀), 「조각」은 Ch 5 토큰 뜻 전용이라 쓰지 않는다. 「갱신」 = 노드가 내놓는 딕셔너리 하나.

## 이 절이 새로 여는 것

- 표시 `Annotated`(`typing`)와 함수 `operator.add` — Part 1~3에서 0건이라 뜻 → 일상 예 → 코드 세 문장으로 푼다.
- 리듀서: 칸의 지금 값과 새 갱신을 받아 그 칸의 다음 값을 만드는 함수.
- `Annotated[list[str], operator.add]`를 적은 상태 형식 `RuleState`.

## 선택한 것과 까닭

1. **모델 요청 0번.** 상태 갱신 규칙이 주제라 모델이 필요 없다(01절과 같음, 규격 §3·AGENT-BRIEF).
   API 키 셀을 두지 않고 설치도 `langgraph==1.2.11` 하나만 한다.
2. **바꾸는 값을 하나로 좁힌다.** 노드 함수 `normalize`·`make_query`를 한 벌만 정의하고,
   **상태 형식만 바꿔**(`FlowState` → `RuleState`) 두 번 실행한다. 두 실행의 차이는 칸에 적은 규칙 하나뿐이다.
   옛 노트북은 상태 이름 `UpdateState`, 칸 `query`·`log`, 노드 `normalize`·`expand`로 01절과 이름이 어긋났다.
   01절 이름을 그대로 쓰고 옛 `log` 칸은 `trace`로 맞췄다(handoff 2항, 까닭은 02-diagnosis.md §3).
3. **덮어쓰기를 실행으로 보여 준다.** 옛 본문은 「리듀서가 없는 키는 덮어쓴다」를 문장으로만 적고
   노트북은 리듀서를 붙인 그래프 하나만 실행했다. 이 판은 규칙이 없는 칸을 먼저 실행해
   `['make_query']` 하나만 남는 것을 출력으로 확인한 뒤 규칙을 적는다.
4. **중복도 실행으로 보여 준다.** 옛 본문 주의 메모 「노드가 기존 목록을 다시 포함하면 중복될 수 있습니다」를
   9절에서 실제로 만든다. 01절 노드(앞 흔적까지 내놓는 판)를 규칙 적은 칸에 그대로 쓰면
   `['normalize', 'normalize', 'make_query']`가 된다. 01절 코드와 02절 코드의 차이를 이 자리에서 잇는다.
5. **`assert`는 코드가 정하는 값에만.** 모델을 부르지 않으므로 모델 답 `assert`는 0건이다.
6. **파일을 쓰지 않는다.** `runs/`에 아무것도 쓰지 않고 읽지도 않는다.
7. **쓰지 않은 것**: `lambda`·내포식·조건 표현식·f-string·`key=`·`reverse=`·세미콜론·한 줄 복합문·
   numpy·sklearn·`list()`·`enumerate`·`zip`·`join`. 부른 내장 이름은 `len`·`print`·`type`뿐이다(01절과 같음).

## 탐색 실행에서 확인한 값 (2026-09-19, /tmp/ch13-02/probe1.py)

langgraph 1.2.11 · langchain-core 1.6.2 · Python 3.12.13. 규칙이 없는 칸은 마지막 갱신만 남겨 `['make_query']`,
규칙을 적은 칸은 `['normalize', 'make_query']`. 처음 실행 흔적에 `['input']`을 넣으면 `['input', 'normalize',
'make_query']`로 처음 값이 지켜진다. 01절 노드를 규칙 적은 칸에 그대로 쓰면 `['normalize', 'normalize',
'make_query']`로 이름 하나가 겹친다. 같은 코드를 두 번 돌려 모든 출력이 같았다.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part4/ch13-langgraph-basics/notebooks"

INSTALL = install_source(["langgraph==1.2.11", "numpy==2.5.3"])

IMPORTS = r'''# 01절에서 쓴 이름 네 개에 규칙을 적는 데 쓸 이름 두 개를 더해 불러옵니다
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
# 01절에서 만든 출력 함수를 도구 파일에서 가져옵니다
from rag_tools import print_state

print("불러온 이름:", "operator", "Annotated", "TypedDict", "StateGraph", "START", "END")'''

VALUES = r'''# 01절에서 쓴 첫 질문과 이 절에서 넣어 볼 처음 실행 흔적을 정합니다
first_question = "  대출 기간은 며칠인가요?  "
started_trace = ["input"]
print("첫 질문:", first_question)
print("첫 질문의 글자 수:", len(first_question))
print("나중에 넣어 볼 처음 실행 흔적:", started_trace)'''

FLOW_STATE = r'''# 01절에서 적은 규칙 없는 상태 형식을 이 절에서도 먼저 씁니다
class FlowState(TypedDict):
    question: str
    query: str
    trace: list[str]'''

NORMALIZE = r'''# 질문 칸의 앞뒤 빈칸을 없애고 실행 흔적에는 자기 이름만 담아 냅니다
def normalize(state):
    clean_question = state["question"].strip()
    return {"question": clean_question, "trace": ["normalize"]}'''

MAKE_QUERY = r'''# 물음표와 맺음말을 지워 검색어를 만들고 실행 흔적에는 자기 이름만 담아 냅니다
def make_query(state):
    without_mark = state["question"].replace("?", "")
    plain = without_mark.replace("인가요", "")
    return {"query": plain.strip(), "trace": ["make_query"]}'''

BUILD_PLAIN = r'''# 규칙이 없는 상태 형식으로 노드 두 개와 엣지 세 개를 적어 컴파일합니다
plain_builder = StateGraph(FlowState)
plain_builder.add_node("normalize", normalize)
plain_builder.add_node("make_query", make_query)
plain_builder.add_edge(START, "normalize")
plain_builder.add_edge("normalize", "make_query")
plain_builder.add_edge("make_query", END)
plain_graph = plain_builder.compile()
print("등록한 노드 수:", len(plain_builder.nodes))
print("컴파일 결과의 종류:", type(plain_graph))'''

RUN_PLAIN = r'''# 규칙이 없는 상태 형식의 그래프에 첫 질문을 넣어 실행합니다
plain_state = {"question": first_question, "query": "", "trace": []}
plain_result = plain_graph.invoke(plain_state)
print_state("규칙이 없는 칸 결과", plain_result)
print("실행 흔적 칸의 길이:", len(plain_result["trace"]))'''

ADD_TRY = r'''# 규칙으로 적을 operator.add가 목록 두 개에 무엇을 하는지 먼저 봅니다
left_trace = ["input"]
right_trace = ["normalize"]
joined_trace = operator.add(left_trace, right_trace)
print("왼쪽 목록:", left_trace)
print("오른쪽 목록:", right_trace)
print("operator.add가 만든 목록:", joined_trace)'''

RULE_STATE = r'''# 실행 흔적 칸에만 이어 붙이기 규칙을 적은 상태 형식을 만듭니다
class RuleState(TypedDict):
    question: str
    query: str
    trace: Annotated[list[str], operator.add]'''

BUILD_RULE = r'''# 같은 노드 두 개와 같은 엣지 세 개를 규칙 적은 상태 형식으로 다시 적습니다
rule_builder = StateGraph(RuleState)
rule_builder.add_node("normalize", normalize)
rule_builder.add_node("make_query", make_query)
rule_builder.add_edge(START, "normalize")
rule_builder.add_edge("normalize", "make_query")
rule_builder.add_edge("make_query", END)
rule_graph = rule_builder.compile()
print("노드 수가 앞 그래프와 같은가:", len(rule_builder.nodes) == len(plain_builder.nodes))
print("컴파일 결과의 종류:", type(rule_graph))'''

RUN_RULE = r'''# 규칙을 적은 상태 형식의 그래프에 같은 첫 질문을 넣어 실행합니다
rule_state = {"question": first_question, "query": "", "trace": []}
rule_result = rule_graph.invoke(rule_state)
print_state("규칙을 적은 칸 결과", rule_result)
print("실행 흔적 칸의 길이:", len(rule_result["trace"]))'''

COMPARE = r'''# 두 실행의 결과를 칸별로 견줍니다
print("질문 칸이 같은가:", plain_result["question"] == rule_result["question"])
print("검색어 칸이 같은가:", plain_result["query"] == rule_result["query"])
print("실행 흔적 칸이 같은가:", plain_result["trace"] == rule_result["trace"])
assert rule_result["trace"] == ["normalize", "make_query"]'''

RUN_STARTED = r'''# 처음 실행 흔적 칸만 바꾸고 같은 그래프에 같은 질문을 넣습니다
started_state = {"question": first_question, "query": "", "trace": started_trace}
started_result = rule_graph.invoke(started_state)
print_state("처음 흔적을 넣은 결과", started_result)
print("실행 흔적 칸의 길이:", len(started_result["trace"]))'''

NORMALIZE_WHOLE = r'''# 01절처럼 앞 실행 흔적까지 함께 담아 내는 판을 만듭니다
def normalize_whole(state):
    clean_question = state["question"].strip()
    new_trace = state["trace"] + ["normalize"]
    return {"question": clean_question, "trace": new_trace}'''

MAKE_QUERY_WHOLE = r'''# 검색어를 만드는 노드도 앞 실행 흔적까지 함께 담아 내는 판으로 만듭니다
def make_query_whole(state):
    without_mark = state["question"].replace("?", "")
    plain = without_mark.replace("인가요", "")
    new_trace = state["trace"] + ["make_query"]
    return {"query": plain.strip(), "trace": new_trace}'''

BUILD_WHOLE = r'''# 규칙을 적은 같은 상태 형식에 방금 만든 노드 두 개를 등록합니다
whole_builder = StateGraph(RuleState)
whole_builder.add_node("normalize", normalize_whole)
whole_builder.add_node("make_query", make_query_whole)
whole_builder.add_edge(START, "normalize")
whole_builder.add_edge("normalize", "make_query")
whole_builder.add_edge("make_query", END)
whole_graph = whole_builder.compile()
print("등록한 노드 이름:")
for node_name in whole_builder.nodes:
    print(node_name)'''

RUN_WHOLE = r'''# 같은 첫 질문으로 이 그래프를 실행합니다
whole_state = {"question": first_question, "query": "", "trace": []}
whole_result = whole_graph.invoke(whole_state)
print_state("앞 흔적까지 내놓은 결과", whole_result)
print("실행 흔적 칸의 길이:", len(whole_result["trace"]))'''

RUN_ROW = r'''# 실행 한 번을 기록 한 줄로 만듭니다
def run_row(run_name, state):
    row = {"실행": run_name}
    row["실행 흔적"] = state["trace"]
    row["흔적 길이"] = len(state["trace"])
    return row'''

ROWS = r'''# 네 실행의 기록을 목록에 담습니다
run_rows = []
run_rows.append(run_row("규칙 없음", plain_result))
run_rows.append(run_row("규칙 적음", rule_result))
run_rows.append(run_row("처음 흔적 넣음", started_result))
run_rows.append(run_row("앞 흔적까지 내놓음", whole_result))
print("담은 기록 줄 수:", len(run_rows))'''

TABLE = r'''# 실행·실행 흔적·흔적 길이를 라벨 줄 아래에 차례로 출력합니다
print("실행 | 실행 흔적 | 흔적 길이")
for row in run_rows:
    print(row["실행"], "|", row["실행 흔적"], "|", row["흔적 길이"])'''

TITLE = """# 상태 갱신

**이 노트북에서 할 일**

1. 01절 상태 형식을 다시 적고 노드 두 개가 자기 이름만 내놓도록 바꿉니다.
2. 규칙이 없는 칸에 갱신 두 개가 모이면 무엇이 남는지 봅니다.
3. 실행 흔적 칸에 이어 붙이기 규칙을 적고 같은 두 노드로 다시 실행합니다.
4. 처음 실행 흔적과 노드가 내놓는 모양을 하나씩 바꿔 네 실행을 견줍니다.

**준비물** — 이 절은 OpenAI API 키를 쓰지 않습니다.
모델 요청이 0번이라 드는 비용이 없습니다.
읽어 오는 자료 파일도 없고 새로 쓰는 파일도 없습니다.
실행 시간은 1분 안팎이고 첫 셀의 설치가 가장 오래 걸립니다.

**기준 버전** — 첫 셀에서 LangGraph 1.2.11과 도구 파일이 쓰는 numpy 2.5.3을 설치합니다.
실습 폴더 잠금 파일은 LangChain 1.4.0도 함께 고정하지만 이 절은 부르지 않습니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3~7절을 읽습니다.
상태 형식에 규칙을 적고 같은 두 노드로 두 번 실행하는 자리입니다.
8절과 9절은 값을 하나씩 바꿔 보는 자리입니다.
10절은 네 실행을 기록 한 줄씩으로 만들어 표로 견주는 자리입니다.
준비부터 끝까지 함께 실행하고 실습 시간에 다시 읽습니다.

실습 폴더 `labs/part4/ch13-langgraph-basics`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""

FIGURE_ALT = ("왼쪽부터 오른쪽으로 놓인 칸 두 개와 회색 상자 하나로 왼쪽 칸 제목은 규칙이 없는 실행 흔적 칸이고 "
              "그 안에 파란 상자 받은 갱신 둘 normalize 다음 make_query와 노란 상자 남은 값 make_query 하나가 있으며 "
              "가운데 칸 제목은 규칙을 적은 실행 흔적 칸이고 그 안에 파란 상자 받은 갱신 둘 normalize 다음 "
              "make_query와 노란 상자 남은 값 normalize 다음 make_query가 있고 오른쪽에 회색 상자 두 칸이 받은 "
              "갱신은 같았음이 놓인 그림")

FIGURE_READ = """왼쪽 칸과 가운데 칸의 위 파란 상자가 같습니다.
두 칸이 받은 갱신이 같다는 뜻입니다.
아래 노란 상자의 값이 서로 다릅니다.
칸에 적은 규칙이 남는 값을 갈랐습니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIGURE_ALT + "](attachment:02-1-칸에-적은-규칙.png)\n\n" + FIGURE_READ, html="skip"),
        md("""## 1. 준비

첫 셀은 패키지 두 개를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 `langgraph: 1.2.11`과 `numpy: 2.5.3`이 보입니다.
패키지 `numpy`는 이 절이 직접 쓰지 않지만 도구 파일을 불러올 때 필요합니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이름 여섯 개를 불러옵니다.
앞의 네 개는 01절에서 쓴 이름이고 뒤의 두 개가 이 절에서 처음 쓰는 이름입니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.

이 노트북은 01절 출력 함수 `print_state()`를 가져옵니다.
라벨 줄을 따로 출력하고 그 아래에 칸 셋을 한 줄씩 적는 함수입니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄은 `불러온 이름: operator Annotated TypedDict StateGraph START END` 하나입니다.
꾸러미 `operator`에는 더하기 같은 기본 연산을 함수로 담아 둔 이름이 들어 있습니다.
표시 `Annotated`는 값 갈래 옆에 함께 쓸 정보를 적어 두는 표시입니다.
두 이름을 쓰는 자리는 6절과 7절입니다.
도구 파일에서 가져온 함수는 출력하지 않습니다.

## 2. 이 절에서 쓸 값 정하기

01절에서 쓴 첫 질문을 글자까지 같게 씁니다.
나중에 처음 실행 흔적으로 넣어 볼 목록도 미리 만들어 둡니다."""),
        code(VALUES),
        md("""**결과 읽기** — 출력 줄 `첫 질문의 글자 수: 17`은 01절과 같은 값입니다.
앞뒤 빈칸 네 개가 함께 세어진 수입니다.
출력 줄 `나중에 넣어 볼 처음 실행 흔적: ['input']`의 목록은 8절에서 씁니다.

## 3. 01절 상태 형식 다시 적기

01절 상태 형식에는 칸이 셋 있었고 어느 칸에도 규칙을 적지 않았습니다.
이 절에서도 그 형식으로 먼저 실행합니다.
이 절은 여기에 규칙 한 줄을 더하는 자리입니다."""),
        code(FLOW_STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 이름 뒤에 값 갈래만 적혀 있습니다.
칸 `trace`에는 지나간 노드 이름을 차례로 담습니다.
출력 함수 `print_state()`는 준비 셀에서 가져온 01절 판을 그대로 씁니다.

## 4. 노드 두 개 — 자기 이름만 내놓기

01절 두 노드는 실행 흔적을 낼 때 `state["trace"] + ["이름"]`으로 앞 값을 함께 담았습니다.
이번에는 두 노드 모두 자기 이름 하나만 담아 냅니다.
앞 값을 어떻게 이어 붙일지는 노드가 아니라 칸이 정하게 할 참입니다."""),
        code(NORMALIZE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
메서드 `strip()`은 글 앞뒤의 빈칸을 없앱니다.
실행 흔적 칸에 담아 내는 목록에는 이름 하나만 들어 있습니다.

다음 셀은 검색어 칸을 만드는 노드입니다."""),
        code(MAKE_QUERY),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
메서드 `replace()`는 글에서 찾은 말을 다른 말로 바꿉니다.
여기서는 물음표와 맺음말 `인가요`를 빈 글로 바꿔 지웁니다.

## 5. 실행 1 — 규칙이 없는 칸

먼저 규칙을 적지 않은 상태 형식으로 그래프를 만듭니다.
노드 두 개와 엣지 세 개는 01절과 같습니다."""),
        code(BUILD_PLAIN),
        md("""**결과 읽기** — 출력 줄 `등록한 노드 수: 2`와 종류 이름 `CompiledStateGraph`가 보입니다.
01절에서 만든 그래프와 같은 모양입니다.

실행 전에 예상해 봅니다.
두 노드가 실행 흔적 칸에 갱신을 하나씩 내니 이름 두 개가 남을 것도 같습니다."""),
        code(RUN_PLAIN),
        md("""**결과 읽기** — 줄 `실행 흔적 칸 | ['make_query']`에 이름이 하나뿐입니다.
출력 줄 `실행 흔적 칸의 길이: 1`이 그 수입니다.
먼저 온 갱신 `['normalize']`는 남지 않았습니다.
규칙을 적지 않은 칸은 마지막에 온 갱신으로 값을 바꿉니다.
줄 `검색어 칸 | 대출 기간은 며칠`은 01절과 같은 값입니다.

## 6. 칸에 적을 규칙 읽어 보기

리듀서(reducer)는 칸의 지금 값과 새 갱신을 받아 그 칸의 다음 값을 만드는 함수입니다.
공용 게시판의 칸마다 「새 쪽지로 바꾸기」와 「아래에 덧붙이기」 중 하나를 미리 정해 둔 것과 같습니다.
이 절에서는 목록 두 개를 이어 붙이는 함수 하나를 리듀서로 씁니다.
다음 셀은 그 함수를 그래프 없이 직접 불러 봅니다."""),
        code(ADD_TRY),
        md("""**결과 읽기** — 출력 줄 `operator.add가 만든 목록: ['input', 'normalize']`가 보입니다.
함수 `operator.add`는 값 두 개를 받아 더하기 기호와 같은 방법으로 합칩니다.
숫자 둘이면 더한 수가 되고 목록 둘이면 앞뒤로 이어 붙인 목록이 됩니다.
왼쪽 목록과 오른쪽 목록은 그대로 있고 새 목록이 따로 만들어졌습니다.

다음 셀은 그 함수를 실행 흔적 칸의 규칙으로 적습니다.
표시 `Annotated`는 값 갈래 옆에 함께 쓸 정보를 적어 두는 표시입니다.
짐 상자에 「깨지기 쉬움」처럼 다루는 방법을 함께 붙여 두는 것과 같습니다.
표시 `Annotated[list[str], operator.add]`는 「문자열 목록인데 합칠 때는 이 함수로」라는 뜻입니다."""),
        code(RULE_STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 `question`과 칸 `query`에는 규칙을 적지 않았습니다.
칸 `trace`에만 규칙을 적었습니다.
칸마다 규칙을 따로 정할 수 있습니다.

## 7. 실행 2 — 규칙을 적은 칸

바꾼 것은 상태 형식 하나입니다.
노드 두 개와 엣지 세 개와 질문은 그대로 둡니다.
실행 전에 예상해 봅니다. 실행 흔적 칸에 이름 두 개가 남을 것입니다."""),
        code(BUILD_RULE),
        md("""**결과 읽기** — 출력 줄 `노드 수가 앞 그래프와 같은가: True`가 보입니다.
종류 이름도 `CompiledStateGraph`로 앞 그래프와 같습니다.

다음 셀은 같은 첫 질문을 넣어 실행합니다."""),
        code(RUN_RULE),
        md("""**결과 읽기** — 줄 `실행 흔적 칸 | ['normalize', 'make_query']`에 이름 두 개가 차례로 남았습니다.
출력 줄 `실행 흔적 칸의 길이: 2`가 그 수입니다.
노드는 자기 이름 하나만 냈는데 칸에 적은 규칙이 앞 값과 이어 붙였습니다.

다음 셀은 두 실행을 칸별로 견줍니다."""),
        code(COMPARE),
        md("""**결과 읽기** — 출력 줄 `질문 칸이 같은가: True`와 `검색어 칸이 같은가: True`가 보입니다.
출력 줄 `실행 흔적 칸이 같은가: False`만 다릅니다.
규칙을 적은 칸에서만 값이 달라졌습니다.
규칙을 적지 않은 칸 두 개는 앞 실행과 같은 값을 냈습니다.

## 8. 값 바꿔 보기 ① 처음 실행 흔적 칸

바꿀 값은 처음 상태의 실행 흔적 칸 하나입니다.
빈 목록 대신 `['input']`을 넣습니다.
그래프와 질문은 실행 2와 그대로 같습니다.
실행 전에 예상해 봅니다. 처음 값 뒤에 이름 두 개가 붙을 것입니다."""),
        code(RUN_STARTED),
        md("""**결과 읽기** — 줄 `실행 흔적 칸 | ['input', 'normalize', 'make_query']`가 보입니다.
출력 줄 `실행 흔적 칸의 길이: 3`이 그 수입니다.
처음에 넣은 값이 지워지지 않고 맨 앞에 남았습니다.
규칙은 노드가 낸 갱신뿐 아니라 처음 넣은 값에도 같은 방법으로 쓰입니다.

## 9. 값 바꿔 보기 ② 노드가 내놓는 모양

바꿀 값은 노드가 실행 흔적 칸에 담아 내는 목록 하나입니다.
01절처럼 앞 실행 흔적까지 함께 담아 내는 노드 두 개를 새로 만듭니다.
상태 형식은 규칙을 적은 것을 그대로 씁니다.
실행 전에 예상해 봅니다. 앞 값이 두 번 들어가 이름 하나가 겹칠 것입니다."""),
        code(NORMALIZE_WHOLE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
줄 `state["trace"] + ["normalize"]`가 01절 노드와 같은 모양입니다.

다음 셀은 검색어 칸을 만드는 노드도 같은 모양으로 만듭니다."""),
        code(MAKE_QUERY_WHOLE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
검색어를 만드는 부분은 앞의 노드와 같고 실행 흔적을 담는 줄만 다릅니다.

다음 셀은 이 노드 두 개로 그래프를 하나 더 만듭니다."""),
        code(BUILD_WHOLE),
        md("""**결과 읽기** — 라벨 줄 `등록한 노드 이름:` 아래 두 줄은 `normalize`와 `make_query`입니다.
등록한 이름은 앞 그래프와 같고 짝지은 함수만 다릅니다.

다음 셀은 같은 첫 질문으로 이 그래프를 실행합니다."""),
        code(RUN_WHOLE),
        md("""**결과 읽기** — 줄 `실행 흔적 칸 | ['normalize', 'normalize', 'make_query']`가 보입니다.
출력 줄 `실행 흔적 칸의 길이: 3`이 그 수입니다.
이름 `normalize`가 두 번 들어갔습니다.
노드가 앞 값을 함께 냈고 칸의 규칙이 거기에 앞 값을 한 번 더 이어 붙였습니다.
규칙을 적은 칸에는 노드가 새 기록만 내야 합니다.

## 10. 네 실행을 기록 한 줄씩으로

실행 한 번을 기록 한 줄로 만들어 담아 둡니다.
Ch 9~12와 01절에서 쓴 기록 한 줄과 같은 모양입니다."""),
        code(RUN_ROW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 네 실행의 기록을 목록에 담습니다."""),
        code(ROWS),
        md("""**결과 읽기** — 출력 줄 `담은 기록 줄 수: 4`가 보입니다.

다음 셀은 담은 줄을 표로 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 네 줄이 나옵니다.
줄 `규칙 없음 | ['make_query'] | 1`이 규칙을 적지 않은 칸의 결과입니다.
줄 `규칙 적음 | ['normalize', 'make_query'] | 2`가 규칙을 적은 칸의 결과입니다.
아래 두 줄은 길이가 모두 3이지만 담긴 이름이 다릅니다.
한 줄은 처음 값을 지켰고 다른 한 줄은 이름 하나가 겹쳤습니다.

## 정리

1. 규칙을 적지 않은 칸은 마지막에 온 갱신으로 값을 바꿨습니다.
2. 실행 흔적 칸에 이어 붙이기 규칙을 적자 같은 두 노드가 낸 이름이 차례로 쌓였습니다.
3. 규칙을 적은 칸에 앞 값까지 함께 내면 이름 하나가 겹쳤습니다.

03절에서는 상태의 값을 읽어 다음 노드를 고르는 조건부 엣지를 만듭니다.
이 절까지는 엣지가 정해 둔 한 갈래 길만 지났습니다."""),
    ]


if __name__ == "__main__":
    path = write_notebook(LAB, "02", "02-State-갱신", "experiment", cells())
    print("wrote", path)
