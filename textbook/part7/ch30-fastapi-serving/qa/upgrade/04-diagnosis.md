# 04절 진단 — astream과 응답 스트림 (experiment)

- 작업일: 2026-09-29 · 작업자: 04절 작업자 · 생성기 `qa/upgrade/author_04.py`(`45d6eb6d…` — 마지막 치환 뒤)
- 읽은 것: `handoff.md`(머리·챕터 공통·§03 → §04 전부, §01 → §02·§02 → §03 훑음) · 준비 노트 `chapter-lead-notes.md`(§0·§1·§2 04·05·§7-1·§7-2·§11) · `03-diagnosis.md` · `author_03.py`(전부)·`author_01.py`(`FIND_LAB` 대조) · Ch 25 `author_01.py`(진행 값·`collect_events`·`positions_of`)·`author_03.py`(시간 처리·experiment 틀) · Ch 25 `stream_tools.py` · Ch 27 `author_02.py`(도구 파일 첫 판 사슬) · Ch 28 03·Ch 29 02 노트북(도구 파일 고정 문장) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 규격 전부 · 과정 요약(Ch 25 줄·§5 용어·§6·§7 표 — §2-7 9번 끝 적용 선례) · Ch 25 04 `_src`(b8) · Ch 6 04 `_src`(제너레이터) · Ch 2 12 `_src`(용어 표). `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 후(`gates-wip-04.json`) |
|---|---|---|
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 1 · 1 · 4 · 0 · 6 · 11 · 3 = **26** | **0 · 0 · 0 · 0 · 0 · 0 · 0** |
| 코드 셀 · 코드 줄(주석·빈 줄·`%` 줄 뺌, `extra_check.py`) | 4 · 29 | **23 · 110** |
| 검사 문장 | 81 | **365** |

- 첫 실행 전 `upgrade_gates.py … --label wip-04 --section 04`: G1·G2 **0**(G6 5 — 70자 넘는 문장 둘·코드로 시작하는 문장 셋, G7 3 — 그림 전) → 고친 뒤 G6 0. 그림을 넣은 뒤 b10 한 문장이 70자를 넘어 한 번 더 고침.
- AST 따로(`/tmp/ch30-04/tools/extra_check.py` — 03 도구에 `async for`·`async with`·`yield` 세기를 더함): 걸린 것은 **챕터 허용 범위뿐** — 셀 맨 위 `async for` 셋(셀 [8]·[10]·[11] — 노트북 도구 기능, 이 절이 첫 풀이) · 셀 맨 위 await 셋(셀 [12] `await agent.ainvoke`·[16]·[17] `await collect_events_async`) · `async def` 하나(셀 [15] `collect_events_async` — 안에 `async for`). f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`while`·`try`·별표 풀기·대입 풀기(for 포함 — 짝은 `event[0]`·`event[1]`)·`+=`·기본값 매개변수·힌트·클래스·데코레이터·`yield`·`join`·가짜 에이전트·`asyncio`·딕셔너리 `.get` **0**. 호출 깊이 최대 **2** · 준비 셀 밖 셀 최대 **8줄** · 함수 본문 최대 **4줄** · 셀당 정의 하나. 도구 파일 `serve_tools.py`: 금지 문법 0·호출 깊이 2·가져오기 0.
- 금지어(`/tmp/ch30-04/tools/ban30.py` — 03 도구 그대로, `_src`·노트북 마크다운·코드 주석·`.mmd`·캡션·alt): 걸린 것은 **허용한 것과 거짓 양성뿐** — 「노드」(Ch 13 말 — 03과 같이 씀, 강사 확인) · 「스트림」(「스트림 사건」·「스트림 모드」 — Ch 25 말, 제목의 「응답 스트림」 한 번) · 「이벤트」(「이벤트 루프」) · 「로그」(「프로그램」) · 「트리」(「스트리밍」). 「조각」·「지연」·「측정」·「반환」·「결정적」·「청크」·사용자가 금지한 표현·「쉽게·간단히·당연히」·「토큰」 단독(칸 `token`은 코드)·「Agent」(본문) **0**.

## 수정 전 주요 문제 (옛 판 — `before/notebooks/04-…ipynb`·`before/_src/04-*.html`)

1. 준비 셀이 루트 커널에서 멈춤(`next((p for p in (start, *start.parents) …), None)` + `os.chdir`) — 01~03과 같은 문제. 셀 맨 위 `async for`를 풀이 없이 씀(과정 첫 등장). `counts = {}`·`count += 1`·`async for _ in`·`''.join(chunks).strip()`·`assert len(chunks) >= 4`.
2. **b2 「스트리밍은 중간 결과를 먼저 전달해 첫 응답 지연을 줄이지만」** — Ch 25를 근거로 쓸 수 없음(Ch 25는 스트리밍하지 않은 실행과 견주지 않음), 「지연」 금지어, 이 절에서 재지 않음.
3. 실험 「질문 셋 조각 수 3·4·5」는 노드 코드의 공백 나누기 규칙이 정한 셈 — 실험이라기보다 규칙 확인, 값 여러 개를 바꿈(질문 셋).
4. 말: 본문 「조각」 22번(Ch 5 토큰 전용 말) · b3 「Ch25에서 스트림 모드와 진행 이벤트를 비교」(Ch 25 말은 「스트림 사건」·「진행 값」) · 「소비」·「반환」·「측정」·「청크」 한정어 없이 · b4 「첫 조각까지의 시간 … 따로 측정해야」(재지 않은 시간 설명) · 도식 읽기 틀 색 문장(「보라색 상자는 Agent 실행」 — 모델 없는 절에 보라).
5. 첫 줄 주석·결과 읽기 0 · 제목 셀·그림 첨부 없음 · 참고 자료 둘(확인 2026-09-11, 설명 없음) · 복습 해설 한 줄.

## 바꾼 것

- **Ch 25 04 b8 조건(handoff §03 → §04 1)**: 모드 `custom` + 비동기 메서드 `astream` + 이어 붙이기. 3절 `astream`을 **부르기만 → `async_generator`**(Ch 6 04 `generator`의 비동기 판 — 「비동기 제너레이터」) → 셀 맨 위 **`async for`**(첫 풀이 — 뜻 → 역에 칸이 들어올 때마다 짐을 내리는 예 → 코드, Python 언어 참조 8.9.2) → 사건 여섯 `{'token': '질문을 '}` … `{'token': '주세요 '}` → 첫 사건 `dict`·키 `['token']` → 같은 객체 다시 `async for` → `다시 꺼낸 사건 수: 0`. 4절 `astream`을 새로 불러 **받을 때마다 이어 붙임**(`지금까지 이어 붙인 글:` 여섯 줄) → `끝 글자가 공백인가: True`·`그대로 견주면 같은가: False`·`앞뒤 공백을 지우고 견주면 같은가: True`(03 `ainvoke` 답) → `답의 낱말 수: 6`=`받은 사건 수: 6`. 2절은 `inspect.getsource(answer_node)`로 노드의 쓰기 줄(`writer({"token": piece + " "})`)을 읽음.
- **실험(experiment, 값 하나만)**: 인자 `stream_mode`만 `"custom"` → `["custom", "updates"]`. 가설은 Ch 25 01의 차례(진행 값이 갱신보다 먼저)에서. 실행 1 `사건 수: 6`(모두 `dict`, 이어 붙인 글이 4절과 같음 `True`) ↔ 실행 2 `사건 수: 7`·`tuple 2`·일곱 줄 차례·`모드 차례: ['custom', 'updates']`·`custom 나온 자리: [1, 2, 3, 4, 5, 6]`·`updates 나온 자리: [7]`·진행 값만 이어 붙인 글이 실행 1과 같음 `True`·`updates` 자료 `{'answer': {'answer': …}}`가 `ainvoke` 답과 같음 `True` · 결과 표 셀. **결론은 개수·자리·차례만**(매번 같은 값). 옛 「질문 셋 조각 수」는 쓰지 않고, 그 규칙은 4절 「사건 수 = 답의 낱말 수」 한 셀과 b7 「다른 질문을 넣어 보지 않았습니다」로.
- **b2 「첫 응답 지연을 줄이지만」 → 차례로(결정 4)**: 「노드가 끝났다는 사건보다 진행 값이 먼저 오면, 받는 쪽은 끝 사건을 받기 전부터 앞 낱말을 붙일 수 있습니다. 이 절은 걸린 시간을 재지 않고, 사건이 온 차례만 봅니다」 · b6 「스트리밍하지 않은 `ainvoke`와 시간을 견주지도 않았습니다. 스트리밍이 몇 초를 줄이는지는 이 절 결과로 말할 수 없습니다」(Ch 25 03 선례). 노드 실행 중에 사건을 꺼내 내놓는 동작은 설치판 소스(`pregel/main.py` 3283~3297·3395~3399·3440~3457)로만 적고 「노트북에서는 사건이 온 차례만 확인」.
- **초 값 처리**: 걸린 시간을 **재지 않음** — 규격 §3 「걸린 시간 주제 절 예외」를 쓰지 않았습니다(이 절의 학습 질문은 받는 방법과 차례이고, 차례는 시각 없이 사건 자리로 보임). 저장 출력·본문·그림에 초 값 0. 준비 노트 §7-2의 0.31·0.61·0.92초(`e4_langgraph.py`)는 교재에 쓰지 않음.
- **말(handoff §03 → §04 5)**: 옛 「조각」 → **「스트림 사건」**(메서드가 하나씩 내놓는 값) · **「진행 값」**(노드가 쓰기 함수로 적은 `{'token': …}`) · **「갱신」**(모드 `updates`의 자료 — Ch 25 01 「노드의 갱신」) · 「스트림 청크」는 쓰지 않음(Ch 25 02 모드 `messages` 말 — 09 몫). 새 용어 **2**: 「비동기 제너레이터(async generator)」·「비동기 반복(async for)」(meta 「새 용어 2」). 「진행 이벤트」 0.
- **도구 파일 `serve_tools.py` 첫 판**(아래) — 실험 결과 셀에서 Ch 25 함수 둘을 실제로 씀.
- 노트북: 제목 셀(할 일 셋·준비물·기준 버전·강의와 실습 범위) · 오늘 볼 그림(04-1 첨부) · 설명 → 코드 → 결과 읽기 · 실험(가설·실행 1·실행 2·결과 표·결론) · 6절 앱 파일에서 `astream`을 부르는 줄(110·111·134·136행 — 05·09 예고) · 정리 세 줄 + 05 예고. 설치 셀은 03과 같은 여섯(잠금 판). 키 셀 없음. 파일 위치 셀은 01절 셀 글 그대로(생성기 `__main__`에서 `author_01.py`와 문자열 대조 `assert`).
- 본문 b1~b10 새로(b3 = 03절 / Ch 25 01·02·03(링크) / Ch 6 04 제너레이터 / Ch 2 12 · b10 = LangGraph Streaming·Python async for 문·Python asyncio.sleep(셋 다 2026-09-29 WebFetch) + 설치판 소스 행 + 실습 파일 행). 복습 넷 → **다섯**(해설 포함). meta 「강의 1.25h | 실습 2.5h」 그대로(챕터 시수 합 유지).
- 그림: Mermaid **4장**(04-1·04-2 b4 · 04-3 b5 · 04-4 b6 — viewBox 폭 261·208·470·565, 모두 868 이하) + 삽화 **1장**(04-5, 재생성 1회). 옛 `{{svg:04-흐름}}` 토큰 제거, 옛 그림 파일 셋(`04-흐름.svg·.excalidraw·.caption.md`)은 그대로.

## 설치판 동작 확인 (모델 없이 — `/tmp/ch30-04/exp/`)

- `p1_astream.py`(5번, md5 `86524da6…` 5/5, 표준 오류 0): `astream` 객체 `async_generator`·`inspect.isasyncgen` `True` · `custom` 사건 여섯·이어 붙인 글 끝 공백 하나·`strip()` 같음 · `["custom","updates"]` 일곱(custom 여섯 → updates 하나) · 끝까지 꺼낸 객체 다시 0 · 목록 차례를 `["updates","custom"]`로 뒤집어도 사건 차례 같음(교재에 안 씀) · 기본 모드 `updates`.
- `p2_ipy.py`: 설치판 IPython 9.17.1 `InteractiveShell.run_cell`로 **셀 맨 위 `async for`가 됨**(과제 확인 사항) · 셀 안 `async def` + `await` 됨.
- `p3_scene.py`(노트북 장면 전체, 셀 맨 위 자리는 `asyncio.run` 안 비동기 함수, 5번): 출력 md5 **5/5 같음**(`1a5a0d72…`), 표준 오류 0. 실습 폴더에 새 파일 0.
- 설치판 소스(langgraph 1.2.11): `pregel/main.py` 3063 `astream`(인자 `version` 기본값 `"v1"`) · 3156 `AsyncQueue` · 3283~3297 모드 `custom`이면 쓰기 함수가 대기열에 넣음 · 3300~3303 고르지 않으면 아무것도 하지 않는 쓰기 함수 · 3395~3399 `custom`이면 노드 실행 중에 기다리는 작업 · 3440~3457 그 사이 쌓인 사건을 꺼내 `yield` · `config.py` 126 `get_stream_writer`(그래프 밖에서 부르면 `RuntimeError: Called get_config outside of a runnable context` — 기기에서 확인).
- 공식 문서(2026-09-29 WebFetch): LangGraph Streaming — 「stream (sync) and astream (async) methods to yield streamed outputs as iterators」·모드 표 `custom` 「Custom data emitted from nodes via get_stream_writer」·`updates` 「State updates after each step」·첫머리는 새 앱에 LangGraph v1.2 event streaming을 권함(b7에 밝힘) · Python 3.12 언어 참조 8.9.2 The async for statement(`await type(iter).__anext__(iter)`와 같음·비동기 함수 밖이면 `SyntaxError`) · asyncio.sleep 「Setting the delay to 0 provides an optimized path to allow other tasks to run」. 「스트리밍이 응답을 빠르게 한다」는 문장은 문서에 없음(b2를 문서 설명으로 한정하지 않고 차례로 바꾼 까닭).

## 실행 (새 커널)

| 실행 | 자리 | 키 | 결과 |
|---|---|---|---|
| 시험 tryA(`/tmp/ch30-04/tryA` 사본, `execute.py` 기본 `--cwd` = 프로젝트 맨 위, `PYTHONPATH` = `notebooks/`) | 루트 커널 | `OPENAI_API_KEY` 지움 | PASS 23셀 |
| 시험 tryB(사본, `--cwd` 실습 폴더 `notebooks/`, `PYTHONPATH` 지움) | 학생 커널 | 지움 | PASS 23셀, 셀별 23/23 같음 |
| **A**(`run_section.sh … 04`, 시작 08:16:49Z · `executed_at` 2026-09-29T08:16:51Z) | 루트 커널 | 지움 | PASS 23셀(그림 첨부 단계에서 멈춤 — 04-1 PNG 전) |
| **B**(A 사본, `uv run … execute.py --cwd notebooks/`, `PYTHONPATH` 지움, 08:17:02Z) | 학생 커널 | 지움 | PASS 23셀 |

- **A ↔ B 셀별 출력 23/23 같음**(이은 글 해시 `f465eebca5201348` 같음), `code_sha256` `2b5a740d6f1d276610033c8e0318692a7d3a475a04fb384742fd92be5c929eb7` 같음, **`outputs_sha256`도 같음** `e7a37a53a5462c2c69c5495d36970df07393a9722960a346af32c1a2f6384f72`(이번에는 설치 셀 스트림이 두 커널에서 같은 자리로 나뉨 — 02·03과 다름). 초 값을 출력하는 셀 없음 · 요청 0이라 셀 [2]~[23] 출력은 모두 같음.
- 그 뒤 `--no-exec` 넷(렌더·첨부·빌드)에서 노트북 코드·출력·`executed_at` 그대로(첨부만 더함 — A 사본과 `cmpout` 23/23·`outputs_sha256` 같음) — 노트북 파일 **`14427e45a20121dade41f6af92aa69f2bb9a1db99a09a7f53ab7ff83a21e7b16`**.
- 모든 실행 `PYTHONDONTWRITEBYTECODE=1` · 실습 폴더에 새로 생긴 파일은 노트북 04와 `notebooks/serve_tools.py`뿐(`find -newer` — `agent_service/__pycache__` 그대로, 도구 파일 pyc 0) · `.failure.json` 0 · 표준 오류 출력 0(커널 TCP 경고는 실행기 쪽) · 설치 셀 출력에 pip 안내 한 줄.
- **모델 요청 0** · 서버 프로그램·포트·자식 프로세스 0 · 남은 프로세스 0(`ps` — ipykernel·uvicorn·jupyter 없음).

## 앱 파일 고침 · `app.openapi()` 대조 · `tests/`

- **04는 앱 파일을 고치지 않음.** 6절은 `app.py`를 글로 읽어 줄 넷(110·111·134·136)을 출력만 함 — 134행 `async for message, metadata in …`(대입 풀기)는 09 처리 함수의 줄이라 결과 읽기에서 「09절에서 씀」으로만 가리킴. 앱 파일을 바꾸면 02(`Depends(` 줄·`chat` 정의 줄)·03(`chat` 소스)·04(줄 번호 110·111·134·136) 출력이 함께 바뀜.
- 확인: `json.dumps(app.openapi(), ensure_ascii=False, indent=2)` sha256 **`06e5d1b9553a1fde91aafc44b02e0836a8a241386e42077dc15825a75be5e658`** = `openapi.json` 바이트 같음 · `pytest -q -p no:cacheprovider` **6 passed, 1 warning** · 앱 파일 해시 `app.py` `3455d405…`·`agent.py` `a6c42e63…`·`live_agent.py` `586a6a69…`·`schemas.py` `ed77b197…`·`__init__.py` `1c7d7aef…`·`tests/test_app.py` `f8611741…` 그대로. `openapi.json`·생성 SDK 손대지 않음.

## 도구 파일 — `notebooks/serve_tools.py` 첫 판

- **만듦** — 이 절 5절 결과 셀(셀 [19]·[22])이 Ch 25에서 배운 평범한 함수 둘을 실제로 씀. 이름은 챕터 공통 9의 예약 이름(Ch 25 `stream_tools`와 겹치지 않음).
- 함수 둘: `positions_of(events, mode)`(Ch 25 01) · `mode_order(events)`(Ch 25 02) — **Ch 25 `stream_tools.py` 마감 판 `3a734aeb87244a7d05574acd9f1d269a7ab2ddd1a944d018e60baa82c4708ff5`**에서 설명 주석과 본문을 글자 그대로 옮김(주석 첫 줄만 「# Ch 25 01절에서 배웠습니다 — Ch 25 도구 파일 stream_tools.py의 같은 이름 함수를 옮겼습니다」). 가져오기 0 · 금지 문법 0.
- 파일 해시 **`e0a3a382260364dcd233abdc6e9e583600aca110da1aee056b6e2d5d08d7e0bb`**(41줄).
- **생성기 대조 사슬(첫 판부터 — Ch 27 `author_02.py` 본)**: `TOOLS_HEAD`·`TOOLS`(원본 sha256 `assert` 뒤 `file_block`으로 조립) · `check_tools()`(함수 차례·글자·AST 대조, 가져오기 0) · `strip_later_imports()` · 쓰기 가드(없거나 이 판과 같을 때만 씀 — 뒤 절이 함수를 더한 판은 건너뜀) · `--tools-copy DIR`. 05·06이 함수를 더하면 그 절 생성기가 이 판으로 시작하는지 대조.
- 노트북 가져오기: 준비 셀(가져오기 셀, `os.chdir` 전) `from serve_tools import mode_order, positions_of` · 결과 읽기에 고정 세 문장(「앞에서 배운 함수는 `serve_tools.py`에 모아 두었습니다」·「파일을 열면 코드를 볼 수 있습니다」·「노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다」) + 커널 폴더 문장 둘(Ch 28 03·Ch 29 02와 같은 글).
- **묶음 목록 두 곳에 줄 더함**: 챕터 `qa/public-files.json`(09 노트북 줄 뒤, `ce9b4d52…` → `15f7dca1…`) · `textbook/part7/public-files.json`(정렬 자리 35, `c823d407…` → `2758fc9a…`, 107 → 108줄 — `collect_public_files.py`가 셀 목록과 같음을 쓰지 않고 셈해 확인). 도구 파일은 표준 라이브러리만 써서 설치 셀에 더할 패키지 없음. `part7-practice.zip`·`check_delivery.py`(결과 파일을 씀 — 돌리지 않음)는 마감 몫.
- 이 절이 처음 가르친 `join_tokens`·`collect_events_async`는 노트북에 둠(05·06이 다시 쓰면 그 절이 도구 파일로 옮김).

## 고친 틀린 사실

- b2 「스트리밍은 중간 결과를 먼저 전달해 첫 응답 지연을 줄이지만」 → 차례(노드 끝 사건보다 진행 값이 먼저)와 「걸린 시간은 재지 않았고, 스트리밍하지 않은 실행과 견주지 않았다」로(Ch 25 근거 불가·「지연」 금지어·문서에도 없음).
- b3 「Ch25에서 스트림 모드와 진행 이벤트를 비교」 → Ch 25 01·02·03이 실제로 가르친 것(`stream_mode`·`get_stream_writer` 진행 값·모드 목록이면 짝·진행 값이 갱신보다 먼저·함수 둘·03의 초는 결론에 안 씀).
- b4 「청크 하나가 … 제공자, 네트워크 버퍼 … 여러 토큰이 묶일 수 있습니다」·「첫 조각까지의 시간, 조각 사이 간격, 완료 시간, 취소 반영 시간」(실행 안 한 설명) → 뺌. 「진행 값은 모델이 글을 쓰는 빠르기가 아니라 노드 코드의 나누기 규칙을 따른다」(b7)와 설치판 소스로 본 동작만.
- b4 「비동기 생성기는 취소 요청을 처리할 기회를 가져야 … 연결이 끊겨도 작업이 계속될 수 있습니다」(실행 안 함) → 뺌(연결이 끊긴 장면은 06 몫).
- 옛 결론 「긴 질문에서 조각 수가 많았지만」(질문 셋) → 「사건 수 여섯은 이 질문의 값, 다른 질문은 넣지 않았다」.
- 도식 읽기 틀 색 문장(보라 = Agent 실행) → 그림마다 색·방향을 그림에 맞춰 새로, 보라 0·빨강 0.

## 그림

- Mermaid 넷: 설계표 `04-figures.md`(렌더 전 작성) → `.mmd`·캡션 → 렌더 → PNG 넷을 직접 열어 확인 → **04-4의 두 칸 사이 `~~~`가 칸을 위아래로 어긋나게 해(폭 438·높이 1008) 빼고 다시 렌더**(폭 565·높이 677, 03-4처럼 공통 상자에서 두 칸으로 화살표만) → 다시 열어 확인(색·방향·칸이 나란함·빨강 0·보라 0). 긴 라벨은 처음부터 `<br>`로 나눠 끊긴 라벨 0. 라벨 숫자는 자리 1·6·7뿐(셀 [19] 출력).
- 삽화 04-5: `04-5-…prompt.md` 상태 줄 — **1차 job `3daa081f-1b59-4d77-80ba-70283944f3f8` 채택**(재생성 1회 — 2차 `175fe2d5-8e8f-43bd-8814-b5f18e40d88a`는 비스듬한 구도로 화면은 찼지만 평판 짐칸 넷·통 다섯으로 「빈 짐칸 둘 = 내린 통 둘」·「짐칸 여섯 = 사건 여섯」 관계가 깨져 탈락) · 거래 2026-09-29T08:19:42.776119Z·08:20:53.295871Z 「Nano Banana Pro −2」 두 줄(**이 절 몫 4크레딧**, 잔액 2287 → 2283, 앞 거래 07:45:24Z는 Ch 30 03) · 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만) · 저장 PNG `a2673d3b…`(1100 × 614)와 채택 결과를 다시 받아 줄인 그림 픽셀 대조 bbox `None`·최대 차이 0 · 저장본 사본을 열어 끝 칸 하나·통을 실은 평판 짐칸 넷·빈 평판 짐칸 둘·기관차 하나·짐 내리는 자리의 통 둘(통 모두 여섯)을 세고 그림 읽기를 씀. **흰 바탕이 위 약 38%·아래 약 31%**(03보다 넓음 — 강사 확인). 01~03 소품 되풀이 없음, 번호판 없음.

## 검사

- `run_section.sh … 04 --no-exec`: 렌더 넷 · 첨부 1 · `_build.py` · **`verify.py --chapter` `PASS 9 sections / 117 code cells (max 14 lines)`** · 게이트 **G1~G7 0 PASS**.
- 빌드 HTML `04-astream과-응답-스트림.html`(`cb929ec3…`): `{{` **0** · `[[` 0 · 인라인 SVG 4 · 삽화 JPEG 1 · 노트북 셀 23.
- `pack.py … 04` → `qa/upgrade/review-pack/04-astream과-응답-스트림.md`.
- 보호 파일 255개: `manifest-changes.md` 「04절 뒤」에 덧붙임.

## 완료 챕터 문장 참·거짓 (이 절 쪽 조건 — 고치지 않음)

| 문장 | 판정 |
|---|---|
| **Ch 25 04 b8** 「Ch 30 04절은 모드 custom의 사건을 비동기 메서드 astream으로 받아 이어 붙입니다」(`_src`·HTML) | **참** — 노트북 3절 `agent.astream(question_input, stream_mode="custom")` + `async for`, 4절 받을 때마다 이어 붙임, 5절 `join_tokens` · 슬러그 그대로 |
| Ch 25 04 b8 「09절은 모드 messages의 스트림 청크를 같은 메서드로 받아 서버 응답으로 보냅니다」 | 09 몫 — 04 6절이 앱 134·136행(`live_chat_stream`의 `stream_mode="messages"`)을 출력만 함(지금 앱 파일로는 참이 될 자리 있음) |
| Ch 25 01~03 「`astream` … 실행하지 않았습니다」 | 참(그 절 범위의 한정 — 04가 처음 실행) |
| Ch 2 12 b8(1절·3절)·Ch 2 11 b8(2절)·Ch 2 `_src/index.html` | 04와 무관(01~03 끝남 — 참) |
| Ch 29 05 b8(01 슬러그) | 04와 무관 — 슬러그 그대로 |
| Ch 31 01 b2·b3(「Ch30에서 FastAPI 요청 함수·경로 함수를 비동기로」)·Ch 32 01·02·Ch 34 04 b3·Part 7 소개 | 글만(참 — 대기 챕터, 고치지 않음. Ch 31 01 b3 「경로 함수」는 Ch 30 말 「처리 함수」와 다름 — 기록만) |

## 챕터 밖 수정

- `textbook/part7/public-files.json`(도구 파일 한 줄 — 위) · `textbook/_notebook/checks/notebook-contracts-part7-ch30-fastapi-serving.json`(`verify.py --chapter`가 다시 씀 — `08bacd36…`) · 사용자 디스크 `.cache/ch30-04-view/`(삽화 보기 사본 셋 — 새로 만든 폴더). 공용 도구·규격·과정 문서·zip·검사 스크립트·앱 파일·Ch 31 이후 파일·Ch 25 도구 파일은 고치지 않음.

## 강사 확인 대상

1. **도구 파일 `serve_tools.py`를 04가 처음 만든 것**(Ch 25 `positions_of`·`mode_order` 둘) — 노트북 1절 파일 위치 셀은 실습 폴더 맨 위(`.`)에서 연 커널도 받지만, 도구 파일 가져오기는 커널이 `notebooks/`에서 시작해야 됨(Ch 28 03과 같은 문장으로 밝힘). 묶음 목록 두 곳에 줄을 더함(zip은 마감).
2. 새 용어 「비동기 제너레이터(async generator)」(Ch 6 04 「제너레이터」 이음)·「비동기 반복(async for)」 · 모드 `updates`의 자료를 「갱신」(Ch 25 01 말)으로 · 「스트림 청크」는 09로 미룬 것(과제 안내 「조각 → 스트림 청크」와 다름 — handoff 용어 표에 적음).
3. 걸린 시간을 재지 않고 차례만으로 b2를 고친 것(규격 §3 주제 절 예외를 쓰지 않음).
4. 실험 변수를 옛 「질문 셋」에서 인자 `stream_mode` 하나로 바꾼 것(규칙 확인은 4절 한 셀로).
5. 「노드」 말(03과 같음).
6. 삽화 04-5(재생성 1회 — 채택본 위아래 흰 바탕이 넓음, 2차는 개수가 어긋나 탈락).
7. 코드 양 29 → 110줄(셀 4 → 23).

## 남은 것 (마감 몫)

- `part7-practice.zip`에 04 노트북 새 판·`serve_tools.py` 반영(마감 때 한 번) · 04는 Part 7 묶음 실행 검사 대상 아님(01만) · `check_delivery.py`는 마감에서.
- 옛 그림 `04-흐름.{svg,excalidraw,caption.md}` 삭제 승인(Part 7 `check_figures.py`와 함께).
- 삭제 승인 대상(지우지 않음): `qa/upgrade/gates-wip-04-04.json` · 기기 `/tmp/ch30-04/`(사본·실험·삽화 원본 둘·생성기 조각, 약 10MB) · 사용자 디스크 `.cache/ch30-04-view/`(보기 사본 셋).
