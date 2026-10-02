"""Ch 25 04절(챕터 끝 실습 절) 생성기 (QUALITY-UPGRADE.md §7-2·§2·§2-7·§3·§4·§6).

사용:
  python3 -B author_04.py            → 도구 파일(없거나 03 판·04 판일 때만) + 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_04.py --src-only → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_04.py --tools-copy DIR → 도구 파일(04 판)만 DIR에 쓴다(새 커널 사본 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
새로 만든 절이라 qa/upgrade/before/ 에 원본이 없다. **experiment 형식**(chapter.json), lesson_part 없음.

## 결정 1 — 붙인 앞 절 기능 셋 (인계 「§03 → 실습(04)」 6항)

01절 모드 목록(스트림 모드를 목록으로 골라 한 실행에서 함께 받기 · (모드 이름, 자료) 짝 · positions_of) +
02절 진행 값(노드 안 get_stream_writer) · 스트림 청크 글 이어 붙이기 · mode_order +
03절 사건마다 시각 적기(collect_timed_events) · 글자가 든 첫 스트림 청크 자리(first_text_place) · 세 시간(three_times).
작은 과제: 자료실 문의 창 흉내 — 사건을 화면에 띄울 것(진행 값 목록·이어 붙인 답 글)으로 바꿔 읽는 기록 장치(screen_log·print_report).
실행 1 = 칸 show_notice "yes"(요청 전 진행 값 켬) · 같은 설정 다시(같은 값과 달라지는 값 가르기) · 실행 2 = show_notice "no"(값 하나).
뺀 것: 01 일곱 모드 전부·체크포인터·멈춤 표시·invoke 견주기 · 02 칸 metadata 읽기·스트림 청크 합치기로 사용량 보기·messages 뺀 실행(02 8절 되풀이) ·
03 예상 비용·두 구간 나누기·목록 차례 바꾸기(03 9절 되풀이).

## 결정 2 — 흔들림 먼저 확인 (qa/upgrade/04-probe.md)

§0에 후보 A·B와 규칙을 먼저 적고 A를 N1·N2 다섯 번씩(10요청). 열 번 모두 결정적 후보 같음 → A 채택(B는 보내지 않음).
노트북은 칸 show_notice를 글 "yes"/"no"로 적는다(내장 이름 bool을 새로 쓰지 않으려고 — 프로브는 참·거짓 값, 요청 글·사건 차례와 무관).

## 결정 3 — 결론은 코드가 정하는 값

모드 차례 · 첫 사건의 모드와 자료 · 첫 스트림 청크 글자 수 · 글자가 든 첫 스트림 청크 자리 · 화면에 띄운 진행 값 목록 ·
화면 글 == 답 글 · 진행 값 자리가 마지막 사건 바로 앞인가. 사건 수·초·답 글은 결과 읽기 둘째 단락·b6 표·「확인할 점」에만
([[…]] 자리 표시 → 교재 출력 실행 뒤 mdpatch.py). assert는 키 셀 하나뿐(모델 글·초에 0).

## 결정 4 — 도구 파일 (§2-7) — 03절 함수 셋을 옮기고 import time 한 줄

03절 노트북에만 있던 collect_timed_events(3절)·first_text_place(5절)·three_times(7절)를 03 셀 글 그대로 도구 파일 끝에 옮긴다
(check_tools()가 03 노트북 셀과 문자열·AST 대조). collect_timed_events가 time을 쓰므로 머리 설명 바로 뒤에 주석 한 줄 + import time.
머리 설명(02 판 글)은 바꾸지 않는다. 02·03 생성기는 이 가져오기 줄을 빼고 앞머리를 견주게 고쳤다(author_02.strip_later_imports).
노드·상태 형식은 노트북 전역 model·system_text를 읽어 노트북에 새로 적는다(02 노드와 모양이 달라 「같은 코드」라고 하지 않음).

## 모델 요청

노트북 한 번 **3번**(5·6·7절 한 번씩). 읽는 파일·쓰는 파일 0, 체크포인터 없음.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`key=`·`reverse=`·
`set`·`setdefault`·노트북 `.get`·`+=`·`break`·`while`·`try`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·대입 풀기·
별표 풀기·세미콜론·`isinstance`·데코레이터·클래스(상태 형식 말고)·`join`·`astream`·`bool`·`round`(노트북 — 도구 파일 three_times 안만)·
체크포인터·예상 비용.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nbkit import RUN_DATE, code, key_and_model_cells, md, setup, write_notebook  # noqa: E402
import author_01  # noqa: E402  (html_text·table_html)
import author_02  # noqa: E402  (설치 셀·도구 파일 머리 설명·strip_later_imports)
import author_03  # noqa: E402  (도구 파일 03 판·03절 함수 셀 글)

html_text = author_01.html_text
table_html = author_01.table_html

LAB = ROOT / "labs/part6/ch25-streaming/notebooks"
FIGS = ROOT / "textbook/part6/ch25-streaming/figures"
SLUG = "04-Streaming-실습"
TITLE_TEXT = "Streaming 실습: 요청 전 진행 값을 켜고 끄며 자료실 문의 답 흘려 보이기"
SRC = ROOT / "textbook/part6/ch25-streaming/_src" / (SLUG + ".html")
TOOLS_PATH = LAB / "stream_tools.py"
NB03 = LAB / "03-TTFT와-total-비교.ipynb"


# ---------------------------------------------------------------- 도구 파일 stream_tools.py (03 판 + import time + 03절 함수 셋)
IMPORT_BLOCK = """# 시각을 읽는 기능 묶음입니다(03절에서 옮긴 함수 collect_timed_events가 씁니다)
import time
"""

NEW_TOOL_PARTS = [
    ("Ch 25 03절에서 배웠습니다 — 03절 노트북 3절의 같은 이름 함수를 옮겼습니다", author_03.DEF_TIMED),
    ("Ch 25 03절에서 배웠습니다 — 03절 노트북 5절의 같은 이름 함수를 옮겼습니다", author_03.DEF_FIRST_TEXT),
    ("Ch 25 03절에서 배웠습니다 — 03절 노트북 7절의 같은 이름 함수를 옮겼습니다", author_03.DEF_THREE),
]


def tools_text() -> str:
    head = author_02.TOOLS_HEAD
    assert author_03.TOOLS.startswith(head)
    text = head + IMPORT_BLOCK + author_03.TOOLS[len(head):]
    for note, definition in NEW_TOOL_PARTS:
        text = text + "\n\n# " + note + "\n" + definition + "\n"
    return text


TOOLS = tools_text()


def check_tools() -> None:
    """도구 파일 04 판이 03 판을 그대로 잇고, 새 함수 셋이 03 노트북(교재 출력 판) 셀과 글자·AST 모두 같은지 확인합니다."""
    plain = author_02.strip_later_imports(TOOLS)
    assert plain.startswith(author_03.TOOLS), "04 판이 03 판을 그대로 잇지 않습니다"
    assert TOOLS.split('"""', 2)[2].startswith("\n" + IMPORT_BLOCK), "가져오기 줄은 머리 설명 바로 뒤에 둡니다"
    cells03 = author_03.code_cells_of(NB03)
    tree = ast.parse(TOOLS)
    names = []
    imports = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
    assert names == ["collect_events", "positions_of", "mode_order", "estimate_cost",
                     "collect_timed_events", "first_text_place", "three_times"], names
    assert imports == ["import time"], imports
    for note, definition in NEW_TOOL_PARTS:
        assert definition in cells03, "03 노트북에 같은 셀 글이 없습니다: " + definition.splitlines()[1]
        assert ("# " + note + "\n" + definition) in TOOLS
        one = ast.parse(definition).body[0]
        found = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == one.name]
        assert found == [ast.dump(one)]
        ref = [ast.dump(ast.parse(c).body[0]) for c in cells03 if c == definition]
        assert ref == [ast.dump(one)]


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = author_02.INSTALL

IMPORTS = r'''# 모델(Ch 6 01절)·그래프(Ch 13 01절)를 만드는 이름과, 진행 값을 보낼 쓰기 함수를 가져옵니다
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer
# 01~03절에서 배운 함수 다섯은 도구 파일에서 가져옵니다
from stream_tools import collect_timed_events, first_text_place, mode_order, positions_of, three_times

print("도구 파일에서 가져온 함수:", "collect_timed_events, first_text_place, mode_order, positions_of, three_times")'''

QUESTION = r'''# 오늘 처리할 자료실 문의 글과, 모델에게 줄 시스템 메시지 글을 정합니다
system_text = "자료실 이용 문의에 답하는 안내 도우미입니다. 두 문장의 한국어로 답하세요."
question_text = "빌린 책의 반납 날짜를 늘리려면 어떻게 하나요?"
print("시스템 메시지 글:", system_text)
print("문의 글:", question_text)
print("두 글의 출처: 이 절에서 실행 전에 정한 글(02절 배송 문의를 자료실 문의로 바꿈)")'''

STATE = r'''# 문의 글·답 글과, 요청 전 진행 값을 보낼지 적는 칸을 둔 상태 형식입니다(Ch 13 01절 모양, 세 칸 모두 규칙 없음)
class InquiryState(TypedDict):
    question: str
    answer: str
    show_notice: str'''

DEF_NODE = r'''# 칸 show_notice가 "yes"일 때만 모델 요청 전 진행 값을 보내고, 모델이 쓴 답 글을 칸 answer에 내는 노드입니다
def answer_inquiry(state):
    writer = get_stream_writer()
    if state["show_notice"] == "yes":
        writer({"stage": "before_model", "progress": 30})
    messages = [("system", system_text), ("user", state["question"])]
    # 모델 요청은 이 줄에서 한 번 나가고, 답을 다 받은 뒤에 다음 줄로 갑니다
    response = model.invoke(messages)
    writer({"stage": "after_model", "progress": 100})
    return {"answer": response.text}'''

BUILD = r'''# 노드 하나를 START → answer_inquiry → END로 잇고, 체크포인터 없이 컴파일합니다
builder = StateGraph(InquiryState)
builder.add_node("answer_inquiry", answer_inquiry)
builder.add_edge(START, "answer_inquiry")
builder.add_edge("answer_inquiry", END)
graph = builder.compile()
print("등록한 노드:", list(builder.nodes))'''

DEF_SCREEN = r'''# 사건을 차례로 읽어, 화면에 띄울 진행 값 목록과 이어 붙인 답 글을 딕셔너리로 내놓습니다
def screen_log(events):
    screen = {"notices": [], "text": ""}
    for mode, data in events:
        if mode == "custom":
            screen["notices"].append(data["progress"])
        # 모드 messages의 자료는 (스트림 청크, 칸 metadata) 짝이라, [0]이 스트림 청크입니다
        if mode == "messages":
            screen["text"] = screen["text"] + data[0].text
    return screen'''

DEF_REPORT = r'''# 시각을 적은 실행 기록 하나(collect_timed_events의 결과)에서, 화면 흐름을 보는 값을 한 줄씩 출력합니다
def print_report(run_record):
    events = run_record["events"]
    screen = screen_log(events)
    # 마지막 사건은 노드의 갱신이고, {노드 이름: {칸 이름: 값}} 모양입니다
    final_answer = events[-1][1]["answer_inquiry"]["answer"]
    print("모드 차례:", mode_order(events))
    print("첫 사건의 모드 이름:", events[0][0])
    print("글자가 든 첫 스트림 청크의 자리:", first_text_place(events))
    print("화면에 띄운 진행 값:", screen["notices"])
    print("화면 글과 답 글이 같은가:", screen["text"] == final_answer)'''

RUN1 = r'''# 실행 1: 요청 전 진행 값을 켜고, 모드 셋을 한 목록으로 골라 한 번 실행합니다(모델 요청 1번)
answer_modes = ["messages", "updates", "custom"]
first_input = {"question": question_text, "answer": "", "show_notice": "yes"}
# 체크포인터가 없어 설정 자리에는 None을 넘깁니다(02·03절과 같음)
first_run = collect_timed_events(graph, first_input, None, answer_modes)
first_events = first_run["events"]
print("받은 사건 수:", len(first_events))
print("사건마다 시각이 하나씩인가:", len(first_events) == len(first_run["times"]))'''

REPORT1 = r'''# 실행 1의 화면 흐름을 기록 장치로 출력합니다
print_report(first_run)'''

DETAIL1 = r'''# 실행 1의 첫 사건 자료를 보고, 화면에 쌓인 답 글을 봅니다(실행마다 달라질 수 있는 글)
print("첫 사건의 자료:", first_events[0][1])
first_screen = screen_log(first_events)
print("화면에 쌓인 답 글:")
print(first_screen["text"])'''

AGAIN = r'''# 실행 1과 같은 설정으로 한 번 더 실행하고, 기록 장치로 화면 흐름을 봅니다(모델 요청 1번)
again_run = collect_timed_events(graph, first_input, None, answer_modes)
again_events = again_run["events"]
print_report(again_run)'''

AGAIN_CMP = r'''# 같은 설정으로 보낸 두 실행의 모드 차례와 받은 사건 수를 견줍니다
print("두 실행의 모드 차례가 같은가:", mode_order(first_events) == mode_order(again_events))
print("두 실행의 받은 사건 수:", len(first_events), len(again_events))'''

RUN2 = r'''# 실행 2: 칸 show_notice 하나만 "no"로 바꿔, 같은 문의로 한 번 더 실행합니다(모델 요청 1번)
second_input = {"question": question_text, "answer": "", "show_notice": "no"}
second_run = collect_timed_events(graph, second_input, None, answer_modes)
second_events = second_run["events"]
print("받은 사건 수:", len(second_events))
print("사건마다 시각이 하나씩인가:", len(second_events) == len(second_run["times"]))'''

REPORT2 = r'''# 실행 2의 화면 흐름을 기록 장치로 출력합니다
print_report(second_run)'''

DETAIL2 = r'''# 실행 2의 첫 사건 스트림 청크와, 진행 값이 나온 자리를 봅니다(01절 함수 positions_of)
second_first = second_events[0][1]
print("첫 사건 스트림 청크의 글자 수:", len(second_first[0].text))
notice_places = positions_of(second_events, "custom")
print("진행 값의 자리가 마지막 사건 바로 앞인가:", notice_places == [len(second_events) - 1])'''

COMPARE = r'''# 세 실행의 첫 사건 모드, 글자가 든 첫 스트림 청크의 자리, 진행 값 수를 한 줄씩 견줍니다
runs = {"실행 1": first_run, "같은 설정 다시": again_run, "실행 2": second_run}
print("실행 | 첫 사건 | 글자가 든 첫 스트림 청크 자리 | 진행 값 수")
for name in runs:
    events = runs[name]["events"]
    notices = positions_of(events, "custom")
    print(name, "|", events[0][0], "|", first_text_place(events), "|", len(notices))'''

SECONDS = r'''# 세 실행의 받은 사건 수와 세 시간(초)을 한 줄씩 견줍니다(03절 함수 three_times)
print("실행 | 사건 수 | 첫 사건 시간 | 첫 토큰 도착 시간 | 전체 걸린 시간")
for name in runs:
    seconds = three_times(runs[name])
    count = len(runs[name]["events"])
    print(name, "|", count, "|", seconds["첫 사건 시간"], "|", seconds["첫 토큰 도착 시간"], "|", seconds["전체 걸린 시간"])'''

# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/04-figures.md)
FIG1 = "04-1-세-절-기능을-붙인-문의-그래프"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 초록 상자 문의 글 한 줄 칸 show_notice yes가 회색 상자 graph.stream 01절 모드 셋 목록 요청 한 번을 거쳐 파란 상자 노드 answer_inquiry 02절 진행 값 30과 100, 30은 yes일 때만으로 이어집니다. 노드에서 보라 상자 모델 gpt-5.4-mini 노드 안 invoke 한 번으로 화살표가 갑니다. 노드는 진행 값과 갱신을, 모델은 스트림 청크를 파란 상자 03절 collect_timed_events 사건마다 시각 하나로 보냅니다. 그 아래 파란 상자 기록 장치 print_report screen_log mode_order first_text_place를 거쳐 노란 상자 화면 흐름 출력 모드 차례 첫 글자 자리 진행 값 화면 글과 답 글로 이어지는 그림"
FIG1_CAP = "01절 모드 목록, 02절 진행 값, 03절 시각 적기를 한 그래프에 붙이고, 기록 장치가 사건을 화면 흐름으로 바꿔 읽습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 넣은 입력, 회색 상자는 라이브러리 메서드, 파란 상자는 우리가 적은 노드와 함수입니다.
보라 상자는 실제로 부른 모델이고, 노란 상자는 노트북 5~7절 기록 장치의 출력입니다.
상자 안의 절 번호는 그 기능을 배운 절이고, 진행 값과 갱신은 노드에서, 스트림 청크는 모델에서 옵니다.
노란 상자의 첫 글자 자리는 글자가 든 첫 스트림 청크의 자리입니다."""
FIG2 = "04-2-실행-1의-사건과-화면"
FIG2_ALT = "위에서 아래로 여섯 상자가 화살표로 이어진 그림입니다. 파란 상자 시작 시각 stream을 부르기 직전에서 노란 상자 자리 1 custom 진행 값 30 모델 요청 전 화면에 진행 표시, 노란 상자 자리 2 messages 글자 없는 스트림 청크 화면 그대로, 노란 상자 자리 3 messages 글자가 든 첫 스트림 청크 화면에 첫 글자로 이어집니다. 그 뒤 스트림 청크들과 화면 글이 이어 붙는 화살표를 지나 노란 상자 custom 진행 값 100 마지막 스트림 청크 뒤, 노란 상자 맨 끝 updates 갱신의 답 글 화면 글과 같음으로 이어지는 그림"
FIG2_CAP = "실행 1에서는 모델 요청 전 진행 값이 첫 사건이라, 화면은 첫 사건에서 처음 바뀝니다."
FIG2_READ = """위에서 아래로 실행 1의 차례대로 읽습니다.
파란 상자는 우리 함수가 시작 시각을 적은 자리이고, 노란 상자는 노트북 5절 출력으로 확인한 사건입니다.
자리 2가 글자 없는 스트림 청크라는 것은, 모드 차례와 글자가 든 첫 스트림 청크의 자리 3에서 나옵니다.
사건 수와 초는 실행마다 달라, 그림에 적지 않았습니다."""
FIG3 = "04-3-요청-전-진행-값을-끈-실행"
FIG3_ALT = "맨 위 회색 상자 세 실행 같음 같은 문의 같은 노드 모드 셋 요청 한 번씩에서 나란한 두 칸으로 화살표가 갑니다. 왼쪽 칸 실행 1 같은 설정 다시에서는 초록 상자 칸 show_notice yes가 노란 상자 모드 차례 custom messages custom updates 첫 사건 진행 값 30 첫 글자 자리 3 화면 진행 값 30과 100으로 이어집니다. 오른쪽 칸 실행 2에서는 초록 상자 칸 show_notice no가 노란 상자 모드 차례 messages custom updates 첫 사건 글자 없는 스트림 청크 첫 글자 자리 2 화면 진행 값 100으로 이어집니다. 맨 아래 회색 상자에는 세 실행 모두 화면 글과 답 글이 같음 updates가 맨 끝이 적힌 그림"
FIG3_CAP = "칸 show_notice 하나만 바꾸자, 첫 사건과 글자가 든 첫 스트림 청크의 자리, 화면에 띄운 진행 값이 달라졌습니다."
FIG3_READ = """맨 위 회색 상자는 세 실행에 같게 둔 조건입니다.
왼쪽과 오른쪽 칸은 칸 show_notice만 바꾼 나란한 설정입니다.
왼쪽 칸의 값은 실행 1과, 같은 설정으로 다시 보낸 실행에서 모두 같았습니다.
초록 상자는 넣은 값이고, 노란 상자는 노트북 5~7절 기록 장치와 7절 출력입니다.
첫 글자 자리는 글자가 든 첫 스트림 청크의 자리이고, 맨 아래 회색 상자는 세 실행 모두에서 확인한 값입니다."""
ILLU = "04-4-마디를-이은-두-홈통과-깃발"
ILLU_ALT = "흰 바탕에 긴 연두색 대나무 홈통 둘이 위아래로 나란히 놓인 그림입니다. 홈통마다 짧은 마디 셋을 이어 이음매 두 곳을 갈색 끈으로 묶었고, 낮은 나무 받침 위에서 오른쪽으로 조금 기울어 있습니다. 위 홈통은 위가 열린 반쪽 관, 아래 홈통은 둥근 관 모양입니다. 위 홈통 왼쪽 끝 옆에는 가는 대나무 막대에 단 노란 천 깃발 하나가 서 있고, 아래 홈통 왼쪽 끝 옆에는 같은 막대만 깃발 없이 서 있습니다. 두 홈통의 오른쪽 끝에서 물방울 몇 개가 작은 나무 받침 위 흰 그릇에 하나씩 떨어집니다. 글자·숫자·사람·손은 없는 그림"
ILLU_CAP = "마디 셋으로 이은 두 홈통 가운데 위 홈통에만 물보다 먼저 올린 깃발이 있고, 비유에서 두 실행의 차이는 이 깃발 하나입니다."
ILLU_READ = "긴 대나무 홈통 둘이 위아래로 나란히 있고, 두 홈통 모두 짧은 마디 셋을 끈 두 곳으로 묶어 이었습니다. 위 홈통 왼쪽 끝 옆에만 노란 깃발 하나가 서 있고, 아래 홈통 옆에는 같은 막대만 서 있습니다. 위 홈통은 위가 열린 반쪽 관, 아래 홈통은 둥근 관으로 모양이 조금 다르게 그려졌습니다. 비유에서 두 실행의 차이는 깃발 하나뿐이라, 위 홈통이 실행 1, 깃발이 없는 아래 홈통이 실행 2입니다. 마디 셋은 01·02·03절 기능이고, 끝의 흰 그릇에 떨어지는 물방울 수는 스트림 청크 수와 짝짓지 않습니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 01~03절의 모드 목록, 진행 값, 스트림 청크 이어 붙이기, 사건마다 시각 적기를 그래프 하나에 모읍니다.
2. 자료실 문의 하나를 실행하며, 화면에 띄울 진행 값과 답 글을 사건 차례대로 기록합니다.
3. 같은 설정으로 한 번 더 실행한 뒤, 모델 요청 전 진행 값 하나만 끄고 세 실행을 견줍니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 모델 요청은 5·6·7절에서 한 번씩, 모두 3번입니다.
요금표로 어림한 예상 비용은 세 요청을 합쳐 0.002달러 아래이고, 청구 금액이 아닙니다.
걸린 시간은 03절 함수로 재지만, 초와 답 글, 스트림 청크 수는 실행마다 달라질 수 있습니다.
그래서 세 실행을 견줄 때는 사건의 모드와 자리를 봅니다.

읽거나 쓰는 파일은 없고, 체크포인터도 쓰지 않습니다.
앞에서 배운 함수 다섯은 도구 파일 `stream_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 넷을 설치합니다.
판은 langchain 1.4.0과 langchain-openai 1.6.0입니다.
langgraph 1.2.11과 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**실습 범위** — 이 절은 챕터 끝 실습 절이고 30분 안에 끝나는 분량입니다.
강사와 함께 첫 셀부터 차례로 실행하고, 따로 내는 과제는 없습니다.
01~03절에서 쓴 이름과 Ch 2에서 배운 문법만 씁니다.
실행 셀 하나만 다시 실행하면 모델 요청이 한 번 더 나가고, 사건 수와 초가 달라질 수 있습니다.

실습 폴더 `labs/part6/ch25-streaming`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""

FIG1_IMAGE = "![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)"


def model_cells() -> list[dict]:
    """과정 표준 키·모델 셀(nbkit)에 이 절의 결과 읽기(실행일·문장이 달라질 수 있음)를 붙입니다."""
    cells = key_and_model_cells("openai:gpt-5.4-mini")
    cells[-1] = md("""**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.

## 2. 오늘 처리할 문의

자료실 홈페이지에 문의 창이 있다고 합시다.
이용자가 문의를 보내면, 창은 답이 다 올 때까지 기다리지 않고 받은 것부터 띄웁니다.
모델에게 요청을 보내기 전에, 「답을 준비하고 있습니다」 같은 진행 표시를 먼저 띄울 수도 있습니다.
이 절은 그 창을 코드로 흉내 내어, 무엇이 언제 화면에 뜨는지 봅니다.
다음 셀은 오늘 처리할 문의 글과 시스템 메시지 글을 정하고, 출처와 함께 출력합니다.""")
    return cells


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n" + FIG1_IMAGE + "\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이번 절은 이 챕터의 실습입니다.
01절 모드 목록, 02절 진행 값과 스트림 청크 이어 붙이기, 03절 사건마다 시각 적기를 문의 하나에 모읍니다.
첫 셀은 02·03절과 같은 패키지 넷을 설치하고, 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langchain: 1.4.0`과 `langgraph: 1.2.11`이 보입니다.
네 판 모두 실습 폴더 잠금과 같은 판입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모델을 만드는 함수 `init_chat_model`은 Ch 6 01절, 상태 형식과 그래프 이름은 Ch 13 01절과 같습니다.
함수 `get_stream_writer`는 01·02절에서 진행 값을 보낼 때 썼습니다.
마지막 가져오기 줄은 앞에서 배운 함수 다섯을 도구 파일 `stream_tools.py`에서 가져옵니다.
이 절에서 새로 배우는 이름은 없습니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: collect_timed_events, first_text_place, mode_order, positions_of, three_times`가 보입니다.
함수 `positions_of`는 01절 노트북 4절, `mode_order`는 02절 노트북 4절에서 처음 적었습니다.
함수 `collect_timed_events`·`first_text_place`·`three_times`는 03절 노트북 3·5·7절에서 처음 적었습니다.

03절 함수 셋은 이 절에서 도구 파일로 옮겼고, 설명 주석과 본문은 03절 셀 글 그대로입니다.
그래서 함수 `three_times` 안 주석의 「5절 함수」는 03절 노트북 5절을 가리킵니다.
함수 `collect_timed_events`가 기능 묶음 `time`을 쓰므로, 도구 파일 맨 위에 `import time` 줄이 생겼습니다.

앞에서 배운 함수는 `stream_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다."""),
    ] + model_cells() + [
        code(QUESTION),
        md("""**결과 읽기** — 출력 줄 `문의 글: 빌린 책의 반납 날짜를 늘리려면 어떻게 하나요?`가 보입니다.
두 글은 이 절에서 실행 전에 정했고, 결과를 보고 바꾸지 않았습니다.
시스템 메시지 글은 02절 글에서 「배송」을 「자료실 이용」으로만 바꿨습니다.
답을 두 문장으로 부탁해, 모델의 답이 짧게 끝나게 했습니다.

## 3. 재료 만들기

먼저 상태 형식을 만듭니다.
칸 `question`과 `answer`는 02절과 같고, 칸 `show_notice`를 하나 더 둡니다.
칸 `show_notice`에는 모델 요청 전에 진행 값을 보낼지를 글 `"yes"`나 `"no"`로 적습니다.
칸 구성이 02절과 달라, 상태 형식에도 새 이름을 붙입니다."""),
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 문의에 답하는 노드입니다.
02절 노드 `write_answer`와 같은 차례에, 요청 전 진행 값을 보낼지 고르는 `if` 하나를 더했습니다.
칸 `show_notice`가 `"yes"`일 때만 진행 값 30을 보내고, 진행 값 100은 늘 보냅니다."""),
        code(DEF_NODE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
진행 값 딕셔너리 둘은 02절 노드와 같은 값입니다.
칸 `show_notice`는 노드 안에서만 읽고, 모델에게 보내는 메시지 목록에는 넣지 않습니다.

다음 셀은 노드 하나를 START → answer_inquiry → END로 이어, 체크포인터 없이 컴파일합니다."""),
        code(BUILD),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['answer_inquiry']`가 보입니다.

## 4. 결과를 볼 기록 장치

화면에 무엇이 뜨는지 보려면, 받은 사건을 화면에 띄울 것으로 바꿔 읽는 장치가 있어야 합니다.
다음 셀의 함수 `screen_log`는 사건을 차례로 읽어, 진행 값은 목록에 모으고 스트림 청크의 글은 이어 붙입니다.
02절 7절에서 스트림 청크의 글을 차례로 이어 붙이던 셀을 함수 하나로 묶은 모양입니다.
글자가 없는 스트림 청크는 빈 글이라, 이어 붙여도 화면의 글이 바뀌지 않습니다."""),
        code(DEF_SCREEN),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
키 `notices`에는 진행 값의 `progress`가 받은 차례대로 쌓입니다.
키 `text`에는 스트림 청크의 글이 받은 차례대로 이어 붙습니다.

다음 셀은 실행 기록 하나를 받아, 화면 흐름을 보는 값을 한 줄씩 출력하는 함수입니다.
모드 차례는 02절 함수 `mode_order`로, 글자가 든 첫 스트림 청크의 자리는 03절 함수 `first_text_place`로 봅니다.
마지막 사건인 갱신에 담긴 답 글과, 화면에 이어 붙인 글이 같은지도 봅니다."""),
        code(DEF_REPORT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 안에서 앞 셀의 `screen_log`를 부르므로, 앞 셀을 먼저 실행해 두어야 합니다.
자리 `-1`은 03절 6절에서 본 대로 목록의 맨 끝 자리입니다.
답 글이나 초처럼 실행마다 달라지는 값은 이 함수가 출력하지 않습니다.

## 5. 실행 1 · 요청 전 진행 값을 켠 실행

실행 1은 칸 `show_notice`를 `"yes"`로 두고, 02·03절과 같은 모드 셋으로 한 번 실행합니다.
03절 함수 `collect_timed_events`로 사건마다 받은 시각도 함께 적습니다.
실행 전에 예상해 봅니다.
노드가 모델 요청 전에 진행 값을 보내니, 첫 사건은 모드 `custom`의 진행 값 30일 것입니다."""),
        code(RUN1),
        md("""**결과 읽기** — 출력 줄 `사건마다 시각이 하나씩인가: True`가 보입니다.
03절처럼 사건 목록과 시각 목록이 같은 자리끼리 짝을 이룹니다.

이번 실행에서는 출력 줄 `받은 사건 수: 62`입니다.
모델의 답이 몇 개의 스트림 청크로 나뉘어 오느냐에 따라, 이 수는 달라질 수 있습니다.

다음 셀은 앞에서 만든 기록 장치로 실행 1의 화면 흐름을 출력합니다."""),
        code(REPORT1),
        md("""**결과 읽기** — 출력 줄 `모드 차례: ['custom', 'messages', 'custom', 'updates']`는 02·03절과 같은 차례입니다.
출력 줄 `첫 사건의 모드 이름: custom`으로, 예상대로 진행 값이 첫 사건이었습니다.
출력 줄 `글자가 든 첫 스트림 청크의 자리: 3`이라, 답의 첫 글자는 셋째 사건에서 화면에 뜹니다.
출력 줄 `화면에 띄운 진행 값: [30, 100]`과 `화면 글과 답 글이 같은가: True`도 보입니다.
화면에 이어 붙인 글은 마지막 갱신의 답 글과 같았습니다.

다음 셀은 첫 사건의 자료와, 화면에 쌓인 답 글을 봅니다."""),
        code(DETAIL1),
        md("""**결과 읽기** — 출력 줄 `첫 사건의 자료: {'stage': 'before_model', 'progress': 30}`이 보입니다.
화면은 이 진행 값을 받자마자 「답을 준비하고 있습니다」 같은 표시를 띄울 수 있습니다.
이 사건은 모델 요청 전에 나오므로, 화면이 처음 바뀌기까지 걸린 시간이 첫 사건 시간입니다.

라벨 줄 `화면에 쌓인 답 글:` 아래가 이번 실행에서 화면에 쌓인 답 글입니다.
이번 실행에서는 두 문장이 두 줄로 찍혔고, 실행마다 문장이 달라질 수 있습니다.

## 6. 같은 설정으로 한 번 더

실행 2로 가기 전에, 실행 1과 같은 설정으로 한 번 더 보냅니다.
같은 설정에서도 실행마다 같은 값과 달라지는 값을 먼저 가르려는 것입니다.
실행 전에 예상해 봅니다.
모드 차례와 자리는 노드 코드가 정하니 같고, 사건 수는 달라질 수 있을 것입니다."""),
        code(AGAIN),
        md("""**결과 읽기** — 기록 장치의 다섯 출력 줄이 실행 1과 같습니다.
출력 줄 `글자가 든 첫 스트림 청크의 자리: 3`과 `화면에 띄운 진행 값: [30, 100]`이 다시 보입니다.

다음 셀은 두 실행의 모드 차례와 받은 사건 수를 견줍니다."""),
        code(AGAIN_CMP),
        md("""**결과 읽기** — 출력 줄 `두 실행의 모드 차례가 같은가: True`가 보입니다.

이번 실행에서는 출력 줄 `두 실행의 받은 사건 수: 62 60`으로, 사건 수가 두 실행에서 달랐습니다.
설정이 같아도 사건 수는 달라질 수 있어, 사건 수의 차이는 설정 탓으로 읽지 않습니다.

## 7. 실행 2 · 요청 전 진행 값만 끈 실행

값 하나만 바꿔 봅니다.
바꿀 값은 칸 `show_notice`이고, `"yes"`를 `"no"`로 바꿉니다.
문의 글, 노드, 모드 목록은 실행 1과 같습니다.
실행 전에 예상해 봅니다.
진행 값 30이 없으니 첫 사건은 모드 `messages`의 스트림 청크이고, 진행 값은 100 하나만 올 것입니다.

다음 셀은 같은 문의로 그래프를 한 번 더 실행합니다(모델 요청 1번)."""),
        code(RUN2),
        md("""**결과 읽기** — 출력 줄 `사건마다 시각이 하나씩인가: True`가 보입니다.

이번 실행에서는 출력 줄 `받은 사건 수: 60`입니다.
실행 1과 같은 문의라도, 이 수는 실행마다 달라질 수 있습니다.

다음 셀은 같은 기록 장치로 실행 2의 화면 흐름을 출력합니다."""),
        code(REPORT2),
        md("""**결과 읽기** — 출력 줄 `모드 차례: ['messages', 'custom', 'updates']`가 보입니다.
맨 앞의 `custom`이 빠졌고, 예상대로 첫 사건의 모드가 `messages`로 바뀌었습니다.
출력 줄 `글자가 든 첫 스트림 청크의 자리: 2`는 실행 1보다 한 자리 앞입니다.
출력 줄 `화면에 띄운 진행 값: [100]`이라, 화면에는 모델 요청 뒤의 진행 값만 떴습니다.
출력 줄 `화면 글과 답 글이 같은가: True`는 실행 1과 같습니다.

다음 셀은 실행 2의 첫 사건이 어떤 스트림 청크인지와, 진행 값이 나온 자리를 봅니다."""),
        code(DETAIL2),
        md("""**결과 읽기** — 출력 줄 `첫 사건 스트림 청크의 글자 수: 0`이 보입니다.
02절 5절에서 본 글자 없는 첫 스트림 청크가, 이번에는 첫 사건이 되었습니다.
이 사건을 받아도 화면의 글은 바뀌지 않고, 자리 2의 첫 글자에서 화면이 처음 바뀝니다.
출력 줄 `진행 값의 자리가 마지막 사건 바로 앞인가: True`로, 진행 값 100은 스트림 청크를 다 받은 뒤에 왔습니다.

## 8. 세 실행 견주기

세 실행을 한 표로 놓고, 무엇이 설정 탓으로 달라졌는지 봅니다.
실행 1과 같은 설정 다시 사이에서 달라진 값은, 설정이 같아도 달라지는 값입니다.
실행 1과 실행 2 사이에서만 달라진 값을, 칸 `show_notice`를 바꾼 탓으로 읽습니다.
다음 셀은 세 실행의 첫 사건 모드, 글자가 든 첫 스트림 청크의 자리, 진행 값 수를 한 줄씩 출력합니다."""),
        code(COMPARE),
        md("""**결과 읽기** — 라벨 줄 `실행 | 첫 사건 | 글자가 든 첫 스트림 청크 자리 | 진행 값 수` 아래 세 줄이 세 실행입니다.
줄 `실행 1 | custom | 3 | 2`와 `같은 설정 다시 | custom | 3 | 2`는 같습니다.
줄 `실행 2 | messages | 2 | 1`만 세 값이 모두 다릅니다.
그래서 이 세 값의 차이는 칸 `show_notice`를 바꾼 탓으로 읽습니다.

다음 셀은 세 실행의 받은 사건 수와 세 시간(초)을 한 줄씩 출력합니다."""),
        code(SECONDS),
        md("""**결과 읽기** — 라벨 줄 `실행 | 사건 수 | 첫 사건 시간 | 첫 토큰 도착 시간 | 전체 걸린 시간` 아래 세 줄이 세 실행입니다.
사건 수와 초는 같은 설정으로 보낸 두 실행 사이에서도 달라질 수 있는 값입니다.
그래서 세 실행의 초를 견주어 어느 설정이 빠르다고 말하지 않습니다.

이번 실행에서는 줄 `실행 1 | 62 | 0.003 | 0.666 | 1.055`와 `실행 2 | 60 | 0.537 | 0.568 | 0.96`입니다.
실행 2의 첫 사건은 모델이 보낸 스트림 청크라, 첫 사건 시간에 모델을 기다린 시간이 들어 있습니다.
줄 `같은 설정 다시 | 60 | 0.003 | 0.699 | 1.131`의 첫 토큰 도착 시간과 전체 걸린 시간도 실행 1과 달랐습니다.

## 정리

1. 모드 목록, 진행 값, 스트림 청크 이어 붙이기, 사건마다 시각 적기를 그래프 하나에 모아 문의 창 화면을 흉내 냈습니다.
2. 요청 전 진행 값을 켠 실행은 첫 사건이 진행 값 30이었고, 같은 설정으로 다시 보내도 모드 차례와 자리가 같았습니다.
3. 진행 값 하나만 끄자 첫 사건이 글자 없는 스트림 청크가 되어, 화면은 자리 2의 첫 글자에서 처음 바뀌었습니다.

이 절로 Ch 25가 끝납니다.
Ch 26 01절에서는 전문 에이전트를 도구로 감싸 일을 맡기는 위임 구조를 다룹니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
L_01 = "01-일곱-가지-stream-mode.html"
L_02 = "02-토큰과-중간-진행-스트리밍.html"
L_03 = "03-TTFT와-total-비교.html"
L_CH06_01 = "../../part2/ch06-langchain-start/01-계층-지도와-첫-호출.html"
L_CH13_01 = "../../part4/ch13-langgraph-basics/01-StateGraph와-노드-엣지.html"
L_CH24_04 = "../ch24-human-in-the-loop/04-Human-in-the-Loop-실습.html"
L_CH26_01 = "../ch26-delegation/01-Subagent-도구-위임.html"
L_CH30_04 = "../../part7/ch30-fastapi-serving/04-astream과-응답-스트림.html"
L_CH30_09 = "../../part7/ch30-fastapi-serving/09-실제-Agent-HTTP-통합.html"


def link(href: str, label: str) -> str:
    return '<a href="' + href + '">' + label + "</a>"


LEARNED_ROWS = [
    (link(L_01, "01절"), "스트림 모드를 목록으로 골라 한 실행에서 함께 받기, 사건 하나 = (모드 이름, 자료) 짝, 함수 <code>positions_of</code>(도구 파일)",
     "모드 셋 목록 <code>answer_modes</code>, 함수 <code>screen_log</code>의 <code>for mode, data in events</code>, 7·8절 진행 값의 자리와 수"),
    (link(L_02, "02절"), "노드 안 <code>get_stream_writer</code>로 진행 값 보내기, 모델을 부르는 노드와 스트림 청크, 스트림 청크 글 이어 붙이기, 함수 <code>mode_order</code>(도구 파일)",
     "노드 <code>answer_inquiry</code>의 진행 값 30·100, 함수 <code>screen_log</code>의 화면 글, 기록 장치의 모드 차례"),
    (link(L_03, "03절"), "사건마다 시각 적기(<code>collect_timed_events</code>), 글자가 든 첫 스트림 청크 자리(<code>first_text_place</code>), 세 시간(<code>three_times</code>) — 이 절에서 도구 파일로 옮김",
     "세 번의 실행, 기록 장치의 첫 글자 자리, 8절 세 시간 표"),
    (link(L_CH06_01, "Ch 6 01절") + "·" + link(L_CH13_01, "Ch 13 01절"), "모델 만들기, 상태 형식·노드·엣지로 그래프 만들기",
     "준비 셀과 그래프 조립"),
    (link(L_CH24_04, "Ch 24 04절"), "자료실 대출 연장 신청 소재", "오늘 처리할 문의 글(이 절에서 실행 전에 정함)"),
]

RESULT_ROWS = [
    ("실행 1", "<code>\"yes\"</code>", "custom · messages · custom · updates", "custom 진행 값 30", "3", "[30, 100]", "True"),
    ("같은 설정 다시", "<code>\"yes\"</code>", "custom · messages · custom · updates", "custom 진행 값 30", "3", "[30, 100]", "True"),
    ("실행 2", "<code>\"no\"</code>", "messages · custom · updates", "messages 글자 없는 스트림 청크", "2", "[100]", "True"),
]

LOOK_B5 = "노트북 5절 기록 장치 출력에서 <code>첫 사건의 모드 이름: custom</code>과 <code>화면에 띄운 진행 값: [30, 100]</code>을 봅니다. 7절에서 <code>글자가 든 첫 스트림 청크의 자리: 2</code>와 <code>첫 사건 스트림 청크의 글자 수: 0</code>을 확인합니다. 교재 출력에서는 실행 1의 사건이 62개, 실행 2의 사건이 60개였고, 다시 실행하면 달라질 수 있습니다."
LOOK_B6 = "노트북 8절 첫 표에서 줄 <code>실행 2 | messages | 2 | 1</code>만 다른지 봅니다. 교재 출력의 첫 토큰 도착 시간은 실행 1 0.666초, 같은 설정 다시 0.699초, 실행 2 0.568초였습니다. 따로 보낸 요청의 초라, 다시 실행하면 세 값의 크기 차례도 바뀔 수 있습니다."
RUNS_B6 = "새 커널로 세 번 실행해 견주자, 사건 수·답 글·초가 찍힌 셀 다섯은 실행에 따라 달랐습니다. 모드 차례·자리·진행 값·<code>True</code>가 찍힌 나머지 셀 열다섯은 세 번 모두 같았습니다."


def mermaid_block(name: str, alt: str, caption: str, reading: str) -> str:
    """그림 파일(SVG)과 글이 있을 때만 본문에 넣습니다(첫 실행 때는 그림이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (name + ".svg")).is_file() or not alt or not reading:
        return ""
    return author_01.mermaid_block(name, alt, caption, reading)


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


def src_html() -> str:
    learned = table_html(["절", "배운 것", "실습에서 쓰는 곳"], LEARNED_ROWS)
    results = table_html(["실행", "칸 <code>show_notice</code>", "모드 차례", "첫 사건", "글자가 든 첫 스트림 청크 자리", "화면에 띄운 진행 값", "화면 글 == 답 글"], RESULT_ROWS)
    return """<!--meta: 실습 30분 | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 0 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>모드 목록·진행 값·스트림 청크 이어 붙이기·시각 적기를 그래프 하나에 모아, 문의 답을 흘려 보일 수 있습니다.</li>
<li>기록 장치의 출력으로 첫 사건의 모드, 글자가 든 첫 스트림 청크의 자리, 화면에 띄운 진행 값을 읽을 수 있습니다.</li>
<li>같은 설정으로 다시 보낸 실행과 값 하나를 바꾼 실행을 견주어, 설정 탓으로 달라진 값을 가를 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>이 챕터에서는 스트리밍을 절마다 따로 익혔습니다. """ + link(L_01, "01절") + """은 스트림 모드를 목록으로 골라 한 실행에서 함께 받았습니다. """ + link(L_02, "02절") + """은 모델을 부르는 노드에서 진행 값과 스트림 청크를 함께 받고, 스트림 청크의 글을 이어 붙였습니다. """ + link(L_03, "03절") + """은 사건마다 받은 시각을 적어 세 시간을 쟀습니다. 실제 문의 창에서는 이 일들이 한 번의 요청 안에서 함께 일어납니다.</p>
<p>이번 실습은 세 절의 기능을 자료실 문의 하나에 모아, 문의 창 화면을 코드로 흉내 냅니다. 같은 설정으로 한 번 더 보낸 뒤, 모델 요청 전 진행 값 하나만 끄고 다시 실행합니다. """ + link(L_02, "02절") + """ 8절은 모드 <code>messages</code>를 빼 보았고, """ + link(L_03, "03절") + """ 9절은 모드 목록의 차례를 바꿔 보았습니다. 새로 볼 것은 요청 전 진행 값이 없을 때, 첫 사건이 무엇이 되고 화면이 몇 번째 사건에서 처음 바뀌는지입니다.</p>
<p>이번 절은 이 챕터의 실습입니다. 01~03절에서 쓴 이름과 Ch 2에서 배운 문법만 쓰고, 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p>
<p><strong>이 절의 질문</strong> — 세 절의 기능을 한 그래프에 붙이면, 문의 하나의 답은 어떤 차례로 화면에 뜰까요? 모델 요청 전 진행 값 하나를 끄면, 화면이 처음 바뀌는 사건은 어떻게 달라질까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>이번 실습은 아래 절에서 배운 이름을 그대로 씁니다. 함수는 도구 파일 <code>stream_tools.py</code>에서 가져오고, 상태 형식·노드·기록 장치 함수는 노트북에 적습니다.</p>
""" + learned + """
<p>붙인 기능은 01절 모드 목록, 02절 진행 값과 스트림 청크 이어 붙이기, 03절 사건마다 시각 적기 셋입니다. 세 기능이 모두 흐름 안에서 일하도록, 문의 창이 받은 사건을 화면에 띄울 것으로 바꿔 읽게 했습니다. 모드 목록은 세 실행 모두 같은 <code>["messages", "updates", "custom"]</code>이고, 기록 장치가 사건을 (모드 이름, 자료) 짝으로 풉니다. 진행 값은 화면에 띄운 진행 값 목록이 되고, 스트림 청크의 글은 화면 글로 이어 붙습니다. 사건마다 적은 시각은 8절에서 세 시간이 됩니다.</p>
<p>01절의 일곱 모드 전부와 체크포인터, 멈춤 표시는 문의 창 화면에 쓰이지 않아 뺐습니다. 02절 칸 <code>metadata</code> 읽기는 노드가 하나라 노드 이름으로 거를 일이 없어 뺐습니다. 02절의 모드 <code>messages</code>를 뺀 실행과 03절의 목록 차례 바꾸기는 앞 절 실험을 되풀이하게 되어 뺐습니다. 03절의 예상 비용과 두 구간 나누기도 화면에 띄울 값이 아니라 뺐습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절부터 대나무 홈통에 물을 흘려 그릇에 받는 모습으로 스트리밍을 보았습니다. 이번에는 짧은 홈통 세 마디를 끈으로 묶어 긴 홈통 하나로 잇습니다. 마디마다 01·02·03절에서 익힌 기능이 하나씩 들어 있다고 봅니다. 긴 홈통 윗머리 옆에는 물이 닿기 전에 먼저 올리는 작은 깃발을 세웁니다.</p>
""" + illustration_block() + """<p>긴 홈통이 이 절의 그래프이고, 끝의 그릇이 문의 창 화면입니다. 깃발은 모델 요청 전 진행 값이고, """ + link(L_02, "02절") + """ 그림의 종처럼 물보다 먼저 화면에 알립니다. 실행 2는 깃발만 뺀 홈통에 같은 물을 흘리는 일입니다.</p><p>비유와 다른 점이 있습니다. 홈통에서 깃발을 빼면, 그릇에 처음 닿는 것은 물방울입니다. 그래프에서 진행 값을 빼면, 첫 사건은 글자 없는 스트림 청크가 됩니다. 그래서 화면은 첫 사건이 아니라 둘째 사건에서 처음 바뀝니다.</p>
<h3>실습 조립의 구성</h3>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>화면이 처음 바뀌는 사건</h3><p>화면이 처음 바뀌는 사건은, 화면에 띄울 것이 든 첫 사건입니다. 진행 값은 받자마자 진행 표시를 띄울 수 있고, 글자가 든 스트림 청크는 답 글을 늘립니다. 글자가 없는 스트림 청크는 받아도 화면이 그대로입니다. """ + link(L_03, "03절") + """에서 본 대로, 시각은 사건 차례대로 적습니다.</p><p>그래서 모델 요청 전 진행 값이 있으면 화면은 첫 사건에서 바뀌고, 그때까지가 첫 사건 시간입니다. 진행 값이 없으면 첫 사건은 글자 없는 스트림 청크이고, 화면은 글자가 든 첫 스트림 청크에서 처음 바뀝니다. 그때까지가 첫 토큰 도착 시간입니다. 이 절은 초가 아니라 이 자리의 차이로 두 설정을 견줍니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 오늘 처리할 문의 글과 시스템 메시지 글을 정합니다. 칸 셋의 상태 형식과 노드 하나짜리 그래프를 만들고, 사건을 화면에 띄울 것으로 바꿔 읽는 기록 장치 함수 둘을 적습니다. 실행 1은 요청 전 진행 값을 켜고, 6절은 같은 설정으로 한 번 더 보냅니다. 실행 2는 진행 값 하나만 끄고, 8절에서 세 실행을 견줍니다.</p><p>실제 OpenAI 모델 <code>gpt-5.4-mini</code>를 temperature 0으로 부릅니다. 모델 요청은 5·6·7절에서 한 번씩, 모두 3번입니다. 요금표로 어림한 예상 비용은 0.002달러 아래이고, 청구 금액이 아닙니다. 초와 답 글, 스트림 청크 수는 실행마다 달라질 수 있습니다. 읽거나 쓰는 파일은 없습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
<h3>실행 1의 실제 순서</h3>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>세 실행은 문의 글·노드·모드 목록이 같고, 칸 <code>show_notice</code>만 실행 2에서 달랐습니다. 아래 표는 노트북 5~8절 출력에서 세 실행 모두 코드가 정하는 값만 모은 것입니다.</p>
""" + results + """
<p>같은 설정으로 다시 보낸 실행은 표의 값이 모두 실행 1과 같았습니다. 실행 2는 모드 차례에서 맨 앞 <code>custom</code>이 빠졌고, 첫 사건은 글자 없는 스트림 청크였습니다. 글자가 든 첫 스트림 청크는 자리 3에서 자리 2로 한 자리 당겨졌습니다. 화면에 띄운 진행 값은 <code>[100]</code> 하나였고, 그 진행 값은 스트림 청크를 다 받은 뒤에 왔습니다.</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>세 실행 모두 화면에 이어 붙인 글이 마지막 갱신의 답 글과 같았습니다. 진행 값을 꺼도 스트림 청크를 이어 붙이는 일은 달라지지 않았습니다. 달라진 것은 화면이 처음 바뀌기 전에 무엇이 오느냐입니다. 실행 1에서는 모델 요청 전의 진행 값이, 실행 2에서는 글자 없는 스트림 청크가 먼저 왔습니다.</p><p>사건 수와 초는 같은 설정으로 보낸 두 실행 사이에서도 달라질 수 있는 값입니다. 그래서 세 실행의 초를 견주어 어느 설정이 빠르다고 말하지 않습니다. """ + RUNS_B6 + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>문의 글과 시스템 메시지 글은 이 절에서 실행 전에 정한 예입니다. """ + link(L_CH24_04, "Ch 24 04절") + """의 대출 연장 소재를 이어 받았고, 실제 이용자가 보낸 글이 아닙니다. 시스템 메시지 글은 02절 글에서 「배송」만 「자료실 이용」으로 바꿨습니다.</li><li>노트북을 쓰기 전에 문의와 판단 규칙을 적어 두고, 노트북 밖에서 실행 1 설정과 실행 2 설정을 다섯 번씩 보냈습니다. 열 번 모두 모드 차례, 첫 사건, 글자가 든 첫 스트림 청크의 자리, 화면에 띄운 진행 값이 설정마다 같았습니다. 첫 후보가 규칙을 채워, 미리 적어 둔 둘째 후보(02절 배송 문의 그대로)는 보내지 않았습니다.</li><li>노트북 밖 다섯 번씩에서는 실행 2 설정의 첫 사건 시간이 실행 1 설정보다 늘 컸습니다. 따로 보낸 요청의 초라서, 이 절의 결론에는 쓰지 않았습니다.</li><li>실행 2는 첫 사건과 글자가 든 첫 스트림 청크가 이웃한 자리라, 두 시간이 셋째 자리까지 같게 찍힐 수 있습니다. 노트북 밖 다섯 번 가운데 한 번이 그랬습니다. 시각을 사건 차례대로 적으므로, 첫 사건 시간이 첫 토큰 도착 시간보다 클 수는 없습니다.</li><li>칸 <code>show_notice</code>는 참·거짓 값 대신 글 <code>"yes"</code>·<code>"no"</code>로 적었습니다. 01~03절에서 쓴 모양만 쓰려고 정한 것입니다.</li><li>함수 <code>print_report</code>는 마지막 사건이 노드의 갱신이라고 보고 자리 <code>-1</code>을 읽습니다. 모드 목록에 <code>updates</code>가 없으면 이 줄에서 셀이 오류로 멈춥니다. 이번에 실행하지 않았습니다.</li><li>걸린 시간은 03절 함수로 쟀지만, 조건마다 한 번씩만 보냈습니다. 여러 번 재어 가운데 값을 보지 않았고, 스트리밍하지 않은 실행과도 견주지 않았습니다.</li><li>요청 전 진행 값을 끄면 이용자가 빈 화면을 얼마나 오래 보는지는, 초를 여러 번 재어야 말할 수 있습니다. 이번에는 사건의 자리까지만 보았습니다.</li><li>모델이 쓴 답 글과 잰 초에는 <code>assert</code>를 걸지 않았습니다. 이 노트북의 <code>assert</code>는 키 확인 셀 하나뿐입니다.</li><li>비동기 메서드 <code>astream</code>, 인자 <code>version="v2"</code>, 노드가 여럿인 그래프의 스트리밍은 이번에도 실행하지 않았습니다.</li><li>예상 비용은 2026-09-17 요금표로 어림한 값이고, 청구 금액이 아닙니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>모드 목록, 진행 값, 스트림 청크 이어 붙이기, 사건마다 시각 적기를 그래프 하나에 모아 문의 창 화면을 흉내 냈습니다.</li><li>요청 전 진행 값을 켠 실행은 첫 사건이 진행 값 30이었고, 같은 설정으로 다시 보내도 모드 차례와 자리가 같았습니다.</li><li>진행 값 하나만 끄자 첫 사건이 글자 없는 스트림 청크가 되어, 화면은 자리 2의 첫 글자에서 처음 바뀌었습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 25가 끝납니다. """ + link(L_CH26_01, "Ch 26 01절") + """에서는 전문 에이전트를 도구로 감싸 일을 맡기는 위임 구조를 다룹니다. """ + link(L_CH30_04, "Ch 30 04절") + """은 모드 <code>custom</code>의 사건을 비동기 메서드 <code>astream</code>으로 받아 이어 붙입니다. """ + link(L_CH30_09, "09절") + """은 모드 <code>messages</code>의 스트림 청크를 같은 메서드로 받아 서버 응답으로 보냅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. [하] 실행 1의 첫 사건이 진행 값 30이었던 까닭은 무엇인가요?</p><p class="quiz-a">노드가 칸 <code>show_notice</code>가 <code>"yes"</code>일 때 모델 요청보다 먼저 진행 값 30을 보냈기 때문입니다. 틀렸다면 노트북 3절 노드 셀과 5절을 다시 읽습니다.</p><p class="quiz-q">2. [중] 실행 2의 첫 사건은 무엇이었고, 화면은 몇 번째 사건에서 처음 바뀌었나요?</p><p class="quiz-a">첫 사건은 글자가 없는 스트림 청크였습니다. 이 사건으로는 화면 글이 바뀌지 않아, 화면은 자리 2의 글자가 든 첫 스트림 청크에서 처음 바뀌었습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">3. [중] 실행 2로 가기 전에 같은 설정으로 한 번 더 보낸 까닭은 무엇인가요?</p><p class="quiz-a">설정이 같아도 달라지는 값과 늘 같은 값을 먼저 가르려는 것입니다. 모드 차례와 자리는 같았고, 사건 수와 초는 달라질 수 있는 값이었습니다. 그래서 실행 2에서 달라진 자리만 설정 탓으로 읽습니다. 틀렸다면 노트북 6·8절을 다시 읽습니다.</p><p class="quiz-q">4. [상] 동료가 「요청 전 진행 값을 끄면 답이 더 빨리 온다」고 말합니다. 이 절 결과로 무엇이라고 답하나요?</p><p class="quiz-a">이 절 결과로는 말할 수 없다고 답합니다. 초는 따로 보낸 요청마다 한 번씩만 쟀고, 같은 설정으로 다시 보낸 실행에서도 달라질 수 있었습니다. 이 절이 보인 것은 첫 사건과 화면이 처음 바뀌는 자리의 차이입니다. 틀렸다면 노트북 8절과 03절 노트북 9절 설명을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li>01절 — 스트림 모드를 목록으로 골라 한 실행에서 함께 받기, 함수 <code>positions_of</code>.</li><li>02절 — 진행 값과 스트림 청크, 스트림 청크 이어 붙이기, 함수 <code>mode_order</code>.</li><li>03절 — 사건마다 시각 적기, 함수 <code>collect_timed_events</code>·<code>first_text_place</code>·<code>three_times</code>.</li><li><div><a href="https://docs.langchain.com/oss/python/langgraph/streaming">LangGraph Streaming</a></div>03절 참고 자료와 같은 문서입니다. 모드를 목록으로 골라 여러 모드를 함께 받는 방법이 있습니다.</li><li>Ch 6 06절 — 요금표와 예상 비용. Ch 24 04절 — 대출 연장 소재.</li><li>기준 버전은 노트북 1절 첫 셀에서 설치한 패키지 넷의 판입니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    check_tools()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "stream_tools.py").write_text(TOOLS, encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        # 도구 파일은 없거나 03 판이거나 이 판과 같을 때만 쓴다. 뒤 절이 함수를 더한 판이면 덮어쓰지 않는다(Ch 24 마감 A-10).
        current = ""
        if TOOLS_PATH.is_file():
            current = TOOLS_PATH.read_text(encoding="utf-8")
        plain = author_02.strip_later_imports(current)
        assert current == "" or plain.startswith(author_03.TOOLS), "도구 파일이 03절 판으로 시작하지 않습니다"
        if current == "" or current == author_03.TOOLS or current == TOOLS:
            TOOLS_PATH.write_text(TOOLS, encoding="utf-8")
            print("wrote", TOOLS_PATH)
        else:
            assert current.startswith(TOOLS), "도구 파일이 04절 판으로 시작하지 않습니다"
            print("skip", TOOLS_PATH, "(뒤 판이 함수를 더한 판 — 덮어쓰지 않음)")
        path = write_notebook(LAB, "04", SLUG, "experiment", cells())
        print("wrote", path)
