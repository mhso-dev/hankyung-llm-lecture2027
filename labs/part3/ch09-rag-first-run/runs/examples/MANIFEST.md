# Ch 9 교재 출력 근거

`ex02.txt`만 2026-09-08에 `uv run --python 3.12 python examples/ex02_load_split.py`로 다시 실행해 저장했습니다. 기존 교재 출력과 내용이 일치했습니다.

파일명이 `_preserved.txt`로 끝나는 출력은 기존 교재 원본의 실행 출력 블록을 그대로 보존한 것입니다. 각 절에 표시된 실행일은 2026-09-07~08입니다. API를 다시 호출해 재현한 출력이 아닙니다. 임베딩·검색 출력에는 `text-embedding-3-small`, 생성 출력에는 `gpt-5.4-mini`가 사용되었습니다. 검색·임베딩 점수와 생성 문장은 실행마다 달라질 수 있습니다. `ex06_preserved.txt`의 네 줄은 `runs/runs.jsonl`과 각 상세 JSONL에 같은 `run_id`가 존재합니다.

2026-09-08 회귀 테스트에서는 `uv run --python 3.12 pytest -q`가 `10 passed`로 끝났습니다. `OPENAI_API_KEY`가 설정된 환경이어서 검색 테스트 하나가 `text-embedding-3-small` 색인과 질의 임베딩을 호출했습니다. 생성 모델 호출은 없었습니다. 비용은 청구 내역을 조회한 값이 아니며, 입력 규모와 교재에 고정된 단가를 기준으로 미화 0.001달러 미만으로 추정합니다.

`examples/ex01_without_context.py`, `examples/ex05_injection.py`, `examples/ex06_commands.sh`는 교재에 표시할 실행 절차의 정본입니다. 이번 보완 과정에서는 API 출력의 재생성을 피하기 위해 실행하지 않았습니다. `examples/ex01_setup.sh`는 실습 준비 명령의 정본이며, `pytest` 명령은 위 회귀 테스트와 같은 범위를 실행합니다.

원본 절·출력 블록 순번·SHA-256 대응은 `manifest.json`에 고정했습니다.
