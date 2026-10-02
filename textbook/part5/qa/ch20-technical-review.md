# Ch20 독립 기술 검토

검토자: 집필자와 구분된 code-reviewer 에이전트. 판정: **APPROVE**. 최종 실제 코드·본문·도식·실습 환경에서 CRITICAL/HIGH/MEDIUM 지적 0건입니다.

## 명세와 실제 구현

StateGraph·ToolNode·tools_condition을 직접 조립하며 create_agent와 create_react_agent를 사용하지 않습니다. 01절은 실제 AIMessage(tool_calls) → ToolMessage → 최종 AIMessage를 출력하고 도구가 필요 없는 질문과 비교합니다. 02절은 동일한 call_bad_1에서 ValueError 전파와 좁은 오류 처리 함수의 ToolMessage 변환을 비교하며 tool_call_id 보존을 assert합니다. 03절은 결정적 로컬 순환 그래프로 recursion_limit=4의 GraphRecursionError를 재현하고 상태 기반 END를 추가해 count=3에서 종료합니다.

04절은 같은 세 질문·자료·gpt-5.4-mini·반복 횟수·컴파일된 그래프·ToolNode·답변 모델을 유지합니다. choose 노드가 고정 규칙 또는 모델로 도구 호출 메시지를 만드는 조건만 달라집니다. ToolMessage 존재를 검사하고 graph.invoke 전체 시간을 측정합니다.

## 수정 확인

- 서로 다른 실행 구조와 직접 대입한 trace를 공통 그래프와 실제 노드 기록으로 교체했습니다. fixed는 fixed_choose → tools → model_answer, agent는 model_choose → tools → model_answer를 기록합니다.
- 코드 셀을 최대 23줄로 분리했습니다.
- 시수 메타를 소수 시간으로 표기해 강의 3h·실습 5h를 확인했습니다.
- usage_metadata 누락을 0으로 숨기지 않고 입력·출력 토큰의 존재를 검사합니다. 비용은 estimated_cost_usd로 표시합니다.
- 모델 호출만이 아닌 그래프 전체 지연을 측정하고 본문·QA 기록을 맞췄습니다.

## 실행 증거

네 노트북은 Python 3.12.13 새 커널, allow_errors=False, status=passed입니다. 독립 verify_lesson은 4절·32개 셀·최대 23줄을 통과했고 코드·출력·내장 다운로드가 일치합니다.

04절의 12회 그래프 실행은 추정 비용 합계 0.003314달러입니다. fixed/agent 평균 입력 토큰 88/264.3, 출력 토큰 22.5/41.5, 그래프 전체 지연 1.077/1.462초입니다. 본문은 3문항×2회 표본의 한계를 명시합니다.

집필 생성기 Pyright는 오류·경고 0건입니다. 도식 생성기의 정적 분석 통과는 도식 의미를 검증한 근거로 사용하지 않습니다. 공통 빌드 래퍼의 동적 경로 추가는 정적 분석기가 builder import를 해석하지 못했지만 실제 빌드와 네 절 검증은 통과했습니다. 하드코딩된 키, 광범위한 예외 삼키기, 비어 있는 fallback, 미완성 TODO·FIXME는 발견하지 못했습니다.

한국어 최종 감사 후 원본 해시·HTML 일치는 Part5 통합 단계에서 다시 확인합니다.

통합 담당 보충: 작성자가 설명 보완 뒤 필요한 재실행을 마쳐 위 수치를 최종 동결 출력으로 갱신했습니다. 실험 설계와 32개 코드 셀 범위는 동일하며 최종 전달 파일의 해시는 통합 기록에서 확인합니다.

독립 검토자의 최종 동결 재확인: 04절 code SHA-256 `fbc24b0065ed1cf8eaa726471072355c918786344da02dcd0c71ddf4abb20af9`, output SHA-256 `628f74110a04cad31a78e5bbd2aa190f5c38c496cc7bbc105240c792bf34de4e`. 출력 문자열 종류 수는 fixed 2/1/2, agent 2/1/2이며 재검증 판정은 APPROVE입니다.

통합 담당 최종 실행: 모든 함수 타입 주석을 보완한 뒤 01·02·04를 실제 챕터 가상환경과 notebooks 작업 폴더에서 재실행했습니다. 새 환경에는 ipykernel·nbclient·pip 개발 의존성을 고정했습니다. 01은 입력 370·출력 50토큰, 추정 0.000503달러·1.963초입니다. 02는 73·97토큰, 추정 0.00049125달러·1.356초입니다.

## 최종 환경·도식 재확인

독립 검토자는 최종 소스에서 ToolNode→model 되돌림, 오류 ToolMessage, count 기반 종료와 외부 recursion_limit, fixed/agent 합류 후 공통 ToolNode·answer를 확인했습니다. Excalidraw 원본에는 실제 rectangle·text·arrow 요소가 있으며 화살표는 절별 5·5·4·6개입니다. dev 고정 의존성과 uv lock --check도 통과했습니다.

낮은 우선순위 스타일 경고: 01·02 준비 셀의 typing.Any와 04 비교 셀의 ToolMessage가 사용되지 않아 Ruff F401 3건이 남습니다. 현재 실행 의미에는 영향이 없으며 완전한 lint 무경고 상태라고 보고하지 않습니다.
