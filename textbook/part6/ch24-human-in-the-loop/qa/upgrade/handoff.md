# Ch 24 Human-in-the-Loop와 Time Travel — 절 사이 인계 (handoff)

- 읽는 순서: 과정 요약 → Ch 23 `chapter-summary.md` → 준비 조사 `qa/upgrade/chapter-lead-notes.md` → **이 파일** → 앞 절 `NN-diagnosis.md`·완료본(`_src`·노트북·생성기).
- 01절 완료 2026-09-25(게이트 0, 새 커널 두 번 28/28 같음, 키 없는 묶음 모양 실행 PASS). 세부 값은 `01-diagnosis.md`.
- 02절 완료 2026-09-25(게이트 27 → 0, 새 커널 두 번 28/28 같음, 모델 요청 0, 도구 파일 그대로). 세부 값은 `02-diagnosis.md`.
- 03절 완료 2026-09-25(게이트 33 → 0, 새 커널 두 번 28/28 같음, 모델 요청 0, 도구 파일에 함수 둘 — `print_history`·`find_before`). 세부 값은 `03-diagnosis.md`. **본문 마지막 절** — 실습 절 04는 아래 「§03 → 실습(04)」.
- 04절(실습 절, 새로 만듦) 완료 2026-09-25(게이트 0, 새 커널 두 번 28/28 같음, 모델 요청 0, 도구 파일 그대로). 세부 값은 `04-diagnosis.md`, 챕터 마감 담당에게는 맨 아래 「실습 → 챕터 검토」.
- **챕터 마감 2026-09-25**(검토 1차 반영 — [중] 11 · [하] 19/20, 노트북 다시 실행 0, 게이트 4/4, 묶음 실행 검사 PASS). 맨 아래 「검토 반영과 챕터 마감 (2026-09-25)」, 전체 기록은 `chapter-summary.md`.
- **전체 마감 2026-09-30 — 도구 파일 머리 줄**: `approval_tools.py` 머리 설명 1행(「앞 챕터와 이 챕터 앞 절에서 배운 …」)·6행(함수 다섯 출처)만 고침 — `d562c9e6…` → **`295bfaf632832bcdd86283c00c09632a0f228f4a5921bb5ec53e4fa3fe9a1f60`**(함수 본문·노트북 해시 같음, 생성기 `author_01.TOOLS_HEAD`·`author_04.TOOLS_SHA256`). 기록 `textbook/qa/final-close-log.md` 2단계·`chapter-summary.md` §8 끝.

## 챕터 공통 (01절에서 정한 것)

### 챕터 리드 결정 (그대로 이어 지키세요)

1. **모델은 부르지 않습니다(M1)** — Ch 23과 같은 까닭(잠금에 모델 패키지 없음 · 결정적 · 묶음 실행 검사가 01을 키 없이 돌림). 사람의 답은 코드가 넣는 값(`Command(resume=…)`의 값)이라는 문장을 노트북 준비물·`_src` b5에(01 판: 「사람의 답은 우리가 셀에 적어 넣는 값(`"approve"`·`"reject"`)입니다. 실제 서비스라면 화면에서 사람이 고른 값을 같은 자리에 넣습니다.」). 준비물에 「모델 요청은 0번이고, API 키 없이 실행합니다」. 키 셀·모델 셀·`dotenv` 가져오기 없음.
2. **파일 쓰기는 임시 폴더에만** — 준비 셀 셋(설치 → 가져오기 → 임시 폴더). 임시 폴더 셀은 Ch 23 01 셀에서 앞머리만 `ch24-NN-`, 주석 선례는 「(Ch 23 01절과 같은 모양)」(01 생성기 `FOLDER` — 02는 `author_01.FOLDER.replace("ch24-01-", "ch24-02-")`로 만들고 `assert`). 도구 파일을 가져오는 절은 **작업 위치를 옮기기 전에** 가져옴. **지우는 줄(`unlink`·`os.remove`) 0** — 장면마다 다른 파일 이름을 새 임시 폴더에 씀. 파일을 쓰지 않는 절(메모리 체크포인터만)도 챕터 모양대로 임시 폴더 셀을 두고 마지막에 `[]`로 확인할 수 있음.
3. **01 paired**(끝남): Before `charge_then_ask`(적고 나서 묻기) = 거절에도 같은 키 두 줄(빨강) ↔ After `ask_then_charge`(묻고 나서 승인일 때만 적기) = 거절 0줄·승인 한 줄. 6절 `receive_then_ask` = `append_key_once`로 묻기 전 접수 기록을 멱등하게 → 거절로 이어 가도 한 줄(Ch 23 06과 잇는 문장 · Ch 30 06 「중복 실행 방지 원칙」의 실행 근거).
4. **도구 파일 B안 `notebooks/approval_tools.py`**(01이 만듦 — §아래 「도구 파일」).
5. **묶음 실행 검사 계약**: 01은 모델·키·새 패키지 없이(잠금에 있는 것만, `dotenv`도 없이) 새 커널로 끝까지 돌아야 함. 01 `code_sha256` **`7187f7a39f3fbd146120412daf4d9675ecf132703117570348b3b570744595ab`**(28셀). **01을 다시 실행하거나 코드 셀을 고치면 이 값이 바뀜** → 마감이 zip을 다시 만든 뒤 `check_bundle_execution.py`로 `bundle-execution.json`을 새로 씀(01절 당시 zip·기록은 옛 01 `718171990c5d…` — 04절이 zip을 새로 만들었고, 마감이 zip을 한 번 더 만든 뒤 `check_bundle_execution.py`로 기록을 새로 씀 — 아래 「검토 반영과 챕터 마감」, 검토 A-12). 01에 모델·키 셀을 넣지 말 것.
6. **용어**(아래 표). 「승인 게이트」 = Ch 17 02 「승인 지점」(제목의 「게이트」는 제목에만, Ch 18 01 「게이트」와 다름을 01 b2·노트북 1절에 한 문장). fork(03 몫)는 「분기」 금지 · 「갈래」는 Ch 13 조건부 엣지 뜻이라 쓰지 않고 **「새 가지」** 같은 쉬운 말(03이 확정).
7. **공용 옛 생성기** `textbook/part6/ch23-persistence/qa/author_ch23_ch24.py` 첫머리 `raise SystemExit`(01이 넣음, `3fc72ded…`) · `figures/_gen_figures.py` 맨 위 `raise SystemExit`(`2a015c6a…`). 옮기기는 마감 몫.
8. **슬러그는 바꾸지 않음**(01은 Ch 23 07이 링크, 02·03도 바꾸지 않는 쪽).
9. **문법 범위**(아래 「허용 문법 범위」).
10. **비유 계열 「도미노 줄과 비워 둔 자리」**(01이 엶, 아래).
11. **준비 셀은 과정 표준** — 설치 `%pip` 줄은 잠금 판 번호까지(01 판 `"langgraph==1.2.11" "langgraph-checkpoint==4.2.0"`), import, 임시 폴더, 도구 파일을 쓰면 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 … 작업 위치를 옮기기 전에 가져왔습니다」 + 「교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어 …」.

### 준비 셀 (01 판 — 뒤 절은 이 모양을 그대로)

- 설치: `nbkit.install_source(["langgraph==1.2.11", "langgraph-checkpoint==4.2.0"])` → 출력 `langgraph: 1.2.11`·`langgraph-checkpoint: 4.2.0` → 결과 읽기에 실행일(`RUN_DATE`).
- 가져오기(01 판): `from typing_extensions import TypedDict` · `from langgraph.graph import StateGraph, START, END` · `from langgraph.checkpoint.memory import InMemorySaver` · `from langgraph.types import Command, interrupt` · `from approval_tools import append_key, append_key_once, read_record` + 가져온 이름을 `print`. 02·03은 쓰는 이름만(도구 파일에서 가져올 것이 없으면 그 줄을 빼고 고정 문장도 뺌).
- 임시 폴더: `tempfile.mkdtemp(prefix="ch24-NN-")` → `os.chdir` → `print("임시 폴더 이름에 ch24-NN-이 들어 있는가:", …)`·`print("현재 작업 폴더의 파일:", os.listdir())`(위치는 출력하지 않음).

### 01이 푼 문장 (뒤 절은 되풀이하지 말고 「01절에서 본 것처럼」으로)

- 멈춤 표시의 세 문장 정의·질문 값·사람의 답으로 이어 가기(아래 표) · Ch 23 03 「스레드 재개」·04·06 worker 단계 `resume`과 다른 장면이라는 문장(01 b3 셋째 단락·노트북 3절) · 「이어 갈 때 노드는 멈춘 줄이 아니라 첫 줄부터 다시 실행」(설치판 `types.py` 864행·공식 문서, 01 노트북 3절 시작 줄 두 번) · 「멈춤 표시를 쓰려면 체크포인터와 스레드 이름」(공식 문서·`types.py` 870~871행) · 결과 키 `__interrupt__`·항목 `Interrupt`의 `.value`·`get_state(config).tasks[0].interrupts[0].value` · 체크포인트 수(노드 하나짜리 그래프: 멈춘 동안 2 → 이어 간 뒤 3) · `try`/`except`로 감싸지 않기(노트북 밖 확인만, 01 b7) · 질문 값은 JSON으로 적을 수 있는 값만(공식 문서, 01은 딕셔너리만 넣음).

### 도구 파일 — `labs/part6/ch24-human-in-the-loop/notebooks/approval_tools.py` (01이 만듦)

- 해시 **`b40aab98ae6ddd87cb4a0107403193c33d9978c436f1a20cf493873458950a93`**, 함수 셋(Ch 23 `checkpoint_tools.py` `a850b2cd…`의 같은 이름 함수를 **본문 글자 그대로** — 01 생성기 `check_same_as_ch23()`가 문자열·AST 대조): `read_record(record_name)`(Ch 23 04 — 설명 주석 「노드 이름」 그대로, 머리 독스트링에 「이 챕터에서는 주문 키를 읽습니다」) · `append_key(record_name, order_key)` → `"적음"` · `append_key_once(record_name, order_key)` → `"건너뜀"` 또는 `append_key`(Ch 23 06). import `os`만(SQLite·langgraph 없음 — 이 챕터 잠금에 SQLite 체크포인터가 없음).
- **파일을 쓰는 생성기는 01 `author_01.py`**(`TOOLS`). 뒤 절이 함수를 더하면 01 생성기의 `TOOL_PARTS`를 고치지 말고, 그 절 생성기가 `author_01.TOOLS` + 새 함수로 파일을 다시 쓰되 **01 함수 셋은 글자 그대로**(Ch 23 06 → 07 선례: 07 생성기가 `author_06.TOOLS`와 해시 대조). 더하는 후보: Ch 23 01 노트북 함수 `print_history(history)`(03 기록 출력 — 도구 파일로 옮길 때 `# Ch 23 01절에서 배웠습니다 — 01절 노트북 8절의 같은 이름 함수를 옮겼습니다`).
- **묶음 목록에 올라 있음**: 챕터 `qa/public-files.json`(14줄, `c629078f…`) · `textbook/part6/public-files.json`(`collect_public_files.py`로 다시 모음, `a7741594…`). 도구 파일을 고치면 해시만 바뀌고 목록은 그대로.
- 가져오는 절: **01**(셋 다). 02·03이 가져오면 그 절 준비 셀에 고정 세 문장.
- 실행할 때 `PYTHONDONTWRITEBYTECODE=1`(실습 폴더 `notebooks/__pycache__`를 만들지 않게 — 연결 폴더라 지울 수 없음), 생성기는 `python3 -B`(`qa/upgrade/__pycache__`를 만들지 않게).

### 용어 (01절에서 정한 것 — 뒤 절은 그대로 이어 씁니다)

| 말 | 뜻(01 정의) | 코드에서 | 비고 |
|---|---|---|---|
| **멈춤 표시(interrupt)** | 노드가 그 자리에서 그래프를 멈추고, 사람에게 보일 값을 남기는 일 | 노드 안 `interrupt(질문 값)` · 결과 키 `__interrupt__`의 항목 `Interrupt` | 함수 이름을 말할 때는 「함수 `interrupt`」 |
| **질문 값** | 멈춤 표시와 함께 사람에게 보일 값 | `{"order_key": "order-2401", "question": "결제할까요?"}` · `.value` | 「payload」 금지 |
| **사람의 답으로 이어 가기** | 멈춘 스레드에 사람의 답을 넘겨, 멈춘 노드부터 실행을 이어 가는 일 | `invoke(Command(resume=답), config)` — `resume`의 값이 노드 안 `interrupt`가 내놓는 값 | Ch 23 03 「스레드 재개」·04·06 worker 단계 `resume`과 **다른 장면**(01 b3·노트북 3절). 본문에서 「재개」 쓰지 않음(제목 02 「재개」는 제목에만) |
| (일반 말) 사람의 답 | `Command(resume=…)`에 넣는 값(01: `"approve"`·`"reject"`) | — | 셀에 적은 값임을 밝힘 |
| (이어 씀) 승인 지점 | Ch 17 02 정의 그대로 — 부작용이 생기는 단계 앞에서 사람이 확인하는 자리 | — | 제목 「승인 게이트」 = 이 말 |
| (이어 씀) 사람 확인 · 사람 확인 값 | Ch 17 03(멈추고 넘김, 이어 가기 없음) · Ch 19 06(참/거짓) | — | 01 b3에서 견줌 |
| (이어 씀) 체크포인터·체크포인트·스레드·멱등성·멱등 키·부작용·설계 객체·상태 형식·칸 | Ch 23·Ch 17 02·Ch 13 | — | — |
| (03 몫) fork | — | — | 「분기」·「갈래」 금지, **「새 가지」** 같은 쉬운 말(03이 확정) |

- 새 용어 meta: 01 = 3(멈춤 표시 · 질문 값 · 사람의 답으로 이어 가기). 02·03은 3씩(옛 목록 02 `Command`·`resume`·재개 값 → 01이 `Command(resume=…)`을 이미 정했으므로 02는 다른 말로 셋 — 예: 허용 답 목록·다시 묻기·오류 칸 등, 03은 체크포인트 목록 고르기·값 바꿔 다시 실행·새 가지 등 — 각 절이 정함).
- **금지어**(01 설명·주석·캡션·`.mmd`·README·도구 파일 0건 — 제목·슬러그·코드 백틱 말고): 「반환」·「경로」·「런타임」·「payload」·「snapshot」·「스냅샷」·「스키마」·「검증」·「포인터」(단독)·「소비」·「분기」·「지연」·「추정」·「직렬화」·「HITL」·「재시작」·「재실행」·「재개」(Ch 23 03 「스레드 재개」를 가리킬 때 말고)·「게이트」(제목과 그 풀이·Ch 18 01 구분 문장 말고)·「갈래」(Ch 13 뜻 말고)·「중단」·「인터럽트」·**「조각」(Ch 5 토큰 전용 — 01 첫 판 도미노 비유에서 걸려 「도미노」로 고침)** + Ch 23 목록(「지시」·「trace」·「superstep」·「병렬」·「채널」·「식별자」·「레코드」·「로그」(「프로그램」 안 글자 말고)·「트랜잭션」·「보장」·「정확히 한 번」·「측정」·「필드」·「사전」·「동시」·「순차」·「돌려줍니다」류·「쉽게·간단히·당연히」·「개선 전」·「강사 시연」) + 「한 겹 더」. 01 검사 스크립트 `/tmp/ch24-01/tools/ban24.py`(Ch 23 `ban_check.py` + 위 말).

### 허용 문법 범위 (01절 AST 확인 — `/tmp/ch24-01/tools/extra_check.py`, Ch 23 마감 판 복사)

- 쓰는 것: 칸만 적은 `TypedDict` 상태 형식(**칸 구성이 바뀌면 이름도 새로** — 01 `ApprovalState`(칸 `order_key`·`record_name`·`answer`, 규칙 없음), 02·03은 다른 이름) · 노드 함수(힌트 없음, 본문 8줄 이하) · 노드 안 `print`(노드가 몇 번 시작하는지 보이기 — 01 선례) · 여러 줄 `if` · `for` · 목록 `append`·`count` · `os.path.exists`·`os.listdir`·키워드 없는 `sorted` · `assert`·`assert not`(우리 코드가 정하는 값에만).
- 쓰지 않는 것(01 0건): f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`key=`·`reverse=`·`set`(리터럴 포함)·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·튜플 풀기·별표 풀기·`{**…}`·**`while True`**·숫자 밑줄 `10_000`·세미콜론·`isinstance`·데코레이터·클래스(상태 형식 말고)·`try`·`Path`·`unlink`·모델. **`Interrupt.id`·체크포인트 ID·시각은 출력하지 않음**(실행마다 바뀜). `len(list(…))` 같은 두 겹 호출은 변수로 풂.
- **한 자리 예외(마감 2026-09-25, 챕터 리드 결정 · 강사 확인 대상)**: 위 「쓰지 않는 것」의 `while True`는 **02절 4절 「권하지 않는 모양」 셀 `ask_in_loop` 하나에만** 기본 경로에서 씁니다(공식 문서가 권하지 않는 모양을 한 번 실행해 부른 횟수를 견줌 — 셀 첫 줄 주석·소제목·b7에 「권하지 않는 모양」). 규격 §2-2 L1이 `while`을 허용하고 G1도 세지 않지만, 이 챕터의 허용 목록에서는 이 한 자리만 예외입니다. 01·03·04절과 도구 파일은 0건. `try`/`except`도 02절 6절 노드 밖 `invoke` 감싸기 둘뿐입니다.
- 셀 모양: 준비 셀이 아닌 셀 10줄 이하(01 최대 9) · 함수 본문 8줄 이하(01 최대 8) · 셀당 정의 하나 · 첫 줄 주석이 그 셀이 하는 일 · 정의 셀 결과 읽기 「정의 셀이라 출력이 없습니다」.

### 색 (01절 Mermaid 4장)

- 넣은 값·사람의 답 **초록(tool)** · 우리 노드와 부른 줄 **파랑(flow)** · 출력으로 확인한 값 **노랑(measure)** · 둘 이상 장면에서 모두 확인한 공통 사실·라이브러리 **회색(클래스 없음)** · **보라 0**(모델 없음) · **빨강은 paired Before 결함 결과만**(01-3 「거절인데 같은 키 두 줄」·01-4 `charge_then_ask` 상자). 02·03은 experiment라 **빨강 0**(받아 출력한 오류는 노랑 — 규격 §5-3).
- 모양: 넷 이상 한 줄은 `flowchart TB` · 나란한 장면·한꺼번에 읽은 값은 `~~~` · 실제 차례는 `-->` · 코드가 고르는 갈래는 점선 · 라벨은 `<br>`로 미리 나눔(01 첫 렌더에서 셋이 저절로 꺾임) · 개수는 한글 · 라벨 숫자는 출력에 있는 것만(01은 `2401` 하나) · 폭 868 이하(01 최대 576).

### 비유 계열 — 「도미노 줄과 비워 둔 자리」 (01절이 엶, 챕터 리드 결정 10)

- 빈자리 = 멈춤 표시 · 빈자리에 도미노를 놓는 일 = 사람의 답 · 넘어진 컵 = 되돌리기 어려운 쓰기(결제 기록) · 빈자리 앞/뒤에 둔 컵 = 적고 나서 묻기/묻고 나서 적기.
- 01-5 삽화: 도미노 두 줄, 줄마다 빈자리 하나, 위 줄 컵은 빈자리 앞에서 쓰러짐(`charge_then_ask`) · 아래 줄 컵은 빈자리 뒤에 섬(`ask_then_charge`). 도미노 개수·탁자 다리는 짝짓지 않음.
- 02 후보: 빈자리에 맞지 않는 모양의 물건이 놓여 줄이 그대로 멈춤 ↔ 맞는 도미노가 놓여 이어짐(허용하지 않는 답은 다시 묻기) — **「조각」이라는 말은 쓰지 않음**. 03 후보: 넘어진 원래 줄은 그대로, 가운데 한 자리에서 다른 방향으로 새로 세운 줄(새 가지 — Ch 13 갈림길로 보이지 않게, Ch 23 사진 한 장 = 체크포인트 한 문장으로 이음).
- 금지 소품: 앞 챕터 도장·쟁반·서랍·바구니·저울·울타리·발자국·공구판·승강 상자·세탁기·체스판·즉석사진·기보·리본. 사람·손·화살표·화면·시계·글자·숫자 없음. 스타일 문구는 규격 §5-4 그대로, `nano_banana_pro` 16:9 2k `use_unlim:false` count 1, 절당 1장·재생성 1회까지.

### 파일 쓰기·시간·비용·실행

- 모델 요청 0 · 비용 0 · 01 삽화 2크레딧(job `fb67df97-…`, 거래 13:52:58Z). 걸린 시간은 재지 않음 — 준비물의 「2초 안에」는 셀 실행 기록(A 13:50:55.28~56.31Z)으로 적은 값.
- 새 커널 두 번: A `PYTHONDONTWRITEBYTECODE=1 env -u OPENAI_API_KEY bash run_section.sh … NN` · B 사본 `/tmp/ch24-NN/B/`에 노트북·도구 파일 → `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch24-human-in-the-loop UV_NO_SYNC=1 PYTHONPATH=/tmp/ch24-NN/B uv run --project labs/part6/ch24-human-in-the-loop --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip --with python-dotenv==1.2.3 python textbook/_notebook/execute.py …` → `cmpout.py`(셀별 글 대조). **실습 폴더 안에서 먼저 실패하면 `.failure.json`이 남고 지울 수 없음** → 첫 실행은 `/tmp` 사본으로 먼저(01 선례).
- **`uv run --project labs/…`를 환경 변수 셋(`UV_CACHE_DIR`·`UV_PROJECT_ENVIRONMENT`·`UV_NO_SYNC`) 없이 부르지 말 것** — 실습 폴더 `.venv`(macOS 판)를 새로 만들려다 `.lock` 지우기에서 멈춤(01에서 한 번, 바뀐 파일 0).

### 완료·대기 챕터 문장 (01에서 확인 — `01-diagnosis.md` §10)

- 참: Ch 23 07 b8(01 슬러그·장면) · Ch 23 03 「Ch 24에서 사람의 확인을 받아 멈춘 실행을 다시 움직이는 일과는 다른 장면」 · Ch 17 02·03 · Ch 19 06 · Ch 13 06.
- 대기(고치지 않음): Ch 30 06 「Ch24의 중복 실행 방지 원칙」(01 b4·b6·6절로 참 — **01 b4 「묻기 전에 꼭 해야 하는 쓰기는 Ch 23 06절처럼 멱등 키로 한 번만 반영되게 적습니다」를 지울 때는 인계**) · Ch 25 01~03 b3 「interrupt와 재개 사건」(사건은 Ch 25 몫) · Ch 27 08 「도구 실행 경계」(부분 참 그대로) · Ch 28 03(참).

## §01 → §02

**02절 주제**: 「Command resume으로 실행 재개」(**experiment**). 옛 판(`before/notebooks/02-…ipynb`·`before/_src/02-*.html`): 노드 `review` 안 `while True` + `interrupt({**prompt, "error": …})` 다시 묻기 · 허용 답 집합 `{"approve", "reject"}` · f-string `f"허용하지 않는 값: {decision}"` · 요청 `publish-local`·스레드 `review-2402` · 답 `maybe` → 둘째 질문에 `error` · `approve` → `decision` 저장·`next ()` · `history count: 3`(호출 두 겹 `len(list(…))`) · 20줄 셀.

1. **01절이 남긴 자리**: `_src` b8·노트북 정리 끝 「02절에서는 사람의 답을 검사해, 허용하지 않는 값이면 다시 묻는 방법을 봅니다」 · b4 「비교와 경계」 「받은 답을 검사해, 허용하지 않는 값이면 다시 묻는 일은 02절에서 다룹니다」 · b7 「이 절의 After 노드는 `approve`가 아닌 답을 모두 쓰지 않는 쪽으로 다룹니다. `approve`·`reject` 말고 다른 글은 이번에 넣어 보지 않았습니다」 → **02가 허용하지 않는 답(예: `maybe`)을 넣고, 알려 주고 다시 묻는 장면**을 보여야 참.
2. **공식 문서 규칙 충돌(준비 노트 §2 02·§5-2, 2026-09-25 확인)**: 「Do not loop `interrupt` calls using logic that isn't deterministic across executions, including `while True` validation loops. Use a conditional edge instead.」 · 권장 모양 = 노드에서 `interrupt()`를 **한 번만** 부르고 오류를 상태 칸에 담아 **조건부 엣지(Ch 13 03 `add_conditional_edges`·`path_map`)로 되돌아가기**. 옛 판 `while True`는 과정 금지 문법(규격 §2-3 한 줄 목록 밖이지만 인계 결정 9 「`while True` 빼기」)이기도 함 → **조건부 엣지 판으로 바꾸는 쪽을 권함**(선택지 (나) `while True` 판을 실험 한 칸으로 견주기는 금지 문법과 충돌하므로 설치판·노트북 밖 확인 수치로만 b7에).
3. **설치판 관찰(준비 노트 §5-2, e2·e5 — 02가 다시 확인할 것)**: `while True` 판은 다시 묻기 한 번마다 노드가 처음부터 돌며 앞선 답을 차례로 다시 받음 — 노드 호출 1 → 2 → 3 → 4, **`interrupt` 호출 누적 1 → 3 → 6 → 9**, 체크포인트는 멈춰 있는 동안 **2 그대로**(다시 물어도 늘지 않음), `approve` 뒤 3. **조건부 엣지 판**은 노드 호출 1 → 3 → 4, **체크포인트 2 → 3 → 4**, 마지막 `next ()`, 둘째 질문 `{'request': 'publish', 'allowed': ['approve', 'reject'], 'error': '허용하지 않는 값: maybe'}`(f-string 대신 글 `+`). 01 노트북처럼 **노드 안 `print`로 노드가 몇 번 시작하는지** 셀 출력에 보이면 「이어 갈 때 처음부터 다시 실행」(01 3절)과 바로 이어짐.
4. **실패 장면 후보(결정적, 받아 출력 → 노랑)**: (가) 체크포인터 없이 컴파일한 그래프 — 첫 `invoke`는 오류 없이 `__interrupt__`를 냄, `Command(resume=…)`에서 `RuntimeError: Cannot use Command(resume=...) without checkpointer`(01 b4·노트북 2절이 「체크포인터가 있어야」를 문서·소스로만 말했으므로 실행 근거가 됨) · (나) **다른 스레드로 답 보내기** — 노드가 빈 상태로 실행돼 `KeyError: 'request'`(오류 글이 친절하지 않음, 옛 b5 「새 ID로 resume을 보내면 기존 interrupt에 값이 전달되지 않습니다」의 실행판) · (다) 끝난 스레드에 다시 보내기 → 오류 없이 상태 그대로 · (라) 같은 단계 두 노드가 함께 멈춘 뒤 값 하나로 이어 가기 → `RuntimeError: When there are multiple pending interrupts, you must specify the interrupt id when resuming.` → `Command(resume={id: 값, …})`(아이디를 딕셔너리 키로 — 출력하지 않고 수·값만). 하나~둘을 고르고, `try`/`except 오류이름 as error`(Ch 2 05 모양)로 받아 `type(error).__name__`·오류 글 앞부분만 출력.
5. **말**: 제목 「Command」·「resume」·「재개」는 제목에만(강사 확인). 본문은 01 용어 「사람의 답으로 이어 가기」·「질문 값」·「멈춤 표시」를 그대로, 「재개」 쓰지 않음. 옛 판 금지어 「반환」 9·「검증」 8(→「검사」)·「payload」 5·「런타임」 2·「스키마」 2·「포인터」(단독 — 「같은 `thread_id`는 기다리던 실행을 찾는 포인터」)·「정확히」·「소비」·「분기」·「경로」 모두 뺌. 허용 답 목록은 **목록**(`["approve", "reject"]`)으로 — 집합 리터럴 금지, `in` 검사.
6. **상태 형식**: 칸이 01과 다르면 새 이름(예 `ReviewState` — 칸 `request`·`answer`·`error`처럼). 01 `ApprovalState`를 그대로 쓰면 이름도 그대로(칸이 같을 때만). 오류 칸은 규칙 없는 글 칸(덮어쓰기)으로.
7. **이어 쓸 이름과 값**: 01 준비 셀 셋(임시 폴더 앞머리 `ch24-02-`) · 01 질문 값 모양 `{"order_key": …, "question": …}`을 잇거나 옛 요청 `publish-local`/스레드 `review-2402` · 주문 키 `order-2401`을 이어 쓸지(02 몫). 도구 파일 함수는 02가 파일을 쓰지 않으면 가져오지 않음(가져오면 고정 세 문장).
8. **체크포인트 수·호출 횟수는 우리 그래프 값** — 노드 수가 다른 그래프에 01의 2·3을 그대로 쓰지 말 것. 01은 **노드 하나짜리 그래프에서 멈춘 동안 2 → 이어 간 뒤 3**.
9. **셀 모양과 그림**: 01 코드 셀 28(준비 셋), 비준비 셀 최대 9줄, 함수 본문 최대 8줄. 옛 c4 20줄·집합·풀기·`while True`·f-string·힌트, c8 호출 두 겹 고침. 그림 번호 `02-1`부터, 설계표 `qa/upgrade/02-figures.md` 먼저. experiment라 **빨강 0**(받은 오류 노랑), 조건부 엣지로 되돌아가는 갈래는 점선, 조건 함수는 노드와 다른 모양·색(규격 §5-3 Ch 13 03-1). 옛 `figures/02-흐름.*` 그대로.
10. **비유와 삽화**: 위 「비유 계열」 02 후보(빈자리에 맞지 않는 물건 ↔ 맞는 도미노). 도미노 개수를 모델이 틀리기 쉬움 — 셀 수 있는 적은 수로, 「조각」이라는 말 없이.
11. **아직 가르치지 않은 것**(02가 설명 없이 전제하면 안 되는 것): 한 노드 안 `interrupt` 여러 번(차례로 맞춤 — `types.py` 866~868행, 02가 쓰면 처음 가르침) · 아이디 딕셔너리 이어 가기 · `update_state`·`get_state_history`로 지난 체크포인트 고르기·다시 실행(03) · `stream`(Ch 25) · 정적 중단점 `interrupt_before`/`after`(문서가 사람 확인에는 권하지 않음 — 안 씀) · 모델·도구 호출 승인(`HumanInTheLoopMiddleware` 없음). 01은 `Interrupt.id`를 **출력하지 않았음** — 02도 수·값만.
12. **02절 작업 순서와 챕터 밖 확인**: `before/`에 02 사본이 이미 있음 → `qa/upgrade/author_02.py`(01 생성기를 본으로 — `FOLDER`·`html_text()`·`table_html()`·`illustration_block()`·`mermaid_block()`를 `import author_01`로 가져와 쓰면 `python3 -B`로 `__pycache__`를 막을 것, experiment라 `{{notebook:slug}}` 하나 · `lesson_part` 없음) → 첫 실행 전 `upgrade_gates.py … --label wip-02 --section 02`(G1·G2) → `/tmp/ch24-02/` 사본으로 먼저 `execute.py`(실패 시 `.failure.json`이 실습 폴더에 남지 않게) → `run_section.sh … 02`(A) → 사본으로 B → 셀별 대조 → `.mmd`·삽화 → `--no-exec` 게이트 0 → AST·금지어(`/tmp/ch24-01/tools/` 복사) → `pack.py` → `02-diagnosis.md` → 이 파일 `§02 → §03` → 점검표·검증 행 → 보호 파일 해시(`manifest-changes.md`에 이어 적기). **02는 묶음 실행 검사 대상이 아님**(01만). 슬러그 02는 들어오는 링크 0(Part 목차는 `_build_index.py`가 다시 만듦) — 바꾸지 않는 쪽.

## §02 → §03

**03절 주제**: 「상태 기록과 다른 분기 재실행」(**experiment**, 본문 마지막 절 — 실습 절 04는 마감 몫). 옛 판(`before/notebooks/03-…ipynb`·`before/_src/03-*.html`): 노드 `quote`·`discount`(한 셀에 함수 둘 · 힌트 · f-string 계산 `f"discount:{state['rate']}"`) · `10_000` · `int(… * (1 - rate))` · 기록에서 `next(item for …)`로 `next == ("discount",)` 체크포인트 고르기 · `update_state(…, {"rate": 0.2})` → `invoke(None, fork_config)` → 원본 `9000`·새 실행 `8000`·`trace ['quote', 'discount:0.2']` · 「분기」 본문 20·노트북 8.

1. **02절이 남긴 자리**: `_src` b8·노트북 정리 끝 「03절에서는 지난 체크포인트를 골라 값을 바꾸고, 그 자리부터 다시 실행해 봅니다」 · b4 「비교와 경계」 「지난 체크포인트로 돌아가 다시 실행하는 일은 03절에서 다룹니다」 → 03이 이 장면을 보여야 참.
2. **기록에서 고르고 값을 바꿔 다시 실행(준비 노트 e3, 03이 다시 확인)**: `get_state_history`는 최신 것부터(Ch 23 01), 스레드의 모든 줄이 한 목록에 섞임 → 고를 때는 `for` + `break`(`next` 금지), 칸은 Ch 23 01 모양 `metadata["step"]`·`metadata["source"]`(`.get` 금지). `update_state(고른 설정, 값)`은 **원천 `update` 체크포인트**(단계 = 고른 자리 + 1, 부모 = 고른 자리)를 만들고 그 설정을 내놓음 → `invoke(None, 그 설정)`으로 뒤 노드만 다시 실행(앞 노드 호출 수 그대로 — 02처럼 노드가 목록에 적는 방식으로 셀 수 있음). **스레드 설정으로 `get_state`하면 가장 최근 줄(새 가지)**이 나오고, 원본 값은 따로 보관한 설정으로만 읽힘.
3. **값을 바꾸지 않고 옛 설정으로 다시 실행해도 새 가지가 생김**: `invoke(None, 옛 체크포인트 설정)` → 설치판이 원천 **`fork`** 체크포인트를 만들고 뒤 노드를 **다시 실행**(`langgraph/pregel/_loop.py` **952~971행** — 02가 행 번호 확인, 주석 「save a fork checkpoint so the replayed execution creates a new branch」, `update_state`로 만든 `update`·`fork` 원천에서는 건너뜀). 공식 문서 Time Travel 「Replay re-executes nodes—it doesn't just read from cache」. 문서 요약 문장과 설치판 표현이 다르므로 **출력(원천 이름·호출 수) 기준**으로 쓰고, 문서는 「다시 실행한다」까지만.
4. **고른 자리 뒤의 멈춤 표시 노드는 다시 멈춤**(문서 「Interrupts are always re-triggered during time travel」, 준비 e4 — 새 값이 질문 값에 실림). 01·02 멈춤 표시와 잇는 장면 후보(넣으면 사람의 답은 셀에 적은 값, 01·02 용어 그대로).
5. **가격은 정수 계산**: 옛 `int(10000 * (1 - rate))`는 0.1·0.2·0.29는 맞지만 **0.33에서 6699**(6699.999…를 잘라 냄 — 02가 기기 Python으로 다시 확인, `10000 * (100 - 33) // 100` = 6700). 할인은 **정수 백분율**(예 칸 `percent` 10 → 20, `price * (100 - percent) // 100`)이나 정해 둔 값 표로. 숫자 밑줄 `10_000`·식 안 숫자는 이름 있는 변수로(`//`는 처음 쓰면 한 문장 — 과정 요약 §2-1).
6. **말**: fork는 **「새 가지」**(「분기」·「갈래」 금지 — 「갈래」는 Ch 13 조건부 엣지 뜻이고 02가 그 뜻으로 조건부 엣지를 씀). 제목 「분기」·「재실행」은 제목에만(02처럼 제목 풀이 한 문장은 「재실행」 글자 없이, 강사 확인). 「time travel」은 한 번 풀고 본문은 「지난 체크포인트에서 다시 실행」. 「snapshot」 → 체크포인트, 「trace」 → 칸 이름만(본문 「실행 흔적」은 Ch 13 01 말), 리듀서는 Ch 13 02 말(01·02 금지어 검사 목록에 있어 쓰면 거짓 양성으로 기록). 옛 b5·b7의 「보상 작업·격리」(Ch 31 몫)·「LLM 다시 호출」은 실행하지 않았다고 적거나 뺌.
7. **ID 출력하지 않기**: 체크포인트 ID·`Interrupt.id`·시각(`created_at`)은 실행마다 바뀜 → 출력·인용·그림 라벨 0. 설정 딕셔너리째 `print`하면 ID가 찍히므로 **원천·단계·다음 노드·칸 값만** 출력.
8. **도구 파일**: 02는 도구 파일을 바꾸지 않았음(`b40aab98ae6d…`, 함수 셋). 03이 Ch 23 01 `print_history(history)`를 쓰면 **03 생성기가 `author_01.TOOLS` + 새 함수로 다시 쓰고** 01 함수 셋은 글자 그대로(01 `check_same_as_ch23()`·02 `checks()`처럼 대조), 주석 `# Ch 23 01절에서 배웠습니다 — 01절 노트북 8절의 같은 이름 함수를 옮겼습니다`, 가져오면 준비 셀에 고정 세 문장 + 커널 폴더 한 문장. 02의 `make_question`·`record_counts`는 02 노트북에만 있음(03이 쓰면 도구 파일로 옮기되 01이 가져오는 이름은 바꾸지 않음). 도구 파일을 고치면 챕터·Part 공개 목록은 해시만 바뀜.
9. **02가 가르친 것(03은 「02절에서 본 것처럼」으로)**: 새 말 **허용 답 목록 · 다시 묻기 · 차례 맞추기**(한 노드 안 여러 `interrupt`에 답을 부른 차례로 맞춤 — `types.py` 866~868행) · 조건부 엣지가 같은 노드로 되돌아가는 모양(Ch 20 01 되돌아가는 엣지와 견줌) · 노드가 기록 목록에 `시작`·`질문`을 적어 횟수 세기 · 노드가 갱신을 내고 마칠 때마다 체크포인트 하나 · 체크포인터 없이 이어 가기 → `RuntimeError`(`_loop.py` 904~908행) · 멈춘 적 없는 스레드로 이어 가기 → `KeyError`(스레드 칸 값 `{}`, 다음 노드 남음) · 끝난 스레드에 다시 보내기는 노트북 밖만(오류 없이 그대로). 노트북 안 `while True`는 02 4절 「권하지 않는 모양」 한 셀뿐, `try`는 02 6절 노드 밖 둘뿐 → 03은 쓰지 않는 쪽.
10. **이어 쓸 이름과 값**: 준비 셀 셋 그대로(임시 폴더 셀은 `author_02.FOLDER.replace("ch24-02-", "ch24-03-")` 또는 01 판에서 — `assert`, 메모리 체크포인터면 마지막 셀 `[]`) · 상태 형식은 칸이 다르면 새 이름(01 `ApprovalState` · 02 `ReviewState`) · 주문 키를 잇는다면 `order-2403`(01 `order-2401` · 02 `order-2402`). 체크포인트 수는 **우리 그래프 값**(02 조건부 엣지 모양 2 → 3 → 4 → 5, while True 2 → 2 → 2 → 3 — 노드 둘인 03 그래프는 새로 셀 것, 준비 e3 원본 4 · `update_state` 뒤 +1 · 다시 실행 뒤 +2).
11. **그림·색(02 선례)**: experiment **빨강 0**, 받은 오류 노랑, 소스로만 확인한 값은 회색 「소스 확인」(02-3), 조건 함수는 회색 마름모(02-1), 라벨 숫자는 출력에 있는 것만(02는 `2402` 하나)·개수는 한글. **새 가지 그림이 Ch 13 조건부 엣지 갈림길처럼 보이지 않게**(원본 줄과 새 가지를 칸 둘 + 공통 상자로). 비유 계열 03 후보: 넘어진 원래 도미노 줄은 그대로 두고, 가운데 한 자리에서 다른 방향으로 새로 세운 줄(Ch 23 사진 한 장 = 체크포인트 한 문장으로 이음). 01 컵·02 파란 구슬과 연두색 도미노는 이미 씀, 「조각」 금지, 금지 소품 목록 그대로.
12. **작업 순서와 주의**: `run_section.sh`는 생성기를 `python3`(`-B` 없이)로 부르므로 **생성기 첫머리 `sys.dont_write_bytecode = True`**(02 선례 — `author_01`을 가져와도 `qa/upgrade/__pycache__` 없음) · 첫 실행 전 `upgrade_gates.py … --label wip-03 --section 03` · `/tmp/ch24-03/` 사본으로 먼저 `execute.py` → A → B → 셀별 대조 → 그림 · Mermaid에서 노드가 자기 자신으로 돌아오는 점선은 라벨이 겹침(02-1 첫 판) · 03 b8 「다음 학습」은 지금 Ch 25(실습 절을 붙이면 마감이 04로) · 뒤 챕터 Ch 25 b3 「interrupt와 재개 사건」은 부분 참 그대로(고치지 않음) · 02는 묶음 실행 검사 대상 아님(01만).

## §03 → 실습(04)

**04절 주제**: 챕터 끝 실습 절 신설(규격 §7-2 · PLAYBOOK §3 — 슬러그 후보 **`04-Human-in-the-Loop-실습`**(선례 `07-Persistence-실습`·`09-Middleware-실습`·`07-create-agent-실습`·`05-ToolNode-실습`·`08-LangGraph-실습` — 챕터 제목의 앞말, 준비 노트 §12. 다른 후보 `04-Human-in-the-Loop와-Time-Travel-실습`은 길어짐), 제목 「Human-in-the-Loop 실습: {주제}」, `chapter.json`에 `format: experiment`로 추가, meta 「실습 30분 · 새 용어 0」, **챕터 시수(3·5h)에 더하지 않음**). **03이 본문 마지막 절**이었습니다. 01~03의 이름·API만 쓰고 새 문법·새 API·새 말 0.

1. **03절이 남긴 자리(04가 생겨야 참)**: `_src` b8 「다음 학습과 이어지는 지점 — 04절 실습에서는 이 챕터에서 배운 것을 작은 흐름 하나에 모아 실행합니다.」 · 노트북 정리 끝 같은 문장(**링크 없음** — 04 파일이 아직 없음, Ch 23 06·Ch 21 06 선례). 04가 「이 챕터에서 배운 것(멈춤 표시·질문 값·사람의 답으로 이어 가기·허용 답 목록·다시 묻기·지난 체크포인트에서 다시 실행·값 고쳐 넣기·새 가지 가운데 2~3개)을 한 흐름에」 모으면 그대로 참. 04가 생기면 03 b8에 `<a href="04-…-실습.html">`을 넣음(`author_03.py`의 `_src` 문장 → `--src-only` → `run_section.sh … 03 --no-exec`, 노트북 문장은 `mdpatch.py`로만 — 03은 다시 실행하지 않아도 됨). **Ch 25로 잇는 문장은 04 b8 몫**(03에서 뺌 — Ch 25 01 b2 「한 실행에서 생긴 사건을 일곱 방식으로 관찰」). 03 b7이 남긴 「실행하지 않음」: 멈춘 채 둔 가지(7절)에 답 넘기기 · 고른 자리 앞/뒤의 바깥 파일 쓰기 · 이어 붙이기 규칙 칸에 값 고쳐 넣기·`as_node`(노트북 밖만) · 모델 노드 — 04가 새로 풀면 새 설계가 되므로 **다루지 않는 쪽**을 권합니다.

2. **이어 쓸 이름 — 도구 파일 `labs/part6/ch24-human-in-the-loop/notebooks/approval_tools.py`(03이 함수 둘을 더함, `d562c9e67c56cab1a6e8435e7f926a7c1858a621faf5f3a9fdaa51a632f1b31f`, import `os`만, 묶음 목록 둘에 이미 올라 있음 — 경로 배열이라 그대로)**:

   | 함수(인자) | 배운 곳 | 01~03에서 | 하는 일 |
   |---|---|---|---|
   | `read_record(record_name)` | Ch 23 04 노트북 3절 | 01이 가져옴 | 기록 파일의 줄 → 목록(`split()`) |
   | `append_key(record_name, order_key)` | Ch 23 06 노트북 2절 | 01이 가져옴 | 기록 파일 끝에 키 한 줄(`"a"`), `"적음"` |
   | `append_key_once(record_name, order_key)` | Ch 23 06 노트북 2절 | 01이 가져옴 | 같은 키가 있으면 `"건너뜀"`, 없으면 `append_key` |
   | `print_history(history)` | Ch 23 01 노트북 8절 | **03이 가져옴** | 체크포인트 목록을 `단계 번호 \| 만든 자리 \| 다음 노드 \| 칸 값` 한 줄씩(아이디·시각 없음) |
   | `find_before(history, node_name)` | **Ch 24 03 노트북 4절** | 03 노트북에 정의 | 목록을 최신 것부터 보며 `node_name in snapshot.next`인 첫 체크포인트(`for`+`break`), 없으면 `None` |

   - 01 함수 셋은 Ch 23 `checkpoint_tools.py`와 문자열·AST 같음(`author_01.check_same_as_ch23()`) · `print_history`는 Ch 23 01 노트북 셀 글과 문자열·AST 같음 · `find_before`는 03 노트북 셀과 같은 문자열(`author_03.checks()`). 도구 파일 = `author_01.TOOLS` + `author_03.NEW_TOOL_PARTS`(생성기 `author_03.TOOLS`). **04가 함수를 더하면** 04 생성기가 `author_03.TOOLS` + 새 함수로 다시 쓰고 `startswith(author_03.TOOLS)` 대조(`author_03.py`는 디스크 파일이 03 판 뒤에 더 붙은 판이면 덮어쓰지 않음).
   - **주의(마감 몫)**: `author_02.py` `checks()` 셋째 줄(`도구 파일 == author_01.TOOLS`)이 이제 거짓 — 02 생성기를 돌리려면 그 줄부터 고칠 것. `author_01.py`를 `--src-only` 없이 돌리면 도구 파일을 함수 셋 판으로 덮어써 03 가져오기가 멈춤.
   - 04는 **처음 가져오는 절이 아니어도** 고정 세 문장(「앞에서 배운 함수는 `approval_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.」)과 「커널이 `notebooks/` 폴더에서 시작해야 …」·「교재 출력을 만든 실행 도구는 …」 문장을 준비 셀 결과 읽기에(01·03 선례), 가져오기는 **임시 폴더로 옮기기 전**, 이름은 알파벳 순.
   - **노트북에만 있는 함수(처음 가르친 절)** — 04가 쓰면 `# Ch 24 NN절에서 배웠습니다 — …`로 도구 파일에 글자 그대로 옮기고 생성기 상수와 대조: 02 `make_question(order_key, error_text)`(허용 답 목록을 전역 `allowed_answers`에서 읽음 — 옮기려면 인자로 바꿔야 해 「글자 그대로」가 안 됨 → 04에서 다시 적거나 쓰지 않는 쪽) · 02 `record_counts(calls, graph, config, rows)` · 노드 함수(`ask_then_charge`·`ask_once`·`after_answer`·`quote`·`discount`·`ask_price`)는 전역 목록·이름에 기대므로 04 노트북에 새로 적음(노드는 도구 파일에 두지 않음 — Ch 23 선례).

3. **허용 문법 범위(01~03 끝 — 04는 이 안에서만)**: 칸만 적은 `TypedDict` 상태 형식(칸 구성이 바뀌면 새 이름 — `ApprovalState`·`ReviewState`·`PriceState` 선례, 04는 새 이름) · 노드 함수(힌트 없음) · `StateGraph`·`add_node`·`add_edge`·`START`·`END`·`add_conditional_edges(노드, 조건 함수, 이름표 표)`(02 — 같은 노드로 되돌아감, 조건 함수는 `END` 또는 이름표를 내놓음) · `compile(checkpointer=InMemorySaver())`·`compile()`(02 실패 장면) · 설정 `{"configurable": {"thread_id": …}}` · 노드 안 `interrupt(질문 값)`(한 노드에 한 번 — 02 권하는 모양) · `invoke(입력, 설정)`·`invoke(Command(resume=답), 설정)`·**`invoke(None, 고른 체크포인트의 설정)`**(03)·**`update_state(고른 설정, {칸: 값})`**(03, `as_node` 없이) · 결과 키 `__interrupt__`·`[0].value` · `get_state(설정)`의 `.values`·`.next`·`.tasks[0].interrupts[0].value`·`.tasks[0].error`·`.parent_config`·`.metadata["step"]`·`["source"]` · `list(get_state_history(설정))`을 변수에 담은 뒤 `len`·`[0]`·`[:2]` · `print_history([스냅숏])` · 목록 `append`·`count`·`in`·슬라이스 `목록[시작:]`(03 — 셀에서 새로 적힌 이름만) · 여러 줄 `if` · `for`·`break`(함수 안) · `range(len(…))`(02) · 글 `+` · `//`(03 첫 사용, 정수 백분율) · `int()`(03 소수 견줌 셀) · `os.listdir`·키워드 없는 `sorted`(마지막 셀) · `tempfile.mkdtemp`·`os.chdir`(준비 셀) · `with open(…)`(도구 파일 안) · `try`/`except RuntimeError`·`KeyError` `as error`(02 노드 밖 `invoke` 감싸기 — 둘뿐) · `type(error).__name__` · `assert`(우리 코드·라이브러리가 정하는 값에만). **01~03 모두 안 쓴 것**: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`key=`·`reverse=`·`set`(리터럴 포함)·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·튜플 풀기·별표 풀기·`{**…}`·숫자 밑줄·세미콜론·`isinstance`·데코레이터·클래스(상태 형식 말고)·`Path`·`unlink`·노드 안 `try`·모델. `while True`는 02 4절 「권하지 않는 모양」 한 셀뿐 → 04는 쓰지 않음. **체크포인트 ID·`Interrupt.id`·시각·임시 폴더 위치는 출력하지 않음**(설정 딕셔너리째 `print` 금지).

4. **결정적 값(01~03, 새 커널 두 번 모두 같음 + 노트북 밖 확인)**: 01 노드 하나짜리 그래프 체크포인트 멈춘 동안 2 → 이어 간 뒤 3 · 네 장면 줄 수 `charge_then_ask | reject` 2 · `ask_then_charge | reject` 0 · `| approve` 1 · `receive_then_ask | reject` 1 · 02 조건부 엣지 모양 시작·부름·체크포인트 `1·1·2 → 3·3·3 → 5·5·4 → 6·6·5` ↔ while True `1·1·2 → 2·3·2 → 3·6·2 → 4·9·3` · `RuntimeError: Cannot use Command(resume=...) without checkpointer` · 스레드 `other` `KeyError: 'order_key'`·칸 값 `{}` · **03** 가격 그래프(노드 셋, 스레드 `price-2403`) 첫 실행 체크포인트 5(`-1 input` · `0~3 loop`) · 고른 체크포인트 `1 | loop | ('discount',)` · `update_state` → `2 | update | ('discount',)`·부모 `True`·6 · 새 가지 실행 노드 `['discount', 'ask_price']`·질문 값 8000 · 8 · 스레드 설정 8000 ↔ 담아 둔 설정 9000 · 그대로 다시 실행 `2 | fork | ('discount',)`·질문 값 9000·10 · 할인 33 → 6700 · 13 · 실행 횟수 `quote 1`·`discount 4`·`ask_price 7` · 소수 할인율 `6699.999999999999`·`6699` ↔ 정수 `6700`. **흔들린 값 없음**(모델 0) — 달라지는 것은 아이디·시각·임시 폴더 위치뿐(출력하지 않음). `outputs_sha256`은 설치 셀 스트림 나뉨으로 흔들림 → 셀별 글로 대조.

5. **요청 수와 04**: 01~03 모두 **모델 요청 0번**(챕터 리드 결정 1, M1 — 키 셀·모델 셀·`dotenv` 없음, 잠금에 모델 패키지 없음). 규격 §7-2 실습 절 「모델 호출 3~5번」과 다름 → 04도 0번이면 **까닭을 04 진단·챕터 요약에 적고 강사 확인 대상**(Ch 23 07 선례 — 모델 없는 챕터의 실습 절 요청 0). 사람의 답은 셀에 적은 값이라는 문장을 준비물·b5에. 모델을 넣으려면 `uv lock`(보호 파일) — 챕터 리드 결정 없이 하지 말 것.

6. **04 설계 권고(규격 §7-2, 준비 노트 §12)**: 실행 1(기본) → 실행 2(값 하나만 바꿈), 각각 예상 → 실행 → 출력 확인 → 비교, 본문 「앞에서 배운 내용」에 「절 | 배운 것 | 실습에서 쓰는 곳」 표, 그림 조립도·실행 1 순서·실행 1·2 비교 + 삽화 1. 「앞 절 기능 2~3개」 후보 — **Ch 23 07 대출 소재 잇기(이용자 `M-0317`·대출 키 `loan-2307`, 준비 노트 §12)**: 연장 기록 노드 앞 승인 지점(01 `ask_then_charge` 모양 — 승인일 때만 `append_key_once`) + 허용 답 목록 검사(02 조건부 엣지로 다시 묻기) + 지난 체크포인트에서 연장 일수만 고쳐 넣어 다시 실행(03 `find_before`·`update_state`·`print_history`). 실행 2는 값 하나만 — 사람의 답을 `reject`로, 또는 고쳐 넣는 연장 일수 하나. 주문 키 선례 `order-2401`·`order-2402`·스레드 `price-2403` → 04는 `…-2404` 꼴. 파일은 임시 폴더에만(`ch24-04-`), 지우는 줄 0, 결과는 코드가 정하는 값이라 `assert` 가능(줄 수·체크포인트 수·실행 횟수·만든 자리). 한 커널 안에서 끝남(자식 프로세스·SQLite 없음 — 잠금에 SQLite 체크포인터 없음).

7. **아직 가르치지 않은 것(04가 설명 없이 전제하면 안 되는 것)**: 스트리밍 `stream`·`stream_events`(**Ch 25 몫**) · **사람 승인 미들웨어(`HumanInTheLoopMiddleware`)·모델이 고른 도구 호출 승인 — 이 챕터에서 다루지 않음**(Ch 27 08 「도구 실행 경계」는 부분 참 그대로) · 정적 중단점 `interrupt_before`/`interrupt_after` · 여러 노드가 함께 멈춘 뒤 아이디 딕셔너리로 이어 가기 · `update_state(…, as_node=…)`·이어 붙이기 규칙 칸에 값 고쳐 넣기(03 노트북 밖만) · 멈춘 채 둔 가지에 답 넘기기 · 끝난 스레드에 다시 답 보내기(02 노트북 밖만) · `Command(goto=…)`와 `resume` 함께 쓰기 · 한 노드 안 `interrupt` 여러 번(02 권하지 않는 모양에서만) · 노드 안 `try`로 멈춤 표시 감싸기(01 노트북 밖만) · SQLite·Postgres 체크포인터(이 잠금에 없음) · 모델·에이전트 그래프에 멈춤 표시 · 체크포인트 아이디 출력·`checkpoint_id` 직접 적기 · 걸린 시간 재기 · Windows·macOS 출력. 본문에서 「재개」·「분기」·「재실행」·「갈래」(이 뜻으로)·「fork」(원어 풀이 밖) 쓰지 않음.

8. **비유 계열 「도미노 줄과 비워 둔 자리」와 삽화 소품**: 빈자리 = 멈춤 표시 · 빈자리에 도미노를 놓는 일 = 사람의 답 · 넘어진 컵 = 되돌리기 어려운 쓰기 · 빈자리에 맞지 않는 물건 = 허용 답 목록 밖의 답 · 원래 줄 옆에 새로 세운 줄 = 새 가지(Ch 23 사진 한 장 = 체크포인트는 문장으로만). **쓴 소품**: 01-5 도미노 두 줄·줄마다 빈자리 하나·흰 컵 둘(위 줄 빈자리 앞에서 쓰러짐 ↔ 아래 줄 빈자리 뒤에 섬) · 02-6 도미노 두 줄·위 줄 빈자리의 파란 구슬(오른쪽 일곱 서 있음) ↔ 아래 줄 가운데 연두색 도미노(끝까지 넘어짐) · **03-5 나무 도미노 한 줄 열다섯 모두 넘어짐 + 가운데쯤에서 오른쪽 위로 뻗은 주황 줄(넷 넘어짐 → 빈자리 → 둘 서 있음)**(1차 job `b6d66b2b-9e64-4f57-88fb-e4f905ccbb7e`, 2크레딧, 거래 14:53:44Z). 04 후보: 한 흐름에 기능을 모은 모습을 **새 소품으로**(컵·구슬·주황 줄 되풀이 피함, `figures/*.prompt.md` `grep`으로 확인) — 예: 도미노 줄 둘 나란히(실행 1·실행 2), 줄마다 빈자리 하나, 값 하나만 다른 모습처럼 물건 수를 작게. 규칙: 「조각」 금지(Ch 5 토큰 전용), 사람·손·화살표·화면·시계·글자·숫자 없음, 물건은 크게, 개수·자리·상태를 이름으로, 금지 소품(도장·쟁반·서랍·바구니·저울·울타리·발자국·공구판·승강 상자·세탁기·체스판·즉석사진·기보·리본), 스타일 첫 문장은 규격 §5-4 그대로, `nano_banana_pro` 16:9 2k `use_unlim:false` count 1, 절당 1장·재생성 1회까지, 크레딧은 거래 기록으로 그 절 몫을 가릴 것. 모델이 도미노 수·빈자리 폭을 틀리기 쉬움 — 그림 읽기에 「개수는 짝짓지 않음」.

9. **실행 방법(01~03과 같음)**: A `PYTHONDONTWRITEBYTECODE=1 env -u OPENAI_API_KEY bash run_section.sh … 04` · B 사본 `/tmp/ch24-04/B/`에 노트북·도구 파일 → `env -u OPENAI_API_KEY UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch24-human-in-the-loop UV_NO_SYNC=1 PYTHONPATH=/tmp/ch24-04/B PYTHONDONTWRITEBYTECODE=1 uv run --project labs/part6/ch24-human-in-the-loop --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip --with python-dotenv==1.2.3 python textbook/_notebook/execute.py …` → `cmpout.py`(`/tmp/ch24-03/tools/` 복사). **실습 폴더 안에서 먼저 실패하면 `.failure.json`이 남고 지울 수 없음** → 첫 실행은 `/tmp` 사본 T로. 생성기 첫머리 `sys.dont_write_bytecode = True`(`run_section.sh`가 `-B` 없이 부름), 손으로는 `python3 -B`. `uv run --project labs/…`는 환경 변수 셋 없이 부르지 말 것. 새 커널 B는 **그림 그리기 전에**.

10. **셀 모양과 문장 선례**: 03 코드 셀 **28**(준비 셋: 설치·가져오기·임시 폴더), 준비 셀이 아닌 셀 주석 뺀 코드 최대 9줄, 함수 본문 최대 6줄(도구 파일 최대 7줄 — `append_key_once`), 셀당 정의 하나, 검사 문장 412. 실습 절은 19~25셀 선례(Ch 22 09 19셀 · Ch 21 07 24셀 · Ch 23 07). **G5**: 결과 읽기 첫 단락의 숫자 든 백틱은 바로 앞 셀 출력에 글자 그대로(정의 셀 결과 읽기 첫 단락에는 숫자 백틱을 두지 말 것 — 출력이 없음), 여러 줄 출력은 「라벨 줄 아래」. **G6**: 70자 — b8·b10 긴 문장이 잘 걸림(03 첫 검사 셋), 괄호 뒤 `).`는 문장 끝으로 세지 않음. 「글자 그대로」는 생성기 `assert`로 대조한 것만.

11. **그림·색 선례**: 03 Mermaid 4장(폭 657·497·630·561) — 두 가지 나란히 = 회색 공통 상자 → subgraph 둘(03-1·03-3, 갈림길로 보이지 않게 실선·점선 없음) · 목록 차례 = 한 줄 상자 + 함수가 고른 자리에 점선(03-2) · 결과 모음 = 칸 안 `~~~`(03-4). 가운뎃점(`·`)이 든 긴 줄은 저절로 꺾이니 `<br>`로 미리(03-1·03-3 첫 렌더). 04는 experiment라 **빨강 0**(받아 출력한 오류도 노랑), 보라 0(모델 없음), 넣은 값·사람의 답 초록 · 우리 노드·함수 파랑 · 출력 노랑 · 공통·라이브러리·조건 함수 회색(마름모), 라벨 숫자는 출력에 있는 것만·개수는 한글, `('__start__',)` 같은 밑줄 값은 말로(「가상 시작점」), 원본 폭 868 이하.

12. **마감 몫(01~03 진단의 남은 것 전부 — 04 뒤 챕터 마감 담당)**:
    - **01은 묶음 실행 검사 대상**(Part 6 `check_bundle_execution.py` — 01만 키 없이 새 커널): 01 `code_sha256` **`7187f7a39f3f…`**, 01 코드 셀을 고치거나 다시 실행하면 값이 바뀜 · 03이 도구 파일에 함수 둘을 더했지만 01이 가져오는 이름 셋은 그대로 — **03 뒤 새 도구 파일로 01 사본을 `PYTHONPATH` 없이 `--cwd`로 실행해 PASS·28/28 같음·`code_sha256` 같음 확인**(03 진단 §3). 마감: **zip 다시 만들기**(`python3 textbook/part6/_build_index.py` — 지금 `part6-practice.zip`(`aa82b386…`) 안은 옛 01~03 노트북·도구 파일 없음) → `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache UV_LINK_MODE=symlink python3 textbook/part6/qa/check_bundle_execution.py` → `bundle-execution.json` 새 해시·01 새 `code_sha256`을 챕터 요약·계약 §5에 · `check_delivery.py`(`llm-practice.zip` Stale 예상).
    - **실습 폴더 README 다시 쓰기**: 「승인 결과는 실습 폴더의 로컬 파일에만 기록」 — **01부터 거짓**(기록은 노트북 임시 폴더) · 노트북 넷 · `uv sync --locked` → `.venv` → `notebooks/`에서 열기 · 도구 파일 단락(`approval_tools.py` 함수 다섯·import `os`) · 절별 모델 요청 0 · API 키 없음.
    - **`chapter.json`**: 04 절 추가 · `objectives` 셋 대조 — 「interrupt와 Command(resume=)로 승인 게이트를 구현」(→ 멈춤 표시·승인 지점 말) · 「승인 입력을 검증하고 … 재개」(「검증」·「재개」 → 허용 답 목록 검사·사람의 답으로 이어 가기) · 「… 다른 값으로 새 분기를 실행」(「분기」 → 새 가지) → `_build.py`.
    - **Part 6 목차·묶음 목록**: `textbook/part6/_build_index.py` 22행(시수 3·5 그대로, 설명 「승인 시점에 중단·재개하고 과거 상태에서 다른 분기를 실행합니다」 — 「중단」·「재개」·「분기」 대조) · `textbook/_notebook/build_index.py` 52행(절 수 3 — 선례대로 둘지) · 챕터 `qa/public-files.json`·`textbook/part6/public-files.json`에 04 노트북·HTML 줄(`collect_public_files.py`) · 챕터 목록의 **옛 SVG 세 줄**(`figures/0N-흐름.svg`)을 옛 그림 삭제와 함께 정리 · `check_scope.py` `EXPECTED`·`SECTION_COUNTS`(기록만) · `labs/part6/continuity-guide.md` 10행 「과거 상태에서 분기」(뜻은 참, 말 대조).
    - **옛 생성기 이동**: 공용 `textbook/part6/ch23-persistence/qa/author_ch23_ch24.py`(`3fc72ded…`, 첫머리 `raise SystemExit`) `mv -n` → `textbook/part6/ch23-persistence/qa/upgrade/before/generators/blocked/`(옮기면 Ch 23 `before-manifest.json`·계약 문서가 가리키는 옛 자리가 비므로 기록에 한 줄) · Ch 24 `figures/_gen_figures.py`(`2a015c6a…`) `mv -n` → `qa/upgrade/before/generators/blocked/`.
    - **옛 그림 9개** 삭제 승인 목록(`figures/0N-흐름.{svg,excalidraw,caption.md}`, N=1~3 — 본문 참조 0, 사본 `before/figures/`, 캡션에 「반환값」·「분기」, `final-artifact-hashes.json`이 해시를 적은 기록 파일) · `visual.cjs`(1280px·390px).
    - **생성기 대조 줄**: `author_02.py` `checks()` 도구 파일 대조(§2 주의) · 도구 파일 함수 다섯을 `author_01.TOOL_PARTS`로 옮길지(Ch 23 07 마감 선례 — `author_06.TOOLS`에 `new_prefix`).
    - **Ch 30 06이 기대는 문장**: 01 b4 「묻기 전에 꼭 해야 하는 쓰기는 Ch 23 06절처럼 멱등 키로 한 번만 반영되게 적습니다」·b6·6절을 지울 때는 인계(지금 참).
    - `qa/research.md`·`qa/verification.md`·`집필점검표.md` 위쪽 옛 기록에 「개선 전 판」 표시 · 챕터 요약 `qa/upgrade/chapter-summary.md`(새 말 합 meta 3·3·3 = 9 — 말은 바뀜: 멈춤 표시·질문 값·사람의 답으로 이어 가기 / 허용 답 목록·다시 묻기·차례 맞추기 / 지난 체크포인트에서 다시 실행·값 고쳐 넣기·새 가지 · 도구 파일 해시 · 요청 0 · `gates-after.json`).
    - **제목의 영어·한자어(강사 확인)**: 챕터 「Human-in-the-Loop와 Time Travel」 · 01 「interrupt」·「게이트」 · 02 「Command」·「resume」·「재개」 · 03 「분기」·「재실행」 — 본문에서 한 번씩 풂. 슬러그는 01 고정(Ch 23 07 링크), 02·03 들어오는 링크 0.
    - **강사 확인 대상 모음**: 01~03 진단 §강사 확인(모델 없는 챕터 M1 · 01 멱등 앞쓰기 장면·도구 파일 새로 · 02 권하지 않는 `while True`를 한 번 실행·실패 장면 둘 · 03 정수 백분율 소재·`fork` 다시 실행을 노트북에서·도구 파일 함수 둘 · 세 절 코드 줄 50→158·32→146·43→137 · Mermaid 4·5·4장) + 04 요청 0번.
    - **뒤 챕터 인계**(고치지 않음, 챕터 요약에): Ch 25 01~03 b3 「interrupt와 재개 사건」 — 부분 참(사건은 Ch 25 몫) · Ch 27 01 b3 참 · Ch 27 08 b3 「도구 실행 경계」 — 부분 참(도구 호출 승인 장면 없음) · Ch 28 03 b3 참 · Ch 30 06 b3 「중복 실행 방지 원칙」 — 01로 참 · time travel·`update_state`를 말하는 뒤 챕터 문장 0 · Ch 23 03·07 문장 참(01 슬러그·장면 그대로).
    - **삭제 승인 대상**: 실습 폴더 `.venv`(macOS 판 125MB) · `.cache/vm/venv-ch24-human-in-the-loop`(207MB, 04까지 씀) · 기기 `/tmp/ch24-prep`·`/tmp/ch24-01`~`/tmp/ch24-03` · 기기 세션 임시 폴더 `$TMPDIR/ch24-0N-*` · `$ROOT/.cache/ch24-0N-view/` · `qa/upgrade/gates-wip-*.json`.

## 실습 → 챕터 검토

**04절 `04-Human-in-the-Loop-실습`을 새로 만들었습니다**(2026-09-25). 제목은 「Human-in-the-Loop 실습: 연장 일수를 고쳐 다시 묻고 승인일 때만 기록하기」이고 `chapter.json`에 `format: experiment`로 더했습니다. 기록은 `qa/upgrade/04-diagnosis.md`, 그림 설계표는 `qa/upgrade/04-figures.md`, 검토 묶음은 `qa/upgrade/review-pack/04-Human-in-the-Loop-실습.md`입니다. 위 「챕터 공통」의 준비 셀·용어·색·비유 약속은 그대로 삽니다. 슬러그는 위 「§03 → 실습(04)」 후보 그대로.

### 1. 이 절이 한 것

- **주제**: Ch 23 07 대출 소재를 이어 받은 대출 연장 신청 한 건 — 이용자 번호 `M-0317`(스레드 이름)·대출 키 `loan-2307`(둘 다 Ch 23 07 값 그대로), 신청서의 연장 일수 `14`(잘못 적힌 값)·고쳐 넣을 연장 일수 `7`·자료실 규칙 「한 번에 7일까지」(셋 다 이 절에서 실행 전에 정함). 상태 형식 `ExtendState`(칸 일곱 — `loan_key`·`record_name`·`days`·`left_days`·`due_days`·`answer`·`error`, 규칙 없음). 노드 `look_up_loan`(남은 날 `3` — 노드 안 상수) → `plan_extension`(`due_days = left_days + days`) → `ask_extension`(멈춤 표시 한 번 · 허용 답 목록 검사 · `approve`일 때만 `append_key`) ⇄ 조건 함수 `after_answer`(02 셀과 같은 문자열) + 이름표 표 `{"ask_again": "ask_extension", END: END}`.
- **붙인 앞 절 기능 셋 — 모두 흐름 안에서 쓰임**(두 실행 모두, 코드로 셈): **01** 승인 지점(확인 노드 안, 멈춤 표시 뒤 — 노드 다섯 번 실행에도 기록 한 줄/없음) · **02** 다시 묻기(첫 답 `change` → `['ask_extension', 'ask_extension']`·오류 글) · **03** 값 고쳐 넣기와 새 가지(`print_history` 목록 다섯 → `find_before`로 단계 1 → `update_state` `2 | update` → `invoke(None, …)` `['plan_extension', 'ask_extension']` → 스레드 설정으로 마지막 답이 새 가지에 닿음). 흐름의 까닭: 목록 밖 답 `change`로는 칸 값을 바꿀 수 없어 지난 체크포인트로 돌아감.
- 실행 1 = 사람의 답 차례 `["change", "approve"]`, 실행 2 = **마지막 답 하나만 `reject`**(01 값 바꿔 보기와 같은 값 — b2·노트북 7절에 「새로 볼 것」 한 문장). 두 실행은 설계 객체를 같이 쓰고 체크포인터는 실행마다 새로 붙임(스레드 이름 같음), 기록 파일 이름은 `extend-1.record`·`extend-2.record`.
- **뺀 것**(b3 둘째 단락): 01 Before·멱등 앞쓰기(`append_key_once` — 묻기 전 쓰기 없음) · 02 `while True`·실패 장면 둘 · 03 `fork` 다시 실행·소수 계산. 03 b7 「실행하지 않음」 장면(멈춘 채 둔 가지에 답 넘기기 · 원래 가지에서 이미 적은 뒤 돌아가기)은 인계 권고대로 다루지 않음(b7 한 줄씩).
- **새 문법·새 API·새 말 0개**(01~03 노트북과 AST 대조 — 내장 이름·속성·키워드 0, 새 import는 도구 파일의 `find_before` — 03 함수). **도구 파일 그대로**(`d562c9e67c56…`, 함수 넷 가져옴). 모델 요청 0 · 키 셀 없음 · 걸린 시간 재지 않음. `assert`는 기록 줄 수 1·기록 파일 없음에만.
- 코드 셀 **28개**(준비 셋), 준비 셀이 아닌 셀 최대 9줄, 함수 본문 최대 8줄(`ask_extension`), 코드 줄 153, 검사 문장 365, 게이트 G1~G7 **0**(챕터 전체 4/4 PASS). meta 「실습 30분 · 새 용어 0」, **챕터 시수에 더하지 않음**(`hours` 그대로). Mermaid 3 + 삽화 1.

### 2. 실행으로 확인한 값 (새 커널 T 15:27:12 · A 15:27:35~36 · B 15:27:55 UTC 세 번 28/28 같음 + 노트북 밖 준비 확인 다섯 번 같음 — 챕터 요약이 인용할 수 있는 값)

- 준비: `도구 파일에서 가져온 함수: append_key, find_before, print_history, read_record` · `임시 폴더 이름에 ch24-04-이 들어 있는가: True`·`현재 작업 폴더의 파일: []` · `이용자 번호: M-0317`·`대출 키: loan-2307`·`신청서에 적힌 연장 일수: 14 | 고쳐 넣을 연장 일수: 7`(출처 줄 둘) · `허용 답 목록: ['approve', 'reject']`·`사람의 답 차례: ['change', 'approve']` · `등록한 노드: ['look_up_loan', 'plan_extension', 'ask_extension']`·`고정 엣지로 적은 수: 3`·`조건부 엣지를 적은 노드 수: 1`.
- 실행 1: `이 셀에서 실행된 노드: ['look_up_loan', 'plan_extension', 'ask_extension']`·`질문 값: {'days': 14, 'due_days': 17, 'error': ''}` → `change` `['ask_extension', 'ask_extension']`·`다시 물은 질문 값: {'days': 14, 'due_days': 17, 'error': '허용하지 않는 값: change'}` → `체크포인트 수: 5`(단계 -1 `input` · 0~3 `loop`) → `1 | loop | ('plan_extension',)`·`따로 담아 둔 체크포인트의 연장 일수: 14` → `2 | update | ('plan_extension',)`(`'days': 7`)·`['plan_extension', 'ask_extension']`·`새 가지의 질문 값: {'days': 7, 'due_days': 10, 'error': ''}` → `approve` `['ask_extension']`·결과 `'days': 7, … 'due_days': 10, 'answer': 'approve'` → `연장 기록 파일의 키: ['loan-2307']`·`같은 키가 적힌 줄 수: 1`·실행 횟수 `1 2 5` → `원래 가지의 다음 노드: ('ask_extension',)`·`원래 가지의 연장 일수: 14`·원래 가지 질문 값(오류 글 `change`).
- 실행 2: `사람의 답 차례: ['change', 'reject']` → 다시 물은 질문 값 같음 → `1 | loop | ('plan_extension',)`·새 가지 질문 값 같음 → `칸 answer: reject`·`연장 기록 파일이 있는가: False`·실행 횟수 `1 2 5`.
- 견주기: `실행 1 | approve | 7 | 10 | 8 | 1`·`실행 2 | reject | 7 | 10 | 8 | 0`(마지막 답·연장 일수·연장 뒤 남은 날·체크포인트 수·같은 키 줄 수) · 끝 `작업 폴더의 파일: ['extend-1.record']`·`파일 수: 1`.
- 흔들린 값 없음. `code_sha256` **`c4722b0d084f…`**(T·A·B 같음) · `outputs_sha256` A `2aeaebb25174…`(B·T `afed104f1fe1…` — 설치 셀 스트림 나뉨) · 노트북 파일 `089ed8d9e413…`.

### 3. 함께 고친 파일 (검토자가 볼 곳)

**챕터 안**
- `chapter.json` — 04절 추가(`64fad507…` → `1ee64948471d…`). **`hours`·`objectives` 그대로**(objectives는 마감 몫, 아래 5번).
- **03절 마지막 문장**: b8·노트북 정리 끝 「04절 실습에서는 이 챕터에서 배운 것을 작은 흐름 하나에 모아 실행합니다」가 04 내용과 맞아 **글은 그대로**, 01·02 b8처럼 **`_src` b8에 04 링크만** — `author_03.py`(`6ec79811…` → `d2c014669b12…`) → `--src-only`(`_src/03` `a6eabd0d…` → `aa00400d83e3…`) → `run_section.sh … 03 --no-exec`(03 게이트 0). 노트북 끝 줄은 링크 없는 선례대로 두어 `mdpatch.py`를 쓰지 않음. **03 노트북 `e7649d5a0cbd…` · `code_sha256` `12b29f1517d5…` · `outputs_sha256` `aab2462d34f9…` · `executed_at` 14:52:29Z 그대로.** 03 빌드 HTML만 `d1d9e365…` → `421d2df7e1f0…`(다음 절 이동 줄 + b8 링크), 챕터 `index.html` `d0dc258b…` → `bd3554a12c2f…`. 01·02 HTML 바이트 같음.
- 챕터 `qa/public-files.json` — **04 HTML·04 노트북 두 줄**(03 줄 다음, `c629078f…` → `c72eba46684…`, 보호 파일). 옛 SVG 세 줄은 그대로(마감 몫).
- 새 파일: 노트북 04 · `_src/04`(`3cfa65d437e6…`) · 빌드 `04-Human-in-the-Loop-실습.html`(`31163ed0f2be…`, `{{` 0건) · `figures/04-1`~`04-3`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`) · `figures/04-4-따로-세운-세-줄을-이은-긴-줄.{png,prompt.md,caption.md}` · `qa/upgrade/author_04.py`(`20930d1a57b7…`) · `04-figures.md`·`04-diagnosis.md` · `gates-wip-04-04.json`·`gates-wip-04.json`·`gates-wip-ch24-after04.json` · `review-pack/04-Human-in-the-Loop-실습.md`. `run_section.sh … 03 --no-exec`가 `gates-wip-03.json`을 다시 씀(값 0 그대로).
- `집필점검표.md` 품질 개선 표 04 행 · `qa/verification.md` 품질 개선 검증 표 04 행 · `qa/upgrade/manifest-changes.md` 「04절 뒤」 · 이 파일 맨 위 한 줄과 이 절.

**챕터 밖**
- `labs/part6/ch24-human-in-the-loop/README.md` — 맨 아래 **04절 한 단락만**(`7c557ad26f23…`). 옛 두 줄(「승인 결과는 실습 폴더의 로컬 파일에만 기록」 — 01부터 거짓)은 마감 몫.
- `textbook/part6/public-files.json` — `python3 textbook/part6/qa/collect_public_files.py`로 다시 모음 → **04 노트북 한 줄만** 늘어남(`a77415947a7e…` → `7c9cb35e3374…`, 보호 파일). `prerequisite-files.json` 바이트 같음.
- `textbook/part6/index.html`(`afe83bc7dede…`) · `textbook/downloads/part6-practice.zip`(`61119a820068…`) · `textbook/part6/qa/integration-results.json`(`fa46898a97f4…`) — `python3 textbook/part6/_build_index.py` 한 번(**`Part 6: 51 verified sections; 98 bundled files`**). 목차에 Ch 24 「4절」·04 링크, **zip 안 Ch 24 항목 8개가 모두 디스크와 같아짐**(01~04 노트북·도구 파일 `d562c9e6…`·README·잠금 둘, `__pycache__` 0). `_build_index.py`는 고치지 않음(22행 설명은 마감 몫).
- `textbook/_notebook/checks/notebook-contracts-part6-ch24-human-in-the-loop.json` — `verify.py --chapter`가 다시 씀(`1a241f44e4a4…`).
- **고치지 않음**: 01·02 파일 · 03 노트북 · 도구 파일 · `pyproject.toml`·`uv.lock` · 공용 옛 생성기 `textbook/part6/ch23-persistence/qa/author_ch23_ch24.py`·`figures/_gen_figures.py` · 옛 그림 · Ch 23·25~31 파일 · `textbook/index.html` · `bundle-execution.json` · 공용 도구·규격·과정 요약·`build_index.py`.

### 4. 검사 결과

- `run_section.sh … 04 --no-exec`: 게이트 G1~G7 **0**, `verify.py --chapter` **`PASS 4 sections / 112 code cells (max 12 lines)`**, 빌드 HTML `{{`·`[[` 0건, SVG 셋·삽화 하나. 챕터 전체 `gates-wip-ch24-after04.json` **4/4 PASS**.
- `check_delivery.py` — **117행 `llm-practice.zip`의 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`에서 멈춤**(알려진 일, 전체 마감 몫). 그 앞(절 검사·비밀값·개인 경로·`part6-practice.zip` 매니페스트 신선도)은 지나감. `delivery-results.json` 안 바뀜(`3cc2d143…`).
- `check_bundle_execution.py`(Ch 24 01)·`check_scope.py`·`visual.cjs`·옛 검사 넷은 돌리지 않음(마감 몫).
- 보호 파일 131개: **109개 같음·22개 바뀜·없어진 파일 0** = 03절 끝까지의 16개(이 절이 값을 다시 바꾼 것 일곱: 묶음 목록 둘·`verification.md`·`집필점검표.md`·notebook-contracts·03 `_src`·03 HTML) + **이 절이 지시대로 새로 바꾼 여섯**(`chapter.json`·실습 폴더 `README.md`·챕터 `index.html`·`part6/index.html`·`part6-practice.zip`·`integration-results.json`) — `manifest-changes.md` 「04절 뒤」.
- 삽화 `04-4` 1차 채택(job `8434076e-428a-4312-8a2b-0716be792e1a`), 2크레딧(거래 15:29:48Z), 저장 PNG ↔ 채택 job 픽셀 차이 0.

### 5. 챕터 마감 담당이 이어서 할 것 (「§03 → 실습(04)」 12번 마감 몫 전부 + 01~03 진단의 마감 몫 + 04가 더한 것)

1. **묶음 실행 검사(Ch 24 01)**: `part6-practice.zip`은 04가 다시 만들어 Ch 24 항목 8개가 디스크와 같음(01 새 판 `code_sha256` `7187f7a39f3f…`·도구 파일 `d562c9e6…`). README·objectives를 고친 뒤 `_build_index.py`를 한 번 더 → `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache UV_LINK_MODE=symlink python3 textbook/part6/qa/check_bundle_execution.py` → `bundle-execution.json`(지금 옛 `718171990c5d…`)·01 새 `code_sha256`을 챕터 요약·계약 §5에. 그 뒤 `check_delivery.py`(`llm-practice.zip` Stale 예상).
2. **`chapter.json` `objectives`** 셋을 절 본문 말과 대조 — 「interrupt와 Command(resume=)로 승인 게이트를 구현」(→ 멈춤 표시·승인 지점) · 「승인 입력을 검증하고 … 재개」(「검증」·「재개」 → 허용 답 목록 검사·사람의 답으로 이어 가기) · 「… 다른 값으로 새 분기를 실행」(「분기」 → 새 가지) + **04 실습 줄을 넣을지**(예: 「실습에서 승인 지점·다시 묻기·값 고쳐 넣기를 한 그래프에 붙여, 사람의 마지막 답 하나를 바꿔 연장 기록 파일의 줄 수를 견줄 수 있습니다」) → `_build.py`. **제목의 영어·한자어(강사 확인)**: 챕터 「Human-in-the-Loop와 Time Travel」 · 01 「interrupt」·「게이트」 · 02 「Command」·「resume」·「재개」 · 03 「분기」·「재실행」 · **04 「Human-in-the-Loop 실습」**(슬러그 01 고정 — Ch 23 07 링크, 02·03 들어오는 링크 0, 04는 03 b8 링크 하나).
3. **실습 폴더 README 다시 쓰기 전체**(지금은 옛 두 줄 + 04 한 단락): 노트북 넷 · `uv sync --locked` → `.venv` → `notebooks/`에서 열기 · 파일은 노트북 임시 폴더에만(「실습 폴더의 로컬 파일에만 기록」 — 01부터 거짓) · 도구 파일 단락(`approval_tools.py` 함수 다섯·import `os`, 가져오는 절 01·03·04) · 절별 모델 요청 0 · API 키 없음.
4. **Part 6 목차·묶음 목록**: `textbook/part6/_build_index.py` 22행(시수 3·5 그대로, 설명 「승인 시점에 중단·재개하고 과거 상태에서 다른 분기를 실행합니다」 — 「중단」·「재개」·「분기」 대조, 실습 절 문구를 더할지 — Ch 21·23 선례) · `textbook/_notebook/build_index.py` 52행(절 수 3 — 선례대로 실습 절을 뺀 수로 둘지) · 챕터 `qa/public-files.json`의 **옛 SVG 세 줄**(`figures/0N-흐름.svg`)을 옛 그림 삭제와 함께 정리 → `collect_public_files.py` · `check_scope.py` `EXPECTED`·`SECTION_COUNTS`(기록만, 실습 절을 붙여 멈출 수 있음) · `labs/part6/continuity-guide.md` 10행 「과거 상태에서 분기」(뜻은 참, 말 대조) · 옛 검사 넷(`check_notebook_readiness.py`는 결과 파일 되돌림).
5. **옛 생성기 이동**: 공용 `textbook/part6/ch23-persistence/qa/author_ch23_ch24.py`(`3fc72ded…`, 첫머리 `raise SystemExit`) `mv -n` → `textbook/part6/ch23-persistence/qa/upgrade/before/generators/blocked/`(옮기면 Ch 23 `before-manifest.json`·계약 문서가 가리키는 옛 자리가 비므로 기록에 한 줄) · Ch 24 `figures/_gen_figures.py`(`2a015c6a…`) `mv -n` → `qa/upgrade/before/generators/blocked/`.
6. **옛 그림 9개** 삭제 승인 목록(`figures/0N-흐름.{svg,excalidraw,caption.md}`, N=1~3 — 본문 참조 0, 사본 `before/figures/`, 캡션에 「반환값」·「분기」, `final-artifact-hashes.json`이 해시를 적은 기록 파일) · `visual.cjs`(1280px·390px, HTML 넷).
7. **생성기 대조 줄**: `author_02.py` `checks()` 셋째 줄(`도구 파일 == author_01.TOOLS`)이 03부터 거짓 — 02 생성기를 돌리려면 그 줄을 `startswith(author_01.TOOLS)`(또는 `author_03.TOOLS`와 대조)로 고칠 것 · `author_01.py`를 `--src-only` 없이 돌리면 도구 파일을 함수 셋 판으로 덮어써 03·04 가져오기가 멈춤 · 함수 다섯을 `author_01.TOOL_PARTS`로 옮길지(Ch 23 07 마감 선례) — **옮겨서 도구 파일 글이 바뀌면 `author_04.py`의 `TOOLS_SHA256`(`d562c9e6…`)과 `tools == author_03.TOOLS` 대조, `author_03.py` `checks()` 마지막 줄도 함께 고칠 것**(04 노트북은 가져오는 이름만 쓰므로 함수 글이 같으면 다시 실행할 필요 없음).
8. **Ch 30 06이 기대는 문장**: 01 b4 「묻기 전에 꼭 해야 하는 쓰기는 Ch 23 06절처럼 멱등 키로 한 번만 반영되게 적습니다」·b6·6절을 지울 때는 인계(지금 참, 04는 이 장면을 쓰지 않음).
9. **기록**: `qa/research.md`·`qa/verification.md`·`집필점검표.md` 위쪽 옛 기록에 「개선 전 판」 표시 · **`chapter-summary.md`**(PLAYBOOK §6): 새 말 합 meta 3·3·3·**0** = 9(멈춤 표시·질문 값·사람의 답으로 이어 가기 / 허용 답 목록·다시 묻기·차례 맞추기 / 지난 체크포인트에서 다시 실행·값 고쳐 넣기·새 가지) · 도구 파일 해시·함수 다섯(04가 넷을 가져옴, `append_key_once`는 01만) · 요청 0(04 포함 — 규격 §7-2와 다름) · **실습 30분은 챕터 시수에 더하지 않음** · 04 주제와 결과(위 2번) · 비유 「도미노 줄과 비워 둔 자리」 네 장(01 컵 · 02 구슬 · 03 주황 줄 · 04 따로 선 세 줄과 이은 긴 줄) · 코드 줄 158·146·137·153(합 594)·도구 파일 30 · `gates-after.json`(`upgrade_gates.py … --label after`) · 한국어 감사 3단·그림 판독 별도 세션(01~04).
10. **강사 확인 대상 모음**: 01~03 진단 §강사 확인(모델 없는 챕터 M1 · 01 멱등 앞쓰기 장면·도구 파일 새로 · 02 권하지 않는 `while True`를 한 번 실행·실패 장면 둘 · 03 정수 백분율 소재·`fork` 다시 실행을 노트북에서·도구 파일 함수 둘 · 세 절 코드 줄 50→158·32→146·43→137 · Mermaid 4·5·4장) + **04 진단 §12**(모델 요청 0 · 실행 2가 01과 같은 값 · 목록 밖 답 `change` 소재 · 코드 셀 28(실습 선례보다 많음) · 새 값 넷).
11. **뒤 챕터 인계**(고치지 않음, 챕터 요약에): Ch 25 01~03 b3 「interrupt와 재개 사건」 — 부분 참(사건은 Ch 25 몫, 04도 스트림 0) · **04 b8은 Ch 25 01 b2 「한 실행에서 생긴 사건을 일곱 방식으로 관찰」을 「일곱 방식으로 받아 보는 방법」으로 잇는 문장만**(Ch 25 01 링크, 이름·그래프를 이어 쓴다는 약속 없음) · Ch 27 01 b3 참 · Ch 27 08 b3 「도구 실행 경계」 — 부분 참(도구 호출 승인 장면 없음, 04도 없음) · Ch 28 03 b3 참 · Ch 30 06 b3 「중복 실행 방지 원칙」 — 01로 참 · time travel·`update_state`를 말하는 뒤 챕터 문장 0 · Ch 23 03·07 문장 참(01 슬러그·장면 그대로, 04가 Ch 23 07 소재를 이어 받음 — Ch 23 쪽 파일은 고치지 않음).
12. **삭제 승인 대상**: 실습 폴더 `.venv`(macOS 판 125MB) · `.cache/vm/venv-ch24-human-in-the-loop`(207MB) · 기기 `/tmp/ch24-prep`·`/tmp/ch24-01`~`/tmp/ch24-04` · 기기 세션 임시 폴더 `$TMPDIR/ch24-0N-*`(04는 노트북 셋 + 준비 확인 `ch24-04-probe-*` 다섯) · `$ROOT/.cache/ch24-0N-view/`(N=1~4) · `qa/upgrade/gates-wip-*.json` · 각 절 진단 「지우지 않은 것」(04는 진단 §13).

### 6. Ch 25 작업자가 전제하면 안 되는 것

- **Ch 24는 모델을 부르지 않았습니다(01~04).** 모델이 고른 도구 호출을 사람이 승인하는 장면·사람 승인 미들웨어(`HumanInTheLoopMiddleware`)·에이전트 그래프에 멈춤 표시를 붙인 장면은 0건입니다. 사람의 답은 모두 셀에 적은 글(`approve`·`reject`·`maybe`·`yes`·`change`)입니다.
- **`stream`·`stream_events`·`stream_mode`는 0건**입니다. 멈춤 표시는 `invoke` 결과의 키 `__interrupt__`와 `get_state(…).tasks[0].interrupts[0].value`로만 읽었습니다. 「interrupt와 재개 사건」을 스트림 사건으로 본 적이 없습니다(Ch 25 01~03 b3은 부분 참). 04 b8은 Ch 25 01을 「한 실행에서 생긴 사건을 일곱 방식으로 받아 보는 방법」으로만 가리킵니다.
- **정적 중단점 `interrupt_before`/`interrupt_after`·여러 노드가 함께 멈춘 뒤 아이디 딕셔너리로 이어 가기·`update_state(…, as_node=…)`·`Command(goto=…)`·한 노드 안 `interrupt` 여러 번(02 권하지 않는 모양 말고)·멈춘 채 둔 가지에 답 넘기기·끝난 스레드에 다시 보내기(02 노트북 밖만)**는 노트북에서 가르치지 않았습니다.
- **체크포인터는 `InMemorySaver`뿐**(이 잠금에 SQLite·Postgres 체크포인터 없음)이고, 체크포인트 아이디·`Interrupt.id`·시각은 한 번도 출력하지 않았습니다. 체크포인트 수·실행 횟수는 절마다 **그 그래프의 값**(04: 노드 셋 + 조건부 엣지, 첫 질문·다시 묻기 뒤 5 → 끝 8)이라 다른 그래프에 그대로 쓰면 안 됩니다.
- **걸린 시간은 재지 않았습니다**(준비물의 「2초 안에」는 셀 실행 기록). Ch 25의 TTFT·total 비교에 Ch 24 시간 값을 쓸 것이 없습니다.
- **말**: 04는 새 말 0 — 01~03 말(멈춤 표시·질문 값·사람의 답으로 이어 가기·허용 답 목록·다시 묻기·차례 맞추기·지난 체크포인트에서 다시 실행·값 고쳐 넣기·새 가지)과 Ch 17 02 「승인 지점」만 씀. 본문에서 「재개」·「분기」·「재실행」·「갈래」(이 뜻으로)·「게이트」는 제목·슬러그 밖 0. 금지어는 위 「챕터 공통」 표.
- 공용 옛 생성기 `textbook/part6/ch23-persistence/qa/author_ch23_ch24.py`는 막혀 있을 뿐 **옮기지 않았습니다**(마감 몫). Ch 25 쪽 옛 생성기(`textbook/part6/_generate_ch25_ch26.py`)는 04가 건드리지 않았습니다.

## 검토 반영과 챕터 마감 (2026-09-25)

별도 세션 검토 둘(`review-round1-A.md` 01~02·공통 중 6 · 하 8, `review-round1-B.md` 03~04·마감 몫 중 5 · 하 12)을 반영하고 챕터를 마감했습니다. 전체 기록은 `chapter-summary.md`, 절별 마감 기록은 각 `NN-diagnosis.md`·`NN-figures.md` 끝 「마감 반영」입니다. **[중] 11을 모두, [하] 20 가운데 19를 반영**했습니다. 반영하지 않은 하나(A-13 도구 파일 머리 설명)는 도구 파일 해시 고정 결정 때문이고, 코드 셀을 고쳐야 맞는 둘(B-5 03 셀 9 · B-9 04 셀 5 주석)은 코드를 그대로 두고 다음 재실행 몫으로 적었습니다(B-9는 04 셀 6 결과 읽기에 한 문장으로 바로잡음). 뒤 챕터 몫(Ch 25 01~03 「재개 사건」·Ch 27 08 「도구 실행 경계」)은 그 챕터 파일을 고치지 않고 요약 §15에 적었습니다. **다시 실행한 노트북은 없습니다**(네 노트북 코드·출력 해시 전후 같음). 이 파일 위 기록 가운데 마감으로 사실이 바뀐 자리만 적습니다.

1. **생성기 대조 줄(검토 A-10·B-17 — 먼저 고침)**: 위 「§03 → 실습(04)」 2항 「주의(마감 몫)」와 「실습 → 챕터 검토」 5-7은 **끝났습니다**. `author_01.py`는 도구 파일이 없거나 01 판과 같을 때만 쓰고, 더 긴 판(지금 `d562c9e6…`)이면 건너뜁니다 — `run_section.sh … 01`을 실행 모드로 불러도 03·04 가져오기가 깨지지 않습니다. `author_02.py` `checks()` 셋째 줄은 `startswith(author_01.TOOLS)`. 함수 다섯을 `author_01.TOOL_PARTS`로 모으는 일은 하지 않았습니다(도구 파일 해시 고정).
2. **02 새 말**: 위 「§02 → §03」 9항의 새 말 셋 가운데 **「허용 답 목록」은 이어 쓰는 말**(Ch 16 01·Ch 18 02 「허용 목록」과 같은 뜻 — meta 새 용어 3 → 2). 「다시 묻기」는 Ch 18 02 「되묻기」(흐름을 끝내고 되물음)와 다른 뜻이라 새 말 그대로이고, 02 b3·용어 표·노트북 2·3절에 가르는 문장이 있습니다. 챕터 새 말 합은 **8**(3·2·3·0).
3. **03 설치판 행 번호**: 위 「§02 → §03」·03 진단에 적힌 `update_state` 자리 `main.py` 1733~1734행은 다른 갈래였습니다 → **`main.py` 2019행(단계 +1)·`pregel/_checkpoint.py` 128행(만든 자리 `update`)**(검토 B-1). 01 `types.py`도 857 → **858**~864행(A-2).
4. **그림**: 다시 렌더 `03-3`(공통 결과 상자를 두 칸 아래 `~~~`로, 폭 674) · `04-2`·`04-3`(「연장 뒤 남은 날」). 「남은 날」은 `left_days`(3)만, `due_days`(17·10)는 「연장 뒤 남은 날」. 삽화는 다시 만들지 않았고 03-5 글을 보이는 대로(「좁은 틈」) 고쳤습니다(B-6, 강사 확인).
5. **준비물의 걸린 시간**: 위 「파일 쓰기·시간·비용·실행」의 「준비물의 「2초 안에」는 셀 실행 기록으로 적은 값」은 **앞 판 기록**입니다 — 마감에서 네 노트북 준비물을 「걸린 시간은 재지 않았습니다」로 바꿨습니다(챕터 리드 결정).
6. **04 「새로 볼 것」**(B-8): 「다시 묻기와 새 가지를 거친 흐름에서도, 기록이 마지막 답 하나로 갈리는지」로 좁힘, 노트북 7절에 「원래 가지에 답을 넘기는 장면은 이 실습에서 실행하지 않습니다」. 실행 2 설계는 그대로(강사 확인).
7. **위 「§03 → 실습(04)」 12번·「실습 → 챕터 검토」 §5의 마감 목록은 끝났습니다**: 실습 폴더 README 전체(`706f760b…`) · `chapter.json` `objectives` 넷(`hours` 그대로) · `textbook/part6/_build_index.py` ch24 설명 줄 · `labs/part6/continuity-guide.md` Ch 24 줄 · 챕터 공개 목록 옛 SVG 세 줄 뺌(Part 목록 바이트 같음) · `part6-practice.zip` **`edd8c3be…`**(Ch 24 8파일 디스크와 같음 — 04 셀 6 결과 읽기를 늦게 고쳐 `_build_index.py`를 두 번 돌렸고 이것이 마지막 판) · `check_bundle_execution.py` **PASS**(`bundle-execution.json` `a72edd8a…`, Ch 24 01 `code_sha256` `7187f7a39f3f…`) · `gates-after.json` 4/4 · `verify.py --chapter` PASS 4/112 · `visual.cjs` 10행 PASS · 옛 생성기 둘 `mv -n`(Ch 24 `figures/_gen_figures.py` → `qa/upgrade/before/generators/blocked/` · 공용 `author_ch23_ch24.py` → `ch23-persistence/qa/upgrade/before/generators/blocked/`, 해시 같음) · 옛 기록 파일 셋에 「개선 전 판」 표시 · `chapter-summary.md`. 옛 그림 아홉·`gates-wip-*.json` 아홉·캐시·임시 폴더·`llm-practice.zip`은 `textbook/qa/upgrade-final-checklist.md` §2-12.
8. **01 묶음 실행 검사 계약은 그대로 삽니다**: 01에 모델·키 셀·새 패키지를 넣지 말 것. 01 코드 셀을 고치거나 다시 실행하면 zip → `check_bundle_execution.py`를 다시.
9. **Ch 25 작업자에게**: 위 「실습 → 챕터 검토」 §6과 요약 §13·§14 — 특히 **Ch 24에는 스트림 사건이 0건**이고 본문은 「재개」 대신 「사람의 답으로 이어 가기」를 씁니다. Ch 25 01~03 b3 「Ch24에서 interrupt와 재개 사건을 확인했습니다」는 Ch 25 작업 때 맞출 문장입니다.

