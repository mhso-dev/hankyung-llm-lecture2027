# Ch21·Ch29 독립 기술 검토

검토일: 2026-09-11  
검토 범위: Ch21 6절과 Ch29 4절의 `_src`, 실행 완료 노트북, Ch21 `rag-comparison.json`, 고정 패키지 `langchain==1.4.0`, `agentevals==0.0.9`

## 결론

조건부 통과입니다. Ch21의 비교는 Ch14 원문 12건과 C01·C05·C07 세 질문을 실제 임베딩·모델 호출로 실행했고, 각 경로의 답·검색 문서 ID·사용량·지연을 저장했습니다. `supported`는 문자열 포함 검사가 아니라 사람 지정 `gold_doc_id` 원문과 답을 읽는 별도 LLM judge의 이 실행에서 나온 판정입니다. 따라서 Agent 3/3, 고정 RAG 2/3은 이 세 질문과 이 judge의 관찰값일 뿐 일반 품질 우열이 아닙니다.

Ch29의 01~03절은 평가 규칙을 보이기 위해 코드로 만든 메시지 궤적을 사용합니다. 03절은 실제 모델 API로 judge를 호출하지만, 그 입력 궤적 자체는 서비스 에이전트 실행 로그가 아닙니다. 실제 기록의 비교는 04절에서 Ch18 저장 출력 5행과 Ch21 저장 JSON 3행을 읽어 수행합니다.

## 확인한 근거

- [LangChain Agents](https://docs.langchain.com/oss/python/langchain/agents) — `create_agent`가 모델·도구 루프를 구성하고 상태와 도구를 사용하는 방식입니다. 확인: 2026-09-11, 설치 버전 1.4.0.
- [LangChain v1 migration guide](https://docs.langchain.com/oss/python/migrate/langchain-v1) — `create_react_agent`에서 `create_agent`로의 이식, `system_prompt`, TypedDict 상태, `context` 사용을 확인했습니다.
- [LangChain Structured output](https://docs.langchain.com/oss/python/langchain/structured-output) — ProviderStrategy·ToolStrategy와 `structured_response` 결과 키를 확인했습니다.
- [agentevals upstream README](https://github.com/langchain-ai/agentevals/blob/main/README.md) — 궤적 매칭과 LLM judge 표면을 확인했습니다. 설치된 `agentevals==0.0.9`의 `trajectory/match.py`도 기본 도구 인자 비교가 `exact`이며 strict·unordered·subset·superset의 방향을 명시함을 확인했습니다.

## 수정·재확인

1. Ch21-03의 `AgentState` 설명은 모든 실행 상태에 `structured_response`가 있다고 읽힐 수 있어, 구조화 출력을 구성한 경우에 추가된다고 좁혔습니다.
2. Ch21-06 복습 3번은 저장된 판정과 달랐습니다. LLM judge 지지 판정 3/3 대 2/3과 작은 표본·재검색 미관찰·judge 한계를 함께 쓰도록 고쳤습니다.
3. Ch29-03은 처음에 참조 궤적 없는 프롬프트를 사용하면서 참조 동등성을 설명했습니다. 통합 담당자가 `TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE`로 고쳐 새 커널에서 실행했습니다. 새 출력은 strict=True, trajectory_accuracy=True이며 동일한 두 고정 예시를 비교한 결과입니다.
4. Ch29-01~03은 고정 예시 궤적과 실제 실행 기록을 구분하도록 본문을 고쳤습니다.

## 도식 의미 점검

파랑은 학생 코드·변환, 보라는 실제 모델 판단, 초록은 도구·데이터, 노랑은 측정·평가로 대조했습니다. Ch21-01의 도구 선택은 모델 판단으로, Ch21-02의 ToolStrategy는 코드 구성으로, Ch21-05의 최종 답은 데이터 결과로 바로잡았습니다. Ch29-01의 모델처럼 보이던 상자는 고정 예시 궤적으로, Ch29-03의 실제 궤적 표시는 고정 예시 궤적으로 바꿨습니다. SVG와 Excalidraw를 같은 생성기로 다시 만들었고, 도식의 의미가 본문 설명과 일치합니다.

## 배포 경로 재검토

Ch21-06은 처음에 프로젝트 루트를 기준으로 한 상대 경로를 사용했습니다. 노트북 커널의 작업 폴더를 `notebooks/`로 두면 Ch14 자료와 Ch21 JSON 저장 위치를 찾지 못하는 결함이었습니다. 환경 준비 셀에서 `labs/part6/ch21-create-agent/pyproject.toml`을 표지로 프로젝트 루트 `ROOT`를 찾고, 입력·출력 경로를 `ROOT / ...`로 바꿨습니다. 출력에는 `relative_to(ROOT)`만 표시해 개인 절대 경로를 남기지 않습니다.

수정한 Ch21-06을 `notebooks/` 작업 폴더의 새 Python 3.12 커널에서 실행했고, 그 JSON을 읽는 Ch29-04도 그 뒤 새 커널에서 다시 실행했습니다. 이번 실행에서 Ch21 두 경로의 judge `supported`는 모두 3/3이었고, Agent 평균은 519.7토큰·1.880초, nearest-rank p95는 541토큰·2.094초였습니다. 이전 실행과 다른 C01 judge 판정은 모델 기반 judge의 변동을 보여 주므로 본문도 해당 관찰 범위로 갱신했습니다. 나머지 아홉 노트북은 파일 입출력과 프로젝트 의존 경로를 읽기 전용으로 점검했으며, 프로젝트 상대 경로를 직접 여는 추가 사례는 발견하지 못했습니다.

## 한계

- Ch21 C01의 고정 RAG 답은 검색된 두 문서 중 `gold_doc_id` 밖의 전자책 정보를 더했습니다. 이전 실행의 judge는 이를 지원하지 않는다고 판정했지만, 배포 경로 수정 뒤 재실행 judge는 원문과 모순되지 않는다며 True로 판정했습니다. 두 판정 모두 고정 RAG 검색 자체의 실패를 증명하지 않습니다.
- Ch29-04의 Ch18 `quality/5`와 Ch21 `supported`는 척도가 다릅니다. 공통 열은 운영 대시보드 형식이며 성능 대결이 아닙니다.
- 세 건의 nearest-rank p95는 최댓값과 같아집니다. 운영 SLO는 더 많은 실제 대화로 정해야 합니다.
