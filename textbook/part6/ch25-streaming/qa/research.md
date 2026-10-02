# Ch25 공식 문서 조사

> **개선 전 판(2026-09-11)** — 이 조사는 품질 개선 전 판이고, 마감(2026-09-25)에서 내용은 고치지 않고 이 표시만 더했습니다. 아래 「`checkpoints`와 `tasks`는 체크포인터가 있어야 사건이 생성됩니다」는 설치한 langgraph 1.2.11 출력과 다릅니다(01절 노트북 8절 — 체크포인터 없이 `tasks` 사건 넷). `messages` 문장의 「메시지 조각」도 지금 교재 말(스트림 청크)과 다르고, 설치판 `pregel/_messages.py`는 노드가 내놓은 메시지 객체도 이 모드로 보냅니다. 지금 교재의 조사와 설치판 소스 확인은 `qa/upgrade/chapter-lead-notes.md`·각 절 `qa/upgrade/NN-diagnosis.md`, 마감 요약은 `qa/upgrade/chapter-summary.md`에 있습니다.

- 확인일: 2026-09-11
- 기준: Python 3.12, LangGraph 1.2.11
- `StreamMode`는 `values`, `updates`, `messages`, `custom`, `checkpoints`, `tasks`, `debug`의 일곱 값입니다.
- 복수 모드의 기본 v1 출력은 `(mode, data)` 튜플이고 최신 v2는 `type`, `ns`, `data` 필드로 통일됩니다. 교재 실습은 기준 버전의 기본 v1 형식을 실행했습니다.
- `checkpoints`와 `tasks`는 체크포인터가 있어야 사건이 생성됩니다. `messages`는 그래프 안의 모델 호출이 있어야 메시지 조각이 생성됩니다.

## 출처

- https://docs.langchain.com/oss/python/langgraph/streaming
- https://reference.langchain.com/python/langgraph/types/StreamMode
- https://github.com/langchain-ai/langgraph/blob/main/LICENSE (MIT)
