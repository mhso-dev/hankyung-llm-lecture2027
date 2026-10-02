# Ch 21 create_agent — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part6/ch21-create-agent`(절 여섯, 모두 experiment) · `labs/part6/ch21-create-agent`. Part 6의 첫 챕터이고 **Ch 20 바로 뒤**입니다. Part 6에서 먼저 끝난 챕터는 시범 Ch 22뿐입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본 46개) · `gates-before.json` · `before-manifest.json`(73개) · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch21-create-agent`.
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(§2·§2-7·§3·§5-3·§5-4·§6·§7·§7-2·§8) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 과정 요약(전부) · 계약 파일(§3 Ch17~20 줄·§4 Ch15~20 줄·§5 Ch16~20 줄·§8) · Ch 20 `chapter-summary.md`(전부, 특히 §13)·`chapter-lead-notes.md`·`before-manifest.json` · Ch 22 `_src`·노트북·`handoff.md` · Ch 29 04 노트북·`_src` · Ch 14 자료·도구 파일 · Ch 15·17·19·20 도구 파일 · Part 6 목록·묶음·검사 스크립트 · 옛 생성기 둘.
- **원고·노트북·그림은 하나도 고치지 않았습니다.** 파일 삭제 0건. 모델·임베딩 호출 0건. 노트북 실행 0건. 모델을 부르지 않는 확인만 했습니다(§5 — import, 설치판 소스 읽기, 모델 객체를 가짜 키 글자로 만들어 그래프 구조만 보기, `/tmp/ch21-prep/`의 작은 그래프로 `ToolRuntime` 주입 보기, 키는 `env -u OPENAI_API_KEY`로 뺀 채).
- `chapter.json` `hours` = 「총 16h · 강의 6h · 실습 10h」. 절 meta 합 강의 1 × 6 = **6h**, 실습 1.5 + 1.5 + 1.5 + 1.5 + 2 + 2 = **10h** → 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part6/_build_index.py` 19행 (6, 10)·`qa/check_scope.py` `EXPECTED` (6, 10)도 같습니다. 새 용어 meta 5 × 6 = **30**(용어 목록은 원고에 없음).

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-25)

| 절 | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 create agent와 ReAct 루프 | 6 | 72 | 4 | 4 | 0 | 0 | 7 | 28 | 3 | 46 |
| 02 구조화 출력 두 전략 | 5 | 76 | 1 | 1 | 0 | 0 | 6 | 28 | 3 | 39 |
| 03 AgentState와 context schema | 5 | 71 | 2 | 1 | 0 | 0 | 5 | 30 | 3 | 41 |
| 04 0x에서 1x로 마이그레이션 | 5 | 64 | 0 | 1 | 0 | 0 | 7 | 20 | 3 | 31 |
| 05 retriever를 도구로 전환 | 5 | 69 | 4 | 4 | 0 | 0 | 6 | 14 | 3 | 31 |
| 06 같은 평가셋으로 RAG 비교 | 12 | 85 | 26 | 0 | 0 | 1 | 13 | 20 | 3 | 63 |
| **합계** | **38** | **437** | **37** | **11** | **0** | **1** | **44** | **140** | **18** | **251** |

- 통과 절 **0/6**. 코드 줄(`count_code.py`) 39·33·35·30·35·107 = **279줄**. 여섯 노트북에 설치 셀(1줄)과 환경 셀(12줄, 06은 15줄)이 글자까지 같게 되풀이됩니다(06 환경 셀에만 `ROOT` 찾기와 `%pip install -q numpy`가 더 붙음).
- G1 37 = 제너레이터 식·내포식 33(06에 26) · 조건 표현식 1(05) · **조건 밖 클래스 정의 2(03 `SupportState(AgentState)`·`@dataclass UserContext`)**. 02 `PolicyAnswer(BaseModel)`·06 `Grade(BaseModel)`는 G1이 허용 모양으로 봄.
- G2 11 = 한 글자 이름 9(`m` 5·`x` 2·`k`·`v`·`w`) · 두 겹 넘는 호출 1(03 c8 `invoke(…, context=UserContext(…))` 한 줄) · 한 줄 복합문 1(04 c8 `for …: print(…)`).
- G3 0 — 그러나 첫 줄 주석 말고 **이유 주석이 0**입니다(38셀 모두 주석 한 줄뿐). 설치·환경 셀 주석 둘은 여섯 노트북이 같은 글.
- **G4 1은 06 `init_chat_model("openai:gpt-5.4-mini", reasoning_effort="none")`의 `temperature` 누락만 잡았습니다.** 01~05는 `create_agent("openai:gpt-5.4-mini", …)`에 **모델 이름 글자를 바로 넘겨** `temperature`·`reasoning_effort`가 **둘 다 없는데** G4가 모델 생성 셀로 보지 않아 놓쳤습니다(설치판 `langchain/agents/factory.py` 995~996행 — 글자면 `init_chat_model(model)`을 기본값으로 부름). 가짜 모델은 0.
- G5 44 = 절마다 `title_cell_missing`·`core_figure_attachment_missing` 12 + 결과 읽기 인용 없음 26 + 마지막 셀 뒤 결과 읽기 없음 6(결과 읽기 셀 자체가 0).
- G6 140 = 70자 초과 55 · 영문으로 시작해 조사가 붙은 문장 **85**. 금지어는 G6가 세지 않은 것이 많음(§1 표 금지어 열).
- G7 18 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 금지·미교육 문법 (AST로 따로 셈)

- **f-string 10곳**: 03 `f"{runtime.context.user_id}:{…}"`(**안에 속성 계산**) · 04 `f"{old:28} -> {new:28} | {note}"`(**형식 지정**, 과정 0건) · 05 `f"{k}: {v}"` · 06 다섯(`f"[{item['doc_id']}] {item['text']}"` 등 **모두 안에 계산**). Ch 13~20 기본 경로 f-string 0건.
- **타입힌트**: `@tool` 함수 넷 모두 반환 힌트 `-> str`(01·03·05·06, Ch 19·20은 `: str` 매개변수만 허용·반환 힌트 0) · 06 도움 함수 둘 `retrieve(query: str, top_k: int = 2) -> list[dict]`·`usage_total(messages: list) -> dict[str, int]` · 06 변수 힌트 `search_events: list[dict]`·`records: list[dict]` · 03 **`runtime: ToolRuntime[UserContext]`**(라이브러리가 읽는 힌트 — §5-3).
- **클래스**: 02 `PolicyAnswer(BaseModel)`(칸 셋 `Field(description=)`) · 03 **`SupportState(AgentState)`**(라이브러리 상태 형식 상속, 칸 하나) · 03 **`@dataclass class UserContext`**(과정 처음 — Ch 16은 `@dataclass` 없이 함) · 06 `Grade(BaseModel)`(`supported: bool`·`explanation: str`).
- **데코레이터**: 맨 `@tool` 넷(Ch 19 01 모양) · **`@dataclass` 하나(과정 0건)**.
- **처음 쓰면 풀어야 하거나 과정이 안 쓴 이름**: `[Path.cwd(), *Path.cwd().parents]`(별표 풀기, 여섯 노트북 환경 셀) · `next(… for … if …)`(06 환경 셀 `ROOT` 찾기·06 c20 정답 문서 찾기 — 규격 §2-3 금지 모양) · `enumerate(…, 1)`·`getattr`·`any`(01·05) · `sum(생성기)`(01·02·06) · `all`·`isinstance`(06) · `{**documents[index], "score": …}`(06 딕셔너리 풀기) · `np.argsort(scores)[::-1][:top_k]`(06 음수 걸음 슬라이스) · `/=`(06 배열 나눠 담기) · `statistics.mean`(06) · `type(agent).__name__`·`sorted(result.keys())`·`model_dump()`(01~03) · `inspect.signature`(04, 과정 처음) · `Path.read_text`·`write_text`·`mkdir(parents=True, exist_ok=True)`·`relative_to`(06 — 과정 파일 쓰기 관례는 `with open(…, "w")`+`json.dump`, Ch 15 08) · `IPython.display.Image`·`display`(01) · 튜플 한 줄 대입 `INPUT_USD_PER_MTOK, OUTPUT_USD_PER_MTOK = 0.75, 4.50`(01) · 숫자를 식에 바로 `tokens_in/1_000_000*…`(01).
- **셀 모양**: 06 c4 15줄(상한) · c10 `retrieve` 본문 5문장이지만 한 줄에 계산 셋 · c16 14줄 한 `for` 안에 요청 둘·시간 재기 넷 · c18·c22·c24 딕셔너리 한 줄에 칸 여덟~열셋(한 줄 200~400자) · 03 c6 한 셀에 클래스 둘 + 도구 하나 · 06 c20 클래스 + 판정 반복 한 셀 · 02 c6 클래스 + 에이전트 둘 + 입력 글 한 셀.

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청(이번 출력) | 손 값 | 금지 문법(셀) | 금지어(`_src` 본문 / 노트북 md / 코드 주석) | `assert`(무엇에) |
|---|---|---|---|---|---|---|
| 01 | 자료실 규정 딕셔너리 둘(대출 「일반 도서는 14일 동안 5권까지 대출할 수 있습니다.」·운영 「평일 09:00~20:00 운영합니다.」)을 한 줄로 찾는 `@tool lookup_policy(topic: str) -> str`(없는 주제는 딕셔너리 `KeyError`) → `create_agent("openai:gpt-5.4-mini", [lookup_policy], system_prompt="규정 도구를 사용해 근거가 있는 답만 하세요.")` → 종류 `CompiledStateGraph`·구조 문자열(상자 넷, **`tools -.-> model` 점선**) → **`draw_mermaid_png()`로 PNG 8,388바이트**(외부 렌더 서비스) → 대출 질문 invoke → 메시지 넷(Human · AI `lookup_policy {'topic': '대출'}` · Tool · AI) → 사용량 합 입력 379·출력 47·「추정」 0.000496 | **2**(+ 모델 아닌 외부 요청 1: mermaid.ink) | 규정 글 둘 · 요금 0.75·4.50(캐시 입력 칸 없음) · 질문 | c4 별표 풀기 · c6 반환 힌트·한 줄 딕셔너리 찾기 · c8 외부 렌더·`display` · c10 `enumerate`·`getattr`·제너레이터 `any`·`m`·튜플 풀기 · c12 내포식·제너레이터 `sum` 둘·`x`·한 줄 대입 둘·식 안 숫자 | 반환 10/3/0 · 지시 3/0/0 · 추정 3/0/1 · 경로 4/1/0 · 지연 1/0/0 · 인터페이스 2 · 실행기 1/1 · **제목 「create agent」·「ReAct」** | 5 — 키 있음 · PNG 서명(**외부 서비스 결과**) · ToolMessage 있음(**모델 선택**) · `"14"` in 답 글(**모델 글**) · 비용 < 1(**잰 값**) |
| 02 | 양식 클래스 `PolicyAnswer(BaseModel)`(topic·answer·source, `Field(description=)`) · 도구 없는 에이전트 둘 `response_format=ToolStrategy(PolicyAnswer)` / `ProviderStrategy(PolicyAnswer)` · 같은 입력 「자료 R-14에 따르면 일반 도서 대출 기간은 14일입니다. 구조화해 주세요.」 → `structured_response` · 메시지 3 vs 2, AI 메시지 1·1 · source `R-14` vs `자료 R-14` | **2** | 입력 글(R-14 자료 번호는 지어낸 값) | c6 클래스 + 에이전트 둘 한 셀 · c8 제너레이터 `sum`·`m`·튜플 풀기·칸 셋 딕셔너리 한 줄 | 스키마 15/7/1 · 검증 9/2/1 · 필드 6/3/1 · 네이티브 3 · 프로필 5/1 · 분기 1/1 · 반환 2/1 · 측정 1 · 지연 1 | 2 — `'R-14' in source and '14' in answer`(**모델 글**) · AI 메시지 ≥ 1 |
| 03 | `SupportState(AgentState)` + `request_tag: str` · `@dataclass UserContext(user_id, access_level)` · `@tool current_access(runtime: ToolRuntime[UserContext]) -> str` · `create_agent(…, state_schema=SupportState, context_schema=UserContext)` · `invoke(상태, context=UserContext("student-7", "read-only"))` → 결과 키 `['messages', 'request_tag']` · 답 글에 `student-7:read-only` | **2** | 태그 `lesson-03` · 사용자 값 둘 | c6 클래스 둘(G1)·`@dataclass`·제네릭 힌트·f-string 안 계산·반환 힌트 · c8 한 줄 두 겹 호출(G2)·`sorted(…keys())` | 로그 4 · 식별자 2/1 · 주입 3/1 · 의존 2/2 · 채널 1/1 · 필드 1 · 스키마 1 · 지연 1 · **제목 「AgentState」·「context schema」** | 2 — `request_tag == 'lesson-03'`(결정적) **and** `'read-only' in 답 글`(**모델 글**) · `'context' not in result`(결정적이지만 증거로 약함 — 결과 딕셔너리에 원래 없는 키) |
| 04 | `inspect.signature(create_agent)` 한 줄 출력(약 900자) + 여섯 인자 이름이 그 글자에 있는지 · 대응표 네 줄(`create_react_agent → create_agent` · `prompt → system_prompt` · 「response_format 별도 후처리 → response_format」 · 「Pydantic 사용자 상태 → TypedDict 기반 AgentState」) · 도구 없는 최소 에이전트 invoke 1 | **1** | 대응표 네 줄 · 질문 | c6 `inspect` · c8 f-string 형식 지정·한 줄 복합문(G2)·튜플 풀기 | v1 11/1/1 · 마이그레이션 3/2/1 · 0.x 2/2/1(md에 1.x 1) · 프롬프트 2 · 동적 2 · 지시 2 · 반환 2/1 · 경로 2/1 · 회귀·호환·이식 · **제목 「0x에서 1x로」(점이 빠짐) · 「마이그레이션」** | 2 — 인자 이름이 서명 글자에 있음(결정적) · 답 글이 비지 않음(**모델 글**, 약함) |
| 05 | 딕셔너리 `DOCS` 셋(대출·예약·운영) + 전역 목록 `SEARCH_LOG` + `@tool search_rules(query: str) -> str`(**임베딩 없는 낱말 겹침**: 주제어가 질문에 있거나 규정 글의 낱말 하나라도 질문에 있으면 걸림) · system_prompt 「결과가 없으면 다른 검색어로 한 번 재검색」 · 예약 질문 → 검색 1·답 「3일」 · 주차 질문 → 검색 둘 `['주차 요금', '주차료']`·없음을 설명 | **5**(예약 2 + 주차 3 — 주차 요청 둘이 한 응답이면 2, 노트북에서 셀 수 없음) | 규정 글 셋 · 질문 둘 | c6 내포식·조건 표현식·제너레이터·f-string·`k`·`v`·`w`·도구 안에서 전역 목록 바꿈 · c8 내포식·`m` | 지연 4 · 반환 3/3 · 경로 3 · 로그 2/1/1 · 거부 1/1 · recall 2 · 인터페이스 1/1 · 파이프라인 1 · 리트리버·retriever 4/3 · Agentic 3/2 · **제목 「retriever」** | 2 — `SEARCH_LOG and '3' in 답 글`(**모델 선택·모델 글**) · `SEARCH_LOG` 비지 않음(**모델 선택**) |
| 06 | Ch 14 `documents.json`(12)·`queries.json`(8) 읽기 → C01·C05·C07(차례 번호 `[0, 4, 6]`) · `OpenAIEmbeddings("text-embedding-3-small")` **기본 1536차원**(Ch 14는 `dimensions=256`)·단위 벡터로 나눔 · `retrieve(query, top_k=2)`(코사인, 상위 둘+점수) · 고정 흐름(검색 → `model.invoke(글)`) / 에이전트 흐름(`@tool search_documents` → `create_agent(model, …)`) · `perf_counter`로 흐름마다 걸린 초 · `usage_total` · 평가 모델 `with_structured_output(Grade, method="json_schema", strict=True)` 여섯 번 · `statistics.mean` 요약(「정확도」) · **`data/rag-comparison.json` 저장(Ch 29 04가 읽음)** | **23** = 모델 15(고정 3 · 에이전트 6 · 판정 6) + 임베딩 8(문서 묶음 1 · 표본 1 · 고정 3 · 도구 안 3) | 질문 번호 셋 · `top_k` 2 · 판정 요청 글 | G1 26 · c4 `next`·15줄·`%pip numpy`(판 없음) · c8 `/=` · c10 기본값 매개변수·힌트·딕셔너리 풀기·`[::-1]` · c12 변수 힌트·f-string 계산·전역 목록 · c16 f-string 계산 둘·14줄 · c18·c22·c24 한 줄 딕셔너리 · c20 `next`·클래스·f-string 계산 둘 · c22 `mean` | 경로 12/6/5 · 지연 9/3/3 · judge 11/0/1 · Agentic 7/3 · 반환 4/4/2 · gold 4/0/1 · 정확도 4/3 · 정답률 1/1 · trace 주석 2 · 분기·프롬프트·변동·측정 · 정규화 주석 1 · **제목 「RAG」** | 10 — 개수·모양·키(결정적) · 표본 질문 정답 문서가 앞 둘 안(임베딩 결과) · 에이전트 답 글이 비지 않음(**모델 글**) · 판정 `supported`가 `bool`(자료형) · 「정확도 ≥ 0」(늘 참) · 저장 파일 3줄 |

- **모델 요청 합계(노트북 한 번씩, 옛 출력 기준) 2 + 2 + 2 + 1 + 5 + 15 = 27번 + 임베딩 8번 = 서비스 요청 35번**, 모두 `gpt-5.4-mini`·`text-embedding-3-small`. 01은 모델이 아닌 외부 서비스(mermaid.ink)에도 한 번 요청합니다.
- **`temperature=0` 0곳, `reasoning_effort="none"` 한 곳(06)**. 01~05는 모델 이름 글자만 넘김(G4가 놓침). Ch 22(완료)는 `init_chat_model(…, temperature=0, reasoning_effort="none")`로 만든 **모델 객체**를 `create_agent(model, tools=[…], middleware=…)`에 넘깁니다.
- **비용**: 01만 자체 식으로 셈(캐시 입력 칸 없음, 말 「추정」 — Ch 18 금지어). 과정 표준은 Ch 6 06 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` 「예상 비용」. 06은 비용을 세지 않음.
- **걸린 시간**: 06만 잼(`perf_counter`, 흐름마다) — 옛 b6·확인할 점·Ch 29 04가 그 값을 결론·표에 씀. 01·05·07 b7 「지연」 문장은 재지 않은 절의 말.
- **`%pip` 셀**: 여섯 모두 `%pip install -q langchain==1.4.0 langchain-openai==1.6.0 langgraph==1.2.11 python-dotenv==1.2.3 pillow`(**pillow 판 없음, 노트북 import 0**) + 06 환경 셀 끝 `%pip install -q numpy`(**판 없음**). 실습 폴더 dev에 `pip==26.2`·잠금에 `pip 26.2` 있음(규격 §7-2 조건 충족). `pyproject.toml`의 `numpy>=2.0`·`pillow>=11.0`은 범위 표기(과정의 다른 챕터는 `==` 고정) — 잠금은 `numpy 2.5.3`·`pillow 12.3.0`.
- **옛 그림 토큰**: 절마다 b4 「도식 읽기」의 `{{svg:NN-흐름}}` 하나(상자 네다섯을 한 줄로 이은 흐름도, `figures/_gen_figures.py`가 `textbook/part5/_figure.py`로 만듦). 노트북 토큰은 모두 `{{notebook:slug}}`. Mermaid·삽화 0장. 옛 그림 02·06은 나란한 두 방법을 한 줄 차례로 그림(규격 §5-3 「두 방법 나란히 = subgraph 둘」과 어긋남), 01은 「도구 선택」을 모델 상자 하나로 따로 그림.
- 노트북 `metadata.verification`: 여섯 모두 `passed`, 실행일 **2026-09-10**(01 16:10:44 · 02 16:10:47 · 03 16:10:50 · 04 16:10:53 · 05 16:11:00 · 06 16:36:35 UTC). `code_sha256` 앞 12자 01 `3ea6bfde67a1` · 02 `2127cd333da9` · 03 `b49e74c21634` · 04 `10763fc23825` · 05 `ce458f85191e` · 06 `191040130f4d`. 노트북 파일 해시 `5fd9db0a…`·`cd124da5…`·`75b45df8…`·`0ba36d5e…`·`41253a8c…`·`0861f6e8…`(`part6-practice.zip` 안 판과 같음. `textbook/part6/qa/final-artifact-hashes.json`의 Ch 21 줄 45개 가운데 HTML·`_src`·노트북 18개는 이미 옛 값 — 기록 파일).
- 노트북 설명 셀: 제목 + 「새 커널에서 독립 실행」 한 줄 · 「패키지 설치」·「환경 준비」 · 소제목 한 줄 + `_src` b4·b5 둘째 단락과 같은 글(옛 도구 `part6a_enrich.py`가 끼움) · **결과 읽기 셀 0**, 「이 노트북에서 할 일」·준비물(호출 수·비용)·실행일 문장 없음, 셀 첨부 그림 0.
- `_src` 틀(옛 생성기 `_author_ch21_ch29.py`의 한 틀): b3 「필요한 자료와 객체는 노트북에서 다시 선언하므로 …」 여섯 절 같음 · b5 첫 단락 여섯 절 같음 · b6 첫 단락 = 확인할 점 = b8 둘째 줄(같은 글 세 번) · b7 둘째·셋째 줄 여섯 절 같음(「절당 1달러 미만」·「모델 문장과 지연이 달라질 수 있으므로」) · b8 「다음 학습과 이어지는 지점 — (슬러그)에서 이 결과를 다시 사용합니다」(틀 문장) · b9 복습 셋, 해설 한 줄 · b10 참고 자료 둘(여섯 절 같음, 확인일 2026-09-14).

## 2. 절별로 더 봐야 할 것

### 01 create agent와 ReAct 루프
- **Ch 22(완료) 01 b3가 기대는 장면**: 「Ch21 01절에서 에이전트가 반복하는 흐름을 봤습니다. 모델을 부르고, 모델이 요청하면 도구를 실행하고, 다시 모델을 부릅니다.」 → 01은 도구를 한 번 부르고 다시 모델을 부르는 실행을 유지해야 참입니다. Ch 20 01·05 b8(「Ch 21 01절은 … 반복 구조를 함수 `create_agent` 한 줄로」·「같은 되풀이 구조」)도 같습니다.
- **구조 문자열 차이(Ch 20 인계 2)**: 설치판 `create_agent`는 `model`·`tools` 노드를 만들지만 갈래는 자체 조건 함수(`_make_model_to_tools_edge` — 도구 호출 요청마다 `Send("tools", [요청])`)와 `_make_tools_to_model_edge`(기본은 모델로, `return_direct` 도구나 양식 도구면 끝으로)로 적어 **되돌아가는 엣지가 조건부 엣지라 점선**입니다(`factory.py` 1672~1735·1923~1975·2004~2037행). `tools_condition`은 가져오지 않습니다(28행 `ToolNode`만). 「상자 넷·엣지 넷」은 Ch 20과 같고, 실선/점선과 조건 함수는 다릅니다.
- **`draw_mermaid_png()`는 기본값이 공개 서비스 mermaid.ink로 보내는 외부 요청**입니다(`langchain_core/runnables/graph.py` 639행 `draw_method=MermaidDrawMethod.API`, `graph_mermaid.py` 423행). 키 없는 학생·오프라인·서비스 장애에서 셀이 멈추고, PNG 바이트 수(8,388)는 서비스 판에 따라 바뀔 수 있습니다. Ch 13·20은 `draw_mermaid()` 글자만 썼습니다.
- **`lookup_policy`가 없는 주제에서 `KeyError`**: `create_agent`가 만드는 `ToolNode`는 `handle_tool_errors` 기본값(`factory.py` 1089행 인자 없음)이라, Ch 20 02 확인대로 도구 몸통의 `KeyError`는 도구 메시지로 바뀌지 않고 올라올 것입니다(이번에 실행하지 않음). 모델이 `'대출 기간'`처럼 다른 주제어를 만들면 셀이 멈춥니다.
- **요청 수 셈 조건(Ch 20 인계 7)**: `create_agent`에는 `bind_tools(…, parallel_tool_calls=False)`를 줄 인자가 없습니다(모델 설정은 미들웨어의 `ModelRequest.model_settings` — Ch 22 몫). `model.bind(parallel_tool_calls=False)`를 넘기면 **그래프는 만들어지지만**(확인) 호출 때 동작은 확인하지 않았습니다. 요청 수 셈은 「요청을 하나씩 받았을 때」로 한정하거나 첫 실행에서 확인할 몫.
- 소재: 규정 글이 Ch 20 `POLICIES`(「1인 5권까지 14일 동안」·토요일 10:00~17:00·연체)와 다름(Ch 20 인계 4). Ch 22 `lookup_hours`는 Ch 20 글과 같은 운영 시간(평일 09:00~20:00·토요일 10:00~17:00).

### 02 구조화 출력 두 전략
- **도구가 없는 에이전트**라 되풀이가 거의 없습니다. ToolStrategy 그래프는 `model` 하나 + **`model → model` 조건부 엣지**(양식 검사 실패 때 다시 요청 — `handle_errors` 기본 `True`), ProviderStrategy는 `model` 하나(§5-2 확인).
- 메시지 3(ToolStrategy: Human · 양식 도구 요청 AI · 도구 메시지 「Returning structured response: …」 — `factory.py` 1263행) vs 2는 **첫 요청에서 양식이 맞았을 때의 결정적 구조**입니다. 검사 실패로 다시 요청하면 늘어납니다(이번 출력에는 없음).
- **자동 선택**: 양식 클래스를 그대로 넘기면 모델 프로필(`gpt-5.4-mini` 프로필 `structured_output: True`)을 보고 ProviderStrategy를 고릅니다(`factory.py` 560~600·1357~1359행). 공식 문서도 「profile data」로 고른다고 적음.
- `source`가 `R-14` / `자료 R-14`로 두 전략에서 달랐습니다 — 모델 글이라 흔들림 대상. `assert 'R-14' in source`는 규격 §3과 부딪힘.
- 입력 글 자체에 답이 들어 있어(「… 14일입니다. 구조화해 주세요」) 「근거에 맞는 답」을 모델이 찾는 장면이 아닙니다. 01 도구와 이으면 「도구 결과 → 양식」 흐름을 보일 수 있으나, 도구와 양식을 함께 쓰면 ProviderStrategy는 한 요청에 도구와 양식을 함께 싣습니다(요청 수·메시지 수가 달라짐 — 실행해 볼 몫).
- 옛 06 노트북 설명 「Ch6에서 배운 `with_structured_output(Grade, method="json_schema", strict=True)`」은 부분 참(Ch 6 03은 `with_structured_output(StudyCard)`·`include_raw=True`, `method`·`strict` 인자는 안 씀).

### 03 AgentState와 context schema
- `AgentState` 칸은 `messages`(`add_messages`)·`jump_to`(내부)·`structured_response`(양식이 있을 때만)(`langchain/agents/middleware/types.py` 349~355행). **Ch 13 04 상태 형식과 같은 모양**(`TypedDict` + `Annotated[list[AnyMessage], add_messages]`)이라 「Ch 13 상태 형식에 칸 하나 더하기」로 이을 수 있습니다. `from langchain.agents import AgentState`와 Ch 22가 쓰는 `from langchain.agents.middleware import AgentState`는 **같은 클래스**(확인).
- b3 「MessagesState와 TypedDict 상태를 사용합니다」 — **Ch 13·20은 `MessagesState`를 가르치지 않았습니다**(과정 요약 §2-12). 틀린 전제.
- `ToolRuntime` 매개변수는 **모델에게 보이는 인자에서 빠집니다**(`current_access.args` = `{}` 확인). 설치판이 힌트 `ToolRuntime`을 읽어 주입 — 힌트가 동작을 바꾸는 자리(Ch 20 02 `error: ValueError`와 같은 성격).
- 「context가 결과 상태에 자동 저장되지 않음」 증거가 `'context' not in result` 하나(원래 없는 키를 확인)라 약합니다. 결과 키 목록 `['messages', 'request_tag']` 출력이 더 직접적.
- 컨텍스트 모양 셋(데이터 클래스·`TypedDict`·`BaseModel`) 모두 도구가 값을 읽는 것을 모델 없는 작은 그래프에서 확인(§5-3).

### 04 0x에서 1x로 마이그레이션
- **옛 API를 실행하지 않고** 대응표 글자만 출력합니다. 그러나 **설치판 `langgraph-prebuilt 1.1.0`에 옛 함수 `create_react_agent`가 사용 중단 예고(`LangGraphDeprecatedSinceV10`, `DeprecationWarning`의 자식)와 함께 남아 있어** 모델 없이 그래프를 만들어 견줄 수 있습니다(§5-4). 잠금에 0.x 판은 없어 **0.x 자체는 실행할 수 없습니다**.
- 대응표 셋째 줄 「response_format 별도 후처리」는 부정확 — 옛 함수도 `response_format`을 받았고, 루프가 끝난 뒤 `generate_structured_response` 노드에서 **모델 요청을 한 번 더** 했습니다(설치판 그래프 확인). 공식 이주 안내: 「in the main loop, reducing cost and latency」.
- 넷째 줄 「Pydantic 사용자 상태 → TypedDict」는 공식 이주 안내(「TypedDict only」)와 맞습니다. 옛 함수 입력 칸에는 `remaining_steps`가 더 있었습니다(설치판 입력 형식 확인).
- `inspect.signature` 한 줄 약 900자 출력은 학생이 읽기 어렵고, 「글자 안에 이름이 있는가」는 인자 이름만 확인합니다.
- 최소 실행 질문(「마이그레이션에서 먼저 고정할 것은 무엇인가요?」)은 모델 일반 답을 받는 것이라 이 절 관찰과 무관.

### 05 retriever를 도구로 전환
- **제목의 retriever(검색 객체)가 없습니다.** 임베딩도 벡터 검색도 없이 딕셔너리 낱말 겹침입니다. `as_retriever()`는 과정 미교육(과정 요약 §2-3), 「검색기」는 Ch 9~12 금지어.
- **낱말 겹침 규칙이 거의 모든 질문에 대출 줄을 붙입니다**: 규정 글의 낱말 가운데 한 글자 「수」·「도서는」이 질문에 있으면 걸림(예약 질문 「예약한 도서는 …」에 대출·예약 두 줄이 모두 걸렸을 것 — 도구 메시지 출력이 없어 노트북에서 확인 안 됨).
- 학습 목표 「재검색 횟수와 답변 범위를 제한」은 시스템 메시지 글의 「한 번」뿐이고 코드 제한(바퀴 한도·실행 한도)은 없음. 주차 질문의 재검색·검색어는 모델 선택이라 흔들림 대상.
- 06의 `retrieve`(실제 임베딩 검색)가 오히려 「검색 함수를 도구로」에 맞습니다(§6·§10).

### 06 같은 평가셋으로 RAG 비교
- **Ch 29 04(대기)와 파일 계약**(§4-6): `data/rag-comparison.json` **3줄**, 읽는 키 `qid`·`agent_usage.input_tokens`·`agent_usage.output_tokens`·**`agent_usage.model_calls`**·`agent_supported`·`tool_calls`(**줄마다 ≥ 1 `assert`**)·`agent_latency_s`·`agent_trace`. `len == 3` `assert`. → 06은 질문 수 3·시간 재기·키 이름을 바꿀 수 없고, 도구 파일로 `sum_usage`(키 `requests`)를 쓰면 `model_calls` 키를 따로 맞춰야 함.
- **판정이 흔들린 기록**: C01 고정 답이 정답 문서(LIB-001) 밖의 전자책 7일(LIB-004)을 더함 → 첫 실행 판정 False(2/3) → 경로 수정 뒤 재실행 True(3/3)(`textbook/part6/qa/ch21-ch29-technical-review.md` 38행). 결론에 판정 비교를 쓰면 규격 §2-7 9번 끝과 부딪힘.
- 세 질문 모두 첫 검색 앞 둘에 정답 문서가 있어 「재검색」 장면이 없음(옛 b6가 밝힘). 질문 `kind`는 semantic 둘(C01·C05)·keyword 하나(C07).
- 임베딩 설정이 Ch 14(`dimensions=256`)와 다름(기본 1536). Ch 14 도구 파일 `search_hits(embedding_model, question, doc_vectors, doc_ids, top_count)`·`rank_by_distance`는 **거리**(작을수록 가까움, 칸 `거리`)를 내고, 06 `retrieve`는 **유사도 점수**(칸 `score`)를 냄.
- **자료 차이**: Ch 14 문서 FAC-003 「평일 자료실은 오전 9시부터 오후 9시까지」 ↔ 01·05·Ch 20·Ch 22의 「평일 09:00~20:00」, LIB-001에는 「5권」이 없음. 한 챕터 안에서 자료실 운영 시간이 둘.
- 「정확도」·「fixed_accuracy」는 판정 비율이지 정답률이 아님(Ch 15 태도 「점수는 정답률도 사람 판단 일치율도 아닙니다」). 과정 말은 평가 모델(judge)·근거 충실도(Ch 15 02)·정답 문서 ID(Ch 11).
- 01~05와 달리 `init_chat_model`로 모델 객체를 만듦(`temperature` 누락).

## 3. 실습 폴더 구조와 읽는 곳

```
labs/part6/ch21-create-agent/
  README.md (1문단 — 「Ch14의 읽기 전용 문서·평가셋」·「절당 예상 비용은 1달러 미만」)
  pyproject.toml   uv.lock (90항목)
  data/rag-comparison.json (06이 씀, 2,750B, 122cfce2…)
  notebooks/01~06-*.ipynb
  .venv/ (macOS 판 211MB — home = /Users/…/cpython-3.12-macos-aarch64-none, uv 0.11.6)
  (없음: runs/ · tests/ · 모듈 · 도구 파일 · 노트북 생성기)
```

- **자료**: 01·05는 노트북 안 딕셔너리(규정 글), 02·03·04는 입력 글만, **06은 Ch 14 실습 폴더의 `data/documents.json`·`queries.json`을 읽고**(환경 셀이 `labs/part6/ch21-create-agent/pyproject.toml`이 보이는 위 폴더를 `ROOT`로 찾음) `data/rag-comparison.json`을 씀. Ch 19 `orders.csv`·`order_tools.py`, Ch 20 `graph_tools.py`는 읽지 않음.
- **Ch 21 파일을 코드로 읽는 곳**(`grep -rn`, `textbook`·`labs`·`.moai`):

| 읽는 곳 | 무엇을 | 계약 |
|---|---|---|
| **`labs/part6/ch29-agent-evaluation/notebooks/04-운영-지표와-Ch18-궤적-비교.ipynb`** c12·c14·c16·c18 | `rag-comparison.json`을 읽어 줄 셋의 `agent_usage`·`agent_supported`·`tool_calls`·`agent_latency_s`·`agent_trace`로 운영 열을 만들고 평균·가장 가까운 자리 p95 | **3줄·키 이름·`tool_calls ≥ 1`** — §2 06. Ch 29 04 `_src` b6가 값(평균 519.7토큰·1.880초·p95 2.094)을 인용 → 06을 다시 실행하면 값이 바뀜(Ch 29는 대기 — 고치지 않고 인계) |
| `textbook/part6/prerequisite-files.json`·`textbook/part6/ch29-agent-evaluation/qa/prerequisite-files.json` | `rag-comparison.json`(선행 파일) — Part 6 묶음에 넣음 | 파일 이름·경로 |
| `textbook/part6/ch21-create-agent/qa/prerequisite-files.json` | Ch 14 `documents.json`·`queries.json`(06이 읽음) | Part 목록에 모아짐(`collect_public_files.py`) |
| `textbook/part6/public-files.json`(2~11행) · 챕터 `qa/public-files.json`(HTML 7·실습 파일 10, **경로 배열**) | 묶음 허용 목록 — `build_bundle.py` `practice_files()`가 Part 목록의 `labs/part6/…`만 넣음 | 도구 파일을 만들면 두 곳에 더함(`collect_public_files.py`가 챕터 목록으로 Part 목록을 **다시 씀**) |
| `textbook/part6/_build_index.py` 19행 · `textbook/_notebook/build_index.py` 46행 · `build_bundle.py` 23행 | (6, 10, 설명) · (`'create_agent'`, 절 수 **6**, 설명) · 공개 챕터 목록 | 실습 절을 더하면 6 ≠ 7(Ch 17~20 선례: `_notebook/build_index.py`는 전체 마감 몫) |
| `textbook/part6/qa/check_bundle_execution.py` | 묶음에서 **Ch 24 01·Ch 28 01만** 키 없이 실행 | **Ch 21은 실행하지 않음**(묶음 실행 계약 없음) |
| `textbook/_notebook/verify.py` 104~123행 | import 금지 모듈 `openai`·`rag`·`context_lab`·`document_processing`·`experiment`·`harness`·`prompts`(첫 이름) | 도구 파일 이름(`rag_tools`는 통과 — Ch 9~15 선례) |
| 옛 검사(고치지 않음, 기록만) | `check_scope.py`(`EXPECTED` ch21 (6, 10) · `SECTION_COUNTS` ch21 = **6**, meta 정규식 `실습\s*([\d.]+)h`) · `check_notebook_readiness.py`(**함수 힌트 필수**·노트북마다 `assert`·`len == 47` — 지금 Part 6 노트북 48이라 이미 멈춤, **멈추기 전에 `notebook-readiness.json`을 다시 씀**) · `check_figures.py`(SVG마다 `.excalidraw` 짝 — Ch 22 Mermaid SVG에서 이미 멈춤) · `check_visual_reports.py`(`len == 116`) · `check_delivery.py`(`part6-practice.zip`·`llm-practice.zip` 신선도) | 실습 절(「실습 30분」)을 더하면 `check_scope.py`가 ch21에서 `Missing scope`(Ch 17 06 선례). 모두 Ch 22 개선 뒤부터 이미 어긋남 |
| 기록만 | `textbook/part6/qa/final-artifact-hashes.json` 2~34·264~273행 · `existing-artifact-hashes.json`(Ch 21 줄 없음, Ch 14 자료 줄도 없음) · `notebook-executions.json`·`visual-results.json`·`lesson-scope.json`·`figure-consistency.json`·`language/ch21-ch29-final.json`·`ch21-ch29-technical-review.md` · `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json`(verify가 다시 씀)·`checks/ch21-create-agent/`(옛 화면 검사) · `textbook/part7/qa/existing-artifacts-before.json` · `.moai/context.md` | — |

- **Part 6 묶음 상태**: `part6-practice.zip` `0543ea63…`(95항목, `integration-results.json` 48절·92파일) 안 Ch 21 파일 열(노트북 6·README·잠금 둘·`rag-comparison.json`)과 Ch 14 자료 둘이 **디스크와 같음**. `llm-practice.zip` 안 Ch 21은 확인하지 않음(전체 마감 몫).
- **옛 생성기**:

| 파일 | 무엇을 씀 | 비고 |
|---|---|---|
| **`textbook/part6/_author_ch21_ch29.py`**(563줄, `1d3d1dc9…`, **Ch 21·Ch 29 공용**) | `write_chapter()` 두 번(561·562행) — **Ch 21과 Ch 29의 `chapter.json`(`hours`·`objectives`·절 `format`을 덮어씀)·노트북 전부(`SOURCES_ONLY`가 없으면)·`_src` 전부** | 실행하면 Ch 21 개선본과 **대기 챕터 Ch 29(01~04)**를 함께 옛 판으로 덮어씀. 부르는 스크립트 0(`grep`). 파일 안 Ch 21 06 셀은 저장 경로가 상대 경로(314행)라 지금 노트북과도 다름 |
| `textbook/part6/ch21-create-agent/figures/_gen_figures.py` | `NN-흐름.{svg,excalidraw,caption.md}`(`textbook/part5/_figure.py`) | 옛 그림 여섯 벌 |
| (챕터 밖) `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6a_enrich.py` | Ch 21 여섯 절 `_src` b4·b5 「코드를 읽는 순서」·「다른 상황과 적용 경계」와 노트북 설명 셀을 끼워 넣은 옛 도구(06 추가 단락 포함) | 기록만(Ch 16~20 선례대로 막지 않음). `part6b_*`·`_generate_ch25_ch26.py`는 Ch 21 0건 |

→ 규격 §8 1번: **01절 작업 때 `figures/_gen_figures.py` 첫머리에 설명 주석 + `raise SystemExit(...)`**. **공용 생성기 `_author_ch21_ch29.py`는 막으면 Ch 29 쪽 생성도 함께 막힙니다** — 선택지: (가) 첫머리에서 막되 「Ch 21 개선 뒤 이 파일은 Ch 21을 덮어씀. Ch 29를 다시 만들려면 Ch 21 줄(561행)을 빼고 쓸 것」을 적음(Ch 29는 개선 때 자기 생성기를 새로 쓰는 것이 과정 흐름이라 영향 작음) · (나) 561행만 막는 한 줄 수정(Ch 29 생성은 살림 — 파일 고치기가 두 챕터에 걸침) · (다) 막지 않고 인계에만 적음(실수로 돌리면 Ch 21 덮어씀). 사본은 이미 `before/generators/`. 챕터 마감 때 `mv -n` → `qa/upgrade/before/generators/blocked/`는 `_gen_figures.py`만 해당(공용 파일은 옮기면 Ch 29 몫이 사라짐 — Part 6 마감 또는 Ch 29 마감 몫).

- **판**: `requires-python = ">=3.12,<3.13"`, `dependencies = ["langchain==1.4.0", "langchain-openai==1.6.0", "langgraph==1.2.11", "numpy>=2.0", "python-dotenv==1.2.3", "pillow>=11.0"]`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`, `[tool.uv] package = false`. 잠금 주요 판: `langchain-core 1.6.2`·`langgraph-prebuilt 1.1.0`·`langgraph-checkpoint 4.2.0`·`openai 3.11.0`·`pydantic 2.13.5`·`numpy 2.5.3`·`pillow 12.3.0`·`langsmith 0.12.4`·`tiktoken 0.14.0`·`httpx 0.28.1`. 임베딩은 `langchain-openai`의 `OpenAIEmbeddings`(따로 패키지 없음), **벡터 저장소 없음**(NumPy 배열로 직접). `pytest` 없음.
- **Ch 20 잠금과 견줌**: 런타임 판 **모두 같음**(langchain·core·openai 판·langgraph·prebuilt·checkpoint·openai·pydantic 2.13.5·dotenv·dev 넷). **Ch 21에만** `numpy 2.5.3`·`pillow 12.3.0`(항목 90 ↔ 88). Ch 22 잠금은 런타임 판이 같고 **dev 그룹이 없음**(47항목 — Ch 22 몫). Ch 19 `pydantic 2.12.5`와 다름(Ch 20과 같은 상태).

## 4. 앞뒤 챕터 이음새

### 4-1. Ch 20 인계(요약 §13 「Ch 21이 전제하면 안 되는 것」) 항목별 지금 상태

| # | Ch 20이 넘긴 것 | Ch 21 지금 자리 | 상태 |
|---|---|---|---|
| 1 | `create_agent`는 `tools_condition`을 안 씀 — 노드 이름·상태 칸·단계 수가 같다고 적지 않기 | 01 b2 「Ch20에서는 model 노드, tools_condition, ToolNode, tools→model 엣지를 직접 연결했습니다. create_agent를 사용하면 호출 한 줄로 같은 반복 구조를 얻지만」 · b4 「마지막 model이 tool_calls를 만들면 초록 ToolNode로 이동」 | 부분 — 같다고 단정하지는 않지만 차이(자체 조건 함수·`Send`·흔적 칸 없음·`jump_to` 칸)를 설명하지 않음. 설치판 사실은 §5-1 |
| 2 | 되돌아가는 엣지 Ch 20 실선 ↔ Ch 21 01 출력 점선 | 01 노트북 c6 출력 `tools -.-> model` · `_src` 설명 0 | **그대로** — 까닭(조건부 엣지, 기본 목적지 모델)은 §5-1 |
| 3 | Ch 20은 시스템 메시지를 안 씀 — 01 b2 「지시」·「반환」 고칠 자리 | 01 b2 「create_agent의 세 인자가 Ch20의 모델·도구·**지시**를 어떻게 묶고, **반환** 그래프가 어떤 루프를 실행하는가?」 · b4·b8 「system_prompt는 근거 사용과 종료 기준을 **지시**합니다」 | **그대로** |
| 4 | 규정 글 차이(Ch 21은 토요일 없음·`KeyError` ↔ Ch 20 `raise ValueError`) | 01 c6 · 05 c6 `DOCS`(+ 예약) | **그대로**. 06은 Ch 14 문서(평일 오후 9시) — 한 챕터 안 운영 시간 둘(§2 06) |
| 5 | 05 흐름에서 오류 처리 함수가 쓰인 장면 없음(도구의 `ValueError`만 받는 02 판) | Ch 21은 오류 처리 인자·함수를 전혀 안 씀. `create_agent`의 `ToolNode`는 기본값(§2 01 `KeyError`) | 해당 문장 없음 — 오류 처리를 다루면 Ch 20 02 판과 가를 것(미들웨어 `@wrap_tool_call`은 Ch 22 몫) |
| 6 | 실행 한도(단계 수) ≠ 바퀴 한도, K+1 규칙 | Ch 21 0건. 05 학습 목표 「재검색 횟수 … 제한」은 시스템 메시지 글뿐 | 해당 문장 없음. `create_agent` 그래프도 설정 딕셔너리 `recursion_limit`을 받음(설치판 기본 10007, 이번에 실행 안 함). 옛 함수 입력 칸 `remaining_steps`는 새 함수에 없음(§5-4) |
| 7 | 요청 수 셈은 `parallel_tool_calls=False`일 때만 | 01 「두 모델 호출의 합」 · 05 주차 검색 둘 · 06 「Agent는 각 질문에서 모델 2회·도구 1회」 | **조건이 다름** — Ch 21은 여럿 담기를 끌 인자가 없음(§2 01), `create_agent`는 요청마다 `Send`로 도구 노드를 부름 |
| 8 | `graph_tools.py`는 Ch 20 폴더 전용 | Ch 21 폴더에 도구 파일 없음 | 맞음 — 가져올지는 §6 |
| 9 | 모델 답이 늘 같다고 쓰지 않기 | 01·02·03·05 `assert`가 모델 글·선택에 걸림 · 06 판정 흔들림 기록 | **부딪힘** |

- **Ch 20에서 이어받을 말**(요약 §4·§13): 모델 노드·도구 실행 노드·도구 조건 함수·되돌아가는 엣지 · 오류 처리 인자(복수) ≠ 오류 담기 설정(단수) · 단계·실행 한도·설정 딕셔너리·명시적 종료 · 규칙 갈래 그래프·모델 선택 그래프·결과 편차 · 예상 비용(Ch 6 06). 06 「고정 RAG ↔ Agentic RAG」는 Ch 20 04 「규칙 갈래 그래프 ↔ 모델 선택 그래프」와 같은 틀이라 말을 이을 수 있음.
- **Ch 20 쪽 참 문장**(요약 §13 「사실(참)」): Ch 21 01 3행 b2 · 4행 b3 「Ch20에서 직접 연결한 StateGraph와 ToolNode」 · 04 4행 b3 「Ch20의 직접 조립 그래프를 사용합니다」(04는 실제로 Ch 20 그래프를 쓰지 않음 — 「사용」은 느슨함).

### 4-2. 앞 챕터 부품과 대조 (다시 쓸 후보)

| 부품 | 앞 챕터 | Ch 21 지금 | 다시 쓸 때 |
|---|---|---|---|
| 모델 셀 | 과정 표준 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(`nbkit.key_and_model_cells()`) · Ch 22 같은 모양 | 01~05 모델 이름 글자 · 06 temperature 없음 | 모델 객체를 만들어 `create_agent(model, tools=[…])`(Ch 22 모양) |
| 상태 형식 | Ch 13 04 `class …(TypedDict)` + 메시지 칸 `add_messages` · 칸이 바뀌면 새 이름 | 03 `SupportState(AgentState)`(상속) | `AgentState` = Ch 13 04 모양(§2 03) |
| 양식 클래스 | Ch 6 03 `StudyCard(BaseModel)`·`Field(description=, ge=, le=)` · Ch 19 02 `OrderQuery`·`Literal` | 02 `PolicyAnswer`·06 `Grade` | 말 「양식 클래스」·「양식」(Ch 6·19), 「스키마」 대신 |
| `@tool` | Ch 19 01 맨 `@tool`·독스트링·매개변수 `: str`(반환 힌트 0) · Ch 20 같음 · Ch 22 `-> str` 있음 | 넷 모두 `-> str` | 반환 힌트를 뺄지(§7-4) |
| 메시지 읽기 | Ch 19 06 `show_messages(messages)`·04 `tool_call_names(response)` · Ch 20 01 `call_id_lists(messages)` | 01 `enumerate`+`getattr` 한 줄 출력 | 도구 파일 후보(§6) |
| 사용량·비용 | Ch 19 05 `sum_usage(messages)`(키 `requests`·`input_tokens`·`output_tokens`) · Ch 6 06 `estimate_cost` | 01 자체 식 · 06 `usage_total`(키 `model_calls` — **Ch 29 계약 키**) | 06은 계약 키를 지켜야 함 |
| 검색 | Ch 14 도구 파일 `cosine_similarity`(Ch 5 02)·`cosine_distance`·`rank_by_distance`(Ch 12 01)·`search_hits`(Ch 14 06) — `OpenAIEmbeddings(dimensions=256)`, 칸 `거리` | 06 `retrieve`(유사도 점수, 1536차원) · 05 낱말 겹침 | §6 |
| 평가 | Ch 15 02 `build_judge_prompt`·`judge_once`(JSON 글) · 네 평가(근거 충실도 등) · 06 `average` · Ch 11 `unique_doc_ids`·`find_gold_rank` | 06 `with_structured_output(Grade, …)`·`mean` | 말 「평가 모델(judge)」·「근거 충실도」·「정답 문서 ID」 |
| 루프 말 | Ch 17 03 루프·바퀴·정지 조건(모델의 끝 선택)·바퀴 한도 · Ch 7 05 ReAct(실행 안 함)·관찰 | 01 「ReAct」·「루프」 | ReAct는 Ch 7 05 말로 이을 수 있음 |
| 시간 재기 | Ch 15 05·06·Ch 17 04·Ch 18 03·06 = 주제 절 예외 | 06 잼 | 06은 Ch 29 계약 칸 때문에 필요(Ch 18 06 선례와 같은 사유) |

### 4-3. 앞 챕터(완료)가 Ch 21에 기대는 문장

| 자리 | 지금 문장 | Ch 21 개선 때 |
|---|---|---|
| Ch 20 01 `_src` b2(끝) | 「Ch 21에서는 create_agent 호출 한 줄로 같은 되풀이 구조를 만듭니다. 그 안에서 무엇이 도는지 읽으려면 이 절의 그래프를 알아야 합니다.」 | 01이 되풀이(도구 → 모델)를 보이면 참 |
| Ch 20 05 `_src`·노트북 b8 | 「Ch 21 01절은 이 챕터에서 직접 이은 반복 구조를 함수 create_agent 한 줄로 얻는 법을 다룹니다.」 | 01 주제를 유지하면 참 |
| Part 5 소개 `_src/index.html` | 「create_agent는 다음 Part의 Ch 21에서 배웁니다.」 | 참 |
| `labs/part4/continuity-guide.md` | 「이후 Ch 21에서는 코드로 정한 흐름과 모델이 선택하는 흐름을 비교하고」 | 06(고정 ↔ 에이전트)을 유지하면 참 |
| `labs/part5/continuity-guide.md` | 「Ch 21에서는 직접 만든 루프를 `create_agent`와 비교합니다.」 | 01에서 Ch 20 그래프와 견주면 참 |
| Ch 1 01 `_src` | 「Part 6 Agent 개발 Ch 21~29」 | 참 |
| Ch 7 05 · Ch 17~19 | Ch 21 언급 0(Ch 7 05 ReAct 연결은 Ch 19·20) | — |

- **Ch 21 절을 링크하는 완료 파일은 0**(`grep` — 링크는 빌드로 다시 만드는 `textbook/part6/index.html`뿐). 슬러그를 바꿔도 완료 챕터 링크는 깨지지 않습니다.

### 4-4. Ch 22 Middleware(완료)가 Ch 21에 기대는 문장·코드 — 개선 뒤에도 참이어야 함

| 자리 | 지금 문장·코드 | 판정 기준 |
|---|---|---|
| Ch 22 01 `_src` b3(4행) | 「Ch21에서는 create_agent() 함수로 에이전트를 만들었습니다. 실제 서비스에서는 여기에 기능이 더 붙습니다.」 | 참 |
| Ch 22 01 `_src` b4(9행) | 「Ch21 01절에서 에이전트가 반복하는 흐름을 봤습니다. 모델을 부르고, 모델이 요청하면 도구를 실행하고, 다시 모델을 부릅니다.」 | **01이 도구를 부르는 실행(모델 → 도구 → 모델)을 유지해야 참** |
| Ch 22 02 `_src` 26행 | 「미들웨어 방식은 create_agent() 함수에 한 번 등록합니다.」 | 참(`middleware=` 인자는 Ch 21이 안 가르쳐도 Ch 22가 가르침) |
| Ch 22 노트북 01~09 | `from langchain.agents import create_agent` · `model = init_chat_model(…, temperature=0, reasoning_effort="none")` · `create_agent(model, tools=[lookup_hours], middleware=hooks)` · 훅 `state: AgentState, runtime: Runtime`(`langchain.agents.middleware`) · `@tool def lookup_hours(day: str) -> str`(자료실 운영 시간 — 평일 09:00~20:00·토요일 10:00~17:00) · `ToolMessage` 직접 import | Ch 21이 **모델 객체 + `tools=` 키워드**로 가르치면 모양이 그대로 이어짐. `AgentState`는 같은 클래스(§2 03). 반환 힌트 `-> str`은 Ch 22에 있음(Ch 19 인계 「Ch22 도구 반환 힌트는 Ch19가 안 가르침」) — Ch 21이 반환 힌트를 뺄지 둘지 정하면 Ch 22와의 관계가 정해짐 |
| Ch 22 `qa/upgrade/handoff.md` 22·37행 | Ch 21 실습 폴더와 이름이 겹치는 정의는 `mask_pii` 하나(Ch 21 폴더엔 없음) · Part 6 묶음 목록은 경로 배열 | Ch 21이 도구 파일을 만들면 이름이 Ch 22 노트북 함수와 겹치지 않게(`mask_pii`·`lookup_hours`·훅 이름 등) |

- Ch 22에는 `chapter-summary.md`가 없습니다(시범 챕터). Ch 22 04 b3의 Ch 16 문장 등 Ch 21과 무관한 문장은 확인하지 않음.

### 4-5. 뒤 챕터(대기)가 Ch 21에 기대는 문장 — 고치지 않음

| 자리 | 지금 문장 | 판정 기준 |
|---|---|---|
| **Ch 29 04 노트북 c12~c18** | `rag-comparison.json` 3줄·키 계약(§4-6) | **파일 계약** |
| Ch 29 04 `_src` b1·b2·b4·b6~b9 · README 3행 | 「저장된 Ch18·Ch21 실행 기록」·「Ch21 세 Agentic RAG 행은 평균 final_score 1.0, 모델 2회, 도구 1회, 519.7토큰, 1.880초」·「Agent 세 건의 p95는 지연 2.094초」·「Ch21의 agent_supported」 | 06을 다시 실행하면 **값이 바뀜** → 인계에 현재 값·새 값 |
| Ch 29 01 `_src` b3 | 「Ch11 평가셋과 Ch21 에이전트를 사용합니다.」 | Ch 29 01 노트북은 Ch 21 파일을 읽지 않음(느슨한 문장 — Ch 29 몫) |
| Ch 27 01 `_src` b3 | 「Ch 21의 create_agent는 모델과 도구의 반복을 만들었습니다.」 | 참 |
| Ch 27 02 `_src` b3 | 「Ch 19에서 @tool로 함수 설명과 입력 스키마를 만들었고 Ch 21에서 create_agent에 도구를 전달했습니다.」 | 참 |
| Ch 30 01·02·03·09 `_src`(Part 7) | 「Ch21에서 Agent 실행 객체를 만들었습니다」·「Ch21의 Agent와 Ch23의 체크포인터처럼 생성 비용과 수명주기가 다른 객체」·「Ch21에서 Agent의 입력과 결과가 상태 사전임을 확인」·**「Ch21에서는 init_chat_model과 create_agent로 도구 호출 Agent를 만들었습니다」** | 09는 **`init_chat_model`로 모델 객체를 만드는 모양**을 전제 — 지금 Ch 21 01~05(글자 모델)와 어긋나고, 개선에서 모델 객체로 바꾸면 참 |
| Part 6 소개 `_src/index.html` · `practice-start.md` 15행 · `labs/part6/continuity-guide.md` 7·12행 · `labs/part7/continuity-guide.md` 8행 | 「Ch 20의 StateGraph·ToolNode 루프를 Ch 21의 create_agent와 비교」·「Ch 21에서 에이전트를 만들고 Ch 22에서 호출 전후의 처리를 추가」·「Ch21 `create_agent`의 도구 호출 루프와 구조화 출력」·「Ch18의 패턴과 Ch21의 에이전트 → Ch26」(Ch 26 `_src`는 Ch 21 언급 0)·「Ch21의 에이전트, Ch23의 저장 상태 → Ch30」 | 참(continuity-guide 12행 「Ch39」는 Ch 21과 무관) |
| Ch 23~26·28 `_src` | Ch 21 언급 0 | — |

### 4-6. Part 6 묶음·목록·계약·검사

- **계약 하나 — Ch 21 06 ↔ Ch 29 04**(Ch 18 06 ↔ Ch 29 04와 같은 모양의 출력 계약. 차이: Ch 18은 노트북 **출력 글**을, Ch 21은 **JSON 파일**을 읽음): 파일 `labs/part6/ch21-create-agent/data/rag-comparison.json`(지금 `122cfce2f3769d60…`) · 줄 **3** · Ch 29가 읽는 키 `qid`·`agent_usage`{`input_tokens`·`output_tokens`·`model_calls`}·`agent_supported`(bool)·`tool_calls`(int, **≥ 1**)·`agent_latency_s`(float)·`agent_trace`(목록) · Ch 29가 읽지 않는 키 `gold_doc_id`·`fixed_*`·`agent_answer`·`fixed_supported`. 06을 다시 실행하면 해시·값이 바뀌므로 규격 §7-2(값이 바뀌면 읽는 쪽 기대값을 돌려 봄)대로 Ch 29 04 c12~c18의 `assert` 세 줄(`len == 3` · `tool_calls ≥ 1` · p95 ≥ 최댓값)을 새 파일로 돌리고, 본문 인용 값(519.7·1.880·2.094 등)은 인계에 적음. **06이 에이전트가 검색하지 않는 질문을 넣으면 Ch 29 04 `assert`가 깨짐.**
- **선행 목록**: Part 6 `prerequisite-files.json`에 Ch 21 줄은 `rag-comparison.json` 하나(Ch 29 몫) + Ch 21 챕터 목록의 Ch 14 자료 둘. 묶음 실행 검사는 Ch 21 없음.
- **묶음을 다시 만들 때**: `python3 textbook/part6/_build_index.py` → `part6-practice.zip`(Ch 22 선례 — 결과 `Part 6: N verified sections; M bundled files`) · 도구 파일을 만들면 챕터 `qa/public-files.json` + `textbook/part6/public-files.json`(Ch 22 선례는 직접 한 줄, `collect_public_files.py`를 돌리면 Part 목록 전체를 다시 씀 — 돌리기 전 차이 확인).
- **Part 6 옛 검사 스크립트가 Ch 21을 보는 법(기록)**: `check_scope.py` 절 수 6·(6, 10)·meta 정규식(「실습 30분」 불통) · `check_notebook_readiness.py` 함수 힌트 필수(과정 규칙과 반대)·`len == 47` · `check_figures.py` SVG마다 `.excalidraw` · `check_visual_reports.py` `len == 116` · `check_delivery.py` 묶음 신선도(`llm-practice.zip`에서 멈추는 것이 과정 공통) · `check_bundle_execution.py` Ch 21 안 돌림. **모두 이미 Ch 22 개선으로 어긋난 상태**라 Ch 21도 선례대로 고치지 않고 돌린 결과만 적음(`check_notebook_readiness.py`는 결과 파일 되돌림).

## 5. 라이브러리 동작 — 설치판 소스와 모델 없는 확인 (2026-09-25)

설치판: `langchain 1.4.0`(`langchain/agents/factory.py` 2090줄)·`langgraph 1.2.11`·`langgraph-prebuilt 1.1.0`·`langchain-core 1.6.2`·`langchain-openai 1.6.0`. 확인 스크립트 `/tmp/ch21-prep/graphs.py`·`runtime_check.py`·`runtime_check2.py`·`bound.py`(기기 `/tmp`, 키 뺌). 모델 객체는 `init_chat_model(…, api_key="sk-not-a-real-key")`로 만들어 **그래프 구조만** 보고 `invoke`하지 않았습니다. **노트북 셀이 아니라 준비 조사용 확인이며, 모델이 낀 흐름에서는 실행하지 않았습니다.**

### 5-1. `create_agent` 그래프
- 노드 `['__start__', 'model', 'tools', '__end__']`, 구조 문자열 `__start__ --> model; model -.-> __end__; model -.-> tools; tools -.-> model;`(01 노트북 출력과 같음). 반환 종류 `CompiledStateGraph`.
- 모델 이름 글자를 넘기면 `init_chat_model(model)`(995~996행) — **temperature·reasoning_effort 기본값**. 모델 객체(`temperature=0.0`·`reasoning_effort='none'`)를 넘기면 그대로 씀.
- 모델 → 도구 갈래는 `_make_model_to_tools_edge`: 마지막 응답에 도구 호출 요청이 없으면 끝(「모델의 끝 선택」), 있으면 **요청마다 `Send("tools", [요청])`**(1923~1975행). 도구 → 모델은 `_make_tools_to_model_edge`(조건부, 기본 모델로 — 그래서 점선). `tools_condition` import 없음.
- `ToolNode(tools=…, wrap_tool_call=…, awrap_tool_call=…)`(1089행) — `handle_tool_errors`는 기본값.
- 여럿 담기를 끌 인자는 없음. `model.bind(parallel_tool_calls=False)`는 그래프 생성까지 됨(호출 동작 미확인). 설치판은 `ModelRequest.model_settings`를 `bind_tools(…, **model_settings)`로 넘김(1396·1439행 — 미들웨어로 바꾸는 값).

### 5-2. 구조화 출력 두 전략
- `ToolStrategy(PolicyAnswer)` 도구 없는 그래프: 노드 `model`만, 엣지 `START→model`·`model→__end__`(조건)·**`model→model`(조건)**. `ProviderStrategy`: 노드 `model`만. 양식 클래스를 그대로 넘기고 도구가 있으면 노드 `model`·`tools`.
- ToolStrategy가 남기는 도구 메시지 글 기본값 `f"Returning structured response: {structured_response}"`(1263행, `tool_message_content`로 바꿈). 검사 실패 재요청은 `handle_errors`(기본 `True`) — 이때만 모델 요청이 늘어남(공식 문서).
- 자동 선택: `_supports_provider_strategy` — 모델 프로필 `structured_output`이 참이면 ProviderStrategy. `gpt-5.4-mini` 프로필 `structured_output: True`·`tool_calling: True`(설치판 프로필 확인). OpenAI 계열은 ProviderStrategy에서 `strict=True`를 더 붙임(1396~1400행).
- 공식 문서 지원 양식: `BaseModel`(검사된 객체) · 데이터 클래스·`TypedDict`·JSON Schema 딕셔너리(딕셔너리로) — 양식을 `TypedDict`로 적을 수도 있음(칸 설명은 못 붙임).
- 결과 칸: ToolStrategy 그래프 출력 형식 키 `['messages', 'structured_response']`.

### 5-3. `AgentState`·`context_schema`·`ToolRuntime`
- `AgentState(TypedDict)` 칸 셋(§2 03), `langchain.agents`·`langchain.agents.middleware` 같은 클래스. `ToolRuntime`도 `langchain.tools`·`langgraph.prebuilt` 같은 클래스(`tool_node.py` 1663행).
- `@tool` 매개변수 `runtime: ToolRuntime` → 도구 인자 `{}`(모델에게 안 보임). 제네릭 `[UserContext]` 없이도 주입됨.
- 작은 그래프(`StateGraph(SupportState, context_schema=…)` + `ToolNode` + 손으로 만든 도구 호출 요청)로 컨텍스트 **데이터 클래스·`TypedDict`·`BaseModel` 셋 모두** 도구가 `student-7:read-only`를 만들고, 결과 키 `['messages', 'request_tag']`·`request_tag` `lesson-03`. **세 모양 모두 이 작은 그래프에서 Pydantic 직렬화 `UserWarning` 2건**(옛 03 노트북 출력의 `create_agent` 흐름에는 경고 없음 — 01·03 첫 실행에서 확인할 몫). `TypedDict` 컨텍스트는 `runtime.context["user_id"]`(딕셔너리 읽기).

### 5-4. 옛 API `create_react_agent`
- `from langgraph.prebuilt import create_react_agent`가 설치판에 **있음**(`chat_agent_executor.py` 274~277행 `@deprecated(… category=LangGraphDeprecatedSinceV10)`). 부르면 경고 `create_react_agent has been moved to langchain.agents. Please update your import to from langchain.agents import create_agent.`(경고 종류는 `DeprecationWarning`의 자식 — 노트북 셀에서 부르면 출력에 보일 것으로 봄, 확인은 첫 실행).
- 옛 그래프(모델 없이 생성): 노드 `agent`·`tools`, **`tools --> agent` 실선** · `response_format`을 주면 **`generate_structured_response` 노드**가 더 생김(루프 뒤 모델 요청 한 번 더) · 입력 칸 `['messages', 'remaining_steps']`(새 함수 `['messages']`) · 인자 `prompt`·`pre_model_hook`·`post_model_hook`·`state_schema`·`context_schema`·`version`.
- 옛 상태 클래스 `langgraph.prebuilt.chat_agent_executor.AgentState`·`AgentStatePydantic`도 사용 중단 예고(53~104행).
- **잠금에 langgraph 0.x·langchain 0.x는 없습니다** → 「0.x 판 실행」은 불가, 「1.x에 옮겨 둔 옛 함수 실행」은 가능.

### 5-5. `draw_mermaid_png`
- 기본 `MermaidDrawMethod.API` → `https://mermaid.ink`(외부 요청). 다른 방법(`PYPPETEER`)은 잠금에 없음.

## 6. §2-7 판단 근거 — 도구 파일

### 사실
1. **챕터 안 되풀이**: 설치·환경 셀 여섯 벌(13줄 × 6 — 준비 셀이라 도구 파일 대상 아님) · 01·05 자료실 규정 딕셔너리와 `@tool`(도구는 노트북 — Ch 19·20 결정) · 01 비용 셀과 06 `usage_total`(사용량 합) · 01 메시지 출력(`enumerate`+`getattr`). 절 사이에 다시 정의한 함수는 **0**(지금은 절마다 다른 일을 함).
2. **앞 챕터 함수로 바꿀 수 있는 것**: 메시지 읽기 — Ch 19 06 `show_messages`·04 `tool_call_names`·Ch 20 01 `call_id_lists` · 사용량·비용 — Ch 19 05 `sum_usage`·Ch 6 06 `estimate_cost` · 06 검색 — Ch 5 02 `cosine_similarity`·Ch 12 01 `cosine_distance`·`rank_by_distance`·Ch 14 06 `search_hits`(모두 Ch 14 도구 파일에 있음, NumPy) · 06 평가 — Ch 15 02 `build_judge_prompt`·`judge_once`(JSON 글)·06 `average`·Ch 11 `unique_doc_ids`·`find_gold_rank`.
3. **옮길 수 없는 것**: `@tool` 함수(도구 객체 — Ch 19 결정)·노트북 전역을 읽는 도구(`search_documents`는 `document_vectors`·`documents` 전역, `search_rules`는 `SEARCH_LOG` 전역)·에이전트 조립.
4. **Ch 20 `graph_tools.py` 통째 복사는 부적합**: `run_row`가 `result["trace"]`(모델 노드가 남기는 흔적 칸)를 읽는데 `create_agent` 결과에는 흔적 칸이 없음 → 여섯 가운데 하나는 못 씀. 나머지 다섯은 import 0이라 그대로 옮길 수 있음.
5. **Ch 14 `rag_tools.py` 통째 복사는 과함**: 21개 가운데 06이 쓸 것은 4~5개(`cosine_similarity`·`cosine_distance`·`rank_by_distance`·`search_hits`·`unique_doc_ids`), 나머지는 질문 재작성·HyDE 등 Ch 14 절 함수. `numpy` import(잠금에 `numpy 2.5.3` 있음 — `%pip`에 `numpy==2.5.3`).
6. **Ch 29 계약 키**: `sum_usage`는 키 `requests`, Ch 29가 읽는 키는 `model_calls` → 06 저장 줄에서 키를 옮겨 담아야 함(또는 `usage_total` 판을 06에 남김).
7. **이미 쓴 도구 파일 이름**: `llm_tools.py`(Ch 5·7·8) · `rag_tools.py`(Ch 9~15, 챕터마다) · `git_tools.py`(Ch 3) · `guardrails.py`(Ch 16) · **`agent_tools.py`(Ch 17)** · `workflow_tools.py`(Ch 18) · `order_tools.py`(Ch 19) · `graph_tools.py`(Ch 20). Part 6·7 실습 폴더 모듈: `durability_worker.py`·`idempotency_worker.py`(Ch 23)·`course_server.py`(Ch 28)·`agent_service/agent.py` 등(Ch 30). `verify.py` 금지 첫 이름 `rag`·`prompts` 등. 실습 폴더 `tests/` 없음 → §2-7 7항 해당 없음.

### 선택지 (결정하지 않음 — 장단점만)

**A. 도구 파일을 만들지 않는다**
- 장점: 묶음 목록·README·잠금 그대로. 06의 계약 키·저장 코드를 건드릴 일이 적음.
- 단점: 01 비용 식이 과정 표준(`estimate_cost`)과 다른 판으로 남고 06 검색·평가를 노트북에 새로 적음 — 규격 §2-7 3항과 부딪힘. 「만들어도 챕터 전체가 줄지 않음」(Ch 2·4·6·22 근거)은 06(107줄)이 앞 챕터 함수를 다시 적는 한 약함.

**B. 필요한 것만 옮긴 새 도구 파일 하나**(담을 후보: Ch 19 `tool_call_names`·`show_messages`·`sum_usage` · Ch 6 `estimate_cost` · Ch 20 `call_id_lists` · 06을 Ch 14 모양으로 바꾸면 `cosine_similarity`·`cosine_distance`·`rank_by_distance`·`search_hits` · 판정을 Ch 15 모양으로 바꾸면 `build_judge_prompt`·`judge_once`·`average`)
- 이름 후보: **`rag_tools.py`**(규격 §2-7 3항 RAG 챕터 이름, 05·06 주제 — 단 01~04 함수는 RAG가 아님) · **`llm_tools.py`**(규격 「그 밖 `llm_tools.py`」) · `policy_tools.py`(자료실 규정 소재) · `create_agent_tools.py`/`agent_run_tools.py`(챕터 이름 — 길고 새 말). `agent_tools.py`는 Ch 17이 이미 씀(피함), `graph_tools.py`는 Ch 20과 내용이 달라 혼동.
- 장점: 앞 챕터 함수를 같은 이름·인자로 이어 씀(Ch 19·20 출력 모양 그대로), 잠금 그대로(NumPy는 이미 있음).
- 단점: 묶음 목록 둘·README·`labs/part6/continuity-guide.md`(「예제 데이터는 각 절에서 다시 준비」류 문장 확인) 손질. 06 검색을 Ch 14 모양(거리·256차원)으로 바꾸면 Ch 29가 인용한 값·해시가 모두 바뀜(어차피 06을 다시 실행하면 바뀜).

**C. 두 파일**(Ch 20 `graph_tools.py`에서 다섯 + Ch 14 `rag_tools.py`에서 넷)
- 장점: 「옮긴 곳」이 파일 단위로 분명.
- 단점: 가져오기 두 줄·묶음 줄 둘, `graph_tools.py` 이름이 Ch 20 파일과 내용이 달라짐(`run_row` 뺌).

**D. 06만 도구 파일(`rag_tools.py`)을 쓰고 01~05는 노트북에**
- 장점: RAG 관례 이름 그대로, 01~04는 짧아 되풀이가 적음.
- 단점: 01 비용·메시지 출력은 노트북에 다시 적음.

공통: 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 …」(과정 요약 §3·Ch 19·20 선례) · `run_section.sh`가 `notebooks/`를 `PYTHONPATH`에 더함 · 함수마다 `# Ch N NN절에서 배웠습니다` · 금지 문법 0(`.get` 둘은 Ch 6 06 원본 예외).

## 7. 과정 규칙과 부딪히는 것 (선택지와 장단점만)

### 7-1. 양식 클래스(02 `PolicyAnswer`·06 `Grade`)
- **사실**: 규격 L5(스키마 클래스 `BaseModel`·`TypedDict`, 칸만, 라이브러리가 요구할 때만) · Ch 6 03·Ch 19 02가 `BaseModel`·`Field`를 세 문장 + Ch 2 10 링크로 가르침 · `response_format`은 양식 클래스를 요구함(`TypedDict`도 받음). 칸만 적어 두 클래스 모두 L5 안.
- (가) 그대로 `BaseModel` + `Field(description=)` — 장점: Ch 6 03·Ch 19 02 이어짐, `structured_response`가 객체로 나와 `model_dump()`·속성 읽기. 단점: 없음에 가까움(「스키마」 말만 「양식」으로).
- (나) `TypedDict` 양식 — 장점: Ch 13 모양, 결과가 딕셔너리. 단점: 칸 설명(`Field(description=)`)을 못 붙여 모델에게 칸 뜻을 알리는 장면이 약해짐, Ch 6·19 말과 끊김.

### 7-2. 상태 형식 확장(03 `SupportState(AgentState)`)
- **사실**: 규격 「조건부 — 라이브러리 클래스 상속은 그 절의 학습 목표일 때만」 · G1이 `class_def`로 잡음 · 03 학습 목표가 바로 이것 · 공식 문서도 「subclassing AgentState」 · Ch 13은 상속 없이 `TypedDict`를 새로 적음.
- (가) 그대로 상속 + 「Ch 13 04 상태 형식과 같은 칸에 칸 하나를 더하는 줄」 세 문장(`upgrade_allow` 또는 G1 예외 기록) — 장점: 공식 모양, 칸 하나만. 단점: 과정 첫 클래스 상속(Ch 22 `AgentMiddleware` 상속은 시범에서 허용된 조건부 예외).
- (나) Ch 13처럼 `TypedDict`를 새로 적고 `messages` 칸까지 다시 적기 — 장점: 상속 없음. 단점: `jump_to`·`structured_response` 칸이 빠져 설치판과 어긋날 수 있음(동작 확인 필요), 공식 모양과 다름.
- (다) 상태 확장을 미들웨어 `state_schema`로(공식 문서가 권하는 길) — Ch 22 몫이라 권하지 않음.

### 7-3. `context_schema` 클래스(03 `@dataclass UserContext`)
- **사실**: `@dataclass`는 과정 0건(데코레이터 + 새 클래스 모양, 위치 인자로 만들기 `UserContext("student-7", "read-only")`) · 공식 문서 예가 데이터 클래스 · 설치판은 세 모양 모두 주입(§5-3).
- (가) 데이터 클래스 그대로 + 세 문장(Ch 2 09 데코레이터 링크) — 장점: 공식 예와 같음, 속성 읽기 `runtime.context.user_id`. 단점: 새 문법 둘(`@dataclass`·데이터 클래스), 규격 L5 목록 밖.
- (나) **`TypedDict` 컨텍스트** — 장점: Ch 13 모양(새 문법 0), `context={"user_id": …}` 딕셔너리로 넘김. 단점: 도구 안에서 `runtime.context["user_id"]`(딕셔너리 읽기), 공식 예와 다름, 경고 여부 확인 필요.
- (다) `BaseModel` 컨텍스트 — 장점: Ch 6·19 모양(02와 같은 클래스 모양). 단점: 컨텍스트에 검사가 붙는지·경고는 확인 필요, 키워드로 만들어야 함.
- 공통: 03의 `ToolRuntime` 힌트는 라이브러리가 읽는 값(Ch 20 02 `error: ValueError`와 같은 성격) — 허용하되 「이 표시를 보고 실행기가 값을 넣어 준다」 한 문장, 제네릭 `[UserContext]`는 뺄 수 있음(§5-3).

### 7-4. 도구 함수 힌트
- Ch 19 결정: `@tool` 매개변수 `: str`만, 반환 힌트 0(「반환 힌트는 입력 형식·명세에 안 들어감」). Ch 20 같음. Ch 22(완료)는 `lookup_hours(day: str) -> str`.
- (가) 반환 힌트를 뺌(Ch 19·20 규칙) — 단점: Ch 22와 모양이 한 번 더 바뀜(Ch 22는 고치지 않음). (나) 둠 — 단점: Ch 19·20과 어긋나고 새 표기 한 문장 필요, 대신 Ch 22로 자연스럽게 이어짐.
- 06 도움 함수 힌트(`-> list[dict]`·`top_k: int = 2`)·변수 힌트는 동작에 영향 없음 — 빼는 쪽이 과정 규칙(기본값 매개변수도 과정 0건).

### 7-5. 제목·`objectives`·Part 목차의 금지어·영문

| 자리 | 말 | 과정 말·선례 |
|---|---|---|
| 챕터 제목 「create_agent — 직접 만든 루프를 한 함수로」 · 01 「create agent와 ReAct 루프」 | API 이름·ReAct | Ch 19·20 선례: API 이름은 **제목에만 두고 강사 확인**, 본문 첫 자리에서 풂. ReAct는 Ch 7 05 말 |
| 02 「구조화 출력 두 전략」 | — | 「구조화 출력」은 Ch 6 말 |
| 03 「AgentState와 context schema」 | API 이름 둘(밑줄이 공백으로 바뀜) | 제목에만(강사 확인) |
| **04 「0x에서 1x로 마이그레이션」** | **점이 빠진 판 번호** · 「마이그레이션」 | 제목 표기가 깨진 상태(`chapter.json`·HTML `<title>`·목차 모두). 0.x → 1.x로 적을지, 「옛 판에서 새 판으로 옮기기」로 풀지(강사 확인). 슬러그 `04-0x에서-1x로-마이그레이션`은 링크 0이라 바꿔도 됨 |
| 05 「retriever를 도구로 전환」 | retriever(내용과 어긋남 §2 05) · 「검색기」는 금지어 | 「검색 함수를 도구로」류, 제목에만 둘지(강사 확인) |
| 06 「같은 평가셋으로 RAG 비교」 | RAG | RAG는 Ch 9 말(허용) |
| `chapter.json` 절 제목 | Ch 20은 밑줄을 살림(「tools_condition」·「recursion_limit」), Ch 21은 밑줄·점이 사라짐(「create agent」·「context schema」·「0x」) | 옛 생성기가 만든 제목 — 마감 때 맞춤 |
| `objectives` 둘 | 「에이전트의 실행 구조를 코드와 궤적으로 설명합니다」·「같은 평가셋과 명시적 기준으로 동작을 비교합니다」(**Ch 29와 같은 글** — 공용 생성기가 두 챕터에 같이 씀) | 마감 때 절별로(Ch 20 선례 셋 → 다섯) |
| `_build_index.py` 19행 · `_notebook/build_index.py` 46행 | 「create_agent로 도구 에이전트를 만들고 같은 평가셋에서 고정 RAG와 비교합니다」 | 마감 때 19행만(46행은 선례대로) |
| 본문 공통 | 반환·지시(시스템 메시지 뜻)·추정·지연·경로·스키마·필드·검증·측정·분기·로그·주입·의존·채널·네이티브·프로필·인터페이스·파이프라인·거부·정확도·judge·gold·recall·Agentic·마이그레이션·v1 | 내놓다·시스템 메시지 글(Ch 16)·예상 비용·걸린 초·차례/흐름·양식/입력 형식·칸·검사·재다·갈래·기록·넣어 주다·(풀어 씀)·평가 모델(judge)·정답 문서 ID·재현율·(풀어 씀) |

### 7-6. 04 옛 API 실행 가능성과 규격 §3
- 규격 §3: 「라이브러리 동작은 설치한 버전의 소스로 확인 · 노트북에서 관찰하지 않은 동작은 「이번에 실행하지 않았습니다」」.
- (가) **1.x에 옮겨 둔 옛 함수를 모델 없이 그래프만 만들어 견줌**(노드 이름 `agent` ↔ `model` · 실선 ↔ 점선 · `response_format` 때 `generate_structured_response` 노드 · 입력 칸 `remaining_steps` · 사용 중단 경고 출력) + 새 함수 최소 실행 1번 — 장점: 옛 모양을 출력으로 보임(글·표보다 강함), 모델 요청 늘지 않음, 「0.x 판 자체는 실행하지 않았고 1.x에 남은 옛 함수로 확인했다」로 정직하게 한정. 단점: 경고 출력(stderr) 한 셀·「사용 중단 예고」 말 필요, 옛 함수가 다음 판에서 없어질 수 있음(잠금으로 고정됨).
- (나) (가) + 옛 함수·새 함수 모두 같은 질문으로 `invoke`(요청 +2~3) — 장점: 메시지 목록·요청 수(구조화 출력 때 한 번 더) 비교를 실제로. 단점: 모델 답이 흔들리는 비교가 늘어남, 옛 함수 호출 결과가 결론에 닿음.
- (다) 지금처럼 글·표 + `inspect.signature`만 — 장점: 단순. 단점: 「실행하지 않은 것」을 표로만 말하고 셋째 줄 사실이 부정확, 900자 서명 출력.
- 공통: 대응표 셋째 줄(「별도 후처리」)을 설치판 사실(「루프 뒤 한 번 더 요청」)로 고칠 것. 「Ch 22에서 훅 단위로」(b6·b7)는 Ch 22 01 훅 여섯과 맞음(참).

### 7-7. 06 걸린 시간·판정·「정확도」
- 걸린 시간: Ch 29 계약 칸(`agent_latency_s`)이라 재야 함 → Ch 18 06(Ch 29 계약 칸) 선례대로 「주제·계약 칸 예외」로 재되, 결론·그림·정리에서는 걸린 초 비교를 뺌(규격 §2-7 9번 끝).
- 판정: C01이 흔들린 기록(§2 06) → 결론은 요청 수·도구 호출 수·입력 토큰(코드로 세는 값)과 「가를 수 없다」, 판정 값은 둘째 단락·표·확인할 점에만. 판정 요청은 Ch 15 02 모양(JSON 글 + `judge_once`)으로 바꿀지, Ch 6 구조화 출력(`with_structured_output`)을 둘지.
- 「정확도」 → 「지지 판정 비율」류(Ch 15 태도). `summary`의 `fixed_accuracy`·`agent_accuracy` 키는 Ch 29가 읽지 않음(바꿔도 계약 밖).

## 8. 삽화 비유 계열 후보

**이미 쓴 계열**(과정 요약·계약·각 챕터 요약·`figures/*.prompt.md` 167개 grep): 카드·봉투(21)·서랍(15)·쟁반(tray 51)·끈·단추·관·깔때기·그릇·클립보드(16)·도장(stamp 11)·저울(scale 14)·나무 길·갈림길·나무 레일·작업대(Ch 13·18)·나무판·구멍·마개(Ch 14)·사과·바구니·모래시계·궤짝·선반(Ch 15)·쪽지·덮개 천·두루마리·개찰구·체(Ch 16)·눈 위 발자국·말뚝·울타리(Ch 17)·점토·물레·가마(Ch 18)·공항 검사·우편 가림막·전화 연결·방문자 명부·안내 데스크(Ch 22)·식당 벽·메뉴판 카드·주문 전표·같은 색 집게·내주는 창(Ch 19)·**자료실 승강 상자(dumbwaiter 5 — 모두 Ch 20)**·계수기·파란 책·빈 회색 카드(Ch 20). prompt grep에서 `oven`(9)·`window`(13)·`dial`(7)·`clock`(8)·`robot`(5)·`puzzle`(5)·`press`(6)·`form`(8)이 이미 있습니다. **`washing`·`laundry`·`sewing`·`coffee`·`drip`·`kettle`·`motor`·`crank`·`dough`·`porthole`·`vending`·`music box`·`loom`은 0건**(`bread` 1·`pulley` 1).

| 후보 | 그림 요소(절별) | 장점 | 겹침·위험 |
|---|---|---|---|
| **A. Ch 20 「자료실 승강 상자」에 모터를 단 판(이어 가기)** — 손잡이 도르래(Ch 20 직접 조립) ↔ 버튼 하나 모터 상자(`create_agent`) | 01 같은 상자·통로에 손잡이 대신 작은 모터 상자와 버튼 하나, 쪽지가 있으면 내려갔다 파란 책을 싣고 옴 · 02 창구에 받침 두 가지(책을 칸 틀에 끼워 올리는 받침 ↔ 상자 바닥에 붙은 칸 틀) · 03 책과 함께 오르내리는 꼬리표(상태) ↔ 창구에만 걸린 방문증(컨텍스트, 상자에 안 실림) · 04 떼어 낸 손잡이 부품과 새 모터 부품을 나란히 · 05 서고 책장에서 필요할 때만 꺼내는 상자 · 06 같은 책 목록 옆 늘 한 번 내려가는 상자 ↔ 쪽지가 있을 때만 내려가는 상자 | **Ch 20에서 바로 이어짐**(「직접 만든 루프를 한 함수로」가 그림 하나로 읽힘), 같은 자료실 소재, 파란 책·빈 카드 약속을 그대로 | 승강 상자 그림이 Ch 20 다섯 + Ch 21 여섯~일곱으로 길어져 새로 볼 것이 적음 · Ch 20 04가 이미 「규칙 ↔ 모델」을 이 상자로 그림(06과 겹침) · 모터·버튼이 작으면 판독 어려움 |
| **B. 세탁기 코스 버튼과 동그란 창** — 손빨래 도구 여럿(대야·빨래판·헹굼 통 = 직접 이은 부품) ↔ 코스 버튼 하나 세탁기 | 01 동그란 창 안에서 빨래가 도는 모습(되풀이가 보임) · 02 개어 나오는 두 방식(칸 나뉜 바구니를 끼우는 것 ↔ 기계 안에 칸이 있는 것) · 03 빨랫감에 붙은 이름표(상태, 끝나고도 남음) ↔ 다이얼 옆 코스 카드(컨텍스트, 옷에 안 남음) · 04 옛 세탁기 다이얼과 새 세탁기 버튼판을 나란히(같은 코스가 다른 자리) · 05 세제 통에서 필요할 때만 세제가 들어가는 투입구 · 06 같은 빨랫감 두 더미를 두 방식으로 | 0건 · 「한 버튼 = 안에서 되풀이」가 창으로 보임 · 03 상태/컨텍스트 차이가 뚜렷 | 버튼·다이얼 숫자·글자 금지라 코스를 색·모양으로만 · 창·표시등이 관계와 무관한 색 요소가 되기 쉬움(규격 §5-4 탈락 원인) · 자료실 소재와 무관 |
| **C. 자동 제빵기** — 반죽 그릇·밀대·오븐(따로 놓인 부품) ↔ 뚜껑 창 달린 제빵기 한 대 | 01 창 안에서 반죽이 섞이고 부풀고 구워짐 · 02 빵틀 두 가지(끼우는 틀 ↔ 기계에 붙은 틀) · 03 빵(상태) ↔ 조리 카드(컨텍스트, 기계가 읽고 빵엔 안 남음) · 04 옛 기계 부품과 새 기계 부품 · 05 재료 자동 투입구(필요할 때만 열림) · 06 같은 재료로 손반죽 ↔ 제빵기 | 0건(`dough`·`bread maker`) · 부품 → 한 기계가 분명 | **부엌 계열(Ch 1·5·6·15 `kitchen`·`oven` 9)과 겹침** · 빵 모양 차이를 그림으로 가르기 어려움 |
| **D. 재봉틀(발판)** — 바늘·실·가위를 따로 쓰는 손바느질 ↔ 발판 하나 재봉틀 | 01 바늘이 오르내리며 되풀이, 천이 밀려 나감 · 02 종이 본을 대고 박기 ↔ 무늬판 내장 · 03 천에 박힌 실(상태) ↔ 실패 색 카드(컨텍스트) · 04 옛 손재봉 부품과 새 부품 · 05 실이 떨어질 때만 북실을 꺼냄 · 06 같은 천 두 장 | 0건 · 오르내리는 바늘이 「되풀이」를 보여 줌 | 학생에게 덜 익숙 · 작은 부품이 많아 판독 어려움 · 03 비유가 약함 |

- **이어 갈지 새로 갈지**: A는 이음새가 가장 강하고 「Ch 20에서 손으로 돌리던 것을 한 장치로」가 챕터 제목과 곧바로 맞지만, Ch 20 그림 다섯과 비슷한 장면이 이어지고 04·06이 Ch 20 04와 겹칩니다. B·C·D는 새 계열이라 새로 볼 것이 있지만 자료실 소재와 끊기고, 버튼·창·표시등이 과한 색 요소가 되기 쉽습니다. 01만 A(모터 단 승강 상자)로 Ch 20을 잇고 02~07을 새 계열로 가는 섞기는 한 챕터 한 계열 선례(Ch 19·20)와 어긋납니다. 사람·손·동물·화면·글자·숫자·화살표를 넣지 않는 것이 Ch 19·20 선례입니다.

## 9. 위험과 깨진 것

1. **06 ↔ Ch 29 04 파일 계약**(§4-6) — 3줄·키·`tool_calls ≥ 1`. 06을 다시 실행하면 Ch 29 04 `_src` 인용 값(평균 519.7토큰·1.880초·p95 2.094초·토큰 p95 541 등)이 어긋남(Ch 29 대기 — 인계). 에이전트가 검색 없이 답한 질문이 생기면 Ch 29 04 `assert`가 깨짐 → 06은 흔들림 확인(에이전트 도구 호출 수) 먼저.
2. **06 판정 흔들림**(C01 2/3 ↔ 3/3 기록) — 판정 비교를 결론에 쓰면 규격 §2-7 9번 끝과 부딪힘. 판정 여섯 번 × 흔들림 확인 다섯 번이 요청 수의 큰 몫.
3. **02 구조화 출력 관찰**: 메시지 3 ↔ 2는 첫 요청에서 양식이 맞을 때의 구조(결정적에 가까움), 양식 칸 값(`R-14`·`자료 R-14`)은 흔들림. `assert`를 모델 글에서 구조(메시지 종류 목록·AI 메시지 수·`structured_response` 자료형)로.
4. **05 재검색 관찰**이 모델 선택에 달림(주차 질문에서 두 번 검색하는가 — 한 응답에 요청 둘일 수도). 낱말 겹침 규칙이 한 글자 낱말로 거의 모든 질문에 걸림(§2 05) → 「검색 결과 없음」 장면이 규칙 쪽 우연에 기댐.
5. **01 외부 렌더 요청**(mermaid.ink) — 키 없는 학생·오프라인에서 멈춤, 바이트 수 인용 불가. **01 `KeyError`**(없는 주제) — 모델이 다른 주제어를 만들면 셀이 멈춤.
6. **모델 설정**: 01~05 `temperature`·`reasoning_effort` 없음(G4가 놓침) → 모델 객체로 바꾸면 옛 출력과 다른 조건. Ch 30 09(대기)가 「`init_chat_model`과 `create_agent`」를 전제.
7. **Ch 22(완료)와 어긋날 위험**: 01이 도구를 부르는 실행을 잃으면 Ch 22 01 b4가 거짓 · 반환 힌트·`tools=` 키워드·모델 객체 모양을 Ch 22와 다르게 가르치면 Ch 22에서 모양이 바뀜(Ch 22는 고치지 않음) · 도구 파일 함수 이름이 Ch 22 노트북 이름(`mask_pii`·`lookup_hours`·`record_*` 훅 등)과 겹치지 않게.
8. **제목 깨짐**: 04 「0x에서 1x로」(점 빠짐) · 절 제목 밑줄이 공백(§7-5).
9. **실행하지 않은 사실·틀린 사실**: 03 b3 「MessagesState」 · 04 대응표 셋째 줄(「별도 후처리」) · 04 b3 「Ch20의 직접 조립 그래프를 사용합니다」(사용 안 함) · 05 제목·b4 「리트리버(retriever)는 … 검색 인터페이스」(코드에 없음) · 05 학습 목표 「재검색 횟수 제한」(코드 제한 없음) · 06 설명 셀 「Ch6에서 배운 `with_structured_output(…, method=…, strict=True)`」(부분 참) · 06 b4 「평가 표본은 Ch14 …」(Ch 14 설정 256차원과 다름) · 모든 절 b8 「(다음 슬러그)에서 이 결과를 다시 사용합니다」(다음 절이 결과를 다시 쓰지 않음) · 06 b8 「Ch22 Middleware에서 이 결과를 다시 사용합니다」(Ch 22는 06 결과를 안 씀 — 실제로 쓰는 곳은 Ch 29 04).
10. **옛 생성기 `_author_ch21_ch29.py`가 Ch 21과 대기 챕터 Ch 29를 함께 덮어씀**(§3) — 막는 방법이 두 챕터에 걸림.
11. **Part 6 옛 검사 넷·`check_visual_reports.py`** — 이미 Ch 22 개선으로 어긋난 상태, 고치지 않고 기록. `check_notebook_readiness.py`는 결과 파일을 먼저 씀(되돌림).
12. **절 수·실습 절**: `check_scope.py` `SECTION_COUNTS` ch21 = 6 · `_notebook/build_index.py` 46행 절 수 6 → 실습 절을 붙이면 7(선례: 뒤 것은 전체 마감 몫).
13. **판 차이**: 잠금 `numpy>=2.0`·`pillow>=11.0` 범위 표기(과정 관례 `==`) · pillow import 0 · `%pip` 두 줄에 판 없음 → 도구 파일에 NumPy를 쓰면 `%pip`에 `numpy==2.5.3`(Ch 14 선례). 잠금을 바꾸면 `uv lock`(마운트 폴더라 `uv sync` 막힘 — 가상환경엔 `uv pip install`).
14. **서비스 요청 어림**: 노트북 한 번 35번(모델 27 · 임베딩 8). 새 커널 두 번 70 + 노트북 밖 다섯 번(01 2 × 5 = 10 · 02 2 × 5 = 10 · 03 2 × 5 = 10 · 05 5 × 5 = 25 · 06 에이전트 흐름 모델 6 + 도구 안 임베딩 3을 × 5 = 45, 판정까지면 + 30) + 04 선택지 (나)면 +3 × 7 + 07 실습 절(3~5 × (2 + 5) ≈ 35) → **약 200~260번**(06 판정 흔들림 확인까지 넣으면 약 290번). 요금표로 어림한 예상 비용은 0.1~0.2달러(Ch 20 203번 0.058달러, 에이전트 흐름 입력이 약 450토큰으로 Ch 20보다 조금 큼 — 청구 금액 아님). 06 한 번 실행 요청 23번은 옛 기록상 흐름 여섯의 걸린 초 합 약 9.3초 + 판정 여섯·임베딩 — 기기 셸 180초 안으로 보이지만 이번에 재지 않았습니다.
15. **디스크·환경**: 기기 루트 여유 **1.8G**(작업 전후 같음 — pip 캐시 안 씀, uv 캐시 `/tmp/uv-cache` 387MB 그대로). 가상환경은 마운트 폴더(328MB). Mermaid 도구(`/tmp/mmd`·`/tmp/libs`·`/tmp/pptr-cache`·`/tmp/pw`) 있음. 루트 `.env`에 `OPENAI_API_KEY` **이름** 있음(값은 보지 않음).

## 10. 01절 작업자가 먼저 결정해야 할 것

1. **모델 셀과 에이전트 호출 모양** — 과정 표준 모델 객체(`nbkit.key_and_model_cells()`, `temperature=0`·`reasoning_effort="none"`)를 `create_agent(model, tools=[…], system_prompt=…)`에 넘길지(Ch 22·Ch 30 09 모양), 01의 `draw_mermaid_png()`(외부 요청)를 `draw_mermaid()` 구조 문자열만으로 바꿀지, 규정 글을 Ch 20 `POLICIES`(토요일·「1인 5권까지 14일 동안」·`raise ValueError`)에 맞출지, 01 도구 흐름(모델 → 도구 → 모델)을 유지해 Ch 22 01 b4를 지킬지. `system_prompt`의 과정 말(「시스템 메시지 글」 — Ch 16) 결정.
2. **도구 파일(§6)** — A(만들지 않음) / B(필요한 것만 새 파일 하나 — 이름 `rag_tools.py`·`llm_tools.py`·`policy_tools.py` 등, `agent_tools.py`·`graph_tools.py`는 피함) / C(두 파일) / D(06만). 06 검색을 Ch 14 모양(`search_hits`·거리·`dimensions=256`)으로 바꿀지, 판정을 Ch 15 02 모양(`judge_once`)으로 바꿀지. **06 저장 줄의 Ch 29 계약 키(`agent_usage.model_calls`·3줄·`tool_calls ≥ 1`·`agent_latency_s`)는 바꾸지 않음.** 결정은 `handoff.md`에.
3. **클래스·힌트 범위(§7-1~7-4)** — 양식 클래스 `BaseModel` 유지(「양식 클래스」 말) · `SupportState(AgentState)` 상속을 조건부 예외로 둘지 · 컨텍스트를 데이터 클래스 / `TypedDict` / `BaseModel` 가운데 무엇으로 · `ToolRuntime` 힌트(라이브러리가 읽는 값) 허용과 제네릭을 뺄지 · `@tool` 반환 힌트를 뺄지(Ch 19·20) 둘지(Ch 22).
4. **04 옛 API를 어디까지 실행할지(§7-6)** — (가) 1.x에 남은 `create_react_agent`로 모델 없이 그래프 견주기 / (나) 옛·새 함수 모두 invoke / (다) 글·표만. 「0.x 판 자체는 실행하지 않음」 문장과 대응표 셋째 줄 고침. 제목 「0x에서 1x로」 표기(강사 확인 대상으로 올릴지).
5. **흔들림 확인 계획과 `assert` 대상** — 노트북 밖 다섯 번을 먼저: 01(도구 호출 요청 수·도구 인자 `topic`) · 02(메시지 종류 목록·AI 메시지 수·양식 재요청 여부) · 03(도구를 부르는가) · 05(검색 호출 수·검색어 차례·한 응답 요청 수) · 06(에이전트 흐름 도구 호출 수 — **Ch 29 `tool_calls ≥ 1` 계약**, 판정 여섯). 모델 글에 건 `assert` 다섯(01·02·03·04·05)을 코드가 정하는 값(메시지 종류, 키, 자료형, `request_tag`)으로 바꿀지. 05 소재(낱말 겹침 ↔ Ch 14 임베딩 검색)와 06 결론 기준(요청 수·도구 호출 수·입력 토큰, 판정·걸린 초는 둘째 단락·표에만).

## 11. 챕터 마감으로 미룰 것

- **07 실습 절 신설**(규격 §7-2): 슬러그 후보 **`07-create-agent-실습`**(선례 `05-ToolNode-실습`·`09-Middleware-실습`·`07-모델과-도구-실습`·`06-Agent-개요-실습`·`08-LangGraph-실습` — 챕터 제목의 앞말, 01 슬러그처럼 밑줄을 줄표로), 제목 「create_agent 실습: …」(`chapter.json` 제목 표기에서 밑줄을 살릴지 §7-5와 함께), `format: experiment`, meta 「실습 30분 · 새 용어 0」(**챕터 시수 6·10h에 더하지 않음**). 요청 3~5번, 새 문법·API 0. 주제 예 — 자료실 문의 에이전트 하나에 01 루프 + 02 구조화 출력(ToolStrategy) + 03 컨텍스트(접근 수준)를 붙이고 값 하나만 바꿔 다시(예: `access_level` 또는 양식 전략). 요청 수가 모델 선택에 달려 흔들림 확인 대상. **06 계약 파일은 실습 절이 쓰지 않음**(Part 3 실습 절 선례 「파일을 쓰지 않습니다」). 따라오는 것: `chapter.json` 절 추가 · `textbook/part6/_build_index.py` 19행(시수 6·10 그대로, 설명) · 챕터 `qa/public-files.json`(경로 배열 — 노트북·HTML 줄을 직접 더함, 글롭 아님) + `textbook/part6/public-files.json` · `textbook/_notebook/build_index.py` 46행(절 수 6, 선례대로 둘지) · `check_scope.py`(기록만) · 06 「다음 학습과 이어지는 지점」을 07로.
- 옛 생성기 `figures/_gen_figures.py` `mv -n` → `qa/upgrade/before/generators/blocked/` · **공용 `_author_ch21_ch29.py`는 옮기지 않음**(Ch 29 몫 — 막은 판을 그대로 두고 인계).
- 옛 그림 18개(`figures/0N-흐름.{svg,excalidraw,caption.md}`) 삭제 승인 목록(사본 `before/figures/`, `final-artifact-hashes.json`이 해시를 적어 둔 기록 파일).
- `chapter.json` `objectives`(Ch 29와 같은 두 줄 → 절별)·절 제목 표기, `textbook/part6/_build_index.py` 19행 설명을 개선 본문과 대조 → `_build.py`·`_build_index.py`.
- 실습 폴더 README 다시 쓰기(노트북 일곱, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 06이 Ch 14 자료를 읽고 `data/rag-comparison.json`을 씀 — Ch 29 04가 읽음, 요청 수·예상 비용, 도구 파일을 만들면 그 단락, 「절당 1달러 미만」 뺌) · `labs/part6/continuity-guide.md`(도구 파일을 만들면) · `qa/research.md`·`technical-notes.md`·`verification.md`·`집필점검표.md`(「개선 전 판」 표시 — 학생 묶음 밖).
- `part6-practice.zip` 재생성(`python3 textbook/part6/_build_index.py`) → `check_delivery.py`(`llm-practice.zip` Stale 예상) · 옛 검사 넷 돌려 기록(`check_notebook_readiness.py`는 결과 파일 되돌림) · `check_bundle_execution.py`(Ch 21 안 돌림 — Ch 24·28 PASS만 확인).
- **뒤 챕터 인계**: Ch 29 04(파일 계약·인용 값 — 새 해시·새 값) · Ch 29 01 b3(느슨한 문장) · Ch 27 01·02 b3 · Ch 30 01·02·03·09 b3(09 「init_chat_model과 create_agent」, 03 「상태 사전」 — 「사전」 금지어는 Ch 30 몫) · Part 6 소개·`practice-start.md`·continuity-guide 둘 · Ch 22(완료) 01 b3·b4·02 문장 대조.
- 삭제 승인 대상: 실습 폴더 `.venv`(macOS 211MB) · `qa/upgrade/gates-wip-*.json` · `qa/upgrade/__pycache__` · `.cache/vm/venv-ch21-create-agent`(328MB) · 기기 `/tmp/ch21-prep`.

## 12. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 6 · `notebooks` 6 · `figures` 19(SVG·excalidraw·caption 각 6 + `_gen_figures.py`) · `generators` 2(**공용 `_author_ch21_ch29.py` 사본**·`_gen_figures.py`) · `qa` 5(`prerequisite-files.json`·`public-files.json`·`research.md`·`technical-notes.md`·`verification.md`) · `data/rag-comparison.json` · `pyproject.toml`·`uv.lock`·`README.md`·`chapter.json`·`집필점검표.md`·`_build.py`·`index.html`(목차, objectives 대조용) = **46개, 556KB**. 원본과 `cmp` 모두 같음(원본은 그대로). `runs/`·`tests/`는 실습 폴더에 없어 없음 |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 251, 통과 0/6), `216e1760…` |
| `qa/upgrade/before-manifest.json` | sha256 **73개** — ① 이 챕터가 읽거나 가져올 수 있는 앞 챕터 파일: Ch 14 `documents.json`·`queries.json`·`rag_tools.py` · Ch 15 `rag_tools.py` · Ch 17 `agent_tools.py`(이름 피함) · Ch 19 `order_tools.py` · Ch 20 `graph_tools.py` ② Ch 21에 기대는 완료 챕터 파일: Ch 1 01·Ch 7 05·Ch 20 01·05 `_src`·Ch 20 05 노트북 · Part 5 소개 · `labs/part4`·`labs/part5` continuity-guide · **Ch 22 01·02 `_src`·01 HTML·01 노트북** ③ Ch 21에 기대는 대기 챕터 파일: **Ch 29 04 노트북(파일 계약)**·04·01 `_src`·README·`qa/prerequisite-files.json` · Ch 27 01·02 · Ch 30 01·02·03·09 `_src` · Part 6 소개·`practice-start.md`·`labs/part6`·`labs/part7` continuity-guide · **공용 생성기 `_author_ch21_ch29.py`** ④ 묶음·목록·기록: `part6-practice.zip`(`0543ea63…`)·`llm-practice.zip` · Part 6 `public-files.json`·`prerequisite-files.json` · 챕터 `qa/public-files.json`·`prerequisite-files.json` · **`rag-comparison.json`(`122cfce2…`)**·실습 폴더 `pyproject.toml`·`uv.lock` · Part 6 `final-artifact-hashes.json`·`existing-artifact-hashes.json`·`integration-results.json`·`bundle-execution.json`·`lesson-scope.json`·`notebook-readiness.json`·`notebook-executions.json`·`visual-results.json`·`figure-consistency.json`·`shared-tests.json`·`language/ch21-ch29-final.json` · Part 7 `existing-artifacts-before.json` · `notebook-contracts-part6-ch21-create-agent.json` · `textbook/index.html`·`part6/index.html` ⑤ 규칙·검사·빌드: `part6/_build_index.py` · `_notebook/build_index.py`·`build_bundle.py` · Part 6 `check_bundle_execution.py`·`check_scope.py`·`check_figures.py`·`check_notebook_readiness.py`·`check_delivery.py`·`collect_public_files.py`·`check_visual_reports.py` · `verify.py`·`tests/test_verify.py` · `_template/builder.py` · 챕터 `_build.py` |
| `$ROOT/.cache/vm/venv-ch21-create-agent` | Python 3.12.13 · 328MB |

### 가상환경 만든 방법과 결과

- `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy uv venv --python 3.12.13 …/venv-ch21-create-agent`. 잠금 목록은 `uv export --project labs/part6/ch21-create-agent --frozen --no-hashes --all-groups --no-emit-project`(실습 폴더 파일은 그대로 — `pyproject.toml`·`uv.lock` 수정 시각 전후 같음), 주석·빈 줄만 빼고 환경 표시는 남김(89줄, `/tmp/ch21-prep/req-clean.txt`).
- Ch 16~20 선례대로 `uv pip install pip==26.2` → **`bin/python -m pip install --no-cache-dir -r`**(루트 디스크에 pip 캐시를 남기지 않음). 설치 오류 0, **uv 캐시 정리(`uv cache prune`) 안 함**.
- 결과: `pip freeze`와 잠금 대조 **판 차이 0**(설치 84 = 잠금 89 − 이 기기에 해당하지 않는 다섯: `appnope`(darwin)·`colorama`(win32)·`cffi`·`pycparser`(PyPy)·`httpx2-jsfetch`(emscripten)). `langchain 1.4.0` · `langchain-core 1.6.2` · `langchain-openai 1.6.0` · `langgraph 1.2.11` · `langgraph-prebuilt 1.1.0` · `langgraph-checkpoint 4.2.0` · `openai 3.11.0` · `numpy 2.5.3` · `pillow 12.3.0` · `pydantic 2.13.5` · `python-dotenv 1.2.3` · `ipykernel 7.3.0` · `nbclient 0.11.0` · `pip 26.2` · `ruff 0.15.6` · `tiktoken 0.14.0` · `httpx 0.28.1` · `langsmith 0.12.4` · `IPython 9.17.1` · `nbformat 5.11.1` · `jupyter-client 8.10.0` · `pyzmq 27.2.0`. `pip check` 이상 없음. 커널 스펙 `share/jupyter/kernels/python3` 있음.
- import 확인만: `from langchain.agents import create_agent, AgentState` · `from langchain.agents.structured_output import ToolStrategy, ProviderStrategy, AutoStrategy` · `from langchain.tools import tool, ToolRuntime` · `from langchain.chat_models import init_chat_model` · `from langchain.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage` · `from langchain_openai import OpenAIEmbeddings` · `from langgraph.graph import StateGraph, START, END` · `from langgraph.prebuilt import ToolNode, tools_condition, create_react_agent` · `from langgraph.errors import GraphRecursionError` · `pydantic`·`typing_extensions`·`numpy`·`dotenv`·`ipykernel`·`nbclient`·`nbformat`·`jupyter_client`·`IPython`·`zmq`·`PIL`. `run_section.sh`는 `$ROOT/.cache/vm/venv-<챕터 폴더 이름>`을 자동으로 씁니다.
- §5 확인은 이 가상환경에서 `env -u OPENAI_API_KEY`로 키를 뺀 채 했습니다.

### 참고 자료 (2026-09-25 확인)
- LangChain v1 이주 안내 `https://docs.langchain.com/oss/python/migrate/langchain-v1`(import 이동 · `prompt` → `system_prompt` · 훅 → 미들웨어 · 사용자 상태 「TypedDict only」 · 구조화 출력 「in the main loop, reducing cost and latency」 · 컨텍스트는 `context=` · 스트림 노드 이름 `agent` → `model` · `ToolNode`를 도구로 직접 넘기지 않음).
- Structured output `https://docs.langchain.com/oss/python/langchain/structured-output`(두 전략 · 프로필로 자동 선택 · 「Returning structured response」 · `handle_errors` · 지원 양식 넷 · `structured_response`).
- Agents `https://docs.langchain.com/oss/python/langchain/agents`(`model=`·`tools=`·`system_prompt=` · 모델 글자 또는 객체 · 「An agent is a model calling tools in a loop」 · `AgentState` 상속 · `context`·`context_schema`는 데이터 클래스 예).
- Retrieval `https://docs.langchain.com/oss/python/langchain/retrieval`(2-Step RAG 「Retrieval always happens before generation」 ↔ Agentic RAG 「decides when and how to retrieve」, 요청 수 「Fixed」 ↔ 「Variable」).
- 설치판 소스: `langchain/agents/factory.py` 28·560~600·995~996·1011~1030·1083~1097·1263·1357~1359·1380~1439·1672~1735·1923~1975·2004~2037행 · `langchain/agents/middleware/types.py` 349~361행 · `langgraph/prebuilt/chat_agent_executor.py` 53~104·274~305행 · `langgraph/prebuilt/tool_node.py` 1663행 · `langgraph/warnings.py`(`LangGraphDeprecatedSinceV10` → `DeprecationWarning`) · `langchain_core/runnables/graph.py` 639~645행 · `graph_mermaid.py` 405~423행.
