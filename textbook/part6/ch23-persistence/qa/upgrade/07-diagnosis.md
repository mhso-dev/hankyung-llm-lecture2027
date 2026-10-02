# 07절 진단과 기록 — Persistence 실습 (챕터 끝 실습 절, 새로 만듦)

- 대상(새 파일): `_src/07-Persistence-실습.html` · `labs/part6/ch23-persistence/notebooks/07-Persistence-실습.ipynb` · 그림 `figures/07-1`~`07-4` · 빌드 `07-Persistence-실습.html`.
- 생성기: `qa/upgrade/author_07.py`(노트북 + `_src`, `21e1e5e9533ab690c9fb71d56d26265808f64252d5adf18bf1b6dd1a1a08726d`) — 01 생성기에서 `FOLDER`·`html_text`·`table_html`, 03·04·05·06 생성기 상수로 `check_same_as_before()`(도구 파일 해시·함수 넷 AST·상태 형식·설계 객체·실패 흉내 글·임시 폴더 셀 대조). `_src` `d0c586bd8191…` · 빌드 HTML `164f1f6ad01c…` · 노트북 파일 `0fe06118afcf…`. 그림 설계표 `qa/upgrade/07-figures.md`. 검토 묶음 `qa/upgrade/review-pack/07-Persistence-실습.md`.
- 작업일 2026-09-25(UTC 11:1x~11:4x). 슬러그 **`07-Persistence-실습`**(규격 §7-2 `{NN+1}-{챕터 이름}-실습`, 선례 `09-Middleware-실습`·`07-create-agent-실습`·`05-ToolNode-실습` — 챕터 제목 앞말, 인계 후보 그대로). 제목 「Persistence 실습: 멈춘 대출 처리를 이어 가고 기록은 한 번만 남기기」, `format: experiment`, meta 「실습 30분 | … | 새 용어 0」, **`hours` 「총 16h · 강의 6h · 실습 10h」 그대로**(실습 절 30분은 챕터 시수에 더하지 않음 — 챕터 요약에 적을 것).
- **모델 요청 0번**(노트북·노트북 밖 모두, 챕터 리드 결정 1 — 잠금에 모델 패키지 없음). 키 셀 없음. 자식 프로세스 0.

## 1. 게이트

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 | — (새 절) | | | | | | | | | |
| 첫 실행 전(`--label wip-07 --section 07`, 생성기만 돌린 판) | 22 | 323 | **0** | **0** | 0 | 0 | 0 | 1 | 14 | — |
| 후 (`gates-wip-07.json`·`gates-wip-07-07.json`) | **22** | **333** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G1·G2 **0**. G6 1 = 「되돌립니다」(게이트 금지어 「돌립니다」) → 「처음 값으로 다시 맞춥니다」로 실행 전에 고침(`_src`·주석의 「되돌린」·「되돌렸습니다」도 함께). G7 14 = 그림·설계표가 없던 때. `gates-wip-07-07.json`은 마지막 확인에서 다시 써 지금은 0.
- 챕터 전체(`gates-wip-ch23-after07.json`): **01~07 일곱 절 모두 PASS**(G1~G7 0).
- AST 따로(`/tmp/ch23-07/extra_check.py` — 06 판 그대로): 노트북 **금지 문법 0건**, 허용 표시 1건 = 마지막 셀 `sorted(os.listdir())`(키워드 없음 — 03~06 판과 같은 모양). 클래스는 칸만 적은 `LoanState(TypedDict)` 하나, 함수 힌트·반환 힌트·데코레이터·f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`.get`·`+=`·기본값·튜플 풀기·별표 풀기·`with`·`is`·세미콜론 0. 호출 안 호출 안 호출 0.
- **01~06에서 쓰지 않은 이름 대조**(`/tmp/ch23-07/names_check.py` — Ch 21 07 판을 Ch 23 폴더로): 내장 이름 **0** · 속성 **0** · 키워드 인자 **0** · import 둘(`checkpoint_tools:append_key`·`append_key_once` — 06 노트북 2절이 셀에 적은 함수를 §2-7대로 도구 파일에서 가져오는 줄, 이름은 06 것). 새 문법·새 API·새 말 **0**.
- 셀 모양(`/tmp/ch23-07/shape.py`): 코드 셀 **22**(준비 셋: 설치·가져오기·임시 폴더 — 자리 찾기 셀 없음, 자식 프로세스를 띄우지 않으므로), 준비 셀이 아닌 셀 주석 뺀 코드 최대 **9줄**(`R1_AFTER`·`R2_AFTER`), 함수 본문 최대 **8줄**(`record_loan`), 셀당 정의 하나(정의 둘 + 상태 형식 하나), 첫 줄 주석 100%.
- 금지어(`/tmp/ch23-07/ban_check.py` — 06 판에 「재시작」을 다시 넣은 판): 노트북·`_src`·캡션 넷·`.mmd` 셋에서 걸린 3건은 모두 「프로그램」 안 「로그」. 「재시작」은 06 슬러그 링크(`href`) 둘 말고 0 — 본문은 「다시 실행」. 규격 §4 쓰지 않는 말·「강사 시연」·「반환」·「지연」·「추정」·「스키마」·「superstep」·「병렬」 0. 빌드 HTML `{{`·`[[` 0건.

## 2. 설계 — 붙인 기능과 뺀 것 (규격 §7-2 1번, 인계 「§06 → 실습(07)」 6항)

| 절 | 붙인 기능 | 흐름 안에서 쓰였는가(코드로 센 값 — 두 실행 모두) |
|---|---|---|
| 03 | SQLite 체크포인터(`sqlite3.connect(…, check_same_thread=False)` → `SqliteSaver` → 컴파일, 임시 폴더 파일) · 스레드 이름 = 이용자 번호 · **연결을 닫고 새 연결·새 체크포인터·새 그래프로 같은 스레드 이어 가기** | **쓰임** — 멈춘 뒤 `one_conn.close()` → 새 그래프가 `새 그래프가 읽은 다음 노드: ('record_loan',)`를 읽고, **이어 가기는 그 새 그래프로 함**(`one_graph_again.invoke(None, config)`) |
| 05 | 실패 흉내(`failure_plan`·`call_count`, 05 `flaky`와 같은 `TimeoutError` 글 — 생성기 `assert`) · `try/except TimeoutError` · 원인을 없앤 뒤 `invoke(None, config)` | **쓰임** — `오류 종류: TimeoutError` → `부른 횟수: {'receive_request': 1, 'record_loan': 1}` → 원인을 없애고 `None` → `{'receive_request': 1, 'record_loan': 2}` |
| 06 | `append_key_once`(멱등 키 = 대출 키 `loan-2307`, 도구 파일) · 쓰기 방식 이름 `idempotent`/`naive` | **쓰임(건너뛰기까지)** — 다시 실행된 `record_loan`이 `건너뜀`을 내 칸 `notes: ['신청 받음', '건너뜀']`, 기록 한 줄. 실행 2는 `append_key`로 `적음`·두 줄 |
| 04(읽기만) | `read_saved`·`read_record`(도구 파일) · 저장 시점 기본값 | 결과를 읽는 데만 씀(「결과를 볼 기록 장치」 — PLAYBOOK §3 노트북 차례) |

- **멱등 키 확인이 흐름 안에서 실제로 일하게 한 까닭**(Ch 20 05 검토 B-8 — 붙이기만 하고 흐름에서 쓰이지 않는 부품을 피함): 한 커널 안에서 `append_key_once`가 「건너뜀」을 내려면 기록을 적은 노드가 다시 실행되어야 한다. 기록 노드와 실패 노드를 나누면(기록 → 알림) 이어 갈 때 알림 노드만 다시 실행되어 `append_key_once`는 한 번만 불리고 쓰기 방식을 바꿔도 결과가 같다(05 교훈 — 앞 단계에서 끝난 노드는 다시 실행하지 않음). 같은 단계 두 노드로 두어도 먼저 끝난 기록 노드의 쓰기가 남은 쓰기로 남아 다시 실행되지 않는다. 그래서 **기록을 적는 노드 `record_loan` 안에, 기록 뒤에 실패 흉내**를 두었다(자식 프로세스 없이 되는 유일한 모양).
- **인계 권고와 다른 점 한 가지(강사 확인)**: 인계 「§06 → 실습(07)」 1항은 06 b7의 「실행하지 않음」 항목(그 가운데 「노트북에서 실패 흉내로 멈추기 — 노트북 밖 판 B만」)을 07이 「다루지 않는 쪽」을 권했다. 위 까닭으로 07은 그 장면을 **노트북에서 실행**했다(새 API 0 — 05 실패 흉내 + 06 함수). 06 b7 문장(「검사 없이 적는 쪽은 두 줄, 건너뛰는 쪽은 한 줄 … 노트북에서 실행하지 않았습니다」)은 06 노트북에 대해 여전히 참이고, 07 결과(두 줄/한 줄)도 그 문장과 같다 — 07 b3·b7에 「06절 주의 메모가 노트북 밖에서만 확인했다고 적은 장면을 이번에는 노트북에서 실행」한 문장씩. 나머지 06 「실행하지 않음」(여러 프로그램이 한 파일·저장 시점 `exit`로 끊기·기록 전에 끊기·실제 결제)은 07도 실행하지 않음(b7).
- **값 하나만 바꿈**: 쓰기 방식 `idempotent` → `naive`(**06 Before/After와 같은 값**) — 그래서 b2·노트북 6절 앞에 「새로 볼 것은 같은 커널 안의 실패 흉내로 멈추고 새 연결에서 이어 갈 때도, 같은 차이가 나는지」 한 문장. 파일 이름(`idempotent.sqlite`/`naive.sqlite`·`.record`)은 두 실행의 기록이 섞이지 않게 쓰기 방식 이름을 앞머리로(06 `kill_at_second` 앞머리 선례) — 실험 값이 아니라 기록 자리라고 b4·복습 1에 적음. 스레드 이름은 두 실행 같음(`M-0317`) — 파일이 달라 섞이지 않음(03 8절 「파일 이름만 바꾸면 빈 딕셔너리」와 이음, 한 파일을 함께 쓰는 장면은 실행하지 않음 — b7).
- **손으로 정한 새 값**(규격 §7-2 7번 — 실행 전에 정함, 출력 줄 「출처」와 b7): 대출 키 `loan-2307`(이 절에서 실행 전에 정함, 06 `order-2306`과 같은 모양) · 이용자 번호 `M-0317`(Ch 21 03절 실행 정보 값 그대로 — 과정의 자료실 이용자). 탐색 실행으로 고른 값 아님(설계 뒤 노트북 밖 준비 확인 한 번 — §3).
- **뺀 것**(b3 둘째 단락): 02 PostgreSQL 체크포인터(서버를 따로 켜야 함 — 30분 실습 부담) · 04 저장 시점 비교·강제 종료(04·06에서 견줌, 자식 프로세스는 코드·실행 시간이 늘고 `async` 강제 종료는 흔들림) · 05 같은 단계 두 노드·남은 쓰기·표 `writes`(노드 하나가 멈추는 이번 흐름에 없음) · 03 메시지 칸(대화 아님) · 01 `InMemorySaver`(새 연결로 다시 열 파일이 필요) · 01 `print_history`·`thread_row`, 03 `print_conversation`·`sqlite_tables`, 05 `saved_channels`(쓰지 않아 도구 파일로 옮기지 않음).
- **모델 요청 0번의 처리**: 규격 §7-2 실습 절 「모델 호출 3~5번」과 다름 → b3 한 문장(「다른 챕터의 실습은 모델을 몇 번 부르지만, 이 챕터의 실습은 모델을 부르지 않습니다. 01절처럼 매번 같은 값을 내는 우리 노드여야, 파일에 남은 값이 맞는지 출력으로 가를 수 있기 때문입니다」)·준비물·이 진단·강사 확인(§12). 선례: Part 1 실습 절(Ch 1·3·4) 0번. 모델을 넣으려면 잠금을 바꿔야 함(`uv lock`, 보호 파일 — 챕터 리드 결정 없이 하지 않음).
- 파일 쓰기는 임시 폴더에만(챕터 결정 2, 앞머리 `ch23-07-` — 생성기 `assert`). Part 3 실습 절 「파일을 쓰지 않습니다」 선례와 다름 — 이 챕터 주제가 파일에 남기는 일이라서(학생 폴더에는 남기지 않음).

## 3. 결정성 확인 (규격 §7-2 6번 — 모델이 없으니 흔들림 확인 대신 두 번 같아야 함)

- 노트북 밖 준비 확인: 규칙을 먼저 적고(`/tmp/ch23-07/probe-rule.txt`, 11:16:22Z — 무엇·몇 번·판정·환경) 노트북 설계와 같은 흐름(`/tmp/ch23-07/dry.py`)을 새 Python 프로세스로 **10번**(회마다 `idempotent`·`naive` 두 실행 = 20 장면, 11:16:33Z 끝) — 출력 전체 해시 **10/10 같음**(`b384129fd29a…`). 값: 실패 뒤 `('record_loan',)`·3·키 한 줄 → 새 그래프가 같은 자리 → 이어 간 뒤 `{'receive_request': 1, 'record_loan': 2}`·`()`·4 · `idempotent` 한 줄 `건너뜀` / `naive` 두 줄 `적음`. 체크포인트 차례(단계 -1 `input` → 0 → 1 → 2, 다음 노드 `('__start__',)` → `('receive_request',)` → `('record_loan',)` → `()`)는 확인만 하고 노트북에는 수만 출력.
- 결론·그림·정리·복습의 값은 모두 이 확인과 새 커널 두 번에서 같았던 값. 흔들린 값 없음 → 결과 읽기 둘째 단락에 「이번 실행에서는」 값을 둔 곳 없음. 04 `async` 강제 종료 값은 쓰지 않음.

## 4. 새 커널 두 번 (규격 §2-7 9번 끝 — 그림 그리기 전)

- **A** `run_section.sh`(셀 실행 기록 11:27:23.81~24.89Z, 약 1.1초 → 준비물 「5초 안에」) — **`PASS 07-Persistence-실습.ipynb: 22 cells`**. 그림 PNG가 아직 없어 `attach_figures.py`에서 멈춤(실행·저장은 끝난 뒤 — 이후 `--no-exec`로 첨부·빌드·verify·게이트).
- **B** 사본 `/tmp/ch23-07/B.ipynb`를 `execute.py`로(11:27:49~51Z, `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch23-persistence UV_NO_SYNC=1 PYTHONPATH=…/notebooks`) — `PASS`. 두 실행 모두 빈 임시 폴더에서 시작(폴더 이름 출력 안 함), 두 실행 모두 `PYTHONDONTWRITEBYTECODE=1`(실습 폴더 `notebooks/__pycache__/` 만들지 않음 — 확인함).
- 셀별 출력 글자 대조(`/tmp/ch23-07/cmpout.py`) **22/22 같음**, 셀별 출력 글자 해시(`texthash.py`) A·B 모두 `25a27d2a6cc440a4…`. `code_sha256` **`c950067c72cc7f49449d7477e6704e008cec114dc5b3bc8cf4e36956f833675a`**, `outputs_sha256` A·B 모두 **`5db80578cc6b9b034f20a741e7371948c862ad99ddb97fc648ba78d1ec4f4309`**. 교재 노트북은 A.
- 뒤이은 `mdpatch.py`(`/tmp/ch23-07/reps1.json` — 07-1 alt·도식 읽기 한 문장, 07-1 첫 렌더 뒤 배치가 바뀌어서)·`author_07.py --src-only`(삽화 alt·캡션·그림 읽기·비유 풀이)·`--no-exec`의 `attach_figures.py`는 노트북 마크다운·`_src`만 바꿈 — `code_sha256`·`outputs_sha256`·`executed_at`(11:27:25Z) 그대로, A 사본과 셀별 출력 22/22 같음.

## 5. 결정적 값의 자리

| 값 | 성격 | 둔 자리 |
|---|---|---|
| `오류 종류: TimeoutError` · `부른 횟수` 1·1 → 1·2 · `다음 노드: ('record_loan',)` → `()` · `체크포인트 수` 3 → 4 · `멈추기 전에 적힌 키: ['loan-2307']` · `새 그래프가 읽은 다음 노드: ('record_loan',)` · 칸 `notes` `['신청 받음', '건너뜀']`/`['신청 받음', '적음']` · 같은 키 줄 수 1/2 · 7절 두 줄 · 파일 넷 | 우리 코드·라이브러리 규칙(밖 10/10·A·B 같음) | 결과 읽기 첫 단락·b6 표·그림·정리·복습 |
| 체크포인트 차례(단계·만든 자리) | 밖 확인에서만 봄 | 출력하지 않음(04·06 문장 「06절에서 둘째 노드 안에서 끊긴 뒤의 수와 같습니다」로만 이음) |

## 6. 그림

- Mermaid **3장**(규격 §7-2 그림 = 조립도 · 실행 1 실제 순서 · 실행 1·2 비교): `07-1` flowchart TB 상자 일곱 **836**(첫 렌더 809는 오른쪽 위 상자의 화살표가 회색 `SqliteSaver` 상자 뒤를 지나감 → 선언 차례·보이지 않는 연결 `~~~` 둘로 두 상자를 오른쪽으로 → 938(868 넘음) → 라벨을 `<br>`로 줄여 836) · `07-2` flowchart TB 한 줄 상자 일곱 **263**(세로 981 — 저절로 꺾인 줄을 `<br>`로 미리 나눔) · `07-3` flowchart TB 초록 → subgraph 둘 + 공통 회색 `~~~` **655**. **모두 868 이하, 빨강 0, 보라 0**(experiment·모델 없음 — `naive` 두 줄도 출력으로 본 값이라 노랑). PNG를 매번 직접 열어 봄(`.cache/ch23-07-view/`, 같은 이름 사본은 보기 도구가 옛 그림을 보여 `m1-v3`~`v5` 새 이름으로). 색: 우리 코드 파랑 · 대출 신청·쓰기 방식(바꾼 값) 초록 · 출력·받은 오류 노랑 · 라이브러리 `SqliteSaver`·그래프·두 실행 공통 회색.
- 삽화 **1장** `07-4-리본으로-이은-사진과-기보`(비유 계열 「체스판과 즉석사진」 07 — 01~06 장면을 되풀이하지 않고 새 소품 **리본**(과정 grep 0건)으로 판·사진·기보를 한 줄로 이음) — **1차 job `a6c8200a-a747-4590-824a-e3c904038749` 채택**, 재생성 0, **2크레딧**(거래 **2026-09-25T11:32:55Z 「Nano Banana Pro −2」**, 생성 전 잔액 2433.75, 바로 앞 거래 10:57:21Z는 06절 몫). 응답 모델 표시 `nano_banana_2`(01~06과 같음). 원본 `95379c0b…`(2752 × 1536) → 저장 `68179ede…`(1100 × 614), 결과 URL을 한 번 더 받아 줄인 그림과 픽셀 대조 bbox `None`·최대 차이 0. 저장 PNG 사본과 원본 확대 두 장을 직접 보고 셈: 나무 탁자 하나 · 체스판 하나(**흰 나이트 하나만 판 가운데 옆으로 누움**) · 판 앞 왼쪽 즉석사진 한 장(작은 체스판) · 오른쪽 흰 종이 한 장에 검은 나이트 실루엣 하나 · 빨간 리본 하나가 판 앞 가장자리에서 두 물건 사이로 탁자 끝까지 이어지고 두 물건 사이에 매듭.
- **삽화 검수에서 고친 것**: 프롬프트는 「두 물건을 리본으로 묶음(tied together)」이었지만 그림의 리본은 **두 물건을 감싸지 않고 판에서 두 물건 사이로 이어진 모양** → 재생성하지 않고(관계 — 판 하나에 딸린 사진 한 장·기록 한 장·쓰러진 말 하나 — 는 읽히고, 재생성에서 개수가 틀릴 위험이 01·02 선례로 더 큼) 본문 비유·alt·캡션·그림 읽기를 **보이는 대로 「리본 하나로 판과 이어 둠」**으로 고치고 파일 이름도 `…묶은…` → `…이은…`(`mv -n`, 지운 파일 0). 세부 `figures/07-4-…prompt.md` 「상태」. 서 있는 흰 나이트 둘·앞으로 나온 검은 나이트 하나는 짝짓지 않음(그림 읽기 「판 위 말의 개수·색과 판의 칸 수는 무엇과도 짝짓지 않습니다」).

## 7. 서비스 요청과 비용

- 모델·임베딩 요청 **0번**(노트북 A·B, 노트북 밖 확인 모두). 키는 읽지 않음.
- Higgsfield 1회 생성, 2크레딧(§6). WebFetch 0(참고 자료는 앞 절과 설치판 소스 행 — 소스 행은 이번에 다시 열어 봄: `langgraph/pregel/main.py` 2967~2968행·`_loop.py` 856·861~865행).

## 8. 도구 파일 `notebooks/checkpoint_tools.py`

- **바꾸지 않음**(`71280dd9fdd748bb9ae98388990a7ed0d33d07e3fb1246abfba95c64c4437c29` 그대로 — 생성기가 해시를 `assert`). 이 절이 쓰는 앞 절 평범한 함수 넷(`append_key`·`append_key_once`·`read_record`·`read_saved`)은 모두 06절이 만든 파일에 이미 있음 — 가져오기는 알파벳 순 한 줄(임시 폴더로 옮기기 전 준비 셀) + 고정 세 문장 + 커널 폴더 한 문장 + 「교재 출력은 실행 도구가 도구 파일 폴더를 따로 알려 준 실행」 한 문장(과정 §9 — 07은 자리 찾기 셀이 없어 가져오기 결과 읽기에). 함수 넷은 `author_06.DEF_APPEND`·`DEF_ONCE`·`author_04.DEF_READ`·`DEF_RECORD`와 문자열 포함·AST 같음(`check_same_as_before()`).
- 노트북 전역 이름(`call_count`·`failure_plan`·`write_plan`)에 기대는 노드 둘과 상태 형식은 노트북에 적음 — 상태 형식은 06 `OrderState`와 칸 이름만, 설계 객체 여섯 줄은 06과 상태 형식·노드 이름만 다름(생성기 `assert`, 본문 「06절 설계 객체와 같은 모양」의 근거). 노트북에만 있는 앞 절 평범한 함수는 쓰지 않아 옮긴 것 0.
- 06 진단 §11-2 「07이 06 함수 셋을 쓰지 않으면 도구 파일에만 남음」 → **07은 06 함수 둘(`append_key`·`append_key_once`)을 가져와 씀**, `kill_then_resume`은 쓰지 않음(도구 파일에만 — 마감 확인).

## 9. 06절 이음새 (06 노트북은 다시 실행하지 않음)

- 06 b8·노트북 정리 끝 「07절 실습에서는 이 챕터에서 배운 것을 작은 흐름 하나에 모아 실행합니다」 → **07 내용과 맞음**(03·05·06 기능을 대출 처리 한 흐름에). 01~05 b8처럼 **`_src` b8에 07 링크만** 더함: `author_06.py`(`912c8dc7…` → `f620b444e385…`, `_src` 문장 한 곳 — 고치기 전 생성기 `src_html()`이 그때 `_src`와 같음을 먼저 확인) → `author_06.py --src-only`(`_src/06` `302faf19…` → `000920725beb…`) → `run_section.sh … 06 --no-exec`(06 게이트 0). 노트북 정리 끝은 링크 없는 선례(01~05도 글자만)라 `mdpatch.py`를 쓰지 않음.
- **06 노트북 그대로**: 파일 `869b6ae460f4…`(전후 같음) · `code_sha256` `52c92b7d341090c2…` · `outputs_sha256` `8cf67c492cc628b4…` · `executed_at` 10:54:54Z 그대로.
- 06 빌드 HTML `2b2a9a45…` → `818b6b402240…`(b8 링크 + 다음 절 링크). 01~05 빌드 HTML은 각 진단 해시와 같음(`d2581c77`·`03bde627`·`7e2c3dc1`·`7c175686`·`df15083f`), 챕터 `index.html` `45f0847c…` → `822f099e9e8f…`(07 링크).

## 10. 챕터 밖 수정 · 보호 파일

| 파일 | 무엇을 |
|---|---|
| `textbook/part6/public-files.json` | `python3 textbook/part6/qa/collect_public_files.py`로 다시 모음(Ch 21 마감 선례) — **07 노트북 한 줄만** 늘어남(`9beba972…` → `8ed6852b524f…`, 보호 파일, 80줄). 함께 쓰는 `prerequisite-files.json`은 바이트까지 같음(`4c7f5a4b…`) |
| `textbook/part6/index.html` | `python3 textbook/part6/_build_index.py`가 다시 씀 — Ch 23 「7절」·07 링크(`c465e7b4…` → `ec2588c0fded…`, 보호 파일) |
| `textbook/downloads/part6-practice.zip` | 같은 스크립트가 다시 만듦(`3755de3d…` → `43b1923fa3e3…`, 보호 파일) — **Ch 23 항목 13개가 모두 디스크와 같아짐**(01~07 노트북·worker 둘·도구 파일 `71280dd9…`·README 새 판·잠금 둘) |
| `textbook/part6/qa/integration-results.json` | 같은 스크립트가 다시 씀(`e539f6d2…` → `2ff2be9f8cd6…`, 보호 파일) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json` | `verify.py --chapter`가 다시 씀(`5cf08935…` → `8d2cedf1b8e2…`, 보호 파일·기록 파일) |

- 챕터 안(실습 폴더 포함): `chapter.json`(07절 추가, `d45772cc…` → `36267fb51acb…`, 보호 파일, `hours`·`objectives` 그대로) · 실습 폴더 `README.md`(맨 아래 07 한 단락, `2c9516e0…` → `a876fed0efab…`, 보호 파일) · 챕터 `qa/public-files.json`(07 HTML·노트북 두 줄, `8aa1f73d…` → `d16b71f330f8…`, 보호 파일) · `qa/verification.md` 07 행(`6587bb44…` → `398ec8fadeed…`, 보호 파일) · `집필점검표.md` 07 행(`23b6c74deedb…`) · 06 `author_06.py`·`_src/06`·빌드 HTML(§9) · 새 파일(노트북 07·`_src/07`·빌드 07·`figures/07-*` — `.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md` 셋 + 삽화 `.png`·`.prompt.md`·`.caption.md` · `qa/upgrade/author_07.py`·`07-figures.md`·`07-diagnosis.md`·`gates-wip-07.json`·`gates-wip-07-07.json`·`gates-wip-ch23-after07.json`·`review-pack/07-…md`) · `handoff.md` 「실습 → 챕터 검토」·`manifest-changes.md` 「07절 끝」.
- **보호 파일 123개**: **104개 같음 · 19개 바뀜 · 없어진 파일 0** = 06절 끝까지 바뀐 14개(이 절이 값을 다시 바꾼 것: 묶음 목록 둘·`verification.md`·notebook-contracts) + **이 절이 지시대로 바꾼 다섯**(`chapter.json`·실습 폴더 `README.md`·`part6/index.html`·`part6-practice.zip`·`integration-results.json`). `textbook/index.html`은 그대로(`1aea1103…`).
- **고치지 않은 것**: 01~05 파일(노트북·`_src`·생성기) · 06 노트북 · 도구 파일 · worker 둘 · 실습 폴더 `pyproject.toml`·`uv.lock` · Ch 24 파일(공용 옛 생성기 `qa/author_ch23_ch24.py` 포함) · 옛 그림 · 공용 도구·게이트·`verify.py`·`build_index.py`·`_build_index.py`(21행 설명·시수 그대로) · 규격·과정 요약. **파일 삭제 0건**(삽화 `.prompt.md`는 `mv -n`으로 이름만 바꿈).

## 11. 검사 결과 (Part 6)

- `run_section.sh … 07 --no-exec`: 게이트 **0**, `verify.py --chapter` **`PASS 7 sections / 179 code cells (max 14 lines)`**, 빌드 HTML 07 `{{`·`[[` 0건, SVG 셋·삽화 JPEG 하나 인라인. 07·06·목차 쪽 상대 링크 59개 모두 파일·조각이 있음(`check_delivery.py`의 링크 규칙으로 따로 확인), 07 복습 4문항·해설 4·고정 블록 b1~b10 있음.
- `python3 textbook/part6/_build_index.py` → **`Part 6: 50 verified sections; 96 bundled files`**(Ch 23 「강의 6시간 · 실습 10시간 · 7절」, 21행 설명 문장은 그대로 — 마감 몫).
- `check_delivery.py` → **117행 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`에서 멈춤**(`llm-practice.zip` — 알려진 일, 전체 마감 몫). 그 앞(절 검사 50·페이지 비밀값·개인 경로·`part6-practice.zip` 매니페스트 신선도)은 지나감. `delivery-results.json`은 쓰기 전에 멈춰 **안 바뀜**(`3cc2d143…`).
- 묶음 실행 검사(`check_bundle_execution.py`)·`visual.cjs`·옛 검사 넷·`check_scope.py`는 **돌리지 않음**(마감 몫).

## 12. 강사 확인 대상

1. **모델 요청 0번**(규격 §7-2 실습 절 3~5번과 다름) — 챕터 리드 결정(모델 없는 챕터, 잠금에 모델 패키지 없음)을 따름. Part 1 실습 절 0번 선례.
2. **06 b7이 노트북 밖에서만 본 장면(실패 흉내로 멈춘 뒤 이어 가기)을 07이 노트북에서 실행**(인계는 「다루지 않는 쪽」 권고) — 멱등 키 확인이 흐름에서 실제로 일하게 하려는 설계(§2). 결과는 06 b7 문장과 같음.
3. **실행 2가 06 Before/After와 같은 값(쓰기 방식)을 바꿈** — 「새로 볼 것」을 강제 종료가 아닌 한 커널 안의 실패 흉내·새 연결로 둠. 다른 값(저장 시점 `exit`)을 바꾸면 체크포인트 수만 달라지고(05 비교 되풀이) 기록 줄 수는 같아 고르지 않음.
4. **대출 키 `loan-2307`을 새로 정함·이용자 번호는 Ch 21 03 값** — 흐름을 보여 주려고 정한 예(출력 줄 「출처」·b7).
5. **삽화 리본 모양** — 프롬프트는 「묶음」, 그림은 「판에서 두 물건 사이로 이어짐」 → 재생성 없이 본문을 보이는 대로 고침(§6).

## 13. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: `handoff.md` 「실습 → 챕터 검토」 5번.
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 **`/tmp/ch23-07/`**(`A.ipynb`·`B.ipynb`·`dry.py`·`probe-rule.txt`·`probe/`(`run-1`~`run-10.txt`)·`illu-1-orig.png`(3.3MB)·`illu-1-again.png`·`illu-1-1100.png`·`reps1.json`·`manifest_check.py`·`names_check.py`·`extra_check.py`·`ban_check.py`·`shape.py`·`cmpout.py`·`texthash.py`·`pixcmp.py`·`resize.py`·`figtext.py`·`chapter.before.json`·`author_06.before.py`·`README.before.md`·`집필점검표.before.md`·`verification.before.md`·`handoff.before.md`·`ch-public-files.before.json`·`part6-public-files.before.json`·`part6-prereq.before.json`·`hashes-before07.txt`·`before-build-index.txt`) · 기기 세션 임시 폴더 **`$TMPDIR/ch23-07-*` 둘**(노트북 A·B, 각 파일 넷) · **`$TMPDIR/ch23-07-dry-*` 열하나**(`dry.py` 준비 확인·첫 시험, 각 파일 넷 — 연결 폴더 밖) · `.cache/ch23-07-view/`(PNG 열 — 그림 확인 사본·확대 둘) · `qa/upgrade/__pycache__/author_07.cpython-310.pyc`(시스템 python으로 생성기를 import할 때 한 번 생김 — 나머지 실행은 `PYTHONDONTWRITEBYTECODE=1`) · `qa/upgrade/gates-wip-07*.json`·`gates-wip-ch23-after07.json`.

## 마감 반영 (2026-09-25, 검토 1차 `review-round1-A.md`·`review-round1-B.md`)

- **A-1** b3 표 01절 줄 「같은 스레드를 이어 실행하는 규칙」 → 「같은 스레드로 다시 부를 때의 규칙」.
- **B-2(07 몫)**: 3절 딕셔너리 셀에서 `write_plan["prefix"] = new_prefix(write_plan["mode"])`(04절 함수, 도구 파일), 노드 `record_loan`은 `write_plan["prefix"] + ".record"`에 적음, 실행 1·2의 연결·읽기 셀은 `one_prefix`·`two_prefix`(`idempotent-1`·`naive-1`), 실행 2 설정 셀도 앞머리를 새로 고름, 7절 견주기는 앞머리마다 한 줄(`idempotent-1 | … | 4 | 1`·`naive-1 | … | 4 | 2`), 마지막 파일 목록 `['idempotent-1.record', 'idempotent-1.sqlite', 'naive-1.record', 'naive-1.sqlite']`. 실행 1 연결 셀은 `SQLite 파일 이름: idempotent-1.sqlite`도 출력. **설정 셀(3절 딕셔너리 셀·6절 첫 셀)부터 다시 실행하면 앞머리 번호만 오르고 나머지 출력은 같음**(노트북 밖 확인 — 실행 1 일곱 셀 5/7·실행 2 다섯 셀 4/5가 같고 다른 셀은 번호 줄뿐). 준비물·3절·b4·b7에 안내. 새 문법·API 0 — 01~06에 없는 내장 이름·속성·키워드 0(`names_check.py`), import에 `new_prefix`(04절 함수)를 더함(함수 다섯). `TOOLS_SHA256`을 마감 판으로, `check_same_as_before()`에 `DEF_NEW`·`author_06.TOOLS` 대조를 더함.
- **B-12** b4 「비교와 경계」·복습 4 해설 「체크포인트는 칸 값만 지키고」 → 「칸 값과 칸에 낸 갱신만 담고」. **B-13** 삽화 뒤 비유 풀이 첫 문장 → 「리본은 판 앞 가장자리에서 사진과 기보 사이를 지나며, 두 물건이 이 판 하나에 딸린 것임을 보이려고 둔 소품입니다.」(PNG를 다시 보고 — 리본은 판 가장자리에서 두 물건 사이를 지나 탁자 끝으로, 두 물건에는 닿지 않음. 다시 만들지 않음, Higgsfield 0) · `figures/07-4-….prompt.md` 「설명 대상 문장」을 지금 b4 글로.
- **그대로(강사 확인)**: 모델 요청 0 · 실행 2가 06과 같은 값(쓰기 방식) · 06 b7 장면을 07이 실행.
- **새 커널 두 번**: A `run_section.sh`(12:36:31.67~12:36:32.69Z, 약 1.0초 → 「5초 안에」 그대로) `PASS … 22 cells` · B 사본 PASS · **22/22 같음**. `code_sha256` `c950067c72cc…` → **`166e293b3b08d731d5795266a9bff0bd9afffc545ce655dc6830014d437052c2`** · `outputs_sha256` `5db80578cc6b…` → **`463388271dd6317f38167c574a1b899553d345759647ed2b5caab158371d7b51`** · 파일 `0fe06118afcf…` → `44613fb4a4b1…` · 생성기 `21e1e5e9533a…` → `22edf45e1a88…`. 게이트 0(검사 문장 333 → 344).
