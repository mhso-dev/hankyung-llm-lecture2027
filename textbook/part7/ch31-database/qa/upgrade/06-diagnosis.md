# 06절 진단 — DB와 상태 영속화 실습 (새 실습 절 · experiment)

- 작업일 2026-09-29 · 생성기 `qa/upgrade/author_06.py`(`fa0bfd3cef6f…`) · 노트북 `labs/part7/ch31-database/notebooks/06-DB와-상태-영속화-실습.ipynb`(`2bdbfbd1015f…`) · 본문 `_src/06-DB와-상태-영속화-실습.html`(`98c4ad60d32a…`) · 빌드 `06-DB와-상태-영속화-실습.html`(`a2ecfab51d8f…`) · 설계 `qa/upgrade/06-design.md`(노트북 전) · 그림 설계표 `qa/upgrade/06-figures.md`(렌더 전) · 검토 묶음 `qa/upgrade/review-pack/06-DB와-상태-영속화-실습.md`.
- 새로 만든 절이라 `qa/upgrade/before/`에 원본이 없습니다. DB 준비 훅 `qa/upgrade/pre_exec.sh`는 05 판 `dd564645…` 그대로(고치지 않음).
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(§7-2 먼저, 그다음 전부) · `handoff.md`(챕터 공통 전부·§05 → 실습 절 전부·나머지 인계 훑기) · `05-diagnosis.md`(전부)·`01~04-diagnosis.md`(강사 확인·마감 몫) · 준비 노트 `chapter-lead-notes.md` §11·§12·§13·§14·§15 · 생성기 `author_01.py`(설정·코드 셀)·`author_02.py`·`author_03.py`·`author_04.py`(코드 셀)·`author_05.py`(전부) · Ch 30 `author_10.py`(머리·도구 파일 사슬)·`10-design.md`·`review-round1-B.md`(B-1·B-3·B-14·B-15·B-16)·`handoff.md` 「실습 → 챕터 검토」 · `AGENT-BRIEF.md`·`PLAYBOOK.md`(§3 실습 절 포함 전부) · Ch 32 `chapter.json`·04 `_src` 「앞에서 배운 내용」(b8 문장 근거) · Ch 33·34 `_src`(Ch 31 언급 0) · `labs/part7/continuity-guide.md` 8~9행 · 실습 폴더 README · `textbook/_notebook/build_index.py`(66행 챕터 짧은 이름) · Part 7 `_build_index.py`·`collect_public_files.py`. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다. Ch 29 `author_05.py`·Ch 23·24 실습 절·Ch 26 05 검토·Ch 27 09 검토는 인계·규격에 옮겨 적힌 교훈(B-7 「새로 볼 것」은 실행이 보인 만큼 · 앞 절 용어를 다른 뜻으로 쓰지 않기 · 설계표는 렌더 전)으로 따랐고 파일을 따로 열지 않았습니다.

## 슬러그와 제목

- 슬러그 **`06-DB와-상태-영속화-실습`** — 선례 `06-MCP-실습`·`05-Agent-평가-실습`·`10-FastAPI-서빙-실습`은 모두 제목 앞말과 같음. 챕터 짧은 이름 = `textbook/_notebook/build_index.py` 66행 「DB와 상태 영속화」, 인계 §05 → 실습 절 6이 제목 「DB와 상태 영속화 실습: …」를 정함 → 슬러그도 그 앞말(`&`는 슬러그에 못 씀). 준비 노트 후보 `06-DB-실습`은 제목 앞말과 달라지고, `06-상태-영속화-실습`은 이름의 반쪽이라 뺌(`06-design.md` 머리).
- 제목 「DB와 상태 영속화 실습: 상담 예약 그래프에서 처음 상담 시간 하나만 바꾸기」 · `format: experiment` · meta 「실습 30분 · 코드 notebooks/06-….ipynb · 새 용어 0」 · `chapter.json` `hours` 「총 16h · 강의 5h · 실습 11h」 그대로(실습 절 30분은 더하지 않음, 01~05 meta 합은 그대로), `objectives`는 마감 몫.

## 게이트

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 첫 실행 전 생성기 대조(`/tmp/ch31-06/tools/pregate.py`) | 23 | 345 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| 첫 실행 전 `--label wip-06 --section 06`(`gates-wip-06-06.json`) | 23 | 345 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3(그림·설계표 없음) |
| 후(`gates-wip-06.json`, `--no-exec`) | **23** | **382** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

- 첫 생성기 대조에서 70자 넘는 문장 다섯(기준 버전 문장·Ch 32 문장·b2 DB 풀이·b3 붙인 기능·b10 첫 참고 자료)과 영어로 시작해 조사가 붙은 문장 하나(「CHECK는」) → 모두 나눔·앞말을 붙여 고친 뒤 0. 마지막 설명 고침(b6 「다음 블록은 …」) 뒤 `--no-exec`에서 70자 넘는 문장 하나를 다시 잡아 둘로 나눔.
- 챕터 전체 `gates-wip-ch31-after06.json` **6/6 PASS**(G1~G7 합 0).
- **AST 따로**: `/tmp/ch31-06/tools/astdiff.py`(이 절에서 만듦 — 01~05 노트북 코드 셀과 대조) **내장 이름·속성·키워드 인자·노드 종류·가져온 이름 새것 0**(06이 쓴 내장 이름 `int`·`print`·`type` — 01~05는 `TimeoutError`·`dict`·`int`·`issubclass`·`len`·`open`·`print`·`round`·`type`만 써서 상태 형식 칸은 `int`만, `str`·`bool`·`range` 0) · `extra_check.py`: 걸린 것은 상태 형식 `BookingState(TypedDict)`(`ClassDef`·`AnnAssign` 셋 — 규격 §2-2 L5·05와 같은 모양)와 노드의 `try`(03 `try_upgrade` 모양)뿐 · 호출 깊이 최대 2 · 준비 셀 밖 셀 최대 9줄 · 함수 본문 최대 8줄(`book_inquiry`) · 코드 줄 130 · f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`next`·`await`·`async`·데코레이터·힌트(상태 칸 말고)·기본값 매개변수·대입 풀기·별표 풀기·세미콜론·한 글자 이름·메서드 셋 이어 부르기 0. 01~05 함수 이름 열넷을 다시 정의하지 않는지 생성기 `__main__`에서 확인.
- **금지어**(`ban33.py` — 05 판 그대로): `_src`·노트북 마크다운·코드 주석·`.mmd` 셋·캡션 넷에서 남은 것은 「노드」(Ch 13 말 — 05와 같은 허용)와 「열」 넷(「하루를 열 때」 — 동사 「열다」, 칸 뜻 아님)뿐. `twoword33.py`(트랜잭션·롤백·커밋·마이그레이션·리비전·스키마·되돌·옮기) **0**. 사용자 금지 표현 0(생성기·노트북·`_src` `grep`). 과정 금지어 「창구」 때문에 상황 이름은 「상담실 하루」·「상담 예약」으로.
- **인용 대조**(`quotes.py`): 노트북 백틱 82개·`_src` `<code>` 65개 가운데 출력·코드에 없는 것은 명령·이름(`docker run`·`docker start …`·`uv sync --locked`·`.venv`·`notebooks/`·`requests`(01 표 이름)·`try_upgrade`·`restored_state`(03·05 함수)·`gather`·`QueuePool`·`conn.begin()`·`DROP SCHEMA … CASCADE`·`sqlalchemy.exc.TimeoutError`·설치판 소스 파일 이름)뿐.

## 설계 (자세한 것은 `06-design.md`)

- **상황**: 상담실 하루의 상담 시간(처음 상담 시간) 안에서 문의 셋(01절 표 `requests`와 같은 번호·이름 — 1 환불 · 2 배송 · 3 결제)이 차례로 예약을 신청. 문의마다 필요한 시간 10·30·10분과 두 처음 상담 시간 50·30분은 이 절에서 실행 전에 정한 값(노트북 출력 라벨 「실행 전에 정한 값」·b7).
- **붙인 기능 셋(모두 실행 1·2 흐름 안에서 씀)**: **02** 한 묶음 작업 — 노드 `book_inquiry`가 `begin()` 블록 하나에 예약 줄 넣기(`INSERT`) + 상담 시간 빼기(`UPDATE`), `CHECK (minutes >= 0)` 위반이면 `IntegrityError`를 받아 `error.orig.sqlstate` 출력·`{"booked": 0}` · **04** 작은 연결 풀 — 동기 엔진 `pool_size=1, max_overflow=0, pool_timeout=0.2`, 두 실행 뒤 `checkedout()`·`status()` · **05** 체크포인터 — 따로 연 psycopg 연결(`autocommit=True`·`dict_row`)·`SET search_path TO ch31_practice`·`setup()`·스레드 = 문의 이름·`get_state`·끝에 연결을 닫고 새 연결로 다시 컴파일해 읽기(05 6절 `restored_state` 모양, 같은 데이터베이스). 받쳐 주는 것: 01 이름 공간 지우고 만들기·`to_regnamespace`·`checkedin()` · 03 동기 엔진·설정 셀·`array_agg(… ORDER BY …)`.
- **실행 2 = 값 하나(처음 상담 시간 50 → 30)**: 02 값 바꿔 보기(보낼 금액)·04 값 바꿔 보기(대기 제한)와 다른 값. 02 After의 취소 모양이 실행 2 둘째 문의에서 다시 나오므로 b2 「새로 볼 것」은 실행이 보인 만큼만 — 한 문의만 취소되고 흐름이 이어짐 · 풀 크기 1인데 다음 문의가 연결을 받음(오류로 끝난 블록도 반납) · 취소된 문의의 상태도 저장(`booked` 0)·체크포인트 줄 수 두 실행 모두 9 · 새 연결로도 같은 상태.
- **뺀 것**(b3 한 단락): 01 `gather`(노드가 문의를 차례로 받음) · 03 Alembic(표 구조를 바꾸는 흐름이 아니고 판 파일 사본·환경 변수·파일 위치 셀이 더해짐, 03은 묶음 실행 검사 절) · 05 pgvector 색인·백업·복원(검색·백업 명령이 더해지고 05 확장 실험 되풀이) · 04 대기 제한 바꾸기.
- **동기만**: 그래프 `invoke` + `PostgresSaver`(psycopg 동기 연결) → 노드 안의 한 묶음 작업도 03처럼 동기 엔진 — 1절·b3에 까닭 문장. 드라이버 psycopg 하나, 접속 글 둘은 드라이버 표시만 다름(설정 셀 = 03 2절 셀 **글자 그대로** — 생성기 `__main__`이 `author_03.py` 글과 03 노트북 코드 셀에 대해 확인 · 체크포인터 글은 `replace("postgresql+psycopg://", "postgresql://")`로 만들고 서버 부분이 같은지 `True` 출력).
- **다시 실행해도 같게**: `open_day`가 실행마다 이름 공간 `ch31_practice`를 지우고 다시 만들고 `setup()`(체크포인터 표 넷 포함 — 실행 1·2가 섞이지 않음) · 끝 셀이 이름 공간을 지우고 `to_regnamespace` → `None`·`dispose()` → `0` · 체크포인터 연결 둘 모두 닫음 · 확장 `vector`(05가 남김)는 건드리지 않음 · 파일 쓰기 0(작업 폴더·임시 폴더).
- **모델 요청 0**(챕터 결정 M0 · 05 인계 5 · Ch 23·24·30 10 선례) — 규격 §7-2 「모델 호출 3~5번」과 다름 → 강사 확인. 그래프는 이름 있는 노드 함수 하나(모델을 쓰지 않는 그래프), 가짜 채팅 모델 0.
- **도구 파일 만들지 않음**: 이 절 함수 넷(`book_inquiry`·`open_day`·`read_tables`·`send_inquiry`)은 흐름을 잇는 새 함수이고, 01~05 함수는 다시 쓰지 않음(모두 그 절의 이름 공간·전역에 묶임) → 규격 §2-7 3의 대상 함수 없음, 챕터 공통 8(S1) 그대로 · 앞 노트북은 가져오게 바꾸지 않음.
- **흉내 낸 단계 없음**: `CHECK` 위반은 실제 서버가 막은 것 · 반납하지 않았을 때의 `TimeoutError`는 노트북에서 흉내 내지 않고 노트북 밖 확인(`e3_leak.py`)으로 b6·b7에만 「노트북 밖에서」로 적음(Ch 30 B-1 교훈).
- **말**: 새 용어 0 · 한 묶음 작업·확정·취소(02) · 연결 풀·빌려 간 연결·쉬고 있는 연결·반납·대기 제한(01·04) · 이름 공간(Ch 23 02) · 체크포인터·체크포인트·스레드·표 만들기 `setup()`(Ch 23) · 설계 객체·노드·엣지(05 이음) · 「취소」는 02 뜻(한 묶음 작업이 확정하지 않음)으로만, 「판」은 쓰지 않음(교환대 비유도 「판」을 쓰나 표 구조의 판 말은 이 절에 없음 — 비유 속 「판」은 교환대 판) · 패키지·서버 번호는 「버전」 · 제목의 DB·상태 영속화는 1절·b2 첫 자리에서 풂.
- **뒤 챕터 문장(Ch 30 B-3 교훈)**: b8·노트북 정리 끝 「다음 챕터 Ch 32는 Docker와 컨테이너를 다룹니다. 그 04절은 Compose로 서비스와 PostgreSQL·pgvector를 함께 띄웁니다」 — Ch 32 `chapter.json` 제목·04절 제목 「Compose와 pgvector 스택」·objectives 「Compose로 FastAPI, PostgreSQL, pgvector 스택을 실행」으로 확인한 사실만. Ch 32는 대기 챕터라 바뀌면 이 문장을 다시 대조.

## 실행 (새 커널)

- **노트북 밖 확인**(기기 `/tmp/ch31-06/exp/`, 가상환경 파이썬 · 훅으로 켠 서버 · 키 뺌 · `PYTHONDONTWRITEBYTECODE=1`): 탐색 `e1_flow.py` 1번(같은 흐름, 라벨·이름만 다름) → 설계 확인 `e2_cells.py`(계획한 코드 셀 스물하나) **5/5 md5 `7cdaba069fc4d0d4` 같음, stderr 0바이트**(19:57:27Z~30Z) → 반납 확인 `e3_leak.py` 2/2 md5 `03ef2afd22d294ea`(닫지 않은 연결 뒤 다음 `begin()` 블록 `TimeoutError` `QueuePool limit of size 1 overflow 0 reached, connection timed out, timeout 0.20`·풀 종류 `QueuePool` · `CHECK` 위반 `23514` 뒤 빌려 간 연결 0 · 이름 공간 `ch31_probe06`은 만들고 지움) → 저장 노트북 코드 셀(설치 셀 뺀 스물둘)을 이어 붙인 `e4_fromcells.py` **5/5 md5 `ec8c15b435a66229`, stderr 0, A 출력과 글자까지 같음**(20:10:23Z~26Z).
- 첫 실행 전 `/tmp/ch31-06/try/copy1.ipynb`를 `runcopy.sh`(훅 source + `execute.py --cwd` 프로젝트 맨 위)로 PASS 23셀 · 실습 폴더 `.failure.json` 0.
- **A**: `env -u OPENAI_API_KEY PYTHONDONTWRITEBYTECODE=1 timeout 170 bash run_section.sh textbook/part7/ch31-database 06` — 프로젝트 맨 위 커널, **`executed_at` 2026-09-29T20:10:04Z**, PASS 23셀(그림 첨부 단계에서 멈춤 — 06-1 PNG가 아직 없어서, 실행·저장은 끝난 뒤) · `code_sha256` **`bb245f74e6577cf881a5dc9f1eea2432b3b7c74f759ab963b8d14144de92728e`** · `outputs_sha256` **`139e24d3c384b0ae1f35f979dde3f03427268e56a2d5aa455c18b35ccb7e9099`**. 한 셸 호출 약 3초.
- **B**(그림 전): 저장 노트북 사본 `/tmp/ch31-06/runB/06B.ipynb`를 `--cwd labs/part7/ch31-database/notebooks`(학생 커널 자리) · `executed_at` 20:10:13Z · PASS 23셀 · **셀별 출력 23/23 같음 · `code_sha256`·`outputs_sha256` 모두 A와 같음**. 사본 시험 copy1도 23/23·두 해시 같음. 갈린 셀 0 → 결과 읽기에 `[[…]]` 자리 없음. 모든 셀 stderr 0.
- **묶음**: 다시 만든 `part7-practice.zip`(최종 `b5dac376…`)을 `/tmp/ch31-06/bundle2`에 풀어 06 노트북을 묶음의 `notebooks/`에서 키 없이 실행 → PASS 23셀·A와 23/23 같음(`outputs_sha256`은 설치 셀 출력 조각 나눔만 다름 — 03·05 선례). 첫 zip(`f3637bd8…`)으로도 같은 결과.
- 설명만 고친 뒤(`mdpatch.py` 두 번 — 오늘 볼 그림 alt·읽기의 왼쪽/오른쪽, 정리 셀의 확장 문장) 저장 노트북 `code_sha256`·`outputs_sha256`·`executed_at` 그대로 · 생성기 `cells()` 49셀과 저장 노트북 셀 소스 49개 모두 같음 · `src_html()`과 `_src` 같음(`--src-only` 바이트 대조).
- 모든 셸 호출 뒤 postgres 프로세스 0·55431 포트 0. 끝의 서버 상태: 이름 공간 `public`만 · 확장 `plpgsql`·`vector` · 데이터베이스 `ch31_lab`·`postgres`.

## 그림

- Mermaid **3장**(설계표 `06-figures.md`를 렌더 전에 씀, 번호 `06-1`부터): 06-1 세 절의 기능을 이은 조립도(b4 「실습 조립의 구성」 뒤·노트북 오늘 볼 그림, viewBox 폭 **462**) · 06-2 실행 1의 실제 차례(b5, **231**) · 06-3 처음 상담 시간만 바꾼 두 실행(b6, **625**). 모두 868 이하 · `flowchart TB` · subgraph 제목 `<br>` 없음 · 라벨 대괄호·따옴표·중괄호 없음 · 개수는 한글(셋·넷·아홉) · 노드 7개 이하 · 노드 id `call`·`end` 없음 · `%% classes`. 첫 렌더에서 자동 줄바꿈 0(긴 코드 이름을 미리 `<br>`로 나눔). PNG 셋을 다른 이름 사본(`.cache/ch31-06-view/r1-06-*.png`)으로 직접 열어 확인 — 06-1은 노드 쪽이 왼쪽·체크포인터 쪽이 오른쪽, 06-3은 실행 1 칸이 왼쪽 → alt·도식 읽기에 왼쪽/오른쪽을 적음. **보라 0 · 빨강 0**(받은 `IntegrityError` 상자도 노랑) · 바꾼 값(처음 상담 시간)은 셀에 적은 값이라 초록(오케스트레이터 지시 「질문·바꾼 값 초록」·챕터 약속 「셀에 적은 값 초록」 — 05-4는 바꾼 복원 방법을 파랑으로, 06-3 도식 읽기에 까닭 한 문장, Ch 30 B-15 교훈) · 06-3 맨 아래 노랑 공통 상자는 두 칸 출력에서 모두 확인한 값만(체크포인트 줄 아홉·빌려 간 연결 없음), 받은 오류 상자는 실행 2 칸에만 · 라벨 숫자는 출력에 있는 값만(중간 값 40분·20분 없음 — 20분은 b6 설명 문장에만 셈으로).
- 삽화 **06-4 세 판을 한 틀에 끼운 교환대**(b4 비유 뒤, 본문만): **1차 job `16823452-429f-4f64-87a6-9b3988613d6e` 채택**(재생성 0회). 거래 2026-09-29T20:12:01.818588Z 「Nano Banana Pro −2」 한 줄 = **이 절 몫 2크레딧**(잔액 2249 → 2247, 바로 앞 거래 19:35:55Z는 05). 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만). 원본 2752 × 1536 `b1c890f8…` · 저장 PNG 1100 × 614 `680ed6c7…`, 결과를 다시 받아 같은 폭으로 줄인 그림과 **픽셀 차이 0**(bbox `None`). 그림에서 센 것: 검은 금속 틀 하나 · 판 셋(청록·테라코타·옅은 노랑) · 왼쪽 자리 하나·흰 선 하나 · 가운데 자리 여섯(두 줄 세 칸) — 왼쪽·오른쪽 칸 위아래를 흰 선 하나씩, 가운데 칸 빔 · 오른쪽 회색 둥근 덮개 셋(위에 경첩 — 프롬프트의 「열려 늘어진」 모양이 아니라 닫힌 덮개로 그려져 그림 읽기·비유는 「덮개 셋이 있음」으로만 적음) · 흰 선 모두 셋 · 불·사람·손·글자·숫자·화살표·콘센트·전원 플러그 0. 거의 흰 가로줄 115/614(틀 위쪽 여백). 세부 `figures/06-4-…prompt.md`.

## 05절과 맞춘 것 (05 노트북은 다시 실행하지 않음)

- 05 b8 「다음 학습과 이어지는 지점」·05 노트북 정리 끝 → 06 슬러그 링크와 이 절 내용: b8 「<a href="06-DB와-상태-영속화-실습.html">06절</a>은 이 챕터의 실습 절입니다. 02절 한 묶음 작업, 04절 작은 연결 풀, 05절 체크포인터를 상담 예약 그래프 하나로 이어 실행합니다」 · 노트북 「06절은 이 챕터의 실습 절입니다.」+ 같은 둘째 문장. `mdpatch.py … 05`(생성기·노트북 마크다운·`_src` 함께) → `author_05.py --src-only`(바이트 같음) → `run_section.sh … 05 --no-exec`(05 게이트 0, 검사 문장 509 → 510).
- **05 노트북 `code_sha256` `6269536315f3…`·`outputs_sha256` `8bac96cd5e64…`·`executed_at` 2026-09-29T19:32:40Z 그대로**(다시 실행하지 않음 — 바뀐 셀은 마지막 마크다운 셀 하나, 생성기 `cells()`와 65/65 같음). 05 노트북 파일 `bc3a68a1…` → `09471344…` · `_src/05` `8e2423a7…` → `604080c9…` · 05 HTML `057b0e2f…` → `da333b53…`(06 빌드 때 꼬리말에 다음 절 링크, 05 `--no-exec` 때 b8 링크) · `author_05.py` `42cd35c9…` → `5e83dfb1…` · `gates-wip-05.json` 다시 씀 · review-pack 05 다시 묶음.

## 챕터 밖 수정 (모두 인계 지시 범위)

- `labs/part7/ch31-database/README.md` — 맨 아래 **06절 한 단락만**(`a54f0fd5…` → `bd99e26b…`). 옛 본문(`.env`·`-p 55431:5432`·`uv sync --project`·「스키마」·「롤백」)은 마감 몫으로 그대로.
- `textbook/part7/public-files.json` — `collect_public_files.py` → 06 노트북 한 줄(`12565fee…` → `d822ee88…`, 112줄, `Explicit public files: 110; prerequisites: 1`) · `prerequisite-files.json` 바이트 같음(`8d57bb0f…`).
- `textbook/part7/_build_index.py` 실행 **두 번**(목차 갱신 · 두 번째는 06 노트북 설명 고침 뒤 묶음을 디스크와 맞추려고): `Part 7: 31 verified sections; 111 bundled files` · `textbook/part7/index.html` `f5e86b4a…` → **`bfea1c9a…`**(Ch 31 「강의 5시간 · 실습 11시간 · 6절」·Part 「Ch 30–34 · 31절 · 총 88시간」 — 88시간 손 글 그대로) · `textbook/downloads/part7-practice.zip` `007f1387…` → (첫 `f3637bd8…`) → **`b5dac376866de5bd5bb9f728a8291b70677ac642f028c3b95cc9e863c3e22cdb`**(114항목·111파일, `__pycache__`·`.pyc`·`.venv`·`.pytest_cache` 0, Ch 31 항목 17개가 디스크와 같음 — **중간 판, 최종 zip은 마감**) · `qa/integration-results.json` `70f89984…` → `e231a76c…`(`sections` 31·`code_cells` 448).
- `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json` — `verify.py --chapter`가 다시 씀(`f73ca7c2…` → `089e8b84…`).
- **고치지 않음**: `check_bundle_execution.py`(Ch 31 03만 실행 — 실습 절을 넣으려면 스크립트 수정, 후보로만 기록) · `bundle-execution.json` · `check_delivery.py`·`visual.cjs`·`check_figures.py`(마감 몫) · `textbook/_notebook/build_index.py`(66행 Ch 31 절 수 5 — 과정 약속) · `_build_index.py` 21행 Ch 31 설명(마감) · 공용 도구·규격·과정 문서 · 01~04 노트북·`_src`·생성기 · 훅 · 실습 폴더 `app/`·`migrations/`·`alembic.ini`·잠금 · Ch 32~34 파일 · claude.ai 프로젝트 문서.

## 강사 확인 대상

1. **모델 요청 0**인 실습 절(규격 §7-2 「모델 호출 3~5번」과 다름 — 챕터 결정 M0, Ch 23·24·30 선례).
2. 슬러그 `06-DB와-상태-영속화-실습`(제목 앞말) — 준비 노트 후보 `06-DB-실습`을 쓰지 않음.
3. 붙인 기능 셋(02·04·05)과 뺀 것(01 `gather`·03 Alembic·05 색인·백업·복원) · 바꾼 값 = 처음 상담 시간.
4. 비동기 절(01·02·04)의 기능을 동기 엔진으로 적음(그래프 `invoke`·`PostgresSaver` 때문 — `AsyncPostgresSaver`는 01~05가 실행하지 않은 새 API).
5. 삽화 오른쪽 판의 덮개가 프롬프트(열려 늘어진 덮개)와 달리 닫힌 모양 — 비유 글은 개수만 짚음 · 위쪽 흰 여백 약 5분의 1(재생성 한도 1회를 쓰지 않고 채택).
6. 코드 양: 코드 셀 23(준비 둘 포함), 코드 줄 130, 함수 넷 — 30분 분량인지.

## 남은 것 (마감 몫 — handoff 「실습 → 챕터 검토」 5에 전부)

- `chapter.json` `objectives`(06 줄을 넣을지 포함) · 실습 폴더 README 다시 쓰기 · zip 최종판·묶음 실행 검사 · `check_figures.py`·`check_delivery.py`·`visual.cjs` · 옛 생성기 이동 · 옛 그림·임시 폴더 삭제 승인 · 01 제목 셀 「이 챕터의 다섯 절은 Docker 컨테이너 하나를 함께 씁니다」(06도 같은 컨테이너 — 「여섯 절」로 고칠지).

## 지우지 않은 것 (삭제 승인 대상 — 이 절이 만든 것)

- 기기 `/tmp/ch31-06/`(약 16MB — `tools/`(05 도구 사본 + `astdiff.py`)·`exp/`(`e1_flow.py`·`e2_cells.py`·`e3_leak.py`·`e4_fromcells.py`와 출력)·`gen/`(생성기 조각 셋·`all.py`·치환 JSON)·`pre/`·`try/`·`runA/`·`runB/`·`bundle/`·`bundle2/`(zip 푼 폴더 둘)·`illu/`(원본 PNG 둘·1100 사본)·`05-before.sha`·`05-src-after-mdpatch.html`·`06-src-after-m2.html`) · 연결 폴더 `.cache/ch31-06/`(도구·확인 스크립트 사본, 116K)·`.cache/ch31-06-view/`(PNG 넷, 872K) · `qa/upgrade/gates-wip-06-06.json`·`gates-wip-06.json`·`gates-wip-ch31-after06.json`.
- 운영체제 임시 폴더: 이 절은 쓰지 않음(`TMPDIR`에 `ch31-06` 0).
- 서버: 이 절이 남긴 것 0(이름 공간 `ch31_practice`·`ch31_probe06` 모두 지움).

## 작업 기록 — 잘못 들어간 명령 하나

- zip 두 번째 검사 셸 명령 가운데에 `rm -rf /dev/null 2>/dev/null`이 잘못 들어갔습니다(뜻한 명령 아님). 바로 확인하니 `/dev/null`은 그대로(문자 장치 `1, 3`, 16:07 만든 것)였고 쓰기도 됐습니다 — 지워진 것 0. 삭제 금지 지시와 어긋나는 명령이라 적어 둡니다.

## 디스크

- 기기 루트 여유: 작업 전 **1.9G** → 끝 **1.9G**(`/tmp/ch31-06` 16MB) · 세션 디스크(`/sessions`, `TMPDIR`) 831M → 831M · 사용자 디스크(연결 폴더) 74G → 74G(이 절이 더한 것은 3MB 남짓 — 노트북·그림·zip 차이).

## 보호 파일 (`before-manifest.json` 209개)

- 06절 뒤 대조 결과는 `manifest-changes.md` 「06절 뒤」.
