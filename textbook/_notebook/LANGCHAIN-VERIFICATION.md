# LangChain 호출 통일 검증

검증일: 2026-09-08. 이 기록은 호출 통일 시점의 결과이며, 후속 [Before/After 보완 검증](BEFORE-AFTER-VERIFICATION.md)에 최신 셀 개수와 실행 결과를 기록했습니다. 사용자의 후속 요청에 따라 Ch 8·9·10의 기본 실습에서 모델 호출 계층을 통일했습니다.

## 변경 내용

생성 모델은 `init_chat_model("openai:gpt-5.4-mini")`로 초기화하고 `invoke()`로 호출합니다. 응답의 텍스트는 `AIMessage.text`, 토큰 사용량은 제공될 때 `usage_metadata`에서 읽습니다. 임베딩은 `OpenAIEmbeddings.embed_documents()`·`embed_query()`를 사용합니다. 이 메서드는 벡터만 반환하므로 Ch 10의 토큰 수는 `local_token_estimate`로 기록하며 API가 반환한 실제 사용량으로 표시하지 않습니다.

Ch 8의 여섯 절, Ch 9의 생성 예제 세 절, Ch 10의 임베딩 예제 세 절을 변경했습니다. 문서 로딩·청킹 등 호출 코드가 바뀌지 않은 여덟 절은 검증된 기존 셀을 유지했습니다. 기존 설명·도식·실패 실험·Jupyter 테마와 복사 기능을 유지했습니다. 변경 전 원본은 각 챕터 `qa/langchain-before/`에 보관했습니다.

기본 실습에 직접 `openai` import가 있으면 공통 검증이 실패합니다. 기존 파일형 구현은 강사용 확장·과거 기록으로 보존했으며, 직접 SDK 학습이 명시된 Ch 18의 교육 범위는 유지합니다.

## 최종 검증

- 전체 20개 노트북, 코드 셀 116개, 셀당 최대 16줄입니다. 직접 OpenAI SDK import는 0건입니다.
- 바뀐 12개 노트북은 Python 3.12.13 새 커널에서 실제 API 실행을 통과했습니다. 전체 노트북의 코드·출력 해시와 연속 실행 번호가 유효합니다.
- Ch 8은 생성 API 11회, Ch 9는 출처 인용과 두 프롬프트 각 5회 비교, Ch 10은 캐시 재사용과 실제 청킹 3종×임베딩 2종을 확인했습니다.
- HTML 셀·내려받기 노트북·실행 원본 대조, PC·모바일 화면과 복사 검사 48건, 전달 파일 44개의 비밀값 검사가 통과했습니다.
- 공통 테스트 14개와 챕터별 회귀 테스트 64개(Ch 8: 16, Ch 9: 10, Ch 10: 38)가 통과했습니다. Ruff와 Pyright는 오류 없이 통과했습니다.

## 독립 검토

최종 판정: **APPROVE**. 변경한 12개 노트북, 공통 검증과 회귀 검사, 관련 본문과 HTML의 일치 여부를 독립 검토했습니다. 일반 import 문법에서 프로젝트 보조 모듈 검사를 빠져나가는 문제를 수정하고 회귀 검사에 추가했습니다. 남은 검토 이슈는 없습니다. 변경 문장의 의미와 API 사용량 구분을 확인했고, 코드와 출력은 윤문하지 않았습니다.

## 근거

- [공식 API 확인](references.md)
- [최종 노트북·HTML 대조](checks/notebook-contracts.json)
- [Ch 8 실행 기록](../part2/ch08-context-engineering/notebook-verification.md)
- [Ch 9 실행 기록](../../labs/part3/ch09-rag-first-run/notebook-verification.md)
- [Ch 10 실행 기록](../part3/ch10-document-processing/notebook-verification.md)

API 응답과 검색 결과는 실행마다 달라질 수 있습니다. 전체 말뭉치 품질 평가나 최종 모델 선정을 완료했다는 뜻은 아닙니다. 외부 맞춤법 서비스는 기존 스킬의 상업적 대량 처리 제한에 따라 생략하고, 변경 문장은 독립 검토를 진행했습니다. 코드와 실제 출력은 윤문하지 않습니다.
