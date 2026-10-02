# Ch 6 노트북 실행 검증

- 실행일: 2026-09-09
- 환경: Python 3.12.13, LangChain 1.4.0, OpenAI 통합 1.6.0, Anthropic 통합 1.7.1, Google 통합 4.4.0
- 실행기: `textbook/_notebook/execute.py`
- 결과: 6개 노트북, 45개 코드 셀 새 커널 실행 통과
- 실제 외부 호출: OpenAI. Anthropic·Google은 키 부재로 실행하지 않음

각 노트북의 `metadata.verification`에 코드와 출력 SHA-256, 실행 시각, Python 버전이 저장되어 있습니다. 03절의 충돌 입력은 모델이 범위 안의 값으로 고쳐 실제 파싱 실패가 관찰되지 않았습니다. 이 결과를 실패 재현으로 표현하지 않습니다.
