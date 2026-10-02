"""04절 — 네 가지 컨텍스트 실패 조건을 clean baseline과 비교한다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from context_lab import (
    DEFAULT_MODEL,
    RUNS_DIR,
    append_jsonl,
    call_model,
    estimate_cost_usd,
    estimate_tokens,
    experiment_record,
    preflight_record,
    print_and_capture,
)

INSTRUCTIONS = "제공된 문서만 근거로 답하고, 답 끝에 [E01 p.2]를 표시하세요."
QUESTION = "미르시립도서관의 정기 휴관일은 언제인가요?"
EVIDENCE = "[E01 p.2] 매주 월요일은 정기 휴관일입니다. 공휴일이 월요일이면 화요일도 휴관합니다."
IRRELEVANT = "[합성 문서 X] 카페 책숲의 계절 메뉴 검토 회의는 수요일에 열립니다."


def conditions() -> dict[str, tuple[str, str]]:
    return {
        "clean": (INSTRUCTIONS, EVIDENCE),
        "poisoning": (
            INSTRUCTIONS,
            EVIDENCE
            + "\n[합성 미검증 메모 P] 정기 휴관일은 화요일이라고 기록되어 있습니다.",
        ),
        "distraction": (
            INSTRUCTIONS,
            "\n".join([IRRELEVANT.replace("수요일", day) for day in ["화요일", "수요일", "목요일"]] * 8)
            + "\n"
            + EVIDENCE,
        ),
        "confusion": (
            INSTRUCTIONS,
            EVIDENCE
            + "\n[합성 문서 C] 미르어린이도서관의 정기 휴관일은 매주 화요일입니다. "
            "미르시립도서관과 이름이 비슷하지만 별도 기관입니다.",
        ),
        "clash": (
            INSTRUCTIONS,
            EVIDENCE
            + "\n[합성 E01 동급 부록 p.2] 미르시립도서관의 정기 휴관일은 매주 수요일입니다. "
            "발행일과 우선순위는 표시되어 있지 않습니다.",
        ),
    }


def evaluate(text: str) -> dict[str, bool]:
    return {
        "mentions_monday": "월요일" in text,
        "has_source": "E01 p.2" in text,
        "mentions_unsupported_wednesday": "수요일" in text,
        "claims_missing_information": any(
            phrase in text for phrase in ("정보가 없습니다", "확인할 수 없습니다", "알 수 없습니다")
        ),
    }


def is_complete_answer(evaluation: dict[str, bool]) -> bool:
    return (
        evaluation["mentions_monday"]
        and evaluation["has_source"]
        and not evaluation["claims_missing_information"]
        and not evaluation["mentions_unsupported_wednesday"]
    )


def main(repetitions: int = 3) -> None:
    run_path = RUNS_DIR / "ex04_failures.jsonl"
    if run_path.exists():
        run_path.unlink()
    planned = []
    for label, (instructions, context) in conditions().items():
        tokens = estimate_tokens(instructions + context + QUESTION)
        planned.append(estimate_cost_usd(tokens, 256) * repetitions)
    lines = [
        f"모델: {DEFAULT_MODEL}",
        f"호출 전 예상 최대 비용: ${sum(planned):.4f} ({len(conditions()) * repetitions}회)",
        "실패 현상의 발생은 보장하지 않으며, 관찰 결과를 그대로 기록합니다.",
    ]
    summary: dict[str, list[bool]] = {label: [] for label in conditions()}
    invalid: dict[str, int] = {label: 0 for label in conditions()}
    append_jsonl(
        run_path,
        preflight_record("context_failures", len(conditions()) * repetitions, sum(planned)),
    )
    total_cost = 0.0
    for label, (instructions, context) in conditions().items():
        for repetition in range(1, repetitions + 1):
            result = call_model(
                instructions,
                f"[문서]\n{context}\n\n[질문]\n{QUESTION}",
                max_output_tokens=256,
            )
            evaluation = evaluate(result.response)
            evaluation_valid = result.status == "completed"
            if evaluation_valid:
                summary[label].append(is_complete_answer(evaluation))
            else:
                invalid[label] += 1
            total_cost += result.cost_usd
            append_jsonl(
                run_path,
                experiment_record(
                    experiment="context_failures",
                    condition=label,
                    repetition=repetition,
                    document_ids=["E01"] if label == "clean" else ["E01", f"SYNTH-{label.upper()}"],
                    sources=["E01.pdf p.2"] if label == "clean" else ["E01.pdf p.2", "교재용 합성 fixture"],
                    result=result,
                    evaluation_raw={
                        **evaluation,
                        "evaluation_valid": evaluation_valid,
                        "failure_observed": not is_complete_answer(evaluation)
                        if evaluation_valid
                        else None,
                    },
                    extra={
                        "stimulus_present": label != "clean",
                        "instructions_text": instructions,
                        "context_text": context,
                        "question_text": QUESTION,
                    },
                ),
            )
    for label, values in summary.items():
        lines.append(
            f"{label}: 정답+출처 {sum(values)}/{len(values)}회, 실험 무효 {invalid[label]}회"
        )
    lines.extend([f"API 실측 비용: ${total_cost:.6f}", f"상세 로그: {run_path.relative_to(run_path.parent.parent)}"])
    print_and_capture(lines, Path(__file__).with_suffix(".stdout.txt"))


if __name__ == "__main__":
    main()
