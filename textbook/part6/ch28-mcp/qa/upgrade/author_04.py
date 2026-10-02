"""Ch 28 04절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§5-3·§6 experiment).

사용:
  python3 -B author_04.py                  → 도구 파일(가드)·노트북·_src 본문을 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_04.py --src-only       → _src 본문만 다시 쓴다(노트북은 그대로)
  python3 -B author_04.py --tools-copy DIR → 디스크의 도구 파일 connect_tools.py를 DIR에 복사한다(새 커널 사본 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**. 슬러그 그대로.

## 결정 1 — 연결은 설치판 langchain 1.4.0의 langchain.mcp.MCPAdapter (챕터 공통·03 인계 2번)

잠금에 langchain-mcp-adapters가 없다(MultiServerMCPClient·load_mcp_tools는 ModuleNotFoundError). 공식 문서(LangChain MCP, 확인 2026-09-28)도
MCPAdapter를 권한다. 다만 문서 예는 MCPAdapter(Path("weather_server.py"))(keep_alive 기본 True — 목록을 받은 뒤에도 자식 1, 시작 안내·새 판 확인 표준 오류,
노트북 밖 /tmp/ch28-04/exp/x3_block.py) → 이 절은 03절 함수 stdio_config(keep_alive False + FASTMCP 세 이름)로 만든 설정 딕셔너리를 넘긴다(차이는 b7).
langchain.mcp는 가져올 때 LangChainBetaWarning을 셀 표준 오류로 한 번 찍고, 그 줄에 커널 임시 파일 이름이 들어가 두 커널 대조를 깬다
(/tmp/ch28-04/exp/nbtest.ipynb) → 가져오기 셀에서 warnings.filterwarnings("ignore", category=LangChainBetaWarning)로 그 종류 하나만 끈다(문서가 적은 방법).

## 결정 2 — 앞 절반 모델 없음(2~4절, 결정적 요청 0), 뒤 절반 실제 모델(5절, 요청 2)

2절 변환: StructuredTool · 입력 형식 dict(01 4절 출력과 같은 글) · response_format content_and_artifact · metadata 꼬리표 ['public', 'read'].
3절 부르기: invoke → NotImplementedError(한 셀 try, Ch 26 선례) · ainvoke → 내용 블록 목록(글만 출력, 블록 id lc_<uuid>는 출력하지 않음) ·
부른 뒤 자식 0 · 연결 블록 안에서는 같은 서버(pid 같음 True — 번호는 출력하지 않음)를 이어 쓰고 블록 뒤 0.
4절 Ch 20 01 선례: StateGraph(MessagesState) + ToolNode(MCP 도구) + 손으로 만든 AIMessage(call_a 운영·call_b 주차) → ainvoke →
ToolMessage call_a success / call_b error(서버 오류 글, 02 6절과 같은 글) · 아티팩트 structured_content / None.
5절: nbkit 키·모델 셀 → create_agent(model, tools=MCP 도구, system_prompt=…, middleware=[ModelCallLimitMiddleware(run_limit=3, exit_behavior="end")])
→ ainvoke 한 번. 요청 수 셈 「도구를 요청한 응답 수 + 1」(Ch 26·27). 흔들림: qa/upgrade/04-probe.md(§0 21:11:15Z, 첫 요청 21:11:24Z, 5/5 같음).
assert는 파일 찾기 셀(01 셀 글)과 키 셀뿐. 흔들리는 값(도구 인자·답 글·토큰·비용)은 [[READ_…]] 자리 표시 → 교재 출력(A) 뒤 mdpatch.py.

## 결정 3 — 도구 파일 connect_tools.py 04 판 (03 판 + stdio_config + 앞 챕터 함수 셋, 대조 사슬 이어 감)

03 판(9139c4f8…)의 머리 설명·함수 블록 둘은 글자 그대로 두고, 가져오기 블록에 import sys를 넣고, 03 노트북 셀 글 stdio_config(author_03.DEF_CONFIG)와
Ch 21 runner_tools.py(f4113158…)의 tool_call_names·sum_usage·estimate_cost(설명 주석·본문 글자 그대로 — Ch 27 harness_tools.py 7a40d994… 판과도 대조)를 더한다.
쓰기 가드: 없거나 · 03 판이거나 · 이 판과 같을 때만 쓰고, 뒤 절 판(머리 설명으로 시작하고 이 판의 블록을 모두 담음)은 건너뛰고, 그 밖이면 멈춘다.
03 생성기의 later_version()은 이 판을 「뒤 절 판」으로 보고 덮어쓰지 않는다(머리 설명·03 블록 글자 그대로).
show_messages는 가져오지 않는다 — MCP 도구 메시지 내용에 실행마다 바뀌는 블록 id가 있어, 5절은 내용을 빼고 같은 차례로 출력하는 셀을 따로 둔다.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·대입 풀기·별표 풀기·
세미콜론·`isinstance`·`importlib`·클래스·데코레이터·`asyncio.run`·`while`. `try`는 invoke 셀 하나. 호출 깊이 2 이하.
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(HERE))
import author_01  # noqa: E402  01절 셀 글(FIND_FILE)
import author_02  # noqa: E402  본문 도우미
import author_03  # noqa: E402  03절 셀 글(QUIET·DEF_CONFIG)·도구 파일 03 판
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch28-mcp/notebooks"
FIGS = ROOT / "textbook/part6/ch28-mcp/figures"
SLUG = "04-LangChain-MCP-클라이언트-연동"
TITLE_TEXT = "LangChain MCP 클라이언트 연동"
SRC = ROOT / "textbook/part6/ch28-mcp/_src" / (SLUG + ".html")
NB03 = LAB / "03-stdio와-원격-전송-권한-경계.ipynb"
TOOLS_PATH = LAB / "connect_tools.py"
RUNNER = ROOT / "labs/part6/ch21-create-agent/notebooks/runner_tools.py"
RUNNER_SHA = "f4113158c0ccaee1205f0eabe315ef153e14c4dc6bcfd70ae8a9378edda96bdf"
HARNESS = ROOT / "labs/part6/ch27-deepagents/notebooks/harness_tools.py"
# 전체 마감(2026-09-30)에서 Ch 27 도구 파일 머리 설명 줄만 고쳐 7a40d994… → ed5c4240…(함수 본문 같음)
HARNESS_SHA = "ed5c424006c2b41dd40c3d4861555fbe4180b8df7de2144febd7ef4f9a3f5b2c"
TOOLS_03_SHA = "9139c4f8410c8e799d838bbf0addb6ca42713869d7d51f6244eb41c6d96ef6e4"
DEF_CONFIG_SHA = hashlib.sha256(author_03.DEF_CONFIG.encode("utf-8")).hexdigest()
html_text = author_02.html_text
table_html = author_02.table_html


def placeholder(name: str) -> str:
    """교재 출력(A) 뒤 mdpatch.py로 채울 자리 표시(흔들리는 값의 둘째 단락·b6 표·두 커널 문장)."""
    return "[[READ_" + name + "]]"


# ---------------------------------------------------------------- 도구 파일 connect_tools.py (04 판)
TOOLS_IMPORTS_04 = '''
import sys

from fastmcp import Client
from fastmcp.exceptions import ToolError
'''
NOTE_03 = "Ch 28 03절에서 배웠습니다 — 03절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다"
RUNNER_NOTES = [
    ("tool_call_names", "Ch 19 04절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다"),
    ("sum_usage", "Ch 19 05절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다"),
    ("estimate_cost", "Ch 6 06절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다"),
]
TOOL_ORDER = ["names_of", "call_tool_row", "stdio_config", "tool_call_names", "sum_usage", "estimate_cost"]


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


def blocks_04() -> list:
    """04 판에 담는 블록(「# 배운 곳」 줄 + 글) 차례: 03 판 블록 둘 + stdio_config + 앞 챕터 함수 셋."""
    runner = RUNNER.read_text(encoding="utf-8")
    assert hashlib.sha256(runner.encode("utf-8")).hexdigest() == RUNNER_SHA, "Ch 21 runner_tools.py가 마감 판과 다릅니다"
    found = []
    for name, note, cell_source, sha, notebook in author_03.CELLS:
        found.append("\n\n# " + note + "\n" + cell_source + "\n")
    found.append("\n\n# " + NOTE_03 + "\n" + author_03.DEF_CONFIG + "\n")
    for name, note in RUNNER_NOTES:
        found.append("\n\n# " + note + "\n" + file_block(runner, name) + "\n")
    return found


def tools_text() -> str:
    text = author_03.TOOLS_HEAD + TOOLS_IMPORTS_04
    for block in blocks_04():
        text = text + block
    return text


TOOLS = tools_text()


def notebook_code_sources(path: Path) -> list:
    return author_03.notebook_code_sources(path)


def later_version(current: str) -> bool:
    """뒤 절이 함수·가져오기 줄을 더한 판인지 봅니다: 머리 설명으로 시작하고 이 판의 블록을 모두 담으면 참."""
    if not current.startswith(author_03.TOOLS_HEAD):
        return False
    for block in blocks_04():
        if block.strip("\n") not in current:
            return False
    return current != TOOLS


def check_tools() -> None:
    """도구 파일 04 판이 03 판을 그대로 잇고, 더한 함수 넷이 원본(03 노트북 셀·Ch 21·Ch 27 도구 파일)과 글자·AST 모두 같은지 봅니다."""
    assert hashlib.sha256(author_03.TOOLS.encode("utf-8")).hexdigest() == TOOLS_03_SHA, "03 생성기의 도구 파일 판이 03 마감 판과 다릅니다"
    harness = HARNESS.read_text(encoding="utf-8")
    assert hashlib.sha256(harness.encode("utf-8")).hexdigest() == HARNESS_SHA, "Ch 27 harness_tools.py가 마감 판과 다릅니다"
    # 03 판 = 머리 설명 + 가져오기 둘 + 블록 둘. 04 판은 가져오기 블록에 import sys만 더하고 나머지 03 글은 그대로 담습니다
    assert TOOLS.startswith(author_03.TOOLS_HEAD)
    assert author_03.TOOLS[len(author_03.TOOLS_HEAD) + len(author_03.TOOLS_IMPORTS):] in TOOLS
    tree = ast.parse(TOOLS)
    names = []
    imports = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
    assert names == TOOL_ORDER, names
    assert imports == ["import sys", "from fastmcp import Client", "from fastmcp.exceptions import ToolError"], imports
    # stdio_config는 03 노트북 셀 글 그대로(디스크 03 노트북 코드 셀에 그 글이 있는지)
    assert author_03.DEF_CONFIG in notebook_code_sources(NB03), "stdio_config가 디스크 03 노트북 셀과 다릅니다"
    mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "stdio_config"]
    theirs = [ast.dump(n) for n in ast.parse(author_03.DEF_CONFIG).body if isinstance(n, ast.FunctionDef)]
    assert mine == theirs and len(mine) == 1, "stdio_config"
    runner = RUNNER.read_text(encoding="utf-8")
    runner_tree = ast.parse(runner)
    for name, note in RUNNER_NOTES:
        block = file_block(runner, name)
        assert ("# " + note + "\n" + block + "\n") in TOOLS
        assert file_block(harness, name) == block, name + "가 Ch 27 판과 다릅니다"
        mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        theirs = [ast.dump(n) for n in runner_tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        assert mine == theirs and len(mine) == 1, name


def write_tools() -> None:
    current = ""
    if TOOLS_PATH.is_file():
        current = TOOLS_PATH.read_text(encoding="utf-8")
    if current == "" or current == TOOLS or current == author_03.TOOLS:
        TOOLS_PATH.write_text(TOOLS, encoding="utf-8")
        print("wrote", TOOLS_PATH)
    elif later_version(current):
        print("skip", TOOLS_PATH, "(뒤 절이 함수를 더한 판 — 덮어쓰지 않음)")
    else:
        raise AssertionError("도구 파일이 03·04절 판으로 시작하지 않습니다")


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["langchain[mcp]==1.4.0", "langchain-core==1.6.2", "langchain-openai==1.6.0", "langgraph==1.2.11",
                          "fastmcp==4.0.3", "mcp==2.2.0", "psutil==7.2.2", "python-dotenv==1.2.3"])

IMPORTS = r'''# 이 절에서 쓸 이름을 가져옵니다(langchain.mcp는 베타 경고 한 종류만 끄고 가져옵니다)
import warnings
import psutil
from langchain_core._api import LangChainBetaWarning
warnings.filterwarnings("ignore", category=LangChainBetaWarning)
from langchain.mcp import MCPAdapter
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
# 01·03절과 앞 챕터에서 배운 함수 다섯은 도구 파일에서 가져옵니다
from connect_tools import estimate_cost, names_of, stdio_config, sum_usage, tool_call_names

print("도구 파일에서 가져온 함수:", "estimate_cost, names_of, stdio_config, sum_usage, tool_call_names")'''

FIND_FILE = author_01.FIND_FILE
QUIET = author_03.QUIET

ADAPT = r'''# 03절 함수 stdio_config로 만든 설정 한 벌을 MCPAdapter에 넘기고, 도구 목록을 LangChain 도구로 받습니다
kernel_process = psutil.Process()
course_config = stdio_config(server_file, quiet_env)
adapter = MCPAdapter(course_config)
mcp_tools = await adapter.list_tools()
children_after = kernel_process.children()
print("받은 도구 이름:", names_of(mcp_tools))
print("목록을 받은 뒤 자식 프로세스 수:", len(children_after))'''

SHAPE = r'''# 바뀐 도구 하나의 종류·설명·입력 형식을 봅니다
policy_tool = mcp_tools[0]
print("도구 종류:", type(policy_tool).__name__)
print("설명:", policy_tool.description)
print("입력 형식의 종류:", type(policy_tool.args_schema).__name__)
print("입력 형식:", policy_tool.args_schema)'''

META = r'''# 도구가 내놓는 값의 모양과, 도구에 붙은 서버 정보·꼬리표를 봅니다
print("내놓는 값의 모양:", policy_tool.response_format)
mcp_info = policy_tool.metadata["mcp"]
tool_meta = mcp_info["tool"]["_meta"]
print("서버 정보:", mcp_info["server"])
print("꼬리표:", tool_meta["fastmcp"]["tags"])'''

INVOKE_ERR = r'''# Ch 19 01절처럼 .invoke로 불러 봅니다(오류 NotImplementedError만 받습니다)
try:
    policy_tool.invoke({"topic": "운영"})
except NotImplementedError as error:
    print("받은 것:", type(error).__name__)
    print("받은 글:", str(error))'''

AINVOKE = r'''# 비동기 판 ainvoke로 같은 인자를 넘겨 부르고, 부른 뒤 자식 프로세스 수를 셉니다
operation_blocks = await policy_tool.ainvoke({"topic": "운영"})
children_now = kernel_process.children()
first_block = operation_blocks[0]
print("받은 값의 종류:", type(operation_blocks).__name__)
print("내용 블록 수:", len(operation_blocks))
print("첫 블록의 키:", list(first_block))
print("첫 블록의 종류:", first_block["type"])
print("첫 블록의 글:", first_block["text"])
print("부른 뒤 자식 프로세스 수:", len(children_now))'''

IN_BLOCK = r'''# 연결 블록 안에서 같은 도구를 부르고, 부르기 전과 뒤의 자식 프로세스를 견줍니다
async with adapter:
    children_before_call = kernel_process.children()
    overdue_blocks = await policy_tool.ainvoke({"topic": "연체"})
    children_after_call = kernel_process.children()
children_now = kernel_process.children()
print("블록 안, 부르기 전 자식 프로세스 수:", len(children_before_call))
print("블록 안, 부른 뒤 자식 프로세스 수:", len(children_after_call))
print("같은 프로세스인가:", children_before_call[0].pid == children_after_call[0].pid)
print("블록을 벗어난 뒤 자식 프로세스 수:", len(children_now))'''

GRAPH = r'''# MCP 도구 목록으로 도구 실행 노드 하나만 둔 그래프를 만듭니다(Ch 20 01절 ToolNode)
builder = StateGraph(MessagesState)
builder.add_node("tools", ToolNode(mcp_tools))
builder.add_edge(START, "tools")
builder.add_edge("tools", END)
tool_graph = builder.compile()
print("등록한 노드:", list(builder.nodes))'''

HAND = r'''# 모델 대신, 도구 호출 요청 둘을 담은 응답 하나를 손으로 만듭니다(Ch 20 01절 모양)
good_call = {"name": "lookup_policy", "args": {"topic": "운영"}, "id": "call_a", "type": "tool_call"}
# 둘째 요청의 주제어 주차는 서버 파일의 규정에 없는 주제어입니다
bad_call = {"name": "lookup_policy", "args": {"topic": "주차"}, "id": "call_b", "type": "tool_call"}
hand_request = AIMessage(content="", tool_calls=[good_call, bad_call])
print("도구 호출 요청:", tool_call_names(hand_request))'''

RUN_GRAPH = r'''# 손으로 만든 응답을 넣어 그래프를 비동기 판 ainvoke로 실행하고, 메시지 종류를 차례로 봅니다
graph_result = await tool_graph.ainvoke({"messages": [hand_request]})
graph_messages = graph_result["messages"]
children_now = kernel_process.children()
print("메시지 종류:")
for message in graph_messages:
    print(type(message).__name__)
print("실행 뒤 자식 프로세스 수:", len(children_now))'''

TOOL_MSGS = r'''# 도구 메시지마다 호출 ID·결과 상태·글을 봅니다(내용 블록의 id는 실행마다 달라 출력하지 않습니다)
for message in graph_messages[1:]:
    print("호출 ID:", message.tool_call_id, "| 결과 상태:", message.status)
    print("글:", message.text)'''

ARTIFACT = r'''# 두 도구 메시지의 아티팩트(모델에게 보내지 않고 메시지에 붙여 두는 값)를 봅니다
success_message = graph_messages[1]
error_message = graph_messages[2]
print("성공한 메시지의 아티팩트:", success_message.artifact)
print("오류 메시지의 아티팩트:", error_message.artifact)'''

LIMIT = r'''# invoke 한 번에 모델 요청을 3번까지만 허락하는 호출 한도를 만듭니다(Ch 22 04절)
call_limit = ModelCallLimitMiddleware(run_limit=3, exit_behavior="end")
print("한 번 실행의 요청 한도:", call_limit.run_limit)
print("한도에 닿으면:", call_limit.exit_behavior)'''

AGENT = r'''# 모델 객체·MCP 도구·시스템 메시지 글·호출 한도로 에이전트를 만듭니다(Ch 21 01절, 요청은 아직 없음)
agent_rule = "교육센터 자료실 규정 질문에는 도구로 규정을 찾아, 찾은 글만 근거로 한국어 한 문장으로 답하세요."
mcp_agent = create_agent(model, tools=mcp_tools, system_prompt=agent_rule, middleware=[call_limit])
agent_graph = mcp_agent.get_graph()
print("노드:", list(agent_graph.nodes))'''

RUN = r'''# 질문 한 줄을 넣어 에이전트를 비동기 판 ainvoke로 한 번 실행합니다(도구를 한 번 부르면 모델 요청 2번)
question = "교육센터 자료실은 토요일에 몇 시까지 운영하나요?"
first_input = {"messages": [HumanMessage(content=question)]}
agent_result = await mcp_agent.ainvoke(first_input)
agent_messages = agent_result["messages"]
children_now = kernel_process.children()
print("결과 메시지 수:", len(agent_messages))
print("실행 뒤 자식 프로세스 수:", len(children_now))'''

KINDS = r'''# 결과 메시지를 차례로 보며, 응답이면 도구 호출 요청 이름을, 도구 메시지면 결과 상태를 출력합니다
for message in agent_messages:
    kind = type(message).__name__
    if kind == "HumanMessage":
        print(kind)
    if kind == "AIMessage":
        print(kind, "| 도구 호출 요청:", tool_call_names(message))
    if kind == "ToolMessage":
        print(kind, "| 결과 상태:", message.status)'''

ARGS = r'''# 모델이 쓴 도구 인자와, 도구 메시지의 글을 봅니다(모델이 고른 값이라 실행마다 달라질 수 있음)
for message in agent_messages:
    if type(message).__name__ == "AIMessage":
        for call in message.tool_calls:
            print("도구 인자:", call["args"])
    if type(message).__name__ == "ToolMessage":
        print("도구 메시지 글:", message.text)'''

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

ANSWER = r'''# 모델이 쓴 마지막 답 글을 봅니다(실행마다 달라질 수 있는 값)
final_answer = agent_messages[-1].text
print("마지막 답 글:")
print(final_answer)'''

COST = r'''# 입력·출력 토큰과, 2026-09-17 요금표(100만 토큰당 달러)로 어림한 예상 비용을 봅니다(Ch 6 06절 함수 estimate_cost)
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
run_cost = estimate_cost(run_usage, input_rate, cached_input_rate, output_rate)
rounded_cost = round(run_cost, 6)
print("입력 토큰:", run_usage["input_tokens"], "| 출력 토큰:", run_usage["output_tokens"])
print("예상 비용(달러):", rounded_cost)'''


def check_same_as_probe() -> None:
    """노트북 셀의 설정·도구·에이전트·질문 줄이 흔들림 확인 스크립트(probe04.py)와 같은 글인지 봅니다."""
    probe = (HERE / "probe/probe04.py").read_text(encoding="utf-8")
    pieces = []
    for cell in [QUIET, author_03.DEF_CONFIG, ADAPT, LIMIT, AGENT, RUN]:
        for line in cell.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("print(") or stripped == "":
                continue
            if stripped.startswith("kernel_process") or stripped.startswith("children_") or stripped.startswith("agent_graph"):
                continue
            if stripped.startswith("agent_result") or stripped.startswith("agent_messages"):
                continue
            pieces.append(stripped)
    pieces.append('model = init_chat_model(')
    pieces.append('"openai:gpt-5.4-mini",')
    pieces.append('temperature=0,')
    pieces.append('reasoning_effort="none",')
    pieces.append('warnings.filterwarnings("ignore", category=LangChainBetaWarning)')
    pieces.append('result = await mcp_agent.ainvoke(first_input)')
    for piece in pieces:
        assert piece in probe, piece


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/04-figures.md)
FIG1 = "04-1-MCP-도구가-LangChain-도구가-되기까지"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 초록 상자 서버 파일 course_server.py 도구 lookup_policy에서 파란 상자 stdio_config 설정 한 벌 keep_alive False로, 거기서 파란 상자 MCPAdapter list_tools로 화살표가 갑니다. 그 아래 노란 상자 StructuredTool lookup_policy 입력 형식 dict ainvoke로만 부름으로 화살표가 가고, 그 상자에서 점선 화살표 둘이 나란히 놓인 파란 상자 ToolNode 도구 실행 노드와 파란 상자 create_agent 에이전트로 가는 그림"
FIG1_CAP = "서버의 MCP 도구는 MCPAdapter를 지나 StructuredTool이 되었고, 같은 도구를 도구 실행 노드와 에이전트에 붙였습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 서버 파일이고, 파란 상자는 우리가 부른 함수와 클래스입니다.
노란 상자는 노트북 2·3절 출력으로 확인한 바뀐 도구의 모양입니다.
맨 아래 점선 둘은 같은 도구를 붙인 두 곳이고, 4절과 5절에서 차례로 씁니다.
모델은 5절에서만 부르고, 이 그림에는 모델 상자를 두지 않았습니다."""

FIG2 = "04-2-부르는-방법과-자식-프로세스"
FIG2_ALT = "위에 노란 상자 StructuredTool lookup_policy가 있고, 거기서 점선 화살표 둘이 아래에 나란한 칸 둘로 갑니다. 왼쪽 칸 블록 밖에서 부르기에는 노란 상자 invoke NotImplementedError와 노란 상자 await ainvoke 부른 뒤 자식 프로세스 0이 위아래로 있습니다. 오른쪽 칸 async with adapter 블록 안에는 노란 상자 부르기 전 자식 프로세스 1 부른 뒤 1 같은 프로세스 True에서 노란 상자 블록을 벗어난 뒤 0으로 화살표가 가는 그림"
FIG2_CAP = "블록 밖에서는 부른 뒤 서버가 남지 않았고, 블록 안에서는 블록이 띄운 서버 하나가 호출을 받았습니다."
FIG2_READ = """위의 노란 상자는 2절에서 받은 도구이고, 아래 두 칸은 3절에서 부른 두 자리입니다.
왼쪽 칸은 연결 블록 밖, 오른쪽 칸은 `async with adapter:` 블록 안입니다.
노란 상자는 모두 노트북 3절 출력이고, 받아 출력한 오류도 노랑으로 두었습니다.
오른쪽 칸 안의 화살표는 블록 안에서 밖으로 나간 차례입니다."""

FIG3 = "04-3-손으로-만든-요청과-도구-메시지"
FIG3_ALT = "위에서 아래로 읽는 흐름도입니다. 파란 상자 손으로 만든 AIMessage call_a 운영 call_b 주차에서 파란 상자 ToolNode 그래프 await ainvoke로, 거기서 초록 상자 서버 도구 lookup_policy 자식 프로세스로 띄움으로 화살표가 갑니다. 초록 상자에서 점선 화살표 둘이 나란한 노란 상자 ToolMessage call_a status success 운영 규정 글과 노란 상자 ToolMessage call_b status error 서버 오류 글로 갑니다. 맨 아래에 노란 상자 실행 뒤 자식 프로세스 0이 따로 있는 그림"
FIG3_CAP = "주제어 운영 요청은 success, 서버 규정에 없는 주차 요청은 서버 오류 글을 담은 error 도구 메시지가 되었습니다."
FIG3_READ = """위에서 아래로 읽습니다.
파란 상자는 4절에서 우리가 만든 응답과 그래프이고, 초록 상자는 도구를 실행한 서버입니다.
노란 상자는 노트북 4절 출력이고, 서버가 낸 오류를 담은 메시지도 노랑입니다.
점선 둘은 한 응답에 담긴 요청 둘이 각각 도구 메시지 하나가 된 갈래입니다.
모델을 부르지 않은 그래프라 보라 상자는 없습니다."""

FIG4 = "04-4-에이전트가-MCP-도구를-부른-차례"
FIG4_ALT = "세로선 넷이 있는 차례 그림입니다. 왼쪽부터 우리 코드, 에이전트 그래프, 연보라 띠 안의 모델 gpt-5.4-mini, MCP 서버 자식 프로세스입니다. 우리 코드에서 await ainvoke 질문 한 줄 화살표가 그래프로 가고, 요청 1 화살표가 모델로 가고 도구 요청 lookup_policy 점선이 돌아옵니다. 그래프에서 도구 실행 노드가 부름 화살표가 서버로 가고 ToolMessage success 점선이 돌아옵니다. 요청 2 화살표가 모델로 가고 도구 요청 없음 점선이 돌아온 뒤, 결과 메시지 넷 점선이 우리 코드로 돌아옵니다. 맨 아래 우리 코드와 그래프에 걸친 노란 메모에 요청 수 2는 도구를 요청한 응답 수 1 더하기 1, 실행 뒤 자식 프로세스 0이 적힌 그림"
FIG4_CAP = "에이전트가 MCP 도구를 한 번 부른 실행에서 모델 요청은 2번이었고, 도구를 요청한 응답 수 1에 1을 더한 값과 같았습니다."
FIG4_READ = """위에서 아래로 실행 차례대로 읽고, 세로선은 왼쪽부터 우리 코드, 그래프, 모델, 서버입니다.
연보라 띠는 실제로 부른 모델 gpt-5.4-mini의 자리입니다.
실선 화살표는 부르는 쪽, 점선 화살표는 내놓은 값이 돌아오는 쪽입니다.
맨 아래 노란 메모는 노트북 5절 출력입니다.
도구를 몇 번 부를지는 모델이 고르며, 이 그림은 한 번 부른 실행입니다."""

ILLU = "04-5-이음-부품으로-이은-모듈"
# 1차 job c08dddec-daf8-4af3-9e32-dbf61c45b3af 탈락(가운데 부품 양쪽 끝이 모두 둥글고 세 물건이 떨어져 있음) → 2차 job f18b3bd2-fb5a-462f-b93b-dbb7ed6f9834 채택
ILLU_ALT = "흰 바탕에 세 물건이 가로 한 줄로 이어진 그림입니다. 왼쪽은 작은 둥근 창 하나가 있는 흰 캡슐로, 둥근 끝이 왼쪽을 향하고 오른쪽 끝에 넓고 둥근 구멍이 열려 있습니다. 가운데 청록 이음 부품 하나는 왼쪽 절반이 끝이 둥근 원통이고 오른쪽 절반이 네모 덩어리이며, 둥근 쪽이 캡슐 구멍에 들어가 있습니다. 네모 쪽은 오른쪽의 크고 모서리를 깎은 연노랑 짐 모듈 왼쪽 끝에 꽂혀 있습니다. 사람·글자·숫자·화살표·별은 없는 그림"
ILLU_CAP = "둥근 구멍의 캡슐과 네모 자리의 짐 모듈이, 한쪽은 둥글고 한쪽은 네모인 이음 부품으로 한 줄이 되었습니다."
ILLU_READ = "왼쪽 흰 캡슐의 오른쪽 끝에 넓고 둥근 구멍이 있고, 가운데 청록 부품의 둥근 쪽이 그 구멍에 들어가 있습니다. 청록 부품의 오른쪽 절반은 네모 덩어리이고, 오른쪽 연노랑 짐 모듈의 왼쪽 끝에 꽂혀 있습니다. 캡슐이 LangChain 에이전트, 청록 부품이 클래스 <code>MCPAdapter</code>, 짐 모듈이 MCP 서버의 도구입니다. 그림은 부품을 한 번 끼워 둔 모습이지만, 이 절의 설정에서는 도구를 부를 때마다 서버를 띄웠다가 닫았습니다. 모듈 옆면의 칸 둘과 모서리 모양은 어떤 값과도 짝짓지 않습니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 서버의 MCP 도구를 `MCPAdapter`로 LangChain 도구로 바꾸고, 바뀐 도구의 모양을 모델 없이 봅니다.
2. 바뀐 도구를 부르는 방법과, 부를 때마다 서버 프로세스가 떴다가 끝나는지를 봅니다.
3. 도구 실행 노드와 에이전트에 MCP 도구를 붙이고, 에이전트를 실제 모델로 한 번 실행합니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 5절에서 에이전트를 한 번 실행합니다.
에이전트가 MCP 도구를 한 번 부르고 답하면, 모델 요청은 2번입니다.
호출 한도 3을 붙여, 요청이 끝없이 늘지 않게 막습니다.
요금표로 어림한 예상 비용은 0.001달러 아래이고, 청구 금액이 아닙니다.

2~4절은 모델을 부르지 않고, 출력은 서버와 도구가 주고받은 값입니다.
모델이 쓰는 도구 인자와 답 글은 실행마다 달라질 수 있습니다.
서버는 실습 폴더 맨 위의 서버 파일 `course_server.py`를 자식 프로세스로 띄웁니다.
노트북이 쓰는 파일은 없고, 걸린 시간은 재지 않았습니다.
앞에서 배운 함수 다섯은 도구 파일 `connect_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 여덟을 설치합니다.
판은 langchain 1.4.0, langchain-core 1.6.2, langgraph 1.2.11입니다.
패키지 langchain-openai 1.6.0, fastmcp 4.0.3, mcp 2.2.0도 설치합니다.
나머지 둘은 psutil 7.2.2와 python-dotenv 1.2.3입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~3절을 읽습니다.
MCP 도구가 LangChain 도구로 바뀐 모양과, 비동기로만 부를 수 있는 까닭을 보는 자리입니다.
4~5절은 도구 실행 노드와 에이전트에 붙여 실행하는 실습이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch28-mcp`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def model_cells() -> list[dict]:
    """과정 표준 키·모델 셀(nbkit)에 이 절의 결과 읽기(실행일·요청은 5절에서만)와 2절 첫 설명을 붙입니다."""
    cells = key_and_model_cells("openai:gpt-5.4-mini")
    cells[-1] = md("""**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.
모델 요청은 5절 실행 셀에서만 나갑니다.

## 2. MCP 도구를 LangChain 도구로 바꾸기

03절까지는 FastMCP의 클래스 `Client`로 서버의 도구를 직접 불렀습니다.
이 절은 같은 서버의 도구를 LangChain 도구로 바꿔, Ch 20·21의 그래프와 에이전트에 붙입니다.
먼저 01절 2절과 같은 셀로 서버 파일의 위치를 찾습니다.""")
    return cells


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

제목의 LangChain MCP는 langchain 1.4.0에 든 모듈 `langchain.mcp`를 가리킵니다.
그 안의 클래스 `MCPAdapter`가 MCP 서버에 붙어, 서버의 도구를 LangChain 도구로 바꿉니다.
바꾼 도구는 Ch 20의 도구 실행 노드와 Ch 21의 에이전트에 넘길 수 있습니다.

첫 셀은 패키지 여덟을 설치하고 설치된 판 번호를 출력합니다.
패키지 psutil은 03절에서 자식 프로세스 수를 센 패키지입니다.
패키지 langgraph는 Ch 20에서 도구 실행 노드를 가져온 패키지입니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langchain: 1.4.0`, `langgraph: 1.2.11`, `fastmcp: 4.0.3`, `psutil: 7.2.2`가 보입니다.
여덟 판 모두 실습 폴더 잠금과 같습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모듈 `langchain.mcp`는 아직 베타라서, 가져올 때 경고 `LangChainBetaWarning`을 한 번 냅니다.
그 경고 줄에는 실행마다 바뀌는 임시 파일 이름이 들어 있습니다.
그래서 모듈 `warnings`의 함수 `filterwarnings`로 이 경고 한 종류만 끄고 가져옵니다.
상태 형식 `MessagesState`는 LangGraph가 미리 만들어 둔 형식이고, 4절에서 풉니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: estimate_cost, names_of, stdio_config, sum_usage, tool_call_names`가 보입니다.
함수 `names_of`는 01절 4절에서 만든 함수로, 목록의 항목마다 이름을 모읍니다.
함수 `stdio_config`는 03절 2절에서 만든 함수로, 서버 파일 하나를 stdio로 띄우는 설정 한 벌을 만듭니다.
나머지 셋은 Ch 19 04·05절과 Ch 6 06절에서 배운 함수이고, 4·5절에서 씁니다.

함수 `stdio_config`와 앞 챕터 함수 셋은 이 절부터 도구 파일에서 가져옵니다.
앞 챕터 함수 셋은 Ch 21 도구 파일 `runner_tools.py`의 함수와 설명 주석·본문이 같습니다.
그 파일은 이 실습 폴더에 없는 패키지를 가져와서, 파일째 가져오지 않고 함수만 옮겼습니다."""),
    ] + model_cells() + [
        code(FIND_FILE),
        md("""**결과 읽기** — 출력 줄 `서버 파일을 찾았는가: True`가 보입니다.
교재 출력은 프로젝트 맨 위에서 실행해 셋째 후보 `labs/part6/ch28-mcp/course_server.py`를 골랐습니다.
`notebooks/` 폴더에서 열면 첫 후보 `../course_server.py`가 골라집니다.

다음 셀은 03절 2절과 같은 셀로, 서버를 조용히 띄우는 환경 변수 셋을 딕셔너리로 만듭니다."""),
        code(QUIET),
        md("""**결과 읽기** — 라벨 `조용히 하는 이름:` 뒤에 이름 셋이 보입니다.
03절에서 본 것처럼, 시작 안내와 새 판 확인을 끄고 기록 수준을 올리는 이름입니다.

다음 셀은 03절 함수 `stdio_config`로 설정 한 벌을 만들어, 클래스 `MCPAdapter`에 넘깁니다.
칸 `keep_alive`가 `False`인 설정이라, 연결을 닫으면 서버도 끝납니다.
메서드 `list_tools`는 서버에 연결해 도구 목록을 받습니다.
받은 도구를 하나씩 LangChain 도구로 바꿔, 그 목록을 내놓습니다.
연결은 이 메서드 안에서 열고 닫으므로, `async with` 블록 없이 `await`만 붙여 부릅니다."""),
        code(ADAPT),
        md("""**결과 읽기** — 출력 줄 `받은 도구 이름: ['lookup_policy']`가 보입니다.
03절에서 클래스 `Client`로 받은 도구와 같은 이름입니다.
출력 줄 `목록을 받은 뒤 자식 프로세스 수: 0`으로, 목록을 받는 동안 띄운 서버도 끝났습니다.

다음 셀은 바뀐 도구 하나의 종류·설명·입력 형식을 봅니다.
속성 `args_schema`는 도구의 입력 형식을 담는 칸입니다."""),
        code(SHAPE),
        md("""**결과 읽기** — 출력 줄 `도구 종류: StructuredTool`이 보입니다.
Ch 19 01절에서 `@tool` 줄로 만든 도구와 같은 종류입니다.
설명은 서버 파일 도구의 독스트링 글 그대로입니다.
출력 줄 `입력 형식의 종류: dict`로, 입력 형식은 딕셔너리입니다.
라벨 `입력 형식:` 뒤의 글은 01절 4절에서 본 서버의 입력 형식과 글자까지 같습니다.

Ch 19 02절은 입력 형식을 양식 클래스 `BaseModel`로 적었습니다.
바뀐 MCP 도구는 서버가 보낸 입력 형식을 딕셔너리 그대로 들고 있습니다.
모델에게 보내는 도구 정의에 이 딕셔너리가 어떻게 실리는지는 05절에서 봅니다.

다음 셀은 도구가 내놓는 값의 모양과, 도구에 붙은 서버 정보를 봅니다.
속성 `response_format`은 도구가 내놓는 값을 어떤 모양으로 나눌지 정합니다.
속성 `metadata`는 도구에 붙여 둔 정보를 담는 딕셔너리입니다."""),
        code(META),
        md("""**결과 읽기** — 출력 줄 `내놓는 값의 모양: content_and_artifact`가 보입니다.
도구가 내놓는 값을 모델에게 보낼 내용과, 메시지에만 붙여 둘 아티팩트로 나눈다는 뜻입니다.
라벨 `서버 정보:` 뒤에 서버 이름 `교육센터 자료실`과 판 `4.0.3`이 보입니다.
출력 줄 `꼬리표: ['public', 'read']`는 서버 파일이 도구를 붙이며 적은 꼬리표입니다.
02절 6절에서 본 꼬리표와 같습니다.

## 3. 비동기로만 부르는 도구

Ch 19 01절에서는 도구의 메서드 `invoke`에 인자 딕셔너리를 넣어 불렀습니다.
바뀐 MCP 도구도 같은 방법으로 불러 봅니다.
오류가 나면 이름 `NotImplementedError`만 받아, 셀이 멈추지 않게 합니다.
실행 전에 예상해 봅니다.
이 도구도 `invoke`로 부를 수 있을까요?"""),
        code(INVOKE_ERR),
        md("""**결과 읽기** — 받은 것은 `NotImplementedError`이고, 받은 글은 `StructuredTool does not support sync invocation.`입니다.
받은 글의 sync invocation은 비동기가 아닌 보통 부르기를 뜻합니다.
이 도구는 보통 부르기로는 쓸 수 없다는 뜻입니다.

바뀐 MCP 도구는 서버와 메시지를 주고받는 비동기 함수 하나만 몸통으로 들고 있습니다.
그래서 메서드 `ainvoke`로 불러야 하고, `ainvoke`는 `invoke`의 비동기 판입니다.
01절에서 본 것처럼, 노트북 셀 맨 위에서는 `await`를 붙여 끝날 때까지 기다립니다.
다음 셀은 같은 인자를 `ainvoke`에 넘겨 부르고, 부른 뒤 자식 프로세스 수를 셉니다."""),
        code(AINVOKE),
        md("""**결과 읽기** — 출력 줄 `받은 값의 종류: list`와 `내용 블록 수: 1`이 보입니다.
라벨 `첫 블록의 글:` 뒤의 글은 서버 파일의 운영 규정 글 그대로입니다.
출력 줄 `부른 뒤 자식 프로세스 수: 0`으로, 이번 호출이 띄운 서버도 끝났습니다.
앞 셀까지 0이었으니, 부를 때 서버가 새로 떠서 답하고 끝났습니다.

인자 딕셔너리로 부르면, 도구는 모델에게 보낼 내용만 내놓습니다.
그 내용은 내용 블록의 목록이고, 블록 하나는 종류와 글을 담은 딕셔너리입니다.
라벨 `첫 블록의 키:` 뒤의 `id`는 LangChain이 블록마다 새로 붙이는 번호라, 실행마다 값이 바뀝니다.
그래서 이 절은 블록 전체 대신 글 `text`만 출력합니다.

LangChain 문서는 바꾼 도구가 부를 때마다 연결을 열고 닫는다고 적습니다.
연결 블록 `async with adapter:` 안에서 부르면, 블록이 연 연결을 그대로 씁니다.
다음 셀은 블록 안에서 같은 도구를 부르고, 부르기 전과 뒤의 자식 프로세스를 견줍니다.
속성 `pid`는 운영체제가 프로세스마다 붙인 번호입니다.
번호는 실행마다 달라 출력하지 않고, 두 번호가 같은지만 봅니다."""),
        code(IN_BLOCK),
        md("""**결과 읽기** — 출력 줄 `블록 안, 부르기 전 자식 프로세스 수: 1`과 `블록 안, 부른 뒤 자식 프로세스 수: 1`이 보입니다.
출력 줄 `같은 프로세스인가: True`로, 블록이 띄운 서버 하나가 도구 호출을 받았습니다.
출력 줄 `블록을 벗어난 뒤 자식 프로세스 수: 0`으로, 블록을 벗어나자 그 서버도 끝났습니다.

블록 밖에서는 부를 때마다 서버가 떴다가 끝났고, 블록 안에서는 서버 하나를 이어 썼습니다.
어느 쪽이든 칸 `keep_alive`가 `False`라, 연결이 모두 닫히면 남는 서버가 없습니다.

## 4. 도구 실행 노드에 손으로 만든 요청 넣기

Ch 20 01절은 모델 대신 도구 호출 요청을 담은 응답을 손으로 만들어 그래프를 살폈습니다.
이 절도 같은 방법으로, 바뀐 MCP 도구를 도구 실행 노드 `ToolNode`에 넣어 봅니다.
그래프의 상태 형식은 LangGraph가 미리 만들어 둔 `MessagesState`를 씁니다.
Ch 21 03절의 `AgentState`보다 칸이 적어, 칸 `messages` 하나만 둔 형식입니다.
그 칸에는 Ch 13 04절의 `add_messages` 규칙이 붙어 있습니다.

다음 셀은 도구 실행 노드 하나만 둔 그래프를 만듭니다."""),
        code(GRAPH),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['tools']`가 보입니다.
Ch 20 01절과 달리 모델 노드가 없고, 시작 엣지와 끝 엣지 사이에 도구 실행 노드만 있습니다.

다음 셀은 모델 대신 도구 호출 요청 둘을 담은 응답 하나를 손으로 만듭니다.
첫 요청에는 주제어 운영을, 둘째 요청에는 서버 규정에 없는 주제어 주차를 넣습니다.
호출 ID `call_a`·`call_b`는 이 셀에서 정한 글입니다."""),
        code(HAND),
        md("""**결과 읽기** — 출력 줄 `도구 호출 요청: ['lookup_policy', 'lookup_policy']`가 보입니다.
Ch 19 04절 함수 `tool_call_names`로 이름만 모았고, 같은 도구를 두 번 부르는 응답입니다.

다음 셀은 이 응답 하나를 메시지 칸에 넣어 그래프를 실행합니다.
도구가 비동기로만 불리므로, 그래프도 `invoke` 대신 `ainvoke`로 실행합니다.
실행 전에 예상해 봅니다.
서버 규정에 없는 주제어를 넣은 요청은 어떻게 될까요?"""),
        code(RUN_GRAPH),
        md("""**결과 읽기** — 라벨 `메시지 종류:` 줄 아래에 `AIMessage` 하나와 `ToolMessage` 둘이 차례로 보입니다.
도구 실행 노드가 요청마다 도구 메시지 하나를 이어 붙였습니다.
출력 줄 `실행 뒤 자식 프로세스 수: 0`으로, 두 요청을 처리한 서버도 모두 끝났습니다.

다음 셀은 도구 메시지마다 호출 ID·결과 상태·글을 봅니다.
속성 `text`는 메시지 내용 가운데 글만 이어 붙여 내놓습니다.
내용 블록의 `id`는 실행마다 바뀌므로, 내용 전체 대신 이 속성을 출력합니다."""),
        code(TOOL_MSGS),
        md("""**결과 읽기** — 출력 줄 `호출 ID: call_a | 결과 상태: success`와 `호출 ID: call_b | 결과 상태: error`가 보입니다.
첫 메시지의 글은 운영 규정 글이고, 둘째 메시지의 글은 서버가 낸 오류 글입니다.
오류 글 `Error calling tool 'lookup_policy': topic은 대출, 운영, 연체 중 하나여야 합니다.`는 02절 6절에서 본 글과 같습니다.

서버 쪽 도구가 오류를 냈어도 셀은 멈추지 않았습니다.
Ch 19 06절에서는 도구 속성 `handle_tool_error`를 두어 오류를 결과 상태 `error`의 도구 메시지로 받았습니다.
클래스 `MCPAdapter`가 바꾼 도구에는 이 속성이 미리 채워져 있습니다.
그래서 서버의 오류 글이 도구 메시지에 담겨, 에이전트라면 다음 모델 요청에 실립니다.

도구 메시지에는 내용 말고도 아티팩트(artifact)라는 칸이 있습니다.
다음 셀은 두 도구 메시지의 아티팩트를 봅니다."""),
        code(ARTIFACT),
        md("""**결과 읽기** — 라벨 `성공한 메시지의 아티팩트:` 뒤에 딕셔너리 하나가 보입니다.
칸 `structured_content` 안의 칸 `result`에 운영 규정 글이 들어 있습니다.
출력 줄 `오류 메시지의 아티팩트: None`으로, 오류 메시지에는 아티팩트가 없습니다.

02절 6절에서 본 서버 파일 도구의 출력 형식이 바로 이 칸 `result`입니다.
패키지 langchain-core의 `ToolMessage` 설명은 아티팩트를 모델에게 보내지 않는 값이라고 적습니다.

## 5. 에이전트에 MCP 도구 붙이기

이제 바꾼 도구를 에이전트에 붙이고, 실제 모델로 한 번 실행합니다.
Ch 21 01절처럼 함수 `create_agent`에 모델 객체와 도구 목록을 넘깁니다.
Ch 26·27처럼 모델을 부르는 에이전트에는 Ch 22 04절의 호출 한도를 함께 붙입니다.
다음 셀은 invoke 한 번에 모델 요청을 3번까지만 허락하는 호출 한도를 만듭니다."""),
        code(LIMIT),
        md("""**결과 읽기** — 출력 줄 `한 번 실행의 요청 한도: 3`과 `한도에 닿으면: end`가 보입니다.
한도에 닿으면 모델을 더 부르지 않고 실행을 끝낸다는 뜻입니다.
이 한도는 `ainvoke`로 실행해도 실행 한 번마다 셉니다.

다음 셀은 모델 객체·MCP 도구·시스템 메시지 글·호출 한도로 에이전트를 만듭니다.
시스템 메시지 글에는 규정 질문에 도구로 규정을 찾으라는 규칙을 적습니다.
이 셀은 에이전트를 만들기만 하고, 모델 요청은 보내지 않습니다."""),
        code(AGENT),
        md("""**결과 읽기** — 라벨 `노드:` 뒤에 노드 여섯의 이름이 보입니다.
모델 노드 `model`과 도구 실행 노드 `tools` 옆에, 호출 한도의 훅 노드 둘이 들어 있습니다.

다음 셀은 질문 한 줄을 넣어 에이전트를 한 번 실행합니다.
에이전트의 도구가 비동기로만 불리므로, 에이전트도 `ainvoke`로 실행합니다.
실행 전에 예상해 봅니다.
모델은 MCP 도구를 부를까요, 그리고 모델 요청은 몇 번일까요?"""),
        code(RUN),
        md("""**결과 읽기** — 출력 줄 `결과 메시지 수: 4`와 `실행 뒤 자식 프로세스 수: 0`이 보입니다.
에이전트가 도구를 부르는 동안 띄운 서버도, 실행이 끝났을 때 남아 있지 않았습니다.

결과 메시지 수는 모델이 도구를 몇 번 부르느냐에 따라 달라질 수 있는 값입니다.
노트북 밖에서 같은 실행을 다섯 번 보냈을 때도 결과 메시지는 넷이었습니다.

다음 셀은 결과 메시지를 차례로 보며 종류와 도구 호출 요청 이름, 결과 상태를 출력합니다.
Ch 19 06절 함수 `show_messages`는 도구 메시지의 내용을 통째로 출력합니다.
MCP 도구 메시지의 내용에는 실행마다 바뀌는 `id`가 들어 있어, 이 셀은 내용을 빼고 출력합니다."""),
        code(KINDS),
        md("""**결과 읽기** — 출력 줄 `AIMessage | 도구 호출 요청: ['lookup_policy']` 다음에 `ToolMessage | 결과 상태: success`가 보입니다.
마지막 줄은 `AIMessage | 도구 호출 요청: []`입니다.
모델이 첫 응답에서 MCP 도구를 한 번 요청했고, 도구 실행 노드가 그 도구를 불렀습니다.
도구 메시지를 받은 모델은 둘째 응답에서 도구를 더 요청하지 않았습니다.

어느 도구를 몇 번 부를지는 모델이 고르는 값입니다.
노트북 밖에서 같은 실행을 다섯 번 보냈을 때 다섯 번 모두 이 차례였습니다.

다음 셀은 모델이 쓴 도구 인자와, 도구 메시지의 글을 봅니다.
인자는 모델이 쓴 값이라 실행마다 달라질 수 있습니다."""),
        code(ARGS),
        md("""**결과 읽기** — 라벨 `도구 인자:` 줄과 `도구 메시지 글:` 줄이 차례로 보입니다.
도구 메시지 글은 서버가 인자로 받은 주제어의 규정 글입니다.

이번 실행에서는 인자가 `{'topic': '운영'}`이었고, 받은 글은 운영 규정 글이었습니다.
노트북 밖 다섯 번과 두 커널 실행에서도 인자는 같았지만, 모델이 쓴 값이라 결론에는 쓰지 않습니다.

Ch 26·27에서는 모델 요청 수를 「도구를 요청한 응답 수 + 1」로 셌습니다.
모델은 도구를 요청할 때마다 응답을 하나 쓰고, 마지막에 답을 쓰는 응답이 하나 더 있기 때문입니다.
다음 셀은 도구를 요청한 응답 수를 세고, Ch 19 05절 함수 `sum_usage`로 센 요청 수와 견줍니다."""),
        code(COUNT),
        md("""**결과 읽기** — 출력 줄 `도구를 요청한 응답 수: 1`과 `모델 요청 수: 2`가 보입니다.
출력 줄 `모델 요청 수 = 도구를 요청한 응답 수 + 1: True`로, 셈이 맞았습니다.
요청 수 2는 호출 한도 3 안에 들었습니다.

도구를 요청한 응답 수는 모델이 고르는 값이라 실행마다 달라질 수 있습니다.
셈은 호출 한도에 닿지 않고 답으로 끝난 실행에서 맞습니다.

다음 셀은 모델이 쓴 마지막 답 글을 봅니다.
답 글은 실행마다 달라질 수 있는 값입니다."""),
        code(ANSWER),
        md("""**결과 읽기** — 라벨 `마지막 답 글:` 줄 아래에 모델이 쓴 답이 보입니다.
시스템 메시지 글은 찾은 글만 근거로 한국어 한 문장으로 답하라고 적었습니다.

이번 실행에서는 답 글이 「토요일은 17:00까지 운영합니다」였습니다.
도구 메시지 글에 적힌 토요일의 끝 시각 17:00과 같은 시각입니다.
노트북 밖 다섯 번 가운데 한 번은 「교육센터 자료실은」으로 시작하는 다른 문장이었습니다.

다음 셀은 이번 실행의 입력·출력 토큰과 예상 비용을 봅니다.
요금은 Ch 6 06절처럼 2026-09-17 요금표의 100만 토큰당 달러입니다.
예상 비용은 요금표로 어림한 값이고, 청구 금액이 아닙니다."""),
        code(COST),
        md("""**결과 읽기** — 라벨 `입력 토큰:`과 `출력 토큰:` 뒤에 이번 실행의 토큰 수가 보입니다.
라벨 `예상 비용(달러):` 뒤에는 요금표로 어림한 비용이 보입니다.
함수 `sum_usage`가 낸 딕셔너리에는 할인되는 입력 토큰 칸이 없어, 입력 토큰을 모두 입력 요금으로 셌습니다.

이번 실행에서는 입력 토큰 430, 출력 토큰 32, 예상 비용 0.000467달러였습니다.
노트북 밖 다섯 번에서 입력 토큰은 모두 430이었고, 출력 토큰은 32와 37로 갈렸습니다.
출력 토큰과 비용은 실행마다 달라질 수 있고, 입력 토큰은 이 절의 주제가 아니라 결론에 쓰지 않습니다.
첫 요청의 입력 토큰은 05절에서 조건을 바꿔 가며 셉니다.

## 정리

1. 클래스 `MCPAdapter`가 바꾼 도구는 `StructuredTool`이고, 입력 형식은 서버가 보낸 딕셔너리였습니다.
2. 이 도구는 `ainvoke`로만 불렸고, 칸 `keep_alive`가 `False`면 부른 뒤 서버가 남지 않았습니다.
3. 서버 오류는 결과 상태 `error`의 도구 메시지가 되었고, 모델 요청 수는 「도구를 요청한 응답 수 + 1」이었습니다.

05절에서는 도구 정의가 모델의 첫 요청 입력 토큰에 얼마나 더해지는지 셉니다."""),
    ]


# ---------------------------------------------------------------- _src 본문
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
L_CH13_04 = "../../part4/ch13-langgraph-basics/04-add_messages-리듀서.html"
L_CH19_01 = "../../part5/ch19-model-tools/01-tool과-Ch4-함수-재사용.html"
L_CH19_02 = "../../part5/ch19-model-tools/02-Pydantic-인자와-반환-스키마.html"
L_CH19_05 = "../../part5/ch19-model-tools/05-bind_tools와-병렬-호출.html"
L_CH19_06 = "../../part5/ch19-model-tools/06-오류와-읽기-쓰기-분리.html"
L_CH20_01 = "../../part5/ch20-tool-node/01-ToolNode와-tools-condition.html"
L_CH21_01 = "../ch21-create-agent/01-create-agent와-ReAct-루프.html"
L_CH22_04 = "../ch22-middleware/04-호출-한도와-재시도-폴백.html"
L_CH27_02 = "../ch27-deepagents/02-create-deep-agent와-도구.html"
L_01 = "01-MCP-구조와-capability-협상.html"
L_02 = "02-FastMCP-로컬-서버-제작.html"
L_03 = "03-stdio와-원격-전송-권한-경계.html"
L_05 = "05-도구-정의와-첫-호출-토큰.html"

TERM_ROWS = [
    ("LangChain 도구로 바꾸기(변환)", "서버가 알린 MCP 도구 정의를 LangChain 도구 객체로 옮겨 담는 일입니다. 모양이 다른 두 도킹 자리 사이에 이음 부품을 끼우는 일과 같습니다. 이 절에서는 메서드 <code>list_tools</code>가 서버의 <code>lookup_policy</code>를 종류 <code>StructuredTool</code>의 도구로 바꿉니다."),
    ("비동기로 부르기(<code>ainvoke</code>)", "메서드 <code>invoke</code>의 비동기 판으로, 끝날 때까지 <code>await</code>로 기다리며 부르는 메서드입니다. 주문한 뒤 진동벨이 울릴 때 음식을 받으러 가는 것과 같습니다. 이 절에서는 MCP 도구·도구 실행 그래프·에이전트를 모두 <code>await</code>와 <code>ainvoke</code>로 부릅니다."),
    ("내용 블록(content block)", "메시지 내용을 종류와 값으로 나눠 담은 딕셔너리 하나입니다. 상자 안을 나눈 칸 하나에 물건 하나를 넣는 것과 같습니다. 이 절의 도구 메시지 내용은 종류 <code>text</code>의 블록 하나를 담은 목록입니다."),
    ("아티팩트(artifact)", "도구 메시지에 붙여 두되 모델에게는 보내지 않는 값입니다. 책을 빌릴 때 책과 따로 남겨 두는 대출 기록과 같습니다. 이 절에서는 칸 <code>structured_content</code>에 서버가 낸 구조화된 결과가 들어 있습니다."),
]

VALUE_ROWS = [
    ("도구 종류 · 입력 형식", "<code>StructuredTool</code> · <code>dict</code>", "설치판 <code>MCPAdapter</code>가 정함"),
    ("<code>invoke</code>로 부르기", "<code>NotImplementedError</code>", "비동기 함수만 둔 도구"),
    ("블록 밖에서 부른 뒤 자식 프로세스", "<code>0</code>", "칸 <code>keep_alive</code>가 <code>False</code>"),
    ("손으로 만든 요청 둘의 결과 상태", "<code>success</code> · <code>error</code>", "서버 규정에 있는 주제어인가"),
    ("에이전트가 요청한 도구", "<code>lookup_policy</code> 한 번", "모델이 고름(노트북 밖 다섯 번·두 커널 같음)"),
    ("모델 요청 수", "<code>2</code> = 도구를 요청한 응답 수 <code>1</code> + 1", "셈(한도에 닿지 않은 실행)"),
    ("입력 토큰(실행 합)", "<code>430</code>", "서비스가 센 값 — 노트북 밖 다섯 번·두 커널 같음, 이 절의 주제가 아니라 결론에 쓰지 않고 05절에서 조건을 바꿔 셈"),
    ("도구 인자 · 답 글 · 출력 토큰 · 예상 비용", "이번 실행에서는 <code>{'topic': '운영'}</code> · 17:00이 든 답 한 문장 · 출력 32 토큰 · 0.000467달러", "모델·서비스 쪽 값이라 결론에 쓰지 않음"),
]

LOOK_B5 = "노트북 2절에서 <code>도구 종류: StructuredTool</code>과 <code>입력 형식의 종류: dict</code>를 봅니다. 3절에서 <code>받은 것: NotImplementedError</code>와 <code>부른 뒤 자식 프로세스 수: 0</code>을 확인합니다. 블록 안에서는 <code>같은 프로세스인가: True</code>인지, 블록 뒤에는 0인지 봅니다."
LOOK_B6 = "4절에서 <code>호출 ID: call_b | 결과 상태: error</code>와 서버 오류 글을 찾습니다. 5절에서 <code>AIMessage | 도구 호출 요청: ['lookup_policy']</code>와 <code>ToolMessage | 결과 상태: success</code>를 봅니다. 마지막으로 <code>모델 요청 수 = 도구를 요청한 응답 수 + 1: True</code>와 <code>실행 뒤 자식 프로세스 수: 0</code>을 확인합니다."


def src_html() -> str:
    terms = table_html(["말", "뜻"], TERM_ROWS)
    values = table_html(["본 것", "이번 출력", "무엇이 정했나"], VALUE_ROWS)
    return """<!--meta: 강의 1h | 실습 2h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 4 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>클래스 <code>MCPAdapter</code>로 MCP 도구를 LangChain 도구로 바꾸고, 바뀐 도구의 모양을 읽을 수 있습니다.</li>
<li>MCP 도구를 <code>ainvoke</code>로만 부르는 까닭과, 부를 때 서버 프로세스가 떴다가 끝나는 것을 설명할 수 있습니다.</li>
<li>바꾼 도구를 도구 실행 노드와 에이전트에 붙이고, 결과 상태와 모델 요청 수를 셀 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_03 + """\">03절</a>까지는 FastMCP의 클래스 <code>Client</code>로 서버의 도구를 직접 불렀습니다. 모델이 도구를 고르게 하려면, 그 도구를 Ch 19~21에서 쓴 LangChain 도구로 알려야 합니다. 서버의 도구를 손으로 다시 적지 않고, 서버가 알린 목록을 그대로 LangChain 도구로 바꾸면 됩니다. 이 절은 그 바꾸는 일과, 바꾼 도구를 에이전트에 붙이는 일을 봅니다.</p><p>제목의 LangChain MCP는 langchain 1.4.0에 든 모듈 <code>langchain.mcp</code>입니다. 그 안의 클래스 <code>MCPAdapter</code>가 MCP 서버에 붙어 도구를 바꿉니다. 바꾼 도구는 서버와 메시지를 주고받아야 해서, 부르는 방법이 직접 만든 도구와 다릅니다. 도구를 부를 때 서버 프로세스가 언제 뜨고 끝나는지도 함께 봅니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_CH19_01 + """\">Ch 19 01절</a>에서는 <code>@tool</code> 줄로 도구를 만들었고, 그 종류는 <code>StructuredTool</code>이었습니다. 도구는 메서드 <code>invoke</code>에 인자 딕셔너리를 넣어 불렀습니다. <a href=\"""" + L_CH19_02 + """\">02절</a>은 입력 형식을 양식 클래스 <code>BaseModel</code>로 적었습니다. <a href=\"""" + L_CH19_05 + """\">05절</a>은 도구 호출 요청으로 도구를 불러 <code>ToolMessage</code>를 받았습니다. <a href=\"""" + L_CH19_06 + """\">06절</a>은 도구 속성 <code>handle_tool_error</code>로 오류를 결과 상태 <code>error</code>의 도구 메시지로 받았습니다.</p><p><a href=\"""" + L_CH20_01 + """\">Ch 20 01절</a>에서는 모델 대신 도구 호출 요청을 담은 응답을 손으로 만들어 도구 실행 노드 <code>ToolNode</code>를 살폈습니다. <a href=\"""" + L_CH21_01 + """\">Ch 21 01절</a>에서는 함수 <code>create_agent</code>에 모델 객체와 도구 목록을 넘겨 에이전트를 만들었습니다. <a href=\"""" + L_CH22_04 + """\">Ch 22 04절</a>의 호출 한도는 Ch 26·27에서 모델을 부르는 에이전트마다 붙였습니다. <a href=\"""" + L_CH27_02 + """\">Ch 27 02절</a>은 모델 요청 수를 「도구를 요청한 응답 수 + 1」로 셌습니다.</p><p><a href=\"""" + L_CH02_12 + """\">Ch 2 12절</a>에서는 <code>async def</code>와 <code>await</code>로 기다리는 일을 적었습니다. <a href=\"""" + L_01 + """\">01절</a>은 셀 맨 위의 <code>async with</code>와 <code>await</code>, 함수 <code>names_of</code>, 서버의 입력 형식을 보였습니다. <a href=\"""" + L_02 + """\">02절</a> 6절은 서버 파일 도구의 꼬리표·출력 형식·오류 글을 보였습니다. <a href=\"""" + L_03 + """\">03절</a>은 함수 <code>stdio_config</code>로 서버 파일을 자식 프로세스로 띄우고, 연결을 닫으면 서버도 끝나는 것을 셌습니다. 이 절은 03절의 <code>Client</code>로 부르던 도구를 LangChain 도구로 바꿔, 모델에게 알립니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>우주 정거장의 짐 모듈 하나를 우주선 조종석에서 쓰려 한다고 합시다. 조종석 캡슐의 도킹 구멍은 둥글고, 짐 모듈의 도킹 자리는 네모라서 그대로는 맞지 않습니다. 한쪽 끝은 둥글고 다른 쪽 끝은 네모인 이음 부품을 끼우면, 두 쪽이 한 줄로 이어집니다.</p><p>네모 자리의 짐 모듈이 MCP 서버의 도구이고, 둥근 구멍의 조종석이 LangChain 에이전트입니다. 이음 부품이 클래스 <code>MCPAdapter</code>이고, 부품을 끼운 모듈이 LangChain 도구로 바뀐 MCP 도구입니다.</p><p>비유와 다른 점도 있습니다. 실제 MCP 도구는 한 번 끼워 두면 계속 붙어 있는 모듈이 아닙니다. 이 절의 설정에서는 도구를 부를 때마다 서버를 띄워 연결하고, 답을 받으면 연결과 서버를 닫았습니다.</p>
""" + illustration_block() + """<h3>LangChain 도구로 바꾸기</h3><p>클래스 <code>MCPAdapter</code>는 안에 FastMCP의 <code>Client</code>를 만들어 서버에 붙습니다. 메서드 <code>list_tools</code>는 서버의 도구 목록을 받아, 도구마다 LangChain 도구 하나로 바꿉니다. 이름과 설명은 서버가 알린 글 그대로이고, 입력 형식은 서버가 보낸 딕셔너리 그대로입니다. 도구의 몸통은 서버에 도구를 부르는 요청을 보내는 비동기 함수입니다.</p>
""" + terms + """
<p>새 말을 이 절 코드에서 보면 이렇습니다. 바꾸기는 <code>도구 종류: StructuredTool</code>로, 비동기로 부르기는 <code>await policy_tool.ainvoke(…)</code>로 보입니다. 내용 블록은 <code>내용 블록 수: 1</code>로, 아티팩트는 칸 <code>structured_content</code>로 출력에 보입니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>비동기로만 부르는 도구</h3><p>바뀐 MCP 도구는 비동기 함수 하나만 몸통으로 들고 있습니다. 그래서 메서드 <code>invoke</code>로 부르면 오류 <code>NotImplementedError</code>가 납니다. 도구 실행 그래프와 에이전트도 이 도구를 품으면 <code>ainvoke</code>로 실행해야 합니다. 메서드 <code>ainvoke</code>는 <code>invoke</code>의 비동기 판이고, 노트북 셀 맨 위에서는 <code>await</code>를 붙여 기다립니다.</p><p>도구가 내놓는 값의 모양은 <code>content_and_artifact</code>입니다. 모델에게 보낼 내용은 내용 블록의 목록이고, 서버의 구조화된 결과는 아티팩트로 따로 붙습니다. 내용 블록에는 LangChain이 붙인 <code>id</code>가 있어 실행마다 바뀌므로, 이 절은 글만 출력합니다.</p>
<h3>부를 때마다 여는 연결</h3><p>바뀐 도구는 서버에 붙는 클라이언트를 쥐고 있어, 연결 블록 밖에서도 부를 수 있습니다. 부를 때마다 연결을 열고, 도구를 부르는 요청 하나를 보낸 뒤 연결을 닫습니다. 03절 설정처럼 칸 <code>keep_alive</code>가 <code>False</code>면, 연결을 닫을 때 서버 프로세스도 끝납니다. 연결 블록 <code>async with adapter:</code> 안에서 부르면, 블록이 띄운 서버 하나를 이어 씁니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 03절 설정을 <code>MCPAdapter</code>에 넘겨 도구를 바꾸고, 바뀐 도구의 모양을 봅니다. 3절은 <code>invoke</code>와 <code>ainvoke</code>로 불러 보고, 연결 블록 밖과 안에서 자식 프로세스를 셉니다. 4절은 손으로 만든 도구 호출 요청으로 도구 실행 노드를 실행합니다. 5절은 에이전트를 실제 모델로 한 번 실행하고, 모델 요청 수를 셉니다.</p><p>모델 요청은 5절에서만 나가고, 에이전트가 도구를 한 번 부르면 2번입니다. 호출 한도 3을 붙였고, 요금표로 어림한 예상 비용은 0.001달러 아래입니다. 노트북이 쓰는 파일은 없고, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>노트북 4절은 모델 없이 손으로 만든 요청 둘을 도구 실행 노드에 넣었습니다. 주제어 운영을 넣은 요청은 결과 상태 <code>success</code>의 도구 메시지가 되었습니다. 서버 규정에 없는 주차를 넣은 요청은 셀을 멈추지 않고, 서버 오류 글을 담은 <code>error</code> 도구 메시지가 되었습니다. 두 요청을 처리한 서버는 실행이 끝났을 때 남아 있지 않았습니다.</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>노트북 5절은 같은 도구를 에이전트에 붙여 실제 모델로 한 번 실행했습니다. 모델은 첫 응답에서 도구 <code>lookup_policy</code>를 한 번 요청했고, 도구 메시지를 받은 뒤 답을 썼습니다. 그래서 모델 요청 수는 도구를 요청한 응답 수 1에 1을 더한 2였습니다. 어느 도구를 몇 번 부를지는 모델이 고르는 값이라, 결론은 요청 수 셈에 둡니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + values + """
<p>표의 위 넷은 코드와 서버가 정하는 값이라, 다시 실행해도 같아야 합니다. 에이전트가 요청한 도구는 모델이 고른 값이고, 노트북 밖에서 다섯 번 보냈을 때도 같았습니다. 입력 토큰은 서비스가 센 값이지만, 노트북 밖 다섯 번과 두 커널에서 모두 430이었습니다. 이 절의 주제가 아니라 결론에는 쓰지 않고, 05절에서 조건을 바꿔 가며 셉니다. 맨 아래 줄은 모델이 쓴 글과 서비스가 센 값이고, 실행마다 달라질 수 있어 결론에 쓰지 않습니다.</p><p>새 커널로 두 번 실행해 견주자, 코드 셀 스물다섯의 출력이 셀마다 모두 같았습니다. 모델이 쓴 인자·답 글·토큰·예상 비용이 찍힌 셀도 이번 두 번에서는 같았지만, 모델 출력이라 결론에는 쓰지 않습니다.</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>모듈 <code>langchain.mcp</code>는 langchain 1.4.0에서 베타이고, 가져올 때 경고 <code>LangChainBetaWarning</code>을 한 번 냅니다. 설치판 소스 <code>langchain/mcp/__init__.py</code> 26~30행이 그 자리입니다. 노트북 셀에 찍히는 경고 줄에는 커널 임시 파일 이름이 들어가, 이 절은 그 경고 한 종류만 껐습니다. 같은 파일 9~12행의 설명도 이 가져오기 줄과 같은 줄로 끄는 방법을 적습니다.</li><li>LangChain MCP 문서의 예는 <code>Path("weather_server.py")</code>처럼 서버 파일을 <code>Path</code>로 넘기고, 어댑터 하나에 자식 프로세스 하나라고 적습니다. 그렇게 넘기면 칸 <code>keep_alive</code>가 기본값 <code>True</code>가 되어, 목록을 받은 뒤에도 자식 프로세스 하나가 남았습니다. 시작 안내와 새 판 확인 글도 표준 오류에 찍혔습니다. 노트북 밖의 작은 스크립트로 확인했고, 이 노트북에서는 실행하지 않았습니다. 이 절은 03절 규칙대로 설정 딕셔너리를 넘겼습니다.</li><li>LangChain 문서의 연결 안내는 바꾼 도구가 부를 때마다 연결을 열고 닫는다고 적습니다. 에이전트를 부르는 동안 연결 블록을 열어 두면 같은 연결을 이어 쓴다고도 적습니다. 노트북 밖에서 블록 밖 호출 두 번의 자식 프로세스 번호를 모아 보니 서로 다른 둘이었습니다.</li><li>설치판 <code>MCPAdapter</code>는 글자 대상을 <code>http</code>·<code>https</code> 주소로만 받습니다. 서버 파일 이름을 글자로 넘기면 오류 <code>ValueError</code>를 냅니다. 설치판 소스 <code>langchain/mcp/adapter.py</code> 84~122행으로만 확인했고, 이 노트북에서는 실행하지 않았습니다.</li><li>도구 실행 그래프를 <code>ainvoke</code> 대신 <code>invoke</code>로 실행해도 같은 오류 <code>NotImplementedError</code>가 났습니다. 노트북 밖에서 확인했습니다.</li><li>서버는 도구 오류를 기록 수준 ERROR로 표준 오류에 씁니다. 03절의 기록 수준 <code>WARNING</code>보다 높아 이 기록은 막히지 않습니다. 교재 실행에서는 이 기록이 셀 출력이 아니라 커널을 띄운 쪽의 표준 오류로 갔습니다. 설치판 fastmcp 4.0.3 <code>server/server.py</code> 1541행이 그 자리입니다.</li><li>설치판 <code>as_langchain_tool</code>은 도구를 만들 때 도구 속성 <code>handle_tool_error</code>를 채웁니다. 소스 <code>langchain/mcp/tools.py</code> 104~117행과 274~282행입니다. 서버와의 연결이 끊기는 오류는 도구 메시지가 되지 않고 셀을 멈춥니다. 이 절에서는 그런 오류를 실행하지 않았습니다.</li><li>인터넷 예제에 많은 패키지 <code>langchain-mcp-adapters</code>는 이 실습 폴더 잠금에 없습니다. 그 패키지를 가져오면 오류 <code>ModuleNotFoundError</code>가 납니다. LangChain 옮기기 안내는 <code>MultiServerMCPClient</code>를 <code>MCPAdapter</code>로, <code>load_mcp_tools()</code>를 <code>list_tools()</code>로 바꾸라고 적습니다. 도구를 가로채던 기능은 Ch 22의 <code>@wrap_tool_call</code> 훅으로 옮기라고 적고, 이 절에서는 실행하지 않았습니다.</li><li>클래스 <code>MCPAdapter</code>는 서버가 사람에게 되묻는 요청을 LangGraph의 멈춤 표시로 받게 준비합니다. 설치판 소스 <code>langchain/mcp/adapter.py</code> 146~151행과 174~200행입니다. 이 절의 서버는 되묻지 않아, 이 동작은 실행하지 않았습니다.</li><li>노트북 밖에서 5절과 같은 실행을 다섯 번 보냈습니다. 요청한 도구·결과 메시지 차례·요청 수는 다섯 번 모두 같았습니다. 마지막 답 글은 다섯 번 가운데 한 번 달랐고, 출력 토큰도 그 한 번만 달랐습니다. 같은 요청도 실행한 때에 따라 모델이 쓰는 글과 토큰이 달라질 수 있습니다.</li><li>이 에이전트는 서브에이전트가 없어, 실행 한 번의 모델 요청은 호출 한도 3을 넘지 않습니다. 예상 비용은 2026-09-17 요금표로 어림한 값이고, 청구 금액이 아닙니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 걸린 시간은 재지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>클래스 <code>MCPAdapter</code>가 바꾼 도구는 <code>StructuredTool</code>이고, 입력 형식은 서버가 보낸 딕셔너리였습니다.</li><li>이 도구는 <code>ainvoke</code>로만 불렸고, 칸 <code>keep_alive</code>가 <code>False</code>면 부른 뒤 서버가 남지 않았습니다.</li><li>서버 오류는 결과 상태 <code>error</code>의 도구 메시지가 되었고, 모델 요청 수는 「도구를 요청한 응답 수 + 1」이었습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_05 + """\">05절</a>에서는 도구 정의가 모델의 첫 요청 입력 토큰에 얼마나 더해지는지 셉니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 클래스 <code>MCPAdapter</code>가 바꾼 도구를 메서드 <code>invoke</code>로 부르면 어떻게 되었나요?</p><p class="quiz-a">오류 <code>NotImplementedError</code>가 났습니다. 이 도구는 서버와 메시지를 주고받는 비동기 함수만 몸통으로 들고 있어, <code>ainvoke</code>로 불러야 합니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">2. 칸 <code>keep_alive</code>가 <code>False</code>인 설정에서, 연결 블록 밖에서 도구를 부른 뒤 자식 프로세스 수는 얼마였나요?</p><p class="quiz-a">0이었습니다. 부를 때 서버가 떠서 답하고, 연결을 닫을 때 끝났습니다. 연결 블록 안에서는 블록이 띄운 서버 하나를 이어 썼습니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">3. 도구 실행 노드에 서버 규정에 없는 주제어를 넣은 요청은 어떻게 되었나요?</p><p class="quiz-a">셀이 멈추지 않고, 결과 상태 <code>error</code>의 도구 메시지가 되었습니다. 그 글은 서버가 낸 오류 글이었습니다. 바꾼 도구에 도구 속성 <code>handle_tool_error</code>가 채워져 있기 때문입니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">4. 에이전트가 MCP 도구를 두 번 요청한 뒤 답했다면, 모델 요청 수는 몇 번일까요?</p><p class="quiz-a">3번입니다. 도구를 요청한 응답 둘에 답을 쓴 응답 하나가 더해집니다. 호출 한도 3 안이라 실행이 끝까지 갑니다. 틀렸다면 노트북 5절의 셈을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langchain/mcp">LangChain MCP</a></div>확인 2026-09-28 · 패키지 <code>langchain[mcp]</code> 1.4.0 이상과 클래스 <code>MCPAdapter</code>를 적습니다. 서버 파일은 <code>Path</code>로 넘기면 stdio로 띄우고, 글자 대상은 주소여야 한다고 적습니다. 모듈이 베타라 가져올 때 경고를 한 번 낸다고도 적습니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langchain/mcp/connections">LangChain MCP Connections</a></div>확인 2026-09-28 · 바꾼 도구는 부를 때마다 연결을 열고 닫는다고 적습니다. 연결 블록을 열어 두면 같은 연결을 이어 쓰고, 설정 딕셔너리로 여러 서버를 붙인다고 적습니다.</li><li><div><a href="https://docs.langchain.com/oss/python/migrate/langchain-mcp-adapters">Migrate from langchain-mcp-adapters</a></div>확인 2026-09-28 · <code>MultiServerMCPClient</code>는 <code>MCPAdapter</code>로 합쳐졌다고 적습니다. 오류를 알린 MCP 도구는 결과 상태 <code>error</code>의 도구 메시지가 되고, 도구 가로채기는 <code>@wrap_tool_call</code>로 옮긴다고 적습니다.</li><li><div><a href="https://gofastmcp.com/clients/transports">FastMCP Client Transports</a></div>확인 2026-09-28 · stdio 설정의 칸 <code>keep_alive</code> 기본값이 참이라 같은 자식 프로세스를 다시 쓴다고 적습니다.</li><li>설치판 langchain 1.4.0 소스 <code>langchain/mcp/adapter.py</code> 84~122행은 글자 대상을 주소로만 받습니다. 174~200행은 클라이언트를 만들고, 221~242행 <code>list_tools</code>는 도구를 바꿉니다. <code>langchain/mcp/tools.py</code> 104~117행은 오류를 도구 메시지로 바꾸고, 261~282행은 비동기 몸통만 둔 <code>StructuredTool</code>을 만듭니다.</li><li>설치판 langchain-core 1.6.2 소스 <code>messages/tool.py</code> 73~79행은 아티팩트를 모델에게 보내지 않는 값이라고 적습니다. langchain 1.4.0 <code>agents/middleware/model_call_limit.py</code> 213행과 253행은 호출 한도의 비동기 훅입니다.</li><li>Ch 19 01·05·06절에서 도구와 도구 메시지를, Ch 20 01절에서 손으로 만든 요청과 도구 실행 노드를 보았습니다. Ch 21 01절에서 에이전트를, Ch 22 04절에서 호출 한도를 보았습니다.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    # 파일 위치 셀은 01절 셀 글, 조용히 하는 셀은 03절 셀 글 그대로(「같은 셀」 문장의 근거)
    assert FIND_FILE in (HERE / "author_01.py").read_text(encoding="utf-8"), "FIND_FILE이 01절 셀과 다릅니다"
    assert QUIET in notebook_code_sources(NB03), "QUIET이 03절 노트북 셀과 다릅니다"
    check_tools()
    check_same_as_probe()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "connect_tools.py").write_text(TOOLS_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        print("copied", target / "connect_tools.py")
        sys.exit(0)
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        write_tools()
        path = write_notebook(LAB, "04", SLUG, "experiment", cells())
        print("wrote", path)
