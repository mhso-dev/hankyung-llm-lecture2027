# Part 2 작성자 검증

범위: Ch6~8 전20절, 대응20노트북, 3개 활성 생성기.

모든 절에 실제 입력·반환·실행 시점을 설명하고 다른 과제로 원리를 적용하는 사례를 추가했습니다. 호출 표기와 개념을 먼저 설명하고 기존 옵션 비교로 연결합니다. 새로운 예시 중 실행하지 않은 것은 가정·추가 실험 설계로 표시했습니다. 기존 비용 기록을 늘려 깊이를 대신하지 않았습니다.

- Ch6: 모델/메시지/응답의 역할, 메시지 객체와 역할 별칭, `with_structured_output`의 클래스 전달·반환·호출 시점, 청크/출력 설정, Runnable 함수 감싸기, 메타데이터 결측 해석.
- Ch7: 공통 run 함수 정의/호출/반환, 역할과 단어 변경의 교란, persona와 행동 규칙, few-shot 형식/사실 구분, prompt의 로컬 서식화와 모델 호출, 공개 근거와 내부 추론, 전체 시도를 분모로 한 합의, JSON 파싱과 검증, 파일 지문과 품질의 구분.
- Ch8: 설계 예산과 모델 설정 분리, 저장/복원/선택의 실제 코드, 사람의 요약 판단과 문자열 조립 구분, 적용 조건과 충돌 구분, 반복 관찰의 범위, 수동 선택과 실제 모델 입력 구분.

정확성 교정: Ch6-01 사용자 작성 TypeError 검사 범위, Ch6-05 실제 없는 직렬화 확인 주장 삭제, Ch7-06 합의 분모/통계 독립성, Ch7-08 실제 JSON 선수 절, Ch8-06 함수가 아닌 반복문 선택·앞절 성능 저하 미관찰·문자열 검사 범위. Ch8 실패 분류 이름은 LangChain이 인용한 Drew Breunig 출처로 정정했습니다.

참고 노트북의 기본→변형→관찰 구조를 참고하되 구버전 API·항상 성능 향상 같은 일반화는 옮기지 않았습니다. 확인 자료: `/Users/mhso/working/lecture/llm/langchain-llm/02_langchain-basics/01_Basics/03_LCEL_basic.ipynb`, `02_Prompt/02-FewShotPromptTemplate.ipynb`.

공식 확인 2026-09-14: https://docs.langchain.com/oss/python/langchain/models , https://docs.langchain.com/oss/python/langchain/messages , https://www.langchain.com/blog/context-engineering-for-agents , https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents . 새 외부 예제 코드를 복제하지 않았습니다. 실행 버전은 기존 고정 환경을 유지했습니다.

1차 빌드/verify: Ch6 6절/53셀 max22, Ch7 8절/58셀 max23, Ch8 6절/80셀 max25 PASS. 이후 국소 수정은 최종 통합 때 재빌드합니다. 코드·출력 변경 없음은 전체 baseline 비교에서 재확인합니다. 생성기를 다시 실행해 정본을 덮어쓰지 않았으며 편집한 markdown 문자열을 생성기 AST와 동기화했습니다.

독립 언어·기술 검토와 전체 화면/배포 검증 대기. 개별 개정 경로는 part2-edits.json에 기록했습니다.

2026-09-14 Self-Consistency 원 논문 https://arxiv.org/abs/2203.11171 을 확인하여 원 기법의 다양한 추론 경로 표집과 최종 답 집계 정의를 대조했습니다. 정리의 첫 문장도 원 기법 전체와 이번 최종 라벨 축소 실습을 구분하도록 맞췄습니다.

- Root 배포 검사 보정: Ch06-01~03의 복습 문제 12개에 공통 `quiz-q`/`quiz-a` 클래스를 붙였습니다. 질문·해설 문장은 그대로이며 공통 스타일과 자동 해설 검사를 적용하기 위한 마크업 정리입니다.
