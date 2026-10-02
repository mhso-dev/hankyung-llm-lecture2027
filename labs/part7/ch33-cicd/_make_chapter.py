"""Ch33 초기 일괄 생성기의 안전 중지점입니다.

현재 교재 원본과 노트북은 절별 실행 결과와 독립 검토 수정을 포함합니다.
초기 생성기를 다시 실행하면 그 내용을 덮어쓸 수 있어 실행 진입점만 남기고
중지했습니다. HTML은 ``textbook/part7/ch33-cicd/_build.py``로 현재
``_src``와 실행 노트북에서 재생성합니다.
"""

from __future__ import annotations


def main() -> None:
    raise SystemExit(
        "초기 생성기는 비활성화되었습니다. "
        "_src와 notebooks를 수정한 뒤 textbook/part7/ch33-cicd/_build.py를 실행하세요."
    )


if __name__ == "__main__":
    main()
