# Ch 02 파이썬 프로그래밍 — 챕터 요약 (다음 챕터 작업자용)

작성 2026-09-16(품질 개선 12절 + 실습 절 13 + 별도 세션 검토 1차 반영 뒤). 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md` §6. 앞 챕터 요약: `textbook/part1/ch01-development-environment/qa/upgrade/chapter-summary.md`.
절: 01 변수와 자료형 · 02 조건문과 반복문 · 03 자료구조 · 04 함수 · 05 파일과 예외 · 06 클래스 · 07 모듈과 타입힌트 · 08 pytest · 09 데코레이터와 컨텍스트 매니저(B) · 10 Pydantic(B) · 11 패키징과 테스트 격리(B) · 12 async와 await · 13 파이썬 실습(experiment). 01~12는 paired. 모델 호출 0번, API 키 불필요. 코드 셀 190개(게이트 13/13, G1~G7 0).

## 1. 새로 가르친 문법·API·용어

### 절별 문법 (기본 경로 사다리 위치)

| 절 | 경로 | 새로 가르친 것 | 사다리 |
|---|---|---|---|
| 01 | A·B | 변수·대입(「오른쪽 값에 왼쪽 이름을 붙여 저장」), 이름 규칙(숫자 시작 금지·밑줄·예약어·대소문자), 자료형 int·float·str·bool과 `type()`, 정수×실수=실수, 다시 대입해도 앞 계산은 그대로, 변수만 넣은 f-string, 형 변환 `int()`, 예약어 | L1 |
| 02 | A·B | 여러 줄 `if/elif/else`, `>=`·`<`, `for` 안의 조건문, 경계값, `range(끝)`·`range(시작, 끝)`(끝 제외), `while`, `break`·`continue`, `enumerate()`, 위치 번호 0부터. 심화만 `IndexError` | L1 |
| 03 | A·B | 슬라이싱 `[0:2]`, `append()`, 빈 목록+`for`+`append()`로 모으기(이후 교재의 기본 모양), `+=`, 튜플과 풀어 담기, 딕셔너리 키 읽기·추가·`in`·`get(키, 기본값)`·`items()`, 집합 `set()`, `sorted()`, `is`(같은 목록 하나)와 `==`(내용), `copy()`. 심화만 튜플 `TypeError` | L1 |
| 04 | A·B | `def`·매개변수·인자·호출·`return`, return 없으면 `None`(`is None` 검사), 지역 변수, 기본값 매개변수(`quantity=1`), 기본값 목록 공유 결함과 `tags=None`+`if tags is None:`, 내장 함수 `round()`(가운데 .5는 짝수 쪽 — 실행 안 함). 정의 셀/호출 셀 분리 | L2 |
| 05 | A·B | `open(이름, "w"/"r", encoding="utf-8")`, `with ... as file:`(끝나면 닫힘, `file.closed`), `write()`(글자 수 반환)·`read()`·`splitlines()`·`split(",")`, 키워드 인자(호출 괄호 안에서 이름으로 넣기 — 정의 줄의 기본값과 다름), 예외, `try`/`except 오류이름 as error:`, `FileNotFoundError`·`ValueError`·`Exception`. 이름 없는 `except:`는 쓰지 않는다고만 적음 | L3 |
| 06 | A·B | `class`, 클래스 이름 규칙, 메서드, `__init__`, `self`, 인스턴스, 속성 읽기·저장, 메서드 호출, 클래스 속성과 인스턴스 속성(인스턴스에 없는 이름은 클래스에서 찾음), `type()` → `<class '__main__.OrderLine'>`. 심화만 `__dict__` | 클래스 정의 셀 예외(§2-4) |
| 07 | A·B | 모듈(Ch 1 3절 「import 뒤에 적는 기능 묶음」 + 직접 만드는 `.py` 파일 하나), `import 모듈`·`모듈.이름`, `from 모듈 import 이름`, 표준 라이브러리, `__name__`과 `__main__`, 처음 불러올 때 한 번 실행, 타입힌트 `매개변수: 자료형 = 기본값`·`-> 자료형`(값을 검사하지 않음). 심화만 `__annotations__` | L4 |
| 08 | A·B | 테스트·기대값·테스트 함수(`test_`, `assert`), pytest 찾기 규칙, `run_pytest() -> int`(`subprocess.run([sys.executable, "-m", "pytest", "-q", "--color=no"], capture_output=True, text=True)`), 결과 줄(점·F·`E` 줄·`파일:줄번호`·`N passed`), 종료 코드 0/1, 회귀 테스트. 심화만 `@pytest.mark.parametrize` | L4 |
| 09 | B | 함수를 값처럼 담기, 데코레이터 정의(함수 안의 함수·`*args`/`**kwargs` — 이 절 정의 셀만 `upgrade_allow`), `@` 줄, `@wraps(function)`, `@contextmanager`와 `yield`, `try`/`finally`. 심화만 `__enter__`·`__exit__` | L6 |
| 10 | B | 데이터 검증, 모델(언어 모델과 다른 뜻), 상속 모양 `class OrderLine(BaseModel):`(뜻만), 필드, 키워드 인자로 인스턴스 만들기, `ValidationError`(`type=int_parsing` 등), 자동 변환, `model_validate()`·`model_dump()`, `Field(ge=, le=)`, `error.errors()`, `Field(strict=True)`. 심화만 `model_json_schema()` | L5 |
| 11 | B | 패키지, `src/패키지 이름/__init__.py`, pyproject.toml `[project]`·`[build-system]`, 배포 이름 price-tools/import 이름 price_tools, 빌드·휠(`py3-none-any`), `uv build --wheel`·`uv venv`·`uv pip install/list`, `zipfile.ZipFile().namelist()`, 테스트 격리, `@pytest.fixture`, `--setup-show`, `파일::함수`. 심화만 monkeypatch | L4·L6 |
| 12 | A·B | `async def`, 코루틴, `await`(셀의 함수 밖 await는 IPython 기능), `asyncio.sleep`, `time.perf_counter()`+`round(…, 1)`, 이벤트 루프, `asyncio.gather(코루틴, 코루틴)`(반환 목록은 넣은 순서), .py의 `async def main()`+`asyncio.run(main())`, 동기 함수·차단 호출·스레드, `asyncio.to_thread(함수, 인자들)`(함수 이름을 괄호 없이 넘김). 심화만 `threading.current_thread().name` | L7 |
| 13 | A·B | 새 문법 없음. 1~7절 부품 조립 + `assert` | — |

### 용어 (용어 표에 넣은 것)

변수·대입·자료형·정수·실수·문자열·불리언·함수 호출·예약어·f-string·형 변환(01) / 조건문·비교 연산자·반복문·위치 번호·경계값·while·break·continue·range·enumerate(02) / 목록·슬라이싱·튜플·풀어 담기·딕셔너리·키·집합·백업·`is`/`==`·copy(03) / 함수·매개변수·인자·반환값·None·지역 변수·기본값(04) / 파일·모드·문자 인코딩·키워드 인자·with 블록·예외·try/except·FileNotFoundError·ValueError·Exception(05) / 클래스·인스턴스·메서드·초기화 메서드·self·속성·클래스 속성(06) / 모듈·import 문·from import 문·표준 라이브러리·`__name__`·타입힌트·정적 타입 검사기(07) / 테스트·기대값·테스트 함수·통과/실패·종료 코드·회귀 테스트·매개변수화(08) / 데코레이터·wrapper·컨텍스트 매니저(본문 「관리자」)·yield·finally(09) / 데이터 검증·모델·상속·필드·검증 오류·엄격 모드(10) / 패키지·빌드·빌드 백엔드·휠·테스트 격리·픽스처(11) / 비동기 함수·코루틴·이벤트 루프·동기 함수·차단 호출·스레드(12).

## 2. 반복해 쓴 예제 데이터·비유·함수 이름

- **주문 한 건(01~04)**: 무선 키보드·수량 2·단가 39000(01은 39000.0 실수, 02부터 원 단위 정수)·할인율 0.1 → 결제 70200. 주문 세 건 `[18000, 42000, 65000]`(02) → 27000 추가·합계 152000(03). 딕셔너리 `order = {"order_id": "A102", "product_name": "무선 키보드", "amount": 78000, "shipping_fee": 0}`(03). 장바구니 `cart ["키보드", "마우스"]`+헤드셋, 상품 이름 목록 `product_names`(03)
- **함수 이름**: `calculate_payment(amount, discount_rate)`(78000·0.1 → 70200, 04), `calculate_line_total(unit_price: int, quantity: int = 1) -> int`(39000·2 → 78000, 생략 → 39000, 3 → 117000; 04 정의, 07 타입힌트, 08·09·11 재사용), `add_tag(tag, tags=None)`(04), `read_items(file_name)`·`parse_order(line)`·`load_orders_before()`/`load_orders(file_name)`(05), `read_unit_price(price_line: str) -> int`·`run_pytest() -> int`(08), `print_call`·`open_order_file`(09), `check_stock`·`lookup_stock`·`ask_warehouse`(12), `make_order_line`·`collect_order_lines`·`add_up_total`·`print_report`·`summarize_orders`(13)
- **클래스**: `OrderLine(name, count)`+`add_count(extra)`(연필 3 → 5, 노트 2 → 4; 06·07·13), `OrderBefore`→`Order`(`self.items = []`, 고객 민지·준호; 06), Pydantic `OrderLine`(`name: str`, `count: int = Field(strict=True, ge=1, le=10)`; 10)
- **파일**: `orders.txt`(연필,3 / 노트,2 → 값 바꿔 보기 연필,5), `bad_orders.txt`(연필,많이 / 노트,2), `missing.txt`(없는 파일), 모듈 `order_tools.py`(07)·`price_tools.py`(08·11), 테스트 `test_price_tools.py`·`test_unit_price.py`(08)·`test_items.py`(11), 가격표 `unit_prices = {"연필": 1000, "노트": 2500}`(13)
- **Before/After 이름 규칙**: 4·5·6절처럼 `…_before()`/`OrderBefore` → 고친 이름, 또는 9·10·12절처럼 같은 이름으로 다시 정의. After 셀 끝 `assert`
- **셀 모양**: 준비 셀 `tempfile.mkdtemp(prefix="ch02-NN-")`+`os.chdir()`(05·07·08·09·11·12·13; 05는 작업 폴더 경로도 출력), 파일·모듈·테스트 글은 `"""…"""`+`with open("w")`+`write()`, 새 Python 실행은 `subprocess.run([sys.executable, ...], capture_output=True, text=True)`, 오류 관찰은 그 오류 이름만 받는 `try/except`, 정의 셀(결과 읽기 「출력이 없습니다」)과 호출 셀 분리
- **비유와 삽화(3~13절 모두 좌우 Before/After 구도)**: 이름표 상자(01) · 택배 상자 분류대(02) · 한 상자에 이름표 두 개(03) · 꼬리표와 고리(04) · 주문서 봉투와 받침(05, 큰 통 = Exception) · 주문서 양식과 바구니(06) · 저금통 몸통의 동전 그림 스티커와 종이 카드(07, 타입힌트) · 동전 저울(08, 기대값) · 창고 문 닫힘 장치(09, finally) · 동전 검사기(10, 엄격 모드) · 마트 입구 바구니 더미(11, 픽스처) · 모래시계 두 개와 식당 주방(12: 번호표 = 코루틴, 냄비 챙기는 직원 = 이벤트 루프, 반죽 치대기 = 차단 호출, 옆 조리대 보조 = 스레드) · 계산대 주문서 두 받침(13)
- **그림 색 규칙**: 코드 줄·블록 flow 파랑, 값·파일·인스턴스 tool 초록, 출력·기록 measure 노랑, 실행하지 않은 분기 회색. **잡아서 출력·기록한 오류는 노랑, 프로그램을 멈춘 실패(받지 못한 오류, 종료 코드 0이 아님, 실패한 테스트)와 Before 결함 결과는 빨강**(검토 1차에서 규격 §5-3에 추가). 예: 05-3·10-1·13-3 노랑, 08-3·11-2·Before 결과 빨강

## 3. 13 실습 절 주제와 결과

- 「파이썬 실습: 주문 파일로 합계 내기」(experiment, 30분, 모델 호출 0번). 5절 파일 두 개를 같은 조립 함수 `summarize_orders(file_name, price_table)`로 읽고, 수량을 읽을 수 없는 줄은 기록장의 「건너뛴 줄」에 남기며 나머지로 합계를 냄
- 실행 1 `orders.txt`: 읽은 줄 수 2·주문 수 2·건너뛴 줄 `[]`·합계 8000
- 실행 2 `bad_orders.txt`(값 하나만 바꿈): 오류 메시지 `invalid literal for int() with base 10: '많이'` 출력, 읽은 줄 수 2·주문 수 1·건너뛴 줄 `['연필,많이']`·합계 5000. 달라진 칸 수 4
- 5절 After(ValueError를 받지 않고 드러냄)와 실습(줄 단위로 받아 기록)은 받는 자리가 다르고, 둘 다 「다른 문제를 같은 빈 결과로 감추지 않는다」는 5절 결론을 지킨다고 본문·노트북·복습에 적음

## 4. 다음 챕터(Ch 03 Git·GitHub 이후)가 이어받을 것

- 「앞에서 배운 내용」에 쓸 수 있는 것(A·B 공통): 01~08·12절 문법 전부. 특히 `with open(..., encoding="utf-8")`, `try/except 오류이름`, 함수 정의(타입힌트 포함), `import`·`from … import`, `subprocess.run([...], capture_output=True, text=True)`와 종료 코드, 테스트 파일과 `run_pytest()`, `assert`
- Ch 3 노트북은 모두 `subprocess.run`을, 01은 `with open(`을 씁니다. Ch 2 08절이 `subprocess.run` 모양과 종료 코드를 이미 가르쳤으므로 「Ch 1 3절·Ch 2 8절에서 쓴 모양」으로 이어 쓸 수 있습니다. Ch 1 요약대로 Ch 3은 `git config`·`.gitignore`·브랜치·GitHub 몫입니다
- 준비 셀 모양: 임시 폴더를 만들고 `os.chdir()`로 옮기는 셀은 Ch 2 07절 뒤라 L4 허용입니다. 파일 경로를 학생에게 보여 줄 때는 05절처럼 출력하고, 실행 도구가 사용자 폴더를 `[사용자 폴더]`로 가린다고 적습니다
- 타입힌트: 기본 경로에서 쓴 모양은 `매개변수: int/str/float = 기본값`과 `-> int/str`뿐입니다(9절은 함수를 받는 매개변수에 적지 않음)
- 오류 받기: 「그 오류 이름만 받는 try/except로 셀을 끝까지 실행하고, 실제 프로그램은 멈추게 둔다」는 문장을 05절에서 정했습니다
- **§12의 `gather`는 코루틴을 괄호에 하나씩 넣는 모양만 가르쳤습니다.** Ch 18 03 노트북의 `gather(*jobs)`·`gather(*(… for …))`는 `*목록` 풀어 넘기기와 제너레이터 식이라, A 경로는 배우지 않았습니다(9절 `*args`도 B만). 그 절에서 한 문장으로 풀거나 목록을 하나씩 넣는 모양으로 씁니다
- 규격에 추가된 규칙(2026-09-16 Ch 2 검토): §2-3 Ch 2 01~06절 준비 셀 표준 라이브러리 import 예외, §2-2 「A 트랙과 L5·L6」, §2-4 클래스 정의 셀(메서드 2개·본문 3줄 이하면 한 셀), §5-3 오류 상자 색

## 5. 아직 가르치지 않은 것 (다음 챕터가 전제하면 안 되는 것)

- **A 트랙(기본 경로)은 09~11절을 건너뜁니다.** A 학생은 `@` 줄(데코레이터 사용·정의), `BaseModel`·`Field()`·`ValidationError`·`model_validate`/`model_dump`, 픽스처·monkeypatch·패키징(uv build·휠)을 배우지 않았을 수 있습니다. 규격 §2-2에 따라 **Part 2 이후 절이 `@` 줄이나 `BaseModel`을 처음 쓰면 세 문장으로 뜻을 풀고 Ch 2 09·10절을 링크합니다.** 확인된 곳: Ch 6 03(BaseModel·Field(ge, le)·ValidationError·strict=True), Ch 19 01(`@tool`)·02(`Field(ge=1, le=10)`·`model_json_schema`)
- 문법(두 트랙 모두): 내포식·lambda·조건 표현식, 형식 지정 f-string(`{x:.3f}`)과 f-string 안 계산, 몫 연산 `//`, `raise`, `try`의 `else`, `global`, 상속 직접 설계·`super()`, `__str__`·`__repr__`, `if __name__ == "__main__":`, `import 모듈 as 별명`, 상대 import, 타입힌트 `list[str]`·`dict[...]`·`None`·`Optional`·`str | None`·`Callable`·`Literal`, 변수 타입힌트, `TypedDict`, 모드 `"a"`, `pathlib.Path`(Ch 1에서만 씀), `KeyError`·`NameError`·`AttributeError` 관찰, `input()`, `*목록` 풀어 넘기기(A)
- 비동기: `asyncio.create_task()`·태스크, `Event`·`Semaphore`·`Queue`, `async for`·`async with`, `wait_for`·시간 제한·취소, `return_exceptions=True`, 노트북 셀의 `asyncio.run()`
- 도구: `pytest.raises`, 매개변수화의 기본 경로 사용, 픽스처 `yield`·범위·`conftest.py`·`tmp_path`, 터미널에서 pytest 실행(안내만), `uv add`·`uv init`·`uv publish`, `pip`, `.env`와 API 키, 모델 호출(Ch 6부터), `os.environ`
- 실행하지 않은 화면: Windows 경로·출력, VS Code에서 모듈 파일 만들기, 정적 타입 검사기, 터미널 pytest

## 6. A·B 트랙 차이

| | A 트랙(기본 경로) | B 트랙(확장 경로) |
|---|---|---|
| 순서 | 01~08 → index 「A트랙 보충 실습」 6과제(12h) → 12 → 13 | 01~13 순서대로 |
| 절 본문 표기 | 「기본 경로(A)」 | 「확장 경로(B)」 |
| 보충 과제 | 1 배송비 경계값(테스트 함수 여섯 개, 매개변수화 모양은 선택), 2 목록 공유 회귀 테스트, 3 `read_items`·`parse_order`·`load_orders`와 ValueError(테스트 안 `try/except`+`assert`), 4 `Order` 두 고객, 5 `calculate_line_total`·`read_unit_price`를 `pricing.py`로(78000·39000·117000, `int()` 빠뜨림 버그, `run_pytest()`), 6 주문 합계와 배송비(8000 → 10200, 50000 → 45000) | 09 데코레이터·with 원리, 10 Pydantic, 11 패키징·픽스처 |
| 13 실습 | 1~7절 부품만 써서 두 트랙이 같이 실행 | 같음 |

## 7. 강사 확인 대상

- 03절 강의·실습 범위: 강의 2~7·13~14번, 실습 8~12번(딕셔너리 키 추가·`in`/`get()`·`items()`·집합·값 바꿔 보기)
- 05절 강의·실습 범위: 강의 2~5·7~10번, 6번(값 바꿔 보기) 비교는 실습(코드 셀 두 개는 강의에서도 실행 — 10번 After가 6번 파일을 읽음)
- 규격에 추가한 네 규칙(§2-3 준비 셀 import 예외, §2-2 A 트랙과 L5·L6, §2-4 클래스 정의 셀, §5-3 오류 상자 색)
- index A트랙 보충 과제 1·3·5 새 문장(기대값·실행 방법)
- 05절 준비 셀이 출력하는 작업 폴더 경로(`[사용자 폴더]/…` 표시)와 설명

## 8. 남은 것

- 다운로드 묶음 `textbook/downloads/ch02-practice.zip` 재생성(개선 전 12개 노트북, 13절 없음). 전체 마감 때 Ch 1 zip과 일괄
- 정리 대상(삭제하지 않고 목록만): `qa/upgrade/_shot08/`(08절 화면 캡처 임시 폴더), `figures/NN-concept.excalidraw`·`NN-concept.svg`(01~12, 옛 도식, 본문에서 뺌), `qa/figures-01-04.json`·`figures-05-08.json`·`figures-09-12.json`(옛 도식 기록), `qa/upgrade/gates-wip-*.json`(절 작업 중간 기록), `textbook/_notebook/checks/--chapter/`(검사 도구 인자 오타로 생긴 폴더로 보임, 챕터 밖)
- 2차 검토(보고서 끝 「반영 결과」의 볼 곳), 강사 확인
- 루트 `.moai/context.md` 진행표에는 Ch 01·02 행이 없어 갱신하지 않았습니다(진행 기록은 `textbook/qa/upgrade-progress.md`)
