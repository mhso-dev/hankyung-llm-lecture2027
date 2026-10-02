# Ch25 공식 문서 조사

- 확인일: 2026-09-11
- 기준: Python 3.12, LangGraph 1.2.11
- `StreamMode`는 `values`, `updates`, `messages`, `custom`, `checkpoints`, `tasks`, `debug`의 일곱 값입니다.
- 복수 모드의 기본 v1 출력은 `(mode, data)` 튜플이고 최신 v2는 `type`, `ns`, `data` 필드로 통일됩니다. 교재 실습은 기준 버전의 기본 v1 형식을 실행했습니다.
- `checkpoints`와 `tasks`는 체크포인터가 있어야 사건이 생성됩니다. `messages`는 그래프 안의 모델 호출이 있어야 메시지 조각이 생성됩니다.

## 출처

- https://docs.langchain.com/oss/python/langgraph/streaming
- https://reference.langchain.com/python/langgraph/types/StreamMode
- https://github.com/langchain-ai/langgraph/blob/main/LICENSE (MIT)
