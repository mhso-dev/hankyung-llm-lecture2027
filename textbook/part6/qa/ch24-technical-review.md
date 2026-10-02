# Ch24 독립 기술 검토

- 검토일: 2026-09-11
- 대상: 3개 `_src` 절, 노트북 코드·저장 출력, `chapter.json`, 그림 캡션, README와 노트북 Markdown
- 기준: LangGraph 1.2.11, Python 3.12

## 판정

수정 후 통과합니다. interrupt의 중단·재개 경로와 time travel 분기는 실제 노트북 출력 및 공식 문서와 일치합니다.

## 수정

- `interrupt()` 자체가 호출자에게 값을 반환한다는 모호한 표현을 고쳤습니다. 그래프 호출 결과가 payload를 `__interrupt__`에 담아 보여 주고, 같은 thread의 `Command(resume=...)` 값이 노드 안 `interrupt()`의 반환값이 된다고 분리했습니다.
- 세 절의 범용 학습 목표·도입·정리를 실제 관찰값으로 교체했습니다. 01절은 unsafe 2회 기록과 safe 파일 미생성, 02절은 maybe 재질문과 approve 완료, 03절은 원본 9000·분기 8000을 명시합니다.
- 도식의 순환 색 배정을 역할 기반으로 바꿨습니다. 사람의 승인 입력과 로컬 외부 쓰기는 초록, interrupt·Command·상태 분기 코드는 파랑입니다.

## 근거

- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) — JSON 직렬화 payload, 동일 thread_id 재개, 노드 처음부터 재실행, interrupt 앞 부작용의 멱등성.
- [LangGraph time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel) — checkpoint 재개·분기와 분기 뒤 노드 재실행.
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) — checkpoint와 state history.

## 실행 대조

01절은 거절해도 unsafe가 `transfer-local`을 두 번 기록하고 safe가 파일을 만들지 않았습니다. 02절은 `maybe` 뒤 error가 든 두 번째 payload를 받고 `approve` 뒤 `decision='approve'`, `next=()`로 끝났습니다. 03절은 0.1 원본 9000을 남긴 채 0.2 분기에서 8000을 반환했습니다.

## 남은 한계

로컬 파일 기록은 실제 송금·배포를 대신한 학습용 부작용입니다. time travel은 그래프 상태를 분기할 뿐 외부 시스템의 이미 수행한 작업을 되돌리지 않습니다.
