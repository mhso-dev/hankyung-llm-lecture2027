# Part 6 Ch21~24 학습 순서 개정 기록

- 담당 범위: Ch21~24의 23개 절 `_src`와 대응 노트북 마크다운
- 개정 방식: 기존 실행 코드·출력·셀 ID·검증 메타데이터를 보존하고, 첫 사용 설명과 다른 상황·비교 경계를 코드 앞뒤에 보강합니다.
- 참고 노트북: `03_langgraph-agents/05_Agent_Development/03-Structured-Output.ipynb`, `06_Middleware/01-Middleware-Basics.ipynb`, `04_LangGraph_Advanced/04-Durable-Execution.ipynb`
- 공식 근거 확인(2026-09-14): LangChain Agents/Structured output/Middleware, LangGraph Persistence/Interrupts 문서 본문을 확인했습니다. 기준 설치 버전은 `langchain 1.4.0`, `langgraph 1.2.11`을 유지합니다.
- 출처: https://docs.langchain.com/oss/python/langchain/agents · https://docs.langchain.com/oss/python/langchain/structured-output · https://docs.langchain.com/oss/python/langchain/middleware/overview · https://docs.langchain.com/oss/python/langgraph/persistence · https://docs.langchain.com/oss/python/langgraph/interrupts

## 진행

- 2026-09-14: 23개 절의 기존 소스·노트북 구조, 첫 주제 코드와 마지막 비교 셀을 대조했습니다. 코드를 바꾸지 않는 산문 보강으로 진행합니다.
- 2026-09-14: 23개 `_src`의 핵심 개념에 「코드를 읽는 순서」를, 실행 예제에 「다른 상황과 적용 경계」를 추가했습니다. 대응 노트북은 실제 첫 주제 코드 앞의 기존 마크다운 셀과 마지막 비교 코드 앞의 기존 마크다운 셀에 같은 설명을 넣었습니다.

## 절별 보정 근거

| 절 | 첫 사용 전에 보강한 내용 | 기본 예제 뒤의 적용·비교 | 위치 |
| --- | --- | --- | --- |
| 21-01 | `@tool`의 이름·타입 힌트·독스트링, `create_agent` 생성과 `invoke` 실행 시점, 메시지 반환 | 주문 조회 적용, 고정 그래프와의 경계, 구조도와 실제 메시지 경로 구분 | `_src` b4/b5, NB 「도구와 에이전트 만들기」/마지막 관찰 셀 앞 |
| 21-02 | Pydantic 스키마·`Field`·`structured_response`, ToolStrategy와 ProviderStrategy의 강제 위치 | 상담 분류 적용, 자유문과의 경계, 메시지 수와 모델 호출 수 구분 | `_src` b4/b5, NB 「출력 스키마와 두 에이전트」/「메인 루프 메시지 확인」 |
| 21-03 | AgentState와 context의 저장 범위, `ToolRuntime` 주입, `invoke`의 state/context 입력 | 장바구니와 권한 분리, 답 문자열에 나타난 context와 상태 저장 구분 | `_src` b4/b5, NB 「상태와 실행 컨텍스트 정의」/「상태와 컨텍스트 구분」 |
| 21-04 | `inspect.signature`가 확인하는 범위, import·인자·반환 경계를 나누는 마이그레이션 순서 | 관찰 테스트를 먼저 고정하는 서비스 이전, 서명 존재와 제공자 지원의 경계 | `_src` b4/b5, NB 「현재 API 서명 확인」/「v1 최소 실행」 |
| 21-05 | retriever 입력·반환, 검색 도구 등록 시 모델이 얻는 선택권, SEARCH_LOG의 관찰 역할 | 주문 지원 적용, 고정 RAG와 Agentic RAG 선택 기준, 재검색 횟수와 품질 구분 | `_src` b4/b5, NB 「로컬 문서와 검색 도구」/「검색 결과가 없는 질문」 |
| 21-06 | 공통 평가 조건, `retrieve`의 입력·점수·반환, 사용량과 검색 이벤트 분리 | 고정/에이전트 경로의 적합 조건, 세 질문 결과의 일반화 한계 | `_src` b4/b5, NB 「Ch14 문서와 평가셋 읽기」/저장 셀 앞 |
| 21-06 추가 | Ch6의 `with_structured_output`을 실제 judge 코드 직전에 다시 설명하고, 구성 시점과 `grader.invoke` 호출·`Grade` 직접 반환을 Ch21-02의 에이전트 반환과 비교 | `bool` 형식 검증과 판정 정확성 분리 | `_src` b5, NB 「원문 기준 LLM 평가」 |
| 22-01 | 노드 훅과 랩 훅, `handler`의 입력·호출·반환, 루프 횟수에 따른 훅 반복 | 사용자 등급·재시도·도구 검사 배치, 업무 노드와 미들웨어 경계 | `_src` b4/b5, NB 「도구와 여섯 훅 trace 준비」/집계 셀 앞 |
| 22-02 | 직접 `mask_pii` 호출과 자동 미들웨어 경계, 입력/출력 적용 범위, mask의 한계 | 한국형 PII와 로그 경계, 마스킹·차단·권한 검사의 역할 구분 | `_src` b4/b5, NB 「Ch16 원본 마스킹 함수 재현」/적용 범위 비교 |
| 22-03 | 요약 트리거·요약 모델·전달 메시지, 저장 기록과 모델 입력의 차이 | 구조화 상태에 보존할 사실, 메시지 수와 토큰 수의 경계 | `_src` b4/b5, NB 「긴 대화 준비」/「압축 전후 비교」 |
| 22-04 | retry/fallback/call limit이 다루는 실패와 카운터, `retry_on`과 `handler` 실행 | 네트워크 오류·제공자 장애·논리 루프 적용, 결정적 모델 관찰 범위 | `_src` b4/b5, NB 「재시도 모델 준비」/정책 표 앞 |
| 22-05 | 예산 예약과 호출 전 차단, `wrap_model_call` 입력·처리·반환, 추정값과 실측 구분 | 사용자별 공유 저장·원자적 예약, 호출 횟수 제한과 예산 제한 비교 | `_src` b4/b5, NB 「After: 예산 미들웨어 작성」/비용 기록 앞 |
| 22-06 | 감사 사건 필드·해시·JSON 직렬화, 호출 시작/완료 구분 | 운영 감사 저장소와 PII 보존, 관측성 로그와 감사 로그 비교 | `_src` b4/b5, NB 「감사 미들웨어 작성」/기록 범위 해석 |
| 22-07 | 진입 훅의 순방향, 랩과 after 훅의 중첩·역방향, 완전 순서 검사 | 마스킹/감사·재시도/사용량 조합에서 순서가 정책을 바꾸는 사례 | `_src` b4/b5, NB 「태그 미들웨어 정의」/합성 표 앞 |
| 22-08 | 현재 모델 호출에 전달할 메시지를 고르는 격리 처리, 원상태 삭제와의 차이 | 주문·환불이 연결된 경우의 공통 context, 입력 격리와 접근 통제 비교 | `_src` b4/b5, NB 「업무가 섞인 메시지 준비」/상태 비교 앞 |
| 23-01 | checkpointer와 thread_id, compile과 invoke의 저장 시점, state/history 반환 | 사용자 ID와 대화 ID 구분, checkpointer와 Store 비교, 메모리 저장 범위 | `_src` b4/b5, NB 「그래프와 체크포인터 준비」/기록 비교 앞 |
| 23-02 | PostgresSaver 연결·스키마·`setup`, checkpoints와 checkpoint_writes | SQLite와 공유 DB 선택, 마이그레이션/실행 권한, URI 비밀과 운영 검증 경계 | `_src` b4/b5, NB 「접속과 그래프 준비」/After 앞 |
| 23-03 | SqliteSaver 연결 수명, 새 그래프 객체의 재개, `Annotated` 리듀서 | 서버 재시작과 새 상담 ID, 누적 리듀서와 덮어쓰기 비교 | `_src` b4/b5, NB 「파일 체크포인터 준비」/새 프로그램 재개 앞 |
| 23-04 | sync/async/exit 저장 시점, 자식 프로세스 종료와 SQLite 관찰 함수 | 결제와 배치 선택 사례, async 경합과 보장/관찰 범위 구분 | `_src` b4/b5, NB 「실험 함수 준비」/손실 범위 요약 |
| 23-05 | superstep 병렬 작업, pending write와 `snapshot.tasks`, `invoke(None)` 재개 | 병렬 문서 분석 적용, 외부 부작용의 별도 멱등성, 전체 롤백 오해 교정 | `_src` b4/b5, NB 「병렬 그래프 준비」/재개 앞 |
| 23-06 | 멱등성·operation_id, 노드 완료 전 종료와 재실행, worker 호출 흐름 | 결제·이메일의 고유 제약/원자적 삽입, 재시도와 멱등성 비교 | `_src` b4/b5, NB 「실제 중단과 재개 함수」/After 앞 |
| 24-01 | interrupt payload·checkpointer·thread_id·Command 반환, 노드 처음부터 재실행 | 위험 도구만 승인하는 정책, 승인 화면과 실제 부작용 순서의 경계 | `_src` b4/b5, NB 「승인 대상과 기록 파일 준비」/After 앞 |
| 24-02 | `Command(resume=...)` 값의 전달 위치, 허용값 검사와 재질문, interrupt 순서 | 주소 보정과 도구 인자 수정, 새 thread와 resume 차이, history count 해석 | `_src` b4/b5, NB 「입력 검증 노드 준비」/완료 앞 |
| 24-03 | `StateSnapshot.next`, `update_state`의 새 체크포인트, `invoke(None)` 분기 실행 | 임계값 재평가, reducer 주의, 그래프 분기와 외부 보상 비교 | `_src` b4/b5, NB 「가격 계산 그래프 준비」/분기 실행 앞 |

## 출처와 버전 대조

- LangChain Agents와 API reference에서 `create_agent`가 LangGraph 기반 그래프를 반환하고, 도구·상태·미들웨어를 연결하는 방식을 확인했습니다.
- Structured output 공식 문서에서 schema 직접 전달의 자동 전략 선택, 명시적 ToolStrategy/ProviderStrategy, 최종 `structured_response` 키를 확인했습니다.
- Middleware overview와 1.4.0 reference에서 노드 훅 4개와 랩 훅 2개, `handler`가 실제 호출을 제어하는 범위를 확인했습니다.
- LangGraph Persistence 공식 문서에서 thread/checkpoint, Store와 checkpointer 구분, pending writes, update_state의 새 체크포인트 동작을 확인했습니다.
- LangGraph Interrupts 공식 문서에서 checkpointer·thread_id 요구, JSON 직렬화 payload, Command resume 값, 노드 재시작과 interrupt 앞 부작용의 멱등성 규칙을 확인했습니다.
- 참고 노트북은 전개 깊이 비교에 사용했습니다. 해당 노트북의 “superstep 전체 롤백” 설명은 현재 공식 pending writes 설명 및 이 교재 Ch23-05의 실제 출력과 맞지 않아 가져오지 않았습니다.

## 초기 보강 단계의 실행 변경과 검증

- 초기 산문 보강 단계의 코드 변경: 없음. 23개 노트북의 코드 셀 source, output, execution_count, 코드 셀 metadata, 모든 cell id, 최상위 metadata를 개정 전 스냅샷과 비교해 모두 동일했습니다. 이후 독립 검토 반영으로 Ch22의 세 노트북 코드를 교정했으며 아래 단락에 따로 기록합니다.
- 초기 생성기 판정: `textbook/part6/_author_ch21_ch29.py`, Ch22/Ch23·24의 `qa/author_*.py`는 실행번호·출력·검증 메타데이터가 비어 있는 초기 집필 생성기입니다. 초기 산문 보강 단계에서는 정본을 덮어쓰지 않도록 실행하거나 수정하지 않았습니다. 독립 검토 후에는 Ch22·23 교정 내용을 각 장의 생성기 정의에도 반영했지만 생성기로 실행 완료 노트북을 덮어쓰지는 않았습니다. 공유 Ch25~29 파일에는 접근하지 않았습니다.
- 새 커널 실행: 코드가 바뀌지 않아 수행하지 않았습니다. 기존 검증 해시를 유지하고 공통 검증기로 정합성을 다시 확인했습니다.
- 빌드/검증: Ch21 6절·38셀, Ch22 8절·50셀, Ch23 6절·29셀, Ch24 3절·13셀. 각 장 `_build.py`와 `verify.py --chapter`를 실행했습니다.
- 독립 언어 감사: 작성자 자체 정독과 금지 표현 검색까지만 수행했습니다. 독립 검토는 root가 별도 담당합니다.
- 분량 변화: 태그 code를 제외한 `_src` 텍스트 기준 Ch21 +5,497자, Ch22 +5,937자, Ch23 +4,464자, Ch24 +2,220자로 합계 18,118자를 추가했습니다. 같은 문서적 문단을 반복 삽입하지 않고 절별 API와 관찰값에 맞추었습니다.
- 최종 국소 점검: Ch21-06의 늦은 첫 사용인 `with_structured_output`은 해당 judge 셀 바로 앞에 별도 설명을 두었습니다. Ch23-05는 참고 노트북의 “superstep 전체 롤백”을 따르지 않고 실제 pending writes 출력과 공식 문서에 맞춰 성공 작업 보존 범위로 설명했습니다. Ch23-04의 async 결과, Ch22-02의 PII 감지 범위, Ch22-04의 retry/fallback 결과는 이번 코드가 관찰한 범위를 넘어 일반화하지 않았습니다.
- 최종 빌드·공통 검증: Ch21 `PASS 6 sections / 38 code cells (max 16 lines)`, Ch22 `PASS 8 / 50 (max 24)`, Ch23 `PASS 6 / 29 (max 23)`, Ch24 `PASS 3 / 13 (max 24)`.

## 독립 검토 필수 지적 반영

- Ch22-01의 실제 API 프롬프트를 `LangChain 에이전트 미들웨어`로 한정했습니다. 새 커널 출력은 에이전트의 요청·응답·도구 호출을 검증·변환·기록·제어하는 중간 처리 계층으로 응답했고, 사용량은 입력 25·출력 57 토큰으로 기록됐습니다.
- Ch22-04의 폴백 설정을 `ModelFallbackMiddleware(backup)`으로 고쳐 최초 모델을 중복 등록하지 않았습니다. 새 출력 `primary_calls: 1 backup_calls: 1`로 최초 실패 한 번 뒤 보조 모델 응답 한 번이 실행됨을 검증했습니다.
- Ch22-05의 `reserved`는 한 `invoke`에서 초기화되지 않고 같은 `BudgetMiddleware` 인스턴스의 두 요청에 누적됩니다. HTML·노트북·생성기를 이 실제 범위에 맞게 고쳤으며, 다른 학습 주제인 도구 루프를 추가하지 않았습니다.
- 최종 잔여 검토에서 Ch22-05의 예외 문구도 실제 누적 범위와 맞추었습니다. 노트북과 생성기의 문구를 `이 미들웨어 인스턴스의 누적 예상비용 상한을 초과합니다.`로 고쳐 새 커널로 다시 실행했습니다. HTML 출력에도 같은 `BudgetExceeded` 문구가 표시됩니다.
- Ch22-06은 소금값과 메시지 길이만 해시하던 구현을 소금값과 실제 텍스트를 함께 해시하는 `fingerprint()`로 바꾸었습니다. `AA`와 `BB`처럼 길이가 같은 다른 텍스트의 지문이 각각 `6c1b4c4c81`, `f714e7ae49`로 다르게 출력되고 단언문을 통과함을 확인했습니다. `EVENTS`는 내용을 바꿀 수 있는 메모리 리스트이며, 짧은 해시가 익명화·위변조 방지·영구 보존을 제공하지 않는다는 한계를 명시했습니다.
- Ch22-02~07의 `ScriptedModel` 구현 앞에 이 모델이 훅 경계를 관찰하는 결정적 검사 장치이며 `BaseChatModel` 상속 구현은 학습 대상이 아니라는 설명을 추가했습니다.
- Ch22 여덟 절의 정리를 질문·목표·관찰문 복제에서 작동 원리·실제 검증값·적용 경계 세 문장으로 다시 작성했습니다. 절별 정리는 마스킹, 압축, 재시도·폴백, 예산, 감사, 합성, 입력 분리의 각각 다른 한계를 설명합니다.
- Ch23-04의 손실 범위 요약에서 실제로 출력하지 않는 데이터베이스 크기 주장을 삭제하고, 실제 셀이 표시하는 `completed`와 노드 호출 횟수로 고쳤습니다.

## 독립 검토 반영 후 실행 검증

- 새 커널 순차 실행: Ch22-01 `PASS 6 cells`, Ch22-04 `PASS 7 cells`, Ch22-06 `PASS 6 cells`. 최종 예외 문구 교정 후 Ch22-05도 별도로 재실행해 `PASS 6 cells`를 확인했습니다.
- HTML 재빌드: Ch22 8개 절, Ch23 6개 절을 새 노트북 출력과 교정한 `_src`로 다시 생성했습니다.
- 공통 검증기: Ch21 `PASS 6 sections / 38 code cells (max 16 lines)`, Ch22 `PASS 8 sections / 50 code cells (max 24 lines)`, Ch23 `PASS 6 sections / 29 code cells (max 23 lines)`, Ch24 `PASS 3 sections / 13 code cells (max 24 lines)`.
- 정적 검사: `author_ch22.py`와 `author_ch23_ch24.py` 문법 검사, 세 노트북의 JSON 형식 검사를 통과했습니다. `ModelFallbackMiddleware(primary, ...)`, 메시지 길이만으로 만든 해시, 변경 불가능한 `EVENTS`, Ch23-04의 데이터베이스 크기 출력 주장이 남지 않았음을 검사했습니다.
