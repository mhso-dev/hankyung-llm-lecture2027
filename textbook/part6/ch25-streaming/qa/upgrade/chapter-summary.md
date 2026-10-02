# Ch 25 Streaming — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part6/ch25-streaming` 01~03절(품질 개선) + **04절 챕터 끝 실습 절 신설**(`04-Streaming-실습`), 노트북 `labs/part6/ch25-streaming/notebooks/01~04-*.ipynb`, 도구 파일 `notebooks/stream_tools.py`. 뒤 챕터가 읽는 계약 파일(산출 파일)은 없습니다.
- 기간: 2026-09-25(준비 조사 · 01~03절 개선 · 04절 신설 · 검토 1차 반영 · 챕터 마감). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 세 절 합계 **124**(G1 7 · G2 9 · G4 2 · G5 15 · G6 82 · G7 9 — 01 40 · 02 34 · 03 50, `gates-before.json`) → 마감 뒤 **4/4 PASS, G1~G7 모두 0**(`gates-after.json`, 검사 문장 395·344·358·317 = **1,414**).
- 코드 셀 28·25·24·20 = **97**(`verify.py --chapter` → `PASS 4 sections / 97 code cells (max 12 lines)` — 12줄은 준비 셀). 코드 줄(`count_code.py`, 주석·빈 줄 뺌) 41·61·76 → **155·138·133 + 04 새 절 103 = 529**, 도구 파일 53줄. Mermaid **15장**(01 넷 · 02 넷 · 03 넷 · 04 셋), 삽화 **4장**(절마다 하나, Higgsfield 10크레딧 — 04만 재생성 1회, 마감 0), 복습 문제는 HTML에만.
- **모델 요청**: 01은 모델 없음(0번, API 키 셀·`dotenv` 없음), 02~04는 실제 `gpt-5.4-mini`(`temperature=0`·`reasoning_effort="none"`). 노트북 한 번 0·2·2·3번, 작업 전체(노트북 밖 흔들림 확인 + 새 커널 세 번) **0·16·16·19 = 51번**, 마감 **0번**. 예상 비용 합 약 **0.014달러**(요금표 2026-09-17로 어림, 청구 금액 아님 — 02 약 0.004 · 03 약 0.004 · 04 약 0.006).
- 화면 검사 `visual.cjs`: HTML **다섯 개**(네 절 + `index.html`) × 1280px·390px = **10행 PASS**.
- **마감에서 다시 실행한 노트북: 없음.** 네 노트북 모두 `code_sha256`·`outputs_sha256`·`executed_at`이 전후 같습니다(마크다운·그림 첨부만 — §17).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 24 요약 → **이 문서** → `handoff.md`(절 사이 세부, 끝 「검토 반영과 챕터 마감 (2026-09-25)」) → 절별 `NN-diagnosis.md`(끝 「마감 반영」)·`NN-probe.md`(02~04 노트북 밖 흔들림 확인) → 검토 `review-round1-A.md`(01~02·공통)·`review-round1-B.md`(03~04) → 준비 조사 `chapter-lead-notes.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 문법·API | 새로 만든 함수 (도구 파일에 둔 것은 굵게) | 새 용어 |
|---|---|---|---|
| 01 일곱 가지 stream mode (experiment, 모델 없음) | 메서드 **`graph.stream(입력, 설정, stream_mode=…)`** — 제너레이터를 내놓고 `for`가 꺼낼 때 실행이 시작됨(꺼내기 전 체크포인트 0 → 다 꺼낸 뒤 4) · 설치판 이름 목록 **`list(get_args(StreamMode))`**(일곱 — `values`·`updates`·`checkpoints`·`tasks`·`debug`·`messages`·`custom`) · **모드를 목록으로 고르면 사건이 `(모드 이름, 자료)` 짝** → `for mode, data in …` · 모드를 고르지 않으면 `graph.stream_mode`(= `updates`) · 모드 이름 하나를 글로 주면 자료만 · 노드 안 **`writer = get_stream_writer()`** 다음 줄 `writer({...})`(진행 값, 모드 `custom`으로만) · `invoke` = 마지막 `values` 사건 · 체크포인터를 빼고 컴파일한 그래프 · Ch 24 01 멈춤 표시를 모드 `updates`로 받기(키 `__interrupt__` 사건 하나) | **`collect_events`**·**`positions_of`**(이 절이 처음 가르침 — 02가 도구 파일로 옮김) · 노드(`prepare`·`write`, 9절 `ask_send`, 노트북) | 스트림 모드 · 스트림 사건 · 진행 값 (3) |
| 02 토큰과 중간 진행 스트리밍 (experiment) | 노드 안 **`model.invoke(...)`도 모드 `messages`를 고르면 스트림 청크로 나옴** · 모드 셋(`messages`·`updates`·`custom`)을 한 실행에서 · `messages` 사건 자료 = **`(AIMessageChunk, 칸 metadata)` 짝** — `data[0].text`·`data[1]["langgraph_node"]`·`["langgraph_step"]`·`["ls_model_name"]` · 스트림 청크 글을 `+`로 이어 붙여 갱신의 답 글과 견줌 · 스트림 청크를 `+`로 합친 객체의 `usage_metadata` · 모드 `messages`를 뺀 실행(사건 셋) | **`mode_order`**(이 절이 처음 가르침 — 03이 도구 파일로 옮김) · 상태 형식 `AnswerState`·노드 `write_answer`(노트북) | 스트림 청크 · 칸 `metadata` · 모드 차례 (3) |
| 03 TTFT와 total 비교 (experiment) | **`import time`·`time.perf_counter()`**로 사건을 꺼낼 때마다 시각을 적기 · `round(뒤 − 앞, 3)` · 세 시간(첫 사건 시간·첫 토큰 도착 시간·전체 걸린 시간)을 한 요청 안에서 · 음수 자리 `[-1]` · 조건 `and`·`!= ""`·`is not None` · 사용량이 든 스트림 청크의 `usage_metadata["input_tokens"]`·`["input_token_details"]["cache_read"]` · 요금표 셀(`pricing_date`·`mini_prices`) · 모드 목록의 차례만 바꾼 실행 | **`collect_timed_events`**·**`first_text_place`**·**`three_times`**(이 절이 처음 가르침 — 04가 도구 파일로 옮김) · 도구 파일에서 **`estimate_cost`**(Ch 6 06)·`mode_order`·`positions_of`를 가져옴 | 첫 사건 시간 · 전체 걸린 시간 (2) — 첫 토큰 도착 시간은 Ch 15 05에서 이어 씀 |
| 04 Streaming 실습 | **새 문법·새 API 0**(01~03 노트북에 없는 AST 노드·내장 이름·속성·키워드 0, `astdiff.py`) · 새 가져오기는 도구 파일로 옮긴 03 함수 셋 | 기록 장치 `screen_log`·`print_report`(노트북) · 상태 형식 `InquiryState`·노드 `answer_inquiry`(노트북) | 0 |

- 새 용어 합계 **8개**(절 meta 「새 용어」 3·3·2·0).
- **이 챕터 주제라서 허용한 문법**: 칸만 적은 `TypedDict` 상태 형식(칸 구성이 바뀌면 새 이름 — `DraftState`·`SendState`·`AnswerState`·`InquiryState`) · `for mode, data in …` 짝 풀기(Ch 6 04 `for role, content in …`과 같은 모양) · 도구 파일 `estimate_cost` 안의 `.get` 두 줄(Ch 6 06·Ch 21 본문 그대로, 노트북 0).
- **쓰지 않은 것(네 절·도구 파일 모두 0건, 마감 AST 따로 `extra_check.py`)**: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·`break`·`while`·`try`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·대입 풀기·별표 풀기·세미콜론·`isinstance`·데코레이터·클래스(상태 형식 말고)·`join`·숫자 밑줄·**`astream`·`async for`·`version="v2"`·`subgraphs=True`·`stream_events`**.
- 셀 모양: 준비 셀이 아닌 셀 최대 9·9·10·9줄(03 8절 사용량 셀이 10줄 — 상한), 함수 본문 최대 5·8·7·8줄, 셀당 정의 하나, 첫 줄 주석 100%, 호출 깊이 최대 2. `assert`는 우리 코드·라이브러리가 정하는 값(01 모드 이름 차례·02 모드 차례·키 셀)에만 — 모델 글·초에 0.

## 2. 앞 챕터에서 이어 쓴 부품과 값

- **Ch 2 12**: 비동기 함수 — Ch 25는 쓰지 않고 b7에 「비동기 메서드 `astream`은 이번에 실행하지 않았습니다」만(뜻 그대로의 말).
- **Ch 5**: 토큰 — 「스트림 청크는 토큰과 단위가 다르다」(02 b3·용어 표). 「조각」(Ch 5 토큰 전용)은 0건.
- **Ch 6 01·04·06**: 모델 설정(`init_chat_model`·`temperature=0`·`reasoning_effort="none"`) · 모델 `stream()`이 제너레이터(01 3절) · **Ch 6 04 「청크」 = 이 과정의 「스트림 청크」**(02 b3·용어 표 두 문장 — §15 A-15) · 글자가 없는 스트림 청크 넷·사용량 청크·`+`로 합친 객체 · `for role, content in …` · **Ch 6 06 `estimate_cost`와 요금표**(03, Ch 21 `runner_tools.py` 판 본문 글자 그대로) · `time.perf_counter()`로 걸린 초.
- **Ch 13 01**: 상태 형식·노드·엣지·컴파일 · **Ch 15 05**: 「첫 토큰 도착 시간」(글자가 든 첫 스트림 청크까지 — 이어 쓴 말, 「전체 지연」은 인용할 때만) · Ch 15 06 백분위수(쓰지 않음 — b7) · Ch 17 04·Ch 18 03(시간이 주제인 자리에서만 잼 — 03 b7).
- **Ch 22 06**: 감사 기록의 「사건」(훅이 적은 사건 이름과 값)은 **스트림 사건과 다른 말**(01 b3).
- **Ch 23 01·03·04·05·06**: `InMemorySaver`·스레드·체크포인트 단계 번호·만든 자리(01 `checkpoints` 사건) · 작업(task, 01 `tasks` 사건) · `resume` 세 장면 구분(Ch 23 03 「스레드 재개」 · Ch 23 04·06 worker `resume` 단계 · Ch 24 `Command(resume=…)` — 01 b3 셋째 단락·노트북 9절).
- **Ch 24 01·04**: 멈춤 표시·질문 값·사람의 답으로 이어 가기(01 9절 — 스트림 사건으로는 01이 처음 받음) · 대출 연장 소재(04 문의 글 「빌린 책의 반납 날짜를 늘리려면 어떻게 하나요?」).
- 소재: 01 「배송 문의」(노드 둘) · 02·03 배송 문의 「주문한 책이 아직 오지 않았어요. 언제 받을 수 있나요?」와 시스템 메시지 「배송 문의에 답하는 안내 도우미입니다. 두 문장의 한국어로 답하세요.」 · 04 자료실 문의(시스템 메시지는 「배송」 → 「자료실 이용」).

## 3. 절별 사례·값 (새 커널 세 번과 노트북 밖 확인에서 같았던 값)

| 절 | 과제·입력 | 결정적 값(결론·그림에 쓴 값) |
|---|---|---|
| 01 | 노드 둘(`prepare` 진행 값 50 → `write` 진행 값 100) + `InMemorySaver`, 입력 `{'topic': ' 배송 문의 ', 'draft': ''}` | 모드 일곱 · 한 실행 사건 **23**(튜플 길이 2) · 모드별 수·자리 `values 3 [3, 12, 21]`·`updates 2 [9, 18]`·`checkpoints 4 [1, 4, 13, 22]`·`tasks 4 [6, 10, 15, 19]`·`debug 8`·`messages 0`·`custom 2 [8, 17]` · 두 번 모드 이름 차례 같음 `True` · 따로 일곱 번 = 한 실행 수 · 체크포인터 없이 **15**(`checkpoints 0`·`tasks 4`·`debug 4`) · 기본 모드 `updates`(사건 둘) · `invoke` == 마지막 values `True` · 멈춤 표시 `['__interrupt__']` → `{'ask_send': {'answer': 'approve'}}` |
| 02 | 노드 `write_answer` 하나(진행 값 30 → `model.invoke` → 진행 값 100), 모드 `["messages", "updates", "custom"]` | 모드 차례 **`['custom', 'messages', 'custom', 'updates']`** · `updates 1`·`custom 2`(첫 자리 1, `updates`가 맨 끝) · 모든 스트림 청크의 `langgraph_node` `write_answer` · 앞 값 `AIMessageChunk` · 이어 붙인 글 == 답 글 `True` · `messages`를 뺀 실행 사건 3·`['custom', 'updates']` |
| 03 | 02 그래프 그대로, 사건마다 시각 적기 · 값 바꿔 보기 = 모드 목록 차례만 `["updates", "messages", "custom"]` | 모드 차례 같음(목록 차례를 바꿔도) · 첫 사건 custom `{'stage': 'before_model', 'progress': 30}`(자리 **1**, 모델 요청 전) · `messages` 첫 사건 자리 **2**·글자 0 · 글자가 든 첫 스트림 청크 자리 **3** · 사건마다 시각 하나씩 `True` · 「첫 사건 시각 < 글자가 든 첫 스트림 청크 시각 < 끝 시각」 두 비교 `True` · 4~6절 계산 == 함수 `True` |
| 04 | §7 | §7 |

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀)

| 절 | 말 | 뜻 | 코드에서 |
|---|---|---|---|
| 01 | 스트림 모드(stream mode) | 한 실행에서 생긴 일 가운데 무엇을 어떤 모양으로 받을지 고르는 이름 | 인자 `stream_mode`의 글(설치판 일곱) |
| 01 | 스트림 사건 | 메서드 `stream`이 한 번에 하나씩 내놓는 값 — **Ch 22 06 감사 기록의 「사건」과 다른 말** | `for`가 꺼낸 값, 목록으로 고르면 `(모드 이름, 자료)` 짝 |
| 01 | 진행 값 | 노드가 실행 도중에 쓰기 함수로 직접 보내는 값(숫자는 우리가 정한 값 — 라이브러리가 계산한 진행률 아님) | `writer({"stage": …, "progress": …})`, 모드 `custom`으로만 받음, **상태의 칸에 들어가지 않음** |
| 02 | 스트림 청크 | 스트리밍에서 한 번에 도착하는 답의 일부 — Ch 6 04 「청크」와 같은 것, 토큰과 단위가 다름 | 모드 `messages` 사건 자료의 앞 값 `AIMessageChunk` |
| 02 | 칸 `metadata` | 스트림 청크와 짝으로 오는 딕셔너리(어느 노드·단계·모델) — **이름에 칸이 붙었지만 그래프 상태의 칸이 아니라, 사건 짝의 둘째 값**(마감 A-3) | `data[1]`, 키 `langgraph_node` 등 열둘 |
| 02 | 모드 차례 | 같은 모드의 사건이 이어지면 한 번만 적어, 모드가 바뀐 차례만 남긴 목록 | `mode_order(events)` |
| 03 | 첫 사건 시간 | **메서드 `stream`을 부른 때부터**(마감 B-2), 모드와 관계없이 처음 받은 사건까지 걸린 시간 | `timed_run["times"][0] - timed_run["start"]` |
| 03 | (이어 씀) 첫 토큰 도착 시간 | Ch 15 05 정의 — 글자가 든 첫 스트림 청크를 받기까지. Ch 15 05는 모델의 `stream()`을 부르기 직전부터, 이 절은 그보다 조금 앞(그래프 `stream`을 부르기 직전)부터 잼 | `first_text_place`로 찾은 자리의 시각 |
| 03 | 전체 걸린 시간 | 메서드 `stream`을 부른 때부터 마지막 사건까지 다 받고 끝날 때까지 | `timed_run["end"] - timed_run["start"]` |

- **쓰지 않는 말(네 절 설명·주석·캡션·`.mmd`·README 참 금지어 0건 — 제목·슬러그·코드 백틱 말고)**: Ch 24 목록 전부 + 「소비자」·「레이턴시」·「이벤트」·「옵션」·「스냅숏」·「태스크」·「디버그」·「메타데이터」(코드 `metadata`는 「칸 `metadata`」)·「도메인」·「필터링」(→ 거르기)·「명시」·「근삿값」·「워밍업」·「공정」·「단조」·「측정」(→ 재기)·「추정」(→ 예상)·「지연」·「조각」·「구독」(→ 함께 받는다)·한정어 없는 「청크」(**02 5절 코드 주석 둘만 — 다음 재실행 몫, 설명 셀에 한 문장**). 「TTFT」·「total」은 03 제목·슬러그와 03 b2·노트북 1절의 제목 풀이에만. 「비동기」는 Ch 2 12 말이라 금지어가 아님(01~04 b7·04 b8 「비동기 메서드 `astream`」 다섯 곳, 뜻 그대로). 마감 전후 금지어 대조(`.cache/ch25-close/tools/bandiff.sh`) — 마감이 더한 문장의 새 걸림은 거짓 양성(「캐시 입력」·제목 풀이 「total」·「체크포인터」 안 「포인터」)뿐.
- **「칸」 뜻 겹침**: 과정의 「칸」은 Ch 13부터 상태 형식의 키(`question`·`answer`). 02의 「칸 `metadata`」는 이름만 칸 — 구분 문장을 두고 이름은 그대로(강사 확인). 01 셀 31 주석 「칸 값에 관한 세 모드(values·updates·custom)」의 custom은 진행 값이라 칸이 아님(셀 32 결과 읽기 한 문장, 주석은 다음 재실행 몫).
- **비유 계열 「대나무 홈통과 물방울」**: 홈통에 한 번 흘린 물 = 한 실행 · 떨어지는 방울 = 스트림 사건 · 구멍과 그릇 = 스트림 모드 · 빈 그릇 = 사건이 없는 모드(01 `messages`) · 크기가 제각각인 물방울 = 스트림 청크 · 종 = 진행 값 · 한 번 기우는 통 = 갱신 하나 · 종이 울린 때 / 첫 방울이 닿은 때 / 그릇이 가득 찬 때 = 첫 사건 시간 / 첫 토큰 도착 시간 / 전체 걸린 시간 · 마디 셋을 이은 긴 홈통 = 세 절 기능을 이은 그래프, 윗머리 깃발 = 모델 요청 전 진행 값. **비유와 다른 점**(각 절 b4): 홈통은 막은 구멍의 물이 다른 구멍으로 가지만 그래프는 고르지 않은 모드의 사건을 넘기지 않음(01) · 통은 저절로 기울지만 갱신은 노드 코드가 끝나야 나옴(02) · 첫 스트림 청크에는 글자가 없음(03) · 진행 값을 빼면 첫 사건은 글자 없는 스트림 청크(04). 01 용어 표의 진행 값 일상 예는 「부엌에서 「재료 손질 끝」 하고 알려 주는 말」(02 비유의 종과 둘 — 강사 판단).
- 삽화 넷: 01-5 홈통 하나·구멍 일곱·흰 그릇 일곱(여섯째 빔) · 02-5 종 둘(왼쪽 = 진행 값 30, 오른쪽 = 100 — **종의 자리는 울리는 차례를 나타내지 않음**, 마감 A-11)·크기가 다른 물방울 일곱·기우는 대나무 통 · 03-5 마주 보는 홈통 끝 둘·첫 방울만 든 그릇과 가득 찬 그릇 · 04-4 마디 셋을 이은 두 홈통·위에만 깃발(**위 반쪽 관·아래 둥근 관으로 모양이 조금 다름 — 비유의 차이는 깃발 하나**, 마감 B-7). 사람·손·화살표·글자·숫자 없음. 물방울 수는 스트림 청크 수와 짝짓지 않음.

## 5. 색 규칙 (Mermaid 15장)

- **넣은 입력·요금표 초록(tool)** · **우리 노드·함수·시각을 적은 자리·고른 모드 목록 파랑(flow)** · **출력으로 확인한 값 노랑(measure)** · **라이브러리 메서드(`graph.stream`)·두 실행 공통 값·소스로만 확인한 동작 회색(클래스 없음, 「소스 확인」)** · **보라 = 이 절에서 실제로 부른 모델**(02-1·03-2·04-1, 01은 0장).
- **네 절 모두 experiment라 빨강 0장**(받아 출력한 오류가 있었다면 노랑).
- 나란한 두 실행은 subgraph 둘 + 회색 공통 상자(`~~~`, 공통 상자에는 두 칸 출력에서 모두 확인한 값만). 원본 viewBox 폭 모두 868 이하(최대 01-4 798). 라벨에 초·사건 수·스트림 청크 수·토큰 수 없음(흔들린 값) — **02-3·03-3은 마감에서 `NN-probe.md` §0 규칙대로 키 목록·단계 번호·입력 토큰·캐시 입력·사용량 청크 수도 뺌**.
- **마감에서 다시 렌더한 `.mmd`: `01-1`·`02-3`·`03-3`**(`--force`, PNG 직접 확인). 01-1은 무리 이름 「칸 값에서」 → 「칸 값과 진행 값에서」(폭 725 그대로, 노트북 첨부도 갈아 끼움) · 02-3 「키 열둘 … langgraph_step 1」 → 「첫 스트림 청크의 langgraph_node write_answer」(폭 576 그대로) · 03-3 「한 요청에 하나」·「입력 토큰 47 · 캐시 입력 0」 → 「사용량이 든 스트림 청크」·「입력 · 캐시 입력 · 출력 토큰 수」(폭 440 → 461). 삽화는 다시 만들지 않음.

## 6. 결정적 값과 흔들린 값

- **결정적 값**(결론·그림·정리·복습에 쓴 값): §3 표 전부 + §7. 모두 새 커널 세 번(01은 네 번)과 노트북 밖 흔들림 확인(02·03·04 각 열 번)에서 같았습니다. 결론은 **사건의 차례와 자리**뿐입니다.
- **흔들린 값 — 결론·그림·정리·복습에 쓰지 않음**(결과 읽기 둘째 단락·b6 표·「확인할 점」·b7에만 「이번 실행에서는」·「교재 출력에서는」): 초 전부(03 교재 출력 첫 사건 0.003·첫 토큰 도착 1.51·전체 1.758 / 노트북 밖 첫 사건 0.003~0.006·첫 토큰 도착 0.498~1.568·전체 0.719~1.773, 04 교재 출력 첫 토큰 도착 0.666·0.699·0.568) · 두 구간 · 비율(03 노트북 밖 열 번 모두 첫 토큰 도착 시간이 전체의 절반을 넘음 — b7 한 문장) · 사건 수·스트림 청크 수(02 교재 출력 `messages` 40, 노트북 밖 34~50 · 04 62·60·60) · 출력 토큰(02·03 40, 밖 40~50 · 04 밖 59~66) · 예상 비용(03 교재 출력 0.000215달러) · 답 글.
- **노트북 밖에서만 본 값(b7에 「노트북 밖」 표시)**: 02 `messages` 사건 수 = 출력 토큰 수(교재 출력과 다섯 번 모두 — 까닭은 확인하지 않음, 「스트림 청크 수를 토큰 수로 읽지 않습니다」를 함께) · 02 `messages`를 고르지 않은 실행의 새 청크 알림 0회(스트리밍 요청이 아님 — 설치판 소스와 함께) · 03 시계 `monotonic=True` · 03 첫 사건 시간 0.003~0.006초(마감 B-3에서 b6 → b7) · 04 실행 2 설정 첫 사건 시간이 실행 1 설정보다 늘 큼(결론에 쓰지 않음).
- **재지 않은 것·견주지 않은 것**: **스트리밍하지 않은 실행과 걸린 시간 견주기**(03·04 — 마감 B-1로 03 b7·b10·노트북 7절에 밝힘) · 여러 번 재어 가운데 값·백분위수 · 네트워크 몫과 서버 몫 · 시작 시각과 첫 노드 시작 차이 · 01·02 걸린 시간 · Windows·macOS 실행 · `astream`·`version="v2"`·`subgraphs=True`.
- 셀 하나만 다시 실행하면 01은 같은 스레드에 체크포인트가 이어 쌓임(노트북 밖 확인 — 단계 3~6) → 준비물·b7 「2절 그래프 셀부터 다시 실행」.

## 7. 04절 실습 절 주제와 결과

- 제목 「**Streaming 실습: 요청 전 진행 값을 켜고 끄며 자료실 문의 답 흘려 보이기**」, 슬러그 `04-Streaming-실습`, `format: experiment`, meta 「실습 30분 · 새 용어 0」. **챕터 시수에 더하지 않습니다**(규격 §7-2). 01~03 meta 합 강의 1+1+1 = **3h** · 실습 1.5+1.5+2 = **5h** = `chapter.json` 「총 8h · 강의 3h · 실습 5h」(`_build_index.py`도 3·5).
- 자료실 문의 창 흉내 — 상태 형식 `InquiryState`(칸 `question`·`answer`·`show_notice`, 셋 다 글) · 노드 `answer_inquiry`(02 `write_answer`와 같은 차례에 `if state["show_notice"] == "yes":` 한 줄 — 진행 값 30은 그때만, 100은 늘) · 기록 장치 `screen_log`(진행 값 목록 + 스트림 청크 글 이어 붙이기)·`print_report`(모드 차례·첫 사건 모드·글자가 든 첫 스트림 청크 자리·화면 진행 값·화면 글 == 답 글).
- 붙인 앞 절 기능 셋(세 실행 모두 흐름 안에서 쓰임): **01** 모드 목록 `["messages", "updates", "custom"]`·(모드 이름, 자료) 짝 풀기·`positions_of` · **02** 진행 값·스트림 청크 이어 붙이기·`mode_order` · **03** `collect_timed_events`·`first_text_place`·`three_times`. 뺀 것: 01 일곱 모드 전부·체크포인터·멈춤 표시 · 02 칸 `metadata`·`messages` 뺀 실행 · 03 목록 차례·예상 비용·두 구간.
- 실행 1(`"yes"`) → **같은 설정 다시**(대조 — 사건 수·초는 달라도 모드 차례·자리는 같음) → 실행 2(**칸 `show_notice` 하나만 `"no"`**). 모델 요청 **3번**.
- 결과(새 커널 세 번 15/20 같음 — 갈린 다섯은 사건 수·답 글·초 셀): 실행 1·같은 설정 다시 `모드 차례: ['custom', 'messages', 'custom', 'updates']`·`첫 사건의 모드 이름: custom`·`글자가 든 첫 스트림 청크의 자리: 3`·`화면에 띄운 진행 값: [30, 100]`·`화면 글과 답 글이 같은가: True`·`두 실행의 모드 차례가 같은가: True` · 실행 2 `모드 차례: ['messages', 'custom', 'updates']`·`첫 사건의 모드 이름: messages`·`글자가 든 첫 스트림 청크의 자리: 2`·`화면에 띄운 진행 값: [100]`·`첫 사건 스트림 청크의 글자 수: 0`·`진행 값의 자리가 마지막 사건 바로 앞인가: True` · 8절 표 `실행 1 | custom | 3 | 2`·`같은 설정 다시 | custom | 3 | 2`·`실행 2 | messages | 2 | 1`. `assert`는 키 셀 하나뿐.
- 코드 셀 20(실습 선례 19~28) · 코드 줄 103 · 함수 본문 7·8줄. 「같은 설정 다시」·`"yes"`/`"no"`·8절 둘째 표(세 시간)는 강사 확인.

## 8. 도구 파일 `notebooks/stream_tools.py` — 함수 표·해시 변천·생성기 대조 사슬

| 함수(인자) | 배운 곳 | 가져오는 절 | 하는 일 |
|---|---|---|---|
| `collect_events(graph_to_run, graph_input, config, modes)` | Ch 25 01 노트북 4절 | 02 | 한 번 실행하며 받은 사건을 목록에 모아 **다 끝난 뒤** 내놓음(시각 없음) |
| `positions_of(events, mode)` | Ch 25 01 노트북 4절 | 02·03·04 | 한 모드 사건이 몇 번째(1부터)에 나왔는지 목록 |
| `mode_order(events)` | **Ch 25 02 노트북 4절** | 03·04 | 같은 모드가 이어지면 한 번만 적은 모드 차례 |
| `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` | Ch 6 06(Ch 21 `runner_tools.py` 판 본문 글자 그대로) | 03 | 사용량과 세 요금(100만 토큰당 달러)으로 예상 비용, `usage`가 `None`이면 `None` — `.get` 두 줄(도구 파일 안 선례) |
| `collect_timed_events(graph_to_run, graph_input, config, modes)` | **Ch 25 03 노트북 3절** | 04 | 시작 시각(`stream`을 부르기 직전) → 사건을 담은 바로 뒤마다 시각 → 끝 시각, 딕셔너리 `start`·`events`·`times`·`end` |
| `first_text_place(events)` | **Ch 25 03 노트북 5절** | 04 | 글자가 든 첫 스트림 청크의 자리(1부터), 없으면 `None` |
| `three_times(run_record)` | **Ch 25 03 노트북 7절** | 04 | 한국어 키 셋 딕셔너리(세 시간, 셋째 자리) — 안에서 `first_text_place`를 부름 |

- 함수 일곱, 함수마다 `# Ch NN MM절에서 배웠습니다 — …의 같은 이름 함수를 옮겼습니다`, import는 `time` 하나(머리 설명 바로 뒤 주석 한 줄과 함께 — `collect_timed_events`가 씀). 노트북 전역 이름 기대기 0, 금지 문법 0(허용 표시 `.get` 둘). 앞 챕터 도구 파일(numpy·SQLite 체크포인터를 가져옴)은 파일째 가져오지 않음. 노드·상태 형식·시스템 메시지 글은 노트북 전역 `model`을 읽어 도구 파일에 두지 않음(03·04가 다시 적음 — 02 셀과 글자 같음, 생성기 대조).
- **해시 변천**: 없음 → 02 `dfea09bc3644…`(함수 둘) → 03 `a468d87878fc…`(+ `mode_order`·`estimate_cost`, 62줄) → 04 **`3a734aeb87244a7d05574acd9f1d269a7ab2ddd1a944d018e60baa82c4708ff5`**(+ `import time`·03 함수 셋, 103줄) → **마감 그대로**(챕터 리드 결정 — Ch 24 A-13 선례와 같이 해시 고정).
- 머리 설명은 02 판 글(「Ch 25 01절 노트북 4절에서 처음 적은 함수 둘은 설명 주석과 본문을 글자 그대로 옮겼습니다」)이라 함수 일곱의 출처를 모두 적지 않습니다(검토 A-14·B-12 — 틀린 말이 아니라 모자란 말). 함수마다 위 주석에 출처가 있고, 마감에서 다시 쓴 실습 폴더 README가 일곱 함수의 배운 절·가져오는 절·`time`을 적습니다. 머리 설명 고침은 Ch 24와 함께 전체 마감 몫(체크리스트 §2-13).
- **생성기 대조 사슬**(마감에서 다시 확인 — 모두 통과, 고친 줄 0): `author_02.TOOLS` = `TOOLS_HEAD` + 01 함수 둘(`author_01.DEF_COLLECT`·`DEF_POSITIONS`) · `author_03.TOOLS` = `author_02.TOOLS` + `NEW_TOOL_PARTS`(`mode_order` — 02 노트북 셀 글, `estimate_cost` — Ch 21 `runner_tools.py` 글) · `author_04.TOOLS` = `TOOLS_HEAD` + `IMPORT_BLOCK`(`import time`) + `author_03.TOOLS` 나머지 + 03 함수 셋 = **디스크 파일**. `author_02.strip_later_imports(디스크)`가 02·03 판으로 시작 → 02·03 생성기는 04 판을 덮어쓰지 않고 건너뜀. `author_02.check_same_as_01()`·`author_03.check_tools()`·`check_same_as_02()`·`author_04.check_tools()`(함수 이름 일곱·import `["import time"]`·03 노트북 셀과 글자·AST 같음) 통과. `author_01`은 도구 파일을 쓰지 않음. **`--src-only` 없이 부르면 노트북 출력이 지워지므로**(각 생성기 머리 설명) 설명만 고칠 때는 `--src-only` → `run_section.sh … NN --no-exec`.
- 마감: 네 생성기를 `--src-only`로 다시 돌려 `_src` 4/4가 바이트까지 같고, `cells()`가 노트북과 59·54·52·44셀 같음(`.cache/ch25-close/tools/genmatch.py` — 코드 셀 글 같음, 마크다운은 마감 고침대로).
- **전체 마감 2026-09-30: 머리 줄 고침, 새 해시 `6df804b89b55ff77b1a148746b68c021767b1ddf7163d6a2194e94c922127db4`**(검토 A-14·B-12 · 체크리스트 §2-13 6번). 1행 「앞에서 배운 평범한 함수를」 → 「앞 챕터와 이 챕터 앞 절에서 배운 평범한 함수를」, 6행 「Ch 25 01절 노트북 4절에서 처음 적은 함수 둘은 설명 주석과 본문을 글자 그대로 옮겼습니다.」 → 「이 챕터 01·02·03절 노트북에서 처음 적은 함수 여섯과 Ch 21 도구 파일 runner_tools.py의 estimate_cost는 / 설명 주석과 본문을 글자 그대로 옮겼습니다.」(두 줄 — 머리 설명 9 → 10줄). `import time` 주석·함수 일곱 본문은 AST·글자 같음. 생성기 안 판: 02 `dfea09bc…` → `b26cc3ca…` · 03 `a468d878…` → `83061c7e…` · 04 = 디스크. 고친 생성기: `author_02.TOOLS_HEAD` 한 곳뿐(`author_03`·`author_04`의 `TOOLS`·`strip_later_imports`·`check_*`·쓰기 가드는 모두 이 상수를 따라감, 챕터 안 해시 고정값 없음). **뒤 챕터 고정값**: Ch 26 `author_01.STREAM_SHA`·Ch 30 `author_04.STREAM_TOOLS_SHA`를 새 값으로(설명 한 줄씩, 두 생성기 `--src-only`를 쓰기 없이 돌려 `_src` 바이트 같음). 조건 넷: (가) 노트북 넷 마크다운·출력과 `_src`·HTML·README에 머리 글·판 해시 0 · (나) 네 생성기를 파일 쓰기를 가로챈 채(`.cache/final-close/2-tools-head/tools/dryrun.py`) `--src-only`와 인자 없는 모드로 돌림 → `_src` 넷 바이트 같음, 02·03 가드 `skip`, 04 가드는 같은 글, `check_same_as_01`·`check_tools`·`check_same_as_02`·`author_04.check_tools` 통과, `cells()`가 노트북과 59·54·52·44셀 같음 · (다) 모델 없는 01 사본(도구 파일을 가져오지 않는 절)을 새 커널로 돌려 셀별 28/28(설치 셀 스트림 나뉨만), 모델 절 02·03·04는 사본 실행 없이 가져오는 이름(2·3·5개)이 새 파일에 있고 함수 본문 AST가 옛 파일과 같음만 확인 · (라) 이 줄·handoff·계약 §4. 노트북 `code_sha256`·`outputs_sha256` 전후 같음.

## 9. 묶음 실행 검사 (Part 6 `check_bundle_execution.py`)

- 검사 목록은 Ch 24 01·Ch 28 01뿐이고 **Ch 25는 없습니다**(스크립트는 고치지 않음). Ch 25 01은 모델·키 없이 결정적으로 도는 노트북이라 Ch 24 01과 같은 조건입니다 — **넣을지는 전체 마감 후보**(체크리스트 §2-13). 02~04는 키가 필요해 대상이 아닙니다.
- **마감 결과**: `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache UV_LINK_MODE=symlink`만(스크립트 수정 0, `TMPDIR`은 세션 폴더 — 맥 마운트 밖) → **PASS**(Ch 24 01 `code_sha256` `7187f7a39f3f…` 28셀 · Ch 28 01 4셀). `bundle-execution.json` `a72edd8a…`(Ch 24 마감 때 zip `edd8c3be…` 기록 — 04절이 zip을 `acf14b06…`으로 다시 만든 뒤에는 돌리지 않았음) → **`baaaf52f223ce29c0d552ffef81ce66c297346dbb7cf4cbfde5fe74cd3b1d378`**(`archive_sha256` `71683e44…`).

## 10. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `labs/part6/ch25-streaming/notebooks/01~04-*.ipynb`·`stream_tools.py` | 01~04절 · **마감(마크다운만)** | 실습 폴더(챕터 몫) — §1·§8. 마감: 코드·출력 그대로, 파일 `723a4a14`→`be881fc5` · `74e56120`→`e4068dbd` · `bf146282`→`933c4202` · 04 `d0001464` 그대로. 도구 파일 그대로 `3a734aeb…` |
| `labs/part6/ch25-streaming/README.md` | 04절(04 단락) · **마감(전체)** | `ef0bf41d…`(원본) → `bd86ef71…` → **`d29f86b3b970d71502db72eb0dfee7fa94ea188e890117cae0eb2c0f0ef1209e`**: 노트북 넷, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 설치 판(01 `langgraph` 1.2.11·`langgraph-checkpoint` 4.2.0 / 02~04 `langchain` 1.4.0·`langchain-openai` 1.6.0·`langgraph` 1.2.11·`python-dotenv` 1.2.3), **모델 요청 01 0번(API 키 불필요) · 02 2번 · 03 2번 · 04 3번**, 예상 비용(요금표 2026-09-17 어림, 청구 금액 아님), 키는 `.env`의 `OPENAI_API_KEY`에서만(학생 묶음이면 `part6-practice/`의 `.env`, 값 출력 0), 초 값은 실행마다 달라짐, 도구 파일 단락(규격 §2-7 고정 문장 뜻 · 함수 일곱 · 배운 절 · 가져오는 절 · import `time`), 절마다 하는 일, 04 단락. 묶음 밖 파일을 가리키지 않음, 참 금지어 0(「체크포인터」 거짓 양성 말고), 문장 70자 이하 |
| `textbook/part6/ch25-streaming/chapter.json` | 04절 · **마감** | 04 절(04절) · `objectives` 셋 → **넷**(절마다 한 줄 + 04 실습 줄, 옛 「stream mode」·「사용자 정의 진행 상황」·「측정」 뺌), `hours` 그대로(`28171e32` → `da13aa03` → `7735f770`, 보호 파일) |
| `textbook/part6/ch25-streaming/qa/public-files.json` | 02·04절 | 도구 파일(02)·04 HTML·노트북 두 줄(04). 옛 그림 줄은 원래 없음 — 마감 그대로(`0b890e75`) |
| `textbook/part6/public-files.json` | 02·04절 | `collect_public_files.py`(도구 파일·04 노트북 줄, `8140df88`) — 마감에서 다시 돌려 **바이트 같음**, `prerequisite-files.json`(`4c7f5a4b`) 같음 |
| `textbook/part6/_build_index.py` | **마감** | ch25 설명 「토큰과 진행 이벤트를 구분하고 첫 응답과 전체 처리 시간을 측정합니다.」 → 「스트림 모드 일곱을 한 실행에서 받아 사건의 수와 자리를 세고, 모델을 부르는 노드에서 진행 값과 스트림 청크를 함께 받아 이어 붙이며, 사건마다 시각을 적어 첫 사건·첫 토큰 도착·전체 걸린 시간을 한 요청 안에서 잰 뒤, 자료실 문의 답에 세 기능을 모아 요청 전 진행 값 하나를 끄는 실습을 합니다.」(시수 3·5 그대로, `5ffb7dde` → `e8d784c4`, 보호 파일) |
| `textbook/_notebook/build_index.py` · `textbook/index.html` | **마감** | Ch 25 설명 「토큰·진행 이벤트를 구분하고 첫 응답과 전체 처리 시간을 측정합니다.」 → 「스트림 모드로 실행 사건을 받고, 진행 값과 스트림 청크의 차례와 첫 토큰 도착 시간을 잽니다.」. **절 수 3은 그대로**(과정 전체가 실습 절을 빼고 세는 약속 — Ch 1~24 모두 같음, 전체 목차 마감 몫). 스크립트를 한 번 돌려 `textbook/index.html`을 다시 만듦 — 돌리기 전 스크립트 출력이 지금 파일과 바이트까지 같았고, 바뀐 줄은 Ch 25 행 하나(`53db811e`→`4bca42a3` · `1aea1103`→`90d6a6b8`, 보호 파일) |
| `labs/part6/continuity-guide.md` | **마감** | Ch 25 줄 「Ch6의 토큰 스트리밍, Ch2의 비동기 실행 \| Ch25 토큰·중간 단계·진행 이벤트와 지연 시간」 → 「Ch6의 스트리밍(스트림 청크), Ch13의 그래프, Ch15의 첫 토큰 도착 시간 \| Ch25 스트림 모드로 받는 사건, 진행 값과 스트림 청크, 첫 사건·첫 토큰 도착·전체 걸린 시간」(셋째 칸 그대로, `149a572a` → `629587f0`, 보호 파일, 묶음에 들어감) |
| `textbook/part6/index.html` · `textbook/downloads/part6-practice.zip` · `textbook/part6/qa/integration-results.json` | 04절 + **마감** | `python3 textbook/part6/_build_index.py`(README·노트북·`chapter.json`·목차 줄·continuity-guide를 모두 고친 뒤 **마지막에 한 번**) → **`Part 6: 52 verified sections; 100 bundled files`**, zip `acf14b06…` → **`71683e44e8e0d5ca9e90e800bc9a9490ef435e7b82c25cf59c45189241adc6f0`**(103항목, **Ch 25 8파일이 모두 디스크와 같음**, `continuity-guide.md` 같음, `__pycache__`·`.env` 0), `index.html` `778b240b` → `64594baf`, `integration-results.json` `8b9ecb32` → `bfe462a5` |
| `textbook/part6/qa/bundle-execution.json` | **마감** | §9(`a72edd8a` → `baaaf52f`) |
| `textbook/part6/qa/visual-results.json` · `textbook/_notebook/checks/ch25-streaming/visual-results.json`(+ 스크린숏 넷) | **마감** | `visual.cjs` 10행 PASS. 공용 파일은 **Ch 25 줄만** 8 → 10(04 두 줄, 새 HTML 해시), `screens` 122 → 124, 다른 챕터 줄 114개 그대로(`dd444465` → `f2b70b7b`, 보호 파일) |
| `textbook/part6/qa/notebook-readiness.json` | **마감(되돌림)** | 옛 `check_notebook_readiness.py`가 멈추기 전에 다시 써서 실행 전 사본으로 되돌림(내용 변경 0, `b3d69e9c…`) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch25-streaming.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀(마감 뒤 `feefa318…` — 04절 뒤와 같음) |
| `textbook/part6/_generate_ch25_ch26.py`(공용 옛 생성기) | 01절 | Ch 25 쪽 건너뛰기(머리 주석 넷 + `chapter == "ch25-streaming"`일 때 `continue` 세 곳, `545db83c` → `0767052613d9`, Ch 26 쪽 결과 파일 15개 해시 같음). **마감은 옮기지 않음**(Ch 26이 아직 씀) — §13 |
| **`textbook/part6/ch25-streaming/figures/_gen_figures.py` → `qa/upgrade/before/generators/blocked/_gen_figures.py`** | 01절(막음) · **마감(`mv -n`)** | 옛 그림 생성기(`cb02fe4e…` 같음). 부르는 빌드·검사 스크립트 0(`grep` — `textbook/part6/qa/final-artifact-hashes.json` 기록뿐) |
| `textbook/qa/upgrade-progress.md` · `textbook/qa/upgrade-final-checklist.md` | **마감** | Ch 25 행 한 줄 · §2-13 Ch 25 항목과 §3·§4 Ch 25 줄 |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`·`PLAYBOOK.md`·과정 요약·`upgrade-contracts.md` · 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs`·`execute.py`·`render_mermaid.py`·`attach_figures.py`) · Part 6 옛 검사 스크립트와 `check_*`·`collect_public_files.py` · Part 6 `_src/index.html` 8행(「Ch 25는 … 시간을 측정합니다」 — 뜻은 참, Part 6 목차 원문 몫) · `labs/part7/continuity-guide.md` 7행 · `textbook/part6/qa/final-artifact-hashes.json`(옛 판 기록) · `textbook/part6/qa/ch25-second-technical-review.md`·`ch21-ch29-technical-review.md`(Part 6 쪽 옛 검토 기록, 보호 파일) · 실습 폴더 `pyproject.toml`·`uv.lock` · 도구 파일(해시 고정) · **Ch 26 이후 파일 전부**(Part 6 목차·묶음·공개 목록·기록·`continuity-guide.md` Ch 25 줄 말고) · 공용 옛 생성기 `_generate_ch25_ch26.py`.
- **파일을 지운 것은 없습니다.** 옮긴 것은 옛 생성기 하나(`mv -n`, 해시 같음). 옮긴 뒤 `_build.py`·`verify.py`·게이트 통과.
- **보호 파일 147개(`before-manifest.json`)**: **114개 같음 · 32개 바뀜 · 1개 옮김(없어짐)** — 모두 의도한 것. 마감이 바꾼 것 28 + 옮김 1 + 01~04절이 바꾼 뒤 마감이 건드리지 않은 4. 목록은 `manifest-changes.md` 「마감 뒤」.

## 11. 기준 버전·확인 날짜

- 실습 폴더 잠금(`pyproject.toml` 직접 의존 `langchain==1.4.0`·`langchain-openai==1.6.0`·`langgraph==1.2.11`·`python-dotenv==1.2.3`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`): `langchain-core 1.6.2`·`langgraph-checkpoint 4.2.0`. 노트북 `%pip`은 01 `"langgraph==1.2.11" "langgraph-checkpoint==4.2.0"`, 02~04 `"langchain==1.4.0" "langchain-openai==1.6.0" "langgraph==1.2.11" "python-dotenv==1.2.3"`(잠금 판).
- 교재 출력: Linux aarch64 · Python **3.12.13** · 환경 `.cache/vm/venv-ch25-streaming`(잠금 판). 실행일 모두 2026-09-25(01 17:46 · 02 18:14 · 03 18:45 · 04 19:16 UTC — 마감에서 다시 실행하지 않음). 모델 `gpt-5.4-mini`(응답 모델 `gpt-5.4-mini-2026-03-17`).
- 설치판 소스 행(검토 A·B와 마감이 다시 확인): langgraph `types.py` 122~135(모드 일곱·설명, 135 `debug` = `checkpoints`·`tasks`)·138~141(쓰기 함수) · `graph/state.py` 1357(기본 모드 `updates`) · `config.py` 126(`get_stream_writer`) · `pregel/main.py` 2655~2672(`stream` 인자)·3913~3955(`invoke`가 `stream`을 부름) · `pregel/_loop.py` 632(`checkpoints` 사건만 체크포인터 조건)·674(`tasks` 조건 없음) · **`pregel/_messages.py` 49~54(모델 스트림 + 노드 출력 속 메시지 객체)·151~164·223~246**(마감 A-2) · langchain-core `language_models/chat_models.py` 549~585(`_should_stream`)·1969~2016 · **`language_models/base.py` 222~290(`lc_versions`)**(마감 A-9) · **langchain-openai `chat_models/base.py` 1332~1351(`stream_usage`는 기본 주소·기본 클라이언트일 때만)**(마감 B-6).
- 참고 자료(2026-09-25 확인): LangGraph Streaming(모드 표 — `checkpoints`·`tasks`에 「Requires a checkpointer」, 설치판 출력과 다름 · `(message_chunk, metadata)` · `.invoke`로도 메시지 사건) · Python 3.12 `time.perf_counter`·`get_clock_info` · OpenAI Latency optimization(스트리밍이 기다림을 줄인다는 **문서의 설명** — 이 챕터는 그 비교를 실행하지 않음) · OpenAI `gpt-5.4-mini` 요금(입력 0.75·캐시 입력 0.075·출력 4.50달러/100만 토큰, 요금표 2026-09-17, 검토 B가 2026-09-25 다시 확인).

## 12. 강사 확인 대상

1. **제목 말**: 챕터 「Streaming」 · 01 「stream mode」 · 02 「토큰」 · 03 「TTFT」·「total」 · 04 「Streaming 실습」(긴 부제). 본문 첫 자리에서 한 번씩 풂. 슬러그 01은 Ch 24 04 b8이 링크해 고정, 02·03은 Part 6 목차·앞 절 링크만, 04는 03 b8·Part 6 목차.
2. **칸 `metadata` 이름**(검토 A-3): 구분 문장만 더하고 이름은 그대로 — 바꾸면(예: 「딸린 정보 `metadata`」) 02 재실행·코드 주석 둘·도구 파일 주석(해시)·생성기 사슬이 바뀜.
3. **삽화 04-4**(검토 B-7): 다시 만들지 않고 그림 읽기·캡션·alt에 두 홈통 관 모양 차이(위 반쪽 관 · 아래 둥근 관)를 밝힘 — 재생성 한도 1회를 이미 씀. 한도를 넘어 다시 만들지.
4. **`chapter.json` 학습 목표 셋 → 넷**(절마다 한 줄 + 04 실습 줄, `hours` 그대로) · `_build_index.py`·`build_index.py`·`continuity-guide.md` Ch 25 문구 · 실습 폴더 README 다시 쓴 범위.
5. **04 「같은 설정 다시」 실행**(요청 3번 — 규격 §7-2 「실행 1·실행 2」 틀보다 한 번 많지만 3~5번 안) · **칸 `show_notice`의 글 `"yes"`/`"no"`**(`bool`을 새로 쓰지 않으려고 — 오타면 조용히 꺼지는 약점) · **04 8절 둘째 표(세 시간)** · 04 코드 셀 20.
6. **코드 줄 증가**(주석·빈 줄 뺌): 01 41→155(셀 4→28) · 02 61→138(4→25) · 03 76→133(5→24) · 04 새 절 103 + 도구 파일 53 — 챕터 178 → 529. 줄일 후보(검토 A 「사람이 정해야 할 것」 1): 01 9절(Ch 24 이음 셀 다섯)·5절 모드별 세부 셀 셋, 02 7절 답 글 셀·합친 객체 셀 — 줄이면 다시 실행.
7. **01·02·03 설계**: 01 모델 없음(M2)·`get_args`·「걸린 시간은 재지 않았습니다」 · 02 준비물 예상 비용을 문장으로만 · 03 새 말 둘·값 바꿔 보기(목록 차례)·`estimate_cost` `.get`·`[-1]`·`and` 첫 사용·b7 비율 문장·시계 문장(노트북 밖)·8절 10줄 셀 · 02 삽화 받침돌 잘림.
8. **b7 「`messages` 사건 수 = 출력 토큰 수」**(02, 노트북 밖 다섯 번과 교재 출력) — 「스트림 청크 수를 토큰 수로 읽지 않습니다」를 붙여 두었음. 뺄지.
9. **01 용어 표 진행 값 일상 예(부엌 말) ↔ 02 비유의 종** — 같은 챕터 진행 값 비유가 둘(검토 A-11 — 02 쪽만 고침).
10. **01을 Part 6 묶음 실행 검사에 넣을지**(키 없이 결정적 — Ch 24 01과 같은 조건, §9).
11. **도구 파일 머리 설명**이 01 함수 둘 기준(A-14·B-12 — 해시 고정 결정으로 그대로, README가 일곱 함수를 설명). Ch 24와 함께 고칠지.
12. 한국어 감사 3단·그림 판독 2차(별도 세션 — 두 검토의 「확인하지 못한 것」: 삽화 01-5·02-5·03-5 직접 판독, Windows·macOS 실제 실행, 학생 `uv sync --locked` `.venv` 첫 셀).

## 13. Ch 26이 이어받을 것과 전제하면 안 되는 것

### 이어받을 것

- 말: 스트림 모드·스트림 사건·진행 값(01) · 스트림 청크·칸 `metadata`(그래프 상태의 칸이 아님)·모드 차례(02) · 첫 사건 시간·전체 걸린 시간(03, 기준점은 메서드 `stream`을 부른 때) · Ch 15 05 첫 토큰 도착 시간.
- 사실(참, 출력 근거): 모드를 목록으로 고르면 사건이 `(모드 이름, 자료)` 짝 · 여러 모드를 함께 골라도 그래프는 한 번 실행되고 모드별 사건 수는 따로 고를 때와 같음 · 모드를 고르지 않으면 `updates` · `invoke` = 마지막 `values` 사건 · 쓰기 함수는 모드 `custom`을 고르지 않으면 아무 일도 안 함 · 노드 안 `model.invoke`도 모드 `messages`를 고르면 스트림 청크로 나옴(고르지 않으면 스트리밍 요청이 아님 — 설치판 소스·노트북 밖 확인) · 사건 차례는 노드 코드가 정함(모드 목록 차례와 무관) · 체크포인터 없이도 `tasks` 사건은 나옴(문서 표와 다름).
- Ch 26 01~04 b3 「Ch25에서는 실행 사건을 스트리밍했습니다」는 **참**입니다.

### 전제하면 안 되는 것 (Ch 26 파일은 고치지 않았습니다)

1. **Ch 25는 동기 메서드 `stream`만 썼습니다(01~04).** `astream`·`async for`·`stream_events`·인자 `version="v2"`·`subgraphs=True`·`print_mode`는 0건입니다(01·02·03·04 b7 「실행하지 않았습니다」). 비동기 스트리밍은 Ch 30 04가 처음 가르칩니다.
2. **스트리밍한 그래프는 모두 작습니다** — 01 노드 둘(모델 없음, `InMemorySaver`) · 02~04 모델 노드 하나(체크포인터 없음). **여러 노드·하위 그래프·에이전트 그래프(`create_agent`)의 스트리밍, 노드 이름(칸 `metadata["langgraph_node"]`)으로 거르기, 도구 호출 스트림 청크·`ToolMessage` 사건, 서브에이전트의 스트림을 바깥으로 흘리기는 0건**입니다. 체크포인터와 모델을 함께 쓴 스트리밍도 0건입니다. 설치판 `pregel/_messages.py`는 노드가 내놓은 메시지 객체(예: `ToolMessage`)도 모드 `messages`로 보낸다고 적습니다 — **이 경우는 실행하지 않았습니다**(01 b7, 마감 A-2). 에이전트 그래프를 스트리밍하면 모델 호출이 아닌 `messages` 사건이 섞일 수 있습니다.
3. **걸린 시간은 03·04가 `time.perf_counter`로 조건마다 한 번씩만 쟀습니다.** 여러 번 재어 가운데 값·백분위수·빠르기 비교·**스트리밍하지 않은 실행과 견주기는 없습니다** — 「스트리밍이 더 빠르다」·「첫 응답 지연을 줄인다」의 근거로 Ch 25를 쓰지 말 것. **초 비교는 결론이 아닙니다.** 결론은 사건 차례·자리뿐입니다.
4. **예상 비용**은 03이 도구 파일 `estimate_cost`(Ch 6 06 — Ch 21 판 글자 그대로)로 요청 한 번만 셌습니다. 사용량이 든 스트림 청크는 OpenAI 기본 주소·기본 클라이언트일 때만 붙습니다(설치판 소스, 03 b7). Ch 25 도구 파일은 Ch 25 실습 폴더에만 있고 Ch 26 실습 폴더와 다릅니다(파일째 가져오지 말 것).
5. **모델 요청 수**는 노드 안 `model.invoke` 한 번 = 요청 한 번인 우리 그래프 값입니다(노트북 한 번 01 0 · 02 2 · 03 2 · 04 3 / 작업 전체 51). Ch 26의 「호출 수」 비교에 이 수를 그대로 쓰지 않습니다.
6. **말**: 「이벤트」·「조각」·「지연」·「측정」·「추정」·「구독」은 Ch 25 제목·슬러그 밖 0, 「TTFT」·「total」은 제목·슬러그와 03 b2·노트북 1절 풀이 밖 0. 04 소재(자료실 문의 창)를 Ch 26이 이어 쓴다는 약속은 없습니다.
7. **공용 옛 생성기 `textbook/part6/_generate_ch25_ch26.py`**(`0767052613d9…`): 01절이 **Ch 25 쪽만 건너뛰게**(머리 주석 넷 + `chapter == "ch25-streaming"`일 때 `continue` 세 곳 — 노트북·`chapter.json`·실습 폴더 `pyproject.toml`·README·`_src`·research.md·점검표·챕터 공개 목록) 했고 **Ch 26 쪽 동작은 그대로**입니다(`before/generators/` 사본과 diff는 이 줄들뿐). Ch 25 마감은 이 파일을 **옮기지 않았습니다**. **Ch 26 01절이 첫머리를 막고(`raise SystemExit` + 설명 주석), Ch 26 마감에 `mv -n`**으로 옮길 것(Ch 23·24 공용 생성기 선례 — 옮긴 자리와 부르는 스크립트 0을 `grep`으로 확인하고, Ch 25 요약·체크리스트 §2-13에 한 줄). 옮기기 전까지 이 파일을 실행하면 Ch 26 쪽을 옛 판으로 덮어씁니다.
   - **옮김(Ch 26 마감 2026-09-28)**: `textbook/part6/ch26-delegation/qa/upgrade/before/generators/blocked/_generate_ch25_ch26.py`(`mv -n`, `06fa7d9993e1…` 같음 — Ch 26 01절이 첫머리를 막은 판), 부르는 빌드·검사 스크립트 0(`grep`).

## 14. 챕터 끝 인계 요약 (Ch 26 작업자용 한 줄)

Ch 26 01~04 b3 「Ch25에서는 실행 사건을 스트리밍했습니다」는 참이지만, **Ch 25는 노드 하나짜리 작은 그래프를 동기 `stream`으로만 받았고 에이전트·서브에이전트 그래프의 스트리밍과 초 비교는 없습니다** — Ch 26이 위임 구조를 스트리밍하면 그 절이 처음 보이는 것이고, 공용 옛 생성기 `_generate_ch25_ch26.py`는 Ch 26 01절이 막고 Ch 26 마감에 옮겨 주세요.

## 15. 뒤 챕터(Ch 26·30)·전체 마감 인계 (그 챕터 파일은 고치지 않음)

| 챕터 | 자리 | 지금 글 | Ch 25 쪽 사실 | 할 일 |
|---|---|---|---|---|
| Ch 26(대기) | 01~04 `_src` b3 | 「Ch25에서는 실행 사건을 스트리밍했습니다」 | 참(01~04) | 없음 — 전제하면 안 되는 것은 §13 |
| Ch 26(대기) | 공용 옛 생성기 `_generate_ch25_ch26.py` | Ch 25 쪽 건너뜀, Ch 26 쪽 그대로 | §13-7 | Ch 26 01절이 막고 Ch 26 마감에 `mv -n` |
| **Ch 30(대기)** | **04 `_src` b2** | 「스트리밍은 중간 결과를 먼저 전달해 **첫 응답 지연을 줄이지만**」 | **Ch 25 근거 아님** — 03·04 모두 스트리밍하지 않은 실행과 걸린 시간을 견주지 않았고(마감 B-1로 03 b7·b10·노트북 7절에 밝힘), OpenAI 문서의 설명일 뿐 | Ch 30 작업 때 문서 근거로 적거나 그 절이 직접 견줌. 「지연」은 Ch 18 이후 금지어 |
| Ch 30(대기) | 01 「조각」 · 03 b3 「단일 실행과 스트리밍이 같은 실행 객체의 다른 소비 방법」 · 04·05 b3 「스트림 모드와 진행 이벤트 비교」·「진행·토큰 이벤트 분리」 · 09 b3 「`stream_mode="messages"`에서 모델 메시지 청크와 실행 메타데이터를 읽었습니다」 | — | 뜻은 참(01 6절 `invoke` == 마지막 values · 02 6절 칸 `metadata`) | 말(「조각」·「소비」·「이벤트」·「메타데이터」·한정어 없는 「청크」)은 Ch 30 몫 |
| Ch 30(대기) | Ch 25 04 b8이 가리키는 Ch 30 04·09 | 「모드 `custom`의 사건을 비동기 메서드 `astream`으로 받아 이어 붙입니다」·「모드 `messages`의 스트림 청크를 같은 메서드로 받아 서버 응답으로」 | 참(Ch 30 04 `_src` `agent.astream(input, stream_mode='custom')`·`agent_service/app.py` 134~136행) | 없음 |
| 전체 마감 | Ch 6 04 「청크」 → 「스트림 청크」 개명(`upgrade-final-checklist.md` 268행) | Ch 25 02 b3 「그 절이 청크라고 부른 답의 일부를, 이 과정은 스트림 청크라고 부릅니다」·b4 용어 표 「Ch 6 04절에서 청크라고 부른 것과 같습니다」 | 지금은 참 | **Ch 6 04 개명 때 Ch 25 02 두 문장과 「사용량 청크」(02 다섯 곳)를 함께 고칠 것**(검토 A-15) — 02 `_src`·노트북 마크다운이라 다시 실행 불필요 |
| 전체 마감 | `llm-practice.zip` 안 Ch 25 | 옛 판(노트북 셋·README, 도구 파일·04 없음, 틀린 「tasks는 체크포인터 필요」 포함) | `part6-practice.zip`은 새 판 8항목이 디스크와 같음 | 전체 묶음 재생성 때 Ch 25 8항목 대조(검토 A-17) |
| Part 6 목차 | `textbook/part6/_src/index.html` 8행 · `practice-start.md` | 「Ch 25는 처리 중인 내용을 사용자에게 보여 주고 시간을 측정합니다」 | 뜻 참(03이 잼) | 말 「측정」 — Part 6 마감 때 |
| Part 7 | `labs/part7/continuity-guide.md` 7행 | 「Ch2의 비동기 함수와 Ch25의 스트리밍」 | 둘 다 앞 챕터 사실로는 참(Ch 25는 동기만) | Ch 30 작업 때 필요하면 |
| Ch 24(완료) | 04 b8(01 슬러그·「한 실행에서 … 일곱 방식」) | — | 참 | 없음 |

- TTFT·첫 토큰을 Ch 25에 기대어 말하는 뒤 챕터 문장은 Ch 30 04 b2 하나뿐입니다(03 `grep`).

## 16. 남은 것 (전체 마감 몫 — `textbook/qa/upgrade-final-checklist.md` §2-13)

1. **옛 그림 아홉 삭제 승인**: `figures/0N-흐름.{svg,excalidraw,caption.md}`(N=1~3, 9개 — 본문 참조 0, 캡션에 「측정」·「조각」, 사본 `qa/upgrade/before/figures/`, `final-artifact-hashes.json`이 해시를 적은 기록 파일, 챕터 공개 목록 줄은 원래 없음). Part 6 옛 검사 `check_figures.py`가 `.excalidraw` 짝을 요구하는 것과 함께 정할 것.
2. **`gates-wip-*.json` 아홉 삭제 승인**(`gates-wip-01-01`·`01`·`02-02`·`02`·`03-03`·`03`·`04-04`·`04`·`ch25-after04` — `gates-after.json` 4/4로 갈음, 절 번호 넷은 마감 `run_section.sh --no-exec`가 다시 씀). `qa/upgrade/__pycache__/`·실습 폴더 `notebooks/__pycache__`는 없음(만들지 않음).
3. **캐시·임시 삭제 승인**: 실습 폴더 `labs/part6/ch25-streaming/.venv`(macOS 판 173MB) · `.cache/vm/venv-ch25-streaming`(238MB) · `.cache/ch25-0N-view/`(N=1~4) · `.cache/ch25-close/`(마감 전 사본 `pre/`·확인 스크립트 `tools/`(`gpatch.py`·`genmatch.py`·`syncmd.py`·`gcheck.py`·`bandiff.sh`·`nbhash.py`·`manifest_check.py`·`dump.py`·`ban25.py`·`extra_check.py`·`shape.py`·`astdiff.py`)·치환 목록 `reps/`·옛 검사 결과 `oldcheck/`·`dx/`(`llm-practice.zip`을 뺀 전달 검사 사본과 결과)·로그 `log/`, 14MB) · 기기 `/tmp/ch25-prep`·`/tmp/ch25-01`~`/tmp/ch25-04`·`/tmp/ch25-close-index-test.html`·`/tmp/ch25-close-src-before.txt` · `/tmp/reviewA25`·`/tmp/reviewB25`(검토 재현 파일). 기기 세션 임시 폴더 `$TMPDIR/ch25-*`는 0개.
4. **코드 쪽 다음 재실행 몫**(마감은 코드 셀을 한 글자도 바꾸지 않음): **01 셀 31 주석** 「칸 값에 관한 세 모드(values·updates·custom)」 → 「칸 값과 진행 값에 관한 세 모드」(검토 A-1, `author_01.STATE_MODES` — 01은 모델 0·결정적) · **02 셀 36 주석의 한정어 없는 「청크」 둘** → 「스트림 청크」(검토 A-12, `author_02.EMPTY` — 02 재실행은 모델 요청 2·인용 숫자·그림 대조) · 코드 줄 줄이기 후보(§12-6, 강사 결정). 다시 실행하면 새 커널 두 번 대조·교재 출력 인용 다시 대조·zip 다시 만들기.
5. **도구 파일 머리 설명**(Ch 24 `approval_tools.py`와 함께 — 전체 마감 한 항목): Ch 25 `stream_tools.py`는 01 함수 둘 기준. 고치면 `author_02.TOOLS_HEAD` → `author_02/03/04.TOOLS`·`strip_later_imports`·세 생성기 `check_*`·쓰기 가드를 함께 맞추고 zip·챕터 공개 목록 해시를 다시 적음(노트북은 다시 실행 불필요).
6. **01을 Part 6 묶음 실행 검사에 넣을 후보**(§9) — 넣으면 `check_bundle_execution.py` 목록에 `('ch25-streaming', '01-*.ipynb')`, 01 `code_sha256` `650e86fce1fa…` 계약이 생김.
7. **Part 6 옛 검사 스크립트 넷(고치지 않음, 마감에서 돌린 결과)** — 모두 Ch 25에 닿기 전에 멈춤: `check_scope.py` Ch 21 07 「실습 30분」 `Missing scope`(Ch 25 04도 같은 모양 — `EXPECTED`·`SECTION_COUNTS`) · `check_figures.py` Ch 21 `01-1-….svg`의 `.excalidraw` 짝(Ch 25 새 SVG도 짝 없음) · `check_notebook_readiness.py` `assert len(reports) == 47`(Part 6 노트북 52), **결과 파일 `notebook-readiness.json`을 먼저 씀 → 실행 전 사본으로 되돌림**(`b3d69e9c…`) · `check_visual_reports.py` `ch22-middleware`에서 멈춤.
8. **`llm-practice.zip`**: Part 6 `check_delivery.py`가 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`(117행)에서 멈춤(결과 파일 안 바뀜). 사본에서 그 zip만 빼면 HTML 63 · 링크 1,224 · 누락 0 · 절 52 · 코드 셀 807 · 복습 197문항 오류 0 · SVG 161 · 비밀값 0 · 개인 경로 0 · `part6-practice.zip` `71683e44…` 103항목(part6 노트북 52) 통과. `llm-practice.zip` 안 Ch 25는 옛 판 — 전체 묶음 재생성 때.
9. **`textbook/_notebook/build_index.py`** 절 수(Ch 25 3 — 실습 절 뺀 수, 과정 전체 약속)·전체 목차 문구 — 전체 목차 마감 때. **`textbook/part6/qa/final-artifact-hashes.json`**(Ch 25 줄 옛 판, `figures/_gen_figures.py` 옛 자리 포함). **Part 6 공용 `visual-results.json`**: Ch 25 줄은 마감에서 10줄로 새로 모음(`screens` 124), 다른 챕터 줄은 옛 HTML 해시 그대로 — Part 6 마감 때 다시 모을 것.
10. **과정 요약(누적 문서 몫)**: Ch 25 용어(§4 — 스트림 사건 ≠ Ch 22 06 「사건」 · 칸 `metadata` ≠ 상태의 칸 · 첫 사건 시간·전체 걸린 시간의 기준점 · 「비동기」는 금지어 아님)와 도구 파일 `stream_tools.py`(`3a734aeb…`, 함수 일곱)는 과정 요약에 아직 넣지 않음(Part 6 마감 오케스트레이터).
11. **옛 기록 파일**: `qa/research.md`·`research.md`(Ch 26 조사가 섞임)·`qa/ch25-technical-review.md`·`qa/authoring-checklist.md`·`qa/verification.md`·`집필점검표.md` 머리에 「개선 전 판」 표시(내용 그대로 — 뒤 둘은 끝에 마감 절) · `qa/ch25-code-output-preservation.sha256`(옛 판 해시) · `textbook/part6/qa/ch25-second-technical-review.md`·`ch25-before-technical-repair/`(Part 6 쪽 옛 기록, 보호 파일 — 고치지 않음) · `textbook/part6/qa/language/ch25-*`(옛 감사 기록) · `qa/upgrade/review-pack/`(검토에 쓴 마감 전 묶음 — 다시 만들지 않음).
12. **실습 폴더 잠금**: `pyproject.toml`·`uv.lock` 그대로. 바꿀 것 없음.
13. **2차 검토**: 두 검토의 「확인하지 못한 것」(한국어 감사 3단, 삽화 직접 판독, Windows·macOS 실제 실행, 학생 `.venv` 첫 셀)과 §12.

## 17. 검토 1차와 반영 (2026-09-25 마감)

- 판정: **A(01~02·공통) 중 2 · 하 15**(01 하 2 · 02 중 1·하 9 · 공통 중 1·하 4), **B(03~04·마감 몫) 중 4 · 하 8**(03 중 1·하 5 · 04 중 1·하 1 · 기록·마감 몫 중 2·하 2). 합 **[중] 6 · [하] 23**, [상] 0.
- **[중] 6건 모두 반영**: A-3(칸 `metadata` 구분 문장 — 02 b4 용어 표·노트북 6절, 이름 그대로) · A-13/B-10(실습 폴더 README 전체) · B-1(03 「스트리밍하지 않은 실행과 견주지 않았다」 — b7 새 항목·b10 「문서의 설명」·노트북 7절 한 문장, handoff 「§03 → 실습(04)」 1항 기록 바로잡음) · B-7(04-4 PNG를 직접 보고 그림 읽기·캡션·alt — 다시 만들지 않음) · B-11(`objectives` 넷, `hours` 그대로).
- **[하] 23건 가운데 21건 반영**: A-1(01-1 라벨·셀 30·셀 36 — 셀 31 주석은 셀 32 결과 읽기 한 문장, 다시 렌더) · A-2(b7 한 항목·b6 표·b8·정리·캡션) · A-4(02 「글자가 든 첫 스트림 청크」) · A-5(02 b6 단계 1 뺌) · A-6(02-3 라벨 — §0 규칙대로 다시 렌더) · A-7(02-2 캡션) · A-8(02 b4 근거 갈래) · A-9(`lc_versions` 한 문장 — 설치판 소스 확인) · A-10(02 복습 3 — 같은 문제 03 복습 3 「본문 4블록」도) · A-11(02-5 그림 읽기에 종 짝짓기) · A-12(02 셀 35 설명에 「청크」 한 문장 — 주석은 다음 재실행) · A-15(요약 §15 기록) · A-16(옛 기록 넷 「개선 전 판」 · `objectives` · `_build_index.py` · `build_index.py` 설명 · continuity-guide) · A-17(요약 §15·체크리스트 기록) · B-2(정의 기준점 「메서드 `stream`을 부른 때」 + Ch 15 05와의 차이 한 문장 · 04 b4 「모델 요청 전」) · B-3(0.003~0.006초 b6 → b7) · B-4(03 복습 3 인과) · B-5((나)안 — 03-3 라벨·b6 단락에서 입력 토큰 47·캐시 입력 0 뺌, 다시 렌더) · B-6(03 b7 사용량 청크 조건) · B-8(04 복습 4 「03절 노트북 9절」) · B-9(04 진단 검사 문장 317·`"yes"`/`"no"` 근거 · handoff 셋).
- **반영하지 않은 것과 까닭(2건 — 같은 항목)**: **A-14·B-12**(도구 파일 머리 설명) — 챕터 리드 결정으로 도구 파일 해시 `3a734aeb…` 고정(02·03·04 생성기 대조 사슬·zip이 이 판에 기댐, Ch 24 A-13 선례). 머리 설명은 틀린 말이 아니라 모자란 말이고, 함수마다 위 주석에 출처가 있으며 README가 함수 일곱의 배운 절·가져오는 절·`time`을 적음. Ch 24와 함께 전체 마감 한 항목(§16-5). **코드 쪽이 남은 둘**(A-1 01 셀 31 주석 · A-12 02 셀 36 주석 「청크」 둘)은 코드 셀을 한 글자도 바꾸지 않는다는 결정대로 결과 읽기·설명 셀에 한 문장씩 두고 다음 재실행 몫(§16-4). 뒤 챕터 파일 수정(Ch 30 04 b2 · Ch 6 04 개명 영향 — §15) · 삽화 다시 만들기(B-7 — 글만) · 노트북 다시 실행 · 01을 묶음 검사에 넣기(검사 스크립트 수정 금지 — 후보로 §16-6)는 과제 결정대로 하지 않음. `pack.py`로 검토 묶음 다시 만들기도 하지 않음(마감 전 묶음 보존).
- **검토의 「사람이 정해야 할 것」 처리**: A 1(코드 양)·5(`messages` = 출력 토큰 b7)·6(제목) · B 2(같은 설정 다시)·3(`"yes"`/`"no"`)·5(제목)·6(04 8절 둘째 표) → 그대로 두고 강사 확인(§12). A 2(칸 `metadata`) → 구분 문장. A 3·B 없음(도구 파일 머리) → 그대로. A 4(01 묶음 검사) → 후보. B 1(04-4) → 글만. B 4(「비동기」) → 금지어 아님(뜻 확인 — 다섯 곳 모두 `astream` 앞). B 7(03-3) → (나)안.
- **노트북 해시 전후**(`code_sha256` / `outputs_sha256`, 앞 12자 — 모두 같음): 01 `650e86fce1fa`/`5027ff86da5a` · 02 `68b434d3f859`/`2238f293d766` · 03 `ffe254e0d3c2`/`9a11da7a456d` · 04 `0c0ecd220c78`/`40744b4c3929`. `executed_at` 넷 모두 같음, `metadata.verification`과 다시 계산한 값이 같음. 파일 해시만 바뀜(01~03 마크다운·01 그림 첨부, 04는 파일도 그대로): §10 첫 줄.
- 고친 방법: `.cache/ch25-close/tools/gpatch.py`(생성기 문자열과 노트북 마크다운을 함께 — 노트북 코드 셀에 옛 글이 있거나 생성기에서 한 번이 아니면 멈춤, `reps/0N.json`) → `author_NN.py --src-only` → `genmatch.py`(셀 59·54·52·44 · `_src` 4/4 같음) → `.mmd` 고친 셋만 `render_mermaid.py --only … --force` → `run_section.sh … NN --no-exec` 네 번(01은 새 PNG 첨부). 마감이 더한 문장의 참 금지어 0, 게이트 G6 0.
- 검사: `upgrade_gates.py … --label after` **4/4 PASS, G1~G7 0** · AST 따로 금지 문법 0(허용 표시 도구 파일 `.get` 둘) · `verify.py --chapter` **PASS 4 sections / 97 code cells (max 12 lines)** · 빌드 HTML 다섯 `{{`·`[[` **0건** · `visual.cjs` **10행 PASS** · Part 6 `check_bundle_execution.py` **PASS**(Ch 24 01·Ch 28 01) · Part 6 `check_delivery.py`는 `llm-practice.zip` Part 1 Stale에서 멈춤(그 zip을 뺀 대조 통과, §16-8) · 옛 검사 넷 Ch 25 전에 멈춤(§16-7) · 보호 파일 147개 114 같음 · 32 의도한 변경 · 1 옮김.
- **전체 마감 2026-09-30: 청크 표기**(검토 A-15 · 점검표 §2-13 12번 처리) — Ch 6 04가 「스트림 청크」로 바뀌어 02 b3 「그 절이 청크라고 부른 답의 일부를, 이 과정은 스트림 청크라고 부릅니다」 → 「그 절에서 도착한 답의 일부를 스트림 청크라고 불렀습니다」, b4 용어 표 「Ch 6 04절에서 청크라고 부른 것과 같습니다」 → 「Ch 6 04절에서 본 스트림 청크와 같습니다」, 「사용량 청크」 다섯 곳(_src 둘·노트북 마크다운 셋) → 「사용량이 든 스트림 청크」(03·Ch 30 09와 같은 말). `mdpatch.py` → `author_02.py --src-only`(같은 판) → `run_section.sh … 02 --no-exec`. 셀 36 주석은 그대로(§2-13 5번). 노트북 02 해시 같음(`68b434d3f859`/`2238f293d766`). 게이트 4/4 · `verify.py` PASS 4/97.
