"""Ch 23 07절(챕터 끝 실습 절) 생성기 (QUALITY-UPGRADE.md §7-2·§2·§2-7·§3·§4·§6).

사용:
  python3 author_07.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_07.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
새로 만든 절이라 qa/upgrade/before/ 에 원본이 없다. **experiment 형식**(chapter.json), lesson_part 없음.

## 결정 1 — 붙인 앞 절 기능 셋 (인계 「§06 → 실습(07)」 6항)

03절 SQLite 체크포인터(임시 폴더의 파일 · 스레드 이름 = 이용자 번호 · 연결을 닫고 새 연결·새 그래프로 이어 가기)
+ 05절 실패 흉내(failure_plan · call_count · TimeoutError 같은 글)와 원인을 없앤 뒤 invoke(None, config)
+ 06절 append_key_once(멱등 키 = 대출 키 loan-2307, 도구 파일에서 가져옴).
멱등 키 확인이 흐름 안에서 실제로 일하려면(Ch 20 05 검토 B-8 — 붙이기만 한 부품 없음) 기록을 적은 노드가 다시 실행되어야 한다.
자식 프로세스를 쓰지 않고 한 커널 안에서 그렇게 되는 길은 「기록을 적은 노드 안의 실패 흉내」뿐이라, 노드 record_loan이
기록 파일에 적은 뒤 실패 흉내를 낸다(06 b7이 노트북 밖에서만 확인했다고 적은 판 B를 노트북에서 실행 — 새 API 0).
04절 read_saved·read_record는 결과를 읽는 데만 쓴다.
실행 1 = 쓰기 방식 idempotent, 실행 2 = 쓰기 방식 하나만 naive(06절 비교와 같은 값 — b2에 「새로 볼 것」 한 문장).
뺀 것: 02 PostgreSQL(서버) · 04 저장 시점 비교·강제 종료(04·06 되풀이, 자식 프로세스) · 05 같은 단계 두 노드·남은 쓰기(이번 흐름에 없음)
· 03 메시지 칸(대화 아님) · 01 InMemorySaver(새 연결로 다시 열 파일이 필요).

## 결정 2 — 결론은 코드로 정해지는 값

부른 횟수 · 다음 노드 · 체크포인트 수 · 칸 notes · 기록 파일의 키와 같은 키 줄 수 · 작업 폴더 파일 이름.
assert는 같은 키 줄 수(우리 코드가 정함)에만. 걸린 시간은 재지 않는다. 노트북 밖 준비 확인(/tmp/ch23-07/probe, 규칙 먼저) 10/10 같음.

## 결정 3 — 도구 파일 (§2-7)

쓰는 앞 절 함수 넷(append_key·append_key_once·read_record·read_saved)은 모두 06절이 만든 도구 파일에 이미 있어 바꾸지 않는다.
노트북 전역 이름(call_count·failure_plan·write_plan)에 기대는 노드 둘과 상태 형식은 노트북에 적는다(06절 모양, 이름만 바꿈 — check_same_as_before()가 대조).

## 모델 요청

0번(챕터 리드 결정 1 — 이 챕터는 모델을 부르지 않는다). 규격 §7-2의 실습 절 3~5번과 다름 → b3 한 문장·진단·강사 확인.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·
튜플 풀기·세미콜론·`isinstance`·별표 풀기·데코레이터·클래스(상태 형식 말고)·`with`(open 밖)·`durability`·`subprocess`·
`interrupt`·`stream`·모델.
"""
from __future__ import annotations

import ast
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nbkit import RUN_DATE, code, install_source, md, setup, write_notebook  # noqa: E402
import author_01  # noqa: E402
import author_03  # noqa: E402
import author_04  # noqa: E402
import author_05  # noqa: E402
import author_06  # noqa: E402
from author_01 import html_text, table_html  # noqa: E402

LAB = ROOT / "labs/part6/ch23-persistence/notebooks"
TOOLS_PATH = LAB / "checkpoint_tools.py"
FIGS = ROOT / "textbook/part6/ch23-persistence/figures"
SLUG = "07-Persistence-실습"
TITLE_TEXT = "Persistence 실습: 멈춘 대출 처리를 이어 가고 기록은 한 번만 남기기"
SRC = ROOT / "textbook/part6/ch23-persistence/_src" / (SLUG + ".html")
# 교재 출력을 만든 실행의 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답)에서 읽은 값
RUNSEC = os.environ.get("AUTHOR07_RUNSEC", "5초 안에")
RUNS_SENTENCE = os.environ.get("AUTHOR07_RUNS_SENTENCE", "새 커널로 두 번 실행했을 때 코드 셀 22개의 출력이 모두 같았습니다.")
# 도구 파일 해시(이 절은 도구 파일을 바꾸지 않는다 — check_same_as_before()가 확인). 마감(2026-09-25)에 04절 new_prefix가 더해진 판
TOOLS_SHA256 = "a850b2cdccbd8ff6f3dd8364e5ab58a8f2845eb6c8607ef7250315c5eee26b37"  # 06절 판 71280dd9… → 마감 판(new_prefix 더함)

INSTALL = install_source(["langgraph==1.2.11", "langgraph-checkpoint-sqlite==3.0.3"])

IMPORTS = r'''# 그래프 이름(Ch 13 01·02절)과 SQLite 체크포인터(03절)를 가져오고, 04·06절에서 배운 함수 다섯을 도구 파일에서 가져옵니다
import operator
import sqlite3
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from checkpoint_tools import append_key, append_key_once, new_prefix, read_record, read_saved

print("도구 파일에서 가져온 함수:", "append_key, append_key_once, new_prefix, read_record, read_saved")'''

# 01절 임시 폴더 셀에서 앞머리만 바꾼 셀(아래 assert)
FOLDER = author_01.FOLDER.replace("ch23-01-", "ch23-07-")

TASK = r'''# 오늘 처리할 대출 신청 한 건의 값 둘을 정합니다(실행 전에 정한 값)
member_id = "M-0317"
loan_key = "loan-2307"
print("이용자 번호:", member_id)
print("이용자 번호 출처: Ch 21 03절 실행 정보의 이용자 번호 그대로")
print("대출 키:", loan_key)
print("대출 키 출처: 이 절에서 실행 전에 정한 값(06절 주문 키 order-2306과 같은 모양)")'''

PLAN = r'''# 노드마다 부른 횟수, 실패 흉내, 쓰기 방식과 파일 앞머리를 정할 딕셔너리 셋을 만듭니다(05절 모양)
call_count = {"receive_request": 0, "record_loan": 0}
failure_plan = {"fail": True}
# 실행 1의 쓰기 방식은 이미 적힌 키를 건너뛰는 idempotent입니다
write_plan = {"mode": "idempotent"}
# 파일 앞머리는 쓰기 방식 이름에 번호를 붙여 고릅니다(04절 함수 — 이 셀을 다시 실행하면 새 번호)
write_plan["prefix"] = new_prefix(write_plan["mode"])
print("부른 횟수:", call_count)
print("실패 흉내:", failure_plan)
print("쓰기 방식:", write_plan)'''

STATE_BODY = '''class LoanState(TypedDict):
    loan_key: str
    notes: Annotated[list[str], operator.add]'''

STATE = "# 대출 키 칸과, 노드가 한 일을 이어 붙이는 칸을 둔 상태 형식을 만듭니다(06절 OrderState와 같은 모양)\n" + STATE_BODY

NODE_RECEIVE = r'''# 첫째 노드: 부른 횟수에 1을 더하고, 한 일 "신청 받음"을 목록에 담아 냅니다
def receive_request(state):
    call_count["receive_request"] = call_count["receive_request"] + 1
    return {"notes": ["신청 받음"]}'''

FAIL_LINE = 'raise TimeoutError("이 절에서 만든 실패 흉내입니다.")'

NODE_RECORD = r'''# 둘째 노드: 쓰기 방식대로 대출 키를 기록 파일에 적은 뒤, 실패 흉내가 켜져 있으면 알림을 보내다 멈춥니다
def record_loan(state):
    call_count["record_loan"] = call_count["record_loan"] + 1
    record_name = write_plan["prefix"] + ".record"
    if write_plan["mode"] == "idempotent":
        note = append_key_once(record_name, state["loan_key"])
    else:
        note = append_key(record_name, state["loan_key"])
    # 알림은 실제로 보내지 않고, 시간 초과처럼 멈추는 실패 흉내만 냅니다
    if failure_plan["fail"]:
        ''' + FAIL_LINE + r'''
    return {"notes": [note]}'''

BUILDER = r'''# 노드 둘을 START → receive_request → record_loan → END로 잇는 설계 객체를 만듭니다
builder = StateGraph(LoanState)
builder.add_node("receive_request", receive_request)
builder.add_node("record_loan", record_loan)
builder.add_edge(START, "receive_request")
builder.add_edge("receive_request", "record_loan")
builder.add_edge("record_loan", END)
print("등록한 노드:", list(builder.nodes))'''

R1_OPEN = r'''# 실행 1의 SQLite 파일(앞머리 + .sqlite)에 연결을 열고, SQLite 체크포인터를 붙여 설계 객체를 컴파일합니다(03절 모양)
one_prefix = write_plan["prefix"]
one_conn = sqlite3.connect(one_prefix + ".sqlite", check_same_thread=False)
one_saver = SqliteSaver(one_conn)
one_graph = builder.compile(checkpointer=one_saver)
# 스레드 이름은 이용자 번호이고, 이 설정 딕셔너리를 두 실행에 함께 씁니다
config = {"configurable": {"thread_id": member_id}}
print("SQLite 파일 이름:", one_prefix + ".sqlite")
print("붙은 체크포인터의 종류:", type(one_graph.checkpointer).__name__)
print("스레드 이름:", config["configurable"]["thread_id"])'''

R1_FAIL = r'''# 대출 신청을 입력으로 넣어 실행하고, 둘째 노드가 낸 실패 흉내를 받아 출력합니다(저장 시점은 기본값)
loan_request = {"loan_key": loan_key, "notes": []}
try:
    one_graph.invoke(loan_request, config)
except TimeoutError as error:
    print("오류 종류:", type(error).__name__)
    print("오류 메시지:", error)
print("부른 횟수:", call_count)'''

R1_READ = r'''# 멈춘 뒤 파일에 남은 체크포인트와, 대출 기록 파일에 적힌 키를 읽습니다(04절 함수 둘 — 도구 파일)
one_saved = read_saved(builder, one_prefix + ".sqlite", member_id)
print("남은 칸 값:", one_saved["칸 값"])
print("다음 노드:", one_saved["다음 노드"])
print("체크포인트 수:", one_saved["체크포인트 수"])
one_before = read_record(one_prefix + ".record")
print("멈추기 전에 적힌 키:", one_before)'''

R1_REOPEN = r'''# 첫 연결을 닫고, 같은 파일에 새 연결·새 체크포인터·새 그래프를 만들어 스레드를 읽습니다(03절 모양)
one_conn.close()
one_conn_again = sqlite3.connect(one_prefix + ".sqlite", check_same_thread=False)
one_saver_again = SqliteSaver(one_conn_again)
one_graph_again = builder.compile(checkpointer=one_saver_again)
reopened = one_graph_again.get_state(config)
print("새 그래프가 읽은 다음 노드:", reopened.next)
print("새 그래프가 읽은 칸 notes:", reopened.values["notes"])'''

R1_RESUME = r'''# 실패 흉내를 끄고, 새 그래프로 새 입력 없이(None) 같은 스레드를 이어 갑니다(05절처럼)
failure_plan["fail"] = False
one_result = one_graph_again.invoke(None, config)
print("칸 notes:", one_result["notes"])
print("부른 횟수:", call_count)'''

R1_AFTER = r'''# 이어 간 뒤 남은 체크포인트와, 대출 기록 파일에 같은 키가 적힌 줄 수를 봅니다
one_after = read_saved(builder, one_prefix + ".sqlite", member_id)
print("다음 노드:", one_after["다음 노드"])
print("체크포인트 수:", one_after["체크포인트 수"])
one_keys = read_record(one_prefix + ".record")
one_count = one_keys.count(loan_key)
print("대출 기록 파일의 키:", one_keys)
print("같은 키가 적힌 줄 수:", one_count)
# 우리 코드가 정하는 값이라 실행마다 같아야 합니다
assert one_count == 1, "쓰기 방식 idempotent는 같은 키를 한 줄만 남겨야 합니다"'''

R2_SET = r'''# 실행 2 · 바꿀 값: 쓰기 방식 하나만 naive로 바꾸고, 부른 횟수와 실패 흉내는 처음 값으로 다시 맞춥니다
write_plan["mode"] = "naive"
# 파일 앞머리는 실행 1처럼 쓰기 방식 이름을 따라 새로 고릅니다
write_plan["prefix"] = new_prefix(write_plan["mode"])
call_count["receive_request"] = 0
call_count["record_loan"] = 0
failure_plan["fail"] = True
print("쓰기 방식:", write_plan)
print("부른 횟수:", call_count)
print("실패 흉내:", failure_plan)'''

R2_FAIL = r'''# 실행 2의 SQLite 파일에 연결을 열어 컴파일하고, 같은 대출 신청으로 실행해 실패 흉내를 받아 출력합니다
two_prefix = write_plan["prefix"]
two_conn = sqlite3.connect(two_prefix + ".sqlite", check_same_thread=False)
two_saver = SqliteSaver(two_conn)
two_graph = builder.compile(checkpointer=two_saver)
try:
    two_graph.invoke(loan_request, config)
except TimeoutError as error:
    print("오류 종류:", type(error).__name__)
print("부른 횟수:", call_count)'''

R2_READ = r'''# 멈춘 뒤 실행 2의 SQLite 파일에 남은 체크포인트와, 대출 기록 파일에 적힌 키를 읽습니다
two_saved = read_saved(builder, two_prefix + ".sqlite", member_id)
print("다음 노드:", two_saved["다음 노드"])
print("체크포인트 수:", two_saved["체크포인트 수"])
two_before = read_record(two_prefix + ".record")
print("멈추기 전에 적힌 키:", two_before)'''

R2_RESUME = r'''# 연결을 닫고 새 연결·새 그래프를 만든 뒤, 실패 흉내를 끄고 새 입력 없이(None) 이어 갑니다
two_conn.close()
two_conn_again = sqlite3.connect(two_prefix + ".sqlite", check_same_thread=False)
two_saver_again = SqliteSaver(two_conn_again)
two_graph_again = builder.compile(checkpointer=two_saver_again)
failure_plan["fail"] = False
two_result = two_graph_again.invoke(None, config)
print("칸 notes:", two_result["notes"])
print("부른 횟수:", call_count)'''

R2_AFTER = r'''# 이어 간 뒤 남은 체크포인트와, 대출 기록 파일에 같은 키가 적힌 줄 수를 봅니다
two_after = read_saved(builder, two_prefix + ".sqlite", member_id)
print("다음 노드:", two_after["다음 노드"])
print("체크포인트 수:", two_after["체크포인트 수"])
two_keys = read_record(two_prefix + ".record")
two_count = two_keys.count(loan_key)
print("대출 기록 파일의 키:", two_keys)
print("같은 키가 적힌 줄 수:", two_count)
# 우리 코드가 정하는 값이라 실행마다 같아야 합니다
assert two_count == 2, "쓰기 방식 naive는 같은 키를 두 줄 남겨야 합니다"'''

COMPARE = r'''# 두 실행이 파일에 남긴 것을 파일 앞머리마다 한 줄씩 견줍니다(파일을 새 연결로 다시 읽음)
print("파일 앞머리 | 칸 notes | 체크포인트 수 | 같은 키가 적힌 줄 수")
for name_prefix in [one_prefix, two_prefix]:
    saved = read_saved(builder, name_prefix + ".sqlite", member_id)
    keys = read_record(name_prefix + ".record")
    print(name_prefix, "|", saved["칸 값"]["notes"], "|", saved["체크포인트 수"], "|", keys.count(loan_key))'''

FILES_END = r'''# 남은 연결 둘을 닫고, 작업 폴더에 남은 파일을 이름 차례로 봅니다
one_conn_again.close()
two_conn_again.close()
file_names = sorted(os.listdir())
print("현재 작업 폴더의 파일:", file_names)'''

FIG1 = "07-1-세-절-기능을-붙인-대출-처리-그래프"
FIG1_ALT = os.environ.get("AUTHOR07_FIG1_ALT", "위에서 아래로 읽는 그림입니다. 맨 위에 초록 상자 쓰기 방식 write_plan 실행 1 idempotent 실행 2 naive, 파란 상자 05절 실패 흉내 failure_plan TimeoutError, 파란 상자 06절 append_key_once 도구 파일이 나란히 있고, 세 상자에서 화살표가 파란 상자 노드 record_loan 대출 키를 적은 뒤 알림에서 멈출 수 있음으로 모입니다. 노드 record_loan 오른쪽에는 초록 상자 대출 신청 한 건 스레드 M-0317 대출 키 loan-2307과 회색 상자 03절 SqliteSaver SQLite 파일이 있습니다. 노드 record_loan, invoke 화살표가 붙은 대출 신청, SqliteSaver에서 화살표 셋이 맨 아래 회색 상자 SQLite 체크포인터를 붙인 그래프 노드 receive_request 노드 record_loan으로 모이는 그림")
FIG1_CAP = "05절 실패 흉내와 06절 함수는 노드 record_loan 안에서 쓰고, 03절 SQLite 체크포인터는 그래프에 붙였습니다."
FIG1_READ = """위에서 아래로 읽습니다.
파란 상자는 우리가 적은 코드이고, 회색 상자는 라이브러리가 준 체크포인터와 그것을 붙인 그래프입니다.
05절 실패 흉내와 06절 함수는 노드 `record_loan` 안에서 씁니다.
노드와 대출 신청과 체크포인터에서 온 화살표 셋이 맨 아래 그래프로 모입니다.
초록 상자 둘 가운데 쓰기 방식이 실행 2에서 바꾸는 값이고, 대출 신청은 두 실행에 같게 넣습니다."""

FIG2 = "07-2-실행-1의-실제-차례"
FIG2_ALT = os.environ.get("AUTHOR07_FIG2_ALT", "위에서 아래로 상자 일곱이 한 줄로 이어진 흐름도입니다. 첫 파란 상자는 invoke 대출 신청 스레드 M-0317 receive_request 마침, 둘째 파란 상자는 record_loan 대출 키를 적은 뒤 실패 흉내로 멈춤입니다. 셋째 노란 상자는 받은 오류 TimeoutError 부른 횟수 두 노드 한 번씩, 넷째 노란 상자는 파일에 남은 것 다음 노드 record_loan 체크포인트 셋 기록 파일 키 한 줄입니다. 다섯째 파란 상자는 연결을 닫고 새 연결 새 그래프 실패 흉내를 끄고 invoke None, 여섯째 파란 상자는 record_loan을 처음부터 다시 실행 키를 찾아 건너뜀입니다. 일곱째 노란 상자는 이어 간 뒤 receive_request 한 번 record_loan 두 번 칸 notes 신청 받음 건너뜀 체크포인트 넷 기록 파일 키 한 줄인 그림")
FIG2_CAP = "실행 1에서 record_loan은 대출 키를 적은 뒤 멈췄고, 새 그래프로 이어 갈 때 처음부터 다시 실행되어 키를 건너뛰었습니다."
FIG2_READ = """위에서 아래로 한 줄로 읽습니다.
파란 상자는 우리가 부른 코드와 노드가 한 일이고, 노란 상자는 노트북 5절 출력입니다.
셋째·넷째 상자가 멈춘 뒤 남은 것이고, 다섯째 상자에서 새 연결로 파일을 다시 엽니다.
맨 아래 상자에서 `record_loan`은 두 번 불렸지만, 기록 파일의 키는 넷째 상자와 같은 한 줄입니다."""

FIG3 = "07-3-쓰기-방식만-바꾼-두-실행"
FIG3_ALT = os.environ.get("AUTHOR07_FIG3_ALT", "맨 위 초록 상자 바꾼 값 하나 쓰기 방식 실행 1 idempotent 실행 2 naive에서 아래 칸 둘로 화살표가 갑니다. 왼쪽 칸 실행 1 idempotent에는 파란 상자 다시 실행한 record_loan append_key_once가 키를 찾아 건너뜀에서 노란 상자 기록 파일에 같은 키 한 줄 칸 notes 신청 받음 건너뜀으로 화살표가 갑니다. 오른쪽 칸 실행 2 naive에는 파란 상자 다시 실행한 record_loan append_key가 검사 없이 한 줄 더에서 노란 상자 기록 파일에 같은 키 두 줄 칸 notes 신청 받음 적음으로 화살표가 갑니다. 맨 아래 회색 상자에 두 실행 같음 멈춘 뒤 다음 노드 record_loan 체크포인트 셋 이어 간 뒤 체크포인트 넷 receive_request 한 번 record_loan 두 번이 적힌 그림")
FIG3_CAP = "쓰기 방식만 바꾸자 기록 파일의 같은 키 줄 수가 한 줄에서 두 줄로 바뀌었고, 멈춘 자리와 부른 횟수는 같았습니다."
FIG3_READ = """맨 위 초록 상자는 두 실행에서 바꾼 값 하나입니다.
왼쪽 칸이 실행 1, 오른쪽 칸이 실행 2이고, 칸 안은 위에서 아래로 다시 실행한 `record_loan`이 한 일과 그 결과입니다.
노란 상자는 노트북 5·6절 출력이고, 맨 아래 회색 상자는 두 실행 출력에서 모두 확인한 공통점입니다.
두 칸끼리는 화살표로 잇지 않았습니다."""

ILLU = "07-4-리본으로-이은-사진과-기보"
ILLU_ALT = os.environ.get("AUTHOR07_ILLU_ALT", "흰 바탕에 나무 탁자 하나를 조금 위에서 본 그림입니다. 탁자 위쪽에 체스판 하나가 있고, 말들은 대부분 서 있지만 판 가운데의 흰 나이트 하나는 옆으로 누워 있습니다. 판 앞 탁자 위 왼쪽에는 작은 체스판이 찍힌 즉석사진 한 장이, 오른쪽에는 검은 나이트 그림 하나가 그려진 흰 종이 한 장이 있습니다. 빨간 리본 하나가 판 앞 가장자리에서 탁자 앞 끝까지 사진과 종이 사이로 이어지고, 두 물건 사이에 나비매듭이 있습니다. 글자·숫자·사람·카메라는 없는 그림")
ILLU_CAP = os.environ.get("AUTHOR07_ILLU_CAP", "판 위의 말 하나가 쓰러졌고, 판 앞에는 판을 찍은 사진 한 장과 표시 하나가 적힌 기보 한 장이 리본으로 판과 이어져 있습니다.")
ILLU_READ = os.environ.get("AUTHOR07_ILLU_READ", "나무 탁자 위쪽에 체스판 하나가 있고, 판 가운데의 흰 나이트 하나만 옆으로 누워 있습니다. 판 앞 왼쪽에는 작은 체스판이 찍힌 즉석사진 한 장, 오른쪽에는 검은 나이트 그림 하나가 그려진 흰 종이 한 장이 있습니다. 빨간 리본 하나가 판 앞 가장자리에서 두 물건 사이를 지나 탁자 끝까지 이어지고, 두 물건 사이에 매듭이 있습니다. 누운 나이트가 멈춘 노드 <code>record_loan</code>, 사진이 SQLite 파일에 남은 마지막 체크포인트, 종이가 대출 기록 파일입니다. 종이의 나이트 그림 하나가 대출 키 한 줄이고, 판 위 말의 개수·색과 판의 칸 수는 무엇과도 짝짓지 않습니다.")

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. 대출 신청 한 건을 처리하는 그래프에 SQLite 체크포인터와 멱등 키 확인을 붙입니다.
2. 대출 기록을 적은 노드를 실패 흉내로 멈추고, 새 연결로 파일을 다시 열어 이어 갑니다.
3. 쓰기 방식 하나만 바꿔 다시 실행하고, 대출 기록 파일의 줄 수로 두 실행을 견줍니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
01절처럼 매번 같은 값을 내는 우리 노드로, 저장된 값이 맞는지 출력으로 가릅니다.

실패는 모두 이 절에서 일부러 만든 실패 흉내입니다.
대출 기록은 실제 서비스가 아니라, 기록 파일에 대출 키를 한 줄 적는 것으로 대신합니다.
자식 프로세스는 띄우지 않고, 모든 일을 이 커널 안에서 합니다.

노트북은 빈 임시 폴더를 만들어 그 폴더에서 실행합니다.
SQLite 파일과 대출 기록 파일은 이 임시 폴더에 생기고, 실습 폴더에는 파일을 남기지 않습니다.
읽어 오는 자료 파일은 없습니다.

걸린 시간은 재지 않습니다.
교재 출력을 만든 실행에서는 노트북 전체가 """ + RUNSEC + """ 끝났습니다.
설치 셀에 걸리는 시간은 네트워크에 따라 달라집니다.

**기준 버전** — 첫 셀에서 패키지 둘을 설치합니다.
그래프는 langgraph 1.2.11입니다.
SQLite 체크포인터는 langgraph-checkpoint-sqlite 3.0.3에 들어 있습니다.

교재 출력은 Linux의 Python 3.12.13과, 그 Python에 들어 있는 SQLite 3.53.1로 만들었습니다.
Windows·macOS에서는 실행하지 않았습니다.

**실습 범위** — 이 절은 챕터 끝 실습 절이고 30분 안에 끝나는 분량입니다.
강사와 함께 첫 셀부터 차례로 실행하고, 따로 내는 과제는 없습니다.
01~06절에서 쓴 이름과 Ch 2에서 배운 문법만 씁니다.

실습 폴더 `labs/part6/ch23-persistence`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이번 절은 이 챕터의 실습입니다.
03절 SQLite 체크포인터, 05절 실패 흉내와 이어 가기, 06절 멱등 키 확인을 대출 처리 한 건에 모읍니다.
첫 셀은 패키지 둘을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langgraph: 1.2.11`과 `langgraph-checkpoint-sqlite: 3.0.3`이 보입니다.
두 판 모두 실습 폴더 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
상태 형식과 그래프 이름은 Ch 13 01·02절, `sqlite3`와 `SqliteSaver`는 03절과 같습니다.
마지막 줄은 04절과 06절에서 배운 함수 다섯을 도구 파일 `checkpoint_tools.py`에서 가져옵니다.
이 절에서 새로 가져오는 이름은 없습니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: append_key, append_key_once, new_prefix, read_record, read_saved`가 보입니다.
함수 `read_saved`·`read_record`·`new_prefix`는 04절 노트북 3절에서 처음 적은 함수입니다.
함수 `append_key`와 `append_key_once`는 06절 노트북 2절에서 처음 적은 함수입니다.
이 절에서 도구 파일에 더한 함수는 없습니다.

앞에서 배운 함수는 `checkpoint_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
그래서 임시 폴더로 작업 위치를 옮기기 전에 가져왔습니다.

교재 출력은 프로젝트 맨 위에서 커널을 띄운 실행입니다.
실행 도구가 도구 파일 폴더를 따로 알려 주어, 그 자리에서도 가져오기가 되었습니다.

다음 셀은 01절처럼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다.
이 절의 SQLite 파일과 대출 기록 파일은 모두 이 임시 폴더에 생깁니다."""),
        setup(FOLDER),
        md("""**결과 읽기** — 출력 줄 `임시 폴더 이름에 ch23-07-이 들어 있는가: True`로, 이 절의 폴더를 만들었습니다.
출력 줄 `현재 작업 폴더의 파일: []`로, 빈 폴더에서 시작합니다.

## 2. 오늘 처리할 대출 한 건

이번 실습은 자료실 창구에 들어온 대출 신청 한 건을 처리합니다.
처리는 노드 둘로 나눕니다.
첫째 노드는 신청을 받고, 둘째 노드는 대출 기록 파일에 대출 키를 적은 뒤 이용자에게 알림을 보냅니다.
알림은 실제로 보내지 않고, 보내다가 시간이 초과되는 실패 흉내만 냅니다.

다음 셀은 오늘 쓸 두 값을 정하고 출처와 함께 출력합니다.
두 값 모두 실행 전에 정했습니다."""),
        code(TASK),
        md("""**결과 읽기** — 출력 줄 `이용자 번호: M-0317`과 `대출 키: loan-2307`로 오늘 쓸 값을 확인합니다.
이용자 번호는 스레드 이름으로 씁니다.
01절에서 본 대로, 스레드 이름은 설정 딕셔너리의 `thread_id`에 적습니다.

대출 키는 06절의 주문 키처럼 멱등 키로 씁니다.
같은 대출이면 다시 실행해도 늘 같은 값이어야 합니다.
두 실행 모두 같은 이용자 번호와 같은 대출 키를 씁니다.

## 3. 재료 · 딕셔너리 셋과 상태 형식, 노드 둘

다음 셀은 05절처럼 노드마다 부른 횟수를 셀 딕셔너리와, 실패 흉내를 정할 딕셔너리를 만듭니다.
05절의 `failure_plan`에서 기다릴 초는 뺐습니다.
이번 그래프에는 같은 단계에서 함께 실행되는 노드가 없기 때문입니다.
셋째 딕셔너리 `write_plan`은 대출 기록을 적는 쓰기 방식과, 파일 이름의 앞머리를 정합니다.

앞머리는 04절 함수 `new_prefix`로, 쓰기 방식 이름 뒤에 번호를 붙여 고릅니다.
이 셀을 다시 실행하면 번호가 올라, 앞 실행의 파일과 섞이지 않는 새 파일을 씁니다.
그래서 실행 1을 처음부터 다시 보려면 이 셀부터, 실행 2는 6절 첫 셀부터 차례로 다시 실행합니다."""),
        code(PLAN),
        md("""**결과 읽기** — 출력 줄 `부른 횟수: {'receive_request': 0, 'record_loan': 0}`과 `실패 흉내: {'fail': True}`입니다.
출력 줄 `쓰기 방식: {'mode': 'idempotent', 'prefix': 'idempotent-1'}`가 실행 1의 설정입니다.
실행 2에서는 쓰기 방식 하나만 바꾸고, 앞머리는 그 이름을 따라 새로 고릅니다.
값 `idempotent`는 06절 `append_key_once`로, 값 `naive`는 `append_key`로 적는다는 뜻입니다.
세 딕셔너리는 체크포인트 밖에 있고, 노드가 노트북에서 만든 이름 그대로 읽고 고칩니다.

다음 셀은 상태 형식입니다.
칸 `loan_key`에 대출 키를, 칸 `notes`에 노드가 한 일을 담습니다.
06절 `OrderState`와 모양은 같고, 칸 이름이 달라 새 이름 `LoanState`를 붙입니다."""),
        code(STATE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 `notes`에는 Ch 13 02절의 이어 붙이기 규칙을 적었습니다.

다음 셀은 첫째 노드 `receive_request`입니다.
부른 횟수에 1을 더하고, 한 일 `신청 받음`을 칸 `notes`에 냅니다."""),
        code(NODE_RECEIVE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 둘째 노드 `record_loan`입니다.
쓰기 방식대로 대출 기록 파일에 대출 키를 적고, 실패 흉내가 켜져 있으면 `TimeoutError`를 냅니다.
오류 메시지는 05절 실패 흉내와 같은 글입니다.
기록 파일 이름은 `write_plan`에 담은 앞머리 뒤에 끝말을 붙여, 두 실행의 기록이 섞이지 않게 합니다."""),
        code(NODE_RECORD),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
기록 파일에 적는 줄이 실패 흉내보다 앞에 있습니다.
그래서 실패 흉내로 멈추면, 칸에 낼 글은 없어도 기록 파일에는 이미 한 줄이 적혀 있습니다.

다음 셀은 두 노드를 차례로 잇는 설계 객체를 만듭니다.
06절 설계 객체와 같은 모양이고, 상태 형식과 노드 이름만 다릅니다."""),
        code(BUILDER),
        md("""**결과 읽기** — 출력 줄 `등록한 노드: ['receive_request', 'record_loan']`입니다.
설계 객체 `builder`는 두 실행에 함께 씁니다.

## 4. 결과를 볼 기록 장치

결과는 04절 함수 둘로 봅니다.
함수 `read_saved`는 새 연결로 SQLite 파일을 열어, 한 스레드의 칸 값·다음 노드·체크포인트 수를 읽습니다.
읽은 뒤에는 연결을 닫습니다.
함수 `read_record`는 기록 파일의 줄을 목록으로 내놓습니다.

## 5. 실행 1 · 멈춘 처리를 새 연결에서 이어 가기

다음 셀은 03절처럼 실행 1의 SQLite 파일에 연결을 열고, SQLite 체크포인터를 붙여 컴파일합니다.
파일 이름은 3절에서 고른 앞머리 뒤에 끝말 `.sqlite`를 붙인 이름입니다.
스레드 이름은 이용자 번호이고, 설정 딕셔너리는 두 실행에 함께 씁니다."""),
        code(R1_OPEN),
        md("""**결과 읽기** — 출력 줄 `SQLite 파일 이름: idempotent-1.sqlite`·`붙은 체크포인터의 종류: SqliteSaver`·`스레드 이름: M-0317`입니다.

다음 셀은 대출 신청을 입력으로 넣어 실행하고, 실패 흉내를 받아 출력합니다.
저장 시점은 적지 않아, 04절에서 본 기본값으로 실행됩니다.
실행 전에 예상해 봅니다.
첫째 노드는 끝나고, 둘째 노드는 기록을 적은 뒤 멈출 것입니다."""),
        code(R1_FAIL),
        md("""**결과 읽기** — 출력 줄 `오류 종류: TimeoutError`와 `오류 메시지: 이 절에서 만든 실패 흉내입니다.`가 받은 오류입니다.
출력 줄 `부른 횟수: {'receive_request': 1, 'record_loan': 1}`로, 두 노드가 한 번씩 불렸습니다.
오류는 셀이 받아 출력해, 노트북은 멈추지 않았습니다.

다음 셀은 04절 함수 `read_saved`로 파일에 남은 체크포인트를 읽고, `read_record`로 기록 파일을 읽습니다.
실행 전에 예상해 봅니다.
다음 노드는 `record_loan`이고, 기록 파일에는 키가 이미 한 줄 있을 것입니다."""),
        code(R1_READ),
        md("""**결과 읽기** — 출력 줄 `다음 노드: ('record_loan',)`와 `체크포인트 수: 3`입니다.
출력 줄 `남은 칸 값: {'loan_key': 'loan-2307', 'notes': ['신청 받음']}`에는 첫째 노드가 낸 글만 있습니다.
출력 줄 `멈추기 전에 적힌 키: ['loan-2307']`로, 기록 파일에는 이미 한 줄이 있습니다.
체크포인트에는 기록을 마친 흔적이 없는데, 바깥 파일에는 기록이 남았습니다.

06절에서 강제 종료로 본 어긋남이, 실패 흉내로 멈출 때도 생겼습니다.
체크포인트 수 3은 06절에서 둘째 노드 안에서 끊긴 뒤의 수와 같습니다.

다음 셀은 03절처럼 첫 연결을 닫고, 같은 파일에 새 연결·새 체크포인터·새 그래프를 만듭니다.
창구 프로그램을 닫았다가 다시 연 것과 같습니다.
새 그래프가 파일에서 읽은 다음 노드와 칸 `notes`도 출력합니다."""),
        code(R1_REOPEN),
        md("""**결과 읽기** — 출력 줄 `새 그래프가 읽은 다음 노드: ('record_loan',)`입니다.
첫 연결과 첫 그래프는 더 쓰지 않지만, 새 그래프가 파일에서 멈춘 자리를 읽었습니다.
출력 줄 `새 그래프가 읽은 칸 notes: ['신청 받음']`도 앞 셀과 같습니다.

다음 셀은 실패 원인을 없애고, 05절처럼 새 입력 없이(`None`) 같은 스레드를 이어 갑니다.
이어 가는 그래프는 방금 만든 새 그래프입니다.
실행 전에 예상해 봅니다.
첫째 노드는 다시 불리지 않고, 둘째 노드 `record_loan`은 처음부터 다시 실행될 것입니다.
다시 실행된 `record_loan`은 기록 파일에서 키를 찾아, 쓰지 않고 건너뛸 것입니다."""),
        code(R1_RESUME),
        md("""**결과 읽기** — 출력 줄 `부른 횟수: {'receive_request': 1, 'record_loan': 2}`입니다.
이어 가는 동안 `record_loan`만 한 번 더 불렸고, 첫째 노드는 다시 불리지 않았습니다.
출력 줄 `칸 notes: ['신청 받음', '건너뜀']`의 `건너뜀`은 다시 실행된 `record_loan`이 낸 글입니다.
멈춘 첫 실행이 낼 글 `적음`은 칸에 없습니다.
노드가 끝나지 못해, 그 노드가 칸에 낼 갱신이 저장되지 않았기 때문입니다.

다음 셀은 이어 간 뒤의 체크포인트와 대출 기록 파일을 봅니다.
실행 전에 예상해 봅니다.
기록 파일에는 키가 한 줄만 있을 것입니다."""),
        code(R1_AFTER),
        md("""**결과 읽기** — 출력 줄 `다음 노드: ()`와 `체크포인트 수: 4`로, 이 스레드의 처리가 끝났습니다.
출력 줄 `같은 키가 적힌 줄 수: 1`입니다.
노드 `record_loan`은 두 번 실행되었지만, 대출 기록에는 한 번 실행한 것과 같은 한 줄만 남았습니다.

이 실행에서 세 절의 기능이 모두 쓰였습니다.
멈춘 자리는 03절처럼 SQLite 파일에 남아, 새 연결로 연 그래프도 읽었습니다.
05절처럼 원인을 없앤 뒤 `None`으로 이어 갔습니다.
다시 실행된 노드의 되풀이는 06절 멱등 키 확인이 막았습니다.

## 6. 실행 2 · 쓰기 방식만 바꾸기

실행 2에서는 쓰기 방식 하나만 `naive`로 바꿉니다.
06절에서는 자식 프로세스를 강제로 끝내, 노드를 다시 실행하게 했습니다.
이번에는 같은 커널 안의 실패 흉내로 멈춘 뒤 새 연결로 이어 갈 때도, 같은 차이가 나는지 봅니다.
다음 셀은 쓰기 방식을 바꾸고, 부른 횟수와 실패 흉내를 처음 값으로 다시 맞춥니다.
파일 앞머리는 실행 1처럼 쓰기 방식 이름을 따라 새로 고릅니다."""),
        code(R2_SET),
        md("""**결과 읽기** — 출력 줄 `쓰기 방식: {'mode': 'naive', 'prefix': 'naive-1'}`가 실행 2의 설정입니다.
출력 줄 `부른 횟수: {'receive_request': 0, 'record_loan': 0}`과 `실패 흉내: {'fail': True}`는 실행 1을 시작할 때와 같습니다.

다음 셀은 새 앞머리 `naive-1`의 SQLite 파일에 연결을 열어 컴파일하고, 같은 대출 신청으로 실행합니다.
스레드 이름은 실행 1과 같은 `M-0317`이지만, 파일이 달라 실행 1의 체크포인트와 섞이지 않습니다.
03절 8절에서 파일 이름만 바꾸면, 스레드 이름이 같아도 빈 딕셔너리를 읽은 것과 같습니다.
실행 전에 예상해 봅니다.
실행 1처럼 둘째 노드가 기록을 적은 뒤 멈출 것입니다."""),
        code(R2_FAIL),
        md("""**결과 읽기** — 출력 줄 `오류 종류: TimeoutError`와 `부른 횟수: {'receive_request': 1, 'record_loan': 1}`은 실행 1과 같습니다.

다음 셀은 멈춘 뒤 파일에 남은 체크포인트와 대출 기록 파일을 읽습니다."""),
        code(R2_READ),
        md("""**결과 읽기** — 출력 줄 `다음 노드: ('record_loan',)`와 `체크포인트 수: 3`은 실행 1과 같습니다.
출력 줄 `멈추기 전에 적힌 키: ['loan-2307']`도 같습니다.
체크포인트 수 3으로, 이 파일의 스레드는 빈 상태에서 시작했습니다.

다음 셀은 실행 1처럼 연결을 닫고 새 연결·새 그래프를 만든 뒤, 실패 흉내를 끄고 이어 갑니다.
실행 전에 예상해 봅니다.
다시 실행된 `record_loan`이 검사 없이 같은 키를 한 줄 더 적을 것입니다."""),
        code(R2_RESUME),
        md("""**결과 읽기** — 출력 줄 `부른 횟수: {'receive_request': 1, 'record_loan': 2}`는 실행 1과 같습니다.
출력 줄 `칸 notes: ['신청 받음', '적음']`의 `적음`은 다시 실행된 `record_loan`이 한 줄을 더 적었다는 뜻입니다.

다음 셀은 이어 간 뒤의 체크포인트와 대출 기록 파일을 봅니다."""),
        code(R2_AFTER),
        md("""**결과 읽기** — 출력 줄 `같은 키가 적힌 줄 수: 2`입니다.
대출은 한 건인데, 대출 기록에 같은 키가 두 줄 남았습니다.
출력 줄 `다음 노드: ()`와 `체크포인트 수: 4`는 실행 1과 같습니다.
체크포인트로 보면 두 실행은 같은 자리에서 멈추고, 같은 자리에서 끝났습니다.
달라진 것은 바깥 파일의 줄 수입니다.

## 7. 두 실행 견주기

다음 셀은 두 실행의 파일을 앞머리마다 새 연결로 다시 읽어, 한 줄씩 견줍니다."""),
        code(COMPARE),
        md("""**결과 읽기** — 라벨 줄 아래 두 줄은 `idempotent-1 | ['신청 받음', '건너뜀'] | 4 | 1`과 `naive-1 | ['신청 받음', '적음'] | 4 | 2`입니다.
두 실행에서 다른 것은 칸 `notes`의 마지막 글과, 기록 파일의 줄 수입니다.
체크포인트 수와, 이어 갈 때 부른 횟수는 같았습니다.

다음 셀은 남은 연결을 닫고, 작업 폴더의 파일을 봅니다."""),
        code(FILES_END),
        md("""**결과 읽기** — 출력 줄 `현재 작업 폴더의 파일: ['idempotent-1.record', 'idempotent-1.sqlite', 'naive-1.record', 'naive-1.sqlite']`입니다.
연결을 모두 닫아, SQLite 옆 파일(`-wal`·`-shm`)은 남지 않았습니다.
파일은 모두 임시 폴더에 있어, 실습 폴더에는 남지 않습니다.

## 정리

1. 대출 기록을 적은 노드가 실패 흉내로 멈추자, 체크포인트에는 그 노드의 갱신이 없고 기록 파일에는 한 줄이 남았습니다.
2. 새 연결로 연 그래프가 `None`으로 이어 가자, 첫째 노드는 두고 멈춘 노드만 처음부터 다시 실행했습니다.
3. 쓰기 방식 `idempotent`는 대출 기록을 한 줄, `naive`는 같은 키를 두 줄 남겼습니다.

이 절로 Ch 23이 끝납니다.
Ch 24 01절에서는 되돌리기 어려운 일을 하기 전에, 사람이 확인하는 자리에서 그래프를 멈추는 방법을 다룹니다."""),
    ]


L_01 = "01-체크포인터와-스레드.html"
L_02 = "02-PostgresSaver-준비와-스키마.html"
L_03 = "03-스레드-재개와-대화-이어가기.html"
L_04 = "04-내구-실행-모드-비교.html"
L_05 = "05-pending-writes와-장애-복구.html"
L_06 = "06-노드-재시작과-멱등성.html"
L_CH13_02 = "../../part4/ch13-langgraph-basics/02-State-갱신.html"
L_CH21_03 = "../ch21-create-agent/03-AgentState와-context-schema.html"
L_CH24_01 = "../ch24-human-in-the-loop/01-interrupt-승인-게이트.html"
STYLE = "<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>"


def link(url: str, label: str) -> str:
    return '<a href="' + url + '">' + label + "</a>"


def c(value: str) -> str:
    return "<code>" + value + "</code>"


LEARNED_TABLE = table_html(["절", "배운 것", "실습에서 쓰는 곳"], [
    (link(L_01, "01절"), "체크포인터·체크포인트·스레드, 설정 딕셔너리의 " + c("thread_id") + ", 같은 스레드로 다시 부를 때의 규칙",
     "이용자 번호를 스레드 이름으로 쓴 설정 딕셔너리"),
    (link(L_03, "03절"), "SQLite 체크포인터(" + c("SqliteSaver") + "), 연결을 닫고 새 연결·새 그래프로 같은 스레드 이어 가기",
     "파일 " + c("idempotent-1.sqlite") + "·" + c("naive-1.sqlite") + ", 멈춘 뒤 새 연결로 다시 연 그래프"),
    (link(L_04, "04절"), "함수 " + c("read_saved") + "·" + c("read_record") + "·" + c("new_prefix") + "(도구 파일), 저장 시점의 기본값",
     "파일에 남은 칸 값·다음 노드·체크포인트 수, 대출 기록 파일의 키, 실행마다 새 파일 앞머리"),
    (link(L_05, "05절"), "실패 흉내(" + c("TimeoutError") + "·" + c("failure_plan") + ")와 부른 횟수(" + c("call_count") + "), 원인을 없앤 뒤 " + c("invoke(None, config)"),
     "둘째 노드의 알림 실패, 이어 갈 때 노드마다 부른 횟수"),
    (link(L_06, "06절"), "멱등 키, 함수 " + c("append_key") + "·" + c("append_key_once") + "(도구 파일), 쓰기 방식 " + c("naive") + "·" + c("idempotent"),
     "대출 키 " + c("loan-2307") + ", 둘째 노드의 대출 기록, 실행 2에서 바꾸는 값"),
    (link(L_CH13_02, "Ch 13 02절"), "이어 붙이기 규칙 " + c("operator.add"), "칸 " + c("notes")),
])

FUNC_TABLE = table_html(["이름", "하는 일", "가져온 곳"], [
    (c("call_count") + "·" + c("failure_plan") + "·" + c("write_plan"), "노드마다 부른 횟수, 실패 흉내, 쓰기 방식과 파일 앞머리", "05절 모양(쓰기 방식 딕셔너리는 이 절에서 더함)"),
    (c("LoanState") + "·" + c("receive_request") + "·" + c("record_loan"), "상태 형식과 노드 둘", "06절 모양(칸·노드 이름을 바꾸고 부른 횟수·실패 흉내를 더함)"),
    (c("append_key()") + "·" + c("append_key_once()"), "기록 파일에 키 한 줄 적기, 이미 적힌 키면 건너뛰기", "도구 파일(06절)"),
    (c("read_saved()") + "·" + c("read_record()") + "·" + c("new_prefix()"), "새 연결로 파일에 남은 체크포인트 읽기, 기록 파일의 키 목록, 아직 쓰지 않은 파일 앞머리 고르기", "도구 파일(04절)"),
])

RESULT_TABLE = table_html(
    ["실행", "쓰기 방식", "멈춘 뒤 다음 노드<br>체크포인트 수 · 적힌 키", "이어 간 뒤 부른 횟수", "이어 간 뒤 칸 " + c("notes") + "<br>체크포인트 수", "같은 키가 적힌 줄 수"],
    [
        ("실행 1", c("idempotent"), c("('record_loan',)") + "<br>3 · " + c("['loan-2307']"), c("{'receive_request': 1, 'record_loan': 2}"), c("['신청 받음', '건너뜀']") + "<br>4", "1"),
        ("실행 2(바꾼 값)", c("naive"), c("('record_loan',)") + "<br>3 · " + c("['loan-2307']"), c("{'receive_request': 1, 'record_loan': 2}"), c("['신청 받음', '적음']") + "<br>4", "2"),
    ])

LOOK_B5 = ("노트북 5절에서 <code>다음 노드: ('record_loan',)</code>과 <code>멈추기 전에 적힌 키: ['loan-2307']</code>을 봅니다. "
           "이어 간 뒤 <code>부른 횟수: {'receive_request': 1, 'record_loan': 2}</code>와 <code>같은 키가 적힌 줄 수: 1</code>인지 확인합니다. "
           "6절에서는 <code>같은 키가 적힌 줄 수: 2</code>를 보고, 7절 두 줄로 두 실행을 맞춰 봅니다.")


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


def mermaid_block(name: str, alt: str, caption: str, reading: str) -> str:
    return ("{{mermaid:" + name + "|" + alt + "|" + caption + "}}\n"
            + '<p class="look"><b>도식 읽기</b> — ' + html_text(reading) + "</p>\n")


def src_html() -> str:
    return ("""<!--meta: 실습 30분 | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 0 -->
""" + STYLE + """
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>SQLite 체크포인터를 붙인 그래프를 실패 흉내로 멈추고, 새 연결로 다시 연 그래프에서 이어 갈 수 있습니다.</li>
<li>멈춘 노드가 이어 갈 때 처음부터 다시 실행되는 것을, 부른 횟수와 칸 값으로 확인할 수 있습니다.</li>
<li>쓰기 방식 하나만 바꿔 다시 실행하고, 대출 기록 파일의 줄 수로 두 실행을 견줄 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>이 챕터에서는 상태를 남기고 이어 가는 기능을 절마다 따로 익혔습니다. """ + link(L_03, "03절") + """은 체크포인트를 SQLite 파일에 남기고, 새 연결로 같은 스레드를 이어 갔습니다. """ + link(L_05, "05절") + """은 실패 흉내로 멈춘 실행을, 원인을 없앤 뒤 <code>invoke(None, config)</code>로 이어 갔습니다. """ + link(L_06, "06절") + """은 다시 실행된 노드가 바깥에 한 쓰기를 멱등 키로 한 번만 남겼습니다. 실제 창구 프로그램에서는 이 일들이 한 처리 안에서 함께 일어납니다.</p>
<p>이번 실습은 세 기능을 자료실 대출 처리 한 건에 모아 실행합니다. 쓰기 방식 하나만 바꿔 한 번 더 실행하고, 두 실행을 견줍니다. 06절도 같은 두 쓰기 방식을 견줬고, 그때는 자식 프로세스를 강제로 끝내 노드를 다시 실행하게 했습니다. 새로 볼 것은 같은 커널 안의 실패 흉내로 멈추고 새 연결에서 이어 갈 때도, 같은 차이가 나는지입니다.</p>
<p>이번 절은 이 챕터의 실습입니다. 01~06절에서 쓴 이름과 Ch 2에서 배운 문법만 쓰고, 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p>
<p><strong>이 절의 질문</strong> — 대출 기록을 적은 노드가 멈췄다가 이어 가면, 그 노드는 어디서부터 다시 실행될까요? 쓰기 방식 하나를 바꾸면 결과의 어디까지 달라질까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>이번 실습은 아래 절에서 배운 이름을 그대로 씁니다. 함수는 도구 파일 <code>checkpoint_tools.py</code>에서 가져오고, 상태 형식과 노드는 노트북에 적습니다.</p>
""" + LEARNED_TABLE + """
<p>붙인 기능은 03절 SQLite 체크포인터, 05절 실패 흉내와 이어 가기, 06절 멱등 키 확인 셋입니다. 멱등 키 확인이 흐름 안에서 일하려면, 기록을 적은 노드가 다시 실행되어야 합니다. 그래서 기록을 적는 노드 안에, 기록 뒤에 실패 흉내를 두었습니다. 06절 주의 메모에서 노트북 밖에서만 확인했다고 적은 장면을, 이번에는 노트북에서 실행합니다. 04절 함수 둘은 결과를 읽는 데만 씁니다.</p>
<p>""" + link(L_02, "02절") + """ PostgreSQL 체크포인터는 서버를 따로 켜야 해 뺐습니다. 04절 저장 시점 비교와 강제 종료는 04절과 06절에서 이미 견줬습니다. 자식 프로세스를 띄우면 코드와 실행 시간도 늘어, 이번에는 한 커널 안에서 끝냅니다. 05절의 같은 단계 두 노드와 남은 쓰기는, 노드 하나가 멈추는 이번 흐름에 나오지 않아 뺐습니다. 03절 메시지 칸은 이번 처리에 대화가 없어 뺐습니다.</p>
<p>다른 챕터의 실습은 모델을 몇 번 부르지만, 이 챕터의 실습은 모델을 부르지 않습니다. 01절처럼 매번 같은 값을 내는 우리 노드여야, 파일에 남은 값이 맞는지 출력으로 가를 수 있기 때문입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>""" + link(L_01, "01절") + """부터 한 수를 둘 때마다 즉석사진을 찍어 판의 모습을 남겼습니다. 06절에서는 판 옆에 기보를 두고, 둔 수를 한 줄씩 적었습니다. 이번에는 판 앞에 사진 한 장과 기보 한 장을 나란히 두고, 리본 하나로 판과 이어 둡니다. 수를 두다가 말 하나가 쓰러지면, 사진을 보고 그 수를 다시 둡니다. 기보에 그 수가 이미 적혀 있으면 다시 적지 않습니다.</p>
""" + illustration_block() + BEYOND_ILLU + """<h3>실습 조립의 구성</h3>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + FUNC_TABLE + """
<h3>두 번의 실행</h3><p>실행 1은 쓰기 방식 <code>idempotent</code>, 실행 2는 <code>naive</code>로 같은 대출 신청을 처리합니다. 두 실행 모두 둘째 노드를 실패 흉내로 멈춘 뒤, 연결을 닫고 새 연결로 연 그래프에서 이어 갑니다. 이용자 번호·대출 키·설계 객체·실패 흉내는 두 실행이 같습니다. 두 실행의 기록이 섞이지 않게, 파일 이름은 쓰기 방식 이름에 번호를 붙인 앞머리로 씁니다. 앞머리는 04절 함수 <code>new_prefix</code>가 고르고, 설정 셀을 다시 실행하면 번호가 올라 새 파일을 씁니다.</p>
<h3>비교와 경계</h3><p>05절에서는 같은 단계의 두 노드 가운데 하나만 멈췄습니다. 먼저 끝난 노드의 쓰기가 체크포인트에 딸려 남아, 이어 갈 때 그 노드는 다시 실행하지 않았습니다. 이번 흐름의 첫째 노드는 앞 단계에서 이미 끝나, 그 결과가 체크포인트에 있습니다. 그래서 이어 갈 때 다시 실행하는 것은 멈춘 둘째 노드뿐입니다.</p><p>멈춘 노드는 첫 줄부터 다시 실행됩니다. 설치판 소스 <code>langgraph/pregel/main.py</code> 2967~2968행은 이어 갈 때 쓰기가 없는 작업만 실행하고, 05절에서도 본 자리입니다. 체크포인트는 칸 값과 칸에 낸 갱신만 담습니다. 그래서 노드가 바깥에 한 쓰기는 06절처럼 노드 스스로 한 번만 반영되게 적어야 합니다.</p><p>세 딕셔너리도 체크포인트 밖에 있습니다. 부른 횟수가 이어 가는 동안 계속 늘어난 것도, 실행 2 전에 코드로 처음 값에 맞춘 것도 그 때문입니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 오늘 처리할 대출 한 건의 값을 정하고, 세 딕셔너리·상태 형식·노드 둘·설계 객체를 만듭니다. 실행 1은 파일 <code>idempotent-1.sqlite</code>로 둘째 노드를 멈춘 뒤, 연결을 닫고 새 그래프로 이어 갑니다. 실행 2는 쓰기 방식 하나만 <code>naive</code>로 바꿔 같은 차례를 되풀이하고, 마지막에 두 실행을 견줍니다.</p><p>이 절은 모델을 부르지 않아 모델 요청은 0번이고, API 키 셀도 없습니다. 자식 프로세스는 띄우지 않습니다. SQLite 파일과 대출 기록 파일은 노트북이 만든 빈 임시 폴더에 생깁니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
<h3>실행 1의 실제 순서</h3>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>두 실행은 쓰기 방식 하나만 달랐습니다. 결과는 아래 표와 같았습니다.</p>
""" + RESULT_TABLE + """
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>두 실행 모두 둘째 노드는 기록을 적은 뒤 멈췄고, 파일에는 첫째 노드까지의 체크포인트 셋이 남았습니다. 새 연결로 연 그래프는 두 실행 모두 멈춘 자리를 읽었고, 둘째 노드만 처음부터 다시 실행했습니다. 부른 횟수와 체크포인트 수는 두 실행이 같았습니다.</p><p>달라진 것은 다시 실행된 <code>record_loan</code>이 한 일입니다. 쓰기 방식 <code>idempotent</code>는 기록 파일에서 키를 찾아 <code>건너뜀</code>을 냈고, 대출 기록은 한 줄이었습니다. 쓰기 방식 <code>naive</code>는 검사 없이 한 줄을 더 적어, 같은 키가 두 줄 남았습니다. 06절 주의 메모가 노트북 밖에서 본 결과와 같은 차이입니다.</p><p>모델을 부르지 않아, 이 값들은 새 커널로 다시 실행해도 같아야 합니다. """ + RUNS_SENTENCE + """ 노트북 밖 준비 확인에서도 같은 흐름을 열 번 되풀이해, 한 번도 다른 값이 나오지 않았습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>대출 키 <code>loan-2307</code>은 이 절에서 실행 전에 정한 값입니다. 이용자 번호 <code>M-0317</code>은 """ + link(L_CH21_03, "Ch 21 03절") + """ 값 그대로이고, 실제 이용자와 대출이 아닙니다.</li><li>대출 기록과 알림은 실제 서비스를 부르지 않았습니다. 기록은 파일 한 줄로, 알림은 실패 흉내로만 대신했습니다.</li><li>실패 흉내는 기록을 적은 뒤에 두었습니다. 기록을 적기 전에 멈추는 장면은 이번에 실행하지 않았습니다.</li><li>06절 주의 메모는 실패 흉내로 멈춘 뒤 이어 가는 장면을 노트북 밖에서만 확인했다고 적었습니다. 이 실습은 그 장면을 노트북에서 실행했고, 두 쓰기 방식의 줄 수도 06절 메모와 같았습니다.</li><li>부른 횟수·실패 흉내·쓰기 방식 딕셔너리는 체크포인트 밖에 있습니다. 그래서 실행 2를 시작하기 전에 코드로 처음 값에 다시 맞췄습니다.</li><li>두 실행은 파일을 따로 썼습니다. 스레드 이름이 같아, 한 파일을 함께 쓰면 01절의 규칙대로 실행 2가 실행 1의 스레드에 이어 붙게 됩니다. 그 장면은 이번에 실행하지 않았습니다.</li><li>설정 셀은 3절 딕셔너리 셀과 6절 첫 셀입니다. 이 셀을 다시 실행하면 파일 앞머리의 번호가 올라, 앞 실행의 파일과 섞이지 않는 새 파일을 씁니다. 그래서 실행 하나를 그 설정 셀부터 다시 실행해도 같은 결과가 나옵니다.</li><li>실패 원인을 없애지 않고 이어 가는 장면은 이번에 실행하지 않았습니다. 05절 노트북 밖 확인에서는 같은 실패 흉내로 다시 멈췄습니다.</li><li>저장 시점은 적지 않아 기본값으로 실행했습니다. 다른 저장 시점과 강제 종료는 이번에 실행하지 않았습니다.</li><li>이 절의 멱등 키 확인은 06절처럼 기록 파일을 읽은 뒤에 적습니다. 여러 프로그램이 같은 파일에 함께 쓰는 장면은 이번에 실행하지 않았습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13과 SQLite 3.53.1로 만들었습니다. Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>대출 기록을 적은 노드가 실패 흉내로 멈추자, 체크포인트에는 그 노드의 갱신이 없고 기록 파일에는 한 줄이 남았습니다.</li><li>새 연결로 연 그래프가 <code>None</code>으로 이어 가자, 첫째 노드는 두고 멈춘 노드만 처음부터 다시 실행했습니다.</li><li>쓰기 방식 <code>idempotent</code>는 대출 기록을 한 줄, <code>naive</code>는 같은 키를 두 줄 남겼습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 23이 끝납니다. """ + link(L_CH24_01, "Ch 24 01절") + """에서는 되돌리기 어려운 일을 하기 전에, 사람이 확인하는 자리에서 그래프를 멈추는 방법을 다룹니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. [하] 두 실행에서 바꾼 값은 무엇이고, 같게 둔 것은 무엇입니까?</p><p class="quiz-a">쓰기 방식을 <code>idempotent</code>에서 <code>naive</code>로 바꿨습니다. 이용자 번호·대출 키·설계 객체·실패 흉내·이어 가는 방법은 같게 두었습니다. 파일 이름은 두 실행의 기록이 섞이지 않게 쓰기 방식 이름에 번호를 붙인 앞머리로 썼습니다.</p><p class="quiz-q">2. [중] 멈춘 뒤 체크포인트에는 <code>record_loan</code>이 낸 글이 없는데, 기록 파일에 키가 한 줄 있었던 까닭은 무엇입니까?</p><p class="quiz-a">노드 <code>record_loan</code>이 기록을 적은 뒤 실패 흉내로 멈췄기 때문입니다. 칸에 낼 갱신은 노드가 끝나야 저장되지만, 파일 쓰기는 이미 끝나 있었습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">3. [중] 이어 갈 때 <code>receive_request</code>는 다시 불리지 않고 <code>record_loan</code>은 다시 불린 까닭은 무엇입니까?</p><p class="quiz-a">첫째 노드는 앞 단계에서 끝나 그 결과가 체크포인트에 있었습니다. 둘째 노드는 끝나지 못해 갱신이 저장되지 않았고, 그래서 처음부터 다시 실행했습니다. 부른 횟수 <code>{'receive_request': 1, 'record_loan': 2}</code>로 확인했습니다. 틀렸다면 노트북 5절과 05절을 다시 읽습니다.</p><p class="quiz-q">4. [상] 동료가 「체크포인터를 SQLite 파일에 두었으니, 멈췄다 이어 가도 대출 기록은 한 번만 남는다」고 말합니다. 이 절 결과로 무엇이라고 답하나요?</p><p class="quiz-a">그렇지 않다고 답합니다. 체크포인트는 칸 값과 칸에 낸 갱신만 담고, 노드가 바깥 파일에 쓴 줄은 담지 않습니다. 쓰기 방식 <code>naive</code>에서는 같은 키가 두 줄 남았습니다. 한 줄만 남긴 것은 멱등 키를 확인한 <code>append_key_once</code>였습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li>01절 — 체크포인터·스레드와 설정 딕셔너리의 <code>thread_id</code>.</li><li>03절 — SQLite 체크포인터와, 새 연결·새 그래프로 이어 가기.</li><li>04절 — 함수 <code>read_saved</code>·<code>read_record</code>와 저장 시점의 기본값.</li><li>05절 — 실패 흉내와 <code>invoke(None, config)</code>.</li><li>06절 — 멱등 키와 함수 <code>append_key</code>·<code>append_key_once</code>.</li><li>langgraph 1.2.11 소스 <code>langgraph/pregel/main.py</code> 2967~2968행 — 이어 갈 때 쓰기가 없는 작업만 실행하는 자리입니다.</li><li>같은 판 <code>langgraph/pregel/_loop.py</code> 856행·861~865행 — 입력이 <code>None</code>이면 이어 가는 것으로 보는 자리입니다.</li><li>기준 버전은 노트북 1절 첫 셀에서 설치한 패키지 둘의 판입니다.</li></ul>
""")


# 삽화 뒤 비유 풀이 단락(삽화를 본 뒤 그림에 보이는 것과 맞춰 씀)
BEYOND_ILLU = os.environ.get("AUTHOR07_BEYOND_ILLU", "<p>리본은 판 앞 가장자리에서 사진과 기보 사이를 지나며, 두 물건이 이 판 하나에 딸린 것임을 보이려고 둔 소품입니다. 말이 쓰러져도 사진이 남아 있으면, 그 자리부터 다시 둘 수 있습니다. 다시 둘 때 기보를 먼저 보면, 이미 적힌 수를 한 번 더 적지 않습니다.</p>\n")


def write_src() -> Path:
    SRC.write_text(src_html(), encoding="utf-8")
    return SRC


def function_dumps(source: str) -> dict:
    found = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.FunctionDef):
            found[node.name] = ast.dump(node)
    return found


def check_same_as_before() -> None:
    """앞 절 생성기·도구 파일과 대조합니다(본문의 「같은 함수」·「같은 모양」·「같은 글」은 이 대조가 근거)."""
    import hashlib
    tools = TOOLS_PATH.read_text(encoding="utf-8")
    assert hashlib.sha256(tools.encode("utf-8")).hexdigest() == TOOLS_SHA256, "도구 파일이 마감 판과 다릅니다"
    assert tools == author_06.TOOLS, "도구 파일이 06절 생성기 판과 다릅니다"
    moved = function_dumps(tools)
    for definition in [author_06.DEF_APPEND, author_06.DEF_ONCE, author_04.DEF_READ, author_04.DEF_RECORD, author_04.DEF_NEW]:
        original = ast.parse(definition).body[0]
        assert definition in tools, original.name
        assert moved[original.name] == ast.dump(original), original.name
    # 임시 폴더 셀은 01절 셀에서 앞머리 ch23-01- → ch23-07- 만 다르다(세 곳)
    assert FOLDER != author_01.FOLDER and FOLDER.replace("ch23-07-", "ch23-01-") == author_01.FOLDER
    assert author_01.FOLDER.count("ch23-01-") == 3
    # 실패 흉내의 오류 글은 05절 노드 flaky와 같다
    assert FAIL_LINE in author_05.NODE_FLAKY
    # 상태 형식은 06절 OrderState와 칸 이름만 다르다
    assert STATE_BODY.replace("LoanState", "OrderState").replace("loan_key", "order_key") == author_06.STATE_BODY
    # 설계 객체 여섯 줄은 06절 여섯 줄과 상태 형식·노드 이름만 다르다
    body = "\n".join(BUILDER.splitlines()[1:7])
    renamed = body.replace("LoanState", "OrderState").replace("receive_request", "receive_order").replace("record_loan", "charge")
    assert renamed == author_06.BUILDER_LINES
    # 새 연결 셀은 03절처럼 check_same_thread=False로 연다
    assert 'check_same_thread=False' in author_03.CONNECT
    # 앞당겨 쓰지 않는 이름
    for source in [IMPORTS, TASK, PLAN, STATE, NODE_RECEIVE, NODE_RECORD, BUILDER, R1_OPEN, R1_FAIL, R1_READ, R1_REOPEN,
                   R1_RESUME, R1_AFTER, R2_SET, R2_FAIL, R2_READ, R2_RESUME, R2_AFTER, COMPARE, FILES_END]:
        for word in ["interrupt", "durability", "stream", "subprocess", "Command"]:
            assert word not in source, word


if __name__ == "__main__":
    check_same_as_before()
    print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "07", SLUG, "experiment", cells())
        print("wrote", path)
