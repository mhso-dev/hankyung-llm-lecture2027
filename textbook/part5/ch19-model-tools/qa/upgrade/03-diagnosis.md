# 03절 진단과 개선 기록 — 좋은 도구 이름과 설명 (experiment)

- 작업 2026-09-24 · 규격 `textbook/QUALITY-UPGRADE.md`(§2·§2-7·§3·§4·§5-3·§5-4·§6·§7-2) · 생성기 `qa/upgrade/author_03.py`(노트북 + `_src` 함께, 본은 `author_02.py`).
- 1차 지시: `handoff.md` 「챕터 공통」 + 「§02 → §03」 12항. 참고: `chapter-lead-notes.md` §2 03·§4-4·§5, `02-diagnosis.md`·`02-figures.md`, 과정 요약 §2·§3·§5·§6.
- **모델 요청 0번**(API 키 셀·모델 셀 없음, `bind_tools` 없음), 임베딩 0. 읽는 파일 `data/orders.csv` 하나, 쓰는 파일 0. 까닭(준비물에 적음): 도구 명세는 파이썬 안에서 만들어져 모델 없이 볼 수 있음. 모델이 도구를 고르는 실험·`bind_tools` 첫 사용은 04절(챕터 리드 결정). 흔들림 확인(노트북 밖 다섯 번)은 해당 없음(`03-probe.md` 만들지 않음).

## 1. 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 6 | 101 | 4 | 3 | 0 | 0 | 5 | 14 | 3 | **29** |
| 수정 뒤(`gates-wip-03.json`, `--no-exec`) | **27** | **349** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 `upgrade_gates.py … --label wip-03 --section 03`(`gates-wip-03-03.json`) → 첫 판 G1 0 · G2 0 · **G6 3**(70자 넘는 문장 셋 — b2 권고 넷을 한 문장에 · b7 노트북 밖 확인 문장 · b10 OpenAI 참고 자료 설명) · G7 18(그림 전). 둘로 나누고, 나눈 문장 하나가 다시 70자를 넘어 한 번 더 나눠 G1·G2·G6 0으로 실행.
- `verify.py --chapter`(`run_section.sh` 안) → `PASS 6 sections / 94 code cells (max 16 lines)`(16줄은 아직 고치지 않은 04~06절). 빌드 HTML 일곱 개 `{{` 잔존 **0건**.
- 코드 줄(주석·빈 줄 뺌, `count_code.py`) 44 → **130**(코드 셀 6 → 27). 준비 셀이 아닌 셀 최대 **9줄**(`check_tool` 정의 셀 — def 줄 + 본문 8줄), 준비 셀 최대 9줄(자리 찾기), 함수 본문 최대 **8줄**(`check_tool`), 셀당 정의 하나.
- **게이트가 세지 않는 과정 금지 문법은 AST로 따로 셈**(`/tmp/ch19-02/extra_check.py`를 그대로 씀 — 03은 `@tool(args_schema=…)`가 없어 01 판과 같은 결과): **1건 = 허용 범위** — 도구 파일 `fetch_orders`의 `status=None`(01·02와 같은 Ch 4 약속 시그니처). 노트북 **0건**: `@tool` 밖 데코레이터·`@tool` 매개변수 밖 타입힌트·복합 타입힌트·반환 힌트·기본값 매개변수·`@tool` 밖 독스트링·변수 주석·클래스·f-string·`key=`/`reverse=`·집합·`set`/`next`/`sum`/`max`/`min`/`zip`/`enumerate`/`sorted`/`any`/`all`/`isinstance`·`.get`/`.setdefault`·튜플 풀기·한 줄 다중 대입·`+=`·별표·세미콜론·내포식·제너레이터 식·`lambda`·조건 표현식. `try` 0개. 도구 함수 일곱(짧은 판 셋·자세한 판 셋·`order_info`)은 모두 맨 `@tool` + 매개변수 `str` 힌트 하나 + 한 줄 독스트링.

## 2. 수정 전 주요 문제

1. **experiment인데 실험이 없었습니다.** 세 도구의 `name`·`description`·`args` 출력과 설명 글자 수·`args` JSON 글자 수(`46 49` · `33 53` · `26 49`)뿐이고, 예상·비교·값 바꿔 보기가 없었습니다. b6 「실험 결과 해석」은 「선택 정확도는 다음 절에서 실제로 측정합니다」 한 줄(노트북).
2. 한 건 찾기 `next((r for r in rows if …), {…})`·집계 `sum(r["amount"] for r in rows)`(제너레이터 식 둘·한 글자 `r`), 한 셀에 도구 둘, 반환 힌트 `-> list[dict[str, Any]]`·`-> dict`, `len(json.dumps(…))` 두 겹 호출, 집합 내포식 `assert`, 준비 셀 `find_up`(`Path | None`·별표 풀기)·`fetch_orders` 다시 적기(`str | Path`·`Any`).
3. b4 「도구 이름은 동작과 대상을 함께 드러내야 합니다」·「설명은 언제 골라야 하는지와 반환값을」은 **근거 없이 단정**했고, 코드로 확인하지 않았습니다. 좋은 설명이면 모델이 잘 고른다는 뉘앙스(「질문의 의도와 대응시키기 쉽습니다」)도 확인 없이 적혀 있었습니다.
4. `%pip` 셀·결과 읽기 셀·제목 셀·핵심 그림 없음(G5 5). 금지어: 반환·측정·필드·식별자·직렬화·문맥·돌려주는 등(준비 조사 §1). 비유 「주문서」는 Ch 2와 겹침. b4 끝 「도구 호출·도구 메시지」 틀 문장(이 절과 무관), b5 「모델 호출이 있는 절은 …」 틀 문장.

## 3. 설계 — experiment (결정과 까닭)

- **실험 변수 = 도구 설명 하나.** 같은 몸통 함수 셋에 **같은 이름·같은 입력 형식**으로 설명만 다른 두 판을 붙입니다. 짧은 판(`주문을 찾습니다.`·`주문 정보를 봅니다.`·`주문 금액을 봅니다.`)을 목록 `short_tools`에 담은 뒤, **같은 함수 이름으로 자세한 판을 다시 정의**합니다(이름에 새 도구가 담겨도 목록에 담은 도구는 남음 — 노트북 4절이 한 문장으로 풂). 4절 출력 `이름 같음: True`·`입력 형식 같음: True`(세 도구)로 설명만 다름을 보이고, `두 결과가 같은가: True`(O103, `assert`)로 설명이 부른 결과를 바꾸지 않음을 보였습니다. 몸통 줄이 두 판에서 같은지는 AST로 대조(독스트링 뺀 함수 정의 AST 세 쌍 모두 `True`).
- **짧은 판 목록 도구는 01절 3절 셀과 독스트링만 다름**(독스트링 뺀 AST `author_01.DEF_TOOL` = `author_03.SHORT_LIST` `True`) — 노트북에는 「함수 이름과 몸통 줄은 01절 도구와 같고, 독스트링만 … 짧습니다」로만 적음(「글자까지 같다」는 쓰지 않음).
- **이 절에서 정한 기준 넷**(코드 `check_tool`): 이름을 밑줄로 나눈 첫 낱말이 동사 표(`list`·`get`·`find`·`search`·`sum`·`count`)에 있는가 / 입력 형식의 첫 인자 이름이 설명에 있는가(이 절 도구는 인자가 하나씩이라 첫 키만 — 노트북에 밝힘) / 설명에 「때 씁니다」(언제 쓰는지) / 「내놓습니다」(내놓는 값). 낱말 표·동사 표는 이 절이 정했다고 본문·노트북·b7에 밝힘. 「하는 일이 뚜렷한지」·「사용 조건이 맞는지」는 코드로 세지 않고 사람이 읽는다고 적음.
- **근거(공식 안내, 2026-09-24 WebFetch로 확인)**:
  - OpenAI Function calling `https://developers.openai.com/api/docs/guides/function-calling` — 「Explicitly describe the purpose of the function and each parameter (and its format), and what the output represents.」 · 「Use the system prompt to describe when (and when not) to use each function.」 · 「Aim for fewer than 20 functions …」 → **언제 쓰는지는 시스템 메시지 쪽**이라 본문 b4·b7에 문서마다 자리가 다르다고 밝힘.
  - Anthropic Define tools `https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools`(옛 `docs.anthropic.com/…/implement-tool-use`에서 옮겨 감) — 「Provide extremely detailed descriptions … What the tool does · When it should be used (and when it shouldn't) · What each parameter means … · Any important caveats or limitations」 · 「Aim for at least 3–4 sentences per tool description」.
  - LangChain Tools `https://docs.langchain.com/oss/python/langchain/tools` — 「By default, the function's docstring becomes the tool's description that helps the model understand when to use it.」 · 「Prefer `snake_case` for tool names」 · 「The docstring should be informative and concise」.
  - 「동사로 시작하는 이름」은 세 문서 어디에도 그대로 없고 **이 절이 정한 기준**(LangChain은 밑줄 이름만 권함)이라 b4 표 「근거」 칸에 「이 절이 정함」으로 적음.
- **단정 금지(§3)**: 「기준을 채우면 모델이 잘 고른다」는 노트북 5절 끝·b2·b4 비유·b6·b7·b8·복습 3에서 모두 **04절에서 확인할 물음**으로 넘김.
- **명세 글자 수**(`spec_length` — `convert_to_openai_tool` → `json.dumps(…, ensure_ascii=False)` → `len`을 도구마다 더함): 짧은 판 599 · 자세한 판 923 · 늘어난 324(이름·입력 형식이 같으니 모두 설명에서 옴) · 도구 1·2·3개 309·610·923. 글자 수 ≠ 토큰 수, 요청에 실리는 모양과 띄어쓰기 등이 다를 수 있어 요청 크기로 읽지 않는다고 결과 읽기·b4·b7·복습 4에 밝힘. `tiktoken`은 쓰지 않음(인코딩 파일 내려받기 확인 안 함).
- **값 바꿔 보기(7절) = 이름 하나만 바꿈**(4절과 반대 방향): 설명·몸통은 자세한 판 한 건 도구와 같게(독스트링 문자열 같음 `True`) 이름만 `order_info` → `채운 기준 수: 3`·`'이름이 동사로 시작': False`·`설명이 자세한 판과 같은가: True`. 이름 기준과 설명 기준이 서로 다른 칸을 본다는 것을 보임. 04절이 「이름을 가려 설명만 보게」 할 때 이 방향을 이어 쓸 수 있음(인계).
- **독스트링 한 줄**: 여러 줄 독스트링은 Python 3.12.13 + langchain-core 1.6.2에서 `description`에 `'\n    '`(둘째 줄부터 앞 빈칸)이 그대로 들어가 명세에도 실림 — 노트북 밖 `/tmp/ch19-03/probe.py`로 확인, 노트북 4절 결과 읽기·b4·b7에 「노트북 밖에서 확인, 노트북에서는 실행하지 않음」.
- **몸통 함수 둘(§2-7 3항 — 처음 가르치는 절)**: `find_order(csv_path, order_id)`(`for` + `if` + `break`, 없으면 `None` — 옛 `{"error": …}` 딕셔너리 대신) · `sum_orders(csv_path, status)`(`total = total + row["amount"]`, Ch 17 `count = count + 1` 선례). 노트북 2절에 정의·호출(`O103`·`O999: None`·`{'status': 'paid', 'count': 2, 'total': 59000}`), 같은 본문을 도구 파일에 옮김. 이 노트북은 두 함수를 가져오지 않음(`from order_tools import fetch_orders`만).
- **도구 이름**: `list_orders_by_status`(01 이름 유지) · `get_order_by_id`(옛 이름 유지) · **`sum_amounts_by_status`**(옛 `summarize_order_amounts`에서 바꿈 — 세 이름을 「동사_대상_by_인자」 모양으로 맞춤, 몸통 `sum_orders`와 동사가 같음). 옛 이름은 Ch 19 안(옛 04·05)에서만 쓰였음(`grep` — 다른 챕터 0건).
- **처음 쓴 문법·API(각각 한 문장)**: `json.dumps(…, ensure_ascii=False)` · 문자열 메서드 `split("_")` · `range(len(목록))`(Part 2 모양)으로 두 목록 짝짓기 · 같은 이름 다시 정의(이름에 새 도구가 담기고 목록의 도구는 남음) · 슬라이싱 `[:count]`(02에서 씀). 01에서 이은 것: `@tool`·독스트링·`.name`·`.description`·`.args`·`.invoke`·`convert_to_openai_tool`·`list(….keys())`.

## 4. 실행값 (새 커널 두 번)

| 실행 | 방법 | 시각(UTC) | `code_sha256` | `outputs_sha256` | 셀별 대조 |
|---|---|---|---|---|---|
| A(교재 출력) | `run_section.sh … 03`(그림 전 — 첨부 단계 `FileNotFoundError`, 실행은 저장) | 01:48:04~08(기록 01:48:07) | `9cfb2f16c41e…` | `d96e6d3d3bc8…` | — |
| B | 사본 `/tmp/ch19-03/B.ipynb`, 같은 가상환경 새 커널(인계의 둘째 새 커널 명령) | 01:48:15~18 | `9cfb2f16c41e…` | `d96e6d3d3bc8…` | A와 **27/27 같음**(해시까지 같음) |

- 그림은 A·B 대조 뒤 처음 렌더했습니다. 모델이 없어 흔들린 값이 없습니다. 그 뒤 생성기에서 바꾼 것은 `_src`만 쓰는 상수(그림 alt·삽화 상수)라 노트북은 다시 쓰지 않았고(생성기 `cells()`와 저장 노트북의 셀 57개 소스 대조 `True`), `--no-exec`로 그림만 첨부했습니다. 교재 노트북은 A 실행 그대로(`verification.executed_at` 01:48:07).
- 셀 실행 기록(첫 셀 입력 → 마지막 셀 응답) A 1.8초 · B 1.6초 → 준비물 「3초 안에」. 커널 시작 시간은 들어 있지 않습니다. 본문은 「걸린 시간은 재지 않았습니다」(b7).
- 노트북 파일 해시 `bb18458d6de3…`(수정 전 — `before-manifest.json` 값) → **`dae5411e50da4068d85984294f01ea1463e17f045e97f8ff0ab54ae22bd9157a`**. Part 6 `final-artifact-hashes.json` 355행(`7dcb5963…`)은 이미 낡은 값이었고 이번에도 고치지 않음(마감 몫). 빌드 HTML `03-좋은-도구-이름과-설명.html` `e5f3820b0da4…` → `abbc99a9e6fd…`.

## 5. 그림

- Mermaid 4장: `03-1-같은-몸통에-두-가지-설명`(b4·노트북 「오늘 볼 그림」) · `03-2-기준-넷으로-도구-하나-보기`(b5) · `03-3-짧은-판과-자세한-판`(b6) · `03-4-이름만-바꾸면`(b6 값 바꿔 보기). 원본 viewBox 폭 **484 · 670 · 554 · 629**(모두 868 이하). **보라 0장**(모델 없음), **빨강 0장**(experiment·받은 오류 없음). 몸통 함수·설명 글·이름·`check_tool` 파랑, 기준 표 초록, 출력 값 노랑, `@tool` 도구·두 칸 공통 회색. `03-3` 첫 렌더의 공통 상자 「O103 부른 결과 같음」이 도구 셋 전체의 값처럼 읽혀 「한 건 도구로 O103 · 부른 결과 같음」으로 고쳐 다시 렌더(규격 §5-3 결과 상자 값 범위). 설계표 `03-figures.md`.
- 삽화 `03-5-흐린-카드와-뚜렷한-카드`: **1차 job `42cda76f-0a0f-4afb-a6b1-d2b7b3da0cf1` 채택**(재생성 없음). 생성 전 잔액 **2561.25**, 거래 기록 **2026-09-24T01:49:58Z 「Nano Banana Pro −2」**(결과 파일 이름 `hf_20260924_014958_42cda76f…`와 같은 시각) = **이 절 몫 2크레딧**. 채택 원본 `e0d3d3fa…`(2752 × 1536) → 저장 `15abfc9a…`(1100 × 614). 결과 URL을 다시 받아 같은 폭으로 줄여 픽셀 대조 차이 0(bbox `None`). 저장 PNG 사본(`.cache/ch19-03-view/saved-03-5.png`)을 열어 그림 읽기를 썼고, 오른쪽 카드 셋은 원본을 잘라 확대해 확인(작은 그릇 네 개·국수 큰 그릇 하나·금화 더미). 02의 덧문·주황 별·빈 접시는 쓰지 않음.

## 6. 도구 파일 · 묶음 목록

- `labs/part5/ch19-model-tools/notebooks/order_tools.py`: 해시 **`ade40a313e396d3ef1de3e3bf264e68be155025f42c47803db8106e9d9c99e5e` → `a7106e48ce75fa885d799abbd3df53bd0d83f4122618b35a7c0dc18d05a9c593`**, 코드 줄 6 → 19. 더한 함수 둘(`# Ch 19 03절에서 배웠습니다`): `find_order(csv_path, order_id)`(본문 6줄) · `sum_orders(csv_path, status)`(본문 5줄). 노트북 2절 정의와 **함수 AST 같음**(`ast.dump` 비교 두 개 `True` — 첫 줄 주석은 도구 파일 쪽이 설명 두 줄로 다름). import 그대로(`pandas`뿐), 노트북 전역 이름에 기대지 않고 CSV 파일 위치를 인자로 받음(§2-7 4항). `@tool` 감싸기·도구 객체는 파일에 없음(B안). 옛 판 사본 `/tmp/ch19-03/order_tools.before.py`.
- 묶음 목록(`textbook/part5/public-files.json`·챕터 `qa/public-files.json`)은 이미 도구 파일을 담고 있어 바꾸지 않음. **Part 6 선행 목록(Ch 28 `qa/prerequisite-files.json`·`textbook/part6/prerequisite-files.json`)에 도구 파일을 더할지는 마감 몫**(챕터 리드 결정 2) — 03 노트북이 이제 도구 파일을 가져오므로, `part6-practice.zip` 안의 03 노트북은 도구 파일 없이는 가져오기 셀에서 멈춤(지금도 `data/orders.csv`가 없어 실행되지 않는 읽기용 파일이었음).

## 7. 용어·금지어 확인

| 말 | 03절의 뜻 | 코드에서 |
|---|---|---|
| 몸통 함수 | 도구로 감싸기 전에 실제 일을 하는 평범한 함수 | `find_order`·`sum_orders` |
| 동사로 시작하는 이름 | 하는 일을 뜻하는 동사를 앞에, 대상을 뒤에 밑줄로 이어 붙인 도구 이름 | `get_order_by_id` |
| 사용 조건 | 그 도구를 언제 쓰는지 적은 설명 문장 | 「… 있을 때 씁니다」 |
| 설명 기준 | 도구 이름과 설명을 코드로 확인하려고 이 절에서 정한 네 가지 물음 | `check_tool` |
| 명세 글자 수 | 도구 명세를 JSON 글로 바꿔 센 글자 수, 토큰 수와 다름 | `spec_length` |
| (새 말 아님) 짧은 판·자세한 판 · 채운 기준 수 · 동사 표·낱말 표(기준 표) | 실험의 두 조건 이름 · `count_met` 값 · `verbs`·`check_words` | |

- meta 「새 용어 5」 = 위 다섯.
- 금지어 `grep`(노트북 설명·코드·출력·`_src`·도구 파일·그림 `.mmd`·`.caption.md`·`.prompt.md`): 분기·경로·반환·임계값·재정렬·쿼리·인덱스·융합·RRF·조각·노드·한 겹·돌려·프롬프트·폴백·레코드·캐시·병렬·검증·범주·사전·거부·측정·집합·정규화·추정·필드·인터페이스·인라인·장식·로직·포장·직렬화·식별자·문맥·동시·강사 시연·개선 전·쉽게·간단히·당연히·함정·재 보·회수·로그·스키마·지연·최대 — **걸린 것은 셋뿐이고 모두 본문 밖 이름**: 「반환」·「스키마」는 02절 링크 주소(파일 이름 `02-Pydantic-인자와-반환-스키마.html`) 한 곳, 「프롬프트」는 `.prompt.md`의 소제목(도구 파일 양식, 01·02와 같음). 「로그」는 0건(「프로그램」도 없음).

## 8. 보호 파일 · 챕터 밖 수정

- 보호 파일: `before-manifest.json` 39개 다시 셈 → **37개 같음, 2개 바뀜**(둘 다 준비 조사가 「③ Part 6 선행 목록의 Ch 19 노트북 셋(기준선 — 이 챕터가 바꿀 파일) + Ch 28 목록이 함께 적은 HTML 셋」으로 적은, 이 절이 바꾸게 되어 있는 파일): `labs/part5/ch19-model-tools/notebooks/03-좋은-도구-이름과-설명.ipynb` `bb18458d…` → `dae5411e…` · `textbook/part5/ch19-model-tools/03-좋은-도구-이름과-설명.html` `e5f3820b…` → `abbc99a9…`. 그 밖(orders.csv 둘·Ch 4 파일·완료 챕터 `_src`·Ch 28 `_src`·Part 6 목록·zip 둘·검사 스크립트)은 모두 그대로.
- 챕터 밖 수정: 실습 폴더 `notebooks/03-좋은-도구-이름과-설명.ipynb`(위)·`notebooks/order_tools.py`(§6) · `textbook/_notebook/checks/notebook-contracts-part5-ch19-model-tools.json`(`verify.py --chapter`가 다시 씀). 공용 도구·규격·과정 요약·계약 파일·Part 6 파일·완료 챕터 파일·Ch 28 파일·묶음 목록은 고치지 않음.

## 9. Ch 28이 이 절에 기대는 문장 (고치지 않고 참·거짓만 기록)

| 자리 | 문장 | 03절 끝 기준 판정 |
|---|---|---|
| Ch 28 01 b2 | 「Ch19에서는 Python 함수를 모델이 읽을 도구 스키마로 바꾸었습니다」 | **참**(01~03 모두 `@tool` → 도구 명세) |
| **Ch 28 01 b3** | 「Ch19에서 도구 이름·설명·입력 스키마가 모델 선택에 영향을 준다는 사실을 확인했습니다」 | **03으로는 거짓** — 03은 모델을 부르지 않아 선택을 보지 않았고, 03 b2·b6·b7·b8에 「04절에서 확인할 물음」으로 적음. 참·거짓은 **04절 결과에 달림**(옛 04는 9/9·9/9로 차이를 관찰하지 못함) |
| **Ch 28 05 b2** | 「Ch19에서 도구 개수가 늘면 선택 정보가 커진다는 사실을 배웠습니다」 | **글자 수로는 참, 토큰으로는 03에서 보지 않음** — 03 6절 `도구 수: 1 \| 명세 글자 수: 309` → 2개 `610` → 3개 `923`. 03 본문은 「토큰은 세지 않았다」로 적음. 「선택 정보」를 명세 글자 수로 읽으면 참 |
| Ch 28 05 b3 | 「Ch19에서 `bind_tools`가 도구 설명을 모델 요청에 포함시키고 `usage_metadata`가 입력·출력 토큰을 제공한다는 사실을 확인」 | 03 해당 없음(04·05 몫). 03은 `bind_tools`를 쓰지 않음 |
| Ch 28 04 b3 | 「Ch19에서 `@tool`로 만든 BaseTool의 name, description, args_schema를 모델에 연결했습니다」 | 03은 이름·설명·입력 형식을 출력만 하고 모델에 연결하지 않음(04·05 몫) |

## 10. 강사 확인 대상

1. **같은 함수 이름으로 도구를 다시 정의하는 설계**(짧은 판 → 목록에 담기 → 자세한 판). 설명 하나만 바꾼 비교를 코드로 보이려는 선택이고, 셀을 순서대로 실행해야 한다는 것을 b7에 적음. 학생이 셀 차례를 바꿔 실행하면 목록 둘에 같은 판이 담길 수 있음.
2. **기준 넷은 이 절이 정한 것**(동사 표 여섯·낱말 「때 씁니다」·「내놓습니다」). 특히 「이름이 동사로 시작」은 공식 문서에 그대로 없는 기준이고, 낱말 검사는 교재 문체(「씁니다」·「내놓습니다」)에 맞춘 것이라 다른 문체의 설명에는 맞지 않음(본문에 「낱말이 있는지만 본다」로 밝힘).
3. **도구 이름 `summarize_order_amounts` → `sum_amounts_by_status`**(04·05가 이어 씀).
4. OpenAI 문서는 언제 쓰는지를 시스템 메시지에 적으라 하고 Anthropic 문서는 설명에 적으라 함 — 이 절은 설명에 적고 b4·b7에 두 자리를 함께 밝힘.
5. 코드 줄 증가 44 → 130(코드 셀 20~30 기준, 01·02와 같은 사정). 도구 파일 코드 줄 6 → 19.
6. 삽화 `03-5` 오른쪽 셋째 카드의 금화 더미를 「합계」로 읽는 비유(돈 합계 → 금화)가 자연스러운지.

## 11. 남은 것 · 지우지 않은 것

- **지워야 하지만 지우지 않은 것**: 기기 `/tmp/ch19-03/`(`probe.py`·`cells.py`·`runcells.py`·`cmp.py`·`shrink.py`·`crop.py`·`cmpimg.py`·A·B 사본 노트북·생성 원본 `illu-1-orig.png`(2752px)·`illu-1-again.png`·축소본·확대본·도구 파일 옛 판 사본 `order_tools.before.py`) · `.cache/ch19-03-view/`(그림 확인 사본 여덟 장 — Mermaid 넷·`03-3` 다시 렌더 하나·삽화 축소본·확대본·저장 사본) · `qa/upgrade/gates-wip-03-03.json`(첫 실행 전 G1·G2·G6 확인 — `gates-wip-03.json`으로 갈음) · `qa/upgrade/__pycache__/`(확인 스크립트가 생성기를 import하며 생길 수 있음).
- 옛 그림 `figures/03-좋은-도구-이름과-설명-flow.*` 셋은 그대로 둠(본문 참조 0 — 마감 삭제 승인 목록).
- 마감 몫: `part5-practice.zip`·`part6-practice.zip` 다시 만들기, Part 6 선행 목록에 도구 파일을 더할지(§6), `final-artifact-hashes.json` 355행, 실습 폴더 README(「노트북은 서로 독립적」 — 03도 도구 파일을 가져옴), `chapter.json` `objectives`(03 해당 문장 없음).

## 마감 반영 (2026-09-24)

검토 1차(`review-round1-A.md`·`review-round1-B.md`)를 반영했습니다. **노트북은 다시 실행하지 않았습니다**(`code_sha256`·`outputs_sha256`·`executed_at` 그대로, 마크다운만 — `mdpatch.py`로 생성기·노트북·`_src`를 같이 고친 뒤 `run_section.sh … --no-exec`). 전체 기록은 `chapter-summary.md` §15.

- **A-5(코드 그대로)**: b6에 「자세한 판 설명은 이 절의 낱말 표와 인자 이름에 맞춰 쓴, 흐름을 보여 주려고 정한 예 → 채운 기준 수 1과 4는 실행 전에 정해진 값 · 이 표로 볼 것은 짧은 판이 어느 기준을 놓쳤는가 · 코드로 새로 알게 된 값은 명세 글자 수 599·923과 309·610·923」 단락, 표 세 줄 → 「도구 셋 각각(목록·한 건·합계)」 한 줄, b7 한 항목, 노트북 5절 끝 셋째 줄 뒤 단락, b8·노트북 정리 둘째 줄 「짧은 판은 이름 기준 하나만 · 그 기준에 맞춰 쓴 자세한 판은 넷」, 복습 3 해설, 그림 `03-3` 캡션(`.caption.md`도). `.mmd` 라벨은 출력 값 그대로라 다시 렌더하지 않음.
- **A-6**: b2 「권고를 모으면 넷」 → 「세 회사 문서는 하는 일·언제 쓰는지·인자의 뜻·내놓는 값·한계 들을 권함 → 그 권고를 바탕으로 기준 넷을 정함」. b4 「비교와 경계」 뒤 단락: Anthropic 문서의 서비스 이름 앞붙이기(`github_list_prs`) — 이 절 이름 기준을 채우지 못함, 도구가 한 곳에 모인 이 챕터에서만 쓰는 기준.
- **A-7**: b4 비유 첫 문장 → 「이번에는 카드가 걸린 자리를 도구 이름, 카드의 그림을 도구 설명으로 봅니다」.
- **A-8**: 복습 1·3 해설의 「이 절 2절」·「b7」 → 「본문 2 「이 내용을 배우는 이유」」·「본문 7 「주의할 점과 실무 메모」」.
- **자리 찾기 셀 결과 읽기(A-11·B-14)**: 「교재 출력은 실행 도구에 도구 파일 폴더를 따로 알려 준 실행이라 `.`이 찍혔습니다」와 「셀 안의 안내 글은 실습 폴더 맨 위도 적었지만, 도구 파일을 가져오려면 `notebooks/` 폴더에서 열어야 합니다」를 더함. 셀 안 `assert` 안내 글(「notebooks 폴더나 실습 폴더 맨 위에서」)과 생성기의 같은 코드는 그대로 — **다음 재실행 때 「notebooks 폴더에서」로**.
- 노트북 파일 `dae5411e…` → `f0d83063…`(Part 6 선행 목록·`final-artifact-hashes.json` 줄도 새 값). 게이트 0(검사 문장 366).
