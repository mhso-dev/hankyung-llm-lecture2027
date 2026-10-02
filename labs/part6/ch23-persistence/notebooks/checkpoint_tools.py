"""Ch 23 Persistence와 Durable Execution — 앞 절에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from checkpoint_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
04절 노트북 3절과 6절에서 처음 적은 함수 일곱(강제 종료 함수와 앞머리 글 함수)은 본문을 글자 그대로 옮겼습니다.
06절 노트북에서 처음 적은 함수 셋도 본문을 글자 그대로 옮겼습니다(07절은 그 가운데 append_key와 append_key_once를 가져옵니다).
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
스크립트 자리·파일 이름·쓰기 방식처럼 절마다 다른 값도 인자로 넘깁니다.
"""

import os
import sqlite3
import subprocess
import sys
import time

from langgraph.checkpoint.sqlite import SqliteSaver


# Ch 23 04절에서 배웠습니다 — 04절 노트북 3절의 같은 이름 함수를 옮겼습니다
# 스크립트를 자식 프로세스로 띄우고, 끝나기를 기다리지 않고 그 프로세스 객체를 내놓습니다
def start_worker(worker_path, files, mode, phase):
    # 명령 목록: 지금 커널의 Python · 스크립트 자리 · 스크립트가 받을 글 다섯
    command = [sys.executable, worker_path, files["sqlite"], files["signal"], files["record"], mode, phase]
    process = subprocess.Popen(command)
    return process


# Ch 23 04절에서 배웠습니다 — 04절 노트북 3절의 같은 이름 함수를 옮겼습니다
# 신호 파일이 생길 때까지 짧게 쉬며 보고, 기한 안에 생겼는지를 True·False로 내놓습니다
def wait_for_signal(signal_name, limit_seconds):
    check_interval = 0.05
    deadline = time.perf_counter() + limit_seconds
    while time.perf_counter() < deadline:
        if os.path.exists(signal_name):
            return True
        time.sleep(check_interval)
    return False


# Ch 23 04절에서 배웠습니다 — 04절 노트북 3절의 같은 이름 함수를 옮겼습니다
# 자식 프로세스를 강제로 끝내고, 끝날 때까지 기다려 종료 코드를 내놓습니다
def stop_worker(process):
    process.kill()
    # 5초 안에 끝나지 않으면 오류가 납니다
    return_code = process.wait(timeout=5)
    return return_code


# Ch 23 04절에서 배웠습니다 — 04절 노트북 3절의 같은 이름 함수를 옮겼습니다
# 새 연결로 SQLite 파일을 열어 한 스레드의 칸 값·다음 노드·체크포인트 수를 읽고, 연결을 닫습니다
def read_saved(graph_builder, sqlite_name, thread_name):
    connection = sqlite3.connect(sqlite_name, check_same_thread=False)
    saver = SqliteSaver(connection)
    reader = graph_builder.compile(checkpointer=saver)
    config = {"configurable": {"thread_id": thread_name}}
    saved = reader.get_state(config)
    history = list(reader.get_state_history(config))
    connection.close()
    return {"칸 값": saved.values, "다음 노드": saved.next, "체크포인트 수": len(history)}


# Ch 23 04절에서 배웠습니다 — 04절 노트북 3절의 같은 이름 함수를 옮겼습니다
# 기록 파일을 읽어, 줄마다 적힌 노드 이름을 목록으로 내놓습니다
def read_record(record_name):
    with open(record_name, encoding="utf-8") as record_file:
        text = record_file.read()
    return text.split()


# Ch 23 04절에서 배웠습니다 — 04절 노트북 3절의 같은 이름 함수를 옮겼습니다
# 작업 폴더에서 아직 쓰지 않은 앞머리 글(이름 뒤에 번호)을 골라 내놓습니다
def new_prefix(name):
    number = 1
    # 같은 앞머리의 SQLite 파일이 이미 있으면, 번호를 하나 올려 다시 봅니다
    while os.path.exists(name + "-" + str(number) + ".sqlite"):
        number = number + 1
    return name + "-" + str(number)


# Ch 23 04절에서 배웠습니다 — 04절 노트북 6절의 같은 이름 함수를 옮겼습니다
# 스크립트를 띄워 둘째 노드에서 강제로 끝내고, 끊긴 뒤 파일에 남은 것을 읽어 내놓습니다
def kill_at_second(worker_path, graph_builder, name_prefix, mode):
    files = {"sqlite": name_prefix + ".sqlite", "signal": name_prefix + ".signal",
             "record": name_prefix + ".record"}
    process = start_worker(worker_path, files, mode, "first-run")
    signal_limit = 20
    arrived = wait_for_signal(files["signal"], signal_limit)
    # 신호를 기다린 결과와 상관없이 먼저 끊어, 자식 프로세스가 남지 않게 합니다
    stop_worker(process)
    assert arrived, "기한 안에 신호 파일이 생기지 않았습니다"
    return read_saved(graph_builder, files["sqlite"], mode)


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


# Ch 23 06절에서 배웠습니다 — 06절 노트북 6절의 같은 이름 함수를 옮겼습니다
# 스크립트를 둘째 노드에서 끊은 뒤 새 자식 프로세스로 다시 실행하고, 결제 기록 파일의 키 목록을 내놓습니다
def kill_then_resume(worker_path, graph_builder, name_prefix, strategy):
    kill_at_second(worker_path, graph_builder, name_prefix, strategy)
    files = {"sqlite": name_prefix + ".sqlite", "signal": name_prefix + ".signal",
             "record": name_prefix + ".record"}
    again = start_worker(worker_path, files, strategy, "resume")
    resume_limit = 30
    again.wait(timeout=resume_limit)
    return read_record(files["record"])
