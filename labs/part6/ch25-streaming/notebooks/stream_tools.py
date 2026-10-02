"""Ch 25 Streaming — 앞 챕터와 이 챕터 앞 절에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from stream_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
이 챕터 01·02·03절 노트북에서 처음 적은 함수 여섯과 Ch 21 도구 파일 runner_tools.py의 estimate_cost는
설명 주석과 본문을 글자 그대로 옮겼습니다.
앞 챕터 도구 파일(Ch 21 runner_tools.py·Ch 23 checkpoint_tools.py 등)은 이 챕터 실습 폴더에 없는
패키지(numpy·SQLite 체크포인터)를 가져와, 파일째 가져오지 않고 이 챕터 노트북이 쓰는 함수만 옮깁니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""
# 시각을 읽는 기능 묶음입니다(03절에서 옮긴 함수 collect_timed_events가 씁니다)
import time


# Ch 25 01절에서 배웠습니다 — 01절 노트북 4절의 같은 이름 함수를 옮겼습니다
# 그래프를 한 번 실행하며 받은 사건을 차례대로 목록에 모아 내놓습니다
def collect_events(graph_to_run, graph_input, config, modes):
    events = []
    # stream_mode에 목록을 주면, 사건 하나가 (모드 이름, 자료) 짝으로 나옵니다
    for event in graph_to_run.stream(graph_input, config, stream_mode=modes):
        events.append(event)
    return events


# Ch 25 01절에서 배웠습니다 — 01절 노트북 4절의 같은 이름 함수를 옮겼습니다
# 사건 목록에서 한 모드의 사건이 몇 번째(1부터 셈)에 나왔는지 목록으로 내놓습니다
def positions_of(events, mode):
    places = []
    for index in range(len(events)):
        # 사건 하나는 (모드 이름, 자료) 짝이라, [0]이 모드 이름입니다
        if events[index][0] == mode:
            places.append(index + 1)
    return places


# Ch 25 02절에서 배웠습니다 — 02절 노트북 4절의 같은 이름 함수를 옮겼습니다
# 사건 목록에서 같은 모드가 이어지면 한 번만 적어, 모드가 바뀐 차례를 목록으로 내놓습니다
def mode_order(events):
    order = []
    last_mode = ""
    for event in events:
        # 사건 하나는 (모드 이름, 자료) 짝이라, [0]이 모드 이름입니다
        mode = event[0]
        # 바로 앞 사건과 모드가 다를 때만 적습니다
        if mode != last_mode:
            order.append(mode)
        last_mode = mode
    return order


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


# Ch 25 03절에서 배웠습니다 — 03절 노트북 3절의 같은 이름 함수를 옮겼습니다
# 그래프를 한 번 실행하며, 사건을 꺼낼 때마다 그때의 시각을 적어 딕셔너리로 내놓습니다
def collect_timed_events(graph_to_run, graph_input, config, modes):
    # 메서드 stream을 부르기 직전의 시각을 시작 시각으로 적습니다
    timed_run = {"start": time.perf_counter(), "events": [], "times": []}
    for event in graph_to_run.stream(graph_input, config, stream_mode=modes):
        timed_run["events"].append(event)
        # 사건을 담은 바로 뒤에 시각을 적어, 두 목록의 자리를 맞춥니다
        timed_run["times"].append(time.perf_counter())
    timed_run["end"] = time.perf_counter()
    return timed_run


# Ch 25 03절에서 배웠습니다 — 03절 노트북 5절의 같은 이름 함수를 옮겼습니다
# 사건 목록에서 글자가 든 첫 스트림 청크가 몇 번째(1부터 셈) 사건인지 내놓습니다
def first_text_place(events):
    for index in range(len(events)):
        mode = events[index][0]
        data = events[index][1]
        # 모드 messages의 자료는 (스트림 청크, 칸 metadata) 짝이라, [0]이 스트림 청크입니다
        if mode == "messages" and data[0].text != "":
            return index + 1
    # 끝까지 찾지 못하면 None을 내놓습니다
    return None


# Ch 25 03절에서 배웠습니다 — 03절 노트북 7절의 같은 이름 함수를 옮겼습니다
# 시각을 적은 실행 기록(collect_timed_events의 결과)에서 세 시간(초)을 계산해 딕셔너리로 내놓습니다
def three_times(run_record):
    start_at = run_record["start"]
    # 5절 함수로 글자가 든 첫 스트림 청크의 자리를 찾습니다
    place = first_text_place(run_record["events"])
    text_at = run_record["times"][place - 1]
    seconds = {"첫 사건 시간": round(run_record["times"][0] - start_at, 3)}
    seconds["첫 토큰 도착 시간"] = round(text_at - start_at, 3)
    seconds["전체 걸린 시간"] = round(run_record["end"] - start_at, 3)
    return seconds
