# 12-async와-await — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/12-concept.*`).
생성기: `qa/upgrade/author_12.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch02-python 12`.
먼저 읽은 것: Ch 1 `qa/upgrade/chapter-summary.md`, 이 챕터 01~11절 개선본(`_src` 08·11, `author_11.py`, `11-diagnosis.md`, `11-figures.md`, 11-6 삽화 프롬프트), `qa/upgrade/handoff.md`(특히 `## §11 → §12`), `upgrade_gates.py`, 뒤 챕터 확인용 Ch 3 01·02 노트북, Ch 4 04 노트북, Ch 18 03 `_src`·노트북, Ch 30 01·03 `_src`·노트북, Ch 34 04 노트북.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 1 | 0 |
| G2 | 1 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 7 | 0 |
| G6 | 31 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 16 (준비 2 + example 8 + before 3 + after 3(심화 1)) |
| 검사한 문장 | 115 | 385 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, 2026-09-16, 오류·stderr 출력 0), verify PASS(12절 174셀). 수정 후 수치는 `gates-wip-12.json`, 수정 전은 `gates-before.json`(덮어쓰지 않음). 빌드 HTML 가로 넘침 없음(puppeteer 1280px·390px에서 scrollWidth 1280·390, SVG 5·삽화 1, 남은 `{{` 토큰 없음).

## 수정 전 주요 문제

- **G1·G2**: 한 셀에 `record_heartbeat`·`blocked_probe` 함수 두 개, 15줄 넘는 셀
- **G1이 잡지 않은 사다리 문제**: 아직 안 배운 타입힌트 `list[str]`(변수·매개변수·반환값), `type(pending).__name__`, 형식 지정 f-string `{sequential:.3f}`, `set(...) == {...}`, `.index()` 비교를 print 안에서 계산, 한 줄에 `asyncio.gather(fetch_label("A", 0.04), fetch_label("B", 0.04))`
- **개념 과부하**: `asyncio.Event()`·`set()`·`wait()`, `asyncio.create_task()`, 하트비트, 태스크를 한 셀에서 처음 쓰면서 Before/After의 차이(한 줄)가 신호 코드 속에 묻힘. `asyncio.run()`은 주의할 점 한 줄뿐
- **이어짐 결함**: 데이터 「문서-A」·「느린 작업」·heartbeat가 1~8절 주문 데이터와 무관. 7절 타입힌트 예로 `name: str`·`-> str`만 언급하고 8절 subprocess·종료 코드, 5·6절 연필·노트를 받지 않음. 다음 학습의 「Ch 4에서는 동기 방식의 데이터 처리를 먼저 익힙니다」「Ch 18의 API 호출」은 구체 절이 없음
- G5: 제목 셀·「오늘 볼 그림」 없음, 결과 읽기 셀 없음. G6: 코드·영문 이름으로 시작하는 문장 23개(「`started.set()`은」「Before는」 등), 70자 초과 5개, 5문장 넘는 단락 3개. G7: Excalidraw 도식 1장뿐, Mermaid 0장, 삽화 0장, 설계표 없음

## §11이 넘긴 판단 거리

- **A 경로 전제**: 9~11절(함수를 값처럼 넘기기·`@` 줄·Pydantic·픽스처)을 쓰지 않음. `asyncio.to_thread(lookup_stock, ...)`에 함수 이름을 괄호 없이 넘기는 모양은 9절에서 배웠지만 A 경로 학생을 위해 노트북 10번과 본문 b6에서 「괄호를 붙이지 않으면 부르지 않고 함수 자체를 넘김」을 새로 설명함
- **Before 고르기**: 기존 학습 질문(동기 대기를 옮기면 다른 작업이 진행하나요?)과 Before/After 구조(같은 `time.sleep`, `to_thread`로 옮김)는 유지. 하트비트·Event·create_task 대신, 6번(gather)과 같은 두 확인을 동기 함수로 기다리게 해 「출력 줄 차례 + 걸린 시간」으로 차단을 보이게 함. 그래서 6번 셀(asyncio.sleep 판)과 After가 같은 차례·같은 0.2초라는 비교가 가능함. 11절 공유 목록·8~10절 `int()` 빠뜨림은 반복하지 않음
- **L7 사용**: `async def`·`await`·`asyncio.run`이 이 절의 학습 목표. G1이 `async def`를 잡지 않아 `upgrade_allow` 없음. 셀 하나에 함수 하나, 정의 셀과 호출 셀 분리. `asyncio.run()`은 노트북 셀에서 부를 수 없으므로(runners.py 설명, 실행 안 함) 8·7절 방식의 .py 파일로 실행
- **데이터**: 7·8절 `calculate_line_total` 대신 5·6절 주문 연필·노트를 씀. 함수 `check_stock(product_name: str, seconds: float) -> str`(자료형 float은 1절에서 배움). 걸린 시간은 4절 `round(elapsed, 1)`
- **뒤 챕터 연결 문장**: 노트북·본문에서 확인한 것만 남김. Ch 3 01·02 노트북의 `subprocess.run`·`with open`, Ch 18 03 `_src`(「반환 목록은 목적, 절차, 지원이라는 입력 순서」)와 노트북 `asyncio.gather`, Ch 30 01 `_src`(「비동기 함수 안에서 동기 HTTP 클라이언트나 긴 파일 처리를 호출하면 이벤트 루프가 멈출 수 있습니다」), Ch 30 03 노트북 `await agent.ainvoke`. Ch 4 문장은 뺌(Ch 4에는 async가 없지만 「동기 방식 데이터 처리를 먼저」는 본문 근거가 없음). 주의할 점의 「Ch 18에서 제공자 정책과 함께」도 뺌. 다음 학습 링크는 두지 않음(실습 절을 붙일 때 고침)

## 바꾼 것

- 노트북(paired 유지): 제목 → 오늘 볼 그림(12-1) → 준비(`3.12.13`, 임시 폴더 `[]`) → check_stock 정의 → 부르기만(`<class 'coroutine'>`, 확인 시작 줄 없음) → await(`확인 시작: 연필`·`확인 끝: 연필`·`받은 값: 연필 재고 있음`·`<class 'str'>`) → await 두 줄 차례로(`0.3`) → gather(시작 두 줄 먼저, `확인 끝: 노트` 먼저, `['연필 재고 있음', '노트 재고 있음']`, `0.2`) → 값 바꿔 보기 노트 0.3초(`확인 끝: 연필` 먼저, 목록 그대로, `0.3`) → stock_main.py(`381`글자)와 `asyncio.run(main())`(같은 목록, 종료 코드 `0`) → Before: 동기 함수 lookup_stock(`time.sleep`) 정의 → ask_warehouse가 바로 부름 → gather(`확인 끝: 연필` 다음 `확인 시작: 노트`, `0.3`) → After: `await asyncio.to_thread(lookup_stock, product_name, seconds)` 한 줄 → gather(`확인 시작: 노트`가 먼저, `0.2`, assert 반환값 목록) → 원리 더 알아보기(심화): 스레드 이름 `MainThread`·`asyncio_1` → 정리
- **학습 목표 조정**: 「태스크의 완료 순서와 gather 반환 순서」→ await 두 줄과 gather의 걸린 시간·반환 순서, 「heartbeat 관찰과 to_thread 수정」→ 출력 줄 차례와 걸린 시간으로 차단을 읽고 to_thread로 고치기. 태스크·Event·create_task는 쓰지 않음(handoff에 「아직 안 가르친 것」으로 남김)
- 본문 10블록 전체를 다시 씀. 「앞에서 배운 내용」 표 5행(Ch 1 4절·4절·5/6절·7절·8절), 용어 7개 표(비동기 함수·코루틴·await·이벤트 루프·동기 함수·차단 호출·스레드), 소제목 「비동기 함수와 코루틴」「이벤트 루프와 gather()」「동기 함수와 차단 호출」「함께 기다린 차례」「걸린 시간과 반환값 목록의 순서」「.py 파일에서는 asyncio.run()」「확인한 범위」, 복습 6문항(4 → 6), 참고 자료 6개(IPython autoawait 포함)
- 그림: Mermaid 5장(코루틴 만들고 기다리기, gather 함께 기다리기 sequenceDiagram, 걸린 시간 비교 gantt, to_thread 차례 sequenceDiagram, Before/After) + 삽화 1장(모래시계 두 개, 1회 생성 통과, 3~11절 좌우 Before/After 구도). 12-3은 챕터에서 처음 쓴 gantt: 첫 렌더에서 줄 이름이 막대와 겹치고 가로축이 `000`·`020`으로 나와 `leftPadding 190`·`tickInterval 100millisecond`·`axisFormat 0.%L초`로 고쳐 다시 렌더. 12-4는 참여자 이름이 상자를 넘어 `<br>`로 줄바꿈. 12-5는 가운데 상자를 「동기 함수 lookup_stock」(초록)으로 이름을 바꿈. 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)
- 동작 근거: Python 3.12.13 설치본 소스 `asyncio/threads.py`(to_thread 「Asynchronously run function func in a separate thread」), `asyncio/tasks.py` gather 설명(「in the order of the original sequence, not necessarily the order of results arrival」, 「not necessarily be scheduled in the same order as passed in」), `asyncio/base_events.py`(기본 실행기 `thread_name_prefix='asyncio'`), `asyncio/runners.py`(「cannot be called when another asyncio event loop is running」). Python 문서 코루틴과 태스크(「simply calling a coroutine will not schedule it to be executed」), asyncio-dev Running Blocking Code, IPython autoawait

## 검토에서 볼 곳

- 새 내용 양: async def·코루틴·await·asyncio.sleep·perf_counter·이벤트 루프·gather·asyncio.run(.py 파일)·동기 함수·차단 호출·스레드·to_thread, 심화 threading. 코드 셀 16개. `asyncio.run()` .py 파일 두 셀(9·10)을 기본 경로에 둔 것이 적절한지(사다리 L7에 asyncio.run이 있고, 뒤 챕터 노트북은 모두 셀의 await를 씀)
- 시간 값(0.3·0.2·0.3)은 `round(..., 1)`로 줄였고 세 번 시험 실행과 노트북 실행 두 번에서 같았음. 느린 컴퓨터에서 반올림 경계를 넘을 가능성은 낮지만 0은 아님. 시간에는 assert를 쓰지 않았고, After assert는 반환값 목록(넣은 순서)만 확인
- gather의 시작 순서(연필 먼저)는 소스 설명상 보장되지 않아 본문 「확인한 범위」에 적음. 출력 줄 차례를 근거로 쓴 Before/After 설명은 이번 실행 관찰로 한정
- 12-3 gantt의 막대는 기본색(회색). 막대 길이는 코드의 초 값이고 실제 측정은 줄 이름에만 있음(캡션에 명시)
- 비유 두 가지: 핵심 개념 삽화는 모래시계(차례로/함께 기다림), 용어 설명은 식당 번호표(코루틴)·주방 냄비(이벤트 루프)·계산대와 포장대(차단 호출·스레드). 비유가 많다고 볼 수 있음
- 삽화: 작은 모래시계가 옆으로 누운 모양으로 「아직 시작 못 함」을 표현. 모래시계 두 개 크기 차이로 0.2초·0.1초를 나타냄

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-B.md`

- 판정 accept-with-fixes(하 3, 공통 C-4). 모두 반영했습니다. 결정: subprocess 유지
- 12-1: 12-3 init에 `'themeCSS': '.tick text { font-size: 15px; }'`(14px는 본문 760px 축소 뒤 13.6px라 `visual.cjs`에 걸림, 작은따옴표는 G7 라벨 숫자 검사를 피하려고). PNG 확인
- 12-2: 「노란 메모 다섯 개 가운데 앞의 네 개는 확인 시작·끝 줄이 찍힌 차례입니다.」
- 12-3: 비유 장소를 주방 하나로(차단 호출 「반죽을 직접 치대는 동안」, 스레드 「옆 조리대의 보조에게 맡기면」). 본문·노트북
- C-4: 노트북 준비 설명 「5·7·8절처럼」
- 검토 밖: `visual.cjs`가 12-4 SVG 글자 13.3px를 잡아 메시지 줄바꿈으로 폭 913 → 850(PNG 확인)
- 새 커널 출력은 반영 전과 같음(걸린 시간 0.3·0.2·0.3). 코드 셀 16, 검사한 문장 386

재실행: `run_section.sh` → 챕터 `upgrade_gates.py --label after --strict` 13/13 PASS(G1~G7 0), `verify.py --chapter` `PASS 13 sections / 190 code cells`, `visual.cjs` 28건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 별도 세션 검토(accept 전), 강사 확인
- 리뷰 묶음: `qa/upgrade/review-pack/12-async와-await.md`
- 챕터 전체 `gates-after.json`, 루트 `textbook/qa/upgrade-progress.md`, `chapter-summary.md`는 13 실습 절까지 마친 뒤
- 다음 학습 링크: 이 절 본문·노트북에 13절 링크 없음. 실습 절을 붙일 때 「다음 학습과 이어지는 지점」과 노트북 정리 셀을 고침
- Windows에서는 실행하지 않음. 노트북 셀에서 `asyncio.run()`을 부르는 장면, 부르기만 하고 버린 코루틴의 경고는 실행하지 않음
- 챕터 index(`_src/index.html`)의 A트랙 보충 과제는 이 절 범위 밖(handoff §10 → §11에 이미 남김)
- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(보고서 끝 「반영 결과」의 볼 곳)가 남음
