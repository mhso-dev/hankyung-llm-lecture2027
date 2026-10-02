# Ch31 실행 검증

> **맨 위 「실제 결과」~「확인 필요 항목」은 개선 전 판(2026-09-11)의 기록입니다.** 품질 개선 기록은 아래 「품질 개선 NN절」과 끝 「마감」 절, 챕터 요약 `qa/upgrade/chapter-summary.md`에 있습니다.

- 실행일: 2026-09-11
- Python 3.12.13
- 독립 데이터베이스: `kdt-ch31-postgres`, `localhost:55431`, PostgreSQL 17.8, pgvector 0.8.1
- 재시작: `docker start kdt-ch31-postgres`; 준비 확인: `docker exec kdt-ch31-postgres pg_isready -U postgres`
- 제거: 전체 Part 7 묶음 검증이 끝난 뒤 `docker rm -f kdt-ch31-postgres`

## 실제 결과

- 01절: 질문은 `['환불', '배송', '결제']` 순서로 조회됐습니다. 0.15초 대기 세 건은 순차 0.468초, 동시 0.195초였습니다.
- 02절: 별도 트랜잭션 Before는 잔액 400·500과 총액 900을 남겼습니다. 한 트랜잭션 After는 500·500과 총액 1000을 유지했습니다.
- 03절: `upgrade head` 뒤 `ch31_migration.tickets`, `downgrade base` 뒤 NULL, 재적용 뒤 같은 표를 확인했습니다.
- 04절: 풀 크기 1·추가 연결 0·대기 0.2초에서 `TimeoutError`를 재현했습니다. 점유 시간을 줄이고 대기를 1초로 둔 실행은 두 결과가 모두 1이며 체크아웃 연결 0으로 끝났습니다.
- 05절: 코사인 검색 첫 결과는 ‘배송’이었고 3행의 실행 계획은 Seq Scan을 선택했습니다. value 6을 12로 계산한 실행은 체크포인트 3행을 저장했습니다. 논리 덤프를 별도 `ch31_restore` 데이터베이스에 복원해 문서 3행, 체크포인트 3행, HNSW 인덱스 존재를 확인했습니다.

## 자동 검증

- `execute.py`: 다섯 노트북 모두 새 커널 PASS, 코드 셀 27개
- `_build.py`: index와 다섯 절 HTML 생성
- `verify.py --chapter`: 5 sections / 27 code cells, 최대 25줄 PASS
- 서비스 정적 검사와 실행: `ruff check`, `python -m app.service`
- 공개 파일: `qa/public-files.json`에 루트 상대 경로만 기록하고 `.env`, 실패 기록, 개인 절대 경로를 제외했습니다.

## 확인 필요 항목

운영 데이터 규모의 HNSW 재현율·지연, 전체 연결 예산, 정기 복원 훈련과 보존 정책은 이 로컬 실습으로 확인하지 않았습니다. 복원 데이터베이스에서 그래프 스레드를 다시 재개하는 경로도 추가 검증 항목입니다. 본문 한국어 감사는 작성자와 다른 검토자가 완료했으며 accept 판정입니다.

## 품질 개선 01절 (2026-09-29)

위 기록은 개선 전 판(2026-09-11)입니다. 개선본 세부는 `qa/upgrade/01-diagnosis.md`, 챕터 공통 결정은 `qa/upgrade/handoff.md`에 있습니다.

- 데이터베이스: 작업 기기에는 Docker가 없어 `qa/upgrade/pre_exec.sh`(`run_section.sh`가 절 실행 직전에 source)가 `.cache/vm/pgenv`의 PostgreSQL 17.11 + pgvector 0.8.1로 `/tmp/ch31-pg/data` 클러스터를 교재와 같은 접속 글(`postgresql+asyncpg://postgres:postgres@127.0.0.1:55431/ch31_lab`, 연습용 비밀번호)로 켜고, 부른 셸이 끝날 때 `trap EXIT`로 끔. 끝낸 뒤 postgres 프로세스 0·55431 포트 0.
- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, 2026-09-29T15:54:38Z) · B(사본, `notebooks/` 커널, 15:54:53Z) — PASS 21셀, 셀별 출력 21개 가운데 19개 같음(다른 둘은 걸린 초가 찍힌 셀 [13]·[19] — 차례로 0.48 ↔ 0.47, 함께 0.19 같음), `code_sha256` `addb4391…` 같음, `outputs_sha256` A `145e0cf3…` · B `c63727fa…`. 두 실행 모두 `OPENAI_API_KEY`를 지운 환경·`PYTHONDONTWRITEBYTECODE=1`.
- 같은 커널 세 번 이어 실행(`/tmp` 사본) · 노트북 밖 파이썬 파일 여섯 번: 기록 앞 세 개·연결 수 1 ↔ 3·받은 값·`함께 기다린 시간이 더 짧은가: True` 모두 같음. 걸린 초는 차례로 0.47~0.48, 함께 0.19~0.20.
- 모델 요청 0 · 실습 폴더에 새로 생긴 파일 0(노트북 01 말고) · pyc 0 · `.failure.json` 0.
- 게이트 G1~G7 0(`gates-wip-01.json`) · `verify.py --chapter` PASS 5 sections / 43 code cells · 빌드 HTML `{{`·`[[` 0.

## 품질 개선 02절 (2026-09-29)

개선본 세부는 `qa/upgrade/02-diagnosis.md`에 있습니다. 데이터베이스는 01절과 같은 훅(`qa/upgrade/pre_exec.sh`, 재시작 뒤 `initdb`부터 다시 만든 `/tmp/ch31-pg/data`, 교재와 같은 접속 글)으로 켰습니다.

- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, `executed_at` 2026-09-29T16:31:16Z) · B(사본, `notebooks/` 커널, 16:31Z) — PASS 23셀, **셀별 출력 글자 23개 모두 같음**, `code_sha256` `39d29f86…` 같음, `outputs_sha256` A `a44f100e…` · B `22e565f5…`(설치 셀 출력 조각 나눔만 다름). 두 실행 모두 `OPENAI_API_KEY`를 지운 환경·`PYTHONDONTWRITEBYTECODE=1`.
- 노트북 밖 파이썬 파일 다섯 번(`/tmp/ch31-02/exp/p1_scene.py`): 출력 다섯 번 모두 같음 — Before `23514` → `[(1, 500), (2, 1100)]` 합계 1600 · After 같은 오류 → `[(1, 500), (2, 500)]` 합계 1000 · 블록 안 2번 1100 → 밖 500 · 500 이체 → `[(1, 0), (2, 1000)]`.
- 모델 요청 0 · 실습 폴더에 새로 생긴 파일 0(노트북 02 말고) · pyc 0 · `.failure.json` 0 · 끝낸 뒤 postgres 프로세스 0·55431 포트 0.
- 게이트 G1~G7 0(`gates-wip-02.json`, 검사 문장 376) · `verify.py --chapter` PASS 5 sections / 61 code cells · 빌드 HTML `{{`·`[[` 0.

## 품질 개선 03절 (2026-09-29)

개선본 세부는 `qa/upgrade/03-diagnosis.md`에 있습니다. 데이터베이스는 01·02절과 같은 훅(`qa/upgrade/pre_exec.sh`, `/tmp/ch31-pg/data`, 교재와 같은 접속 글)으로 켰습니다. 노트북은 Alembic에 동기 드라이버 판 접속 글(`postgresql+psycopg://…@127.0.0.1:55431/ch31_lab`)을 환경 변수 `CH31_SYNC_URL`로 넘깁니다.

- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, `executed_at` 2026-09-29T17:09:43Z) · B(사본, `notebooks/` 커널, 17:09Z) — PASS 31셀, **셀별 출력 글자 31개 모두 같음**, `code_sha256` `f97cba07…` 같음, `outputs_sha256` A `875e6c2e…` · B `ddcf90d9…`(끝 셀 출력 조각 나눔만 다름). 두 실행 모두 `OPENAI_API_KEY`를 지운 환경·`PYTHONDONTWRITEBYTECODE=1`.
- 묶음 모양: `part7-practice.zip`을 `/tmp/ch31-03/bundle`에 풀고 03 노트북만 새 판으로 바꿔 `--cwd …/ch31-database/notebooks`, 키 없이(`.env` 0) PASS 31셀 — 셀별 31개 같음, `outputs_sha256` A와 같음(`875e6c2e…`), 묶음 `migrations/`에 새 파일 0.
- 노트북 밖 파이썬 파일 다섯 번(`/tmp/ch31-03/exp/e1_scene.py`): 출력(stdout·stderr) 다섯 번 모두 같음 — Before `23502` → 판 `20260911_01`·칸 둘 · After → `20260929_02`·세 줄 `'미정'` · 판 내리기 → 칸 둘 · 다시 올리기 → `'민지'`가 `'미정'`.
- 모델 요청 0 · 실습 폴더 파일 17개(`app/`·`migrations/`·`alembic.ini`·README·잠금·맥 pyc) sha256 전후 같음 · 새로 생긴 파일 0(노트북 03 말고) · pyc 0 · `.failure.json` 0 · 끝낸 뒤 postgres 프로세스 0·55431 포트 0.
- 게이트 G1~G7 0(`gates-wip-03.json`, 검사 문장 457) · `verify.py --chapter` PASS 5 sections / 86 code cells · 빌드 HTML `{{`·`[[` 0.

## 품질 개선 04절 (2026-09-29)

개선본 세부는 `qa/upgrade/04-diagnosis.md`에 있습니다. 앞 작업자가 기기 연결이 끊겨 멈춘 자리부터 이어 한 재개 작업입니다(설계·노트북 밖 확인은 앞 작업자 기록 그대로, 재개 뒤 노트북 밖 2번 더 같음). 데이터베이스는 01~03절과 같은 훅(`qa/upgrade/pre_exec.sh`, `/tmp/ch31-pg/data`, 교재와 같은 접속 글)으로 켰습니다. 노트북은 표·이름 공간을 만들지 않고 `SELECT current_database()`만 보냅니다.

- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, `executed_at` 2026-09-29T18:54:00Z) · B(사본, `notebooks/` 커널, 18:54:09Z) — PASS 21셀, **셀별 출력 글자 21개 모두 같음**, `code_sha256` `d919bdcd…` 같음, `outputs_sha256` `1673bbd9…` 같음. 두 실행 모두 `OPENAI_API_KEY`를 지운 환경·`PYTHONDONTWRITEBYTECODE=1`. 모든 셀 stderr 0.
- 노트북 밖 파이썬 파일(`/tmp/ch31-04/exp/e1_scene.py` — 노트북 장면을 `asyncio.run`으로): 앞 작업자 5번 + 재개 2번, stdout sha256 앞 16자리 모두 `91c726007280fa11`, stderr 0바이트 — Before 빌려 간 1 → 다음 요청 `TimeoutError`(`timeout 0.20`) · After 0 → `ch31_lab` · 값 바꿔 보기 `timeout 1.00` · 정리 0·0.
- 모델 요청 0 · 실습 폴더 파일 17개(`app/`·`migrations/`·`alembic.ini`·README·잠금·맥 pyc) sha256 전후 같음 · 새로 생긴 파일 0(노트북 04 말고) · pyc 0 · `.failure.json` 0 · 서버에 남긴 것 0(이름 공간 `public`만·확장 `plpgsql`만) · 끝낸 뒤 postgres 프로세스 0·55431 포트 0.
- 게이트 G1~G7 0(`gates-wip-04.json`, 검사 문장 400) · `verify.py --chapter` PASS 5 sections / 103 code cells · 빌드 HTML `{{`·`[[` 0.

## 품질 개선 05절 (2026-09-29)

개선본 세부는 `qa/upgrade/05-diagnosis.md`에 있습니다. 데이터베이스는 01~04절과 같은 훅(`qa/upgrade/pre_exec.sh`, `/tmp/ch31-pg/data`, 교재와 같은 접속 글)으로 켰고, 이 절에서 훅에 pgenv `bin`(PostgreSQL 17.11 명령)을 PATH 끝에 더하는 한 줄을 넣었습니다(`8a9529f1…` → `dd564645…`). 노트북은 이름 공간 `ch31_shared`와 복원 데이터베이스 `ch31_restore`를 만들었다가 끝에서 지우고, 확장 `vector`는 `ch31_lab`에 남깁니다.

- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, `executed_at` 2026-09-29T19:32:40Z) · B(사본, `notebooks/` 커널, 19:32:50Z) — PASS 31셀, **셀별 출력 글자 31개 모두 같음**, `code_sha256` `62695363…` 같음, `outputs_sha256` A `8bac96cd…` ↔ B `930cc17a…`(설치 셀의 stdout 조각 나눔만 다름). 사본 시험(copy1)과 A는 `outputs_sha256`까지 같음. 모두 `OPENAI_API_KEY`를 지운 환경·`PYTHONDONTWRITEBYTECODE=1`. 모든 셀 stderr 0.
- 노트북 밖 파이썬 파일(`/tmp/ch31-05/exp/e3_scene.py` — 노트북과 같은 인자): 5번, 목차 원문 줄 뺀 stdout sha256 앞 16자리 모두 `a10ce6dbc04c5c4a`, stderr 0바이트 — 거리·계획 줄·표 다섯·`(3, 1, 3, 10)`·`{'value': 12}`·목차 `True`·`True`·`False`·실행 1 종료 코드 1·오류 다섯(모두 `ch31_shared.documents`)·실행 2 종료 코드 0·표 다섯·복원 DB `Index Scan`. `e1_scene.py`(`--no-owner` 판, 오류 넷) 5번 같음 · `e2_public.py`(따로 만든 DB에서 `search_path` 없이 `setup()` → 표 넷 모두 `public`, DB 지움).
- 모델 요청 0 · 실습 폴더 파일 17개(`app/`·`migrations/`·`alembic.ini`·README·잠금·맥 pyc) sha256 전후 같음 · 새로 생긴 파일 0(노트북 05 말고) · pyc 0 · `.failure.json` 0 · 끝의 서버 상태: 이름 공간 `public`만·확장 `plpgsql`·`vector 0.8.1`·데이터베이스 `ch31_lab`·`postgres` · 끝낸 뒤 postgres 프로세스 0·55431 포트 0 · 덤프 파일은 기기 셸 `TMPDIR`의 `ch31-05-*` 폴더(노트북이 지우지 않음).
- 게이트 G1~G7 0(`gates-wip-05.json`, 검사 문장 509) · `verify.py --chapter` PASS 5 sections / 127 code cells(max 14 lines) · 빌드 HTML `{{`·`[[` 0.

## 품질 개선 06절 (2026-09-29)

새로 만든 챕터 끝 실습 절입니다. 설계는 `qa/upgrade/06-design.md`(노트북 전), 세부는 `qa/upgrade/06-diagnosis.md`에 있습니다. 데이터베이스는 01~05절과 같은 훅(`qa/upgrade/pre_exec.sh` `dd564645…`, `/tmp/ch31-pg/data`, 교재와 같은 접속 글)으로 켰습니다. 노트북은 이름 공간 `ch31_practice`를 실행마다 지우고 다시 만들고, 끝에서 지웁니다(체크포인터 표 포함).

- 새 커널 두 번: A(`run_section.sh`, 프로젝트 맨 위 커널, `executed_at` 2026-09-29T20:10:04Z) · B(사본, `notebooks/` 커널, 20:10:13Z) — PASS 23셀, **셀별 출력 글자 23개 모두 같음**, `code_sha256` `bb245f74…` 같음, `outputs_sha256` `139e24d3…` 같음. 두 실행 모두 `OPENAI_API_KEY`를 지운 환경·`PYTHONDONTWRITEBYTECODE=1`. 모든 셀 stderr 0.
- 묶음 모양: 다시 만든 `part7-practice.zip`을 `/tmp/ch31-06/bundle`에 풀어 06 노트북을 묶음의 `notebooks/`에서, 키 없이 PASS 23셀 — 셀별 23개 A와 같음.
- 노트북 밖 파이썬 파일: 설계 확인 `/tmp/ch31-06/exp/e2_cells.py` 5번(stdout md5 `7cdaba069fc4d0d4`, stderr 0) · 저장 노트북 코드 셀을 이어 붙인 `e4_fromcells.py` 5번(md5 `ec8c15b435a66229`, A 출력과 글자까지 같음) · 반납 확인 `e3_leak.py` 2번(닫지 않은 연결 뒤 `TimeoutError` · CHECK 위반 뒤 빌려 간 연결 0).
- 모델 요청 0 · 실습 폴더 파일 17개 가운데 `README.md`만 바뀜(06 한 단락) — `app/`·`migrations/`·`alembic.ini`·잠금·맥 pyc 16개 sha256 전후 같음 · 새로 생긴 파일 0(노트북 06 말고) · pyc 0 · `.failure.json` 0 · 끝의 서버 상태: 이름 공간 `public`만·확장 `plpgsql`·`vector`(05가 남김)·데이터베이스 `ch31_lab`·`postgres` · 끝낸 뒤 postgres 프로세스 0·55431 포트 0.
- 게이트 G1~G7 0(`gates-wip-06.json`, 검사 문장 382 · 챕터 `gates-wip-ch31-after06.json` 6/6 PASS) · `verify.py --chapter` PASS 6 sections / 150 code cells(max 14 lines) · 빌드 HTML `{{`·`[[` 0.

## 마감 — 검토 반영과 챕터 마감 (2026-09-29)

- 검토 1차 A(01~03·공통 — 상 0·중 3·하 14)와 B(04~06 — 상 1·중 2·하 6)를 반영했습니다. 반영 25건, 미반영 1건(A-14 03 짧은 셀 열둘 — 강사 확인). 세부는 `qa/upgrade/chapter-summary.md` §21과 `handoff.md` 끝 절.
- **01만 다시 실행**(모델 없음 — 코드 주석 [11]·출력 라벨 `데이터베이스와 서버 버전:`): 새 커널 두 번(A 루트 커널 21:08:37Z · B `notebooks/` 커널 사본) 셀별 21개 가운데 19개 같음(다른 둘은 걸린 초 셀, A 0.48·0.19 · B 0.47·0.19), 두 비교 `True` 둘 다, 교재 값은 새 A 출력과 같음. 01 `code_sha256` `1566ad038be4…`·`outputs_sha256` `f8a551e4d649…`.
- 02~06 마크다운·`_src`·`.mmd`(03-2·03-3·06-3)만 고침 — 다섯 노트북 `code_sha256`·`outputs_sha256`·`executed_at` 전후 같음(05 `6269536315f3…`/`8bac96cd5e64…`).
- 여섯 생성기를 메모리에서 실행해 셀·`src_html()`이 노트북·`_src`와 글자까지 같음(45/51/67/47/65/49) · 인용 대조(숫자 없는 인용 포함) 출력 값 인용인데 출력에 없는 것 0.
- `upgrade_gates.py --label after` 6/6 PASS·G1~G7 0(문장 2,560) · `verify.py --chapter` PASS 6 sections / 150 code cells (max 14 lines) · `visual.cjs` 14행 PASS · 빌드 HTML `{{`·`[[` 0.
- 묶음: `part7-practice.zip` `6711c32a…`(114항목, Ch 31 17파일 = 디스크). `check_bundle_execution.py`는 실행기가 이 챕터 맥 `.venv`라 이 기기에서 돌 수 없어, 새 zip을 풀어 03·06을 키 없이·훅으로 DB를 켜고 손으로 실행(PASS 31셀·23셀, 저장 노트북과 셀별 출력 같음). `bundle-execution.json`은 옛 zip 기준 그대로.
- 노트북 밖 확인(검토 B-3): 확장을 이름 공간 안에 만들어 `--schema`로 덤프해도 확장 항목 0 · `--extension=vector`를 더하거나 DB 전체를 덤프하면 들어감 · `ch31_lab`의 `--schema=public`도 0(`.cache/ch31-close/exp/b3_ext.out`, 임시 DB `ch31_close_b3`만 쓰고 지움). 실습 폴더 사본에서 README 명령(`alembic upgrade head` → `python -m app.service` → `alembic downgrade base`)이 돌고 `[]`가 나옴, 프로젝트 맨 위에서는 `ModuleNotFoundError`.
- 모델 요청 0 · 삽화 생성 0 · 파일 삭제 0 · 옛 생성기 둘 `qa/upgrade/before/generators/blocked/`로 `mv -n` · 끝낸 뒤 postgres 프로세스 0·55431 포트 0.
