"""Ch 28 MCP — 앞 챕터와 이 챕터에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from connect_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
이 챕터 노트북이 실제로 쓰는 함수만 담고, 새 함수가 필요한 절이 그때 더합니다.
이 챕터 앞 절 노트북에서 옮긴 함수는 그 셀의 주석과 본문을 글자 그대로 옮겼습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
서버 파일(course_server.py 등)은 이 파일을 가져오지 않습니다.
자식 프로세스로 띄운 서버는 이 폴더를 가져오기 자리로 받지 않기 때문입니다.
"""

import json
import sys

from fastmcp import Client
from fastmcp.exceptions import ToolError
from langchain_core.utils.function_calling import convert_to_openai_tool


# Ch 28 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 목록의 항목마다 이름 칸 name을 모아 내놓습니다
def names_of(items):
    names = []
    for item in items:
        names.append(item.name)
    return names


# Ch 28 02절에서 배웠습니다 — 02절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 서버에 연결해 도구 하나를 부르고, 받은 결과나 오류를 한국어 키 딕셔너리로 내놓습니다
async def call_tool_row(server, tool_name, arguments):
    async with Client(server) as client:
        try:
            result = await client.call_tool(tool_name, arguments)
            row = {"받은 것": "결과", "글 줄": result.content[0].text.splitlines()}
        except ToolError as error:
            # 받은 오류의 종류 이름과, 오류 글을 줄마다 나눈 목록을 담습니다
            row = {"받은 것": type(error).__name__, "글 줄": str(error).splitlines()}
    return row


# Ch 28 03절에서 배웠습니다 — 03절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 서버 파일 하나를 stdio로 띄우는 MCP 설정 한 벌을 만들어 내놓습니다
def stdio_config(server_path, env):
    settings = {
        "command": sys.executable,
        "args": [server_path],
        "env": env,
        "keep_alive": False,
    }
    return {"mcpServers": {"server": settings}}


# Ch 19 04절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다
# 모델 응답 하나에서 도구 호출 목록의 도구 이름만 모아 목록으로 내놓습니다(도구를 고르지 않았으면 빈 목록)
def tool_call_names(response):
    names = []
    for call in response.tool_calls:
        names.append(call["name"])
    return names


# Ch 19 05절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다
# 메시지 목록에서 모델 응답(AIMessage)만 골라 요청 수와 입력·출력 토큰을 더해 딕셔너리로 내놓습니다
# 토큰 칸 이름은 usage_metadata와 같아서, 결과를 estimate_cost에 그대로 넘길 수 있습니다(캐시 입력 칸은 없음)
def sum_usage(messages):
    total = {"requests": 0, "input_tokens": 0, "output_tokens": 0}
    for message in messages:
        if type(message).__name__ == "AIMessage":
            usage = message.usage_metadata
            total["requests"] = total["requests"] + 1
            total["input_tokens"] = total["input_tokens"] + usage["input_tokens"]
            total["output_tokens"] = total["output_tokens"] + usage["output_tokens"]
    return total


# Ch 6 06절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다
# 사용량 딕셔너리와 세 요금(100만 토큰당 달러)으로 요청 한 번의 예상 비용(달러)을 계산합니다
# 사용량이 None이면 비용도 None을 내고, 입력 토큰 가운데 캐시 입력을 뺀 나머지를 일반 입력으로 봅니다
def estimate_cost(usage, input_rate, cached_input_rate, output_rate):
    if usage is None:
        return None
    # 캐시 입력 키가 없으면 할인 없이 모두 입력 요금으로 계산합니다
    details = usage.get("input_token_details", {})
    cache_read = details.get("cache_read", 0)
    normal_input = usage["input_tokens"] - cache_read
    input_cost = normal_input * input_rate + cache_read * cached_input_rate
    output_cost = usage["output_tokens"] * output_rate
    price_unit = 1000000
    return (input_cost + output_cost) / price_unit


# Ch 19 03절에서 배웠습니다 — Ch 19 03절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 도구 목록을 받아 도구마다 명세를 JSON 글로 바꾸고, 글자 수를 모두 더해 내놓습니다
def spec_length(tools):
    total = 0
    for one_tool in tools:
        spec = convert_to_openai_tool(one_tool)
        # 한글을 글자 그대로 두고 JSON 글로 바꿉니다
        spec_text = json.dumps(spec, ensure_ascii=False)
        total = total + len(spec_text)
    return total
