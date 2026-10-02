# Part 6 Ch25~29 개정 기록

- 담당 범위: `textbook/part6/ch25-*`부터 `ch29-*`까지 `_src` 24절, 대응 노트북 24개, Ch28 초안 생성기
- 개정 기준: 핵심 API를 사용하기 전에 필요 이유, 호출 표기, 입력, 처리, 반환, 실행 시점을 설명하고 기본 예제 뒤에 다른 상황과 가까운 개념의 경계를 연결함
- 코드 변경: Ch26-01에 교재용 고정 환불 규정과 근거 검사를 추가하고, Ch26-02에서 사용하지 않는 모델·API 키 설정을 제거함. 두 노트북만 새 커널에서 다시 실행함
- 노트북 메타데이터: 코드를 바꾸지 않은 22개는 기존 실행 번호·셀 ID·출력을 보존했고, Ch26-01·02는 새 실행 출력과 검증 메타데이터를 저장함

## 절별 학습 보강

| 절 | 첫 사용 전 설명 | 기본 예제와 출력 해석 | 다른 상황·비교 경계 |
| --- | --- | --- | --- |
| Ch25-01 일곱 stream mode | HTML 4번과 NB `그래프 준비` 앞에서 `graph.stream(input, config, stream_mode)`의 세 입력, 반복 반환, `list()`가 즉시 소비를 늦추는 점을 설명함 | 기존 일곱 모드 사건 수와 `(mode, data)` 출력을 그대로 사용함 | 전체 상태 `values`, 변경분 `updates`, 화면 진행 `custom`, 답변 조각 `messages`의 소비자별 선택을 주문 상태 예로 비교함 |
| Ch25-02 토큰과 중간 진행 | HTML 4번과 NB `모델이 포함된 그래프` 앞에서 `get_stream_writer()`, `writer({...})`, 노드 반환값, `(message_chunk, metadata)`를 설명함 | messages 사건과 내용 조각 수, 이어 붙인 답과 최종 상태의 일치 출력을 해석함 | 채팅 말풍선, 단계 목록, 업무 진행률에 각각 어떤 사건을 써야 하는지와 진행률의 계산 근거를 구분함 |
| Ch25-03 TTFT와 total | HTML 4번과 NB `측정 그래프 준비` 앞에서 `perf_counter()`, first event, 내용 있는 첫 조각, total의 측정 위치를 설명함 | 세 독립 실행의 기존 시간·사용량 출력을 유지함 | custom 시작 알림과 첫 답변을 구분하고, 세 별도 호출로 모드의 속도 우열을 정할 수 없는 이유를 설명함 |
| Ch26-01 Subagent 도구 위임 | HTML 4번과 NB `전문 에이전트를 도구로 감싸기` 앞에서 `@tool`이 이름·docstring·타입으로 만드는 도구와 중앙→전문→중앙 호출 경계를 설명함 | 교재용 고정 환불 규정을 입력으로 제공하고 `tool_calls`, 함수 실행 기록, 규정 근거 문구를 검증함 | 결정 함수 도구와 판단형 서브에이전트의 사용 조건, 문자 수가 품질이나 토큰 절감을 증명하지 않는 범위를 비교함 |
| Ch26-02 Handoff | HTML 4번과 NB `활성 담당자 상태 정의` 앞에서 `active_agent`, `thread_id`, 체크포인터가 두 번째 입력의 누락 상태를 잇는 흐름을 설명함. 로컬 StateGraph만 사용하도록 모델·API 키 설정을 제거함 | 두 턴의 담당자 유지와 주문 번호 기반 종료 출력을 해석함 | 결과를 중앙에 반환하는 위임과 다음 턴 제어권을 넘기는 핸드오프를 구분하고 복귀 규칙의 필요성을 설명함 |
| Ch26-03 Router | HTML 4번과 NB `구조화된 분류` 앞에서 `with_structured_output(Route)`의 필요, 스키마 입력, 실제 모델 호출, 반환 객체를 설명함 | 선택 분야와 병렬 전문 결과 출력을 유지함 | 스키마 검증과 분류 정확성을 구분하고, 독립 작업만 병렬화할 수 있다는 선후 관계 경계를 설명함 |
| Ch26-04 구조 비교 | HTML 4번과 NB `호출 계측기 준비` 앞에서 `records`, `measured_call`, 업무 완료 값의 서로 다른 역할을 설명함 | 기존 세 구조의 호출·종료 기록을 유지함 | Subagent, Handoff, Router의 호출 역할과 실행 한도·업무 완료 조건의 차이를 설명함 |
| Ch27-01 하네스 | HTML 4번과 NB `단계 1` 앞에서 하네스의 뜻과 `inspect.getsource()`·`in source`가 확인하는 범위를 설명함 | 일곱 조립 경로의 True와 합계 7을 그대로 해석함 | LangGraph, LangChain agent, Deep Agents의 추상화 층과 기본 기능·선택 기능을 구분함 |
| Ch27-02 create_deep_agent | HTML 4번과 NB `단계 1` 앞에서 생성 함수의 반환값이 `CompiledStateGraph`이며 `invoke` 때 실행된다는 점과 메시지 순서를 설명함 | `course_lookup` ToolMessage와 최종 AIMessage 출력을 유지함 | 업무 도구와 하네스 도구, 모델 지침과 필수 궤적 검사의 경계를 설명함 |
| Ch27-03 플래닝 | HTML 4번과 NB `단계 1` 앞에서 `TodoListMiddleware`, `write_todos`, middleware 인자와 상태 저장을 설명함 | 기존 도구 호출과 todo 상태, 릴리스 수치 재계산을 구분함 | 여러 단계 작업의 계획과 한 단계 조회의 직접 호출을 비교하고 프롬프트 길이와 품질이 같은 측정값이 아님을 설명함 |
| Ch27-04 파일시스템 | HTML 4번과 NB `단계 1` 앞에서 `FilesystemBackend`, 가상 경로, `write_file`·`read_file` 반환과 실행 시점을 설명함 | 실제 파일 쓰기·목록·읽기 출력을 유지함 | 메시지 상태와 파일 인계의 장단점, 실행별 경로·출처·보존 정책을 설명함 |
| Ch27-05 오프로딩 | HTML 4번과 NB `단계 1` 앞에서 큰 도구 결과를 파일로 옮기고 ToolMessage에 미리보기와 경로를 남기는 과정을 설명함 | ToolMessage 길이와 파일 존재를 검증하고, 최종 답의 내용은 현재 출력이 입증하지 않으므로 해석 범위에서 제외함 | 메시지 뜻을 줄이는 요약과 원문 위치를 바꾸는 오프로딩의 손실·재읽기 경계를 비교함 |
| Ch27-06 서브에이전트 | HTML 4번과 NB `단계 1` 앞에서 `subagents` 사전, 부모의 `task` 도구, 동기 반환과 backend 공유를 설명함 | 부모 메시지의 task 호출·반환을 그대로 사용함 | 모호한 위임과 검증 가능한 완료 조건을 비교하고 도구·스킬·권한을 명시해야 하는 이유를 설명함 |
| Ch27-07 출처 검증 조사 | HTML 4번과 NB `단계 1` 앞에서 `source_lookup`이 웹 검색이 아닌 허용 자료 조회임과 주장-출처 추적을 설명함 | 제공 자료 두 건과 저장 보고서 출력을 유지함 | 제한 자료 조사의 재현성과 실제 웹 조사의 검색 누락·원문 열기·상충 비교 범위를 구분함 |
| Ch27-08 통합 실행 | HTML 4번과 NB `단계 1` 앞에서 권한이 도구 실행 직전에 판정되어야 하고 ToolMessage와 파일 존재를 함께 검사해야 함을 설명함 | 허용 보고서와 permission denied 결과를 그대로 사용함 | 최대 반복 수와 업무 완료 조건, 성공 답변과 실제 산출물의 경계를 설명함 |
| Ch28-01 MCP 구조 | HTML 4번과 NB `학생용 서버 불러오기` 앞에서 initialize 요청·응답·initialized 알림 순서와 capability의 뜻을 설명함. 첫 `async def`·`await`·`async with` 실행 앞에 코루틴 정의·호출·연결 정리 시점을 설명함 | 도구·리소스·프롬프트 발견과 실제 사용 출력을 유지함 | 실행 기능, URI 자료, 메시지 틀의 선택 주체와 부작용 경계를 도서관 예로 비교함 |
| Ch28-02 FastMCP 서버 | HTML 4번과 NB `Before: 등록하지 않은 함수` 앞에서 서버 객체, 데코레이터 등록 시점, 이름·docstring·타입의 변환을 설명함 | 미등록 목록·오류와 등록 후 목록·반환을 유지함 | Python 함수 존재와 MCP 공개 표면, tool·resource·prompt의 발견 경로를 구분함 |
| Ch28-03 전송과 권한 | HTML 4번과 NB `Before: 전체 환경 전달 확인` 앞에서 stdio 하위 프로세스, JSON-RPC, `env`의 전달 범위를 설명함 | 전체 환경과 선택 환경, 실제 stdio 호출 출력을 유지함 | stdio의 OS 권한과 HTTP의 TLS·인증·인가를 구분하고 로컬 연결도 실행 범위를 제한해야 함을 설명함 |
| Ch28-04 MCPAdapter | HTML 4번과 NB `MCPAdapter로 stdio 도구 발견` 앞에서 `async with`, `await list_tools`, BaseTool 변환, `ainvoke` 반환을 설명함 | 발견 도구의 이름·스키마·호출 결과와 직접 도구 비교를 유지함 | 호출 인터페이스가 같아도 배포·연결·장애 경계가 다름을 설명함 |
| Ch28-05 도구 정의와 토큰 | HTML 4번과 NB `직접 도구와 소형 MCP 서버 준비` 앞에서 `bind_tools`, `tool_choice`, 첫 AIMessage, usage, `schema_chars`를 설명함 | 기존 세 조건의 스키마 문자 수와 입력 토큰 출력을 유지함 | MCP 자체와 도구 정의 개수·내용을 분리하고, 도구 필터링과 서버 인가의 역할을 구분함 |
| Ch29-01 세 평가 전략 | HTML 4번과 NB `환경 준비` 앞에서 평가 함수가 최종 메시지·한 tool_calls·전체 메시지 중 무엇을 읽는지와 `trace()`가 고정 입력 생성기임을 설명함 | 정상·낭비 궤적의 답과 호출 수 출력을 유지함 | 사실성, 필수 단계, 금지 행동, 효율을 한 점수로 대신할 수 없는 사례를 설명함 |
| Ch29-02 네 매칭 모드 | HTML 4번과 NB `환경 준비` 앞에서 평가 함수 생성·호출·사전 반환과 동등성/포함 관계를 설명함 | reversed·short·extra의 기존 True/False 출력을 유지함 | subset과 superset의 방향을 문장으로 풀고, 순서 안전 조건·금지 도구·필수 도구 규칙 조합을 설명함 |
| Ch29-03 LLM judge | HTML 4번과 NB `환경 준비` 앞에서 평가 함수, 실제 judge 모델 호출, actual/reference 입력과 사전 반환을 설명함 | 동일 고정 궤적의 strict와 judge 출력을 유지함 | 결정적 규칙과 의미 판단의 역할을 구분하고, 동일 궤적 예제가 다른 경로 비교를 증명하지 않는다고 명시함 |
| Ch29-04 운영 지표 | HTML 4번과 NB `환경 준비` 앞에서 공통 열 변환, 서로 다른 final_score 원척도, trace_source를 설명함 | Ch18·Ch21의 저장 기록과 평균·p95 출력을 유지함 | 표본 세 건의 nearest-rank p95가 최댓값이 되는 이유와 서로 다른 과제의 직접 우열 비교 한계를 설명함 |

## 조사 근거

- LangGraph Streaming: <https://docs.langchain.com/oss/python/langgraph/streaming> — 2026-09-14 본문 확인. `values`, `updates`, `messages`, `custom`, `checkpoints`, `tasks`, `debug`의 반환 범위를 대조함.
- LangGraph Functional API: <https://docs.langchain.com/oss/python/langgraph/use-functional-api> — 2026-09-14 본문 확인. `get_stream_writer`와 복수 stream mode 사용을 대조함.
- Deep Agents Subagents: <https://docs.langchain.com/oss/python/deepagents/subagents> — 2026-09-14 본문 확인. 동기 위임, 부모 문맥 격리, 사용자 정의 서브에이전트 설정 경계를 대조함.
- Deep Agents Backends: <https://docs.langchain.com/oss/python/deepagents/backends> — 2026-09-14 본문 확인. backend와 가상 파일시스템 경계를 대조함.
- Deep Agents Permissions: <https://docs.langchain.com/oss/python/deepagents/permissions> — 2026-09-14 본문 확인. 내장 파일 도구 권한의 적용 범위를 대조함.
- MCP Specification: <https://modelcontextprotocol.io/specification/2025-06-18> — 2026-09-14 본문 확인. tools/resources/prompts와 capability, 사용자 동의 원칙을 대조함. 교재 정본의 기준 사양 링크는 2025-11-25이므로 기존 기준을 변경하지 않음.
- LangSmith Trajectory Evals: <https://docs.langchain.com/langsmith/trajectory-evals> — 2026-09-14 본문 확인. subset·superset 방향과 도구 인자 비교 범위를 대조함.
- 참고 노트북: `01_llm-agent-scratch/04_02_parallel.ipynb`, `01_llm-agent-scratch/03_routing.ipynb`, `02_langchain-basics/08_Evaluation/05-LangSmith-Heuristic-Evaluation.ipynb`를 읽음. 개념→차이→예제→한계의 전개 깊이만 참고하고 오래된 모델명, 단가, 일반화된 지표 권고는 가져오지 않음.

## 생성기 처리

- Ch27 `qa/author_ch27.py`는 기존 파일이 있으면 중단하는 초기 초안 생성기입니다. 검토 후의 핵심 설명, 절별 주의 사항, 정리 문장, 노트북의 국소 설명을 생성 데이터에 동기화했습니다.
- Ch28 `qa/author_ch28.py`도 검토된 정본과 실행 메타데이터를 덮어쓰지 않도록 기존 보호를 유지했습니다. 첫 비동기 문법 설명과 단계별 입력·반환값 설명을 생성 데이터에 동기화했습니다.
- Ch25, Ch26, Ch29에는 본문·노트북 정본을 생성하는 Python 생성기가 없습니다.

## 검증

- 24개 `_src` 모두 개정 전 백업과 달라졌습니다.
- 24개 노트북의 핵심 설명을 실제 API·코드가 처음 나오는 셀 앞으로 옮기고, 후속 첫 사용 구문에도 입력·처리·반환값 설명을 추가했습니다.
- 코드를 바꾸지 않은 22개 노트북은 기존 실행 출력을 보존했습니다. Ch26-01·02는 새 커널에서 각각 `PASS 4 cells`, `PASS 6 cells`를 확인했습니다.
- Ch25 빌드 성공, `PASS 3 sections / 13 code cells (max 25 lines)`.
- Ch26 빌드 성공, `PASS 4 sections / 23 code cells (max 22 lines)`.
- Ch27 빌드 성공, `PASS 8 sections / 36 code cells (max 17 lines)`.
- Ch28 빌드 성공, `PASS 5 sections / 22 code cells (max 25 lines)`.
- Ch29 빌드 성공, `PASS 4 sections / 24 code cells (max 12 lines)`.
- 총 24절, 118개 코드 셀을 검증했습니다.
- 소스 HTML 영문 토큰 기준 증분: Ch25 +495, Ch26 +612, Ch27 +1,016, Ch28 +650, Ch29 +514. 이 수치는 분량 통과 기준이 아니라 실제 개정 범위를 확인하는 보조값입니다.

## 자가 검토

- API가 실행되는 시점과 객체를 만드는 시점을 구분했습니다.
- 상태 변경, 화면 출력, 함수 반환, 도구 메시지를 같은 결과로 서술하지 않았습니다.
- 고정 예시·제공 자료·실제 모델 호출·저장된 운영 기록의 관찰 범위를 구분했습니다.
- `with_structured_output()`은 Ch26-03 노트북의 첫 호출 전에 필요, 스키마, 반환 객체, 실제 실행 시점을 설명했습니다.
- 새 설명에서 비용 부연을 추가하지 않았습니다. 비용 자체가 학습 목표인 Ch26-04와 Ch28-05의 기존 실행은 보존했습니다.
- 독립 검토 F1~F10을 모두 반영했습니다. Ch27의 반복 비용 문단을 제거하고 파일을 다루는 절에만 경로·권한 주의를 남겼습니다. Ch29-01·02·04의 로컬·저장 기록 실습에서 모델 호출 비용·변동 설명을 제거했습니다.
- 코드 블록과 출력은 언어 검수 대상에서 제외했습니다. 독립 한국어 감사와 시각 검토는 root 담당이므로 아직 완료로 표시하지 않습니다.

## 최종 독립 검토 반영

- Ch26-01은 중앙 기록 639자와 고객 질문 38자의 범위를 분리했습니다. 전문 입력은 질문에 `TRAINING_POLICY`를 결합한다는 사실을 본문·노트북·복습 문제에 맞췄고, 반복되던 정리 문장은 문자 수 비교가 토큰 절감이나 답변 품질을 입증하지 않는다는 관찰 한계로 바꿨습니다.
- Ch27 생성기의 `DETAILS`, `REVIEWED_CORE_HTML`, `REVIEWED_STEP_MARKDOWN`을 정본과 동기화했습니다. Ch27-05는 최종 답변을 출력하거나 검사하지 않았다고 서술하고, Ch27-07은 입력 2,379·출력 34·합계 2,413토큰으로 맞췄습니다.
- Ch27-08은 학습 목표·핵심 개념·도식·노트북 설명을 권한 규칙, 허용 파일, 거부 ToolMessage, 차단 파일 부재, 종료 판정 범위로 한정했습니다. 이번 실습은 사용량을 집계하지 않는다고 명시했습니다.
- Ch28-02는 실제 출력 범위를 도구·리소스·프롬프트 목록으로 한정하고 입력 스키마를 출력하지 않는다고 밝혔습니다. Ch28-03은 실제 코드의 `server_config` 사전이 `MCPAdapter(server_config)`에 전달되는 흐름으로 설명했습니다.
- Ch29-04는 별도 JSON 파일이 아니라 Ch18 실행 노트북에 저장된 stream 출력에서 표의 행을 추출한다는 실제 동작으로 설명을 고쳤습니다.
- Ch27 생성 함수의 임시 HTML·노트북 결과에서 Ch27-08의 권한·정지 설명이 정본과 일치함을 확인했습니다. Ch27·Ch28 생성기와 Ch27 도식 생성기는 `py_compile`을 통과했습니다.
- 최종 재빌드 뒤 Ch25 3절/13셀, Ch26 4절/23셀, Ch27 8절/36셀, Ch28 5절/22셀, Ch29 4절/24셀을 다시 검증했습니다. Part6b 전체 24절·118개 코드 셀이 통과했습니다.
