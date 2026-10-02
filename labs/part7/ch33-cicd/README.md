# Ch33 CI/CD 실습

Python 3.12와 uv를 사용합니다. `uv sync --dev` 뒤 `uv run ruff check cicd_demo.py server.py tests scripts`, `uv run python -m pytest`, `uv run python -m build`, `uv run python scripts/evaluate_regression.py`를 실행합니다. `.github/workflows/ci.yml`은 같은 명령을 PR과 main push에서 실행하는 완성 예시입니다.

`data/regression-baseline.json`은 Ch15의 Groundedness와 Ch29의 추가 도구 호출 개념을 학습용 최소 자료로 다시 작성한 공개 고정 자료입니다. 실제 Ch15·29 전체 실행 결과를 복사하거나 재평가한 자료가 아닙니다. 원본 경로와 SHA-256은 기준선 파일에 기록했습니다. 노트북은 Docker 이미지 v1·v2를 실제로 빌드하고, HTTP 서비스를 v1→v2→v1 순서로 실행해 health 응답을 확인합니다. `scripts/deploy.py`와 `rollback.py`는 이 실습의 감사 가능한 로컬 배포 이력을 남깁니다. 레지스트리 push, 클라우드 인증, GitHub PR 생성, 실제 클라우드 배포는 수행하지 않습니다.
