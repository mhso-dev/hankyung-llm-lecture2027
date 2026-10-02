"""Ch 28 04절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe04.py P <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  P : 서버 파일 course_server.py를 stdio로 띄워 받은 MCP 도구(lookup_policy 하나)를 붙인 에이전트
      (create_agent + 호출 한도 3)에 질문 한 줄을 넣어 한 번 실행 — 노트북 5절 본 실행과 같은 코드
입력·도구·시스템 메시지 글·한도·질문은 04-probe.md §0과 같다(노트북과 같은 코드).
"""
import asyncio
import json
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

import psutil
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[6]
load_dotenv(ROOT / ".env")

from langchain_core._api import LangChainBetaWarning  # noqa: E402

warnings.filterwarnings("ignore", category=LangChainBetaWarning)
from langchain.mcp import MCPAdapter  # noqa: E402
from langchain.agents import create_agent  # noqa: E402
from langchain.agents.middleware import ModelCallLimitMiddleware  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import HumanMessage  # noqa: E402

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


model = init_chat_model(
    "openai:gpt-5.4-mini",
    temperature=0,
    reasoning_effort="none",
)
call_limit = ModelCallLimitMiddleware(run_limit=3, exit_behavior="end")
agent_rule = "교육센터 자료실 규정 질문에는 도구로 규정을 찾아, 찾은 글만 근거로 한국어 한 문장으로 답하세요."
question = "교육센터 자료실은 토요일에 몇 시까지 운영하나요?"


async def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    assert mode == "P"
    kernel_process = psutil.Process()
    course_config = stdio_config(server_file, quiet_env)
    adapter = MCPAdapter(course_config)
    mcp_tools = await adapter.list_tools()
    mcp_agent = create_agent(model, tools=mcp_tools, system_prompt=agent_rule, middleware=[call_limit])
    tool_names = [t.name for t in mcp_tools]
    nodes = list(mcp_agent.get_graph().nodes)
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            row = {"mode": mode, "round": round_no, "start": datetime.now(timezone.utc).strftime("%H:%M:%SZ"),
                   "tools": tool_names, "nodes": nodes}
            first_input = {"messages": [HumanMessage(content=question)]}
            try:
                result = await mcp_agent.ainvoke(first_input)
                msgs = result["messages"]
                new = msgs[len(first_input["messages"]):]
                row["kinds"] = [type(m).__name__ for m in msgs]
                ais = [m for m in new if type(m).__name__ == "AIMessage"]
                row["calls_per_response"] = [len(m.tool_calls) for m in ais]
                row["tool_names"] = [c["name"] for m in ais for c in m.tool_calls]
                row["tool_args"] = [c["args"] for m in ais for c in m.tool_calls]
                tms = [m for m in new if type(m).__name__ == "ToolMessage"]
                row["tool_status"] = [m.status for m in tms]
                row["tool_texts"] = [m.text for m in tms]
                row["tool_content_keys"] = [sorted(m.content[0].keys()) for m in tms]
                usage_none = [m for m in ais if m.usage_metadata is None]
                row["limit_hit"] = bool(usage_none) or ("Model call limits exceeded" in str(msgs[-1].content))
                asked = len([m for m in ais if m.tool_calls])
                row["asked_responses"] = asked
                row["requests"] = len(ais)
                row["requests_eq_asked_plus_1"] = len(ais) == asked + 1
                if not usage_none:
                    tin = sum(m.usage_metadata["input_tokens"] for m in ais)
                    tout = sum(m.usage_metadata["output_tokens"] for m in ais)
                    cache = sum(m.usage_metadata.get("input_token_details", {}).get("cache_read", 0) for m in ais)
                    row["input_tokens"], row["output_tokens"], row["cache_read"] = tin, tout, cache
                    row["per_request_input"] = [m.usage_metadata["input_tokens"] for m in ais]
                    row["per_request_output"] = [m.usage_metadata["output_tokens"] for m in ais]
                    # 노트북과 같은 셈(sum_usage는 캐시 입력 칸이 없어 모두 일반 입력으로 봄)
                    row["cost_notebook_way"] = round((tin * 0.75 + tout * 4.50) / 1000000, 6)
                    row["cost_with_cache"] = round(((tin - cache) * 0.75 + cache * 0.075 + tout * 4.50) / 1000000, 6)
                row["answer"] = msgs[-1].text
                row["answer_len"] = len(msgs[-1].text)
                row["children_after"] = len(kernel_process.children())
            except Exception as error:  # 기록만 하고 다음 회차로(다시 보내지 않음)
                row["error"] = type(error).__name__ + ": " + str(error)[:300]
            row["end"] = datetime.now(timezone.utc).strftime("%H:%M:%SZ")
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    asyncio.run(main())
