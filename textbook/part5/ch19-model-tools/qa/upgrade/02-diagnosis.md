# 02절 진단과 개선 기록 — Pydantic 인자와 반환 스키마 (paired)

- 작업 2026-09-24 · 규격 `textbook/QUALITY-UPGRADE.md`(§2·§2-7·§3·§4·§5-3·§5-4·§6·§7-2) · 생성기 `qa/upgrade/author_02.py`(노트북 + `_src` 함께, 본은 `author_01.py`).
- 1차 지시: `handoff.md` 「챕터 공통」 + 「§01 → §02」 12항. 참고: `chapter-lead-notes.md` §2 02·§6·§8 7, `01-diagnosis.md`·`01-figures.md`, 과정 요약 §2-1(세 문장 + 링크 — Ch19 02)·Ch 6 03 「양식 클래스」·Ch 2 10 b2·b8 약속.
- **모델 요청 0번**(API 키 셀·모델 셀 없음), 임베딩 0. 읽는 파일 `data/orders.csv` 하나, 쓰는 파일 0. 까닭(준비물에 적음): 입력 형식 검사·내놓은 값 검사 모두 도구를 부르는 프로그램 안에서 일어나 모델 없이 보입니다. 흔들림 확인(노트북 밖 다섯 번)은 해당 없음(`02-probe.md` 만들지 않음).

## 1. 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 6 | 88 | 1 | 0 | 0 | 0 | 7 | 16 | 3 | **27** |
| 수정 뒤(`gates-wip-02.json`, `--no-exec`) | **21** | **346** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 `upgrade_gates.py … --label wip-02 --section 02` → 첫 판 G1 0 · G2 0 · **G6 4**(70자 넘는 문장 둘 — 기준 버전 한 줄·괄호 뒤 마침표로 두 문장이 한 문장으로 셈 / 영문 시작 둘 — b1 `@tool(args_schema=…)`로 시작 · 「CSV의 상태는」) · G7 18(그림 전). 고친 뒤 G1·G2·G6 0으로 실행(`gates-wip-02-02.json`에는 고친 뒤 판이 남음).
- `verify.py --chapter` → `PASS 6 sections / 73 code cells (max 16 lines)`(16줄은 아직 고치지 않은 03~06절). 빌드 HTML 일곱 개 `{{` 잔존 **0건**.
- 코드 줄(주석·빈 줄 뺌, `count_code.py`) 55 → **109**(코드 셀 6 → 21). 준비 셀이 아닌 셀 최대 **8줄**(5절 검사 셀·만든 줄 셀), 준비 셀 최대 9줄(자리 찾기), 함수 본문 최대 **2줄**(`search_orders` — 출력 한 줄 + `return`). 셀당 정의 하나. 도구 파일 변경 0.
- **게이트가 세지 않는 과정 금지 문법은 AST로 따로 셈**(`/tmp/ch19-02/extra_check.py` — 01절 `extra_check.py`에서 `@tool(args_schema=OrderQuery)` 데코레이터만 허용 목록에 더함): **9건(노트북 8 + 도구 파일 1) = 모두 허용 범위** — `class` 2(`OrderQuery`·`OrderRecord`, 둘 다 `BaseModel`, 몸통은 칸 대입 `AnnAssign`만 — 메서드 0) · 변수 주석 6(클래스 칸 `status: Literal[…]`·`limit: int`·`order_id: str`·`customer_id: str`·`status: Literal[…]`·`amount: int` — 챕터 공통 「02의 `BaseModel` 허용(칸만)」) · 도구 파일 1(`fetch_orders`의 `status=None` — 01절과 같은 Ch 4 약속 시그니처). 그 밖 **0건**: `@tool` 밖 데코레이터·`@tool` 매개변수 밖 타입힌트(클래스 칸 제외)·복합 타입힌트(클래스 칸 밖)·반환 힌트·기본값 매개변수(정의)·`@tool` 밖 독스트링·f-string·`key=`/`reverse=`·집합·`set`/`next`/`sum`/`max`/`min`/`zip`/`enumerate`/`sorted`/`any`/`all`/`isinstance`·`.get`/`.setdefault`·튜플 풀기·한 줄 다중 대입·`+=`·별표·세미콜론·내포식·제너레이터 식·`lambda`·조건 표현식. `search_orders`의 매개변수는 힌트 없음, 01절 도구 셀만 `status: str`(01절 판 그대로).

## 2. 수정 전 주요 문제

1. **paired Before가 결함이 아니었습니다.** 옛 Before는 `shipped`·`limit 0`을 넣어 `ValidationError`(`literal_error`·`greater_than_equal`)를 받는 장면 — 스키마가 일하는 모습이고, After는 입력만 `pending`으로 고친 것이었습니다(준비 조사 §2 02·§8 7).
2. 반환 쪽 `OrderRecord.amount: float`이 금액 `32000`을 `32000.0`으로 바꾸고 까닭을 적지 않았습니다. `TypeAdapter(list[OrderRecord])`(새 API + `list[…]` 표기)·`sorted(value[0])`·리스트 내포식 `[row.model_dump() for row in validated]`.
3. 「반환 스키마」가 모델에게 전해지는 것처럼 읽혔습니다(b4 「입력과 반환 형식을 검사」 · b7 「다음 모델 호출에 전달할 필드가 유지되는지」). `@tool` 도구 명세에는 내놓는 값의 모양이 없습니다(준비 조사 §6, 이번 노트북 5절 출력).
4. 한 셀에 클래스 + `@tool` 함수 + 출력 둘(c7), 클래스 + 호출(c9), 목록 `for` 안 `try`(c11), 기본값 매개변수 `limit: int = 3`·반환 힌트 `-> list[dict]`, 준비 셀 `find_up`(`Path | None`·별표 풀기)·`fetch_orders` 다시 적기(`str | Path`·`Any`).
5. `%pip` 셀·결과 읽기 셀·제목 셀·핵심 그림 없음(G5 7). 금지어: 반환·검증·**거부**·필드·돌려주는·사전·최대 등(준비 조사 §1 표). 비유 「주문서」는 Ch 2와 겹침. `Literal`·`Field`·`args_schema`의 뜻 풀이 없음. b5 「모델 호출이 있는 절은 `gpt-5.4-mini`…」 틀 문장.

## 3. 설계 — paired (결정과 까닭)

- **예시(2~5절)**: 01절 도구 다시 적기(01절 3절 셀과 **문자열 대조 같음** — `author_01.DEF_TOOL == author_02.DEF_OLD_TOOL` `True`, 자리 찾기 셀도 `PATH` 같음) → 입력 형식 `{'status': {'title': 'Status', 'type': 'string'}}`·상태 셋은 설명 글에만 → 양식 클래스 `OrderQuery`(`status: Literal["paid", "pending", "cancelled"] = Field(description=…)` · `limit: int = Field(ge=1, le=10, description=…)`, 둘 다 기본값 없음) → 양식 객체 직접 만들기 → `model_json_schema()`(`enum`·`maximum`·`minimum`·`required`) → `@tool(args_schema=OrderQuery)` `search_orders(status, limit)` → 입력 형식이 양식의 칸과 같은가 `True` → 도구 명세(`convert_to_openai_tool`)에 `enum`·`minimum`·`maximum`이 그대로(칸 `title`만 빠짐) → `paid`·`2` → 두 줄 → **5절 내놓은 값 검사**.
- **몸통 첫 줄 `print("몸통 실행 | 상태:", …)`**: 「도구를 부르기 전에(몸통 실행 전에) 막는다」를 단정하지 않고 **출력으로 보이려고** 넣었습니다. After·값 바꿔 보기에서 이 줄이 없고, 규칙 안의 호출(4절·7절 둘째 셀)에서는 있습니다. 함수 본문은 2줄.
- **Before(6절)**: 01절 도구 `.invoke({"status": "shipped"})` → **`받은 주문 수: 0`·`받은 값: []`, 오류 없음**(새 커널 세 번 모두). 둘째 셀이 CSV 상태 넷(`paid`·`pending`·`paid`·`cancelled`)을 출력해 빈 목록이 입력 탓이라는 것을 보임. Ch 4 03절 Before(오류 없이 끝나는 결함)와 이음. 그림 `02-3` 왼쪽 아래 빨강.
- **After(7절)**: `search_orders.invoke({"status": "shipped", "limit": 1})` → `ValidationError` `1 validation error for OrderQuery`·`status`·`Input should be 'paid', 'pending' or 'cancelled' [type=literal_error, input_value='shipped', …]`, **몸통 실행 줄 없음**. Ch 2 05 모양 `try/except ValidationError as error`로 그 셀에서만 받고 「오류를 받지 않는 실제 프로그램이라면 여기서 멈춥니다」. 받은 오류라 그림에서 노랑. 둘째 셀: 규칙 안의 `pending` → 두 도구 모두 `O102` 한 줄, 같음 `True` + `assert`(CSV에서 정해지는 값).
- **Before·After 입력 차이 한 가지**: 새 도구는 `limit`도 꼭 채울 인자라 After에만 `"limit": 1`이 붙습니다(본문에 밝힘). `limit`에 기본값을 주면 LangChain이 입력에 없는 칸을 몸통에 넘기지 않아(설치판 `_parse_input` — 입력에 있던 키만 넘김) 함수에도 기본값 매개변수가 필요해지므로(G1 금지) 기본값을 두지 않았습니다.
- **값 바꿔 보기(8절)**: `limit`만 2 → 0 → `greater_than_equal`·`input_value=0`, 몸통 실행 줄 없음. 예상 → 실행 → 결과.
- **「반환 스키마」 풀이(5절)**: 제목 말은 두고 1절·b2에서 「도구가 내놓는 값의 칸을 코드로 검사하는 틀」로 한 번 풂. 양식 클래스 `OrderRecord`(칸 넷, `status` `Literal`, `amount: int = Field(ge=0)`)를 도구에 붙이지 않고 `for` + `OrderRecord.model_validate(row)`로 코드가 부름 → `검사를 통과한 줄 수: 2`·`첫 줄 금액의 자료형: int`. **셀에서 직접 만든 줄**(`O105`·`C004`·금액 −9000 — CSV에 없음을 본문·b7에 밝힘)이 `greater_than_equal`로 걸리는 것을 보임. 다음 셀 `명세의 칸: ['name', 'description', 'parameters']`·`명세에 amount 글자가 있는가: False`로 **이 검사가 도구 명세(모델이 읽는 모양)에 없다**는 것을 출력으로 보임.
- **`32000.0` 처리**: **설계를 바꿔 없앰** — 금액 칸을 CSV 값과 같은 `int`로 적어 `amount=32000`이 그대로 남는 것을 출력(`첫 줄 금액의 자료형: int`)으로 확인. 학생 본문에는 옛 `float` 판 이야기를 쓰지 않음(제작 이력 금지).
- **`TypeAdapter`**: 뺐습니다(`list[…]` 표기와 새 API가 따라오므로). `model_validate`는 처음 쓰는 자리에서 한 문장(「딕셔너리 하나를 받아 칸 규칙으로 검사하고, 통과하면 양식 객체를 내놓는다」). `**` 풀기·`error.errors()`도 쓰지 않음.
- **반환 힌트**: 노트북 밖 확인(`/tmp/ch19-02/probe2.py`, 설치판 langchain-core 1.6.2) — `@tool` 함수에 `-> list`·`-> OrderRecord`를 붙여도 `convert_to_openai_tool` 결과에 없고, `-> OrderRecord`를 붙인 도구도 목록을 그대로 내놓음(검사하지 않음). 본문 b7에 「노트북 밖에서 했고, 노트북에서는 실행하지 않았습니다 · 이 챕터는 그 표시를 쓰지 않습니다」로만 적음.
- **처음 쓴 문법·API(각각 한 문장)**: `from typing import Literal` · `Literal[…]`(클래스 칸) · 인자 있는 `@tool(args_schema=…)` · 슬라이싱 `[:limit]`(L1, 뜻만) · `OrderQuery.model_json_schema()["required"]` · `.model_validate` · 값 비교 `search_args == query_schema["properties"]`. Ch 6 03에서 배운 것(「Ch 6 03절처럼」): `BaseModel`·`Field(ge=, le=, description=)`·`ValidationError`·`model_json_schema()`·키워드 인자로 양식 객체 만들기·점으로 칸 값 꺼내기. Ch 2 10은 「자세히 다룹니다 + Ch 2에서 건너뛸 수 있는 절」 링크(b3·노트북 3절).

## 4. 실행값 (새 커널 세 번)

| 실행 | 방법 | 시각(UTC) | `code_sha256` | `outputs_sha256` | 셀별 대조 |
|---|---|---|---|---|---|
| A | `run_section.sh … 02`(그림 전 — 첨부 단계 `FileNotFoundError`, 실행은 저장) | 01:17:47~49 | `a00c3c75f4a3…` | `fa546a3c2aba…` | — |
| B | 사본 `/tmp/ch19-02/B.ipynb`, 같은 가상환경 새 커널(인계의 둘째 새 커널 명령) | 01:18:13~15 | `a00c3c75f4a3…` | `fa546a3c2aba…` | A와 **21/21 같음** |
| C(교재 출력) | 그림 alt·삽화 상수를 넣고 `run_section.sh … 02`(생성기가 출력을 지우므로 다시 실행) | 01:24:21~23 | `a00c3c75f4a3…` | `0ba214225b49…` | 글자는 A·B와 **21/21 같음**. 해시가 다른 까닭은 설치 셀 한 곳: pip의 「Note: you may need to restart …」 줄이 A·B에서는 판 번호 줄과 한 스트림 조각, C에서는 따로 조각(출력 글자 같음) |

- 그림은 A·B 대조 뒤 처음 렌더했습니다. 모델이 없어 흔들린 값이 없습니다.
- 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답) A 1.7초 · B 1.5초 · C 1.7초 → 준비물 「3초 안에」. 커널 시작 시간은 들어 있지 않습니다. 본문은 「걸린 시간은 재지 않았습니다」(b7).
- 묶음 모양 키 없는 실행은 하지 않았습니다(02는 `check_bundle_execution.py` 대상이 아님 — 01만). 가져오는 이름·자리 찾기 셀은 01과 같습니다.

## 5. 그림

- Mermaid 4장: `02-1-양식-클래스에서-도구-명세로`(b4·노트북 「오늘 볼 그림」) · `02-2-입력-검사와-내놓은-값-검사`(b5) · `02-3-없는-상태-shipped를-넣으면`(b6) · `02-4-최대-개수를-0으로`(b6 값 바꿔 보기). 원본 viewBox 폭 **800 · 507 · 610 · 638**(모두 868 이하). **보라 0장**(모델 없음), **빨강은 `02-3` Before 결함 하나**, 받은 `ValidationError`(After·값 바꿔 보기·5절)는 노랑, 도구가 하는 입력 검사·`@tool` 도구는 회색(라이브러리), 양식 클래스의 칸·몸통·`model_validate` 부르는 줄은 파랑, 인자 딕셔너리 초록. 첫 렌더에서 칸 안 `direction LR`이 무시돼 위아래로 쌓인 것(`02-1`)과 저절로 꺾인 라벨 셋을 고쳐 다시 렌더. 설계표 `02-figures.md`.
- 삽화 `02-5-칸이-정해진-전표와-닫힌-창`: **1차 job `bda00c54-c0d7-401e-9d50-6018b75006cd` 탈락**(오른쪽 전표의 주황 별이 셋째 동그라미 테두리에 겹쳐 「셋째를 골랐다」로도 읽힘) → **2차 job `d8b4bd0e-cf29-4130-9215-1005809ffa45` 채택**(재생성 1회 — 한도 안). 생성 전 잔액 2565.25, 거래 기록 2026-09-24T01:20:12Z −2 · 01:21:25Z −2(결과 파일 이름 `hf_20260924_012012_bda00c54…`·`hf_20260924_012125_d8b4bd0e…`와 같은 시각) = **이 절 몫 4크레딧**. 채택 원본 `6622f77a…`(2752 × 1536) → 저장 `37b09f23…`(1100 × 614). 결과 URL을 다시 받아 같은 폭으로 줄여 픽셀 대조 차이 0(bbox `None`). 저장 PNG 사본을 열어 그림 읽기를 씀. 채택본에서 왼쪽 전표의 주황 별이 프롬프트(칸 안)와 달리 네모 칸 **오른쪽 바깥**에 그려졌고, 그림 읽기는 보이는 그대로 적음(강사 확인 §9).

## 6. 도구 파일 · 묶음 목록

- `labs/part5/ch19-model-tools/notebooks/order_tools.py` **변경 없음**(해시 `ade40a313e396d3ef1de3e3bf264e68be155025f42c47803db8106e9d9c99e5e` 그대로). 이 절이 새로 만든 것은 양식 클래스 둘과 도구 둘뿐이고, 챕터 공통 B안(도구 파일은 평범한 함수만)대로 옮기지 않았습니다. 뒤 절이 같은 양식을 쓰려면 그 절 노트북에서 다시 적습니다(인계 §02→§03).
- 묶음 목록(`public-files.json` 두 곳)은 바꾸지 않았습니다(노트북 이름 그대로, 새 파일 없음).

## 7. 용어·금지어 확인

| 말 | 02절의 뜻 | 코드에서 |
|---|---|---|
| 양식 클래스(BaseModel) | 칸마다 자료형과 규칙을 적어 값을 검사하는 클래스(Ch 6 03 말) | `OrderQuery`·`OrderRecord` |
| 고를 수 있는 값(Literal) | 칸에 적을 수 있는 값을 몇 개로 정해 두는 표시 | `Literal["paid", "pending", "cancelled"]` |
| 입력 형식 클래스(args_schema) | 도구의 입력 형식을 매개변수 대신 정하는 양식 클래스 | `@tool(args_schema=OrderQuery)` |
| 입력 검사 | 도구가 몸통을 실행하기 전에 인자 딕셔너리를 입력 형식의 규칙에 맞춰 보는 일 | 걸리면 `ValidationError` |
| 내놓는 값 검사 틀(반환 스키마) | 도구가 내놓은 값의 칸을 코드가 따로 검사하는 양식 클래스, 도구 명세에 없음 | `OrderRecord.model_validate(row)` |
| (새 말 아님) 칸 · 값 검사 오류 · 몸통 실행 줄 · 최대 개수 · 꼭 채울 칸 · JSON 스키마 모양 | 「필드」 대신 · Ch 6 01 말 · `print("몸통 실행 …")` · `limit` · `required` · Ch 6 03 말 | |

- meta 「새 용어 5」 = 위 다섯.
- 금지어 `grep`(노트북 설명·`_src` 글·코드·출력·그림 라벨): 분기·경로·임계값·재정렬·쿼리·인덱스·융합·조각·노드·한 겹·돌려·프롬프트·폴백·레코드·캐시·병렬·범주·사전·거부·측정·집합·정규화·추정·필드·인터페이스·인라인·장식·로직·포장·직렬화·식별자·문맥·동시·강사 시연·개선 전·쉽게·간단히·당연히 **0건**. 「반환」은 제목 풀이 두 곳(노트북 1절·b2)과 용어 표 한 칸 「내놓는 값 검사 틀(반환 스키마)」뿐, 「검증」은 Ch 6 03 파일 이름(링크 주소) 하나뿐, 「로그」는 모두 「프로그램」. 「Pydantic」은 제목 풀이 두 곳·Ch 2 10 링크 주소·참고 자료 제목뿐. 「스키마」는 제목 풀이·용어 표·「JSON 스키마 모양」(Ch 6 03 말)뿐.

## 8. 보호 파일 · 챕터 밖 수정

- 보호 파일: `before-manifest.json` 39개 다시 셈 → **모두 같음**(바뀐 것 0 → `manifest-changes.md` 만들지 않음).
- 챕터 밖 수정: 실습 폴더 `labs/part5/ch19-model-tools/notebooks/02-Pydantic-인자와-반환-스키마.ipynb`(`536491c3…` → `1244ce6f…`) · `textbook/_notebook/checks/notebook-contracts-part5-ch19-model-tools.json`(`verify.py --chapter`가 다시 씀). 공용 도구·규격·과정 요약·계약 파일·Part 6 파일·완료 챕터 파일·도구 파일·묶음 목록은 고치지 않음. 02 노트북은 Part 6 선행 목록에 없음(03·05·06만).

## 9. 강사 확인 대상

1. **제목 「Pydantic 인자와 반환 스키마」의 두 말**을 두고 본문에서 한 번씩 풂(Pydantic = `BaseModel`을 주는 라이브러리 이름 · 반환 스키마 = 도구가 내놓는 값의 칸을 코드로 검사하는 틀, 모델에게 가지 않음).
2. **5절의 만든 줄**(`O105`·`C004`·금액 −9000)을 내놓은 값 검사가 거르는 모습을 보이려고 셀에서 만듦 — 본문·b7에 밝힘.
3. **몸통 첫 줄 `print`**를 도구 몸통에 넣어 「몸통 실행 전에 막음」을 출력으로 보임(도구가 출력하는 모양이 학생에게 익숙하지 않을 수 있음).
4. 삽화 `02-5`: 왼쪽 전표의 주황 별이 네모 칸 밖에 그려졌고(프롬프트는 칸 안), 오른쪽 전표가 1100px에서 얇게 보임. 「두 전표에 같은 별 · 열린 창의 빈 접시 · 닫힌 덧문」으로 관계는 읽힌다고 보고 채택.
5. 코드 줄 증가 55 → 109(코드 셀 20~30 기준에 맞추려는 늘어남, 01절과 같은 사정).
6. `limit`을 꼭 채울 칸으로 둔 까닭(기본값을 주면 함수에도 기본값 매개변수가 필요해짐)과, 그래서 After 입력에만 `"limit": 1`이 붙는 점.

## 10. 남은 것 · 지우지 않은 것

- **지워야 하지만 지우지 않은 것**: 기기 `/tmp/ch19-02/`(생성 원본 PNG `illu-1-orig.png`·`illu-2-orig.png`·`illu-2-again.png`·축소본·확대본, A·B 사본 노트북, `probe.py`·`probe2.py`·`extra_check.py`·`shrink.py`·`crop.py`·`crop2.py`·`cmp.py`) · `.cache/ch19-02-view/`(그림 확인 사본 열한 장 — Mermaid 넷·삽화 1차 원본 하나(3.1MB)·축소본 둘·확대본 셋·저장 사본 하나) · `qa/upgrade/gates-wip-02-02.json`(첫 실행 전 G1·G2·G6 확인 — `gates-wip-02.json`으로 갈음) · `qa/upgrade/__pycache__/`(확인 스크립트가 생성기를 import하며 생김).
- 옛 그림 `figures/02-Pydantic-인자와-반환-스키마-flow.*` 셋은 그대로 둠(본문 참조 0 — 마감 삭제 승인 목록).
- 마감 몫: `part5-practice.zip` 다시 만들기, 실습 폴더 README, `chapter.json` `objectives` 1행 「입력·반환 스키마를 설명」 대조(이 절 풀이와 맞음 — 「반환 스키마」는 코드 쪽 검사).

## 마감 반영 (2026-09-24)

검토 1차(`review-round1-A.md`·`review-round1-B.md`)를 반영했습니다. **노트북은 다시 실행하지 않았습니다**(`code_sha256`·`outputs_sha256`·`executed_at` 그대로, 마크다운만 — `mdpatch.py`로 생성기·노트북·`_src`를 같이 고친 뒤 `run_section.sh … --no-exec`). 전체 기록은 `chapter-summary.md` §15.

- **A-4**: 용어 표 「입력 검사」 칸에 「[Ch 16 01절](링크)의 입력 검사(모델을 부르기 전에 사용자 질문을 보는 일)와는 보는 값과 자리가 다릅니다」 한 문장(말은 그대로). 02 노트북에는 「입력 검사」라는 말이 없어 노트북은 A-11만.
- **A-1 짝 문장**: b4 비유 둘째 단락에 「01절 그림의 동그라미는 설명 글의 안내였고, 그 도구의 입력 형식이 정한 칸은 글을 적는 빈칸 하나였습니다. 그래서 …」.
- **자리 찾기 셀 결과 읽기(A-11·B-14)**: 「교재 출력은 실행 도구에 도구 파일 폴더를 따로 알려 준 실행이라 `.`이 찍혔습니다」와 「셀 안의 안내 글은 실습 폴더 맨 위도 적었지만, 도구 파일을 가져오려면 `notebooks/` 폴더에서 열어야 합니다」를 더함. 셀 안 `assert` 안내 글(「notebooks 폴더나 실습 폴더 맨 위에서」)과 생성기의 같은 코드는 그대로 — **다음 재실행 때 「notebooks 폴더에서」로**.
- 노트북 파일 `1244ce6f…` → `e5a8b5e3…`. 게이트 0(검사 문장 349).
