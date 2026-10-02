# 02절 진단 — create deep agent와 도구 (2026-09-28)

- 생성기 `qa/upgrade/author_02.py`(`24a42ef5…`) · 노트북 `labs/part6/ch27-deepagents/notebooks/02-create-deep-agent와-도구.ipynb`(`f031b310…`, `code_sha256` `6f5358591ac9…`) · `_src/02-create-deep-agent와-도구.html`(`5b670ce8…`) · 빌드 HTML(`cad8f9af…`) · 그림 `figures/02-1~02-5` · 흔들림 확인 `02-probe.md`·`probe/probe02.py`(`f87af6d9…`)·`probe/probe-02-P1.jsonl` · **도구 파일 첫 판** `notebooks/harness_tools.py`(`14ee39ca196a2da1351f8dce7a4cab3e7b473f74fba2d2f2cb4bafd7f667e258`).
- 형식 **experiment** 유지, 슬러그 `02-create-deep-agent와-도구` 그대로(01 b8·Part 6 목차 링크), 제목 「create deep agent와 도구」 그대로 — 본문 1절·b2에서 「함수 `create_deep_agent`의 이름을 띄어 쓴 것」으로 풂(강사 확인).
- 챕터 리드 결정 M2: **앞 절반(2~4절) 모델 없음 · 뒤 절반(5~7절) 실제 모델 한 번 실행(요청 2번)**.

## 1. 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 뒤(`gates-wip-02-02.json`) |
|---|---|---|
| 코드 셀 | 5 | **26**(준비 셋 + 모델 셀 하나 + 본문 스물둘) |
| 검사 문장 | 69 | **365** |
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 6 · 4 · 2 · 1 · 7 · 19 · 3 = **42** | **0 · 0 · 0 · 0 · 0 · 0 · 0 (PASS)** |
| 코드 줄(`count_code.py`, 주석·빈 줄 뺌) | 28 | 132(+ 도구 파일 44줄 — 여섯 함수, 가져오기 0) |

- **첫 실행 전** `upgrade_gates.py … --label wip-02 --section 02`: G1 0 · G2 0 · G3 0 · G4 0 · G5 0 · G6 7(괄호 뒤 「).」 합쳐 세진 긴 문장 셋 · 코드 이름으로 시작한 문장 넷) · G7 18(그림 전). G6은 실행 전에 고쳐 0.
- AST 따로(`/tmp/ch27-02/tools/extra_check.py` — 01 판 + `@wrap_model_call` 허용 표시 한 줄): **금지 문법 0건**. 허용 표시만 셋 — 셀 `record_tool_names`의 `@wrap_model_call`(규격 §2-2 L6, Ch 22 02 기록 훅 선례 — 처음 쓰는 자리에 「이 줄은 아래 함수를 모델 요청을 감싸는 훅으로 등록합니다」) · 도구 파일 `estimate_cost`의 `usage.get`·`details.get`(Ch 6 06·Ch 21 판 본문, Ch 26과 같음). 호출 깊이(`depth.py`) **최대 2**. 준비 셀 밖 셀 최대 10줄(5절 `rule_agent` 셀), 함수 본문 최대 6줄(`record_tool_names`), 셀당 정의 하나. 힌트는 `@tool` 매개변수 `topic: str` 하나.
- 금지어(`ban27.py`): 노트북 설명·주석·`_src`·`.mmd`·캡션에서 걸림 3건, 모두 「캐시 입력」(과정 요약 §5 Ch 15 약속 말 — 단독 「캐시」 아님, Ch 26 01과 같은 문장). 「경로」·「반환」·「측정」·「검증」·「프롬프트」·「한 겹 더」 0건. (옛 그림 `02-흐름.caption.md`의 「반환」은 본문 참조 0 — 삭제 승인 목록.)
- `verify.py --chapter`: `PASS 8 sections / 79 code cells (max 17 lines)`(17줄은 03~08 옛 노트북). 빌드 HTML `{{`·`[[` 0건, 인라인 SVG 4·삽화 JPEG 1.

## 2. 수정 전 주요 문제 (옛 판 — 학생 본문에는 쓰지 않음)

1. **모델의 도구 선택에 `assert`**(`any(call['name'] == 'course_lookup' …)`)와 **도구 결과 글 속 단어에 `assert`**(`'DeepAgents' in str(m.content)`) — 규격 §3 위반(흔들리는 값).
2. 모델 `init_chat_model('openai:gpt-5.4-mini')` — `temperature=0`·`reasoning_effort="none"` 없음(G4), 모델·도구·에이전트 한 셀. 흔들림 확인 기록 없음.
3. 도구 `course_lookup(chapter: int) -> str` + `{27: …}[chapter]`(다른 장은 `KeyError`), 영어 독스트링, 반환 힌트.
4. 문법: 내포식 넷·제너레이터·`getattr` 둘·`any` 둘·`m` 넷(한 글자 변수)·`sorted(agent.get_graph().nodes)`(호출 세 겹) · 첫 줄 주석 없는 준비 셀 · `assert version(...)`.
5. 옛 b4 「기본 파일 도구는 … `execute`는 샌드박스 백엔드가 있을 때만 실제 명령을 수행」 — **부분 참**: 그래프에는 늘 등록되지만 명령을 실행하지 못하는 백엔드면 모델 요청 목록에서 빠짐(이 절 6절 출력). 설치판 독스트링 297~299행의 「오류 글을 낸다」도 같은 판 미들웨어와 어긋남(b7에 밝힘).
6. 금지어: 반환 6/5/1 · 측정 2 · 명시 2/1 · 궤적 1/1 · 표면 2/1 · 시그니처 1 · 보장 1/1 · 스키마 1. 결과 읽기 셀 0 · 제목 셀·핵심 그림 없음 · Mermaid 0 · 삽화 0 · 옛 SVG 토큰 · b10이 여덟 절 공통 여섯(확인 2026-09-11) · b1 둘째·셋째와 b8 셋째가 틀 문장.
7. 요금 사고 방지 규칙(01 결정) 없음 — 바깥 한도·general-purpose 명세 한도 없이 모델 실행.

## 3. 바꾼 것

- **노트북(26 코드 셀, 일곱 절)**: 1절 준비(설치 넷 — deepagents 0.7.0·langchain 1.4.0·langchain-openai 1.6.0·python-dotenv 1.2.3, langgraph는 직접 가져오지 않아 뺌 · 가져오기(도구 파일 한 줄 포함) · 키 · 모델) → **2절** 규정 글 넷(Ch 21 01 `POLICIES` 대출·운영·연체 그대로 + Ch 26 01 연장 두 문장, 교재용) · `@tool lookup_rule(topic: str)`(없는 주제어는 정해 둔 글 — Ch 21 01 `lookup_policy`와 이름을 달리함) · 도구 이름·설명·인자 · 모델 없이 `invoke` 두 번 → **3절** 기준 Deep Agent `도구 수: 9`·우리 도구를 넘긴 `도구 수: 10`·`더해진 도구: ['lookup_rule']`·`빠진 도구: []`·`노드가 같은가: True` · **「백엔드」 첫 정의** · `supports_execution(StateBackend())` `False` → **4절 값 바꿔 보기** `LocalShellBackend()`(만들기만, 에이전트에 넘기지 않음) `True` → **5절** 바깥 호출 한도 3 · 같은 이름 general-purpose 명세(한도 2, `tools` 없음) · 기록 훅 `@wrap_model_call record_tool_names` · `rule_agent`(도구 10·노드에 한도 둘) → **6절** 한 번 실행 · `show_messages` · 마지막 답 글 · `tool_call_names`로 요청한 도구·`task` 0 · 기록 훅 `모델이 받은 도구 수: 9` · `그래프에만 있는 도구: ['execute']`·요청마다 `False` → **7절** `sum_usage`(이번 실행이 더한 메시지만)와 기록 훅 요청 수 2 = 2 · `estimate_cost` → 정리 셋.
- **본문 10블록** 블록 단위로 다시 씀: b2(01이 넘긴 자리 · 제목 풀이) · b3(Ch 19 01·05, Ch 2 09 링크, Ch 21 01, Ch 26 01, Ch 22 02·04, Ch 6 06, 01절) · b4 비유(온실 연장 걸이) + 삽화 + 「백엔드」 세 문장(뜻 → 보관 방식 → 코드 모습) + 두 목록 설명 + 02-1 + 「더해지기만」(독스트링 336행, 하네스 프로필은 전역이라 안 씀) + 안전 설정 셈 · b5 + 02-2 · b6 값 성격 표(구조 값 / 모델 판단 값 / 흔들리는 값) + 02-3 + 요청 수 셈 + 02-4 + 두 커널 문장 · b7 여덟 항목 · b8 · b9 네 문제 · b10 절 자료(확인 2026-09-28).
- **새 용어 1**(meta): 백엔드(용어 표 「02 첫 정의」 자리). 이어 쓴 말: 기록 훅(Ch 22 02) · 호출 한도(Ch 22 04) · general-purpose 서브에이전트·서브에이전트 명세·파일 도구·Deep Agent(01) · 예상 비용(Ch 6 06).
- 옛 판의 `assert` 셋(판 번호·도구 선택·도구 결과 단어) 뺌 — `assert`는 키 셀 하나뿐.
- 도구 파일에서 가져온 함수 여섯: Ch 19 `tool_call_names`·`show_messages`·`sum_usage` · Ch 6 06 `estimate_cost` · 01 `tool_names`·`names_only_in`(아래 §7).

## 4. 흔들림 확인 (노트북 밖, `02-probe.md`)

- §0(판단 규칙·그림 라벨 규칙)을 **2026-09-28T12:13Z에 적음**(파일 쓰기 뒤 기기 시각 12:13:08Z) → 첫 요청 12:13:16Z(§0은 그 전에 적음 — 마감에서 표현 고침, 검토 A-19)(회차 1 기록 시각 12:13:18Z). Ch 26 A-8 교훈대로 §0 먼저.
- P1 5번(요청 10번, 서비스 오류 0): 구조 값 5/5(훅 첫 요청 도구 아홉·`execute` 없음·그래프에만 `['execute']`·요청 수 == 훅 수) · 모델 판단 값 5/5(첫 응답 `lookup_rule` 1개·둘째 0개·`task`·파일 도구 0·메시지 넷·요청 2·인자 `{'topic': '연장'}`) → **입력 그대로**.
- 흔들린 값: 캐시 입력 토큰 1664 ↔ 3328 → 캐시를 넣은 어림 0.001946 ↔ 0.000823달러. 입력 3792·출력 50·답 글(55자)은 다섯 번 같았지만 서비스 쪽 값·모델 글이라 결론에 안 씀.

## 5. 실행과 값

- 교재 출력 **A**: `run_section.sh` 2026-09-28T12:24:49Z · `PASS … 26 cells` · `code_sha256` `6f5358591ac9e955…` · `outputs_sha256` `7691ccfa…`. 사본 **B**(그림 전, `--tools-copy`로 디스크 도구 파일 복사): 12:25:12Z, 같은 `code_sha256`·같은 `outputs_sha256`. **셀별 출력 대조 26/26 같음**(`cmpout.py`, 셀 출력 글 연결 해시 `f9358c736e056cc1` 셋 — A·B·마크다운 채운 뒤 디스크 노트북). 갈린 셀 없음(답 글·토큰·비용 셀도 이번 두 번은 같음 — 결론에는 안 씀).
- **구조 값(결론·그림)**: `기본 도구 수: 9` · `도구 수: 10` · `더해진 도구: ['lookup_rule']` · `빠진 도구: []` · `노드가 같은가: True` · `백엔드 종류: StateBackend`/`명령을 실행할 수 있는가: False` · `LocalShellBackend`/`True` · `바깥 호출 한도: 3` · 명세 키 넷 · `그래프에 등록된 도구 수: 10` · 노드 일곱(`ModelCallLimitMiddleware` 둘 더함, 기록 훅은 노드 없음) · `모델이 받은 도구 수: 9`(받은 차례 `['ls', 'read_file', 'write_file', 'edit_file', 'delete', 'glob', 'grep', 'task', 'lookup_rule']`) · `그래프에만 있는 도구: ['execute']` · 요청마다 `False`.
- **모델 판단 값(흔들림 확인 5/5 + 두 커널 같음 — 「이번 실행에서는」·「우리 도구를 한 번 부른 실행」 한정어와 함께만)**: `결과 메시지 수: 4` · `AIMessage | 도구 호출 요청: ['lookup_rule']` · `요청한 도구 이름: ['lookup_rule']` · `task를 부른 횟수: 0` · `기록된 모델 요청 수: 2` · `응답으로 센 요청 수: 2` = `기록 훅이 센 요청 수: 2`. 결론은 셈 「도구를 요청한 응답 수 + 1」.
- **흔들리는 값(둘째 단락·b6 표·확인할 점·b7만)**: 도구 메시지 내용(주제어 「연장」 규정) · 답 글(도구 글 그대로 두 문장) · `입력 토큰: 3792 | 출력 토큰: 50` · `예상 비용(달러): 0.003069`(캐시 입력을 빼지 않은 요금표 어림).
- 걸린 시간은 재지 않음. 파일 쓰기 0(`StateBackend` — 이번 실행은 파일 도구를 부르지 않아 상태 칸에도 없음). 결과 읽기 둘째 단락의 흔들리는 값은 `[[READ_…]]` 자리 표시로 두고 교재 출력(A) 뒤 생성기·노트북 마크다운에 같이 채움(`_src`는 `--src-only`로 다시 씀, `genmatch.py` 셀 56 차이 0·`_src` 같음).

## 6. 안전 규칙 적용 (챕터 공통 (가)·(나))

- (가) 바깥 `middleware=[ModelCallLimitMiddleware(run_limit=3, exit_behavior="end"), record_tool_names]` — 노드 `ModelCallLimitMiddleware.before_model`·`.after_model`이 출력에 보임.
- (나) `subagents=[같은 이름 general-purpose 명세]` — 자기 호출 한도 2(01 명세 모양, 한도 0 → 2), `tools` 없음 → `lookup_rule` 물려받음(`graph.py` 728행 · 노트북 밖 모델 없는 확인 `x2_seen.py`: 안쪽 요청 도구 여덟 = 파일 도구 일곱 + `lookup_rule`, `task`·`execute` 없음, 시스템 메시지 글 = 명세 글).
- 상한: 한 번 실행 요청 ≤ 3 + `task` 부른 횟수 × 2(본문 b4·복습 4). 이번 실행 `task` 0, 요청 2, 한도에 닿지 않음. (라) `recursion_limit`은 주지 않음.
- 요청 수 세기: 이번 실행이 더한 메시지만 잘라 `sum_usage`(Ch 26 01) = 기록 훅 요청 수. 서브에이전트 요청은 두 셈 모두에 없다는 한계를 b6·b7·복습 3에 공개. 한도 글 응답의 사용량 `None` → `sum_usage` 멈춤 가능(Ch 26 01)을 b7에.

## 7. 도구 파일 — `harness_tools.py` 첫 판 (이 절이 만듦)

- 함수 여섯(차례): `tool_call_names`(Ch 19 04) · `show_messages`(Ch 19 06) · `sum_usage`(Ch 19 05) · `estimate_cost`(Ch 6 06) — **Ch 21 `runner_tools.py`(`f4113158…`) 설명 주석·본문 글자 그대로, Ch 26 `delegation_tools.py`(`c3c1709a…`)의 같은 블록과도 글자 같음** · `tool_names`·`names_only_in`(**01절 노트북 셀 글 그대로** — `# Ch 27 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다`). 가져오기 0, numpy 없음. 머리 설명 첫 줄 「앞 챕터와 이 챕터에서 배운 평범한 함수를 모아 둔 도구 파일입니다」(Ch 24 A-13·Ch 25 A-14·Ch 26 A-18 교훈).
- **생성기 대조 사슬(첫 판부터)**: `TOOLS_HEAD` + `file_block(runner, 이름)`(runner 해시 고정 확인 뒤) + 01 셀 글(`author_01.DEF_TOOL_NAMES`·`DEF_ONLY_IN`, 01 노트북 디스크 셀에 그 글이 있는지 확인) · `strip_later_imports(text)` · `check_tools()`(이름 차례·가져오기 0·runner/delegation 블록 문자열·AST·01 셀 AST 대조) · **쓰기 가드**(없거나 `== TOOLS`일 때만 쓰고, `strip_later_imports(디스크).startswith(TOOLS)`면 뒤 절 판이라 건너뜀, 둘 다 아니면 `assert`) · `--tools-copy DIR`은 **디스크 판** 복사(Ch 26 A-19). `check_same_as_probe()`로 노트북 셀 글(규정·도구·명세·훅·에이전트·질문·모델)이 `probe02.py`와 같은지 확인.
- 설치 셀: 도구 파일이 가져오는 패키지 0이라 더할 것 없음(규격 §2-7 6번). 처음 가져오는 절의 결과 읽기에 규격 §2-7 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 …」 + 실행 도구 한 문장(Ch 26 01 판).
- 묶음 목록: 챕터 `qa/public-files.json`에 한 줄(`d1330533` → `47aa0ac8`) → `python3 -B textbook/part6/qa/collect_public_files.py`(`Explicit public files: 87; prerequisites: 13`) → `textbook/part6/public-files.json` 69행(`0d44ef6f` → `205d50ff`), `prerequisite-files.json` 같음(`4c7f5a4b`). **zip은 다시 만들지 않음**(챕터 마감에 `_build_index.py` 한 번).

## 8. 고친 틀린 사실·과장

- 옛 b4 「`execute`는 샌드박스 백엔드가 있을 때만 실제 명령을 수행」 → 그래프에는 등록되지만 모델 요청 목록에서 빠짐(출력 `그래프에만 있는 도구: ['execute']`). 설치판 독스트링 297~299행 「오류 글을 낸다」와 같은 판 미들웨어(`filesystem.py` 2688~2707행)가 어긋남을 b7에 적음.
- 옛 b4 「필수 호출을 보장해야 한다면 … 궤적 검사」·「도구 호출과 `ToolMessage` 존재를 확인」 → 도구 선택은 흔들리는 모델 판단이라 `assert` 대신 흔들림 확인 5번 + 셈으로.
- 옛 b6 「저장된 실행은 … 한 사례」 → 새 커널 두 번 + 흔들림 확인 5번 기준으로 값의 성격을 나눈 표.
- 옛 b10 공통 여섯(가격·라이선스 등) → 이 절 자료(customization·backends·0.7.0 릴리스·설치판 행).

## 9. 그림

- Mermaid **4장**: 02-1(폭 533) · 02-2(676 — 첫 판 920을 도구 세로선을 빼고 그래프 메모로 옮겨 줄임) · 02-3(493) · 02-4(472) — 모두 868 이하, PNG 직접 열어 확인. 보라는 02-2 모델 띠 하나(실제로 부른 모델) · 앞 절반 그림 보라 0 · 빨강 0. 노트북 첨부 02-1 하나(`attached 1`).
- 삽화 **1장** `02-5-도구-걸이에-더한-연장`: 1차 job `53bb1474-a947-4fe5-b387-351bb3521502` 탈락(연장 넷이 자루 두 끝에 머리 — 평범한 물건 아님) → **2차 job `fff0218f-8b07-4272-ac79-0214a982549c` 채택**(재생성 1회, 한도 안). 거래 12:28:04.869699Z·12:29:34.137174Z 「Nano Banana Pro −2」 둘 = **4크레딧**(잔액 2341 → 2337, 바로 앞 거래 11:54:30Z는 01절 몫). 작업 조회 모델 표시 `nano_banana_2`(요청 `nano_banana_pro` — 01과 같은 표시 차이). 저장 1100 × 614 `12a3d67f…`, 다시 받은 원본(해시 같음)을 같은 폭으로 줄여 픽셀 대조 bbox `None`·최대 차이 0. 플러그가 둘로 그려짐(프롬프트는 하나 — 둘 다 꽂히지 않아 관계에 영향 없음, 그림 읽기에 사실대로). 세부 `figures/02-5-도구-걸이에-더한-연장.prompt.md`.
- 옛 그림 `02-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0 — 삭제 승인 목록).

## 10. 뒤 챕터가 이 절에 기대는 문장 (고치지 않음, 참·거짓만)

- `grep -rn 'Ch *27' textbook/part6/ch2[8-9]-*/_src textbook/part7`: **1건** — Ch 28 01 b3 「Ch27에서는 파일시스템과 하위 작업 기능을 미리 조립한 하네스를 사용했습니다」 → **참**(02도 파일 도구·`task`를 기본으로 조립한 Deep Agent를 씀. 「하위 작업」은 Ch 28 몫 말). Part 7 0건.
- 01 b8 「02절에서는 우리 도구를 더하고, 실제 모델이 도구를 고르는 장면을 봅니다」 → **참**(3절 조립 · 6절 실제 모델이 `lookup_rule`을 고름).

## 11. 서비스 요청·비용

- 이 절 모델 요청: 흔들림 확인 **10** + 교재 출력 A **2** + 사본 B **2** = **14번**(탐색 `x1_shape.py`·`x2_seen.py`는 가짜 키 글로 요청 0 — `x2`는 탐색용 훅이 핸들러를 부르지 않고 정해 둔 응답을 내는 **노트북 밖 탐색 전용** 코드). 임베딩 0.
- 예상 비용(요금표 2026-09-17, 청구 금액 아님): 캐시 입력을 빼지 않은 어림 실행당 0.003069달러 × 7 = **약 0.021달러**(흔들림 확인 기록의 캐시 반영 어림은 다섯 번 0.0052달러). 절 1달러 한도 안.

## 12. 강사 확인 대상

1. 제목 「create deep agent와 도구」 유지(밑줄 빠진 함수 이름) — 본문에서 풂.
2. 4절 값 바꿔 보기에 `LocalShellBackend`를 **만들기만** 함(에이전트에 넘기지 않음, 위험 문장 두 곳). 학생이 따라 쓸 위험과 「`execute`가 남는 조건」을 보이는 값의 균형.
3. `@wrap_model_call`을 Ch 27에서 처음 씀(규격 L6 · Ch 22 02 선례 — 01 허용 범위 표에는 없던 데코레이터). 03·06·07·09가 기록 훅을 쓰면 이 판을 이어 씀.
4. 코드 셀 5 → 26, 코드 줄 28 → 132(앞 절반 결정적 비교 + 안전 설정 + 실행·셈).
5. 삽화 플러그 둘(재생성 한도를 씀 — 글로만).
6. 질문 글에 「교육센터 자료실」과 답 길이를 더함(도구 설명과 이어지게, 실행 전에 정함 — b7 「흐름을 보여 주려고 정한 예」).

## 13. 챕터 밖 수정·보호 파일·남은 것

- **챕터 밖 수정**: `textbook/part6/public-files.json`(도구 파일 한 줄, `collect_public_files.py`) · `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json`(`verify.py --chapter`가 다시 씀). 공용 도구·과정 문서·앞 챕터 파일은 고치지 않음.
- 보호 파일(`before-manifest.json` 238개): `manifest-changes.md` 「02절 뒤」 참고.
- 지워야 하지만 지우지 않은 것(삭제 승인 목록): 기기 `/tmp/ch27-02/`(탐색 `x1_shape.py`·`x2_seen.py` · `tools/` · 사본 `A/`·`B/`·`cnt/` · 흔들림 확인 원 기록 `probe/` · 삽화 원본 `illu/`(1차·2차 원본·확대 사본)) · `.cache/ch27-02-view/`(그림 확인 사본 셋 — 이 절이 만듦) · `qa/upgrade/gates-wip-02.json`·`gates-wip-02-02.json` · 옛 그림 `figures/02-흐름.*` · `qa/__pycache__/`. `rm`은 한 번도 부르지 않음.

## 마감 반영 (2026-09-28)

검토 1차(`review-round1-A.md`·`review-round1-B.md`)를 글·그림·기록으로 반영했습니다. **노트북은 다시 실행하지 않았고** 코드 셀은 한 글자도 바꾸지 않았습니다(`code_sha256`·`outputs_sha256`·`executed_at` 전후 같음). 고친 방법: 생성기 문자열 치환(`.cache/ch27-close/tools/gapply.py`·`smartrep.py` — 바뀐 생성기의 `cells()` 코드 셀이 노트북과 다르면 멈춤) → 달라진 마크다운 셀만 노트북에 옮김 → `src_html()`로 `_src` → `run_section.sh … NN --no-exec`. 전체 기록은 `chapter-summary.md`.

- A-6 b6 「두 방법 모두 바깥 에이전트의 요청만 셉니다. 이 수가 전체 요청 수와 같은 것은 도구 `task`를 부르지 않았을 때뿐입니다」 · A-7 b10 「명령을 따로 가둬 실행하는 환경(샌드박스)」·b4 「모델마다 따로 등록하는 설정 묶음(하네스 프로필)」 · A-19 `02-probe.md` §0 머리(「첫 요청(12:13:16Z) 전에 적음」 + 출처)와 이 진단 §4 표현.
- A-14·B-7 「안내 글」 한 뜻: 셀 15·19의 「정해 둔 안내 글」 → 「넣을 수 있는 주제어를 알려 주는 (정해 둔) 글」. 셀 14 `lookup_rule` 주석 「정해 둔 안내 글」은 코드라 그대로 — **다음 재실행 몫**(05 셀 35가 다른 뜻임을 밝힘). A-2 결: 셀 37 「이 훅은 짝 맞추기 미들웨어 뒤에 붙습니다」.
- 마크다운 셀 15·19·37. 노트북 `f031b310` → `bfdade30` · `_src` `5b670ce8` → `077fdc74` · HTML → `1013ac28` · `author_02.py` `24a42ef5` → `ba5faf79`(도구 파일 줄 `TOOLS_HEAD`·`TOOLS` 그대로 — 사슬 통과).
