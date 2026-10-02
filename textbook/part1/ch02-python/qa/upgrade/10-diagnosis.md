# 10-Pydantic — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/10-concept.*`).
생성기: `qa/upgrade/author_10.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch02-python 10`.
먼저 읽은 것: Ch 1 `qa/upgrade/chapter-summary.md`, 이 챕터 01~09절 개선본(`_src`, `author_06.py`·`author_08.py`·`author_09.py`, `09-diagnosis.md`, `09-figures.md`), `qa/upgrade/handoff.md`(특히 `## §09 → §10`), `upgrade_gates.py`(스키마 클래스 판정 `SCHEMA_BASES`).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 7 | 0 |
| G6 | 24 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 14 (준비 1 + example 8 + before 1 + after 4(심화 1)) |
| 검사한 문장 | 100 | 359 |
| 모델 호출 | 0 | 0 (언어 모델 없음, API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, Pydantic 2.13.5, 2026-09-16, 오류 출력 0), verify PASS(12절 154셀). 수정 후 수치는 `gates-wip-10.json`, 수정 전은 `gates-before.json`(덮어쓰지 않음). 빌드 HTML 가로 넘침 없음(puppeteer 1280px·390px에서 scrollWidth 1280·390, SVG 4·삽화 1, 남은 `{{` 토큰 없음).

## 수정 전 주요 문제

- **G1이 잡지 않은 사다리 문제**: 한 셀에 import·클래스 정의·검증·출력을 함께 둠(범위 셀은 클래스 정의·통과 확인·try/except/else를 한 셀에), `else: raise AssertionError(...)`(`raise`·`try`의 `else`는 아직 안 배움), `error.errors()[0]`와 `type(job.retries).__name__`, 준비 셀의 `%pip install`(8절은 import 버전 확인으로 바꿨음)
- **이어짐 결함**: 데이터 `retries`(재시도 횟수)·`LooseJob`·`BoundedJob`·`StrictJob`이 1~9절 주문 데이터와 무관. 「07절의 타입힌트는 `retries: int`처럼」은 개선된 7절 예(`unit_price: int`, '39000' → 3900039000)와 다름. 6절에서 상속을 가르치지 않았는데 「BaseModel의 검증 기능을 물려받아」를 설명 없이 씀. 「06절에서 클래스로 객체를」의 「객체」는 6절 용어(인스턴스)와 다름. Ch 18 연결 문장은 Ch 18 본문에서 확인되지 않음(Ch 18 _src에 BaseModel 없음)
- **Before/After 구조**: Before는 `LooseJob`에 "3"을 넣어 통과를 보여 주기만 해서, 무엇이 문제인지 출력으로 드러나지 않음(「입력 제공자가 JSON 숫자를 보내야 한다는 규칙이라면」이라는 가정만 있음)
- G5: 제목 셀·「오늘 볼 그림」 없음, 결과 읽기 셀 없음. G6: 코드 이름으로 시작하는 문장 18개(「`Field(strict=True)`는」「`model_dump()`는」 등), 70자 초과 3개, 5문장 넘는 단락 2개. G7: Excalidraw 도식 1장뿐, Mermaid 0장, 삽화 0장, 설계표 없음

## §09가 넘긴 판단 거리

- **L5 첫 절**: 스키마 클래스 `class OrderLine(BaseModel):`에 필드만 적음(메서드 없음). G1은 `BaseModel`을 물려받고 필드만 적은 클래스를 잡지 않으므로 `upgrade_allow`가 필요한 셀이 없음. 함수 정의가 없어 타입힌트는 필드 줄에만 나옴. L6 `@` 줄 사용·L7 async 없음
- **상속**: 6절에서 가르치지 않았으므로 노트북 2번과 본문 「BaseModel을 물려받고 필드만 적기」에서 뜻 → 일상 예(인쇄된 빈 양식 용지에 칸 이름만 적기) → 코드 순으로 세 문장. 「상속으로 클래스를 직접 설계하는 방법은 이 절에서 다루지 않습니다」를 적음(`super()`는 쓰지 않음)
- **7절 「타입힌트는 값을 검사하지 않음」·8절 '39000' 결함 연결**: 이유 블록 첫 단락과 노트북 2번에서 7절 3900039000을 인용하고, Before를 「`int()` 줄을 빠뜨린 수량 글자」(7·8절과 같은 빠뜨림)로 만듦
- **기존 데이터 `retries="3"`·`ge=0/le=5`·`strict=True`**: 학습 질문(자동 변환을 제한하면서 같은 범위 제약을 유지할 수 있나요?)과 실패 구조(기본 모드가 "3"을 통과 → 같은 범위 규칙에 `strict=True`만 더해 `int_type`)는 유지. 데이터는 6·7절 `OrderLine(name, count)`, 5절 줄 "연필,3"과 bad_orders.txt의 '많이', 범위 1~10(Ch 19 02절 `Field(ge=1, le=10)`과 같은 범위)으로 바꿈
- **`ValidationError`**: 5절처럼 그 오류 이름만 받는 try/except. `raise AssertionError`는 쓰지 않고, 알렸는지를 표시 `was_reported`(False/True)로 출력하고 After에서 `assert was_reported`

## 바꾼 것

- 노트북(paired 유지): 제목 → 오늘 볼 그림(10-1) → 준비(`pydantic 버전: 2.13.5`) → 모델 정의(필드 name·count) → 키워드 인자로 인스턴스(`name='연필' count=3`) → 글자 '많이'(`1 validation error for OrderLine`, `type=int_parsing`, `input_value='많이'`) → 글자 "3"(`3`, `<class 'int'>`, 자동 변환·lax mode) → 딕셔너리 오가기(`model_validate()`·`model_dump()`, `True`) → `Field(ge=1, le=10)` 다시 정의 → 수량 10(`count=10`, `errors()`의 loc·type·input을 미리 적음) → 값 바꿔 보기: 수량 11(`('count',)`, `less_than_equal`, `11`) → Before: 줄 "연필,3", `int()` 빠뜨림(`count=3`, `<class 'str'>`, `False`) → After: `strict=True`만 더해 다시 정의 → 같은 셀(`int_type`, `<class 'str'>`, `True`, `assert was_reported`) → `int()` 더하기(`count=3`, `<class 'int'>`, assert) → 원리 더 알아보기(심화): `model_json_schema()`(`['name', 'count']`, minimum 1·maximum 10, 엄격 모드 항목 없음) → 정리
- **학습 목표 조정**: 「Pydantic v2 모델로 자료형과 범위 선언」→ BaseModel·필드·키워드 인자·딕셔너리, 「`ValidationError.errors()`의 유형과 위치」→ 메시지 읽기와 `errors()`의 loc·type, 「자동 변환과 `Field(strict=True)` 차이」→ 같은 글자 '3'의 출력으로. `int_parsing`(읽을 수 없음)과 `int_type`(자료형이 아님)의 차이를 본문 소제목으로 둠
- 본문 10블록 전체를 다시 씀. 「앞에서 배운 내용」 표 7행(1·3·5·6·7·8·9절), 용어 8개 표(데이터 검증·모델·상속·필드·검증 오류·자동 변환·범위 규칙·엄격 모드), 소제목 「데이터 검증과 모델」「BaseModel을 물려받고 필드만 적기」「검증 오류 읽기」「자동 변환과 엄격 모드」「딕셔너리로 받고 딕셔너리로 꺼내기」「범위 규칙과 값 바꿔 보기」「오류 종류 int_parsing과 int_type」「확인한 범위」, 복습 6문항(4 → 6), 참고 자료 7개(Pydantic 문서가 pydantic.dev/docs/validation으로 옮겨 가 주소를 새로 적음). 다음 학습: B는 11절, A는 12절, Ch 6 03절 구조화 출력·Ch 19 02절 도구 입력 규칙(두 절 노트북에서 BaseModel·Field 사용 확인). 기존 Ch 18·Ch 30 연결 문장은 뺌
- 그림: Mermaid 4장(세 입력 검사, 딕셔너리 오가기, 범위 규칙, Before/After) + 삽화 1장(동전 검사기, 1회 생성 통과, 3~9절 좌우 Before/After 구도, 7·8절 동전 그림 종이 카드를 이어 씀). 10-2는 처음 LR로 원본 폭 1111px라 TB로 바꿈(274px). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)
- 동작 근거: 설치한 Pydantic 2.13.5 소스 `BaseModel.__init__(self, /, **data)`(키워드 인자만 받음, 위치 인자는 노트북에서 실행하지 않았다고 적음), Pydantic 문서 Strict Mode(lax 기본값, 문자열 '123' → 123, 필드·모델·호출 단위), Models(「BaseModel을 물려받고 필드를 적은 클래스」, 「필드 값은 키워드 인자로」), Migration Guide(`parse_obj()` → `model_validate()`)

## 검토에서 볼 곳

- Before의 「실패」가 오류가 아니라 「알리지 않음(False)」이라는 점. 본문은 이름 count_text가 여전히 `<class 'str'>`임을 근거로 들고, 「엄격 모드가 언제나 더 좋은 것은 아닙니다」 단락과 복습 6번으로 균형을 둠
- 이 절의 「모델」과 언어 모델의 혼동: 제목 셀 준비물은 「언어 모델 호출은 0번」, 노트북 2번·용어 표·「데이터 검증과 모델」에 「언어 모델과 다른 뜻」을 적음
- 새 내용 양: BaseModel·상속(뜻만)·필드·ValidationError·자동 변환·model_validate/model_dump·Field(ge, le)·errors()·strict. 코드 셀 14개. 검증 오류 출력은 모델이 규칙대로 알린 결과라 그림에서 노랑, 빨강은 Before 결과만
- 삽화: 오른쪽 반환구가 컵보다 가로 틈 모양(종이 카드가 앞으로 밀려 나온 것은 분명해 채택)

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-B.md`

- 판정 accept-with-fixes(하 1). 반영했습니다.
- 10-1: 넣은 값 상자를 파랑 → 초록(10-1 `i1~i3`, 10-3 `in10`·`in11`)으로 바꿔 렌더(PNG 확인). 도식 읽기·노트북 오늘 볼 그림·캡션 읽는 법·설계표 색 규칙
- 검증 오류 노랑은 챕터 색 규칙(규격 §5-3)과 같음
- 새 커널 출력은 반영 전과 같음. 코드 셀 14, 검사한 문장 360

재실행: `run_section.sh` → 챕터 `upgrade_gates.py --label after --strict` 13/13 PASS(G1~G7 0), `verify.py --chapter` `PASS 13 sections / 190 code cells`, `visual.cjs` 28건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/10-Pydantic.md`
- 챕터 전체 `gates-after.json`과 루트 `textbook/qa/upgrade-progress.md` 갱신은 챕터를 마친 뒤
- 챕터 index의 A트랙 보충 과제 5는 개선 전 07·08절 데이터를 가리킴(이 절 범위 밖, handoff에 남김)
- A트랙은 09~11절을 건너뛰지만 Ch 6 03절이 BaseModel·Field·ValidationError를 씀(챕터 요약에서 Ch 6 작업자에게 넘길 것, handoff에 남김)
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
