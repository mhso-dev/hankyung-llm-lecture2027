# Ch 8 강사용 확장 실험

`context_lab.py`, `examples/`, `tests/`, `runs/`는 OpenAI SDK로 작성한 전체 실험과 회귀 검증을 보존한 강사용 확장 자료입니다. 학생은 노트북 실습을 위해 이 모듈을 가져올 필요가 없습니다.

> **먼저 읽을 것(2026-09-17)** — `examples/ex01·ex04·ex05·ex06`은 실행할 때 `runs/*.jsonl`을 지우고 다시 씁니다. 이 파일들의 해시는 `tests/test_ch06_ch08_continuity.py::test_legacy_logs_are_unchanged`가 요구하므로, 수업 전 재현은 실습 폴더를 복사한 곳에서 합니다.
> `ex04_failures.py`의 조건 이름은 교재 04절 노트북의 정의와 뜻이 다릅니다. 예제의 `confusion`은 이름이 비슷한 별도 기관 문서, `distraction`은 무관한 문장 되풀이입니다. 교재 04절의 혼란은 필요 없는 내용이 답에 쓰이는 경우, 산만은 아주 긴 컨텍스트에 치우치는 경우입니다.

강사용 전체 실험과 회귀 테스트는 아래 명령으로 실행합니다.

```bash
cd labs/part2/ch08-context-engineering
uv sync
uv run python examples/ex01_budget.py
uv run python examples/ex02_write_select.py
uv run python examples/ex03_compress_isolate.py
uv run python examples/ex04_failures.py
uv run python examples/ex05_rot.py
uv run python examples/ex06_compare.py
uv run ruff check .
uv run pytest -q
```

기존 OpenAI SDK 확장 실험도 프로젝트 루트의 `.env`를 읽으며 키를 출력하거나 로그에 기록하지 않습니다. 가격 상수는 2026-09-08 OpenAI 공식 가격 페이지의 Standard 가격인 입력 100만 토큰당 0.75달러, 캐시 입력 0.075달러, 출력 100만 토큰당 4.50달러를 사용합니다. 실제 청구액은 계정 설정과 가격 변경에 따라 달라질 수 있습니다.

각 예제의 콘솔 출력은 같은 이름의 `examples/*.stdout.txt`에 저장됩니다. API 실험의 원자료는 `runs/*.jsonl`에 조건, 반복 번호, 문서 ID, 출처, 모델 응답, API usage, 계산 비용, 지연 시간, 평가 원자료, UTC 날짜, 모델명을 기록합니다. 정답률 감소나 실패 발생을 보장하지 않으며 발생하지 않은 경우도 그대로 기록합니다.

## 강사용 재현 안내

수업 전 위 명령을 순서대로 한 번 실행해 모델 접근 권한과 비용을 확인합니다. `ex04_failures.py`는 clean을 포함한 5개 조건을 각 3회, `ex05_rot.py`는 3개 길이와 3개 근거 위치 조합을 각 3회 실행합니다. 수업에서 더 많은 반복이 필요하면 `main(repetitions=5)`로만 바꾸고, 호출 전 예상 비용이 1달러 미만인지 먼저 확인합니다. 모델과 근거 문장은 고정해야 길이와 위치 효과를 비교할 수 있습니다.

`ex03_compress_isolate.py`의 독립 필드 조립은 관찰과 디버깅을 위한 구조이며 보안 경계가 아닙니다. `ex06_compare.py`의 progressive disclosure도 학생 코드에 고정된 목록 확인→수동 ID 선택의 2단계 로딩이며 에이전트 구현이 아닙니다.
