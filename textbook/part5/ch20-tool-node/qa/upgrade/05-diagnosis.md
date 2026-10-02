# 05절 「ToolNode 실습」 신규 집필 기록 (챕터 끝 실습 절, experiment)

새로 만든 챕터 끝 실습 절입니다(규격 `textbook/QUALITY-UPGRADE.md` §7-2, PLAYBOOK §3, handoff 「§04 → 실습(05)」). 수정 전 원본이 없어 `qa/upgrade/before/`에 넣을 파일이 없고, 게이트는 처음부터 이 절 기준으로 잽니다.

- 작업 2026-09-24(08:15~08:50 UTC) · 생성기 `qa/upgrade/author_05.py`(본문과 노트북을 함께 씀, `--src-only`는 본문만, `AUTHOR05_NB_ONLY=1`은 노트북만, 본은 `author_04.py` — 01 상수 `INSTALL`·`POLICY_DATA`·`BIND`·`STATE`·`CALL_MODEL`·`PATH_MAP`·`STRUCTURE`·`html_text`, 02 `DEF_HANDLER`, 03 `DEF_TOOL`을 import해 씀, 생성기 끝 `assert`로 글자 대조).
- 파일: `_src/05-ToolNode-실습.html` · `labs/part5/ch20-tool-node/notebooks/05-ToolNode-실습.ipynb` · 빌드 `05-ToolNode-실습.html` · `figures/05-1`~`05-4` · `qa/upgrade/05-figures.md` · `qa/upgrade/05-probe.md` · `qa/upgrade/probe/probe05.py`·`probe-05.jsonl` · `qa/upgrade/review-pack/05-ToolNode-실습.md`.
- **슬러그 `05-ToolNode-실습`**, 제목 「ToolNode 실습: 자료실 문의 그래프에 오류 처리 함수와 실행 한도 붙이기」, `chapter.json`에 `format: experiment`로 더함. 규격 §7-2 `{NN+1}-{챕터 이름}-실습`에서 챕터 이름 = `chapter.json` 제목 「ToolNode — 모델이 도구를 고른다」의 앞말(선례 `06-Agent-개요-실습`·`07-워크플로우-패턴-실습`·`07-모델과-도구-실습`·`08-LangGraph-실습`·`09-Middleware-실습`, 인계 권고와 같음).
- **`hours` 그대로**(「총 8h · 강의 3h · 실습 5h」). 이 절 meta는 「실습 30분 · 새 용어 0」이고 챕터 시수에 더하지 않았습니다. `objectives`는 손대지 않았습니다(마감 몫).
- **서비스 모델 절**입니다. 설명만 고칠 때는 `mdpatch.py` → `run_section.sh … 05 --no-exec`.

## 1. 게이트

| 항목 | 값 |
|---|---|
| 게이트(첫 실행 전, 노트북·본문만 쓴 상태) | `upgrade_gates.py … --label wip-05 --section 05` → G1 0 · **G2 1**(3절 `print(…, list(inquiry_state.keys()))` 중첩 호출 두 겹) · G3~G5 0 · **G6 1**(제목 셀 준비물 단락 6문장) · G7 14(그림 전). 둘을 고쳐 **실행 전 G1~G6 0**(`gates-wip-05-05.json`은 고친 뒤 판) |
| 게이트(최종, `--no-exec`) | **G1~G7 모두 0 · PASS**(`gates-wip-05.json`), 코드 셀 **25**(준비 셀 3: 설치·가져오기·키 — 모델 셀은 결과 읽기가 있는 코드 셀), 검사 문장 **357**. 그림 뒤 한 번 G6 2(05-1 도식 읽기 첫 문장 70자 넘음 · 비유 풀이 단락 6문장) → `mdpatch.py`로 고쳐 0 |
| 셀 모양 | 준비 셀이 아닌 셀 주석 뺀 코드 최대 **9줄**(`COST`), 이 절이 새로 정의한 함수 0(노트북의 함수 정의는 01·02 셀 그대로인 `call_model`·`handle_policy_error`·`lookup_policy` 셋, 본문 최대 3줄), 첫 줄 주석 100%. 코드 줄(`count_code.py`) **131** + 도구 파일 33 → 50줄 |
| 새 커널 | `PASS 05-ToolNode-실습.ipynb: 25 cells`. 같은 코드(`code_sha256` `6408399ee855…`)로 **새 커널 두 번** — 셀별 출력 **23/25 같음**(§4) |
| verify | `PASS 5 sections / 135 code cells (max 16 lines)`(16줄은 04절 가져오기 준비 셀의 빈 줄 포함 줄 수) |
| 빌드 | 챕터 HTML 여섯(절 다섯 + `index.html`) `{{` 잔존 **0건**. 05절 HTML에 Mermaid `svg` 3 · 삽화 1 |
| 그림 | Mermaid 3장(`05-1`~`05-3`, 원본 폭 550·746·663, 빨강 0) · 삽화 1장(`05-4`, 2차 채택) |
| 요청 | 노트북 한 번에 **모델 4번**(실행 1 두 번 + 실행 2 두 번 — 실행 2는 한도에 닿아 결과가 없어 노트북 밖에서 셈), 임베딩 0. 규격 §7-2의 3~5번 안 |

- **게이트 밖 AST 검사**(`/tmp/ch20-05/extra_check.py` — 04 판 복사): 노트북 **1건 = 02절 오류 처리 함수의 `error: ValueError`**(02 판 그대로, 챕터 리드 결정 4 · 인계 3번 허용). 도구 파일 **2건 = `estimate_cost`의 `.get` 둘**(04절과 같은 예외). 클래스는 필드만 적은 `AgentState` 하나, 데코레이터 맨 `@tool` 하나, `try` 하나(7절 `except GraphRecursionError as error` — 안에서 출력만, 03절 모양), `assert`는 키 셀 하나. f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`+=`·기본값 매개변수·반환 힌트·튜플 풀기·별표 풀기·`set`/`next`/`sum`/`zip`/`sorted`/`isinstance`·`key=`/`reverse=`·노트북 `.get`·세미콜론·`'__end__'` 글자·`Literal`·`MessagesState`·`perf_counter`·시스템 메시지·`tool_choice`·`create_agent`·체크포인터 0건.
- **01~04에 없던 이름 대조**(`/tmp/ch20-05/newnames.py` — 05 노트북 코드 셀의 이름·속성·키워드 인자·연산자·AST 노드를 01~04 노트북 코드 셀과 대조): 새 내장 이름 0 · 새 속성 0 · 새 키워드 인자 0 · 새 연산자 0 · 새 AST 노드 0 · 새 이름은 이 절 변수 열둘뿐(`inquiry`·`inquiry_state`·`one_result`·`one_row`·`one_steps`·`tight_config` 등). 첫 판의 `>=`(01~04 0건)는 `<`(03절)로 바꿈.
- **금지어 검사**(`/tmp/ch20-05/ban_check.py` — 04 판, 코드 백틱 밖): 노트북 마크다운·코드 주석·`_src`·`.mmd` 셋·캡션 넷 **0건**. `.prompt.md`에만 「프롬프트」(소제목 두 곳 — 01~04와 같은 양식). 「한 겹 더」 0.
- 생성기 대조(`/tmp/ch20-05/gen_match.py`): `cells()` 55개가 노트북과 글자까지 같고 `src_html()`이 `_src`와 같음. 생성기 `assert`: 01 셀 일곱과 글자 같음 · 도구 셀 = 03 셀(01과 AST 같음) · 오류 처리 함수 = 02 7절 셀 · 불러 보는 셀은 02 7절 셀과 AST 같고 첫 줄 주석만 다름 · 안내 글이 `probe05.py`와 같음.

## 2. 주제와 붙인 앞 절 기능 (b3 세 단락)

**주제**: 자료실 창구에 들어온 문의 하나(「자료실에서 일반 도서를 며칠 빌릴 수 있나요?」 — 01절 7절 대출 질문 그대로, 출력 줄 `출처: 01절 7절 대출 질문 그대로, 이 절에서 실행 전에 정함`)를 이 챕터의 그래프로 처리합니다. 실행 1은 한도 10, 실행 2는 한도 하나만 실행 1의 노드 실행 수(3)로.

- **붙인 기능 셋**(인계 「§04 → 실습(05)」 6항 권고 그대로):
  1. **01절 그래프** — 모델 노드 `call_model`·이름표 표 `path_map`·도구 조건 함수·되돌아가는 엣지(셀 글자 그대로), 구조 문자열도 01절 6절과 같은 네 줄. 기록 장치는 01절 10절 함수 `run_row`(도구 파일로 옮김, §5).
  2. **02절 오류 처리 함수** — `ToolNode(tools, handle_tool_errors=handle_policy_error)`(02 7절 모양). 오류 처리 함수는 02 7절 셀 글자 그대로, 받을 오류 표시 `error: ValueError`도 02 판 그대로(허용 범위).
  3. **03절 설정 딕셔너리·실행 한도·명시적 종료** — `limit_config = {"recursion_limit": 10}`(03 4절과 같은 이름·값), `GraphRecursionError`를 `try/except` 안에서 출력만(03 모양), 8절에서 03 6절 규칙(노드 실행 수보다 하나 큰 한도부터 통과)으로 통과 한도를 셈. 명시적 종료는 01절 도구 조건 함수가 맡음(03 b4의 「01절 도구 조건 함수가 END를 골랐다」와 같은 말).
- **고른 까닭**(b3 셋째 단락): 셋 모두 01절 그래프 하나에 붙음(오류 처리 함수는 도구 실행 노드를 만드는 줄에, 한도는 `invoke` 둘째 인자에) · 그래프 모양이 01절과 같아 두 실행에서 바뀌는 것이 한도 하나 · 요청 수는 「모델이 부른 도구 수 + 마지막 답 하나」라 실행 전에 **범위로** 어림(Ch 19 검토 B-10 — 「실행 전에 셀 수 있다」로 쓰지 않음).
- **오류 처리 함수를 붙여 두기만 한 까닭**(b3 넷째 단락·b7): §3 흔들림 확인에서 딕셔너리에 없는 주제를 묻는 문의 두 후보가 모두 조건을 못 채움 → 규칙대로 대출 문의(C). 그래서 **이번 두 실행에서 오류 처리 함수는 쓰이지 않았고**, 4절에서 그래프 없이 한 번 불러 내놓는 글만 보입니다(모델 요청 없음). Ch 19 검토 B-9처럼 넓게 읽히지 않게, 이 함수가 받는 것은 도구가 낸 `ValueError`뿐이고 **한도 오류와 입력 검사 오류는 받지 않는다**를 노트북 7절 결과 읽기·b4 「비교와 경계」·b7·복습 4에 적었습니다(입력 검사 오류는 02절에서 본 장면, 이번에 실행하지 않음).
- **뺀 것과 까닭**(b3 다섯째 단락): 04절 두 그래프 견주기(04 실험 되풀이 — 인계 권고) · 02절 Before 기본값 노드 · 03절 Before 끝나는 엣지 없는 그래프(앞 절에서 결함으로 이미 봄) · 01절 인사·운영·연체 질문(요청 수가 늚). 04 b7 「다루지 않음」(규칙과 모델을 섞은 설계·규칙 차례·걸린 시간)은 새로 풀지 않음.
- **새로 볼 것**(Ch 19 검토 B-11 — 앞 절 값 바꿔 보기와 같은 값을 바꿀 때 초점 한 문장): 03절 6절은 한도(3·4)를 모델 없는 그래프에서 바꿨고, 이 절은 같은 한도를 **모델 요청이 든 흐름**에서 바꿈. b2 둘째 단락 「새로 볼 것은 한도를 그 흐름의 노드 실행 수와 같게 줄인 실행 2입니다. 03절은 이 경계를 모델 없는 그래프에서만 실행했습니다」와 노트북 7절 도입에 적음. 03 b4 「다른 상황에 적용」이 「01절 그래프에도 같은 설정 딕셔너리를 넘길 수 있습니다 … 이번에 실행하지 않았습니다」로 남긴 조합을 이 절이 실행.
- **손으로 적은 새 값**: 새 문의 글 없음(01 글 그대로 — 출처 줄). 실행 2의 한도는 손으로 적지 않고 실행 1에서 센 노드 실행 수를 그대로 씀(`tight_config = {"recursion_limit": one_steps}`), 실행 1의 한도 10은 03절 값. 후보 셋과 차례·판단 규칙은 `05-probe.md` §0에 첫 요청 전에 적었고, b7에 「흐름을 보여 주려고 정한 예이고, 후보와 차례는 첫 요청 전에 적어 두었습니다」.

## 3. 흔들림 확인 — `qa/upgrade/05-probe.md`

- §0(08:20:40Z 기록) → 첫 요청 08:21:04Z. 후보 A → B → C 차례, 회차마다 실행 1(한도 10) → 실행 2(한도 = 실행 1의 노드 실행 수). 노트북 밖에서만 모델 노드 함수에 부른 횟수를 적는 목록을 두어, 결과가 없는 실행 2의 요청 수도 셈.
- **A 「자료실 주차 규정을 알려 주세요.」**(02절 질문): 첫 요청 열 번 가운데 **여덟 번 주제어 `운영`**(결과 상태 `success`, 실행 1 답 글 다섯 번 모두 운영 시간 — 물음과 어긋난 답), **두 번 도구를 부르지 않음**(실행 2 두 회차가 `['model']`로 끝까지 감). 주제어 `주차`를 도구에 넣은 회차 0 → 조건 1·2 불충족.
- **B 「주제어 주차로 자료실 규정을 찾아 주세요.」**: 다섯 번 모두 도구를 부르지 않음(`['model']`, 노드 1, 실행 2 한도 1 → `GraphRecursionError`) → 조건 1 불충족.
- **C 「자료실에서 일반 도서를 며칠 빌릴 수 있나요?」**: **5/5 조건 모두 충족** — 흔적 `['model', 'model']` · `lookup_policy {'topic': '대출'}` · `success` · 호출 ID 짝 `True` · 마지막 응답 요청 0건 · 노드 실행 수 3 · 입력 토큰 164·214 · 실행 2 한도 3 → `GraphRecursionError`, **모델 노드 두 번**(둘째 응답은 요청 0건의 답 글까지 만듦). 흔들린 것은 답 글 쉼표 자리·둘째 응답 출력 토큰(27·28)뿐.
- 요청 **48번**(A 18 · B 10 · C 20), 입력 8,664 · 출력 1,827 토큰, 요금표 어림 약 0.0147달러(청구 금액 아님). 원하는 값이 나올 때까지 다시 보낸 일은 없고, 노트북 실행은 A·B 두 번뿐.

## 4. 새 커널 두 번 실행 (셀별 대조)

| 실행 | UTC(첫 셀 입력 → 마지막 셀 응답) | 코드 | outputs | 비고 |
|---|---|---|---|---|
| **A(교재 출력)** | 08:34:38.9 → 08:34:45.3(약 6.3초) | `6408399ee8553a8b345533c5757058d6395a9297e8c4a31ef1cf6701e54bdf1a` | `1daf319fbe87651cd0fb62623260da448e5253ad243e215f0f727879ba536095` | `run_section.sh … 05`(그림 전이라 첨부 단계에서 `FileNotFoundError`로 멈췄지만 실행은 저장됨), 사본 `/tmp/ch20-05/A.ipynb` |
| B | 08:35:05.1 → 08:35:10.5(약 5.4초) | 같음 | `975d369c99d3…` | 사본 `/tmp/ch20-05/B.ipynb`를 같은 가상환경·`PYTHONPATH`로 `execute.py` |

- **셀별 출력 23/25 같음.** 다른 둘: ① 6절 마지막 응답 셀의 답 글(A 「**1인 5권까지, 14일 동안**」 / B 「**1인 5권까지 14일 동안**」 — 쉼표 하나) ② 9절 사용량·예상 비용 셀(A `output_tokens` 46·`0.000491` / B 45·`0.000486`). 둘 다 결과 읽기 둘째 단락에만 「이번 실행에서는」으로 두고 결론·그림·정리·복습에서 뺌.
- **두 번 모두 같음 → 결론·그림·정리에 씀**(노트북 밖 C 다섯 번과도 같음): `첫 상태의 칸: ['messages', 'trace']` · `내놓은 글: 규정을 찾지 못했습니다(지원하지 않는 주제: 주차). …` · `만든 것의 종류: ToolNode` · 구조 문자열 `__start__ --> model`·`model -.-> __end__`·`model -.-> tools`·`tools --> model`(01절 6절 출력과 같은 넷) · `설정 딕셔너리: {'recursion_limit': 10}`·`실행 흔적 칸: ['model', 'model']`·`메시지 칸의 메시지 수: 4` · `인자: {'topic': '대출'}`·`셋째 메시지의 결과 상태: success` · `기록 한 줄: {'질문': '대출 문의', … '모델 요청 수': 2, '도구 메시지 수': 1, '호출 ID 짝': True}`·`노드 실행 수: 3` · `마지막 응답의 도구 호출 요청 수: 0` · `실행 2의 설정 딕셔너리: {'recursion_limit': 3}` · `받은 오류: GraphRecursionError`·`Recursion limit of 3 reached without hitting a stop condition.` · `셈으로 통과하는 가장 작은 한도: 4`·`False`/`True` · `실행 1 사용량: {'requests': 2, 'input_tokens': 378`.
- 그림은 A·B를 마친 **뒤에** 처음 렌더(Mermaid 08:36, 삽화 제출 08:38). 준비물 `[[RUNSEC]]`, 결과 읽기 둘째 단락 둘(`[[ONE_ANSWER_READ2]]`·`[[COST_READ2]]`), b6 `[[B6_TWICE]]`, 삽화 alt·캡션·그림 읽기·비유 두 단락은 A·B 대조와 그림 확인 뒤 `mdpatch.py`(`/tmp/ch20-05/reps1.json`~`reps3.json`)로 채움 → `run_section.sh … 05 --no-exec` 세 번. **노트북 `code_sha256`·`outputs_sha256`·`executed_at`은 A 그대로**(최종 노트북과 `A.ipynb` 셀별 25/25 같음).
- 준비물 「10초 안에」 = A 셀 실행 기록 약 6.3초(설치 셀 포함, 커널 시작 뺌). 본문은 「걸린 시간은 재지 않았습니다」.

## 5. 도구 파일 `notebooks/graph_tools.py` (§2-7)

- **01절 노트북 함수 둘을 더함**: `call_id_lists(messages)`(01절 7절) · `run_row(question_name, result)`(01절 10절 — 안에서 `call_id_lists`를 불러 둘을 함께). 본문은 01 생성기 상수 `DEF_IDS`·`DEF_ROW`와 **AST 소스 조각 문자열이 같음**(`ast.get_source_segment` 대조), 주석 첫 줄 「# Ch 20 01절에서 배웠습니다 — 01절 노트북 N절의 같은 이름 함수를 옮겼습니다」 + 01 셀 첫 줄 주석(`run_row`는 「도구 메시지 수와 호출 ID 짝은 call_id_lists로 셈」을 덧붙임). 기존 네 함수는 고치지 않음(소스 조각 대조 같음), import 0 그대로(잠금 그대로). 모듈 독스트링에 한 줄 「이 챕터 01절 노트북에서 처음 가르친 함수도 같은 방법으로 옮겼습니다.」를 더함.
- 해시 **`45f8d0de5be5dd198dccc00281edaaf26460caa2e46b3fba3834c3a88da79a8a`(04절 끝) → `34161a6f5fc7f15d7d15ee6a0e5cb20d6f34eaa76b778521fb14c9f7b0c30061`**(코드 줄 33 → 50). 전 판 사본 기기 `/tmp/ch20-05/graph_tools.before.py`.
- **01 노트북**은 두 함수를 노트북 안에서 정의하고 도구 파일에서는 `show_messages`·`tool_call_names`만 가져옴 → 이름 충돌 없음, **다시 실행하지 않음**. 02(`show_messages`·`tool_call_names`)·04(`estimate_cost`·`show_messages`·`sum_usage`)도 가져오는 이름 그대로 — 키 없이 가져오기만 확인. 03은 도구 파일을 가져오지 않음(묶음 키 없는 실행에 영향 없음).
- 05는 `estimate_cost`·`run_row`·`show_messages`·`sum_usage`를 알파벳 순으로 가져옴(`call_id_lists`는 `run_row`가 안에서 부름). 준비 셀 결과 읽기에 고정 세 문장 + 커널 폴더 한 문장 + 「이 절에서 더한 함수 둘 · 배운 절 · 글자 그대로 옮김」.
- 노드·조건 함수·도구·오류 처리 함수(`call_model`·`lookup_policy`·`handle_policy_error`)는 챕터 리드 결정 1대로 노트북에 01·02·03 셀 글자 그대로.

## 6. 그림

- Mermaid 3장(규격 §7-2 조립도 1 · 실행 1 실제 순서 1 · 실행 1·2 비교 1): `05-1-오류-처리-함수와-한도를-붙인-그래프`(b4 조립도 + 노트북 「오늘 볼 그림」, `flowchart TB` + 칸 하나, 폭 **550**, 노드 7 — 첫 상태·설정 딕셔너리 초록, 모델 노드 보라, 오류 처리 함수 파랑, 도구 실행 노드·시작점·끝점 회색, 오류 처리 함수는 도구 실행 노드와 「오류 처리 인자」 선으로만 이음, 도구 조건 함수는 점선 갈래 라벨) · `05-2-실행-1이-지난-단계-셋`(b5, `sequenceDiagram`, 모델 노드 `box Lavender`, 폭 **746** — 첫 렌더 955·887 → 메시지 라벨을 줄이고 마지막 메모를 `over P,M`으로) · `05-3-한도-하나만-바꾼-두-실행`(b6, `flowchart TB` + 칸 둘 + 셈 상자, 폭 **663**, 노드 7 — 받아 출력한 `GraphRecursionError`는 노랑, 노트북 밖 값·03절 규칙 셈 회색; 첫 판의 초록 「바꾼 값」 상자는 노드 수를 줄이려고 칸 제목 「실행 2 · 바꾼 값 한도 3」으로 옮김). **빨강 0**(experiment). PNG를 직접 열어 확인한 뒤 alt·도식 읽기를 고침(`.cache/ch20-05-view/v1-05-1~3.png`·`v2-05-3.png`·`v3-05-2.png`·`v4-05-2.png`). 답 글·출력 토큰·예상 비용은 어느 그림에도 없음. 라벨 숫자(10·3·4)는 모두 노트북 출력에 있음(G7 통과).
- 삽화 **1장** `05-4-받침에-선-상자와-빈-카드-주머니`: 「자료실 승강 상자」 계열의 새 조립 장면 — **통로 하나**(01~04는 모두 둘)에 앞 절 소품을 모음: 받침(03 명시적 종료) 위 상자에 쪽지(도구 호출 요청)와 파란 책(success 도구 메시지), 계수기 판(03 실행 한도, 아래 셋만 켜짐 = 실행 1의 단계 셋), 서고 옆 빈 카드 주머니(02 오류 처리 함수, 그대로). `nano_banana_pro`(응답 `nano_banana_2`) · 16:9 · 2k · `use_unlim: false` · count 1. 생성 전 잔액 **2537.25**.
  - **1차 job `25aed51d-7a07-47d8-af52-2c0329f00558` 탈락** — 구성은 맞았지만 계수기 등이 **열한 개·아래 넷 켜짐**(요청 열 개·아래 셋), 켜진 등 수가 실행 1의 단계 셋과 어긋남. 원본 `1ababe163567…`.
  - **2차 job `1109ab59-ae4b-43ba-a64f-35f77478bb3b` 채택**(재생성 1회 — 상한, 계수기 판만 「위층 벽, 큰 등 정확히 여섯, 아래 셋 켜짐」으로 바꿈). 원본 `0abe450e214b…`(2752 × 1536) → 저장 1100 × 614 RGB `b786645d60e2…`. 결과 URL을 다시 받아(같은 해시) 같은 폭으로 줄여 저장 PNG와 픽셀 대조: bbox `None`, 가장 큰 차이 0. 저장본과 상자·계수기·주머니 확대본을 열어 셌습니다 — 통로 **하나** · 위층 왼쪽 창구 **하나** · 아래층 왼쪽 책장 **하나** · 위층 높이 받침 **하나** 위 상자 **하나**(흰 쪽지 **한 장**·파란 책 **한 권**) · 위층 오른쪽 벽 판 **하나**에 등 **여섯**(위 셋 회색·아래 셋 노랑, 켜진 등 둘레에 짧은 빛살 선) · 아래층 오른쪽 벽 주머니 **하나**(빈 회색 카드 여러 장). 사람·손·화살표·끈·도르래·톱니·집게·화면·글자·숫자 없음. 등 수(여섯)가 한도 10과 달라 b4 풀이에 「판의 등 여섯은 한도 값을 그대로 그린 것이 아닙니다」.
  - 크레딧: 거래 기록 **08:38:11Z · 08:40:04Z 「Nano Banana Pro −2」 두 줄 = 이 절 몫 4크레딧**(그 앞 줄은 04절 08:01:17Z), 생성 뒤 잔액 2533.25.

## 7. 함께 고친 파일

**챕터 안**
- `chapter.json` — `sections`에 05 한 줄(`b15774922c2b…` → `a6cacdda400e…`, `hours`·`objectives` 그대로 — objectives는 마감 몫). 전 판 사본 `/tmp/ch20-05/chapter.before.json`.
- **04절 마지막 문장은 고치지 않았습니다**: b8·노트북 정리 끝 줄 「05절 실습에서는 이 챕터에서 만든 그래프와 함수를 모아, 자료실 문의 하나를 처리합니다.」 — 05가 01 그래프·02 오류 처리 함수·03 설정 딕셔너리·01 `run_row`를 모아 대출 문의 하나를 처리하므로 **그대로 참**. `mdpatch.py`·`--src-only` 쓰지 않음, 링크도 더하지 않음(Ch 19 06 선례). **04 노트북 `e790caf40829…` · `code_sha256` `b0920807d041…` · `outputs_sha256` `a0bcc06b99fd…` 그대로**, 04 `_src` `7fdd54080015…` 그대로. **04 빌드 HTML만 `2ed4edab…` → `7020937a…`**: `_build.py`가 다음 절 링크를 「챕터 끝」에서 05절 링크로 바꾼 한 줄뿐(그 한 줄을 「챕터 끝」으로 되돌리면 `2ed4edab3481…`와 같음을 확인). 01~03 노트북·`_src`·빌드 HTML 해시 그대로.
- 새 파일: 노트북 05 · `_src/05` · 빌드 `05-ToolNode-실습.html` · `figures/05-*`(mmd 3·svg 3·png 4·render.json 3·caption 4·prompt 1) · `qa/upgrade/author_05.py` · `05-figures.md` · `05-probe.md` · `05-diagnosis.md` · `probe/probe05.py`·`probe-05.jsonl` · `gates-wip-05.json`·`gates-wip-05-05.json` · `review-pack/05-ToolNode-실습.md`. 챕터 `index.html`(05 링크) 다시 빌드(`628a5471…` → `868c1dcb5489…`).
- `qa/upgrade/handoff.md` 「실습 → 챕터 검토」 · `집필점검표.md` 품질 개선 표 05 행 · `qa/verification.md` 품질 개선 검증 표 05 행 · `qa/upgrade/manifest-changes.md`(05 줄).
- 챕터 `qa/public-files.json`은 **고치지 않았습니다** — `include`가 `notebooks/*.ipynb`·`notebooks/graph_tools.py` 글롭이라 05 노트북이 자동으로 들어갑니다(새 zip에 있음 확인).

**챕터 밖**
- `labs/part5/ch20-tool-node/README.md` — 맨 아래 **05절 한 단락만** 더함(`cea28211feff…` → `f6157253cef4…`, 전 판 `/tmp/ch20-05/README.before.md`). 옛 두 문장(「예상 비용이 절당 1달러 미만인지 검사」 등)은 손대지 않음 — 마감 몫.
- `labs/part5/ch20-tool-node/notebooks/graph_tools.py` — 함수 둘 더함(§5).
- `textbook/part5/index.html` · `textbook/downloads/part5-practice.zip` · `textbook/part5/qa/integration-results.json` — `python3 textbook/part5/_build_index.py`로 다시 만듦(**`Part 5: 25 verified sections; 65 bundled files`**, zip 항목 68). 목차 `8bcdb27a9968…` → `262d21122e0f…`, zip `72d3e3e78683…` → **`6d8846e3ea4be34e3176b7632329530e67c528aa530bb47f7b6ddd220d46cc68`**, `integration-results.json` `d4b45da69244…` → `576a2ca84932…`. 새 zip에 05 노트북·새 도구 파일·05 단락 README가 처음 들어감. `_build_index.py`는 절 수를 링크 수로 세어 고칠 줄이 없음 — 25행 Ch 20 설명(「고정 **분기**와 모델 선택을 비교합니다」, 실습 절 없음)은 마감 몫이라 그대로.
- `textbook/_notebook/checks/notebook-contracts-part5-ch20-tool-node.json` — `verify.py --chapter`가 다시 씀(`ba6b6e0c37dd…` → `d2e6286f45e7…`).
- **`textbook/part5/public-files.json`은 고치지 않았습니다**(도구 파일은 01절이 이미 올림, 노트북은 슬러그로 자동). 공용 도구(`textbook/_notebook/`·`textbook/_template/`) 코드·규격·과정 요약·계약 파일·완료 챕터·Ch 21 파일은 고치지 않았습니다.

## 8. 검사 스크립트가 멈춘 자리

- `python3 textbook/part5/qa/check_delivery.py` — **115행 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`**(`llm-practice.zip`)에서 멈춤(Ch 14~19 때와 같은 자리, 전체 마감 몫). 멈춰서 `qa/delivery-results.json`은 다시 쓰지 않았습니다(`a446579388c4…` 그대로).
  - 같은 대조를 `llm-practice.zip`만 빼고 파일을 쓰지 않게 따로 돌린 결과(`/tmp/ch20-05/delivery_no_llm.py`): **HTML 31쪽 · 절 25 · 로컬 링크 576 · 누락 0 · 비밀값 노출 0 · 복습 문제 100 · 오류 0 · `part5-practice.zip` 항목 68 · part5 노트북 25 = 절 25**.
- **학생 묶음 확인**(규격 §7-2): 새 zip에서 Ch 20 폴더만 `/tmp/ch20-05/bundle/`에 풀어, `notebooks/` 폴더에서 `OPENAI_API_KEY` 없이 `from graph_tools import estimate_cost, run_row, show_messages, sum_usage` → 통과(묶음 안 새 도구 파일을 가져옴). 05는 모델 셀이 있어 키 없는 새 커널 전체 실행은 하지 않았습니다.
- `check_bundle_execution.py`(Ch 20 03을 키 없이)는 돌리지 않았습니다(마감 몫 — 03 노트북은 도구 파일을 가져오지 않아 이 절 변경의 영향 없음). 옛 검사 스크립트 `check_scope.py`(`SECTION_COUNTS` ch20 = 4)는 05와 어긋나 멈출 것 — 돌리지 않음(기록만).

## 9. 보호 파일 50개

`before-manifest.json` 50개 — 작업 시작(08:1x, 49개 같음·1개 다름 = 04절 끝과 같음)과 끝(08:45)에 다시 계산: **48개 같음, 2개 다름** = `textbook/part5/public-files.json`(01절 값 `77511382e222` 그대로) + **`textbook/downloads/part5-practice.zip` `72d3e3e78683` → `6d8846e3ea4b`**(작업 지시 §4대로 `_build_index.py`로 다시 만든 결과 — `manifest-changes.md`). 05절이 새로 바꾼 보호 파일은 이 zip 하나. `check_bundle_execution.py`·`bundle-execution.json`·`build_bundle.py`·Ch 17 05 자료는 그대로.

## 10. 요청 수 · 비용

- 노트북 실행 한 번 **4번**(실행 1 두 번 + 실행 2 두 번 — 규격 §7-2 3~5번 안, 준비물 「모두 4번」·「모델이 도구를 몇 번 부르느냐에 따라 달라질 수 있음」). 작업 합계 **56번**(노트북 밖 48 + 새 커널 A 4 + B 4), 모두 `gpt-5.4-mini`(응답 `gpt-5.4-mini-2026-03-17`), 임베딩 0, 오류 0. 모델 없는 확인(도구 파일 가져오기·`run_row` 손 메시지·묶음 가져오기)은 0번.
- 사용량 합: 입력 약 10,180 · 출력 약 2,010 토큰(밖 8,664·1,827 + A·B 각각 입력 756·출력 약 91). 요금표(Ch 6 06, 2026-09-17: 100만 토큰당 입력 0.75 · 캐시 입력 0.075 · 출력 4.50달러)로 어림하면 **약 0.017달러**(청구 금액 아님). 노트북 한 번은 약 0.001달러(실행 1 `0.000491` + 실행 2 비슷한 크기, 실행 2는 사용량을 받지 못함).
- 삽화 두 장(1차 탈락·2차 채택) 4크레딧(§6).

## 11. 강사 확인 대상

1. **오류 처리 함수를 붙여 두기만 한 설계** — 흔들림 확인 규칙대로 대출 문의(C)를 쓰게 되어, 02 기능이 흐름 안에서 일하는 장면이 없습니다(4절에서 그래프 없이 부른 글만). 대신 「주차를 물으면 모델이 운영을 찾아 오류 없이 어긋난 답을 쓴다」(노트북 밖 A 결과)를 b7·복습 4에 적었습니다. 흐름 안 오류 처리 장면을 꼭 보이려면 손으로 만든 요청(02 모양)이나 `tool_choice`(과정 미교육)가 필요합니다.
2. **실행 2의 모델 요청 수 2는 노트북에서 셀 수 없음** — 한도에 닿으면 `invoke`가 결과를 내놓지 않아, 노트북 밖에서 모델 노드 함수에 부른 횟수를 적어 셈(준비물·b5·b7에 밝힘). 노트북에서 세려면 노드 함수에 기록을 더해야 해 01 셀과 달라짐.
3. **실행 2 한도 = 실행 1 노드 실행 수**(코드로 정함) — 모델이 실행 1에서 도구를 다른 수만큼 부르면 두 실행의 한도가 함께 달라짐(b7). 한도 4(통과 쪽)는 실행하지 않고 03 규칙으로 셈만.
4. 삽화 `05-4` 2차 채택본의 계수기 등 여섯(한도 10과 다름 — b4에 한 문장) · 켜진 등의 짧은 빛살 선.
5. 코드 셀 25(실습 선례 20~25 위 끝), 이 절이 새로 정의한 함수 0, 도구 파일에 01 함수 둘.
6. 한국어 감사 3단·그림 판독은 별도 세션 몫.

## 12. 챕터 마감 몫 (이 절이 더하거나 확인한 것 — handoff 「실습 → 챕터 검토」 §5에 모음)

- `chapter.json` `objectives`(셋째 「분기」·「trace」·「지연」, 실습 줄을 넣을지) → `_build.py` · `textbook/part5/_build_index.py` 25행 Ch 20 설명(「분기」, 실습 절) · `textbook/_notebook/build_index.py` 44행(절 수 4 → 5?, 다른 챕터 선례는 실습 절을 뺀 수).
- 실습 폴더 `README.md` 전체 다시 쓰기(05 단락은 이번 판) → `part5-practice.zip` 재생성 → `check_bundle_execution.py`(Ch 20 03) → `bundle-execution.json` 03 `code_sha256` `50ae424d8b20…` → `877f2261aa0a…`.
- `check_scope.py` `SECTION_COUNTS`(기록만) · `check_delivery.py`(`llm-practice.zip` Stale — 전체 마감) · `gates-after.json` · `visual.cjs` 1280px·390px(HTML 여섯) · `chapter-summary.md`(**실습 30분은 챕터 시수에 더하지 않음**, 05는 새 문법·API·말 0, 도구 파일 함수 여섯).

## 13. 지우지 않은 것 (삭제 승인 대상)

- `qa/upgrade/gates-wip-05-05.json`(첫 실행 전 게이트 — `gates-wip-05.json`으로 갈음) · `qa/upgrade/__pycache__/`(`author_01`~`author_05` import로 생긴 `.pyc`가 있을 수 있음 — 이 절은 `PYTHONDONTWRITEBYTECODE=1`로 부른 곳이 많지만 `run_section.sh`는 그 변수 없이 생성기를 부름).
- 프로젝트 `.cache/ch20-05-view/`: Mermaid 확인 사본 `v1-05-1~3.png`·`v2-05-3.png`·`v3-05-2.png`·`v4-05-2.png`, 삽화 `illu-1-1100.png`·`illu-2-1100.png`·`saved-05-4.png`·`crop-lamps.png`·`crop-box.png`·`crop2-box.png`·`crop2-lamps.png`·`crop2-pocket.png`.
- 기기 `/tmp/ch20-05/`: `protect.py`·`protect-start.txt`·`protect-end.txt`·`start-hashes.txt`·`now.txt` · `chapter.before.json`·`README.before.md`·`graph_tools.before.py` · 생성기 조각 `part1.py`~`part5.py` · `probe-05.jsonl` · `A.ipynb`·`B.ipynb`·`A-start.txt` · `reps1.json`~`reps3.json` · `extra_check.py`·`ban_check.py`·`newnames.py`·`cmpnb.py`·`gen_match.py`·`delivery_no_llm.py`·`shrink.py`·`cmpimg.py`·`crop.py` · 삽화 `illu-1-orig.png`·`illu-2-orig.png`·`illu-2-again.png`(각 2752px)·`illu-1-1100.png`·`illu-2-1100.png`·`crop-lamps.png`·`crop-box.png`·`crop2-*.png` · 묶음 확인 `bundle/part5-practice/labs/part5/ch20-tool-node/…`.
- 실습 폴더 `notebooks/__pycache__/`(도구 파일 가져오기로 생긴 `graph_tools.cpython-312.pyc`가 갱신됐을 수 있음).

## 마감 반영 (2026-09-24, 검토 1차 B·A-9 — 노트북 다시 실행하지 않음)

- **B-8 [중] (가)**: 설계 유지. 학습 목표에 「붙여 둔 오류 처리 함수가 이번 흐름에서 쓰였는지, 도구 메시지의 결과 상태로 확인할 수 있습니다」를 더함(목표 넷) · 「이 노트북에서 할 일」 2 같은 뜻 · b2에 「오류 처리 함수는 붙여 두었지만 이번 두 실행에서는 쓰이지 않았습니다 · 실행 1에서는 결과 상태 `success`로 그 사실을 확인합니다」 · b3 표 02절 행 「흐름에서는 쓰이지 않음(결과 상태 `success`로 확인)」. 제목은 유지(붙인 것은 사실). 강사 확인 대상.
- **B-12**: 05-1 오류 처리 함수 상자를 양옆 세로줄 상자(`[[…]]`)와 「이번 흐름에서 쓰이지 않음」 줄로, 캡션·alt·「도식 읽기」(본문·노트북 「오늘 볼 그림」) 같이 → `--force` 다시 렌더(폭 550 → 549), 노트북 첨부 PNG 새 판(`42338beb37b2…`).
- **B-9 [중]**: b6 넷째 단락을 둘로 — 「실행 2처럼 노드 실행 수와 같은 한도로는 같은 흐름도 멈췄습니다 · 통과하는 가장 작은 한도(노드 실행 수 + 1)에 맞춰도, 도구를 한 번 더 부르는 실행은 셈으로 한도에 닿습니다」.
- **B-10**: b5·제목 셀 준비물을 「실행 1은 2번 · 실행 2는 노트북에서 셀 수 없고 노트북 밖 다섯 번에서 2번 · 모두 4번으로 어림」 차례로.
- **B-11**: b6 「같은 경계를 보였습니다」 → 「03절 경계의 멈추는 쪽과 같았습니다」 · 노트북 7절 앞 「그 경계의 멈추는 쪽을 봅니다」.
- **B-13**: 05-4 PNG를 직접 봄(등 여섯, 아래 셋 켜짐). 그림 읽기 → 「계수기 판은 한도 10을 등 여섯으로 줄여 그렸고, 켜진 등 셋만 실행 1이 지난 단계 셋입니다」. 다시 만들지 않음.
- **B-14**: b8·노트북 정리 끝 「네 부품을」 → 「반복 구조를」(설치판 `create_agent`는 `tools_condition`을 쓰지 않음 — 검토 B 확인).
- **B-15·A-9**: 복습 4 → 「이 오류 처리 함수는 도구 몸통이 낸 `ValueError`만 받도록 좁힌 설계 · 한도 오류는 받지 않아 멈춤 · 02절 8절의 입력 검사 오류도 받지 않음」(노트북 밖 주차 → 운영 관찰은 b7에만) · b7 오류 처리 함수 항목에 「02절 판 그대로 좁힌 설계 · 입력 검사 오류까지 받는 방법은 이번에 실행하지 않았습니다」.
- **B-16**: `05-figures.md` 폭 칸 549·746·663.
- A-7 결 맞춤: [22] 결과 읽기 「받을 오류 표시가 `ValueError`라서 …」 → 「02절에서 본 설치판 소스대로면, 받을 오류 표시가 `ValueError`인 이 함수에는 다른 종류의 오류가 넘어오지 않습니다」.
- 결과: 노트북 `code_sha256` `6408399ee855…`·`outputs_sha256` `1daf319fbe87…`·`executed_at` 그대로, 파일 `32252e12e8de…` → `8db65a774a36…`. `_src` `1a8c53d2b785…` → `0dbe492657ef…`, 생성기 `360965cd3c63…` → `0187366a725f…`. 게이트 0(검사 문장 361).
