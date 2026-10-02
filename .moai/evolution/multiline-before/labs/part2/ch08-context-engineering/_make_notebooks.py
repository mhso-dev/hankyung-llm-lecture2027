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


SETUP = """from dotenv import find_dotenv, load_dotenv
from langchain.chat_models import init_chat_model
import os

env_path = find_dotenv(usecwd=True)
if not env_path:
    raise FileNotFoundError("현재 폴더의 상위 경로에서 .env를 찾지 못했습니다.")
load_dotenv(env_path)
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(".env에 OPENAI_API_KEY가 없습니다.")
model = init_chat_model("openai:gpt-5.4-mini", reasoning_effort="none", max_tokens=300)
print("LangChain 모델 준비 완료")"""

INSTALL = (
    '%pip install -q "langchain==1.4.0" "langchain-openai==1.6.0" '
    '"python-dotenv==1.2.3" "tiktoken==0.14.0"'
)


def api_cell(prompt_name: str, instructions: str) -> str:
    return f'''messages = [
    ("system", "{instructions}"),
    ("user", {prompt_name}),
]
response = model.invoke(messages)
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
        code("""def input_budget(total: int, output_reserve: int, safety_margin: int) -> int:
    available = total - output_reserve - safety_margin
    if available < 0:
        raise ValueError("출력 예약분과 여유가 전체 예산보다 큽니다.")
    return available

available = input_budget(4096, 300, 128)
print("입력에 사용할 수 있는 토큰:", available)"""),
        markdown("""## 3. 로컬 추정값을 확인합니다

토크나이저의 추정값은 호출 전 차단에 쓰고, `AIMessage.usage_metadata`는 호출 후 기록에 씁니다."""),
        code("""import tiktoken

question = "미르시립도서관의 정기 휴관일은 언제인가요?"
evidence = "[E01 p.2] 정기 휴관일은 매주 월요일입니다."
prompt = f"근거:\\n{evidence}\\n\\n질문: {question}"
encoding = tiktoken.get_encoding("o200k_base")
estimated = len(encoding.encode(prompt))
print("로컬 추정 입력 토큰:", estimated)
print("예산 안에 있음:", estimated <= available)"""),
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
            """bad_total = 300
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
            """fixed_total = 4096
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
        code("""import json
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
        code("""selected_ids = {"E01-p3", "E01-p5"}
selected = [row for row in loaded if row["id"] in selected_ids]
for row in selected:
    print(row["id"], row["topic"], row["text"])"""),
        markdown("""## 4. 선택한 기록으로 답을 생성합니다

모델에는 저장소 전체 대신 선택한 두 기록만 전달합니다."""),
        code("""context = "\\n".join(f"[{r['id']}] {r['text']}" for r in selected)
prompt = f'근거:\\n{context}\\n\\n질문: 대출 권수와 주차 무료 시간을 알려 주세요.'"""),
        code(api_cell("prompt", "제공된 근거만 사용하고 문장마다 식별자를 붙이세요.")),
        markdown("""## 정리

외부 기록은 저장만으로 모델에 전달되지 않습니다. 질문에 맞는 항목을 선택하여 호출 입력에 넣어야 합니다."""),
        markdown(
            """## 실패 재현: 저장한 기록을 선택하지 않습니다

파일에 기록이 있어도 선택 결과가 비어 있으면 모델에 전달할 근거가 없습니다.""",
            lesson_part="before",
        ),
        code(
            """def require_context(rows: list[dict[str, str]]) -> None:
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
            """require_context(selected)
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
        code("""def compress(record: dict[str, str]) -> str:
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
        code("""question = "대출 권수, 기간, 연장 조건을 알려 주세요."
prompt = f"[근거]\\n{compressed}\\n\\n[질문]\\n{question}"
print(prompt)"""),
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
            """broken = {"fact": "7권을 14일 대출", "condition": "회원 1명 기준",
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
            """fixed = {**broken, "exception": loan["exception"]}
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
        code("""clean = "[E01 p.2] 미르시립도서관은 매주 월요일 휴관입니다."
noise = "회의 안건: 행사 배너와 좌석 배치를 논의했습니다. " * 12
conditions = {
    "clean": clean,
    "poisoning": f"{clean}\\n[미검증 메모] 휴관일은 화요일입니다.",
    "distraction": f"{noise}\\n{clean}",
    "confusion": f"{clean}\\n[미르고등학교 도서실] 화요일 휴관입니다.",
    "clash": f"{clean}\\n[합성 부록] 미르시립도서관은 수요일 휴관입니다.",
}
print("실험 조건:", list(conditions))"""),
        markdown("""## 3. 같은 질문으로 다섯 조건을 실행합니다

어떤 실패가 나타날지 미리 정하지 않습니다. 조건 이름, 실제 입력 토큰, 응답 원문을 나란히 기록합니다."""),
        code("""results = {}
for name, context in conditions.items():
    messages = [
        ("system", "근거만 사용하고, 충돌하면 확인이 필요하다고 답하세요."),
        ("user", f"근거:\\n{context}\\n\\n질문: 정기 휴관일은 언제인가요?"),
    ]
    response = model.invoke(messages)
    usage = response.usage_metadata
    if usage is None:
        raise RuntimeError("모델 사용량 메타데이터가 없습니다.")
    results[name] = response
    print(f"\\n[{name}] input_tokens={usage['input_tokens']}")
    print(response.text)"""),
        markdown("""## 4. 출력에서 관찰한 문자열을 비교합니다

요일과 확인 요청 표현의 등장 여부만 표시합니다. 이 표만으로 답의 완결성을 확정하지 않고 응답 원문을 함께 읽습니다."""),
        code("""for name, response in results.items():
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
            """def require_versions(items: list[str]) -> None:
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
            """versioned = [
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
        code("""evidence = "[E01 p.2] 정기 휴관일은 매주 월요일입니다."
question = "미르시립도서관의 정기 휴관일과 출처를 알려 주세요."
noise = "회의 준비 항목을 확인했습니다. " * 120
prompts = {
    "short": f"근거:\\n{evidence}\\n\\n질문: {question}",
    "long": f"근거:\\n{noise}\\n{evidence}\\n\\n질문: {question}",
}
print({name: len(text) for name, text in prompts.items()})"""),
        markdown("""## 3. 두 조건의 실제 사용량을 측정합니다

두 호출의 입력 토큰과 답을 나란히 출력합니다. 두 번의 호출만으로 일반 결론을 내리지는 않습니다."""),
        code("""results = {}
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
        code("""for name, result in results.items():
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
            """def require_same_question(questions: list[str]) -> None:
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
            """fixed_questions = [question, question]
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
        code("""documents = [
    {"id": "E01-p2", "title": "이용 시간", "text": "월요일 휴관"},
    {"id": "E01-p3", "title": "대출 규정",
     "text": "7권을 14일 대출. 예약이 없으면 1회 7일 연장."},
    {"id": "E01-p5", "title": "주차 안내", "text": "90분 무료"},
]
catalog = [{"id": d["id"], "title": d["title"]} for d in documents]
print(catalog)"""),
        markdown("""## 3. 필요한 ID의 원문만 공개합니다

이 예제에서는 학생이 `E01-p3`을 직접 선택합니다."""),
        code("""selected_id = "E01-p3"
selected = next(d for d in documents if d["id"] == selected_id)
full = "\\n".join(d["text"] for d in documents)
compressed = "7권, 14일, 예약 없으면 1회 7일 연장 [E01 p.3]"
print("full 문자 수:", len(full))
print("selected 문자 수:", len(selected["text"]))
print("compressed 문자 수:", len(compressed))"""),
        markdown("""## 4. 선택한 원문으로 답을 생성합니다"""),
        code("""prompt = f'근거 [E01 p.3]: {selected["text"]}\\n질문: 대출과 연장 조건은?'"""),
        code(api_cell("prompt", "근거의 조건과 출처를 빠뜨리지 마세요.")),
        markdown("""## 정리

목록, 선택, 원문 읽기를 순서대로 수행합니다. 토큰 감소와 필요한 조건의 보존 여부를 함께 비교합니다."""),
        markdown(
            """## 실패 재현: 질문과 다른 문서를 선택합니다

대출 질문에 주차 문서를 선택하면 입력은 짧아져도 필요한 대출 근거가 사라집니다.""",
            lesson_part="before",
        ),
        code(
            """def require_document(selected_id: str, required_id: str) -> None:
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
            """fixed_id = "E01-p3"
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
