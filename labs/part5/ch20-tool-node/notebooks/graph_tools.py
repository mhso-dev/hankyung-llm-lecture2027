"""Ch 20 ToolNode — 앞 챕터에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from graph_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
Ch 19 도구 파일 order_tools.py에서 이 챕터 노트북이 쓰는 함수만 본문을 글자 그대로 옮겼습니다.
이 챕터 01절 노트북에서 처음 가르친 함수도 같은 방법으로 옮겼습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
도구를 만드는 @tool 줄과 그래프의 노드 함수는 이 파일에 두지 않고 노트북에 둡니다.
"""


# Ch 19 04절에서 배웠습니다 — Ch 19 도구 파일 order_tools.py의 같은 이름 함수를 옮겼습니다
# 모델 응답 하나에서 도구 호출 목록의 도구 이름만 모아 목록으로 내놓습니다(도구를 고르지 않았으면 빈 목록)
def tool_call_names(response):
    names = []
    for call in response.tool_calls:
        names.append(call["name"])
    return names


# Ch 19 06절에서 배웠습니다 — Ch 19 도구 파일 order_tools.py의 같은 이름 함수를 옮겼습니다
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


# Ch 19 05절에서 배웠습니다 — Ch 19 도구 파일 order_tools.py의 같은 이름 함수를 옮겼습니다
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


# Ch 6 06절에서 배웠습니다 — Ch 19 도구 파일 order_tools.py의 같은 이름 함수를 옮겼습니다
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


# Ch 20 01절에서 배웠습니다 — 01절 노트북 7절의 같은 이름 함수를 옮겼습니다
# 메시지 목록에서 도구 호출 요청의 id 목록과 도구 메시지의 호출 ID 목록을 모아 내놓습니다
def call_id_lists(messages):
    lists = {"요청 id": [], "호출 ID": []}
    for message in messages:
        if type(message).__name__ == "AIMessage":
            for call in message.tool_calls:
                lists["요청 id"].append(call["id"])
        if type(message).__name__ == "ToolMessage":
            lists["호출 ID"].append(message.tool_call_id)
    return lists


# Ch 20 01절에서 배웠습니다 — 01절 노트북 10절의 같은 이름 함수를 옮겼습니다
# 실행 결과 하나를 기록 한 줄로 만듭니다(모델 요청 수 = 실행 흔적 칸의 길이, 도구 메시지 수와 호출 ID 짝은 call_id_lists로 셈)
def run_row(question_name, result):
    ids = call_id_lists(result["messages"])
    row = {"질문": question_name}
    row["실행 흔적"] = result["trace"]
    row["모델 요청 수"] = len(result["trace"])
    row["도구 메시지 수"] = len(ids["호출 ID"])
    row["호출 ID 짝"] = ids["요청 id"] == ids["호출 ID"]
    return row
