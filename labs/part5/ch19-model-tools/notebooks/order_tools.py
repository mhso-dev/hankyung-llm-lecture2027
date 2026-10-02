"""Ch 19 모델과 도구 — 앞 챕터와 이 챕터 앞 절에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from order_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
함수를 도구로 감싸는 @tool 줄은 이 파일에 두지 않고 노트북에 둡니다.
"""
import pandas as pd


# Ch 4 01절에서 배웠습니다 — Ch 4 실습 폴더 data_tools.py의 판을 옮겼습니다(자료형 표시와 설명 글을 빼고 주석을 달았습니다)
# CSV 파일 위치를 받아 주문을 읽고, status를 주면 그 상태의 줄만 남겨 딕셔너리 목록으로 내놓습니다
# 별표 * 뒤의 status는 이름을 붙여서만 넘기고(status="paid"), 넘기지 않으면 None이라 모든 줄을 남깁니다
def fetch_orders(csv_path, *, status=None):
    # 주문 번호와 고객 번호 두 칸만 글자로 읽습니다(금액 칸은 정수로 남습니다)
    orders = pd.read_csv(csv_path, dtype={"order_id": "string", "customer_id": "string"})
    if status is not None:
        orders = orders.loc[orders["status"] == status]
    return orders.to_dict(orient="records")


# Ch 6 06절에서 배웠습니다 — 사용량 딕셔너리와 세 요금(100만 토큰당 달러)으로 요청 한 번의 예상 비용(달러)을 계산합니다
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


# Ch 19 03절에서 배웠습니다
# 주문 번호 하나로 주문 한 줄을 찾아 딕셔너리로 내놓고, 없으면 None을 내놓습니다
def find_order(csv_path, order_id):
    found = None
    # 모든 주문을 읽고, 번호가 같은 줄을 만나면 담고 멈춥니다
    for row in fetch_orders(csv_path):
        if row["order_id"] == order_id:
            found = row
            break
    return found


# Ch 19 03절에서 배웠습니다
# 주문 상태 하나로 그 상태의 주문 수와 금액 합계를 세어 딕셔너리로 내놓습니다
def sum_orders(csv_path, status):
    rows = fetch_orders(csv_path, status=status)
    total = 0
    # 줄마다 금액을 더해 합계를 만듭니다
    for row in rows:
        total = total + row["amount"]
    return {"status": status, "count": len(rows), "total": total}


# Ch 19 04절에서 배웠습니다
# 모델 응답 하나에서 도구 호출 목록의 도구 이름만 모아 목록으로 내놓습니다(도구를 고르지 않았으면 빈 목록)
def tool_call_names(response):
    names = []
    for call in response.tool_calls:
        names.append(call["name"])
    return names


# Ch 19 04절에서 배웠습니다
# 도구를 알려 준 모델에 질문마다 정한 횟수만큼 요청을 보내고(요청 수 = 질문 수 × 횟수), 고른 도구 이름과 사용량을 기록합니다
# expected_tools는 {질문: 기대 도구 이름} 딕셔너리이고, 기록 한 줄은 칸 「질문」·「고른 도구」·「사용량」을 담습니다
def ask_questions(bound_model, expected_tools, repeats):
    records = []
    for question in expected_tools:
        for turn in range(repeats):
            response = bound_model.invoke(question)
            names = tool_call_names(response)
            records.append({"질문": question, "고른 도구": names, "사용량": response.usage_metadata})
    return records


# Ch 19 04절에서 배웠습니다
# 기록마다 고른 도구가 기대 도구 하나뿐인지 보고, 맞은 기록 수를 셉니다(도구 이름만 보고 인자는 보지 않습니다)
def count_expected(records, expected_tools):
    matched = 0
    for record in records:
        expected = [expected_tools[record["질문"]]]
        if record["고른 도구"] == expected:
            matched = matched + 1
    return matched


# Ch 19 05절에서 배웠습니다
# 응답의 도구 호출 요청을 받은 차례대로 하나씩 실행해, 도구 메시지(ToolMessage) 목록을 내놓습니다
# tools_by_name은 {공개 이름: 도구} 딕셔너리이고, 요청을 통째로 넣어야 호출 ID가 도구 메시지에 옮겨집니다
def run_tool_calls(response, tools_by_name):
    tool_messages = []
    for call in response.tool_calls:
        # 공개 이름으로 도구를 찾고, 요청을 통째로 넣어 도구 메시지를 받습니다
        one_tool = tools_by_name[call["name"]]
        tool_messages.append(one_tool.invoke(call))
    return tool_messages


# Ch 19 05절에서 배웠습니다
# 도구 호출 요청이 없는 응답이 올 때까지 도구를 실행하고 다시 묻습니다(바퀴 한 번에 모델 요청 한 번, turn_limit 바퀴까지)
# 받은 메시지 목록에 응답과 도구 메시지를 이어 붙이고, 그 목록을 내놓습니다
def ask_until_answer(bound_model, messages, tools_by_name, turn_limit):
    for turn in range(turn_limit):
        response = bound_model.invoke(messages)
        messages.append(response)
        # 도구 호출 요청이 없으면 최종 답이라 멈춥니다
        if len(response.tool_calls) == 0:
            break
        for message in run_tool_calls(response, tools_by_name):
            messages.append(message)
    return messages


# Ch 19 05절에서 배웠습니다
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


# Ch 19 06절에서 배웠습니다
# 사람 확인 값(person_confirmed)에 따라 모델에게 알려 줄 도구 목록을 만듭니다
# 읽기 도구 목록은 늘 담고, 사람이 확인한 뒤(True)에만 쓰기 도구 목록을 뒤에 더합니다
def pick_tools(read_tools, write_tools, person_confirmed):
    # 읽기 도구는 늘 담고, 원래 목록을 건드리지 않게 새 목록으로 복사합니다
    tools = list(read_tools)
    # 사람이 확인한 뒤에만 쓰기 도구를 목록에 더합니다
    if person_confirmed:
        tools = tools + write_tools
    return tools


# Ch 19 06절에서 배웠습니다 — 05절 4절에서 셀로 만든 도구 찾기 표를 함수로 옮겼습니다
# 도구 목록을 받아 {공개 이름: 도구} 딕셔너리를 내놓습니다(알려 준 목록으로 만들면 알려 주지 않은 도구는 표에 없습니다)
def make_tools_table(tools):
    tools_by_name = {}
    for one_tool in tools:
        tools_by_name[one_tool.name] = one_tool
    return tools_by_name


# Ch 19 06절에서 배웠습니다
# bind_tools로 도구를 알려 준 모델이 요청마다 싣는 명세(kwargs["tools"])에서 도구 이름만 모아 목록으로 내놓습니다(요청은 보내지 않음)
def spec_names(bound_model):
    names = []
    for spec in bound_model.kwargs["tools"]:
        # 명세 한 건은 04절에서 본 모양이고, 도구 이름은 칸 function 안에 있습니다
        names.append(spec["function"]["name"])
    return names


# Ch 19 06절에서 배웠습니다
# 메시지 목록을 차례로 보며 종류 이름을 출력하고, 응답(AIMessage)이면 도구 호출 요청 이름을,
# 도구 메시지(ToolMessage)면 결과 상태(status)와 내용을 함께 출력합니다(내놓는 값 없음)
def show_messages(messages):
    for message in messages:
        kind = type(message).__name__
        if kind == "HumanMessage":
            print(kind)
        if kind == "AIMessage":
            print(kind, "| 도구 호출 요청:", tool_call_names(message))
        if kind == "ToolMessage":
            print(kind, "| 결과 상태:", message.status, "| 내용:", message.content)
