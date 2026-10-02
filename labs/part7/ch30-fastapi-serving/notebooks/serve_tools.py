"""Ch 30 FastAPI로 Agent 서빙 — 앞 챕터와 이 챕터 앞 절에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from serve_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
이 챕터 노트북이 실제로 쓰는 함수만 담고, 새 함수가 필요한 절이 그때 더합니다.
Ch 25 도구 파일 stream_tools.py에서 옮긴 함수는 설명 주석과 본문을 글자 그대로 옮겼습니다.
이 챕터 02·04·05·06·07절 노트북에서 처음 적은 함수 열은 그 셀의 주석과 본문을 글자 그대로 옮겼습니다.
앞 챕터 도구 파일은 그 챕터 실습 폴더에 묶여 있어, 파일째 가져오지 않습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
실습 앱 파일(agent_service/)은 이 챕터가 가르치는 코드라 이 파일과 따로 둡니다.
"""

import json


# Ch 25 01절에서 배웠습니다 — Ch 25 도구 파일 stream_tools.py의 같은 이름 함수를 옮겼습니다
# 사건 목록에서 한 모드의 사건이 몇 번째(1부터 셈)에 나왔는지 목록으로 내놓습니다
def positions_of(events, mode):
    places = []
    for index in range(len(events)):
        # 사건 하나는 (모드 이름, 자료) 짝이라, [0]이 모드 이름입니다
        if events[index][0] == mode:
            places.append(index + 1)
    return places


# Ch 25 02절에서 배웠습니다 — Ch 25 도구 파일 stream_tools.py의 같은 이름 함수를 옮겼습니다
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


# Ch 30 02절에서 배웠습니다 — 02절 노트북의 같은 이름 함수를 옮겼습니다
# 시험용으로, 시간 제한 0초를 내놓는 함수를 정의합니다
async def zero_timeout():
    return 0.0


# Ch 30 04절에서 배웠습니다 — 04절 노트북의 같은 이름 함수를 옮겼습니다
# 진행 값 목록을 받아, 칸 token의 글을 차례대로 이어 붙인 글을 내놓습니다
def join_tokens(stream_values):
    joined = ""
    for value in stream_values:
        joined = joined + value["token"]
    return joined


# Ch 30 05절에서 배웠습니다 — 05절 노트북의 같은 이름 함수를 옮겼습니다
# 본문 글을 빈 줄로 나눠, 빈 글을 뺀 SSE 사건 글의 목록을 내놓습니다
def split_sse(body_text):
    found = []
    # SSE 사건 하나는 빈 줄로 끝나므로, 줄바꿈 두 개가 사건 사이의 경계입니다
    for part in body_text.split("\n\n"):
        if part != "":
            found.append(part)
    return found


# Ch 30 05절에서 배웠습니다 — 05절 노트북의 같은 이름 함수를 옮겼습니다
# SSE 사건 글 하나를 받아, 줄마다 칸 이름과 값으로 나눈 딕셔너리를 내놓습니다
def parse_sse(sse_text):
    fields = {}
    for line in sse_text.split("\n"):
        # split의 둘째 인자 1은 처음 나온 자리에서 한 번만 나눈다는 뜻입니다
        name_and_value = line.split(": ", 1)
        fields[name_and_value[0]] = name_and_value[1]
    return fields


# Ch 30 06절에서 배웠습니다 — 06절 노트북의 같은 이름 함수를 옮겼습니다
# 응답 본문 글을 SSE 사건으로 나누고, 사건마다 칸 딕셔너리로 바꾼 목록을 내놓습니다
def read_events(body_text):
    events = []
    for sse_text in split_sse(body_text):
        events.append(parse_sse(sse_text))
    return events


# Ch 30 06절에서 배웠습니다 — 06절 노트북의 같은 이름 함수를 옮겼습니다
# 칸 딕셔너리 목록에서, 사건마다 칸 event의 사건 이름을 모은 목록을 내놓습니다
def event_names(events):
    names = []
    for fields in events:
        names.append(fields["event"])
    return names


# Ch 30 06절에서 배웠습니다 — 06절 노트북의 같은 이름 함수를 옮겼습니다
# 칸 딕셔너리 목록에서 token 사건만 골라, 칸 data의 JSON 글을 읽은 값의 목록을 내놓습니다
def token_values(events):
    values = []
    for fields in events:
        if fields["event"] == "token":
            values.append(json.loads(fields["data"]))
    return values


# Ch 30 06절에서 배웠습니다 — 06절 노트북의 같은 이름 함수를 옮겼습니다
# After 판정: 칸 딕셔너리 목록에서 마지막 사건의 이름이 done인지 봅니다
def ended_with_done(events):
    # 사건이 하나도 없으면 끝까지 받지 못한 것으로 셉니다
    if len(events) == 0:
        return False
    last_fields = events[-1]
    return last_fields["event"] == "done"


# Ch 30 06절에서 배웠습니다 — 06절 노트북의 같은 이름 함수를 옮겼습니다
# 칸 딕셔너리 목록에서, 칸 id가 있는 마지막 사건의 번호를 내놓습니다(하나도 없으면 None)
def last_event_id(events):
    found = None
    for fields in events:
        # 번호가 없는 사건(done 등)은 건너뛰어, 앞에서 본 번호를 그대로 둡니다
        if "id" in fields:
            found = fields["id"]
    return found


# Ch 30 07절에서 배웠습니다 — 07절 노트북의 같은 이름 함수를 옮겼습니다
# 응답 머리에서 이름이 name인 칸의 값을 내놓습니다(그런 칸이 없으면 None)
def header_or_none(response, name):
    if name in response.headers:
        return response.headers[name]
    return None
