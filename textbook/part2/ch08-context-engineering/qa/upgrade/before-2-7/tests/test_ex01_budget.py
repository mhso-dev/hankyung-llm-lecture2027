import pytest

from context_lab import ensure_input_fits, make_budget


def test_budget_accounts_for_every_reserved_part() -> None:
    budget = make_budget(4096, 256, 128, "지시", "질문")
    assert (
        budget.output_reserve
        + budget.safety_margin
        + budget.instruction_tokens
        + budget.question_tokens
        + budget.evidence_budget
        == budget.total_limit
    )


def test_budget_rejects_overflow() -> None:
    try:
        make_budget(1, 1, 1, "긴 지시", "긴 질문")
    except ValueError as error:
        assert "전체 한도" in str(error)
    else:
        raise AssertionError("초과 예산이 거부되지 않았습니다")


def test_estimated_input_must_leave_output_and_safety_reserves() -> None:
    budget = make_budget(100, 20, 10, "지시", "질문")
    ensure_input_fits(budget, 70)
    with pytest.raises(ValueError, match="입력 상한"):
        ensure_input_fits(budget, 71)
