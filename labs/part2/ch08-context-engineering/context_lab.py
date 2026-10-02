"""Ch 8 컨텍스트 엔지니어링 실험의 공통 함수."""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import tiktoken
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_ROOT = Path(__file__).resolve().parents[2] / "data" / "rag-corpus"
E01_PDF = DATA_ROOT / "pdf" / "easy" / "E01.pdf"
RUNS_DIR = ROOT / "runs"
DEFAULT_MODEL = "gpt-5.4-mini"

# 2026-09-07 OpenAI 공식 가격 페이지 확인. Standard, USD / 1M tokens.
MODEL_PRICES = {DEFAULT_MODEL: {"input": 0.75, "cached_input": 0.075, "output": 4.50}}


@dataclass(frozen=True)
class ContextBudget:
    total_limit: int
    output_reserve: int
    safety_margin: int
    instruction_tokens: int
    question_tokens: int
    evidence_budget: int


@dataclass(frozen=True)
class CallResult:
    response: str
    input_tokens: int
    cached_input_tokens: int
    output_tokens: int
    reasoning_tokens: int
    latency_seconds: float
    cost_usd: float
    status: str
    incomplete_reason: str | None
    resolved_model: str


def load_environment() -> None:
    """프로젝트 루트의 .env를 읽되 값을 출력하지 않는다."""
    load_dotenv(PROJECT_ROOT / ".env")


def require_api_key() -> None:
    load_environment()
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY가 프로젝트 루트 .env에 없습니다")


def estimate_tokens(text: str, model: str = DEFAULT_MODEL) -> int:
    """API 호출 전 로컬 토크나이저로 입력 길이를 추정한다."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("o200k_base")
    return len(encoding.encode(text))


def make_budget(
    total_limit: int,
    output_reserve: int,
    safety_margin: int,
    instructions: str,
    question: str,
) -> ContextBudget:
    instruction_tokens = estimate_tokens(instructions)
    question_tokens = estimate_tokens(question)
    evidence_budget = (
        total_limit
        - output_reserve
        - safety_margin
        - instruction_tokens
        - question_tokens
    )
    if evidence_budget < 0:
        raise ValueError("출력 예약·여유·지시·질문이 전체 한도를 초과했습니다")
    return ContextBudget(
        total_limit=total_limit,
        output_reserve=output_reserve,
        safety_margin=safety_margin,
        instruction_tokens=instruction_tokens,
        question_tokens=question_tokens,
        evidence_budget=evidence_budget,
    )


def ensure_input_fits(budget: ContextBudget, estimated_input_tokens: int) -> None:
    """출력 예약과 여유를 제외한 입력 상한을 넘으면 호출 전에 중단한다."""
    input_limit = budget.total_limit - budget.output_reserve - budget.safety_margin
    if estimated_input_tokens > input_limit:
        raise ValueError(
            f"로컬 추정 입력 {estimated_input_tokens}토큰이 입력 상한 {input_limit}토큰을 초과했습니다"
        )


def estimate_cost_usd(
    input_tokens: int,
    output_tokens: int,
    model: str = DEFAULT_MODEL,
    cached_input_tokens: int = 0,
) -> float:
    price = MODEL_PRICES[model]
    uncached_input_tokens = max(0, input_tokens - cached_input_tokens)
    return (
        uncached_input_tokens * price["input"]
        + cached_input_tokens * price["cached_input"]
        + output_tokens * price["output"]
    ) / 1_000_000


def call_model(
    instructions: str,
    prompt: str,
    *,
    model: str = DEFAULT_MODEL,
    max_output_tokens: int = 256,
) -> CallResult:
    """Responses API를 직접 호출하고 실측 usage·지연·비용을 반환한다."""
    require_api_key()
    client = OpenAI()
    started = time.perf_counter()
    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=prompt,
        max_output_tokens=max_output_tokens,
        reasoning={"effort": "none"},
    )
    elapsed = time.perf_counter() - started
    usage = response.usage
    if usage is None:
        raise RuntimeError("Responses API가 usage를 반환하지 않아 실측값을 기록할 수 없습니다")
    input_tokens = usage.input_tokens
    output_tokens = usage.output_tokens
    cached_input_tokens = usage.input_tokens_details.cached_tokens
    reasoning_tokens = usage.output_tokens_details.reasoning_tokens
    incomplete_reason = response.incomplete_details.reason if response.incomplete_details else None
    return CallResult(
        response=response.output_text,
        input_tokens=input_tokens,
        cached_input_tokens=cached_input_tokens,
        output_tokens=output_tokens,
        reasoning_tokens=reasoning_tokens,
        latency_seconds=round(elapsed, 3),
        cost_usd=round(
            estimate_cost_usd(input_tokens, output_tokens, model, cached_input_tokens), 8
        ),
        status=response.status,
        incomplete_reason=incomplete_reason,
        resolved_model=response.model,
    )


def extract_e01_pages() -> list[dict[str, Any]]:
    """E01 PDF의 텍스트를 페이지별 출처 메타데이터와 함께 읽는다."""
    reader = PdfReader(str(E01_PDF))
    return [
        {"doc_id": "E01", "page": page_no, "text": page.extract_text() or ""}
        for page_no, page in enumerate(reader.pages, start=1)
    ]


def source_block(page: dict[str, Any]) -> str:
    return f"[문서 ID: {page['doc_id']} | 출처: E01.pdf p.{page['page']}]\n{page['text']}"


def save_memory(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_memory(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def select_documents(records: list[dict[str, Any]], selected_ids: list[str]) -> list[dict[str, Any]]:
    """학생이 공개된 규칙에 따라 고른 문서 ID만 반환한다.

    규칙은 ID의 입력 순서를 보존하고, 존재하지 않는 ID와 중복 ID는 제외하는 것이다.
    내용이나 정답 문자열은 선택에 사용하지 않는다.
    """
    by_id = {record["doc_id"]: record for record in records}
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for doc_id in selected_ids:
        if doc_id in by_id and doc_id not in seen:
            result.append(by_id[doc_id])
            seen.add(doc_id)
    return result


def compress_facts(records: list[dict[str, str]]) -> str:
    """출처·조건·예외 필드를 버리지 않는 수동 압축 형식."""
    lines = []
    for record in records:
        required = {"fact", "source", "condition", "exception"}
        missing = required - record.keys()
        if missing:
            raise ValueError(f"압축할 레코드에 필드가 없습니다: {sorted(missing)}")
        lines.append(
            f"- 사실: {record['fact']} | 조건: {record['condition']} | "
            f"예외: {record['exception']} | 출처: {record['source']}"
        )
    return "\n".join(lines)


def assemble_isolated_messages(instructions: str, evidence: str, question: str) -> dict[str, str]:
    """지시·근거·질문을 별도 필드로 조립한다. 이 구분은 보안 격리를 뜻하지 않는다."""
    return {
        "instructions": instructions,
        "input": f"[근거]\n{evidence}\n\n[질문]\n{question}",
    }


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def experiment_record(
    *,
    experiment: str,
    condition: str,
    repetition: int,
    document_ids: list[str],
    sources: list[str],
    result: CallResult,
    evaluation_raw: dict[str, Any],
    model: str = DEFAULT_MODEL,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    record = {
        "timestamp_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "experiment": experiment,
        "condition": condition,
        "repetition": repetition,
        "document_ids": document_ids,
        "sources": sources,
        "model": result.resolved_model,
        "requested_model": model,
        "response": result.response,
        "usage": {
            "input_tokens": result.input_tokens,
            "cached_input_tokens": result.cached_input_tokens,
            "output_tokens": result.output_tokens,
            "reasoning_tokens": result.reasoning_tokens,
        },
        "cost_usd": result.cost_usd,
        "latency_seconds": result.latency_seconds,
        "response_status": result.status,
        "incomplete_reason": result.incomplete_reason,
        "evaluation_raw": evaluation_raw,
    }
    if extra:
        record.update(extra)
    return record


def preflight_record(experiment: str, planned_calls: int, estimated_max_cost_usd: float) -> dict[str, Any]:
    """실제 호출보다 먼저 로그에 쓰는 비용 상한 레코드."""
    return {
        "record_type": "preflight",
        "timestamp_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "experiment": experiment,
        "model": DEFAULT_MODEL,
        "planned_calls": planned_calls,
        "estimated_max_cost_usd": round(estimated_max_cost_usd, 6),
        "pricing_assumption": "uncached Standard input; output reservation 256 tokens/call",
    }


def result_asdict(result: CallResult) -> dict[str, Any]:
    return asdict(result)


def print_and_capture(lines: list[str], output_path: Path) -> None:
    """실행 원문을 콘솔과 examples/*.stdout.txt에 똑같이 남긴다."""
    text = "\n".join(lines) + "\n"
    print(text, end="")
    output_path.write_text(text, encoding="utf-8")
