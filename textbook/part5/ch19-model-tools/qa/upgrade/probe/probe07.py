"""Ch 19 07절(실습) 흔들림 확인 (노트북 밖). 키 값은 루트 .env에서만 읽고 출력하지 않는다.

사용: python probe07.py <모드 check|A|B> <회차 수> <기록 파일>
입력과 고르는 규칙은 qa/upgrade/07-probe.md §0 (첫 요청 전에 적음).
도구·양식 클래스·조립 함수·기록 장치는 author_07.py의 노트북 코드 셀 문자열을 그대로 exec 한다.
쓰기 도구 request_cancel은 이 절의 흉내라 파일·주문 상태를 바꾸지 않는다.
"""
import contextlib
import io
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / "labs/part5/ch19-model-tools/notebooks"))
sys.path.insert(0, str(ROOT / "textbook/part5/ch19-model-tools/qa/upgrade"))
from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")
import author_07  # noqa: E402

INQUIRIES = {
    "A": "O102 주문이 아직 결제 대기 중이면 취소해 주세요. 다른 상품을 잘못 주문했어요.",
    "B": "O102 주문을 취소해 주세요. 다른 상품을 잘못 주문했어요.",
}


def build_namespace():
    os.chdir(ROOT)
    namespace = {}
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        for cell in author_07.SETUP_CELLS:
            exec(cell, namespace)
    from langchain.chat_models import init_chat_model
    namespace["model"] = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")
    return namespace, buffer.getvalue()


def describe(result, body_lines):
    steps = []
    for m in result["메시지"]:
        kind = type(m).__name__
        row = {"kind": kind}
        if kind == "AIMessage":
            row["names"] = [c["name"] for c in m.tool_calls]
            row["args"] = [c["args"] for c in m.tool_calls]
            row["content_len"] = len(m.content)
            u = m.usage_metadata
            row["usage"] = {"input": u["input_tokens"], "output": u["output_tokens"],
                            "cache_read": u.get("input_token_details", {}).get("cache_read")}
            row["model_name"] = m.response_metadata.get("model_name")
        if kind == "ToolMessage":
            row["status"] = m.status
            row["content"] = m.content
        steps.append(row)
    return {"spec": result["명세"], "steps": steps, "body_lines": body_lines,
            "last_tool_calls": len(result["메시지"][-1].tool_calls),
            "final_content": result["메시지"][-1].content}


def main():
    mode, rounds, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    namespace, setup_out = build_namespace()
    print("SETUP OUTPUT (inquiry cell not used by probe flows):")
    print(setup_out)
    handle = namespace["handle_inquiry"]
    summarize = namespace["summarize_run"]
    question = INQUIRIES["A" if mode == "check" else mode]
    with open(out, "a", encoding="utf-8") as fh:
        if mode == "check":
            from langchain_core.messages import HumanMessage
            tools = namespace["read_tools"] + namespace["write_tools"]
            bound = namespace["model"].bind_tools(tools, parallel_tool_calls=False)
            row = {"mode": "check", "question": question,
                   "spec": [s["function"]["name"] for s in bound.kwargs["tools"]],
                   "write_spec": bound.kwargs["tools"][1]}
            try:
                response = bound.invoke([HumanMessage(content=question)])
                row["accepted"] = True
                row["names"] = [c["name"] for c in response.tool_calls]
                row["args"] = [c["args"] for c in response.tool_calls]
                row["content_len"] = len(response.content)
                u = response.usage_metadata
                row["usage"] = {"input": u["input_tokens"], "output": u["output_tokens"],
                                "cache_read": u.get("input_token_details", {}).get("cache_read")}
                row["model_name"] = response.response_metadata.get("model_name")
            except Exception as error:  # 받아들여지지 않으면 기록만
                row["accepted"] = False
                row["error"] = type(error).__name__ + ": " + str(error)[:500]
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps(row, ensure_ascii=False))
            return
        for round_no in range(1, rounds + 1):
            row = {"mode": mode, "round": round_no, "question": question}
            for label, confirmed in (("run1", False), ("run2", True)):
                buffer = io.StringIO()
                try:
                    with contextlib.redirect_stdout(buffer):
                        result = handle(namespace["model"], namespace["read_tools"], namespace["write_tools"],
                                        confirmed, question, 5)
                    body = [l for l in buffer.getvalue().splitlines() if l.startswith("쓰기 도구 몸통 실행")]
                    info = describe(result, body)
                    info["summary"] = summarize(result)
                    row[label] = info
                except Exception as error:
                    row[label] = {"error": type(error).__name__ + ": " + str(error)[:500],
                                  "stdout": buffer.getvalue()[:500]}
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            s1 = row["run1"].get("summary")
            s2 = row["run2"].get("summary")
            print(round_no, "run1", s1, "| run2", s2)


if __name__ == "__main__":
    main()
