"""03절 — 출처·조건·예외를 보존해 압축하고 메시지를 독립 조립한다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from context_lab import assemble_isolated_messages, compress_facts, print_and_capture


def main() -> None:
    records = [
        {
            "fact": "도서는 7권까지 14일 동안 대출할 수 있습니다.",
            "condition": "회원 1인 기준",
            "exception": "예약자가 없고 반납 예정일 전에 신청하면 1회 7일 연장 가능",
            "source": "E01.pdf p.3",
        },
        {
            "fact": "매주 월요일은 정기 휴관일입니다.",
            "condition": "정기 휴관",
            "exception": "공휴일이 월요일이면 화요일도 휴관",
            "source": "E01.pdf p.2",
        },
    ]
    compressed = compress_facts(records)
    loan_messages = assemble_isolated_messages(
        "근거만 사용하고 출처를 표시하세요.",
        compress_facts([records[0]]),
        "도서 대출 기간과 연장 조건은 무엇인가요?",
    )
    closure_messages = assemble_isolated_messages(
        "근거만 사용하고 출처를 표시하세요.",
        compress_facts([records[1]]),
        "정기 휴관일과 예외는 무엇인가요?",
    )
    assert "휴관" not in loan_messages["input"]
    assert "대출" not in closure_messages["input"]
    lines = [
        "압축 결과:",
        compressed,
        "",
        f"대출 질문 독립 입력: {loan_messages['input']}",
        f"휴관 질문 독립 입력: {closure_messages['input']}",
        "주의: 질문별 입력 분리는 간섭을 줄이지만 보안 격리를 제공하지 않습니다.",
    ]
    print_and_capture(lines, Path(__file__).with_suffix(".stdout.txt"))


if __name__ == "__main__":
    main()
