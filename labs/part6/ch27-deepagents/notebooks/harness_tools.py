"""Ch 27 DeepAgents — 앞 챕터와 이 챕터에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from harness_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
이 챕터 노트북이 실제로 쓰는 함수만 담고, 새 함수가 필요한 절이 그때 더합니다.
Ch 21 도구 파일 runner_tools.py에서 옮긴 함수는 설명 주석과 본문을 글자 그대로 옮겼습니다.
Ch 16 도구 파일 guardrails.py에서 옮긴 find_source_marks는 몸통 첫 줄 주석까지 글자 그대로 옮겼습니다.
이 챕터 01절·07절 노트북에서 옮긴 함수는 그 셀의 주석과 본문을 글자 그대로 옮겼습니다.
앞 챕터 도구 파일은 이 챕터 실습 폴더에 없는 패키지(numpy 등)를 가져오거나 그 챕터 폴더에 묶여 있어,
파일째 가져오지 않습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
도구를 만드는 @tool 줄과 에이전트를 만드는 create_deep_agent 줄은 이 파일에 두지 않고 노트북에 둡니다.
"""


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


# Ch 27 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 에이전트 그래프의 도구 실행 노드에서 도구 이름을 모아, 알파벳 차례로 내놓습니다
def tool_names(agent):
    tool_node = agent.nodes["tools"].bound
    # 도구 찾기 표 tools_by_name(Ch 20 01절)의 키가 도구 이름입니다
    names = list(tool_node.tools_by_name)
    names.sort()
    return names


# Ch 27 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 둘째 목록에만 있는 이름을 차례대로 모아 내놓습니다
def names_only_in(base, other):
    found = []
    for name in other:
        if name not in base:
            found.append(name)
    return found


# Ch 16 01절에서 배웠습니다 — Ch 16 도구 파일 guardrails.py의 같은 이름 함수를 몸통 첫 줄 주석까지 글자 그대로 옮겼습니다
# 답 글에서 대괄호로 묶은 출처 표시를 모두 뽑아, 대괄호까지 붙은 글의 목록으로 내놓습니다
def find_source_marks(answer):
    # Ch 16 01절에서 배웠습니다 — 답에서 대괄호로 묶은 출처 표시를 모두 뽑습니다
    marks = []
    pieces = answer.split("[")
    for piece in pieces[1:]:
        if "]" in piece:
            inside = piece.split("]")[0]
            marks.append("[" + inside + "]")
    return marks


# Ch 27 07절에서 배웠습니다 — 07절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 답 글의 출처 표시마다 대괄호를 뺀 파일 위치가 known 안에 있는지 판정해, 한 줄씩 모아 내놓습니다
def check_citations(answer, known):
    rows = []
    for mark in find_source_marks(answer):
        # 첫 글자와 마지막 글자(대괄호 둘)를 뺀 글이 인용한 파일 위치입니다
        cited = mark[1:-1]
        rows.append({"인용": cited, "있는가": cited in known})
    return rows


# Ch 27 07절에서 배웠습니다 — 07절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다
# 메시지 목록의 응답에서, 이름이 tool_name인 도구 요청마다 인자 arg_name의 값을 차례로 모아 내놓습니다
def call_args(messages, tool_name, arg_name):
    values = []
    for message in messages:
        if type(message).__name__ == "AIMessage":
            for call in message.tool_calls:
                if call["name"] == tool_name:
                    values.append(call["args"][arg_name])
    return values
