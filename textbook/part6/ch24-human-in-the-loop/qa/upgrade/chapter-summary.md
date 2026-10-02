# Ch 24 Human-in-the-Loop와 Time Travel — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part6/ch24-human-in-the-loop` 01~03절(품질 개선) + **04절 챕터 끝 실습 절 신설**(`04-Human-in-the-Loop-실습`), 노트북 `labs/part6/ch24-human-in-the-loop/notebooks/01~04-*.ipynb`, 도구 파일 `notebooks/approval_tools.py`. 뒤 챕터가 읽는 계약 파일(산출 파일)은 없습니다.
- 기간: 2026-09-25(준비 조사 · 01~03절 개선 · 04절 신설 · 검토 1차 반영 · 챕터 마감). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 세 절 합계 **93**(G1 6 · G2 7 · G5 15 · G6 56 · G7 9 — 01 33 · 02 27 · 03 33, `gates-before.json`) → 마감 뒤 **4/4 PASS, G1~G7 모두 0**(`gates-after.json`, 검사 문장 388·421·417·367 = **1,593**).
- 코드 셀 28·28·28·28 = **112**(`verify.py --chapter` → `PASS 4 sections / 112 code cells (max 12 lines)` — 12줄은 준비 셀). Mermaid **16장**(01 넷 · 02 다섯 · 03 넷 · 04 셋), 삽화 **4장**(절마다 하나, Higgsfield 8크레딧 — 모두 1차 채택, 마감 0), 복습 문제는 HTML에만.
- **모델 요청 0번(네 절 모두)** — 챕터 리드 결정 1(M1). API 키 셀·모델 셀·`dotenv` 없음, 실습 폴더 잠금에 모델 패키지 없음. 사람의 답은 모두 셀에 적은 값입니다.
- 화면 검사 `visual.cjs`: HTML **다섯 개**(네 절 + `index.html`) × 1280px·390px = **10행 PASS**.
- **마감에서 다시 실행한 노트북: 없음.** 네 노트북 모두 `code_sha256`·`outputs_sha256`·`executed_at`이 전후 같습니다(마크다운만 — §17).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 23 요약 → **이 문서** → `handoff.md`(절 사이 세부, 끝 「검토 반영과 챕터 마감 (2026-09-25)」) → 절별 `NN-diagnosis.md`(끝 「마감 반영」) → 검토 `review-round1-A.md`(01~02·공통)·`review-round1-B.md`(03~04) → 준비 조사 `chapter-lead-notes.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 문법·API | 새로 만든 함수 (도구 파일에 둔 것은 굵게) | 새 용어 |
|---|---|---|---|
| 01 interrupt 승인 게이트 (paired) | **노드 안 `interrupt(질문 값)`** · 결과 키 `__interrupt__`와 항목 `Interrupt`의 `.value` · **`invoke(Command(resume=답), config)`** — `resume`의 값이 노드 안 `interrupt`가 내놓는 값 · 멈춘 동안 `get_state(config).next`·`.tasks[0].interrupts[0].value` · 이어 갈 때 노드가 **첫 줄부터 다시 실행**(노드 안 `print`로 두 번 시작) · 체크포인트 2 → 3(노드 하나짜리 그래프) · Before `charge_then_ask`(적고 묻기) ↔ After `ask_then_charge`(묻고 승인일 때만 적기) · 6절 `receive_then_ask`(`append_key_once`로 멱등 앞쓰기) | 노드 넷(`ask_only`·`charge_then_ask`·`ask_then_charge`·`receive_then_ask`, 노트북) · 도구 파일에 Ch 23 함수 **`read_record`·`append_key`·`append_key_once`**(글자 그대로 옮김) | 멈춤 표시 · 질문 값 · 사람의 답으로 이어 가기 (3) |
| 02 Command resume으로 실행 재개 (experiment) | 허용 답 목록 `in` 검사 · **조건부 엣지로 다시 묻기**(노드에서 `interrupt` 한 번 → 오류 글을 칸 `error`에 → 조건 함수 `after_answer` + 이름표 표로 같은 노드에 되돌아감, Ch 13 03 · Ch 20 03 모양) · **권하지 않는 모양** 노드 안 `while True`(4절 한 셀 — 부른 차례대로 답을 맞춤) · 실패 둘: 체크포인터 없이 `Command(resume=…)` → `RuntimeError` · 멈춘 적 없는 스레드 → `KeyError`(칸 값 `{}`·다음 노드 남음·`tasks[0].error`) · 노드 밖 `try`/`except 오류이름 as error` 둘 | `make_question`·`record_counts`·`ask_once`·`after_answer`·`ask_in_loop`(노트북) | 다시 묻기 · 차례 맞추기 (2) — **허용 답 목록은 Ch 16 01·Ch 18 02 「허용 목록」을 이어 쓴 말**(마감 A-6, meta 3 → 2) |
| 03 상태 기록과 다른 분기 재실행 (experiment) | `list(get_state_history(config))`에서 **`for`+`break`로 지난 체크포인트 고르기** · **`update_state(고른 설정, {칸: 값})`** → 만든 자리 `update`·단계 = 고른 자리 + 1·부모 = 고른 자리 · **`invoke(None, 고른 설정)`**으로 뒤 노드만 다시 실행(새 가지) · 값을 바꾸지 않고 옛 설정으로 다시 실행 → 만든 자리 **`fork`** · 멈춤 표시 노드가 다시 멈춤 · 스레드 설정은 가장 최근 가지, 원래 값은 담아 둔 설정으로만 · 정수 백분율 `//`(소수 할인율 `6699` ↔ `6700`) | **`find_before`**(이 절이 처음 가르침, 도구 파일로) · 도구 파일에 Ch 23 01 **`print_history`** · 노드 셋(`quote`·`discount`·`ask_price`, 노트북) | 지난 체크포인트에서 다시 실행 · 값 고쳐 넣기 · 새 가지 (3) |
| 04 Human-in-the-Loop 실습 | **새 문법·새 API 0**(01~03 이름만 — 01~03 노트북에 없는 내장 이름·속성·키워드 0, 새 import는 도구 파일의 `find_before` — 03 함수) | 0(상태 형식 `ExtendState`와 노드 셋·조건 함수만 노트북에) | 0 |

- 새 용어 합계 **8개**(절 meta 「새 용어」 3·2·3·0 — 02는 마감에서 3 → 2).
- **이 챕터 주제라서 허용한 문법**: 칸만 적은 `TypedDict` 상태 형식(칸 구성이 바뀌면 새 이름 — `ApprovalState`·`ReviewState`·`PriceState`·`ExtendState`) · `while True`는 **02절 4절 「권하지 않는 모양」 한 셀뿐**(마감에서 handoff 허용 목록에 한 자리 예외로 적음 — 강사 확인) · `try`/`except RuntimeError`·`KeyError`는 02절 6절 노드 밖 둘뿐 · 키워드 없는 `sorted`(마지막 셀).
- **쓰지 않은 것(네 절·도구 파일 모두 0건, 마감 AST 따로 `extra_check.py`)**: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·튜플 풀기·별표 풀기·`{**…}`·숫자 밑줄·세미콜론·`isinstance`·데코레이터·`Path`·`unlink`·노드 안 `try`·`stream`·`interrupt_before/after`·`as_node`·`Command(goto=…)`·모델.
- 셀 모양: 준비 셀이 아닌 셀 최대 9줄, 함수 본문 최대 8줄(`ask_then_charge`·`ask_in_loop`·`ask_extension`), 셀당 정의 하나, 첫 줄 주석 100%, 호출 깊이 최대 2. `assert`는 우리 코드·라이브러리가 정하는 값(체크포인트 수·줄 수·부른 횟수·만든 자리)에만.

## 2. 앞 챕터에서 이어 쓴 부품과 값

- **Ch 2 05**: `try`/`except 오류이름 as error`(02 6절 — 「셀은 끝까지 · 실제 프로그램은 멈춤」 문장은 마감 A-8에서 더함). **Ch 4 03 → Ch 23 01**: 임시 폴더 준비 셀(네 절이 앞머리 `ch24-NN-`만 다르고 글자까지 같음 — 생성기 `assert`).
- **Ch 13**: 상태·상태 형식·노드·엣지·설계 객체·컴파일·가상 시작점/끝점(01 `Command` — Ch 13 06의 다른 자리 `resume`) · 03 조건 함수·이름표 표 `path_map`(02). **Ch 20** 01 되돌아가는 엣지(02 견줌) · 03 `END`를 내놓는 조건 함수·`__end__`.
- **Ch 16 01·Ch 18 02**: 「허용 목록」 — 02 「허용 답 목록」은 같은 뜻으로 이어 씀(마감 A-6). Ch 18 02 「되묻기」(흐름을 끝내고 되물음)는 02 「다시 묻기」(멈춘 자리에서 다시 멈춤)와 **다른 뜻** — 02 b3·용어 표·노트북 2·3절에 가르는 문장.
- **Ch 17 02** 승인 지점(제목 「승인 게이트」 = 이 말) · **Ch 17 03** 사람 확인(멈추고 넘김, 이어 가기 없음) · **Ch 19 06** 사람 확인 값 · **Ch 18 01** 「게이트」(다른 뜻 — 01 b2·노트북 1절에 한 문장).
- **Ch 23**: 01 `InMemorySaver`·스레드·`get_state`·`get_state_history`(최신 것부터)·만든 자리 `input`·`loop`·`print_history` · 05 `tasks`·`invoke(None, config)` · 06 멱등 키·`append_key`·`append_key_once` · 04 `read_record` · 07 대출 소재(이용자 번호 `M-0317`·대출 키 `loan-2307` — 04가 이어 받음) · 03 「스레드 재개」·04·06 worker 단계 `resume`과 **다른 장면**이라는 문장(01 b3·노트북 3절).
- 소재 번호: 주문 키 `order-2401`(01)·`order-2402`(02)·스레드 `price-2403`(03)·04는 Ch 23 07 값 그대로.

## 3. 절별 사례·값 (새 커널 두 번과 노트북 밖 확인에서 같았던 값)

| 절 | 과제·입력 | 결정적 값(결론·그림에 쓴 값) |
|---|---|---|
| 01 | 노드 하나짜리 그래프, 주문 키 `order-2401`, 사람의 답 `approve`·`reject` | 결과 키 `['order_key', 'answer', '__interrupt__']` · 질문 값 `{'order_key': 'order-2401', 'question': '결제할까요?'}` · 멈춘 동안 `('ask_only',)`·체크포인트 2 → 이어 간 뒤 3 · 네 장면 줄 수 `charge_then_ask \| reject` 2 · `ask_then_charge \| reject` 0 · `\| approve` 1 · `receive_then_ask \| reject` 1 · 파일 `['after-approve.record', 'before.record', 'receipt.record']` |
| 02 | 노드 하나, 허용 답 목록 `['approve', 'reject']`, 답 차례 `maybe` → `yes` → `approve`, 스레드 `edge`·`loop`·`plain`·`other` | 조건부 엣지 모양 시작·부름·체크포인트 `1·1·2 → 3·3·3 → 5·5·4 → 6·6·5` ↔ `while True` `1·1·2 → 2·3·2 → 3·6·2 → 4·9·3` · `RuntimeError: Cannot use Command(resume=...) without checkpointer` · 스레드 `other` `KeyError: 'order_key'`·칸 값 `{}`·다음 노드 `('ask_once',)` · 파일 `[]` · **노트북 밖 확인(마감, b7만)**: 목록 밖 답 다섯 + `approve`면 `12·12·8` ↔ `7·27·3` |
| 03 | 노드 셋 가격 그래프(수량 × 2500 · 정수 백분율 할인 · 확인 노드), 스레드 `price-2403` | 첫 실행 체크포인트 5(`-1 input`·`0~3 loop`) · 고른 자리 `1 \| loop \| ('discount',)` · `update_state` → `2 \| update \| ('discount',)`·부모 `True`·6 · 새 가지 `['discount', 'ask_price']`·질문 값 8000·8 · 스레드 설정 8000 ↔ 담아 둔 설정 9000 · 그대로 다시 실행 `2 \| fork`·9000·10 · 할인 33 → 6700·13 · 실행 횟수 `quote 1`·`discount 4`·`ask_price 7` · 소수 `6699.999999999999`·`6699` ↔ 정수 `6700` |
| 04 | §7 | §7 |

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀)

| 절 | 말 | 뜻 | 코드에서 |
|---|---|---|---|
| 01 | 멈춤 표시(interrupt) | 노드가 그 자리에서 그래프를 멈추고, 사람에게 보일 값을 남기는 일 | `interrupt(질문 값)` · 결과 키 `__interrupt__` |
| 01 | 질문 값 | 멈춤 표시와 함께 사람에게 보일 값(「payload」 대신) | `{"order_key": …, "question": …}` · `.value` |
| 01 | 사람의 답으로 이어 가기 | 멈춘 스레드에 사람의 답을 넘겨 멈춘 노드부터 실행을 이어 가는 일 — 이어 갈 때 노드는 **첫 줄부터 다시 실행**(비유와 다른 점 — 마감 A-1) | `invoke(Command(resume=답), config)` |
| 02 | (이어 씀) 허용 답 목록 | Ch 16 01·Ch 18 02 허용 목록을 사람의 답에 쓴 것(마감 A-6 — 새 말에서 뺌) | `allowed_answers` · `in` |
| 02 | 다시 묻기 | 받아들이지 않는 답이면 까닭을 질문 값에 담아 **같은 자리에서 한 번 더 멈추는** 일 — Ch 18 02 「되묻기」(흐름을 끝냄)와 다름 | 칸 `error` + 조건부 엣지 |
| 02 | 차례 맞추기 | 한 노드 안 여러 `interrupt`에 받은 답을 부른 차례대로 맞추는 일 | `ask_in_loop`(설치판 `types.py` 866~868행) |
| 03 | 지난 체크포인트에서 다시 실행(Time Travel) | 체크포인트 목록에서 지난 것 하나를 골라 그 자리부터 다시 실행하는 일 | `invoke(None, 고른 설정)` |
| 03 | 값 고쳐 넣기 | 고른 체크포인트의 칸 값 일부를 바꾼 체크포인트를 새로 만드는 일 | `update_state` → 만든 자리 `update` |
| 03 | 새 가지(fork) | 지난 체크포인트 하나에서 이어 붙여 새로 쌓은 체크포인트 줄 — **「분기」·「갈래」 쓰지 않음** | 만든 자리 `update`·`fork`에서 시작 |

- **`resume` 겹침 구분**: Ch 23 03 「스레드 재개」(객체를 새로 만든 뒤 같은 스레드로 대화를 이어 감) · Ch 23 04·06 worker 단계 이름 `resume`(강제 종료 뒤 새 프로세스로 다시 실행) · Ch 24 `Command(resume=…)`(멈춰 기다리던 실행에 사람의 답을 넣어 이어 감) — **셋 다 다른 장면**(01 b3 셋째 단락·노트북 3절). 본문에서 「재개」는 제목(02)과 Ch 23 03 말을 가리킬 때만.
- **「승인 지점」**: Ch 17 02 정의 그대로 이어 씀. 01 제목 「승인 게이트」는 이 말이고, Ch 18 01 「게이트」(중간 결과를 코드로 검사하는 자리)와 다릅니다.
- **「새 가지」**: fork의 쉬운 말. 문서의 「Fork」 절(`update_state`)은 만든 자리 `update`, 「Replay」 절(그대로 다시 실행)은 만든 자리 `fork`를 남김 — 엇갈려 짝지어짐(03 b6, 마감 B-2).
- **「남은 날」(04)**: 칸 `left_days`(지금 반납까지 남은 날, 3)만 가리킴. 칸 `due_days`는 **「연장 뒤 남은 날」**(17·10) — 마감 B-7에서 04-2·04-3 라벨을 갈랐습니다.
- **일반 말(새 말 아님)**: 사람의 답 · 승인 지점 · 체크포인트 목록 · 만든 자리 · 다음 노드 · 원래 가지 · 권하는 모양 / 권하지 않는 모양 · 임시 폴더 · 기록 파일.
- **비유 계열 「도미노 줄과 비워 둔 자리」**: 빈자리 = 멈춤 표시 · 빈자리에 도미노를 놓는 일 = 사람의 답 · 넘어진 컵 = 되돌리기 어려운 쓰기 · 맞지 않는 물건(구슬) = 허용 답 목록 밖의 답 · 원래 줄 옆에 새로 세운 줄 = 새 가지. **실제 그래프는 이어 갈 때 멈춘 노드의 첫 줄부터 다시 실행**하므로 빈자리 앞의 컵은 한 번 더 쓰러집니다(01 b4 「비유와 다른 점」 단락 — 마감 A-1).
- **금지어(네 절 설명·주석·캡션·`.mmd`·README·도구 파일 참 금지어 0건 — 제목·슬러그·코드 백틱 말고)**: 「반환」·「경로」·「런타임」·「payload」·「snapshot」·「스냅샷」·「스키마」·「검증」·「포인터」(단독)·「소비」·「분기」·「지연」·「추정」·「직렬화」·「HITL」·「재시작」·「재실행」·「재개」·「게이트」·「갈래」(Ch 13 뜻 말고)·「중단」·「인터럽트」·**「조각」(Ch 5 토큰 전용)** + Ch 23 목록 + 규격 §4 「쓰지 않는 말」. 마감 전후 금지어 대조(`.cache/ch24-close/tools/bandiff.sh`) — 마감이 더한 문장의 새 걸림은 거짓 양성 둘(02 meta 줄 슬러그의 「재개」 · 「프로그램」 속 「로그」)뿐.
- 제목 말 「Human-in-the-Loop와 Time Travel」(챕터)·「interrupt」·「게이트」(01)·「Command」·「resume」·「재개」(02)·「분기」·「재실행」(03)·「Human-in-the-Loop 실습」(04)은 제목과 본문 첫 풀이에만(강사 확인).

## 5. 색 규칙 (Mermaid 16장)

- **넣은 값·사람의 답 초록(tool)** · **우리 노드·부른 줄·함수 파랑(flow)** · **출력으로 확인한 값·받아 출력한 오류 노랑(measure)** · **두 장면 공통 사실·라이브러리·조건 함수(마름모) 회색(클래스 없음)** · **모델 없음 → 보라 0장**.
- **빨강은 paired 01절 Before 결함 결과만**(01-3 「거절인데 같은 키 두 줄」·01-4 `charge_then_ask`). experiment 절(02·03·04)은 빨강 0 — 02 `RuntimeError`·`KeyError`는 노랑.
- 소스로만 확인한 값은 회색 「소스 확인」(02-3). 조건 함수는 노드와 다른 모양(회색 마름모 — 02-1·04-1). 나란한 칸은 subgraph + `~~~` 회색 공통 상자(공통 상자에는 두 칸 출력에서 모두 확인한 값만). 원본 viewBox 폭 모두 868 이하(최대 03-3 674).
- **마감에서 다시 렌더한 `.mmd`: `03-3`·`04-2`·`04-3`**(`--force`, PNG 직접 확인). 03-3은 결과가 든 공통 상자에서 두 칸으로 가던 실선을 없애고 출발 자리를 칸 제목에, 공통 결과를 두 칸 아래 회색 상자(`~~~`)로(B-4, 폭 630 → 674, 상자 일곱 그대로). 04-2·04-3은 17·10 앞말 「연장 뒤 남은 날」(B-7, 폭 269·539 그대로). 노트북 첨부 그림(01-1·02-1·03-1·04-1)은 그대로.
- 삽화 넷: 01-5 도미노 두 줄 · 빈자리 앞/뒤 컵 · 02-6 빈자리의 파란 구슬 ↔ 연두색 도미노 · 03-5 넘어진 나무 줄과 가운데에서 뻗은 주황 줄(넷 넘어짐 · 좁은 틈 · 둘 서 있음 — 마감 B-6에서 틈이 도미노 한 개 폭보다 좁음을 그림 읽기에 밝힘) · 04-4 따로 선 세 색 줄과 이어 붙인 긴 줄(색과 절은 짝짓지 않음 — B-13). 사람·손·화살표·글자·숫자 없음, 네 장 모두 1차 채택·마감에서 다시 만들지 않음.

## 6. 결정적 값과 흔들린 값

- **흔들린 값 없음**(모델 0). 새 커널 두 번(각 절 A·B, 04는 T·A·B 세 번) 셀별 출력 28/28 같음. `outputs_sha256`은 설치 셀 스트림 나뉨으로 A·B가 다를 수 있음 → 셀별 글로 대조(과정 요약 §9).
- **결정적 값**: §3 표 전부 + §7. 달라지는 것은 체크포인트 아이디·`Interrupt.id`·시각·임시 폴더 위치뿐이고 **한 번도 출력하지 않았습니다**.
- **셀 하나만 다시 실행하면** 같은 스레드·같은 기록 파일에 이어 붙어 값이 달라짐 → 네 노트북 준비물·b7에 「1절 임시 폴더 셀부터 다시 실행」.
- **재지 않은 것**: 걸린 시간(마감에서 준비물 「노트북 전체가 2초 안에」를 **「걸린 시간은 재지 않았습니다」로 바꿈** — 챕터 리드 결정) · Windows·macOS 실행 · 여러 프로그램이 한 파일에 쓰기 · 실제 결제·배포 서비스 · 모델·도구 호출 승인.

## 7. 04절 실습 절 주제와 결과

- 제목 「**Human-in-the-Loop 실습: 연장 일수를 고쳐 다시 묻고 승인일 때만 기록하기**」, 슬러그 `04-Human-in-the-Loop-실습`, `format: experiment`, meta 「실습 30분 · 새 용어 0」. **챕터 시수에 더하지 않습니다**(규격 §7-2). 01~03 meta 합 강의 1+1+1 = **3h** · 실습 1.5+1.5+2 = **5h** = `chapter.json` 「총 8h · 강의 3h · 실습 5h」(`_build_index.py`도 3·5).
- Ch 23 07 소재를 이어 받은 대출 연장 신청 한 건 — 스레드 = 이용자 번호 `M-0317`, 대출 키 `loan-2307`, 신청서의 연장 일수 `14`(잘못 적힌 값)·고쳐 넣을 값 `7`·규칙 「한 번에 7일까지」·남은 날 `3`(모두 실행 전에 정한 예 — 출력 줄 「출처」·b7). 상태 형식 `ExtendState`(칸 일곱), 노드 `look_up_loan` → `plan_extension` → `ask_extension` ⇄ 조건 함수 `after_answer`(02 셀과 같은 문자열).
- 붙인 앞 절 기능 셋(두 실행 모두 흐름 안에서 쓰임): **01** 승인 지점(멈춤 표시 뒤, `approve`일 때만 `append_key`) · **02** 다시 묻기(첫 답 `change` → `['ask_extension', 'ask_extension']`·오류 글) · **03** 값 고쳐 넣기와 새 가지(`print_history` 목록 다섯 → `find_before` 단계 1 → `update_state` `2 | update` → `invoke(None, …)` `['plan_extension', 'ask_extension']`). 흐름의 까닭: 목록 밖 답 `change`로는 칸 값을 바꿀 수 없어 지난 체크포인트로 돌아감.
- 실행 1 = 답 차례 `["change", "approve"]`, **실행 2 = 마지막 답 하나만 `reject`**(01 값 바꿔 보기와 같은 값). 「새로 볼 것」은 마감(B-8)에서 「다시 묻기와 새 가지를 거친 흐름에서도, 기록이 마지막 답 하나로 갈리는지」로 좁혔고, 원래 가지에 답을 넘기는 장면은 실행하지 않았다고 노트북 7절에 적음. 설계는 그대로(강사 확인).
- 결과(새 커널 세 번 28/28 같음): `질문 값: {'days': 14, 'due_days': 17, 'error': ''}` → `change` → `'error': '허용하지 않는 값: change'` → `체크포인트 수: 5` → `1 | loop | ('plan_extension',)` → `2 | update | ('plan_extension',)` → `새 가지의 질문 값: {'days': 7, 'due_days': 10, 'error': ''}` → `approve` → `연장 기록 파일의 키: ['loan-2307']`·줄 수 1·실행 횟수 `1 2 5` · 원래 가지 연장 일수 14 · 실행 2 `연장 기록 파일이 있는가: False` · 견주기 `실행 1 | approve | 7 | 10 | 8 | 1`·`실행 2 | reject | 7 | 10 | 8 | 0` · 파일 `['extend-1.record']`. 모델 요청 0 · `assert`는 줄 수 1·파일 없음에만.
- 코드 셀 28(실습 선례 19~25보다 많음 — 강사 확인, 다음 재실행 때 8절 두 셀 합치기 후보). 04 진단의 「규격 범위 20~32」는 근거가 없어 마감(B-12)에서 뺌.

## 8. 도구 파일 `notebooks/approval_tools.py` — 함수 표·해시 변천·생성기 대조 줄

| 함수(인자) | 배운 곳 | 가져오는 절 | 하는 일 |
|---|---|---|---|
| `read_record(record_name)` | Ch 23 04 노트북 3절 | 01·04 | 기록 파일의 줄 → 목록(`split()`) |
| `append_key(record_name, order_key)` | Ch 23 06 노트북 2절 | 01·04 | 기록 파일 끝에 키 한 줄(`"a"`), `"적음"` |
| `append_key_once(record_name, order_key)` | Ch 23 06 노트북 2절 | 01 | 같은 키가 있으면 `"건너뜀"`, 없으면 `append_key` |
| `print_history(history)` | Ch 23 01 노트북 8절 | 03·04 | 체크포인트 목록을 `단계 번호 \| 만든 자리 \| 다음 노드 \| 칸 값` 한 줄씩(아이디·시각 없음) |
| `find_before(history, node_name)` | **Ch 24 03 노트북 4절** | 04 | 최신 것부터 보며 `node_name in snapshot.next`인 첫 체크포인트(`for`+`break`), 없으면 `None` |

- 함수 다섯, 함수마다 `# Ch NN MM절에서 배웠습니다 — …의 같은 이름 함수를 옮겼습니다`, import `os` 하나(SQLite·langgraph 없음 — 이 잠금에 SQLite 체크포인터 없음), 노트북 전역 이름 기대기 0, 금지 문법 0(마감 AST 따로 0건). Ch 23 함수 셋은 `checkpoint_tools.py`(`a850b2cd…`)와 문자열·AST 같음(`author_01.check_same_as_ch23()`), `print_history`는 Ch 23 01 노트북 셀과 같음(`author_03.checks()`), `find_before`는 03 노트북 셀과 같은 문자열.
- **해시 변천**: 없음 → 01 `b40aab98ae6ddd87cb4a0107403193c33d9978c436f1a20cf493873458950a93`(함수 셋) → 02 그대로 → 03 **`d562c9e67c56cab1a6e8435e7f926a7c1858a621faf5f3a9fdaa51a632f1b31f`**(+ `print_history`·`find_before`) → 04·**마감 그대로**(챕터 리드 결정 — 해시 고정).
- 머리 독스트링은 01 판(「Ch 23 04절과 06절 노트북에서 처음 적은 함수 셋은 …」)이라 함수 다섯의 출처를 모두 적지 않습니다(검토 A-13). 함수마다 위 주석에 출처가 있고, 실습 폴더 README가 다섯 함수의 배운 절·가져오는 절을 적었습니다. 머리 설명 고침은 **다음에 도구 파일을 다시 쓸 때**(그때 `author_04.TOOLS_SHA256`·`author_03` 대조 줄·zip·묶음 검사를 함께) — 체크리스트 Ch 24 몫.
- **생성기 대조 줄 고침(마감 A-10·B-17)**:
  - `author_01.py` — 전에는 `--src-only`가 없으면 도구 파일을 **함수 셋 판으로 덮어써** 03·04 가져오기가 `ImportError`로 멈출 모양이었음(`run_section.sh … 01` 실행 모드가 인자 없이 부름). 이제 **파일이 없거나 01 판과 같을 때만 쓰고**, 01 판으로 시작하는 더 긴 판(지금 파일)이면 `skip`을 알리며 건너뛰고, 01 판으로 시작하지 않으면 `assert`로 멈춤. 사본 기기(`/tmp/ch24-close/sandbox` — 생성기 사본 + 읽기 전용 링크)에서 네 경우를 돌려 확인(함수 다섯 판 → 해시 그대로 · 없음 → `b40aab98…`을 씀 · 01 판 → 그대로 씀 · 다른 글 → 멈춤).
  - `author_02.py` `checks()` 셋째 줄 `== author_01.TOOLS` → **`.startswith(author_01.TOOLS)`** — 이제 `--src-only`·`--figures`로 돌아감(마감에서 둘 다 씀).
  - `author_03.py`(`current == author_01.TOOLS or current.startswith(TOOLS)`)·`author_04.py`(`TOOLS_SHA256` `d562c9e6…`·`tools == author_03.TOOLS`)는 지금 파일과 맞아 그대로(`author_03.py`는 머리 설명의 주의 문장만 마감 판으로).
  - 고친 뒤 네 생성기를 `--src-only`로 돌림 → `_src` 넷이 생성기와 같고, `cells()`가 노트북과 셀 62·59·59·59개 모두 같음(`.cache/ch24-close/tools/genmatch.py` — 코드 셀 글 같음, 마크다운은 마감 고침대로). 마감 전 생성기와 노트북이 달랐던 셀은 02 「오늘 볼 그림」 하나(A-4)였고 마감에서 맞춤.
  - 함수 다섯을 `author_01.TOOL_PARTS`로 모으는 일(Ch 23 07 마감 선례)은 하지 않음(도구 파일 글이 바뀌지 않게) — 체크리스트 Ch 24 몫.
- **전체 마감 2026-09-30: 머리 줄 고침, 새 해시 `295bfaf632832bcdd86283c00c09632a0f228f4a5921bb5ec53e4fa3fe9a1f60`**(검토 A-13 · 체크리스트 §2-12 5번·§2-13 6번). 1행 「앞에서 배운 평범한 함수를」 → 「앞 챕터와 이 챕터 앞 절에서 배운 평범한 함수를」, 6행 「Ch 23 04절과 06절 노트북에서 처음 적은 함수 셋은」 → 「Ch 23 01·04·06절 노트북에서 처음 적은 함수 넷과 이 챕터 03절 노트북에서 처음 적은 함수 하나는」. 나머지 머리 줄·함수 다섯 본문·`import os`는 AST·글자 같음. 생성기 안 01 판도 `b40aab98…` → `f0b19507…`(쓰기 가드가 쓰는 판 — 디스크에는 없음). 고친 생성기: `author_01.TOOLS_HEAD`(한 곳) · `author_04.TOOLS_SHA256`(새 값 + 설명 한 줄) — `author_02`(`startswith(author_01.TOOLS)`)·`author_03`(`== author_01.TOOLS or startswith(TOOLS)`)은 글을 따라가서 그대로. 조건 넷: (가) 노트북 넷 마크다운·출력과 `_src`·HTML·README에 머리 글·판 해시 0 · (나) 네 생성기를 파일 쓰기를 가로챈 채(`.cache/final-close/2-tools-head/tools/dryrun.py`) `--src-only`와 인자 없는 모드로 돌림 → `_src` 넷 바이트 같음, 01 가드 `skip`, 03 가드는 같은 글, 04 해시·`author_03.TOOLS` 대조 통과, `check_same_as_ch23()` 통과, `cells()`가 노트북과 62·59·59·59셀 같음(`UPGRADE_RUN_DATE=2026-09-25`) · (다) 새 파일로 네 노트북 사본(`.cache/final-close/2-tools-head/ch24/notebooks`, 키 없이)을 새 커널로 돌려 셀별 28/28 같음(02·03은 설치 셀 스트림 나뉨만 다르고 글 같음 — §9와 같은 흔들림) · (라) 이 줄·handoff·계약 §4. 노트북 `code_sha256`·`outputs_sha256` 전후 같음.

## 9. 묶음 실행 검사 계약 (Part 6 `check_bundle_execution.py`)

- 검사는 `part6-practice.zip`을 풀어 **Ch 24 01**과 Ch 28 01을 키 없이 새 커널로(`uv sync --locked` → `execute.py … --cwd notebooks --kernel-python .venv/bin/python`) 돌리고, zip 속 노트북의 `code_sha256`과 새로 잰 값이 같은지 `assert`합니다.
- **01에 모델·키 셀·새 패키지를 넣지 말 것**(잠금에 있는 것만, `dotenv`도 없이). 01 `code_sha256` **`7187f7a39f3fbd146120412daf4d9675ecf132703117570348b3b570744595ab`**(28셀) — 01 코드 셀을 고치거나 다시 실행하면 zip을 다시 만든 뒤 이 검사를 다시 돌려야 합니다.
- **마감 결과**: `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache UV_LINK_MODE=symlink`만(스크립트 수정 0, `TMPDIR`은 세션 폴더 — 맥 마운트 밖) → **PASS**(Ch 24 01 `PASS 01-interrupt-승인-게이트.ipynb: 28 cells`·`code_sha256` `7187f7a39f3f…` / Ch 28 01 4셀 PASS). 묶음 실행의 `outputs_sha256`은 설치 셀 스트림 나뉨에 따라 `fbaaa8908bd1…`(첫 번째 마감 실행)·`1c27f8cfe46f…`(zip을 다시 만든 뒤 마지막 실행)로 흔들림 — 셀 글은 같고 검사는 `code_sha256`만 봄. `bundle-execution.json` `f53987e8…`(옛 01 `718171990c5d…`·옛 zip `aa82b386…`) → **`a72edd8a79a6561aaad71aa5f9c096cec997d8e4c5f68b4b9e2cfd426951a0af`**(`archive_sha256` `edd8c3be…`).

## 10. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `labs/part6/ch24-human-in-the-loop/notebooks/01~04-*.ipynb`·`approval_tools.py` | 01~04절 · **마감(마크다운만)** | 실습 폴더(챕터 몫) — §1·§8. 마감: 코드·출력 그대로, 파일 `9f25361b`→`a7476f9b` · `5391d97b`→`ba886aff` · `e7649d5a`→`9b5508dd` · `089ed8d9`→`c78b1a2d`. 도구 파일 그대로 `d562c9e6…` |
| `labs/part6/ch24-human-in-the-loop/README.md` | 04절(04 단락) · **마감(전체)** | `7c557ad2…` → **`706f760bf50775e3019a7fdfb32f1927c50e703437cdf66fdee2940cdca5eb8b`**: 노트북 넷(모두 모델 요청 0·API 키 불필요, 01은 묶음 검사가 키 없이 돌리는 노트북), `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 설치 판(`langgraph` 1.2.11·`langgraph-checkpoint` 4.2.0), **파일은 임시 폴더에만**(옛 「실습 폴더의 로컬 파일에만 기록」 뺌), 도구 파일 단락(규격 §2-7 고정 문장 뜻 · 함수 다섯 · 배운 절 · 가져오는 절 · import `os`), 절마다 하는 일, 04 단락. 묶음 밖 파일을 가리키지 않음, 금지어 0(「체크포인터」 거짓 양성 말고), 문장 70자 이하 |
| `textbook/part6/ch24-human-in-the-loop/chapter.json` | 04절 · **마감** | 04 절(04절) · `objectives` 셋 → **넷**(절마다 한 줄 + 04 실습 줄, 옛 「승인 게이트」·「검증」·「중단된」·「재개」·「새 분기」 뺌), `hours` 그대로(`1ee64948` → `40a6a389`, 보호 파일) |
| `textbook/part6/ch24-human-in-the-loop/qa/public-files.json` | 01·04절 · **마감** | 도구 파일(01)·04 두 줄(04) · **옛 SVG 세 줄(`figures/0N-흐름.svg`) 뺌**(본문 참조 0, 파일은 지우지 않음 — `c72eba46` → `6efdb732`, 보호 파일). `collect_public_files.py`로 다시 모은 Part 목록 `textbook/part6/public-files.json`(`7c9cb35e…`)·`prerequisite-files.json`(`4c7f5a4b…`)은 **바이트까지 같음**(도구 파일·04 노트북 줄 있음) |
| `textbook/part6/_build_index.py` | **마감** | ch24 설명 「승인 시점에 중단·재개하고 과거 상태에서 다른 분기를 실행합니다.」 → 「노드 안의 멈춤 표시로 그래프를 멈추고 사람의 답으로 이어 가며, 허용 답 목록에 없는 답이면 조건부 엣지로 다시 묻고, 지난 체크포인트에 값을 고쳐 넣어 새 가지로 다시 실행한 뒤, 대출 연장 신청에 세 기능을 모아 사람의 마지막 답 하나를 바꾸는 실습을 합니다.」(시수 3·5 그대로, `036fbdd2` → `5ffb7dde`, 보호 파일) |
| `labs/part6/continuity-guide.md` | **마감** | Ch 24 줄 가운데 칸 「Ch24 중단·재개, 과거 상태에서 분기」 → 「Ch24 멈춤 표시와 사람의 답으로 이어 가기, 허용 답 목록으로 다시 묻기, 지난 체크포인트에서 값을 고쳐 다시 실행」(`2bc2cadc` → `149a572a`, 보호 파일, 묶음에 들어감). Ch 23 줄 셋째 칸 「Ch24 승인·상태 기록」은 참이라 그대로 |
| `textbook/part6/index.html` · `textbook/downloads/part6-practice.zip` · `textbook/part6/qa/integration-results.json` | 04절 + **마감** | `python3 textbook/part6/_build_index.py`(README·노트북·목록·`chapter.json`을 고친 뒤 한 번 → 04 셀 6 결과 읽기(B-9)를 늦게 고쳐 **한 번 더** — 아래 값은 마지막 판이고, 묶음 실행 검사·`visual.cjs`·전달 검사도 마지막 판으로 다시 돌림) → **`Part 6: 51 verified sections; 98 bundled files`**, zip `61119a82…` → **`edd8c3be117905b50712788b08589becb055afbe44cb1984ffe0638d8e9e7de2`**(101항목, **Ch 24 8파일이 모두 디스크와 같음**, `continuity-guide.md` 같음, `__pycache__` 0, zip 속 01 `code_sha256` `7187f7a39f3f…`), `index.html` `afe83bc7` → `a183814b`, `integration-results.json` `fa46898a` → `a9661d7c` |
| `textbook/part6/qa/bundle-execution.json` | **마감** | §9(`f53987e8` → `a72edd8a`) |
| `textbook/part6/qa/visual-results.json` · `textbook/_notebook/checks/ch24-human-in-the-loop/visual-results.json`(+ 스크린숏 넷) | **마감** | `visual.cjs` 10행 PASS. 공용 파일은 **Ch 24 줄만** 8 → 10(04 두 줄, 새 HTML 해시), `screens` 120 → 122, 다른 챕터 줄 112개 그대로(`367e23e3` → `dd444465`, 보호 파일) |
| `textbook/part6/qa/notebook-readiness.json` | **마감(되돌림)** | 옛 `check_notebook_readiness.py`가 멈추기 전에 다시 써서 실행 전 사본으로 되돌림(내용 변경 0, `b3d69e9c…`) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch24-human-in-the-loop.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀(마감 뒤 `1a241f44…` — 04절 뒤와 같음) |
| **`textbook/part6/ch23-persistence/qa/author_ch23_ch24.py` → `textbook/part6/ch23-persistence/qa/upgrade/before/generators/blocked/author_ch23_ch24.py`** | 01절(막음) · **마감(`mv -n`)** | 공용 옛 생성기(`3fc72ded…` 같음) — Ch 23·24 모두 마감이라 옮김(Ch 23 인계). 부르는 빌드·검사 스크립트 0(`grep` — `before-manifest.json` 둘·`final-artifact-hashes.json` 기록뿐). Ch 23 요약 §16 1번·체크리스트 §2-11 1번에 한 줄 |
| `textbook/part6/ch23-persistence/qa/upgrade/chapter-summary.md` | **마감** | §16 1번 끝에 이동 한 줄 |
| `textbook/qa/upgrade-progress.md` · `textbook/qa/upgrade-final-checklist.md` | **마감** | Ch 24 행 한 줄 · §2-12 Ch 24 항목과 §3·§4 Ch 24 줄, §2-11 1번·§4 Ch 23 줄의 공용 옛 생성기 문장 |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`·`PLAYBOOK.md`·과정 요약·`upgrade-contracts.md` · 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs`·`execute.py`·`render_mermaid.py`·`attach_figures.py`) · Part 6 옛 검사 스크립트와 `check_*`·`collect_public_files.py` · **`textbook/_notebook/build_index.py`**(Ch 24 절 수 3 — 선례대로) · `textbook/part6/qa/final-artifact-hashes.json`(옛 판 기록) · `textbook/part6/qa/ch24-technical-review.md`(Part 6 쪽 옛 검토 기록, 보호 파일) · 실습 폴더 `pyproject.toml`·`uv.lock` · **Ch 25 이후 파일 전부**(Part 6 목차·묶음·공개 목록·기록·`continuity-guide.md` Ch 24 줄 말고) · 도구 파일(해시 고정).
- **파일을 지운 것은 없습니다.** 옮긴 것은 옛 생성기 둘(`mv -n`, 해시 같음): Ch 24 `figures/_gen_figures.py`(`2a015c6a…` → `qa/upgrade/before/generators/blocked/`) · 공용 `author_ch23_ch24.py`(§ 위 표). 옮긴 뒤 `_build.py`·`verify.py`·게이트 통과.
- **보호 파일 131개(`before-manifest.json`)**: **102개 같음 · 27개 바뀜 · 2개 옮김(없어짐)** — 모두 의도한 것. 마감이 바꾼 것 25(Ch 23 `chapter-summary.md` 한 줄(과제 지시) · README · 노트북 01~03(마크다운) · `continuity-guide.md` · zip · 챕터 공개 목록 · `research.md`·`verification.md`·`집필점검표.md`(「개선 전 판」 표시·마감 절) · `bundle-execution.json` · `integration-results.json` · Part 6 `visual-results.json` · 챕터 `visual-results.json` · Part 6 `index.html` · 챕터 `index.html` · 01~03 HTML · 01~03 `_src` · `_build_index.py` · `chapter.json`) + 옮김 2 + 01~04절이 바꾼 뒤 마감이 건드리지 않은 둘(Part 6 `public-files.json` · notebook-contracts). 목록은 `manifest-changes.md` 「마감 뒤」.

## 11. 기준 버전·확인 날짜

- 실습 폴더 잠금(`pyproject.toml` 직접 의존 `langgraph==1.2.11`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`): `langgraph-checkpoint 4.2.0`·`typing-extensions 4.16.0`. 노트북 `%pip`은 네 절 모두 `"langgraph==1.2.11" "langgraph-checkpoint==4.2.0"`(잠금 판).
- 교재 출력: Linux aarch64 · Python **3.12.13** · 환경 `.cache/vm/venv-ch24-human-in-the-loop`(잠금 판). 실행일 모두 2026-09-25(01 13:50 · 02 14:23 · 03 14:52 · 04 15:27 UTC — 마감에서 다시 실행하지 않음).
- 설치판 소스 행(검토 A·B와 마감이 다시 확인): `types.py` 851~871(858~860 처음 부르면 `GraphInterrupt` · 864 노드 처음부터 다시 실행 · 866~868 차례로 맞춤 · 870~871 체크포인터 필요 — 마감 A-2에서 857 → 858) · `errors.py` 50·102 · `pregel/_loop.py` 904~908(`RuntimeError`)·952~971(만든 자리 `fork`) · **`pregel/main.py` 2019(단계 +1)·`pregel/_checkpoint.py` 117·128(만든 자리 `update`)** — 마감 B-1에서 옛 1733~1734(다른 갈래)를 바로잡음 · `main.py` 2522~2524(`as_node` 없을 때).
- 참고 자료(2026-09-25 확인): LangGraph Interrupts(「Rules of interrupts」·「Validating human input」) · LangGraph Time Travel(「Replay」·「Fork」 경고 상자).

## 12. 강사 확인 대상

1. **제목 말**: 챕터 「Human-in-the-Loop와 Time Travel」 · 01 「interrupt」·「게이트」 · 02 「Command」·「resume」·「재개」 · 03 「분기」·「재실행」 · 04 「Human-in-the-Loop 실습」. 슬러그 01은 Ch 23 07 링크 때문에 고정, 02·03은 들어오는 링크 0, 04는 03 b8 링크 하나.
2. **모델 없는 챕터(M1)** — 네 절 모델 요청 0, 키 셀 없음. **04 실습 절도 0번**(규격 §7-2 「3~5번」과 다름 — Ch 23 07 선례, 04 b3를 「Ch 23 07절 실습처럼 …」으로 고침, B-11).
3. **02 `while True` 셀을 기본 경로에 둔 것** — 셀·소제목·b7에 「권하지 않는 모양」, handoff 허용 목록에 한 자리 예외로 적음. 「원리 더 알아보기」(`deep-dive`)로 옮길지.
4. **02 새 말 수 3 → 2**(A-6 — 「허용 답 목록」은 Ch 16 01·Ch 18 02 허용 목록을 이어 쓴 말, 「다시 묻기」는 Ch 18 되묻기와 다른 뜻이라 새 말 유지).
5. **04 실행 2가 01 값 바꿔 보기와 같은 값**(`approve` ↔ `reject`) — 「새로 볼 것」만 실행 2가 보인 만큼 좁힘(B-8 (가)). 원래 가지와 새 가지가 가려지는 설계로 바꾸려면 다시 실행해야 함.
6. **04 코드 셀 28 · 실습 30분**(선례 19~25) — 다음 재실행 때 8절 두 셀을 합치고 5절 글을 4절 끝으로 옮길지(B-12) · 04 소재(목록 밖 답 `change`로 값 고치기)·새 값 넷.
7. **코드 줄 증가**(주석·빈 줄 뺌, `count_code.py`: 01 50→158 · 02 32→146 · 03 43→137 · 04 새 절 153, + 도구 파일 30줄 — 챕터 합 125 → 594) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘. 01의 노드 하나짜리 그래프 셀 넷을 함수 하나로 묶으면 줄지만 새 함수가 생김.
8. **01 멱등 앞쓰기 장면(6절)**·새 도구 파일 · **03 정수 백분율 소재·`fork` 다시 실행을 노트북에서·도구 파일 함수 둘** · Mermaid 4·5·4·3장.
9. **03-5 삽화의 틈**이 도미노 한 개 폭보다 좁음(B-6) — 다시 만들지 않고 그림 읽기·alt·캡션을 보이는 대로 고침. 다시 만들지(남은 재생성 한 번, 2크레딧).
10. **준비물의 걸린 시간 문장**: 「노트북 전체가 2초 안에」(셀 실행 기록 값)를 빼고 「걸린 시간은 재지 않았습니다」로 — Ch 21·23 준비물 선례와 다름. 과정 기준을 정할지.
11. **도구 파일 머리 설명**이 함수 셋 기준(A-13 — 해시 고정 결정으로 그대로, README가 다섯 함수를 설명).
12. **`chapter.json` 학습 목표 셋 → 넷**(절마다 한 줄 + 04 실습 줄, `hours` 그대로) · `_build_index.py`·`continuity-guide.md` Ch 24 문구 · 실습 폴더 README 다시 쓴 범위.
13. **04-2 넷째 상자 색**(B-10) — 상자를 나누면 여덟이 되어(규격 §5-3 일곱 이하) 나누지 않고 도식 읽기에 까닭을 적음.
14. 한국어 감사 3단·그림 판독 2차(별도 세션 — 두 검토의 「확인하지 못한 것」: 삽화 01-5·02-6 직접 판독, Windows·macOS 실제 실행, 학생 `uv sync --locked` `.venv` 첫 셀).

## 13. Ch 25가 이어받을 것과 전제하면 안 되는 것

### 이어받을 것

- 말: 멈춤 표시·질문 값·사람의 답으로 이어 가기(01) · 다시 묻기·차례 맞추기(02, 허용 답 목록은 이어 쓴 말) · 지난 체크포인트에서 다시 실행·값 고쳐 넣기·새 가지(03). 「승인 지점」 = Ch 17 02.
- 사실(참, 출력 근거): `interrupt`를 부르면 `invoke` 결과에 키 `__interrupt__`가 생기고 `get_state(…).tasks[0].interrupts[0].value`로 질문 값을 읽음 · `Command(resume=…)`로 같은 스레드를 이어 가면 노드가 첫 줄부터 다시 실행 · 체크포인터가 없으면 `RuntimeError` · 멈춘 적 없는 스레드로 답을 넘기면 `KeyError`(스레드를 알려 주지 않음) · `update_state`는 만든 자리 `update`, 옛 설정으로 그대로 다시 실행하면 만든 자리 `fork` · 지난 체크포인트에서 다시 실행하면 멈춤 표시 노드가 다시 멈춤.

### 전제하면 안 되는 것 (Ch 25 파일은 고치지 않았습니다)

1. **Ch 24는 모델을 부르지 않았습니다(01~04).** 모델이 고른 도구 호출을 사람이 승인하는 장면·사람 승인 미들웨어(`HumanInTheLoopMiddleware`)·에이전트 그래프에 멈춤 표시를 붙인 장면은 0건입니다. 사람의 답은 모두 셀에 적은 글(`approve`·`reject`·`maybe`·`yes`·`change`)입니다.
2. **`stream`·`stream_events`·`stream_mode`는 0건**입니다. 멈춤 표시는 `invoke` 결과의 키 `__interrupt__`와 `get_state`로만 읽었습니다. **「interrupt와 재개 사건」을 스트림 사건으로 본 적이 없습니다**(Ch 25 01~03 b3 「Ch24에서 interrupt와 재개 사건을 확인했습니다」는 부분 참 — 사건은 Ch 25 몫). 04 b8은 Ch 25 01을 「한 실행에서 생긴 사건을 일곱 방식으로 받아 보는 방법」으로만 가리킵니다.
3. **`resume` 사건 말**: Ch 24 본문은 「재개」를 쓰지 않고 「사람의 답으로 이어 가기」라고 합니다. Ch 25가 스트림의 resume 사건을 말할 때는 Ch 24 `Command(resume=…)`(멈춘 실행에 답을 넣는 호출)·Ch 23 03 「스레드 재개」·Ch 23 04·06 worker `resume` 단계와 무엇이 같은지 한 문장으로 밝히는 쪽을 권합니다.
4. **정적 중단점 `interrupt_before`/`interrupt_after`·여러 노드가 함께 멈춘 뒤 아이디 딕셔너리로 이어 가기·`update_state(…, as_node=…)`(03 노트북 밖만)·`Command(goto=…)`·한 노드 안 `interrupt` 여러 번(02 권하지 않는 모양 말고)·멈춘 채 둔 가지에 답 넘기기·끝난 스레드에 다시 보내기(02 노트북 밖만)**는 노트북에서 가르치지 않았습니다.
5. **체크포인터는 `InMemorySaver`뿐**(이 잠금에 SQLite·Postgres 체크포인터 없음)이고, 체크포인트 아이디·`Interrupt.id`·시각은 한 번도 출력하지 않았습니다. 체크포인트 수·실행 횟수는 절마다 **그 그래프의 값**(01 노드 하나 2 → 3 · 02 조건부 엣지 2 → 5 · 03 첫 실행 5 → 13 · 04 5 → 8)이라 다른 그래프에 그대로 쓰면 안 됩니다.
6. **걸린 시간은 재지 않았습니다**(마감에서 준비물의 「2초 안에」도 뺌). Ch 25의 TTFT·total 비교에 Ch 24 시간 값을 쓸 것이 없습니다.
7. 공용 옛 생성기 `author_ch23_ch24.py`는 마감에서 `ch23-persistence/qa/upgrade/before/generators/blocked/`로 옮겼습니다. Ch 25 쪽 옛 생성기(`textbook/part6/_generate_ch25_ch26.py`)는 Ch 24가 건드리지 않았습니다.

## 14. 챕터 끝 인계 요약 (Ch 25 작업자용 한 줄)

Ch 25 01~03 b3 「Ch24에서 interrupt와 재개 사건을 확인했습니다」 가운데 `interrupt`와 이어 가기는 참이지만 **스트림 「사건」은 Ch 24에 없습니다** — Ch 25가 사건을 처음 보이거나 문장을 「Ch24에서 interrupt로 멈추고 사람의 답으로 이어 가는 것을 확인했습니다」 쪽으로 맞추고, `resume` 말 겹침을 한 문장으로 밝혀 주세요.

## 15. 뒤 챕터(Ch 25·27·28·30) 인계 (그 챕터 파일은 고치지 않음)

| 챕터 | 자리 | 지금 글 | Ch 24 쪽 사실 | 할 일 |
|---|---|---|---|---|
| Ch 25(대기) | 01·02·03 `_src` b3 | 「Ch23에서 체크포인터와 thread_id가 상태를 저장하는 방법을 배웠고, Ch24에서 interrupt와 재개 사건을 확인했습니다」 | `interrupt`·`Command(resume=…)`는 참(01·02) · **스트림 사건은 0건** · 본문 말은 「사람의 답으로 이어 가기」 | Ch 25 작업 때 사건을 Ch 25가 처음 보이거나 문장을 맞춤 + `resume` 겹침 한 문장(§13-3) |
| Ch 25(대기) | 04 b8이 가리키는 01 b2 | 「한 실행에서 생긴 사건을 일곱 방식으로 관찰」 | 04 b8은 Ch 25 01 링크로 「일곱 방식으로 받아 보는 방법」만 말함(이름·그래프를 이어 쓴다는 약속 없음) | 없음 |
| Ch 27(대기) | 01 `_src` | 「Ch 24는 사람 승인을 … 다뤘습니다」 | 01 승인 지점·02·04로 참 | 없음 |
| Ch 27(대기) | 08 `_src` b3 | 「Ch 24의 사람 승인과 이 장의 permissions는 도구 실행 경계를 다룹니다」 | **부분 참** — Ch 24는 쓰기 노드 하나의 승인 지점만, 모델이 고른 도구 호출 승인·`HumanInTheLoopMiddleware` 장면 0 | Ch 27 작업 때 「도구 실행 경계」를 Ch 27이 보이거나 「부작용 앞 승인 지점」으로 맞춤 |
| Ch 28(대기) | 03 `_src` b3 | 「Ch24에서 사람이 승인해야 하는 작업 경계를 확인했습니다」 | 01로 참 | 없음 |
| Ch 30(대기) | 06 `_src` b3 | 「Ch24의 중복 실행 방지 원칙」 | 01 b4·b6·6절(`receive_then_ask` — 멱등 앞쓰기, 이어 가도 한 줄)로 참 | 없음 — **01 b4 「묻기 전에 꼭 해야 하는 쓰기는 Ch 23 06절처럼 멱등 키로 한 번만 반영되게 적습니다」·6절을 지울 때는 Ch 30 06에 인계** |
| Ch 23(완료) | 03 · 07 b8 | 「Ch 24에서 사람의 확인을 받아 멈춘 실행을 다시 움직이는 일과는 다른 장면」 · 01 슬러그 링크 | 01 3절·슬러그 그대로로 참, 04가 Ch 23 07 소재를 이어 받음 | 없음(Ch 23 파일 고치지 않음 — 공용 옛 생성기 이동과 요약 한 줄만) |

- time travel·`update_state`를 말하는 뒤 챕터 문장은 0건입니다(03 진단 §9 `grep`).

## 16. 남은 것 (전체 마감 몫 — `textbook/qa/upgrade-final-checklist.md` §2-12)

1. **옛 그림 아홉 삭제 승인**: `figures/0N-흐름.{svg,excalidraw,caption.md}`(N=1~3, 본문 참조 0, 캡션에 「반환값」·「분기」, 챕터 공개 목록 줄은 마감에서 뺌, 사본 `qa/upgrade/before/figures/`, `final-artifact-hashes.json`이 해시를 적은 기록 파일) — Part 6 옛 검사 `check_figures.py`가 `.excalidraw` 짝을 요구하는 것과 함께 정할 것.
2. **`gates-wip-*.json` 아홉 삭제 승인**(`gates-wip-01-01`·`01`·`02-02`·`02`·`03-03`·`03`·`04-04`·`04`·`ch24-after04` — `gates-after.json` 4/4로 갈음). `qa/upgrade/__pycache__/`·실습 폴더 `notebooks/__pycache__`는 만들지 않음(0).
3. **캐시·임시 삭제 승인**: 실습 폴더 `labs/part6/ch24-human-in-the-loop/.venv`(macOS 판 125MB) · `.cache/vm/venv-ch24-human-in-the-loop`(207MB) · `.cache/ch24-0N-view/`(N=1~4) · `.cache/ch24-close/`(마감 전 사본 `pre/`·확인 스크립트 `tools/`(`gpatch.py`·`syncmd.py`·`genmatch.py`·`gcheck.py`·`bandiff.sh`·`nbhash.py`·`manifest_check.py` 등)·치환 목록 `reps/`·옛 검사 결과 `oldcheck/`·`dx/`(`llm-practice.zip`을 뺀 전달 검사 사본과 결과)·로그 `log/`, 15MB) · 기기 `/tmp/ch24-prep`·`/tmp/ch24-01`~`/tmp/ch24-04`·`/tmp/ch24-close`(생성기 사본 `sandbox/`·노트북 밖 확인 `probe/p02five.py`) · 기기 세션 임시 폴더 `$TMPDIR/ch24-*`(23개 — 노트북 실행·노트북 밖 확인이 만든 폴더) · `/tmp/reviewA24`·`/tmp/reviewB24`(검토 재현 파일, B에 `__pycache__`).
4. **코드 쪽 다음 재실행 몫**(이번에는 코드 셀을 한 글자도 바꾸지 않음): 03 셀 9 `print` 인자 안 계산·식 안 숫자 `1`(B-5 — 계산 결과를 변수에) · 04 셀 5 주석 「Ch 23 01·04·06절과 03절에서」 → 「… 이 챕터 03절에서」(B-9) · 04 8절 두 셀 합치기·5절 글 옮기기(B-12, 강사 결정) · 도구 파일 머리 설명을 함수 다섯 기준으로(A-13 — 해시가 바뀌므로 `author_04.TOOLS_SHA256`·`author_03` 대조 줄·zip·묶음 검사를 함께) · 함수 다섯을 `author_01.TOOL_PARTS`로 모을지(A-10 남은 몫). 01을 다시 실행하면 §9 계약대로 zip → `check_bundle_execution.py`.
5. **Part 6 옛 검사 스크립트 넷(고치지 않음, 마감에서 돌린 결과)** — 모두 Ch 24에 닿기 전에 멈춤: `check_scope.py` Ch 21 `_src/07-create-agent-실습.html` `Missing scope`(Ch 24 04 「실습 30분」도 같은 모양 — `EXPECTED`·`SECTION_COUNTS` 기록만) · `check_figures.py` Ch 21 `01-1-….svg`의 `.excalidraw` 짝(Ch 24 새 SVG도 짝 없음) · `check_notebook_readiness.py` `assert len(reports) == 47`(Part 6 노트북 51) — **결과 파일 `notebook-readiness.json`을 먼저 씀 → 실행 전 사본으로 되돌림**(`b3d69e9c…`) · `check_visual_reports.py` `ch22-middleware`에서 멈춤(Part 6 `visual-results.json`은 쓰지 않음, Ch 24 줄은 10).
6. **`llm-practice.zip`**: Part 6 `check_delivery.py`가 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`(117행)에서 멈춤(결과 파일 안 바뀜). 사본(`.cache/ch24-close/dx/check_delivery_nollm.py`)에서 그 zip만 빼면 HTML 62 · 링크 1,160 · 누락 0 · 절 51 · 코드 셀 723 · 복습 193문항 오류 0 · SVG 146 · 비밀값 0 · 개인 경로 0 · `part6-practice.zip` `edd8c3be…` 101항목(part6 노트북 51) 통과. `llm-practice.zip` 안 Ch 24는 옛 판 — 전체 묶음 재생성 때.
7. **`textbook/_notebook/build_index.py`**(Ch 24 절 수 3·설명) — 선례대로 고치지 않음. **`textbook/part6/qa/final-artifact-hashes.json`**(Ch 24 줄 옛 판, `figures/_gen_figures.py` 옛 자리 포함) — 전체 마감 때 다시 모을지. **Part 6 공용 `visual-results.json`**: Ch 24 줄은 마감에서 10줄로 새로 모음, 다른 챕터 줄(Ch 22 등)은 옛 HTML 해시 그대로 — Part 6 마감 때 다시 모을 것.
8. **과정 요약·계약 문서(누적 문서 몫)**: Ch 24 용어(§4 — `resume` 겹침 구분 · 「승인 지점」 = 「승인 게이트」 · 「새 가지」 · 「허용 답 목록」 = 허용 목록 · 「다시 묻기」 ≠ Ch 18 「되묻기」 · 「남은 날」 ≠ 「연장 뒤 남은 날」)와 도구 파일 `approval_tools.py`(`d562c9e6…`)는 과정 요약에 아직 넣지 않음(Part 6 마감 오케스트레이터). 계약 파일은 없음.
9. **옛 기록 파일**: `qa/research.md`·`qa/verification.md`·`집필점검표.md` 머리에 「개선 전 판」 표시(내용 그대로 — `verification.md`·`집필점검표.md`는 끝에 마감 절) · `textbook/part6/qa/ch24-technical-review.md`(Part 6 쪽 옛 검토 기록, 보호 파일 — 고치지 않음) · `textbook/part6/qa/language/ch24-*`(옛 감사 기록 여섯) · `qa/upgrade/review-pack/`(검토에 쓴 마감 전 묶음 — 다시 만들지 않음, A-4의 `pack.py` 권고는 하지 않음).
10. **실습 폴더 잠금**: `pyproject.toml`·`uv.lock` 그대로(모델 패키지 없음). 바꿀 것 없음.
11. **2차 검토**: 두 검토의 「확인하지 못한 것」(한국어 감사 3단, 삽화 01-5·02-6 직접 판독, Windows·macOS 실제 실행, 학생 `.venv` 첫 셀)과 §12.

## 17. 검토 1차와 반영 (2026-09-25 마감)

- 판정: **A(01~02·공통) 중 6 · 하 8**(01 중 1·하 2 · 02 중 3·하 3 · 공통 중 2·하 3), **B(03~04·마감 몫) 중 5 · 하 12**(03 중 1·하 5 · 04 중 2·하 6 · 두 절 밖 중 2·하 1). 합 **[중] 11 · [하] 20**, [상] 0.
- **[중] 11건 모두 반영**: A-1(01 비유와 「첫 줄부터 다시 실행」 — b4 새 단락·용어 표·노트북 셀 22·그림 읽기 한정) · A-4(02 「오늘 볼 그림」 alt·읽기 — 생성기 판과 같게) · A-5(02 b6 두 단락·노트북 5절 네 문장 — 시작 수 6 ↔ 4의 뜻, 부른 수 `1·3·5·6` ↔ `1·3·6·9`, 셈 줄 = `interrupt` 앞 줄, 노트북 밖 다섯 번 `12·12·8` ↔ `7·27·3`은 b7에만) · A-6(02 b3 새 단락·용어 표·노트북 2·3절 — 허용 답 목록은 이어 쓴 말, 다시 묻기는 Ch 18 되묻기와 가름, meta 3 → 2) · **A-10(생성기 대조 줄 — 먼저 고침, §8)** · A-11/B-15(README 전체) · B-1(03 b4·b10 설치판 행 → `main.py` 2019·`_checkpoint.py` 128) · B-7(04-2·04-3 「연장 뒤 남은 날」 다시 렌더) · B-8(04 「새로 볼 것」 좁힘) · B-16(`objectives` 넷·`_build_index.py`·`continuity-guide.md` Ch 24 줄).
- **[하] 20건 가운데 19건 반영**: A-2(857 → 858) · A-3(01-5 prompt 「조각」 → 「도미노」) · A-7(02 소스로만 본 값 세 자리 한정) · A-8(02 「셀은 끝까지 · 실제 프로그램은 멈춤」) · A-9(02-4 파란 상자) · A-12(묶음 검사 다시 돌림 + handoff 「챕터 공통」 5번 문장) · A-14(= B-16) · B-2(03 문서 Fork/Replay ↔ 만든 자리 `update`/`fork`) · B-3(03-4 캡션) · B-4(03-3 공통 상자 → 두 칸 아래, 다시 렌더) · B-6(03-5 PNG를 직접 보고 글을 보이는 대로 — 다시 만들지 않음) · **B-5(검토 권고대로 기록만 — 코드 셀이라 고치지 않고, 결과 읽기에 바로잡을 사실 오류가 없어 문장도 더하지 않음, 다음 재실행 몫)** · B-9(04 b4 표 「이 챕터 03절」·셀 4 「새로 배우는 이름」·**셀 6 결과 읽기에 「가져오기 줄 주석의 「03절」도 Ch 23이 아니라 이 챕터 03절입니다」 한 문장** — 셀 5 주석 자체는 다음 재실행) · B-10(04-2 도식 읽기 두 문장) · B-11(04 b3 Ch 23 07) · B-12(04 진단 「20~32」 뺌) · B-13(04-4 「색과 절 짝짓지 않음」) · B-14(04-figures 절차 메모) · B-17(= A-10).
- **반영하지 않은 것과 까닭(1건)**: **A-13**(도구 파일 머리 설명을 함수 다섯 기준으로) — 챕터 리드 결정으로 도구 파일 해시 `d562c9e6…`를 고정(03·04 생성기 대조 줄·zip·묶음 검사가 이 판에 기댐). 머리 설명은 틀린 말이 아니라 모자란 말이고, 함수마다 위 주석에 출처가 있으며 README가 함수 다섯의 배운 절·가져오는 절을 적음. 다음에 도구 파일을 다시 쓸 때 고침. **코드 쪽이 남은 둘**(B-5 03 셀 9 · B-9 04 셀 5 주석)은 코드 셀을 한 글자도 바꾸지 않는다는 결정대로 다음 재실행 몫으로 적음. 뒤 챕터 파일 수정(Ch 25 01~03 「재개 사건」·Ch 27 08 「도구 실행 경계」 — §15) · 삽화 다시 만들기(B-6 — 글만) · 노트북 다시 실행은 과제 결정대로 하지 않음. A-4의 `pack.py`로 검토 묶음 다시 만들기도 하지 않음(Ch 23 선례 — 마감 전 묶음 보존).
- **노트북 해시 전후**(`code_sha256` / `outputs_sha256`, 앞 12자 — 모두 같음): 01 `7187f7a39f3f`/`fbaaa8908bd1` · 02 `ead91c80882f`/`b3385367b194` · 03 `12b29f1517d5`/`aab2462d34f9` · 04 `c4722b0d084f`/`2aeaebb25174`. `executed_at` 넷 모두 같음, `metadata.verification`과 다시 계산한 값이 같음. 파일 해시만 바뀜(마크다운): §10 첫 줄.
- 고친 방법: `.cache/ch24-close/tools/gpatch.py`(생성기 문자열과 노트북 마크다운을 함께 — 노트북 코드 셀에 옛 글이 있거나 생성기에서 한 번이 아니면 멈춤) → `author_NN.py --src-only`(·`--figures`) → `genmatch.py`(셀 62·59·59·59 · `_src` 4/4 같음) → `.mmd` 고친 셋만 `render_mermaid.py --only … --force` → `run_section.sh … NN --no-exec` 네 번. 02 셀 1은 `syncmd.py`(생성기 셀 글로, 첨부 그대로). 마감이 더한 문장의 참 금지어 0, 게이트 G6 0.
- 검사: `upgrade_gates.py … --label after` **4/4 PASS, G1~G7 0** · AST 따로 금지 문법 0(허용 표시 — 02 `while True` 하나·`try` 둘·키워드 없는 `sorted` 넷) · `verify.py --chapter` **PASS 4 sections / 112 code cells (max 12 lines)** · 빌드 HTML 다섯 `{{`·`[[` **0건** · `visual.cjs` **10행 PASS** · Part 6 `check_bundle_execution.py` **PASS**(Ch 24 01·Ch 28 01) · Part 6 `check_delivery.py`는 `llm-practice.zip` Part 1 Stale에서 멈춤(그 zip을 뺀 대조 통과, §16 6번) · 옛 검사 넷 Ch 24 전에 멈춤(§16 5번) · 보호 파일 131개 102 같음 · 27 의도한 변경 · 2 옮김.
- 절차 메모(B-14): 04 그림 설계표는 첫 렌더 뒤 PNG를 보고 옮겨 적었습니다(규격 §5-2 「그리기 전에」와 차례가 다름 — 결과물 영향 없음).
