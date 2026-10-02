# Ch23 공식 문서 조사

> **개선 전 판(2026-09-11)** — 이 조사는 품질 개선 전 판이고, 마감(2026-09-25)에서 내용은 고치지 않고 이 표시만 더했습니다. 아래의 「스냅샷」·「반환」 같은 말과 옛 절 설계(실습 폴더 `data/` 쓰기·옛 Docker 명령 등)는 지금 교재와 다릅니다. 지금 교재의 조사와 설치판 소스 확인은 `qa/upgrade/chapter-lead-notes.md`·각 절 `qa/upgrade/NN-diagnosis.md`·`NN-probe.md`, 마감 요약은 `qa/upgrade/chapter-summary.md`에 있습니다.

조사일은 2026-09-11입니다. Python 3.12.13과 LangGraph 1.2.11을 기준으로 공식 문서, 공식 API 레퍼런스, LangGraph 저장소의 Postgres 체크포인터 README를 대조했습니다.

## 확인한 API와 실행 의미

- 체크포인터는 그래프 단계마다 상태 스냅샷을 저장하고 `thread_id`로 관련 기록을 묶습니다. `get_state()`는 최신 상태를, `get_state_history()`는 스레드의 기록을 반환합니다.
- `PostgresSaver`는 별도 패키지인 `langgraph-checkpoint-postgres`에서 제공됩니다. 최초 사용 시 `setup()`으로 표를 준비합니다. `from_conn_string()`은 `autocommit=True`, `prepare_threshold=0`, `row_factory=dict_row` 연결을 구성합니다.
- `durability="sync"`는 다음 단계 전에 저장을 완료하고, `async`는 다음 단계 실행과 저장을 겹치며, `exit`는 실행이 끝날 때 저장합니다.
- 같은 superstep에서 일부 task가 실패하면 성공한 task의 쓰기는 pending writes로 보존됩니다. 재개할 때 성공한 task는 다시 실행하지 않습니다.
- 내구 실행의 재개 단위는 노드 경계입니다. 노드 안에서 외부 쓰기를 마친 뒤 상태 반환 전에 종료되면 해당 노드가 처음부터 다시 실행되므로 외부 쓰기는 멱등해야 합니다.

## 교재의 실제 검증 대응

02절은 로컬 PostgreSQL 17의 `ch23_lab` 스키마에서 setup 전 `UndefinedTable`을 재현하고 setup 뒤 네 체크포인트 표를 조회합니다. 04절은 `exit`, `async`, `sync` 각각에서 두 번째 노드 진입 직후 실제 자식 프로세스를 종료하고 같은 SQLite와 `thread_id`로 재개합니다. 05절은 같은 superstep의 `good`과 `flaky` 호출 로그로 pending writes를 확인합니다. 06절은 외부 쓰기 뒤 프로세스를 종료해 `operation_id` 검사 전후의 중복 기록을 비교합니다.

## 공식 자료

- https://docs.langchain.com/oss/python/langgraph/persistence — 체크포인트, 스레드, 상태 기록, pending writes, 확인 2026-09-11
- https://reference.langchain.com/python/langgraph/types/Durability — `sync`, `async`, `exit` 정의, LangGraph 1.2.11, 확인 2026-09-11
- https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph — 노드 경계와 내구 실행 모드, 확인 2026-09-11
- https://github.com/langchain-ai/langgraph/blob/main/libs/checkpoint-postgres/README.md — PostgresSaver 설치·setup·연결 조건, 확인 2026-09-11
- https://github.com/langchain-ai/langgraph/blob/main/LICENSE — MIT 라이선스, 확인 2026-09-11

## 확인 필요 항목

- `async` 모드의 중단 전 저장 여부는 저장 장치 속도와 프로세스 종료 시점에 따라 달라질 수 있습니다. 교재는 이번 로컬 실행에서 관찰한 값과 그 한계를 함께 적었습니다.
