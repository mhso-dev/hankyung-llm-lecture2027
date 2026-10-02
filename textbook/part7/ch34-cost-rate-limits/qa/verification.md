# Ch34 검증 기록

> 「확인 필요 항목」까지는 **개선 전 판(2026-09-11)** 기록입니다. 품질 개선 절별 기록은 아래 「품질 개선 0N절」, 마감은 맨 끝 「품질 개선 마감」에 있습니다.

- 실행일: 2026-09-11
- 환경: Python 3.12.13, LangChain 1.4.0, langchain-openai 1.6.0
- 새 커널 실행: 5개 노트북, 코드 셀 26개 모두 성공
- 실제 API: 캐시 계측 2회, 모델 라우팅 비교 6회 실행
- 캐시: 첫 호출 `cache_read=0`, 두 번째 호출 `cache_read=11,520`; 두 호출 모두 텍스트와 출력 토큰 확인. `cache_creation=null`은 미제공 값
- 라우팅: 같은 3문항에서 GPT-5.4 nano 2/3, GPT-5.4 mini 3/3. 실제 응답 원문과 전체 `usage_metadata`를 `runs/routing-comparison.json`에 저장
- Batch: JSONL 3건 생성, 필수 키와 `custom_id` 중복 검사 통과. 파일 업로드와 Batch 생성·조회는 수행하지 않음
- Rate limit: 외부 제공자 과부하 없이 로컬 HTTP 서버에서 429 재현. 지수 백오프 후 200, 초기 큐 6건, 완료 6건, 최대 동시 실행 2 확인
- 예산: 고정 실습 자료에서 대화당 p50 0.0020달러, p95 0.0062달러; 0.005달러 목표 초과와 요청 전 차단 확인
- 코드 셀: 최대 19줄로 25줄 이하
- 빌드·정적 검사: 5개 절과 index 생성, 26개 코드 셀·최대 19줄 검사 통과
- 화면 검사: 1280px·390px의 6개 HTML에서 글자 크기, 대비, 잘림, 가로 넘침, SVG 경계, 복사, 다운로드 모두 통과
- 비밀값: API 키 값 출력 없음, `.env`와 `.venv` 공개 목록 제외
- 한국어 감사: 별도 모델의 Phase 6 최종 대조 완료, corrected

## 확인 필요 항목

- Batch API는 외부 제출하지 않았으므로 실제 처리 완료 시간, 결과 파일, 청구 비용을 확인하지 않았습니다.
- 모델 비교는 세 개의 단일 의도 분류 사례에 한정되며 운영 품질을 대표하지 않습니다.
- 대화당 비용 p95 자료는 계산 방식을 학습하기 위한 고정값이며 실제 서비스 청구 자료가 아닙니다.
- 공식 단가와 Rate limit은 계정 등급과 시점에 따라 바뀔 수 있어 배포 시 다시 확인해야 합니다.

## 품질 개선 01절 (2026-09-29)

위 기록은 개선 전 판(2026-09-11)입니다. 개선본 세부는 `qa/upgrade/01-diagnosis.md`, 챕터 공통 결정은 `qa/upgrade/handoff.md`, 흔들림 확인은 `qa/upgrade/probe/01-probe.md`에 있습니다.

- 환경: Linux aarch64 · Python 3.12.13 · 가상환경 `.cache/vm/venv-ch34-cost-rate-limits`(잠금 판 — langchain 1.4.0·langchain-openai 1.6.0·openai 3.13.0·python-dotenv 1.2.3) · 모델 `gpt-5.4-mini`(`temperature=0`·`reasoning_effort="none"`, 응답 날짜판 `gpt-5.4-mini-2026-03-17`).
- 흔들림 확인(노트북 밖, 첫 요청 전 §0 22:30:10Z): 5회차 × 요청 넷 = 20번(22:30:24Z~22:30:53Z, 오류 0) — 두 실행 첫 요청·실행 2 둘째 요청 캐시 입력 0 · 실행 1 둘째 요청 2816(5/5) · 128의 배수 20/20 · `cache_creation` 없음 20/20.
- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-29T22:43:28Z) · B(사본, `notebooks/` 커널, `PYTHONPATH` 없이, 22:43:50Z) — PASS 22셀, `code_sha256` `f5a17ed5…` 같음, `outputs_sha256` A `0a7c2201…` · B `e7b20c67…`. 셀별 출력 22개 가운데 15개 같음(다른 일곱은 입력 토큰 수 3166·3170 ↔ 3163·3167과 그 수로 셈한 표·요금 — 실험 번호의 토큰 수 차이). 캐시 입력·나머지·참거짓·답 글은 두 번 같음.
- 파일 쓰기 0(`runs/cache-measurement.json` 옛 파일 해시 그대로) · 도구 파일 `notebooks/cost_tools.py` 01 판 `af9e1288…`(공개 목록 두 곳에 줄) · 저장 출력에 Traceback·임시 위치·응답 ID·시각·키 0.
- 검사: 게이트 G1~G7 0(`gates-wip-01.json`) · `verify.py --chapter` PASS 5 sections / 43 code cells · 빌드 HTML `{{` 0 · Mermaid 4장(viewBox 폭 588·241·746·554) + 삽화 1장(job `168634ae…`, 2크레딧, 픽셀 대조 bbox `None`). `visual.cjs`는 챕터 마감 몫.
- 요금표 어림(2026-09-29 확인, 청구 금액 아님): 노트북 한 번 약 0.0077달러 · 작업 전체 요청 28번 약 0.054달러.

## 품질 개선 02절 (2026-09-29)

개선본 세부는 `qa/upgrade/02-diagnosis.md`, 노트북 밖 일괄 작업 기록은 `qa/upgrade/probe/02-batch.md`에 있습니다.

- 환경: Linux aarch64 · Python 3.12.13 · 가상환경 `.cache/vm/venv-ch34-cost-rate-limits`(잠금 판 — openai 3.13.0·python-dotenv 1.2.3) · 노트북은 표준 라이브러리와 도구 파일만 씀(설치 셀·키 셀·모델 셀 없음).
- 노트북 밖 일괄 작업 한 번(§0 23:08:21Z → 작업 만든 때 23:08:49Z → `completed` 23:10:57Z, 128초): 입력 5줄(1780바이트, `6ea21c43…` — 노트북 2절 셀로 만든 파일과 바이트까지 같음), 모델 `gpt-5.4-mini`, 요청 주소 `/v1/chat/completions`, 처리 기한 `24h` · 완료 4 · 실패 1(`inquiry-2` — `reasoning_effort` low + `temperature` 0 → 400 `unsupported_value`) · 사용량 입력 173·출력 18 · 요금표 어림 약 0.000105달러(50% 할인 넣음, 청구 금액 아님). 계정에 입력·결과·오류 파일과 작업 기록이 남음(지우지 않음).
- 자료 파일(ID·시각 뺌, 노트북은 읽기만): `labs/part7/ch34-cost-rate-limits/data/batch-output.jsonl` `41e43483…` · `batch-errors.jsonl` `965a2522…` · `batch-job.json` `6c8031d8…` — 공개 목록 두 곳에 줄.
- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-29T23:24:53Z) · B(사본, `notebooks/` 커널, `PYTHONPATH` 없이, 23:25:03Z) — PASS 29셀, `code_sha256` `51e2b77e…`·`outputs_sha256` `0d10754f…` 둘 다 같음, 셀별 29/29 같음. 짝짓기 Before/After 노트북 밖 5/5 같음.
- 파일 쓰기: 실습 폴더 0(입력 JSONL은 운영체제 임시 폴더, 옛 `runs/batch-input.jsonl` 해시 그대로) · 도구 파일 `notebooks/cost_tools.py` 02 판 `72429dfa…`(01 판 뒤에 `import json` + Ch 15 08 함수 넷) · 저장 출력에 Traceback·임시 위치·작업/요청 ID·시각·키 0.
- 검사: 게이트 G1~G7 0(`gates-wip-02.json`, 검사 문장 405) · `verify.py --chapter` PASS 5 sections / 67 code cells · 빌드 HTML `{{` 0 · Mermaid 4장(viewBox 폭 303·616·487·588) + 삽화 1장(job `6d54643e…` 2차 채택, 4크레딧, 픽셀 대조 bbox `None`). `visual.cjs`는 챕터 마감 몫.

## 품질 개선 03절 (2026-09-30)

개선본 세부는 `qa/upgrade/03-diagnosis.md`, 흔들림 확인은 `qa/upgrade/probe/03-probe.md`에 있습니다. 앞 작업자가 멈춘 자리에서 이은 재개 작업입니다(진단 §0).

- 환경: Linux aarch64 · Python 3.12.13 · 가상환경 `.cache/vm/venv-ch34-cost-rate-limits`(잠금 판 — langchain 1.4.0·langchain-openai 1.6.0·langchain-core 1.6.2·openai 3.13.0·python-dotenv 1.2.3) · 모델 `gpt-5.4-nano`·`gpt-5.4-mini`(`temperature=0`·`reasoning_effort="none"`, 이름만 다름).
- 흔들림 확인(노트북 밖, §0 23:48:49Z → 첫 요청 23:49:03Z): 5회차 × 6 = 30번, 오류 0, 설계로 정한 값·서비스 판단 값 모두 5/5 같음, 흔들린 값 없음.
- 새 커널 셋: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-30T00:00:50Z) · B0(사본, 00:01:17Z, 실행 조건 기록 없음) · B(사본, `notebooks/` 커널, `PYTHONPATH` 없이, 00:08:28Z) — PASS 23셀, `code_sha256` `2d7f2868…` 모두 같음, 셀별 출력 글 23/23 같음(`outputs_sha256` 차이는 첫 셀 `%pip` 출력의 스트림 나뉨뿐).
- 모델 요청: 노트북 한 번 6(nano 2·mini 4) · 작업 전체 48(흔들림 확인 30 + A·B0·B 18) · 요금표 어림 약 0.0019달러(청구 금액 아님). 서비스 오류 0.
- 파일 쓰기: 실습 폴더 0(옛 `runs/routing-comparison.json` `bf15958f…` 그대로) · 도구 파일 `notebooks/cost_tools.py` 02 판 `72429dfa…` 그대로 · 저장 출력에 Traceback·임시 위치·응답 ID·시각·키 0.
- 검사: 게이트 G1~G7 0(`gates-wip-03.json`, 검사 문장 383) · `verify.py --chapter` PASS 5 sections / 84 code cells · 빌드 HTML `{{` 0 · Mermaid 4장(viewBox 폭 507·418·511·624) + 삽화 1장(job `1b1deb81…` 1차 채택, 2크레딧, 픽셀 대조 bbox `None`). `visual.cjs`는 챕터 마감 몫.

## 품질 개선 04절 (2026-09-30)

개선본 세부는 `qa/upgrade/04-diagnosis.md`, 설치판 모양 확인은 `qa/upgrade/probe/04-shape.md`에 있습니다.

- 환경: Linux aarch64 · Python 3.12.13 · 가상환경 `.cache/vm/venv-ch34-cost-rate-limits`(잠금 판 — langchain 1.4.0·langchain-core 1.6.2·langchain-openai 1.6.0·openai 3.13.0·httpx 0.28.1·tenacity 9.1.4) · 모델 객체는 과정 표준 설정(`gpt-5.4-mini`·`temperature=0`·`reasoning_effort="none"`) + `base_url` = `127.0.0.1` 연습용 서버 + 가짜 키 — **OpenAI 서비스 요청 0**, 키 셀 없음, 모든 실행 `env -u OPENAI_API_KEY`.
- 연습용 서버 `labs/part7/ch34-cost-rate-limits/notebooks/always_429_server.py`(`3f25ebd8…`): 함수 하나 `wsgiref`, 모든 응답 429(답 글 없음), 모델 요청만 셈(머리 `practice-count`), `/reset`·`/count`. 노트북이 자식 프로세스로 띄우고(`stdout`·`stderr` 버림) 끝 셀에서 `terminate()`·`wait()` → −15. 실행마다 남은 프로세스 0·대기 포트 0. 공개 목록 두 곳에 줄.
- 설치판 모양 확인: 초안 6/6 같음(00:3x~00:39:32Z) · 생성기가 쓴 노트북 사본 5/5 셀별 같음(01:00:58Z~01:03:45Z) — 기본 3·`max_retries=0` 1·Before 9·After 3·동시 5 ↔ 2·요청 15.
- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-30T01:04:46Z) · B(사본, `notebooks/` 커널, `PYTHONPATH` 없이, 01:05:31Z) — PASS 24셀, `code_sha256` `85149d05…` 같음, 셀별 출력 글 24/24 같음(`outputs_sha256` 차이는 첫 셀 `%pip` 출력의 스트림 나뉨뿐).
- 파일 쓰기: 실습 폴더 0(옛 `runs/` 셋 그대로) · 도구 파일 `notebooks/cost_tools.py` 04 판 `7de7225a…`(02 판 + `import socket`·`import time` + Ch 28 03 `wait_for_port`, 01·02 가드 `skip` 확인) · 저장 출력에 Traceback·임시 위치·포트·주소·시각·키 0.
- 검사: 게이트 G1~G7 0(`gates-wip-04.json`, 검사 문장 427) · `verify.py --chapter` PASS 5 sections / 103 code cells · 빌드 HTML `{{` 0 · Mermaid 5장(viewBox 폭 267·685·274·612·656) + 삽화 1장(job `c3c6d588…` 2차 채택, 4크레딧, 픽셀 대조 bbox `None`). `visual.cjs`는 챕터 마감 몫.

## 품질 개선 05절 (2026-09-30)

개선본 세부는 `qa/upgrade/05-diagnosis.md`에 있습니다.

- 환경: Linux aarch64 · Python 3.12.13 · 가상환경 `.cache/vm/venv-ch34-cost-rate-limits`(잠금 판) · 노트북은 Python 기본 모듈 `math`와 도구 파일만 씀(설치 셀 없음) — **모델 요청 0**, 키 셀 없음, 모든 실행 `env -u OPENAI_API_KEY`.
- 자료: 이 절에서 정한 대화 스무 개의 토큰 수(입력·캐시 입력(128의 배수)·출력) → 도구 파일 `estimate_cost`(요금표 2026-09-29 mini 0.75·0.075·4.50 — 2026-09-30 모델 안내에서 다시 확인) → 대화당 비용. 결과는 정한 목록(대화 차례 포함)에서 본 것으로만 적음(b7).
- 설계 확인: 생성기 `--design-check`(코드 셀을 커널 없이 차례로 실행 — 본문 값 38개 출력에 있음) · 사본 실행 `/tmp/ch34-05/try1` PASS.
- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-30T01:48:41Z) · B(사본, `notebooks/` 커널, `PYTHONPATH` 없이, 01:48:52Z) — PASS 23셀, `code_sha256` `92e7ef90…`·`outputs_sha256` `627531578c0a…` 둘 다 같음, 셀별 출력 23/23 같음.
- 파일 쓰기: 실습 폴더 0(옛 `runs/` 셋 그대로) · 도구 파일 `notebooks/cost_tools.py` 05 판 `39bb0e25…`(04 판 + `import math` + `average`·`nearest_rank`(Ch 29 `eval_tools.py` = Ch 15 06 셀) + `make_budget`·`reserve`(Ch 16 04 셀 — `guardrails.py`와 AST 같음), 01·02·04 가드 `skip`·03 대조 통과 확인) · 저장 출력에 Traceback·임시 위치·시각·키 0.
- 검사: 게이트 G1~G7 0(`gates-wip-05.json`, 검사 문장 388) · `verify.py --chapter` PASS 5 sections / 121 code cells · 빌드 HTML `{{` 0 · Mermaid 4장(viewBox 폭 480·461·455·606, 보라·빨강 0) + 삽화 1장(job `7d80c904…` 2차 채택, 4크레딧, 픽셀 대조 bbox `None`). `visual.cjs`는 챕터 마감 몫.

## 품질 개선 06절 — 실습 절 (2026-09-30)

개선본 세부는 `qa/upgrade/06-design.md`·`06-diagnosis.md`, 흔들림 확인은 `qa/upgrade/probe/06-probe.md`에 있습니다.

- 새 절 `06-비용과-Rate-Limit-실습`(experiment, 챕터 시수에 더하지 않음 — meta 「실습 30분 · 새 용어 0」). 붙인 기능 01·03·05(흐름 안에서 출력으로 보임), 뺀 것 02·04(까닭 b3).
- 환경: Linux aarch64 · Python 3.12.13 · 가상환경 `.cache/vm/venv-ch34-cost-rate-limits`(잠금 판) · 설치 셀 langchain 1.4.0·langchain-openai 1.6.0·python-dotenv 1.2.3 · 모델 `gpt-5.4-nano`·`gpt-5.4-mini`(과정 표준 설정, 03 셀 그대로) · 요금표 2026-09-30 모델 안내 두 쪽 다시 확인(nano 0.20·0.02·1.25 · mini 0.75·0.075·4.50).
- 흔들림 확인: §0 저장 02:25:06Z → 첫 요청 02:25:25Z · 노트북 밖 5회차 × 요청 5 = 25번(서비스 오류 0) — 설계로 정한 값·서비스 판단 값 5/5 같음.
- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-30T02:36:47Z, `code_sha256` `ef7f93c07463…`·`outputs_sha256` `dbf373b58301…`) · B(사본, `notebooks/` 커널, `PYTHONPATH` 없이, 02:37:10Z, `outputs_sha256` `b1ffa2a29841…`) — PASS 26셀, 셀별 출력 20/26 같음. 다른 여섯은 토큰 수·비용 셀과, B에서 실행 1 대화 2(nano 둘째)의 캐시 입력이 0이었던 셀(본문 b6·b7·결과 읽기 둘째 단락에 밝힘).
- 모델 요청: 노트북 한 번 5(nano 2·mini 3) · 작업 전체 35(흔들림 확인 25 + A 5 + B 5), 요금표 어림 약 0.043달러(흔들림 확인 0.030298 + A 0.006059 + B 0.00657, 청구 금액 아님).
- 파일 쓰기: 실습 폴더 0 · 도구 파일 `notebooks/cost_tools.py` 05 판 `39bb0e25…` → 06 판 `5d2da3de…`(앞 절 노트북 함수 일곱을 셀 글 그대로 옮김, 01·02·04·05 가드 `skip`·03 대조 통과, 02·04·05 노트북 사본을 06 판으로 실행해 셀별 출력 같음) · 저장 출력에 Traceback·임시 위치·실험 번호 글·시각·키 0.
- 검사: 게이트 G1~G7 0(`gates-wip-06.json`, 검사 문장 440 · 챕터 전체 `gates-wip-ch34-after06.json` 6/6) · `verify.py --chapter` PASS 6 sections / 147 code cells · 빌드 HTML `{{` 0 · Mermaid 3장(viewBox 폭 461·363·682, 빨강 0, 보라 = 실제로 부른 두 모델) + 삽화 1장(job `455f2dcd…` 1차 채택, 2크레딧, 픽셀 대조 가장 큰 차이 0). `visual.cjs`·`check_delivery.py`는 챕터 마감 몫.

## 품질 개선 마감 (2026-09-30)

요약은 `qa/upgrade/chapter-summary.md`, 절 사이 인계의 마감 절은 `qa/upgrade/handoff.md` 「검토 반영과 챕터 마감 (2026-09-30)」입니다.

- 검토 1차 A(01~03·공통 — 상 1·중 4·하 11)·B(04~06 — 중 2·하 12) **30건 모두 반영**(마감이 더 고친 것: 01 b2 Ch 5 01 링크 경로 `ch05-llm-basics` → `ch05-llm-principles`, `check_delivery.py`가 찾은 깨진 링크).
- **노트북 재실행 0**: 여섯 노트북 `code_sha256`·`outputs_sha256`·`executed_at` 전후 같음(01 `f5a17ed5befb`/`0a7c2201e492` · 02 `51e2b77e959b`/`0d10754ff204` · 03 `2d7f2868d55a`/`1f1032aadab8` · 04 `85149d05fc2b`/`19201b0a9600` · 05 `92e7ef90171e`/`627531578c0a` · 06 `ef7f93c07463`/`dbf373b58301`). 01·02·03·05·06은 마크다운 셀만, 04는 파일까지 같음.
- 모델 요청 0 · Batch 작업·파일 올리기 0 · 삽화 생성 0.
- 도구 파일 머리 첫 줄을 「앞 챕터와 이 챕터 앞 절에서 배운 …」으로 고침: 06 판 `5d2da3de…` → `9fd988464043d075ef96963285f1b214a77930a1fc9507c460c13217974e009c`(함수 17개 본문·가져오기 줄 같음). 02·04·05 노트북 사본을 새 06 판으로 실행해 셀별 출력 29/29·24/24·23/23 같음.
- 게이트 `gates-after.json` **6/6 PASS · G1~G7 0**(검사 문장 373·409·385·429·391·444 = 2,431) · `verify.py --chapter` PASS 6 sections / 147 code cells (max 13 lines) · `visual.cjs` 14행 PASS · 빌드 HTML `{{`·`[[` 0 · 상대 링크 118개 깨짐 0.
- 학생 묶음 `part7-practice.zip` `af44a3287324…`(117항목, Ch 34 14파일이 디스크와 같음) — 풀어서 02·04·05를 키 없이 실행해 셀별 출력 같음(04 서버 정리·포트 0).

