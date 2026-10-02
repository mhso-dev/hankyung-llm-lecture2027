"""Ch 19 05절 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe05.py <모드 check|P|M|C1|C2> <회차 수> <기록 파일>
  check : parallel_tool_calls=True + 과정 표준 설정 요청이 받아들여지는지 1번(첫 응답만)
  P/C1/C2 : parallel_tool_calls=True, 첫 요청 → 도구 실행 → 둘째 요청(요청 2번)
  M     : parallel_tool_calls=False, 도구 호출 요청이 없는 응답까지 되풀이(바퀴 한도 5)
도구 설명은 author_03.GOOD_GET_DOC 문자열 그대로, 몸통은 도구 파일 find_order.
"""
import json
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
from langchain_core.messages import HumanMessage  # noqa: E402
from order_tools import find_order  # noqa: E402

csv_path = str(ROOT / "labs/part5/ch19-model-tools/data/orders.csv")
QUESTIONS = {
    "check": "O101 주문과 O103 주문의 금액을 알려 줘.",
    "P": "O101 주문과 O103 주문의 금액을 알려 줘.",
    "M": "O101 주문과 O103 주문의 금액을 알려 줘.",
    "C1": "O101과 O103 주문을 각각 조회해 줘. 각 주문마다 도구를 한 번씩 호출해.",
    "C2": "O101 주문의 금액은 얼마고, O103 주문의 금액은 얼마야?",
}


@tool(description=author_03.GOOD_GET_DOC)
def get_order_by_id(order_id: str):
    return find_order(csv_path, order_id)


def usage_of(response):
    usage = response.usage_metadata
    return {"input": usage["input_tokens"], "output": usage["output_tokens"],
            "cache_read": usage.get("input_token_details", {}).get("cache_read")}


def one_response(response):
    return {"n_calls": len(response.tool_calls), "names": [c["name"] for c in response.tool_calls],
            "args": [c["args"] for c in response.tool_calls], "content_len": len(response.content),
            "usage": usage_of(response)}


def run_calls(response):
    out = []
    for call in response.tool_calls:
        out.append(get_order_by_id.invoke(call))
    return out


def markers(text):
    plain = text.replace(",", "")
    return {"has_32000": "32000" in plain, "has_27000": "27000" in plain}


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    assert get_order_by_id.description == author_03.GOOD_GET_DOC
    model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
    parallel = mode != "M"
    bound = model.bind_tools([get_order_by_id], parallel_tool_calls=parallel)
    question = QUESTIONS[mode]
    with open(out, "a", encoding="utf-8") as handle:
        for round_no in range(1, rounds + 1):
            row = {"mode": mode, "round": round_no, "question": question, "parallel_tool_calls": parallel}
            try:
                messages = [HumanMessage(question)]
                if mode == "check":
                    first = bound.invoke(messages)
                    row["accepted"] = True
                    row["first"] = one_response(first)
                    row["type"] = type(first).__name__
                    row["model_name"] = first.response_metadata.get("model_name")
                elif mode == "M":
                    steps = []
                    for turn in range(5):
                        response = bound.invoke(messages)
                        messages.append(response)
                        steps.append(one_response(response))
                        if not response.tool_calls:
                            break
                        for message in run_calls(response):
                            messages.append(message)
                    row["steps"] = steps
                    row["requests"] = len(steps)
                    row["final_content"] = messages[-1].content
                    row["markers"] = markers(messages[-1].content)
                    row["input_sum"] = sum(s["usage"]["input"] for s in steps)
                    row["output_sum"] = sum(s["usage"]["output"] for s in steps)
                else:
                    first = bound.invoke(messages)
                    tool_messages = run_calls(first)
                    row["first"] = one_response(first)
                    row["tool_msg_count"] = len(tool_messages)
                    row["ids_match"] = [c["id"] for c in first.tool_calls] == [m.tool_call_id for m in tool_messages]
                    row["tool_contents"] = [m.content for m in tool_messages]
                    messages.append(first)
                    for message in tool_messages:
                        messages.append(message)
                    final = bound.invoke(messages)
                    row["final"] = one_response(final)
                    row["final_content"] = final.content
                    row["markers"] = markers(final.content)
            except Exception as error:  # 서비스 오류·받아들여지지 않음은 기록만
                row["accepted"] = False
                row["error"] = type(error).__name__ + ": " + str(error)[:500]
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False))


if __name__ == "__main__":
    main()
