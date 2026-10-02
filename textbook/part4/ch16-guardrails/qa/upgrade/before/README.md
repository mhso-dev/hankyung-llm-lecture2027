# Ch 16 가드레일 · 안정화 실습

여섯 노트북은 Python 3.12 새 커널에서 각각 독립 실행됩니다. 각 노트북의 첫 코드 셀은 LangChain 1.4.0, langchain-openai 1.6.1, python-dotenv 1.2.3을 고정 설치합니다. 프로젝트 루트 `.env`의 `OPENAI_API_KEY`를 읽지만 키 값은 출력하거나 학생 파일에 저장하지 않습니다.

실습은 입력·출처 검증, 합성 개인정보 마스킹, 히스토리 트리밍과 실제 요약, 계획 호출·비용 상한, 재시도·폴백·감사 로그, 검색 문서의 간접 프롬프트 인젝션 순서로 진행합니다. 개인정보 예제와 공격 문서는 모두 이 챕터에서 만든 합성 데이터입니다. 실제 사람의 정보나 외부 공격 문서를 사용하지 않습니다.

06절의 실제 API 실행에서는 완화 전과 완화 후 모두 공격 영향 표지가 나타나지 않았습니다. 따라서 이 실행은 ‘영향 미관찰’이며 프롬프트 분리의 효과를 입증하지 않습니다. 안전 문서 통합 경로에서는 E01 출처가 통과했고, 의심 문서는 모델 호출 전에 격리하는 회귀 테스트를 별도로 확인합니다.

```bash
uv run --project labs/part4/ch16-guardrails \
  --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip \
  python textbook/_notebook/execute.py \
  labs/part4/ch16-guardrails/notebooks/*.ipynb

uv run --project labs/part4/ch16-guardrails python -m pytest -q \
  labs/part4/ch16-guardrails/tests
```

각 노트북의 실제 API 호출은 짧은 입력과 최대 140 출력 토큰으로 구성해 절당 예상 비용을 미화 1달러 미만으로 제한했습니다. 정확한 청구액은 실행 시점의 공식 가격과 제공자 사용량 화면에서 확인합니다.
