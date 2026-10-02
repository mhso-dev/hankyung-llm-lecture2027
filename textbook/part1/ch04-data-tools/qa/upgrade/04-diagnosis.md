# 04-REST와-페이지네이션 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/04-rest-pagination.*`).
생성기: `qa/upgrade/author_04.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch04-data-tools 04`.
수정 전 게이트는 01절 작업 때 챕터 전체로 남긴 `gates-before.json`(04절 50건)을 씁니다.

작업 경과: 같은 날 앞선 작업 세션이 생성기·본문·그림·삽화·review-pack(14:03~14:21)까지 만들고 진단·인계 기록 전에 멈췄습니다. 이 세션이 그 결과를 규격·앞 챕터 요약·01~03 handoff와 대조해 검토하고, 본문 한 단락(Ch 1 05절 연결)을 고친 뒤 새 커널부터 다시 실행해 마감했습니다.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 6 | 0 |
| G2 | 3 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 7 | 0 |
| G6 | 31 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 6 | 13 (준비 4 + 본문 9, 03절 20개보다 7개 적음) |
| 검사한 문장 | 107 | 359 (검토 반영 뒤, `gates-after.json`) |
| 모델 호출 | 0 | 0 (API 키 불필요, 인터넷 접속 없음) |

새 커널 실행 PASS(Linux aarch64, Python 3.12.13, httpx 0.28.1, 2026-09-16 14:28 UTC), `verify.py --chapter` `PASS 5 sections / 72 code cells (max 21 lines)`(21줄은 개선 전 05절), `visual.cjs` 1280·390px PASS(이 절 HTML과 `visual.cjs` 사본을 `/tmp/ch04-04-vis`에서 실행해 `_notebook/checks/`를 건드리지 않음), 실습 폴더 `uv run python -m pytest -q` 10 passed(`data_tools.py`·테스트는 고치지 않음).

## 수정 전 주요 문제

- G1·G2: 준비용 서버 `class Handler(BaseHTTPRequestHandler)` 상속·`do_GET`·`log_message(self, format, *args: object)`(클래스 정의·`*args`), 셀 15줄 초과 두 곳, 목록 내포식 네 곳(`[item["id"] for item in …]`), 메서드 이어 부르기 `httpx.get(...).json()`
- 게이트가 세지 않은 사다리 밖 문법(Ch 1~3 요약 §5, 01~03 handoff): `threading.Thread(target=…, daemon=True)`·`ThreadingHTTPServer`·`server.shutdown()`/`thread.join()`, `from http.server import`(점 경로 import), f-string 안 속성 접근 `{server.server_port}`, 타입힌트 `list[dict]`·`int | None`·키워드 전용 `*`·변수 타입힌트 `items: list[dict] = []`, `try/finally`(Ch 2 09절 B 트랙), `httpx.Client`, `items.extend()`, `payload.get()`, 한 줄 딕셔너리 `pages = {1:{…},2:{…}}`
- 01~03절과 이어지지 않음: 데이터가 기사 A01·A02·A03(주문 O101~O103·합계 77000이 아님), 준비 셀이 `mkdtemp`+`chdir` 모양이 아님, 「앞에서 배운 내용」이 한 단락이고 03절 `find_customer_orders()`·「빈 목록은 입력이 이상했는지 알려 주지 않음」과 연결하지 않음. `async`는 Ch 2 12절에서 배웠는데 「아직 선수 개념으로 사용하지 않습니다」라고 적음
- HTTP를 처음 가르치는 절인데 요청·응답·상태 코드·헤더·JSON·쿼리 매개변수를 한 단락에 몰아 풀고, 상태 코드 확인(`raise_for_status()`)을 성공 응답에서만 실행해 무엇을 막는지 출력으로 보이지 않음
- G5: 제목 셀·오늘 볼 그림 없음, 결과 읽기 셀이 출력 값을 인용하지 않음
- G6: 70자 초과 문장·코드 이름+조사로 시작하는 문장(「`do_GET`은」, 「`json`은」, 「`threading`은」) 31건
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. 기존 Excalidraw 도식 1장
- 준비물에 기준 httpx 버전 없음(규격 §6)

## 연습용 서버를 어떻게 바꿨는가 — 판단 근거

학습 목표는 「요청 주소·쿼리 문자열·상태 코드·JSON 본문을 읽고, 다음 페이지 번호가 빌 때까지 요청하는 함수」입니다. 서버 구현은 목표가 아닙니다. 외부 인터넷 API는 재현성 때문에 쓰지 않습니다. 네 방법을 비교했습니다.

| 방법 | 쿼리 문자열 `?page=` | 실제 HTTP | 학생이 읽을 코드 | 판단 |
|---|---|---|---|---|
| 기존: `BaseHTTPRequestHandler` 상속 + `threading` | 됨 | 됨 | 클래스 상속·`*args`·스레드(A 트랙 미교육, 규격 §2-3 준비용 상속 금지) | 뺌 |
| `python -m http.server`로 파일 폴더 제공 | **안 됨**(쿼리 문자열을 무시하고 경로만 봄) | 됨 | 없음 | 쿼리 문자열 학습과 페이지 404가 흐려져 뺌 |
| `httpx.MockTransport(함수)` | 됨 | **아님**(네트워크 없이 함수가 응답) | `httpx.Client(transport=…)` — 실제 서비스 호출 코드와 모양이 달라짐 | 뺌 |
| **채택**: 준비 셀이 쓴 `order_server.py`(표준 라이브러리 `wsgiref`의 함수 하나)를 `subprocess.Popen()`으로 따로 실행 | 됨(`QUERY_STRING` → `page=1.json`) | 됨(포트 0 → 서버가 알린 포트) | 노트북 코드에는 클래스·스레드 없음. 서버 글은 `"""…"""` 문자열이라 기본 경로 문법 검사 대상이 아님 | 채택 |

- 준비 셀 4개(`lesson_role="setup"`): ① 임시 폴더(01~03절 모양) ② 페이지 글 파일 두 개 `page=1.json`·`page=2.json`(`with open("w")`) ③ 서버 프로그램 파일 `order_server.py`(`with open("w")`) ④ `subprocess.Popen([sys.executable, "order_server.py"], stdout=PIPE, stderr=DEVNULL, text=True)` + 첫 줄 포트 읽기. 2절 앞 설명에 「**연습용 서버를 켜는 준비 코드**이며, 줄마다 읽지 않아도 됩니다」와 서버(server) 한 문장 정의를 둠
- 이어짐: Ch 2 08절 `subprocess.run()`(끝날 때까지 기다림)과 `Popen()`(켜 두고 넘어감)을 한 문장으로 대비. 서비스 끄기는 마지막 셀 `terminate()`·`wait()`·`poll() is None` → `False`
- 파일 서버라 서버가 계산하지 않음: 요청 page 값과 파일 이름이 맞으면 그 글, 아니면 404 `{"error": "not found"}`. 이 덕분에 페이지 3 요청으로 실제 404를 재현
- 포트 0(운영체제가 고름)이라 고정 포트 충돌이 없고, 출력의 포트 번호는 실행마다 달라 결과 읽기에서 인용하지 않음(`http://127.0.0.1:`까지만)

## 바꾼 것

- 노트북(paired 유지, 학습 질문 「여러 페이지 목록을 언제까지 읽어야 하는가」와 첫 페이지 2건 → next_page None까지 3건 유지): 제목(할 일 3, 호출 0번·1분 이내, 기준 httpx 0.28.1·Python 3.12.13·httpx 요구 Python 3.8 이상·다른 버전 실행 안 함) → 오늘 볼 그림(04-1) → 1 준비(`mkdtemp(prefix="ch04-04-")`) → 2 연습용 서비스 켜기(준비 3셀) → 3 `import httpx`·`httpx.__version__`·`httpx.get(orders_url, params={"page": 1}, timeout=2.0)`·`response.url`·`status_code` 200 → 4 `response.text`·`response.json()`·`<class 'dict'>`·주문 수 2·다음 페이지 번호 2(페이지네이션 정의) → 5 값 바꿔 보기 page 2(`null` → `None`, O103) → 6 없는 page 3 → 404 + `raise_for_status()`를 `try/except httpx.HTTPStatusError`로 받음(03절 `sqlite3.IntegrityError` 점 이음 모양) → 7 Before `fetch_orders_before(orders_url) -> list`(첫 페이지만) 2건·50000 → 8 After `fetch_all_orders(orders_url) -> list`(`while page is not None` + `for`+`append()` + `page = body["next_page"]`) 3건·77000·`assert` → 9 서비스 끄기 → 정리
- 데이터: 01~03절 주문 O101(C001, 32000)·O102(C002, 18000)·O103(C001, 27000)을 한 페이지 두 건으로 나눔. Before 합계 50000 = 77000 − O103 27000
- 가르치지 않은 문법 처리: 상속·`threading`·`from http.server import`·`list[dict]`·`int | None`·`*`·변수 타입힌트·내포식·`try/finally`·`httpx.Client`·`extend()`·`.get()`·메서드 이어 부르기·f-string 안 속성 접근을 뺌. 주소는 Ch 3에서 쓴 글자 `+`(`base_url + "/orders"`), 서비스 주소만 변수 넣은 f-string `f"http://127.0.0.1:{port_text}"`
- 본문 10블록 전체를 다시 씀. 「이 절의 질문」, 용어 9개 표(HTTP, 요청과 응답, 서버와 포트, 쿼리 문자열, 상태 코드, JSON, REST API, 페이지네이션, 시간 제한), 비유(창고 창구와 깃발 꽂힌 쟁반 — 03-5 쟁반·서류철을 이어 씀), 「앞에서 배운 내용」 5단락(03절 `find_customer_orders()`와 딕셔너리 목록, 03절 「오류 없이 덜 가져온 결과」, 01~03 주문·77000, Ch 2 02·03·04·05·08절, Ch 1 05절 클라이언트·서버), 주의 메모에 실행하지 않은 것(다른 페이지 방식, 같은 다음 페이지 번호 반복, `httpx.Client`, 시간 제한 초과, 5xx, 준비 셀 여러 번 실행·커널 재시작, Windows·macOS·다른 httpx 버전). 복습 5문항
- 이 세션에서 고친 문장: 「앞에서 배운 내용」의 「Ch 1 05절에서는 Docker 명령(클라이언트)이 따로 켜진 프로그램(데몬)에 일을 요청했습니다」 → 「Docker 도구를 명령을 입력하는 클라이언트와, 요청을 받아 일하는 서버(데몬)로 나눠 보았습니다」. Ch 1 교재 출력 환경에는 docker가 없어(Ch 1 요약 §3) 요청이 실제로 오간 장면을 보지 않았기 때문
- 그림: Mermaid 4장(끝까지 읽는 순서, 요청과 응답, 페이지 번호 바꾸기, 한 페이지 비교) + 삽화 1장(깃발 쟁반). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)
- 라이브러리 동작 확인(설치본 `/tmp/venv-ch04-data-tools`): httpx 0.28.1 `Requires-Python: >=3.8`, `_config.py` `DEFAULT_TIMEOUT_CONFIG = Timeout(timeout=5.0)`(인자 없는 요청 5초), `_models.py` `raise_for_status()`는 `is_success`(200번대)가 아니면 `HTTPStatusError`, 메시지 `{error_type} '{status_code} {reason_phrase}' for url …` + MDN 링크 줄(노트북 출력과 일치). HTTPX Clients 문서의 「experimentation, one-off scripts, or prototypes가 아니면 Client」 권고. 실습 `data_tools.py` `fetch_articles()`의 `seen_pages`로 반복 페이지 `ValueError`(주의 메모 근거)

## 그림 확인

- PNG 네 장을 직접 열어 확인(이 세션). 04-1 sequenceDiagram은 `messageAlign: left`로 라벨이 세로선과 겹치지 않고, 요청 실선·응답 점선, 메모 노랑(viewBox 585). 04-2 TB 초록 두 개·노랑 두 개, 화살표 라벨 `httpx.get()`·`response.json()`(viewBox 239). 04-3은 page=1 → 2 줄이 왼쪽, page=3 줄이 오른쪽에 떨어져 본문 「왼쪽 줄/오른쪽 줄」과 맞음(viewBox 431). 04-4는 Before 칸 위·After 칸 아래, 칸 안은 왼쪽 → 오른쪽, 빨강은 Before 결과 상자 하나(viewBox 741, 868 이하)
- 404 상자(04-3)는 `try/except`로 받아 출력한 오류라 노랑(규격 §5-3). 빨강은 04-4 Before 결과에만
- 삽화 04-5(깃발 쟁반): 1회 생성 job `d55f7a01-cea2-4d66-ad48-f3f63b1dc3ab` 채택, 2크레딧(잔액 2908 → 2906). 이 세션에서 job 결과(2752×1536)를 다시 받아 저장 PNG(1100×614) 크기로 줄여 대조해 픽셀 차이 0을 재확인. 저장 파일을 열어 그림 읽기·캡션(왼쪽 창구 안에 초록 서류철 쟁반이 남음, 오른쪽 창구가 비고 깃발 있음·없음 두 쟁반)과 맞는지 확인

## 검토에서 볼 곳

- 준비 셀의 서버 방식(위 판단 근거 표). 특히 `subprocess.Popen()`·`stdout=subprocess.PIPE`·`readline()`을 「줄마다 읽지 않아도 됩니다」로 둔 수준이 A 트랙 학생에게 충분한지, 서버 글 안의 `or not os.path.exists()`·`b'…'`를 주석만으로 둔 것
- 준비물 기준 버전 표기: httpx 교재 출력 0.28.1·요구 Python 3.8 이상만 적음. httpx 코드가 쓰는 API(`get`의 `params`·`timeout`, `raise_for_status`, `json`)의 최소 httpx 버전은 확인하지 않음
- 상태 코드 확인을 Before·After 함수 모두에 넣어, Before의 결함을 「페이지를 따라가지 않음」 하나로 좁힌 설계(두 함수의 차이는 반복·모으기 줄뿐)

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept(하 5). 모두 반영했습니다.
- 04-1: 본문 b1 셋째 목표 「…다음 페이지 번호를 따라 반복하도록 고칠 수 있습니다.」
- 04-2: 노트북 「오늘 볼 그림」 「첫 노란 메모는 다음 요청에 넣을 페이지 번호이고, 마지막 노란 메모는 반복이 끝난 뒤의 결과입니다.」
- 04-3(Q4 권고: 준비 셀 방식 유지): 준비 3번 설명에 「인자 `stdout=subprocess.PIPE`는 서비스가 출력한 글을 이 노트북이 읽을 수 있게 이어 둡니다. 메서드 `readline()`은 그 글에서 한 줄을 읽습니다.」(G6 단락 5문장 상한 때문에 따로 단락)
- 04-4: 7번 설명 「이런 함수가 에이전트 도구가 되면, 모델은 함수가 반환한 목록을 보고 답을 만듭니다.」
- 04-5: 용어 표 시간 제한 「응답을 기다릴 때 단계마다 둘 최대 시간. 넘으면 기다리기를 멈춥니다」. 같은 사실 오류가 있던 4번 설명 「`timeout=2.0`은 응답을 최대 2초까지 기다린다」도 「연결하기와 응답 읽기 같은 단계마다 최대 2초까지」로 함께 고침(보고서 밖). 준비물 기준 버전에 「실습 폴더의 `uv.lock`이 httpx를 0.28.1로 고정하므로, `uv sync --locked`로 만든 환경에는 이 버전이 설치됩니다.」「다른 버전과 httpx 1.0 개발판은 이번에 실행하지 않았습니다.」(`uv.lock` 194~195행 확인, 따로 단락)
- 코드 셀 13, 검사한 문장 359

재실행: 생성기 `author_04.py` 수정 → `run_section.sh … 04`(새 커널 PASS). 코드 셀 출력은 새 라벨 줄·임시 경로·포트를 빼고 반영 전과 같습니다. 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0, `qa/upgrade/gates-after.json`), `verify.py --chapter` `PASS 6 sections / 96 code cells (max 21 lines)`, `visual.cjs` 14건 PASS, 실습 폴더 pytest 10 passed. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(`review-round1.md` 끝 「반영 결과」의 볼 곳)가 남음
- 리뷰 묶음: `qa/upgrade/review-pack/04-REST와-페이지네이션.md`(이 세션에서 다시 만듦)
- 정리 대상(삭제하지 않고 목록만): `figures/04-rest-pagination.excalidraw`·`.svg`(옛 도식, 본문에서 뺌), `/tmp/ch04-04-proto`(앞선 세션의 서버 시험 폴더)·`/tmp/ch04-04-vis`(화면 검사 사본)
- 실습 폴더 `data_tools.py`의 `fetch_articles(base_url, *, category, timeout, client)`(기사 `/articles`, `httpx.Client`, 반복 페이지 검사)는 노트북 함수 `fetch_all_orders()`와 이름·데이터·모양이 다름. 01절 `fetch_orders`·03절 `find_customer_orders`와 같은 상황이라 고치지 않음(주의 메모에 적음)
