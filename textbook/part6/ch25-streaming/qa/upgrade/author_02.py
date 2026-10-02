"""Ch 25 02절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 -B author_02.py            → 도구 파일(없거나 이 판일 때만) + 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_02.py --src-only → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_02.py --tools-copy DIR → 도구 파일만 DIR에 쓴다(새 커널 사본 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**. 슬러그 그대로.

## 결정 1 — 실제 모델 첫 절 (챕터 리드 결정 1, M2의 02 몫)

nbkit.key_and_model_cells("openai:gpt-5.4-mini") — temperature=0·reasoning_effort="none", 키는 루트 .env에서만(값 출력 없음).
노드 write_answer 하나가 모델 요청 앞뒤로 진행 값 30·100을 보내고, 노드 안 model.invoke로 두 문장 답을 받는다.
입력은 01절 소재 「배송 문의」를 잇는 질문 하나. 체크포인터 없음(설정 None). 모델 요청은 노트북 한 번에 2번(3절·8절).

## 결정 2 — 세 모드를 한 실행에서 함께 받고, 결론은 실행마다 같은 값에만 (인계 §01 → §02 3·5·6항)

노트북 밖 흔들림 확인(qa/upgrade/02-probe.md, 요청 10번)에서 messages 사건 수는 41·41·50·34·41로 흔들렸고,
모드 차례 ['custom', 'messages', 'custom', 'updates']·updates 1·custom 2·langgraph_node·이어 붙인 글 == 답 글은 5/5 같았다.
결론·그림은 뒤의 값에만, 청크 수·답 글·토큰은 결과 읽기 둘째 단락과 b6 표·「확인할 점」에만([[READ_…]] 자리 표시 →
교재 출력 실행 뒤 mdpatch.py로 채움). assert는 모드 차례(노드 코드가 정하는 값) 하나뿐, 모델 글에 건 assert 없음.

## 결정 3 — 칸 metadata를 읽는다 (인계 7항, Ch 30 09 「실행 메타데이터를 읽었습니다」)

첫 청크의 키 목록·langgraph_node·langgraph_step·ls_model_name·ls_temperature(실행마다 같은 값)와 모든 청크의 노드 이름.
checkpoint_ns·langgraph_checkpoint_ns 값(작업 아이디)은 출력하지 않는다.

## 결정 4 — 도구 파일 stream_tools.py를 이 절이 처음 만든다 (챕터 리드 결정 5, B안)

01절이 처음 가르친 collect_events·positions_of를 이 절이 다시 쓰므로 옮긴다(01 노트북 셀 글자와 같음 — check_same_as_01()).
mode_order는 이 절에서 처음 가르치므로 노트북에 둔다. 앞 챕터 함수(estimate_cost·sum_usage)는 쓰지 않아 옮기지 않는다.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·
대입 풀기·별표 풀기·`while`·`try`·세미콜론·`isinstance`·데코레이터·클래스(상태 형식 말고)·`join`·`astream`·체크포인터.
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
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402
import author_01  # noqa: E402  (html_text·table_html·mermaid_block·링크, 01 함수 셀 글)

html_text = author_01.html_text
table_html = author_01.table_html
mermaid_block = author_01.mermaid_block

LAB = ROOT / "labs/part6/ch25-streaming/notebooks"
FIGS = ROOT / "textbook/part6/ch25-streaming/figures"
SLUG = "02-토큰과-중간-진행-스트리밍"
TITLE_TEXT = "토큰과 중간 진행 스트리밍"
SRC = ROOT / "textbook/part6/ch25-streaming/_src" / (SLUG + ".html")
TOOLS_PATH = LAB / "stream_tools.py"
NB01 = LAB / "01-일곱-가지-stream-mode.ipynb"

# ---------------------------------------------------------------- 도구 파일 stream_tools.py
TOOLS_HEAD = '''"""Ch 25 Streaming — 앞 챕터와 이 챕터 앞 절에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from stream_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
이 챕터 01·02·03절 노트북에서 처음 적은 함수 여섯과 Ch 21 도구 파일 runner_tools.py의 estimate_cost는
설명 주석과 본문을 글자 그대로 옮겼습니다.
앞 챕터 도구 파일(Ch 21 runner_tools.py·Ch 23 checkpoint_tools.py 등)은 이 챕터 실습 폴더에 없는
패키지(numpy·SQLite 체크포인터)를 가져와, 파일째 가져오지 않고 이 챕터 노트북이 쓰는 함수만 옮깁니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""
'''

TOOL_PARTS = [
    ("Ch 25 01절에서 배웠습니다 — 01절 노트북 4절의 같은 이름 함수를 옮겼습니다", author_01.DEF_COLLECT),
    ("Ch 25 01절에서 배웠습니다 — 01절 노트북 4절의 같은 이름 함수를 옮겼습니다", author_01.DEF_POSITIONS),
]


def tools_text() -> str:
    text = TOOLS_HEAD
    for note, definition in TOOL_PARTS:
        text = text + "\n\n# " + note + "\n" + definition + "\n"
    return text


TOOLS = tools_text()


def strip_later_imports(text: str) -> str:
    """머리 설명과 첫 함수 주석 사이의 가져오기 줄을 빼고 내놓습니다(04절 뒤 생성기 대조 줄).

    04절 판 도구 파일은 머리 설명 바로 뒤에 주석 한 줄과 `import time`을 더했습니다(03절 함수를 옮기며).
    뒤 절 판이 앞 절 판을 그대로 이어 쓰는지 볼 때는, 이 가져오기 줄을 빼고 앞머리를 견줍니다.
    """
    if not text.startswith(TOOLS_HEAD):
        return text
    rest = text[len(TOOLS_HEAD):]
    first = rest.find("\n\n# Ch ")
    if first <= 0:
        return text
    return TOOLS_HEAD + rest[first:]


def check_same_as_01() -> None:
    """도구 파일의 함수 둘이 01절 노트북(교재 출력 판)의 같은 셀 글과 글자·AST 모두 같은지 확인합니다."""
    nb = json.loads(NB01.read_text(encoding="utf-8"))
    cells = []
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source = cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
            cells.append(source)
    tree = ast.parse(TOOLS)
    names = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
    assert names == ["collect_events", "positions_of"], names
    for note, definition in TOOL_PARTS:
        assert definition in cells, "01절 노트북에 같은 셀 글이 없습니다: " + definition.splitlines()[1]
        assert ("# " + note + "\n" + definition) in TOOLS
        one = ast.dump(ast.parse(definition).body[0])
        found = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == ast.parse(definition).body[0].name]
        assert found == [one]
    # 이 판(02절 판, 상수 TOOLS)은 아무것도 가져오지 않습니다. 04절 판은 머리 설명 뒤에 import time 한 줄을 더했습니다
    assert "import" not in TOOLS.split('"""', 2)[2], "02절 판 도구 파일은 아무것도 가져오지 않습니다"


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["langchain==1.4.0", "langchain-openai==1.6.0", "langgraph==1.2.11", "python-dotenv==1.2.3"])

IMPORTS = r'''# 모델(Ch 6 01절)·그래프(Ch 13 01절)를 만드는 이름과, 진행 값을 보낼 쓰기 함수를 가져옵니다
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer
# 01절에서 배운 함수 둘은 도구 파일에서 가져옵니다
from stream_tools import collect_events, positions_of

print("도구 파일에서 가져온 함수:", "collect_events, positions_of")'''

STATE = r'''# 문의 글과 모델이 쓴 답 글 칸을 둔 상태 형식을 만듭니다(Ch 13 01절 모양, 두 칸 모두 규칙 없음)
class AnswerState(TypedDict):
    question: str
    answer: str'''

SYSTEM = r'''# 모델에게 줄 시스템 메시지 글을 정합니다(답을 두 문장으로 짧게 받으려고)
system_text = "배송 문의에 답하는 안내 도우미입니다. 두 문장의 한국어로 답하세요."
print("시스템 메시지 글:", system_text)'''

DEF_NODE = r'''# 모델 요청 앞뒤에 진행 값을 보내고, 모델이 쓴 답 글을 칸 answer에 내는 노드입니다
def write_answer(state):
    writer = get_stream_writer()
    writer({"stage": "before_model", "progress": 30})
    messages = [("system", system_text), ("user", state["question"])]
    # 모델 요청은 이 줄에서 한 번 나가고, 답을 다 받은 뒤에 다음 줄로 갑니다
    response = model.invoke(messages)
    writer({"stage": "after_model", "progress": 100})
    return {"answer": response.text}'''

BUILD = r'''# 노드 하나를 START → write_answer → END로 잇고, 체크포인터 없이 컴파일합니다
builder = StateGraph(AnswerState)
builder.add_node("write_answer", write_answer)
builder.add_edge(START, "write_answer")
builder.add_edge("write_answer", END)
graph = builder.compile()
print("등록한 노드:", list(builder.nodes))'''

RUN = r'''# 모드 셋을 한 목록으로 골라, 배송 문의 하나로 그래프를 한 번 실행합니다(모델 요청 1번)
answer_input = {"question": "주문한 책이 아직 오지 않았어요. 언제 받을 수 있나요?", "answer": ""}
answer_modes = ["messages", "updates", "custom"]
# 체크포인터가 없어 설정 자리에는 None을 넘깁니다(01절 8절과 같음)
answer_events = collect_events(graph, answer_input, None, answer_modes)
print("받은 사건 수:", len(answer_events))
print("첫 사건의 모드 이름:", answer_events[0][0])
print("첫 사건의 자료:", answer_events[0][1])'''

COUNT = r'''# 모드마다 사건 수를 한 줄씩 출력합니다(01절 함수 positions_of)
print("모드 | 사건 수")
for mode in answer_modes:
    places = positions_of(answer_events, mode)
    print(mode, "|", len(places))'''

DEF_ORDER = r'''# 사건 목록에서 같은 모드가 이어지면 한 번만 적어, 모드가 바뀐 차례를 목록으로 내놓습니다
def mode_order(events):
    order = []
    last_mode = ""
    for event in events:
        # 사건 하나는 (모드 이름, 자료) 짝이라, [0]이 모드 이름입니다
        mode = event[0]
        # 바로 앞 사건과 모드가 다를 때만 적습니다
        if mode != last_mode:
            order.append(mode)
        last_mode = mode
    return order'''

ORDER = r'''# 이 실행의 모드 차례를 보고, 노드 코드의 차례와 같은지 확인합니다
answer_order = mode_order(answer_events)
print("모드 차례:", answer_order)
# 진행 값 → 모델의 답 → 진행 값 → 갱신은 노드 코드가 정한 차례라, 실행마다 같아야 합니다
assert answer_order == ["custom", "messages", "custom", "updates"], "사건 차례가 노드 코드와 다릅니다"'''

PLACES = r'''# 진행 값과 갱신이 몇 번째 사건이었는지 보고, 갱신이 마지막 사건인지 확인합니다
custom_places = positions_of(answer_events, "custom")
update_places = positions_of(answer_events, "updates")
print("custom이 나온 자리:", custom_places)
print("updates가 나온 자리:", update_places)
print("updates가 마지막 사건인가:", update_places[0] == len(answer_events))'''

MODES_DATA = r'''# 모드 custom과 updates의 사건만 나온 차례대로 봅니다
for mode, data in answer_events:
    if mode == "custom":
        print(mode, "|", data)
    if mode == "updates":
        # 갱신은 {노드 이름: {칸 이름: 값}} 모양이라, 두 층의 키만 꺼냅니다(답 글은 실행마다 다름)
        print(mode, "| 노드:", list(data), "| 칸:", list(data["write_answer"]))'''

FIRST_MSG = r'''# 모드 messages의 첫 사건을 찾아, 자료의 모양을 봅니다
message_places = positions_of(answer_events, "messages")
print("첫 스트림 청크 사건의 자리:", message_places[0])
first_message = answer_events[message_places[0] - 1][1]
print("자료의 종류와 길이:", type(first_message).__name__, len(first_message))
print("앞 값의 종류:", type(first_message[0]).__name__)
print("뒤 값의 종류:", type(first_message[1]).__name__)'''

CHUNKS = r'''# 모드 messages의 사건에서 스트림 청크만 차례대로 꺼내 목록에 담습니다
answer_chunks = []
for mode, data in answer_events:
    if mode == "messages":
        # 자료는 (스트림 청크, 딕셔너리) 짝이라, [0]이 스트림 청크입니다
        answer_chunks.append(data[0])
print("스트림 청크 수:", len(answer_chunks))'''

EMPTY = r'''# 글자가 없는 스트림 청크의 차례(1부터)와 사용량이 든 청크인지 보고, 글자가 든 청크 수를 셉니다
text_count = 0
print("글자가 없는 스트림 청크:")
for index in range(len(answer_chunks)):
    chunk = answer_chunks[index]
    if chunk.text == "":
        print(index + 1, "| 사용량 있음:", chunk.usage_metadata is not None)
    else:
        text_count = text_count + 1
print("글자가 든 스트림 청크 수:", text_count)'''

META_KEYS = r'''# 첫 스트림 청크와 짝을 이룬 칸 metadata의 키를 봅니다
first_metadata = first_message[1]
print("키 수:", len(first_metadata))
print("키:", list(first_metadata))'''

META_VALUES = r'''# 칸 metadata에서 실행마다 같은 값을 가진 키 넷을 꺼냅니다
print("langgraph_node:", first_metadata["langgraph_node"])
print("langgraph_step:", first_metadata["langgraph_step"])
print("ls_model_name:", first_metadata["ls_model_name"])
print("ls_temperature:", first_metadata["ls_temperature"])'''

META_ALL = r'''# 모든 스트림 청크의 칸 metadata에서 노드 이름을 모아, 서로 다른 이름만 남깁니다
chunk_nodes = []
for mode, data in answer_events:
    if mode == "messages":
        node_name = data[1]["langgraph_node"]
        if node_name not in chunk_nodes:
            chunk_nodes.append(node_name)
print("스트림 청크가 온 노드:", chunk_nodes)'''

JOIN = r'''# 스트림 청크의 글을 차례대로 이어 붙이고, 모드 updates가 보낸 답 글과 견줍니다
joined_text = ""
for chunk in answer_chunks:
    joined_text = joined_text + chunk.text
final_answer = ""
for mode, data in answer_events:
    if mode == "updates":
        final_answer = data["write_answer"]["answer"]
print("이어 붙인 글과 답 글이 같은가:", joined_text == final_answer)'''

ANSWER = r'''# 이번 실행의 답 글과 글자 수를 봅니다(실행마다 달라질 수 있는 값)
print("답 글:")
print(final_answer)
print("글자 수:", len(final_answer))'''

COMBINE = r'''# 첫 스트림 청크에 나머지를 차례로 더해 하나로 합치고, 사용량을 봅니다(Ch 6 04절 모양)
combined = answer_chunks[0]
for chunk in answer_chunks[1:]:
    combined = combined + chunk
print("합친 객체 종류:", type(combined).__name__)
print("입력 토큰 수:", combined.usage_metadata["input_tokens"])
print("출력 토큰 수:", combined.usage_metadata["output_tokens"])'''

RUN2 = r'''# 모드 messages를 빼고, 같은 문의로 그래프를 한 번 더 실행합니다(모델 요청 1번)
quiet_modes = ["updates", "custom"]
quiet_events = collect_events(graph, answer_input, None, quiet_modes)
print("받은 사건 수:", len(quiet_events))
print("모드 차례:", mode_order(quiet_events))
print("custom이 나온 자리:", positions_of(quiet_events, "custom"))
print("updates가 나온 자리:", positions_of(quiet_events, "updates"))'''

COMPARE = r'''# 두 실행의 모드별 사건 수를 한 줄씩 견줍니다
print("모드 | 세 모드 실행 | 두 모드 실행")
for mode in answer_modes:
    with_messages = positions_of(answer_events, mode)
    without_messages = positions_of(quiet_events, mode)
    print(mode, "|", len(with_messages), "|", len(without_messages))'''

# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/02-figures.md)
FIG1 = "02-1-한-실행에서-함께-받은-세-모드"
FIG1_ALT = os.environ.get("AUTHOR02_FIG1_ALT", "위에서 아래로 읽는 흐름도입니다. 초록 상자 입력 칸 question 배송 문의 한 줄이 회색 상자 graph.stream 모드 셋을 한 목록으로를 거쳐 파란 상자 노드 write_answer 요청 앞뒤에 진행 값으로 이어집니다. 파란 상자에서 보라 상자 모델 gpt-5.4-mini 노드 안 invoke 한 번, 노란 상자 custom 진행 값 둘 30과 100, 노란 상자 updates 갱신 하나로 화살표가 갑니다. 보라 상자 아래 노란 상자 messages 스트림 청크 여러 개가 있는 그림")
FIG1_CAP = "노드 하나를 모드 셋으로 한 번 실행하자, 진행 값 둘과 스트림 청크 여러 개와 갱신 하나를 함께 받았습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 넣은 입력, 회색 상자는 라이브러리 메서드, 파란 상자는 우리가 적은 노드입니다.
보라 상자는 이 절에서 실제로 부른 모델이고, 노란 상자는 노트북 3·4절에서 출력으로 확인한 값입니다.
스트림 청크는 모델에서, 진행 값과 갱신은 노드에서 나옵니다."""

FIG2 = "02-2-사건이-나온-차례"
FIG2_ALT = os.environ.get("AUTHOR02_FIG2_ALT", "위에서 아래로 노란 상자 넷이 화살표로 이어진 그림입니다. 첫 상자 첫 사건 custom before_model 30, 둘째 상자 messages 스트림 청크가 이어짐 모두 노드 write_answer, 셋째 상자 custom after_model 100, 넷째 상자 마지막 사건 updates 노드 write_answer 칸 answer가 적혀 있습니다")
FIG2_CAP = "사건은 진행 값 30, 스트림 청크들, 진행 값 100, 갱신의 차례로 나왔습니다. 이 차례는 새 커널 세 번과 노트북 밖 다섯 번에서 모두 같았습니다."
FIG2_READ = """위에서 아래로 실행 차례대로 읽습니다.
노란 상자는 모두 노트북 4·6절 출력이고, 같은 모드가 이어진 사건은 한 상자로 묶었습니다.
둘째 상자의 스트림 청크 수는 실행마다 달라, 그림에 적지 않았습니다."""

FIG3 = "02-3-스트림-청크와-칸-metadata"
FIG3_ALT = os.environ.get("AUTHOR02_FIG3_ALT", "위에 노란 상자 messages 사건 하나 둘짜리 튜플이 있고, 아래 칸 둘로 화살표가 갑니다. 칸 앞 값 스트림 청크에는 노란 상자 AIMessageChunk 글자가 든 것과 글자 없는 것에서 노란 상자 글을 차례로 이어 붙임 갱신의 답 글과 같음 True로 화살표가 갑니다. 칸 뒤 값 칸 metadata에는 노란 상자 첫 스트림 청크의 langgraph_node write_answer와 노란 상자 모든 스트림 청크의 노드 이름 write_answer 하나가 위아래로 놓인 그림")
FIG3_CAP = "모드 messages 사건의 앞 값은 이어 붙이면 답 글이 되는 스트림 청크, 뒤 값은 노드 이름을 적은 칸 metadata였습니다."
FIG3_READ = """맨 위 상자는 모드 messages 사건 하나이고, 아래 두 칸은 그 짝의 앞 값과 뒤 값입니다.
노란 상자는 모두 노트북 5~7절 출력입니다.
뒤 값 칸의 두 상자는 나란한 값이라 화살표 없이 위아래로 놓았습니다."""

FIG4 = "02-4-모드-messages를-뺀-실행"
FIG4_ALT = os.environ.get("AUTHOR02_FIG4_ALT", "위에 회색 상자 두 실행 같음 같은 문의 노드 write_answer custom 둘 updates 하나가 있고, 아래 칸 둘로 화살표가 갑니다. 칸 세 모드 실행의 노란 상자에는 모드 차례 custom messages custom updates 답 글이 스트림 청크로 먼저 옴, 칸 두 모드 실행의 노란 상자에는 모드 차례 custom updates 사건 셋 답 글은 맨 끝 갱신에만이 적혀 있습니다. 맨 아래 회색 상자에는 소스 확인 messages를 고른 실행만 노드 안 invoke가 스트리밍 요청이 적힌 그림")
FIG4_CAP = "모드 messages를 빼도 진행 값 둘과 갱신 하나는 그대로 왔지만, 답 글은 맨 끝 갱신에만 담겨 왔습니다."
FIG4_READ = """맨 위 회색 상자는 두 실행에서 모두 같았던 값이고, 노트북 8절 견주기 출력입니다.
두 칸은 모드 목록만 바꾼 나란한 실행이고, 노란 상자는 4절과 8절 출력입니다.
맨 아래 회색 상자는 설치판 소스로 확인한 동작이고, 노트북에서는 요청 종류를 확인하지 않았습니다."""

ILLU = "02-5-홈통-끝-물방울과-기우는-대나무-통"
ILLU_ALT = os.environ.get("AUTHOR02_ILLU_ALT", "흰 바탕에 연두색 대나무 홈통 하나가 Y자 모양 나무 받침 둘 위에 가로로 놓인 그림입니다. 홈통에는 작은 놋쇠 종 둘이 왼쪽 끝 가까이와 둘째 받침 오른쪽에 짧은 끈으로 매달려 있습니다. 홈통의 열린 오른쪽 끝에서 크기가 서로 다른 물방울 일곱이 한 줄로 떨어집니다. 그 아래 나무 받침 위의 대나무 통 하나가 앞으로 기울어, 열린 끝으로 물을 쏟고 있습니다. 글자·숫자·사람·손은 없는 그림")
ILLU_CAP = os.environ.get("AUTHOR02_ILLU_CAP", "홈통 끝에서 크기가 제각각인 물방울이 하나씩 떨어지고, 아래 대나무 통은 한 번 기울어 물을 쏟습니다.")
ILLU_READ = os.environ.get("AUTHOR02_ILLU_READ", "연두색 대나무 홈통 하나에 작은 놋쇠 종 둘이 매달려 있습니다. 홈통의 오른쪽 끝에서 크기가 서로 다른 물방울 일곱이 한 줄로 떨어지고, 맨 아래 방울은 대나무 통의 위쪽 틈으로 들어갑니다. 대나무 통 하나는 받침 위에서 앞으로 기울어, 열린 끝으로 물을 쏟고 있습니다. 물방울이 스트림 청크, 기울어 쏟는 통이 갱신 하나이고, 왼쪽 종이 진행 값 30, 오른쪽 종이 진행 값 100입니다. 두 종의 자리는 울리는 차례를 나타내지 않고, 물방울 수도 스트림 청크 수와 짝짓지 않습니다.")

RUNS_SENTENCE = os.environ.get("AUTHOR02_RUNS_SENTENCE", "새 커널로 세 번 실행해 견주자, 스트림 청크 수·자리·답 글·출력 토큰이 찍힌 셀 여덟은 실행에 따라 달랐습니다. 모드 차례·진행 값·갱신의 키·이어 붙인 글과 답 글의 <code>True</code>가 찍힌 나머지 셀 열일곱은 늘 같았습니다.")

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 노드 안에서 실제 모델을 부르는 그래프를 만들고, 모델 요청 앞뒤에 진행 값을 보냅니다.
2. 모드 셋(`messages`·`updates`·`custom`)을 한 실행에서 함께 받아, 사건이 나온 차례를 봅니다.
3. 스트림 청크와 칸 `metadata`를 읽고, 이어 붙인 글이 최종 답 글과 같은지 확인합니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 모델 요청은 3절과 8절에서 한 번씩, 모두 2번입니다.
요금표로 어림한 예상 비용은 두 요청을 합쳐 0.001달러 아래이고, 청구 금액이 아닙니다.
모델의 답 글과 스트림 청크 수는 실행마다 달라질 수 있습니다.
걸린 시간은 재지 않았습니다.

읽거나 쓰는 파일은 없고, 체크포인터도 쓰지 않습니다.
01절에서 배운 함수 둘은 도구 파일 `stream_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 넷을 설치합니다.
판은 langchain 1.4.0과 langchain-openai 1.6.0입니다.
langgraph 1.2.11과 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~5절을 읽습니다.
모델을 부르는 노드를 만들고, 세 모드를 함께 받아 사건 차례와 스트림 청크를 보는 자리입니다.
6~8절은 칸 `metadata`, 스트림 청크 이어 붙이기, 모드를 뺀 실행을 보는 자리이고 실습 시간에 실행합니다.

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

## 2. 모델을 부르는 노드

01절 노드 `write`는 문의 제목 뒤에 글을 붙여 안내 초안을 만들었습니다.
이 절의 노드는 배송 문의에 답하는 안내 문장을 모델에게 쓰게 합니다.
먼저 상태 형식을 만듭니다.
칸 `question`은 문의 글, 칸 `answer`는 모델이 쓴 답 글입니다.
칸 구성이 01절과 달라, 상태 형식에도 새 이름을 붙입니다.""")
    return cells


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

01절은 모델 없이 노드 둘짜리 그래프를 실행했고, 모드 `messages`의 사건은 0개였습니다.
이 절에서는 노드 안에서 실제 모델을 불러, 그 모드로 모델의 답을 받습니다.
절 제목의 중간 진행은 01절에서 정한 진행 값이고, 이번에도 모드 `custom`으로 받습니다.
제목의 토큰 스트리밍이 무엇을 받는 일인지는 5절에서 풉니다.

첫 셀은 패키지 넷을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langchain: 1.4.0`과 `langgraph: 1.2.11`이 보입니다.
네 판 모두 실습 폴더 잠금과 같은 판입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모델을 만드는 함수 `init_chat_model`은 Ch 6 01절, 상태 형식과 그래프 이름은 Ch 13 01절과 같습니다.
함수 `get_stream_writer`는 01절에서 진행 값을 보낼 때 썼습니다.
마지막 가져오기 줄은 01절에서 배운 함수 둘을 도구 파일 `stream_tools.py`에서 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: collect_events, positions_of`가 보입니다.
함수 `collect_events`는 그래프를 한 번 실행하며 받은 사건을 목록에 모아 내놓습니다.
함수 `positions_of`는 한 모드의 사건이 몇 번째(1부터 셈)에 나왔는지 목록으로 내놓습니다.
두 함수 모두 01절 노트북 4절에서 처음 적었습니다.

앞에서 배운 함수는 `stream_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다."""),
    ] + model_cells() + [
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 절의 그래프가 이 상태 형식을 씁니다.

다음 셀은 모델에게 줄 시스템 메시지 글을 정합니다.
Ch 6 04절처럼 메시지 목록의 첫 튜플에 역할 `system`과 함께 넣을 글입니다."""),
        code(SYSTEM),
        md("""**결과 읽기** — 출력 줄 `시스템 메시지 글: 배송 문의에 답하는 안내 도우미입니다. 두 문장의 한국어로 답하세요.`가 보입니다.
답을 두 문장으로 부탁해, 모델의 답이 짧게 끝나게 했습니다.

다음 셀은 이 절의 노드입니다.
01절처럼 `writer = get_stream_writer()`로 쓰기 함수를 꺼내, 모델 요청 앞뒤에 진행 값을 하나씩 보냅니다.
요청 앞에는 `{"stage": "before_model", "progress": 30}`, 요청 뒤에는 진행 값 100을 보냅니다.
모델 요청은 노드 안의 `model.invoke(messages)` 한 줄에서 나갑니다."""),
        code(DEF_NODE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
진행 값의 숫자 30과 100은 우리가 정한 값이고, 모델이 쓴 글의 양과 관계가 없습니다.
노드는 `invoke`로 답을 다 받은 뒤에야 진행 값 100을 보내고 끝납니다.

다음 셀은 이 노드 하나를 START → write_answer → END로 이어 컴파일합니다.
이 절은 저장한 체크포인트를 보지 않아, 01절 8절처럼 체크포인터 없이 컴파일합니다."""),
        code(BUILD),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['write_answer']`가 보입니다.

## 3. 세 모드를 한 실행에서 함께 받기

01절 4절처럼 인자 `stream_mode`에 모드 이름을 목록으로 주면, 여러 모드의 사건을 한 실행에서 함께 받습니다.
이 절은 모드 셋을 고릅니다.
모드 `messages`는 모델의 답을, `updates`는 노드가 낸 갱신을, `custom`은 진행 값을 받습니다.
공식 문서는 모델을 `stream`이 아니라 `invoke`로 불러도, 모드 `messages`로 답이 나온다고 적습니다.

다음 셀은 배송 문의 하나로 그래프를 한 번 실행하며, 사건을 목록에 모읍니다(모델 요청 1번).
실행 전에 예상해 봅니다.
진행 값 30을 모델 요청보다 먼저 보내니, 첫 사건은 모드 `custom`일 것입니다."""),
        code(RUN),
        md("""**결과 읽기** — 출력 줄 `첫 사건의 모드 이름: custom`과 `첫 사건의 자료: {'stage': 'before_model', 'progress': 30}`이 보입니다.
예상대로 모델 요청 앞에 보낸 진행 값이 첫 사건입니다.

이번 실행에서는 출력 줄 `받은 사건 수: 43`입니다.
모델의 답이 몇 개의 스트림 청크로 나뉘어 오느냐에 따라, 같은 요청도 이 수가 달라질 수 있습니다.

다음 셀은 01절처럼 모드마다 사건 수를 한 줄씩 셉니다."""),
        code(COUNT),
        md("""**결과 읽기** — 라벨 줄 아래 `updates | 1`과 `custom | 2`가 보입니다.
갱신은 노드 하나가 끝날 때 한 번, 진행 값은 노드가 쓰기 함수를 부른 두 번입니다.
이 두 수는 노드 코드와 그래프 모양이 정하므로, 실행마다 같습니다.

이번 실행에서는 줄 `messages | 40`입니다.
01절 그래프에서는 사건이 0개였던 모드가, 모델을 부르자 사건을 여럿 냈습니다.

## 4. 사건이 나온 차례

사건이 많아, 모드 이름을 하나씩 늘어놓으면 차례를 한눈에 보기 어렵습니다.
모드 차례는 같은 모드의 사건이 이어지면 한 번만 적어, 모드가 바뀐 차례만 남긴 목록입니다.
버스 창밖을 보며 「논 → 마을 → 논」처럼 바뀐 풍경만 적는 것과 같습니다.
이 절 코드에서는 다음 셀의 함수 `mode_order`가 내놓는 목록입니다."""),
        code(DEF_ORDER),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
처음에는 변수 `last_mode`가 빈 글이라, 첫 사건의 모드는 늘 적힙니다.

다음 셀은 이 실행의 모드 차례를 봅니다.
실행 전에 예상해 봅니다.
노드 코드는 진행 값, 모델 요청, 진행 값, 끝의 차례이니 모드 차례도 그 차례일 것입니다."""),
        code(ORDER),
        md("""**결과 읽기** — 출력 줄 `모드 차례: ['custom', 'messages', 'custom', 'updates']`입니다.
진행 값 30, 스트림 청크들, 진행 값 100, 갱신의 차례로 사건이 나왔습니다.
모델의 답은 두 진행 값 사이에만 나왔고, 갱신은 맨 끝에 한 번 나왔습니다.
이 차례는 노드 코드가 정하므로, 셀 끝의 `assert`로 확인했습니다.

다음 셀은 01절 함수 `positions_of`로 진행 값과 갱신이 몇 번째 사건이었는지 봅니다."""),
        code(PLACES),
        md("""**결과 읽기** — 출력 줄 `updates가 마지막 사건인가: True`입니다.
진행 값 30은 첫 사건이었고, 진행 값 100과 갱신은 맨 끝 두 자리에 나왔습니다.

이번 실행에서는 `custom이 나온 자리: [1, 42]`와 `updates가 나온 자리: [43]`입니다.
두 진행 값 사이의 사건은 모두 모드 `messages`의 사건입니다.

다음 셀은 모드 `custom`과 `updates`의 사건만 나온 차례대로 출력합니다.
갱신 안의 답 글은 실행마다 달라, 노드 이름과 칸 이름만 봅니다."""),
        code(MODES_DATA),
        md("""**결과 읽기** — 세 줄이 나옵니다.
첫 줄 `custom | {'stage': 'before_model', 'progress': 30}`은 요청 앞에 보낸 진행 값입니다.
둘째 줄 `custom | {'stage': 'after_model', 'progress': 100}`은 요청 뒤에 보낸 진행 값입니다.
셋째 줄 `updates | 노드: ['write_answer'] | 칸: ['answer']`는 노드가 칸 `answer`를 갱신했다는 뜻입니다.
진행 값은 상태의 칸에 들어가지 않고, 모드 `custom`으로만 나옵니다.

## 5. 스트림 청크

절 제목의 토큰 스트리밍은 모델의 답을 생기는 대로 나눠 받는 일을 가리킵니다.
스트림 청크는 스트리밍에서 한 번에 도착하는 답의 일부입니다.
홈통 끝에서 크기가 제각각인 물방울이 하나씩 떨어지는 것과 같습니다.
이 절 코드에서는 모드 `messages` 사건 자료의 앞 값입니다.
Ch 6 04절에서 본 대로, 스트림 청크는 Ch 5의 토큰과 단위가 같지 않습니다.

다음 셀은 모드 `messages`의 첫 사건을 찾아, 자료가 어떤 모양인지 봅니다."""),
        code(FIRST_MSG),
        md("""**결과 읽기** — 출력 줄 `첫 스트림 청크 사건의 자리: 2`와 `자료의 종류와 길이: tuple 2`가 보입니다.
진행 값 30 바로 다음 사건부터 모델의 답이 왔습니다.
자료는 둘짜리 튜플이고, 앞 값은 `AIMessageChunk`, 뒤 값은 `dict`입니다.
Ch 6 04절 `model.stream()`이 내놓던 스트림 청크와 같은 종류가, 이번에는 짝의 앞 값으로 왔습니다.

다음 셀은 모드 `messages`의 사건에서 스트림 청크만 차례대로 꺼내 목록에 담습니다."""),
        code(CHUNKS),
        md("""**결과 읽기** — 스트림 청크 수는 3절 표의 모드 `messages` 사건 수와 같습니다.
모드 `messages`의 사건 하나에 스트림 청크가 하나씩 들어 있기 때문입니다.

이번 실행에서는 출력 줄 `스트림 청크 수: 40`입니다.

다음 셀은 Ch 6 04절처럼, 글자가 없는 스트림 청크를 찾아 차례와 사용량을 봅니다.
셀 주석의 「청크」는 모두 스트림 청크를 줄여 쓴 말입니다."""),
        code(EMPTY),
        md("""**결과 읽기** — 라벨 줄 아래 글자가 없는 스트림 청크는 네 줄이고, 첫 줄은 `1 | 사용량 있음: False`입니다.
나머지 세 줄은 목록의 맨 끝 세 스트림 청크이고, 그 가운데 끝에서 둘째만 `사용량 있음: True`입니다.
Ch 6 04절에서 본 사용량이 든 스트림 청크가, 그래프 노드 안에서 부른 모델에서도 끝 쪽에 왔습니다.
Ch 6 04절에서는 끝에서 셋째에 끝난 이유가 담겼고, 마지막 빈 스트림 청크는 LangChain이 붙였습니다.
이 노트북에서는 끝난 이유를 출력하지 않았습니다.

이번 실행에서는 끝 세 줄이 38·39·40번째 스트림 청크였고, 출력 줄 `글자가 든 스트림 청크 수: 36`입니다.

## 6. 칸 metadata 읽기

칸 `metadata`는 스트림 청크와 짝으로 오는 딕셔너리로, 그 스트림 청크가 어디서 왔는지 적혀 있습니다.
편지 봉투 뒷면에 적힌 보낸 사람 주소와 같습니다.
이름에 칸이 붙었지만 상태 형식의 칸(`question`·`answer`)이 아니라, 사건 짝의 둘째 값입니다.
이 절 코드에서는 모드 `messages` 사건 자료의 뒤 값 `data[1]`입니다.
공식 문서는 이 짝을 `(message_chunk, metadata)`로 적습니다.

다음 셀은 첫 스트림 청크와 짝을 이룬 칸 `metadata`의 키를 봅니다."""),
        code(META_KEYS),
        md("""**결과 읽기** — 출력 줄 `키 수: 12`입니다.
이름이 `langgraph_`로 시작하는 키는 LangGraph가 적은 실행 자리입니다.
이름이 `ls_`로 시작하는 키는 LangChain이 적은 모델 정보입니다.
설치판 소스를 보면 키 `lc_versions`에는 설치한 LangChain 패키지의 판 번호가 담기고, 이 절에서는 값을 읽지 않습니다.
키 `checkpoint_ns`와 `langgraph_checkpoint_ns`의 값에는 실행마다 달라지는 작업 아이디가 있어, 출력하지 않습니다.

다음 셀은 실행마다 같은 값을 가진 키 넷을 꺼내 봅니다."""),
        code(META_VALUES),
        md("""**결과 읽기** — 출력 줄 `langgraph_node: write_answer`와 `langgraph_step: 1`이 보입니다.
이 스트림 청크는 그래프의 단계 1에서 실행한 노드 `write_answer` 안의 모델에서 왔습니다.
출력 줄 `ls_model_name: gpt-5.4-mini`와 `ls_temperature: 0.0`은 1절에서 만든 모델 객체의 설정과 같습니다.

다음 셀은 모든 스트림 청크의 칸 `metadata`에서 노드 이름을 모아, 서로 다른 이름만 남깁니다."""),
        code(META_ALL),
        md("""**결과 읽기** — 출력 줄 `스트림 청크가 온 노드: ['write_answer']`입니다.
이 그래프는 노드가 하나라, 모든 스트림 청크가 같은 노드에서 왔습니다.
노드가 여럿이면 키 `langgraph_node`로 어느 노드의 답인지 가릅니다.
그렇게 거르는 일은 이번에 실행하지 않았습니다.

## 7. 스트림 청크를 이어 붙이기

화면에는 스트림 청크의 글을 도착하는 대로 이어 붙여 보여 줍니다.
다 이어 붙인 글은 노드가 칸 `answer`에 낸 답 글과 같아야 합니다.
다음 셀은 Ch 6 04절처럼 글을 `+`로 이어 붙이고, 모드 `updates`가 보낸 답 글과 견줍니다."""),
        code(JOIN),
        md("""**결과 읽기** — 출력 줄 `이어 붙인 글과 답 글이 같은가: True`입니다.
화면에 이어 붙여 보여 줄 글이, 노드가 끝나며 칸 `answer`에 낸 답 글과 같았습니다.
글자가 없는 스트림 청크 넷은 이어 붙여도 글을 늘리지 않습니다.

다음 셀은 이번 실행의 답 글과 글자 수를 봅니다."""),
        code(ANSWER),
        md("""**결과 읽기** — 라벨 줄 아래는 모델이 쓴 배송 안내 글입니다.
답 글은 실행마다 달라질 수 있어, 이 절의 결론에 쓰지 않습니다.

이번 실행에서는 답 글이 두 줄이었고, 출력 줄 `글자 수: 68`입니다.
첫 줄은 「불편을 드려 죄송합니다, 주문 상태를 확인해 보겠습니다.」입니다.
둘째 줄은 「주문번호를 알려주시면 예상 배송일을 바로 안내해 드리겠습니다.」입니다.

다음 셀은 Ch 6 04절처럼 첫 스트림 청크에 나머지를 차례로 더해 하나로 합칩니다.
합친 객체에는 사용량이 든 스트림 청크의 토큰 수가 들어 있습니다."""),
        code(COMBINE),
        md("""**결과 읽기** — 출력 줄 `합친 객체 종류: AIMessageChunk`가 보입니다.
Ch 6 04절처럼 사용량이 든 스트림 청크의 토큰 수가 합친 객체에 모였습니다.

이번 실행에서는 `입력 토큰 수: 47`, `출력 토큰 수: 40`입니다.
3절 표의 모드 `messages` 사건 수와 출력 토큰 수는 같았지만, 5절의 글자가 든 스트림 청크 수와는 달랐습니다.
Ch 6 04절 교재 출력에서는 스트림 청크 수와 출력 토큰 수가 달랐으니, 스트림 청크 수를 토큰 수로 읽지 않습니다.

## 8. 모드 messages를 빼면

값 하나만 바꿔 봅니다.
바꿀 값은 모드 목록이고, 3절의 목록에서 `messages`를 뺀 `["updates", "custom"]`입니다.
실행 전에 예상해 봅니다.
진행 값 둘과 갱신 하나는 그대로 나오고, 스트림 청크는 하나도 오지 않을 것입니다.

다음 셀은 같은 문의로 그래프를 한 번 더 실행합니다(모델 요청 1번)."""),
        code(RUN2),
        md("""**결과 읽기** — 출력 줄 `받은 사건 수: 3`과 `모드 차례: ['custom', 'updates']`입니다.
진행 값은 `custom이 나온 자리: [1, 2]`로 잇달아 나왔고, 갱신은 `updates가 나온 자리: [3]`으로 맨 끝입니다.
예상대로 스트림 청크는 오지 않았고, 답 글은 맨 끝 갱신 사건에만 담겨 왔습니다.

모드 `messages`를 고르지 않으면, 노드 안 `invoke`는 스트리밍이 아닌 일반 요청을 보냅니다.
설치한 langchain-core 1.6.2 소스의 `_should_stream`(549~585행)이 그렇게 정합니다.
이 노트북에서는 요청 종류를 따로 확인하지 않았습니다.

다음 셀은 두 실행의 모드별 사건 수를 한 줄씩 견줍니다."""),
        code(COMPARE),
        md("""**결과 읽기** — 라벨 줄 아래 `updates | 1 | 1`과 `custom | 2 | 2`는 두 실행이 같습니다.
모드 `messages`를 빼도 진행 값과 갱신은 그대로 받았습니다.

이번 실행에서는 줄 `messages | 40 | 0`입니다.
세 모드를 받은 실행에서만, 모델의 답이 스트림 청크로 나뉘어 갱신보다 먼저 왔습니다.

## 정리

1. 모드 셋을 한 실행에서 함께 받자, 진행 값 30, 스트림 청크들, 진행 값 100, 갱신의 차례로 사건이 나왔습니다.
2. 모드 `messages` 사건은 스트림 청크와 칸 `metadata`의 짝이었고, 노드 이름은 모두 `write_answer`였습니다.
3. 스트림 청크의 글을 이어 붙인 글은 모드 `updates`가 보낸 답 글과 같았습니다.

03절에서는 같은 그래프를 한 번 실행하며, 첫 사건과 글자가 든 첫 스트림 청크와 끝이 언제 오는지 시간을 잽니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
L_CH05_01 = "../../part1/ch05-llm-principles/01-토큰화와-한국어-효율.html"
L_CH06_01 = "../../part2/ch06-langchain-start/01-계층-지도와-첫-호출.html"
L_CH06_04 = author_01.L_CH06_04
L_CH13_01 = author_01.L_CH13_01
L_01 = "01-일곱-가지-stream-mode.html"
L_03 = "03-TTFT와-total-비교.html"

MODE_ROWS = [
    ("<code>custom</code>", "2", "1·42", "노드가 보낸 딕셔너리 그대로(키 <code>stage</code>·<code>progress</code>)", "수와 첫 자리가 같음"),
    ("<code>messages</code>", "40", "2~41", "(스트림 청크 <code>AIMessageChunk</code>, 칸 <code>metadata</code> 딕셔너리) 짝", "수가 달라짐"),
    ("<code>updates</code>", "1", "43", "<code>{'write_answer': {'answer': 답 글}}</code>", "수와 맨 끝 자리가 같음, 답 글은 달라짐"),
]

LOOK_B5 = "노트북 4절에서 <code>모드 차례: ['custom', 'messages', 'custom', 'updates']</code>를 봅니다. 6절에서 <code>langgraph_node: write_answer</code>와 <code>스트림 청크가 온 노드: ['write_answer']</code>를 확인합니다. 7절에서 <code>이어 붙인 글과 답 글이 같은가: True</code>를 봅니다. 교재 출력에서는 스트림 청크가 40개였고, 다시 실행하면 이 수는 달라질 수 있습니다."
LOOK_B6 = "노트북 8절에서 <code>받은 사건 수: 3</code>과 <code>custom이 나온 자리: [1, 2]</code>를 확인합니다. 3절 표의 <code>updates | 1</code>과 <code>custom | 2</code>가 8절 견주기에서도 같은지 봅니다. 교재 출력의 답 글과 토큰 수는 다시 실행하면 달라질 수 있어, 이 절의 결론에 쓰지 않았습니다."


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


def src_html() -> str:
    modes = table_html(["모드", "사건 수(교재 출력)", "나온 자리(교재 출력)", "사건 하나의 모양", "다시 실행하면"], MODE_ROWS)
    return """<!--meta: 강의 1h | 실습 1.5h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>모델을 부르는 노드를 모드 셋으로 한 번 실행하고, 사건이 나온 차례를 모드 차례로 읽을 수 있습니다.</li>
<li>모드 <code>messages</code> 사건의 짝에서 스트림 청크와 칸 <code>metadata</code>를 꺼내, 어느 노드의 답인지 확인할 수 있습니다.</li>
<li>스트림 청크의 글을 이어 붙여 최종 답 글과 견주고, 실행마다 같은 값과 달라지는 값을 가를 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_01 + """\">01절</a> 그래프는 모델을 부르지 않아, 모드 <code>messages</code>의 사건이 0개였습니다. 실제 서비스의 노드는 모델을 부르고, 모델이 답을 끝까지 쓸 때까지 사용자는 빈 화면을 봅니다. 그래서 화면에는 두 가지를 함께 보여 주고 싶습니다. 하나는 모델이 쓰고 있는 답 글이고, 다른 하나는 「답을 쓰는 중」 같은 진행 표시입니다.</p><p>절 제목의 토큰 스트리밍은 모델의 답을 생기는 대로 나눠 받는 일이고, 중간 진행은 01절의 진행 값입니다. 받는 단위는 토큰이 아니라 스트림 청크라서, 본문에서는 스트림 청크라고 씁니다. 이 절은 두 가지를 한 실행에서 함께 받고, 어느 모드에서 무엇이 어떤 차례로 오는지 셉니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_01 + """\">01절</a>에서는 스트림 모드 일곱을 한 목록으로 골라, 한 실행에서 사건을 받았습니다. 진행 값은 노드가 쓰기 함수로 보내고 모드 <code>custom</code>으로만 받았습니다. 사건을 목록에 모으는 함수 <code>collect_events</code>와 한 모드의 자리를 찾는 함수 <code>positions_of</code>도 01절에서 적었습니다. 이 절은 두 함수를 도구 파일 <code>stream_tools.py</code>에서 가져옵니다.</p><p><a href=\"""" + L_CH06_04 + """\">Ch 6 04절</a>에서는 모델의 <code>stream()</code>으로 답을 도착하는 대로 나눠 받았습니다. 그 절에서 도착한 답의 일부를 스트림 청크라고 불렀습니다. 스트림 청크는 <a href=\"""" + L_CH05_01 + """\">Ch 5</a>의 토큰과 단위가 다릅니다. 글자가 없는 스트림 청크 넷, 사용량이 든 스트림 청크, 스트림 청크를 <code>+</code>로 합친 객체의 사용량도 그 절에서 보았습니다. 모델 설정 <code>temperature=0</code>·<code>reasoning_effort="none"</code>은 <a href=\"""" + L_CH06_01 + """\">Ch 6 01절</a>, 상태 형식과 노드는 <a href=\"""" + L_CH13_01 + """\">Ch 13 01절</a> 그대로입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절에서는 대나무 홈통의 물을 구멍마다 그릇으로 나눠 받았습니다. 이번에는 홈통 끝 한 곳을 봅니다. 물방울이 크기가 제각각인 채 하나씩 떨어져, 아래 대나무 통에 모입니다. 통은 물이 다 차면 한 번 기울어 물을 쏟습니다. 홈통에는 작은 종 둘이 매달려 있습니다.</p><p>떨어지는 물방울 하나가 스트림 청크 하나이고, 방울 크기가 제각각이듯 스트림 청크마다 글자 수가 다릅니다. 통이 한 번 기우는 것이 노드가 끝나며 내는 갱신 하나입니다. 종 둘은 노드가 모델 요청 앞뒤에 보내는 진행 값 둘입니다.</p><p>비유와 다른 점이 있습니다. 대나무 통은 물이 차면 저절로 기울지만, 갱신은 노드 코드가 끝까지 가야 나옵니다. 그래서 마지막 스트림 청크와 갱신 사이에 진행 값 100이 끼어 있었습니다.</p>
""" + illustration_block() + """<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>스트림 청크</td><td>스트리밍에서 한 번에 도착하는 답의 일부입니다. 홈통 끝에서 떨어지는 물방울 하나와 같습니다. 이 절에서는 모드 <code>messages</code> 사건 자료의 앞 값 <code>AIMessageChunk</code>이고, Ch 6 04절에서 본 스트림 청크와 같습니다.</td></tr><tr><td>칸 <code>metadata</code></td><td>스트림 청크와 짝으로 오는 딕셔너리로, 그 스트림 청크가 어느 노드·어느 단계·어느 모델에서 왔는지 적혀 있습니다. 편지 봉투 뒷면에 적힌 보낸 사람 주소와 같습니다. 이 절에서는 사건 자료의 뒤 값이고, 키 <code>langgraph_node</code>에 노드 이름이 있습니다. 이름에 칸이 붙었지만 그래프 상태의 칸이 아니라, 사건 짝의 둘째 값입니다.</td></tr><tr><td>모드 차례</td><td>같은 모드의 사건이 이어지면 한 번만 적어, 모드가 바뀐 차례만 남긴 목록입니다. 버스 창밖을 보며 바뀐 풍경만 적는 것과 같습니다. 이 절에서는 함수 <code>mode_order</code>가 내놓는 목록입니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 스트림 청크는 노트북 5절 출력 <code>앞 값의 종류: AIMessageChunk</code>입니다. 칸 <code>metadata</code>는 6절 출력 <code>langgraph_node: write_answer</code>처럼 읽습니다. 모드 차례는 4절 출력 <code>모드 차례: ['custom', 'messages', 'custom', 'updates']</code>입니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>노드 안의 invoke도 스트림 청크로 나옵니다</h3><p>노드는 모델을 <code>stream()</code>이 아니라 <code>invoke()</code>로 불렀습니다. 그래도 모드 <code>messages</code>를 고른 실행에서는 답이 스트림 청크로 나뉘어 왔습니다. 공식 문서도 모델을 <code>invoke</code>로 불러도 이 모드의 사건이 나온다고 적습니다.</p><p>모드 <code>messages</code>를 고르면, LangGraph가 모델 실행에 스트림 청크를 받아 가는 장치를 붙입니다. 설치판 langgraph 1.2.11에서는 <code>pregel/_messages.py</code> 49행의 <code>StreamMessagesHandler</code>입니다. 설치판 langchain-core 1.6.2의 <code>_should_stream</code>(549~585행)은 이 장치가 붙어 있을 때 스트리밍 요청을 보내게 합니다. 그래서 같은 노드 코드도, 받을 모드에 따라 모델 요청의 종류가 달라집니다. 노트북에서는 요청 종류를 확인하지 않았고, 이 차이는 설치판 소스와 노트북 밖 확인으로 본 것입니다.</p>
<h3>사건 차례는 노드 코드가 정합니다</h3><p>노드는 진행 값 30을 보낸 뒤 모델을 부르고, 답을 다 받은 뒤 진행 값 100을 보냅니다. 갱신은 노드가 칸 값을 내고 끝난 뒤에 나옵니다. 그래서 모드 차례는 진행 값, 스트림 청크들, 진행 값, 갱신이었습니다. 스트림 청크가 몇 개로 나뉘든 이 차례는 같습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 모델을 부르는 노드 하나짜리 그래프를 만듭니다. 그다음 모드 셋을 한 목록으로 골라 배송 문의 하나로 한 번 실행하고, 사건 수·모드 차례·자리를 봅니다. 5~7절은 스트림 청크와 칸 <code>metadata</code>를 읽고 스트림 청크의 글을 이어 붙입니다. 8절은 모드 <code>messages</code>를 빼고 같은 문의를 한 번 더 보냅니다.</p><p>실제 OpenAI 모델 <code>gpt-5.4-mini</code>를 temperature 0으로 부릅니다. 모델 요청은 3절과 8절에서 한 번씩, 모두 2번입니다. 요금표로 어림한 예상 비용은 0.001달러 아래이고, 청구 금액이 아닙니다. 답 글과 스트림 청크 수는 실행마다 달라질 수 있습니다. 읽거나 쓰는 파일은 없습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>모드 셋을 한 목록으로 고른 한 실행에서, 사건은 진행 값, 스트림 청크들, 진행 값, 갱신의 차례로 나왔습니다. 아래 표는 모드마다 사건 수·나온 자리·사건 하나의 모양을 모은 것입니다. 모드 <code>messages</code>에 걸린 수와 자리는 교재 출력의 값이고, 다시 실행하면 달라질 수 있습니다.</p>
""" + modes + """
<p>진행 값 30은 모델 요청보다 먼저, 첫 사건으로 왔습니다. 모델의 답은 두 진행 값 사이에만 나왔고, 갱신은 맨 끝에 한 번 나왔습니다. 이 차례와 갱신 1·진행 값 2는 노드 코드가 정하므로, 스트림 청크 수와 관계없이 같습니다. 그래서 이 절의 결론은 스트림 청크 수가 아니라 이 차례와 두 수에 둡니다.</p><p>스트림 청크의 글을 차례대로 이어 붙인 글은, 모드 <code>updates</code>가 보낸 답 글과 같았습니다. 화면에 이어 붙여 보여 줄 글이 노드가 칸에 낸 답과 어긋나지 않는다는 뜻입니다. 모든 스트림 청크의 칸 <code>metadata</code>에는 노드 이름 <code>write_answer</code>가 적혀 있었습니다.</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>노트북 8절에서 모드 <code>messages</code>를 빼자, 사건은 진행 값 둘과 갱신 하나로 셋이었습니다. 모드 차례는 <code>['custom', 'updates']</code>였고, 답 글은 맨 끝 갱신에만 담겨 왔습니다. 모드 <code>custom</code>과 <code>updates</code>의 사건 수는 두 실행이 같았습니다. 두 모드만 받는 화면은 진행 표시만 바뀌다가, 끝에 답 글을 한꺼번에 보여 주게 됩니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>모델을 부르는 절이라 답 글과 스트림 청크 수는 실행마다 달라질 수 있습니다. """ + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>스트림 청크 수·답 글·출력 토큰은 실행마다 달라집니다. 노트북 밖에서 같은 요청을 다섯 번 보내자 모드 <code>messages</code>의 사건은 34~50개였습니다. 모드 차례·진행 값·갱신 수·이어 붙인 글과 답 글이 같은지는 다섯 번 모두 같았고, 이 절은 그 값만 결론에 썼습니다.</li><li>교재 출력과 노트북 밖 다섯 번 모두, 모드 <code>messages</code>의 사건 수와 출력 토큰 수가 같았습니다. 글자가 든 스트림 청크 수와는 달랐고, 두 수가 같아지는 까닭은 이번에 확인하지 않았습니다. Ch 6 04절 교재 출력은 스트림 청크 18개·출력 토큰 17개로 달랐습니다. 그래서 스트림 청크 수를 토큰 수로 읽지 않습니다.</li><li>모드 <code>messages</code>를 고르지 않은 실행에서는 노드 안 <code>invoke</code>가 스트리밍 요청을 보내지 않습니다. 설치판 langchain-core 1.6.2 <code>language_models/chat_models.py</code> 549~585행과 1969행으로 확인했습니다. 노트북 밖에서 모델이 새 스트림 청크를 알린 횟수를 세어 보니 다섯 번 모두 0이었습니다. 노트북에서는 요청 종류를 확인하지 않았습니다.</li><li>그래서 모드마다 따로 실행하면 요청 종류부터 달라질 수 있습니다. <a href=\"""" + L_03 + """\">03절</a>은 모드를 한 실행에서 함께 받아 시간을 잽니다.</li><li>공식 문서의 모드 표는 모드 <code>messages</code>의 앞 값을 LLM token이라고 적습니다. 이 절에서 받은 앞 값의 종류는 <code>AIMessageChunk</code>였고, 본문은 스트림 청크라고 불렀습니다.</li><li>진행 값 30과 100은 우리가 정한 값입니다. 실제 작업량(처리한 문서 수 등)을 세어 보내지 않으면, 화면에 진행률로 약속할 수 없습니다.</li><li>칸 <code>metadata</code>의 키 <code>checkpoint_ns</code>·<code>langgraph_checkpoint_ns</code>에는 실행마다 다른 작업 아이디가 있어 출력하지 않았습니다. 노드가 여럿인 그래프에서 키 <code>langgraph_node</code>로 스트림 청크를 거르는 일은 이번에 실행하지 않았습니다.</li><li>비동기 메서드 <code>astream</code>과 인자 <code>version="v2"</code>는 01절처럼 이번에도 실행하지 않았습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>모드 셋을 한 실행에서 함께 받자, 진행 값 30, 스트림 청크들, 진행 값 100, 갱신의 차례로 사건이 나왔습니다.</li><li>모드 <code>messages</code> 사건은 스트림 청크와 칸 <code>metadata</code>의 짝이었고, 노드 이름은 모두 <code>write_answer</code>였습니다.</li><li>스트림 청크의 글을 이어 붙인 글은 모드 <code>updates</code>가 보낸 답 글과 같았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_03 + """\">03절</a>에서는 첫 사건·글자가 든 첫 스트림 청크·끝이 언제 오는지 시간을 잽니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 모드 셋을 함께 받은 실행에서 첫 사건이 모드 <code>custom</code>이었던 까닭은 무엇인가요?</p><p class="quiz-a">노드가 모델 요청보다 먼저 쓰기 함수로 진행 값 30을 보냈기 때문입니다. 틀렸다면 노트북 3·4절을 다시 읽습니다.</p><p class="quiz-q">2. 모드 <code>messages</code> 사건에서 어느 노드의 답인지 알려 주는 값은 무엇인가요?</p><p class="quiz-a">짝의 뒤 값인 칸 <code>metadata</code>의 키 <code>langgraph_node</code>입니다. 이 절에서는 <code>write_answer</code>였습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">3. 스트림 청크 수를 이 절의 결론에 쓰지 않은 까닭은 무엇인가요?</p><p class="quiz-a">같은 요청도 실행마다 달라질 수 있는 값이기 때문입니다. 결론은 실행마다 같은 모드 차례와 갱신 1·진행 값 2에 두었습니다. 틀렸다면 노트북 3·5절과 본문 「주의할 점과 실무 메모」를 다시 읽습니다.</p><p class="quiz-q">4. 모드 <code>messages</code>를 빼고 실행하면 받은 사건이 어떻게 달라졌나요?</p><p class="quiz-a">진행 값 둘과 갱신 하나로 사건이 셋이었고, 스트림 청크는 오지 않았습니다. 답 글은 맨 끝 갱신에만 담겨 왔습니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langgraph/streaming">LangGraph Streaming</a></div>확인 2026-09-25 · 모드 <code>messages</code>의 짝 <code>(message_chunk, metadata)</code>와, 모델을 <code>invoke</code>로 불러도 사건이 나온다는 설명이 있습니다. 키 <code>langgraph_node</code>로 거르는 방법과 함수 <code>get_stream_writer</code> 설명도 있습니다.</li><li>langchain-core 1.6.2 소스 <code>language_models/chat_models.py</code> 549~585행은 <code>_should_stream</code>입니다. 1969~2016행은 스트리밍 요청을 보내 스트림 청크마다 알리고, 마지막 빈 스트림 청크를 붙이는 자리입니다.</li><li>langgraph 1.2.11 소스 <code>pregel/_messages.py</code> 49행은 <code>StreamMessagesHandler</code>, 151~164행은 새 스트림 청크를 사건으로 내보내는 자리입니다.</li><li>Ch 6 04절에서 스트림 청크와 사용량이 든 스트림 청크를, 01절에서 스트림 모드와 진행 값을 보았습니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    check_same_as_01()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "stream_tools.py").write_text(TOOLS, encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        # 도구 파일은 없거나 이 판과 같을 때만 쓴다. 뒤 절(03)이 함수를 더한 판이면 덮어쓰지 않는다(Ch 24 마감 A-10).
        current = ""
        if TOOLS_PATH.is_file():
            current = TOOLS_PATH.read_text(encoding="utf-8")
        # 04절 판은 머리 설명 뒤에 가져오기 줄을 더했으므로, 그 줄을 빼고 02절 판으로 시작하는지 봅니다
        plain = strip_later_imports(current)
        assert current == "" or plain.startswith(TOOLS), "도구 파일이 02절 판으로 시작하지 않습니다"
        if current == "" or current == TOOLS:
            TOOLS_PATH.write_text(TOOLS, encoding="utf-8")
            print("wrote", TOOLS_PATH)
        else:
            print("skip", TOOLS_PATH, "(뒤 절이 함수를 더한 판 — 덮어쓰지 않음)")
        path = write_notebook(LAB, "02", SLUG, "experiment", cells())
        print("wrote", path)
