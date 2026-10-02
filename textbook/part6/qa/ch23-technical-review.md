# Ch23 독립 기술 검토

- 검토일: 2026-09-11
- 대상: 6개 `_src` 절, 노트북·저장 출력, `durability_worker.py`, `idempotency_worker.py`, `chapter.json`, 그림 캡션, README와 노트북 Markdown
- 기준: LangGraph 1.2.11, PostgreSQL 17, SQLite checkpointer 3.0.3

## 판정

수정 후 통과합니다. 체크포인트·thread_id, PostgresSaver 준비, durability 모드, pending writes, 노드 경계와 멱등성의 설명은 실제 실행 결과와 공식 문서에 맞습니다.

## 수정

- 여섯 절의 범용 학습 목표·도입·정리를 각 실험의 실제 값과 범위로 바꿨습니다.
- 04절은 이번 종료 시점에서만 async와 sync가 `first`를 보존했다는 관찰을 명시했습니다. async가 언제나 보존한다는 주장은 하지 않습니다.
- 05절은 pending writes가 런타임 상태의 부분 성공을 보존한다는 범위와 외부 부작용 중복 방지의 별도 필요성을 분리했습니다.
- 도식의 순환 색 배정을 역할 기반으로 바꿨습니다. PostgreSQL·SQLite 저장소와 체크포인트 표는 초록, 종료 실패와 flaky 실패는 빨강, 그래프의 저장·재개·내구성 제어는 파랑입니다.

## 근거

- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) — 단계별 checkpoint, thread, pending writes, checkpointer 구현.
- [LangGraph durability reference](https://reference.langchain.com/python/langgraph/types/Durability) — `sync`, `async`, `exit`의 저장 시점.
- [Postgres checkpointer README](https://github.com/langchain-ai/langgraph/blob/main/libs/checkpoint-postgres/README.md) — `PostgresSaver`, 연결, `setup()`.

## 실행 대조

02절은 setup 전 `UndefinedTable`, setup 뒤 `value=12`와 네 checkpoint 표를 출력합니다. 04절은 exit에서 `first, second, first, second`, 이번 async·sync에서 `first, second, second`를 기록했습니다. 05절은 `good, flaky, flaky`로 good의 부분 성공을 보존했습니다. 06절은 동일한 종료·재개 조건에서 naive 2회, idempotent 1회 기록을 확인했습니다.

## 남은 한계

async의 결과는 저장 매체와 종료 타이밍에 따라 달라집니다. SQLite 파일 검사와 단일 작업 키는 학습용 비교이며, 운영의 동시 요청에는 원자적 고유 제약 또는 제공자의 멱등 키가 필요합니다.
