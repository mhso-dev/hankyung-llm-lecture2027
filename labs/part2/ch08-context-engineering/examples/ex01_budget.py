"""01절 — 로컬 토큰 예산과 API 실측 usage를 구분한다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from context_lab import (
    DEFAULT_MODEL,
    RUNS_DIR,
    append_jsonl,
    call_model,
    ensure_input_fits,
    estimate_cost_usd,
    estimate_tokens,
    experiment_record,
    extract_e01_pages,
    make_budget,
    preflight_record,
    print_and_capture,
    source_block,
)

INSTRUCTIONS = "제공된 근거만 사용해 한 문장으로 답하고 [E01 p.2] 출처를 표시하세요."
QUESTION = "미르시립도서관의 정기 휴관일은 언제인가요?"


def main() -> None:
    budget = make_budget(4096, 256, 128, INSTRUCTIONS, QUESTION)
    evidence = source_block(extract_e01_pages()[1])
    if "매주 월요일은 정기 휴관일" not in evidence:
        raise RuntimeError("E01.pdf p.2에서 실습 근거를 확인하지 못했습니다")
    estimated_input = estimate_tokens(INSTRUCTIONS + "\n" + evidence + "\n" + QUESTION)
    ensure_input_fits(budget, estimated_input)
    estimated_cost = estimate_cost_usd(estimated_input, budget.output_reserve)
    run_path = RUNS_DIR / "ex01_budget.jsonl"
    if run_path.exists():
        run_path.unlink()
    append_jsonl(run_path, preflight_record("token_budget", 1, estimated_cost))
    result = call_model(
        INSTRUCTIONS, f"[근거]\n{evidence}\n\n[질문]\n{QUESTION}", max_output_tokens=256
    )
    append_jsonl(
        run_path,
        experiment_record(
            experiment="token_budget",
            condition="single_e01_page",
            repetition=1,
            document_ids=["E01"],
            sources=["E01.pdf p.2"],
            result=result,
            evaluation_raw={"response_completed": result.status == "completed"},
            extra={
                "instructions_text": INSTRUCTIONS,
                "context_text": evidence,
                "question_text": QUESTION,
                "local_input_tokens_estimate": estimated_input,
            },
        ),
    )
    lines = [
        f"모델: {DEFAULT_MODEL}",
        f"예산: 총 {budget.total_limit} / 출력 예약 {budget.output_reserve} / 여유 {budget.safety_margin}",
        f"지시 {budget.instruction_tokens} / 질문 {budget.question_tokens} / 근거 가용 {budget.evidence_budget}",
        f"호출 전 로컬 추정: 입력 {estimated_input}토큰, 최대 비용 ${estimated_cost:.6f}",
        (
            f"API 실측: 입력 {result.input_tokens}(캐시 {result.cached_input_tokens}) / "
            f"출력 {result.output_tokens}토큰, 비용 ${result.cost_usd:.6f}"
        ),
        f"응답 상태: {result.status}",
        f"API 응답 모델: {result.resolved_model}",
        f"답변: {result.response}",
    ]
    print_and_capture(lines, Path(__file__).with_suffix(".stdout.txt"))


if __name__ == "__main__":
    main()
