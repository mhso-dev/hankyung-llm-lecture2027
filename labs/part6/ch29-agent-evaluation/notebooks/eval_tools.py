"""Ch 29 Agent 평가 — 앞 챕터와 이 챕터에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from eval_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
이 챕터 노트북이 실제로 쓰는 함수만 담고, 새 함수가 필요한 절이 그때 더합니다.
Ch 21 도구 파일 runner_tools.py에서 옮긴 함수는 설명 주석과 본문을 글자 그대로 옮겼습니다.
Ch 15 06절 노트북 셀에서 옮긴 함수(average·nearest_rank)도 그 셀의 주석과 본문을 글자 그대로 옮겼습니다.
이 챕터 앞 절 노트북에서 처음 적은 함수를 옮길 때는, 그 셀의 주석과 본문을 글자 그대로 옮깁니다.
앞 챕터 도구 파일은 이 챕터 실습 폴더에 없는 패키지(numpy 등)를 가져오거나 그 챕터 폴더에 묶여 있어,
파일째 가져오지 않습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
평가 함수를 만드는 줄(create_trajectory_match_evaluator 등)은 이 파일에 두지 않고 노트북에 둡니다.
"""
# 01절에서 옮긴 함수 make_trajectory가 만드는 메시지 클래스 셋(Ch 13 04절·Ch 19 05절)을 가져옵니다
from langchain.messages import AIMessage, HumanMessage, ToolMessage
# 04절에서 옮긴 함수 nearest_rank(Ch 15 06절)가 쓰는 올림 함수 math.ceil의 모듈을 가져옵니다
import math


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


# Ch 29 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 질문·도구 요청 목록·결과 글·답 글로, 질문에서 답까지의 메시지 목록(궤적)을 만들어 내놓습니다
def make_trajectory(question, calls, results, answer):
    messages = [HumanMessage(content=question)]
    # 도구 요청 하나마다, 그 요청을 담은 모델 응답과 같은 호출 ID의 도구 메시지를 한 쌍씩 붙입니다
    for call in calls:
        messages.append(AIMessage(content="", tool_calls=[call]))
        messages.append(ToolMessage(content=results[call["name"]], tool_call_id=call["id"]))
    # 마지막에는 도구를 요청하지 않는 모델 응답, 곧 최종 답을 붙입니다
    messages.append(AIMessage(content=answer))
    return messages


# Ch 29 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 궤적의 모델 응답마다 요청한 도구 이름을 차례대로 모아, 목록 하나로 내놓습니다
def called_tool_names(messages):
    names = []
    for message in messages:
        # 도구 호출 요청은 모델 응답(AIMessage)에만 있습니다
        if type(message).__name__ == "AIMessage":
            for name in tool_call_names(message):
                names.append(name)
    return names


# Ch 29 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 궤적 평가: 평가 함수로 실제 궤적을 기준 궤적과 견주고, 결과 딕셔너리의 칸 score만 꺼냅니다
def trajectory_pass(messages, reference, evaluator):
    result = evaluator(outputs=messages, reference_outputs=reference)
    return result["score"]


# Ch 29 02절에서 배웠습니다 — 02절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 한 궤적을 네 모드의 평가 함수로 모두 견줘, 모드 이름을 키로 한 점수 딕셔너리로 내놓습니다
def four_modes(messages, reference, evaluators):
    row = {}
    for mode in evaluators:
        # 01절 함수 trajectory_pass가 결과 딕셔너리에서 칸 score만 꺼냅니다
        row[mode] = trajectory_pass(messages, reference, evaluators[mode])
    return row


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


# Ch 15 06절에서 배웠습니다 — Ch 15 06절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 값 목록을 모두 더해 값의 수로 나눈 평균을 냅니다(여섯째 자리에서 반올림합니다)
def average(values):
    total = 0
    for value in values:
        total = total + value
    return round(total / len(values), 6)


# Ch 15 06절에서 배웠습니다 — Ch 15 06절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 값 목록을 작은 값부터 줄 세우고 가장 가까운 자리 방식으로 백분위수 하나를 찾습니다
def nearest_rank(values, percent):
    ordered = sorted(values)
    rank = math.ceil(percent * len(ordered) / 100)
    return ordered[rank - 1]


# Ch 29 04절에서 배웠습니다 — 04절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 공통 칸 딕셔너리 한 줄을 「|」로 이은 표 한 줄로 출력합니다(내놓는 값 없음)
def show_row(row):
    print(row["이름"], "|", row["요청 수"], "|", row["도구 요청 수"], "|", row["토큰 수"], "|", row["걸린 초"], "|", row["점수"])
