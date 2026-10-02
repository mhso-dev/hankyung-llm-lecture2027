"""06절 — full·selected·compressed 설계의 토큰·품질·비용을 비교한다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from context_lab import (
    DEFAULT_MODEL,
    RUNS_DIR,
    append_jsonl,
    call_model,
    compress_facts,
    estimate_cost_usd,
    estimate_tokens,
    experiment_record,
    extract_e01_pages,
    preflight_record,
    print_and_capture,
    select_documents,
    source_block,
)

INSTRUCTIONS = "문서만 근거로 답하고, 답 끝에 [E01 p.3]을 표시하세요."
QUESTION = "일반 도서는 한 번에 몇 권까지 며칠 동안 빌릴 수 있으며, 어떤 조건에서 연장할 수 있나요?"


def build_designs() -> dict[str, str]:
    pages = extract_e01_pages()
    selected = select_documents(
        [{**page, "doc_id": f"E01-p{page['page']}"} for page in pages], ["E01-p3"]
    )
    compressed = compress_facts(
        [
            {
                "fact": "도서는 7권까지 14일 동안 대출할 수 있습니다.",
                "condition": "회원 1인 기준",
                "exception": "다른 이용자의 예약이 없고 반납 예정일 전에 신청하면 1회에 한해 7일 연장 가능",
                "source": "E01.pdf p.3",
            }
        ]
    )
    return {
        "full": "\n\n".join(source_block(page) for page in pages),
        "selected": "\n\n".join(source_block(page) for page in selected),
        "compressed": compressed,
    }


def progressive_disclosure() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """고정된 2단계 로딩: 1단계 목록, 2단계 수동 선택 원문. 에이전트 루프가 아니다."""
    pages = extract_e01_pages()
    catalog = [
        {"doc_id": f"E01-p{page['page']}", "source": f"E01.pdf p.{page['page']}"}
        for page in pages
    ]
    selected = select_documents(
        [{**page, "doc_id": f"E01-p{page['page']}"} for page in pages], ["E01-p3"]
    )
    return catalog, selected


def evaluate(text: str) -> dict[str, bool]:
    checks = {
        "seven_books": "7권" in text,
        "fourteen_days": "14일" in text,
        "one_extension": "1회" in text,
        "seven_day_extension": "7일" in text,
        "reservation_condition": "예약" in text,
        "before_due_date": "반납 예정일 전" in text,
        "has_source": "E01 p.3" in text,
    }
    checks["all_pass"] = all(checks.values())
    return checks


def main() -> None:
    run_path = RUNS_DIR / "ex06_compare.jsonl"
    if run_path.exists():
        run_path.unlink()
    designs = build_designs()
    expected_cost = sum(
        estimate_cost_usd(estimate_tokens(INSTRUCTIONS + context + QUESTION), 256)
        for context in designs.values()
    )
    lines = [
        f"동일 질문·모델: {DEFAULT_MODEL}",
        f"호출 전 예상 최대 비용: ${expected_cost:.4f} (3회)",
    ]
    total_cost = 0.0
    append_jsonl(
        run_path,
        preflight_record("context_design_compare", len(designs), expected_cost),
    )
    for name, context in designs.items():
        result = call_model(
            INSTRUCTIONS,
            f"[문서]\n{context}\n\n[질문]\n{QUESTION}",
            max_output_tokens=256,
        )
        evaluation = evaluate(result.response)
        evaluation_valid = result.status == "completed"
        total_cost += result.cost_usd
        append_jsonl(
            run_path,
            experiment_record(
                experiment="context_design_compare",
                condition=name,
                repetition=1,
                document_ids=["E01"],
                sources=["E01.pdf p.1-5" if name == "full" else "E01.pdf p.3"],
                result=result,
                evaluation_raw={**evaluation, "evaluation_valid": evaluation_valid},
                extra={
                    "context_tokens_local_estimate": estimate_tokens(context),
                    "instructions_text": INSTRUCTIONS,
                    "context_text": context,
                    "question_text": QUESTION,
                },
            ),
        )
        quality = "무효" if not evaluation_valid else f"{int(evaluation['all_pass'])}/1"
        lines.append(
            f"{name:10}: 문맥≈{estimate_tokens(context)}토큰 / API 입력={result.input_tokens} / "
            f"품질={quality} / 비용=${result.cost_usd:.6f}"
        )
    catalog, selected = progressive_disclosure()
    lines.extend(
        [
            f"progressive disclosure 1단계: 메타데이터 {len(catalog)}건",
            f"progressive disclosure 2단계: 수동 선택 {[row['doc_id'] for row in selected]}",
            "이 2단계 코드는 고정된 학생 코드이며 에이전트가 아닙니다.",
            f"API 실측 비용: ${total_cost:.6f}",
            f"상세 로그: {run_path.relative_to(run_path.parent.parent)}",
        ]
    )
    print_and_capture(lines, Path(__file__).with_suffix(".stdout.txt"))


if __name__ == "__main__":
    main()
