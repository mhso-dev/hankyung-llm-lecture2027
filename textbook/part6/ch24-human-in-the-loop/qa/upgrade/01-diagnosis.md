# 01절 진단 — interrupt 승인 게이트 (paired)

- 작업일 2026-09-25 · 생성기 `qa/upgrade/author_01.py`(`0eb074b1…`) · 노트북 `labs/part6/ch24-human-in-the-loop/notebooks/01-interrupt-승인-게이트.ipynb`(`9f25361b…`) · 도구 파일 `notebooks/approval_tools.py`(**새로 만듦**, `b40aab98ae6ddd87cb4a0107403193c33d9978c436f1a20cf493873458950a93`) · 본문 `_src/01-interrupt-승인-게이트.html`(`5960408b…`) · 빌드 HTML `01-interrupt-승인-게이트.html`(`09f46b30…`).
- 형식 **paired 유지**, 슬러그 그대로(Ch 23 07 b8 링크), 절 meta 「강의 1h | 실습 1.5h | 새 용어 3」(시수 그대로 — 챕터 합 3h·5h 유지).
- **모델 요청 0번 · API 키 셀 없음**(챕터 리드 결정 1, M1). 사람의 답은 셀에 적은 값(`"approve"`·`"reject"`)을 `Command(resume=…)`에 넣습니다 — 준비물·b5에 그 문장.

## 1. 게이트 전후

| 구분 | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 4 | 77 | 3 | 4 | 0 | 0 | 5 | 18 | 3 | **33** |
| 첫 실행 전(`gates-wip-01-01.json`) | 28 | — | 0 | 0 | 0 | 0 | 0 | 4 | 18 | 22(G6 4는 실행 전 고침, G7은 그림 전) |
| 마지막(`gates-wip-01.json`, `--no-exec`) | **28** | **383** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 게이트 밖 확인(규격보다 좁은 과제 기준): 준비 셀이 아닌 셀 최대 **9줄**(≤10) · 함수 본문 최대 **8줄**(`ask_then_charge`, ≤8) · 셀당 정의 하나 · 정의 넷(노드) + 상태 형식 하나.
- AST 따로(`/tmp/ch24-01/tools/extra_check.py` — Ch 23 마감 판 복사): 노트북·도구 파일 금지 문법 **0건**, 허용 표시만(키워드 없는 `sorted` 하나 — 마지막 셀 파일 목록, Ch 23 선례). f-string·내포식·제너레이터 식·조건 표현식·`lambda`·`elif`·`next`·`set`·`.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·튜플 풀기·별표 풀기·`{**…}`·`while True`·숫자 밑줄·`try`·`Path`·`unlink`·데코레이터·세미콜론 0.
- 금지어(`/tmp/ch24-01/tools/ban24.py` — Ch 23 목록 + payload·snapshot·포인터·소비·게이트·HITL·재실행·재개·중단·갈래·time travel·fork·직렬화·리듀서·결정적·**조각**·반환값): 노트북 설명·주석·`_src`·캡션·`.mmd`·도구 파일에서 참 금지어 **0건**. 남은 걸림은 모두 거짓 양성 — 「체크포인터」 안 「포인터」, 「프로그램」 안 「로그」, 절 제목 「승인 게이트」와 그 풀이·Ch 18 01 「게이트」 구분 문장, Ch 23 03 용어 「스레드 재개」를 가리키는 구분 문장.
- **「조각」은 첫 판 비유에 있었고 고침**: 과정 용어 「조각 = 토큰 전용」(Ch 5)과 겹쳐 도미노 비유 여덟 자리를 「도미노」·「도미노 하나」로 바꿈(`mdpatch.py`, 코드·출력 변화 없음).

## 2. 수정 전 주요 문제 (옛 판 `before/notebooks/01-…ipynb`·`before/_src/01-*.html`)

1. **파일 쓰기가 실습 폴더 맨 위**(`approval-effects.txt`) + `unlink` 두 줄 — 연결 폴더에서는 지우기가 막혀 제자리 실행이 멈출 모양이고, 학생 폴더에 파일이 남음. 경로 셀은 `[Path.cwd(), *Path.cwd().parents]`·`next(… for …)`(규격 §2-3 금지 모양)·한 글자 `p` 둘.
2. 셀 17·18줄, 노드 타입힌트·반환 힌트, 조건 표현식 `"approved" if approved else "rejected"`, 상태 형식 이름 `State`(칸 구성이 다른 02·03도 같은 이름).
3. 설명 셀에 결과 읽기 0 · 제목 셀·준비물·그림 첨부 없음 · b5 「확인할 점」 = b6 둘째 단락(같은 글 두 번).
4. 금지어·어려운 말: 반환 12 · 경로 8 · 런타임 3 · 직렬화 3 · payload 5 · 분기 · 재시작 · 적절 · HITL · 「승인 게이트」(Ch 18 「게이트」와 겹침).
5. **재지 않은 속도 단정**: b5 「읽기 전용 검색까지 매번 승인받으면 흐름만 느려질 수 있으므로」 → 뺌. b4 다른 상황 둘째 단락은 「어떤 도구·어떤 인자에 승인 지점을 둘지는 서비스가 정할 일 … 읽기만 하는 일에 묻는 장면은 만들지 않았습니다」로 바꿈.
6. b7 「interrupt를 try/except로 감싸면 …」은 실행하지 않은 문장 → 노트북 밖 확인 결과와 「노트북에서 실행하지 않았습니다」를 함께 적음(§5).
7. `Command(resume=…)`와 Ch 23 03 「스레드 재개」·04·06 worker `resume` 단계를 가르는 문장 없음 → b3 셋째 단락과 노트북 3절에 첫 자리 구분 문장.
8. 그림: `{{svg:01-흐름}}` 한 장(옛 `_gen_figures.py` 상자 넷), Mermaid·삽화 0.

## 3. 바꾼 것 (결정)

- **Before/After(결정 3)**: 상태 형식 `ApprovalState`(칸 `order_key`·`record_name`·`answer`, 규칙 없음 — Ch 13 01 모양). Before `charge_then_ask` = `append_key` → `interrupt` → 답을 칸에. After `ask_then_charge` = `interrupt` → 답이 `approve`일 때만 `append_key`. 노드 안 `print("노드 … 시작")`으로 **노드가 이어 갈 때 처음부터 다시 실행되는 것**을 셀 출력에 보임(After도 두 번 시작 — 거절이 쓰기를 막은 까닭이 「노드가 다시 실행되지 않아서」가 아님을 보임).
- **예시 부분(2·3절)**: 파일을 쓰지 않는 `ask_only`로 멈춤 표시 → 결과 키 `__interrupt__` → 멈춤 표시 수·종류·질문 값(아이디는 출력하지 않음) → `get_state` 다음 노드·칸 값 → `tasks[0].interrupts[0].value`·체크포인트 2 → `Command(resume="approve")` → 시작 줄 다시·`받은 답: approve` → 다음 노드 `()`·체크포인트 3(`assert`).
- **값 바꿔 보기**: After에 답 하나만 `approve`(새 스레드·새 파일 `after-approve`) → 한 줄(`assert`).
- **6절(After 부분) 멱등 앞쓰기**: `receive_then_ask` = `append_key_once`로 접수 기록 → `interrupt`. 거절로 이어 가도 `적음` → `건너뜀`, 한 줄. 「멱등하면 두 줄은 막지만 거절해도 한 줄은 남는다 → 되돌리기 어려운 일은 묻고 나서」 — Ch 23 06과 잇는 문장(b4 「다른 상황에 적용」·b6 넷째 단락·b9 문제 4). **Ch 30 06 「Ch24의 중복 실행 방지 원칙」이 기대는 문장이 실행 근거와 함께 남음.**
- **네 장면 견주기 표**(6절 끝) — 노드 | 답 | 기록 파일 | 같은 키 줄 수: `2`·`0`·`1`·`1`. 마지막 셀 파일 목록 `['after-approve.record', 'before.record', 'receipt.record']`.
- **파일 쓰기(결정 2)**: 준비 셀 셋(설치 → 가져오기(도구 파일 포함, 작업 위치를 옮기기 전) → 임시 폴더). 임시 폴더 셀은 **Ch 23 01 셀에서 앞머리 `ch23-01-` → `ch24-01-`(세 곳)와 주석 선례 「(Ch 4 03절과 같은 모양)」 → 「(Ch 23 01절과 같은 모양)」만 다름**(생성기 `assert` — Ch 23 `author_01.py`에 원문이 있는지까지). **지우는 줄 0** — 장면마다 다른 기록 파일 이름(`before.record`·`after-reject.record`·`after-approve.record`·`receipt.record`)을 새 임시 폴더에 씀. 셀 하나만 다시 실행하면 같은 스레드·파일에 이어 적어 값이 달라짐 → 준비물·b7에 「1절 임시 폴더 셀부터」(Ch 23 06 2절 선례).
- **설치 셀**: `%pip install -q "langgraph==1.2.11" "langgraph-checkpoint==4.2.0"`(잠금 판, Ch 23 01과 같은 둘). `dotenv` 가져오기 없음.
- **셀 수 4 → 28**, 코드 줄(`count_code.py`, 주석·빈 줄 뺌) **50 → 158**(+108) · 도구 파일 17줄. 02·03 그대로. Ch 23 01(32 → 113)과 같은 늘어남 — 강사 확인 대상(§8).

## 4. 새 커널 실행

- 노트북 밖 먼저(`/tmp/ch24-01/T/` 사본, `execute.py`, 키 없이) `PASS 28 cells` — 실습 폴더에 `.failure.json`이 남지 않게 사본으로 먼저 확인.
- **A** `run_section.sh … 01`(`PYTHONDONTWRITEBYTECODE=1`, `env -u OPENAI_API_KEY`) → `PASS 01-interrupt-승인-게이트.ipynb: 28 cells`, 셀 실행 13:50:55.28~56.31Z(UTC), `code_sha256` **`7187f7a39f3fbd146120412daf4d9675ecf132703117570348b3b570744595ab`**, `outputs_sha256` `fbaaa8908bd1…`. (그림이 아직 없어 첨부 단계에서 멈춘 것은 예정대로 — 그림 뒤 `--no-exec`로 이음.)
- **B** 사본(`/tmp/ch24-01/B/B.ipynb` + 도구 파일 사본, `execute.py`, 같은 환경 변수, 13:51:07.70~08.70Z) → PASS. **셀별 출력 28/28 같음**(`cmpout.py`), `outputs_sha256` A·B 모두 `fbaaa8908bd1…`.
- 그 뒤 설명만 고침(`mdpatch.py` 세 번 — 실행 시간 줄 「2초 안에」·「조각」 → 「도미노」·b6/b10 글) → 노트북 코드·출력·`metadata.verification` 그대로(`executed_at` 13:50:56Z).
- 실습 폴더 `notebooks/__pycache__` 만들지 않음(`PYTHONDONTWRITEBYTECODE=1`, 생성기는 `python3 -B`).
- 실수 기록: 확인 중 환경 변수 없이 `uv run --project labs/part6/ch24-human-in-the-loop …`를 한 번 불러 실습 폴더 `.venv/.lock` 지우기에서 `Operation not permitted`로 멈춤 — `.venv` 안 파일 mtime을 확인해 **바뀐 것 0**(모두 09-10), verify는 `run_section.sh` 판으로 확인.

## 5. 키 없는 묶음 모양 실행 확인 (결정 5, Ch 20 03 선례)

- `/tmp/ch24-01/bundle/part6-practice/labs/part6/ch24-human-in-the-loop/`에 **Part 6 공개 목록의 Ch 24 파일 일곱**(README·`pyproject.toml`·`uv.lock`·노트북 셋·`approval_tools.py`)만 복사 → `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=symlink uv sync --locked`(`.venv` 새로 — `dotenv` 없음 확인: `ModuleNotFoundError: No module named 'dotenv'`) → 묶음 검사와 같은 명령 `uv run --project <lab> --with nbclient==0.11.0 --with python-dotenv==1.2.3 python textbook/_notebook/execute.py <노트북> --cwd <lab>/notebooks --kernel-python <lab>/.venv/bin/python`, `env -u OPENAI_API_KEY -u PYTHONPATH`, 작업 위치는 `.env`가 닿지 않는 `/tmp` 아래 실습 폴더.
- 결과 **`PASS 01-interrupt-승인-게이트.ipynb: 28 cells`**, `status passed`, `code_sha256`이 묶음 안 값과 같음(`7187f7a39f3f…` — 검사의 `assert` 조건), 셀별 출력 A와 **28/28 같음**. `outputs_sha256`만 `1c27f8cfe46f…`로 다름 — 설치 셀 출력이 스트림 둘로 나뉘어 온 차이뿐(글은 같음, 과정 요약 §9 「outputs_sha256은 흔들림」).
- 도구 파일은 `--cwd notebooks`로 커널이 그 폴더에서 시작해 가져옴(PYTHONPATH 없이). **`bundle-execution.json`·zip은 고치지 않음 — 마감 몫**: 지금 `part6-practice.zip`(`aa82b386…`)에는 옛 01(`718171990c5d…`)이 들어 있어 검사는 옛 판으로 통과함. 마감에서 zip을 다시 만든 뒤 `check_bundle_execution.py`를 돌리면 새 `code_sha256` `7187f7a39f3f…`로 기록됨.

## 6. 도구 파일 `approval_tools.py` (결정 4, B안)

- 함수 셋, Ch 23 `checkpoint_tools.py`(`a850b2cd…`)의 같은 이름 함수를 **본문 글자 그대로**(생성기 `check_same_as_ch23()` — 머리 주석·설명 주석·본문 한 덩어리가 Ch 23 파일에 있는지 문자열 대조 + AST 대조): `read_record`(`# Ch 23 04절에서 배웠습니다 — 04절 노트북 3절의 같은 이름 함수를 옮겼습니다`) · `append_key`·`append_key_once`(`# Ch 23 06절에서 배웠습니다 — 06절 노트북 2절의 같은 이름 함수를 옮겼습니다`). import `os` 하나, SQLite·langgraph 없음, 전역 이름 기대기 0, 금지 문법 0.
- `read_record` 설명 주석은 Ch 23 04 그대로 「노드 이름」 — 머리 독스트링에 「이 챕터에서는 주문 키를 읽습니다」 한 줄. `print_history`는 01이 쓰지 않아 넣지 않음(03이 쓰면 03이 더함).
- 노트북 준비 셀 결과 읽기에 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 … 작업 위치를 옮기기 전에 가져왔습니다」 + 「교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어 …」(Ch 19·23 선례).
- **묶음 목록**: 챕터 `qa/public-files.json` 13 → 14줄(`52d2b01c…` → `c629078f134d8b03144aca6a0c9e82c1adb0fa9d9c4b745fa610e9f382f95d2c`) → `python3 textbook/part6/qa/collect_public_files.py`(`Explicit public files: 81; prerequisites: 13`) → `textbook/part6/public-files.json` 한 줄 더함(`8ed6852b…` → `a77415947a7ed58e7505a8241974b5e4397e86d3c346ca8fd48b5302d0638d27`), `prerequisite-files.json` 바이트 같음(`4c7f5a4b…`).

## 7. 그림

- Mermaid **4장**(설계표 `01-figures.md`): 01-1 차례(폭 241) · 01-2 멈춘 동안 남은 것(284) · 01-3 Before/After 같은 거절(576) · 01-4 네 장면 줄 수(576) — 모두 868 이하, PNG 네 장 직접 열어 확인. 첫 렌더에서 저절로 꺾인 라벨 셋을 `<br>`로 미리 나눠 다시 렌더. **빨강은 Before 결함 결과만**(01-3 「거절인데 같은 키 두 줄」·01-4 `charge_then_ask` 상자), **보라 0**, 공통 사실 회색, 넣은 값·사람의 답 초록, 노드·부른 줄 파랑, 출력 노랑. 라벨 숫자는 `2401` 하나(출력에 있음).
- 삽화 **1장** `01-5-빈자리-앞의-컵과-빈자리-뒤의-컵`: job **`fb67df97-9798-43b5-b80c-cb1cdcf01e37`**, **1차 채택(재생성 0)**, 거래 2026-09-25T13:52:58Z 「Nano Banana Pro −2」(이 절 몫 **2크레딧**, 생성 전 잔액 2431.75 · 바로 앞 거래 11:32:55Z는 Ch 23 07 몫). 원본 `dd2bcb50…`(2752×1536) → 1100×614 `f66b7c27…`, 다시 받은 결과와 **픽셀 대조 차이 0**(bbox `None`). 저장 PNG와 같은 사본을 열어 셈: 도미노 두 줄, 줄마다 빈자리 하나, 위 줄 컵 하나가 빈자리 왼쪽에서 쓰러짐, 아래 줄 컵 하나가 빈자리 오른쪽 끝에 섬, 글자·숫자·사람·손 없음(자세히는 `.prompt.md`).
- 비유 계열 **「도미노 줄과 비워 둔 자리」**를 이 절이 엶(챕터 리드 결정 10).
- 옛 그림 파일 `figures/01-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0 — 챕터 공개 목록 줄 빼기는 마감 몫).

## 8. 강사 확인 대상

1. 제목 말 「interrupt」·「게이트」(본문은 「멈춤 표시(interrupt)」·「승인 지점」, 제목 「승인 게이트」 = Ch 17 02 승인 지점 · Ch 18 01 게이트와 다름을 b2·노트북 1절에 한 문장).
2. 모델 없는 절(M1) — 사람의 답은 셀에 적은 값.
3. 6절 멱등 앞쓰기 장면을 더함(옛 판에 없던 실행 — b7 문장을 실행 근거로 바꿈) · 값 바꿔 보기 `approve` · 노드 안 `print`.
4. 코드 줄 50 → 158(셀 4 → 28) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘.
5. 새 도구 파일 `approval_tools.py`(Ch 23 함수 셋 복사) — 챕터마다 따로 두는 선례대로.
6. 용어 「멈춤 표시」·「질문 값」·「사람의 답으로 이어 가기」(§9) — 02·03이 이어 씀.

## 9. 용어 (01이 정함 — `handoff.md` 표와 같음)

| 말 | 뜻 | 코드 |
|---|---|---|
| 멈춤 표시(interrupt) | 노드가 그 자리에서 그래프를 멈추고, 사람에게 보일 값을 남기는 일 | `interrupt(질문 값)` · 결과 키 `__interrupt__`의 `Interrupt` 항목 |
| 질문 값 | 멈춤 표시와 함께 사람에게 보일 값(payload 대신) | `{"order_key": …, "question": "결제할까요?"}` · `.value` |
| 사람의 답으로 이어 가기 | 멈춘 스레드에 사람의 답을 넘겨, 멈춘 노드부터 실행을 이어 가는 일 — Ch 23 03 「스레드 재개」·04·06 worker `resume` 단계와 다른 장면 | `invoke(Command(resume=답), config)` |
| (이어 씀) 승인 지점 | Ch 17 02 정의 그대로 | — |

## 10. 완료·대기 챕터 문장 대조

- **참**: Ch 23 07 b8 「Ch 24 01절에서는 되돌리기 어려운 일을 하기 전에, 사람이 확인하는 자리에서 그래프를 멈추는 방법을 다룹니다」 + 01 슬러그 링크(슬러그·장면 그대로) · Ch 23 03 「Ch 24에서 사람의 확인을 받아 멈춘 실행을 다시 움직이는 일과는 다른 장면」(01 3절이 그 장면) · Ch 17 02 승인 지점 정의(그대로 이어 씀) · Ch 17 03 「사람 확인 뒤 이어 가기 없음」(01 b3·b4 「비교와 경계」가 같은 사실) · Ch 19 06 사람 확인 값(b3 한 문장, 사실 그대로) · Ch 13 06 `Command`(갱신·다음 노드 — b3).
- **대기 챕터(고치지 않음)**: Ch 30 06 「Ch24의 중복 실행 방지 원칙」 → 01 b4·b6·6절로 참 · Ch 25 01~03 b3 「Ch24에서 interrupt와 재개 사건을 확인」 → `interrupt`와 이어 가기는 참, 「사건」(스트리밍 사건)은 Ch 25 몫 · Ch 27 08 「도구 실행 경계」 → 01은 쓰기 노드 하나의 승인 지점(도구 호출 승인 장면 없음 — 부분 참 그대로) · Ch 28 03 「사람이 승인해야 하는 작업 경계」 → 참.

## 11. 챕터 밖 수정

- `textbook/part6/ch23-persistence/qa/author_ch23_ch24.py`: 첫머리(`from __future__` 줄과 Ch 23 설명 주석 바로 뒤)에 설명 주석 셋 + `raise SystemExit("…")`(`44c9d593…` → `3fc72dedb865fd35424b182204228f9707a4b034f8c24e9a7a7758901b37adb2`). 실행하면 종료 코드 1로 바로 멈춤을 확인. **Ch 23 쪽 영향 없음** — 이 파일을 부르거나 가져오는 스크립트 0(`grep`, `before/` 사본 말고), Ch 23 개선본은 `qa/upgrade/author_NN.py`가 씀. 옮기기(`mv -n` → `ch23-persistence/qa/upgrade/before/generators/blocked/`)는 마감 몫.
- `textbook/part6/public-files.json`(§6, `collect_public_files.py`로 다시 모음).
- `textbook/_notebook/checks/notebook-contracts-part6-ch24-human-in-the-loop.json`(`verify.py`가 다시 씀).
- 챕터 안: `figures/_gen_figures.py` 맨 위 설명 주석 셋 + `raise SystemExit(...)`(`ced25fb2…` → `2a015c6a…`, 실행하면 종료 코드 1) — 옮기기는 마감 몫.
- 고치지 않음: `check_bundle_execution.py`·`bundle-execution.json`·zip 둘·`_build_index.py`·실습 폴더 README(「승인 결과는 실습 폴더의 로컬 파일에만 기록」 — **지금은 거짓**, 임시 폴더로 바뀜 → 마감 몫)·`pyproject.toml`·`uv.lock`·`chapter.json`·공용 도구.

## 12. 참고 자료 확인

- LangGraph Interrupts `https://docs.langchain.com/oss/python/langgraph/interrupts` — 2026-09-25 `WebFetch`: 「the runtime restarts the entire node from the beginning」 · 「side effects called before interrupt should (ideally) be idempotent」 · 「If you wrap the interrupt call in a try/except block, you will catch this exception and the interrupt will not be passed back to the graph」 · 「To use interrupt, you need: 1. A checkpointer … 2. A thread ID」 · 「only use values that can be reasonably serialized」 · 「The default graph.invoke(...) API still works and surfaces interrupts under result['__interrupt__']」 · 「The value passed to Command(resume=...) becomes the return value of the interrupt call」.
- 설치판 소스(`.cache/vm/venv-ch24-human-in-the-loop`, langgraph 1.2.11): `langgraph/types.py` 851~871행(858~860 처음 부르면 `GraphInterrupt`로 멈춤 — 마감에서 857 → 858로 바로잡음, 검토 A-2 · 864 「resumes from the start of the node, re-executing all logic」 · 870~871 체크포인터 필요) · `langgraph/errors.py` 50행 `class GraphBubbleUp(Exception)`·102행 `class GraphInterrupt(GraphBubbleUp)`.
- 노트북 밖 확인 `/tmp/ch24-01/probe/probe.py`(두 번 실행, 출력 같음): 네 장면 줄 수 2·0·1·1 · 체크포인트 2 → 3 · **`try`/`except Exception`으로 감싼 노드는 `받은 오류: GraphInterrupt`를 받고 칸 `answer`가 `caught`, 결과에 `__interrupt__` 없음, 다음 노드 `()`** — b7 문장의 근거(노트북에서는 실행하지 않았다고 적음).

## 13. 남은 것과 지우지 않은 것

- **마감 몫**: 공용 옛 생성기와 `figures/_gen_figures.py` `mv -n` · 옛 그림 `figures/0N-흐름.*` 삭제 승인·챕터 공개 목록 옛 SVG 줄 빼기 · zip 다시 만들기 → `check_bundle_execution.py`(01 새 `code_sha256` `7187f7a39f3f…`) → `bundle-execution.json` · 실습 폴더 README 다시 쓰기(파일은 임시 폴더, 도구 파일, 노트북 01은 키 없이) · `chapter.json` `objectives`(「승인 게이트를 구현」 → 승인 지점 말로)·`_build_index.py` 설명.
- **지워야 하지만 지우지 않은 것(삭제 승인 대상)**: `qa/upgrade/gates-wip-01-01.json`·`gates-wip-01.json` · `$ROOT/.cache/ch24-01-view/`(삽화 확인 사본 `illu-1-1100.png`) · 기기 `/tmp/ch24-01/`(probe·T·A·B·bundle(`.venv` symlink 판·`notebooks/__pycache__`)·illu·tools·reps·public-files 사본) · 기기 세션 임시 폴더 `$TMPDIR/ch24-01-*`(노트북 실행 넷·probe 둘이 만든 임시 폴더) · 실습 폴더 `.venv`(macOS 판, 준비 노트 목록 그대로) · `.cache/vm/venv-ch24-human-in-the-loop`(챕터 끝까지 씀).

## 마감 반영 (2026-09-25, 검토 1차)

노트북은 다시 실행하지 않았습니다(`code_sha256` `7187f7a39f3f…`·`outputs_sha256` `fbaaa8908bd1…`·`executed_at` 13:50:56Z 그대로 — 묶음 실행 검사 계약 유지). 고친 방법은 생성기 문자열(`author_01.py`) + 노트북 마크다운 같은 치환(`.cache/ch24-close/tools/gpatch.py`) → `author_01.py --src-only` → `run_section.sh … 01 --no-exec`, 대조는 `genmatch.py`(셀 62/62·`_src` 같음).

- **A-1 [중] 도미노 비유와 「처음부터 다시 실행」**: b4 비유 뒤에 「비유와 다른 점」 단락(이어 갈 때 멈춘 노드의 첫 줄부터 다시 실행 → 빈자리 앞의 컵은 한 번 더 쓰러짐, 노트북 4절 두 줄) · 용어 표 셋째 줄에 「다만 실제 그래프는 멈춘 줄이 아니라 노드의 첫 줄부터 다시 실행합니다」 · 노트북 3절 「사람의 답으로 이어 가기」 첫 자리(셀 22)에 같은 뜻 한 문장 · 삽화 그림 읽기를 「첫 실행이 멈추고 사람이 아직 답하지 않은 때의 모습」으로 한정. 삽화는 다시 만들지 않음.
- **A-2 [하]**: b4 「`types.py` 857~864행」 → 858~864행, 위 §12도 858~860.
- **A-3 [하]**: `figures/01-5-….prompt.md`의 설명 대상 문장·구성 요소 「조각」 → 「도미노」(지금 b4 비유 단락), 상태 끝에 마감 줄.
- **A-10 [중] 생성기**: `author_01.py`를 어떤 모드로 돌려도 도구 파일을 함수 셋 판으로 덮어쓰지 않게 — 파일이 없거나 01 판과 같을 때만 쓰고, 01 판으로 시작하는 더 긴 판(지금 `d562c9e6…`)이면 `skip`을 알림, 01 판으로 시작하지 않으면 `assert`로 멈춤. 사본 기기(`/tmp/ch24-close/sandbox`)에서 네 경우(함수 다섯 판·없음·01 판·다른 글)를 돌려 확인(도구 파일 해시 그대로, 없을 때만 `b40aab98…`을 씀).
- **준비물 「노트북 전체가 2초 안에」 뺌**(챕터 리드 결정 — 재지 않은 속도 숫자) → 「걸린 시간은 재지 않았습니다.」 생성기의 `RUNSEC`은 쓰지 않게 됨(변수는 남김).
- 게이트 G1~G7 0(검사 문장 383 → 388), 과정 금지어 새 걸림 0(`bandiff.sh` — 마감 전 사본과 견줌).
