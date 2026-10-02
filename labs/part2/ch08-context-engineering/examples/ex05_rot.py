"""05절 — 길이와 근거 위치만 바꾸어 context rot을 반복 측정한다."""

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

INSTRUCTIONS = "문서에서 답을 찾아 한 문장으로 답하고 근거 출처를 [E01 p.2] 형식으로 표시하세요."
QUESTION = "미르시립도서관의 정기 휴관일은 언제인가요?"
EVIDENCE = "[E01 p.2] 매주 월요일은 정기 휴관일입니다. 공휴일이 월요일이면 다음 날 화요일에도 휴관합니다."
TARGET_TOKENS = {"short": 1200, "medium": 4800, "long": 12000}


def filler(target_tokens: int) -> str:
    sentence = (
        "[합성 방해 문서 D] 푸른별 기록관은 자료 상자 번호와 습도 점검표를 매일 대조합니다. "
        "이 문서는 미르시립도서관의 운영 규정과 관계가 없습니다.\n"
    )
    count = max(1, target_tokens // max(estimate_tokens(sentence), 1))
    return sentence * count


def position_evidence(noise: str, position: str) -> str:
    midpoint = len(noise) // 2
    if position == "start":
        return EVIDENCE + "\n" + noise
    if position == "middle":
        return noise[:midpoint] + "\n" + EVIDENCE + "\n" + noise[midpoint:]
    if position == "end":
        return noise + "\n" + EVIDENCE
    raise ValueError(f"지원하지 않는 위치: {position}")


def evaluate(text: str) -> dict[str, bool]:
    return {"mentions_monday": "월요일" in text, "has_source": "E01 p.2" in text}


def main(repetitions: int = 3) -> None:
    run_path = RUNS_DIR / "ex05_rot.jsonl"
    if run_path.exists():
        run_path.unlink()
    cases = []
    for length, token_target in TARGET_TOKENS.items():
        noise = filler(token_target)
        for position in ("start", "middle", "end"):
            context = position_evidence(noise, position)
            cases.append((length, position, context))
    expected_cost = sum(
        estimate_cost_usd(estimate_tokens(INSTRUCTIONS + context + QUESTION), 256) * repetitions
        for _, _, context in cases
    )
    lines = [
        f"모델·과제·근거 고정: {DEFAULT_MODEL} / 정기 휴관일 / E01.pdf p.2",
        f"호출 전 예상 최대 비용: ${expected_cost:.4f} ({len(cases) * repetitions}회)",
        "감소가 나타나지 않아도 실측값을 그대로 기록합니다.",
    ]
    aggregates: dict[tuple[str, str], list[bool]] = {}
    invalid: dict[tuple[str, str], int] = {}
    append_jsonl(
        run_path,
        preflight_record("context_rot", len(cases) * repetitions, expected_cost),
    )
    total_cost = 0.0
    for length, position, context in cases:
        values = aggregates.setdefault((length, position), [])
        invalid.setdefault((length, position), 0)
        for repetition in range(1, repetitions + 1):
            result = call_model(
                INSTRUCTIONS,
                f"[문서]\n{context}\n\n[질문]\n{QUESTION}",
                max_output_tokens=256,
            )
            evaluation = evaluate(result.response)
            evaluation_valid = result.status == "completed"
            if evaluation_valid:
                values.append(evaluation["mentions_monday"] and evaluation["has_source"])
            else:
                invalid[(length, position)] += 1
            total_cost += result.cost_usd
            append_jsonl(
                run_path,
                experiment_record(
                    experiment="context_rot",
                    condition=f"{length}:{position}",
                    repetition=repetition,
                    document_ids=["E01", "SYNTH-DISTRACTOR"],
                    sources=["E01.pdf p.2", "교재용 합성 fixture"],
                    result=result,
                    evaluation_raw={**evaluation, "evaluation_valid": evaluation_valid},
                    extra={
                        "length": length,
                        "evidence_position": position,
                        "context_tokens_local_estimate": estimate_tokens(context),
                        "instructions_text": INSTRUCTIONS,
                        "context_text": context,
                        "question_text": QUESTION,
                    },
                ),
            )
    for length in TARGET_TOKENS:
        for position in ("start", "middle", "end"):
            values = aggregates[(length, position)]
            lines.append(
                f"{length:6} {position:6}: 정답+출처 {sum(values)}/{len(values)}회, "
                f"실험 무효 {invalid[(length, position)]}회"
            )
    lines.extend([f"API 실측 비용: ${total_cost:.6f}", f"상세 로그: {run_path.relative_to(run_path.parent.parent)}"])
    print_and_capture(lines, Path(__file__).with_suffix(".stdout.txt"))


if __name__ == "__main__":
    main()
