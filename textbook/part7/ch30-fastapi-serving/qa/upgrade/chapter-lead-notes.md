# Ch 30 FastAPI로 Agent 서빙 — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part7/ch30-fastapi-serving`(절 아홉 — paired 01·02·03·06·07, experiment 04·05·08·09) · 실습 폴더 `labs/part7/ch30-fastapi-serving`(자리 확인: `chapter.json` `lab_path`와 같음). 바로 앞 Ch 29(완료, Part 6 마지막)를 잇는 **Part 7 첫 챕터**입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본 **103개, 1,090,200바이트** — 원본과 바이트 대조 103/103 같음) · `gates-before.json`(`8951dc50…`) · `before-manifest.json`(**255개**, `9e7bbb4d…`) · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch30-fastapi-serving`(252MB, 사용자 디스크).
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(전부) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 과정 요약(§0~§9, 특히 §2-13~§2-20·§5·§6·§7) · 계약 파일(`grep -n '^#'` 뒤 §3 Ch21~29 줄·§4 도구 파일 줄·§5 묶음 줄·§8 기준 버전) · Ch 29 `chapter-summary.md`(전부)·`chapter-lead-notes.md`·`before-manifest.json`(모양) · Ch 21·23·24·25·28 요약의 Ch 30 인계 줄 · Ch 2 요약(비동기) · Part 7 목록·목차·묶음·검사 스크립트 · 챕터 `qa/` 기록. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.
- **원고·노트북·그림·앱 파일은 하나도 고치지 않았습니다.** 연결 폴더 안 파일 삭제 0건, 노트북 실행 0건, 서비스 모델 요청 0건, `uv cache prune` 안 함. 확인은 기기 `/tmp/ch30-prep/exp/`의 작은 스크립트(`e1`~`e7`)·설치판 소스·공식 문서로 했습니다. 모든 파이썬 호출은 `PYTHONDONTWRITEBYTECODE=1`·`OPENAI_API_KEY`를 지운 환경. 서버는 `127.0.0.1`에서 두 번 띄웠고(uvicorn 자식 프로세스 — 임시 앱 1번·실습 앱 1번, 요청은 모두 결정적 그래프) 두 번 모두 `SIGTERM`으로 끝냄(종료 코드 −15·143), 남은 uvicorn·node 프로세스 0, 포트 8000 닫힘. 실습 폴더에 새로 생긴 파일 0(`find -newer`).
- `chapter.json` `hours` = 「총 32h · 강의 10h · 실습 22h」. 절 meta 강의 1.25·1·1·1.25·1.25·1.5·1·0.75·1 = **10h**, 실습 2.5·2.5·2.5·2.5·2.75·2.75·2.5·2·2 = **22h** — 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part7/_build_index.py` 20행 `(10, 22)`도 같습니다. 새 용어 meta 4×8 + 3(09) = 35(옛 생성기 틀 값 — 실제 새 말 목록 없음).

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-29)

| 절 | 코드 셀 | 코드 줄 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 비동기 라우팅과 스키마 (paired) | 5 | 27 | 86 | 1 | 1 | 5 | 0 | 6 | 11 | 3 | 27 |
| 02 의존성으로 Agent 주입 (paired) | 5 | 29 | 84 | 3 | 1 | 5 | 0 | 6 | 13 | 3 | 31 |
| 03 ainvoke 요청 응답 (paired) | 5 | 25 | 82 | 1 | 1 | 5 | 0 | 7 | 12 | 3 | 29 |
| 04 astream과 응답 스트림 | 4 | 29 | 81 | 1 | 1 | 4 | 0 | 6 | 11 | 3 | 26 |
| 05 POST SSE 이벤트 설계 | 4 | 30 | 79 | 2 | 2 | 4 | 0 | 6 | 21 | 3 | 38 |
| 06 fetch 재연결과 오류 이벤트 (paired) | 5 | 32 | 84 | 1 | 1 | 5 | 0 | 6 | 9 | 3 | 25 |
| 07 인증 CORS 타임아웃 (paired) | 7 | 53 | 86 | 4 | 1 | 7 | 0 | 10 | 16 | 3 | 41 |
| 08 OpenAPI와 TS SDK | 4 | 26 | 80 | 1 | 1 | 4 | 0 | 6 | 17 | 3 | 32 |
| 09 실제 Agent HTTP 통합 | 6 | 54 | 102 | 5 | 2 | 6 | 0 | 8 | 19 | 3 | 43 |
| **합계** | **45** | **305** | **764** | **19** | **11** | **45** | **0** | **61** | **129** | **27** | **292** |

- 통과 절 **0/9**. 코드 줄은 주석·빈 줄 뺀 값(`/tmp/ch30-prep/ast_scan.py`), 셀 최대 14줄(09).
- G1 19 = 제너레이터 식 13(아홉 절 모두 준비 셀 `next((p for p in (start, *start.parents) …), None)` + 09 `next(…)` 셋) · 내포식 2(05·09 `[b for b in re.split(…) if b]`) · 준비용 클래스 2(02 `StubAgent`·07 `SlowAgent`) · `lambda` 3(02 하나·07 둘). **G1이 `class Question(BaseModel)`(01)은 스키마 클래스로 봐서 세지 않음.**
- G2 11 = 한 글자 변수 `p`(아홉 절 준비 셀) · `b`(05·09).
- **G3 45 = 모든 코드 셀에 첫 줄 주석이 없음**(주석 0줄).
- **G4 0이지만 규격 §3을 어김** — 실제 모델은 노트북이 아니라 앱 파일 `agent_service/live_agent.py` 18~22행 `init_chat_model("openai:gpt-5.4-mini", temperature=0, timeout=30)`에서 만듦 → 게이트가 못 봄. **`reasoning_effort="none"` 없음**(Ch 29 03 문자열 모델과 같은 사각지대).
- G5 61 = 제목 셀·핵심 그림 첨부 없음 18 + 결과 읽기 인용 없음·빠짐 43.
- G6 129 = 70자 넘는 문장·영문 시작 조사(「Pydantic의」·「`astream`은」·「SSE는」 등). §4·과정 금지어는 대부분 G6가 세지 않음(§1 표·§10).
- G7 27 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 것 (AST로 따로 셈 — 노트북 45셀)

- **별표 풀기** `(start, *start.parents)` 아홉 절(과정 요약 2-2 금지 모양) · **딕셔너리 풀기** `{**auth, 'Last-Event-ID': …}`(06) · `+=`(04).
- **비동기**: 셀 맨 위 `await` 6(03 셋·07 둘·09 하나) · `async for` 2(04) · 셀 안 `async def` 4(01 라우트·02·07 클래스 메서드) · **`yield`**(07 `SlowAgent.astream` — 비동기 생성기, 과정 A 트랙 처음).
- **데코레이터** `@mini.post('/ask')`(01) · **타입힌트** `body: Question`(01 — FastAPI가 힌트로 본문을 읽음)·`text: str = Field(…)`.
- **그 밖**: `try/except RuntimeError as exc`(03, `failed` 변수가 예외가 안 나면 정의되지 않는 모양) · `next`(09 넷)·`getattr`·`isinstance`(09) · `sorted`(03) · `re.split`·`re.findall`(05·06·09) · `import json, re`(09 한 줄 두 모듈) · `.get`(07) · `''.join`(04·09) · f-string 0.
- 앱·테스트 파일(학생이 여는 파일 — Ch 28 A-17 「서버 파일도 금지 문법 0」 선례 대상): `app.py` 126줄에 `async def` 10·**매개변수 힌트 20·반환 힌트 9**·기본값 매개변수 2·데코레이터 5·f-string 3·`try` 4·`.get` 4·`async with` 2·`async for` 2·`yield` 6·`+=` 2, `X | None`·`Annotated`·`AsyncIterable`·`from __future__ import annotations`·`raise … from exc`·`except Exception`·`removeprefix` · `agent.py` `class AgentState(TypedDict)`·f-string·반환 힌트·`try/except RuntimeError` · `live_agent.py` `@lru_cache`·`@tool`·`.get` · `tests/test_app.py` 반환 힌트 6·`{**AUTH, …}`·한 줄 두 조건 `assert a and b`.

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청(한 번) | 서버를 띄우는 법·끄는 법 | JS·TS | 파일 쓰기 | 손 값 | `assert` 대상 |
|---|---|---|---|---|---|---|---|
| 01 | 노트북 안에서 작은 앱 `mini = FastAPI()` + `class Question(BaseModel)`(`Field(min_length=1, max_length=20)`) + `@mini.post('/ask') async def ask(body: Question)` → `{'length': len(body.text)}`. 정상 200 `{'length': 5}` · Before 빈 글 422 `string_too_short` · After 「확인」 200 | **0** | 같은 프로세스 `TestClient(mini)`(포트 없음, 끌 것 없음) | 없음 | 0 | 길이 상한 20 · 입력 글 | 상태 코드·`{'length': 5}` |
| 02 | 실습 앱 `agent_service.app`의 `get_agent`를 `app.dependency_overrides`로 `StubAgent`(클래스 + `lambda`)로 바꿈 → `'대체 응답'` · Before 재정의를 남긴 채 다음 질문도 `'대체 응답'` · After `.clear()` 뒤 결정적 그래프 답 | **0** | `TestClient(app)` | 없음 | 0 | `'대체 응답'`(가짜 객체가 정한 글) · `local-demo-token` | 답 글(가짜 객체 글·결정적 그래프 글) |
| 03 | 결정적 그래프 `agent_service.agent.agent`에 셀 맨 위 `await agent.ainvoke({'messages': [...]})` → 키 `['answer', 'messages']` · Before 「오류를 발생」 질문 → `RuntimeError 교육용 스트림 오류`(앱 코드가 「오류」 글자를 보면 일부러 던짐) · After 정상 질문으로 다시 부름(고친 것 없음). **HTTP를 부르지 않음** | **0** | 없음(그래프 직접) | 없음 | 0 | 오류를 일으키는 글자 「오류」 | 답에 질문 포함·키 목록 |
| 04 | `async for chunk in agent.astream(…, stream_mode='custom')` → `['질문을 ', '확인했습니다: ', '세 ', '단어 ', '질문 ']`, 이어 붙이면 최종 답과 같음 · 질문 단어 수만 바꾼 조각 수 `{'짧음': 3, '두 단어': 4, '세 개의 단어': 5}` | **0** | 없음(그래프 직접) | 없음 | 0 | 공백 나누기 규칙(노드 코드) | `len >= 4`·이어 붙인 글·조각 수 크기 |
| 05 | `POST /v1/chat/stream`(FastAPI 0.135 `EventSourceResponse`·`ServerSentEvent`) → `200 text/event-stream; charset=utf-8`, 첫 블록 `event: token`·`id: sse-1:0`, 마지막 `event: done` · 질문 길이별 token 수(3·4)와 done 1 | **0** | `TestClient(app)` — **응답을 끝까지 받은 뒤 한꺼번에 나눔**(§7-1) | 없음 | 0 | `thread_id` 글 | 첫·끝 블록 줄·done 수 |
| 06 | 첫 응답에서 `id` 목록 `['resume-1:0', 'resume-1:1']` → `Last-Event-ID: resume-1:0`으로 다시 보내면 첫 id `resume-1:1` · Before 「오류」 질문 → 200 + `event: error`(앱이 일부러 던진 예외) · After `'event: error' in text`·`'stream_failed' in text` | **0** | `TestClient(app)` | **본문이 `client/stream.ts`를 언급만**(노트북에서 실행 안 함, README가 `npx tsx client/test_stream.ts` 안내) | 0 | 「오류」 글자 | id 글·상태 200·오류 글 있음 |
| 07 | CORS 사전 요청(허용 출처 200) · 인증 헤더 없음 401 · `SlowAgent`(클래스·`asyncio.sleep(0.05)`·`yield`)와 `get_timeout`→`0.01`(`lambda` 둘)로 단일 504·스트림 200 + `event: error` · Before 모르는 출처 사전 요청 → **400**·허용 헤더 없음 · After 올바른 인증 200 | **0** | `TestClient(app)` | 없음 | 0 | 0.05초·0.01초·출처 두 글 | 상태 코드·헤더 있음·없음 |
| 08 | `app.openapi()` → `3.1.0`, 경로 5, `/v1/chat` 요청·응답 참조 `ChatRequest`·`ChatResponse` · 두 번 만든 문서 정렬 직렬화가 같음(`문자 수: 4885`) · 파일 저장 | **0** | 서버 없음(앱 객체 메서드) | **TS SDK 생성은 README의 `npx @openapitools/openapi-generator-cli …`만**(노트북에서 실행 안 함) | **`openapi.json`을 실습 폴더 맨 위에 씀**(`os.chdir(lab)` 뒤 `Path('openapi.json').write_text`) — 지금 파일과 새로 만든 글이 바이트 같음(§7-5) | — | 참조 글 끝·두 문서 같음 |
| 09 | 키 확인 → `POST /v1/chat/live`(`create_agent` + `@tool lookup_library_hours`) 답 · 같은 에이전트 `await live_agent.ainvoke`를 **따로 한 번 더** 불러 `tool_calls`·`ToolMessage` 확인 · `POST /v1/chat/live/stream`(`stream_mode="messages"`, 노드 `model`의 글 블록만 token 사건) 이어 붙인 답 · token 사건 수 `20` | **6**(도구 한 번이면 invoke마다 2 × 셋: HTTP ainvoke·직접 ainvoke·HTTP astream) | `TestClient(app)` | 없음 | 0 | 도구의 요일 표(월 `09:00~18:00`·화 `09:00~21:00`) | 키 있음·200·**모델 답 글에 `'18:00'`(규격 §3 위반)**·**모델이 고른 인자 `day == '월요일'`(흔들림)**·도구 결과·마지막 done·token 수 > 0 |

- **서비스 요청 합계(한 번 실행)**: 01~08 **0** · 09 **6**(모델이 도구를 한 번 부를 때. 임베딩 0). 키 셀은 09에만.
- **`temperature=0`·`reasoning_effort="none"`**: 앱 파일 `live_agent.py`에 `temperature=0`만, `reasoning_effort` 없음(노트북 모델 셀 0 — G4 사각지대).
- **흔들리는 값**: 09 답 글·token 사건 수(`20`)·모델이 고른 도구 인자와 도구를 부를지·걸린 시간(저장된 셀 기록 3.05·3.89·2.13초). 01~08은 결정적(결정적 그래프·`TestClient`) — 단, 06·07 저장 출력의 **표준 오류 기록(Traceback 전문과 파일 위치)**은 기기·경로에 따라 달라짐(§12-4).
- **결정적 그래프**(`agent_service/agent.py`): 노드 하나 `answer_node`(`async def`)가 `f"질문을 확인했습니다: {question}"`를 공백으로 나눠 `get_stream_writer()`로 `{"token": piece + " "}`를 적음, 질문에 「오류」가 있으면 `RuntimeError("교육용 스트림 오류")`. **모델 없음**(Ch 20 03·Ch 23·24 「모델 없는 그래프」 모양). 상태 형식 이름 `AgentState`는 과정의 세 번째 같은 이름(Ch 21 요약 §13-7).
- **옛 그림 토큰**: 절마다 b4 「도식 읽기」의 `{{svg:NN-흐름}}` 하나(`figures/_gen_figures.py` → `textbook/part5/_figure.py`) · 노트북 토큰 paired `{{notebook:slug|example}}`+`{{notebook:slug|failure}}`, experiment `{{notebook:slug}}`. Mermaid·삽화 0장. **챕터 공개 목록에 옛 SVG 줄 없음.**
- 노트북 `metadata.verification`: 아홉 모두 `passed`, 실행일 **2026-09-11**(02:29 UTC, 사용자 맥 환경 — 출력의 `[사용자 폴더]/working/…`·`/var/folders/…`). 코드 셀 5·5·5·4·4·5·7·4·6 = 45. **코드 셀은 `notebooks/_generate.py`와 글자까지 같고, 마크다운 셀은 셋씩 더 있음**(09-14 옛 보조 스크립트 `.moai/…/part7_apply_depth.py`·`part7_review_fixes.py`·`part7_final_repairs.py`가 끼운 「이 준비 셀이 하는 일」·「바로 다음 코드를 읽는 방법」·「이 단계에서 구분할 범위」).
- 노트북 설명 셀: 제목 한 줄 · 「실행 환경 준비」 · 소제목 한두 문장 · **결과 읽기 셀 0**, 「이 노트북에서 할 일」·준비물(요청 수·비용·시간)·실행일 문장 없음, 첨부 그림 0.
- `_src` 틀(`_src/_generate.py` 옛 생성기): b4에 「코드 읽기와 개념 경계」·「서비스 설계 판단」(09는 「서비스 운영 인계」) 긴 단락 · b5 「확인할 점」 · 복습 넷씩 · 참고 자료 둘(09 셋, 확인 2026-09-11) · 도식 읽기 틀 문장 「파란 상자는 데이터, 보라색 상자는 Agent 실행, 초록 상자는 확인할 결과」(01~08 같은 글 — 과정 색 규칙과 다름).

### 금지어·주의 말 (`_src` 산문 / 노트북 마크다운 / 코드 주석 — 코드 백틱·`<pre>` 뺌, `/tmp/ch30-prep/ban.py`)

| 절 | 걸린 말(수) |
|---|---|
| 01 | 반환 5/2 · 스키마 5/2(제목에도) · 필드 9/0 · 검증 5/3 · **경로 7/1(URL 뜻)** · 라우트 5/3·라우팅 0/1(제목) · 사전 1/1 · 쿼리 1/1 · 병렬 2 · 직렬화 1 · 결정적 1 · 측정 2 · 로그 1 · 조각 1 · 실행 객체 1(Ch 21 인계) · **주문표 1(비유 — Ch 19 겹침)** |
| 02 | 반환 3/1 · 검증 4/1 · 라우트 11/5 · 의존성 7/3 · **주입 3/1(제목에도 — Ch 21 금지어)** · 세션 3/1 · 인터페이스 2 · 수명주기 2 · 보장 1/1 · 명시 1 · 지연 1 · 식별자 1 |
| 03 | **반환 7/4** · 사전 3/2 · 로그 4/1 · 이벤트 2/2 · 조각 2/1 · 명시 2 · 직렬화·지연·측정·보장·식별자 1 · **평가셋 1(Ch 29 인계)** · **택배 1(비유 — Ch 20 금지어 「택배 송장」)** |
| 04 | **조각 22/11(Ch 5 토큰 전용 말)** · 스트림 9/6 · 청크 6(한정어 없음) · 토큰 7/2 · 측정 3/1 · 지연 2/1 · 이벤트 3 · 반환 3/1 · 메타데이터 1 · 결정적 1 · 버퍼·인코딩·렌더링 |
| 05 | **이벤트 17/6(제목에도)** · 필드 7/3 · 식별자 6/3 · 프록시 4 · 버퍼 3 · 헤더 3 · 토큰 3/2 · 인스턴스 2 · 재연결 1/2 · 옵션·캐시·메타데이터·직렬화·재개·보장·파싱 1 · **택배 1(비유)** |
| 06 | 이벤트 14/3(제목에도) · 재연결 7/2(제목에도) · 헤더 5/3 · 식별자 4/2 · 스트림 4/3 · 멱등 2 · 버퍼 2 · 재실행·최대·결정적·세션·지연·반환·검증 1 |
| 07 | **헤더 12/5** · 토큰 7/1(「접근 토큰」 아님 — Ch 28 인계) · 스트림 6/2 · 의존성 5/1 · 명시 4 · 프로토콜 3 · 반환 3/3 · 사전 3/2 · 로그 3 · 최대 2/1 · 프록시 2/1 · 주입 0/1 |
| 08 | 스키마 8/6 · 필드 6/3 · 배포 3/2 · 경로 3/1 · 직렬화 2/1 · 보장 2 · 옵션 2 · 재연결 2 · **런타임 1(Ch 21 금지어)** · 결정적 1/1 · 캐시·재시작·명시 1 |
| 09 | 이벤트 14/2 · 결정적 5/1 · 스트림 9/1 · **경로 4/5** · 반환 5/1 · 청크 5/1 · **엔드포인트 3** · 메타데이터 3 · 지연 3/1 · 배포 3 · **평가셋 2(Ch 29 인계)** · 라우팅·추정·재시작·재실행·재연결 1 · 중단 0/2 |

- 제목의 영어·약어: 챕터 「FastAPI로 Agent 서빙」 · 01 「라우팅」·「스키마」 · 02 「Agent 주입」 · 03 「ainvoke」 · 04 「astream」·「스트림」 · 05 「POST SSE 이벤트」 · 06 「fetch」·「이벤트」 · 07 「CORS」·「타임아웃」 · 08 「OpenAPI」·「TS SDK」 · 09 「Agent HTTP」.

## 2. 절별로 더 봐야 할 것

### 01 비동기 라우팅과 스키마 (paired)
- 지금 Before(빈 글 → 422)는 **결함이 아니라 검사가 제대로 막은 장면**이고 After는 입력 글만 바꿈(코드를 고치지 않음). paired 규격(§5-3 Before 빨강 = 결함 결과)과 맞지 않음(§3 판정).
- 실제로 재현되는 결함 후보(모델 없이 결정적, `e2_app.py`·`e7_minimal.py`에서 확인한 동작): ① 본문을 딕셔너리로 받는 라우트(스키마 없음) → 빈 질문이 몸통(=에이전트 부르는 자리)까지 들어감 ↔ `BaseModel`+`Field(min_length=1)` → 몸통 전에 422 ② 응답 모양을 정하지 않은 라우트가 그래프 결과 상태 전체(`messages` 포함)를 내놓음 ↔ `response_model=ChatResponse`로 `answer`·`thread_id`만.
- **Ch 29 05 b8이 01 슬러그로 이음** — 「웹 서비스가 받을 요청과 내놓을 응답의 모양을 정합니다」 → **슬러그 `01-비동기-라우팅과-스키마` 고정**, b2·b3가 요청·응답 모양을 받아야 함. **Ch 2 12 b8** 「Ch 30 1절은 비동기 함수 안의 동기 호출이 이벤트 루프를 멈출 수 있다고 설명합니다」 → 01 b7(지금 첫 항목)에 그 설명을 남겨야 참.
- 설치판 사실: 422 본문 `detail[0]`의 칸 `type`·`loc`·`msg`·`input`·`ctx` · 501자 → `string_too_long` · `thread_id` 정규식 어긋남 → `string_pattern_mismatch`.
- b3 「Ch21에서 Agent **실행 객체**를 만들었습니다」 → Ch 21 03의 「실행 객체」(도구 매개변수 `runtime`)와 뜻이 다름(Ch 21 인계 — 「에이전트 그래프」로). b4 비유 「식당의 주문표」는 Ch 19 비유 「식당 주문 전표와 내주는 창」과 겹침.

### 02 의존성으로 Agent 주입 (paired)
- Before 「재정의를 남김 → 다음 질문도 대체 응답」은 **실제로 일어나는 상태 누수**(`app.dependency_overrides`는 앱 객체 속성이라 셀 사이에 남음) — 결함 장면으로 맞음. **Ch 2 11 b8** 「Ch 30 2절에서는 한 테스트가 남긴 대체 설정이 다음 질문까지 이어지는 실패를 다룹니다」가 이 장면에 기대므로 **장면 자체는 유지해야 참**.
- 문제는 도구: `class StubAgent`(준비용 클래스 — G1 `class_def`)·`lambda: StubAgent()`(G1). 가짜 모델은 아니지만 「정해 둔 응답을 내보내는 클래스」(규격 §3 금지 목록)에 가까움. **클래스·`lambda` 없이 같은 결함을 보이는 방법(확인함)**: 값 제공 함수를 이름 있는 `async def`로 바꿔 넣기 — `get_timeout`을 `0.0`을 내놓는 함수로 재정의하면 첫 질문 504 → **재정의를 남긴 채 다음 질문도 504** → `.clear()` 뒤 200(`e6_repeat.py`, 5/5 같음). 또는 `get_agent`를 다른 **컴파일한 그래프**(노드가 코드인 진짜 LangGraph)를 내놓는 이름 있는 함수로 재정의.
- b3 「Ch23의 체크포인터처럼 **생성 비용**과 수명주기가 다른 객체」 → Ch 23 인계: **수명만 참**, 생성 비용은 Ch 23이 재지 않음. b4 「`yield` 의존성으로 열고 정리」·`Protocol` — 실행하지 않은 설명. 공유 객체: 결정적 그래프는 모듈을 읽을 때 한 번 컴파일(`agent = build_agent()`), 실제 에이전트는 `@lru_cache(maxsize=1)`로 첫 요청 때 한 번 — **`lifespan`은 앱에 없음**(쓰면 `TestClient`를 `with` 블록으로 열어야 시작·끝 사건이 돎 — FastAPI 문서 확인).

### 03 ainvoke 요청 응답 (paired)
- Before 「오류」 질문 → `RuntimeError`는 **앱 코드가 일부러 던지는 예외**(`agent.py` 18~19행 `if "오류" in question: raise …`)이고 After는 질문만 바꿈 — 고친 것이 없음. 과정 규격 §3 「실패 장면은 실제로 일어나는 조건으로」와 Ch 16 05 「실패 흉내」 선례 사이 판단 필요.
- **실제로 재현되는 결함 후보(확인함, 결정적)**: ① 비동기 노드 그래프에 동기 `invoke`·`stream`(Ch 21·25에서 배운 모양) → **`TypeError: No synchronous function provided to "answer". Either initialize with a synchronous function or invoke via the async API (ainvoke, astream, etc.)`** ↔ `await agent.ainvoke(...)`(`e4_langgraph.py`) — Ch 2 12 b8 「Ch 30 3절은 await로 Agent 실행을 기다립니다」와도 맞음 ② `/v1/chat`은 에이전트 예외를 받지 않음 → `TestClient` 기본은 예외를 그대로 올리고, `raise_server_exceptions=False`면 **500 `Internal Server Error`**(안정적 오류 코드 없음) ↔ 스트림 라우트는 `event: error`로 바꿈 ③ 결과 상태 전체를 내놓는 라우트 ↔ 응답 모양으로 거름.
- b3 「Ch21에서 … 상태 **사전**」(금지어) · 「Ch25에서는 단일 실행과 스트리밍이 같은 실행 객체의 다른 **소비** 방법」(Ch 25 인계 — 뜻은 01 6절 `invoke` == 마지막 values로 참, 말은 Ch 30 몫) · **b7 「실제 모델 품질은 Ch29 평가셋으로 확인합니다」 → Ch 29에는 평가셋 없음**(Ch 29 인계 §16-1 — 「Ch 29의 궤적 맞춰 보기·평가 모델 판정」처럼 실제로 가르친 것으로). b4 비유 「택배 창구·송장 번호」 → Ch 20 금지어 「택배 송장」.
- `asyncio.wait_for`(시간 제한)는 과정에서 아직 안 가르침(Ch 2 요약 전제 금지 — `wait_for`·시간 제한·취소). `except TimeoutError`는 Ch 16 05에서 배움.

### 04 astream과 응답 스트림 (experiment)
- **Ch 25는 동기 `stream`만 가르침** → `astream`·`async for`는 이 절이 처음(Ch 25 요약 §15-1). **Ch 25 04 b8이 04·09 슬러그로 이음**: 「Ch 30 04절은 모드 custom의 사건을 비동기 메서드 astream으로 받아 이어 붙입니다. 09절은 모드 messages의 스트림 청크를 같은 메서드로 받아 서버 응답으로 보냅니다」 → **04는 모드 `custom` + `astream` + 이어 붙이기, 09는 모드 `messages`를 유지해야 참**, 슬러그 04·09 고정.
- **b2 「스트리밍은 중간 결과를 먼저 전달해 첫 응답 지연을 줄이지만」은 Ch 25를 근거로 쓸 수 없음**(Ch 25 인계 — 스트리밍하지 않은 실행과 견주지 않음, 「지연」은 금지어). 선택지: 문서 근거로 한정 · 이 절에서 결정적 부등식으로 직접 보임(같은 프로세스 `astream`은 실제로 사건이 생기는 때에 옴 — 0.3초 간격 노드에서 0.31·0.61·0.92초, 끝 0.92초, `e4_langgraph.py`) · 문장을 뺌. **초 값은 흔들리는 값**(Ch 25 03 선례 — 결론엔 차례·부등식만).
- 모드 목록 `stream_mode=["custom","updates"]`이면 사건이 `(모드 이름, 자료)` 짝(Ch 25 01과 같음). 설치판 `astream` 인자에 `version`(문서: `"v2"`면 사건이 늘 `type`·`ns`·`data` 칸을 가진 딕셔너리) — 과정은 v1 모양만 씀.
- b3 「Ch25에서 스트림 모드와 진행 **이벤트**를 비교」 → Ch 25 말은 「스트림 사건」·「진행 값」. 본문 「조각」 22번 → Ch 5 토큰 전용 말, 「청크」는 「스트림 청크」로(과정 결정).
- 실험 결과 해석 「조각 수 3·4·5」는 노드 코드의 공백 나누기 규칙이 정한 셈 — 실험이라기보다 규칙 확인.

### 05 POST SSE 이벤트 설계 (experiment)
- FastAPI **0.135.0에서 들어온** 기본 SSE(`fastapi.sse`: `EventSourceResponse`·`ServerSentEvent`·`format_sse_event`·`KEEPALIVE_COMMENT`) — 설치판 `sse.py` 20~34행(「Works with any HTTP method」)·42~143행(칸 `data`·`raw_data`·`event`·`id`·`retry`·`comment`, `data`는 늘 JSON — 글도 따옴표)·146~214행(줄 차례 `event` → `data` → `id` → `retry`, 끝 빈 줄 둘)·220~222행(쉼 신호 `: ping` **15초**) · `routing.py` 572·574행 `Cache-Control: no-cache`·`X-Accel-Buffering: no`.
- **확인한 모양**: `response_class=EventSourceResponse` + `yield ServerSentEvent(…)`이면 반환 힌트 없이도 SSE로 나감 · `response_class`를 빼고 `yield`만 하면 **`application/jsonl`**로 나감 · `data`의 한글은 `질…`로 나감(출력에 그대로 찍으면 읽기 어려움 — `json.loads`로 읽어 보일 것) · OpenAPI에 `itemSchema`(OpenAPI 3.2 방식)가 들어감.
- `TestClient`는 응답을 **끝까지 받은 뒤** 줄을 나눔(§7-1) — 「순서대로 도착」을 보이려면 uvicorn 자식 프로세스가 필요.
- b4 비유 「택배 상자 운송장」(Ch 20 금지어·03과 같은 계열) · b3 「Ch25에서 진행 이벤트와 토큰 이벤트를 분리」(Ch 25 말 아님).

### 06 fetch 재연결과 오류 이벤트 (paired)
- **이어 받기의 실제 모양**: 서버가 `Last-Event-ID`를 받으면 **그래프를 처음부터 다시 실행**하고 번호가 작은 사건을 건너뜀(`app.py` 107~117행) — 결정적 그래프라 같은 글이 다시 나와 맞아 보일 뿐, 실제 모델이면 글이 달라짐(b4가 밝힘). 범위 밖 번호(`sse-1:99`)는 검사 없이 `done`만 보냄 · 다른 스레드 접두사는 400 · 숫자가 아니면 400(`e2_app.py`).
- 지금 Before(「오류」 글자 → 200 + `event: error`)는 앱이 일부러 던진 예외. **실제 조건으로 바꿀 수 있음(확인함, 5/5)**: 시간 제한 값을 0으로 재정의(규격 §3 「아주 짧은 시간 제한」) → 스트림 200 + `event: error`, `done` 없음 → Before 「상태 코드만 보고 성공 판정」 ↔ After 「마지막 사건이 `done`인지」. 다른 실제 결함 후보: **클라이언트가 마지막 번호를 보내지 않고 다시 요청 → 이어 붙인 답 앞부분이 두 번**(결정적, 클라이언트 쪽 결함).
- **JS**: `client/stream.ts`(36줄 — `fetch`·`TextDecoderStream`·`split(/\r?\n\r?\n/)`·`async function*`·`yield`)·`test_stream.ts`(32줄). **이 기기 Node v22.23.2는 타입 지우기가 기본이라 `node client/test_stream.ts`가 npm 설치 없이 돎** — uvicorn(127.0.0.1:8000, 결정적 그래프)을 띄워 실행: `{"normal":["token","token","token","token","token","done"],"firstId":"web-01:0","resumedFirstId":"web-01:1","failed":["error"]}`, 종료 코드 0. `decodeBlock`은 `data:` 첫 줄만 읽고, 사건이 아니면 `null`을 내보냄(받는 쪽이 `if (event)`로 거름). 주소·접근 토큰·`thread_id`가 코드에 박혀 있음(포트 8000).
- b3 「Ch23의 thread 분리」 → 01로 참, 단 **앱은 체크포인터를 쓰지 않아 `thread_id`는 사건 번호 앞머리와 응답에만 쓰임** · 「Ch24의 중복 실행 방지 원칙」 → 참(Ch 24 인계 — 01 b4·6절에 기댐). b4 「Ch31에서 실행과 이벤트를 저장하면 동일 이벤트를 재생할 수 있습니다」 → **Ch 31에 사건 저장 없음**(§5-4).
- 06·07 저장 출력에 **`logger.exception`의 Traceback 전문이 표준 오류로 찍힘**(파일 위치 `[사용자 폴더]/…`·맥 임시 폴더 `/var/folders/…` 포함) — Ch 28 선례처럼 노트북에서 기록을 조용히 할지 결정.

### 07 인증 CORS 타임아웃 (paired)
- 지금 Before(모르는 출처 → 사전 요청 400·허용 헤더 없음)는 **미들웨어가 제대로 막은 장면**(결함 아님). 모르는 출처의 사전 요청 없는 POST는 **200, 서버가 그대로 실행**(허용 헤더만 없음 — CORS는 브라우저 규칙이라는 증거).
- **실제로 재현되는 결함 후보(확인함, 결정적)**: ① **`allow_origins=["*"]` + `allow_credentials=True`** → Starlette 1.6이 **아무 출처나 그대로 되돌려 주고 `access-control-allow-credentials: true`**(`https://evil.example`로 확인) — FastAPI 문서 「None of allow_origins, allow_methods and allow_headers can be set to ['*'] if allow_credentials is set to True」 ↔ 출처를 적은 설정은 400 ② **401에 `WWW-Authenticate` 헤더가 없음**(지금 `require_token` — `e2_app.py`) ↔ FastAPI `HTTPBearer`는 **401 + `WWW-Authenticate: Bearer`**, OpenAPI에 `securitySchemes: {'HTTPBearer': {'type': 'http', 'scheme': 'bearer'}}`까지(`e5_security.py`) — **Ch 28 03(401·`WWW-Authenticate: Bearer`·「접근 토큰」)과 말·동작을 맞출 수 있음** ③ 시간 제한 0 → 단일 504·스트림 `event: error`(5/5, `SlowAgent` 클래스 없이).
- 지금 코드의 `SlowAgent`(클래스·`yield`·`lambda` 둘)는 G1 넷 — ③으로 갈음 가능. 「토큰」 단독 7번 → Ch 28 인계 「접근 토큰」. 지금 앱은 인증을 **헤더 매개변수 `authorization`**으로 받아 OpenAPI에 보안 정보가 없음(08과 이어짐).
- b3 「Ch16에서 입력 **검증**과 비용 상한을, Ch22에서 호출 전후 처리」(말). b4 비유 「건물 출입구」 → Ch 22 공항 검사·안내 데스크 계열과 겹침.

### 08 OpenAPI와 TS SDK (experiment)
- `app.openapi()`는 모델 없이 결정적(두 번 같음, `3.1.0`, 경로 5: `/health`·`/v1/chat`·`/v1/chat/live`·`/v1/chat/live/stream`·`/v1/chat/stream`). **실습 폴더 `openapi.json`(06e5d1b9…)은 지금 앱으로 새로 만든 글과 바이트 같음** → 08을 다시 돌려도 해시 그대로. 단 **앱을 고치면(보안 방식·경로를 바꾸면) 이 파일과 생성 SDK가 함께 바뀜**.
- **생성 SDK(`client/generated/` 18개, OpenAPI Generator 7.25.0 `typescript-fetch`)**: JSON 라우트는 `ChatResponse`를 받는 함수가 생기지만 **스트림 라우트 둘은 `Promise<void>`**(스트림을 읽지 못함) → SSE는 손으로 쓴 `stream.ts`가 맡는다는 b4 설명과 맞음. 생성 SDK는 **확장자 없는 가져오기·생성자 매개변수 속성** 때문에 Node 타입 지우기로 못 돎(`ERR_MODULE_NOT_FOUND …/generated/runtime` 확인) → `tsx`나 `tsc`가 필요.
- **생성은 노트북 밖**: README `npx @openapitools/openapi-generator-cli generate --skip-validate-spec …`(Java 11 이상 필요 — **이 기기에 OpenJDK 11.0.32 있음**, 첫 실행 때 jar를 받음) · `npx --package typescript@latest tsc …`(**판 고정 없음 — 지금 `typescript` 최신은 7.0.2**) · `npx tsx client/test_stream.ts`.
- b6 「같은 앱 객체의 두 직렬화 결과는 같았습니다」 — 결정적이라 실험이라기보다 성질 확인. b8 「Ch31에서는 이벤트를 데이터베이스에 저장해 프로세스 재시작 뒤에도 복구」 → **Ch 31에 없음**. 옛 확인 기록(`qa/verification.md`)은 Node 25.9.0으로 생성·`tsc` 통과라고 적음(맥).

### 09 실제 Agent HTTP 통합 (experiment)
- 요청 여섯 가운데 **둘은 HTTP를 거치지 않은 따로 실행**(도구 차례를 보려고 `live_agent.ainvoke`를 한 번 더) → 앞 HTTP 호출과 같은 궤적이 아님(09 마크다운이 밝힘). Ch 29 04 「요청 수 셈」(도구를 요청한 응답 수 + 1)을 쓰면 셈으로 정리 가능.
- `assert '18:00' in response.json()['answer']`·`in live_answer` — **모델 글에 건 `assert`(규격 §3 위반)** · `tool_call['args']['day'] == '월요일'` — 모델이 고른 인자(흔들림 확인 전엔 `assert` 못 함 — 흔들림 확인 5/5 뒤 한정어로만).
- 모델 셀이 앱 파일 안이라 노트북에 `temperature`·`reasoning_effort` 줄이 안 보임 · `/v1/chat/live`는 `TimeoutError`를 504로 바꾸지 않음(500) · `/v1/chat/live/stream`은 노드 이름 `model`·`content_blocks`의 `type == "text"`만 보냄(Ch 25 02 칸 `metadata` 뜻과 맞음) · 모델 객체는 `@lru_cache`로 한 번만.
- b3 「Ch25에서는 stream_mode="messages"에서 모델 메시지 청크와 실행 메타데이터를 읽었습니다」 → 뜻은 참(Ch 25 02), 말은 「스트림 청크」·「칸 `metadata`」. **b6 「Ch29 평가셋으로 도구 선택과 최종 답을 반복 평가하고」 → Ch 29에 평가셋·반복 평가 없음**(Ch 29 인계). b8 「Ch31에서는 실제 Agent 실행과 이벤트를 데이터베이스에 저장」 → **Ch 31에 없음**. 「엔드포인트」 3·「경로」 4/5.

## 3. paired 절 Before 판정 (§5-3 빨강 = Before 결함 결과)

| 절 | 지금 Before | 실제 결함인가 | 모델 없이 결정적인가 | After가 결함을 고치는가 | 실제 결함으로 바꿀 후보(모두 모델 없이 결정적 — 확인함) |
|---|---|---|---|---|---|
| 01 | 빈 글 → 422 | **아님**(검사가 제대로 막음) | 예 | 아님(입력만 바꿈) | 스키마 없는 라우트 → 빈 질문이 몸통까지 ↔ `Field(min_length=1)` 422 / 결과 상태 전체 노출 ↔ `response_model` |
| 02 | 재정의를 남겨 다음 질문도 대체 응답 | **예**(실제 상태 누수 — Ch 2 11 b8이 기댐) | 예 | 예(`.clear()`) | 같은 장면을 클래스·`lambda` 없이: 시간 제한 제공 함수 재정의 504 → 다음도 504 → `.clear()` 200(5/5) |
| 03 | 「오류」 글자 → `RuntimeError` | 앱이 **일부러 던진 예외**(실패 흉내) | 예 | 아님(질문만 바꿈) | 비동기 노드 그래프에 동기 `invoke` → `TypeError` ↔ `await ainvoke` / `/v1/chat` 예외 → 500 ↔ 받아서 오류 코드 |
| 06 | 「오류」 글자 → 200 + `event: error`, 상태만 보고 성공 판정 | 판정 쪽 결함은 **예**, 예외는 **일부러 던짐** | 예 | 예(사건 종류 검사) | 시간 제한 0(실제 조건) → 200 + `event: error`·`done` 없음 / 마지막 번호를 안 보내 이어 붙인 답이 겹침 |
| 07 | 모르는 출처 사전 요청 → 400·허용 헤더 없음 | **아님**(미들웨어가 제대로 막음) | 예 | 아님(인증 헤더를 붙인 다른 요청) | `allow_origins=["*"]`+자격 증명 → 아무 출처나 되돌려 줌 ↔ 출처 명시 / 401에 `WWW-Authenticate` 없음 ↔ `HTTPBearer` |

## 4. 실습 폴더 구조와 읽는 곳

```
labs/part7/ch30-fastapi-serving/
  README.md (e58431d2… — uv sync / fastapi dev / pytest / npx 생성·tsc·tsx 안내, 「교육용 토큰」)
  pyproject.toml (a410ea2a…) · uv.lock (59c86868…, 2026-09-11)
  openapi.json (06e5d1b9… — 08이 다시 씀) · openapitools.json (생성기 7.25.0 고정)
  agent_service/ __init__.py(app 다시 내보냄) · schemas.py(ChatRequest·ChatResponse·HealthResponse)
                 agent.py(결정적 그래프 a6c42e63…) · app.py(라우트 다섯·CORS·인증·시간 제한 3455d405…)
                 live_agent.py(create_agent + @tool, 586a6a69…) · __pycache__/(맥 pyc 다섯)
  tests/test_app.py (6 tests, f8611741…) · tests/__pycache__/(pyc 둘)
  client/ stream.ts(a27e5db5…) · test_stream.ts(d9a61c50…) · generated/(18 + .openapi-generator/FILES·VERSION·ignore)
  notebooks/ 01~09 .ipynb · _generate.py(옛 생성기 a9640d09…)
  .venv/ (macOS 판 171MB, uv 0.11.6) · .pytest_cache/
```

- **package.json·node_modules 없음**(npx가 그때그때 받음). `.env`는 프로젝트 맨 위만.
- **코드로 읽는 곳**(`grep -rn`, `.venv`·`before` 제외): `agent_service`는 노트북 02·05·06·07·08·09(`from agent_service.app import …`)·03·04(`agent_service.agent`)·09(`agent_service.live_agent`)·`tests/test_app.py`·README `fastapi dev agent_service/app.py`가 가져옴. 노트북 준비 셀은 **지금 폴더와 부모 폴더에서 `agent_service`가 있는 곳을 찾아 `os.chdir`**. `client/stream.ts`는 `test_stream.ts`만, `client/generated`는 README `tsc`만, `openapi.json`은 08(쓰기)·README(생성 입력 — 실제로는 `http://127.0.0.1:8000/openapi.json`을 가리킴). **뒤 챕터 코드·검사가 읽는 Ch 30 파일은 없음**(§5-4) — Part 7 묶음 실행 검사가 **01 노트북**을 실행(§5-5).
- **`run_section.sh`와 부딪힘(중요)**: `execute.py`는 커널을 **저장소 맨 위에서** 띄움(`--cwd` 기본값 = 루트, 132행) → 지금 준비 셀(지금 폴더·부모 폴더에서 찾기)은 루트에서 `agent_service`를 못 찾아 **`assert`로 멈춤**. `run_section.sh`가 더하는 `PYTHONPATH`는 `notebooks/`뿐이라 맨 위 패키지를 가져오지 못함. → 준비 셀 후보에 `labs/part7/ch30-fastapi-serving`을 넣거나(Ch 28 01 `candidates = ["../course_server.py", "course_server.py", "labs/part6/ch28-mcp/course_server.py"]` 선례) 앱 파일 자리를 바꿔야 함(§8·§13).
- `run_section.sh`의 `--with python-dotenv==1.2.3`은 **잠금 `python-dotenv==1.2.1`과 다름**(겹쳐 설치된 판으로 실행됨 — 교재 출력 판 표기에 주의).
- 옛 생성기와 부르는 곳: `_src/_generate.py`(79c8c6f6… — `_src` 아홉을 틀 글로 덮어씀) · `notebooks/_generate.py`(a9640d09… — 노트북 아홉을 출력 없이 덮어씀) · `figures/_gen_figures.py`(dbd4ec67… — `textbook/part5/_figure.py` 7f1c64ca…로 SVG·excalidraw) · **`.moai/…/part7_apply_depth.py`(3c217354…)·`part7_review_fixes.py`(eadfd1c2…)·`part7_final_repairs.py`(05c32efe…)** — Ch 30~34 `_src`·노트북을 씀. **Part 7 공용 생성기(Part 6 `_author_ch21_ch29.py` 같은 것)는 없음.** 부르는 빌드·검사 스크립트 0(`grep`), 단 **Part 7 `qa/check_figures.py`가 챕터마다 `figures/_gen_figures.py`가 있는지 `assert`**(§5-5).
- 잠금 판: `fastapi 0.135.0`(`[standard-no-fastapi-cloud-cli]` — `fastapi-cli 0.0.32`·`uvicorn 0.52.4`·`uvloop 0.22.1`·`httptools 0.8.0`·`watchfiles`·`websockets`·`jinja2`·`python-multipart`·`email-validator`) · `starlette 1.6.0` · `pydantic 2.12.5` · `httpx 0.28.1` · `langchain 1.4.0` · `langchain-core 1.6.2` · `langchain-openai 1.6.0` · `langgraph 1.2.11`(`langgraph-checkpoint 4.2.0`·`langgraph-prebuilt 1.1.0`) · **`openai 3.13.0`** · **`python-dotenv 1.2.1`** · dev `ipykernel 7.3.0`·`nbclient 0.11.0`·`pip 26.2`·**`pytest 9.0.2`**·`pytest-asyncio 1.3.0`. **Part 6과 다른 것**: `pydantic 2.13.5 → 2.12.5`(Ch 19와 같음) · `python-dotenv 1.2.3 → 1.2.1` · `openai 3.11.0 → 3.13.0` · `sse-starlette` 없음(FastAPI 기본 SSE).
- 실습 폴더 테스트: `pytest -q -p no:cacheprovider`(가상환경, 쓰기 0) → **6 passed, 1 warning**(Starlette `TestClient`의 anyio 별칭 경고).

## 5. 앞뒤 챕터 이음새

### 5-1. 앞 챕터 인계 — 항목별 지금 상태

| 넘긴 챕터 | 자리 | 지금 원고 | 판정 · 할 일 |
|---|---|---|---|
| Ch 29 §16-1·§17 | 03 b7 · 09 b6 · `_src/_generate.py` | 「Ch29 평가셋으로 확인」·「Ch29 평가셋으로 … 반복 평가」 | **틀림**(평가셋·반복 평가·결과 파일 없음) — 「Ch 29의 궤적 맞춰 보기·평가 모델 판정으로」처럼 |
| Ch 29 §16 | 01 b2·b3 · 01 슬러그 | 요청·응답 모양 | 참 — 슬러그 고정 |
| Ch 29 §16-2·3 | — | Ch 29 파일을 읽지 않음 | 참(파일 계약 없음, `eval_tools.py`는 Ch 29 폴더에만 — 잠금이 다르므로 파일째 가져오지 말 것) |
| Ch 25 인계 | **04 b2** | 「첫 응답 지연을 줄이지만」 | **Ch 25 근거 아님** — 문서 근거·이 절의 부등식·삭제 중 하나(§2 04) |
| Ch 25 인계 | 01 「조각」 · 03 b3 「소비」 · 04·05 b3 「진행 이벤트」 · 09 b3 「메시지 청크·실행 메타데이터」 | — | 뜻은 참, 말은 Ch 30 몫(스트림 사건·진행 값·스트림 청크·칸 `metadata`) |
| Ch 25 04 b8 | 04·09 슬러그 링크 | 「custom의 사건을 astream으로 이어 붙임」·「messages 스트림 청크를 서버 응답으로」 | 참 — **04 custom·09 messages 유지, 슬러그 고정** |
| Ch 28 §17 | **07·02** | 「토큰」 단독 · 문자열 비교 인증 · 401(헤더 없음) | 「접근 토큰」 말 · 401 + `WWW-Authenticate: Bearer` 맞춤 여부 결정(`HTTPBearer`로 그대로 됨 — §2 07) |
| Ch 28 `labs/part6/continuity-guide.md` 14행 | 「Ch30 FastAPI 서빙의 요청 헤더 인증」 | 07 인증 의존성 | 참(요청 헤더 인증을 유지하면) |
| Ch 23 인계 | 02 b3 | 「생성 비용과 수명주기」 | **수명만 참** — 「수명」만 남기거나 이 절이 보임 |
| Ch 23 인계 | 06 b3 | 「Ch23의 thread 분리」 | 참(단 앱은 체크포인터를 쓰지 않음) |
| Ch 24 인계 | 06 b3 | 「Ch24의 중복 실행 방지 원칙」 | 참(Ch 24 01 b4·6절 — 그쪽을 지우면 인계) |
| Ch 21 인계 | 01 b3 | 「Ch21에서 Agent 실행 객체」 | **말 틀림** — 「에이전트 그래프(`create_agent`의 결과)」 |
| Ch 21 인계 | 03 b3 · 09 b3 · `agent.py` 11행 | 「상태 사전」 · 「init_chat_model과 create_agent」 · `AgentState` | 「사전」 금지어 · 참 · 같은 이름 셋째(뒤에서 쓰면 어느 것인지 적기) |
| Ch 26·27 | — | Ch 30 줄 없음 | Ch 26은 Part 7 `existing-artifacts-before.json`의 옛 해시만(§5-5) |

### 5-2. 앞 챕터에서 가르친 것 (Ch 30이 전제할 수 있는 것)
- **비동기**: Ch 2 12 `async def`·`await`(셀 맨 위 await는 IPython 기능)·`asyncio.sleep`·`asyncio.gather(코루틴, 코루틴)`·`.py`의 `asyncio.run` · Ch 18 03 `asyncio.to_thread`·`gather(*…)` · Ch 28 셀 맨 위 `async with`·`async def` 셀당 하나·`ainvoke`(04). **아직 안 가르친 것**: `async for`·비동기 생성기(`yield`)·`asyncio.wait_for`·`asyncio.timeout`·취소·`create_task`(Ch 2 요약 전제 금지) · **`yield` 자체는 Ch 2 09(B 트랙)만**.
- **스트리밍**: Ch 6 04 스트림 청크 · Ch 25 동기 `stream`·모드 일곱·모드 목록 짝·`get_stream_writer()` 진행 값(custom)·`messages` 짝 `(AIMessageChunk, 칸 metadata)`·세 시간(차례·부등식만 결론).
- **HTTP**: Ch 4 04 `httpx.get`·상태 코드·헤더 · Ch 28 03 `httpx.post`·401·「접근 토큰」·127.0.0.1 자식 프로세스 규칙(포트 빔 → `poll() is None` → `terminate()`·`wait()`).
- **스키마·데코레이터**: Ch 2 10(B) `BaseModel`·Ch 6 01·03 세 문장 · Ch 19 02 `BaseModel`·`Field`·`Literal`(양식 클래스 칸) · Ch 2 09(B)·Ch 19 01 데코레이터 세 문장 + 링크 · Ch 13 02 **`Annotated`**(리듀서 표시) · Ch 21 03 `TypedDict` 칸만 · Ch 19 01·Ch 28 02 `: str` 힌트 예외.
- **에이전트**: Ch 21 `create_agent(모델 객체, tools=…, system_prompt=…)` · Ch 22 04 `ModelCallLimitMiddleware` · Ch 27 02 요청 수 셈 · Ch 16 05 `except TimeoutError` · Ch 15 05 `time.perf_counter`(시간이 주제인 절만).

### 5-3. 완료 챕터가 Ch 30에 기대는 문장 — 개선 뒤에도 참이어야 함

| 파일 | 문장 | Ch 30 쪽 조건 |
|---|---|---|
| Ch 1 01 `_src`·HTML·`author_01.py` 73행 | 과정 지도 「Part 7 서비스화와 배포 · Ch 30~34 · W15~W17」 | 참 |
| Ch 2 `_src/index.html` | 「비동기 대기는 Ch 18의 API 호출과 Ch 30의 FastAPI에서 다시 사용합니다」 | 참 |
| **Ch 2 11 b8** | 「Ch 30 2절에서는 한 테스트가 남긴 대체 설정이 다음 질문까지 이어지는 실패를 다룹니다」 | **02 Before가 재정의 누수 장면이어야 참** |
| **Ch 2 12 b8** | 「Ch 30 1절은 비동기 함수 안의 동기 호출이 이벤트 루프를 멈출 수 있다고 설명합니다. Ch 30 3절은 await로 Agent 실행을 기다립니다」 | **01에 그 설명, 03에 `await ainvoke`가 있어야 참** |
| **Ch 25 04 b8**(+ `author_04.py` 534~535행 링크 상수) | 04·09 슬러그 링크와 모드 문장 | **04 custom·09 messages·슬러그 고정** |
| Ch 25 `author_02.py` 23행 | 주석 「Ch 30 09 실행 메타데이터」(생성기 주석) | 기록 |
| Ch 24 `author_01.py` 28행 | 주석 「Ch 30 06 중복 실행 방지 원칙」 | 기록 |
| **Ch 29 05 b8**(+ `author_04.py` 776행·`author_05.py` 651행) | 「Part 7 Ch 30 01절에서는 웹 서비스가 받을 요청과 내놓을 응답의 모양을 정합니다」 + 01 슬러그 링크 | 01 b2·b3·슬러그 |
| `labs/part6/continuity-guide.md` 14행 | 「Ch30 FastAPI 서빙의 요청 헤더 인증」 | 07 |

- 슬러그를 바꾸면 Part 7 `check_delivery.py`의 링크 검사가 멈추고(Part 6 HTML은 검사 밖이지만 학생 화면 링크가 깨짐) 완료 챕터 `_src`·생성기·HTML을 고쳐야 함(Ch 29 마감 「완료 챕터 문장은 `_src`·생성기·HTML만」 선례).

### 5-4. 뒤 챕터(대기)·Part 7이 Ch 30에 기대는 것 — 고치지 않음

| 파일 | 내용 | 계약 여부 |
|---|---|---|
| Ch 31 01 `_src` b2·b3 | 「Ch30에서 FastAPI 요청 함수를 비동기로 작성했습니다」 | 글만(참) |
| Ch 34 04 `_src` b3 | 「Ch 30에서는 FastAPI 비동기 요청 처리를 배웠습니다」 | 글만(참) |
| Part 7 `_src/index.html` | 「Ch30의 요청·응답 형식에서 시작해 …」 | 글만(참) |
| `labs/part7/continuity-guide.md` 7·8행 | 「Ch2의 비동기 함수와 Ch25의 스트리밍 → Ch30 HTTP 요청과 SSE 이벤트」·「Ch21의 에이전트, Ch23의 저장 상태 → Ch30의 호출 경계와 Ch31의 데이터 저장」 | 글만(7행 「이벤트」, 12행 「Ch6·29의 사용량·지연 측정」·11행 「Ch38」 — Part 7 마감 몫) |
| `labs/part7/ch32-docker/README.md` 3행 | 「이 폴더는 Ch30 결과에 의존하지 않는 최소 FastAPI 서비스」(`fastapi 0.135.1`, 자기 `app.py`) | **의존 없음** |
| Ch 33 CI(`.github/workflows/ci.yml`) | 자기 폴더 `pytest`·`evaluate_regression.py`만 | **Ch 30 테스트를 돌리지 않음** |
| Ch 31 | 표 `tickets`·트랜잭션·Alembic·연결 풀·pgvector 체크포인터 — **SSE 사건·에이전트 실행 저장 없음, Ch 30 앱을 이어 쓰지 않음** | 없음 → Ch 30 06 b4·08 b8·09 b8의 Ch 31 예고 문장은 **사실과 다름**(Ch 30 쪽에서 고칠 것) |
| 제외 챕터 Ch 32·33 | 실습 절 없음(사용자 결정) | 없음 |

### 5-5. Part 7 묶음·목록·기록·검사

- **목록**: Part 목록 `textbook/part7/public-files.json`(c823d407…, Ch 30 **40줄** — 노트북 아홉·앱 다섯·테스트·TS 21·README·잠금 둘·`openapi*.json` 둘) · 챕터 `qa/public-files.json`(ce9b4d52…, 40줄, **옛 SVG 줄 없음**) · **선행 목록 `prerequisite-files.json`은 Ch 15 `batch-eval-input.jsonl` 한 줄뿐 — Part 6 파일을 읽지 않음**(Ch 34 몫). `collect_public_files.py`가 챕터 목록 다섯 + `continuity-guide.md`로 Part 목록을 다시 만듦(다섯 챕터 `assert`).
- **묶음** `textbook/downloads/part7-practice.zip`(1e805674…, 111항목 = 시작하기·`env.example`·`manifest.json` + 108파일 — **디스크와 108/108 같음**) ← `python3 -B textbook/part7/_build_index.py`(Part 7 29절 `verify_lesson` 모두 → `index.html`·zip·`qa/integration-results.json`). **절 수 검사 없음**(Part 6과 다름 — 절 수는 `chapter.json`에서 셈, 「Ch 30–34 · N절」 자동, 「총 88시간 · 강의 28 · 실습 60」은 손 글).
- **묶음 실행 검사** `textbook/part7/qa/check_bundle_execution.py`(Part 6 판과 다름): zip을 임시 폴더에 풀어 **다섯 챕터 모두 `uv sync --locked`**(네트워크·디스크 큼) → `import ipykernel, pip` → **Ch 30 01**·Ch 31 03·Ch 33 02를 `execute.py`로 `notebooks/`에서 실행(`code_sha256` 대조는 **안 함** — 기록만) · 실행기 파이썬이 **`labs/part7/ch31-database/.venv/bin/python`(맥 판)이라 이 기기에서 그대로는 못 돎** · `bundle-execution.json`(Ch 30 01 `7bd57d1f…` 기록). → **01에 키·모델·`dotenv`를 넣으면 묶음에서 멈춤**(Part 6 선례와 같은 계약, 포트·자식 프로세스도 피하는 것이 안전).
- **옛 검사 스크립트(고치지 않음, 결과 파일을 쓰므로 돌리지 않고 읽어서 판정)**: `check_delivery.py` — b1~b10·복습 3~5·링크·zip 대조 뒤 **`existing-artifacts-before.json`(376개) 해시 대조에서 멈춤(지금 375개 바뀜·1개 없음 — Part 1~6 개선 때문)** + `llm-practice.zip` 대조 · `check_figures.py` — **챕터마다 `figures/_gen_figures.py`가 있어야 하고(`assert`) SVG·excalidraw 짝·상자 1~7** → 마감에서 옛 생성기·옛 그림을 옮기면 Ch 30에서 멈춤 · `check_secrets.py`·`check_special_secret.py` — 비밀값 대조(결과 파일 씀) · `final-artifact-hashes.json`(232개 중 87개 이미 다름 — 기록 파일) · `existing-artifacts-before.json`은 **기록이 아니라 `check_delivery.py`의 입력**(Ch 26 요약 「검사 입력 아님」과 다름 — 확인).
- `textbook/_notebook/build_index.py` 64행 Ch 30 절 수 **9**(실습 절을 빼고 세는 과정 약속 — 그대로) · `build_bundle.py` 28행 Part 7 목록 · `check_course_continuity.py`는 Part 7을 보지 않음(`grep` 0).

## 6. Part 7 구조 — Part 6과 다른 점

| 항목 | Part 6 | Part 7 |
|---|---|---|
| 챕터 빌드 | 챕터 `_build.py`(공용 `builder.build_chapter`) | 같음 — `{{mermaid:}}`·`{{img:}}` 치환 있음(`builder.py` 103·116행) |
| 목차 스크립트 | `_build_index.py` 절 수 검사 있음 | **절 수 검사 없음**, 챕터 시수 `(강의, 실습)` 표만 · Part 시수 손 글 |
| 선행 목록 | Part 5 이전 파일 13줄 | **Ch 15 파일 한 줄**(Ch 34용) |
| 묶음 실행 검사 | Ch 24 01·Ch 28 01, `code_sha256` 대조, `uv run` 하나 | **Ch 30 01·31 03·33 02**, 대조 없음, **다섯 챕터 `uv sync --locked`**, 실행기 = Ch 31 맥 `.venv` |
| 전달 검사 | `llm-practice.zip` Stale에서 멈춤 | **`existing-artifacts-before.json` 해시 대조에서 멈춤**(+ `llm-practice.zip`) |
| 그림 검사 | `check_figures.py`(excalidraw 짝) | 같은 짝 + **`_gen_figures.py` 존재 `assert`** |
| 챕터 모양 | 챕터마다 도구 파일·노트북만 | Ch 30 앱 패키지·TS·생성 SDK · Ch 31 Alembic · Ch 32 Docker · Ch 33 Actions — **README 터미널 명령이 실습의 한 축** |
| 옛 생성기 | 공용 `_author_ch21_ch29.py` 등 | 챕터 `_src/_generate.py`·`notebooks/_generate.py`·`figures/_gen_figures.py` + `.moai` part7 스크립트 셋 |

## 7. 설치판 동작 — 모델 없는 확인 (2026-09-29, 가상환경 = 잠금 판)

### 7-1. 서버 없이 요청 보내기와 스트림 읽기 (`e2`·`e3`)
- **`fastapi.testclient.TestClient(app)`**: 포트 없이 결정적. `/health` 200 · 422 본문 · 401 · CORS 사전 요청 · 스트림 전문 모두 확인. 기본은 앱 안 예외를 그대로 올림(`raise_server_exceptions=False`면 500). `lifespan`은 `with TestClient(app) as client:`일 때만 돎(문서).
- **스트림 도착 시각(0.4초 간격 사건 셋)**: `TestClient.stream` + `iter_lines` → 네 줄 모두 **1.22초**(앱이 끝난 뒤 한꺼번에) · **`httpx.AsyncClient(transport=httpx.ASGITransport(app=app))` + `aiter_lines` → 모두 1.21초**(마찬가지로 끝까지 모아 줌) · **uvicorn 자식 프로세스(127.0.0.1 빈 포트) + `httpx.stream` → 0.42·0.82·1.23초**(사건마다 도착). → **「먼저 온 사건부터 처리」를 HTTP로 보이려면 uvicorn 자식 프로세스가 필요**(Ch 28 03 규칙). 같은 프로세스 `graph.astream`은 사건이 생기는 때에 옴(0.31·0.61·0.92초).
- uvicorn 자식 프로세스: `subprocess.Popen([sys.executable, "-m", "uvicorn", "모듈:app", "--host", "127.0.0.1", "--port", 빈 포트, "--log-level", "warning"])` → 준비 확인(`/health` 또는 `/docs`) → `terminate()`·`wait()`(−15). 실습 앱은 `--app-dir labs/part7/ch30-fastapi-serving`로 가져옴(pyc 0 — `PYTHONDONTWRITEBYTECODE=1`).

### 7-2. `astream`·`ainvoke` (`e4`)
- langgraph 1.2.11 `Pregel.astream(input, config, context, stream_mode, print_mode, output_keys, interrupt_before, interrupt_after, durability, control, subgraphs, debug, version, **kwargs)` · `ainvoke`도 같은 무리 · `astream_events(input, config, version, include_*, exclude_*)`(Runnable). 모드 목록이면 `(모드, 자료)` 짝, 한 모드면 자료만. 문서: `version="v2"`면 늘 `type`·`ns`·`data`.
- **비동기 노드 그래프에 동기 `invoke`·`stream` → `TypeError: No synchronous function provided to "answer"…`**(실습 그래프·임시 그래프 모두).
- `get_stream_writer()`는 Python 3.11 이상 비동기 노드에서 됨(문서: 3.11 미만이면 노드 매개변수 `writer`로) — 기기·학생 3.12.
- 실습 그래프 custom 사건: `[{'token': '질문을 '}, {'token': '확인했습니다: '}, {'token': '세 '}, {'token': '단어 '}, {'token': '질문 '}]`(저장 출력과 같음).

### 7-3. 실습 앱 동작 (`e2`·`e6`, 결정적)
- `/v1/chat` 200 `{'answer': '질문을 확인했습니다: 안녕하세요', 'thread_id': 't-1'}` · 빈 글 422 `string_too_short` · 501자 `string_too_long` · `thread_id` `bad id!` → `string_pattern_mismatch` · 인증 없음·틀림 401 `{'detail': '인증 정보가 올바르지 않습니다'}`, **`WWW-Authenticate` 없음**.
- 스트림 전문(`sse-1`): `event: token` → `data: {"token": "질문을 "}` → `id: sse-1:0` … 넷 → `event: done` / `data: {"thread_id": "sse-1"}`, 머리 `text/event-stream; charset=utf-8`·`cache-control: no-cache`·`x-accel-buffering: no`. 이어 받기 `sse-1:0` → 첫 id `sse-1:1` · 다른 스레드 400 · 범위 밖 `sse-1:99` → `done`만.
- **시간 제한 0 재정의(실제 조건)**: `/v1/chat` 504 `Agent 응답 시간이 초과되었습니다` · 스트림 200 + `event: error`(`stream_failed`) · `.clear()` 뒤 200 — **5/5 같음**. 재정의를 남기면 다음 질문도 504.
- CORS: 허용 출처 사전 요청 200 + `access-control-allow-origin: http://localhost:5173`·`…-credentials: true`·`…-headers: Accept, Accept-Language, Authorization, Content-Language, Content-Type, Last-Event-ID`·`max-age 600` · 모르는 출처 사전 요청 **400 `Disallowed CORS origin`**(허용 출처 헤더 없음) · 모르는 출처 보통 POST 200(허용 출처 헤더 없음, 서버는 실행).
- 오류 사건을 낼 때 `logger.exception`이 **Traceback을 표준 오류로** 찍음(기록 설정이 없으면 파이썬 기본 처리기가 ERROR를 보냄).

### 7-4. 보안 방식·CORS 잘못된 설정 (`e5`)
- `HTTPBearer()` + `Depends` → 헤더 없음·`Basic` **401 `{'detail': 'Not authenticated'}` + `WWW-Authenticate: Bearer`**, `Bearer abc` 200 · OpenAPI `securitySchemes` 생김. 설치판 `fastapi/security/http.py`가 `WWW-Authenticate`를 붙이고 401을 씀.
- `allow_origins=["*"]`+`allow_credentials=True`+`allow_methods=["*"]`+`allow_headers=["*"]` → `https://evil.example` 사전 요청 200·**허용 출처 `https://evil.example`·자격 증명 `true`**, 보통 요청도 같음.

### 7-5. OpenAPI (`e2`·`e7`)
- `app.openapi()` 두 번 정렬 직렬화 같음 · `openapi: 3.1.0` · 스트림 라우트 200 `text/event-stream`에 **`itemSchema`**(칸 `data`·`event`·`id`·`retry`) · `securitySchemes` 없음 · 인증은 헤더 매개변수 `authorization` · **실습 폴더 `openapi.json` = `json.dumps(app.openapi(), ensure_ascii=False, indent=2)`와 바이트 같음**.
- 반환 힌트 없이 `yield`만 하는 라우트도 SSE(`response_class`가 있을 때) · `response_class` 없으면 `application/jsonl` · `Header()`는 `last_event_id` 매개변수를 `last-event-id` 헤더로 알아서 이음(`alias` 없이) · `word=Depends(get_word)`(기본값 모양)도 됨.

### 7-6. TS 클라이언트·SDK 생성
- 기기: **Node v22.23.2**(`process.features.typescript` = `strip`), npm·npx 있음, **OpenJDK 11.0.32** 있음. `node client/test_stream.ts`가 npm 설치 없이 돎(§2 06). 생성 SDK는 Node만으로 못 돎(§2 08).
- 도구 크기(npm 정보만 봄 — 설치 안 함, 2026-09-29): `@openapitools/openapi-generator-cli` 2.41.0(자기 91KB + 의존 패키지 + 첫 실행 때 jar 7.25.0, Node ≥22, Java ≥11) · `openapi-typescript` 7.13.0(0.9MB, 타입만 만듦 — Java 필요 없음) · `@hey-api/openapi-ts` 0.99.0(2.9MB, Node ≥22.18) · `typescript` **7.0.2**(2.5MB + 기기별 바이너리) · `tsx` 4.23.15(0.4MB + esbuild 바이너리) · `openapi-fetch` 0.17.0(0.2MB). 정확한 설치 크기는 의존 패키지까지 합쳐야 해서 어림만(openapi-generator 경로 수십 MB, openapi-typescript 경로 수 MB).
- `npm view`가 사용자 홈 `~/.npm/_cacache`(`/sessions` 디스크)에 정보 캐시 21MB를 남김(지우지 않음).

## 8. §2-7 판단 근거 — 도구 파일·앱 파일

### 사실
- 절끼리 되풀이하는 코드: **준비 셀(실습 폴더 찾기)** 아홉 절 글자 같음 · 인증 헤더 딕셔너리 `{'Authorization': 'Bearer local-demo-token'}` 02·05·06·07·09 · `TestClient(app)` 02·05·06·07·09 · **SSE 글을 빈 줄로 나눠 사건 목록 만들기** 05·06·09(`re.split(r'\r?\n\r?\n', …)`·`re.findall(r'id: …')`·`data:` 줄 `json.loads`) · token 글 이어 붙이기 04·09 · 상태 코드와 JSON 출력 여러 절.
- 앞 챕터 함수로 가져올 만한 것: Ch 19·21 `tool_call_names`·`show_messages`·`sum_usage`·`estimate_cost`(09 요청 수·비용 — **Ch 21 `runner_tools.py`와 같은 본문**이 Ch 25~29 도구 파일에 반복) · Ch 29 04 요청 수 셈 · Ch 28 03 노트북의 포트 확인 함수(`wait_for_port` — 도구 파일 아닌 노트북 함수) · Ch 25 `collect_events`·`positions_of`(동기 `stream`용이라 그대로는 못 씀).
- 도구 파일 이름 과정 목록(`find labs -name '*_tools.py'`): `llm_tools`(3)·`rag_tools`(7)·`git_tools`·`data_tools`·`agent_tools`·`workflow_tools`·`order_tools`·`graph_tools`·`runner_tools`·`checkpoint_tools`·`approval_tools`·**`stream_tools`(Ch 25)**·`delegation_tools`·`harness_tools`·`connect_tools`·`eval_tools` + `guardrails.py`. **쓸 수 있는 후보**: `serve_tools.py`·`sse_tools.py`·`http_tools.py`·`api_tools.py`(`stream_tools`·`agent_tools`는 겹침).
- 앱 파일과 도구 파일의 관계: 앱(`agent_service/`)은 노트북·테스트·README 명령·TS 클라이언트가 함께 쓰는 **서버 코드**, 도구 파일(`notebooks/`)은 **노트북이 가져오는 읽기·출력 함수**. 앱 파일은 `run_section.sh`의 `PYTHONPATH`(`notebooks/`) 밖이라 지금 모양으로는 루트 실행에서 못 가져옴(§4).

### 선택지 (결정하지 않음 — 장단점만)
- **앱 코드 자리** — (A) 지금처럼 맨 위 패키지를 노트북이 가져옴(준비 셀 후보에 루트 기준 자리 + `os.chdir`) — 장: README·테스트·TS와 같은 앱, 단: 학생이 여는 `app.py`가 금지 문법 투성이(Ch 28 A-17 선례면 고쳐야 함)·`os.chdir` 뒤 08이 맨 위 파일을 씀·상대 가져오기 때문에 `runpy.run_path` 불가 / (B) 절마다 노트북에서 작은 앱을 직접 적고 키움, 패키지는 README·테스트용 완성판 — 장: 절 학습 목표가 코드에 보임·가져오기 문제 없음, 단: 노트북 앱과 패키지가 두 판(「같은 코드」 말 조심)·코드 늘어남(§2-7 「코드를 늘려 가며 개선할 필요 없다」) / (C) 앱을 파일 하나(절대 가져오기)로 합쳐 맨 위에 두고 Ch 28처럼 `runpy.run_path` — 장: 선례 있음·후보 셋으로 루트·실습 폴더·`notebooks` 모두, 단: 패키지 구조·README 명령·테스트 가져오기를 바꿔야 함 / (D) 앱을 `notebooks/` 안으로 — 장: `run_section.sh`·학생 커널 모두 바로 가져옴, 단: README `fastapi dev`·테스트·공개 목록 자리가 바뀜.
- **도구 파일** — (가) 만듦(SSE 나누기·인증 헤더·요청 수 셈 + Ch 21 판 넷) — 장: 05·06·09·실습 절 코드가 줄어듦, 단: 처음 가르치는 절(05)은 노트북에 남겨야 하고 생성기 대조 사슬 부담 / (나) 안 만듦 — 장: 단순, 단: 같은 나누기 코드가 넷 이상 되풀이 / (다) 앱 패키지에 넣음 — 단: 노트북 도구와 서버 코드가 섞임(§2-7 4번 「학생이 파일을 열어 봄」).

## 9. 모델·비용 선택지와 흔들림 처리 (결정하지 않음 — 장단점만)

### 9-1. 모델 없이 결정적으로 보일 수 있는 것 (확인함)
라우트·입력 형식 거절(422 종류 셋) · 응답 모양으로 거르기 · 의존성 주입·재정의 누수(504 사슬) · 동기 `invoke` `TypeError` · `ainvoke` 결과 키 · `astream` custom 사건 차례·이어 붙이기·도착 차례 부등식 · SSE 줄 모양·머리·`done` 한 번 · 이어 받기 번호·400 두 가지·범위 밖 · 시간 제한 0 → 504·`event: error` · CORS 허용·400·와일드카드 되돌려 주기 · 401·`WWW-Authenticate` · OpenAPI 결정성·`itemSchema`·`securitySchemes` · TS 클라이언트(Node + uvicorn).

### 9-2. 선택지
| 결정 | 실제 모델을 부르는 절 | 요청(노트북 한 번) | 장점 | 단점 |
|---|---|---|---|---|
| **M0** | 09만(지금과 같음) | 09 여섯(따로 실행 둘을 빼면 넷) | 01~08 전부 결정적·묶음 실행 검사 후보 많음·비용 거의 0 | 01~08의 「Agent」가 모델 없는 그래프라는 점을 매 절 밝혀야 함 |
| **M1** | 03·04 뒤 절반 + 09 | 03 둘 · 04 둘 · 09 넷~여섯 | `ainvoke`·`astream`을 실제 에이전트로도 봄(Ch 25 04 b8 「custom」은 앞 절반이 지킴) | 03·04 흔들림 확인(노트북 밖 5번) 필요·키 셀 늘어남 |
| **M2** | 03~09 전부 실제 에이전트 | 절마다 둘~여섯 | 서비스 현실감 | 05~07 결정적 검사가 흔들리는 글에 기댐·06 이어 받기가 다시 실행이라 글이 달라짐(결함이 드러나지만 결과가 매번 다름) |
| **M0′** | 09 + 실습 절 | 09 넷~여섯 · 실습 셋~다섯 | 규격 §7-2 실습 요청 수 안 | 실습 절에 키 필요 |

- **흔들림 처리(규격 §2-7 9번 끝·10번 끝)**: 09의 결정적 값 후보 = 상태 코드·마지막 사건 `done`·도구 결과 글(도구 함수가 정한 값)·요청 수 셈. 흔들리는 값 = 답 글·token 사건 수·도구 인자(`day`)·도구를 부를지·걸린 초·토큰·비용 → 결과 읽기 둘째 단락·표·b7에만. **`'18:00' in 답` `assert`는 빼고**, 도구 인자·도구를 부른 사실은 노트북 밖 5번·두 커널 같을 때만 한정어로(Ch 29 03 선례). 첫 요청 전에 `09-probe.md` §0(그림 라벨 규칙)부터(Ch 25·26 선례). 시간 값은 결론·그림·정리에서 뺌(Ch 25 03).
- **서비스 요청·비용 어림**(요금표 2026-09-17 mini 입력 0.75·캐시 입력 0.075·출력 4.50달러/100만 토큰 — 청구 금액 아님, 요청 하나 입력 약 300~400·출력 약 30~60토큰으로 어림): 요청 하나 약 0.0005달러 → 09 노트북 한 번(6) 약 0.003달러 · 09 작업 전체(흔들림 확인 5회 × 6 + 시험 1 + 새 커널 A·B = 약 48번) 약 0.025달러 · M1이면 03·04 각각 작업 전체 약 16번(약 0.008달러) · 실습 절 작업 전체 약 40번(약 0.02달러). **절마다 1달러 안**, 챕터 전체 어림 0.1달러 안.
- **Part 7 묶음 실행 검사 후보**(모델·키 없는 절): 지금 목록 **01**(계약) + 후보 02·05·06·07·08(08은 풀린 폴더에 `openapi.json`을 씀). 넣으려면 Part 7 스크립트를 고쳐야 하고(실행기 = Ch 31 맥 `.venv` 문제·다섯 챕터 `uv sync`), 준비 과제는 「모델·키·`dotenv`·포트·자식 프로세스 없음」 계약.

## 10. 과정 규칙과 부딪히는 것 (선택지와 장단점만)

### 10-1. 비동기 문법 — Ch 28 허용 범위(셀 맨 위 `async with`·await, `async def` 셀당 하나, `ainvoke`)에서 늘어나는 것
- 새로 필요: **`async for`**(04 — Ch 25가 미룸, 규격 L7 「비동기가 학습 목표」 조건 충족) · **비동기 생성기 `async def … yield`**(05 SSE 라우트 — A 트랙은 `yield` 처음, 06 `stream.ts`의 `async function*`도) · **`asyncio.wait_for`·`asyncio.timeout`(`async with`)**(03·07 — Ch 2 전제 금지 목록) · 라우트 함수 `async def`가 셀마다 하나 이상(라우트 + 제공 함수 → 셀 나누기로 해결).
- 선택지: (가) 학습 목표로 보고 절에서 처음 쓰는 자리마다 세 문장(뜻 → 일상 예 → 이 절 코드) — 장: 규격 L7 조건 그대로, 단: 새 문법이 한 챕터에 넷 / (나) `yield` 라우트는 앱 파일에만 두고 노트북은 읽기만 — 장: 노트북 문법 줄어듦, 단: 05 학습 목표(사건을 만드는 쪽)가 코드에서 안 보임 / (다) `asyncio.timeout` 대신 `wait_for` 하나로 통일(스트림은 `async with asyncio.timeout`이 필요 — 앱 쪽만).

### 10-2. 타입힌트·클래스·데코레이터 (FastAPI·Pydantic은 힌트가 동작을 정함 — Ch 28 MCP 도구 매개변수 힌트 예외와 같은 성격)
- 반드시 필요한 것: 본문 매개변수 힌트 `body: ChatRequest`(없으면 쿼리 매개변수로 읽음) · 스키마 클래스 `BaseModel` + `Field`(L5 — 칸만) · 헤더 매개변수(`Annotated[str | None, Header()] = None` 또는 `= Header(default=None)`) · 데코레이터 `@app.post(…)`(L6 — 세 문장 + Ch 2 09 링크) · 의존성(`Annotated[T, Depends(f)]`(Ch 13 02 `Annotated` 선례) 또는 기본값 모양 `x=Depends(f)` — **힌트 없는 기본값 모양도 됨, 확인함**) · 반환 힌트는 **필요 없음**(`response_model=`·`response_class=`로 갈음, 확인함).
- 선택지: (가) **챕터 예외 「FastAPI·Pydantic이 읽는 매개변수 힌트」**(Ch 28 `: str` 선례를 넓혀 본문·헤더·의존성 힌트까지, 반환 힌트·변수 힌트는 0) — 장: 공식 문서 모양, 단: 예외 범위 넓어짐(강사 확인) / (나) 기본값 모양 `Depends(f)`·`Header(default=None)`로 힌트 줄이기 — 장: 힌트 적음, 단: 기본값 매개변수(과정이 안 쓴 모양)·공식 문서가 권하는 `Annotated`와 다름 / (다) 준비용 클래스(`StubAgent`·`SlowAgent`)는 없애고 스키마 클래스만(§3 후보로 모두 갈음 가능).
- 앱 파일(`app.py`)의 `X | None`·`AsyncIterable`·`from __future__`·f-string·`except Exception`·`raise … from` — 학생이 여는 파일이면 Ch 28 A-17 선례로 고칠 대상(고치면 `openapi.json`·생성 SDK·테스트가 따라 바뀔 수 있음).

### 10-3. JS·TS 코드
- (가) 교재 본문에 `stream.ts` 조각만 싣고 실행은 README(지금) — 장: 파이썬 과정 흐름 유지, 단: 06 제목 「fetch」의 학습 목표를 노트북 출력으로 못 보임 / (나) 노트북에서 `subprocess.run(["node", "client/test_stream.ts"])` + uvicorn 자식 프로세스 — 장: **이 기기에서 확인됨**(Node 22.18 이상이면 설치 없이), 단: 학생 Node 판·포트 8000·자식 프로세스 둘 정리·묶음 검사 불가 / (다) 같은 재연결 규칙을 파이썬 `httpx` 스트림으로 보이고 TS는 비교표로 — 장: 결정적·과정 언어, 단: 「fetch」가 제목에만 남음.
- SDK 생성(08): (가) README로만(지금) / (나) 노트북에서 `npx`(Java·jar 다운로드·네트워크 — 새 커널 실행에 부적합) / (다) Java 없는 `openapi-typescript`로 바꿈(타입만 — 호출 함수 없음) / (라) 생성 결과(`client/generated`)를 읽기만 하고 「스트림 함수는 `Promise<void>`」 같은 사실을 보임 — 장: 결정적, 단: 앱을 고치면 생성물이 낡음(다시 만들려면 Java + jar).

### 10-4. 말
- **「경로」**(URL path): 과정 금지어(Ch 13~29, 파일은 「파일 위치」). 대체어 후보: 「요청 주소」(Ch 15 08 「요청 주소 `url`」 — 이미 과정 말) · 「주소 뒷부분」 · 「주소」. FastAPI 원어 「경로 연산(path operation)」은 한 번 풀고 「라우트 함수」 등으로.
- 「스키마」(Ch 20·21 금지 → 「양식」·「입력 형식」(Ch 19)) · 「필드」(→ 「칸」) · 「반환」(→ 「내놓다」) · 「검증」(→ 「검사」) · 「이벤트」(Ch 25 금지 → 「사건」, SSE 원어는 괄호 한 번) · 「주입」·「런타임」(Ch 21 금지) · 「토큰」 단독(→ 「접근 토큰」, 모델 토큰과 가름) · 「지연」·「측정」 · 「엔드포인트」·「라우팅」(Ch 18 「라우팅」은 다른 뜻 — 갈래로 보내기) · 「세션」(Ch 28 금지 → 「연결」) · 「조각」(Ch 5 토큰 전용) · 「청크」 단독(→ 「스트림 청크」) · 「사전」·「직렬화」·「식별자」·「보장」·「명시」·「결정적」.
- **제목의 영어·약어**: 「astream」·「SSE」·「fetch」·「CORS」·「OpenAPI」·「TS SDK」·「ainvoke」 — 선택지: (가) 「제목에만 남음(강사 확인)」(Ch 19~29 선례, 본문 첫 자리에서 풂) / (나) 제목을 한국어로(슬러그 01·04·09는 링크로 고정 — 제목만 바꾸고 슬러그 유지 가능). 「타임아웃」 → 「시간 제한」(Ch 30 본문 말과 맞춤) 후보.

## 11. 삽화 비유 계열 후보 (앞 챕터와 겹치지 않게)

앞 계열: Ch 3 창고 선반 · Ch 4 쟁반·카드 상자 · Ch 5 나무 쟁반·블록 · **Ch 6 01 도서관 상담 창구** · Ch 7·8 한 책상 색 약속 · Ch 10 도막 · Ch 11 흰 카드 · Ch 17 눈 위 발자국 · Ch 18 도예 · **Ch 19 식당 주문 전표와 내주는 창** · **Ch 20 자료실 승강 상자(택배 송장 금지)** · Ch 21 세탁기 · **Ch 22 공항 검사·안내 데스크** · Ch 23 체스판과 즉석사진 · Ch 24 도미노 줄 · **Ch 25 대나무 홈통과 물방울** · Ch 26 항구 예인선과 바지선 · Ch 27 온실과 모종판 · Ch 28 우주 정거장 도킹 포트 · Ch 29 오르골 종이띠. → 「창구」·「주문」·「택배」·「물 흐름」·「문 검사」는 피함(지금 원고 비유 01 주문표·02 공구 대여 창구·03 택배 창구·05 택배 운송장·07 건물 출입구가 모두 겹침).

1. **기송관(공기 튜브) 캡슐 우편** — 은행·병원 건물의 관: 정해진 크기 캡슐만 들어감(01 입력 형식), 역마다 캡슐을 받는 통(02 의존성), 캡슐 하나가 한 번에 돌아옴(03), 번호 붙은 캡슐이 차례로 도착(04·05), 끊기면 번호부터 다시(06), 관 입구 덮개·열쇠(07), 관 배치도(08). 장: 요청·응답 왕복이 한눈에, 과정에 없던 사물 / 단: 학생에게 낯선 사물일 수 있음.
2. **화물 열차와 번호판 달린 차량** — 차량 규격 틀(01), 역에서 바꿔 다는 기관차(02), 한 번에 오는 화물(03), 한 칸씩 들어오는 열차(04), 칸마다 번호판·마지막 칸(05 `done`), 끊긴 뒤 번호부터(06), 역 개찰구·출입 허가·출발 시각(07), 편성도(08). 장: 흘려 보내기·번호·끝 칸이 자연스러움 / 단: Ch 26 항구(운송) 계열과 영역이 가까움.
3. **공장 컨베이어와 규격 틀·번호 스티커 상자** — 틀에 안 맞는 상자는 벨트에 못 오름(01), 벨트 위 상자가 하나씩(04·05), 번호 스티커로 다시 이어 받기(06), 벨트 입구 잠금(07). 장: 사물이 평범 / 단: Ch 29 종이띠(띠 모양)와 닮을 수 있음.
4. **등대·신호 깃발(한 방향으로 계속 보내는 신호)** — SSE 한 방향 흐름·신호 번호·끝 신호. 장: SSE 성격(서버 → 클라이언트)이 뚜렷 / 단: 요청·인증 장면을 담기 어려움(05·06만 맞음).

## 12. 위험과 깨진 것

1. **`run_section.sh`로 지금 노트북을 돌리면 준비 셀에서 멈춤**(루트 커널에서 `agent_service`를 못 찾음 — §4). 앱 파일 자리·준비 셀 결정이 01절 전에 필요.
2. **paired 넷의 Before가 결함 장면이 아님**(01·07 = 검사가 제대로 막음, 03 = 일부러 던진 예외·After가 안 고침, 06 = 일부러 던진 예외) — §3. 02만 실제 결함.
3. **규격 §3 위반** — 09 모델 글 `assert`·모델 선택 인자 `assert` · 모델 셀이 앱 파일 안(`reasoning_effort` 없음, G4 사각지대) · 02·07 준비용 가짜 객체 클래스.
4. **출력의 표준 오류 Traceback**(06·07) — 파일 위치·맥 임시 폴더(`/var/folders/14/…`)가 노트북 저장 출력에 남음. 08은 `path.resolve()` 절대 위치를 출력(가려졌지만 인용 금지 대상).
5. **사실과 다른 글** — 03·09 「Ch29 평가셋」 · 04 b2 「첫 응답 지연을 줄이지만」 · 06 b4·08 b8·09 b8 「Ch31에서 이벤트·실행 저장」 · 01 b3 「실행 객체」 · 02 b3 「생성 비용」 · 07 b5 「정확한 Bearer 헤더는 실제 Agent를 호출해 200」(결정적 그래프) · 도식 읽기 틀 색 문장.
6. **서버 프로세스·포트** — uvicorn 자식 프로세스를 쓰면 Ch 28 규칙(빈 포트 `assert` → `poll() is None` → 끝 셀 `terminate()`·`wait()`) · TS 테스트는 포트 8000 고정 · 기기 셸 호출이 끝나면 백그라운드도 끝남(한 셀·한 호출 안에서).
7. **비동기 문법이 한 챕터에 몰림** — `async for`·비동기 생성기·`wait_for`·`timeout`·`async with`(§10-1).
8. **JS·TS 실행 환경** — 학생 Node 판(22.18 미만이면 타입 지우기 없음), 생성 SDK는 `tsx`/`tsc` 필요, SDK 다시 만들기는 Java 11 + jar, README `typescript@latest`는 판이 떠다님(지금 7.x).
9. **앱을 고치면 따라 바뀌는 파일** — `openapi.json`(08이 다시 씀) · `client/generated/` 18개(다시 만들려면 Java) · `tests/test_app.py`(401·CORS·SSE 글 `assert`) · `client/test_stream.ts`(id 글 `web-01:0`) · 공개 목록·zip·`bundle-execution.json`.
10. **파일 쓰기 자리** — 08이 실습 폴더 맨 위 `openapi.json`을 씀(학생 묶음 공개 파일). 지금은 바이트 같지만 앱이 바뀌면 해시가 바뀜.
11. **흔들림** — 09 답 글·사건 수·도구 인자. 06 이어 받기는 다시 실행 방식이라 실제 모델이면 앞뒤 글이 어긋남.
12. **뒤 챕터 계약** — 파일 계약 없음. 글 셋(Ch 31 01·Ch 34 04·Part 7 소개)은 참. **Part 7 묶음 실행 검사가 01을 실행**(키·모델 넣으면 멈춤).
13. **Part 7 옛 검사 스크립트** — `check_figures.py`는 `_gen_figures.py`·excalidraw 짝을 요구(옮기면 Ch 30에서 멈춤) · `check_delivery.py`는 이미 `existing-artifacts-before.json`에서 멈춤 · `check_bundle_execution.py`는 기기에서 그대로 못 돎.
14. **긴 실행 시간** — 결정적 절은 1초 안(저장 기록), 09 셀 3~4초씩. uvicorn 기동 약 1초. 설치 없는 한 셸 180초 제한에 걸릴 일 없음.
15. **기기 디스크** — 루트 여유 **2.0G(작업 전후 같음)** · `/sessions` **831M(전후 같음 — `npm view` 뒤 잠깐 810M로 보였음, `~/.npm/_cacache` 21MB 남음)**. 가상환경 252MB는 사용자 디스크(`$ROOT/.cache/vm`), 기기 `/tmp/ch30-prep` 80KB. uv 캐시 `/tmp/uv-cache`는 `uv venv`·`pip==26.2`만 씀(나머지 `pip --no-cache-dir`).

## 13. 01절 작업자가 먼저 결정해야 할 것

1. **앱 코드를 노트북에서 어떻게 가져올지(§8 A~D)와 준비 셀 모양** — `run_section.sh`(루트 커널)·학생 커널(`notebooks/`)·Part 7 묶음 실행(풀린 폴더 `notebooks/`) 세 자리에서 모두 도는 방법. 학생이 여는 앱 파일(`app.py` 등)의 금지 문법을 고칠지(Ch 28 A-17) — 고치면 `openapi.json`·생성 SDK·테스트·TS 테스트가 함께 움직임.
2. **paired 넷의 Before를 실제 결함으로 바꿀지(§3 표)** — 01(스키마 없는 라우트·결과 상태 노출) · 03(동기 `invoke` `TypeError`·500) · 06(시간 제한 0·이어 받기 번호 누락) · 07(와일드카드 + 자격 증명·`WWW-Authenticate`) · 02는 장면 유지하되 클래스·`lambda` 없이. 완료 챕터 문장(Ch 2 11·12 b8, Ch 25 04 b8, Ch 29 05 b8) 조건 지키기.
3. **모델 결정(§9 M0/M1/M2/M0′)과 09 정리** — 모델 셀을 노트북에 보이게(`temperature=0`·`reasoning_effort="none"`) 할지, 따로 실행 둘을 뺄지, 모델 글 `assert` 제거, `09-probe.md` §0 규칙을 첫 요청 전에.
4. **허용 문법 범위(§10-1·10-2)** — `async for`·비동기 생성기·`wait_for`/`timeout`을 어느 절에서 처음 가르칠지, FastAPI 힌트 챕터 예외 범위(본문·헤더·의존성 힌트, `Annotated` vs 기본값 모양), 반환 힌트 0.
5. **JS·TS와 SDK를 어디까지 실행할지(§10-3)와 말·제목(§10-4)** — 「경로」 대체어(「요청 주소」 후보), 「접근 토큰」·401 말(Ch 28 맞춤), 제목 영어를 「제목에만 남음」으로 둘지. **슬러그 01·04·09는 링크로 고정.**

## 14. 챕터 마감으로 미룰 것

- **10 실습 절 신설**(규격 §7-2): 슬러그 후보 **`10-FastAPI-서빙-실습`**(제목 「FastAPI 서빙 실습: …」 — 선례 `09-Middleware-실습`·`04-Streaming-실습`·`06-MCP-실습`·`05-Agent-평가-실습`은 챕터 짧은 이름 + 「실습」) · 다른 후보 `10-FastAPI-실습`(가장 짧음, `_notebook/build_index.py` 64행 제목 「FastAPI로 Agent 서빙」의 앞말) · `10-Agent-서빙-실습`. `format: experiment`, meta 「실습 30분 · 새 용어 0」(**챕터 시수 10·22h에 더하지 않음**). 새 문법·API 0, 요청 3~5번(모델 결정에 따라 0도 선례 — Ch 23·24). 주제 예: 01~09 기능(입력 형식·인증·SSE·이어 받기·시간 제한)을 한 요청 흐름에 모으고 실행 2는 값 하나만(예: 시간 제한 값·허용 출처 하나·`Last-Event-ID` 하나) 바꿔 사건 목록을 견줌.
- **Part 7에서 다른 점**: `_build_index.py`에 절 수 검사 없음(자동 「30절」) · Part 시수 손 글 「88시간」 그대로(실습 절 시수 안 더함) · `textbook/_notebook/build_index.py` 64행 절 수 9 그대로(과정 약속) · Part 7 `check_bundle_execution.py`는 01을 실행(실습 절을 넣으려면 스크립트 수정 — 금지, 후보로 기록) · `check_figures.py`는 옛 그림 짝·`_gen_figures.py`를 요구(옮기면 멈춤 — 기록).
- 옛 생성기 막기(첫 절 작업 때 `raise SystemExit`) → 마감 때 `qa/upgrade/before/generators/blocked/`로 `mv -n`: `_src/_generate.py`(79c8c6f6…) · `notebooks/_generate.py`(a9640d09… — 공개 목록 밖) · `figures/_gen_figures.py`(dbd4ec67…) · `.moai/…/part7_*.py` 셋은 맨 위 `raise SystemExit`만(Ch 29 A-13 선례 — 옮길지는 사용자·강사).
- 옛 그림 27개(`figures/0N-흐름.{svg,excalidraw,caption.md}`) 삭제 승인 목록(사본 `before/figures/`, 공개 목록에 줄 없음) — Part 7 `check_figures.py`와 함께 판단.
- `chapter.json` `objectives`(「ainvoke와 astream을 호출」·「POST SSE」·「OpenAPI에서 TypeScript SDK를 생성」) · 절 제목 · `textbook/part7/_build_index.py` 20행 ch30 설명 · `_notebook/build_index.py` 64~65행 설명 · 챕터 `index.html`을 개선 본문과 대조 → `_build.py`·`_build_index.py`.
- 실습 폴더 README 다시 쓰기(노트북 열, `uv sync --locked` → `.venv` → `notebooks/`, 절마다 요청 수·키 필요, 서버·Node·Java 준비물, `typescript@latest` 판 고정 여부, 「교육용 토큰」 → 「교재용 접근 토큰」) · `labs/part7/continuity-guide.md` 7·8행 · `qa/research.md`·`verification.md`·`집필점검표.md`에 「개선 전 판」 표시 · 실습 폴더 `.venv`(맥 171MB)·`__pycache__`·`.pytest_cache`는 삭제 승인 대상.
- 공개 목록 두 곳(10 노트북·도구 파일·바뀐 앱 파일) → `part7-practice.zip` 다시 만들기(마지막에 한 번) → 묶음을 풀어 01·10 준비 셀 확인 → Part 7 `check_bundle_execution.py`는 기기에서 사본으로(실행기 문제) · `check_delivery.py`(`existing-artifacts-before.json`에서 멈춤 예상) 기록.
- **뒤 챕터 인계**(고치지 않음): Ch 31 01 b2·b3·Ch 34 04 b3(참인지) · `labs/part7/continuity-guide.md` · 과정 요약에 Ch 30 줄(비동기 허용 범위·FastAPI 힌트 예외·자식 프로세스·용어).
- 삭제 승인 대상: `.cache/vm/venv-ch30-fastapi-serving`(252MB) · 기기 `/tmp/ch30-prep`(80KB) · `~/.npm/_cacache`(21MB, `npm view`가 남김) · `qa/upgrade/gates-wip-*.json`(생기면).

## 15. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 9 · `html` 9(빌드한 절 HTML) · `notebooks` 9 · `figures` 28(SVG·excalidraw·caption 각 9 + `_gen_figures.py`) · `generators` 7(`_src_generate.py`·`notebooks_generate.py`·`_gen_figures.py` + `moai/` part7 스크립트 셋·`part7-author.md`) · `qa` 3(`public-files.json`·`research.md`·`verification.md`) · `lab` 34(README·`pyproject.toml`·`uv.lock`·`openapi.json`·`openapitools.json`·`agent_service` 다섯·`tests/test_app.py`·`client` TS 둘·`client/generated` 21) · `chapter.json`·`_build.py`·`index.html`·`집필점검표.md` = **103개, 1,090,200바이트**. 원본과 바이트 대조 모두 같음 |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 292, 통과 0/9, 문장 764), `8951dc50a13d2d47b059b816f6047c0ca3b0f0b7c89aef3db1321de70620d3d0` |
| `qa/upgrade/before-manifest.json` | sha256 **255개**(`9e7bbb4d43e2380fd0cbd3cf4546a4b8ef526e9830ae75aaa5c384a2dba5eb27`) — ① 이 챕터 원고·실습 폴더(`qa/upgrade` 뺀 챕터 파일 전부·실습 폴더 파일 전부(`.venv`·pyc·`.pytest_cache` 뺌)·`.venv/pyvenv.cfg`·생성 SDK 기록 파일·노트북 계약 JSON·화면 검사 결과) ② 이어 쓸 만한 앞 챕터 도구·서버 파일(Ch 19 `order_tools.py`·Ch 21 `runner_tools.py`·Ch 25 `stream_tools.py`·Ch 28 `connect_tools.py`·`auth_server.py`·Ch 29 `eval_tools.py` + 잠금 몇) ③ 챕터 요약 전부 ④ Part 7 목록 둘·목차·소개·`practice-start.md`·`qa/` 전부(스크립트·JSON·기록·`language/`·`before-integration/`)·continuity-guide 둘·`build_index.py`·`build_bundle.py`·`textbook/index.html`·zip 셋(part7·part6·llm) ⑤ 뒤 챕터가 Ch 30을 가리키는 파일(Ch 31 01·Ch 34 04 `_src`·HTML, Ch 32 README·`app.py`, Ch 33 CI·기준선, Ch 31~34 `chapter.json`) ⑥ Ch 30을 가리키는 완료 챕터 파일(Ch 1 01·Ch 2 11·12·목차·Ch 24 `author_01.py`·01 `_src`·Ch 23 03·06·Ch 25 02·04·`author_02/04.py`·Ch 28 03·Ch 29 05·`author_04/05.py`) ⑦ 옛 생성기(`textbook/part5/_figure.py`·`.moai` part7 스크립트 셋·`part7-author.md`·`review-part7.md`) ⑧ 과정 문서·공용 도구(규격·PLAYBOOK·AGENT-BRIEF·누적 문서 셋·게이트·`verify.py`·`execute.py`·빌더·렌더·첨부·`nbkit`·`run_section.sh`·`mdpatch`·`patch`·`pack`·`count_code`·`check_course_continuity.py`·`theme.css`·`AGENTS.md`·`CLAUDE.md`) |
| `qa/upgrade/chapter-lead-notes.md` | 이 파일 |
| `$ROOT/.cache/vm/venv-ch30-fastapi-serving` | Python 3.12.13 · 252MB |

### 가상환경 만든 방법과 결과
- Ch 29 준비와 같은 방법: `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy uv venv --python 3.12.13 …/venv-ch30-fastapi-serving` → `uv pip install --python …/bin/python pip==26.2` → 잠금 목록 `uv export --project labs/part7/ch30-fastapi-serving --frozen --no-hashes --all-groups --no-emit-project`(실습 폴더 파일 그대로), 주석·들여 쓴 줄을 뺀 112줄(`/tmp/ch30-prep/req-clean.txt`, 환경 표시 유지) → **`bin/python -m pip install --no-cache-dir -q -r`**(한 호출, 170초 안). 설치 오류 0, **`uv cache prune` 안 함**.
- 크기 어림(만들기 전): Ch 29 265MB·Ch 28 302MB 사이일 것, 사용자 디스크(여유 67G)라 기기 루트(2.0G)·`/sessions`(831M)는 그대로일 것 → 만듦. **전후 루트 2.0G · `/sessions` 831M.**
- 결과: `pip freeze --all`과 잠금 대조 **판 차이 0**(설치 107 = 잠금 112 − 이 기기에 해당하지 않는 다섯: `appnope`(darwin)·`colorama`(win32)·`cffi`·`pycparser`(pypy)·`httpx2-jsfetch`(emscripten)). `pip check` 이상 없음. 커널 스펙 `share/jupyter/kernels/python3` 있음. `run_section.sh`는 `$ROOT/.cache/vm/venv-<챕터 폴더 이름>`을 자동으로 씀(`UV_NO_SYNC=1`).
- import 확인(`env -u OPENAI_API_KEY`): `fastapi`·`fastapi.sse`(`EventSourceResponse`·`ServerSentEvent`·`format_sse_event`·`KEEPALIVE_COMMENT`)·`fastapi.testclient`·`fastapi.security.HTTPBearer`·`fastapi.middleware.cors` · `httpx`(`ASGITransport`) · `uvicorn` · `langgraph`(`StateGraph`·`get_stream_writer`) · `agent_service.app`·`agent`·`live_agent`(모델 객체는 만들지 않음) 모두 됨. 실습 테스트 6 passed.

### 참고 자료 (2026-09-29 확인)
- FastAPI Server-Sent Events `https://fastapi.tiangolo.com/tutorial/server-sent-events/` — 「Added in FastAPI 0.135.0」 · 「SSE works with any HTTP method, not just GET」 · 쉼 신호 15초 · `Cache-Control: no-cache` · `X-Accel-Buffering: no` · `Last-Event-ID` 헤더로 이어 보내는 예(목록을 건너뛰는 모양 — 실습 앱과 같은 방식).
- FastAPI CORS `https://fastapi.tiangolo.com/tutorial/cors/` — 「None of allow_origins, allow_methods and allow_headers can be set to ['*'] if allow_credentials is set to True」 · 사전 요청은 200 또는 400 · 기본값(`allow_methods` GET·`max_age` 600).
- FastAPI Testing Events `https://fastapi.tiangolo.com/advanced/testing-events/` — `lifespan`은 `with TestClient(app)`일 때만.
- HTTPX Transports `https://www.python-httpx.org/advanced/transports/` — `ASGITransport` 사용법, 「It is not in the scope of HTTPX to trigger ASGI lifespan events」, 스트림 지원은 문서에 없음(기기에서 끝까지 모아 줌을 확인).
- MDN `EventSource()` `https://developer.mozilla.org/en-US/docs/Web/API/EventSource/EventSource` — 인자는 `url`과 `withCredentials`뿐(메서드·본문·헤더 못 정함).
- LangGraph Streaming `https://docs.langchain.com/oss/python/langgraph/streaming` — `astream`·모드·`version="v2"`(`type`·`ns`·`data`) · 「In async code running on Python < 3.11, get_stream_writer will not work」.
- OpenAPI Generator 설치 `https://openapi-generator.tech/docs/installation/` — 「Java 11 runtime at a minimum」, npm 판은 jar를 감싼 것.
- 설치판 소스: `fastapi/sse.py` 1~222 · `fastapi/routing.py` 531~574(SSE 쉼 신호·머리) · `fastapi/security/http.py`(`WWW-Authenticate`·401) · `agent_service/app.py` 29~154 · `agent.py` 16~46 · `live_agent.py` 15~27 · langgraph `Pregel.astream`·`ainvoke` 인자.
- 모델 없는 확인 파일(기기 `/tmp/ch30-prep/exp/`): `e1_versions.py`(판) · `e2_app.py`(실습 앱 전체 동작) · `e3_stream_read.py`(스트림 도착 시각 셋 — uvicorn 자식 프로세스 포함) · `e4_langgraph.py`(`astream`·동기 `invoke` 오류) · `e5_security.py`(`HTTPBearer`·와일드카드 CORS) · `e6_repeat.py`(시간 제한 0 5회·재정의 누수) · `e7_minimal.py`(힌트 없는 SSE·`jsonl`·헤더 이름) · `run_ts.sh`(uvicorn 8000 + `node client/test_stream.ts`). AST·금지어 세기 `ast_scan.py`·`ban.py`, 사본 `snapshot.py`, 매니페스트 `manifest.py`.
