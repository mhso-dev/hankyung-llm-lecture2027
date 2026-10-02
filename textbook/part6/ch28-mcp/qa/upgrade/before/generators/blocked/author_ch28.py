# 2026-09-28 Ch 28 01절 품질 개선: 옛 원고(_src 다섯)·노트북 다섯·chapter.json을 만드는 옛 생성기입니다.
# 개선본은 절마다 qa/upgrade/author_NN.py가 대신합니다(QUALITY-UPGRADE.md §8, PLAYBOOK §2-1).
# 이 파일을 실행하면 옛 판(chapter.json 포함)을 다시 쓰려 하므로, 아래 줄에서 실행을 막습니다. 옮기기(mv -n)는 챕터 마감 몫입니다.
from __future__ import annotations
raise SystemExit("옛 Ch 28 원고·노트북·chapter.json 생성기입니다. 개선본은 qa/upgrade/author_NN.py를 쓰세요.")

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHAPTER = ROOT / "textbook/part6/ch28-mcp"
LAB = ROOT / "labs/part6/ch28-mcp"


def md(text: str, part: str | None = None) -> dict:
    metadata = {"lesson_part": part} if part else {}
    return {"cell_type": "markdown", "id": "", "metadata": metadata, "source": text.splitlines(keepends=True)}


def code(text: str, part: str | None = None) -> dict:
    metadata = {"lesson_part": part} if part else {}
    return {"cell_type": "code", "execution_count": None, "id": "", "metadata": metadata, "outputs": [], "source": text.splitlines(keepends=True)}


INSTALL = '''%pip install -q "langchain[mcp]==1.4.0" langchain-openai==1.6.0 fastmcp==4.0.3 mcp==2.2.0 python-dotenv==1.2.3
import warnings
from importlib.metadata import version
from langchain_core._api import LangChainBetaWarning

warnings.filterwarnings("ignore", message=r".*langchain\\.mcp.*", category=LangChainBetaWarning)

for package in ["langchain", "langchain-openai", "fastmcp", "mcp"]:
    print(package, version(package))'''

SERVER_LOAD = '''import importlib.util
from pathlib import Path

server_path = Path.cwd() / "labs/part6/ch28-mcp/course_server.py"
assert server_path.is_file(), f"서버 파일을 찾지 못했습니다: {server_path}"
spec = importlib.util.spec_from_file_location("course_server", server_path)
course_server = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(course_server)
print("server:", course_server.mcp.name)'''

LESSONS = {
"01-MCP-구조와-capability-협상": {
"title": "MCP 구조와 capability 협상", "format": "experiment", "hours": "강의 1h · 실습 2h", "terms": "6",
"question": "MCP 클라이언트와 서버는 도구·리소스·프롬프트를 어떻게 구분하고 서로 지원하는 기능을 어떻게 확인할까요?",
"goals": ["초기화와 capability 협상의 순서를 설명할 수 있습니다.", "도구·리소스·프롬프트의 책임을 구분할 수 있습니다.", "FastMCP 클라이언트로 세 종류를 발견하고 실제 결과를 읽을 수 있습니다."],
"why": "Ch19에서는 Python 함수를 모델이 읽을 도구 스키마로 바꾸었습니다. 그 함수는 같은 프로그램 안에 있었습니다. Ch28에서는 기능을 별도 프로세스나 원격 서비스로 옮기고 여러 클라이언트가 같은 방식으로 발견하도록 만드는 MCP(Model Context Protocol)를 배웁니다. 먼저 프로토콜이 무엇을 주고받는지 알아야 서버 코드, 전송 방식, 모델 토큰을 서로 다른 층으로 구분할 수 있습니다.",
"prior": "Ch6에서 모델·프레임워크·하네스 계층을 구분했고, Ch19에서 도구 이름·설명·입력 스키마가 모델 선택에 영향을 준다는 사실을 확인했습니다. Ch27에서는 파일시스템과 하위 작업 기능을 미리 조립한 하네스를 사용했습니다. MCP는 이러한 기능을 클라이언트와 서버 사이의 표준 메시지로 제공하지만, 모델의 판단이나 업무 권한을 자동으로 해결하지는 않습니다.",
"concept": "호텔 안내 데스크를 떠올려 봅니다. 손님이 요청할 수 있는 서비스 목록은 도구(tools), 읽을 수 있는 안내서는 리소스(resources), 직원에게 건넬 수 있는 작성 양식은 프롬프트(prompts)에 해당합니다. MCP에서 도구는 서버가 실행하는 호출 가능한 기능입니다. 리소스는 URI로 식별하는 읽을 자료입니다. 프롬프트는 사용자가 명시적으로 선택해 가져오는 재사용 메시지 틀입니다. 연결이 시작되면 클라이언트와 서버는 initialize 요청과 응답으로 프로토콜 버전과 capability를 교환합니다. 서버가 resources capability를 알리지 않았다면 클라이언트는 resources/list를 당연히 사용할 수 있다고 가정해서는 안 됩니다. 협상은 기능 존재를 확인하는 절차이고, 호출 권한을 부여하는 인증 절차와는 다릅니다.",
"definition": "MCP는 클라이언트와 서버가 JSON-RPC 2.0 메시지로 기능과 데이터를 교환하는 응용 계층 프로토콜입니다. 클라이언트는 호스트 애플리케이션 안에서 서버 연결을 관리하고, 서버는 한정된 기능을 공개합니다. 초기화 요청에는 클라이언트가 지원하는 프로토콜 버전과 capability가 들어가며 서버 응답에도 선택한 버전과 서버 capability가 들어갑니다. 이 왕복이 끝난 뒤 initialized 알림을 보내면 정상 동작 단계로 넘어갑니다. tools/list는 호출 가능한 도구 정의, resources/list는 고정 URI 자료, prompts/list는 재사용 프롬프트 정의를 반환합니다. 목록 조회와 실제 사용은 각각 tools/call, resources/read, prompts/get으로 분리됩니다.",
"observe": "실험은 같은 FastMCP 서버를 메모리 안에서 연결합니다. 네트워크와 하위 프로세스의 변동을 제거하고 발견 결과에 집중합니다. list_tools, list_resources, list_prompts는 각각 한 항목을 반환합니다. lookup_policy 도구 호출은 대출 규정 문자열을 반환하고 policy://handbook 리소스는 세 규정을 담습니다. explain_policy 프롬프트는 입력한 주제를 포함하는 사용자 메시지를 반환합니다. 세 목록의 개수가 같다는 사실보다 결과의 역할과 호출 방법이 다르다는 점을 확인합니다.",
"notes": ["MCP의 JSON-RPC 메시지와 모델에게 전달되는 프롬프트는 같은 데이터가 아닙니다. 서버 발견 결과 중 모델에 도구 정의로 넣은 내용만 모델 입력 토큰에 포함됩니다.", "서버가 capability를 알렸다는 사실은 해당 사용자가 모든 기능을 호출할 수 있다는 뜻이 아닙니다. 인증 뒤에도 도구별 권한 확인이 필요합니다.", "커리큘럼의 MCP 2026-07은 개강 기준 목표 버전입니다. 2026-09-11 공식 사이트에서 확인한 최신 발행 스펙은 2025-11-25이므로 본문은 확인 가능한 스펙을 기준으로 작성했습니다."],
"next": "다음 절에서는 한 파일에 도구·리소스·프롬프트를 등록하고 stdio로 실행되는 FastMCP 서버를 완성합니다.",
"quiz": [("도구와 리소스의 가장 큰 차이는 무엇인가요?", "도구는 서버가 실행하는 기능이고, 리소스는 URI로 읽는 자료입니다."), ("프롬프트는 언제 사용되나요?", "클라이언트 사용자가 이름과 인자를 지정해 재사용 메시지 틀을 가져올 때 사용됩니다."), ("capability 협상으로 확인할 수 없는 것은 무엇인가요?", "사용자의 실제 호출 권한은 별도의 인증·인가 검사로 확인해야 합니다."), ("도구 목록 개수와 모델 입력 토큰을 같은 수치로 볼 수 있나요?", "아닙니다. 목록 개수는 프로토콜 발견 결과이고 입력 토큰은 모델에 직렬화해 전달한 내용의 토큰화 결과입니다.")],
"cells": [("패키지 버전 확인", INSTALL), ("학생용 서버 불러오기", SERVER_LOAD), ("세 capability 발견", '''import asyncio
from fastmcp import Client

async def discover() -> tuple[list, list, list]:
    async with Client(course_server.mcp) as client:
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()
        return tools, resources, prompts

tools, resources, prompts = await discover()
print("tools:", [item.name for item in tools])
print("resources:", [str(item.uri) for item in resources])
print("prompts:", [item.name for item in prompts])
assert (len(tools), len(resources), len(prompts)) == (1, 1, 1)'''), ("도구·리소스·프롬프트 실제 사용", '''async def use_components() -> tuple[object, list, object]:
    async with Client(course_server.mcp) as client:
        tool_result = await client.call_tool("lookup_policy", {"topic": "대출"})
        resource_result = await client.read_resource("policy://handbook")
        prompt_result = await client.get_prompt("explain_policy", {"topic": "대출"})
        return tool_result, resource_result, prompt_result

tool_result, resource_result, prompt_result = await use_components()
print("tool:", tool_result.content[0].text)
print("resource:", resource_result[0].text)
print("prompt:", prompt_result.messages[0].content.text)
assert "14일" in tool_result.content[0].text
assert "운영:" in resource_result[0].text
assert "대출" in prompt_result.messages[0].content.text''')]
},
"02-FastMCP-로컬-서버-제작": {
"title": "FastMCP 로컬 서버 제작", "format": "paired", "hours": "강의 1h · 실습 3h", "terms": "5",
"question": "일반 Python 함수를 MCP 클라이언트가 발견하고 호출할 수 있는 서버 구성 요소로 만들려면 무엇을 등록해야 할까요?",
"goals": ["FastMCP 인스턴스에 도구·리소스·프롬프트를 등록할 수 있습니다.", "등록하지 않은 함수와 @mcp.tool 함수를 발견 결과로 비교할 수 있습니다.", "독립 실행 가능한 course_server.py를 stdio 서버로 제공할 수 있습니다."],
"why": "프로토콜 구조를 알아도 서버가 기능을 공개하지 않으면 클라이언트는 아무것도 발견하지 못합니다. FastMCP는 Python 함수의 타입 힌트와 docstring에서 입력 스키마와 설명을 만들고, 장식자(decorator)로 구성 요소 종류를 등록합니다. 이 절에서 만든 서버 파일은 다음 세 절에서 그대로 실행하므로 학생이 복사할 기준 파일이 됩니다.",
"prior": "앞 절에서 list_tools, list_resources, list_prompts와 실제 호출 방법을 확인했습니다. Ch4에서 함수와 타입 힌트를, Ch19에서 @tool 장식자와 입력 스키마를 배웠습니다. FastMCP의 @mcp.tool은 LangChain의 @tool과 이름이 비슷하지만 서로 다른 등록소에 함수를 넣습니다.",
"concept": "게시판에 종이를 붙이지 않으면 방문자는 종이가 있다는 사실을 알 수 없습니다. Python 함수도 FastMCP 인스턴스에 등록해야 MCP 발견 요청에 나타납니다. @mcp.tool은 실행 가능한 기능, @mcp.resource(URI)는 읽을 자료, @mcp.prompt는 재사용 메시지를 등록합니다. 함수 이름은 기본 구성 요소 이름이 되고 docstring은 설명이 됩니다. 인자의 타입 힌트는 JSON Schema 입력 정의를 만듭니다. 서버 파일 마지막의 if __name__ == '__main__' 블록은 파일을 직접 실행할 때 stdio 전송을 시작합니다. 이 블록이 있어야 다른 클라이언트가 파일을 하위 프로세스로 실행할 수 있습니다.",
"definition": "FastMCP는 MCP 서버와 클라이언트를 Python으로 구현하는 프레임워크입니다. FastMCP 인스턴스는 등록된 구성 요소와 서버 설정을 보관합니다. @mcp.tool이 붙은 함수는 이름, 설명, 입력 스키마와 실행 함수를 가진 도구가 됩니다. @mcp.resource에는 클라이언트가 요청할 URI를 지정하고, @mcp.prompt 함수에는 프롬프트 인자를 타입으로 선언합니다. course_server.py는 외부 API나 사용자 파일을 읽지 않고 모듈 안의 공개 규정 딕셔너리만 반환합니다. 이 제한 덕분에 서버 제작과 프로토콜 호출을 외부 상태 변경 없이 반복할 수 있습니다.",
"observe": "Before에서는 lookup_policy와 이름이 같은 일반 함수를 만들지만 @mcp.tool을 붙이지 않습니다. list_tools 결과는 빈 목록이고 call_tool은 UnknownToolError를 발생시킵니다. After에서는 같은 인자와 반환 규칙을 유지하고 장식자로 등록합니다. 목록에 lookup_policy가 나타나고 대출을 입력하면 14일 규정이 반환됩니다. 비교한 원인은 함수 등록 여부 하나입니다. 실제 배포 파일에는 도구뿐 아니라 handbook 리소스와 explain_policy 프롬프트도 포함합니다.",
"notes": ["도구 docstring은 모델이 어떤 기능을 언제 호출할지 판단하는 자료가 됩니다. 내부 구현 설명보다 입력 범위와 반환 내용을 구체적으로 적습니다.", "도구는 읽기 전용으로 만들었습니다. 파일 삭제·메일 발송·결제처럼 되돌리기 어려운 동작에는 승인, 중복 방지, 감사 로그를 추가해야 합니다.", "stdio 서버에서 일반 print를 표준 출력에 쓰면 프로토콜 메시지를 손상할 수 있습니다. 진단 로그는 표준 오류나 FastMCP 로깅 기능으로 보냅니다.", "학생 배포 파일은 course_server.py, 다섯 개 노트북, pyproject.toml, uv.lock입니다. .env와 실행 환경의 비밀 값은 배포 목록에 포함하지 않습니다."],
"next": "다음 절에서는 완성한 course_server.py를 실제 하위 프로세스로 실행하고 stdio와 원격 HTTP의 신뢰 경계를 비교합니다.",
"quiz": [("일반 함수가 list_tools에 나타나지 않는 이유는 무엇인가요?", "FastMCP 인스턴스에 도구로 등록되지 않았기 때문입니다."), ("타입 힌트는 MCP 도구에서 어디에 쓰이나요?", "클라이언트가 받는 도구 입력 JSON Schema를 만드는 데 쓰입니다."), ("stdio 서버가 표준 출력에 임의 문자열을 쓰면 왜 문제인가요?", "클라이언트가 JSON-RPC 메시지로 해석해야 할 스트림에 다른 문자열이 섞이기 때문입니다."), ("course_server.py의 기능이 읽기 전용인 이유는 무엇인가요?", "학습 중 잘못된 호출이 외부 상태를 바꾸지 않도록 실행 위험을 제한하기 위해서입니다.")],
"cells": [("패키지 버전 확인", INSTALL), ("Before: 등록하지 않은 함수", '''import asyncio
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError

before = FastMCP("등록 전 서버")

def lookup_policy(topic: str) -> str:
    return {"대출": "14일"}[topic]

async def run_before() -> tuple[list[str], str]:
    async with Client(before) as client:
        names = [item.name for item in await client.list_tools()]
        try:
            await client.call_tool("lookup_policy", {"topic": "대출"})
        except ToolError as error:
            return names, type(error).__name__

before_names, before_error = await run_before()
print("tools:", before_names)
print("error:", before_error)
assert before_names == []''', "before"), ("After: 도구 등록", '''after = FastMCP("등록 후 서버")

@after.tool
def lookup_policy(topic: str) -> str:
    """자료실 규정을 조회합니다. topic은 대출입니다."""
    return {"대출": "일반 도서는 14일 동안 대출할 수 있습니다."}[topic]

async def run_after() -> tuple[list[str], str]:
    async with Client(after) as client:
        names = [item.name for item in await client.list_tools()]
        result = await client.call_tool("lookup_policy", {"topic": "대출"})
        return names, result.content[0].text

after_names, after_text = await run_after()
print("tools:", after_names)
print("result:", after_text)
assert after_names == ["lookup_policy"]
assert "14일" in after_text''', "after"), ("완성 서버의 세 구성 요소 확인", SERVER_LOAD + '''

async def inspect_server() -> tuple[list[str], list[str], list[str]]:
    async with Client(course_server.mcp) as client:
        return (
            [item.name for item in await client.list_tools()],
            [str(item.uri) for item in await client.list_resources()],
            [item.name for item in await client.list_prompts()],
        )

print(await inspect_server())''', "after")]
},
"03-stdio와-원격-전송-권한-경계": {
"title": "stdio와 원격 전송·권한 경계", "format": "paired", "hours": "강의 1h · 실습 2h", "terms": "7",
"question": "로컬 stdio 서버와 원격 Streamable HTTP 서버는 실행 주체·비밀 전달·권한 확인의 경계가 어떻게 다를까요?",
"goals": ["클라이언트가 course_server.py를 stdio 하위 프로세스로 실행할 수 있습니다.", "stdio와 Streamable HTTP의 프로세스·네트워크 경계를 비교할 수 있습니다.", "하위 프로세스 환경 변수와 원격 Authorization 헤더를 최소 범위로 구성할 수 있습니다."],
"why": "같은 도구 목록을 제공해도 서버가 어디에서 실행되는지에 따라 위험이 달라집니다. stdio에서는 클라이언트가 로컬 하위 프로세스를 만들고 표준 입력과 출력으로 통신합니다. 원격 서버에서는 이미 실행 중인 HTTP 서비스에 연결합니다. 코드를 그대로 옮기기 전에 누가 서버를 시작하고 어떤 비밀과 파일에 접근할 수 있는지 선을 그어야 합니다.",
"prior": "앞 절에서 course_server.py의 main 블록이 stdio 전송을 시작하도록 작성했습니다. Ch16에서 허용 목록과 최소 권한을 다뤘고, Ch24에서 사람이 승인해야 하는 작업 경계를 확인했습니다. 여기서는 인증(authentication: 누구인지 확인)과 인가(authorization: 무엇을 할 수 있는지 결정)를 구분합니다.",
"concept": "stdio는 같은 컴퓨터 안의 전용 통로입니다. 클라이언트가 서버 프로세스의 시작과 종료를 관리하며 네트워크 포트를 열지 않습니다. 그러나 하위 프로세스는 전달받은 환경 변수와 운영체제 권한으로 로컬 파일에 접근할 수 있습니다. Streamable HTTP는 네트워크 주소의 서비스에 연결하며 여러 클라이언트가 사용할 수 있습니다. TLS, Origin 검사, 인증 토큰, 사용자별 인가가 필요합니다. MCP 공식 스펙은 stdio에 HTTP 인증 절차를 적용하지 말고 환경에서 자격 정보를 가져오도록 구분합니다. HTTP에서는 Authorization 헤더나 OAuth 흐름을 쓸 수 있지만, 헤더가 있다는 사실만으로 모든 도구를 허용해서는 안 됩니다.",
"definition": "전송(transport)은 JSON-RPC 메시지를 어느 통로로 옮길지 정합니다. stdio 전송은 줄바꿈으로 구분한 메시지를 하위 프로세스의 표준 입력과 출력에서 교환합니다. Streamable HTTP 전송은 하나의 MCP 엔드포인트에 HTTP POST와 선택적인 GET을 사용합니다. 전송 선택은 도구의 업무 의미를 바꾸지 않지만 연결 수명, 자격 정보 위치, 접근 가능한 사용자의 범위를 바꿉니다. 인증은 요청 주체를 확인하는 과정이고 인가는 확인된 주체가 특정 도구를 호출할 수 있는지 판정하는 과정입니다. 최소 권한은 서버 프로세스와 사용자에게 필요한 자원과 동작만 허용하는 원칙입니다.",
"observe": "Before 구성은 부모 프로세스의 전체 환경을 복사하므로 OPENAI_API_KEY 같은 업무와 무관한 비밀 이름까지 하위 프로세스에 포함될 수 있습니다. 값은 출력하지 않고 포함 여부만 확인합니다. After 구성은 서버 실행에 필요한 PATH와 PYTHONUNBUFFERED만 MCP 서버 설정의 env에 전달합니다. 이어서 LangChain MCPAdapter가 이 설정으로 course_server.py를 시작하고 실제 stdio 도구를 호출합니다. 원격 예시는 실행하지 않는 설정 표로만 제시합니다. 공개 서버 배포나 외부 상태 변경은 이 실습 범위가 아닙니다.",
"notes": ["stdio라는 이름만으로 서버가 안전해지는 것은 아닙니다. 실행 파일 경로를 고정하고 설치 출처를 확인하며 전달 환경을 제한합니다.", "Streamable HTTP 서버는 127.0.0.1 실험과 공개 네트워크 배포를 구분합니다. 이 챕터는 외부에 포트를 공개하지 않습니다.", "원격 토큰은 코드나 노트북 출력에 적지 않습니다. .env에서 읽고 헤더를 구성하더라도 존재 여부만 확인합니다.", "인증은 사용자 신원을 확인하고 인가는 도구·리소스별 허용 범위를 정합니다. 읽기 권한이 있는 사용자가 관리 도구까지 호출할 수 있어서는 안 됩니다."],
"next": "다음 절에서는 stdio 서버의 도구를 LangChain BaseTool로 변환하고 기존 bind_tools 흐름에 연결합니다.",
"quiz": [("stdio 서버를 누가 시작하나요?", "일반적으로 MCP 클라이언트가 로컬 하위 프로세스로 시작하고 종료합니다."), ("부모 환경 전체를 하위 프로세스에 전달할 때의 문제는 무엇인가요?", "서버에 필요하지 않은 비밀 값과 설정까지 접근 가능해질 수 있습니다."), ("인증과 인가는 어떻게 다른가요?", "인증은 사용자가 누구인지 확인하고, 인가는 확인된 사용자가 어떤 기능을 사용할 수 있는지 결정합니다."), ("이 실습에서 원격 서버를 공개하지 않는 이유는 무엇인가요?", "TLS·OAuth·호스팅 운영까지 검증하지 않은 상태에서 외부 접근 경계를 만들지 않기 위해서입니다.")],
"cells": [("패키지 버전 확인", INSTALL), ("Before: 전체 환경 전달 확인", '''import os

unsafe_env = dict(os.environ)
print("전체 환경 변수 개수:", len(unsafe_env))
print("OPENAI_API_KEY 이름 포함:", "OPENAI_API_KEY" in unsafe_env)
assert len(unsafe_env) > 2''', "before"), ("After: 서버에 필요한 환경만 선택", '''safe_env = {
    "PATH": os.environ.get("PATH", ""),
    "PYTHONUNBUFFERED": "1",
}
print("전달할 이름:", sorted(safe_env))
print("OPENAI_API_KEY 이름 포함:", "OPENAI_API_KEY" in safe_env)
assert "OPENAI_API_KEY" not in safe_env''', "after"), ("제한한 환경으로 실제 stdio 서버 호출", '''import asyncio
import sys
from pathlib import Path
from langchain.mcp import MCPAdapter

server_path = Path.cwd() / "labs/part6/ch28-mcp/course_server.py"
server_config = {"mcpServers": {"course": {
    "command": sys.executable,
    "args": [str(server_path)],
    "env": safe_env,
}}}

async def call_over_stdio() -> tuple[list[str], object]:
    async with MCPAdapter(server_config) as adapter:
        tools = await adapter.list_tools()
        result = await tools[0].ainvoke({"topic": "운영"})
        return [tool.name for tool in tools], result

tool_names, result = await call_over_stdio()
print("transport: stdio")
print("tools:", tool_names)
print("result:", result)
assert tool_names == ["lookup_policy"]
assert "20:00" in str(result)''', "after"), ("전송별 신뢰 경계 비교", '''boundaries = [
    ("stdio", "클라이언트가 로컬 프로세스 시작", "선택한 환경 변수", "운영체제 사용자 권한"),
    ("Streamable HTTP", "원격 서비스가 별도 실행", "TLS와 Authorization", "사용자·도구별 인가"),
]
for row in boundaries:
    print(" | ".join(row))
assert boundaries[0][0] != boundaries[1][0]''', "after")]
},
"04-LangChain-MCP-클라이언트-연동": {
"title": "LangChain MCP 클라이언트 연동", "format": "experiment", "hours": "강의 1h · 실습 2h", "terms": "5",
"question": "MCP 서버의 도구를 LangChain 도구로 변환해 기존 모델 호출 코드에서 사용하려면 어떤 어댑터가 필요할까요?",
"goals": ["langchain.mcp의 MCPAdapter를 올바른 대상 형식으로 열 수 있습니다.", "MCP 도구를 LangChain BaseTool로 발견하고 직접 호출할 수 있습니다.", "직접 작성한 LangChain 도구와 MCP 어댑터 도구의 경계를 설명할 수 있습니다."],
"why": "서버 호출이 성공해도 기존 LangChain 에이전트가 그 도구를 바로 읽는 것은 아닙니다. 어댑터(adapter)는 MCP의 도구 설명과 호출 방식을 LangChain BaseTool 인터페이스로 바꿉니다. 이 변환을 확인하면 Ch19의 bind_tools 코드와 MCP 서버를 같은 모델 인터페이스에서 다룰 수 있습니다.",
"prior": "Ch19에서 @tool로 만든 BaseTool의 name, description, args_schema를 모델에 연결했습니다. 앞 절에서는 course_server.py를 stdio로 호출했습니다. 이번에는 같은 서버를 MCPAdapter에 넘기고 반환된 도구의 이름·설명·입력 스키마·호출 결과를 읽습니다.",
"concept": "서로 다른 규격의 플러그를 연결하는 변환기를 생각해 봅니다. MCPAdapter는 FastMCP 클라이언트 연결과 프로토콜 협상을 담당하고, list_tools 결과를 LangChain BaseTool 목록으로 바꿉니다. LangChain 1.4.0에서는 from langchain.mcp import MCPAdapter가 공식 문서의 현재 경로이며 beta 경고가 발생합니다. 과거 외부 패키지인 langchain-mcp-adapters의 MultiServerMCPClient 예제가 많이 남아 있지만, 1.4.0 공식 문서는 새 네임스페이스로의 이동을 안내합니다. 커리큘럼의 langchain.mcp 표기는 확인 결과 유효합니다. 다만 모듈 이름만 적는 것으로 충분하지 않고 MCPAdapter 클래스를 사용해야 합니다.",
"definition": "어댑터는 한 인터페이스의 값을 다른 인터페이스에서 사용할 수 있도록 변환하는 객체입니다. MCPAdapter는 URL, Path, FastMCP 인스턴스 같은 대상을 받고 연결 방법을 정합니다. Path 대상은 stdio 하위 프로세스, http 또는 https URL은 Streamable HTTP, FastMCP 인스턴스는 메모리 연결을 사용합니다. list_tools는 MCP 도구의 이름·설명·입력 스키마와 원격 호출 함수를 LangChain BaseTool로 감쌉니다. 반환 도구는 invoke나 ainvoke로 호출할 수 있고 bind_tools에도 전달할 수 있습니다. 연결 수명과 도구 캐시 정책은 어댑터가 관리하지만 업무 권한 판정은 서버나 호출 전 인터셉터에서 별도로 구현해야 합니다.",
"observe": "실험은 Path 객체로 서버 파일을 지정합니다. MCPAdapter는 이 파일을 stdio 하위 프로세스로 시작하고 list_tools에서 lookup_policy 하나를 반환합니다. 도구의 args_schema는 topic 문자열을 요구하며 ainvoke에 운영을 전달하면 운영 시간이 반환됩니다. 직접 작성한 LangChain @tool과 비교하면 호출 측 인터페이스는 name과 invoke로 비슷하지만, MCP 도구 실행은 프로토콜을 거쳐 별도 서버로 전달됩니다. 어댑터가 변환한다고 해서 서버 코드를 클라이언트 프로세스 안에서 직접 호출하는 것은 아닙니다.",
"notes": ["langchain.mcp는 1.4.0에서 beta입니다. 경고를 숨기기보다 기준 버전과 변경 가능성을 참고 자료에 기록합니다.", "MCPAdapter의 문자열 대상은 http 또는 https URL이어야 합니다. 로컬 스크립트는 Path 객체로 넘겨 의도를 분명히 합니다.", "도구 목록은 연결 시점에 발견한 결과입니다. 서버 구성 요소가 바뀌면 캐시 정책과 재발견 시점을 정해야 합니다.", "모델이 도구를 자동 선택하게 하는 호출은 다음 절에서 수행합니다. 이 절은 어댑터 변환과 실제 도구 호출만 분리해 확인합니다."],
"next": "마지막 절에서는 직접 도구 한 개, MCP 도구 한 개, MCP 도구 다섯 개를 같은 첫 질문에 연결해 모델 입력 토큰을 측정합니다.",
"quiz": [("LangChain 1.4.0의 공식 MCP import 경로는 무엇인가요?", "from langchain.mcp import MCPAdapter입니다."), ("로컬 서버 파일을 MCPAdapter에 넘길 때 권장 형식은 무엇인가요?", "문자열 대신 pathlib.Path 객체로 넘깁니다."), ("어댑터가 반환한 도구는 어떤 공통 인터페이스를 따르나요?", "LangChain BaseTool 인터페이스를 따라 name, description, args_schema와 invoke 계열 메서드를 제공합니다."), ("직접 도구와 MCP 도구의 호출 측 모양이 비슷해도 실행 경계가 다른 이유는 무엇인가요?", "MCP 도구는 어댑터와 전송 계층을 거쳐 별도 서버에서 실행되기 때문입니다.")],
"cells": [("패키지 버전 확인", INSTALL), ("MCPAdapter로 stdio 도구 발견", '''import asyncio
from pathlib import Path
from langchain.mcp import MCPAdapter

server_path = Path.cwd() / "labs/part6/ch28-mcp/course_server.py"

async def load_and_call() -> tuple[list, dict, object]:
    async with MCPAdapter(server_path) as adapter:
        tools = await adapter.list_tools()
        raw_schema = tools[0].args_schema
        schema = raw_schema if isinstance(raw_schema, dict) else raw_schema.model_json_schema()
        result = await tools[0].ainvoke({"topic": "운영"})
        return tools, schema, result

tools, schema, result = await load_and_call()
print("tool:", tools[0].name)
print("required:", schema.get("required"))
print("result:", result)
assert tools[0].name == "lookup_policy"
assert schema.get("required") == ["topic"]
assert "20:00" in str(result)'''), ("직접 LangChain 도구와 인터페이스 비교", '''from langchain.tools import tool

@tool
def direct_lookup_policy(topic: str) -> str:
    """자료실 규정을 직접 조회합니다."""
    return {"운영": "평일 09:00~20:00"}[topic]

comparison = {
    "direct": (direct_lookup_policy.name, bool(direct_lookup_policy.args_schema)),
    "mcp": (tools[0].name, bool(tools[0].args_schema)),
}
print(comparison)
print("direct result:", direct_lookup_policy.invoke({"topic": "운영"}))
print("mcp result:", result)
assert all(has_schema for _, has_schema in comparison.values())''')]
},
"05-도구-정의와-첫-호출-토큰": {
"title": "도구 정의와 첫 호출 토큰", "format": "experiment", "hours": "강의 1h · 실습 2h", "terms": "6",
"question": "MCP 서버에서 발견한 도구 정의의 수가 늘면 같은 첫 모델 호출의 입력 토큰은 얼마나 달라질까요?",
"goals": ["직접 도구와 MCP 도구를 같은 질문과 모델 조건에서 비교할 수 있습니다.", "도구 정의 개수·직렬화 크기·모델 입력 토큰을 서로 다른 측정값으로 기록할 수 있습니다.", "첫 호출 usage_metadata로 비용을 계산하고 결과의 적용 범위를 설명할 수 있습니다."],
"why": "MCP는 기능을 연결하는 비용을 없애지 않습니다. 모델이 어떤 도구를 고를지 판단하려면 이름·설명·입력 스키마를 첫 호출에 받아야 합니다. Ch19에서 도구 개수가 늘면 선택 정보가 커진다는 사실을 배웠습니다. 이제 직접 도구와 MCP 어댑터 도구를 같은 모델에 연결해 프로토콜 도입 자체와 도구 정의 수 증가를 분리합니다.",
"prior": "Ch19에서 bind_tools가 도구 설명을 모델 요청에 포함시키고 usage_metadata가 입력·출력 토큰을 제공한다는 사실을 확인했습니다. 앞 절에서 MCPAdapter가 MCP 도구를 BaseTool로 변환했습니다. 이번 실험은 도구 실행 뒤의 두 번째 호출이 아니라, 도구를 고르는 첫 모델 호출만 측정합니다.",
"concept": "메뉴판의 음식 수와 종이 무게는 관련이 있지만 같은 값은 아닙니다. 도구 정의 수는 항목 개수입니다. JSON Schema 직렬화 문자의 수는 클라이언트가 가진 정의의 대략적인 크기입니다. input_tokens는 모델 제공자가 실제 요청을 토큰화하고 보고한 값입니다. MCP JSON-RPC 전송 바이트는 클라이언트와 서버 사이 통신량이며 usage_metadata에 포함되지 않습니다. 따라서 MCP 연결 전후 토큰을 말할 때는 모델에 전달한 도구 정의가 무엇인지 함께 기록해야 합니다. 직접 도구 한 개와 MCP 도구 한 개 비교는 어댑터 변환 차이를, MCP 도구 한 개와 다섯 개 비교는 목록 규모 차이를 보여 줍니다.",
"definition": "첫 호출 입력 토큰은 사용자 메시지와 시스템 지침, 모델에 전달된 도구 정의 등 첫 모델 요청에 포함된 입력을 제공자가 토큰화한 수치입니다. 이번 실험에서는 대화 이력과 도구 결과가 아직 없으므로 도구 정의 규모의 차이를 읽기 좋습니다. schema_chars는 동일한 Python JSON 직렬화 방식으로 이름·설명·스키마를 문자열로 바꾼 문자 수입니다. 이 값은 토큰 수의 대체물이 아니며 설명 길이를 대조하는 보조 측정입니다. 직접 도구와 MCP 도구가 같은 158 입력 토큰을 기록하면 MCP라는 이유만으로 모델 입력이 늘었다고 말할 수 없습니다. MCP 도구 다섯 개가 316 토큰을 기록한 결과는 이 실행에서 정의 수와 내용이 늘어 입력이 커졌다는 증거입니다.",
"observe": "세 조건은 같은 gpt-5.4-mini 모델, 같은 질문, tool_choice='required', reasoning_effort='none'을 사용합니다. A는 직접 @tool 한 개, B는 같은 역할의 MCP 도구 한 개, C는 읽기 전용 MCP 도구 다섯 개입니다. 각 호출에서 input_tokens, output_tokens와 첫 AIMessage의 tool_calls를 출력합니다. 실행된 수치는 노트북 출력과 verification.md에 기록합니다. 한 번의 작은 질문이므로 토큰 증가 방향을 관찰할 수 있지만 모든 모델과 제공자의 직렬화 방식에 일반화할 수는 없습니다.",
"notes": ["MCP 연결 초기화·목록 조회의 JSON-RPC 바이트를 모델 입력 토큰으로 부르지 않습니다. 이 실습은 OpenAI가 보고한 모델 호출 usage_metadata를 측정합니다.", "직접 도구 한 개와 MCP 도구 한 개는 이름과 변환된 스키마 표현이 완전히 같지 않으므로 결과 차이를 MCP 하나의 원인으로 단정하지 않습니다. MCP 한 개와 다섯 개 조건도 도구 수와 각 정의 내용이 함께 바뀝니다.", "도구가 많다고 항상 선형으로 같은 토큰 수가 늘지는 않습니다. 이름·설명·스키마 길이와 제공자 직렬화가 함께 영향을 줍니다.", "비용은 2026-09-11에 이 교재가 사용하는 기존 gpt-5.4-mini 단가 가정으로 추정하며 모든 조건 합계가 1달러 미만인지 확인합니다. 실제 청구는 계정 조건에 따라 달라질 수 있습니다.", "권한이 없는 도구는 모델에게 보이지 않게 서버나 클라이언트에서 필터링하면 보안 범위와 도구 정의 입력을 함께 줄일 수 있습니다. 단, 토큰 절감을 권한 검사의 대체 수단으로 사용해서는 안 됩니다."],
"next": "Ch29에서는 최종 답만 보지 않고 도구 선택과 호출 순서를 포함한 실행 궤적을 평가합니다. Ch37에서는 MCP 도구 정의가 계기판의 컨텍스트 지표를 어떻게 악화시키는지 다시 측정합니다.",
"quiz": [("usage_metadata의 input_tokens가 포함하지 않는 것은 무엇인가요?", "MCP 클라이언트와 서버 사이에서 오간 JSON-RPC 전송 바이트입니다."), ("직접 도구 한 개와 MCP 도구 한 개를 비교하는 이유는 무엇인가요?", "도구 수 증가와 어댑터 변환의 영향을 분리해서 보기 위해서입니다."), ("MCP 도구 한 개와 다섯 개 조건에서 고정한 값은 무엇인가요?", "모델, 질문, 첫 호출, tool_choice와 추론 설정을 고정합니다."), ("권한별 도구 필터링의 두 효과는 무엇인가요?", "사용자가 호출할 수 있는 범위를 제한하고 모델에 전달할 불필요한 도구 정의를 줄입니다."), ("한 번의 측정으로 모든 MCP 서버의 비용을 단정할 수 없는 이유는 무엇인가요?", "도구 설명 길이, 스키마, 모델, 제공자 직렬화와 실행 시점이 다르기 때문입니다.")],
"cells": [("패키지와 API 키 확인", INSTALL + '''
import os
from pathlib import Path
from dotenv import load_dotenv

for folder in [Path.cwd(), *Path.cwd().parents]:
    if (folder / ".env").is_file():
        load_dotenv(folder / ".env")
        break
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY가 필요합니다."
print("API 키 존재 여부 확인 완료")'''), ("직접 도구와 소형 MCP 서버 준비", '''import asyncio
from fastmcp import FastMCP
from langchain.mcp import MCPAdapter
from langchain.tools import tool

@tool
def direct_lookup(topic: str) -> str:
    """자료실 규정을 조회합니다. topic은 대출, 운영, 연체 중 하나입니다."""
    return topic

small = FastMCP("small")
@small.tool
def lookup_policy(topic: str) -> str:
    """자료실 규정을 조회합니다. topic은 대출, 운영, 연체 중 하나입니다."""
    return topic

async def load_mcp_tools(server: object) -> list:
    async with MCPAdapter(server) as adapter:
        return await adapter.list_tools()

small_tools = await load_mcp_tools(small)
print("small count:", len(small_tools))
assert len(small_tools) == 1'''), ("대형 MCP 서버와 다섯 도구 준비", '''large = FastMCP("large")
for name, description in [
    ("lookup_policy", "자료실 규정을 조회합니다."),
    ("search_catalog", "도서 제목을 검색합니다."),
    ("check_hours", "운영 시간을 확인합니다."),
    ("list_events", "공개 행사를 조회합니다."),
    ("find_room", "자료실 위치를 조회합니다."),
]:
    async def read_only(query: str, _name: str = name) -> str:
        return f"{_name}: {query}"
    read_only.__name__ = name
    read_only.__doc__ = description + " query는 검색어입니다."
    large.tool(read_only, name=name)

large_tools = await load_mcp_tools(large)
print("counts:", 1, len(small_tools), len(large_tools))
assert len(small_tools) == 1 and len(large_tools) == 5'''), ("도구 정의 직렬화 크기 비교", '''import json

def schema_chars(tools: list) -> int:
    payload = [{
        "name": item.name,
        "description": item.description,
        "schema": item.args_schema if isinstance(item.args_schema, dict) else item.args_schema.model_json_schema(),
    } for item in tools]
    return len(json.dumps(payload, ensure_ascii=False, sort_keys=True))

schema_sizes = {
    "direct_1": schema_chars([direct_lookup]),
    "mcp_1": schema_chars(small_tools),
    "mcp_5": schema_chars(large_tools),
}
print("schema_chars:", schema_sizes)
assert schema_sizes["mcp_5"] > schema_sizes["mcp_1"]'''), ("같은 첫 모델 호출의 토큰 실측", '''from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-5.4-mini", reasoning_effort="none")
question = "자료실의 대출 규정을 확인하려면 어떤 도구를 써야 하나요?"

def first_call(tools: list) -> dict:
    reply = model.bind_tools(tools, tool_choice="required").invoke(question)
    usage = reply.usage_metadata
    assert usage is not None and reply.tool_calls
    return {
        "input_tokens": usage["input_tokens"],
        "output_tokens": usage["output_tokens"],
        "selected": reply.tool_calls[0]["name"],
    }

measurements = {
    "direct_1": first_call([direct_lookup]),
    "mcp_1": first_call(small_tools),
    "mcp_5": first_call(large_tools),
}
for condition, result in measurements.items():
    print(condition, result)
assert measurements["mcp_5"]["input_tokens"] > measurements["mcp_1"]["input_tokens"]'''), ("비용 계산과 해석 범위", '''INPUT_USD_PER_MTOK = 0.75
OUTPUT_USD_PER_MTOK = 4.50

for result in measurements.values():
    result["estimated_cost_usd"] = round(
        result["input_tokens"] / 1_000_000 * INPUT_USD_PER_MTOK
        + result["output_tokens"] / 1_000_000 * OUTPUT_USD_PER_MTOK,
        8,
    )
total_cost = sum(item["estimated_cost_usd"] for item in measurements.values())
print("measurements:", measurements)
print("total_estimated_cost_usd:", round(total_cost, 8))
print("MCP 전송 바이트는 이 토큰 수에 포함되지 않습니다.")
assert total_cost < 1.0''')]
}}


ENRICHMENTS = {
    "01-MCP-구조와-capability-협상": (
        "초기화 협상은 연결 직후 한 번의 요청과 응답으로 시작합니다. 클라이언트는 지원하는 프로토콜 버전과 기능을 보내고, 서버는 선택한 버전과 자신이 제공하는 capability를 반환합니다. 이어서 클라이언트가 `initialized` 알림을 보내면 도구 목록 같은 정상 요청을 시작합니다. capability는 ‘이 종류의 요청을 이해한다’는 선언이며, 특정 사용자가 그 도구를 호출해도 된다는 권한 판정은 아닙니다.",
        "도구·리소스·프롬프트는 모델에 전달되는 방식도 다릅니다. 도구는 모델이 실행을 요청할 수 있는 이름·설명·입력 스키마를 가집니다. 리소스는 URI로 읽는 데이터이고, 프롬프트는 사용자가 선택하거나 클라이언트가 가져오는 메시지 틀입니다. 같은 도서관 서버라도 ‘대출 가능 여부 계산’은 도구, ‘운영 규정 원문’은 리소스, ‘문의 답변 작성 틀’은 프롬프트가 됩니다. 기능을 어느 범주로 공개할지는 변경 가능성, 실행 부작용, 선택 주체를 기준으로 정합니다.",
    ),
    "02-FastMCP-로컬-서버-제작": (
        "`FastMCP('course')`는 등록 정보를 보관하는 서버 객체를 만듭니다. 일반 함수는 Python 코드 안에 존재할 뿐 클라이언트가 발견할 수 없습니다. `@mcp.tool`을 붙이면 함수 이름, docstring, 타입 힌트가 각각 도구 이름, 설명, JSON Schema로 변환되어 `list_tools()` 결과에 나타납니다. 데코레이터가 붙는 시점은 서버 실행 시점이 아니라 모듈을 읽어 함수 정의를 실행하는 시점입니다.",
        "도구 설명은 사람용 주석만이 아니라 모델의 선택 입력입니다. ‘조회합니다’처럼 범위가 넓은 설명보다 어떤 자료를 어떤 인자로 조회하고 무엇을 반환하는지 적어야 합니다. 리소스는 읽을 URI, 프롬프트는 재사용 메시지라는 다른 발견 경로를 가지므로 실행 가능한 계산을 리소스로 위장하지 않습니다. Before에서 함수가 목록에 없고 After에서 등록된 도구가 나타나는 차이는 Python 함수의 존재와 MCP 공개 표면이 별개임을 보여 줍니다.",
    ),
    "03-stdio와-원격-전송-권한-경계": (
        "stdio 연결에서는 클라이언트가 서버 명령을 하위 프로세스로 시작하고 표준 입력·출력으로 JSON-RPC 메시지를 교환합니다. `env`에 넘긴 사전은 그 프로세스가 볼 수 있는 환경 변수를 정합니다. 부모 프로세스의 전체 환경을 복사하면 API 키처럼 서버에 필요하지 않은 값도 함께 전달될 수 있습니다. 필요한 변수만 새 사전에 넣는 After 코드는 서버 기능은 유지하면서 노출 범위를 줄입니다.",
        "Streamable HTTP에서는 서버가 별도 주소에서 실행되므로 프로세스 환경 대신 네트워크 요청의 인증 정보와 서버 측 인가가 중요합니다. TLS는 전송 중 내용을 보호하고 인증은 요청 주체를 확인하지만, 어떤 사용자가 어떤 도구를 실행할 수 있는지는 인가 규칙이 정합니다. stdio가 로컬이라는 이유로 안전하다고 단정할 수도 없습니다. 하위 프로세스는 전달받은 운영체제 권한으로 파일과 네트워크에 접근할 수 있으므로 실행 파일, 환경, 작업 폴더를 함께 제한해야 합니다.",
    ),
    "04-LangChain-MCP-클라이언트-연동": (
        "`async with MCPAdapter(server_path) as adapter`는 연결을 열고 블록을 벗어날 때 정리합니다. `await adapter.list_tools()`는 서버의 MCP 도구 정의를 가져와 LangChain `BaseTool` 객체 목록으로 변환합니다. 변환된 도구의 `.name`과 `.args_schema`는 모델 선택에 쓰이고, `.ainvoke({...})`를 호출하면 어댑터가 인자를 MCP 요청으로 보내 서버 결과를 다시 LangChain 결과 형식으로 반환합니다. `await`는 원격 또는 하위 프로세스 응답을 기다리는 동안 다른 비동기 작업이 실행될 수 있게 합니다.",
        "직접 `@tool`로 만든 도구와 MCP 도구는 에이전트에서 비슷한 인터페이스를 가지지만 소유 경계가 다릅니다. 직접 도구는 같은 애플리케이션 코드와 배포 주기를 따르고, MCP 도구는 별도 서버가 목록·스키마·실행을 제공합니다. 어댑터가 형식을 맞춰도 서버 권한, 연결 실패, 버전 협상, 결과 신뢰성까지 해결하지는 않습니다. 예제의 두 도구가 같은 운영 시간을 반환한다는 사실은 인터페이스 호환을 보여 주며 두 구현의 장애 특성이 같다는 뜻은 아닙니다.",
    ),
    "05-도구-정의와-첫-호출-토큰": (
        "`bind_tools(tools, tool_choice='required')`는 선택 가능한 도구 정의를 첫 모델 요청에 포함하고 모델이 반드시 하나의 도구 호출을 만들도록 합니다. 이때 도구가 실행되는 것은 아닙니다. 반환한 첫 `AIMessage`의 `tool_calls`에는 선택한 이름과 인자가 있고, `usage_metadata['input_tokens']`에는 공급자가 보고한 전체 입력 토큰이 있습니다. `schema_chars`는 도구 이름·설명·스키마를 같은 JSON 방식으로 직렬화한 문자 수라서 정의 규모를 읽는 보조값입니다.",
        "도구 수와 입력 토큰의 관계를 분리해서 읽어야 합니다. 직접 도구 한 개와 MCP 도구 한 개는 연결 방식이 다르지만 모델에 보이는 변환 결과가 비슷할 수 있습니다. MCP 한 개와 다섯 개 비교에서는 개수뿐 아니라 각 이름과 설명의 내용도 함께 바뀝니다. 따라서 이번 결과는 ‘이 정의 묶음에서 다섯 개 조건의 입력이 더 컸다’는 관찰입니다. 자주 쓰지 않는 도구를 상황에 따라 필터링하면 선택 오류와 입력 규모를 함께 줄일 수 있지만, 권한이 없는 도구를 숨기는 일은 서버의 인가 검사를 대신하지 않습니다.",
    ),
}


def enrichment_html(slug: str) -> str:
    rendered = []
    for paragraph in ENRICHMENTS[slug]:
        value = html.escape(paragraph)
        value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
        rendered.append(f"<p>{value}</p>")
    return "".join(rendered)


REVIEWED_STEP_MARKDOWN = {'01-MCP-구조와-capability-협상': ['## 패키지 버전 확인\n\n설치된 FastMCP와 LangChain 버전을 출력해 아래 API가 어떤 기준에서 실행됐는지 고정합니다.',
                              '## 학생용 서버 불러오기\n'
                              '\n'
                              '`course_server.py`의 FastMCP 인스턴스를 메모리 안에 불러옵니다. 이 단계는 아직 목록 조회나 도구 호출을 수행하지 않습니다.\n'
                              '\n'
                              '### 코드 읽기와 비교 경계\n'
                              '\n'
                              '초기화 협상은 연결 직후 한 번의 요청과 응답으로 시작합니다. 클라이언트는 지원하는 프로토콜 버전과 기능을 보내고, 서버는 선택한 버전과 자신이 제공하는 capability를 반환합니다. 이어서 클라이언트가 '
                              '`initialized` 알림을 보내면 도구 목록 같은 정상 요청을 시작합니다. capability는 ‘이 종류의 요청을 이해한다’는 선언이며, 특정 사용자가 그 도구를 호출해도 된다는 권한 판정은 아닙니다.\n'
                              '\n'
                              '도구·리소스·프롬프트는 모델에 전달되는 방식도 다릅니다. 도구는 모델이 실행을 요청할 수 있는 이름·설명·입력 스키마를 가집니다. 리소스는 URI로 읽는 데이터이고, 프롬프트는 사용자가 선택하거나 클라이언트가 가져오는 메시지 '
                              '틀입니다. 같은 도서관 서버라도 ‘대출 가능 여부 계산’은 도구, ‘운영 규정 원문’은 리소스, ‘문의 답변 작성 틀’은 프롬프트가 됩니다. 기능을 어느 범주로 공개할지는 변경 가능성, 실행 부작용, 선택 주체를 기준으로 '
                              '정합니다.\n',
                              '## 세 capability 발견\n'
                              '\n'
                              '한 클라이언트 연결에서 도구, 리소스, 프롬프트 목록을 각각 조회하고 반환된 이름을 비교합니다.\n'
                              '\n'
                              '`async def`는 코루틴 함수를 정의하며, 함수를 호출한 것만으로는 본문이 실행되지 않습니다. `await discover()`가 코루틴을 실행하고 결과를 기다립니다. `async with Client(mcp)`는 연결을 '
                              '열고 블록을 벗어날 때 연결을 정리합니다.\n',
                              '## 도구·리소스·프롬프트 실제 사용\n'
                              '\n'
                              '`call_tool`, `read_resource`, `get_prompt`에 각각 필요한 이름과 인자를 넘기고 서로 다른 반환 구조를 확인합니다.\n'
                              '\n'
                              '목록 조회는 정의를 반환하고, `call_tool`·`read_resource`·`get_prompt`는 각 구성 요소를 실제로 사용합니다. 이 셀에서 실행 결과, URI 본문, 메시지 틀을 서로 다른 반환값으로 읽습니다.\n'],
 '02-FastMCP-로컬-서버-제작': ['## 패키지 버전 확인\n\n설치된 FastMCP와 LangChain 버전을 출력해 아래 API가 어떤 기준에서 실행됐는지 고정합니다.',
                         '## Before: 등록하지 않은 함수\n'
                         '\n'
                         '일반 Python 함수만 정의한 뒤 `list_tools()`가 빈 목록을 반환하고 호출이 거부되는지 확인합니다.\n'
                         '\n'
                         '### 코드 읽기와 비교 경계\n'
                         '\n'
                         "`FastMCP('course')`는 등록 정보를 보관하는 서버 객체를 만듭니다. 일반 함수는 Python 코드 안에 존재할 뿐 클라이언트가 발견할 수 없습니다. `@mcp.tool`을 붙이면 함수 이름, docstring, 타입 힌트가 "
                         '각각 도구 이름, 설명, JSON Schema로 변환되어 `list_tools()` 결과에 나타납니다. 데코레이터가 붙는 시점은 서버 실행 시점이 아니라 모듈을 읽어 함수 정의를 실행하는 시점입니다.\n'
                         '\n'
                         '도구 설명은 사람용 주석만이 아니라 모델의 선택 입력입니다. ‘조회합니다’처럼 범위가 넓은 설명보다 어떤 자료를 어떤 인자로 조회하고 무엇을 반환하는지 적어야 합니다. 리소스는 읽을 URI, 프롬프트는 재사용 메시지라는 다른 발견 경로를 '
                         '가지므로 실행 가능한 계산을 리소스로 위장하지 않습니다. Before에서 함수가 목록에 없고 After에서 등록된 도구가 나타나는 차이는 Python 함수의 존재와 MCP 공개 표면이 별개임을 보여 줍니다.\n',
                         '## After: 도구 등록\n'
                         '\n'
                         '같은 함수에 `@mcp.tool`을 적용해 목록에 등록하고, `topic` 인자를 넘겨 규정 문자열을 반환받습니다.\n'
                         '\n'
                         '앞 절의 비동기 호출을 다시 사용합니다. `async def` 본문은 `await`할 때 실행되고, `async with Client(...)`는 등록 목록을 읽는 동안만 연결을 유지합니다.\n',
                         '## 완성 서버의 세 구성 요소 확인\n'
                         '\n'
                         '완성한 서버의 도구·리소스·프롬프트 목록을 읽어 각 구성 요소가 하나씩 발견되는지 확인합니다. 이 셀은 입력 스키마를 출력하지 않습니다.\n'
                         '\n'
                         '완성 서버의 목록은 도구·리소스·프롬프트가 각각 하나씩 등록됐는지 확인합니다. 서버 파일이 존재하는 것과 클라이언트가 구성 요소를 발견하는 것을 따로 검사합니다.\n'],
 '03-stdio와-원격-전송-권한-경계': ['## 패키지 버전 확인\n\n설치된 FastMCP와 LangChain 버전을 출력해 아래 API가 어떤 기준에서 실행됐는지 고정합니다.',
                           '## Before: 전체 환경 전달 확인\n'
                           '\n'
                           '`os.environ`을 복사하면 서버가 업무와 무관한 환경 변수 이름까지 받게 됨을 키 목록으로 확인합니다.\n'
                           '\n'
                           '### 코드 읽기와 비교 경계\n'
                           '\n'
                           'stdio 연결에서는 클라이언트가 서버 명령을 하위 프로세스로 시작하고 표준 입력·출력으로 JSON-RPC 메시지를 교환합니다. `env`에 넘긴 사전은 그 프로세스가 볼 수 있는 환경 변수를 정합니다. 부모 프로세스의 전체 환경을 '
                           '복사하면 API 키처럼 서버에 필요하지 않은 값도 함께 전달될 수 있습니다. 필요한 변수만 새 사전에 넣는 After 코드는 서버 기능은 유지하면서 노출 범위를 줄입니다.\n'
                           '\n'
                           'Streamable HTTP에서는 서버가 별도 주소에서 실행되므로 프로세스 환경 대신 네트워크 요청의 인증 정보와 서버 측 인가가 중요합니다. TLS는 전송 중 내용을 보호하고 인증은 요청 주체를 확인하지만, 어떤 사용자가 어떤 '
                           '도구를 실행할 수 있는지는 인가 규칙이 정합니다. stdio가 로컬이라는 이유로 안전하다고 단정할 수도 없습니다. 하위 프로세스는 전달받은 운영체제 권한으로 파일과 네트워크에 접근할 수 있으므로 실행 파일, 환경, 작업 폴더를 함께 '
                           '제한해야 합니다.\n',
                           '## After: 서버에 필요한 환경만 선택\n'
                           '\n'
                           '서버에 필요한 키만 담은 새 `env`를 만들고, 전체 복사 결과와 키 범위를 비교합니다.\n'
                           '\n'
                           '수정 후에는 전체 `os.environ`을 복사하지 않고 서버 실행에 필요한 키만 새 사전에 넣습니다. 출력은 전달된 키 이름을 비교하며 비밀 값은 보여 주지 않습니다.\n',
                           '## 제한한 환경으로 실제 stdio 서버 호출\n'
                           '\n'
                           '하위 프로세스에 제한한 `env`를 넘기고 MCP 도구를 호출해 규정 반환값을 검증합니다.\n'
                           '\n'
                           '`server_config = {"mcpServers": ...}` 사전의 `command`, `args`, `env`는 `MCPAdapter(server_config)`가 stdio 하위 프로세스를 시작할 때 사용하는 입력입니다. 도구 반환값이 예상 규정과 같은지까지 확인해야 전송 설정과 서버 실행을 함께 검증할 수 있습니다.\n',
                           '## 전송별 신뢰 경계 비교\n\nstdio와 Streamable HTTP의 실행 주체, 비밀 전달, 인증, 인가 책임을 표의 각 열로 비교합니다.'],
 '04-LangChain-MCP-클라이언트-연동': ['## 패키지 버전 확인\n\n설치된 FastMCP와 LangChain 버전을 출력해 아래 API가 어떤 기준에서 실행됐는지 고정합니다.',
                               '## MCPAdapter로 stdio 도구 발견\n'
                               '\n'
                               '`MCPAdapter`가 stdio 연결을 열고 `lookup_policy`를 LangChain `BaseTool`로 변환하는 과정과 스키마를 확인합니다.\n'
                               '\n'
                               '### 코드 읽기와 비교 경계\n'
                               '\n'
                               '`async with MCPAdapter(server_path) as adapter`는 연결을 열고 블록을 벗어날 때 정리합니다. `await adapter.list_tools()`는 서버의 MCP 도구 정의를 가져와 '
                               'LangChain `BaseTool` 객체 목록으로 변환합니다. 변환된 도구의 `.name`과 `.args_schema`는 모델 선택에 쓰이고, `.ainvoke({...})`를 호출하면 어댑터가 인자를 MCP 요청으로 보내 '
                               '서버 결과를 다시 LangChain 결과 형식으로 반환합니다. `await`는 원격 또는 하위 프로세스 응답을 기다리는 동안 다른 비동기 작업이 실행될 수 있게 합니다.\n'
                               '\n'
                               '직접 `@tool`로 만든 도구와 MCP 도구는 에이전트에서 비슷한 인터페이스를 가지지만 소유 경계가 다릅니다. 직접 도구는 같은 애플리케이션 코드와 배포 주기를 따르고, MCP 도구는 별도 서버가 목록·스키마·실행을 '
                               '제공합니다. 어댑터가 형식을 맞춰도 서버 권한, 연결 실패, 버전 협상, 결과 신뢰성까지 해결하지는 않습니다. 예제의 두 도구가 같은 운영 시간을 반환한다는 사실은 인터페이스 호환을 보여 주며 두 구현의 장애 특성이 같다는 '
                               '뜻은 아닙니다.\n',
                               '## 직접 LangChain 도구와 인터페이스 비교\n'
                               '\n'
                               '직접 도구와 MCP 변환 도구에 같은 입력을 넘기고 `name`, `args_schema`, 반환 내용을 비교합니다.\n'
                               '\n'
                               '직접 작성한 LangChain 도구와 MCP에서 변환한 도구에 같은 입력 사전을 넘긴 뒤 반환 메시지를 비교합니다. 호출 형태가 같아도 MCP 도구는 어댑터와 전송 계층을 거칩니다.\n'],
 '05-도구-정의와-첫-호출-토큰': ['## 패키지와 API 키 확인\n\n실측 모델 호출에 사용할 LangChain 버전과 API 키 존재 여부만 확인합니다. 키 값은 출력하지 않습니다.',
                       '## 직접 도구와 소형 MCP 서버 준비\n'
                       '\n'
                       '직접 도구 하나와 MCP에서 발견한 도구 하나를 준비하고 각 스키마를 저장합니다.\n'
                       '\n'
                       '### 코드 읽기와 비교 경계\n'
                       '\n'
                       "`bind_tools(tools, tool_choice='required')`는 선택 가능한 도구 정의를 첫 모델 요청에 포함하고 모델이 반드시 하나의 도구 호출을 만들도록 합니다. 이때 도구가 실행되는 것은 아닙니다. 반환한 첫 "
                       "`AIMessage`의 `tool_calls`에는 선택한 이름과 인자가 있고, `usage_metadata['input_tokens']`에는 공급자가 보고한 전체 입력 토큰이 있습니다. `schema_chars`는 도구 이름·설명·스키마를 "
                       '같은 JSON 방식으로 직렬화한 문자 수라서 정의 규모를 읽는 보조값입니다.\n'
                       '\n'
                       '도구 수와 입력 토큰의 관계를 분리해서 읽어야 합니다. 직접 도구 한 개와 MCP 도구 한 개는 연결 방식이 다르지만 모델에 보이는 변환 결과가 비슷할 수 있습니다. MCP 한 개와 다섯 개 비교에서는 개수뿐 아니라 각 이름과 설명의 내용도 '
                       '함께 바뀝니다. 따라서 이번 결과는 ‘이 정의 묶음에서 다섯 개 조건의 입력이 더 컸다’는 관찰입니다. 자주 쓰지 않는 도구를 상황에 따라 필터링하면 선택 오류와 입력 규모를 함께 줄일 수 있지만, 권한이 없는 도구를 숨기는 일은 서버의 '
                       '인가 검사를 대신하지 않습니다.\n',
                       '## 대형 MCP 서버와 다섯 도구 준비\n\n입력 형태가 다른 다섯 도구를 등록한 서버를 만들고 발견 목록을 저장합니다.',
                       '## 도구 정의 직렬화 크기 비교\n'
                       '\n'
                       '세 조건의 도구 정의를 JSON으로 직렬화해 문자 수를 비교하고 이를 모델 토큰과 구분합니다.\n'
                       '\n'
                       '`schema_chars`는 도구 정의를 JSON으로 직렬화한 문자 수입니다. 모델이 보고한 토큰 수와 동일한 단위가 아니므로 증가 방향을 설명하는 보조 측정값으로만 사용합니다.\n',
                       '## 같은 첫 모델 호출의 토큰 실측\n'
                       '\n'
                       '같은 질문과 모델을 사용하고 도구 정의 조건만 바꾸어 첫 응답의 `usage_metadata.input_tokens`를 기록합니다.\n'
                       '\n'
                       '세 조건은 같은 질문을 보내지만 도구 정의의 수와 내용이 함께 달라집니다. 따라서 입력 토큰 차이를 MCP 연결 하나의 효과로 해석하지 않습니다.\n',
                       '## 비용 계산과 해석 범위\n\n저장된 사용량에 실습의 고정 단가 가정을 적용합니다. 비용은 이 절의 핵심 학습 목표가 아니며 토큰 차이의 크기를 보조적으로 읽는 값입니다.']}

def notebook(slug: str, lesson: dict) -> dict:
    cells = [md(f"# {lesson['title']}\n\n{lesson['question']}"), md("## 실행 환경 준비\n\nPython 3.12 새 커널에서 첫 셀부터 순서대로 실행합니다. 비밀 값은 출력하지 않습니다.")]
    for item in lesson["cells"]:
        label, source, *part = item
        role = part[0] if part else None
        purpose = f"# {label}에 필요한 값을 준비하고 결과를 확인합니다.\n"
        step_index = len(cells) // 2 - 1
        cells.extend([md(REVIEWED_STEP_MARKDOWN[slug][step_index], role), code(purpose + source, role)])
    for index, cell in enumerate(cells, 1):
        cell["id"] = f"cell-{index:02d}"
    return {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.12"}, "lesson_format": lesson["format"]}, "nbformat": 4, "nbformat_minor": 5}


def render_source(slug: str, lesson: dict, number: int) -> str:
    goals = "".join(f"<li>{html.escape(item)}</li>" for item in lesson["goals"])
    notes = "".join(f"<li>{html.escape(item)}</li>" for item in lesson["notes"])
    quizzes = "".join(f'<details class="quiz"><summary>문제 {i}</summary><p class="quiz-q">{html.escape(q)}</p><p class="quiz-a"><b>해설</b> — {html.escape(a)}</p></details>' for i, (q, a) in enumerate(lesson["quiz"], 1))
    notebook_tag = f"{{{{notebook:{slug}}}}}" if lesson["format"] == "experiment" else f"{{{{notebook:{slug}|example}}}}"
    failure_title = "실험 결과 해석" if lesson["format"] == "experiment" else "일부러 실패해 보기"
    failure_tag = "" if lesson["format"] == "experiment" else f"{{{{notebook:{slug}|failure}}}}"
    return f'''<!--meta: {lesson['hours']} | 코드 Jupyter Notebook | 새 용어 {lesson['terms']} -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>{goals}</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>{html.escape(lesson['why'])}</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>{html.escape(lesson['prior'])}</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>쉬운 예</h3><p>{html.escape(lesson['concept'])}</p><h3>정의와 경계</h3><p>{html.escape(lesson['definition'])}</p><h3>코드 읽기와 비교 경계</h3>{enrichment_html(slug)}<h3>도식 읽기</h3>{{{{svg:{number:02d}-흐름}}}}<p>파란색은 클라이언트가 준비하거나 선택하는 항목, 초록색은 서버 기능, 주황색은 경계 또는 측정값을 뜻합니다. 화살표를 따라가며 어느 프로세스에서 연산이 실행되고 어떤 값만 다음 층으로 전달되는지 확인합니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 다른 절의 변수에 의존하지 않습니다. 첫 셀에서 고정 버전을 확인한 뒤 각 단계의 실제 반환값과 검사식을 함께 실행합니다.</p>{notebook_tag}<p class="look"><b>확인할 점</b> — {html.escape(lesson['observe'])}</p>
<h2 id="b6"><span class="no">6</span>{failure_title}</h2><p>{html.escape(lesson['observe'])}</p>{failure_tag}
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul>{notes}</ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>MCP의 발견·전송·모델 호출은 서로 다른 층이므로 각 층의 값을 따로 측정합니다.</li><li>서버 기능은 클라이언트가 발견할 수 있어도 인증과 인가를 통과한 범위에서만 실행합니다.</li><li>실습 결과는 고정 버전과 로컬 읽기 전용 서버의 범위에서 해석합니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — {html.escape(lesson['next'])}</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>{quizzes}
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><a href="https://modelcontextprotocol.io/specification/2025-11-25">MCP Specification 2025-11-25</a> · 확인 2026-09-11</li><li><a href="https://gofastmcp.com/v2/servers/server">FastMCP Server</a> · 실행 검증 4.0.3 · 확인 2026-09-11</li><li><a href="https://docs.langchain.com/oss/python/langchain/mcp">LangChain MCP</a> · LangChain 1.4.0 beta · 확인 2026-09-11</li></ul>
'''


def refuse_existing_drafts() -> None:
    """검토된 정본을 초기 초안 생성기로 덮어쓰지 않습니다."""
    targets = [
        *(CHAPTER / "_src" / f"{slug}.html" for slug in LESSONS),
        *(LAB / "notebooks" / f"{slug}.ipynb" for slug in LESSONS),
    ]
    existing = [path for path in targets if path.exists()]
    if existing:
        paths = "\n".join(f"- {path.relative_to(ROOT)}" for path in existing)
        raise FileExistsError(
            "Ch28 초안 생성기는 기존 교재 원본이나 실행 노트북을 덮어쓰지 않습니다. "
            "기존 파일을 읽고 필요한 부분만 직접 수정하세요.\n"
            f"{paths}"
        )


def main() -> None:
    refuse_existing_drafts()
    config = {
        "part": 6, "part_title": "Part 6 · 운영 가능한 Agent", "chapter": "ch28-mcp", "title": "MCP — Model Context Protocol", "hours": "총 16h · 강의 5h · 실습 11h",
        "objectives": ["MCP의 도구·리소스·프롬프트와 capability 협상을 설명할 수 있습니다.", "FastMCP 읽기 전용 서버를 만들고 stdio 클라이언트에서 호출할 수 있습니다.", "LangChain 1.4.0 MCPAdapter로 도구를 연결하고 첫 호출 입력 토큰을 측정할 수 있습니다.", "로컬·원격 전송의 인증과 최소 권한 경계를 구분할 수 있습니다."],
        "lab_path": "labs/part6/ch28-mcp", "sections": [{"slug": slug, "title": item["title"], "format": item["format"]} for slug, item in LESSONS.items()]}
    (CHAPTER / "chapter.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for number, (slug, lesson) in enumerate(LESSONS.items(), 1):
        (CHAPTER / "_src" / f"{slug}.html").write_text(render_source(slug, lesson, number), encoding="utf-8")
        path = LAB / "notebooks" / f"{slug}.ipynb"
        path.write_text(json.dumps(notebook(slug, lesson), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"authored {len(LESSONS)} lessons")


if __name__ == "__main__":
    main()
