# 06-데이터-도구-실습 — 챕터 끝 실습 절 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md` §7-2, `textbook/_notebook/upgrade/PLAYBOOK.md` §3, `.claude/agents/easy-upgrade-editor.md` 6.8. 기준 사례: Ch 22 `09-Middleware-실습`, Ch 2 `13-파이썬-실습`, Ch 3 `06-Git-실습`(`author_06.py`, 검토 반영본).
새 절이라 수정 전 원본(`qa/upgrade/before/`)은 없습니다. 생성기: `qa/upgrade/author_06.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch04-data-tools 06`.
먼저 읽은 것: Ch 1·2·3 `qa/upgrade/chapter-summary.md`, 이 챕터 `qa/upgrade/handoff.md`(특히 `## §05 → 실습`), `author_01`~`05.py`, `_src/05`, `05-diagnosis.md`, 04-5·03-5 삽화 프롬프트, Ch 3 `author_06.py`·`_src/06`·`06-figures.md`·`06-diagnosis.md`·06-4 프롬프트, Ch 19 01 본문(Ch 4 함수 재사용 문장 확인).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 새 절 | 0 |
| G2 | 새 절 | 0 |
| G3 | 새 절 | 0 |
| G4 | 새 절 | 0 |
| G5 | 새 절 | 0 |
| G6 | 새 절 | 0 (첫 검사 7건: 70자 초과 7 → 문장 나눔, 나눈 뒤 6문장 단락 1 → 단락 나눔) |
| G7 | 새 절 | 0 |
| 코드 셀 | 새 절 | 18 (준비 4 + 본 경로 14, 심화 셀 없음) |
| 검사한 문장 | 새 절 | 362 (검토 반영 뒤, `gates-after.json`) |
| 모델 호출 | 새 절 | 0 (API 키 불필요) |

새 커널 실행 PASS(Linux aarch64, Python 3.12.13·pandas 3.0.5·SQLite 3.53.1·httpx 0.28.1, 2026-09-16, `PASS 06-데이터-도구-실습.ipynb: 18 cells`, 생성기 수정 뒤 전체 재실행 3회 모두 같은 기록장). verify PASS(`6 sections / 96 code cells (max 21 lines)`). 챕터 전체 게이트 6/6 PASS(`gates-wip-all.json`, G1~G7 0). `visual.cjs` 챕터 7페이지 × 1280·390px 14건 PASS(`playwright` 사본 경로만 바꾼 래퍼 `/tmp/ch04-06-proto/vis.cjs`로 실행, 공용 도구는 고치지 않음). 빌드 HTML: SVG 3·삽화 1, 남은 `{{` 토큰 0, 챕터 `index.html` 절 목록에 06 링크, 05절 HTML에 06 링크.

**모델 호출 수 근거**: §7-2의 「모델 호출 3~5번」은 LLM 챕터 기준입니다. Ch 4는 01~05절 모두 모델을 부르지 않고 API 키도 쓰지 않으므로(모델 호출은 Ch 6부터), 이 실습도 0번입니다. Ch 1 06·Ch 2 13·Ch 3 06 실습과 같은 판단입니다.

## 주제와 구성

- 주제: 「주문 서비스에서 고객별 합계 내기」. 고객 명단은 02절 CSV, 주문은 04절 연습용 주문 서비스(페이지 두 개), 두 데이터를 03절 SQLite 데이터베이스에 모아 `JOIN`으로 고객별 합계
- 고른 절(핵심 네 개): 01 `pd.read_csv`·`to_dict(orient="records")`·`len`, 02 고객 파일 두 개·`is_unique`, 03 테이블 제약·자리표시자 INSERT·`IntegrityError`·`JOIN`, 04 준비 코드·`fetch_all_orders()`. 05절(HTML 파싱)은 쓰지 않음 — 주문 데이터 흐름이고, 05절이 쓴 `data/article-text.json`을 Ch 5 01·`run_course_bundle.py`·테스트가 읽어 `data` 폴더를 건드리지 않으려고(본문 b3). 실행 전후 `article-text.json` 수정 시각 15:04(작업 전) 그대로
- 바꾸는 값: `customer_file` 하나(`customers.csv` → 02절 Before의 `all_customers.csv`). 데이터베이스 파일 `shop-1.db`/`shop-2.db`는 두 실행의 데이터를 나누는 자리이고 조건이 아니라고 노트북 13번·본문 b4에 적음(Ch 3 06 `run-1`/`run-2`와 같은 판단)
- 노트북 순서(PLAYBOOK §3): 준비(`[]`) → 도구 세 가지 불러오기(버전) → 주제 → 재료(고객 파일 두 개, 04절 준비 코드 세 셀로 서비스 켜기, 같은 모양의 빈 데이터베이스 두 개) → 부품 4개(`insert_customers`·`fetch_all_orders`(04절 그대로)·`insert_orders`·`total_by_customer`) → 기록 장치(`print_report`, Ch 2 13) → 조립 `run_pipeline(customer_file, database_name, orders_url)`(줄마다 절 주석) → 실행 1 → 실행 2 → 칸별 비교(+assert 2) → 데이터베이스에 남은 고객 확인 → 서비스 끄기 → 정리 3줄
- 실행 1(`customers.csv`): 요청 두 줄(`다음 페이지 번호: 2`·`None`), `연결한 행 수: 3`, 기록장 `고객 번호가 모두 다른가 | True`·`넣지 못한 고객 | []`·`받은 주문 수 | 3`·`주문 테이블의 행 수 | 3`·`고객별 합계 | {'김하나': 59000, '이두리': 18000}`
- 실행 2(`all_customers.csv`): `고객 넣기 오류: C001 UNIQUE constraint failed: customers.customer_id` → 기록장 `False`·`['C001']`·3·3·같은 합계, `연결한 행 수: 3`
- 비교: `달라진 칸 수: 3`(고객 파일·겹침 확인·넣지 못한 고객), 같은 칸 3, `assert` 두 줄 통과. 확인 셀 `고객 파일의 행 수: 3`·`고객 테이블의 행: [('C001', '김하나'), ('C002', '이두리')]`·`고객 테이블의 행 수: 2`. 서비스 끄기 `False`
- 02절 Before(같은 파일을 `merge()`로 바로 이어 5행·136000)와의 대비는 본문 b3·b6·복습 3과 노트북 3번·15번 설명에서 **앞 절 결과로만 인용**(이번에 다시 실행하지 않았다고 b3에 명시)
- 사다리: L1~L4. 셀 하나에 함수 하나, 함수 본문 최대 9문장(`total_by_customer`·`run_pipeline`), 코드 셀 최대 14줄(`insert_customers`). 타입힌트는 `: str`·`: list`, 반환 `-> list`·`-> int`·`-> dict`(01·05절·Ch 2), pandas 표 매개변수는 05절 `find_text(parent)`처럼 적지 않고 설명 셀에 이유. 바깥 변수를 함수 안에서 읽지 않음(주소·파일 이름은 매개변수). `upgrade_allow` 없음

## 앞 절에서 가져온 이름과 연속성 판단

- 가져온 것: 준비 셀 `mkdtemp(prefix="ch04-06-")`+`chdir`+`listdir`, 02절 `customers.csv`·`all_customers.csv` 글(같은 바이트), 04절 `page=1.json`·`page=2.json`·`order_server.py`·`Popen` 셀 그대로(준비 역할), `base_url + "/orders"`, `fetch_all_orders()` 정의 셀 그대로, 03절 테이블 제약(열 정의만 한 줄로 몰아 적고 `status` 열 뺌 — 서비스 주문에 상태 칸이 없음), `PRAGMA foreign_keys = ON`, `sqlite3.IntegrityError` 받기, 03절 `find_customer_orders()`의 JOIN SQL에서 `WHERE`만 뺀 모양, 라벨 「연결한 행 수:」, 03절 마지막 셀의 `SELECT * FROM` 행 수 세기, 04절 서비스 끄기 셀, Ch 2 03 `get(키, 기본값)`·`items()`·풀어 담기, Ch 2 13 `print_report()`·칸별 비교 셀, 초록 = C001 김하나·파랑 = C002 이두리(04-5 삽화)
- 새 이름: 함수 `insert_customers`·`insert_orders`·`total_by_customer`·`run_pipeline`, 값 `customer_file`·`report_1`·`report_2`·`rejected_ids`·`totals`·`customer_rows`·`all_customers`, 파일 `shop-1.db`·`shop-2.db`, 라벨 「고객 넣기 오류:」·「고객 파일의 행 수:」·「고객 테이블의 행:」·「고객 테이블의 행 수:」
- 한 문장으로 푼 모양: 자리표시자가 둘·셋인 INSERT(03절 `execute(sql, [값])`의 값 목록 길이만 늘림), `totals.get(name, 0) + amount`(Ch 2 03 `get` 기본값), `all_customer_text = customer_text + "C001,김하나\n"`(Ch 3 글자 `+`, 05절 줄바꿈 한 글자). 새 문법·새 API 없음
- 03절과의 차이: 03절은 겹친 C001을 셀에서 한 번 넣어 오류를 봄. 이번에는 함수가 줄마다 받아 목록에 모으고 다음 고객으로 넘어감(노란색, Ch 3 06-3과 같은 판단)
- 05절 「다음 학습」: Ch 5 01 문장을 06 b8로 옮기고 05 b8은 06절 링크와 실습 소개 네 문장으로 바꿈. 05 노트북 정리 셀 끝 문장도 06절 안내 두 문장으로 바꿈(`mdpatch.py`, 재실행 없음, 05 게이트 0). Ch 19 문장은 05 검토에서 「확인되지 않음」으로 뺀 전례가 있어, Ch 19 01 본문(「Ch 4의 `fetch_orders()`를 다시 작성하지 않습니다」)으로 확인한 사실만 06 b8·노트북 3번에 적음

## 사실 주장 확인

- 실행 출력으로 확인: 노트북 전체 출력(위). 프로토타입(`/tmp/ch04-06-proto/proto.py`, 연결 폴더 밖)과 새 커널 실행에서 기록장 값이 같음. 포트 번호·임시 경로는 인용하지 않음
- 실행하지 않았다고 적은 것(b7·노트북 정리): 번호는 같고 이름이 다른 겹친 줄, `NOT NULL`에 걸리는 빈 이름, 고객 테이블에 없는 번호의 주문(`FOREIGN KEY constraint failed`로 멈출 것으로 봄), 같은 데이터베이스에 두 번 실행, Windows·macOS
- SQLite 동작: `CREATE TABLE`만 한 연결을 `commit()` 뒤 닫았고, 다음 연결에서 INSERT·SELECT가 되는 것을 실행으로 확인. `PRAGMA foreign_keys`는 연결마다(03절 설명과 같음)

## 그림

- Mermaid 3장(PNG 직접 확인): 06-1 조립도(flowchart TB 7노드, viewBox 271), 06-2 실행 1 순서(sequenceDiagram 참여자 셋, `messageAlign: left`, viewBox 798), 06-3 두 실행 비교(처음 TB 두 칸 + 칸 안 LR로 viewBox 1089 → LR 두 칸 + 칸 안 TB로 바꿔 601)
- 삽화 1장: 06-4 주문 쟁반과 카드 꽂이(04-5 창구·깃발 쟁반·초록/파랑 서류철을 이어 씀). nano_banana_pro 16:9 2k, 1회 생성, 2크레딧(잔액 2904에서 생성). 채택 job 96165042-cd32-463f-8f45-1517e9e52caf. 저장 PNG(1100×614)를 기기에서 다시 받아 job 결과를 같은 폭으로 줄인 것과 대조해 픽셀 차이 0. 그림 읽기·캡션은 저장 파일 기준
- 색(§5-3): 바꾸는 값·고객 파일 초록, 부르는 코드·부품 파랑, 기록장·확인 출력 노랑, 실행 1의 「겹친 번호·막힌 고객 없음」 회색. 실행 2의 `UNIQUE constraint failed`는 함수가 받아 기록하고 셀이 끝까지 간 일이라 노랑. 이 절 그림에 빨강 없음. 근거는 `06-figures.md`

## 바꾼 다른 파일

- `chapter.json` sections 끝에 `06-데이터-도구-실습`(「데이터 도구 실습: 주문 서비스에서 고객별 합계 내기」, experiment) 추가
- `_src/05-문서-파싱과-스크래핑.html` b8 「다음 학습과 이어지는 지점」 → 06절 링크와 실습 소개(Ch 5 01 문장은 06 b8로 옮김). `author_05.py`·05 노트북 정리 셀 끝 문장 → 「다음 06절은 이 챕터의 실습입니다. …」
- `_src/index.html`: 이 챕터에는 없음(`_build.py`가 `chapter.json`으로 목차를 만듦). 빌드한 `index.html`에 06이 들어간 것을 확인. 노트북 개수를 적은 문장도 챕터 안에는 없음
- `집필점검표.md` 품질 개선 표에 06 행, `qa/verification.md`에 06절 한 절, `qa/upgrade/handoff.md` 끝에 `## 실습 → 챕터 검토`
- 챕터 밖(고치지 않음): `textbook/part1/_build_index.py`·`textbook/part1/index.html`(Ch 4 절 수), `textbook/downloads/` 묶음, `textbook/qa/upgrade-progress.md`(Ch 04 행 「대기」 그대로 — 오케스트레이터가 챕터 상태를 적음), `textbook/_notebook/checks/ch04-data-tools/`(visual.cjs가 결과 JSON·스크린숏을 다시 씀)

## 검토에서 볼 곳

- 실행 2에서 달라진 칸이 앞의 두 확인 칸뿐이라 비교가 너무 밋밋하지 않은지, 대신 02절 Before(136000)와의 대비를 앞 절 결과 인용으로만 둔 판단(b3·b6·복습 3)
- 04절 준비 코드 세 셀을 실습에 다시 둔 분량(준비 셀 4개 + 본 경로 14개, 30분 안팎인지)과, `insert_orders()`에 오류 받는 줄을 두지 않은 판단(b7에 한정)
- 삽화 06-4에서 접시의 초록 카드가 원근 때문에 꽂이 카드보다 작아 보이는 점, 파랑 서류철 뒷장 테두리(검수 메모에 적음)

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept-with-fixes(중 2, 하 1, 공통 C-1). 모두 반영했습니다. Q6 권고대로 비교 3칸·준비 셀 4개·06-3 실행 2 노랑은 유지
- 06-1(중): 본문 b6 결론 「받은 주문 수와 주문 테이블의 행 수는 고객 파일과 관계없는 칸이라 같았습니다. 기본 키가 겹친 줄을 막았으므로 연결한 행 수와 고객별 합계도 같았습니다.」, 노트북 16번 결과 읽기 「주문 두 칸은 고객 파일과 관계없이 같았습니다. 기본 키가 겹친 줄을 막아, 연결한 행 수와 합계도 실행 1과 같았습니다.」 기본 키 없는 테이블의 5행 장면은 노트북에서 실행하지 않아 넣지 않음
- 06-2(중): 2026-09-16 기기 셸에서 노트북 코드 셀(준비~실행 1)을 그대로 실행하고 `run_pipeline(customer_file, "shop-1.db", orders_url)`를 한 번 더 불러 확인했습니다. `고객 넣기 오류:` C001·C002 두 줄 → 요청 두 줄 → `IntegrityError: UNIQUE constraint failed: orders.order_id`로 멈춤, 오류를 쥔 상태에서 다른 연결의 쓰기는 `database is locked`. 본문 b7 다섯째 항목 「실행 1·2 셀만 같은 데이터베이스 파일로 다시 실행하면, 고객은 넣기 오류로 기록되지만 주문은 첫 줄에서 `IntegrityError`로 멈춥니다. 이 동작은 노트북과 같은 함수를 따로 실행해 확인했고, 노트북 출력에는 없습니다.」+ 잠김 문장 + 「다시 연습할 때는 마지막 셀로 서비스를 끄고, 첫 셀부터 실행합니다.」 노트북 마지막 결과 읽기에 앞 두 문장을 따로 단락으로
- 06-3: `06-2-실행1-순서.mmd` 요청 라벨 `INSERT 주문 O101~O103 · SELECT *`, 응답 `결과 3행`. 다시 렌더해 viewBox 798(868 이하), PNG 확인. alt(본문 토큰·caption.md)와 도식 읽기 「주문을 넣고 `SELECT *`로 받은 「결과 3행」」
- C-1: 본문 b8 「Ch 19 01절은 실습 폴더 `data_tools.py`의 `fetch_orders(csv_path, *, status=None)`를 모델이 고를 수 있는 도구로 다시 씁니다. 01절 함수와 하는 일은 같고, 상태를 키워드 인자 `status=`로 받는 모양입니다.」, 노트북 3번 설명도 같은 뜻(따로 단락). `data_tools.py`는 고치지 않음
- C-5: 게이트 표 검사한 문장 362. 코드 셀 18

재실행: 생성기 `author_06.py` 수정 → `run_section.sh … 06`(새 커널 PASS). 코드 셀 출력은 새 라벨 줄·임시 경로·포트를 빼고 반영 전과 같습니다. 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0, `qa/upgrade/gates-after.json`), `verify.py --chapter` `PASS 6 sections / 96 code cells (max 21 lines)`, `visual.cjs` 14건 PASS, 실습 폴더 pytest 10 passed. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(`review-round1.md` 끝 「반영 결과」의 볼 곳)가 남음
- 리뷰 묶음: `qa/upgrade/review-pack/06-데이터-도구-실습.md`
- 정리 대상(삭제하지 않고 목록만)은 `chapter-summary.md` §10
