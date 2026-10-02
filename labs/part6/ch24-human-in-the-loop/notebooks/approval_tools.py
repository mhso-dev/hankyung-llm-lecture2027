"""Ch 24 Human-in-the-Loop와 Time Travel — 앞 챕터와 이 챕터 앞 절에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from approval_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
Ch 23 01·04·06절 노트북에서 처음 적은 함수 넷과 이 챕터 03절 노트북에서 처음 적은 함수 하나는 본문을 글자 그대로 옮겼습니다.
Ch 23 도구 파일 checkpoint_tools.py는 SQLite 체크포인터를 가져오는데, 이 챕터 실습 폴더에는 그 패키지가 없습니다.
그래서 파일째 가져오지 않고, 이 챕터 노트북이 쓰는 함수만 옮겼습니다.
read_record의 설명 주석은 Ch 23 04절 그대로라 「노드 이름」이라고 적혀 있고, 이 챕터에서는 주문 키를 읽습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""

import os


# Ch 23 04절에서 배웠습니다 — 04절 노트북 3절의 같은 이름 함수를 옮겼습니다
# 기록 파일을 읽어, 줄마다 적힌 노드 이름을 목록으로 내놓습니다
def read_record(record_name):
    with open(record_name, encoding="utf-8") as record_file:
        text = record_file.read()
    return text.split()


# Ch 23 06절에서 배웠습니다 — 06절 노트북 2절의 같은 이름 함수를 옮겼습니다
# 기록 파일 끝에 주문 키 한 줄을 덧붙이고, 한 일을 글 "적음"으로 내놓습니다
def append_key(record_name, order_key):
    # 여는 방식 "a"는 파일 끝에 이어 쓰고, 파일이 없으면 새로 만듭니다
    with open(record_name, "a", encoding="utf-8") as record_file:
        record_file.write(order_key + "\n")
    return "적음"


# Ch 23 06절에서 배웠습니다 — 06절 노트북 2절의 같은 이름 함수를 옮겼습니다
# 기록 파일에 같은 주문 키가 이미 있으면 건너뛰고, 없을 때만 한 줄을 덧붙입니다
def append_key_once(record_name, order_key):
    written_keys = []
    # 기록 파일이 있을 때만 읽습니다(처음 부를 때는 파일이 없습니다)
    if os.path.exists(record_name):
        with open(record_name, encoding="utf-8") as record_file:
            written_keys = record_file.read().split()
    if order_key in written_keys:
        return "건너뜀"
    return append_key(record_name, order_key)


# Ch 23 01절에서 배웠습니다 — 01절 노트북 8절의 같은 이름 함수를 옮겼습니다
# 체크포인트 목록을 받아, 하나마다 단계 번호·만든 자리·다음 노드·칸 값을 한 줄로 출력합니다(내놓는 값 없음)
def print_history(history):
    print("단계 번호 | 만든 자리 | 다음 노드 | 칸 값")
    for snapshot in history:
        step = snapshot.metadata["step"]
        source = snapshot.metadata["source"]
        print(step, "|", source, "|", snapshot.next, "|", snapshot.values)


# Ch 24 03절에서 배웠습니다 — 03절 노트북 4절의 같은 이름 함수를 옮겼습니다
# 체크포인트 목록을 최신 것부터 보며, 다음 노드에 node_name이 든 첫 체크포인트를 찾아 내놓습니다
def find_before(history, node_name):
    found = None
    for snapshot in history:
        # 속성 next는 다음에 실행할 노드 이름들의 튜플이고, in은 그 안에 이름이 있는지 봅니다
        if node_name in snapshot.next:
            found = snapshot
            # 처음 찾은 것에서 반복을 멈춥니다(하나도 없으면 None을 그대로 내놓습니다)
            break
    return found
