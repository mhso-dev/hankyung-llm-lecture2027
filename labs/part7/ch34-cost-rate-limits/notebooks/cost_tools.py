"""Ch 34 비용 · Rate Limit 엔지니어링 — 앞 챕터와 이 챕터 앞 절에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from cost_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
이 챕터 노트북이 실제로 쓰는 함수만 담고, 새 함수가 필요한 절이 그때 더합니다.
앞 챕터 도구 파일에서 옮긴 함수는 설명 주석과 본문을 글자 그대로 옮겼습니다.
앞 챕터 도구 파일은 그 챕터 실습 폴더에 묶여 있어, 파일째 가져오지 않습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""

import json
import math
import socket
import time


# Ch 6 06절에서 배웠습니다 — Ch 29 도구 파일 eval_tools.py의 같은 이름 함수를 옮겼습니다
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


# Ch 15 08절에서 배웠습니다 — Ch 15 08절 노트북 셀의 같은 이름 함수를 옮겼습니다
# 요청 이름표(custom_id)·요청 주소·본문 설정·요청 글로, 입력 파일 한 줄에 들어갈 요청 하나를 만듭니다(설명 줄만 이 챕터 말로 바꿨습니다)
def make_batch_line(custom_id, url, settings, prompt_text):
    body = settings.copy()
    body["messages"] = [{"role": "user", "content": prompt_text}]
    line = {"custom_id": custom_id, "method": "POST", "url": url, "body": body}
    return line


# Ch 15 08절에서 배웠습니다 — Ch 15 08절 노트북 셀의 같은 이름 함수를 옮겼습니다
# 요청 목록을 받아 요청 하나를 JSON 글 한 줄로 바꿔 파일에 차례로 씁니다(파일이 있으면 새 내용으로 바꿔 씁니다)
def write_jsonl(file_path, lines):
    with open(file_path, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(json.dumps(line, ensure_ascii=False) + "\n")


# Ch 15 08절에서 배웠습니다 — Ch 15 도구 파일 rag_tools.py의 같은 이름 함수를 옮겼습니다
# JSONL 파일을 읽어 빈 줄을 뺀 줄마다 JSON으로 읽고 딕셔너리 목록을 만듭니다
def read_jsonl(file_path):
    with open(file_path, encoding="utf-8") as file:
        text_lines = file.read().split("\n")
    rows = []
    for text_line in text_lines:
        if text_line != "":
            rows.append(json.loads(text_line))
    return rows


# Ch 15 08절에서 배웠습니다 — Ch 15 도구 파일 rag_tools.py의 같은 이름 함수를 옮겼습니다
# 첫째 목록에는 있고 둘째 목록에는 없는 이름을 첫째 목록 차례대로 모읍니다
def ids_not_in(first_ids, second_ids):
    missing = []
    for custom_id in first_ids:
        if custom_id not in second_ids:
            missing.append(custom_id)
    return missing


# Ch 28 03절에서 배웠습니다 — Ch 28 03절 노트북 셀의 같은 이름 함수를 옮겼습니다
# 서버가 포트를 열 때까지 짧게 쉬며 연결해 보고, 기한 안에 열렸는지를 True·False로 내놓습니다
def wait_for_port(port, limit_seconds):
    check_interval = 0.05
    deadline = time.perf_counter() + limit_seconds
    while time.perf_counter() < deadline:
        with socket.socket() as probe:
            if probe.connect_ex(("127.0.0.1", port)) == 0:
                return True
        time.sleep(check_interval)
    return False


# Ch 15 06절에서 배웠습니다 — Ch 29 도구 파일 eval_tools.py의 같은 이름 함수를 옮겼습니다
# 값 목록을 모두 더해 값의 수로 나눈 평균을 냅니다(여섯째 자리에서 반올림합니다)
def average(values):
    total = 0
    for value in values:
        total = total + value
    return round(total / len(values), 6)


# Ch 15 06절에서 배웠습니다 — Ch 29 도구 파일 eval_tools.py의 같은 이름 함수를 옮겼습니다
# 값 목록을 작은 값부터 줄 세우고 가장 가까운 자리 방식으로 백분위수 하나를 찾습니다
def nearest_rank(values, percent):
    ordered = sorted(values)
    rank = math.ceil(percent * len(ordered) / 100)
    return ordered[rank - 1]


# Ch 16 04절에서 배웠습니다 — Ch 16 04절 노트북 셀의 같은 이름 함수를 옮겼습니다
# 호출 한도와 비용 상한을 담은 예산 딕셔너리를 만듭니다
def make_budget(max_calls, max_cost_usd):
    if max_calls < 1:
        raise ValueError("호출 한도는 1 이상이어야 합니다.")
    if not math.isfinite(max_cost_usd) or max_cost_usd <= 0:
        raise ValueError("비용 상한은 끝이 있는 양수여야 합니다.")
    return {"max_calls": max_calls, "max_cost_usd": max_cost_usd, "calls": 0, "cost_usd": 0.0}


# Ch 16 04절에서 배웠습니다 — Ch 16 04절 노트북 셀의 같은 이름 함수를 옮겼습니다
# 모델을 부르기 전에 호출 한 번과 예상 비용을 예산에 예약합니다
def reserve(budget, estimated_cost_usd):
    if not math.isfinite(estimated_cost_usd) or estimated_cost_usd < 0:
        raise ValueError("예상 비용은 끝이 있는 0 이상 값이어야 합니다.")
    if budget["calls"] + 1 > budget["max_calls"]:
        raise ValueError("호출 한도를 넘습니다.")
    if budget["cost_usd"] + estimated_cost_usd > budget["max_cost_usd"]:
        raise ValueError("비용 상한을 넘습니다.")
    budget["calls"] = budget["calls"] + 1
    budget["cost_usd"] = budget["cost_usd"] + estimated_cost_usd


# Ch 34 01절에서 배웠습니다 — Ch 34 01절 노트북 셀의 같은 이름 함수를 옮겼습니다
# 실험 번호·앞 글·뒤 글을 줄바꿈으로 이어, 모델에 보낼 요청 글 하나를 만듭니다
def make_request(mark, first_text, second_text):
    # 실험 번호는 언제나 맨 앞에 두고, 정책 글과 문의 글의 차례만 인자로 정합니다
    request_text = mark + "\n" + first_text + "\n" + second_text
    return request_text


# Ch 34 01절에서 배웠습니다 — Ch 34 01절 노트북 셀의 같은 이름 함수를 옮겼습니다
# 사용량 하나의 예상 비용을 캐시 입력 할인을 넣은 값과 할인 없이 센 값으로 한 줄에 출력하고, 앞의 값을 내놓습니다
def cost_row(label, usage, prices):
    # 할인 없이 셀 때는 Ch 6 06절처럼, 캐시 입력 요금 자리에 입력 요금을 넣습니다
    with_discount = estimate_cost(usage, prices["ordinary_input"], prices["cached_input"], prices["output"])
    without_discount = estimate_cost(usage, prices["ordinary_input"], prices["ordinary_input"], prices["output"])
    print(label, "|", round(with_discount, 6), "|", round(without_discount, 6), "|", with_discount == without_discount)
    return with_discount


# Ch 34 03절에서 배웠습니다 — Ch 34 03절 노트북 셀의 같은 이름 함수를 옮겼습니다
# 문의 글의 글자 수를 기준 길이와 견주어, 보낼 모델의 이름을 고릅니다
def choose_model(inquiry, length_limit):
    # 이름을 먼저 nano로 두고, 기준 길이보다 긴 문의만 mini로 바꿉니다
    model_name = "gpt-5.4-nano"
    if len(inquiry) > length_limit:
        model_name = "gpt-5.4-mini"
    return model_name


# Ch 34 03절에서 배웠습니다 — Ch 34 03절 노트북 셀의 같은 이름 함수를 옮겼습니다
# 고른 이름으로 모델 객체를 찾아, 문의 글 뒤에 답 형식 글을 붙여 보내고 응답을 내놓습니다
def send_inquiry(inquiry, model_name, models, answer_rule):
    chosen_model = models[model_name]
    request_text = inquiry + " " + answer_rule
    response = chosen_model.invoke(request_text)
    return response


# Ch 34 05절에서 배웠습니다 — Ch 34 05절 노트북 셀의 같은 이름 함수를 옮겼습니다
# 입력·캐시 입력·출력 토큰 수로, 응답의 사용량(usage_metadata)과 같은 모양의 딕셔너리를 만듭니다
def make_usage(input_tokens, cached_tokens, output_tokens):
    details = {"cache_read": cached_tokens}
    usage = {"input_tokens": input_tokens, "output_tokens": output_tokens, "input_token_details": details}
    return usage


# Ch 34 05절에서 배웠습니다 — Ch 34 05절 노트북 셀의 같은 이름 함수를 옮겼습니다
# 대화당 비용 목록을 모두 더하고, 여섯째 자리에서 반올림한 합을 내놓습니다
def total_cost(values):
    total = 0
    for value in values:
        total = total + value
    return round(total, 6)


# Ch 34 05절에서 배웠습니다 — Ch 34 05절 노트북 셀의 같은 이름 함수를 옮겼습니다
# 예산에 예약 금액을 예약해 보고, 되면 「예약됨」을, 막히면 받은 ValueError의 글을 내놓습니다
def try_reserve(budget, amount):
    try:
        reserve(budget, amount)
    except ValueError as error:
        return str(error)
    return "예약됨"
