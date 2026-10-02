from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CH = Path(__file__).resolve().parent
LAB = ROOT / "labs/part5/ch19-model-tools"

SECTIONS = [
    ("01-tool과-Ch4-함수-재사용", "@tool과 Ch4 함수 재사용", "paired"),
    ("02-Pydantic-인자와-반환-스키마", "Pydantic 인자와 반환 스키마", "paired"),
    ("03-좋은-도구-이름과-설명", "좋은 도구 이름과 설명", "experiment"),
    ("04-설명만으로-도구-선택하기", "설명만으로 도구 선택하기", "experiment"),
    ("05-bind_tools와-병렬-호출", "bind_tools와 병렬 호출", "experiment"),
    ("06-오류와-읽기-쓰기-분리", "오류와 읽기 도구·쓰기 도구 분리", "paired"),
]
LAB_HOURS = dict(zip((item[0] for item in SECTIONS), (2, 2, 1, 2, 2, 1)))

FETCH_SOURCE = '''from pathlib import Path
from typing import Any

import pandas as pd


def fetch_orders(csv_path: str | Path, *, status: str | None = None) -> list[dict[str, Any]]:
    """CSV 주문을 읽고 선택한 상태의 행을 사전 목록으로 반환합니다."""
    orders = pd.read_csv(csv_path, dtype={"order_id": "string", "customer_id": "string"})
    if status is not None:
        orders = orders.loc[orders["status"] == status]
    return orders.to_dict(orient="records")'''

PREP = '''from pathlib import Path
from dotenv import load_dotenv

def find_up(name: str) -> Path | None:
    current = Path.cwd().resolve()
    for folder in (current, *current.parents):
        candidate = folder / name
        if candidate.exists():
            return candidate
    return None

load_dotenv(find_up(".env"))
data_path = Path("data/orders.csv")
assert data_path.exists(), "노트북은 labs/part5/ch19-model-tools에서 실행합니다."
print("Python 실습 준비 완료")'''

def md(text: str, *, part: str | None = None) -> dict:
    meta = {} if part is None else {"lesson_part": part}
    return {"cell_type": "markdown", "metadata": meta, "source": text.splitlines(True)}

def code(text: str, *, part: str | None = None) -> dict:
    meta = {} if part is None else {"lesson_part": part}
    return {"cell_type": "code", "execution_count": None, "metadata": meta, "outputs": [], "source": text.splitlines(True)}

def notebook(title: str, fmt: str, cells: list[dict]) -> dict:
    for i, cell in enumerate(cells, 1):
        cell["id"] = f"cell-{i:02d}"
    return {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.12"}, "lesson_format": fmt}, "nbformat": 4, "nbformat_minor": 5}

def notebooks() -> dict[str, dict]:
    one_tool = '''from langchain.tools import tool
@tool
def list_orders_by_status(status: str) -> list[dict[str, Any]]:
    """주문 상태(paid, pending, cancelled)로 주문 목록을 조회합니다."""
    return fetch_orders(data_path, status=status)'''
    more_tools = '''@tool
def get_order_by_id(order_id: str) -> dict:
    """정확한 주문 ID로 주문 한 건의 상태와 금액을 조회합니다."""
    rows = fetch_orders(data_path)
    return next((r for r in rows if r["order_id"] == order_id), {"error": "주문을 찾지 못했습니다."})

@tool
def summarize_order_amounts(status: str) -> dict:
    """주문 상태별 건수와 총 주문 금액을 집계합니다."""
    rows = fetch_orders(data_path, status=status)
    return {"status": status, "count": len(rows), "total": sum(r["amount"] for r in rows)}'''
    schema_tool = '''from typing import Literal
from pydantic import BaseModel, Field
from langchain.tools import tool
class OrderQuery(BaseModel):
    status: Literal["paid", "pending", "cancelled"] = Field(description="조회할 주문 상태")
    limit: int = Field(default=3, ge=1, le=10, description="반환할 최대 주문 수")
@tool(args_schema=OrderQuery)
def search_orders(status: str, limit: int = 3) -> list[dict]:
    """주문 상태로 주문을 조회하고 최대 limit개를 반환합니다."""
    return fetch_orders(data_path, status=status)[:limit]'''
    model_setup = '''import os
from langchain_openai import ChatOpenAI
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY가 필요합니다."
MODEL = "gpt-5.4-mini"
model = ChatOpenAI(model=MODEL, temperature=0)
print({"model": MODEL, "temperature": 0, "예상_절별_비용_USD_상한": 1.0})'''
    n1 = notebook(SECTIONS[0][1], "paired", [md("# @tool과 Ch4 함수 재사용\n\n검증한 조회 함수에 도구 인터페이스를 더합니다."), md("## 준비\n\n공개 CSV와 Ch4 함수 원문을 사용합니다."), code(PREP), code(FETCH_SOURCE), md("## 도구 정의"), code(one_tool), md("## 같은 값 비교"), code('direct = fetch_orders(data_path, status="cancelled")\nwrapped = list_orders_by_status.invoke({"status": "cancelled"})\nprint({"same": direct == wrapped, "rows": wrapped})'), md("## 실패 재현", part="before"), code('try:\n    list_orders_by_status("paid")\nexcept TypeError as error:\n    print(type(error).__name__, str(error))', part="before"), md("## 수정", part="after"), code('result = list_orders_by_status.invoke({"status": "paid"})\nprint({"count": len(result), "first_id": result[0]["order_id"]})', part="after")])
    n2 = notebook(SECTIONS[1][1], "paired", [md("# Pydantic 인자와 반환 스키마\n\n허용 값과 개수 범위를 실행 전에 검사합니다."), md("## 준비"), code(PREP), code(FETCH_SOURCE), md("## 스키마와 정상 실행"), code(schema_tool + '\nprint(search_orders.args_schema.model_json_schema())\nprint(search_orders.invoke({"status": "paid", "limit": 2}))'), md("## 반환 형식"), code('value = search_orders.invoke({"status": "paid", "limit": 1})\nprint({"type": type(value).__name__, "fields": sorted(value[0])})'), md("## 실패 재현", part="before"), code('from pydantic import ValidationError\nfor invalid in [{"status": "shipped", "limit": 1}, {"status": "paid", "limit": 0}]:\n    try:\n        search_orders.invoke(invalid)\n    except ValidationError as error:\n        item = error.errors()[0]\n        print({"input": invalid, "type": item["type"], "loc": item["loc"]})', part="before"), md("## 수정", part="after"), code('print(search_orders.invoke({"status": "pending", "limit": 1}))', part="after")])
    n3 = notebook(SECTIONS[2][1], "experiment", [md("# 좋은 도구 이름과 설명\n\n목록·ID·집계 도구의 설명서를 비교합니다."), md("## 준비"), code(PREP), code(FETCH_SOURCE), code(one_tool), code(more_tools), md("## 모델이 보는 설명"), code('tools = [list_orders_by_status, get_order_by_id, summarize_order_amounts]\nfor item in tools:\n    print({"name": item.name, "description": item.description, "args": item.args})'), md("## 설명서 크기"), code('import json\nfor item in tools:\n    print(item.name, len(item.description), len(json.dumps(item.args, ensure_ascii=False)))'), md("## 실험 결과 해석\n\n선택 정확도는 다음 절에서 실제로 측정합니다.")])
    bad_defs = '''from langchain.tools import tool
@tool("list_orders_by_status", description="주문 정보를 찾습니다.")
def bad_status(status: str) -> list[dict]:
    return fetch_orders(data_path, status=status)
@tool("get_order_by_id", description="주문 정보를 찾습니다.")
def bad_id(order_id: str) -> dict:
    rows = fetch_orders(data_path)
    return next((r for r in rows if r["order_id"] == order_id), {"error": "주문을 찾지 못했습니다."})
@tool("summarize_order_amounts", description="주문 정보를 찾습니다.")
def bad_summary(status: str) -> dict:
    rows = fetch_orders(data_path, status=status)
    return {"status": status, "count": len(rows), "total": sum(r["amount"] for r in rows)}'''
    run_select = '''def run_selection(tools):
    bound = model.bind_tools(tools, parallel_tool_calls=False)
    logs = []
    for question, expected in questions:
        for repeat in range(REPEATS):
            response = bound.invoke(question)
            logs.append({"question": question, "expected": expected, "repeat": repeat + 1,
                         "tool_calls": response.tool_calls, "usage": response.usage_metadata})
    return logs
bad_logs = run_selection(bad_set)
good_logs = run_selection(good_set)
for condition, logs in [("모호", bad_logs), ("구체", good_logs)]:
    for row in logs:
        print(condition, row)'''
    n4 = notebook(SECTIONS[3][1], "experiment", [md("# 설명만으로 도구 선택하기\n\n공개 이름·스키마·동작을 유지하고 description만 바꿉니다."), md("## 준비"), code(PREP), code(model_setup), code(FETCH_SOURCE), md("## 모호한 설명"), code(bad_defs), md("## 구체적인 설명"), code(one_tool), code(more_tools), md("## 조건 확인"), code('bad_set = [bad_status, bad_id, bad_summary]\ngood_set = [list_orders_by_status, get_order_by_id, summarize_order_amounts]\nfor bad, good in zip(bad_set, good_set):\n    print({"same_name": bad.name == good.name, "same_args": bad.args == good.args,\n           "descriptions": [bad.description, good.description]})'), md("## 반복 조건"), code('questions = [("paid 주문 목록을 보여 줘", "list_orders_by_status"),\n             ("O103 주문을 찾아 줘", "get_order_by_id"),\n             ("paid 주문의 건수와 총액을 계산해 줘", "summarize_order_amounts")]\nREPEATS = 3\nprint({"questions": len(questions), "repeats": REPEATS, "calls_per_condition": 9})'), md("## 전체 호출 로그"), code(run_select), md("## 수동 채점"), code('def grade(logs):\n    names = [r["tool_calls"][0]["name"] if len(r["tool_calls"]) == 1 else None for r in logs]\n    return {"correct": sum(n == r["expected"] for n, r in zip(names, logs)), "total": len(logs)}\nprint({"ambiguous": grade(bad_logs), "specific": grade(good_logs)})'), md("## 실험 결과 해석\n\n질문 3개와 조건별 9회에서 관찰한 결과만 해석합니다.")])
    n5 = notebook(SECTIONS[4][1], "experiment", [md("# bind_tools와 병렬 호출\n\n요청, 실행, ToolMessage를 구분합니다."), md("## 준비"), code(PREP), code(model_setup), code(FETCH_SOURCE), code(one_tool), code(more_tools), md("## 병렬 호출 요청"), code('bound = model.bind_tools([get_order_by_id], parallel_tool_calls=True)\nquestion = "O101과 O103 주문을 각각 조회해 줘. 각 주문마다 도구를 한 번씩 호출해."\nai_message = bound.invoke(question)\nprint({"content": ai_message.text, "tool_calls": ai_message.tool_calls, "usage": ai_message.usage_metadata})'), md("## 실제 실행"), code('tool_messages = [get_order_by_id.invoke(call) for call in ai_message.tool_calls]\nfor message in tool_messages:\n    print({"type": type(message).__name__, "tool_call_id": message.tool_call_id, "content": message.content})'), md("## ID 대응"), code('requested_ids = [call["id"] for call in ai_message.tool_calls]\nreturned_ids = [message.tool_call_id for message in tool_messages]\nprint({"requested": requested_ids, "returned": returned_ids, "same": requested_ids == returned_ids})'), md("## 결과 전달"), code('final = bound.invoke([{"role": "user", "content": question}, ai_message, *tool_messages])\nprint(final.text)\nprint(final.usage_metadata)'), md("## 실험 결과 해석\n\n호출 두 개는 확인했지만 실행 시간의 동시성은 측정하지 않았습니다.")])
    n6 = notebook(SECTIONS[5][1], "paired", [md("# 오류와 읽기 도구·쓰기 도구 분리\n\n오류 코드와 제공 경로를 분리합니다."), md("## 준비"), code(PREP), code('from langchain.tools import tool\nORDERS = __import__("pandas").read_csv(data_path).to_dict(orient="records")'), md("## 읽기 도구"), code('@tool\ndef read_order(order_id: str) -> dict:\n    """주문 ID로 조회하며 데이터를 변경하지 않습니다."""\n    row = next((r for r in ORDERS if r["order_id"] == order_id), None)\n    return {"ok": True, "order": row} if row else {"ok": False, "error": "NOT_FOUND", "order_id": order_id}\nprint(read_order.invoke({"order_id": "O999"}))'), md("## 쓰기 도구"), code('@tool\ndef request_order_cancellation(order_id: str) -> dict:\n    """애플리케이션이 확인한 주문의 취소 요청을 기록합니다."""\n    return {"ok": True, "status": "cancellation_requested", "order_id": order_id}'), md("## 확인 전", part="before"), code('app_user_confirmed = False  # 신뢰하는 애플리케이션 상태의 실습값\navailable_tools = [read_order]\nprint({"confirmed": app_user_confirmed, "tools": [t.name for t in available_tools]})\nassert request_order_cancellation not in available_tools', part="before"), md("## 애플리케이션이 사용자 확인을 기록한 뒤", part="after"), code('app_user_confirmed = True  # 실제 서비스에서는 UI 확인 결과를 서버가 기록합니다.\navailable_tools = [read_order, request_order_cancellation] if app_user_confirmed else [read_order]\nprint({"confirmed": app_user_confirmed, "tools": [t.name for t in available_tools]})\nresult = request_order_cancellation.invoke({"order_id": "O101"})\nprint(result)', part="after")])
    return {slug: nb for (slug, _, _), nb in zip(SECTIONS, [n1, n2, n3, n4, n5, n6])}

DETAIL = {
    SECTIONS[0][0]: ("검증한 함수를 도구로 감싸는 경계를 설명할 수 있습니다.", "Ch4의 `fetch_orders()`는 CSV를 읽고 조건에 맞는 사전 목록을 반환합니다. 이번 절에서는 함수 본문을 바꾸지 않고 `@tool` 데코레이터로 모델이 읽을 이름·설명·입력 형식을 더합니다.", "직접 호출과 도구의 `invoke()` 결과를 비교하면 포장 전후의 업무 로직이 같음을 확인할 수 있습니다."),
    SECTIONS[1][0]: ("Pydantic으로 도구 인자의 범위와 의미를 검증할 수 있습니다.", "인자 스키마는 모델이 채워야 할 입력 칸과 각 칸의 조건을 정의합니다. `Field`의 설명과 최솟값·최댓값은 JSON Schema로 변환되어 모델과 실행기 사이의 공통 형식이 됩니다.", "유효하지 않은 `limit`은 조회 함수가 실행되기 전에 `ValidationError`로 거부됩니다."),
    SECTIONS[2][0]: ("서로 겹치지 않는 도구 이름과 설명을 작성할 수 있습니다.", "도구 이름은 동작과 대상을 함께 드러내야 합니다. 설명은 언제 이 도구를 골라야 하는지와 반환값을 짧게 밝힙니다. 세 도구가 목록 조회, ID 조회, 집계로 나뉘면 질문의 의도와 대응시키기 쉽습니다.", "설명과 스키마도 매 요청의 모델 컨텍스트에 들어가므로 길이를 측정하고 필요한 정보만 남깁니다."),
    SECTIONS[3][0]: ("같은 조건에서 도구 설명이 선택에 미치는 영향을 측정할 수 있습니다.", "모델은 함수 본문을 읽지 않습니다. 바인딩할 때 전달한 이름·설명·스키마만 보고 호출할 도구와 인자를 정합니다. 따라서 구현이 같아도 설명이 모호하면 선택 근거가 부족합니다.", "질문 3개, 반복 3회, 같은 모델과 temperature를 유지하고 설명만 바꿉니다. 전체 `tool_calls`와 사용량을 로그로 남긴 뒤 사람이 질문별 기대 도구와 비교합니다."),
    SECTIONS[4][0]: ("`bind_tools` 응답과 실제 도구 실행을 구분할 수 있습니다.", "`bind_tools()`는 모델에게 도구 설명서를 제공합니다. 모델의 `tool_calls`에는 이름·인자·고유 ID가 들어 있지만 조회 결과는 아직 없습니다. 프로그램이 호출을 실행하고 같은 ID를 가진 `ToolMessage`를 대화에 추가해야 결과를 바탕으로 답할 수 있습니다.", "한 질문이 독립된 두 주문을 요구하면 모델은 한 응답에 여러 호출을 낼 수 있습니다. 실제 출력의 호출 개수와 ID 대응을 확인합니다."),
    SECTIONS[5][0]: ("오류 결과를 모델이 읽을 수 있게 만들고 읽기와 쓰기 도구를 분리할 수 있습니다.", "예상 가능한 업무 오류는 `NOT_FOUND`처럼 짧고 일정한 코드와 관련 인자를 반환합니다. 쓰기 권한은 모델 인자가 아니라 애플리케이션이 기록한 사용자 확인 상태로 제어합니다.", "조회는 상태를 바꾸지 않지만 취소 요청은 부작용이 있습니다. 확인 전에는 읽기 도구만 제공하고 확인 뒤에만 쓰기 도구를 추가합니다."),
}
UNIQUE = {
    SECTIONS[0][0]: (
        "Ch4에서는 사람이 상태 값을 정해 함수를 호출했습니다. 이제 같은 함수가 모델이 선택할 수 있는 도구가 됩니다. 업무 로직을 다시 작성하지 않고 인터페이스만 추가해야 Ch4 테스트의 신뢰를 이어갈 수 있습니다.",
        "노트북에 <code>fetch_orders()</code> 원문을 인라인하고 공개 CSV도 함께 제공합니다. 학생은 Part1 폴더를 import하지 않아도 되며, 원본 함수와 AST가 같은지 검증 기록에서 확인할 수 있습니다.",
        "cancelled 상태를 직접 함수와 도구에 각각 넣습니다. O104 한 행이 양쪽에 나타나므로 빈 목록의 우연한 일치가 아닙니다.",
        "데코레이터를 붙인 뒤 변수는 일반 함수가 아니라 StructuredTool입니다. 일반 위치 인자로 부르지 않고 <code>invoke()</code>에 필드 이름이 있는 사전을 전달합니다.",
        "Ch4 함수의 반환값을 보존하면서 모델용 설명서를 추가했습니다.",
        "문제 5. cancelled 비교에서 O104가 양쪽에 나타난 사실은 무엇을 보여 주나요?<span class=\"quiz-a\">도구 포장이 기존 상태 필터와 반환 행을 바꾸지 않았음을 보여 줍니다.</span>",
    ),
    SECTIONS[1][0]: (
        "모델이 문자열을 만들 수 있다는 사실만으로 업무 입력이 안전해지지는 않습니다. 상태 이름의 허용 목록과 반환 개수 범위를 코드로 정하면 잘못된 요청을 데이터 조회 전에 멈출 수 있습니다.",
        "Ch4 함수의 status는 어떤 문자열도 받을 수 있었습니다. 이번 절은 Pydantic의 Literal과 Field 범위를 도구 경계에 추가해 실제 공개 데이터의 paid, pending, cancelled만 허용합니다.",
        "shipped와 limit 0을 각각 전달해 literal_error와 greater_than_equal을 확인합니다. 그 뒤 pending과 limit 1로 고쳐 정상 행을 받습니다.",
        "설명 문장에 허용 값을 적는 것만으로는 검증되지 않습니다. 자료형 또는 검증 규칙에도 같은 제약이 있어야 실행기가 거부할 수 있습니다.",
        "상태 목록과 개수 범위를 JSON Schema와 실제 검증에 함께 반영했습니다.",
        "문제 5. status 설명에만 허용 값을 쓰고 자료형을 str로 두면 어떤 문제가 있나요?<span class=\"quiz-a\">실행기는 허용 목록 밖의 문자열을 거부하지 못합니다.</span>",
    ),
    SECTIONS[2][0]: (
        "도구가 세 개가 되면 이름만 보아도 목록 조회, 한 건 조회, 집계를 구분할 수 있어야 합니다. 모델이 읽는 설명서를 출력해 사람도 그 차이를 점검합니다.",
        "01절의 상태별 목록 조회에 정확한 주문 ID 조회와 상태별 금액 집계를 더합니다. 세 함수는 모두 같은 Ch4 CSV를 읽지만 반환 목적이 다릅니다.",
        "각 도구의 name, description, args를 그대로 출력하고 설명과 스키마의 문자 수도 측정합니다. 이 수치는 토큰 수가 아니며 설명서 크기를 비교하는 보조 관찰입니다.",
        "도구 이름에는 동작과 대상을 함께 씁니다. get_data처럼 범위가 넓은 이름이나 같은 설명을 반복하면 질문과 도구를 대응할 근거가 줄어듭니다.",
        "목록, 단건, 집계 도구가 이름과 반환 목적에서 서로 구분됩니다.",
        "문제 5. <code>get_order_by_id</code>와 <code>list_orders_by_status</code>를 구분하는 핵심 입력은 무엇인가요?<span class=\"quiz-a\">하나는 정확한 order_id, 다른 하나는 status를 받습니다.</span>",
    ),
    SECTIONS[3][0]: (
        "좋은 설명이 선택을 돕는다는 주장을 확인하려면 설명 외의 조건을 고정해야 합니다. 공개 도구 이름과 인자 스키마, 함수 동작, 질문, 모델, temperature, 도구 순서를 같게 둡니다.",
        "03절의 세 도구를 두 묶음으로 다시 정의합니다. 모호 조건은 모두 ‘주문 정보를 찾습니다’라고 설명하고 구체 조건은 목록·단건·집계 목적을 각각 밝힙니다.",
        "질문 3개를 조건마다 3회씩 호출합니다. 전체 tool_calls와 사용량을 보존하고, 호출이 정확히 하나일 때 이름을 기대값과 사람이 비교합니다.",
        "temperature 0이어도 서비스 실행이 언제나 동일하다고 가정하지 않습니다. 9회라는 작은 표본과 사용한 질문에 한정해 결과를 보고합니다.",
        "description만 다른 두 조건의 실제 선택 기록을 같은 채점 기준으로 비교했습니다.",
        "문제 5. 이 실험에서 도구 순서를 고정하는 이유는 무엇인가요?<span class=\"quiz-a\">설명 외의 조건이 선택에 미치는 영향을 줄이기 위해서입니다.</span>",
    ),
    SECTIONS[4][0]: (
        "모델이 올바른 도구 이름과 인자를 만들었더라도 조회 결과는 아직 없습니다. 요청을 실행한 뒤 결과 메시지를 원래 호출과 연결하는 과정을 직접 확인해야 합니다.",
        "03절의 ID 조회 도구를 사용합니다. 공개 CSV에 실제로 있는 O101과 O103을 한 질문에 넣어 빈 결과가 아닌 주문 상태와 금액을 반환하게 합니다.",
        "모델 응답에서 호출 두 개와 각 ID를 먼저 출력합니다. 프로그램이 각 호출을 실행한 뒤 ToolMessage ID를 나란히 비교하고, 마지막 모델 호출에 결과를 전달합니다.",
        "parallel_tool_calls는 한 응답에 여러 호출을 허용하는 설정입니다. 이 노트북은 실제 함수 실행 시간을 측정하지 않으므로 동시에 실행됐다고 주장하지 않습니다.",
        "O101과 O103의 두 요청, 두 성공 결과, 두 ID의 대응을 확인했습니다.",
        "문제 5. ToolMessage의 ID가 요청 ID와 달라지면 무엇이 어려워지나요?<span class=\"quiz-a\">여러 결과 중 어느 것이 어느 요청의 답인지 모델이 연결하기 어려워집니다.</span>",
    ),
    SECTIONS[5][0]: (
        "주문 조회 실패와 주문 취소 요청은 위험이 다릅니다. 예상 가능한 조회 실패는 모델이 다음 판단에 사용할 오류 코드로 반환하고, 상태를 바꾸는 동작은 확인 경로를 별도로 둡니다.",
        "공개 주문 목록을 메모리에서 읽고 존재하지 않는 O999를 조회합니다. 쓰기 예제는 실제 주문을 변경하지 않고 취소 요청 상태만 구조화해 반환합니다.",
        "읽기 도구는 NOT_FOUND와 order_id를 반환합니다. 쓰기 도구는 모델이 정하는 confirmed 인자를 받지 않으며, 애플리케이션 확인 상태에 따라 제공 목록에 추가됩니다.",
        "예상 가능한 업무 실패와 시스템 예외를 구분합니다. 내부 스택 추적은 운영 로그에 남기고 모델에는 다음 행동에 필요한 코드와 대상만 제공합니다.",
        "읽기 질문의 도구 집합과 확인 뒤의 쓰기 도구 집합을 분리했습니다.",
        "문제 5. confirmed를 모델 인자로 받지 않는 이유는 무엇인가요?<span class=\"quiz-a\">모델이 True를 생성한 사실은 사용자가 확인했다는 증거가 아니기 때문입니다.</span>",
    ),
}
DEEP = {
    SECTIONS[0][0]: "도구로 감싼 뒤에도 CSV 경로는 프로그램이 넘깁니다. 모델에게 파일 경로까지 선택하게 하면 학습 목표와 관계없는 경로 오류가 늘어납니다. 이 절의 도구는 status만 공개하고 data_path는 함수 안에서 사용합니다. 직접 호출과 invoke 호출에 cancelled를 넣었을 때 모두 O104를 반환하므로 필터 조건과 행의 네 필드가 보존됐음을 읽을 수 있습니다. 반면 StructuredTool을 위치 인자로 호출한 TypeError는 주문 데이터의 실패가 아니라 인터페이스 사용 오류입니다. 실패의 층을 구분해야 수정 위치도 정확해집니다.",
    SECTIONS[1][0]: "Literal은 선택 가능한 문자열을 JSON Schema의 enum으로 나타냅니다. 모델은 paid, pending, cancelled라는 후보를 설명서에서 볼 수 있고, 실행기는 후보 밖의 shipped를 거부합니다. limit의 ge와 le는 각각 최솟값과 최댓값입니다. 두 제약은 서로 다른 오류 유형으로 출력됩니다. 반환값은 list 안에 주문 사전이 들어 있는 구조이므로 다음 모델 호출이 order_id와 amount를 필드 이름으로 읽을 수 있습니다. 스키마는 잘못된 입력을 줄이지만 데이터에 주문이 실제로 존재하는지까지 보장하지는 않습니다.",
    SECTIONS[2][0]: "목록 조회는 여러 행을 반환하고, ID 조회는 한 행을 반환하며, 집계는 count와 total을 새로 계산합니다. 세 도구의 입력 이름도 status, order_id, status로 나뉩니다. 이름만 길게 만든다고 좋은 설명이 되지는 않습니다. 언제 선택하는지와 무엇을 반환하는지가 서로 겹치지 않아야 합니다. 노트북이 출력하는 문자 수는 description과 args가 공짜가 아니라는 점을 눈으로 확인하기 위한 값입니다. 실제 토큰 수는 모델의 토크나이저와 직렬화 형식에 따라 달라지므로 문자 수를 비용으로 환산하지 않습니다.",
    SECTIONS[3][0]: "모호 조건과 구체 조건의 Python 함수 이름은 다르지만 모델에게 공개되는 tool name은 동일합니다. 노트북은 same_name과 same_args가 모두 True인지 먼저 확인합니다. 함수 본문도 같은 CSV 조회와 집계를 수행합니다. 따라서 모델에게 달라지는 정보는 description입니다. 채점은 목록 질문에는 list_orders_by_status, 정확한 주문 번호 질문에는 get_order_by_id, 건수와 총액 질문에는 summarize_order_amounts를 기대합니다. 두 조건이 모두 맞았다면 이 표본에서는 차이를 관찰하지 못했다고 기록해야 하며, 모호 조건이 틀렸을 때만 관찰된 차이를 설명합니다.",
    SECTIONS[4][0]: "AIMessage의 content가 비어 있어도 tool_calls가 있으면 모델은 답 대신 실행 요청을 보낸 것입니다. 각 항목의 name은 실행할 도구를, args는 전달할 주문 ID를, id는 결과 연결표를 나타냅니다. StructuredTool.invoke에 호출 사전 전체를 넘기면 LangChain은 실행 결과를 ToolMessage로 만들고 원래 id를 넣습니다. 마지막 호출에서는 사용자 질문, AIMessage, 두 ToolMessage를 순서대로 전달합니다. 이 메시지 순서가 어긋나거나 ID가 빠지면 제공자 API가 잘못된 대화 형식으로 판단할 수 있습니다.",
    SECTIONS[5][0]: "O999가 없다는 사실은 예상 가능한 업무 결과입니다. read_order는 예외 대신 ok=False, error=NOT_FOUND, order_id=O999를 반환합니다. 취소 도구에는 confirmed 필드가 없습니다. 확인 전 available_tools에는 읽기 도구만 있고, 신뢰하는 애플리케이션 상태가 사용자 확인을 기록한 뒤에만 취소 도구를 추가합니다. 이 예제의 True는 흐름을 보여 주는 로컬 실습값이며 실제 외부 동의가 아닙니다. 실제 서비스라면 인증, 권한, 중복 요청 방지 키, 감사 로그가 추가로 필요합니다.",
}
READING = {
    SECTIONS[0][0]: "출력을 읽을 때 먼저 same이 True인지 확인하고, 이어서 rows 안의 order_id가 O104인지 봅니다. True만 확인하면 두 결과가 모두 빈 목록인 경우를 놓칠 수 있습니다. 실제 행의 ID·고객 ID·상태·금액까지 같아야 기존 함수의 의미가 유지됐다고 말할 수 있습니다. 다음으로 도구 객체의 name과 description, args를 확인합니다. 이 세 값은 모델에게 전달되는 설명서이고 CSV 경로는 포함되지 않습니다. 학생이 상태를 paid로 바꾸면 두 행이 반환되며, 이 변화는 도구 포장 때문이 아니라 입력 상태가 달라졌기 때문입니다.",
    SECTIONS[1][0]: "오류 출력의 loc는 문제가 생긴 필드를 가리킵니다. shipped 입력에서는 status가, limit 0에서는 limit가 표시됩니다. type은 각각 허용 목록 위반과 최솟값 위반을 구분합니다. 프로그램은 이 정보를 운영 로그에 남기거나 사용자에게 고칠 항목을 안내할 수 있습니다. 수정 셀에서 pending을 넣으면 O102가 반환됩니다. 이 행은 공개 CSV에 실제로 있으므로 스키마 통과와 데이터 조회 성공을 함께 확인합니다. 단, Literal 후보를 바꾸면 모델 설명서와 테스트, 데이터 문서도 함께 갱신해야 합니다.",
    SECTIONS[2][0]: "세 설명서를 표처럼 읽어 봅니다. list_orders_by_status는 상태로 여러 주문을 찾는 질문에 대응합니다. get_order_by_id는 O103처럼 식별자가 들어간 질문에 대응합니다. summarize_order_amounts는 개별 행 대신 건수와 합계를 요구하는 질문에 대응합니다. 설명에 이 차이가 나타나지 않으면 모델은 인자 이름만으로 추측해야 합니다. args 출력은 status와 order_id의 차이를 보여 주지만 반환 목적은 알려 주지 않으므로 docstring이 필요합니다. 다음 절에서는 바로 이 설명 문장을 실험 변수로 삼습니다.",
    SECTIONS[3][0]: "실험 결과가 모호 9/9, 구체 9/9라면 이 실행에서는 선택 차이를 관찰하지 못한 것입니다. 이것은 설명이 필요 없다는 결론이 아닙니다. 질문에 주문 목록, 주문 번호, 건수와 총액이라는 강한 단서가 있고 인자 스키마도 서로 달라 모델이 구분했을 수 있습니다. 다른 질문이나 도구 수에서 결과가 달라질 수 있습니다. 차이를 더 조사하려면 질문 수를 늘리고 독립 실행을 반복하되, 결과를 얻기 위해 질문 문구를 조건마다 바꾸면 안 됩니다. 원시 tool_calls를 남겨야 수동 채점 오류도 다시 확인할 수 있습니다.",
    SECTIONS[4][0]: "첫 출력에서 content가 빈 문자열이고 tool_calls가 두 개인지 확인합니다. 이것은 모델이 최종 문장보다 두 조회를 먼저 요청했다는 뜻입니다. 두 번째 출력의 content에는 O101의 paid·32000과 O103의 paid·27000이 직렬화되어 있습니다. 세 번째 출력에서 requested와 returned 배열이 같은 순서와 값인지 확인합니다. 마지막 자연어 답은 두 도구 결과를 읽은 모델의 새 응답입니다. 중간 ToolMessage를 생략하고 마지막 호출을 보내면 모델은 주문 상태와 금액을 알 수 없습니다.",
    SECTIONS[5][0]: "NOT_FOUND는 재시도하면 항상 해결되는 시스템 장애가 아닙니다. 먼저 주문 ID를 확인하거나 사용자에게 올바른 대상을 요청해야 합니다. 쓰기 도구 제공 여부는 모델 출력과 분리된 애플리케이션 상태가 결정합니다. 확인 전 목록에 취소 도구가 없다는 assert는 구성 실수를 찾는 작은 검사입니다. 실제 취소 API를 연결할 때는 인증된 사용자와 대상 주문의 소유 관계도 검사해야 합니다.",
}
PRACTICE2 = {
    SECTIONS[0][0]: "직접 함수는 Python 코드가 이름을 정해 호출합니다. 도구 객체는 같은 함수를 모델 선택 후보로 표현합니다. 이 변화 때문에 함수의 책임까지 넓히면 안 됩니다. CSV 읽기와 상태 필터는 Ch4 함수가 맡고, 도구는 모델이 채울 status 한 칸만 공개합니다. 새로운 상태가 데이터에 추가되면 함수 테스트와 도구 설명을 함께 갱신합니다. 원본 해시는 출처 추적용이며 해시가 같다는 사실만으로 실행 결과까지 보장하지 않으므로 새 커널 비교도 수행합니다.",
    SECTIONS[1][0]: "JSON Schema를 출력하면 enum, minimum, maximum에 해당하는 제약을 찾을 수 있습니다. 모델 제공자는 이 설명을 도구 호출 형식으로 변환하지만 최종 검증 책임은 애플리케이션에 있습니다. 오류를 잡아 무조건 빈 목록으로 바꾸면 잘못된 상태와 검색 결과 없음이 구분되지 않습니다. 입력 오류는 입력 오류로 남기고, 허용된 입력에서 행이 없을 때만 빈 결과로 해석합니다. 반환 목록의 필드 이름도 안정적으로 유지해야 후속 모델이 금액과 상태를 혼동하지 않습니다.",
    SECTIONS[2][0]: "도구 설명을 작성한 뒤에는 실제 질문을 세 부류로 적어 봅니다. ‘paid 주문을 보여 줘’는 목록, ‘O103을 찾아 줘’는 단건, ‘paid 총액은 얼마야’는 집계입니다. 어느 질문이 두 도구 설명에 동시에 맞으면 경계가 겹친 것입니다. 이때 설명에 예문을 계속 붙이기보다 함수 책임을 나누거나 이름을 고치는 편이 낫습니다. 반환 필드 설명은 모델이 다음 답을 만들 때 필요한 정도로 적고, 내부 파일명이나 구현 라이브러리는 노출하지 않습니다.",
    SECTIONS[3][0]: "실험은 실행 전에 채점 기준과 반복 횟수를 정합니다. 결과를 본 뒤 기대 도구를 바꾸면 선택률을 믿을 수 없습니다. 한 응답에 호출이 없거나 둘 이상이면 이 실험에서는 오답으로 처리합니다. 전체 로그에는 질문, 기대 이름, 반복 번호, 원시 호출, 토큰 사용량이 있으므로 다른 검토자가 같은 규칙으로 다시 채점할 수 있습니다. 이번 실제 실행에서 두 조건이 모두 9/9이면 ‘혼동을 재현했다’고 쓰지 않고 차이를 관찰하지 못했다고 본문과 검증 기록에 남깁니다.",
    SECTIONS[4][0]: "두 주문 조회는 서로 의존하지 않으므로 모델이 호출 두 개를 한 응답에 담을 수 있는 사례입니다. 두 번째 주문이 첫 번째 결과를 필요로 한다면 같은 방식으로 병렬 요청하면 안 됩니다. 또한 호출 두 개가 생성됐다는 사실과 Python 함수가 동시에 실행됐다는 사실은 다릅니다. 이 노트북의 리스트 컴프리헨션은 순서대로 invoke를 호출합니다. 실제 동시 실행을 가르치려면 비동기 실행 시간과 시작·종료 기록을 별도 측정해야 하며, 그 내용은 이 절의 범위를 넘습니다.",
    SECTIONS[5][0]: "확인 상태는 대화 문장만 보고 추측하지 않습니다. 애플리케이션의 확인 화면이나 승인 API가 남긴 신뢰 가능한 상태를 서버가 읽어야 합니다. 실습의 app_user_confirmed=True는 이 경계를 보여 주는 고정 예시이며 실제 사용자의 승인을 대신하지 않습니다. 확인이 취소되거나 시간이 지나면 쓰기 도구를 다시 목록에서 제거해야 합니다. 도구 실행 뒤에는 order_id와 요청 상태를 반환하고, 실제 운영에서는 요청 식별자와 실행 시각도 감사 로그에 남깁니다.",
}
DEPTH_NOTE = {
    SECTIONS[0][0]: "복사 동등성은 소스 출처를 투명하게 남기기 위한 선택입니다. 실무에서는 검증된 함수를 패키지로 배포해 import하는 편이 중복을 줄입니다. 이 기본 노트북은 프로젝트 전용 import 없이도 실행되어야 하므로 짧은 원문을 포함했습니다. 원본이 바뀌면 해시와 AST 비교가 실패하도록 검증해야 두 사본이 조용히 달라지는 일을 막을 수 있습니다.",
    SECTIONS[1][0]: "반환 타입 주석은 독자에게 결과 구조를 알려 주지만 Pydantic 입력 검증과 같은 역할은 아닙니다. 반환값도 엄격히 검사해야 하는 서비스라면 별도의 결과 모델을 만들고 함수 경계에서 검증합니다. 이 절에서는 실제 사전 목록을 출력해 필드와 자료형을 사람이 읽는 범위까지만 다룹니다.",
    SECTIONS[2][0]: "도구 수가 늘어날 때는 새 도구를 추가하기 전에 기존 도구의 인자 하나로 표현할 수 있는지 검토합니다. 그러나 목록과 집계처럼 반환 의미가 크게 다르면 억지로 합치지 않습니다. 이름 충돌 검사와 대표 질문 표를 변경 검토에 넣으면 설명이 비슷해지는 시점을 일찍 찾을 수 있습니다.",
    SECTIONS[3][0]: "설명 품질 평가는 선택률 하나로 끝나지 않습니다. 올바른 도구를 골라도 status나 order_id를 잘못 채울 수 있으므로 인자 정확도도 별도로 봅니다. 이번 채점은 도구 이름만 평가하며 인자 값은 원시 로그에서 사람이 확인합니다. 평가 항목의 범위를 명시하면 9/9를 전체 성공률로 오해하지 않습니다.",
    SECTIONS[4][0]: "도구 결과를 모델에게 다시 보낼 때 원본 AIMessage도 함께 넣습니다. ToolMessage만 보내면 어떤 요청에 대한 결과인지 대화 기록이 완전하지 않습니다. 운영 로그에서는 호출 ID로 모델 요청, 함수 시작, 함수 종료, 최종 답을 연결하면 지연과 오류가 생긴 위치를 찾기 쉽습니다.",
    SECTIONS[5][0]: "읽기와 쓰기를 분리해도 쓰기 함수 자체의 검증은 필요합니다. 도구 목록은 선택 가능성을 제한하고, 함수 내부 권한 검사는 최종 방어선을 제공합니다. 모델이 도구를 호출하지 않는 별도 경로에서도 같은 쓰기 API가 사용될 수 있으므로 권한 검사를 도구 설명에만 의존하면 안 됩니다.",
}

def page(slug: str, title: str, fmt: str) -> str:
    goal, concept, observation = DETAIL[slug]
    reason, prior, practice, caution, summary, quiz = UNIQUE[slug]
    deep = DEEP[slug]
    reading = READING[slug]
    practice2 = PRACTICE2[slug]
    depth_note = DEPTH_NOTE[slug]
    concept = re.sub(r"`([^`]+)`", r"<code>\1</code>", concept)
    observation = re.sub(r"`([^`]+)`", r"<code>\1</code>", observation)
    quiz_question, quiz_answer = quiz.split('<span class="quiz-a">', 1)
    quiz_answer = quiz_answer.removesuffix("</span>")
    sec6 = "실험 결과 해석" if fmt == "experiment" else "일부러 실패해 보기"
    macro6 = "" if fmt == "experiment" else f"{{{{notebook:{slug}|failure}}}}"
    macro5 = f"{{{{notebook:{slug}}}}}" if fmt == "experiment" else f"{{{{notebook:{slug}|example}}}}"
    content = f'''<!--meta: 강의 1h | 실습 {LAB_HOURS[slug]}h | 코드 Jupyter Notebook | 새 용어 5 -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul><li>{goal}</li><li>노트북의 실제 출력에서 도구 이름, 인자, 결과를 확인할 수 있습니다.</li><li>관찰한 범위를 넘지 않고 결과를 해석할 수 있습니다.</li></ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>{reason}</p><p>Ch20에서 <code>ToolNode</code>로 실행 흐름을 조립하기 전에 도구 한 개가 어떤 정보와 결과를 주고받는지 확인합니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>{prior}</p><p>실행 파일은 <code>labs/part5/ch19-model-tools/data/orders.csv</code>를 사용하며 Part1 모듈을 런타임에 import하지 않습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 먼저 이해하기</h3><p>도구 설명서는 식당의 주문서와 비슷합니다. 손님은 주방 안의 조리 과정을 보지 않지만 메뉴 이름과 설명, 선택 항목을 보고 주문합니다. 모델도 Python 함수 본문을 보지 않고 도구 이름, 설명, 인자 스키마를 보고 호출 요청을 만듭니다. 주문서가 모호하면 주방이 정확해도 원하는 메뉴를 고르기 어렵습니다.</p><h3>정의</h3><p>{concept}</p><p><strong>도구 호출(tool call)</strong>은 모델이 프로그램에 보내는 구조화된 실행 요청입니다. <strong>인자 스키마(argument schema)</strong>는 요청에 필요한 필드와 형식을 적은 규칙입니다. <strong>도구 메시지(ToolMessage)</strong>는 실행 결과와 호출 ID를 모델에게 전달하는 메시지입니다. 요청과 결과를 구분하면 어느 단계에서 오류가 생겼는지 추적할 수 있습니다.</p><h3>도식 읽기</h3><figure><img src="figures/{slug}-flow.svg" alt="{title}의 입력, 선택, 실행, 결과 흐름"><figcaption>파란 상자는 모델이 읽는 정보, 초록 상자는 프로그램이 실행하는 함수, 주황 상자는 검사 또는 기록 지점입니다. 화살표는 데이터가 전달되는 순서를 나타냅니다.</figcaption></figure><p>도식에서 모델의 호출 요청과 함수 실행 사이가 분리되어 있습니다. 이 경계가 Ch20의 조건부 흐름으로 이어집니다. 이번 절의 노트북은 한 번의 요청과 결과만 다루며 자율 반복은 구현하지 않습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 먼저 이해하기</h3><p>도구 설명서는 주문서와 비슷합니다. 모델은 함수 내부를 보지 않고 이름, 설명, 선택 항목을 보고 요청합니다.</p><h3>정의</h3><p>{concept}</p><p>{deep}</p><p><strong>도구 호출(tool call)</strong>은 구조화된 실행 요청이며 <strong>도구 메시지(ToolMessage)</strong>는 실행 결과와 호출 ID를 돌려주는 메시지입니다.</p><h3>도식 읽기</h3><figure><img src="figures/{slug}-flow.svg" alt="{title}의 입력, 선택, 실행, 결과 흐름"><figcaption>파란 상자는 모델이 읽는 정보, 초록 상자는 프로그램이 실행하는 함수, 주황 상자는 검사 또는 기록 지점입니다.</figcaption></figure><p>모델 요청과 함수 실행 사이의 경계를 따라 읽습니다. 자율 반복은 Ch20 이후에 다룹니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>{practice}</p><p>빈 Python 3.12 커널에서 준비 셀부터 실행합니다. 모델 호출이 있는 절은 <code>gpt-5.4-mini</code>, <code>temperature=0</code>을 사용하며 키 값은 출력하지 않습니다.</p>{macro5}<p class="look"><b>확인할 점</b> — {observation}</p>
<h2 id="b6"><span class="no">6</span>{sec6}</h2><p>{observation} 같은 질문과 입력을 유지한 채 비교 대상 한 가지를 바꿉니다. 출력에 나타난 값만 근거로 삼으며, 작은 표본으로 모든 모델과 질문에 같은 결과가 난다고 단정하지 않습니다.</p><h3>출력 읽기</h3><p>{reading}</p>{macro6}
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><p>{caution}</p><p>{practice2}</p><p>{depth_note}</p><ul><li>도구 설명과 인자 스키마도 모델 컨텍스트를 사용합니다.</li><li>API 가격과 모델 동작은 달라질 수 있으므로 실행 시점의 공식 정보를 확인합니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>{summary}</li><li>관찰한 요청과 실행 결과를 구분해 기록했습니다.</li><li>작은 표본의 결과를 다른 모델과 질문에 일반화하지 않습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — Ch20에서는 <code>ToolNode</code>와 조건부 엣지가 호출 요청을 실행하고 결과를 다시 모델에 전달합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz"><summary>문제 1. 모델은 무엇을 보고 도구를 고르나요?</summary><p class="quiz-a">바인딩된 이름·설명·인자 스키마를 봅니다.</p></details><details class="quiz"><summary>문제 2. <code>tool_calls</code>가 있으면 실행도 끝났나요?</summary><p class="quiz-a">아닙니다. 프로그램이 검사하고 실행해야 합니다.</p></details><details class="quiz"><summary>문제 3. 이 절에서 확인한 실제 출력은 무엇인가요?</summary><p class="quiz-a">{observation}</p></details><details class="quiz"><summary>{quiz_question}</summary><p class="quiz-a">{quiz_answer}</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><p>공식 문서의 예제는 개념과 API 형태를 확인하는 근거로 사용했습니다. 교재 코드는 공개 주문 자료와 이 과정의 변수명으로 다시 작성하고 Python 3.12 새 커널에서 실행했습니다. 버전이 달라지면 import 경로와 메시지 형식이 달라질 수 있으므로 아래 기준 버전을 먼저 확인합니다.</p><ul><li><a href="https://docs.langchain.com/oss/python/langchain/tools">LangChain Tools</a> · 확인 2026-09-10 · LangChain 1.4.0</li><li><a href="https://docs.langchain.com/oss/python/langchain/models">LangChain Models: Tool calling</a> · 확인 2026-09-10</li><li><a href="https://docs.langchain.com/oss/python/langchain/messages">LangChain Messages</a> · 확인 2026-09-10</li><li><a href="https://docs.pydantic.dev/latest/concepts/models/">Pydantic Models</a> · 확인 2026-09-10 · Pydantic 2.12.5</li></ul>'''
    first_b4 = content.index('<h2 id="b4"')
    second_b4 = content.index('<h2 id="b4"', first_b4 + 1)
    return content[:first_b4] + content[second_b4:]

def main() -> None:
    for slug, title, fmt in SECTIONS:
        (CH / "_src" / f"{slug}.html").write_text(page(slug, title, fmt), encoding="utf-8")
    for slug, nb in notebooks().items():
        (LAB / "notebooks" / f"{slug}.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
