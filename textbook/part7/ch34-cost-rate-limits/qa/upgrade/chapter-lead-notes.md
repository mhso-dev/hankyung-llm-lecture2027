# Ch 34 비용 · Rate Limit 엔지니어링 — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part7/ch34-cost-rate-limits`(절 다섯 — experiment 01·03·05, paired 02·04) · 실습 폴더 `labs/part7/ch34-cost-rate-limits`(`chapter.json` `lab_path`와 같음). Part 7의 마지막 챕터이자 **이번 품질 개선의 마지막 챕터**입니다. 바로 앞 개선 챕터는 Ch 31(완료), Ch 32·33은 이번 개선에서만 제외(과정에는 남음). 뒤 챕터 없음 — 과정표로는 다음이 Part 8 Ch 35 「0단계 — 무지침」(`커리큘럼_v6.html`, 교재 폴더 `textbook/part8` 없음).
- 준비 산출물: `qa/upgrade/before/`(원본 사본 **46개, 617,754바이트** — sha256 대조 46/46 같음) · `gates-before.json`(`a8bb38ae361bf50bf32186c3ada82c74c23216606b4fdf1effc6f8ca01541373`) · `before-manifest.json`(**191개**, `5a2afe9546d6391c77851f65a3b572f5719b3d7315d9fb498468db42da391017`) · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch34-cost-rate-limits`(215MB, 사용자 디스크).
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(전부) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 과정 요약(§0~§9 전부) · 계약 파일(`grep` 뒤 §3 Ch15 08 줄·Ch18/26/30/31 줄) · Ch 31 `chapter-summary.md`(전부)·`chapter-lead-notes.md`(구조·§11~§15) · Ch 30 요약 §5·§7·§8 · Ch 6·15·16·18·22·26·29 요약·`_src`에서 Ch 34와 닿는 곳 · Part 7 목록·목차·묶음·검사 스크립트 · 챕터 `qa/` 기록 · `커리큘럼_v6.html` Ch 34·Ch 35 줄. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.
- **원고·노트북·그림·실습 폴더 파일은 하나도 고치지 않았습니다**(보호 파일 191개를 끝에 다시 대조 — 바뀐 것 0). 연결 폴더 파일 삭제 0(`rm` 0), 노트북 실행 0, **서비스 모델 요청 0**, Batch 작업·파일 올리기 0, `uv cache prune` 안 함, 키 값 출력 0(루트 `.env`에는 이름 `OPENAI_API_KEY` 하나). 파이썬 호출은 모두 `PYTHONDONTWRITEBYTECODE=1`, 설치판 확인은 `OPENAI_API_KEY`를 지운 환경에서 가짜 키 `sk-local-test`로(요청은 모두 `127.0.0.1`로만). 로컬 서버는 확인 스크립트 안에서만 켜고 끔 — **남은 프로세스 0, 127.0.0.1 대기 포트 0**.
- 시수: `chapter.json` `hours` = 「총 8h · 강의 3h · 실습 5h」. 절 meta 강의 0.6 × 5 = **3h**, 실습 1 × 5 = **5h** — 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part7/_build_index.py` ch34 줄 `(3, 5)`도 같음. 새 용어 meta 4·4·4·5·5 = 22.

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-29)

| 절 | 코드 셀 | 코드 줄 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 프롬프트 캐시 계측 (experiment) | 5 | 38 | 79 | 5 | 3 | 5 | 1 | 6 | 10 | 3 | 33 |
| 02 Batch API (paired) | 5 | 32 | 66 | 12 | 5 | 5 | 0 | 7 | 10 | 3 | 42 |
| 03 모델 라우팅 (experiment) | 6 | 44 | 80 | 9 | 6 | 6 | 1 | 8 | 6 | 3 | 39 |
| 04 백오프 큐 동시성 (paired) | 5 | 50 | 70 | 5 | 9 | 5 | 0 | 7 | 9 | 3 | 38 |
| 05 예산 가드와 p95 (experiment) | 5 | 28 | 81 | 2 | 1 | 5 | 0 | 7 | 10 | 3 | 28 |
| **합계** | **26** | **192** | **376** | **33** | **24** | **26** | **2** | **35** | **45** | **15** | **180** |

- 통과 절 **0/5**. 코드 줄 = `count_code.py`(주석·빈 줄 뺌). 셀 최대 15·10·15·**17**·10줄.
- G1 33 = 제너레이터 식 15(준비 셀 `next(… for …)` 둘씩 × 01·02·03, `all(… for …)`·`sum(… for …)`·`"\n".join(… for …)`) · 내포식 9(목록 7·집합 1 — 02 `{row["custom_id"] for …}`) · 조건 표현식 7(준비 셀 셋, 03 `route`, 04 `Handler`, 05 둘) · **클래스 1**(04 `class Handler(BaseHTTPRequestHandler)`) · `*args` 정의 1(04 `log_message(self, *args)`) · **`global` 1**(04 `worker`).
- G2 24 = 세미콜론 8(01 [8] `run_dir = …; run_dir.mkdir`, 03 [8], 04 [5]·[8] 둘·[13] 둘) · 한 줄 복합문 4(04 [5]·[8] `for number in range(6): …`·[13] `if …: raise`, 05 [6] `for row in calls: …`) · 한 글자 변수 11(`p` 준비 셀 × 3절 둘씩, 02 `r`·`x`×2, 03 `r`×3) · 15줄 넘는 셀 1(04 [8] 17줄).
- G3 26 = **첫 줄 주석 없는 코드 셀 26 — 26셀 전부**(코드 주석이 챕터에 한 줄도 없음).
- G4 2 = 01 [8]·03 [8] 모델 셀에 `temperature=0` 없음(`reasoning_effort="none"`·`seed=34`·`max_tokens`·`max_retries=1`은 있음).
- G5 35 = 제목 셀·핵심 그림 첨부 없음 10 + 결과 읽기 인용 없음·빠짐 25.
- G6 45 = 70자 넘는 문장 16 · 영문 시작 조사 24 · 5문장 넘는 단락 5(용어 `dl` 줄).
- G7 15 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 것 (AST로 따로 셈 — `/tmp/ch34-prep/ast_scan.py`, 노트북 26셀)

- **f-string 9**(계산이 든 것 5 — 01 [5] `f"실험 ID: {uuid.uuid4()}\n"`·[11] `{row['input']}` 셋, 04 [5] `{server.server_port}` / 형식 지정 2 — 05 [8] `{p50:.4f}`·`{p95:.4f}`) · **별표 풀기 7**(준비 셀 `(here, *here.parents)` 둘씩 × 3, 05 `allow_call(*values)`) · **`next` 6** · `all` 5 · `sum` 3 · `enumerate` 2 · `max` 2 · `isinstance` 2 · `repr` 1 · `sorted` 1 · 집합 1 · `**`(거듭제곱) 1(04 `2 ** attempt`) · `+=` 3(04) · `while` 1 · 대입 풀기 4(04 [8] `active = peak = 0`·`queue, semaphore, completed, waits = …`, 03 [10] `inp, out = prices[model]`, 04 [13] `status, waits = …`) · `for` 대입 풀기 2(01 [11] `for index, row in enumerate(…, 1)`, 03 [8] `for text, expected in cases`) · 기본값 매개변수 1(04 `attempts=4`) · `.get` 9 · `raise` 4(준비 셀 셋 `FileNotFoundError`, 04 맨 `raise`).
- **비동기**: 04 [8] 셀 맨 위 `await asyncio.gather(worker(), worker(), worker())` · `async def worker` · `async with semaphore` · `await queue.get()` · `await asyncio.sleep(0.03)` · `asyncio.Queue`·`put_nowait`·`task_done`·`qsize`(Ch 2 요약 「처음 쓰면 한 문장」 목록의 `Semaphore`, 목록 밖의 `Queue`).
- **import 한 줄에 다섯 모듈**(04 [3] `import asyncio, json, random, threading, time`) · 표준 라이브러리 `http.server`·`urllib.request.urlopen`·`threading.Thread(daemon=True)`·`uuid`·`random.uniform`.
- **한 셀에 함수 둘**(04 [5] 클래스 메서드 둘 — 클래스 예외 조건 밖) · 셀 안 함수 03 `route` · 04 `worker`·`fetch_with_backoff` · 05 `nearest_rank`·`allow_call`.
- `assert`와 다른 문장을 한 줄에(04 [13] `server.shutdown(); assert status == 200`).
- 옛 노트북은 `metadata.verification` 모두 통과, 실행일 **2026-09-11**(사용자 맥), `code_sha256` 01 `1f8a671c…`·02 `e37299ee…`·03 `61e88876…`·04 `312098d5…`·05 `b024b219…`. 마크다운 셀은 2026-09-14 `.moai` part7 보조 스크립트가 끼운 「이 준비 셀이 하는 일」·「바로 다음 코드를 읽는 방법」·「이 단계에서 구분할 범위」 모양(Ch 30·31과 같음).

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청 · 요금 어림(청구 금액 아님) | 흉내 여부 | 파일 쓰기 | 손 값 | `assert` 대상 | `temperature=0`·none |
|---|---|---|---|---|---|---|---|
| 01 | 실험 ID(`uuid4`) + 정책 한 문장 × 420(22,724자) 앞부분 → 질문 둘로 `init_chat_model("openai:gpt-5.4-mini", reasoning_effort="none", max_tokens=40, max_retries=1, seed=34)` 두 번 → `usage_metadata`의 `input_token_details["cache_read"]` 0 → 11,520 · `cache_creation` `None` · 「비캐시 입력」 `[11805, 284]` | **2번** · 약 **0.0103달러**(첫 요청 11,805토큰 전부 일반 입력 0.00885 + 둘째 284 × 0.75 + 11,520 × 0.075 = 0.00108 + 출력 40 × 2 × 4.50 = 0.00036, 100만 토큰당) | 없음(실제 모델) | **`runs/cache-measurement.json`**(실습 폴더 안, 답 글·토큰이 흔들려 실행마다 해시가 바뀜) | 정책 × 420 · 질문 둘 · `max_tokens=40` | **`records[1]["cached_read"] >= 1024`(흔들리는 값)** · 답 글이 비지 않음·출력 토큰 > 0 | temperature 없음 · none 있음 |
| 02 | 문의 셋을 `/v1/responses`·`"model": "gpt-5-mini"`(과정 모델 아님) 요청 줄로 → JSONL 쓰기 → 필수 키·`custom_id` 중복 검사 → Before: 목록 전체를 JSON 배열 한 줄로 → 첫 줄이 `list` → After: 저장한 파일 줄마다 `dict` · 「실제 Batch 제출: 수행하지 않음」 | **0** · 0달러(제출 안 함) | Before가 스스로 만든 잘못된 글을 스스로 검사(§4) | **`runs/batch-input.jsonl`**(내용 결정적, 해시 `ee6ac19d…` — 같은 해시의 **떠돌이 사본이 루트 `batch-input.jsonl`에도 있음**, 옛 실행 흔적) | 문의 셋 · 모델 이름 | 구조 유효·`custom_id` 고유 · 줄 수 3 | 해당 없음 |
| 03 | 문의 셋(배송·환불·상품)을 nano·mini에 각각 → 정확 일치 채점 → 손으로 적은 요금 딕셔너리(캐시 입력 요금 없음)로 비용 → `route(text)`(길이 > 60 또는 「비교」·「근거」)가 두 문장에 모델 이름만 고름(부르지 않음) | **6번** · 약 **0.00016달러**(교재 출력 nano 0.00003325 + mini 0.00012225) | 없음 | **`runs/routing-comparison.json`**(흔들림 — 답 글·토큰) | 문의 셋·정답 · 요금(2026-09-11 값) · 길이 60 · 낱말 둘 | 답 글이 비지 않음 | temperature 없음 · none 있음 |
| 04 | 커널 안 스레드 서버(`BaseHTTPRequestHandler` 상속, 처음 두 요청 429·그 뒤 200) · `asyncio.Queue` 6개 + `Semaphore(2)` 일꾼 셋 → 「최대 동시 실행 2」 · Before `urlopen` 한 번 → 429 · After 지수 백오프(0.05 × 2^n + 0~0.01초 무작위) → 200 | **0** | **예 — 서버가 요청 차례(처음 둘)로 429를 보냄**, 작업 대신 `asyncio.sleep(0.03)`, 무작위 지터 | 0 | 429 둘·시도 4·0.05초·지터 0.01·세마포어 2·작업 6·0.03초 | `queue.empty() and peak <= 2` · `error.code == 429` · `status == 200` | 해당 없음 |
| 05 | 호출 11줄(대화 열 개, 비용 **손으로 적은 값**) → 대화별 합 → `nearest_rank(values, percentile)`(**0~1 비율**) p50 0.0020·p95 0.0062 → `allow_call(spent, estimated_max, hard_limit)` 두 경우 허용·차단 → 목표 0.005 초과 | **0** | 비용 값이 손 값(「고정 실습 데이터」) | 0 | 비용 11개 · 목표 0.005 · 검사 두 벌 | `p95 == max(costs)` | 해당 없음 |

- **한 번 실행 합계**: 모델 요청 **8번**(01 둘·03 여섯), 요금 어림 약 **0.0105달러**. 02·04·05는 API 키를 읽지만(02 준비 셀) 부르지 않음 — 05는 키 셀도 없음.
- **흔들리는 값**: 01 `cache_read`(둘째 요청이 캐시 입력을 받는지부터 — §3-1)·입력 토큰(실험 ID 길이·질문에 따라 ±몇 토큰)·답 글 · 03 답 글(nano의 「재질이 면인가요」 → `'배송'` 오답이 이 절의 핵심 관찰)·토큰·비용 · 04 지터 대기 `[0.052]`·걸린 시간 · 05 없음(손 값). **결정적 값**: 02 전부 · 04 요청 수·동시에 처리된 수의 가장 큰 값(§7) · 05 전부.
- **옛 그림 토큰**: 절마다 b4 `<figure>{{svg:NN-…}}` 하나(`figures/_gen_figures.py`가 만든 SVG·excalidraw 다섯 쌍) · 노트북 토큰 paired `{{notebook:slug|example}}`+`{{notebook:slug|failure}}`, experiment `{{notebook:slug}}`. **04 그림은 b4 개념 그림의 「로컬 429 응답」 상자를 빨강으로 칠함**(과정 색 규칙: 빨강은 paired Before 결함 결과만). Mermaid·삽화 0장. 챕터 공개 목록에 옛 SVG 줄 없음.
- 노트북 설명 셀: 제목 한 줄 · 결과 읽기 셀 0 · 준비물(요청 수·비용·시간)·실행일 문장 없음 · 첨부 그림 0 · **코드 주석 0줄**.
- `_src` b3·b8·b10(확인일 2026-09-11) · b9 복습 셋(05 넷) · b6 제목 paired 「일부러 실패해 보기」.

### 금지어·주의 말 (`_src` 산문 / 노트북 마크다운 — 코드 백틱 뺌, `/tmp/ch34-prep/ban34.py`, 코드 주석은 0줄)

| 절 | 걸린 말(`_src` / 노트북) |
|---|---|
| 01 | **캐시 24/7**(단독 「캐시」 — Ch 15 금지, 「캐시 입력」으로) · 토큰 23/6 · **접두어 14/5** · 적중 5/3 · 프롬프트 4/3 · 지시 3/1 · 지연 2 · 반환 2/2 · 측정 1 · 추정 0/1 · 메타데이터 1/1 · 대시보드 1 · 식별자 1/1 · 필드 1 · 보장 1 · 계측 1/1 · 「냉·온」 1 · 신청서 1(비유 — Ch 6 일상 예 「신청서 양식」과 겹침) |
| 02 | **배치 11/3 · Batch 9/3** · 제출 6/3 · 비동기 4/2 · **검증 4/3** · 완료 창 4 · 식별자 3/1 · 업로드 3/2 · 직렬화 2/2 · 엔드포인트 2/1 · 할인 2 · **사전 1**(「각 줄이 사전인지」) · 필드 1 · 창구·접수함 1(비유 — Ch 6 「상담 창구」 겹침) · 중단 1 · 「실패 재현」 0/1 |
| 03 | 라우팅 7/3 · **폴백 5/1** · **라우터 5/2**(Ch 26 03과 다른 뜻 — §6-1) · 경로 4/1 · 담당자 3(비유) · 측정 2 · 추정 2/1 · 오분류 2 · **기준선 2**(Ch 15 07 「기준선」 = 회귀 기준선과 다른 뜻) · 검증 2 · 범주 2/2 · 표본 2 · 배포 2 · 임계 1 · 평가셋·평가 세트 1/1 · 프롬프트 1 · **분기 1**(b3 — Ch 18 인계) · **스냅샷 1**(Ch 6은 「날짜판」) · 별칭 1 · 페이지 1 · 「알 수 있습니다」 1 |
| 04 | 백오프 7/4 · 지터 6/3 · 반환 4/3 · 세마포어 4/1 · **최대 4/1** · Rate limit 4 · 부하 3 · 통제된 2/1 · 지연 1/1 · 측정 1/1 · 헤더 1 · 처리량 1 · 동시성 1/3 · 입장·「문을 두드」 1(비유) · 「교육용」 0/1 · 「실패 재현」 0/1 |
| 05 | p95 18/7 · 상한 9/3 · **최대 8/2** · 가드 7/3 · p50 6 · 식별자 5/1 · 표본 5/2 · **최근접 4/1**(과정 말은 Ch 15 06 「가장 가까운 자리 방식」) · 지연 2 · 경로 2/1 · 집계 2/2 · 정산 2 · 꼬리 2 · **하드 리밋 1** · 폴백·라우팅·캐시·접두어·Batch 1 · 대시보드·트레이스·관측성 1 · **「Ch 35」 1(b8 — 틀린 앞 연결, §6-4)** · 「고정 실습 데이터」·「합성」 1 |

- 사용자가 금지한 표현(과정 규칙)은 챕터·실습 폴더 전체에서 0건(코드값으로 만든 문자열로 셈).
- **과정 말과 겹치는 것**: 「캐시 입력(cached input)」(Ch 6 06·Ch 15 05·06) ↔ 옛 01의 「캐시 읽기·캐시 생성·적중·접두어」 · 「예상 비용」(Ch 6 06 뜻)·「요금표로 어림한 요금」(Ch 16) ↔ 옛 03 「추정 비용」 · 「일괄 처리(Batch API)·요청 식별자(custom_id)·요청 주소(url)·요청 본문(body)·입력 파일」(Ch 15 08) ↔ 옛 02 「배치·식별자·엔드포인트」 · 「요청 제한(429)」(Ch 6 05 b7) · 「호출 한도·비용 상한·예약·예산」(Ch 16 04) · 「가장 가까운 자리 방식·95 백분위수·운영 지표」(Ch 15 06·Ch 29 04) · 「대체 모델·대체 경로」(Ch 6 05 `with_fallbacks`)·「예비 흐름·예비 모델」(Ch 16 05) ↔ 옛 03 「폴백」 · 「날짜판」(Ch 6 06) ↔ 옛 03 「스냅샷」 · 「응답 머리」(Ch 30 — 「헤더」 금지) · 「요청 주소」(Ch 30·15 — 「엔드포인트」 금지).
- 제목의 영어·약어: 챕터 「비용 · Rate Limit 엔지니어링」(`textbook/_notebook/build_index.py` 72행은 「비용과 Rate Limit 엔지니어링」 — 두 이름) · 01 「프롬프트 캐시」(「프롬프트」·단독 「캐시」 둘 다 금지어) · 02 「Batch API」 · 04 「백오프 큐 동시성」(세 말 모두 영어 뜻말·「동시성」은 Ch 31 금지 목록) · 05 「p95」.

## 2. 절별로 더 봐야 할 것

### 01 프롬프트 캐시 계측 (experiment)
- **옛 설명이 틀린 곳**: b6·노트북 [9]·b1 목표 3 「캐시 생성 값은 LangChain `usage_metadata`에서 얻지 못해 `None`」 — 설치판 langchain-openai 1.6.0은 서버가 `cache_write_tokens`를 보내면 `cache_creation`에 담음(`chat_models/base.py` 4355행·4409행, 독스트링 3628~3632행). 교재 출력에 그 키가 없었던 까닭은 **서버가 이 모델(GPT-5.6 이전)에서 캐시 쓰기 수를 보내지 않았기 때문**으로 보임(공식 안내: 캐시 쓰기 요금·보고는 GPT-5.6 이후, 이전 모델은 「No additional cache-write charge」). 「LangChain이 못 줌」 → 「이번 응답에 그 칸이 없었음」으로 고칠 곳.
- **b3 틀린 곳**: 「Ch 15에서는 추적 항목에서 캐시 읽기와 생성을 구분했습니다」 — Ch 15 05·06은 캐시 입력 토큰 수만 적음(05 b7 「사용량 안쪽 딕셔너리에는 칸 audio와 cache_read만 보였습니다」, 「캐시 생성」 0건).
- **Ch 15 05의 관찰**: 노트북 **첫 요청에도 캐시 입력 1792**(앞 절이 같은 요청 글을 보냄) — 앞부분을 고정하면 앞 실행의 캐시를 받을 수 있다는 실제 근거. 옛 01의 **맨 앞 실험 ID(`uuid4`)**가 첫 요청을 「캐시 입력 0」으로 만드는 장치라 지켜야 할 설계(SDK 독스트링: ZDR이 아닌 조직의 옛 모델 기본 보관은 `24h` — `types/chat/completion_create_params.py` 210~227행).
- 결과 읽기에 「11,520은 128의 배수」(공식 안내: 옛 모델은 `cached_tokens`를 128 배수로 내림) — 값은 흔들려도 **배수라는 성질**은 결정적 후보(밖 확인 필요).
- 비용 셈은 Ch 6 06 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`가 이미 캐시 입력을 뺀 나머지를 일반 입력으로 셈 — 옛 01의 「비캐시 입력」 목록 내포식을 대신할 수 있음(§8).
- 옛 셀 [8]은 한 셀에 요청 두 번 + 파일 쓰기 + 목록 출력(15줄) — 나눌 곳.

### 02 Batch API (paired)
- **Ch 15 08과 겹침**: Ch 15 08이 이미 요청 줄 네 칸·요청 식별자·JSONL 쓰기·다시 읽기·`line_problems`·`duplicate_ids`를 가르침(입력 파일 6줄 `runs/batch-eval-input.jsonl`, 요청 주소 `/v1/chat/completions`, **제출 0번**). 옛 02는 같은 일을 Responses 주소로 다시 함 + 제출 안 함 → 새로 가르치는 것이 거의 없음. 02가 더 가르칠 것은 **맡긴 뒤의 일**(파일 올리기 → 작업 만들기 → 상태 → 결과 파일·오류 파일 → `custom_id`로 짝짓기 → 할인 셈 → 취소).
- 옛 모델 `gpt-5-mini`(과정 표준 아님) · 요청 주소 Responses(Ch 15는 Chat Completions — Ch 15 요약 「수업에서 차이를 짚기」). LangChain `invoke` 기본 길은 Chat Completions(§7).
- Part 7 선행 목록 두 곳이 Ch 15 파일을 묶음에 넣지만 **옛 02는 읽지 않음**(b3 이름만).
- **말 겹침**: LangChain `model.batch([...])`(요청 여러 개를 곧바로 함께 보내는 메서드 — Part 2 「처음 쓰면 풀기」)와 일괄 처리(Batch API — 나중에 파일로 결과)를 가를 문장 필요(04에서 `batch(config={"max_concurrency": 2})`를 쓰면 더욱).

### 03 모델 라우팅 (experiment)
- **본문과 출력이 어긋남**: b4 「코드 읽기」 둘째 단락·노트북 [14] 「세 사례에서 두 모델이 모두 맞았더라도」 ↔ 출력은 nano 2/3.
- 라우팅 기준은 **규칙**(길이 60자·낱말 「비교」·「근거」) — 모델 판정 라우터 아님. 규칙은 두 문장에 모델 이름만 고르고 **고른 모델로 부르지 않음**(b4 「실제 모델 답은 선택 뒤 별도 호출에서 얻습니다」는 이 노트북에서 일어나지 않음).
- 요금 딕셔너리가 캐시 입력 요금을 빼고 튜플로 적음 — Ch 6 06 요금표 키(`ordinary_input`·`cached_input`·`output`)·`estimate_cost`와 다름.
- `answer == expected` 정확 일치 — 모델이 마침표·설명을 붙이면 틀림으로 셈(흔들림을 키움). `max_tokens=20`.
- 「폴백」 용어를 b4에서 정의하지만 코드에 없음(`with_fallbacks`는 Ch 6 05·07이 이미 가르침).
- 「모델 라우터」와 맨말 「라우터」 모두 씀 → Ch 26 03 인계(§6-1).

### 04 백오프 큐 동시성 (paired)
- **Before가 After의 결과를 정함**: 서버 수(`Handler.count`)가 커널 전체에 하나 — Before가 첫 429를 쓰고, After는 둘째 429 한 번 뒤 셋째에 200(그래서 대기 목록이 `[0.052]` 하나). After만 따로 돌리면 대기가 둘이 됨.
- 「대기 발생 작업: 6」은 뜻 없는 값(`perf_counter` 차는 늘 0보다 큼).
- b6 「실제 운영에서는 응답 헤더의 재시도 안내와 SDK의 내장 재시도 정책도 함께 확인합니다」 — 확인하지 않은 말. 설치판 SDK는 `Retry-After`·`retry-after-ms`를 따르고 없으면 0.5·1.0초(× 0.75~1 무작위) 지수 대기, 기본 재시도 2(§7 e1 — 모델 없이 결정적으로 보임).
- `Retry-After` 머리 없음 · SDK 재시도 없음 · 실제 모델 없음 · 비동기 문법 여럿(§1 G1 밖).
- b3 「Ch 16에서는 호출 한도와 재시도 함수를 직접 만들었습니다」 참 · 「Ch 30에서는 FastAPI 비동기 요청 처리」 참(Ch 30 요약 246행) — 그러나 **Ch 6 05(`max_retries`·`with_retry`·「요청 제한(429)은 이번에 실행하지 않았습니다」)·Ch 22 04(재시도·대체 모델 미들웨어 — 「모델 객체의 `max_retries`와 재시도 미들웨어를 함께 쓰면 시도 횟수가 곱해질 수 있습니다」, 실행 안 함)**를 가리키지 않음.

### 05 예산 가드와 p95 (experiment)
- **Ch 15 06·Ch 16 04와 겹침**: Ch 15 06이 이미 「이 절에서 정한」 대화 백 개로 p50·p95·p99·`nearest_rank`를 가르침, Ch 16 04가 `make_budget`·`reserve`(호출 한도·비용 상한·예약)를 가르침, Ch 22 05가 토큰 예산 미들웨어, Ch 29 04가 운영 지표·95 백분위수. 옛 05는 손 값 열한 개로 같은 계산을 되풀이.
- **같은 이름·다른 모양**: 과정 `nearest_rank(values, percent)`는 **0~100**(`math.ceil(percent * len / 100)`, Ch 15 06 셀 = Ch 29 `eval_tools.py`) ↔ 옛 05 `nearest_rank(values, percentile)`은 **0~1**. 그대로 두면 규격 §7-2 「같은 이름·다른 모양」 문장이 필요.
- b3 「Ch 15에서는 합성 비용 분포」 — Ch 15 말은 「이 절에서 정한 목록」.
- b8 「Ch 35 관측성에서는 …」 — **틀림**(§6-4).
- `allow_call` = `spent + estimated_max <= hard_limit` 한 줄(Ch 16 `reserve`와 같은 일, 예외 대신 참·거짓). 「예상 최대 비용」을 어떻게 셈하는지 코드 없음.

## 3. 실제 조건으로 보일 수 있는 것 (가장 중요 — 선택지와 장단점)

### 3-1. 01 프롬프트 캐시 (문서 근거만 — 모델은 부르지 않음, 01 작업자가 흔들림 확인에서 볼 것)
- **문서(2026-09-29 확인, `https://developers.openai.com/api/docs/guides/prompt-caching`)**: 캐시는 지원 모델에서 기본으로 켜짐 · 「The first request writes an eligible prefix to the cache and subsequent requests look for the longest matching cached prefix available」 · 「Cache reuse requires the entire rendered prefix to match」 · **최소 길이 1,024토큰은 GPT-5.6 이후 규칙**이고, 옛 모델은 「the minimum cacheable input length varies with request settings, including tools, images, output schemas, reasoning effort, and verbosity」 · 옛 모델 `cached_tokens`는 숨은 시스템 토큰을 빼고 **128 배수로 내림** · 적중은 「A request can reuse a cached prefix only if it reaches a machine holding a matching entry that has not expired」(보장 아님) · 같은 앞부분·키로 **분당 15번을 넘으면 다른 기계로 흩어질 수 있음** · 옛 모델 보관 `in_memory`(보통 쉬는 5~10분, 최대 1시간)·`24h` · GPT-5.6 이전은 안정된 `prompt_cache_key`로 같은 기계에 보내기를 권함 · 옛 모델 캐시 쓰기 추가 요금 없음 · 캐시 입력 할인 최대 95%(mini 모델 페이지 0.75 → 0.075 = 90%).
- **Ch 6 06 실측 선례**: 규칙 문장 50번(약 1,250토큰) 둘째 요청 캐시 입력 **0**, 80번(1,958토큰) **1792** — 1,024 넘는 길이에서도 0이 나온 기록.
- **결정적 후보**: 첫 요청 캐시 입력 0(맨 앞 실험 번호가 실행마다 다르면 앞 실행 캐시와 맞을 수 없음) · 캐시 입력이 128의 배수 · 캐시 입력 ≤ 입력 토큰 · **값 바꿔 보기로 「바뀌는 글을 맨 앞에」 두면 둘째 요청도 0**(앞부분이 첫 토큰부터 달라 맞을 수 없음 — 결정적일 가능성이 큼, 밖 확인 대상).
- **흔들리는 값**: 둘째 요청이 캐시 입력을 받는지 자체(기계 배정·만료) · 받은 수(11,520 같은 값) · 입력 토큰(±몇) · 답 글 · 비용.
- **01 작업자의 흔들림 확인(규격 §2-7 10번 끝)**: 노트북 밖에서 같은 두 요청 쌍(쌍마다 새 실험 번호)을 5번 → 「첫 요청 0 / 둘째 > 0 / 128 배수 / 받은 수」를 `01-probe.md`에 · 그림 라벨 규칙을 probe §0에 먼저(Ch 25 선례). 5/5면 「둘째 요청에서 캐시 입력을 받음」을 한정어와 결론에, 아니면 둘째 단락·b7에만.
- 선택지: (가) 옛 설계(실험 번호 + 약 11,800토큰) — 쌍당 약 0.0103달러, 밖 5쌍 + 새 커널 두 번 ≈ 0.07달러 · (나) 앞부분을 약 2,000토큰으로(Ch 6 06 길이) — 쌍당 약 0.0022달러, 다만 Ch 6 06처럼 짧으면 0이 나올 수 있어 probe가 더 중요 · (다) (가)·(나) + 호출 때 `prompt_cache_key="…"`(생성자에 넣으면 `UserWarning … transferred to model_kwargs`가 출력에 찍힘 — 호출 인자로 넣을 것, §7) · (라) 값 바꿔 보기 = 바뀌는 글을 맨 앞에(결정적 0 후보).

### 3-2. 02 Batch API
- **문서(`https://developers.openai.com/api/docs/guides/batch`, 2026-09-29)**: 「50% cost discount compared to synchronous APIs」 · 완료 창은 `24h`만 · 「Each batch completes within 24 hours (and often more quickly)」 — **보통 걸리는 시간은 문서에 없음** · 순서: JSONL(`custom_id`·`method`·`url`·`body`) → Files API `purpose="batch"` → `batches.create(input_file_id, endpoint, completion_window="24h", metadata)` → 상태 확인 → `output_file_id`·`error_file_id` 내려받기 → 취소 · 상태 여덟 `validating`·`failed`(입력 파일 검사 실패)·`in_progress`·`finalizing`·`completed`·`expired`·`cancelling`(최대 10분)·`cancelled` · 「the output line order may not match the input line order … use the custom_id field」 · 「each input file can only include requests to a single model」 · 요청 5만 줄·200MB · 「Any failed requests in the batch will have their error information written to an error file」 · 만료되면 끝난 요청만 결과에 남고 그 토큰은 청구 · 동기 요청 제한과 따로(요금 제한 문서 「without impacting your synchronous request rate limits」) · 캐시 입력 할인이 일괄 처리에도 붙는지는 문서에 없음.
- 설치판 SDK(openai 3.13.0): `client.batches.create/retrieve/cancel/list` · `client.files.create(file=, purpose="batch")`·`files.content` · `Batch.status` 여덟(`types/batch.py` 40~42) · `request_counts`(`completed`·`failed`·`total`) · `usage`(2025-09-07 이후 작업만) · 요청 주소 목록에 `/v1/chat/completions`·`/v1/responses` 등(`resources/batches.py` 47~67).
- **노트북 안에서 끝까지 기다리기**: 문서가 걸리는 시간을 약속하지 않고, `execute.py` 새 커널 실행·기기 셸 호출 180초·학생 수업 시간 모두에 안 맞음 → **노트북에서 완료까지 기다리는 설계는 권하지 않음**.
- **모델 없이 결정적으로 보일 수 있는 것**: 입력 파일 형식 검사(Ch 15 08과 겹침) · 한 파일 한 모델 검사(03 라우팅 결과를 한 파일에 섞으면 nano·mini가 섞임 — 실제로 일어날 법한 실수) · **결과 파일을 `custom_id`로 짝짓기 ↔ 차례로 짝짓기**(실제 결과 파일이 있어야 결함이 보임) · 할인 셈(요금표 × 0.5).
- **실제 작업이 필요한 것**: 상태 변화·완료 시각·결과 파일·오류 파일·`request_counts`·실제 할인 청구.
- 선택지:
  - (B1) **제출하지 않음**(옛 판 방향) — 비용 0·결정적, 그러나 Ch 15 08과 거의 같은 절이 되고 paired 결함도 스스로 만든 것.
  - (B2) **노트북 밖에서 한 번 실제 제출 → 끝난 작업의 배치 객체·결과 파일·오류 파일을 자료로 저장 → 노트북은 저장 자료를 읽어 짝짓기·셈**(Ch 29 04가 앞 챕터 저장 출력을 자료로 읽은 선례, 규격 §3 「실제 처리를 미리 계산한 값으로 바꾸지 않습니다」와의 관계는 「실제 처리 결과를 자료로 둔다」로 밝힘) — Before 후보: 요청 줄 하나에 실제로 실패하는 본문(예: 허용 범위 밖 인자)을 넣으면 결과 파일 줄 수가 입력보다 적어져 **차례로 짝지으면 뒤 줄이 밀림**(실제 결과로 결정적) ↔ After `custom_id`로 짝짓고 오류 파일을 따로 읽음. **어떤 인자가 줄 단위 실패로 가고 어떤 것이 작업 전체 `failed`로 가는지는 제출해 보기 전에는 모름**(문서에 없음 — 준비에서 제출하지 않음). 비용 어림: 짧은 문의 3~6줄 < 0.0005달러, Ch 15 08 파일 6줄(판정 요청 글 약 2천~3천 토큰씩)이면 약 0.006달러(50% 할인 반영). 계정에 파일·작업 기록이 남음(파일은 기본 30일 뒤 만료 — `types/file_create_params.py` 31행).
  - (B3) 노트북 안에서 올리기·만들기·상태 한 번까지만(상태 `validating`/`in_progress`가 실행마다 다름 — 흔들림), 결과는 (B2) 자료로 — 학생이 제 키로 따라 할 수 있는 장점, 요청이 계정에 남고 끝나기 전에 셀이 끝나 「결과를 받았다」를 보일 수 없음.
  - (B4) 입력 검사에 실패하는 작업을 일부러 만들어 `failed`를 보기 — 토큰 비용 없이 실제 조건일 가능성, 걸리는 시간·오류 모양 미확인.
- **Ch 15 파일을 쓸지**: (B2)에서 Ch 15 08 입력 파일(이미 Part 7 묶음에 들어 있음, 과정 모델·온도 0·추론 none, 요청 주소 Chat Completions)을 그대로 맡기면 「Ch 15에서 만들고 맡기지 않은 파일을 여기서 맡긴다」가 이어짐 — 판정 요청 글이 길어 비용·결과 글이 큼. 쓰지 않으면 선행 목록 줄을 그대로 둘지 마감에서 정함.

### 3-3. 03 모델 라우팅
- 옛 판: 규칙 라우터 · 두 모델 모두 부름(평가용 6번) · 고른 모델로는 안 부름.
- **Ch 26 03과 가르는 문장 후보**: 「Ch 26 03의 라우터는 문의를 분류해 맞는 전문 에이전트에게 보냈습니다. 이 절의 모델 라우터는 같은 요청을 어느 모델로 보낼지만 고릅니다.」 + Ch 18 02 「라우팅」(모델이 쓴 종류로 코드가 다음 단계를 고름)과도 한 문장.
- 결정적으로 보일 수 있는 것: **규칙이 문의마다 고른 모델 이름**(코드 값) · 고른 모델로 보낸 요청 수 셈 · 요금표 셈(토큰이 정해지면). 흔들리는 것: 답 글·정답 여부(특히 nano)·토큰·비용.
- 선택지: (가) 옛 흐름(두 모델 모두 평가 → 규칙) — nano 오답이 핵심 관찰이라 **§2-7 10번 끝 흔들림 확인 필수**(밖 5번, 뒤집히면 결론은 「규칙이 고른 모델」·셈으로) · (나) 규칙 라우터 → 고른 모델로만 요청 → 「모두 mini로 보냈을 때」 비용을 같은 토큰으로 셈(Ch 6 07 「같은 토큰 수를 mini 요금표로 계산하면」 선례) — 요청 수 절반, 결론은 배정·셈 · (다) nano가 허용 낱말 밖을 내면 mini로 다시(코드 검사 + 두 번째 요청 — 「검사 실패 뒤 상위 모델」, `with_fallbacks`는 오류일 때만 넘어가므로 답 검사에는 맞지 않음 — Ch 6 05 요약) — 다시 보낸 요청 수가 흔들림. 비용: (가) 문의 셋 6요청 약 0.0002달러, 문의 열 × 두 모델 20요청 약 0.0006달러.
- 요금: 모델 페이지(2026-09-29 확인) mini 0.75·캐시 입력 0.075·출력 4.50 / nano 0.20·0.02·1.25, 날짜판 `…-2026-03-17`, 지역 처리 10% 추가 — Ch 6 06(2026-09-17)과 같음. 요금 총표 페이지(`/api/docs/pricing`)에는 5.4 모델 줄이 보이지 않음(모델 페이지를 근거로).

### 3-4. 04 백오프·큐·동시성 (모델 없는 확인 — 모두 `127.0.0.1`, 가짜 키, §7 e1~e5)
- **실제 제공자 429를 결정적으로 재현하기는 불가능에 가까움**: 제한은 조직·프로젝트·모델별(요금 제한 문서) — mini Tier 1도 분당 500요청·50만 토큰. 문서: 「A `slow_down` error can occur even when your traffic is within its requests-per-minute and tokens-per-minute limits」.
- **실제 조건에 가장 가까운 길(확인만)**: 프로젝트 설정 「Limits」에서 모델별 요청 제한을 낮출 수 있음(도움말 `https://help.openai.com/en/articles/9186755`) → 전용 프로젝트 키로 실제 429. 계정 소유자 권한·전용 키·학생 재현 어려움·도착 시각에 따른 흔들림.
- **설치판에서 결정적으로 보인 것**(두 번 이상 같음): SDK `max_retries=0` → 서버 요청 1·`RateLimitError` · 기본(2) → **요청 3**·머리 `x-stainless-retry-count` `0,1,2` · `Retry-After: 0.2` → 간격 0.20초대로 따름 · `retry-after-ms` 우선 · 머리 없으면 0.40·0.93초(지수 + 무작위) · `Retry-After` 121초(> 120) → 다시 시도 안 함 · `x-should-retry: false` → 다시 시도 안 함 · `ChatOpenAI` `max_retries` 적지 않음 → 요청 3(**LangChain 문서의 「기본 6」과 다름** — 설치판은 SDK 기본 2), 0 → 1, 3 → 4 · 오류 이름 `langchain_openai…OpenAIRateLimitError`(`openai.RateLimitError`와 `langchain_core` `ModelRateLimitError`를 함께 이어받음 — 둘 다로 받을 수 있음) · **겹친 재시도: 모델 기본 재시도 + `with_retry(stop_after_attempt=3)` → 서버 요청 9, 모델 `max_retries=0` + 같은 `with_retry` → 3**(e5, 두 번 같음) · **동시에 보내는 수: `batch(["q"]*6, config={"max_concurrency": 2})` → 서버가 동시에 처리한 수의 가장 큰 값 2, 1 → 1, 없음 → 6**(동기 `batch`·`abatch` 모두, 두 번 같음 — **`async`/`await` 없이**) · `asyncio.Semaphore(2)`로 감싼 `AsyncOpenAI` 여섯 → 6/2/1(세 번 같음) · 함수 하나짜리 `wsgiref` 서버(클래스 없음)를 자식 프로세스로 띄워도 SDK 재시도 3번이 서버 기록에 찍힘(e3).
- 선택지:
  - (R1) **로컬 연습용 서버가 늘 429만 보냄**(답은 보내지 않음 → 가짜 모델 아님) + 요청 수 셈: Before **겹친 재시도 9** ↔ After **한 층만 3**(실제 코드 결함 — Ch 22 04가 적어 두고 실행하지 않은 일, Ch 6 05의 「모델 객체 안 재시도 시도 수는 세지 못함」을 서버 쪽에서 셈) · 동시에 보내는 수 6 ↔ 2(`max_concurrency`). 모델 0·결정적·비용 0. 단점: 429는 연습용 서버가 보낸 것(Ch 16 05 「실패 흉내」 선례와 같은 성격) — 본문에 「제공자의 429가 아님」을 밝혀야 함, 성공 장면 없음.
  - (R2) (R1) + 끝에 실제 모델로 같은 설정(`max_concurrency=2`, 문의 여섯) — 실제 답·`include_response_headers=True`로 실제 `x-ratelimit-remaining-requests` 등 머리 읽기(값은 흔들림, 칸이 있는지는 결정적 후보). 요청 6 ≈ 0.0012달러.
  - (R3) 요청 제한을 실제로 거는 로컬 중계 서버(창 안 허용 수를 넘으면 429 + `Retry-After`, 허용 요청은 실제 API로 넘김) — 성공 답이 실제 모델 답, 429 정책도 코드로 실제 동작. 서버 파일이 키를 다룸·복잡·도착 시각 흔들림.
  - (R4) 프로젝트 요청 제한을 낮춘 전용 키(위) — 가장 실제 조건, 재현·권한 문제.
  - (R5) 옛 판(커널 안 스레드 서버·차례로 정한 429·`sleep` 작업) — 클래스·`global`·비동기 문법 예외가 많고 Before가 After 결과를 정함.
- **서버 모양**: 과정 선례는 Ch 28 03·Ch 30의 `127.0.0.1` 자식 프로세스(띄우기 전 포트 빔·뒤 `poll() is None`·끝 셀 `terminate()`·`wait()`), 학생이 여는 서버 파일도 금지 문법 0(Ch 28 A-17). `http.server`는 처리 클래스를 이어받아야 하지만 **`wsgiref.simple_server.make_server`는 함수 하나로 됨**(e3에서 확인, 단 한 번에 한 요청만 처리 — 동시 수는 클라이언트 쪽에서 셈해야 함).

### 3-5. 05 예산 가드·p95
- 옛 판의 예산 계산은 손 값 합·Ch 6 `estimate_cost`와 다른 식(없음) · p95는 이름은 같고 인자 뜻이 다른 `nearest_rank`(0~1) · 걸린 시간 없음.
- 결정적으로 보일 수 있는 것: 자리 = `ceil(95 × n / 100)`(n이 정해지면) · 「p50 ≤ p95 ≤ 가장 큰 값」 부등식 · 예산 가드가 요청 **전에** 막아 요청 수가 늘지 않음(`reserve`가 `ValueError` — Ch 16 04) · 「예상 최대 비용 ≥ 실제 비용」(출력 상한 `max_tokens`로 출력 토큰 위를 막고, 입력은 보내기 전 `tiktoken` 셈 + 여유 — `tiktoken 0.14.0`에서 `encoding_for_model("gpt-5.4-mini")` = `o200k_base`, 옛 01 앞부분 11,761토큰 ↔ 서버 입력 11,805: 메시지 틀·실험 번호 몫 차이).
- 흔들리는 것: 실제 요청의 토큰·비용 → 대화당 비용·p95 값.
- 선택지: (가) 옛 손 값 유지(Ch 15 06 되풀이, 모델 0) · (나) 이 절 안에서 짧은 대화 여러 개를 실제로 보내 사용량 → `estimate_cost` → 대화별 합 → 95 백분위수, 가드는 `make_budget`·`reserve`로 요청 전 막기(대화 10개 × 평균 2요청 ≈ 0.007달러) — 값은 흔들려 결론은 부등식·요청 수 · (다) 앞 절(01·03) 기록 파일을 읽어 대화 단위로 묶기 — 파일 계약이 생기고 01·03 다시 실행마다 값이 바뀜 · (라) Ch 29 04처럼 앞 챕터 저장 기록을 자료로(요청 0).
- 과정 말로는 과정표 Ch 34 「예산 가드와 알림」 — 알림은 옛 판에 없음(프로젝트 월 지출 한도·알림은 대시보드 기능 — 도움말: 기본은 요청을 막지 않는 「soft」, 막는 한도는 따로 설정).

## 4. paired 절 Before 판정 (규격 §5-3 빨강 = Before 결함 결과, Ch 30·31 판정 방식)

| 절 | 옛 Before | 실제 결함인가 | After가 고치는가 | 모델 없이 결정적인가 | 실제 조건 후보 |
|---|---|---|---|---|---|
| 02 | 요청 목록을 `json.dumps(rows)`로 한 줄 배열로 만들고 줄마다 읽음 → 첫 줄 `list` → 「요청 객체로 판정: False」 | **약함** — 흔한 실수이긴 하나 결함 판정을 우리 `isinstance` 검사가 함(서비스가 거절하는 장면 아님), 파일로 쓰지도 않음(메모리 글), Ch 15 08 `line_problems`와 겹침 | 저장한 JSONL을 다시 읽어 `dict` — Before와 다른 자료를 읽음(같은 조건 비교 아님) | 예 | 결과 파일을 **차례로 짝지어 밀림**(실제 결과 파일 필요 — §3-2 B2) · **한 파일에 두 모델**(03 라우팅 결과를 섞은 입력 — 실제 작업이면 문서 규칙 위반, 결과 모양은 제출 전 모름) |
| 04 | 연습 서버가 처음 두 요청에 429 → `urlopen` 한 번 → 429 | **흉내 쪽** — 코드(재시도 없음)는 실제지만 429는 서버가 요청 차례로 정해 보냄(Ch 16 05 「실패 흉내」 성격), Before가 서버 수를 써서 After 결과를 바꿈 | 자작 백오프로 200 — 성공 200도 연습 서버의 글자 `200`(모델 답 아님) | 요청 수는 예, 대기 초는 아니오(지터) | **겹친 재시도 9 ↔ 3**(e5 — 실제 설치판 동작, 서버는 늘 429) · **동시에 보낸 수 6 ↔ 2**(e4 — `max_concurrency`) · 실제 모델 + 실제 응답 머리(R2) · 프로젝트 제한 키(R4) |

## 5. 실습 폴더 구조와 읽는 곳

```
labs/part7/ch34-cost-rate-limits/
  README.md  pyproject.toml  uv.lock  .venv/(맥 — /Users/… 링크, uv 0.11.6)
  notebooks/01~05-*.ipynb          (도구 파일·모듈·tests/ 없음)
  runs/batch-input.jsonl  runs/cache-measurement.json  runs/routing-comparison.json
```
- **코드로 읽는 곳**(`grep -rn`, `.venv`·`.cache` 뺌): `runs/batch-input.jsonl` ← 02 노트북 [8]·[13](자기가 쓴 파일) · 나머지 둘은 **읽는 코드 없음**(01·03이 쓰기만). 이름만: 공개 목록 두 곳(`textbook/part7/public-files.json` 100~110행·챕터 `qa/public-files.json`)·`qa/delivery-inventory.json`·Part 7 `final-artifact-hashes.json`(97~107행)·`verification.md`·옛 `_src`/HTML·`.moai/evolution/…/before*` 사본 · 루트 떠돌이 `batch-input.jsonl`(같은 해시, 누구도 안 읽음).
- **세 `runs` 파일이 학생 묶음·공개 목록에 들어감** → 01·03을 다시 실행하면(파일을 쓰는 한) 해시가 바뀌고 `part7-practice.zip`·`llm-practice.zip`·`final-artifact-hashes.json`과 어긋남(규격 §2-7 8번).
- 준비 셀이 `Path.cwd()`에서 위로 `ch34-cost-rate-limits` 폴더를 찾음 → **`execute.py`(저장소 루트 커널, `run_section.sh`)에서는 찾지 못해 `FileNotFoundError`**(옛 판은 `--cwd notebooks`로 실행). Ch 30 과정 표준 파일 위치 셀(후보 `..`·`.`·`labs/part7/ch34-cost-rate-limits`)로 바꿀 곳. `.env`는 위로 찾아 루트 `.env`를 읽음.
- README: `uv sync`(`--locked` 아님) · `execute.py … --cwd notebooks` · 「02는 Responses API용 Batch 입력을 만들고 검증하지만 제출하지 않습니다」·「04의 429는 로컬 HTTP 서버에서만」 · 요청 수·비용·도구 파일 설명 없음.
- **옛 생성기와 부르는 곳**: `figures/_gen_figures.py`(`a0f6ef78…`, 막혀 있지 않음 — Part 7 `check_figures.py` 20행이 파일이 있는지 `assert`) · 챕터 `qa/author_ch34.py` **없음** · 실습 폴더 `_generate.py` 없음 · `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part7_apply_depth.py`(111~127행 Ch 34 다섯)·`part7_review_fixes.py`(23~24·33~37·81행)·`part7_final_repairs.py` — **셋 모두 Ch 30 01이 맨 위 `raise SystemExit`로 막은 판**(해시 `f60d7287…`·`8cb946ea…`·`b171658f…`).
- 빈 폴더 `textbook/_notebook/checks/ch34-cost-optimization`(옛 이름, 기록만) · 화면 검사 결과 `textbook/_notebook/checks/ch34-cost-rate-limits/`(PNG 넷·`visual-results.json`) · 노트북 계약 `notebook-contracts-part7-ch34-cost-rate-limits.json`(`573426ca…`, `verify.py --chapter`가 다시 씀).

## 6. 앞뒤 이음새

### 6-1. 앞 챕터 인계 — 항목별 지금 상태

| 인계 | 내용 | 지금 원고 | 할 일 |
|---|---|---|---|
| **Ch 26 03 라우터**(계약 110행·Ch 26 요약 69·199행·최종 점검표) | Ch 34 03 「모델 라우터」·맨말 「라우터」는 Ch 26 03 「라우터」(분류해 전문 에이전트에게 보내는 쪽)와 다른 뜻 — 한 문장으로 가를 것 | **안 됨** — b4 용어·「코드 읽기」·노트북 [7]에 정의 없이 씀 | 03 b3·b4 첫 자리에 가르는 문장(§3-3 후보) |
| **Ch 18 02 라우팅**(Ch 18 요약 173행·최종 점검표 126행) | 03 b3 「Ch 18에서는 코드가 분기를 고르는 라우팅 패턴」 — 뜻은 참, 「분기」 → 「갈래」 | 그대로 | 03 b3 고침 + Ch 30 「요청 주소와 처리 함수 잇기(≠ Ch18 라우팅)」와도 겹치지 않게 |
| **Ch 29 04 운영 지표·95 백분위수** | `nearest_rank(values, percent)` 0~100 · 「요청 수 셈은 답까지 간 실행에서만」 · 운영 지표·공통 칸 | 05가 0~1 판·「최근접 순위」·「p95」, b3에 Ch 29 없음 | 05에서 과정 판을 가져오거나 모양 차이를 밝힘 |
| **Ch 30 04 b3**(Ch 30 요약 246행·계약 115행) | Ch 34 04 b3 「Ch 30에서는 FastAPI 비동기 요청 처리」 — 참 | 참 | 04가 비동기를 안 쓰게 되면 b3 문장 조정 |
| **Ch 31 전제 금지**(계약 117행·Ch 31 요약 §18) | 모델 요청 0 → 비용·토큰 기록·계약 파일 없음 · `create_task` 안 가르침 · Ch 32·33 개선본 전제 금지 | Ch 34에 Ch 31 언급 없음(참) | Ch 31 값을 비용 계산에 쓰지 말 것 |
| **Ch 6 요금 어림** | `estimate_cost`·요금표 키·「예상 비용 ≠ 청구 금액」·확인일(2026-09-17) · Ch 6 전제 금지 목록의 「캐시 유지 시간·`prompt_cache_key`, Batch·Flex·지역 처리 요금, 429·5xx·401」 = Ch 34가 처음 가르칠 것 | 03은 손 요금 딕셔너리·「추정 비용」, 01·05는 `estimate_cost` 안 씀 | 요금표·함수 이어 쓰기(§8) |
| **Ch 15 08 입력 파일**(계약 88행) | 02 b3가 이름만 가리킴 · Part 7 선행 목록 두 곳에 있음 · 02 노트북은 안 읽음(주소 차이) | 그대로 | 02 설계에 따라 읽거나 선행 목록 처분을 마감에서 |
| **Ch 15 01 b3 거짓**(§2 01) | 01 b3 「Ch 15에서 캐시 읽기와 생성을 구분」 | 거짓 | 고침 |
| **Ch 6 05·Ch 22 04** | 재시도·대체 모델·겹친 재시도(Ch 22 04 「곱해질 수 있습니다」 실행 안 함) | 04 b3에 없음 | 04 b3에 이음(겹친 재시도는 04가 처음 셀 수 있음) |
| **Ch 16 04·Ch 22 05** | `make_budget`·`reserve` / 토큰 예산 미들웨어 | 05 b3 Ch 16만 | 05 b3 |

### 6-2. Part 7 묶음·목록·기록·검사 (기록만, 고치지 않음)
- `_build_index.py`: `CHAPTERS` ch34 줄 `('ch34-cost-rate-limits', 3, 5, '사용량·대화 비용을 측정하고 캐시·라우팅·호출 제한·예산을 적용합니다.')`(「측정」 금지어) · **절 수 검사 없음**(목차가 `chapter.json`에서 셈) · Part 머리 손 글 「Ch 30–34 · N절 · 총 88시간 · 강의 28시간 · 실습 60시간」(시수 합 맞음) · 목차와 `part7-practice.zip`·`qa/integration-results.json`을 함께 다시 만듦.
- `textbook/_notebook/build_index.py` 72~73행 `('34', '비용과 Rate Limit 엔지니어링', …, 5, '캐시·모델 선택·호출 제한을 적용하고 대화 비용과 예산을 관리합니다.')` — 절 수 5(Ch 31 마감은 「과정 약속」으로 5 유지).
- 공개 목록: Part 목록 100~110행 11줄 · 챕터 목록 11줄(같은 내용, 차례 다름) · `prerequisite-files.json` 두 곳 = Ch 15 입력 파일 한 줄.
- `check_bundle_execution.py`: 풀린 묶음의 **모든** 챕터에 `uv sync --locked` + `import ipykernel, pip`, `smoke_sections`(27행)는 Ch 30 01·Ch 31 03·Ch 33 02만 — **Ch 34 노트북은 실행하지 않음**. 실행기가 `labs/part7/ch31-database/.venv/bin/python`(맥 링크)이라 이 기기에서 스크립트 그대로는 못 돎. `bundle-execution.json`의 Ch 34 줄 = `locked_sync: true, notebook_kernel_import: true`. Ch 34 잠금에 dev `pip==26.2`·`ipykernel==7.3.0` 있음(가져오기 조건 만족).
- `check_delivery.py`: 절마다 `_src` b1~b10·복습 3~5개·`[[작성:` 없음·링크 · `part7-practice.zip`과 **`llm-practice.zip`의 모든 파일이 디스크와 바이트까지 같아야 함** · `existing-artifacts-before.json`의 없는 Part 2 파일에서 멈춤(알려진 일).
- `check_figures.py`: 챕터마다 `figures/_gen_figures.py` `assert` → **Ch 30에서 이미 멈춤**(Ch 30 마감이 옮김) — Ch 34 옛 그림 다섯 쌍은 그 뒤라 닿지 않음.
- `final-artifact-hashes.json` Ch 34 32줄 · `visual-results.json` Ch 34 12행 · `figure-consistency.json` 5행 · `delivery-results.json` 5줄 · `review-findings.json` 1줄(옛 검토: 「max_output_tokens=20 빈 응답 → LangChain 호출로」).
- `part7-practice.zip` `6711c32a…`(Ch 31 마감 판) — Ch 34 11파일 + Ch 15 입력 파일 포함, `llm-practice.zip`에도 같은 12파일.
- `labs/part7/continuity-guide.md` 12행 「Ch6·29의 사용량·지연 측정 | Ch34 캐시·모델 선택·대기열·예산 | 최종 프로젝트의 품질과 비용 목표」(「지연」·「측정」 금지어, Ch 15·16·22 빠짐).

### 6-3. 완료 챕터가 Ch 34에 기대는 문장
- `textbook/part1~6/*/_src`·Ch 30·31 `_src`·완료 노트북·README에서 **「Ch 34」 링크 0**(`grep`, Ch 2 10 노트북 한 곳은 그림 base64 안 거짓 양성). 「Batch API」는 Ch 15 08·09 참고 자료 링크(공식 문서), 「429」는 Ch 6 05 b7(「이번에 실행하지 않았습니다」)뿐 — 개선 뒤에도 참이어야 할 Ch 34 쪽 문장은 없음.
- 뜻으로 기대는 것: Part 7 소개(`_src/index.html`) 「Ch34의 사용량 관리로 이어집니다」·「대화 비용을 절반 이하로 줄이는 활동은 비교 과제」 · continuity-guide 12행 · Ch 1 01 과정 지도(「Part 8 AI 페어 개발 Ch 35~41」).

### 6-4. 과정 끝 문장 (이번 개선의 마지막 챕터)
- **05 b8 「Ch 35 관측성에서는 비용 p95, 429 횟수, 큐 대기 시간, 모델 라우팅 결과를 같은 트레이스와 대시보드에서 확인합니다」는 거짓** — `커리큘럼_v6.html`의 Ch 35는 Part 8 「0단계 — 무지침」(코딩 에이전트 지침 단계), Ch 1 01도 「Part 8 AI 페어 개발 Ch 35~41」, 교재에 `part8` 폴더 없음, 과정표에 「관측성」 챕터 없음. 06 실습 절이 생기면 05 b8은 06을 가리키고, 06 b8(챕터 끝)은 Part 8·최종 통합 프로젝트를 **과정표에 적힌 만큼만**(「Part 8은 도구가 개강 전에 정해지며 세부는 그때 확정」 — 과정표 문구) 가리킬 것. continuity-guide 12행의 「최종 프로젝트의 품질과 비용 목표」는 과정표와 맞음.

## 7. 설치판 동작 — 모델 없는 확인 (2026-09-29, 가상환경 = 잠금 판)

### 7-1. 판과 사용량 칸
- 판: openai **3.13.0**(내부 HTTP는 **`httpx2` 2.12.0** — `http_client`에 넘길 것은 `httpx2.Client`, `_base_client.py` 37행·`_client.py` 181행) · langchain 1.4.0 · langchain-core 1.6.2 · langchain-openai 1.6.0 · langgraph 1.2.11 · httpx 0.28.1 · tiktoken 0.14.0 · python-dotenv 1.2.3 · ipykernel 7.3.0 · nbclient 0.11.0 · pip 26.2 — **Ch 30 잠금과 이 여덟이 모두 같음**(Ch 29·28은 openai 3.11.0, Ch 6은 3.10.0, Ch 15·16은 langchain-openai 1.6.1).
- **`init_chat_model("openai:gpt-5.4-mini", …)`의 `invoke`는 Chat Completions 길**(`_use_responses_api` 1900~1913행 — 이 모델 이름은 Responses 전용 목록 아님, 옛 출력의 `'audio'` 칸도 같은 증거).
- Chat Completions 사용량: SDK `PromptTokensDetails.cached_tokens`·`cache_write_tokens`(`types/completion_usage.py` 43·46행) → LangChain `input_token_details["cache_read"]` ← `cached_tokens`(4354행), `["cache_creation"]` ← `cache_write_tokens`(4355행), 값이 `None`이면 **키를 아예 뺌**(4381행 딕셔너리 거르기 — 그래서 `.get("cache_creation")`이 `None`). Responses: `input_tokens_details.cached_tokens`·`cache_write_tokens`(`types/responses/response_usage.py` 11·14행) → 4408~4409행. `priority`·`flex` 처리 등급이면 키 앞에 등급 이름.
- 캐시 인자: `prompt_cache_key`·`prompt_cache_options`(GPT-5.6 이후)·`prompt_cache_retention`(옛 모델 `in_memory`/`24h`, 문서상 사용 중단 예정 표시) — `completion_create_params.py` 189~227행. `init_chat_model(…, prompt_cache_key=…)`는 `UserWarning: prompt_cache_key is not default parameter … transferred to model_kwargs`(e0) → 호출 인자로 넣으면 경고 없이 요청 본문에 들어감(`payload = {**self._default_params, **kwargs}`).
- 응답 머리: `ChatOpenAI(include_response_headers=True)`(1075행)면 `with_raw_response`로 받아 `response_metadata`에 머리를 담음(1604~1609·1771~1785행) — 실제 `x-ratelimit-*`를 읽을 길.

### 7-2. 재시도·요청 제한 소스 행
- `openai/_constants.py` 7~13: `DEFAULT_MAX_RETRIES = 2` · `INITIAL_RETRY_DELAY = 0.5` · `MAX_RETRY_DELAY = 8.0` · `MAX_RETRY_AFTER_DELAY = 120` · 기본 시간 제한 600초(연결 5초).
- `_base_client.py` 488~489(`x-stainless-retry-count` 머리) · 753~789 `_parse_retry_after_header`(`retry-after-ms` 먼저, 다음 `retry-after` 초·날짜) · 791~813 `_calculate_retry_timeout`(서버가 준 0초 초과 120초 이하 대기를 그대로, 아니면 `min(0.5 × 2^n, 8) × (1 − 0.25 × random())`) · 815~855 `_should_retry`(`Retry-After` > 120이면 안 함 · `x-should-retry` 따름 · 408·409·429·5xx면 다시) · 1155~1167 `_sleep_for_retry`(`time.sleep`).
- LangChain: `ChatOpenAI.max_retries: int | None = None`(838행) → `None`이면 클라이언트에 넘기지 않아 SDK 기본 2(1371~1372행, e0 `client max_retries: 2`) · `OpenAIRateLimitError(openai.RateLimitError, ModelRateLimitError)`(594행) · `langchain_core.rate_limiters.InMemoryRateLimiter`(67·123~125행 — `requests_per_second`·`check_every_n_seconds`·`max_bucket_size`, 문서: 요청 수만 막고 크기는 못 막음, **「통에 담는 토큰」은 모델 토큰이 아님**) · `RunnableConfig["max_concurrency"]`(`runnables/config.py` 103행 — `abatch`는 `gather_with_concurrency`(내부 `Semaphore`), `batch`는 스레드 수) · `get_usage_metadata_callback`·`UsageMetadataCallbackHandler`(`callbacks/usage.py` 81·18행) · `with_fallbacks` 기본 `exceptions_to_handle=(Exception,)`.
- LangChain 문서(`https://docs.langchain.com/oss/python/langchain/models`)는 `max_retries` 기본을 **6**이라 적음 ↔ 설치판 실측 요청 3(재시도 2) — 교재는 설치판 값으로.

### 7-3. Batch SDK
- `client.batches.create(completion_window="24h", endpoint=…, input_file_id=…, metadata=…, output_expires_after=…)`(`resources/batches.py` 47~67) · `retrieve`·`cancel`·`list` · `client.files.create(file=…, purpose="batch")`·`files.content(file_id)` · `Batch` 칸 `status`(여덟)·`request_counts`·`output_file_id`·`error_file_id`·`errors`·`usage`·시각 칸 여럿(`types/batch.py`). 로컬 서버로 `batches.create` 요청 주소가 `/v1/batches`, 재시도 규칙이 같음을 확인(e1 — 요청 2, `max_retries=1`).

### 7-4. 모델 없는 확인 결과 (`/tmp/ch34-prep/exp/`, 출력은 같은 이름 `.out`)
- `e0_imports`: 판·모델 객체 만들기(가짜 키)·`prompt_cache_key` 경고·`configurable_fields`·`with_fallbacks`·오류 계보·배치 메서드.
- `e1_sdk_retry`: 늘 429를 보내는 스레드 서버로 SDK·`ChatOpenAI`·`init_chat_model` 재시도 수와 간격(두 번 실행, 요청 수·머리 모두 같음, 간격만 흔들림) — §3-4.
- `e2_semaphore`: `AsyncOpenAI` + `Semaphore` 동시 처리 수 6/2/1(세 번 같음, 걸린 초 0.22~0.54/0.62~0.64/1.26~1.28).
- `e3_child` + `limit_server.py`: 함수 하나 `wsgiref` 서버를 자식 프로세스로 — SDK 요청 3번·`x-local-count: 3`·`terminate()` 뒤 종료 코드 −15.
- `e4_max_concurrency`: `batch`·`abatch` `max_concurrency` 6/2/1(두 번 같음).
- `e5_stacked_retry`: 겹친 재시도 9 ↔ 3(두 번 같음).

## 8. §2-7 판단 근거 — 도구 파일

### 사실
- 앞 챕터 함수(모두 과정 문법 안, 같은 본문이 여러 도구 파일에 그대로 — AST 대조): **`estimate_cost`**(Ch 6 06 — 도구 파일 **열 곳**이 한 가지 본문: Ch 15·17·19·20·21·25·26·27·28·29) · **`sum_usage`**(Ch 19 05 — 일곱 곳 한 본문, **캐시 입력 칸은 모으지 않음**) · **`average`·`nearest_rank(values, percent)`**(Ch 15 06 셀 = Ch 29 `eval_tools.py` 117~130행, `math`) · **`make_budget`·`reserve`**(Ch 16 04 — `guardrails.py` 151~169행, `math.isfinite`·`raise ValueError`) · **`read_jsonl`**(Ch 15 08 — `rag_tools.py` 127~134행).
- 절끼리 다시 쓸 후보: 요금 어림(01 캐시 입력 할인·02 일괄 처리 절반·03 모델별·05 대화별) · 사용량 합(03·05) · 백분위수(05) · 요청 보내기·기록 한 줄(01·03·05) · JSONL 읽기(02).
- 과정의 도구 파일 이름(겹치면 안 됨): `git_tools`·`data_tools`·`llm_tools`·`rag_tools`·`agent_tools`·`workflow_tools`·`order_tools`·`graph_tools`·`runner_tools`·`checkpoint_tools`·`approval_tools`·`stream_tools`·`delegation_tools`·`harness_tools`·`connect_tools`·`eval_tools`·`serve_tools`·`guardrails`. **후보: `cost_tools.py`**(가장 뜻이 맞음) · `budget_tools.py` · `usage_tools.py` · `limit_tools.py` — 모두 과정에 없음.

### 선택지 (결정하지 않음 — 장단점만)
- (S1) **`cost_tools.py`를 01에서 만들기**: Ch 6 `estimate_cost`(+ Ch 21 등과 같은 본문 주석 「Ch 6 06절에서 배웠습니다 — Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다」) → 03·05에서 `nearest_rank`·`average`·`make_budget`·`reserve`를 더함. 장점: 요금 셈이 네 절에서 한 줄 · 과정 판 `nearest_rank`(0~100)를 쓰게 되어 모양 차이 문제가 사라짐. 단점: 판마다 해시 대조 사슬(Ch 24·25 교훈 — 앞 절 생성기가 긴 판을 덮어쓰지 않게) · 공개 목록·묶음에 새 파일.
- (S2) 도구 파일 없음(Ch 31처럼) — 절마다 셀에 다시 적음 → §2-7 3번 위반(앞 챕터에서 가르친 함수를 다시 적음), 코드 증가.
- (S3) 앞 챕터 도구 파일을 경로로 가져오기(예: Ch 29 `eval_tools.py`) — 과정 선례 없음(도구 파일은 챕터마다 따로), 묶음 경로 문제.
- 04 연습 서버 파일(선택 시)은 도구 파일이 아니라 실습 폴더의 실행 자료(Ch 28 서버 파일 선례) — 금지 문법 0 · 공개 목록에 넣기.

## 9. 모델·비용 선택지와 흔들림 처리 (결정하지 않음 — 장단점만)

### 9-1. 절마다 모델이 꼭 필요한가
| 절 | 실제 모델이 꼭 필요한 부분 | 모델 없이 결정적으로 보일 수 있는 부분 |
|---|---|---|
| 01 | **캐시 입력 자체**(실제 요청의 사용량에서만 보임) | 요금 셈·128 배수 성질·앞부분 토큰 셈(`tiktoken`) |
| 02 | 상태·결과 파일·오류 파일(실제 작업 — 노트북 안에서 기다리기는 비권장) | 입력 파일 검사·한 파일 한 모델·짝짓기 코드·할인 셈 |
| 03 | 모델별 답·정확도·실제 토큰 | 규칙이 고른 모델 이름·요청 수 셈·요금 셈 |
| 04 | 없음(실제 429는 재현 불가에 가까움) — 실제 머리·성공 답을 보이려면 선택 | 재시도 요청 수(1/3/4/9)·`Retry-After` 따르기·동시에 보낸 수(6/2/1) |
| 05 | 실제 대화 비용을 쓰려면 | 백분위 자리·부등식·요청 전 막기·요청 수 |

### 9-2. 흔들림 처리 (규격 §2-7 9번 끝·10번 끝)
- 결론·그림 라벨·정리에는 결정적 값(요청 수·자리·부등식·모델 배정·「첫 요청 0」)만. 캐시 입력 수·토큰·비용·걸린 초·답 글·정답 여부는 결과 읽기 둘째 단락·본문 표·「확인할 점」·b7에만 「이번 실행에서는」(Ch 25 03·Ch 31 01·Ch 26 04 선례).
- **01·03은 핵심 관찰이 모델 결과에 기댐**(01 「둘째 요청이 캐시 입력을 받음」·03 「nano가 한 문의를 틀림」) → 입력을 고치기 전에 밖 5번 확인·probe §0에 라벨 규칙 먼저.
- 04 대기 초는 지터라 늘 흔들림 → 시간 `assert` 금지(규격 §3), 결론은 요청 수.

### 9-3. 서비스 요청·비용 어림 (100만 토큰당 mini 0.75·0.075·4.50 / nano 0.20·0.02·1.25, 일괄 처리 50% — 확인 2026-09-29, 청구 금액 아님)
| 절 | 선택 | 노트북 한 번 요청 | 요금 어림(한 번) | 작업 전체(새 커널 두 번 + 밖 5번) |
|---|---|---|---|---|
| 01 | 옛 길이(약 11,800토큰) | 2 | 약 0.0103달러 | 약 0.07달러 |
| 01 | 약 2,000토큰 | 2 | 약 0.0022달러 | 약 0.02달러 |
| 02 | 제출 안 함 | 0 | 0 | 0 |
| 02 | 밖에서 한 번 제출(짧은 문의 3~6줄 / Ch 15 파일 6줄) | 0(노트북) | — | 0.0005 이하 / 약 0.006달러 |
| 03 | 문의 셋 × 두 모델 / 문의 열 × 두 모델 | 6 / 20 | 약 0.0002 / 0.0006달러 | 약 0.002 / 0.005달러 |
| 04 | 로컬 서버만 / + 실제 여섯 | 0 / 6 | 0 / 약 0.0012달러 | 0 / 약 0.01달러 |
| 05 | 손 값 / 실제 대화 10개 × 평균 2 | 0 / 20 | 0 / 약 0.007달러 | 0 / 약 0.05달러 |
- 어느 선택도 절마다 1달러 안(규격 §3). 06 실습 절은 규격 §7-2의 3~5번.

## 10. 과정 규칙과 부딪히는 것 (선택지와 장단점만)

### 10-1. 연습용 429 서버·`sleep` 지연과 규격 §3
- §3은 「가짜 모델」(정해 둔 응답을 내는 모델)을 막고 「실패 장면은 실제로 일어나는 조건」을 요구. **늘 429만 보내는 로컬 서버**는 모델 답을 흉내 내지 않지만 제공자 실패를 흉내 냄 — Ch 16 05 「실패 흉내」 선례(말로 정함)와 같은 쪽, Ch 30 07 「0초 재정의」·Ch 22 04 「없는 모델 이름」은 실제 조건 쪽. 선택지: (가) 흉내임을 본문·그림에 밝히고 **결함은 코드 쪽 사실**(겹친 재시도·동시 수)로 세움(Ch 19 06 「흔들린 모델 선택에 기대는 Before 결함은 코드 쪽 사실로」 선례와 결이 같음) · (나) 실제 조건만(R2·R4) — 재현성·권한 문제 · (다) 로컬 서버가 200 + 정해 둔 완료 JSON을 보내는 설계는 **가짜 모델에 해당**(쓰지 말 것).
- 옛 04의 `asyncio.sleep(0.03)`(작업 대신 기다리기)은 「sleep으로 만든 지연」 — 동시 수를 보려면 실제 요청(로컬 서버가 붙잡는 0.2초 또는 실제 모델)으로 바꿀 수 있음.

### 10-2. 비동기 문법 (Ch 28·30 허용 범위: 셀 맨 위 `await`·`async with`, `async def` 셀당 하나, `ainvoke`·`async for`, `asyncio.run` 셀 금지)
- 옛 04는 `Queue`·`Semaphore`·일꾼 셋·`global`·`while` — Ch 2 요약 「`Semaphore`는 처음 쓰면 한 문장」, `Queue`는 목록 밖. **동기 `batch(config={"max_concurrency": 2})`로 같은 관찰(동시 수 2)을 비동기 문법 없이 보임**(e4) — Part 2 「`batch`는 처음 쓰면 풀기」. 선택지: (가) `max_concurrency`(문법 쉬움, 라이브러리 기능) · (나) `Semaphore` + `ainvoke` + 셀 맨 위 `await gather(...)`(Ch 31 01 `gather` 선례, `async def` 하나, 제목의 「동시성」을 직접 보임) · (다) 둘 다(04 본문 길어짐). 「큐(대기열)」는 (가)·(나) 모두에서 라이브러리 안쪽 — 직접 `Queue`를 쓰지 않으면 제목 「큐」를 말로만 설명(강사 확인).

### 10-3. 요금 값(바뀌는 값)
- 모델 페이지 확인일을 준비물·b10에(`https://developers.openai.com/api/docs/models/gpt-5.4-mini`·`…/gpt-5.4-nano`, 2026-09-29) · 요금 총표 페이지에는 5.4 줄이 안 보임 · 일괄 처리 50%는 가이드 문장 · 지역 처리 10% 추가 · Ch 6 06 요금표 날짜(2026-09-17)와 값이 같음을 적을지.

### 10-4. 제목의 영어·약어
- 「Rate Limit」·「Batch API」·「p95」·「프롬프트 캐시」·「백오프」·「큐」·「동시성」 — 과정 관례는 「제목에만 남음(강사 확인)」 + 본문 첫 자리 풀이(Ch 15 03 「프롬프트」·Ch 30·31 선례). 본문 말 후보: 요청 제한(rate limit — Ch 6 05) · 일괄 처리(Batch API — Ch 15 08) · 95 백분위수(Ch 29 04) · 캐시 입력(Ch 6 06) · 기다리는 시간을 두 배씩 늘리기(지수 백오프) · 기다리는 시간에 더하는 작은 무작위 값(지터 — Ch 22 04 `jitter=False` 설명과 같게) · 대기열(큐) · 한꺼번에 들어갈 수 있는 수(세마포어).
- 슬러그는 목차·링크가 없으니(§6-3) 바꿀 수 있으나 공개 목록·계약 JSON·화면 검사 PNG 이름이 따라 바뀜 — 바꾸지 않는 편이 안전.

### 10-5. 「토큰」 뜻 가르기
- 모델 토큰(Ch 5 「조각」 = 토큰, 입력·출력·캐시 입력 토큰) ↔ Ch 28·30 **접근 토큰** ↔ `InMemoryRateLimiter`의 **통에 담는 토큰**(토큰 버킷 — 요청 허락 수) ↔ 요금 제한 문서의 TPM(분당 모델 토큰). 04에서 요청 제한기를 쓰면 한 문장 필요. 과정 요약 Ch 28·30 금지어 「토큰」 단독.
- 그 밖: 「라우터」(Ch 26) · 「일괄 처리」 ↔ LangChain `batch()` · 「기준선」(Ch 15 07) ↔ 03 「품질 기준선」 · 「호출 한도」(Ch 16 — 앱이 정한 요청 수 상한) ↔ 요청 제한(제공자) ↔ 바퀴 한도·실행 한도 · 「예상 비용」(Ch 6) ↔ 「예상 최대 비용」(05 가드) · 「캐시 입력」 ↔ 옛 「캐시 읽기」.

## 11. 삽화 비유 계열 후보 (앞 챕터와 겹치지 않게)

앞 챕터가 쓴 계열: Ch 1 사물함 · Ch 2 동전 저울 · Ch 3 창고 선반 · Ch 4 쟁반·카드 상자·서류철 · Ch 5 나무 쟁반·블록 · Ch 6 도서관 상담 창구·우편함·구슬·나무 레일·저울·동전·초시계·갈림길 카드 · Ch 7·8 책상 색 약속 · Ch 10 도막·공책과 장부 · Ch 11 쪽지·쟁반 · Ch 12 관·깔때기·구슬 · Ch 15 저울·사과·바구니 · Ch 16 쪽지·도장 대장·개찰구 · Ch 17 눈 위 발자국 · Ch 18 도예 · Ch 19 식당 주문 전표 · Ch 20 자료실 승강 상자 · Ch 21 세탁기 · Ch 23 체스판과 즉석사진 · Ch 24 도미노 · Ch 25 대나무 홈통과 물방울 · Ch 26 항구 예인선과 바지선 · Ch 27 온실과 모종판 · Ch 28 우주 정거장 도킹 포트 · Ch 29 오르골 종이띠 · Ch 30 화물 열차와 번호판 차량 · Ch 31 전화 교환대. **옛 Ch 34 비유**(신청서·창구 접수함·담당자 배정·입장 제한 문 앞)는 Ch 6 「창구」·「신청서 양식」과 겹침.

1. **「충전 거치대와 배터리」** — 미리 채워 둔 예비 배터리(01 캐시 입력) · 선반 가득 꽂아 두고 한꺼번에 밤새 충전(02 일괄 처리) · 크기가 다른 두 배터리를 쓰임에 맞게 고르기(03) · 꽂는 자리 두 개와 앞에 줄 선 배터리(04 동시 수·대기열) · 눈금 대신 채움 높이로만 보이는 잔량 막대(05 예산). 겹침 없음, 글자 없이 채움 높이로 그리기 쉬움. 「충전」이 전기 요금으로 읽혀 비용 주제와 맞음.
2. **「제과점 오븐과 반죽판」** — 미리 밀어 둔 반죽(01) · 한 판에 모아 굽기(02) · 작은 틀·큰 틀(03) · 오븐 칸 둘(04) · 밀가루 통 잔량(05). 겹침은 Ch 18 도예 가마와 결이 가까움(불·가마).
3. **「놀이기구 탑승 줄과 손목 밴드」** — 정원 둘인 탑승 칸(04) · 줄 선 사람 없이 빈 칸과 밴드만(사람 없는 그림 어려움) · 01·02는 약함. Ch 30 차량과 탈것 결이 가까움.
4. **「방앗간 곡식 자루와 저울 없는 됫박」** — 자루를 맡겨 두고 다음 날 찾음(02) · 미리 빻아 둔 가루(01) · 맷돌 두 개(04) · 됫박 수로 정한 몫(05). 03이 약함, 됫박이 Ch 2·15 저울 계열과 가까움.

## 12. 위험과 깨진 것

1. **05 b8 과정 끝 문장 거짓**(Ch 35 관측성 — §6-4) · 01 b3 거짓(Ch 15 캐시 생성) · 03 본문 「두 모델이 모두 맞았더라도」 ↔ 출력 2/3 · 01 「LangChain이 캐시 생성 값을 못 줌」 부정확.
2. **준비 셀이 루트 커널에서 멈춤**(`FileNotFoundError` — `run_section.sh`는 루트에서 실행) → 파일 위치 셀 필요.
3. **모델 의존**: 01·03 핵심 관찰이 흔들리는 모델 결과(캐시 기계 배정·nano 오답) · 01의 `assert records[1]["cached_read"] >= 1024`가 흔들리는 값에 걸림(규격 §3).
4. **요금**: 절마다 1달러 안(§9-3). 요금표 값은 바뀔 수 있음 — 확인일.
5. **Batch 작업 대기 시간**: 24시간 창, 보통 걸리는 시간 문서 없음 → 노트북 안 완료 대기 불가에 가까움 · 제출하면 계정에 파일·작업이 남음(파일 30일).
6. **계정 한도**: 실제 429 재현 불가에 가까움 · 프로젝트 제한을 낮추는 길은 권한·전용 키 필요 · 작업 중 01·03 여러 번 실행해도 Tier 1 한도(분당 500)에 한참 못 미침 · 캐시는 같은 앞부분 분당 15번을 넘으면 흩어짐(밖 확인을 한꺼번에 몰아 보내지 말 것).
7. **파일 쓰기 자리**: `runs/` 세 파일이 공개 목록·묶음·최종 해시에 있음 → 01·03 재실행마다 해시가 바뀜(02는 결정적) · 루트 떠돌이 `batch-input.jsonl`(삭제 승인 대상 — 제가 지우지 않음).
8. **04 로컬 서버**: 포트 충돌·남은 프로세스(자식 프로세스면 끝 셀 `terminate()`·`wait()` — Ch 28 규칙) · 커널 안 스레드 서버는 셀이 오류로 멈추면 커널이 죽을 때까지 남음 · `http.server`는 클래스 상속 필요(`wsgiref` 함수 판은 한 번에 한 요청).
9. **같은 이름·다른 모양**: `nearest_rank` 0~1 ↔ 0~100.
10. **옛 생성기**: `figures/_gen_figures.py`가 막혀 있지 않음(실행하면 옛 그림 열 파일을 다시 씀 — 01 첫머리에서 막기) · `.moai` 셋은 막힌 판.
11. **잠금**: dev `pip==26.2` 있음(Ch 31과 달리 과정 기준과 같음) · `%pip` 셀을 새로 넣으면 잠금과 판 맞추기 · `uv sync`는 마운트 폴더에서 막힐 수 있어 `UV_NO_SYNC=1`(run_section 자동).
12. **학생 환경**: 제 키로 실제 요청(요금) · 캐시 입력은 조직·지역마다 따로(문서) — 학생 출력과 교재 출력이 다를 수 있음 · Windows·macOS 미확인.
13. **기기 디스크**: 루트 여유 **1.6G → 1.5G**(가상환경은 사용자 디스크 215MB, `/tmp/ch34-prep` 96K) · `/tmp`에 공용 도구(`/tmp/mmd` 470M·`/tmp/pptr-cache` 662M·`/tmp/pw-browsers` 269M·`/tmp/uv-cache` 242M)와 끝난 Ch 31 임시 폴더가 남아 있음(오케스트레이터 몫).
14. **뒤 챕터 계약**: 없음(마지막 챕터, Ch 34 파일을 읽는 코드 0). 글 계약은 Part 7 소개·continuity-guide·과정 요약·최종 점검표.

## 13. 01절 작업자가 먼저 결정해야 할 것

1. **01 캐시 설계와 흔들림 확인(§3-1)** — 앞부분 길이(약 11,800 ↔ 약 2,000토큰), 맨 앞 실험 번호 유지, `prompt_cache_key`를 호출 인자로 넣을지, 값 바꿔 보기(바뀌는 글을 맨 앞에), 결정적 결론(첫 요청 0·128 배수·부등식)과 흔들리는 값(둘째 요청 캐시 입력 수)의 자리, **밖 5쌍 probe와 라벨 규칙을 첫 요청 전에**. 옛 「캐시 생성 None」 설명 고치기.
2. **말과 제목(§1 금지어·§10-4·§10-5)** — 「캐시 입력」(Ch 6·15)으로 이어 쓸지, 「프롬프트」·「캐시」·「Rate Limit」·「동시성」을 제목에만 남길지, 「요청 제한」·「일괄 처리」·「95 백분위수」·「가장 가까운 자리 방식」·「예상 비용」, 「라우터」(Ch 26)·「토큰」 세 뜻 가르기를 챕터 첫 자리에서 정해 handoff 용어 표에.
3. **§2-7 도구 파일(§8)** — `cost_tools.py`를 01에서 만들지(Ch 6 `estimate_cost` 한 본문 + 뒤 절에서 Ch 15 06·Ch 16 04 함수), 판마다 해시 대조 사슬을 첫 판부터(Ch 25 교훈), 05 `nearest_rank`를 과정 판(0~100)으로.
4. **파일 쓰기 자리(§5·§12-7)** — 01·03이 `runs/`에 계속 쓸지(묶음·해시가 실행마다 바뀜) ↔ 출력만 ↔ 임시 폴더(Ch 23·31 선례), 파일 위치 셀(Ch 30 표준)과 루트 커널 문제.
5. **모델 결정과 paired 두 절의 방향(§3-2·§3-4·§4·§9)** — 챕터 모델 결정(M 수준: 01·03 실제 / 02·04 모델 0 또는 일부 / 05 실제 ↔ 손 값), 02 Batch 실제 제출을 밖에서 한 번 할지(할 경우 누가·언제·자료 파일 이름과 공개 목록), 04 Before를 겹친 재시도(9 ↔ 3)·동시 수(6 ↔ 2)로 바꿀지와 비동기 문법(`max_concurrency` ↔ `Semaphore`), 연습용 서버를 흉내로 밝히는 문장.

## 14. 챕터 마감으로 미룰 것

- **06 실습 절 신설**(규격 §7-2): 슬러그 후보 **`06-비용과-Rate-Limit-실습`**(`_notebook/build_index.py` 제목 「비용과 Rate Limit 엔지니어링」의 앞부분 — `10-FastAPI-서빙-실습`·`09-평가-심화-실습`처럼 짧은 이름) · `06-비용과-Rate-Limit-엔지니어링-실습`(Ch 31 `06-DB와-상태-영속화-실습`처럼 제목 전체) · `06-비용-관리-실습`(영어 없음). 챕터 제목의 「·」는 슬러그에 쓰지 않음. 제목 「비용과 Rate Limit 엔지니어링 실습: …」 · `format: experiment` · meta 「실습 30분 · 새 용어 0」(**챕터 시수 3·5h에 더하지 않음**) · 새 문법·API 0 · 요청 3~5번. 주제 예(과정표 「자기 서비스의 대화당 비용을 절반으로 줄이는 과제 · 무엇을 포기했는지 함께 기록」): 문의 몇 개에 01 캐시 입력(긴 정책 앞부분)·03 모델 배정·05 예산 가드를 붙이고, 실행 2는 값 하나만(예: 라우팅 기준값·비용 상한·앞부분 차례) → 대화당 요금 어림과 포기한 것(정답 여부 등)을 한 표에.
- **Part 7에서 다른 점**: `_build_index.py` 절 수 검사 없음(자동 「N절」) · Part 머리 시수 손 글 「88시간」 그대로 · ch34 설명 한 줄(「측정」 금지어) · `textbook/_notebook/build_index.py` 72~73행 절 수 5(과정 약속으로 둘지)·설명 · `check_bundle_execution.py`는 Ch 34를 `uv sync`·가져오기만(06 또는 모델 없는 절을 `smoke_sections`에 넣으려면 스크립트 수정 — 후보로 기록, 실행기 맥 경로 문제) · `check_figures.py`는 옛 그림 짝·`_gen_figures.py`를 요구(이미 Ch 30에서 멈춤) · `check_delivery.py`는 `llm-practice.zip`까지 바이트 대조.
- 옛 생성기 `figures/_gen_figures.py` 막기(01 첫머리 `raise SystemExit`) → 마감 때 `qa/upgrade/before/generators/blocked/`로 `mv -n` · `.moai` part7 셋은 막힌 판 그대로(처분은 사용자·강사).
- 옛 그림 10개(`figures/0N-*.{svg,excalidraw}`) 삭제 승인 목록(사본 `before/figures/`, 공개 목록 줄 없음) · 빈 폴더 `textbook/_notebook/checks/ch34-cost-optimization` · 루트 떠돌이 `batch-input.jsonl`.
- `chapter.json` `objectives`(「캐시 읽기」·「Batch 입력」·「p95 예산 가드」 — 절 본문 말과 대조, 06 줄 더함, `hours` 8h = 강의 3 + 실습 5 = 01~05 meta 합)·챕터 `index.html` → `_build.py`·`_build_index.py`.
- 실습 폴더 README 다시 쓰기(`uv sync --locked` → `.venv` → `notebooks/`, 절별 요청 수·비용 어림·요금 확인일, 연습용 서버 파일·끄는 법, 일괄 처리 제출 여부와 자료 파일, 도구 파일) · `labs/part7/continuity-guide.md` 12행 · `qa/research.md`·`verification.md`·`집필점검표.md`에 「개선 전 판」 표시.
- 공개 목록 두 곳(06 노트북·도구 파일·서버 파일·자료 파일·`runs` 줄 처분) · 선행 목록 두 곳(Ch 15 파일을 02가 읽지 않으면 둘지) → `part7-practice.zip` 다시 만들기(마지막에 한 번) → 묶음을 풀어 파일 위치 셀·도구 파일 가져오기 확인.
- **과정 끝 마감(이번 개선 전체의 마지막)**: 05·06 b8 과정 끝 문장 · 과정 요약에 Part 7 마감 줄(오케스트레이터) · `upgrade-contracts.md` §5 새 zip · 최종 점검표 Ch 34 항목 · `llm-practice.zip` 전체 재생성 때 Ch 34 대조.
- 삭제 승인 대상: 실습 폴더 `.venv`(맥 — 묶음 실행 검사 실행기와 무관하지만 공개 목록 밖) · `.cache/vm/venv-ch34-cost-rate-limits`(215MB) · 기기 `/tmp/ch34-prep`(96K) · 생기면 `qa/upgrade/gates-wip-*.json`·`.cache/ch34-*`.

## 15. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 5 · `html` 5(빌드한 절 HTML) · `notebooks` 5 · `figures` 11(SVG·excalidraw 각 5 + `_gen_figures.py`) · `generators` 5(`_gen_figures.py` + `moai/` part7 스크립트 셋·`part7-author.md`) · `qa` 5(`delivery-inventory.json`·`prerequisite-files.json`·`public-files.json`·`research.md`·`verification.md`) · `lab` 6(README·`pyproject.toml`·`uv.lock`·`runs` 셋 — `.venv` 뺌) · `chapter.json`·`_build.py`·`index.html`·`집필점검표.md` = **46개, 617,754바이트**. 원본과 sha256 모두 같음 |
| `qa/upgrade/gates-before.json` | §0 표(합계 180, 통과 0/5, 문장 376), `a8bb38ae…` |
| `qa/upgrade/before-manifest.json` | sha256 **191개**(`5a2afe95…`) — ① 이 챕터 원고·실습 폴더 49(`qa/upgrade` 뺀 챕터 파일·실습 폴더 파일·`.venv/pyvenv.cfg`·노트북 계약 JSON·화면 검사 결과·루트 떠돌이 `batch-input.jsonl`) ② 앞 챕터 선례·가져올 함수 25(Ch 6 05·06 `_src`·`provider-comparison-continuity.json` / Ch 15 `rag_tools.py`·입력 파일·06·08 `_src`·노트북 / Ch 16 `guardrails.py`·04·05 `_src` / Ch 18 02·Ch 22 04·05·Ch 26 03·Ch 28 03·Ch 29 04·Ch 30 07 `_src` / Ch 21 `runner_tools.py`·Ch 28 `connect_tools.py`·Ch 29 `eval_tools.py`·Ch 30 `serve_tools.py`·잠금) ③ 챕터 요약 30 ④ Part 7 목록·목차·소개·`practice-start.md`·`qa/` 전부·continuity-guide 둘·`build_index.py`·`build_bundle.py`·`textbook/index.html`·zip·Part 7 화면 검사 52 ⑤ Part 7 다른 챕터 `chapter.json` 4 ⑥ 과정 끝 문장 근거 3(Ch 1 01 `_src`·HTML·`커리큘럼_v6.html`) ⑦ 옛 생성기 5(`.moai` part7 셋·`part7-author.md`·`review-part7.md` — 챕터 `_gen_figures.py`는 ①에) ⑧ 과정 문서·공용 도구 23. **끝에 다시 대조 — 191개 모두 같음** |
| `qa/upgrade/chapter-lead-notes.md` | 이 파일 |
| `$ROOT/.cache/vm/venv-ch34-cost-rate-limits` | Python 3.12.13 · 215MB |

### 가상환경 만든 방법과 결과
- Ch 31 준비와 같은 방법: `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy uv venv --python 3.12.13 …/venv-ch34-cost-rate-limits` → `uv pip install --python …/bin/python pip==26.2` → `uv export --project labs/part7/ch34-cost-rate-limits --frozen --no-hashes --all-groups --no-emit-project`에서 주석·들여 쓴 줄을 뺀 86줄(`/tmp/ch34-prep/req.txt` — 잠금 dev 그룹에 이미 `ipykernel==7.3.0`·`pip==26.2`·`nbclient==0.11.0`이 있어 바꾼 줄 없음) → `bin/python -m pip install --no-cache-dir -q -r`(한 호출). 설치 오류 0, `uv cache prune` 안 함.
- 결과: `pip freeze --all`과 잠금 대조 **판 차이 0**(설치 81 = 잠금 86 − 이 기기에 해당하지 않는 다섯: `appnope`(darwin)·`colorama`(win32)·`cffi`·`pycparser`(pypy)·`httpx2-jsfetch`(emscripten)). `pip check` 이상 없음. 커널 스펙 `share/jupyter/kernels/python3` 있음. `run_section.sh`는 `$ROOT/.cache/vm/venv-ch34-cost-rate-limits`를 자동으로 씀(`UV_NO_SYNC=1`).
- 디스크: 루트 1.6G → 1.5G · 사용자 디스크 74G 여유.

### 참고 자료 (2026-09-29 확인)
- OpenAI Prompt caching `https://developers.openai.com/api/docs/guides/prompt-caching` — §3-1 인용(옛 모델 최소 길이는 설정마다 다름·128 배수·기계 배정·분당 15번·`in_memory`/`24h`·`prompt_cache_key`·캐시 쓰기 요금은 GPT-5.6 이후·입력 비용 식). 옛 판 b10의 `…/guides/prompt-cache-diagnostics`는 **404**.
- OpenAI Batch API `https://developers.openai.com/api/docs/guides/batch` — §3-2 인용.
- OpenAI Rate limits `https://developers.openai.com/api/docs/guides/rate-limits` — RPM·RPD·TPM·TPD·IPM, 조직·프로젝트·모델별, `x-ratelimit-limit/remaining/reset-requests/tokens`(예 `1s`·`6m0s`), 「unsuccessful requests contribute to your per-minute limit」, `Retry-After`(예 56), `slow_down` ↔ `insufficient_quota`, 「Each official OpenAI SDK automatically retries eligible `429` and `503` responses」, 한도 셈은 `max_tokens`와 글자 수 어림 중 큰 값, 일괄 처리는 동기 한도와 따로.
- 모델 페이지 `https://developers.openai.com/api/docs/models/gpt-5.4-mini`·`…/gpt-5.4-nano` — 요금·날짜판·지역 10%·Tier별 RPM/TPM/일괄 처리 대기열(mini Tier 1 500·50만·500만, nano Tier 1 500·20만·200만).
- 요금 총표 `https://developers.openai.com/api/docs/pricing` — 5.4 줄 안 보임(모델 페이지를 근거로).
- 프로젝트 설정 `https://help.openai.com/en/articles/9186755-managing-your-work-in-the-api-platform-with-projects` — 모델별 요청 제한 설정·월 지출 한도(기본 막지 않음, 막는 한도 따로)·알림.
- LangChain Models `https://docs.langchain.com/oss/python/langchain/models` — 사용량 콜백·`InMemoryRateLimiter`(요청 수만)·`configurable_fields`·「max_retries 기본 6」(설치판과 다름)·OpenAI 캐시는 자동이고 `usage_metadata`에 보임.
- 설치판 소스 행: §7.
