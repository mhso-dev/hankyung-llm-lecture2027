"""Ch 16 02절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§6).

사용:
  python3 author_02.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_02.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
  AUTHOR02_NB_ONLY=1 python3 author_02.py → 노트북만 다시 쓴다(그림을 그리기 전 새 커널 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다. **paired 형식 유지**(chapter.json).
**서비스 모델 절이다.** 설명만 고칠 때는 이 파일을 다시 실행하지 말고 mdpatch.py → run_section.sh --no-exec(규격 §3).

## 결정 1 — 개인정보 네 가지와 가짜 값 (챕터 리드 결정 2)

이메일·전화번호·주민등록번호·카드 번호 넷. 값은 모두 이 절에서 지어낸 가짜이고 가짜임이 드러나게 정했다.
`test.user@example.com`(예시용 이름 example.com) · `010-0000-0000`(가운데·끝 0) ·
`123456-1234567`(앞자리 34월 56일, 뒷자리 1~7 차례) · `1111-2222-3333-4444`(같은 숫자 네 자리씩).
옛 판의 `010-1234-5678`은 실제로 쓰일 수 있는 번호라 노트북에서 쓰지 않는다(테스트 2는 그대로).

## 결정 2 — `re`를 이 절이 처음 연다 (챕터 리드 결정 3)

`re.findall`·`re.sub`만, 정규식은 한 셀에 하나씩(이메일 → 전화번호 → 주민등록번호 → 카드 번호), 기호는 한 문장씩, 플래그 없음.
정규식 넷은 도구 파일 `PII_PATTERNS`와 글자까지 같다. 전화번호·주민등록번호·카드 번호 셋은
Ch 22 02 노트북 `PII_PATTERNS`와도 글자까지 같다(Ch 22 본문 「Ch16에서 쓴 전화번호 정규식을 detector 인자로」).
이메일은 Ch 22 판(`[\\w.+-]+@[\\w-]+\\.[\\w.]+`)보다 기호가 적은 `[\\w.]+@[\\w.]+`로 두었다(설명할 기호 수를 줄임).

## 결정 3 — 도구 파일과 같게 (규격 §2-7)

`mask_pii`는 이 절이 처음 가르치는 함수라 노트북 안에 적고, `notebooks/guardrails.py`의 `mask_pii`와 본문 줄이
글자까지 같다(주석 자리만 다름: 노트북은 셀 첫 줄, 도구 파일은 함수 안 첫 줄 「02절에서 배웠습니다」).
01절 함수 `validate_query`는 도구 파일에서 가져온다(이 챕터 첫 가져오기 → 고정 세 문장).
원문 값이 남았는지 찾는 `find_raw_values`는 이 절 노트북에만 있다(도구 파일에 넣지 않음).

## 결정 4 — paired 구성

Before(lesson_part="before") = 가리기 함수를 만들어 두고도 부르지 않은 흐름. 입력 검사를 지난 질문을 그대로
보낼 사용자 메시지와 기록 한 줄에 담는다 → 원문 값 넷씩(그림에서 빨강). 모델에는 보내지 않는다.
After(lesson_part="after") = 가린 질문으로 메시지·기록 한 줄을 만들고 가린 메시지만 모델에 보낸다 → 원문 값 0.
핵심 관찰(원문 값 수·종류별 개수)은 결정적이다. 모델 답에는 `assert`를 걸지 않는다.

## 결정 5 — 흔들림 확인 (규격 §2-7 10번 끝)

노트북 실행 전에 가린 메시지를 노트북 밖에서 다섯 번 보냈다(`qa/upgrade/02-probe.md`).
다섯 번 모두 같은 답(73자, 끝에 `[E01 p.1]`, 원문 값·표식 없음).

## 모델 요청

실행 한 번에 **1번**(`gpt-5.4-mini`, After 7절), 임베딩 0. 파일 쓰기 0번(자료 파일은 읽기만, 기록 한 줄은 글로만).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`key=`·`reverse=`·`set`·`setdefault`·`.get`·`+=`·기본값 매개변수·타입힌트·한 줄 다중 대입(`a, b = 1, 2`)·세미콜론·클래스 정의·
정규식 플래그(`re.I` 등)·`re.compile`·`re.subn`·앞뒤 경계(`(?<!…)`).
튜플 풀기(`masked_question, pii_counts = mask_pii(…)`)와 튜플 번호 꺼내기(`[0]`)는 처음 쓰는 자리에서 한 문장씩 풀었다.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part4/ch16-guardrails/notebooks"
SRC = ROOT / "textbook/part4/ch16-guardrails/_src/02-PII-마스킹.html"
SLUG = "02-PII-마스킹"

INSTALL = install_source(["langchain==1.4.0", "langchain-openai==1.6.1", "python-dotenv==1.2.3"])

IMPORTS = r'''# 파일을 읽을 이름, 정규 표현식 모듈, 01절 입력 검사 함수, 모델을 만들 이름을 불러옵니다
import json
import os
import re

from guardrails import validate_query
from langchain.chat_models import init_chat_model

print("불러온 이름:", "json", "os", "re", "validate_query", "init_chat_model")'''

ROOT_PATH = r'''# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part4/ch16-guardrails/data"):
        root_path = candidate
        break
print("찾은 프로젝트 맨 위:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

READ_PICK = r'''# 자료 파일을 읽고 이 절의 검색 결과로 안내 문서 E01 하나만 고릅니다(읽기만 합니다)
data_path = root_path + "/labs/part4/ch16-guardrails/data"
with open(data_path + "/retrieved-documents.json", encoding="utf-8") as file:
    all_documents = json.loads(file.read())
retrieved = []
for document in all_documents:
    if document["doc_id"] == "E01":
        retrieved.append(document)
print("자료 파일의 문서 수:", len(all_documents))
print("이번 검색 결과의 문서 수:", len(retrieved))'''

SETTINGS = r'''# 이 절에서 정한 값입니다: 01절과 같은 글자 수 상한·지킬 말과 검색 문서 한 줄입니다
max_chars = 500
system_text = "검색 문서에 있는 사실만 써서 한국어 한 문장으로 답하세요. 답 끝에 쓴 문서의 출처를 [문서ID p.쪽] 꼴로 적으세요."
document = retrieved[0]
document_line = "검색 문서 " + document["doc_id"] + " " + str(document["page"]) + "쪽: " + document["text"]
print("정한 질문 글자 수 상한:", max_chars)
print("검색 문서 한 줄:")
print(document_line)'''

FAKE = r'''# 이 절에서 지어낸 가짜 개인정보 넷입니다(실제 사람의 정보가 아닙니다)
fake_email = "test.user@example.com"
fake_phone = "010-0000-0000"
fake_rrn = "123456-1234567"
fake_card = "1111-2222-3333-4444"
fake_values = [fake_email, fake_phone, fake_rrn, fake_card]
print("가짜 값 수:", len(fake_values))
print("가짜 값:", fake_values)'''

DEF_RAW = r'''# 글 안에 원문 그대로 남은 가짜 값만 모읍니다
def find_raw_values(text, values):
    remaining = []
    for value in values:
        if value in text:
            remaining.append(value)
    return remaining'''

QUESTION = r'''# 가짜 값 넷을 넣은 질문을 만들고 01절 입력 검사에 겁니다
contact_line = "답은 " + fake_email + " 이나 " + fake_phone + " 으로 보내 주세요."
member_line = "주민등록번호는 " + fake_rrn + " 이고, 연체료는 카드 " + fake_card + " 로 내겠습니다."
question = "도서관 휴관일은 언제인가요? " + contact_line + " " + member_line
checked_question = validate_query(question, max_chars)
raw_in_question = find_raw_values(checked_question, fake_values)
print("입력 검사를 지난 질문:")
print(checked_question)
print("질문에 든 원문 값 수:", len(raw_in_question))'''

EMAIL = r'''# 이메일 모양 정규식으로 질문에서 이메일을 찾습니다
email_pattern = r"[\w.]+@[\w.]+"
print("이메일 정규식:", email_pattern)
print("찾은 이메일:", re.findall(email_pattern, checked_question))'''

PHONE = r'''# 휴대 전화번호 모양 정규식으로 질문에서 전화번호를 찾습니다
phone_pattern = r"01[016789]-?\d{3,4}-?\d{4}"
print("전화번호 정규식:", phone_pattern)
print("찾은 전화번호:", re.findall(phone_pattern, checked_question))'''

RRN = r'''# 주민등록번호 모양 정규식으로 질문에서 주민등록번호를 찾습니다
rrn_pattern = r"\d{6}-?[1-4]\d{6}"
print("주민등록번호 정규식:", rrn_pattern)
print("찾은 주민등록번호:", re.findall(rrn_pattern, checked_question))'''

CARD = r'''# 카드 번호 모양 정규식으로 질문에서 카드 번호를 찾습니다
card_pattern = r"\d{4}-\d{4}-\d{4}-\d{4}"
print("카드 번호 정규식:", card_pattern)
print("찾은 카드 번호:", re.findall(card_pattern, checked_question))'''

SUB = r'''# 질문의 이메일을 표식 <EMAIL_MASKED>로 바꿉니다
email_masked = re.sub(email_pattern, "<EMAIL_MASKED>", checked_question)
print("이메일만 바꾼 질문:")
print(email_masked)'''

LISTS = r'''# 정규식 넷과 종류 이름 넷을 같은 차례로 목록 둘에 담습니다
PII_PATTERNS = [email_pattern, phone_pattern, rrn_pattern, card_pattern]
PII_NAMES = ["email", "phone", "rrn", "card"]
print("정규식 수:", len(PII_PATTERNS))
print("종류 이름:", PII_NAMES)'''

DEF_MASK = r'''# 개인정보 네 가지를 표식으로 바꾸고 종류별 개수를 셉니다
def mask_pii(text):
    masked = text
    counts = {}
    for i in range(len(PII_NAMES)):
        mark = "<" + PII_NAMES[i].upper() + "_MASKED>"
        found = re.findall(PII_PATTERNS[i], masked)
        counts[PII_NAMES[i]] = len(found)
        masked = re.sub(PII_PATTERNS[i], mark, masked)
    return masked, counts'''

CALL_MASK = r'''# 입력 검사를 지난 질문을 가리고 종류별 개수와 남은 원문 값을 봅니다
masked_question, pii_counts = mask_pii(checked_question)
raw_in_masked = find_raw_values(masked_question, fake_values)
print("가린 질문:")
print(masked_question)
print("종류별 개수:", pii_counts)
print("가린 질문에 남은 원문 값 수:", len(raw_in_masked))'''

BEFORE_SEND = r'''# 가리지 않는 흐름입니다: 입력 검사를 지난 질문을 그대로 메시지에 담습니다(보내지는 않습니다)
raw_messages = [
    {"role": "system", "content": system_text},
    {"role": "user", "content": "질문: " + checked_question + "\n" + document_line},
]
raw_sent = find_raw_values(raw_messages[1]["content"], fake_values)
print("보낼 사용자 메시지:")
print(raw_messages[1]["content"])
print("보낼 사용자 메시지에 남은 원문 값 수:", len(raw_sent))'''

BEFORE_LOG = r'''# 가리지 않는 흐름입니다: 같은 질문을 그대로 기록 한 줄로 바꿉니다
raw_row = {"event": "question", "question": checked_question}
raw_log_line = json.dumps(raw_row, ensure_ascii=False)
raw_logged = find_raw_values(raw_log_line, fake_values)
print("기록 한 줄:")
print(raw_log_line)
print("기록 한 줄에 남은 원문 값 수:", len(raw_logged))'''

AFTER_SEND = r'''# 가린 질문으로 메시지를 만들고 원문 값이 남았는지 봅니다
masked_messages = [
    {"role": "system", "content": system_text},
    {"role": "user", "content": "질문: " + masked_question + "\n" + document_line},
]
masked_sent = find_raw_values(masked_messages[1]["content"], fake_values)
print("보낼 사용자 메시지:")
print(masked_messages[1]["content"])
print("보낼 사용자 메시지에 남은 원문 값 수:", len(masked_sent))'''

ASK = r'''# 가린 메시지만 모델에게 보냅니다(모델 요청 1번)
model_answer = model.invoke(masked_messages).text
answer_raw = find_raw_values(model_answer, fake_values)
print("모델이 쓴 답:")
print(model_answer)
print("답에 든 원문 값 수:", len(answer_raw))'''

AFTER_LOG = r'''# 가린 질문과 종류별 개수만 기록 한 줄로 바꿉니다
safe_row = {"event": "question", "question": masked_question, "pii": pii_counts}
safe_log_line = json.dumps(safe_row, ensure_ascii=False)
safe_logged = find_raw_values(safe_log_line, fake_values)
print("기록 한 줄:")
print(safe_log_line)
print("기록 한 줄에 남은 원문 값 수:", len(safe_logged))'''

COMPARE = r'''# 두 흐름에서 원문 값이 남은 수를 한 표로 나란히 봅니다
print("흐름 | 보낼 사용자 메시지 | 기록 한 줄")
print("가리지 않은 흐름 |", len(raw_sent), "|", len(raw_logged))
print("가린 흐름 |", len(masked_sent), "|", len(safe_logged))'''

HAND = r'''# 손으로 적은 글 둘로 가리기를 확인합니다(미리 정한 글이라 assert로 봅니다)
source_sample = "메일 test.user@example.com, 출처 [E01 p.1]"
particle_sample = "메일 test.user@example.com으로 주세요"
source_masked, source_counts = mask_pii(source_sample)
particle_masked = mask_pii(particle_sample)[0]
print("출처 표시가 든 글:", source_masked)
print("조사를 붙여 쓴 글:", particle_masked)
assert source_masked == "메일 <EMAIL_MASKED>, 출처 [E01 p.1]"
assert source_counts == {"email": 1, "phone": 0, "rrn": 0, "card": 0}'''

VALUE = r'''# 바꿀 값은 전화번호 모양 하나입니다: 질문의 번호를 빈칸으로 적은 모양으로 바꿔 가립니다
spaced_phone = "010 0000 0000"
spaced_question = checked_question.replace(fake_phone, spaced_phone)
spaced_masked, spaced_counts = mask_pii(spaced_question)
spaced_raw = find_raw_values(spaced_masked, [spaced_phone])
print("가린 질문:")
print(spaced_masked)
print("종류별 개수:", spaced_counts)
print("남은 원문 값 수:", len(spaced_raw))'''


FIG1 = "02-1-보내기-전과-남기기-전에-가리기"
FIG1_ALT = "위에서 아래로 읽는 그림으로 초록 상자 받은 질문 가짜 개인정보 넷에서 파란 상자 입력 검사 validate_query로, 다시 파란 상자 가리기 mask_pii 정규식 넷을 차례로로, 다시 노란 상자 가린 질문 표식 넷과 종류별 개수로 이어지고 거기서 화살표가 둘로 나뉘어 보라 상자 모델 gpt-5.4-mini 가린 메시지만 받음과 노란 상자 기록 한 줄 가린 질문과 개수로 가는 그림"
FIG1_READ = """위에서 아래로 읽습니다. 초록 질문이 파란 입력 검사와 파란 가리기를 차례로 지납니다.
노란 가린 질문에서 화살표가 둘로 나뉘어 보라 모델과 노란 기록 한 줄로 갑니다."""
FIG1_CAP = "질문은 입력 검사를 지난 뒤 가립니다. 모델과 기록 한 줄은 가린 질문만 받습니다."

FIG2 = "02-2-전화번호-정규식-한-칸씩"
FIG2_ALT = "위에서 아래로 파란 상자 다섯이 이어지는 그림으로 첫 상자는 01과 한 글자 016789 가운데 하나 맞은 글 010, 둘째 상자는 붙임표 자리 없어도 됨 맞은 글 붙임표, 셋째 상자는 숫자 서너 개 맞은 글 0000, 넷째 상자는 붙임표 자리 없어도 됨 맞은 글 붙임표, 다섯째 상자는 숫자 네 개 맞은 글 0000이고 맨 아래 노란 상자 찾은 전화번호 010-0000-0000으로 끝나는 그림"
FIG2_CAP = "전화번호 정규식은 다섯 규칙이 차례로 맞아야 번호 하나를 찾습니다."

FIG3 = "02-3-가리지-않은-흐름과-가린-흐름"
FIG3_ALT = "칸 둘이 나란히 있고 아래에 회색 상자가 있는 그림으로 왼쪽 Before 가리지 않고 쓰는 흐름 칸에서는 초록 상자 받은 질문 원문 값 넷에서 화살표가 둘로 나뉘어 빨간 상자 보낼 메시지 원문 값 넷과 빨간 상자 기록 한 줄 원문 값 넷으로 가고 오른쪽 After 가린 뒤에 쓰는 흐름 칸에서는 같은 질문을 넣은 파란 상자 받은 질문 가리기 mask_pii에서 화살표가 둘로 나뉘어 노란 상자 보낼 메시지 원문 값 없음과 노란 상자 기록 한 줄 원문 값 없음으로 가며 맨 아래 회색 상자에 두 칸에 넣은 질문은 같습니다가 적힌 그림"
FIG3_CAP = "같은 질문에서 가리지 않은 흐름은 두 곳에 원문 넷을 담았고, 가린 흐름은 원문을 담지 않았습니다."

FIG4 = "02-4-빈칸으로-적은-전화번호"
FIG4_ALT = "칸 둘이 나란히 있고 아래에 회색 상자가 있는 그림으로 붙임표로 적은 번호 칸에는 초록 상자 질문 속 번호 010-0000-0000에서 노란 상자 전화번호 하나를 찾음 표식으로 바뀜으로 이어지고 빈칸으로 적은 번호 칸에는 초록 상자 질문 속 번호 010 0000 0000에서 노란 상자 찾은 전화번호 없음 원문이 그대로 남음으로 이어지며 맨 아래 회색 상자에 두 칸 모두 같은 함수 mask_pii로 가림 나머지 세 값은 두 칸 모두 표식으로가 적힌 그림"
FIG4_CAP = "전화번호를 빈칸으로 적자 같은 정규식이 번호를 찾지 못해 원문이 남았습니다."

ILLU = "02-5-쪽지와-덮개-천"
ILLU_ALT = "흰 바탕 나무 탁자 위에 다섯 자리가 한 줄로 놓여 있고 첫째·셋째·다섯째 자리에는 물결 줄이 그어진 종이 쪽지가 보이며 둘째 자리는 둥근 주황 헝겊을 덧댄 파란 천이, 넷째 자리는 세모난 노란 헝겊을 덧댄 초록 천이 쪽지를 완전히 덮고 있고 탁자 뒤 오른쪽에 펼친 대장 한 권과 나무 손도장 하나가 작게 놓인 그림"
ILLU_CAP = "다섯 자리 가운데 둘만 천으로 덮였습니다. 천 위 헝겊 모양으로 무엇을 덮었는지만 알 수 있습니다."
ILLU_READ = "나무 탁자 위에 다섯 자리가 한 줄로 놓여 있습니다. 첫째·셋째·다섯째 자리는 물결 줄이 그어진 종이 쪽지입니다. 둘째 자리는 둥근 주황 헝겊을 덧댄 파란 천이, 넷째 자리는 세모난 노란 헝겊을 덧댄 초록 천이 덮고 있습니다. 천 아래 쪽지는 보이지 않습니다. 탁자 뒤 오른쪽에는 01절의 펼친 대장과 나무 손도장이 작게 놓여 있습니다."

TITLE = """# PII 마스킹

이 절은 질문에 든 개인정보(PII, personally identifiable information)를 가립니다.
가리기를 영어로 마스킹(masking)이라고 부릅니다.

**이 노트북에서 할 일**

1. 가짜 개인정보 넷이 든 질문을 만들고 01절 입력 검사에 겁니다.
2. 정규 표현식 넷으로 이메일·전화번호·주민등록번호·카드 번호를 찾아 표식으로 바꿉니다.
3. 가리지 않고 쓰는 흐름이 메시지와 기록 한 줄에 원문을 남기는 것을 봅니다(Before).
4. 가린 뒤에 보내고 남기면 두 곳 모두 원문이 남지 않는 것을 봅니다(After).

**준비물** — 이 절은 프로젝트 맨 위 폴더의 `.env`에 적어 둔 `OPENAI_API_KEY`를 씁니다.
모델 `gpt-5.4-mini`에 보내는 요청은 한 번이고 임베딩 요청은 없습니다.
노트북을 한 번 실행하는 요금은 요금표로 어림해 미화 0.01달러 아래입니다.
실제 청구 금액과는 다를 수 있습니다.

읽는 파일은 이 챕터 자료 파일 `data/retrieved-documents.json` 하나입니다.
새로 쓰는 파일은 없습니다.
교재 출력을 만든 실행에서는 노트북 전체가 약 3초 만에 끝났습니다.

질문에 넣은 개인정보 넷은 모두 이 절에서 지어낸 가짜 값입니다.
실제 사람의 정보는 쓰지 않습니다.

**기준 버전** — 첫 셀에서 LangChain 1.4.0과 langchain-openai 1.6.1을 설치합니다.
키를 읽는 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 4~6절을 읽습니다.
정규식으로 값을 찾아 가리고, 가리지 않은 흐름이 무엇을 남기는지 보는 자리입니다.
7절은 가린 뒤에 보내고 남기는 자리입니다.
8절 손 확인과 9절 값 바꿔 보기는 실습 시간에 실행합니다.

실습 폴더 `labs/part4/ch16-guardrails`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ,
           html="skip"),
        md("""## 1. 준비

첫 셀은 패키지 세 개를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 설치가 끝나면 판 번호 세 줄이 보입니다.
출력 줄 `langchain: 1.4.0`과 `langchain-openai: 1.6.1`이 실습 폴더 잠금과 같은 판입니다.
이 노트북의 출력은 """ + RUN_DATE + """에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름 다섯을 불러옵니다.
모듈 `re`는 파이썬에 들어 있는 정규 표현식 기능입니다.
이 과정에서 `re`를 쓰는 것은 이 절이 처음입니다.

앞에서 배운 함수는 `guardrails.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
이 절은 그 파일에서 01절 입력 검사 함수 `validate_query` 하나만 가져옵니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `불러온 이름: json os re validate_query init_chat_model`로 이름 다섯을 불러왔습니다.
함수 `validate_query`는 01절 노트북에서 정의한 함수와 같은 본문입니다.

## 2. 키와 모델 준비

이 절은 7절에서 가린 질문을 답 모델 `gpt-5.4-mini`에 한 번 보냅니다."""),
    ] + key_and_model_cells(
        "openai:gpt-5.4-mini",
        "temperature 값을 0으로 두어도 답 문장이 매번 같다고 보장하지는 않습니다.",
    ) + [
        md("""## 3. 자료와 이 절에서 정한 값

먼저 노트북을 연 자리에서 프로젝트 맨 위를 찾습니다.
01절과 같은 자리 찾기 셀입니다."""),
        setup(ROOT_PATH),
        md("""**결과 읽기** — 출력 줄 `찾은 프로젝트 맨 위:` 뒤에 점 하나나 위로 올라가는 자리가 보입니다.

다음 셀은 01절과 같은 자료 파일을 읽고 안내 문서 `E01` 하나를 고릅니다.
이 절의 검색 결과는 이 문서 하나입니다."""),
        code(READ_PICK),
        md("""**결과 읽기** — 출력 줄 `자료 파일의 문서 수: 2`로 자료 파일의 문서는 둘입니다.
출력 줄 `이번 검색 결과의 문서 수: 1`로 이 절은 안내 문서 하나만 씁니다.

다음 셀은 이 절에서 정한 값을 적습니다.
글자 수 상한과 시스템 메시지 글은 01절과 같습니다.
검색 문서 한 줄도 01절과 같은 모양으로 만듭니다."""),
        code(SETTINGS),
        md("""**결과 읽기** — 출력 줄 `정한 질문 글자 수 상한: 500`이 01절과 같은 상한입니다.
라벨 줄 `검색 문서 한 줄:` 아래 줄이 모델에게 함께 보낼 문서입니다.
이 문서에는 개인정보가 없습니다.
코드 첫 줄 주석의 「지킬 말」은 01절과 같은 시스템 메시지 글을 가리킵니다.

다음 셀은 이 절에서 지어낸 가짜 개인정보 넷을 적습니다.
실제 사람의 정보가 아니고, 가짜임이 드러나게 정한 값입니다."""),
        code(FAKE),
        md("""**결과 읽기** — 출력 줄 `가짜 값 수: 4`로 값은 넷입니다.
차례로 이메일, 휴대 전화번호, 주민등록번호, 카드 번호입니다.

이메일의 `example.com`은 문서 예시용으로 따로 떼어 둔 주소 이름입니다.
전화번호는 가운데와 끝자리가 모두 0입니다.
주민등록번호 앞자리 `123456`은 34월 56일이라 있을 수 없는 날짜입니다.
카드 번호는 같은 숫자를 네 자리씩 늘어놓아 모양만 맞췄습니다.

다음 셀은 글 안에 이 값이 원문 그대로 남았는지 찾는 함수입니다."""),
        code(DEF_RAW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `find_raw_values`는 글 하나와 값 목록을 받습니다.
값마다 조건 `value in text`로 글 안에 그 값이 그대로 들어 있는지 봅니다.
들어 있는 값만 새 목록에 담아 내놓습니다.

다음 셀은 가짜 값 넷을 넣은 질문을 만들고 01절 입력 검사에 겁니다.
휴관일을 묻고, 답을 받을 연락처와 주민등록번호·카드 번호를 함께 적은 질문입니다."""),
        code(QUESTION),
        md(r"""**결과 읽기** — 라벨 줄 `입력 검사를 지난 질문:` 아래 줄이 이 절의 질문입니다.
출력 줄 `질문에 든 원문 값 수: 4`로 가짜 값 넷이 모두 들어 있습니다.
01절 입력 검사는 빈칸과 글자 수만 보므로 이 질문을 막지 않았습니다.

휴관일을 답하는 데에는 이 넷이 하나도 필요하지 않습니다.
다음 소절부터 이 값을 찾아 가리는 방법을 배웁니다.

## 4. 정규 표현식으로 찾기

정규 표현식(regular expression)은 글자 모양을 적은 짧은 규칙입니다.
이 교재에서는 줄여서 정규식이라고도 부릅니다.
값을 하나하나 적는 대신 「숫자 셋, 붙임표, 숫자 넷」처럼 모양을 적어 찾습니다.
이 절 코드에서는 `r"…"` 꼴 글 하나가 정규식 하나입니다.

함수 `re.findall(정규식, 글)`은 글에서 정규식에 맞는 부분을 모두 찾아 목록으로 내놓습니다.
글 앞의 `r`은 역슬래시(`\`)를 글자 그대로 두라는 표시입니다.
정규식에는 역슬래시가 자주 들어가서 이 표시를 붙입니다.

첫 정규식은 이메일 모양입니다. 기호는 하나씩 봅니다.

- 대괄호 `[ ]`는 그 안에 적은 글자 가운데 한 글자에 맞습니다.
- 기호 `\w`는 글자·숫자·밑줄 가운데 한 글자이고, 한글 글자도 여기에 들어갑니다.
- 그래서 `[\w.]`는 그런 글자나 점 한 글자입니다. 대괄호 안의 점은 점 그대로입니다.
- 기호 `+`는 바로 앞 규칙이 한 번 이상 이어진다는 뜻입니다.
- 가운데 `@`는 골뱅이 글자 그대로입니다."""),
        code(EMAIL),
        md(r"""**결과 읽기** — 출력 줄 `찾은 이메일: ['test.user@example.com']`으로 질문에서 이메일 하나를 찾았습니다.
점이 섞인 글자 덩어리, 골뱅이, 다시 점이 섞인 글자 덩어리가 이어진 부분입니다.

둘째 정규식은 휴대 전화번호 모양입니다.

- 맨 앞 `01`은 글자 0과 1 그대로입니다.
- 대괄호 `[016789]`는 0·1·6·7·8·9 가운데 한 글자입니다.
- 기호 `?`는 바로 앞 글자가 없어도 되고 한 번 있어도 된다는 뜻입니다. 그래서 `-?`는 붙임표가 있어도 없어도 맞습니다.
- 기호 `\d`는 숫자 한 글자입니다.
- 중괄호 `{3,4}`는 바로 앞 규칙이 세 번이나 네 번 이어진다는 뜻입니다. 중괄호 `{4}`는 꼭 네 번입니다."""),
        code(PHONE),
        md(r"""**결과 읽기** — 출력 줄 `찾은 전화번호: ['010-0000-0000']`으로 전화번호 하나를 찾았습니다.
앞 세 글자 `010`이 `01[016789]`에 맞고, 붙임표 둘이 `-?` 자리에 맞았습니다.
가운데 `0000`과 끝 `0000`이 숫자 자리에 맞았습니다.

셋째 정규식은 주민등록번호 모양입니다.
앞 여섯 자리, 붙임표 자리, 뒤 일곱 자리 차례입니다.

- 대괄호 안의 `1-4`는 1부터 4까지 숫자 가운데 한 글자라는 뜻입니다.
- 뒷자리 첫 글자를 이 넷으로 좁혔습니다. 나머지 `\d{6}`과 `-?`는 앞에서 본 기호입니다."""),
        code(RRN),
        md(r"""**결과 읽기** — 출력 줄 `찾은 주민등록번호: ['123456-1234567']`로 값 하나를 찾았습니다.
뒷자리 첫 글자 1이 `[1-4]` 자리에 맞았습니다.

넷째 정규식은 카드 번호 모양입니다.
숫자 네 자리를 붙임표로 이어 네 번 적은 모양입니다.
새 기호는 없습니다.
이 정규식의 붙임표에는 `?`가 없어서 붙임표가 꼭 있어야 맞습니다."""),
        code(CARD),
        md("""**결과 읽기** — 출력 줄 `찾은 카드 번호: ['1111-2222-3333-4444']`로 값 하나를 찾았습니다.
정규식 넷이 질문에서 값을 하나씩 찾았습니다.

## 5. 표식으로 바꾸기

찾은 값은 표식으로 바꿉니다.
표식은 가린 자리에 종류 이름만 남긴 짧은 글입니다.
쪽지에 천을 덮고 천 위에 무엇을 덮었는지 표시하는 것과 같습니다.
이 절의 표식은 `<EMAIL_MASKED>`처럼 꺾쇠 안에 종류 이름을 적습니다.

함수 `re.sub(정규식, 바꿀 글, 글)`은 맞는 부분을 모두 바꾼 새 글을 내놓습니다.
먼저 이메일 하나만 바꿔 봅니다."""),
        code(SUB),
        md("""**결과 읽기** — 라벨 줄 `이메일만 바꾼 질문:` 아래 줄에서 이메일 자리가 `<EMAIL_MASKED>`로 바뀌었습니다.
전화번호·주민등록번호·카드 번호는 아직 원문 그대로입니다.
원래 질문 `checked_question`은 그대로 두고 바꾼 글은 `email_masked`에 담았습니다.

이제 정규식 넷을 한 번에 겁니다.
정규식과 종류 이름을 같은 차례로 목록 둘에 담습니다.
이름을 모두 대문자로 적은 것은 한 번 정하면 바꾸지 않는 값이라는 표시입니다."""),
        code(LISTS),
        md("""**결과 읽기** — 출력 줄 `정규식 수: 4`와 `종류 이름: ['email', 'phone', 'rrn', 'card']`가 두 목록입니다.
두 목록은 같은 번호 자리끼리 한 짝입니다.
0번 자리는 이메일 정규식과 이름 `email`이고, 3번 자리는 카드 번호 정규식과 이름 `card`입니다.

다음 셀은 가리기 함수 `mask_pii`입니다.
번호 `i`로 두 목록을 함께 돌며 정규식을 하나씩 겁니다.
정규식마다 `re.findall`로 맞는 값의 개수를 먼저 세고, 그다음 `re.sub`로 바꿉니다.
앞 정규식이 바꾼 글에 다음 정규식을 겁니다.

표식은 종류 이름을 대문자로 바꿔 `<`와 `_MASKED>` 사이에 넣어 만듭니다.
글 메서드 `upper()`는 영문 소문자를 대문자로 바꾼 새 글을 내놓습니다.
마지막 줄 `return masked, counts`는 가린 글과 개수 딕셔너리를 함께 내놓습니다.
쉼표로 이은 두 값은 튜플 하나로 묶여 나갑니다."""),
        code(DEF_MASK),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `mask_pii`는 글 하나를 받아 가린 글과 종류별 개수를 함께 내놓습니다.
개수 딕셔너리의 키는 종류 이름 넷입니다.

다음 셀은 입력 검사를 지난 질문을 이 함수로 가립니다.
왼쪽에 이름 둘을 쉼표로 적으면 함수가 내놓은 튜플의 두 값을 차례로 받습니다.
가린 글은 `masked_question`에, 개수 딕셔너리는 `pii_counts`에 담깁니다."""),
        code(CALL_MASK),
        md("""**결과 읽기** — 라벨 줄 `가린 질문:` 아래 줄에서 값 넷이 모두 표식으로 바뀌었습니다.
출력 줄 `종류별 개수: {'email': 1, 'phone': 1, 'rrn': 1, 'card': 1}`로 종류마다 하나씩 찾았습니다.
출력 줄 `가린 질문에 남은 원문 값 수: 0`으로 원문은 하나도 남지 않았습니다.

휴관일을 묻는 앞 문장은 그대로입니다.
표식 자리를 보면 어떤 종류의 값이 있었는지는 알 수 있습니다.

## 6. 가리지 않고 쓰는 흐름 (Before)""", lesson_part="before"),
        md("""Before 셀은 가리기 함수를 만들어 두고도 부르지 않은 흐름입니다.
입력 검사를 지난 질문 `checked_question`을 그대로 메시지와 기록 한 줄에 담습니다.
이 흐름은 보내기 직전에서 멈추고 실제로 모델에 보내지는 않았습니다.

먼저 모델에게 보낼 메시지를 만듭니다.
메시지 모양은 01절과 같은 역할 딕셔너리 두 개입니다.""", lesson_part="before"),
        code(BEFORE_SEND, lesson_part="before"),
        md("""**결과 읽기** — 라벨 줄 `보낼 사용자 메시지:` 아래 두 줄이 모델에게 갈 글입니다.
첫 줄 질문에 가짜 값 넷이 원문 그대로 있습니다.
출력 줄 `보낼 사용자 메시지에 남은 원문 값 수: 4`가 이 흐름의 결함입니다.
이대로 보내면 모델 서비스가 개인정보 넷을 그대로 받습니다.

다음 셀은 같은 질문을 기록 한 줄로 바꿉니다.
Ch 15 08절처럼 `json.dumps(…, ensure_ascii=False)`로 딕셔너리를 JSON 글 한 줄로 바꿉니다.
이 절은 기록을 파일에 쓰지 않고 글로만 만듭니다.""", lesson_part="before"),
        code(BEFORE_LOG, lesson_part="before"),
        md("""**결과 읽기** — 라벨 줄 `기록 한 줄:` 아래 줄에 가짜 값 넷이 원문 그대로 들어 있습니다.
출력 줄 `기록 한 줄에 남은 원문 값 수: 4`도 이 흐름의 결함입니다.
이 줄이 기록 파일에 들어가면 원문 넷이 그대로 남습니다.

가리기 함수는 5절에서 이미 만들었습니다.
함수를 만들어 두어도 보내는 코드와 남기는 코드가 부르지 않으면 원문이 나갑니다.

## 7. 가린 뒤에 보내고 남기는 흐름 (After)""", lesson_part="after"),
        md("""After 셀은 5절에서 가린 질문 `masked_question`을 씁니다.
메시지와 기록 한 줄에 원문 대신 표식이 들어갑니다.
먼저 모델에게 보낼 메시지를 만듭니다.""", lesson_part="after"),
        code(AFTER_SEND, lesson_part="after"),
        md("""**결과 읽기** — 라벨 줄 `보낼 사용자 메시지:` 아래 첫 줄에 표식 넷이 보입니다.
출력 줄 `보낼 사용자 메시지에 남은 원문 값 수: 0`으로 원문은 남지 않았습니다.

앞 6절 Before 셀에서는 `보낼 사용자 메시지에 남은 원문 값 수: 4`였습니다.

다음 셀은 가린 메시지만 모델에게 보냅니다.
이 셀에서 모델 요청이 한 번 나갑니다.""", lesson_part="after"),
        code(ASK, lesson_part="after"),
        md("""**결과 읽기** — 라벨 줄 `모델이 쓴 답:` 아래 줄이 모델 답입니다.
출력 줄 `답에 든 원문 값 수: 0`으로 답에도 원문 값이 없습니다.
모델이 받은 글에 원문이 없었기 때문입니다.

이 답은 모델이 쓴 글이라 여러분 실행에서는 문장이 다를 수 있습니다.
교재 출력을 만들기 전에 같은 요청을 따로 다섯 번 보냈습니다.
다섯 번 모두 같은 답이었고 끝에 출처 표시 `[E01 p.1]`이 붙었습니다.

다음 셀은 가린 질문과 종류별 개수만 기록 한 줄로 바꿉니다.
개수는 어떤 종류를 가렸는지 뒤에서 알아볼 때 씁니다.""", lesson_part="after"),
        code(AFTER_LOG, lesson_part="after"),
        md("""**결과 읽기** — 라벨 줄 `기록 한 줄:` 아래 줄에 표식 넷과 종류별 개수가 들어 있습니다.
출력 줄 `기록 한 줄에 남은 원문 값 수: 0`으로 기록에도 원문이 남지 않았습니다.

앞 6절 Before 셀에서는 `기록 한 줄에 남은 원문 값 수: 4`였습니다.

다음 셀은 두 흐름의 원문 값 수를 한 표로 나란히 봅니다.""", lesson_part="after"),
        code(COMPARE, lesson_part="after"),
        md("""**결과 읽기** — 라벨 줄 `흐름 | 보낼 사용자 메시지 | 기록 한 줄` 아래 두 줄이 두 흐름입니다.
출력 줄 `가리지 않은 흐름 | 4 | 4`로 가리지 않은 흐름은 두 곳 모두 원문 넷을 담았습니다.
출력 줄 `가린 흐름 | 0 | 0`으로 가린 흐름은 두 곳 모두 원문이 없습니다.
두 흐름은 같은 질문을 썼고 가리기를 불렀는지만 달랐습니다.

## 8. 손으로 적은 글로 확인하기

다음 셀은 손으로 적은 글 둘로 가리기를 확인합니다.
첫째 글에는 01절의 출처 표시 `[E01 p.1]`을 함께 적었습니다.
가리기가 출력 검사에 쓸 표시를 건드리면 안 되기 때문입니다.

둘째 글은 이메일 바로 뒤에 조사 「으로」를 붙여 썼습니다.
함수 결과 뒤의 `[0]`은 튜플의 첫째 값인 가린 글만 꺼냅니다.
미리 정한 글이라 결과를 `assert`로 확인할 수 있습니다.""", lesson_part="after"),
        code(HAND, lesson_part="after"),
        md(r"""**결과 읽기** — 출력 줄 `출처 표시가 든 글: 메일 <EMAIL_MASKED>, 출처 [E01 p.1]`에서 출처 표시가 그대로 남았습니다.
마지막 두 줄의 `assert`도 통과했습니다.

출력 줄 `조사를 붙여 쓴 글: 메일 <EMAIL_MASKED> 주세요`에서는 조사 「으로」까지 사라졌습니다.
기호 `\w`가 한글 글자도 한 글자로 보아 조사까지 이메일로 묶었기 때문입니다.
그래서 이 절의 질문은 이메일 뒤에 빈칸을 두었습니다.

## 9. 값 바꿔 보기 · 빈칸으로 적은 전화번호

바꿀 값은 질문 속 전화번호의 모양 하나입니다.
붙임표 대신 빈칸으로 적은 번호 `010 0000 0000`으로 바꾸고 같은 함수로 가립니다.
글 메서드 `replace(찾을 글, 바꿀 글)`는 찾은 글을 바꾼 새 글을 내놓습니다.

실행 전에 예상해 봅니다.
전화번호 정규식의 `-?` 자리는 붙임표만 받으므로 이 번호는 찾지 못할 것입니다.
나머지 셋은 5절처럼 하나씩 찾을 것입니다.""", lesson_part="after"),
        code(VALUE, lesson_part="after"),
        md("""**결과 읽기** — 라벨 줄 `가린 질문:` 아래 줄에 `010 0000 0000`이 원문 그대로 남았습니다.
출력 줄 `종류별 개수: {'email': 1, 'phone': 0, 'rrn': 1, 'card': 1}`로 전화번호만 0개입니다.
출력 줄 `남은 원문 값 수: 1`이 놓친 번호 하나입니다.

예상대로 정규식은 적어 둔 모양만 찾았습니다.
5절 출력에서는 `'phone': 1`이었습니다.
실제 입력에 어떤 모양이 들어오는지 먼저 보고 정규식을 정해야 합니다.

## 정리

1. 정규식 넷으로 이메일·전화번호·주민등록번호·카드 번호를 찾아 표식으로 바꿨습니다.
2. 가리지 않은 흐름은 보낼 메시지와 기록 한 줄에 원문 값 넷을 그대로 담았습니다.
3. 가린 흐름은 두 곳 모두 원문 값이 없었고, 빈칸으로 적은 전화번호는 찾지 못했습니다.

03절에서는 길어진 대화 기록을 자르는 방법과 요약하는 방법을 견줍니다.""", lesson_part="after"),
    ]


SRC_HTML = """<!--meta: 강의 0.5h | 실습 0.75h | 코드 notebooks/02-PII-마스킹.ipynb | 새 용어 4 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>정규 표현식으로 이메일·전화번호·주민등록번호·카드 번호의 모양을 찾을 수 있습니다.</li>
<li>모델에 보내기 전과 기록에 남기기 전에 개인정보를 표식으로 가릴 수 있습니다.</li>
<li>가리지 않은 흐름이 무엇을 남기는지 출력으로 설명할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>사용자는 질문에 자기 연락처나 주민등록번호·카드 번호를 함께 적곤 합니다. 01절의 입력 검사는 빈칸과 글자 수만 봅니다. 그래서 이메일이나 카드 번호가 든 질문도 그대로 검사를 지납니다.</p><p>그 질문을 그대로 쓰면 개인정보가 모델 서비스로 나갑니다. 질문을 적어 두는 기록에도 원문이 남습니다. 휴관일을 답하는 데에는 이 값들이 필요하지 않습니다. 이 절은 보내기 전과 남기기 전에 이런 값을 표식으로 바꿉니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>01절에서는 모델을 부르기 전에 질문을 입력 검사 <code>validate_query</code>에 걸었습니다. 빈칸을 정리하고, 빈 질문과 글자 수 상한을 넘는 질문을 막았습니다. 이 절은 그 함수를 도구 파일 <code>guardrails.py</code>에서 가져와 그대로 씁니다.</p><p>01절의 출력 검사는 답 끝 출처 표시 <code>[E01 p.1]</code>을 허용 목록과 견줬습니다. 이 절의 가리기는 그 표시를 건드리지 않아야 합니다. 노트북 8절의 손 확인 셀에서 이 점을 봅니다.</p><p>기록 한 줄은 Ch 15 08절처럼 <code>json.dumps(…, ensure_ascii=False)</code>로 만듭니다. 딕셔너리를 JSON 글 한 줄로 바꾸는 함수입니다. 정규 표현식은 이 과정에서 이 절이 처음 다룹니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절의 탁자에 이번에는 쪽지 다섯 장이 한 줄로 놓였다고 해 봅니다. 그 가운데 두 장에는 남에게 보이면 안 되는 번호가 적혀 있습니다. 그 두 장만 작은 천으로 덮고, 천 위에 무엇을 덮었는지 모양으로 표시합니다.</p><p>천을 덮어도 그 자리에 어떤 종류의 쪽지가 있었는지는 알 수 있습니다. 번호 자체는 보이지 않습니다. 쪽지를 옮기거나 대장에 적을 때도 천을 덮은 채로 다룹니다.</p>
{{img:""" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + """}}
<p class="look"><b>그림 읽기</b> — """ + ILLU_READ + """</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>개인정보(PII)</td><td>한 사람을 알아볼 수 있게 하는 값입니다. 이메일·전화번호·주민등록번호·카드 번호가 예입니다. 쪽지에 적힌 남의 번호와 같습니다.</td></tr><tr><td>가리기(마스킹, masking)</td><td>값을 종류만 알 수 있는 짧은 글로 바꾸는 일입니다. 쪽지 위에 천을 덮는 일과 같습니다.</td></tr><tr><td>정규 표현식(regular expression)</td><td>글자 모양을 적은 짧은 규칙입니다. 줄여서 정규식이라고도 부릅니다. 값 대신 「숫자 셋, 붙임표, 숫자 넷」처럼 모양을 적습니다.</td></tr><tr><td>표식</td><td>가린 자리에 넣는 짧은 글입니다. 값은 보이지 않고 종류 이름만 남습니다. 천 위의 모양 표시와 같습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 개인정보는 질문에 넣은 가짜 값 넷입니다. 정규식은 <code>r"01[016789]-?\\d{3,4}-?\\d{4}"</code> 같은 글입니다. 표식은 <code>&lt;PHONE_MASKED&gt;</code> 같은 글이고, 가리기는 함수 <code>mask_pii</code>가 합니다.</p>
{{mermaid:""" + FIG1 + "|" + FIG1_ALT + "|" + FIG1_CAP + """}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자가 받은 질문이고, 그 아래 파란 상자 둘이 입력 검사와 가리기입니다. 가리기를 지난 노란 상자가 가린 질문입니다. 거기서 화살표가 둘로 나뉘어 보라 모델과 노란 기록 한 줄로 갑니다. 두 곳 모두 가린 질문만 받습니다.</p>
<h3>가리는 자리는 보내기 전과 남기기 전입니다</h3><p>가리기는 값이 밖으로 나가거나 남기 전에 해야 합니다. 이 절은 두 자리를 봅니다. 하나는 모델에게 보낼 사용자 메시지이고, 다른 하나는 기록 한 줄입니다. 이미 보낸 뒤에 가리면 모델 서비스는 원문을 받은 뒤입니다.</p><p>함수를 만들어 두는 것만으로는 가려지지 않습니다. 보내는 코드와 남기는 코드가 그 함수를 불러야 합니다. 노트북 6절 Before는 가리기 함수를 만들어 두고도 부르지 않은 흐름입니다.</p>
<h3>정규식은 모양을 적은 규칙입니다</h3><p>정규식은 값 하나하나를 적지 않고 모양을 적습니다. 전화번호 정규식은 01과 한 글자, 붙임표 자리, 숫자 서너 개, 붙임표 자리, 숫자 네 개를 차례로 적은 규칙입니다. 이 모양에 맞는 글이면 어떤 번호든 찾습니다. 반대로 모양이 조금만 달라도 찾지 못합니다.</p>
<h3>다른 상황에 적용</h3><p>상담 챗봇이라면 상담 기록을 모델에게 요약시키기 전에 전화번호를 가릴 수 있습니다. 쇼핑몰 문의 분류라면 문의 글의 카드 번호를 가린 채 문의 종류만 고르게 합니다. 자리는 같습니다. 밖으로 보내기 전과 기록에 남기기 전입니다.</p>
<h3>비교와 경계</h3><p>정규식은 적어 둔 모양만 찾습니다. 노트북 9절처럼 빈칸으로 적은 전화번호는 놓칩니다. 사람 이름이나 주소처럼 모양이 정해지지 않은 개인정보는 이 절의 정규식으로 찾지 않았습니다. 가린 뒤에도 표식 자리에 어떤 종류가 있었는지는 드러납니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 01절과 같은 자료 파일에서 안내 문서 <code>E01</code> 하나를 고릅니다. 질문에는 이 절에서 지어낸 가짜 개인정보 넷을 넣습니다. 노트북 4절은 정규식 넷을 하나씩 적어 질문에서 값을 찾습니다. 노트북 5절은 네 정규식을 함수 <code>mask_pii</code> 하나로 묶어 질문을 가립니다.</p><p>가짜 값은 가짜임이 드러나게 정했습니다. 이메일의 <code>example.com</code>은 문서 예시용으로 따로 떼어 둔 주소 이름입니다. 전화번호는 가운데와 끝자리가 모두 0입니다. 주민등록번호 앞자리 <code>123456</code>은 34월 56일이라 있을 수 없는 날짜입니다. 카드 번호는 같은 숫자를 네 자리씩 늘어놓아 모양만 맞췄습니다.</p><p>모델 <code>gpt-5.4-mini</code>에 보내는 요청은 노트북 7절의 한 번이고 임베딩 요청은 없습니다. 노트북을 한 번 실행하는 요금은 요금표로 어림해 미화 0.01달러 아래입니다. 실제 청구 금액과는 다를 수 있습니다. 새로 쓰는 파일은 없습니다.</p>
{{notebook:""" + SLUG + """|example}}
<p class="look"><b>확인할 점</b> — 노트북 4절 출력에서 정규식마다 값을 하나씩 찾았는지 봅니다. 노트북 5절 출력 <code>종류별 개수: {'email': 1, 'phone': 1, 'rrn': 1, 'card': 1}</code>과 <code>가린 질문에 남은 원문 값 수: 0</code>을 봅니다.</p>
{{mermaid:""" + FIG2 + "|" + FIG2_ALT + "|" + FIG2_CAP + """}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 전화번호 정규식 <code>01[016789]-?\\d{3,4}-?\\d{4}</code>를 다섯 규칙으로 나눈 그림입니다. 파란 상자 다섯이 차례로 맞아야 맨 아래 노란 상자의 번호 하나를 찾습니다. 붙임표 자리 두 규칙은 붙임표가 없어도 맞습니다.</p>
<p>함수 <code>mask_pii</code>는 정규식 넷을 목록 차례대로 겁니다. 이메일, 전화번호, 주민등록번호, 카드 번호 차례입니다. 정규식마다 먼저 맞는 값의 개수를 세고 그다음 표식으로 바꿉니다. 앞 정규식이 바꾼 글에 다음 정규식을 겁니다.</p>
<h2 id="b6"><span class="no">6</span>실패 확인</h2><p>아래 Before 셀은 가리기 함수를 만들어 두고도 부르지 않은 흐름입니다. 입력 검사를 지난 질문을 그대로 메시지와 기록 한 줄에 담습니다. 이어지는 After 셀은 같은 질문을 가린 뒤에 담고, 가린 메시지만 모델에게 보냅니다.</p>
{{notebook:""" + SLUG + """|failure}}
{{mermaid:""" + FIG3 + "|" + FIG3_ALT + "|" + FIG3_CAP + """}}
<p class="look"><b>도식 읽기</b> — 왼쪽 칸이 Before이고 오른쪽 칸이 After입니다. 왼쪽 칸 맨 위 초록 상자가 받은 질문이고, 오른쪽 칸은 같은 질문을 맨 위 파란 가리기에 넣습니다. 왼쪽 빨간 상자 둘은 보낼 메시지와 기록 한 줄에 원문 넷이 남은 결함입니다. 오른쪽은 가리기를 지난 뒤라 노란 상자 둘에 원문이 없습니다. 모델 요청은 오른쪽 흐름에서만 한 번 보냈고 그림에는 넣지 않았습니다.</p>
<p>두 흐름은 같은 질문을 썼고 가리기를 불렀는지만 달랐습니다. 가리지 않은 흐름은 출력 줄 <code>가리지 않은 흐름 | 4 | 4</code>로 두 곳 모두 원문 넷을 담았습니다. 가린 흐름은 출력 줄 <code>가린 흐름 | 0 | 0</code>이었습니다.</p><p>Before 흐름은 보내기 직전에서 멈췄습니다. 원문이 든 메시지를 실제로 모델에 보내지는 않았습니다. 가린 메시지를 받은 모델의 답에서는 출력 줄 <code>답에 든 원문 값 수: 0</code>이 나왔습니다.</p><p>새 커널로 두 번 실행했을 때 원문 값 수와 종류별 개수는 두 번 모두 같았습니다. 모델이 쓴 답 문장은 실행마다 달라질 수 있어 본문에 옮기지 않았습니다.</p>
<p>값 바꿔 보기는 질문 속 전화번호의 모양 하나만 바꿉니다. 붙임표 대신 빈칸으로 적은 번호는 전화번호 정규식에 맞지 않았습니다. 출력 줄 <code>종류별 개수: {'email': 1, 'phone': 0, 'rrn': 1, 'card': 1}</code>로 전화번호만 찾지 못했습니다. 그 번호는 가린 질문에 원문 그대로 남았습니다.</p>
{{mermaid:""" + FIG4 + "|" + FIG4_ALT + "|" + FIG4_CAP + """}}
<p class="look"><b>도식 읽기</b> — 왼쪽 칸은 노트북 5절의 붙임표로 적은 번호이고, 오른쪽 칸은 노트북 9절의 빈칸으로 적은 번호입니다. 칸마다 초록 상자가 질문 속 번호이고 노란 상자가 가린 결과입니다. 왼쪽은 전화번호를 찾아 표식으로 바꿨고, 오른쪽은 찾지 못해 원문이 남았습니다. 맨 아래 회색 상자는 두 칸 모두 같은 함수로 가렸고 나머지 세 값은 두 칸 모두 표식이 되었다는 메모입니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>질문에 넣은 개인정보 넷은 모두 이 절에서 지어낸 가짜 값입니다. 실제 사람의 정보로 시험하지 않습니다. 카드 번호 <code>1111-2222-3333-4444</code>는 네 자리씩 모양만 맞춘 가짜 번호이고, 실제 카드 발급 규칙과는 무관합니다.</li><li>정규식은 적어 둔 모양만 찾습니다. 빈칸으로 적은 전화번호는 찾지 못했습니다. 실제 입력 예시로 먼저 확인합니다.</li><li>사람 이름과 주소처럼 모양이 정해지지 않은 개인정보는 이번에 다루지 않았습니다. 이런 값은 정규식만으로 찾기 어렵습니다.</li><li>기호 <code>\\w</code>는 한글 글자도 한 글자로 봅니다. 이메일 바로 뒤에 조사를 붙여 쓴 글에서는 조사까지 가려졌습니다. 그래서 이 절의 질문은 값 뒤에 빈칸을 두었고, 흐름을 보여 주려고 정한 예입니다.</li><li>이 절의 이메일 정규식은 모양을 넓게 잡았습니다. 골뱅이 앞뒤가 글자와 점이면 이메일로 봅니다.</li><li>정규식 넷은 정한 차례대로 겁니다. 앞 정규식이 바꾼 글에 다음 정규식을 겁니다.</li><li>가리지 않은 흐름은 보내기 직전에서 멈췄습니다. 원문이 든 메시지를 실제로 모델에 보내지는 않았습니다.</li><li>기록 한 줄은 글로만 만들고 파일에 쓰지 않았습니다. 기록 파일 쓰기는 05절에서 다룹니다.</li><li>노트북을 쓰기 전에 가린 메시지를 따로 다섯 번 보냈습니다. 다섯 번 모두 같은 답이었고 원문 값도 표식도 답에 없었습니다.</li><li>같은 요청도 실행한 때에 따라 답 문장이 달라질 수 있습니다. 그래서 모델 답에는 <code>assert</code>를 쓰지 않았습니다.</li><li>걸린 시간과 비용은 재지 않았습니다. 요청 수와 요금 어림만 준비물에 적었습니다.</li><li>이 절은 파일을 쓰지 않습니다. 이 챕터 자료 파일은 읽기만 합니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>정규식 넷으로 이메일·전화번호·주민등록번호·카드 번호를 찾아 표식으로 바꿨습니다.</li><li>가리지 않은 흐름은 보낼 메시지와 기록 한 줄에 원문 값 넷을 그대로 담았습니다.</li><li>가린 흐름은 두 곳 모두 원문 값이 없었고, 빈칸으로 적은 전화번호는 찾지 못했습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 03절에서는 길어진 대화 기록을 자르는 방법과 요약하는 방법을 견줍니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 이 절은 개인정보를 어느 두 자리에서 가렸나요?</p><p class="quiz-a">모델에게 보낼 사용자 메시지와 기록 한 줄입니다. 둘 다 값이 밖으로 나가거나 남기 전의 자리입니다. 틀렸다면 「핵심 개념」의 「가리는 자리」를 다시 읽습니다.</p><p class="quiz-q">2. 전화번호 정규식의 <code>-?</code>는 무슨 뜻인가요?</p><p class="quiz-a">붙임표가 있어도 없어도 맞는다는 뜻입니다. 기호 <code>?</code>는 바로 앞 글자가 없거나 한 번 있다는 뜻입니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">3. 가리지 않은 흐름에서 기록 한 줄에 남은 원문 값은 몇 개였나요?</p><p class="quiz-a">넷입니다. 출력 줄 <code>기록 한 줄에 남은 원문 값 수: 4</code>가 그 결과입니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">4. 질문 속 전화번호를 빈칸으로 적으면 무엇이 달라지나요?</p><p class="quiz-a">전화번호를 찾지 못해 원문이 그대로 남습니다. 정규식은 적어 둔 모양만 찾기 때문입니다. 틀렸다면 노트북 9절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.python.org/3.12/library/re.html">re — Regular expression operations</a></div>확인 2026-09-23 · 함수 <code>re.findall</code>·<code>re.sub</code>와 기호 <code>\\w</code>·<code>\\d</code>·<code>?</code>·<code>{m,n}</code>의 뜻을 적어 둔 문서입니다.</li><li><div><a href="https://www.rfc-editor.org/rfc/rfc2606.html">RFC 2606 Reserved Top Level DNS Names</a></div>확인 2026-09-23 · 주소 이름 <code>example.com</code>을 예시용으로 떼어 둔 문서입니다.</li><li>Ch 16 01절 — 입력 검사 <code>validate_query</code>와 출처 표시.</li><li>Ch 15 08절 — <code>json.dumps(…, ensure_ascii=False)</code>로 JSON 글 한 줄 만들기.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(SRC_HTML, encoding="utf-8")
    return SRC


if __name__ == "__main__":
    if os.environ.get("AUTHOR02_NB_ONLY") != "1":
        print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "02", SLUG, "paired", cells())
        print("wrote", path)
