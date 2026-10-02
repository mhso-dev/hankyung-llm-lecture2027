# Ch 04 데이터 다루기 — 도구 제작 관점 — 챕터 요약 (다음 챕터 작업자용)

작성 2026-09-16(품질 개선 5절 + 실습 절 06 + 별도 세션 검토 1차 반영 뒤). 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md` §6. 앞 챕터 요약: `textbook/part1/ch01-development-environment/qa/upgrade/chapter-summary.md`, `textbook/part1/ch02-python/qa/upgrade/chapter-summary.md`, `textbook/part1/ch03-git-github/qa/upgrade/chapter-summary.md`. 절 사이 인계 원문: `qa/upgrade/handoff.md`. 검토: `qa/upgrade/review-round1.md`(끝에 「반영 결과」).
절: 01 Pandas로 표 다루기 · 02 관계형 테이블과 키 · 03 SQL로 조회 함수 만들기 · 04 REST와 페이지네이션 · 05 문서 파싱과 스크래핑 · 06 데이터 도구 실습(experiment). 01~05는 paired. 모델 호출 0번, API 키 불필요, 인터넷 접속 없음. 코드 셀 96개(16·16·20·13·13·18), 게이트 6/6(G1~G7 0, 수정 전 237건). **삽화 1장 대기(02-5)**, 나머지 삽화 5장·Mermaid 23장.

## 1. 새로 가르친 도구·API·문법·용어

### 절별 도구와 API (노트북에서 실행한 것만)

| 절 | 도구 | API·SQL | 조회 함수(반환) |
|---|---|---|---|
| 01 | pandas 3.0.5 | `import pandas as pd`, `pd.__version__`, `pd.read_csv(이름)`(인자 `dtype=str`), `print(표)`(인덱스), `shape`·`dtypes`, `표["열"]`(시리즈), `== 값`(불리언 마스크), `표.loc[마스크]`·`표.loc[마스크, "열"]`, 시리즈 `sum()`·`dtype`, `표.to_dict(orient="records")`, `pd.to_numeric()`(`ValueError: Unable to parse string "미정" at position 1`), 같은 열 이름에 다시 대입 | `fetch_orders(file_name: str, status: str) -> list`(딕셔너리 목록) |
| 02 | pandas | `표.copy()`, `표.loc[인덱스, "열"] = 값`(대입 기호 왼쪽 `loc`는 저장), `sorted(os.listdir())`, 시리즈 `is_unique`, `표.merge(오른쪽, on=)`(기본 내부 조인)·`how="left"`(`NaN`)·`validate="many_to_one"`(`pd.errors.MergeError`), `drop_duplicates()`(인자 없음) | 없음 |
| 03 | sqlite3(SQLite 3.53.1) | `import sqlite3`·`sqlite3.sqlite_version`·`connect()`·연결 `execute(sql)`/`execute(sql, [값])`·`commit()`·`close()`, 커서 `fetchall()`(튜플 목록)·`rowcount`, `sqlite3.IntegrityError`. SQL `PRAGMA foreign_keys = ON`, `CREATE TABLE`(`TEXT`·`INTEGER`·`PRIMARY KEY`·`NOT NULL`·`FOREIGN KEY … REFERENCES`), `INSERT INTO … VALUES`, `SELECT … FROM`, `WHERE 열 = '값'`, `ORDER BY 열`(방향을 적지 않으면 작은 값부터, `DESC`는 실행 안 함), `JOIN … ON 표.열 = 표.열`, `OR`, 자리표시자 `?` | `find_customer_orders(database_name: str, customer_id: str) -> list`(키 `order_id`·`name`·`amount`) |
| 04 | httpx 0.28.1, 표준 `wsgiref` 연습 서버 | `import httpx`·`httpx.__version__`, `httpx.get(주소, params={"page": n}, timeout=2.0)`(단계마다 최대 2초), 응답 `url`·`status_code`·`text`·`json()`(`null` → `None`)·`raise_for_status()`(`httpx.HTTPStatusError`, `Client error '404 Not Found' for url …`), `while page is not None:`. 준비 셀에서만 `subprocess.Popen([sys.executable, "order_server.py"], stdout=subprocess.PIPE, …)`·`stdout.readline()`·`terminate()`·`wait()`·`poll()` | `fetch_all_orders(orders_url: str) -> list`(키 `order_id`·`customer_id`·`amount`) |
| 05 | beautifulsoup4 4.15.0·lxml 6.1.3·soupsieve 2.9.2, 표준 `urllib.robotparser`·`json` | `os.path.exists()`(준비 셀), `urllib.robotparser.RobotFileParser()`·`parse(줄 목록)`·`can_fetch(이름, 주소)`, `bs4.BeautifulSoup(글, "lxml")`·`prettify()`·`select_one(선택자)`(없으면 `None`)·요소 `.name`·`get_text(strip=True)`·`요소["속성"]`, `AttributeError`(`'NoneType' object has no attribute 'get_text'`), `import json`·`json.dumps(값, ensure_ascii=False, indent=2)`, 글자 `replace()`·`"\n"` | `find_text(parent, selector: str)` + `parse_article(html_text: str) -> dict`(딕셔너리 **하나**) |
| 06 | 새 API 없음 | 01~04 조립(§3) | `insert_customers`·`insert_orders`·`total_by_customer`·`run_pipeline` |

### Python 쪽에서 Ch 4가 새로 쓴 모양 (모두 한 문장씩 풀었음)

- 별명 import `import pandas as pd`(01), 모듈 속성 `__version__`(01·04·05, Ch 2 07 `__name__`에 연결), 반환 힌트 `-> list`·`-> dict`·`-> int`(Ch 2 07 `-> int` 모양), 오류 이름 점 이음 `pd.errors.MergeError`·`sqlite3.IntegrityError`·`httpx.HTTPStatusError`·`import urllib.robotparser`(`from 패키지.모듈 import`는 쓰지 않음)
- 키워드 인자에 딕셔너리 `params={"page": 1}`, 반복 안에서 다음 값 대입 `page = body["next_page"]`, 여러 줄 f-string `f"""…'{customer_id}'…"""`(03 Before 전용, 변수만), 목록 안 튜플 풀기 `for page_name, one_record in page_records:`, `totals.get(name, 0) + amount`(06)
- 표·목록 출력은 라벨을 앞줄에 따로 `print("주문 표:")` 다음 줄 `print(orders)`(검토 C-2, 규격 §2-4에 추가)
- `raise`·try `else`/`finally`·내포식·제너레이터 식·조건 표현식·f-string 안 식·`lambda`·`pathlib.Path`·`TemporaryDirectory`·`list[dict]`·`X | None`·`*`·`isinstance`·클래스 상속·`threading`·`@`·`BaseModel`은 기본 경로 코드 셀 96개에서 0건(검토 AST 확인)

### 용어 표에 넣은 것

CSV·데이터프레임·행과 열·인덱스·자료형(dtype)·시리즈·불리언 마스크(01) / 기본 키·외래 키·다대일 관계·정규화·조인·내부 조인·왼쪽 조인·결측값(02) / 데이터베이스·SQL·테이블·연결·커서·제약·커밋(Git 커밋과 이름만 같음)·자리표시자·SQL 주입(03) / HTTP·요청과 응답·서버와 포트·쿼리 문자열·상태 코드·JSON·REST API·페이지네이션·시간 제한(04) / 스크래핑·robots.txt·HTML·태그와 요소·속성·파싱과 파서·요소 트리·CSS 선택자·class 속성(05).

## 2. 반복해 쓴 데이터·함수·서버·파일·비유·이름

- **주문 세 건(01~04·06)**: O101 C001 paid 32000 / O102 C002 pending 18000 / O103 C001 paid 27000. 결제 완료 합계 59000(= 김하나 합계, 「두 주문이 마침 모두 결제 완료」), 전체 77000. 금액은 원 단위 정수
- **고객 두 명(02·03·06)**: C001 김하나, C002 이두리. 짝 없는 번호 C003(02·03은 「고객 표에 없는 번호」, 실습 폴더 `data/customers.csv`의 C003 박세진과 다름). 겹친 고객 파일 `all_customers.csv`(C001 줄 두 번) → 02 Before 5행·136000
- **파일·이름**: 준비 셀 `import os`·`import tempfile` → `practice_folder = tempfile.mkdtemp(prefix="ch04-NN-")` → `os.chdir()` → `os.listdir()`(05만 실습 폴더 `data`로 chdir). `orders.csv`·`customers.csv`·`all_customers.csv`(01·02·06), `shop.db`(03)·`shop-1.db`/`shop-2.db`(06), `page=1.json`(O101·O102, next 2)·`page=2.json`(O103, null)·`order_server.py`(04·06), `data/article.html`(기사 A10 「골목상권 매출 회복」, 270글자)·`data/robots.txt`·`data/article-text.json`(05)
- **연습용 주문 서비스(04·06)**: 준비 셀이 쓴 `order_server.py`(`wsgiref.simple_server.make_server("127.0.0.1", 0, answer)`, 쿼리 문자열 `page=1` → 파일 `page=1.json`, 없으면 404), `Popen`으로 켜고 첫 줄 포트 번호를 읽어 `base_url`, 마지막 셀에서 `terminate()`·`wait()` → `서비스가 아직 켜져 있는가: False`. 포트 번호는 인용하지 않음
- **Before/After 흐름**: 01~04 Before는 「오류 없이 틀린/덜 가져온 결과」(글자 합계 `320001800027000`, 겹친 키 5행, 주입 3건, 첫 페이지만 50000), 05 Before는 「오류로 멈춤」(AttributeError). After는 모두 「읽기 전에 확인」(자료형, `validate`, 자리표시자, 다음 페이지 번호, `is None`)
- **비유와 삽화**: 01-5 창을 낸 덮개(마스크) → 02 쪽지 색 스티커와 카드 상자(**삽화 대기**, 글로만) → 03-5 요청서 빈칸·분홍 쪽지·투명 봉투·서류철(초록 김하나, 파랑 이두리)·빈 쟁반 → 04-5 창고 창구·쟁반(한 페이지)·깃발(`next_page`) → 05-5 나무 상자 안 흰 카드·색 스티커(class)·노란 스티커 쟁반(선택자)·빈 쟁반(`None`) → 06-4 카드 꽂이(기본 키)·접시의 초록 카드(막힌 C001)·색별 서류철 묶음(고객별 합계). 일상 예: 식당 주문서·영수증(요청·응답), 택배 송장(JSON), 건물 호수(포트), 도서관 서고와 사서(데이터베이스), 출석 번호(기본 키)
- **실습 폴더 `data_tools.py`(고치지 않음, pytest 10개)**: `fetch_orders(csv_path, *, status=None)`, `find_customer_orders(database, customer_id)`(키 `customer_name`·`status`, 금액 내림차순), `fetch_articles(base_url, *, category, timeout, client)`, `parse_article_html(html)`. 노트북 함수와 이름은 같거나 비슷하지만 모양이 다르고, 01·03·04·05 본문 주의 메모에 적음

## 3. 06 실습 절 주제와 결과

- 「데이터 도구 실습: 주문 서비스에서 고객별 합계 내기」(experiment, 30분, 모델 호출 0번, 따로 과제 없음). 부품: 03절 `insert_customers(database_name, customers) -> list`(`IntegrityError`를 받아 막힌 번호 목록), 04절 `fetch_all_orders()` 그대로, 03절 `insert_orders(database_name, orders) -> int`(PRAGMA, 오류 받는 줄 없음, `SELECT *` 행 수), 03절 `total_by_customer(database_name) -> dict`(JOIN, `get(키, 0)`), Ch 2 13절 `print_report()`. 조립 `run_pipeline(customer_file, database_name, orders_url) -> dict`, 기록장 칸 여섯 개
- 실행 1 `customers.csv`/`shop-1.db`: `고객 번호가 모두 다른가 | True`, `넣지 못한 고객 | []`, 받은 주문 수 3, 주문 테이블의 행 수 3, `연결한 행 수: 3`, `{'김하나': 59000, '이두리': 18000}`
- 실행 2 `all_customers.csv`/`shop-2.db`(값 하나만 바꿈): `고객 넣기 오류: C001 UNIQUE constraint failed: customers.customer_id`, `False`, `['C001']`, 나머지 같음. `달라진 칸 수: 3`(고객 파일 포함). 확인 셀 `고객 파일의 행 수: 3` vs `고객 테이블의 행 수: 2`
- 결론(검토 06-1 반영): 받은 주문 수와 주문 테이블의 행 수는 고객 파일과 관계없는 칸이라 같았고, **기본 키가 겹친 줄을 막아 연결한 행 수와 고객별 합계가 같았음**. 번호와 이름이 모두 같은 겹친 줄 한 가지로 관찰한 것
- 재실행 주의(검토 06-2, 기기 셸에서 같은 함수로 확인, 노트북 출력에는 없음): 실행 1·2 셀만 같은 데이터베이스로 다시 실행하면 고객은 넣기 오류로 기록되고 주문은 `IntegrityError: UNIQUE constraint failed: orders.order_id`로 멈추며, 닫히지 않은 연결 때문에 다른 연결 쓰기가 `database is locked`
- 05절(HTML 파싱)과 `data` 폴더는 06에서 쓰지 않음

## 4. 다음 챕터(Ch 05 LLM 동작 원리: 토큰화·임베딩·어텐션·컨텍스트·temperature·환각·모델 선택)가 이어받을 것

- **`labs/part1/ch04-data-tools/data/article-text.json`(Ch 5 01이 읽는 파일)**: `{"schema_version": "ch04-parsed-article-v1", "source": "labs/part1/ch04-data-tools/data/article.html", "record": {"id": "A10", "title": "골목상권 매출 회복", "summary": "주말 방문객 증가로 음식점 매출이 늘었습니다.", "published": "2026-09-01", "text": "골목상권 매출 회복\n주말 방문객 증가로 음식점 매출이 늘었습니다."}}`, `indent=2`, 끝 줄바꿈 하나, SHA-256 `e241854443edac502e0a9e090191ace34dbced1885a600db3af29a20a93103d1`(검토 반영 전후 같음). Ch 4 05 노트북이 다시 쓰고, `textbook/qa/run_course_bundle.py`가 05 노트북을 `notebooks` 폴더에서 실행해 바이트를 비교함. **이름·경로·칸 이름·글을 바꾸지 않습니다**
- **Ch 5 01 노트북 셀 4(개선 전, 2026-09-16 확인)**: 작업 폴더와 조상 폴더를 `for`로 올라가며 `labs/part1/ch04-data-tools/data/article-text.json`을 찾고 `schema_version`·`source`·`record.id`·`record.text`를 읽어 두 토큰화기로 셈(개선 전 출력 `GPT-2: 81 | KLUE: 17`). 셀 10은 `schema_version`·`record.id == "A10"`·`text`를 `assert`. 이 셀은 Ch 1~4 기본 경로에서 가르치지 않은 `from pathlib import Path`·`Path.cwd().parents`·`Path / "…"`·`exists()`·`read_text()`·`raise FileNotFoundError`·`json.loads()`·`repr()`·`assert A and B`를 씀 → **Ch 5 작업자의 전제 금지 목록**. Ch 4 05 준비 셀의 경로 분기(`os.path.exists("../data")`면 `../data`, 아니면 `labs/part1/ch04-data-tools/data`)와 `with open(…, encoding="utf-8")`+`file.read()`로 바꾸면 이어짐. JSON을 다시 읽는 `json.loads()`는 Ch 4에서 실행하지 않았으므로(05는 `dumps`, 04는 응답 `json()`) 처음 쓰는 자리에서 「04절 `response.json()`처럼 JSON 글을 딕셔너리로 바꿈」 한 문장
- 「앞에서 배운 내용」에 쓸 수 있는 것: 05절 「제목과 요약을 줄바꿈 한 글자로 이은 `text` 칸」, 04절 JSON·딕셔너리, 01절 표·시리즈(임베딩 비교 표를 pandas로 보일 때 `read_csv`·`loc`·`dtypes`), 03절 「오류 없이 틀린 결과」 습관, 준비 셀 `mkdtemp(prefix="ch05-NN-")`
- Ch 4 06 b8 「다음 학습」: 「Ch 4는 이 절에서 끝납니다. 05절에서 쓴 `data/article-text.json`은 Ch 5 01절이 직접 읽습니다. 그 절은 파일의 `text` 칸 … 두 토큰화기로 나눠 토큰 수를 셉니다.」 Ch 5 01을 고쳐 토큰화기·출력이 바뀌면 이 문장을 확인합니다
- **Ch 19 01(검토 C-1)**: Ch 19 01 노트북은 실습 폴더 `data_tools.py` 판 `fetch_orders(csv_path, *, status=None)`와 `data/orders.csv`(O104 C003 cancelled 9000 포함)를 씀(셀 5 선언, 셀 9 `status="cancelled"`). Ch 4 01절 함수 `fetch_orders(file_name, status)`와 모양이 다르다는 사실을 01 b7·03 b7·06 b8에 적음. Ch 19 작업 때 01절 모양과의 차이를 한 문장으로 잇거나 모양을 맞출지 결정. Part 5·6에서 `find_customer_orders`·`fetch_articles`·`fetch_all_orders`는 쓰지 않음
- Ch 1~3 요약의 이어받을 것(준비 셀, `with open`, 결과 읽기 방식, `.gitignore` 확인 습관)은 그대로 유효

## 5. 아직 가르치지 않은 것 (다음 챕터가 전제하면 안 되는 것)

- pandas: `pd.DataFrame()`으로 표 만들기, `concat`, 열 목록 `표[["a", "b"]]`, `iloc`, `head()`·`value_counts()`·`groupby`·`sort_values`, `astype`·`assign`, `isna`·결측값 처리, `read_csv`의 열별 `dtype={…}`·`errors="coerce"`, `tolist()`, `to_string()`, `drop_duplicates(subset=, keep=)`·`duplicated()`, 인덱스 다시 매기기, `read_sql`·`to_sql`
- SQL·sqlite3: `DESC`·`LIMIT`·`COUNT`·`SUM`·`GROUP BY`·`UPDATE`·`DELETE`·`LEFT JOIN`·별칭 `AS`·주석 `--`·이름 붙은 자리표시자, `executemany`·`executescript`·`row_factory`·`sqlite3.Row`·`with connection:`·`rollback()`, 한 원소 튜플 `(x,)`(주의 메모에만)
- HTTP: `httpx.Client`, 헤더·`Content-Type`(서버 글 안에만), POST·인증·API 키 헤더, 시간 제한 초과, 5xx, 재시도·대기, 커서·다음 주소 방식 페이지, 인터넷 서비스 호출
- HTML·JSON: `select()`·`find_all()`, 요소 `.get()`, 속성식 접근 `soup.h1`, 다른 파서, 인터넷 페이지 가져오기, `robots.txt` `read()`·`crawl_delay()`, 인코딩 판별, `json.loads()`·`json.load()`·`json.dump()`
- Python: `raise`·try `else`/`finally`(A 트랙)·내포식·제너레이터 식·조건 표현식·f-string 안 식·`lambda`·`pathlib.Path`·`TemporaryDirectory`·`list[dict]`·`X | None`·`*`(06 b8·01·03 b7에서 `data_tools.py` 모양으로 보이기만 함, 01 b7에 뜻 한 문장)·`**` 풀기·`isinstance`·`from 패키지.모듈 import 이름`의 점 경로·`@`·`BaseModel`·`*args`·클래스 상속·`threading`·`repr()`. `subprocess.Popen`은 04·06 준비 셀에서만, `os.path.exists`는 05 준비 셀에서만(기본 경로 전제 금지). 타입힌트는 `: str`·`-> list`·`-> dict`·`-> int`까지
- 모델: 토큰·토큰화기·임베딩·모델 호출은 Ch 4에서 전혀 쓰지 않음. 「에이전트 도구」는 연결 문장으로만 언급(모델 동작은 실행하지 않음)

## 6. A·B 트랙 제약 (Ch 2에서 넘어온 것, 그대로 유지)

- A 트랙(기본 경로)은 Ch 2 09~11절(데코레이터 `@`·컨텍스트 매니저 원리, Pydantic `BaseModel`, 패키징·픽스처)을 건너뜀. Ch 4는 이 문법을 한 번도 쓰지 않았으므로 **A 학생 기준 전제는 Ch 2 요약 §5 + Ch 3·Ch 4의 위 목록**
- 규격 §2-2: Part 2 이후 절이 `@` 줄이나 `BaseModel`을 처음 쓰면 세 문장으로 풀고 Ch 2 09·10절을 링크. `*args`·`**kwargs`·`*목록` 풀어 넘기기도 A 트랙 미교육
- try `finally`는 Ch 2 09절(B 트랙)에서만 배웠으므로 Ch 4는 「오류가 나도 연결을 닫는 방법(확장 경로)」으로 문장만 둠(03 b7)

## 7. 기준 버전 (교재 출력 2026-09-16, Linux aarch64, Python 3.12.13)

- pandas **3.0.5**(Python 3.11 이상, pandas 2 이하 실행 안 함), SQLite **3.53.1**(Python 3.12 sqlite3는 SQLite 3.7.15 이상 요구, 외래 키 검사는 3.6.19부터), httpx **0.28.1**(Python 3.8 이상, 실습 폴더 `uv.lock` 194~195행 고정, 2026-09-16 PyPI 최신 정식판도 0.28.1, 1.0 개발판 실행 안 함), beautifulsoup4 **4.15.0**·lxml **6.1.3**·soupsieve **2.9.2**, pytest 9.1.1
- 실습 폴더 `pyproject.toml`은 `requires-python = "==3.12.*"`와 위 버전을 `==`로 고정. 각 절 노트북 준비물에 기준 버전을 적음. Windows·macOS는 실행하지 않음(05 b7: Windows에서는 `article-text.json` 줄바꿈 바이트가 달라 보일 수 있다고 적음)

## 8. 그림 색 판단 선례

- 파일·표·열·테이블·요소·요청·서비스가 준 값·함수 인자 **초록**, 실행한 코드·SQL 조각·정의한 함수 **파랑**, 출력으로 확인한 행 수·합계·반환값·상태 코드 **노랑**, 인덱스·실행하지 않은 다음 챕터·바깥 요소·「문제 없음」 **회색**, Before 결함 결과 **빨강**
- **코드가 받아 출력한 오류는 노랑**(02 `MergeError`, 03 제약 오류, 04 404, 06-3 실행 2 넣기 오류 — Ch 3 06-3 규칙 그대로)
- **05-3 AttributeError는 빨강**: 노트북은 셀을 이어 가려고 받았지만, 함수가 할 일(기록 반환)을 못 한 Before 결함 결과라 규격 §5-3 「Before 결함 결과는 빨강」(검토 Q5에서 유지)
- sequenceDiagram: 참여자 회색, 메모 노랑, 실선 요청 → 점선 응답, `messageAlign: left`(04-1·06-2). 응답만 있고 요청이 없으면 요청 라벨에 합침(06-2 `INSERT 주문 O101~O103 · SELECT *`)
- Mermaid 주의: 화살표 라벨에는 따옴표를 쓰지 않음(`&quot;`로 보임), subgraph 제목에 `<br>` 금지, 줄바꿈은 `<br>`로 직접, 노트북 설명 셀에 `<h1>`·`<p>`·`<div>`·`<table>`을 백틱으로 인용하면 `render.py`가 HTML로 봄. 화살표 선이 라벨 글자를 가로지르는 문제(01-1·05-1·05-2·06-1·02-3)는 공용 `config.json` `edgeLabelBackground` 검토로 넘김(검토 C-3, 이 챕터 미반영)

## 9. 강사 확인 대상

- 03절 강의·실습 범위: 강의 4~10번(테이블 만들기~JOIN)과 14·15·17·18번(조회 함수·Before/After), 2·3번·11~13번·16번은 함께 실행하고 결과 읽기는 실습 시간에(검토 Q3). 03은 코드 셀 20·검사 문장 416으로 챕터 최대
- 01절 Before `dtype=str` 설정과 앞자리 0 번호 까닭(Q1), 02절 `loc` 대입 한 줄 설명 수준(Q2), 04절 준비 셀 서버 방식(`wsgiref`+`Popen`)과 `PIPE`·`readline()` 설명 수준(Q4), 05절 `data` 폴더 chdir와 05-3 빨강(Q5), 06 비교 3칸·준비 셀 4개·06-3 노랑(Q6)
- 기준 버전 표기(pandas·SQLite·httpx·bs4)
- 규격에 더한 두 규칙(§2-4 여러 줄 출력 라벨, §7-2 뒤 챕터 연결)
- 삽화 02-5 대기 상태로 챕터를 마감한 것

## 10. 남은 것

- **삽화 1장 대기(02-5)**: `figures/02-5-쪽지와-카드-상자.prompt.md`(2회 탈락, 「다음 시도 프롬프트」 있음), `qa/upgrade/illustration-pending.md`. 절당 재생성 한도를 써서 이번 마감에서 만들지 않음. 넣을 때 `_src` 주석을 `{{img:…}}`+「그림 읽기」로 바꾸고 `run_section.sh … 02 --no-exec`·게이트·저장 PNG 대조
- 다운로드 묶음: `textbook/downloads/part1-practice.zip` 안 Ch 4는 개선 전 노트북 5개(06 없음)와 개선 전 README. 전체 마감 때 일괄 재생성
- Part 목차: `textbook/part1/_build_index.py`(Ch 4 절 수 5)와 `textbook/part1/index.html`. 전체 마감 때 재생성
- 정리 대상(삭제하지 않고 목록만): `figures/01-dataframe-flow.*`·`02-relational-keys.*`·`03-sql-query.*`·`04-rest-pagination.*`·`05-document-parsing.*`(옛 Excalidraw·SVG, 본문에서 뺌), `figures/_gen_figures.py`(옛 도식 생성기), `qa/upgrade/__pycache__/`(`author_05.cpython-310.pyc` 등), `qa/upgrade/gates-wip-*.json`(절 작업 중간 기록), `textbook/_notebook/checks/ch04-data-tools/`(visual.cjs 결과, 챕터 밖), 기기 `/tmp/venv-ch04-data-tools`(224MB)·`/tmp/ch04-01`·`/tmp/ch04-04-proto`·`/tmp/ch04-04-vis`·`/tmp/ch04-05-vis`·`/tmp/ch04-06-proto`·`/tmp/ch04-review`·`/tmp/ch04-close`(작업자 임시 폴더), 01 진단 기록의 `$HOME/ch04-01-hold/uv-archive-v0/`(01절 작업 세션이 옮긴 uv 캐시 113MB, 이번 마감 세션의 홈에서는 보이지 않아 확인하지 못함)
- 공용 설정 검토 넘김: Mermaid `edgeLabelBackground`(검토 C-3)
- `집필점검표.md` 위 체크 목록은 개선 전(2026-09-09) 기록이라 검토 1차 반영 때 현재 기준 문장을 덧붙임
- 2차 검토(`review-round1.md` 끝 「반영 결과」의 볼 곳), 강사 확인
