# 05-문서-파싱과-스크래핑 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/05-document-parsing.*`, 수정 전 `article-text.json` 사본).
생성기: `qa/upgrade/author_05.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch04-data-tools 05`.
수정 전 게이트는 01절 작업 때 챕터 전체로 남긴 `gates-before.json`(05절 47건)을 씁니다.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 2 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 7 | 0 |
| G6 | 35 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 7 | 13 (준비 1 + 본문 12, 주석 뺀 코드 최대 12줄 = After 호출 셀) |
| 검사한 문장 | 104 | 401 (검토 반영 뒤, `gates-after.json`) |
| 모델 호출 | 0 | 0 (API 키 불필요, 인터넷 접속 없음) |

새 커널 실행 PASS(Linux aarch64, Python 3.12.13, beautifulsoup4 4.15.0, lxml 6.1.3, soupsieve 2.9.2, 2026-09-16 15:04 UTC), `verify.py --chapter` `PASS 5 sections / 78 code cells (max 21 lines)`(21줄은 04절 서버 프로그램 셀, 04 진단의 「개선 전 05절」 표기는 이제 해당 없음), `visual.cjs` 1280·390px PASS(이 절 HTML과 `visual.cjs` 사본을 `/tmp/ch04-05-vis`에서 실행), 실습 폴더 `uv run python -m pytest -q` 10 passed(`data_tools.py`·테스트는 고치지 않음).

## 수정 전 주요 문제

- G1: 준비 셀 `next(path for path in (Path.cwd(), *Path.cwd().parents) if …)`(제너레이터 식·`*` 풀어 넘기기), After 셀 조건 표현식 `… if subtitle_node else None`
- 게이트가 세지 않은 사다리 밖 문법(Ch 1~3 요약 §5, 01~04 handoff): `from pathlib import Path`·`read_text`/`write_text`, `from urllib.robotparser import`(점 경로 import), 딕셔너리 풀기 `{**record, …}`, f-string 안 식 `f"{record['title']}\n{record['summary']}"`, `json.loads`, `soup.builder.NAME`, `article.h1`·`article.time` 속성식 자식 접근, `type(error).__name__`, 한 줄에 여러 칸 딕셔너리, 한 셀에 기사 추출·JSON 쓰기·다시 읽기·검사 몰기
- 01~04절과 이어지지 않음: 준비 셀이 `mkdtemp`/`chdir` 모양이 아님, 「앞에서 배운 내용」이 04절 `json()`·`raise_for_status()`·딕셔너리 목록 반환 함수와 연결하지 않음, 조회 함수로 묶지 않음. 실패 장면이 없는 선택자 `.subtitle`을 기존 페이지에 걸어 보는 인위 조건이라, 왜 요소가 없어지는지(사이트 구조 변경) 설명이 없음
- HTML·태그·요소·속성·파싱·요소 트리·CSS 선택자·robots.txt를 처음 가르치는 절인데 한 단락에 몰아 풀고, 트리 모양을 출력으로 보여 주지 않음
- 준비물에 기준 beautifulsoup4·lxml 버전 없음(규격 §6)
- 「다음 학습」의 「Ch 19에서는 세 가지 조회 함수를 도구로 등록하되 스크래핑 정책 검사는 함수 바깥의 운영 규칙으로도 유지」는 실제 Ch 19 파일과 다름(`part5/ch19-model-tools`의 `_src`·노트북은 `fetch_orders`만 쓰고 `robots`·스크래핑 언급 없음, 2026-09-16 grep)
- G5: 제목 셀·오늘 볼 그림 없음, 결과 읽기가 출력 값을 인용하지 않음. G6: 코드 이름·영문+조사로 시작하는 문장(「`select_one()`은」, 「robots.txt는」, 「Before는」 등) 30건, 70자 초과 3건, 금지어 「돌립니다」 1건, 5문장 넘는 단락 1건. G7: Mermaid 0장, 삽화 0장, 설계표 없음

## Ch 5 전달 파일 `data/article-text.json` — 호환 판단 근거

- 읽는 쪽 확인: `labs/part1/ch05-llm-principles/notebooks/01-토큰화와-한국어-효율.ipynb` 셀 4가 부모 폴더를 올라가며 `labs/part1/ch04-data-tools/data/article-text.json`을 찾고 `handoff["schema_version"]`, `handoff["source"]`, `handoff["record"]["id"]`, `handoff["record"]["text"]`를 읽음. `textbook/qa/run_course_bundle.py`는 압축 해제본에서 이 파일을 **지운 뒤** Ch 4 05 노트북을 `--cwd notebooks`로 실행하고, 새로 생긴 파일이 저장소 파일과 **바이트까지 같은지** assert. `tests/test_data_tools.py`는 `schema_version`·`source`와 `record == parse_article_html(article.html)`을 검사. `_notebook/build_bundle.py`가 배포 목록에 이 파일을 넣음
- 그래서 파일 이름·경로·구조(`schema_version` `ch04-parsed-article-v1`, `source`, `record` 칸 순서 `id`·`title`·`summary`·`published`·`text`)·내용·쓰는 방식(`json.dumps(payload, ensure_ascii=False, indent=2) + "\n"`)을 그대로 두고, 입력 `data/article.html`·`robots.txt`도 고치지 않음
- 확인: 수정 전 SHA-256 `e241854443edac502e0a9e090191ace34dbced1885a600db3af29a20a93103d1`, 노트북 실행 뒤(파일 수정 시각이 바뀜) 같은 값. 커널 cwd 두 경우 모두 확인 — run_section.sh(프로젝트 맨 위 폴더, `labs/…/data` 분기)와 `/tmp` 사본을 `execute.py --cwd labs/part1/ch04-data-tools/notebooks`로 실행(`../data` 분기, bundle 러너와 같은 조건) → 13셀 PASS, 코드 셀 출력 동일, JSON 해시 동일. 파일을 지우고 다시 만드는 실행은 삭제 금지라 하지 않음(노트북은 이 파일을 읽지 않고 새로 씀)
- 01~04절의 임시 폴더 대신 `os.chdir(data 폴더)`로 바꾼 이유: 이 절은 새 연습 파일을 만들지 않고, Ch 5가 읽을 파일을 실습 폴더에 남겨야 함. chdir 뒤 파일 이름만 쓰는 모양은 01~04절과 같음. 준비 셀 설명과 본문 「앞에서 배운 내용」에 이유를 적음
- 데이터를 01~04절 주문(O101~O103)으로 바꾸지 않은 이유: 기사 `A10` 기록이 Ch 5 01 토큰화 입력이라, 바꾸면 Ch 5 출력(`GPT-2`·`KLUE` 토큰 수)과 배포 검증이 깨짐. 본문에 「Ch 5 01절이 이어 받기 때문」이라고 적음

## 바꾼 것

- 노트북(paired 유지, 학습 질문 「HTML 구조에서 필드를 안전하게 추출」과 실패 「없는 선택자 결과에 메서드 호출 → AttributeError」, 수정 「None 확인」 유지): 제목(할 일 3, 호출 0번·1분 이내, 기준 beautifulsoup4 4.15.0·lxml 6.1.3·soupsieve 2.9.2·Python 3.12.13, 설치 정보의 Python 요구 3.7/3.8/3.10 이상, 다른 버전 실행 안 함) → 오늘 볼 그림(05-1) → 1 준비(`os.path.exists("../data/article.html")` 분기 + `os.chdir()`) → 2 robots.txt(`import urllib.robotparser`, 파일 `with open`+`splitlines()`, `RobotFileParser()`·`parse()`·`can_fetch("course-bot", 주소)`, 주소는 시험용 이름 `example.test`) → 3 HTML 글 읽기(270글자 한 줄, 태그·요소·속성) → 4 `import bs4`·`import lxml`·버전·`bs4.BeautifulSoup(html_text, "lxml")`·`prettify()`(요소 트리·자식 요소) → 5 `select_one("article")`·`.name`·`["data-id"]`·`select_one("h1")`·`get_text(strip=True)` → 6 `.summary`·`time` 화면 글 vs `["datetime"]` → 7 값 바꿔 보기 `html_text.replace('class="summary"', 'class="lead"')` → `.summary` 결과 `None`(오류 없음)·`.lead`로는 요약 글 → 8 Before `parse_article_before(html_text) -> dict`, 원래 페이지 기록 4칸·바뀐 페이지 `속성 오류: 'NoneType' object has no attribute 'get_text'`(`try/except AttributeError`) → 9 After `find_text(parent, selector)`(없으면 `찾지 못한 선택자:` 출력 + `None`)·`parse_article(html_text) -> dict`(Before와 두 줄만 다름), 빈 칸 모으기(`items()`+풀어 담기, 원래 `[]`, 바뀐 `['summary']`, `assert`) → 10 `record["text"]` 더하고 `import json`·`json.dumps(…, ensure_ascii=False, indent=2)`·`with open("w")`로 `article-text.json` 쓰기 → 정리
- 가르치지 않은 문법 처리: 위 「사다리 밖 문법」을 모두 뺌. `from bs4 import BeautifulSoup` 대신 01~04절 `pd.read_csv`·`sqlite3.connect`·`httpx.get`처럼 `bs4.BeautifulSoup`. 점 이음 모듈 `urllib.robotparser`는 03절 `sqlite3.IntegrityError`·04절 `httpx.HTTPStatusError`처럼 한 문장으로 풂. `find_text()`는 매개변수 `parent`와 반환에 타입힌트를 적지 않은 이유(요소 자료형 미교육, 글자 또는 None)를 설명 셀에 적음
- 본문 10블록 전체를 다시 씀. 「이 절의 질문」, 용어 9개 표(스크래핑, robots.txt, HTML, 태그와 요소, 속성, 파싱과 파서, 요소 트리, CSS 선택자, class 속성), 비유(나무 상자의 색 스티커 카드와 노란 스티커 쟁반 — 03-5·04-5의 나무 쟁반을 이어 씀), 「앞에서 배운 내용」 4단락(04절 `json()`·`raise_for_status()` 「읽기 전에 확인」, 01·03·04절 딕셔너리 목록 반환 함수와 오류 이름 `try/except`, 주문 데이터 대신 기사 A10을 쓰는 이유, Ch 2 03·04·05절·Ch 1 02·04절). 주의 메모에 실행하지 않은 것(요청 간격, 겹치는 robots 규칙 — Python은 먼저 적힌 줄·RFC 9309는 가장 긴 줄, article·time 요소가 없는 페이지, 없는 속성 KeyError, 다른 파서, Windows·macOS·다른 버전). 복습 5문항
- 「다음 학습」: Ch 5 01 연결만 남기고(노트북 소스로 확인), 확인되지 않은 Ch 19 문장을 뺌. 06 실습 절 링크는 붙이지 않음(다음 단계)
- 그림: Mermaid 4장(요소 트리, 선택자로 값 읽기, 바뀐 페이지 비교, Ch 5에 넘길 파일) + 삽화 1장(스티커 쟁반). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)
- 라이브러리 동작 확인(설치본 `/tmp/venv-ch04-data-tools`): beautifulsoup4 4.15.0 METADATA `Requires-Python >=3.7.0`, lxml 6.1.3 `>=3.8`, soupsieve 2.9.2 `>=3.10`. `bs4/css.py` `select_one() -> element.Tag | None`, `element.py` `get_text(strip=True)`는 글자 조각마다 앞뒤 공백을 지우고 이어 붙임, `Tag.__getitem__`은 `self.attrs[key]`(없으면 KeyError, 실행 안 함). Python 3.12 `urllib/robotparser.py` `can_fetch()`는 규칙을 읽기 전이면 `False`, 읽은 뒤에는 네트워크 없이 `Entry.allowance()`가 먼저 맞는 줄을 반환. RFC 9309 §2.2.2 「most specific match … most octets」, Beautiful Soup 문서 「Differences between parsers」(2026-09-16 WebFetch)

## 그림 확인

- PNG 네 장을 직접 열어 확인. 05-1 TB: 초록 파일 → 회색 바깥 요소(html·body·main, 처음 렌더의 `head`는 기사를 감싸지 않아 뺌) → 초록 article(A10) → 아래 줄 초록 h1·p·time(viewBox 785). 05-2 TB: 초록 soup·article·time, 노랑 제목·요약·화면 글·속성 값, 화살표 라벨에 코드(viewBox 763, ID를 따로 뺀 시안은 949라 되돌림). 05-3: Before 칸 위·After 칸 아래, 칸 안 왼쪽 → 오른쪽, 빨강은 Before 결과 하나(viewBox 837). 05-4 TB: 노랑 빈 칸 `[]` → 파랑 text 칸 더하기 → 초록 JSON 파일 → 점선 회색 Ch 5 01(viewBox 273)
- 색 판단(검토 대상): 05-3 Before의 AttributeError는 노트북이 `try/except`로 받아 출력했지만, 함수가 기록을 반환하지 못하고 멈춘 결함 결과라 규격 §5-3 「Before 결함 결과」로 빨강. 7절 `None`은 오류가 아닌 반환값이라 빨강을 쓰지 않음
- 삽화 05-5(스티커 쟁반): 1회 생성 job `07413a99-9326-49f5-af2c-eb79c433f6f0` 채택, 2크레딧(잔액 2906 → 2904). 저장 PNG(1100×614)를 기기에서 다시 받아 job 결과(2752×1536)를 같은 폭으로 줄인 것과 대조해 픽셀 차이 0. 저장 파일을 열어 그림 읽기·캡션(왼쪽 상자 초록·파랑 카드, 쟁반 위 노란 스티커 카드 / 오른쪽 상자 초록·보라·파랑 카드, 빈 쟁반)과 맞는지 확인

## 빌드에서 걸린 것

- 노트북 설명 셀에 `<h1>`·`<p class="summary">`를 백틱으로 인용하면 `textbook/_notebook/render.py`의 `markdown()`이 「HTML 호환 마크다운」으로 보고(`<(?:p|h[1-6]|ul|ol|div|table|details)\b`) 셀 전체를 변환 없이 넣어, HTML에 실제 `<h1>` 태그가 생김(첫 빌드에서 확인). 공용 도구는 고치지 않고, 해당 네 셀의 인용을 `<article …>`·`<time …>`(검사식에 걸리지 않음)과 「제목 태그 h1」 같은 말로 바꿈. 뒤 챕터에서 HTML 태그를 노트북 설명에 인용할 때 같은 주의가 필요함

## 검토에서 볼 곳

- 준비 셀이 임시 폴더 대신 실습 폴더 `data`로 `chdir`하고, 경로를 `../data` 있으면 그대로·없으면 `labs/part1/ch04-data-tools/data`로 고르는 방식(`os.path.exists` 한 문장 설명). 노트북이 실습 폴더 파일을 다시 쓰는 점
- 05-3 Before 결과 빨강(위 색 판단), After 함수가 제목·요약 두 칸만 확인하는 범위(주의 메모에 한정)
- 비유 삽화의 대응(쟁반 앞 노란 스티커 = 선택자, 빈 쟁반 = None)이 그림만 보고 읽히는지

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept(하 2, 공통 C-2·C-5). 모두 반영했습니다. Q5 권고대로 `data` 폴더 방식과 05-3 Before 빨강은 유지
- 05-1: After 호출 셀 `assert` 앞 주석 「반복이 끝나면 empty_keys에는 마지막 페이지(바뀐 페이지)의 빈 칸이 남습니다」, 결과 읽기 「검사 줄 `assert`는 마지막으로 모은 바뀐 페이지의 빈 칸이 `['summary']`인지 확인했고, 멈추지 않았습니다.」
- 05-2: 10번 결과 읽기 「작업 기록에서 파일 내용의 지문 값(SHA-256)을 비교하니, 실행 전과 바이트까지 같았습니다. 노트북 안에서 다시 읽어 비교하지는 않았습니다.」(괄호 뒤 마침표를 피해 문장 순서를 바꿈), 본문 b7 여덟째 항목 끝 「Windows에서는 줄바꿈 글자가 달라 파일이 바뀐 것으로 보일 수 있고, 이 경우는 실행하지 않았습니다.」
- C-2: `print("HTML 글:")`·`print("트리 글:")`·`print("JSON 글:")`. 결과 읽기는 줄 위치를 쓰지 않아 그대로
- `data/article-text.json` SHA-256: 반영 전 `e241854443edac502e0a9e090191ace34dbced1885a600db3af29a20a93103d1` → 05 재실행(16:17:58에 다시 씀)·06 재실행·pytest 뒤 같은 값
- C-5: 게이트 표 검사한 문장을 `gates-after.json` 401로 맞춤. 코드 셀 13

재실행: 생성기 `author_05.py` 수정 → `run_section.sh … 05`(새 커널 PASS). 코드 셀 출력은 새 라벨 줄·임시 경로·포트를 빼고 반영 전과 같습니다. 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0, `qa/upgrade/gates-after.json`), `verify.py --chapter` `PASS 6 sections / 96 code cells (max 21 lines)`, `visual.cjs` 14건 PASS, 실습 폴더 pytest 10 passed. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 검토 1차 반영 완료(2026-09-16). 강사 확인과 2차 검토(`review-round1.md` 끝 「반영 결과」의 볼 곳)가 남음
- 리뷰 묶음: `qa/upgrade/review-pack/05-문서-파싱과-스크래핑.md`
- 정리 대상(삭제하지 않고 목록만): `figures/05-document-parsing.excalidraw`·`.svg`(옛 도식, 본문에서 뺌), `/tmp/ch04-05-vis`(화면 검사 사본)
- 실습 폴더 `data_tools.py`의 `parse_article_html()`(bs4 `from import`, 조건 표현식, `raise ValueError`)은 노트북 함수 `parse_article()`과 이름·모양이 다름. 01·03·04절과 같은 상황이라 고치지 않음(주의 메모에 적음)
- 06 실습 절, 「다음 학습」 링크 교체, 챕터 `chapter-summary.md`
