# Ch 24 Human-in-the-Loop와 Time Travel — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part6/ch24-human-in-the-loop`(절 셋 — 01 paired, 02·03 experiment) · `labs/part6/ch24-human-in-the-loop`. 바로 앞 Ch 23(완료, 모델 요청 0)을 잇는 Part 6 네 번째 챕터입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본 28개, 392KB — 원본과 `cmp` 모두 같음) · `gates-before.json`(`f86992b4…`) · `before-manifest.json`(131개, `ab149cd5…`) · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch24-human-in-the-loop`.
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(전부) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 과정 요약(전부) · 계약 파일(§3 Ch 20~23 줄 · §4 Ch 16~23 줄 · §5 Ch 16~23 줄 · §8) · Ch 23 `chapter-summary.md`(전부)·`chapter-lead-notes.md`·`before-manifest.json` · Ch 17 02·03·Ch 19 06·Ch 22 `_src`의 사람 확인·승인 문장 · 뒤 챕터(Ch 25·27·28·30) `_src`의 Ch 24 문장 · 공용 옛 생성기 · Part 6 목록·묶음·검사 스크립트 · `ch24-technical-review.md`·챕터 `qa/research.md`·`verification.md`·`집필점검표.md`. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.
- **원고·노트북·그림은 하나도 고치지 않았습니다.** 연결 폴더 안 파일 삭제 0건, 노트북 실행 0건, 모델·임베딩 호출 0건(이 챕터는 원래 모델을 부르지 않음). 확인은 모두 기기 `/tmp/ch24-prep/exp/`의 작은 그래프(`e1.py`~`e6.py`, `env -u OPENAI_API_KEY`)와 설치판 소스·공식 문서로 했습니다.
- `chapter.json` `hours` = 「총 8h · 강의 3h · 실습 5h」. 절 meta 합 강의 1+1+1 = **3h**, 실습 1.5+1.5+2 = **5h** → 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part6/_build_index.py` 22행 (3, 5)·`qa/check_scope.py` `EXPECTED` (3, 5)도 같습니다. 새 용어 meta 3+3+3 = **9**(옛 생성기 목록: 01 `interrupt`·승인 게이트·중단 상태 / 02 `Command`·`resume`·재개 값 / 03 상태 기록·time travel·분기).

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-25)

| 절 | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 interrupt 승인 게이트 | 4 | 77 | 3 | 4 | 0 | 0 | 5 | 18 | 3 | 33 |
| 02 Command resume으로 실행 재개 | 4 | 79 | 0 | 3 | 0 | 0 | 5 | 16 | 3 | 27 |
| 03 상태 기록과 다른 분기 재실행 | 5 | 81 | 3 | 0 | 0 | 0 | 5 | 22 | 3 | 33 |
| **합계** | **13** | **237** | **6** | **7** | **0** | **0** | **15** | **56** | **9** | **93** |

- 통과 절 **0/3**. 코드 줄(`count_code.py`) 50·32·43 = **125줄**.
- G1 6 = 제너레이터 식 3(01 c4 경로 둘 · 03 c8 `next(item for …)`) · 조건 표현식 1(01 c6 `"approved" if approved else "rejected"`) · 내포식 1(03 c8 기록 출력) · 셀당 함수 둘 1(03 c4 `quote`·`discount`).
- G2 7 = 15줄 넘는 셀 3(01 c4 17줄 · 01 c8 18줄 · 02 c4 20줄) · 한 글자 이름 `p` 2(01 c4) · 호출 두 겹 넘음 2(02 c8 `len(list(graph.get_state_history(config)))`).
- G3 0 — 그러나 셀마다 첫 줄 주석 한 줄뿐(옛 생성기 `CODE_COMMENTS`), 이유 주석 0.
- **G4 0은 모델 셀이 없어서입니다**(세 절 모두 모델·임베딩 요청 0, 키 셀 0).
- G5 15 = 절마다 제목 셀·핵심 그림 첨부 없음 6 + 결과 읽기 인용 없음 6 + 마지막 코드 셀 뒤 결과 읽기 없음 3(결과 읽기 셀 자체가 0).
- G6 56 = 70자 초과 17 · 영문으로 시작해 조사가 붙은 문장 39. 금지어는 G6가 대부분 세지 않습니다(§1 표).
- G7 9 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 것 (AST로 따로 셈, `/tmp/ch24-prep/ast_scan.py`)

- **f-string**: 변수만 1(02 c4 `f"허용하지 않는 값: {decision}"`) · 계산 1(03 c4 `f"discount:{state['rate']}"`). Ch 13~23은 f-string 0건.
- **타입힌트**: 노드·도움 함수 모두 매개변수·반환 힌트(`unsafe_node(state: State) -> dict`·`write_effect(request: str) -> None`·`review`·`quote`·`discount`). 상태 형식 칸 `trace: list[str]`(03). Ch 13·20·23 노드는 힌트 0.
- **클래스**: `class State(TypedDict)` 셋(01·02·03, 칸만 — Ch 13 L5 범위). 세 노트북 모두 이름이 `State`이고 칸이 다름 → Ch 13·23 규칙 「칸 구성이 바뀌면 새 이름」과 다름.
- **그 밖**: 집합 `{"approve", "reject"}`(02 — 과정 `set` 0건) · 딕셔너리 풀기 `{**prompt, "error": …}`(02 — 처음 쓰면 한 문장) · `while True`(02, §2-3·공식 문서와 충돌 §5-2) · `[Path.cwd(), *Path.cwd().parents]` 별표 풀기·`next(…)`(01 — 규격 §2-3 금지 모양) · `Path`·`Path.open`·`unlink(missing_ok=True)`·`read_text().splitlines()`(01 — Ch 23은 `os.path`) · 숫자 밑줄 `10_000`(03) · 식 안 숫자 `(1 - state["rate"])`·`int(…)` 잘라 내기(03) · 노트북 `.get("step")`·`reversed()`(03 — Ch 23 01은 `metadata["step"]`) · `assert A and B` 셋.

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청 | 파일 쓰기 | 손 값 | 금지 문법(셀) | 금지어(`_src` 본문/노트북 md/코드 주석) | `assert`(무엇에) |
|---|---|---|---|---|---|---|---|
| 01 (paired) | 되돌리기 어려운 일(파일 쓰기로 흉내) 앞에 `interrupt`를 두어야 거절이 쓰기를 막는다 · Before `unsafe_node`: 쓰기 → `interrupt` → 거절(`Command(resume=False)`)에도 `transfer-local` **두 줄**(첫 실행 + 다시 실행된 노드) · After `safe_node`: `interrupt` → 거절이면 쓰기 없음, 파일 없음 · b7 멱등성(Ch 23 06)·try/except 금지 | 0 | **실습 폴더 맨 위 `approval-effects.txt`**(`lab / …`, 글자 파일) + 두 번 `unlink` | 요청 `transfer-local` · 질문 `승인합니까?` · 스레드 `unsafe`/`safe` · 답 `False` | c4 제너레이터 둘·`p` 둘·17줄·힌트·`Path` · c6 조건 표현식·힌트 · c8 18줄·힌트 | 반환 10/2/0 · 경로 7/1/0 · 런타임 2/1/0 · 직렬화 3/0/0 · payload 4/1/0 · 분기 1(b9) · 재시작 1(b3, Ch 23 06 제목 말) · 재실행 1 · 적절 1/1 · HITL 0/0/1 · **제목 「interrupt」·「게이트」** | 1 — `rejected["status"] == "rejected" and not effect_path.exists()`(결정적) |
| 02 (experiment) | 답이 허용 목록(`approve`·`reject`) 밖이면 오류를 담아 다시 묻는다 · 노드 안 `while True` + `interrupt` · `maybe` → 둘째 질문에 `error` · `approve` → `decision` 저장·`next ()` · `history count: 3` | 0 | 없음(`InMemorySaver`) | 요청 `publish-local` · 스레드 `review-2402` · 답 `maybe`·`approve` | c4 20줄·집합·풀기·`while True`·f-string·힌트 · c8 호출 두 겹 | 반환 9/0/0 · 검증 5/2/1 · payload 3/2 · 런타임 1/1 · 스키마 1/1 · 포인터(단독) 1 · 정확히 1 · 소비 1 · 분기 1 · 경로 1 · **제목 「Command」·「resume」·「재개」** | 2 — `"error" in second[…].value` · `decision == "approve" and next == ()`(결정적) |
| 03 (experiment) | 끝난 실행의 기록에서 `next == ("discount",)`인 체크포인트를 골라 `update_state`로 `rate` 0.1 → 0.2 → `invoke(None, fork_config)` → 원본 `9000` 그대로·새 실행 `8000`·`trace ['quote', 'discount:0.2']`(quote 다시 실행 안 됨) | 0 | 없음(`InMemorySaver`) | 기본 가격 `10_000` · 할인율 0.1/0.2 · 스레드 `price-2403` | c4 함수 둘·f-string 계산·힌트·`list[str]` · c8 제너레이터·내포식·`.get`·`reversed` | **분기 20/8/1** · 반환 8/2 · snapshot 6/1 · trace 6/1 · time travel 4/1 · fork 4 · 경로 3/2 · 보상 4/1 · 격리 3/1 · reducer 1/1 · 파라미터 1 · 프롬프트 1/1 · 임계값 1/1 · 시나리오 1 · 재실행 1/2 · **제목 「분기」·「재실행」** | 3 — `final_price == 9000` · `== 8000`(결정적) |

- **서비스 요청 합계 0.** 노트북 `%pip`은 세 절 모두 `langgraph==1.2.11` 한 줄. 실습 폴더 dev에 `pip==26.2`, 잠금에 `pip 26.2` 있음(규격 §7-2 조건 충족).
- **`temperature=0`·`reasoning_effort="none"`**: 모델 셀이 없어 해당 없음. **걸린 시간·비용**: 어느 절도 재지 않음. 그런데 01 b5 「읽기 전용 검색까지 매번 승인받으면 흐름만 느려질 수 있으므로」는 재지 않은 속도 단정(규격 §3).
- **옛 그림 토큰**: 절마다 b4 「도식 읽기」의 `{{svg:NN-흐름}}` 하나(`figures/_gen_figures.py`가 `textbook/part5/_figure.py`로 만든 상자 넷 흐름도). 노트북 토큰 01 `{{notebook:…|example}}`+`{{notebook:…|failure}}` · 02·03 `{{notebook:slug}}`. Mermaid·삽화 0장.
- 노트북 `metadata.verification`: 셋 모두 `passed`, 실행일 **2026-09-10**(16:18 UTC). `code_sha256` 앞 12자 01 `718171990c5d` · 02 `52b2eff6d632` · 03 `6abb33a294bc`. 파일 해시 `74e0176d…`·`b787cf03…`·`fcf438dc…`(`part6-practice.zip`·`llm-practice.zip` 안 판과 같음). 셀 수 9·9·11, 01만 `lesson_part`(example/before/after).
- 노트북 설명 셀: 제목 + 한 줄 · 「실행 환경 준비」 · 소제목 + `_src` b4·b5 둘째 단락과 같은 글(옛 도구 `part6a_enrich.py`가 끼움) · **결과 읽기 셀 0**, 「이 노트북에서 할 일」·준비물·실행일 문장 없음, 셀 첨부 그림 0.
- `_src` 틀(옛 생성기 한 틀): b5 「확인할 점」 = b6 둘째 단락(같은 글 두 번) · b9 복습 넷 · **b10 참고 자료 넷이 세 절 모두 같음**(Persistence · Interrupts · Time Travel · LICENSE, 확인일 2026-09-14).

## 2. 절별로 더 봐야 할 것

### 01 interrupt 승인 게이트
- Ch 23 07 b8이 이 절 슬러그를 링크(`../ch24-human-in-the-loop/01-interrupt-승인-게이트.html`, Ch 23 `author_07.py` 574행 `L_CH24_01`)하고 「되돌리기 어려운 일을 하기 전에, 사람이 확인하는 자리에서 그래프를 멈추는 방법」이라고 소개 → **슬러그 고정**, 장면(부작용 앞에서 멈춤)도 지켜야 참.
- **묶음 실행 검사 대상**(§4-2) — 키·모델 셀을 넣으면 멈춤.
- 파일 쓰기가 실습 폴더 맨 위에 남고(`approval-effects.txt`, 묶음 목록 밖), c8이 **이미 있는 파일을 `unlink`**합니다. 이 기기 연결 폴더는 삭제가 막혀 있어 제자리에서 실행하면 그 줄에서 멈출 것으로 보입니다(도구 설명 기준, 실행 확인 안 함). Ch 23처럼 임시 폴더로 옮기면 둘 다 풀립니다.
- b3 「Ch23에서 노드는 장애 뒤 처음부터 재시작될 수 있고 외부 쓰기에는 멱등성이 필요하다」는 Ch 23 06·07로 **참**(「재시작」은 Ch 23 06 제목 말 — 본문은 「다시 실행」). 「체크포인터는 InMemorySaver」도 Ch 23 01로 이어짐.
- b7 「interrupt를 try/except로 감싸면 …」은 실행하지 않은 문장 → 설치판에서 **확인됨**(`except Exception`이 `GraphInterrupt`를 받아 노드가 `caught GraphInterrupt`로 끝나고 `next ()` — `GraphInterrupt` → `GraphBubbleUp` → `Exception`, e2). 노트북에 실패 장면으로 넣을 수 있음.
- Ch 17 02가 이미 정의한 **「승인 지점」**(부작용이 생기는 단계 앞에서 사람이 확인하는 자리)과 이 절 「승인 게이트」가 같은 뜻 · Ch 18 01 「게이트」(단계 사이 코드 검사)와 말이 겹침(§9-4).

### 02 Command resume으로 실행 재개
- **공식 문서(2026-09-25 확인)와 충돌**: 「Do not loop `interrupt` calls using logic that isn't deterministic across executions, including `while True` validation loops. Use a conditional edge instead.」 — 권장 모양은 노드에서 `interrupt()`를 **한 번만** 부르고 오류를 상태에 담아 조건부 엣지(Ch 13 03)로 되돌아가는 것. 지금 02는 그 `while True` 모양 그대로입니다.
- 설치판 관찰(e2): `while True` 판은 다시 묻기 한 번마다 노드 전체가 처음부터 돌며 앞선 답을 차례로 다시 받습니다 — 노드 호출 1 → 2 → 3 → 4, `interrupt` 호출 누적 1 → 3 → 6 → 9. 체크포인트는 멈춰 있는 동안 **2 그대로**(다시 물어도 늘지 않음), `approve` 뒤 3 → 지금 출력 `history count: 3`은 참. 조건부 엣지 판(e5)은 노드 호출 1 → 3 → 4, 체크포인트 2 → 3 → 4, 마지막 `next ()`.
- b5 「새 ID로 resume을 보내면 기존 interrupt에 값이 전달되지 않습니다」 → 설치판에서 **다른 스레드에 `Command(resume="approve")`를 보내면 노드가 빈 상태로 실행돼 `KeyError: 'request'`**(e2, 오류 글이 친절하지 않음). 끝난 스레드에 다시 보내면 오류 없이 상태 그대로.
- 결정적 실패 장면 후보(e5·e6): 체크포인터 없이 `Command(resume=…)` → `RuntimeError: Cannot use Command(resume=...) without checkpointer`(체크포인터 없이 첫 `invoke`는 오류 없이 `__interrupt__`만 냄) · 같은 단계 두 노드가 동시에 멈춘 뒤 값 하나로 재개 → `RuntimeError: When there are multiple pending interrupts, you must specify the interrupt id when resuming.` → `Command(resume={id: 값, …})`로 풀림.
- 「같은 `thread_id`는 기다리던 실행을 찾는 포인터」(포인터), 「정확히 대응」, 「소비」, 「스키마」 — 금지어·어려운 말.

### 03 상태 기록과 다른 분기 재실행
- 설치판(e3): 원본 실행 뒤 체크포인트 **4**(단계 -1·0·1·2) · `update_state(before.config, {"rate": 0.2})`는 **원천 `update`, 단계 2, 부모 = 고른 체크포인트**인 새 체크포인트를 만들고 그 설정을 내놓음 · `invoke(None, fork_config)` → `quote` 호출 1 그대로, `discount` 한 번 더, 체크포인트 +2 · **스레드 설정으로 `get_state`하면 가장 최근 줄(8000)**이 나오고 원본 9000은 따로 보관한 설정으로만 읽힘.
- **다시 실행(replay, 값을 안 바꾸고 옛 설정으로 `invoke(None, 옛 설정)`)**: 설치판은 원천 **`fork`** 체크포인트를 새로 만들고 그 뒤 노드를 **다시 실행**합니다(`discount` 호출 +1, 체크포인트 +2 — `pregel/_loop.py` 952~971행: 「save a fork checkpoint so the replayed execution creates a new branch」). 공식 문서 Time Travel은 「Replay re-executes nodes—it doesn't just read from cache」·「Interrupts are always re-triggered during time travel」(설치판 e4에서 확인 — 고른 자리 뒤의 `interrupt` 노드가 다시 멈춤).
- b5 「reducer가 있는 상태 키를 update하면 … 누적」 → 설치판에서 확인됨(`operator.add` 칸 `['a']` + `["edited"]` → `['a', 'edited']`, e4) — 노트북에서는 실행 안 함. b7 `as_node` → 확인됨(`as_node="gate"`면 다음 노드가 `('pay',)`) — 실행 안 함. b7 「LLM 호출, API 요청 … 다시 실행」은 모델 없는 절이라 실행 안 함.
- **소수 잘라 내기 함정**: `int(10000 * (1 - rate))` — 0.1·0.2·0.29는 9000·8000·7100이지만 **0.33은 6699**(6699.999…를 잘라 냄). 「값 바꿔 보기」에서 학생이 다른 값을 넣으면 틀려 보임 → 정수 백분율(`… * (100 - 할인율) // 100`)이나 정해 둔 값 표로.
- 「분기」가 본문 20·노트북 8·주석 1(Ch 13 금지어 → 「갈래」, 그러나 「갈래」는 Ch 13 조건부 엣지 뜻 §9-4) · 「time travel」·「fork」·「snapshot」·「reducer」(→ 리듀서, Ch 13 말) · b7 「보상 작업」은 Ch 23도 다루지 않은 Ch 31 몫.
- b8 「Ch25에서는 저장된 실행에서 상태·메시지·사용자 정의 진행 상황을 스트리밍합니다」 — 실습 절을 붙이면 04로 고칠 자리.

## 3. 실습 폴더 구조와 읽는 곳

```
labs/part6/ch24-human-in-the-loop/
  README.md (두 줄 — 「승인 결과는 실습 폴더의 로컬 파일에만 기록」)
  pyproject.toml   uv.lock (81항목)
  notebooks/01~03-*.ipynb
  .venv/ (macOS 판 125MB — home = /Users/…/cpython-3.12-macos-aarch64-none, uv 0.11.6)
  (없음: data/ · runs/ · tests/ · 도구 파일 · 체크포인트 파일 · worker · 노트북 생성기)
```

- **노트북이 쓰는 파일**: 01 `approval-effects.txt`(실습 폴더 맨 위, 셀 [4]·[8]에서 `unlink`) 하나. 02·03은 메모리 체크포인터라 파일 0. SQLite 없음 → 연결 폴더 SQLite `disk I/O error`(Ch 23 발견)는 지금 판에는 해당 없음(SQLite를 쓰게 바꾸면 해당).
- **Ch 24 파일을 코드로 읽는 곳**(`grep`, `textbook`·`labs`, `.venv`·`before`·zip 제외):

| 자리 | 무엇을 | 성격 |
|---|---|---|
| `textbook/part6/qa/check_bundle_execution.py` 29~31행 | **01 노트북을 묶음에서 키 없이 실행**(`code_sha256` 대조) | **계약**(§4-2) |
| `textbook/part6/public-files.json` 39~44행 | 실습 파일 여섯(README·노트북 셋·`pyproject.toml`·`uv.lock`) | 묶음 허용 목록 |
| 챕터 `qa/public-files.json` | HTML 4 + 옛 SVG 3 + 실습 파일 6 = 13(경로 배열) | `collect_public_files.py`가 Part 목록으로 모음 |
| `textbook/downloads/part6-practice.zip`(`aa82b386…`)·`llm-practice.zip`(`f2d2008a…`) | Ch 24 여섯 파일이 디스크와 같음 | 묶음 |
| `textbook/part6/_build_index.py` 22행 · `textbook/_notebook/build_index.py` 52행 · `build_bundle.py` 24행 | (3, 5, 「승인 시점에 중단·재개하고 과거 상태에서 다른 분기를 실행합니다.」) · (절 수 3) · 공개 챕터 목록 | 실습 절을 붙이면 3 ≠ 4(`_notebook/build_index.py`는 선례대로 전체 마감 몫) |
| Part 6·7 선행 목록(`prerequisite-files.json`) | **Ch 24 줄 0** | 뒤 챕터가 Ch 24 파일을 쓰지 않음 |
| Part 7 `check_bundle_execution.py` | Part 7 챕터만(Ch 24 안 봄) | — |
| 옛 검사(고치지 않음, 기록만) | `check_scope.py` `EXPECTED` (3,5)·`SECTION_COUNTS` 3(실습 절을 붙이면 멈춤) · `check_notebook_readiness.py` `assert len(reports) == 47`(이미 50 — 결과 파일을 먼저 씀 → 되돌림 선례) · `check_figures.py`(SVG마다 `.excalidraw` 짝) · `check_visual_reports.py` · `check_delivery.py`(`llm-practice.zip` 신선도) | Ch 21~23 선례대로 이미 어긋난 상태 |
| 기록만 | `final-artifact-hashes.json`(Ch 24 줄 24 — **노트북·`_src`·HTML 줄은 이미 옛 해시**) · `notebook-executions.json`·`notebook-readiness.json`·`figure-consistency.json`(각 3) · `visual-results.json`(8) · `lesson-scope.json`·`prose-repetition-initial.json`·`bundle-execution.json`(1) · `ch24-technical-review.md` · `language/ch24-final.{json,md}`·`ch24-source-{before,after}.sha256`·`ch22-ch24-code-output-figure-*.sha256`·`originals/ch24/` · Part 7 `existing-artifacts-before.json`(6)·`before-integration/build_*.py` · `_notebook/checks/notebook-contracts-part6-ch24-human-in-the-loop.json`(verify가 다시 씀)·`checks/ch24-human-in-the-loop/`(옛 화면 검사) · `existing-artifact-hashes.json`에는 Ch 24 줄 0 | — |

- **옛 생성기**:

| 파일 | 무엇을 씀 | 비고 |
|---|---|---|
| **`textbook/part6/ch23-persistence/qa/author_ch23_ch24.py`**(711줄, `44c9d593…`, Ch 23·24 공용) | `write_all()` — **Ch 24 노트북 셋**(출력 없이 — `lab/…` 파일 쓰기 판) · **Ch 24 `_src` 셋** · **Ch 24 `figures/_gen_figures.py`**(지금 판과 다른 글 — 순환 색 배정 판). Ch 23 쪽은 Ch 23 01절이 넣은 두 줄로 건너뜀 | 지금 돌리면 Ch 24의 현재 노트북·`_src`(09-14 `part6a_enrich.py`가 더한 b4·b5 단락 포함)를 옛 판으로 덮어씀. **부르는 스크립트 0**(`grep` — 기록 문서만). 사본 `before/generators/author_ch23_ch24.py` |
| `figures/_gen_figures.py`(Ch 24, `ced25fb2…`) | `NN-흐름.{svg,excalidraw,caption.md}` 9개(`textbook/part5/_figure.py`) | 옛 그림 세 벌. 사본 `before/generators/`·`before/figures/` |
| (챕터 밖) `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6a_enrich.py` 193~220행 | Ch 24 세 절 `_src` b4 「코드를 읽는 순서」·b5 「다른 상황과 적용 경계」와 노트북 설명 셀 | 기록만(Ch 21·23 선례) |
| `textbook/part6/_author_ch21_ch29.py` | **Ch 24 안 씀**(`grep` 0) | — |

→ 공용 생성기의 Ch 23 쪽은 이미 아무것도 쓰지 않으므로, **파일 첫머리에 설명 주석 + `raise SystemExit(...)`를 넣어도 Ch 23에 영향 없음**(Ch 23 파일은 `qa/upgrade/author_NN.py`가 씀). 파일 자리가 Ch 23 `qa/` 안이라 수정·이동이 챕터 밖 파일 수정이지만 Ch 23 요약 §13-6·§16-1과 계약 §5·체크리스트 §2-11이 **Ch 24 몫으로 넘김**: Ch 24 작업 뒤 `mv -n` → `textbook/part6/ch23-persistence/qa/upgrade/before/generators/blocked/`(이미 Ch 23 `_gen_figures.py`가 있는 폴더). 옮기면 Ch 23 `before-manifest.json`·계약 문서가 가리키는 옛 자리가 비므로 기록에 한 줄. Ch 24 `figures/_gen_figures.py`는 Ch 24 마감 때 `mv -n` → `qa/upgrade/before/generators/blocked/`(Ch 23 선례).

- **판**: `requires-python = ">=3.12,<3.13"`, `dependencies = ["langgraph==1.2.11"]`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`, `[tool.uv] package = false`. 잠금 주요 판: `langgraph-checkpoint 4.2.0`·`langgraph-prebuilt 1.1.0`·`langgraph-sdk 0.4.4`·`langchain-core 1.6.2`·`pydantic 2.13.5`·`langsmith 0.12.4`. **`langchain`·`langchain-openai`·`openai`·`python-dotenv`·`numpy`·`langgraph-checkpoint-sqlite` 없음**.
- **Ch 23 잠금과 견줌**: 겹치는 판 **모두 같음**(`langgraph 1.2.11`·`langgraph-checkpoint 4.2.0`·`langgraph-prebuilt 1.1.0`·`langchain-core 1.6.2`·`pydantic 2.13.5`·dev 넷). Ch 23에만 SQLite·Postgres 체크포인터·psycopg. Ch 21·22·25 잠금에는 `langchain 1.4.0`·`langchain-openai 1.6.0`·`openai 3.11.0`·`python-dotenv 1.2.3`(Ch 22는 `pip` 없음).
- `pytest`·`tests/` 없음. 실습 폴더 `.venv`는 macOS 판(삭제 승인 대상).

## 4. 앞뒤 챕터 이음새

### 4-1. Ch 23 인계(요약 §13·§14·§15, 계약 §3 Ch23 줄) 항목별 지금 상태

| 인계 항목 | 지금 Ch 24 원고 | 상태 |
|---|---|---|
| 01 b3 「노드는 장애 뒤 처음부터 재시작 … 멱등성」 | 그대로 | 참(06·07) — 「재시작」은 Ch 23 06 제목 말 |
| 「체크포인터는 InMemorySaver」 | 01~03 모두 `InMemorySaver` | 참(Ch 23 01) |
| 모델 답·에이전트 그래프 저장 없음 | 세 절 모두 모델 없음 | 어긋남 없음(모델을 넣으면 Ch 24가 처음) |
| `interrupt`·`Command(resume=)`·`update_state`·시간 여행·`stream` 0건 | 세 절이 처음 가르침(`stream` 안 씀) | 맞음 — 단 `Command` 자체는 **Ch 13 06**이 `Command(update=, goto=)`로 가르침 → 「Ch 13 06절의 `Command`에 `resume` 칸」으로 이을 수 있음 |
| **`resume` 말 세 장면**(03 스레드 재개 · 04·06 worker `resume` 단계 · Ch 24 `Command(resume=)`) | 01 b3에 구분 문장 없음. **제목 「실행 재개」·본문 「재개」 01 11번 · 02 10번** | **미해결** — Ch 23 03 `_src` 13행이 「Ch 24에서 사람의 확인을 받아 멈춘 실행을 다시 움직이는 일과는 다른 장면」이라고 이미 약속 → Ch 24 첫 자리에 03과 다르다는 한 문장 + 본문 말을 「재개」 말고 따로(§9-4) |
| 「이어 실행」 = Durable Execution 한 뜻(멈춘 실행을 저장된 자리부터 이어 감) | 없음 | `interrupt` 뒤 이어 가기도 글자 뜻으로는 들어맞음 — 「답 값을 넣어 이어 간다」로 가를지 정할 것 |
| 체크포인트 수는 우리 그래프 값 | 02 `history count: 3`, 03 목록 넷 | 이 챕터 그래프 값으로만 쓰면 됨(§2) |
| 07 이어 가기 = 실패 흉내 뒤 `invoke(None, config)` | 03이 `invoke(None, fork_config)` | Ch 23 05·07 말로 이을 수 있음 |
| 멱등 키는 한 커널 안에서만, 보상 작업 없음 | 03 b5·b7 「보상 작업이나 격리」 | Ch 23도 안 함 — 「실행하지 않았습니다」로 |
| `new_prefix`는 Ch 23 도구 파일에만 | — | Ch 24가 파일 이름 앞머리가 필요하면 옮겨 와야 함 |
| 공용 옛 생성기 이동 | — | Ch 24 몫(§3) |
| Ch 24 01에 있는 「경로」·「런타임」·「반환값」 | 01 경로 7·런타임 2·반환 10 | Ch 24 몫(§1) |

- **Ch 23 도구 파일 `checkpoint_tools.py`**(`a850b2cd…`)는 **맨 위에서 `from langgraph.checkpoint.sqlite import SqliteSaver`**를 가져와 Ch 24 잠금(SQLite 체크포인터 없음)에서는 import 자체가 멈춥니다. 쓸 만한 함수: 06 `append_key`·`append_key_once`(01의 「interrupt 앞 쓰기는 멱등하게」를 실행으로 보일 때) · 04 `read_record`(기록 파일 줄 읽기). 규격 §2-7 3번대로 Ch 24 도구 파일에 **같은 본문으로 옮기고 `# Ch 23 NN절에서 배웠습니다`**.
- **Ch 23 01 노트북 함수 `print_history(history)`**(단계 번호·만든 자리·다음 노드·칸 값 한 줄씩 — 도구 파일에는 없음)가 03의 기록 출력과 같은 일 → 옮겨 올 후보. 03이 `metadata.get("step")` 대신 Ch 23 01 모양 `metadata["step"]`·`["source"]`를 쓰면 원천 `input`·`loop`·`update`·`fork`가 그대로 보임.
- **Ch 21 `runner_tools.py`·Ch 19·20 함수**(`tool_call_names`·`show_messages`·`sum_usage`·`estimate_cost`)는 모델·도구 장면을 넣을 때만 후보(§7).
- **「사람 확인」 말과 「승인」 말**: Ch 17 02 **승인 지점**(부작용이 생기는 단계 앞에서 사람이 확인하는 자리 — 정의된 말) · Ch 17 03 **사람 확인**(정지 조건 넷 가운데 하나 — 부작용 도구를 모델이 고르면 부르기 전에 반복을 **멈추고 사람에게 넘김**, 이어 가기는 없음 — Ch 17 요약 152행 「사람 확인 뒤 이어 가기 … 없습니다」) · Ch 19 06·07 **사람 확인 값**(`person_confirmed` 참/거짓 — 확인 전에는 쓰기 도구를 모델에게 알리지 않음, 비유 「걸쇠 건 서랍」). → Ch 24는 **사람 확인 뒤 멈춘 실행을 이어 가는 첫 챕터**. 01에서 「Ch 17 02 승인 지점을 그래프 안에 둔다」·「Ch 17 03은 멈추고 끝났지만 이 절은 답을 받아 이어 간다」로 이을 수 있음.
- **Ch 22 Middleware**: 사람 승인 미들웨어(`HumanInTheLoopMiddleware`) 언급 **0건**(`_src`·노트북 `grep`). Ch 22 03 b7 「승인 여부나 금액처럼 틀리면 안 되는 값은 요약에 맡기지 말고」 한 곳뿐(관계 없음).

### 4-2. 묶음 실행 검사 계약 (Part 6 `check_bundle_execution.py`)

- 하는 일: `part6-practice.zip`을 임시 폴더에 풀고 **Ch 24 01**과 Ch 28 01만 → 실습 폴더에서 `uv sync --locked` → `uv run --project <lab> --with nbclient==0.11.0 --with python-dotenv==1.2.3 python textbook/_notebook/execute.py <노트북> --cwd <lab>/notebooks --kernel-python <lab>/.venv/bin/python` → `assert after['status'] == 'passed' and after['code_sha256'] == original`(zip 안 노트북 `metadata.verification.code_sha256`과 새로 잰 값). 결과를 `textbook/part6/qa/bundle-execution.json`에 씀(지금 `f53987e8…`, 01 `code_sha256` `718171990c5d…`·4셀 PASS, 2026-09-25 Ch 23 마감 때).
- **01에 모델 요청·키 셀을 넣으면 멈춤**: 풀린 묶음에 `.env`가 없고(Part 7 검사는 `.env`가 없음을 `assert`), Ch 24 잠금에 `langchain`·`langchain-openai`가 없어 `uv sync --locked` 판에서 import가 실패. 검사가 `--with python-dotenv`를 주므로 **`dotenv` import만은 검사에서 통과하고 학생 `.venv`에서는 실패**하는 틈이 있음(주의).
- 01이 **도구 파일을 가져오면** 그 파일이 Part 목록에 들어가고 zip을 다시 만든 뒤라야 통과(커널 시작 폴더가 `notebooks/`라 찾음). `%pip` 셀은 네트워크와 잠금의 `pip`이 필요(있음).
- **개선 뒤 기록 갱신(Ch 20 03 선례, Ch 21·23 마감과 같은 방법)**: 01 새 커널 실행 → 챕터·Part 공개 목록 → `python3 textbook/part6/_build_index.py`(zip 다시 만듦) → `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache UV_LINK_MODE=symlink python3 textbook/part6/qa/check_bundle_execution.py`(스크립트 수정 0) → `bundle-execution.json` 새 해시·01 새 `code_sha256`을 챕터 요약·계약 §5에 적음. 01은 **모델·키 없이** 두는 것이 계약.

### 4-3. 완료 챕터가 Ch 24에 기대는 문장 — 개선 뒤에도 참이어야 함

| 자리 | 문장 | 조건 |
|---|---|---|
| Ch 23 07 `_src` 39행 b8(+ HTML·노트북 마지막 셀·`author_07.py` 562·574행) | 「Ch 24 01절에서는 되돌리기 어려운 일을 하기 전에, 사람이 확인하는 자리에서 그래프를 멈추는 방법을 다룹니다」 + 01 슬러그 링크 | 01 슬러그·장면 유지 |
| Ch 23 03 `_src` 13행(+ HTML·`author_03.py` 635행) | 「Ch 24에서 사람의 확인을 받아 멈춘 실행을 다시 움직이는 일과는 다른 장면입니다」 | Ch 24가 그 장면을 가르침 |
| Ch 23 `author_06.py` 25행 | 결정 3 「함수 이름에 Ch 24 API 이름 interrupt를 쓰지 않는다」 | 기록 |
| Ch 17·19·20·21·22 `_src` | Ch 24 언급 0 | — |

### 4-4. 뒤 챕터(대기)가 Ch 24에 기대는 문장 — 고치지 않음

| 자리 | 문장 | Ch 24가 지켜야 할 것 |
|---|---|---|
| Ch 25 01·02·03 `_src` b3(+ `textbook/part6/_generate_ch25_ch26.py`) | 「Ch24에서 interrupt와 재개 사건을 확인했습니다」 | `interrupt`·이어 가기 장면(스트리밍은 Ch 25 몫 — Ch 24는 `stream` 안 씀) |
| Ch 27 01 `_src` b3 | 「Ch 24는 사람 승인을」 | 참 |
| Ch 27 08 `_src` b3·복습 3 | 「Ch 24의 사람 승인과 이 장의 permissions는 **도구 실행 경계**를 다룹니다」·「interrupt는 체크포인터와 승인 처리를 구성했을 때 사람의 결정을 기다립니다」 | **Ch 24에 도구 호출 승인 장면이 없음** → 지금은 부분 참(작업 경계 수준). 도구 승인 장면을 넣을지와 관련(§7) |
| Ch 28 03 `_src` b3 | 「Ch24에서 사람이 승인해야 하는 작업 경계를 확인했습니다」 | 참 |
| Ch 30 06 `_src` b3(+ `_generate.py`) | 「Ch23의 thread 분리와 **Ch24의 중복 실행 방지 원칙**」 | 01 b7·정리의 「interrupt 앞 쓰기는 멱등하게」를 남겨야 참 |
| Part 6 `_src/index.html`·`practice-start.md` | 「Ch 23과 Ch 24는 저장한 상태로 실행을 이어 가는 방법」·「저장·재개·승인을 실습」 | 참 |
| `labs/part6/continuity-guide.md` 9·10행 | 「Ch24 승인·상태 기록」·「Ch24 중단·재개, 과거 상태에서 분기」 | 참(「분기」 말 — 마감 때 볼지) |
| Ch 25~31 노트북·코드 | Ch 24 노트북·출력을 읽는 코드 **0** | 산출 파일 계약 없음 |

### 4-5. Part 6 묶음·목록·기록

- Part 6 선행 목록(`prerequisite-files.json`)·`existing-artifact-hashes.json`에 Ch 24 줄 **0**. `final-artifact-hashes.json` Ch 24 줄 24개는 옛 판(노트북·`_src`·HTML 해시가 이미 디스크와 다름 — 만드는 스크립트 없음, Ch 21·23 선례대로 기록만).
- 공개 목록 두 곳 + zip 두 개(§3). `llm-practice.zip`은 전체 마감 몫(Part 6 `check_delivery.py`가 Part 1 Stale에서 멈추는 알려진 상태).

## 5. 라이브러리 동작 — 설치판 소스와 모델 없는 확인 (2026-09-25, `langgraph 1.2.11`)

### 5-1. `interrupt`와 결과 모양(e1)
- 첫 `invoke` 결과 키 `['request', 'status', '__interrupt__']`, `__interrupt__` = `[Interrupt(value=…, id='…')]` — **`id`는 실행마다 다른 32자 글**(출력·인용 금지). 속성 `value`·`id`(`interrupt_id`는 사용 중단 경고).
- 멈춘 동안 `get_state(config).next` = `('gate',)`, `.tasks[0].interrupts` 1개, 칸 값은 입력 그대로, 체크포인트 **2**. `Command(resume=False)` 뒤 **3**(단계 -1 `input` · 0 `loop` · 1 `loop`).
- 쓰기 → `interrupt` 순서 노드는 호출 **2번**, 파일 **두 줄**(결정적, 두 번 실행 같음).
- 체크포인터 없이 첫 `invoke`는 **오류 없이** `__interrupt__`를 냄(e1·e6) → `Command(resume=…)`에서 `RuntimeError: Cannot use Command(resume=...) without checkpointer`. 설치판 독스트링 「To use an `interrupt`, you must enable a checkpointer」.
- `try/except Exception`으로 감싸면 `GraphInterrupt`를 받아 버림(e2) — 공식 문서 규칙과 같음.

### 5-2. 다시 묻기(e2·e5)
- `while True` 판: 노드 호출 1·2·3·4 / `interrupt` 호출 누적 1·3·6·9 / 체크포인트 2·2·2·3. 공식 문서 「Matching is **strictly index-based**」·「Do not loop `interrupt` calls … including `while True` validation loops. Use a conditional edge instead.」 · 권장 「call `interrupt()` **exactly once**, return from the node with the error message stored in state, and use a **conditional edge** to loop back」.
- 조건부 엣지 판: 노드 호출 1·3·4 / 체크포인트 2·3·4 / 둘째 질문 `{'request': 'publish', 'allowed': ['approve', 'reject'], 'error': '허용하지 않는 값: maybe'}`.
- 같은 단계 두 노드가 함께 멈춤 → 값 하나로 재개하면 `RuntimeError`(아이디 지정 요구), `Command(resume={id: 값})` 딕셔너리로 풀림.

### 5-3. 시간 여행(e3·e4)
- 기록은 최신 것부터(Ch 23 01과 같음), 스레드의 모든 줄이 한 목록에 섞임(원본 줄과 새 줄).
- `update_state` → 원천 `update` 체크포인트(단계는 고른 자리 + 1, 부모 = 고른 자리) · 칸에 리듀서가 있으면 이어 붙음 · `as_node`로 다음 노드가 바뀜.
- 옛 설정으로 `invoke(None, …)`(값 안 바꿈) → 원천 `fork` 체크포인트 + 뒤 노드 다시 실행. 공식 문서 Time Travel의 「Replaying … doesn't branch」 요약과 설치판(`fork` 체크포인트를 만듦)이 표현이 다름 → **설치판 출력 기준으로 쓰고 문서는 「다시 실행한다」까지만**.
- 고른 자리 뒤에 `interrupt` 노드가 있으면 새 줄에서도 다시 멈춤(e4 — `gate` 호출 +1, 새 금액 `30000`이 질문에 실림).
- `invoke` 인자에 `version`(`"v1"` 기본 / `"v2"`)·`durability`·`control`이 있음. 공식 문서는 HITL에 `stream_events(..., version="v3")`를 권하지만 `stream`은 Ch 25 몫 → Ch 24는 `invoke`의 `__interrupt__`(문서: 「The default `graph.invoke(...)` API still works and surfaces interrupts under `result["__interrupt__"]`」).

### 5-4. 사람 승인 미들웨어(참고, Ch 21 가상환경 `langchain 1.4.0`)
- `from langchain.agents.middleware import HumanInTheLoopMiddleware` 있음 — `HumanInTheLoopMiddleware(interrupt_on: dict[str, bool | InterruptOnConfig], *, description_prefix=…)`, 훅 `after_model`, 안에서 `interrupt(hitl_request)["decisions"]`, 결정 종류 `Literal["approve", "edit", "reject", "respond"]`. **Ch 24 잠금에는 없음**(쓰려면 `langchain`·`langchain-openai`·`python-dotenv`를 넣고 `uv lock`, 모델 필요). Ch 22는 이 미들웨어를 언급하지 않음.

## 6. 결정적 장면 가능성과 모델을 부를지

- **모델 없이 세 장면 모두 결정적**(e1~e5를 두 번씩 돌려 같음 — `Interrupt.id`·체크포인트 ID·시각만 다름, 출력하지 않으면 됨). 멈춘 값(질문 딕셔너리)·이어 간 뒤 값(`status`·`decision`)·고른 체크포인트에서 다시 실행한 값(9000·8000·`trace`)·호출 횟수·체크포인트 수·오류 이름 모두 노드 코드가 정함(Ch 23처럼).
- **모델을 부르면 흔들리는 자리**: (1) 모델이 고른 도구·인자(Ch 19 06 첫 응답 11번 중 1번 · Ch 17 29번 중 2번 다름) → 승인 질문 내용이 바뀜 · (2) **모델 호출을 `interrupt`와 같은 노드 앞에 두면 이어 갈 때 모델을 한 번 더 부름**(노드가 처음부터 다시 실행 — 사람이 본 질문과 다시 만든 질문이 다를 수 있고 요청 수가 늘어남) → 모델 노드와 승인 노드를 나눠야 함 · (3) 시간 여행으로 다시 실행하면 뒤 노드의 모델 호출이 새로 나감(문서 「may return different results」).

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **M1 모델 없음**(Ch 23처럼) | 세 절·실습 절 모두 노드가 만든 요청·질문·답 | 결정적 · 키 셀·잠금 변경 없음 · 묶음 검사 그대로 · 비용 0 | 규격 §3 「실제 모델 호출」과 다른 챕터가 둘째가 됨(강사 확인) · Ch 27 08 「도구 실행 경계」 부분 참 그대로 · 실습 절 요청 0(Ch 23 07 선례) |
| **M2 모델이 요청을 만들고 사람이 승인**(02·03 또는 실습 절만) | 모델 노드(Ch 19·21 설정)가 쓰기 요청(도구 호출 또는 요약)을 만들고, 다음 노드가 `interrupt`로 승인 · 01은 모델 없이 | 실무 모습(모델이 고른 쓰기를 사람이 막음) · Ch 17 03·Ch 19 06의 「사람 확인」을 이어 가기까지 완성 · Ch 27 08 문장 참에 가까움 | `uv lock`으로 `langchain`·`langchain-openai`·`python-dotenv` 추가(Ch 21 판) · 모델 선택 흔들림(§2-7 9·10번 절차) · 노드 나누기 필수 · 시간 여행 절은 다시 실행마다 요청 |
| **M3 `create_agent` + `HumanInTheLoopMiddleware`** | Ch 21·22 에이전트에 사람 승인 미들웨어 | Ch 21·22와 바로 이어짐 · 결정 넷(approve/edit/reject/respond) | 새 API(Ch 22가 안 가르침) · 설치판 소스 확인 필요 · 실습 절에는 새 API 금지라 01~03 가운데 한 절을 크게 바꿔야 함 · 모델 필수 |

- 모델을 넣어도 **01은 모델·키 없이**(묶음 실행 검사 계약).

## 7. §2-7 판단 근거 — 도구 파일

### 사실
- 지금 세 노트북은 함수를 서로 다시 쓰지 않음(01 `write_effect`·노드 둘 · 02 `review` · 03 `quote`·`discount`, 모두 노드 또는 한 번 쓰는 도움 함수).
- 앞 챕터에서 가져올 만한 함수: Ch 23 01 `print_history`(도구 파일 밖) · Ch 23 04 `read_record` · Ch 23 06 `append_key`·`append_key_once`(Ch 23 도구 파일 — Ch 24 잠금에서는 파일째 import 불가, §4-1).
- 실습 절(04)을 붙이면 01~03 도움 함수(질문 값 꺼내기·체크포인트 고르기·기록 출력·멱등 쓰기)를 다시 쓸 자리가 생김.
- 과정의 도구 파일 이름: `llm_tools`·`rag_tools`·`git_tools`·`data_tools`(Ch 4, 실습 폴더 맨 위)·`guardrails`·`agent_tools`·`workflow_tools`·`order_tools`·`graph_tools`·`runner_tools`·`checkpoint_tools`. **안 겹치는 후보**: `approval_tools.py`(가장 뜻이 드러남) · `review_tools.py` · `pause_tools.py` · `hitl_tools.py`(영문 줄임말이라 비권장). `labs/` 전체에 같은 이름 파일 0.

### 선택지 (결정하지 않음 — 장단점만)

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| A. 도구 파일 없음(Ch 2·4·6·22 선례) | 노드·도움 함수를 노트북마다 | 파일·묶음 목록 변경 없음 · 01 묶음 검사가 가장 단순 | Ch 23 함수를 옮겨 오면 규격 §2-7 3번(앞 챕터 함수는 노트북에 다시 적지 않음)과 충돌 · 실습 절에서 되풀이 |
| B. `approval_tools.py`에 앞 챕터 함수만 | Ch 23 01 `print_history`·04 `read_record`·06 `append_key`·`append_key_once`를 같은 본문으로 | §2-7 3번을 지킴 · 01 After/b7의 멱등 쓰기를 실행으로 보일 수 있음 | 01이 가져오면 묶음 목록·zip을 먼저 고쳐야 묶음 검사 통과 · 이름 공간 고정 문장 셋 |
| C. B + 이 챕터 도움 함수 | 01·02 질문 값 꺼내기, 03 체크포인트 고르기(`for`+`break` — `next(…)` 대신), 기록 한 줄 | 실습 절 코드가 가장 짧음 | 처음 가르친 절은 노트북에 남겨야 해서 절 사이 판이 둘 · 챕터 전체 코드가 줄어드는지 먼저 셀 것(`count_code.py`) |
| D. Ch 23 `checkpoint_tools.py`를 그대로 가져오기 | 실습 폴더 밖 파일 import 또는 잠금에 SQLite 체크포인터 추가 | 코드 0줄 | 챕터마다 파일을 따로 둔다는 선례와 다름 · 경로 문제 · SQLite 쓰기(임시 폴더 필수) |

## 8. 과정 규칙과 부딪히는 것 (선택지와 장단점만)

### 8-1. 모델 없는 챕터와 규격 §3 — §6 표.

### 8-2. 파일 쓰기 자리
- 지금 01만 파일을 씀(실습 폴더 맨 위, `unlink` 둘). Ch 23 결정: **파일은 임시 폴더에만**(`mkdtemp(prefix="chNN-MM-")` → `os.chdir` → `os.listdir()`, 일곱 절 같은 셀). 선택: (가) Ch 23 준비 셀 모양 그대로 `ch24-01-` — 학생 폴더에 파일이 안 남고 삭제 줄이 필요 없음, 01 경로 셀(`Path`·`next`·별표 풀기)이 통째로 빠짐 / (나) 실습 폴더에 두되 `unlink` 대신 실행마다 새 이름 — 연결 폴더 삭제 문제는 풀리나 학생 폴더에 파일이 쌓임. 02·03은 메모리 체크포인터라 파일 없음 — 01만 준비 셀을 둘지, 세 절 같은 모양으로 둘지.
- 실습 절에서 SQLite(Ch 23 03 체크포인터)를 쓰면 잠금에 `langgraph-checkpoint-sqlite==3.0.3` 추가 + 임시 폴더 필수(연결 폴더 `disk I/O error`).

### 8-3. 02 `while True`
- (가) 조건부 엣지 판으로 바꿈(공식 문서 권장·Ch 13 03 문법) — 출력 숫자가 바뀜(체크포인트 3 → 4, 노드 호출), 상태 칸 `error` 추가, 새 문법 0 / (나) `while True` 판을 **Before처럼 보이고** 조건부 엣지 판과 견줌 — 02가 experiment라 형식은 그대로 두되 「노드 호출·질문 호출 누적 1·3·6」을 실험 결과로 · (다) 그대로 두고 b7에 문서 규칙 — 설치판 동작은 맞지만 공식 규칙과 다른 코드를 학생에게 가르치게 됨.

### 8-4. 제목·용어
- **제목 말**(강사 확인 대상 후보): 챕터 「Human-in-the-Loop」·「Time Travel」 · 01 「interrupt」·「게이트」 · 02 「Command」·「resume」·「재개」 · 03 「분기」(Ch 13 금지어)·「재실행」. 슬러그: **01 고정**(Ch 23 07 링크) · 02·03은 들어오는 링크 0(Part 목차는 `_build_index.py`로 다시 만듦, 공개 목록·기록만) → 바꿀 수 있음.
- **말 정하기 후보**: `interrupt` → 「멈춤」·「멈춤 질문」(payload = 「질문 값」·「확인 요청」) · `Command(resume=…)` → 「답 넘기기」·「답 값」(Ch 23 03 「스레드 재개」·04·06 worker `resume`과 가르기) · 승인 게이트 → **Ch 17 02 「승인 지점」 다시 씀**(Ch 18 「게이트」와 겹침 피함) · 시간 여행 → 「지난 체크포인트에서 다시 실행」 · fork → 「분기」 금지, 「갈래」는 Ch 13 조건부 엣지 뜻 → 「새 줄」·「갈라 낸 실행」·「곁줄」 가운데 · 상태 기록 → Ch 23 01 「체크포인트 목록」 · StateSnapshot → Ch 23 「체크포인트」 · reducer → 「리듀서」(Ch 13) · 「직렬화」 → 「JSON으로 적을 수 있는 값」.
- 금지어 목록은 Ch 23 요약 §4 끝(「지시」·「반환」·「추정」·「지연」·「분기」·「경로」·「trace」·「스키마」·「스냅샷」·「채널」·「식별자」·「레코드」·「로그」·「런타임」·「보장」·「정확히 한 번」·「측정」·「검증」·「필드」·「사전」·「순차」·「재시작」 등) + 이 챕터에 많은 「포인터」(단독)·「소비」·「시나리오」·「파라미터」·「프롬프트」·「임계값」·「fork」·「payload」.

### 8-5. 힌트·클래스·셀 모양
- 노드 힌트 빼기(Ch 13·20·23) · 상태 형식 이름을 칸 구성마다(`GateState`·`ReviewState`·`PriceState` 등) · `.get`·`reversed`·`10_000`·집합·풀기·f-string 없이 · 15줄 넘는 셀 셋 나누기 · 호출 두 겹(`len(list(…))`) 풀기.

### 8-6. 참고 자료 b10
- 세 절이 같은 넷 → 절마다 맞는 문서로: 01 Interrupts(규칙·승인) · 02 Interrupts(다시 묻기·아이디 딕셔너리) · 03 Time Travel·Persistence. 설치판 소스 행(아래 §13)도.

## 9. 삽화 비유 계열 후보

**이미 쓴 계열**(과정 요약·Ch 23 준비 조사·`figures/*.prompt.md` 181개 `grep`): Ch 23 준비 조사 §10 목록 + **체스판·즉석사진·사진첩·기보·리본(Ch 23)** · 식당 주문 전표·창·**걸쇠 건 서랍**(Ch 19 06 — 사람 확인 값) · 자료실 승강 상자(Ch 20) · 세탁기(Ch 21) · 공항 검사·우편 가림막·방문자 명부(Ch 22) · 눈 위 발자국·말뚝·**울타리 = 사람 확인**(Ch 17) · 개찰구(Ch 16) · 레일·갈림길(Ch 13·18). `grep` 수: `stamp`/`seal` 23(**도장은 Ch 6 01 등에서 씀 → 피함**) · `gate` 6 · `turnstile` 2 · `photo`·`polaroid` 8 · `album` 6 · `chess` 7 · `elevator` 9 · `hourglass` 5 · `ticket` 5 · `flag` 4. **0건**: `domino` · `canal`·`lock gate` · `cassette`·`tape recorder`·`film` · `railway`·`train` · `bookmark` · `drawbridge` · `map`.

| 후보 | 그림 요소(절별) | 장점 | 겹침·위험 |
|---|---|---|---|
| **A. 도미노 줄과 비워 둔 자리** | 01 Before: 빈자리 **앞**에 쓰러진 컵(부작용이 먼저) ↔ After: 빈자리 뒤의 컵이 서 있음 · 02 빈자리에 맞지 않는 모양의 조각이 누워 있고 줄은 멈춤 ↔ 맞는 조각이 서서 줄이 이어짐 · 03 쓰러진 원래 줄은 그대로, 가운데 자리에서 다른 방향으로 새로 세운 줄 · 실습 절 두 줄 견주기 | 「사람이 조각을 놓아야 이어진다」가 손 없이도 읽힘 · 「노드가 처음부터 다시」(줄 앞부분이 다시 쓰러짐)도 그림으로 가능 · 0건 계열 | 도미노 수·빈자리를 생성 모델이 틀리기 쉬움 · 03 새 줄이 Ch 13 갈림길(조건부 엣지)처럼 보일 수 있음 |
| **B. 운하 갑문과 곁 물길** | 01 배가 갑문 방 안에서 기다림(아래쪽 문 닫힘) ↔ Before: 문이 먼저 열려 물이 쏟아진 방 · 02 문 손잡이에 걸린 잘못된 쐐기 ↔ 맞는 쐐기 · 03 앞 갑문으로 돌아온 두 번째 배가 곁 물길로, 첫 배는 아래 물길 끝에 그대로 | 「멈춰서 기다린다」·「되돌리기 어려운 물」이 선명 · 0건 계열 · 사람 없이 가능 | 03 「지난 자리로 돌아가기」가 약함(배를 둘 그려야 함) · 갑문 구조를 모델이 틀리기 쉬움 · 02 비유 약함 |
| **C. Ch 23 체스판·즉석사진 이어 가기 + 봉함 수(봉투에 넣어 둔 다음 수)** | 01 판 옆에 봉한 봉투(다음 수를 적어 둠), 판은 그대로 ↔ Before: 봉투를 열기 전에 이미 잡힌 말 · 02 되돌아온 봉투에 쪽지 · 03 사진첩에서 고른 사진 한 장대로 **두 번째 판**을 차려 다른 수, 원래 판은 그대로 · 실습 절 판 둘 | **03 시간 여행이 가장 자연스러움**(사진 = 체크포인트, 사진첩 = 스레드 — 학생이 이미 앎) · 계열 이음으로 Ch 23 → 24 연속성 | 한 챕터 한 계열 선례와 다름(두 챕터가 한 계열) · 봉함 수는 학생에게 낯섦 · 봉투(`envelope`) 이미 씀 · Ch 23이 막은 시계·사람 없이 「기다림」 표현이 약함 |
| **D. 녹음 카세트와 표시 붙인 테이프** | 01 멈춤 단추가 눌린 녹음기 옆 확인 카드 · 02 되감긴 자리 · 03 표시 자리에서 **복사한 두 번째 테이프**에 다른 녹음, 원본 테이프는 그대로 | 「지난 자리로 되감아 다른 길」이 직관적 · 0건 계열 | 단추 기호(▶·‖)가 글자·기호 금지와 부딪힘 · 테이프 표시가 작아 판독 어려움 · 옛 물건이라 학생에게 낯섦 |

- **Ch 23 계열을 이어 갈지**: 잇는 쪽(C)은 03·실습 절이 가장 잘 읽히고 체크포인트 비유를 새로 풀 필요가 없음. 대신 01·02(사람이 멈춰 확인)가 체스 장면과 맞지 않아 억지가 되고 「한 챕터 한 계열」(Ch 19~23 선례)과 다름. 새 계열(A·B·D)은 01·02가 선명하나 03에서 「체크포인트」 비유를 다시 세워야 함 → A를 고르면 03 「그림 읽기」에 「Ch 23의 사진 한 장처럼, 쓰러지기 전 줄의 한 자리」 한 문장으로 이을 수 있음.
- 사람·손·동물·화면·글자·숫자·화살표·시계 없음이 선례. 스타일 문구는 규격 §5-4 그대로.

## 10. 위험과 깨진 것

1. **02가 지금 공식 문서 규칙과 반대 모양**(`while True` 다시 묻기, §5-2) — 고치면 출력·본문 숫자(`history count: 3` 등)가 바뀜.
2. **묶음 실행 검사 계약**(§4-2) — 01에 키·모델·새 패키지·도구 파일을 넣으면 zip·목록·잠금을 함께 고쳐야 통과, 마감에서 `bundle-execution.json`·01 `code_sha256` 다시 적기.
3. **파일 쓰기 자리** — 01이 실습 폴더에 쓰고 지움(연결 폴더 삭제 막힘 — 제자리 실행 불가 추정, 학생 폴더에 파일 남음). SQLite를 넣으면 임시 폴더 필수.
4. **공용 옛 생성기** — 돌리면 Ch 24 현재 노트북(출력 포함)·`_src`·그림 생성기를 옛 판으로 덮어씀. 01절 작업 때 막고(파일은 Ch 23 `qa/` 안) 마감에 옮길 것(§3).
5. **`resume` 말 세 장면** + 「이어 실행」 + Ch 23 03의 약속 문장 — 제목·본문 「재개」 21번(01·02). 첫 자리 구분 문장이 없음.
6. **다시 실행(replay) 설명** — 설치판은 `fork` 체크포인트를 만들고 뒤 노드를 다시 실행 · 스레드 설정 `get_state`는 가장 최근 줄(새 실행) — 「원본이 남는다」를 「원본 설정으로 읽으면 9000」으로 정확히.
7. **03 소수 잘라 내기**(0.33 → 6699) — 값 바꿔 보기 함정.
8. **실행하지 않은 문장**: JSON 직렬화 규칙(메모리 체크포인터에서는 확인 안 함) · 리듀서 누적·`as_node`·LLM 다시 호출(03) · 「흐름만 느려질」(01, 재지 않음) · 보상 작업(Ch 31 몫) · 감사 기록(02 b7).
9. **뒤 챕터 문장**: Ch 27 08 「도구 실행 경계」(도구 승인 장면 없음 — 부분 참) · Ch 30 06 「중복 실행 방지 원칙」(01 멱등 문장을 남겨야 참) · Ch 25 「재개 사건」.
10. **옛 검사** — `check_scope.py`(실습 절 붙이면 멈춤)·`check_notebook_readiness.py`(결과 파일 먼저 씀 → 되돌림)·`check_figures.py`(`.excalidraw` 짝) — 기록만.
11. **서비스 요청 어림**: **M1이면 0번**(키 셀 없음). M2로 02·03·04에 모델을 넣으면 절마다 2~5번 × (새 커널 2 + 노트북 밖 5) → 약 **40~80번**, 요금표 어림 **0.1달러 아래**(Ch 21 판 요금 mini 입력 0.75·출력 4.50달러/100만 토큰, 요청당 입력 약 600토큰 가정 — 청구 금액 아님). 삽화 넷(04 포함) 약 8크레딧(재생성 포함 최대 16).
12. **실행 시간**: e1~e6 모두 1초 안팎(재지 않음 — 셸 180초 안에 여유).

## 11. 01절 작업자가 먼저 결정해야 할 것

1. **모델을 부를지(§6)** — M1(없음) / M2(모델 노드 + 승인 노드, 잠금 추가) / M3(사람 승인 미들웨어). 어느 쪽이든 **01은 모델·키 없이**(묶음 검사 계약). Ch 27 08 문장과 실습 절 요청 수가 여기서 정해짐.
2. **파일 쓰기 자리와 부작용 흉내(§8-2)** — 01 기록 파일을 Ch 23 임시 폴더 준비 셀(`ch24-01-`)로 옮길지, 기록 파일 모양을 Ch 23 06(`append_key`·`append_key_once`·`read_record`)으로 맞춰 「interrupt 앞 쓰기는 멱등하게」(Ch 30 06이 기대는 문장)를 실행으로 보일지 → 도구 파일 A/B/C(§7)와 이름(`approval_tools.py` 후보).
3. **02 다시 묻기 구조(§8-3)** — `while True`를 조건부 엣지 판으로 바꿀지(공식 문서 권장), 견줄지. 실패 장면(체크포인터 없이 이어 가기 `RuntimeError` · 다른 스레드 `KeyError` · 여러 멈춤 `RuntimeError`) 가운데 무엇을 넣을지.
4. **용어와 제목(§8-4)** — `Command(resume=…)`을 부를 한국어 말(Ch 23 03 「스레드 재개」와 가르기), 「승인 지점」(Ch 17 02) 다시 쓰기, 03 「분기」·fork 대신 말, 「time travel」 풀이, 02·03 슬러그를 바꿀지(01 고정). `handoff.md`에 용어 표로 먼저.
5. **출력·`assert` 대상과 03 계산** — `Interrupt.id`·체크포인트 ID는 출력하지 않음 · 체크포인트 수·호출 횟수·오류 이름·칸 값에만 `assert` · 03 가격 계산을 정수로(소수 잘라 내기 함정) · 기록 출력은 Ch 23 01 `print_history` 모양(`metadata["step"]`·`["source"]`)으로 원천 `update`·`fork`를 보일지.

## 12. 챕터 마감으로 미룰 것

- **04 실습 절 신설**(규격 §7-2): 슬러그 후보 **`04-Human-in-the-Loop-실습`**(선례 `07-Persistence-실습`·`09-Middleware-실습`·`07-create-agent-실습`·`05-ToolNode-실습`·`08-LangGraph-실습`처럼 챕터 제목의 앞말) — 다른 후보 `04-Human-in-the-Loop와-Time-Travel-실습`(`07-모델과-도구-실습`처럼 제목 전부, 길어짐). 제목 「Human-in-the-Loop 실습: …」, `format: experiment`, meta 「실습 30분 · 새 용어 0」(**챕터 시수 3·5h에 더하지 않음**). 새 문법·API 0. 주제 예 — Ch 23 07 대출 소재 잇기(이용자 `M-0317`·대출 키 `loan-2307`): 대출 연장 기록 노드 앞 승인 지점 → 실행 1 승인 ↔ 실행 2 값 하나만(거절, 또는 지난 체크포인트에서 연장 일수만 바꿔 다시 실행) · 또는 Ch 17 03·Ch 19 07 「사람 확인」 소재(환불 요청 등록·주문 취소 `O102`)를 이어 가기까지. 모델 요청은 §6 선택에 따라 0 또는 3~5(0이면 Ch 23 07 선례·강사 확인). 따라오는 것: `chapter.json` 절 추가 · `textbook/part6/_build_index.py` 22행(시수 3·5 그대로, 설명의 「분기」) · 챕터 `qa/public-files.json`(경로 배열 — 노트북·HTML 줄) + `collect_public_files.py`로 Part 목록 · `textbook/_notebook/build_index.py` 52행(절 수 3, 선례대로 둘지) · `check_scope.py`(기록만) · 03 「다음 학습과 이어지는 지점」(지금 Ch 25)을 04로.
- 공용 옛 생성기 `mv -n` → `textbook/part6/ch23-persistence/qa/upgrade/before/generators/blocked/` · Ch 24 `figures/_gen_figures.py` `mv -n` → `qa/upgrade/before/generators/blocked/`.
- 옛 그림 9개(`figures/0N-흐름.{svg,excalidraw,caption.md}`) 삭제 승인 목록(사본 `before/figures/`, `final-artifact-hashes.json`이 해시를 적은 기록 파일) · 챕터 공개 목록의 옛 SVG 세 줄 빼기(Ch 23 선례).
- `chapter.json` `objectives`(「interrupt와 Command(resume=)」·「승인 입력을 검증」·「새 분기」)·절 제목, `_build_index.py` 설명을 개선 본문과 대조 → `_build.py`·`_build_index.py`.
- 실습 폴더 README 다시 쓰기(노트북 넷, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 파일은 임시 폴더, 요청 수, 도구 파일) · `labs/part6/continuity-guide.md` 9·10행(「분기」 말 — 참이면 둠) · `qa/research.md`·`verification.md`·`집필점검표.md`에 「개선 전 판」 표시.
- `part6-practice.zip` 다시 만들기 → **`check_bundle_execution.py`(01 PASS·새 `code_sha256`)** → `check_delivery.py`(`llm-practice.zip` Stale 예상) · 옛 검사 넷 돌려 기록(`check_notebook_readiness.py` 결과 파일 되돌림).
- **뒤 챕터 인계**(고치지 않음): Ch 25 01~03 b3 · Ch 27 01·08 b3(도구 실행 경계) · Ch 28 03 b3 · Ch 30 06 b3(중복 실행 방지) · Part 6 소개·`practice-start.md`·continuity-guide · Ch 23 03·07 문장 대조.
- 삭제 승인 대상: 실습 폴더 `.venv`(macOS 125MB) · `qa/upgrade/gates-wip-*.json` · `qa/upgrade/__pycache__`(생기면) · `.cache/vm/venv-ch24-human-in-the-loop`(207MB) · 기기 `/tmp/ch24-prep`(64KB).

## 13. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 3 · `notebooks` 3 · `figures` 10(SVG·excalidraw·caption 각 3 + `_gen_figures.py`) · `generators` 2(**공용 `author_ch23_ch24.py` 사본**·`_gen_figures.py`) · `qa` 3(`public-files.json`·`research.md`·`verification.md`) · 실습 폴더 3(`pyproject.toml`·`uv.lock`·`README.md`) · `chapter.json`·`집필점검표.md`·`_build.py`·`index.html`(목차, objectives 대조용) = **28개, 392KB**. 원본과 `cmp` 모두 같음 |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 93, 통과 0/3), `f86992b4…` |
| `qa/upgrade/before-manifest.json` | sha256 **131개**(`ab149cd5…`) — ① 이 챕터가 읽거나 가져올 수 있는 파일 30: 실습 폴더 6 · Ch 23 도구 파일·노트북 01·03·05·06·07·잠금 둘 · Ch 21 `runner_tools.py`·잠금 둘 · Ch 22 잠금 둘 · 도구 파일 여섯(Ch 13·16~20, 이름 피하기용) · Ch 17 02·03·Ch 18 01·Ch 19 06·07 `_src`(사람 확인·승인 지점·게이트 말) ② Ch 24를 가리키는 완료 챕터 파일 8: Ch 23 03·07 `_src`·HTML · `author_03.py`·`author_06.py`·`author_07.py` · Ch 23 `chapter-summary.md` ③ Ch 24에 기대는 대기 챕터·Part 파일 12: Ch 25 01~03 · Ch 27 01·08 · Ch 28 03 · Ch 30 06·`_generate.py` · `_generate_ch25_ch26.py` · Part 6 소개·`practice-start.md`·continuity-guide ④ 공용 옛 생성기·Ch 24 `_gen_figures.py`·`textbook/part5/_figure.py`·`part6a_enrich.py` ⑤ 묶음·목록·기록 57: `part6`·`llm`·`part7-practice.zip` · Part 6·7 목록 · 챕터 `qa/` 셋·`집필점검표.md` · Part 6 `qa/*.json` 열둘·검토·색·언어 기록 · Part 7 기록 셋 · notebook-contracts·챕터 화면 기록 · `textbook/index.html`·`part6/index.html` · Ch 24 HTML 넷·`_src` 셋·옛 그림 아홉 ⑥ 규칙·검사·빌드 20: `part6/_build_index.py` · `_notebook/build_index.py`·`build_bundle.py`·`verify.py`·`execute.py` · Part 6 검사 일곱 · Part 7 `check_bundle_execution.py` · `_template/builder.py` · 챕터 `_build.py`·`chapter.json` · `run_section.sh`·`nbkit.py`·`upgrade_gates.py` · `check_course_continuity.py` |
| `$ROOT/.cache/vm/venv-ch24-human-in-the-loop` | Python 3.12.13 · 207MB |

### 가상환경 만든 방법과 결과
- Ch 23 준비와 같은 방법: `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy uv venv --python 3.12.13 …/venv-ch24-human-in-the-loop` → 잠금 목록 `uv export --project labs/part6/ch24-human-in-the-loop --frozen --no-hashes --all-groups --no-emit-project`(실습 폴더 파일 그대로 — `pyproject.toml`·`uv.lock` 수정 시각 09-10 그대로), 주석·빈 줄만 뺀 80줄(`/tmp/ch24-prep/req-clean.txt`) → `uv pip install pip==26.2` → **`bin/python -m pip install --no-cache-dir -r`**. 설치 오류 0, **uv 캐시 정리(`uv cache prune`) 안 함**. 기기 루트 디스크 여유 **1.5G**(작업 전후 같음), `/tmp/uv-cache` 392MB 그대로.
- 결과: `pip freeze`와 잠금 대조 **판 차이 0**(설치 75 = 잠금 80 − 이 기기에 해당하지 않는 다섯: `appnope`(darwin)·`colorama`(win32)·`cffi`·`pycparser`(PyPy)·`httpx2-jsfetch`(emscripten), `pip`은 freeze에 안 나옴). `ipykernel 7.3.0`·`nbclient 0.11.0`·`pip 26.2`(규격 요구 판). `pip check` 이상 없음. 커널 스펙 `share/jupyter/kernels/python3` 있음.
- import 확인만: `interrupt`·`Command`·`Interrupt`·`StateSnapshot`(`langgraph.types`) · `InMemorySaver` · `StateGraph`·`START`·`END` · `GraphInterrupt`. `langchain`·`langchain_openai`·`openai`·`dotenv`·`numpy`·`HumanInTheLoopMiddleware`는 없음(잠금대로). `run_section.sh`는 `$ROOT/.cache/vm/venv-<챕터 폴더 이름>`을 자동으로 씁니다.

### 참고 자료 (2026-09-25 확인)
- Interrupts `https://docs.langchain.com/oss/python/langgraph/interrupts` — 「the runtime restarts the entire node from the beginning」·「Matching is strictly index-based」·「Do not loop `interrupt` calls … including `while True` validation loops. Use a conditional edge instead.」·「If you wrap the `interrupt` call in a try/except block, you will catch this exception」·「Side effects called before `interrupt` should (ideally) be idempotent」·「Pass simple, JSON-serializable types」·아이디 딕셔너리 재개·정적 중단점(`interrupt_before`/`after`)은 HITL에 권하지 않음·`invoke`는 `result["__interrupt__"]`.
- Time Travel `https://docs.langchain.com/oss/python/langgraph/use-time-travel` — 「Replay re-executes nodes—it doesn't just read from cache」·「History is in reverse chronological order」·`update_state` 「creates a new checkpoint that branches from the specified point. The original execution history remains intact」·`as_node`·「Interrupts are always re-triggered during time travel」.
- Persistence `https://docs.langchain.com/oss/python/langgraph/persistence`(Ch 23 확인분).
- 설치판 소스(`langgraph 1.2.11`): `types.py` 851~935행(`interrupt` 독스트링 — 여러 호출은 차례로 맞춤·체크포인터 필요)·622~625행(`interrupt_id` 사용 중단) · `pregel/_loop.py` 952~971행(다시 실행 때 `fork` 체크포인트) · `pregel/main.py` 1819·2282행(`source: fork`)·2631~2670행(`invoke(version=…)`) · `errors.py`(`GraphInterrupt` → `GraphBubbleUp` → `Exception`) · (Ch 21 가상환경) `langchain/agents/middleware/human_in_the_loop.py` 405행 `after_model`.
