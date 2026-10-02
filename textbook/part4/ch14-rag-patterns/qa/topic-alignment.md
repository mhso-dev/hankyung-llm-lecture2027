# Ch 14 주제 점검

커리큘럼의 대화형 질문 재작성, Multi-Query, 질의 분해, Step-back, HyDE, CRAG, Self-RAG, RAPTOR를 9개 절에 배치했습니다. 모든 흐름 선택은 `if` 문, 임계값, 반복 상한으로 구현했으며 에이전트와 패턴 래퍼를 사용하지 않았습니다.

CRAG는 최고 유사도 기준의 단발 폴백, Self-RAG는 생성 뒤 근거 검사, RAPTOR는 수동 범주를 사용한 한 단계 요약으로 범위를 제한했습니다. 원 논문의 학습된 평가기, reflection token, 반복 군집 트리를 재현했다고 설명하지 않습니다.

09절은 Ch12의 문서 12건과 Ch11 형식의 정답 문서 ID를 재사용합니다. 질문 세 건, 문서 집합, 모델, 온도를 고정하고 기준선·RRF Multi-Query·HyDE의 Recall@3, 생성 포함 전체 지연, 입출력 토큰, 추정 비용을 기록합니다. Multi-Query의 Recall은 기준선과 같았고 HyDE만 이 축소 표본에서 높았습니다.
