# 03-SQL로-조회-함수-만들기 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/03-sql-query.*`).
생성기: `qa/upgrade/author_03.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch04-data-tools 03`.
수정 전 게이트는 01절 작업 때 챕터 전체로 남긴 `gates-before.json`(03절 53건)을 씁니다.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 2 | 0 |
| G2 | 3 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 7 | 0 |
| G6 | 38 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 20 (준비 1 + 본문 19, 최대 15줄 = Before 함수 정의) |
| 검사한 문장 | 96 | 416 (검토 반영 뒤, `gates-after.json`) |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Linux aarch64, Python 3.12.13, SQLite 3.53.1, 2026-09-16), `verify.py --chapter` `PASS 5 sections / 65 code cells (max 20 lines)`(04·05절은 개선 전), `visual.cjs` 1280·390px PASS(이 절 HTML과 `visual.cjs` 사본을 `/tmp/ch04-03-vis`에서 실행해 `_notebook/checks/`를 건드리지 않음), 실습 폴더 pytest 10 passed(`data_tools.py`는 고치지 않음).

## 수정 전 주요 문제

- G1·G2: 목록 내포식 두 곳(`[dict(row) for row in …]`, `[row["order_id"] for row in rows]`), `executescript` 안 SQL 한 줄에 세미콜론 세 개
- 게이트가 세지 않은 사다리 밖 문법(Ch 1~3 요약 §5, 01·02 handoff): `from pathlib import Path`·`TemporaryDirectory`·`Path(...) / "orders.db"`, 타입힌트 `str | Path`·`list[dict]`, `try/finally`(Ch 2 09절 B 트랙), try의 `else`+`raise AssertionError`, `with db:`(트랜잭션 — `with open`과 다른 뜻), `sqlite3.Row`·`row_factory`, `_ = …`, 함수 본문에 `return [내포식]`, 한 셀에 `assert` 두 개와 호출 세 번
- 01·02절과 이어지지 않음: 준비 셀 모양이 다름(`TemporaryDirectory`), 「앞에서 배운 내용」이 한 단락이고 02 개선본의 C003·겹친 C001·`validate`와 연결하지 않음. 반환 딕셔너리 키 `customer_name`이 01 `fetch_orders()`와 다른 모양
- SQL을 처음 가르치는 절인데 `CREATE TABLE`·`INSERT`·`PRAGMA`·`PRIMARY KEY`·`FOREIGN KEY`를 `executescript` 한 셀에 몰아 넣고, 셀 앞 설명이 「`execute()`는 …, `executescript()`는 …, `commit()`은 …」처럼 한 단락에 API 여러 개. 테이블 별칭 `orders o`·`USING`·`AS`까지 한 번에 풀이
- G5: 제목 셀·오늘 볼 그림 없음, 결과 읽기 셀이 없거나 출력 값을 인용하지 않음
- G6: 코드 이름·영문+조사로 시작하는 문장 30여 개(「`SELECT`는」, 「SQLite는」, 「Before는」), 70자 초과 6개, 5문장 넘는 단락 1개
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. 기존 Excalidraw 도식 1장(「빨간 상자는 … 조건식의 구조가 바뀌는 실패」 — 그림과 본문 대응 확인 기록 없음)
- 내용: Before 입력 `C001' OR 1=1 --`는 SQL 주석 `--`을 설명하지 않음. 외래 키 거부는 After 셀 안에 `else: raise`로 넣어 결과 읽기가 없음. 기준 SQLite 버전 없음

## 바꾼 것

- 노트북(paired 유지, 학습 질문 「SQL 함수에 입력을 어떻게 넘겨야 뜻이 바뀌지 않는가」와 C001 2건 → 이어 붙이기 3건 → 매개변수 0건 유지): 제목(할 일 3, 호출 0번·1분 이내, 기준 버전 Python 3.12.13·SQLite 3.53.1·sqlite3 요구 3.7.15 이상·외래 키 3.6.19부터) → 오늘 볼 그림(03-1) → 준비(`mkdtemp(prefix="ch04-03-")`) → `import sqlite3`·`sqlite_version` → `connect("shop.db")`+`PRAGMA foreign_keys = ON`·`['shop.db']` → `CREATE TABLE customers`(TEXT·PRIMARY KEY·NOT NULL, 제약) → `CREATE TABLE orders`(INTEGER·FOREIGN KEY … REFERENCES) → `INSERT INTO … VALUES` 2·3행(`rowcount`)+`commit()`(Git 커밋과 이름만 같음) → `SELECT * FROM orders`+`fetchall()`(커서, 튜플, ORDER BY 없으면 순서 약속 없음) → `WHERE customer_id = 'C001'`(01 마스크 연결) → `ORDER BY amount`(O103 먼저, `DESC`는 실행 안 함) → `JOIN … ON 표.열`(02 `merge()` 내부 조인 연결) → 겹친 C001 `UNIQUE constraint failed: customers.customer_id`(02 Before 연결) → C003 주문 `FOREIGN KEY constraint failed`(02 값 바꿔 보기 연결) → 남은 행 2·3·`close()` → `find_customer_orders(database_name, customer_id) -> list`(`?`+값 목록 `[customer_id]`, 풀어 담기로 딕셔너리) → C001 합계 `59000`(`+=`, assert) → 값 바꿔 보기 C002 `주문 수: 1` → Before `find_orders_before()`(f-string, 만든 SQL 출력) C001 2건 → `C001' OR '1'='1` 3건(O102 이두리 포함, SQL 주입) → After 같은 입력 `[]`·0건·assert → 정리
- SQL 문장마다 「뜻 → 일상 예 → 코드」: 서고와 사서(데이터베이스), 통화 연결(연결), 새 장부 첫 줄(CREATE TABLE), 새 줄 적기(INSERT), 「모든 칸을 보여 주세요」(SELECT), 「C001 줄만」(WHERE), 금액 작은 쪽지부터(ORDER BY), 쪽지 번호로 카드 찾기(JOIN, 02 비유), 인쇄된 신청서 빈칸(자리표시자). 본문에 「문장 | 뜻 | 일상 예 | 노트북 코드」 표
- 가르치지 않은 문법 처리: `Path`·`TemporaryDirectory`·`str | Path`·`list[dict]`·내포식·`try/finally`·try `else`·`raise`·`with connection:`·`row_factory`·`executescript`·테이블 별칭·`USING`·`AS`·SQL 주석 `--`·한 원소 튜플 `(x,)`는 뺌. 새로 쓴 Python 모양은 `sqlite3.IntegrityError`(02 `pd.errors.MergeError`와 같은 점 이음 한 문장), 여러 줄 f-string `f"""…"""`(Ch 2 01 f-string + 05 여러 줄 글, 변수만 넣음), `execute(sql, [값])`의 목록 인자, `cursor.rowcount`·`fetchall()`. 반환 키는 01 모양에 맞춰 `order_id`·`name`·`amount`
- Before 입력을 `C001' OR '1'='1`로 바꿔 SQL 주석 없이 재현하고, 함수가 만든 SQL을 출력해 조건 줄이 바뀌는 것을 출력으로 인용. Before와 After 함수는 SQL 조건 줄(과 Before의 SQL 출력 한 줄)만 다름
- 본문 10블록 전체를 다시 씀. 「이 절의 질문」, 용어 9개 표, 비유(요청서 빈칸), SQL 문장 표, 「앞에서 배운 내용」 4단락(02절 C003·겹친 C001·validate, 01절 마스크·`fetch_orders()`, Ch 2 01·03·04·05절, Ch 3 01절 커밋, Ch 1 05절 `or`), 주의 메모에 실행하지 않은 것(식별자 자리의 `?`, 검사를 켜지 않은 연결로 넣기, 커밋 없이 닫기, 오류 시 연결 닫기 `finally`, 다른 SQLite·OS), 튜플 `(customer_id,)` 대신 목록을 쓴 이유, 실습 `data/customers.csv`의 C003 박세진과 구분. 복습 5문항
- 그림: Mermaid 4장(요청과 SQL 조각, 테이블과 제약, 조회 함수, 이어 붙이기 비교) + 삽화 1장(요청서 빈칸). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)
- 라이브러리 동작 확인: Python 3.12 sqlite3 설명서(요구 SQLite 3.7.15 이상, `execute()`가 새 커서 반환, `fetchall()`, `rowcount`는 INSERT 등에서 바뀐 행 수, 물음표 방식 매개변수는 순서 있는 묶음 sequence, 레거시 트랜잭션에서 INSERT 전에 트랜잭션을 열어 커밋이 필요, 닫기 전에 커밋하라는 문장), SQLite 설명서(외래 키 3.6.19부터·기본 꺼짐·연결마다 켬, ORDER BY 없는 여러 행의 순서는 정해지지 않음, ASC가 기본). 설치본에서 `sqlite3.connect()` 직후 파일 크기 0, `autocommit` 값 -1(LEGACY), 제약 오류 뒤 `in_transaction` True를 따로 실행해 확인(노트북 밖, 결론에 쓰지 않음)

## 그림 확인

- PNG 네 장을 직접 열어 확인. 03-1 첫 판은 요청 상자 라벨이 「· 이름 · 금액」에서 어색하게 줄바꿈되고 FROM 조각이 세 줄로 흩어져 `<br>` 위치를 고침. 03-2 첫 판은 `PRAGMA foreign_keys =` / `ON`, `FOREIGN KEY constraint` / `failed`로 끊겨 `<br>`로 나눔. 03-3(viewBox 718)·03-4(792)는 첫 판 유지. 03-4는 Before → After 화살표가 칸 사이에 한 개
- 03-2의 IntegrityError 두 상자는 `try/except`로 받아 출력한 오류라 노랑(규격 §5-3). 빨강은 03-4 Before 결과에만
- 삽화 03-5(요청서 빈칸): 1차 job `deb486a8-0b82-4ec3-a120-677e2fab8280`은 관계는 읽혔으나 왼쪽 쟁반·서류철이 가운데 세로선에, 오른쪽 쟁반이 그림 끝에 잘려 채택 보류. 여백·크기 문장을 더한 2차 job `7e78bd4b-8ac2-4bc3-b805-13a448bcfc69` 채택. 4크레딧(잔액 2912에서). 저장 PNG(1100×614)를 채택 job 결과와 픽셀 대조해 차이 0, 1차 결과와는 전 영역 차이. 그림 읽기·캡션은 저장 파일을 보고 씀

## 검토에서 볼 곳

- SQL을 처음 가르치는 절이라 코드 셀이 20개(02절 16개)이고 검사 문장이 406개입니다. 강의 1h·실습 2h 안에 들어가는지, 7~10절(SELECT·WHERE·ORDER BY·JOIN)을 강의로, 11~13절(제약)을 실습으로 나눌지
- 함수 정의 셀 두 개가 14·15줄(규격 권장 3~12줄, 상한 15줄). Before와 After 함수를 한 줄만 다르게 두려고 SQL을 함수 안에 뒀습니다. 대안은 SQL 글을 앞 셀 변수로 빼는 것(함수가 바깥 변수를 읽게 됨)
- 값 목록으로 튜플 대신 목록 `[customer_id]`를 쓴 결정(설명서 예시는 튜플). 주의 메모에 이유를 적음
- 13절 `connection.close()`를 행 수 세기 셀 끝에 함께 둔 것(첫 줄 주석은 행 수 세기, 닫기는 둘째 주석)

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept-with-fixes(중 2, 하 2, 공통 C-1·C-2). 모두 반영했습니다.
- 03-1(중): 본문 b4 SQL 표 `ORDER BY` 행 「행의 순서를 정합니다. 방향을 적지 않으면 작은 값부터입니다」
- 03-2(중, Q3 권고: 코드 셀 20개·14·15줄 함수 셀 유지): 노트북 준비물 아래와 본문 b5 노트북 토큰 앞에 **강의와 실습 범위** 「강의 시간에는 4~10번과 14·15·17·18번 소제목을 설명합니다. 4~10번은 테이블 만들기부터 JOIN까지이고, 14·15·17·18번은 조회 함수와 Before/After입니다. 2·3번, 11~13번(제약과 남은 행 수), 16번(값 바꿔 보기)은 셀을 함께 실행합니다. 결과 읽기는 실습 시간에 이어서 읽습니다.」 **강사 확인 대상**
- 03-3: 17번 설명 「조회 함수가 에이전트 도구가 되면, 사용자 문장에서 고른 값이 함수에 들어갑니다.」(Ch 19에 고객 번호 조회 도구가 없어 Ch 19 약속을 뺌)
- 03-4: 본문 b6 둘째 단락 「두 함수는 SQL 조건 줄과, Before가 만든 SQL을 출력하는 줄만 다릅니다.」
- C-1: 본문 b7에 「실습 폴더 `data_tools.py`의 `find_customer_orders()`는 키 이름과 정렬 순서가 이 절 함수와 다릅니다. Ch 19 01절이 도구로 다시 쓰는 것은 같은 파일의 `fetch_orders(csv_path, *, status=None)`입니다.」
- C-2: 반복 출력 네 곳 앞에 `print("읽은 행:")`, 조회 결과 네 곳을 `print("조회 결과:", …)`로. 7·9번 결과 읽기 「라벨 줄 아래 첫 줄/첫 행」, 15·16·18번 「첫 줄 `조회 결과:` 뒤」
- 코드 셀 20, 검사한 문장 416

재실행: 생성기 `author_03.py` 수정 → `run_section.sh … 03`(새 커널 PASS). 코드 셀 출력은 새 라벨 줄·임시 경로·포트를 빼고 반영 전과 같습니다. 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0, `qa/upgrade/gates-after.json`), `verify.py --chapter` `PASS 6 sections / 96 code cells (max 21 lines)`, `visual.cjs` 14건 PASS, 실습 폴더 pytest 10 passed. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(`review-round1.md` 끝 「반영 결과」의 볼 곳)가 남음
- 리뷰 묶음: `qa/upgrade/review-pack/03-SQL로-조회-함수-만들기.md`
- 정리 대상(삭제하지 않고 목록만): `figures/03-sql-query.excalidraw`·`.svg`(옛 도식, 본문에서 뺌)
- 실습 폴더 `data_tools.py`의 `find_customer_orders(database: str | Path, customer_id: str) -> list[dict[str, Any]]`는 반환 키 `customer_name`·`status`와 `ORDER BY amount DESC, order_id`로 노트북 함수와 모양이 다름(01절 `fetch_orders`와 같은 상황, 고치지 않음)
