"""Ch 28 06절(실습) 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe06.py P <회차 수> <기록 파일(JSONL, 이어 쓰기)>
  P : 노트북 실행 1(에이전트에 붙인 MCP 도구 하나)·실행 2(도구 셋 — 값 하나만 바꿈)를
      회차마다 노트북 차례대로 한 번씩 실행한다(ainvoke 한 번씩, 호출 한도 3).
입력·도구·시스템 메시지 글·질문·조립 함수는 06-probe.md §0과 같다(노트북과 같은 코드).
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
sys.path.insert(0, str(ROOT / "labs/part6/ch28-mcp/notebooks"))

from langchain_core._api import LangChainBetaWarning  # noqa: E402

warnings.filterwarnings("ignore", category=LangChainBetaWarning)
from langchain.mcp import MCPAdapter  # noqa: E402
from langchain.agents import create_agent  # noqa: E402
from langchain.agents.middleware import ModelCallLimitMiddleware  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.messages import HumanMessage  # noqa: E402
from connect_tools import estimate_cost, names_of, spec_length, sum_usage, tool_call_names  # noqa: E402

server_file = str(ROOT / "labs/part6/ch28-mcp/course_server.py")

model = init_chat_model(
    "openai:gpt-5.4-mini",
    temperature=0,
    reasoning_effort="none",
)

server_names = runpy.run_path(server_file)
server = server_names["mcp"]
policies = server_names["POLICIES"]


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


call_limit = ModelCallLimitMiddleware(run_limit=3, exit_behavior="end")
agent_rule = "교육센터 자료실 규정 질문에는 도구로 규정을 찾아, 찾은 글만 근거로 한국어 한 문장으로 답하세요."
question = "교육센터 자료실은 토요일에 몇 시까지 운영하나요?"


async def run_agent(chosen_tools):
    agent = create_agent(model, tools=chosen_tools, system_prompt=agent_rule, middleware=[call_limit])
    first_input = {"messages": [HumanMessage(content=question)]}
    result = await agent.ainvoke(first_input)
    return result["messages"]


def count_asked(messages):
    asked = 0
    for message in messages:
        if type(message).__name__ == "AIMessage":
            if len(tool_call_names(message)) > 0:
                asked = asked + 1
    return asked


input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50


async def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    assert mode == "P"
    practice_adapter = MCPAdapter(server)
    served_tools = await practice_adapter.list_tools()
    header = {"mode": "header", "served": names_of(served_tools),
              "spec": {"1": spec_length(served_tools[:1]), "3": spec_length(served_tools[:3])}}
    with open(out, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(header, ensure_ascii=False) + "\n")
        print(json.dumps(header, ensure_ascii=False))
        for round_no in range(1, rounds + 1):
            inputs_by_run = {}
            for run_name, tool_count in [("run1", 1), ("run2", 3)]:
                chosen_tools = served_tools[:tool_count]
                row = {"mode": mode, "round": round_no, "run": run_name, "tool_count": tool_count,
                       "tools": names_of(chosen_tools), "spec_length": spec_length(chosen_tools),
                       "start": datetime.now(timezone.utc).strftime("%H:%M:%SZ")}
                try:
                    messages = await run_agent(chosen_tools)
                    row["kinds"] = [type(m).__name__ for m in messages]
                    reqs = []
                    for m in messages:
                        if type(m).__name__ == "AIMessage":
                            u = m.usage_metadata
                            reqs.append({"tool_calls": tool_call_names(m), "args": [c["args"] for c in m.tool_calls],
                                         "input_tokens": u["input_tokens"], "output_tokens": u["output_tokens"],
                                         "cache_read": u.get("input_token_details", {}).get("cache_read", 0)})
                        if type(m).__name__ == "ToolMessage":
                            row.setdefault("tool_messages", []).append({"status": m.status, "text": m.text})
                    row["requests_detail"] = reqs
                    usage = sum_usage(messages)
                    asked = count_asked(messages)
                    row["requests"] = usage["requests"]
                    row["asked"] = asked
                    row["count_rule"] = usage["requests"] == asked + 1
                    row["input_total"] = usage["input_tokens"]
                    row["output_total"] = usage["output_tokens"]
                    row["cost_notebook"] = round(estimate_cost(usage, input_rate, cached_input_rate, output_rate), 6)
                    row["answer"] = messages[-1].text
                    row["answer_len"] = len(messages[-1].text)
                    inputs_by_run[run_name] = [r["input_tokens"] for r in reqs]
                except Exception as error:  # 기록만 하고 다음으로(다시 보내지 않음)
                    row["error"] = type(error).__name__ + ": " + str(error)[:300]
                row["end"] = datetime.now(timezone.utc).strftime("%H:%M:%SZ")
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                print(json.dumps(row, ensure_ascii=False)[:700])
            if "run1" in inputs_by_run and "run2" in inputs_by_run:
                first_inputs, second_inputs = inputs_by_run["run1"], inputs_by_run["run2"]
                diff = {"mode": "diff", "round": round_no, "same_count": len(first_inputs) == len(second_inputs)}
                if diff["same_count"]:
                    diff["added"] = [b - a for a, b in zip(first_inputs, second_inputs)]
                handle.write(json.dumps(diff, ensure_ascii=False) + "\n")
                print(json.dumps(diff, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
