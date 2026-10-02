# 01절 진단과 개선 기록 — tool과 Ch 4 함수 재사용 (paired)

- 작업 2026-09-24 · 규격 `textbook/QUALITY-UPGRADE.md`(§2·§2-7·§3·§4·§5-3·§5-4·§6·§7-2·§8) · 생성기 `qa/upgrade/author_01.py`(노트북 + `_src` 함께).
- 1차 자료: `qa/upgrade/chapter-lead-notes.md`(준비 담당 조사) + 챕터 리드 결정 10개(`handoff.md` 「챕터 공통」).
- Part 5 셋째 챕터의 첫 절입니다. **모델 요청 0번**(API 키 셀·모델 셀 없음), 임베딩 0. 읽는 파일 `data/orders.csv` 하나, 쓰는 파일 0.

## 1. 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 6 | 92 | 1 | 1 | 0 | 0 | 6 | 20 | 3 | **31** |
| 수정 뒤(`gates-wip-01.json`, `--no-exec`) | **21** | **347** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 `upgrade_gates.py … --label wip-01 --section 01` → `gates-wip-01-01.json`: G1 0 · **G2 2**(`print(…, list(딕셔너리.keys()))` 두 겹 호출 둘 → 중간 변수 `row_keys`·`part_keys`) · **G6 2**(긴 문장 둘 — 나눔) · G7 18(그림 전). 고친 뒤 G1·G2·G6 0으로 실행.
- `verify.py --chapter` → `PASS 6 sections / 58 code cells (max 16 lines)`(16줄은 아직 고치지 않은 02~06절, 01절 셀은 주석 포함 최대 11줄 — 자리 찾기 준비 셀). 빌드 HTML 일곱 개 `{{` 잔존 **0건**.
- 코드 줄(주석·빈 줄 뺌, `count_code.py`) 38 → **90**, 도구 파일 6줄. 비준비 셀 최대 **6줄**, 함수 본문 최대 **1줄**(+ 독스트링). 셀당 정의 하나.
- 게이트가 세지 않는 과정 금지 문법은 따로 AST로 셌습니다(`/tmp/ch19-01/extra_check.py` — 데코레이터가 `@tool` 밖·타입힌트가 `@tool` 매개변수 밖·복합 타입힌트·반환 힌트·기본값 매개변수·독스트링이 `@tool` 밖·변수 주석·클래스·f-string·`key=`/`reverse=`·집합·`set`/`next`/`sum`/`max`/`min`/`zip`/`enumerate`/`sorted`/`any`/`all`/`isinstance`·`.get`/`.setdefault`·튜플 풀기·`+=`·별표). **노트북 0건**, 도구 파일 1건(`fetch_orders`의 `status=None` — Ch 4 약속 시그니처, §3 결정 1).

## 2. 수정 전 주요 문제

1. **실행하지 않은 사실을 적음**: b3 「원본 함수와 AST가 같은지 검증 기록에서 확인할 수 있습니다」·b7 「원본 해시는 출처 추적용…」 — 노트북에 AST·해시 비교가 없었습니다. → 학생 본문에서 뺐습니다. AST 대조는 이 진단(§8)에만 적습니다.
2. **b6 「일부러 실패해 보기」가 실패 장면이 아니라 `cancelled` 비교를 설명**(블록 내용과 `{{notebook:…|failure}}`가 어긋남).
3. `fetch_orders`를 노트북에 다시 적음(01~05 다섯 번 같은 셀) — 규격 §2-7 3항과 부딪힘.
4. 금지·미교육 문법: 준비 셀 `find_up(name: str) -> Path | None`(정의+호출·`Path`·`(current, *current.parents)` 별표 풀기) · `str | Path`·`list[dict[str, Any]]`·`from typing import Any` · 키워드 전용 `*`·기본값 `None`·`dtype` 풀이 없음 · After의 집합 내포식 `{r["order_id"] for r in result}`·한 글자 이름 `r` · 반환 힌트.
5. `%pip` 셀·결과 읽기 셀·제목 셀·핵심 그림 없음(G5 6). 데코레이터·독스트링·타입힌트의 뜻을 풀지 않음(과정 첫 독스트링). 제목 「tool」 뜻 풀이 없음.
6. 금지어: 반환 ×8 · 돌려주는 · 사전 ×3 · 경로 ×6 · 검증 ×7 · 필드 ×2 · 인터페이스 ×4 · 인라인 · 장식 · 로직 · 포장(준비 조사 §1). 비유 「주문서」는 Ch 2 06·13과 겹침. G6 20(70자 초과·영문 시작·빽빽한 단락).
7. 옛 생성기 둘(`_make_sources.py`·`figures/_gen_figures.py`)이 실행하면 개선본을 덮어씀.

## 3. 챕터 리드 결정의 반영

| 결정 | 반영 |
|---|---|
| 1 `fetch_orders` = Ch 4 실습 폴더 판 | `notebooks/order_tools.py`에 옮김. 주석 `# Ch 4 01절에서 배웠습니다 — Ch 4 실습 폴더 data_tools.py의 판을 옮겼습니다(자료형 표시만 뺐습니다)`. **Ch 4에서 처음 가르친 절은 01**(Ch 4 01 노트북이 `fetch_orders(file_name, status)`를 만들고 b7이 실습 폴더 판 `fetch_orders(csv_path, *, status=None)`을 소개 — `chapter-summary.md` 12·38·55행 확인). 본문 2절에서 두 판의 차이(위치 인자 ↔ 키워드 인자 `status=`)와 별표 `*`·`status=None`을 한 문장씩 풂. `dtype` 딕셔너리는 「Ch 4 01절이 말만 하고 실행하지 않았던 방법」으로 이음 |
| 2 도구 파일 B안 `order_tools.py` | 평범한 함수 하나(`fetch_orders`)만, `@tool`은 노트북. 파일 안 CSV 상수 없음(인자 `csv_path`). 이름은 `verify.py` 금지 이름(`openai`·`rag`·`context_lab`·`document_processing`·`experiment`·`harness`·`prompts`)과 겹치지 않음. 묶음 목록 둘에 더함(§8). Ch 6 06 `estimate_cost`는 01이 쓰지 않아 넣지 않음(04 몫) |
| 3 도구 정의 문법 범위 | `@tool`(맨 모양 하나) · `status: str` · 독스트링. 데코레이터 = 「함수 위에 붙여 그 함수를 다른 것으로 감싸는 표시」 + 「이 줄은 아래 함수를 도구로 등록합니다」(L6 문장) + Ch 2 09 `@` 줄 규칙(「같은 이름에 담는다」)과 링크 · 독스트링 세 문장(뜻 → 요리법 카드 소개 → 도구 설명이 됨) · 타입힌트는 Ch 2 07과 잇고 「이 챕터는 도구로 감쌀 함수의 매개변수에만」. **반환 힌트 쓰지 않음**. 게이트 허용 방법은 §4 |
| 4 01은 모델을 부르지 않음 | 준비물 「모델 요청은 0번이라 API 키가 필요 없고 … 도구를 만들고 부르는 일은 모두 파이썬 안에서 끝나기 때문」. 키·모델 셀 없음. 묶음 모양 키 없는 실행으로 확인(§6) |
| 5 `bind_tools` 약속 순서 | 01은 b4·노트북 4절에서 「모델에게 도구를 알려 주는 메서드(`bind_tools`)는 04절에서 처음 씁니다」로만 적음. Ch 7 05·Ch 17 03의 「Ch 19 05절」 문장은 고치지 않음(인계) |
| 6 용어 | §9 표 |
| 7 paired Before = 실제 결함 | §5 |
| 8 비유 「식당 주문 전표와 내주는 창」 | b4 비유 단락·노트북 3·4·6절·삽화 `01-5`. 쟁반·주문서 쓰지 않음 |
| 9 옛 생성기 막기 | §10 |
| 10 `%pip`·결과 읽기 셀 | 준비 셀 셋(설치 → 가져오기 → 자리 찾기), 셀마다 결과 읽기 |

## 4. 게이트가 `@tool`·타입힌트·독스트링을 허용한 방법 (Ch 22 선례 확인)

- `textbook/_notebook/checks/upgrade_gates.py`의 G1(`g1_ladder`)은 `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`/`nonlocal`·`*args`/`**kwargs` 정의·함수 안 함수·본문 10문장 초과·클래스(`BaseModel`/`TypedDict` 필드만은 통과)·셀당 정의 둘을 셉니다. **데코레이터·타입힌트·독스트링은 세지 않습니다.** 독스트링은 함수 본문 길이 셈에서도 빠집니다(`ast.Expr` + `ast.Constant` 제외).
- Ch 22 노트북 01·04·06·09의 `@tool` + `lookup_hours(day: str) -> str` + 독스트링 셀에는 **`upgrade_allow` 메타데이터가 없습니다**(이번에 네 노트북 셀 메타데이터를 읽어 확인). 그래서 Ch 22와 같이 **메타데이터 없이** 두었습니다.
- 대신 규격이 막는 나머지 문법은 §1의 따로 만든 AST 검사로 0건을 확인했습니다(`@tool` 밖 데코레이터·`@tool` 매개변수 밖 타입힌트·반환 힌트·`@tool` 밖 독스트링 포함). Ch 22와 달리 **반환 힌트(`-> str`)는 쓰지 않았습니다**(챕터 리드 결정 3).

## 5. 설계 — paired

- **예시(1~4절)**: Ch 4 함수 직접 호출(전체 4줄·칸 자료형·`status="paid"` 2줄) → `@tool` 정의 → `type(…).__name__`(`function` vs `StructuredTool`) → 속성 `func`(원래 함수가 안에 있음) → `name`·`description`(+ `__doc__`와 같은가 `True`) → `args` → `convert_to_openai_tool` 도구 명세 → 명세의 칸·인자·필수 인자·`"csv" in str(tool_spec)` `False`.
- **Before(5절)**: Ch 4 버릇대로 `list_orders_by_status("paid")` → **실제 `TypeError: 'StructuredTool' object is not callable`**(langchain-core 1.6.2, 이번 새 커널 세 번 모두). 셀은 Ch 2 05 모양 `try/except TypeError as error`로 그 오류만 받고(「실제 프로그램이라면 여기서 멈춥니다」), 둘째 셀 `callable` 두 줄(`True`/`False`)로 원인을 보임. 규격 §5-3대로 받았어도 Before 결함 결과라 그림 `01-3`에서 빨강(Ch 4 05-3·Ch 18 02 선례).
- **After(6절)**: `.invoke({"status": "paid"})` → 2줄 · 2절 직접 호출과 `==` `True`(+ `assert`, CSV에서 정해지는 값) · `cancelled`도 `O104` 한 줄로 같음(빈 목록끼리 같은 것이 아님).
- **값 바꿔 보기(7절, `lesson_part="after"`)**: 매개변수 `: str` 하나만 뺀 도구(두 도구를 함께 보려고 함수 이름만 다름 — 본문에 밝힘) → 입력 형식 `{'status': {'title': 'Status'}}`·명세 `{'status': {}}` · 결과는 같음 `True`. LangChain 문서가 「타입힌트는 꼭 적으라」고 한 것과 「빼도 도구는 만들어지고 자료형만 빠진다」를 함께 적음.
- 잘못된 자료형(`{"status": 3}`)을 넣는 장면은 **02 몫으로 남김**(노트북 밖 확인: 힌트 있는 도구 → `ValidationError`(`string_type`), 힌트 없는 도구 → 오류 없이 `[]`). 01 본문은 「이번에 보지 않았습니다」.
- `assert`는 CSV 파일에서 정해지는 값 두 곳(After 둘)뿐. 모델 답 `assert` 0(모델 없음).

## 6. 실행값 (새 커널 세 번 + 키 없는 묶음 모양 실행)

| 실행 | 방법 | 시각(UTC) | `code_sha256` | `outputs_sha256` | 셀별 대조 |
|---|---|---|---|---|---|
| A | `run_section.sh … 01` | 00:49:55~57 | `acf002bdaf50…` | `990530ef6fb2…` | — |
| B | 사본 `/tmp/ch19-01/B.ipynb`, 같은 가상환경 새 커널 | 00:50:25~27 | `acf002bdaf50…` | `990530ef6fb2…` | A와 **21/21 같음** |
| C(교재 출력) | 삽화·캡션 상수를 넣고 `run_section.sh … 01`(생성기가 출력을 지우므로 다시 실행) | 00:55:13 | `acf002bdaf50…` | `990530ef6fb2…` | A·B와 같음 |
| 묶음 모양 | `/tmp/ch19-01/bundle/part5-practice/labs/part5/ch19-model-tools/`에 `data/orders.csv`·`notebooks/`(노트북·`order_tools.py`)·`pyproject.toml`·`uv.lock`·`README.md`만 복사, 작업 폴더 `notebooks/`, **`env -u OPENAI_API_KEY -u PYTHONPATH`**, 커널 = 이 챕터 가상환경 python | 00:51 | `acf002bdaf50…` | `ee3fb222e97f…` | 다른 셀은 자리 찾기 한 줄 `찾은 프로젝트 맨 위: ../../../..`뿐(본문이 예고한 값) |

- 모델이 없어 흔들린 값이 없습니다. 흔들림 확인(노트북 밖 다섯 번)은 해당하지 않습니다.
- 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답) A 1.8초 · B 1.6초 → 준비물 「3초 안에」. 커널 시작 시간은 들어 있지 않습니다. 본문은 「걸린 시간은 재지 않았습니다」(b7).
- 실제 `check_bundle_execution.py`(zip을 풀어 `uv sync --locked`)는 zip을 다시 만들지 않아 돌리지 않았습니다 — 마감 몫(zip에 `order_tools.py`가 들어가야 함).

## 7. 그림

- Mermaid 4장: `01-1-함수에서-도구로`(b4·노트북 「오늘 볼 그림」) · `01-2-도구-명세의-칸`(b5) · `01-3-괄호로-부르기와-invoke로-부르기`(b6) · `01-4-타입힌트를-빼면`(b6 값 바꿔 보기). 원본 viewBox 폭 736·668·642·611. **보라 0장**(모델 없음), **빨강은 `01-3` Before 결함 하나**. 라벨 숫자는 `O101`·`O103`만(출력에 있음). 첫 렌더에서 저절로 꺾인 라벨 셋을 `<br>`로 다시 나눔. 설계표 `01-figures.md`.
- 삽화 `01-5-메뉴판과-주문-전표`: 1차 job `c55f5e4e-6129-4ef7-995c-47987eb3e918` 채택, 재생성 0. 생성 전 잔액 2567.25, 거래 기록 2026-09-24T00:52:26Z 「Nano Banana Pro −2」(결과 파일 이름 `hf_20260924_005226_c55f5e4e…`와 같은 시각) = 이 절 몫 **2크레딧**. 원본 `c8eaaa3b…`(2752 × 1536) → 저장 `deb1a9e2…`(1100 × 614). 결과 URL을 다시 받아 같은 폭으로 줄여 픽셀 대조 차이 0. 원본을 확대해 전표의 동그라미 셋 가운데 둘째만 칠해진 것을 확인. 전표가 1100px 그림에서 작게 보이는 점은 강사 확인 대상(§12).

## 8. 도구 파일과 묶음 목록

- `labs/part5/ch19-model-tools/notebooks/order_tools.py`(새 파일) — 함수 **하나** `fetch_orders(csv_path, *, status=None)`, import `pandas`만, 코드 6줄, 해시 **`ade40a313e396d3ef1de3e3bf264e68be155025f42c47803db8106e9d9c99e5e`**.
- **AST 대조(이 절 작업에서 실행)**: `labs/part1/ch04-data-tools/data_tools.py`의 `fetch_orders`와 견줘 **몸통 문장 AST 같음**(독스트링 제외) · **인자 이름·키워드 전용·기본값 같음** · 자료형 표시 없음(`csv_path: str | Path`·`status: str | None`·`-> list[dict[str, Any]]`을 뺌) · 독스트링(「… 사전 목록으로 반환합니다」)을 빼고 주석 넷으로 갈음. 학생 본문은 「옮기면서 자료형 표시와 설명 글을 빼고 주석을 달았습니다」·「두 파일을 나란히 열어 볼 수 있습니다」까지만 적음(「같은 코드」라고 쓰지 않음).
- 묶음 목록: `textbook/part5/public-files.json`에 `labs/part5/ch19-model-tools/notebooks/order_tools.py` 한 줄(`8b9d1aca…` → `08ee1d6c…`) · 챕터 `qa/public-files.json` `labs`에 `notebooks/order_tools.py`(`826b2192…` → `21c78dde…`). `part5-practice.zip`은 다시 만들지 않음(마감 몫). Part 6 선행 목록(Ch 28 `qa/prerequisite-files.json`·`textbook/part6/prerequisite-files.json`)은 건드리지 않음 — 03·05·06이 도구 파일을 가져오면 마감 몫.

## 9. 용어·금지어 확인 (`_src`·노트북 설명·코드·출력·도구 파일 `grep`)

| 말 | 01절의 뜻 | 코드에서 |
|---|---|---|
| 도구(tool) | 모델이 고를 수 있게 이름·설명·입력 형식을 붙여 감싼 함수 | `@tool` 아래 `list_orders_by_status`, 종류 `StructuredTool` |
| 도구 설명(description) | 도구가 하는 일을 적은 글, 독스트링이 들어감 | `.description` |
| 독스트링(docstring) | 함수 첫 줄에 큰따옴표 세 개로 감싸 적는 설명 글 | `"""…"""`, `.__doc__` |
| 입력 형식(스키마, schema) | 도구가 받는 인자의 이름과 자료형을 적은 틀 | `.args` |
| 도구 명세(tool definition) | 이름·설명·입력 형식을 모델 요청에 실을 모양으로 한 딕셔너리에 모은 것 | `convert_to_openai_tool(…)` |
| (새 말 아님) 데코레이터 줄 · 도구 이름 · 인자 딕셔너리 · CSV 파일 위치 · 모델이 채울 인자 · 꼭 채울 인자 | Ch 2 09 · 함수 이름에서 옴 · `.invoke`에 넣는 딕셔너리 · 「경로」 대신 · 입력 형식의 인자 · 명세 `required` | |

- meta 「새 용어 5」 = 위 다섯.
- 금지어 `grep`(노트북 설명·`_src` 글·코드·출력·도구 파일): 분기·경로·반환·임계값·재정렬·쿼리·인덱스·조각·노드·돌려·프롬프트·폴백·레코드·캐시·병렬·검증·범주·사전·거부·측정·집합·정규화·추정·필드·인터페이스·장식·동시·「한 겹」·「쉽게·간단히·당연히」 **0건**. 「경로」는 첫 판의 「확장 경로·기본 경로」(Ch 2 트랙 이름) 두 곳을 `mdpatch.py`로 「Ch 2에서 건너뛸 수 있는 절」로 고침. 「스키마」는 「입력 형식(스키마, schema)」 원어 풀이 한 곳, `bind_tools`는 「모델에게 도구를 알려 주는 메서드(`bind_tools`)」 풀이 한 곳, 「tool」은 제목과 「제목의 tool은 도구라는 뜻」 풀이(노트북 1절·b2)뿐. 「Pydantic」·「병렬」 0.

## 10. 옛 생성기 막기 · 보호 파일 · 챕터 밖 수정

- 옛 생성기 막기: `textbook/part5/ch19-model-tools/_make_sources.py`(`b2d0b9ea…` → `8fcb94d3…`, `from __future__` 다음 줄) · `figures/_gen_figures.py`(`96de6118…` → `348b928d…`, 독스트링 다음 줄)에 설명 주석 셋 + `raise SystemExit("개선 전 생성기입니다. textbook/part5/ch19-model-tools/qa/upgrade/author_NN.py를 쓰세요.")`. 두 파일 모두 실행해 종료 코드 1·그 글만 나오는 것을 확인. 원본 사본은 준비 담당이 둔 `qa/upgrade/before/generators/`. 옮기기(`mv -n` → `before/generators/blocked/`)는 마감 몫.
- 보호 파일: `before-manifest.json` 39개 다시 셈 → **모두 같음**(바뀐 것 0 → `manifest-changes.md` 만들지 않음).
- 챕터 밖 수정: `textbook/part5/public-files.json`(한 줄) · 실습 폴더 `labs/part5/ch19-model-tools/notebooks/`(01 노트북·`order_tools.py` 새 파일) · `textbook/_notebook/checks/notebook-contracts-part5-ch19-model-tools.json`(`verify.py --chapter`가 다시 씀). 공용 도구·규격·과정 요약·계약 파일·Part 6 파일·완료 챕터 파일은 고치지 않음.

## 11. 참고 자료 확인 (WebFetch, 2026-09-24)

- `https://docs.langchain.com/oss/python/langchain/tools` — 기본 도구 이름은 함수 이름, 「the function's docstring becomes the tool's description」, 「Type hints are **required** as they define the tool's input schema」.
- 설치판 소스(가상환경): `langchain_core/tools/structured.py` 289행 「Function must have a docstring if description not provided.」(노트북에서 실행하지 않음 — 본문에 밝힘) · `langchain_openai/chat_models/base.py` 2435~2436행 `bind_tools`가 `convert_to_openai_tool(tool, strict=strict)`로 도구마다 명세를 만듦(본문 「소스를 보면」).
- Python 3.12 문서 `callable` 링크(본문 b10).

## 12. 강사 확인 대상

1. **제목 「tool과 Ch 4 함수 재사용」의 영어 「tool」**을 두고 본문에서 「도구」로 한 번 풂(Ch 15~18 선례).
2. **데코레이터·타입힌트·독스트링을 이 챕터 주제로 허용한 범위**(`@tool` 맨 모양 · 매개변수 `str` 힌트 · 독스트링, 반환 힌트 없음). A 트랙은 Ch 2 09를 건너뛰므로 세 문장 + 링크.
3. **새 API `convert_to_openai_tool`**(`langchain_core.utils.function_calling`)을 01에서 도구 명세를 보이려고 씀 — 과제가 말한 「tool.name·tool.description·입력 형식」보다 한 걸음 더(모델에 실릴 모양을 모델 없이 보임). 04가 `bind_tools`로 실제 요청을 보낼 때 같은 모양인지 확인할 몫.
4. `fetch_orders`의 키워드 전용 `*`·기본값 `None`(도구 파일, Ch 4 약속 시그니처) — 노트북 G1 규칙의 「기본값 매개변수 금지」는 정의에만 해당하고 01 노트북 정의에는 없음.
5. 삽화 `01-5`의 전표가 1100px에서 작게 보임(동그라미 셋과 주황 하나는 보임) · 「그림만 보고 관계가 읽히는가」 별도 검토.
6. 코드 줄 증가 38 → 90(+ 도구 파일 6) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘(코드 셀 20~30 기준을 맞추려는 늘어남).

## 13. 남은 것 · 지우지 않은 것

- **지워야 하지만 지우지 않은 것**: 기기 `/tmp/ch19-01/`(생성 원본 PNG `illu-1-orig.png`·`illu-1-again.png`·확대본·B 사본 노트북·묶음 모양 폴더 `bundle/`·`extra_check.py`·`probe.py`·`probe2.py`·`reps1.json`·`reps2.json`) · `.cache/ch19-01-view/`(그림 확인 사본 열한 장) · `qa/upgrade/gates-wip-01-01.json`(첫 실행 전 G1·G2 확인 — `gates-wip-01.json`으로 갈음) · `textbook/part5/ch19-model-tools/qa/upgrade/__pycache__/`(`pack.py`·확인 스크립트가 생성기를 import하며 생김).
- 마감 몫: `part5-practice.zip` 다시 만들기와 `check_bundle_execution.py`(zip에 `order_tools.py` — 이 절은 묶음 모양 임시 폴더로만 확인) · 옛 생성기 옮기기 · 옛 그림 `figures/01-tool과-Ch4-함수-재사용-flow.*` 셋(본문 참조 0, 그대로 둠) · 실습 폴더 README(「노트북은 서로 독립적」이 도구 파일 때문에 틀림) · `labs/part5/continuity-guide.md` 7행(「원본 SHA-256이 함께 적혀 있습니다」 — 사실과 다름) · Ch 7 05·Ch 17 03 「`bind_tools`는 Ch 19 05절」 문장.

## 마감 반영 (2026-09-24)

검토 1차(`review-round1-A.md`·`review-round1-B.md`)를 반영했습니다. **노트북은 다시 실행하지 않았습니다**(`code_sha256`·`outputs_sha256`·`executed_at` 그대로, 마크다운만 — `mdpatch.py`로 생성기·노트북·`_src`를 같이 고친 뒤 `run_section.sh … --no-exec`). 전체 기록은 `chapter-summary.md` §15.

- **A-1 삽화 글(다시 만들지 않음)**: PNG를 직접 보고, 그림 읽기 끝 문장에서 「동그라미 셋은 고를 수 있는 상태 셋」을 빼고 풀이 단락 하나를 더함(카드의 동그라미 셋 = 설명 글에 적은 상태 셋이라는 안내 · 전표의 칠한 동그라미 하나 = 고른 값 · 입력 형식은 `status`가 글이라는 것뿐 · 셋 밖의 글은 02절에서). 비유 첫 단락·용어 표의 「고를 칸」·「맵기 선택」 칸 → 「주문할 때 적는 칸」, 캡션 「그림과 고를 칸만」 → 「메뉴판만」(`01-5-…caption.md`도 같게). 02 b4에 짝 문장.
- **A-2**: b3 Ch 17 03 요약 → 「그 이름을 함수 `run_tool`에 넘겨 정해 둔 글을 받았습니다. 그 도구 흉내는 주문 번호 같은 값을 받지 않았습니다」.
- **A-3**: 노트북 2절 자료형 결과 읽기에 「이 CSV의 번호에는 글자 O·C가 섞여 있어 `dtype` 없이 읽어도 같은 자료형 — 차이는 Ch 4 01절이 예로 든 01234 같은 번호에서」.
- **A-12**: 노트북 준비 셀 결과 읽기 고정 문장 뒤(따로 단락)와 `_src` b3(Ch 2 07 링크)에 「Ch 2 07절에서 임시 폴더에 만든 같은 이름의 모듈과는 다른 파일 · 가져오기가 현재 작업 폴더에서 파일을 찾는 것은 그 절 그대로」.
- **A-10**: 도구 파일 `fetch_orders` 주석 「(자료형 표시만 뺐습니다)」 → 「(자료형 표시와 설명 글을 빼고 주석을 달았습니다)」 — 도구 파일 `f2f48a15…` → **`fa5975b5e2466cf205d84a235f4ace2e0655d28f28f276f4fc1e72da5c597062`**(AST 같음).
- **자리 찾기 셀 결과 읽기(A-11·B-14)**: 「교재 출력은 실행 도구에 도구 파일 폴더를 따로 알려 준 실행이라 `.`이 찍혔습니다」와 「셀 안의 안내 글은 실습 폴더 맨 위도 적었지만, 도구 파일을 가져오려면 `notebooks/` 폴더에서 열어야 합니다」를 더함. 셀 안 `assert` 안내 글(「notebooks 폴더나 실습 폴더 맨 위에서」)과 생성기의 같은 코드는 그대로 — **다음 재실행 때 「notebooks 폴더에서」로**.
- 노트북 파일 `5d376140…` → `ff44fdea…`. 게이트 0(검사 문장 347 → 359).
