"""Ch 16 04절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§6).

사용:
  python3 author_04.py            → 노트북 + _src 본문을 함께 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행해야 한다)
  python3 author_04.py --src-only → _src 본문만 다시 쓴다(노트북은 그대로)
  AUTHOR04_NB_ONLY=1 python3 author_04.py → 노트북만 다시 쓴다(그림을 그리기 전 새 커널 실행용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 이어서 한다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다. **paired 형식 유지**(chapter.json).
**서비스 모델 절이다.** 설명만 고칠 때는 이 파일을 다시 실행하지 말고 mdpatch.py → run_section.sh --no-exec(규격 §3).

## 결정 1 — 클래스 대신 함수와 딕셔너리 (챕터 리드 결정 4)

옛 판의 `@dataclass class CallBudget`을 쓰지 않는다. 예산은 딕셔너리 하나(칸 `max_calls`·`max_cost_usd`·`calls`·`cost_usd`),
만들기는 `make_budget(max_calls, max_cost_usd)`, 예약은 `reserve(budget, estimated_cost_usd)`. 두 함수는 이 절이 처음 가르치므로
노트북 안에 적고, 도구 파일 `notebooks/guardrails.py`의 두 함수와 AST·본문 줄이 같게 맞췄다(주석 자리만 다름,
「# Ch 16 04절에서 배웠습니다」). 테스트 4가 보는 인자 이름과 오류 문구의 「호출」·「비용」은 그대로 두었다.
본문을 8줄 안에 두려고 `reserve`의 마지막 `return budget`을 뺐다(부르는 곳 모두 돌아온 값을 쓰지 않음).

## 결정 2 — 비용 값의 출처는 (가) 이 절에서 정한 값

요청 하나의 예상 비용은 **이 절에서 정한 값 0.002달러**다. 요금표·토큰 수로 센 값이 아니고 청구 금액도 아니다.
한도 동작(몇 번째 요청이 어느 검사에서 막히는지)을 실행마다 같게 보이려고 정했다. 실제 사용량을 센 예상 비용(나)은
캐시 입력·출력 토큰에 따라 흔들리므로(Ch 15 06·09) 섞지 않는다. 응답 뒤 실제 토큰 수는 7절에서 따로 출력만 하고
비용으로 바꾸지 않는다.

## 결정 3 — paired 구성과 실제로 보내는 요청

Before(lesson_part="before") = 예산을 만들어 두고도 보지 않는 흐름. 질문 셋을 모두 보낼 목록에 담고 **보내기 직전에서 멈춘다**
(모델 요청 0번). 한도 2를 넘는 셋째 요청이 목록에 들어간 것이 결함(그림에서 빨강).
After(lesson_part="after") = 질문마다 `reserve`로 먼저 예약하고 예약이 된 질문만 모델에 보낸다. 셋째 질문은
`ValueError("호출 한도를 넘습니다.")`로 모델을 부르기 전에 멈춘다(받아 출력한 오류라 노랑).
핵심 관찰(보낸 요청 수·멈춘 질문·예산 칸)은 모델 답에 기대지 않아 결정적이다. 모델 답 문장·토큰 수는 결과 읽기 둘째 단락에만.

## 모델 요청

실행 한 번에 **3번**(`gpt-5.4-mini`, 7절 두 번 + 9절 한 번), 임베딩 0. 파일 쓰기 0번(자료 파일은 읽기만).

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·
`key=`·`reverse=`·`set`·`setdefault`·`.get`·`+=`·기본값 매개변수·타입힌트·한 줄 다중 대입(`a, b = 1, 2`)·세미콜론·클래스 정의·데코레이터.
처음 쓴 것: `math.isfinite`·`float("nan")`·`float("inf")`·`not A or B`·딕셔너리 칸 고치기(`budget["calls"] = budget["calls"] + 1`)·
함수에 넘긴 딕셔너리를 함수 안에서 고치기.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, install_source, key_and_model_cells, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part4/ch16-guardrails/notebooks"
SRC = ROOT / "textbook/part4/ch16-guardrails/_src/04-호출-한도와-비용-상한.html"
SLUG = "04-호출-한도와-비용-상한"

INSTALL = install_source(["langchain==1.4.0", "langchain-openai==1.6.1", "python-dotenv==1.2.3"])

IMPORTS = r'''# 파일을 읽을 이름, 수학 기능 묶음, 모델을 만들 이름을 불러옵니다
import json
import math
import os

from langchain.chat_models import init_chat_model

print("불러온 이름:", "json", "math", "os", "init_chat_model")'''

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

SETTINGS = r'''# 01·02절과 같은 지킬 말과 검색 문서 한 줄입니다
system_text = "검색 문서에 있는 사실만 써서 한국어 한 문장으로 답하세요. 답 끝에 쓴 문서의 출처를 [문서ID p.쪽] 꼴로 적으세요."
document = retrieved[0]
document_line = "검색 문서 " + document["doc_id"] + " " + str(document["page"]) + "쪽: " + document["text"]
print("지킬 말:")
print(system_text)
print("검색 문서 한 줄:")
print(document_line)'''

LIMITS = r'''# 이 절에서 정한 값입니다: 한 대화의 호출 한도와 비용 상한, 요청 하나의 예상 비용
max_calls = 2
max_cost_usd = 0.01
estimated_cost = 0.002
print("호출 한도:", max_calls)
print("비용 상한(달러):", max_cost_usd)
print("요청 하나의 예상 비용(달러):", estimated_cost)'''

QUESTIONS = r'''# 한 대화에서 사용자가 차례로 보낸 질문 셋입니다(이 절에서 손으로 적었습니다)
questions = [
    "도서관 휴관일은 언제인가요?",
    "공휴일이 월요일과 겹치면 언제 쉬나요?",
    "법정 공휴일에도 문을 여나요?",
]
print("질문 수:", len(questions))'''

DEF_BUILD = r'''# 질문 하나로 지킬 말과 사용자 메시지, 두 역할 딕셔너리를 만듭니다
def build_messages(question):
    user_text = "질문: " + question + "\n" + document_line
    messages = [
        {"role": "system", "content": system_text},
        {"role": "user", "content": user_text},
    ]
    return messages'''

CALL_BUILD = r'''# 첫 질문으로 메시지를 만들어 모양을 봅니다(보내지는 않습니다)
first_messages = build_messages(questions[0])
print("메시지 수:", len(first_messages))
print("역할:", first_messages[0]["role"], first_messages[1]["role"])
print("사용자 메시지:")
print(first_messages[1]["content"])'''

ISFINITE = r'''# nan과 inf를 만들어 보고, math.isfinite가 끝이 있는 숫자인지 가리는 모습을 봅니다
not_a_number = float("nan")
infinity = float("inf")
print("0.002는 끝이 있는 숫자:", math.isfinite(estimated_cost))
print("nan은 끝이 있는 숫자:", math.isfinite(not_a_number))
print("inf는 끝이 있는 숫자:", math.isfinite(infinity))
print("nan이 비용 상한보다 큰가:", not_a_number > max_cost_usd)'''

DEF_MAKE = r'''# 호출 한도와 비용 상한을 담은 예산 딕셔너리를 만듭니다
def make_budget(max_calls, max_cost_usd):
    if max_calls < 1:
        raise ValueError("호출 한도는 1 이상이어야 합니다.")
    if not math.isfinite(max_cost_usd) or max_cost_usd <= 0:
        raise ValueError("비용 상한은 끝이 있는 양수여야 합니다.")
    return {"max_calls": max_calls, "max_cost_usd": max_cost_usd, "calls": 0, "cost_usd": 0.0}'''

CALL_MAKE = r'''# 3절에서 정한 값으로 예산을 하나 만들고 네 칸을 봅니다
sample_budget = make_budget(max_calls, max_cost_usd)
print("새 예산:", sample_budget)'''

DEF_RESERVE = r'''# 모델을 부르기 전에 호출 한 번과 예상 비용을 예산에 예약합니다
def reserve(budget, estimated_cost_usd):
    if not math.isfinite(estimated_cost_usd) or estimated_cost_usd < 0:
        raise ValueError("예상 비용은 끝이 있는 0 이상 값이어야 합니다.")
    if budget["calls"] + 1 > budget["max_calls"]:
        raise ValueError("호출 한도를 넘습니다.")
    if budget["cost_usd"] + estimated_cost_usd > budget["max_cost_usd"]:
        raise ValueError("비용 상한을 넘습니다.")
    budget["calls"] = budget["calls"] + 1
    budget["cost_usd"] = budget["cost_usd"] + estimated_cost_usd'''

TRIAL = r'''# 새 예산에 한 번 예약하고 칸이 어떻게 바뀌었는지 봅니다(모델은 부르지 않습니다)
reserve(sample_budget, estimated_cost)
print("예약 한 번 뒤 예산:", sample_budget)'''

BEFORE_OUTBOX = r'''# 한도를 보지 않는 흐름입니다: 질문마다 메시지를 만들어 보낼 목록에 담습니다(보내지는 않습니다)
outbox = []
planned_cost = 0.0
for question in questions:
    messages = build_messages(question)
    outbox.append(messages)
    planned_cost = planned_cost + estimated_cost
print("보낼 목록의 요청 수:", len(outbox))
print("보낼 목록의 예상 비용 합계(달러):", planned_cost)'''

BEFORE_OVER = r'''# 보낼 목록을 3절에서 정한 호출 한도와 견줘 한도를 넘는 요청을 셉니다
over_count = len(outbox) - max_calls
print("정한 호출 한도:", max_calls)
print("한도를 넘는 요청 수:", over_count)
print("한도를 넘는 첫 요청의 질문:", questions[max_calls])'''

DEF_ASK = r'''# 먼저 예약하고, 예약이 되면 그 질문을 모델에게 보냅니다(부를 때마다 모델 요청 1번)
def ask_with_budget(budget, question, estimated_cost_usd):
    reserve(budget, estimated_cost_usd)
    messages = build_messages(question)
    return model.invoke(messages)'''

DEF_ALL = r'''# 질문 목록을 차례로 보내다가 예약이 막히면 그 자리에서 멈춥니다
def ask_all(budget, questions, estimated_cost_usd):
    answers = []
    for question in questions:
        try:
            answers.append(ask_with_budget(budget, question, estimated_cost_usd))
        except ValueError as error:
            print("멈춘 질문:", question, "| 까닭:", error)
            break
    return answers'''

RUN = r'''# 새 예산으로 질문 셋을 차례로 보냅니다(모델 요청 2번, 셋째 질문은 예약에서 멈춥니다)
budget = make_budget(max_calls, max_cost_usd)
answers = ask_all(budget, questions, estimated_cost)
print("모델에 보낸 요청 수:", len(answers))
print("예약한 호출 수:", budget["calls"])
print("예약한 예상 비용 합계(달러):", budget["cost_usd"])'''

ANSWERS = r'''# 받은 답을 번호와 함께 봅니다
print("받은 답:")
for i in range(len(answers)):
    print(i, "|", answers[i].text)'''

USAGE = r'''# 첫 응답의 실제 사용량을 따로 봅니다: 예약할 때 쓴 예상 비용과는 다른 값입니다
first_usage = answers[0].usage_metadata
print("첫 응답 입력 토큰 수:", first_usage["input_tokens"])
print("첫 응답 출력 토큰 수:", first_usage["output_tokens"])
print("예약한 요청 하나의 예상 비용(달러):", estimated_cost)'''

COMPARE = r'''# 두 흐름을 한 표로 나란히 봅니다
print("흐름 | 모델에 갈 요청 수 | 멈춘 질문 수")
print("한도를 보지 않는 흐름 |", len(outbox), "|", len(questions) - len(outbox))
print("예약하는 흐름 |", len(answers), "|", len(questions) - len(answers))'''

HAND = r'''# 잘못된 예상 비용 셋을 예약해 봅니다(미리 정한 값이라 assert로 봅니다, 모델은 부르지 않습니다)
check_budget = make_budget(max_calls, max_cost_usd)
negative_cost = -0.1
print("예상 비용 | 막은 까닭")
for bad_cost in [not_a_number, infinity, negative_cost]:
    try:
        reserve(check_budget, bad_cost)
    except ValueError as error:
        print(bad_cost, "|", error)
assert check_budget["calls"] == 0
assert check_budget["cost_usd"] == 0.0'''

VALUE = r'''# 바꿀 값은 비용 상한 하나입니다: 0.01 대신 0.003으로 같은 질문 셋을 보냅니다
small_cost_cap = 0.003
small_budget = make_budget(max_calls, small_cost_cap)
small_answers = ask_all(small_budget, questions, estimated_cost)
print("비용 상한(달러):", small_cost_cap)
print("모델에 보낸 요청 수:", len(small_answers))
print("예약한 예상 비용 합계(달러):", small_budget["cost_usd"])'''


FIG1 = "04-1-부르기-전에-예약하기"
FIG1_ALT = "위에서 아래로 읽는 그림으로 초록 상자 질문 셋 한 대화에서 차례로에서 파란 상자 예약 reserve 호출 한도 둘 비용 상한 0.01로 이어지고 거기서 화살표가 둘로 나뉘어 왼쪽은 보라 상자 모델 gpt-5.4-mini 첫째와 둘째 질문을 지나 노란 상자 받은 응답 둘로 가고 오른쪽은 노란 상자 셋째 질문 멈춤 ValueError 호출 한도로 가는 그림"
FIG1_READ = """위에서 아래로 읽습니다. 초록 질문 셋이 파란 예약을 지나 화살표 둘로 나뉩니다.
왼쪽은 보라 모델을 거쳐 응답 둘을 받고, 오른쪽은 셋째 질문이 노란 상자에서 멈춥니다."""
FIG1_CAP = "질문마다 먼저 예약합니다. 예약이 된 질문만 모델에 가고, 셋째 질문은 호출 한도에서 멈췄습니다."

FIG2 = "04-2-예약-함수의-검사-셋"
FIG2_ALT = "위에서 아래로 읽는 그림으로 초록 상자 예상 비용 한 번 몫 정한 값 0.002에서 파란 상자 검사 하나 끝이 있는 0 이상 값인가, 파란 상자 검사 둘 호출 수에 하나를 더해도 한도 안인가, 파란 상자 검사 셋 예상 비용을 더해도 상한 안인가, 파란 상자 예산 칸 둘을 고침 calls와 cost_usd, 노란 상자 예약 한 번 뒤 calls 1 cost_usd 0.002가 차례로 이어지고 검사 세 상자에서 각각 점선 화살표가 오른쪽 노란 상자 ValueError 예산 칸은 그대로로 가는 그림"
FIG2_CAP = "예약 함수는 검사 셋을 모두 지나야 예산 칸을 고칩니다. 하나라도 걸리면 ValueError를 냅니다."

FIG3 = "04-3-한도를-보지-않는-흐름과-예약하는-흐름"
FIG3_ALT = "칸 둘이 나란히 있고 아래에 회색 상자가 있는 그림으로 왼쪽 Before 한도를 보지 않는 흐름 칸에서는 초록 상자 질문 셋에서 빨간 상자 보낼 목록 요청 셋 한도 둘을 넘는 요청 하나로 이어지고 오른쪽 After 부르기 전에 예약하는 흐름 칸에서는 초록 상자 질문 셋에서 파란 상자 예약 reserve를 지나 화살표가 둘로 나뉘어 노란 상자 모델에 보낸 요청 둘과 노란 상자 셋째 질문 멈춤 호출 한도로 가며 맨 아래 회색 상자에 두 칸 모두 같은 질문 셋 호출 한도 둘 비용 상한 0.01이 적힌 그림"
FIG3_CAP = "같은 질문 셋에서 한도를 보지 않는 흐름은 셋째 요청까지 담았고, 예약하는 흐름은 두 번만 보냈습니다."

FIG4 = "04-4-비용-상한을-낮추면"
FIG4_ALT = "칸 둘이 나란히 있고 아래에 회색 상자가 있는 그림으로 왼쪽 비용 상한 0.01 노트북 7절 칸에서는 초록 상자 질문 셋에서 노란 상자 보낸 요청 둘 셋째 질문에서 호출 한도로 멈춤으로 이어지고 오른쪽 비용 상한 0.003 노트북 9절 칸에서는 초록 상자 질문 셋에서 노란 상자 보낸 요청 하나 둘째 질문에서 비용 상한으로 멈춤으로 이어지며 맨 아래 회색 상자에 두 칸 모두 호출 한도 둘 요청 하나 예상 비용 0.002가 적힌 그림"
FIG4_CAP = "비용 상한을 0.003으로 낮추자 호출 한도가 아니라 비용 상한이 둘째 질문을 막았습니다."

ILLU = "04-5-개찰구와-회전-막대"
ILLU_ALT = "흰 바탕 나무 탁자 가운데에 네모난 나무 틀 하나가 서 있고 틀에서 왼쪽으로 둥근 막대 하나가 뻗어 있으며 틀 왼쪽 막대 앞에는 파란 표 한 장이, 틀 오른쪽 건너편에는 파란 표 두 장이 나란히 놓여 있고 탁자 뒤 오른쪽에 펼친 대장 한 권과 그 위에 선 나무 손도장 하나가 놓인 그림"
ILLU_CAP = "표 두 장은 막대를 지나 건너편에 있고, 셋째 표는 막대 앞에 멈춰 있습니다."
ILLU_READ = "나무 탁자 가운데에 네모난 나무 틀이 서 있고, 틀에서 왼쪽으로 둥근 막대 하나가 뻗어 있습니다. 이 틀과 막대가 개찰구입니다. 틀 왼쪽 막대 앞에는 파란 표 한 장이 놓여 있습니다. 틀 오른쪽 건너편에는 파란 표 두 장이 나란히 놓여 있습니다. 탁자 뒤 오른쪽에는 01절의 펼친 대장과 그 위에 선 나무 손도장이 있습니다."

TITLE = """# 호출 한도와 비용 상한

이 절은 모델을 부르기 전에 호출 수와 예상 비용을 예약합니다.
정한 한도를 넘는 요청은 모델을 부르기 전에 멈춥니다.

**이 노트북에서 할 일**

1. 한 대화의 호출 한도·비용 상한과 요청 하나의 예상 비용을 정합니다.
2. 예산 딕셔너리를 만드는 함수와, 부르기 전에 예약하는 함수를 만듭니다.
3. 한도를 보지 않는 흐름이 한도를 넘는 요청까지 보낼 목록에 담는 것을 봅니다(Before).
4. 부르기 전에 예약하면 한도를 넘는 요청이 모델에 가지 않는 것을 봅니다(After).

**준비물** — 이 절은 프로젝트 맨 위 폴더의 `.env`에 적어 둔 `OPENAI_API_KEY`를 씁니다.
모델 `gpt-5.4-mini`에 보내는 요청은 7절 두 번과 9절 한 번, 모두 세 번입니다.
임베딩 요청은 없습니다.
노트북을 한 번 실행하는 요금은 요금표로 어림해 미화 0.01달러 아래입니다.
이 값은 3절에서 정할 요청 하나의 예상 비용 0.002달러와 다르고, 실제 청구 금액과도 다를 수 있습니다.

읽는 파일은 이 챕터 자료 파일 `data/retrieved-documents.json` 하나입니다.
새로 쓰는 파일은 없습니다.
교재 출력을 만든 실행에서는 노트북 전체가 약 5초 만에 끝났습니다.

**기준 버전** — 첫 셀에서 LangChain 1.4.0과 langchain-openai 1.6.1을 설치합니다.
키를 읽는 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3~7절을 읽습니다.
한도를 정하고, 예약 함수를 만들고, 한도를 보지 않는 흐름을 보는 자리입니다.
7절은 부르기 전에 예약하며 질문을 보내는 자리입니다.
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

다음 셀은 이 절에서 쓸 이름 넷을 불러옵니다.
모듈 `math`는 Ch 15 06절에서 `math.ceil`을 쓸 때 불러온 모듈입니다.
이 절은 그 안의 함수 `math.isfinite`를 처음 씁니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 출력 줄 `불러온 이름: json math os init_chat_model`로 이름 넷을 불러왔습니다.
이 절은 도구 파일 `guardrails.py`에서 가져오는 함수가 없습니다.
호출 한도와 비용 상한을 다루는 함수는 이 절에서 처음 만듭니다.

## 2. 키와 모델 준비

이 절은 7절에서 두 번, 9절에서 한 번 모델 `gpt-5.4-mini`를 부릅니다."""),
    ] + key_and_model_cells(
        "openai:gpt-5.4-mini",
        "temperature 값을 0으로 두어도 답 문장이 매번 같다고 보장하지는 않습니다.",
    ) + [
        md("""## 3. 자료와 이 절에서 정한 값

먼저 노트북을 연 자리에서 프로젝트 맨 위를 찾습니다.
01·02절과 같은 자리 찾기 셀입니다."""),
        setup(ROOT_PATH),
        md("""**결과 읽기** — 출력 줄 `찾은 프로젝트 맨 위:` 뒤에 점 하나나 위로 올라가는 자리가 보입니다.

다음 셀은 01·02절과 같은 자료 파일을 읽고 안내 문서 하나를 고릅니다.
이 절의 질문은 모두 이 문서로 답할 수 있습니다."""),
        code(READ_PICK),
        md("""**결과 읽기** — 출력 줄 `자료 파일의 문서 수: 2`로 자료 파일의 문서는 둘입니다.
출력 줄 `이번 검색 결과의 문서 수: 1`로 이 절은 안내 문서 하나만 씁니다.

다음 셀은 01·02절과 같은 시스템 메시지 글과 검색 문서 한 줄을 적습니다."""),
        code(SETTINGS),
        md("""**결과 읽기** — 라벨 줄 `지킬 말:` 아래 줄이 시스템 메시지로 보낼 글입니다.
라벨 줄 `검색 문서 한 줄:` 아래 줄이 질문과 함께 보낼 문서입니다.
두 글 모두 01·02절과 같습니다.
출력 라벨과 코드 주석의 「지킬 말」은 시스템 메시지 글을 부르는 이름입니다.
Ch 8 03절의 지킬 말(꼭 남아야 할 말 목록)과는 다른 뜻입니다.

다음 셀은 이 절에서 정한 값 셋을 적습니다.
호출 한도(call limit)는 한 대화에서 모델을 부를 수 있는 가장 많은 횟수입니다.
비용 상한(cost cap)은 한 대화에서 쓸 수 있는 예상 비용 합계의 가장 큰 값입니다.
예상 비용은 요청을 보내기 전에 어림한 비용이고 청구 금액이 아닙니다.

Ch 15 06절처럼 예산은 요청 한 번이 아니라 대화 하나를 단위로 셉니다.
요청 하나의 예상 비용 0.002달러는 요금표로 센 값이 아니라 이 절에서 정한 값입니다."""),
        code(LIMITS),
        md("""**결과 읽기** — 출력 줄 `호출 한도: 2`로 한 대화에서 모델을 두 번까지 부릅니다.
출력 줄 `비용 상한(달러): 0.01`이 예상 비용 합계의 상한입니다.
출력 줄 `요청 하나의 예상 비용(달러): 0.002`로 요청마다 같은 값을 씁니다.

세 값은 한도에 걸리는 모습이 잘 보이게 정한 값입니다.
실제 서비스라면 Ch 6 06절 요금표처럼 토큰 수와 요금으로 예상 비용을 어림합니다.

## 4. 질문 셋과 보낼 메시지

한 대화에서 사용자가 질문 셋을 차례로 보냈다고 해 봅니다.
세 질문 모두 안내 문서로 답할 수 있습니다.
정한 호출 한도가 2라서 셋째 질문은 한도를 넘습니다."""),
        code(QUESTIONS),
        md("""**결과 읽기** — 출력 줄 `질문 수: 3`으로 질문은 셋입니다.
첫 질문은 01·02절과 같은 휴관일 질문입니다.

다음 셀은 질문 하나로 보낼 메시지를 만드는 함수입니다.
메시지 모양은 01·02절과 같은 역할 딕셔너리 두 개입니다.
시스템 메시지 글과 검색 문서 한 줄은 3절에서 적은 값을 씁니다."""),
        code(DEF_BUILD),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `build_messages`는 질문 하나를 받아 메시지 목록 하나를 내놓습니다.
사용자 메시지는 「질문: 」 뒤에 질문을 적고, 줄을 바꿔 검색 문서 한 줄을 붙입니다.

다음 셀은 첫 질문으로 메시지를 만들어 모양을 봅니다.
이 셀은 모델에 보내지 않습니다."""),
        code(CALL_BUILD),
        md("""**결과 읽기** — 출력 줄 `메시지 수: 2`와 `역할: system user`로 역할 딕셔너리 두 개가 만들어졌습니다.
라벨 줄 `사용자 메시지:` 아래 두 줄이 모델에게 갈 사용자 메시지입니다.

## 5. 예산 딕셔너리와 예약

예약(reserve)은 모델을 부르기 전에 호출 한 번과 예상 비용을 미리 적어 두는 일입니다.
표를 내야 개찰구를 지나가듯, 예약이 되어야 모델을 부릅니다.
예약한 양은 예산(budget) 딕셔너리에 적습니다.
예산 딕셔너리에는 두 한도와 지금까지 예약한 호출 수·예상 비용이 함께 들어갑니다.

예상 비용 자리에 보통 숫자가 아닌 값이 들어올 수도 있습니다.
값 `float("nan")`은 숫자가 아니라는 뜻(not a number)의 특별한 값입니다.
값 `float("inf")`는 끝없이 큰 값입니다.
함수 `math.isfinite(값)`은 값이 nan도 inf도 아닌 끝이 있는 숫자이면 `True`를 내놓습니다."""),
        code(ISFINITE),
        md("""**결과 읽기** — 출력 줄 `0.002는 끝이 있는 숫자: True`로 정한 예상 비용은 보통 숫자입니다.
출력 줄 `nan은 끝이 있는 숫자: False`와 `inf는 끝이 있는 숫자: False`로 두 값은 걸러집니다.
출력 줄 `nan이 비용 상한보다 큰가: False`를 눈여겨봅니다.
값 nan은 어떤 값과 견줘도 크다는 결과가 나오지 않습니다.

그래서 「상한보다 크면 막기」만 두면 nan은 그 검사를 그냥 지나갑니다.
다음 두 함수는 이런 값을 `math.isfinite`로 먼저 막습니다.

다음 셀은 예산 딕셔너리를 만드는 함수입니다.
호출 한도가 1보다 작거나, 비용 상한이 끝이 있는 양수가 아니면 `ValueError`를 냅니다.
조건 `not A or B`에서 `not`은 바로 뒤 조건 A에만 붙습니다.
그래서 「A가 아니거나 B이면」이라는 뜻입니다."""),
        code(DEF_MAKE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `make_budget`은 두 한도를 받아 칸 넷짜리 딕셔너리를 내놓습니다.
칸 `calls`는 지금까지 예약한 호출 수이고, 칸 `cost_usd`는 지금까지 예약한 예상 비용 합계입니다.
두 칸 모두 0에서 시작합니다.

다음 셀은 3절에서 정한 값으로 예산을 하나 만들어 봅니다."""),
        code(CALL_MAKE),
        md("""**결과 읽기** — 출력 줄 `새 예산: {'max_calls': 2, 'max_cost_usd': 0.01, 'calls': 0, 'cost_usd': 0.0}`이 새 예산입니다.
한도 칸 둘은 3절 값과 같고, 예약한 양 칸 둘은 0입니다.

다음 셀은 예약 함수 `reserve`입니다.
검사 셋을 차례로 하고, 모두 지나야 예산 칸을 고칩니다.
첫째는 예상 비용이 끝이 있는 0 이상 값인지 봅니다.
둘째는 호출 수에 하나를 더해도 한도 안인지, 셋째는 예상 비용을 더해도 상한 안인지 봅니다.

칸 고치기는 `budget["calls"] = budget["calls"] + 1`처럼 씁니다.
오른쪽에서 지금 값에 1을 더한 뒤 같은 칸에 다시 넣습니다.
이 함수는 아무것도 내놓지 않고 받은 딕셔너리의 칸만 고칩니다."""),
        code(DEF_RESERVE),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
검사 하나라도 걸리면 `raise`에서 멈추고 아래 줄은 실행되지 않습니다.
그래서 막힌 예약은 예산 칸을 바꾸지 않습니다.
함수에 넘긴 딕셔너리는 함수 밖의 딕셔너리와 같은 것입니다.
함수 안에서 고친 칸이 밖에서도 보입니다.

다음 셀은 앞에서 만든 새 예산에 한 번 예약해 봅니다.
모델은 부르지 않습니다."""),
        code(TRIAL),
        md("""**결과 읽기** — 출력 줄 `예약 한 번 뒤 예산: {'max_calls': 2, 'max_cost_usd': 0.01, 'calls': 1, 'cost_usd': 0.002}`에서 두 칸이 바뀌었습니다.
칸 `calls`는 1이 되었고 칸 `cost_usd`는 0.002가 되었습니다.
함수 `reserve`는 아무것도 내놓지 않았지만 넘긴 딕셔너리의 칸이 바뀌었습니다.

## 6. 한도를 보지 않는 흐름 (Before)""", lesson_part="before"),
        md("""Before 셀은 예산을 만들어 두고도 쓰지 않는 흐름입니다.
질문마다 메시지를 만들어 보낼 목록에 그대로 담습니다.
이 흐름은 보내기 직전에서 멈추고 실제로 모델에 보내지는 않았습니다.
목록에 담은 요청 수와 예상 비용 합계를 셉니다.""", lesson_part="before"),
        code(BEFORE_OUTBOX, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `보낼 목록의 요청 수: 3`으로 질문 셋이 모두 보낼 목록에 들어갔습니다.
출력 줄 `보낼 목록의 예상 비용 합계(달러): 0.006`은 비용 상한 0.01 안입니다.
이 흐름은 호출 수도 예상 비용도 한도와 견주지 않았습니다.

다음 셀은 보낼 목록을 3절에서 정한 호출 한도와 견줍니다.""", lesson_part="before"),
        code(BEFORE_OVER, lesson_part="before"),
        md("""**결과 읽기** — 출력 줄 `한도를 넘는 요청 수: 1`이 이 흐름의 결함입니다.
라벨 `한도를 넘는 첫 요청의 질문:` 뒤가 셋째 질문입니다.
이대로 보내면 호출 한도 2를 넘어 모델을 세 번 부릅니다.

한도를 적어 두기만 하고 보내는 코드가 보지 않으면 한도는 아무것도 막지 못합니다.

## 7. 부르기 전에 예약하는 흐름 (After)""", lesson_part="after"),
        md("""After 셀은 질문을 보내기 전마다 `reserve`로 예약합니다.
예약이 막히면 모델을 부르지 않고 그 자리에서 멈춥니다.
먼저 예약과 모델 부르기를 한 함수로 묶습니다.""", lesson_part="after"),
        code(DEF_ASK, lesson_part="after"),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `ask_with_budget`의 첫 줄이 예약입니다.
예약에서 `ValueError`가 나면 아래 두 줄은 실행되지 않아 모델을 부르지 않습니다.
예약이 되면 메시지를 만들어 모델에게 보내고 받은 응답을 내놓습니다.

다음 셀은 질문 목록을 차례로 보내는 함수입니다.
03절처럼 `try/except ValueError as error`로 오류를 받습니다.
예약이 막히면 막힌 질문과 까닭을 출력하고 그때까지 받은 응답 목록을 내놓습니다.""", lesson_part="after"),
        code(DEF_ALL, lesson_part="after"),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
블록 `try` 안의 한 줄은 예약하고 받은 응답을 목록에 더합니다.
예약이 막히면 응답이 없으므로 목록에 아무것도 더하지 않습니다.
오류를 받은 뒤의 `break`는 남은 질문을 보지 않고 반복을 끝냅니다.
그래서 막힌 질문 뒤의 질문도 보내지 않습니다.

다음 셀은 새 예산으로 질문 셋을 보냅니다.
이 셀에서 모델 요청이 두 번 나가고, 셋째 질문은 예약에서 멈출 것입니다.""", lesson_part="after"),
        code(RUN, lesson_part="after"),
        md("""**결과 읽기** — 첫 출력 줄 `멈춘 질문: 법정 공휴일에도 문을 여나요? | 까닭: 호출 한도를 넘습니다.`가 셋째 질문입니다.
출력 줄 `모델에 보낸 요청 수: 2`로 모델은 두 번만 불렸습니다.
출력 줄 `예약한 호출 수: 2`와 `예약한 예상 비용 합계(달러): 0.004`가 예산에 적힌 양입니다.

셋째 질문은 호출 수 검사에서 막혀 모델에 가지 않았습니다.
앞 6절 Before 셀에서는 `보낼 목록의 요청 수: 3`이었습니다.

다음 셀은 받은 답 둘을 봅니다.""", lesson_part="after"),
        code(ANSWERS, lesson_part="after"),
        md("""**결과 읽기** — 라벨 줄 `받은 답:` 아래 두 줄이 모델 답입니다.
번호 0은 첫 질문의 답이고, 번호 1은 둘째 질문의 답입니다.
셋째 질문의 답은 없습니다.

이 답은 모델이 쓴 글이라 여러분 실행에서는 문장이 다를 수 있습니다.
교재 출력을 만들며 새 커널로 두 번 실행했을 때도 둘째 답의 끝말이 달랐습니다.
이 절은 답 문장이 아니라 보낸 요청 수와 멈춘 질문을 봅니다.

다음 셀은 첫 응답의 실제 사용량을 봅니다.
Ch 6 06절처럼 응답의 `usage_metadata`에 입력·출력 토큰 수가 들어 있습니다.
이 값은 응답을 받은 뒤에야 알 수 있습니다.""", lesson_part="after"),
        code(USAGE, lesson_part="after"),
        md("""**결과 읽기** — 라벨 `첫 응답 입력 토큰 수:`와 `첫 응답 출력 토큰 수:` 뒤가 실제로 쓴 토큰 수입니다.
출력 줄 `예약한 요청 하나의 예상 비용(달러): 0.002`는 보내기 전에 정한 값입니다.
두 값은 서로 다른 것이라 섞지 않습니다.
이 절은 토큰 수로 비용을 다시 셈하지 않았습니다.

이번 실행에서는 입력 토큰 122개, 출력 토큰 53개였습니다.
교재 출력을 만들며 새 커널로 두 번 실행했을 때 두 값은 같았습니다.
그래도 출력 토큰 수는 답 문장에 따라 달라질 수 있습니다.

다음 셀은 두 흐름을 한 표로 나란히 봅니다.""", lesson_part="after"),
        code(COMPARE, lesson_part="after"),
        md("""**결과 읽기** — 라벨 줄 `흐름 | 모델에 갈 요청 수 | 멈춘 질문 수` 아래 두 줄이 두 흐름입니다.
출력 줄 `한도를 보지 않는 흐름 | 3 | 0`은 보낼 목록에 담은 수입니다.
출력 줄 `예약하는 흐름 | 2 | 1`은 실제로 보낸 수와 멈춘 수입니다.
두 흐름은 같은 질문 셋과 같은 한도를 썼고, 예약을 했는지만 달랐습니다.

## 8. 손으로 정한 값으로 확인하기

다음 셀은 잘못된 예상 비용 셋을 새 예산에 예약해 봅니다.
5절에서 만든 nan과 inf, 그리고 음수 -0.1입니다.
셋 모두 막혀야 하고 예산 칸은 그대로여야 합니다.
미리 정한 값이라 결과를 `assert`로 확인할 수 있습니다.""", lesson_part="after"),
        code(HAND, lesson_part="after"),
        md("""**결과 읽기** — 라벨 줄 `예상 비용 | 막은 까닭` 아래 세 줄에서 세 값이 모두 막혔습니다.
까닭은 모두 `예상 비용은 끝이 있는 0 이상 값이어야 합니다.`입니다.
마지막 두 줄의 `assert`도 통과해 예약한 호출 수와 예상 비용은 0 그대로입니다.

## 9. 값 바꿔 보기 · 비용 상한 0.003

바꿀 값은 비용 상한 하나입니다.
0.01 대신 0.003으로 새 예산을 만들고 같은 질문 셋을 보냅니다.
호출 한도 2와 요청 하나의 예상 비용 0.002는 그대로입니다.

실행 전에 예상해 봅니다.
첫 질문은 예상 비용 0.002가 상한 안이라 보낼 것입니다.
둘째 질문은 합계가 0.004가 되어 상한 0.003을 넘으므로 멈출 것입니다.
이 셀에서 모델 요청은 한 번 나갈 것입니다.""", lesson_part="after"),
        code(VALUE, lesson_part="after"),
        md("""**결과 읽기** — 첫 출력 줄에서 둘째 질문이 `비용 상한을 넘습니다.`로 멈췄습니다.
출력 줄 `모델에 보낸 요청 수: 1`로 모델은 한 번만 불렸습니다.
출력 줄 `예약한 예상 비용 합계(달러): 0.002`가 예산에 적힌 양입니다.

예상대로 이번에는 호출 수가 아니라 비용 상한이 둘째 질문을 막았습니다.
7절 출력에서는 셋째 질문이 `호출 한도를 넘습니다.`로 멈췄습니다.

## 정리

1. 한 대화의 호출 한도와 비용 상한을 예산 딕셔너리에 담고, 부르기 전에 예약하는 함수를 만들었습니다.
2. 한도를 보지 않는 흐름은 호출 한도 2를 넘는 셋째 질문까지 보낼 목록에 담았습니다.
3. 예약하는 흐름은 셋째 질문을 부르기 전에 멈췄고, 비용 상한을 낮추자 둘째 질문에서 멈췄습니다.

05절에서는 실패한 요청을 다시 부르거나 예비 답을 내고, 감사 기록 파일에 남깁니다.""", lesson_part="after"),
    ]


SRC_HTML = """<!--meta: 강의 0.5h | 실습 0.75h | 코드 notebooks/04-호출-한도와-비용-상한.ipynb | 새 용어 4 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>모델을 부르기 전에 호출 수와 예상 비용을 예약하는 함수를 만들 수 있습니다.</li>
<li>호출 한도나 비용 상한을 넘는 요청을 모델을 부르기 전에 멈출 수 있습니다.</li>
<li>예약한 예상 비용과 응답 뒤의 실제 사용량을 나눠 설명할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>모델 요청 하나하나에 비용이 듭니다. 한 대화에서 질문이 이어지면 요청 수와 비용도 함께 늘어납니다. 03절의 요약하기처럼 질문 하나가 요청을 더 부르는 흐름도 있습니다.</p><p>응답의 사용량은 요청이 나간 뒤에야 알 수 있습니다. 그때 한도를 넘은 것을 알아도 요청은 이미 나갔습니다. 그래서 이 절은 보내기 전에 호출 수와 예상 비용을 먼저 적어 둡니다. 한도를 넘는 요청은 보내지 않습니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>Ch 6 06절에서는 응답의 <code>usage_metadata</code>로 입력·출력 토큰 수를 읽었습니다. 그 토큰 수와 요금표로 요청 한 번의 예상 비용을 셌습니다. 두 값 모두 응답을 받은 뒤에 센 값입니다.</p><p>Ch 15 06절은 예산을 요청 한 번이 아니라 대화 하나를 단위로 센다고 했습니다. Ch 15 09절은 보낸 요청의 예상 비용을 세기만 했고 상한으로 막지는 않았습니다. 이 절에서 처음으로 부르기 전에 막습니다.</p><p>메시지는 01·02절과 같은 역할 딕셔너리 두 개이고, 질문도 같은 안내 문서로 답합니다. 오류는 03절처럼 <code>try/except ValueError as error</code>로 받습니다. 모듈 <code>math</code>는 Ch 15 06절에서 <code>math.ceil</code>을 쓸 때 불러온 이름입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절의 탁자 위에 이번에는 작은 개찰구 하나가 놓였다고 해 봅니다. 개찰구의 회전 막대는 표 한 장을 받아야 한 번 돌아갑니다. 이 개찰구가 받는 표는 두 장까지입니다. 표 두 장은 막대를 지나 건너편에 놓였고, 셋째 표는 막대 앞에서 멈췄습니다.</p><p>막대는 지나가기 전에 표를 봅니다. 건너간 뒤에 세면 이미 늦습니다. 이 절의 예약이 이 회전 막대 자리입니다. 지나간 표는 곁에 둔 대장에 적어 둡니다.</p>
{{img:""" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + """}}
<p class="look"><b>그림 읽기</b> — """ + ILLU_READ + """</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>호출 한도(call limit)</td><td>한 대화에서 모델을 부를 수 있는 가장 많은 횟수입니다. 개찰구가 받는 표의 수와 같습니다.</td></tr><tr><td>비용 상한(cost cap)</td><td>한 대화에서 쓸 수 있는 예상 비용 합계의 가장 큰 값입니다. 예상 비용은 보내기 전에 어림한 값이고 청구 금액이 아닙니다.</td></tr><tr><td>예약(reserve)</td><td>모델을 부르기 전에 호출 한 번과 예상 비용을 미리 적어 두는 일입니다. 한도나 상한을 넘으면 적지 않고 멈춥니다. 표를 내고 회전 막대를 지나가는 일과 같습니다.</td></tr><tr><td>예산(budget)</td><td>두 한도와 지금까지 예약한 양을 함께 적어 둔 딕셔너리입니다. 개찰구 곁에 둔 대장과 같습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 호출 한도는 인자 <code>max_calls</code>이고, 비용 상한은 인자 <code>max_cost_usd</code>입니다. 예산은 함수 <code>make_budget</code>이 만드는 딕셔너리이고, 예약은 함수 <code>reserve</code>가 합니다.</p>
{{mermaid:""" + FIG1 + "|" + FIG1_ALT + "|" + FIG1_CAP + """}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자가 한 대화의 질문 셋이고, 파란 예약 상자에서 화살표가 둘로 나뉩니다. 왼쪽은 보라 모델을 지나 노란 받은 응답 둘로 갑니다. 오른쪽 노란 상자는 셋째 질문이 호출 한도에서 멈춘 자리입니다. 두 쪽 모두 노트북 7절에서 실제로 실행한 흐름입니다.</p>
<h3>예약은 부르기 전에 합니다</h3><p>실제로 쓴 토큰 수는 응답의 <code>usage_metadata</code>에 있습니다. 이 값은 응답을 받은 뒤에야 알 수 있습니다. 그래서 예약은 보내기 전에 정한 예상 비용으로 합니다. 예약이 막히면 그 요청은 모델에 가지 않습니다.</p>
<h3>예상 비용은 이 절에서 정한 값입니다</h3><p>이 절의 요청 하나 예상 비용 0.002달러는 이 절에서 정한 값입니다. 요금표와 토큰 수로 센 값이 아니고 청구 금액도 아닙니다. 한도에 걸리는 모습이 잘 보이게 정했습니다. 실제 서비스라면 Ch 6 06절 요금표와 요청 길이로 예상 비용을 어림합니다.</p>
<h3>nan과 inf는 먼저 막습니다</h3><p>값 <code>float("nan")</code>은 숫자가 아니라는 뜻의 특별한 값입니다. 어떤 값과 견줘도 크다는 결과가 나오지 않습니다. 「상한보다 크면 막기」만 두면 nan은 그 검사를 그냥 지나갑니다. 그래서 두 함수는 <code>math.isfinite</code>로 끝이 있는 숫자인지 먼저 봅니다.</p>
<h3>다른 상황에 적용</h3><p>03절의 요약하기도 모델 요청입니다. 요약 요청 앞에서도 같은 예산에 예약하면 요약까지 한도 안에서 셉니다. 질문 하나가 모델을 여러 번 부르는 흐름이라면 부를 때마다 예약합니다.</p>
<h3>비교와 경계</h3><p>이 절의 호출 한도는 우리 코드가 정한 규칙입니다. 모델 서비스가 정한 시간당 요청 수 제한과는 다르고, 그 제한은 이번에 다루지 않았습니다. 예약은 예상 비용만 더합니다. 실제 사용량이 예상보다 크면 실제 비용은 상한을 넘을 수 있습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 01·02절과 같은 자료 파일에서 안내 문서 하나를 고릅니다. 노트북 3절은 호출 한도 2와 비용 상한 0.01달러, 요청 하나의 예상 비용 0.002달러를 정합니다. 노트북 4절은 한 대화의 질문 셋과 보낼 메시지를 만듭니다. 노트북 5절은 예산을 만드는 함수와 예약 함수를 만들고 한 번 예약해 봅니다.</p><p>모델 <code>gpt-5.4-mini</code>에 보내는 요청은 노트북 7절 두 번과 9절 한 번입니다. 임베딩 요청은 없습니다. 노트북을 한 번 실행하는 요금은 요금표로 어림해 미화 0.01달러 아래입니다. 노트북 3절에서 정한 요청 하나의 예상 비용 0.002달러와는 다른 값이고, 실제 청구 금액과도 다를 수 있습니다. 새로 쓰는 파일은 없습니다.</p>
{{notebook:""" + SLUG + """|example}}
<p class="look"><b>확인할 점</b> — 노트북 5절 출력 <code>예약 한 번 뒤 예산: {'max_calls': 2, 'max_cost_usd': 0.01, 'calls': 1, 'cost_usd': 0.002}</code>에서 두 칸이 바뀌었는지 봅니다. 출력 <code>nan이 비용 상한보다 큰가: False</code>도 봅니다.</p>
{{mermaid:""" + FIG2 + "|" + FIG2_ALT + "|" + FIG2_CAP + """}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽는 예약 함수의 차례입니다. 초록 예상 비용이 파란 검사 셋을 차례로 지나야 파란 칸 고치기 상자에 닿습니다. 맨 아래 노란 상자가 노트북 5절에서 한 번 예약한 뒤의 두 칸입니다. 오른쪽 노란 ValueError 상자로 가는 점선 셋은 검사에 걸릴 때만 가는 갈래입니다. 노트북에서는 8절이 검사 하나에, 7절이 검사 둘에, 9절이 검사 셋에 걸렸습니다.</p>
<p>함수 <code>reserve</code>는 검사 셋을 차례로 합니다. 하나라도 걸리면 <code>ValueError</code>를 내고 예산 칸을 고치지 않습니다. 모두 지나면 호출 수에 1을 더하고, 예상 비용 합계에 예상 비용을 더합니다. 함수에 넘긴 예산 딕셔너리를 함수 안에서 고치므로 밖에서도 바뀐 칸이 보입니다.</p>
<h2 id="b6"><span class="no">6</span>실패 확인</h2><p>아래 Before 셀은 예산을 만들어 두고도 보지 않는 흐름입니다. 질문 셋을 모두 보낼 목록에 담고 보내기 직전에서 멈춥니다. 이어지는 After 셀은 질문을 보내기 전마다 예약하고, 예약이 된 질문만 모델에 보냅니다.</p>
{{notebook:""" + SLUG + """|failure}}
{{mermaid:""" + FIG3 + "|" + FIG3_ALT + "|" + FIG3_CAP + """}}
<p class="look"><b>도식 읽기</b> — 왼쪽 칸이 Before이고 오른쪽 칸이 After입니다. 칸마다 맨 위 초록 상자가 같은 질문 셋이고, 맨 아래 회색 상자는 두 칸에 모두 해당합니다. 왼쪽 빨간 상자는 한도 둘을 넘는 요청까지 보낼 목록에 담은 결함입니다. 오른쪽은 파란 예약에서 화살표가 둘로 나뉘어 보낸 요청 둘과 멈춘 셋째 질문으로 갑니다. 모델 요청은 오른쪽 흐름에서만 두 번 보냈고 그림에는 모델 상자를 넣지 않았습니다.</p>
<p>두 흐름은 같은 질문 셋과 같은 한도를 썼고 예약을 했는지만 달랐습니다. 한도를 보지 않는 흐름은 출력 줄 <code>한도를 넘는 요청 수: 1</code>로 셋째 질문까지 목록에 담았습니다. 예약하는 흐름은 출력 줄 <code>예약하는 흐름 | 2 | 1</code>로 두 번만 보내고 하나를 멈췄습니다.</p><p>Before 흐름은 보내기 직전에서 멈췄고, 한도를 넘는 요청을 실제로 보내지는 않았습니다. 예약하는 흐름에서 셋째 질문은 호출 수 검사에서 막혀 모델에 가지 않았습니다. 새 커널로 두 번 실행했을 때 보낸 요청 수와 멈춘 질문은 두 번 모두 같았습니다. 모델이 쓴 답 문장은 실행마다 달라질 수 있어 본문에 옮기지 않았습니다.</p>
<p>값 바꿔 보기는 비용 상한만 0.01에서 0.003으로 낮췄습니다. 첫 질문을 보낸 뒤 둘째 질문의 예약이 출력 <code>비용 상한을 넘습니다.</code>로 막혔습니다. 모델에 보낸 요청은 하나였고 예산에 적힌 예상 비용은 0.002달러였습니다.</p>
{{mermaid:""" + FIG4 + "|" + FIG4_ALT + "|" + FIG4_CAP + """}}
<p class="look"><b>도식 읽기</b> — 왼쪽 칸이 노트북 7절의 비용 상한 0.01이고, 오른쪽 칸이 노트북 9절의 0.003입니다. 칸마다 초록 질문 셋에서 노란 결과로 갑니다. 왼쪽은 호출 한도가 셋째 질문을 막았고, 오른쪽은 비용 상한이 둘째 질문을 막았습니다. 맨 아래 회색 상자는 두 칸에 모두 해당하는 정한 값입니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>요청 하나의 예상 비용 0.002달러는 이 절에서 정한 값입니다. 요금표와 토큰 수로 센 값이 아니고 청구 금액도 아닙니다.</li><li>호출 한도 2와 비용 상한 0.01달러, 값 바꿔 보기의 0.003달러는 흐름을 보여 주려고 실행 전에 정한 예입니다.</li><li>한도를 보지 않는 흐름은 보내기 직전에서 멈췄습니다. 한도를 넘는 요청을 실제로 모델에 보내지는 않았습니다.</li><li>예약은 요청을 보내기 전에 적습니다. 그래서 요청이 실패해도 예약한 호출 수와 예상 비용은 그대로 남습니다. 이번 실행에서 실패한 요청은 없었습니다.</li><li>실제 사용량은 응답 뒤 <code>usage_metadata</code>의 토큰 수로만 봤습니다. 그 토큰 수로 비용을 다시 셈하지는 않았습니다.</li><li>모델 서비스가 정한 시간당 요청 수 제한은 이번에 다루지 않았습니다.</li><li>예산 딕셔너리는 노트북을 실행하는 동안만 있습니다. 커널을 다시 시작하면 예약한 양도 처음부터 다시 셉니다.</li><li>같은 요청도 실행한 때에 따라 답 문장과 토큰 수가 달라질 수 있습니다. 그래서 모델 답에는 <code>assert</code>를 쓰지 않았습니다. 예산 칸처럼 코드가 정하는 값에만 씁니다.</li><li>걸린 시간과 실제 비용은 재지 않았습니다. 요청 수와 요금 어림만 준비물에 적었습니다.</li><li>이 절은 파일을 쓰지 않습니다. 이 챕터 자료 파일은 읽기만 합니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>한 대화의 호출 한도와 비용 상한을 예산 딕셔너리에 담고, 부르기 전에 예약하는 함수를 만들었습니다.</li><li>한도를 보지 않는 흐름은 호출 한도 2를 넘는 셋째 질문까지 보낼 목록에 담았습니다.</li><li>예약하는 흐름은 셋째 질문을 부르기 전에 멈췄고, 비용 상한을 낮추자 둘째 질문에서 멈췄습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 05절에서는 실패한 요청을 다시 부르거나 예비 답을 내고, 감사 기록 파일에 남깁니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 이 절은 왜 응답을 받은 뒤가 아니라 모델을 부르기 전에 예약하나요?</p><p class="quiz-a">응답의 사용량은 요청이 나간 뒤에야 알 수 있기 때문입니다. 그때 한도를 넘은 것을 알아도 요청은 이미 나갔습니다. 틀렸다면 「핵심 개념」의 「예약은 부르기 전에 합니다」를 다시 읽습니다.</p><p class="quiz-q">2. 호출 한도가 2인 예산으로 질문 셋을 보내면 셋째 질문은 어떻게 되나요?</p><p class="quiz-a">예약에서 <code>호출 한도를 넘습니다.</code>로 막혀 모델에 가지 않습니다. 노트북 7절에서 모델에 보낸 요청은 둘이었습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">3. 예상 비용이 nan인지 <code>math.isfinite</code>로 먼저 보는 까닭은 무엇인가요?</p><p class="quiz-a">값 nan은 어떤 값과 견줘도 크다는 결과가 나오지 않습니다. 그래서 「상한보다 크면 막기」만 두면 그 검사를 그냥 지나갑니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">4. 예산에 적힌 예상 비용 0.004달러는 청구 금액인가요?</p><p class="quiz-a">아닙니다. 이 절에서 정한 요청 하나의 예상 비용 0.002달러를 두 번 더한 값입니다. 실제 사용량은 응답의 <code>usage_metadata</code>에 따로 있습니다. 틀렸다면 「핵심 개념」의 「예상 비용은 이 절에서 정한 값입니다」를 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.python.org/3.12/library/math.html#math.isfinite">math — Mathematical functions</a></div>확인 2026-09-23 · 함수 <code>math.isfinite</code>가 nan과 무한대에서 <code>False</code>를 내놓는다고 적어 둔 문서입니다.</li><li><div><a href="https://docs.python.org/3.12/library/functions.html#float">Built-in Functions · float</a></div>확인 2026-09-23 · 글 <code>"nan"</code>·<code>"inf"</code>로 특별한 값을 만드는 방법을 적어 둔 문서입니다.</li><li>Ch 6 06절 — 응답의 <code>usage_metadata</code>와 요금표로 요청 한 번의 예상 비용을 세기.</li><li>Ch 15 09절 — 보낸 요청의 예상 비용을 세기만 하고 상한으로 막지 않은 자리.</li></ul>
"""


def write_src() -> Path:
    SRC.write_text(SRC_HTML, encoding="utf-8")
    return SRC


if __name__ == "__main__":
    if os.environ.get("AUTHOR04_NB_ONLY") != "1":
        print("wrote", write_src())
    if "--src-only" not in sys.argv:
        path = write_notebook(LAB, "04", SLUG, "paired", cells())
        print("wrote", path)
