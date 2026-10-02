"""Ch 8의 복사·붙여넣기형 Jupyter Notebook 6개를 생성합니다."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOTEBOOKS = ROOT / "notebooks"


def markdown(text: str, *, lesson_part: str | None = None) -> dict:
    metadata = {"lesson_part": lesson_part} if lesson_part else {}
    return {"cell_type": "markdown", "metadata": metadata, "source": text.splitlines(keepends=True)}


def code(source: str, *, lesson_part: str | None = None) -> dict:
    metadata = {"lesson_part": lesson_part} if lesson_part else {}
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": metadata,
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


ENV_SETUP = """# find_dotenv는 현재 폴더부터 상위 폴더를 검색해 .env 경로를 찾습니다.
import os

from dotenv import find_dotenv, load_dotenv

# usecwd=True는 노트북을 실행한 폴더를 검색 시작점으로 지정합니다.
# 키 값은 출력하지 않고 존재 여부만 확인합니다.
env_path = find_dotenv(usecwd=True)
if not env_path:
    raise FileNotFoundError("현재 폴더의 상위 경로에서 .env를 찾지 못했습니다.")
load_dotenv(env_path)
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(".env에 OPENAI_API_KEY가 없습니다.")
print(".env와 API 키 확인 완료")"""

MODEL_SETUP = """# init_chat_model은 provider:model 형식으로 채팅 모델 객체를 만듭니다.
# model은 이후 셀에서 invoke()를 호출할 때 사용합니다.
from langchain.chat_models import init_chat_model

# openai:는 공급자 이름이며, reasoning_effort="none"은 별도 추론 토큰을 사용하지 않는 설정입니다.
# max_tokens=300은 생성할 출력 토큰 수의 상한입니다.
model = init_chat_model(
    "openai:gpt-5.4-mini",
    reasoning_effort="none",
    max_tokens=300,
)
print("LangChain 모델 준비 완료")"""


def setup_cells() -> list[dict]:
    return [
        code(ENV_SETUP),
        markdown("""### 모델 객체를 만듭니다

`.env` 확인이 끝난 뒤 모델 이름과 출력 제한을 지정합니다. 이 셀은 아직 API에 질문을 보내지 않습니다."""),
        code(MODEL_SETUP),
    ]

INSTALL = (
    '# %pip은 현재 노트북 커널에 패키지를 설치하는 Jupyter 전용 명령입니다.\n'
    '# -q는 설치 로그를 줄이고, == 뒤 숫자는 수업에서 검증한 버전을 고정합니다.\n'
    '%pip install -q "langchain==1.4.0" "langchain-openai==1.6.0" '
    '"python-dotenv==1.2.3" "tiktoken==0.14.0"'
)


def api_cells(prompt_name: str, instructions: str) -> list[dict]:
    return [
        markdown("""### 모델에 전달할 메시지를 만듭니다

`system`에는 답변 규칙을, `user`에는 앞에서 만든 질문을 넣습니다. 셀을 실행한 뒤 역할 순서를 확인합니다."""),
        code(f'''# messages는 역할과 내용을 짝지은 목록입니다.
# system 지시를 user 질문보다 먼저 둡니다.
messages = [
    ("system", "{instructions}"),
    ("user", {prompt_name}),
]
roles = []
for role, content in messages:
    roles.append(role)
print("메시지 역할:", roles)'''),
        markdown("""### 모델을 한 번 호출합니다

`invoke()`의 반환값은 `AIMessage`입니다. 사용량 정보가 없으면 이후 비교를 할 수 없으므로 즉시 오류를 냅니다."""),
        code('''# response는 모델의 답과 메타데이터를 가진 AIMessage입니다.
response = model.invoke(messages)
usage = response.usage_metadata

if usage is None:
    raise RuntimeError("모델 사용량 메타데이터가 없습니다.")'''),
        markdown("""### 답과 실제 토큰 수를 관찰합니다

먼저 답변 원문을 읽고, 다음 두 줄에서 API가 보고한 입력·출력 토큰 수를 확인합니다. 답변 문구와 수치는 실행마다 달라질 수 있습니다."""),
        code('''# text는 답변 문자열이고 usage는 실제 호출의 토큰 사용량입니다.
print(response.text)
print("input_tokens:", usage.get("input_tokens"))
print("output_tokens:", usage.get("output_tokens"))'''),
    ]


NOTEBOOK_DATA: dict[str, list[dict]] = {
    "01-컨텍스트와-토큰-예산": [
        markdown("""# 01. 컨텍스트와 토큰 예산

모델 호출에는 입력과 출력이 함께 들어갈 공간이 필요합니다. 이 노트북에서는 입력 길이를 호출 전에 추정하고, 실제 API 사용량과 비교합니다."""),
        markdown("""## 1. API 연결 준비

아래 셀은 현재 작업 폴더에서 상위 폴더로 올라가며 `.env`를 찾습니다. 키 값은 화면에 출력하지 않습니다."""),
        *setup_cells(),
        markdown('## 2. 출력 공간을 먼저 예약합니다\n\n전체 예산에서 출력 예약분과 안전 여유를 빼면 입력에 사용할 수 있는 범위가 나옵니다.\n\n`input_budget()`는 직접 작성하는 산술 함수입니다. 세 인자를 빼서 입력 배정량 하나를 반환하며 모델을 호출하지 않습니다. `total=4096`은 수업에서 정한 배정량입니다. 모델의 최대 컨텍스트를 조회한 결과로 읽지 않습니다.\n\n한 줄 분류와 여러 문단 설명은 필요한 출력 공간이 다릅니다. 뒤에서 출력 예약량을 600으로 바꾸는 셀은 입력 배정량의 감소만 계산합니다. 앞의 모델 객체에 지정한 `max_tokens=300`을 변경하지는 않습니다.'),
        code("""# total은 전체 한도, output_reserve는 답변용 예약분입니다.
# safety_margin은 토큰 추정 오차를 위한 여유입니다.
def input_budget(total: int, output_reserve: int, safety_margin: int) -> int:
    available = total - output_reserve - safety_margin

    if available < 0:
        raise ValueError("출력 예약분과 여유가 전체 예산보다 큽니다.")

    return available
"""),
        markdown("""### 세 값을 넣어 반환값을 확인합니다

전체 한도 `4096`에서 출력 예약분 `300`과 안전 여유 `128`을 뺍니다. 반환된 숫자는 `available`에 저장됩니다."""),
        code("""# 세 인자는 함수 정의에 적힌 순서대로 전달합니다.
available = input_budget(4096, 300, 128)
print("입력에 사용할 수 있는 토큰:", available)"""),
        markdown("""## 3. 로컬 추정값을 확인합니다

토크나이저는 문장을 모델이 세는 작은 단위인 토큰으로 나누어, 호출 전에 입력 크기를 추정합니다. 실제 호출 뒤에는 응답 객체의 `AIMessage.usage_metadata`에서 제공자가 센 토큰 수를 확인합니다."""),
        code('''# question은 질문이고 evidence는 답변 근거입니다.
import tiktoken

question = "미르시립도서관의 정기 휴관일은 언제인가요?"
evidence = "[E01 p.2] 정기 휴관일은 매주 월요일입니다."
prompt = f"""근거:
{evidence}

질문: {question}"""
print(prompt)'''),
        markdown('### 같은 문자열을 토큰으로 바꿉니다\n\n`encode()`는 문자열을 토큰 ID 목록으로 반환합니다. 목록 길이를 세어 호출 전 입력 크기를 추정합니다.\n\n`get_encoding("o200k_base")`는 지정한 토큰화 규칙을 불러오고 `encode(prompt)`는 문자열을 토큰 ID 목록으로 바꿉니다. 여기서 세는 대상은 `prompt` 문자열뿐입니다. 뒤의 system 메시지와 메시지 형식까지 포함한 실제 입력 사용량은 응답의 `usage_metadata`에서 따로 확인합니다.'),
        code('''# 실제 API 입력에는 system 메시지와 채팅 형식용 토큰도 더해집니다.
encoding = tiktoken.get_encoding("o200k_base")
token_ids = encoding.encode(prompt)
estimated = len(token_ids)
print("로컬 추정 입력 토큰:", estimated)
print("예산 안에 있음:", estimated <= available)'''),
        markdown("""## 4. 실제 API 사용량을 비교합니다

`AIMessage.text`와 `usage_metadata`를 함께 확인합니다. 출력은 실행마다 달라질 수 있습니다."""),
        *api_cells("prompt", "근거에 있는 정보만 사용하고 출처를 표시하세요."),
        markdown("""## 5. 출력 예약분 한 값만 바꿔 비교합니다

전체 한도와 안전 여유는 유지하고 출력 예약분만 `300`에서 `600`으로 늘립니다. 입력 예산이 얼마나 줄어드는지 확인합니다."""),
        code("""# 두 호출은 output_reserve 값 하나만 다릅니다.
base_budget = input_budget(4096, 300, 128)
changed_budget = input_budget(4096, 600, 128)
print("기본 입력 예산:", base_budget)
print("변경 입력 예산:", changed_budget)
print("차이:", changed_budget - base_budget)"""),
        markdown("""## 정리

출력 공간을 먼저 예약하고, 입력을 로컬에서 추정한 뒤, 실제 사용량은 API 응답에서 확인합니다."""),
        markdown(
            """## 실패 재현: 출력 공간을 남기지 않습니다

전체 예산보다 출력 예약분과 여유를 크게 설정하면 준비한 입력을 넣을 공간이 없습니다. 같은 입력 길이를 수정 전후 허용량과 비교합니다.""",
            lesson_part="before",
        ),
        code(
            """# planned_input은 모델에 넣으려는 입력의 길이입니다.
# 잘못된 전체 예산에서는 입력 허용량을 계산할 수 없습니다.
planned_input = 500
bad_total = 300
try:
    bad_available = input_budget(bad_total, 300, 128)
except ValueError as error:
    print("관찰한 실패:", error)
    print("준비한 입력 토큰:", planned_input, "> 허용량 없음")
else:
    raise AssertionError("예산 오류가 발생해야 합니다.")""",
            lesson_part="before",
        ),
        markdown(
            """## 수정: 전체 예산을 복원합니다

같은 500토큰 입력은 유지합니다. 모델 한도를 바꾸는 것이 아니라 수업에서 정한 작업 예산을 4,096토큰으로 고친 뒤 입력 허용량 안에 들어가는지 확인합니다.""",
            lesson_part="after",
        ),
        code(
            """# 입력 길이는 그대로 두고 전체 예산만 복원합니다.
# 출력 예약분과 여유를 빼도 500토큰 입력을 넣을 수 있어야 합니다.
fixed_total = 4096
fixed_available = input_budget(fixed_total, 300, 128)
assert fixed_available == 3668
assert planned_input <= fixed_available
print("준비한 입력 토큰:", planned_input)
print("수정 후 입력 허용량:", fixed_available)
print("입력 가능:", planned_input <= fixed_available)""",
            lesson_part="after",
        ),
    ],
    "02-Write와-Select": [
        markdown("""# 02. Write와 Select

Write는 정보를 외부 기록에 남기는 단계이고, Select는 현재 질문에 필요한 기록만 고르는 단계입니다."""),
        markdown("""## 1. API 연결 준비

각 노트북은 빈 커널에서 시작할 수 있도록 연결 코드를 포함합니다."""),
        *setup_cells(),
        markdown("""## 2. 기록을 JSON으로 저장하고 다시 읽습니다

예제 데이터는 코드 안에 직접 적습니다. `effective_date`는 날짜 필터를 관찰하기 위한 합성 메타데이터이며, PDF의 발행일이나 실제 규정 시행일을 뜻하지 않습니다. 저장 파일은 운영체제의 임시 폴더에 만들기 때문에 노트북을 어느 폴더에서 열어도 실행할 수 있습니다."""),
        code("""# 각 기록에는 선택에 쓸 기관·주제·적용일과 답에 쓸 본문이 있습니다.
import json
from pathlib import Path
from tempfile import gettempdir

records = [
    {"id": "E01-p2", "institution": "미르시립도서관", "topic": "휴관",
     "effective_date": "2025-01-01", "text": "매주 월요일 휴관"},
    {"id": "E01-p3", "institution": "미르시립도서관", "topic": "대출",
     "effective_date": "2025-01-01", "text": "7권, 14일 대출"},
    {"id": "E01-p5", "institution": "미르시립도서관", "topic": "주차",
     "effective_date": "2025-01-01", "text": "회원은 최초 2시간 무료입니다."},
]
print("저장할 기록:", len(records))"""),
        markdown('### 임시 파일에 기록을 씁니다\n\n`gettempdir()`를 사용하므로 노트북을 어느 폴더에서 열어도 같은 방식으로 실행됩니다. 출력된 이름으로 저장 파일을 확인합니다.\n\n`Path(gettempdir()) / "ch08-memory.json"`은 임시 폴더에 파일 이름을 연결한 경로입니다. `json.dumps()`는 목록을 JSON 문자열로 바꾸고 `write_text()`가 그 문자열을 저장합니다. 고정 파일 이름이므로 이 셀을 다시 실행하면 같은 이름의 기록을 덮어씁니다. 장기 보존이나 여러 사용자의 저장을 설계한 예제는 아닙니다.'),
        code("""# ensure_ascii=False는 한국어를 그대로 JSON에 기록합니다.
memory_path = Path(gettempdir()) / "ch08-memory.json"
json_text = json.dumps(records, ensure_ascii=False)
memory_path.write_text(json_text, encoding="utf-8")
print("임시 폴더에 저장한 파일:", memory_path.name)"""),
        markdown("""### 파일을 다시 읽어 중간 결과를 확인합니다

`read_text()`는 문자열을 반환하고, `json.loads()`는 그 문자열을 파이썬 목록으로 복원합니다."""),
        code("""# loaded에는 파일에서 복원한 기록 목록이 저장됩니다.
saved_text = memory_path.read_text(encoding="utf-8")
loaded = json.loads(saved_text)
print("다시 읽은 기록:", len(loaded))"""),
        markdown('## 3. 질문에 필요한 기록만 선택합니다\n\n기관·주제·질문 날짜를 코드에 적고, 세 조건이 맞는 기록의 ID를 고릅니다. 자동 검색은 Ch 9에서 다룹니다.\n\n`topics`는 필요한 주제의 집합이고 `in`은 포함 여부를 검사합니다. 세 조건을 `and`로 연결하므로 모두 참인 기록만 ID 집합에 넣습니다. 이어지는 반복문은 `loaded`의 원래 순서로 선택한 기록을 모읍니다.\n\n예를 들어 같은 상품의 2025년과 2026년 설명서가 모두 기준일 전에 시행되었다면 두 문서가 함께 선택될 수 있습니다. 아래 조건은 최신 버전 하나를 고르거나 폐기 여부를 확인하지 않습니다. 질문의 기관·주제·날짜 역시 사람이 정한 값이며 모델이 질문에서 자동 추출하지 않습니다.'),
        code("""# criteria는 질문에서 확인한 기관·주제·날짜입니다.
criteria = {
    "institution": "미르시립도서관",
    "topics": {"대출", "주차"},
    "as_of": "2026-09-08",
}
selected_ids = set()
for row in loaded:
    same_institution = row["institution"] == criteria["institution"]
    needed_topic = row["topic"] in criteria["topics"]
    already_effective = row["effective_date"] <= criteria["as_of"]
    if same_institution and needed_topic and already_effective:
        selected_ids.add(row["id"])

selected = []
for row in loaded:
    if row["id"] in selected_ids:
        selected.append(row)

for row in selected:
    print(row["id"], row["topic"], row["text"])"""),
        markdown("""## 4. 선택한 기록으로 답을 생성합니다

모델에는 저장소 전체 대신 선택한 두 기록만 전달합니다."""),
        code('''# context_lines에 출처 ID와 내용을 한 줄씩 추가합니다.
context_lines = []
for row in selected:
    line = f"[{row['id']}] {row['text']}"
    context_lines.append(line)

context = "\\n".join(context_lines)
prompt = f"""근거:
{context}

질문: 대출 권수와 주차 무료 시간을 알려 주세요."""
print(prompt)'''),
        *api_cells("prompt", "제공된 근거만 사용하고 문장마다 식별자를 붙이세요."),
        markdown("""## 5. 선택 ID 한 개를 줄여 비교합니다

기본 선택에는 대출과 주차가 들어 있습니다. 주차 ID 하나를 제외한 뒤 선택된 기록 수와 주제를 비교합니다."""),
        code("""# changed_ids에서는 E01-p5 하나만 제외합니다.
changed_ids = selected_ids - {"E01-p5"}
changed_selected = []
for row in loaded:
    if row["id"] in changed_ids:
        changed_selected.append(row)

print("기본 선택 수:", len(selected))
print("변경 선택 수:", len(changed_selected))
print("변경 후 주제:", changed_selected[0]["topic"])"""),
        markdown("""## 정리

외부 기록은 저장만으로 모델에 전달되지 않습니다. 질문에 맞는 항목을 선택하여 호출 입력에 넣어야 합니다."""),
        markdown(
            '''## 실패 재현: 저장한 기록을 메시지에 넣지 않습니다

파일에는 세 기록이 있지만 모델에는 빈 근거를 전달합니다. 대출 권수와 주차 시간을 답할 정보가 실제 메시지에 있는지 확인합니다.''',
            lesson_part="before",
        ),
        code(
            '''# 두 호출에서 질문과 답변 규칙은 그대로 사용합니다.
question = "대출 권수와 주차 무료 시간을 알려 주세요."
answer_rule = "제공된 근거만 사용하고 문장마다 식별자를 붙이세요. 근거가 없으면 모른다고 답하세요."
# 빈 문자열은 저장 파일의 본문을 메시지에 옮기지 않은 상태입니다.
missing_context = ""
before_prompt = f"""근거:
{missing_context}

질문: {question}"""
print(before_prompt)''',
            lesson_part="before",
        ),
        markdown(
            '''### 근거가 없는 메시지로 실제 답을 확인합니다

`invoke()`에 파일 경로를 전달하지 않았고, 메시지에도 본문이 없습니다. 모델은 저장 파일의 내용을 자동으로 읽지 않습니다. 출력 문구는 실행마다 달라집니다.''',
            lesson_part="before",
        ),
        code(
            '''# 근거가 비어 있으면 정확한 권수와 시간을 답할 수 없는지 읽습니다.
before_response = model.invoke([
    ("system", answer_rule),
    ("user", before_prompt),
])
print(before_response.text)''',
            lesson_part="before",
        ),
        markdown(
            '''## 수정: 선택한 기록을 같은 질문의 근거로 넣습니다

앞에서 만든 `context`에는 대출·주차 본문과 출처 ID가 있습니다. 근거 영역만 이 값으로 바꾸어 다시 호출합니다. 답의 7권·2시간과 출처 ID를 원래 기록과 비교합니다.''',
            lesson_part="after",
        ),
        code(
            '''# context는 앞에서 selected의 본문과 출처 ID를 연결한 문자열입니다.
after_prompt = f"""근거:
{context}

질문: {question}"""
after_response = model.invoke([
    ("system", answer_rule),
    ("user", after_prompt),
])
print("전달한 근거:", context)
print("모델 답:", after_response.text)''',
            lesson_part="after",
        ),
    ],
    "03-Compress와-Isolate": [
        markdown("""# 03. Compress와 Isolate

Compress는 한 기록에서 필요한 사실을 남기고 반복 표현을 줄입니다. Isolate는 대출과 휴관처럼 서로 다른 질문의 근거가 한 메시지에 섞이지 않게 나눕니다."""),
        markdown("""## 1. API 연결 준비"""),
        *setup_cells(),
        markdown('## 2. 사실·조건·예외·출처를 보존합니다\n\n길이만 줄이면 중요한 예외를 잃을 수 있습니다. 네 필드를 모두 확인한 뒤 한 줄로 압축합니다.\n\n`compress(record)`의 입력은 사람이 이미 골라 적은 네 항목의 딕셔너리이고 반환값은 이를 연결한 문자열입니다. 원문을 자동 요약하거나 모델을 호출하는 함수가 아닙니다. `set(required) - record.keys()`는 빠진 키를 찾으며, 각 값의 진실성이나 원문과의 일치까지 검사하지 않습니다.\n\n회의 기록에서 “검토가 완료되면 금요일 배포”를 “금요일 배포”로 줄이면 적용 조건이 사라집니다. 아래 대출 규정도 같은 관점으로 원문과 조건을 비교합니다. 이후 서로 다른 메시지 목록을 만드는 작업은 입력 자료를 나누는 것으로, 운영체제의 접근 권한이나 보안 격리를 설정하지 않습니다.'),
        code("""# record는 사실·조건·예외·출처를 가진 사전입니다.
# required 튜플은 압축 결과의 필드 순서를 고정합니다.
def compress(record: dict[str, str]) -> str:
    required = ("fact", "condition", "exception", "source")
    missing = set(required) - record.keys()

    if missing:
        raise ValueError(f"빠진 필드: {sorted(missing)}")

    parts = []
    for key in required:
        parts.append(f"{key}: {record[key]}")

    return " | ".join(parts)"""),
        markdown("""### 압축할 원본을 준비합니다

긴 원문을 읽고 답에 필요한 사실·조건·예외·출처를 짧은 사전에 옮깁니다. 다음 셀에서 원문과 압축 결과의 길이를 비교합니다."""),
        code("""# loan_original은 반복 설명이 있는 원문이고 loan은 남길 내용만 정리한 사전입니다.
loan_original = (
    "미르시립도서관 일반 회원 한 명은 일반자료를 모두 합해 7권까지 빌릴 수 있습니다. "
    "기본 대출 기간은 빌린 날부터 14일입니다. "
    "다른 회원의 예약이 들어오지 않은 자료만 1회에 한해 7일 연장할 수 있습니다. "
    "이 규정의 출처는 E01 문서 3쪽입니다."
)
loan = {
    "fact": "7권을 14일 대출",
    "condition": "회원 1명 기준",
    "exception": "예약이 없으면 1회 7일 연장",
    "source": "E01 p.3",
}
print("원본 필드:", list(loan))"""),
        markdown("""### 함수의 반환값을 관찰합니다

`compressed`에는 네 필드가 정해진 순서로 연결됩니다. 원문보다 짧으면서 조건이 남았는지 확인합니다."""),
        code("""# 문자 수 비교는 이 예에서 실제로 표현이 줄었는지 보여 줍니다.
compressed = compress(loan)
assert len(compressed) < len(loan_original)
print("원문 문자 수:", len(loan_original))
print("압축 문자 수:", len(compressed))
print(compressed)"""),
        markdown("""## 3. 서로 다른 주제의 근거를 함께 놓아 봅니다

대출 규정 옆에 휴관 규정을 추가합니다. 먼저 두 주제가 섞인 문자열을 출력해 분리 전 상태를 관찰합니다."""),
        code("""# closure도 같은 네 필드를 가진 레코드입니다.
closure = {
    "fact": "매주 월요일 휴관",
    "condition": "정기 휴관일 기준",
    "exception": "공휴일이 월요일과 겹치면 다음 화요일도 휴관",
    "source": "E01 p.2",
}
closure_compressed = compress(closure)
mixed_context = compressed + "\\n" + closure_compressed
print("분리 전 근거:\\n", mixed_context)"""),
        markdown('## 4. 질문별 메시지를 두 묶음으로 분리합니다\n\n대출 질문에는 대출 근거만, 휴관 질문에는 휴관 근거만 넣습니다. 각 메시지의 사용자 내용을 출력해 출처가 섞이지 않았는지 확인합니다.\n\n`loan_messages`와 `closure_messages`는 서로 다른 입력 목록입니다. 각각 필요한 규정만 포함한 뒤 별도로 호출합니다. 뒤의 `assert`는 특정 출처 ID가 다른 입력에 없는지 확인할 뿐, 모든 정보 유출 가능성을 검사하지 않습니다.'),
        code('''# 두 목록은 서로 독립된 모델 입력입니다.
loan_messages = [
    ("system", "근거의 조건·예외·출처를 빠뜨리지 마세요."),
    ("user", f"근거: {compressed}\\n질문: 대출과 연장 조건은?"),
]
closure_messages = [
    ("system", "근거의 조건·예외·출처를 빠뜨리지 마세요."),
    ("user", f"근거: {closure_compressed}\\n질문: 정기 휴관일은?"),
]
print("대출 메시지:\\n", loan_messages[1][1])
print("휴관 메시지:\\n", closure_messages[1][1])'''),
        markdown("""### 분리 결과를 코드로 확인합니다

대출 메시지에는 휴관 출처가 없고, 휴관 메시지에는 대출 출처가 없어야 합니다."""),
        code('''# not in 검사는 다른 주제의 출처가 섞이지 않았는지 확인합니다.
assert "E01 p.2" not in loan_messages[1][1]
assert "E01 p.3" not in closure_messages[1][1]
print("질문별 근거 분리 확인 완료")'''),
        markdown("""### 분리한 두 메시지를 각각 실행합니다

두 호출의 답변을 주제 이름과 함께 출력합니다. 답변 문구는 실행마다 달라질 수 있습니다."""),
        code('''# 각 invoke()에는 해당 질문의 메시지 목록 하나만 전달합니다.
isolated_messages = {
    "대출": loan_messages,
    "휴관": closure_messages,
}
for topic, messages in isolated_messages.items():
    response = model.invoke(messages)
    print(f"[{topic}]", response.text)'''),
        markdown("""## 5. 조건 값 한 개를 바꿔 비교합니다

원본을 복사한 뒤 `condition` 값만 더 구체적으로 바꿉니다. 두 압축 문자열에서 달라진 부분을 확인합니다."""),
        code("""# copy()를 사용하면 원본 loan은 그대로 유지됩니다.
changed_loan = loan.copy()
changed_loan["condition"] = "회원 한 사람의 도서 대출 기준"
changed_compressed = compress(changed_loan)
print("기본 압축:", compressed)
print("변경 압축:", changed_compressed)"""),
        markdown("""## 정리

압축은 짧게 만드는 작업과 보존해야 할 필드를 검사하는 작업을 함께 수행합니다. 질문별 입력은 호출 전에 분리합니다."""),
        markdown(
            """## 실패 재현: 연장 조건을 빼고 결과를 줄입니다

같은 원문에서 ‘1회 7일 연장’만 남기면 예약이 있는 자료도 연장할 수 있는 것처럼 읽힙니다. 빠진 조건을 문자열에서 직접 확인합니다.""",
            lesson_part="before",
        ),
        code(
            """# broken_summary는 원문의 연장 횟수와 기간만 남기고 적용 조건을 뺀 요약입니다.
broken_summary = "7권을 14일 대출, 1회 7일 연장 [E01 p.3]"
condition_preserved = "예약이 없으면" in broken_summary
assert not condition_preserved
print("조건이 빠진 요약:", broken_summary)
print("연장 조건 보존:", condition_preserved)""",
            lesson_part="before",
        ),
        markdown(
            """## 수정: 원문의 연장 조건을 복원합니다

같은 사실·기간·출처를 유지하고 ‘예약이 없으면’이라는 조건만 되돌립니다. 두 요약에서 달라진 문구를 확인합니다.""",
            lesson_part="after",
        ),
        code(
            """# fixed_summary는 broken_summary에 빠졌던 조건을 원문 표현대로 복원합니다.
fixed_summary = "7권을 14일 대출, 예약이 없으면 1회 7일 연장 [E01 p.3]"
condition_preserved = "예약이 없으면" in fixed_summary
assert condition_preserved
print("조건을 복원한 요약:", fixed_summary)
print("연장 조건 보존:", condition_preserved)""",
            lesson_part="after",
        ),
    ],
    "04-네-가지-실패-모드": [
        markdown("""# 04. 네 가지 실패 모드

네 이름은 잘못된 정보, 무관한 정보, 비슷한 대상, 서로 충돌하는 규정이 입력에 들어간 문제를 살펴볼 때 씁니다. 한 사례에 여러 문제가 함께 나타날 수 있습니다. 문제 문장을 넣은 사실과 모델 답에서 실제 오류를 확인한 사실은 따로 기록합니다."""),
        markdown("""## 1. API 연결 준비"""),
        *setup_cells(),
        markdown("""## 2. 다섯 가지 입력 조건을 만듭니다

기준 입력을 유지하면서 잘못된 메모, 무관한 정보, 비슷한 기관, 상충 규정을 하나씩 추가합니다."""),
        code('''# clean은 비교의 기준이 되는 근거입니다.
# noise는 길이만 늘리는 무관한 문장입니다.
clean = "[E01 p.2] 미르시립도서관의 정기 휴관일은 오직 매주 월요일 하루뿐입니다."
noise = "회의 안건: 행사 배너와 좌석 배치를 논의했습니다. " * 12
print("기준 문자 수:", len(clean))
print("무관한 문장 문자 수:", len(noise))'''),
        markdown("""### 기준 입력에 문제 문장을 하나씩 추가합니다

각 조건은 정상 입력인 `clean`을 그대로 두고, 잘못된 메모·무관한 문장·비슷한 기관·상충 규정 중 하나만 더합니다. 조건 이름과 실제로 추가한 문장을 함께 읽습니다."""),
        code('''# conditions는 기준 입력과 네 실패 자극을 이름별로 보관합니다.
conditions = {
    "clean": clean,
    "poisoning": f"""{clean}
[미검증 메모] 휴관일은 화요일입니다.""",
    "distraction": f"""{noise}
{clean}""",
    "confusion": f"""{clean}
[미르고등학교 도서실] 화요일 휴관입니다.""",
    "clash": f"""{clean}
[합성 부록] 미르시립도서관의 정기 휴관일은 오직 매주 화요일 하루뿐입니다.""",
}
print("실험 조건:", list(conditions))'''),
        markdown('## 3. 같은 질문으로 다섯 조건을 실행합니다\n\n어떤 실패가 나타날지 미리 정하지 않습니다. 조건 이름, 실제 입력 토큰, 응답 원문을 나란히 기록합니다.\n\n`conditions.items()`는 조건 이름과 입력 내용을 쌍으로 제공합니다. `results[name] = response`는 해당 이름에 실제 응답 객체를 저장합니다. 이름은 개발자가 붙인 실험 조건이며 모델 오류를 자동 진단한 값이 아닙니다.\n\n일반 배송 3일과 도서 지역 배송 5일은 적용 조건이 다릅니다. 같은 조건에 서로 다른 값이 있을 때 충돌을 검토합니다. 이처럼 입력에서 의심할 문제와 실제 출력에서 확인한 오류를 나누어 기록합니다.'),
        code('''# items()는 조건 이름과 근거를 한 쌍씩 반환하며 모든 조건에 같은 질문을 적용합니다.
# results에는 조건별 AIMessage를 저장하고, usage에서 실제 입력 토큰 수를 읽습니다.
results = {}
for name, context in conditions.items():
    messages = [
        ("system", "근거만 사용하고, 충돌하면 확인이 필요하다고 답하세요."),
        ("user", f"""근거:
{context}

질문: 미르시립도서관의 정기 휴관일은 언제인가요?"""),
    ]
    response = model.invoke(messages)
    usage = response.usage_metadata
    if usage is None:
        raise RuntimeError("모델 사용량 메타데이터가 없습니다.")
    results[name] = response
    print(f"\\n[{name}] input_tokens={usage['input_tokens']}")
    print(response.text)'''),
        markdown("""## 4. 출력에서 관찰한 문자열을 비교합니다

요일과 추가 확인 요청이 답에 있는지만 표시합니다. 이 표는 문자열의 포함 여부만 보여 주므로, 답 전체가 맞는지는 응답 원문을 함께 읽어 판단합니다."""),
        code("""# 각 응답에서 요일 문자열과 추가 확인 표현을 차례로 검사합니다.
for name, response in results.items():
    answer = response.text
    observed = []
    for day in ("월요일", "화요일", "수요일"):
        if day in answer:
            observed.append(day)

    if "확인" in answer or "충돌" in answer or "상충" in answer:
        observed.append("추가 확인 표현")

    if not observed:
        observed = ["요일 표현 없음"]
    print(name, observed)"""),
        markdown("""## 5. 무관 문장 반복 횟수 한 값만 바꿉니다

근거와 질문은 유지하고 반복 횟수만 `12`에서 `24`로 늘립니다. 이 셀은 추가 API 호출 없이 입력 길이 변화만 비교합니다."""),
        code("""# changed_noise는 같은 문장을 24번 연결한 문자열입니다.
changed_noise = "회의 안건: 행사 배너와 좌석 배치를 논의했습니다. " * 24
base_context = noise + clean
changed_context = changed_noise + clean
print("기본 문자 수:", len(base_context))
print("변경 문자 수:", len(changed_context))"""),
        markdown("""## 정리

실패가 나도록 문제 문장을 넣었다고 해서 모델이 실제로 틀렸다고 기록하지 않습니다. 모델 답에서 확인한 문장을 어떤 입력과 함께 보냈는지 연결해 기록합니다."""),
        markdown(
            '''## 실패 재현: 상충 규정의 시행일을 기록하지 않습니다

월요일 하루만 휴관한다는 규정과 화요일 하루만 휴관한다는 규정을 함께 전달합니다. 질문 날짜는 같지만 규정의 시행일이 없어 어느 쪽을 적용할지 알 수 없습니다.''',
            lesson_part="before",
        ),
        code(
            '''# 비교할 날짜와 질문을 먼저 고정합니다.
as_of = "2026-09-08"
question = f"{as_of} 기준 미르시립도서관의 정기 휴관일은 언제인가요?"
# 두 호출 모두 같은 규칙을 사용합니다. 모르는 날짜를 추측하지 않게 합니다.
answer_rule = "근거만 사용하고 출처를 표시하세요. 규정이 충돌하고 시행일을 알 수 없으면 확인이 필요하다고 답하세요."
before_context = conditions["clash"]
print(before_context)''',
            lesson_part="before",
        ),
        markdown(
            '''### 같은 질문으로 실제 답을 읽습니다

임의의 오류를 내는 검사 대신 모델이 두 규정을 어떻게 설명하는지 확인합니다. 확인이 필요하다고 답했다면 잘못된 규정을 고른 실패는 관찰되지 않은 것입니다. 다만 현재 자료만으로 질문에 확정 답변을 할 수는 없습니다.''',
            lesson_part="before",
        ),
        code(
            '''# 두 규정의 본문과 질문을 그대로 전달합니다.
before_prompt = f"""근거:
{before_context}

질문: {question}"""
before_response = model.invoke([
    ("system", answer_rule),
    ("user", before_prompt),
])
print(before_response.text)''',
            lesson_part="before",
        ),
        markdown(
            '## 수정: 확인한 시행일로 적용할 규정을 고릅니다\n\n이 연습에서는 기관에 확인한 결과 기존 규정의 시행일은 2025-01-01, 대체 규정의 시행일은 2026-01-01이라고 가정합니다. 날짜는 실습용으로 정한 값이며 실제 기관의 규정이 아닙니다. 두 규정의 본문은 그대로 두고, 같은 업무의 새 규정이 이전 규정을 대체한다는 조건에서 기준일까지 시행된 가장 최근 규정을 선택합니다.\n\n`eligible`은 기준일 전에 시행된 후보 목록입니다. `max(eligible, key=effective_date)`는 각 후보를 `effective_date()`에 넘겨 얻은 날짜 문자열을 비교합니다. 함수 이름을 넘기므로 비교할 때마다 필요한 후보의 날짜를 읽습니다. 후보가 비어 있거나 서로 다른 날짜 형식이 섞인 경우는 이 예제의 입력에 없으며 실제 처리에서는 별도 분기가 필요합니다.',
            lesson_part="after",
        ),
        code(
            '''# versioned는 같은 두 규정에 시행일만 추가한 목록이고 as_of는 질문한 날짜입니다.
# eligible에서 기준일까지 시행된 규정만 남긴 뒤 max의 key로 가장 최근 시행일을 고릅니다.
# YYYY-MM-DD처럼 자릿수가 고정된 날짜는 문자열 순서와 날짜 순서가 같습니다. 다른 형식은 날짜 객체로 바꿉니다.
versioned = [
    {"effective_date": "2025-01-01", "rule": clean, "source": "E01 p.2"},
    {"effective_date": "2026-01-01", "rule": conditions["clash"].splitlines()[-1],
     "source": "합성 부록"},
]
eligible = []
for record in versioned:
    if record["effective_date"] <= as_of:
        eligible.append(record)

def effective_date(record: dict[str, str]) -> str:
    return record["effective_date"]

selected_rule = max(eligible, key=effective_date)
assert "오직 매주 화요일 하루뿐" in selected_rule["rule"]
assert selected_rule["source"] == "합성 부록"
print("수정 후 적용 규정:", selected_rule)''',
            lesson_part="after",
        ),
        markdown(
            '''### 선택한 규정으로 같은 질문에 다시 답합니다

새 규정을 고른 결과를 근거로 넣습니다. 질문·모델·답변 규칙은 Before와 같습니다. 실제 답이 화요일과 선택한 출처를 사용하는지 확인합니다. 이는 시행일을 확인하고 선택한 효과이며, 모델 자체의 성능이 높아졌다는 뜻은 아닙니다.''',
            lesson_part="after",
        ),
        code(
            '''# 날짜로 선택한 규정만 모델에 전달합니다.
after_prompt = f"""근거:
{selected_rule['rule']}
시행일: {selected_rule['effective_date']}

질문: {question}"""
after_response = model.invoke([
    ("system", answer_rule),
    ("user", after_prompt),
])
print(after_response.text)''',
            lesson_part="after",
        ),
    ],
    "05-Context-rot-측정": [
        markdown('''# 05. 입력 길이에 따라 정답을 활용하는 성능이 달라질까요?

같은 질문·정답 근거·모델을 사용하고, 근거 앞뒤의 무관한 문장 수만 늘립니다. 세 길이를 각각 세 번 호출하여 답과 입력 토큰, 정답 확인 결과를 기록합니다. 성능 저하가 나오는지는 실행 후 판단합니다. 토큰 수가 늘었다는 사실만으로 context rot가 나타났다고 결론 내리지 않습니다.'''),
        markdown('''## 1. 실행 환경 준비

Python 3.12 커널에서 아래 셀을 순서대로 실행합니다. 프로젝트 폴더 또는 상위 폴더의 `.env`에 OPENAI_API_KEY를 둡니다. 이 실습은 생성 API를 총 아홉 번 호출합니다.'''),
        code('''# find_dotenv는 현재 폴더부터 상위 폴더를 검색해 .env 경로를 찾습니다.
import os

from dotenv import find_dotenv, load_dotenv

# usecwd=True는 노트북을 실행한 폴더를 검색 시작점으로 지정합니다.
# 키 값은 출력하지 않고 존재 여부만 확인합니다.
env_path = find_dotenv(usecwd=True)
if not env_path:
    raise FileNotFoundError("현재 폴더의 상위 경로에서 .env를 찾지 못했습니다.")
load_dotenv(env_path)
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(".env에 OPENAI_API_KEY가 없습니다.")
print(".env와 API 키 확인 완료")'''),
        code('''# init_chat_model은 provider:model 형식으로 채팅 모델 객체를 만듭니다.
# model은 이후 셀에서 invoke()를 호출할 때 사용합니다.
from langchain.chat_models import init_chat_model

# openai:는 공급자 이름이며, reasoning_effort="none"은 별도 추론 토큰을 사용하지 않는 설정입니다.
# max_tokens=300은 생성할 출력 토큰 수의 상한입니다.
model = init_chat_model(
    "openai:gpt-5.4-mini",
    reasoning_effort="none",
    max_tokens=300,
)
print("LangChain 모델 준비 완료")'''),
        markdown('''## 2. 모든 조건에서 같은 문제를 사용합니다

답에 필요한 정보는 아래 근거 문장 하나에 있습니다. 모델은 휴관일과 출처를 답해야 합니다. 근거 문장과 질문을 바꾸면 문제 자체가 달라지므로 두 값을 고정합니다.'''),
        code('''# evidence는 정답을 포함한 자료이며 question은 모든 실행에 사용하는 질문입니다.
evidence = "[E01 p.2] 정기 휴관일은 매주 월요일입니다."
question = "미르시립도서관의 정기 휴관일과 출처를 알려 주세요."
# note는 휴관일 답변에 필요하지 않은 주변 문장입니다.
note = "회의 준비 항목을 확인했습니다. "
print("질문:", question)
print("정답 근거:", evidence)'''),
        markdown('''## 3. 근거를 가운데에 두고 주변 문장 수만 바꿉니다

0·120·1,200은 근거의 각 앞뒤에 붙일 문장의 반복 수입니다. 토큰 수가 아닙니다. 실제 입력 토큰 수는 모델 호출 후 확인합니다. 근거를 입력 자료 가운데에 두는 배치 규칙은 세 조건에서 같습니다.'''),
        code('''# 조건 이름과 근거 한쪽에 붙일 반복 수를 딕셔너리로 정합니다.
repeat_counts = {"short": 0, "medium": 120, "long": 1200}
prompts = {}
for name, count in repeat_counts.items():
    # 같은 문장을 근거 앞뒤에 같은 양으로 넣어 중앙 배치를 유지합니다.
    padding = note * count
    prompts[name] = f"""자료:
{padding}
{evidence}
{padding}

질문: {question}"""
    # 문자 수는 입력이 길어졌는지 미리 확인하는 값입니다.
    print(name, "문자 수:", len(prompts[name]))'''),
        markdown('''## 4. 비교 전에 입력 조건을 확인합니다

모든 입력에 질문과 정답 근거가 한 번씩 들어 있어야 합니다. 주변 문장에 정답을 추가하거나 근거 문장을 삭제하지 않았는지 확인합니다. 이 검사는 성능 점수가 아니라 실험에 사용할 입력의 확인입니다.'''),
        code('''# 입력이 길어져도 동일한 질문과 근거가 보존되었는지 확인합니다.
for name, prompt in prompts.items():
    print(name, "근거 수:", prompt.count(evidence), "질문 수:", prompt.count(question))
    assert prompt.count(evidence) == 1
    assert prompt.count(question) == 1
# short → medium → long 순으로 실제 문자열 길이가 증가합니다.
assert len(prompts["short"]) < len(prompts["medium"]) < len(prompts["long"])'''),
        markdown('''## 5. 각 길이를 세 번 실행하고 실제 답을 읽습니다

짧음·중간·김 순서의 비교를 세 차례 반복합니다. `record`는 한 번 실행한 길이, 반복 번호, 답, 토큰 수를 담는 딕셔너리입니다. `records`는 아홉 개의 `record`를 차례로 모은 목록입니다. 응답의 `input_tokens`는 모델 제공자가 센 입력 토큰 수입니다. 아홉 번의 호출이 끝날 때까지 출력되는 답을 확인합니다.'''),
        code('''# records는 나중에 같은 길이의 결과를 모으기 위한 기록 목록입니다.
records = []
for trial in range(1, 4):
    for name, prompt in prompts.items():
        # 모든 호출에 같은 모델·지시문을 사용합니다.
        result = model.invoke([
            ("system", "근거만 사용하고 출처를 표시하세요."),
            ("user", prompt),
        ])
        record = {
            "length": name,
            "trial": trial,
            "input_tokens": result.usage_metadata["input_tokens"],
            "answer": result.text,
        }
        records.append(record)
        print(name, "반복:", trial, "입력 토큰:", record["input_tokens"])
        print(record["answer"])'''),
        markdown('''## 6. 모든 답에 같은 확인 기준을 적용합니다

월요일과 출처가 모두 포함되었는지 확인합니다. 이 문자열 검사만으로 답 전체의 정확성을 보장할 수는 없습니다. 위 답 원문에서 ‘월요일이 아니다’처럼 뜻이 반대인 표현, 다른 기관의 답, 근거 밖 설명이 있는지도 읽어야 합니다.'''),
        code('''# 두 핵심 문자열이 모두 있으면 True, 하나라도 없으면 False입니다.
for record in records:
    answer = record["answer"]
    record["keyword_pass"] = "월요일" in answer and "E01 p.2" in answer
    print(record["length"], "반복:", record["trial"],
          "핵심어·출처 확인:", record["keyword_pass"])
# 모든 조건을 세 번씩 호출했는지 확인합니다.
assert len(records) == len(prompts) * 3'''),
        markdown('## 7. 입력 토큰과 정답 확인 결과를 나란히 비교합니다\n\n각 길이에서 조건을 충족한 응답 수를 셉니다. 점수가 낮아졌다면 먼저 실제 답을 다시 읽습니다. 점수가 같다면 이번 과제와 입력 범위에서는 이 기준으로 성능 저하를 관찰하지 못한 것입니다.\n\n`rows`는 현재 길이 조건과 이름이 같은 기록만 고르는 목록 표현식입니다. `sum()`은 참을 1, 거짓을 0으로 더하여 문자열 기준 충족 횟수를 셉니다. 이번에는 길이마다 기록이 세 개이므로 분모가 3입니다. 이 값은 답 전체의 사실성을 자동 채점한 점수가 아닙니다.\n\n회의록 담당자 찾기에도 같은 비교 방법을 적용할 수 있습니다. 여러 문서의 일정을 연결하는 과제는 필요한 추론이 달라 별도 실험이 필요합니다. 추가 실험에서 근거 위치와 길이를 동시에 바꾸면 원인을 구분하기 어려우므로 하나씩 변경합니다. 여기의 저장 출력에는 그런 추가 실험이 포함되어 있지 않습니다.'),
        code('''# rows는 같은 입력 길이 조건의 실행 기록만 모은 목록입니다.
for name in prompts:
    rows = [record for record in records if record["length"] == name]
    passed = sum(record["keyword_pass"] for record in rows)
    # 토큰 수는 세 호출의 값을 모두 보여 주어 실행 기록을 보존합니다.
    tokens = [record["input_tokens"] for record in rows]
    print(name, "입력 토큰:", tokens, "기준 충족:", passed, "/", len(rows))'''),
        markdown('''## 결과 해석

입력 토큰 증가와 정답 확인 결과를 함께 읽습니다. 모든 길이에서 정답을 유지할 수도 있습니다. 그런 결과를 성능 저하가 발생한 것처럼 표현하지 않습니다. 짧은 근거 한 문장과 반복된 주변 문장만 사용하는 작은 실험이므로, 긴 실제 문서의 모든 과제로 결론을 확대하지 않습니다. 더 복잡한 과제와 여러 질문을 사용하는 평가는 Ch 11·15에서 다룹니다.'''),
    ],
    "06-단계적-공개와-설계-비교": [
        markdown("""# 06. 단계적 공개와 설계 비교

단계적 공개는 문서 ID와 제목만 먼저 보고, 질문에 필요한 문서를 고른 뒤, 그 문서의 자세한 본문만 모델에 전달하는 방식입니다."""),
        markdown("""## 1. API 연결 준비"""),
        *setup_cells(),
        markdown("""### Ch 7 실행 기록을 확인합니다

Ch 7의 프롬프트 A/B 기록을 읽고 필수 필드와 파일 지문을 확인합니다. 이전 실행 수치를 현재 실행 결과와 직접 비교하지는 않습니다."""),
        code('''from hashlib import sha256
import json
from pathlib import Path

course_root = next((path for path in [Path.cwd(), *Path.cwd().parents]
                    if (path / "labs/part2/ch07-prompt-engineering").is_dir()), None)
if course_root is None:
    raise FileNotFoundError("실습 묶음의 labs/part2 폴더를 찾지 못했습니다.")
ch07_relative = Path("labs/part2/ch07-prompt-engineering/runs/prompt-ab-continuity.json")
ch07_path = course_root / ch07_relative
if not ch07_path.exists():
    raise FileNotFoundError("Ch 7의 08 노트북을 먼저 실행하세요.")
ch07_record = json.loads(ch07_path.read_text(encoding="utf-8"))
ch07_sha256 = sha256(ch07_path.read_bytes()).hexdigest()
required = {"run_id", "run_date", "source_chapter", "source_record", "settings", "versions"}
assert required <= ch07_record.keys()
assert ch07_record["settings"]["pricing_usd_per_million"] == {
    "ordinary_input": 0.75, "cached_input": 0.075, "output": 4.50}
print("Ch 7 기록:", ch07_record["run_id"], ch07_sha256[:12])'''),
        markdown("""## 2. 목록과 원문을 분리합니다

목록에는 여러 문서의 ID와 제목만 넣어 선택을 돕습니다. 답에 필요한 근거는 선택한 문서의 원문에서 가져옵니다."""),
        code("""# documents는 ID·제목·원문을 가진 문서 목록입니다.
documents = [
    {"id": "E01-p2", "title": "이용 시간", "text": "월요일 휴관"},
    {"id": "E01-p3", "title": "대출 규정",
     "text": "회원 1명당 최대 7권, 대출 기간 14일. 예약이 없으면 1회 7일 연장."},
    {"id": "E01-p5", "title": "주차 안내", "text": "회원은 최초 2시간 무료입니다."},
]
print("전체 문서 수:", len(documents))"""),
        markdown("""### 먼저 제목 목록만 공개합니다

원문 전체를 읽기 전에 ID와 제목만 복사합니다. 반복문에서 만든 `item`을 `catalog`에 하나씩 추가합니다."""),
        code("""# catalog에는 선택에 필요한 두 필드만 남깁니다.
catalog = []
for document in documents:
    item = {"id": document["id"], "title": document["title"]}
    catalog.append(item)

print(catalog)"""),
        markdown('## 3. 필요한 ID의 원문만 공개합니다\n\n이 예제에서는 학생이 `E01-p3`을 직접 선택합니다.\n\n`selected_id`는 사람이 정한 값입니다. 반복문은 각 문서의 ID와 비교하고 일치하면 문서 딕셔너리를 `selected`에 저장한 뒤 `break`로 중단합니다. `selected is None`은 끝까지 찾지 못했는지 확인합니다. 이 단계에서 모델은 문서를 선택하지 않습니다.\n\n상품 두 모델의 호환성 차이를 비교한다면 두 상세 규격이 모두 필요합니다. 선택 입력의 문서 수는 항상 하나로 고정하지 않고 질문의 근거 범위에 맞춰 정합니다. 아래에서는 대출 규정 한 문서로 답할 수 있는 질문을 사용합니다.'),
        code("""# selected_id는 질문에 맞춰 고른 문서 ID입니다.
# 반복문은 ID가 같은 문서를 찾으면 selected에 저장하고 중단합니다.
selected_id = "E01-p3"
selected = None
for document in documents:
    if document["id"] == selected_id:
        selected = document
        break

if selected is None:
    raise ValueError("선택한 문서를 찾지 못했습니다.")

print("선택한 제목:", selected["title"])"""),
        markdown("""### 세 가지 공개 방식의 길이를 비교합니다

전체 원문, 선택한 원문, 사람이 작성한 압축문을 같은 문자 수 기준으로 비교합니다."""),
        code("""# full_lines를 만든 뒤 join으로 출처가 붙은 전체 원문을 연결합니다.
full_lines = []
for document in documents:
    line = f"[{document['id']}] {document['text']}"
    full_lines.append(line)

full = "\\n".join(full_lines)
compressed = "1명당 최대 7권, 14일 대출, 예약 없으면 1회 7일 연장 [E01-p3]"
print("full 문자 수:", len(full))
print("selected 문자 수:", len(selected["text"]))
print("compressed 문자 수:", len(compressed))"""),
        markdown("""## 4. 세 설계를 같은 조건으로 실행합니다

전체 원문, 선택 원문, 압축문을 이름별로 준비합니다. 선택 원문에도 같은 출처 ID를 붙여 세 입력의 표기 조건을 맞춥니다."""),
        code('''# design_contexts의 값만 다르고 질문과 지시는 다음 셀에서 고정합니다.
selected_context = f"[{selected['id']}] {selected['text']}"
design_contexts = {
    "full": full,
    "selected": selected_context,
    "compressed": compressed,
}
for name, context in design_contexts.items():
    print(name, "문자 수:", len(context))'''),
        markdown("""### 같은 질문과 지시로 세 번 호출합니다

압축문은 앞에서 사람이 작성한 값이므로 별도의 압축 모델 호출 비용은 없습니다. 여기서 측정하는 사용량은 세 답변 호출의 입력 토큰입니다."""),
        code('''# Ch 6과 같은 기준일 단가로 OpenAI 호출 비용을 계산합니다.
def estimate_openai_cost(usage):
    input_tokens = usage.get("input_tokens")
    output_tokens = usage.get("output_tokens")
    if input_tokens is None or output_tokens is None:
        return None
    cache_read = (usage.get("input_token_details") or {}).get("cache_read") or 0
    normal_input = input_tokens - cache_read
    return (normal_input * 0.75 + cache_read * 0.075 + output_tokens * 4.50) / 1_000_000'''),
        code('''# 모든 설계에 같은 instruction과 question을 사용합니다.
import time

instruction = "근거의 조건·예외·출처를 빠뜨리지 마세요."
question = "대출 권수, 기간, 연장 조건과 출처를 알려 주세요."
design_results = {}
for name, context in design_contexts.items():
    messages = [("system", instruction), ("user", f"근거: {context}\\n질문: {question}")]
    started = time.perf_counter()
    response = model.invoke(messages)
    latency_ms = round((time.perf_counter() - started) * 1000, 1)
    usage = response.usage_metadata
    if usage is None:
        raise RuntimeError("모델 사용량 메타데이터가 없습니다.")
    cache_read = (usage.get("input_token_details") or {}).get("cache_read") or 0
    design_results[name] = {"response": response, "usage": usage,
                            "latency_ms": latency_ms, "cache_read_tokens": cache_read,
                            "estimated_cost_usd": round(estimate_openai_cost(usage), 8)}'''),
        markdown("""### 실제 출력과 입력 토큰을 관찰합니다

설계 이름 아래에 입력 토큰과 답변 원문을 함께 출력합니다. 세 응답의 표현은 실행마다 달라질 수 있습니다."""),
        code('''# 토큰·지연·비용과 답변 원문을 설계별로 확인합니다.
for name, result in design_results.items():
    usage = result["usage"]
    print(f"\\n[{name}] input={usage['input_tokens']} output={usage['output_tokens']} "
          f"cache={result['cache_read_tokens']} latency_ms={result['latency_ms']} "
          f"cost_usd={result['estimated_cost_usd']}")
    print(result["response"].text)'''),
        markdown('### 필요한 정보가 보존됐는지 비교합니다\n\n토큰 수가 작아도 대출 조건, 연장 예외, 출처가 빠지면 충분한 답이 아닙니다. 자동 검사는 문자열 존재 여부만 보여 주므로 답변 원문도 함께 읽습니다.\n\n아래 딕셔너리의 “연장 예외”는 실제로 “연장” 문자열이 있는지만 검사합니다. 예약이 없다는 조건과 1회·7일 제한을 모두 확인하는 검사가 아니므로 답 원문에서 별도로 읽습니다. “출처”도 `E01` 포함만 보므로 페이지가 정확한지까지 자동 판정하지 않습니다.'),
        code('''# 세 기준이 답변에 나타났는지 설계별로 확인합니다.
for name, result in design_results.items():
    answer = result["response"].text
    checks = {
        "대출 조건": "7권" in answer and "14일" in answer,
        "연장 예외": "연장" in answer,
        "출처": "E01" in answer,
    }
    result["checks"] = checks
    print(name, checks)'''),
        markdown("""### 실행 기록을 보존합니다

Ch 7과 같이 비교 조건과 원문, 사용량, 지연, 예상 비용, 자동 확인을 정본과 실행별 사본에 저장합니다."""),
        code('''from datetime import datetime, timezone
import json
from pathlib import Path
run_at = datetime.now(timezone.utc)
session_id = run_at.strftime("%Y%m%dT%H%M%S%fZ")
results_for_log = []
for name, result in design_results.items():
    results_for_log.append({"design": name, "context": design_contexts[name],
                            "answer": result["response"].text, "usage": result["usage"],
                            "latency_ms": result["latency_ms"],
                            "cache_read_tokens": result["cache_read_tokens"],
                            "estimated_cost_usd": result["estimated_cost_usd"], "checks": result["checks"]})
record = {"run_id": f"ch08-context-{session_id}", "run_date": run_at.date().isoformat(),
          "source_chapter": "ch08", "source_record": {"path": str(ch07_relative), "sha256": ch07_sha256, "run_id": ch07_record["run_id"]}, "model": "openai:gpt-5.4-mini",
          "settings": {"max_tokens": 300, "pricing_date": ch07_record["settings"]["pricing_date"],
                       "pricing_usd_per_million": ch07_record["settings"]["pricing_usd_per_million"]},
          "question": question, "comparison_policy": "문자열 확인은 원문 정독 보조임", "results": results_for_log}
runs_dir = course_root / "labs/part2/ch08-context-engineering/runs"
record_path = runs_dir / "context-design-continuity.json"
session_path = runs_dir / "continuity" / session_id / record_path.name
session_path.parent.mkdir(parents=True, exist_ok=False)
payload = json.dumps(record, ensure_ascii=False, indent=2)
record_path.write_text(payload, encoding="utf-8")
session_path.write_text(payload, encoding="utf-8")
print(record_path.relative_to(course_root), "보존 사본:", session_path.relative_to(course_root))'''),
        markdown("""## 5. 목록 공개 수 한 값만 바꿉니다

전체 문서와 선택 결과는 그대로 두고 목록에서 보여 줄 항목 수만 `1`에서 `2`로 바꿉니다."""),
        code("""# 슬라이스 [:N]은 앞에서 N개 항목을 반환합니다.
base_limit = 1
changed_limit = 2
print("기본 목록:", catalog[:base_limit])
print("변경 목록:", catalog[:changed_limit])"""),
        markdown("""## 정리

목록, 선택, 원문 읽기를 순서대로 수행합니다. 토큰 감소와 필요한 조건의 보존 여부를 함께 비교합니다."""),
        markdown(
            """## 실패 재현: 질문과 다른 문서를 선택합니다

대출 질문에 주차 문서를 선택하면 입력은 짧아져도 필요한 대출 근거가 사라집니다.""",
            lesson_part="before",
        ),
        code(
            """# wrong_id는 질문과 관계없는 주차 문서 ID입니다.
# 반복문으로 실제 문서를 찾아 모델에 보낼 메시지를 만듭니다.
wrong_id = "E01-p5"
wrong_document = None
for document in documents:
    if document["id"] == wrong_id:
        wrong_document = document
        break

if wrong_document is None:
    raise ValueError("잘못 선택한 문서를 찾지 못했습니다.")

wrong_messages = [
    ("system", instruction),
    ("user", f"근거: [{wrong_document['id']}] {wrong_document['text']}\\n질문: {question}"),
]""",
            lesson_part="before",
        ),
        markdown(
            """### 주차 문서를 모델에 전달해 답을 확인합니다

질문과 지시는 그대로 두고 선택한 문서만 `E01-p5`로 바꿉니다. 모델이 대출 조건의 근거를 받지 못한 상태에서 어떤 답을 하는지 읽습니다.""",
            lesson_part="before",
        ),
        code(
            """# 같은 모델을 실제 호출하고 선택한 문서와 답을 함께 출력합니다.
wrong_response = model.invoke(wrong_messages)
assert wrong_document["title"] == "주차 안내"
print("잘못 선택한 문서:", wrong_document["id"], wrong_document["title"])
print("모델 답:", wrong_response.text)""",
            lesson_part="before",
        ),
        markdown(
            """## 수정: 대출 규정 문서를 선택합니다

질문과 지시는 유지하고 대출 규정 `E01-p3`을 선택합니다. 같은 모델의 답에 대출 권수·기간·연장 조건이 나타나는지 확인합니다.""",
            lesson_part="after",
        ),
        code(
            """# 선택 ID만 대출 규정으로 고치고 같은 질문으로 다시 호출합니다.
fixed_id = "E01-p3"
fixed_document = None
for document in documents:
    if document["id"] == fixed_id:
        fixed_document = document
        break

if fixed_document is None:
    raise ValueError("수정한 문서를 찾지 못했습니다.")

assert fixed_document["title"] == "대출 규정"
fixed_messages = [
    ("system", instruction),
    ("user", f"근거: [{fixed_document['id']}] {fixed_document['text']}\\n질문: {question}"),
]
fixed_response = model.invoke(fixed_messages)
assert "7권" in fixed_response.text and "14일" in fixed_response.text
assert "연장" in fixed_response.text
print("수정 후 선택:", fixed_document["id"], fixed_document["title"])
print("모델 답:", fixed_response.text)""",
            lesson_part="after",
        ),
    ],
}


def main() -> None:
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    for slug, cells in NOTEBOOK_DATA.items():
        install_note = markdown(f"""## 실행 환경 준비

실습 파일은 `labs/part2/ch08-context-engineering/notebooks/{slug}.ipynb`입니다. 새 커널에서 시작해 첫 코드 셀로 패키지 버전을 맞춘 뒤, 설명과 코드를 위에서부터 순서대로 실행합니다. `.env`는 현재 작업 폴더의 상위 경로에서도 찾습니다.""")
        if slug == "05-Context-rot-측정":
            rendered_cells = [cells[0], cells[1], code(INSTALL), *cells[2:]]
        else:
            rendered_cells = [cells[0], install_note, code(INSTALL), *cells[1:]]
        for index, cell in enumerate(rendered_cells, start=1):
            cell["id"] = f"cell-{index:02d}"
        notebook = {
            "cells": rendered_cells,
            "metadata": {
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python", "version": "3.12"},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        if slug == "05-Context-rot-측정":
            notebook["metadata"]["lesson_format"] = "experiment"
        path = NOTEBOOKS / f"{slug}.ipynb"
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
