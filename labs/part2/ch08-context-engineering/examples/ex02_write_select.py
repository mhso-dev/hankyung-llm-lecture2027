"""02절 — 외부 JSON 메모리에 쓰고, 학생이 문서 ID를 수동 선택한다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from context_lab import ROOT, load_memory, print_and_capture, save_memory, select_documents


def sample_records() -> list[dict[str, str]]:
    return [
        {"doc_id": "E01-p2", "source": "E01.pdf p.2", "topic": "이용 시간", "text": "매주 월요일은 정기 휴관일입니다."},
        {"doc_id": "E01-p3", "source": "E01.pdf p.3", "topic": "자료 대출", "text": "도서는 7권까지 14일 동안 대출할 수 있습니다."},
        {"doc_id": "E01-p5", "source": "E01.pdf p.5", "topic": "주차", "text": "회원은 최초 2시간 무료입니다."},
    ]


def main() -> None:
    path = ROOT / "data" / "memory.json"
    save_memory(path, sample_records())
    selected_ids = ["E01-p3", "E01-p5"]
    selected = select_documents(load_memory(path), selected_ids)
    lines = [
        f"저장 파일: {path.relative_to(ROOT)}",
        "선택 규칙: 학생이 입력한 문서 ID 순서를 보존하고, 없는 ID와 중복 ID를 제외합니다.",
        "선택에 문서 내용이나 정답 문자열을 사용하지 않습니다.",
        f"수동 선택 ID: {selected_ids}",
        f"선택 결과: {[(row['doc_id'], row['source']) for row in selected]}",
    ]
    print_and_capture(lines, Path(__file__).with_suffix(".stdout.txt"))


if __name__ == "__main__":
    main()
