"""Ch 17 Agent 개요 — 이 챕터 앞 절과 앞 챕터에서 배운 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from agent_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""
import json
import time


# Ch 17 01절에서 배웠습니다 — 기록 하나를 줄마다 번호·단계·한 쪽·고른 쪽 차례로 출력합니다
def print_steps(steps):
    print("번호 | 단계 | 한 쪽 | 고른 쪽")
    for i in range(len(steps)):
        step = steps[i]
        print(i, "|", step["단계"], "|", step["한 쪽"], "|", step["고른 쪽"])


# Ch 17 01절에서 배웠습니다 — 기록에서 칸 key의 값이 value와 같은 줄 수를 셉니다
def count_steps(steps, key, value):
    count = 0
    for step in steps:
        if step[key] == value:
            count = count + 1
    return count


# Ch 17 01절에서 배웠습니다 — 모델이 고른 단계가 없으면 워크플로우, 하나라도 있으면 에이전트 후보로 가릅니다
def classify(steps):
    chosen = count_steps(steps, "고른 쪽", "모델")
    if chosen == 0:
        return "워크플로우"
    return "에이전트 후보"


# Ch 17 02절에서 배웠습니다 — 기록에서 도구가 한 단계의 이름만 차례대로 모읍니다
def tool_names(steps):
    names = []
    for step in steps:
        if step["한 쪽"] == "도구":
            names.append(step["단계"])
    return names


# Ch 17 03절에서 배웠습니다 — 도구 흉내: 도구 이름을 받아 03절에서 정해 둔 결과 글을 내놓습니다
def run_tool(tool_name):
    if tool_name == "주문 조회":
        return "주문 A-1024 · 무선 이어폰 · 배송 완료 · 받은 지 5일"
    if tool_name == "환불 규정 확인":
        return "받은 지 7일 안의 상품은 환불할 수 있음"
    if tool_name == "환불 요청 등록":
        return "환불 요청을 등록함"
    return "목록에 없는 도구"


# Ch 17 03절에서 배웠습니다 — 머리글 뒤에 문의와 지금까지 부른 도구의 결과를 이어 붙여 요청 글 하나를 만듭니다
def build_request(head, question, steps):
    text = head + "\n\n문의: " + question + "\n지금까지 부른 도구와 결과:"
    if count_steps(steps, "한 쪽", "도구") == 0:
        text = text + " 없음"
    for step in steps:
        if step["한 쪽"] == "도구":
            text = text + "\n- " + step["단계"] + ": " + step["결과"]
    return text


# Ch 17 03절에서 배웠습니다 — 모델이 고른 이름을 보고 멈출 까닭을 찾습니다(멈추지 않으면 빈 글)
def stop_reason(name, steps, confirm_tools):
    if name == "끝":
        return "모델이 끝을 고름"
    if name in confirm_tools:
        return "사람 확인"
    if count_steps(steps, "단계", name) > 0:
        return "같은 도구를 다시 고름"
    return ""


# Ch 17 03절에서 배웠습니다 — 멈춘 까닭을 기록 한 줄로 만듭니다: 끝은 모델이 고른 멈춤, 나머지는 코드가 정한 멈춤
def stop_line(reason):
    chooser = "코드"
    if reason == "모델이 끝을 고름":
        chooser = "모델"
    return {"단계": "멈춤", "한 쪽": "코드", "고른 쪽": chooser, "결과": reason}


# Ch 17 03절에서 배웠습니다 — 한 바퀴의 기록 줄을 만듭니다: 고른 줄 뒤에 멈춤 줄 또는 도구를 부른 줄
def turn_lines(name, reason):
    choose = {"단계": "다음 단계 고르기", "한 쪽": "모델", "고른 쪽": "코드", "결과": name}
    if reason != "":
        return [choose, stop_line(reason)]
    result = run_tool(name)
    tool_step = {"단계": name, "한 쪽": "도구", "고른 쪽": "모델", "결과": result}
    return [choose, tool_step]


# Ch 17 03절에서 배웠습니다 — 기록을 줄마다 번호·단계·한 쪽·고른 쪽·결과 차례로 출력합니다
def print_results(steps):
    print("번호 | 단계 | 한 쪽 | 고른 쪽 | 결과")
    for i in range(len(steps)):
        step = steps[i]
        print(i, "|", step["단계"], "|", step["한 쪽"], "|", step["고른 쪽"], "|", step["결과"])


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


# Ch 17 04절에서 배웠습니다 — 요청 글 하나를 모델에 보내고 받은 글·걸린 초·입력 토큰·출력 토큰을 딕셔너리로 내놓습니다(모델 요청 1번)
def send_and_measure(chat_model, request_text):
    start_time = time.perf_counter()
    reply = chat_model.invoke(request_text)
    seconds = round(time.perf_counter() - start_time, 3)
    usage = reply.usage_metadata
    measure = {"받은 글": reply.text, "걸린 초": seconds}
    measure["입력 토큰"] = usage["input_tokens"]
    measure["출력 토큰"] = usage["output_tokens"]
    return measure


# Ch 17 04절에서 배웠습니다 — 03절 ask_next처럼 다음 행동을 묻고, 잰 값 셋을 더한 「다음 단계 고르기」 줄을 내놓습니다(모델 요청 1번)
def choose_line(chat_model, head, question, steps):
    request_text = build_request(head, question, steps)
    measure = send_and_measure(chat_model, request_text)
    choice = json.loads(measure["받은 글"])
    line = {"단계": "다음 단계 고르기", "한 쪽": "모델", "고른 쪽": "코드", "결과": choice["다음"]}
    line["입력 토큰"] = measure["입력 토큰"]
    line["출력 토큰"] = measure["출력 토큰"]
    line["걸린 초"] = measure["걸린 초"]
    return line


# Ch 17 04절에서 배웠습니다 — 루프: 03절 run_loop와 같은 차례로 돌되, 고른 줄은 잰 값이 든 줄로 씁니다
def run_measured_loop(chat_model, head, question, confirm_tools, turn_limit):
    steps = []
    for turn in range(turn_limit):
        choose = choose_line(chat_model, head, question, steps)
        reason = stop_reason(choose["결과"], steps, confirm_tools)
        steps = steps + [choose] + turn_lines(choose["결과"], reason)[1:]
        if reason != "":
            return steps
    return steps + [stop_line("바퀴 한도")]


# Ch 17 04절에서 배웠습니다 — 기록에서 모델이 한 줄만 골라 바퀴마다 고른 이름과 잰 값 셋을 출력합니다
def print_measures(steps):
    print("바퀴 | 고른 이름 | 입력 토큰 | 출력 토큰 | 걸린 초")
    turn = 0
    for step in steps:
        if step["한 쪽"] == "모델":
            turn = turn + 1
            print(turn, "|", step["결과"], "|", step["입력 토큰"], "|", step["출력 토큰"], "|", step["걸린 초"])


# Ch 17 04절에서 배웠습니다 — 기록에서 모델이 한 줄의 칸 key 값을 모두 더합니다(토큰 수를 합칠 때 씁니다)
def total_of(steps, key):
    total = 0
    for step in steps:
        if step["한 쪽"] == "모델":
            total = total + step[key]
    return total
