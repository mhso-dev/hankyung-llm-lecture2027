# Ch 4 개념 학습 순서 작성자 검토

- 검토 범위: `textbook/part1/ch04-data-tools/_src/` 5절, `labs/part1/ch04-data-tools/notebooks/` 5개
- 변경 전 백업: `.moai/evolution/part1-learning-sequence-2026-09-11/before/` 아래 동일 상대 경로
- 집필 기준: 문제 → 정의 → 입력·처리·반환과 코드 표기 → 최소 예제 → 실제 결과 해석
- 코드 동작: 기존 조회·조인·파싱 함수의 동작은 유지했습니다. 개념과 출력을 연결하기 위한 관찰용 출력만 01·02·04·05절 노트북에 추가했습니다.

## 01 Pandas로 표 다루기

- 기존 누락: DataFrame에서 곧바로 `loc` 활용으로 넘어가 Series, 인덱스, 열 선택 표기, `to_dict(orient="records")`의 반환 구조가 설명되지 않았습니다.
- 수정 위치: 본문 3~5번, 노트북 `cell-04`, `cell-06`, `cell-08`, 코드 `cell-07`.
- 선수 개념 확인: Ch 2 `03-자료구조`, `04-함수`, `05-파일과-예외`의 사전·목록, 매개변수·반환, `Path`와 파일 읽기를 실제 파일에서 확인하고 절 번호로 적었습니다.
- 예제 연결: 사전 목록 → 3행 3열 DataFrame → 상태 Series → `[True, False, True]` 마스크 → `loc` 선택 → 사전 목록 반환 순서로 설명했습니다. 상태만 `pending`으로 바꾼 비교와 문자열 금액 실패를 기본 이해 뒤에 유지했습니다.
- 실제 관찰: paid 마스크 `[True, False, True]`, paid 주문 `O101`, `O103`, pending 주문 `O102`, 문자열 합계 `320001800027000`, 숫자 합계 `77000`.
- 실행 해시: code `d866f45eff2b0e4b42bc98ca213f16610cf2054720c7577a6a9544def4899d90`, output `071d36c9717dfdb036a97dc810a4fb4391075289dadc16b3b02df8f99722b907`.

## 02 관계형 테이블과 키

- 기존 누락: 기본 키와 외래 키 정의 뒤 곧바로 `merge`를 실행해 관계의 읽는 방향, 내부 조인과 왼쪽 조인, 일치하지 않은 오른쪽 열의 결측값과 SQL의 NULL 관계가 충분히 설명되지 않았습니다.
- 수정 위치: 본문 4~5번, 노트북 `cell-04`, `cell-06`, `cell-08`, 코드 `cell-09`.
- 선수 개념 확인: 바로 앞 절의 DataFrame, 행 선택, 사전 목록을 사용하며 새로운 선행 지식을 가정하지 않았습니다.
- 예제 연결: 고객 기본 키와 주문 외래 키 → 주문 기준 `many_to_one` → 내부 조인 3행 → C999를 추가한 왼쪽 조인 → 고객 이름 `NaN`과 `_merge=left_only` → 중복 고객 키로 5행 증가 순서로 설명했습니다.
- 실제 관찰: 정상 조인 3행, O104의 고객 이름 `NaN`, `_merge=left_only`, 중복 조인 5행, `MergeError`, 수정 후 3행.
- 실행 해시: code `b3b14496c53e46c004b592db6cd0f9cc80412f3925cb2d2502a13107d4eb64ae`, output `775917f9f3a2132c9c3cd9a441464dd8d7ef641edabb00d609cc325575edc05a`.

## 03 SQL로 조회 함수 만들기

- 기존 누락: SELECT·JOIN·WHERE·ORDER BY의 역할은 있었지만 SQL 작성 순서와 데이터베이스의 개념적 처리 순서, `LIMIT`, 한 원소 튜플의 쉼표, `AS`, 커서와 행 팩토리가 코드 전에 연결되지 않았습니다.
- 수정 위치: 본문 3~5번, 노트북 `cell-04`, `cell-06`, `cell-08`.
- 선수 개념 확인: 앞 절의 기본 키·외래 키·조인과 Ch 2 `04-함수`, `05-파일과-예외`의 함수 경계와 예외를 실제 파일에서 확인했습니다. pytest는 Ch 2의 08절에서 다루지만 이 조회 예제의 시작 조건은 아니므로 선수 설명에서 제외했습니다.
- 예제 연결: 자연어 조회 요구 → SQL 작성 절 → 개념적 처리 순서 → `execute(sql, (customer_id,))` 입력 → `sqlite3.Row` 처리 → 사전 목록 반환 → 고객 번호만 바꾼 비교 순서로 설명했습니다.
- 실제 관찰: C001은 O101·O103, C002는 O102, 문자열 결합 조회는 3행, 매개변수 조회는 0행, 부모 없는 주문은 `IntegrityError`.
- 실행 해시: code `b07b8e602bdb95770e8a8e5911339727a488428cde5f84324dafadad124aaa6c`, output `70e8de21eabbb3856f7e8b6559e08bdf3dcbfa0829b0d6a76f4425de5af7aa02`.

## 04 REST와 페이지네이션

- 기존 누락: REST와 페이지네이션을 설명하면서 HTTP 요청과 응답의 구성, JSON에서 Python 값으로의 변환, 쿼리 매개변수의 위치가 압축되어 있었습니다. async/await는 Ch 2의 공통 12절에서 다루지만 이 절의 동기 HTTP 예제를 이해하는 데 필요한 선수 조건은 아니었습니다.
- 수정 위치: 본문 3~5번, 노트북 `cell-04`, `cell-06`, `cell-08`, 코드 `cell-07`.
- 선수 개념 확인: 앞 절의 함수 입력·조회·사전 목록 반환과 Ch 2 `05-파일과-예외`의 예외 처리만 선수 개념으로 남겼습니다. 비동기는 Ch 30의 후속 학습으로 분리했습니다.
- 예제 연결: GET 요청의 주소·매개변수 → 응답 상태·헤더·JSON 본문 → Python 사전의 `items`·`next_page` → 다음 요청 입력 갱신 → `None` 종료 → 누적 목록 반환 순서로 설명했습니다. 로컬 fixture HTTP만 사용했습니다.
- 실제 관찰: 첫 응답 상태 200, 요청 주소의 `?page=1`, 첫 페이지 A01·A02와 `next_page=2`, 둘째 페이지 A03과 `next_page=None`, 전체 ID A01·A02·A03.
- 실행 해시: code `0870a96e7f7e229f208fb4a2f3be98a1569badbefb521d24b6134ad312fceb1f`, output `302df331eefa070dfc2cc1702e2c89372b4bc004e70ad093f570813acdf59d63`.

## 05 문서 파싱과 스크래핑

- 기존 누락: 파싱과 CSS 선택자의 정의는 있었지만 HTML 태그·속성·부모·자식·요소 트리, 선택자에서 점의 의미, `select_one`과 `get_text`의 입력·반환이 코드 전에 충분히 설명되지 않았습니다.
- 수정 위치: 본문 3~5번, 노트북 `cell-04`, `cell-06`, `cell-08`, 코드 `cell-05`.
- 선수 개념 확인: 앞 절의 HTTP JSON 사전, Ch 2 `04-함수`의 `None` 사용, `05-파일과-예외`의 예외 구분을 실제 파일에서 확인했습니다.
- 예제 연결: HTML 문자열 → lxml 요소 트리 → `article` 노드 → `.summary` 자식 노드와 속성 → 문자열 추출 → 정해진 키의 사전 반환 순서로 설명했습니다. robots.txt 비교는 기본 파싱 흐름 뒤에 별도 조건으로 배치했습니다.
- 실제 관찰: 파서 `lxml`, 선택 요소 `article`, ID A10, 제목 `골목상권 매출 회복`, 발행일 `2026-09-01`, 허용 경로 `True`, 비공개 경로 `False`, 없는 선택자 `None`, 수정 후 `subtitle=None`.
- 실행 해시: code `8c7270369a5e3f9c3483db100d3d93e18ae75c0648f816f4ceb9e0fa6dda9a9c`, output `bb7fdeb7241121142eac15908e75f74f170dc7eaf3274f2647de6bfc0df3306d`.

## 검증 결과

- 빈 커널 순차 실행: 5개 노트북 모두 Python 3.12.13, `fresh_kernel=true`, `status=passed`, 오류 출력 0건입니다. 01~04절은 코드 셀 6개, 선택자 비교를 추가한 05절은 7개입니다.
- Ch 4 단위 테스트: `uv run python -m pytest -q tests`를 `labs/part1/ch04-data-tools`에서 실행해 10개 모두 통과했습니다.
- 구조 검사: 5개 `_src` 파일 모두 고정 섹션 10개를 유지했습니다. 5개 노트북은 `jq` JSON 검사를 통과했습니다.
- 어휘 검사: `당연히`, `간단히`, `쉽게`, `함정`, 내부 용어 `회수`, 실행 의미의 `돌리다`, 구어 축약형을 범위 내에서 검색해 발견하지 못했습니다.
- 빌드·완성 HTML·시각 4축 검사는 공통 파일 충돌을 피하기 위해 루트 통합 검토에서 수행합니다.

## 확인 필요 항목

- 없음. 외부 API와 유료 호출을 사용하지 않았으며 REST 실습은 로컬 fixture HTTP 서버에서 검증했습니다.

## 독립 검토 후 보정

- 01절: `pd` 별칭, 점 표기, `pd.DataFrame` 생성자와 `pd.read_csv`의 입력·반환을 코드 전에 추가했습니다.
- 02절: `merge`, `concat`, `indicator`, `drop_duplicates`, `is_unique`, `iloc`을 첫 호출 전에 설명했습니다. 중복 조인으로 합계가 77,000에서 136,000으로 증가하고 수정 후 77,000으로 돌아오는 실제 출력을 추가했습니다.
- 03절: `sqlite3`, `TemporaryDirectory`, `connect`, `row_factory`, `execute`, `executescript`, `commit`, `close`를 준비 순서에 맞춰 설명했습니다. 연결 객체의 `with` 블록은 정상 종료 시 커밋하고 예외 시 롤백하지만 연결을 닫지 않으므로 조회 함수와 실패·수정 셀 세 곳 모두 `finally`에서 연결을 닫습니다. 트랜잭션이 필요한 외래 키 입력 셀에는 `with db:`를 내부에 유지했습니다. `orders o`, `customers c`의 테이블 별칭과 `USING(customer_id)`의 같은 이름 열 연결도 SQL 실행 전에 본문과 노트북에서 설명했습니다. 준비 셀의 불필요한 Cursor 표현 출력도 제거했습니다.
- 04절: 로컬 HTTP 서버의 상속 표기와 요청 처리 메서드를 보조 준비로 명시했습니다. 노트북의 기본 `fetch_articles` 입력을 `base_url`과 `timeout`으로 줄이고, 요청 → 상태 검사 → 현재 목록 누적 → 다음 페이지 갱신 → 반환 순서로 정리했습니다. `Client`, `client.get`, `extend`, 사전 `get`, `close`의 입력·처리·반환 역할을 코드 전에 설명했습니다. 범주 필터, 외부 클라이언트 입력, 반복 페이지 검사는 공용 `data_tools.py`의 확장 기능으로 구분했습니다.
- 05절: `Path.cwd().parents`, 제너레이터 표현식, `next`, `read_text`, `json.dumps`, `write_text`, `json.loads`를 설명했습니다. 같은 HTML에서 `.summary`와 `time` 선택자를 바꾸어 요약, 화면 날짜, 날짜 속성을 비교하는 코드 셀을 추가하고 robots.txt를 별도 주의 실습으로 분리했습니다.
