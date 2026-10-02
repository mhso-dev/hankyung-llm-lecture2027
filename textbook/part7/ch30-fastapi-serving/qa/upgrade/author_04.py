"""Ch 30 04절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§5-3·§6 experiment).

사용:
  python3 -B author_04.py            → 도구 파일(없거나 04 판일 때만) + 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_04.py --src-only → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_04.py --tools-copy DIR → 디스크의 도구 파일을 DIR에 복사한다(새 커널 사본 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**. 슬러그 그대로
(Ch 25 04 b8 「Ch 30 04절은 모드 custom의 사건을 비동기 메서드 astream으로 받아 이어 붙입니다」가 링크).

## 결정 1 — 모드 custom + astream + 이어 붙이기 (handoff §03 → §04 1·2)

astream을 부르기만 → async_generator(Ch 6 04 generator의 비동기 판) → 셀 맨 위 async for로 사건 여섯 →
같은 객체 다시 async for → 0 → astream을 새로 불러 받을 때마다 칸 token을 이어 붙임(여섯 줄이 늘어남) →
끝 공백 하나(노드가 piece + " "를 적음) → strip하면 ainvoke 답과 같음 → 사건 수 = 답의 낱말 수.
async for는 이 절이 처음 풀이(뜻 → 일상 예 → 코드). 비동기 생성기 yield는 쓰지 않는다(앱 chat_stream은 05 몫).

## 결정 2 — 실험: 인자 stream_mode 하나만 "custom" → ["custom", "updates"] (handoff §03 → §04 3·6)

실행 1 사건 여섯(모두 dict) · 실행 2 사건 일곱(모두 짝) — custom 자리 [1..6], updates 자리 [7], 모드 차례 ['custom', 'updates'],
custom 자료만 이어 붙인 글 = 실행 1 글. 결론은 차례·자리·개수(매번 같은 값)만. 노트북 밖 /tmp/ch30-04/exp 5/5 같음.
걸린 시간은 재지 않는다(규격 §3 주제 절 예외를 쓰지 않음) — b2 「첫 응답 지연」은 차례(노드 끝 사건보다 진행 값이 먼저)로 바꿈.

## 결정 3 — 도구 파일 serve_tools.py 첫 판 (handoff 챕터 공통 9 · 규격 §2-7)

Ch 25 도구 파일 stream_tools.py(마감 판 3a734aeb…)에서 이 노트북이 쓰는 함수 둘(positions_of·mode_order)의 설명 주석과 본문을
글자 그대로 옮긴다. import 0. 쓰기 가드: 파일이 없거나 이 판과 같을 때만 쓰고, 뒤 절이 함수를 더한 판(strip_later_imports 뒤
이 판으로 시작)은 건너뜀. 이 절이 처음 가르친 join_tokens·collect_events_async는 노트북에 둔다(뒤 절이 쓰면 그 절이 옮김).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 딕셔너리 `.get`·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·대입 풀기(for 포함)·별표 풀기·
`while`·`try`·세미콜론·`isinstance`·클래스·데코레이터·가짜 에이전트·`asyncio`·`join`·`yield`. async def는 collect_events_async 하나,
셀 맨 위 await 셋(ainvoke 하나·collect_events_async 둘)과 셀 맨 위 async for 셋(노트북 도구 기능). 호출 깊이 2 이하.
"""
from __future__ import annotations

import ast
import hashlib
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part7/ch30-fastapi-serving/notebooks"
FIGS = ROOT / "textbook/part7/ch30-fastapi-serving/figures"
SLUG = "04-astream과-응답-스트림"
TITLE_TEXT = "astream과 응답 스트림"
SRC = ROOT / "textbook/part7/ch30-fastapi-serving/_src" / (SLUG + ".html")
AUTHOR01 = ROOT / "textbook/part7/ch30-fastapi-serving/qa/upgrade/author_01.py"
TOOLS_PATH = LAB / "serve_tools.py"
STREAM_TOOLS = ROOT / "labs/part6/ch25-streaming/notebooks/stream_tools.py"
# 전체 마감(2026-09-30)에서 Ch 25 도구 파일 머리 설명 줄만 고쳐 3a734aeb… → 6df804b8…(함수 본문 같음)
STREAM_TOOLS_SHA = "6df804b89b55ff77b1a148746b68c021767b1ddf7163d6a2194e94c922127db4"
RUNS_SENTENCE = os.environ.get("AUTHOR04_RUNS_SENTENCE", "새 커널로 두 번 실행해 견주자, 코드 셀 스물셋의 출력이 셀마다 모두 같았습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 노트북 밖에서도 같은 장면을 파이썬 파일로 다섯 번 실행해, 출력이 모두 같았습니다. 모델을 부르지 않아, 사건의 차례와 개수는 노드 코드가 정합니다.")

# ---------------------------------------------------------------- 도구 파일 serve_tools.py (첫 판)
TOOLS_HEAD = '''"""Ch 30 FastAPI로 Agent 서빙 — 앞 챕터와 이 챕터 앞 절에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from serve_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
이 챕터 노트북이 실제로 쓰는 함수만 담고, 새 함수가 필요한 절이 그때 더합니다.
Ch 25 도구 파일 stream_tools.py에서 옮긴 함수는 설명 주석과 본문을 글자 그대로 옮겼습니다.
이 챕터 02·04·05·06·07절 노트북에서 처음 적은 함수 열은 그 셀의 주석과 본문을 글자 그대로 옮겼습니다.
앞 챕터 도구 파일은 그 챕터 실습 폴더에 묶여 있어, 파일째 가져오지 않습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
실습 앱 파일(agent_service/)은 이 챕터가 가르치는 코드라 이 파일과 따로 둡니다.
"""
'''

STREAM_NOTES = [
    ("positions_of", "Ch 25 01절에서 배웠습니다 — Ch 25 도구 파일 stream_tools.py의 같은 이름 함수를 옮겼습니다"),
    ("mode_order", "Ch 25 02절에서 배웠습니다 — Ch 25 도구 파일 stream_tools.py의 같은 이름 함수를 옮겼습니다"),
]
TOOL_ORDER = ["positions_of", "mode_order"]


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
            # 맨 위 한 줄은 「…에서 배웠습니다」 줄이라 빼고, 그 아래 설명 주석부터 가져옵니다
            return "\n".join(lines[top + 1:node.end_lineno])
    raise KeyError(name)


def tools_text() -> str:
    source = STREAM_TOOLS.read_text(encoding="utf-8")
    assert hashlib.sha256(source.encode("utf-8")).hexdigest() == STREAM_TOOLS_SHA, "Ch 25 stream_tools.py가 마감 판과 다릅니다"
    text = TOOLS_HEAD
    for name, note in STREAM_NOTES:
        text = text + "\n\n# " + note + "\n" + file_block(source, name) + "\n"
    return text


TOOLS = tools_text()


def strip_later_imports(text: str) -> str:
    """머리 설명과 첫 함수 주석 사이에 뒤 절이 더한 가져오기 줄이 있으면 빼고 내놓습니다(Ch 25~29 대조 사슬과 같은 줄).

    뒤 절 판이 04절 판을 그대로 이어 쓰는지 볼 때는, 이 가져오기 줄을 빼고 앞머리를 견줍니다.
    """
    if not text.startswith(TOOLS_HEAD):
        return text
    rest = text[len(TOOLS_HEAD):]
    first = rest.find("\n\n# Ch ")
    if first <= 0:
        return text
    return TOOLS_HEAD + rest[first:]


def check_tools() -> None:
    """도구 파일 04절 판의 함수 둘이 Ch 25 stream_tools.py 마감 판과 글자·AST 모두 같은지 봅니다."""
    source = STREAM_TOOLS.read_text(encoding="utf-8")
    tree = ast.parse(TOOLS)
    names = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise AssertionError("04절 판 도구 파일은 아무것도 가져오지 않습니다")
    assert names == TOOL_ORDER, names
    source_tree = ast.parse(source)
    for name, note in STREAM_NOTES:
        block = file_block(source, name)
        assert ("# " + note + "\n" + block + "\n") in TOOLS
        mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        theirs = [ast.dump(n) for n in source_tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        assert mine == theirs and len(mine) == 1, name


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["fastapi==0.135.0", "httpx==0.28.1", "pydantic==2.12.5", "starlette==1.6.0",
                          "langgraph==1.2.11", "langchain==1.4.0"])

IMPORTS = r'''# 이 절에서 쓸 이름을 가져옵니다(os·inspect는 Python에 들어 있는 모듈입니다)
import os
import inspect
# Ch 25 01·02절에서 배운 함수 둘은 도구 파일에서 가져옵니다
from serve_tools import mode_order, positions_of

print("가져온 이름:", "inspect")
print("도구 파일에서 가져온 함수:", "mode_order, positions_of")'''

# 01절 2절 셀 글 그대로(아래 __main__에서 author_01.py와 문자열 대조)
FIND_LAB = r'''# 노트북을 연 자리에서 본 실습 폴더의 위치를 후보 셋 가운데에서 고릅니다
candidates = ["..", ".", "labs/part7/ch30-fastapi-serving"]
lab_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/agent_service/schemas.py"):
        lab_path = candidate
        break
print("실습 폴더를 찾았는가:", lab_path is not None)
assert lab_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

IMPORT_AGENT = r'''# 작업 폴더를 실습 폴더로 옮기고, 그래프 파일에서 그래프와 노드 함수를 가져옵니다
os.chdir(lab_path)
from agent_service.agent import agent, answer_node
print("가져온 그래프의 종류:", type(agent).__name__)
print("그래프의 노드 이름:", list(agent.nodes))'''

NODE_SOURCE = r'''# 노드 함수 answer_node를 소스 글 그대로 출력합니다(inspect.getsource는 03절에서 썼습니다)
node_source = inspect.getsource(answer_node)
print("노드 함수 answer_node의 소스:")
print(node_source)'''

MAKE_INPUT = r'''# 03절과 같은 질문으로, 그래프에 넣을 입력을 만듭니다
question_input = {"messages": ["반납 기한을 알려 주세요"]}
print("입력:", question_input)'''

CALL_ONLY = r'''# astream을 모드 custom으로 부르기만 하고, 받은 값의 종류를 봅니다
# astream은 입력과 모드를 받아, 스트림 사건을 하나씩 꺼낼 수 있는 객체를 내놓습니다
stream_obj = agent.astream(question_input, stream_mode="custom")
print("부르기만 해서 받은 값의 종류:", type(stream_obj).__name__)'''

ASYNC_FOR = r'''# async for로 사건을 하나씩 꺼내, 받을 때마다 출력하고 목록에 담습니다
events = []
async for event in stream_obj:
    print("받은 스트림 사건:", event)
    events.append(event)
print("받은 사건 수:", len(events))'''

EVENT_SHAPE = r'''# 첫 사건의 종류와 키, 칸 token의 값을 봅니다
first_event = events[0]
print("첫 사건의 종류:", type(first_event).__name__)
print("첫 사건의 키:", list(first_event))
print("첫 사건의 칸 token:", first_event["token"])'''

AGAIN = r'''# 이미 끝까지 꺼낸 stream_obj에서 사건을 한 번 더 꺼내 봅니다
again_events = []
async for event in stream_obj:
    again_events.append(event)
print("다시 꺼낸 사건 수:", len(again_events))'''

LIVE_JOIN = r'''# astream을 새로 불러, 사건을 받을 때마다 칸 token의 글을 뒤에 이어 붙이고 출력합니다
shown_text = ""
async for event in agent.astream(question_input, stream_mode="custom"):
    shown_text = shown_text + event["token"]
    print("지금까지 이어 붙인 글:", shown_text)'''

END_SPACE = r'''# 이어 붙인 글의 끝 글자를 보고, 03절처럼 ainvoke로 받은 답과 견줍니다
print("끝 글자가 공백인가:", shown_text.endswith(" "))
result = await agent.ainvoke(question_input)
print("ainvoke 결과의 칸 answer:", result["answer"])
print("그대로 견주면 같은가:", shown_text == result["answer"])
# strip()은 글의 앞뒤 공백을 지운 새 글을 내놓습니다
print("앞뒤 공백을 지우고 견주면 같은가:", shown_text.strip() == result["answer"])'''

COUNT_RULE = r'''# 답을 공백으로 나눈 낱말 수와, 3절에서 받은 사건 수를 견줍니다
answer_words = result["answer"].split()
print("답의 낱말:", answer_words)
print("답의 낱말 수:", len(answer_words))
print("받은 사건 수:", len(events))
print("두 수가 같은가:", len(answer_words) == len(events))'''

DEF_JOIN = r'''# 진행 값 목록을 받아, 칸 token의 글을 차례대로 이어 붙인 글을 내놓습니다
def join_tokens(stream_values):
    joined = ""
    for value in stream_values:
        joined = joined + value["token"]
    return joined'''

DEF_COLLECT = r'''# 그래프를 astream으로 한 번 실행하며 받은 사건을 차례대로 목록에 모아 내놓습니다
async def collect_events_async(graph_to_run, graph_input, modes):
    collected = []
    # stream_mode에 목록을 주면, 사건 하나가 (모드 이름, 자료) 짝으로 나옵니다
    async for event in graph_to_run.astream(graph_input, stream_mode=modes):
        collected.append(event)
    return collected'''

RUN1 = r'''# 실행 1: 모드 custom 하나로 사건을 모읍니다
run1_events = await collect_events_async(agent, question_input, "custom")
print("사건 수:", len(run1_events))
print("첫 사건:", run1_events[0])
print("마지막 사건:", run1_events[-1])
print("이어 붙인 글이 4절과 같은가:", join_tokens(run1_events) == shown_text)'''

RUN2 = r'''# 실행 2: 값 하나만 바꿔, 모드 목록 custom·updates로 사건을 모읍니다
run2_events = await collect_events_async(agent, question_input, ["custom", "updates"])
print("사건 수:", len(run2_events))
first_pair = run2_events[0]
print("첫 사건의 종류와 길이:", type(first_pair).__name__, len(first_pair))
print("첫 사건:", first_pair)
print("마지막 사건:", run2_events[-1])'''

RUN2_LIST = r'''# 실행 2의 사건을 받은 차례대로, 자리·모드 이름·자료를 한 줄씩 출력합니다
print("자리 | 모드 이름 | 자료")
for index in range(len(run2_events)):
    event = run2_events[index]
    # 사건 하나는 (모드 이름, 자료) 짝이라, [0]이 모드 이름이고 [1]이 자료입니다
    print(index + 1, "|", event[0], "|", event[1])'''

RUN2_POSITIONS = r'''# 도구 파일의 함수 둘로, 모드 차례와 모드마다 나온 자리를 봅니다
print("모드 차례:", mode_order(run2_events))
print("custom 나온 자리:", positions_of(run2_events, "custom"))
print("updates 나온 자리:", positions_of(run2_events, "updates"))'''

RUN2_JOIN = r'''# 실행 2에서 모드 custom의 자료만 모아 이어 붙이고, 실행 1의 글과 견줍니다
custom_values = []
for event in run2_events:
    if event[0] == "custom":
        custom_values.append(event[1])
print("모은 진행 값 수:", len(custom_values))
print("이어 붙인 글이 실행 1과 같은가:", join_tokens(custom_values) == join_tokens(run1_events))'''

UPDATE_VALUE = r'''# 실행 2의 마지막 사건인 updates의 자료에서, 노드가 낸 갱신을 봅니다
update_data = run2_events[-1][1]
print("updates 자료의 키:", list(update_data))
print("노드 answer가 낸 갱신:", update_data["answer"])
print("칸 answer가 ainvoke 답과 같은가:", update_data["answer"]["answer"] == result["answer"])'''

RESULT_TABLE = r'''# 두 실행의 사건 수·진행 값 수·사건의 종류·updates 자리를 한 표로 모읍니다
print("견준 것 | 실행 1 | 실행 2")
print("모드 | custom | custom, updates")
print("사건 수 |", len(run1_events), "|", len(run2_events))
print("진행 값 수 |", len(run1_events), "|", len(custom_values))
print("사건의 종류 |", type(run1_events[0]).__name__, "|", type(first_pair).__name__)
print("updates 나온 자리 | 없음 |", positions_of(run2_events, "updates"))'''

APP_LINES = r'''# 앱 파일을 글로 읽어, astream을 부르는 줄과 모드를 적은 줄만 줄 번호와 함께 출력합니다
with open("agent_service/app.py", encoding="utf-8") as app_file:
    app_text = app_file.read()
app_lines = app_text.splitlines()
print("줄 번호 | 줄")
for index in range(len(app_lines)):
    line = app_lines[index]
    if "astream(" in line or "stream_mode=" in line:
        print(index + 1, "|", line.strip())'''

# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/04-figures.md)
FIG1 = "04-1-진행-값에서-이어-붙인-글까지"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 초록 상자 입력 messages에 질문 하나에서 초록 상자 노드 answer 낱말마다 쓰기 함수로 진행 값을 적음으로 이어집니다. 이어서 회색 상자 astream 모드 custom, 파란 상자 async for로 사건을 하나씩 받음, 노란 상자 스트림 사건 여섯 모두 칸 token 하나를 지납니다. 마지막으로 파란 상자 받을 때마다 글을 뒤에 이어 붙임과 노란 상자 이어 붙인 글 끝에 공백 하나 공백을 지우면 ainvoke 답과 같음 True로 이어지는 그림"
FIG1_CAP = "노드가 낱말마다 적은 진행 값을 astream이 사건 여섯으로 내놓았고, 받을 때마다 이어 붙인 글은 공백을 지우자 ainvoke의 답과 같았습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자 둘은 우리가 넣은 입력과 실습 폴더의 노드이고, 회색 상자는 라이브러리 메서드입니다.
파란 상자 둘은 노트북에서 우리가 쓴 줄이고, 노란 상자 둘은 노트북 3·4절의 출력입니다."""

FIG2 = "04-2-부르기만-한-astream과-async-for"
FIG2_ALT = "위에서 아래로 읽는 흐름도입니다. 파란 상자 stream_obj = agent.astream 부르기만 함에서 노란 상자 받은 값의 종류 async_generator로 갑니다. 이어서 파란 상자 async for event in stream_obj와 노란 상자 받은 사건 여섯 첫 사건의 종류 dict를 지나, 파란 상자 같은 stream_obj를 다시 async for와 노란 상자 다시 꺼낸 사건 없음으로 이어지는 그림"
FIG2_CAP = "astream을 부르기만 하자 비동기 제너레이터를 받았고, async for로 사건 여섯을 꺼낸 뒤에는 같은 객체에서 꺼낼 사건이 없었습니다."
FIG2_READ = """위에서 아래로 읽습니다.
파란 상자 셋은 노트북 3절에서 우리가 쓴 줄이고, 노란 상자 셋은 그 셀들의 출력입니다.
Ch 6 04절의 제너레이터처럼, 끝까지 꺼낸 비동기 제너레이터도 비어 있었습니다."""

FIG3 = "04-3-사건-수는-답의-낱말-수"
FIG3_ALT = "위에서 아래로 읽는 그림입니다. 초록 상자 노드가 만든 답 글 질문을 확인했습니다: 반납 기한을 알려 주세요에서 초록 상자 공백으로 나눔 낱말 여섯, 초록 상자 낱말마다 뒤에 공백을 붙여 칸 token에 적음으로 이어집니다. 마지막 초록 상자에서 화살표 둘이 노란 상자 사건 수와 낱말 수가 같음 True와 노란 상자 끝 글자가 공백 True 공백을 지우면 ainvoke 답과 같음 True로 가는 그림"
FIG3_CAP = "사건 수 여섯은 노드가 답 글을 공백으로 나눈 낱말 수이고, 낱말마다 붙인 공백 때문에 이어 붙인 글 끝에도 공백이 하나 남았습니다."
FIG3_READ = """위에서 아래로 읽습니다.
초록 상자 셋은 노트북 2절에서 출력한 노드 함수의 줄을 차례대로 적은 것입니다.
노란 상자 둘은 4절 출력으로, 사건 수 규칙과 끝 공백을 확인한 값입니다."""

FIG4 = "04-4-모드-하나와-모드-목록의-사건-자리"
FIG4_ALT = "맨 위에 초록 상자 같은 그래프와 같은 입력이 있고, 그 아래 칸 둘이 나란히 놓여 있습니다. 왼쪽 칸 실행 1에는 파란 상자 stream_mode custom과 노란 상자 사건 여섯 모두 dict 진행 값이 있습니다. 오른쪽 칸 실행 2에는 파란 상자 stream_mode 목록 custom과 updates, 노란 상자 자리 1에서 6 custom 진행 값 여섯, 노란 상자 자리 7 updates 노드 answer가 낸 갱신이 위에서 아래로 있습니다. 두 칸 아래 노란 상자 두 실행의 이어 붙인 글 같음 True로 이어지는 그림"
FIG4_CAP = "모드 목록에 updates를 더한 실행 2에서는 진행 값 여섯이 자리 1에서 6에 오고, 노드 끝 갱신 updates가 맨 끝 자리 7에 왔습니다."
FIG4_READ = """맨 위 초록 상자는 두 실행이 함께 쓴 그래프와 입력입니다.
왼쪽 칸이 실행 1, 오른쪽 칸이 실행 2이고, 칸마다 맨 위 파란 상자가 바꾼 값입니다.
노란 상자는 5절 출력이고, 맨 아래 상자는 두 실행의 글을 견준 출력입니다.
실험 절이라 빨강은 쓰지 않았습니다."""

ILLU = "04-5-한-칸씩-들어오는-화물-열차"
ILLU_ALT = "흰 바탕에 곧은 선로 하나가 가로로 놓여 있습니다. 선로 위에 왼쪽부터 지붕 위 작은 망루가 있는 겨자색 끝 칸 하나, 청록 통을 하나씩 세워 실은 옅은 회색 평판 짐칸 넷, 빈 평판 짐칸 둘, 짙은 빨강 기관차 하나가 이어져 있습니다. 선로 앞에는 길고 낮은 회색 콘크리트 짐 내리는 자리가 있고, 빈 짐칸 앞쪽에 청록 통 둘이 나란히 서 있습니다. 사람·글자·숫자·화살표는 없는 그림"
ILLU_CAP = "앞 칸 둘의 통은 벌써 내려 한 줄로 놓였고, 뒤 칸 넷에는 아직 통이 실려 있으며, 맨 뒤에 모양이 다른 끝 칸이 붙어 있습니다."
# 1차 job 3daa081f-1b59-4d77-80ba-70283944f3f8 채택(재생성 1회 — 2차 175fe2d5는 짐칸 넷·통 다섯으로 개수가 어긋나 탈락) — 저장 PNG를 열어 센 개수로 적음
ILLU_READ = "흰 바탕의 선로 위에 오른쪽부터 짙은 빨강 기관차 하나와 빈 평판 짐칸 둘이 있습니다. 그 뒤로 청록 통을 하나씩 실은 짐칸 넷과, 겨자색 끝 칸 하나가 이어집니다. 선로 앞 낮은 짐 내리는 자리에는 청록 통 둘이 나란히 서 있습니다. 짐칸 여섯이 스트림 사건 여섯이고, 내려 놓은 통 둘은 먼저 받아 이어 붙인 진행 값입니다. 아직 실린 통 넷은 뒤에 받을 진행 값이고, 맨 왼쪽 끝 칸이 실행 2의 마지막 사건 <code>updates</code>입니다."

METAPHOR = """<p>화물역 선로로 짐을 실은 열차가 들어옵니다. 짐칸 여섯에 통이 하나씩 실려 있고, 맨 뒤에는 모양이 다른 끝 칸이 붙어 있습니다. 역에서는 먼저 들어온 앞 칸부터 통을 내려, 선로 앞 짐 내리는 자리에 한 줄로 놓습니다. 앞 칸 둘의 통이 벌써 줄에 놓였을 때, 뒤 칸 넷에는 아직 통이 실려 있습니다.</p><p>02·03절에서는 짐칸을 처리 함수와 결과의 칸에 짝지었지만, 이 절부터는 짐칸 하나가 스트림 사건 하나입니다. 칸에 실린 통이 진행 값입니다. 통을 내려 줄 끝에 놓는 일이 칸 <code>token</code>의 글을 이어 붙이는 일이고, 줄에 놓인 통이 지금까지 이어 붙인 글입니다. 맨 뒤 끝 칸은 실행 2에서 맨 끝 자리 7에 온 모드 <code>updates</code>의 사건입니다.</p><p>비유와 다른 점이 있습니다. 실제 열차는 칸이 들어오는 데 시간이 걸리지만, 이 절은 걸린 시간을 재지 않고 차례만 봅니다. 또 끝 칸은 모드 목록에 <code>updates</code>를 더했을 때만 붙고, 모드 <code>custom</code> 하나인 실행 1에는 없습니다.</p>"""

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 노드가 답을 낱말마다 진행 값으로 적는 줄을 읽습니다.
2. 비동기 메서드 `astream`과 `async for`로 스트림 사건을 하나씩 받아 이어 붙입니다.
3. 모드 목록에 `updates`를 더해, 노드 끝 사건이 진행 값보다 뒤에 오는지 실험합니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
예상 비용도 0달러입니다.
실습 앱의 에이전트 그래프는 모델을 쓰지 않고, 정해 둔 말로 답합니다.
그래서 다시 실행해도 같은 값이 나와야 합니다.

그래프를 같은 노트북 안에서 바로 부릅니다.
서버 프로그램을 띄우지 않고, 네트워크와 포트를 쓰지 않습니다.
실습 폴더의 파일을 가져오고 읽기만 하며, 쓰는 파일은 없습니다.

걸린 시간은 재지 않았습니다.
이 절은 사건이 온 차례와 개수만 봅니다.
앞 챕터에서 배운 함수 둘은 도구 파일 `serve_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 여섯을 설치합니다.
판은 fastapi 0.135.0, httpx 0.28.1, pydantic 2.12.5, starlette 1.6.0입니다.
패키지 langgraph 1.2.11과 langchain 1.4.0은 실습 앱 파일이 가져오는 패키지입니다.
여섯 모두 실습 폴더 잠금과 같은 판입니다.

교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~4절을 읽고, 5절 실험의 가설을 함께 세웁니다.
5절의 두 실행과 6절은 실습 시간에 실행합니다.

실습 폴더 `labs/part7/ch30-fastapi-serving`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

03절에서는 처리 함수가 그래프를 await와 `ainvoke`로 불러, 끝난 결과를 한 번에 받았습니다.
이 절은 같은 그래프를 비동기 메서드 `astream`으로 불러, 노드가 적은 값을 하나씩 받습니다.
제목의 astream은 Ch 25에서 배운 메서드 `stream`의 비동기 판입니다.

첫 셀은 패키지 여섯을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `fastapi: 0.135.0`과 `langgraph: 1.2.11`이 보입니다.
여섯 모두 실습 폴더 잠금과 같은 판이고, 03절과 같은 목록입니다.
이 절은 모델 객체를 만들지 않아, API 키를 확인하는 셀도 없습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모듈 `inspect`는 03절에서 함수의 소스 글을 꺼낼 때 쓴 모듈입니다.
마지막 가져오기 줄은 Ch 25에서 배운 함수 둘을 도구 파일에서 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: mode_order, positions_of`가 보입니다.
함수 `positions_of`는 Ch 25 01절, `mode_order`는 Ch 25 02절에서 배웠습니다.
두 함수 모두 (모드 이름, 자료) 짝의 목록을 받습니다.
Ch 25 도구 파일 `stream_tools.py`의 같은 이름 함수를, 주석과 본문 그대로 옮겼습니다.

앞에서 배운 함수는 `serve_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다.

다음 셀은 01절 2절과 같은 파일 위치 셀로, 후보 셋 가운데 실습 폴더를 고릅니다."""),
        code(FIND_LAB),
        md("""**결과 읽기** — 출력 줄 `실습 폴더를 찾았는가: True`가 보입니다.
고른 후보는 연 자리마다 달라서 출력하지 않습니다.
실습 폴더 맨 위에서 연 커널은 이 안내를 보기 전에, 앞 셀의 도구 파일 가져오기에서 먼저 멈춥니다.

다음 셀은 03절처럼 작업 폴더를 실습 폴더로 옮긴 뒤 이름을 가져옵니다.
그래프 파일 `agent.py`에서 에이전트 그래프 `agent`와 노드 함수 `answer_node`를 가져옵니다."""),
        code(IMPORT_AGENT),
        md("""**결과 읽기** — 출력 줄 `가져온 그래프의 종류: CompiledStateGraph`가 보입니다.
노드 이름은 `['__start__', 'answer']`이고, 답을 만드는 노드는 `answer` 하나입니다.
03절에서 본 것처럼 이 노드는 비동기 노드이고, 모델을 쓰지 않습니다.

## 2. 노드가 진행 값을 적는 줄

Ch 25 01절에서는 노드 안에서 `get_stream_writer()`로 쓰기 함수를 꺼내 진행 값을 보냈습니다.
실습 그래프의 노드도 같은 방법으로 진행 값을 적습니다.
다음 셀은 노드 함수 `answer_node`의 소스 글을 그대로 출력합니다."""),
        code(NODE_SOURCE),
        md("""**결과 읽기** — 라벨 줄 아래에 정의 줄부터 `return` 줄까지 열두 줄이 있습니다.
셋째 줄의 함수 `_compose_answer`가 답 글 전체를 먼저 만듭니다.
그다음 줄 `writer = get_stream_writer()`가 쓰기 함수를 꺼냅니다.
그래프 밖에서 노드 함수를 바로 부르면 이 줄이 오류 `RuntimeError`를 내서, `try`로 받아 `None`으로 둡니다.

반복 줄 `for piece in answer.split():`은 답 글을 공백으로 나눈 낱말마다 돕니다.
낱말마다 `await asyncio.sleep(0)`으로 한 번 쉬고, `writer({"token": piece + " "})`로 진행 값을 적습니다.
Python 문서는 0초 쉬기를 다른 작업에 차례를 넘기는 방법이라고 적습니다.
그래서 진행 값 하나는 칸 `token` 하나를 가진 딕셔너리이고, 낱말 뒤에 공백이 붙습니다.

다음 셀은 03절과 같은 질문으로 입력을 만듭니다."""),
        code(MAKE_INPUT),
        md("""**결과 읽기** — 출력 줄 `입력: {'messages': ['반납 기한을 알려 주세요']}`가 보입니다.
03절 3절의 입력과 같은 모양, 같은 질문입니다.

## 3. astream과 async for

03절 4절에서는 이 그래프를 동기 메서드 `stream`으로 불러 오류 `TypeError`를 받았습니다.
그 오류 글은 비동기로 부르는 메서드로 `ainvoke`와 `astream`을 적었습니다.
메서드 `astream`은 `stream`의 비동기 판이고, 인자 `stream_mode`도 같습니다.
다음 셀은 모드 `custom`으로 `astream`을 부르기만 하고, 받은 값의 종류를 봅니다."""),
        code(CALL_ONLY),
        md("""**결과 읽기** — 출력 줄 `부르기만 해서 받은 값의 종류: async_generator`가 보입니다.
받은 값은 비동기 제너레이터(async generator)이고, 이 줄에서는 사건을 하나도 받지 않았습니다.
Ch 6 04절에서 메서드 `stream()`이 준 객체 종류는 `generator`였습니다.
비동기 제너레이터는 그 제너레이터의 비동기 판으로, 값을 하나 꺼낼 때마다 await로 기다려 받습니다.

값을 꺼내는 반복이 비동기 반복(async for)입니다.
보통 반복처럼 값을 하나씩 꺼내 본문을 실행하되, 꺼낼 때마다 다음 값을 await로 기다립니다.
역에 칸이 하나 들어올 때마다 기다렸다가 짐을 내리는 일과 같습니다.
다음 셀은 `async for`로 사건을 꺼내, 받을 때마다 출력하고 목록에 담습니다.
셀 맨 위의 `async for`는 셀 맨 위 await처럼 노트북 도구(IPython)의 기능입니다."""),
        code(ASYNC_FOR),
        md("""**결과 읽기** — 라벨 `받은 스트림 사건:`이 붙은 줄이 여섯이고, 출력 줄 `받은 사건 수: 6`이 보입니다.
첫 사건은 `{'token': '질문을 '}`이고, 마지막 사건은 `{'token': '주세요 '}`입니다.
사건마다 낱말 하나와 그 뒤 공백 하나가 칸 `token`에 들어 있습니다.
Ch 25 01절에서 본 진행 값이, 비동기 판에서도 스트림 사건으로 하나씩 왔습니다.

다음 셀은 첫 사건의 종류와 키를 출력해 모양을 확인합니다."""),
        code(EVENT_SHAPE),
        md("""**결과 읽기** — 출력 줄 `첫 사건의 종류: dict`와 `첫 사건의 키: ['token']`이 보입니다.
모드를 하나만 고르면 사건은 자료 그대로이고, 모드 이름이 붙지 않습니다.
Ch 25 01절에서 모드를 목록으로 골랐을 때의 (모드 이름, 자료) 짝과 다른 모양입니다.
칸 `token`의 값 `질문을 ` 뒤에도 공백이 하나 있습니다.

Ch 6 04절에서는 끝까지 꺼낸 제너레이터가 비어 있었습니다.
다음 셀은 이미 끝까지 꺼낸 `stream_obj`에서 사건을 한 번 더 꺼내 봅니다."""),
        code(AGAIN),
        md("""**결과 읽기** — 출력 줄 `다시 꺼낸 사건 수: 0`이 보입니다.
한 번 끝까지 꺼낸 비동기 제너레이터는 비어 있어, 사건을 하나도 받지 않았습니다.
사건을 다시 받으려면 메서드 `astream`을 새로 불러야 합니다.

## 4. 받을 때마다 이어 붙이기

화면에 답을 앞 낱말부터 보이려면, 사건을 받을 때마다 글을 뒤에 붙입니다.
다음 셀은 `astream`을 새로 불러, 칸 `token`의 글을 받을 때마다 이어 붙이고 출력합니다.
반복 줄에서 메서드를 바로 부르는 모양은 6절에서 볼 앱 파일과 같습니다."""),
        code(LIVE_JOIN),
        md("""**결과 읽기** — 라벨 `지금까지 이어 붙인 글:`이 붙은 줄이 여섯입니다.
첫 줄은 `지금까지 이어 붙인 글: 질문을`이고, 줄마다 낱말이 하나씩 늘어납니다.
마지막 줄은 `지금까지 이어 붙인 글: 질문을 확인했습니다: 반납 기한을 알려 주세요`입니다.
사건을 받을 때마다 반복 본문이 한 번씩 실행되어, 받은 차례대로 글이 길어졌습니다.

다음 셀은 이어 붙인 글의 끝 글자를 보고, 03절처럼 `ainvoke`로 받은 답과 견줍니다."""),
        code(END_SPACE),
        md("""**결과 읽기** — 출력 줄 `끝 글자가 공백인가: True`와 `그대로 견주면 같은가: False`가 보입니다.
출력 줄 `앞뒤 공백을 지우고 견주면 같은가: True`도 보입니다.
이어 붙인 글은 끝에 공백이 하나 남아, 그대로는 `ainvoke`의 답과 다릅니다.
메서드 `strip()`으로 앞뒤 공백을 지우자 같은 글이 되었습니다.

다음 셀은 사건 수가 어디서 정해지는지, 답의 낱말 수와 견줍니다."""),
        code(COUNT_RULE),
        md("""**결과 읽기** — 출력 줄 `답의 낱말 수: 6`과 `받은 사건 수: 6`, `두 수가 같은가: True`가 보입니다.
라벨 `답의 낱말:` 줄에는 정해 둔 말의 두 낱말과 질문의 네 낱말이 있습니다.
2절에서 읽은 대로, 노드가 답을 공백으로 나눈 낱말마다 진행 값을 하나씩 적었기 때문입니다.
노드 코드로 보면 질문의 낱말 수가 바뀔 때 사건 수도 바뀌고, 이번에는 다른 질문을 넣지 않았습니다.

## 5. 실험: 모드 목록에 updates를 더하기

Ch 25 01절에서는 동기 `stream`으로 모드를 목록으로 골라, 사건이 나온 자리를 봤습니다.
그때 노드가 보낸 진행 값은 그 노드의 갱신(`updates`)보다 먼저 나왔습니다.
이 실험은 같은 차례가 비동기 판 `astream`에서도 나오는지 봅니다.
바꿀 값은 인자 `stream_mode` 하나이고, 그래프와 입력은 그대로 둡니다.

**가설** — 실행 1은 모드 `custom` 하나, 실행 2는 모드 목록 `["custom", "updates"]`입니다.
실행 2에서는 노드가 끝난 뒤의 갱신 사건이 하나 더해져, 사건이 일곱이 될 것입니다.
더해진 사건은 진행 값 여섯보다 뒤, 맨 끝 자리에 올 것입니다.
진행 값 여섯과 이어 붙인 글은 두 실행에서 같을 것입니다.

두 실행에 쓸 함수 둘을 먼저 정의합니다.
다음 셀은 4절에서 셀로 적은 이어 붙이기를 함수로 묶습니다."""),
        code(DEF_JOIN),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
진행 값 목록을 받아, 칸 `token`의 글을 차례대로 이어 붙인 글을 내놓습니다.
앞뒤 공백은 지우지 않아, 4절의 글처럼 끝에 공백이 남습니다.

다음 셀은 그래프를 `astream`으로 한 번 실행하며, 받은 사건을 목록에 모으는 함수를 정의합니다.
Ch 25 01절 함수 `collect_events`와 같은 일을 `async for`로 하고, 인자 `config`는 받지 않습니다.
함수 안에서 `async for`를 쓰므로 정의 줄은 `async def`이고, 부를 때는 await를 붙입니다."""),
        code(DEF_COLLECT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
인자 `modes`에 모드 이름 하나를 주면 자료가, 목록을 주면 (모드 이름, 자료) 짝이 모입니다.

**실행 1** — 다음 셀은 모드 `custom` 하나로 사건을 모읍니다.
실행 전에 예상해 봅니다.
사건은 몇 개이고, 이어 붙인 글은 4절과 같을까요?"""),
        code(RUN1),
        md("""**결과 읽기** — 출력 줄 `사건 수: 6`과 `이어 붙인 글이 4절과 같은가: True`가 보입니다.
첫 사건은 `{'token': '질문을 '}`, 마지막 사건은 `{'token': '주세요 '}`로 3절과 같습니다.
실행 1의 사건은 모두 진행 값입니다.

**실행 2** — 다음 셀은 값 하나만 바꿔, 모드 목록 `["custom", "updates"]`로 사건을 모읍니다.
실행 전에 예상해 봅니다.
사건 수와 사건의 모양은 어떻게 바뀔까요?"""),
        code(RUN2),
        md("""**결과 읽기** — 출력 줄 `사건 수: 7`과 `첫 사건의 종류와 길이: tuple 2`가 보입니다.
첫 사건은 `('custom', {'token': '질문을 '})`로, 모드 이름과 자료의 짝입니다.
마지막 사건은 `('updates', {'answer': {'answer': '질문을 확인했습니다: 반납 기한을 알려 주세요'}})`입니다.
가설대로 사건이 하나 늘었고, 첫 사건과 마지막 사건 모두 짝입니다.

다음 셀은 일곱 사건을 받은 차례대로 한 줄씩 출력합니다.
사건 하나에서 모드 이름은 `event[0]`, 자료는 `event[1]`로 꺼냅니다."""),
        code(RUN2_LIST),
        md("""**결과 읽기** — 라벨 줄 아래 일곱 줄 가운데 첫 줄은 `1 | custom | {'token': '질문을 '}`입니다.
자리 1부터 6까지는 모두 `custom`이고, 마지막 줄은 `7 | updates | {'answer': {'answer': '질문을 확인했습니다: 반납 기한을 알려 주세요'}}`입니다.
진행 값 여섯이 차례대로 온 뒤에, 노드의 갱신이 한 번 왔습니다.

다음 셀은 Ch 25의 함수 둘로 이 차례를 목록으로 받아 봅니다.
함수 `mode_order`는 모드가 바뀐 차례를, `positions_of`는 한 모드의 사건이 나온 자리를 내놓습니다."""),
        code(RUN2_POSITIONS),
        md("""**결과 읽기** — 출력 줄 `모드 차례: ['custom', 'updates']`가 보입니다.
출력 줄 `custom 나온 자리: [1, 2, 3, 4, 5, 6]`과 `updates 나온 자리: [7]`도 보입니다.
모드 `updates`의 사건은 일곱 사건 가운데 맨 끝 자리 7에 왔습니다.
가설대로, 노드가 끝난 뒤의 갱신은 진행 값 여섯보다 뒤였습니다.

다음 셀은 실행 2에서 모드 `custom`의 자료만 모아 이어 붙이고, 실행 1의 글과 견줍니다."""),
        code(RUN2_JOIN),
        md("""**결과 읽기** — 출력 줄 `모은 진행 값 수: 6`과 `이어 붙인 글이 실행 1과 같은가: True`가 보입니다.
모드 `updates`를 더해도, 진행 값의 수와 글은 바뀌지 않았습니다.

다음 셀은 마지막 사건인 `updates`의 자료를 꺼내, 노드가 낸 갱신을 봅니다."""),
        code(UPDATE_VALUE),
        md("""**결과 읽기** — 출력 줄 `updates 자료의 키: ['answer']`가 보입니다.
키 `answer`는 노드 이름이고, 그 값 `{'answer': '질문을 확인했습니다: 반납 기한을 알려 주세요'}`가 노드가 낸 갱신입니다.
출력 줄 `칸 answer가 ainvoke 답과 같은가: True`도 보입니다.
노드는 진행 값 여섯을 모두 적은 뒤에 칸 `answer`를 내며 끝났고, 그 갱신이 마지막 사건이었습니다.

다음 셀은 두 실행을 한 표로 모읍니다."""),
        code(RESULT_TABLE),
        md("""**결과 읽기** — 라벨 줄 아래 다섯 줄이 두 실행을 견줍니다.
사건 수는 `사건 수 | 6 | 7`, 사건의 종류는 `사건의 종류 | dict | tuple`입니다.
진행 값 수는 두 실행 모두 여섯이고, 마지막 줄은 `updates 나온 자리 | 없음 | [7]`입니다.

**결론** — 바꾼 값은 인자 `stream_mode` 하나였습니다.
모드 목록에 `updates`를 더하자 사건이 여섯에서 일곱으로 늘고, 모두 (모드 이름, 자료) 짝이 되었습니다.
진행 값 여섯은 자리 1~6에 그대로 왔고, 노드 끝 갱신은 맨 끝 자리 7에 왔습니다.
그래서 받는 쪽이 첫 진행 값을 받은 때에는, 노드 끝 사건을 아직 받지 않은 상태입니다.
이 노트북은 걸린 시간을 재지 않았고, 사건이 온 차례만 확인했습니다.

## 6. 앱 파일에서 astream을 부르는 자리

실습 앱 파일도 처리 함수 안에서 `astream`을 부릅니다.
다음 셀은 앱 파일을 글로 읽어, `astream`을 부르는 줄과 모드를 적은 줄만 줄 번호와 함께 출력합니다."""),
        code(APP_LINES),
        md("""**결과 읽기** — 라벨 줄 아래에 네 줄이 있습니다.
첫 두 줄은 `110 | async for chunk in runtime.astream(`와 `111 | {"messages": [body.question]}, stream_mode="custom"`입니다.
처리 함수 `chat_stream`이 이 절과 같은 모드 `custom`으로 `astream`을 부르는 자리입니다.
나머지 두 줄(134·136행)은 모드 `messages`로 부르는 처리 함수 `live_chat_stream`의 줄입니다.

처리 함수 `chat_stream`은 받은 진행 값을 서버 응답으로 보내며, 05절에서 봅니다.
모드 `messages`는 모델이 쓴 글을 받는 모드로, 모델을 부르는 09절에서 씁니다.
두 처리 함수 모두 몸통에서 `astream`을 부르므로, 요청이 올 때마다 새로 부릅니다.

## 정리

1. 비동기 메서드 `astream`은 비동기 제너레이터를 내놓았고, `async for`로 모드 `custom`의 스트림 사건 여섯을 받았습니다.
2. 칸 `token`의 글을 받을 때마다 이어 붙이자 끝에 공백이 하나 남았고, 공백을 지우면 `ainvoke`의 답과 같았습니다.
3. 모드 목록에 `updates`를 더하자 사건이 일곱이 되었고, 노드 끝 갱신은 진행 값 여섯 뒤 자리 7에 왔습니다.

05절에서는 처리 함수 `chat_stream`이 이 진행 값을 SSE 응답으로 보내는 모양을 봅니다."""),
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
    """노트북용 마크다운 한 단락(백틱·줄바꿈)을 _src 문단 글로 바꿉니다(01~03절 생성기와 같은 함수)."""
    parts = text.replace("\n", " ").split("`")
    out = ""
    for index in range(len(parts)):
        if index % 2 == 1:
            out = out + "<code>" + parts[index] + "</code>"
        else:
            out = out + parts[index]
    return out


def mermaid_block(name: str, alt: str, caption: str, reading: str) -> str:
    """.mmd가 있을 때만 본문에 넣습니다(새 커널 A·B를 그림보다 먼저 돌릴 때 빌드가 멈추지 않게)."""
    if not (FIGS / (name + ".mmd")).is_file():
        return ""
    return ("{{mermaid:" + name + "|" + alt + "|" + caption + "}}\n"
            + '<p class="look"><b>도식 읽기</b> — ' + html_text(reading) + "</p>\n")


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


L_CH02_12 = "../../part1/ch02-python/12-async와-await.html"
L_CH06_04 = "../../part2/ch06-langchain-start/04-스트리밍과-content-blocks.html"
L_CH25_01 = "../../part6/ch25-streaming/01-일곱-가지-stream-mode.html"
L_CH25_02 = "../../part6/ch25-streaming/02-토큰과-중간-진행-스트리밍.html"
L_CH25_03 = "../../part6/ch25-streaming/03-TTFT와-total-비교.html"
L_03 = "03-ainvoke-요청-응답.html"
L_05 = "05-POST-SSE-이벤트-설계.html"
L_09 = "09-실제-Agent-HTTP-통합.html"

TERM_ROWS = [
    ("비동기 제너레이터(async generator)", "값을 하나 꺼낼 때마다, 그 값이 준비될 때까지 await로 기다려 받는 제너레이터입니다. 오븐에서 빵이 한 판 나올 때마다 기다렸다가 진열대에 올리는 일과 같습니다. 이 절에서는 <code>agent.astream(…)</code>을 부르기만 해서 받은 값이고, 종류 이름은 <code>async_generator</code>입니다."),
    ("비동기 반복(async for)", "비동기 제너레이터에서 값을 하나씩 꺼내, 꺼낼 때마다 본문을 실행하는 반복입니다. 역에 칸이 하나 들어올 때마다 기다렸다가 짐을 내리는 일과 같습니다. 이 절에서는 <code>async for event in stream_obj:</code>가 스트림 사건 여섯을 차례로 꺼냈습니다."),
    ("스트림 사건 · 진행 값 — Ch 25 01절에서 이어 씀", "스트림 사건은 메서드가 한 번에 하나씩 내놓는 값이고, 진행 값은 노드가 쓰기 함수로 적은 값입니다. 이 절의 진행 값은 칸 <code>token</code> 하나를 가진 딕셔너리입니다. 모드 <code>custom</code> 하나만 고르면 사건이 진행 값 그대로이고, 모드를 목록으로 고르면 (모드 이름, 자료) 짝입니다."),
]

COMPARE_ROWS = [
    ("바꾼 값 <code>stream_mode</code>", "<code>\"custom\"</code>", "<code>[\"custom\", \"updates\"]</code>"),
    ("사건 수", "<code>6</code>", "<code>7</code>"),
    ("사건의 종류", "<code>dict</code> — 진행 값 그대로", "<code>tuple</code> — (모드 이름, 자료) 짝"),
    ("진행 값이 나온 자리", "사건 여섯 모두", "<code>[1, 2, 3, 4, 5, 6]</code>"),
    ("<code>updates</code>가 나온 자리", "없음", "<code>[7]</code>"),
    ("이어 붙인 글", "4절의 글과 같음 <code>True</code>", "실행 1의 글과 같음 <code>True</code>"),
]

LOOK_B5 = "노트북 3절에서 <code>부르기만 해서 받은 값의 종류: async_generator</code>와 <code>받은 사건 수: 6</code>을 찾습니다. <code>다시 꺼낸 사건 수: 0</code>도 확인합니다. 4절에서는 <code>끝 글자가 공백인가: True</code>와 <code>앞뒤 공백을 지우고 견주면 같은가: True</code>를 봅니다."
LOOK_B6 = "5절 실행 2의 출력 <code>사건 수: 7</code>과 <code>updates 나온 자리: [7]</code>을 찾습니다. 출력 <code>custom 나온 자리: [1, 2, 3, 4, 5, 6]</code>과 <code>이어 붙인 글이 실행 1과 같은가: True</code>도 확인합니다. 6절에서는 <code>111 | {\"messages\": [body.question]}, stream_mode=\"custom\"</code> 줄을 봅니다."


def src_html() -> str:
    terms = table_html(["말", "뜻"], TERM_ROWS)
    compare = table_html(["견준 것", "실행 1(모드 custom)", "실행 2(모드 목록 custom·updates)"], COMPARE_ROWS)
    return """<!--meta: 강의 1.25h | 실습 2.5h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 2 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>비동기 메서드 <code>astream</code>과 <code>async for</code>로 모드 <code>custom</code>의 스트림 사건을 하나씩 받을 수 있습니다.</li>
<li>받은 진행 값의 칸 <code>token</code>을 차례대로 이어 붙이고, <code>ainvoke</code>의 답과 견줄 수 있습니다.</li>
<li>모드 목록에 <code>updates</code>를 더한 실험으로, 노드 끝 사건이 진행 값 뒤에 오는 것을 자리로 확인할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_03 + """\">03절</a>의 <code>ainvoke</code>는 그래프가 끝난 뒤의 결과를 한 번에 주었습니다. 웹 화면에 답을 앞 낱말부터 차례로 붙여 보이려면, 노드가 적은 값을 하나씩 받아야 합니다. 이 앱의 노드는 답을 낱말마다 진행 값으로 적습니다. 비동기 메서드 <code>astream</code>은 그 진행 값을 스트림 사건으로 하나씩 내놓습니다.</p><p>제목의 astream은 Ch 25에서 배운 메서드 <code>stream</code>의 비동기 판입니다. 03절에서는 이 그래프를 동기 <code>stream</code>으로 부르자 오류로 끝났습니다. 제목의 응답 스트림은 이렇게 받은 사건을 서버 응답으로 보내는 일이고, <a href=\"""" + L_05 + """\">05절</a>에서 다룹니다. 이 절은 그 앞 단계로, 같은 프로그램 안에서 사건을 받는 방법을 봅니다.</p><p>받는 차례도 봅니다. 노드가 끝났다는 사건보다 진행 값이 먼저 오면, 받는 쪽은 끝 사건을 받기 전부터 앞 낱말을 붙일 수 있습니다. 이 절은 걸린 시간을 재지 않고, 사건이 온 차례만 봅니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_03 + """\">03절</a>에서는 처리 함수가 그래프를 await와 <code>ainvoke</code>로 부르는 것을 봤습니다. 메서드 <code>ainvoke</code>를 부르기만 하면 코루틴이 나왔고, await 줄에서 그래프가 끝까지 실행되었습니다. 이 그래프의 노드는 비동기 노드라, 동기 메서드 <code>invoke</code>와 <code>stream</code>은 오류 <code>TypeError</code>로 끝났습니다. 그때 동기 <code>stream</code>은 스트림 사건을 하나도 받지 못했습니다.</p><p><a href=\"""" + L_CH25_01 + """\">Ch 25 01절</a>에서는 인자 <code>stream_mode</code>로 스트림 모드를 골랐습니다. 노드 안에서 <code>get_stream_writer()</code>로 꺼낸 쓰기 함수에 넣은 값이 진행 값이고, 모드 <code>custom</code>을 골라야 받았습니다. 모드를 목록으로 고르면 사건이 (모드 이름, 자료) 짝으로 나왔고, 진행 값이 노드의 갱신보다 먼저 왔습니다. 그 절의 함수 <code>positions_of</code>와 <a href=\"""" + L_CH25_02 + """\">02절</a>의 함수 <code>mode_order</code>를 이 절은 도구 파일에서 가져옵니다.</p><p><a href=\"""" + L_CH25_03 + """\">Ch 25 03절</a>은 사건마다 시각을 적었지만, 초는 실행마다 달라 결론에는 사건 차례만 썼습니다. 이 절은 시각을 적지 않고 차례만 봅니다.</p><p><a href=\"""" + L_CH06_04 + """\">Ch 6 04절</a>에서는 메서드 <code>stream()</code>이 제너레이터를 내놓았습니다. 제너레이터는 반복이 하나를 꺼낼 때마다 다음 값을 만드는 객체였고, 끝까지 꺼내면 비었습니다. <a href=\"""" + L_CH02_12 + """\">Ch 2 12절</a>에서는 비동기 함수·코루틴·await·이벤트 루프를 배웠습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3>""" + METAPHOR + """
""" + illustration_block() + """<h3>astream과 async for</h3><p>컴파일한 그래프에는 메서드 <code>stream</code>의 비동기 판 <code>astream</code>이 있습니다. 부르기만 하면 사건을 받지 않고, 비동기 제너레이터 하나를 받습니다. 비동기 제너레이터는 Ch 6 04절 제너레이터의 비동기 판입니다. 값을 하나 꺼낼 때마다, 그 값이 준비될 때까지 await로 기다립니다.</p><p>이 제너레이터에서 값을 꺼내는 반복이 <code>async for</code>입니다. Python 언어 참조는 이 반복이 값마다 await로 다음 값을 꺼내는 반복과 같다고 적습니다. 파이썬 파일에서는 비동기 함수 안에서만 쓸 수 있고, 밖에서 쓰면 <code>SyntaxError</code>입니다. 노트북 셀 맨 위의 <code>async for</code>는 셀 맨 위 await처럼 노트북 도구(IPython)의 기능입니다.</p>
""" + terms + """
<p>새 말을 이 절 코드에서 보면 이렇습니다. 메서드 <code>astream</code>을 부르기만 하자 받은 값의 종류가 <code>async_generator</code>였습니다. 반복 <code>async for</code>로 꺼내자 사건 여섯이 차례로 왔고, 끝까지 꺼낸 뒤 다시 꺼낸 사건 수는 <code>0</code>이었습니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h3>노드가 적는 진행 값</h3><p>실습 그래프의 노드 함수 <code>answer_node</code>는 답 글 전체를 먼저 만든 뒤 공백으로 나눕니다. 낱말마다 <code>await asyncio.sleep(0)</code>으로 한 번 쉬고, 쓰기 함수에 <code>{"token": piece + " "}</code>를 넣습니다. Python 문서는 0초 쉬기를 다른 작업에 차례를 넘기는 방법이라고 적습니다.</p><p>그래서 진행 값 수는 답의 낱말 수와 같고, 칸 <code>token</code>의 글 끝에는 늘 공백이 하나 붙습니다. 이어 붙인 글의 끝에도 공백이 하나 남아, 03절 <code>ainvoke</code>의 답과 견주려면 앞뒤 공백을 지웁니다.</p><h3>모드 목록과 사건의 차례</h3><p>모드를 목록으로 고르면 사건 하나가 (모드 이름, 자료) 짝으로 옵니다. Ch 25 01절처럼 짝의 첫째가 모드 이름, 둘째가 자료입니다. 이 절은 짝을 두 이름으로 나눠 받지 않고, <code>event[0]</code>·<code>event[1]</code>로 꺼냅니다.</p><p>모드 <code>updates</code>는 노드가 끝난 뒤 그 노드가 낸 갱신을 사건으로 내놓습니다. LangGraph 문서의 모드 표도 <code>updates</code>를 각 단계가 끝난 뒤의 상태 갱신이라고 적습니다. 모드 <code>custom</code>은 노드가 쓰기 함수로 보낸 값을 내놓습니다.</p><p>설치판 langgraph 1.2.11 <code>pregel/main.py</code> 3283~3297행은 모드 <code>custom</code>이면 쓰기 함수가 값을 대기열에 넣게 합니다. 3395~3399행과 3440~3457행은 노드가 실행되는 동안에도 대기열의 사건을 꺼내 내놓게 합니다. 이 동작은 설치판 소스로 보았고, 노트북에서는 사건이 온 차례만 확인했습니다. 사건마다 받은 시각은 재지 않았습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 노드 함수 <code>answer_node</code>의 소스를 출력해, 진행 값을 적는 줄을 읽습니다. 3절은 <code>astream</code>을 부르기만 해 받은 값의 종류를 보고, <code>async for</code>로 사건 여섯을 받습니다. 같은 객체에서 한 번 더 꺼내면 사건이 없다는 것도 봅니다. 4절은 사건을 받을 때마다 글을 이어 붙이고, 03절처럼 <code>ainvoke</code>로 받은 답과 견줍니다.</p><p>5절은 인자 <code>stream_mode</code> 하나만 바꾼 두 실행으로 실험하고, 6절은 앱 파일에서 <code>astream</code>을 부르는 줄을 읽습니다. 모델 요청은 0번이고, API 키 없이 실행합니다. 서버 프로그램을 띄우지 않아 네트워크·포트·자식 프로세스를 쓰지 않습니다. 실습 폴더의 파일을 가져오고 읽기만 하며, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>가설은 Ch 25 01절의 차례에서 세웠습니다. 모드 목록에 <code>updates</code>를 더하면 사건이 하나 늘고, 늘어난 사건은 진행 값 여섯보다 뒤에 온다는 예상이었습니다. 두 실행에서 그래프와 입력은 같았고, 바꾼 것은 인자 <code>stream_mode</code> 하나였습니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + compare + """
<p>실행 2에서 진행 값 여섯은 자리 1~6에, 모드 <code>updates</code>의 사건은 자리 7에 왔습니다. 노드가 끝난 뒤 나오는 갱신이 맨 끝이었고, 진행 값은 모두 그 앞이었습니다. 가설대로였고, Ch 25 01절에서 동기 <code>stream</code>으로 본 차례와 같았습니다.</p><p>진행 값의 수와 글은 모드를 더해도 바뀌지 않았습니다. 실행 2에서 모드 <code>custom</code>의 자료만 모아 이어 붙인 글은 실행 1의 글과 같았습니다. 모드 <code>updates</code>의 자료에는 노드 <code>answer</code>가 낸 칸 <code>answer</code>가 있었고, <code>ainvoke</code>의 답과 같았습니다.</p><p>이 차례가 받는 쪽에 주는 뜻은 이렇습니다. 첫 진행 값을 받은 때에는 노드 끝 사건을 아직 받지 않았습니다. 그래서 화면에 앞 낱말을 붙이는 일은 노드 끝 사건을 기다리지 않고 시작할 수 있습니다. 다만 걸린 시간은 재지 않았고, 스트리밍하지 않은 <code>ainvoke</code>와 시간을 견주지도 않았습니다. 스트리밍이 몇 초를 줄이는지는 이 절 결과로 말할 수 없습니다.</p>
<p>""" + RUNS_SENTENCE + """</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>이 실습 노드는 답 글 전체를 먼저 만든 뒤, 낱말마다 나눠 적습니다. 그래프 파일 25행이 답을 만들고, 30~33행이 낱말마다 적습니다. 그래서 진행 값은 모델이 글을 쓰는 빠르기가 아니라, 노드 코드의 나누기 규칙을 따릅니다. 모델이 쓴 글을 받는 모드 <code>messages</code>는 <a href=\"""" + L_09 + """\">09절</a>에서 씁니다.</li><li>사건 수 여섯은 답을 공백으로 나눈 낱말 수이고, 이 질문의 값입니다. 질문의 낱말 수가 다르면 사건 수도 달라지므로, 여섯을 다른 질문에 그대로 쓰지 않습니다. 이 절에서는 다른 질문을 넣어 보지 않았습니다.</li><li>한 번 끝까지 꺼낸 비동기 제너레이터는 비어 있습니다. 노트북 3절에서 다시 꺼낸 사건 수가 <code>0</code>이었습니다. 사건을 다시 받으려면 메서드 <code>astream</code>을 새로 부릅니다.</li><li>셀 맨 위의 <code>async for</code>와 await는 노트북 도구(IPython)의 기능입니다. 파이썬 파일에서는 비동기 함수 안에 적고, Ch 2 12절처럼 <code>asyncio.run</code>으로 실행합니다. 노트북 밖의 다섯 번 실행은 이 모양으로 했습니다.</li><li>앱 파일 110~111행은 이 절과 같은 모드 <code>custom</code>으로 <code>astream</code>을 부르고, 05절에서 그 사건을 서버 응답으로 보냅니다. 134·136행은 모드 <code>messages</code>로 부르고, 09절에서 씁니다.</li><li>LangGraph 문서는 인자 <code>version="v2"</code>를 주면 사건이 칸 <code>type</code>을 가진 딕셔너리로 바뀐다고 적습니다. 이 절은 기본값 <code>"v1"</code>의 모양만 썼고, v2는 실행하지 않았습니다. 문서 첫머리는 새 앱에 LangGraph 1.2의 다른 스트리밍 방식을 권합니다. 이 절은 실습 앱 파일이 쓰는 스트림 모드 방식을 따랐습니다.</li><li>질문에 「오류」라는 글자가 들어가면 노드가 일부러 오류 <code>RuntimeError</code>를 냅니다. 그래프 파일 18~19행에 교재용으로 넣어 둔 줄입니다. 이 절에서는 그 글자가 든 질문을 보내지 않았습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>비동기 메서드 <code>astream</code>은 비동기 제너레이터를 내놓았고, <code>async for</code>로 모드 <code>custom</code>의 스트림 사건 여섯을 받았습니다.</li><li>칸 <code>token</code>의 글을 받을 때마다 이어 붙이자 끝에 공백이 하나 남았고, 공백을 지우면 <code>ainvoke</code>의 답과 같았습니다.</li><li>모드 목록에 <code>updates</code>를 더하자 사건이 일곱이 되었고, 노드 끝 갱신은 진행 값 여섯 뒤 자리 7에 왔습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_05 + """\">05절</a>에서는 처리 함수 <code>chat_stream</code>이 이 진행 값을 SSE 응답으로 보내는 모양을 봅니다. 사건마다 이름과 번호를 붙여 보내는 방법입니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. 메서드 <code>astream</code>을 부르기만 하면 무엇을 받나요?</p><p class="quiz-a">비동기 제너레이터(<code>async_generator</code>)를 받고, 그 줄에서는 사건을 받지 않습니다. 반복 <code>async for</code>로 꺼낼 때마다 사건이 하나씩 옵니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">2. 이어 붙인 글과 <code>ainvoke</code>의 답을 그대로 견주면 왜 <code>False</code>인가요?</p><p class="quiz-a">노드가 낱말마다 뒤에 공백을 붙여 적어서, 이어 붙인 글 끝에 공백이 하나 남기 때문입니다. 메서드 <code>strip()</code>으로 앞뒤 공백을 지우면 같은 글이 됩니다. 틀렸다면 노트북 2절과 4절을 다시 읽습니다.</p><p class="quiz-q">3. 동료가 「astream은 늘 사건을 여섯 번 준다」고 말합니다. 맞나요?</p><p class="quiz-a">맞지 않습니다. 여섯은 노드가 이 질문의 답을 공백으로 나눈 낱말 수입니다. 질문의 낱말 수가 다르면 노드 코드에 따라 사건 수도 달라집니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">4. 실행 2에서 모드 <code>updates</code>의 사건은 몇 번째 자리에 왔고, 그것은 무엇을 뜻하나요?</p><p class="quiz-a">일곱 사건 가운데 맨 끝 자리 7에 왔습니다. 노드가 끝난 뒤의 갱신이라, 진행 값 여섯보다 뒤였습니다. 그래서 첫 진행 값을 받은 때에는 노드 끝 사건을 아직 받지 않은 상태입니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">5. 끝까지 꺼낸 <code>stream_obj</code>로 다시 <code>async for</code>를 하면 사건을 몇 개 받나요?</p><p class="quiz-a">하나도 받지 않습니다. 노트북 3절의 출력은 <code>다시 꺼낸 사건 수: 0</code>이었습니다. 다시 받으려면 메서드 <code>astream</code>을 새로 부릅니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langgraph/streaming">LangGraph Streaming</a></div>확인 2026-09-29 · 메서드 <code>stream</code>(동기)과 <code>astream</code>(비동기)이 출력을 하나씩 꺼내게 한다고 적습니다. 모드 표는 <code>custom</code>을 노드가 <code>get_stream_writer</code>로 보낸 값, <code>updates</code>를 각 단계 뒤의 상태 갱신이라고 적습니다.</li><li><div><a href="https://docs.python.org/3.12/reference/compound_stmts.html#the-async-for-statement">Python The async for statement</a></div>확인 2026-09-29 · 반복마다 await로 다음 값을 꺼내는 반복과 같다고 적습니다. 비동기 함수 밖에서 쓰면 <code>SyntaxError</code>라고 적습니다.</li><li><div><a href="https://docs.python.org/3.12/library/asyncio-task.html#asyncio.sleep">Python asyncio.sleep</a></div>확인 2026-09-29 · 0초로 쉬면 다른 작업이 실행될 차례를 준다고 적습니다.</li><li>설치판 langgraph 1.2.11 소스 <code>pregel/main.py</code> 3063행이 메서드 <code>astream</code>을 정의하고, 인자 <code>version</code>의 기본값은 <code>"v1"</code>입니다. 3283~3297행은 모드 <code>custom</code>이면 쓰기 함수가 값을 대기열에 넣게 합니다. 3300~3303행은 그 모드를 고르지 않으면 아무것도 하지 않는 쓰기 함수를 둡니다. 3395~3399행과 3440~3457행은 노드가 실행되는 동안 대기열의 사건을 꺼내 내놓습니다. <code>config.py</code> 126행이 함수 <code>get_stream_writer</code>입니다.</li><li>실습 폴더 <code>agent_service/agent.py</code> 23~34행이 노드 함수 <code>answer_node</code>이고, 30~33행이 낱말마다 진행 값을 적습니다. <code>agent_service/app.py</code> 110~111행은 처리 함수 <code>chat_stream</code>, 134·136행은 <code>live_chat_stream</code>이 <code>astream</code>을 부르는 줄입니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    # 1절 파일 위치 셀은 01절 셀 글 그대로(「01절 2절과 같은 파일 위치 셀」 문장의 근거)
    assert FIND_LAB in AUTHOR01.read_text(encoding="utf-8"), "FIND_LAB이 01절 셀과 다릅니다"
    check_tools()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "serve_tools.py").write_text(TOOLS_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        # 도구 파일은 없거나 이 판과 같을 때만 쓴다. 뒤 절이 함수를 더한 판이면 덮어쓰지 않는다(Ch 24 마감 A-10·Ch 25~29 교훈).
        current = ""
        if TOOLS_PATH.is_file():
            current = TOOLS_PATH.read_text(encoding="utf-8")
        # 뒤 절 판은 머리 설명 뒤에 가져오기 줄을 더할 수 있으므로, 그 줄을 빼고 04절 판으로 시작하는지 봅니다
        plain = strip_later_imports(current)
        assert current == "" or plain.startswith(TOOLS), "도구 파일이 04절 판으로 시작하지 않습니다"
        if current == "" or current == TOOLS:
            TOOLS_PATH.write_text(TOOLS, encoding="utf-8")
            print("wrote", TOOLS_PATH)
        else:
            print("skip", TOOLS_PATH, "(뒤 절이 함수를 더한 판 — 덮어쓰지 않음)")
        path = write_notebook(LAB, "04", SLUG, "experiment", cells())
        print("wrote", path)
