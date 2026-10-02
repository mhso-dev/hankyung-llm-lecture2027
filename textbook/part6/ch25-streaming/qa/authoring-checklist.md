# 집필 점검표

> **개선 전 판(2026-09-11~14)** — 옛 판 점검표이고, 마감(2026-09-25)에서 내용은 고치지 않고 이 표시만 더했습니다. 「stream mode」·「조각」·「측정」 같은 옛 말과 옛 절 설계(03의 모드별 따로 세 번 요청)가 남아 있습니다. 지금 기록은 챕터 폴더 `집필점검표.md`의 「품질 개선」·「마감」 절과 `qa/upgrade/`입니다.

## 01-일곱-가지-stream-mode

- 학습 질문: 일곱 가지 stream mode의 실행 경계와 관찰값은 무엇인가?
- 입력과 비교 조건: 노트북의 고정 입력과 모드 또는 위임 구조만 변경
- 실제 연산: 새 커널에서 모델 호출 없이 LangGraph 로컬 그래프 실행
- 관찰 결과: 실행 출력과 verification 해시로 확인
- 형식: experiment
- 해석 범위: 한 질문·한 실행의 결과이며 일반 성능으로 확대하지 않음
- 본문과 그림: 노트북 출력과 도식 요소를 대조
- 별도 검토: 독립 언어 검토 완료. `textbook/part6/qa/language/ch25-final.md` 참조

## 실제 실행 근거

- 01: values=3, updates=2, messages=0, custom=2, checkpoints=4, tasks=4, debug=8
- 02: messages 사건 88개, 내용이 있는 조각 84개, updates 1개, custom 2개, 이어 붙인 조각과 최종 answer 일치
- 03: updates first_event/total 2.622초, messages first_event/TTFT 근삿값/total 0.613/0.620/1.101초, custom first_event/total 0.003/1.431초, 세 호출 추정 비용 합계 $0.00138825
- 실행 검증: 3개 노트북 13개 코드 셀 새 커널 통과

## 02-토큰과-중간-진행-스트리밍

- 학습 질문: 토큰과 중간 진행 스트리밍의 실행 경계와 관찰값은 무엇인가?
- 입력과 비교 조건: 노트북의 고정 입력과 모드 또는 위임 구조만 변경
- 실제 연산: 새 커널에서 LangGraph 또는 LangChain 모델 호출
- 관찰 결과: 실행 출력과 verification 해시로 확인
- 형식: experiment
- 해석 범위: 한 질문·한 실행의 결과이며 일반 성능으로 확대하지 않음
- 본문과 그림: 노트북 출력과 도식 요소를 대조
- 별도 검토: 독립 언어 검토 완료. `textbook/part6/qa/language/ch25-final.md` 참조

## 03-TTFT와-total-비교

- 학습 질문: TTFT와 total 비교의 실행 경계와 관찰값은 무엇인가?
- 입력과 비교 조건: 노트북의 고정 입력과 모드 또는 위임 구조만 변경
- 실제 연산: 새 커널에서 LangGraph 또는 LangChain 모델 호출
- 관찰 결과: 실행 출력과 verification 해시로 확인
- 형식: experiment
- 해석 범위: 한 질문·한 실행의 결과이며 일반 성능으로 확대하지 않음
- 본문과 그림: 노트북 출력과 도식 요소를 대조
- 별도 검토: 독립 언어 검토 완료. `textbook/part6/qa/language/ch25-final.md` 참조
