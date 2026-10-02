# Ch 25 Streaming — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part6/ch25-streaming`(절 셋 — 01·02·03 모두 experiment) · `labs/part6/ch25-streaming`. 바로 앞 Ch 24(완료, 모델 요청 0)를 잇는 Part 6 다섯째 챕터입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본 33개, 404KB — 원본과 `cmp` 모두 같음) · `gates-before.json`(`967671a0…`) · `before-manifest.json`(147개, `d5114134…`) · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch25-streaming`.
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(전부) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 과정 요약(전부) · 계약 파일(§3 Ch 18~24 줄 · §4 Ch 15~24 줄 · §5 · §8) · Ch 24 `chapter-summary.md`(전부)·`chapter-lead-notes.md`·`before-manifest.json` · Ch 21 `chapter-lead-notes.md`(목차·모델 관련 줄) · Ch 2 12 · Ch 6 04·06 · Ch 15 05 노트북·`_src` · Ch 26·Ch 30 `_src`의 Ch 25 문장 · Ch 30 `agent_service` · 공용 옛 생성기 · Part 6 목록·묶음·검사 스크립트 · 챕터 `qa/` 기록 일곱. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.
- **원고·노트북·그림은 하나도 고치지 않았습니다.** 연결 폴더 안 파일 삭제 0건, 노트북 실행 0건, 서비스 모델·임베딩 요청 0건, `uv cache prune` 안 함. 확인은 기기 `/tmp/ch25-prep/exp/`의 작은 그래프(`e1.py`~`e5.py`, `env -u OPENAI_API_KEY`)와 설치판 소스·공식 문서로 했습니다. `e3.py`만 `messages` 모드 모양을 보려고 `GenericFakeChatModel`을 썼습니다(조사 전용 — 교재에 넣으면 규격 §3 위반).
- `chapter.json` `hours` = 「총 8h · 강의 3h · 실습 5h」. 절 meta 합 강의 1+1+1 = **3h**, 실습 1.5+1.5+2 = **5h** → 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part6/_build_index.py` 23행 (3, 5)·`qa/check_scope.py` `EXPECTED` (3, 5)도 같습니다. 새 용어 meta 5+5+5 = **15**(옛 생성기가 세 절 모두 「5」로 찍은 틀 값 — 실제 새 말 목록 없음).

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-25)

| 절 | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 일곱 가지 stream mode | 4 | 83 | 3 | 1 | 0 | 0 | 5 | 28 | 3 | 40 |
| 02 토큰과 중간 진행 스트리밍 | 4 | 81 | 0 | 2 | 0 | 1 | 5 | 23 | 3 | 34 |
| 03 TTFT와 total 비교 | 5 | 85 | 4 | 6 | 0 | 1 | 5 | 31 | 3 | 50 |
| **합계** | **13** | **249** | **7** | **9** | **0** | **2** | **15** | **82** | **9** | **124** |

- 통과 절 **0/3**. 코드 줄(`count_code.py labs/part6/ch25-streaming/notebooks`) 41·61·76 = **178줄**.
- G1 7 = 셀당 함수 둘 1(01 c4 `prepare`·`write`) · 조건 표현식 3(01 c6 `… if events else "없음"` · 03 c6 `None if first_text is None else …` · 03 c10 `"첫 답변 …" if … else …`) · 집합 내포식 1(01 c8 `assert {mode for mode, _ in events} == …`) · 제너레이터 식 2(03 c8 `next(r for r in rows if …)` · 03 c10 `sum(r["estimated_usd"] for r in rows)`).
- G2 9 = 15줄 넘는 셀 6(01 c4 20 · 02 c4 20 · 02 c6 22 · 03 c4 21 · 03 c6 21 · 03 c8 17) · 한 글자 이름 `r` 2(03 c8·c10) · 호출 두 겹 1(03 c10 `round(sum(…))`).
- G3 0 — 셀마다 첫 줄 주석 한 줄뿐, 이유 주석 0.
- **G4 2 = 02 c4·03 c4 `init_chat_model(f"openai:{MODEL}", reasoning_effort="none")`에 `temperature` 없음.** 가짜 모델 0. 01은 모델 셀이 없어 0.
- G5 15 = 절마다 제목 셀 없음·핵심 그림 첨부 없음 6 + 결과 읽기 인용 없음 6 + 마지막 코드 셀 뒤 결과 읽기 없음 3(결과 읽기 셀 자체가 0).
- G6 82 = 70자 초과 37(13·9·15) · 영문으로 시작해 조사가 붙은 문장 45(15·14·16). 금지어는 G6가 대부분 세지 않습니다(§1 표).
- G7 9 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 것 (AST로 따로 셈, `/tmp/ch25-prep/ast_scan.py`)

- **f-string**: 01 c4 `f"{state['topic']} 스트리밍 요약"`(계산) · 01 c6 `f"mode-{index}"`·`f"{mode:11} events={len(events):2} first={sample_type}"`(형식 지정·계산) · 02 c4·03 c4 `f"openai:{MODEL}"`. Ch 13~24는 f-string 0건.
- **타입힌트**: 노드 모두 `(state: State) -> dict[str, str]` · 03 `measure(mode: str, question: str) -> dict`. Ch 13·20·23·24 노드는 힌트 0.
- **클래스**: `class State(TypedDict)` 셋(칸만 — L5 범위). 세 노트북 모두 이름 `State`, 칸이 다름(01 `topic`·`draft` ↔ 02·03 `question`·`answer`) → Ch 13·23·24 규칙 「칸 구성이 바뀌면 새 이름」과 다름.
- **그 밖**: `enumerate`(01 c6 — Ch 6 04 22셀에서 씀) · `for mode, data in …` 튜플 풀기(01 c8·02 c6 — Ch 6 04 12셀 `for role, content in messages`에서 씀) · `chunk, metadata = data` 대입 풀기(02 c6)·`chunk, _ = data`(03 c6, `_` 이름) · **호출한 결과를 바로 호출** `get_stream_writer()({...})`(01 c4 둘·03 c4) · `[Path.cwd(), *Path.cwd().parents]` 별표 풀기(02·03 c2 — 과정 요약 2-2 금지 모양) · `.get(…, {}).get(…)` 사슬·`row.update({...})`·숫자 밑줄 `1_000_000`·식 안 요금 숫자 `0.75`·`0.075`·`4.50`(03 c8) · 노드 안에서 노트북 전역 목록 `call_records.append`(03 c4) · 노드 안 `assert`(03 c4) · `assert A and B and C`(02 c6) · 함수 본문 16줄(03 `measure` — 규격 L2 10줄 넘음) · `"".join(preview)`(02 c6 — Part 3 0건, Ch 6 04는 `+`로 이음) · `type(events[0]).__name__`(01 c6 — Ch 6 04에서 씀).

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청 | 파일 쓰기 | 손 값 | 금지 문법(셀) | 금지어(`_src` 본문/노트북 md/코드 주석) | `assert`(무엇에) |
|---|---|---|---|---|---|---|---|
| 01 | 노드 둘(`prepare`·`write`, 노드마다 `get_stream_writer()`로 진행 값 50·100) + `InMemorySaver` 그래프를 **일곱 모드로 따로 일곱 번**(스레드 `mode-0`~`mode-6`) 실행해 사건 수·첫 자료형 출력(values 3·updates 2·messages 0·custom 2·checkpoints 4·tasks 4·debug 8) · 여러 모드 목록 `["updates","custom"]` → `(mode, data)` 튜플 넷 | **0** | 없음(메모리 체크포인터) | 진행 값 50·100(코드가 정한 값) · 입력 `"고객 문의"`·`"배송"` | c4 함수 둘·20줄·힌트·f-string 계산·호출 결과 호출 · c6 조건 표현식·f-string 형식 지정·`enumerate` · c8 집합 내포식 | 반환 3/2/0 · 조각 2/0/0(**Ch 5 토큰 전용**) · 스냅숏 1 · 로그 1 · 분기 0/1 · 소비(자) 7/2 · 옵션 1 · 필드 2/1 · 메타데이터 1 · 재개 1(b3) · 측정 1 · 태스크 5 · 디버그 1 · 구현 1/1 · v1·v2 3 · **제목 「stream mode」** | 3 — `counts["messages"] == 0`·`counts["custom"] == 2`·모드 집합(모두 결정적) |
| 02 | 노드 하나 `answer`가 모델 앞뒤로 진행 값 30·100을 쓰고 `model.invoke`로 두 문장 답 · `stream_mode=["messages","updates","custom"]` 한 실행에서 사건 수 세기(messages 88·내용 있는 조각 84·updates 1·custom 2) · 내용 조각을 이어 붙인 글 == 최종 상태 `answer` · 표시 문구 딕셔너리 셋 | **1** | 없음 | 진행 값 30·100 · `cost_limit_usd` 1.0 출력 · b5 「예상 API 비용은 1달러 미만」 | c2 별표 풀기 · c4 20줄·힌트·f-string · c6 22줄·`assert A and B and C`·대입 풀기 | 반환 4/4 · 지연 1 · **조각 18/4/1** · 로그 1 · 도메인 1 · 메타데이터 0/2 · 재개 1 · 측정 2 · 명시 0/1 · 정확 1/1 · 필터링 1 · TTFT·total·first_event 각 1 | 2 — `seen` 셋(구조) · 이어 붙인 글 == 최종 답(구조, Ch 6 04 `assert same_text`와 같은 성질) |
| 03 | 같은 질문을 `updates`·`messages`·`custom` **세 번 따로 실행**하며 `measure()`가 첫 사건·내용 있는 첫 조각(「TTFT 근삿값」)·끝을 `perf_counter`로 잼 · 호출마다 사용량·손 요금으로 「추정 비용」 · 교재 출력 2.622/2.622 · 0.613/0.620/1.101 · 0.003/1.431초, 비용 합 $0.00138825 | **3** | 없음 | **요금 0.75·0.075·4.50을 식 안에** · 1,000,000 · `cost_limit_usd` 1.0 · b6 시간·토큰·비용 전부 한 번 실행 값 | c4 21줄·힌트·전역 목록·노드 안 `assert`·호출 결과 호출 · c6 `measure` 본문 16줄·조건 표현식·힌트 · c8 17줄·제너레이터·`next`·`r`·`.get` 사슬·`update`·`1_000_000` · c10 조건 표현식·제너레이터·`sum`·호출 두 겹 | 반환 1/2/1 · 지연 1 · **추정 4/1** · **조각 10/4** · 로그 1 · 소비 1/1/1 · 재개 1 · **측정 8/3/1** · 이벤트 1 · 워밍업 1 · 공정 1/1 · 근삿값 8/1 · 단조 1/1 · `yield` 1 · **TTFT 13/3 · total 11/2 · first_event 9** · **제목 「TTFT」·「total」** | 3 — `usage_metadata is not None`(노드 안) · `len(call_records) == 3` · messages 줄 `ttft_s is not None`(모두 구조) |

- **서비스 요청 합계 4번**(01 0 · 02 1 · 03 3). 임베딩 0. 노트북 `%pip`은 세 절 모두 `langchain==1.4.0 langchain-openai==1.6.0 langgraph==1.2.11 python-dotenv==1.2.3`(01도 모델 패키지를 설치 — 쓰지 않음). 실습 폴더 dev에 `pip==26.2`, 잠금에 `pip 26.2` 있음(규격 §7-2 조건 충족).
- **`temperature=0`**: 0곳(G4 2). **`reasoning_effort="none"`**: 02·03 두 곳. 모델 이름은 `MODEL = "gpt-5.4-mini"`를 f-string으로 이어 붙임(규격 §3 기본 모양과 다름).
- **걸린 시간**: 03만 잼(주제 — §6). 02 b7 「외부 모델 호출의 응답과 지연은 …」·03 b7 「운영 기준은 반복 측정의 중앙값과 상위 백분위수」는 실행하지 않은 권고(백분위수는 Ch 15 06 말이지만 여기선 재지 않음).
- **옛 그림 토큰**: 절마다 b4 「도식 읽기」의 `{{svg:NN-흐름}}` 하나(`figures/_gen_figures.py`가 `textbook/part5/_figure.py`로 만든 상자 셋 흐름도, 02만 보라 `model`). 노트북 토큰 `{{notebook:slug}}` 셋. Mermaid·삽화 0장.
- 노트북 `metadata.verification`: 셋 모두 `passed`, 실행일 **2026-09-10**(16:26 UTC). `code_sha256` 앞 12자 01 `65fe9d1c1a28` · 02 `ca417f77a751` · 03 `6ca57c836214`. 파일 해시 `c7b77265…`·`f4f74415…`·`4bef74ac…`(`part6-practice.zip`·`llm-practice.zip` 안 판과 같음). 셀 수 9·9·11.
- 노트북 설명 셀: 제목(질문 한 줄) · 「실행 환경 준비」 · 소제목 + `_src` b4 「코드 읽기와 비교 경계」와 같은 글(옛 도구 `part6b_enrich.py`가 끼움) · 소제목 뒤 한두 문장(`part6b_review_fixes.py`가 더함) · **결과 읽기 셀 0**, 「이 노트북에서 할 일」·준비물(요청 수·비용·시간)·실행일 문장 없음, 셀 첨부 그림 0.
- `_src` 틀(옛 생성기 한 틀): b1 첫 줄 「{제목}의 핵심 구성 요소를 실제 출력에서 구분할 수 있습니다」(세 절 같은 모양) · **b3 세 절이 글자까지 같음**(「Ch23에서 …, Ch24에서 interrupt와 재개 사건을 확인했습니다」) · b7 둘째·셋째 항목 02·03 같음(키 검사·「응답과 지연」) · **b10 참고 자료 셋이 세 절 모두 같음**(Streaming 문서·StreamMode API·LICENSE, 확인 2026-09-11) · b9 복습 넷.

## 2. 절별로 더 봐야 할 것

### 01 일곱 가지 stream mode
- **슬러그 고정**: Ch 24 04 b8(완료)이 `../ch25-streaming/01-일곱-가지-stream-mode.html`을 링크하고 「**한 실행**에서 생긴 사건을 일곱 방식으로 받아 보는 방법」이라고 소개합니다. 그런데 지금 01은 **일곱 모드를 따로 일곱 번 실행**합니다(스레드 일곱). 설치판에서 `stream_mode`에 일곱 이름 목록을 한 번에 주면 **한 실행에서 사건 23개**(checkpoints 4·debug 8·values 3·tasks 4·custom 2·updates 2·messages 0)가 나오고, 두 번 돌려 개수와 차례가 같았습니다(e5, 결정적). → Ch 24 04 b8 문장이 참이 되려면 한 실행 목록 모양을 보이는 편이 맞습니다.
- **틀린 사실(설치판 출력과 다름)**: b4 정의·b7 둘째 항목·복습 2 「checkpoints와 **tasks**는 체크포인터가 있어야 사건이 생깁니다」 → 설치판에서 체크포인터 없이 **tasks 4개**(시작 둘·끝 둘)·**debug 4개**(task·task_result만)·checkpoints 0개(e1). 공식 문서 표는 tasks에도 「Requires a checkpointer」라고 적어 설치판과 어긋남 → **설치판 출력 기준으로 쓰고 문서 표기와 다르다는 사실을 b7에** 두는 쪽을 권합니다.
- b7 「기본 v1 형식에서는 (mode, data) 튜플 … version='v2'는 type·ns·data」 → 설치판 `stream(..., version="v2")` 있음(기본 `"v1"`). v2는 목록·단일 모드 모두 딕셔너리 `type`·`ns`·`data`(values는 `interrupts` 칸 추가, e2). 노트북에서는 실행하지 않은 문장.
- **기본 모드**: 컴파일한 `StateGraph`의 `stream_mode` 기본값은 **`"updates"`**(설치판 `graph/state.py` 1357행, e2 `graph.stream_mode` 출력). Pregel 클래스 기본값 `"values"`와 다름 → 「기본값」을 말하면 출력으로 확인한 값만.
- b4 정의가 한 문단에 일곱 모드를 모두 몰아 넣음(70자 초과 넷) · 「스냅숏」·「태스크」·「디버그」·「소비자」·「옵션」 · 「같은 실행을 재생하거나 복구하려면 checkpoints」는 실행하지 않은 권고.
- c6 `list(graph.stream(...))`은 끝난 뒤 한꺼번에 모음(본문이 그 사실을 밝힘 — 참). `graph.stream(...)`을 만들기만 하면 실행이 시작되지 않고 첫 `next`에서 시작(e4 — Ch 6 04 「stream()을 부르기만 하면 요청을 보내지 않습니다」와 같은 성질, 이어 쓰기 좋음).
- 사건 모양(설치판, e1): values = 칸 전체 딕셔너리(시작 입력 포함 3) · updates = `{노드 이름: 바꾼 칸}` · custom = 쓴 딕셔너리 그대로 · checkpoints = 키 여섯 `config`·`metadata`·`next`·`parent_config`·`tasks`·`values`(단계 -1 `input` → 0·1·2 `loop` — Ch 23 01 `get_state_history`와 같은 넷) · tasks = 시작 `id`·`input`·`name`·`triggers` / 끝 `error`·`id`·`interrupts`·`name`·`result` · debug = `type`(`checkpoint`·`task`·`task_result`)·`step`·`timestamp`·`payload`. **`id`·`timestamp`·체크포인트 아이디는 실행마다 다름 → 출력·인용 금지.**

### 02 토큰과 중간 진행 스트리밍
- **모델이 있어야 보이는 절**: `messages` 사건은 노드 안 `model.invoke(...)`에서도 나옵니다(공식 문서 「message events are emitted even when the LLM is run using .invoke」, e3 확인). 설치판 `langchain_core` `_should_stream`(chat_models.py 549~585행, `_generate_with_cache` 1969행에서 부름)은 **스트리밍 콜백이 붙었을 때만 스트리밍 요청**을 보냅니다 → `messages`를 구독하지 않은 실행의 `invoke`는 스트리밍 요청이 아닙니다(§03과 이어짐).
- **「조각」 문제(용어 약속 위반)**: 본문 18·노트북 4·출력 라벨(「내용이 있는 조각 수」). 규격 §4·과정 요약 §5 — 「조각」은 Ch 5 토큰 전용, 스트리밍 단위는 **「스트림 청크」**(Ch 6 04 정의, Ch 15 05도 씀). b4 「토큰 스트리밍 … 메시지 조각」도 「토큰 = 스트림 청크」로 오해하게 함(Ch 6 04 「청크와 토큰은 단위가 다름」).
- **흔들린 기록**: messages 사건 수가 옛 기록마다 **71 → 73 → 88**(`qa/ch25-second-technical-review.md`·옛 생성기 점검표·지금 출력) — 결론·그림에 넣을 수 없는 값. 결정적인 것은 「updates 1개·custom 2개」·「이어 붙인 글 == 최종 답」·차례(custom 30 → messages … → custom 100 → updates, e3 모양).
- `metadata`를 풀기만 하고 읽지 않음(`chunk, metadata = data`) → **Ch 30 09 b3 「Ch25에서는 `stream_mode="messages"`에서 모델 메시지 청크와 실행 메타데이터를 읽었습니다」가 부분 참**. 설치판 메타데이터 키: `langgraph_node`·`langgraph_step`·`langgraph_triggers`·`langgraph_path`·`langgraph_checkpoint_ns`·`checkpoint_ns`·`ls_provider`·`ls_model_type` 등(e3). `langgraph_node`만 출력하면 결정적.
- c8 「표시 문구」 딕셔너리는 사건을 받지 않고 딕셔너리만 출력(흐름과 무관 — 결과 읽기가 붙을 값이 없음).
- b7 「messages의 metadata로 노드 이름과 호출을 필터링할 수 있습니다」·「운영 기준 … 중앙값과 상위 백분위수」 — 실행 안 함.
- `custom` 진행 값 30·100은 코드가 정한 값이라는 설명은 참이고 좋음(b4) — 「정확한 진행률로 약속할 수 없습니다」.

### 03 TTFT와 total 비교
- **측정 설계의 결함(가장 큼)**: 세 모드를 **따로 세 번 요청**합니다. 그런데 설치판에서 `messages`를 구독한 실행만 스트리밍 요청을 보내고 `updates`·`custom` 실행은 일반 요청입니다(§02 `_should_stream`). 세 줄의 걸린 초는 받는 방법뿐 아니라 **요청 종류·답 길이(출력 91·84·111토큰)·서버 상태**가 모두 다른 값입니다. 본문 b4 둘째 단락이 이미 「공정하게 비교하려면 한 모델 호출에서 여러 모드를 동시에 구독」이라고 적었지만 코드는 그렇게 하지 않습니다.
- **Ch 15 05와 겹침**: Ch 15 05(완료)가 이미 `model.stream()` + `time.perf_counter()`로 **「첫 토큰 도착 시간(TTFT)」**과 **「전체 지연」**을 정의·측정했고(글자가 든 첫 스트림 청크 기준), 결론은 두 실행에서 같은 관찰 「첫 토큰이 끝보다 먼저 왔는가: True」·「첫 토큰 도착 시간이 전체 지연의 절반을 넘음(짧은 JSON)」만 적었습니다. 03의 새 말 「TTFT 근삿값」·「total」·「first_event」는 그 정의와 따로 놉니다 → Ch 15 05 말을 이어 쓰고, 03이 새로 보일 것은 **그래프 사건 수준의 「첫 사건」**(모드마다 첫 사건이 가리키는 일이 다름)으로 좁히는 쪽을 권합니다.
- **Ch 6 06과 이어짐**: Ch 6 06 b7 「첫 청크까지의 시간은 이 절에서도 재지 않았습니다」·칸 「걸린 초」·「예상 비용」(요금표·`estimate_cost`) — 03의 「추정 비용」(금지어)·식 안 요금 숫자는 Ch 6 06 `estimate_cost`(Ch 21 `runner_tools.py`에 옮겨 둔 판 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`)로 바꿀 수 있음.
- 구조로 정해지는 관찰(결정적 후보): `updates`만 구독하면 첫 사건이 노드가 끝난 뒤(노드 하나면 첫 사건 ≈ 끝, 사건 1개) · `custom` 시작 사건은 모델 요청 전에 씀(노드 코드 차례) · 한 실행 목록 구독에서 차례 `custom(시작) → messages … → custom(끝) → updates`(e3·e4) · 글자가 든 첫 스트림 청크 시각 < 끝 시각(Ch 15 05와 같은 성질, 정의상 참).
- 흔들리는 값: 초 전부·출력 토큰·답 글자 수·비용·messages 사건 수 → 규격 §2-7 9번 끝(둘째 단락·표·「확인할 점」에만, 「교재 출력에서는」) — §6.
- `measure()` 본문 16줄·힌트 `-> dict`·노드가 노트북 전역 `call_records`에 붙임·노드 안 `assert` → 셀·함수 나누기.
- b2 「Ch30의 FastAPI 서버 전송 이벤트(SSE) 응답 설계에 그대로 이어집니다」·b8 「Ch30에서는 messages와 custom 사건을 FastAPI SSE로 … 연결 종료와 재접속을 처리합니다」 → Ch 30 `agent_service/app.py`가 `astream(…, stream_mode="custom")`·`astream(…, stream_mode="messages")`를 씀 · Ch 30 06이 재연결 → **참**(실습 절을 붙이면 03 b8은 04로 고칠 자리).
- 제목 「TTFT」·「total」(영문) — 슬러그 `03-TTFT와-total-비교`는 Part 6 목차만 링크(다시 만들어짐) → 바꿀 수 있음.

## 3. 실습 폴더 구조와 읽는 곳

```
labs/part6/ch25-streaming/
  README.md (한 단락 — 「01은 API 키 불필요 · 02·03은 .env 키 · 03은 세 번의 별도 호출 비용 합산 · 추정 비용」, uv sync 안내 없음)
  pyproject.toml   uv.lock (87항목)
  notebooks/01~03-*.ipynb
  .venv/ (macOS 판 173MB — home = /Users/…/cpython-3.12-macos-aarch64-none, uv 0.11.6)
  (없음: data/ · runs/ · tests/ · 도구 파일 · worker · 노트북 생성기)
```

- **노트북이 쓰는 파일: 0**(세 절 모두 `open`·쓰기 없음, 01만 `InMemorySaver`). 연결 폴더 SQLite 멈춤(Ch 23 발견)은 지금 판에는 해당 없음.
- **Ch 25 파일을 코드로 읽는 곳**(`grep`, `textbook`·`labs`, `.venv`·`before`·zip 제외):

| 자리 | 무엇을 | 성격 |
|---|---|---|
| `textbook/part6/public-files.json` 47~50행 | README·노트북 셋(**`pyproject.toml`·`uv.lock` 줄 없음** — Ch 24는 여섯 줄) | 묶음 허용 목록. 그래도 zip에는 잠금 둘이 들어감(`build_bundle.py`가 실습 폴더 잠금을 함께 넣음) |
| 챕터 `qa/public-files.json` | HTML 4 + 실습 파일 4 = 8(옛 SVG 줄 없음) | `collect_public_files.py`가 Part 목록으로 모음 |
| `textbook/downloads/part6-practice.zip`(`edd8c3be…`)·`llm-practice.zip`(`f2d2008a…`) | Ch 25 여섯 파일(노트북 셋·README·`pyproject.toml`·`uv.lock`)이 **디스크와 같음** | 묶음 |
| `textbook/part6/_build_index.py` 23행 · `textbook/_notebook/build_index.py` 54행 · `build_bundle.py` 25행 | (3, 5, 「토큰과 진행 이벤트를 구분하고 첫 응답과 전체 처리 시간을 측정합니다.」) · (절 수 3, 「… 측정합니다」) · 공개 챕터 목록 | 실습 절을 붙이면 3 ≠ 4(`_notebook/build_index.py`는 선례대로 전체 마감 몫) |
| Part 6·7 선행 목록(`prerequisite-files.json`) · `existing-artifact-hashes.json` · 챕터 `qa/prerequisite-files.json`(`[]`) | **Ch 25 줄 0** | 뒤 챕터가 Ch 25 파일을 읽지 않음 |
| Part 6 `check_bundle_execution.py` | Ch 24 01·Ch 28 01만(**Ch 25 안 봄**) | 묶음 실행 계약 없음 — 01에 모델·키를 넣어도 이 검사는 안 멈춤 |
| Part 7 `check_bundle_execution.py` | Part 7 챕터만 | — |
| 옛 검사(고치지 않음, 기록만) | `check_scope.py` `EXPECTED` (3,5)·`SECTION_COUNTS` 3(실습 절을 붙이면 멈춤, 이미 Ch 21에서 멈춤) · `check_notebook_readiness.py` 43행 `assert len(reports) == 47`(Part 6 노트북 이미 51 — 결과 파일을 먼저 씀 → 되돌림 선례) · `check_figures.py`(SVG마다 `.excalidraw` 짝 — 새 Mermaid SVG는 짝 없음) · `check_visual_reports.py` · `check_delivery.py`(`llm-practice.zip` 신선도) | Ch 21~24 선례대로 이미 어긋난 상태 |
| 기록만 | `final-artifact-hashes.json`(Ch 25 줄 24 — **노트북 셋·`_src` 셋·HTML 셋 = 9줄은 이미 옛 해시**, 그림·잠금·README 15줄은 같음) · `notebook-executions.json`·`notebook-readiness.json`·`figure-consistency.json`(각 3) · `visual-results.json`(8) · `lesson-scope.json`·`prose-repetition-initial.json`(1) · `ch25-second-technical-review.md`·`ch25-before-technical-repair/`(옛 노트북 셋) · `language/ch25-final.{json,md}`·`ch25-*.sha256` 셋·`ch25-original/`·`ch25-post-technical-before-language/`·`ch25-technical-corrected-before-language/` · Part 7 `existing-artifacts-before.json`(6)·`before-integration/build_*.py` · `_notebook/checks/notebook-contracts-part6-ch25-streaming.json`(verify가 다시 씀)·`checks/ch25-streaming/`(옛 화면 검사) · 챕터 `qa/ch25-code-output-preservation.sha256`(10줄 — 노트북 셋은 이미 옛 해시) | — |

- **옛 생성기**:

| 파일 | 무엇을 씀 | 비고 |
|---|---|---|
| **`textbook/part6/_generate_ch25_ch26.py`**(554줄, `545db83c…`, **Ch 25·26 공용**) | `write()` — **Ch 25·26 노트북**(출력 없이) · `chapter.json` · 실습 폴더 `pyproject.toml`·`README.md` · `_src`(`page()` 틀) · `research.md`·`qa/authoring-checklist.md`·`집필점검표.md`(옛 수치 「messages 73개」 등) · 챕터 `qa/public-files.json`. `--pages-only`는 `_src`만 | 지금 돌리면 Ch 25의 현재 노트북(출력 포함)·`_src`(09-14 `part6b_*`가 더한 단락 포함)·목록을 옛 판으로 덮어씀. **부르는 스크립트 0**(`grep` — 기록 문서만). 사본 `before/generators/_generate_ch25_ch26.py` |
| `figures/_gen_figures.py`(Ch 25, `45d88f5e…`) | `NN-흐름.{svg,excalidraw,caption.md}` 9개(`textbook/part5/_figure.py`) | 옛 그림 세 벌. 사본 `before/generators/`·`before/figures/` |
| (챕터 밖) `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6b_enrich.py`·`part6b_review_fixes.py` 35행 | Ch 25 세 노트북 설명 셀·`_src` 단락 덧붙임 | 기록만(Ch 21·23·24 선례) |
| `textbook/part6/_author_ch21_ch29.py` | **Ch 25 안 씀**(`grep` 0) | — |

→ 공용 생성기는 Ch 26 쪽도 씁니다. **Ch 23·24 선례**(공용 `author_ch23_ch24.py` — 앞 챕터 01절이 자기 쪽만 건너뛰는 줄을 넣고, 뒤 챕터 01절이 `raise SystemExit`, 뒤 챕터 마감에 `mv -n`)대로라면: Ch 25 01절 작업 때 `write()`·`write_pages_only()`의 `CHAPTERS`·`NOTEBOOKS` 반복에서 **`ch25-streaming`을 건너뛰는 줄**(설명 주석 + `if chapter == "ch25-streaming": continue`)을 넣고, Ch 26 01절이 `raise SystemExit`, Ch 26 마감에 `before/generators/blocked/`로 옮깁니다. 파일 자리가 Part 6 맨 위라 챕터 밖 수정 — 진단·요약에 한 줄. Ch 25 `figures/_gen_figures.py`는 Ch 25 마감 때 `mv -n` → `qa/upgrade/before/generators/blocked/`(Ch 23·24 선례).

- **판**: `requires-python = ">=3.12,<3.13"`, `dependencies = ["langchain==1.4.0", "langchain-openai==1.6.0", "langgraph==1.2.11", "python-dotenv==1.2.3"]`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`, `[tool.uv] package = false`. 잠금 주요 판: `langchain-core 1.6.2`·`openai 3.11.0`·`langgraph-checkpoint 4.2.0`·`langgraph-prebuilt 1.1.0`·`langgraph-sdk 0.4.4`·`langsmith 0.12.4`·`pydantic 2.13.5`·`tiktoken 0.14.0`·`httpx 0.28.1`. **`numpy`·`pillow`·`langgraph-checkpoint-sqlite` 없음.**
- **Ch 21 잠금과 견줌**: `uv export` 목록이 **Ch 21에서 `numpy 2.5.3`·`pillow 12.3.0` 둘만 뺀 것과 같음**(87 ↔ 89, 겹치는 판 모두 같음). Ch 24 잠금(`langgraph` 하나)과 겹치는 판(`langgraph 1.2.11`·`langgraph-checkpoint 4.2.0`·`langgraph-prebuilt 1.1.0`·`langchain-core 1.6.2`·`pydantic 2.13.5`·dev 넷)도 같음. **Ch 21 `runner_tools.py`는 맨 위에서 `numpy`를 가져와 Ch 25 잠금에서는 import 자체가 멈춤**(파일째 가져오기 불가 — §7).
- `pytest`·`tests/` 없음. 실습 폴더 `.venv`는 macOS 판(삭제 승인 대상).

## 4. 앞뒤 챕터 이음새

### 4-1. Ch 24 인계(요약 §13·§14·§15, 계약 §3 Ch24 줄) 항목별 지금 상태

| 인계 항목 | 지금 Ch 25 원고 | 상태 |
|---|---|---|
| 01~03 b3 「Ch24에서 interrupt와 **재개 사건**을 확인했습니다」 | 세 절 글자까지 같음(+ 옛 생성기 `prior`) | **부분 참** — `interrupt`·`Command(resume=…)`로 이어 가기는 Ch 24 01·02로 참, **스트림 사건은 Ch 24에 0건**. 본문 말 「재개」도 Ch 24는 「사람의 답으로 이어 가기」 |
| `resume` 세 장면(Ch 23 03 스레드 재개 · Ch 23 04·06 worker `resume` 단계 · Ch 24 `Command(resume=…)`)을 스트림 쪽과 한 문장으로 가를 것 | 구분 문장 0 | **미해결**. 설치판에는 「resume 사건」이라는 모드가 **없음** — `stream(Command(resume="approve"), config, stream_mode="updates")`는 보통 갱신 `{'ask': {'answer': 'approve'}}` 한 줄을 냄(e2). 멈춤은 `updates`에 `{'__interrupt__': (Interrupt(...),)}` · v1 `values` 마지막 딕셔너리에 키 `__interrupt__` · v2 `values`는 칸 `interrupts` · `tasks` 끝 사건 `interrupts` 칸에 `{'value': …, 'id': …}`(e2). → 「멈춤 표시도 사건으로 흘러나온다」를 보일지는 선택(§9) |
| Ch 24 04 b8 → Ch 25 01 슬러그·「한 실행에서 생긴 사건을 일곱 방식으로 받아 보는 방법」 | 01은 일곱 번 따로 실행 | **부분 참** — §2 01 첫 항목(한 실행 목록 모양이면 참) |
| 모델 0 — 도구 호출 승인·`HumanInTheLoopMiddleware`·에이전트 그래프 멈춤 0건 | Ch 25도 도구·미들웨어 없음 | 어긋남 없음(에이전트 그래프를 스트리밍하면 Ch 25가 처음) |
| 정적 중단점 `interrupt_before/after`·`as_node`·`Command(goto=)` 안 가르침 | 안 씀(설치판 `stream()` 인자에 `interrupt_before`·`interrupt_after` 있음) | 어긋남 없음 |
| 체크포인터는 `InMemorySaver`뿐 · 체크포인트 수는 그 그래프 값 | 01 `InMemorySaver`, checkpoints 4 | 참 — 노드 둘 그래프의 값(Ch 23 01 「노드 둘 4」와 같음)으로만 |
| 걸린 시간 안 잼(Ch 24 준비물 「걸린 시간은 재지 않았습니다」) | 03이 잼 | Ch 24 값을 쓸 것 없음 — 03 걸린 시간은 Ch 15 05·Ch 6 06에 이음 |
| Ch 25 쪽 옛 생성기 `_generate_ch25_ch26.py`는 Ch 24가 건드리지 않음 | — | Ch 25 몫(§3) |

- **Ch 23 이음**: b3 「Ch23에서 체크포인터와 thread_id가 상태를 저장하는 방법을 배웠고」 → 참(Ch 23 01). `checkpoints` 모드 사건 = `get_state()`와 같은 모양(설치판 독스트링) → Ch 23 01 `get_state_history` 목록(단계 번호·만든 자리 `input`·`loop`)과 같은 넷이 흘러나옴(e1) — 이어 쓰기 좋은 자리. `tasks`는 Ch 23 05 `.tasks` 말과 이어짐.
- **다시 쓸 앞 챕터 함수**:
  - Ch 6 06 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` — Ch 21 `runner_tools.py` 판(`f4113158…`)·Ch 20 `graph_tools.py` 판·Ch 17 `agent_tools.py` 판·Ch 15 `rag_tools.py` 판. 03이 비용을 보이면 손 요금 식 대신.
  - Ch 19·20·21 `sum_usage(messages)`(에이전트 메시지 목록의 AI 메시지 수·토큰 합) · `show_messages` · `tool_call_names` — 에이전트 그래프(`create_agent`)를 스트리밍하는 장면을 넣을 때만 후보.
  - Ch 17 04 `send_and_measure(chat_model, request_text)`(걸린 초·토큰) — `invoke` 한 번 재기. 03에서 `invoke`와 견주면 후보.
  - Ch 23·24 도구 파일(`checkpoint_tools.py`는 SQLite import라 이 잠금에서 import 멈춤 · `approval_tools.py` `print_history(history)`는 `StateSnapshot` **속성**(`snapshot.metadata[…]`)을 읽어 `checkpoints` 사건(**딕셔너리**)에 그대로 못 씀).
  - Ch 15 05 첫 토큰 도착 시간 셀(함수 아님 — 셀 모양 `stream_start`·`first_text_time`·`chunk.text != ""`) · Ch 6 04 스트림 청크 합치기 셀(`combined = combined + chunk`, `joined_text`).

### 4-2. 앞 챕터에서 가르친 것 (Ch 25가 전제할 수 있는 것)

| 챕터·절 | 가르친 것 | Ch 25와의 관계 |
|---|---|---|
| Ch 2 12 | `async def`·`await`(셀 맨 위 `await` 포함)·`asyncio.run`·`gather`·`to_thread`·`perf_counter` | **`async for` 0건** → `astream`을 쓰면 `async for`를 처음 푸는 자리(규격 L7 — 비동기가 학습 목표일 때만). Ch 30 04가 「`astream`은 비동기 스트림 실행 메서드입니다」로 스스로 가르침 |
| Ch 6 01·04·06 | `init_chat_model(… temperature=0, reasoning_effort="none")` · **`model.stream()`·제너레이터·스트림 청크·`chunk.text`·빈 청크·`+`로 합치기·`stream_usage`·사용량 청크** · 「걸린 초」·요금표·`estimate_cost`·**「첫 청크까지의 시간은 재지 않았습니다」** | 02의 「메시지 조각」은 Ch 6 04 스트림 청크 그대로 이어 쓸 말. `enumerate`·튜플 풀기 `for role, content in …`도 Ch 6 04 |
| Ch 13 | `StateGraph`·`TypedDict` 상태 형식·`compile`·`invoke` | `stream` 0건 |
| Ch 15 05 | **「첫 토큰 도착 시간(TTFT)」·「전체 지연」·「실행 추적」·「단계 기록」**, `model.stream`+`perf_counter`, 결론은 두 실행에서 같은 관찰만(「교재 출력에서」) | 03 용어·측정 방법·흔들림 처리의 직접 선례 |
| Ch 15 06 | 백분위수(가장 가까운 자리 방식) | 03 b7 「백분위수」를 말하면 이 절 뜻 |
| Ch 17 04 · Ch 18 03 | 걸린 시간을 잰 주제 절 예외 · 걸린 초·도착 차례 비교는 결론·그림·정리에서 뺌(Ch 18 03) | 03 처리 선례 |
| Ch 20·21 | 모델 노드 그래프·`create_agent` 에이전트 그래프(`invoke`만) | 에이전트를 스트리밍하면 Ch 25가 처음. Ch 30 09 「Ch21에서 만든 Agent와 Ch25의 모델 스트림」 |
| Ch 23 01·05 | `InMemorySaver`·`get_state`·`get_state_history`(최신 것부터, 단계 번호·만든 자리)·`.tasks` | 01 `checkpoints`·`tasks` 사건과 이음 |
| Ch 24 01~03 | `interrupt`·`__interrupt__`·`Command(resume=…)` | §4-1 |

### 4-3. 완료 챕터가 Ch 25에 기대는 문장 — 개선 뒤에도 참이어야 함

| 자리 | 문장 | 조건 |
|---|---|---|
| Ch 24 04 `_src` b8(+ HTML·`author_04.py` 697행) | 「이 절로 Ch 24가 끝납니다. Ch 25 01절에서는 한 실행에서 생긴 사건을 일곱 방식으로 받아 보는 방법을 다룹니다」 + 01 슬러그 링크 | **01 슬러그 유지** · 한 실행에서 일곱 모드(§2 01) |
| Ch 23 `chapter-summary.md` §15 · Ch 23 02·03 진단 | 「Ch 25 01~03 b3 「Ch23에서 체크포인터와 thread_id」 참」 | b3를 고쳐도 Ch 23 01 이음이 남으면 참 |
| Ch 6 04·06 · Ch 15 05 `_src` | Ch 25 언급 0 | — |
| Part 1·2·5 `_src` | Ch 25 언급 0(`grep`) | — |

### 4-4. 뒤 챕터(대기)가 Ch 25에 기대는 문장 — 고치지 않음

| 자리 | 문장 | Ch 25 쪽 사실(지금 판) |
|---|---|---|
| Ch 26 01~04 `_src` b3(+ `_generate_ch25_ch26.py`) | 「Ch25에서는 실행 사건을 스트리밍했습니다」 | 참 |
| Ch 30 01 `_src` b3 | 「Ch25에서는 결과가 **조각**으로 이어질 수 있음을 확인했습니다」 | 뜻은 참 · 「조각」은 Ch 5 토큰 전용(Ch 30 몫) |
| Ch 30 03 `_src` b3 | 「Ch25에서는 **단일 실행과 스트리밍이 같은 실행 객체의 다른 소비 방법**임을 배웠습니다」 | **부분 참** — 지금 Ch 25는 `invoke`와 `stream`을 견주지 않음(Ch 6 04는 모델에서 견줌). 01에서 `graph.invoke(...)` 결과 = 마지막 `values` 사건을 보이면 참(모델 없이 결정적) |
| Ch 30 04 `_src` b3 | 「Ch25에서 스트림 모드와 진행 이벤트를 비교했고」 | 참 |
| Ch 30 05 `_src` b3 | 「Ch25에서 진행 이벤트와 토큰 이벤트를 분리했습니다」 | 참(02) |
| Ch 30 09 `_src` b3·b4 | 「Ch25에서는 `stream_mode="messages"`에서 모델 메시지 청크와 **실행 메타데이터를 읽었습니다**」 · 「Ch21에서 만든 Agent와 Ch25의 모델 스트림」 | **부분 참** — 02가 `metadata`를 풀기만 하고 읽지 않음. `metadata["langgraph_node"]`를 출력하면 참 |
| Ch 30 코드 `labs/part7/ch30-fastapi-serving/agent_service/app.py` 110~111·134~136행 · `agent.py` 6·27행 | `astream(…, stream_mode="custom")` · `async for message, metadata in runtime.astream(…, stream_mode="messages")` · `get_stream_writer()` | Ch 25 파일을 읽지 않음(계약 아님). 이름·모양(`custom`·`messages` 튜플·`get_stream_writer`)을 Ch 25가 가르치면 이어짐 |
| `labs/part6/continuity-guide.md` 11행 | 「Ch6의 토큰 스트리밍, Ch2의 비동기 실행 \| Ch25 토큰·중간 단계·진행 이벤트와 지연 시간 \| Ch30 FastAPI의 응답 스트림」 | 「Ch2의 비동기 실행」 — 지금 Ch 25는 비동기 0건(부분 참), 「지연」 말 |
| `labs/part7/continuity-guide.md` 7행 | 「Ch2의 비동기 함수와 Ch25의 스트리밍」 | 참 |
| Part 6 `_src/index.html` 8행 · `practice-start.md` 15행 | 「Ch 25는 처리 중인 내용을 사용자에게 보여 주고 시간을 측정합니다」·「Ch 25에서 스트리밍을 관찰한 뒤」 | 참(「측정」 말) |
| Ch 27~29 `_src`·노트북 | Ch 25 언급 0 · Ch 25 파일을 읽는 코드 0 | 산출 파일 계약 없음 |

### 4-5. Part 6 묶음·목록·기록

- Part 6 선행 목록·`existing-artifact-hashes.json`에 Ch 25 줄 **0**. `final-artifact-hashes.json` Ch 25 줄 24개는 옛 판(9줄 이미 다름 — 만드는 스크립트 없음, Ch 21·23·24 선례대로 기록만).
- 공개 목록 두 곳 + zip 두 개(§3). **묶음 실행 검사 계약 없음**(`check_bundle_execution.py`가 Ch 25를 안 돌림). Part 6 공개 목록에 Ch 25 `pyproject.toml`·`uv.lock` 줄이 없으나 zip에는 들어감 — 도구 파일을 만들면 `notebooks/…_tools.py` 줄을 두 목록에 더하고 zip 다시 만들기.
- 뒤 챕터가 Ch 25 노트북·출력·파일을 읽는 코드: **0**(Ch 29·30 모두 — Ch 29 04는 Ch 18 06·Ch 21 06만 읽음). Ch 25는 산출 파일을 쓰지 않음 → **파일 계약 없음**.

## 5. 라이브러리 동작 — 설치판 소스와 모델 없는 확인 (2026-09-25, `langgraph 1.2.11`·`langchain-core 1.6.2`)

### 5-1. 설치판 `stream_mode` 목록
- `langgraph/types.py` 122~124행 `StreamMode = Literal["values", "updates", "checkpoints", "tasks", "debug", "messages", "custom"]` — **일곱**(공식 문서 표와 이름 같음). 독스트링 127~135행.
- `Pregel.stream()`(`pregel/main.py` 2655행~) 인자: `input`·`config`·`context`·**`stream_mode`(하나 또는 목록)**·`print_mode`·`output_keys`·`interrupt_before`·`interrupt_after`·`durability`·`control`·**`subgraphs=False`**·`debug`·**`version: Literal["v1", "v2"] = "v1"`**. `astream()` 3063행(같은 인자). `stream_events()` 3638행은 `version: Literal["v1","v2","v3"] = "v2"`(v3는 「experimental」 경고). `invoke()`에도 `version`.
- 컴파일한 `StateGraph`의 기본 `stream_mode`는 **`"updates"`**(`graph/state.py` 1357행 — `graph.stream(입력)`만 쓰면 updates). Pregel 기본값 `"values"`(main.py 709행)는 하위 그래프로 불릴 때 등.
- `get_stream_writer()`(`langgraph/config.py` 126행~): 노드 안에서 부르면 이 실행의 쓰기 함수. 독스트링 경고 「Python < 3.11 async에서는 안 됨」(교재 3.12 — 해당 없음). 노드 매개변수 `writer: StreamWriter`로 받아도 됨(e2 `write-injected`). **`custom`을 구독하지 않으면 쓴 값은 어디에도 안 나옴**(e2 — updates만 구독한 실행에 custom 흔적 0, `types.py` 138~141행 「no-op when not using stream_mode="custom"」).
- `graph.stream(...)`은 제너레이터를 만들 뿐 실행을 시작하지 않음 — 첫 `next`에서 시작(e4, 0.3초 노드: 만든 뒤 0.0초 · 첫 사건 0.31초).

### 5-2. 모드별 사건 모양 (노드 둘 + `InMemorySaver`, e1 — 두 번 같음)

| 모드 | 사건 수(체크포인터 있음 / 없음) | 한 사건의 모양 |
|---|---|---|
| `values` | 3 / 3 | 칸 전체 딕셔너리 — 시작 입력 `{'topic': ' 배송 ', 'draft': ''}` → 노드마다 한 번 |
| `updates` | 2 / 2 | `{'prepare': {'topic': '배송'}}` — 노드 이름 → 그 노드가 바꾼 칸 |
| `messages` | 0 / 0 | 모델 요청이 없으면 0. 있으면 `(AIMessageChunk, metadata)` 튜플(§5-4) |
| `custom` | 2 / 2 | 노드가 쓴 값 그대로 `{'stage': 'prepare', 'progress': 50}` |
| `checkpoints` | 4 / **0** | 키 여섯 `config`·`metadata`·`next`·`parent_config`·`tasks`·`values` — 단계 -1(`input`, `next ['__start__']`)·0·1·2(`loop`) = Ch 23 01 체크포인트 넷 |
| `tasks` | 4 / **4** | 시작 `id`·`input`·`name`·`triggers`(`('branch:to:prepare',)`) · 끝 `error`·`id`·`interrupts`·`name`·`result` |
| `debug` | 8 / **4** | `type`(`checkpoint`·`task`·`task_result`)·`step`·`timestamp`·`payload` — 체크포인터가 있으면 checkpoints 4 + tasks 4 |

- **공식 문서 표는 `tasks`에도 「Requires a checkpointer」** — 설치판 출력은 체크포인터 없이 tasks 4. 문서와 설치판이 다름 → 설치판 출력으로 쓰고 문서 표기를 한 줄 밝힘.
- **일곱 모드를 목록 하나로 한 실행**: `(mode, data)` 튜플 **23개**, 모드별 수가 따로 실행한 값과 같음, 차례 `checkpoints > debug > values > checkpoints > debug > tasks > debug > custom > updates > tasks > …`가 두 번 같음(e5). 스레드 체크포인트 4(한 실행이라 늘지 않음).

### 5-3. 여러 모드·`version="v2"`·`subgraphs=True`·멈춤 (e2)
- 목록 v1: `('custom', {...})`·`('updates', {...})` 튜플(길이 2). **목록 v2**: 딕셔너리 `{'type': 'custom', 'ns': (), 'data': {...}}`. **단일 모드 v2**도 딕셔너리(values는 `interrupts` 칸 추가, 멈춤 없으면 `()`).
- `subgraphs=True`: 단일 모드면 `(ns, data)`, 목록이면 **`(ns, mode, data)`**(길이 3). 바깥 노드 `ns = ()`, 하위 그래프 안 `ns = ('child:<작업 아이디>',)` — 아이디는 실행마다 다름(출력 금지). `subgraphs=False`면 하위 그래프 안 갱신은 바깥 노드 갱신 하나로 합쳐 보임.
- 멈춤(`interrupt`): v1 `values` 마지막 딕셔너리에 키 `__interrupt__`(값 `(Interrupt(value=…, id=…),)`) · `updates`는 `{'__interrupt__': (...)}` 한 사건 · `tasks` 끝 사건 `interrupts` 칸 `[{'value': …, 'id': …}]` · v2 `values`는 칸 `interrupts`. **이어 가기** `stream(Command(resume="approve"), config, stream_mode="updates")` → `{'ask': {'answer': 'approve'}}` 한 줄(따로 「resume 사건」 없음).

### 5-4. `messages` 모드와 모델 요청 (e3는 조사 전용 가짜 모델 — 서비스 요청 0)
- 노드 안 `model.invoke(...)`로도 스트림 청크가 흘러나옴(문서 「message events are emitted even when the LLM is run using .invoke」). 사건 = `(AIMessageChunk, metadata)`, 마지막 청크 `chunk_position == 'last'`. 메타데이터 키 `langgraph_node`·`langgraph_step`·`langgraph_triggers`·`langgraph_path`·`langgraph_checkpoint_ns`·`checkpoint_ns`·`ls_provider`·`ls_model_type`·`ls_integration`·`lc_versions`(실제 모델이면 `ls_model_name` 등 더 있음 — 실행 안 함).
- 한 실행 세 모드 차례(e3): `custom 시작 → messages 청크들 → custom 끝 → updates` — 노드 코드 차례로 정해짐.
- **스트리밍 요청이 나가는 조건**: `langchain_core` `BaseChatModel._should_stream`(549~585행)이 `stream=True`·`streaming=True`·**스트리밍 콜백(`_StreamingCallbackHandler`)이 붙었을 때만** 참. langgraph `StreamMessagesHandler`(`pregel/_messages.py` 49행)가 그 콜백 → **`messages`를 구독한 실행에서만 노드 안 `invoke`가 스트리밍 요청**, `updates`·`custom`만 구독하면 일반 요청(옛 03의 세 줄은 요청 종류부터 다름).
- 모델 객체(가짜 키로 만들기만, 요청 0): `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` → `ChatOpenAI`, `temperature 0.0`·`reasoning_effort 'none'`·**`stream_usage True`**(기본 주소 — Ch 6 04와 같음, 마지막 사용량 청크)·`streaming False`·`disable_streaming False`.
- `version="v2"` + messages는 `StreamMessagesHandlerV2`(content-block 프로토콜) — 가짜 모델에서는 데이터가 여전히 튜플이었음. 실제 모델에서 v2 모양은 확인 안 함.

## 6. 모델을 부를지와 03 걸린 시간 처리 (결정하지 않음 — 장단점만)

### 6-1. 모델
- **토큰 스트리밍(`messages`)은 모델이 있어야 보입니다.** 규격 §3은 기본 경로에서 가짜 모델(`GenericFakeChatModel` 포함)을 금지 → 02·03의 핵심 관찰은 실제 모델 없이는 못 보임. 모델 없이 결정적으로 보일 수 있는 것은 01 전부(일곱 모드·목록·v2·`invoke` 결과 = 마지막 values)와 `custom`·`updates`의 차례·걸린 시간 모양(`time.sleep` 노드 — 흉내라 TTFT가 아님)뿐.

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **M1 모델 없음** | 세 절 모두 노드가 만든 값, `messages` 0 | 결정적 · 키 셀·비용 0 · 흔들림 0 | 챕터 목표(토큰·첫 토큰 도착 시간)를 가르칠 수 없음 · 가짜 모델은 §3 금지 · Ch 30 09 「모델 메시지 청크와 실행 메타데이터를 읽었습니다」 거짓 · 실용성 없음 |
| **M2 절마다 다르게(권장 후보)** | **01 모델 없음**(노드 둘 + 체크포인터, 일곱 모드 한 실행 — 결정적) · 02·03·04 실제 모델 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` | 01은 흔들림 0·키 셀 없음(Ch 20 03·Ch 24 01 선례 모양) · 02·03은 진짜 스트림 청크·메타데이터 · Ch 30 인계가 참이 됨 | 01에서 `messages` 0을 「모델이 없어서」로만 설명(02에서 채움) · 02·03 흔들림 처리(§2-7 9·10번) · 서비스 요청 |
| **M3 모든 절 실제 모델** | 01도 모델 노드 하나를 넣어 일곱 모드 한 실행에 `messages` > 0 | 한 실행에서 일곱 모드가 모두 0이 아님 | 01 사건 수 가운데 `messages`가 흔들림(71·73·88 선례) → 01 결론에 쓸 수 없는 값이 섞임 · 01 키 셀 |

- 모델 설정은 과정 표준(`nbkit.key_and_model_cells()`) — 지금 02·03의 `temperature` 없음·f-string 모델 이름·`[Path.cwd(), *…parents]` 키 찾기는 모두 표준 셀로 바꿀 자리.
- 에이전트 그래프(`create_agent` — Ch 21)를 스트리밍할지: Ch 30 09 「Ch21에서 만든 Agent와 Ch25의 모델 스트림」과 가까워지지만 도구 호출이 끼면 `messages`에 도구 호출 청크·`ToolMessage`가 섞이고 요청 수가 모델 선택에 따라 흔들림(Ch 21 요약 흔들림 기록). 모델 노드 하나짜리 `StateGraph`(Ch 20 모양)가 가장 단순.

### 6-2. 03 걸린 시간
- **규격상 자리**: 규격 §3 「재지 않은 시간·속도를 단정하지 않습니다」 + 과정 요약 2-7·2-9·2-10의 **「시간이 주제인 절은 재는 예외」**(Ch 15 05·06 · Ch 17 04 · Ch 18 03). 03은 제목부터 걸린 시간이 주제 → **예외에 해당**. 단 규격 §2-7 9번 끝: 새 커널 두 번에서 같았던 값만 본문·그림·정리, 달랐던 값(초 전부·출력 토큰·청크 수·비용)은 결과 읽기 둘째 단락·본문 표·「확인할 점」에만 「교재 출력에서는」·「이번 실행에서는」, **결론·그림·정리·복습에 초 비교 금지**(Ch 18 03 선례 — 도착 차례 비교도 뺌).
- **결론에 쓸 수 있는 결정적 관찰 후보**(구조로 정해짐): ① 한 실행에서 차례 `custom 시작 → 첫 스트림 청크 → … → custom 끝 → updates`(노드 코드 차례) ② `updates`만 받으면 첫 사건이 노드가 끝난 뒤(노드 하나면 사건 1개 — 첫 사건 = 끝) ③ 글자가 든 첫 스트림 청크 시각 < 마지막 사건 시각(정의상 참 — Ch 15 05 「첫 토큰이 끝보다 먼저 왔는가: True」와 같은 모양) ④ 이어 붙인 청크 글 == 최종 답 ⑤ 요청 수(한 실행 = 요청 1).

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **T1 한 실행·여러 모드 동시 구독** | `stream_mode=["custom", "messages", "updates"]` 한 실행에서 모드마다 **처음 받은 시각**과 끝을 적음(요청 1) | 같은 요청·같은 답에서 「첫 사건이 무엇이냐에 따라 사용자가 먼저 보는 것이 다르다」를 공정하게 보임 · 옛 본문 b4가 권한 설계 · 결론 ①~⑤가 모두 결정적 · 요청 최소 | 모드별 「따로 받을 때」의 모습(updates만 받는 화면)은 이 실행 안의 updates 시각으로 대신 설명해야 함 |
| **T2 모드별 따로 실행(지금 모양)** | 세 모드를 따로 세 요청 | 코드가 단순 | 요청 종류(스트리밍/일반)·답 길이·서버 상태가 다 달라 비교 불가(§2 03) — 본문이 스스로 「우열을 판정하지 않습니다」로 끝나는 절이 됨 |
| **T3 T1 + 같은 실행을 N번(예 5) 되풀이해 범위** | T1을 셀 안 `for`로 5번, 초의 최솟값·최댓값 또는 Ch 15 06 백분위수 | 흔들림 자체를 보여 줌 · 「한 번 잰 값으로 가르지 않는다」를 실행으로 | 요청 ×5 · 범위 값도 두 커널에서 흔들림(그림·결론 불가) · 셀·함수가 늘어남(§2-7 「코드를 늘려 가면서 개선할 필요는 없다」) |
| **T4 `invoke` ↔ 그래프 `stream`(messages) 견주기** | Ch 15 05처럼 받는 방법 둘 | Ch 30 03 「단일 실행과 스트리밍」 인계가 참 | Ch 15 05와 거의 같은 실험(되풀이) · 어느 쪽이 먼저 끝났는지는 Ch 15 05에서도 두 실행이 달랐음 |

- **입력을 고르기 전 흔들림 확인**(규격 §2-7 10번 끝): 결론으로 쓸 관찰(예 「첫 토큰 도착 시간이 전체의 절반보다 작다」 같은 비율)을 넣으려면 노트북 밖에서 같은 요청 5번으로 먼저 확인(요청 5). 비율 관찰은 답 길이에 기대므로(Ch 15 05는 짧은 JSON에서 「절반을 넘음」) 결정적 후보가 아님 — 쓰려면 5번 확인 뒤 b7 한정.
- **용어**: Ch 15 05 정의 **「첫 토큰 도착 시간(TTFT)」**(글자가 든 첫 스트림 청크) · **「전체 지연」**을 이어 쓸지, Ch 6 06 칸 **「걸린 초」**로 쓸지(§8-3). 「first_event」는 새 말 「첫 사건 시간」 후보.

## 7. §2-7 판단 근거 — 도구 파일

### 사실
- 지금 세 노트북은 함수를 서로 다시 쓰지 않음(01 노드 둘 · 02 노드 하나 · 03 노드 하나 + `measure`). 02·03 노드 `answer`는 거의 같음(진행 값·글만 다름 — 절마다 한 판).
- 개선하면 절 사이에 되풀이될 자리: 사건을 모드별로 세기(01 → 02·04) · 한 실행의 모드별 첫 사건 시각 적기(03 → 04) · 스트림 청크 글 이어 붙이기(02 → 03·04 — Ch 6 04가 셀로 가르침) · 예상 비용(Ch 6 06 `estimate_cost`, 03·04가 비용을 보이면).
- 앞 챕터 도구 파일은 **파일째 못 가져옴**: Ch 21 `runner_tools.py`(맨 위 `import numpy` — 이 잠금에 없음) · Ch 23 `checkpoint_tools.py`(SQLite) · Ch 24 `approval_tools.py`(`print_history`가 `StateSnapshot` 속성용). 규격 §2-7 3번대로 쓸 함수만 **같은 본문으로 옮기고 `# Ch N NN절에서 배웠습니다`**.
- 과정의 도구 파일 이름: `llm_tools`·`rag_tools`·`git_tools`·`data_tools`·`guardrails`·`agent_tools`·`workflow_tools`·`order_tools`·`graph_tools`·`runner_tools`·`checkpoint_tools`·`approval_tools`. **안 겹치는 후보**: **`stream_tools.py`**(가장 뜻이 드러남, `labs/` 전체에 같은 이름 0) · `event_tools.py` · `watch_tools.py`.

### 선택지 (결정하지 않음 — 장단점만)

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| A. 도구 파일 없음(Ch 2·4·6·22 선례) | 절마다 노트북에 | 목록·zip 변경 없음 | 03·04가 앞 절 셈 함수·Ch 6 06 `estimate_cost`를 다시 적으면 §2-7 3번과 충돌 |
| B. `stream_tools.py`에 앞 챕터 함수만 | Ch 6 06 `estimate_cost`(Ch 21 판 본문) 하나 | §2-7 3번을 지킴 · 작음 | 함수 하나짜리 파일 — 챕터 전체 코드가 줄지 않을 수 있음(`count_code.py`로 먼저 셀 것) · 비용을 안 보이면 필요 없음 |
| C. B + 이 챕터 도움 함수 | 01 모드별 세기 · 03 모드별 첫 사건 시각(인자로 그래프·입력·모드 목록) · 02 청크 글 잇기 | 04 실습 절 코드가 가장 짧음 | 처음 가르친 절은 노트북에 남겨 절 사이 판이 둘 · 함수 본문 10줄(L2) 넘기 쉬운 시각 기록 함수 |

## 8. 과정 규칙과 부딪히는 것 (선택지와 장단점만)

### 8-1. 모델과 규격 §3 — §6 표.

### 8-2. 「조각」·「사건」·모드 이름
- 「조각」(02 18·03 10번 + 출력 라벨) → Ch 5 토큰 전용 말. 선택: (가) **「스트림 청크」**(Ch 6 04 정의·Ch 15 05·규격 §4 청크 결정) — 과정 약속 그대로, 「청크와 토큰은 단위가 다름」을 Ch 6 04 링크로 / (나) 「메시지 청크」(`AIMessageChunk` 이름에 가까움) — 새 말 하나가 늘어남.
- 「사건」(event): 지금 세 절 본문·Ch 26 b3이 씀, Ch 30은 「이벤트」. 새 용어로 정할지(뜻 → 일상 예 → 코드 세 문장), 「이벤트」 금지어 처리 여부.
- 모드 이름 `values`·`updates` 등은 코드 이름이라 그대로 두되, 문장 첫머리 「values는 …」(G6 영문 시작 45건) → 「모드 `values`는」·「전체 상태를 보내는 모드(`values`)는」. 「stream mode」 → 「스트림 모드」 한 번 풀고 코드 이름 `stream_mode`.
- 「소비(자)」·「반환」·「옵션」·「필드」·「스냅숏」·「태스크」·「디버그」·「메타데이터」·「도메인」·「필터링」·「명시」·「워밍업」·「공정」·「단조 증가 시계」·「근삿값」·「추정」·「측정」·「지연」·「이벤트」 → Ch 13~24 금지어 계열(반환→내놓다, 추정 비용→예상 비용, 측정→재기, 필드→칸, 스냅숏→체크포인트 …). 「메타데이터」는 코드 `metadata`를 가리킬 때만.

### 8-3. 03 시간 말
- (가) Ch 15 05 말 그대로 **「첫 토큰 도착 시간(TTFT)」·「전체 지연」** — Ch 15에서 정의한 말이라 이어 씀(과정 요약 §5 Ch 15 용어). 단 Ch 18 금지어 「지연」(→걸린 초)과 겹쳐 보임 → 「전체 지연」은 Ch 15 05 말 인용으로만 / (나) 「첫 토큰 도착 시간」 + Ch 6 06 **「걸린 초」**(전체) — Ch 17~24 금지어와 맞음, Ch 15 05 「전체 지연」과는 다른 이름 / (다) 새 말 「첫 사건 시간」(모드와 관계없이 처음 받은 사건) — 03에 새로 필요한 말은 이것 하나.
- 제목 「TTFT와 total 비교」 → 영문 둘. 슬러그 `03-TTFT와-total-비교`는 Part 6 목차만 링크 → 바꿀 수 있음(`03-첫-토큰과-전체-시간-비교` 등, 강사 확인). 01 제목 「일곱 가지 stream mode」 → 슬러그는 Ch 24 04 링크로 **고정**, 제목 글만 「일곱 가지 스트림 모드」로 바꾸는 것은 가능(슬러그와 제목이 달라짐 — Ch 24 01 선례는 제목 말 강사 확인).

### 8-4. 비동기(`astream`·`async for`)
- Ch 2 12는 `async for`를 가르치지 않음(0건). Ch 30 04가 `astream`을 스스로 가르침. 선택: (가) Ch 25는 `stream`만(동기) — 사다리 L7 조건(비동기가 학습 목표일 때만)과 맞음, `continuity-guide.md` 11행 「Ch2의 비동기 실행」은 부분 참으로 인계 / (나) 03이나 「원리 더 알아보기」(`deep-dive`)에 `astream` + `async for` 한 셀 — Ch 30과 바로 이어지나 새 문법, 결과는 `stream`과 같은 모양(e4 `astream marks` = `stream marks`).

### 8-5. 힌트·클래스·셀 모양
- 노드 힌트 빼기(Ch 13·20·23·24) · 상태 형식 이름을 칸 구성마다(`DraftState`·`AnswerState` 등) · f-string·별표 풀기·`next`·`sum`·제너레이터·`.get` 사슬·`update`·`1_000_000`·식 안 요금 없이 · `get_stream_writer()({...})` → `writer = get_stream_writer()` 다음 줄 `writer({...})`(02가 이미 이 모양) · 15줄 넘는 셀 여섯 나누기 · `measure` 본문 16줄 나누기 · 노드 안 `assert`·노드가 노트북 전역 목록에 붙이기 빼기.
- 튜플 풀기 `for mode, data in …`는 Ch 6 04에서 씀 → 처음 쓰는 자리에 한 문장(목록 모드의 사건이 둘짜리 튜플이라는 뜻).

### 8-6. 참고 자료 b10
- 세 절이 같은 셋 → 절마다: 01 Streaming 문서의 모드 표·`StreamMode` 설치판 행 · 02 Streaming 문서 「LLM tokens」·「Custom data」 · 03 Ch 15 05·Ch 6 06 링크 + OpenAI latency 문서(「waiting ↔ watching progress」). 확인일 새로.

## 9. 삽화 비유 계열 후보

**이미 쓴 계열**(과정 요약·Ch 23·24 준비 조사·`figures/*.prompt.md` 185개 `grep`): **구슬 꿰기(Ch 6 04 — 스트리밍 청크)** · 모래시계 두 개(Ch 2 12)·구간마다 모래시계(Ch 15 05 — 걸린 시간)·소포 세 가지 재기·초시계(Ch 6 06) · 식당 주문 전표·내주는 창(Ch 19) · 자료실 승강 상자(Ch 20) · 세탁기(Ch 21) · 공항 검사(Ch 22) · 체스판·즉석사진(Ch 23) · 도미노 줄(Ch 24) · 레일·갈림길(Ch 13·18) · 분류대·검수대 컨베이어(Ch 2·3) · 도장(Ch 6 등). Ch 15 05 본문 비유 「첫 접시가 나올 때까지 기다린 시간」(말로만).

| 후보 | 그림 요소(절별) | 장점 | 겹침·위험 |
|---|---|---|---|
| **A. 회전초밥 레일과 색 접시** | 01 같은 레일을 여러 자리에서 봄(전체 접시 줄 · 한 칸씩 · 깃발 꽂은 접시) · 02 음식 접시(스트림 청크)와 작은 깃발 접시(custom)·빈 접시 쌓임(updates)이 한 레일에 섞여 옴 · 03 레일 앞쪽 첫 접시와 멀리 끝 접시, 깃발 접시가 맨 먼저 | 「먼저 온 한 접시 ↔ 마지막 접시가 지나가야 끝」이 사람 없이 읽힘 · Ch 15 05 「첫 접시」 말과 이어짐 · 0건 계열 | 식당 계열(Ch 19 전표)과 가까움 · 컨베이어(Ch 2·3 분류대) · 초밥 모양을 모델이 틀리기 쉬움 · 「접시 = 스트림 청크」를 한 문장으로 가를 것 |
| **B. 대나무 물받이와 떨어지는 물방울** | 02 홈통에서 물방울이 하나씩(청크) · 물이 차면 대나무가 한 번 기울어짐(노드 끝 = updates) · 옆 작은 풍경 방울(custom) · 03 첫 방울과 기울어지는 순간 | 「흘러나오는 것 · 먼저 나온 한 방울 · 다 찼을 때 한 번」이 선명 · 0건 계열 · 글자 없이 가능 | 01 일곱 모드 장면이 약함 · 물방울 개수·기울기 판독이 어려움 · 낯선 물건일 수 있음 |
| **C. 모형 기차와 칸** | 03 기관차(첫 칸)가 먼저 역에 닿고 마지막 칸이 지나야 끝 · 02 짐칸(청크)·깃발 칸(custom)·끝 칸 뒤 신호등(updates) · 01 같은 기차를 사진 한 장(values)·칸 하나씩(messages)·통과 기록(checkpoints)으로 보는 세 자리 | 「첫 칸 도착 ↔ 마지막 칸 통과」가 직관적 · 기차 0건 | 선로가 Ch 13·18 레일·갈림길 계열과 겹침 — **갈래 없는 곧은 선로**로 한정 · 신호등 색이 뜻을 얻을 위험 |
| **D. 솜사탕 기계** | 03 첫 실 가닥이 보이는 때와 다 감긴 솜사탕 · 02 막대에 감기는 실(청크)과 옆 작은 깃발(custom) | 0건 계열 · 밝고 단순 | 모드 구분(updates·values)을 그리기 어려움 · 솜 모양이 흐려 「그림만 보고 관계가 읽히는가」 검수에서 떨어지기 쉬움 |

- 사람·손·동물·화면·글자·숫자·시계 없음이 선례. 시계·모래시계는 Ch 2 12·Ch 15 05 계열이라 피함. 스타일 문구는 규격 §5-4 그대로. 「조각」은 말로 쓰지 않음(그림 읽기에서도 「청크」·「접시 하나」 등).

## 10. 위험과 깨진 것

1. **03 측정 설계** — 세 모드를 따로 요청, 스트리밍 요청은 `messages` 실행뿐(§5-4) → 지금 결과 표는 비교 근거가 없음. 한 실행 구독(T1)으로 바꾸면 출력·본문·복습 숫자가 모두 바뀜.
2. **틀린 사실** — 「tasks는 체크포인터가 있어야 사건이 생긴다」(01 b4·b7·복습 2) · 「Ch24에서 재개 사건」(세 절 b3) · Ch 24 04 b8 「한 실행」 ↔ 01 일곱 실행.
3. **흔들림** — messages 사건 수(71·73·88 기록)·초·출력 토큰·답 글자 수·비용. 01만 결정적(모델 없음). 02·03·04 결론은 구조 값(차례·updates 1·custom 2·이어 붙인 글 == 최종 답·요청 수)으로.
4. **용어** — 「조각」(Ch 5)·「TTFT 근삿값」·「total」·「first_event」 ↔ Ch 15 05 「첫 토큰 도착 시간」·「전체 지연」 · 금지어 다수(§1 표) · 제목 영문(「stream mode」·「TTFT」·「total」).
5. **공용 옛 생성기** — `_generate_ch25_ch26.py`를 돌리면 Ch 25(+ Ch 26) 노트북·`_src`·`chapter.json`·`pyproject.toml`·README·목록을 옛 판으로 덮어씀. 01절 작업 때 Ch 25 쪽을 건너뛰게(§3).
6. **뒤 챕터 인계** — Ch 30 03(단일 실행 ↔ 스트리밍)·09(메타데이터 읽기) 부분 참, Ch 30 01 「조각」 · `continuity-guide.md` 11행 「Ch2의 비동기 실행」·「지연 시간」. 파일 계약은 없음.
7. **모델 설정** — `temperature` 없음(G4 2), 키 찾기 별표 풀기, 01도 모델 패키지를 설치. 표준 모델 셀로 바꾸면 옛 출력과 다른 조건(어차피 다시 실행).
8. **파일 쓰기** — 지금 0. 04 실습 절이 기록을 쓰면 임시 폴더(`mkdtemp`) 모양(Ch 23·24 선례, 연결 폴더 SQLite 멈춤은 SQLite를 쓸 때만).
9. **옛 검사** — `check_scope.py`(실습 절 붙이면 멈춤)·`check_notebook_readiness.py`(결과 파일 먼저 씀 → 되돌림)·`check_figures.py`(`.excalidraw` 짝) — 기록만. 묶음 실행 검사는 Ch 25를 안 봄.
10. **기본 모드 오해** — 컴파일한 그래프 기본 `updates`(문서에 기본값 문장 없음). 「기본값」 문장은 출력으로 확인한 값만.
11. **서비스 요청 어림**(M2·T1 기준, 요금표 2026-09-17 mini 입력 0.75·출력 4.50달러/100만 토큰, 요청당 입력 약 60~150·출력 약 100~300토큰 가정 — 청구 금액 아님):
    - 노트북 한 번: 01 **0** · 02 **1~2**(세 모드 한 실행 + 값 바꿔 보기 한 번) · 03 **1~2**(T1, T3면 5~6) · 04 실습 **3~5** → **약 5~9번**(T3면 약 9~13번).
    - 새 커널 두 번 → 10~18(T3 18~26) · 노트북 밖 흔들림 확인 다섯 번(02 2×5 = 10 · 03 2×5 = 10 · 04 4×5 = 20) → 약 40.
    - **합계 약 50~60번(T3면 약 60~70번)**, 요청당 약 0.0005~0.0015달러 → **0.1달러 아래**. 임베딩 0. 삽화 넷(04 포함) 약 8크레딧(재생성 포함 최대 16).
12. **실행 시간**: e1~e5 모두 1초 안팎(모델 없음). 모델 절은 옛 출력 기준 요청당 1~3초 — 셸 180초 안에 여유.

## 11. 01절 작업자가 먼저 결정해야 할 것

1. **모델을 부를지(§6-1)** — M1 / **M2(01 모델 없음 · 02~04 실제 모델)** / M3. 01을 모델 없이 두면 01 사건 수는 모두 결정적이고 키 셀·모델 패키지 설치 줄이 빠짐. 02 이후는 과정 표준 모델 셀(`temperature=0`·`reasoning_effort="none"`).
2. **01 실행 모양(§2 01·§5-2)** — 일곱 모드를 **목록 하나로 한 실행**(사건 23개, Ch 24 04 b8 「한 실행」을 참으로)으로 할지, 따로 일곱 번과 견줄지 · `tasks`는 체크포인터 없이도 사건이 나온다는 설치판 사실(문서와 다름)을 체크포인터 있음/없음 두 실행으로 보일지 · `version="v2"`·`subgraphs=True`·`graph.invoke` 결과 = 마지막 values(Ch 30 03 인계)를 본문에 넣을지, 「이번에 실행하지 않았습니다」로 둘지.
3. **용어와 제목(§8-2·8-3)** — 「조각」 → 「스트림 청크」, 「사건」을 새 용어로 정할지, 03 시간 말(Ch 15 05 「첫 토큰 도착 시간」·「전체 지연」 / Ch 6 06 「걸린 초」 / 새 말 「첫 사건 시간」), 제목 영문(01 슬러그 고정 · 03 슬러그 바꿀지). `handoff.md`에 용어 표로 먼저 — 세 절 b3 「재개 사건」 고침과 `resume` 세 장면 구분 문장(§4-1)도 여기서 정함.
4. **03 측정 설계와 흔들림 처리(§6-2)** — T1(한 실행 여러 모드) / T2 / T3(되풀이) / T4(`invoke` 견주기), 결론에 쓸 결정적 관찰 목록(차례·updates 1·첫 청크 시각 < 끝·이어 붙인 글 == 최종 답·요청 수)과 「교재 출력에서는」으로만 둘 값(초·토큰·청크 수·비용)을 01절 작업 때 정해 두면 02·03 생성기 틀이 같아짐.
5. **도구 파일과 공용 옛 생성기(§7·§3)** — A/B/C와 이름(`stream_tools.py` 후보), Ch 6 06 `estimate_cost`를 옮길지(03 비용을 보일지와 함께) · `_generate_ch25_ch26.py`의 Ch 25 쪽 건너뛰기 줄을 01절에서 넣을지.

## 12. 챕터 마감으로 미룰 것

- **04 실습 절 신설**(규격 §7-2): 슬러그 후보 **`04-Streaming-실습`**(선례 `07-Persistence-실습`·`09-Middleware-실습`·`05-ToolNode-실습`·`07-create-agent-실습`·`04-Human-in-the-Loop-실습` — 챕터 제목 말 그대로) — 챕터 제목을 한국어로 바꾸면 `04-스트리밍-실습`(강사 확인). 제목 「Streaming 실습: …」, `format: experiment`, meta 「실습 30분 · 새 용어 0」(**챕터 시수 3·5h에 더하지 않음**). 새 문법·API 0, 모델 요청 3~5번. 주제 예 — Ch 21~24 도서관 소재 잇기(자료실 안내 답을 스트리밍하며 「검색 중 → 답 쓰는 중 → 끝」 custom 진행 값을 함께 보이기): 실행 1 세 모드 한 실행, 실행 2 값 하나만 바꿈(구독 목록에서 `messages`를 빼 첫 사건이 무엇이 되는지 등).
- 공용 옛 생성기 `_generate_ch25_ch26.py`는 Ch 26 마감 몫(`mv -n` → Ch 26 `qa/upgrade/before/generators/blocked/` 등, Ch 23·24 선례) · Ch 25 `figures/_gen_figures.py` `mv -n` → `qa/upgrade/before/generators/blocked/`.
- 옛 그림 9개(`figures/0N-흐름.{svg,excalidraw,caption.md}`) 삭제 승인 목록(사본 `before/figures/`, `final-artifact-hashes.json`·`ch25-code-output-preservation.sha256`이 해시를 적은 기록 파일). 챕터 공개 목록에는 옛 SVG 줄이 **원래 없음**(Ch 23·24와 다름).
- `chapter.json` `objectives`(「stream mode」·「측정」) · 절 제목 · `_build_index.py` 23행 설명(「측정합니다」) · 챕터 목차를 개선 본문과 대조 → `_build.py`·`_build_index.py`.
- 실습 폴더 README 다시 쓰기(노트북 넷, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 절마다 요청 수, 「추정 비용」 → 예상 비용, 도구 파일) · `labs/part6/continuity-guide.md` 11행(「Ch2의 비동기 실행」·「지연 시간」 — 참이 되게) · `qa/research.md`·`verification.md`·`집필점검표.md`·`authoring-checklist.md`·`research.md`에 「개선 전 판」 표시.
- Part 6 공개 목록에 04·(도구 파일) 줄 → `part6-practice.zip` 다시 만들기 → `check_delivery.py`(`llm-practice.zip` Stale 예상) · 묶음을 풀어 04 경로 셀 확인 · 옛 검사 넷 돌려 기록(`check_notebook_readiness.py` 결과 파일 되돌림). 묶음 실행 검사는 Ch 25를 안 봄(계약 없음 — 넣을지는 강사 확인).
- **뒤 챕터 인계**(고치지 않음): Ch 26 01~04 b3(참) · Ch 30 01(「조각」)·03(단일 실행 ↔ 스트리밍)·04·05·09(메타데이터) b3 · `continuity-guide.md` 두 곳 · Part 6 소개·`practice-start.md` · Ch 24 04 b8(01 슬러그·「한 실행」).
- 삭제 승인 대상: 실습 폴더 `.venv`(macOS 173MB) · `qa/upgrade/gates-wip-*.json` · `qa/upgrade/__pycache__`(생기면) · `.cache/vm/venv-ch25-streaming`(238MB) · 기기 `/tmp/ch25-prep`.

## 13. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 3 · `notebooks` 3 · `figures` 10(SVG·excalidraw·caption 각 3 + `_gen_figures.py`) · `generators` 2(**공용 `_generate_ch25_ch26.py` 사본**·`_gen_figures.py`) · `qa` 7(`public-files.json`·`prerequisite-files.json`·`research.md`·`verification.md`·`authoring-checklist.md`·`ch25-technical-review.md`·`ch25-code-output-preservation.sha256`) · 실습 폴더 3(`pyproject.toml`·`uv.lock`·`README.md`) · `chapter.json`·`집필점검표.md`·`_build.py`·`index.html`·`research.md` = **33개, 404KB**. 원본과 `cmp` 모두 같음 |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 124, 통과 0/3), `967671a0…` |
| `qa/upgrade/before-manifest.json` | sha256 **147개**(`d5114134…`) — ① 이 챕터가 읽거나 가져올 수 있는 파일: 실습 폴더 6 · Ch 24 도구 파일·01 노트북·잠금 둘 · Ch 23 도구 파일·01·05 노트북 · Ch 21 `runner_tools.py`·잠금 둘 · Ch 22 잠금 둘 · 도구 파일 일곱(Ch 13·15·16~20, 이름 피하기·`estimate_cost` 판) · Ch 2 12·Ch 6 04·06·Ch 15 05·Ch 17 04·Ch 18 03 노트북 · Ch 6 04·06·Ch 15 05·Ch 17 04·Ch 18 03·Ch 23 01·Ch 24 01 `_src` ② Ch 25를 가리키는 완료 챕터 파일: Ch 24 04 `_src`·HTML·`author_04.py`·`chapter-summary.md`·`handoff.md` · Ch 23 `chapter-summary.md` ③ Ch 25에 기대는 대기 챕터·Part 파일: Ch 26 01~04 `_src` · Ch 30 01·03·04·05·09 `_src`·`_generate.py`·`agent_service/agent.py`·`app.py`·04·09 노트북 · 연속성 안내 둘 · Part 6 소개·`practice-start.md` ④ 옛 생성기·옛 도구: `_generate_ch25_ch26.py`·`_author_ch21_ch29.py`·Ch 25 `_gen_figures.py`·`part5/_figure.py`·`.moai/…/part6b_enrich.py`·`part6b_review_fixes.py` ⑤ 묶음·목록·기록: zip 셋 · Part 6·7 공개·선행 목록 · Part 6 `qa/` 기록 열둘 + `ch25-second-technical-review.md`·`ch21-ch29-technical-review.md`·`language/ch25-*` 다섯·`ch21-ch29-final` 둘 · Part 7 `existing-artifacts-before.json`·`before-integration/build_*.py` · `notebook-contracts-part6-ch25-streaming.json`·`checks/ch25-streaming/visual-results.json` ⑥ 이 챕터 파일: `chapter.json`·`_build.py`·`index.html`·HTML 셋·`_src` 셋·그림 9·`qa/` 일곱·`집필점검표.md`·`research.md` ⑦ 공용 도구·검사: `_build_index.py`·`_notebook/build_index.py`·`build_bundle.py`·`verify.py`·`execute.py`·Part 6 검사 일곱·Part 7 묶음 검사·`builder.py`·`run_section.sh`·`nbkit.py`·`upgrade_gates.py`·`check_course_continuity.py` · `textbook/index.html`·Part 6 `index.html` |
| `$ROOT/.cache/vm/venv-ch25-streaming` | Python 3.12.13 · 238MB |

### 가상환경 만든 방법과 결과
- Ch 24 준비와 같은 방법: `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy uv venv --python 3.12.13 …/venv-ch25-streaming` → 잠금 목록 `uv export --project labs/part6/ch25-streaming --frozen --no-hashes --all-groups --no-emit-project`(실습 폴더 파일 그대로 — `pyproject.toml`·`uv.lock` 수정 시각 09-10 그대로), 주석 줄만 뺀 87줄(`/tmp/ch25-prep/req-clean.txt`, 환경 표시 `; sys_platform == …` 유지) → `uv pip install pip==26.2` → **`bin/python -m pip install --no-cache-dir -r`**. 설치 오류 0, **uv 캐시 정리(`uv cache prune`) 안 함**. 기기 루트 디스크 여유 **1.4G**(작업 전후 같음), `/tmp/uv-cache` 398MB 그대로.
- 결과: `pip freeze --all`과 잠금 대조 **판 차이 0**(설치 82 = 잠금 87 − 이 기기에 해당하지 않는 다섯: `appnope`(darwin)·`colorama`(win32)·`cffi`·`pycparser`(PyPy)·`httpx2-jsfetch`(emscripten)). `langgraph 1.2.11`·`langgraph-checkpoint 4.2.0`·`langgraph-prebuilt 1.1.0`·`langchain 1.4.0`·`langchain-core 1.6.2`·`langchain-openai 1.6.0`·`openai 3.11.0`·`python-dotenv 1.2.3`·`pydantic 2.13.5`·`tiktoken 0.14.0`·`ipykernel 7.3.0`·`nbclient 0.11.0`·`pip 26.2`. `pip check` 이상 없음. 커널 스펙 `share/jupyter/kernels/python3` 있음.
- import 확인만(`env -u OPENAI_API_KEY`): `StreamMode`·`StreamWriter`·`Command`·`interrupt`(`langgraph.types`) · `get_stream_writer` · `StateGraph`·`START`·`END` · `InMemorySaver` · `init_chat_model` · `ChatOpenAI` · `AIMessageChunk` · `dotenv`·`ipykernel`·`nbclient`. `numpy`·`pillow`·`langgraph.checkpoint.sqlite`는 없음(잠금대로). 모델 객체는 가짜 키로 만들기만 확인(요청 0). 루트 `.env`에 `OPENAI_API_KEY` 이름 한 줄 있음(값은 보지 않음). `run_section.sh`는 `$ROOT/.cache/vm/venv-<챕터 폴더 이름>`을 자동으로 씁니다.

### 참고 자료 (2026-09-25 확인)
- LangGraph Streaming `https://docs.langchain.com/oss/python/langgraph/streaming` — 모드 표(values·updates·messages·custom·checkpoints·tasks·debug, **checkpoints·tasks 모두 「Requires a checkpointer」** — 설치판 tasks와 다름) · 「With v1 (default), the output format changes based on your streaming options」 · v2 `{"type", "ns", "data"}` · `subgraphs`와 `ns` · 「In async code running on Python < 3.11, `get_stream_writer` will not work … add a `writer` parameter」 · 「message events are emitted even when the LLM is run using .invoke rather than .stream」 · `metadata["langgraph_node"]`·`tags`로 거르기. 기본 모드 문장은 없음.
- OpenAI Latency optimization `https://developers.openai.com/api/docs/guides/latency-optimization` — 「There's a huge difference between waiting and watching progress happen」 · 스트리밍은 기다리는 시간(사용자가 느끼는 시간)을 줄임. TTFT 정의는 없음 → 03 정의는 Ch 15 05 것을 이어 씀.
- 설치판 소스(`langgraph 1.2.11`): `types.py` 122~135행(`StreamMode`·설명)·138~141행(`StreamWriter` — custom 아니면 아무 일도 안 함)·264~353행(v2 `StreamPart` 일곱 모양) · `pregel/main.py` 709행(Pregel 기본 `values`)·2655~2745행(`stream()` 인자·`subgraphs` 튜플 모양·목록이면 `(mode, data)`)·3063행 `astream`·3638행 `stream_events(version v1/v2/v3)` · `graph/state.py` 1357행(컴파일 그래프 기본 `updates`) · `config.py` 126행 `get_stream_writer` · `pregel/_messages.py` 49행 `StreamMessagesHandler`(스트리밍 콜백)·259행 V2 · (`langchain-core 1.6.2`) `language_models/chat_models.py` 549~585행 `_should_stream`·1969행 부르는 자리 · (`langchain-openai 1.6.0`) `chat_models/base.py` 1332~1351행(`stream_usage` 기본 켬).
- 앞 챕터: Ch 15 05 노트북 셀 38·40(첫 토큰 도착 시간 · 전체 지연 · `첫 토큰이 끝보다 먼저 왔는가: True`) · Ch 6 04 셀 16~26(stream·청크·합치기) · Ch 6 06 b7(첫 청크까지의 시간은 재지 않음) · Ch 2 12(`async for` 0건).
