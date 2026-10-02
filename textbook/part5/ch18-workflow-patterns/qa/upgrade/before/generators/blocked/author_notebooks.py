"""Ch18의 독립 실행 노트북 여섯 개를 생성한다."""

from __future__ import annotations

# 개선 전(2026-09-10~14) 생성기입니다. 지금 교재·노트북·그림은 이 파일이 만들지 않습니다.
# 실행하면 노트북 여섯 개을 옛 판으로 덮어씁니다. 읽기 자료로만 둡니다.
# 절 생성기는 textbook/part5/ch18-workflow-patterns/qa/upgrade/author_NN.py입니다.
raise SystemExit("개선 전 생성기입니다. textbook/part5/ch18-workflow-patterns/qa/upgrade/author_NN.py를 쓰세요.")

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
NOTEBOOKS = HERE / "notebooks"


def markdown(text: str, lesson_part: str | None = None) -> dict:
    metadata = {} if lesson_part is None else {"lesson_part": lesson_part}
    return {"cell_type": "markdown", "id": "", "metadata": metadata, "source": text.splitlines(keepends=True)}


def cell_purpose(text: str) -> str:
    purposes = [
        ("candidate_prompts =", "두 후보를 만들고 세 평가자의 표를 수집한 뒤 유효표를 집계합니다."),
        ("history: list[dict]", "초안 생성과 평가를 반복하고 실제 점수에 따라 중단 여부를 판단합니다."),
        ("print(\"반복 기록:\"", "반복 이력, 중단 이유, 최종 초안과 성공 응답 사용량을 출력합니다."),
        ("import asyncio", "비동기 API 호출과 사용량 측정에 필요한 도구를 준비합니다."),
        ("import json", "동기 API 호출과 사용량 측정에 필요한 도구를 준비합니다."),
        ("async def call_json", "비동기 Responses API의 JSON 응답과 사용량을 기록합니다."),
        ("def call_json", "동기 Responses API의 JSON 응답과 사용량을 기록합니다."),
        ("async def call_answer", "비동기 응답의 answer 형식을 엄격하게 검사합니다."),
        ("def call_answer", "동기 응답의 answer 형식을 엄격하게 검사합니다."),
        ("def cost_usd", "반환된 토큰 사용량으로 할인 없는 비용을 추정합니다."),
        ("def outline_gate", "완전한 예시로 체이닝 게이트의 통과 조건을 확인합니다."),
        ("before = call_json", "필드가 빠진 실제 중간 출력에서 후속 호출을 중단합니다."),
        ("outline = call_json", "검사에 통과한 기획만 최종 안내문 호출에 전달합니다."),
        ("ALLOWED =", "분류값과 신뢰도를 검사해 사용할 전문 경로를 결정합니다."),
        ("prompts =", "허용 목록 밖 분류를 사전 키로 쓸 때의 문제를 확인합니다."),
        ("def answer_ticket", "유효한 분류는 전문 경로로 보내고 나머지는 추가 정보를 요청합니다."),
        ("brief =", "독립적인 세 섹션을 동시에 작성하고 지연을 측정합니다."),
        ("candidate_prompts", "두 후보를 만들고 세 평가자의 표를 동시에 수집합니다."),
        ("총 호출:", "병렬 실험의 호출 수와 토큰, 비용 추정치를 출력합니다."),
        ("task =", "입력에 필요한 하위 작업을 모델이 동적으로 만들게 합니다."),
        ("async def run_worker", "계획에 포함된 작업 수만큼 워커를 동시에 실행합니다."),
        ("synthesis =", "검사된 워커 결과를 엄격한 answer 형식으로 종합합니다."),
        ("MAX_ITERATIONS", "생성자와 평가자 반복에 적용할 세 정지 조건을 선언합니다."),
        ("history:", "초안 생성과 평가를 반복하며 정지 이유를 기록합니다."),
        ("반복 기록:", "반복 횟수와 실제로 작동한 정지 조건을 확인합니다."),
        ("def grade", "다섯 패턴에 공통으로 적용할 과제와 채점 기준을 선언합니다."),
        ("outline = await", "체이닝과 라우팅을 같은 과제로 실행합니다."),
        ("section_jobs", "세 부분을 동시에 작성한 뒤 실제 내용을 편집자에게 전달합니다."),
        ("plan = await", "동적 계획에서 나온 작업만 워커와 종합 호출에 사용합니다."),
        ("evaluations =", "생성자와 평가자를 실행하고 품질 임계값을 적용합니다."),
        ("rows =", "패턴별 호출 수와 토큰, 지연, 품질을 같은 표로 집계합니다."),
    ]
    return next((comment for marker, comment in purposes if marker in text),
                "이 셀의 입력과 출력을 다음 워크플로우 단계에 맞게 처리합니다.")


def code(text: str, lesson_part: str | None = None) -> dict:
    metadata = {} if lesson_part is None else {"lesson_part": lesson_part}
    lines = [line for line in text.strip().splitlines() if line.strip()]
    if not lines[0].lstrip().startswith("#"):
        lines.insert(0, "# " + cell_purpose(text))
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": "",
        "metadata": metadata,
        "outputs": [],
        "source": [line + "\n" for line in lines],
    }


def helper_cells(source: str) -> list[dict]:
    answer_marker = "async def call_answer" if "async def call_json" in source else "def call_answer"
    answer_at = source.index(answer_marker)
    utility_at = source.index("def cost_usd")
    async_mode = "async def call_json" in source
    call_json_note = (
        "`call_json()`은 `await client.responses.create()`에서 실제 요청을 기다리고, "
        "JSON 텍스트를 파이썬 사전으로 바꾸어 반환합니다."
        if async_mode else
        "`call_json()`은 `client.responses.create()`에서 실제 요청을 보내고, "
        "JSON 텍스트를 파이썬 사전으로 바꾸어 반환합니다."
    )
    call_answer_note = (
        "`call_answer()`는 answer 문자열 하나만 허용하는 JSON Schema를 요청에 넣고, "
        "반환값이 비어 있지 않은지 다시 검사합니다. 형식 통과가 사실 정확성을 보장하지는 않습니다."
    )
    utility_note = (
        "`cost_usd()`는 기록한 성공 응답의 토큰을 합산합니다. `score_of()`는 평가 점수가 "
        "불리언이 아닌 숫자이며 0~100 범위인지 확인합니다. 두 함수는 모델을 호출하지 않습니다."
    )
    return [
        markdown("### JSON 응답 helper 읽기\n\n" + call_json_note),
        code(source[:answer_at].rstrip()),
        markdown("### answer 응답 helper 읽기\n\n" + call_answer_note),
        code(source[answer_at:utility_at].rstrip()),
        markdown("### 측정 helper 읽기\n\n" + utility_note),
        code(source[utility_at:].rstrip()),
    ]


INSTALL = """# 이 장은 OpenAI SDK를 직접 배우므로 두 패키지만 고정합니다.
%pip install -q openai==2.29.0 python-dotenv==1.2.3"""

SYNC_SETUP_NOTE = """### 동기 클라이언트 준비 읽기

`load_dotenv(find_dotenv(usecwd=True))`는 현재 폴더에서 위로 올라가며 `.env`를 찾습니다. `OpenAI(timeout=45.0, max_retries=0)`는 동기 클라이언트를 만들며 아직 모델을 호출하지 않습니다. `calls`는 이후 성공 응답의 지연과 토큰을 모을 빈 목록입니다."""

ASYNC_SETUP_NOTE = """### 비동기 클라이언트 준비 읽기

`load_dotenv(find_dotenv(usecwd=True))`는 현재 폴더에서 위로 올라가며 `.env`를 찾습니다. `AsyncOpenAI(timeout=45.0, max_retries=0)`는 비동기 클라이언트를 만들며 아직 모델을 호출하지 않습니다. `calls`는 이후 성공 응답의 지연과 토큰을 모을 빈 목록입니다."""

SYNC_SETUP = """import json
import os
import time
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

load_dotenv(find_dotenv(usecwd=True))
assert os.getenv("OPENAI_API_KEY"), "프로젝트 루트 .env에 OPENAI_API_KEY가 필요합니다."
MODEL = "gpt-5.4-mini"
client = OpenAI(timeout=45.0, max_retries=0)
calls: list[dict[str, float | int | str]] = []
print("모델:", MODEL, "| API 키 존재: 예")"""

SYNC_HELPER = """def call_json(instructions: str, prompt: str, limit: int = 240) -> dict:
    started = time.perf_counter()
    response = client.responses.create(
        model=MODEL,
        instructions=instructions + " 반드시 유효한 JSON 객체만 반환하세요.",
        input="JSON 요청\\n" + prompt,
        max_output_tokens=limit,
        reasoning={"effort": "none"},
        text={"format": {"type": "json_object"}},
    )
    elapsed = time.perf_counter() - started
    usage = response.usage
    calls.append({"latency_s": elapsed, "input": usage.input_tokens,
                  "output": usage.output_tokens})
    return json.loads(response.output_text)

def call_answer(instructions: str, prompt: str, limit: int = 400) -> dict:
    started = time.perf_counter()
    response = client.responses.create(
        model=MODEL, instructions=instructions, input=prompt,
        max_output_tokens=limit, reasoning={"effort": "none"},
        text={"format": {"type": "json_schema", "name": "answer_payload",
              "schema": {"type": "object", "properties": {"answer": {"type": "string"}},
              "required": ["answer"], "additionalProperties": False}, "strict": True}},
    )
    calls.append({"latency_s": time.perf_counter() - started,
                  "input": response.usage.input_tokens, "output": response.usage.output_tokens})
    data = json.loads(response.output_text)
    if not isinstance(data.get("answer"), str) or not data["answer"].strip():
        raise ValueError("응답의 answer가 비어 있습니다.")
    return data

def cost_usd(records: list[dict]) -> float:
    inputs = sum(int(row["input"]) for row in records)
    outputs = sum(int(row["output"]) for row in records)
    return inputs * 0.75 / 1_000_000 + outputs * 4.50 / 1_000_000

def score_of(data: dict) -> int:
    value = data.get("score")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("평가 응답의 score는 숫자여야 합니다.")
    if not 0 <= value <= 100:
        raise ValueError("평가 응답의 score는 0~100이어야 합니다.")
    return int(value)

"""

ASYNC_SETUP = """import asyncio
import json
import os
import re
import time
from collections import Counter
from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI

load_dotenv(find_dotenv(usecwd=True))
assert os.getenv("OPENAI_API_KEY"), "프로젝트 루트 .env에 OPENAI_API_KEY가 필요합니다."
MODEL = "gpt-5.4-mini"
client = AsyncOpenAI(timeout=45.0, max_retries=0)
calls: list[dict[str, float | int | str]] = []
print("모델:", MODEL, "| API 키 존재: 예")"""

ASYNC_HELPER = """async def call_json(instructions: str, prompt: str, limit: int = 220) -> dict:
    started = time.perf_counter()
    response = await client.responses.create(
        model=MODEL,
        instructions=instructions + " 반드시 유효한 JSON 객체만 반환하세요.",
        input="JSON 요청\\n" + prompt,
        max_output_tokens=limit,
        reasoning={"effort": "none"},
        text={"format": {"type": "json_object"}},
    )
    calls.append({"latency_s": time.perf_counter() - started,
                  "input": response.usage.input_tokens,
                  "output": response.usage.output_tokens})
    return json.loads(response.output_text)

async def call_answer(instructions: str, prompt: str, limit: int = 400) -> dict:
    started = time.perf_counter()
    response = await client.responses.create(
        model=MODEL, instructions=instructions, input=prompt,
        max_output_tokens=limit, reasoning={"effort": "none"},
        text={"format": {"type": "json_schema", "name": "answer_payload",
              "schema": {"type": "object", "properties": {"answer": {"type": "string"}},
              "required": ["answer"], "additionalProperties": False}, "strict": True}},
    )
    calls.append({"latency_s": time.perf_counter() - started,
                  "input": response.usage.input_tokens, "output": response.usage.output_tokens})
    data = json.loads(response.output_text)
    if not isinstance(data.get("answer"), str) or not data["answer"].strip():
        raise ValueError("응답의 answer가 비어 있습니다.")
    return data

def cost_usd(records: list[dict]) -> float:
    return (sum(int(r["input"]) for r in records) * 0.75
            + sum(int(r["output"]) for r in records) * 4.50) / 1_000_000

def score_of(data: dict) -> int:
    value = data.get("score")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("평가 응답의 score는 숫자여야 합니다.")
    if not 0 <= value <= 100:
        raise ValueError("평가 응답의 score는 0~100이어야 합니다.")
    return int(value)

"""


def notebook_01() -> dict:
    cells = [
        markdown("# 게이트가 있는 프롬프트 체이닝\n\n첫 출력이 다음 호출에 들어가기 전에 필요한 항목을 갖췄는지 검사합니다."),
        markdown("## 실행 환경과 비용 상한\n\n최대 3회, 호출당 출력 260토큰으로 제한합니다. 계획 비용은 0.0081달러 미만입니다."),
        code(INSTALL), markdown(SYNC_SETUP_NOTE), code(SYNC_SETUP), *helper_cells(SYNC_HELPER),
        markdown("## 기본 실행: 게이트의 통과 조건 확인"),
        code("""def outline_gate(data: dict) -> tuple[bool, list[str]]:
    required = {"title", "audience", "steps"}
    missing = sorted(required - data.keys())
    if not isinstance(data.get("steps"), list) or len(data.get("steps", [])) < 3:
        missing.append("steps(3개 이상)")
    return not missing, missing

sample = {"title": "비밀번호 재설정", "audience": "로그인 사용자",
          "steps": ["이메일 입력", "코드 확인", "새 비밀번호 저장"]}
print("완전한 중간 결과:", outline_gate(sample))
assert outline_gate(sample) == (True, [])"""),
        markdown("## Before: 불완전한 중간 결과에서 중단", "before"),
        code("""

before = call_json("한글 안내문 기획자입니다.",
                   "비밀번호 재설정 안내의 title만 JSON으로 작성하세요.", 120)
passed, reasons = outline_gate(before)
print("중간 출력:", before)
print("게이트 통과:", passed, "| 부족한 항목:", reasons)
print("다음 호출 수:", 0 if not passed else 1)
assert not passed and reasons""", "before"),
        markdown("## After: 검사한 출력만 다음 프롬프트에 전달", "after"),
        code("""outline = call_json(
    "고객 지원 안내문 기획자입니다.",
    "비밀번호 재설정 안내를 title, audience, steps 3개인 JSON으로 작성하세요.", 180)
passed, reasons = outline_gate(outline)
if not passed:
    final = {"status": "stopped", "reasons": reasons}
else:
    final = call_answer(
        "초보 사용자를 위한 고객 지원 작성자입니다.",
        f"검사된 기획을 4문장 안내문으로 작성하세요. JSON answer로 반환: {outline}", 260)
print("게이트 통과:", passed)
print("최종 결과:", final)
print("누적 성공 응답:", len(calls), "| 사용량 기준 추정 비용($):", round(cost_usd(calls), 6))
assert passed and final["answer"].strip()""", "after"),
    ]
    return finish(cells, "paired")


def notebook_02() -> dict:
    cells = [
        markdown("# 실패를 처리하는 라우팅\n\n분류값을 허용 목록과 신뢰도 기준으로 검사한 뒤 전문 프롬프트로 분기합니다."),
        markdown("## 실행 환경과 비용 상한\n\n최대 4회, 호출당 출력 220토큰으로 제한합니다. 계획 비용은 0.0100달러 미만입니다."),
        code(INSTALL), markdown(SYNC_SETUP_NOTE), code(SYNC_SETUP), *helper_cells(SYNC_HELPER),
        markdown("## 분류 결과를 검사하는 라우터"),
        code("""ALLOWED = {"billing", "account", "technical"}

def route(decision: dict) -> tuple[str | None, str]:
    category = decision.get("category")
    confidence = float(decision.get("confidence", 0))
    if category not in ALLOWED:
        return None, "허용 목록에 없는 분류"
    if confidence < 0.75:
        return None, "신뢰도 기준 미달"
    return str(category), "전문 경로 사용"

classifier = "billing, account, technical 중 하나로 분류합니다. 혼합 질문은 unknown입니다. category와 confidence를 반환합니다."
valid = call_json(classifier, "카드에서 같은 요금이 두 번 결제됐어요.", 120)
invalid = call_json(classifier, "로그인도 안 되고 카드 청구도 이상해요.", 120)
print("단일 의도:", valid, "->", route(valid))
print("혼합 의도:", invalid, "->", route(invalid))"""),
        markdown("## Before: 분류값을 그대로 사전 키로 사용", "before"),
        code("""prompts = {"billing": "결제 지원 담당자", "account": "계정 지원 담당자",
           "technical": "기술 지원 담당자"}
bad_key = invalid.get("category")
print("분류값:", bad_key)
print("Before 결과:", "KeyError 위험" if bad_key not in prompts else prompts[bad_key])""", "before"),
        markdown("## After: 거절하지 않고 필요한 구분을 요청", "after"),
        code("""def answer_ticket(question: str, decision: dict) -> dict:
    category, reason = route(decision)
    if category is None:
        return {"status": "needs_clarification", "reason": reason,
                "answer": "계정 로그인과 결제 중 먼저 확인할 문제를 골라 주세요."}
    return call_json(prompts[category],
                     f"질문에 2문장으로 답하세요. JSON answer: {question}", 220)

good_answer = answer_ticket("카드에서 같은 요금이 두 번 결제됐어요.", valid)
safe_answer = answer_ticket("로그인도 안 되고 카드 청구도 이상해요.", invalid)
print("전문 경로:", good_answer)
print("안전 처리:", safe_answer)
print("누적 성공 응답:", len(calls), "| 사용량 기준 추정 비용($):", round(cost_usd(calls), 6))""", "after"),
    ]
    return finish(cells, "paired")


def notebook_03() -> dict:
    cells = [
        markdown("# 병렬 섹셔닝과 투표\n\n독립적인 섹션과 평가 호출을 `asyncio.gather`로 함께 기다립니다."),
        markdown("## 실행 환경과 비용 상한\n\n최대 8회, 호출당 출력 220토큰으로 제한합니다. 계획 비용은 0.0199달러 미만입니다."),
        code(INSTALL), markdown(ASYNC_SETUP_NOTE), code(ASYNC_SETUP), *helper_cells(ASYNC_HELPER),
        markdown("## 섹셔닝: 서로 의존하지 않는 세 부분을 병렬 작성"),
        code("""brief = "2026년 10월 15일부터 사내 2단계 인증을 적용합니다. 대상은 전 직원입니다."
sections = [
    ("목적", "도입 목적을 2문장으로"),
    ("절차", "등록 절차를 번호 3개로"),
    ("지원", "주의점과 문의 방법을 2문장으로"),
]

async def write_section(name: str, request: str) -> dict:
    prompt = f"공통 사실: {brief}\\n부분: {name}\\n요청: {request}"
    result = await call_json("사내 안내문 작성자입니다. name과 text를 반환합니다.", prompt)
    text = result.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"{name} 섹션의 text가 비어 있습니다.")
    return {"name": name, "text": text.strip()}

started = time.perf_counter()
parts = await asyncio.gather(*(write_section(*item) for item in sections))
wall = time.perf_counter() - started
print("입력 순서대로 반환:", [part["name"] for part in parts])
print("병렬 벽시계 시간(초):", round(wall, 3))
print("개별 지연 합(초):", round(sum(float(r["latency_s"]) for r in calls), 3))"""),
        markdown("## 투표: 후보와 평가자를 병렬 실행"),
        code("""candidate_prompts = ["정중하고 자세한 안내", "짧고 행동 중심인 안내"]
candidates = await asyncio.gather(*[
    call_answer("사내 안내문 작성자입니다.",
                f"{brief} {style}를 4문장으로 작성하세요.", 200)
    for style in candidate_prompts
])

async def vote(judge: str) -> dict:
    prompt = f"A={candidates[0]['answer']}\\nB={candidates[1]['answer']}"
    return await call_json(
        f"{judge} 기준 평가자입니다. winner는 A, B, tie, refuse 중 하나입니다.",
        prompt + "\\n사실 정확성과 실행 가능성을 평가하세요.", 120)

votes = await asyncio.gather(*(vote(name) for name in ["인사", "보안", "신입 직원"]))
valid_votes = [v.get("winner") for v in votes if v.get("winner") in {"A", "B"}]
counts = Counter(valid_votes)
if not valid_votes:
    winner = "undecided"
elif counts.get("A", 0) == counts.get("B", 0):
    winner = "tie"
else:
    winner = counts.most_common(1)[0][0]
print("원표:", votes)
print("유효표:", dict(counts), "| 결과:", winner)
print("승자 집계 제외 표:", len(votes) - len(valid_votes))"""),
        markdown("## 실험 결과 해석\n\n`gather`는 입력 순서대로 결과 목록을 반환하지만 각 요청의 완료 시각까지 같게 만들지는 않습니다. 벽시계 시간은 네트워크 상태와 서비스 부하에 따라 달라집니다. 투표가 동점이거나 평가자가 거절하면 결과를 그대로 기록하며 임의로 승자를 만들지 않습니다."),
        code("""print("총 호출:", len(calls))
print("입력 토큰:", sum(int(r["input"]) for r in calls))
print("출력 토큰:", sum(int(r["output"]) for r in calls))
print("사용량 기준 추정 비용($):", round(cost_usd(calls), 6))"""),
    ]
    return finish(cells, "experiment")


def notebook_04() -> dict:
    cells = [
        markdown("# 동적 오케스트레이터와 워커\n\n중앙 모델이 입력을 읽고 필요한 하위 작업의 개수와 지시를 정합니다."),
        markdown("## 실행 환경과 비용 상한\n\n오케스트레이터 1회, 워커 최대 4회, 종합 1회로 제한합니다. 계획 비용은 0.0183달러 미만입니다."),
        code(INSTALL), markdown(ASYNC_SETUP_NOTE), code(ASYNC_SETUP), *helper_cells(ASYNC_HELPER),
        markdown("## 오케스트레이터가 입력에 맞춰 작업 분해"),
        code("""task = "전 직원에게 2단계 인증 도입을 설명하고, 등록 절차와 지원 방법을 포함한 안내문을 작성하세요."
plan = await call_json(
    "작업 오케스트레이터입니다. 입력에 필요한 하위 작업을 동적으로 설계합니다.",
    task + "\\nJSON tasks 배열에 2~4개의 id, instruction을 반환하세요. instruction은 각각 40자 이내입니다.", 600)
raw_tasks = plan.get("tasks", [])
tasks = [item for item in raw_tasks if isinstance(item, dict)
         and item.get("id") and item.get("instruction")][:4]
if len(tasks) < 2:
    raise ValueError("오케스트레이터가 유효한 하위 작업을 2개 이상 만들지 못했습니다.")
print("동적 작업 수:", len(tasks))
for item in tasks:
    print(item["id"], "-", item["instruction"])"""),
        markdown("## 계획에 생긴 작업 수만큼 워커 실행"),
        code("""async def run_worker(item: dict) -> dict:
    result = await call_answer(
        "독립 워커입니다. 맡은 범위만 조사하거나 작성합니다.",
        f"전체 과제: {task}\\n담당: {item['instruction']}\\nJSON result를 120자 이내로 반환하세요.", 400)
    return {"id": item["id"], "result": result["answer"]}

worker_results = await asyncio.gather(*(run_worker(item) for item in tasks))
print("실행한 워커:", [item["id"] for item in worker_results])
print("고정 목록 사용:", False)"""),
        markdown("## 오케스트레이터가 워커 결과를 종합"),
        code("""synthesis = await call_answer(
    "편집 오케스트레이터입니다. 중복을 줄이고 사실을 보존합니다.",
    f"과제: {task}\\n워커 결과: {worker_results}\\nJSON answer 하나만 300자 이내로 작성하세요.", 700)
final_answer = synthesis["answer"]
print("최종 결과:", final_answer)
print("종합 응답 상태: ok")
print("호출 수:", len(calls), "= 계획 1 + 워커", len(tasks), "+ 종합 1")
print("사용량 기준 추정 비용($):", round(cost_usd(calls), 6))
assert final_answer"""),
        markdown("## 실험 결과 해석\n\n작업 목록은 코드에 고정하지 않았습니다. 같은 입력에서도 모델이 2~4개 범위에서 다른 분해를 만들 수 있습니다. 유효한 작업이 2개보다 적으면 조용히 기본 목록으로 바꾸지 않고 오류로 중단합니다. 그래야 오케스트레이터의 실제 실패를 관찰할 수 있습니다."),
    ]
    return finish(cells, "experiment")


def notebook_05() -> dict:
    cells = [
        markdown("# 생성자-평가자와 정지 조건\n\n생성자와 평가자를 분리하고 세 조건 가운데 하나가 충족되면 반복을 멈춥니다."),
        markdown("## 실행 환경과 비용 상한\n\n최대 3회 반복, 회당 생성·평가 2회, 마지막 보고 1회 이하입니다. 계획 비용은 0.0217달러 미만입니다."),
        code(INSTALL), markdown(SYNC_SETUP_NOTE), code(SYNC_SETUP), *helper_cells(SYNC_HELPER),
        markdown("## 품질 기준과 반복 상한"),
        code("""TASK = "2단계 인증 도입 안내를 120~180자로 작성하세요. 2026년 10월 15일, 전 직원, help@company.test를 포함하고 등록 절차를 1)·2)·3)으로 표시합니다."
MAX_ITERATIONS = 3
QUALITY_THRESHOLD = 85
MIN_IMPROVEMENT = 3

print({"최대 반복": MAX_ITERATIONS, "품질 임계": QUALITY_THRESHOLD,
       "최소 개선 폭": MIN_IMPROVEMENT})"""),
        markdown("## 생성과 평가를 번갈아 실행"),
        code("""history: list[dict] = []
draft = ""
feedback = "첫 초안을 작성하세요."
previous_score: int | None = None
stop_reason = "max_iterations"

for iteration in range(1, MAX_ITERATIONS + 1):
    generated = call_answer("사내 안내문 생성자입니다.",
                          f"과제: {TASK}\\n이전 피드백: {feedback}\\nJSON answer", 260)
    draft = generated["answer"]
    judged = call_json("독립 평가자입니다. 요구 충족도를 0~100으로 채점합니다.",
                       f"과제: {TASK}\\n초안: {draft}\\nJSON score, feedback", 180)
    score = score_of(judged)
    improvement = None if previous_score is None else score - previous_score
    history.append({"iteration": iteration, "score": score, "improvement": improvement})
    feedback = str(judged.get("feedback", ""))
    if score >= QUALITY_THRESHOLD:
        stop_reason = "quality_threshold"; break
    if improvement is not None and improvement < MIN_IMPROVEMENT:
        stop_reason = "min_improvement"; break
    previous_score = score"""),
        markdown("## 실험 결과와 중단 이유"),
        code("""print("반복 기록:", history)
print("중단 이유:", stop_reason)
print("최종 초안:", draft)
print("성공 응답 수:", len(calls), "| 사용량 기준 추정 비용($):", round(cost_usd(calls), 6))
assert len(history) <= MAX_ITERATIONS
assert stop_reason in {"quality_threshold", "min_improvement", "max_iterations"}"""),
        markdown("## 실험 결과 해석\n\n품질 임계값에 도달하면 남은 반복을 사용하지 않습니다. 점수가 오르더라도 개선 폭이 3점보다 작으면 추가 비용의 효과가 작다고 보고 중단합니다. 두 조건에 걸리지 않으면 최대 3회에서 끝납니다. 평가 점수는 이 과제와 이 평가 프롬프트 안에서만 의미가 있으며 사람 검토를 대신하지 않습니다."),
    ]
    return finish(cells, "experiment")


def notebook_06() -> dict:
    cells = [
        markdown("# 같은 과제로 다섯 패턴 비교\n\n같은 입력·모델·출력 상한·채점 기준으로 다섯 패턴을 실제 호출해 비교합니다."),
        markdown("## 실행 환경과 비용 상한\n\n최대 18회, 호출당 출력 500토큰으로 제한합니다. 계획 비용은 0.0600달러 미만입니다."),
        code(INSTALL), markdown(ASYNC_SETUP_NOTE), code(ASYNC_SETUP), *helper_cells(ASYNC_HELPER),
        markdown("## 같은 과제와 공개 채점 기준"),
        code("""TASK = "2단계 인증 도입 안내를 120~180자로 작성하세요. 2026년 10월 15일, 전 직원, help@company.test를 포함하고 등록 절차를 1)·2)·3)으로 표시합니다."

def grade(answer: str) -> dict[str, int]:
    checks = {
        "date": int("2026년 10월 15일" in answer),
        "audience": int("전 직원" in answer),
        "three_steps": int(bool(re.search(r"1[.)].+2[.)].+3[.)]", answer, re.S))),
        "contact": int("help@company.test" in answer),
        "length": int(120 <= len(answer) <= 180),
    }
    return {**checks, "score": sum(checks.values())}

def answer_of(data: dict) -> str:
    answer = data.get("answer") if isinstance(data, dict) else None
    return answer.strip() if isinstance(answer, str) else ""

results: dict[str, dict] = {}
print("과제:", TASK)
print("채점: 날짜·대상·3단계·문의처·120~180자, 각 1점")"""),
        markdown("## 패턴 1~2: 체이닝과 라우팅"),
        code("""start = len(calls); began = time.perf_counter()
outline = await call_json("안내문 기획자입니다.", TASK + " JSON plan", 250)
chain = await call_answer("안내문 작성자입니다.", f"과제: {TASK}\\n기획: {outline}", 500)
results["chaining"] = {"answer": answer_of(chain), "from": start,
                       "latency": time.perf_counter() - began}

start = len(calls); began = time.perf_counter()
route = await call_json("문서를 security, hr, finance 중 분류합니다. JSON category.", TASK, 150)
category = route.get("category")
if category not in {"security", "hr", "finance"}:
    routed = {"answer": "", "status": "invalid_category"}
else:
    routed = await call_answer(f"{category} 전문 작성자입니다.", TASK, 500)
results["routing"] = {"answer": answer_of(routed), "from": start,
                     "latency": time.perf_counter() - began}
print("체이닝·라우팅 완료")"""),
        markdown("## 패턴 3: 병렬 섹셔닝"),
        code("""start = len(calls); began = time.perf_counter()
section_jobs = [
    call_answer("안내문 부분 작성자입니다.", f"{TASK}\\n담당: 핵심 사실", 220),
    call_answer("안내문 부분 작성자입니다.", f"{TASK}\\n담당: 등록 3단계", 220),
    call_answer("안내문 부분 작성자입니다.", f"{TASK}\\n담당: 문의처와 길이", 220),
]
sections = await asyncio.gather(*section_jobs)
assert all(answer_of(item) for item in sections)
merged = " ".join(answer_of(item) for item in sections)
parallel = await call_answer("편집자입니다.", f"과제: {TASK}\\n부분: {merged}", 500)
results["parallel"] = {"answer": answer_of(parallel), "from": start,
                       "latency": time.perf_counter() - began}
print("병렬 섹셔닝 완료")"""),
        markdown("## 패턴 4: 동적 오케스트레이터-워커"),
        code("""start = len(calls); began = time.perf_counter()
plan = await call_json("오케스트레이터입니다.",
                       TASK + " 필요한 작업 2개만 동적으로 정해 JSON tasks(id,instruction).", 500)
tasks = [x for x in plan.get("tasks", []) if x.get("instruction")][:2]
worker_jobs = [call_answer("독립 워커입니다.",
                         f"과제: {TASK}\\n담당: {item['instruction']}", 300)
               for item in tasks]
worker_outputs = await asyncio.gather(*worker_jobs) if worker_jobs else []
orchestrated = await call_answer("종합 작성자입니다.",
    f"과제: {TASK}\\n결과: {worker_outputs}", 500)
results["orchestrator_worker"] = {"answer": answer_of(orchestrated), "from": start,
                                  "latency": time.perf_counter() - began}
print("동적 작업 수:", len(tasks))"""),
        markdown("## 패턴 5: 생성자-평가자"),
        code("""start = len(calls); began = time.perf_counter()
draft = ""; feedback = "첫 초안"; evaluations = []
for iteration in range(2):
    made = await call_answer("생성자입니다.", f"{TASK}\\n피드백: {feedback}", 500)
    draft = answer_of(made)
    judged = await call_json("평가자입니다. JSON score 0~100, feedback.",
                             f"과제: {TASK}\\n답: {draft}", 200)
    score = score_of(judged)
    evaluations.append(score)
    feedback = str(judged.get("feedback", ""))
    if score >= 85:
        break
results["generator_evaluator"] = {"answer": draft, "from": start,
                                   "latency": time.perf_counter() - began}
print("평가 점수 원자료:", evaluations)"""),
        markdown("## 호출 수·토큰·지연·품질 비교"),
        code("""rows = []
ordered = list(results)
for index, name in enumerate(ordered):
    begin = int(results[name]["from"])
    end = int(results[ordered[index + 1]]["from"]) if index + 1 < len(ordered) else len(calls)
    records = calls[begin:end]
    answer = str(results[name]["answer"])
    rows.append({"pattern": name, "calls": len(records),
                 "tokens": sum(int(r["input"]) + int(r["output"]) for r in records),
                 "latency_s": round(float(results[name]["latency"]), 3),
                 "quality": grade(answer)["score"], "status": "ok" if answer else "no_answer"})

print("pattern | calls | tokens | latency_s | quality/5 | status")
for row in rows:
    print(" | ".join(str(row[key]) for key in
          ["pattern", "calls", "tokens", "latency_s", "quality", "status"]))
best = max(row["quality"] for row in rows)
print("최고 품질 동점 포함:", [row["pattern"] for row in rows if row["quality"] == best])
print("전체 사용량 기준 추정 비용($):", round(cost_usd(calls), 6))"""),
        markdown("## 실험 결과 해석\n\n품질은 공개한 다섯 항목을 충족했는지만 셉니다. 문장 미감이나 조직 정책의 정확성을 평가하지 않습니다. 지연은 이 한 번의 실행에서 측정한 벽시계 시간이라 일반적인 속도 순위가 아닙니다. 최고 점수가 같으면 동점을 유지하며, 빈 답이나 거절은 `no_answer`로 기록합니다. 따라서 화려한 패턴이 언제나 더 높은 점수를 낸다고 결론 내리지 않습니다."),
    ]
    return finish(cells, "experiment")


def finish(cells: list[dict], lesson_format: str) -> dict:
    for index, cell in enumerate(cells, 1):
        cell["id"] = f"cell-{index:02d}"
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "lesson_format": lesson_format,
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


NOTEBOOK_BUILDERS = {
    "01-게이트가-있는-프롬프트-체이닝": notebook_01,
    "02-실패를-처리하는-라우팅": notebook_02,
    "03-병렬-섹셔닝과-투표": notebook_03,
    "04-동적-오케스트레이터와-워커": notebook_04,
    "05-생성자-평가자와-정지-조건": notebook_05,
    "06-같은-과제로-다섯-패턴-비교": notebook_06,
}


def main() -> None:
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    for slug, builder in NOTEBOOK_BUILDERS.items():
        path = NOTEBOOKS / f"{slug}.ipynb"
        path.write_text(json.dumps(builder(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("wrote", path.name)


if __name__ == "__main__":
    main()
