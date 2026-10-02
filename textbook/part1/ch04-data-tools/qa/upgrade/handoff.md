# Ch 04 절 사이 인계 메모

절 작업자가 다음 절 작업자에게 넘기는 메모입니다. 절을 마칠 때 맨 아래에 `## §NN → §NN+1`을 붙입니다.
「이어 쓸 이름과 값」은 다음 절이 쓸 수 있는 후보이고, 「아직 안 가르친 것」은 다음 절이 설명 없이 전제하면 안 되는 것입니다.
앞 챕터 요약: `textbook/part1/ch01-development-environment/qa/upgrade/chapter-summary.md`, `textbook/part1/ch02-python/qa/upgrade/chapter-summary.md`, `textbook/part1/ch03-git-github/qa/upgrade/chapter-summary.md`.

## §01 → §02

(01절 품질 개선 2026-09-16. 결과는 `01-diagnosis.md`, 게이트 G1~G7 0, 코드 셀 16, 모델 호출 0. 챕터 첫 절이라 `gates-before.json`은 5절 전체 수정 전 기록)

- 새로 가르친 문법: `import pandas as pd`(키워드 `as` = 불러온 모듈에 짧은 별명, 「별명 pd는 설명서와 많은 코드가 함께 쓰는 관례」), 모듈 속성 `pd.__version__`(Ch 2 07절 `__name__`에 연결), 반환 타입힌트 `-> list`(「Ch 2 07절 `-> int`와 같은 모양」 한 문장. `list[dict]`는 쓰지 않음). 그 밖에는 Ch 2 문법만 씀: `with open("w", encoding="utf-8")`+`"""…"""`, 정의 셀/호출 셀 분리, 빈 목록+`for`+`append()`, `try/except ValueError as error`, `type()`, `len()`, `assert`
- 새로 가르친 pandas API(노트북에서 실행한 것만): `pd.read_csv(파일 이름)`(첫 줄 = 열 이름, 숫자로 보이는 열은 숫자로 읽음), 인자 `dtype=str`(모든 열을 글자로), `print(표)`(왼쪽 인덱스 0·1·2), 속성 `shape`(`(3, 3)` 튜플)·`dtypes`(열마다 `str`/`int64`, 마지막 줄 `dtype: object`는 「목록 자체에 붙은 표시라 읽지 않음」), `표["열 이름"]`(시리즈, 끝 줄 `Name: status, dtype: str`), 시리즈 `== "paid"`(불리언 마스크, `dtype: bool`), `표.loc[마스크]`(참인 행만 남은 새 표, 인덱스는 원래 번호 유지, 원래 표 그대로), `표.loc[마스크, "열 이름"]`, 시리즈 `sum()`(정수 열 → `59000`, 글자 열 → 이어 붙인 `320001800027000`·`<class 'str'>`), 시리즈 속성 `dtype`, `표.to_dict(orient="records")`(행 하나 = 딕셔너리 하나, 키 = 열 이름, 인덱스 빠짐), `pd.to_numeric(시리즈 또는 목록)`(숫자 시리즈 반환, 바꿀 수 없는 값은 `ValueError: Unable to parse string "미정" at position 1`), 같은 열 이름에 다시 대입 `표["amount"] = 시리즈`(Ch 2 03절 딕셔너리 키 대입과 연결)
- 새로 가르친 용어(용어 표 7개): CSV(comma-separated values), 데이터프레임(DataFrame), 행(row)과 열(column), 인덱스(index), 자료형(dtype), 시리즈(Series), 불리언 마스크(boolean mask). 본문 비유: 종이 장부 = 표, 줄 = 행, 창을 낸 덮개 = 마스크(삽화 01-5)
- 이어 쓸 함수(정의 셀 그대로):
  ```python
  def fetch_orders(file_name: str, status: str) -> list:
      table = pd.read_csv(file_name)
      status_mask = table["status"] == status
      selected = table.loc[status_mask]
      records = selected.to_dict(orient="records")
      return records
  ```
  `data_tools.py`의 `fetch_orders(csv_path: str | Path, *, status: str | None = None) -> list[dict[str, Any]]`와 이름은 같지만 모양이 다름(실습 모듈·테스트는 이번에 고치지 않음). 노트북에서 부른 모양은 `fetch_orders("orders.csv", "paid")` → `['O101', 'O103']`, `"pending"` → 딕셔너리 1개
- 이어 쓸 폴더·파일 이름과 값: 준비 셀 `import os`·`import tempfile` → `practice_folder = tempfile.mkdtemp(prefix="ch04-01-")` → `os.chdir(practice_folder)` → `file_names = os.listdir()` 출력 `[]`(02절은 `ch04-02-`). 파일 `orders.csv`는 `order_text = """order_id,status,amount\nO101,paid,32000\nO102,pending,18000\nO103,paid,27000\n"""`를 `with open("orders.csv", "w", encoding="utf-8") as file:`로 씀. 표 이름 `orders`, 열 `status_column`, 마스크 `paid_mask`, 고른 표 `paid_orders`, 금액 `paid_amounts`, 합계 `paid_total` = 59000, 반환 `paid_records`·`paid_ids`·`pending_records`, Before `text_orders`·`wrong_total`, After `amount_numbers`·`correct_total` = 77000, `amount_texts = ["32000", "미정", "27000"]`. 상태 뜻: `paid` 결제 완료, `pending` 결제 대기. 금액은 원 단위 정수(Ch 2 02절부터). 교재 출력 Linux·Python 3.12.13·pandas 3.0.5(2026-09-16)
- 02절이 이어받을 연결: 01 본문 「다음 학습」은 「02절에서는 주문 표에 고객 번호 열을 더합니다. 그 번호로 고객 표와 주문 표를 연결하고, 연결 뒤에도 주문 행 수가 그대로인지 확인합니다」. 01 노트북 끝은 「다음 절에서는 주문 표에 고객 번호 열을 더해, 고객 표와 연결합니다」. 기존 02 노트북의 주문 세 건·금액(32000/18000/27000, 합계 77000)은 01과 같음. 01의 준비 셀과 `with open`으로 CSV 글을 쓰는 방식(또는 표를 셀에서 만드는 방식을 새로 풀기)을 맞추면 이어짐. 기존 02 노트북은 개선 전 모양: `pd.DataFrame([딕셔너리, …])`(01에서 안 씀 — 쓰면 한 문장으로 풀기), `from pandas.errors import MergeError`, `pd.concat`, `merge(on=, validate=, how="left", indicator=True)`, `joined[["order_id","name","amount"]]`(열 목록 선택, 01에서 안 씀), `to_string(index=False)`, `drop_duplicates`·`is_unique`·`iloc`, 한 줄에 여러 조건 `assert A and B and C`, `raise AssertionError`(try의 `else`와 `raise` 둘 다 미교육)
- 그림 색(01에서 정함): 파일·표의 열·시리즈·마스크·함수 인자 등 값 tool 초록, 실행한 코드·정의한 함수 flow 파랑, 출력으로 확인한 결과(합계·반환값) measure 노랑, Before 결함 결과 fail 빨강, try/except로 받아 출력한 오류 노랑, 인덱스(파일에 없던 번호) 회색. Mermaid 라벨 안 큰따옴표는 노드 라벨의 `#quot;`만 제대로 보이고 화살표 라벨에서는 `&quot;` 글자로 보였음(01-2에서 확인) — 화살표 라벨에는 따옴표를 쓰지 않음. 표 뒤 `LR`로 노드 5개를 이으면 viewBox 폭이 1500을 넘어 `TB`로 바꿈
- 아직 안 가르친 것(02절이 설명 없이 전제하면 안 됨): `pd.DataFrame()`으로 표 직접 만들기, `pd.concat`, `merge`/조인·키·기본 키·외래 키, 열 목록 `표[["a", "b"]]`, `iloc`, `to_string()`, `drop_duplicates`·`is_unique`, `astype`·`assign`, `head()`·`value_counts()`·`groupby`, `isna`·결측값, `read_csv`의 `dtype={열: 자료형}`(열별 지정 — 01은 주의 메모에 「이번에 실행하지 않음」), `errors="coerce"`, `Series.tolist()`, `pd.errors` 모듈·`MergeError`, 인덱스 다시 매기기. Python 쪽: `import 모듈 as 별명`은 01에서 풀었으나 `from 패키지.모듈 import 이름`의 점 경로는 안 씀, `raise`·try의 `else`, 목록 내포식·조건 표현식, f-string 안 식, `pathlib.Path`·`TemporaryDirectory`, 타입힌트 `list[dict]`·`X | None`·`*`, `isinstance`, `@` 줄·`BaseModel`·`*args`(A 트랙은 Ch 2 09~11절을 건너뜀)

## §02 → §03

(02절 품질 개선 2026-09-16. 결과는 `02-diagnosis.md`, 게이트 G1~G7 0, 코드 셀 16, 모델 호출 0. 삽화 02-5는 **삽화 대기**(2회 탈락, `illustration-pending.md`))

- 새로 가르친 Python 모양: `표.copy()`(Ch 2 03절 목록 `copy()`에 연결, 「원래 표는 그대로 두려고 복사」), `표.loc[인덱스 번호, "열 이름"] = 값`(「01절에서 마스크를 넣던 자리에 인덱스 번호를 넣은 모양」), `sorted(os.listdir())`(파일 두 개 이상일 때 순서 고정), 오류 이름 `pd.errors.MergeError`(「pandas 안의 errors 모듈에 있는 오류 이름이라 점으로 이어 적음」 — `from 패키지.모듈 import`는 여전히 안 씀), `except 오류이름 as error:` + `print("연결 오류:", error)`. 그 밖에는 01절·Ch 2 문법만 씀
- 새로 가르친 pandas API(노트북에서 실행한 것만): 시리즈 속성 `is_unique`(모두 다르면 `True`), 메서드 `표.merge(오른쪽 표, on="열 이름")`(기본값 내부 조인, 결과 열 순서 = 왼쪽 표 열 + 오른쪽 표의 나머지 열, 행 순서는 왼쪽 표 순서 — pandas 3.0.5 설명서 「preserve the order of the left keys」), 키워드 인자 `how="left"`(짝 없는 칸 `NaN`), `validate="many_to_one"`(오른쪽 키가 겹치면 결과를 만들기 전에 `MergeError`: `Merge keys are not unique in right dataset; not a many-to-one merge` + `Duplicates in right:` 줄), `drop_duplicates()`(인자 없음 = 모든 열이 같은 줄을 지우고 처음 줄을 남김)
- 새로 가르친 용어(용어 표 8개): 기본 키(primary key), 외래 키(foreign key), 다대일 관계(many-to-one), 정규화(normalization), 조인(join), 내부 조인(inner join), 왼쪽 조인(left join), 결측값(missing value, pandas 표시 `NaN`). 일상 예: 한 반의 출석 번호(기본 키). 비유(삽화 대기): 주문 쪽지의 색 스티커(외래 키)로 카드 상자의 손님 카드(기본 키)를 찾음. Ch 3 02절 `git merge`와 「이름만 같음」이라고 적음
- 이어 쓸 데이터(03절 SQLite 노트북·`data_tools.py` 테스트와 같은 값):
  - `customers.csv` = `customer_id,name` / `C001,김하나` / `C002,이두리`
  - `orders.csv` = `order_id,customer_id,status,amount` / `O101,C001,paid,32000` / `O102,C002,pending,18000` / `O103,C001,paid,27000`
  - 연결 결과 3행(O101 김하나, O102 이두리, O103 김하나), 김하나 주문 합계 59000(= 01절 결제 완료 합계, 「두 주문이 마침 모두 결제 완료」라고 적음), 전체 합계 77000
  - 짝 없는 키: O103 → `C003`(고객 표에 없음) → 내부 조인 2행, 왼쪽 조인 3행·이름 `NaN`. Before 파일 `all_customers.csv`(C001 줄 두 번) → 5행·136000. 개선 전 노트북의 O104·C999는 쓰지 않음(실습 `data/orders.csv`의 O104·C003 박세진과도 다름 — 03절이 C003을 쓰면 「02절에서는 고객 표에 없는 번호로 썼다」를 한 문장으로 구분)
- 이어 쓸 이름: 준비 셀 `practice_folder = tempfile.mkdtemp(prefix="ch04-02-")`(03은 `ch04-03-`), 텍스트 변수 `customer_text`·`order_text`·`all_customer_text`, 표 `customers`·`orders`·`all_customers`·`unique_customers`, 시리즈 `customer_ids`·`order_customer_ids`·`unique_ids`, 연결 결과 `joined`·`changed_joined`·`left_joined`·`wrong_joined`·`fixed_joined`, 합계 `kim_total`·`original_total`·`wrong_total`·`fixed_total`, 마스크 `name_mask`, 복사한 표 `changed_orders`. 출력 라벨 「주문 표의 행 수:」, 「연결한 표의 행 수:」, 「연결한 표의 금액 합계:」, 「고객 표의 고객 번호가 모두 다른가:」
- 03절이 이어받을 연결: 02 본문 「다음 학습」은 「03절에서는 같은 고객 표와 주문 표를 SQLite 데이터베이스에 만듭니다. SQL 문장으로 두 표를 잇고, 고객 번호로 주문을 조회합니다」. 02 노트북 끝도 같은 뜻. 03의 `JOIN`은 02의 `merge()`(내부 조인), `PRIMARY KEY`는 02의 기본 키·`is_unique`, `FOREIGN KEY`/`IntegrityError`(부모 없는 주문 거부)는 02의 「짝 없는 키가 조용히 빠짐」과 짝지어 설명할 수 있음. 02 주의 메모에 「기본 키는 비어 있으면 안 됨 — 실행하지 않음」이 있어 03의 `NOT NULL`로 이을 수 있음
- 기존 03 노트북(개선 전)이 쓰는 것 중 **Ch 1~3·01~02절에서 안 가르친 것**: `from pathlib import Path`·`from tempfile import TemporaryDirectory`·`Path(...) / "orders.db"`, 타입힌트 `str | Path`·`-> list[dict]`, 목록 내포식 `[dict(row) for row in …]`·`[row["order_id"] for row in rows]`, try의 `else`+`raise AssertionError`, `try/finally`(Ch 2 09절 B 트랙에서만), f-string 안에 입력 넣기(SQL 주입 실패 재현 — 「f-string 안 식」은 아니지만 변수만 넣은 f-string이라 L1 범위, 뜻은 풀어야 함), `sqlite3.Row`·`row_factory`·`executescript`·`PRAGMA`, `with connection:`(트랜잭션 — `with open`과 다른 뜻), `_ = …`. 02는 `import sqlite3`·SQL을 전혀 쓰지 않음
- 그림 색(01·02에서 같게 씀): 파일·표·행·값 초록, 실행한 코드 파랑, 출력으로 확인한 행 수·합계·검사 결과 노랑, Before 결함 결과 빨강, try/except로 받아 출력한 오류 노랑. Mermaid 주의: subgraph 제목에 `<br>`를 쓰면 제목이 안쪽 상자와 겹침(LR·TB 모두 확인). 칸 밖 노드와 subgraph를 `-.-`·`~~~`로 이으면 배치가 흩어짐. subgraph 두 칸 좌우 순서는 정의 순서를 바꿔 잡음(02-3)
- 아직 안 가르친 것(03절이 설명 없이 전제하면 안 됨): SQL 전부(`SELECT`·`JOIN`·`WHERE`·`ORDER BY`·`?` 자리표시자), 데이터베이스·테이블 제약(`PRIMARY KEY`·`FOREIGN KEY`·`NOT NULL`), `sqlite3` 모듈, 트랜잭션·커밋(Git 커밋과 다른 뜻), 오른쪽·바깥 조인, `indicator=True`·`_merge`, `pd.concat`, `pd.DataFrame()`, 열 목록 `표[["a", "b"]]`, `iloc`, `to_string()`, `tolist()`, `drop_duplicates(subset=…, keep=…)`, `duplicated()`, `isna()`·결측값 찾기(02는 `NaN`을 보기만 함), `validate`의 다른 값(`one_to_one` 등), 인덱스 다시 매기기. Python 쪽은 01 handoff 목록과 같음(`raise`·try `else`·`finally`(A)·내포식·조건 표현식·f-string 안 식·`pathlib.Path`·`TemporaryDirectory`·`list[dict]`·`X | None`·`*`·`isinstance`·`from 패키지.모듈 import`·`@`·`BaseModel`·`*args`)

## §03 → §04

(03절 품질 개선 2026-09-16. 결과는 `03-diagnosis.md`, 게이트 G1~G7 0, 코드 셀 20, 모델 호출 0. 삽화 03-5 채택(job `7e78bd4b-…`))

- 새로 가르친 Python 모양: `import sqlite3`(표준 라이브러리, 설치 없음), 모듈 속성 `sqlite3.sqlite_version`, 함수 `sqlite3.connect("파일 이름")`(없으면 만들고 연결 객체 반환), 연결 메서드 `execute(SQL 글)`·`execute(SQL 글, [값])`(새 커서 반환)·`commit()`·`close()`, 커서 속성 `rowcount`와 메서드 `fetchall()`(튜플 목록), 오류 이름 `sqlite3.IntegrityError`(「02절 `pd.errors.MergeError`처럼 모듈 이름에 점으로 이어 적음」), 여러 줄 f-string `f"""…'{customer_id}'…"""`(변수만 넣음, Before 전용), `for order_id, name, amount in rows:`(Ch 2 03 풀어 담기), 함수 안의 지역 변수 `connection`(13절에서 닫은 연결과 다름을 한 문장). 반환 결과를 쓰지 않는 `execute()`는 `cursor = …`로 받아 셀 끝에 커서 표시가 나오지 않게 함
- 새로 가르친 SQL(문장마다 뜻 → 일상 예 → 코드): `PRAGMA foreign_keys = ON`(연결마다, SQLite는 기본 꺼짐), `CREATE TABLE 이름 (열 자료형 제약, …)`·`TEXT`·`INTEGER`·`PRIMARY KEY`·`NOT NULL`·`FOREIGN KEY (열) REFERENCES 표 (열)`, `INSERT INTO 표 VALUES (…), (…)`(글자는 작은따옴표), `SELECT * FROM 표`, `SELECT 열, 열 FROM`, `WHERE 열 = '값'`(SQL 비교는 `=` 하나), `ORDER BY 열`(작은 값부터, `DESC`는 실행 안 함), `JOIN 표 ON 표.열 = 표.열`(내부 조인, `표 이름.열 이름`), 조건의 `OR`(Ch 1 05 `or`), 자리표시자 `?`. 오류 메시지 `UNIQUE constraint failed: customers.customer_id`, `FOREIGN KEY constraint failed`
- 새로 가르친 용어(용어 표 9개): 데이터베이스(database), SQL(Structured Query Language), 테이블(table), 연결(connection), 커서(cursor), 제약(constraint), 커밋(commit — Git 커밋과 이름만 같음), 자리표시자(placeholder), SQL 주입(SQL injection). 비유: 도서관 서고와 사서(데이터베이스), 전화 통화 연결(연결), 인쇄된 요청서의 빈칸(자리표시자, 삽화 03-5 — 줄을 덮은 분홍 쪽지 = 이어 붙인 입력, 투명 봉투 = 값 목록, 서류철 세 개 = 주문 세 건, 빈 쟁반 = 빈 목록)
- 이어 쓸 함수(정의 셀 그대로, 01 `fetch_orders()`와 같은 딕셔너리 목록 반환):
  ```python
  def find_customer_orders(database_name: str, customer_id: str) -> list:
      sql = """SELECT orders.order_id, customers.name, orders.amount
      FROM orders JOIN customers ON orders.customer_id = customers.customer_id
      WHERE orders.customer_id = ?
      ORDER BY orders.order_id"""
      connection = sqlite3.connect(database_name)
      cursor = connection.execute(sql, [customer_id])
      rows = cursor.fetchall()
      connection.close()
      records = []
      for order_id, name, amount in rows:
          record = {"order_id": order_id, "name": name, "amount": amount}
          records.append(record)
      return records
  ```
  `find_customer_orders("shop.db", "C001")` → O101·O103 김하나, 합계 `59000`(`+=`), `"C002"` → `[{'order_id': 'O102', 'name': '이두리', 'amount': 18000}]`. Before `find_orders_before()`(f-string, 만든 SQL 출력) + `typed_id = "C001' OR '1'='1"` → 3건, After 같은 입력 → `[]`. `data_tools.py`의 같은 이름 함수(키 `customer_name`·`status`, `ORDER BY amount DESC, order_id`)와 모양이 다름(고치지 않음)
- 이어 쓸 이름과 값: 준비 셀 `practice_folder = tempfile.mkdtemp(prefix="ch04-03-")`(04는 `ch04-04-`), 파일 `shop.db`, 변수 `connection`·`cursor`·`rows`·`row`, SQL 글 변수 `customer_table_sql`·`order_table_sql`·`where_sql`·`order_by_sql`·`join_sql`, 결과 `kim_records`·`kim_total`·`lee_records`·`normal_records`·`wrong_records`·`safe_records`, 출력 라벨 「고객 테이블에 넣은 행 수:」, 「연결한 행 수:」, 「넣기 오류:」, 「찾은 주문 수:」, 「주문 수:」. 교재 출력 Linux·Python 3.12.13·SQLite 3.53.1(2026-09-16)
- 04절이 이어받을 연결: 03 본문 「다음 학습」은 「04절에서는 데이터베이스 대신 HTTP 주소로 데이터를 주는 REST 서비스를 조회합니다. 여러 페이지로 나뉜 목록을 끝까지 읽는 함수를 만들고, 이 절처럼 딕셔너리 목록을 반환합니다」. 노트북 끝은 「다음 절에서는 데이터베이스 대신 HTTP 주소로 데이터를 주는 REST 서비스에서, 여러 페이지로 나뉜 목록을 끝까지 읽습니다」. 04가 반환 모양을 딕셔너리 목록으로 두면 01 `fetch_orders()`·03 `find_customer_orders()`와 이어짐. 03의 「빈 목록은 입력이 이상했는지 알려 주지 않음」 메모와 04의 「첫 페이지만 읽어도 오류 없음」을 「오류 없이 덜 가져온 결과」로 이을 수 있음. 03의 「`close()` 줄까지 못 가는 경우, `finally`는 확장 경로」 메모는 04의 `httpx.Client`+`try/finally`와 겹침 — A 트랙 기준이면 `with`나 한 번 호출 `httpx.get()`으로 풀거나 한 문장씩 설명
- 기존 04 노트북(개선 전)이 쓰는 것 중 **Ch 1~3·01~03절에서 안 가르친 것**: `class Handler(BaseHTTPRequestHandler)` 상속·`do_GET`·`self.wfile`·`*args: object`(A 트랙 금지)·`threading.Thread(target=…, daemon=True)`·`ThreadingHTTPServer`(준비용 서버 — 규격 §2-3 「준비용 클래스 상속」 금지, 심화 셀이나 따로 띄운 서버로 옮길지 판단 필요), `from http.server import`(점 경로 import), f-string 안 식 `f"{base_url}/articles"`는 변수만이라 L1이지만 `f"http://127.0.0.1:{server.server_port}"`는 속성 접근, 목록 내포식 `[item["id"] for item in …]`, 타입힌트 `list[dict]`·`int | None`·키워드 전용 `*`·변수 타입힌트 `items: list[dict] = []`, `try/finally`(B), `dict.get()`은 Ch 2 03에서 배움, `items.extend()`(미교육 — `append` 반복이나 한 문장), 메서드 이어 부르기 `httpx.get(...).json()`, `response.raise_for_status()`·`status_code`·`request.url`·JSON(미교육 — `import json`은 Ch 2에서 쓰지 않음, Ch 1 03에서 `import json` 모듈 이름만), `params=`·`timeout=`
- 그림 색(01~03 같게 씀): 파일·테이블·값·인자 초록, 실행한 코드·SQL 조각·정의한 함수 파랑, 출력으로 확인한 행 수·합계·반환값·받아서 출력한 오류 노랑, Before 결함 결과 빨강, 코드도 값도 아닌 요청 문장 회색. Mermaid: 라벨에 작은따옴표·`=`·`?`는 큰따옴표 라벨 안에서 문제없이 그려짐(03-4). 줄바꿈은 `<br>`로 직접 넣어야 `PRAGMA foreign_keys =` / `ON` 같은 어색한 끊김이 없음
- 아직 안 가르친 것(04절이 설명 없이 전제하면 안 됨): SQL `DESC`·`LIMIT`·`COUNT`·`SUM`·`GROUP BY`·`UPDATE`·`DELETE`·`LEFT JOIN`·테이블 별칭·`USING`·`AS`·SQL 주석 `--`·이름 붙은 자리표시자 `:name`, `executemany`·`executescript`·`row_factory`·`sqlite3.Row`·`with connection:`(트랜잭션)·`rollback()`·`autocommit`, 한 원소 튜플 `(x,)`(주의 메모에만), 인덱스, pandas `read_sql`·`to_sql`. HTTP·REST·JSON·상태 코드·URL·쿼리 문자열·`httpx` 전부. Python 쪽은 02 handoff 목록과 같음(`raise`·try `else`·`finally`(A)·내포식·조건 표현식·f-string 안 식·`pathlib.Path`·`TemporaryDirectory`·`list[dict]`·`X | None`·`*`·`isinstance`·`from 패키지.모듈 import`·`@`·`BaseModel`·`*args`·클래스 상속·`threading`)

## §04 → §05

(04절 품질 개선 2026-09-16. 결과는 `04-diagnosis.md`, 게이트 G1~G7 0(수정 전 50), 코드 셀 13(준비 4 + 본문 9), 모델 호출 0, 인터넷 접속 없음. 삽화 04-5 채택(job `d55f7a01-…`, 2크레딧))

- 새로 가르친 Python 모양: `import httpx`(패키지, 실습 `uv sync --locked`로 설치됨), 모듈 속성 `httpx.__version__`(01절 `pd.__version__`과 같은 모양), 글자 `+`로 주소 잇기 `base_url + "/orders"`(Ch 3), 키워드 인자에 딕셔너리 넣기 `params={"page": 1}`, 오류 이름 `httpx.HTTPStatusError`(03절 `sqlite3.IntegrityError`처럼 점 이음), `while page is not None:`(Ch 2 02 `while` + 04 `None`), 반복 안에서 다음 값으로 다시 대입 `page = body["next_page"]`. 준비 셀에서만(설명 없이 실행): `subprocess.Popen([sys.executable, "order_server.py"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)`·`server_process.stdout.readline().strip()`·`terminate()`·`wait()`·`poll() is None`(마지막 셋은 9절 설명 셀에서 한 문장씩 풂). Ch 2 08절 `subprocess.run()`은 「끝날 때까지 기다림」, `Popen()`은 「켜 두고 넘어감」으로 대비
- 새로 가르친 httpx API(노트북에서 실행한 것만): `httpx.get(주소, params=딕셔너리, timeout=2.0)`(요청마다 연결을 새로 엶, GET 요청 → 응답 객체), 응답 속성 `url`(쿼리 문자열이 붙은 주소)·`status_code`(200·404)·`text`(본문 글), 메서드 `json()`(JSON 글 → 딕셔너리·목록, `null` → `None`)·`raise_for_status()`(200번대가 아니면 `HTTPStatusError`, 메시지 첫 줄 `Client error '404 Not Found' for url '…'`). 실행하지 않은 것: `httpx.Client`, `timeout` 초과, 5xx, 헤더, POST, 인증
- 새로 가르친 용어(용어 표 9개): HTTP(HyperText Transfer Protocol), 요청(request)과 응답(response), 서버(server)와 포트(port), 쿼리 문자열(query string), 상태 코드(status code), JSON(JavaScript Object Notation), REST API, 페이지네이션(pagination), 시간 제한(timeout). 본문(body)은 설명 셀에서 한 문장. 127.0.0.1 = 「이 컴퓨터 자신」. 일상 예: 식당 주문서(요청) → 영수증(상태 코드)과 음식(본문), 택배 송장(JSON), 건물 호수(포트). 비유 삽화 04-5: 창고 벽 창구(연습용 서비스)·쟁반(응답 한 페이지)·서류철(주문, 초록 = C001 김하나, 파랑 = C002 이두리 — 03-5 이어 씀)·깃발(`next_page`)·깃발 없는 쟁반(마지막 페이지)
- 이어 쓸 함수(정의 셀 그대로, 01·03절처럼 딕셔너리 목록 반환):
  ```python
  def fetch_all_orders(orders_url: str) -> list:
      all_orders = []
      page = 1
      while page is not None:
          response = httpx.get(orders_url, params={"page": page}, timeout=2.0)
          response.raise_for_status()
          body = response.json()
          print("요청한 페이지:", page, "/ 다음 페이지 번호:", body["next_page"])
          for order in body["orders"]:
              all_orders.append(order)
          # 응답이 알려 준 다음 페이지 번호로 바꿉니다. 마지막 페이지에서는 None입니다
          page = body["next_page"]
      return all_orders
  ```
  Before `fetch_orders_before(orders_url) -> list`는 `page = 1` 한 번 요청·`return body["orders"]`. 반환 딕셔너리 키는 `order_id`·`customer_id`·`amount`(01절 `fetch_orders`의 `status`, 03절의 `name`과 다름 — 서비스가 준 글 그대로). `data_tools.py`의 `fetch_articles()`(기사 `/articles`, `httpx.Client`, 반복 페이지 검사)와 이름·모양이 다름(고치지 않음)
- 이어 쓸 이름과 값: 준비 셀 `practice_folder = tempfile.mkdtemp(prefix="ch04-04-")`(05는 `ch04-05-`), 파일 `page=1.json`(O101 C001 32000, O102 C002 18000, `"next_page": 2`)·`page=2.json`(O103 C001 27000, `"next_page": null`)·`order_server.py`, 변수 `server_text`·`server_process`·`port_text`·`base_url`·`orders_url`·`response`·`body`·`before_orders`·`before_total`(50000)·`all_orders`·`after_total`(77000), 반복 변수 `order`. 출력 라벨 「서비스 주소:」, 「요청한 주소:」, 「상태 코드:」, 「본문 글:」, 「이 페이지의 주문 수:」, 「다음 페이지 번호:」, 「상태 오류:」, 「요청한 페이지: … / 다음 페이지 번호: …」, 「읽은 주문:」, 「읽은 주문 수:」, 「금액 합계:」, 「서비스가 아직 켜져 있는가:」. 교재 출력 Linux·Python 3.12.13·httpx 0.28.1(2026-09-16). 포트 번호는 실행마다 달라 인용하지 않음
- 05절이 이어받을 연결: 04 본문 「다음 학습」은 「05절에서는 JSON을 주는 서비스가 없을 때를 다룹니다. 그때는 HTML로 된 문서에서 필요한 값을 골라 읽습니다. 이 절처럼 읽은 값이 빠지거나 없을 때를 먼저 확인합니다」. 노트북 끝은 「다음 절에서는 JSON 대신 HTML로 된 문서에서 필요한 값을 골라 읽습니다」. 04의 「응답 본문 글 → `json()`으로 딕셔너리」를 05의 「HTML 글 → 파서로 요소 트리」로, 04 6절 「404 본문에는 `orders` 칸이 없음 → 상태 코드부터 확인」을 05의 「없는 선택자 결과 `None`에 메서드를 부르면 `AttributeError` → 먼저 확인」으로 이을 수 있음. 05 Before/After(선택 결과 확인)는 01~04절의 「오류 없이 틀린/덜 가져온 결과」 흐름과 달리 「오류로 멈춤」이라, 03절 IntegrityError·04절 HTTPStatusError처럼 「그 오류 이름만 받는 try/except」 모양으로 쓰면 이어짐. 05에서 인터넷 사이트를 부르지 않는다면 04의 「인터넷 서비스는 내용이 바뀌거나 접속이 막힐 수 있어 연습용을 씀」을 제공 HTML 파일 이유로 이어 쓸 수 있음
- 기존 05 노트북(개선 전)이 쓰는 것 중 **Ch 1~3·01~04절에서 안 가르친 것**: `from pathlib import Path`·`Path.cwd().parents`·`read_text`/`write_text`(Ch 1에서만), `next(path for path in (…, *…) if …)`(제너레이터 식·`*` 풀어 넘기기), `from urllib.robotparser import RobotFileParser`·`from bs4 import BeautifulSoup`(점 경로·패키지 import), 한 셀 여러 줄 딕셔너리에 메서드 이어 부르기 `article.select_one(".summary").get_text(strip=True)`, f-string 안 식 `f"{record['title']}\n{record['summary']}"`, 딕셔너리 풀기 `{**record, …}`, 조건 표현식 `… if subtitle_node else None`, `json.dumps(…, ensure_ascii=False, indent=2)`·`json.loads`(04는 `response.json()`만 — `import json` 모듈은 안 씀), `soup.builder.NAME`, `type(error).__name__`(Ch 1 02 심화만). 05는 실습 폴더 `data/article.html`을 읽고 **`data/article-text.json`을 써서 Ch 5 01절이 그 파일을 읽음**(05 본문 「다음 학습」) — 파일 이름·경로·`schema_version`을 바꾸면 Ch 5 01과 어긋나니 임시 폴더로 옮길지 판단 필요
- 그림 색(01~04 같게 씀): 파일·요청·서비스가 준 값·인자 초록, 실행한 코드·정의한 함수 파랑, 출력으로 확인한 상태 코드·딕셔너리·합계·받아서 출력한 오류 노랑, Before 결함 결과 빨강. sequenceDiagram 참여자는 기본 회색, 메모 노랑, 요청 실선·응답 점선, `messageAlign: left`(04-1). Mermaid: 이어지지 않은 노드 두 줄은 TB에서 좌우로 나란히 놓임(04-3), subgraph 두 칸을 TB로 쌓고 칸 안 `direction LR`이면 viewBox 741(04-4)
- 아직 안 가르친 것(05절이 설명 없이 전제하면 안 됨): HTML·태그·요소·속성·CSS 선택자, BeautifulSoup·lxml·파서, robots.txt·`urllib.robotparser`, 이용 약관·저작권 확인 절차, `import json`·`json.dumps`/`json.loads`(04는 응답 메서드 `json()`만), 헤더·`Content-Type`(서버 글 안에만 있고 설명 안 함), POST·인증·API 키 헤더, `httpx.Client`·세션, 재시도·대기, 시간 제한 초과, 5xx, 다른 페이지 방식(커서·다음 주소·빈 목록). Python 쪽은 03 handoff 목록과 같음(`raise`·try `else`·`finally`(A)·내포식·제너레이터 식·조건 표현식·f-string 안 식·`pathlib.Path`·`TemporaryDirectory`·`list[dict]`·`X | None`·`*`·`**` 풀기·`isinstance`·`from 패키지.모듈 import`·`@`·`BaseModel`·`*args`·클래스 상속·`threading`), 그리고 `subprocess.Popen`은 04 준비 셀에서만 썼으므로 기본 경로 전제 금지

## §05 → 실습

(05절 품질 개선 2026-09-16. 결과는 `05-diagnosis.md`, 게이트 G1~G7 0(수정 전 47), 코드 셀 13(준비 1 + 본문 12), 모델 호출 0, 인터넷 접속 없음. 삽화 05-5 채택(job `07413a99-…`, 2크레딧). 챕터 본문 01~05절 개선 끝 — 다음은 06 실습 절)

### 05절이 새로 가르친 것

- Python 모양: `os.path.exists(경로)`(준비 셀에서 한 문장), `os.chdir()`로 실습 폴더 `data`에 들어감(임시 폴더 아님), `import urllib.robotparser`(묶음 안 모듈을 점으로 이음 — 03절 `sqlite3.IntegrityError`·04절 `httpx.HTTPStatusError`와 같은 설명), `import bs4`·`import lxml`·`bs4.__version__`·`lxml.__version__`, `html_text.replace(a, b)`(Ch 1 04), 오류 이름 `AttributeError`(「없는 속성이나 메서드를 쓰려 할 때」, 이 절에서 처음 관찰), 타입힌트를 일부 적지 않은 함수 `find_text(parent, selector: str)`(요소 자료형 미교육이라 적지 않았다고 설명), 두 줄 딕셔너리, 목록 안 튜플을 `for page_name, one_record in page_records:`로 풀기 + 안쪽 `for key, value in one_record.items():`, 글자 `"\n"`(줄바꿈 한 글자), `import json`·`json.dumps(값, ensure_ascii=False, indent=2)`(04절 `response.json()`의 반대 방향)
- API(노트북에서 실행한 것만): `urllib.robotparser.RobotFileParser()`·`parse(규칙 줄 목록)`·`can_fetch(프로그램 이름, 주소)`, `bs4.BeautifulSoup(글, "lxml")`·`prettify()`·`select_one(선택자)`(없으면 `None`)·요소 `.name`·`get_text(strip=True)`·`요소["속성 이름"]`, `json.dumps()`. 실행하지 않은 것: `select()`·`find()`·`find_all()`, `soup.h1` 같은 속성식 접근, `요소.get("속성")`, 없는 속성 KeyError, `RobotFileParser.read()`·`set_url()`, `json.loads()`·`json.load()`, 다른 파서(`html.parser`·html5lib)
- 용어(용어 표 9개): 스크래핑(scraping), robots.txt, HTML(HyperText Markup Language), 태그(tag)와 요소(element), 속성(attribute), 파싱(parsing)과 파서(parser), 요소 트리(element tree)·자식 요소, CSS 선택자(CSS selector), class 속성. 선택자 두 모양: 요소 이름 `article`·`h1`·`time`, class `.summary`/`.lead`
- 비유 삽화 05-5: 나무 상자(기사 요소) 안 흰 카드(자식 요소)의 색 스티커(class 이름), 앞면에 노란 스티커가 붙은 쟁반(선택자 `.summary`), 빈 쟁반(`None`), 보라 스티커(바뀐 `lead`). 03-5·04-5 나무 쟁반을 이어 씀. 서류철(주문)과 구분하려고 흰 카드
- 결론 문장: 「`select_one()`은 맞는 요소가 없어도 오류 없이 `None`」, 「`None`에서 `get_text()`를 부르면 AttributeError로 멈추고, 메시지에 어느 선택자가 비었는지 없음」, 「먼저 `is None`을 확인하면 빈 칸을 이름으로 알리고 나머지 칸을 채움」, 「robots.txt `True`는 이용 허가가 아님 — 약관·저작권·개인정보·요청 간격은 따로」

### 05절 이름과 값 (실습에서 이어 쓸 후보)

- 파일(실습 폴더 `labs/part1/ch04-data-tools/data`, 고치지 않음): `article.html`(270글자 한 줄, `<article data-id="A10">` 안 h1 `골목상권 매출 회복`, `p class="summary"` `주말 방문객 증가로 음식점 매출이 늘었습니다.`, `<time datetime="2026-09-01">2026년 9월 1일</time>`), `robots.txt`(`User-agent: *`·`Allow: /articles/`·`Disallow: /private/`), **`article-text.json`**(노트북이 다시 씀 — 아래 주의)
- 변수: `data_folder`, `rule_lines`, `robots`, `article_address = "https://example.test/articles/A10"`, `private_address = "https://example.test/private/A10"`, `html_text`, `soup`, `tree_text`, `article`, `title_node`, `summary_node`, `time_node`, `changed_html`(`class="lead"`), `changed_soup`, `changed_summary`, `lead_node`, `before_record`, `record`, `changed_record`, `page_records`, `empty_keys`, `payload`, `json_text`. 출력 라벨 「규칙 줄:」, 「기사 주소를 허용하는가:」, 「HTML 글의 글자 수:」, 「고른 요소의 이름:」, 「기사 번호 속성:」, 「제목:」, 「요약:」, 「화면에 보이는 날짜:」, 「datetime 속성:」, 「.summary로 고른 결과:」, 「원래 페이지 기록:」, 「바뀐 페이지 기록:」, 「속성 오류:」, 「찾지 못한 선택자:」, 「원래 페이지 빈 칸:」
- 함수(정의 셀 그대로, 노트북에서는 셀 두 개):
  ```python
  def find_text(parent, selector: str):
      found = parent.select_one(selector)
      if found is None:
          print("찾지 못한 선택자:", selector)
          return None
      return found.get_text(strip=True)

  def parse_article(html_text: str) -> dict:
      soup = bs4.BeautifulSoup(html_text, "lxml")
      article = soup.select_one("article")
      title = find_text(article, "h1")
      summary = find_text(article, ".summary")
      published = article.select_one("time")["datetime"]
      record = {"id": article["data-id"], "title": title,
                "summary": summary, "published": published}
      return record
  ```
  Before `parse_article_before(html_text: str) -> dict`는 제목·요약을 `article.select_one(…).get_text(strip=True)`로 바로 읽음. 반환은 딕셔너리 **하나**(01 `fetch_orders`·03 `find_customer_orders`·04 `fetch_all_orders`는 딕셔너리 목록). `text` 칸은 함수 밖(10절 셀)에서 더함. `data_tools.py`의 `parse_article_html()`(`from bs4 import`, 조건 표현식, `raise ValueError`, `text` 칸 포함)과 이름·모양이 다름(고치지 않음)
- 교재 출력 Linux·Python 3.12.13·beautifulsoup4 4.15.0·lxml 6.1.3·soupsieve 2.9.2(2026-09-16)

### 실습 절이 꼭 지킬 것 — `data/article-text.json`

- Ch 5 01 노트북 셀 4가 부모 폴더를 올라가며 `labs/part1/ch04-data-tools/data/article-text.json`을 찾아 `schema_version`·`source`·`record.id`·`record.text`를 읽음. `textbook/qa/run_course_bundle.py`는 압축 해제본에서 이 파일을 지운 뒤 Ch 4 **05** 노트북을 `--cwd notebooks`로 실행해, 새 파일이 저장소 파일과 바이트까지 같은지 assert. `tests/test_data_tools.py`도 `schema_version`·`source`·`record == parse_article_html(article.html)`을 검사
- 그래서 06 실습 노트북은 `data/article-text.json`·`data/article.html`·`data/robots.txt`를 쓰거나 바꾸지 않는 것을 권함. 기사 기록을 다시 만들어 보려면 임시 폴더(01~04절 `mkdtemp(prefix="ch04-06-")`+`chdir`)에 다른 이름으로 씀. `data` 폴더 파일을 읽어야 한다면 05절 준비 셀의 경로 분기(`../data` 있으면 그대로, 없으면 `labs/part1/ch04-data-tools/data` — run_section.sh의 커널 cwd는 프로젝트 맨 위 폴더, VS Code·배포 러너는 `notebooks`)를 쓰고, 임시 폴더로 옮길 거면 **옮기기 전에** 파일 글을 변수에 담아 둠
- 05 노트북 셀 순서·출력을 바꾸면 05절 본문 인용·그림 라벨을 다시 대조해야 함(실습 절 작업에서 05를 건드리지 않는 것이 안전)

### 챕터 전체(01~05)에서 가르친 도구·문법·API 한눈에

| 절 | 도구 | 새 문법·API(노트북 실행) | 조회 함수(반환) | 데이터 |
|---|---|---|---|---|
| 01 | pandas 3.0.5 | `import pandas as pd`, `pd.read_csv`(`dtype=str`), `shape`·`dtypes`·`표["열"]`·`== 값` 마스크·`loc[마스크]`·`loc[마스크, "열"]`·`sum()`·`to_dict(orient="records")`·`pd.to_numeric`(`ValueError`), 반환 힌트 `-> list` | `fetch_orders(file_name, status) -> list`(딕셔너리 목록) | `orders.csv` O101 paid 32000 / O102 pending 18000 / O103 paid 27000, paid 59000, 전체 77000 |
| 02 | pandas | `copy()`, `loc[번호, "열"] = 값`, `sorted(os.listdir())`, `is_unique`, `merge(on=, how="left", validate="many_to_one")`, `pd.errors.MergeError`, `drop_duplicates()`, `NaN` 보기 | (함수 없음) | `customers.csv` C001 김하나 / C002 이두리, `orders.csv`에 `customer_id`, 김하나 59000, 짝 없는 C003, `all_customers.csv` 5행 136000 |
| 03 | sqlite3(SQLite 3.53.1) | `sqlite3.connect`·`execute(sql, [값])`·`commit()`·`close()`·`fetchall()`·`rowcount`, `sqlite3.IntegrityError`, SQL `PRAGMA foreign_keys = ON`·`CREATE TABLE`(PRIMARY KEY·NOT NULL·FOREIGN KEY)·`INSERT INTO`·`SELECT`·`WHERE`·`ORDER BY`·`JOIN … ON`·`?` | `find_customer_orders(database_name, customer_id) -> list`(딕셔너리 목록, 키 `order_id`·`name`·`amount`) | `shop.db`, C001 → O101·O103 59000, C002 → O102, 주입 입력 `C001' OR '1'='1` |
| 04 | httpx 0.28.1, 표준 `wsgiref` 연습 서버 | `httpx.get(url, params=, timeout=2.0)`·`url`·`status_code`·`text`·`json()`·`raise_for_status()`, `httpx.HTTPStatusError`, `while page is not None`, 준비 셀만 `subprocess.Popen(...)`·`readline()`·`terminate()`·`wait()`·`poll()` | `fetch_all_orders(orders_url) -> list`(딕셔너리 목록, 키 `order_id`·`customer_id`·`amount`) | `page=1.json`(O101·O102, next 2)·`page=2.json`(O103, null)·`order_server.py`(포트 0), Before 50000 → After 77000 |
| 05 | beautifulsoup4 4.15.0·lxml 6.1.3·soupsieve 2.9.2, 표준 `urllib.robotparser`·`json` | 위 「05절이 새로 가르친 것」 | `parse_article(html_text) -> dict`(딕셔너리 하나) + `find_text()` | `data/article.html` A10, `robots.txt`, `article-text.json` |

- 공통 셀 모양: 준비 셀 `import os`·`import tempfile` → `mkdtemp(prefix="ch04-NN-")` → `os.chdir()` → `os.listdir()`(05만 `data` 폴더로 chdir), 파일 쓰기 `with open("w", encoding="utf-8")`+여러 줄 글, 오류는 이름만 받는 `try/except 오류이름 as error:` + `print("라벨:", error)`, 모으기 빈 목록+`for`+`append()`, 합계 `+=`, 정의 셀(결과 읽기 「출력이 없습니다」)과 호출 셀 분리, 셀 끝 `assert`는 매번 같은 값에만
- 챕터 흐름(실습 절이 조립에 쓸 수 있는 연결): 01~04절 Before는 「오류 없이 틀린/덜 가져온 결과」(글자 합계, 겹친 키, 주입, 첫 페이지만), 05절 Before는 「오류로 멈춤」. After는 모두 「읽기 전에 확인」(자료형, `validate`, 자리표시자, 다음 페이지 번호, `None`)
- 실습에서 이어 쓸 수 있는 조합 후보(판단은 실습 작업자): 04절 연습 서버 방식(파일 글 + `wsgiref` + `Popen`, 포트 0)으로 HTML 페이지를 줄 수도 있음(서버 글의 `Content-Type`을 `text/html`로 — 04·05에서 실행하지 않음, 응답 `text`는 04에서 실행함). 01~04절 주문 데이터(O101~O103, C001 김하나, C002 이두리, 77000)를 쓰면 01~04와 이어짐. 모델 호출은 Ch 4에 없음(Ch 6부터)
- 그림 색(01~05 같음): 파일·요소·요청·값 초록, 실행한 코드·정의한 함수 파랑, 출력으로 확인한 값·받아서 출력한 오류 노랑, Before 결함 결과 빨강(05-3은 받아 출력했지만 함수가 기록을 반환하지 못한 결함이라 빨강 — 검토 대상), 실행하지 않은 다음 챕터·바깥 요소 회색
- 빌드 주의(05에서 확인): 노트북 설명 셀에 `<h1>`·`<p …>`·`<div>`·`<table>`·`<ul>`·`<ol>`·`<details>`를 백틱으로 인용하면 `textbook/_notebook/render.py` `markdown()`이 셀을 HTML로 보고 변환 없이 넣음 → 이런 태그는 인용하지 않음(`<article …>`·`<time …>`·`</h1>`·`<html …>`은 괜찮음). Mermaid 화살표 라벨 줄바꿈은 `<br>`로 직접(05-1)

### 아직 안 가르친 것 (실습 절이 설명 없이 전제하면 안 됨)

- HTML·스크래핑: `select()`·`find_all()`로 여러 요소 모으기, 요소 `.get()`, 속성식 자식 접근(`soup.h1`), 다른 파서, 인터넷 사이트에서 HTML 가져오기, 요청 간격·재시도, `robots.txt` `read()`·`crawl_delay()`, 이용 약관 확인 절차의 실제 실행, 인코딩 판별, JavaScript로 그리는 페이지
- JSON: `json.loads()`·`json.load()`로 파일 다시 읽기(05는 `dumps`만, 04는 응답 `json()`만), `json.dump()`
- 01~04절 handoff의 「아직 안 가르친 것」 그대로: pandas `DataFrame()`·`concat`·열 목록·`iloc`·`groupby`·`isna`, SQL `DESC`·`LIMIT`·집계·`UPDATE`/`DELETE`·`LEFT JOIN`, `executemany`·`row_factory`·`with connection:`, `httpx.Client`·헤더·POST·인증·시간 제한 초과·5xx·다른 페이지 방식
- Python: `raise`·try `else`·`finally`(A 트랙)·내포식·제너레이터 식·조건 표현식·f-string 안 식·`pathlib.Path`·`TemporaryDirectory`·`list[dict]`·`X | None`·`*`·`**` 풀기·`isinstance`·`from 패키지.모듈 import`·`@` 줄·`BaseModel`·`*args`·클래스 상속·`threading`·`lambda`. `subprocess.Popen`은 04 준비 셀에서만(기본 경로 전제 금지), `os.path.exists`는 05 준비 셀에서만(한 문장 설명). 타입힌트는 `: str`·`-> list`·`-> dict`까지(05 `find_text`는 힌트 일부 생략)

## 실습 → 챕터 검토

(06 실습 절 새로 만듦 2026-09-16. 결과는 `06-diagnosis.md`, 게이트 G1~G7 0, 챕터 6/6 PASS(`gates-wip-all.json`), verify `PASS 6 sections / 96 code cells`, `visual.cjs` 14건 PASS, 코드 셀 18(준비 4 + 본 경로 14), 모델 호출 0, 인터넷 접속 없음. 삽화 06-4 채택(job `96165042-…`, 2크레딧). 리뷰 묶음 `review-pack/06-데이터-도구-실습.md`, 05도 다시 묶음)

### 실습 절이 한 것

- 제목 「데이터 도구 실습: 주문 서비스에서 고객별 합계 내기」, 파일 `06-데이터-도구-실습`, experiment. 「강사 시연」 문구 0건(노트북·`_src` 확인)
- 01~04절 조립: 02절 고객 파일 → 01절 `pd.read_csv` + 02절 `is_unique` → 03절 `insert_customers()`(자리표시자 둘, `IntegrityError`를 줄마다 받아 막힌 번호 목록 반환) → 04절 `fetch_all_orders()` 그대로 → 03절 `insert_orders()`(PRAGMA, 자리표시자 셋, `SELECT *` 행 수 반환) → 03절 `total_by_customer()`(JOIN, `get(키, 0)`로 이름별 합계) → Ch 2 13 `print_report()`. 조립 함수 `run_pipeline(customer_file, database_name, orders_url) -> dict`, 기록장 칸 여섯 개
- 실행 1 `customers.csv`/`shop-1.db`: `True`·`[]`·3·3·`{'김하나': 59000, '이두리': 18000}`. 실행 2 `all_customers.csv`/`shop-2.db`: `고객 넣기 오류: C001 UNIQUE constraint failed: customers.customer_id`, `False`·`['C001']`·3·3·같은 합계. `달라진 칸 수: 3`. 확인 셀 파일 3행 vs 테이블 2행
- 05절(HTML 파싱)은 쓰지 않음. `data/article-text.json`·`article.html`·`robots.txt`는 읽지도 쓰지도 않음(임시 폴더 `ch04-06-`만)
- 02절 Before 5행·136000은 다시 실행하지 않고 앞 절 결과로만 비교(b3·b6·복습 3)

### 챕터 연결을 바꾼 곳

- `chapter.json` 06 추가, 05 `_src` b8 → 06 링크(Ch 5 01 문장은 06 b8로 옮김), 05 노트북·`author_05.py` 정리 셀 끝 → 「다음 06절은 이 챕터의 실습입니다. …」(`mdpatch.py`, 05는 다시 실행하지 않음, 05 게이트 0)
- 06 b8: Ch 4 끝, Ch 5 01이 `article-text.json`의 `text` 칸으로 토큰 수, Ch 19 01이 01절 `fetch_orders()`를 도구로 다시 씀(Ch 19 01 본문으로 확인). 05 검토에서 뺀 「반환값만 보고 답」 류 문장은 쓰지 않음
- 챕터 밖 미반영: `textbook/part1/_build_index.py`·`part1/index.html`(Ch 4 절 수 5), `textbook/downloads/` 묶음, `textbook/qa/upgrade-progress.md` Ch 04 행(「대기」 그대로)

### 챕터 검토 세션이 볼 곳

- 06: 실행 2에서 달라진 칸이 앞의 두 확인 칸뿐인 설계(뒤 결과가 같다는 것이 결론), `insert_orders()`에 오류 받는 줄이 없는 판단(b7에 「실행하지 않음」), 04절 준비 코드 세 셀 반복 분량, 06-3 실행 2 노랑 판단, 삽화 06-4(접시 카드 크기·파랑 서류철 테두리)
- 01~05 전체: `illustration-pending.md`의 02-5 삽화 대기(2회 탈락) 그대로, 05-3 Before 빨강 판단, 05 준비 셀 `data` 폴더 `chdir`
- 챕터 요약 `chapter-summary.md`는 아직 없음(검토 뒤 작성). 쓸 때 06 실습 주제·결과와 「아직 안 가르친 것」(05 handoff 목록 + 06에서도 쓰지 않은 `pd.DataFrame()`·`drop_duplicates(subset=)`·SQL 집계·`executemany`·`with connection:`)을 옮김

### 06에서 새로 쓴 이름 (다음 챕터·검토용)

- 함수 `insert_customers(database_name: str, customers) -> list`, `insert_orders(database_name: str, orders: list) -> int`, `total_by_customer(database_name: str) -> dict`, `run_pipeline(customer_file: str, database_name: str, orders_url: str) -> dict`, `print_report(report)`(Ch 2 13 그대로)
- 파일 `shop-1.db`·`shop-2.db`, 변수 `customer_file`·`orders_url`·`report_1`·`report_2`·`changed_count`·`all_customers`·`customer_rows`, 라벨 「고객 넣기 오류:」·「연결한 행 수:」·「고객 파일의 행 수:」·「고객 테이블의 행:」·「고객 테이블의 행 수:」
- 비유 삽화 06-4: 창구·쟁반·깃발(04-5) → 두 칸 카드 꽂이(고객 테이블 기본 키, 초록 = C001 김하나, 파랑 = C002 이두리) → 접시의 초록 카드(막힌 C001) → 색별 서류철 묶음(고객별 합계)
- 그림 색: 고객 파일·바꾸는 값 초록, 부르는 코드·부품 파랑, 기록장·받아 출력한 오류 노랑, 문제 없음 회색, 빨강 없음

## §2-7 확인 (2026-09-21)

규격 `textbook/QUALITY-UPGRADE.md` §2-7(앞에서 배운 함수는 도구 파일에서 가져오고, 벡터 계산은 NumPy로). **결정: 그대로(노트북·생성기·`_src` 바꾸지 않음).**

### 조사(AST, 노트북 6개·코드 셀 96개·코드 줄 669, 최상위 함수 정의 14개)

| 이름 | 정의한 절(코드 셀) | 본문 비교(AST) | 그 자리의 역할 |
|---|---|---|---|
| `fetch_all_orders` | 04(c30, After) · 06(c26) | **같음**(12줄) | 06 실습 「8. 부품 준비 — 주문을 끝까지 받아 넣기」, 본문은 「04절 After의 `fetch_all_orders()`를 그대로 가져옵니다」 |
| `print_report` | 06(c35) | Ch 2 13절 c37과 **같음**(3줄) | 06 「10. 기록 장치」 |
| `fetch_orders`(01) · `find_customer_orders`·`find_orders_before`(03) · `fetch_orders_before`(04) · `parse_article_before`·`find_text`·`parse_article`(05) · `insert_customers`·`insert_orders`·`total_by_customer`·`run_pipeline`(06) | 한 절씩 | 되풀이 없음 | 각 절 학습 대상 |

- 01~05절 안 되풀이 정의는 0개. 되풀이는 06 실습 두 개, **코드 15줄(2.2%)**. 벡터 계산 0곳(NumPy 해당 없음).
- 함수가 아닌 되풀이: 06 준비 셀 셋(페이지 글 두 개·`order_server.py` 글·`subprocess.Popen`, 약 37줄, 셀 주석 「04절과 같음」). §2-7은 앞에서 배운 **함수**를 대상으로 하고, 이 셋을 함수로 묶으면 04절에서 가르치지 않은 새 함수를 만드는 것이라 대상 밖으로 둠.

### 결정: 그대로 — 까닭

1. **줄지 않음**: 둘을 도구 파일로 옮기면 06 노트북은 −15줄 + 가져오기 한 줄 = −14줄(167 → 153)이지만, 도구 파일이 약 16줄(`import httpx` + 함수 둘)이라 챕터 전체는 +2줄. 파일 하나를 한 절이 함수 두 개 때문에 쓰는 모양이고, 규격 3항에 덧붙인 「도구 파일을 더하면 챕터 전체 코드가 줄지 않는 챕터에는 만들지 않음」에 해당.
2. **같은 실습 폴더에 이미 `data_tools.py`가 있음**: 실습 폴더 루트의 `data_tools.py`(`fetch_orders`·`find_customer_orders`·`fetch_articles`·`parse_article_html`)는 pytest(`tests/test_data_tools.py`)가 확인하고 Ch 19 01절이 도구로 다시 쓰는 참고 모듈이고, 06 3번과 README가 이 파일을 그렇게 소개함. 노트북 폴더에 이름과 역할이 비슷한 도구 파일을 하나 더 두면 학생이 두 파일을 헷갈릴 수 있음. `data_tools.py`는 사다리 밖 문법(내포식·`or`·키워드 전용 인자)을 쓰고 노트북 폴더 밖에 있어 노트북이 가져오는 도구 파일로도 쓸 수 없음.
3. 06 실습의 「부품 준비」는 01~05절 도구를 한 노트북에 모아 다시 보이는 절이고, 조립도(06-1)의 `fetch_all_orders()` 상자와 노트북 코드가 한곳에서 맞음.

- Ch 5 `llm_tools.py`의 `print_report` 주석 「Ch 2 13절·Ch 4 06절에서 배웠습니다」는 그대로 맞음.
- 바꾼 파일 없음. 이 절만 덧붙임. 스냅숏 `before-2-7/`도 만들지 않음.
