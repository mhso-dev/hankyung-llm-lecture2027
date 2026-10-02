# Part 4 Ch 13~16 집필용 공식 자료 조사

- 확인일: 2026-09-10 (KST)
- 대상: Ch 13 LangGraph 기초, Ch 14 RAG 패턴 확장, Ch 15 평가 심화, Ch 16 가드레일·안정화
- 조사 방법: LangChain/LangSmith/OpenAI/OWASP의 현재 공식 문서를 우선하고, 패턴의 원전은 저자 공개 논문으로 확인했다. 논문 성능 수치는 해당 데이터셋·모델·실험 설정의 결과일 뿐 이 교재 말뭉치의 결과가 아니다.
- 연결 기준: Part 3의 정본은 `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl`의 질문·정답 문서 ID와 `labs/part3/ch12-retrieval-tuning/runs/`의 실행 기록이다. Ch 12의 생성 스모크 테스트 `advanced-continuity-20260910T020805-integrated-01`은 검색 결과·출처·응답·총 소요 시간만 남겼고 생성 품질은 `not_evaluated`다. Ch 15가 이 빈칸을 채운다.

## Ch 13 — LangGraph v1의 그래프 API

### 설치 가능한 기준 버전

`langgraph==1.2.0`은 PyPI에 배포된 wheel(`langgraph-1.2.0-py3-none-any.whl`, 2026-05-12)이며 Python `>=3.10`을 요구한다. 따라서 과정의 Python 3.12 기준에서 설치할 수 있다. 확인 시점 최신 1.2 계열은 1.2.11이다. 교재 실행은 재현성을 위해 `uv add 'langgraph==1.2.0'`처럼 기준 버전을 고정하고, 실제 lock에 해석된 의존성까지 남긴다. 최신판을 무조건 설치하는 명령은 교재의 기준 버전을 바꾼다.

- [PyPI langgraph 1.2.0](https://pypi.org/project/langgraph/1.2.0/) — 배포물·업로드일·Python 요구사항
- [PyPI langgraph](https://pypi.org/project/langgraph/) — 확인 시점 최신 공개 버전
- [LangGraph 설치](https://docs.langchain.com/oss/python/langgraph/install) — base 패키지와 provider 패키지를 별도로 설치하는 공식 안내
- [LangGraph v1 마이그레이션](https://docs.langchain.com/oss/python/migrate/langgraph-v1) — v1에서 `create_react_agent`는 deprecated, `MessageGraph`는 메시지 키가 있는 `StateGraph`로 대응
- [LangGraph 1.2.0 LICENSE](https://github.com/langchain-ai/langgraph/blob/1.2.0/LICENSE) — MIT 라이선스. 공식 예제를 그대로 복사하지 않고 과정의 RAG 데이터·함수명으로 다시 작성한다.

### 절에서 확정해도 되는 동작

|개념|공식 API가 보장하는 범위|Ch 13에서 보일 최소 형태|주의점|
|---|---|---|---|
|`StateGraph`|상태 스키마, 노드, edge를 만들고 `compile()`한다. 노드는 상태를 읽고 **update를 반환**한다.|Part 3의 `retrieve → rerank → generate`를 각 노드로 옮기고 `START`·`END` edge를 잇는다.|노드 안에서 입력 state를 직접 변경하는 설명을 쓰지 않는다.|
|리듀서|같은 state key로 들어오는 update를 결합한다.|검색 결과·로그처럼 병합할 목록은 `Annotated[..., operator.add]` 등 명시한 결합 규칙을 둔다.|병렬 경로에서 순서에 따라 값이 달라지는 리듀서나 외부 부작용을 넣지 않는다.|
|`add_messages`|메시지 목록에 추가하고, 메시지 ID가 같으면 갱신하는 내장 reducer다.|대화형 질의 재작성 절의 `messages`에만 사용한다.|RAG 문서 목록의 일반 병합 reducer로 소개하지 않는다.|
|조건부 edge|함수 반환값으로 다음 노드를 고른다.|점수·빈 검색 결과 같은 **학생이 정한 if 조건**으로 분기한다.|이 Ch에는 모델이 목적지를 고르는 agent loop·`ToolNode`·`create_agent`를 넣지 않는다.|
|`Send`|조건부 edge가 실행 시점에 정한 수만큼 node와 node별 state를 보낼 수 있는 map-reduce API다.|질의 분해 뒤 하위 질문별 검색을 fan-out하고 결과를 reducer로 합친다.|fan-out 수 상한과 하위 state의 입력 형식을 코드로 고정한다.|
|`Command`|한 노드 반환에서 state update와 `goto`를 함께 표현한다.|검사 노드가 `quality`를 갱신하고 `retry` 또는 `generate`로 이동한다.|단순한 조건부 edge로 읽히는 예제를 억지로 `Command`로 바꾸지 않는다.|

[Graph API 공식 안내](https://docs.langchain.com/oss/python/langgraph/use-graph-api)는 `Send`를 map-reduce용 동적 분기로, `Command`를 update와 이동을 합친 반환값으로 설명한다. `add_messages`의 목록 추가·ID별 갱신 동작도 이 문서에서 확인했다. 시각화는 컴파일된 그래프의 구조를 확인하는 도구이며, 노드 함수가 실제로 맞게 동작한다는 실행 증거를 대신하지 않는다.

## Ch 14 — 직접 구현하는 RAG 패턴의 범위

패턴 이름은 구현 범위를 숨기지 않는다. 아래의 “직접 구현”은 Python 함수와 고정된 조건부 edge를 뜻한다. 모델이 검색·재시도·종료를 자율적으로 결정하는 agent는 Part 5 이후 범위다. 모든 변형은 Part 3의 원 질문, `doc_id`/`chunk_id`, 동일한 질의셋·평가 정책을 보존하고, 원 질문 baseline과 **한 변경만 다른** 실행 행으로 비교한다.

|패턴|최소 알고리즘|교재에 필요한 경계|1차 근거|
|---|---|---|---|
|다중 질의(Multi-Query)|원 질문에서 제한된 수의 검색용 변형을 만든 뒤 각각 검색하고 `doc_id` 중복을 제거해 후보를 합친다.|변형 질의와 각 검색 결과를 로그로 남긴다. 변형 문장은 근거 문서가 아니며 답변 인용에 쓰지 않는다.|다중 질의는 단일 표준 사양이 아니므로 구현 계약을 교재가 명시한다.|
|질의 분해|복합 질문을 2~N개의 하위 질문으로 나누어 각각 검색하고 후보를 병합·재정렬한다.|다중 단계 질문에만 적용한다. max 하위 질문 수, 병합 규칙, 빈 하위 결과를 고정한다. 원 질문도 함께 검색해 고유명사·날짜·부정 조건이 사라지는지 확인한다.|[Question Decomposition for RAG](https://arxiv.org/abs/2507.00355) — 분해→하위 검색→병합 후보 재정렬 구조|
|Step-back|구체 질문에서 상위 원리·정의 질문을 하나 만든 뒤, 원 질문과 함께 검색한다.|상위 질문이 원 질문을 대체하면 안 된다. 두 결과를 RRF 등 명시한 규칙으로 합치고 원 질문만의 baseline과 비교한다.|[Step-Back Prompting](https://arxiv.org/abs/2310.06117) — 구체 사례에서 상위 개념을 유도하는 프롬프팅|
|HyDE|가상의 관련 문서를 생성해 **검색용 임베딩**만 만들고, 그 벡터로 실제 말뭉치를 검색한다.|가상 문서의 허구 내용을 답변·인용·정답으로 사용하지 않는다. 생성 호출 한 번의 토큰·지연을 별도 기록한다.|[HyDE](https://arxiv.org/abs/2212.10496) — 가상 문서를 임베딩한 뒤 실제 코퍼스 이웃을 검색|
|CRAG식 폴백|검색 결과 품질 점수와 임계값을 비교해 그대로 생성·재검색·거부 중 하나로 간다.|원 CRAG의 학습된 retrieval evaluator, 웹 검색 확장, 문서 decompose-then-recompose를 이 실습이 자동으로 재현한다고 쓰지 않는다. 이 절의 고정 임계값 분기는 **CRAG에서 영감을 받은 단순화**다.|[CRAG](https://arxiv.org/abs/2401.15884) — retrieval evaluator와 confidence별 action|
|Self-RAG식 근거 검사|생성 후 응답 주장과 검색 문서의 관계를 검사해 통과·재검색·거부를 if로 정한다.|원 Self-RAG는 reflection token을 생성하도록 학습한 모델 프레임워크다. 사후 judge/임계값 검사는 **Self-RAG 자체의 재현이 아니라 영감 받은 검사**라고 쓴다.|[Self-RAG](https://arxiv.org/abs/2310.11511) — on-demand retrieval와 reflection token 기반 학습|
|RAPTOR|문서 청크를 묶고 요약·임베딩해 계층을 **색인 시점에** 만들고, 질의 때 여러 계층에서 검색한다.|요약 생성의 비용·지연·오류는 온라인 검색 비용과 분리한다. 이 교재에서는 작은 말뭉치의 구조를 보여 주며, 원 논문의 모든 clustering·tree traversal을 재현한다고 주장하지 않는다.|[RAPTOR](https://arxiv.org/abs/2401.18059) — cluster→summary→tree와 다층 retrieval|

### 공통 실험 계약

각 행에 `run_id`, 원 질문과 변형 질문, pattern/version, 모델·프롬프트·temperature, 질의 수·fan-out 상한, candidate/window·merge·rerank 정책, `corpus_fingerprint`, `query_fingerprint`, 검색 단계와 생성 단계의 토큰·비용·시간을 기록한다. Ch 11의 `Recall@50`, `Precision@5`, `nDCG@5`는 검색 후보/순위의 변화만 말한다. 생성 답변의 정확성·근거성은 Ch 15에서 별도로 평가한다. 패턴을 더하면 호출 수와 전달 문맥이 늘 수 있으므로, 동일 조건에서 지연·비용·품질을 함께 관찰해야 한다.

## Ch 15 — judge, trace, 회귀

### LangSmith RAG 평가자의 reference 경계

|평가자|비교 대상|reference answer 필요 여부|Ch 11·12에서 가져올 자료|
|---|---|---|---|
|Correctness|응답 vs 정답 답변|필요|사람이 작성·검토한 answer reference. `gold_doc_ids`만으로 대체하지 않는다.|
|Relevance / Helpfulness|응답 vs 사용자 질문|불필요|질문·응답|
|Groundedness / Faithfulness|응답 vs 검색 문서|불필요|실제로 generation node에 전달한 문서·응답|
|Retrieval relevance / Document relevance|검색 문서 vs 질문|불필요|질문·retrieved 문서. Ch 11의 `gold_doc_ids`가 있으면 규칙 기반 retrieval 지표도 병행한다.|

[LangSmith RAG 평가 튜토리얼](https://docs.langchain.com/langsmith/evaluate-rag-tutorial)은 Correctness만 ground-truth reference를 요구하고, 나머지 셋은 각각 질문 또는 retrieved docs와 비교한다고 명시한다. 현재 [평가 접근 문서](https://docs.langchain.com/langsmith/evaluation-approaches)는 동일 범주를 `Answer correctness`, `Answer helpfulness`, `Answer faithfulness`, `Document relevance`라고도 부른다. 절에는 대응 관계를 함께 써 UI·프롬프트 이름 차이를 오류로 오해하지 않게 한다.

trace는 최종 답만 저장하는 로그가 아니다. [중간 단계 평가 문서](https://docs.langchain.com/langsmith/evaluate-on-intermediate-steps)는 retrieval child run과 generation child run을 나누어 평가하는 방법을 제시한다. 따라서 `rewrite`, `retrieve`, `rerank`, `context_select`, `generate`, `judge`를 구분한 child run 또는 동등한 구조의 로컬 JSONL 행을 남긴다. `doc_id`, `chunk_id`, rank/score, 전달 문맥 hash·길이, 거부/폴백 reason도 있어야 실패를 읽을 수 있다.

### judge와 관측 지표의 고정

- judge 모델 ID·공급자·모델 release/날짜, system prompt와 rubric의 해시, temperature, structured-output schema, dataset·corpus fingerprint를 experiment metadata에 고정한다. “같은 judge”라는 이름만으로는 재현 조건이 되지 않는다.
- LLM judge 결과는 측정값이지 정답 보증이 아니다. [MT-Bench / Chatbot Arena 연구](https://arxiv.org/abs/2306.05685)는 position, verbosity, self-enhancement 편향을 검토했고, [self-preference bias 연구](https://arxiv.org/abs/2410.21819)는 GPT-4에서 자기 선호 관련 위험을 보고했다. 후보 순서를 바꾼 pairwise 검사, 판정 기준·출력 형식 고정, 소량의 사람 라벨과 agreement 기록을 함께 둔다.
- 요청 시작 시각 `started_at`, 첫 스트림 토큰 시각 `first_token_at`, 완료 시각 `ended_at`을 남긴다. `TTFT = first_token_at - started_at`, `total = ended_at - started_at`으로 계산해 한 값으로 섞지 않는다. percentile은 동일한 설정·질의 집합의 관측값에만 계산하고 표본 수를 같이 표시한다.
- [LangSmith LLM trace 문서](https://docs.langchain.com/langsmith/log-llm-trace)는 `input_tokens`, `output_tokens`, `input_token_details.cache_read`, `cache_creation` 같은 usage metadata와 TTFT 기록 방법을 설명한다. [비용 추적 문서](https://docs.langchain.com/langsmith/cost-tracking)는 input·output·cache read 등의 비용을 분리한다. 캐시 read와 creation, 모델별 가격표 변경일을 한 비용으로 뭉치지 않는다.
- 회귀 스위트는 Ch 12의 성공 사례만 모은 목록이 아니다. 검색 실패·부족한 후보·환각·문서 속 지시문 사례와 기존 성공 사례를 분리한 고정 집합이다. 기준선과 새 실행이 다른 입력/말뭉치/모델일 때는 점수 차이를 회귀라고 부르지 않는다.
- [OpenAI Batch API](https://developers.openai.com/api/reference/resources/batches)는 JSONL 요청을 비동기로 처리하며 현재 `24h` completion window와 50% 할인 조건을 명시한다. 그러므로 학생 대화의 즉시 응답 경로가 아니라, 재현 가능한 오프라인 judge/eval 묶음에서만 사용한다. Batch 결과도 요청별 `custom_id`, model version, prompt hash를 원 실행과 연결한다.

## Ch 16 — 직접 만드는 가드레일과 안정화

### 최소 정책과 실패 경계

|영역|직접 구현할 정책|단정하면 안 되는 것|
|---|---|---|
|입출력 검증|입력 길이·형식·허용 문자/스키마, 도구 인수 allowlist, 출력 구조/출처 형식을 결정적 코드로 검사한다.|프롬프트 한 줄이나 JSON schema만으로 악의적 입력이 모두 차단된다고 쓰지 않는다.|
|PII 마스킹|모델 호출·trace 전에 정규식/검증기로 후보를 redaction하고, 정책 버전·검사 결과·원문을 제외한 audit event를 남긴다.|정규식 기반 마스킹이 모든 개인정보를 찾아내거나, 오탐 없이 문맥을 보존한다고 보장하지 않는다.|
|히스토리|우선순위가 낮은 오래된 대화를 자르고, 필요한 사실은 별도 요약 record로 남긴다. 원문 메시지 ID·요약 모델·시각을 연결한다.|요약이 원 대화의 모든 조건·부정·출처를 보존한다고 가정하지 않는다.|
|예산|호출 전 최대 토큰/모델 단가를 이용해 reserve하고, 호출 뒤 actual usage로 정산한다. 상한을 넘으면 축소·거부·로컬 폴백처럼 정한 종료 경로로 간다.|총 비용이 항상 사전 추정과 같거나, retry가 무료라고 쓰지 않는다.|
|재시도·폴백|408/409/429/5xx 같은 transient 실패에만 최대 횟수·최대 경과 시간·지수 backoff+jitter를 적용한다. 영구 4xx/입력 검증 실패는 즉시 종료한다.|모든 오류에 재시도하거나, 쓰기/외부 행동을 idempotency 없이 반복하지 않는다.|
|감사 로그|`run_id`, 정책 version/decision, 모델/프롬프트 hash, token·cost·duration, 오류 코드, redact 여부와 최소한의 디버그 근거를 남긴다.|원문 PII, API key, 전체 대화·검색 문서를 기본 로그에 그대로 넣지 않는다.|
|프롬프트 인젝션|검색 문서는 신뢰할 수 없는 **data**로 분리한다. retrieved text를 명령으로 실행하지 않고, 외부 행동·권한을 최소화하며 민감 동작 전에는 결정적 검증을 둔다.|시스템 프롬프트만으로 문서 속 지시문을 완전히 무력화한다고 주장하지 않는다.|

[OWASP LLM01: Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)은 prompt injection이 direct/indirect channel에서 발생할 수 있고, 예방책은 영향을 줄이기 위한 완화책이라고 설명한다. Part 3의 문서 안 지시문 실패 사례는 Ch 16에서 이 **indirect 입력**으로 이어진다. 검색 문서를 신뢰 경계 밖 데이터로 분리하고, 출력 형식을 결정적 코드로 검사하며, 필요한 최소 도구만 허용하는 실습으로 연결한다.

[OpenAI Responses reference](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)는 `usage`의 cache read·write 세부 값과 `safety_identifier`에 해시한 사용자 식별자를 권장하는 현재 API 형태를 보여 준다. [데이터 제어 문서](https://developers.openai.com/api/docs/guides/your-data)는 Responses API·prompt cache의 보존 조건이 조직 설정과 API 옵션에 따라 달라짐을 명시한다. 따라서 trace/마스킹 예제는 특정 provider의 데이터 보존을 일반화하지 않으며, 실제 배포 전 해당 provider·조직의 현행 보존 정책을 다시 확인한다.

### Part 3 연결 시 주의할 점

- `gold_doc_ids`, `doc_id`, `chunk_id`, `retrieved`, `metrics_policy`는 Ch 11·12의 연결 계약이다. Ch 13~16이 field 이름이나 평가 단위를 바꾸면 이전 run과 직접 비교할 수 없다.
- `advanced-continuity-integrated-result.json`의 Q002 응답은 한 건의 generation smoke test다. 응답이 출처 표기를 했다는 사실은 확인할 수 있지만, 전체 생성 품질·안전성·지연 분포의 근거는 아니다.
- Ch 12의 dev/test 로그는 `chunk-candidate-unique-parent-macro-v1` 정책과 `corpus_fingerprint`·`query_fingerprint`를 남긴다. Ch 14의 패턴 비교도 같은 종류의 fingerprint, candidate/window, 반환 수를 남겨야 한다.

## 확인 필요 항목

- 실제 Part 4 실습을 실행하는 날에는 `uv lock` 결과, 사용 모델 ID·pricing, LangGraph와 LangSmith의 실제 해석 버전, OpenAI/다른 provider의 데이터 보존 설정을 다시 기록한다. 이 문서는 설치 가능성·현재 문서 기준을 확인한 자료이며 실행 결과가 아니다.
- judge 모델은 `[[미정: judge 모델]]` 상태다. 모델을 정하기 전에는 모델 간 우열·비용·사람과의 agreement 수치를 쓰지 않는다.
- PII 탐지 규칙의 적용 대상(한국 전화번호·이메일·주민등록번호·계정 ID 등)과 보존 기간은 실제 서비스의 개인정보 정책·법적 요구에 맞춰 별도 확정해야 한다.
