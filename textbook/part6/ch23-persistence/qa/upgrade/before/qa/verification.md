# Ch23 실행 검증

- 실행일: 2026-09-11
- 환경: Python 3.12.13, LangGraph 1.2.11, langgraph-checkpoint-sqlite 3.0.3, langgraph-checkpoint-postgres 3.0.5, psycopg 3.3.3, PostgreSQL 17
- 노트북: 6개를 각각 새 커널에서 실행했습니다. 공통 검증기는 29개 코드 셀과 셀당 최대 23줄을 확인했습니다.
- 외부 동작: Docker의 로컬 PostgreSQL과 실습 폴더의 SQLite·텍스트 파일만 사용했습니다. 모델 API와 외부 업무 시스템은 호출하지 않았습니다.

## 실제 결과

- 01절: 같은 `customer-a` 스레드는 `3 → 7`로 이어졌고 `customer-b`는 4에서 독립적으로 시작했습니다.
- 02절: `setup()` 전 PostgreSQL `UndefinedTable`을 재현했습니다. setup 뒤 결과는 `value=12`였고 `checkpoint_blobs`, `checkpoint_migrations`, `checkpoint_writes`, `checkpoints` 표를 확인했습니다.
- 03절: 첫 SQLite 연결을 닫은 뒤 새 연결과 새 그래프 객체에서 `질문 1 → 답변 1 → 질문 2 → 답변 3` 순서를 복원했습니다.
- 04절: 두 번째 노드 진입 직후 자식 프로세스를 종료했습니다. `exit`의 중단 전 상태는 없고 재개 호출 로그는 `first, second, first, second`였습니다. 이번 실행의 `async`와 `sync`는 `completed=['first']`를 보존했고 호출 로그는 `first, second, second`였습니다. 세 모드 모두 실제 재개 뒤 `['first', 'second']`로 완료했습니다.
- 05절: 첫 실행 호출은 `good, flaky`, 재개 뒤 전체 호출은 `good, flaky, flaky`였습니다. 최종 상태는 `good-result`와 `flaky-result`를 모두 포함했습니다.
- 06절: 외부 쓰기 뒤 자식 프로세스를 종료하고 재개했습니다. naive 방식은 `order-2306`을 2회, 멱등 키 방식은 1회 기록했습니다.

## 검증 명령 결과

- `execute.py notebooks/*.ipynb --cwd <project-root>` → 6개 PASS
- `_build.py` → index와 절 6개 생성
- `verify.py --chapter textbook/part6/ch23-persistence` → `PASS 6 sections / 29 code cells (max 23 lines)`
- `visual.cjs textbook/part6/ch23-persistence` → 1280px·390px에서 6개 절과 index 모두 PASS
- Part 6 노트북 준비 검사에서 Ch23 6개는 설치 셀, 구체적 목적 주석, 함수 타입 힌트, assert, 셀당 25줄 이하를 모두 충족했습니다.
- `ruff check`와 `python -m py_compile`로 두 worker와 집필 생성 스크립트를 검사해 통과했습니다.
- 검증에 사용한 `kdt-ch23-postgres` 컨테이너는 최종 검사 뒤 중지하고 제거했습니다.

## 확인 필요 항목

- 한국어 감사 3단은 집필자와 다른 검토 세션에서 수행할 예정입니다.
- `async` 저장 결과는 종료 타이밍과 저장 장치에 따라 달라질 수 있습니다.
