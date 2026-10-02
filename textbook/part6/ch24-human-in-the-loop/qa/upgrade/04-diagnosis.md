# 04절 진단과 기록 — Human-in-the-Loop 실습 (챕터 끝 실습 절, 새로 만듦)

- 대상(새 파일): `_src/04-Human-in-the-Loop-실습.html` · `labs/part6/ch24-human-in-the-loop/notebooks/04-Human-in-the-Loop-실습.ipynb` · 그림 `figures/04-1`~`04-4` · 빌드 `04-Human-in-the-Loop-실습.html`.
- 생성기: `qa/upgrade/author_04.py`(노트북 + `_src`, **`20930d1a57b7abd7…`**) — `author_01`(`FOLDER`·`INSTALL`·`html_text`·`table_html`·`mermaid_block`)·`author_02`(`DEF_AFTER`·`ALLOWED`·`PATH_MAP`·`DEF_ONCE`)·`author_03`(`FOLDER`·`TOOLS`·`DEF_FIND`·`DEF_HISTORY`)를 가져와 `checks()`로 대조. 첫머리 `sys.dont_write_bytecode = True`(`qa/upgrade/__pycache__` 없음). `_src` `3cfa65d437e6…` · 빌드 HTML `31163ed0f2be…` · 노트북 파일 `089ed8d9e413…`. 그림 설계표 `qa/upgrade/04-figures.md`. 검토 묶음 `qa/upgrade/review-pack/04-Human-in-the-Loop-실습.md`.
- 작업일 2026-09-25(UTC 15:2x~15:4x). 슬러그 **`04-Human-in-the-Loop-실습`**(규격 §7-2 `{NN+1}-{챕터 이름}-실습`, 선례 `07-Persistence-실습`·`09-Middleware-실습`·`07-create-agent-실습` — 챕터 제목 앞말, 인계 후보 그대로). 제목 「Human-in-the-Loop 실습: 연장 일수를 고쳐 다시 묻고 승인일 때만 기록하기」, `format: experiment`, meta 「실습 30분 · 새 용어 0」, **`hours` 「총 8h · 강의 3h · 실습 5h」 그대로**(실습 절 30분은 챕터 시수에 더하지 않음 — 01~03 meta 합 강의 3·실습 5와 같음).
- **모델 요청 0번**(노트북·노트북 밖 모두, 챕터 리드 결정 1 — 잠금에 모델 패키지 없음). 키 셀 없음. 자식 프로세스 0. 도구 파일 그대로.

## 1. 게이트

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 | — (새 절) | | | | | | | | | |
| 첫 실행 전(`gates-wip-04-04.json`, `--label wip-04 --section 04`, 생성기만 돌린 판) | 28 | — | **0** | **0** | 0 | 0 | 0 | 0 | 14 | G7 14는 그림 전 |
| 후 (`gates-wip-04.json`, `run_section.sh … 04 --no-exec`) | **28** | **365** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 챕터 전체(`gates-wip-ch24-after04.json`): **01~04 네 절 모두 PASS**(G1~G7 0).
- AST 따로(`/tmp/ch24-04/tools/extra_check.py` — 03 판 그대로): 노트북 **금지 문법 0건**, 허용 표시 1건 = 마지막 셀 `sorted(os.listdir())`(키워드 없음 — 01~03과 같은 모양). 클래스는 칸만 적은 `ExtendState(TypedDict)` 하나, 함수 힌트·반환 힌트·데코레이터·f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`.get`·`+=`·기본값·튜플 풀기·별표 풀기·`while`·`try`·`set`·`key=`·`reverse=`·세미콜론 0. 호출 깊이 최대 **2**(`/tmp/ch24-04/tools/depth.py` — 세 겹 0, 03과 같음).
- **01~03에서 쓰지 않은 이름 대조**(`/tmp/ch24-04/tools/names_check.py` — Ch 23 07 판을 Ch 24로): 내장 이름 **0** · 속성 **0** · 키워드 인자 **0** · import 하나(`approval_tools:find_before` — 03 노트북 4절이 셀에 적은 함수를 §2-7대로 도구 파일에서 가져오는 줄, 이름은 03 것). 새 문법·새 API·새 말 **0**. 생성기 `checks()`가 `stream`·`interrupt_before`/`after`·`as_node`·`HumanInTheLoop`·`while`·`try:`·`append_key_once`·`unlink`·`Path(`가 코드 셀에 없음을 확인.
- 셀 모양(`/tmp/ch24-04/tools/shape.py`): 코드 셀 **28**(준비 셋: 설치·가져오기·임시 폴더 — 01~03과 같은 수, 실습 선례 19~25보다 많음 — §2 끝), 준비 셀이 아닌 셀 주석 뺀 코드 최대 **9줄**, 함수 본문 최대 **8줄**(`ask_extension`), 셀당 정의 하나(노드 셋 + 조건 함수 하나 + 상태 형식 하나), 첫 줄 주석 100%. 코드 줄(`count_code.py`) **153**(01 158 · 02 146 · 03 137 → 챕터 합 594), 도구 파일 30줄 그대로.
- 금지어(`/tmp/ch24-04/tools/ban24.py` — 03 판 그대로, 노트북 설명·주석·`_src`·캡션 셋·`.mmd` 셋): 걸린 12건은 모두 「체크포인터」 안 「포인터」. 「분기」 2건은 03 슬러그 링크(`href`) 둘. 「조각」·「지연」·「추정」·「반환」·「강사 시연」·「결정적」·「재개」·「재실행」·「갈래」·「게이트」 0, 「한 겹 더」 0. `.prompt.md`의 금지어 언급도 말을 바꿔 0. 빌드 HTML `{{`·`[[` 0건.

## 2. 설계 — 붙인 기능과 뺀 것 (규격 §7-2 1번, 인계 「§03 → 실습(04)」 6항)

| 절 | 붙인 기능 | 흐름 안에서 쓰였는가(코드로 센 값 — 두 실행 모두) |
|---|---|---|
| 01 | 승인 지점 — 확인 노드 `ask_extension`에서 멈춤 표시로 먼저 묻고, 답이 `approve`일 때만 `append_key`(01 `ask_then_charge` 모양, 도구 파일 함수) · 노드는 이어 갈 때 첫 줄부터 다시 실행 | **쓰임** — 확인 노드 다섯 번 실행(`실행 횟수 … : 1 2 5`)에도 실행 1 기록 `['loan-2307']` 한 줄, 실행 2(`reject`) 기록 파일 없음. 원래 가지(연장 일수 14)는 승인 전에 멈춘 채라 기록 0 |
| 02 | 허용 답 목록 `["approve", "reject"]`(02와 같은 줄) · `interrupt` 한 번 + 오류 칸 · 조건 함수 `after_answer`(02 셀과 **같은 문자열** — `checks()`) · 이름표 표로 같은 노드에 되돌아감 | **쓰임** — 첫 답 `change`에 `이 셀에서 실행된 노드: ['ask_extension', 'ask_extension']`·`'error': '허용하지 않는 값: change'`(두 실행 같음) |
| 03 | `print_history`·`find_before`(도구 파일) · `update_state`로 값 고쳐 넣기 · `invoke(None, 새 설정)`으로 새 가지 · 스레드 설정은 가장 최근 체크포인트 | **쓰임** — `1 \| loop \| ('plan_extension',)` 고름 → `2 \| update \| ('plan_extension',)`(`'days': 7`) → `['plan_extension', 'ask_extension']`(대출 조회 다시 실행 0) → `새 가지의 질문 값: {'days': 7, 'due_days': 10, 'error': ''}` → 스레드 설정으로 마지막 답이 새 가지에 닿음 |
| Ch 23 07(소재) | 이용자 번호 `M-0317`·대출 키 `loan-2307`, 스레드 이름 = 이용자 번호 | 과제 값·두 실행의 스레드 이름(체크포인터는 실행마다 새로 붙여 섞이지 않음) |

- **세 기능이 모두 일하게 한 흐름**(Ch 20 05 검토 B-8 — 붙이기만 한 부품 없음): 신청서의 연장 일수를 잘못 적힌 값(14)으로 두고, 직원의 첫 답을 목록 밖의 `change`(연장 일수를 바꿔 달라는 뜻)로 정했다. 그래프는 목록에 없는 답이라 다시 묻고(02), 답으로는 칸 값을 바꿀 수 없으므로 직원은 다음 노드가 `plan_extension`인 지난 체크포인트에 7을 고쳐 넣어 새 가지에서 다시 묻는다(03). 기록은 마지막 답이 `approve`일 때만(01). 01의 쓰기를 확인 노드 **안**, 멈춤 표시 **뒤**에 두어(01 After 모양) 「노드가 다시 시작해도 한 번만 적음」이 실제로 일하게 했다(따로 기록 노드를 두면 이 성질이 구조로만 보장되어 01 교훈이 흐름에 드러나지 않음).
- **값 하나만 바꿈**: 사람의 답 차례 `["change", "approve"]` → 마지막 답 하나만 `"reject"`(`answer_turns[1] = "reject"`). **01 값 바꿔 보기와 같은 값(거절 ↔ 승인)** — 그래서 b2·노트북 7절 앞에 「새로 볼 것은 다시 묻기와 새 가지를 거친 뒤에도, 기록이 가장 최근 가지의 마지막 답으로만 갈리는지」 한 문장. 다른 후보를 고르지 않은 까닭: 첫 답을 `reject`로 바꾸면 실행 2에서 다시 묻기(02)가 쓰이지 않음 · 첫 답을 `approve`로 바꾸면 원래 가지가 먼저 기록한 뒤 돌아가는 장면(03 b7 「실행하지 않음」, 인계 권고 「다루지 않는 쪽」)이 됨 · 고쳐 넣는 연장 일수만 바꾸면 질문 값 숫자만 달라짐(03 값 바꿔 보기 되풀이).
- **손으로 정한 새 값**(규격 §7-2 7번 — 실행 전에 정함, 출력 줄 「출처」와 b7): 연장 일수 `14`·`7`과 자료실 규칙 「한 번에 7일까지」(이 절에서 정함) · 사람의 답 차례 `change`·`approve`(실행 2 `reject`) · 남은 날 `3`(노드 안 상수, 대출 기록을 읽지 않음) · 기록 파일 이름 `extend-1.record`·`extend-2.record`. 이용자 번호·대출 키는 Ch 23 07 값 그대로. 탐색 실행으로 고른 값 아님(설계 뒤 노트북 밖 준비 확인만 — §3).
- **뺀 것**(b3 둘째 단락): 01 Before `charge_then_ask`·멱등 앞쓰기 `receive_then_ask`(`append_key_once` — 이번 흐름에 묻기 전 쓰기가 없음) · 02 `while True` 모양·실패 장면 둘(체크포인터 없이·다른 스레드 — 02에서 견줌, 노트북 `try` 0) · 03 값을 바꾸지 않은 다시 실행(`fork`)·소수 할인율 계산(값을 고쳐야 하는 흐름에 나오지 않음). 03 b7이 「실행하지 않음」으로 남긴 멈춘 채 둔 가지에 답 넘기기·원래 가지에서 이미 적은 뒤 돌아가기는 인계 권고대로 **다루지 않음**(b7에 한 줄씩).
- **모델 요청 0번의 처리**: 규격 §7-2 실습 절 「모델 호출 3~5번」과 다름 → b3 한 단락(「다른 챕터의 실습은 모델을 몇 번 부르지만, 이 챕터의 실습은 모델을 부르지 않습니다. 01절처럼 매번 같은 값을 내는 우리 노드여야, 기록 파일의 줄 수와 체크포인트 수를 출력으로 가를 수 있기 때문입니다. 사람의 답도 셀에 적은 값입니다.」)·준비물·이 진단·강사 확인(§12). 선례 Ch 23 07(요청 0, 검토자 「정당」). 모델을 넣으려면 잠금을 바꿔야 함(`uv lock`, 보호 파일 — 챕터 리드 결정 없이 하지 않음).
- 파일 쓰기는 임시 폴더에만(챕터 결정 2, 앞머리 `ch24-04-` — `checks()`), 지우는 줄 0. 셀 하나를 다시 실행하면 같은 스레드에 체크포인트가 더해지고 기록 줄이 늘 수 있어, 준비물·b7에 「1절 임시 폴더 셀부터 차례로 다시 실행」(03 선례, Ch 23 검토 B-2와 같은 위험 — 이 절은 실행 1 기록 파일 이름이 고정이라 실행 1 셀만 다시 누르면 줄이 늘 수 있음, 실행하지 않음).

## 3. 결정성 확인 (규격 §7-2 6번 — 모델이 없으니 두 번 같아야 함)

- 노트북 밖 준비 확인(`/tmp/ch24-04/probe/probe.py` — 노트북 설계와 같은 그래프·같은 차례, 실행 1·2 두 장면): 새 Python 프로세스로 **다섯 번**(15:2x~15:28:16Z) — 출력 전체 해시 **5/5 같음**(`39e725f04ff2…`). 값: 첫 질문 `{'days': 14, 'due_days': 17, 'error': ''}` → `change` 뒤 노드 `['ask_extension', 'ask_extension']`·오류 글 · 목록 다섯 · 단계 1 고름 · `2 | update` · 새 가지 `['plan_extension', 'ask_extension']`·`10` · 체크포인트 8 · 기록 `['loan-2307']`/없음 · 원래 가지 `('ask_extension',)`·14 · 실행 횟수 1·2·5.
- 결론·그림·정리·복습의 값은 모두 이 확인과 새 커널 세 번(T·A·B)에서 같았던 값. 흔들린 값 없음 → 결과 읽기 둘째 단락에 「이번 실행에서는」 값을 둔 곳 없음. 달라지는 것은 체크포인트 아이디·시각·임시 폴더 위치뿐(출력하지 않음).

## 4. 새 커널 (규격 §2-7 9번 끝 — 그림 그리기 전)

- **T**(실습 폴더 밖 사본 `/tmp/ch24-04/T/T.ipynb` + 도구 파일 사본, `execute.py`, 15:27:12Z) — `PASS T.ipynb: 28 cells`. 실습 폴더에 `.failure.json`이 남지 않게 먼저.
- **A** `PYTHONDONTWRITEBYTECODE=1 env -u OPENAI_API_KEY bash run_section.sh … 04`(셀 실행 기록 **15:27:35.00~35.99Z**, 약 1초 → 준비물 「2초 안에」) — **`PASS 04-Human-in-the-Loop-실습.ipynb: 28 cells`**. 그림 PNG가 아직 없어 `attach_figures.py`에서 멈춤(실행·저장은 끝난 뒤 — 예정대로).
- **B**(A에서 출력만 지운 사본 `/tmp/ch24-04/B/B.ipynb` + 도구 파일 사본, `execute.py`, 같은 환경 변수, 15:27:55Z) — `PASS`. 셀별 출력 글자 대조(`cmpout.py`) **A↔B 28/28 같음**, **A↔T 28/28 같음**. `code_sha256` **`c4722b0d084f12987ac29f96abb6da6e4dbbeb7550fc9d8e5ff57897919a02e6`**(셋 같음), `outputs_sha256` A **`2aeaebb251740d00…`** ↔ B·T `afed104f1fe195a6…` — 설치 셀 출력이 B·T에서 스트림 둘로 나뉜 차이뿐(글은 같음, 01~03과 같은 현상 — 셀별로 확인). 교재 노트북은 A.
- 그 뒤 코드·출력은 고치지 않음: `mdpatch.py`(`/tmp/ch24-04/reps-fig1.json` — 「오늘 볼 그림」 alt 한 문장, 04-1 첫 렌더 뒤 라벨을 고쳐서) · `author_04.py --src-only`(삽화 alt·그림 읽기·b7 한 줄) · `--no-exec`의 첨부는 노트북 마크다운·`_src`만 바꿈 — `code_sha256`·`outputs_sha256`·`executed_at`(15:27:36Z) 그대로, 생성기 `cells()`와 노트북 셀 글 **59셀 모두 같음**(대조 스크립트).
- `verify.py --chapter`(`run_section.sh` 안): **`PASS 4 sections / 112 code cells (max 12 lines)`**. 실습 폴더 `notebooks/__pycache__`·`qa/upgrade/__pycache__` 만들지 않음. `uv run --project labs/…`는 늘 환경 변수 셋과 함께.

## 5. 결정적 값의 자리

| 값 | 성격 | 둔 자리 |
|---|---|---|
| 질문 값 `{'days': 14, 'due_days': 17, 'error': ''}` · 다시 물은 질문 값(오류 글 `허용하지 않는 값: change`) · 실행된 노드 목록 넷 · `체크포인트 수: 5` · 체크포인트 줄 `1 \| loop \| ('plan_extension',)`·`2 \| update \| ('plan_extension',)` · 새 가지 질문 값(`7`·`10`) · 기록 `['loan-2307']`·줄 수 1 / 파일 없음 · 실행 횟수 `1 2 5` · 원래 가지 `('ask_extension',)`·14 · 견주기 두 줄(`8` 체크포인트) · 파일 `['extend-1.record']` | 우리 코드·라이브러리 규칙(밖 5/5·T·A·B 같음) | 결과 읽기 첫 단락·b6 표·그림·정리·복습 |
| 목록 전체의 칸 값(일곱 칸 딕셔너리) | 같음 | 결과 읽기는 칸 하나씩만 인용 |

## 6. 그림

- Mermaid **3장**(규격 §7-2 그림 = 조립도 · 실행 1 실제 순서 · 실행 1·2 비교): `04-1` flowchart TB 상자 일곱(노드 셋 파랑 · 고쳐 넣기·사람의 답 초록 · 조건 함수 회색 마름모 · 가상 끝점, 조건부 엣지 둘 점선) **609** · `04-2` flowchart TB 한 줄 상자 일곱 **269**(세로 858) · `04-3` flowchart TB 초록 → subgraph 둘 + 공통 회색 `~~~` **539**. **모두 868 이하, 빨강 0, 보라 0**(experiment·모델 없음 — 목록 밖 답도 코드가 받아 오류 칸에 적은 값이라 노란 상자 안의 글). PNG를 매번 직접 열어 봄(`.cache/ch24-04-view/m1-v1`~`m3-v2`·`m2-v3`, 같은 이름 사본은 옛 그림이 보일 수 있어 새 이름). 첫 렌더에서 저절로 꺾인 라벨(04-2 맨 아래 상자, 04-3 초록 상자·회색 상자)을 `<br>`로 미리 나누고, 줄 끝 가운뎃점 둘(04-1 확인 노드, 04-2 다섯째 상자)을 빼 다시 렌더(04-1 alt 한 문장도 고침). 설계표는 그림 차례·라벨을 생성기 `FIG*_MMD`에 먼저 적은 뒤, 첫 렌더를 보고 `04-figures.md`에 옮겨 적음(규격 §5-2 「설계표 먼저」와 차례가 조금 다름 — 기록).
- 삽화 **1장** `04-4-따로-세운-세-줄을-이은-긴-줄`(비유 계열 「도미노 줄과 비워 둔 자리」 04 — 01 컵·02 파란 구슬과 연두색 도미노·03 넘어진 나무 줄과 주황 줄을 되풀이하지 않고 「조립」: 따로 선 짧은 세 줄 ↔ 같은 세 색을 이어 붙인 긴 줄 하나 + 빈자리 하나) — **1차 job `8434076e-428a-4312-8a2b-0716be792e1a` 채택**, 재생성 0, **2크레딧**(거래 **2026-09-25T15:29:48Z 「Nano Banana Pro −2」**, 생성 전 잔액 2425.75, 바로 앞 거래 14:53:44Z는 03절 몫). 응답 모델 표시 `nano_banana_2`(01~03과 같음). 원본 `646a24164ac6…`(2752 × 1536) → 저장 `f9f4b5527a16…`(1100 × 614), 결과 URL을 한 번 더 받아 줄인 그림과 픽셀 대조 bbox `None`·최대 차이 0. 저장 PNG와 해시가 같은 사본을 직접 보고 셈: 흰 탁자 하나 · 왼쪽 짧은 줄 셋(연한 파랑 셋 · 초록 셋 · 노랑 셋, 모두 서 있음) · 오른쪽 긴 줄 하나(파랑 넷 → 초록 넷 → 노랑 셋 → **빈자리 하나** → 노랑 셋, 모두 서 있음) · 넘어진 도미노·글자·숫자·사람·손·컵·구슬 없음. 짧은 줄과 긴 줄의 개수가 달라 그림 읽기에 「도미노 개수는 무엇과도 짝짓지 않습니다」. 세부 `figures/04-4-….prompt.md`.

## 7. 서비스 요청과 비용

- 모델·임베딩 요청 **0번**(노트북 T·A·B, 노트북 밖 확인 모두). 키는 읽지 않음(`env -u OPENAI_API_KEY`).
- Higgsfield 1회 생성, 2크레딧(§6). WebFetch 0(참고 자료는 01~03절·Ch 23 01·07절 — 새 설치판 소스 인용 없음).

## 8. 도구 파일 `notebooks/approval_tools.py`

- **바꾸지 않음**(`d562c9e67c56cab1a6e8435e7f926a7c1858a621faf5f3a9fdaa51a632f1b31f` 그대로 — 생성기가 해시와 `author_03.TOOLS` 같음을 `assert`). 이 절이 쓰는 앞 절 평범한 함수 넷(`append_key`·`read_record` — Ch 23 06·04, 01이 옮김 · `print_history` — Ch 23 01, 03이 옮김 · `find_before` — Ch 24 03, 03이 옮김)이 모두 이미 있음 — 가져오기는 알파벳 순 한 줄(임시 폴더로 옮기기 전 준비 셀) + 고정 세 문장 + 커널 폴더 한 문장 + 실행 도구 한 문장. `find_before`는 03 노트북 셀 글(`author_03.DEF_FIND`)과 도구 파일 글이 같음(`checks()`).
- 노트북 전역 이름(`extend_calls`·`allowed_answers`·`END`)에 기대는 노드 셋과 조건 함수는 노트북에 적음 — 조건 함수는 02 셀과 **같은 문자열**, 확인 노드는 01 `ask_then_charge`·02 `ask_once`의 줄(`if answer == "approve":`·`if answer in allowed_answers:`·`"허용하지 않는 값: " + answer`)을 담음(`checks()` — 「글자까지 같음」은 조건 함수에만 씀). 노트북에만 있는 앞 절 평범한 함수(02 `make_question`·`record_counts`)는 쓰지 않아 옮긴 것 0. 01 노트북이 가져오는 이름·01 묶음 실행 검사 계약에 영향 0.

## 9. 03절 이음새 (03 노트북은 다시 실행하지 않음)

- 03 b8·노트북 정리 끝 「04절 실습에서는 이 챕터에서 배운 것을 작은 흐름 하나에 모아 실행합니다」 → **04 내용과 맞음**(01~03 기능을 연장 신청 한 흐름에). 01·02 b8처럼 **`_src` b8에 04 링크만** 더함: `author_03.py`(`6ec79811…` → **`d2c014669b12…`**, `_src` 문장 한 곳 — 고치기 전 생성기 `src_html()`이 그때 `_src`와 같음을 먼저 확인) → `author_03.py --src-only`(`_src/03` `a6eabd0d…` → **`aa00400d83e3…`**) → `run_section.sh … 03 --no-exec`(03 게이트 0 — `gates-wip-03.json`을 다시 씀). 노트북 정리 끝은 링크 없는 선례(01~03 모두 글자만)라 `mdpatch.py`를 쓰지 않음.
- **03 노트북 그대로**: 파일 `e7649d5a0cbd…`(전후 같음, `--no-exec`의 첨부 단계도 바이트를 바꾸지 않음) · `code_sha256` **`12b29f1517d5…`** · `outputs_sha256` **`aab2462d34f9…`** · `executed_at` 14:52:29Z 그대로.
- 03 빌드 HTML `d1d9e365…` → `e3141468…`(04 빌드 때 다음 절 이동 줄) → **`421d2df7e1f0…`**(b8 링크). 01·02 빌드 HTML은 바이트 같음(`09f46b30…`·`8f502dfb…`), 챕터 `index.html` `d0dc258b…` → **`bd3554a12c2f…`**(04 줄).

## 10. 챕터 밖 수정 · 보호 파일

| 파일 | 무엇을 |
|---|---|
| `textbook/part6/public-files.json` | `python3 textbook/part6/qa/collect_public_files.py`로 다시 모음 — **04 노트북 한 줄만** 늘어남(`a77415947a7e…` → **`7c9cb35e3374…`**, 보호 파일, 82줄). `prerequisite-files.json` 바이트 같음(`4c7f5a4b…`) |
| `textbook/part6/index.html` | `python3 textbook/part6/_build_index.py`가 다시 씀 — Ch 24 「4절」·04 링크(`cfd0cd817524…` → **`afe83bc7dede…`**, 보호 파일). 22행 설명·시수(3·5)는 그대로 |
| `textbook/downloads/part6-practice.zip` | 같은 스크립트가 다시 만듦(`aa82b386b154…` → **`61119a820068…`**, 보호 파일) — **Ch 24 항목 8개가 모두 디스크와 같아짐**(01~04 노트북·도구 파일 `d562c9e6…`·README 04 단락 판·잠금 둘), `__pycache__` 0 |
| `textbook/part6/qa/integration-results.json` | 같은 스크립트가 다시 씀(`624a596eb10d…` → **`fa46898a97f4…`**, 보호 파일 — `sections: 51`·`bundle_files: 98`) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch24-human-in-the-loop.json` | `verify.py --chapter`가 다시 씀(`cfbce0b9e1b3…` → **`1a241f44e4a4…`**, 보호 파일·기록 파일) |

- 챕터 안(실습 폴더 포함): `chapter.json`(04절 추가, `64fad507e973…` → **`1ee64948471d…`**, 보호 파일, `hours`·`objectives` 그대로) · 실습 폴더 `README.md`(맨 아래 04 한 단락, `525aa21ac755…` → **`7c557ad26f23…`**, 보호 파일) · 챕터 `qa/public-files.json`(04 HTML·노트북 두 줄 — 03 줄 다음, `c629078f134d…` → **`c72eba46684…`**, 보호 파일) · `qa/verification.md` 04 행(**`d4cefae849a1…`**) · `집필점검표.md` 04 행(**`a0b1c726e78f…`**) · 03 `author_03.py`·`_src/03`·빌드 HTML(§9) · 새 파일(노트북 04·`_src/04`·빌드 04·`figures/04-*` — `.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md` 셋 + 삽화 `.png`·`.prompt.md`·`.caption.md` · `qa/upgrade/author_04.py`·`04-figures.md`·`04-diagnosis.md`·`gates-wip-04-04.json`·`gates-wip-04.json`·`gates-wip-ch24-after04.json`·`review-pack/04-…md`) · `handoff.md` 「실습 → 챕터 검토」·`manifest-changes.md` 「04절 뒤」.
- **보호 파일 131개**: **109개 같음 · 22개 바뀜 · 없어진 파일 0** = 03절 끝까지 바뀐 16개(이 절이 값을 다시 바꾼 것 일곱: 묶음 목록 둘·`verification.md`·`집필점검표.md`·notebook-contracts·03 `_src`·03 HTML) + **이 절이 지시대로 새로 바꾼 여섯**(`chapter.json`·실습 폴더 `README.md`·챕터 `index.html`·`part6/index.html`·`part6-practice.zip`·`integration-results.json`). `textbook/index.html`·`llm-practice.zip`·`part7-practice.zip`·`bundle-execution.json`·`delivery-results.json`·`_build_index.py`·잠금 둘·공용 도구 그대로.
- **고치지 않은 것**: 01·02 파일(노트북·`_src`·생성기) · 03 노트북 · 도구 파일 · 실습 폴더 `pyproject.toml`·`uv.lock` · 공용 옛 생성기 `textbook/part6/ch23-persistence/qa/author_ch23_ch24.py`·`figures/_gen_figures.py` · 옛 그림 · Ch 23·25~31 파일 · 공용 도구·게이트·`verify.py`·`build_index.py`·`_build_index.py`·`check_*.py` · 규격·과정 요약. **파일 삭제 0건**.

## 11. 검사 결과 (Part 6)

- `run_section.sh … 04 --no-exec`: 게이트 **0**, `verify.py --chapter` **`PASS 4 sections / 112 code cells (max 12 lines)`**, 빌드 HTML 04 `{{`·`[[` 0건, SVG 셋·삽화 JPEG 하나 인라인. 챕터 전체 4/4 PASS.
- `python3 textbook/part6/_build_index.py` → **`Part 6: 51 verified sections; 98 bundled files`**(Ch 24 「강의 3시간 · 실습 5시간 · 4절」, 22행 설명 문장은 그대로 — 마감 몫).
- `check_delivery.py` → **117행 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`에서 멈춤**(`llm-practice.zip` — 알려진 일, 전체 마감 몫, Ch 23 07과 같은 자리). 그 앞(절 검사·페이지 비밀값·개인 경로·`part6-practice.zip` 매니페스트 신선도)은 지나감. `delivery-results.json`은 쓰기 전에 멈춰 **안 바뀜**(`3cc2d143…`).
- 묶음 실행 검사(`check_bundle_execution.py` — Ch 24 01)·`visual.cjs`·`check_scope.py`·옛 검사 넷은 **돌리지 않음**(마감 몫). 지금 zip 안 01은 새 판(`code_sha256` `7187f7a39f3f…`)이고 `bundle-execution.json`은 옛 값(`718171990c5d…`)이라, 마감이 검사를 다시 돌려야 기록이 맞음.

## 12. 강사 확인 대상

1. **모델 요청 0번**(규격 §7-2 실습 절 3~5번과 다름) — 챕터 리드 결정(모델 없는 챕터, 잠금에 모델 패키지 없음)을 따름. Ch 23 07 선례.
2. **실행 2가 01 값 바꿔 보기와 같은 값(거절 ↔ 승인)을 바꿈** — 「새로 볼 것」을 다시 묻기와 새 가지를 거친 뒤로 둠(§2 — 다른 후보는 기능이 빠지거나 03 b7 장면이 됨).
3. **직원의 첫 답 `change`(목록 밖 답)로 「답으로는 값을 바꿀 수 없어 지난 체크포인트로 돌아감」을 보인 소재** — 실제 화면이라면 「고치기」 단추를 두는 설계도 있음(이번에 다루지 않음).
4. **코드 셀 28개**(실습 선례 19~25보다 많음) — 실행 1을 셀 하나씩 보이고 원래 가지 읽기 셀을 둔 까닭. (마감 B-12: 처음 판의 「규격 범위 20~32 안」은 규격·PLAYBOOK·AGENTS·CLAUDE 어디에도 없는 수라 뺐습니다. 다음 재실행이 있으면 8절 두 셀(`runs` 모으기 · 견줌 출력)을 한 셀로 합치고 5절 글을 4절 끝으로 옮기는 쪽을 권합니다.)
5. **새 값**: 연장 일수 14·7·규칙 「7일까지」·남은 날 3·사람의 답 차례 — 흐름을 보여 주려고 정한 예(출력 줄 「출처」·b7).

## 13. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: `handoff.md` 「실습 → 챕터 검토」 5번.
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 **`/tmp/ch24-04/`**(`T/`·`A/`·`B/`(노트북 사본·도구 파일 사본)·`probe/`(`probe.py`·`run-1`~`run-5.txt`)·`illu/`(`illu-1-orig.png` 3.1MB·`illu-1-again.png`·`resize.py`·`pixcmp.py`)·`tools/`(03 판 복사 + `names_check.py`·`depth.py`·`showout.py`)·`hashes-before04.txt`·`manifest-now.txt`·`before-build-index.txt`·`after-build-index.txt`·`reps-fig1.json`·`chapter.before.json`·`author_03.before.py`·`README.before.md`·`집필점검표.before.md`·`verification.before.md`·`ch-public-files.before.json`·`part6-public-files.before.json`·`part6-prereq.before.json`·`handoff.before.md`·`manifest-changes.before.md`) · 기기 세션 임시 폴더 **`$TMPDIR/ch24-04-*`**(노트북 T·A·B가 만든 폴더 셋, 각 `extend-1.record` 하나) · **`$TMPDIR/ch24-04-probe-*` 다섯**(준비 확인, 각 파일 하나 — 연결 폴더 밖) · `$ROOT/.cache/ch24-04-view/`(PNG 여덟 — 그림 확인 사본) · `qa/upgrade/gates-wip-04-04.json`·`gates-wip-04.json`·`gates-wip-ch24-after04.json` · `.cache/vm/venv-ch24-human-in-the-loop`(마감까지 씀).

## 마감 반영 (2026-09-25, 검토 1차)

노트북은 다시 실행하지 않았습니다(`code_sha256` `c4722b0d084f…`·`outputs_sha256` `2aeaebb25174…`·`executed_at` 15:27:36Z 그대로 — 모델 요청 0 · 코드 셀 28 · 실행 2 설계 그대로). 고친 방법은 01과 같고, `author_04.py --figures`로 04-2·04-3 `.mmd`가 바뀜 → **04-2·04-3을 `--force`로 다시 렌더**(노트북 첨부는 04-1뿐이라 첨부 그대로, 04-1 라벨 「남은 날 3」은 `left_days` 뜻 그대로라 두었음).

- **B-7 [중] 「남은 날」 두 뜻**: 04-2 첫·다섯째 상자와 04-3 회색 상자의 17·10 앞말을 **「연장 뒤 남은 날」**(`due_days`)로, 폭이 늘지 않게 `<br>`로 나눔. alt도 같게. 「남은 날」은 `left_days`(3)만 가리킴. 폭 04-2 269 · 04-3 539(그대로 868 이하). PNG를 직접 열어 확인.
- **B-8 [중] 「새로 볼 것」**: b2·노트북 7절을 「다시 묻기와 새 가지를 거친 흐름에서도, 기록이 마지막 답 하나로 갈리는지」로 좁힘, 노트북 7절에 「원래 가지에 답을 넘기는 장면은 이 실습에서 실행하지 않습니다」. 설계는 그대로(검토 (가)안, 강사 확인 대상).
- **B-9 [하]**: b4 함수 표 「도구 파일(Ch 23 01절·이 챕터 03절)」 · 노트북 셀 4 「이 절에서 새로 배우는 이름은 없습니다」 · 셀 6 결과 읽기 「함수 `find_before`는 이 챕터 03절 노트북 4절에서 …」·「가져오기 줄 주석의 「03절」도 Ch 23이 아니라 이 챕터 03절입니다」(코드 주석을 결과 읽기에서 바로잡음 — 규격 §3 마지막 항목). 셀 5 주석 자체는 코드 셀이라 **다음 재실행 때** 「… 이 챕터 03절에서」로(체크리스트 Ch 24 몫).
- **B-10 [하] 04-2 도식 읽기**: 넷째 파란 상자는 셀 둘(셀 35 `find_before` · 셀 37 `update_state`·`invoke(None, …)`)에서 부른 줄을 묶은 것이고 그 안의 연장 일수 7은 04-1에서 초록으로 그린 고쳐 넣은 값이라는 문장 · 「노란 상자는 노트북 6절 출력이고, 일곱째 상자의 체크포인트 여덟만 8절 출력」. 상자를 나누면 상자가 여덟이 되어(규격 §5-3 일곱 이하) 글로 풀었습니다.
- **B-11 [하]**: b3 「Ch 23 07절 실습처럼, 이 챕터의 실습도 모델을 부르지 않습니다. 이 챕터 실습 폴더에는 모델 패키지가 없고, 01~03절도 매번 같은 값을 내는 우리 노드로 결과를 갈랐습니다.」(Ch 23 07 링크).
- **B-12 [하]**: 위 §12 4번의 「규격 범위 20~32」를 뺌(근거 없는 수). 셀 합치기는 다음 재실행 몫·강사 확인.
- **B-13 [하]**: 04-4 그림 읽기 끝 「색과 절, 도미노 개수는 서로 짝짓지 않습니다」.
- **B-14 [하]**: 설계표를 첫 렌더 뒤에 적은 절차는 챕터 요약 절차 메모에 한 줄(결과물 영향 없음).
- 준비물 「걸린 시간은 재지 않습니다. / 교재 출력을 만든 실행에서는 노트북 전체가 2초 안에 끝났습니다.」 → 「걸린 시간은 재지 않았습니다.」 한 줄.
- 게이트 G1~G7 0(검사 문장 365 → 367), 과정 금지어 새 걸림 0.
