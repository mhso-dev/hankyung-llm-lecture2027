"""Ch 26 위임 구조 — 앞 챕터와 이 챕터 앞 절에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from delegation_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
이 챕터 노트북이 실제로 쓰는 함수만 담고, 새 함수가 필요한 절이 그때 더합니다.
Ch 21 도구 파일 runner_tools.py에서 옮긴 함수는 설명 주석과 본문을 글자 그대로 옮겼습니다.
앞 챕터 도구 파일은 이 챕터 실습 폴더에 없는 패키지(numpy 등)를 가져오거나 그 챕터 폴더에 묶여 있어,
파일째 가져오지 않습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
도구를 만드는 @tool 줄과 에이전트를 만드는 create_agent 줄은 이 파일에 두지 않고 노트북에 둡니다.
"""
# 03절 함수 send_to_desks가 만드는 객체 Send(Ch 13 05절)를 가져옵니다
from langgraph.types import Send


# Ch 19 04절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다
# 모델 응답 하나에서 도구 호출 목록의 도구 이름만 모아 목록으로 내놓습니다(도구를 고르지 않았으면 빈 목록)
def tool_call_names(response):
    names = []
    for call in response.tool_calls:
        names.append(call["name"])
    return names


# Ch 19 06절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다
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


# Ch 19 05절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다
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


# Ch 6 06절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다
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


# Ch 26 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 메시지 목록에서 종류 이름만 차례대로 모아 목록으로 내놓습니다
def message_kinds(messages):
    kinds = []
    for message in messages:
        kinds.append(type(message).__name__)
    return kinds


# Ch 26 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 이번 실행이 더한 바깥 메시지와 안쪽 목록 여럿의 요청 수·토큰을 모두 더해 내놓습니다
def usage_with_specialists(new_messages, inner_runs):
    total = sum_usage(new_messages)
    for inner_list in inner_runs:
        inner_usage = sum_usage(inner_list)
        # 요청 수·입력 토큰·출력 토큰 세 키를 차례로 더합니다
        for key in total:
            total[key] = total[key] + inner_usage[key]
    return total


# Ch 26 02절에서 배웠습니다 — 02절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 메시지 목록에서 응답(AIMessage)마다, 그 응답을 쓴 에이전트 이름(칸 name)을 모아 내놓습니다
def writer_names(messages):
    names = []
    for message in messages:
        if type(message).__name__ == "AIMessage":
            names.append(message.name)
    return names


# Ch 26 03절에서 배웠습니다 — 03절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 분류 노드 뒤에 둘 조건 함수입니다. 분야 칸의 이름마다 Send 하나를 만들어 목록으로 내놓습니다
def send_to_desks(state):
    sends = []
    for desk in state["desks"]:
        # Send의 첫 자리는 갈 노드 이름, 둘째 자리는 그 실행에만 넘길 갈래별 상태입니다(Ch 13 05절)
        branch = {"desk": desk, "question": state["question"]}
        sends.append(Send(desk, branch))
    return sends


# Ch 26 04절에서 배웠습니다 — 04절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 기록 목록의 안쪽 목록마다 마지막 응답을 쓴 담당 이름을 보고, 분야 이름 차례로 모아 내놓습니다
def answered_desks(inner_runs, names):
    desks = []
    for desk in names:
        for inner_list in inner_runs:
            if inner_list[-1].name == desk:
                desks.append(desk)
    return desks


# Ch 26 04절에서 배웠습니다 — 04절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 완료 조건 함수입니다. 필요한 분야가 모두 모인 분야에 들어 있고 마지막 답도 있으면 True를 내놓습니다
def is_complete(collected, needed, has_final):
    for desk in needed:
        if desk not in collected:
            return False
    return has_final
