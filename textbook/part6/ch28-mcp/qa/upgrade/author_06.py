"""Ch 28 06절(챕터 끝 실습 절) 생성기 (QUALITY-UPGRADE.md §7-2·§2·§2-7·§3·§4·§6).

사용:
  python3 -B author_06.py                  → 노트북 + _src 본문을 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행). 도구 파일은 쓰지 않는다(05절 판 그대로)
  python3 -B author_06.py --src-only       → _src 본문만 다시 쓴다(노트북은 그대로)
  python3 -B author_06.py --tools-copy DIR → 디스크의 도구 파일 connect_tools.py를 DIR에 복사한다(새 커널 사본 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
새로 만든 절이라 qa/upgrade/before/ 에 원본이 없다. **experiment 형식**(chapter.json), lesson_part 없음.
슬러그 `06-MCP-실습`(규격 §7-2 `{NN+1}-{챕터 이름}-실습` — 챕터 제목 머리말 「MCP」, 인계 후보 · 선례 `09-DeepAgents-실습`).

## 결정 1 — 붙인 앞 절 기능 셋 (인계 「§05 → 실습(06)」 3·4항, 06-probe.md §0)

02절 서버에 도구 붙이기(runpy.run_path로 읽은 서버 객체에 @server.tool 둘 — 05절 4절 셀 글 그대로, 실행 2에서 에이전트에 실림) +
04절 에이전트 연결(MCPAdapter 메모리 연결 → create_agent + 호출 한도 3 → await ainvoke, 셈 「요청 수 = 도구를 요청한 응답 수 + 1」 — 두 실행 모두) +
05절 명세 글자 수(spec_length)·입력 토큰(usage_metadata — 요청마다, 두 실행을 견주는 잣대).
실행 1 = tool_count 1(served_tools[:1] — lookup_policy) · 실행 2 = tool_count 3(도구 셋) — 값 하나(인계 후보 (가)).
05절이 이미 보인 비교(첫 요청 187 ↔ 252 · 명세 252 ↔ 685)는 「05절 5절에서 본 값과 같음」으로만 쓰고, b2 「새로 볼 것」은
05절 b7이 재지 않았다고 적은 둘째 요청(도구를 부른 뒤의 요청)과 실행 전체의 합만(Ch 26 B-7 교훈).
뺀 것: 03 stdio·HTTP 전송과 접근 토큰(도구 수를 바꾸는 데 전송이 필요 없고, 서버를 띄우고 끄는 셀이 늘어 30분을 넘김) ·
04 손으로 만든 도구 호출 요청(ToolNode — 에이전트가 대신) · 05 직접 도구·설명을 늘린 도구(바꿀 값의 다른 후보 — 도구 수 하나만 바꿈) ·
01 기능 목록·판 번호(에이전트 흐름에 쓰이지 않음 — 메모리 연결만 이어 씀).

## 결정 2 — 흔들림 먼저 확인 (qa/upgrade/06-probe.md)

§0(22:29:56Z) → 첫 요청 22:30:05Z. 실행 1·2 회차마다 한 번씩 5회차, 요청 20번: 구조 값·모델 판단 값·요청마다 입력 토큰 모두 5/5
(두 실행 모두 첫 응답 lookup_policy → 둘째 응답 답 · 요청 2 · 입력 187·243 ↔ 252·308 · 늘어난 입력 토큰 65·65) → 입력 그대로.

## 결정 3 — 결론은 코드가 정하는 값 + 5/5·두 커널 같은 서비스 값(한정어와 함께)

명세 글자 수 252 ↔ 685 · 셈 · (5/5 + 두 커널이면) 요청마다 늘어난 입력 토큰. 모델 판단 값은 「이번 실행에서는」.
답 글·도구 인자·출력 토큰·예상 비용은 둘째 단락·b6 표·b7에만([[READ_…]] 자리 표시 — 생성기에 글자 그대로, mdpatch.py가 생성기까지 고침).
assert는 파일 찾기 셀(01 셀 글)과 키 셀뿐.

## 결정 4 — 도구 파일 (§2-7)

connect_tools.py 05절 판(570ed3cc…) 그대로 — 이 절이 쓰는 앞 절 함수 다섯(estimate_cost·names_of·spec_length·sum_usage·tool_call_names)이
모두 이미 있음. 노트북에 다시 적은 앞 절 셀은 서버 객체에 붙이는 도구 정의 둘(@server.tool — 서버 객체에 묶여 도구 파일로 옮길 수 없음)과
셀 글(FIND_FILE·LOAD·LIMIT)뿐. author_05.check_tools() 사슬(05 → 04 → 03)만 돌리고 도구 파일은 쓰지 않는다.
이 절이 처음 적은 함수: 조립 함수 async def run_agent(chosen_tools) · 요청마다 보기 show_requests(messages) · 셈 count_asked(messages)
(셋 다 노트북 전역 이름을 읽거나 이 절에서만 써서 노트북에 둠).

## 모델 요청

노트북 한 번 **4번**(실행 1 = 2 · 실행 2 = 2, 호출 한도 3 × 2 = 상한 6). 디스크 쓰기 0(메모리 연결 — 자식 프로세스 0).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`else`·`!=`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`range`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·대입 풀기·별표 풀기·
`while`·`try`·세미콜론·`isinstance`·`importlib`·클래스·`asyncio.run`·`tool_choice`. 데코레이터는 @server.tool 둘(05절 셀 글 — 그 함수 매개변수 단순 힌트).
호출 깊이 2 이하. 01~05 노트북·도구 파일에 없는 내장 이름·속성·키워드 인자·연산자·가져오기 0(/tmp/ch28-06/tools/inventory.py).
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(HERE))
import author_01  # noqa: E402  01절 셀 글(FIND_FILE)
import author_02  # noqa: E402  본문 도우미
import author_03  # noqa: E402  노트북 코드 셀 읽기
import author_04  # noqa: E402  04절 셀 글(LIMIT)
import author_05  # noqa: E402  05절 셀 글·도구 파일 05절 판과 대조 사슬(05 → 04 → 03)
from nbkit import RUN_DATE, code, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch28-mcp/notebooks"
FIGS = ROOT / "textbook/part6/ch28-mcp/figures"
SLUG = "06-MCP-실습"
TITLE_TEXT = "MCP 실습: 에이전트에 붙이는 MCP 도구를 하나에서 셋으로 늘리기"
SRC = ROOT / "textbook/part6/ch28-mcp/_src" / (SLUG + ".html")
NB04 = LAB / "04-LangChain-MCP-클라이언트-연동.ipynb"
NB05 = LAB / "05-도구-정의와-첫-호출-토큰.ipynb"
TOOLS_PATH = LAB / "connect_tools.py"
TOOLS_05_SHA = "570ed3cc607871a374ac1d5d7fc3ba6435908669ae79f48908535787d16f204c"
PROBE = HERE / "probe/probe06.py"
html_text = author_02.html_text
table_html = author_02.table_html


# ---------------------------------------------------------------- 도구 파일 (05절 판 그대로 — 쓰지 않음)
def check_tools() -> None:
    """05절까지의 대조 사슬을 돌리고, 디스크 도구 파일이 05절 판 그대로인지 봅니다(06절은 함수를 더하지 않음)."""
    author_05.check_tools()
    disk = TOOLS_PATH.read_text(encoding="utf-8")
    assert disk == author_05.TOOLS, "도구 파일이 05절 판과 다릅니다(06절은 도구 파일을 바꾸지 않습니다)"
    assert hashlib.sha256(disk.encode("utf-8")).hexdigest() == TOOLS_05_SHA, "도구 파일 해시가 05절 판과 다릅니다"


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = author_05.INSTALL

IMPORTS = r'''# 이 절에서 쓸 이름을 가져옵니다(langchain.mcp는 베타 경고 한 종류만 끄고 가져옵니다)
import runpy
import warnings
from langchain_core._api import LangChainBetaWarning
warnings.filterwarnings("ignore", category=LangChainBetaWarning)
from langchain.mcp import MCPAdapter
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
# 01절과 앞 챕터에서 배운 함수 다섯은 도구 파일에서 가져옵니다
from connect_tools import estimate_cost, names_of, spec_length, sum_usage, tool_call_names

print("도구 파일에서 가져온 함수:", "estimate_cost, names_of, spec_length, sum_usage, tool_call_names")'''

FIND_FILE = author_01.FIND_FILE
LOAD = author_05.LOAD
DEF_SEARCH = author_05.DEF_SEARCH
DEF_SHOW = author_05.DEF_SHOW
LIMIT = author_04.LIMIT

SERVED = r'''# 도구 셋이 붙은 서버 객체를 메모리 연결로 MCPAdapter에 넘겨, LangChain 도구 목록으로 받습니다(05절 4절)
practice_adapter = MCPAdapter(server)
served_tools = await practice_adapter.list_tools()
print("서버가 알린 도구:", names_of(served_tools))
print("받은 도구 수:", len(served_tools))'''

TEXTS = r'''# 두 실행에 같게 쓸 시스템 메시지 글과 질문을 정합니다(04절 5절과 같은 글)
agent_rule = "교육센터 자료실 규정 질문에는 도구로 규정을 찾아, 찾은 글만 근거로 한국어 한 문장으로 답하세요."
question = "교육센터 자료실은 토요일에 몇 시까지 운영하나요?"
print("시스템 메시지 글:", agent_rule)
print("질문:", question)
print("두 글의 출처: 04절 5절 에이전트에 준 글(실행 전에 정함)")'''

DEF_RUN = r'''# 에이전트에 붙일 도구 목록을 받아 에이전트를 만들고, 질문 한 줄로 한 번 실행해 결과 메시지를 내놓습니다(04절 5절)
async def run_agent(chosen_tools):
    agent = create_agent(model, tools=chosen_tools, system_prompt=agent_rule, middleware=[call_limit])
    first_input = {"messages": [HumanMessage(content=question)]}
    result = await agent.ainvoke(first_input)
    return result["messages"]'''

DEF_SHOW_REQ = r'''# 결과 메시지에서 모델 응답마다 도구 호출 요청과 입력 토큰을 한 줄씩 출력하고, 입력 토큰 목록을 내놓습니다
def show_requests(messages):
    input_list = []
    for message in messages:
        if type(message).__name__ == "AIMessage":
            tokens = message.usage_metadata["input_tokens"]
            input_list.append(tokens)
            print("요청", len(input_list), "| 도구 호출 요청:", tool_call_names(message), "| 입력 토큰:", tokens)
    return input_list'''

DEF_COUNT = r'''# 결과 메시지에서 도구 호출 요청이 하나라도 있는 모델 응답의 수를 세어 내놓습니다
def count_asked(messages):
    asked = 0
    for message in messages:
        if type(message).__name__ == "AIMessage":
            if len(tool_call_names(message)) > 0:
                asked = asked + 1
    return asked'''

CHOOSE1 = r'''# 실행 1: 서버가 알린 도구 셋 가운데 목록 앞에서 하나만 골라, 이름과 명세 글자 수를 봅니다
tool_count = 1
first_tools = served_tools[:tool_count]
print("붙일 도구:", names_of(first_tools))
print("명세 글자 수:", spec_length(first_tools))'''

RUN1 = r'''# 실행 1의 에이전트를 만들어 한 번 실행하고, 결과 메시지 수와 마지막 답 글을 봅니다
first_messages = await run_agent(first_tools)
print("결과 메시지 수:", len(first_messages))
print("마지막 답 글:")
print(first_messages[-1].text)'''

SHOW1 = r'''# 실행 1의 모델 응답마다 도구 호출 요청과 입력 토큰을 보고, 입력 토큰 목록을 받습니다
print("실행 1의 요청:")
first_inputs = show_requests(first_messages)'''

CHECK1 = r'''# 실행 1에서 도구를 요청한 응답 수와 모델 요청 수(Ch 19 05절 함수 sum_usage)를 견줍니다
first_usage = sum_usage(first_messages)
first_asked = count_asked(first_messages)
print("도구를 요청한 응답 수:", first_asked)
print("모델 요청 수:", first_usage["requests"])
print("모델 요청 수 = 도구를 요청한 응답 수 + 1:", first_usage["requests"] == first_asked + 1)'''

CHOOSE2 = r'''# 실행 2: 값 하나만 바꿉니다. 붙이는 도구 수를 3으로 해 도구 셋을 모두 고르고, 이름과 명세 글자 수를 봅니다
tool_count = 3
second_tools = served_tools[:tool_count]
print("붙일 도구:", names_of(second_tools))
print("명세 글자 수:", spec_length(second_tools))'''

RUN2 = r'''# 실행 2의 에이전트를 만들어 한 번 실행하고, 결과 메시지 수와 마지막 답 글을 봅니다
second_messages = await run_agent(second_tools)
print("결과 메시지 수:", len(second_messages))
print("마지막 답 글:")
print(second_messages[-1].text)'''

SHOW2 = r'''# 실행 2의 모델 응답마다 도구 호출 요청과 입력 토큰을 보고, 입력 토큰 목록을 받습니다
print("실행 2의 요청:")
second_inputs = show_requests(second_messages)'''

CHECK2 = r'''# 실행 2에서 도구를 요청한 응답 수와 모델 요청 수를 견줍니다
second_usage = sum_usage(second_messages)
second_asked = count_asked(second_messages)
print("도구를 요청한 응답 수:", second_asked)
print("모델 요청 수:", second_usage["requests"])
print("모델 요청 수 = 도구를 요청한 응답 수 + 1:", second_usage["requests"] == second_asked + 1)'''

COMPARE = r'''# 두 실행의 요청 수가 같으면, 같은 번호의 요청끼리 입력 토큰이 얼마나 늘었는지 봅니다
same_count = len(first_inputs) == len(second_inputs)
print("두 실행의 요청 수가 같은가:", same_count)
if same_count:
    position = 0
    for tokens in first_inputs:
        later = second_inputs[position]
        position = position + 1
        print("요청", position, "| 도구 하나:", tokens, "| 도구 셋:", later, "| 늘어난 입력 토큰:", later - tokens)'''

TOTAL = r'''# 두 실행의 입력·출력 토큰 합과, 2026-09-17 요금표(100만 토큰당 달러)로 어림한 예상 비용을 봅니다(Ch 6 06절 함수 estimate_cost)
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
first_cost = round(estimate_cost(first_usage, input_rate, cached_input_rate, output_rate), 6)
second_cost = round(estimate_cost(second_usage, input_rate, cached_input_rate, output_rate), 6)
print("실행 1 | 입력 토큰 합:", first_usage["input_tokens"], "| 출력 토큰 합:", first_usage["output_tokens"], "| 예상 비용(달러):", first_cost)
print("실행 2 | 입력 토큰 합:", second_usage["input_tokens"], "| 출력 토큰 합:", second_usage["output_tokens"], "| 예상 비용(달러):", second_cost)
print("입력 토큰 합의 차:", second_usage["input_tokens"] - first_usage["input_tokens"])'''


def check_same_as_prev() -> None:
    """앞 절 셀과 같은 글이라고 적는 셀이 디스크 노트북 셀과 글자 그대로 같은지 봅니다."""
    sources_04 = author_03.notebook_code_sources(NB04)
    sources_05 = author_03.notebook_code_sources(NB05)
    # 파일 위치 셀은 01절 셀 글(05절에도 같은 글), 서버 읽기·도구 둘은 05절 3·4절 셀 글, 호출 한도는 04절 5절 셀 글
    assert FIND_FILE in sources_05, "FIND_FILE이 05 노트북 셀과 다릅니다"
    assert FIND_FILE in (HERE / "author_01.py").read_text(encoding="utf-8"), "FIND_FILE이 01절 셀과 다릅니다"
    for cell in [LOAD, DEF_SEARCH, DEF_SHOW]:
        assert cell in sources_05, cell.splitlines()[0]
    assert LIMIT in sources_04, "LIMIT이 04 노트북 셀과 다릅니다"
    # 시스템 메시지 글·질문은 04절 5절 셀과 같은 글입니다
    joined_04 = "\n".join(sources_04)
    for line in TEXTS.splitlines()[1:3]:
        assert line in joined_04, line
    # 설치 셀은 05절과 같은 여섯 판입니다
    assert INSTALL in sources_05, "INSTALL이 05 노트북 셀과 다릅니다"


def check_same_as_probe() -> None:
    """노트북 셀의 서버·도구·한도·글·조립 함수·셈 함수·모델 줄이 흔들림 확인 스크립트(probe06.py)에 같은 글로 있는지 봅니다."""
    probe = PROBE.read_text(encoding="utf-8")
    for cell in [LOAD, DEF_SEARCH, DEF_SHOW, LIMIT, TEXTS, DEF_RUN, DEF_COUNT]:
        for line in cell.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("print(") or stripped == "":
                continue
            assert stripped in probe, stripped
    for piece in ['"openai:gpt-5.4-mini",', "temperature=0,", 'reasoning_effort="none",',
                  'warnings.filterwarnings("ignore", category=LangChainBetaWarning)',
                  "practice_adapter = MCPAdapter(server)", "served_tools = await practice_adapter.list_tools()",
                  'for run_name, tool_count in [("run1", 1), ("run2", 3)]:', "chosen_tools = served_tools[:tool_count]",
                  "messages = await run_agent(chosen_tools)",
                  "from connect_tools import estimate_cost, names_of, spec_length, sum_usage, tool_call_names"]:
        assert piece in probe, piece


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/06-figures.md)
FIG1 = "06-1-도구-셋-서버와-에이전트-조립"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 초록 상자 서버 객체 server 서버 파일 도구 lookup_policy + @server.tool 둘에서 파란 상자 MCPAdapter list_tools 메모리 연결, 노란 상자 서버가 알린 도구 셋 lookup_policy · search_topics · show_topics, 파란 상자 바꾸는 값 tool_count 실행 1은 1 · 실행 2는 3으로 화살표가 이어집니다. 그 파란 상자에서 점선이 노란 상자 spec_length 명세 글자 수 252 · 685로 가고, 화살표는 파란 상자 run_agent create_agent · 호출 한도 3 await ainvoke 질문 한 줄을 지나 파란 상자 show_requests · count_asked 요청마다 입력 토큰 · 셈으로 가는 그림"
FIG1_CAP = "서버 객체에 붙인 도구 셋을 MCPAdapter로 받고, 에이전트에 붙일 도구 수 하나만 1과 3으로 바꿔 두 실행을 조립했습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 서버 객체이고, 파란 상자는 우리가 부른 클래스 MCPAdapter와 바꾸는 값, 이 노트북에 적은 함수입니다.
노란 상자는 노트북 2·5·6절 출력으로 확인한 값입니다.
점선은 바꾸는 값에 따라 달라지는 명세 글자 수로 가는 갈래입니다.
모델은 함수 run_agent 안에서만 부르고, 이 그림에는 모델 상자를 두지 않았습니다."""

FIG2 = "06-2-실행-1의-실제-순서"
FIG2_ALT = "세로선 넷이 있는 차례 그림입니다. 왼쪽부터 우리 코드 run_agent, 에이전트 그래프, 연보라 띠 안의 모델 gpt-5.4-mini, MCP 서버 메모리 연결입니다. 우리 코드에서 await ainvoke 질문 한 줄 화살표가 그래프로 가고, 요청 1 입력 토큰 187 화살표가 모델로 가고 도구 요청 lookup_policy 점선이 돌아옵니다. 그래프에서 도구 실행 노드가 부름 화살표가 서버로 가고 도구 메시지 점선이 돌아옵니다. 요청 2 입력 토큰 243 화살표가 모델로 가고 도구 요청 없음 점선이 돌아온 뒤, 결과 메시지 넷 점선이 우리 코드로 돌아옵니다. 맨 아래 우리 코드와 그래프에 걸친 노란 메모에 요청 수 2 = 도구를 요청한 응답 수 1 + 1이 적힌 그림"
FIG2_CAP = "흔들림 확인 다섯 번과 두 커널에서 모두, 도구를 한 번 부른 실행 1의 요청은 2번이었고 입력 토큰은 187과 243이었습니다."
FIG2_READ = "위에서 아래로 실행 차례대로 읽고, 세로선은 왼쪽부터 우리 코드, 그래프, 모델, 서버입니다. 연보라 띠는 실제로 부른 모델 gpt-5.4-mini의 자리이고, 실선은 부르는 쪽, 점선은 돌아오는 쪽입니다. 요청 옆의 입력 토큰과 맨 아래 노란 메모는 노트북 5절 출력입니다. 도구 메시지의 결과 상태는 이 노트북에서 출력하지 않았고, 서버는 같은 커널 안의 메모리 연결입니다. 요청의 차례와 입력 토큰은 흔들림 확인 다섯 번과 두 커널에서 같았을 때만 그렸습니다."

FIG3 = "06-3-도구-하나와-셋의-요청마다-입력-토큰"
FIG3_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 회색 상자 두 실행에 같게 둔 것 서버 · 질문 시스템 메시지 글 호출 한도 3 · run_agent에서 점선 둘이 나란한 파란 상자 둘로 갑니다. 왼쪽 실행 1 tool_count 1 명세 252자 아래에 노란 상자 요청 1 입력 토큰 187 요청 2 입력 토큰 243 합 430이 있습니다. 오른쪽 실행 2 tool_count 3 명세 685자 아래에 노란 상자 요청 1 입력 토큰 252 요청 2 입력 토큰 308 합 560이 있습니다. 두 노란 상자는 맨 아래 노란 상자 요청마다 늘어난 입력 토큰 요청 1 65 · 요청 2 65 합의 차 130으로 모이는 그림"
FIG3_CAP = "흔들림 확인 다섯 번과 두 커널에서 모두, 도구를 셋 붙인 실행은 첫 요청과 둘째 요청에서 입력 토큰이 65씩 많았습니다."
FIG3_READ = "맨 위 회색 상자는 두 실행에 같게 둔 조건입니다. 왼쪽 칸이 실행 1, 오른쪽 칸이 실행 2이고, 파란 상자가 바꾼 값 tool_count입니다. 노란 상자는 노트북 5·6·7절 출력이고, 칸 안은 위에서 아래로 실행 차례입니다. 맨 아래 상자는 같은 번호의 요청끼리 뺀 차와, 두 실행의 입력 토큰 합의 차입니다. 입력 토큰은 흔들림 확인 다섯 번과 두 커널에서 같았을 때만 넣었습니다."

ILLU = "06-4-받침대에-꽂은-통-하나와-셋"
ILLU_ALT = "흰 바탕에 오른쪽의 연회색 네모 격납고와, 왼쪽의 흰 네모 받침대 둘이 있는 그림입니다. 격납고 앞면은 크게 열려 있고 안은 어둡게 비어 있으며, 지붕에는 마디가 있는 회색 로봇 팔 하나가 있습니다. 두 받침대는 같은 모양이고, 윗면에 동그란 자리가 셋씩 한 줄로 파여 있습니다. 왼쪽 받침대에는 구리색 육각 통 하나가 맨 왼쪽 자리에 꽂혀 있고, 나머지 두 자리는 비어 있습니다. 오른쪽 받침대에는 같은 통 둘이 왼쪽과 가운데 자리에 꽂혀 있고, 로봇 팔 끝의 집게가 셋째 통을 집어 빈 오른쪽 자리 위에 들고 있습니다. 사람·글자·숫자·화살표·별은 없는 그림"
ILLU_CAP = "같은 받침대 둘 가운데 왼쪽에는 통이 하나 꽂혔고, 오른쪽에는 로봇 팔이 셋째 통을 꽂는 중입니다."
ILLU_READ = "오른쪽 격납고 지붕의 로봇 팔이 집게로 통 하나를 집어, 오른쪽 받침대의 빈 오른쪽 자리 위에 들고 있습니다. 오른쪽 받침대에는 통 둘이 이미 꽂혀 있고, 왼쪽 받침대에는 통이 하나만 꽂혀 두 자리가 비어 있습니다. 격납고가 MCP 서버, 로봇 팔이 조립 함수 <code>run_agent</code>, 받침대에 꽂힌 통이 에이전트에 붙인 도구입니다. 왼쪽 받침대가 도구 하나를 붙인 실행 1, 오른쪽 받침대가 도구 셋을 붙이는 실행 2입니다. 그림에는 교신하는 장면이 없고, 격납고의 문 모양과 통의 색은 어떤 값과도 짝짓지 않습니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 앞 절에서 배운 서버에 도구 붙이기·에이전트 연결·입력 토큰 세기를 한 흐름에 모읍니다.
2. 서버가 알린 도구 셋 가운데 하나를 붙인 실행 1과, 셋을 모두 붙인 실행 2를 차례로 실행합니다.
3. 두 실행의 입력 토큰을 요청마다 견주어, 붙인 도구의 명세가 어느 요청에 실리는지 봅니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 실행 1과 실행 2에서 에이전트를 한 번씩 실행합니다.
노트북 밖에서 두 실행을 다섯 번씩 보냈을 때, 요청은 열 번 모두 실행마다 2번이었습니다.
그래서 이 노트북의 모델 요청은 모두 4번으로 어림합니다.
호출 한도 3을 붙여, 한 실행의 요청이 3번을 넘지 않게 막습니다.

요금표로 어림한 예상 비용은 두 실행을 합쳐 0.002달러 아래이고, 청구 금액이 아닙니다.
서버는 서버 파일 `course_server.py`를 이 커널에서 읽어 메모리 연결로 붙입니다.
자식 프로세스는 띄우지 않고, 노트북이 쓰는 파일도 없습니다.
모델이 쓰는 도구 인자와 답 글은 실행마다 달라질 수 있고, 걸린 시간은 재지 않았습니다.
앞에서 배운 함수 다섯은 도구 파일 `connect_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 여섯을 설치합니다.
판은 langchain 1.4.0, langchain-core 1.6.2, langchain-openai 1.6.0입니다.
패키지 fastmcp 4.0.3, mcp 2.2.0, python-dotenv 1.2.3도 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**실습 범위** — 이 절은 이 챕터의 실습이고, 30분 안팎입니다.
따로 내는 과제는 없고, 강사와 함께 첫 셀부터 차례로 실행합니다.

실습 폴더 `labs/part6/ch28-mcp`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def model_cells() -> list[dict]:
    """과정 표준 키·모델 셀(nbkit)에 이 절의 결과 읽기(실행일·요청은 5·6절 실행 셀에서만)와 2절 첫 설명을 붙입니다."""
    cells = key_and_model_cells("openai:gpt-5.4-mini")
    cells[-1] = md("""**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.
모델 요청은 5절과 6절의 실행 셀에서만 나갑니다.

## 2. 재료: 도구 셋을 알리는 서버

실습에 쓸 서버는 05절 4절에서 만든 도구 셋 서버와 같습니다.
서버 파일을 이 커널에서 읽고, 그 서버 객체에 도구 둘을 더 붙입니다.
먼저 01절 2절과 같은 셀로 서버 파일의 위치를 찾습니다.""")
    return cells


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이 절은 Ch 28의 실습입니다.
01~05절에서 하나씩 본 기능 가운데 셋을, 자료실 규정에 답하는 에이전트 하나에 모읍니다.
02절의 서버에 도구 붙이기, 04절의 에이전트 연결, 05절의 명세 글자 수와 입력 토큰 세기입니다.
그다음 에이전트에 붙이는 도구 수 하나만 바꿔 두 번 실행하고, 두 결과를 견줍니다.

첫 셀은 패키지 여섯을 설치하고 설치된 판 번호를 출력합니다.
05절과 같은 여섯이고, 04절의 langgraph와 psutil은 쓰지 않아 설치하지 않습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langchain: 1.4.0`, `langchain-core: 1.6.2`, `fastmcp: 4.0.3`이 보입니다.
여섯 판 모두 실습 폴더 잠금과 같습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
04절처럼 모듈 `langchain.mcp`는 베타 경고 한 종류만 끄고 가져옵니다.
마지막 가져오기 줄은 앞에서 배운 함수 다섯을 도구 파일 `connect_tools.py`에서 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: estimate_cost, names_of, spec_length, sum_usage, tool_call_names`가 보입니다.
함수 `names_of`는 01절 4절에서, 함수 `spec_length`는 Ch 19 03절에서 배웠습니다.
함수 `tool_call_names`와 `sum_usage`는 Ch 19 04·05절, `estimate_cost`는 Ch 6 06절에서 배웠습니다.
다섯 모두 04·05절에서 가져온 이름이고, 이 절에서 새로 배우는 이름은 없습니다.

앞에서 배운 함수는 `connect_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다."""),
    ] + model_cells() + [
        code(FIND_FILE),
        md("""**결과 읽기** — 출력 줄 `서버 파일을 찾았는가: True`가 보입니다.
교재 출력은 프로젝트 맨 위에서 실행해 셋째 후보 `labs/part6/ch28-mcp/course_server.py`를 골랐습니다.
`notebooks/` 폴더에서 열면 첫 후보 `../course_server.py`가 골라집니다.

다음 셀은 05절 3절과 같은 셀로, 서버 파일을 실행해 서버 객체와 규정 딕셔너리를 받습니다."""),
        code(LOAD),
        md("""**결과 읽기** — 출력 줄 `서버 이름: 교육센터 자료실`과 `규정 주제: ['대출', '운영', '연체']`가 보입니다.
변수 `server`는 서버 파일이 만든 서버 객체이고, 변수 `policies`는 규정 딕셔너리입니다.
파일을 실행해 이름을 받았을 뿐이라, 서버 파일은 그대로입니다.

다음 셀은 05절 4절과 같은 셀로, 규정 글에서 낱말이 든 주제어를 찾는 도구를 서버 객체에 붙입니다.
셀의 `@server.tool` 줄은 02절처럼 아래 함수를 서버 객체 `server`의 도구로 등록합니다."""),
        code(DEF_SEARCH),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
몸통은 규정 딕셔너리의 주제어를 차례로 보며, 규정 글에 낱말이 든 주제어를 모읍니다.
이 도구는 커널 안의 서버 객체에만 붙고, 서버 파일은 고치지 않습니다.

다음 셀도 05절 4절과 같은 셀로, 인자가 없는 도구 하나를 같은 서버 객체에 더 붙입니다."""),
        code(DEF_SHOW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
몸통은 규정 딕셔너리의 주제어를 목록으로 내놓습니다.
이제 서버 객체에는 서버 파일의 `lookup_policy`까지 도구 셋이 붙었습니다.

다음 셀은 이 서버 객체를 05절 4절처럼 메모리 연결로 클래스 `MCPAdapter`에 넘겨 도구를 받습니다."""),
        code(SERVED),
        md("""**결과 읽기** — 출력 줄 `서버가 알린 도구: ['lookup_policy', 'search_topics', 'show_topics']`와 `받은 도구 수: 3`이 보입니다.
목록 맨 앞이 `lookup_policy`라서, 실행 1은 목록 앞에서 하나만 골라 이 도구를 붙입니다.
메모리 연결이라 자식 프로세스는 띄우지 않았습니다.
도구를 부를 때에도 이 커널 안의 서버 객체가 도구를 실행합니다.

## 3. 조립하기

조립에는 04절의 에이전트 연결을 씁니다.
Ch 26·27처럼 모델을 부르는 에이전트에는 Ch 22 04절의 호출 한도를 함께 붙입니다.
다음 셀은 04절 5절과 같은 셀로, invoke 한 번에 모델 요청을 3번까지만 허락하는 호출 한도를 만듭니다."""),
        code(LIMIT),
        md("""**결과 읽기** — 출력 줄 `한 번 실행의 요청 한도: 3`과 `한도에 닿으면: end`가 보입니다.
04절에서 본 것처럼, 이 한도는 `ainvoke`로 실행해도 실행 한 번마다 셉니다.
두 실행의 에이전트가 이 객체 하나를 함께 씁니다.

다음 셀은 두 실행에 같게 쓸 시스템 메시지 글과 질문을 정합니다.
04절 5절의 에이전트에 준 글과 같은 글입니다."""),
        code(TEXTS),
        md("""**결과 읽기** — 라벨 `시스템 메시지 글:`과 `질문:` 뒤에 두 글이 보입니다.
라벨 `두 글의 출처:` 뒤에는 두 글을 가져온 곳이 보입니다.
시스템 메시지 글은 규정 질문에 도구로 규정을 찾고, 찾은 글만 근거로 답하라고 정합니다.
질문은 서버 파일의 운영 규정으로 답할 수 있는 질문입니다.
두 글은 실행 전에 정했고, 결과를 보고 바꾸지 않았습니다.

다음 셀은 에이전트에 붙일 도구 목록 하나를 받아, 에이전트를 만들고 한 번 실행하는 조립 함수입니다.
04절 5절의 에이전트 셀과 실행 셀을 한 함수로 모았습니다.
함수 안에서 `await`를 쓰므로, 02절 2절처럼 정의 줄을 `async def`로 씁니다."""),
        code(DEF_RUN),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
모델·시스템 메시지 글·호출 한도·질문은 앞 셀에서 만든 이름을 그대로 씁니다.
그래서 두 실행 사이에 달라지는 것은 인자로 넘기는 도구 목록 하나뿐입니다.
에이전트의 도구가 비동기로만 불리므로, 04절처럼 `ainvoke`로 실행합니다.

## 4. 결과를 볼 함수

두 실행을 같은 잣대로 보려고, 결과 메시지에서 볼 값을 출력하는 함수 둘을 먼저 적습니다.
첫째 함수 `show_requests`는 모델 응답(`AIMessage`)마다 한 줄씩 출력합니다.
한 줄에는 요청 번호, 그 응답의 도구 호출 요청, 그 요청의 입력 토큰이 들어갑니다.
입력 토큰은 05절처럼 응답의 속성 `usage_metadata`에서 읽습니다."""),
        code(DEF_SHOW_REQ),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
모델 응답 하나는 모델 요청 하나의 결과라, 응답마다 한 줄이 요청마다 한 줄입니다.
요청 번호는 지금까지 모은 입력 토큰의 개수라, 첫 응답이 요청 1, 둘째 응답이 요청 2가 됩니다.
함수가 내놓는 입력 토큰 목록은 7절에서 두 실행을 요청마다 견줄 때 씁니다.

둘째 함수 `count_asked`는 도구를 요청한 응답 수를 셉니다.
04절 5절에서 셈 「요청 수 = 도구를 요청한 응답 수 + 1」을 확인한 셀의 반복문을 함수로 옮긴 모양입니다."""),
        code(DEF_COUNT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
모델 요청 수는 Ch 19 05절 함수 `sum_usage`가 모델 응답 수로 셉니다.
두 수를 견주면, 한 실행이 셈대로 끝났는지 볼 수 있습니다.

## 5. 실행 1: 도구 하나를 붙인 에이전트

이제 실행 1을 합니다.
서버가 알린 도구 셋 가운데, 목록 앞에서 하나만 골라 에이전트에 붙입니다.
05절 4절처럼 슬라이싱 `[:tool_count]`로 목록 앞에서부터 고릅니다.
붙인 도구의 명세 글자 수도 Ch 19 03절 함수 `spec_length`로 셉니다."""),
        code(CHOOSE1),
        md("""**결과 읽기** — 출력 줄 `붙일 도구: ['lookup_policy']`와 `명세 글자 수: 252`가 보입니다.
05절 2절에서 센 서버 파일 도구의 명세 글자 수와 같습니다.
메모리 연결로 받아도 같은 도구는 같은 명세라는 것을 05절 4절에서 보았습니다.

다음 셀은 이 도구 하나로 실행 1의 에이전트를 만들어 한 번 실행합니다.
실행 전에 예상해 봅니다.
04절 5절과 같은 질문이라면, 모델은 도구를 몇 번 부르고 요청은 몇 번일까요?"""),
        code(RUN1),
        md("""**결과 읽기** — 라벨 `결과 메시지 수:` 뒤에 결과 메시지의 수가 보입니다.
라벨 줄 `마지막 답 글:` 아래는 모델이 쓴 답입니다.
결과 메시지 수는 모델이 도구를 몇 번 부르느냐에 따라 달라질 수 있습니다.

이번 실행에서는 `결과 메시지 수: 4`였고, 답 글은 `토요일은 17:00까지 운영합니다.`였습니다.
새 커널 두 번과 노트북 밖 다섯 번에서도 결과 메시지는 넷이었습니다.
노트북 밖 다섯 번의 답 글은 모두 「교육센터 자료실은」으로 시작하는 다른 문장이었습니다.
답 글은 모델이 쓴 글이라 실행마다 달라질 수 있어, 결론에 쓰지 않습니다.

다음 셀은 함수 `show_requests`로 실행 1의 모델 응답을 요청마다 봅니다."""),
        code(SHOW1),
        md("""**결과 읽기** — 라벨 줄 `실행 1의 요청:` 아래가 실행 1의 요청마다 한 줄입니다.
줄마다 요청 번호, 그 응답의 도구 호출 요청, 그 요청의 입력 토큰이 차례로 보입니다.

이번 실행에서는 요청 1의 응답이 `lookup_policy`를 요청했고, 요청 2의 응답은 도구 요청 없이 답했습니다.
입력 토큰은 요청 1이 187, 요청 2가 243이었습니다.
요청 1의 187은 05절 5절에서 MCP 도구 하나를 알린 첫 요청과 같은 값입니다.
요청 2에는 모델의 도구 호출 요청과 도구 메시지가 더 실려, 입력 토큰이 늘었습니다.
도구 차례와 입력 토큰은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.

다음 셀은 도구를 요청한 응답 수와 모델 요청 수를 견줍니다."""),
        code(CHECK1),
        md("""**결과 읽기** — 라벨 `도구를 요청한 응답 수:`와 `모델 요청 수:` 뒤에 두 수가 보입니다.
마지막 줄은 04절에서 확인한 셈이 이번 실행에서도 맞는지 보여 줍니다.
셈은 호출 한도에 닿지 않고 답으로 끝난 실행에서 맞습니다.

이번 실행에서는 `도구를 요청한 응답 수: 1`, `모델 요청 수: 2`였고, 셈이 `True`였습니다.
요청 2번은 호출 한도 3 안에 들었습니다.
노트북 밖 다섯 번과 새 커널 두 번에서도 같았습니다.

## 6. 실행 2: 도구 셋을 붙인 에이전트

실행 2는 값 하나만 바꿉니다.
에이전트에 붙이는 도구 수 `tool_count`를 1에서 3으로 바꿔, 서버가 알린 도구 셋을 모두 붙입니다.
서버·질문·시스템 메시지 글·호출 한도·조립 함수는 실행 1과 같습니다."""),
        code(CHOOSE2),
        md("""**결과 읽기** — 출력 줄 `붙일 도구: ['lookup_policy', 'search_topics', 'show_topics']`와 `명세 글자 수: 685`가 보입니다.
05절 4절에서 도구 셋의 명세 글자 수를 셀 때와 같은 값입니다.
명세 글자 수는 코드가 정하는 값이라, 다시 실행해도 같습니다.

다음 셀은 이 도구 셋으로 실행 2의 에이전트를 만들어 한 번 실행합니다.
실행 전에 예상해 봅니다.
질문은 운영 규정으로 답할 수 있으니, 모델은 여전히 `lookup_policy`를 부를까요?
도구를 부른 뒤의 둘째 요청은 실행 1과 같은 입력 토큰일까요, 아니면 늘어날까요?"""),
        code(RUN2),
        md("""**결과 읽기** — 라벨 `결과 메시지 수:` 뒤에 결과 메시지의 수가 보입니다.
라벨 줄 `마지막 답 글:` 아래는 모델이 쓴 답입니다.

이번 실행에서도 `결과 메시지 수: 4`였고, 답 글은 실행 1과 같은 `토요일은 17:00까지 운영합니다.`였습니다.
결과 메시지 수는 노트북 밖 다섯 번과 새 커널 두 번에서도 넷이었습니다.
답 글은 모델이 쓴 글이라, 두 실행의 답 글이 늘 같다고는 읽지 않습니다.

다음 셀은 함수 `show_requests`로 실행 2의 모델 응답을 요청마다 봅니다."""),
        code(SHOW2),
        md("""**결과 읽기** — 라벨 줄 `실행 2의 요청:` 아래가 실행 2의 요청마다 한 줄입니다.
실행 1의 줄과 요청 번호마다 견주어 봅니다.

이번 실행에서도 요청 1의 응답이 `lookup_policy`를 요청했고, 요청 2의 응답은 도구 요청 없이 답했습니다.
붙인 도구가 셋이어도, 모델은 운영 규정 도구 하나만 불렀습니다.
입력 토큰은 요청 1이 252, 요청 2가 308이었습니다.
요청 1의 252는 05절 5절에서 MCP 도구 셋을 알린 첫 요청과 같은 값입니다.
도구 차례와 입력 토큰은 노트북 밖 다섯 번과 새 커널 두 번에서 모두 같았습니다.

다음 셀은 실행 2에서도 셈이 맞는지 봅니다."""),
        code(CHECK2),
        md("""**결과 읽기** — 라벨 `도구를 요청한 응답 수:`와 `모델 요청 수:` 뒤에 두 수가 보입니다.
마지막 줄로 실행 2도 셈대로 끝났는지 봅니다.

이번 실행에서도 `도구를 요청한 응답 수: 1`, `모델 요청 수: 2`였고, 셈이 `True`였습니다.
도구를 셋 붙여도 요청 수는 실행 1과 같았습니다.
노트북 밖 다섯 번과 새 커널 두 번에서도 같았습니다.

## 7. 두 실행 견주기

마지막으로 두 실행의 입력 토큰을 요청마다 견줍니다.
두 실행의 요청 수가 같을 때만, 같은 번호의 요청끼리 입력 토큰의 차를 셉니다.
요청 수가 다르면 같은 번호라도 실린 메시지가 달라, 이 셀은 차를 출력하지 않습니다."""),
        code(COMPARE),
        md("""**결과 읽기** — 라벨 `두 실행의 요청 수가 같은가:` 뒤의 값을 먼저 봅니다.
그 값이 참이면, 아래 줄마다 요청 번호와 두 실행의 입력 토큰, 그 차가 보입니다.

이번 실행에서는 `두 실행의 요청 수가 같은가: True`였고, 두 요청 모두 `늘어난 입력 토큰: 65`였습니다.
요청 1은 187에서 252로, 요청 2는 243에서 308로 늘었습니다.
흔들림 확인 다섯 번과 두 커널에서 모두, 두 요청의 늘어난 입력 토큰은 65로 같았습니다.
도구를 부른 뒤의 둘째 요청에도, 붙인 도구 셋의 명세가 첫 요청과 같은 만큼 실린 셈입니다.
노트북 밖 기록에서는 두 실행의 도구 인자와 도구 메시지 글도 같았습니다.

마지막 셀은 두 실행의 토큰 합과 예상 비용을 봅니다.
요금은 Ch 6 06절처럼 2026-09-17 요금표의 100만 토큰당 달러입니다."""),
        code(TOTAL),
        md("""**결과 읽기** — 줄마다 한 실행의 입력·출력 토큰 합과, 라벨 `예상 비용(달러):` 뒤의 어림값이 보입니다.
마지막 줄은 두 실행의 입력 토큰 합의 차입니다.
함수 `sum_usage`가 낸 딕셔너리에는 할인되는 입력 토큰 칸이 없어, 입력 토큰을 모두 입력 요금으로 셌습니다.
예상 비용은 요금표로 어림한 값이고, 청구 금액이 아닙니다.

이번 실행에서는 입력 토큰 합이 실행 1 430, 실행 2 560이라, 차가 `입력 토큰 합의 차: 130`이었습니다.
130은 요청마다 늘어난 65가 요청 수 2만큼 더해진 값입니다.
출력 토큰 합은 두 실행 모두 32였고, 예상 비용은 0.000467달러와 0.000564달러였습니다.
노트북 밖 다섯 번에서 실행 1의 출력 토큰 합은 37로, 이 노트북과 달랐습니다.
출력 토큰과 비용은 모델이 쓴 글에 따라 달라지는 값이라 결론에 쓰지 않습니다.

## 정리

1. 02절 서버에 도구 붙이기, 04절 에이전트 연결, 05절 명세 글자 수와 입력 토큰 세기를 에이전트 하나에 모았습니다.
2. 붙인 도구를 하나에서 셋으로 바꾸자 명세 글자 수가 252에서 685가 되었고, 두 실행 모두 셈대로 요청이 끝났습니다.
3. 흔들림 확인 다섯 번과 두 커널에서 모두, 도구 셋을 붙인 실행은 첫 요청과 둘째 요청에서 입력 토큰이 65씩 많았습니다.

이 절로 Ch 28이 끝납니다.
Ch 29에서는 에이전트를 평가하는 방법을 배웁니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
def mermaid_block(name: str, alt: str, caption: str, reading: str) -> str:
    """.mmd와 글이 있을 때만 본문에 넣습니다(새 커널 A·B를 그림보다 먼저 돌릴 때 빌드가 멈추지 않게)."""
    if not (FIGS / (name + ".mmd")).is_file() or reading.startswith("[["):
        return ""
    return ("{{mermaid:" + name + "|" + alt + "|" + caption + "}}\n"
            + '<p class="look"><b>도식 읽기</b> — ' + html_text(reading) + "</p>\n")


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or ILLU_READ.startswith("[["):
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


def link(url: str, label: str) -> str:
    return '<a href="' + url + '">' + label + "</a>"


L_CH06_06 = "../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html"
L_CH19_03 = "../../part5/ch19-model-tools/03-좋은-도구-이름과-설명.html"
L_CH19_04 = "../../part5/ch19-model-tools/04-설명만으로-도구-선택하기.html"
L_CH19_05 = "../../part5/ch19-model-tools/05-bind_tools와-병렬-호출.html"
L_CH22_04 = "../ch22-middleware/04-호출-한도와-재시도-폴백.html"
L_CH29_01 = "../ch29-agent-evaluation/01-에이전트-평가-세-전략.html"
L_01 = "01-MCP-구조와-capability-협상.html"
L_02 = "02-FastMCP-로컬-서버-제작.html"
L_03 = "03-stdio와-원격-전송-권한-경계.html"
L_04 = "04-LangChain-MCP-클라이언트-연동.html"
L_05 = "05-도구-정의와-첫-호출-토큰.html"

LEARNED_ROWS = [
    (link(L_01, "01절"), "서버 객체를 넘기면 같은 커널 안에서 붙는 메모리 연결 · 함수 <code>names_of</code>", "도구 셋을 받는 연결 · 서버가 알린 도구와 붙일 도구의 이름"),
    (link(L_02, "02절"), "데코레이터 줄로 서버 객체에 도구 붙이기 · <code>runpy.run_path</code>로 서버 파일 읽기", "<code>@server.tool</code> 둘로 도구 셋 서버 만들기"),
    (link(L_04, "04절"), "클래스 <code>MCPAdapter</code>로 MCP 도구 받기 · <code>create_agent</code>와 호출 한도 3 · <code>ainvoke</code> · 셈 「요청 수 = 도구를 요청한 응답 수 + 1」", "조립 함수 <code>run_agent</code> · 두 실행의 셈"),
    (link(L_05, "05절"), "명세 글자 수 · 첫 요청 입력 토큰 · 서버 객체에 도구 둘을 더 붙인 셀", "붙일 도구의 명세 글자 수 · 요청마다 입력 토큰"),
    (link(L_CH19_03, "Ch 19 03절"), "함수 <code>spec_length</code>로 명세 글자 수 세기", "5절·6절 첫 셀"),
    (link(L_CH19_04, "Ch 19 04") + "·" + link(L_CH19_05, "05절"), "함수 <code>tool_call_names</code>·<code>sum_usage</code>", "응답마다 도구 호출 요청 · 모델 요청 수"),
    (link(L_CH22_04, "Ch 22 04절"), "호출 한도 <code>ModelCallLimitMiddleware</code>", "<code>call_limit</code>(한 번 실행에 요청 3번까지)"),
    (link(L_CH06_06, "Ch 6 06절"), "요금표와 함수 <code>estimate_cost</code>", "두 실행의 예상 비용"),
]

RESULT_ROWS = [
    ("붙인 도구 수 <code>tool_count</code>", "1(<code>lookup_policy</code>)", "3(도구 셋)", "바꾼 값"),
    ("붙인 도구의 명세 글자 수", "<code>명세 글자 수: 252</code>", "<code>명세 글자 수: 685</code>", "구조 값"),
    ("응답마다 도구 호출 요청 · 요청 수", "<code>['lookup_policy']</code> → <code>[]</code> · 요청 2", "<code>['lookup_policy']</code> → <code>[]</code> · 요청 2", "모델 판단 값"),
    ("셈 「요청 수 = 도구를 요청한 응답 수 + 1」", "<code>True</code>(도구를 요청한 응답 1 + 1)", "<code>True</code>(도구를 요청한 응답 1 + 1)", "구조 값"),
    ("요청마다 입력 토큰", "요청 1 187 · 요청 2 243", "요청 1 252 · 요청 2 308", "서비스가 센 값"),
    ("요청마다 늘어난 입력 토큰(실행 2 − 실행 1)", "기준", "65 · 65(합의 차 130)", "서비스가 센 값의 차"),
    ("출력 토큰 · 예상 비용 · 답 글", "출력 토큰·예상 비용은 아래 표, 답 글은 5절 둘째 셀 출력", "출력 토큰·예상 비용은 아래 표, 답 글은 6절 둘째 셀 출력", "흔들리는 값"),
    ("도구 인자", "출력하지 않음", "출력하지 않음", "노트북 밖 열 번 같음 — 결론에 쓰지 않음"),
]

TOKEN_ROWS = [
    ("실행 1(도구 하나)", "430", "32", "0.000467"),
    ("실행 2(도구 셋)", "560", "32", "0.000564"),
]

B4_ANALOGY = "<p>01절부터 쓴 우주 정거장 비유를 이어 갑니다. 정거장의 네모난 격납고 앞에 받침대가 있고, 받침대 위에는 통을 꽂는 자리가 셋 있습니다. 격납고 지붕의 로봇 팔이 통을 집어 받침대에 꽂습니다. 관제실은 보급선과 교신할 때마다, 받침대에 꽂힌 통의 설명을 모두 함께 읽어 줍니다.</p><p>격납고가 MCP 서버이고, 격납고가 내줄 수 있는 통 셋이 서버가 알린 도구 셋입니다. 로봇 팔이 조립 함수 <code>run_agent</code>이고, 받침대에 꽂힌 통이 에이전트에 붙인 도구입니다. 교신 한 번이 모델 요청 한 번이고, 읽어 주는 설명이 도구 명세입니다. 통을 셋 꽂으면 교신할 때마다 설명 셋을 읽으니, 교신이 두 번이면 두 번 모두 길어집니다.</p><p>비유와 다른 점도 있습니다. 설명이 셋이라고 입력 토큰이 세 배가 되지는 않는다는 것을 05절에서 보았습니다. 또 그림에는 교신하는 장면이 없고, 통을 꽂는 모습만 있습니다.</p>"

LOOK_B5 = "노트북 5절과 6절 첫 셀에서 붙일 도구와 명세 글자 수가 252와 685로 다른지 봅니다. 두 실행의 넷째 셀에서 셈이 맞는지 봅니다. 7절 첫 셀에서 요청 번호마다 늘어난 입력 토큰을 봅니다."

B7_ITEMS = [
    "질문과 시스템 메시지 글은 04절 5절과 같은 글로 실행 전에 정했고, 결과를 보고 바꾸지 않았습니다. 바꿀 값 <code>tool_count</code>의 1과 3도 실행 전에 정했습니다. 서버가 알린 도구 셋 가운데 하나와 셋 전부이고, 흐름을 보여 주려고 정한 예입니다.",
    "노트북을 쓰기 전에 두 실행을 노트북 밖에서 다섯 번씩 보냈습니다. 열 번 모두 모델은 <code>lookup_policy</code>를 한 번 부른 뒤 답했고, 요청마다 입력 토큰도 다섯 번 모두 같았습니다. 답 글은 실행 1 조건 다섯 번이 모두 이 노트북과 다른 문장이었습니다. 같은 요청도 실행한 때에 따라 모델이 쓰는 글이 달라질 수 있습니다.",
    "두 실행을 요청 번호마다 견줄 수 있는 것은, 두 실행이 같은 도구를 같은 차례로 불렀을 때입니다. 노트북 밖 기록에서는 열 번 모두 도구 인자와 도구 메시지 글도 같았습니다. 모델이 다른 도구를 부르거나 여러 번 부르면 요청에 실린 메시지가 달라져, 이렇게 견줄 수 없습니다.",
    "실행 2에서 붙인 <code>search_topics</code>·<code>show_topics</code>는 이번 실행에서 불리지 않았습니다. 불리지 않은 도구도 붙어 있으면 요청마다 명세가 실립니다. 이 절은 그만큼을 요청 번호마다 늘어난 입력 토큰으로 보았습니다.",
    "실무에서는 MCP 서버가 알린 도구를 모두 붙이지 않고, 쓸 도구만 골라 붙이는 방법을 생각할 수 있습니다. 05절 참고 자료의 OpenAI 함수 호출 문서도 토큰 한도에 닿으면 처음에 싣는 함수 수를 줄이라고 제안합니다. 이 절은 목록 앞에서 고르기만 했고, 이름이나 꼬리표로 고르는 방법은 실행하지 않았습니다.",
    "도구를 덜 붙이면 모델이 부를 수 있는 도구도 줄어듭니다. 이 절의 질문은 운영 규정 도구 하나로 답할 수 있는 질문이라, 도구 하나로도 답했습니다. 질문에 필요한 도구를 빼면 모델이 규정을 찾지 못할 수 있고, 그 경우는 실행하지 않았습니다.",
    "메모리 연결로 붙여 자식 프로세스를 띄우지 않았습니다. 04절처럼 stdio로 붙여도 같은 도구는 같은 명세라는 것을 05절 4절에서 보았습니다. 04절 5절은 stdio로 붙인 도구 하나와 같은 질문으로 에이전트를 실행해, 입력 토큰 합만 출력했습니다. 그 절의 이번 실행에서는 실행 1의 합과 같은 430이었고, 요청마다 나눈 값은 보지 않았습니다.",
    "서버 객체에 붙인 도구 둘은 이 커널 안에서만 붙었고, 서버 파일은 그대로입니다. 호출 한도 객체 하나를 두 에이전트가 함께 썼고, 한도는 invoke 한 번마다 셉니다. 03절처럼 접근 토큰의 범위에 따라 서버가 알리는 도구가 달라지는 조건은 이번에도 실행하지 않았습니다.",
    "캐시 입력은 노트북 밖 스무 요청 모두 0이었습니다. 예상 비용은 2026-09-17 요금표로 어림한 값이고, 청구 금액이 아닙니다. 이 노트북의 <code>assert</code>는 파일 찾기 셀과 키 확인 셀뿐이고, 모델이 고른 값에는 걸지 않았습니다.",
    "교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다. 걸린 시간은 재지 않았습니다.",
]

QUIZ = [
    ("[하] 실행 2에서 바꾼 값은 무엇이고, 그 값으로 붙인 도구의 명세 글자 수는 어떻게 달라졌나요?",
     "에이전트에 붙이는 도구 수 <code>tool_count</code>를 1에서 3으로 바꿨습니다. 붙인 도구의 명세 글자 수는 252에서 685가 되었습니다. 명세 글자 수는 코드가 정하는 값이라 다시 실행해도 같습니다. 틀렸다면 노트북 5절과 6절 첫 셀을 다시 읽습니다."),
    ("[중] 두 실행에서 모델 요청은 몇 번이었고, 그 수를 셈으로 어떻게 설명하나요?",
     "두 실행 모두 2번이었습니다. 모델이 도구를 요청한 응답이 하나였고, 마지막에 답을 쓴 응답이 하나 더 있어 1 + 1입니다. 흔들림 확인 다섯 번과 두 커널에서도 같았습니다. 틀렸다면 노트북 5절과 6절의 넷째 셀을 다시 읽습니다."),
    ("[중] 도구를 셋 붙인 실행 2에서, 도구를 부른 뒤의 둘째 요청도 입력 토큰이 늘었나요?",
     "늘었습니다. 요청 2의 입력 토큰은 실행 1이 243, 실행 2가 308로 65 많았고, 요청 1과 같은 만큼이었습니다. 붙인 도구의 명세가 도구를 부른 뒤의 요청에도 실린 셈입니다. 흔들림 확인 다섯 번과 두 커널에서 같은 값이었습니다. 틀렸다면 노트북 7절 첫 셀을 다시 읽습니다."),
    ("[상] 도구를 셋 붙인 에이전트가 도구를 두 번 부르고 답해, 요청이 3번이었다고 합시다. 입력 토큰 합은 도구 하나일 때보다 얼마나 늘 것으로 어림하나요?",
     "요청마다 65씩 늘어난다면, 세 요청이라 65의 세 배인 195쯤 늘 것으로 어림합니다. 다만 두 실행이 같은 도구를 같은 차례로 부르고, 명세 말고는 같은 메시지를 실을 때의 어림입니다. 도구를 두 번 부르는 실행은 이번에 하지 않았습니다. 틀렸다면 노트북 7절과 본문의 주의할 점을 다시 읽습니다."),
]


def quiz_html() -> str:
    parts = ['<details class="quiz" open><summary>문제 4개 · 해설 포함</summary>']
    number = 1
    for question, answer in QUIZ:
        parts.append('<p class="quiz-q">' + str(number) + ". " + question + '</p><p class="quiz-a">' + answer + "</p>")
        number = number + 1
    parts.append("</details>")
    return "".join(parts)


def src_html() -> str:
    learned = table_html(["절", "배운 것", "실습에서 쓰는 곳"], LEARNED_ROWS)
    results = table_html(["확인한 것", "실행 1(도구 하나)", "실행 2(도구 셋)", "값의 성격"], RESULT_ROWS)
    tokens = table_html(["실행", "입력 토큰 합(교재 출력)", "출력 토큰 합(교재 출력)", "예상 비용(교재 출력, 달러)"], TOKEN_ROWS)
    b7 = ""
    for item in B7_ITEMS:
        b7 = b7 + "<li>" + item + "</li>"
    return ("""<!--meta: 실습 30분 | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 0 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>서버에 도구 붙이기·에이전트 연결·입력 토큰 세기를 한 흐름에 모아, MCP 도구를 붙인 에이전트를 실행할 수 있습니다.</li>
<li>에이전트에 붙이는 도구 수 하나만 바꾼 두 실행을, 요청마다 입력 토큰으로 견줄 수 있습니다.</li>
<li>붙인 도구의 명세가 도구를 부른 뒤의 요청에도 실리는지 출력으로 설명할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>이 챕터에서는 MCP의 기능을 절마다 따로 익혔습니다. """ + link(L_02, "02절") + """은 서버 객체에 도구를 붙였고, """ + link(L_04, "04절") + """은 MCP 도구를 에이전트에 붙였습니다. """ + link(L_05, "05절") + """은 도구를 알린 첫 요청이 입력 토큰을 얼마나 더 쓰는지 셌습니다. MCP 서버를 실제로 쓸 때는, 서버가 알린 도구를 모두 붙일지 몇 개만 고를지 정해야 합니다.</p>
<p>이번 실습은 도구 셋을 알리는 자료실 서버에서, 에이전트에 붙이는 도구 수만 바꿔 두 번 실행합니다. 실행 1은 도구 하나를 붙여 04절 5절과 같은 질문으로 실행하고, 실행 2는 도구 셋을 붙입니다. 두 조건의 첫 요청은 05절 5절에서 이미 셌습니다. 새로 볼 것은 에이전트가 도구를 부른 뒤 모델을 다시 부르는 둘째 요청과, 실행 전체의 입력 토큰 합입니다.</p>
<p>이번 절은 이 챕터의 실습입니다. 01~05절에서 쓴 이름과 Ch 2에서 배운 문법만 쓰고, 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p>
<p><strong>이 절의 질문</strong> — 에이전트에 붙인 MCP 도구를 하나에서 셋으로 늘리면, 도구를 부른 뒤의 요청에서도 입력 토큰이 늘어날까요? 늘어난다면 실행 전체로는 얼마나 늘까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>이번 실습은 아래 절에서 배운 이름을 그대로 씁니다. 함수는 도구 파일 <code>connect_tools.py</code>에서 가져오고, 조립 함수와 결과를 볼 함수 둘은 노트북에 적습니다.</p>
""" + learned + """
<p>붙인 기능은 02절 서버에 도구 붙이기, 04절 에이전트 연결, 05절 명세 글자 수와 입력 토큰 세기 셋입니다. 셋이 모두 흐름 안에서 일하도록 했습니다. 02절 모양으로 붙인 도구 둘은 실행 2의 에이전트에 실립니다. 04절의 조립과 셈은 두 실행 모두에 쓰고, 05절의 두 값은 두 실행을 견주는 잣대입니다.</p>
<p>바꿀 값으로는 에이전트에 붙이는 도구 수를 골랐습니다. 05절은 첫 요청만 셌고, 도구를 부른 뒤의 요청은 재지 않았다고 적었기 때문입니다. """ + link(L_03, "03절") + """의 전송과 접근 토큰은 붙이지 않았습니다. 도구 수를 바꾸는 데 전송이 필요 없고, 서버를 띄우고 끄는 셀이 늘기 때문입니다. 05절의 직접 도구와 설명을 늘린 도구는 바꿀 값의 다른 후보라, 이번에는 도구 수 하나만 바꿨습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3>""" + B4_ANALOGY + """
""" + illustration_block() + """<h3>실습 조립의 구성</h3><p>조립 함수 <code>run_agent</code>는 에이전트에 붙일 도구 목록 하나만 인자로 받습니다. 모델·시스템 메시지 글·호출 한도·질문은 앞 셀에서 만든 이름을 두 실행이 그대로 씁니다. 도구 목록은 서버가 알린 도구 셋에서 앞의 <code>tool_count</code>개를 골라 만듭니다. 결과는 함수 <code>show_requests</code>와 <code>count_asked</code>가 두 실행 모두 같은 모양으로 출력합니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>요청마다 실리는 도구 명세</h3><p>04절에서 본 것처럼, 에이전트는 도구를 부르고 나면 모델을 한 번 더 부릅니다. 설치판 langchain 1.4.0 소스 <code>langchain/agents/factory.py</code> 1431~1438행은 도구가 있으면 모델에게 도구 목록을 알립니다. 1500~1505행은 비동기로 모델을 부를 때마다 이 일을 하고, 시스템 메시지를 맨 앞에 둡니다. 소스대로라면 둘째 요청에도 붙인 도구의 명세가 모두 실립니다.</p><p>그래서 도구를 셋 붙이면, 첫 요청뿐 아니라 도구를 부른 뒤의 요청에도 입력 토큰이 늘 것으로 예상합니다. 모델이 두 실행에서 같은 도구를 같은 차례로 부른다면, 요청마다 늘어나는 입력 토큰도 같을 것입니다. 이 예상이 맞는지는 노트북 7절에서 봅니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 서버 객체에 도구 둘을 더 붙이고, 메모리 연결로 도구 셋을 받습니다. 3절은 호출 한도·글·조립 함수를, 4절은 결과를 볼 함수 둘을 적습니다. 5절은 도구 하나를 붙인 실행 1을, 6절은 도구 수만 셋으로 바꾼 실행 2를 실행합니다. 7절에서 두 실행의 입력 토큰을 요청마다 견줍니다.</p><p>실제 OpenAI 모델 <code>gpt-5.4-mini</code>를 temperature 0으로 부릅니다. 모델 요청은 5절에서 2번, 6절에서 2번, 모두 4번이었고, 노트북 밖 열 번과 새 커널 두 번에서 같았습니다. 요금표로 어림한 예상 비용은 두 실행을 합쳐 0.002달러 아래이고, 청구 금액이 아닙니다. 메모리 연결이라 자식 프로세스를 띄우지 않고, 노트북이 쓰는 파일도 없습니다. 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
<h3>실행 1의 실제 순서</h3>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>두 실행은 서버·질문·시스템 메시지 글·호출 한도·조립 함수가 같고, 에이전트에 붙인 도구 수만 달랐습니다. 아래 표는 노트북 5·6·7절 출력에서 코드가 정하는 값과, 모델과 서비스가 정한 값을 모은 것입니다.</p>
""" + results + """
<p>흔들림 확인 다섯 번과 두 커널에서 모두, 두 실행의 차례는 같았습니다. 모델은 첫 응답에서 <code>lookup_policy</code> 하나를 요청하고, 둘째 응답에서 도구 요청 없이 답했습니다. 그래서 두 실행 모두 모델 요청은 2번이었고, 셈 「요청 수 = 도구를 요청한 응답 수 + 1」이 맞았습니다. 도구를 셋 붙여도, 이번 질문에서 모델은 운영 규정 도구 하나만 불렀습니다.</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>같은 확인에서 요청마다 입력 토큰은 실행 1이 187·243, 실행 2가 252·308이었습니다. 요청 1과 요청 2 모두 65씩 늘어, 입력 토큰 합은 130 많았습니다. 첫 요청의 65는 05절 5절에서 도구 하나와 셋의 첫 요청 차로 본 값과 같습니다. 새로 본 것은 도구를 부른 뒤의 둘째 요청에도 같은 65가 더해졌다는 점입니다.</p><p>불리지 않은 두 도구도 붙어 있는 동안 두 요청 모두에 명세가 실린 셈입니다. 이번 두 실행에서는 늘어난 입력 토큰이 요청마다 되풀이되어, 합의 차가 요청마다의 차의 두 배였습니다. 요청이 셋 이상인 실행에서도 그런지는 이번에 재지 않았습니다.</p>
<p>아래 표는 두 실행의 교재 출력 토큰 합과 예상 비용입니다. 출력 토큰과 예상 비용은 다시 실행하면 달라질 수 있습니다.</p>
""" + tokens + """
<p>새 커널로 두 번 실행해 견주자, 코드 셀 스물넷의 출력이 셀마다 모두 같았습니다. 답 글과 출력 토큰도 두 번 같았지만, 노트북 밖 다섯 번에서는 실행 1의 답 글과 출력 토큰이 달랐습니다. 그래서 답 글·출력 토큰·예상 비용은 결론에 쓰지 않았고, 명세 글자 수·셈·요청마다 입력 토큰만 결론과 그림에 썼습니다.</p>
<p class="look"><b>확인할 점</b> — 노트북 7절 첫 셀에서 두 줄의 늘어난 입력 토큰이 같은지 봅니다. 마지막 셀의 입력 토큰 합의 차가 그 두 값의 합인지 셉니다. 교재 출력에서는 65·65와 130이었습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul>""" + b7 + """</ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>02절 서버에 도구 붙이기, 04절 에이전트 연결, 05절 명세 글자 수와 입력 토큰 세기를 에이전트 하나에 모았습니다.</li><li>붙인 도구를 하나에서 셋으로 바꾸자 명세 글자 수가 252에서 685가 되었고, 두 실행 모두 셈대로 요청이 끝났습니다.</li><li>흔들림 확인 다섯 번과 두 커널에서 모두, 도구 셋을 붙인 실행은 첫 요청과 둘째 요청에서 입력 토큰이 65씩 많았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 28이 끝납니다. Ch 29에서는 에이전트를 평가하는 방법을 배웁니다. """ + link(L_CH29_01, "Ch 29 01절") + """은 평가 방법 세 가지를 견줍니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>""" + quiz_html() + """
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li>04절 — 클래스 <code>MCPAdapter</code>로 받은 MCP 도구, <code>create_agent</code>와 호출 한도, 셈 「요청 수 = 도구를 요청한 응답 수 + 1」.</li><li>05절 — 도구 명세와 명세 글자 수, 첫 요청 입력 토큰을 보았습니다. OpenAI 함수 호출 문서의 권고도 그 절의 참고 자료에 있습니다.</li><li>설치판 langchain 1.4.0 소스 <code>langchain/agents/factory.py</code> 1431~1438행은 도구가 있으면 모델에게 도구 목록을 알리는 자리입니다. 1500~1505행은 비동기로 모델을 부를 때마다 그 자리를 거치고, 시스템 메시지를 맨 앞에 둡니다.</li><li>""" + link(L_CH22_04, "Ch 22 04절") + """ — 호출 한도 <code>ModelCallLimitMiddleware</code>.</li><li>기준 버전은 노트북 1절 첫 셀에서 설치한 패키지 여섯의 판입니다.</li></ul>
""")


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    check_tools()
    check_same_as_prev()
    check_same_as_probe()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "connect_tools.py").write_text(TOOLS_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        print("copied", target / "connect_tools.py")
        sys.exit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        # 06절은 도구 파일을 쓰지 않습니다(05절 판 그대로 — check_tools()가 확인)
        path = write_notebook(LAB, "06", SLUG, "experiment", cells())
        print("wrote", path)
