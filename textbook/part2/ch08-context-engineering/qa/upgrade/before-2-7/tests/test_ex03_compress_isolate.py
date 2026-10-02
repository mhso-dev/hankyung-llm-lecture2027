import pytest

from context_lab import assemble_isolated_messages, compress_facts


def test_compression_preserves_fact_condition_exception_and_source() -> None:
    compressed = compress_facts(
        [{"fact": "사실", "condition": "조건", "exception": "예외", "source": "E01 p.3"}]
    )
    for value in ("사실", "조건", "예외", "E01 p.3"):
        assert value in compressed


def test_compression_rejects_missing_provenance() -> None:
    with pytest.raises(ValueError, match="필드"):
        compress_facts([{"fact": "사실", "condition": "조건", "exception": "예외"}])


def test_message_fields_are_separate() -> None:
    messages = assemble_isolated_messages("지시", "근거", "질문")
    assert messages["instructions"] == "지시"
    assert "[근거]\n근거" in messages["input"]
    assert "[질문]\n질문" in messages["input"]


def test_two_tasks_can_receive_only_their_own_evidence() -> None:
    loan = assemble_isolated_messages("지시", "대출 근거", "대출 질문")
    closure = assemble_isolated_messages("지시", "휴관 근거", "휴관 질문")
    assert "휴관" not in loan["input"]
    assert "대출" not in closure["input"]
