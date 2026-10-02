"""Ch 13 01절 품질 개선본 노트북 생성기 (QUALITY-UPGRADE.md §2·§3·§6).

사용: python3 author_01.py → labs/part4/ch13-langgraph-basics/notebooks/01-StateGraph와-노드-엣지.ipynb 를 새로 쓴다.
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북은 qa/upgrade/before/notebooks/ 에 있다. **experiment 형식 유지**(chapter.json).
챕터 옛 생성기 `qa/author_ch13.py`(7절을 한 번에 쓰던 파일)는 실행을 막아 두었다(규격 §8).

## Part 1~3에서 이어 쓴 것 (과정 요약 `textbook/qa/upgrade-course-summary.md`)

- 셀 모양: 정의 셀과 호출 셀 분리, 셀당 함수 하나, 함수 본문 10줄 이하, 코드 3~12줄(15 상한).
- 여러 줄 출력은 라벨 줄을 따로 두고 결과 읽기에서 「라벨 줄 아래」로 가리킨다(규격 §2-4).
- 기록 한 줄 = 실행 한 번, 한국어 키 딕셔너리 → 목록에 `append` → 끝난 뒤 한꺼번에 표로 출력.
- 「칸」 = 상태의 키 자리(Ch 9~12 용어). 「조각」은 Ch 5 토큰 뜻 전용이라 쓰지 않는다.
- `lambda`·내포식·조건 표현식·f-string·`key=`·`reverse=`·세미콜론·한 줄 복합문·numpy·sklearn 0건.
- 부른 내장 이름은 `len`·`print`·`type`뿐이다(Part 3이 쓴 목록 안).

## 이 절이 새로 여는 것 (LangGraph 첫 절)

- `StateGraph(상태 형식)` · `add_node(이름, 함수)` · `add_edge(앞, 뒤)` · `START` · `END` · `compile()` · `invoke(상태)`.
- `get_graph().draw_mermaid()` · `get_graph().nodes`.
- 상태 형식을 적는 `TypedDict`와 타입힌트 `str`·`list[str]`(규격 §2-2 L5, 과정 요약 §2 「처음 쓰면 한 문장」).
  Ch 2 06절에서 배운 `class` 문을 Part 2·3에서 한 번도 쓰지 않았으므로 본문 b3·b4에서 되짚는다.
  필드만 적고 메서드를 넣지 않아 게이트 G1의 스키마 클래스 예외에 든다.

## 선택한 것과 까닭

1. **모델 요청 0번.** 이 절의 주제는 그래프 구조다(AGENT-BRIEF 「그래프 구조가 주제면 모델 호출 0번도
   좋습니다」). API 키 셀도 두지 않았다. Ch 10 01~05절·Ch 12 04절 선례와 같다. 설치도 `langgraph==1.2.11`
   하나만 한다(개선 전은 쓰지 않는 langchain·langchain-openai·python-dotenv·scikit-learn까지 설치했다).
2. **두 노드가 실행 흔적을 같은 방법으로 이어 붙인다.** 개선 전 `normalize`는 `{'trace': ['normalize']}`로
   앞 값을 덮어쓰고 `make_query`만 `state['trace'] + [...]`로 이어 붙여 두 노드의 규칙이 달랐다.
   리듀서는 02절 주제이므로 01절에서는 두 노드 모두 코드에서 직접 이어 붙인다.
3. **손으로 이어 부르기 → 그래프로 옮기기 차례.** 학습 질문이 「함수 나열을 그래프로 옮기면」이므로
   같은 두 함수를 먼저 손으로 이어 부르고(7~10절) 그 결과를 그래프 결과와 견준다(14절).
4. **등록 차례만 바꾼 그래프를 실제로 만들어 실행한다.** 개선 전 본문은 「노드를 등록한 순서가 실행 순서를
   정하는 것이 아니라」를 실행 없이 단언했다. 규격 §3 「노트북에서 실행하지 않은 동작은 일반화하지 않는다」에
   걸리므로 22~24절에서 등록 차례만 바꾼 그래프를 만들어 같은 실행 흔적이 나오는지 확인한다.
5. **`assert`는 코드가 정하는 값에만 건다.** 모델을 부르지 않으므로 모델 답 `assert`는 처음부터 0건이다.
6. **파일을 쓰지 않는다.** 이 절은 `runs/`에 아무것도 쓰지 않고 읽지도 않는다(Ch 12 기록 계약과 무관).
7. **`list()`·`enumerate`·`zip`·`join`을 쓰지 않는다.** 노드 이름 목록은 `for`로 한 줄씩 출력한다
   (Part 3이 쓰지 않은 내장 이름을 늘리지 않으려고).

## 탐색 실행에서 확인한 값 (2026-09-19, /tmp/ch13-01/probe1.py)

langgraph 1.2.11 · langchain-core 1.6.2 · Python 3.12.13. `builder.nodes`는 등록 차례대로 담긴
딕셔너리이고 `graph.get_graph().nodes`에는 `__start__`·`__end__`가 함께 있다. 등록 차례를 바꿔도
실행 흔적은 `['normalize', 'make_query']`로 같았다. 같은 코드를 두 번 돌려 모든 출력이 같았다.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part4/ch13-langgraph-basics/notebooks"

INSTALL = install_source(["langgraph==1.2.11"])

IMPORTS = r'''# 상태 형식과 그래프 만들기에 쓸 이름 네 개를 불러옵니다
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

print("불러온 이름:", "TypedDict", "StateGraph", "START", "END")'''

VALUES = r'''# 이 절에서 쓸 질문 두 개를 정합니다(앞뒤에 빈칸을 일부러 넣었습니다)
first_question = "  대출 기간은 며칠인가요?  "
second_question = "  주말 운영 시간은 언제인가요?  "
print("첫 질문:", first_question)
print("첫 질문의 글자 수:", len(first_question))
print("바꿔 볼 질문:", second_question)'''

STATE = r'''# 그래프가 도는 동안 노드들이 함께 읽고 고칠 칸 세 개를 적습니다
class FlowState(TypedDict):
    question: str
    query: str
    trace: list[str]'''

PRINT_STATE = r'''# 상태의 칸 세 개를 라벨 줄 아래에 한 줄씩 출력합니다
def print_state(label, state):
    print(label)
    print("질문 칸 |", state["question"])
    print("검색어 칸 |", state["query"])
    print("실행 흔적 칸 |", state["trace"])'''

NORMALIZE = r'''# 질문 칸의 앞뒤 빈칸을 없애고 이 노드가 지난 자취를 실행 흔적에 붙입니다
def normalize(state):
    clean_question = state["question"].strip()
    new_trace = state["trace"] + ["normalize"]
    return {"question": clean_question, "trace": new_trace}'''

NORMALIZE_TRY = r'''# 노드 함수도 보통 함수입니다. 그래프 없이 직접 불러 봅니다
hand_state = {"question": first_question, "query": "", "trace": []}
first_update = normalize(hand_state)
print("normalize가 낸 갱신:", first_update)
print("갱신에 든 칸 수:", len(first_update))'''

MAKE_QUERY = r'''# 물음표와 맺음말을 지워 검색어 칸에 넣을 말을 만듭니다
def make_query(state):
    without_mark = state["question"].replace("?", "")
    plain = without_mark.replace("인가요", "")
    new_trace = state["trace"] + ["make_query"]
    return {"query": plain.strip(), "trace": new_trace}'''

MAKE_QUERY_TRY = r'''# 앞 갱신을 상태에 합친 뒤 두 번째 노드 함수를 불러 봅니다
hand_state.update(first_update)
second_update = make_query(hand_state)
print("make_query가 낸 갱신:", second_update)
print("갱신에 든 칸 수:", len(second_update))'''

BY_HAND = r'''# 두 번째 갱신까지 합쳐 손으로 이어 부른 결과를 봅니다
hand_state.update(second_update)
print_state("손으로 이어 부른 결과", hand_state)'''

BUILDER = r'''# 노드 두 개를 그래프에서 쓸 이름과 함께 설계 객체에 등록합니다
builder = StateGraph(FlowState)
builder.add_node("normalize", normalize)
builder.add_node("make_query", make_query)
print("등록한 노드 수:", len(builder.nodes))
print("등록한 노드 이름:")
for node_name in builder.nodes:
    print(node_name)'''

EDGES = r'''# START부터 END까지 실행 순서를 엣지 세 개로 적습니다
builder.add_edge(START, "normalize")
builder.add_edge("normalize", "make_query")
builder.add_edge("make_query", END)
edge_order = ["START", "normalize", "make_query", "END"]
print("엣지로 적은 실행 순서:", edge_order)'''

COMPILE = r'''# 선언한 구조를 확인해 실행할 수 있는 그래프로 만듭니다
graph = builder.compile()
print("설계 객체의 종류:", type(builder))
print("컴파일 결과의 종류:", type(graph))'''

RUN_ONE = r'''# 컴파일한 그래프에 첫 상태를 넣어 실행합니다
first_state = {"question": first_question, "query": "", "trace": []}
first_result = graph.invoke(first_state)
print_state("그래프 실행 1 결과", first_result)'''

COMPARE_HAND = r'''# 손으로 이어 부른 결과와 그래프가 낸 결과를 칸별로 견줍니다
print("검색어 칸이 같은가:", hand_state["query"] == first_result["query"])
print("실행 흔적이 같은가:", hand_state["trace"] == first_result["trace"])
assert first_result["trace"] == ["normalize", "make_query"]'''

RUN_TWO = r'''# 질문만 바꾸고 그래프와 처음 칸 값은 그대로 두어 다시 실행합니다
second_state = {"question": second_question, "query": "", "trace": []}
second_result = graph.invoke(second_state)
print_state("그래프 실행 2 결과", second_result)'''

RUN_ROW = r'''# 실행 한 번을 기록 한 줄로 만듭니다
def run_row(run_name, state):
    row = {"실행": run_name}
    row["검색어 칸"] = state["query"]
    row["실행 흔적"] = state["trace"]
    return row'''

ROWS = r'''# 두 실행의 기록을 목록에 담습니다
run_rows = []
run_rows.append(run_row("실행 1", first_result))
run_rows.append(run_row("실행 2", second_result))
print("담은 기록 줄 수:", len(run_rows))'''

TABLE = r'''# 실행·검색어 칸·실행 흔적을 라벨 줄 아래에 차례로 출력합니다
print("실행 | 검색어 칸 | 실행 흔적")
for row in run_rows:
    print(row["실행"], "|", row["검색어 칸"], "|", row["실행 흔적"])'''

MERMAID = r'''# 컴파일한 그래프가 스스로 그린 구조 문자열을 받아 옵니다
mermaid_text = graph.get_graph().draw_mermaid()
print("그래프가 그린 구조:")
print(mermaid_text)'''

NODE_NAMES = r'''# 그래프에 남은 노드 이름을 한 줄씩 출력해 우리가 적은 이름과 맞춰 봅니다
graph_nodes = graph.get_graph().nodes
print("그래프에 있는 노드 이름:")
for node_name in graph_nodes:
    print(node_name)'''

SWAP_NODES = r'''# 노드를 등록하는 차례만 바꿔 설계 객체를 하나 더 만듭니다
swapped = StateGraph(FlowState)
swapped.add_node("make_query", make_query)
swapped.add_node("normalize", normalize)
print("등록한 차례:")
for node_name in swapped.nodes:
    print(node_name)'''

SWAP_EDGES = r'''# 엣지 세 개는 실행 1에 쓴 그래프와 똑같이 적고 컴파일합니다
swapped.add_edge(START, "normalize")
swapped.add_edge("normalize", "make_query")
swapped.add_edge("make_query", END)
swapped_graph = swapped.compile()
print("컴파일 결과의 종류:", type(swapped_graph))'''

RUN_THREE = r'''# 같은 첫 질문으로 등록 차례를 바꾼 그래프를 실행합니다
swapped_state = {"question": first_question, "query": "", "trace": []}
swapped_result = swapped_graph.invoke(swapped_state)
print_state("등록 차례를 바꾼 그래프 결과", swapped_result)
print("실행 1과 실행 흔적이 같은가:", swapped_result["trace"] == first_result["trace"])'''

TITLE = """# StateGraph와 노드·엣지

**이 노트북에서 할 일**

1. 상태 칸 세 개를 적고 노드로 쓸 함수 두 개를 만듭니다.
2. 두 함수를 손으로 이어 부른 뒤 같은 일을 그래프로 옮깁니다.
3. 질문 하나만 바꿔 다시 실행하고 두 실행을 기록으로 견줍니다.
4. 노드를 등록한 차례만 바꿔 실행 순서가 달라지는지 봅니다.

**준비물** — 이 절은 OpenAI API 키를 쓰지 않습니다.
모델 요청이 0번이라 드는 비용이 없습니다.
읽어 오는 자료 파일도 없고 새로 쓰는 파일도 없습니다.
실행 시간은 1분 안팎이고 첫 셀의 설치가 가장 오래 걸립니다.

**기준 버전** — 첫 셀에서 LangGraph 1.2.11을 설치합니다.
실습 폴더 잠금 파일은 LangChain 1.4.0도 함께 고정하지만 이 절은 부르지 않습니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3~6절과 11~14절을 읽습니다.
상태 칸을 적고 노드 함수를 만든 뒤 그래프로 옮기는 자리입니다.
7~10절은 같은 두 함수를 손으로 이어 부르는 자리이고 15~17절은 값 바꿔 보기입니다.
18~21절과 22~24절은 함께 실행하고 실습 시간에 다시 읽습니다.

실습 폴더 `labs/part4/ch13-langgraph-basics`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""

FIGURE_ALT = ("위에서 아래로 내려가는 흐름도로 맨 위 초록 상자 들어간 상태 질문 칸에 빈칸이 붙어 있음에서 "
              "회색 둥근 상자 START를 지나 파란 상자 노드 normalize 질문 칸 정리와 파란 상자 노드 "
              "make_query 검색어 칸 만들기를 차례로 지나고 회색 둥근 상자 END를 거쳐 맨 아래 노란 상자 "
              "나온 상태 검색어 칸 대출 기간은 며칠로 이어지는 그림")

FIGURE_READ = """맨 위 초록 상자가 그래프에 넣은 상태입니다.
가운데 파란 상자 두 개가 우리가 만든 노드이고 위에서 아래로 읽습니다.
회색 둥근 상자 두 개는 LangGraph가 두는 가상 지점입니다.
맨 아래 노란 상자는 이 노트북의 출력으로 확인한 결과입니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIGURE_ALT + "](attachment:01-1-상태-노드-엣지-한눈에.png)\n\n" + FIGURE_READ, html="skip"),
        md("""## 1. 준비

첫 셀은 패키지 하나를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 `langgraph: 1.2.11`이 보입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름 네 개를 불러옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄은 `불러온 이름: TypedDict StateGraph START END` 하나입니다.
형식 `TypedDict`는 어떤 칸에 어떤 값이 들어가는지 적어 두는 딕셔너리 형식입니다.
설계 객체 `StateGraph`는 노드와 엣지를 모아 그래프를 만드는 이름입니다.
이름 `START`와 `END`는 LangGraph가 두는 가상 시작점과 가상 끝점입니다.

## 2. 이 절에서 쓸 질문 정하기

질문 두 개를 미리 정해 둡니다.
앞뒤에 빈칸을 일부러 넣어 첫 노드가 할 일을 만듭니다."""),
        code(VALUES),
        md("""**결과 읽기** — 출력 줄 `첫 질문의 글자 수: 17`에서 앞뒤 빈칸 네 개가 함께 세어졌습니다.
질문 자체는 열세 글자이고 나머지 네 글자가 빈칸입니다.
빈칸은 화면에서 잘 보이지 않으므로 글자 수로 확인합니다.

## 3. 상태 칸 적기

상태는 그래프가 도는 동안 노드들이 함께 읽고 고치는 값입니다.
공용 게시판에 칸이 셋 있고 사람마다 맡은 칸에만 적는 모습과 같습니다.
다음 셀은 그 칸 세 개의 이름과 값 갈래를 적습니다.
Ch 2 06절에서 배운 `class` 문을 Part 2·3에서는 쓰지 않았습니다.
여기서는 라이브러리가 상태 형식을 요구해 필드만 적은 형식 하나를 만듭니다."""),
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 이름 뒤 `: str`은 그 칸에 문자열이 들어간다는 표시입니다.
표시 `list[str]`은 문자열을 담은 목록이라는 뜻입니다.
칸 `trace`에는 지나간 노드 이름을 차례로 담아 실행 흔적으로 씁니다.

다음 셀은 상태를 칸별로 출력하는 함수입니다."""),
        code(PRINT_STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
라벨 줄을 따로 출력하고 그 아래에 칸을 한 줄씩 적습니다.

## 4. 노드로 쓸 함수 두 개 만들기

노드는 상태를 받아 바꿀 칸만 딕셔너리로 내놓는 함수입니다.
먼저 질문 칸을 정리하는 함수를 만듭니다."""),
        code(NORMALIZE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
메서드 `strip()`은 글 앞뒤의 빈칸을 없앱니다.
실행 흔적 칸에는 기존 목록 뒤에 이름 하나를 붙여 새 목록을 만듭니다.
칸마다 합치는 규칙을 상태에 적어 두는 방법은 02절에서 배웁니다.

다음 셀은 그 함수를 그래프 없이 직접 불러 봅니다."""),
        code(NORMALIZE_TRY),
        md("""**결과 읽기** — 출력 줄에 `{'question': '대출 기간은 며칠인가요?', 'trace': ['normalize']}`가 보입니다.
앞뒤 빈칸이 사라졌고 실행 흔적에 이름 하나가 담겼습니다.
출력 줄 `갱신에 든 칸 수: 2`에서 검색어 칸이 빠진 것을 확인합니다.
노드는 자기가 바꾸는 칸만 내놓습니다.

다음 셀은 검색어 칸을 만드는 함수입니다."""),
        code(MAKE_QUERY),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
메서드 `replace()`는 글에서 찾은 말을 다른 말로 바꿉니다.
여기서는 물음표와 맺음말 `인가요`를 빈 글로 바꿔 지웁니다.

다음 셀은 앞 갱신을 상태에 합친 뒤 이 함수를 불러 봅니다."""),
        code(MAKE_QUERY_TRY),
        md("""**결과 읽기** — 출력 줄에 `{'query': '대출 기간은 며칠', 'trace': ['normalize', 'make_query']}`가 보입니다.
검색어 칸에 물음표와 맺음말이 빠진 말이 담겼습니다.
실행 흔적에는 이름 두 개가 차례로 쌓였습니다.

## 5. 손으로 이어 부른 결과 보기

메서드 `update()`는 딕셔너리에 다른 딕셔너리의 칸을 덮어 씁니다.
갱신을 상태에 합치는 일을 손으로 한 셈입니다."""),
        code(BY_HAND),
        md("""**결과 읽기** — 라벨 줄 `손으로 이어 부른 결과` 아래 세 줄이 나옵니다.
줄 `검색어 칸 | 대출 기간은 며칠`이 두 함수를 지난 결과입니다.
줄 `실행 흔적 칸 | ['normalize', 'make_query']`에 지나온 차례가 남았습니다.
여기까지는 그래프를 쓰지 않았고 부르는 차례를 코드 줄이 정했습니다.

## 6. 같은 일을 그래프로 옮기기

이제 같은 두 함수를 그래프에 등록합니다.
등록은 함수를 부르는 것이 아니라 이름과 함수를 짝지어 적어 두는 일입니다."""),
        code(BUILDER),
        md("""**결과 읽기** — 출력 줄 `등록한 노드 수: 2`가 보입니다.
라벨 줄 `등록한 노드 이름:` 아래 두 줄은 `normalize`와 `make_query`입니다.
등록만 했을 뿐 아직 함수 본문은 실행되지 않았습니다.

다음 셀은 실행 순서를 엣지로 적습니다."""),
        code(EDGES),
        md("""**결과 읽기** — 출력 줄 `엣지로 적은 실행 순서: ['START', 'normalize', 'make_query', 'END']`가 보입니다.
엣지 하나가 「이 노드 다음에는 저 노드」라는 이동 한 칸입니다.
가상 시작점에서 첫 노드로, 마지막 노드에서 가상 끝점으로 가는 엣지도 적습니다.

다음 셀은 적어 둔 구조를 실행할 수 있는 그래프로 만듭니다."""),
        code(COMPILE),
        md("""**결과 읽기** — 출력 줄 두 개의 종류 이름이 서로 다릅니다.
설계 객체는 `StateGraph`이고 컴파일 결과는 `CompiledStateGraph`입니다.
컴파일하기 전 객체는 적어 둔 설계도이고 컴파일 결과가 실행하는 객체입니다.

## 7. 실행 1 — 첫 질문

실행 전에 예상해 봅니다.
검색어 칸에는 손으로 이어 부른 결과와 같은 말이 담길 것입니다."""),
        code(RUN_ONE),
        md("""**결과 읽기** — 라벨 줄 `그래프 실행 1 결과` 아래 세 줄이 나옵니다.
줄 `검색어 칸 | 대출 기간은 며칠`과 줄 `실행 흔적 칸 | ['normalize', 'make_query']`가 보입니다.
빈 글로 넣은 검색어 칸이 둘째 노드에서 채워졌습니다.

다음 셀은 손으로 이어 부른 결과와 칸별로 견줍니다."""),
        code(COMPARE_HAND),
        md("""**결과 읽기** — 출력 줄 `검색어 칸이 같은가: True`와 `실행 흔적이 같은가: True`가 보입니다.
같은 두 함수를 썼으니 결과가 같습니다.
달라진 것은 실행 순서를 어디에 적었는가입니다.
손으로 부를 때는 코드 줄의 차례가, 그래프에서는 엣지가 순서를 정했습니다.

## 8. 값 바꿔 보기 — 질문 하나만 바꾸기

바꿀 값은 질문 하나입니다.
그래프와 처음 칸 값은 그대로 둡니다.
실행 전에 예상해 봅니다. 검색어 칸은 달라지고 실행 흔적은 같을 것입니다."""),
        code(RUN_TWO),
        md("""**결과 읽기** — 줄 `검색어 칸 | 주말 운영 시간은 언제`로 값이 달라졌습니다.
줄 `실행 흔적 칸 | ['normalize', 'make_query']`는 실행 1과 같습니다.
엣지로 고정한 순서라 질문 내용이 순서를 바꾸지 못했습니다.

## 9. 두 실행을 기록 한 줄씩으로

실행 한 번을 기록 한 줄로 만들어 담아 둡니다.
Ch 9~12에서 쓴 기록 한 줄과 같은 모양입니다."""),
        code(RUN_ROW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 두 실행의 기록을 목록에 담습니다."""),
        code(ROWS),
        md("""**결과 읽기** — 출력 줄 `담은 기록 줄 수: 2`가 보입니다.

다음 셀은 담은 줄을 표로 출력합니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄이 나옵니다.
줄 `실행 1 | 대출 기간은 며칠 | ['normalize', 'make_query']`가 첫 실행입니다.
줄 `실행 2 | 주말 운영 시간은 언제 | ['normalize', 'make_query']`가 질문만 바꾼 실행입니다.
검색어 칸만 달라지고 실행 흔적 칸은 같습니다.

## 10. 그래프가 그린 구조 보기

그래프는 자기 구조를 문자열로 그려 줍니다.
우리가 적은 엣지가 그대로 있는지 확인합니다."""),
        code(MERMAID),
        md("""**결과 읽기** — 라벨 줄 `그래프가 그린 구조:` 아래에 여러 줄이 나옵니다.
줄 `normalize --> make_query;`가 우리가 적은 둘째 엣지입니다.
줄 `__start__ --> normalize;`와 `make_query --> __end__;`도 보입니다.
이 문자열은 LangGraph가 만든 것이라 색과 모양이 교재 도식과 다릅니다.

다음 셀은 그래프에 남은 노드 이름을 한 줄씩 봅니다."""),
        code(NODE_NAMES),
        md("""**결과 읽기** — 라벨 줄 아래 네 줄이 나옵니다.
이름 `__start__`와 `__end__`는 라이브러리가 붙인 가상 지점 이름입니다.
가운데 두 줄이 우리가 등록한 `normalize`와 `make_query`입니다.

## 11. 값 바꿔 보기 — 등록 차례만 바꾸기

이번에 바꿀 값은 노드를 등록하는 차례 하나입니다.
엣지 세 개와 질문은 그대로 둡니다.
실행 전에 예상해 봅니다. 실행 흔적은 실행 1과 같을 것입니다."""),
        code(SWAP_NODES),
        md("""**결과 읽기** — 라벨 줄 `등록한 차례:` 아래 첫 줄이 `make_query`입니다.
실행 1에 쓴 그래프와 등록 차례가 뒤바뀌었습니다.

다음 셀은 엣지를 똑같이 적고 컴파일합니다."""),
        code(SWAP_EDGES),
        md("""**결과 읽기** — 출력 줄의 종류 이름이 `CompiledStateGraph`로 실행 1의 그래프와 같습니다.
엣지 세 개도 실행 1에 쓴 그래프와 글자까지 같습니다.

다음 셀은 같은 첫 질문으로 이 그래프를 실행합니다."""),
        code(RUN_THREE),
        md("""**결과 읽기** — 줄 `실행 흔적 칸 | ['normalize', 'make_query']`가 보입니다.
출력 줄 `실행 1과 실행 흔적이 같은가: True`로 두 실행이 같음을 확인했습니다.
등록 차례를 바꿔도 실행 순서는 엣지가 정했습니다.
노드가 셋 이상이거나 갈래가 있는 그래프는 이번에 실행하지 않았습니다.

## 정리

1. 노드는 상태를 받아 바꿀 칸만 내놓는 보통 함수였습니다.
2. 같은 두 함수를 손으로 이어 부른 결과와 그래프 실행 1 결과가 같았습니다.
3. 질문을 바꾸거나 등록 차례를 바꿔도 실행 흔적은 `['normalize', 'make_query']`였습니다.

02절에서는 같은 칸에 갱신이 여러 번 모일 때 합치는 규칙을 상태에 적어 둡니다.
이 절에서 코드로 직접 이어 붙인 실행 흔적을 그 규칙으로 옮깁니다."""),
    ]


if __name__ == "__main__":
    path = write_notebook(LAB, "01", "01-StateGraph와-노드-엣지", "experiment", cells())
    print("wrote", path)
