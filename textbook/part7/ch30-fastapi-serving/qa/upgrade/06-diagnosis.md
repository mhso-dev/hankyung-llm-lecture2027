# 06절 진단 — fetch 재연결과 오류 이벤트 (paired)

- 작업일: 2026-09-29 · 작업자: 06절 작업자 · 생성기 `qa/upgrade/author_06.py`(`b4cc80fd…` — 마지막 `mdpatch` 뒤)
- 읽은 것: `handoff.md`(머리·챕터 공통 전부·§05 → §06 전부, §01~§04 인계 훑음) · 준비 노트 `chapter-lead-notes.md`(§2 06·§3·§5-3·§5-4·§7-1~7-6) · `05-diagnosis.md` · `05-figures.md` · `author_01.py`(`FIND_LAB`)·`author_02.py`(재정의 paired·`DEF_ZERO`)·`author_04.py`(도구 파일 첫 판·대조 사슬·`DEF_JOIN`)·`author_05.py`(전부 — `DEF_SPLIT`·`DEF_PARSE`) · Ch 28 `author_02.py`(기록기 수준 선례)·`author_03.py`(자식 프로세스 정리 — 노트북 밖 TS 시험에만 씀) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 규격 전부 · 과정 요약(§1 Ch 23·24·28 줄, §2-14·2-15·2-19, §5, §7) · Ch 24 01·Ch 23 01·06 `_src`(멱등성·노드 다시 실행·스레드) · Ch 31 `_src` 제목 다섯 · 옛 06 `_src`·노트북·옛 07 노트북·`_src`(`before/`). `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 후(`gates-wip-06.json`) |
|---|---|---|
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 1 · 1 · 5 · 0 · 6 · 9 · 3 = **25** | **0 · 0 · 0 · 0 · 0 · 0 · 0** |
| 코드 셀 · 코드 줄(주석·빈 줄·`%` 줄 뺌, `extra_check.py`) | 5 · 32 | **26 · 151** |
| 검사 문장 | 84 | **428** |

- 첫 실행 전 `upgrade_gates.py … --label wip-06 --section 06`: G1·G2 **0**(첫 판에서 호출 깊이 3인 줄 셋 — `print(…, len(split_sse(…)))` 모양 — 을 AST로 먼저 잡아 변수로 나눔), G6 7(70자 넘는 문장 둘·영문 시작 셋·「되돌립니다」 둘 — 게이트 금지 「돌립니다」에 걸림 → 「재정의 딕셔너리를 비웁니다」) → 고친 뒤 G6 0. 그림 뒤 「그림 읽기 —」 머리 때문에 70자 넘은 한 문장을 나눔.
- AST 따로(`/tmp/ch30-06/tools/extra_check.py` — 05 도구 그대로): 걸린 것은 **챕터 허용 범위뿐** — 셀 맨 위 `await` 하나(코드 셀 [21], 재정의 함수 `zero_timeout`의 값 보기 — 02 모양) · 도구 파일의 `async def zero_timeout`(02 함수 그대로). f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`while`·`try`·별표 풀기·대입 풀기(for 포함)·`+=`·기본값 매개변수·힌트·클래스·데코레이터·가짜 에이전트·`asyncio`·`join`·딕셔너리 `.get`·`.items` **0**. 호출 깊이 최대 **2** · 준비 셀 밖 셀 최대 **9줄**(코드 셀 [18] 값 셋 반복) · 함수 본문 최대 **5줄**(`last_event_id`·`token_values`, 주석 뺌) · 셀당 정의 하나.
- 금지어(`/tmp/ch30-06/tools/ban30.py` — `_src`·노트북 마크다운·코드 주석·`.mmd`·캡션·alt): 걸린 것은 **허용한 것과 거짓 양성뿐** — 「노드」(Ch 13 말, 03~05와 같음 — 「노드가 낱말마다 공백」·「Ch 24 01절의 노드」) · 「이벤트」(제목 풀이 「제목의 오류 이벤트는 …」 `_src` 한 번·노트북 한 번 + 노트북 제목 셀) · 「토큰」(「접근 토큰」) · 「로그」(「프로그램」). 도구 파일 머리 글의 「서빙」·「Agent」는 04 판 머리(챕터 제목) 그대로. 「재연결」·「식별자」·「헤더」·「멱등」(단독)·「중단」(코드 백틱 출력 밖)·「조각」·「반환」·「검증」·「지연」·「결정적」·「돌려」·사용자가 금지한 표현·「쉽게·간단히·당연히」·「Agent」(본문) **0**.

## 수정 전 주요 문제 (옛 판 — `before/notebooks/06-…ipynb`·`before/_src/06-*.html`)

1. 준비 셀이 루트 커널에서 멈춤(`next((p for p in (start, *start.parents) …), None)` + `os.chdir`) — 01~05와 같은 문제. `{**auth, 'Last-Event-ID': …}` 딕셔너리 풀기 · `re.findall` · 첫 줄 주석·결과 읽기 0.
2. **Before가 결함 장면이 아님**: 「오류」 글자 질문 → 200 + `event: error`는 **앱이 일부러 던지는 예외**(`agent.py` 18~19행 — 실패 흉내), After는 `'event: error' in text`·`'stream_failed' in text`를 `assert`할 뿐 고친 것 없음. **저장 출력에 `logger.exception` Traceback**(옛 07에는 `/var/folders/…`까지).
3. b4 「안정적인 재연결은 … Ch31에서 실행과 이벤트를 저장하면 동일 이벤트를 재생할 수 있습니다」(거짓 — Ch 31은 사건 저장을 다루지 않음) · b3 「Ch23의 thread 분리와 Ch24의 중복 실행 방지 원칙을 브라우저 경계에 적용」(앱은 체크포인터를 쓰지 않음 — 한정 없음) · 본문이 `client/stream.ts`를 언급만(코드·실행 근거 없음) · b4 「서비스 설계 판단」(지수 백오프·무작위 지연·작업 식별자 — 실행 안 한 설명) · 도식 읽기 틀 색 문장(「보라색 상자는 Agent 실행」 — 모델 없는 절).
4. 「이벤트」 14·「재연결」 7·「헤더」·「식별자」·「멱등」·「조각」·「버퍼」·「청크」 · 복습 넷(해설 한 줄) · b8이 학습 목표 되풀이 · 참고 자료 셋(확인 2026-09-11, 설명 없음).

## 바꾼 것

- **05 b8 조건(handoff §05 → §06 1)**: 「06절에서는 끊긴 뒤 사건 번호로 이어 받는 방법과, 오류 사건 `error`를 봅니다. 브라우저 쪽 함수 `fetch`가 SSE 사건을 읽는 모양도 봅니다」 → **참**. 2절 첫 응답 SSE 사건 일곱 → 3절 `Last-Event-ID` 이어 받기 → 4절 TS `client/stream.ts` 11~30행 읽기(함수 `fetch`) → 5·6절 오류 사건.
- **paired Before = 실제 조건의 결함(handoff §05 → §06 2)**: 도구 파일의 `zero_timeout`(02 함수)으로 `get_timeout` 재정의 → POST(같은 질문·`sse-1`) → **같은 셀에서 `app.dependency_overrides.clear()`**(02 교훈 — `비운 뒤 재정의 딕셔너리의 키 수: 0`) → `상태 코드: 200`·`본문 종류: text/event-stream; charset=utf-8` → Before 판정 `status_says_ok` → **`상태 코드만 본 판정(성공인가): True`**(받은 결함 결과 — 빨강) · 실제 사건 `['error']`·`받은 token 사건 수: 0` · 오류 사건 칸 `['event', 'data']`(id 없음)·`{'code': 'stream_failed', …}` ↔ After `ended_with_done` → `0초 응답 | True | False`·`첫 응답 | True | True`. 0초 취소 자리는 설치판 Python 3.12.13 `asyncio/timeouts.py` 68~69·112~115행, 상태 코드를 먼저 보내는 자리는 starlette 1.6.0 `responses.py` 248~255행(본문에 밝힘).
- **값 바꿔 보기(한계, 빨강 0)**: `Last-Event-ID`만 범위 밖 `sse-1:99` → 200·`['done']`·After `True`·token 0 — 앱이 범위를 검사하지 않아 After 판정도 못 가림(3절 `sse-1:5` → `done`만과 받는 쪽 모양이 같음).
- **예시 부분 — 이어 받기의 실제 모양(handoff §05 → §06 3)**: 앞 사건 둘을 받은 것으로 봄(**연결을 실제로 끊지 않음** — 시험용 클라이언트는 본문을 끝까지 모아 주므로 첫 응답 목록의 앞 둘을 씀, 본문·노트북에 밝힘) → `last_event_id` → `sse-1:1` → 앱 41~53행 출력(`Header(alias="Last-Event-ID")`·400 둘·`+ 1`) → `Last-Event-ID: sse-1:1`로 다시 → `sse-1:2`부터 넷 + `done` → `join_tokens`로 이어 붙인 글 = 첫 응답 글 `True` → 앱 107~117행 출력(자리 0부터 세며 건너뜀 — **서버가 그래프를 처음부터 다시 실행**, 모델 그래프면 다시 만든 글이 달라질 수 있음은 「노트북에서는 그런 그래프로 실행하지 않았습니다」) → 요청 머리 없이 다시 → `sse-1:0`부터·앞 두 낱말 두 번 `False`(예시 부분이라 노랑) → 값 셋 `sse-1:5 | 200 | ['done']`·`other:0 | 400 | Last-Event-ID의 thread가 다릅니다`·`sse-1:x | 400 | Last-Event-ID 형식이 올바르지 않습니다` + 제공 함수는 처리 함수보다 먼저 불려 응답 전에 400(fastapi `routing.py` 452·491~493행).
- **기록 조용히(handoff §05 → §06 4)**: 1절 셀 `logging.getLogger("agent_service.app").setLevel(logging.CRITICAL)`(Ch 28 02 선례 — 결과 읽기에 「함수 `logging.getLogger`는 Ch 28 02절에서 본 것처럼 …」·「막은 것은 기록뿐이고, 앱이 보내는 응답은 바뀌지 않습니다」). 막지 않으면 0초 요청 하나에 표준 오류 25줄(Traceback 사슬 둘 `CancelledError` → `TimeoutError`, 기기 파일 위치 포함 — 노트북 밖 `p1_scene.py --loud`). 저장 출력 표준 오류 0·Traceback 0·`/var/folders` 0.
- **말(handoff §05 → §06 5)**: 새 용어 **3**(meta 「새 용어 3」): **이어 받기(resuming)**·**오류 사건**·**함수 fetch**(뜻 → 일상 예(책갈피·주문 취소 알림·편지와 답장) → 코드). 제목의 「fetch」·「재연결」·「오류 이벤트」는 1절·b2에서 「제목의 …」로 한 번씩. 「식별자」 → 「사건 번호」 · 「헤더」 → 「요청 머리」 · 「멱등」 → Ch 23 06 「멱등성」 말로(b3·b7). 기록기(logger)는 Ch 28 02 이어 씀.
- **b3 고침(handoff §05 → §06 8·11)**: 05절(SSE 사건·칸·사건 번호·`split_sse`·`parse_sse`) + 02절(재정의·앱 객체에 남음·같은 셀에서 비움) + 04절(`join_tokens`) + **Ch 23 01(체크포인터·스레드 — 「이 앱은 체크포인터를 쓰지 않아 `thread_id`는 사건 번호 앞머리와 응답 본문에만」, 노트북 1절 출력 `그래프의 체크포인터: None`으로 한정)** + **Ch 24 01(이어 갈 때 노드가 첫 줄부터 다시 실행) + Ch 23 06(멱등성) — 「이 절의 서버도 이어 받을 때 그래프를 처음부터 다시 실행하므로, 그래프에 바깥 쓰기가 있으면 같은 원칙이 필요합니다」(참 유지)** + Ch 28 02(기록기).
- **b4 「Ch31에서 … 동일 이벤트를 재생」 고침(거짓)**: b7 「Ch 31은 PostgreSQL 데이터베이스에 표를 만들어 쓰는 방법과 체크포인터를 다룹니다. 보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다」 + 「보낸 사건을 저장해 두었다가 다시 보내는 방법도 실행하지 않았습니다」. Ch 31 `_src` 제목 다섯(SQLAlchemy 비동기 PostgreSQL·트랜잭션과 원자성·Alembic·커넥션 풀·pgvector 체크포인터 공존과 백업)과 준비 노트 §5-4로 확인.
- **JS·TS(handoff §05 → §06 7)**: 노트북은 `node`를 부르지 않고 TS 파일을 글로 읽어 줄 번호와 출력 — 16행(요청 머리 `Last-Event-ID`)·17~21행(`fetch` POST)·22행(`response.ok` — 상태 코드 200대)·28~29행(빈 줄에서 나누고 끝 글을 남겨 다음 읽기와 합침)·30행 `decodeBlock`(3~9행, 칸마다 첫 줄) 풀이 + 「이 노트북에서는 실행하지 않았고」 + b7에 README 명령(`uv run fastapi dev agent_service/app.py` → `npx tsx client/test_stream.ts`)과 노트북 밖 확인 한 문장. `parse_sse`는 `\n\n`만(`\r\n`·`: ping` 안 다룸) ↔ TS `split(/\r?\n\r?\n/)` 차이를 노트북 4절·b7에 밝힘.
- 노트북: 제목 셀(할 일 셋·준비물·기준 버전·강의와 실습 범위) · 오늘 볼 그림(06-1 첨부) · 1 준비(설치 여섯·가져오기 + 도구 파일·파일 위치 셀·앱 가져오기와 체크포인터·기록기) · 2 첫 응답의 사건 번호 · 3 Last-Event-ID로 이어 받기 · 4 fetch로 읽는 쪽 · 5 Before · 6 After · 7 값 바꿔 보기 · 정리 세 줄 + 07 예고. 파일 위치 셀은 01절 셀 글 그대로(생성기 `__main__`에서 `author_01.py`와 문자열 대조 `assert`). 설치 셀은 05와 같은 여섯(도구 파일은 표준 라이브러리도 가져오지 않음). 키 셀 없음.
- 본문 b1~b10 새로(b10 = WHATWG HTML SSE·FastAPI SSE·MDN fetch()·MDN Response.body·MDN Using server-sent events(다섯 모두 2026-09-29 WebFetch, MDN은 최종 수정일 함께) + 설치판 소스 행 + 실습 파일 행). 복습 넷 → **다섯**(해설 포함). meta 「강의 1.5h | 실습 2.75h」 그대로(챕터 시수 합 유지).
- 옛 `{{svg:06-흐름}}` 토큰 제거, 옛 그림 파일 셋(`06-흐름.svg·.excalidraw·.caption.md`)은 그대로.
- 설명만 고친 뒤(`removeprefix` 문장 한 곳) `mdpatch.py`로 생성기·노트북 마크다운을 함께 고침 — 코드·출력·`executed_at` 그대로(A 사본과 `cmpout` 26/26·`outputs_sha256` 같음), 생성기 `cells()`와 노트북 셀 글 57/57 같음 확인(mdpatch 전).

## 설치판 동작 확인 (모델 없이 — `/tmp/ch30-06/exp/`)

- `p1_scene.py`(노트북 장면 전체, 셀 맨 위 await 자리는 `asyncio.run` 안 비동기 함수, 5번): 출력 md5 **5/5 같음**(`438a7bf7ead8f4fe1f1bf05cb555331a`), 표준 오류 0. `--loud`(기록기 수준을 올리지 않음)는 표준 출력 같고 표준 오류 25줄·`Traceback` 2. 덧붙여 본 값: `Last-Event-ID: sse-1:0` → token 다섯 + `done` · `sse-1:-1` → 사건 일곱 전부(`int("-1") + 1 = 0` — b7에 「노트북 밖에서」로 한 문장) · `sse-1: 3`(공백) → token 둘 + `done`(본문에 안 씀).
- `p2_ts.py`(TS 시험): 포트 8000 빈 것 확인 → `subprocess.Popen([python, -m, uvicorn, agent_service.app:app, --app-dir 실습 폴더, --host 127.0.0.1, --port 8000, --log-level warning])`(`OPENAI_API_KEY` 뺀 환경·`PYTHONDONTWRITEBYTECODE=1`) → `/health` 200 → `node client/test_stream.ts`(Node **v22.23.2**, `process.features.typescript` `strip` — npm 설치 없이 돎) → **종료 코드 0**, 출력 `{"normal":["token","token","token","token","token","done"],"firstId":"web-01:0","resumedFirstId":"web-01:1","failed":["error"]}`, node 표준 오류 0 → `terminate()`·`wait()` −15 → 포트 8000 다시 빔 · uvicorn 표준 오류 26줄(`Traceback` 1 — 시험 파일의 질문 「오류」에 `agent.py` 18~19행이 일부러 던진 `RuntimeError`) · 남은 uvicorn·node·ipykernel 0 · 실습 폴더에 새 파일 0.
- `p3_next.py`(07 인계용, 5번, 출력 md5 5/5 `f36331c5a7e04e5d54c077ff53d045be`, 표준 오류 0): 아래 「§06 → §07」 사실 — CORS 와일드카드 + 자격 증명·실습 앱 CORS·401 머리·`HTTPBearer`·`/v1/chat` 0초 504.
- `agent.checkpointer` → `None`(노트북 1절 출력으로도 보임) · 앱 기록기 이름 `agent_service.app`(기본 유효 수준 WARNING).
- 공식 문서(2026-09-29 WebFetch): FastAPI SSE 「Resuming with Last-Event-ID」(브라우저가 끊긴 뒤 다시 연결하면 마지막 `id`를 `Last-Event-ID`로 보냄, 요청 머리 매개변수로 읽어 처음부터 세며 `i < start`면 건너뛰는 예 — 실습 앱과 같은 모양)·「SSE works with any HTTP method」·스트림 안 오류 처리는 문서에 없음 · WHATWG HTML SSE(다시 연결할 때 마지막 사건 번호가 비어 있지 않으면 `Last-Event-ID`를 담음 · `id` 없는 사건은 앞 번호를 이어 씀 · 200이 아니거나 `text/event-stream`이 아니면 연결 실패·다시 연결 안 함) · MDN `fetch()`(2025-12-16 — 404·504에도 실패하지 않음, `ok`·`status`를 봐야 함) · MDN `Response.body`(2025-03-13 — `ReadableStream`) · MDN Using server-sent events(2026-09-03 — `id`는 `EventSource`의 마지막 사건 번호) · **MDN `Last-Event-ID` 요청 머리 쪽은 404**(참고 자료에 넣지 않음) · FastAPI CORS(07 인계용 — `allow_credentials=True`면 세 칸 모두 `['*']` 불가).

## 실행 (새 커널)

| 실행 | 자리 | 키 | 결과 |
|---|---|---|---|
| 시험 tryA(`/tmp/ch30-06/tryA` 사본, `execute.py` 기본 `--cwd` = 프로젝트 맨 위, `PYTHONPATH` = `notebooks/`, 09:31:43Z) | 루트 커널 | `OPENAI_API_KEY` 지움 | PASS 26셀 |
| 시험 tryB(사본, `--cwd` 실습 폴더 `notebooks/`, `PYTHONPATH` 지움, 09:32:03Z) | 학생 커널 | 지움 | PASS 26셀, tryA와 셀별 26/26·`outputs_sha256` 같음(`08fa05f6…`) |
| **A**(`run_section.sh … 06`, `executed_at` 2026-09-29T09:32:33.074728Z) | 루트 커널 | 지움 | PASS 26셀(그림 첨부 단계에서 멈춤 — 06-1 PNG 전) |
| **B**(A 사본 `/tmp/ch30-06/B`, `uv run … execute.py --cwd notebooks/`, `PYTHONPATH` 지움, 09:32:44Z) | 학생 커널 | 지움 | PASS 26셀 |

- **A ↔ B 셀별 출력 글자 26/26 같음**(이은 글 해시 `8d0059bba5553721` 같음), `code_sha256` `21a623d11a53dc5ef945858d8636da9a1cd7796b991a3555cdd5156e7a135ecb` 같음. **`outputs_sha256`은 다름**(A `e1b573c11c415069e40b58d451812336bde56ee609856c27eb63750fb9b72465` · B `08fa05f61405307d9708311ef0a1a5f24b0cf0a82734ef6b82efb4e0fb145959`) — 까닭: 설치 셀 [1]의 표준 출력 스트림이 A는 66 + 100글자 둘로 나뉨, B·tryA·tryB는 166글자 하나(합친 글은 같음 — 02·03·05 선례). 요청 0이라 셀 [2]~[26] 출력 구조까지 같음. 초·ID·포트를 출력하는 셀 없음.
- 그 뒤 `--no-exec` 다섯(렌더·첨부·빌드)과 `mdpatch` 한 번에서 노트북 코드·출력·`executed_at` 그대로(A 사본과 `cmpout` 26/26·`outputs_sha256` 같음) — 노트북 파일 **`dafe25761ee5e57554d87433117ed287604d6fb636a1e661a99b4c13037faec8`**.
- 모든 실행 `PYTHONDONTWRITEBYTECODE=1` · 실습 폴더에 새로 생기거나 바뀐 파일은 노트북 06·도구 파일뿐(`find -newer` — `agent_service/__pycache__` 그대로, pyc 0) · `.failure.json` 0 · 노트북 표준 오류 출력 0 · 설치 셀 출력에 pip 안내 한 줄.
- **모델 요청 0** · 노트북 안 서버 프로그램·포트·자식 프로세스 0(TS 시험만 노트북 밖에서 uvicorn 하나 — 끝내고 0) · 남은 프로세스 0(`ps` — uvicorn·node·ipykernel·jupyter 없음).

## 앱 파일 고침 · `app.openapi()` 대조 · `tests/`

- **06은 앱 파일을 고치지 않음.** 3절이 `app.py` 41~53행·107~117행을, 4절이 `client/stream.ts` 11~30행을 글로 읽어 출력만 함 — 47행 f-string·51행 `removeprefix`·53행 `raise … from exc`·43행 `str | None`·117행 `index += 1`은 출력된 앱 파일 줄로 두고 뜻만 풂(「둘 다 이 과정의 노트북에서는 쓰지 않는 모양이라, 뜻만 봅니다」). 고치면 02~05의 출력(줄 번호·글)이 함께 바뀜.
- 확인: `json.dumps(app.openapi(), ensure_ascii=False, indent=2)` sha256 **`06e5d1b9553a1fde91aafc44b02e0836a8a241386e42077dc15825a75be5e658`** = `openapi.json` 바이트 같음 · `pytest -q -p no:cacheprovider` **6 passed, 1 warning** · 앱 파일 해시 `app.py` `3455d405…`·`agent.py` `a6c42e63…`·`live_agent.py` `586a6a69…`·`schemas.py` `ed77b197…`·`__init__.py` `1c7d7aef…`·`tests/test_app.py` `f8611741…` 그대로. `openapi.json`·생성 SDK·`client/*.ts` 손대지 않음.

## 도구 파일 — 06 판 (04 대조 사슬 이음)

- **옮긴 함수 넷**(이 절이 다시 쓰는 앞 절 함수 — 규격 §2-7 3번): `zero_timeout`(02 `author_02.DEF_ZERO`) · `join_tokens`(04 `author_04.DEF_JOIN`) · `split_sse`·`parse_sse`(05 `author_05.DEF_SPLIT`·`DEF_PARSE`). 04 판(`author_04.TOOLS` — Ch 25 `positions_of`·`mode_order`) 뒤에 차례대로, 각 블록은 「`# Ch 30 NN절에서 배웠습니다 — NN절 노트북의 같은 이름 함수를 옮겼습니다`」 + 그 절 노트북 셀 글 그대로(설명 주석 첫 줄·본문·안쪽 주석 모두). 가져오기 0.
- 파일 `e0a3a382…`(04 판) → **`e1a1464d0f647e0b2ca99fd14338eeb22c596effd405b5acf2ee49ac1d2c704d`**(2222자).
- 대조(`author_06.check_tools06`, 생성기 `__main__`마다): 06 판이 04 판으로 시작 · 함수 이름 차례 `positions_of, mode_order, zero_timeout, join_tokens, split_sse, parse_sse` · 각 셀 글이 **그 절 노트북(02·04·05)의 코드 셀 글과 문자열로 같음** · 도구 파일 함수와 셀 함수의 AST 같음 · 04 생성기 가드(`strip_later_imports` 뒤 04 판으로 시작하고 04 판과 다르면 건너뜀)가 06 판을 덮어쓰지 않음.
- 쓰기 가드: 디스크 파일이 04 판이거나 06 판일 때만 06 판을 씀 · 06 판으로 시작하는 더 긴 판(뒤 절이 더함)은 건너뜀 · 그 밖은 멈춤. `--tools-copy DIR` 있음.
- **04 노트북 영향**: 04 노트북 사본을 06 판 도구 파일로 `notebooks/` 커널에서 다시 실행 → PASS 23셀·셀별 23/23·`outputs_sha256` `e7a37a53…`까지 저장본과 같음(실습 폴더 04 노트북은 그대로 `14427e45…`). 05 노트북은 도구 파일을 가져오지 않음.
- 가져오는 준비 셀은 `os.chdir` 전(1절 둘째 셀) · 결과 읽기에 고정 세 문장 + 커널 폴더 문장 둘(04 글 그대로) + 「도구 파일에는 04절이 옮긴 Ch 25 함수 둘도 있지만, 이 절에서는 쓰지 않습니다」.
- 공개 목록 두 곳(`textbook/part7/public-files.json`·챕터 `qa/public-files.json`)은 04에서 줄을 넣어 그대로 — 파일 해시만 바뀜(목록 밖 파일이라 `manifest-changes.md`에는 메모로).
- 이 절이 처음 가르친 함수 여섯(`read_events`·`event_names`·`last_event_id`·`token_values`·`status_says_ok`·`ended_with_done`)은 노트북에 둠 — 뒤 절이 다시 쓰면 그 절이 옮김(handoff §06 → §07 6).

## 고친 틀린 사실

- b4 「Ch31에서 실행과 이벤트를 저장하면 동일 이벤트를 재생할 수 있습니다」(거짓) → b7 두 문장(Ch 31이 다루는 것 · SSE 사건 저장은 Ch 31에서도 다루지 않음).
- b3 「Ch23의 thread 분리」 → 한정(노트북 출력 `그래프의 체크포인터: None` — `thread_id`는 사건 번호 앞머리와 응답 본문에만).
- b3 「Ch24의 중복 실행 방지 원칙」 → 참(유지) — Ch 24 01 + Ch 23 06 링크, 그래프에 바깥 쓰기가 있을 때로 조건을 적음.
- b4 「이 예제는 결정적 Agent를 다시 실행해 앞부분을 건너뜁니다. 외부 모델은 재실행 결과가 달라질 수 있으므로」 → 사실은 참 — 앱 107~117행 출력 + `sse-1:5`·`sse-1:99` → `done`만 출력으로 보이고, 모델 그래프는 「실행하지 않았습니다」로 한정.
- b4 「클라이언트는 처리에 성공한 id를 저장」·「서비스 설계 판단」(백오프·무작위 지연·작업 ID)·b7 「재시도 횟수와 간격에 상한」·「마지막 ID는 사용자와 실행 식별자에 묶어」 → 실행하지 않은 설명이라 뺌.
- Before(「오류」 글자 — 일부러 던지는 예외) → 시간 제한 0초(실제 조건)로 바꿈. 시험 파일 `test_stream.ts`가 「오류」 글자를 쓴다는 사실은 b7에 밝힘.
- 「이벤트」·「재연결」·「헤더」·「식별자」·「멱등」·「조각」 → 위 「말」. 도식 읽기 틀 색 문장 → 그림마다 새로, 보라 0·빨강은 06-4 Before 판정 상자 하나.

## 그림

- Mermaid 넷: 설계표 `06-figures.md`(렌더 전 작성) → `.mmd`·캡션 → 렌더 → PNG 넷을 직접 열어 확인(stage 사본): 06-1(`flowchart TB` 상자 일곱 한 줄, viewBox 폭 275) · 06-2(갈래 셋 — 400 둘 점선, 폭 642) · 06-3(공통 상자 + 칸 둘, 폭 607) · 06-4(공통 둘 + 칸 둘, 폭 546) — 모두 868 이하, 끊긴 라벨 0, 색은 설계표대로(초록 요청 머리·앱 파일 함수 / 파랑 우리 줄·판정 함수 / 노랑 출력 / **빨강 06-4 Before 판정 `True` 하나** / 보라 0 / 06-3 요청 머리 없는 칸은 예시 부분이라 노랑). 다시 렌더한 것 없음. 라벨 숫자는 출력에 있는 사건 번호·상태 코드 200·400·줄 번호 41~53뿐(`start` 값 2는 출력하지 않아 「다음 자리부터」로).
- 삽화 06-5: **1차 job `88ffc73c-f7e9-4e7c-b8e4-8e30821d91f7` 채택(재생성 0)** · 거래 2026-09-29T09:35:17.872916Z 「Nano Banana Pro −2」(**이 절 몫 2크레딧**, 잔액 2279 → 2277, 앞 거래 08:57:46Z는 Ch 30 05) · 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만) · 원본 `5f6dee43…`(2752 × 1536) → 저장 PNG `18ec9260164f786bc7fe400255d9481b6d8db7dfa977d3f60784a6162016c0a7`(1100 × 614) · 결과를 다시 받아 줄인 그림과 픽셀 대조 bbox `None`·최대 차이 0 · 저장본 사본을 열어 위 선로 크림색 짐칸 둘·아래 선로 크림색 짐칸 넷 + 분홍 짐칸 하나·크림색 칸마다 검은 세모 판 하나·분홍 칸 판 없음·기관차·사람·글자·숫자·화살표 없음을 세고 그림 읽기를 씀. **거의 흰 가로줄 115 / 614**(05 6·04 423). **설계와 다른 점**: 아래 줄이 위 줄 끝 오른쪽에서 계단처럼 시작하지 않음 — 개수·색·판이 맞아 「두 선로 세모 판 칸 합 여섯, 겹치는 칸 없음」으로 읽고 채택(재생성 한도를 개수 위험이 있는 다시 그리기에 쓰지 않음). 01~05 소품 되풀이 없음, 번호판을 05와 다른 모양(검은 세모)으로.

## 검사

- `run_section.sh … 06 --no-exec`: 렌더 넷 · 첨부 1 · `_build.py` · **`verify.py --chapter` `PASS 9 sections / 159 code cells (max 14 lines)`** · 게이트 **G1~G7 0 PASS**.
- 빌드 HTML `06-fetch-재연결과-오류-이벤트.html`(`ebec3561…`): `{{` **0** · `[[` 0 · 인라인 SVG 4 · 삽화 JPEG 1.
- `pack.py … 06` → `qa/upgrade/review-pack/06-fetch-재연결과-오류-이벤트.md`(`d1712f86…`).
- 보호 파일 255개: `manifest-changes.md` 「06절 뒤」에 덧붙임.

## 완료 챕터 문장 참·거짓 (이 절 쪽 조건 — 고치지 않음)

`grep -rn 'Ch *30' textbook/part1 part2 part5 part6 part7 --include=*.html | grep -v ch30-fastapi`(최종 HTML·`_src`만, `qa/` 뺌) + 생성기 주석:

| 문장 | 판정 |
|---|---|
| Ch 24 `author_01.py` 28행 주석 「멱등하게 적는 노드 … (Ch 30 06 「중복 실행 방지 원칙」이 기대는 문장의 실행 근거)」 | **참** — 06 b3가 Ch 24 01 링크와 「그래프에 바깥 쓰기가 있으면 같은 원칙」을 유지 |
| Ch 2 11 b8(2절)·Ch 2 12 b8(1절·3절)·Ch 2 `index.html` | 06과 무관 — 참 |
| Ch 29 05 b8(01 슬러그) · Ch 1 01 과정 지도 · Part 7 소개 「Ch30의 요청·응답 형식에서 시작해 …」 | 06과 무관 — 참 |
| Ch 31 01 b2·b3 · Ch 34 04 b3 「Ch 30에서는 FastAPI 비동기 요청 처리」 | 글만(참 — 대기 챕터, 고치지 않음) |

- 완료 챕터 최종 `_src`에 「Last-Event-ID」·「재연결」·「이어 받기」로 Ch 30 06을 가리키는 문장 없음.

## 챕터 밖 수정

- `textbook/_notebook/checks/notebook-contracts-part7-ch30-fastapi-serving.json`(`verify.py --chapter`가 다시 씀 — `33adffef…`) · 사용자 디스크 `.cache/ch30-06-view/`(삽화 보기 사본 하나 — 새로 만든 폴더). 공용 도구·규격·과정 문서·zip·검사 스크립트·앱 파일·TS 파일·공개 목록·Ch 31 이후 파일은 고치지 않음.

## 강사 확인 대상

1. 새 말 「이어 받기」·「오류 사건」·「함수 fetch」와, 제목 「fetch 재연결과 오류 이벤트」를 그대로 둔 것(본문 첫 자리 풀이).
2. Before를 옛 「오류」 글자(일부러 던지는 예외)에서 시간 제한 0초(실제 조건)로 바꾼 것 · Before 결함을 「상태 코드만 보는 판정」 함수로 세운 것.
3. 연결을 실제로 끊지 않고 첫 응답의 앞 사건 둘을 「받은 사건」으로 쓴 것(시험용 클라이언트 한계 — 본문·노트북에 밝힘).
4. 도구 파일로 02절 `zero_timeout`까지 옮긴 것(규격 §2-7 3번 — 재정의 함수도 앞 절이 가르친 함수로 봄, 셀 글 그대로라 도구 파일 주석이 「… 함수를 정의합니다」 모양).
5. TS 시험을 노트북 밖에서만 돌리고 본문 b7에 「교재를 만들 때 노트북 밖에서 … 통과했습니다」로 적은 것.
6. 삽화의 계단 모양이 안 나왔지만 재생성하지 않은 것(흰 가로줄 115/614).
7. 앱 파일 41~53행의 f-string·`removeprefix`·`raise … from exc`를 고치지 않고 「뜻만 봅니다」로 둔 것(고치면 02~05 출력이 바뀜).

## 남은 것 (마감 몫)

- `part7-practice.zip`에 06 노트북 새 판·도구 파일 06 판 반영(마감 때 한 번) · 06은 Part 7 묶음 실행 검사 대상 아님(01만).
- 옛 그림 `06-흐름.{svg,excalidraw,caption.md}` 삭제 승인(Part 7 `check_figures.py`와 함께).
- 삭제 승인 대상(지우지 않음): `qa/upgrade/gates-wip-06-06.json` · 기기 `/tmp/ch30-06/`(사본·실험·삽화 원본 둘·도구 복사본, 약 10MB) · 사용자 디스크 `.cache/ch30-06-view/`(보기 사본 하나).
