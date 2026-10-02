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


SETUP = """# find_dotenv는 현재 폴더부터 상위 폴더를 검색해 .env 경로를 찾습니다.
# model은 이후 셀에서 공통으로 사용할 LangChain 채팅 모델 객체입니다.
from dotenv import find_dotenv, load_dotenv
from langchain.chat_models import init_chat_model
import os

# usecwd=True는 노트북을 실행한 폴더를 검색 시작점으로 지정합니다.
# 키 값은 출력하지 않고 존재 여부만 확인합니다.
env_path = find_dotenv(usecwd=True)
if not env_path:
    raise FileNotFoundError("현재 폴더의 상위 경로에서 .env를 찾지 못했습니다.")
load_dotenv(env_path)
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(".env에 OPENAI_API_KEY가 없습니다.")
# openai:는 공급자 이름이며, reasoning_effort="none"은 별도 추론 토큰을 사용하지 않는 설정입니다.
# max_tokens=300은 생성할 출력 토큰 수의 상한입니다.
model = init_chat_model("openai:gpt-5.4-mini", reasoning_effort="none", max_tokens=300)
print("LangChain 모델 준비 완료")"""

INSTALL = (
    '# %pip은 현재 노트북 커널에 패키지를 설치하는 Jupyter 전용 명령입니다.\n'
    '# -q는 설치 로그를 줄이고, == 뒤 숫자는 수업에서 검증한 버전을 고정합니다.\n'
    '%pip install -q "langchain==1.4.0" "langchain-openai==1.6.0" '
    '"python-dotenv==1.2.3" "tiktoken==0.14.0"'
)


def api_cell(prompt_name: str, instructions: str) -> str:
    return f'''# messages는 역할과 내용을 짝지은 목록이며 system 지시를 user 질문보다 먼저 둡니다.
# invoke()는 모델을 한 번 호출하고, 반환된 AIMessage에서 text와 사용량을 읽습니다.
messages = [
    ("system", "{instructions}"),
    ("user", {prompt_name}),
]
response = model.invoke(messages)
# usage_metadata는 입력·출력 토큰 수를 담지만 제공되지 않을 가능성도 검사합니다.
usage = response.usage_metadata
if usage is None:
    raise RuntimeError("모델 사용량 메타데이터가 없습니다.")
print(response.text)
print("input_tokens:", usage.get("input_tokens"))
print("output_tokens:", usage.get("output_tokens"))'''


NOTEBOOK_DATA: dict[str, list[dict]] = {
    "01-컨텍스트와-토큰-예산": [
        markdown("""# 01. 컨텍스트와 토큰 예산

모델 호출에는 입력과 출력이 함께 들어갈 공간이 필요합니다. 이 노트북에서는 입력 길이를 호출 전에 추정하고, 실제 API 사용량과 비교합니다."""),
        markdown("""## 1. API 연결 준비

아래 셀은 현재 작업 폴더에서 상위 폴더로 올라가며 `.env`를 찾습니다. 키 값은 화면에 출력하지 않습니다."""),
        code(SETUP),
        markdown("""## 2. 출력 공간을 먼저 예약합니다

전체 예산에서 출력 예약분과 안전 여유를 빼면 입력에 사용할 수 있는 범위가 나옵니다."""),
        code("""# total은 전체 한도, output_reserve는 답변용 예약분, safety_margin은 오차 여유입니다.
# 함수는 세 값을 계산한 입력 가용량을 반환하며, 음수이면 호출 전에 오류를 냅니다.
def input_budget(total: int, output_reserve: int, safety_margin: int) -> int:
    available = total - output_reserve - safety_margin
    if available < 0:
        raise ValueError("출력 예약분과 여유가 전체 예산보다 큽니다.")
    return available

available = input_budget(4096, 300, 128)
print("입력에 사용할 수 있는 토큰:", available)"""),
        markdown("""## 3. 로컬 추정값을 확인합니다

토크나이저의 추정값은 호출 전 차단에 쓰고, `AIMessage.usage_metadata`는 호출 후 기록에 씁니다."""),
        code('''# question과 evidence를 합쳐 모델에 보낼 prompt를 만듭니다.
# estimated는 prompt 문자열만 로컬에서 센 토큰 수입니다.
# system 메시지와 채팅 형식에 필요한 토큰은 제외되어 실제 API 입력 토큰과 다를 수 있습니다.
import tiktoken

question = "미르시립도서관의 정기 휴관일은 언제인가요?"
evidence = "[E01 p.2] 정기 휴관일은 매주 월요일입니다."
prompt = f"""근거:
{evidence}

질문: {question}"""
encoding = tiktoken.get_encoding("o200k_base")
estimated = len(encoding.encode(prompt))
print("로컬 추정 입력 토큰:", estimated)
print("예산 안에 있음:", estimated <= available)'''),
        markdown("""## 4. 실제 API 사용량을 비교합니다

`AIMessage.text`와 `usage_metadata`를 함께 확인합니다. 출력은 실행마다 달라질 수 있습니다."""),
        code(api_cell("prompt", "근거에 있는 정보만 사용하고 출처를 표시하세요.")),
        markdown("""## 정리

출력 공간을 먼저 예약하고, 입력을 로컬에서 추정한 뒤, 실제 사용량은 API 응답에서 확인합니다."""),
        markdown(
            """## 실패 재현: 출력 공간을 남기지 않습니다

전체 예산보다 출력 예약분과 여유를 크게 설정하면 입력에 사용할 공간이 음수가 됩니다.""",
            lesson_part="before",
        ),
        code(
            """# bad_total은 출력 예약분만큼만 잡아 안전 여유를 남기지 못한 잘못된 예산입니다.
# try/except는 예상한 ValueError만 포착하여 실패 원인을 출력합니다.
bad_total = 300
try:
    input_budget(bad_total, 300, 128)
except ValueError as error:
    print("관찰한 실패:", error)
else:
    raise AssertionError("예산 오류가 발생해야 합니다.")""",
            lesson_part="before",
        ),
        markdown(
            """## 수정: 전체 예산을 복원합니다

출력 예약분과 여유를 제외하고도 입력 공간이 남도록 전체 예산을 4,096토큰으로 복원합니다.""",
            lesson_part="after",
        ),
        code(
            """# fixed_total을 충분히 늘려 출력 예약분과 안전 여유를 모두 확보합니다.
# fixed_available은 수정된 입력 가용량이며 assert로 계산 결과를 확인합니다.
fixed_total = 4096
fixed_available = input_budget(fixed_total, 300, 128)
assert fixed_available == 3668
print("수정 후 입력 예산:", fixed_available)""",
            lesson_part="after",
        ),
    ],
    "02-Write와-Select": [
        markdown("""# 02. Write와 Select

Write는 정보를 외부 기록에 남기는 단계이고, Select는 현재 질문에 필요한 기록만 고르는 단계입니다."""),
        markdown("""## 1. API 연결 준비

각 노트북은 빈 커널에서 시작할 수 있도록 연결 코드를 포함합니다."""),
        code(SETUP),
        markdown("""## 2. 기록을 JSON으로 저장하고 다시 읽습니다

예제 데이터는 짧게 인라인으로 두고, 임시 폴더에 저장하여 작업 폴더에 의존하지 않게 합니다."""),
        code("""# records의 각 사전은 문서 식별자, 주제, 본문을 나타냅니다.
# 임시 JSON 파일에 썼다가 다시 읽어 외부 기록의 저장과 불러오기를 확인합니다.
import json
from pathlib import Path
from tempfile import gettempdir

records = [
    {"id": "E01-p2", "topic": "휴관", "text": "매주 월요일 휴관"},
    {"id": "E01-p3", "topic": "대출", "text": "7권, 14일 대출"},
    {"id": "E01-p5", "topic": "주차", "text": "90분 무료"},
]
memory_path = Path(gettempdir()) / "ch08-memory.json"
memory_path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
loaded = json.loads(memory_path.read_text(encoding="utf-8"))
print("다시 읽은 기록:", len(loaded))"""),
        markdown("""## 3. 질문에 필요한 기록만 선택합니다

여기서는 학생이 식별자를 직접 지정합니다. 자동 검색은 Ch 9에서 다룹니다."""),
        code("""# selected_ids는 이번 질문에 필요한 문서 ID 모음입니다.
# 리스트 컴프리헨션은 loaded를 순회하며 ID가 포함된 기록만 selected에 남깁니다.
selected_ids = {"E01-p3", "E01-p5"}
selected = [row for row in loaded if row["id"] in selected_ids]
for row in selected:
    print(row["id"], row["topic"], row["text"])"""),
        markdown("""## 4. 선택한 기록으로 답을 생성합니다

모델에는 저장소 전체 대신 선택한 두 기록만 전달합니다."""),
        code('''# join은 선택한 기록을 줄바꿈으로 합치고, f-string은 각 근거 앞에 출처 ID를 붙입니다.
# prompt는 합친 근거와 학생 질문을 모델에 전달할 하나의 문자열입니다.
context = "\\n".join(f"[{r['id']}] {r['text']}" for r in selected)
prompt = f"""근거:
{context}

질문: 대출 권수와 주차 무료 시간을 알려 주세요."""'''),
        code(api_cell("prompt", "제공된 근거만 사용하고 문장마다 식별자를 붙이세요.")),
        markdown("""## 정리

외부 기록은 저장만으로 모델에 전달되지 않습니다. 질문에 맞는 항목을 선택하여 호출 입력에 넣어야 합니다."""),
        markdown(
            """## 실패 재현: 저장한 기록을 선택하지 않습니다

파일에 기록이 있어도 선택 결과가 비어 있으면 모델에 전달할 근거가 없습니다.""",
            lesson_part="before",
        ),
        code(
            """# rows는 선택된 근거 목록이며, 빈 목록이면 모델에 줄 정보가 없습니다.
# None 반환 함수의 -> None과 예상 오류를 포착하는 try/except를 함께 확인합니다.
def require_context(rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("선택한 근거가 없습니다.")

try:
    require_context([])
except ValueError as error:
    print("관찰한 실패:", error)
else:
    raise AssertionError("빈 근거 오류가 발생해야 합니다.")""",
            lesson_part="before",
        ),
        markdown(
            """## 수정: 선택한 기록을 검사합니다

앞에서 선택한 대출과 주차 기록을 검사한 뒤 모델 입력에 사용합니다.""",
            lesson_part="after",
        ),
        code(
            """# 앞에서 만든 selected를 검사해 빈 근거 문제가 해결됐는지 확인합니다.
# 리스트 컴프리헨션으로 실제 선택 순서까지 검증합니다.
require_context(selected)
assert [row["id"] for row in selected] == ["E01-p3", "E01-p5"]
print("수정 후 선택한 기록:", len(selected))""",
            lesson_part="after",
        ),
    ],
    "03-Compress와-Isolate": [
        markdown("""# 03. Compress와 Isolate

Compress는 필요한 사실을 짧게 보존하고, Isolate는 질문마다 전달할 근거를 분리합니다."""),
        markdown("""## 1. API 연결 준비"""),
        code(SETUP),
        markdown("""## 2. 사실·조건·예외·출처를 보존합니다

길이만 줄이면 중요한 예외를 잃을 수 있습니다. 네 필드를 모두 확인한 뒤 한 줄로 압축합니다."""),
        code("""# record는 사실·조건·예외·출처를 가진 사전이고, required는 출력 순서를 고정합니다.
# 집합 차이는 빠진 키를 찾고, 함수는 네 필드를 한 줄 문자열로 반환합니다.
def compress(record: dict[str, str]) -> str:
    required = ("fact", "condition", "exception", "source")
    missing = set(required) - record.keys()
    if missing:
        raise ValueError(f"빠진 필드: {sorted(missing)}")
    return " | ".join(f"{key}: {record[key]}" for key in required)

loan = {"fact": "7권을 14일 대출", "condition": "회원 1명 기준",
        "exception": "예약이 없으면 1회 7일 연장", "source": "E01 p.3"}
compressed = compress(loan)
print(compressed)"""),
        markdown("""## 3. 질문별 입력을 분리합니다

대출 질문에는 대출 근거만 넣습니다. 태그는 읽기 구조를 돕지만 보안 경계는 아닙니다."""),
        code('''# question은 답을 구할 질문이고, compressed에는 앞 셀에서 보존한 네 필드가 있습니다.
# f-string은 두 값을 구획 표시와 함께 prompt 문자열에 삽입합니다.
question = "대출 권수, 기간, 연장 조건을 알려 주세요."
prompt = f"""[근거]
{compressed}

[질문]
{question}"""
print(prompt)'''),
        markdown("""## 4. 압축한 근거로 답을 생성합니다"""),
        code(api_cell("prompt", "근거의 사실·조건·예외·출처를 빠뜨리지 마세요.")),
        markdown("""## 정리

압축은 짧게 만드는 작업과 보존해야 할 필드를 검사하는 작업을 함께 수행합니다. 질문별 입력은 호출 전에 분리합니다."""),
        markdown(
            """## 실패 재현: 압축본에서 예외를 삭제합니다

연장 예외가 빠진 레코드는 일반 규칙을 예외 대상에도 적용하게 만들 수 있습니다.""",
            lesson_part="before",
        ),
        code(
            """# broken은 의도적으로 exception 키를 뺀 레코드입니다.
# compress가 누락을 발견하면 ValueError를 내며, except가 그 실패만 포착합니다.
broken = {"fact": "7권을 14일 대출", "condition": "회원 1명 기준",
          "source": "E01 p.3"}
try:
    compress(broken)
except ValueError as error:
    print("관찰한 실패:", error)
else:
    raise AssertionError("필드 누락 오류가 발생해야 합니다.")""",
            lesson_part="before",
        ),
        markdown(
            """## 수정: 원문의 예외 필드를 복원합니다

누락된 예외를 원문 레코드에서 가져와 다시 압축합니다.""",
            lesson_part="after",
        ),
        code(
            """# {**broken, ...}은 기존 사전을 펼친 뒤 누락된 exception 키를 추가합니다.
# fixed_compressed는 복원한 레코드의 압축 결과이며 예외 문구 보존을 검사합니다.
fixed = {**broken, "exception": loan["exception"]}
fixed_compressed = compress(fixed)
assert "예약이 없으면 1회 7일 연장" in fixed_compressed
print("수정 후 압축:", fixed_compressed)""",
            lesson_part="after",
        ),
    ],
    "04-네-가지-실패-모드": [
        markdown("""# 04. 네 가지 실패 모드

Poisoning, Distraction, Confusion, Clash는 입력에서 생기는 문제를 서로 다른 관점으로 설명합니다. 실험에서는 자극의 이름과 실제 출력 관찰을 구분합니다."""),
        markdown("""## 1. API 연결 준비"""),
        code(SETUP),
        markdown("""## 2. 다섯 가지 입력 조건을 만듭니다

기준 입력을 유지하면서 잘못된 메모, 무관한 정보, 비슷한 기관, 상충 규정을 하나씩 추가합니다."""),
        code('''# clean은 기준 근거이고, noise는 길이만 늘리는 무관한 문장입니다.
# conditions는 기준 입력과 네 실패 자극을 이름별로 보관하는 사전입니다.
clean = "[E01 p.2] 미르시립도서관은 매주 월요일 휴관입니다."
noise = "회의 안건: 행사 배너와 좌석 배치를 논의했습니다. " * 12
conditions = {
    "clean": clean,
    "poisoning": f"""{clean}
[미검증 메모] 휴관일은 화요일입니다.""",
    "distraction": f"""{noise}
{clean}""",
    "confusion": f"""{clean}
[미르고등학교 도서실] 화요일 휴관입니다.""",
    "clash": f"""{clean}
[합성 부록] 미르시립도서관은 수요일 휴관입니다.""",
}
print("실험 조건:", list(conditions))'''),
        markdown("""## 3. 같은 질문으로 다섯 조건을 실행합니다

어떤 실패가 나타날지 미리 정하지 않습니다. 조건 이름, 실제 입력 토큰, 응답 원문을 나란히 기록합니다."""),
        code('''# items()는 조건 이름과 근거를 한 쌍씩 반환하며 모든 조건에 같은 질문을 적용합니다.
# results에는 조건별 AIMessage를 저장하고, usage에서 실제 입력 토큰 수를 읽습니다.
results = {}
for name, context in conditions.items():
    messages = [
        ("system", "근거만 사용하고, 충돌하면 확인이 필요하다고 답하세요."),
        ("user", f"""근거:
{context}

질문: 정기 휴관일은 언제인가요?"""),
    ]
    response = model.invoke(messages)
    usage = response.usage_metadata
    if usage is None:
        raise RuntimeError("모델 사용량 메타데이터가 없습니다.")
    results[name] = response
    print(f"\\n[{name}] input_tokens={usage['input_tokens']}")
    print(response.text)'''),
        markdown("""## 4. 출력에서 관찰한 문자열을 비교합니다

요일과 확인 요청 표현의 등장 여부만 표시합니다. 이 표만으로 답의 완결성을 확정하지 않고 응답 원문을 함께 읽습니다."""),
        code("""# 각 응답 text에서 요일 문자열과 추가 확인 표현이 나타났는지 검사합니다.
# observed가 비어 있으면 or 뒤의 기본 목록을 출력합니다.
for name, response in results.items():
    answer = response.text
    observed = [day for day in ("월요일", "화요일", "수요일") if day in answer]
    if "확인" in answer or "충돌" in answer or "상충" in answer:
        observed.append("추가 확인 표현")
    print(name, observed or ["요일 표현 없음"])"""),
        markdown("""## 정리

실패 자극을 넣었다는 사실만으로 실패가 발생했다고 기록하지 않습니다. 출력에서 관찰한 문장과 입력 근거를 연결합니다."""),
        markdown(
            """## 실패 재현: 상충 규정의 시행일을 기록하지 않습니다

두 규정에 시행일이 없으면 어느 규정이 질문 시점에 유효한지 판정할 수 없습니다.""",
            lesson_part="before",
        ),
        code(
            """# items는 서로 상충할 수 있는 규정 문자열 목록입니다.
# any()는 하나라도 시행일 표기가 없으면 True가 되어 ValueError를 발생시킵니다.
def require_versions(items: list[str]) -> None:
    if any("시행일:" not in item for item in items):
        raise ValueError("상충 규정의 시행일이 없습니다.")

try:
    require_versions([conditions["clean"], conditions["clash"]])
except ValueError as error:
    print("관찰한 실패:", error)
else:
    raise AssertionError("시행일 누락 오류가 발생해야 합니다.")""",
            lesson_part="before",
        ),
        markdown(
            """## 수정: 각 규정에 시행일을 기록합니다

시행일·요일·출처를 구조화하고 질문 기준일에 유효한 규정 가운데 가장 최근 규정을 선택합니다.""",
            lesson_part="after",
        ),
        code(
            """# versioned는 시행일·요일·출처를 분리한 규정 목록이고 as_of는 질문 기준일입니다.
# eligible에서 기준일까지 시행된 규정만 남긴 뒤 max의 key로 가장 최근 시행일을 고릅니다.
# YYYY-MM-DD처럼 자릿수가 고정된 날짜는 문자열 순서와 날짜 순서가 같습니다. 다른 형식은 날짜 객체로 바꿉니다.
versioned = [
    {"effective_date": "2025-01-01", "weekday": "월요일", "source": "E01 p.2"},
    {"effective_date": "2026-01-01", "weekday": "수요일", "source": "합성 부록"},
]
as_of = "2026-09-08"
eligible = [record for record in versioned if record["effective_date"] <= as_of]
selected_rule = max(eligible, key=lambda record: record["effective_date"])
assert selected_rule["weekday"] == "수요일"
assert selected_rule["source"] == "합성 부록"
print("수정 후 적용 규정:", selected_rule)""",
            lesson_part="after",
        ),
    ],
    "05-Context-rot-측정": [
        markdown("""# 05. Context rot 측정

입력 길이와 근거 위치를 바꾸되 질문, 모델, 지시, 평가 기준은 고정해야 길이 효과를 비교할 수 있습니다."""),
        markdown("""## 1. API 연결 준비"""),
        code(SETUP),
        markdown("""## 2. 같은 근거를 짧은 입력과 긴 입력에 배치합니다

긴 입력에는 질문과 무관한 문장을 추가합니다. 실제 실험에서는 길이와 위치별로 여러 번 반복합니다."""),
        code('''# evidence와 question은 두 실험 조건에서 동일하게 사용하는 통제 변수입니다.
# noise만 긴 조건에 추가하고, prompts는 조건 이름과 완성된 입력을 연결합니다.
evidence = "[E01 p.2] 정기 휴관일은 매주 월요일입니다."
question = "미르시립도서관의 정기 휴관일과 출처를 알려 주세요."
noise = "회의 준비 항목을 확인했습니다. " * 120
prompts = {
    "short": f"""근거:
{evidence}

질문: {question}""",
    "long": f"""근거:
{noise}
{evidence}

질문: {question}""",
}
print({name: len(text) for name, text in prompts.items()})'''),
        markdown("""## 3. 두 조건의 실제 사용량을 측정합니다

두 호출의 입력 토큰과 답을 나란히 출력합니다. 두 번의 호출만으로 일반 결론을 내리지는 않습니다."""),
        code("""# 두 prompt를 같은 system 지시로 호출해 입력 길이만 다른 결과를 만듭니다.
# result는 AIMessage이며 results에 보관한 뒤 실제 입력 토큰과 답변을 출력합니다.
results = {}
for name, prompt in prompts.items():
    messages = [("system", "근거만 사용하고 출처를 표시하세요."), ("user", prompt)]
    result = model.invoke(messages)
    usage = result.usage_metadata
    if usage is None:
        raise RuntimeError("모델 사용량 메타데이터가 없습니다.")
    results[name] = result
    print(name, "input_tokens:", usage["input_tokens"])
    print(result.text)"""),
        markdown("""## 4. 최소 루브릭으로 확인합니다

자동 문자열 검사는 빠르지만, 대상 기관과 문장의 모순 여부는 사람이 함께 읽어야 합니다."""),
        code("""# int(True)는 1, int(False)는 0이므로 두 문자열 검사를 점수로 더할 수 있습니다.
# score는 요일과 출처 표기가 각각 있는지만 확인하는 0~2점 값입니다.
for name, result in results.items():
    answer = result.text
    score = int("월요일" in answer) + int("E01 p.2" in answer)
    print(name, "자동 점수:", score, "/ 2")"""),
        markdown("""## 정리

이번 두 호출은 측정 방법을 익히는 최소 예제입니다. 반복 횟수와 실행 순서를 기록해야 재현 가능한 실험이 됩니다."""),
        markdown(
            """## 실패 재현: 조건마다 질문을 바꿉니다

입력 길이와 질문 난이도를 함께 바꾸면 어느 변화가 점수 차이를 만들었는지 구분할 수 없습니다.""",
            lesson_part="before",
        ),
        code(
            """# questions는 조건별 질문 목록이며, set은 중복 질문을 하나로 모읍니다.
# 서로 다른 질문이 두 개 이상이면 비교 조건이 달라졌으므로 ValueError를 냅니다.
def require_same_question(questions: list[str]) -> None:
    if len(set(questions)) != 1:
        raise ValueError("조건마다 질문이 다릅니다.")

try:
    require_same_question([question, "대출 기간은 얼마인가요?"])
except ValueError as error:
    print("관찰한 실패:", error)
else:
    raise AssertionError("질문 불일치 오류가 발생해야 합니다.")""",
            lesson_part="before",
        ),
        markdown(
            """## 수정: 모든 조건에 같은 질문을 사용합니다

짧은 입력과 긴 입력 모두 앞에서 정의한 휴관일 질문을 사용합니다.""",
            lesson_part="after",
        ),
        code(
            """# fixed_questions는 두 조건 모두에 같은 question 값을 사용합니다.
# 검사 함수를 통과한 뒤 고유 질문 수가 하나인지 다시 확인합니다.
fixed_questions = [question, question]
require_same_question(fixed_questions)
assert len(set(fixed_questions)) == 1
print("수정 후 질문 수:", len(fixed_questions))""",
            lesson_part="after",
        ),
    ],
    "06-단계적-공개와-설계-비교": [
        markdown("""# 06. 단계적 공개와 설계 비교

단계적 공개는 먼저 짧은 목록을 보고, 필요한 문서 ID를 고른 뒤, 해당 원문만 모델에 전달하는 방식입니다."""),
        markdown("""## 1. API 연결 준비"""),
        code(SETUP),
        markdown("""## 2. 목록과 원문을 분리합니다

목록은 선택을 돕고, 답은 선택한 원문에서 만듭니다."""),
        code("""# documents는 ID·제목·원문을 가진 문서 목록입니다.
# 리스트 컴프리헨션은 선택 화면에 필요한 ID와 제목만 catalog에 반환합니다.
documents = [
    {"id": "E01-p2", "title": "이용 시간", "text": "월요일 휴관"},
    {"id": "E01-p3", "title": "대출 규정",
     "text": "7권을 14일 대출. 예약이 없으면 1회 7일 연장."},
    {"id": "E01-p5", "title": "주차 안내", "text": "90분 무료"},
]
catalog = [{"id": d["id"], "title": d["title"]} for d in documents]
print(catalog)"""),
        markdown("""## 3. 필요한 ID의 원문만 공개합니다

이 예제에서는 학생이 `E01-p3`을 직접 선택합니다."""),
        code("""# selected_id는 질문에 맞춰 고른 문서 ID이고, next()는 첫 일치 문서를 반환합니다.
# full·selected·compressed의 문자 수를 비교해 공개 범위 차이를 확인합니다.
selected_id = "E01-p3"
selected = next(d for d in documents if d["id"] == selected_id)
full = "\\n".join(d["text"] for d in documents)
compressed = "7권, 14일, 예약 없으면 1회 7일 연장 [E01 p.3]"
print("full 문자 수:", len(full))
print("selected 문자 수:", len(selected["text"]))
print("compressed 문자 수:", len(compressed))"""),
        markdown("""## 4. 선택한 원문으로 답을 생성합니다"""),
        code('''# selected의 원문만 f-string에 넣어 모델에 전달할 prompt를 만듭니다.
# 질문과 근거를 한 문자열에 두되 출처 표기를 함께 남깁니다.
prompt = f"""근거 [E01 p.3]: {selected["text"]}
질문: 대출과 연장 조건은?"""'''),
        code(api_cell("prompt", "근거의 조건과 출처를 빠뜨리지 마세요.")),
        markdown("""## 정리

목록, 선택, 원문 읽기를 순서대로 수행합니다. 토큰 감소와 필요한 조건의 보존 여부를 함께 비교합니다."""),
        markdown(
            """## 실패 재현: 질문과 다른 문서를 선택합니다

대출 질문에 주차 문서를 선택하면 입력은 짧아져도 필요한 대출 근거가 사라집니다.""",
            lesson_part="before",
        ),
        code(
            """# selected_id는 실제 선택값, required_id는 질문에 필요한 문서 ID입니다.
# 두 값이 다르면 잘못된 문서 선택이므로 ValueError를 발생시킵니다.
def require_document(selected_id: str, required_id: str) -> None:
    if selected_id != required_id:
        raise ValueError(f"필요한 문서 {required_id}가 선택되지 않았습니다.")

try:
    require_document("E01-p5", "E01-p3")
except ValueError as error:
    print("관찰한 실패:", error)
else:
    raise AssertionError("문서 선택 오류가 발생해야 합니다.")""",
            lesson_part="before",
        ),
        markdown(
            """## 수정: 대출 규정 문서를 선택합니다

질문에 필요한 `E01-p3`을 선택하고 해당 원문을 확인합니다.""",
            lesson_part="after",
        ),
        code(
            """# fixed_id를 필요한 대출 규정 ID로 고친 뒤 선택 검사를 다시 실행합니다.
# next()로 실제 문서를 찾아 제목도 대출 규정인지 확인합니다.
fixed_id = "E01-p3"
require_document(fixed_id, "E01-p3")
fixed_document = next(d for d in documents if d["id"] == fixed_id)
assert fixed_document["title"] == "대출 규정"
print("수정 후 선택:", fixed_document["id"], fixed_document["title"])""",
            lesson_part="after",
        ),
    ],
}


def main() -> None:
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    for slug, cells in NOTEBOOK_DATA.items():
        install_note = markdown("""## 실행 환경 준비

첫 코드 셀은 노트북에서 사용할 패키지 버전을 맞춥니다. 설치가 끝나면 이어지는 셀을 순서대로 실행합니다.""")
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
        path = NOTEBOOKS / f"{slug}.ipynb"
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
