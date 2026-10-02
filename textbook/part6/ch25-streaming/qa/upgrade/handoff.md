# Ch 25 Streaming — 절 사이 인계 (handoff)

- 읽는 순서: 과정 요약 → Ch 24 `chapter-summary.md` → 준비 조사 `qa/upgrade/chapter-lead-notes.md` → **이 파일** → 앞 절 `NN-diagnosis.md`·완료본(`_src`·노트북·생성기).
- 01절 완료 2026-09-25(게이트 40 → 0, 코드 셀 28, 새 커널 네 번 28/28 같음 — 모델 요청 0, 키 없이). 세부 값은 `01-diagnosis.md`.
- 02절 완료 2026-09-25(게이트 34 → 0, 코드 셀 25, 실제 모델 첫 절 — 노트북 요청 2·흔들림 확인 10, 새 커널 세 번 중 결정적 셀 17/25 같음, 도구 파일 `stream_tools.py` 신설). 세부 값은 `02-diagnosis.md`·`02-probe.md`.
- 03절 완료 2026-09-25(게이트 50 → 0, 코드 셀 24, T1 한 실행에 세 모드 + 사건마다 시각 — 노트북 요청 2·흔들림 확인 10, 새 커널 세 번 16/24 같음(갈린 여덟은 초·사건 수·출력 토큰·비용 셀), 도구 파일에 `mode_order`·`estimate_cost` 더함). 세부 값은 `03-diagnosis.md`·`03-probe.md`. **본문 마지막 절 — 다음은 04 실습 절**(아래 「§03 → 실습(04)」).
- 04절 완료 2026-09-25(**챕터 끝 실습 절 신설** `04-Streaming-실습` — 게이트 0, 코드 셀 20, 자료실 문의 창 흉내에 01 모드 목록·02 진행 값과 스트림 청크 이어 붙이기·03 사건마다 시각 적기, 실행 1 → 같은 설정 다시 → 실행 2(칸 `show_notice` 하나) — 노트북 요청 3·흔들림 확인 10, 새 커널 세 번 15/20 같음(갈린 다섯은 사건 수·답 글·초 셀), 도구 파일에 03절 함수 셋과 `import time`). 세부 값은 `04-diagnosis.md`·`04-probe.md`. **다음은 챕터 검토·마감**(아래 「실습 → 챕터 검토」).
- **전체 마감 2026-09-30 — 도구 파일 머리 줄**: `stream_tools.py` 머리 설명 1행(「앞 챕터와 이 챕터 앞 절에서 배운 …」)·6행(함수 일곱 출처, 두 줄로)만 고침 — `3a734aeb…` → **`6df804b89b55ff77b1a148746b68c021767b1ddf7163d6a2194e94c922127db4`**(함수 본문·노트북 해시 같음, 생성기 `author_02.TOOLS_HEAD` 한 곳, 뒤 챕터 고정값 Ch 26 `author_01.STREAM_SHA`·Ch 30 `author_04.STREAM_TOOLS_SHA`도 새 값). 기록 `textbook/qa/final-close-log.md` 2단계·`chapter-summary.md` §8 끝.

## 챕터 공통 (01절에서 정한 것)

### 챕터 리드 결정 (그대로 이어 지키세요)

1. **모델 선택 M2** — **01은 모델 없이**(노드 둘 + `InMemorySaver`, 키 셀·`dotenv` 없음, 모드 `messages` 사건 0을 출력으로 보이고 02로 넘김). **02·03·04는 실제 모델**: `nbkit.key_and_model_cells("openai:gpt-5.4-mini")`(`temperature=0`·`reasoning_effort="none"`, 키는 루트 `.env`에서만, 값 출력 금지). 가짜 채팅 모델(`GenericFakeChatModel` 등) 금지(규격 §3 — 준비 노트 e3은 조사 전용).
2. **01 모양 = 일곱 모드를 한 실행에**(끝남): 설치판 `StreamMode`를 `get_args`로 꺼낸 목록 → 한 실행 사건 **23**, 모드별 수·나온 자리·모양, 두 번 같음(`assert`), 따로 일곱 번 = 한 실행 수, 체크포인터 없이 → `tasks` 4 그대로(옛 판 틀린 사실 바로잡음), 기본 모드 `updates`, `invoke` = 마지막 values(`True`). `version="v2"`·`subgraphs=True`·`astream`은 01 b7 「이번에 실행하지 않았습니다」.
3. **동기 `stream`만** — `astream`·`async for`는 쓰지 않음(Ch 2 12가 `async for`를 가르치지 않음). 필요하면 「이번에 실행하지 않았습니다」 한 문장(01 b7에 있음).
4. **용어**(아래 표). 시간 말은 Ch 15 05 **「첫 토큰 도착 시간」**을 이어 쓰고, 끝까지 걸린 시간은 **「전체 걸린 시간」**(「지연」은 Ch 18 금지어), 새 말 **「첫 사건 시간」**은 03 몫. 제목 「stream mode」는 제목에 두고 본문 첫 자리에서 「스트림 모드」로 풂(강사 확인). **`resume` 세 장면 구분 문장**(Ch 23 03 스레드 재개 · Ch 23 04·06 worker 단계 `resume` · Ch 24 `Command(resume=…)`)은 01 b3 셋째 단락·노트북 9절에 있음 — 02·03 b3의 「Ch24에서 interrupt와 재개 사건」을 고칠 때 되풀이하지 말고 「01절에서 본 것처럼」으로.
5. **도구 파일 B안 `labs/part6/ch25-streaming/notebooks/stream_tools.py`** — **01은 만들지 않음**(쓰는 앞 챕터 함수 없음). 처음 쓰는 절이 만듦(아래 「도구 파일」). 앞 챕터 도구 파일은 파일째 가져오지 않음(numpy·SQLite 의존).
6. **공용 옛 생성기** `textbook/part6/_generate_ch25_ch26.py`는 01이 Ch 25 쪽만 건너뛰게 함(`0767052613d9…`, Ch 26 쪽 동작 같음 — 사본 대조) · `figures/_gen_figures.py` 맨 위 `raise SystemExit`(`cb02fe4e59df…`). 옮기기는 마감 몫(`_gen_figures.py`는 Ch 25 마감 `mv -n` → `qa/upgrade/before/generators/blocked/`, 공용 생성기는 Ch 26 마감).
7. **슬러그 바꾸지 않음** — 01은 Ch 24 04 b8이 링크, 02·03도 그대로.
8. **03 설계 T1**(아래 「03 설계」).
9. **문법 범위**(아래 「허용 문법 범위」).
10. **비유 계열 「대나무 홈통과 물방울」**(01이 엶, 아래).
11. **준비 셀은 과정 표준** — 설치 `%pip` 줄은 잠금 판 번호까지, 그 절이 쓰는 패키지만 · import · 키·모델 셀(02~) · 파일을 쓰면 임시 폴더(01은 파일 0이라 없음).

### 준비 셀 (01 판)

- 설치: `nbkit.install_source(["langgraph==1.2.11", "langgraph-checkpoint==4.2.0"])` → 출력 `langgraph: 1.2.11`·`langgraph-checkpoint: 4.2.0` → 결과 읽기에 실행일(`RUN_DATE`). **02 이후 모델 절**은 잠금 판 `langchain==1.4.0`·`langchain-openai==1.6.0`·`langgraph==1.2.11`·`python-dotenv==1.2.3`(+ 체크포인터를 쓰면 `langgraph-checkpoint==4.2.0`) — 실습 폴더 `pyproject.toml` 직접 의존과 잠금 판이 같음, dev `pip==26.2` 있음.
- 가져오기(01 판): `from typing import get_args` · `from typing_extensions import TypedDict` · `from langgraph.graph import StateGraph, START, END` · `from langgraph.checkpoint.memory import InMemorySaver` · `from langgraph.config import get_stream_writer` · `from langgraph.types import Command, StreamMode, interrupt` + 가져온 이름 `print`. 뒤 절은 쓰는 이름만.
- 키·모델(02~): `nbkit.key_and_model_cells("openai:gpt-5.4-mini")` 그대로(`KEY` 준비 셀 → 모델 셀 → 실행일 결과 읽기). 옛 02·03의 `[Path.cwd(), *…parents]` 키 찾기·`MODEL` f-string·`temperature` 없음(G4 2)은 모두 이 셀로 바꿈.

### 01이 푼 문장 (뒤 절은 되풀이하지 말고 「01절에서 본 것처럼」으로)

- 메서드 `stream`은 제너레이터를 내놓고, `for`가 꺼낼 때 실행이 시작됨(꺼내기 전 체크포인트 0 → 다 꺼낸 뒤 4, Ch 6 04 `model.stream()`과 같은 성질) · 모드를 고르지 않으면 컴파일한 그래프는 `updates`(`graph.stream_mode`, 설치판 `graph/state.py` 1357행) · 모드를 목록으로 고르면 사건이 `(모드 이름, 자료)` 짝, `for mode, data in …`로 풂(Ch 6 04 `for role, content in …` 한 문장) · 모드 하나를 글로 주면 자료만(공식 문서 v1) · 쓰기 함수는 모드 `custom`을 고르지 않으면 아무 일도 안 함(3절 출력 + 설치판 `types.py` 138~141행) · `invoke` = 마지막 values 사건(`pregel/main.py` 3913~3955행) · 모드를 함께 골라도 모드별 사건 수는 따로 고를 때와 같음 · 체크포인터 없이 `checkpoints` 0·`tasks` 그대로(문서 표와 다름) · 멈춤 표시는 모드 `updates`에서 키 `__interrupt__` 사건 하나, 이어 가기는 이어 간 노드의 갱신 한 줄(따로 「resume 사건」 모드 없음).

### 용어 (01절에서 정한 것 — 뒤 절은 그대로 이어 씁니다)

| 말 | 뜻 | 코드에서 | 비고 |
|---|---|---|---|
| **스트림 모드(stream mode)** | 한 실행에서 생긴 일 가운데 무엇을 어떤 모양으로 받을지 고르는 이름 | 인자 `stream_mode`의 글(설치판 일곱 — `values`·`updates`·`checkpoints`·`tasks`·`debug`·`messages`·`custom`) | 제목 말 「stream mode」는 제목에만. 문장 첫머리는 「모드 `values`는」처럼 |
| **스트림 사건** | 메서드 `stream`이 한 번에 하나씩 내놓는 값 | `for`가 꺼낸 값, 목록으로 고르면 `(모드 이름, 자료)` 짝 | **Ch 22 06 감사 기록의 「사건」(훅이 적은 사건 이름과 값)과 다른 말**(01 b3). 「이벤트」 금지 |
| **진행 값** | 노드가 실행 도중에 쓰기 함수로 직접 보내는 값 | `writer = get_stream_writer()` 다음 줄 `writer({...})`, 모드 `custom`으로만 받음 | 01 값 `{"stage": …, "progress": 50/100}`은 우리가 정한 값(라이브러리가 계산한 진행률 아님) |
| (02 몫, 이어 씀) **스트림 청크** | Ch 6 04 청크(스트리밍에서 한 번에 도착하는 답의 일부 — 토큰과 단위가 다름) | 모드 `messages` 사건의 앞 값 `AIMessageChunk` | **「조각」은 Ch 5 토큰 전용 — 쓰지 않음.** 한정어 없는 「청크」도 금지(과정 §5 「청크」 결정) |
| (03 몫) 첫 토큰 도착 시간 · 전체 걸린 시간 · 첫 사건 시간 | Ch 15 05 정의(글자가 든 첫 스트림 청크까지) · 끝까지 · 모드와 관계없이 처음 받은 사건까지(03이 세 문장으로 정함) | `time.perf_counter` | 「TTFT 근삿값」·「total」·「first_event」·「지연」·「레이턴시」 금지. 제목 「TTFT와 total」은 03 몫(슬러그 그대로) |
| (이어 씀) 작업(task) · 체크포인트 · 만든 자리 · 단계 번호 | Ch 23 05·01 | `tasks` 사건 · `checkpoints` 사건의 `metadata["step"]`·`["source"]` | 「태스크」·「스냅숏」 금지 |
| (이어 씀) 멈춤 표시 · 질문 값 · 사람의 답으로 이어 가기 | Ch 24 01 | `interrupt(질문 값)`·`Command(resume=…)` | 「재개」 금지(Ch 23 03 「스레드 재개」를 가리킬 때 말고) |

- 새 용어 meta: 01 = **3**(스트림 모드·스트림 사건·진행 값). 02·03은 각 절이 정함(옛 meta 5는 옛 생성기의 틀 값 — 실제 새 말 수로).
- 쓰지 않는 말 「구독」 → 「받을 모드로 고른다」·「함께 받는다」(01 0건 — 02도 이렇게 권함).

### 금지어 (01 설명·주석·캡션·`.mmd`·prompt 0건 — 제목·슬러그·코드 백틱 말고)

- Ch 24 목록 전부(「반환」·「경로」·「런타임」·「payload」·「스냅샷」·「스키마」·「검증」·「포인터」(단독)·「소비」·「분기」·「지연」·「추정」·「직렬화」·「재시작」·「재실행」·「재개」·「게이트」·「중단」·「인터럽트」·「조각」 + Ch 23 목록 「지시」·「trace」·「병렬」·「채널」·「식별자」·「레코드」·「로그」·「보장」·「측정」·「필드」·「사전」·「동시」·「순차」·「돌려줍니다」류·「쉽게·간단히·당연히」·「개선 전」·「강사 시연」) + **Ch 25 더함**: 「소비자」·「레이턴시」·「이벤트」·「옵션」·「스냅숏」·「태스크」·「디버그」·「메타데이터」(코드 `metadata`는 「칸 `metadata`」)·「도메인」·「필터링」(→「거르기」)·「명시」·「근삿값」·「워밍업」·「공정」·「단조」·「TTFT」·「total」·「first_event」(본문 말로) + 「한 겹 더」.
- 검사 스크립트 `/tmp/ch25-01/tools/ban25.py`(Ch 24 `ban24.py` + 위 말). 거짓 양성: 「체크포인터」 안 「포인터」·Ch 23 03 「스레드 재개」 문장·prompt 기록 파일 제목 「프롬프트」.

### 허용 문법 범위 (01절 AST 확인 — `/tmp/ch25-01/tools/extra_check.py` 0건)

- 쓰는 것: 칸만 적은 `TypedDict` 상태 형식(**칸 구성이 바뀌면 새 이름** — 01 `DraftState`(칸 `topic`·`draft`)·`SendState`(칸 `topic`·`answer`), 02는 칸이 다르면 예 `AnswerState`) · 노드 함수(힌트 없음, 본문 8줄 이하) · `writer = get_stream_writer()` 다음 줄 `writer({...})`(호출 결과를 바로 호출하지 않음) · 여러 줄 `if`/`else` · `for` · **`for mode, data in 사건 목록:` 풀기**(01 5절에서 한 문장으로 연 모양 — 02는 「01절처럼」) · 목록 `append` · `in` 검사 · `range(len(…))`·자리 `[0]`·`[1]` · 글 `+` · `assert`(우리 코드·라이브러리가 정하는 값에만 — 01은 두 실행의 모드 이름 차례 하나).
- 쓰지 않는 것(01 0건): f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·대입 풀기(`a, b = …`)·별표 풀기·`while`·`try`·세미콜론·`isinstance`·데코레이터·클래스(상태 형식 말고)·`join`(Part 3 0건 — 청크 글은 Ch 6 04처럼 `+`로)·숫자 밑줄·식 안 요금 숫자·`astream`. `len(list(…))` 같은 세 겹 호출은 변수로 풂(01 호출 깊이 최대 2).
- 셀 모양: 준비 셀이 아닌 셀 10줄 이하(01 최대 9) · 함수 본문 8줄 이하(01 최대 5, 주석 뺌) · 셀당 정의 하나 · 첫 줄 주석이 그 셀이 하는 일 · 정의 셀 결과 읽기 「정의 셀이라 출력이 없습니다」 · 여러 줄 출력은 라벨 줄 따로(「라벨 줄 아래」).
- **출력하지 않는 값**: 체크포인트 `config` 아이디·작업 `id`·debug `timestamp`·`Interrupt.id`·모델 응답 아이디·`metadata`의 실행마다 다른 칸(02는 `metadata["langgraph_node"]`처럼 실행마다 같은 칸만).

### 도구 파일 — `notebooks/stream_tools.py` (01은 만들지 않음, 처음 쓰는 절이 만듦)

- 넣을 후보: ① 이 챕터 01이 처음 가르친 함수 둘(뒤 절이 쓰면 01 노트북 셀 글 그대로, AST·문자열 대조) — 주석 머리줄 `# Ch 25 01절에서 배웠습니다 — 01절 노트북 4절의 같은 이름 함수를 옮겼습니다`:
  ```python
  # 그래프를 한 번 실행하며 받은 사건을 차례대로 목록에 모아 내놓습니다
  def collect_events(graph_to_run, graph_input, config, modes):
      events = []
      # stream_mode에 목록을 주면, 사건 하나가 (모드 이름, 자료) 짝으로 나옵니다
      for event in graph_to_run.stream(graph_input, config, stream_mode=modes):
          events.append(event)
      return events
  ```
  ```python
  # 사건 목록에서 한 모드의 사건이 몇 번째(1부터 셈)에 나왔는지 목록으로 내놓습니다
  def positions_of(events, mode):
      places = []
      for index in range(len(events)):
          # 사건 하나는 (모드 이름, 자료) 짝이라, [0]이 모드 이름입니다
          if events[index][0] == mode:
              places.append(index + 1)
      return places
  ```
  (생성기 `author_01.DEF_COLLECT`·`DEF_POSITIONS`에서 첫 줄 주석 뒤를 그대로 가져오면 됨 — `import author_01`은 `python3 -B`로.) ② 앞 챕터 함수: Ch 6 06 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`(Ch 21 `runner_tools.py` 판 본문 — 03·04가 예상 비용을 보이면) · Ch 19 `sum_usage`(에이전트 그래프를 스트리밍할 때만). **노트북이 실제로 쓰는 것만**.
- 만들 때 할 일(Ch 24 01 선례): 머리 독스트링(이 챕터 판, 파일째 가져오지 않은 까닭) · 함수마다 배운 절 주석 · import는 쓰는 것만 · 챕터 `qa/public-files.json`에 한 줄 + `collect_public_files.py`로 Part 목록 다시 모음 · 가져오는 절 준비 셀에 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야…」 · 뒤 절 생성기가 함수를 더하면 앞 절 생성기가 긴 판을 덮어쓰지 않게(Ch 24 마감 A-10) · 실행은 `PYTHONDONTWRITEBYTECODE=1`.

### 색 (01절 Mermaid 4장)

- 넣은 입력 **초록(tool)** · 우리 노드·그래프 **파랑(flow)** · 출력으로 확인한 값 **노랑(measure)** · 라이브러리가 준 것(`graph.stream`·체크포인터)·두 실행 공통 값 **회색(클래스 없음)** · **보라 = 실행한 모델**(01은 0 — 02~은 모델 상자 보라, 실행 안 한 모델은 회색 점선) · **experiment라 빨강 0**(받은 오류는 노랑).
- 모양: 넷 이상 한 줄은 `flowchart TB` · 나란한 칸은 subgraph(칸끼리 `~~~`를 두면 위아래로 쌓임 — 01-3에서 빼서 나란히) · 폭 868 이하(01 최대 798 — 칸 셋이면 칸 제목을 짧게) · 라벨은 `<br>`로 미리 나눔(한 줄 20자 안팎을 넘으면 저절로 꺾임) · 개수는 한글 · 라벨 숫자는 출력에 있는 것만(G7) · 대괄호·따옴표·subgraph 제목 `<br>` 없음 · 노드 id `call`·`end` 없음.

### 비유 계열 — 「대나무 홈통과 물방울」 (01절이 엶)

- 홈통에 한 번 흘린 물 = 그래프 한 번 실행 · 떨어지는 방울 하나 = 스트림 사건 · 구멍과 그 아래 그릇 하나 = 스트림 모드 · 빈 그릇 = 사건이 없는 모드(01 `messages`). **비유와 다른 점**(01 b4): 홈통은 구멍을 막으면 물이 다른 구멍으로 더 나오지만, 그래프는 고르지 않은 모드의 사건을 다른 모드로 넘기지 않음.
- 01-5 삽화: 홈통 하나·구멍 일곱·흰 그릇 일곱, 여섯째 구멍만 물방울 없음·여섯째 그릇 빔(= 4절 표 여섯째 줄 `messages`), 물 높이는 사건 수와 짝짓지 않음.
- 02 후보: 홈통 끝에서 물방울이 하나씩 그릇에 떨어짐(스트림 청크 — 방울 크기가 제각각이라 「방울 = 토큰」으로 읽히지 않게) + 옆에 매단 작은 표시(진행 값 — 풍경·깃발 같은 물건은 소품 금지 목록과 겹치지 않는지 확인) + 그릇이 다 차면 한 번 기우는 대나무(노드 끝 = 갱신 하나). 03 후보(준비 노트 비유 B): 첫 방울이 그릇에 닿는 때 ↔ 그릇이 다 차는 때 — 시계·모래시계 없이 「첫 방울 하나만 담긴 그릇」과 「가득 찬 그릇」을 나란히.
- 금지 소품: 쟁반·서랍·바구니·저울·울타리·발자국·공구판·승강 상자·세탁기·체스판·즉석사진·도미노·구슬·모래시계·회전 레일·도장·식당 전표·컨베이어. 사람·손·화살표·화면·시계·글자·숫자 없음. 스타일 문구 규격 §5-4 그대로, `nano_banana_pro` 16:9 2k `use_unlim:false` count 1, 절당 1장·재생성 1회까지.

### 모델 설정과 요청 (02~)

- `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(nbkit) — 설치판에서 `ChatOpenAI`, `stream_usage True`(기본 주소 — 마지막 사용량 청크, Ch 6 04와 같음)·`streaming False`(준비 노트 §5-4, 가짜 키로 만들기만 확인).
- **노드 안 `model.invoke(...)`도 모드 `messages`를 고르면 스트림 청크를 흘림**(공식 문서 「message events are emitted even when the LLM is run using .invoke」). 설치판 `langchain_core` `BaseChatModel._should_stream`(549~585행)은 스트리밍 콜백이 붙었을 때만 스트리밍 요청 → **`messages`를 고른 실행에서만 스트리밍 요청**, `updates`·`custom`만 고르면 일반 요청(노트북에서 확인하지 않았으면 「설치판 소스로 확인」으로).
- 요청 수는 준비물·진단에 적음(일반 절은 요청 수만으로 강사 확인 대상이 아님). 준비 노트 어림: 02 1~2 · 03 1~2(T1) · 04 3~5, 새 커널 두 번과 노트북 밖 흔들림 확인 다섯 번 포함 챕터 약 50~60번, 0.1달러 아래.

### 03 설계 (결정 8 — 03 몫)

- **T1: 한 실행에 여러 모드를 함께 받아**(예 `["custom", "messages", "updates"]`) 첫 사건·첫 토큰 도착·전체 걸린 시간을 **한 요청 안에서** 잼. 옛 판처럼 모드마다 따로 요청하면 요청 종류부터 다름(`messages`를 고를 때만 스트리밍 요청 — 위).
- 걸린 시간은 03의 주제라 잼(규격 §3 주제 절 예외 — Ch 15 05·Ch 17 04·Ch 18 03 선례). **결론은 결정적 차례**(첫 사건이 첫 스트림 청크보다 먼저 · 글자가 든 첫 스트림 청크가 끝보다 먼저 · 노드 코드 차례 `custom 시작 → messages … → custom 끝 → updates`)에만. 초·토큰·청크 수·비용은 결과 읽기 둘째 단락·본문 표·「확인할 점」에 「교재 출력에서는」·「이번 실행에서는」만, 결론·그림·정리·복습에서 초 비교 금지(규격 §2-7 9번 끝, Ch 18 03).
- **흔들림 확인 먼저**(규격 §2-7 10번 끝): 결론에 쓸 관찰을 노트북 밖 같은 요청 다섯 번으로 확인하고 진단에.
- 예상 비용은 Ch 6 06 `estimate_cost`(도구 파일로) — 「추정 비용」·식 안 요금 숫자 금지.

### 파일 쓰기·시간·비용·실행

- 01: 모델 요청 0 · 비용 0 · 파일 0 · 삽화 2크레딧(job `cde26edf-…`, 거래 17:42:24Z). 걸린 시간은 재지 않음(준비물 「걸린 시간은 재지 않았습니다」).
- 새 커널 두 번: 첫 실행은 사본 `/tmp/ch25-NN/T/`에서 `execute.py`(실습 폴더에 `.failure.json`이 남지 않게) → B 사본 → **그림 전에** 셀별 대조(`/tmp/ch25-01/tools/cmpout.py`) → `run_section.sh` A. 명령: `env -u OPENAI_API_KEY PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch25-streaming UV_NO_SYNC=1 PYTHONPATH=<사본 폴더> uv run --project labs/part6/ch25-streaming --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip --with python-dotenv==1.2.3 python textbook/_notebook/execute.py <사본>.ipynb`. **모델 절은 `env -u OPENAI_API_KEY`를 빼고**(노트북 키 셀은 `find_dotenv(usecwd=True)`로 커널 작업 폴더에서 위로 `.env`를 찾음 — `execute.py`의 기본 작업 폴더는 저장소 맨 위라 루트 `.env`를 찾으므로 `--cwd`를 `/tmp`로 주지 말 것).
- `uv run --project labs/…`를 환경 변수 셋(`UV_CACHE_DIR`·`UV_PROJECT_ENVIRONMENT`·`UV_NO_SYNC`) 없이 부르지 말 것(Ch 24 선례).
- 셀 하나만 다시 실행하면 같은 스레드에 체크포인트가 이어 쌓임(노트북 밖 확인 — 단계 3~6) → 준비물·b7에 「그래프 셀부터 다시 실행」.

### 완료·대기 챕터 문장 (01에서 확인 — `01-diagnosis.md` §10)

- 참: Ch 24 04 b8(01 슬러그·「한 실행에서 … 일곱 방식」) · Ch 23 요약 §15(b3 Ch 23 01 이음) · Ch 26 01~04 b3 · Ch 30 03(「단일 실행과 스트리밍」 — 01 6절 `invoke` == 마지막 values) · Ch 30 04.
- 남은 것: **Ch 30 09 「`stream_mode="messages"`에서 모델 메시지 청크와 실행 메타데이터를 읽었습니다」 → 02가 `metadata`를 읽어야 참** · Ch 30 01 「조각」(Ch 30 몫) · `labs/part6/continuity-guide.md` 11행 「Ch2의 비동기 실행」·「지연 시간」(마감 몫 — 01·02는 동기만).
- 준비 노트 §4-1·§5-2의 「Ch 23 01 노드 둘 4」 표기는 Ch 23 01 노트북(노드 하나 `add`, 실행 한 번에 셋)과 다름 — 01 본문은 「노드 하나짜리 … 셋, 이 그래프는 노드가 하나 더 있어 넷」으로 적음. 뒤 절도 Ch 23 01 수를 인용할 때 셋으로.

## §01 → §02

**02절 주제**: 「토큰과 중간 진행 스트리밍」(**experiment**, 실제 모델 첫 절). 옛 판(`before/notebooks/02-…ipynb`·`before/_src/02-*.html`): 노드 하나 `answer`가 모델 앞뒤로 진행 값 30·100을 보내고 `model.invoke`로 두 문장 답 · `stream_mode=["messages", "updates", "custom"]` 한 실행에서 사건 수(messages 88·내용 있는 것 84·updates 1·custom 2) · 내용 청크를 `"".join(preview)`로 이은 글 == 최종 `answer` · 표시 문구 딕셔너리 셋(사건과 무관) · c2 별표 풀기 키 찾기·c4 20줄·c6 22줄·`chunk, metadata = data`(대입 풀기, `metadata`는 읽지 않음) · `temperature` 없음(G4).

1. **01절이 남긴 자리**: `_src` b8·노트북 정리 끝 「02절에서는 모델을 부르는 노드로, 스트림 청크와 진행 값을 함께 받습니다」 · 01 b7 「모델을 부르는 노드의 `messages` 사건은 02절에서 실제 모델로 봅니다」 · 01 준비물 「실제 모델로 보는 일은 02절 몫」 → **02가 실제 모델로 모드 `messages` 사건(스트림 청크)과 진행 값을 한 실행에서 함께 받아야 참**.
2. **실제 모델 첫 절**: 준비 셀 = 설치(`langchain==1.4.0`·`langchain-openai==1.6.0`·`langgraph==1.2.11`·`python-dotenv==1.2.3`, 체크포인터를 쓰면 `langgraph-checkpoint==4.2.0`) → import → `nbkit.key_and_model_cells("openai:gpt-5.4-mini")`(`temperature=0`·`reasoning_effort="none"` — **G4 옛 2건의 원인**). 키 값 출력 금지. 모델 준비 셀 결과 읽기에 실행일·모델 이름·「실행마다 문장이 달라질 수 있습니다」.
3. **세 모드를 한 실행에서 함께 받기**(`messages`·`updates`·`custom`): 01 4절처럼 목록으로 고르고, 사건마다 모드 이름을 봄. 「구독」 대신 「함께 받는다」. 01이 연 `collect_events`·`positions_of`를 쓰면 **02가 `stream_tools.py`를 만들고 가져옴**(위 「도구 파일」 — 노트북에 다시 적지 않음, 규격 §2-7 3번).
4. **진행 값 쓰기(`get_stream_writer`)**: 01 2절이 뜻(세 문장)·`writer = get_stream_writer()` 모양·「숫자는 우리가 정한 값」을 이미 풂 → 02는 「01절처럼」으로 잇고, 모델 요청 앞뒤(예 30 → 100)에 둬 차례를 보임. 설치판 `config.py` 126행 경고(Python 3.11 미만 비동기) — 교재 3.12라 해당 없음.
5. **흔들리는 값과 결정적 값**: 모드 `messages` 사건 수는 옛 기록마다 **71 → 73 → 88**로 흔들림 → 결론·그림·정리에 넣지 않음(결과 읽기 둘째 단락·표·「확인할 점」에 「교재 출력에서는」). **노트북 밖 같은 요청 다섯 번으로 흔들림 먼저 확인**(규격 §2-7 10번 끝)하고 진단에. 결론은 결정적 값 — 모드 종류 셋 · `updates` 1 · `custom` 2 · 차례(`custom` 시작 → `messages` … → `custom` 끝 → `updates`, 준비 노트 e3 모양) · 이어 붙인 청크 글 == 최종 칸 값.
6. **스트림 청크 잇기**: Ch 6 04처럼 `+`로 더함(`join`은 Part 3 0건 — 쓰지 않음) · 빈 청크·마지막 사용량 청크(`stream_usage True`)가 섞일 수 있음 → 「글자가 든 청크」를 세는 조건을 코드로. 「청크와 토큰은 단위가 다름」은 Ch 6 04 링크 한 문장.
7. **`metadata`를 읽기(Ch 30 09 인계)**: 사건 `(청크, metadata)` 짝에서 `metadata["langgraph_node"]`(실행마다 같음)를 출력해 Ch 30 09 b3 「실행 메타데이터를 읽었습니다」가 참이 되게. 키 목록 전체는 실제 모델에서 `ls_model_name` 등이 더 붙을 수 있어(준비 노트 §5-4 — 실행 안 함) 출력하면 두 번 같은지 대조. 「메타데이터」는 금지어 → 「칸 `metadata`」.
8. **「조각」 23번 고치기**(옛 본문 18·노트북 4·출력 라벨 1 「내용이 있는 조각 수」) → 「스트림 청크」·「글자가 든 스트림 청크」. b4 「토큰 스트리밍 … 메시지 조각」은 「토큰 = 스트림 청크」로 읽히지 않게(Ch 6 04 단위 차이 문장). 제목 「토큰과 중간 진행 스트리밍」의 「토큰」은 제목에 두고 본문에서 풀기(강사 확인).
9. **상태 형식·노드**: 칸이 01과 다르면 새 이름(예 `AnswerState` 칸 `question`·`answer`). 노드 힌트 없음, `writer({...})` 두 줄 모양, 노드 안 `assert`·노트북 전역 목록 `append` 없음(옛 03 결함 — 02도 피함). 옛 c8 「표시 문구」 딕셔너리(사건과 무관)는 빼거나 사건을 읽는 셀로.
10. **b3 고치기**: 「Ch24에서 interrupt와 재개 사건」(세 절 같은 글) → 01 b3처럼 사실대로, `resume` 세 장면은 「01절에서 본 것처럼」 한 줄로. 「Ch23에서 체크포인터와 thread_id」 이음은 02가 체크포인터를 쓸 때만.
11. **그림과 비유**: 그림 번호 `02-1`부터, 설계표 `qa/upgrade/02-figures.md` 먼저. 모델 상자 **보라**(실행한 모델), 받은 오류 노랑, **빨강 0**. 흔들린 값(청크 수·글자 수·토큰)은 라벨에 넣지 않음. 비유는 위 「비유 계열」 02 후보. 옛 `figures/02-흐름.*`(보라 `model` 상자) 그대로.
12. **작업 순서와 챕터 밖 확인**: `before/`에 02 사본 있음 → `qa/upgrade/author_02.py`(01 생성기를 본으로 — `html_text()`·`table_html()`·`mermaid_block()`·`illustration_block()`을 `import author_01`로 가져오면 `python3 -B`) → 첫 실행 전 `upgrade_gates.py … --label wip-02 --section 02`(G1·G2) → 노트북 밖 흔들림 확인 다섯 번 → 사본 T(키 필요 — `--cwd` 없이 기본 작업 폴더로) → B → 셀별 대조(흔들린 셀을 적음) → 그림 → `run_section.sh … 02`(A — 모델 요청이 한 번 더 나감, 결과 읽기는 A 출력으로) → `--no-exec` 게이트 0 → AST·금지어(`/tmp/ch25-01/tools/`) → `pack.py` → `02-diagnosis.md` → 이 파일 `§02 → §03` → 점검표·검증 행 → 보호 파일 해시(`manifest-changes.md`에 이어 적기). 도구 파일을 만들면 공개 목록 두 곳·`collect_public_files.py`. 02는 묶음 실행 검사 대상이 아님(Part 6 `check_bundle_execution.py`는 Ch 25를 돌리지 않음).

## §02 → §03

**03절 주제**: 「TTFT와 total 비교」(**experiment**, 지금 챕터 마지막 본문 절 — 04 실습 절은 마감 몫). 옛 판(`before/notebooks/03-…ipynb`·`before/_src/03-*.html`): 같은 질문을 `updates`·`messages`·`custom` **따로 세 번 요청**하며 `measure()`(본문 16줄·힌트 `-> dict`·조건 표현식)가 첫 사건·「TTFT 근삿값」·끝을 `perf_counter`로 잼 · 노드가 노트북 전역 `call_records`에 `append`·노드 안 `assert` · c8 `next(r for r in rows if …)`(제너레이터 식·`next`·한 글자 `r`)·`.get(…, {}).get(…)` 사슬·`row.update`·숫자 밑줄 `1_000_000`·**요금 0.75·0.075·4.50을 식 안에** · c10 `sum(r["estimated_usd"] for r in rows)`·`round(sum(…))` 두 겹·조건 표현식 · 「추정 비용」·「조각」·「측정」·「근삿값」·「워밍업」·「공정」·「단조」 · 제목·본문 「TTFT」·「total」·「first_event」.

1. **02절이 남긴 자리**: 02 b8·노트북 정리 끝 「03절에서는 (같은 그래프를 한 번 실행하며,) 첫 사건·첫 스트림 청크·끝이 언제 오는지 시간을 잽니다」 · 02 b7 「모드마다 따로 실행하면 요청 종류부터 달라질 수 있습니다. 03절은 모드를 한 실행에서 함께 받아 시간을 잽니다」 → **03은 02 그래프(같은 노드·같은 질문)로 T1을 해야 참**. 02 노트북의 상태 형식 `AnswerState`·시스템 메시지 글·노드 `write_answer`·그래프 셀은 노드가 노트북 전역 `model`·`system_text`를 읽어 도구 파일로 옮기지 않았습니다 → 03이 다시 적으면 「02절과 같은 코드」는 **AST·문자열 대조한 뒤에만**(생성기에서 `author_02.STATE`·`SYSTEM`·`DEF_NODE`·`BUILD`를 그대로 가져오면 됨, `import author_02`는 `sys.dont_write_bytecode = True` 뒤).
2. **T1 한 실행에 여러 모드 함께 받기**(챕터 리드 결정 8): `stream_mode=["messages", "updates", "custom"]` 한 실행에서 사건마다 `time.perf_counter()` 시각을 적어 **첫 사건 시간 · 첫 토큰 도착 시간 · 전체 걸린 시간을 한 요청 안에서**. 모드마다 따로 요청하지 않음 — 02 확인: `messages`를 고르지 않은 실행은 노드 안 `invoke`가 **스트리밍 요청을 보내지 않음**(설치판 langchain-core 1.6.2 `language_models/chat_models.py` 549~585행 `_should_stream` + 노트북 밖 평범한 콜백 새 청크 알림 5/5 0회, `02-probe.md` M2). 01·02의 `collect_events`는 다 모은 뒤에 내놓아 시각을 못 적음 → 시각을 적는 함수는 03이 처음 가르치므로 노트북에 둠(본문 8줄 이하, 힌트·기본값·전역 목록 없이 인자로).
3. **결정적 차례(결론·그림에 쓸 값)** — 02 노트북 밖 다섯 번 + 새 커널 세 번 모두 같았음: 첫 사건 = `custom` `{'stage': 'before_model', 'progress': 30}`(자리 1, **모델 요청 전**) · 모드 `messages` 첫 사건(자리 2)은 **글자가 없는 스트림 청크**(첫 청크) → **글자가 든 첫 스트림 청크는 자리 3** · 마지막 셋 스트림 청크도 글자 없음(끝에서 셋째 끝난 이유·둘째 사용량·마지막 LangChain이 붙인 빈 청크) · 진행 값 100 → `updates`(맨 끝) · 모드 차례 `['custom', 'messages', 'custom', 'updates']`. 그래서 「첫 사건 시각 < 글자가 든 첫 스트림 청크 시각 < 끝 시각」은 차례로 정해지는 값(정의상 참, Ch 15 05 「첫 토큰이 끝보다 먼저 왔는가: True」와 같은 모양) — 결론은 이 차례에만.
4. **걸린 시간은 03 주제라 잰다**(규격 §3 주제 절 예외 — Ch 15 05·Ch 17 04·Ch 18 03 선례). 초·토큰·청크 수·비용은 결과 읽기 둘째 단락·본문 표·「확인할 점」에 「교재 출력에서는」·「이번 실행에서는」만, **결론·그림·정리·복습에서 초 비교 금지**(규격 §2-7 9번 끝, Ch 18 03). 첫 사건 시간은 모델 요청 전 진행 값이라 아주 짧게 나올 것 — 「몇 배 빠르다」 류 비교를 쓰지 않음.
5. **흔들림 확인 먼저**(규격 §2-7 10번 끝): 결론에 쓸 관찰(위 차례와, 쓰고 싶다면 「첫 토큰 도착 시간이 전체 걸린 시간보다 작다」 같은 비율)을 노트북 밖 같은 요청 **다섯 번**으로 확인하고 `03-probe.md` §0에 판단 규칙을 먼저 적을 것. 02 probe 스크립트(`probe/probe02.py`)에 시각 적기만 더하면 됨. 02 노트북 밖 값: messages 사건 34~50개·답 글 흔들림(두 줄 답도 나옴)·입력 토큰 47 다섯 번 같음.
6. **용어**: Ch 15 05 **「첫 토큰 도착 시간」**(글자가 든 첫 스트림 청크까지 — Ch 15 05 정의 그대로, 「글자가 든」을 코드로 `chunk.text != ""`) · 끝까지는 **「전체 걸린 시간」**(Ch 15 05 「전체 지연」은 인용할 때만, 「지연」은 금지어) · 새 말 **「첫 사건 시간」**(모드와 관계없이 처음 받은 사건까지 — 뜻 → 일상 예 → 코드 세 문장) · 02가 정한 「스트림 청크」·「칸 `metadata`」·「모드 차례」 이어 씀 · 「TTFT」·「total」·「first_event」·「근삿값」·「측정」(→ 재기)·「워밍업」·「공정」·「단조」·「추정 비용」(→ 예상 비용) 금지. **제목 「TTFT와 total 비교」**는 영문 둘 — 슬러그 `03-TTFT와-total-비교`는 Part 6 목차만 링크(02 b7·b8도 링크하지만 파일 이름이 바뀌면 02 `_src` 링크 두 곳 `L_03`을 함께 고쳐야 함), 제목 글만 바꿀지·슬러그째 바꿀지 강사 확인(01은 제목 「stream mode」를 두고 본문에서 풂).
7. **옛 판 코드 고치기**: `measure` 16줄 → 셀·함수 나누기(본문 8줄 이하) · 제너레이터 식·`next`·`sum`·조건 표현식·한 글자 `r`·`.get` 사슬·`update`·`1_000_000`·노드 안 `assert`·전역 `call_records` 빼기 · 힌트 빼기 · `[Path.cwd(), *…parents]` → `nbkit.key_and_model_cells` · 걸린 시간은 `perf_counter`를 변수에 담아 뺄셈(식 안 계산 없이, `round`는 Ch 15 05처럼).
8. **예상 비용을 보이면** Ch 6 06 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`를 Ch 21 `runner_tools.py` 판 본문 그대로 `stream_tools.py` **끝에 덧붙여** 옮기고(머리줄 `# Ch 6 06절에서 배웠습니다 — …`, `import` 없이 됨 — 다만 Ch 21 판 본문은 `usage.get("input_token_details", {})`·`details.get("cache_read", 0)` 두 줄을 씀: 노트북 `.get`은 금지지만 도구 파일 안은 Ch 15·20·21 선례, `/tmp/ch25-02/tools/extra_check.py`는 도구 파일의 `.get`도 세므로 허용 표시로 따로 적을 것), 요금은 이름 있는 변수(요금표 2026-09-17 mini 0.75·0.075·4.50)로, 「예상 비용」(청구 금액 아님). 02 생성기는 도구 파일이 **02 판으로 시작하는 긴 판이면 덮어쓰지 않음**(`startswith` 검사) — 03 생성기도 같은 가드(없음·02 판·03 판일 때만 씀). 02의 `mode_order`를 03이 쓰면 02 노트북 4절 셀 글 그대로 도구 파일에 옮김(첫 가르친 절 02). 옮기면 챕터 `qa/public-files.json`은 이미 줄이 있어 그대로, zip은 마감.
9. **준비 셀**: 설치 넷(02 판 — `langchain==1.4.0`·`langchain-openai==1.6.0`·`langgraph==1.2.11`·`python-dotenv==1.2.3`) · 가져오기(+ `import time`) · 도구 파일 가져오기 줄(알파벳 순)과 고정 세 문장 + 커널 폴더 한 문장(02 판 결과 읽기 그대로) · `nbkit.key_and_model_cells`(02 판 결과 읽기처럼 실행일·「실행마다 답 문장이 달라질 수 있습니다」·「요청은 아직 보내지 않습니다」).
10. **값 바꿔 보기 후보**: 02 8절이 이미 「messages를 뺀 실행」(사건 3·답은 끝에만)을 보였으므로 되풀이하지 말고, 03은 예) 모드 목록 차례만 바꾸기(`["custom", "updates", "messages"]` — 사건 차례는 목록 차례와 관계없이 노드 코드가 정함, 요청 1) 또는 값 바꿔 보기 없이 T1 한 번 + 새 커널 두 번. 요청은 노트북 한 번에 1~2번, 새 커널 세 번(T·B·A)과 흔들림 확인 다섯 번 포함 약 10~15번.
11. **그림과 비유**: 그림 번호 `03-1`부터, 설계표 `qa/upgrade/03-figures.md` 먼저. 초 값은 라벨에 넣지 않음(차례만 — 「첫 사건 → 글자가 든 첫 스트림 청크 → 끝」). 모델 상자 보라(실행한 모델), 빨강 0. 비유 계열 「대나무 홈통과 물방울」 03 후보(준비 노트): 첫 방울 하나만 담긴 그릇 ↔ 가득 찬 그릇을 나란히(시계·모래시계 없이). 02 삽화는 홈통 끝 물방울·기우는 대나무 통·종 둘 — 03은 종·기우는 통을 되풀이하지 않는 편이 좋음.
12. **뒤 챕터 문장**(고치지 않음, 03이 참이 되게): Part 6 소개·`practice-start.md` 「Ch 25는 … 시간을 측정합니다」(03이 재면 참, 말 「측정」은 마감 몫) · `labs/part6/continuity-guide.md` 11행 「지연 시간」(03이 재면 뜻은 참) · Ch 30 04~06 본문의 시간 문장은 02에서 대조하지 않았음(03이 `grep`으로 확인). 03 b8은 지금 「Ch30 … FastAPI SSE」 — 04 실습 절이 붙으면(마감) 04로 고칠 자리. 작업 순서는 02와 같음: 흔들림 확인 → `author_03.py`(첫 실행 전 `--label wip-03 --section 03`) → T·B 사본(키 필요, `--cwd` 없이) → 셀별 대조 → 그림 → `run_section.sh … 03`(A, 결과 읽기 둘째 단락은 `[[READ_…]]` → `mdpatch.py`) → `--no-exec` 게이트 0 → AST·금지어(`/tmp/ch25-02/tools/`) → `pack.py` → 진단 → 이 파일 `§03 → 마감` → 점검표·검증 행 → 보호 파일 해시.

## §03 → 실습(04)

**04절 주제**: 챕터 끝 실습 절 신설(규격 §7-2 · PLAYBOOK §3) — 슬러그 후보 **`04-Streaming-실습`**(선례 `04-Human-in-the-Loop-실습`·`07-Persistence-실습`·`09-Middleware-실습`·`07-create-agent-실습`·`05-ToolNode-실습` — 챕터 제목 「Streaming」 그대로. 챕터 제목을 한국어로 바꾸면 `04-스트리밍-실습`, 강사 확인), 제목 「Streaming 실습: {주제}」, `chapter.json`에 `format: experiment`로 추가, meta 「실습 30분 · 새 용어 0」, **챕터 시수(3·5h)에 더하지 않음**(`hours` 그대로). **03이 본문 마지막 절**이었습니다. 01~03의 이름·API만 쓰고 새 문법·새 API·새 말 0.

1. **03절이 남긴 자리(04가 생겨야 참)**: `_src` b8 「다음 학습과 이어지는 지점 — 04절 실습에서는 이 챕터에서 배운 것을 작은 흐름 하나에 모아 실행합니다.」 · 노트북 정리 끝 같은 문장(**링크 없음** — 04 파일이 아직 없음, Ch 24 03 선례). 04가 「이 챕터에서 배운 것(스트림 모드 고르기·진행 값·스트림 청크와 칸 `metadata`·모드 차례·사건마다 시각 적기·세 시간·예상 비용 가운데 2~3개)을 한 흐름에」 모으면 그대로 참. 04가 생기면 03 b8에 `<a href="04-…-실습.html">`만 넣음(`author_03.py`의 `_src` 문장 → `python3 -B author_03.py --src-only` → `run_section.sh … 03 --no-exec` — **03은 다시 실행하지 않음**, 노트북 끝 줄은 링크 없는 선례대로 두어 `mdpatch.py` 불필요). **Ch 30으로 잇는 문장은 04 b8 몫**(옛 03 b8 「Ch30에서는 messages와 custom 사건을 FastAPI SSE로 …」를 03에서 뺌 — Ch 30 `agent_service/app.py` 110~111·134~136행 `astream(…, stream_mode="custom")`·`async for message, metadata in runtime.astream(…, stream_mode="messages")`로 참, 말 「이벤트」 없이). 03 b7이 남긴 「실행하지 않음」: 모드 `messages`가 없는 실행에 `three_times`(첫 글자 자리 `None`에서 1을 빼다 오류) · 여러 번 재어 가운데 값·백분위수 · 네트워크 몫과 서버 몫 가르기 · 스트리밍하지 않은 실행과 걸린 시간 견주기(마감 주: 이 항목은 기록 당시 03 b7에 없었고, 마감에서 검토 B-1로 03 b7·b10·노트북 7절에 더함) · `astream`·`version="v2"` — 04가 새로 풀면 새 설계가 되므로 **다루지 않는 쪽**을 권합니다.

2. **이어 쓸 이름 — 도구 파일 `labs/part6/ch25-streaming/notebooks/stream_tools.py`(03 판 `a468d87878fcce0f5351c3da504aaab2bbadf19bcfec40a7246531be053515ea`, 62줄, `import` 0, 함수 넷, 묶음 목록 두 곳에 이미 한 줄 — 경로라 그대로)**:

   | 함수(인자) | 배운 곳 | 가져온 절 | 하는 일 |
   |---|---|---|---|
   | `collect_events(graph_to_run, graph_input, config, modes)` | Ch 25 01 노트북 4절 | 02 | 그래프를 한 번 실행하며 받은 사건을 목록에 모아 **다 끝난 뒤** 내놓음(시각 없음) |
   | `positions_of(events, mode)` | Ch 25 01 노트북 4절 | 02·03 | 한 모드 사건이 몇 번째(1부터)에 나왔는지 목록 |
   | `mode_order(events)` | **Ch 25 02 노트북 4절** | 03 | 같은 모드가 이어지면 한 번만 적은 「모드 차례」 목록 |
   | `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` | Ch 6 06(Ch 21 `runner_tools.py` 판 본문 글자 그대로) | 03 | 사용량 딕셔너리와 세 요금(100만 토큰당 달러)으로 예상 비용(달러), `usage`가 `None`이면 `None` — `.get` 두 줄(도구 파일 안 선례, 노트북 0) |

   - 대조: 01 함수 둘 = `author_01.DEF_COLLECT`·`DEF_POSITIONS`(`author_02.check_same_as_01()`) · `mode_order` = 02 노트북 셀 글·AST(`author_03.check_tools()`) · `estimate_cost` = Ch 21 `runner_tools.py`(`f4113158…`) 글·AST. 도구 파일 = `author_02.TOOLS` + `author_03.NEW_TOOL_PARTS`(생성기 `author_03.TOOLS`). 02 생성기는 02 판으로 시작하는 긴 판을, 03 생성기는 03 판으로 시작하는 더 긴 판을 덮어쓰지 않음. **04가 함수를 더하면** 04 생성기가 `author_03.TOOLS` + 새 함수로 쓰고 `startswith(author_03.TOOLS)` 대조, 없음·03 판·04 판일 때만 씀(Ch 24 마감 A-10).
   - **노트북에만 있는 함수(03 처음 가르침)** — 04가 쓰면 `# Ch 25 03절에서 배웠습니다 — 03절 노트북 N절의 같은 이름 함수를 옮겼습니다`로 도구 파일에 **글자 그대로** 옮기고 생성기 상수와 대조: `collect_timed_events(graph_to_run, graph_input, config, modes)`(`author_03.DEF_TIMED`, 3절 — 딕셔너리 키 `start`·`events`·`times`·`end`, **모듈 `time`을 씀 → 도구 파일에 `import time` 한 줄이 생기므로 `author_02.check_same_as_01()`·`author_03.check_tools()`의 「도구 파일은 아무것도 가져오지 않습니다」 대조 줄을 04 판에 맞게 고칠 것**, 머리 독스트링은 02 판 글이라 바꾸지 않음) · `first_text_place(events)`(`DEF_FIRST_TEXT`, 5절 — 자리 또는 `None`) · `three_times(run_record)`(`DEF_THREE`, 7절 — 한국어 키 셋 딕셔너리, **안에서 `first_text_place`를 부르므로 둘을 함께 옮김**). 노드·상태 형식(`write_answer`·`AnswerState`)과 시스템 메시지 글은 노트북 전역 `model`·`system_text`를 읽어 도구 파일에 두지 않음 → 04 노트북에 새로 적음(칸이 다르면 새 이름).
   - 04는 처음 가져오는 절이 아니어도 고정 세 문장(「앞에서 배운 함수는 `stream_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.」)과 「커널이 `notebooks/` 폴더에서 시작해야 …」·「교재 출력을 만든 실행 도구는 …」 문장을 준비 셀 결과 읽기에(02·03 선례), 이름은 알파벳 순.

3. **허용 문법 범위(01~03 끝 — 04는 이 안에서만)**: 칸만 적은 `TypedDict` 상태 형식(칸 구성이 바뀌면 새 이름 — `DraftState`·`SendState`·`AnswerState` 선례) · 노드 함수(힌트 없음) · `writer = get_stream_writer()` 다음 줄 `writer({...})` · `StateGraph`·`add_node`·`add_edge`·`START`·`END`·`compile()`(01만 `InMemorySaver`) · `graph.stream(입력, 설정, stream_mode=목록)`·`for mode, data in 사건 목록:`·자리 `[0]`·`[1]` · `list(get_args(StreamMode))`(01)·`graph.stream_mode`(01)·`invoke`(01) · 모델 `init_chat_model`(표준 셀)·노드 안 `model.invoke([("system", …), ("user", …)])`·`response.text` · 스트림 청크 `.text`·`.usage_metadata`·`+`로 합치기(02)·칸 `metadata["langgraph_node"]` 등(02) · **03이 더한 것**: `import time`·`time.perf_counter()`·`round(뒤 − 앞, 3)` · 딕셔너리 키에 든 목록에 `append` · 함수 안 `for`+`return`(찾으면 바로 내놓기)과 끝 `return None` · 조건 `and`·`!= ""`·`is not None`·비교 `<` · 음수 자리 `[-1]`(6절 한 문장) · 한국어 키 딕셔너리·딕셔너리 `==`·`for name in 딕셔너리:` · 요금 셀 `pricing_date = "2026-09-17"`·`mini_prices = {"ordinary_input": 0.75, "cached_input": 0.075, "output": 4.50}`(Ch 6 06 모양 — 식 안 요금 숫자 0) · 목록 `append`·`in`·`range(len(…))`·글 `+` · `assert`(우리 코드·라이브러리가 정하는 값에만 — 03은 키 셀 하나, 02는 모드 차례 하나). **01~03 모두 안 쓴 것**: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·`break`·`while`·`try`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·대입 풀기·별표 풀기·세미콜론·`isinstance`·데코레이터·클래스(상태 형식 말고)·`join`·숫자 밑줄·`astream`. 호출 깊이 최대 2(03), 부른 내장 이름 `len`·`list`·`print`·`range`·`round`·`type`. **출력하지 않는 값**: 체크포인트·작업·`Interrupt` 아이디·debug 시각·모델 응답 아이디·칸 `metadata`의 `checkpoint_ns`·`langgraph_checkpoint_ns` 값.
   - 셀 모양: 03 코드 셀 **24**(준비 셋), 준비 셀이 아닌 셀 최대 **10줄**(8절 사용량 셀 — 상한, 04는 9줄 이하 권함), 함수 본문 최대 7줄, 셀당 정의 하나, 검사 문장 349. 실습 절 선례 19~28셀(Ch 22 09 19 · Ch 21 07 24 · Ch 24 04 28).

4. **결정적 값과 흔들린 값(04가 결론·그림에 쓸 수 있는 것)**:
   - **결정적**(새 커널 세 번 + 노트북 밖 확인): 01 전부(한 실행 23사건·모드별 수·자리 등, 모델 없음) · 02·03 공통 그래프(노드 `write_answer`, 진행 값 30 → 모델 → 100): 모드 차례 `['custom', 'messages', 'custom', 'updates']`(**목록 차례를 바꿔도 같음**, 03 9절) · `updates | 1`·`custom | 2` · 첫 사건 custom `{'stage': 'before_model', 'progress': 30}` · 모드 `messages` 첫 사건 자리 2·글자 0 · 글자가 든 첫 스트림 청크 자리 3 · 마지막 사건 updates · `langgraph_node` `write_answer` · 이어 붙인 글 == 답 글 `True` · 사건마다 시각이 하나씩 `True` · 「첫 사건 시각 < 글자가 든 첫 스트림 청크 시각 < 끝 시각」 두 비교 `True` · 사용량 청크 1 · 입력 토큰 47 · 캐시 입력 0 · messages 뺀 실행 사건 3·`['custom', 'updates']`(02).
   - **흔들린 값 — 결론·그림·정리·복습에 쓰지 않음**(규격 §2-7 9번 끝, 결과 읽기 둘째 단락·본문 표·「확인할 점」에 「이번 실행에서는」·「교재 출력에서는」만): 초 전부(03 새 커널 첫 토큰 도착 0.519·1.463·1.51 · 전체 0.74·1.72·1.758 · 밖 0.498~1.568·0.719~1.773, 첫 사건 0.003~0.006) · 두 구간 · 비율(밖 열 번 모두 첫 토큰 도착 시간이 전체의 절반을 넘음 — b7 한 문장만) · 사건 수·스트림 청크 수(02·03 밖 34~53) · 출력 토큰 40~50 · 예상 비용 0.000215~0.00026달러 · 답 글. **두 실행의 초를 견주어 빠르기를 말하지 않음**(따로 보낸 요청).

5. **요청 수 선례와 04**: 01 **0** · 02 노트북 **2**(밖 10 + 새 커널 T·B·A 6 = 16) · 03 노트북 **2**(밖 10 + 6 = 16) → 챕터 지금 32번, 예상 비용 합 약 0.008달러(청구 금액 아님). **04 실습 절은 규격 §7-2 「모델 호출 3~5번」** — 예) 실행 1(세 모드 한 번) + 실행 2(값 하나 바꿈) + 필요하면 견주기 한 번. 3번보다 적으면 까닭을 진단에 적고 강사 확인(Ch 24 04 선례는 모델 없는 챕터라 0). 결론에 쓸 관찰은 **노트북 밖 5번 먼저**(규격 §2-7 10번 끝, `probe/probe03.py`를 본으로), 새 커널 두 번(T·B 사본) 뒤 그림. 요청당 약 0.0002~0.0003달러.

6. **04 설계 권고(규격 §7-2)**: 실행 1(기본) → 실행 2(값 하나만 바꿈), 각각 예상 → 실행 → 출력 확인 → 비교, 본문 「앞에서 배운 내용」에 「절 | 배운 것 | 실습에서 쓰는 곳」 표, 그림 조립도·실행 1 순서·실행 1·2 비교 + 삽화 1. 「앞 절 기능 2~3개」 후보: 진행 값 여러 개(01·02 `get_stream_writer`) + 세 모드 한 실행과 모드 차례(02 `mode_order`·`positions_of`) + 사건마다 시각·세 시간·예상 비용(03). 소재 후보: ① 02·03 배송 문의를 잇되 새 문의 하나(요청 전 진행 값 「문의 확인」·요청 뒤 「답 정리」 등) ② 준비 노트 §12 — Ch 21~24 도서관 소재(자료실 안내 답을 스트리밍하며 「검색 중 → 답 쓰는 중 → 끝」 진행 값). 실행 2 후보(값 하나만): **노드의 모델 요청 전 진행 값을 빼기** — 첫 사건이 글자 없는 스트림 청크(모드 `messages`)로 바뀌고 첫 사건 시간에 모델 기다림이 들어가는지(차례는 결정적일 것 — 밖 5번 먼저 확인) · 모드 목록에서 `custom`만 빼기(진행 값 사건 0, 첫 사건이 스트림 청크) — 02 8절(`messages` 뺌)·03 9절(목록 차례)은 되풀이하지 않음. 파일은 쓰지 않는 쪽(01~03 파일 0), 체크포인터가 필요 없으면 없이.

7. **아직 가르치지 않은 것(04가 설명 없이 전제하면 안 되는 것)**: 비동기 `astream`·`async for`(Ch 2 12가 `async for`를 가르치지 않음 — Ch 30 04 몫) · 인자 `version="v2"`·`subgraphs=True`·`print_mode`·`stream_events` · 하위 그래프·여러 노드 그래프의 스트리밍(노드 이름으로 거르기 — 02는 실행 안 함) · 에이전트 그래프(`create_agent`) 스트리밍·도구 호출 스트림 청크·`ToolMessage` 사건 · 체크포인터와 모델을 함께 쓰는 스트리밍(01만 `InMemorySaver`, 모델 없음) · 멈춤 표시(`interrupt`)를 모델 그래프에서 스트리밍(01 9절은 모델 없는 한 장면) · 여러 번 재어 가운데 값·백분위수(Ch 15 06은 배웠으나 Ch 25에서 안 씀) · 네트워크 몫·서버 몫 가르기 · 스트리밍하지 않은 실행과 걸린 시간 견주기(「스트리밍이 더 빠르다」류 문장 금지) · `time.get_clock_info`(03 b7 노트북 밖만) · FastAPI·SSE·재연결(Ch 30) · Windows·macOS 출력. 말: 「구독」·「이벤트」·「조각」·「지연」·「측정」·「추정」·「TTFT」·「total」(03 제목 풀이 밖) 쓰지 않음.

8. **비유 계열 「대나무 홈통과 물방울」과 삽화 소품**: 홈통에 한 번 흘린 물 = 한 실행 · 떨어지는 방울 = 스트림 사건 · 구멍과 그릇 = 스트림 모드 · 홈통 끝 크기가 제각각인 물방울 = 스트림 청크 · 종 = 진행 값 · 한 번 기우는 통 = 갱신 하나 · 물을 흘리기 시작한 때부터 종이 울린 때 / 첫 방울이 닿은 때 / 그릇이 가득 찬 때 = 첫 사건 시간 / 첫 토큰 도착 시간 / 전체 걸린 시간. **쓴 소품**: 01-5 홈통 하나·구멍 일곱·흰 그릇 일곱(여섯째 빔, 1차 job `cde26edf-…`) · 02-5 홈통 하나(Y자 받침 둘)·놋쇠 종 둘·크기가 다른 물방울 일곱·기우는 대나무 통 하나(받침돌, 1차 job `d0559a2f-…`) · **03-5 짧은 홈통 끝 둘(나무 기둥 하나씩, 서로 마주 봄)·흰 그릇 둘(왼쪽 바닥에 물방울 하나 · 오른쪽 가장자리까지 가득)**(1차 job `f3a1cbad-825c-4153-a304-0a33fb213357`, 2크레딧, 거래 18:43:32Z). 04 후보: 앞 세 장의 소품(구멍 일곱·종 둘·기우는 통·마주 보는 홈통 둘)을 되풀이하지 않는 **새 배치 하나** — 예) 홈통 두 줄 나란히(실행 1·실행 2)에 한 줄만 다른 점 하나(값 하나 바꿈)처럼 물건 수를 작게, `figures/*.prompt.md` `grep`으로 겹침 확인. 규칙: 금지 소품(쟁반·서랍·바구니·저울·울타리·발자국·공구판·승강 상자·세탁기·체스판·즉석사진·도미노·구슬·모래시계·회전 레일·도장·식당 전표·컨베이어), 사람·손·동물·화살표·화면·시계·글자·숫자 없음, 물건은 크게, 개수·자리·상태를 이름으로, 스타일 첫 문장 규격 §5-4 그대로, `nano_banana_pro` 16:9 2k `use_unlim:false` count 1, 절당 1장·재생성 1회까지, 크레딧은 거래 기록으로 그 절 몫. 모델이 물방울 수·배치를 틀리기 쉬움 — 그림 읽기에 「개수는 짝짓지 않음」.

9. **실행 방법(02·03과 같음)**: 흔들림 확인 → `author_04.py`(첫머리 `sys.dont_write_bytecode = True`, `import author_03`은 `python3 -B`) → 첫 실행 전 `upgrade_gates.py … --label wip-04 --section 04`(G1·G2) → 사본 T `/tmp/ch25-04/T/`(노트북 + 도구 파일, **키 필요 — `env -u OPENAI_API_KEY` 없이, `--cwd` 주지 않음**(키 셀 `find_dotenv(usecwd=True)`가 저장소 맨 위 작업 폴더에서 루트 `.env`를 찾음)): `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch25-streaming UV_NO_SYNC=1 PYTHONPATH=/tmp/ch25-04/T uv run --project labs/part6/ch25-streaming --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip --with python-dotenv==1.2.3 python textbook/_notebook/execute.py …` → B 사본(그림 전) → `cmpout.py`(`/tmp/ch25-03/tools/`) → 그림 → `PYTHONDONTWRITEBYTECODE=1 bash run_section.sh … 04`(A, 교재 출력) → 둘째 단락 `[[…]]` → `mdpatch.py` → `--no-exec` 게이트 0 → AST·금지어(`/tmp/ch25-03/tools/` — `extra_check.py` 03 판은 도구 파일 `estimate_cost`의 `.get` 둘을 허용 표시) → `pack.py`. **실습 폴더 안에서 먼저 실패하면 `.failure.json`이 남고 지울 수 없음** → 첫 실행은 `/tmp` 사본으로. `uv run --project labs/…`는 환경 변수 셋 없이 부르지 말 것.

10. **셀 모양과 문장 선례(03에서 걸린 것)**: 정의 셀 결과 읽기 첫 단락에 숫자 든 백틱 두지 않음(출력 없음) · 흔들리는 값은 둘째 단락 `[[…]]`로 두었다가 A 뒤 `mdpatch.py`(값 뒤 조사 — `0.642`와 — 는 채운 뒤 확인) · b5 「확인할 점」 교재 출력 문장이 70자를 넘기 쉬움(03 첫 검사에서 하나) · 게이트 금지어 「돌려」·「재 보」(「재 보면」 금지) · 「캐시」는 「캐시 입력」으로(ban25 거짓 양성) · 출력에서 `4.50`이 `4.5`로 찍힘 — 첫 단락 백틱에 `4.50` 금지 · 「글자 그대로」·「같은 코드」는 생성기 `assert`로 대조한 것만 · 「TTFT」·「total」 풀이는 03 b2·노트북 1절 두 곳뿐.

11. **그림·색 선례**: 03 Mermaid 4장(폭 259·344·440·595) — 한 실행의 사건 차례 = 상자 여섯 한 줄(03-1, 「여기까지 …」 끝줄) · 구조 = 노드·모델에서 함수로 라벨 화살표 둘(03-2) · 두 줄이 함수로 모임(03-3) · 나란한 두 실행 = 회색 공통 → subgraph 둘(칸 안 파란 고른 목록 → 노란 결과) → 맨 아래 회색 `~~~`(03-4, 한 상자에 목록과 결과를 함께 넣으면 저절로 꺾여 둘로 나눔). 04는 experiment라 **빨강 0**(받아 출력한 오류도 노랑), **보라 = 실행한 모델**, 넣은 입력·요금표 초록 · 우리 노드·함수·시각을 적은 자리·고른 설정 파랑 · 출력 노랑 · 라이브러리 메서드·공통 값 회색, **라벨에 초 값 넣지 않음**, 라벨 숫자는 출력에 있는 것만·개수는 한글, 원본 폭 868 이하, `<br>`로 미리 나눔(한 줄 라틴 18자 안팎을 넘으면 꺾임).

12. **마감 몫(01~03 진단의 남은 것 전부 — 04 뒤 챕터 마감 담당)**:
    - **`chapter.json`**: 04 절 추가 · `objectives`(「stream mode」·「측정」 등 옛 말) 절 본문 말과 대조 → `_build.py` · `textbook/part6/_build_index.py` 23행(시수 3·5 그대로, 설명 「토큰과 진행 이벤트를 구분하고 첫 응답과 전체 처리 시간을 측정합니다」 — 「이벤트」·「측정」 대조) · `textbook/_notebook/build_index.py` 54행(절 수 3 — 선례대로 전체 마감에 둘지) · `qa/check_scope.py` `EXPECTED`·`SECTION_COUNTS`(기록만).
    - **실습 폴더 README 다시 쓰기**: 지금 「01은 API 키 불필요 · 02·03은 .env 키 · **03은 세 번의 별도 호출 비용 합산 · 추정 비용**」 — **03 부분이 거짓**(이제 한 요청 안에서 세 시간, 노트북 두 요청, 「예상 비용」) · 노트북 넷 · `uv sync --locked` → `.venv` → `notebooks/`에서 열기 · 도구 파일 단락(`stream_tools.py` 함수 넷, import 0) · 절별 모델 요청(01 0 · 02 2 · 03 2 · 04 N).
    - **공개 목록·묶음**: 챕터 `qa/public-files.json`·`textbook/part6/public-files.json`에 04 노트북·HTML 줄(`collect_public_files.py` — 도구 파일 줄은 02가 이미 올림) · **zip 다시 만들기**(`part6-practice.zip`·`llm-practice.zip` 안은 옛 01~03 노트북·도구 파일 없음) → `check_delivery.py`(`llm-practice.zip` Stale 예상) · 묶음을 풀어 04 노트북 가져오기 셀 확인. 묶음 실행 검사(`check_bundle_execution.py`)는 Ch 25를 안 봄(계약 없음 — 넣을지 강사 확인).
    - **옛 생성기 이동**: Ch 25 `figures/_gen_figures.py`(`cb02fe4e59df…`, `raise SystemExit`) `mv -n` → `qa/upgrade/before/generators/blocked/` · 공용 `textbook/part6/_generate_ch25_ch26.py`(`0767052613d9…`, Ch 25 쪽 건너뜀)는 **Ch 26 01절이 `raise SystemExit`, Ch 26 마감에 `mv -n`**.
    - **옛 그림 9개** 삭제 승인 목록(`figures/0N-흐름.{svg,excalidraw,caption.md}`, N=1~3 — 본문 참조 0, 사본 `before/figures/`, 캡션에 「측정」·「조각」, `final-artifact-hashes.json`이 해시를 적은 기록 파일). 챕터 공개 목록에는 옛 SVG 줄이 원래 없음. `visual.cjs`(1280px·390px).
    - **02 노트북 5절 코드 주석의 줄인 「청크」 둘**(02 진단 §1 — 다음 재실행 때 `author_02.EMPTY` 주석을 「스트림 청크」로; 재실행하면 02 출력·그림 숫자 다시 대조).
    - **생성기 대조 줄**: 04가 도구 파일에 `import`를 넣으면 `author_02.check_same_as_01()`·`author_03.check_tools()`의 「도구 파일은 아무것도 가져오지 않습니다」 줄 · 04가 03 함수를 옮기면 `author_03.check_tools()`의 함수 이름 목록 대조(`== [collect_events, positions_of, mode_order, estimate_cost]`)는 `author_03.TOOLS`(상수)만 보므로 그대로 참.
    - `labs/part6/continuity-guide.md` 11행(「Ch2의 비동기 실행」 부분 참 · 「진행 이벤트와 지연 시간」 뜻은 참, 말 「이벤트」·「지연」) · `labs/part7/continuity-guide.md` 7행(「Ch2의 비동기 함수와 Ch25의 스트리밍」 — Ch 25는 동기만) · Part 6 `_src/index.html` 8행 「시간을 측정합니다」(참, 말 「측정」).
    - `qa/research.md`·`qa/verification.md`·`집필점검표.md`·`qa/authoring-checklist.md`·`research.md` 위쪽 옛 기록에 「개선 전 판」 표시 · 챕터 요약 `qa/upgrade/chapter-summary.md`(새 말 meta 3·3·2 = 8 — 스트림 모드·스트림 사건·진행 값 / 스트림 청크·칸 `metadata`·모드 차례 / 첫 사건 시간·전체 걸린 시간, 이어 쓴 말 첫 토큰 도착 시간 · 도구 파일 해시 · 요청 수 · `gates-after.json`).
    - **제목의 영어(강사 확인)**: 챕터 「Streaming」 · 01 「stream mode」 · 02 「토큰」(말은 한국어, 뜻 풀이) · 03 「TTFT」·「total」 — 본문 첫 자리에서 한 번씩 풂. 슬러그는 01 고정(Ch 24 04 링크), 02·03은 Part 6 목차·앞 절 링크만.
    - **강사 확인 대상 모음**: 01 진단 §12(제목·코드 줄 41→155·`get_args`·비유 계열·「걸린 시간은 재지 않았습니다」) · 02 진단 §12(제목 「토큰」·61→138·칸 `metadata`·b7 노트북 밖 값·예상 비용 문장만·주석 「청크」·삽화 받침돌 잘림) · 03 진단 §12(제목 TTFT·total·76→133·새 말 둘·값 바꿔 보기 목록 차례·`estimate_cost` `.get`·`[-1]`·`and` 첫 사용·b7 비율·시계 문장·10줄 셀·삽화 배치) + 04 요청 수.
    - **뒤 챕터 인계**(고치지 않음, 챕터 요약에): Ch 26 01~04 b3 참 · Ch 30 01 「조각」(뜻 참, 말 Ch 30 몫)·03(01로 참)·04·05 참·09(02로 참) · **Ch 30 04 b2 「스트리밍은 … 첫 응답 지연을 줄이지만」**(Ch 25는 스트리밍하지 않은 실행과 걸린 시간을 견주지 않음 — 근거 아님, Ch 30 몫) · Part 6 소개·`practice-start.md` 참 · continuity-guide 두 곳 · Ch 24 04 b8(01 슬러그·「한 실행」) 참. TTFT·첫 토큰을 Ch 25에 기대어 말하는 뒤 챕터 문장 0(03 `grep`).
    - **삭제 승인 대상**: 실습 폴더 `.venv`(macOS 판 173MB) · `.cache/vm/venv-ch25-streaming`(238MB, 04까지 씀) · `qa/upgrade/gates-wip-*.json` · `$ROOT/.cache/ch25-0N-view/` · 기기 `/tmp/ch25-prep`·`/tmp/ch25-01`~`/tmp/ch25-03`(`/tmp/ch25-03/`: `T/`·`B/`·`A-copy.ipynb`·`probe/`·`illu/`·`tools/`·`stream_tools.py`·`reps-A.json`·`reps-B.json`).

## 실습 → 챕터 검토

**04절 `04-Streaming-실습`을 새로 만들었습니다**(2026-09-25). 제목은 「Streaming 실습: 요청 전 진행 값을 켜고 끄며 자료실 문의 답 흘려 보이기」이고 `chapter.json`에 `format: experiment`로 더했습니다. 기록은 `qa/upgrade/04-diagnosis.md`, 흔들림 확인은 `qa/upgrade/04-probe.md`, 그림 설계표는 `qa/upgrade/04-figures.md`, 검토 묶음은 `qa/upgrade/review-pack/04-Streaming-실습.md`입니다. 위 「챕터 공통」의 준비 셀·용어·색·비유 약속은 그대로 삽니다. 슬러그는 위 「§03 → 실습(04)」 후보 그대로.

### 1. 이 절이 한 것

- **주제**: 자료실 문의 창 흉내 — 문의 글 「빌린 책의 반납 날짜를 늘리려면 어떻게 하나요?」(Ch 24 04 대출 연장 소재)·시스템 메시지 글 「자료실 이용 문의에 답하는 안내 도우미입니다. 두 문장의 한국어로 답하세요.」(02 글에서 「배송」만 바꿈), 둘 다 첫 요청 전에 `04-probe.md` §0에 적음(출력 출처 줄·b7). 상태 형식 `InquiryState`(칸 `question`·`answer`·`show_notice` — 셋 다 `str`, 칸 `show_notice`는 글 `"yes"`/`"no"`) · 노드 `answer_inquiry`(02 `write_answer`와 같은 차례에 `if state["show_notice"] == "yes":` 한 줄 — 진행 값 30은 그때만, 100은 늘) · 그래프 `START → answer_inquiry → END`, 체크포인터 없음 · 기록 장치 `screen_log(events)`(진행 값 `progress` 목록 + 스트림 청크 글 이어 붙이기)·`print_report(run_record)`(모드 차례·첫 사건 모드·글자가 든 첫 스트림 청크 자리·화면 진행 값·화면 글 == 답 글).
- **붙인 앞 절 기능 셋 — 모두 흐름 안에서 쓰임**(세 실행 출력으로 셈): **01** 모드 목록 `["messages", "updates", "custom"]`·(모드 이름, 자료) 짝 풀기·`positions_of`(7절 진행 값 자리 `True`, 8절 진행 값 수 `2·2·1`) · **02** 진행 값(`[30, 100]`/`[100]`)·스트림 청크 이어 붙이기(`화면 글과 답 글이 같은가: True` 세 번)·`mode_order` · **03** `collect_timed_events`(세 실행)·`first_text_place`(3·3·2)·`three_times`(8절 표).
- 실행 1(`"yes"`) → **같은 설정 다시**(대조 실행 — 사건 수·초는 달라도 모드 차례·자리는 같음을 먼저 보임) → 실행 2(**칸 `show_notice` 하나만 `"no"`**, 인계 6항 첫 후보). 02 8절·03 9절 비교는 되풀이하지 않음, b2 「새로 볼 것」은 첫 사건과 화면이 처음 바뀌는 자리까지만.
- **뺀 것**(b3 둘째 단락): 01 일곱 모드 전부·체크포인터·멈춤 표시 · 02 칸 `metadata`·`messages` 뺀 실행 · 03 목록 차례·예상 비용·두 구간.
- **새 문법·새 API·새 말 0**(01~03 노트북과 AST 대조 — 새 노드 종류·연산자·내장 이름·속성·키워드 0, 새 가져오기는 도구 파일로 옮긴 03 함수 셋, `bool`·`round`는 노트북에서 안 씀). `assert`는 키 셀 하나뿐. 걸린 시간은 03 함수로 재지만 결론에 쓰지 않음.
- 코드 셀 **20**(준비 셋), 준비 셀이 아닌 셀 최대 9줄, 함수 본문 최대 8줄(`print_report`), 코드 줄 103, 검사 문장 317(처음 313으로 잘못 적음 — 마감에서 바로잡음, 검토 B-9), 게이트 G1~G7 **0**(챕터 전체 4/4 PASS). meta 「실습 30분 · 새 용어 0」, **챕터 시수에 더하지 않음**. Mermaid 3 + 삽화 1(재생성 1회). 모델 요청 노트북 한 번 **3번**.

### 2. 실행으로 확인한 값 (새 커널 T 19:15:45 · A 19:16:02 · B 19:16:16 UTC, 결정적 셀 15/20 세 번 같음 + 노트북 밖 흔들림 확인 열 번 같음 — 챕터 요약이 인용할 수 있는 값)

- 준비: `도구 파일에서 가져온 함수: collect_timed_events, first_text_place, mode_order, positions_of, three_times` · `문의 글: 빌린 책의 반납 날짜를 늘리려면 어떻게 하나요?` · `등록한 노드: ['answer_inquiry']`.
- 실행 1·같은 설정 다시: `사건마다 시각이 하나씩인가: True` · `모드 차례: ['custom', 'messages', 'custom', 'updates']` · `첫 사건의 모드 이름: custom` · `글자가 든 첫 스트림 청크의 자리: 3` · `화면에 띄운 진행 값: [30, 100]` · `화면 글과 답 글이 같은가: True` · `첫 사건의 자료: {'stage': 'before_model', 'progress': 30}` · `두 실행의 모드 차례가 같은가: True`.
- 실행 2: `모드 차례: ['messages', 'custom', 'updates']` · `첫 사건의 모드 이름: messages` · `글자가 든 첫 스트림 청크의 자리: 2` · `화면에 띄운 진행 값: [100]` · `화면 글과 답 글이 같은가: True` · `첫 사건 스트림 청크의 글자 수: 0` · `진행 값의 자리가 마지막 사건 바로 앞인가: True`.
- 8절 표: `실행 1 | custom | 3 | 2` · `같은 설정 다시 | custom | 3 | 2` · `실행 2 | messages | 2 | 1`.
- **흔들린 값(결론·그림·정리·복습에 안 씀)**: 교재 출력(A) 사건 수 62·60·60, 세 시간 `실행 1 | 62 | 0.003 | 0.666 | 1.055` · `같은 설정 다시 | 60 | 0.003 | 0.699 | 1.131` · `실행 2 | 60 | 0.537 | 0.568 | 0.96`, 답 글 두 줄 · 노트북 밖 사건 수 61~68·출력 토큰 59~66·입력 토큰 48(열 번 같음 — 노트북은 출력하지 않음)·실행 2 설정 첫 사건 0.561~0.826초(실행 1 설정 0.003~0.004 — b7 한 문장만)·첫 사건과 첫 글자 사이 0.002~43.5밀리초(셋째 자리 초로 같게 찍힐 수 있음 — T 실행 2 0.884/0.884, b7 반올림 문장).
- `code_sha256` **`0c0ecd220c78…`**(T·A·B 같음) · `outputs_sha256` A `40744b4c3929…`(T `ece2021debde…`·B `dd0447bb3d6a…`) · 노트북 파일 `d00014642d82…`.

### 3. 함께 고친 파일 (검토자가 볼 곳)

**챕터 안**
- `chapter.json` — 04절 추가(`28171e3214bf` → `da13aa03f20c`). **`hours`·`objectives` 그대로**(objectives는 마감 몫).
- **도구 파일** `labs/part6/ch25-streaming/notebooks/stream_tools.py` 03 판 `a468d878…` → **04 판 `3a734aeb87244a7d05574acd9f1d269a7ab2ddd1a944d018e60baa82c4708ff5`**(103줄, 함수 일곱 — `collect_events`·`positions_of`·`mode_order`·`estimate_cost`·`collect_timed_events`·`first_text_place`·`three_times`, import `time` 하나를 머리 설명 바로 뒤에). 머리 설명(02 판 글 — 01 함수 둘만 말함)은 바꾸지 않음.
- **생성기 대조 줄**: `author_02.py`(`1f1fe37be326` → `76afb50a0eb7`)에 `strip_later_imports()` 더하고 도구 파일 쓰기 가드가 그 함수를 거침 · `author_03.py`(`9ac6183ce92f` → `747df9a376ba`) 가드 같은 방식 + 「import 없음」 줄 메시지를 「02절 판 …」·「03절 판 …」으로(상수만 보는 줄이라 참) + b8 04 링크. 02·03 생성기는 04 판이 있으면 도구 파일을 덮어쓰지 않고 건너뜀.
- **03절 마지막 문장**: b8 글은 그대로, **`_src` b8에 04 링크만**(`--src-only`, `_src/03` `3ca2fa1c` → `91d9f2cf`) → `run_section.sh … 03 --no-exec`(03 게이트 0). 노트북 끝 줄은 링크 없는 선례대로 두어 `mdpatch.py` 안 씀. **03 노트북 `bf1462828c47…` · `code_sha256` `ffe254e0d3c2…` · `outputs_sha256` `9a11da7a456d…` · `executed_at` 18:45:20Z 그대로.** 03 HTML `546ba916` → `466b95df`, 챕터 `index.html` `6c94f5ec` → `725777d6`. 01·02 HTML 바이트 같음. 03 검토 묶음 다시 만듦.
- 챕터 `qa/public-files.json` — **04 HTML·04 노트북 두 줄**(`bbfdade3` → `0b890e75`).
- 새 파일: 노트북 04 · `_src/04`(`000855a425c0…`) · 빌드 `04-Streaming-실습.html`(`f69e61292b5f…`, `{{`·`[[` 0건) · `figures/04-1`~`04-3`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`) · `figures/04-4-마디를-이은-두-홈통과-깃발.{png,prompt.md,caption.md}` · `qa/upgrade/author_04.py`(`fac48ade21b6…`) · `04-probe.md`·`04-figures.md`·`04-diagnosis.md` · `probe/probe04.py`·`probe/probe-04-{N1,N2}.jsonl` · `gates-wip-04-04.json`·`gates-wip-04.json`·`gates-wip-ch25-after04.json` · `review-pack/04-Streaming-실습.md`.
- `집필점검표.md` 품질 개선 표 04 행 · `qa/verification.md` 품질 개선 검증 표 04 행 · `qa/upgrade/manifest-changes.md` 「04절 뒤」 · 이 파일 맨 위 한 줄과 이 절.

**챕터 밖**
- `labs/part6/ch25-streaming/README.md` — 맨 아래 **04절 한 단락만**(`bd86ef71819f`). 옛 첫 단락(「03은 세 번의 별도 호출 … 추정 비용」 — 거짓)은 마감 몫.
- `textbook/part6/public-files.json` — `collect_public_files.py` → **04 노트북 한 줄**(`b12a3921` → `8140df88`). `prerequisite-files.json` 바이트 같음.
- `textbook/part6/index.html`(`778b240be0d6`) · `textbook/downloads/part6-practice.zip`(`acf14b060f58`) · `textbook/part6/qa/integration-results.json`(`8b9ecb322c8b`) — `python3 textbook/part6/_build_index.py` 한 번(**`Part 6: 52 verified sections; 100 bundled files`**). 목차에 Ch 25 「4절」·04 링크, **zip 안 Ch 25 항목 8개(노트북 넷·도구 파일 04 판·README·잠금 둘)가 디스크와 같음**, `__pycache__` 0. `_build_index.py`는 고치지 않음(23행 설명은 마감 몫).
- `textbook/_notebook/checks/notebook-contracts-part6-ch25-streaming.json` — `verify.py --chapter`가 다시 씀(`feefa318eca4`).
- **고치지 않음**: 01·02·03 노트북 · 01·02 `_src`·HTML · `pyproject.toml`·`uv.lock` · 공용 옛 생성기 `_generate_ch25_ch26.py`·`figures/_gen_figures.py` · 옛 그림 · Ch 21·23·24·26·30 파일 · `textbook/index.html` · `llm-practice.zip`·`bundle-execution.json`·`delivery-results.json` · 공용 도구·규격·과정 요약·`build_index.py`.

### 4. 검사 결과

- `run_section.sh … 04 --no-exec`: 게이트 G1~G7 **0**, `verify.py --chapter` **`PASS 4 sections / 97 code cells (max 12 lines)`**, 빌드 HTML `{{`·`[[` 0건, SVG 셋·삽화 하나. 챕터 전체 `gates-wip-ch25-after04.json` **4/4 PASS**.
- AST(`/tmp/ch25-04/tools/astdiff.py` — 01~03 노트북 대조)·`extra_check.py`(03 판)·`shape.py`·`ban25.py` 모두 0건(허용 표시·거짓 양성 말고). 생성기 `author_04.cells()` 44셀 = 노트북 셀 글, `src_html()` = `_src`, `TOOLS` = 디스크 도구 파일, `author_03.src_html()` = `_src/03`.
- `check_delivery.py` — **117행 `llm-practice.zip`의 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`에서 멈춤**(알려진 일, 전체 마감 몫). 그 앞(`part6-practice.zip` 신선도 등)은 지나감. `delivery-results.json` 안 바뀜(`3cc2d143…`).
- `check_bundle_execution.py`(Ch 25 계약 없음)·`check_scope.py`·`check_course_continuity.py`·`visual.cjs`·옛 검사 넷은 돌리지 않음(마감 몫).
- 보호 파일 147개: **125개 같음·22개 바뀜·없어진 파일 0** = 03절 끝까지의 16개(이 절이 값을 다시 바꾼 것 일곱: 묶음 목록 둘·`verification.md`·`집필점검표.md`·notebook-contracts·03 `_src`·03 HTML) + **이 절이 지시대로 새로 바꾼 여섯**(`chapter.json`·실습 폴더 `README.md`·챕터 `index.html`·`part6/index.html`·`part6-practice.zip`·`integration-results.json`) — `manifest-changes.md` 「04절 뒤」.
- 삽화 `04-4` 1차 job `8af32746-…` 탈락 → **2차 job `61323491-89d7-4fc5-97b4-755d9b4d9e2c` 채택**, 4크레딧(거래 19:19:51Z·19:20:59Z), 저장 PNG ↔ 채택 job 픽셀 차이 0.

### 5. 챕터 마감 담당이 이어서 할 것 (「§03 → 실습(04)」 12번 마감 몫 전부 + 01~03 진단의 마감 몫 + 04가 더한 것)

1. **`chapter.json` `objectives`** 셋을 절 본문 말과 대조 — 「일곱 가지 stream mode가 내보내는 사건」(→ 스트림 모드·스트림 사건) · 「사용자 정의 진행 상황」(→ 진행 값) · 「첫 사건·첫 토큰까지의 시간·전체 완료 시간을 따로 측정」(→ 첫 사건 시간·첫 토큰 도착 시간·전체 걸린 시간, 「측정」 → 재기) + **04 실습 줄을 넣을지**(예: 「실습에서 모드 목록·진행 값·스트림 청크 이어 붙이기·시각 적기를 문의 하나에 붙이고, 요청 전 진행 값 하나를 꺼 첫 사건과 화면이 처음 바뀌는 자리를 견줄 수 있습니다」) → `_build.py`. `textbook/part6/_build_index.py` 23행(시수 3·5 그대로, 설명 「토큰과 진행 이벤트를 구분하고 첫 응답과 전체 처리 시간을 측정합니다」 — 「이벤트」·「측정」 대조, 실습 절 문구를 더할지 — Ch 21·23·24 선례) · `textbook/_notebook/build_index.py` 54행(절 수 3 — 선례대로 전체 마감에 둘지) · `qa/check_scope.py` `EXPECTED`·`SECTION_COUNTS`(기록만, 실습 절로 멈출 수 있음).
2. **실습 폴더 README 다시 쓰기 전체**(지금은 옛 첫 단락 + 04 한 단락): 「03은 세 번의 별도 호출 … 추정 비용」은 **거짓**(03은 한 요청 안에서 세 시간, 노트북 두 요청, 「예상 비용」) · 노트북 넷 · `uv sync --locked` → `.venv` → `notebooks/`에서 열기 · 도구 파일 단락(`stream_tools.py` **함수 일곱·import `time`**, 가져오는 절 02·03·04) · 절별 모델 요청(01 0 · 02 2 · 03 2 · 04 3) · API 키(02~04). 그다음 `_build_index.py` 한 번 더(zip·목차).
3. **묶음**: `part6-practice.zip`은 04가 다시 만들어 Ch 25 항목이 디스크와 같음 — README·objectives를 고친 뒤 다시 만들고 `check_delivery.py`(`llm-practice.zip` Stale 예상) · 묶음을 풀어 04 노트북 가져오기 셀(`stream_tools` 함수 다섯)을 확인 · 묶음 실행 검사(`check_bundle_execution.py`)는 Ch 25를 안 봄(계약 없음 — 넣을지 강사 확인, 02~04는 키 필요).
4. **도구 파일 머리 설명**: 02 판 글 그대로라 「01절 함수 둘은 글자 그대로 옮겼습니다」까지만 말함 — 함수 일곱의 출처(01 둘·02 하나·Ch 6 06 하나·03 셋)와 `import time`을 한 줄씩 적을지(Ch 24 검토 A 선례). **고치면 `author_02.TOOLS_HEAD`가 바뀌어 02·03·04 판 대조 사슬이 모두 바뀜** → `author_02.TOOLS`·`author_03.TOOLS`·`author_04.TOOLS`·`strip_later_imports`·세 생성기의 `check_*` 줄을 함께 맞추고, 01~04 노트북은 가져오는 이름만 쓰므로 다시 실행할 필요 없음(함수 글이 같으면).
5. **옛 생성기 이동**: Ch 25 `figures/_gen_figures.py`(`cb02fe4e59df…`, `raise SystemExit`) `mv -n` → `qa/upgrade/before/generators/blocked/` · 공용 `textbook/part6/_generate_ch25_ch26.py`(`0767052613d9…`, Ch 25 쪽 건너뜀)는 **Ch 26 01절이 `raise SystemExit`, Ch 26 마감에 `mv -n`**.
6. **옛 그림 9개** 삭제 승인 목록(`figures/0N-흐름.{svg,excalidraw,caption.md}`, N=1~3 — 본문 참조 0, 사본 `before/figures/`, 캡션에 「측정」·「조각」, `final-artifact-hashes.json`이 해시를 적은 기록 파일) · `visual.cjs`(1280px·390px, HTML 넷).
7. **02 노트북 5절 코드 주석의 줄인 「청크」 둘**(02 진단 §1 — 다음 재실행 때 `author_02.EMPTY` 주석을 「스트림 청크」로; 재실행하면 02 출력·그림 숫자 다시 대조).
8. `labs/part6/continuity-guide.md` 11행(「Ch2의 비동기 실행」 부분 참 · 「진행 이벤트와 지연 시간」 뜻은 참, 말 「이벤트」·「지연」) · `labs/part7/continuity-guide.md` 7행(Ch 25는 동기만) · Part 6 `_src/index.html` 8행 「시간을 측정합니다」(참, 말 「측정」).
9. **기록**: `qa/research.md`·`qa/verification.md`·`집필점검표.md`·`qa/authoring-checklist.md`·`research.md` 위쪽 옛 기록에 「개선 전 판」 표시 · **`chapter-summary.md`**(PLAYBOOK §6): 새 말 meta 3·3·2·**0** = 8(스트림 모드·스트림 사건·진행 값 / 스트림 청크·칸 `metadata`·모드 차례 / 첫 사건 시간·전체 걸린 시간, 이어 쓴 말 첫 토큰 도착 시간) · 도구 파일 04 판 `3a734aeb…`·함수 일곱·import `time` · 요청 수 01 0 · 02 16 · 03 16 · **04 19**(= 51, 노트북 한 번 0·2·2·3) · **실습 30분은 챕터 시수에 더하지 않음** · 04 주제와 결과(위 2번) · 비유 「대나무 홈통과 물방울」 네 장(01 구멍 일곱·그릇 일곱 · 02 종 둘·기우는 통 · 03 첫 방울 그릇·가득 찬 그릇 · **04 마디 셋을 이은 두 홈통·위에만 깃발**) · 코드 줄 155·138·133·103(합 529)·도구 파일 53 · `gates-after.json`(`upgrade_gates.py … --label after`) · 한국어 감사 3단·그림 판독 별도 세션(01~04).
10. **제목의 영어(강사 확인)**: 챕터 「Streaming」 · 01 「stream mode」 · 02 「토큰」 · 03 「TTFT」·「total」 · **04 「Streaming 실습」**(슬러그 01 고정 — Ch 24 04 링크, 02·03은 Part 6 목차·앞 절 링크, 04는 03 b8·Part 6 목차).
11. **강사 확인 대상 모음**: 01 진단 §12 · 02 진단 §12 · 03 진단 §12 + **04 진단 §11**(슬러그·긴 제목 · 요청 3번 중 하나가 「같은 설정 다시」 · 칸 `show_notice` 글 `"yes"`/`"no"` · 코드 줄 103·셀 20·기록 장치 함수 둘 · b7 노트북 밖 값·반올림 문장 · 삽화 재생성 1회·두 홈통 모양 차이).
12. **뒤 챕터 인계**(고치지 않음, 챕터 요약에): Ch 26 01~04 b3 「Ch25에서는 실행 사건을 스트리밍했습니다」 참 · **04 b8** 「Ch 26 01절에서는 전문 에이전트를 도구로 감싸 일을 맡기는 위임 구조」(Ch 26 01 `_src` b2와 맞춤)·「Ch 30 04절은 모드 `custom`의 사건을 `astream`으로 받아 이어 붙이고, 09절은 모드 `messages`의 스트림 청크를 서버 응답으로」(Ch 30 04·09 `_src`·`agent_service/app.py` 확인) · Ch 30 01 「조각」(Ch 30 몫)·03(01로 참)·04·05 참·09(02로 참) · **Ch 30 04 b2 「스트리밍은 … 첫 응답 지연을 줄이지만」**(Ch 25는 스트리밍하지 않은 실행과 견주지 않음 — 근거 아님, Ch 30 몫) · Part 6 소개·`practice-start.md` 참 · continuity-guide 두 곳 · Ch 24 04 b8 참.
13. **삭제 승인 대상**: 실습 폴더 `.venv`(macOS 판 173MB) · `.cache/vm/venv-ch25-streaming`(238MB) · `qa/upgrade/gates-wip-*.json` · `$ROOT/.cache/ch25-0N-view/`(N=1~4) · 기기 `/tmp/ch25-prep`·`/tmp/ch25-01`~`/tmp/ch25-04` · 각 절 진단 「지우지 않은 것」(04는 진단 §12).

### 6. Ch 26 작업자가 전제하면 안 되는 것

- **Ch 25는 동기 메서드 `stream`만 썼습니다(01~04).** `astream`·`async for`·`stream_events`·인자 `version="v2"`·`subgraphs=True`·`print_mode`는 0건입니다(01 b7·03 b7·04 b7 「실행하지 않았습니다」). 비동기 스트리밍은 Ch 30 04가 처음 가르칩니다.
- **스트리밍한 그래프는 모두 작습니다** — 01 노드 둘(모델 없음, `InMemorySaver`) · 02~04 모델 노드 하나(체크포인터 없음). **여러 노드·하위 그래프·에이전트 그래프(`create_agent`)의 스트리밍, 노드 이름(칸 `metadata["langgraph_node"]`)으로 거르기, 도구 호출 스트림 청크·`ToolMessage` 사건, 서브에이전트의 스트림을 바깥으로 흘리기는 0건**입니다. 체크포인터와 모델을 함께 쓴 스트리밍도 0건입니다.
- **걸린 시간은 03·04가 `time.perf_counter`로 조건마다 한 번씩만 쟀습니다.** 여러 번 재어 가운데 값·백분위수·빠르기 비교·스트리밍하지 않은 실행과 견주기는 없습니다(「스트리밍이 더 빠르다」의 근거로 쓰지 말 것). 결론은 사건 차례·자리뿐입니다.
- **예상 비용**은 03이 도구 파일 `estimate_cost`(Ch 6 06 — Ch 21 판 글자 그대로)로 요청 한 번만 셌습니다. Ch 25 도구 파일은 Ch 25 실습 폴더에만 있고, Ch 26 실습 폴더와 다릅니다(파일째 가져오지 말 것 — Ch 26은 자기 판).
- **모델 요청 수**는 노드 안 `model.invoke` 한 번 = 요청 한 번인 우리 그래프 값입니다(01 0 · 02 2 · 03 2 · 04 3 / 노트북 밖·새 커널 포함 51). Ch 26의 「호출 수」 비교에 이 수를 그대로 쓰지 않습니다.
- **말**: 01~03 말(스트림 모드·스트림 사건·진행 값·스트림 청크·칸 `metadata`·모드 차례·첫 사건 시간·전체 걸린 시간)과 Ch 15 05 「첫 토큰 도착 시간」만 씀, 04는 새 말 0. 「이벤트」·「조각」·「지연」·「측정」·「추정」·「구독」은 제목·슬러그 밖 0, 「TTFT」·「total」은 제목·슬러그와 03 b2·03 노트북 1절의 제목 풀이 밖 0(위 「챕터 공통」 금지어 — 범위는 마감에서 바로잡음, 검토 B-9). 챕터 `index.html` 학습 목표의 「stream mode」·「측정」은 마감에서 `objectives`를 고쳐 뺐음. Ch 26 01~04 b3 「Ch25에서는 실행 사건을 스트리밍했습니다」는 참입니다.
- 04 소재(자료실 문의 창, Ch 24 04 대출 연장 이어 받음)를 Ch 26이 이어 쓴다는 약속은 없습니다. 공용 옛 생성기 `textbook/part6/_generate_ch25_ch26.py`는 Ch 25 쪽만 건너뛰고 **Ch 26 쪽 동작은 그대로**입니다 — Ch 26 01절이 첫머리를 막고(`raise SystemExit`), Ch 26 마감에 옮깁니다. 04는 이 파일을 건드리지 않았습니다.

## 검토 반영과 챕터 마감 (2026-09-25)

별도 세션 검토 둘(`review-round1-A.md` 01~02·공통 중 2 · 하 15, `review-round1-B.md` 03~04·마감 몫 중 4 · 하 8)을 반영하고 챕터를 마감했습니다. 전체 기록은 `chapter-summary.md`, 절별 마감 기록은 각 `NN-diagnosis.md`·`NN-figures.md` 끝 「마감 반영」입니다. **[중] 6을 모두, [하] 23 가운데 21을 반영**했습니다. 반영하지 않은 둘(A-14·B-12 — 같은 항목, 도구 파일 머리 설명)은 도구 파일 해시 `3a734aeb…` 고정 결정 때문이고, 코드 셀을 고쳐야 맞는 둘(A-1 01 셀 31 주석 · A-12 02 셀 36 주석 「청크」 둘)은 코드를 그대로 두고 결과 읽기·설명 셀에 한 문장씩 둔 뒤 다음 재실행 몫으로 적었습니다. 뒤 챕터 몫(Ch 30 04 b2 · Ch 6 04 개명 영향)은 그 챕터 파일을 고치지 않고 요약 §15에 적었습니다. **다시 실행한 노트북은 없습니다**(네 노트북 코드·출력 해시 전후 같음, 모델 요청 0 · 삽화 생성 0). 이 파일 위 기록 가운데 마감으로 사실이 바뀐 자리만 적습니다.

1. **위 「§03 → 실습(04)」 12번·「실습 → 챕터 검토」 §5의 마감 목록은 끝났습니다**: 실습 폴더 README 전체(`d29f86b3…` — 절별 모델 요청 01 0 · 02 2 · 03 2 · 04 3, 키는 `.env`에서만, 도구 파일 함수 일곱·`time`) · `chapter.json` `objectives` 넷(`hours` 그대로) · `textbook/part6/_build_index.py` ch25 설명 줄 · `textbook/_notebook/build_index.py` Ch 25 설명(절 수 3은 과정 전체가 실습 절을 빼고 세는 약속이라 그대로)과 `textbook/index.html`(Ch 25 행만) · `labs/part6/continuity-guide.md` Ch 25 줄(「Ch2의 비동기 실행」·「이벤트」·「지연」 뺌) · 옛 기록 넷(`qa/research.md`·`research.md`·`qa/ch25-technical-review.md`·`qa/authoring-checklist.md`) 머리에 「개선 전 판」 표시 · `qa/verification.md`·`집필점검표.md` 머리 표시와 끝 「마감」 절 · `figures/_gen_figures.py` → `qa/upgrade/before/generators/blocked/`(`mv -n`, `cb02fe4e…` 같음) · `part6-practice.zip` **`71683e44…`**(Ch 25 8파일 디스크와 같음 — 마지막에 한 번) · `check_bundle_execution.py` **PASS**(`bundle-execution.json` `baaaf52f…` — Ch 25는 검사 목록에 없음) · `gates-after.json` 4/4 · `verify.py --chapter` PASS 4/97 · `visual.cjs` 10행 PASS · `chapter-summary.md`. 옛 그림 아홉·`gates-wip-*.json` 아홉·캐시·임시 폴더·`llm-practice.zip`은 `textbook/qa/upgrade-final-checklist.md` §2-13.
2. **공용 옛 생성기 `textbook/part6/_generate_ch25_ch26.py`는 옮기지 않았습니다**(Ch 26이 아직 씀, `0767052613d9…` 그대로). 위 「챕터 공통」 결정 6대로 **Ch 26 01절이 첫머리를 막고 Ch 26 마감에 `mv -n`**.
3. **03 정의 기준점**(검토 B-2): 위 「챕터 공통」 용어 표·「§02 → §03」 6항의 세 시간 정의는 이제 **「메서드 `stream`을 부른 때부터」**입니다(제목 풀이는 「그래프 실행을 시작한 때」). Ch 15 05는 모델의 `stream()`을 부르기 직전부터 쟀고, 03은 그보다 조금 앞에서부터 잰다는 문장이 03 b4 용어 표·노트북 5절에 있습니다.
4. **칸 `metadata`**(검토 A-3): 이름은 그대로, 02 b4 용어 표·노트북 6절에 「이름에 칸이 붙었지만 그래프 상태의 칸이 아니라, 사건 짝의 둘째 값입니다」(강사 확인).
5. **그림**: 다시 렌더 `01-1`(「칸 값과 진행 값에서」, 노트북 첨부 갈아 끼움) · `02-3`(키 열둘·`langgraph_step 1` 뺌) · `03-3`(입력 토큰 47·캐시 입력 0·사용량 청크 수 뺌) — `02-probe.md`·`03-probe.md` §0 규칙을 뒤에서 넓히지 않음. 위 「§03 → 실습(04)」 4항 「결정적」 목록의 「사용량 청크 1 · 입력 토큰 47 · 캐시 입력 0」은 §0에서 **결과 읽기 첫 단락까지만** 쓸 값이라 그림·결론에는 쓰지 않습니다. 삽화는 다시 만들지 않고 02-5(종 둘 짝짓기)·04-4(관 모양 차이) 글을 PNG를 보고 고쳤습니다.
6. **03 한계**(검토 B-1): 03 b7·b10·노트북 7절에 「스트리밍하지 않은 실행과 걸린 시간을 견주지 않았다」 — 위 「§03 → 실습(04)」 1항과 「실습 → 챕터 검토」 12항의 「스트리밍하지 않은 실행과 견주지 않음」은 이제 03 학생 글에도 있습니다.
7. **기록 바로잡음**(검토 B-9): 위 「실습 → 챕터 검토」 1항 검사 문장 313 → **317** · 04 진단 §3 `"yes"`/`"no"` 근거 → `probe04.py`·`author_04.py` 결정 2 · §6 「「TTFT」·「total」은 제목·슬러그 밖 0」 → 제목·슬러그와 03 b2·노트북 1절 풀이 밖 0.
8. **Ch 26 작업자에게**: 위 「실습 → 챕터 검토」 §6과 요약 §13·§14 — 특히 **Ch 25는 노드 하나짜리 작은 그래프를 동기 `stream`으로만 받았고, 에이전트·여러 노드 그래프 스트리밍·`ToolMessage` 사건·초 비교가 없습니다**(초 비교는 결론이 아님). Ch 26 01~04 b3 「Ch25에서는 실행 사건을 스트리밍했습니다」는 참입니다.

- 전체 마감 2026-09-30: 청크 표기 — 02 b3·b4 두 문장을 Ch 6 04 새 표기(「스트림 청크」)에 맞추고 「사용량 청크」 다섯 곳 → 「사용량이 든 스트림 청크」. 노트북 해시 같음(요약 끝 줄).
