# 02절 진단 — 토큰과 중간 진행 스트리밍 (experiment)

- 작업일 2026-09-25. 생성기 `qa/upgrade/author_02.py`(도구 파일 + 노트북 + `_src`, `author_01`을 `import` — `sys.dont_write_bytecode`), 흔들림 확인 `02-probe.md`·`probe/probe02.py`, 그림 설계표 `02-figures.md`, 검토 묶음 `review-pack/02-토큰과-중간-진행-스트리밍.md`.
- 옛 판 사본: `before/notebooks/02-…ipynb`·`before/_src/02-*.html`·`before/figures/02-흐름.*`(준비 담당이 복사).
- 챕터 리드 결정(인계 「챕터 공통」)과 「§01 → §02」 1~12항을 따랐습니다.

## 1. 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 후(`gates-wip-02.json`, `run_section.sh … --no-exec` 마지막) |
|---|---|---|
| 코드 셀 | 4 | **25**(준비 셀 셋 — 설치·가져오기·키) |
| 검사 문장 | 81 | **340** |
| G1 | 0 | **0** |
| G2 | 2(c4 20줄 · c6 22줄) | **0** |
| G3 | 0 | **0** |
| G4 | 1(`init_chat_model(f"openai:{MODEL}", reasoning_effort="none")`에 `temperature` 없음) | **0**(`nbkit.key_and_model_cells` — `temperature=0`·`reasoning_effort="none"`) |
| G5 | 5(제목 셀·핵심 그림 없음 · 결과 읽기 없음) | **0** |
| G6 | 23(70자 초과 9 · 영문 시작 14) | **0** |
| G7 | 3(Mermaid 0 · 삽화 0 · 설계표 없음) | **0**(Mermaid 4 · 삽화 1 · 설계표) |
| 합 | **34** | **0 (PASS)** |

- 첫 실행 전 G1·G2 확인(`upgrade_gates.py … --label wip-02 --section 02`, `gates-wip-02-02.json`): G1 0 · G2 0 · G3 0 · G4 0 · G5 0 · **G6 3**(b8 다음 절 문장 70자 초과 · 준비물 판 번호 한 줄 70자 초과 · b10 `` `langgraph_node`로 ``로 시작) → 실행 전에 고침 → G1~G6 0, G7 18(그림 전). 마지막 판에서 G6 1(b7 한 문장 70자 초과 — 「스트림 청크」로 바꾸며 길어짐)을 둘로 나눠 0.
- 코드 줄(`count_code.py`, 주석·빈 줄 뺌): 02 **61 → 138**(챕터 292 → 369), 도구 파일 `stream_tools.py` 함수 둘(본문 9줄)은 따로. 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘 강사 확인 대상(§12).
- AST 따로(`/tmp/ch25-02/tools/extra_check.py` = 01 판 복사, 노트북 + 도구 파일): **0건**. 셀 모양(`shape.py`): 준비 셀이 아닌 셀 최대 **9줄**, 함수 본문 최대 **8줄**(`mode_order`, 주석 뺌), 정의 셋(상태 형식 `AnswerState` · 노드 `write_answer` · 함수 `mode_order`), 셀당 정의 하나. 호출 깊이 최대 2(`print(…, mode_order(quiet_events))`·`print(…, positions_of(…))`·`print(type(x).__name__, …)`). 부른 내장 이름 `len`·`list`·`print`·`range`·`type`뿐. `assert` 하나(4절 모드 차례 — 노드 코드가 정하는 값), 모델 글에 건 `assert` 0.
- 금지어(`/tmp/ch25-02/tools/ban25.py` = 01 판): 노트북·`_src`·캡션·`.mmd`에서 **참 금지어 0**. 걸린 것은 거짓 양성뿐 — 「체크포인터」 안 「포인터」 넷 · prompt 기록 파일 제목 「프롬프트 (1차, 채택)」·「최대 차이 0」(01과 같은 틀, 학생 묶음 밖). 「조각」 0 · 「구독」·「이벤트」·「태스크」·「지연」·「추정」·「측정」·「메타데이터」 0 · 「한 겹 더」 0.
- **한정어 없는 「청크」**: 본문·노트북 설명·캡션·`.mmd`는 모두 「스트림 청크」·「사용량 청크」로 고쳤습니다(마지막 판 `mdpatch.py` 18곳). 남은 것은 셋 — `_src` b3 「그 절이 청크라고 부른 답의 일부를, 이 과정은 스트림 청크라고 부릅니다」·b4 용어 표 「Ch 6 04절에서 청크라고 부른 것과 같습니다」(Ch 6 04 원래 이름을 가리키는 자리) · **노트북 5절 코드 셀(`EMPTY`) 첫 줄 주석** 「…스트림 청크의 차례(1부터)와 사용량이 든 청크인지 보고, 글자가 든 청크 수를 셉니다」(한 문장 안 앞에서 「스트림 청크」라 한 뒤 줄여 씀). 주석을 고치면 `code_sha256`이 바뀌어 모델 요청을 다시 보내야 하므로(규격 §3 「설명만 고칠 때 재실행 안 함」) 이번에는 두고, **다음 재실행 때 생성기 `EMPTY` 주석을 「스트림 청크」로 고칠 것**.

## 2. 수정 전 주요 문제 (옛 판)

1. 준비 셀 하나에 설치·`[Path.cwd(), *Path.cwd().parents]` 별표 풀기 키 찾기·`MODEL` 글·`cost_limit_usd` 출력이 섞임 · `init_chat_model(f"openai:{MODEL}", reasoning_effort="none")`에 **`temperature` 없음**(G4).
2. c4 20줄(상태 형식 `State`·힌트 `(state: State) -> dict[str, str]`·노드·그래프가 한 셀) · c6 22줄(`seen` 딕셔너리·`chunk, metadata = data` 대입 풀기·`"".join(preview)`·`assert A and B and C`·조각 세기) · c8 「표시 문구」 딕셔너리(사건을 받지 않는 셀).
3. **「조각」 23번**(본문 18·노트북 4·출력 라벨 「내용이 있는 조각 수」) — Ch 5 토큰 전용 말. b4 「토큰 스트리밍 … 메시지 조각」이 「토큰 = 스트림 청크」로 읽힘.
4. `metadata`를 풀기만 하고 읽지 않음 → Ch 30 09 b3 「실행 메타데이터를 읽었습니다」 부분 참.
5. messages 사건 수 88·내용 있는 조각 84를 결론·복습(「88개인데 84개인 까닭」)에 씀 — 옛 기록마다 71·73·88로 흔들린 값.
6. b3 「Ch24에서 interrupt와 재개 사건」(세 절 같은 글, Ch 24에 스트림 사건 0) · b7 「messages의 metadata로 노드 이름과 호출을 필터링할 수 있습니다」·「중앙값과 상위 백분위수」(실행 안 한 권고) · b5 「예상 API 비용은 1달러 미만」(근거 없음) · 금지어(반환·지연·로그·도메인·재개·측정·명시·필터링·TTFT·total·first_event) · 결과 읽기 0 · 옛 그림 토큰 `{{svg:02-흐름}}`.

## 3. 바꾼 것 (결정)

- **실제 모델 첫 절(결정 1)**: 준비 셀 = 설치(`langchain==1.4.0`·`langchain-openai==1.6.0`·`langgraph==1.2.11`·`python-dotenv==1.2.3`, 체크포인터를 안 써 `langgraph-checkpoint` 줄 없음) → 가져오기(`TypedDict`·`init_chat_model`·`StateGraph, START, END`·`get_stream_writer`·`from stream_tools import collect_events, positions_of`) → `nbkit.key_and_model_cells("openai:gpt-5.4-mini")`(결과 읽기에 실행일·「실행마다 답 문장이 달라질 수 있습니다」·「요청은 아직 보내지 않습니다」를 붙인 판).
- **그래프**: 상태 형식 `AnswerState`(칸 `question`·`answer` — 01과 칸이 달라 새 이름) · 시스템 메시지 글 셀 · 노드 `write_answer`(`writer = get_stream_writer()` 다음 줄 `writer({"stage": "before_model", "progress": 30})` → `model.invoke([("system", …), ("user", …)])` → 진행 값 100 → `{"answer": response.text}`, 힌트·f-string·노드 안 `assert`·전역 목록 없음) · 체크포인터 없이 컴파일(설정 `None`, 01 8절과 같음). 입력은 01 소재 「배송 문의」를 잇는 질문 「주문한 책이 아직 오지 않았어요. 언제 받을 수 있나요?」(흔들림 확인 전에 정함, 결과를 보고 바꾸지 않음).
- **세 모드를 한 실행에서 함께 받기(결정 3)**: `["messages", "updates", "custom"]` · `collect_events`(도구 파일) · 모드별 수(`positions_of`) · **새 함수 `mode_order`**(같은 모드가 이어지면 한 번만 적는 「모드 차례」, 이 절에서 처음 가르쳐 노트북에 둠) · 자리·custom과 updates 자료 · 스트림 청크 모양(`tuple 2`·`AIMessageChunk`·`dict`) · 글자가 없는 스트림 청크(첫 청크 + 끝 셋, 끝에서 둘째만 사용량) · **칸 `metadata`**(키 열둘·`langgraph_node`·`langgraph_step`·`ls_model_name`·`ls_temperature`, 모든 청크의 노드 이름) · 이어 붙인 글 == 답 글(`+`로, `join` 없음) · 답 글·글자 수 · 합친 객체의 사용량(Ch 6 04 모양) · **값 바꿔 보기** `["updates", "custom"]`(사건 3·차례 `['custom', 'updates']`·자리 `[1, 2]`·`[3]`) · 두 실행 견주기.
- **결론은 실행마다 같은 값에만(결정 2·§2-7 9번 끝)**: 모드 차례 `['custom', 'messages', 'custom', 'updates']`(assert) · `updates | 1`·`custom | 2` · 진행 값 30이 첫 사건 · 갱신이 마지막 사건 · `langgraph_node` `write_answer` · 이어 붙인 글 == 답 글 `True` · 두 모드 실행 사건 셋. 흔들리는 값(사건 수·청크 수·글자가 든 청크 수·custom 둘째 자리·updates 자리·답 글·글자 수·토큰)은 결과 읽기 둘째 단락(「이번 실행에서는」)·b6 표(「교재 출력」 열)·「확인할 점」·b7에만. 둘째 단락 값은 `[[READ_…]]` 자리 표시로 두었다가 교재 출력(A) 뒤 `mdpatch.py`로 채움(`/tmp/ch25-02/reps-A.json`).
- **`_should_stream`(인계 7·결정)**: 8절 결과 읽기·b4·b7에 설치판 소스(langchain-core 1.6.2 `language_models/chat_models.py` 549~585행·1969행, langgraph `pregel/_messages.py` 49행)와 노트북 밖 확인(§4)을 적고 「노트북에서는 요청 종류를 확인하지 않았습니다」.
- **용어**: 「조각」 23곳 → 「스트림 청크」·「글자가 든 스트림 청크」 · 새 말 셋 — 스트림 청크(이 챕터 첫 정의, Ch 6 04 「청크」와 같은 것) · 칸 `metadata`(「메타데이터」 금지 → 「칸 `metadata`」, 편지 봉투 뒷면 비유) · 모드 차례(버스 창밖 비유). 제목 「토큰과 중간 진행 스트리밍」의 「토큰」은 제목에 두고 b2·노트북 1·5절에서 「받는 단위는 토큰이 아니라 스트림 청크」로 풂(강사 확인). 「구독」 대신 「함께 받는다」, 「시스템 프롬프트」·「지시」 대신 「시스템 메시지 글」.
- **b3**: 옛 「Ch23 … thread_id」·「Ch24에서 interrupt와 재개 사건」 문장을 뺌(02는 체크포인터·멈춤 표시를 쓰지 않음) → 01절(스트림 모드·진행 값·함수 둘)·Ch 6 04(청크·사용량 청크·`+` 합치기)·Ch 5 01(토큰)·Ch 6 01(모델 설정)·Ch 13 01로 이음.
- **도구 파일(결정 4)**: §6.
- **그림**: Mermaid 4 + 삽화 1(§7). 옛 `figures/02-흐름.*` 셋은 그대로(본문 참조 0 — 챕터 마감 삭제 승인 목록).
- **b10 참고 자료**: Streaming 문서(2026-09-25 WebFetch — 「The streamed output from `messages` mode is a tuple `(message_chunk, metadata)`」·「message events are emitted even when the LLM is run using .invoke rather than .stream」·「filter the outputs by the `langgraph_node` field」·모드 표 messages 「2-tuples of (LLM token, metadata)」) · 설치판 소스 행 · Ch 6 04·01절.

## 4. 흔들림 확인 (규격 §2-7 10번 끝, `02-probe.md`)

- 판단 규칙을 첫 요청 전(17:58Z)에 `02-probe.md` §0에 적고, 노트북 밖에서 **M3(세 모드) 5번 · M2(messages 뺌) 5번 = 요청 10번**.
- M3: 결정적 후보(모드 차례·updates 1·custom 2와 값·custom 첫 자리 1·updates 맨 끝·`langgraph_node`·청크 자료형·이어 붙인 글 == 답 글) **5/5 같음**, `metadata` 키 열둘·`langgraph_step` 1·`ls_*`·글자 없는 청크 넷(첫 + 끝 셋)·사용량 청크 1·입력 토큰 47도 5/5. **흔들린 값**: messages 사건 41·41·50·34·41, 글자가 든 청크 37·37·46·30·37, 답 글(다섯 가운데 셋 같은 글, 한 번 두 줄), 출력 토큰.
- M2: 사건 3·차례 `['custom', 'updates']`·**평범한 콜백의 새 청크 알림 0회** 5/5 → `_should_stream` 문장의 근거(콜백 방법은 서비스 요청 없이 조사 전용 가짜 모델로 먼저 확인 — `counter_check.py`, 교재에 넣지 않음).
- 판단: **입력 그대로**, 결정적 값만 결론·그림. 원하는 값을 고르려고 다시 실행하지 않았습니다(노트북은 T·B·A 세 번만, §5).

## 5. 새 커널 실행 (모델 요청 노트북 한 번에 2번)

| 실행 | 어디서 | 시각(UTC) | 결과 |
|---|---|---|---|
| T | 사본 `/tmp/ch25-02/T/`(`execute.py`, 키는 기본 작업 폴더에서 루트 `.env`, `PYTHONPATH=사본`) — 실습 폴더에 `.failure.json`이 남지 않게 먼저 | 18:10:35~18:10:42 | PASS 25셀 |
| B | 사본 `/tmp/ch25-02/B/` — **그림을 그리기 전** 두 번째 새 커널 | 18:10:52~18:10:57 | PASS 25셀, T와 셀별 출력 **25/25 같음**(`outputs_sha256` 둘 다 `7ab4b07f8699…`) |
| **A(교재 출력)** | `run_section.sh … 02`(실습 폴더, 그림 뒤) | 18:14:39~18:14:46 | PASS 25셀, B와 **17/25 같음** |

- `code_sha256` 세 번 모두 **`68b434d3f859241f3917ccb2c06c19129a8f95103684a6736916d1e80e97efda`**. A `outputs_sha256` **`2238f293d7668e7b6f324b295eb3b0974d043ddbe3532ffe651f5b6bd34f3477`**. 노트북 파일 `74e56120e2ee…`(A + 그림 첨부 + `mdpatch` 설명 셀).
- **A와 B가 갈린 셀 여덟**(모두 모델의 답에 걸린 값 — T·B는 우연히 같은 답): 3절 실행(`받은 사건 수` 37 → 43) · 3절 표(`messages` 34 → 40) · 4절 자리(`[1, 36]`·`[37]` → `[1, 42]`·`[43]`) · 5절 청크 수(34 → 40) · 5절 빈 청크 자리(32·33·34 → 38·39·40, 글자가 든 청크 30 → 36) · 7절 답 글(한 줄 56자 → 두 줄 68자) · 7절 출력 토큰(34 → 40) · 8절 견주기 `messages` 줄. **같았던 열일곱**: 설치·가져오기·키·모델 · 상태 형식·시스템 메시지 글·노드·그래프·`mode_order` 정의 · 4절 모드 차례·custom과 updates 자료 · 5절 첫 청크 모양 · 6절 `metadata` 키 열둘(순서까지)·값 넷·노드 이름 · 7절 이어 붙인 글 == 답 글 `True` · 8절 두 모드 실행. 3절 실행 셀의 `첫 사건의 모드 이름`·`첫 사건의 자료`, 7절 합친 객체 종류·입력 토큰 47은 갈린 셀 안에서도 세 번 같았습니다.
- 결과 읽기 첫 단락·결론·그림은 세 번 모두 같았던 값만, 둘째 단락과 b6 표는 A 값(「이번 실행에서는」·「교재 출력」). b6 본문은 「새 커널로 세 번 실행해 견주자 … 셀 여덟은 실행에 따라 달랐습니다」로만 적고, 다른 실행의 값은 싣지 않았습니다(제작 이력 금지).
- 가상환경 `.cache/vm/venv-ch25-streaming` 그대로 — 설치 0. 걸린 시간은 재지 않았습니다(03 몫).

## 6. 도구 파일 `labs/part6/ch25-streaming/notebooks/stream_tools.py` (이 절이 처음 만듦)

- 함수 둘 `collect_events(graph_to_run, graph_input, config, modes)`·`positions_of(events, mode)` — 01절 노트북 4절 셀 글(첫 줄 설명 주석 + 본문)을 **글자 그대로** 옮기고 머리줄 `# Ch 25 01절에서 배웠습니다 — 01절 노트북 4절의 같은 이름 함수를 옮겼습니다`. `check_same_as_01()`이 01 노트북(교재 출력 판 `723a4a14824f…`)의 코드 셀 글에 두 정의가 그대로 있는지·AST가 같은지 확인. `import` 0. 머리 독스트링에 앞 챕터 도구 파일을 파일째 가져오지 않은 까닭(numpy·SQLite 체크포인터).
- 해시 **`dfea09bc3644416fb799501d28e1e33a0b1d945d1a3a796faee97dfddda64185`**(39줄). 생성기는 파일이 없거나 이 판과 같을 때만 쓰고, 03이 함수를 더한 긴 판(이 판으로 시작)이면 건너뜀(Ch 24 마감 A-10 선례).
- 준비 셀에 가져오기 한 줄(알파벳 순) + 결과 읽기에 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야…」 + 교재 출력 실행 도구 한 문장.
- **묶음 목록**: 챕터 `qa/public-files.json` 8 → 9줄(`d728ac4f…` → `bbfdade37e95e1b1df315cfe78d35bbec33720d2d234ff06def51615d347bd5d`) → `python3 textbook/part6/qa/collect_public_files.py`(`Explicit public files: 83; prerequisites: 13`, 먼저 `/tmp` 사본으로 돌려 한 줄만 늘어남을 확인) → `textbook/part6/public-files.json` 한 줄 더함(`7c9cb35e3374…` → `b12a39212fbc3bb138c103f5081c85d7767e30eee2665650f5a8fe6c758c6e9f`), `prerequisite-files.json` 바이트 같음(`4c7f5a4b…`). **zip(`part6-practice.zip`·`llm-practice.zip`)은 다시 만들지 않음**(챕터 마감 몫 — Ch 21~24 선례, `check_delivery.py`도 마감에).
- 앞 챕터 함수(Ch 6 06 `estimate_cost`·Ch 19 `sum_usage`)는 이 절이 쓰지 않아 옮기지 않았습니다(준비물 예상 비용은 문장으로만 — 요금표 어림 0.001달러 아래).

## 7. 그림 (`02-figures.md`)

- Mermaid 넷: 02-1 한 실행에서 함께 받은 세 모드(547) · 02-2 사건이 나온 차례(245) · 02-3 스트림 청크와 칸 metadata(576) · 02-4 모드 messages를 뺀 실행(646) — 괄호는 원본 viewBox 폭, 모두 868 이하. 첫 렌더 뒤 02-4(줄 꺾임 넷)·02-3(한 줄 꺾임, 한정어 없는 「청크」) 고쳐 다시 렌더, PNG 넷 직접 확인. 색: 모델 보라 하나(02-1, 실제로 부른 `gpt-5.4-mini`) · 입력 초록 · 노드 파랑 · 출력 노랑 · `graph.stream`·두 실행 공통·소스로만 확인한 동작 회색 · **빨강 0**. 라벨 숫자는 `30`·`100`·`5.4`·`1`뿐(출력에 있음), 개수는 한글, 흔들린 값 없음.
- 삽화 02-5 홈통 끝 물방울과 기우는 대나무 통: **1차 job `d0559a2f-890b-4c5f-8c53-170f13bf922f` 채택**(재생성 0), 거래 2026-09-25T18:12:32Z 「Nano Banana Pro −2」 한 줄 = **이 절 몫 2크레딧**(생성 전 잔액 2421.75, 바로 앞 거래 17:42:24Z는 01절). 원본 `3cd041c6…`(2752×1536) → 저장 PNG 1100×614 `dce82711…`, 결과 URL 다시 받아 같은 폭으로 줄인 그림과 픽셀 대조 bbox `None`·최대 차이 0. 저장 PNG와 같은 사본을 직접 열고 오른쪽을 잘라 크게 다시 봐 종 둘·물방울 일곱·기우는 통 하나를 셌습니다(받침돌 아래가 그림 가장자리에서 잘림 — 관계 판독에 영향 없어 채택).

## 8. 서비스 요청과 예상 비용

| 무엇 | 요청 |
|---|---|
| 흔들림 확인 M3·M2 | 10 |
| 새 커널 T · B · A(각 2) | 6 |
| **합** | **16**(임베딩 0, 오류 0) |

- 요금표(2026-09-17, 100만 토큰당 mini 입력 0.75·출력 4.50달러)로 어림하면 요청당 입력 47토큰·출력 약 34~50토큰 → 요청당 약 0.0002~0.0003달러, **합 약 0.004달러**(예상 비용, 청구 금액 아님). 노트북 한 번은 2요청으로 0.001달러 아래(준비물·b5 문장).

## 9. 라이브러리 확인 (2026-09-25)

- 설치판 langchain-core 1.6.2 `language_models/chat_models.py` 549~585행 `_should_stream`(스트리밍 콜백 `_StreamingCallbackHandler`가 붙었을 때 참) · 1969~2016행(스트리밍 경로에서 청크마다 `on_llm_new_token`, 마지막 빈 청크 `chunk_position="last"`) · langgraph 1.2.11 `pregel/_messages.py` 49행 `StreamMessagesHandler(BaseCallbackHandler, _StreamingCallbackHandler)` · 130~149행 `on_chat_model_start`(메타데이터를 run id로 기억) · 151~164행 `on_llm_new_token` → `(청크, metadata)` · 166~176행 `on_llm_end`(같은 id면 다시 내보내지 않음).
- 공식 문서(§3 b10 인용). 문서 표는 messages 앞 값을 「LLM token」이라 적지만 받은 값은 `AIMessageChunk` → b7에 한 줄.

## 10. 완료·대기 챕터 문장 대조 (고치지 않음)

- **Ch 30 09 b3** 「Ch25에서는 `stream_mode="messages"`에서 모델 메시지 청크와 실행 메타데이터를 읽었습니다」 → **이제 참**(02 6절이 칸 `metadata`의 키·`langgraph_node`·`langgraph_step`·`ls_model_name`·`ls_temperature`를 읽음). 말 「메타데이터」·한정어 없는 「청크」는 Ch 30 몫.
- Ch 30 09 b4 「Ch21에서 만든 Agent와 Ch25의 모델 스트림」 → 참(모델 노드 스트림). 에이전트 그래프(`create_agent`) 스트리밍은 Ch 25가 하지 않음.
- **Ch 30 05 b3** 「Ch25에서 진행 이벤트와 토큰 이벤트를 분리했습니다」 → 참(02가 한 실행에서 `custom`과 `messages`를 모드 이름으로 가름). 말 「이벤트」는 Ch 30 몫.
- Ch 30 04 b3 「스트림 모드와 진행 이벤트를 비교」 → 참(01·02). Ch 30 03 「단일 실행과 스트리밍이 같은 실행 객체의 다른 소비 방법」 → 01 6절로 참(02는 바꾸지 않음). Ch 30 01 「결과가 조각으로 이어질 수 있음」 → 뜻은 참(02 7절 이어 붙이기), 「조각」은 Ch 30 몫.
- Ch 26 01~04 b3 「Ch25에서는 실행 사건을 스트리밍했습니다」 → 참.
- Ch 30 `agent_service/app.py` `async for message, metadata in runtime.astream(…, stream_mode="messages")` → 02의 `(스트림 청크, 칸 metadata)` 짝과 같은 모양(Ch 25는 동기 `stream`만).
- `labs/part6/continuity-guide.md` 11행 「Ch2의 비동기 실행」(02도 동기만 — 부분 참)·「지연 시간」(03 몫) → 마감 몫 그대로.

## 11. 챕터 밖 수정

| 파일 | 전 → 후 | 까닭 |
|---|---|---|
| `textbook/part6/public-files.json` | `7c9cb35e3374` → `b12a39212fbc` | `collect_public_files.py`로 다시 모음(도구 파일 한 줄) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch25-streaming.json` | `22d280f95bf0` → `bb84d87808b3` | `verify.py --chapter`가 다시 씀(`run_section.sh`) |

- 실습 폴더(챕터 몫): 02 노트북(`f4f74415…` → `74e56120e2ee…`) · **새 파일** `notebooks/stream_tools.py`. README·`pyproject.toml`·`uv.lock`·01·03 노트북 그대로.

## 12. 강사 확인 대상

1. 제목 말 「토큰」(제목에만, 본문은 「받는 단위는 토큰이 아니라 스트림 청크」로 풂) — 슬러그 그대로.
2. 코드 줄 61 → 138·코드 셀 4 → 25 — 청크 모양·빈 청크·칸 `metadata`·이어 붙이기·값 바꿔 보기를 모두 출력으로 보이느라 늘었습니다. 6절 셀 셋(키·값·노드 이름)을 줄일지.
3. 칸 `metadata`라는 부름(짝의 뒤 값을 「칸」으로 — 챕터 리드 결정) · 새 말 「모드 차례」.
4. b7의 노트북 밖 값(messages 사건 34~50개, 새 청크 알림 0회)과 「messages 사건 수 = 출력 토큰 수」(교재 출력·밖 다섯 번 모두, 까닭 확인 안 함 — Ch 6 04 교재 출력은 18 ↔ 17로 달랐음)를 본문에 둔 것.
5. 준비물의 예상 비용을 노트북에서 계산하지 않고 문장(요금표 어림 0.001달러 아래)으로만 둔 것 — `estimate_cost`는 03이 비용을 보일 때 도구 파일로.
6. 노트북 5절 코드 주석의 줄인 「청크」 둘(§1, 다음 재실행 때 고침).
7. 삽화의 받침돌 아래가 그림 가장자리에서 잘림.

## 13. 남은 것과 지우지 않은 것

- 다음 절 인계는 `handoff.md` 「§02 → §03」.
- **지워야 하지만 지우지 않은 것(삭제 승인 대상)**: `qa/upgrade/gates-wip-02-02.json`·`gates-wip-02.json`(마감 `gates-after.json`으로 갈음) · `.cache/ch25-02-view/`(Mermaid PNG 사본 넷·삽화 1100 사본·잘라 본 `crop-right.png`) · 기기 `/tmp/ch25-02/`(`T/`·`B/` 노트북·도구 파일 사본 · `probe/`(`counter_check.py`·JSONL 원본 둘) · `illu/`(원본·다시 받은 원본·1100 판·잘라 본 그림) · `tools/`(01 판 복사 다섯 + `stream_tools.py` 사본) · `reps-A~D.json` · `collect_dry.py`·`public-files.json`·`prerequisite-files.json`(목록 모으기 사본 실행 결과)). 옛 그림 `figures/02-흐름.{svg,excalidraw,caption.md}`는 챕터 마감의 삭제 승인 목록.
- `qa/upgrade/probe/`(`probe02.py`·`probe-02-{M3,M2}.jsonl`)는 흔들림 확인 기록이라 남김(학생 묶음 밖, 키 값 없음). `qa/upgrade/__pycache__`·실습 폴더 `notebooks/__pycache__`는 만들지 않음.

## 마감 반영 (2026-09-25, 검토 1차)

검토 `review-round1-A.md`의 02절 몫 [중] 1(A-3)·[하] 9(A-4~A-12)를 반영했습니다. **노트북은 다시 실행하지 않았습니다**(모델 요청 0) — `code_sha256` `68b434d3f859…`·`outputs_sha256` `2238f293d766…`·`executed_at` 18:14:45Z 그대로(파일 `74e56120…` → `e4068dbd…`, 마크다운만). 방법은 01과 같음(`gpatch.py` → `author_02.py --src-only` → `genmatch.py` 54셀 같음 → `render_mermaid.py --only 02-3 --force` → `run_section.sh … 02 --no-exec`).

- **A-3 칸 `metadata`**(이름 그대로 — 바꾸면 02 재실행·도구 파일 주석·생성기 사슬): b4 용어 표 그 칸 끝과 노트북 6절 첫 설명에 「이름에 칸이 붙었지만 그래프 상태의 칸이 아니라, 사건 짝의 둘째 값입니다」(노트북은 「상태 형식의 칸(`question`·`answer`)이 아니라」). 강사 확인 대상.
- **A-4**: b8·노트북 정리 끝 「첫 스트림 청크」 → 「글자가 든 첫 스트림 청크」.
- **A-5**: b6 「모든 스트림 청크의 칸 `metadata`에는 노드 이름 `write_answer`와 단계 1」 → 노드 이름만(단계 번호는 첫 스트림 청크 하나에서만 출력했고, `02-probe.md` §0 규칙상 결론·그림 밖 값 — 노트북 6절 결과 읽기에만 남김).
- **A-6 그림 02-3**: 라벨 「키 열둘」·「langgraph_step 1」을 빼고 「첫 스트림 청크의 langgraph_node write_answer」로(§0 규칙을 뒤에서 바꾸지 않음, 다시 렌더 — `02-figures.md` 마감 반영).
- **A-7 캡션 02-2**: 「두 번 실행해도 같았습니다」 → 「새 커널 세 번과 노트북 밖 다섯 번에서 모두 같았습니다」(두 문장).
- **A-8**: b4 요청 종류 문장 뒤 「노트북에서는 요청 종류를 확인하지 않았고, 이 차이는 설치판 소스와 노트북 밖 확인으로 본 것입니다」.
- **A-9 `lc_versions`**: 설치판 `langchain_core/language_models/base.py` 222~290행(`model_post_init`·`_add_version` — 설치한 langchain-core·langchain·파트너 패키지 판 번호를 모음)을 읽고, 노트북 6절 결과 읽기 첫 단락에 「설치판 소스를 보면 키 `lc_versions`에는 설치한 LangChain 패키지의 판 번호가 담기고, 이 절에서는 값을 읽지 않습니다」(단락 다섯 문장을 넘지 않게 `checkpoint_ns` 두 문장을 한 문장으로).
- **A-10**: 복습 3 「본문 7블록」 → 「본문 「주의할 점과 실무 메모」」.
- **A-11 종 비유**: 삽화 02-5를 기기에서 직접 봄(왼쪽 종 = 첫 받침 왼쪽, 오른쪽 종 = 둘째 받침 오른쪽, 둘 다 홈통 끝보다 앞). 그림 읽기 넷째·다섯째 문장을 「…왼쪽 종이 진행 값 30, 오른쪽 종이 진행 값 100입니다. 두 종의 자리는 울리는 차례를 나타내지 않고, …」로, alt에 두 종의 자리. 01 용어 표의 부엌 예는 그대로(강사 판단).
- **A-12**: 5절 코드 주석의 한정어 없는 「청크」 둘은 코드라 그대로, 앞 설명 셀(셀 35 「다음 셀은 …」 단락)에 「셀 주석의 「청크」는 모두 스트림 청크를 줄여 쓴 말입니다」 한 문장 — 주석 고침은 **다음 재실행 몫**(`author_02.EMPTY`).
- **b7 「사건 수 = 출력 토큰 수」**(검토 A 「사람이 정해야 할 것」 5): `02-probe.md` §1(다섯 번 41·41·50·34·41 = 출력 토큰)과 교재 출력(40·40)이 근거라 「노트북 밖 다섯 번」 표시와 함께 두고, 끝에 「그래서 스트림 청크 수를 토큰 수로 읽지 않습니다」(노트북 7절 결과 읽기와 같은 결론)를 더함.
- 게이트 02: G1~G7 0(코드 셀 25, 검사 문장 340 → **344**). 마감이 더한 문장의 새 금지어 걸림 0.
