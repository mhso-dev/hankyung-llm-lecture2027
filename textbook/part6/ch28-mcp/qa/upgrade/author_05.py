"""Ch 28 05절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§5-3·§6 experiment). 본문 마지막 절.

사용:
  python3 -B author_05.py                  → 도구 파일(가드)·노트북·_src 본문을 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_05.py --src-only       → _src 본문만 다시 쓴다(노트북은 그대로)
  python3 -B author_05.py --tools-copy DIR → 디스크의 도구 파일 connect_tools.py를 DIR에 복사한다(새 커널 사본 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**. 슬러그 그대로.

## 결정 1 — 앞 절반 모델 없음(2~4절, 요청 0): 도구 정의 → 도구 명세 → 명세 글자 수

2절: 04절 설정(03절 stdio_config + quiet_env)으로 서버 파일 도구를 MCPAdapter로 받고, convert_to_openai_tool(Ch 19 01)로 만든 명세의
칸 parameters가 입력 형식과 같음(True)을 본 뒤, Ch 19 03 spec_length(도구 파일, 셀 글 그대로)로 252자. bind_tools(Ch 19 04)의 .kwargs["tools"]가
명세와 같음(True, 요청 0). 3절: 이름·설명이 같은 직접 @tool("lookup_policy") → additionalProperties 없음 221자(31자 짧음).
4절: 설명만 두 문장 늘린 메모리 서버 longer → 299자(명세 +47 = 설명 +47) · runpy로 받은 서버 객체 server에 @server.tool 둘을 더 붙여
메모리 연결로 받은 도구 셋 → 252·503·685(첫 도구 명세 = 2절 명세 True). 자체 schema_chars는 뺐다.

## 결정 2 — 뒤 절반 실제 모델(5절, 요청 5): 첫 요청 입력 토큰

04절 에이전트와 같은 시스템 메시지 글·질문(first_messages)을 조건 다섯(도구 없음 · MCP 도구 하나 · 직접 도구 하나 · 설명을 늘린 도구 하나 ·
MCP 도구 셋)에 한 번씩 보낸다(bind_tools(...).invoke, tool_choice 없음, 도구는 부르지 않음). 흔들림: qa/upgrade/05-probe.md
(§0 21:52:17Z, 첫 요청 21:52:29Z, 조건마다 5/5 같음 — 56·187·187·218·252). 입력 토큰은 5/5 + 두 커널 같을 때만 결론에(한정어와 함께).
도구 호출 요청·출력 토큰·답 글·예상 비용은 둘째 단락에만. assert는 파일 찾기 셀(01 셀 글)과 키 셀뿐 — 모델 값에 assert 없음.
흔들리는 값의 둘째 단락은 [[READ_…]] 자리 표시(글자 그대로 — mdpatch.py가 생성기까지 고침) → 교재 출력(A)·사본(B) 뒤 채움.

## 결정 3 — 도구 파일 connect_tools.py 05 판 (04 판 + spec_length, 대조 사슬 이어 감)

04 판(cc066bd7…)의 머리 설명·블록 여섯은 글자 그대로 두고, 가져오기 블록에만 import json · convert_to_openai_tool 두 줄을 넣고,
Ch 19 03절 노트북 셀 글 spec_length(8afb6cff…)를 더한다. 쓰기 가드: 없거나 · 03 판 · 04 판 · 이 판이면 쓰고, 뒤 판(머리 설명으로 시작하고
이 판의 블록을 모두 담음)은 건너뛰고, 그 밖이면 멈춘다. 03·04 생성기의 later_version()은 이 판을 「뒤 절 판」으로 본다(check_tools에서 확인).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·변수 힌트·내놓는 값 힌트·대입 풀기·별표 풀기·
세미콜론·`isinstance`·`importlib`·클래스·`asyncio.run`·`while`·`try`·`tool_choice`. 데코레이터는 @tool("lookup_policy")·@longer.tool·
@server.tool(그 함수 매개변수 단순 힌트 — 챕터 예외). 호출 깊이 2 이하.
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
import author_03  # noqa: E402  03절 셀 글(QUIET)·도구 파일 머리 설명
import author_04  # noqa: E402  도구 파일 04 판
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch28-mcp/notebooks"
FIGS = ROOT / "textbook/part6/ch28-mcp/figures"
SLUG = "05-도구-정의와-첫-호출-토큰"
TITLE_TEXT = "도구 정의와 첫 호출 토큰"
SRC = ROOT / "textbook/part6/ch28-mcp/_src" / (SLUG + ".html")
NB03 = LAB / "03-stdio와-원격-전송-권한-경계.ipynb"
NB19_03 = ROOT / "labs/part5/ch19-model-tools/notebooks/03-좋은-도구-이름과-설명.ipynb"
TOOLS_PATH = LAB / "connect_tools.py"
TOOLS_04_SHA = "cc066bd7fac0985313305fa6dfc9d3144cbd6c64f98ef2fd679b2c496b99edb3"
DEF_SPEC_SHA = "8afb6cff1e3df9a690a9a4d1b1da08ee8bd55e4f0e2bfdfa40464fab898bbd36"
html_text = author_02.html_text
table_html = author_02.table_html


# ---------------------------------------------------------------- 도구 파일 connect_tools.py (05 판)
TOOLS_IMPORTS_05 = '''
import json
import sys

from fastmcp import Client
from fastmcp.exceptions import ToolError
from langchain_core.utils.function_calling import convert_to_openai_tool
'''
NOTE_19_03 = "Ch 19 03절에서 배웠습니다 — Ch 19 03절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다"
TOOL_ORDER = author_04.TOOL_ORDER + ["spec_length"]


def ch19_spec_cell() -> str:
    """Ch 19 03절 노트북에서 spec_length를 정의한 코드 셀 글을 꺼냅니다(고정 해시와 같아야 함)."""
    found = []
    for source in author_03.notebook_code_sources(NB19_03):
        if "def spec_length" in source:
            found.append(source)
    assert len(found) == 1, "Ch 19 03절 노트북에서 spec_length 셀을 하나만 찾아야 합니다"
    assert hashlib.sha256(found[0].encode("utf-8")).hexdigest() == DEF_SPEC_SHA, "Ch 19 03절 spec_length 셀 글이 고정 해시와 다릅니다"
    return found[0]


DEF_SPEC = ch19_spec_cell()


def blocks_05() -> list:
    """05 판에 담는 블록 차례: 04 판 블록 여섯 + Ch 19 03 spec_length."""
    return author_04.blocks_04() + ["\n\n# " + NOTE_19_03 + "\n" + DEF_SPEC + "\n"]


def tools_text() -> str:
    text = author_03.TOOLS_HEAD + TOOLS_IMPORTS_05
    for block in blocks_05():
        text = text + block
    return text


TOOLS = tools_text()


def later_version(current: str) -> bool:
    """뒤 판인지 봅니다: 머리 설명으로 시작하고 이 판의 블록을 모두 담으면서 이 판과 다르면 참."""
    if not current.startswith(author_03.TOOLS_HEAD):
        return False
    for block in blocks_05():
        if block.strip("\n") not in current:
            return False
    return current != TOOLS


def check_tools() -> None:
    """도구 파일 05 판이 04 판을 그대로 잇고, 더한 spec_length가 Ch 19 03절 노트북 셀과 글자·AST 모두 같은지 봅니다."""
    assert hashlib.sha256(author_04.TOOLS.encode("utf-8")).hexdigest() == TOOLS_04_SHA, "04 생성기의 도구 파일 판이 04 마감 판과 다릅니다"
    assert TOOLS.startswith(author_03.TOOLS_HEAD)
    # 04 판 = 머리 설명 + 가져오기 블록 + 블록 여섯. 05 판은 가져오기 블록에 두 줄만 더하고 04 블록 여섯을 글자 그대로 담습니다
    assert author_04.TOOLS[len(author_03.TOOLS_HEAD) + len(author_04.TOOLS_IMPORTS_04):] in TOOLS
    tree = ast.parse(TOOLS)
    names = []
    imports = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
    assert names == TOOL_ORDER, names
    assert imports == ["import json", "import sys", "from fastmcp import Client", "from fastmcp.exceptions import ToolError",
                       "from langchain_core.utils.function_calling import convert_to_openai_tool"], imports
    assert DEF_SPEC in author_03.notebook_code_sources(NB19_03)
    assert ("# " + NOTE_19_03 + "\n" + DEF_SPEC + "\n") in TOOLS
    mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "spec_length"]
    theirs = [ast.dump(n) for n in ast.parse(DEF_SPEC).body if isinstance(n, ast.FunctionDef)]
    assert mine == theirs and len(mine) == 1, "spec_length"
    # 앞 절 생성기가 이 판을 뒤 판으로 보아 덮어쓰지 않는지(03·04를 다시 돌려도 안전한지)
    assert author_03.later_version(TOOLS), "03 생성기가 05 판을 뒤 판으로 보지 않습니다"
    assert author_04.later_version(TOOLS), "04 생성기가 05 판을 뒤 판으로 보지 않습니다"


def write_tools() -> None:
    current = ""
    if TOOLS_PATH.is_file():
        current = TOOLS_PATH.read_text(encoding="utf-8")
    if current in ("", TOOLS, author_04.TOOLS, author_03.TOOLS):
        TOOLS_PATH.write_text(TOOLS, encoding="utf-8")
        print("wrote", TOOLS_PATH)
    elif later_version(current):
        print("skip", TOOLS_PATH, "(뒤 판 — 덮어쓰지 않음)")
    else:
        raise AssertionError("도구 파일이 03·04·05절 판으로 시작하지 않습니다")


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["langchain[mcp]==1.4.0", "langchain-core==1.6.2", "langchain-openai==1.6.0",
                          "fastmcp==4.0.3", "mcp==2.2.0", "python-dotenv==1.2.3"])

IMPORTS = r'''# 이 절에서 쓸 이름을 가져옵니다(langchain.mcp는 베타 경고 한 종류만 끄고 가져옵니다)
import json
import runpy
import warnings
from langchain_core._api import LangChainBetaWarning
warnings.filterwarnings("ignore", category=LangChainBetaWarning)
from langchain.mcp import MCPAdapter
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_tool
from fastmcp import FastMCP
# 01·03절과 앞 챕터에서 배운 함수 다섯은 도구 파일에서 가져옵니다
from connect_tools import estimate_cost, names_of, spec_length, stdio_config, tool_call_names

print("도구 파일에서 가져온 함수:", "estimate_cost, names_of, spec_length, stdio_config, tool_call_names")'''

FIND_FILE = author_01.FIND_FILE
QUIET = author_03.QUIET

ADAPT = r'''# 03절 함수 stdio_config로 만든 설정을 MCPAdapter에 넘겨, 서버 파일의 도구를 LangChain 도구로 받습니다
course_config = stdio_config(server_file, quiet_env)
adapter = MCPAdapter(course_config)
mcp_tools = await adapter.list_tools()
policy_tool = mcp_tools[0]
print("받은 도구 이름:", names_of(mcp_tools))
print("입력 형식:", policy_tool.args_schema)'''

SPEC = r'''# 바꾼 도구 하나를 모델에게 보낼 도구 명세 딕셔너리로 만들고, 칸을 봅니다(Ch 19 01절 convert_to_openai_tool)
policy_spec = convert_to_openai_tool(policy_tool)
spec_function = policy_spec["function"]
print("명세의 칸:", list(policy_spec))
print("칸 function 안의 칸:", list(spec_function))
print("이름:", spec_function["name"])
print("설명:", spec_function["description"])
print("parameters 칸이 입력 형식과 같은가:", spec_function["parameters"] == policy_tool.args_schema)'''

SPEC_TEXT = r'''# 명세를 JSON 글로 바꿔 글자 수를 세고, Ch 19 03절 함수 spec_length로 센 값과 견줍니다
policy_text = json.dumps(policy_spec, ensure_ascii=False)
mcp_length = spec_length(mcp_tools)
print("명세 JSON 글:")
print(policy_text)
print("글자 수:", len(policy_text))
print("spec_length로 센 글자 수:", mcp_length)'''

BIND = r'''# 모델 객체에 MCP 도구를 알리고, 요청에 실을 도구 칸이 앞 셀의 명세와 같은지 봅니다(요청은 아직 없음)
mcp_model = model.bind_tools(mcp_tools)
bound_tools = mcp_model.kwargs["tools"]
print("알린 도구 수:", len(bound_tools))
print("앞 셀의 명세와 같은가:", bound_tools[0] == policy_spec)'''

LOAD = r'''# 서버 파일을 실행해 서버 객체와 규정 딕셔너리를 받습니다(02절 6절처럼 runpy.run_path로 읽고, 파일은 고치지 않습니다)
server_names = runpy.run_path(server_file)
server = server_names["mcp"]
policies = server_names["POLICIES"]
print("서버 이름:", server.name)
print("규정 주제:", list(policies))'''

DEF_DIRECT = r'''# 서버 파일 도구와 이름·설명이 같은 도구를 Ch 19처럼 @tool 줄로 직접 만듭니다
@tool("lookup_policy")
def direct_lookup(topic: str):
    """자료실 규정을 조회합니다. topic은 대출, 운영, 연체 중 하나입니다."""
    return policies[topic]'''

DIRECT_SPEC = r'''# 직접 도구의 명세를 만들고, MCP 도구 명세와 이름·설명·칸 parameters·글자 수를 견줍니다
direct_function = convert_to_openai_tool(direct_lookup)["function"]
direct_length = spec_length([direct_lookup])
print("이름이 같은가:", direct_function["name"] == spec_function["name"])
print("설명이 같은가:", direct_function["description"] == spec_function["description"])
print("직접 도구 parameters 칸:", direct_function["parameters"])
print("직접 도구 명세 글자 수:", direct_length)
print("MCP 도구 명세 글자 수:", mcp_length)
print("MCP 쪽이 긴 글자 수:", mcp_length - direct_length)'''

DEF_LONG = r'''# 설명만 두 문장 늘린 lookup_policy 도구를 붙인 연습 서버를 만듭니다(이름·매개변수 힌트는 서버 파일과 같음)
longer = FastMCP("설명을 늘린 자료실")

@longer.tool
def lookup_policy(topic: str):
    """자료실 규정을 조회합니다. topic은 대출, 운영, 연체 중 하나입니다. 대출·운영·연체 규정을 물을 때 씁니다. 그 주제의 규정 글 한 문장을 내놓습니다."""
    return policies[topic]'''

LONG_LIST = r'''# 연습 서버 객체를 메모리 연결로 MCPAdapter에 넘겨 도구를 받고, 서버 파일 도구와 견줍니다
long_adapter = MCPAdapter(longer)
long_tools = await long_adapter.list_tools()
long_tool = long_tools[0]
print("받은 도구 이름:", names_of(long_tools))
print("입력 형식이 같은가:", long_tool.args_schema == policy_tool.args_schema)
print("설명이 같은가:", long_tool.description == policy_tool.description)'''

LONG_SPEC = r'''# 설명을 늘린 판의 명세 글자 수를 세고, 늘어난 명세 글자 수와 늘어난 설명 글자 수를 견줍니다
long_length = spec_length(long_tools)
added_spec = long_length - mcp_length
added_description = len(long_tool.description) - len(policy_tool.description)
print("설명을 늘린 판 명세 글자 수:", long_length)
print("늘어난 명세 글자 수:", added_spec)
print("늘어난 설명 글자 수:", added_description)
print("두 수가 같은가:", added_spec == added_description)'''

DEF_SEARCH = r'''# 서버 객체에 규정 글에서 낱말이 든 주제어를 찾는 도구를 더 붙입니다(서버 파일은 그대로입니다)
@server.tool
def search_topics(word: str):
    """규정 글에 낱말이 든 주제어를 찾습니다. word에는 찾을 낱말을 넣습니다."""
    found = []
    for topic in policies:
        if word in policies[topic]:
            found.append(topic)
    return found'''

DEF_SHOW = r'''# 같은 서버 객체에 규정 주제어 목록을 알려 주는, 인자 없는 도구를 더 붙입니다
@server.tool
def show_topics():
    """자료실 규정의 주제어 목록을 알려 줍니다."""
    return list(policies)'''

WIDE_LIST = r'''# 도구 셋이 붙은 서버 객체를 메모리 연결로 넘겨 도구를 받고, 첫 도구 명세를 2절 명세와 견줍니다
wide_adapter = MCPAdapter(server)
wide_tools = await wide_adapter.list_tools()
first_wide_spec = convert_to_openai_tool(wide_tools[0])
print("받은 도구 이름:", names_of(wide_tools))
print("첫 도구 명세가 2절 명세와 같은가:", first_wide_spec == policy_spec)'''

COUNT = r'''# 도구를 하나·둘·셋으로 늘리며 명세 글자 수를 셉니다
for count in [1, 2, 3]:
    chosen_tools = wide_tools[:count]
    print("도구 수:", count, "| 명세 글자 수:", spec_length(chosen_tools))'''

MESSAGES = r'''# 04절 에이전트와 같은 시스템 메시지 글과 질문으로, 첫 요청에 실을 메시지 둘을 만듭니다
agent_rule = "교육센터 자료실 규정 질문에는 도구로 규정을 찾아, 찾은 글만 근거로 한국어 한 문장으로 답하세요."
question = "교육센터 자료실은 토요일에 몇 시까지 운영하나요?"
first_messages = [SystemMessage(content=agent_rule), HumanMessage(content=question)]
print("첫 요청 메시지 수:", len(first_messages))
print("첫 메시지 종류:", type(first_messages[0]).__name__)'''

ASK_NONE = r'''# 도구를 알리지 않은 모델에 첫 요청을 한 번 보내고, 도구 호출 요청·입력 토큰·답 글을 봅니다
none_reply = model.invoke(first_messages)
none_usage = none_reply.usage_metadata
print("도구 호출 요청:", tool_call_names(none_reply))
print("입력 토큰:", none_usage["input_tokens"])
print("답 글:")
print(none_reply.text)'''

ASK_MCP = r'''# 2절에서 MCP 도구를 알린 모델 mcp_model로 같은 메시지를 보냅니다(도구는 부르지 않고, 명세만 실립니다)
mcp_reply = mcp_model.invoke(first_messages)
print("도구 호출 요청:", tool_call_names(mcp_reply))
print("입력 토큰:", mcp_reply.usage_metadata["input_tokens"])'''

ASK_DIRECT = r'''# 3절의 직접 도구를 알린 모델로 같은 메시지를 보내고, 입력 토큰을 봅니다
direct_model = model.bind_tools([direct_lookup])
direct_reply = direct_model.invoke(first_messages)
print("도구 호출 요청:", tool_call_names(direct_reply))
print("입력 토큰:", direct_reply.usage_metadata["input_tokens"])'''

ASK_LONG = r'''# 4절의 설명을 늘린 도구를 알린 모델로 같은 메시지를 보내고, 입력 토큰을 봅니다
long_model = model.bind_tools(long_tools)
long_reply = long_model.invoke(first_messages)
print("도구 호출 요청:", tool_call_names(long_reply))
print("입력 토큰:", long_reply.usage_metadata["input_tokens"])'''

ASK_WIDE = r'''# 4절의 도구 셋을 알린 모델로 같은 메시지를 보내고, 입력 토큰을 봅니다
wide_model = model.bind_tools(wide_tools)
wide_reply = wide_model.invoke(first_messages)
print("도구 호출 요청:", tool_call_names(wide_reply))
print("입력 토큰:", wide_reply.usage_metadata["input_tokens"])'''

TABLE = r'''# 도구를 알린 네 요청마다 입력 토큰과, 도구 없는 요청보다 더 쓴 입력 토큰(도구 정의 몫)을 봅니다
base_tokens = none_usage["input_tokens"]
replies = {
    "MCP 도구 하나": mcp_reply,
    "직접 도구 하나": direct_reply,
    "설명을 늘린 도구 하나": long_reply,
    "MCP 도구 셋": wide_reply,
}
for label in replies:
    tokens = replies[label].usage_metadata["input_tokens"]
    print(label, "| 입력 토큰:", tokens, "| 도구 정의 몫:", tokens - base_tokens)'''

COST = r'''# 다섯 요청의 출력 토큰을 보고, 2026-09-17 요금표(100만 토큰당 달러)로 어림한 예상 비용을 더합니다(Ch 6 06절 함수 estimate_cost)
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
all_replies = [none_reply, mcp_reply, direct_reply, long_reply, wide_reply]
total_cost = 0
for reply in all_replies:
    print("출력 토큰:", reply.usage_metadata["output_tokens"])
    total_cost = total_cost + estimate_cost(reply.usage_metadata, input_rate, cached_input_rate, output_rate)
print("예상 비용 합(달러):", round(total_cost, 6))'''


def check_same_as_probe() -> None:
    """노트북 셀의 서버·도구·메시지·모델 줄이 흔들림 확인 스크립트(probe05.py)와 같은 글인지 봅니다."""
    probe = (HERE / "probe/probe05.py").read_text(encoding="utf-8")
    pieces = []
    for cell in [QUIET, author_03.DEF_CONFIG, DEF_DIRECT, DEF_LONG, DEF_SEARCH, DEF_SHOW, MESSAGES, LOAD, BIND]:
        for line in cell.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("print(") or stripped == "":
                continue
            if stripped.startswith("bound_tools") or stripped.startswith("first_messages"):
                continue
            pieces.append(stripped)
    pieces += ["course_config = stdio_config(server_file, quiet_env)", "adapter = MCPAdapter(course_config)",
               "mcp_tools = await adapter.list_tools()", "long_tools = await MCPAdapter(longer).list_tools()",
               "wide_tools = await MCPAdapter(server).list_tools()", "direct_model = model.bind_tools([direct_lookup])",
               "long_model = model.bind_tools(long_tools)", "wide_model = model.bind_tools(wide_tools)",
               'first_messages = [SystemMessage(content=agent_rule), HumanMessage(content=question)]',
               "reply = bound.invoke(first_messages)", '("none", model, 0),',
               '"openai:gpt-5.4-mini",', "temperature=0,", 'reasoning_effort="none",',
               'warnings.filterwarnings("ignore", category=LangChainBetaWarning)']
    for piece in pieces:
        assert piece in probe, piece


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/05-figures.md)
FIG1 = "05-1-도구-정의가-도구-명세가-되기까지"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 초록 상자 서버 파일 course_server.py 도구 정의 lookup_policy에서 파란 상자 MCPAdapter list_tools stdio 연결, 노란 상자 StructuredTool 입력 형식 dict, 파란 상자 convert_to_openai_tool을 지나 노란 상자 도구 명세로 화살표가 이어집니다. 명세 상자에는 type function, 칸 name · description, 칸 parameters = 입력 형식 True가 적혀 있고, 거기서 점선 둘이 나란히 놓인 노란 상자 spec_length 명세 글자 수 252와 노란 상자 bind_tools 요청에 실을 도구 칸 명세와 같음 True로 가는 그림"
FIG1_CAP = "서버가 알린 도구 정의는 StructuredTool을 지나 도구 명세가 되었고, 입력 형식은 칸 parameters에 그대로 실렸습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자는 서버 파일이고, 파란 상자는 우리가 부른 클래스와 함수입니다.
노란 상자는 노트북 2절 출력으로 확인한 값입니다.
맨 아래 점선 둘은 같은 명세를 두 쪽에서 본 갈래로, 글자 수를 센 쪽과 모델 객체에 알린 쪽입니다.
모델은 5절에서만 부르고, 이 그림에는 모델 상자를 두지 않았습니다."""

FIG2 = "05-2-바꾼-것과-명세-글자-수"
FIG2_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 노란 상자 MCP 도구 하나 lookup_policy 명세 252자에서 점선 셋이 나란한 파란 상자 셋으로 갑니다. 왼쪽 입력 형식 모양만 바꿈 직접 만든 @tool 아래에 노란 상자 221자 additionalProperties 없음 31자 짧음, 가운데 설명만 바꿈 두 문장 더함 아래에 노란 상자 299자 늘어난 명세 47 = 늘어난 설명 47, 오른쪽 도구 수만 바꿈 서버 객체에 둘 더 붙임 아래에 노란 상자 도구 하나 둘 셋 252 503 685자가 있는 그림"
FIG2_CAP = "입력 형식 모양·설명·도구 수를 하나씩 바꾸자 명세 글자 수는 221, 299, 685로 달라졌고, 늘어난 설명만큼 명세도 늘었습니다."
FIG2_READ = """맨 위 노란 상자는 2절에서 센 MCP 도구 하나의 명세 글자 수입니다.
파란 상자 셋은 3·4절에서 바꾼 것 하나씩이고, 점선은 서로 다른 조건으로 갈라진 갈래입니다.
아래 노란 상자 셋은 노트북 3·4절 출력입니다.
모델을 부르지 않은 값이라 보라 상자는 없습니다."""

FIG3 = "05-3-도구를-알린-첫-요청"
FIG3_ALT = "위에서 아래로 읽는 흐름도입니다. 나란한 파란 상자 둘 model.invoke first_messages 도구 없음과 mcp_model.invoke first_messages MCP 도구 하나 명세 252자가 있고, 각각 보라 상자 gpt-5.4-mini 첫 요청 한 번을 지나 노란 상자 입력 토큰 56과 노란 상자 입력 토큰 187로 이어집니다. 두 노란 상자는 맨 아래 노란 상자 도구 정의 몫 131 = 187 − 56으로 모이는 그림"
FIG3_CAP = "흔들림 확인 다섯 번과 두 커널에서 모두, 같은 메시지에 MCP 도구 하나를 알린 첫 요청은 입력 토큰이 131 많았습니다."
FIG3_READ = """위에서 아래로 읽고, 왼쪽 칸이 도구 없는 요청, 오른쪽 칸이 MCP 도구를 알린 요청입니다.
파란 상자는 우리가 부른 코드이고, 보라 상자는 실제로 부른 모델 gpt-5.4-mini입니다.
노란 상자는 노트북 5절 출력이고, 맨 아래 상자는 두 입력 토큰의 차입니다.
두 요청 모두 도구를 부르지 않은 첫 요청 하나씩입니다."""

FIG4 = "05-4-명세-글자-수와-도구-정의-몫"
FIG4_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 노란 상자 도구 없는 첫 요청 입력 토큰 56 몫의 기준에서 노란 상자 MCP 도구 하나 명세 252자 몫 131로 화살표가 가고, 그 상자에서 점선 셋이 나란한 노란 상자 셋으로 갑니다. 왼쪽부터 직접 도구 하나 명세 221자 몫 131, 설명을 늘린 도구 하나 명세 299자 몫 162, MCP 도구 셋 명세 685자 몫 196이 적힌 그림"
FIG4_CAP = "흔들림 확인 다섯 번과 두 커널에서 모두, 명세 글자 수가 달라진 만큼 도구 정의 몫이 늘지는 않았습니다."
FIG4_READ = """위에서 아래로 읽습니다.
맨 위 상자는 도구 정의 몫을 셀 때 빼는 기준, 도구 없는 첫 요청의 입력 토큰입니다.
그 아래 상자는 MCP 도구 하나이고, 점선 셋은 3·4절에서 바꾼 조건으로 갈라진 갈래입니다.
노란 상자는 모두 노트북 3~5절 출력입니다.
상자마다 명세 글자 수와 도구 정의 몫을 나란히 적어, 두 값이 같은 비율로 늘지 않은 것을 견줍니다."""

ILLU = "05-5-모듈-수만큼-쌓이는-설명서"
# 1차 job ec17f0a9-5ffa-4c96-9163-441329e06a8c 채택(재생성 0)
ILLU_ALT = "흰 바탕에 두 장면이 가운데 가는 회색 세로선을 사이에 두고 좌우로 놓인 그림입니다. 왼쪽은 짧은 회색 격자 트러스 위에 모서리가 둥근 산호색 네모 모듈 하나가 얹혀 있고, 그 아래에 산호색 책 한 권이 놓여 있습니다. 오른쪽은 더 긴 회색 격자 트러스 위에 산호색·민트색·연보라 모듈 셋이 나란히 얹혀 있고, 그 아래에 같은 세 색의 책 세 권이 포개져 있습니다. 사람·글자·숫자·화살표·별은 없는 그림"
ILLU_CAP = "모듈이 하나인 정거장 옆에는 설명서가 한 권, 모듈이 셋인 정거장 옆에는 세 권이 쌓였습니다."
ILLU_READ = "왼쪽 짧은 회색 트러스에는 산호색 모듈 하나가 얹혀 있고, 아래에 같은 색 책 한 권이 있습니다. 오른쪽 긴 트러스에는 산호색·민트색·연보라 모듈 셋이 얹혀 있고, 아래에 같은 세 색의 책 세 권이 포개져 있습니다. 트러스가 MCP 서버, 모듈이 서버의 도구, 책 한 권이 도구 명세 하나입니다. 그림의 책 더미와 달리, 흔들림 확인 다섯 번과 두 커널에서 모두 도구 셋의 정의 몫은 세 배가 되지 않았습니다. 모듈끼리 조금 겹쳐 보이는 것과 트러스 길이, 색은 어떤 값과도 짝짓지 않습니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. MCP 서버의 도구 정의가 모델에게 보낼 도구 명세가 되는 모양과 글자 수를 모델 없이 봅니다.
2. 입력 형식 모양·설명 길이·도구 수를 하나씩 바꾸며 명세 글자 수를 셉니다.
3. 같은 메시지로 첫 요청을 조건마다 한 번씩 보내, 도구 정의가 입력 토큰에 얼마나 더해지는지 봅니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 5절에서 조건 다섯에 첫 요청을 한 번씩 보냅니다.
도구는 알리기만 하고 부르지 않아서, 모델 요청은 모두 5번입니다.
요금표로 어림한 예상 비용은 다섯 요청을 합쳐 0.002달러 아래이고, 청구 금액이 아닙니다.

2~4절은 모델을 부르지 않고, 출력은 도구 정의와 도구 명세에서 센 값입니다.
서버는 실습 폴더 맨 위의 서버 파일 `course_server.py`를 씁니다.
2절은 04절처럼 서버를 자식 프로세스로 띄우고, 3·4절은 서버 파일을 이 커널 안에서 읽습니다.
노트북이 쓰는 파일은 없고, 걸린 시간은 재지 않았습니다.
앞에서 배운 함수 다섯은 도구 파일 `connect_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 여섯을 설치합니다.
판은 langchain 1.4.0, langchain-core 1.6.2, langchain-openai 1.6.0입니다.
패키지 fastmcp 4.0.3, mcp 2.2.0, python-dotenv 1.2.3도 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~4절을 읽습니다.
도구 정의가 도구 명세가 되는 모양과, 무엇을 바꾸면 명세 글자 수가 달라지는지 보는 자리입니다.
5절은 실제 모델에 첫 요청을 보내는 실습이고, 실습 시간에 실행합니다.

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
모델 요청은 5절의 요청 셀 다섯에서만 나갑니다.

## 2. 도구 정의가 도구 명세가 되기까지

01절에서 서버가 알린 도구 정의에는 이름·설명·입력 형식이 들어 있었습니다.
04절은 그 정의를 받아 LangChain 도구로 바꿨습니다.
이 절은 바꾼 도구를 모델에게 보낼 도구 명세로 만들어, 그 모양과 글자 수를 봅니다.
먼저 01절 2절과 같은 셀로 서버 파일의 위치를 찾습니다.""")
    return cells


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

04절은 MCP 도구를 LangChain 도구로 바꿔 에이전트에 붙였습니다.
이 절은 그 도구 정의가 모델에게 가는 요청에 어떤 모양으로 실리는지 봅니다.
그리고 도구를 부르기 전 첫 요청의 입력 토큰에 얼마나 더해지는지 셉니다.

첫 셀은 패키지 여섯을 설치하고 설치된 판 번호를 출력합니다.
04절과 달리 langgraph와 psutil은 쓰지 않아 설치하지 않습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langchain: 1.4.0`, `langchain-core: 1.6.2`, `fastmcp: 4.0.3`이 보입니다.
여섯 판 모두 실습 폴더 잠금과 같습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
04절처럼 모듈 `langchain.mcp`는 베타 경고 한 종류만 끄고 가져옵니다.
모듈 `json`과 함수 `convert_to_openai_tool`은 Ch 19에서 도구 명세를 볼 때 쓴 이름입니다.
모듈 `runpy`는 01·02절처럼 서버 파일을 이 커널에서 읽을 때 씁니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: estimate_cost, names_of, spec_length, stdio_config, tool_call_names`가 보입니다.
함수 `spec_length`는 Ch 19 03절에서 만든 함수로, 도구 목록의 명세 글자 수를 모두 더합니다.
이 절부터 도구 파일에서 가져오고, 설명 주석과 본문은 Ch 19 03절 노트북 셀과 글자까지 같습니다.
나머지 넷은 04절에서처럼 01·03절과 Ch 19 04절, Ch 6 06절에서 배운 함수입니다."""),
    ] + model_cells() + [
        code(FIND_FILE),
        md("""**결과 읽기** — 출력 줄 `서버 파일을 찾았는가: True`가 보입니다.
교재 출력은 프로젝트 맨 위에서 실행해 셋째 후보 `labs/part6/ch28-mcp/course_server.py`를 골랐습니다.
`notebooks/` 폴더에서 열면 첫 후보 `../course_server.py`가 골라집니다.

다음 셀은 03절 2절과 같은 셀로, 서버를 조용히 띄우는 환경 변수 셋을 딕셔너리로 만듭니다."""),
        code(QUIET),
        md("""**결과 읽기** — 라벨 `조용히 하는 이름:` 뒤에 이름 셋이 보입니다.
03절에서 본 것처럼, 시작 안내와 새 판 확인을 끄고 기록 수준을 올리는 이름입니다.

다음 셀은 04절 2절처럼 설정 한 벌을 클래스 `MCPAdapter`에 넘겨, 서버 파일의 도구를 받습니다.
받은 도구의 입력 형식도 함께 출력합니다."""),
        code(ADAPT),
        md("""**결과 읽기** — 출력 줄 `받은 도구 이름: ['lookup_policy']`가 보입니다.
라벨 `입력 형식:` 뒤의 딕셔너리는 04절 2절에서 본 입력 형식과 같은 글입니다.
칸 `'additionalProperties': False`는 적힌 칸 `topic` 말고 다른 칸은 받지 않는다는 표시입니다.
01절 4절에서 서버의 입력 형식에 이 칸이 있는 것을 보았습니다.

다음 셀은 이 도구 하나를 모델에게 보낼 도구 명세로 만듭니다.
Ch 19 01절에서 쓴 함수 `convert_to_openai_tool`은 도구 하나를 받아 명세 딕셔너리를 내놓습니다.
Ch 19 03절처럼, 이 딕셔너리를 이 절에서도 도구 명세라고 부릅니다."""),
        code(SPEC),
        md("""**결과 읽기** — 출력 줄 `명세의 칸: ['type', 'function']`과 `칸 function 안의 칸: ['name', 'description', 'parameters']`가 보입니다.
이름과 설명은 서버 파일 도구의 이름과 독스트링 글 그대로입니다.
출력 줄 `parameters 칸이 입력 형식과 같은가: True`로, 서버가 보낸 입력 형식이 그대로 실립니다.

04절은 모델에게 보내는 도구 정의에 입력 형식 딕셔너리가 어떻게 실리는지 05절에서 본다고 했습니다.
바꾼 MCP 도구의 입력 형식 딕셔너리는 명세의 칸 `parameters`에 그대로 들어갑니다.
서버 파일 도구의 출력 형식(02절 6절)은 명세의 칸에 없습니다.

다음 셀은 이 명세를 JSON 글로 바꿔 글자 수를 셉니다.
Ch 19 03절의 함수 `spec_length`도 같은 방법으로 세므로, 두 값을 견줍니다."""),
        code(SPEC_TEXT),
        md("""**결과 읽기** — 라벨 줄 `명세 JSON 글:` 아래에 명세 한 줄이 보입니다.
출력 줄 `글자 수: 252`와 `spec_length로 센 글자 수: 252`가 같습니다.
도구가 하나라서, 함수 `spec_length`가 더한 값도 명세 하나의 글자 수입니다.

JSON 글에서는 파이썬의 `False`가 `false`로 바뀌고, 따옴표도 큰따옴표가 됩니다.
Ch 19 03절에서 본 것처럼 이 글자 수는 토큰 수와 다릅니다.
모델이 이 명세를 몇 토큰으로 세는지는 5절에서 요청을 보내 봅니다.

다음 셀은 모델 객체에 이 도구를 알리고, 요청에 실을 도구 칸을 봅니다.
Ch 19 04절처럼 메서드 `bind_tools`는 도구 목록을 받은 새 모델 객체를 내놓습니다.
속성 `kwargs["tools"]`에 요청에 실을 도구 칸이 들어 있고, 이 셀은 요청을 보내지 않습니다."""),
        code(BIND),
        md("""**결과 읽기** — 출력 줄 `알린 도구 수: 1`과 `앞 셀의 명세와 같은가: True`가 보입니다.
메서드 `bind_tools`도 앞 셀과 같은 명세를 만들어 요청에 실을 준비를 합니다.
모델 객체 `mcp_model`은 5절에서 첫 요청을 보낼 때 다시 씁니다.

실제 요청에서는 이 딕셔너리가 JSON 글로 바뀌어 서비스에 갑니다.
그때 띄어쓰기나 한글을 적는 방법이 이 셀과 다를 수 있어, 글자 수를 요청 크기로 읽지는 않습니다.

## 3. 입력 형식 모양만 다른 직접 도구

MCP 도구의 명세에는 칸 `additionalProperties`가 있었습니다.
Ch 19처럼 `@tool` 줄로 직접 만든 도구의 명세에도 이 칸이 있을까요?
이름과 설명을 똑같이 둔 직접 도구를 만들어 견줍니다.
직접 도구의 몸통이 쓸 규정 글은 서버 파일에서 가져옵니다.
다음 셀은 02절 6절처럼 서버 파일을 이 커널에서 실행해, 서버 객체와 규정 딕셔너리를 받습니다."""),
        code(LOAD),
        md("""**결과 읽기** — 출력 줄 `서버 이름: 교육센터 자료실`과 `규정 주제: ['대출', '운영', '연체']`가 보입니다.
변수 `server`는 서버 파일이 만든 서버 객체이고, 변수 `policies`는 서버 파일의 규정 딕셔너리입니다.
파일을 실행해 이름을 받았을 뿐이라, 서버 파일은 그대로입니다.

다음 셀은 서버 파일 도구와 이름·설명이 같은 도구를 직접 만듭니다.
셀의 `@tool("lookup_policy")` 줄은 아래 함수를 이름이 lookup_policy인 LangChain 도구로 만듭니다.
Ch 19 04절처럼 도구 이름을 따로 정해, 파이썬 함수 이름 `direct_lookup`과 다르게 둡니다.
몸통은 규정 딕셔너리에서 주제어의 글을 찾는 한 줄입니다."""),
        code(DEF_DIRECT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
매개변수 힌트 `topic: str`과 독스트링은 서버 파일 도구와 같은 글입니다.
서버 파일 도구의 내놓는 값 힌트는 명세에 실리지 않아 적지 않았습니다.

다음 셀은 직접 도구의 명세를 만들어, MCP 도구의 명세와 견줍니다.
실행 전에 예상해 봅니다.
이름과 설명이 같다면, 두 명세의 글자 수도 같을까요?"""),
        code(DIRECT_SPEC),
        md("""**결과 읽기** — 출력 줄 `이름이 같은가: True`와 `설명이 같은가: True`가 보입니다.
라벨 `직접 도구 parameters 칸:` 뒤의 딕셔너리에는 칸 `additionalProperties`가 없습니다.
출력 줄 `직접 도구 명세 글자 수: 221`과 `MCP 도구 명세 글자 수: 252`가 보입니다.
출력 줄 `MCP 쪽이 긴 글자 수: 31`은 쉼표와 띄어쓰기를 넣은 `, "additionalProperties": false`의 글자 수와 같습니다.

칸 차례도 다릅니다. 직접 도구는 `properties`부터, MCP 도구는 `type`부터 적혀 있습니다.
이름과 설명이 같아도, 서버가 보낸 입력 형식을 그대로 싣는 MCP 도구는 명세가 조금 깁니다.
이 차이가 첫 요청의 입력 토큰에도 나타나는지는 5절에서 봅니다.

## 4. 설명 길이와 도구 수

Ch 19 03절에서는 설명을 늘리면 명세 글자 수가 늘었고, 도구가 늘수록 글자 수도 늘었습니다.
MCP 도구도 같은지 서버 쪽에서 두 가지를 하나씩 바꿔 봅니다.
먼저 설명만 두 문장 늘린 도구를 붙인 연습 서버를 만듭니다.
셀의 `@longer.tool` 줄은 02절처럼 아래 함수를 서버 `longer`의 도구로 등록합니다."""),
        code(DEF_LONG),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
독스트링의 앞 두 문장은 서버 파일 도구와 같습니다.
언제 쓰는지와 내놓는 값을 적은 두 문장을 뒤에 더했고, 네 문장을 한 줄에 적었습니다.

다음 셀은 연습 서버를 클래스 `MCPAdapter`에 넘겨 도구를 받습니다.
01절에서 `Client`에 서버 객체를 넘긴 것처럼, 서버 객체를 넘기면 메모리 연결로 붙습니다.
자식 프로세스를 띄우지 않아, 설정 딕셔너리가 필요 없습니다."""),
        code(LONG_LIST),
        md("""**결과 읽기** — 출력 줄 `받은 도구 이름: ['lookup_policy']`와 `입력 형식이 같은가: True`가 보입니다.
출력 줄 `설명이 같은가: False`로, 서버 파일 도구와 다른 것은 설명뿐입니다.

다음 셀은 늘어난 명세 글자 수와 늘어난 설명 글자 수를 견줍니다.
실행 전에 예상해 봅니다.
설명이 늘어난 만큼만 명세가 늘어날까요?"""),
        code(LONG_SPEC),
        md("""**결과 읽기** — 출력 줄 `설명을 늘린 판 명세 글자 수: 299`가 보입니다.
출력 줄 `늘어난 명세 글자 수: 47`과 `늘어난 설명 글자 수: 47`이 같고, `두 수가 같은가: True`입니다.
명세의 다른 칸은 그대로라, 늘어난 글자는 모두 설명에서 왔습니다.

다음은 도구 수를 바꿔 봅니다.
3절에서 받은 서버 객체 `server`에 도구 둘을 더 붙입니다.
파일은 고치지 않고, 이 커널 안의 서버 객체에만 붙습니다.

셀의 `@server.tool` 줄은 아래 함수를 서버 객체 `server`의 도구로 등록합니다.
첫째 도구는 규정 글에 낱말이 든 주제어를 찾습니다."""),
        code(DEF_SEARCH),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
몸통은 규정 딕셔너리의 주제어를 차례로 보며, 규정 글에 낱말이 든 주제어를 모읍니다.
이 절은 도구를 부르지 않고, 도구 정의만 봅니다.

다음 셀은 인자가 없는 도구 하나를 같은 서버 객체에 더 붙입니다."""),
        code(DEF_SHOW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
몸통은 규정 딕셔너리의 주제어를 목록으로 내놓습니다.

다음 셀은 도구 셋이 붙은 서버 객체를 메모리 연결로 넘겨 도구를 받습니다.
첫 도구의 명세가 2절에서 받은 도구의 명세와 같은지도 봅니다."""),
        code(WIDE_LIST),
        md("""**결과 읽기** — 출력 줄 `받은 도구 이름: ['lookup_policy', 'search_topics', 'show_topics']`가 보입니다.
출력 줄 `첫 도구 명세가 2절 명세와 같은가: True`로, 연결 방법이 달라도 같은 도구는 같은 명세였습니다.
2절은 서버를 자식 프로세스로 띄웠고, 이 셀은 같은 커널 안에서 메모리 연결로 붙였습니다.

다음 셀은 도구를 하나·둘·셋으로 늘리며 명세 글자 수를 셉니다.
Ch 19 03절처럼 슬라이싱 `[:count]`로 목록 앞에서부터 도구를 고릅니다."""),
        code(COUNT),
        md("""**결과 읽기** — 명세 글자 수는 도구 하나에서 `252`, 둘에서 `503`, 셋에서 `685`입니다.
도구 하나일 때의 252는 2절에서 센 MCP 도구 명세 글자 수와 같습니다.
둘째 도구 `search_topics`는 251자, 셋째 도구 `show_topics`는 182자를 더했습니다.
인자가 없는 셋째 도구는 명세가 짧아, 도구마다 더해지는 글자 수가 다릅니다.

## 5. 첫 요청의 입력 토큰

이제 실제 모델에 첫 요청을 보내, 도구 명세가 입력 토큰에 얼마나 더해지는지 셉니다.
첫 요청은 도구를 한 번도 부르기 전, 대화를 시작하는 모델 요청입니다.
도구 목록을 알린 모델 객체는 요청마다 도구 명세를 함께 싣습니다.
이 절은 도구를 알리기만 하고 부르지 않아서, 조건마다 요청은 한 번입니다.

다음 셀은 첫 요청에 실을 메시지 둘을 만듭니다.
시스템 메시지 글과 질문은 04절 에이전트에 준 글과 같습니다.
Ch 6 02절에서 본 메시지 객체 `SystemMessage`와 `HumanMessage`로 만듭니다."""),
        code(MESSAGES),
        md("""**결과 읽기** — 출력 줄 `첫 요청 메시지 수: 2`와 `첫 메시지 종류: SystemMessage`가 보입니다.
설치판 소스를 보면, 04절의 에이전트도 시스템 메시지를 맨 앞에 두고 요청마다 도구 목록을 알립니다.
그래서 이 절의 첫 요청은 04절 에이전트의 첫 요청과 같은 모양입니다.
이 절은 에이전트를 실행하지 않고, 모델 객체에 바로 보냅니다.

다음 셀은 도구를 알리지 않은 모델 `model`에 첫 요청을 보냅니다.
응답의 속성 `usage_metadata`는 Ch 6 01절에서 본 사용량 딕셔너리이고, 입력 토큰 칸이 있습니다.
실행 전에 예상해 봅니다.
도구를 모르는 모델은 이 질문에 어떻게 답할까요?"""),
        code(ASK_NONE),
        md("""**결과 읽기** — 출력 줄 `도구 호출 요청: []`과 `입력 토큰: 56`이 보입니다.
도구를 알리지 않아, 응답에는 도구 호출 요청이 없습니다.
입력 토큰 56은 서비스가 시스템 메시지 글과 질문을 센 값입니다.

이번 실행에서는 답 글이 `규정에서 확인되는 자료만으로는 교육센터 자료실의 토요일 운영 종료 시간이 명시되어 있지 않습니다.`였습니다.
도구가 없어, 모델은 서버 파일의 규정을 볼 수 없었습니다.
다시 실행한 새 커널과 노트북 밖 다섯 번 가운데 셋에서는 서버 규정에 없는 토요일 시각을 적었습니다.
서버 파일의 토요일 운영 시각은 10:00~17:00이고, 답 글은 실행마다 달라지는 값이라 결론에 쓰지 않습니다.

다음 셀은 2절에서 MCP 도구를 알린 모델 `mcp_model`로 같은 메시지를 보냅니다.
04절 3절에서 MCP 도구는 `invoke`로 부를 수 없었지만, 이 셀에서 `invoke`하는 것은 모델입니다.
도구는 부르지 않고 명세만 실리므로, 보통 부르기로 보낼 수 있습니다."""),
        code(ASK_MCP),
        md("""**결과 읽기** — 라벨 `도구 호출 요청:` 줄 다음에 출력 줄 `입력 토큰: 187`이 보입니다.
같은 메시지에 MCP 도구 명세 하나를 더 실으니, 입력 토큰이 56에서 187로 늘었습니다.
늘어난 131을 이 절에서는 도구 정의 몫이라고 부릅니다.
같은 메시지로 보낸 두 요청 가운데, 도구를 알린 요청이 더 쓴 입력 토큰입니다.

이번 실행에서는 모델이 첫 응답에서 도구 `lookup_policy`를 요청했습니다.
첫 요청만 보냈으므로, 이 요청을 받아 도구를 부르지는 않았습니다.
도구 호출 요청은 모델이 고르는 값이라 결론에 쓰지 않습니다.

다음 셀은 3절의 직접 도구를 알린 모델로 같은 메시지를 보냅니다.
3절에서 직접 도구의 명세는 MCP 도구보다 31자 짧았습니다.
실행 전에 예상해 봅니다.
입력 토큰도 줄어들까요?"""),
        code(ASK_DIRECT),
        md("""**결과 읽기** — 출력 줄 `입력 토큰: 187`로, MCP 도구를 알린 요청과 같습니다.
명세 글자는 31자 짧았지만, 입력 토큰은 줄지 않았습니다.
입력 토큰은 서비스가 센 값이라, 칸 `additionalProperties`가 어떻게 세졌는지는 이 출력으로 볼 수 없습니다.

도구 호출 요청은 모델이 고른 값이라 결론에 쓰지 않습니다.
이번 실행에서 모델이 고른 도구는 라벨 `도구 호출 요청:` 뒤에 보입니다.

다음 셀은 4절의 설명을 늘린 도구를 알린 모델로 보냅니다.
명세는 설명 두 문장만큼, 47자 길었습니다."""),
        code(ASK_LONG),
        md("""**결과 읽기** — 출력 줄 `입력 토큰: 218`로, MCP 도구 하나일 때의 187보다 31 늘었습니다.
늘어난 명세 47자는 모두 설명 글자였습니다.
설명이 늘면 입력 토큰도 늘었지만, 글자 수와 같은 수만큼 늘지는 않았습니다.

다음 셀은 4절의 도구 셋을 알린 모델로 보냅니다.
명세 글자 수는 도구 하나일 때 252, 셋일 때 685였습니다.
실행 전에 예상해 봅니다.
도구 정의 몫도 세 배쯤 될까요?"""),
        code(ASK_WIDE),
        md("""**결과 읽기** — 출력 줄 `입력 토큰: 252`가 보입니다.
2절의 명세 글자 수 252와 숫자가 같은 것은 우연이고, 하나는 글자 수, 하나는 토큰 수입니다.
도구 하나일 때보다 65 늘어, 도구 둘을 더 알린 몫은 첫 도구 하나의 몫 131보다 작았습니다.

다음 셀은 도구를 알린 네 요청의 입력 토큰에서, 도구 없는 요청의 입력 토큰을 뺍니다.
조건마다 도구 정의 몫을 한눈에 견주기 위해서입니다."""),
        code(TABLE),
        md("""**결과 읽기** — 네 줄의 도구 정의 몫은 차례로 `131`, `131`, `162`, `196`입니다.
명세 글자 수는 252·221·299·685였으니, 몫은 글자 수와 같은 비율로 늘지 않았습니다.
직접 도구와 MCP 도구는 명세 글자가 달라도 몫이 같았습니다.
도구 셋의 몫 196은 도구 하나의 몫 131의 세 배가 아니었습니다.

입력 토큰은 서비스가 센 값입니다.
노트북 밖에서 같은 다섯 요청을 조건마다 다섯 번 보냈을 때도 입력 토큰은 모두 이 값이었습니다.
새 커널로 두 번 실행했을 때도 다섯 요청의 입력 토큰은 두 번 모두 같았습니다.
다른 모델이나 다른 판에서는 달라질 수 있습니다.

마지막 셀은 다섯 요청의 출력 토큰과 예상 비용을 봅니다.
요금은 Ch 6 06절처럼 2026-09-17 요금표의 100만 토큰당 달러입니다.
함수 `estimate_cost`는 응답의 사용량 딕셔너리를 그대로 받아, 캐시 입력 칸까지 셉니다."""),
        code(COST),
        md("""**결과 읽기** — 라벨 `출력 토큰:` 줄 다섯에 요청마다 출력 토큰이 보입니다.
라벨 `예상 비용 합(달러):` 뒤에는 요금표로 어림한 다섯 요청의 비용 합이 보입니다.
예상 비용은 요금표로 어림한 값이고, 청구 금액이 아닙니다.

이번 실행에서는 출력 토큰이 도구 없는 요청 29, 도구를 알린 네 요청은 18씩이었습니다.
예상 비용 합은 0.00113달러였고, 도구를 알린 네 요청의 응답은 도구 호출 요청이었습니다.
다시 실행한 새 커널에서는 도구 없는 요청의 출력 토큰이 30이었습니다.
출력 토큰과 비용은 실행마다 달라질 수 있는 값이라 결론에 쓰지 않습니다.

## 정리

1. MCP 도구의 입력 형식은 도구 명세의 칸 `parameters`에 그대로 실렸고, 설명과 도구를 늘리면 명세 글자 수도 늘었습니다.
2. 흔들림 확인 다섯 번과 두 커널에서 모두, MCP 도구 하나의 정의는 첫 요청 입력 토큰을 131 늘렸습니다.
3. 같은 확인에서 이름·설명이 같은 직접 도구도 입력 토큰이 같아, MCP라서 입력이 늘지는 않았습니다.

06절은 이 챕터의 실습입니다.
에이전트에 붙이는 MCP 도구를 하나에서 셋으로 늘려, 도구를 부른 뒤의 요청에서도 입력 토큰이 늘어나는지 봅니다."""),
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


def link(url: str, label: str) -> str:
    return '<a href="' + url + '">' + label + "</a>"


L_CH05_01 = "../../part1/ch05-llm-principles/01-토큰화와-한국어-효율.html"
L_CH06_01 = "../../part2/ch06-langchain-start/01-계층-지도와-첫-호출.html"
L_CH06_02 = "../../part2/ch06-langchain-start/02-메시지와-제공자-전환.html"
L_CH06_06 = "../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html"
L_CH19_01 = "../../part5/ch19-model-tools/01-tool과-Ch4-함수-재사용.html"
L_CH19_03 = "../../part5/ch19-model-tools/03-좋은-도구-이름과-설명.html"
L_CH19_04 = "../../part5/ch19-model-tools/04-설명만으로-도구-선택하기.html"
L_CH27_03 = "../ch27-deepagents/03-플래닝과-시스템-프롬프트.html"
L_CH29_01 = "../ch29-agent-evaluation/01-에이전트-평가-세-전략.html"
L_01 = "01-MCP-구조와-capability-협상.html"
L_02 = "02-FastMCP-로컬-서버-제작.html"
L_03 = "03-stdio와-원격-전송-권한-경계.html"
L_04 = "04-LangChain-MCP-클라이언트-연동.html"

TERM_ROWS = [
    ("(이어 씀) 도구 명세", "모델에게 알리려고 도구의 이름·설명·입력 형식을 담은 딕셔너리입니다(Ch 19 03절 말). 보급선 조종사에게 먼저 보내는 모듈 설명서 한 권과 같습니다. 이 절에서는 함수 <code>convert_to_openai_tool</code>이 MCP 도구 하나로 만든 <code>policy_spec</code>입니다."),
    ("첫 요청(first request)", "도구를 한 번도 부르기 전, 대화를 시작하며 모델에게 보내는 요청입니다. 보급선을 처음 부를 때 짐과 함께 설명서 묶음부터 싣는 것과 같습니다. 이 절에서는 시스템 메시지 글과 질문을 담은 <code>first_messages</code>를 조건마다 한 번씩 보냅니다."),
    ("도구 정의 몫", "같은 메시지로 보낸 두 요청 가운데, 도구를 알린 요청이 더 쓴 입력 토큰입니다. 짐 무게에서 설명서 묶음의 무게만 떼어 보는 것과 같습니다. 이 절에서는 MCP 도구 하나를 알린 요청의 187에서 도구 없는 요청의 56을 뺀 131입니다. 흔들림 확인 다섯 번과 두 커널에서 모두 같은 값이었습니다."),
]

VALUE_ROWS = [
    ("명세의 칸 <code>parameters</code> = 입력 형식", "<code>True</code>", "설치판 <code>convert_to_openai_tool</code>(코드)"),
    ("명세 글자 수(MCP · 직접 · 설명을 늘린 판 · 도구 셋)", "252 · 221 · 299 · 685", "JSON 글의 글자 수(코드)"),
    ("늘어난 명세 = 늘어난 설명", "47 = 47, <code>True</code>", "코드"),
    ("첫 요청 입력 토큰(도구 없음 · MCP · 직접 · 설명을 늘린 판 · 도구 셋)", "56 · 187 · 187 · 218 · 252", "서비스가 셈(노트북 밖 다섯 번·두 커널 같음)"),
    ("도구 정의 몫(MCP · 직접 · 설명을 늘린 판 · 도구 셋)", "131 · 131 · 162 · 196", "위 입력 토큰의 차"),
    ("도구 호출 요청 · 출력 토큰 · 답 글 · 예상 비용", "이번 실행에서는 네 요청 모두 <code>lookup_policy</code> 요청 · 출력 토큰 29·18·18·18·18 · 예상 비용 합 0.00113달러", "모델·서비스 쪽 값이라 결론에 쓰지 않음"),
]

LOOK_B5 = "노트북 2절에서 <code>parameters 칸이 입력 형식과 같은가: True</code>와 <code>글자 수: 252</code>를 봅니다. 3절에서 <code>MCP 쪽이 긴 글자 수: 31</code>을, 4절에서 <code>두 수가 같은가: True</code>를 확인합니다. 4절 마지막 셀의 명세 글자 수 252·503·685도 봅니다."
LOOK_B6 = "노트북 5절에서 <code>입력 토큰: 56</code>과 <code>입력 토큰: 187</code>을 먼저 봅니다. 직접 도구 셀의 입력 토큰이 MCP 도구 셀과 같은지 확인합니다. 마지막 표에서 도구 정의 몫 <code>131</code>·<code>162</code>·<code>196</code>을 명세 글자 수와 견줍니다."

B7_ITEMS = [
    "입력 토큰은 서비스가 센 값입니다. 노트북 밖에서 조건마다 다섯 번 보냈을 때와 두 커널에서 모두 같았습니다. 다른 모델이나 다른 판에서는 달라질 수 있습니다.",
    "OpenAI 함수 호출 문서는 함수 정의가 모델이 배운 문법으로 시스템 메시지에 들어간다고 적습니다. 그래서 명세의 칸 <code>additionalProperties</code>가 입력 토큰에 들어가는지는 문서와 출력만으로 가를 수 없습니다. 이번 출력에서는 이 칸이 있는 명세와 없는 명세의 입력 토큰이 같았습니다.",
    "설치판 langchain 1.4.0 소스 <code>langchain/agents/factory.py</code> 998~1004행은 시스템 메시지 글을 <code>SystemMessage</code>로 만듭니다. 1431~1438행은 모델을 부를 때마다 도구 목록을 다시 알리고, 1500~1505행은 시스템 메시지를 맨 앞에 둡니다. 그래서 04절 에이전트의 첫 요청은 5절의 MCP 도구 하나 조건과 같은 모양입니다. 소스로만 확인했고, 이 노트북에서 에이전트를 실행해 견주지는 않았습니다.",
    "도구를 알린 에이전트는 요청마다 도구 명세를 다시 싣습니다. 도구를 여러 번 부르는 실행에서는 도구 정의 몫이 요청 수만큼 되풀이해 들어갈 수 있습니다. 이 절은 첫 요청만 셌고, 여러 요청의 합은 재지 않았습니다.",
    "이 절은 MCP 클라이언트와 서버가 주고받은 메시지의 크기를 재지 않았습니다. 입력 토큰은 모델 요청 하나를 서비스가 센 값이라, 서버와 주고받은 목록 요청은 들어가지 않습니다.",
    "현재 판 MCP 규격(2026-07-28)의 도구 문서는 서버가 도구를 정해진 차례로 내놓으라고 권합니다. 차례가 같으면 클라이언트가 목록을 저장해 두기 쉽다고 적습니다. 도구가 모델 요청에 들어갈 때 캐시 입력도 생기기 쉽다고 적습니다. 이 절은 그 동작을 실행하지 않았습니다.",
    "같은 규격은 도구 목록이 요청의 권한에 따라 달라질 수 있다고 적습니다. 03절처럼 접근 토큰의 범위로 관리 도구가 목록에서 빠지면, 모델에게 알리는 도구 정의도 줄어듭니다. 이 절에서는 그 조건으로 입력 토큰을 재지 않았습니다. 권한 검사는 입력을 줄이는 방법이 아니라, 누가 도구를 부를 수 있는지 막는 일입니다.",
    "5절의 요청은 <code>tool_choice</code> 없이 보냈고, 첫 요청만 보내 도구는 부르지 않았습니다. 도구를 알린 네 조건에서 모델이 도구를 요청할지는 모델이 고르는 값입니다. 노트북 밖 다섯 번에서는 네 조건 모두 첫 응답이 <code>lookup_policy</code> 요청이었습니다.",
    "도구를 알리지 않은 요청의 답은 노트북 밖 다섯 번 모두 달랐습니다. 셋은 서버 규정에 없는 토요일 시각을 적었고, 둘은 규정에서 확인되지 않는다고 답했습니다. 같은 요청도 실행한 때에 따라 모델이 쓰는 글이 달라질 수 있습니다.",
    "명세 글자 수는 셀에서 <code>json.dumps</code>로 바꾼 글의 길이입니다. 실제 요청 본문은 띄어쓰기나 한글을 적는 방법이 다를 수 있어, 요청 크기로 읽지 않습니다. 설치판 langchain-core 1.6.2 <code>utils/function_calling.py</code> 345~352행이 명세를 만드는 자리입니다. 입력 형식이 딕셔너리인지 양식 클래스인지에 따라 다른 함수로 명세를 만듭니다.",
    "4절에서 서버 객체에 붙인 도구 둘은 이 커널 안에서만 붙었고, 서버 파일은 그대로입니다. 두 도구는 이 절에서 부르지 않았습니다.",
    "캐시 입력은 노트북 밖 스물다섯 요청 모두 0이었습니다. 예상 비용은 2026-09-17 요금표로 어림한 값이고, 청구 금액이 아닙니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 걸린 시간은 재지 않았습니다.",
]

QUIZ = [
    ("MCP 도구의 입력 형식 딕셔너리는 도구 명세의 어느 칸에 실렸나요?",
     "칸 <code>function</code> 안의 칸 <code>parameters</code>입니다. 2절 출력 <code>parameters 칸이 입력 형식과 같은가: True</code>로 확인했습니다. 틀렸다면 노트북 2절을 다시 읽습니다."),
    ("설명만 두 문장 늘린 도구의 명세 글자 수는 얼마나 늘었고, 무엇과 같았나요?",
     "47자 늘었고, 늘어난 설명 글자 수 47과 같았습니다. 명세의 다른 칸은 그대로라, 늘어난 글자는 모두 설명에서 왔습니다. 틀렸다면 노트북 4절을 다시 읽습니다."),
    ("도구 없는 첫 요청은 입력 토큰 56, MCP 도구 하나를 알린 첫 요청은 187이었습니다. 도구 정의 몫은 얼마인가요?",
     "131입니다. 같은 메시지로 보낸 두 요청의 입력 토큰 차이입니다. 흔들림 확인 다섯 번과 두 커널에서 모두 같은 값이었습니다. 틀렸다면 노트북 5절을 다시 읽습니다."),
    ("직접 도구의 명세는 MCP 도구보다 31자 짧았습니다. 입력 토큰도 줄었나요?",
     "줄지 않았습니다. 같은 확인에서 두 요청 모두 187이었습니다. 명세 글자 수는 우리가 센 값이고 입력 토큰은 서비스가 센 값이라, 같은 비율로 움직이지 않았습니다. 틀렸다면 노트북 5절의 직접 도구 셀을 다시 읽습니다."),
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
    terms = table_html(["말", "뜻"], TERM_ROWS)
    values = table_html(["본 것", "이번 출력", "무엇이 정했나"], VALUE_ROWS)
    b7 = "".join("<li>" + item + "</li>" for item in B7_ITEMS)
    return ("""<!--meta: 강의 1h | 실습 2h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 2 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>MCP 도구의 입력 형식이 도구 명세의 어느 칸에 실리는지 출력으로 짚을 수 있습니다.</li>
<li>입력 형식 모양·설명 길이·도구 수를 하나씩 바꾸며 명세 글자 수를 셀 수 있습니다.</li>
<li>도구 없는 첫 요청과 견주어, 도구 정의가 더한 입력 토큰을 셀 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>""" + link(L_04, "04절") + """에서는 MCP 서버의 도구를 LangChain 도구로 바꿔 에이전트에 붙였습니다. 모델이 도구를 고르려면, 먼저 도구의 이름·설명·입력 형식을 읽어야 합니다. 그래서 도구를 알린 모델 요청에는 도구 명세가 함께 실리고, 그만큼 입력 토큰을 씁니다. 서버가 도구를 많이 알릴수록, 도구를 한 번도 부르지 않은 첫 요청부터 입력이 커질 수 있습니다.</p><p>MCP 서버에서 도구를 가져오면, 서버가 적은 정의를 손대지 않고 그대로 싣게 됩니다. 이 절은 그 정의가 명세의 어느 칸에 들어가는지 모델 없이 먼저 봅니다. 그다음 같은 메시지로 첫 요청을 보내, 도구 정의가 입력 토큰에 얼마나 더해지는지 셉니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>""" + link(L_CH05_01, "Ch 5 01절") + """에서는 모델이 글을 토큰으로 나눠 세고, 글자 수와 토큰 수가 어긋나는 것을 보았습니다. """ + link(L_CH06_01, "Ch 6 01절") + """은 응답의 속성 <code>usage_metadata</code>에서 입력·출력 토큰을 읽었습니다. """ + link(L_CH06_02, "02절") + """은 메시지 객체 <code>SystemMessage</code>와 <code>HumanMessage</code>를 보였습니다. """ + link(L_CH06_06, "06절") + """은 요금표와 함수 <code>estimate_cost</code>로 예상 비용을 어림했습니다.</p><p>""" + link(L_CH19_01, "Ch 19 01절") + """에서는 함수 <code>convert_to_openai_tool</code>로 도구 명세를 보았습니다. """ + link(L_CH19_03, "03절") + """은 함수 <code>spec_length</code>로 명세 글자 수를 세고, 설명이나 도구를 늘리면 글자 수가 늘어나는 것을 보았습니다. 그 절은 모델을 부르지 않아 토큰 수는 세지 않았습니다. """ + link(L_CH19_04, "04절") + """은 메서드 <code>bind_tools</code>로 모델에게 도구를 알리고, 설명만 바꾼 두 판의 입력 토큰을 견주었습니다. """ + link(L_CH27_03, "Ch 27 03절") + """은 도구 설명과 할 일 설명 글이 더 실린 실행의 첫 요청 입력 토큰을 견주었습니다.</p><p>""" + link(L_01, "01절") + """은 서버가 알린 도구 정의의 입력 형식을 보았고, """ + link(L_02, "02절") + """ 6절은 서버 파일을 <code>runpy.run_path</code>로 이 커널에서 읽었습니다. """ + link(L_03, "03절") + """은 함수 <code>stdio_config</code>로 서버 파일을 자식 프로세스로 띄웠습니다. """ + link(L_04, "04절") + """은 클래스 <code>MCPAdapter</code>로 MCP 도구를 <code>StructuredTool</code>로 바꿨고, 입력 형식은 딕셔너리 그대로였습니다. 이 절은 그 딕셔너리가 모델에게 가는 모양과, 첫 요청의 입력 토큰을 봅니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>우주 정거장의 관제실이 보급선을 부른다고 합시다. 관제실은 보급선을 부를 때마다, 정거장에 붙은 모듈마다 설명서 한 권씩을 먼저 실어 보냅니다. 보급선 조종사는 그 설명서를 읽어야, 어느 모듈에 무엇을 가져갈지 정할 수 있습니다. 모듈이 셋이면 설명서도 세 권이라, 보급선에 실리는 짐이 늘어납니다.</p><p>모듈이 MCP 서버의 도구이고, 설명서 한 권이 도구 명세 하나입니다. 조종사가 모델이고, 보급선을 부르는 일이 모델 요청이며, 실린 짐의 무게가 입력 토큰입니다. 이 절은 보급선을 처음 부를 때, 곧 첫 요청의 짐만 잽니다.</p><p>비유와 다른 점도 있습니다. 설명서의 글자 수와 모델이 센 입력 토큰은 같은 비율로 늘지 않았습니다. 이름과 설명이 같은 직접 도구는 명세가 31자 짧았습니다. 그래도 입력 토큰은 MCP 도구와 같았고, 흔들림 확인 다섯 번과 두 커널에서 모두 그랬습니다.</p>
""" + illustration_block() + """<h3>도구 정의가 도구 명세가 되기까지</h3><p>01절에서 본 것처럼 MCP 서버는 도구마다 이름·설명·입력 형식을 담은 도구 정의를 알립니다. 04절의 클래스 <code>MCPAdapter</code>는 그 정의를 받아 LangChain 도구로 바꿨고, 입력 형식은 딕셔너리 그대로였습니다. 이 도구를 모델에게 알리면, 함수 <code>convert_to_openai_tool</code>이 만든 도구 명세가 요청에 실립니다. 명세의 칸 <code>parameters</code>에는 서버가 보낸 입력 형식이 그대로 들어갑니다.</p>
""" + terms + """
<p>새 말을 이 절 코드에서 보면 이렇습니다. 첫 요청은 조건마다 한 번씩 보낸 <code>invoke(first_messages)</code>입니다. 도구 정의 몫은 5절 표의 <code>도구 정의 몫: 131</code>처럼 출력에 보입니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>명세 글자 수를 바꾸는 것</h3><p>명세 글자 수는 명세를 JSON 글로 바꿔 센 값이라, 코드가 정합니다. 이 절은 세 가지를 하나씩 바꿔 봅니다. 입력 형식 모양만 다른 직접 도구, 설명만 두 문장 늘린 도구, 도구를 셋으로 늘린 서버입니다. 늘어난 설명 글자 수만큼 명세도 늘었고, 도구를 더하면 그 도구의 명세만큼 늘었습니다.</p>
<h3>첫 요청 입력 토큰</h3><p>입력 토큰은 서비스가 요청을 받아 센 값입니다. OpenAI 문서는 함수 정의가 모델이 배운 문법으로 시스템 메시지에 들어가, 입력 토큰으로 청구된다고 적습니다. 그래서 명세의 JSON 글자 수와 입력 토큰은 같은 값이 아니고, 같은 비율로 늘지도 않을 수 있습니다. 이 절은 같은 메시지로 조건마다 첫 요청을 보내, 입력 토큰의 차이로 도구 정의 몫을 셉니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 04절 설정으로 서버 파일의 도구를 받아, 도구 명세의 칸과 글자 수를 봅니다. 3절은 이름·설명이 같은 직접 도구를, 4절은 설명을 늘린 도구와 도구 셋을 만들어 명세 글자 수를 셉니다. 5절은 같은 메시지로 조건 다섯에 첫 요청을 한 번씩 보내 입력 토큰을 봅니다.</p><p>모델 요청은 5절에서만 나가고 모두 5번입니다. 요금표로 어림한 예상 비용은 합쳐서 0.002달러 아래입니다. 노트북이 쓰는 파일은 없고, 걸린 시간은 재지 않았습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>노트북 2~4절은 모델 없이 도구 명세를 보았습니다. MCP 도구의 입력 형식은 칸 <code>parameters</code>에 그대로 실렸고, 명세 글자 수는 252였습니다. 직접 도구는 칸 <code>additionalProperties</code>가 없어 31자 짧았고, 설명을 두 문장 늘리자 명세도 설명만큼 47자 늘었습니다. 도구를 셋으로 늘리자 명세 글자 수는 685가 되었습니다.</p><p>노트북 5절은 같은 메시지로 첫 요청을 조건마다 한 번씩 보냈습니다. 흔들림 확인 다섯 번과 두 커널에서 모두, 도구 없는 요청의 입력 토큰은 56이었습니다. MCP 도구 하나를 알린 요청은 187이라, 도구 정의 하나가 첫 요청 입력 토큰을 131 늘린 셈입니다.</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>같은 확인에서 직접 도구를 알린 요청도 187로, MCP 도구와 같았습니다. MCP 서버에서 가져온 도구라서 입력이 늘어난 것이 아니라, 도구 정의를 실어서 늘어났습니다. 설명을 늘린 도구는 218, 도구 셋은 252였고, 도구 정의 몫은 162와 196이었습니다. 명세 글자 수가 달라진 만큼 몫이 늘지는 않았고, 도구 셋의 몫은 도구 하나의 세 배가 아니었습니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + values + """
<p>표의 위 셋은 코드가 정하는 값입니다. 가운데 둘은 서비스가 센 값이고, 노트북 밖 다섯 번과 두 커널에서 모두 같았습니다. 맨 아래 줄은 모델이 고르거나 쓴 값이라, 결론에는 쓰지 않습니다.</p><p>새 커널로 두 번 실행해 견주자, 코드 셀 스물여덟 가운데 스물여섯의 출력이 셀마다 같았습니다. 달랐던 두 셀은 도구 없는 요청의 답 글이 찍힌 셀과, 그 요청의 출력 토큰과 예상 비용이 찍힌 셀입니다. 명세 글자 수와 다섯 요청의 입력 토큰은 두 번 모두 같았고, 이 값만 결론과 그림에 썼습니다.</p>
<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul>""" + b7 + """</ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>MCP 도구의 입력 형식은 도구 명세의 칸 <code>parameters</code>에 그대로 실렸고, 설명과 도구를 늘리면 명세 글자 수도 늘었습니다.</li><li>흔들림 확인 다섯 번과 두 커널에서 모두, MCP 도구 하나의 정의는 첫 요청 입력 토큰을 131 늘렸습니다.</li><li>같은 확인에서 이름·설명이 같은 직접 도구도 입력 토큰이 같아, MCP라서 입력이 늘지는 않았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — """ + link("06-MCP-실습.html", "06절") + """은 이 챕터의 실습입니다. 에이전트에 붙이는 MCP 도구를 하나에서 셋으로 늘려, 도구를 부른 뒤의 요청에서도 입력 토큰이 늘어나는지 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>""" + quiz_html() + """
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://modelcontextprotocol.io/specification/2026-07-28/server/tools">MCP Specification 2026-07-28 · Tools</a></div>확인 2026-09-28 · 서버가 도구를 정해진 차례로 내놓으라고 권합니다. 차례가 같으면 목록을 저장해 두기 쉽고, 캐시 입력도 생기기 쉽다고 적습니다. 도구 목록은 요청에 담긴 권한에 따라 달라질 수 있다고도 적습니다.</li><li><div><a href="https://developers.openai.com/api/docs/guides/function-calling">OpenAI Function calling</a></div>확인 2026-09-28 · 함수 정의가 모델이 배운 문법으로 시스템 메시지에 들어가고, 입력 토큰으로 청구된다고 적습니다. 토큰 한도에 닿으면 처음에 싣는 함수 수를 줄이거나 설명을 줄이라고 제안합니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langchain/mcp">LangChain MCP</a></div>확인 2026-09-28 · 클래스 <code>MCPAdapter</code>가 MCP 서버의 도구를 LangChain 도구로 바꾼다고 적습니다.</li><li>설치판 langchain-core 1.6.2 소스 <code>utils/function_calling.py</code> 345~352행은 도구 명세를 만드는 자리입니다. langchain 1.4.0 소스 <code>langchain/agents/factory.py</code>의 세 자리는 주의할 점에 적었습니다.</li><li>Ch 19 03절에서 명세 글자 수를, 04절에서 설명만 바꾼 두 판의 입력 토큰을 보았습니다. Ch 6 06절에서 요금표와 예상 비용을 보았습니다.</li></ul>
""")


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


if __name__ == "__main__":
    # 파일 위치 셀은 01절 셀 글, 조용히 하는 셀은 03절 셀 글 그대로(「같은 셀」 문장의 근거)
    assert FIND_FILE in (HERE / "author_01.py").read_text(encoding="utf-8"), "FIND_FILE이 01절 셀과 다릅니다"
    assert QUIET in author_03.notebook_code_sources(NB03), "QUIET이 03절 노트북 셀과 다릅니다"
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
        path = write_notebook(LAB, "05", SLUG, "experiment", cells())
        print("wrote", path)
