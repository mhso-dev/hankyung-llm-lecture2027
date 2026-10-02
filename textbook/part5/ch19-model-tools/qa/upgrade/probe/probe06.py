"""Ch 19 06절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe06.py <모드 check|BW2|BW1|BE|AW2|AE|V> <회차 수> <기록 파일>
입력과 판단 규칙은 qa/upgrade/06-probe.md §0 (첫 요청 전에 적음).
쓰기 도구 cancel_order는 이 절의 흉내라 파일·주문 상태를 바꾸지 않는다.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / "labs/part5/ch19-model-tools/notebooks"))
from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.tools import tool  # noqa: E402
from langchain_core.messages import HumanMessage  # noqa: E402
from langchain_core.tools import ToolException  # noqa: E402
from order_tools import ask_until_answer, find_order, tool_call_names  # noqa: E402

csv_path = str(ROOT / "labs/part5/ch19-model-tools/data/orders.csv")
READ_DOC = "주문 번호로 주문 한 건을 찾습니다. 질문에 O103 같은 주문 번호가 있을 때 씁니다. 인자 order_id는 찾을 주문 번호입니다. 그 주문 한 줄을 딕셔너리로 내놓고, 없으면 오류를 냅니다."
WRITE_DOC = "주문 번호로 주문 취소 요청을 등록합니다. 손님이 주문을 취소해 달라고 할 때 씁니다. 인자 order_id는 취소할 주문 번호입니다. 등록한 주문 번호를 딕셔너리로 내놓습니다."
QUESTIONS = {
    "W2": "O101 주문을 취소해 줘.",
    "W1": "O101 주문을 취소할 수 있는지 알려 줘.",
    "E": "O999 주문의 금액을 알려 줘.",
}
MODES = {  # 모드: (도구 목록 이름, handle_tool_error, 질문, 흐름)
    "check": ("both", False, "W2", "first"),
    "BW2": ("both", False, "W2", "first"),
    "BW1": ("both", False, "W1", "first"),
    "BE": ("both", False, "E", "loop"),
    "AW2": ("read", True, "W2", "loop"),
    "AE": ("read", True, "E", "loop"),
    "V": ("both", True, "W2", "loop"),
}


@tool(description=READ_DOC)
def get_order_by_id(order_id: str):
    order = find_order(csv_path, order_id)
    if order is None:
        raise ToolException("주문 번호 " + order_id + "에 맞는 주문이 없습니다. 주문 번호를 다시 확인해 주세요.")
    return order


@tool(description=WRITE_DOC)
def cancel_order(order_id: str):
    return {"order_id": order_id, "cancel_requested": True}


def describe(messages):
    steps = []
    for m in messages:
        kind = type(m).__name__
        row = {"kind": kind}
        if kind == "AIMessage":
            row["names"] = tool_call_names(m)
            row["args"] = [c["args"] for c in m.tool_calls]
            row["content_len"] = len(m.content)
            row["usage"] = {"input": m.usage_metadata["input_tokens"], "output": m.usage_metadata["output_tokens"],
                            "cache_read": m.usage_metadata.get("input_token_details", {}).get("cache_read")}
        if kind == "ToolMessage":
            row["status"] = m.status
            row["content"] = m.content
        steps.append(row)
    return steps


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    list_name, handle, qkey, flow = MODES[mode]
    get_order_by_id.handle_tool_error = handle
    tools = [get_order_by_id, cancel_order] if list_name == "both" else [get_order_by_id]
    table = {t.name: t for t in tools}
    model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
    bound = model.bind_tools(tools, parallel_tool_calls=False)
    spec_names = [s["function"]["name"] for s in bound.kwargs["tools"]]
    question = QUESTIONS[qkey]
    with open(out, "a", encoding="utf-8") as handle_file:
        for round_no in range(1, rounds + 1):
            row = {"mode": mode, "round": round_no, "question": question, "spec_names": spec_names,
                   "handle_tool_error": handle}
            messages = [HumanMessage(content=question)]
            try:
                if flow == "first":
                    response = bound.invoke(messages)
                    messages.append(response)
                    row["model_name"] = response.response_metadata.get("model_name")
                else:
                    try:
                        ask_until_answer(bound, messages, table, 5)
                        row["stopped_by"] = None
                    except ToolException as error:
                        row["stopped_by"] = "ToolException: " + str(error)
                row["steps"] = describe(messages)
                ai = [s for s in row["steps"] if s["kind"] == "AIMessage"]
                row["requests"] = len(ai)
                row["message_count"] = len(messages)
                last = messages[-1]
                if type(last).__name__ == "AIMessage" and not last.tool_calls:
                    row["final_content"] = last.content
                    row["final_has_O999"] = "O999" in last.content
                row["accepted"] = True
            except Exception as error:  # 서비스 오류·받아들여지지 않음은 기록만
                row["accepted"] = False
                row["error"] = type(error).__name__ + ": " + str(error)[:500]
            handle_file.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False))


if __name__ == "__main__":
    main()
