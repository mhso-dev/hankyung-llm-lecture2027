# 01절 진단 — 일곱 가지 stream mode (experiment)

- 작업일 2026-09-25. 생성기 `qa/upgrade/author_01.py`(노트북 + `_src`), 그림 설계표 `01-figures.md`, 검토 묶음 `review-pack/01-일곱-가지-stream-mode.md`.
- 옛 판 사본: `before/notebooks/01-…ipynb`·`before/_src/01-*.html`·`before/figures/01-흐름.*`(준비 담당이 복사, 원본과 `cmp` 같음).
- 챕터 리드 결정 1~11을 그대로 따랐습니다(`handoff.md` 「챕터 공통」에 옮겨 적음).

## 1. 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 후(`gates-wip-01.json`, `run_section.sh` 마지막 실행) |
|---|---|---|
| 코드 셀 | 4 | **28**(준비 셀 둘 — 설치·가져오기) |
| 검사 문장 | 83 | **387** |
| G1 | 3(c4 셀당 함수 둘 · c6 조건 표현식 · c8 집합 내포식) | **0** |
| G2 | 1(c4 20줄) | **0** |
| G3 | 0 | **0** |
| G4 | 0(모델 없음) | **0**(모델 없음 — 결정 1) |
| G5 | 5(제목 셀·핵심 그림 없음 · 결과 읽기 인용 없음 둘 · 마지막 셀 뒤 결과 읽기 없음) | **0** |
| G6 | 28(70자 초과 13 · 영문 시작 15) | **0** |
| G7 | 3(Mermaid 0 · 삽화 0 · 설계표 없음) | **0**(Mermaid 4 · 삽화 1 · 설계표) |
| 합 | **40** | **0 (PASS)** |

- 첫 실행 전 G1·G2 확인(`upgrade_gates.py … --label wip-01 --section 01`): G1 0 · G2 0 · G3 0 · G4 0 · G5 0 · **G6 2**(b8 다음 절 문장 70자 초과 · 복습 해설 1이 `` `stream`이 ``로 시작) → 실행 전에 고침 → G1~G6 0, G7 18(그림 전). 이 첫 기록 파일 `gates-wip-01-01.json`은 마지막 확인 때 같은 이름으로 다시 써져, 지금 파일은 그림 뒤 0건 판입니다.
- 코드 줄(`count_code.py`, 주석·빈 줄 뺌): 01 **41 → 155**(챕터 178 → 292). 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘 강사 확인 대상(§12).
- AST 따로(`/tmp/ch25-01/tools/extra_check.py`, Ch 24 판 복사): **0건**. 셀 모양(`shape.py`): 준비 셀이 아닌 셀 최대 **9줄**, 함수 본문 최대 5줄(주석 뺌), 정의 다섯(노드 셋·함수 둘)+상태 형식 둘, 셀당 정의 하나. 호출 깊이 최대 2(`list(graph.get_state_history(…))`·`list(get_args(StreamMode))`). 부른 내장 이름 `len`·`list`·`print`·`range`·`type`뿐. `for mode, data in …` 풀기 여섯 곳(5절 처음 쓰는 자리에 Ch 6 04 `for role, content in …` 한 문장).
- 금지어(`/tmp/ch25-01/tools/ban25.py` = Ch 24 `ban24.py` + 준비 노트 §8-2 말 「소비자」·「레이턴시」·「이벤트」·「옵션」·「스냅숏」·「태스크」·「디버그」·「메타데이터」·「도메인」·「필터링」·「명시」·「근삿값」·「워밍업」·「공정」·「단조」·「TTFT」·「total」·「first_event」·「구독」): 노트북·`_src`·캡션·`.mmd`·prompt에서 **참 금지어 0**. 걸린 것은 거짓 양성뿐 — 「체크포인터」 안 「포인터」 · Ch 23 03 「스레드 재개」를 가리키는 문장(b3·노트북 9절, 준비 노트가 허용한 자리) · 기록 파일 `01-5-….prompt.md`의 제목 「프롬프트 (1차, 채택)」·「최대 차이 0」(Ch 24 prompt 파일과 같은 틀, 학생 묶음 밖). 한정어 없는 「청크」 0(「스트림 청크」 둘 — b8·노트북 정리의 02절 예고). 「한 겹 더」 0.

## 2. 수정 전 주요 문제 (옛 판)

1. **일곱 모드를 따로 일곱 번 실행**(스레드 `mode-0`~`mode-6`) — Ch 24 04 b8(완료) 「한 실행에서 생긴 사건을 일곱 방식으로 받아 보는 방법」과 어긋남.
2. **틀린 사실**: b4 정의·b7 둘째 항목·복습 2 「checkpoints와 tasks는 체크포인터가 있어야 사건이 생깁니다」 — 설치판 출력은 체크포인터 없이 tasks 4·debug 4(준비 노트 e1, 이번 노트북 8절).
3. b3 「Ch24에서 interrupt와 재개 사건을 확인했습니다」(세 절 같은 글) — Ch 24에는 스트림 사건 0건. `resume` 세 장면 구분 없음.
4. 한 셀에 노드 둘·힌트 `(state: State) -> dict[str, str]`·f-string 계산 `f"{state['topic']} 스트리밍 요약"`·형식 지정 `f"{mode:11} …"`·호출 결과를 바로 호출 `get_stream_writer()({...})`·조건 표현식·집합 내포식·`enumerate`·20줄 셀. 상태 형식 이름 `State`.
5. 금지어 다수(반환·조각·스냅숏·소비자·태스크·디버그·옵션·필드·분기·측정 등), 제목 말 「stream mode」 풀이 없음, 결과 읽기 셀 0, 핵심 그림 0, 옛 그림 토큰 `{{svg:01-흐름}}`(상자 셋 흐름도, 본문과 1:1 아님).
6. 설치 셀이 쓰지 않는 모델 패키지(`langchain`·`langchain-openai`·`python-dotenv`)까지 설치.
7. b10 참고 자료 셋이 세 절 같음(확인 2026-09-11).

## 3. 바꾼 것 (결정)

- **모델 없음(결정 1, M2의 01 몫)**: 노드 둘(`prepare` — 앞뒤 빈칸 지우기·진행 값 50, `write` — 「안내 초안」 붙이기·진행 값 100) + `InMemorySaver`. 키 셀·`dotenv`·임시 폴더 없음(파일 0). 설치 셀은 `langgraph==1.2.11`·`langgraph-checkpoint==4.2.0`만(잠금 판). 입력 `{"topic": " 배송 문의 ", "draft": ""}`(옛 판 「고객 문의」·「배송」 소재를 하나로 — 앞뒤 빈칸이 `values` 첫 사건과 갱신에서 보이게).
- **일곱 모드를 한 실행에(결정 2)**: 모드 이름은 설치판 `StreamMode`에서 `get_args`로 꺼냄(`['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom']` — 공식 문서 표와 이름 같음). 한 실행 사건 **23**, 모드별 수·나온 자리(함수 `positions_of`)·첫 사건 모양(자료형·키)·모드별 내용(values·updates·custom 차례 / checkpoints 단계·만든 자리·다음 노드·칸 값 / tasks 시작·끝 키와 `result` / debug `type` 여덟).
- **결정적 확인**: 새 스레드 `all-2`로 한 번 더 → 사건 수 `23 23`·모드 이름 차례 같음(`assert`) · 모드 하나씩 따로 일곱 번(`[mode]` 목록) → 한 실행 수와 모두 같음 · 체크포인터 없이 다시 컴파일 → 사건 15, `checkpoints 4 → 0`·`debug 8 → 4`(type `task`·`task_result`만)·`tasks 4 → 4`(**틀린 사실 바로잡음** — b6·b7·노트북 8절에 공식 문서 표와 다르다고 밝힘).
- **기본 모드·`stream`이 실행을 늦게 시작함·`invoke` = 마지막 values**: `graph.stream(...)` → `generator`·꺼내기 전 체크포인트 0 → 다 꺼낸 뒤 4 · `graph.stream_mode` = `updates`(사건 둘, 진행 값 없음 — 쓰기 함수는 `custom`이 아니면 아무 일도 안 함, 설치판 `types.py` 138~141행) · `invoke` 결과 == 마지막 `values` 사건 `True`(설치판 `pregel/main.py` 3913~3955행).
- **9절 Ch 24 이음(결정 4)**: `SendState`·노드 `ask_send`(멈춤 표시) → 모드 `updates`로 첫 실행 → 사건 하나 `['__interrupt__']`·질문 값 → `Command(resume="approve")` → 사건 `{'ask_send': {'answer': 'approve'}}` 한 줄. `Interrupt.id`는 출력하지 않음. b3·노트북 9절에 `resume` 세 장면 구분 문장.
- **동기 `stream`만(결정 3)**: `astream`·`version="v2"`·`subgraphs=True`는 b7에 「이번에 실행하지 않았습니다」 한 문장(설치판 기본 `version="v1"`).
- **용어(결정 4)**: 새 말 셋 — 스트림 모드 · 스트림 사건 · 진행 값(§9). 제목 「stream mode」는 제목에 두고 b2·노트북 1절 첫 자리에서 「스트림 모드」로 풂.
- **도구 파일 만들지 않음(결정 5)**: §6.
- **문법(결정 9)**: 노드 힌트 없음, 상태 형식 Ch 13 모양 두 이름(`DraftState` 칸 `topic`·`draft` / `SendState` 칸 `topic`·`answer`), f-string·조건 표현식·내포식·`enumerate`·호출 결과 바로 호출 없음(`writer = get_stream_writer()` 다음 줄 `writer({...})`), 셀 10줄 이하.
- **그림**: Mermaid 4 + 삽화 1(§7), 옛 `figures/01-흐름.*` 셋은 그대로(본문 참조 0).
- **b10 참고 자료**: Streaming 문서(2026-09-25 다시 확인) · 설치판 소스 행 넷 · 앞 챕터 셋.

## 4. 새 커널 실행 (모델 요청 0, 키 없이)

| 실행 | 어디서 | 시각(UTC) | 결과 |
|---|---|---|---|
| T | 사본 `/tmp/ch25-01/T/`(`execute.py`, `env -u OPENAI_API_KEY`) — 실습 폴더에 `.failure.json`이 남지 않게 먼저 | 17:40:32 | PASS 28셀 |
| B | 사본 `/tmp/ch25-01/B/` — **그림을 그리기 전** 두 번째 새 커널 | 17:40:45 | PASS 28셀, T와 셀별 출력 **28/28 같음** |
| A | `run_section.sh … 01`(실습 폴더, 그림 뒤 첫 판) | 17:44:48 | PASS, B와 28/28 같음 |
| **A2(교재 출력)** | `run_section.sh … 01`(Ch 23 01 체크포인트 수 문장·Ch 22 06 문장을 바로잡은 뒤 — 마크다운만 바뀜) | **17:46:35** | PASS, **B와 28/28 같음** |

- 네 실행 모두 `code_sha256` **`650e86fce1fa2d9e7b4d902ce2de6e86ee6f0bc6d6fadbbb47dbc416569b6e83`** · `outputs_sha256` **`5027ff86da5a1117cdc2703d55314282f2fecffc76e82e6551afb322dd4aac7d`**(설치 셀 스트림 나뉨 차이도 없었음). 노트북 파일 `723a4a14824f…`(A2, 그림 첨부 포함).
- 실행마다 달라지는 값(체크포인트 `config` 아이디·작업 `id`·debug `timestamp`·`Interrupt.id`)은 한 번도 출력하지 않았습니다.
- 노트북 밖 확인(`/tmp/ch25-01/probe/`, `env -u OPENAI_API_KEY`, 같은 가상환경): `p1.py`(노트북 값 전부 미리 — 같음) · `p2.py`(멈춤 표시를 `updates`·`tasks`로 — `tasks` 끝 사건 `interrupts` 칸에 `value`·`id`) · `p3.py`(같은 스레드 `all-1`로 두 번 → 사건 23 그대로, 단계 `[-1, 0, 1, 2]` → `[3, 4, 5, 6]`, 체크포인트 4 → 8 — b7·준비물 문장의 근거).
- 가상환경 `.cache/vm/venv-ch25-streaming`(준비 담당, 잠금 판) 그대로 — 설치 0. 걸린 시간은 재지 않았습니다.

## 5. 라이브러리 확인 (2026-09-25)

- 설치판 소스(`langgraph 1.2.11`): `types.py` 122~124행 `StreamMode = Literal["values", "updates", "checkpoints", "tasks", "debug", "messages", "custom"]`·125~135행 설명(debug = 「Emit "checkpoints" and "tasks" events」) · 138~141행 `StreamWriter`(「no-op when not using stream_mode="custom"」) · `graph/state.py` 1357행 `stream_mode="updates"`(컴파일한 그래프) · `config.py` 126행 `get_stream_writer` · `pregel/main.py` 2655~2672행 `stream()` 인자(`version: Literal["v1", "v2"] = "v1"`·`subgraphs=False`) · 3913~3955행 `invoke`(v1: 안에서 `stream(…, ["updates", "values"])`, 마지막 values를 `latest`로).
- 공식 문서 `https://docs.langchain.com/oss/python/langgraph/streaming`(WebFetch 2026-09-25): 모드 표 일곱 · `checkpoints`·`tasks` 모두 「Requires a checkpointer」(debug는 「combines checkpoints and tasks」) · 「With v1 (default) … single mode returns raw data, multiple modes return (mode, data) tuples」 · 기본 모드 문장 없음. → **설치판 출력(tasks 4, 체크포인터 없이)과 문서 표가 다름** — 출력 기준으로 쓰고 b6·b7·노트북 8절에 차이를 밝힘.

## 6. 도구 파일 — 만들지 않음 (결정 5)

- 이 절이 쓰는 앞 챕터 함수가 없습니다(Ch 6 06 `estimate_cost`·Ch 19 `sum_usage` 모두 모델 없는 01에서 쓸 일 없음). 이 절이 처음 가르친 함수 `collect_events`·`positions_of`는 규격 §2-7 3번대로 노트북에 둡니다.
- 02 이후가 이 둘이나 앞 챕터 함수를 쓰면, **처음 쓰는 절이 `labs/part6/ch25-streaming/notebooks/stream_tools.py`를 만들고** 01 노트북 셀 글 그대로 옮깁니다(`handoff.md` 「도구 파일」에 두 함수 본문과 주석 머리줄). `labs/` 안 같은 이름 파일 0(준비 노트 §7).

## 7. 그림 (`01-figures.md`)

- Mermaid 넷: 01-1 한 실행에서 받은 일곱 모드(725) · 01-2 스물세 사건이 나온 자리(252) · 01-3 체크포인터가 있을 때와 없을 때(529) · 01-4 같은 그래프를 받는 세 방법(798) — 괄호는 원본 viewBox 폭, 모두 868 이하. 첫 렌더 뒤 01-3(두 칸이 위아래로 쌓임)·01-4(폭 936)·01-2(줄 꺾임) 고쳐 다시 렌더, PNG 넷 직접 확인. 색 보라 0·빨강 0, `graph.stream`·공통 상자 회색, 노드·그래프 파랑, 입력 초록, 출력 노랑. 라벨 숫자는 4·5절 출력의 나온 자리와 진행 값 50·100뿐, 개수는 한글.
- 삽화 01-5 대나무 홈통과 일곱 그릇: **1차 job `cde26edf-d411-4ad1-a753-2407b4441a4c` 채택**(재생성 0), 거래 2026-09-25T17:42:24Z 「Nano Banana Pro −2」 한 줄 = **이 절 몫 2크레딧**(생성 전 잔액 2423.75, 바로 앞 거래 15:29:48Z는 Ch 24 04절). 원본 `13280ade…`(2752×1536) → 저장 PNG 1100×614 `d4c2d8bf…`, 결과 URL 다시 받아 같은 폭으로 줄인 그림과 픽셀 대조 bbox `None`·최대 차이 0. 저장 PNG와 같은 사본을 직접 열고, 오른쪽 절반을 잘라 크게 다시 봐 구멍 일곱·그릇 일곱·물방울 없는 여섯째 구멍과 빈 여섯째 그릇을 셌습니다.

## 8. 공용 옛 생성기 처리 (결정 6)

- **`textbook/part6/_generate_ch25_ch26.py`**(챕터 밖, Ch 26도 씀): `545db83c…` → **`0767052613d98edabf9fe54efe9efce4d8e452952df0f46caf6b35a1fa9f1b9c`**. 머리 설명 주석 넷 + `write()`의 노트북 반복·챕터 반복과 `write_pages_only()` 반복에 `if chapter == "ch25-streaming": continue`(줄마다 까닭 주석, 두 곳은 `skip ch25` 알림). Ch 21 `_author_ch21_ch29.py` 선례 모양.
- **Ch 26 쪽 동작 그대로 확인**: 사본 기기 `/tmp/ch25-01/gen/`에 빈 폴더 틀을 만들고 옛 판·새 판을 각각 `write()`·`--pages-only`로 돌려 결과 파일 해시 목록을 견줌 — 옛 판 28개(Ch 25 13 + Ch 26 15) ↔ 새 판 15개(**Ch 26 15개 해시 모두 같음**, Ch 25 0개). `--pages-only`도 옛 7 ↔ 새 4(Ch 26 넷 같음, Ch 25 0). 연결 폴더 안에서는 돌리지 않았습니다.
- **`figures/_gen_figures.py`**(Ch 25): 맨 위 설명 주석 셋 + `raise SystemExit(...)` — `45d88f5e…` → **`cb02fe4e59dff46091f162c66b035c0beb3e39a88d367596a42e89ea7a053041`**, 실행하면 종료 코드 1로 멈춤 확인. 옮기기(`mv -n` → `qa/upgrade/before/generators/blocked/`)는 챕터 마감 몫, 공용 생성기 옮기기는 Ch 26 마감 몫.

## 9. 용어 (01이 정함 — `handoff.md` 표와 같음)

| 말 | 뜻 | 코드에서 |
|---|---|---|
| 스트림 모드(stream mode) | 한 실행에서 생긴 일 가운데 무엇을 어떤 모양으로 받을지 고르는 이름 | 인자 `stream_mode`의 글, 설치판 일곱 |
| 스트림 사건 | 메서드 `stream`이 한 번에 하나씩 내놓는 값 — Ch 22 06 감사 기록의 「사건」(훅이 적은 사건 이름과 값)과 다른 말(b3 한 문장) | `for`가 꺼낸 값, 목록으로 고르면 `(모드 이름, 자료)` 짝 |
| 진행 값 | 노드가 실행 도중에 쓰기 함수로 직접 보내는 값 | `get_stream_writer()`로 꺼낸 함수에 넣은 딕셔너리, `custom`으로만 받음 |

- 이어 쓴 말: 작업(task, Ch 23 05) · 체크포인트·만든 자리·단계 번호(Ch 23 01) · 멈춤 표시·질문 값·사람의 답으로 이어 가기(Ch 24 01) · 설계 객체·상태 형식·칸·갱신(Ch 13·24) · 제너레이터(Ch 6 04).
- 쓰지 않은 말: 「조각」·「청크」(한정어 없이)·「구독」(→「고른다」·「함께 받는다」)·「반환」·「소비자」·「지연」·「추정」·「측정」·「이벤트」·「태스크」·「디버그」·「스냅숏」·「옵션」·「필드」·「메타데이터」·「재개」(Ch 23 03 이름 말고). 시간 말(첫 토큰 도착 시간·전체 걸린 시간·첫 사건 시간)은 03 몫이라 01에 없음.

## 10. 완료·대기 챕터 문장 대조

- **참이 됨**: Ch 24 04 b8 「Ch 25 01절에서는 한 실행에서 생긴 사건을 일곱 방식으로 받아 보는 방법」 — 01 노트북 4절(한 실행 23사건)·b1·b6. 슬러그 그대로라 링크 살아 있음(빌드 HTML 확인).
- **참 그대로**: Ch 23 요약 §15 「Ch 25 01~03 b3 「Ch23에서 체크포인터와 thread_id」 참」 — 01 b3가 Ch 23 01(체크포인터·스레드)·05(작업)를 가리킴. Ch 24 요약 §14 요청(「재개 사건」 바로잡기 + `resume` 겹침 한 문장) — 01 b3 둘째·셋째 단락·노트북 9절로 반영(02·03 b3는 각 절 몫).
- **대기 챕터(고치지 않음)**: Ch 26 01~04 b3 「Ch25에서는 실행 사건을 스트리밍했습니다」 참 · Ch 30 03 「단일 실행과 스트리밍이 같은 실행 객체의 다른 소비 방법」 — 01 6절 `invoke` == 마지막 values(`True`)로 **이제 참**(말 「소비」는 Ch 30 몫) · Ch 30 04 「스트림 모드와 진행 이벤트를 비교」 참 · Ch 30 09 「메타데이터를 읽었다」는 02 몫 · Ch 30 01 「조각」은 Ch 30 몫.
- 틀린 사실을 앞 챕터에서 가져온 문장 0. 01 첫 판의 「Ch 23 01절에서 노드 둘짜리 그래프를 … 넷」은 Ch 23 01 노트북(노드 하나 `add`, 실행 한 번에 셋)과 달라, A2 전에 「노드 하나짜리 … 셋, 이 그래프는 노드가 하나 더 있어 넷」으로 고침(준비 노트 §4-1·§5-2 「Ch 23 01 노드 둘 4」 표기도 Ch 23 01에는 맞지 않음 — 인계에 적음).

## 11. 챕터 밖 수정

| 파일 | 전 → 후 | 까닭 |
|---|---|---|
| `textbook/part6/_generate_ch25_ch26.py` | `545db83c` → `07670526` | §8 공용 옛 생성기 Ch 25 쪽 건너뛰기(Ch 26 동작 같음) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch25-streaming.json` | `e4366f11` → `22d280f9` | `verify.py --chapter`가 다시 씀(`run_section.sh`) |

- 실습 폴더(챕터 몫): 01 노트북만(`c7b77265` → `723a4a14`). README·`pyproject.toml`·`uv.lock`·02·03 노트북 그대로. 공개 목록·zip·Part 6 목차 그대로(도구 파일 없음 — 목록 바뀔 것 없음).

## 12. 강사 확인 대상

1. 제목 말 「stream mode」(제목·슬러그에만, 본문은 「스트림 모드」) — 슬러그는 Ch 24 04 링크로 고정.
2. 코드 줄 41 → 155·코드 셀 4 → 28(Ch 24 선례 28) — 한 실행·두 번·따로·체크포인터 없이·`invoke`·Ch 24 이음을 모두 출력으로 보이느라 늘었습니다. 9절(셀 다섯)을 뺄지.
3. 새 이름 `get_args`·`StreamMode`로 설치판 모드 이름을 꺼낸 것(손으로 적은 목록 대신) · `graph.stream_mode` 속성으로 기본 모드를 보인 것.
4. 비유 계열 「대나무 홈통과 물방울」(삽화: 구멍·그릇 일곱, 빈 여섯째 = `messages`).
5. 준비물의 「걸린 시간은 재지 않았습니다」(Ch 24 선례).

## 13. 참고 자료 확인

- LangGraph Streaming 문서 — 2026-09-25 WebFetch(§5). 설치판 소스 행은 가상환경 `site-packages/langgraph`에서 `sed -n`·`grep -n`으로 다시 셈(준비 노트의 `pregel/main.py` 2655행 = 실제 `def stream(`, 오버로드 2616·2636행 앞).

## 14. 남은 것과 지우지 않은 것

- 다음 절 인계는 `handoff.md` 「§01 → §02」.
- **지워야 하지만 지우지 않은 것(삭제 승인 대상)**: `qa/upgrade/gates-wip-01-01.json`·`gates-wip-01.json`(마감 `gates-after.json`으로 갈음) · `.cache/ch25-01-view/`(PNG 사본 넷·삽화 사본·잘라 본 그림 `crop-right.png`) · 기기 `/tmp/ch25-01/`(`T/`·`B/` 노트북 사본 · `gen/`(옛 생성기 사본과 빈 폴더 틀 넷·해시 목록) · `probe/`(`p1~p3.py`) · `illu/`(원본·다시 받은 원본·1100 판) · `tools/`(`ban25.py`·`cmpout.py`·`extra_check.py`·`shape.py`) · `manifest-now.txt`). 옛 그림 `figures/01-흐름.{svg,excalidraw,caption.md}`는 챕터 마감의 삭제 승인 목록.
- `qa/upgrade/__pycache__`·실습 폴더 `notebooks/__pycache__`는 만들지 않음(`PYTHONDONTWRITEBYTECODE=1`·`python3 -B`).

## 마감 반영 (2026-09-25, 검토 1차)

검토 `review-round1-A.md`의 01절 몫 [하] 둘(A-1·A-2)을 반영했습니다. **노트북은 다시 실행하지 않았습니다** — `code_sha256` `650e86fce1fa…`·`outputs_sha256` `5027ff86da5a…`·`executed_at` 17:46:35Z 그대로(파일 `723a4a14…` → `be881fc5…`, 마크다운과 그림 첨부만). 고친 방법: `.cache/ch25-close/tools/gpatch.py`(생성기 문자열과 노트북 마크다운을 함께, 코드 셀에 옛 글이 있으면 멈춤) → `author_01.py --src-only` → `genmatch.py`(59셀·`_src` 같음) → `render_mermaid.py --only 01-1 --force` → `run_section.sh … 01 --no-exec`(그림 첨부만 갈아 끼움).

- **A-1 무리 이름**: 그림 01-1 왼쪽 아래 상자 「칸 값에서」 → **「칸 값과 진행 값에서」**(alt·노트북 「오늘 볼 그림」 alt 같이) · 노트북 5절 설명 셀 「칸 값에 관한 세 모드」 → 「칸 값과 진행 값에 관한 세 모드」 · 셀 36 「모드 `debug`는 다른 모드의 사건을」 → 「모드 `checkpoints`·`tasks`의 사건을」(설치판 `types.py` 135행). **셀 31 코드 주석**(「칸 값에 관한 세 모드(values·updates·custom)」)은 코드라 그대로 두고, 셀 32 결과 읽기에 「진행 값은 상태의 칸에 들어가지 않으므로, 셀 주석의 「칸 값에 관한 세 모드」는 칸 값과 진행 값에 관한 세 모드로 읽습니다」 한 문장 — 주석 고침은 **다음 재실행 몫**(`author_01.STATE_MODES` 첫 줄).
- **A-2 `messages` 0개의 까닭**: 설치판 `langgraph/pregel/_messages.py` 49~54행(모델 스트림 + 노드 출력 속 메시지 객체)·223~246행(`on_chain_end` → `_find_and_emit_messages`)을 이 기기 가상환경 파일로 다시 읽음. b7에 한 항목(「노드가 내놓은 메시지 객체도 보낸다고 적습니다 … 이번에 실행하지 않았습니다」) · b8·노트북 정리 2 「모델이 없어 `messages`만 0개」 → 「노드가 모델을 부르지 않고 글만 내서, `messages`만 0개」 · b6 표 「이 그래프에는 모델이 없음」 → 「노드가 모델을 부르지 않고 글만 냄」 · 캡션 01-1(파일·`_src`) 「모델이 없어 messages만 비었습니다」 → 「그 가운데 messages만 비었습니다」. 학습 목표 3(「체크포인터나 모델이 없을 때」)과 b4 「공식 문서와 설치판 설명은 … 모델의 답을 보낸다」는 이 그래프에서 참이라 그대로.
- 게이트 01: G1~G7 0(코드 셀 28, 검사 문장 389 → **395**). 마감이 더한 문장의 새 금지어 걸림 0(`bandiff.sh` — 「체크포인터」 안 「포인터」 거짓 양성 말고).
- **지우지 않은 것 더함**: `gates-wip-01.json`은 마감 `run_section.sh … 01 --no-exec`가 다시 씀(내용은 PASS, 절 작업 때 판은 `.cache/ch25-close/pre/`).
