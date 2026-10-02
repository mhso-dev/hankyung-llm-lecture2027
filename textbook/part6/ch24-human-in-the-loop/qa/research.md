# Ch24 공식 문서 조사

> **개선 전 판(2026-09-11)** — 이 조사는 품질 개선 전 판이고, 마감(2026-09-25)에서 내용은 고치지 않고 이 표시만 더했습니다. 아래의 「payload」·「반환값」·「재개」·「분기」·「승인 게이트」·「검증」 같은 말과 옛 절 설계(실습 폴더 로컬 파일 쓰기 · 노드 안 `while True` 다시 묻기 · 소수 할인율 `0.2`)는 지금 교재와 다릅니다. 지금 교재의 조사와 설치판 소스 확인은 `qa/upgrade/chapter-lead-notes.md`·각 절 `qa/upgrade/NN-diagnosis.md`, 마감 요약은 `qa/upgrade/chapter-summary.md`에 있습니다.

조사일은 2026-09-11입니다. Python 3.12.13과 LangGraph 1.2.11을 기준으로 공식 Interrupts, Persistence, Time Travel 문서를 대조했습니다.

## 확인한 API와 실행 의미

- `interrupt(payload)`는 현재 상태를 체크포인터에 저장하고 실행을 중단합니다. payload는 JSON으로 직렬화할 수 있어야 합니다.
- 같은 `thread_id`에 `Command(resume=value)`를 전달하면 value가 중단된 `interrupt()`의 반환값이 됩니다.
- 재개 시 노드는 `interrupt()`가 있는 코드 줄부터 이어지는 방식이 아니라 노드 시작부터 다시 실행됩니다. 따라서 interrupt 앞의 부작용은 멱등해야 하며, 되돌리기 어려운 동작의 승인 게이트는 부작용 앞에 둡니다.
- `get_state_history()`로 과거 `StateSnapshot`을 찾고, `update_state()`로 값을 바꾼 체크포인트를 만든 뒤 `invoke(None, fork_config)`을 호출하면 다른 분기를 실행할 수 있습니다. 분기 지점 뒤의 노드는 다시 실행됩니다.

## 교재의 실제 검증 대응

01절은 부작용 뒤에 interrupt를 둔 실행과 interrupt 뒤에 부작용을 둔 실행을 같은 거절 값으로 비교합니다. 02절은 `maybe`를 전달해 재질문한 뒤 `approve`로 완료합니다. 03절은 10% 할인의 원본 결과 9000을 보존한 채 `discount` 직전 체크포인트의 할인율을 20%로 바꾸어 분기 결과 8000을 생성합니다.

## 공식 자료

- https://docs.langchain.com/oss/python/langgraph/interrupts — 중단·재개, 노드 재시작, interrupt 규칙, 확인 2026-09-11
- https://docs.langchain.com/oss/python/langgraph/use-time-travel — replay, fork, interrupt 재실행, 확인 2026-09-11
- https://docs.langchain.com/oss/python/langgraph/persistence — 상태 기록과 체크포인터, 확인 2026-09-11
- https://github.com/langchain-ai/langgraph/blob/main/LICENSE — MIT 라이선스, 확인 2026-09-11

## 확인 필요 항목

- 실습은 승인 순서를 안전하게 관찰하기 위해 실제 송금·배포 대신 로컬 파일 쓰기를 사용합니다.
