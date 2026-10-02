"""Ch 25 03절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 -B author_03.py            → 도구 파일(없거나 02 판·03 판일 때만) + 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_03.py --src-only → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_03.py --tools-copy DIR → 도구 파일만 DIR에 쓴다(새 커널 사본 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**. 슬러그 그대로(Part 6 목차만 링크).

## 결정 1 — T1: 한 실행에 세 모드를 함께 받아, 한 요청 안에서 세 시간을 잰다 (챕터 리드 결정 8)

02절 그래프(상태 형식·시스템 메시지 글·노드·그래프 셀 — author_02 셀 글 그대로, 02 노트북과 문자열 대조)를
stream_mode=["messages", "updates", "custom"] 한 번으로 실행하며, 새 함수 collect_timed_events가 사건을 꺼낼 때마다
time.perf_counter()로 시각을 적는다. 첫 사건 시간(자리 1 — 진행 값 30, 모델 요청 전) · 첫 토큰 도착 시간(Ch 15 05 정의 —
글자가 든 첫 스트림 청크, 자리 3) · 전체 걸린 시간(for가 끝난 뒤 끝 시각). 모드마다 따로 요청하지 않는다(옛 판의 결함 — 02 확인:
messages를 고르지 않으면 노드 안 invoke가 스트리밍 요청을 보내지 않음).

## 결정 2 — 걸린 시간은 이 절의 주제라 잰다(규격 §3 주제 절 예외), 결론은 차례에만 (규격 §2-7 9번 끝)

노트북 밖 흔들림 확인(03-probe.md, 요청 10번)에서 모드 차례·첫 사건·자리 2(글자 0)·자리 3·두 부등식 True가 10/10 같았다.
결론·그림은 이 값에만. 초·비율·사건 수·출력 토큰·예상 비용·답 글은 결과 읽기 둘째 단락·b6 표·「확인할 점」에만
([[…]] 자리 표시 → 교재 출력 실행 뒤 mdpatch.py로 채움). 모델 글·잰 값·비용에 건 assert 없음.

## 결정 3 — 도구 파일 stream_tools.py에 함수 둘을 더한다 (챕터 리드 결정 5 · §2-7 3번)

02 판(collect_events·positions_of) 뒤에 mode_order(02 노트북 4절 셀 글 그대로)와 estimate_cost(Ch 6 06 — Ch 21 runner_tools.py
판 본문 글자 그대로)를 덧붙인다. check_tools()가 문자열·AST로 대조한다. 02 생성기는 02 판으로 시작하는 긴 판을 덮어쓰지 않는다.
collect_timed_events·first_text_place·three_times는 이 절에서 처음 가르치므로 노트북에 둔다.

## 결정 4 — 값 바꿔 보기: 모드 목록의 차례만 바꾼다 (인계 10항, 03-probe.md R3 5/5)

["updates", "messages", "custom"] — 모드 차례·첫 사건·자리 3은 목록 차례와 관계없이 노드 코드가 정한다. 요청 1.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`(도구 파일 estimate_cost 안은 Ch 6 06 본문 그대로)·`+=`·기본값 매개변수·
타입힌트(상태 형식 칸 말고)·반환 힌트·대입 풀기·별표 풀기·`while`·`try`·세미콜론·`isinstance`·데코레이터·클래스(상태 형식 말고)·
`join`·`astream`·체크포인터·식 안 요금 숫자.
"""
from __future__ import annotations

import ast
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nbkit import RUN_DATE, code, key_and_model_cells, md, setup, write_notebook  # noqa: E402
import author_01  # noqa: E402  (html_text·table_html·mermaid_block·링크)
import author_02  # noqa: E402  (02 그래프 셀 글·도구 파일 02 판·설치 셀)

html_text = author_01.html_text
table_html = author_01.table_html
mermaid_block = author_01.mermaid_block

LAB = ROOT / "labs/part6/ch25-streaming/notebooks"
FIGS = ROOT / "textbook/part6/ch25-streaming/figures"
SLUG = "03-TTFT와-total-비교"
TITLE_TEXT = "TTFT와 total 비교"
SRC = ROOT / "textbook/part6/ch25-streaming/_src" / (SLUG + ".html")
TOOLS_PATH = LAB / "stream_tools.py"
NB02 = LAB / "02-토큰과-중간-진행-스트리밍.ipynb"
CH21_TOOLS = ROOT / "labs/part6/ch21-create-agent/notebooks/runner_tools.py"


# ---------------------------------------------------------------- 도구 파일 stream_tools.py (02 판 + 둘)
def ch21_estimate_cost_text() -> str:
    """Ch 21 runner_tools.py에서 estimate_cost의 설명 주석 둘과 정의를 글자 그대로 꺼냅니다(첫 머리줄은 뺌)."""
    lines = CH21_TOOLS.read_text(encoding="utf-8").splitlines()
    tree = ast.parse("\n".join(lines))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "estimate_cost":
            start = node.lineno - 1
            head = start
            while head > 0 and lines[head - 1].startswith("#"):
                head = head - 1
            block = lines[head:node.end_lineno]
            assert block[0].startswith("# Ch 6 06절에서 배웠습니다"), block[0]
            return "\n".join(block[1:])
    raise SystemExit("Ch 21 runner_tools.py에 estimate_cost가 없습니다")


DEF_COST = ch21_estimate_cost_text()

NEW_TOOL_PARTS = [
    ("Ch 25 02절에서 배웠습니다 — 02절 노트북 4절의 같은 이름 함수를 옮겼습니다", author_02.DEF_ORDER),
    ("Ch 6 06절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다", DEF_COST),
]


def tools_text() -> str:
    text = author_02.TOOLS
    for note, definition in NEW_TOOL_PARTS:
        text = text + "\n\n# " + note + "\n" + definition + "\n"
    return text


TOOLS = tools_text()


def code_cells_of(path: Path) -> list[str]:
    nb = json.loads(path.read_text(encoding="utf-8"))
    out = []
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source = cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
            out.append(source)
    return out


def check_tools() -> None:
    """도구 파일의 새 함수 둘이 앞 판(02 노트북 셀 · Ch 21 도구 파일)과 글자·AST 모두 같은지, 02 판으로 시작하는지 확인합니다."""
    assert TOOLS.startswith(author_02.TOOLS)
    cells02 = code_cells_of(NB02)
    assert author_02.DEF_ORDER in cells02, "02 노트북에 mode_order 셀 글이 없습니다"
    ch21 = CH21_TOOLS.read_text(encoding="utf-8")
    assert DEF_COST in ch21, "Ch 21 runner_tools.py 판과 글이 다릅니다"
    tree = ast.parse(TOOLS)
    names = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
    assert names == ["collect_events", "positions_of", "mode_order", "estimate_cost"], names
    ch21_tree = ast.parse(ch21)
    for note, definition in NEW_TOOL_PARTS:
        assert ("# " + note + "\n" + definition) in TOOLS
        one = ast.parse(definition).body[0]
        found = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == one.name]
        assert found == [ast.dump(one)]
    ref = [ast.dump(n) for n in ch21_tree.body if isinstance(n, ast.FunctionDef) and n.name == "estimate_cost"]
    assert ref == [ast.dump(ast.parse(DEF_COST).body[0])]
    # 이 판(03절 판, 상수 TOOLS)은 아무것도 가져오지 않습니다. 04절 판은 머리 설명 뒤에 import time 한 줄을 더했습니다
    assert "import" not in TOOLS.split('"""', 2)[2], "03절 판 도구 파일은 아무것도 가져오지 않습니다"


def check_same_as_02() -> None:
    """02절과 같은 코드라고 적는 셀 넷이 02 노트북(교재 출력 판)의 셀 글과 문자열·AST 모두 같은지 확인합니다."""
    cells02 = code_cells_of(NB02)
    for source in (author_02.STATE, author_02.SYSTEM, author_02.DEF_NODE, author_02.BUILD):
        assert source in cells02, source.splitlines()[0]
        assert ast.dump(ast.parse(source)) in [ast.dump(ast.parse(c)) for c in cells02 if c == source]


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = author_02.INSTALL

IMPORTS = r'''# 시각을 읽는 기능 묶음(Ch 6 06절)과, 02절 그래프를 만드는 이름을 가져옵니다
import time
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer
# 앞에서 배운 함수 셋은 도구 파일에서 가져옵니다
from stream_tools import estimate_cost, mode_order, positions_of

print("도구 파일에서 가져온 함수:", "estimate_cost, mode_order, positions_of")'''

STATE = author_02.STATE
SYSTEM = author_02.SYSTEM
DEF_NODE = author_02.DEF_NODE
BUILD = author_02.BUILD

DEF_TIMED = r'''# 그래프를 한 번 실행하며, 사건을 꺼낼 때마다 그때의 시각을 적어 딕셔너리로 내놓습니다
def collect_timed_events(graph_to_run, graph_input, config, modes):
    # 메서드 stream을 부르기 직전의 시각을 시작 시각으로 적습니다
    timed_run = {"start": time.perf_counter(), "events": [], "times": []}
    for event in graph_to_run.stream(graph_input, config, stream_mode=modes):
        timed_run["events"].append(event)
        # 사건을 담은 바로 뒤에 시각을 적어, 두 목록의 자리를 맞춥니다
        timed_run["times"].append(time.perf_counter())
    timed_run["end"] = time.perf_counter()
    return timed_run'''

RUN = r'''# 모드 셋을 한 목록으로 골라 한 번 실행하며, 사건마다 시각을 적습니다(모델 요청 1번)
answer_input = {"question": "주문한 책이 아직 오지 않았어요. 언제 받을 수 있나요?", "answer": ""}
answer_modes = ["messages", "updates", "custom"]
# 체크포인터가 없어 설정 자리에는 None을 넘깁니다(02절과 같음)
timed_run = collect_timed_events(graph, answer_input, None, answer_modes)
answer_events = timed_run["events"]
event_times = timed_run["times"]
print("받은 사건 수:", len(answer_events))
print("사건마다 시각이 하나씩인가:", len(answer_events) == len(event_times))
print("모드 차례:", mode_order(answer_events))'''

FIRST_EVENT = r'''# 첫 사건의 모드와 자료를 보고, 시작부터 첫 사건까지 걸린 시간(초)을 계산합니다
start_time = timed_run["start"]
first_event_seconds = round(event_times[0] - start_time, 3)
print("첫 사건의 모드 이름:", answer_events[0][0])
print("첫 사건의 자료:", answer_events[0][1])
print("첫 사건 시간(초):", first_event_seconds)'''

FIRST_MSG = r'''# 모드 messages의 첫 사건이 몇 번째인지와, 그 스트림 청크의 글자 수를 봅니다(01절 함수 positions_of)
message_places = positions_of(answer_events, "messages")
first_message = answer_events[message_places[0] - 1][1]
print("모드 messages 첫 사건의 자리:", message_places[0])
print("그 스트림 청크의 글자 수:", len(first_message[0].text))'''

DEF_FIRST_TEXT = r'''# 사건 목록에서 글자가 든 첫 스트림 청크가 몇 번째(1부터 셈) 사건인지 내놓습니다
def first_text_place(events):
    for index in range(len(events)):
        mode = events[index][0]
        data = events[index][1]
        # 모드 messages의 자료는 (스트림 청크, 칸 metadata) 짝이라, [0]이 스트림 청크입니다
        if mode == "messages" and data[0].text != "":
            return index + 1
    # 끝까지 찾지 못하면 None을 내놓습니다
    return None'''

FIRST_TOKEN = r'''# 글자가 든 첫 스트림 청크의 자리를 찾고, 시작부터 그 사건까지 걸린 시간(초)을 계산합니다
text_place = first_text_place(answer_events)
# 자리는 1부터 세므로, 시각 목록에서는 한 칸 앞 [text_place - 1]에 있습니다
text_time = event_times[text_place - 1]
first_token_seconds = round(text_time - start_time, 3)
print("글자가 든 첫 스트림 청크의 자리:", text_place)
print("첫 토큰 도착 시간(초):", first_token_seconds)'''

TOTAL = r'''# 마지막 사건의 모드를 보고, 시작부터 끝 시각까지 걸린 시간(초)을 계산합니다
end_time = timed_run["end"]
total_seconds = round(end_time - start_time, 3)
# 자리 -1은 목록의 맨 끝 사건입니다
print("마지막 사건의 모드 이름:", answer_events[-1][0])
print("전체 걸린 시간(초):", total_seconds)'''

ORDER = r'''# 세 시각을 차례대로 견줍니다(사건을 받은 차례로 정해지는 크기 관계)
print("첫 사건 시각이 글자가 든 첫 스트림 청크 시각보다 앞인가:", event_times[0] < text_time)
print("글자가 든 첫 스트림 청크 시각이 끝 시각보다 앞인가:", text_time < end_time)'''

DEF_THREE = r'''# 시각을 적은 실행 기록(collect_timed_events의 결과)에서 세 시간(초)을 계산해 딕셔너리로 내놓습니다
def three_times(run_record):
    start_at = run_record["start"]
    # 5절 함수로 글자가 든 첫 스트림 청크의 자리를 찾습니다
    place = first_text_place(run_record["events"])
    text_at = run_record["times"][place - 1]
    seconds = {"첫 사건 시간": round(run_record["times"][0] - start_at, 3)}
    seconds["첫 토큰 도착 시간"] = round(text_at - start_at, 3)
    seconds["전체 걸린 시간"] = round(run_record["end"] - start_at, 3)
    return seconds'''

THREE_RUN = r'''# 3절 실행의 세 시간을 함수로 계산하고, 4~6절에서 하나씩 계산한 값과 견줍니다
answer_seconds = three_times(timed_run)
earlier_seconds = {"첫 사건 시간": first_event_seconds}
earlier_seconds["첫 토큰 도착 시간"] = first_token_seconds
earlier_seconds["전체 걸린 시간"] = total_seconds
print("세 시간(초):", answer_seconds)
print("4~6절에서 계산한 값과 같은가:", answer_seconds == earlier_seconds)'''

SPLIT = r'''# 첫 글자를 받기까지 기다린 시간과, 첫 글자 뒤 끝날 때까지 걸린 시간을 나눠 봅니다
after_text_seconds = round(end_time - text_time, 3)
print("구간 | 초")
print("시작부터 첫 글자까지 |", first_token_seconds)
print("첫 글자부터 끝까지 |", after_text_seconds)'''

USAGE = r'''# 사용량이 든 스트림 청크를 찾아, 3절 요청 한 번의 토큰 수를 봅니다
answer_usage = None
usage_count = 0
for mode, data in answer_events:
    if mode == "messages" and data[0].usage_metadata is not None:
        answer_usage = data[0].usage_metadata
        usage_count = usage_count + 1
print("사용량이 든 스트림 청크 수:", usage_count)
print("입력 토큰 수:", answer_usage["input_tokens"])
print("캐시 입력 토큰 수:", answer_usage["input_token_details"]["cache_read"])
print("출력 토큰 수:", answer_usage["output_tokens"])'''

PRICES = r'''# Ch 6 06절 요금표(100만 토큰당 달러)와 확인한 날짜를 적습니다
pricing_date = "2026-09-17"
mini_prices = {"ordinary_input": 0.75, "cached_input": 0.075, "output": 4.50}
print("요금 확인 날짜:", pricing_date)
print("mini 요금:", mini_prices)'''

COST = r'''# 3절 요청 한 번의 예상 비용(달러)을 셉니다(Ch 6 06절 함수 estimate_cost)
answer_cost = estimate_cost(
    answer_usage, mini_prices["ordinary_input"], mini_prices["cached_input"], mini_prices["output"]
)
print("예상 비용(달러):", round(answer_cost, 6))'''

RUN2 = r'''# 모드 목록의 차례만 바꿔, 같은 문의로 한 번 더 실행하며 시각을 적습니다(모델 요청 1번)
swapped_modes = ["updates", "messages", "custom"]
swapped_run = collect_timed_events(graph, answer_input, None, swapped_modes)
swapped_events = swapped_run["events"]
print("모드 차례:", mode_order(swapped_events))
print("첫 사건의 자료:", swapped_events[0][1])
print("글자가 든 첫 스트림 청크의 자리:", first_text_place(swapped_events))'''

COMPARE = r'''# 두 실행의 세 시간(초)을 한 줄씩 견줍니다(7절 함수 three_times)
swapped_seconds = three_times(swapped_run)
print("시간 | 3절 실행 | 목록 차례를 바꾼 실행")
for name in answer_seconds:
    print(name, "|", answer_seconds[name], "|", swapped_seconds[name])'''

# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/03-figures.md)
FIG1 = "03-1-세-시간을-재는-자리"
FIG1_ALT = os.environ.get("AUTHOR03_FIG1_ALT", "위에서 아래로 여섯 상자가 화살표로 이어진 그림입니다. 파란 상자 시작 시각 stream을 부르기 직전에서 노란 상자 자리 1 custom 진행 값 30 모델 요청 전 여기까지 첫 사건 시간, 노란 상자 자리 2 messages 글자 없는 스트림 청크, 노란 상자 자리 3 messages 글자가 든 첫 스트림 청크 여기까지 첫 토큰 도착 시간으로 이어집니다. 그 뒤 스트림 청크들과 둘째 진행 값을 지나 노란 상자 맨 끝 updates 노드 write_answer의 갱신, 파란 상자 끝 시각 for가 끝난 뒤 여기까지 전체 걸린 시간으로 이어지는 그림")
FIG1_CAP = "세 시간은 모두 같은 시작 시각부터 재고, 어느 사건까지 재는지만 다릅니다."
FIG1_READ = """위에서 아래로 한 실행의 차례대로 읽습니다.
파란 상자는 우리 함수가 시각을 적은 자리이고, 노란 상자는 노트북 3~6절 출력으로 확인한 사건입니다.
세 시간은 모두 맨 위 시작 시각부터 재며, 어디까지 재는지는 상자 셋의 끝줄에 적었습니다.
초 값은 실행마다 달라, 그림에 적지 않았습니다."""

FIG2 = "03-2-사건마다-시각을-적는-함수"
FIG2_ALT = os.environ.get("AUTHOR03_FIG2_ALT", "위에서 아래로 읽는 흐름도입니다. 초록 상자 입력 칸 question 배송 문의 한 줄이 회색 상자 graph.stream 모드 셋을 한 목록으로 요청 한 번을 거쳐 파란 상자 노드 write_answer로 이어집니다. 노드에서 보라 상자 모델 gpt-5.4-mini 노드 안 invoke 한 번으로 화살표가 갑니다. 노드는 진행 값과 갱신을, 모델은 스트림 청크를 파란 상자 함수 collect_timed_events로 보내고, 함수에서 노란 상자 사건 목록과 시각 목록 길이가 같음 같은 자리끼리 짝으로 이어지는 그림")
FIG2_CAP = "사건은 노드와 모델에서 나오고, 우리 함수는 사건을 꺼낼 때마다 시각을 하나씩 적습니다."
FIG2_READ = """위에서 아래로 읽습니다.
초록 상자는 넣은 입력, 회색 상자는 라이브러리 메서드, 파란 상자는 우리가 적은 노드와 함수입니다.
보라 상자는 실제로 부른 모델이고, 노란 상자는 노트북 3절 출력으로 확인한 값입니다.
진행 값과 갱신은 노드에서, 스트림 청크는 모델에서 함수로 옵니다."""

FIG3 = "03-3-사용량이-든-스트림-청크와-예상-비용"
FIG3_ALT = os.environ.get("AUTHOR03_FIG3_ALT", "위에서 아래로 읽는 흐름도입니다. 노란 상자 사용량이 든 스트림 청크가 노란 상자 사용량 딕셔너리 입력 캐시 입력 출력 토큰 수로 이어집니다. 이 상자와 초록 상자 요금표 2026-09-17 mini 요금 세 가지가 함께 파란 상자 함수 estimate_cost 도구 파일에서 가져옴으로 들어가고, 노란 상자 예상 비용 달러 청구 금액이 아님 출력 토큰 따라 달라짐으로 이어지는 그림")
FIG3_CAP = "사용량이 든 스트림 청크의 토큰 수와 요금표로, 요청 한 번의 예상 비용을 셉니다."
FIG3_READ = """위에서 아래로 읽습니다.
노란 상자는 노트북 8절 출력이고, 초록 상자는 셀에 적은 요금표, 파란 상자는 도구 파일에서 가져온 함수입니다.
토큰 수와 예상 비용은 그림에 적지 않았고, 값은 노트북 8절 출력에서 봅니다."""

FIG4 = "03-4-모드-목록의-차례만-바꾼-실행"
FIG4_ALT = os.environ.get("AUTHOR03_FIG4_ALT", "맨 위 회색 상자 두 실행 같음 같은 문의 같은 노드 모델 요청 한 번씩에서 나란한 두 칸으로 화살표가 갑니다. 왼쪽 칸 처음 목록에서는 파란 상자 고른 목록 messages updates custom이 노란 상자 모드 차례 custom messages custom updates로 이어집니다. 오른쪽 칸 바꾼 목록에서는 파란 상자 고른 목록 updates messages custom이 같은 모드 차례의 노란 상자로 이어집니다. 맨 아래 회색 상자에는 두 칸 모두 첫 사건 진행 값 30 글자가 든 첫 스트림 청크 자리 3이 적힌 그림")
FIG4_CAP = "모드 목록의 차례만 바꿔도, 모드 차례와 첫 사건, 글자가 든 첫 스트림 청크의 자리는 같았습니다."
FIG4_READ = """맨 위 회색 상자는 두 실행에 같게 둔 조건이고, 왼쪽과 오른쪽 칸은 모드 목록만 바꾼 나란한 실행입니다.
파란 상자는 우리가 고른 모드 목록이고, 노란 상자는 노트북 3절과 9절의 모드 차례 출력입니다.
맨 아래 회색 상자는 4·5절과 9절 출력에서 모두 확인한 값입니다."""

ILLU = "03-5-첫-방울만-든-그릇과-가득-찬-그릇"
ILLU_ALT = os.environ.get("AUTHOR03_ILLU_ALT", "흰 바탕에 연두색 대나무 홈통 끝 둘이 나무 기둥에 하나씩 얹혀 서로 마주 보고, 홈통 끝마다 아래에 흰 그릇이 하나씩 놓인 그림입니다. 왼쪽 그릇은 비어 있고 바닥 가운데에 물방울 하나만 있습니다. 오른쪽 그릇은 옅은 파란 물로 가장자리까지 가득 차 있습니다. 글자·숫자·사람·손은 없는 그림")
ILLU_CAP = os.environ.get("AUTHOR03_ILLU_CAP", "같은 홈통 끝에서 받는 그릇을 두 때로 나눠 보면, 첫 방울이 닿은 때와 그릇이 가득 찬 때가 다릅니다.")
ILLU_READ = os.environ.get("AUTHOR03_ILLU_READ", "연두색 대나무 홈통 끝 둘이 나무 기둥 위에서 서로 마주 보고, 끝마다 아래에 흰 그릇이 하나씩 있습니다. 왼쪽 그릇 바닥 가운데에는 물방울 하나만 있고, 오른쪽 그릇은 가장자리까지 물이 찼습니다. 같은 그릇을 두 때로 나눠 본 모습으로 읽습니다. 왼쪽 그릇이 첫 방울이 닿은 때, 곧 첫 토큰 도착 시간의 끝이고, 오른쪽 그릇이 다 받은 때, 곧 전체 걸린 시간의 끝입니다. 물방울 하나를 스트림 청크 하나와 짝짓지 않습니다.")

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 02절 그래프를 모드 셋으로 한 번 실행하며, 사건마다 받은 시각을 적습니다.
2. 적은 시각으로 첫 사건 시간, 첫 토큰 도착 시간, 전체 걸린 시간을 계산합니다.
3. 세 시각의 차례와 요청 한 번의 예상 비용을 보고, 모드 목록의 차례만 바꿔 다시 실행합니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 모델 요청은 3절과 9절에서 한 번씩, 모두 2번입니다.
요금표로 어림한 예상 비용은 두 요청을 합쳐 0.001달러 아래이고, 청구 금액이 아닙니다.
이 절은 걸린 시간이 주제라서, 시간을 실제로 잽니다.
잰 초와 답 글, 스트림 청크 수는 실행마다 달라질 수 있습니다.

읽거나 쓰는 파일은 없고, 체크포인터도 쓰지 않습니다.
앞에서 배운 함수 셋은 도구 파일 `stream_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 넷을 설치합니다.
판은 langchain 1.4.0과 langchain-openai 1.6.0입니다.
langgraph 1.2.11과 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~6절을 읽습니다.
02절 그래프에 시각을 적는 함수를 붙여, 세 시간을 하나씩 재는 자리입니다.
7~9절은 세 시간을 모아 보고, 예상 비용과 목록 차례를 바꾼 실행을 보는 자리입니다.
7~9절은 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch25-streaming`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def model_cells() -> list[dict]:
    """과정 표준 키·모델 셀(nbkit)에 이 절의 결과 읽기(실행일·문장이 달라질 수 있음)를 붙입니다."""
    cells = key_and_model_cells("openai:gpt-5.4-mini")
    cells[-1] = md("""**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.

## 2. 02절과 같은 그래프

걸린 시간을 재려면, 02절에서 사건 차례를 본 그 그래프에 같은 요청을 보내야 합니다.
그래서 이 절은 02절 그래프를 다시 만듭니다.
다음 네 셀은 02절 노트북 2절의 네 셀과 같은 코드입니다.
노드가 노트북의 모델 객체와 시스템 메시지 글을 읽어서, 도구 파일로 옮기지 않았습니다.
먼저 칸 `question`과 `answer`를 둔 상태 형식을 만듭니다.""")
    return cells


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

02절에서는 모드 셋을 한 실행에서 함께 받아, 사건이 나온 차례를 보았습니다.
이 절은 같은 그래프를 한 번 실행하며, 사건마다 받은 시각을 적어 걸린 시간을 잽니다.
절 제목의 TTFT는 Ch 15 05절에서 배운 첫 토큰 도착 시간(time to first token)입니다.
절 제목의 total은 그래프 실행을 시작한 때부터 끝날 때까지 걸린 시간입니다.
본문에서는 이 시간을 전체 걸린 시간이라고 씁니다.

첫 셀은 패키지 넷을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langchain: 1.4.0`과 `langgraph: 1.2.11`이 보입니다.
네 판 모두 실습 폴더 잠금과 같은 판입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
첫 줄 `import time`은 시각을 읽는 함수 `time.perf_counter`가 든 기능 묶음을 가져옵니다.
Ch 6 06절과 Ch 15 05절에서 걸린 초를 잴 때 쓴 함수입니다.
그다음 줄들은 02절과 같은 이름이고, 마지막 가져오기 줄은 앞에서 배운 함수 셋을 도구 파일에서 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: estimate_cost, mode_order, positions_of`가 보입니다.
함수 `positions_of`는 01절 노트북 4절, `mode_order`는 02절 노트북 4절에서 처음 적었습니다.
함수 `estimate_cost`는 Ch 6 06절에서 배웠고, 사용량 딕셔너리와 세 요금을 받아 예상 비용(달러)을 내놓습니다.
이 함수는 Ch 21 도구 파일 `runner_tools.py`에 있던 같은 이름 함수를 그대로 옮겼습니다.

앞에서 배운 함수는 `stream_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다."""),
    ] + model_cells() + [
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 02절과 같은 시스템 메시지 글을 정합니다."""),
        code(SYSTEM),
        md("""**결과 읽기** — 출력 줄 `시스템 메시지 글: 배송 문의에 답하는 안내 도우미입니다. 두 문장의 한국어로 답하세요.`가 보입니다.
답을 두 문장으로 부탁해, 모델의 답이 짧게 끝나게 했습니다.

다음 셀은 02절의 노드 `write_answer`입니다.
모델 요청 앞에 진행 값 30을, 뒤에 진행 값 100을 보냅니다."""),
        code(DEF_NODE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
진행 값 30은 모델 요청을 보내기 전에 나갑니다.
그래서 이 절의 첫 사건은 모델의 답을 기다리지 않고 나올 것입니다.

다음 셀은 노드 하나를 START → write_answer → END로 이어, 체크포인터 없이 컴파일합니다."""),
        code(BUILD),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['write_answer']`가 보입니다.

## 3. 사건마다 시각 적기

시각은 시계를 읽은 값이고, 걸린 시간은 두 시각의 차이입니다.
함수 `time.perf_counter()`가 내놓는 수는 그 하나만으로는 뜻이 없습니다.
두 번 읽어 뒤 값에서 앞 값을 빼야 그 사이에 걸린 초가 됩니다.

01절 함수 `collect_events`는 사건을 다 모은 뒤에 목록을 내놓아, 사건마다 받은 때를 알 수 없습니다.
다음 셀의 함수 `collect_timed_events`는 사건을 꺼낼 때마다 그때의 시각을 하나씩 적습니다.
메서드 `stream`을 부르기 직전에 시작 시각을, 반복문 `for`가 끝난 뒤에 끝 시각을 적습니다.
네 가지를 딕셔너리 하나에 담아 내놓습니다."""),
        code(DEF_TIMED),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
키 `start`와 `end`에는 시작 시각과 끝 시각이 하나씩 들어갑니다.
키 `events`와 `times`에는 사건과 시각이 같은 자리끼리 짝을 이루어 들어갑니다.
01절에서 본 것처럼, 메서드 `stream`을 부르기만 해서는 실행이 시작되지 않습니다.
실행은 반복문이 첫 사건을 꺼낼 때 시작됩니다.

다음 셀은 02절과 같은 문의로 그래프를 한 번 실행합니다(모델 요청 1번).
모드 목록도 02절과 같은 `["messages", "updates", "custom"]`입니다.
모드마다 따로 요청하지 않고, 한 요청 안에서 세 시간을 모두 잽니다."""),
        code(RUN),
        md("""**결과 읽기** — 출력 줄 `사건마다 시각이 하나씩인가: True`와 `모드 차례: ['custom', 'messages', 'custom', 'updates']`가 보입니다.
사건 목록과 시각 목록의 길이가 같아, 자리마다 사건 하나와 시각 하나가 짝을 이룹니다.
모드 차례는 02절처럼 진행 값, 스트림 청크들, 진행 값, 갱신의 차례입니다.

이번 실행에서는 출력 줄 `받은 사건 수: 43`입니다.
모델의 답이 몇 개의 스트림 청크로 나뉘어 오느냐에 따라, 이 수는 달라질 수 있습니다.

## 4. 첫 사건 시간

첫 사건 시간은 메서드 `stream`을 부른 때부터, 모드와 관계없이 처음 받은 사건까지 걸린 시간입니다.
가게에 전화를 걸고 「잠시만 기다려 주세요」라는 말을 듣기까지 걸린 시간과 같습니다.
이 절 코드에서는 시각 목록의 첫 값 `event_times[0]`에서 시작 시각을 뺀 초입니다.

다음 셀은 첫 사건의 모드와 자료, 첫 사건 시간을 봅니다.
실행 전에 예상해 봅니다.
첫 사건은 모델 요청 전에 보낸 진행 값 30일 것입니다."""),
        code(FIRST_EVENT),
        md("""**결과 읽기** — 출력 줄 `첫 사건의 모드 이름: custom`과 `첫 사건의 자료: {'stage': 'before_model', 'progress': 30}`이 보입니다.
예상대로 첫 사건은 모델 요청 앞에 보낸 진행 값입니다.
그래서 첫 사건 시간에는 모델의 답을 기다린 시간이 들어 있지 않습니다.
화면은 이 사건을 받자마자 「답을 쓰는 중」 같은 표시를 띄울 수 있습니다.

이번 실행에서는 출력 줄 `첫 사건 시간(초): 0.003`입니다.
잰 초는 기기와 네트워크, 실행한 때에 따라 달라집니다.

## 5. 첫 토큰 도착 시간

Ch 15 05절에서 첫 토큰 도착 시간은 답의 첫 글자를 받기까지 걸린 시간이었습니다.
그 절은 모델의 `stream()`을 부르기 직전부터, 글자가 든 첫 스트림 청크가 도착할 때까지로 쟀습니다.
이 절은 그보다 조금 앞인, 그래프의 메서드 `stream`을 부르기 직전부터 잽니다.
02절 5절에서 본 대로, 모드 `messages`의 첫 스트림 청크에는 글자가 없었습니다.
그래서 모드 `messages`의 첫 사건과 글자가 든 첫 스트림 청크를 나눠 봅니다.

다음 셀은 모드 `messages`의 첫 사건이 몇 번째인지와, 그 스트림 청크의 글자 수를 봅니다."""),
        code(FIRST_MSG),
        md("""**결과 읽기** — 출력 줄 `모드 messages 첫 사건의 자리: 2`와 `그 스트림 청크의 글자 수: 0`이 보입니다.
진행 값 30 바로 다음에 모드 `messages`의 사건이 왔지만, 그 스트림 청크에는 글자가 없었습니다.
이 사건의 시각을 쓰면, 답의 글자가 오기 전의 시각을 재게 됩니다.

다음 셀은 글자가 든 첫 스트림 청크가 몇 번째 사건인지 찾는 함수입니다.
사건을 앞에서부터 보다가, 모드가 `messages`이고 스트림 청크의 글이 빈 글이 아닌 첫 사건에서 멈춥니다.
끝까지 찾지 못하면 `None`을 내놓습니다."""),
        code(DEF_FIRST_TEXT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
두 조건을 `and`로 이어, 둘 다 맞을 때만 자리를 내놓습니다.
모드 `custom`의 자료는 딕셔너리라서, 모드를 먼저 보고 나서 스트림 청크의 글을 봅니다.

다음 셀은 이 함수로 자리를 찾고, 그 사건의 시각으로 첫 토큰 도착 시간을 계산합니다."""),
        code(FIRST_TOKEN),
        md("""**결과 읽기** — 출력 줄 `글자가 든 첫 스트림 청크의 자리: 3`이 보입니다.
모드 `messages`의 둘째 사건부터 답의 글자가 왔습니다.
첫 토큰 도착 시간은 이 셋째 사건의 시각에서 시작 시각을 뺀 값입니다.

이번 실행에서는 출력 줄 `첫 토큰 도착 시간(초): 1.51`입니다.
4절의 첫 사건 시간과 달리, 모델 요청을 보내고 첫 글자를 받기까지 기다린 시간이 들어 있습니다.

## 6. 전체 걸린 시간

전체 걸린 시간은 메서드 `stream`을 부른 때부터 마지막 사건까지 다 받고 끝날 때까지 걸린 시간입니다.
가게 전화로 치면, 안내를 끝까지 듣고 전화를 끊을 때까지 걸린 시간입니다.
이 절 코드에서는 반복문이 끝난 뒤 적은 끝 시각에서 시작 시각을 뺀 초입니다.
Ch 15 05절은 같은 시간을 다른 이름으로 불렀고, 이 챕터는 전체 걸린 시간이라고 씁니다.

다음 셀은 마지막 사건의 모드와 전체 걸린 시간을 봅니다.
자리 `-1`은 목록의 맨 끝 자리입니다."""),
        code(TOTAL),
        md("""**결과 읽기** — 출력 줄 `마지막 사건의 모드 이름: updates`가 보입니다.
노드가 끝나며 낸 갱신이 마지막 사건이고, 칸 `answer`의 답 글 전체가 여기에 담겨 옵니다.
끝 시각은 이 갱신을 받고 반복문이 끝난 뒤에 적었습니다.

이번 실행에서는 출력 줄 `전체 걸린 시간(초): 1.758`입니다.

## 7. 세 시간 모아 보기

세 시각은 사건을 받은 차례대로 적었습니다.
첫 사건은 자리 1, 글자가 든 첫 스트림 청크는 자리 3이고, 끝 시각은 마지막 사건 뒤에 적었습니다.
실행 전에 예상해 봅니다.
앞 사건의 시각을 먼저 적었으니, 다음 셀의 두 비교는 모두 `True`일 것입니다."""),
        code(ORDER),
        md("""**결과 읽기** — 두 출력 줄이 모두 `True`입니다.
그래서 세 시간은 첫 사건 시간, 첫 토큰 도착 시간, 전체 걸린 시간의 차례로 커집니다.
이 차례는 사건이 나온 차례로 정해지므로, 초 값이 달라져도 같습니다.
Ch 15 05절 출력 「첫 토큰이 끝보다 먼저 왔는가: True」와 같은 모양입니다.

다음 셀은 세 시간을 한 딕셔너리로 계산하는 함수입니다.
4~6절에서 하나씩 한 계산을 묶어, 9절의 다른 실행에도 그대로 씁니다."""),
        code(DEF_THREE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 안에서 5절 함수 `first_text_place`를 불러, 글자가 든 첫 스트림 청크의 자리를 찾습니다.
그래서 이 셀보다 5절의 함수 셀을 먼저 실행해 두어야 합니다.

다음 셀은 3절 실행의 세 시간을 이 함수로 계산하고, 4~6절 값과 견줍니다."""),
        code(THREE_RUN),
        md("""**결과 읽기** — 출력 줄 `4~6절에서 계산한 값과 같은가: True`가 보입니다.
라벨 `세 시간(초):` 뒤 딕셔너리의 세 값은 4~6절 출력의 세 값과 같습니다.
같은 실행의 같은 시각으로 같은 계산을 했기 때문입니다.

다음 셀은 첫 토큰 도착 시간을 기준으로, 전체 걸린 시간을 두 구간으로 나눠 봅니다.
앞 구간은 사용자가 첫 글자를 기다리는 시간입니다.
뒤 구간은 글자가 이어 붙는 것을 지켜보는 시간입니다."""),
        code(SPLIT),
        md("""**결과 읽기** — 라벨 줄 `구간 | 초` 아래 두 줄이 두 구간입니다.
두 구간을 더하면 6절의 전체 걸린 시간과 거의 같고, 반올림 때문에 끝자리가 다를 수 있습니다.

이번 실행에서는 첫 글자까지 1.51초, 첫 글자부터 끝까지 0.248초였습니다.
두 구간의 크기는 답 길이와 실행한 때에 따라 달라져, 이 절의 결론에 쓰지 않습니다.
스트리밍하지 않은 실행과는 견주지 않아, 스트리밍이 기다림을 줄이는지도 이 결과로 말할 수 없습니다.

## 8. 사용량과 예상 비용

Ch 6 06절은 걸린 초와 함께 요청 한 번의 예상 비용을 셌습니다.
이 절도 3절 요청 한 번의 사용량으로 예상 비용을 셉니다.
02절 5절에서 본 대로, 사용량은 스트림 청크 하나에만 들어 있었습니다.
다음 셀은 사용량이 든 스트림 청크를 찾아 토큰 수를 봅니다."""),
        code(USAGE),
        md("""**결과 읽기** — 출력 줄 `사용량이 든 스트림 청크 수: 1`과 `입력 토큰 수: 47`이 보입니다.
사용량이 든 스트림 청크가 하나라, 그 사용량이 이 요청 한 번의 사용량입니다.
출력 줄 `캐시 입력 토큰 수: 0`이라, 입력 토큰은 모두 일반 입력 요금으로 셉니다.

이번 실행에서는 출력 줄 `출력 토큰 수: 40`입니다.
출력 토큰 수는 모델이 쓴 답 글에 따라 실행마다 달라질 수 있습니다.

다음 셀은 Ch 6 06절 요금표와 확인한 날짜를 적습니다.
요금은 모델 `gpt-5.4-mini`의 100만 토큰당 달러입니다."""),
        code(PRICES),
        md("""**결과 읽기** — 출력 줄 `요금 확인 날짜: 2026-09-17`이 보입니다.
라벨 `mini 요금:` 뒤 딕셔너리는 일반 입력, 캐시 입력, 출력 토큰의 100만 개당 달러입니다.
출력 요금은 셀에 4.50으로 적었지만, 출력에서는 끝자리 0 없이 찍힙니다.

다음 셀은 함수 `estimate_cost`에 3절 사용량과 세 요금을 넣어 예상 비용을 셉니다."""),
        code(COST),
        md("""**결과 읽기** — 라벨 `예상 비용(달러):` 뒤 값이 요금표로 어림한 예상 비용이고, 청구 금액이 아닙니다.
세 요금은 식 안에 숫자로 적지 않고, 앞 셀의 딕셔너리에서 꺼내 넣었습니다.

이번 실행에서는 `0.000215`달러였습니다.
출력 토큰 수가 달라지면 이 값도 달라집니다.
이 노트북은 모델 요청을 두 번 보내므로, 노트북 한 번의 예상 비용은 이 값의 두 배쯤입니다.

## 9. 값 바꿔 보기 · 모드 목록의 차례만 바꾸기

값 하나만 바꿔 봅니다.
바꿀 값은 모드 목록의 차례이고, 3절 목록을 `["updates", "messages", "custom"]`으로 바꿉니다.
실행 전에 예상해 봅니다.
사건 차례는 노드 코드가 정하니, 모드 `updates`를 앞에 적어도 첫 사건은 진행 값 30일 것입니다.
글자가 든 첫 스트림 청크의 자리도 3 그대로일 것입니다.

다음 셀은 같은 문의로 그래프를 한 번 더 실행합니다(모델 요청 1번)."""),
        code(RUN2),
        md("""**결과 읽기** — 출력 줄 `모드 차례: ['custom', 'messages', 'custom', 'updates']`는 3절과 같습니다.
출력 줄 `첫 사건의 자료: {'stage': 'before_model', 'progress': 30}`도 3절과 같습니다.
출력 줄 `글자가 든 첫 스트림 청크의 자리: 3`도 5절과 같습니다.
목록에서 모드 `updates`를 맨 앞에 적었지만, 첫 사건은 여전히 진행 값이었습니다.
모드 목록은 받을 모드를 고를 뿐이고, 사건 차례는 노드 코드가 정합니다.

다음 셀은 두 실행의 세 시간을 한 줄씩 견줍니다."""),
        code(COMPARE),
        md("""**결과 읽기** — 라벨 줄 `시간 | 3절 실행 | 목록 차례를 바꾼 실행` 아래 세 줄이 두 실행의 세 시간입니다.
두 실행 모두 사건 차례가 같아, 세 값이 위에서 아래로 커집니다.

이번 실행에서는 줄 `첫 토큰 도착 시간 | 1.51 | 0.642`와 `전체 걸린 시간 | 1.758 | 0.84`입니다.
두 요청은 따로 보낸 요청이라, 초의 차이를 모드 목록 차례 탓으로 읽지 않습니다.

## 정리

1. 모드 셋을 한 실행에서 함께 받으며 사건마다 시각을 적자, 한 요청 안에서 세 시간을 모두 잴 수 있었습니다.
2. 첫 사건은 모델 요청 전의 진행 값이었고, 글자가 든 첫 스트림 청크는 셋째 사건이었습니다.
3. 세 시각은 사건 차례대로 커졌고, 모드 목록의 차례를 바꿔도 사건 차례는 같았습니다.

04절 실습에서는 이 챕터에서 배운 것을 작은 흐름 하나에 모아 실행합니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
L_CH06_06 = "../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html"
L_CH15_05 = "../../part4/ch15-evaluation-advanced/05-로컬-트레이싱과-지연.html"
L_CH15_06 = "../../part4/ch15-evaluation-advanced/06-대화당-비용-백분위수.html"
L_CH17_04 = "../../part5/ch17-agent-overview/04-자율성의-대가.html"
L_CH18_03 = "../../part5/ch18-workflow-patterns/03-병렬-섹셔닝과-투표.html"
L_CH21_01 = "../ch21-create-agent/01-create-agent와-ReAct-루프.html"
L_01 = "01-일곱-가지-stream-mode.html"
L_02 = "02-토큰과-중간-진행-스트리밍.html"
L_04 = "04-Streaming-실습.html"

TIME_ROWS = [
    ("첫 사건 시간", "모드 <code>custom</code>의 진행 값 30(모델 요청 전)", "1", "0.003", "자리와 자료는 같음, 초는 달라짐"),
    ("첫 토큰 도착 시간", "모드 <code>messages</code>의 글자가 든 첫 스트림 청크", "3", "1.51", "자리는 같음, 초는 달라짐"),
    ("전체 걸린 시간", "마지막 사건 <code>updates</code>를 받고 반복문이 끝난 때", "맨 끝 뒤", "1.758", "초는 달라짐"),
]

LOOK_B5 = "노트북 3절에서 <code>사건마다 시각이 하나씩인가: True</code>를 봅니다. 4절 <code>첫 사건의 자료: {'stage': 'before_model', 'progress': 30}</code>과 5절 <code>글자가 든 첫 스트림 청크의 자리: 3</code>을 확인합니다. 7절 두 비교가 모두 <code>True</code>인지 봅니다. 교재 출력에서는 첫 사건 시간 0.003초, 첫 토큰 도착 시간 1.51초였습니다. 전체 걸린 시간은 1.758초였고, 다시 실행하면 달라집니다."
LOOK_B6 = "노트북 9절에서 <code>모드 차례: ['custom', 'messages', 'custom', 'updates']</code>가 3절과 같은지 봅니다. 7절 <code>4~6절에서 계산한 값과 같은가: True</code>를 확인합니다. 교재 출력의 출력 토큰은 40개, 예상 비용은 0.000215달러였고, 다시 실행하면 달라질 수 있습니다."


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


def src_html() -> str:
    times = table_html(["시간", "어디까지", "사건 자리", "교재 출력(초)", "다시 실행하면"], TIME_ROWS)
    return """<!--meta: 강의 1h | 실습 2h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 2 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>모드 셋을 한 실행에서 함께 받으며 사건마다 시각을 적고, 세 시간을 계산할 수 있습니다.</li>
<li>첫 사건과 글자가 든 첫 스트림 청크가 몇 번째 사건인지 가르고, 세 시각의 차례를 설명할 수 있습니다.</li>
<li>요청 한 번의 사용량으로 예상 비용을 셈하고, 실행마다 같은 값과 달라지는 값을 가를 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_02 + """\">02절</a>에서는 진행 값과 스트림 청크, 갱신을 한 실행에서 함께 받았습니다. 무엇을 받느냐에 따라, 사용자가 화면에서 무언가를 처음 보는 때도 달라집니다. 진행 표시는 모델을 기다리기 전에 뜨고, 답의 첫 글자는 모델이 답을 쓰기 시작해야 옵니다. 그래서 사용자가 기다리는 시간은 하나가 아니라 여럿입니다.</p><p>절 제목의 TTFT는 <a href=\"""" + L_CH15_05 + """\">Ch 15 05절</a>에서 배운 첫 토큰 도착 시간(time to first token)입니다. 절 제목의 total은 그래프 실행을 시작한 때부터 끝날 때까지 걸린 시간이고, 본문에서는 전체 걸린 시간이라고 씁니다. 이 절은 여기에 첫 사건 시간을 더해, 세 시간을 한 요청 안에서 잽니다. 모드마다 따로 요청하면 요청 종류부터 달라질 수 있기 때문입니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_02 + """\">02절</a>에서는 모델을 부르는 노드 <code>write_answer</code>를 모드 셋으로 한 번 실행했습니다. 사건은 진행 값 30, 스트림 청크들, 진행 값 100, 갱신의 차례로 나왔습니다. 모드 <code>messages</code>의 첫 스트림 청크에는 글자가 없었고, 사용량은 스트림 청크 하나에만 있었습니다. 02절은 모드 <code>messages</code>를 고르지 않으면 노드 안 <code>invoke</code>가 스트리밍 요청을 보내지 않는다고 설치판 소스로 적었습니다. 이 절은 02절 그래프를 그대로 쓰고, <a href=\"""" + L_01 + """\">01절</a> 함수 <code>positions_of</code>와 02절 함수 <code>mode_order</code>를 도구 파일에서 가져옵니다.</p><p><a href=\"""" + L_CH15_05 + """\">Ch 15 05절</a>에서는 모델의 <code>stream()</code>으로 답을 받으며 첫 토큰 도착 시간을 쟀습니다. 그 절은 글자가 든 첫 스트림 청크를 받은 때까지로 쟀습니다. 시각은 <a href=\"""" + L_CH06_06 + """\">Ch 6 06절</a>처럼 <code>time.perf_counter()</code>로 읽고, 두 값을 빼 걸린 초를 냈습니다. Ch 6 06절은 요금표와 함수 <code>estimate_cost</code>로 요청 한 번의 예상 비용도 셌습니다. 이 절은 그 함수를 <a href=\"""" + L_CH21_01 + """\">Ch 21</a> 도구 파일 <code>runner_tools.py</code>에서 그대로 옮겨 씁니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절부터 대나무 홈통에 물을 흘려 그릇에 받는 모습으로 스트리밍을 보았습니다. 이번에는 물을 흘리기 시작한 때부터 시간을 잽니다. 물이 닿기 전에 02절의 종이 먼저 울립니다. 조금 뒤 첫 물방울이 그릇 바닥에 닿고, 더 지나 그릇이 가득 찹니다.</p><p>종이 울린 때까지가 첫 사건 시간, 첫 방울이 닿은 때까지가 첫 토큰 도착 시간입니다. 그릇이 가득 찰 때까지가 전체 걸린 시간입니다. 세 시간 모두 물을 흘리기 시작한 때부터 잽니다.</p><p>비유와 다른 점이 있습니다. 홈통에서는 빈 방울이 떨어지지 않지만, 모드 <code>messages</code>의 첫 스트림 청크에는 글자가 없었습니다. 그래서 첫 토큰 도착 시간은 글자가 든 첫 스트림 청크를 받은 때로 잽니다.</p>
""" + illustration_block() + """<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>첫 사건 시간</td><td>메서드 <code>stream</code>을 부른 때부터, 모드와 관계없이 처음 받은 사건까지 걸린 시간입니다. 가게에 전화를 걸고 「잠시만 기다려 주세요」를 듣기까지 걸린 시간과 같습니다. 이 절에서는 시각 목록의 첫 값에서 시작 시각을 뺀 초이고, 첫 사건은 진행 값 30이었습니다.</td></tr><tr><td>첫 토큰 도착 시간</td><td>Ch 15 05절에서 배운 말로, 글자가 든 첫 스트림 청크를 받기까지 걸린 시간입니다. 그 절은 식당에서 첫 접시가 나올 때까지 기다린 시간에 빗댔습니다. 이 절에서는 셋째 사건의 시각에서 시작 시각을 뺀 초입니다. Ch 15 05절은 모델의 <code>stream()</code>을 부르기 직전부터 쟀고, 이 절은 그보다 조금 앞에서부터 잽니다.</td></tr><tr><td>전체 걸린 시간</td><td>메서드 <code>stream</code>을 부른 때부터 마지막 사건까지 다 받고 끝날 때까지 걸린 시간입니다. 가게 전화로 치면 안내를 끝까지 듣고 전화를 끊을 때까지 걸린 시간입니다. 이 절에서는 반복문이 끝난 뒤 적은 끝 시각에서 시작 시각을 뺀 초입니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 첫 사건 시간은 노트북 4절 출력 <code>첫 사건 시간(초):</code> 뒤 값입니다. 첫 토큰 도착 시간은 5절, 전체 걸린 시간은 6절 출력의 같은 이름 줄입니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>한 요청 안에서 세 시간을 잽니다</h3><p>함수 <code>collect_timed_events</code>는 메서드 <code>stream</code>을 부르기 직전에 시작 시각을 적습니다. 그다음 사건을 하나 꺼낼 때마다 시각을 하나씩 적고, 반복문이 끝나면 끝 시각을 적습니다. 그래서 사건 목록과 시각 목록은 길이가 같고, 같은 자리끼리 짝을 이룹니다. 01절에서 본 것처럼 실행은 반복문이 첫 사건을 꺼낼 때 시작됩니다.</p><p>세 모드를 한 요청으로 받으니, 세 시간은 같은 요청의 같은 답에서 나옵니다. 02절에서 본 대로 모드 <code>messages</code>를 고르지 않은 실행은 스트리밍 요청을 보내지 않습니다. 모드마다 따로 요청하면 요청 종류와 답 길이가 함께 달라져, 세 시간을 한 줄에 놓고 견줄 수 없습니다.</p>
<h3>세 시각의 차례는 사건 차례가 정합니다</h3><p>첫 사건은 노드가 모델 요청 전에 보낸 진행 값이라 자리 1입니다. 모델의 답은 그 뒤에 오고, 글자가 든 첫 스트림 청크는 자리 3이었습니다. 끝 시각은 마지막 사건인 갱신을 받은 뒤에 적습니다. 시각을 사건 차례대로 적으니, 세 시간이 커지는 차례는 초 값과 관계없이 같습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 02절 그래프를 다시 만들고, 사건마다 시각을 적는 함수 <code>collect_timed_events</code>를 새로 적습니다. 3절에서 모드 셋으로 한 번 실행하고, 4~6절에서 세 시간을 하나씩 계산합니다. 7절은 세 시각의 차례를 견주고 세 시간을 함수 하나로 묶습니다. 8절은 사용량으로 예상 비용을 셈하고, 9절은 모드 목록의 차례만 바꿔 한 번 더 실행합니다.</p><p>실제 OpenAI 모델 <code>gpt-5.4-mini</code>를 temperature 0으로 부릅니다. 모델 요청은 3절과 9절에서 한 번씩, 모두 2번입니다. 요금표로 어림한 예상 비용은 0.001달러 아래이고, 청구 금액이 아닙니다. 잰 초와 답 글, 스트림 청크 수는 실행마다 달라질 수 있습니다. 읽거나 쓰는 파일은 없습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>한 요청 안에서 적은 세 시각은 사건 차례대로 커졌습니다. 아래 표는 세 시간이 어느 사건까지의 시간인지와 교재 출력의 초를 모은 것입니다. 초는 교재 출력의 값이고, 다시 실행하면 달라집니다.</p>
""" + times + """
<p>첫 사건은 모델 요청 전에 보낸 진행 값이라, 모델의 답을 기다린 시간이 들어 있지 않습니다. 모드 <code>messages</code>의 첫 사건은 자리 2였지만 글자가 없어, 첫 토큰 도착 시간은 자리 3의 시각으로 쟀습니다. 노트북 7절의 두 비교는 모두 <code>True</code>였습니다. 이 차례는 사건이 나온 차례로 정해지므로, 이 절의 결론은 초가 아니라 이 차례에 둡니다.</p><p>요청 한 번의 사용량은 사용량이 든 스트림 청크에서 읽었습니다. 입력 토큰과 캐시 입력 토큰의 수는 노트북 8절 결과 읽기에 있습니다. 출력 토큰과 예상 비용은 실행마다 달라져, 결과 읽기와 「확인할 점」에만 적었습니다.</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>노트북 9절에서 모드 목록의 차례만 바꾸자, 모드 차례와 첫 사건, 글자가 든 첫 스트림 청크의 자리는 3절과 같았습니다. 모드 목록은 받을 모드를 고를 뿐이고, 사건 차례는 노드 코드가 정합니다. 두 실행의 초는 따로 보낸 요청의 값이라, 그 차이를 목록 차례 탓으로 읽지 않습니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>모델을 부르는 절이라 초와 답 글, 스트림 청크 수는 실행마다 달라질 수 있습니다. 새 커널로 세 번 실행해 견주자, 사건 수·초·출력 토큰·예상 비용이 찍힌 셀 여덟은 실행에 따라 달랐습니다. 모드 차례·자리·진행 값·두 비교의 <code>True</code>가 찍힌 나머지 셀 열여섯은 세 번 모두 같았습니다.</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>걸린 시간은 이 절의 주제라서 실제로 쟀습니다. <a href=\"""" + L_CH15_05 + """\">Ch 15 05절</a>·<a href=\"""" + L_CH17_04 + """\">Ch 17 04절</a>·<a href=\"""" + L_CH18_03 + """\">Ch 18 03절</a>도 시간이 주제인 자리에서만 쟀습니다. 잰 초는 교재 출력을 만든 기기에서 <code>time.perf_counter()</code>로 읽은 값이라, 기기·네트워크·실행한 때에 따라 달라집니다.</li><li>요청은 조건마다 한 번씩만 보냈습니다. 여러 번 재어 가운데 값이나 <a href=\"""" + L_CH15_06 + """\">Ch 15 06절</a>의 백분위수를 보지 않았으므로, 두 실행의 빠르기를 견주지 않았습니다.</li><li>이 절은 모드 <code>messages</code>를 고르지 않은, 스트리밍하지 않은 실행과 걸린 시간을 견주지 않았습니다. 그래서 스트리밍이 첫 글자까지의 시간이나 전체 걸린 시간을 줄이는지는 이 절 결과로 말할 수 없습니다.</li><li>노트북을 쓰기 전에 노트북 밖에서 3절 실행과 9절 실행을 다섯 번씩, 모두 열 번 보냈습니다. 9절의 바꾼 목록은 그 전에 정해 둔 예입니다. 모드 차례, 첫 사건의 자료, 글자가 든 첫 스트림 청크의 자리 3, 두 비교의 <code>True</code>는 열 번 모두 같았습니다. 사건 수와 초, 출력 토큰은 실행마다 달랐습니다. 첫 사건 시간은 새 커널 세 번에서는 같았지만, 노트북 밖에서는 0.003~0.006초로 달라 결론에 쓰지 않았습니다.</li><li>노트북 밖 열 번 모두, 첫 토큰 도착 시간이 전체 걸린 시간의 절반을 넘었습니다. 두 문장짜리 짧은 답에서 본 모양이고, 긴 답에서도 같다고 말할 수는 없습니다.</li><li>첫 토큰 도착 시간에는 네트워크를 오간 시간과 서버에서 답을 만든 시간이 함께 들어 있고, 이 절은 둘을 가르지 않았습니다. 시작 시각을 적은 때와 그래프가 첫 노드를 시작한 때의 차이도 따로 재지 않았습니다.</li><li>세 시각의 차례는 사건을 받은 차례대로 시각을 적어서 정해집니다. 교재 출력을 만든 기기에서 <code>time.get_clock_info("perf_counter")</code>는 뒤로 가지 않는 시계라고 알렸습니다. 속성 <code>monotonic</code>이 <code>True</code>였고, 이 확인은 노트북 밖에서 했습니다.</li><li>모드 목록에 <code>messages</code>가 없으면 글자가 든 스트림 청크가 없어, 함수 <code>first_text_place</code>가 <code>None</code>을 내놓습니다. 그런 실행에 함수 <code>three_times</code>를 쓰면 <code>None</code>에서 1을 빼는 줄에서 셀이 오류로 멈춥니다. 이번에 실행하지 않았습니다.</li><li>사용량이 든 스트림 청크는 OpenAI 기본 주소와 기본 클라이언트로 모델을 부를 때 붙습니다. 설치판 langchain-openai 1.6.0 <code>chat_models/base.py</code> 1332~1351행으로 확인했습니다. 다른 주소로 부르면 이 스트림 청크가 없어 8절 셀이 멈출 수 있고, 이번에 실행하지 않았습니다.</li><li>예상 비용은 2026-09-17 요금표로 어림한 값이고, 청구 금액이 아닙니다. 모델이 쓴 답 글과 잰 초, 토큰, 예상 비용에는 <code>assert</code>를 걸지 않았습니다.</li><li>비동기 메서드 <code>astream</code>과 인자 <code>version="v2"</code>는 01·02절처럼 이번에도 실행하지 않았습니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>모드 셋을 한 실행에서 함께 받으며 사건마다 시각을 적자, 한 요청 안에서 세 시간을 모두 잴 수 있었습니다.</li><li>첫 사건은 모델 요청 전의 진행 값이었고, 글자가 든 첫 스트림 청크는 셋째 사건이었습니다.</li><li>세 시각은 사건 차례대로 커졌고, 모드 목록의 차례를 바꿔도 사건 차례는 같았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_04 + """\">04절 실습</a>에서는 이 챕터에서 배운 것을 작은 흐름 하나에 모아 실행합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 첫 사건 시간에 모델의 답을 기다린 시간이 들어 있지 않은 까닭은 무엇인가요?</p><p class="quiz-a">첫 사건이 노드가 모델 요청보다 먼저 보낸 진행 값 30이었기 때문입니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">2. 첫 토큰 도착 시간을 모드 <code>messages</code>의 첫 사건 시각으로 재지 않은 까닭은 무엇인가요?</p><p class="quiz-a">자리 2의 첫 스트림 청크에는 글자가 없었기 때문입니다. 그래서 글자가 든 첫 스트림 청크인 자리 3의 시각으로 쟀습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">3. 세 시간을 모드마다 따로 요청해 재지 않은 까닭은 무엇인가요?</p><p class="quiz-a">모드마다 따로 요청하면 요청 종류와 답 길이가 함께 달라지기 때문입니다. 모드 <code>messages</code>를 고르지 않은 요청은 스트리밍 요청이 아니고, 따로 보낸 요청이라 답 길이도 다를 수 있습니다. 그래서 한 요청 안에서 세 시간을 잽니다. 틀렸다면 본문 「핵심 개념」과 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">4. 모드 목록의 차례를 바꾸자 첫 사건이 바뀌었나요?</p><p class="quiz-a">바뀌지 않았습니다. 모드 차례와 첫 사건, 글자가 든 첫 스트림 청크의 자리가 3절과 같았습니다. 사건 차례는 노드 코드가 정하기 때문입니다. 틀렸다면 노트북 9절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.python.org/3.12/library/time.html#time.perf_counter">time.perf_counter</a></div>확인 2026-09-25 · 내놓는 값의 기준점이 정해져 있지 않아, 두 번 부른 값의 차이만 뜻이 있다고 적습니다. 같은 문서의 <code>get_clock_info</code>는 시계가 뒤로 갈 수 있는지 알려 줍니다.</li><li><div><a href="https://developers.openai.com/api/docs/guides/latency-optimization">Latency optimization</a></div>확인 2026-09-25 · OpenAI 안내 문서입니다. 스트리밍이 기다리는 시간을 줄인다고 적고, 기다리는 것과 진행을 지켜보는 것은 크게 다르다고 적습니다. 이는 문서의 설명이고, 이 절은 스트리밍하지 않은 실행과 견주지 않았습니다. 첫 토큰 도착 시간의 정의는 없어, 이 절은 Ch 15 05절의 정의를 씁니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langgraph/streaming">LangGraph Streaming</a></div>확인 2026-09-25 · 모드를 목록으로 골라 여러 모드를 함께 받는 방법이 있습니다. 모드 <code>messages</code>의 사건이 (스트림 청크, 칸 <code>metadata</code>) 짝이라는 설명도 있습니다.</li><li>Ch 15 05절에서 첫 토큰 도착 시간을, Ch 6 06절에서 걸린 초와 예상 비용을, 02절에서 사건 차례를 보았습니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    check_tools()
    check_same_as_02()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "stream_tools.py").write_text(TOOLS, encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        # 도구 파일은 없거나 02 판이거나 이 판과 같을 때만 쓴다. 뒤 절(04)이 함수를 더한 판이면 덮어쓰지 않는다(Ch 24 마감 A-10).
        current = ""
        if TOOLS_PATH.is_file():
            current = TOOLS_PATH.read_text(encoding="utf-8")
        # 04절 판은 머리 설명 뒤에 가져오기 줄(import time)을 더했으므로, 그 줄을 빼고 앞 판으로 시작하는지 봅니다
        plain = author_02.strip_later_imports(current)
        assert current == "" or plain.startswith(author_02.TOOLS), "도구 파일이 02절 판으로 시작하지 않습니다"
        if current == "" or current == author_02.TOOLS or current == TOOLS:
            TOOLS_PATH.write_text(TOOLS, encoding="utf-8")
            print("wrote", TOOLS_PATH)
        else:
            assert plain.startswith(TOOLS), "도구 파일이 03절 판으로 시작하지 않습니다"
            print("skip", TOOLS_PATH, "(뒤 절이 함수를 더한 판 — 덮어쓰지 않음)")
        path = write_notebook(LAB, "03", SLUG, "experiment", cells())
        print("wrote", path)
