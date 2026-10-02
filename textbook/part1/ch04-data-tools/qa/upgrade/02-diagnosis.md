# 02-관계형-테이블과-키 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/02-relational-keys.*`).
생성기: `qa/upgrade/author_02.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch04-data-tools 02`.
수정 전 게이트는 01절 작업 때 챕터 전체로 남긴 `gates-before.json`(02절 34건)을 씁니다.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 8 | 0 |
| G6 | 23 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 16 (준비 1 + 본문 15, 최대 9줄) |
| 검사한 문장 | 90 | 320 (검토 반영 뒤, `gates-after.json`) |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Linux aarch64, Python 3.12.13, pandas 3.0.5, 2026-09-16), `verify.py --chapter` `PASS 5 sections / 51 code cells (max 20 lines)`(03~05절은 개선 전), `visual.cjs` 1280·390px PASS(이 절 HTML을 `/tmp`에 복사해 실행), 실습 폴더 pytest 10 passed(`data_tools.py`는 고치지 않음).

## 수정 전 주요 문제

- 게이트가 세지 않은 사다리 밖 문법: `from pandas.errors import MergeError`(점 경로 import), `pd.DataFrame([딕셔너리, …])`(01절에서 안 씀), `pd.concat([표, pd.DataFrame([...])])` 안에 호출 두 겹, 열 목록 선택 `joined[["order_id","name","amount"]]`, `to_string(index=False)`, `iloc`, `.tolist()`, try의 `else`와 `raise AssertionError`(Ch 2 요약 §5 미교육), 한 줄 `assert A and B and C`, 한 셀에 조인·합계·검증·예외를 몰아 둠(Before 셀 12줄)
- 01절과 이어지지 않음: 준비 셀·임시 폴더 없음, CSV 파일 대신 셀에서 표를 만듦, 「앞에서 배운 내용」이 한 단락(「앞 절에서 주문 세 건을 DataFrame으로 표현」)이고 01 개선본의 마스크·`loc`·`sum()`·Before 합계를 쓰지 않음. 01은 `orders.csv`를 `with open`으로 씀
- G5: 제목 셀·오늘 볼 그림 없음, 결과 읽기 셀이 없거나 출력 값을 인용하지 않음
- G6: 코드 이름·영문+조사로 시작하는 문장 18개(「`validate="many_to_one"`은」, 「Before는」 등), 70자 초과 5개. 한 문장에 인자 세 개 설명을 몰아 넣음
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. 기존 Excalidraw 도식 1장
- 내용: 「pandas에서는 문자열 열의 결측값이 `NaN` 또는 `<NA>`처럼 표시될 수 있습니다」는 노트북에서 한 가지만 봄. 「`validate="many_to_one"`은 … 검사」 동작 설명에 설치본 확인 기록 없음. 값 바꿔 보기가 `concat`+`indicator=True`+`_merge` 열로 새 API 세 개를 한 셀에 씀

## 바꾼 것

- 노트북: 제목(할 일 3, API 키 불필요·호출 0번·1분 이내, 기준 pandas 3.0.5·Python 3.11 이상·pandas 2 이하 실행 안 함) → 오늘 볼 그림(02-1) → 준비(`mkdtemp(prefix="ch04-02-")`+`chdir`+`listdir` `[]`) → `import pandas as pd`(01절 별명 한 문장 복습) → `customers.csv`(C001 김하나, C002 이두리) → `orders.csv`(01 주문 세 건에 `customer_id` 열, `sorted(os.listdir())`) → 두 표 읽기 → `is_unique` `True`/`False`(기본 키·외래 키 정의, 출석 번호 예) → `orders.merge(customers, on="customer_id")` 3행·assert(조인 정의, Ch 3 `git merge`와 구분) → 연결한 표에 01절 마스크·`loc`·`sum()` → `김하나 고객의 주문 합계: 59000` → 값 바꿔 보기 `copy()`+`loc[2, "customer_id"] = "C003"` → 2행(내부 조인 = 기본값) → `how="left"` 3행·`NaN`(결측값) → Before `all_customers.csv`(C001 줄 두 번) → 5행 → 합계 `77000` vs `136000` → After `validate="many_to_one"`+`except pd.errors.MergeError` → `drop_duplicates()`·`True` → 검사 켠 채 3행·`77000`·assert → 정리
- 데이터·학습 질문(키로 두 표를 이을 때 행 수 지키기)·paired 형식 유지. 고객 이름 김하나·이두리, 주문 O101~O103, 합계 77000·136000은 개선 전 노트북·03절·`data_tools.py` 테스트와 같음
- Before 원인을 「지난달과 이번 달 고객 목록을 이어 붙이다 C001 줄이 두 번 들어감」으로 바꿔 `concat` 없이 파일 하나로 재현. 개선 전의 `김하나(중복)` 대신 같은 줄 반복이라 After가 인자 없는 `drop_duplicates()`로 끝남(번호는 같고 이름이 다른 줄은 주의 메모에 「만들어 보지 않음」)
- 가르치지 않은 문법 처리(Ch 3 요약 §5, 01 handoff): `from pandas.errors import`는 `pd.errors.MergeError`(「pandas 안의 errors 모듈에 있는 오류 이름이라 점으로 이어 적음」 한 문장)로, `pd.DataFrame`·`concat`·열 목록·`to_string`·`iloc`·`tolist`·`indicator`는 뺌. `raise`·try의 `else`·내포식·`Path`·`TemporaryDirectory`·`list[dict]`·`str | None`·f-string 안 식·`@`·`BaseModel`·`*args` 없음. 새로 쓴 모양은 `표.copy()`(Ch 2 03절 목록 `copy()` 연결), `표.loc[인덱스 번호, 열 이름] = 값`(01 `loc[마스크, 열]` 자리 설명), `sorted(os.listdir())`(Ch 2 03절)
- 본문 10블록 전체를 다시 씀. 「이 절의 질문」, 용어 8개 표(기본 키·외래 키·다대일 관계·정규화·조인·내부 조인·왼쪽 조인·결측값), 비유(주문 쪽지와 카드 상자), 「앞에서 배운 내용」 4단락(01절, Ch 2 03·05절, Ch 3 02절 `git merge`와 이름만 같음), 주의 메모에 실행하지 않은 것(짝 없는 키 + validate, 이름이 다른 중복 줄, 빈 기본 키, 다른 OS·pandas 2)과 01절 `git status --short` 연결. 복습 5문항
- 그림: Mermaid 4장(두 표와 키, 두 표 연결, 짝 없는 키, 겹친 키 Before/After). 삽화 1장은 2회 생성 모두 탈락해 **삽화 대기**(prompt·caption만, `illustration-pending.md`). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)
- 라이브러리 동작 확인(설치본 pandas 3.0.5): `DataFrame.merge` 시그니처 `how='inner'`·`validate=None`, 설명서 「inner: … preserve the order of the left keys」, `_MergeOperation.__init__`에서 `_validate_validate_kwd`가 결과 계산(`get_result`) 전에 실행됨, 메시지 `Merge keys are not unique in right dataset; not a many-to-one merge`, `MergeError`는 `ValueError` 하위, `drop_duplicates(subset=None, keep='first')` 설명 「by default use all of the columns」, `Series.is_unique` 설명

## 그림 확인

- PNG 네 장을 직접 열어 확인. 02-1 첫 판(LR + 노란 검사 상자 두 개)은 O101 화살표가 O102 상자를 가로지르고 노란 상자가 흩어짐. TB로 바꾼 둘째 판은 화살표가 고객 표 제목 글자를 덮음. 셋째 판은 LR에 칸 제목 세 줄(`<br>`)이 행 상자와 겹침. 넷째 판에서 칸 제목 한 줄에 `모두 다른가: False/True`를 넣고 노란 상자를 뺌(viewBox 542). 주문 상자가 O101·O103·O102 순서로 놓여 도식 읽기·노트북 그림 설명에 적음
- 02-3 첫 판은 두 칸이 왼쪽 조인 → 내부 조인 순서로 놓였고, `~~~`로 순서를 잡은 둘째 판은 칸 높이가 어긋남. subgraph 정의 순서를 바꾼 셋째 판에서 왼쪽 내부 조인, 오른쪽 왼쪽 조인, 같은 높이. 초록 상자 라벨을 세 줄로 나눠 `C003` 줄바꿈 제거
- 02-4 After 둘째 줄 화살표에 「다시 연결」 라벨을 더해 drop_duplicates 뒤 다시 merge했음을 보이게 함
- 삽화 02-5(쪽지와 카드 상자): 1차 job `0b0f8381-25a1-473e-989f-93a4e941245c` 탈락(회색 끈이 엇갈려 초록 쪽지 끈이 파란 카드로 감). 끈 색을 스티커 색과 같게 고친 2차 job `31286c11-a64c-4fda-9082-a851abaa91e8` 탈락(위 초록 끈이 파란 스티커에서 끝남, 카드 뒤에 빈 카드가 겹침). 4크레딧(잔액 2916에서). 규격 §5-4대로 prompt 파일에 「다음 시도 프롬프트」(끈 없이 카드 아래에 쪽지를 모아 놓기)를 남김. 저장한 PNG 없음

## 검토에서 볼 곳

- 값 바꿔 보기에서 `changed_orders.loc[2, "customer_id"] = "C003"`(인덱스 번호로 칸에 대입)을 한 문장 설명으로 넘긴 것이 A 트랙 학생에게 충분한지. 대안은 파일을 하나 더 쓰는 방식(셀이 길어짐)
- Before를 「같은 줄이 두 번」으로 만들어 After가 인자 없는 `drop_duplicates()`로 끝나는 설계. 번호는 같고 이름이 다른 실제 중복은 주의 메모에만 둠
- 02-1 도식에서 노란 검사 상자를 빼고 칸 제목에 `is_unique` 출력을 적은 것(색 규칙상 출력은 노랑이지만 배치 문제로 제목에 둠)

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept(하 3, 공통 C-2). 모두 반영했습니다.
- 02-1: 13번 설명 「메서드 `drop_duplicates()`는 앞에 이미 나온 줄과 모든 열의 값이 같은 줄을 지운 새 표를 반환합니다.」
- 02-2(Q2 권고: `loc` 대입 한 줄 유지): 9번 설명에 「대입 기호 왼쪽에 `loc[행, 열]`을 쓰면 그 칸을 읽지 않고 새 값을 저장합니다. 숫자 2는 주문 O103 행의 인덱스이고, 복사한 표만 바뀝니다.」 기존 문장의 「새 값을 저장」과 겹치지 않게 앞 문장을 「01절에서 마스크를 넣던 자리에 인덱스 번호를 넣은 모양」 하나로 합침
- 02-3: 본문 b2 셋째 단락 「03절에서는 같은 두 표를 SQL로 잇고, 고객 번호로 주문을 찾는 조회 함수를 만듭니다.」
- C-2: 라벨 줄 9개(`고객 표:` 2곳, `주문 표:`, `연결한 표:` 3곳, `김하나 고객의 금액:`, `왼쪽 조인한 표:`, `겹친 줄을 지운 고객 표:`). 5번 결과 읽기 「위의 고객 표」「아래 주문 표」를 「라벨 줄 `고객 표:`/`주문 표:` 아래의 표」로
- 삽화 02-5: 절당 재생성 1회 한도(2회 생성)를 이미 써서 새로 생성하지 않음. **삽화 대기 유지**(`illustration-pending.md`, 크레딧 0)
- 코드 셀 16, 검사한 문장 320

재실행: 생성기 `author_02.py` 수정 → `run_section.sh … 02`(새 커널 PASS). 코드 셀 출력은 새 라벨 줄·임시 경로·포트를 빼고 반영 전과 같습니다. 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0, `qa/upgrade/gates-after.json`), `verify.py --chapter` `PASS 6 sections / 96 code cells (max 21 lines)`, `visual.cjs` 14건 PASS, 실습 폴더 pytest 10 passed. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- **삽화 1장 대기(02-5)**: 절당 재생성 1회 한도를 이미 써서 이번 마감에서 새로 생성하지 않음. 다시 만들 수 있게 되면 `illustration-pending.md` 순서대로 생성·검수하고, 넣은 뒤 `run_section.sh … 02 --no-exec`·게이트·저장 PNG 대조
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(`review-round1.md` 끝 「반영 결과」의 볼 곳)가 남음
- 리뷰 묶음: `qa/upgrade/review-pack/02-관계형-테이블과-키.md`
- 정리 대상(삭제하지 않고 목록만): `figures/02-relational-keys.excalidraw`·`.svg`(옛 도식, 본문에서 뺌)
- 01절에서 본 것(고치지 않음, 01 담당 검토에 넘김): 01 노트북 「오늘 볼 그림」 설명이 TB 도식 01-1에 「왼쪽에서 오른쪽으로 읽습니다」·「오른쪽 끝 상자」라고 적음(PLAYBOOK §4 방향 말 규칙) → 검토 1차 01-1로 반영 완료
