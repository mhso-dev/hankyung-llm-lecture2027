"""Ch 19 04절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe04.py <입력판 P|C1|C2> <조건 short|detailed|mixed> <회차 수> <기록 파일>
도구는 실행하지 않고 모델이 고른 도구 이름·인자·토큰만 기록한다. 설명 글은 author_03.py 상수를 그대로 쓴다.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / "textbook/part5/ch19-model-tools/qa/upgrade"))
sys.path.insert(0, str(ROOT / "labs/part5/ch19-model-tools/notebooks"))
from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")
import author_03  # noqa: E402
from langchain.chat_models import init_chat_model  # noqa: E402
from langchain.tools import tool  # noqa: E402
from order_tools import fetch_orders, find_order, sum_orders  # noqa: E402

csv_path = str(ROOT / "labs/part5/ch19-model-tools/data/orders.csv")
SHORT = {"a": "주문을 찾습니다.", "b": "주문 정보를 봅니다.", "c": "주문 금액을 봅니다."}
DETAIL = {"a": author_03.GOOD_LIST_DOC, "b": author_03.GOOD_GET_DOC, "c": author_03.GOOD_SUM_DOC}
SAME = {"a": "주문 정보를 봅니다.", "b": "주문 정보를 봅니다.", "c": "주문 정보를 봅니다."}
QUESTIONS = {
    "P": [("결제된(paid) 주문 목록을 보여 줘.", "tool_a"), ("O103 주문의 금액은 얼마야?", "tool_b"), ("결제된(paid) 주문은 모두 몇 건이야?", "tool_c")],
    "C1": [("결제된(paid) 주문 목록을 보여 줘.", "tool_a"), ("O103 주문의 금액은 얼마야?", "tool_b"), ("결제된(paid) 주문이 몇 건인지만 알려 줘.", "tool_c")],
    "C2": [("결제된(paid) 주문 목록을 보여 줘.", "tool_a"), ("O103 주문의 금액은 얼마야?", "tool_b"), ("결제된(paid) 주문은 모두 몇 건이야?", "tool_c")],
}


def make_tools(desc_a, desc_b, desc_c):
    @tool("tool_a", description=desc_a)
    def list_tool(status: str):
        return fetch_orders(csv_path, status=status)

    @tool("tool_b", description=desc_b)
    def get_tool(order_id: str):
        return find_order(csv_path, order_id)

    @tool("tool_c", description=desc_c)
    def sum_tool(status: str):
        return sum_orders(csv_path, status)

    return [list_tool, get_tool, sum_tool]


def descriptions(version, condition):
    short = SAME if version == "C2" else SHORT
    if condition == "short":
        return short["a"], short["b"], short["c"]
    if condition == "detailed":
        return DETAIL["a"], DETAIL["b"], DETAIL["c"]
    return short["a"], short["b"], DETAIL["c"]  # mixed: 합계 도구 설명만 자세한 판


def main():
    version, condition, rounds, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
    bound = model.bind_tools(make_tools(*descriptions(version, condition)), parallel_tool_calls=False)
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            for question, expected in QUESTIONS[version]:
                try:
                    response = bound.invoke(question)
                except Exception as error:  # 서비스 오류는 기록만
                    row = {"version": version, "condition": condition, "round": round_no, "question": question, "error": type(error).__name__ + ": " + str(error)[:300]}
                else:
                    names = [call["name"] for call in response.tool_calls]
                    row = {"version": version, "condition": condition, "round": round_no, "question": question, "expected": expected,
                           "names": names, "args": [call["args"] for call in response.tool_calls], "content": response.content,
                           "input_tokens": response.usage_metadata["input_tokens"], "output_tokens": response.usage_metadata["output_tokens"],
                           "cache_read": response.usage_metadata.get("input_token_details", {}).get("cache_read")}
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                print(json.dumps(row, ensure_ascii=False))


if __name__ == "__main__":
    main()
