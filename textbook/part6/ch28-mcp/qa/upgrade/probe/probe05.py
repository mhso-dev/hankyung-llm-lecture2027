"""Ch 28 05절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe05.py P <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  P : 노트북 5절과 같은 첫 요청 다섯 조건(도구 없음 · MCP 도구 하나 · 직접 도구 하나 · 설명을 늘린 도구 하나 · MCP 도구 셋)을
      회차마다 노트북 차례대로 한 번씩 보낸다. 도구는 부르지 않는다(첫 요청 하나만).
입력·도구·시스템 메시지 글·질문은 05-probe.md §0과 같다(노트북과 같은 코드).
"""
import asyncio
import json
import runpy
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")

from langchain_core._api import LangChainBetaWarning  # noqa: E402

warnings.filterwarnings("ignore", category=LangChainBetaWarning)
from langchain.mcp import MCPAdapter  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import HumanMessage, SystemMessage  # noqa: E402
from langchain.tools import tool  # noqa: E402
from langchain_core.utils.function_calling import convert_to_openai_tool  # noqa: E402
from fastmcp import FastMCP  # noqa: E402

server_file = str(ROOT / "labs/part6/ch28-mcp/course_server.py")
quiet_env = {
    "FASTMCP_SHOW_SERVER_BANNER": "false",
    "FASTMCP_CHECK_FOR_UPDATES": "off",
    "FASTMCP_LOG_LEVEL": "WARNING",
}


def stdio_config(server_path, env):
    settings = {
        "command": sys.executable,
        "args": [server_path],
        "env": env,
        "keep_alive": False,
    }
    return {"mcpServers": {"server": settings}}


def spec_length(tools):
    total = 0
    for one_tool in tools:
        spec = convert_to_openai_tool(one_tool)
        # 한글을 글자 그대로 두고 JSON 글로 바꿉니다
        spec_text = json.dumps(spec, ensure_ascii=False)
        total = total + len(spec_text)
    return total


model = init_chat_model(
    "openai:gpt-5.4-mini",
    temperature=0,
    reasoning_effort="none",
)

server_names = runpy.run_path(server_file)
server = server_names["mcp"]
policies = server_names["POLICIES"]


@tool("lookup_policy")
def direct_lookup(topic: str):
    """자료실 규정을 조회합니다. topic은 대출, 운영, 연체 중 하나입니다."""
    return policies[topic]


longer = FastMCP("설명을 늘린 자료실")


@longer.tool
def lookup_policy(topic: str):
    """자료실 규정을 조회합니다. topic은 대출, 운영, 연체 중 하나입니다. 대출·운영·연체 규정을 물을 때 씁니다. 그 주제의 규정 글 한 문장을 내놓습니다."""
    return policies[topic]


@server.tool
def search_topics(word: str):
    """규정 글에 낱말이 든 주제어를 찾습니다. word에는 찾을 낱말을 넣습니다."""
    found = []
    for topic in policies:
        if word in policies[topic]:
            found.append(topic)
    return found


@server.tool
def show_topics():
    """자료실 규정의 주제어 목록을 알려 줍니다."""
    return list(policies)


agent_rule = "교육센터 자료실 규정 질문에는 도구로 규정을 찾아, 찾은 글만 근거로 한국어 한 문장으로 답하세요."
question = "교육센터 자료실은 토요일에 몇 시까지 운영하나요?"
first_messages = [SystemMessage(content=agent_rule), HumanMessage(content=question)]


async def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    assert mode == "P"
    course_config = stdio_config(server_file, quiet_env)
    adapter = MCPAdapter(course_config)
    mcp_tools = await adapter.list_tools()
    long_tools = await MCPAdapter(longer).list_tools()
    wide_tools = await MCPAdapter(server).list_tools()
    mcp_model = model.bind_tools(mcp_tools)
    direct_model = model.bind_tools([direct_lookup])
    long_model = model.bind_tools(long_tools)
    wide_model = model.bind_tools(wide_tools)
    conditions = [
        ("none", model, 0),
        ("mcp", mcp_model, spec_length(mcp_tools)),
        ("direct", direct_model, spec_length([direct_lookup])),
        ("long", long_model, spec_length(long_tools)),
        ("wide", wide_model, spec_length(wide_tools)),
    ]
    header = {"mode": "header", "mcp_names": [t.name for t in mcp_tools], "long_names": [t.name for t in long_tools],
              "wide_names": [t.name for t in wide_tools], "spec_lengths": {c[0]: c[2] for c in conditions}}
    with open(out, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(header, ensure_ascii=False) + "\n")
        print(json.dumps(header, ensure_ascii=False))
        for round_no in range(1, rounds + 1):
            for name, bound, length in conditions:
                row = {"mode": mode, "round": round_no, "condition": name, "spec_length": length,
                       "start": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
                try:
                    reply = bound.invoke(first_messages)
                    usage = reply.usage_metadata
                    row["input_tokens"] = usage["input_tokens"]
                    row["output_tokens"] = usage["output_tokens"]
                    row["cache_read"] = usage.get("input_token_details", {}).get("cache_read", 0)
                    row["tool_calls"] = [c["name"] for c in reply.tool_calls]
                    row["tool_args"] = [c["args"] for c in reply.tool_calls]
                    row["text_len"] = len(reply.text)
                    row["text"] = reply.text[:200]
                    row["cost"] = round(((usage["input_tokens"] - row["cache_read"]) * 0.75 + row["cache_read"] * 0.075
                                         + usage["output_tokens"] * 4.50) / 1000000, 8)
                except Exception as error:  # 기록만 하고 다음으로(다시 보내지 않음)
                    row["error"] = type(error).__name__ + ": " + str(error)[:300]
                row["end"] = datetime.now(timezone.utc).strftime("%H:%M:%SZ")
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                print(json.dumps(row, ensure_ascii=False)[:600])


if __name__ == "__main__":
    asyncio.run(main())
