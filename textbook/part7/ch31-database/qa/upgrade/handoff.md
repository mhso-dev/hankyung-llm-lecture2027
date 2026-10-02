# Ch 31 DB & 상태 영속화 — 절 사이 인계 (handoff)

- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 30 `chapter-summary.md`(§18 「Ch 31이 이어받을 것과 전제하면 안 되는 것」) → 준비 조사 `qa/upgrade/chapter-lead-notes.md` → **이 파일** → 앞 절 `NN-diagnosis.md`·완료본(`_src`·노트북·생성기).
- **01절 완료 2026-09-29**(experiment, 게이트 37 → 0, 코드 셀 5 → 21, 검사 문장 387, **모델 요청 0**, 새 커널 두 번(A 루트 커널 15:54:38Z · B `notebooks/` 커널 15:54:53Z) 셀별 21개 가운데 19개 같음 — 다른 둘은 걸린 초 셀, 같은 커널 세 번·노트북 밖 여섯 번 모두 부등식 참, **`qa/upgrade/pre_exec.sh` 새로 만듦**(다섯 절 공통), 옛 생성기 둘 막음, Mermaid 4 + 삽화 1(재생성 1회·4크레딧)). 세부 값은 `01-diagnosis.md`.
- **02절 완료 2026-09-29**(paired, 게이트 32 → 0, 코드 셀 5 → 23, 검사 문장 376, **모델 요청 0**, Before = 블록 둘로 따로 확정한 이체가 CHECK 위반 `23514`로 막힌 뒤 `[(1, 500), (2, 1100)]` 합계 1600(빨강) ↔ After = 한 블록 → 같은 오류 뒤 `[(1, 500), (2, 500)]` 합계 1000, 새 커널 두 번(A 루트 커널 16:31:16Z · B `notebooks/` 커널) **셀별 23개 모두 같음**, 노트북 밖 다섯 번 같음, 도구 파일 없음, 실습 폴더 파일 고침 0, Mermaid 4 + 삽화 1(재생성 1회·4크레딧)). 세부 값은 `02-diagnosis.md`. **02 시작 전 기기 VM이 또 재시작**(uptime 8분, `/tmp` 빔) — Mermaid 도구 `/tmp/mmd`·`/tmp/libs`·`/tmp/pptr-cache`를 02가 다시 설치함(루트 여유 3.6G → 2.0G). 02 검사 도구는 연결 폴더 **`.cache/ch31-02/tools/`**(`ban32.py`·`twoword.py`·`srcdump.py` + 01 도구 사본).
- **03절 완료 2026-09-29**(paired, 게이트 35 → 0, 코드 셀 6 → 31, 검사 문장 457, **모델 요청 0**, Before = 줄 셋이 든 표에 기본값 없는 NOT NULL 칸 `owner`를 더하는 판 `20260929_02` → `IntegrityError`(`NotNullViolation`·`23502`) 뒤 `판 번호: 20260911_01`·`칸: ['id', 'question']` 그대로(빨강) ↔ After = 같은 파일에 `server_default="미정"`만 → `20260929_02`·세 줄 `'미정'` · 판 내리기(`-1`) 뒤 다시 올리면 1번 줄 `'민지'` → `'미정'` · 값 바꿔 보기 `nullable=True` → `None` 셋, 새 커널 두 번(A 루트 커널 17:09:43Z · B `notebooks/` 커널) **셀별 31개 모두 같음**, **묶음을 푼 `notebooks/`에서 키 없이 31개 같음**, 노트북 밖 다섯 번 같음, 실습 폴더 파일 고침 0(17개 해시 같음), 도구 파일 없음, Mermaid 5 + 삽화 1(재생성 1회·4크레딧)). 세부 값은 `03-diagnosis.md`. 03 검사 도구는 연결 폴더 **`.cache/ch31-03/tools/`**(`ban33.py`·`twoword33.py`·`dump3.py` + 01·02 도구 사본)·확인 스크립트 `.cache/ch31-03/exp/`(`e1_scene.py`·`e3_empty.py`·**`e4_pool.py` — 04 인계 확인**).
- **04절 완료 2026-09-29**(paired, **재개 작업** — 앞 작업자가 설계·노트북 밖 확인 뒤 기기 연결이 끊겨 멈춘 자리부터, 게이트 26 → 0, 코드 셀 4 → 21, 검사 문장 400, **모델 요청 0**, Before = 풀 크기 1·더 만들 0·대기 제한 0.2초 엔진에서 `conn = await engine.connect()`로 빌리고 닫지 않음 → `빌려 간 연결 수: 1`·`풀에 쉬고 있는 연결 수: 0` → 같은 다음 요청 셀이 `sqlalchemy.exc.TimeoutError`(`… timeout 0.20`)로 연결을 받지 못함(빨강) ↔ After = `await conn.close()` → 0·1 → 같은 조회를 `async with`로 → 0·1 → 같은 다음 요청 셀이 `받은 데이터베이스 이름: ch31_lab` · 값 바꿔 보기 대기 제한 1.0초 → 다시 닫지 않으면 `timeout 1.00` · 이름 가르기 `파이썬의 TimeoutError를 이어받는가: False`, 새 커널 두 번(A 루트 커널 18:54:00Z · B `notebooks/` 커널 18:54:09Z) **셀별 21개 모두 같음·`outputs_sha256`도 같음**, 노트북 밖 5+2번 같음, 표·이름 공간 만들지 않음(서버에 남긴 것 0), 실습 폴더 파일 고침 0, 도구 파일 없음, Mermaid 4 + 삽화 1(재생성 0회·2크레딧)). 세부 값은 `04-diagnosis.md`. 04 검사 도구는 기기 **`/tmp/ch31-04/tools/`**(03 도구 사본)·생성기 조각·치환 도구 `/tmp/ch31-04/gen/edit.py` — `/tmp`가 비면 `.cache/ch31-03/tools/`에서 다시 복사. 재개 자료·노트북 밖 확인은 연결 폴더 **`.cache/ch31-04/resume/`·`.cache/ch31-04/exp/`**.
- **05절 완료 2026-09-29**(experiment, 게이트 45 → 0, 코드 셀 7 → 31, 검사 문장 509, **모델 요청 0**, 가설 = 이름 공간 하나만 덤프하면 public의 확장 vector가 파일에 없어 확장 없는 새 DB에서는 문서 표만 빠진다 → 실행 1(확장 만들기 `False`) = `pg_restore 종료 코드: 1`·`type "public.vector" does not exist`·`errors ignored on restore: 5`·표 넷(문서 표 없음)·`{'value': 12}` ↔ 실행 2(**바꾼 값 하나 — 복원 전에 `CREATE EXTENSION vector`**) = `0`·표 다섯(`'documents': 3`)·`{'value': 12}` · 복원 DB `enable_seqscan` off 계획 `Index Scan using documents_embedding_hnsw on documents`, 체크포인터 표는 `SET search_path TO ch31_shared`로 문서 표와 같은 이름 공간(Ch 23 02 모양), 새 커널 두 번(A 루트 커널 19:32:40Z · B `notebooks/` 커널 19:32:50Z) **셀별 31개 모두 같음**(`outputs_sha256`은 설치 셀 조각 나눔만 다름), 노트북 밖 5번 같음, **훅 `pre_exec.sh` 고침 `8a9529f1…` → `dd564645…`(pgenv `bin`을 PATH **끝**에 — `pg_dump`·`pg_restore` 17.11)**, 실습 폴더 파일 고침 0, 도구 파일 없음, Mermaid 4 + 삽화 1(재생성 0회·2크레딧)). 세부 값은 `05-diagnosis.md`. 05 검사 도구는 기기 **`/tmp/ch31-05/tools/`**(04 도구 사본 + `edit.py`)·확인 스크립트 `/tmp/ch31-05/exp/` — 연결 폴더 사본 **`.cache/ch31-05/exp/`**(`e1_scene.py`·`e2_public.py`·`e3_scene.py`)·**`.cache/ch31-05/tools/edit.py`**.
- **06절(실습 절) 완료 2026-09-29**(새 절 `06-DB와-상태-영속화-실습`, experiment, 게이트 G1~G7 0 · 챕터 6/6 PASS, 코드 셀 23, 검사 문장 382, **모델 요청 0**, 붙인 기능 02 한 묶음 작업 · 04 작은 연결 풀과 반납 · 05 체크포인터 → 상담 예약 그래프 하나, 실행 1 처음 상담 시간 50분 = `[1, 1, 1]`·남은 0·예약 `[1, 2, 3]` ↔ 실행 2(**바꾼 값 하나 — 30분**) = `문의 2 받은 오류: IntegrityError 23514`·`[1, 0, 1]`·남은 10·예약 `[1, 3]` · 두 실행 모두 체크포인트 줄 9·빌려 간 연결 0 · 배송 상태 `booked` 1 ↔ 0 · 새 연결로도 `{'no': 2, 'minutes': 30, 'booked': 0}`, 새 커널 두 번(A 루트 커널 20:10:04Z · B `notebooks/` 커널 20:10:13Z) **셀별 23개 모두 같음·`outputs_sha256`도 같음**, 묶음을 풀어 23개 같음, 노트북 밖 5+5번 같음, 도구 파일 없음, 실습 폴더 파일 고침은 README 한 단락뿐, **05 노트북 다시 실행하지 않음(`code_sha256`·`outputs_sha256` 그대로 — b8·정리 끝만 `mdpatch.py`)**, Mermaid 3 + 삽화 1(재생성 0회·2크레딧)). 세부 값은 `06-diagnosis.md`·설계 `06-design.md`·아래 「실습 → 챕터 검토」. 06 검사 도구는 기기 `/tmp/ch31-06/tools/`(05 도구 사본 + **`astdiff.py` — 01~05 노트북과 AST 대조**) — 연결 폴더 사본 **`.cache/ch31-06/tools/`·`.cache/ch31-06/exp/`**.
- **챕터 마감 끝남 2026-09-29**(검토 1차 26건 가운데 25건 반영 · **01만 다시 실행**(모델 없음 — 코드 주석 [11]·출력 라벨 「버전」, 두 커널 초 셀 둘 말고 같음·교재 값 그대로) · 02~06 코드·출력 해시 같음 · 게이트 6/6·G1~G7 0 · `verify.py` PASS 6/150 · `visual.cjs` 14행 PASS · README 전체·`objectives` 여섯 · `part7-practice.zip` `6711c32a…` · 묶음 실행 검사는 손 대조(03·06) · 옛 생성기 둘 옮김 · 모델 요청 0). 세부는 맨 아래 「검토 반영과 챕터 마감」과 `chapter-summary.md`.

- **기기 VM 재시작(2026-09-29 16:07Z 안팎, 01 작업 끝 무렵)**: `/tmp` 전체가 비었음 — **Mermaid 렌더 도구 `/tmp/mmd`·`/tmp/libs`·`/tmp/pptr-cache`를 `textbook/_notebook/mermaid/README.md`대로 다시 설치해야 `run_section.sh`의 렌더 단계가 돎**(AGENT-BRIEF 「기기 VM이 다시 만들어지면」). `uv` 캐시 `/tmp/uv-cache`는 저절로 다시 생김. 챕터 클러스터 `/tmp/ch31-pg`는 `pre_exec.sh`가 `initdb`부터 다시 만듦(재시작 뒤 확인). 01의 검사 도구는 연결 폴더 **`.cache/ch31-01/tools/`**(`ban31.py`·`extra_check.py`·`pregate.py`·`cmpout.py`·`quotes.py`·`dump.py`·`runcopy.sh`)에 있음.

## 챕터 공통 (01절에서 정한 것)

### 챕터 리드 결정 (그대로 이어 지키세요)

1. **DB 준비 — Ch 12·23 선례를 잇습니다.**
   - **학생**: 챕터 전용 Docker 컨테이너 하나를 다섯 절이 함께 씀. 01 노트북 제목 셀 준비물의 명령(글자 그대로 이어 쓰기):
     ```bash
     docker run --name kdt-ch31-postgres \
       -e POSTGRES_USER=postgres \
       -e POSTGRES_PASSWORD=postgres \
       -e POSTGRES_DB=ch31_lab \
       -p 127.0.0.1:55431:5432 \
       -d pgvector/pgvector:0.8.1-pg17
     ```
     꺼져 있으면 `docker start kdt-ch31-postgres`. 비밀번호 `postgres`는 연습용 값이라고 밝힘. 줄 `-p 127.0.0.1:55431:5432`는 「이 컴퓨터 안에서만 서버에 붙을 수 있게 묶는 설정」(Docker 문서 — 기본은 바깥에서도 붙음). 옛 README `-p 55431:5432`는 모든 주소에 열림 — **README 다시 쓰기는 마감 몫**.
   - **작업 기기**: `qa/upgrade/pre_exec.sh`(`8a9529f101ef38bdbf57ae31118c70fd53736df65ca884038fe1096aae009b9e`, 01이 만듦 — **다섯 절 모두 이 훅**, `N` 조건 없음). `run_section.sh` 32행이 절 실행 직전에 source(`--no-exec`에도). 요지: `.cache/vm/pgenv/bin`(PostgreSQL 17.11 + pgvector 0.8.1)으로 **`/tmp/ch31-pg/data`**(연결 폴더 밖, 46MB)에 클러스터 — 없을 때만 `initdb -U postgres`(연습용 비밀번호, scram-sha-256, UTF8, locale C)·`createdb ch31_lab` · `127.0.0.1:55431`만 받음(소켓 `/tmp/ch31-pg`) · 켜진 뒤 학생 글과 같은 TCP 접속 글로 `SELECT 1`까지 기다림 · **부른 셸이 끝날 때 `trap EXIT`로 `pg_ctl -m fast -w stop`**. 두 번 불러도 안전(이미 켜져 있으면 그대로 씀, 다른 서버가 55431을 받으면 `return 1`). **기기 셸은 호출이 끝나면 postgres도 끝남(bwrap `--die-with-parent`)** — trap 없이 끝나면 잠금 파일 둘이 남고, 다음 호출이 PID를 1부터 다시 써 그 PID를 다른 프로세스가 쓰면 켜지지 않음 → 훅이 PID 프로세스 이름이 `postgres`가 아닌 잠금 파일을 **지우지 않고 이름만 바꿈**(`….stale-<초>`). 셸 호출 하나 180초 제한에 걸려 trap이 못 돌아도 다음 호출은 켜짐(두 경우 재현). **끝낸 뒤 확인**: `ps -eo comm | grep -c '^postgres$'` → 0 · `ss -ltn | grep -c 55431` → 0. 데이터는 호출 사이에 남으므로 **절마다 제 이름 공간을 처음에 지우고 다시 만들 것**. 사본 실행은 `.cache/ch31-01/tools/runcopy.sh <사본> <커널 작업 폴더>`(훅 source + `execute.py --cwd`) 모양을 쓰면 편함.
   - **교재 본문 판 가름**(01 글, Ch 12·23 모양): 「교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다. 그 서버는 Docker 컨테이너가 아니라, 같은 접속 글로 켠 서버입니다. Docker 이미지로 켜면 서버 판 번호의 끝자리가 다를 수 있습니다.」 · pgvector를 쓰는 05는 「확장 판 0.8.1(교재 출력)·이미지 태그 0.8.1」과 공식 문서 판을 가름.
   - **pgembed·SQLite 대체는 쓰지 않음**(까닭은 준비 노트 §4·§10-1) — 강사 확인 대상에 한 줄(01 진단에 있음).
2. **접속 글 자리**: 노트북은 `.env`를 읽지 않음(옛 README 문장은 거짓 — 마감이 고침). 접속 글은 준비 셀 뒤 **설정 셀에 연습용 값으로 한 번**. 01 설정 셀(`author_01.SETTINGS`)의 글을 **문자열 대조로 이어 쓰기**:
   ```python
   # 데이터베이스 접속 글을 정합니다(비밀번호 postgres는 이 실습에서만 쓰는 연습용 값입니다)
   database_url = "postgresql+asyncpg://postgres:postgres@127.0.0.1:55431/ch31_lab"
   # 비밀번호가 찍히지 않게, 글을 @에서 나눠 앞의 드라이버 부분과 뒤의 서버 부분만 출력합니다
   url_parts = database_url.split("@")
   print("드라이버 부분:", database_url.split("://")[0])
   print("서버 주소와 데이터베이스:", url_parts[1])
   ```
   - 글자 그대로: **`postgresql+asyncpg://postgres:postgres@127.0.0.1:55431/ch31_lab`**(비동기 — 01·02·04). 동기 드라이버가 필요한 절(03 Alembic 자식 프로세스·05 `PostgresSaver`·`psycopg`)은 같은 서버의 **`postgresql+psycopg://postgres:postgres@127.0.0.1:55431/ch31_lab`**(SQLAlchemy psycopg) · **`postgresql://postgres:postgres@127.0.0.1:55431/ch31_lab`**(psycopg·`PostgresSaver` 그대로) — 그 절이 첫 자리에서 드라이버 부분만 다르다는 한 문장. 옛 노트북의 `replace`로 셋을 만드는 모양은 쓰지 않음(01은 하나만).
   - `localhost`가 아니라 `127.0.0.1`(Docker 명령을 127.0.0.1에만 묶었기 때문). **주의**: 실습 폴더 `migrations/env.py`(03이 부름)·`app/db.py`의 기본 접속 글은 아직 `localhost`이고 환경 변수 `CH31_SYNC_URL`·`CH31_DATABASE_URL`을 읽음 — 03이 Alembic에 접속 글을 넘길 방법(파이썬 API `Config.set_main_option` 또는 자식 프로세스 환경 변수)을 정하고, 앱 파일을 고칠지는 03·마감이 판단.
   - 비밀번호가 든 글은 출력하지 않기(01은 드라이버 부분과 `@` 뒤만).
3. **모델 M0**: 01~06 모두 모델 요청 0(키 셀 없음 — 준비 노트 §9). 가짜 채팅 모델·정해 둔 답 클래스 금지(규격 §3) — 05의 그래프는 「모델을 쓰지 않는 그래프」로 공개(Ch 20 03·Ch 23·24 선례). 06 실습 절 요청 0은 강사 확인 대상.
4. **걸린 시간(01 끝남)**: 결론은 부등식과 매번 같은 값만, 초는 결과 읽기 둘째 단락·b6 표·「확인할 점」·b7에만(Ch 25 03 선례). 시간 `assert` 0. 04에서 기다린 초를 출력한다면 같은 규칙(04는 결정적 장면 권장 — 아래 paired).
5. **paired 설계**: 아래 「paired 설계」 표.
6. **문법 범위**: 아래 「문법 범위」.
7. **용어**: 아래 「용어 표」·「금지어·대체어」. 다섯 절 b3·b10을 절마다 새로.
8. **도구 파일 — 만들지 않음(S1, 01 결정)**: 01이 만든 함수는 `read_question(item_id, wait_seconds)` 하나이고, 전역 `engine`·`read_sql`·`step_log`에 기대는 실험용이라 뒤 절이 그대로 쓸 일이 없음. 둘 이상의 절이 같은 평범한 함수를 실제로 쓰게 되면 그 절이 `notebooks/db_tools.py`(이름 겹침 확인 — 과정의 `*_tools.py`와 안 겹침, `data_tools.py`는 Ch 4)를 첫 판으로 만들고 첫 판부터 생성기 대조 사슬(Ch 30 04 본: `TOOLS_HEAD`·`TOOLS`·`check_tools`·`strip_later_imports`·쓰기 가드·`--tools-copy`) · 공개 목록 두 곳에 줄 · 03은 묶음 실행 검사 절이라 도구 파일을 가져오지 않는 편이 안전(Ch 28 01 선례).
9. **옛 생성기(01 끝남)**: `qa/author_ch31.py`(`1755fcec…` → `79bf670c…`)·`figures/_gen_figures.py`(`dc2d8216…` → `34448715…`) 맨 위(`from __future__` 줄 뒤)에 설명 주석 셋 + `raise SystemExit(…)`. **실행하지 말 것**(둘 다 안내 글 + 종료 코드 1). 챕터·실습 폴더에 `_generate.py` 없음. `.moai` part7 셋은 Ch 30 01이 막은 판 그대로. 옮기기(`mv -n` → `before/generators/blocked/`)는 마감 — Part 7 `check_figures.py` 20행이 `_gen_figures.py`를 봄.
10. **파일 위치 셀**: 01은 실습 폴더 파일을 읽지 않아 넣지 않음. **03은 `alembic.ini`·`migrations/`를 읽으므로 필요** — Ch 30 과정 표준 모양(후보 `".."`·`"."`·`"labs/part7/ch31-database"`, 찾을 파일 `"/alembic.ini"`, 고른 후보는 출력하지 않음, `assert` 한 줄). 루트 커널(`run_section.sh`)·`notebooks/`·묶음을 푼 `notebooks/` 세 자리에서 확인.
11. **슬러그 고정**: 01(Ch 30 10 b8·Ch 30 `author_09.py` `L_CH31_01`·Part 7 목차가 링크 — 01은 그대로). **05의 체크포인터 저장 유지**(Ch 30 10 b8 「Ch 31 05절은 체크포인터로 그래프의 실행 상태를 PostgreSQL 표에 저장합니다」). 06 실습 절 슬러그 후보(`06-DB-실습` 등)는 마감·실습 작업자 몫.
12. **비유 계열 「전화 교환대」(01이 엶)**: 아래 「비유 계열」.
13. **준비 셀은 과정 표준**: 설치 `%pip`은 그 절이 쓰는 패키지만·잠금 판 번호까지(`install_source` — 01 = `sqlalchemy[asyncio]==2.0.43`·`asyncpg==0.30.0`, 출력 줄 `sqlalchemy: 2.0.43`·`asyncpg: 0.30.0`) → 가져오기(준비 셀) → 설정 셀(접속 글) · 키 셀 없음. 잠금의 dev `pip==25.2`(과정 `26.2`와 다름)는 `%pip` 셀을 바꾸지 않았으므로 01은 건드리지 않음 — 마감 판단.
14. **실행 규칙(01이 씀)**: `env -u OPENAI_API_KEY PYTHONDONTWRITEBYTECODE=1 timeout 170 bash textbook/_notebook/upgrade/run_section.sh textbook/part7/ch31-database NN` · **첫 실행 전 `/tmp` 사본에서 `execute.py`로 한 번**(실패하면 `.failure.json`이 실습 폴더에 남음) · 그림 파일 없이 첫 `run_section.sh`를 부르면 `attach_figures.py`에서 멈춤(실행·저장은 끝난 뒤) → **B를 그림 전에** · A = 루트 커널, B = 사본을 `--cwd labs/part7/ch31-database/notebooks`(학생 자리) · 셀별 출력 대조(`.cache/ch31-01/tools/cmpout.py`) · 결과 읽기의 흔들리는 값은 `[[…]]` 자리 → A 출력으로 `mdpatch.py`(재실행 없이) · Alembic 자식 프로세스(03)는 `PYTHONDONTWRITEBYTECODE=1`을 넘겨 `migrations/`에 pyc를 남기지 않기.

### 문법 범위 (Ch 28·30 이음 + 이 챕터에서 늘어난 것 — 01 AST 확인, 호출 깊이 최대 2)

| 문법·API | 처음 풀이한 절 | 조건 |
|---|---|---|
| 셀 맨 위 `await`·`async with` | Ch 28·30(이어 씀) — 01 2절 결과 읽기 「Ch 28·30처럼 노트북 도구(IPython)의 기능」 | `asyncio.run` 셀에서 안 씀 |
| `async def` | Ch 2 12 · 01 `read_question`(셀당 정의 하나, 본문 8줄 이하 — 01은 7줄) | 매개변수·반환 힌트 없음 |
| `asyncio.gather` | Ch 2 12(이어 씀) — 01 7절: 코루틴을 변수 셋에 만든 뒤 **인자로 하나씩 적어** 넣음(별표 풀기·제너레이터 식 없음) | 받은 목록은 넣은 차례 |
| `create_async_engine(url, pool_size=3, max_overflow=0)`·`engine.pool.size()`·`checkedin()`·`checkedout()`·`await engine.dispose()` | **01** | 04가 `pool_timeout`·`pool.status()`를 더하면 첫 풀이 |
| `async with engine.connect() as conn:`·`await conn.execute(text(…))`·`fetchone`·`fetchall`·`scalar_one`·`rowcount` | **01** | `execute(text("…"))` 깊이 2까지 |
| `async with engine.begin() as conn:` | **01**(「블록 안의 SQL 글을 한 묶음으로 실행하고, 오류 없이 끝나면 확정 — Ch 4 03 커밋과 같은 일, 오류 모양은 02절」) | **02가 오류 난 블록(확정하지 않음)을 처음 보임** |
| `text("… :id …")` + 딕셔너리로 값 넘기기 | **01**(Ch 4 03 물음표 자리 이음) | SQL 글을 `+`로 이어 붙여 값을 넣지 않기 |
| SQL 글 | 문자열(코드 셀 줄 수에 셈) · 긴 글은 변수로(01 `table_sql`·`insert_sql`) · 01이 쓴 SQL: `DROP SCHEMA IF EXISTS … CASCADE`·`CREATE SCHEMA`·`CREATE TABLE`·`INSERT INTO … VALUES`·`SELECT … ORDER BY`·`pg_sleep`·`current_database()`·`current_setting('server_version')`·`to_regnamespace` | 새 SQL 낱말(`UPDATE`·`CHECK`·`EXPLAIN`·`CREATE EXTENSION`·`to_regclass` 등)은 처음 쓰는 자리에서 한 문장(`UPDATE`는 과정 요약 §2-1 「처음 쓰면 한 문장」) |
| `time.perf_counter()`·`round(…, 2)` | Ch 2 12(이어 씀) — 01만 | 초에 `assert` 금지 |
| `asyncio.create_task` | **쓰는 절이 첫 풀이**(Ch 2 12 전제 금지 목록 — 04가 쓰면 한 문장) | — |
| ORM(`DeclarativeBase`·`Mapped[...]`·`mapped_column`)·`AsyncSession`·`async_sessionmaker` | **01은 쓰지 않음**(Core `text()`로 충분) | 뒤 절이 꼭 가르쳐야 하면: ORM 클래스는 Ch 30 앱 파일 예외와 같은 성격으로 **클래스 하나·힌트는 `Mapped[...]`만** + 「힌트가 칸의 자료형을 정한다」 까닭 한 문장 · `AsyncSession`은 「세션」 말 없이 코드 이름 그대로(`AsyncSession` 객체), 「작업마다 따로 — SQLAlchemy 문서」 |
| 앱 파일(`app/`·`migrations/env.py`) | 노트북이 열지 않으면 고치지 않음(README 명령에서만 — 마감) · 03이 `migrations/`를 읽으면 그때 03이 판단(Ch 28 A-17 「학생이 여는 서버 파일도 금지 문법 0」 선례) | `env.py` 35행 조건 표현식·반환 힌트·`from __future__` |

- **쓰지 않은 것(01 0건)**: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·변수·반환 힌트·대입 풀기·별표 풀기·`while`·`try`·세미콜론·`isinstance`·클래스·데코레이터·`os.environ`·`create_task`·가짜 모델.
- 셀 모양: 준비 셀 밖 셀 10줄 이하(01 최대 9) · 첫 줄 주석이 그 셀이 하는 일 · 정의 셀 결과 읽기 「정의 셀이라 출력이 없습니다」 · 여러 줄 출력은 라벨 줄 따로 · 코드 셀 20~32(01 21) · 저장 출력에 Traceback·임시 파일 위치·실행마다 다른 ID·시각 없음 · 받은 오류를 출력할 때 `type(error).__name__`·SQLSTATE처럼 매번 같은 것만(오류 글에 서버 주소·PID가 들면 뺄 것).

### 용어 표 (01에서 정함 — 02~06은 그대로 이어 씀)

| 말 | 뜻 | 코드에서 | 첫 자리 |
|---|---|---|---|
| **비동기 엔진**(`AsyncEngine`) | 데이터베이스에 붙는 방법과 연결 풀을 함께 관리하는 객체. 만들 때는 서버에 붙지 않음(차단기·스위치 예) | `create_async_engine(database_url, pool_size=3, max_overflow=0)` | 01 |
| **드라이버**(driver) | 파이썬과 데이터베이스 서버 사이에서 말을 주고받는 패키지(통역사 예). 접속 글의 `+asyncpg` | asyncpg(비동기) · 03·05의 psycopg는 동기 드라이버 — 그 절이 한 문장 | 01 |
| **연결**(connection) | 엔진이 서버와 열어 둔 통로 하나, SQL 글을 보내고 답을 받는 자리(전화 예). Ch 28 「세션 → 연결」 대체어와 같은 글자이고 이 챕터에서는 **데이터베이스 연결만** | `async with engine.connect() as conn:`의 `conn`(`AsyncConnection`) | 01 |
| **연결 풀**(connection pool) | 한 번 연 연결을 서버와 끊지 않고 모아 두었다가 다시 빌려 주는 곳(공용 자전거 거치대 예). 쉬고 있는 연결·빌려 간 연결 | `pool_size`·`max_overflow`·`checkedin()`·`checkedout()` · 04 제목 「커넥션 풀」은 제목에만(강사 확인) | 01 |
| **SQL 글 객체**(`text()`) | SQL 글 하나를 연결로 보낼 수 있게 감싼 객체. 글 속 `:id`는 값 자리(풀이만 — Ch 4 03 물음표 자리 이음) | `read_sql = text("… WHERE id = :id")` → `TextClause` | 01 |
| (이어 씀) **이름 공간**(SQL `SCHEMA`) | Ch 23 02 말 — 한 데이터베이스 안에서 표들을 이름으로 묶어 두는 자리. 절마다 제 이름 공간(01 `ch31_async`·02 `ch31_tx`·03 `ch31_migration`·05 `ch31_shared` — 옛 원고 이름 유지 권장) | `DROP SCHEMA IF EXISTS … CASCADE`·`CREATE SCHEMA` | Ch 23 02 |
| (이어 씀) **커밋**(commit) = **확정** | Ch 4 03 말 — 바꾼 내용을 데이터베이스에 확정하는 일(Git 커밋과 이름만 같음). 01은 `engine.begin()` 블록 끝의 확정으로 이음 | `engine.begin()` | Ch 4 03 |
| (이어 씀) 코루틴·`gather()`·이벤트 루프 | Ch 2 12 말 | 01 7절 | Ch 2 12 |
| (풀이만) 기록 목록 `step_log`·쉬고 있는 연결·빌려 간 연결·걸린 시간 | 01 노트북 안에서만 | — | 01 |
| **한 묶음 작업**(트랜잭션, transaction) — 02가 정함 | 여러 SQL 글을 한 묶음으로 실행하고, 끝에서 한꺼번에 확정하는 작업(장바구니 한꺼번에 계산 예). 절 제목 「트랜잭션」은 제목에만, 본문은 첫 자리 괄호 원어 뒤 「한 묶음 작업」 | 블록 `async with engine.begin() as conn:` 하나 | 02 |
| **원자성**(atomicity) — 02 제목 말 | 한 묶음 작업 안의 변경이 모두 확정되거나 모두 없던 일이 되는 성질(두 사람 서명 계약서 예) | 02 After — 빼기가 막히자 더하기도 남지 않음 | 02 |
| **취소**(롤백, rollback) — 02가 정함 | 블록 안에서 오류가 나면 확정하지 않고 블록 안의 변경을 모두 없던 일로 하는 것(볼펜으로 옮겨 적기 전 지우개 예). **03 제목의 롤백(판 내리기)과 다른 뜻** — 02가 「03절 제목의 롤백은 표 구조의 판을 내리는 일이라, 이 절의 취소와 뜻이 다릅니다」를 씀 | 02 블록 안 2번 잔액 1100 → 밖 500 | 02 |
| (이어 씀) **확정**(커밋) | Ch 4 03 커밋 = 01 「확정」. 02는 「확정(커밋)」으로 한 번 괄호 원어 | `engine.begin()` 블록 끝 | Ch 4 03·01·02 |
| (풀이만) CHECK 제약 · 오류 코드 SQLSTATE · `IntegrityError` · `error.orig` | CHECK 제약 = 칸 값이 적어 둔 식을 만족해야 한다는 조건(Ch 4 03 「제약(constraint)」 이음) · SQLSTATE = 서버가 오류마다 붙이는 다섯 글자 코드(앞 두 글자 갈래, 23 = 제약 위반, `23514` CHECK 위반) · `IntegrityError` = Ch 4 03 `sqlite3.IntegrityError`와 같은 이름(패키지 sqlalchemy의 모듈 `exc`) · `error.orig` = SQLAlchemy asyncpg 방언이 드라이버 오류를 DB-API 모양으로 바꾼 오류(`sqlstate` 속성 · 글 첫머리에 드라이버 오류 이름 `CheckViolationError`, 드라이버 오류 자체는 `__cause__` — 설치판 `dialects/postgresql/asyncpg.py` 776~791행, 마감 검토 A-6) | `except IntegrityError as error:` · `error.orig.sqlstate` · `print(error.orig)` | 02 |
| **표 구조 바꾸기**(마이그레이션, migration) — 03이 정함 | 데이터베이스 표에 칸을 더하거나 빼는 것처럼 표의 모양을 바꾸는 일(학급 출석부에 연락처 칸 긋기 예). 본문은 첫 자리 괄호 원어 뒤 「표 구조 바꾸기」 · **Ch 21 04 「옮기기(마이그레이션)」(옛 버전 라이브러리 코드를 새 버전에 맞춰 고치는 일)와 다른 뜻** — 03 노트북 2절·b3에 문장 | 판 `20260929_02`의 `op.add_column` | 03 |
| **판**(리비전, revision) — 03이 정함 | 표 구조 바꾸기 한 번을 적은 파일 하나와 그 판 번호(책의 개정판 예). 앞 판 번호(`down_revision`)로 이어진 줄 = 「판 사슬」(풀이만). **챕터 전체에서 「판」은 표 구조의 판(리비전)에만 쓰고, 패키지·서버 번호는 「버전」**(마감 검토 A-15 — 01·02의 「판은 sqlalchemy …」·「서버 판 번호」를 「버전」으로 고침, 01 출력 라벨 `데이터베이스와 서버 버전:`은 01 재실행으로) · 교환대 비유의 「판」(나무 판·금속 판)과 02의 「Before 판·After 판」(두 가지 코드)은 그대로 | `revision = "20260929_02"`·`down_revision = "20260911_01"` | 03 |
| **판 올리기**(upgrade)·**판 내리기**(downgrade) — 03이 정함 | 판 파일의 함수 `upgrade`·`downgrade`를 불러 다음 판·앞 판으로 가는 일(계단 예). **03 제목의 「롤백」 = 판 내리기**, 02 「취소(롤백)」와 다른 뜻(03 노트북 1·8절·b2·b4 소제목·복습 5) | `command.upgrade(alembic_cfg, "head")`·`command.downgrade(alembic_cfg, "-1")` | 03 |
| (풀이만) 판 기록 표 · NOT NULL 제약 · 서버 기본값 · 환경 변수(`os.environ`) · 진행 기록 | 판 기록 표 = Alembic이 지금 판 번호 한 줄을 적는 표 `alembic_version`(Ch 23 02 「표 만들기 기록」 판 번호와 같은 생각) · NOT NULL 제약 = 칸이 빈 값(`NULL`)을 가질 수 없다는 조건(Ch 4 03 제약 이음, SQLSTATE `23502`) · 서버 기본값 = `server_default` — 새 칸을 더할 때 이미 있는 줄에도 들어감 · 환경 변수 = Ch 28 03 말, 파이썬 `os.environ`(처음 쓰면 한 문장 — 03이 씀) · 진행 기록 = Alembic이 stderr로 찍는 `INFO  [alembic.runtime.migration] …` 줄(「로그」 금지어 대신) | `os.environ["CH31_SYNC_URL"] = database_url` · `Will assume transactional DDL.` | 03 |
| **대기 제한**(`pool_timeout`) — 04가 정함 | 풀에 빌려 줄 연결이 없을 때 새 요청이 반납을 기다리는 초의 한도(공용 자전거 거치대에서 반납을 기다리다 정한 시간이 지나면 그만두기 예 — 01 연결 풀 비유 이음). 오류 글 끝에 `timeout 0.20`으로 찍힘 | `create_async_engine(…, pool_timeout=0.2)` · `engine.pool.timeout()` → `0.2` | 04 |
| **반납** — 04가 정함 | 빌린 연결을 닫아 풀에 다시 넣는 일(01 「풀에 다시 넣음」에 붙인 이름, 「반환」 금지 · 거치대에 자전거 다시 세우기 예). 반납 누락 = 「닫지 않고 둔 연결」 | `await conn.close()` · `async with engine.connect()` 블록 끝(설치판 `ext/asyncio/engine.py` 894~896행 `__aexit__` → `close()`) | 04 |
| **이름 가림** — 04가 정함 | 같은 이름을 새로 가져오거나 만들어, 앞의 같은 이름을 쓸 수 없게 되는 일(게시판에 같은 제목의 새 공지를 겹쳐 붙이기 예) | `from sqlalchemy.exc import TimeoutError` 쓰지 않음 → `import sqlalchemy.exc` · `except sqlalchemy.exc.TimeoutError as error:` | 04 |
| (제목 말) 커넥션 풀·고갈 — 04 | 제목에만. 본문 첫 자리(노트북 1절·b2) 「절 제목의 커넥션 풀(connection pool)은 01절에서 본 연결 풀입니다. 제목의 고갈은 풀에 빌려 줄 연결이 하나도 남지 않은 상태를 말합니다. 이 교재 본문에서는 「빌려 줄 연결이 없다」고 적습니다」 | — | 04 |
| (풀이만) 풀 상태 글 · `__module__` · `issubclass` — 04 | `engine.pool.status()` = 풀 크기·쉬고 있는 연결·더 만든 연결·빌려 간 연결 수를 적은 한 줄 글(`Pool size: 1  Connections in pool: 1 Current Overflow: 0 Current Checked out connections: 0`) · 속성 `__module__` = 종류가 정의된 모듈 이름 · 함수 `issubclass(앞, 뒤)` = 앞 종류가 뒤 종류를 이어받았는지 참·거짓 | — | 04 |
| **백업**(backup) — 05가 정함 | 데이터베이스의 표와 줄을 파일로 옮겨 적어 두는 일(휴대폰 연락처를 파일 하나로 내보내기 예) | `pg_dump --format=custom --schema=ch31_shared --dbname=ch31_lab`(표준 출력 바이트를 임시 폴더 파일에 `"wb"`) | 05 |
| **복원**(restore) — 05가 정함 | 백업 파일로 표와 줄을 데이터베이스에 다시 만드는 일(새 휴대폰에서 연락처 파일 가져오기 예) | `pg_restore --dbname=ch31_restore`(파일을 표준 입력으로) | 05 |
| **덤프 파일**(dump) — 05가 정함 | 명령 `pg_dump`가 만든 백업 파일(내보낸 연락처 파일 그 자체) · 목차는 `pg_restore --list`(원문 줄의 번호는 실행마다 바뀜 — 출력 금지) | `ch31_shared.dump` | 05 |
| (이어 씀) 색인 · HNSW · 계획 줄 · 색인 스캔 — Ch 12 02 말 | 색인 = 「인덱스」(Ch 14 금지어) 대신 · 계획 줄 = `EXPLAIN`이 내놓은 줄(05는 `EXPLAIN (COSTS OFF)` — 어림 비용 뺌, 매번 같음) · 색인 스캔 = `Index Scan using …` · **`Seq Scan`은 「표의 줄을 처음부터 모두 읽는 계획」으로 풂**(Ch 12 말 「순차 스캔」은 Ch 31 금지어 「순차」 때문에 인용하지 않음) | `CREATE INDEX … USING hnsw (embedding vector_cosine_ops)` · `SET enable_seqscan = off` | Ch 12 02 |
| (이어 씀) 체크포인터 · 체크포인트 · 스레드(Ch 23 01) · 표 만들기 `setup()` · 표 만들기 기록 · 이름 공간(Ch 23 02) | 새 용어로 세지 않음(Ch 23 요약 §15 211행) · 05는 Ch 23 02 모양 그대로 `saver_conn`(autocommit·`dict_row`) + `SET search_path TO ch31_shared` | `PostgresSaver(saver_conn)`·`setup()` → 표 넷 · 기록 10줄 | Ch 23 |
| (풀이만) 확장 · `PGPASSWORD` · 표준 오류 출력(stderr) — 05 | 확장 = PostgreSQL에 새 자료형과 함수를 더하는 꾸러미(`CREATE EXTENSION` — 기본 이름 공간 `public`에 생김) · `PGPASSWORD` = PostgreSQL 명령이 비밀번호를 읽는 환경 변수(문서는 보안 까닭으로 권하지 않음 — 비밀번호 파일) · stderr = 명령이 오류 글을 내는 출력 | `dict(os.environ)` 복사에 넣음(Ch 28 03 모양) · `result.stderr.decode("utf-8").splitlines()` | 05 |

**뒤 절이 정할 말(01 권장 — 과정 금지어·대체어 목록이 먼저)**:

| 절 | 챕터 주제어 | 과정 금지어 여부 | 01 권장 |
|---|---|---|---|
| 02 | 트랜잭션 | **Ch 23 금지어** | 대체어 + 괄호 원어: **「한 묶음 작업(트랜잭션, transaction)」** — 01의 「한 묶음으로 실행하고 끝에서 확정」과 이음. 제목의 「트랜잭션」은 제목에만(강사 확인) |
| 02 | 커밋 | 아님(Ch 4 03 말) | 「확정(커밋)」 이어 씀 |
| 02 | 롤백 | 아님 — 단 **03 제목의 「롤백」(Alembic `downgrade`)과 뜻이 다름** | **「취소(롤백, rollback)」** — 「확정하지 않고 블록 안에서 바꾼 것을 모두 없던 일로 함」. 「되돌립니다」는 게이트 금지어 「돌립니다」, 「되돌려」는 금지어 「돌려」에 걸림 — 쓰지 말 것 |
| 02 | 원자성 | 아님 | 제목 말 — 첫 자리 세 문장(모두 되거나 모두 안 되는 성질) |
| 03 | 마이그레이션(DB 뜻) | **Ch 23 금지어** | 대체어 + 괄호 원어: **「표 구조 바꾸기(마이그레이션, migration)」**, 리비전 → **「판(리비전)」**, `upgrade` → **「판 올리기」**, `downgrade` → **「판 내리기」**, 03 제목의 「롤백」 = 판 내리기(02의 취소와 다름을 한 문장). **Ch 21 04 「옮기기(마이그레이션)」 = 코드 판 옮기기와 다른 뜻을 가르는 문장 필수**(Ch 21 요약 64행이 기댐) |
| 03 | 스키마(DB 표 구조) | **Ch 30 금지어** | 「표 구조」 · SQL 객체 `SCHEMA`는 「이름 공간」(Ch 23) |
| 04 | 커넥션 풀·고갈 | 「커넥션」은 제목에만 | 본문 **「연결 풀」**, 고갈 → 「연결 풀에 빈 연결이 없음」 · 「반환」(금지) → **「풀에 다시 넣음」**(01 글) · 반납 누락 → 「닫지 않고 둔 연결」 |
| 05 | 인덱스(HNSW) | **Ch 14 금지어** | **「색인」**(Ch 12 말) · 체크포인터·표 만들기(`setup()`)·스레드는 Ch 23 말 이어 씀(**새 용어로 세지 않기** — Ch 23 요약 §15 211행) · 백업·복원은 첫 자리 세 문장 · 「스냅샷」(Ch 23 금지) 쓰지 않기 |
| 모두 | 쿼리·레코드·필드·순차·병렬·반환·검증·측정·지연·추정·결정적·최대·로그·세션·이벤트(루프 말고) | 과정 금지어 | 조회 · 줄 · 칸 · 차례로 · 함께 · 내놓다(풀은 「다시 넣다」) · 검사 · 재다 · 걸린 초·기다린 시간 · 어림 · 매번 같은 값 · 이하·한도 · 기록 · 연결(DB) 또는 코드 이름(`AsyncSession`) · 사건 |

- **Ch 30 01 인계 반영(01 끝남)**: b2 「처리 함수를 `async def`로」(Ch 30 01 링크) — 「요청 함수」·「경로 함수」 0.
- 제목의 영어(「SQLAlchemy」·「PostgreSQL」·「Alembic」·「pgvector」·「DB &」)는 제목에 두고 본문 첫 자리에서 풂(01: 1절·b2 「챕터 제목의 DB는 데이터베이스(database)입니다. 상태 영속화는 Ch 23에서 배운 상태 저장(Persistence)과 같은 뜻입니다」·「절 제목의 SQLAlchemy는 …」) — 강사 확인.
- 새 용어 meta: 01 = **5**(비동기 엔진·드라이버·연결·연결 풀·SQL 글 객체).

### 금지어 (01 설명·주석·캡션·`.mmd`·alt 0건 — 제목·슬러그·코드 백틱 말고)

- 검사 스크립트 기기 **`.cache/ch31-01/tools/ban31.py`**(인자: `_src` 파일·노트북·추가 글롭) = Ch 30 `ban30.py` 목록 전부 + 「순차」·「동시성」·「식당」·「은행」·「창고」·「요청 함수」·「경로 함수」·「레코드」·「되돌려」·「되돌립」·「돌려」·「롤백」(01만 — 02·03은 대체어 결정 뒤 목록에서 빼고 괄호 원어만 허용)·「스키마」·「세션」·「쿼리」 + 과정 목록·사용자가 금지한 표현(과정 규칙)·「쉽게·간단히·당연히」·「강사 시연」·「개선 전」. **거짓 양성**: 「이벤트 」(← 「이벤트 루프」, 허용) · 「로그」(← 「프로그램」).
- **02 판(`.cache/ch31-02/tools/ban32.py`)**: 01 목록에서 「트랜잭션」·「롤백」만 빼고, 두 말은 `twoword.py`로 나온 자리를 모두 봄 — 허용 자리는 절 제목·제목 풀이(「절 제목의 트랜잭션(transaction)은」)·괄호 원어(「한 묶음 작업(트랜잭션)」·「취소(롤백, rollback)」)·03 제목 인용(「03절 제목의 롤백은」)뿐. 03도 「마이그레이션」을 같은 방식으로(괄호 원어·제목 인용만).
- G6 함정(01에서 걸린 것): 「PostgreSQL은 …」처럼 영어로 시작해 조사가 붙는 문장 → 「데이터베이스 서버 PostgreSQL은」 · 백틱 인용 바로 뒤 조사로 문장 시작(「`풀에 …: 0`은」) → 「출력 줄 `…`은」.

### 모델 설정

- 01~06 **모델 요청 0**, 키 셀 없음. 05 그래프는 「모델을 쓰지 않는 그래프」(노드가 값 두 배 — 준비 노트 §7). `nbkit.key_and_model_cells`를 쓰지 않음.

### 걸린 시간 처리 (01 선례)

- 01: 실행 1 `걸린 시간(초): 0.48` ↔ 실행 2 `0.19`(교재 출력 A) · B 0.47 ↔ 0.19 · 노트북 밖 0.47~0.48 ↔ 0.19~0.20. 결론·그림·b8·복습은 `함께 기다린 시간이 더 짧은가: True`와 매번 같은 값만.
- 04가 기다린 초를 다룬다면 출력하지 않거나(준비 노트 — 옛 판도 출력 안 함) 같은 규칙.

### paired 설계 (02·03·04 몫 — 01이 요지만)

| 절 | Before(실제 결함 — 받은 결함 결과만 빨강) | After | 주의 |
|---|---|---|---|
| **02** | **CHECK 위반**: 표 `accounts`(`CHECK (balance >= 0)`, 잔액 500·500) · 입금 +600을 **따로 확정**한 뒤 출금 −600이 SQLSTATE **`23514`**(`IntegrityError` ← `CheckViolationError`, `accounts_balance_check`)로 막힘 → `[(1, 500), (2, 1100)]` **합 1600**(빨강) | 두 줄을 **한 `engine.begin()` 블록** → 같은 오류 뒤 `[(1, 500), (2, 500)]` **합 1000** | 옛 판 「코드가 직접 던진 `RuntimeError`」는 Before로 쓰지 않음(준비 노트 §3 — `e3_tx.py`, 두 번 같음). 오류 출력은 `type(error).__name__`·SQLSTATE 등 매번 같은 것만 |
| **03** | 준비 노트 후보 가운데 **실제 결함 하나** — 권장 **기본값 없는 NOT NULL 칸 추가**: 줄 셋이 든 `tickets`에 `nullable=False` 칸을 더하는 리비전 → `upgrade head` 실패 `NotNullViolation`(`column "owner" … contains null values`) · 판 `20260911_01` 그대로 · 칸 없음(PostgreSQL DDL이 한 묶음이라 반쯤 적용 없음) | `server_default` 판 → 판 `20260929_02`·세 줄 모두 기본값 | **새 리비전 파일은 실습 폴더 `migrations/`가 아니라 임시 폴더 사본에**(Ch 23 「파일은 임시 폴더에만」) · Alembic은 `PATH`에 기대지 않게(파이썬 API `alembic.command`+`Config` 또는 `subprocess.run([sys.executable, "-m", "alembic", …])`) · 자식 프로세스에 `PYTHONDONTWRITEBYTECODE=1` · 파일 위치 셀 필요 · **묶음 계약(아래)** |
| **04** | 두 후보 가운데 **결정적인 쪽 권장 — 반납 누락**: `conn = await small.connect()`로 빌리고 닫지 않음 → `checkedout()` 1 → 둘째 `async with small.connect()` → **`sqlalchemy.exc.TimeoutError`**(`QueuePool limit of size 1 overflow 0 reached, connection timed out, timeout 0.20`) | `async with`로 빌림 → 둘 다 끝·`checkedout()` 0 | **이름 가르기**: `from sqlalchemy.exc import TimeoutError`는 내장 `TimeoutError`(Ch 16 05)를 가림 → **`sqlalchemy.exc.TimeoutError`로 적고**, 「내장 `TimeoutError`의 하위 클래스가 아님」(`issubclass` `False`, MRO `TimeoutError → SQLAlchemyError → …`) 한 문장 · `create_task`를 쓰면 첫 풀이 |

### 묶음 계약 (03 몫 — 01이 적어 둠)

- Part 7 `qa/check_bundle_execution.py` 27행 `smoke_sections`가 **Ch 31 03**을 풀린 묶음 `notebooks/`에서 실행(실행기 32행 = 이 챕터 맥 `.venv` — 기기에서 그대로 못 돎, Ch 30 마감처럼 손 대조) → **03은 키·모델·도구 파일 없이, DB만 있으면 돌아야 함** · 03 코드를 바꾸면 zip → (서버를 켠 곳에서) 검사 → 새 `code_sha256`(지금 `bundle-execution.json` Ch 31 줄 `b0594f2d…`는 옛 판) — 마감 몫.
- 03이 실습 폴더 `migrations/versions/`에 파일을 더하면 묶음·학생 리비전 사슬이 바뀜 → 임시 폴더 사본에서만.

### 색 (01절 Mermaid 4장)

- 셀에 적은 자료·값(접속 글·표의 줄) **초록(tool)** · 우리가 적은 코드(엔진 만들기·`async with` 블록·SQL 글·함수·await 줄·`gather()`)와 **실험·값 바꿔 보기에서 바꾼 값 파랑(flow)** · 출력으로 확인한 값(연결 수·줄 수·기록·참·거짓·Before 아닌 절에서 받은 오류) **노랑(measure)** · 라이브러리의 연결 풀·블록 끝 확정·PostgreSQL 서버·두 조건 공통 값·설치판 소스로만 본 것 **회색** · **보라 0**(모델 없음) · **빨강은 paired Before 결함 결과만**(02 합 1600·03 판 그대로·04 `TimeoutError` 등 — 01은 0).
- 모양: 넷 이상 한 줄은 `flowchart TB` · 나란한 조건은 공통 상자에서 칸 둘로(01-4 — 칸 사이 `~~~` 없이도 나란히 놓임) · 갈래는 점선 · subgraph 제목 `<br>` 금지 · 라벨 대괄호·따옴표·중괄호 금지(`[('시작', 1), …]` → 「시작 1 · 끝 1 · 시작 2」) · 개수는 한글 · **긴 라벨·코드는 `<br>`로 미리 나눔**(01 첫 렌더에서 넷이 자동 줄바꿈) · viewBox 폭 868 이하(01 최대 597) · 노드 id `call`·`end` 금지 · 라벨 숫자는 출력에 있는 것만 · 흔들린 초는 라벨·캡션·alt에 넣지 않음 · `%% classes` 줄.

### 비유 계열 — 「전화 교환대」 (01절이 엶)

- 사람 없이 **판·꽂는 자리·선(코드)·불빛만** — 꽂힌 선 수·빈자리·불 켜진 자리로 세어 읽히게. 짝: 판 = 연결 풀 · 꽂는 자리 수 = `pool_size` · 꽂힌 선 = 연결 · 켜진 불 = 서버와 이어진(쉬고 있거나 빌려 간) 연결.
- **01-5(채택, job `55814eca-21ec-4435-9945-4f45614baf2a`, 재생성 1회)**: 흰 바탕 · 같은 갈색 나무 판 둘 나란히 · 판마다 작은 둥근 불 셋 + 금색 테두리 꽂는 자리 셋 한 줄 · 왼쪽 판 왼쪽 자리에만 짧은 검은 선 하나 곧게 아래로·불 하나 노랑·나머지 불 둘 회색 · 오른쪽 판 선 셋·불 셋 노랑. 1차 `3d304f8c…`은 판 아래 선 고리가 여럿이라 탈락. 거의 흰 가로줄 172/614.
- **뒤 절 후보(되풀이 금지 — 01 소품: 같은 나무 판 둘·금색 테두리 자리·짧은 검은 곧은 선·노란/회색 둥근 불)**: 02 한 묶음 — 두 자리를 잇는 선 한 가닥의 양 끝(한쪽만 꽂힌 채 남은 판 = Before ↔ 양 끝이 모두 꽂히거나 모두 빠진 판 = After) · 03 판 올리기/내리기 — 교환대 판을 한 칸 더 넓은 새 판으로 갈아 끼우기(새 자리를 받칠 틀이 없어 옛 판이 그대로 = Before) · 04 빈자리 없음 — 모든 자리에 선이 꽂혀 불이 다 켜진 판과, 뽑지 않고 둔 선 하나 · 05 같은 배선을 둘째 판에 옮겨 꽂기(복원), 한 판에 두 색 선(검색 문서·체크포인트). 색·모양을 바꿔 01과 구별.
- **금지 소품**(앞 챕터·옛 원고): 화물 열차·번호판 차량·선로·창고(옛 원고)·오르골·종이띠·도킹 포트·정거장·우주선·온실·모종판·예인선·바지선·밧줄·홈통·물방울·도미노·체스판·즉석사진·세탁기·승강 상자·전표·가마·물레·발자국·말뚝·쟁반·서랍·바구니·저울·도장·개찰구·플러그(콘센트 플러그 — 교환대 선 끝은 괜찮음)·공항 검사·안내 데스크·식당·은행 창구·도서관 태블릿·건물 도면. 사람·손·글자·숫자·화살표·표지판·화면·전화기·헤드셋 없음. 스타일 문구 규격 §5-4 그대로, `generate_image` `params` `{"model":"nano_banana_pro",…,"aspect_ratio":"16:9","resolution":"2k","use_unlim":false,"count":1}`, 절당 1장·재생성 1회까지, 개수는 「exactly one …」·「Only these four cords」 모양으로, 「no loose cords, no loops」가 01에서 효과가 있었음. 크레딧은 거래 기록으로 그 절 몫(작업 조회 모델 표시 `nano_banana_2` — 기록만).

### 앞 챕터 인계 항목과 몫

| 넘긴 챕터 | 자리 | 판정 · 몫 |
|---|---|---|
| Ch 30 §19 | 01 b2 「요청 함수」·b3 「경로 함수」 | **고침(01 끝남)** — 「처리 함수」 |
| Ch 30 10 b8·06 b7 | 01 슬러그 · 05 체크포인터 저장 · SSE 저장 안 다룸 | **01 참(끝남)** — 슬러그 그대로, 표를 만들어 씀, SSE 0 · **05 몫**: 체크포인터로 그래프 상태를 PostgreSQL 표에 저장하는 장면 유지, Ch 30 앱·SSE 저장 넣지 않기 |
| Ch 30 §18-7 | 앱 파일 문법 예외 | 01은 앱 파일을 열지 않음 · 03(`migrations/`)이 열면 판단 |
| Ch 23 §15 209행 | 02 b3 「Ch23 중단 뒤 재개와 멱등성」 | 참 — 02 유지 |
| Ch 23 §15 210행 | 02 b7 「보상 작업」 | Ch 23이 다루지 않음 — **02 몫**(풀어 쓰거나 「이 챕터에서 실행하지 않음」) |
| Ch 23 §15 211행 | 05 새 용어 「체크포인터」 | **05 몫** — Ch 23 01 말로 잇고 새 용어로 세지 않기 |
| Ch 21 요약 64행 | 03 「마이그레이션」 | **03 몫** — Ch 21 04 「옮기기」와 다른 뜻 문장 |
| Ch 12 02 | 05 HNSW·`<=>`·`vector_cosine_ops` | 참 — 05는 「색인」 말, 학생 컨테이너가 Ch 12와 다름(포트 55431·계정 `postgres`)을 한 문장 |
| Ch 4 03 | 01 SQL·커밋·물음표 자리 | **이어 씀(01 끝남)** |
| Ch 2 12 | 01 `gather`·`perf_counter` · 04 `create_task` | **01 이어 씀(끝남)** · 04가 `create_task`를 쓰면 첫 풀이 |
| Ch 16 05 | 04 `except TimeoutError` | **04 몫** — 이름 가르기 |
| Ch 32 04 b3(대기 챕터 — 고치지 않음) | 「Ch31에서는 PostgreSQL, 트랜잭션, 인덱스와 pgvector를 배웁니다」 | 02(한 묶음 작업)·05(색인·pgvector)가 남아야 참 — 말은 바뀌어도 내용 유지 |
| `labs/part7/continuity-guide.md` 8~10행 | Ch 31 데이터·체크포인트 저장·트랜잭션·연결 풀·인덱스 | 마감 대조 |

## §01 → §02

**02절 주제**: 「트랜잭션과 원자성」(paired, **모델 없음 — 요청 0, 키 셀 없음**). 옛 판(`before/notebooks/02-…ipynb`·`before/_src/02-*.html`): 이름 공간 `ch31_tx` 표 `accounts`(`CHECK(balance>=0)`, 500·500) · Before 출금만 `engine.begin()`으로 확정 → **코드가 직접 `raise RuntimeError("입금 직전 장애")`** → 900 · After 한 블록(닿지 않는 입금 줄) → 1000 · 「트랜잭션」 22·「롤백」 12·「되돌립니다」(게이트 금지어) · 비유 「은행 창구」(Ch 6 겹침).

1. **01이 남긴 자리**: 01 정리 끝·b8 「02절에서는 두 계좌의 잔액을 바꾸는 이체를 봅니다. 바꾼 내용을 따로 확정할 때와 한 블록으로 확정할 때를 견줍니다」 → **02는 이체(두 계좌 잔액 바꾸기)를 따로 확정 ↔ 한 블록으로 확정해 견줘야 참**. 01 3절 결과 읽기 「블록 안에서 오류가 나면 확정하지 않는데, 그 모양은 02절에서 봅니다」 → **02가 오류 난 `engine.begin()` 블록이 확정하지 않는 것을 처음 보여야 참**.
2. **paired Before = CHECK 위반**(실제 결함 — 준비 노트 §3 `e3_tx.py`, 두 번 같음): 입금 +600을 따로 확정한 뒤 출금 −600이 SQLSTATE `23514`로 막힘 → `[(1, 500), (2, 1100)]` **합 1600**(빨강 — 받은 결함 결과). After = 두 줄을 한 `engine.begin()` 블록 → 같은 오류 뒤 `[(1, 500), (2, 500)]` **합 1000**(노랑). 정상 이체 100 → `[(1, 400), (2, 600)]`는 예시 부분 후보.
3. **옛 `RuntimeError` 장면 빼기**: 코드가 직접 던진 예외는 결함 장면이 아님(Ch 30 판정 기준) · `raise` 뒤 닿지 않는 줄도 빼기.
4. **말 「트랜잭션·커밋·롤백」**: 위 「뒤 절이 정할 말」 — 트랜잭션 → 「한 묶음 작업(트랜잭션)」(Ch 23 금지어라 대체어 + 괄호 원어), 커밋 → 「확정(커밋)」(Ch 4 03 이음, 01이 「확정」으로 씀), 롤백 → 「취소(롤백)」 권장(03 제목 「롤백」 = 판 내리기와 다른 뜻을 한 문장). 「되돌립니다」·「되돌려」 쓰지 않기(게이트·금지어). 02가 정한 말을 이 파일 용어 표에 덧붙이기.
5. **빨강은 Before 결함 결과만**: 합 1600(과 그 잔액 줄). 받은 `IntegrityError`는 Before에서도 오류 자체보다 「남은 잔액」이 결함 결과 — 오류 상자는 규격 §5-3대로(받아 출력한 오류 노랑, Before 결함 결과 빨강). After 결과 노랑.
6. **모델 없음 · 요청 0 · 키 셀 없음 · 파일 쓰기 0**.
7. **01이 정한 접속·이름 공간 모양**: 설정 셀 = `author_01.SETTINGS` 문자열 대조(위 「접속 글 자리」) · 엔진 `create_async_engine(database_url, …)`(02가 풀 인자를 쓰지 않으면 기본값 — 인자를 바꾸면 한 문장) · 이름 공간 `ch31_tx`를 처음 셀에서 `DROP SCHEMA IF EXISTS … CASCADE` → `CREATE SCHEMA` → 표 · **끝 정리 셀에서 지우고 `to_regnamespace` → `None`·`dispose()`**(01 9절 모양 — 다시 실행해도 같은 출력) · After 앞에서 잔액을 500·500으로 되살리는 셀(옛 `UPDATE … SET balance=500`)은 `UPDATE` 첫 풀이 한 문장.
8. **오류 받기**: `try`/`except IntegrityError as error`(Ch 2 05 L3 — 받은 오류 이름만, 셀은 끝까지) · 출력은 `type(error).__name__`·`error.orig.sqlstate`(또는 준비 노트의 확인한 속성) 등 **매번 같은 것만** — 오류 글 전체(서버 PID·주소가 들 수 있음)는 출력하지 않거나 첫 줄만 확인 뒤. `from sqlalchemy.exc import IntegrityError`는 내장 이름을 가리지 않음(04의 `TimeoutError`와 다름 — 04 몫).
9. **세션 판**: 준비 노트 e3 「세션 판도 같은 결과」 — 02가 `AsyncSession`을 쓰면 「세션」 말 없이 코드 이름 그대로 + `async_sessionmaker` 첫 풀이(위 「문법 범위」). 쓰지 않아도 됨(Core `engine.begin()`으로 충분).
10. **b3·b10 새로**: b3 = 01절(엔진·연결·`begin` 블록·이름 공간·확정) + Ch 4 03(커밋) + Ch 23 04~07(중단 뒤 이어 실행·멱등성 — Ch 23 §15 209행 참) · b7 「보상 작업」은 Ch 23이 다루지 않음(02가 풀거나 「실행하지 않음」) · b10 = PostgreSQL 트랜잭션·CHECK 제약 문서·SQLAlchemy Connections(`begin()` 오류 시 롤백) — 확인일.
11. **그림**: Mermaid 3~5(한 묶음 차례·Before/After 칸 둘·잔액 비교) + 삽화 1(「전화 교환대」 — 02 후보: 한 가닥 선의 양 끝, 01 소품 되풀이 금지), 보라 0, 빨강은 Before 결함 결과만.
12. **기록**: `02-diagnosis.md`·`02-figures.md`(렌더 전)·`집필점검표.md`·`qa/verification.md` 행 · 이 파일에 「§02 → §03」 · 보호 파일 대조(`manifest-changes.md`에 덧붙임 — 01 뒤 해시는 01 기록 값) · 새 커널 두 번(A 루트·B `notebooks/` 사본, B는 그림 전) 셀별 대조 · `env -u OPENAI_API_KEY PYTHONDONTWRITEBYTECODE=1` · 첫 실행은 `/tmp` 사본에서 · 끝낸 뒤 postgres 프로세스 0·55431 포트 0 확인.

## §02 → §03

**03절 주제**: 「Alembic 적용과 롤백」(paired, **모델 없음 — 요청 0, 키 셀 없음**). 옛 판(`before/notebooks/03-…ipynb`·`before/_src/03-*.html`): 파일 위치 `next(path for …)` → `subprocess.run(["alembic", …])`(PATH 의존) → 이름 공간 `ch31_migration` 지우고 `upgrade head`(`Running upgrade  -> 20260911_01`) → `to_regclass` → Before `downgrade base` → `None`(명령대로 한 것 — 결함 아님) · After 다시 `upgrade head`(고친 것 없음). 「리비전」 16·「롤백」 9·「마이그레이션」 7·「스키마」 6·「되돌」 1 · 비유 「도면」.

1. **02가 남긴 자리(03이 참이 되게 할 것)**: 02 노트북 6절·b4 소제목 「이 절의 취소와 03절 제목의 롤백」 = 「03절 제목의 롤백은 표 구조의 판을 내리는 일이라, 이 절의 취소와 뜻이 다릅니다」 · 02 b8·노트북 정리 끝 「03절에서는 Alembic으로 표 구조를 판마다 바꾸는 방법을 봅니다」 → **03은 제목의 롤백 = 판 내리기(`downgrade`)를 첫 자리에서 풀고, 표 구조를 판마다 바꾸는(판 올리기) 장면을 가져야 참**. 03이 「판 내리기」·「표 구조」와 다른 말을 고르면 02 두 문장(`author_02.py` 문자열 — 노트북 6절 결과 읽기·b4·b8)을 어떻게 맞출지 03 진단에 적을 것(02는 다시 실행할 필요 없이 `mdpatch.py`·`--src-only`로 됨 — 모델 없음, 출력 결정적).
2. **Before 실제 결함 후보(준비 노트 §3 — 02는 Alembic을 실행하지 않음)**: ① **기본값 없는 NOT NULL 칸 추가**(권장) → `upgrade head` 실패 `NotNullViolation`·판 `20260911_01` 그대로·칸 없음 ↔ After `server_default` 판 → 판 `20260929_02`·세 줄 모두 기본값 · ② downgrade 뒤 다시 올리면 줄 3 → 0 · ③ downgrade 없음(`pass`) → 다시 올리기 `DuplicateTable`. **02가 Alembic 없이 확인한 오류 모양**(`/tmp/ch31-02/exp/p2_for03.py`, 같은 서버·동기 드라이버 psycopg 3.3.3): 줄 셋이 든 표에 `ALTER TABLE … ADD COLUMN owner text NOT NULL`을 `engine.begin()` 블록에서 보내면 **`sqlalchemy.exc.IntegrityError`**(02와 같은 이름 — `except IntegrityError as error`로 받음) · `error.orig` = **`psycopg.errors.NotNullViolation`** · `error.orig.sqlstate` = **`23502`** · `str(error.orig)` = 한 줄 `column "owner" of relation "tickets" contains null values` · 블록이 취소되어 칸은 `id`·`title` 그대로. → 03이 Alembic 파이썬 API를 같은 프로세스에서 부르면 이 모양으로 올 것으로 보이나 **Alembic을 거친 모양은 03이 설치판에서 확인**(자식 프로세스면 종료 코드 1과 오류 글 — 준비 노트 e4). 02의 출력 모양(`type(error).__name__`·`error.orig.sqlstate`·라벨 줄 뒤 `print(error.orig)` — 매번 같은 것만)을 이어 쓸 수 있음.
3. **새 리비전 파일은 실습 폴더 `migrations/`가 아니라 임시 폴더 사본에**(묶음·학생 리비전 사슬·묶음 실행 계약 보호, Ch 23 「파일은 임시 폴더에만」). 02가 읽은 사실: `alembic.ini` = `script_location = %(here)s/migrations`·`prepend_sys_path = .` → ini와 `migrations/`를 함께 임시 폴더로 복사하면 `%(here)s`가 사본을 가리킴. 사본이면 Alembic이 가져온 `env.py`·리비전의 pyc도 사본에 생김(실습 폴더 `migrations/__pycache__/`·`versions/__pycache__/`에는 2026-09-11 맥 pyc가 이미 있음 — 늘리지 않기). `tempfile`·`shutil`은 처음 쓰면 한 문장.
4. **Alembic은 PATH에 기대지 않게**: 설치판 alembic **1.16.5**에서 `import alembic.command, alembic.config` 됨 · `sys.executable -m alembic --version` → `alembic 1.16.5`(02 확인, 가상환경 `bin`이 PATH에 없어도). 파이썬 API(`alembic.command.upgrade(cfg, "head")`)면 자식 프로세스·`PYTHONDONTWRITEBYTECODE` 넘기기가 필요 없음. 자식 프로세스를 쓰면 `env=`에 `PYTHONDONTWRITEBYTECODE=1`.
5. **접속 글 넘기기 — 02가 `env.py`를 읽어 찾은 함정**: `migrations/env.py` **12~15행** `config.set_main_option("sqlalchemy.url", os.getenv("CH31_SYNC_URL", "postgresql+psycopg://postgres:postgres@localhost:55431/ch31_lab"))`가 **ini·`Config.set_main_option`으로 적은 URL을 늘 덮어씀** → 파이썬 API에서 `cfg.set_main_option("sqlalchemy.url", …)`만 해서는 쓰이지 않음. 선택: 환경 변수 `CH31_SYNC_URL`(`os.environ` — 과정 「처음 쓰면 한 문장」, 앞 챕터 「키 값 출력 금지」와 같게 비밀번호 든 글은 출력하지 않기) / 임시 사본의 `env.py`만 고치기(실습 폴더 판은 그대로) / 기본값 `localhost` 그대로 — **이 기기에서는 `localhost:55431`도 붙음**(02 확인, 서버는 127.0.0.1에만 묶음 — 학생 Docker `-p 127.0.0.1:…`에서는 확인 안 함). 동기 접속 글은 챕터 공통 2의 `postgresql+psycopg://postgres:postgres@127.0.0.1:55431/ch31_lab`(01 설정 셀과 드라이버 부분만 다르다는 한 문장 — 02는 01 `SETTINGS`를 글자 그대로 썼고, 03은 다른 글이므로 「글자까지 같다」를 쓰지 말 것). `env.py`는 이름 공간 `ch31_migration`을 `CREATE SCHEMA IF NOT EXISTS`로 만들고 버전 표를 그 안에 둠 · 35행 조건 표현식·반환 힌트·`from __future__`(앱 파일 문법 — 03이 열면 판단, Ch 28 A-17 선례).
6. **파일 위치 셀(Ch 30 과정 표준, 챕터 공통 10)**: 후보 `".."`·`"."`·`"labs/part7/ch31-database"`, 찾을 파일 `"/alembic.ini"`, 고른 후보는 출력하지 않음, `assert` 한 줄 · 루트 커널(`run_section.sh`)·`notebooks/`(B)·묶음을 푼 `notebooks/` 세 자리에서 확인. 02는 실습 폴더 파일을 읽지 않아 이 셀이 없음(03이 챕터 첫 사용).
7. **묶음 계약(챕터 공통 「묶음 계약」)**: Part 7 `check_bundle_execution.py` 27행이 **Ch 31 03**을 풀린 `notebooks/`에서 실행 — **키·모델·도구 파일 없이 DB만 있으면 돌아야 함**(02도 도구 파일을 만들지 않음 — 03이 가져올 파일 없음) · 03 코드를 바꾸면 zip → (서버를 켠 곳에서) 검사 → 새 `code_sha256`(지금 `bundle-execution.json` Ch 31 줄 `b0594f2d…`는 옛 판) — 마감 몫.
8. **말**: 02가 정한 말 이어 씀 — 한 묶음 작업(트랜잭션)·확정(커밋)·취소(롤백) (위 용어 표). 01 권장 03 말: 「표 구조 바꾸기(마이그레이션, migration)」·「판(리비전)」·「판 올리기(upgrade)」·「판 내리기(downgrade)」 · **Ch 21 04 「옮기기(마이그레이션)」(코드 판 옮기기)와 다른 뜻 문장 필수**(Ch 21 요약 64행) · 「스키마」(Ch 30 금지) → 「표 구조」, SQL `SCHEMA` = 「이름 공간」(Ch 23) · 금지어 검사는 02 `ban32.py`에서 「마이그레이션」도 목록에서 빼고 `twoword.py`처럼 자리를 모두 보기. PostgreSQL은 표 구조 바꾸기(DDL)도 한 묶음 작업 안에서 돌아, 실패하면 칸이 반쯤 생기지 않음(준비 노트 ① 「칸 없음」·02 p2 확인 「칸 `id`·`title` 그대로」) — 02의 「한 묶음 작업·취소」로 이을 수 있음.
9. **빨강은 Before 결함 결과만**(예: 올리기 실패 뒤 판 번호 그대로·칸 없음, 또는 다시 올린 뒤 줄 0) · 받아 출력한 오류(`IntegrityError`·`NotNullViolation`·`23502`)는 노랑 · After 결과 노랑 · 보라 0 · 「도식 읽기」는 한쪽에만 맞는 상자를 공통이라 쓰지 않기(02-4는 두 판 출력에서 모두 확인한 값만 공통 상자에).
10. **그림**: Mermaid 3~5 + 삽화 1(「전화 교환대」 03 후보 — 판을 한 칸 넓은 새 판으로 갈아 끼우기·새 자리를 받칠 틀이 없어 옛 판 그대로). **되풀이 금지 소품**: 01 = 같은 갈색 나무 판 둘·금색 테두리 자리·짧은 검은 곧은 선·노랑/회색 둥근 불 · **02 = 짙은 초록 금속 판 하나·구멍 하나짜리 은색 자리 여섯(짝 셋)·파란 천 선(헤드폰 잭 모양 끝)·초록/회색 불·옅은 나무 선반·감긴 선**. 02 1차가 두 구멍 콘센트·두 핀 전원 플러그로 나와 탈락 → 「a single hole each, like a headphone jack」·「slim cylindrical metal tip plugs」·「No power outlets, no power plugs, no two-pin plugs」가 2차에서 효과 있었음. 작업 조회 모델 표시 `nano_banana_2`(기록만). 거래 기록 마지막은 02의 2026-09-29T16:34:28.831637Z(잔액 2257).
11. **옛 판에서 고칠 것(준비 노트)**: Before `downgrade base`(명령대로 한 것) · `["alembic", …]` PATH 의존 · `os.environ | {…}` 딕셔너리 합치기 · `(Path.cwd(), *Path.cwd().parents)`·`next(…)` · `import os, subprocess` 한 줄 · `.splitlines()[-1]` 사슬 · 리비전 설명 글 「상담 티켓 표 구조를 변경합니다」(실제로는 표를 만듦 — 출력 줄에 찍힘) · 자동 생성(`revision --autogenerate`) 설명(`env.py`에 `target_metadata` 없음 — 실행한 적 없음) · `alembic check` 종료 255 · pyc 생김 · b6 「Docker PostgreSQL 17.8」 틀 문장.
12. **실행·기록(02와 같은 차례)**: 노트북 밖 5번(Before 결함·After 결과가 결정적인지 — 판 번호·칸·줄 수·오류 이름·SQLSTATE) → `/tmp` 사본(`.cache/ch31-02/tools/runcopy.sh`) → A(`env -u OPENAI_API_KEY PYTHONDONTWRITEBYTECODE=1 … run_section.sh … 03`) → B(그림 전, `--cwd labs/part7/ch31-database/notebooks`) → 셀별 대조(`cmpout.py` — 설치 셀은 출력 조각 나눔만 달라 `outputs_sha256`이 다를 수 있음, 글자 대조로 판단) → 설계표 → `.mmd`·캡션 → `--no-exec` → 삽화 → `--no-exec` · 이름 공간 `ch31_migration`(버전 표 포함) 처음에 지우고 끝에서 지워 두 번 실행해도 같은 출력 · 실습 폴더 `migrations/`·`alembic.ini` 해시 전후 같음 확인 · 끝낸 뒤 postgres 프로세스 0·55431 포트 0 · 보호 파일 대조(`manifest-changes.md`에 덧붙임 — 02 뒤 값은 02 기록).

## §03 → §04

**04절 주제**: 「커넥션 풀 고갈과 대응」(paired, **모델 없음 — 요청 0, 키 셀 없음**). 옛 판(`before/notebooks/04-…ipynb`·`before/_src/04-*.html`): `pool_size=1, max_overflow=0, pool_timeout=0.2` · `asyncio.create_task(hold(0.6))` + `asyncio.sleep(0.05)` 뒤 둘째 연결 → `sqlalchemy.exc.TimeoutError`(Before) · After `pool_timeout=1.0`·첫 작업 0.25초 → `1 1`·`pool.status()` 글 · **`from sqlalchemy.exc import TimeoutError`가 내장 이름을 가림** · `create_task` 첫 풀이 없음 · 힌트(`delay: float`·`-> None`·`-> int`) · 「반환」·「지연」·「백프레셔」·「상위 백분위수」.

1. **03이 남긴 자리(04가 참이 되게 할 것)**: 03 노트북 정리 끝·b8 「04절에서는 연결 풀에 빈 연결이 없을 때 무슨 일이 생기는지 봅니다」 → **04는 풀에 빈 연결이 없어 둘째 연결을 받지 못하는 장면을 가져야 참**(아래 두 후보 모두 해당). 02·03은 연결을 한 번에 하나씩만 빌렸고(02 기본 풀 5·03 동기 엔진 기본), 「연결 풀」 말은 01이 정함(04 제목의 「커넥션 풀」은 제목에만).
2. **Before 실제 결함 — 03이 이 기기에서 다시 확인(`.cache/ch31-03/exp/e4_pool.py`, 3번 모두 출력 sha256 `124e967d72dbe645`)**: **반납 누락(권장 — 타이밍에 기대지 않음)** `small = create_async_engine(URL, pool_size=1, max_overflow=0, pool_timeout=0.2)` → `conn = await small.connect()`(닫지 않음) → `small.pool.checkedout()` **1**, `small.pool.status()` = **`Pool size: 1  Connections in pool: 0 Current Overflow: 0 Current Checked out connections: 1`** → 둘째 `async with small.connect() as second:` → **`sqlalchemy.exc.TimeoutError`**, 글 한 줄 **`QueuePool limit of size 1 overflow 0 reached, connection timed out, timeout 0.20 (Background on this error at: https://sqlalche.me/e/20/3o7r)`** · 풀 클래스 `AsyncAdaptedQueuePool`. **After** = `await conn.close()` 뒤 `checkedout()` **0**·`checkedin()` **1**, `async with`로 두 번 빌리면 둘 다 `SELECT 1` → `1`, 끝난 뒤 `status()` = **`Pool size: 1  Connections in pool: 1 Current Overflow: 0 Current Checked out connections: 0`**. 지금 장면(풀 1·대기 0.2초·`create_task` 동시 둘 — 준비 노트 5/5)도 되지만 첫 연결에 걸린 초와 `sleep(0.05)`가 비슷해(준비 노트 §2 04) 반납 누락 쪽을 권장.
3. **이름 가르기(03 확인)**: `issubclass(sqlalchemy.exc.TimeoutError, TimeoutError)`(내장) = **`False`**, MRO **`TimeoutError → SQLAlchemyError → HasDescriptionCode → Exception → BaseException → object`** → 노트북은 `import sqlalchemy.exc`·`except sqlalchemy.exc.TimeoutError as error:`로 적고, Ch 16 05에서 배운 `except TimeoutError`(내장)로는 이 오류를 받지 못한다는 한 문장. `from sqlalchemy.exc import TimeoutError`는 쓰지 않기(내장 이름을 가림). 오류 출력은 `type(error).__name__`·모듈 이름(`sqlalchemy.exc`)·글 첫 줄처럼 매번 같은 것만(글의 오류 설명 주소 `https://sqlalche.me/e/20/3o7r`은 판마다 같은 글 — 인용하면 b10과 맞출 것).
4. **닫지 않은 연결은 셀 안에서 직접 닫기**: 반납 누락 장면에서 `conn`을 그대로 두고 `dispose()`·커널 끝으로 가면 SQLAlchemy가 쓰레기 수거 때 경고를 stderr에 낼 수 있음(03 확인에서는 `await conn.close()`를 불러 경고 0 — 부르지 않은 판은 실행하지 않음). **결정적 출력**을 위해 After 앞에서 `await conn.close()`로 닫고 `checkedout()` 0을 출력.
5. **풀 상태는 결정적 값으로**: `pool.checkedout()`·`checkedin()`·`size()`·`status()` 글은 매번 같음(위 2). **걸린 초는 결론에 쓰지 않기**(챕터 공통 4 — 01 선례: 초는 결과 읽기 둘째 단락·b6 표·「확인할 점」·b7에만, `assert` 금지). 대기 제한 `pool_timeout=0.2`는 글에 찍히는 설정값(흔들리지 않음).
6. **출력 차례(03에서 배운 것)**: 한 셀에서 stdout과 stderr(경고·라이브러리 기록)가 섞이면 ipykernel이 흐름마다 0.2초 타이머로 내보내 셀 안 차례가 실행마다 바뀔 수 있음(설치 ipykernel 7.3.0 `iostream.py` 446·658~669행) — 04에 경고가 찍힐 수 있는 셀은 print와 나누거나 경고가 안 나게(위 4).
7. **비동기 문법**: 04는 비동기 엔진(asyncpg) — 설정 셀은 **`author_01.SETTINGS` 글자 그대로** 쓸 수 있음(03은 `psycopg`로 바꾼 판 — 04는 01 판을 쓸 것, 생성기에서 대조). 셀 맨 위 `await`·`async with`는 01·02 이어 씀. `asyncio.create_task`를 쓰면 **첫 풀이 한 문장**(Ch 2 12 전제 금지). `async def` 힌트(`delay: float`·`-> None`) 빼기.
8. **말**: 01 「연결 풀」·「쉬고 있는 연결」·「빌려 간 연결」·「풀에 다시 넣음」(「반환」 금지) · 반납 누락 → 「닫지 않고 둔 연결」 · 고갈 → 「연결 풀에 빈 연결이 없음」 · 02 「한 묶음 작업」·「취소」, 03 「판」(표 구조의 판에만 — 04가 패키지 번호를 적으면 01·02처럼 「판은 sqlalchemy …」로 둘지, 03처럼 「버전」으로 둘지 정할 것: 04는 Alembic을 쓰지 않으므로 01·02 모양도 됨) · 「대기 제한」(`pool_timeout`) · 「백프레셔」·「상위 백분위수」(옛 판)는 실행하지 않으면 빼거나 「실행하지 않았습니다」.
9. **색**: 빨강은 **Before 결함 결과만**(닫지 않은 연결 때문에 둘째 연결이 `TimeoutError`로 막혀 받지 못한 것 — 받아 출력한 오류 상자는 노랑, 「빌려 간 연결 1·빈 연결 0」 같은 결함 결과 값이 빨강 후보) · After 결과 노랑 · 풀·라이브러리 회색 · 보라 0.
10. **그림**: Mermaid 3~5 + 삽화 1(「전화 교환대」 04 후보 — 모든 자리에 선이 꽂혀 불이 다 켜진 판과, 뽑지 않고 둔 선 하나). **되풀이 금지 소품**: 01 = 갈색 나무 판 둘·금색 테두리 자리·짧은 검은 곧은 선·노랑/회색 둥근 불 · 02 = 짙은 초록 금속 판 하나·은색 한 구멍 자리 여섯(짝 셋)·파란 천 선·초록/회색 불·옅은 나무 선반·감긴 선 · **03 = 크림색 판 둘·검은 둥근 자리(세로 줄마다 둥근 테두리)·주황 짧은 꽂이·회색 둥근 마개·옅은 회색 탁자·빈 구멍 셋 가는 판, 선·불 없음**. 03 1차가 「빈 자리」를 판에 붙여 그려 탈락 → 「no panel has any empty hole」·「Left panel is narrow: it has only two columns」가 2차에서 효과. 작업 조회 모델 표시 `nano_banana_2`(기록만). 거래 기록 마지막은 03의 2026-09-29T17:14:39.983621Z(잔액 2253).
11. **옛 판에서 고칠 것(준비 노트)**: `from sqlalchemy.exc import TimeoutError` · `create_task` 풀이 없음 · `sleep(0.05)` 타이밍 기대 · After가 설정값 바꾸기(1.0초 — 결함 코드를 고친 것 아님) · 힌트 · 코드 셀 4·최대 18줄 · b1·b6 「연결을 일찍 반환」·b4 `pool_pre_ping`·`pool_recycle`·백프레셔(실행 안 함)·b7 「상위 백분위수」.
12. **실행·기록(02·03과 같은 차례)**: 노트북 밖 5번 → `/tmp` 사본(`.cache/ch31-03/tools/runcopy.sh <사본> <커널 작업 폴더>`) → A(`env -u OPENAI_API_KEY PYTHONDONTWRITEBYTECODE=1 … run_section.sh … 04`) → B(그림 전, `--cwd labs/part7/ch31-database/notebooks`) → 셀별 대조(`cmpout.py`, 글자 대조 · `dump3.py`로 셀별 출력 보기) → 설계표 → `.mmd`·캡션 → `--no-exec` → 삽화 → `--no-exec` · **`--no-exec` 뒤 G5 「결과 읽기 첫 단락 숫자 인용이 출력에 없음」은 출력이 생긴 뒤에야 잡히므로 한 번 더 확인**(03에서 셋) · 직접 렌더는 기기가 aarch64라 `LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu` · 다시 렌더한 PNG를 같은 이름으로 다시 stage하면 옛 그림이 보일 수 있음 → 다른 이름 사본으로 확인 · 04는 표가 필요 없으면 이름 공간을 만들지 않아도 됨(옛 판은 `SELECT pg_sleep`만) — 만들면 제 이름(`ch31_pool` 등)을 처음에 지우고 끝에서 지우기 · 끝낸 뒤 postgres 프로세스 0·55431 포트 0 · 보호 파일 대조(`manifest-changes.md`에 덧붙임 — 03 뒤 값은 03 기록).

## §04 → §05

**05절 주제**: 「pgvector 체크포인터 공존과 백업」(experiment, **모델 없음 — 요청 0, 키 셀 없음**). 옛 판(`before/notebooks/05-…ipynb`·`before/_src/05-*.html` — 준비 노트 §1·§2 05): 기본 이름 공간 `public`에 `CREATE EXTENSION vector` · 이름 공간 `ch31_shared` 표 `documents`(`vector(3)` 세 줄)·HNSW(`vector_cosine_ops`) · `<=> '[0.9,0.1,0]'` → `['배송', '환불']` · `EXPLAIN (ANALYZE, BUFFERS, COSTS OFF)`(시간·버퍼 줄이 흔들림) · `PostgresSaver.from_conn_string(…)`+`setup()`+**`lambda` 노드** 그래프 `{'value': 12}` · **`docker exec kdt-ch31-postgres pg_dump …`** → `dropdb`/`createdb ch31_restore` → `CREATE EXTENSION vector` → `psql` 복원 → `(3, 3)`·HNSW `True` · 상태 형식 클래스를 `with` 안에서 정의 · **코드 셀 25줄**(verify 「max 25 lines」가 이 셀) · 「인덱스」·「스냅샷」 류 · 비유 「창고와 배송 장부」(Ch 3 가족 겹침).

1. **04가 남긴 자리(05가 참이 되게 할 것)**: 04 노트북 정리 끝 「05절에서는 같은 PostgreSQL 서버에 검색 문서 표와 체크포인터 표를 함께 두고, 백업과 복원을 해 봅니다.」(글자 그대로) · 04 b8은 굵은 라벨 때문에 70자를 넘어 둘로 나눔 — 「05절에서는 같은 PostgreSQL 서버에 검색 문서 표와 체크포인터 표를 함께 둡니다. 그 서버에서 백업과 복원을 해 봅니다.」 → **05는 같은 서버(`127.0.0.1:55431`의 `ch31_lab`)에 검색 문서 표(pgvector)와 체크포인터 표를 함께 두고, 백업과 복원을 실제로 해야 참**. 05가 다른 말(예: 「색인이 든 문서 표」)을 고르면 04 두 문장(`author_04.py` — 노트북 정리 셀·`src_html()` b8)을 `mdpatch.py`·`--src-only`로 맞출 수 있음(모델 없음, 04 출력 결정적 — 다시 실행 불필요).
2. **준비 노트 결정적 값(준비 노트 §7-2 `e6_shared.py` — 04는 다시 돌리지 않음, 05가 설치판에서 다시 확인)**: 가까운 문서 `배송`(거리 `0.0061`)·`환불`(`0.8896`) · **`EXPLAIN (COSTS OFF)`(ANALYZE 없이)** = `Limit / Sort / Seq Scan on documents` 네 줄(시간 줄 없음 — 매번 같음) · `SET enable_seqscan = off` 뒤 `Index Scan using documents_embedding_hnsw`(매번 같음) · `setup()` 뒤 표 넷 + `documents` · `{'value': 12}`·기록 길이 3 · **체크포인트 표 줄 수 `(3, 1, 3, 10)`** · 덤프에 `CREATE TABLE ch31_shared.documents`·`USING hnsw` 있음, `CREATE EXTENSION` 없음 · 확장 없이 복원 → 종료 3 `type "public.vector" does not exist` · 확장 뒤 복원 → `(3, 3, True)` · **복원한 DB에서도 `get_state` → `{'value': 12}`** · `pg_restore -l`의 TABLE 항목 5. 흔들리는 값: 덤프 줄 수(이 판 232)·아카이브 바이트(이 판 8,494)·`EXPLAIN ANALYZE` 시간 줄 → 결론·그림에 쓰지 않기(챕터 공통 4). 결정적 비교 값은 **행 수·`get_state` 값·계획 글의 노드 이름**.
3. **완료 챕터가 기대는 것**: **Ch 30 10 b8 「Ch 31 05절은 체크포인터로 그래프의 실행 상태를 PostgreSQL 표에 저장합니다」 유지**(`_src`·HTML·노트북 [44]·`author_10.py` — 05가 체크포인터 저장 장면을 빼면 거짓) · 같은 b8 「보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다」(Ch 30 06 b7도) — SSE 넣지 않기 · Ch 30 앱에 붙이는 일 넣지 않기 · **Ch 23 01 「체크포인터」·「스레드」, Ch 23 02 `setup()` = 「표 만들기」 말 이어 씀 — 새 용어로 세지 않기**(Ch 23 요약 §15 211행) · Ch 12 02 HNSW·`<=>`·`vector_cosine_ops`(05는 「색인」 말, 학생 컨테이너가 Ch 12와 다름 — 포트 55431·계정 `postgres` 한 문장) · **Ch 32 04 b3**(대기) 「Ch31에서는 PostgreSQL, 트랜잭션, 인덱스와 pgvector를 배웁니다」 — 05가 색인(HNSW)·pgvector를 남겨야 참.
4. **백업 명령을 두 환경에서 — 04가 이 기기에서 확인한 사실**: 훅(`pre_exec.sh`)을 source한 셸의 `PATH`에 **`pg_dump` 없음**(`command -v pg_dump` → 없음) · 가상환경 파이썬의 **`shutil.which("pg_dump")` → `None`** · pgenv(`$ROOT/.cache/vm/pgenv/bin`)에 `pg_dump`·`pg_restore`·`psql` **17.11** 있음(서버와 같은 버전 — `pg_dump`는 서버 버전 이상이어야 함). 작업 기기에는 Docker 없음. → **훅이 `PATH`에 pgenv `bin`을 더할지 05가 정함**(훅은 01이 만든 다섯 절 공용 파일 `8a9529f1…` — 고치면 해시·01~04 진단의 훅 해시와 달라짐을 05 진단에 적기; 더하지 않으면 작업 기기에서 노트북이 백업 셀을 못 돎) · 학생은 컨테이너 안 명령(`docker exec kdt-ch31-postgres pg_dump …`) — 노트북이 두 환경에서 돌게: `shutil.which("pg_dump")`로 찾고, 없으면 `docker` 명령 목록으로(**조건 표현식 없이 여러 줄 `if` 문**, `subprocess.run([...])` 리스트 — 셸 없이) · `shutil`·`subprocess`는 처음 쓰면 한 문장(03이 `shutil`·`tempfile`을 씀 — 이어 씀) · 비밀번호는 명령 줄·출력에 찍지 않기(`PGPASSWORD`를 `env=`로 넘기면 값 출력 금지 — 앞 챕터 「키 값 출력 금지」와 같게).
5. **백업 파일 자리**: 연결 폴더 밖 임시 폴더(`tempfile.mkdtemp(prefix="ch31-05-")` — 03 선례, 지우지 않고 둠을 한 문장) · **출력에 경로 찍지 않기**(임시 폴더 위치는 실행마다 다름) · 결정적 비교 값은 파일 크기 대신 복원 뒤 행 수·HNSW 색인 있음·`get_state` 값.
6. **04 끝 서버 상태(04가 확인)**: 이름 공간 `public`만 · 확장 **`plpgsql`만 — `vector` 없음** · 데이터베이스 `ch31_lab`·`postgres`만(**`ch31_restore` 없음**) · `max_connections` 100. → 05는 제 첫 셀에서 `CREATE EXTENSION IF NOT EXISTS vector`(확장은 `public`에 생김 — **마감 검토 B-3 정정**: 이름 공간 덤프에 `CREATE EXTENSION`이 빠지는 까닭은 확장의 자리가 아니라 `pg_dump`에 `--schema`를 주면 확장을 넣지 않기 때문, 확장을 이름 공간 안에 만들어도 0 · `--extension=vector`를 더하거나 DB 전체면 들어감 — `.cache/ch31-close/exp/b3_ext.out`) · 복원 DB `ch31_restore`와 이름 공간 `ch31_shared`는 처음에 지우고 다시 만들고 끝에서 지우기(옛 판은 지우지 않음 — 두 번 실행해도 같은 출력) · **체크포인터 표는 `setup()`이 기본 이름 공간 `public`에 만듦(준비 노트 「표 넷」)** → 다시 실행하면 줄 수 `(3, 1, 3, 10)`이 늘 수 있으니 처음에 그 표들을 지우거나 스레드를 지우는 방법을 05가 설치판에서 확인해 고르기 · 확장 없이 복원하는 실패(종료 3)는 실제 조건 실패 장면 후보(experiment라 **노랑**).
7. **문법**: `lambda` 노드 → **이름 있는 함수**(값 두 배 — 「모델을 쓰지 않는 그래프」로 공개, Ch 20 03·Ch 23·24 선례, 가짜 모델 아님) · 상태 형식 클래스는 `with` 밖 제 셀에(`TypedDict` — 규격 §2-2 L5, 필드만) · **25줄 셀 나누기**(비준비 셀 10줄 이하) · `import os, subprocess` 한 줄 두 모듈 → 줄 나누기 · 호출 깊이 2 이하 · 04가 쓴 것: 셀 맨 위 `await`·`async with`, `try`/`except 모듈.이름 as error`, `issubclass`·`__module__`(첫 풀이 04).
8. **Windows**: 05 옛 판은 동기 `PostgresSaver`(psycopg) — 그대로면 해당 없음. **비동기 체크포인터(`AsyncPostgresSaver`)로 바꾸면** 「On Windows, Psycopg is not compatible with the default ProactorEventLoop」(psycopg 문서 — 준비 노트 §7-3, 실행 안 함) 한 문장. 01~04의 asyncpg는 해당 없음.
9. **접속 글**: 05는 동기 드라이버 — `PostgresSaver.from_conn_string`·`psycopg`는 `postgresql://postgres:postgres@127.0.0.1:55431/ch31_lab`, SQLAlchemy로 pgvector를 쓰면 `postgresql+psycopg://…`(챕터 공통 2) — 「01 설정 셀과 드라이버 부분만 다르다」 한 문장, 「글자까지 같다」 금지(03 선례, 생성기에서 `replace` 대조). 04는 01 판 글자 그대로.
10. **말(04가 정한 것 이어 씀)**: 대기 제한·반납·이름 가림(용어 표) · 패키지·서버 번호는 **「버전」**(03·04 모양 — 교환대 「판」 비유와 겹치지 않게; 05도 비유에 「판」을 쓰면 같은 까닭) · 「색인」(Ch 12 — 「인덱스」 Ch 14 금지어) · 백업·복원은 첫 자리 세 문장(뜻 → 일상 예 → 코드) · 「스냅샷」(Ch 23 금지)·「인스턴스」(과정 금지 — 옛 04 b8에 있었음) 쓰지 않기 · 사용자 금지 표현(위 금지어 목록) 0.
11. **색·그림**: experiment → **빨강 0** · 받은 오류(확장 없이 복원)는 노랑 · 보라 0 · Mermaid 3~5 + 삽화 1(「전화 교환대」 05 후보: 같은 배선을 둘째 판에 옮겨 꽂기(복원), 한 판에 두 색 선(검색 문서·체크포인트)). **되풀이 금지 소품**: 01 = 갈색 나무 판 둘·금색 테두리 자리 셋·짧은 검은 곧은 선·노랑/회색 불 · 02 = 짙은 초록 금속 판 하나·은색 한 구멍 자리 여섯(짝 셋)·파란 천 선(헤드폰 잭 모양 끝)·초록/회색 불·옅은 나무 선반·감긴 선 · 03 = 크림색 판 둘·검은 둥근 자리·주황 짧은 꽂이·회색 둥근 마개·옅은 회색 탁자, 선·불 없음 · **04 = 짙은 남색 ㄴ자 교환대 둘(세운 판 + 누운 선반)·흰 테두리 자리 하나씩·선반 받침 구멍 하나씩·겨자색 굵은 선과 가는 금빛 끝, 불 없음**. 04는 1차 채택 — 「exactly one …」·「Only these two cords in the whole image」·「No lamps, no lights」·「No power outlets, no power plugs, no two-pin plugs」가 효과. 작업 조회 모델 표시 `nano_banana_2`(기록만). **거래 기록 마지막은 04의 2026-09-29T18:56:18.327904Z(잔액 2251)**.
12. **실행·기록(01~04와 같은 차례)**: 노트북 밖 5번(계획 글·행 수·`get_state`·복원 결과가 결정적인지) → `/tmp` 사본(`/tmp/ch31-04/tools/runcopy.sh <사본> <커널 작업 폴더>` — 없으면 `.cache/ch31-03/tools/runcopy.sh`) → A(`env -u OPENAI_API_KEY PYTHONDONTWRITEBYTECODE=1 timeout 170 bash run_section.sh textbook/part7/ch31-database 05`) → B(그림 전, `--cwd labs/part7/ch31-database/notebooks`) → 셀별 대조(`cmpout.py`, `dump3.py`) → 설계표 → `.mmd`·캡션 → 직접 렌더로 PNG 확인(`PUPPETEER_CACHE_DIR=/tmp/pptr-cache LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu python3 textbook/_notebook/mermaid/render_mermaid.py … --only 05-` — 04는 첫 렌더에서 넷 모두 자동 줄바꿈, `<br>`로 미리 나눔) → 삽화 → `--src-only` 뒤 `--no-exec`(**`--no-exec`는 생성기를 부르지 않음** — `_src`만 고쳤으면 먼저 `author_05.py --src-only`) · **실행 시간**: 05는 `pg_dump`·복원·그래프가 있어 한 셸 호출 180초 안에 A가 끝나는지 사본에서 먼저 재기(04 A는 약 10초) · 끝낸 뒤 postgres 프로세스 0·55431 포트 0 · 실습 폴더 파일 17개 해시(`/tmp/ch31-03/lab-before.sha` — 04 끝에도 17/17 같음) · 보호 파일 대조(`manifest-changes.md`에 덧붙임 — 04 뒤 값은 04 기록).

## §05 → 실습 절

**실습 절(06)**: 챕터 끝 실습 절(다른 작업자가 새로 씀 — 슬러그 후보 `06-DB-실습`·`06-상태-영속화-실습`·`06-DB와-상태-영속화-실습`, 준비 노트 §14). 형식 experiment · 새 문법·API 0 · 01~05에서 쓴 이름만. 아래는 05 작업자가 01~05 완료본(노트북·생성기·진단)에서 실제로 확인한 사실입니다.

1. **05가 남긴 자리(실습 절이 참이 되게 할 것)**: 05 노트북 정리 끝·b8 「06절은 이 챕터의 실습 절입니다. 01~05절에서 배운 것을 한 흐름으로 모아 실행합니다」 → **06은 01~05 기능 가운데 몇 가지(규격 §7-2 — 2~3개)를 한 상황에 이어 붙여야 참**. 05 b8에는 06 링크가 없음(슬러그 미정) — 슬러그를 정하면 05 b8에 링크를 더할지 06 작업자·마감이 판단(`author_05.py` `src_html()` b8 문장 + `--src-only` → `run_section.sh … 05 --no-exec`, 모델 없음·출력 결정적이라 05 재실행 불필요 · 노트북 정리 셀은 `mdpatch.py`).
2. **01~05가 실제로 가르친 것(실습 절 「앞에서 배운 내용」 표의 재료)**:

   | 절 | 배운 것(노트북에서 실제로 실행) | 실습에서 쓸 수 있는 곳 |
   |---|---|---|
   | 01 | `create_async_engine(url, pool_size=3, max_overflow=0)` · `async with engine.connect()`·`engine.begin()` · `text("… :id …")` + 딕셔너리 값 · `fetchall`·`scalar_one`·`rowcount` · `asyncio.gather`(코루틴을 인자로 하나씩) · `engine.pool.checkedin()`·`checkedout()` · `dispose()` · 이름 공간 지우고 만들기·`to_regnamespace` | 표 준비·줄 읽기·끝 정리 |
   | 02 | 한 묶음 작업(`engine.begin()` 블록 하나)·확정·취소 · `CHECK` 제약 · `except IntegrityError as error`·`error.orig.sqlstate`(`23514`) · `UPDATE` | 두 변경을 한 블록으로 — 실행 2 값 하나(CHECK를 넘는 값) 후보 |
   | 03 | Alembic 파이썬 API(`command.upgrade`·`downgrade`)·임시 폴더 사본·환경 변수 `CH31_SYNC_URL`·파일 위치 셀 | 실습 흐름에 넣으면 셀이 많아짐(03은 묶음 실행 검사 절 — 아래 8) |
   | 04 | 풀 크기·대기 제한 `pool_timeout`·반납(`close()`·`async with`)·`sqlalchemy.exc.TimeoutError`·이름 가림·`pool.status()` | 흐름 끝에 `checkedout()` 0 확인 · 실행 2 값 하나(`pool_timeout`) 후보 |
   | 05 | psycopg 동기 연결(`autocommit=True`)·pgvector `vector(3)`·HNSW·`<=>`·`EXPLAIN (COSTS OFF)` · `PostgresSaver`+`setup()`+`SET search_path` · 모델을 쓰지 않는 그래프(`double_value`) · `get_state` · `shutil.which`·`subprocess.run(…, input=, capture_output=True, env=)` · `pg_dump --format=custom --schema=…`·`pg_restore --list`·`pg_restore --dbname=…` · 복원 전에 확장 만들기 | 체크포인트 저장 → 백업 → 복원 뒤 `get_state` 같음 — 실행 2 값 하나(복원 전에 확장 만들기) 후보 |

   **주의**: 01·02·04는 **비동기**(asyncpg — 셀 맨 위 `await`), 03·05는 **동기**(psycopg). 한 흐름에 둘을 섞으면 드라이버 부분만 다른 접속 글 둘이 필요하고 그 까닭을 한 문장(05 1절·b3 문장 모양). 05의 체크포인터는 동기 `PostgresSaver` — `AsyncPostgresSaver`는 어느 절도 실행하지 않음(새 API — 실습 절에 쓰면 안 됨).
3. **새 문법·API 0 조건에서 쓸 수 있는 함수(모두 노트북에만 있음 — 도구 파일 없음)**: 01 `read_question(item_id, wait_seconds)`(전역 `engine`·`read_sql`·`step_log`) · 02 `read_balances()`·`add_balances(rows)`·`transfer_one_block(from_id, to_id, amount)`·`transfer_two_blocks(…)` · 03 `show_state()`·`try_upgrade()` · 04 `ask_database()` · 05 `shared_tables(cursor)`(이름 공간 `ch31_shared` 고정)·`run_tool(tool_args, input_bytes)`(전역 `command_start`·`server_args`·`tool_env`)·`restore_copy(make_extension)`(전역 `cur`·`restore_url`·`dump_bytes`, DB 이름 `ch31_restore` 고정)·`read_restored()`·`restored_state()`(전역 `builder`·`thread_config`)·노드 `double_value(state)`. **대부분 전역 이름에 기댐** → 실습 절이 두 절 이상의 함수를 그대로 쓰려면 **`notebooks/db_tools.py` 첫 판**(챕터 공통 8 — 이름 겹침 확인·생성기 대조 사슬(Ch 30 04 본 `TOOLS_HEAD`·`check_tools`·쓰기 가드)·공개 목록 두 곳·함수마다 「어느 절에서 배웠는지」 주석·전역 대신 인자 — 인자 모양이 바뀌면 처음 가져오는 절(=06)에서 한 문장, 규격 §2-7 4·5). 노트북에 다시 적으면 「같은 코드로 다시 정의합니다」 금지(규격 §2-7 5) — 짧은 조립 셀로 풀어 쓰는 편이 도구 파일 사슬보다 가벼울 수 있음(Ch 2·4 선례 — 챕터 전체 코드가 줄지 않으면 도구 파일을 만들지 않음).
4. **설정 셀·훅·이름 공간 정리 모양**: 접속 글 셀은 01 `author_01.SETTINGS`(asyncpg) 또는 05 판(`postgresql://…` — psycopg, 드라이버 부분만 다름)을 **생성기에서 문자열 대조**(「글자까지 같다」는 대조한 판에만) · 훅 `pre_exec.sh` **`dd564645…`**(05가 pgenv `bin`을 PATH 끝에 더함 — 실습 절이 `pg_dump`를 부르면 작업 기기에서 그대로 찾음, 학생은 `shutil.which`가 없으면 Docker 갈래) · 이름 공간은 제 이름(예 `ch31_practice` — 01 `ch31_async`·02 `ch31_tx`·03 `ch31_migration`·05 `ch31_shared`와 겹치지 않게)을 **처음 셀에서 `DROP SCHEMA IF EXISTS … CASCADE`로 지우고 끝에서 지움**(`to_regnamespace` → `None`) · 체크포인터 표를 쓰면 **`SET search_path TO <제 이름 공간>`**(`public`에 두면 다시 실행할 때 줄 수가 쌓이고 이름 공간 백업에 안 듦 — 05 b7·노트북 밖 `e2_public.py`) · 복원 DB를 쓰면 제 이름(예 `ch31_practice_restore`)을 처음에 `DROP DATABASE IF EXISTS`, 붙은 연결을 모두 닫은 뒤 끝에서 지움(`DROP DATABASE`는 붙은 연결이 있으면 실패 — PostgreSQL 문서) · **05 끝 서버 상태**: 이름 공간 `public`만 · 확장 `plpgsql`·**`vector 0.8.1`(public — 05가 남김)** · DB `ch31_lab`·`postgres` · `public` 표 0.
5. **모델 요청 0 권장**(챕터 공통 3 — 01~05 모두 0) · 규격 §7-2 「3~5번」과 다름 → **강사 확인 대상**(Ch 23·24·30 선례) · 그래프는 「모델을 쓰지 않는 그래프」(이름 있는 노드 함수), 벡터는 손으로 정한 값(실행 전에 정했다는 것과 뜻을 밝힘) · 가짜 채팅 모델·정해 둔 답 클래스 금지.
6. **쓰면 안 되는 말**: 챕터 금지어(`/tmp/ch31-05/tools/ban33.py` — 04·05 판 그대로, 사라지면 `.cache/ch31-03/tools/ban33.py`) — 「트랜잭션」·「롤백」·「마이그레이션」은 괄호 원어·제목 인용만 · 「인덱스」 → 색인 · 「순차」(Ch 12 「순차 스캔」도 인용하지 않음) · 「스냅샷」·「재개」·「재실행」·「스키마」·「쿼리」·「세션」·「반환」·「경로」·「최대」·「결정적」·「지연」·「측정」·「검증」 · 사용자가 금지한 표현(과정 규칙)·평소에 쓰지 않는 문구 · 허용(거짓 양성): 「노드」(Ch 13 말)·「이벤트 루프」·「프로그램」의 「로그」 · 실습 절 제목 「DB와 상태 영속화 실습: …」의 「DB」는 제목에만(본문 첫 자리 「데이터베이스」) · 「강사 시연」 금지.
7. **소품(삽화)**: 비유 계열 「전화 교환대」 — 01~04 소품(위 §04 → §05 11) + **05 = 옅은 회색 금속 판 둘·구리색 둥근 자리(넷 + 구멍 없는 자리 하나 / 다섯)·짙은 회색 선 넷과 노란 초록 선 하나(끝은 가는 원통 금속)·판 아래 좁은 턱, 불 없음** → 06은 되풀이 금지. 효과 있었던 문구: 「Only these ten cords in the whole image」·「a plain flat gray patch with no hole」·「No lamps, no lights, no power outlets, no power plugs, no two-pin plugs, no loops, no coils」(1차 채택). 작업 조회 모델 표시 `nano_banana_2`(기록만). **거래 기록 마지막은 05의 2026-09-29T19:35:55.970604Z(잔액 2249)**. 금지 소품 목록(챕터 공통 「비유 계열」) 그대로.
8. **묶음 계약**: Part 7 `qa/check_bundle_execution.py` 27행 `smoke_sections`는 **Ch 31 03만** 실행 — **실습 절은 스크립트 수정 없이는 묶음 실행 검사 대상이 아님**(스크립트 수정 금지 — 넣으려면 마감 후보로 기록) · 03 코드는 04·05가 건드리지 않음(03 `code_sha256` 그대로) · 실습 절이 도구 파일을 만들면 03은 가져오지 않는 편이 안전(Ch 28 01 선례) · 실습 절 노트북·도구 파일은 공개 목록 두 곳(`textbook/part7/public-files.json`·챕터 `qa/public-files.json`) → 묶음 다시 만들기는 마감.
9. **05에서 배운 실행 사실**: 설치 셀의 출력 조각 나눔 때문에 A·B `outputs_sha256`이 다를 수 있음(글자 대조로 판단 — 03·05) · `pg_restore`는 기본으로 오류를 넘기고 끝까지 가서 종료 코드 1과 끝 줄 오류 수를 냄(`--no-owner` 여부로 오류 수가 4 ↔ 5 — 인자를 바꾸면 출력이 바뀜) · `pg_restore --list` 원문 줄은 OID가 실행마다 바뀜(출력하지 말고 `in`으로) · `tempfile.mkdtemp` 폴더는 기기 셸 `TMPDIR`(`/sessions/…/tmp`, 여유 831M)에 쌓임 · psycopg `DROP … IF EXISTS`의 NOTICE는 셀 출력에 찍히지 않음(stderr 0) · `run_tool(["pg_dump", "--version"], None)`처럼 `--version`을 명령 바로 뒤에 두면 뒤에 서버 인자가 붙어도 버전만 찍음(05 출력 — 다른 자리는 시험하지 않음) · 한 셸 호출: 05 A 약 10초.
10. **시수·meta**: 실습 절 meta 「실습 30분 · 새 용어 0」(챕터 시수 5·11h에 더하지 않음 — 01~05 meta 강의 1·1·1·1·1·실습 2·2·2·2·3 그대로, 05는 「강의 1h | 실습 3h | … | 새 용어 3」) · `chapter.json`에 절 추가(`format: experiment`) · Part 7 `_build_index.py`(절 수 검사 없음 — 자동)·`textbook/_notebook/build_index.py` 66행 절 수 5(과정 약속 — 마감) · 04·05 b8처럼 굵은 라벨이 붙은 다음 절 문장은 70자를 넘기 쉬움(둘로 나눔).
11. **05 문장과 맞출 것**: 05 정리 끝·b8의 06 문장(위 1) · 05 b7·복습은 06을 가리키지 않음 · 05의 `RUNS_SENTENCE`(셀 서른하나 모두 같음)는 그대로.
12. **실행·기록 차례(01~05와 같음)**: 노트북 밖 5번(값이 결정적인지) → `/tmp` 사본(`/tmp/ch31-05/tools/runcopy.sh <사본> <커널 작업 폴더>` — 없으면 `.cache/ch31-03/tools/runcopy.sh`, 훅 source 포함) → A(`env -u OPENAI_API_KEY PYTHONDONTWRITEBYTECODE=1 timeout 170 bash textbook/_notebook/upgrade/run_section.sh textbook/part7/ch31-database 06`) → B(그림 전, `--cwd labs/part7/ch31-database/notebooks`) → 셀별 대조(`cmpout.py`·`dump3.py`) → 설계표 → `.mmd`·캡션(첫 렌더에서 긴 코드 라벨이 자동 줄바꿈 — `<br>`로 미리) → 직접 렌더 PNG 확인(`PUPPETEER_CACHE_DIR=/tmp/pptr-cache LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu python3 textbook/_notebook/mermaid/render_mermaid.py … --only 06-`, 다른 이름 사본으로 stage) → 삽화 → `--src-only` → `--no-exec`(G5 결과 읽기 첫 단락 인용은 출력이 생긴 뒤 다시 확인 — 05에서 다섯) · 끝낸 뒤 postgres 프로세스 0·55431 포트 0 · 실습 폴더 17개 해시(`/tmp/ch31-03/lab-before.sha` — 05 끝에도 17/17 같음) · 보호 파일 대조(`manifest-changes.md` — 05 뒤 값은 05 기록) · 치환 도구 `/tmp/ch31-05/tools/edit.py`(연결 폴더 사본 `.cache/ch31-05/tools/edit.py`).

## 실습 → 챕터 검토

**06절 `06-DB와-상태-영속화-실습`을 새로 만들었습니다**(2026-09-29). 제목은 「DB와 상태 영속화 실습: 상담 예약 그래프에서 처음 상담 시간 하나만 바꾸기」이고 `chapter.json`에 `format: experiment`로 더했습니다(`hours` 「총 16h · 강의 5h · 실습 11h」 그대로 — 실습 절 30분은 더하지 않음, `objectives`는 마감 몫). 설계는 `qa/upgrade/06-design.md`(노트북 전), 기록은 `qa/upgrade/06-diagnosis.md`, 그림 설계표는 `qa/upgrade/06-figures.md`(렌더 전), 검토 묶음은 `qa/upgrade/review-pack/06-DB와-상태-영속화-실습.md`.

### 1. 이 절이 한 것

- **슬러그**: `06-DB와-상태-영속화-실습` — 선례(`06-MCP-실습`·`05-Agent-평가-실습`·`10-FastAPI-서빙-실습`)가 모두 제목 앞말과 같고, 챕터 짧은 이름은 `textbook/_notebook/build_index.py` 66행 「DB와 상태 영속화」(인계 §05 → 실습 절 6의 제목과 같음). 준비 노트 후보 `06-DB-실습`은 쓰지 않음 — 강사 확인.
- **주제**: 상담실 하루의 상담 시간 안에서 문의 셋(01절 표 `requests`와 같은 번호·이름 — 1 환불 10분 · 2 배송 30분 · 3 결제 10분, 분은 이 절에서 실행 전에 정함)이 차례로 예약을 신청하는 **모델을 쓰지 않는 그래프 하나**(노드 `book`).
- **붙인 앞 절 기능 셋 — 모두 실행 1·2 흐름 안에서 쓰임**: **02** 한 묶음 작업(노드 `book_inquiry`의 `begin()` 블록 하나 — 예약 줄 `INSERT` + 상담 시간 `UPDATE`, `CHECK (minutes >= 0)` 위반 `IntegrityError`를 받아 `error.orig.sqlstate` 출력·`{"booked": 0}`) · **04** 작은 연결 풀(동기 엔진 `pool_size=1, max_overflow=0, pool_timeout=0.2` — 오류로 끝난 블록도 반납해야 다음 문의가 연결을 받음, `checkedout()`·`status()`) · **05** 체크포인터(따로 연 psycopg 연결 `autocommit=True`·`dict_row`·`SET search_path TO ch31_practice`·`setup()`·스레드 = 문의 이름·`get_state`·연결을 닫고 새 연결로 다시 컴파일해 읽기). 받쳐 주는 것: 01 이름 공간 지우고 만들기·`to_regnamespace`·`checkedin()` · 03 동기 엔진·설정 셀(**03 2절 셀 글자 그대로 — 생성기 대조**)·`array_agg(… ORDER BY …)`. 이 절이 노트북에 적은 함수 넷: 노드 `book_inquiry(state)` · 조립 `open_day(start_minutes)`(이름 공간을 지우고 다시 만들어 두 표·처음 상담 시간 한 줄 + `setup()`) · 기록 장치 `read_tables()` · `send_inquiry(inquiry)`.
- **동기만 쓴 까닭**(1절·b3 문장): 그래프를 `invoke`로 부르고 `PostgresSaver`가 psycopg 동기 연결을 쓰므로 노드 안의 한 묶음 작업도 03처럼 동기 엔진. `AsyncPostgresSaver`·`await` 노드는 01~05가 실행하지 않은 새 API라 쓰지 않음.
- **바꾼 값 하나**: 처음 상담 시간 `first_start = 50` → **`second_start = 30`**. 02·04의 값 바꿔 보기(보낼 금액·대기 제한)와 다른 값. 02 After의 취소 모양이 둘째 문의에서 다시 나오므로 **b2·노트북 6절 「새로 볼 것」은 실행이 보인 만큼만**(Ch 26 05 B-7): 한 문의만 취소되고 흐름이 이어짐 · 풀 크기 1인데 다음 문의가 연결을 받음 · 취소된 문의의 상태도 저장 · 새 연결로도 같은 상태.
- **뺀 것과 까닭**(b3 한 단락 + 진단): 01 `gather` · 03 Alembic(표 구조를 바꾸는 흐름 아님, 판 파일 사본·환경 변수·파일 위치 셀이 더해짐, 03은 묶음 실행 검사 절) · 05 pgvector 색인·백업·복원(검색·백업 명령이 더해지고 05 실험 되풀이) · 04 대기 제한 바꾸기.
- **새 문법·새 API·새 말 0**(`/tmp/ch31-06/tools/astdiff.py` — 01~05 노트북 코드 셀과 대조, 내장 이름·속성·키워드 인자·노드 종류·가져온 이름 새것 0 · 상태 형식 칸은 `int`만 — 01~05가 `str`·`bool`을 쓰지 않음 · 01~05 함수 이름 열넷 다시 정의 0 — 생성기 확인). 「취소」는 02 뜻으로만, 「판 내리기」·「표 구조」 말은 쓰지 않음 · 「창구」(과정 금지어) 대신 「상담실 하루」.
- 코드 셀 **23**(준비 둘 + 설정·체크포인터 접속 글·엔진·표 SQL 글·문의 하나의 SQL 글·문의 셋·체크포인터·상태 형식·노드·그래프·`open_day`·`read_tables`·`send_inquiry`·실행 1 둘·실행 2 둘·풀 상태·두 실행 표·새 연결로 읽기·정리), 준비 셀 밖 셀 최대 9줄, 함수 본문 최대 8줄(`book_inquiry`), 호출 깊이 최대 2, 코드 줄 130, 검사 문장 382. meta 「실습 30분 · 새 용어 0」. Mermaid 3(조립도·실행 1 실제 차례·실행 1·2 비교) + 삽화 1(「전화 교환대」 — 검은 틀 하나에 청록·테라코타·옅은 노랑 판 셋). **모델 요청 0.**

### 2. 실행으로 확인한 값 (노트북 밖 5/5 `e2_cells.py` md5 `7cdaba06…` + 저장 노트북 셀 `e4_fromcells.py` 5/5 md5 `ec8c15b4…`·stderr 0 + 새 커널 A 20:10:04Z · B 20:10:13Z 23/23 같음·`outputs_sha256` 같음 + 묶음을 풀어 실행 23/23 같음 — 챕터 요약이 인용할 수 있는 값)

- 설정 `드라이버 부분: postgresql+psycopg`·`서버 주소와 데이터베이스: 127.0.0.1:55431/ch31_lab` · 체크포인터 글 `postgresql`·`같은 서버와 데이터베이스인가: True` · `풀에 둘 연결 수: 1`·`대기 제한(초): 0.2`·`빌려 간 연결 수: 0` · 표 SQL `CREATE TABLE ch31_practice.schedule (minutes int CHECK (minutes >= 0))`·`CREATE TABLE ch31_practice.bookings (no int PRIMARY KEY)` · 문의 셋 `1 | 환불 | 10`·`2 | 배송 | 30`·`3 | 결제 | 10` · `체크포인터의 종류: PostgresSaver`·`붙은 체크포인터의 종류: PostgresSaver`.
- 실행 1(50분): `문의마다 남긴 예약 줄 수: [1, 1, 1]` · `표에서 읽은 값: {'남은 상담 시간(분)': 0, '예약된 문의 번호': [1, 2, 3], '체크포인트 줄 수': 9}` · `빌려 간 연결 수: 0` · `배송 문의의 저장된 상태: {'no': 2, 'minutes': 30, 'booked': 1}`.
- 실행 2(30분): `문의 2 받은 오류: IntegrityError 23514`(노드가 출력) · `[1, 0, 1]` · `{'남은 상담 시간(분)': 10, '예약된 문의 번호': [1, 3], '체크포인트 줄 수': 9}` · `빌려 간 연결 수: 0` · `{'no': 2, 'minutes': 30, 'booked': 0}` · 풀 상태 `Pool size: 1  Connections in pool: 1 Current Overflow: 0 Current Checked out connections: 0`(04 After와 같은 글).
- 표 `실행 1 | 50 | [1, 1, 1] | … | 0` · `실행 2 | 30 | [1, 0, 1] | … | 0` · `새 연결로 읽은 배송 문의의 상태: {'no': 2, 'minutes': 30, 'booked': 0}` · `남은 이름 공간: None`·`풀에 쉬고 있는 연결 수: 0`. 흔들리는 값 없음.
- 노트북 밖 반납 확인(`e3_leak.py` 2/2): 같은 동기 엔진에서 연결 하나를 닫지 않으면 다음 `begin()` 블록 `TimeoutError`(`QueuePool limit of size 1 overflow 0 reached, connection timed out, timeout 0.20`) · 풀 종류 `QueuePool` · `CHECK` 위반으로 끝난 블록 뒤 빌려 간 연결 0 — b6·b7에 「노트북 밖에서」로만.
- `code_sha256` **`bb245f74e6577cf881a5dc9f1eea2432b3b7c74f759ab963b8d14144de92728e`** · `outputs_sha256` **`139e24d3c384b0ae1f35f979dde3f03427268e56a2d5aa455c18b35ccb7e9099`** · 노트북 파일 `2bdbfbd1…`(그림 첨부·설명 고침 뒤).

### 3. 함께 고친 파일 (검토자가 볼 곳)

**챕터 안**
- `chapter.json` — 06절 추가(`2f4ce4ae` → `75549502`, 들여쓰기 2 — 원래 모양). **`hours`·`objectives` 그대로**.
- 새 파일: `_src/06-DB와-상태-영속화-실습.html`(`98c4ad60…`) · 빌드 `06-DB와-상태-영속화-실습.html`(`a2ecfab5…`, `{{`·`[[` 0건) · `figures/06-1`~`06-3`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`) · `figures/06-4-세-판을-한-틀에-끼운-교환대.{png,prompt.md,caption.md}` · `qa/upgrade/author_06.py`(`fa0bfd3c…`) · `06-design.md`·`06-figures.md`·`06-diagnosis.md` · `gates-wip-06-06.json`·`gates-wip-06.json`·`gates-wip-ch31-after06.json` · `review-pack/06-…md`(05 묶음도 다시).
- 챕터 `index.html`(`_build.py`가 06절 줄을 더함, `815dcc96` → `d9cc74a2`) · 01~04 HTML은 다시 썼지만 해시 같음.
- **05절 마지막 문장**: 05 b8 「다음 학습과 이어지는 지점」 → 「<a href="06-DB와-상태-영속화-실습.html">06절</a>은 이 챕터의 실습 절입니다. 02절 한 묶음 작업, 04절 작은 연결 풀, 05절 체크포인터를 상담 예약 그래프 하나로 이어 실행합니다」 · 노트북 정리 끝도 같은 두 문장(링크 없이). `mdpatch.py … 05` → `author_05.py --src-only`(바이트 같음) → `run_section.sh … 05 --no-exec`(05 게이트 0, 검사 문장 510). **05 노트북 `code_sha256` `6269536315f3…`·`outputs_sha256` `8bac96cd5e64…`·`executed_at` 19:32:40Z 그대로**(바뀐 셀은 마지막 마크다운 셀 하나, 생성기 `cells()`와 65/65 같음). 05 노트북 `bc3a68a1` → `09471344` · `_src/05` `8e2423a7` → `604080c9` · 05 HTML `057b0e2f` → `da333b53` · `author_05.py` `42cd35c9` → `5e83dfb1`.
- 챕터 `qa/public-files.json` — 06 HTML·06 노트북 두 줄(`dd039b3a` → `51fc1808`, 26줄 — 이 챕터 목록은 절 HTML도 적는 모양).
- `집필점검표.md` 품질 개선 표 06 행(`e542a3b6` → `a5df89a2`) · `qa/verification.md` 「품질 개선 06절」(`8cd5a312` → `b2781c08`) · `qa/upgrade/manifest-changes.md` 「06절 뒤」 · 이 파일 맨 위 한 줄과 이 절.
- **고치지 않음**: `author_01~04.py`·01~04 노트북·`_src` · 훅 `pre_exec.sh`(`dd564645…`) · 옛 생성기 둘·옛 그림.

**챕터 밖**
- `labs/part7/ch31-database/README.md` — 맨 아래 **06절 한 단락만**(`a54f0fd5` → `bd99e26b`). 옛 본문은 마감 몫.
- `textbook/part7/public-files.json` — `collect_public_files.py` → 06 노트북 한 줄(`12565fee` → `d822ee88`, 112줄, `Explicit public files: 110; prerequisites: 1`) · `prerequisite-files.json` 바이트 같음(`8d57bb0f`).
- **`textbook/part7/_build_index.py`**(목차·zip·`qa/integration-results.json`을 한 번에 다시 만듦) 두 번 실행 — 첫째는 목차 갱신, 둘째는 06 노트북 설명 고침 뒤 묶음을 디스크와 맞추려고: `Part 7: 31 verified sections; 111 bundled files` · `textbook/part7/index.html` `f5e86b4a` → **`bfea1c9a`**(Ch 31 「강의 5시간 · 실습 11시간 · 6절」·Part 「Ch 30–34 · 31절 · 총 88시간」 — 88시간 손 글 그대로) · `textbook/downloads/part7-practice.zip` `007f1387` → (`f3637bd8`) → **`b5dac376866de5bd5bb9f728a8291b70677ac642f028c3b95cc9e863c3e22cdb`**(114항목·111파일, `__pycache__`·`.pyc`·`.venv`·`.pytest_cache` 0, Ch 31 항목 17개가 디스크와 같음 — **중간 판**) · `integration-results.json` `70f89984` → `e231a76c`(`sections` 31·`code_cells` 448). 묶음을 풀어 06 노트북을 학생 자리(`notebooks/` 커널)에서 실행 → PASS 23셀·A와 23/23 같음.
- `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json` — `verify.py --chapter`가 다시 씀(`f73ca7c2` → `089e8b84`).
- **고치지 않음**: `check_bundle_execution.py`(27행 `smoke_sections`가 Ch 31 **03만** — 실습 절을 넣으려면 수정 필요, 후보로만 기록) · `bundle-execution.json`(옛 값) · `check_delivery.py`·`visual.cjs`·`check_figures.py`(실행 안 함 — 마감 몫) · `textbook/_notebook/build_index.py`(66행 Ch 31 절 수 5 — 실습 절을 빼고 세는 과정 약속) · `textbook/part7/_build_index.py` 21행 Ch 31 설명 · `labs/part7/continuity-guide.md` · 공용 도구·규격·과정 문서 · Ch 32~34 파일 · claude.ai 프로젝트 문서.

### 4. 검사 결과

- `run_section.sh … 06 --no-exec`: 게이트 G1~G7 **0**(챕터 전체 `gates-wip-ch31-after06.json` **6/6 PASS**), `verify.py --chapter` **`PASS 6 sections / 150 code cells (max 14 lines)`**, 빌드 HTML `{{`·`[[` 0건, SVG 셋·삽화 하나. 05 `--no-exec` 게이트 0.
- AST(`astdiff.py` 새것 0 · `extra_check.py` 걸린 것 TypedDict·노드 `try`뿐·깊이 2) · 금지어(`ban33.py` — 「노드」(허용)·「열」(동사 「열다」)뿐, `twoword33.py` 0) · 인용 대조(이름·명령뿐) · 생성기 대조(06 `cells()` 49/49 · 05 65/65 같음, `--src-only` 바이트 같음) · 설정 셀 = 03 2절 셀 글자 그대로(생성기 `__main__` 확인).
- 실습 폴더 파일 17개 가운데 README만 바뀜(16개 sha256 전후 같음 — `/tmp/ch31-03/lab-before.sha`) · 새로 생긴 파일은 06 노트북뿐 · pyc 0 · `.failure.json` 0 · 서버에 남긴 것 0 · 끝낸 뒤 postgres 프로세스 0·55431 포트 0.
- 보호 파일 209개: **181 같음 · 28 바뀜 · 없어진 파일 0** = 05 뒤 값 14 그대로 + 이 절 14(여덟은 처음 바뀜: `chapter.json`·챕터 `index.html`·챕터 `qa/public-files.json`·실습 폴더 `README.md`·`part7/public-files.json`·`part7/index.html`·`part7-practice.zip`·`integration-results.json`) — `manifest-changes.md` 「06절 뒤」.
- 삽화 `06-4` **1차 job `16823452-429f-4f64-87a6-9b3988613d6e` 채택**, 2크레딧(거래 20:12:01.818588Z, 잔액 2249 → 2247), 저장 PNG ↔ 채택 job 픽셀 차이 0. 설계표는 렌더 전, 새 커널 두 번째 실행은 그림 전.
- 돌리지 않음(마감 몫): `check_bundle_execution.py` · `check_delivery.py` · `visual.cjs` · `check_figures.py`.

### 5. 챕터 마감 담당이 이어서 할 것 (준비 노트 §14 마감 몫 전부 + 01~05 진단의 마감 몫 + 06이 더한 것)

1. **옛 생성기 이동**: 01이 막은 `qa/author_ch31.py`(`79bf670c…`)·`figures/_gen_figures.py`(`34448715…`)를 `mv -n` → `qa/upgrade/before/generators/blocked/` — **Part 7 `qa/check_figures.py` 20행이 `figures/_gen_figures.py`를 봄** → 옮기기 전에 그 검사와의 충돌을 먼저 판단(Ch 30 마감 선례) · `.moai` part7 스크립트 셋은 Ch 30 01이 막은 판 그대로(처분은 사용자·강사, 실행 금지).
2. **실습 폴더 README 다시 쓰기 전체**(지금은 옛 본문 + 06 한 단락): `.env`의 `CH31_DATABASE_URL` 문장(노트북은 `.env`를 읽지 않음 — 거짓) · `docker run … -p 55431:5432` → **`-p 127.0.0.1:55431:5432`**(01 노트북 준비물 글 그대로, `-e POSTGRES_USER=postgres` 포함) · `uv sync --project …` → 실습 폴더에서 **`uv sync --locked`** → `.venv` 커널 → `notebooks/`에서 열기 · 절마다 이름 공간(`ch31_async`·`ch31_tx`·`ch31_migration`·`ch31_shared`·**`ch31_practice`**)과 05의 복원 DB `ch31_restore` · 모델 요청 0·키 없음 · 05 백업 명령(이 컴퓨터의 `pg_dump` 17 이상 ↔ 컨테이너 안 `docker exec -i` 두 갈래, 확장 `vector`를 남김) · `python -m app.service`(프로젝트 맨 위에서 실패 — 실행 자리) · 「스키마」·「롤백」·「트랜잭션」 말 · 끄는 명령 · dev 그룹 **`pip==25.2`**(과정 `26.2` — `%pip` 셀은 바꾸지 않았으니 잠금을 고칠지 판단, 고치면 `uv lock` → `uv sync --locked` → 묶음).
3. **실습 폴더 파일 판단**: 03 첫 판 파일 설명 글 「상담 티켓 표 구조를 변경합니다」(실제로는 표를 만듦 — 03 출력에 찍힘, 고치면 03 출력·묶음 실행 검사 해시가 바뀜) · `migrations/env.py` 35행 조건 표현식·반환 힌트·`from __future__`(Ch 28 A-17 선례 대상인지) · `app/db.py`·`migrations/env.py` 기본 접속 글 `localhost`.
4. **`chapter.json`**: `objectives` 셋(「작업 경계를 설계」·「실제 환경에서 재현하고 대응」·「논리 백업 범위」 — 절 본문 말과 대조) + **06 실습 줄을 넣을지** · 제목 `&` → `_build.py`로 챕터 `index.html` · `textbook/part7/_build_index.py` 21행 Ch 31 설명(「트랜잭션·연결 풀·마이그레이션」 — 본문 말 「한 묶음 작업」·「표 구조 바꾸기」와 대조) · `textbook/_notebook/build_index.py` 67행 설명(66행 절 수 5는 약속대로 그대로)과 `textbook/index.html` Ch 31 행.
5. **01 제목 셀 문장** 「이 챕터의 다섯 절은 Docker 컨테이너 `kdt-ch31-postgres` 하나를 함께 씁니다」 — 06도 같은 컨테이너를 쓰므로 「여섯 절」로 고칠지(01은 모델 없음·출력 결정적 → `mdpatch.py … 01` + `--no-exec`, 다시 실행 불필요). 01~05 진단 강사 확인 대상과 함께 강사에게.
6. **묶음**: README·`objectives`·목차 설명을 고친 뒤 `python3 -B textbook/part7/_build_index.py`를 **마지막에 한 번 더**(이 절이 만든 zip `b5dac376…`은 중간 판) → 묶음을 풀어 03·06 준비 셀 확인(DB 켠 채) → Part 7 **`check_bundle_execution.py`는 실행기가 이 챕터 맥 `.venv`(32행)라 기기에서 그대로 못 돎** → 사본으로 손 대조 → 새 `bundle-execution.json`(Ch 31 03 옛 `b0594f2d…` → 지금 03 `code_sha256` `f97cba07…`)·zip 해시를 챕터 요약·계약 파일에. **실습 절 06(키 없음·DB만 필요)은 묶음 실행 검사 목록 후보**(27행 `smoke_sections` 수정 — 강사·마감 판단).
7. **검사**: `check_figures.py`(옛 그림 짝·`_gen_figures.py` 요구 — 옛 그림을 옮기면 멈춤) · `check_delivery.py`(`existing-artifacts-before.json`에서 멈출 것으로 예상 — Ch 30 기록) · `visual.cjs`(1280px·390px, G8)를 01~06 HTML·챕터 `index.html`·Part 7 `index.html`에 한 번에.
8. **옛 그림 15개**(`figures/0N-흐름.{svg,excalidraw,caption.md}` N=1~5, 사본 `before/figures/`, 공개 목록 줄 없음, 본문 참조 0) 삭제 승인 목록 — `check_figures.py`와 함께 판단.
9. **기록**: `qa/research.md`·`qa/verification.md`·`집필점검표.md` 머리에 「개선 전 판」 표시(지금은 끝에 품질 개선 절만) · `labs/part7/continuity-guide.md` 8~9행(Ch 31 「데이터·체크포인트 저장」·「트랜잭션·연결 풀·인덱스」 — 내용은 참, 말은 「인덱스」) · **챕터 요약 `chapter-summary.md`**(용어 표·문법 범위·DB 준비 방식(학생 컨테이너 ↔ 작업 기기 훅)·모델 0·실습 절 결과와 「실습 30분은 시수에 더하지 않음」·강사 확인 모음 01~06·뒤 챕터 인계).
10. **뒤 챕터 인계 대조**(고치지 않음): Ch 32 04 b3 「Ch31에서는 PostgreSQL, 트랜잭션, 인덱스와 pgvector를 배웁니다」(02 한 묶음 작업·05 색인·pgvector — 참, 말만 다름) · 06 b8 「Ch 32 04절은 Compose로 서비스와 PostgreSQL·pgvector를 함께 띄웁니다」(Ch 32 `chapter.json` 04절 제목·objectives로 확인 — Ch 32가 바뀌면 다시 대조).
11. **삭제 승인 대상**(지우지 않음): 실습 폴더 `.venv`(맥 217MB — 묶음 실행 검사 실행기와 묶임)·`app/__pycache__`·`migrations/**/__pycache__`(맥 pyc 여섯) · `.cache/vm/venv-ch31-database`(349MB)·**`.cache/vm/pgembed-try`(204MB)** · 기기 `/tmp/ch31-prep`(109MB)·`/tmp/ch31-02`~`/tmp/ch31-06`·`/tmp/ch31-pg`(클러스터 — 지우면 다음 훅이 `initdb`부터) · 기기 셸 `TMPDIR`의 `ch31-03-*`·`ch31-05-*` 폴더(덤프·Alembic 사본) · 연결 폴더 `.cache/ch31-01`~`.cache/ch31-06`·`.cache/ch31-0N-view`(N=1~6)·`.cache/ch31-04/resume` · `qa/upgrade/gates-wip-*.json` · 옛 그림 15개(8).

### 6. Ch 34 작업자(와 뒤에 Ch 32·33을 여는 작업자)가 전제하면 안 되는 것

- **Ch 31은 모델 요청 0**(01~06 모두 — 키 셀 없음, 실제 모델 비용·토큰 기록 없음). `runs/`·계약 파일 0 — 뒤 챕터가 읽을 산출 파일이 없습니다.
- **작업 기기 DB는 훅**(`qa/upgrade/pre_exec.sh` — pgenv PostgreSQL 17.11 + pgvector 0.8.1, 데이터 `/tmp/ch31-pg/data`, `127.0.0.1:55431`, 셸 호출이 끝나면 꺼짐)이고, **학생은 Docker 컨테이너 `kdt-ch31-postgres`**(`pgvector/pgvector:0.8.1-pg17`, `-p 127.0.0.1:55431:5432`, 연습용 비밀번호). 교재 출력은 Docker로 만들지 않았고, 05의 Docker 쪽 백업 갈래도 실행하지 않았습니다.
- 서버에 남기는 것은 05의 확장 `vector`(`ch31_lab`의 `public`)뿐 — 절마다 제 이름 공간·복원 DB를 지웁니다. Ch 32의 Compose 스택은 Ch 31 파일을 복사하지 않고 제 `init.sql`을 씁니다(Ch 32 04 b3).
- Ch 31은 **Ch 30 앱에 DB·체크포인터를 붙이지 않았습니다**(SSE 사건 저장 0) · 실습 폴더 `app/`는 노트북이 열지 않는 옛 코드 그대로(`localhost`·`.env` 기대).
- 비동기(asyncpg)는 01·02·04, 동기(psycopg)는 03·05·06. **ORM(`Mapped`)·`AsyncSession`·`async_sessionmaker`·`AsyncPostgresSaver`·노트북 `create_task`는 가르치지 않았습니다**(`gather`는 01만). 도구 파일 `db_tools.py` 없음.
- 실습 절에서 예약 표와 체크포인터 표는 **다른 연결로 확정된다는 사실만** 적었고, 두 표가 한 묶음 작업으로 함께 취소되는지 가르는 장면은 실행하지 않았습니다(함께 확정하는 설계는 다루지 않음). 취소된 문의의 상태가 남는 까닭은 「노드가 오류를 받아 `{"booked": 0}`을 내고 끝났고, 체크포인터는 노드가 끝난 뒤 적기 때문」입니다(마감 검토 B-5 — 설치판 langgraph `pregel/_runner.py` 207~221행·`_loop.py` 683~718행).
- 용어(이 파일 용어 표): 한 묶음 작업(트랜잭션)·확정(커밋)·**취소(롤백 — 02)** ↔ **판 내리기(03 제목의 롤백)** · 표 구조 바꾸기(마이그레이션 — Ch 21 04 옮기기와 다름)·판(리비전) · 연결 풀·빌려 간/쉬고 있는 연결·반납·대기 제한·이름 가림 · 백업·복원·덤프 파일 · 색인(「인덱스」 대신) · 패키지·서버 번호는 「버전」.
- Ch 33·34 `_src`에는 Ch 31 언급이 없습니다(2026-09-29 `grep`).

## 검토 반영과 챕터 마감 (2026-09-29)

**챕터 마감 끝남.** 요약은 `qa/upgrade/chapter-summary.md`(Ch 30 요약과 같은 목차 — 22절). 아래는 절 사이 인계로서 남길 것만 적습니다.

### 1. 한 것
- 검토 1차 A(01~03·공통 — 상 0·중 3·하 14)·B(04~06 — 상 1·중 2·하 6) 26건 가운데 **25건 반영**, 미반영 1건(A-14 03 짧은 셀 열둘 → 강사 확인). 건별은 요약 §21.
- **01만 다시 실행**(모델 없음): A-1 코드 주석 [11] 「닫히지 않고」 → 「서버와 끊기지 않은 채」 · A-15 출력 라벨 `데이터베이스와 서버 판:` → `버전:`. B(생성기 사본, `notebooks/` 커널)를 먼저, A(`run_section.sh`)를 뒤에 — 셀별 21개 가운데 19개 같음(걸린 초 두 셀), 교재 값 0.48·0.19는 새 A 출력과 같아 고칠 곳 없음. 01 `code_sha256` `addb4391…` → `1566ad038be4…`·`outputs_sha256` `145e0cf3…` → `f8a551e4d649…`.
- 02~06은 글(노트북 마크다운·`_src`)·`.mmd` 셋(03-2·03-3·06-3)·설계표(03·06)·캡션 넷(01-1·03-3·05-2·06-3)만 — **다섯 노트북 `code_sha256`·`outputs_sha256`·`executed_at` 전후 같음**(05 `6269536315f3…`/`8bac96cd5e64…`). 생성기 여섯을 문자열 치환으로 고치고 메모리 실행으로 노트북·`_src`와 대조(`.cache/ch31-close/tools/gapply31.py` — 코드 셀이 다르면 멈춤) → `run_section.sh … NN --no-exec`.
- **B-5 [상]**(06): 취소된 문의의 상태가 남는 까닭을 「노드가 오류를 받아 `{"booked": 0}`을 내고 끝났고, 체크포인터는 노드가 끝난 뒤 적음」으로(설치판 langgraph `pregel/_runner.py` 207~221행·`_loop.py` 683~718행 — 행 번호 마감 확인). 「다른 연결로 적기 때문」·「실행 2는 이 차이를 보여 줍니다」를 b4·b6·[40]·복습 4·b7·목표 3·정리에서 고침. 위 「실습 → 챕터 검토」 §6 줄도 고침.
- **B-3**(05): 덤프에 확장이 빠진 까닭 = `pg_dump`에 `--schema`를 주면 확장을 넣지 않음 — 마감이 노트북 밖에서 재현(`.cache/ch31-close/exp/b3_ext.sh`·`.out`). 위 「§04 → §05」 6번 괄호도 정정.
- 용어 표: 「연결 풀」 뜻(「서버와 끊지 않고」)·`error.orig`(A-6)·**「판」 ↔ 「버전」 가름**(A-15) 세 줄 고침.
- 실습 폴더 `README.md` 전체 다시 씀(`e6eba05a…`) · `chapter.json` `objectives` 여섯(`hours` 그대로) · Part 7 목차 스크립트·전체 목차 스크립트 Ch 31 설명(절 수 5 그대로)·`continuity-guide.md` 9행 · `part7-practice.zip` `6711c32a…`(마지막 한 번) · 훅 `pre_exec.sh` 주석 두 줄 「여섯 절」(`dd564645…` → `3a838c92…`, 주석 밖 같음) · 옛 생성기 둘 `qa/upgrade/before/generators/blocked/`로 `mv -n`(해시 같음).
- **실습 폴더 파일은 README만 고침**: 첫 판 파일 설명 글은 03 출력 [27]의 Alembic 진행 기록에 찍혀 조건 불충족 — 고치지 않음(A-17). `env.py`·`app/`도 그대로.
- 사용자가 금지한 표현(과정 규칙)이 글자 그대로 남아 있던 네 곳(`01-diagnosis.md` 15행·`05-diagnosis.md` 16행·이 파일 130행·273행 — 금지어 목록 줄)을 「사용자가 금지한 표현(과정 규칙)」으로.

### 2. 검사
- `gates-after.json` **6/6 PASS · G1~G7 0**(문장 2,560) · AST 따로 챕터 예외만 · `verify.py --chapter` **PASS 6 sections / 150 code cells (max 14 lines)** · `visual.cjs` **14행 PASS**(마감이 `/tmp/pw`·`/tmp/pw-browsers`를 다시 설치) · 빌드 HTML `{{`·`[[` 0 · 인용 대조 출력에 없는 출력 인용 0.
- **묶음 실행 검사는 손으로**: `check_bundle_execution.py` 32행 실행기가 이 챕터 맥 `.venv` → 새 zip을 `/tmp/ch31-close/bundle`에 풀어 Ch 31 가상환경으로 03·06을 키 없이·훅으로 DB를 켜고 실행(PASS 31·23셀, 저장 노트북과 셀별 출력 같음). `bundle-execution.json`은 옛 zip 기준 그대로(전체 마감).
- `check_delivery.py`는 `existing-artifacts-before.json`의 없는 파일에서 멈춤(알려진 일) — 그 대조와 `llm-practice.zip`을 뺀 사본 통과(절 31·코드 셀 448·깨진 링크 0·zip 111파일 = 디스크). `check_figures.py`는 20행 `_gen_figures.py` `assert`에서 **Ch 30 폴더로** 멈춤(알려진 충돌) — Ch 31만 도는 사본은 옮기기 전 PASS 5쌍. `check_secrets.py` PASS 178파일(결과 파일 되돌림).
- 보호 파일 209개: 같음 169 · 바뀜 38(마감에서 36) · 옮김 2 — `manifest-changes.md` 「마감 뒤」.

### 3. Ch 34 작업자에게 (요약 §18)
- **Ch 31은 모델 요청 0** — 비용·토큰·지연 기록이 없음. 작업 기기 DB는 훅, 학생은 Docker 컨테이너. Ch 32·33은 이번 품질 개선에서만 제외(과정에는 남음).
- 패키지·서버 번호는 「버전」, 「판」은 표 구조의 판(리비전)에만. 「취소」는 02 뜻(한 묶음 작업)으로만.
- Ch 32 04 b7 「연결 재시도·마이그레이션 동시 실행은 Ch31의 운영 설계와 함께」 — Ch 31은 둘 다 다루지 않음(Ch 32 개선 때 고칠 것, 요약 §19).

