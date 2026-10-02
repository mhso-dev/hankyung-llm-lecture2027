"""Ch 6 학생용 노트북을 생성합니다."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NB = ROOT / "notebooks"


def md(text: str, part: str | None = None) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": ({"lesson_part": part} if part else {}),
        "source": text.splitlines(keepends=True),
    }


def code(text: str, part: str | None = None) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": ({"lesson_part": part} if part else {}),
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


INSTALL = '''# 현재 커널에 수업에서 검증한 버전을 설치합니다.
%pip install -q "langchain==1.4.0" "langchain-openai==1.6.0" "langchain-anthropic==1.7.1" "langchain-google-genai==4.4.0" "pydantic==2.13.5" "python-dotenv==1.2.3"'''
ENV = """from dotenv import find_dotenv, load_dotenv
import os

env_path = find_dotenv(usecwd=True)
if not env_path:
    raise FileNotFoundError("현재 폴더의 상위 경로에서 .env를 찾지 못했습니다.")
load_dotenv(env_path)
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(".env에 OPENAI_API_KEY가 없습니다.")
print("OPENAI_API_KEY 확인 완료")"""
MODEL = """from langchain.chat_models import init_chat_model

# provider:model은 통합 패키지와 모델을 함께 지정합니다.
# timeout은 한 요청의 최대 대기 초, max_retries는 SDK의 추가 시도 상한입니다.
# max_tokens는 생성할 출력 토큰 수의 상한입니다.
model = init_chat_model(
    "openai:gpt-5.4-mini",
    reasoning_effort="none",
    max_tokens=180,
    timeout=30,
    max_retries=1,
)
print(type(model).__name__)"""


def base(title: str, question: str) -> list[dict]:
    return [
        md(f"# {title}\n\n{question}"),
        md("## 실행 환경 준비\n\nPython 3.12 새 커널에서 패키지와 API 키 존재 여부를 확인합니다."),
        code(INSTALL),
        code(ENV),
        code(MODEL),
    ]


notebooks: dict[str, tuple[str, list[dict]]] = {}

cells = base(
    "01. 계층 지도와 첫 호출", "LangChain의 공통 모델 인터페이스는 첫 호출의 어느 부분을 맡을까요?"
)
cells += [
    md("## 메시지와 첫 호출\n\n역할이 있는 메시지 목록을 만들고 `invoke()`를 한 번 호출합니다."),
    code("""messages = [
    ("system", "두 문장 이내의 한국어로 답하세요."),
    ("user", "LangChain 모델 인터페이스의 장점을 한 가지 설명하세요."),
]
print("역할:", [role for role, _ in messages])"""),
    code("""response = model.invoke(messages)
print(response.text)
print("응답 타입:", type(response).__name__)
print("사용량 있음:", response.usage_metadata is not None)"""),
    md("## 값 하나 변경\n\n사용자 질문만 바꾸고 같은 모델 객체와 호출 방법을 유지합니다."),
    code("""changed = model.invoke([
    messages[0],
    ("user", "LangChain 모델 인터페이스를 한 문장으로 설명하세요."),
])
print(changed.text)
print("실제 반환 타입:", type(changed).__name__)"""),
    md("## 실패 재현", "before"),
    code(
        """bad_messages = [("user", None)]
try:
    if not all(isinstance(content, str) for _, content in bad_messages):
        raise TypeError("메시지 content는 문자열이어야 합니다.")
except TypeError as error:
    print("관찰한 예외 유형:", type(error).__name__)
else:
    raise AssertionError("잘못된 메시지는 예외가 발생해야 합니다.")""",
        "before",
    ),
    md("## 수정", "after"),
    code(
        """good_messages = [("user", "AIMessage라고만 답하세요.")]
fixed = model.invoke(good_messages)
print("수정 후 응답:", fixed.text)
assert fixed.text.strip()""",
        "after",
    ),
]
notebooks["01-계층-지도와-첫-호출"] = ("paired", cells)

cells = base(
    "02. 메시지와 제공자 전환",
    "같은 메시지를 세 제공자 설정에 적용할 때 무엇을 고정하고 무엇을 기록해야 할까요?",
)
cells += [
    md("## 같은 과제 정의\n\n질문과 출력 길이 요구를 고정합니다."),
    code("""messages = [
    ("system", "한 문장의 한국어로 답하세요."),
    ("user", "채팅 모델에서 system 메시지의 역할은 무엇인가요?"),
]
providers = {
    "openai": ("OPENAI_API_KEY", "openai:gpt-5.4-mini"),
    "anthropic": ("ANTHROPIC_API_KEY", "anthropic:claude-haiku-4-5"),
    "google": ("GOOGLE_API_KEY", "google_genai:gemini-2.5-flash-lite"),
}
print({name: bool(os.getenv(key)) for name, (key, _) in providers.items()})"""),
    md(
        "## 제공자별 실행\n\n설치와 키가 모두 준비된 제공자만 호출합니다. 이번 검증 환경에서는 OpenAI만 실행합니다."
    ),
    code("""records = []
for name, (key_name, model_id) in providers.items():
    if not os.getenv(key_name):  # 키 필요
        records.append({"provider": name, "status": f"skipped: {key_name} 필요"})
        continue
    current = init_chat_model(model_id, timeout=30, max_retries=1, max_tokens=180)
    answer = current.invoke(messages)
    records.append({
        "provider": name, "status": "executed", "text": answer.text,
        "usage": answer.usage_metadata, "content_blocks": answer.content_blocks,
    })
for record in records:
    print(record)"""),
    md(
        "## 메시지 객체로 같은 뜻 표현\n\n튜플 대신 명시적인 메시지 클래스를 사용해 역할을 확인합니다."
    ),
    code("""from langchain.messages import HumanMessage, SystemMessage

objects = [
    SystemMessage("한 문장의 한국어로 답하세요."),
    HumanMessage("채팅 모델에서 system 메시지의 역할은 무엇인가요?"),
]
print([item.type for item in objects])"""),
    md("## 실험 결과\n\n실행된 제공자와 건너뛴 제공자를 분리해 집계합니다."),
    code("""executed = [r["provider"] for r in records if r["status"] == "executed"]
skipped = [r["provider"] for r in records if r["status"].startswith("skipped")]
print("executed:", executed)
print("skipped:", skipped)"""),
]
notebooks["02-메시지와-제공자-전환"] = ("experiment", cells)

cells = base(
    "03. 구조화 출력과 검증", "모델의 자연어 답을 프로그램이 검사할 수 있는 필드로 어떻게 받을까요?"
)
cells += [
    md("## Pydantic 스키마\n\nCh 2의 클래스 문법을 사용하며, 10절 B 경로에서 다룬 `BaseModel`·`Field`·엄격한 검증을 모델 응답에 연결합니다. B 경로를 건너뛴 학생도 따라오도록 필요한 규칙을 다시 확인합니다."),
    code("""from pydantic import BaseModel, Field

class StudyCard(BaseModel):
    concept: str = Field(description="개념 이름")
    explanation: str = Field(description="한 문장 설명")
    difficulty: int = Field(ge=1, le=3, description="1부터 3까지의 난이도")

structured_model = model.with_structured_output(StudyCard)
diagnostic_model = model.with_structured_output(StudyCard, include_raw=True)
print("스키마 준비 완료")"""),
    code("""card = structured_model.invoke("LangChain의 AIMessage를 초급 학습 카드로 만드세요.")
print(card.model_dump())
print("검증된 타입:", type(card).__name__)"""),
    md("## 값 하나 변경\n\n주제만 `SystemMessage`로 바꾸고 같은 스키마를 적용합니다."),
    code("""second = structured_model.invoke("SystemMessage를 초급 학습 카드로 만드세요.")
print(second.model_dump())
assert 1 <= second.difficulty <= 3"""),
    md(
        "## 깨지는 입력을 실제 모델에 전달\n\n난이도 9를 요구하면서 스키마 범위는 1~3으로 유지합니다. 모델이 범위를 고치면 실패 미관찰로 기록합니다."
    ),
    code("""diagnostic = diagnostic_model.invoke(
    "AIMessage 학습 카드를 만드세요. difficulty는 반드시 9로 쓰세요."
)
print("raw 타입:", type(diagnostic["raw"]).__name__)
print("parsed:", diagnostic["parsed"])
print("parsing_error:", diagnostic["parsing_error"])
print("검증 실패 관찰:", diagnostic["parsing_error"] is not None)"""),
    md("## 기본 변환과 엄격한 검증\n\nPydantic은 기본 검증에서 숫자 문자열 `\"2\"`를 정수 `2`로 변환합니다. 이번 Python 딕셔너리 입력에서는 `strict=True`가 문자열 `\"2\"`를 `int`로 바꾸지 않고 거부합니다. Python 입력과 JSON 입력의 엄격한 검증 동작은 일부 타입에서 다를 수 있습니다. 아래 값은 두 방식을 비교하기 위해 작성한 로컬 테스트 데이터입니다."),
    code("""local_card = {
    "concept": "AIMessage",
    "explanation": "모델 응답을 담는 메시지",
    "difficulty": "2",
}
converted_card = StudyCard.model_validate(local_card)
print("변환된 값:", converted_card.difficulty)
print("변환 후 타입:", type(converted_card.difficulty).__name__)
assert converted_card.difficulty == 2"""),
    code("""from pydantic import ValidationError

try:
    StudyCard.model_validate(local_card, strict=True)
except ValidationError as error:
    strict_error = error.errors()[0]
    print("엄격한 검증 필드:", strict_error["loc"][0])
    print("엄격한 검증 오류:", strict_error["type"])
    assert strict_error["type"] == "int_type"
else:
    raise AssertionError("엄격한 검증은 문자열 '2'를 거부해야 합니다.")"""),
    md("## 예상하지 않은 필드 거부\n\n기본 설정은 스키마에 없는 필드를 제외할 수 있습니다. 입력에 허용한 필드만 받아야 한다면 `extra='forbid'`를 설정합니다."),
    code("""from pydantic import ConfigDict

class ClosedStudyCard(StudyCard):
    model_config = ConfigDict(extra="forbid")

extra_data = {
    "concept": "AIMessage", "explanation": "모델 응답",
    "difficulty": 2, "source": "로컬 메모",
}
try:
    ClosedStudyCard.model_validate(extra_data)
except ValidationError as error:
    extra_error = error.errors()[0]
    print("거부된 필드:", extra_error["loc"][0])
    print("검증 오류:", extra_error["type"])
    assert extra_error["type"] == "extra_forbidden"
else:
    raise AssertionError("추가 필드는 거부되어야 합니다.")"""),
    md("## JSON 문법과 스키마 값 제약\n\n`json.loads`는 JSON 문법을, Pydantic은 파싱된 객체의 필드·타입·범위를 검사합니다. 둘을 통과해도 주문이 실제로 존재하는지나 품명이 사실인지는 별도로 확인합니다."),
    code("""import json

class OrderItem(BaseModel):
    product_name: str = Field(min_length=1, description="품명")
    quantity: int = Field(ge=1, description="1 이상의 수량")

valid_text = '{"product_name": "노트", "quantity": 2}'
parsed_order = json.loads(valid_text)
valid_order = OrderItem.model_validate(parsed_order)
print("JSON 형식: 통과")
print("주문 내용:", valid_order.model_dump())"""),
    code("""broken_text = '{"product_name": "노트", "quantity": 2'
try:
    json.loads(broken_text)
except json.JSONDecodeError as error:
    print("JSON 형식 오류:", type(error).__name__)

wrong_content = '{"product_name": "노트", "quantity": 0}'
parsed_wrong = json.loads(wrong_content)
try:
    OrderItem.model_validate(parsed_wrong)
except ValidationError as error:
    content_error = error.errors()[0]
    print("주문 내용 오류:", content_error["type"])
    assert content_error["type"] == "greater_than_equal"
else:
    raise AssertionError("수량 0은 거부되어야 합니다.")"""),
    md("## 실패 재현", "before"),
    code(
        """from pydantic import ValidationError

bad_data = {"concept": "AIMessage", "explanation": "모델 응답", "difficulty": 7}
try:
    StudyCard.model_validate(bad_data)
except ValidationError as error:
    print("관찰한 검증 오류:", error.errors()[0]["type"])
else:
    raise AssertionError("범위를 벗어난 값은 거부되어야 합니다.")""",
        "before",
    ),
    md("## 수정", "after"),
    code(
        """fixed_data = {"concept": "AIMessage", "explanation": "모델 응답", "difficulty": 2}
fixed_card = StudyCard.model_validate(fixed_data)
print(fixed_card.model_dump())
assert fixed_card.difficulty == 2""",
        "after",
    ),
]
notebooks["03-구조화-출력과-검증"] = ("paired", cells)

cells = base(
    "04. 스트리밍과 content blocks",
    "응답 조각은 어떤 순서로 도착하고 최종 텍스트와 어떻게 연결될까요?",
)
cells += [
    md("## 스트리밍 호출\n\n`stream()`이 반환하는 `AIMessageChunk`를 도착 순서대로 저장합니다."),
    code("""messages = [("user", "LangChain 스트리밍을 열두 단어 이내로 설명하세요.")]
chunks = []
for chunk in model.stream(messages):
    chunks.append(chunk)
    print(chunk.text, end="", flush=True)
print()
print("조각 수:", len(chunks))"""),
    md("## 조각 결합\n\n`+` 연산으로 메시지 조각을 결합하고 최종 텍스트를 확인합니다."),
    code("""combined = chunks[0]
for chunk in chunks[1:]:
    combined = combined + chunk
print("결합 텍스트:", combined.text)
print("결합 성공:", bool(combined.text.strip()))"""),
    md(
        "## content blocks 관찰\n\n각 조각의 표준 콘텐츠 블록 수를 세되 제공자별 블록 모양을 단정하지 않습니다."
    ),
    code("""block_counts = [len(chunk.content_blocks) for chunk in chunks]
print("조각별 블록 수:", block_counts)
print("전체 블록 수:", sum(block_counts))
representative = next((c.content_blocks[0] for c in chunks if c.content_blocks), None)
print("대표 content block:", representative)
print("결합 메시지 usage 있음:", combined.usage_metadata is not None)"""),
    md("## invoke와 결과 비교\n\n같은 질문을 일반 호출로 한 번 더 실행해 반환 타입을 비교합니다."),
    code("""single = model.invoke(messages)
print("stream 반환 타입:", type(chunks[0]).__name__)
print("invoke 반환 타입:", type(single).__name__)
print("두 결과 모두 텍스트 있음:", bool(combined.text and single.text))"""),
]
notebooks["04-스트리밍과-content-blocks"] = ("experiment", cells)

cells = base(
    "05. 타임아웃 재시도 폴백",
    "일시적인 실패를 몇 번까지 다시 시도하고 언제 대체 경로를 선택해야 할까요?",
)
cells += [
    md(
        "## 실제 호출의 제한 설정\n\n모델 객체에 타임아웃과 최대 재시도 횟수가 설정되었음을 직렬화 가능한 설정에서 확인합니다."
    ),
    code("""print("기본 모델 타입:", type(model).__name__)
healthy = model.invoke("재시도는 왜 횟수를 제한해야 하나요? 한 문장으로 답하세요.")
print(healthy.text)"""),
    md(
        "## 결정적인 로컬 시뮬레이션\n\n네트워크 장애를 꾸며 내지 않고, 실패하는 Runnable로 제어 흐름만 검증합니다."
    ),
    code("""from langchain_core.runnables import RunnableLambda

attempts = {"primary": 0}
def fail_primary(value: str) -> str:
    attempts["primary"] += 1
    raise TimeoutError("수업용 로컬 타임아웃")

primary = RunnableLambda(fail_primary)
fallback = RunnableLambda(lambda value: f"대체 경로: {value}")"""),
    md(
        "## 제한된 재시도\n\n첫 시도만 실패하고 두 번째 시도에 성공하는 함수로 실제 재시도 횟수를 셉니다."
    ),
    code("""retry_attempts = {"count": 0}
def transient(value: str) -> str:
    retry_attempts["count"] += 1
    if retry_attempts["count"] == 1:
        raise TimeoutError("수업용 일시 오류")
    return f"재시도 성공: {value}"

retrying = RunnableLambda(transient).with_retry(
    retry_if_exception_type=(TimeoutError,), stop_after_attempt=2
)
print(retrying.invoke("질문"))
print("총 시도 횟수:", retry_attempts["count"])"""),
    md("## 실패 재현", "before"),
    code(
        """try:
    primary.invoke("질문")
except TimeoutError as error:
    print("로컬 시뮬레이션:", type(error).__name__)
    print("시도 횟수:", attempts["primary"])
else:
    raise AssertionError("기본 경로는 실패해야 합니다.")""",
        "before",
    ),
    md("## 폴백 연결", "after"),
    code(
        """safe_chain = primary.with_fallbacks([fallback], exceptions_to_handle=(TimeoutError,))
result = safe_chain.invoke("질문")
print(result)
print("누적 기본 경로 시도:", attempts["primary"])
assert result.startswith("대체 경로")""",
        "after",
    ),
]
notebooks["05-타임아웃-재시도-폴백"] = ("paired", cells)

cells = base(
    "06. 토큰 비용 지연 비교",
    "같은 과제를 여러 제공자에 보낼 때 어떤 원자료를 남겨야 공정하게 비교할 수 있을까요?",
)
cells += [
    md("## 비교 조건 고정\n\n질문, 반복 횟수, 출력 상한을 기록합니다."),
    code("""import json
import time

messages = [("user", "AIMessage의 역할을 한 문장으로 설명하세요.")]
conditions = {"repetitions": 1, "max_tokens": 180, "same_messages": True}
provider_specs = {
    "openai": ("OPENAI_API_KEY", "openai:gpt-5.4-mini", 0.75, 0.075, 4.50),
    "anthropic": ("ANTHROPIC_API_KEY", "anthropic:claude-haiku-4-5", 1.00, None, 5.00),
    "google": ("GOOGLE_API_KEY", "google_genai:gemini-2.5-flash-lite", 0.10, None, 0.40),
}
print(conditions)"""),
    md(
        "## OpenAI 실제 측정\n\n호출 직전과 직후의 단조 시계를 읽고 API가 보고한 토큰 수를 저장합니다."
    ),
    code("""def estimate_cost(usage, input_rate, cached_input_rate, output_rate):
    input_tokens = usage.get("input_tokens")
    output_tokens = usage.get("output_tokens")
    if input_tokens is None or output_tokens is None:
        return None
    cache_read = (usage.get("input_token_details") or {}).get("cache_read") or 0
    if cache_read and cached_input_rate is None:
        return None
    normal_input = input_tokens - cache_read
    return (normal_input * input_rate + cache_read * (cached_input_rate or input_rate)
            + output_tokens * output_rate) / 1_000_000"""),
    code("""records = []
for name, rates in provider_specs.items():
    key_name, model_id, input_rate, cached_input_rate, output_rate = rates
    if not os.getenv(key_name):  # 키 필요
        records.append({"provider": name, "model_id": model_id,
                        "status": f"skipped: {key_name} 필요"})
        continue
    current = init_chat_model(model_id, timeout=30, max_retries=1, max_tokens=180)
    started = time.perf_counter()
    answer = current.invoke(messages)
    elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
    usage = answer.usage_metadata or {}
    cache_read = (usage.get("input_token_details") or {}).get("cache_read") or 0
    cost = estimate_cost(usage, input_rate, cached_input_rate, output_rate)
    records.append({"provider": name, "model_id": model_id,
                    "status": "executed", "text": answer.text,
                    "latency_ms": elapsed_ms, "usage": usage,
                    "cache_read_tokens": cache_read,
                    "estimated_cost_usd": None if cost is None else round(cost, 8),
                    "pricing_date": "2026-09-09"})
    print(records[-1])"""),
    md(
        "## 준비되지 않은 제공자 기록\n\n키가 없는 제공자는 0으로 채우지 않고 건너뜀 상태로 남깁니다."
    ),
    code("""# 위 셀은 키가 있는 제공자를 모두 실행하고, 없는 제공자는 건너뜁니다.
for record in records:
    print(record["provider"], record["status"])"""),
    md(
        "## 관찰 범위\n\n한 번의 측정으로 제공자 전체 성능을 단정하지 않고 실행 여부와 원자료 완전성을 확인합니다."
    ),
    code("""executed = [r for r in records if r["status"] == "executed"]
print("실행 건수:", len(executed))
print("비교 가능한 제공자 수:", len(executed))
print("여러 제공자 측정값 있음:", len(executed) >= 2)
assert executed[0]["latency_ms"] > 0"""),
    md("## 실행 기록 보존\n\nCh 7에서 공통 필드를 다시 읽을 수 있도록 정본과 실행별 사본을 함께 저장합니다."),
    code("""from datetime import datetime, timezone
from pathlib import Path

run_at = datetime.now(timezone.utc)
session_id = run_at.strftime("%Y%m%dT%H%M%S%fZ")
pricing = {"date": "2026-09-09", "unit": "USD per 1M tokens",
           "openai": {"ordinary_input": 0.75, "cached_input": 0.075, "output": 4.50}}
record = {"run_id": f"ch06-provider-{session_id}", "run_date": run_at.date().isoformat(),
          "source_chapter": "ch06", "conditions": conditions, "pricing": pricing, "records": records}
course_root = next((path for path in [Path.cwd(), *Path.cwd().parents]
                    if (path / "labs/part2/ch06-langchain-start").is_dir()), None)
if course_root is None:
    raise FileNotFoundError("실습 묶음의 labs/part2 폴더를 찾지 못했습니다.")
runs_dir = course_root / "labs/part2/ch06-langchain-start/runs"
canonical_path = runs_dir / "provider-comparison-continuity.json"
session_path = runs_dir / "continuity" / session_id / canonical_path.name
session_path.parent.mkdir(parents=True, exist_ok=False)
payload = json.dumps(record, ensure_ascii=False, indent=2)
canonical_path.write_text(payload, encoding="utf-8")
session_path.write_text(payload, encoding="utf-8")
print(canonical_path.relative_to(course_root), "보존 사본:", session_path.relative_to(course_root))"""),
]
notebooks["06-토큰-비용-지연-비교"] = ("experiment", cells)

COMMENTS = {
    "01-계층-지도와-첫-호출": [
        "현재 커널에 네 수업 패키지의 검증 버전을 설치합니다.",
        "상위 폴더에서 .env를 찾고 키 값은 출력하지 않은 채 존재 여부만 확인합니다.",
        "제공자·모델과 초 단위 타임아웃, 재시도·출력 상한을 가진 모델 객체를 만듭니다.",
        "messages 목록의 0번 system 규칙을 이후 비교 호출에서도 그대로 재사용합니다.",
        "invoke 반환값의 text·실제 타입·usage_metadata 존재 여부를 확인합니다.",
        "사용자 질문만 바꾸고 모델 객체와 system 메시지는 그대로 둡니다.",
        "API 요청 전에 content 타입을 검사해 예상한 TypeError만 처리합니다.",
        "잘못된 None 하나를 문자열로 고친 뒤 같은 invoke 경로가 성공하는지 확인합니다.",
    ],
    "02-메시지와-제공자-전환": [
        "현재 커널에 세 provider 통합 패키지의 검증 버전을 설치합니다.",
        "상위 폴더의 .env에서 OpenAI 키 존재 여부만 확인하고 비밀값은 출력하지 않습니다.",
        "기본 OpenAI 모델 객체의 모델 ID와 초 단위 제한을 설정합니다.",
        "provider마다 환경 변수 이름과 model ID를 한 쌍으로 기록합니다.",
        "키가 있으면 해당 모델을 호출하고, 없으면 continue로 건너뜀 상태를 남깁니다.",
        "튜플과 같은 역할 구조를 명시적인 SystemMessage·HumanMessage로 만듭니다.",
        "records에서 실제 실행 행과 키가 없어 건너뛴 행을 분리합니다.",
    ],
    "03-구조화-출력과-검증": [
        "현재 커널에 구조화 출력 실습의 고정 패키지 버전을 설치합니다.",
        "상위 폴더에서 .env를 찾고 OpenAI 키 문자열은 화면에 표시하지 않습니다.",
        "구조화 출력 호출에도 적용할 타임아웃과 최대 재시도·출력 토큰 상한을 둡니다.",
        "StudyCard 필드와 difficulty의 허용 범위 1~3을 선언합니다.",
        "invoke가 반환한 StudyCard를 딕셔너리로 바꾸고 실제 타입을 확인합니다.",
        "주제만 바꾼 두 번째 객체가 같은 difficulty 범위를 지키는지 검사합니다.",
        "include_raw 결과의 raw·parsed·parsing_error를 각각 출력해 실패 미관찰도 남깁니다.",
        "기본 검증은 정수로 표현할 수 있는 문자열을 변환합니다.",
        "엄격한 검증은 값을 변환하지 않고 잘못된 타입을 거부합니다.",
        "허용하지 않은 source 필드가 포함되면 검증이 실패합니다.",
        "정상 JSON을 파싱한 뒤 주문 내용 규칙을 검증합니다.",
        "JSON 형식 오류와 주문 내용 오류를 각각 확인합니다.",
        "범위 밖 7을 직접 넣어 예상한 Pydantic ValidationError 유형만 처리합니다.",
        "다른 필드는 유지하고 difficulty만 2로 고쳐 검증된 객체를 만듭니다.",
    ],
    "04-스트리밍과-content-blocks": [
        "현재 커널에 스트리밍 실습의 고정 패키지 버전을 설치합니다.",
        "상위 폴더에서 .env를 찾고 API 키의 존재 여부만 확인합니다.",
        "스트리밍에도 같은 모델 ID와 초 단위 타임아웃·출력 상한을 적용합니다.",
        "stream이 내보내는 AIMessageChunk를 도착 순서대로 chunks 목록에 저장합니다.",
        "청크의 + 연산으로 메타데이터를 보존한 최종 AIMessageChunk를 만듭니다.",
        "각 청크의 표준 content_blocks 개수와 합계를 관찰값으로 남깁니다.",
        "같은 질문의 invoke 반환 타입과 결합 청크 타입을 비교합니다.",
    ],
    "05-타임아웃-재시도-폴백": [
        "현재 커널에 Runnable 재시도·폴백 실습의 고정 패키지 버전을 설치합니다.",
        "상위 폴더에서 .env를 찾고 OpenAI 키 값은 출력하지 않습니다.",
        "timeout은 초 단위 대기 상한, max_retries는 SDK의 추가 시도 상한으로 설정합니다.",
        "실제 API가 정상인 현재 조건의 응답을 로컬 오류 시뮬레이션과 분리합니다.",
        "primary는 항상 TimeoutError를 내고 fallback은 대체 문자열을 반환합니다.",
        "첫 실행만 실패하는 함수에 with_retry의 총 시도 상한 2회를 적용합니다.",
        "폴백 없이 primary 한 번의 예상한 TimeoutError와 시도 횟수를 확인합니다.",
        "TimeoutError에만 with_fallbacks를 적용해 대체 경로 반환값을 확인합니다.",
    ],
    "06-토큰-비용-지연-비교": [
        "현재 커널에 세 provider 비교에 필요한 통합 패키지 버전을 설치합니다.",
        "상위 폴더에서 .env를 찾고 OpenAI 키의 존재 여부만 확인합니다.",
        "비교 호출에 공통으로 쓸 모델 ID·초 단위 제한·출력 토큰 상한을 둡니다.",
        "같은 메시지와 반복 수, USD/100만 토큰 단가를 provider별로 기록합니다.",
        "입력 토큰에서 캐시 사용량을 빼고 일반·캐시 단가를 나누어 적용합니다.",
        "키가 있는 제공자를 호출하고 사용량·지연·예상 비용을 한 레코드로 남깁니다.",
        "앞 셀의 records에서 provider 이름과 executed·skipped 상태만 모아 확인합니다.",
        "실행 행을 세어 여러 provider의 측정값이 있는지만 판단하고 우열은 단정하지 않습니다.",
        "Ch 7이 읽을 정본과 이번 실행의 불변 사본을 같은 JSON으로 저장합니다.",
    ],
}

for slug, (lesson_format, cells) in notebooks.items():
    code_index = 0
    for cell in cells:
        if cell["cell_type"] == "code":
            cell["source"] = [f"# {COMMENTS[slug][code_index]}\n", *cell["source"]]
            code_index += 1
    for index, cell in enumerate(cells, 1):
        cell["id"] = f"cell-{index:02d}"
    data = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "lesson_format": lesson_format,
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path = NB / f"{slug}.ipynb"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", path.name)
