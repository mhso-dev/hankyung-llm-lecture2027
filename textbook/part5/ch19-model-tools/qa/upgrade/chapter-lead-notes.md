# Ch 19 모델과 도구 — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part5/ch19-model-tools`(절 여섯 — 01·02·06 paired, 03·04·05 experiment) · `labs/part5/ch19-model-tools`. Part 5의 셋째 챕터이고 **Ch 18 바로 뒤**입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본) · `gates-before.json` · `before-manifest.json` · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch19-model-tools`.
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(§2·§2-7·§3·§5-3·§5-4·§6·§7-2·§8) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · `qa/upgrade-course-summary.md`(§1·§2 전부·§3·§5·§6·§9) · `qa/upgrade-contracts.md`(§1 Ch4 줄·§3 Ch17/Ch18 줄·§4·§5·§8) · Ch 18 `chapter-summary.md`(§13·「마감 뒤 보완」) · Ch 18 `chapter-lead-notes.md`·`before-manifest.json` · Ch 4 `chapter-summary.md` §4·§5 · Ch 6·7·17 요약의 해당 줄 · Ch 4 `data_tools.py`·01·06 노트북 · Ch 28 `_src`·`qa/prerequisite-files.json` · Part 5·6 묶음·검사 스크립트.
- **원고·노트북·그림은 하나도 고치지 않았습니다.** 파일 삭제 0건. 모델 호출 0건. 노트북 실행 0건. 모델을 부르지 않는 확인만 했습니다(§6 도구 스키마 시험 · `test_verify.py`의 Ch 18/19 두 시험 통과 · Ch 4 `fetch_orders`와 AST 대조 · 스키마 없는 도구에 `shipped` 넣기).
- `chapter.json` `hours` = 「총 16h · 강의 6h · 실습 10h」. 절 meta 합 강의 1×6 = **6h**, 실습 2+2+1+2+2+1 = **10h** → 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part5/_build_index.py`(6, 10)·`qa/check_scope.py` `EXPECTED`(6, 10)도 같습니다. 새 용어 meta 5×6 = 30.

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-24)

| 절 | 형식 | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 tool과 Ch 4 함수 재사용 | paired | 6 | 92 | 1 | 1 | 0 | 0 | 6 | 20 | 3 | 31 |
| 02 Pydantic 인자와 반환 스키마 | paired | 6 | 88 | 1 | 0 | 0 | 0 | 7 | 16 | 3 | 27 |
| 03 좋은 도구 이름과 설명 | experiment | 6 | 101 | 4 | 3 | 0 | 0 | 5 | 14 | 3 | 29 |
| 04 설명만으로 도구 선택하기 | experiment | 10 | 98 | 11 | 7 | 0 | 0 | 8 | 11 | 3 | 40 |
| 05 bind_tools와 병렬 호출 | experiment | 9 | 100 | 8 | 3 | 0 | 0 | 8 | 16 | 3 | 38 |
| 06 오류와 읽기 쓰기 분리 | paired | 6 | 90 | 5 | 3 | 0 | 0 | 6 | 8 | 3 | 25 |
| **합계** | | **43** | **569** | **30** | **17** | **0** | **0** | **40** | **85** | **18** | **190** |

- 통과 절 **0/6**. 코드 줄(`count_code.py`) 38·55·44·92·65·52 = **346줄**. **여러 노트북에 글자까지 같은 셀 다섯 벌이 185줄(53%)**: 준비 셀(`find_up`) 13줄 × 6 · `fetch_orders` 셀 9줄 × 5(01~05) · `list_orders_by_status` 도구 5줄 × 4(01·03·04·05) · `get_order_by_id`+`summarize_order_amounts` 10줄 × 3(03·04·05) · 모델 셀 6줄 × 2(04·05).
- G1 30 = 제너레이터 식 13 · 리스트 내포식 7 · 한 셀에 함수 둘 이상 4 · 집합 내포식 3 · 조건 표현식 3.
- G2 17 = 한 글자 이름 16(`r` 12 · `t` 2 · `n` · `u`) · 두 겹 호출 1(03 `len(json.dumps(…))`). 15줄 넘는 셀·세미콜론 0.
- G3 0 — 첫 줄 주석은 셀마다 구체적입니다. 2~3줄마다 이유 주석(§2-5)은 거의 없습니다.
- **G4 0은 착시입니다.** 01·02·03·06은 모델을 부르지 않고, 04·05는 `init_chat_model(MODEL, model_provider="openai", temperature=0)` — **`reasoning_effort="none"`이 없습니다**(G4는 temperature만 봄). 가짜 모델은 없습니다.
- G5 40 = 절마다 `title_cell_missing`·`core_figure_attachment_missing` 12 + 결과 읽기 인용 없음 28(결과 읽기 셀 자체가 0).
- G6 85 = 70자 초과 27 · 영문으로 시작해 조사가 붙은 문장 **48** · 빽빽한 단락 10.
- G7 18 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 금지·미교육 문법 (AST로 따로 셈)

- **타입힌트**: 함수 29개 모두(준비 셀 `find_up(name: str) -> Path | None` 여섯 번 포함), 모양은 `str | Path`·`list[dict[str, Any]]`·`list[dict]`·`dict[str, int]`·`Path | None`. 변수 주석 06 `confirmed_order_ids: set[str] = set()`. 양식 클래스 필드 02 여섯 줄(`Literal[…]`·`int = Field(…)`·`float = Field(ge=0)`). **Ch 13~18은 0건**, Ch 2 07이 가르친 모양은 `매개변수: int/str = 기본값`·`-> int/str`뿐(Ch 2 요약 53행).
- **데코레이터**: `@tool` 13개(01 1·02 1·03 3·04 6·05 3·06 2), 모양 셋 — 맨 `@tool` · `@tool(args_schema=OrderQuery)`(02) · `@tool("list_orders_by_status", description="…")`(04 모호 조건 셋).
- **클래스**: 02 `OrderQuery(BaseModel)`·`OrderRecord(BaseModel)`(필드만, 규격 L5 안). 과정 첫 `BaseModel`은 Ch 6 03(「양식 클래스」 `StudyCard`, 세 문장 + Ch 2 10 링크 완료).
- **독스트링**: 도구 함수 12개 + `fetch_orders` 5번. **과정 교재에 「독스트링·문서 문자열」을 가르친 절이 없습니다**(Part 1~4·Ch 17·18·22 `_src` grep 0건). `@tool`은 독스트링이 없으면 `ValueError`(§6 시험).
- **기본값 매개변수·키워드 전용 `*`**: `fetch_orders(csv_path, *, status=None)`(01~05, Ch 4 01 b7이 「이 절에서는 쓰지 않았습니다」로만 풂) · 02 `search_orders(status, limit=3)`.
- **별표 풀기**: 준비 셀 `(current, *current.parents)`(여섯 노트북) · 05 `[…, ai_message, *tool_messages]`. Ch 18 03이 `gather(*waitings)`로 과정 첫 별표 풀기를 풂.
- **`next(생성기, 기본값)`**: 03·04(둘)·05·06 — 과정 요약 §2-3 금지 목록(「`next(… for … if …)`로 첫 항목 찾기」).
- **`sum(생성기)`**·**`zip`**·**`sorted`**·**`set()`**·**집합 리터럴**: 03·04·05 `sum`, 04 `zip` 둘, 02 `sorted(value[0])`, 05·06 `set()`, 01·05·06 `{'O101', 'O103'}` 모양. 04 이어진 비교 `a == b == c * d`, 요금 `0.75`·`4.5`·`1_000_000`을 식 안에(04·05, 규격 §2-3).
- **try**: 01 `except TypeError` · 02 `except ValidationError`(목록 `for` 안) · 06 `except PermissionError` + **`else: raise AssertionError(…)`** 두 번(try `else`는 과정에서 B 트랙만) · 06 도구 안 `raise PermissionError`(Ch 16 01이 `raise ValueError`를 풂).
- **한 셀에 정의와 호출·함수 여럿**(규격 §2-2): 02 cell7(클래스 + `@tool` 함수 + 출력 둘)·cell9(클래스 + 호출) · 03 cell9(도구 둘) · 04 cell9(도구 셋)·cell13(둘)·cell19(`run_selection` 정의 + 18번 호출 + 출력)·cell21(`grade` 정의 + 호출) · 05 cell11(도구 둘) · 06 cell7(정의 + 호출).
- **메시지 모양**: 05 마지막 요청이 딕셔너리 메시지 `{"role": "user", "content": question}`(과정 관례는 Ch 7 튜플 `("user", …)`·Ch 13 04 `HumanMessage`) · 응답 글을 `.text`로 읽음(과정은 Ch 6부터 `.content`).
- **처음 쓰면 풀어야 하는 이름**: `Path.cwd().resolve()`·`.parents`·`/`·`exists()`(준비 셀) · `pd.read_csv(…, dtype={…})`(Ch 4 요약 §5 「열별 `dtype`」 미교육) · `from typing import Any`·`Literal` · `TypeAdapter`·`validate_python`·`error.errors()`·`item["loc"]`(02) · `StructuredTool`·`.name`·`.description`·`.args`·`.args_schema`(01~04) · `bind_tools(…, parallel_tool_calls=…)`·`tool_calls`·`usage_metadata`·`ToolMessage`·`tool_call_id`(04·05) · `os.getenv`(04·05).

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청(이번 출력) | 손 값 | 금지 문법(셀) | 금지어(`_src` 블록 / 노트북 md) | `assert`(무엇에) |
|---|---|---|---|---|---|---|
| 01 | Ch 4 실습 폴더 판 `fetch_orders(csv_path, *, status=None)`를 노트북에 다시 적음(`data_tools.py`와 AST 같음) → `@tool`로 `list_orders_by_status(status)` — CSV 자리는 숨기고 `status`만 공개. 직접 호출과 `invoke({"status": "cancelled"})`가 같음(`O104`). Before: 도구 객체를 함수처럼 부름 → `TypeError 'StructuredTool' object is not callable`(받아 출력). After: `invoke({"status": "paid"})` → 2건 | **0** | 없음(CSV만) | c3 `find_up`(Path·별표·`Path \| None`·정의+호출) · c5 `str \| Path`·`Any`·키워드 전용 `*`·`dtype` · c13 집합 내포식·`r` | **제목 「tool」** · 반환 b4×3·b6×2·b8×2·b9 / md3 · 돌려주는 b4 · 사전 b4×2·b7 / md2 · 경로 b4×5·b6 / md2 · 검증 b1·b3·b4×2·b7×2 / md4 · 필드 b4·b7 · 인터페이스 b2·b4×2 / md2 · 인라인 b3 · 장식 b4 / md1 · 로직·포장 | 3 — CSV 찾음(준비) · 직접 == 도구 & `O104` · 2건 & ID 집합(모두 CSV에서 정해지는 값) |
| 02 | 양식 클래스 `OrderQuery`(`status` `Literal` 셋 · `limit` `Field(default=3, ge=1, le=10)`) + `@tool(args_schema=OrderQuery)` `search_orders` → `model_json_schema()` 출력 · 반환 쪽 `OrderRecord` + `TypeAdapter(list[OrderRecord])`(금액 `32000` → `32000.0`). Before: `shipped`·`limit 0` → `ValidationError`(`literal_error`·`greater_than_equal`, `loc`) 받아 출력. After: `pending` 1건 → `O102` | **0** | `Literal` 셋·범위 1~10·기본 3 | c7 클래스+도구+출력 한 셀·기본값 `limit: int = 3` · c9 클래스+호출·`TypeAdapter`·`sorted`·리스트 내포식 · c11 목록 `for` 안 `try` | 반환 b2·b4×6·b5×2·b6×2·b7×3·b8 / md6 · 검증 b1·b4×3·b5·b7×5·b8×2 / md4 · **거부** b1·b4·b5·b7·b8·b9×3 · 필드 b4·b5·b6×2·b7×3 · 돌려주는 b4 · 사전 b4·b7 / md2 · 최대 b4 | 3 — CSV · 검사한 행 1개 `O101` · `O102`(결정적) |
| 03 | 목록·한 건·집계 세 도구의 `name`·`description`·`args` 출력 + 설명 글자 수·`args` JSON 글자 수(`46 49` · `33 53` · `26 49`). 「선택 정확도는 다음 절에서」 | **0** | 세 독스트링 | c9 도구 둘 한 셀·`next(생성기, 기본값)`·`sum(생성기)`·`r` · c11 집합 내포식 · c13 두 겹 호출 | 반환 b1·b3·b4×6·b6·b7×2·b8×2·b9×2 / md5 · **측정** b1·b5×2 / md1 · 필드 b4×3·b7 / md3 · 식별자 b4·b6 · 직렬화 b4·b9 · 문맥 b4 · 돌려주는 b4×2 / md1 | 2 — CSV · 이름 셋이 서로 다름 |
| 04 | 모호 조건(세 도구 모두 「주문 정보를 찾습니다.」, `@tool("이름", description=…)`로 이름·`args` 같게) vs 구체 조건(03 독스트링). 질문 3 × 반복 3 × 조건 2, `bind_tools(…, parallel_tool_calls=False)` → **두 조건 모두 9/9**. 입력 3,483·출력 366토큰, 「추정 비용」 0.00425925달러. 요청당 입력 토큰 모호 175·181 / 구체 208·214 | **18**(한 조건 9) | 질문 셋·기대 이름·`REPEATS = 3` | c9 도구 셋 한 셀·`next`·`sum` · c13 도구 둘 · c15 `zip` · c19 정의+18번 호출+출력·`list[dict]` · c21 내포식+조건 표현식+`zip`+`sum(생성기)` 셋·이어진 비교·요금 식 안 | 측정 b1 · 추정 b6 · 집합 b4 / md1 · 로그 b5·b7×2 / md1 · 검증 b7 · 돌려주는 b4 | 6 — CSV · 키 이름 · 이름·`args` 같음 · `usage_metadata` 있음 · 기록 수 = 3×3 · **비용 < 1(잰 값)** |
| 05 | `bind_tools([get_order_by_id], parallel_tool_calls=True)` + 「O101과 O103 주문을 각각 조회해 줘. 각 주문마다 도구를 한 번씩 호출해.」 → 한 응답에 `tool_calls` 둘 → `get_order_by_id.invoke(call)`로 `ToolMessage` 둘(요청 ID = `tool_call_id`) → 마지막 요청에 사용자 글 + AI 메시지 + 도구 메시지 둘 → 답 글. 순차 실행이라고 b2·b6에서 밝힘. **정의만 하고 쓰지 않는 도구 둘**(`list_orders_by_status`·`summarize_order_amounts`) | **2**(입력 163·290 · 출력 55·36, 「추정」 0.00074925) | 질문 글 | c11 도구 둘 한 셀·`next`·`sum` · c13 집합 내포식 · c15·c17 내포식 셋·`set()` · c19 `*tool_messages`·딕셔너리 메시지·`sum(생성기)`·요금 식 안·`u` | **제목 「bind_tools」·「병렬」**(Ch 13·18 금지어) · 병렬 b4×2·b5·b7 / md3 · 동시 b4×2·b7×3·b9 / md3 · 순차 b4×3 / md2 · 로그 b4×3·b5·b6·b7 / md2 · 측정 b7×2 · 추정 b6 · 돌려주는 b4 | 8 — CSV · 키 · **`tool_calls` 2개(모델 답)** · **인자 집합 `O101`·`O103`(모델 답)** · 두 ID 목록 같음 · **답 글 있음·도구 호출 없음(모델 답)** · 사용량 있음 · 비용 < 1 |
| 06 | `ORDERS`(CSV를 `dtype` 없이) → `read_order(order_id)`: 없으면 `{"ok": False, "error": "NOT_FOUND", …}`를 내놓음(`O999`) · `request_order_cancellation(order_id)`: 노트북 전역 `app_user_confirmed`·`confirmed_order_ids`(뒤 셀에서 정의)를 보고 아니면 `raise PermissionError`. Before(확인 전): 도구 목록 `['read_order']`, 직접 `invoke` → `PermissionError` 받아 출력. After: 확인 `{"O101"}` → 취소 요청 결과, `O103` → `PermissionError` | **0** | 확인 상태 `True`/`False`·`{"O101"}` | c7 `next(생성기, None)`·조건 표현식·정의+호출 · c9 전역 이름에 기댐 · c11 `set[str]`·`set()`·내포식·**try `else`**·`raise AssertionError`·줄 끝 주석 · c13 조건 표현식으로 목록 고르기·try `else` | 반환 b2·b3·b4×4·b5×2·b6·b7 / md2 · 애플리케이션 ×10 / md2 · **거부** b5·b6 · 집합 b4×2 / md1 · 모의 b5·b7 · 경로 b2·b7 · 검증 b7 · 돌려주는 b4 | 3 — CSV · 쓰기 도구가 목록에 없음 · 취소 결과 칸(결정적) |

- **모델 요청 합계(노트북 한 번씩, 교재 출력 기준) 0 + 0 + 0 + 18 + 2 + 0 = 20번**, 모두 `gpt-5.4-mini`(LangChain `init_chat_model`), 임베딩 0. 출력한 「추정 비용」 합 0.00425925 + 0.00074925 ≈ **0.005달러**(할인 없는 요금표 어림, 청구 금액 아님). 과정 말은 **「예상 비용」(Ch 6 06 `estimate_cost` = 사용량 × 요금표)**이고 「추정 비용」은 Ch 18 금지어.
- **`temperature=0`** 04·05만(모델을 부르는 절 전부), **`reasoning_effort="none"` 0곳**. 모델 이름은 `"gpt-5.4-mini"` + `model_provider="openai"`(과정 관례 `"openai:gpt-5.4-mini"`). 04·05 준비 출력 `{'model': 'gpt-5.4-mini', 'temperature': 0, '예상_절별_비용_USD_상한': 1.0}`(1.0은 손으로 적은 상한).
- **걸린 시간은 어느 절도 재지 않습니다.** 05 b6이 「실행 시간의 동시성은 측정하지 않았습니다」로 밝힘.
- **`%pip` 셀이 없습니다**(여섯 노트북). Part 5 앞 두 챕터는 `%pip install` 셀을 둠. 실습 폴더 dev에 `pip==26.2`·잠금에 `pip 26.2` 있음.
- **옛 그림 토큰**: 절마다 b4 「도식 읽기」의 `{{svg:NN-…-flow}}` 하나. 노트북 토큰은 01·02·06 `{{notebook:slug|example}}`+`|failure}}`, 03~05 `{{notebook:slug}}`(`chapter.json` 형식과 같음). Mermaid·삽화 0장.
- 노트북 `metadata.verification`: 여섯 모두 `passed`, 실행일 **2026-09-10**(01~05 06:10~06:11 · 06 06:15 UTC). `code_sha256` 앞 12자 01 `768bc0125165` · 02 `27cca56fb8d7` · 03 `37ebb48e1543` · 04 `c7ba2c70b0d5` · 05 `8204a4fd0a14` · 06 `0c1edd68c16f`. 노트북 파일 해시 03 `bb18458d…` · 05 `899919f7…` · 06 `3f5d44c2…`(§4-1).
- 노트북 설명 셀: 제목 한 줄 · 「준비」 · 「코드를 읽기 전에」(`_src` b4와 같은 글, `revision: 2026-09-14-first-use-depth`) · 「다음 셀을 읽는 방법」(`2026-09-14-direct-cell-reading`) · 소제목 · 「다른 상황에 적용하기」. **결과 읽기 셀 0.**
- `_src` 틀 문장(여섯 절 같음): b2 끝 「Ch 20에서 `ToolNode`로 … 확인합니다」 · b3 끝 「실행 파일은 … Part 1 모듈을 런타임에 import하지 않습니다」 · b4 비유 「도구 설명서는 주문서와 비슷합니다」(Ch 2 06·13 「주문서」 삽화와 겹침) · b4 「도구 메시지(ToolMessage)는 실행 결과와 호출 ID를 **돌려주는** 메시지」 · b5 「모델 호출이 있는 절은 `gpt-5.4-mini`, `temperature=0`」 · b7 목록 둘 · b10 참고 자료 다섯(확인일 2026-09-10). 복습 문제 절마다 넷(문제 3 「이 절에서 확인한 실제 출력은 무엇인가요?」 틀).

## 2. 절별로 더 봐야 할 것

### 01 tool과 Ch 4 함수 재사용 (paired)
- **`fetch_orders` 판**: 노트북 판은 Ch 4 **실습 폴더 `data_tools.py`** 판과 AST가 같습니다(이번 확인 — 01~05 다섯 셀 모두 `True`). Ch 4 **01 노트북이 가르친 판**은 `fetch_orders(file_name: str, status: str) -> list`(열 셋짜리 CSV를 임시 폴더에 만들어 읽음)라 모양이 다릅니다. **완료 챕터 Ch 4가 약속을 네 곳에 적었습니다** — `_src/01` b7 「Ch 19 01절이 도구로 다시 쓰는 것은 이 실습 폴더 판입니다」 · `_src/03` b7 · `_src/06` b8 「Ch 19 01절은 실습 폴더 `data_tools.py`의 `fetch_orders(csv_path, *, status=None)`를 모델이 고를 수 있는 도구로 다시 씁니다. 01절 함수와 하는 일은 같고, 상태를 키워드 인자 `status=`로 받는 모양입니다」 · 06 노트북 셀 8(같은 문장). 계약 파일 §1 「Ch19 01이 이 판을 씀 → 01절 모양과 차이를 잇거나 맞출지 결정」.
- `data_tools.py`를 **직접 가져올 수는 없습니다**: 파일 맨 위에서 `httpx`·`bs4`·`sqlite3`를 import하고, Ch 19 잠금에 `beautifulsoup4`가 없습니다. 폴더도 Part 1입니다(`labs/part1/…`). 그래서 지금처럼 복사하거나 Ch 19 도구 파일에 옮겨야 합니다.
- `dtype={"order_id": "string", "customer_id": "string"}`는 이 자료에서 결과를 바꾸지 않습니다(pandas 3.0.5에서 `dtype` 없이 읽어도 네 칸이 `str`·`str`·`str`·`int`, 이번 확인). Ch 4 요약 §5가 「열별 `dtype`」을 미교육으로 둠.
- **실행하지 않은 사실을 적음**: b3 「원본 함수와 AST가 같은지 검증 기록에서 확인할 수 있습니다」·b7 「원본 해시는 출처 추적용 …」 — 노트북에 해시·AST 비교가 없습니다. `labs/part5/continuity-guide.md` 7행 「첫 번째 노트북에는 Ch 4의 `fetch_orders()` 본문과 **원본 SHA-256이 함께 적혀 있습니다**」도 사실과 다릅니다(노트북의 `sha256` 두 곳은 `metadata.verification` 값).
- **b6 「일부러 실패해 보기」가 실패 장면(`TypeError`)이 아니라 `cancelled` 비교를 설명합니다**(블록 내용과 `{{notebook:…|failure}}`가 어긋남).
- Before `TypeError`는 **실제로 일어나는 결함**(도구 객체를 위치 인자로 부름)이라 paired Before로 맞습니다. 모델 요청은 없습니다 → **§4-2 오프라인 계약**.
- 처음 나오는 것이 몰려 있습니다: 데코레이터 `@tool`(A 트랙은 Ch 2 09를 건너뜀 → 세 문장 + 링크, 규격 §2-2) · 독스트링(과정 첫) · `StructuredTool` · `invoke(딕셔너리)` · 이름·설명·입력 형식(`args`). 「이 줄은 아래 함수를 도구로 등록합니다」(규격 L6 문장).

### 02 Pydantic 인자와 반환 스키마 (paired)
- **Ch 6 03이 먼저 가르쳤습니다**: 양식 클래스 `StudyCard`·`Field(description=, ge=1, le=3)`·범위 밖 `ValidationError`·`model_json_schema()`·`model_dump()`. 02는 「Ch 6 03절 양식 클래스처럼」으로 이으면 됩니다(세 문장 반복 불필요, Ch 6 요약 64행). Ch 2 10 b2·b8이 「Ch 19의 도구 입력 규칙에서 `BaseModel`과 `Field()`를 다시 만납니다」로 약속.
- **Before가 결함 코드가 아닙니다.** Before는 스키마가 잘못된 입력을 막는 장면(= 스키마가 일하는 모습)이고, After는 입력만 고친 것입니다. 실제 결함은 **스키마 없는 도구가 `shipped`에 오류 없이 빈 목록 `[]`을 내놓는 것**입니다(이번 확인 — 01의 `list_orders_by_status.invoke({"status": "shipped"})` → `[]`). Ch 4 03 「오류 없이 틀린 결과」 습관과 이어집니다.
- `TypeAdapter(list[OrderRecord])`는 새 API이고 제네릭 표기 `list[…]`가 들어갑니다. `OrderRecord.amount: float`이 금액 `32000`을 `32000.0`으로 바꿉니다(Ch 4 01 자료형 확인 습관과 부딪힘 — 출력에 보임).
- 「반환 스키마」가 모델에게 전달되지는 않습니다(`@tool`의 반환 힌트는 입력 형식에 안 들어감 — §6 시험). 반환 검사는 코드 쪽 검사입니다.

### 03 좋은 도구 이름과 설명 (experiment)
- **experiment인데 실험이 없습니다**: 설명서를 출력하고 글자 수만 셉니다. 「값 바꿔 보기」·예상·비교가 없고 b6 「실험 결과 해석」은 「선택 정확도는 다음 절에서 실제로 측정합니다」 한 줄(노트북).
- 글자 수 `46 49`·`33 53`·`26 49`는 모델 입력 토큰과 다릅니다(b4가 밝힘). 04 출력에 **실제 입력 토큰 차이**가 있습니다 — 같은 질문에서 모호 175 · 구체 208(`+33`). 도구 설명이 입력 토큰을 쓴다는 것을 잰 값으로 보이려면 03이 `bind_tools` 한 번을 부르거나 04의 값을 인용해야 합니다(Ch 28 05 b2·b3이 이 사실에 기댐 — §4-3).
- 세 도구 정의는 03이 처음이고 04·05가 글자까지 같게 다시 적습니다(§5).

### 04 설명만으로 도구 선택하기 (experiment)
- **핵심 관찰이 이 설계로는 나오지 않습니다.** 모호 조건도 공개 이름이 `list_orders_by_status`·`get_order_by_id`·`summarize_order_amounts`라 **이름만으로 역할이 드러납니다.** 두 조건 모두 9/9이고, 요청마다 고른 도구·인자가 18번 모두 기대와 같았습니다(출력 대조). 「설명만으로」 가르려면 공개 이름을 역할이 안 드러나는 이름(예: `tool_a`)으로 두는 등 **같은 학습 목표 안에서 입력을 고치는 결정**이 필요합니다(규격 §2-7 10번 — 먼저 노트북 밖 다섯 번, 탐색으로 고른 입력은 b7에 「흐름을 보여 주려고 정한 예」).
- 그렇게 고치면 모호 조건의 선택이 **실행마다 흔들릴 것**이 예상됩니다(그것이 이 절이 보여 줄 장면). 결론에는 두 번 같은 값만, 흔들린 값은 결과 읽기 둘째 단락·표·「확인할 점」에만(규격 §2-7 9번 끝).
- **`bind_tools`를 처음 쓰는 절이 04입니다.** 완료 챕터 두 곳이 「`bind_tools`는 Ch 19 05절」로 약속했습니다 — Ch 7 05 b4 「도구를 모델에 알려 주고 호출 요청을 받는 방법은 Ch 19 05절에서 다룹니다」 · Ch 17 03 b4 「모델 요청에 도구를 함께 싣는 방법(`bind_tools`)은 Ch 19 05절에서 다룹니다」. 04에서 `bind_tools`를 한두 문장으로 먼저 풀고 05에서 자세히 다룰지, 순서를 바꿀지 정해야 합니다.
- 반복 3번은 노트북 안에서 **미리 정한 반복**(값 고르기 아님)입니다. `REPEATS = 3` · `calls_per_condition: 9`는 손으로 적은 `9`(계산 아님).
- 「수동 채점」 `grade`는 첫 도구 호출 이름만 봅니다(`parallel_tool_calls=False`). 인자가 맞는지는 채점하지 않습니다.
- Ch 8 04 b8(완료)·Ch 8 목차 「혼란 조건 → Ch 19 04절에서 도구 설명만으로 도구를 고르는 실험」, Ch 17 03(모델이 도구 이름을 **JSON 글**로 적고 코드가 `json.loads`로 읽음)과 이어 쓸 수 있습니다 — 이 절은 같은 일을 **도구 호출 목록(`tool_calls`)**으로 받습니다. Ch 18 02 「라우팅」(모델이 종류 이름을 쓰고 코드가 갈래를 고름)은 **도구 선택과 다릅니다**(Ch 18 요약 §13).

### 05 bind_tools와 병렬 호출 (experiment)
- 핵심 관찰(한 응답에 호출 둘)이 모델 답에 달렸고 **`assert` 셋이 모델 답에 걸려 있습니다**(개수 2 · 인자 집합 · 답 글 있음·도구 호출 없음). 질문 글이 「각 주문마다 도구를 한 번씩 호출해」로 호출 수를 사실상 정합니다(Ch 18 04 B-1과 같은 모양 — 밝혀 둘 것). 모델이 한 번에 하나만 부르거나 도구 없이 답하면 셀이 멈춥니다 → **흔들림 먼저 확인 대상**.
- 「병렬」: 제목에만 두고 본문은 뜻을 풀어야 합니다 — **한 응답 안에 도구 호출 요청이 여럿**(`parallel_tool_calls`)이고, 프로그램은 이번에 차례대로 실행했습니다. **Ch 18 03 「함께 보내기」(요청 여럿을 동시에 보냄)와 다르다는 한 문장**(Ch 18 요약 §13). 「동시」·「순차」·「병렬」 풀이.
- 정의만 하고 안 쓰는 도구 둘(cell9·11) — 지우거나 도구 파일에서 필요한 것만 가져오기.
- 마지막 요청의 메시지 목록: 딕셔너리 메시지 + `AIMessage` + `*tool_messages`. 과정 관례(튜플·`HumanMessage`·`append`)로 바꿀 수 있습니다. `final.text`는 과정의 `.content`와 다른 이름.
- Ch 7 05(완료)가 `tool_calls`를 「도구를 알려 주지 않은 요청은 `[]`」로 가르쳤습니다 → 「이번에는 도구를 알려 주었으니 목록이 찹니다」로 이을 수 있습니다.

### 06 오류와 읽기 쓰기 분리 (paired)
- **모델을 부르지 않습니다.** 「제공 경로 분리」는 파이썬 목록 `available_tools`를 바꾸는 것뿐이고, 그 목록을 모델에 넘기지 않습니다. 「모델은 숨긴 쓰기 도구를 고를 수 없다」는 **관찰하지 않은 사실**입니다(노트북 밖에서도 확인 안 함).
- **서비스 오류(429·5xx·시간 제한)는 다루지 않습니다.** 「오류」는 도구 안의 업무 오류(없는 주문 → `ok: False`·`NOT_FOUND`를 **내놓기**)와 도구 안 예외(`PermissionError`)뿐입니다. 서비스 오류 장면을 넣으려면 규격 §3대로 실제 조건(없는 모델 이름·아주 짧은 `timeout`)으로 만들어야 합니다. 도구 예외의 기본값 `handle_tool_error=False`(이번 확인 — `invoke(tool_call)`도 `PermissionError`를 그대로 내보냄). 도구 오류를 도구 메시지로 바꾸는 것은 Ch 20 02 몫(`handle_tool_errors`).
- **Before가 결함 코드가 아닙니다.** Before는 안전 장치가 막는 장면이고 After는 확인 뒤 여는 장면입니다. 결함 장면 후보: 쓰기 도구를 늘 도구 목록에 두고 확인 여부를 모델이 채우는 인자로 받는 모양(b4가 말만 함).
- 쓰기 도구가 노트북 전역 `app_user_confirmed`·`confirmed_order_ids`를 읽습니다(도구 파일로 옮기면 인자로 받아야 함 — 규격 §2-7 4항). `ORDERS`는 CSV를 **`dtype` 없이** 읽어 01~05와 읽는 법이 다릅니다.
- **Ch 17 이음새**: Ch 17 02 「부작용」·「승인 지점」, 03 「사람 확인」(사람 확인 도구 `['환불 요청 등록']` — 부작용 있는 도구 앞에서 루프를 멈춤), Ch 16 01 「허용 목록」·「막습니다」. 06의 취소 요청 = Ch 17의 등록 도구와 같은 자리입니다.

## 3. 실습 폴더 구조와 읽는 곳

```
labs/part5/ch19-model-tools/
  README.md (4줄 — 「노트북은 서로 독립적」·「Ch 4 공개 실습 자료를 그대로 복사」·「예상 API 비용은 절마다 1달러 미만」)
  pyproject.toml   uv.lock (94항목)
  data/orders.csv  (Ch 4와 바이트 같음, sha256 f2d1e3ee…, 4행 O101~O104)
  notebooks/01~06-*.ipynb
  .ruff_cache/ · .venv/ (macOS 판 243MB — home = /Users/…/cpython-3.12-macos-aarch64-none, uv 0.11.6)
  (없음: runs/ · tests/ · 모듈 · 도구 파일 · 노트북 생성기)
```

- **코드로 읽는 파일**: 여섯 노트북 모두 준비 셀 `find_up("data/orders.csv")`(현재 폴더와 조상 폴더)와 `find_up(".env")`. 01~05는 `fetch_orders(data_path, …)`, 06은 `pd.read_csv(data_path)`. 파일 쓰기 0건. Ch 4 폴더(`labs/part1/…`)는 코드로 읽지 않습니다.
- **`data/orders.csv`는 보호 파일**(Ch 17 요약·Ch 18 매니페스트, 바꾸지 않음). 학생 묶음 `textbook/part5/public-files.json` 8행 · 챕터 `qa/public-files.json` `labs` 목록(`README.md`·`pyproject.toml`·`uv.lock`·`data/orders.csv`·`notebooks/*.ipynb` — **`*.py`는 없음**). `part5-practice.zip`에는 Ch 4 실습 폴더 전체(`data_tools.py`·`tests/`·`data/`)도 들어 있습니다(`textbook/part5/_build_index.py` 68행).
- **옛 생성기**(부르는 곳 0 — 챕터 `qa/public-files.json` 제외 목록 `_src`·`qa`에 걸리지 않지만 실행하는 스크립트 없음):

| 파일 | 무엇을 씀 | 비고 |
|---|---|---|
| `textbook/part5/ch19-model-tools/_make_sources.py`(46KB) | `_src/*.html` 여섯 + `labs/…/notebooks/*.ipynb` 여섯(출력 없이) | 실행하면 개선본을 옛 판으로 덮어씀. 제목 「@tool과 Ch4 함수 재사용」 등 옛 제목·b8 틀 |
| `textbook/part5/ch19-model-tools/figures/_gen_figures.py` | `NN-…-flow.{svg,excalidraw,caption.md}` 18개(`textbook/part5/_figure.py`) | 옛 그림 |
| (챕터 밖) `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part5_enrich.py`·`part5_review_repairs.py` | 「코드를 읽기 전에」·「다음 셀을 읽는 방법」 블록을 끼워 넣은 옛 도구(ch19 이름이 들어 있음) | 기록만(Ch 16~18 선례대로 막지 않음) |

→ 규격 §8 1번: **01절 작업 때 앞의 둘 첫머리에 설명 주석 + `raise SystemExit(...)`**, 마감 때 `mv -n` → `qa/upgrade/before/generators/blocked/`(사본은 이미 `before/generators/`).

- **판**: `requires-python = ">=3.12,<3.13"`, `dependencies = ["langchain==1.4.0", "langchain-openai==1.6.0", "pandas==3.0.5", "pydantic==2.12.5", "python-dotenv==1.2.3"]`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`pytest==9.1.1`·`ruff==0.15.6`, `[tool.uv] package = false`. 잠금 주요 판: `langchain-core 1.6.2`·`langgraph 1.2.11`·`openai 3.11.0`·`langsmith 0.12.4`·`pydantic-core 2.41.5`·`numpy 2.5.3`(pandas가 끌어옴)·`httpx 0.28.1`·`tiktoken 0.14.0`. `pytest`는 있지만 `tests/`가 없습니다.
- **Part 5 안 판 차이**: `langchain-openai` Ch 19·20 **1.6.0** ↔ Ch 17 **1.6.1**(과정 요약·Ch 17 요약 「강사 확인」) · `pydantic` Ch 19 **2.12.5**(pyproject에 고정) ↔ Ch 17·20 **2.13.5** · `openai` Ch 19 3.11.0 ↔ Ch 18 2.29.0(SDK 직접). Ch 19에만 `pandas`.
- **`verify.py` 규칙**(`check_imports`): Ch 18 폴더 밖에서는 `openai` import 금지 → Ch 19는 LangChain으로만. 모든 노트북에서 모듈 이름 `rag`·`context_lab`·`document_processing`·`experiment`·`harness`·`prompts` import 금지 → **도구 파일 이름을 이것들로 지으면 verify가 멈춤**. `tests/test_verify.py` 60·62행이 「Ch 18 예외는 `labs/part5/ch19-model-tools/notebooks`에 안 걸린다」를 시험(이번에 통과 확인).

## 4. 이음새 — Part 6 선행 목록 계약과 앞뒤 챕터

### 4-1. Part 6 선행 목록 (Ch 19 03·05·06)

| 파일 | 무엇을 | 계약 |
|---|---|---|
| `textbook/part6/ch28-mcp/qa/prerequisite-files.json`(Ch 28 **대기**, 고치지 않음) | Ch 19 **HTML 셋**(`textbook/part5/ch19-model-tools/03·05·06-*.html`) + **노트북 셋**을 적음 | 선행 목록의 **원본**. `textbook/part6/qa/collect_public_files.py`가 챕터 목록의 `labs/` 줄만 모아 `textbook/part6/prerequisite-files.json`을 다시 씀 |
| `textbook/part6/prerequisite-files.json` 7~9행 | 노트북 셋(+ Ch 14 자료 둘·Ch 16 `guardrails.py`·테스트·Ch 18 06·`workflow_tools.py`·Ch 21 자료) | `textbook/part6/_build_index.py` 67~74행이 **`part6-practice.zip`에 넣음**. 목록의 파일이 공개 파일(`practice_files`)에 없으면 `ValueError`로 멈춤 |
| `textbook/downloads/part6-practice.zip`(`dacb688e…`, Ch 18 마감 뒤 보완) | Ch 19 노트북 셋만 들어 있음 — **`data/orders.csv`·`pyproject.toml`·`uv.lock`은 없음** | 그래서 **Part 6 묶음에서 Ch 19 노트북은 지금도 실행되지 않습니다**(준비 셀 `assert data_path is not None`에서 멈춤). **읽기용 참고 파일**입니다 |
| `textbook/part6/qa/final-artifact-hashes.json` 355~357행 | 노트북 셋 해시 `7dcb5963…`·`c0888cbd…`·`928d47ca…` | **읽는 스크립트 없음**(`.py` grep 0). **이미 지금 파일과 다름**(지금 `bb18458d…`·`899919f7…`·`3f5d44c2…`). Ch 18 마감은 자기 줄만 손으로 고침 |
| Ch 28 `_src` 01 b2·b3 · 02 b3 · 04 b2·b3 · 05 b2·b3 | **문장으로만 인용**(아래 4-4) | 저장된 출력을 읽는 코드·실행하는 코드 **0건**(Ch 28 노트북·`course_server.py` grep 0) |
| `labs/part6/continuity-guide.md` 14행 | 「Ch19의 도구 정의와 호출 비용 → Ch28 MCP 서버·클라이언트와 도구 정의 토큰」 | 문장 |

- **결론: 출력 계약은 없고 묶음 계약만 있습니다.** Ch 29 04가 Ch 18 06의 저장 출력을 코드로 읽는 것과 다릅니다. Ch 19가 03·05·06을 다시 쓰면 (a) `part6-practice.zip`이 낡으므로 마감 때 `python3 textbook/part6/_build_index.py`로 다시 만들고(Ch 18 선례 — `integration-results.json`도 바뀜), (b) `final-artifact-hashes.json` 세 줄을 손으로 새 값으로 적을지 정하고(Ch 18은 자기 줄을 고침), (c) **03·05·06이 도구 파일을 가져오게 되면** 도구 파일을 Ch 28 `qa/prerequisite-files.json`·`textbook/part6/prerequisite-files.json`에 더할지 정합니다(Ch 18 「마감 뒤 챕터 리드 보완」이 `workflow_tools.py`를 Ch 29 목록에 더한 선례). 다만 Part 6 묶음엔 `data/orders.csv`도 없어 더해도 실행되지 않습니다 — 읽기용으로 둘지, 자료·잠금까지 넣어 실행되게 할지는 강사 확인 대상입니다.

### 4-2. Ch 19 파일을 **코드로** 읽거나 실행하는 곳

| 읽는 곳 | 무엇을 | 계약 |
|---|---|---|
| **`textbook/part5/qa/check_bundle_execution.py`** 29~42행 | `part5-practice.zip`을 풀어 **Ch 19 01 노트북을 새 커널로 실행**(Ch 17 05·Ch 20 03과 함께 「대표 오프라인 노트북」, `uv sync --locked` 뒤 `notebooks/`에서, **API 키 복사 없음**), 실행 뒤 `code_sha256`이 같은지 봄 | **01에 모델 요청을 넣으면 이 검사가 멈춥니다**(키 없음). `%pip` 셀을 넣으면 네트워크 설치가 끼어듦. Ch 17 마감 기록 `bundle-execution.json`(zip `3088b2e2…`, 01 `768bc0125165` PASS) |
| `textbook/_notebook/verify.py` 105~124행 | import 규칙(§3) | 도구 파일 이름 |
| `textbook/part5/_build_index.py` 23행 | (6, 10, 설명 「조회 함수를 도구로 감싸고 입력 검증·설명문·호출 결과를 연결합니다」) · `verify_lesson` | 실습 절·설명 대조 |
| `textbook/_notebook/build_index.py` 42행 | (`'LangChain Model과 Tool'`, 절 수 **6**, 설명) · `build_bundle.py` 22행 | 제목이 `chapter.json` 「모델과 도구」와 다름 · 실습 절 |
| `textbook/part5/qa/check_scope.py`(`EXPECTED` (6, 10) · `SECTION_COUNTS` ch19 = 6) · `check_notebook_readiness.py`(**함수 타입힌트 필수**·노트북마다 `assert`·21개) · `check_figures.py`(SVG마다 `.excalidraw`) · `finalize_evidence.py`(`language/ch19-final.json` 해시) · `check_delivery.py` | 옛 검사 | Ch 17·18과 같이 **고치지 않고 기록** |
| 기록만 | `textbook/part5/qa/ch19-before-integration/`·`language/ch19-original/`(옛 사본) · `ch19-technical-review.md`·`ch19-visual-summary.json` · `textbook/part6/qa/existing-artifact-hashes.json` · `textbook/part7/qa/existing-artifacts-before.json` · `textbook/_notebook/checks/notebook-contracts-part5-ch19-model-tools.json`(verify가 다시 씀) | — |

- **Ch 20 이후가 Ch 19 파일을 코드로 읽는 곳 0건**(Ch 20 노트북은 자기 규정 자료·도구를 다시 선언). `textbook/qa/check_course_continuity.py` 노트북 목록에도 Part 5가 없습니다.

### 4-3. Ch 19가 앞 챕터 파일을 읽는가

- **0건.** Ch 4 `fetch_orders`는 복사본(AST 같음). Ch 17 `agent_tools.py`(LangChain `chat_model.invoke` 모양 — `estimate_cost` 포함)·Ch 18 `workflow_tools.py`(SDK 직접)는 가져오지 않습니다. **Ch 6 06 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`**는 LangChain `usage_metadata`에 그대로 맞아(Ch 17 `agent_tools.py`에도 같은 본문) 04·05 비용 셈에 옮겨 쓸 수 있습니다.

### 4-4. 문장으로 기대는 곳 (확인한 것만)

| 자리 | 지금 문장 | Ch 19 개선 때 |
|---|---|---|
| **Ch 2 09 b2·b8**(완료) | 「Ch 19에서 쓰는 `@tool` 줄도 아래 함수를 감싸는 데코레이터라서, 이 절의 `@` 줄과 같은 규칙으로 읽습니다」 | **`@tool` 줄을 남겨야 참** |
| **Ch 2 10 b2·b8**(완료) | 「Ch 6의 구조화 출력과 Ch 19의 도구 입력 규칙에서 `BaseModel`과 `Field()`를 다시 만납니다」 | 02가 `BaseModel`·`Field` 유지 |
| **Ch 4 01 b2·b7 · 03 b2·b7 · 04 b2 · 06 b8 · 06 노트북 셀 8**(완료) | 「Ch 19에서는 이런 조회 함수를 에이전트가 부르는 도구로 씁니다」 · 「Ch 19 01절이 도구로 다시 쓰는 것은 이 실습 폴더 판(`fetch_orders(csv_path, *, status=None)`)입니다」 | **01이 실습 폴더 판을 써야 참**(§2 01) |
| **Ch 7 05 b4**(완료) | 「도구를 모델에 알려 주고 호출 요청을 받는 방법은 Ch 19 05절에서 다룹니다」 | 05가 `bind_tools`·`tool_calls` 유지(04가 먼저 쓰는 순서 — §2 04) |
| **Ch 8 02 b7 · 04 b8 · 목차**(완료) | 「모델이 도구로 함수를 부르게 하는 방법은 Ch 19에서」 · 「모델이 도구 설명을 보고 도구를 고르는 실험은 Ch 19 04절」 · 「혼란 조건 → Ch 19 04절에서 도구 설명만으로 도구를 고르는 실험」 | 04가 설명으로 고르는 실험 유지 |
| **Ch 17 01 b7 · 03 b4**(완료) | 「모델이 실제로 도구를 고르는 코드는 Ch 19와 Ch 20에서 만듭니다」 · 「모델 요청에 도구를 함께 싣는 방법(`bind_tools`)은 Ch 19 05절에서 다룹니다」 | 〃 |
| **Ch 18 07 b8 · 노트북 정리**(완료) · `labs/part5/continuity-guide.md` 5행 | 「Ch 19에서는 함수를 도구로 만들고, 모델이 도구 설명을 보고 고르게 합니다」 | 참 |
| **Ch 22 01 b3**(시범 — 완료) | 「Ch19에서는 함수 위에 `@tool` 줄을 붙여 도구로 만들었습니다」 · Ch 22 노트북 01·04·09의 도구 `lookup_hours(day: str) -> str` + 독스트링 | **`@tool` 줄을 남겨야 참** · 도구 정의 모양의 선례 |
| Ch 20 01 b2·b3 · 02 b3 · 04 b3(대기) | 「Ch19에서는 `@tool`과 `bind_tools`로 … 모델 응답의 `tool_calls`를 해석해 도구 함수를 호출했습니다」 · 「주문 조회 함수에 `@tool`을 붙이고 `model.bind_tools(tools)`가 도구 스키마를 모델 요청에 포함시키는 과정」 · 「지원 범위를 도구 docstring과 Pydantic 스키마에 적었습니다」 · 「`tool_calls`를 해석했습니다」 | 05가 `tool_calls`로 실제 도구를 실행해야 참. Ch 20 02 비유 「택배 송장 번호 = `tool_call_id`」(Ch 19 삽화와 겹치지 않게) |
| Ch 21 05 b3 · Ch 27 02 b3(대기) | 「Ch19의 `@tool`를 사용합니다」 · 「Ch 19에서 `@tool`로 함수 설명과 입력 스키마를 만들었고」 | 참 |
| **Ch 28 01 b3**(대기) | 「Ch19에서 도구 이름·설명·입력 스키마가 **모델 선택에 영향을 준다는 사실을 확인했습니다**」 | **지금 Ch 19 04는 차이를 관찰하지 못했습니다(9/9·9/9)** → 04 결과에 따라 참/거짓. Ch 28 몫이지만 인계에 적을 것 |
| Ch 28 02 b3 · 04 b2·b3 · 05 b2·b3(대기) | 「Ch4에서 함수와 **타입 힌트**를, Ch19에서 `@tool` 장식자와 입력 스키마를 배웠습니다」 · 「Ch19에서 `@tool`로 만든 BaseTool의 name, description, args_schema를 모델에 연결」 · 「Ch19에서 **도구 개수가 늘면 선택 정보가 커진다**는 사실을 배웠습니다」 · 「`bind_tools`가 도구 설명을 모델 요청에 포함시키고 `usage_metadata`가 입력·출력 토큰을 제공한다는 사실을 확인」 | 「도구 개수 → 입력 토큰」은 지금 Ch 19 어느 절도 재지 않습니다(03은 글자 수, 04는 설명 길이 차이 `+33`만) → 03·04가 잴지 결정, 아니면 Ch 28 인계 |
| `textbook/part5/_src/index.html` 7행 · `practice-start.md` 7·15행 · `labs/part5/continuity-guide.md` 7·9행 | 「Ch 4의 조회 함수는 Ch 19의 도구 설계로」 · 「Ch 4 원본과 비교할 수 있도록 `labs/part1/ch04-data-tools`도 함께 제공」 · 「원본 SHA-256이 함께 적혀 있습니다」(**사실과 다름**) | Part 5 마감 몫 또는 Ch 19 마감(Ch 18은 continuity-guide 한 줄을 고침) |

## 5. §2-7 판단 근거 — 도구 파일

### 사실
1. **앞 챕터 함수**: Ch 4 `fetch_orders`(01~05 다섯 번 같은 셀). 규격 §2-7 3항대로면 「앞 챕터에서 이미 가르친 함수는 노트북에 다시 적지 않습니다」 — 다만 Ch 4가 **노트북에서 가르친 판**과 **Ch 19가 쓰는 판**이 다릅니다(§2 01). Ch 6 06 `estimate_cost`도 후보(04·05).
2. **챕터 안 되풀이**: 준비 셀·`fetch_orders`·도구 셋·모델 셀이 185줄(53%). 도구 셋(목록·한 건·집계)은 **03이 처음 정의**하고 04(구체 조건)·05가 글자까지 같게 다시 적습니다. 01의 `list_orders_by_status`도 같은 본문.
3. **도구 객체를 옮기기 어려운 까닭**: 세 도구가 노트북 전역 `data_path`를 읽습니다. 모델에게 CSV 자리를 숨기는 것이 01의 학습 내용이라 도구 인자로 받을 수 없습니다 → 도구 파일에 두려면 **파일 안에 CSV 자리 상수**(예: 파일 위치 기준 `../data/orders.csv`)를 둬야 하고, 규격 §2-7 4항 「노트북 전역 이름에 기대지 말고 필요한 값은 인자로 받습니다」와 어긋납니다. 도구를 만들어 내는 함수(함수 안에 `@tool` 함수)는 「함수 안의 함수」라 금지.
4. 04는 조건마다 **설명만 다른 도구 벌**을 새로 만들어야 하므로(실험 변수) 04의 도구 정의는 노트북에 남습니다. 06의 도구 둘은 06이 처음.
5. 벡터 계산이 없어 NumPy 대상은 없습니다. `tests/` 없음 → §2-7 7항(AST 테스트) 해당 없음.

### 선택지 (결정하지 않음 — 장단점만)

**A. 도구 파일을 만들지 않는다** — 장점: 묶음 목록·README·Part 6 선행 목록이 움직이지 않음. 01이 `fetch_orders` 본문을 보여 주며 「고치지 않고 감싼다」를 눈으로 비교. 단점: 185줄 되풀이(준비 셀은 줄여도 도구 셋이 03·04·05에 남음). 규격 §2-7 3항과 부딪힘(과정 선례 Ch 2·4·6·22는 「만들어도 챕터 전체가 줄지 않음」이 근거였고 Ch 19는 줄어듦).

**B. 평범한 함수만 담은 도구 파일**(이름 후보 **`order_tools.py`** — 내용 이름·과정 관례 `*_tools.py` / `model_tools.py` — 챕터 이름. `tools.py`는 `langchain.tools`와 헷갈림, `prompts.py`·`experiment.py`는 verify가 막음, `agent_tools.py`·`workflow_tools.py`는 앞 챕터와 같은 이름)
- 담을 후보: Ch 4 `fetch_orders`(주석 「Ch 4 실습 폴더 `data_tools.py`에서 옮겼습니다」) · 03 한 건 찾기·집계의 **몸통 함수**(`find_order(csv_path, order_id)`·`sum_orders(csv_path, status)` 꼴 — 인자로 받음) · Ch 6 06 `estimate_cost` · 04 채점·기록 출력 함수. `@tool` 감싸기(3~5줄)는 노트북에 남김.
- 장점: 규격 §2-7 4항(인자로 받기)을 지킴. 노트북 `@tool` 셀이 짧아지고 「도구 = 감싼 겉」이 드러남. 04가 몸통을 가져와 설명만 다른 겉 둘을 만들기 쉬움.
- 단점: 셀 수는 크게 안 줄 수 있음(겉 감싸기가 절마다 남음). 01에서 `fetch_orders`를 가져오면 01 제목 「Ch 4 함수 재사용」을 **가져오기로 보여 주는 셈** — 본문을 파일에서 열어 보라는 문장 필요.

**C. 도구 객체까지 담은 도구 파일**
- 장점: 03이 만든 세 도구를 04 구체 조건·05가 한 줄로 가져옴(가장 많이 줄어듦).
- 단점: CSV 자리를 파일 안 상수로(§2-7 4항과 충돌) · `@tool` 객체 import는 학생이 「도구가 어디서 왔는지」 읽기 어려움 · 05·06이 가져오면 Part 6 선행 목록·`part6-practice.zip` 처리(§4-1) · 파일 위치 계산에 `__file__`·경로 조작(미교육).

**공통으로 따라오는 것(B·C)**: 묶음 목록 두 곳(`textbook/part5/public-files.json`·챕터 `qa/public-files.json` `labs`에 `notebooks/order_tools.py`) · README · 「앞에서 배운 함수는 `…_tools.py`에 모아 두었습니다 …」 고정 문장(과정 요약 §3) · `run_section.sh`는 이미 `notebooks/`를 `PYTHONPATH`에 더함 · `check_bundle_execution.py`가 01을 `notebooks/`에서 실행하므로 01이 가져와도 됨 · 03·05·06이 가져오면 §4-1 (c).

## 6. 과정 규칙과 부딪히는 것 — 도구 정의에 필요한 문법

**이번에 모델 없이 확인한 사실**(가상환경, `langchain-core 1.6.2`·`pydantic 2.12.5`):

| 시험 | 결과 |
|---|---|
| `@tool` + `status: str`(지금 모양) | `args` = `{'status': {'title': 'Status', 'type': 'string'}}`, 모델에 가는 도구 글 `{"properties": {"status": {"type": "string"}}, "required": ["status"]}` · 정수 `3`을 넣으면 **`ValidationError`** |
| `@tool` + **타입힌트 없음** | `args` = `{'status': {'title': 'Status'}}`, 모델에 가는 글 `{"status": {}}`(**자료형 없음**) · 정수 `3`이 **검사 없이 통과**(`[]`) |
| `@tool` + **독스트링 없음** | **`ValueError: Function must have a docstring if description not provided.`** |
| 데코레이터 없이 `tool(함수)` | `StructuredTool`, `args` 같음(자료형은 여전히 힌트에서) |
| `StructuredTool.from_function(함수, name=, description=)` | 이름·설명을 인자로, `args` 같음 |
| `@tool(args_schema=OrderQuery)` + **함수 힌트 없음** | `args`가 양식 클래스에서 옴(`type`·`description` 포함) |
| `@tool("get_order_by_id", description="…")` | 파이썬 함수 이름과 다른 공개 이름 |
| 반환 힌트(`-> list`·`-> list[dict[str, Any]]`) | **입력 형식에 안 들어감**(모델에 가는 글에 반환 없음) |
| 도구가 목록·딕셔너리를 내놓음 → `invoke(tool_call)` | `ToolMessage` 내용이 JSON 글 `'[{"order_id": "O101", "amount": 32000}]'` |
| `model.bind_tools([...], parallel_tool_calls=False)`(모델 호출 없이 `kwargs` 확인) | 요청에 실리는 것 = `{"type": "function", "function": {"name", "description", "parameters"}}` 목록 + `parallel_tool_calls` |

**과정 규칙과 선례**: 규격 사다리 L2(Ch 2 04 이후 함수 정의 **타입힌트 포함**) · L5(`BaseModel`은 라이브러리가 스키마를 요구할 때만, 필드만) · L6(`@tool` 같은 라이브러리 데코레이터, 처음 쓰는 자리에 「이 줄은 아래 함수를 ○○로 등록합니다」) · A 트랙은 Ch 2 09·10을 건너뜀 → **세 문장 + 링크**(과정 요약 §2-1이 「확인된 곳: Ch19 01(`@tool`)·02」로 이미 지목). Ch 2 07이 가르친 힌트 모양은 `: int/str/float = 기본값`·`-> int/str`뿐이고 **Ch 13~18은 힌트 0건**(Ch 18 마감은 Part 5 소개의 「타입 힌트」를 뺌). 시범 Ch 22(강사 확인 완료)는 `@tool` + `day: str` + `-> str` + 독스트링.

### 선택지 (결정하지 않음 — 장단점만)

**타입힌트**
- (가) **`@tool` 함수의 매개변수에만 Ch 2 07 모양 힌트**(`status: str`·`order_id: str`·`limit: int`), 반환 힌트는 `-> list`/`-> dict`로 짧게 두거나 뺌, 평범한 함수·준비 셀은 힌트 없음 — 장점: 입력 형식에 자료형이 생기고 잘못된 자료형이 막힘(위 시험), Ch 22 선례와 같음, 「힌트가 곧 모델이 보는 형식」을 가르칠 수 있음. 단점: Ch 13~18 흐름(0건)과 달라 한 문장 필요, `fetch_orders` 실습 폴더 판의 `str | Path`·`list[dict[str, Any]]`를 그대로 두면 새 표기가 늘어남.
- (나) **힌트를 모두 빼고 02부터 양식 클래스(`args_schema`)로 자료형을 줌** — 장점: 함수에 힌트 0. 단점: 01·03~05의 도구 글에 자료형이 없고 검사도 없음(위 시험), 01이 `BaseModel`을 먼저 써야 하거나 형식 없는 도구를 가르치게 됨, Ch 28 02 「Ch4에서 함수와 타입 힌트를, Ch19에서 @tool과 입력 스키마」와 멀어짐.
- (다) 지금 모양 그대로(`list[dict[str, Any]]`·`str | Path`·`Path | None`) — 장점: Ch 4 `data_tools.py`와 AST 같음 유지. 단점: 처음 쓰는 표기 넷(`|`·`list[…]`·`dict[…]`·`Any`)마다 한 문장, 준비 셀까지 힌트.

**클래스(`BaseModel`)**
- 02 `OrderQuery`는 **라이브러리가 스키마를 요구하는 자리**(L5 안)이고 Ch 6 03 「양식 클래스」로 이어 씀. 반환 쪽 `OrderRecord` + `TypeAdapter`는 선택: (가) 두기(새 API `TypeAdapter`·`list[…]`, 금액 `float` 변환이 출력에 보임) / (나) `for` + `OrderRecord.model_validate(행)` 또는 `OrderRecord(**행)`(각각 미교육 한 문장) / (다) 반환 검사를 빼고 입력 검사만(제목 「반환 스키마」와 어긋남).

**데코레이터**
- (가) **`@tool` 유지** — 장점: 완료 챕터 약속 넷(Ch 2 09·Ch 22 01·Ch 21·27·28 문장)이 참, 과정 요약이 이미 「세 문장 + 링크」 자리로 지목. 단점: A 트랙 첫 `@`, 인자 있는 모양 `@tool(args_schema=…)`·`@tool("이름", description=…)`까지 세 모양.
- (나) `tool(함수)`·`StructuredTool.from_function(…)` 호출 모양 — 장점: `@` 문법 없이 같은 도구(위 시험). 단점: 약속 문장이 거짓이 됨(완료 챕터 Ch 2 09·Ch 22 01 수정 필요), LangChain 문서의 기본 모양과 다름.
- (다) 절마다 한 모양만(01·03·05·06 맨 `@tool`, 02만 `args_schema`, 04만 이름·설명 인자) — 모양이 늘어나는 자리를 절 학습 목표에 묶음.

**독스트링**: `@tool`이 설명으로 쓰므로 필수(없으면 `ValueError`) — 과정 첫 등장. 01에서 「함수 첫 줄의 세 따옴표 글 = 도구 설명」을 세 문장(뜻 → 일상 예 → 코드 모습)으로 가르치고 03이 좋은 설명을 다룸. 대안은 `description=` 인자만 쓰기(04 모호 조건 모양) — 독스트링을 안 가르쳐도 되지만 LangChain 기본 모양·Ch 22 선례와 다름.

**그 밖**: 키워드 전용 `*`·기본값 `None`(실습 폴더 판을 쓰면 남음 — Ch 4 01 b7이 뜻만 풂) · 06 try `else` + `raise AssertionError`(B 트랙 문법 → `if`로 풀기) · 준비 셀 `find_up`(→ Ch 17 05 `candidates = [".", "../../..", "../../../.."]` + `os.path.exists` + `for`·`break` 선례).

## 7. 삽화 비유 계열 후보

**이미 쓴 계열**(과정 요약·계약 §1·각 챕터 요약·`figures/*.prompt.md` 155개 grep): 카드·카드 상자·서류철·봉투·두 겹 봉투·서랍·쟁반·칸막이 쟁반·블록·끈·실·단추·관·깔때기·그릇(Ch 1)·빵 칼(Ch 5)·**주문서 양식·바구니(Ch 2 06·13)**·이름표·꼬리표(Ch 2)·우편함·소포(Ch 6·7)·명찰·클립보드(Ch 7)·도막(Ch 10)·색 딱지(Ch 11)·자물쇠(Ch 3·10·12)·열쇠(Ch 2·3)·리모컨·플러그(Ch 1)·**나무 길·갈림길·나무 레일·작업대(Ch 13·18)**·**나무판·구멍·마개(Ch 14 — 모양 맞추기)**·바구니·사과·저울·모래시계·궤짝·선반·눈금(Ch 15)·쪽지·도장·덮개 천·두루마리·개찰구·체·돌(Ch 16)·눈 위 발자국·바위·말뚝·울타리(Ch 17)·**점토·물레·가마(Ch 18)**·공항 검사·우편 가림막·전화 연결·교통카드 개찰구·방문자 명부·서류함·안내 데스크(Ch 22). **도구 상자·공구·공구판·걸이·정원 도구·물뿌리개·전지가위·식당·메뉴판·주문 전표·접이식 다용도 칼은 0건**(드라이버는 Ch 3 05-5 사람 손의 소품 한 번). 지금 `_src` b4 비유 「도구 설명서는 주문서와 비슷합니다」는 Ch 2 「주문서」와 겹칩니다.

| 후보 | 그림 요소 | 맞는 절 | 겹침 점검 |
|---|---|---|---|
| **벽 공구 걸이와 그림 꼬리표** | 벽의 고리에 걸린 공구마다 글자 없는 그림 꼬리표(돋보기·자·가위 모양 그림) / 꼬리표가 모두 똑같이 빈 벽과 저마다 다른 벽 / 공구 둘을 한꺼번에 내린 빈 고리 둘 / 자르는 공구만 닫힌 유리문 안 | 01(공구는 그대로, 꼬리표만 더함) · 03·04(꼬리표 = 설명) · 05(한 번에 둘) · 06(읽기 공구 열린 걸이 · 쓰기 공구 닫힌 문) | 공구·걸이 0건. **구멍·윤곽선 자리는 쓰지 말 것**(Ch 14 모양 맞추기와 겹침) · 작업대 빼기(Ch 13·18) · 자물쇠 대신 걸쇠 유리문(Ch 3 자물쇠) |
| **정원 도구 창고** | 물뿌리개·모종삽·갈퀴·전지가위가 그림 표식과 함께 걸림 / 들여다보는 도구(돋보기·자)와 되돌릴 수 없는 도구(전지가위)를 나눈 두 칸 | 01·03·04 · 06(자르면 되돌릴 수 없음 = 쓰기) | 원예·정원 0건(Ch 18 후보였지만 안 씀). 화분에 모종 맞추기는 모양 맞추기라 피할 것 |
| **식당 주문 전표와 내주는 창** | 그림만 있는 메뉴판 / 색 집게를 단 전표 둘이 한꺼번에 걸림 → 같은 색 집게가 꽂힌 접시 둘이 창으로 나옴 / 칼 서랍은 닫히고 국자는 걸려 있음 | **05**(호출 ID ↔ 도구 메시지 짝, 모델은 주문만 쓰고 요리는 프로그램) · 04(그림 메뉴 vs 빈 메뉴) · 06 | 식당 0건. **쟁반 금지 문구 필수**(Ch 4·5·6 쟁반 계열) · 집게는 Ch 7 클립보드와 조금 겹침 · 레일은 Ch 13 · 사람 없이 그리면 「누가 주문하는가」가 약함 · Ch 20 02 비유 「택배 송장 번호」와 겹치지 않음 |
| **접이식 다용도 칼(멀티툴)** | 손잡이 하나에 접혀 들어간 도구 여럿, 둘을 동시에 편 모습 / 칼날만 접혀 걸쇠로 잠김 | 01(한 몸통에 도구를 붙임) · 05 · 06 | 0건. Ch 5 「빵 칼」과 칼날이 겹침 · 부품이 작아 「그림만 보고 읽히는가」 위험 |

- 한 계열로 챕터를 이을지(예: 공구 걸이 01·03·04·06 + 식당 05), 절마다 다를지는 01 작업자가 정합니다. 사람·손·동물·화면·글자·숫자는 넣지 않는 것이 앞 챕터 선례입니다(꼬리표는 **그림 표식**으로).

## 8. 위험과 깨진 것

1. **04의 핵심 관찰이 없음**(§2 04) — 공개 이름이 역할을 말해 설명 차이가 선택을 가르지 않음(9/9·9/9). 입력(공개 이름·질문)을 고치면 모호 조건 선택이 **실행마다 흔들릴 것** → 규격 §2-7 9·10번(밖 다섯 번 먼저, 두 번 같은 값만 결론, 탐색 입력 b7). Ch 28 01 b3 문장이 이 결과에 걸림.
2. **05가 모델 답에 건 `assert` 셋**(호출 2개·인자 집합·답 글) — 규격 §3은 매번 같은 값에만. 질문 글이 호출 수를 정하는 모양. 모델이 한 번에 하나만 부르면 셀이 멈춤 → 흔들림 확인 대상.
3. **`reasoning_effort="none"` 없음**(04·05) — `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` + `bind_tools(…, parallel_tool_calls=…)` 조합은 **이번에 보내지 않았습니다**(Ch 22는 `create_agent` 경로에서 도구 호출까지 통과). 04 첫 실행에서 확인.
4. **01 오프라인 계약**(§4-2) — `check_bundle_execution.py`가 Ch 19 01을 키 없이 실행. 01에 모델 요청·`%pip`을 넣으면 멈추거나 느려짐.
5. **완료 챕터 약속**(§4-4) — `@tool` 줄(Ch 2 09·Ch 22 01) · `BaseModel`·`Field`(Ch 2 10) · 실습 폴더 판 `fetch_orders`(Ch 4 네 곳) · `bind_tools`는 05절(Ch 7 05·Ch 17 03) · 04는 설명으로 고르는 실험(Ch 8). 어기면 완료 챕터를 고쳐야 함.
6. **Part 6 묶음**(§4-1) — 03·05·06을 바꾸면 `part6-practice.zip` 재생성, `final-artifact-hashes.json` 세 줄(이미 낡음), 도구 파일을 가져오면 선행 목록. Part 6 묶음에서 Ch 19 노트북은 **지금도 실행 불가**(자료·잠금 없음).
7. **paired Before 셋 중 둘이 결함 장면이 아님**(02 스키마가 막는 장면 · 06 안전 장치가 막는 장면). 01 `TypeError`만 실제 결함. paired 빨강 상자 규칙(규격 §5-3)을 쓰려면 결함 장면 필요.
8. **06은 모델도 서비스 오류도 없음** — 「읽기·쓰기 제공 경로 분리」를 모델로 관찰하지 않음. 넣으면 모델 답(숨긴 도구를 고르려 하는가·다른 도구로 대신하는가)에 기대 흔들림.
9. **실행하지 않은 사실**: 01 b3·b7(AST·해시 「검증 기록」), `continuity-guide.md` 7행(SHA-256), 03 b1 「측정」(모델 없음), 06 「모델이 만든 문자열은 승인 증거가 될 수 없다」(개념은 맞지만 실행 장면 없음).
10. **05 병렬 말** — 제목 「병렬」(Ch 13 금지어, Ch 18은 「함께 보내기」), 한 응답의 호출 여럿 ≠ 동시 실행. 「동시성은 측정하지 않았습니다」는 이미 밝힘 — 재지 않은 속도 단정 금지(규격 §3).
11. **옛 생성기 둘이 개선본을 덮어씀**(§3) — 01 작업 첫머리에 `raise SystemExit`.
12. **Part 5 옛 검사 넷**(Ch 17·18과 같음) — `check_scope.py` 절 수 6·실습 meta · `check_notebook_readiness.py` 타입힌트 필수·21개·결과 파일을 먼저 씀 · `check_figures.py` `.excalidraw` 짝 · `finalize_evidence.py` 해시. 고치지 않고 기록.
13. **비용·요청 수**: 한 번씩 20번 ≈ 0.005달러. 04가 18번이라 새 커널 두 번 + 밖 다섯 번(04 한 판 18번 × 5 = 90) + 05(2 × 5)까지 해도 요청 약 200번·0.05달러 안팎 — 절당 1달러 상한과 거리가 멂. 04 한 번의 모델 대기는 짧아(요청 18) 기기 셸 180초 안이지만 걸린 시간은 잰 적 없음.
14. **판 차이**: `langchain-openai` 1.6.0(Ch 19·20) ↔ 1.6.1(Ch 17) · `pydantic` 2.12.5 ↔ 2.13.5 · `openai` 3.11.0 ↔ 2.29.0(Ch 18) — 잠금은 바꾸지 않는 것이 선례, 강사 확인.
15. **디스크·환경**: 기기 루트 여유 **2.0G**(작업 전후 같음 — pip 캐시 안 씀). 가상환경은 마운트 폴더(382MB, pandas·numpy 포함). Mermaid 도구(`/tmp/mmd`·`/tmp/libs`·`/tmp/pptr-cache`·`/tmp/pw`) 있음. 루트 `.env`에 `OPENAI_API_KEY` **이름** 있음(값은 보지 않음).

## 9. 01절 작업자가 먼저 결정해야 할 것

1. **`fetch_orders` 판과 도구 파일(§2 01·§5)** — Ch 4 실습 폴더 판(`csv_path, *, status=None`)을 쓸지(Ch 4 약속 네 곳 유지 · 키워드 전용 `*`·기본값·`dtype` 한 문장씩) / Ch 4 01 노트북 판으로 맞출지(약속 문장이 틀어져 완료 챕터 수정 필요) · 도구 파일을 만들지(A/B/C)와 이름(`order_tools.py` 후보) · 01부터 가져올지 노트북에 적을지. 03이 만든 도구 셋을 04·05가 어떻게 받을지까지 01에서 정해 `handoff.md`에 적어야 합니다.
2. **도구 정의 문법의 범위(§6)** — `@tool` 유지(약속 넷) · 매개변수 힌트는 Ch 2 07 모양만 둘지 · 반환 힌트 · 독스트링을 01에서 처음 가르치는 세 문장 · A 트랙용 `@` 세 문장 + Ch 2 09 링크 · 「이 줄은 아래 함수를 도구로 등록합니다」. 준비 셀을 Ch 17 `candidates` 모양으로 바꿀지.
3. **01을 오프라인으로 둘지와 모델 셀 모양(§4-2·§8 3)** — 01에 모델 요청을 넣지 않으면 `check_bundle_execution.py` 계약 유지. 04·05 모델 셀을 과정 표준(`"openai:gpt-5.4-mini"`·`temperature=0`·`reasoning_effort="none"`, `nbkit.key_and_model_cells`)으로. `bind_tools`를 처음 쓰는 절(04)과 약속(「Ch 19 05절」) 사이 순서 처리.
4. **용어 표와 금지어** — 도구(tool) · 도구 설명(description) · 입력 형식(args, 「스키마」를 쓸지) · 양식 클래스(Ch 6 03) · 도구 호출 요청(`tool_calls`) · 도구 메시지(`ToolMessage`) · 호출 ID · 공개 이름 · 읽기 도구/쓰기 도구 · 부작용·승인 지점·사람 확인(Ch 17). 반환→내놓다 · 돌려주다 → 게이트 금지어 · 사전→딕셔너리 · 경로→(CSV 파일) 자리 · 검증→검사 · 거부→막다 · 필드→칸 · 측정→재다 · 추정 비용→예상 비용(Ch 6 06 `estimate_cost`) · 「병렬」은 05 제목과 풀이 한 번. 제목 영어(「tool」·「Pydantic」·「bind_tools」)를 제목에만 두고 본문에서 풀지(Ch 15~18 선례 — 강사 확인).
5. **paired Before의 방향과 흔들림 확인 계획** — 01 `TypeError`(실제 결함)는 그대로 · 02·06 Before를 결함 장면(스키마 없는 도구가 `shipped`에 `[]` · 쓰기 도구를 늘 목록에 둔 모양)으로 바꿀지 02·06 작업자에게 넘길 기준 · 04(공개 이름·질문 고치기)와 05(호출 수)의 노트북 밖 다섯 번 확인 순서와 모델 답에 건 `assert`를 무엇(요청 수·도구 이름 목록의 자료형 등)으로 바꿀지.

## 10. 챕터 마감으로 미룰 것

- **07 실습 절 신설**(규격 §7-2): 슬러그 후보 `07-모델과-도구-실습`, 요청 3~5번, 새 문법·API 0. 주제 예 — 새 주문 문의 하나에 01 도구 + 02 입력 검사 + 06 읽기/쓰기 분리(확인 전후 값 하나만 바꿔 다시). 04(요청 18)·05(모델 답이 호출 수를 정함)는 요청 수 때문에 조심. 따라오는 것: `chapter.json` 절 추가·meta 「실습 30분」(시수에 더하지 않음) · `textbook/part5/_build_index.py` · 챕터 `qa/public-files.json` · `textbook/_notebook/build_index.py` 42행(절 수 6 → 7, 제목 「LangChain Model과 Tool」 ↔ `chapter.json` 「모델과 도구」) · `check_scope.py` `SECTION_COUNTS`(기록만).
- 옛 생성기 둘 `mv -n` → `qa/upgrade/before/generators/blocked/`.
- 옛 그림 18개(`figures/NN-…-flow.{svg,excalidraw,caption.md}`) + `figures/_gen_figures.py` 삭제 승인 목록(사본 `before/figures/`).
- `chapter.json` `objectives` 넷(「tool_calls를 기록하고 평가」·「ToolMessage 반환」·「제공 경로」)과 `textbook/part5/_build_index.py` 23행 설명·`textbook/_notebook/build_index.py` 42행을 개선 본문과 대조.
- `labs/part5/continuity-guide.md` 7행(SHA-256 문장)·9행 · `textbook/part5/practice-start.md` 7·15행 · Part 5 소개 `_src/index.html` 7행 — Ch 19 마감 또는 Part 5 마감 몫(Ch 18은 한 줄씩 고침).
- 실습 폴더 README 다시 쓰기(도구 파일·`notebooks/`에서 열기·`uv sync --locked`·요청 수·예상 비용 — 「노트북은 서로 독립적」은 도구 파일을 만들면 틀림), `qa/research.md`·`qa/verification.md`·`집필점검표.md` 새 값으로(또는 「개선 전 판」 표시).
- `part5-practice.zip` + **`part6-practice.zip`** 재생성, `final-artifact-hashes.json` 355~357행, 도구 파일을 03·05·06이 가져오면 Part 6 선행 목록 둘(§4-1), `check_bundle_execution.py`(Ch 19 01)·`check_delivery.py` 실행(`llm-practice.zip` Stale 멈춤 예상).
- **뒤 챕터 인계**: Ch 28 01 b3(모델 선택에 영향 — 04 결과)·05 b2(도구 개수 → 선택 정보 크기)·02 b3(「Ch4에서 타입 힌트」) · Ch 20 01·02·04 b3(`tool_calls` 해석·docstring·Pydantic)·02 비유(택배 송장) · Ch 21 05·Ch 27 02 b3 문장 대조.
- 삭제 승인 대상: 실습 폴더 `.venv`(macOS 243MB)·`.ruff_cache` · `qa/upgrade/gates-wip-*.json` · `.cache/vm/venv-ch19-model-tools`(382MB) · 기기 `/tmp/ch19-prep`.

## 11. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 6 · `notebooks` 6 · `figures` 19(SVG·excalidraw·caption 각 6 + `_gen_figures.py`) · `generators` 2(`_make_sources.py`·`_gen_figures.py`) · `qa` 3(`public-files.json`·`research.md`·`verification.md`) · `data/orders.csv` · `pyproject.toml`·`uv.lock`·`README.md`·`chapter.json`·`집필점검표.md` = **42개, 540KB**. 원본과 `cmp` 모두 같음(원본은 그대로). `runs/`·`tests/`는 챕터에 없어 없음 |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 190, 통과 0/6) |
| `qa/upgrade/before-manifest.json` | sha256 **39개** — ① Ch 19가 읽는 보호 파일: `orders.csv` 둘(`f2d1e3ee…`) · Ch 4 `data_tools.py`(`d0e9b7b8…`)·`tests/test_data_tools.py` ② Ch 19에 문장으로 기대는 완료 챕터 파일: Ch 4 01·06 노트북·`_src` 01·03·06 · Ch 2 09·10 `_src` · Ch 7 05 · Ch 8 02·04·목차 · Ch 17 01·03 · Ch 18 07 · **Ch 22 01** `_src` · `labs/part5/continuity-guide.md` ③ **Part 6 선행 목록의 Ch 19 노트북 셋(기준선 — 이 챕터가 바꿀 파일)** + Ch 28 목록이 함께 적은 HTML 셋 ④ 그것을 읽는 Part 6 파일: `textbook/part6/prerequisite-files.json` · Ch 28 `qa/prerequisite-files.json` · `final-artifact-hashes.json` · Ch 28 `_src` 01·02·04·05 · `labs/part6/continuity-guide.md` · `part6-practice.zip`(`dacb688e…`)·`part5-practice.zip`(`fe860153…`) ⑤ 규칙을 가진 검사: `verify.py`·`test_verify.py`·`check_bundle_execution.py` |
| `$ROOT/.cache/vm/venv-ch19-model-tools` | Python 3.12.13 · 382MB |

### 가상환경 만든 방법과 걸린 것

- `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy` → `uv venv --python 3.12.13`. 잠금 목록은 `uv export --project labs/part5/ch19-model-tools --frozen --no-hashes --all-groups --no-emit-project`(실습 폴더 파일은 그대로 — 수정 시각 같음), 주석 줄만 빼고 환경 표시는 남김(93줄).
- Ch 16~18 선례대로 `uv pip install pip==26.2` → **`bin/python -m pip install --no-cache-dir -r`**(마운트 폴더에서 `uv pip install -r`이 `.data` 폴더를 못 지워 멈추는 문제를 피함, 루트 디스크에 pip 캐시를 남기지 않음). 이번에는 멈춘 흔적(`*.data/` 폴더) 없음.
- 결과: `pip freeze`와 잠금 대조 **판 차이 0**(설치 87 = 잠금 93 − 이 기기에 해당하지 않는 여섯: `appnope`(darwin)·`colorama`·`tzdata`(win32)·`cffi`·`pycparser`(PyPy)·`httpx2-jsfetch`(emscripten)). `langchain 1.4.0` · `langchain-core 1.6.2` · `langchain-openai 1.6.0` · `langgraph 1.2.11` · `openai 3.11.0` · `pandas 3.0.5` · `numpy 2.5.3` · `pydantic 2.12.5` · `python-dotenv 1.2.3` · `ipykernel 7.3.0` · `nbclient 0.11.0` · `pip 26.2` · `pytest 9.1.1` · `ruff 0.15.6` · `IPython 9.17.1`. `pip check` 이상 없음. 커널 스펙 `share/jupyter/kernels/python3` 있음.
- import 확인만(`langchain`·`langchain_core`·`langchain_openai`·`langgraph`·`openai`·`pandas`·`numpy`·`pydantic`·`dotenv`·`ipykernel`·`nbclient`·`nbformat`·`jupyter_client`·`IPython`·`zmq`·`pytest` · `from langchain.tools import tool` · `from langchain.chat_models import init_chat_model`). `UV_PROJECT_ENVIRONMENT=…/venv-ch19-model-tools UV_NO_SYNC=1 uv run --project labs/part5/ch19-model-tools`로 이 가상환경을 잡는 것도 확인(`run_section.sh`가 자동으로 씀).
- §6 시험은 이 가상환경에서 `OPENAI_API_KEY`를 뺀 채(`env -u`) 가짜 키 글자(`api_key="dummy-not-a-key"`)로 모델 객체만 만들고 **요청은 보내지 않았습니다**.
