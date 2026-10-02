# Ch25 기술 최종 검토

- 검토일: 2026-09-11
- 대상: Ch25 Streaming 01~03의 노트북 코드·실행 출력·도식·학생용 원고
- 판정: 통과. 코드와 실행 출력은 수정하지 않았습니다. 원고의 이전 실행 수치와 설명만 최신 출력에 맞췄습니다.

## 공식 근거

- [LangGraph Streaming](https://docs.langchain.com/oss/python/langgraph/streaming) — `values`, `updates`, `messages`, `custom`, `checkpoints`, `tasks`, `debug`의 의미, 복수 모드의 v1 튜플 형식, `messages`의 `(message_chunk, metadata)` 형식을 확인했습니다. 확인 2026-09-11, LangGraph 1.2.11.
- [GPT-5.4 mini 모델 문서](https://developers.openai.com/api/docs/models/gpt-5.4-mini) — 입력 $0.75/1M, 캐시 입력 $0.075/1M, 출력 $4.50/1M 토큰 가격을 확인했습니다. 확인 2026-09-11.

## 코드·출력 대조

- 01은 모델을 호출하지 않는 로컬 `StateGraph`입니다. 출력은 values 3, updates 2, messages 0, custom 2, checkpoints 4, tasks 4, debug 8입니다. 따라서 API 키·비용을 요구한다고 쓴 이전 원고를 정정했습니다.
- 02는 messages 사건 88개와 내용이 있는 조각 84개를 구분합니다. 내용 조각을 이어 붙인 값과 `answer` 상태의 최종 답변이 같다는 assert가 통과합니다. 사건 수를 토큰 수로 부르지 않도록 원고와 복습 문제를 정정했습니다.
- 03은 updates, messages, custom을 순서대로 각각 호출합니다. updates는 first_event/total 2.622초, messages는 0.613/0.620/1.101초, custom은 0.003/1.431초입니다. `ttft_s`는 클라이언트가 messages의 내용 있는 첫 조각을 받은 시간의 근삿값이며, 서버 내부 첫 토큰 시각이나 조각 하나의 토큰 수를 뜻하지 않습니다.
- 세 호출의 input/cached input/output은 각각 45/0/91, 45/0/84, 45/0/111이고, 추정 비용은 $0.00044325, $0.00041175, $0.00053325, 합계 $0.00138825입니다. 별도 순차 호출과 서로 다른 생성 길이 때문에 모드의 속도·비용 우열을 뜻하지 않습니다.

## 도식과 보존

- 02 도식의 “모델 노드 실행”은 실제 모델 응답 생성 단계이므로 생성기 역할을 `model`로 바꾸어 보라색으로 렌더링했습니다. 데이터는 초록색, 측정값은 노란색으로 유지했습니다.
- 노트북 3개와 도식 소스·출력 7개, 생성기 1개의 SHA-256은 `ch25-code-output-preservation.sha256`에 고정했고, 최종 확인에서 10개 모두 일치했습니다.

## 한계

- 03의 시간·usage·추정 비용은 해당 실행 한 번의 관찰값입니다. 운영 기준에는 같은 입력의 반복 실행과 분포 기록이 필요합니다.
