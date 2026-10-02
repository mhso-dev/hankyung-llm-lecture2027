"""Ch 16 07절(챕터 끝 실습 절) 노트북 + 본문 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§6·§7-2).

사용:
  python3 author_07.py            → 노트북 + _src 본문을 함께 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_07.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
  AUTHOR07_NB_ONLY=1 python3 author_07.py → 노트북만 다시 쓴다(그림을 그리기 전 새 커널 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
새 절이라 수정 전 원본이 없다. **서비스 모델 절이다.** 설명만 고칠 때는 mdpatch.py → run_section.sh --no-exec(규격 §3).

주제: 미르시립도서관 상담 창구에 들어온 질문 셋(가짜 개인정보가 하나씩 든 질문)을 차례로 처리한다.
질문마다 02절 mask_pii로 가리고, 04절 reserve로 예약한 뒤 모델에 보내고, 05절 감사 기록 한 줄(칸 넷)을
노트북 안 기록 목록에 남긴다. 예약에서 멈춘 질문도 사건 stopped로 남긴다(serve_all의 except). 실행 1은 04절 호출 한도 2,
실행 2는 호출 한도 하나만 1로 바꾼다. 끝에 두 실행의 기록을 지문으로 짝지어 사건 이름이 달라진 줄을 찾는다.

## 함께 붙인 앞 절 기능 세 가지 (규격 §7-2 「앞 절 기능 2~3개」, handoff §06 → 실습(07))

1. 02절 가리기 — mask_pii(질문마다), find_raw_values(보낼 메시지·기록 목록에 원문 값이 남았는지).
2. 04절 예약 — make_budget·reserve(04절 값 호출 한도 2·비용 상한 0.01·예상 비용 0.002).
3. 05절 감사 기록 — fingerprint_of·safe_detail로 만드는 칸 넷(event·query_hash·query_masked·detail), 소금값 ch16-session,
   사건 이름 answer·stopped. 파일에는 쓰지 않고 노트북 안 목록에만 더한다
   (note_event = 도구 파일 record_event에서 write_audit_rows(log) 한 줄만 뺀 함수, 인자 이름·나머지 본문 같음).
메시지 모양은 06절 build_rag_messages(문서 구역)로 만든다 — 보낼 글을 만드는 자리라 붙인 기능 셋에 세지 않는다.

## 뺀 것과 까닭 (b3 · 07-diagnosis.md §2)

- 01 입력 검사·출력 검사: 06절 한 흐름에 이미 들어 있다. 출력 검사는 모델이 적은 표시 꼴에 결과가 달려 있다.
- 03 자르기·요약: 질문이 하나씩 따로 오는 창구라 대화 기록이 없다. 요약은 모델 요청을 늘린다.
- 05 재시도·예비 흐름: 실패 흉내를 다시 만들어야 하고 05절 되풀이.
- 06 문서 검사·격리: 06절 주제이고, 이번 모델은 숨은 지시문을 따른 적이 없다(38번). 이 실습은 안내 문서 E01만 쓴다.
- 06 guarded_generate: 그대로 부르면 06절 조립 되풀이(규격 §7-2 5항). 이 실습 조립은 예약에서 멈춘 질문도 기록한다
  (guarded_generate는 reserve가 막으면 기록 없이 오류를 올리는 모양 — 06절은 그 자리를 실행하지 않았다).

## 흔들림 확인을 하지 않은 까닭 (규격 §2-7 10번 끝)

핵심 관찰(받은 답 수·예약한 호출 수·기록 줄 수·사건 이름·원문 값 없음·달라진 줄)은 모두 reserve·mask_pii·fingerprint_of가
정하는 값이다. 모델 답 문장은 출력만 하고 기록·결론·그림에 쓰지 않는다(04·05절 선례).

## 요청 수

실행 한 번에 3번(실행 1 두 번 + 실행 2 한 번), 모두 gpt-5.4-mini(temperature=0·reasoning_effort="none"), 임베딩 0.
규격 §7-2의 3~5번 안. 쓰는 파일 0(자료 파일 읽기만, runs/05·06-audit.jsonl은 건드리지 않음).

## 이 절이 새로 만든 함수 넷(노트북에만, 도구 파일은 고치지 않음)

note_event(log, event, query, detail) · print_rows(log) · serve_question(log, budget, question, documents, estimated_cost_usd)(조립: 가리기 → 예약 → 모델 → answer 기록) ·
serve_all(log, budget, questions, documents, estimated_cost_usd)(질문 목록, 예약에서 막힌 ValueError를 받아 stopped 기록 뒤 다음 질문).
함수 본문 최대 8줄(serve_all). 멈춘 질문은 원문 질문을 note_event에 넘기지만 note_event가 첫 줄에서 가린다(05절 record_event와 같음).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·lambda·조건 표현식·elif·next·all·any·sum·max·min·enumerate·zip·key=·reverse=·set·
setdefault·.get·+=·기본값 매개변수·타입힌트·한 줄 다중 대입·세미콜론·클래스 정의·데코레이터·isinstance·dict()·맨 raise·
파일 쓰기. 앞 절 노트북에만 있던 함수(summarize_text·build_messages·ask_with_budget·ask_all·ask_primary·ask_backup·ask_model)도
다시 쓰지 않았다(모델은 조립 함수 안에서 model.invoke(...).text로 직접 부름).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part4/ch16-guardrails/notebooks"
SRC = ROOT / "textbook/part4/ch16-guardrails/_src/07-가드레일-실습.html"
SLUG = "07-가드레일-실습"

INSTALL = install_source(["langchain==1.4.0", "langchain-openai==1.6.1", "python-dotenv==1.2.3"])

IMPORTS = r'''# 자료 파일을 읽을 모듈, 앞 절 함수 일곱, 모델을 만들 이름을 불러옵니다
import json
import os

from guardrails import build_rag_messages, find_raw_values, fingerprint_of, make_budget, mask_pii, reserve, safe_detail
from langchain.chat_models import init_chat_model

print("02절:", "find_raw_values", "mask_pii")
print("04절:", "make_budget", "reserve")
print("05절:", "fingerprint_of", "safe_detail")
print("06절:", "build_rag_messages")'''

ROOT_PATH = r'''# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part4/ch16-guardrails/data"):
        root_path = candidate
        break
print("찾은 프로젝트 맨 위:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

READ_PICK = r'''# 자료 파일을 읽고 이 실습의 검색 결과로 안내 문서 E01 하나만 고릅니다(읽기만 합니다)
data_path = root_path + "/labs/part4/ch16-guardrails/data"
with open(data_path + "/retrieved-documents.json", encoding="utf-8") as file:
    all_documents = json.loads(file.read())
retrieved = []
for document in all_documents:
    if document["doc_id"] == "E01":
        retrieved.append(document)
print("자료 파일의 문서 수:", len(all_documents))
print("고른 문서:", retrieved[0]["doc_id"], "|", retrieved[0]["title"])'''

QUESTIONS = r'''# 실행 전에 정한 상담 질문 셋입니다: 질문은 이 절에서 적었고, 가짜 값 셋은 02절에서 지어낸 값입니다
fake_values = ["test.user@example.com", "010-0000-0000", "1111-2222-3333-4444"]
questions = [
    "이번 주 월요일에 책을 반납하러 가도 되나요? 답은 " + fake_values[0] + " 으로 보내 주세요.",
    "공휴일이 월요일과 겹치면 화요일에도 쉬나요? 연락처는 " + fake_values[1] + " 입니다.",
    "법정 공휴일에도 문을 여나요? 연체료는 카드 " + fake_values[2] + " 로 내겠습니다.",
]
print("질문 수:", len(questions))
print("질문 출처:", "이 절에서 실행 전에 적은 글")
print("가짜 값 출처:", "02절에서 지어낸 값", fake_values)'''

MASK_ALL = r'''# 질문 셋을 02절 함수 mask_pii로 가려 봅니다(모델은 부르지 않습니다)
print("번호 | 가린 질문 | 종류별 개수")
for i in range(len(questions)):
    masked, counts = mask_pii(questions[i])
    print(i, "|", masked, "|", counts)'''

MESSAGES = r'''# 가린 첫 질문으로 06절 함수 build_rag_messages가 만드는 메시지를 봅니다(보내지는 않습니다)
first_masked = mask_pii(questions[0])[0]
first_messages = build_rag_messages(first_masked, retrieved)
first_raw = find_raw_values(first_messages[1]["content"], fake_values)
print("메시지 수:", len(first_messages))
print("사용자 메시지:")
print(first_messages[1]["content"])
print("사용자 메시지에 남은 원문 값:", first_raw)'''

SETTINGS = r'''# 04절 예산 값과 05절 소금값을 그대로 씁니다(요금표로 센 값이 아니라 앞 절에서 정한 값입니다)
max_calls = 2
max_cost_usd = 0.01
estimated_cost = 0.002
session_salt = "ch16-session"
print("호출 한도:", max_calls)
print("비용 상한(달러):", max_cost_usd)
print("요청 하나의 예상 비용(달러):", estimated_cost)
print("소금값:", session_salt)'''

DEF_NOTE = r'''# 05절 record_event처럼 기록 한 줄을 만들어 목록에 더합니다(파일에는 쓰지 않습니다)
def note_event(log, event, query, detail):
    masked_query = mask_pii(query)[0]
    fingerprint = fingerprint_of(log["salt"], masked_query)
    row = {"event": event, "query_hash": fingerprint,
           "query_masked": masked_query, "detail": safe_detail(detail)}
    log["rows"].append(row)
    return row'''

DEF_PRINT = r'''# 기록 목록을 한 줄씩 봅니다: 번호·사건 이름·가린 질문, 그다음 줄에 기록 칸
def print_rows(log):
    rows = log["rows"]
    print("번호 | 사건 | 가린 질문")
    for i in range(len(rows)):
        print(i, "|", rows[i]["event"], "|", rows[i]["query_masked"])
        print("  기록 칸:", rows[i]["detail"])'''

DEF_SERVE = r'''# 조립 함수: 가리기(02절) → 예약(04절) → 모델 요청 → 기록 한 줄(05절 칸 넷)을 한 흐름으로 잇습니다
def serve_question(log, budget, question, documents, estimated_cost_usd):
    # 02절: 모델에 보낼 질문을 먼저 가립니다
    masked_question, pii_counts = mask_pii(question)
    # 04절: 부르기 전에 예약합니다(한도를 넘으면 여기서 ValueError가 나고 모델은 부르지 않습니다)
    reserve(budget, estimated_cost_usd)
    # 예약이 되면 모델에 한 번 보내고, 답을 받은 사건을 05절 칸 넷으로 남깁니다(답 문장은 넣지 않습니다)
    answer = model.invoke(build_rag_messages(masked_question, documents)).text
    note_event(log, "answer", masked_question, {"pii": pii_counts, "reserved_calls": budget["calls"]})
    return answer'''

DEF_ALL = r'''# 질문 목록을 차례로 처리합니다: 예약에서 멈춘 질문도 사건 stopped로 기록하고 다음 질문으로 넘어갑니다
def serve_all(log, budget, questions, documents, estimated_cost_usd):
    answers = []
    for question in questions:
        try:
            answers.append(serve_question(log, budget, question, documents, estimated_cost_usd))
        except ValueError as error:
            note_event(log, "stopped", question, {"reason": str(error), "reserved_calls": budget["calls"]})
            print("멈춘 까닭:", error)
    return answers'''

RUN1 = r'''# 실행 1: 04절 호출 한도 2로 질문 셋을 처리합니다(모델 요청 2번, 셋째 질문은 예약에서 멈출 것입니다)
budget_one = make_budget(max_calls, max_cost_usd)
log_one = {"salt": session_salt, "rows": []}
answers_one = serve_all(log_one, budget_one, questions, retrieved, estimated_cost)
print("받은 답 수:", len(answers_one))
print("예약한 호출 수:", budget_one["calls"])
print("기록 줄 수:", len(log_one["rows"]))'''

SHOW1_ROWS = r'''# 실행 1의 기록 목록을 한 줄씩 봅니다
print("실행 1의 기록 목록:")
print_rows(log_one)'''

SHOW1_ANSWERS = r'''# 실행 1에서 받은 답을 번호와 함께 봅니다(모델이 쓴 글이라 실행마다 달라질 수 있습니다)
print("번호 | 받은 답")
for i in range(len(answers_one)):
    print(i, "|", answers_one[i])'''

CHECK1 = r'''# 실행 1의 기록 목록을 JSON 글로 펴서 가짜 값 원문이 남았는지 봅니다(코드가 정한 값이라 assert로 봅니다)
rows_text_one = json.dumps(log_one["rows"], ensure_ascii=False)
raw_one = find_raw_values(rows_text_one, fake_values)
print("기록에 남은 원문 값:", raw_one)
assert raw_one == []'''

RUN2 = r'''# 실행 2: 바꿀 값은 호출 한도 하나입니다. 2 대신 1로 같은 질문 셋을 처리합니다(모델 요청 1번)
smaller_call_limit = 1
budget_two = make_budget(smaller_call_limit, max_cost_usd)
log_two = {"salt": session_salt, "rows": []}
answers_two = serve_all(log_two, budget_two, questions, retrieved, estimated_cost)
print("받은 답 수:", len(answers_two))
print("예약한 호출 수:", budget_two["calls"])
print("기록 줄 수:", len(log_two["rows"]))'''

SHOW2_ROWS = r'''# 실행 2의 기록 목록을 한 줄씩 봅니다
print("실행 2의 기록 목록:")
print_rows(log_two)'''

CHECK2 = r'''# 실행 2의 기록 목록에도 가짜 값 원문이 남았는지 봅니다(코드가 정한 값이라 assert로 봅니다)
rows_text_two = json.dumps(log_two["rows"], ensure_ascii=False)
raw_two = find_raw_values(rows_text_two, fake_values)
print("기록에 남은 원문 값:", raw_two)
assert raw_two == []'''

COMPARE = r'''# 두 실행을 한 표로 나란히 봅니다(멈춘 질문 수는 기록 줄 수에서 받은 답 수를 뺀 값입니다)
stopped_one = len(log_one["rows"]) - len(answers_one)
stopped_two = len(log_two["rows"]) - len(answers_two)
print("실행 | 호출 한도 | 받은 답 수 | 멈춘 질문 수 | 기록 줄 수")
print("실행 1 |", max_calls, "|", len(answers_one), "|", stopped_one, "|", len(log_one["rows"]))
print("실행 2 |", smaller_call_limit, "|", len(answers_two), "|", stopped_two, "|", len(log_two["rows"]))'''

PAIR = r'''# 두 실행의 기록을 번호마다 짝지어 지문이 같은지와 사건 이름을 봅니다
rows_one = log_one["rows"]
rows_two = log_two["rows"]
print("번호 | 같은 지문인가 | 실행 1 사건 | 실행 2 사건")
for i in range(len(rows_one)):
    same_print = rows_one[i]["query_hash"] == rows_two[i]["query_hash"]
    print(i, "|", same_print, "|", rows_one[i]["event"], "|", rows_two[i]["event"])'''

CHANGED = r'''# 사건 이름이 달라진 줄의 가린 질문만 모읍니다(원문 없이 어느 질문이 달라졌는지 찾습니다)
changed = []
for i in range(len(rows_one)):
    if rows_one[i]["event"] != rows_two[i]["event"]:
        changed.append(rows_two[i]["query_masked"])
print("사건이 달라진 줄 수:", len(changed))
print("달라진 질문(가린 글):", changed)'''


FIG1 = "07-1-가리기-예약-기록의-조립"
FIG1_ALT = "위에서 아래로 읽는 그림으로 초록 상자 상담 질문 셋에서 파란 상자 가리기 mask_pii 02절과 파란 상자 예약 reserve 04절을 지나고, 예약에서 왼쪽 실선은 보라 상자 모델 gpt-5.4-mini와 파란 상자 기록 한 줄 남기기 note_event answer로, 오른쪽 점선 한도를 넘으면 멈춤은 파란 상자 기록 한 줄 남기기 note_event stopped로 가며, 두 기록 상자가 맨 아래 초록 상자 기록 목록 파일에 쓰지 않음으로 모이는 그림"
FIG1_READ = """위에서 아래로 읽습니다. 초록 질문 셋이 파란 가리기와 예약을 지나 왼쪽 보라 모델에 닿습니다.
오른쪽 점선은 호출 한도를 넘을 때만 가는 갈래이고, 두 기록 상자는 맨 아래 초록 기록 목록으로 모입니다."""
FIG1_CAP = "질문마다 가리고 예약한 뒤 모델에 보냅니다. 답을 받든 예약에서 멈추든 기록 목록에 한 줄 남깁니다."

FIG2 = "07-2-실행-1의-실제-순서"
FIG2_ALT = "위에서 아래로 읽는 차례 그림으로 serve_all과 serve_question, 예산 04절, 모델 gpt-5.4-mini, 기록 목록 네 세로줄이 있고, 첫째와 둘째 질문은 예산에 예약하고, 예산 아래 노란 메모의 칸 calls가 1과 2가 된 뒤 가린 질문을 모델에 보내 답을 받고 기록 목록에 answer 한 줄을 남기며, 셋째 질문은 예산에서 점선 ValueError를 받고 예산 아래 노란 메모 호출 한도를 넘습니다가 붙은 뒤 기록 목록에 stopped 한 줄을 남기고, 맨 아래 기록 목록 쪽 노란 메모에 기록 줄 셋 원문 값 없음이 적힌 그림"
FIG2_CAP = "실행 1은 첫째와 둘째 질문만 모델에 보냈고, 셋째 질문은 예약에서 멈춘 채 기록에 남았습니다."

FIG3 = "07-3-호출-한도-둘과-하나"
FIG3_ALT = "칸 둘이 나란히 있고 아래에 상자 둘이 있는 그림으로 왼쪽 실행 1 호출 한도 둘 칸의 노란 상자에는 받은 답 둘, 예약한 호출 둘, answer 둘 stopped 하나가, 오른쪽 실행 2 호출 한도 하나 칸의 노란 상자에는 받은 답 하나, 예약한 호출 하나, answer 하나 stopped 둘이 적혀 있고, 두 칸에서 내려온 화살표가 가운데 노란 상자 지문으로 짝지은 줄 셋, 사건이 달라진 줄 하나, 둘째 질문이 실행 2에서 멈춤에 모이며, 맨 아래 회색 상자에 두 칸 모두 같은 질문 셋, 같은 소금값, 기록 줄 셋, 원문 값 없음이 적힌 그림"
FIG3_CAP = "호출 한도를 하나로 줄이자 둘째 질문도 멈췄고, 두 기록을 지문으로 짝지어 그 줄을 찾았습니다."

ILLU = "07-4-천과-개찰구와-대장"
ILLU_ALT = "흰 바탕에 긴 나무 탁자가 있고 탁자 가운데에 나무 기둥 둘과 가로대로 된 개찰구가 탁자 폭을 가로질러 서 있으며 거기서 나무 막대 하나가 왼쪽으로 뻗어 있고, 막대 앞 탁자 왼쪽 절반에는 오른쪽 절반이 하늘색 천으로 덮인 흰 쪽지 하나가, 개찰구 너머 오른쪽 절반에는 같은 천으로 덮인 쪽지 둘이 놓여 있으며, 탁자 뒤쪽 오른편에 왼쪽 쪽에 짧은 줄 셋이 적힌 펼친 대장과 나무 손도장 하나가 놓인 그림"
ILLU_CAP = "천으로 가린 쪽지 둘은 막대를 지났고, 하나는 막대 앞에 멈췄습니다. 뒤쪽 대장에는 줄 셋이 적혀 있습니다."
ILLU_READ = "긴 나무 탁자 가운데에 나무 기둥 둘과 가로대로 된 개찰구가 탁자 폭을 가로질러 서 있습니다. 개찰구에서 뻗은 막대 하나가 탁자 왼쪽 절반을 막고, 그 앞에 쪽지 하나가 놓여 있습니다. 개찰구 너머 오른쪽 절반에는 쪽지 둘이 놓여 있습니다. 쪽지 셋은 모두 오른쪽 절반이 하늘색 천으로 덮여 있습니다. 탁자 뒤쪽 오른편에는 왼쪽 쪽에 짧은 줄 셋이 적힌 펼친 대장과 나무 손도장 하나가 있습니다."

TITLE = """# 가드레일 실습: 상담 질문 셋에 가리기·예약·감사 기록 붙이기

**이 노트북에서 할 일**

1. 가짜 개인정보가 든 상담 질문 셋을 02절 함수로 가립니다.
2. 04절 예약과 05절 감사 기록을 붙인 조립 함수로 질문 셋을 차례로 처리합니다.
3. 호출 한도 하나만 바꿔 한 번 더 실행하고, 두 실행의 기록을 지문으로 짝지어 견줍니다.

**준비물** — 이 절은 프로젝트 맨 위 폴더의 `.env`에 적어 둔 `OPENAI_API_KEY`를 씁니다.
모델 요청은 모두 세 번이고, 실행 1에서 두 번, 실행 2에서 한 번 `gpt-5.4-mini`에 보냅니다.
임베딩 요청은 없습니다.
노트북을 한 번 실행하는 요금은 요금표로 어림해 미화 0.01달러 아래입니다.
실제 청구 금액과는 다를 수 있습니다.

읽는 파일은 이 챕터 자료 파일 `data/retrieved-documents.json` 하나이고, 읽기만 합니다.
새로 쓰는 파일은 없습니다. 감사 기록은 노트북 안 목록에만 남깁니다.
교재 출력을 만든 실행에서는 노트북 전체가 약 5초 만에 끝났습니다.

**기준 버전** — 첫 셀에서 LangChain 1.4.0과 langchain-openai 1.6.1을 설치합니다.
키를 읽는 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**실습 범위** — 이 절은 챕터 끝 실습 절이고 30분 안에 끝나는 분량입니다.
강사와 함께 첫 셀부터 차례로 실행하고, 따로 내는 과제는 없습니다.
01~06절에서 쓴 이름과 문법만 씁니다.

실습 폴더 `labs/part4/ch16-guardrails`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

이번 절은 이 챕터의 실습입니다.
01~06절에서 쓴 이름과 문법만 쓰고 따로 내는 과제는 없습니다.
첫 셀은 패키지 세 개를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 판 번호 세 줄이 보입니다.
출력 줄 `langchain: 1.4.0`과 `langchain-openai: 1.6.1`이 실습 폴더 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 모듈과 앞 절 함수 일곱을 불러옵니다.
02절 함수 둘, 04절 함수 둘, 05절 함수 둘, 06절 함수 하나를 다시 씁니다.

앞에서 배운 함수는 `guardrails.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
일곱 함수 모두 앞 절에서 쓰던 인자 그대로입니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 네 줄이 절마다 가져온 함수 이름입니다.
출력 줄 `02절: find_raw_values mask_pii`의 두 함수로 질문을 가리고 원문 값을 찾습니다.
출력 줄 `05절: fingerprint_of safe_detail`의 두 함수로 감사 기록 한 줄의 칸을 만듭니다.
출력 줄 `06절: build_rag_messages`는 모델에 보낼 메시지를 만드는 데만 씁니다.

## 2. 키와 모델 준비

이 절도 01~06절과 같은 모델 `gpt-5.4-mini` 하나만 씁니다."""),
    ] + key_and_model_cells(
        "openai:gpt-5.4-mini",
        "temperature 값을 0으로 두어도 답 문장이 매번 같다고 보장하지는 않습니다.",
    ) + [
        md("""## 3. 상황과 재료

이 실습의 상황은 이렇습니다.
미르시립도서관 상담 창구에 질문 셋이 차례로 들어왔습니다.
사용자는 질문마다 연락처나 카드 번호를 함께 적었습니다.
창구는 질문을 가린 뒤 모델에 보냅니다.
모델 요청은 정한 호출 한도 안에서만 하고, 한 일은 모두 기록합니다.

먼저 노트북을 연 자리에서 프로젝트 맨 위를 찾습니다.
01~06절과 같은 자리 찾기 셀입니다."""),
        setup(ROOT_PATH),
        md("""**결과 읽기** — 출력 줄 `찾은 프로젝트 맨 위:` 뒤에 점 하나나 위로 올라가는 자리가 보입니다.

다음 셀은 자료 파일을 읽고 안내 문서 `E01` 하나만 고릅니다.
01~05절과 같은 검색 결과입니다.
공격 문서 `E99`는 06절에서 살펴본 문서라 이 실습에서는 쓰지 않습니다."""),
        code(READ_PICK),
        md("""**결과 읽기** — 출력 줄 `자료 파일의 문서 수: 2`로 자료 파일에는 문서가 둘 있습니다.
출력 줄 `고른 문서: E01 | 미르시립도서관 이용 안내`가 이 실습의 검색 결과입니다.
세 질문 모두 이 문서 하나를 붙여 모델에 보냅니다.

다음 셀은 상담 질문 셋을 적습니다.
질문은 이 절에서 실행 전에 적은 글이고, 가짜 값 셋은 02절에서 지어낸 값입니다.
실제 사람의 정보가 아닙니다."""),
        code(QUESTIONS),
        md("""**결과 읽기** — 출력 줄 `질문 수: 3`으로 질문은 셋입니다.
출력 줄 `질문 출처: 이 절에서 실행 전에 적은 글`이 질문을 정한 곳입니다.
출력 줄 `가짜 값 출처: 02절에서 지어낸 값` 뒤 목록이 질문에 하나씩 넣은 가짜 값입니다.
첫 질문에는 이메일, 둘째에는 전화번호, 셋째에는 카드 번호가 들어 있습니다.

다음 셀은 질문 셋을 02절 함수 `mask_pii`로 가려 봅니다.
함수는 02절처럼 가린 글과 종류별 개수를 튜플 하나로 내놓습니다.
모델은 부르지 않습니다."""),
        code(MASK_ALL),
        md("""**결과 읽기** — 라벨 줄 `번호 | 가린 질문 | 종류별 개수` 아래 세 줄이 질문마다 가린 결과입니다.
번호 0 줄은 이메일이 `<EMAIL_MASKED>`로 바뀌었고, 종류별 개수에 `'email': 1`이 보입니다.
번호 1 줄은 전화번호가, 번호 2 줄은 카드 번호가 표식으로 바뀌었습니다.
질문마다 가린 값은 하나씩입니다.

다음 셀은 가린 첫 질문으로 모델에 보낼 메시지를 만들어 봅니다.
06절 함수 `build_rag_messages`는 시스템 메시지 글과 문서 구역을 담은 메시지 두 개를 만듭니다.
이 실습은 이 함수를 보낼 글을 만드는 데만 쓰고, 06절의 문서 검사와 격리는 쓰지 않습니다."""),
        code(MESSAGES),
        md("""**결과 읽기** — 출력 줄 `메시지 수: 2`로 06절과 같은 역할 딕셔너리 두 개입니다.
라벨 줄 `사용자 메시지:` 아래 첫 줄이 가린 첫 질문이고, 그 아래가 `E01` 문서 구역입니다.
출력 줄 `사용자 메시지에 남은 원문 값: []`으로 보낼 글에 가짜 값 원문은 없습니다.

다음 셀은 04절 예산 값과 05절 소금값을 적습니다.
모두 앞 절에서 정한 값을 그대로 씁니다."""),
        code(SETTINGS),
        md("""**결과 읽기** — 출력 줄 `호출 한도: 2`와 `비용 상한(달러): 0.01`은 04절에서 정한 값입니다.
출력 줄 `요청 하나의 예상 비용(달러): 0.002`도 04절 값이고, 요금표로 센 값이 아닙니다.
이 값은 청구 금액도 아닙니다.
출력 줄 `소금값: ch16-session`은 05절에서 지문을 만들 때 쓴 값입니다.

## 4. 기록 장치

결과를 볼 기록 장치부터 만듭니다.
05절 감사 기록은 한 줄마다 칸 넷을 두고 파일 전체를 다시 썼습니다.
이 실습은 같은 칸 넷을 노트북 안 목록에만 더하고 파일에는 쓰지 않습니다.
기록 목록은 소금값과 빈 목록을 담은 딕셔너리로 6절에서 만듭니다."""),
        code(DEF_NOTE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `note_event`는 05절 `record_event`에서 파일을 다시 쓰는 줄 하나만 뺀 함수입니다.
받은 질문을 한 번 더 가리고, 소금값과 가린 질문으로 지문을 만듭니다.
칸 `event`·`query_hash`·`query_masked`·`detail` 넷을 담은 한 줄을 `log["rows"]` 목록에 더합니다.
칸 `detail`의 값은 05절 `safe_detail`로 한 번 더 가립니다.

다음 셀은 기록 목록을 한 줄씩 보여 주는 함수입니다."""),
        code(DEF_PRINT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `print_rows`는 한 줄마다 번호·사건 이름·가린 질문을 출력합니다.
그다음 줄에는 칸 `detail`을 출력합니다.
기록에 든 값만 출력하므로 원문 질문은 나오지 않습니다.

## 5. 조립

다음 셀은 앞 절 기능 셋을 한 흐름으로 잇는 조립 함수입니다.
먼저 02절처럼 질문을 가리고, 04절처럼 예약합니다.
예약이 되면 모델에 보내고, 05절 칸 넷으로 기록 한 줄을 남깁니다.
예약이 막히면 04절처럼 `ValueError`가 나고, 그 뒤 줄은 실행되지 않습니다."""),
        code(DEF_SERVE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `serve_question`은 가린 질문만 메시지에 넣으므로 원문 값은 모델에 가지 않습니다.
예약이 모델 요청보다 앞이라, 예약이 막히면 모델을 부르지 않습니다.
답을 받으면 사건 `answer`와 종류별 개수·예약한 호출 수를 남깁니다.
모델은 2절에서 만든 `model`을 쓰고, 모델 답 문장은 기록에 넣지 않습니다.

다음 셀은 질문 목록을 차례로 처리하는 함수입니다.
예약에서 막힌 질문은 블록 `except`가 받아 사건 `stopped`로 한 줄 남깁니다.
04절 함수 `ask_all`은 예약이 막히면 그 자리에서 멈췄습니다.
이번에는 까닭을 출력하고 다음 질문으로 넘어가, 뒤 질문도 한 줄씩 남깁니다."""),
        code(DEF_ALL),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `serve_all`은 질문마다 조립 함수를 부르고, 받은 답만 목록에 모아 내놓습니다.
멈춘 질문은 원문 질문을 `note_event`에 넘기지만, 기록 장치가 첫 줄에서 가립니다.
그래서 멈춘 질문의 기록에도 가린 글만 남습니다.

06절 함수 `guarded_generate`는 예약에서 막히면 기록 없이 오류만 올리는 모양입니다.
이 실습은 멈춘 질문도 기록에 남겨, 기록만 보고 어느 질문이 왜 멈췄는지 알 수 있게 했습니다.

이것으로 부품과 기록 장치를 모두 만들었습니다.

## 6. 실행 1 · 호출 한도 2

실행 1은 04절 값 그대로 호출 한도 2로 질문 셋을 처리합니다.
실행 전에 예상해 봅니다.
첫째와 둘째 질문은 예약되어 모델에 가고, 셋째 질문은 예약에서 멈출 것입니다.
기록은 세 줄이고, 사건은 `answer`·`answer`·`stopped` 차례일 것입니다.
이 셀에서 모델 요청이 두 번 나갑니다."""),
        code(RUN1),
        md("""**결과 읽기** — 출력 줄 `멈춘 까닭: 호출 한도를 넘습니다.`는 예약에서 막힌 질문 하나의 까닭입니다.
출력 줄 `받은 답 수: 2`와 `예약한 호출 수: 2`로 모델 요청은 두 번 나갔습니다.
출력 줄 `기록 줄 수: 3`으로 멈춘 질문까지 세 줄이 남았습니다.
예상과 같습니다.

다음 셀은 실행 1의 기록 목록을 봅니다."""),
        code(SHOW1_ROWS),
        md("""**결과 읽기** — 라벨 줄 `번호 | 사건 | 가린 질문` 아래에 기록 세 줄이 있습니다.
번호 0과 1 줄은 사건 `answer`이고, 기록 칸에 종류별 개수와 예약한 호출 수가 있습니다.
두 줄의 `'reserved_calls': 1`과 `'reserved_calls': 2`가 그 줄을 남길 때까지 예약한 호출 수입니다.
번호 2 줄은 사건 `stopped`이고, 기록 칸 `'reason': '호출 한도를 넘습니다.'`가 멈춘 까닭입니다.
멈춘 질문도 카드 번호가 `<CARD_MASKED>`로 가려진 채 남았습니다.

칸 `query_hash`는 출력하지 않았지만 줄마다 들어 있습니다.
8절에서 두 실행의 기록을 짝지을 때 씁니다.

다음 셀은 실행 1에서 받은 답을 봅니다."""),
        code(SHOW1_ANSWERS),
        md("""**결과 읽기** — 라벨 줄 `번호 | 받은 답` 아래 두 줄이 모델이 쓴 답입니다.
셋째 질문은 예약에서 멈춰 답이 없습니다.

이번 실행에서는 두 답 모두 안내 문서 `E01`의 휴관일 내용으로 한 문장을 쓰고 끝에 `[E01 p.1]`을 적었습니다.
새 커널로 두 번 실행했을 때 두 답은 글자까지 같았습니다.
그래도 모델이 쓴 글이라 여러분 실행에서는 다를 수 있습니다.
이 실습은 답 문장을 기록에도 결론에도 쓰지 않습니다.

다음 셀은 기록 목록 전체를 JSON 글로 펴서 가짜 값 원문이 남았는지 봅니다.
02절 함수 `find_raw_values`로 찾고, 코드가 정한 값이라 `assert`로도 확인합니다."""),
        code(CHECK1),
        md("""**결과 읽기** — 출력 줄 `기록에 남은 원문 값: []`으로 세 줄 어디에도 가짜 값 원문은 없습니다.
마지막 줄의 `assert`도 통과했습니다.
멈춘 질문의 기록도 기록 장치가 먼저 가려서 원문 값이 들어가지 않았습니다.

## 7. 실행 2 · 호출 한도 1

실행 2는 호출 한도 하나만 2에서 1로 바꿉니다.
질문 셋, 비용 상한, 예상 비용, 소금값, 조립 함수는 실행 1과 같습니다.
실행 전에 예상해 봅니다.
첫째 질문만 모델에 가고, 둘째와 셋째 질문은 예약에서 멈출 것입니다.
기록은 여전히 세 줄이고, 이 셀에서 모델 요청은 한 번 나갑니다."""),
        code(RUN2),
        md("""**결과 읽기** — 출력 줄 `멈춘 까닭: 호출 한도를 넘습니다.`가 두 번 보입니다.
출력 줄 `받은 답 수: 1`과 `예약한 호출 수: 1`로 모델 요청은 한 번 나갔습니다.
출력 줄 `기록 줄 수: 3`으로 멈춘 질문 둘까지 세 줄이 남았습니다.
예상과 같습니다.

다음 셀은 실행 2의 기록 목록을 봅니다."""),
        code(SHOW2_ROWS),
        md("""**결과 읽기** — 라벨 줄 `번호 | 사건 | 가린 질문` 아래에서 번호 0 줄만 사건 `answer`입니다.
번호 1과 2 줄은 사건 `stopped`이고, 두 줄 모두 기록 칸에 `'reserved_calls': 1`이 있습니다.
멈춘 둘째 질문도 전화번호가 `<PHONE_MASKED>`로 가려진 채 남았습니다.

다음 셀은 실행 1처럼 기록 목록에 가짜 값 원문이 남았는지 봅니다."""),
        code(CHECK2),
        md("""**결과 읽기** — 출력 줄 `기록에 남은 원문 값: []`으로 실행 2의 기록에도 원문 값은 없습니다.
마지막 줄의 `assert`도 통과했습니다.

## 8. 두 실행 견주기

다음 셀은 두 실행을 한 표로 나란히 봅니다.
멈춘 질문 수는 기록 줄 수에서 받은 답 수를 빼서 셉니다."""),
        code(COMPARE),
        md("""**결과 읽기** — 라벨 줄 `실행 | 호출 한도 | 받은 답 수 | 멈춘 질문 수 | 기록 줄 수` 아래 두 줄이 두 실행입니다.
줄 `실행 1 | 2 | 2 | 1 | 3`과 `실행 2 | 1 | 1 | 2 | 3`을 견줍니다.
호출 한도를 하나 줄이자 받은 답이 하나 줄고, 멈춘 질문이 하나 늘었습니다.
기록 줄 수는 두 실행 모두 3이라, 질문마다 한 줄씩 남았습니다.

다음 셀은 두 실행의 기록을 번호마다 짝지어 봅니다.
두 실행은 같은 질문을 같은 차례로 처리했으므로 같은 번호 줄이 같은 질문입니다.
그 사실을 칸 `query_hash`의 지문이 같은지로 확인합니다."""),
        code(PAIR),
        md("""**결과 읽기** — 라벨 줄 `번호 | 같은 지문인가 | 실행 1 사건 | 실행 2 사건` 아래 세 줄 모두 `True`입니다.
같은 소금값으로 같은 가린 질문의 지문을 만들었기 때문입니다.
줄 `1 | True | answer | stopped`에서만 두 실행의 사건 이름이 다릅니다.

이번에는 두 기록의 차례가 같아 번호로 짝지었습니다.
지문이 같은지로 그 짝이 맞는지 확인했고, 짝짓는 데 원문 질문은 쓰지 않았습니다.

다음 셀은 사건 이름이 달라진 줄의 가린 질문만 모읍니다.
비교 `!=`는 두 값이 다를 때 참입니다."""),
        code(CHANGED),
        md("""**결과 읽기** — 출력 줄 `사건이 달라진 줄 수: 1`로 달라진 줄은 하나입니다.
출력 줄 `달라진 질문(가린 글):` 뒤 목록이 그 줄의 가린 질문이고, 전화번호가 든 둘째 질문입니다.
원문 전화번호를 보지 않고도 어느 질문의 결과가 바뀌었는지 찾았습니다.

## 정리

1. 상담 질문 셋을 02절 `mask_pii`로 가린 뒤 04절 `reserve`로 예약하고, 예약된 질문만 모델에 보냈습니다.
2. 답을 받은 질문도 예약에서 멈춘 질문도 05절 칸 넷으로 기록 목록에 한 줄씩 남겼고, 원문 값은 없었습니다.
3. 호출 한도를 2에서 1로 줄이자 둘째 질문도 멈췄고, 지문으로 짝지은 기록에서 그 줄을 찾았습니다.

이 절로 Ch 16이 끝납니다. 다음은 Ch 17 Agent 개요입니다."""),
    ]


SRC_HTML = """<!--meta: 실습 30분 | 코드 notebooks/07-가드레일-실습.ipynb | 새 용어 0 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>02·04·05절 함수로 상담 질문마다 가리기·예약·감사 기록을 한 흐름으로 이을 수 있습니다.</li>
<li>예약에서 멈춘 질문도 가린 글로 기록 목록에 남길 수 있습니다.</li>
<li>호출 한도 하나만 바꿔 다시 실행하고 두 실행의 결과를 견줄 수 있습니다.</li>
<li>두 실행의 기록을 지문으로 짝지어 결과가 달라진 질문을 원문 없이 찾을 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>도서관 상담 창구에는 하루에도 여러 질문이 들어옵니다. 사용자는 질문에 연락처나 카드 번호를 함께 적기도 합니다. 창구는 질문마다 개인정보를 가린 뒤 모델을 부릅니다. 모델 요청은 정한 호출 한도 안에서만 하고, 한 일은 모두 기록합니다.</p>
<p>02절 가리기, 04절 예약, 05절 감사 기록은 각 절에서 따로 배웠습니다. 이번 실습은 셋을 한 조립 함수로 이어 질문 셋에 차례로 겁니다. 예약에서 멈춘 질문도 기록에 남겨, 기록만 보고 무슨 일이 있었는지 알 수 있게 합니다.</p>
<p>이번 절은 이 챕터의 실습입니다. 01~06절에서 쓴 이름과 문법만 쓰고 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p>
<p><strong>이 절의 질문</strong> — 호출 한도 하나를 바꾸면 기록 목록의 어느 줄이 달라지고, 그 줄을 원문 없이 찾을 수 있을까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>이번 실습은 아래 절에서 배운 것을 도구 파일 <code>guardrails.py</code>에서 그대로 가져옵니다.</p>
<table><thead><tr><th>절</th><th>배운 것</th><th>실습에서 쓰는 곳</th></tr></thead><tbody>
<tr><td>02절</td><td>개인정보 네 가지를 표식으로 가리는 <code>mask_pii()</code>, 원문 값을 찾는 <code>find_raw_values()</code>, 가짜 값</td><td>노트북 3절 질문 가리기, 5절 조립 함수 첫 줄, 6·7절 기록 원문 확인</td></tr>
<tr><td>04절</td><td>예산 <code>make_budget()</code>과 예약 <code>reserve()</code>, 정한 값(호출 한도 2·비용 상한 0.01달러·예상 비용 0.002달러)</td><td>노트북 3절 정한 값, 5절 조립 함수, 6·7절 두 실행</td></tr>
<tr><td>05절</td><td>감사 기록 한 줄의 칸 넷, 지문 <code>fingerprint_of()</code>와 <code>safe_detail()</code>, 소금값, 사건 이름 <code>answer</code>·<code>stopped</code></td><td>노트북 4절 기록 장치 <code>note_event()</code>, 8절 지문으로 짝짓기</td></tr>
<tr><td>06절</td><td>문서 구역 메시지 <code>build_rag_messages()</code></td><td>노트북 3절 메시지 미리 보기, 5절 조립 함수</td></tr>
</tbody></table>
<p>받은 오류에 이름을 붙이는 <code>except ValueError as error</code>는 03절에서 썼습니다. 일곱 함수 모두 앞 절에서 쓰던 인자 그대로입니다.</p>
<p>세 절을 고른 까닭은 이렇습니다. 상담 창구가 질문마다 꼭 할 일은 개인정보 가리기, 호출 한도 지키기, 한 일 남기기입니다. 이 셋이 02·04·05절 기능입니다. 06절 함수는 보낼 메시지를 만드는 데만 씁니다.</p>
<p>다른 절의 기능은 쓰지 않습니다. 01절 입력 검사와 출력 검사는 06절 한 흐름에 이미 들어 있습니다. 게다가 출력 검사는 모델이 적은 표시에 결과가 달려 있습니다. 03절 자르기와 요약은 질문이 하나씩 따로 오는 창구라 대화 기록이 없어 쓰지 않습니다. 05절 재시도와 예비 흐름은 실패 흉내를 다시 만들어야 해서 쓰지 않습니다.</p>
<p>06절 문서 검사와 격리도 쓰지 않습니다. 06절에서 이번 모델은 숨은 지시문을 따르지 않았고, 이 실습은 안내 문서 <code>E01</code>만 씁니다. 06절 함수 <code>guarded_generate()</code>를 그대로 부르면 06절을 되풀이하게 됩니다. 그래서 멈춘 질문까지 기록하는 조립 함수를 새로 적습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3>
<p>01절 탁자에 앞 절 소품을 함께 놓아 봅니다. 쪽지 셋은 상담 질문이고, 쪽지마다 02절 덮개 천이 적어 둔 연락처를 덮습니다. 쪽지는 04절 개찰구의 회전 막대를 지나야 안으로 들어갑니다. 무엇을 했는지는 뒤쪽 대장에 한 줄씩 적습니다.</p>
{{img:""" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + """}}
<p class="look"><b>그림 읽기</b> — """ + ILLU_READ + """</p>
<p class="look">막대를 지난 쪽지 둘은 모델에 간 질문이고, 막대 앞의 쪽지 하나는 예약에서 멈춘 질문입니다. 대장의 줄 셋은 실행 1의 기록 세 줄이고, 멈춘 쪽지도 한 줄을 남깁니다. 천은 쪽지가 개찰구에 닿기 전부터 덮여 있습니다. 질문을 먼저 가린 뒤 예약하는 차례와 같습니다.</p>
<h3>실습 조립의 구성</h3>
{{mermaid:""" + FIG1 + "|" + FIG1_ALT + "|" + FIG1_CAP + """}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 초록 상담 질문 셋이 파란 가리기와 예약을 차례로 지납니다. 예약에서 왼쪽 실선은 보라 모델로 가고, 답을 받으면 파란 기록 한 줄 남기기 상자에서 <code>answer</code> 한 줄을 남깁니다. 오른쪽 점선은 호출 한도를 넘을 때만 가는 갈래이고, 모델을 거치지 않고 <code>stopped</code> 한 줄을 남깁니다. 두 기록 상자는 맨 아래 초록 기록 목록으로 모이고, 이 목록은 파일에 쓰지 않습니다.</p>
<table><thead><tr><th>함수</th><th>하는 일</th><th>가져온 곳</th></tr></thead><tbody>
<tr><td><code>note_event()</code></td><td>기록 한 줄(칸 넷)을 만들어 목록에 더함, 파일에는 쓰지 않음</td><td>05절 <code>record_event()</code>에서 파일을 다시 쓰는 줄만 뺌</td></tr>
<tr><td><code>print_rows()</code></td><td>기록 목록을 한 줄씩 출력</td><td>이 절의 기록 장치</td></tr>
<tr><td><code>serve_question()</code></td><td>질문 하나를 가리고 예약한 뒤 모델에 보내고, 기록 한 줄을 남김</td><td>02·04·05절 함수를 이 절이 묶은 조립 함수</td></tr>
<tr><td><code>serve_all()</code></td><td>질문 목록을 차례로 처리, 예약에서 멈춘 질문은 <code>stopped</code>로 기록하고 다음 질문으로 넘어감</td><td>04절 <code>ask_all()</code>과 달리 멈춘 뒤에도 이어 감</td></tr>
</tbody></table>
<h3>멈춘 질문도 기록하기</h3>
<p>04절 함수 <code>ask_all()</code>은 예약이 막히면 그 자리에서 멈췄습니다. 06절 함수 <code>guarded_generate()</code>는 예약에서 막히면 기록 없이 오류만 올리는 모양입니다. 이번에는 <code>serve_all()</code>이 예약에서 막힌 질문도 사건 <code>stopped</code>로 한 줄 남깁니다. 그 줄에는 가린 질문과 멈춘 까닭, 예약한 호출 수가 들어갑니다.</p>
<p>기록 장치 <code>note_event()</code>는 05절 <code>record_event()</code>처럼 받은 질문을 먼저 가립니다. 그래서 멈춘 질문의 기록에도 원문 값은 들어가지 않습니다. 기록 목록만 보고도 어느 질문이 왜 멈췄는지 알 수 있습니다.</p>
<h3>두 번의 실행</h3>
<p>실행 1은 04절 값 그대로 호출 한도 2로 질문 셋을 처리합니다. 실행 2는 호출 한도 하나만 1로 바꿉니다. 질문 셋, 비용 상한, 예상 비용, 소금값, 조립 함수는 두 실행이 같습니다.</p>
<p>두 실행은 같은 질문을 같은 차례로 처리합니다. 같은 소금값으로 같은 가린 질문의 지문을 만들므로, 같은 질문의 줄은 지문이 같을 것입니다. 이 지문으로 두 기록의 줄을 짝지어 결과가 달라진 질문을 찾습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2>
<p>노트북은 먼저 자료 파일에서 안내 문서 <code>E01</code>을 고르고 상담 질문 셋을 적습니다. 질문 셋을 가려 보고, 모델에 보낼 메시지 모양을 봅니다. 기록 장치 둘과 조립 함수 둘을 만든 뒤 실행 1과 실행 2를 차례로 합니다. 마지막에 두 실행을 한 표로 견주고, 기록을 지문으로 짝짓습니다.</p>
<p>실제 OpenAI 모델을 부릅니다. 교재 출력은 """ + RUN_DATE + """에 실행한 결과입니다. 모델 요청은 실행 1이 두 번, 실행 2가 한 번으로 모두 세 번이고 임베딩 요청은 없습니다. 노트북을 한 번 실행하는 요금은 요금표로 어림해 미화 0.01달러 아래이고, 청구 금액과는 다를 수 있습니다. 새로 쓰는 파일은 없습니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — 실행 1과 실행 2의 <code>받은 답 수:</code>·<code>예약한 호출 수:</code>·<code>기록 줄 수:</code> 줄을 견줍니다. 두 실행의 <code>기록에 남은 원문 값: []</code> 줄을 봅니다. 노트북 8절 <code>사건이 달라진 줄 수: 1</code>도 확인합니다.</p>
<h3>실행 1의 실제 순서</h3>
{{mermaid:""" + FIG2 + "|" + FIG2_ALT + "|" + FIG2_CAP + """}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽으며, 맨 왼쪽 세로줄이 이 절의 두 함수이고 오른쪽으로 예산·모델·기록 목록이 있습니다. 첫째와 둘째 질문은 예약한 뒤 가린 질문을 모델에 보내고, 기록 목록에 <code>answer</code> 한 줄을 남깁니다. 함수 <code>reserve</code>는 값을 내놓지 않고 예산 칸만 고치므로, 그 칸 값은 예산 아래 노란 메모에 적었습니다. 셋째 질문은 예산에서 <code>ValueError</code>를 받아 모델로 가지 않고 <code>stopped</code> 한 줄만 남깁니다. 나머지 노란 메모 둘은 출력으로 확인한 멈춘 까닭과 기록 줄 수·원문 값 없음입니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2>
<p>두 실행은 호출 한도 하나만 달랐습니다.</p>
<table><thead><tr><th>실행</th><th>호출 한도</th><th>받은 답 수</th><th>멈춘 질문 수</th><th>기록 줄 수</th><th>모델 요청 수</th></tr></thead><tbody>
<tr><td>실행 1</td><td>2</td><td>2</td><td>1</td><td>3</td><td>2</td></tr>
<tr><td>실행 2</td><td>1</td><td>1</td><td>2</td><td>3</td><td>1</td></tr>
</tbody></table>
<p>호출 한도를 하나 줄이자 받은 답이 하나 줄고 멈춘 질문이 하나 늘었습니다. 기록 줄 수는 두 실행 모두 3이었습니다. 답을 받았든 멈췄든 질문마다 한 줄씩 남겼기 때문입니다.</p>
{{mermaid:""" + FIG3 + "|" + FIG3_ALT + "|" + FIG3_CAP + """}}
<p class="look"><b>도식 읽기</b> — 위쪽 두 칸이 두 실행이고 왼쪽이 실행 1, 오른쪽이 실행 2입니다. 칸마다 노란 상자에 받은 답 수, 예약한 호출 수, 사건 이름별 줄 수를 적었습니다. 두 칸에서 내려온 화살표는 노트북 8절에서 두 기록을 짝지은 결과인 가운데 노란 상자로 모입니다. 맨 아래 회색 상자는 두 실행의 출력에서 모두 확인한 조건과 값이라 어느 칸에도 넣지 않았습니다.</p>
<p>두 기록을 번호마다 짝지으면 세 줄 모두 지문이 같았습니다. 사건 이름이 달라진 줄은 하나였고, 전화번호가 든 둘째 질문이었습니다. 그 줄은 가린 글로만 찾았으므로 원문 전화번호는 보지 않았습니다.</p>
<p>두 실행의 기록 목록 어디에도 가짜 값 원문은 없었습니다. 멈춘 질문의 기록도 가린 글이었습니다. 기록 장치가 받은 질문을 먼저 가렸기 때문입니다. 새 커널로 두 번 실행했을 때 표와 기록 목록의 값은 두 번 모두 같았습니다.</p>
<p>모델이 쓴 답 문장은 기록에도 결론에도 쓰지 않았습니다. 답 문장은 노트북 6절 출력에만 있고, 실행마다 달라질 수 있습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2>
<ul>
<li><strong>질문과 가짜 값은 실행 전에 정했습니다.</strong> 질문 셋은 이 절에서 적은 글이고, 가짜 값 셋은 02절에서 지어낸 값입니다. 실제 사람의 정보가 아닙니다.</li>
<li><strong>예산 값은 04절에서 정한 값입니다.</strong> 호출 한도 2, 비용 상한 0.01달러, 요청 하나의 예상 비용 0.002달러입니다. 요금표로 센 값이 아니고 청구 금액도 아닙니다.</li>
<li><strong>이 실습은 파일을 쓰지 않습니다.</strong> 기록 목록은 노트북 안에만 있어 커널을 다시 시작하면 사라집니다. 파일에 남기려면 05절 <code>record_event()</code>를 씁니다.</li>
<li><strong>가리기는 02절 정규식 넷이 찾는 모양만 가립니다.</strong> 이름·주소처럼 정규식 밖 개인정보는 이번에 다루지 않았습니다.</li>
<li><strong>모델 답에는 01절 출력 검사를 걸지 않았습니다.</strong> 답의 출처 표시가 맞는지는 이번에 보지 않았습니다.</li>
<li><strong>재시도와 예비 흐름, 문서 검사와 격리는 넣지 않았습니다.</strong> 05절과 06절에서 따로 살펴본 부분입니다.</li>
<li><strong>예약은 요청을 보내기 전에 적습니다.</strong> 요청이 실패해도 예약은 그대로 남지만, 이번 두 실행에서 실패한 요청은 없었습니다.</li>
<li><strong>모델이 쓴 답은 실행마다 달라질 수 있습니다.</strong> 답에는 <code>assert</code>를 쓰지 않았고, 기록 목록처럼 코드가 정한 값에만 썼습니다.</li>
<li><strong>걸린 시간과 실제 비용은 재지 않았습니다.</strong> 요청 수와 요금 어림만 준비물에 적었습니다.</li>
<li><strong>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.</strong> 패키지는 langchain 1.4.0과 langchain-openai 1.6.1과 python-dotenv 1.2.3입니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li>
</ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2>
<ul>
<li>상담 질문 셋을 02절 <code>mask_pii()</code>로 가린 뒤 04절 <code>reserve()</code>로 예약하고, 예약된 질문만 모델에 보냈습니다.</li>
<li>답을 받은 질문도 예약에서 멈춘 질문도 05절 칸 넷으로 기록 목록에 한 줄씩 남겼습니다.</li>
<li>호출 한도를 2에서 1로 줄이자 받은 답이 하나 줄고, 둘째 질문도 멈췄습니다.</li>
<li>두 기록을 지문으로 짝지어 결과가 달라진 줄을 원문 없이 찾았습니다.</li>
</ul>
<p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 16이 끝납니다. 다음은 Ch 17 Agent 개요입니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>
<details class="quiz" open><summary>문제 4개 · 해설 포함</summary>
<p class="quiz-q">1. [하] 두 실행에서 바꾼 값은 무엇입니까?</p>
<p class="quiz-a">호출 한도 하나입니다. 실행 1은 2이고 실행 2는 1입니다. 질문 셋과 비용 상한, 예상 비용, 소금값, 조립 함수는 같게 두었습니다.</p>
<p class="quiz-q">2. [중] 실행 1에서 예약에서 멈춘 셋째 질문의 기록에도 카드 번호 원문이 없는 까닭은 무엇입니까?</p>
<p class="quiz-a">기록 장치 <code>note_event()</code>가 05절 <code>record_event()</code>처럼 받은 질문을 먼저 가린 뒤 한 줄을 만들기 때문입니다. 멈춘 질문을 원문 그대로 넘겨도 기록에는 가린 글만 남습니다. 틀렸다면 노트북 4절과 5절을 다시 읽습니다.</p>
<p class="quiz-q">3. [중] 두 실행 모두 기록 줄 수가 3인 까닭은 무엇입니까?</p>
<p class="quiz-a">함수 <code>serve_all()</code>이 예약에서 멈춘 질문도 사건 <code>stopped</code>로 한 줄 남기기 때문입니다. 멈춘 뒤에도 다음 질문으로 넘어가므로 질문마다 한 줄씩 남습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p>
<p class="quiz-q">4. [상] 동료가 「기록에서 어느 질문이 바뀌었는지 보려면 원문 질문을 기록에 남겨야 한다」라고 말합니다. 이 절 출력으로 무엇이라고 답하나요?</p>
<p class="quiz-a">원문 없이도 찾을 수 있다고 답합니다. 같은 소금값으로 같은 가린 질문의 지문을 만들면 두 기록의 같은 질문 줄은 지문이 같습니다. 이 절은 지문이 같은 줄끼리 짝지어 사건 이름이 달라진 둘째 질문을 가린 글로만 찾았습니다.</p>
</details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2>
<ul>
<li>Ch 16 02절 — 개인정보 네 가지를 가리는 함수와 가짜 값을 만든 자리.</li>
<li>Ch 16 04절 — 예산과 예약 함수, 이 실습이 쓴 호출 한도와 예상 비용을 정한 자리.</li>
<li>Ch 16 05절 — 감사 기록 한 줄의 칸 넷과 지문, 사건 이름 <code>answer</code>·<code>stopped</code>를 만든 자리.</li>
<li>Ch 16 06절 — 문서 구역 메시지를 만드는 함수와 한 흐름을 만든 자리.</li>
<li>기준 버전은 langchain 1.4.0과 langchain-openai 1.6.1, python-dotenv 1.2.3입니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.</li>
</ul>
"""


def write_src() -> Path:
    SRC.write_text(SRC_HTML, encoding="utf-8")
    return SRC


if __name__ == "__main__":
    if os.environ.get("AUTHOR07_NB_ONLY") != "1":
        print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "07", SLUG, "experiment", cells())
        print("wrote", path)
