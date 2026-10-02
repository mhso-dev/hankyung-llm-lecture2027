# Ch 10 문서 처리 — 절 사이 인계

절 작업자가 다음 절 작업자에게 넘기는 기록입니다. 앞 내용: `textbook/qa/upgrade-course-summary.md`(Part 1·Part 2 절), 같은 Part 앞 챕터 요약 `textbook/part3/ch09-rag-first-run/qa/upgrade/chapter-summary.md`(§5 Ch 10 인계). 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md`.

## §01 → §02

(01절 품질 개선 2026-09-18. 결과는 `01-diagnosis.md`, 게이트 G1~G7 0(수정 전 G5 9·G6 25·G7 3 = 37), 코드 셀 18(준비 2), 검사 문장 306(검토 반영 뒤 게이트 값. 절 작업 기록 296은 틀렸습니다), **서비스 요청 0번**(모델·임베딩 없음, API 키 없이 실행), 새 커널 두 번 실행해 출력 같음(교재 출력은 마지막 실행 2026-09-18T01:49:37Z). 챕터 첫 절이라 `gates-before.json`은 8절 전체 수정 전 기록(G1 22·G2 9·G3 16·G4 0·G5 86·G6 206·G7 24 = 363). 삽화 01-5 채택(2차 job `97390942-…`, 4크레딧, 잔액 2808), Mermaid 4장)

### 빌더 변경과 02~08 작업자가 쓸 토큰 모양 (먼저 읽을 것)

- **`_build.py`를 고쳤습니다**(챕터 파일만, 공용 `_template`·`_notebook`은 그대로). 옛 사본 `qa/upgrade/before/_build.before-upgrade.py`. 절 목록은 `SECTIONS` 하드코딩이고 `chapter.json`은 없습니다. 실습 절 09를 붙일 때 `SECTIONS`에 주제까지 넣은 제목 한 줄(규격 §7-2), `render_index()`의 「개념 8절」, `_src/index.html` 절 표, `textbook/part3/_build_index.py` `CHAPTERS`의 ch10 절 수 칸(8 → 9, 강의 시수 8은 그대로)을 함께 고칩니다.
- **토큰 모양**(`_src`에 이대로 씁니다)
  - `{{notebook:slug|example}}`·`{{notebook:slug|failure}}`(paired) 또는 `{{notebook:slug}}`(experiment) — 공용 `render.expand_notebooks`, 개선 전부터 동작. 02~07 개선 전 노트북은 `lesson_part` before/after가 있는 paired, 08은 그 절 작업자가 노트북 메타데이터 `lesson_format`으로 확인
  - `{{mermaid:이름|alt|캡션}}` — `figures/이름.svg`를 `<figure class="mmd">`로 넣고 캡션을 붙입니다. `_src`에서 `<figure>`로 감싸지 않습니다. alt·캡션에 `|`·`}` 금지
  - `{{img:이름|alt|캡션}}` — 삽화 PNG를 폭 1100px JPEG `<figure class="illustration">`로. `_src`에서 `<figure>`로 감싸지 않고 바로 아래에 「그림 읽기」 단락
  - 옛 두 칸 `{{img:이름|캡션}}`은 개선 전과 같은 `<img alt>`(하위 호환, 2026-09-18 기준 사용처 0), 옛 `{{svg:이름}}`·`{{code:파일#함수}}`·`{{output:파일}}`도 그대로 동작합니다. **02~08 개선 전 `_src`는 아직 `{{svg:0N-…}}`을 씁니다** → 개선할 때 `{{mermaid:}}`로 바꾸고 옛 SVG·Excalidraw는 지우지 않습니다
  - 치환 뒤 `\{\{[a-z]+:` 모양이 남으면 `ValueError: <slug>: 치환하지 못한 토큰`으로 빌드가 멈춥니다
  - **Ch 9와 같은 점**: 이 챕터 CSS에도 `figure svg{width:100%;min-width:760px}`가 있어 `inline_mermaid()`만 SVG 인라인 style에 `min-width:0`을 더합니다(CSS는 그대로라 다른 절 HTML 불변). 그 밖의 출력은 `_template/builder.py`와 문자열까지 같습니다
- **빌더 확인 방법**: (a) 고치기 전 디스크 HTML 9개 해시(`/tmp/ch10-01/hash/disk-before.txt`), (b) `_build.py`만 고친 뒤 다시 빌드 → 9개 해시 **모두 같음**, (c) 01 본문을 새로 쓴 뒤 → **01만 달라짐**, (d) `grep -c "{{" *.html` 0건. 02~08 작업 전후에 `cd textbook/part3/ch10-document-processing && sha256sum *.html`로 다른 절 HTML이 바뀌지 않았는지 보세요. 01 뒤 기준: `/tmp/ch10-01/hash/final.txt`
- **verify**: `run_section.sh`는 `chapter.json`이 없으면 verify를 건너뜁니다. 따로 실행하세요.
  `UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch10-document-processing uv run --project labs/part3/ch10-document-processing python textbook/_notebook/verify.py --chapter textbook/part3/ch10-document-processing`
  → 01 뒤 `PASS 8 sections / 77 code cells (max 24 lines)`(01절 전 66). `visual.cjs`는 `/tmp` 사본으로(아래 실행 환경).
- **게이트·mdpatch·pack**: `upgrade_gates.py`·`mdpatch.py`·`pack.py`는 `chapter.json` 없이 `_src/NN-*.html`·`labs/part3/ch10-document-processing`으로 동작합니다(01에서 확인). 게이트는 `--section NN`으로 돌립니다.

### 용어 (01에서 정한 것, 02~08도 같게)

- **Ch 9 뜻 그대로 이어 씁니다**: 문서 청크(한정어 없는 「청크」 금지), 색인, 벡터스토어, top-k 검색, 검색 점수, 문서 청크 크기, 겹침, 끊을 자리 순서, 색인 이름표, Document(`page_content`·`metadata`), 출처 표시 `[E01 p.2]`, 메타데이터. **「조각」은 Ch 5 토큰 뜻 전용**, 「스트림 청크」는 Ch 6 04 뜻입니다.
- **01이 새로 정한 말 네 개**(본문 b4 용어 표): **파서(parser)**, **파일 형식(file type)**, **출처 기록**(다섯 칸 딕셔너리), **출처 계보(provenance)**.
- **다섯 칸 이름**: `doc_id` · `source` · `file_type` · `parser` · `page`. 실습 폴더 `document_processing.py` `normalize_metadata()`가 만드는 칸과 같습니다. 02~04절이 형식마다 로더를 쓸 때 이 칸 이름을 그대로 쓰세요(모듈은 `row`·`section` 같은 칸을 더 붙입니다).
- **`parser` 값 이름**: `pypdf-plain`(01에서 씀). 모듈 `load_pdf(mode=)`가 쓰는 `pypdf-plain`·`pypdf-layout`, `pdfplumber`, `python-docx`, `beautifulsoup`, `csv.DictReader`, `zip-xml`과 같은 글로 맞추세요.
- 정의를 `<dl class="term">`으로 쓰면 `</dd>`가 단락을 나누지 않아 G6가 한 단락 12문장으로 셉니다. **Ch 9 01절처럼 용어 표(`<table>`)로 쓰세요**(표는 G6 대상 밖).
- 쓰지 않은 말: 「출처 태그」(→ 출처 표시), 「문맥」·「프롬프트」, 「스키마」(→ 칸 이름), 「정규화」(→ 같은 칸으로 맞추기), 「필드」(→ 칸).

### 01에서 새로 가르친 것

- **API·동작(노트북에서 실행한 것만)**: `os.listdir(경로)`, `sorted(목록)`, `from pathlib import Path`·`Path(경로 글)`·속성 `name`·`stem`·`suffix`·`type(객체).__name__`, `PdfReader(경로)`·`reader.pages`·`page.extract_text()`·**`page.extract_text(extraction_mode="layout")`**, `Document(page_content=, metadata=)`, `딕셔너리.keys()`, 글 `replace(".", "")`·`lower()`.
- **Python 모양**: 후보 경로 `for`+`break`(Ch 8 06·Ch 9 01 모양, 이번에는 **프로젝트 맨 위**를 고름), 글 `+`로 경로 만들기, 함수가 딕셔너리 반환(`make_source_record`, 본문 6줄), 여러 줄 딕셔너리 리터럴, `len(a) - len(b)`. 쓰지 않은 것: `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·try·`raise`·`with`·`+=`·`enumerate`·`zip`·`sum`·`max`·`any`·`all`·`join`·`isinstance`·f-string 안 계산·타입힌트·`@`·`BaseModel`·모델 문장 `assert`.
- **이어 쓸 이름과 값**: `candidates = [".", "../../..", "../../../.."]`·`root_path`(교재 출력 `.`), `corpus_path`·`fixtures_path`, `tier_names = ["easy", "medium", "hard", "scanned"]`, `pdf_path`(= `corpus_path + "/pdf/easy/E01.pdf"`), `load_pdf_pages(pdf_path, doc_id)`·`pages`(Document 5개, 메타데이터 `{'doc_id': 'E01', 'page': N, 'source': 'E01.pdf'}`), `reader`·`plain_text`(905자·26줄)·`layout_text`(1396자·51줄)·`plain_lines`·`layout_lines`, `closure_sentence = "정기 휴관일입니다"`, `three_key_metadata`, `pdf_path_object`, `make_source_record(file_path, page, parser)`, `page_two_record`·`page_three_record`, `make_source_mark(chunk)`, `page_two_document`·`page_three_document`, `selected_index = 1`·`wrong_record`·`wrong_document`·`page_number`·`fixed_record`·`fixed_document`.
- **출력 라벨(전부)**: 「pypdf:」「langchain-core:」「프로젝트 맨 위를 찾았는가:」「고른 경로:」「폴더 | PDF 수:」「견본 파일 | 확장자:」「Document 수:」「2쪽 메타데이터:」「2쪽 본문 글자 수:」「기본 읽기 글자 수:」「기본 읽기 줄 수:」「레이아웃 읽기 글자 수:」「레이아웃 읽기 줄 수:」「기본 읽기에 있는가:」「레이아웃 읽기에 있는가:」「기본 읽기에서 「휴관」이 든 줄:」「레이아웃 읽기에서 「휴관」이 든 줄:」「세 칸 기록:」「두 읽기의 본문이 같은가:」「두 본문의 글자 수 차이:」「이 기록에 읽은 방법을 적는 칸이 있는가:」「경로 객체의 자료형:」「name:」「stem:」「suffix:」「출처 기록:」「기록의 칸 이름:」「Ch 9 세 칸보다 늘어난 칸 수:」「본문 글자 수:」「메타데이터 칸 수:」「출처 표시:」「2쪽 출처 표시:」「3쪽 출처 표시:」「2쪽 기록의 쪽 번호:」「3쪽 본문 글자 수:」「고른 목록 자리:」「기록한 쪽 번호:」「1쪽 본문 글자 수:」「출처 표시와 본문이 같은 쪽인가:」「Ch 9 로더가 적은 쪽 번호:」
- **실행값(2026-09-18 두 번째 새 커널, 두 번 같음)**: `pypdf: 6.18.0`·`langchain-core: 1.6.2`, `고른 경로: .`, `easy | 6`·`medium | 6`·`hard | 6`·`scanned | 3`, 견본 다섯 줄(`.hwp`·`.hwpx`·`.csv`·`.docx`·`.html`), `Document 수: 5`·`2쪽 본문 글자 수: 905`, `기본 읽기 글자 수: 905`·`줄 수: 26`·`레이아웃 읽기 글자 수: 1396`·`줄 수: 51`, `기본 읽기에 있는가: False`·`레이아웃 읽기에 있는가: True`, 기본 읽기 줄 `매주 월요일은 정기 휴관일 입니다. …`·레이아웃 줄 `매주 월요일은 정기 휴관일입니다. …`, `두 본문의 글자 수 차이: 491`, `PosixPath`·`E01.pdf`·`E01`·`.pdf`, `{'doc_id': 'E01', 'source': 'E01.pdf', 'file_type': 'pdf', 'parser': 'pypdf-plain', 'page': 2}`·`늘어난 칸 수: 2`, `메타데이터 칸 수: 5`·`출처 표시: [E01 p.2]`, `3쪽 출처 표시: [E01 p.3]`·`3쪽 본문 글자 수: 925`, Before `기록한 쪽 번호: 1`·`[E01 p.1]`·`본문 글자 수: 905`·`1쪽 본문 글자 수: 45`·`False`, After `2`·`[E01 p.2]`·`True`·`Ch 9 로더가 적은 쪽 번호: 2`.
- **E01 PDF 읽기 결과(02절이 쓸 값)**: pypdf 6.18.0 기본 읽기 쪽별 글자 수 `45 · 905 · 925 · 871 · 270`, 줄 수 `5 · 26 · 25 · 26 · 9`, 빈 줄 없음, 마지막 줄은 쪽 번호. 레이아웃 읽기 글자 수 `144 · 1396 · 978 · 1304 · 369`, 2쪽 줄 수 51, 빈 줄 있음, 쪽 끝 쪽 번호 앞에 빈 줄 여러 개. 기본 읽기는 낱말 사이에 빈칸이 끼어듭니다(`정기 휴관일 입니다`·`규모 이며`·`메이커 스 페이스`). **Ch 9 02절 값(pypdf 6.17.0)과 기본 읽기 글자 수가 같았습니다.**
- **결론 태도(Ch 9 §1과 같음)**: 한 번 본 결과는 「이번 실행에서는」, 두 조건 공통 값은 한 조건 효과로 적지 않음, 읽기 방법 하나가 늘 더 좋다고 쓰지 않음(01은 「글이 달라진다」까지만).

### 02절이 이어받을 연결과 확인할 것

- 01 b8·노트북 정리 끝: 「02절에서는 같은 PDF를 pypdf가 아닌 다른 라이브러리로도 읽습니다. 표의 행과 열이 남는지, 스캔본에서 글자가 아예 나오지 않는지 확인합니다. 그때 `parser` 칸에 적을 이름이 하나 더 늘어납니다.」
- **개선 전 02 노트북**은 `E02.pdf`와 `S01-E01-scan.pdf`를 쓰고, `pypdf==6.18.0`·`pdfplumber==0.11.10`을 설치하며, `pdfplumber.open()`·`extract_text(layout=True)`·`extract_tables()`를 씁니다. Before는 스캔본 모든 쪽에 글이 있다고 보는 `all(...)`+`assert`, After는 `enumerate(..., 1)`로 OCR 후보 쪽 모으기입니다. **01이 이미 pypdf 기본 읽기와 레이아웃 읽기를 견줬으므로**, 02는 pdfplumber 쪽(표·스캔본)에 무게를 두고 01과 겹치는 설명을 되풀이하지 마세요.
- **문서 결정**: 01은 Ch 9와 잇기 위해 `E01.pdf`를 씁니다. 02가 표를 보이려면 `E02.pdf`(표 2개)나 `M03.pdf`(표 많음)가 낫습니다. 어느 쪽을 골라도 01의 다섯 칸 기록·`make_source_record()`·`make_source_mark()`를 그대로 쓸 수 있습니다. 문서를 바꾸면 그 절 본문에 까닭을 한 문장 적어 주세요(01은 E01, 02는 다른 문서).
- 개선 전 02 노트북이 쓰는 것 가운데 **01·Part 1·2에서 안 가르친 것**: `Path.cwd()`·`parents`·`/` 경로 연산·`relative_to()`·`path.stat().st_size`, `with pdfplumber.open(...) as pdf:`(L3 `with`는 Ch 2 05에서 배움 — 라이브러리 객체에 쓰는 자리는 처음), `text or ""`, `all(...)`+제너레이터 식, `enumerate(..., 1)`, `try/except AssertionError`, f-string 안 `{error}`, 타입힌트 `def text_length(reader: PdfReader, page_number: int) -> int`, 영어 출력 라벨(`OCR candidate pages:`).
- **아직 안 가르친 것(02가 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 전체 + 01에서도 안 한 것 — 표 구조 살려 읽기·`extract_tables()`, 스캔본·OCR, 두 단 레이아웃과 읽기 순서, 다른 라이브러리(`pdfplumber`·`python-docx`·`bs4`·`csv`·`zipfile`), 토큰 기준 스플리터, 임베딩·검색·점수(이 챕터 05~08), 실습 폴더 모듈 `import`, `chunk_id`, 여러 문서 한 번에 읽기, 파일 크기·수정 시각 읽기, 민감한 문서 속성 걸러내기.
- 01 b7의 「실습 폴더 `normalize_metadata()`는 인자 모양이 다르고 쪽 번호가 1보다 작으면 오류를 냅니다. 이번 노트북에서는 그 모듈을 부르지 않았습니다」는 02 이후에도 모듈을 부르지 않는다면 되풀이하지 않아도 됩니다.

### 산출 파일·실습 폴더·묶음

- 01은 `runs/`를 읽지도 쓰지도 않았습니다. `labs/part3/ch10-document-processing/runs/` 전체 해시 전후 같음. 이 챕터 `runs/`를 쓰는 곳은 개선 전 **08절**(`runs/continuity-ch10-indexing.jsonl` 한 줄 + `runs/continuity/` 사본 24개)입니다.
- **08절 작업자가 먼저 읽을 곳**(Ch 9 요약 §4와 같은 계약): `labs/part3/ch11-evaluation/evaluate.py` 176~250행, `textbook/part3/qa/check_continuity.py` 58~78·140~155행, `textbook/qa/check_course_continuity.py` 94~112·172~198행, `textbook/part3/qa/run_continuity_bundle.py` 45~54행(묶음 연기 실행이 **08절 노트북만** 씀), `textbook/part3/qa/finalize_continuity_evidence.py` 15·37·44~56행. 현재 기록의 `chunk_id`는 `ch10:recursive:0000`(네 자리 채움)이고 Ch 9는 `ch09:6f9f83db90:0`입니다 — 모양 차이를 08절 본문·챕터 요약에 적으세요(Ch 9 검토 B R-3).
- **Ch 9 「점수 = 코사인 유사도」는 `InMemoryVectorStore` 한정입니다.** 07·08절에서 다른 벡터스토어나 다른 방식으로 점수를 내면 「점수가 크면 가깝다」를 그대로 이어 쓰지 마세요(Ch 9 요약 §5).
- 실습 폴더 테스트 `38 passed`(전후 같음). `document_processing.py`·`experiment.py`·`tests/`·`fixtures/`는 고치지 않았습니다.
- **학생 묶음**: 01이 읽는 `labs/data/rag-corpus/pdf/*/`와 `labs/part3/ch10-document-processing/fixtures/`는 이미 `build_bundle.py`의 `data`·`FIXTURES`에 있어 허용 목록을 고치지 않았습니다. **새로 읽는 입력이 생기면** `textbook/part3/public-files.json`(`labs/part3/` 접두만)과 `build_bundle.py`를 함께 보고, `part3-practice.zip`을 `/tmp`에 풀어 그 절 경로 셀을 **묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리**에서 돌려 보세요. 01에서 후보 경로 실수를 이 방법으로 잡았습니다.
- `textbook/part3/qa/check_continuity.py`는 154행 zip 신선도(`part2-practice.zip`), `textbook/qa/check_course_continuity.py`는 212행 zip 신선도(`part1-practice.zip`)에서 멈춥니다. 전체 마감 몫이고 Ch 9 마감 때와 같은 자리입니다.

### 실행 환경

- 가상환경 `$ROOT/.cache/vm/venv-ch10-document-processing`을 이 절에서 만들었습니다(`uv sync --locked`, uv 캐시 `$ROOT/.cache/vm/uv`). `run_section.sh`가 자동으로 씁니다. torch·로컬 모델 없음.
- **기준 버전(uv.lock)**: pypdf **6.18.0**(Ch 9 폴더는 6.17.0), pdfplumber 0.11.10, python-docx 1.2.0, beautifulsoup4 4.15.0, lxml 6.1.3, langchain-core 1.6.2, langchain-text-splitters 1.1.2, langchain-openai 1.6.0, langchain-classic 1.0.8, langchain-experimental 0.4.2, langchain-community 0.4.2, openai **2.54.0**(Ch 9는 3.8.0), tiktoken 0.14.0, numpy 2.5.3, python-dotenv 1.2.3. 새 커널 `nbclient==0.11.0`·`ipykernel==7.3.0`, Linux aarch64 Python 3.12.13. **이 챕터에는 `langchain` 메인 패키지가 없습니다** → `from langchain.chat_models import init_chat_model`이 되는지 그 절에서 확인하세요(01은 모델을 부르지 않아 확인하지 않았습니다).
- 키는 루트 `.env`(`nbkit.KEY`가 `find_dotenv(usecwd=True)`로 읽음). 01은 키를 쓰지 않습니다.
- **execute.py 작업 폴더 = 프로젝트 맨 위**: 01 경로 후보는 첫째(`.`)가 골라집니다. 결과 읽기에 그렇게 밝혔습니다.
- Mermaid 렌더만 따로: `PUPPETEER_CACHE_DIR=/tmp/pptr-cache LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu python3 textbook/_notebook/mermaid/render_mermaid.py textbook/part3/ch10-document-processing --only NN-`. 렌더 도장 `*.render.json`은 지우지 않습니다(같은 mmd를 다시 렌더할 때만 `--force`).
- `visual.cjs`: `sed "s|require('playwright')|require('/tmp/pw/node_modules/playwright')|" textbook/_notebook/visual.cjs > /tmp/ch10-NN/vis/vis.cjs` + HTML을 `/tmp/ch10-NN/html/`에 복사 → `cd /tmp/ch10-NN/vis && LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu node vis.cjs /tmp/ch10-NN/html`. 01은 1280·390 두 건 PASS.
- 삽화: 클라우드 `outputs` 쓰기가 막혀 기기 셸에서 `curl`로 받아 pillow로 폭 1100px로 줄여 `figures/`에 바로 저장했습니다. 저장 PNG를 채택 job 결과와 픽셀 대조(`ImageChops.difference(...).getbbox() is None`). Higgsfield 잔액 2808(01 뒤).
- `run_section.sh`는 「오늘 볼 그림」 PNG가 없으면 그림 첨부 단계에서 멈추므로 `.mmd`를 먼저 두고 렌더한 뒤 실행하세요.
- 기기 루트 여유 약 520MB. 작업 폴더 `/tmp/ch10-01`(해시·묶음 풀기·삽화 원본·visual 사본).
- **옛 도식 생성기 `figures/_gen_figures.py`는 실행을 막아 두었습니다**(첫머리 `raise SystemExit`). 02~08절 개선 때도 실행하지 마세요. 챕터 마감 때 `qa/upgrade/before/generators/`로 옮깁니다. 옛 노트북 생성기(`make_*.py`·`_make_notebooks.py`)는 이 챕터에 없습니다.
- 개선 전 QA 스크립트 `qa/check_content.py`·`qa/check_visual.cjs`는 개선 전 본문·도식 기준입니다(01에서 실행하지 않음). 챕터 마감 때 확인하세요.

## §02 → §03

(02절 품질 개선 2026-09-18. 결과는 `02-diagnosis.md`, 게이트 G1~G7 0(수정 전 G1 1·G2 1·G5 10·G6 34·G7 3 = 49), 코드 셀 18(준비 2), 검사 문장 323, **서비스 요청 0번**(모델·임베딩 없음, API 키 없이 실행), 새 커널로 두 번 이어 실행해 `outputs_sha256` `f7b750bc…` 같음(교재 출력은 마지막 실행 2026-09-18T02:32:23Z). 삽화 02-5 1차 채택(job `93541862-…`, 2크레딧, 잔액 2806), Mermaid 4장. **빌드 도구·챕터 밖 파일 변경 0건**)

### 02가 확인한 실행 환경 (01 §01 → §02 그대로 쓸 수 있음)

- `run_section.sh textbook/part3/ch10-document-processing 02`로 생성기 → 새 커널 → 렌더 → 첨부 → 빌드 → 게이트가 한 번에 돌아갑니다. `chapter.json`이 없어 verify는 따로:
  `UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch10-document-processing uv run --project labs/part3/ch10-document-processing python textbook/_notebook/verify.py --chapter textbook/part3/ch10-document-processing`
  → 02 뒤 `PASS 8 sections / 87 code cells (max 24 lines)`(01 뒤 77).
- 02 뒤 디스크 HTML 기준: `/tmp/ch10-02/hash/final.txt`. 작업 전후 `sha256sum *.html`로 다른 절이 바뀌지 않았는지 보세요(02에서는 02 HTML만 `666e2acd…` → `dcfe8da182…`).
- `visual.cjs`·묶음 풀기·삽화 저장 방법은 §01 → §02와 같습니다. `.cache/vm/shot/`에 검수용 캡처를 두었습니다(`ch10-02-cand1.png`·`ch10-02-page-illu.png`·`ch10-02-page-mmd2.png`).
- 기기 루트 여유 약 516MB. 작업 폴더 `/tmp/ch10-02`(해시·탐색 실행·묶음·삽화 원본·visual 사본).
- `%pip` 셀의 출력이 실행에 따라 한 덩이일 때와 두 덩이일 때가 있습니다(값은 같음). 두 번 이어 실행하면 `outputs_sha256`까지 같아졌습니다.

### 용어 (02에서 정한 것, 03~08도 같게)

- **01절이 정한 네 말**(파서·파일 형식·출처 기록·출처 계보)과 Ch 9 용어를 그대로 씁니다. 02가 새로 정한 말은 네 개입니다: **글자 층(text layer)**, **표 읽기(table extraction)**, **글자 인식(OCR)**, **OCR 후보 쪽**.
- **「빈칸」은 글자 사이의 공백입니다**(01절 뜻). 표에서 값이 없는 칸은 **「값이 없는 칸」**으로 쓰고, 코드가 넣는 자리 표시 글은 **`(값 없음)`**입니다. 03~04절에서 표를 다룰 때 이 갈래를 이어 쓰세요.
- 「빈 글」은 빈 문자열 `''`입니다(02 노트북 4절 결과 읽기).
- `parser` 값 이름: 01 `pypdf-plain`, **02 `pdfplumber`**. 03·04절은 모듈 `document_processing.py`가 쓰는 `python-docx`·`beautifulsoup`·`csv.DictReader`·`zip-xml`을 같은 글로 맞추세요.
- 쓰지 않은 말: 「텍스트 레이어」(→ 글자 층), 「레이아웃」(01절이 「레이아웃 읽기」로 이미 씀 — 02는 pypdf 레이아웃 읽기를 다시 다루지 않음), 「읽기 순서」(이 절에서 실행하지 않음), 「표 추출」(→ 표 읽기), 「광학 문자 인식」(→ 글자 인식), 상용 파서 이름(PyMuPDF·Tesseract·Upstage·LlamaParse는 본문에서 뺐습니다).

### 02에서 새로 가르친 것

- **API·동작(노트북에서 실행한 것만)**: `import pdfplumber`, `with pdfplumber.open(경로) as pdf:`(Ch 2 05절 `with`를 **라이브러리 객체에 처음 쓰는 자리** — 노트북 4절 설명 셀에 한 문장), `pdf.pages[n]`, `page.extract_tables()`(표 → 행 → 칸 세 겹 목록), 글 `split(" ")`.
- **Python 모양**: 세 겹 목록 인덱싱(`tables[0]`·`first_table[1]`), 목록 안 목록의 칸 번호로 짝 찾기, 함수가 함수를 부르기(`make_row_text` → `make_cell_text`), 글 `+`로 이어 붙이며 구분자 넣기. 01절과 같은 후보 경로 `for`+`break`.
- **01절이 안 쓴 것 가운데 02도 안 쓴 것**: `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·try·`raise`·`+=`·`enumerate`·`zip`·`sum`·`max`·`any`·`all`·`join`·`isinstance`·f-string 안 계산·타입힌트·`@`·`BaseModel`·모델 문장 `assert`·`Path.cwd()`·`parents`.
- **함수 본문 10줄 규칙(규격 §2-2 L2)**: 처음 쓴 `make_row_text`가 11줄이어서 칸 하나를 맡는 `make_cell_text`를 떼어 9줄로 줄였습니다. G1 `long_function`은 문장 수만 세어 걸리지 않으므로 **줄 수를 직접 세세요**.
- **이어 쓸 이름과 값**: `candidates`·`root_path`(교재 출력 `.`), `corpus_path`, `pdf_path`(= `corpus_path + "/pdf/easy/E01.pdf"`), `scan_path`(= `corpus_path + "/pdf/scanned/S01-E01-scan.pdf"`), `reader`·`plain_text`(905자)·`plain_lines`(26줄), `header_line`·`first_row_line`·`header_values`·`first_row_values`, `tables`·`first_table`(7행)·`header_row`, `make_cell_text(label, cell)`·`make_row_text(header_row, row)`, `make_source_record(file_path, page, parser)`·`make_source_mark(chunk)`(01절과 같은 코드), `table_record`·`row_documents`(6개)·`row_number`, `fourth_table`(5행)·`fourth_header`, `scan_reader`·`scan_documents`, `count_page_lengths(pdf_reader)`·`find_ocr_candidates(lengths, minimum_chars)`·`minimum_chars = 20`·`scan_lengths`·`origin_lengths`·`scan_candidates`·`origin_candidates`.
- **출력 라벨(전부)**: 「고른 경로:」「E01 파일이 있는가:」「스캔본 파일이 있는가:」「스캔본 파일 이름:」「기본 읽기 글자 수:」「기본 읽기 줄 수:」「마지막 줄:」「머리글 줄:」「머리글 줄의 값 개수:」「첫 행 줄:」「첫 행 줄의 값 개수:」「찾은 표의 수:」「첫 표의 행 수:」「머리글 행:」「첫 행:」「첫 행의 칸 수:」「기본 읽기 줄:」「머리글을 붙인 줄:」「둘째 행:」「행 Document 수:」「첫 행의 출처 표시:」「첫 행의 기록:」「4쪽에서 찾은 표의 수:」「4쪽 첫 표의 행 수:」「4쪽 머리글 행:」「4쪽 첫 행:」「스캔본 쪽 수:」「만든 Document 수:」「2쪽 출처 표시:」「2쪽 본문 글자 수:」「기준값(글자 수):」「스캔본 쪽별 글자 수:」「E01 쪽별 글자 수:」「스캔본의 OCR 후보 쪽:」「E01의 OCR 후보 쪽:」
- **실행값(2026-09-18, 새 커널 두 번 같음)**: `pypdf: 6.18.0`·`pdfplumber: 0.11.10`·`langchain-core: 1.6.2`, `고른 경로: .`, `스캔본 파일 이름: S01-E01-scan.pdf`, `기본 읽기 글자 수: 905`·`줄 수: 26`·`마지막 줄: 2`, `머리글 줄: 구역 평일 주말 비고`·`값 개수: 4`, `첫 행 줄: 종합자료실(2층) 09:00~22:00 09:00~18:00`·`값 개수: 3`, `찾은 표의 수: 1`·`첫 표의 행 수: 7`·`머리글 행: ['구역', '평일', '주말', '비고']`·`첫 행: ['종합자료실(2층)', '09:00~22:00', '09:00~18:00', '']`·`칸 수: 4`, `머리글을 붙인 줄: 구역: 종합자료실(2층) / 평일: 09:00~22:00 / 주말: 09:00~18:00 / 비고: (값 없음)`, `둘째 행: 구역: 어린이자료실(1층) / 평일: 09:00~18:00 / 주말: 09:00~18:00 / 비고: 보호자 동반 권장`, `행 Document 수: 6`·`[E01 p.2]`·`{'doc_id': 'E01', 'source': 'E01.pdf', 'file_type': 'pdf', 'parser': 'pdfplumber', 'page': 2}`, 4쪽 `표의 수: 1`·`행 수: 5`·`['시설', '정원', '이용료(시간당)', '예약 방법']`·`시설: 강당(지하 1층) / 정원: 150명 / 이용료(시간당): 30,000원 / 예약 방법: 14일 전 홈페이지`, Before `스캔본 쪽 수: 5`·`만든 Document 수: 5`·`[S01-E01-scan p.2]`·`2쪽 본문 글자 수: 0`, After `기준값(글자 수): 20`·`[0, 0, 0, 0, 0]`·`[45, 905, 925, 871, 270]`·`[1, 2, 3, 4, 5]`·`[]`.
- **E01·스캔본 읽기 결과(03~08절이 쓸 값)**: E01 2쪽 표 1개 7행(머리글 + 구역 6행, 칸 4개, 첫 데이터 행 `종합자료실(2층)`의 비고 칸만 빈 글), 4쪽 표 1개 5행. pdfplumber가 읽은 쪽 글자 수는 pypdf와 1~3자 다릅니다(2쪽 904 대 905). 스캔본 `S01-E01-scan.pdf`는 다섯 쪽 모두 `extract_text()`가 **빈 글 `''`**를 반환합니다(`None`이 아님). `pdf/scanned/`의 다른 두 건은 `S02-M03-scan.pdf`·`S03-H01-scan.pdf`입니다.
- **기준값 20자**: 탐색 실행에서 스캔본 0자와 E01 가장 짧은 쪽 45자를 본 뒤 그 사이에서 정했고, 실습 폴더 `detect_scanned_pdf(min_text_chars=20)` 기본값과 같습니다. 본문 b7 첫 항목에 과정과 「흐름을 보여 주려고 정한 예」를 적었습니다(규격 §3).
- **결론 태도(01·Ch 9와 같음)**: 「이번 실행에서는」, 어느 읽기가 늘 더 좋은지 판정하지 않음, 후보로 가른 것을 글자를 얻은 것으로 쓰지 않음, 실행하지 않은 동작은 「이번에 실행하지 않았습니다」.

### 03절이 이어받을 연결과 확인할 것

- 02 b8·노트북 정리 끝: 「03절에서는 PDF가 아닌 형식을 읽습니다. DOCX·HTML·CSV 견본을 열어 형식마다 어디까지 구조가 남는지 봅니다. 그때도 같은 다섯 칸에 담고 `parser` 칸에 적을 이름이 더 늘어납니다.」
- **개선 전 03 노트북**을 먼저 읽고 어떤 견본·API를 쓰는지 확인하세요. 견본은 `labs/part3/ch10-document-processing/fixtures/`의 `sample.docx`·`sample.html`·`sample.csv`이고(01절 2절에서 확장자를 이미 세어 보였습니다), 모듈이 쓰는 이름은 `python-docx`·`beautifulsoup`·`csv.DictReader`입니다.
- **02와 겹치지 않게**: 표는 02가 pdfplumber로 다뤘습니다. 03은 DOCX 표와 HTML 표에서 **형식마다 표가 어떻게 들어 있는지**에 무게를 두고, 「머리글을 붙여 한 줄로 만들기」는 02 함수를 이어 쓰거나 형식 차이만 보이면 됩니다. 「기본 읽기 대 표 읽기」 비교를 되풀이하지 마세요.
- 03·04절이 `Document`를 만들 때 **쪽 번호가 없는 형식**(DOCX·HTML·CSV)을 만납니다. 01절 `make_source_record()`는 `page`를 반드시 받습니다. 모듈 `normalize_metadata()`는 `page`가 없으면 그 칸을 넣지 않고 `row`·`section` 같은 칸을 대신 붙입니다. 어느 쪽을 쓸지 정해 본문에 한 문장 적고, `make_source_mark()`가 `page` 칸을 읽는다는 점(01·02와 같은 코드)을 함께 확인하세요.
- **아직 안 가르친 것(03이 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 전체 + 01·02에서도 안 한 것 — 글자 인식(OCR) 실행, 선 없는 표·병합 셀 표, 두 단 레이아웃과 읽기 순서, 글자가 있는 쪽과 없는 쪽이 섞인 파일, pdfplumber `layout=True`, `python-docx`·`bs4`·`csv`·`zipfile`, 토큰 기준 스플리터, 임베딩·검색·점수(이 챕터 05~08), 실습 폴더 모듈 `import`, `chunk_id`, 여러 문서 한 번에 읽기, 파일 크기·수정 시각 읽기.

### 산출 파일·실습 폴더·묶음

- 02도 `runs/`를 읽지도 쓰지도 않았습니다(40개 파일 해시 전후 같음). 이 챕터 `runs/`를 쓰는 곳은 개선 전 **08절**입니다(§01 → §02의 08절 계약 목록을 그대로 보세요).
- 실습 폴더 테스트 `38 passed`(전후 같음). `document_processing.py`·`experiment.py`·`tests/`·`fixtures/`는 고치지 않았습니다.
- **학생 묶음**: 02가 읽는 `pdf/easy/E01.pdf`·`pdf/scanned/S01-E01-scan.pdf`는 `build_bundle.py` 63행 `labs/data/rag-corpus/pdf/*/*.pdf`에 이미 들어 있어 허용 목록을 고치지 않았습니다. 03절이 `fixtures/`의 견본을 읽으면 `FIXTURES` 목록(31행)에 다섯 개가 이미 있습니다. 새 입력이 생기면 묶음을 `/tmp`에 풀어 **묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리**에서 경로 셀을 돌려 보세요(02에서 두 파일로 확인).
- 절 수는 8개 그대로라 `textbook/part3/_build_index.py`(ch10 칸 8)와 `qa/visual-results.json` 행 수는 고치지 않았습니다.

## §03 → §04

(03절 품질 개선 2026-09-18. 결과는 `03-diagnosis.md`, 게이트 G1~G7 0(수정 전 G1 1·G2 1·G5 10·G6 22·G7 3 = 37), 코드 셀 23(준비 2), 검사 문장 403, **서비스 요청 0번**(모델·임베딩 없음, API 키 없이 실행), 새 커널로 두 번 이어 실행해 `outputs_sha256` `7df82873…` 같음(교재 출력은 마지막 실행 2026-09-18T03:05:58Z). 삽화 03-5 1차 채택(job `eca83a35-…`, 2크레딧, 잔액 2804), Mermaid 4장. **빌드 도구·챕터 밖 파일 변경 0건**)

### 03이 확인한 실행 환경 (§01 → §02·§02 → §03 그대로 쓸 수 있음)

- `run_section.sh textbook/part3/ch10-document-processing 03`으로 생성기 → 새 커널 → 렌더 → 첨부 → 빌드 → 게이트가 한 번에 돌아갑니다. `chapter.json`이 없어 verify는 따로:
  `UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch10-document-processing uv run --project labs/part3/ch10-document-processing python textbook/_notebook/verify.py --chapter textbook/part3/ch10-document-processing`
  → 03 뒤 `PASS 8 sections / 102 code cells (max 24 lines)`(02 뒤 87).
- 03 뒤 디스크 HTML 기준: `/tmp/ch10-03/hash/final.txt`. 작업 전후 `sha256sum *.html`로 다른 절이 바뀌지 않았는지 보세요(03에서는 03 HTML만 `36664a7d…` → `74d29499…`).
- `visual.cjs`·묶음 풀기·삽화 저장 방법은 §01 → §02와 같습니다. `.cache/vm/shot/`에 검수용 캡처를 두었습니다(`ch10-03-cand1.png`·`ch10-03-page-illu.png`·`ch10-03-page-mmd3.png`).
- 기기 루트 여유 약 511MB. 작업 폴더 `/tmp/ch10-03`(해시·탐색 실행·묶음·삽화 원본·visual 사본).
- **게이트 라벨**: `upgrade_gates.py … --label after --section 03`이 `gates-after-03.json`을 씁니다. `--label after-03`을 주면 `gates-after-03-03.json`이 되므로 라벨은 `after`만 주세요(03에서 한 번 잘못 주어 `/tmp/ch10-03/gates-stray.json`으로 옮겼습니다).
- 셀을 나누기 전 판에서도 두 번 이어 실행해 `outputs_sha256`이 같았고, 그보다 앞선 실행에서 한 번 달랐습니다. 값은 언제나 같고 `%pip` 셀 출력이 한 덩이일 때와 두 덩이일 때가 있습니다(02절과 같음).

### 용어 (03에서 정한 것, 04~08도 같게)

- **01절 네 말**(파서·파일 형식·출처 기록·출처 계보), **02절 네 말**(글자 층·표 읽기·글자 인식·OCR 후보 쪽), Ch 9 용어를 그대로 씁니다. 03이 새로 정한 말은 네 개입니다: **문단(paragraph)**, **꾸밈 이름(style name)**, **태그(tag)**, **자리 칸**.
- **「자리 칸」** = 쪽이 없는 형식에서 본문이 파일의 어디에서 왔는지 적는 칸입니다. 03에서는 CSV의 `row`가 그것입니다. 04절 HWPX의 `section`도 자리 칸이니 같은 말로 부르세요.
- **「빈칸」·「값이 없는 칸」 갈래는 02절 그대로**입니다(빈칸 = 글자 사이의 공백, 값이 없는 칸 = 표의 빈 칸, 자리 표시 글 `(값 없음)`). 03 견본 세 개에는 값이 없는 칸이 없어 `(값 없음)`이 출력에 나오지 않았고, 노트북 7절 설명 셀에 그 사실을 적었습니다.
- `parser` 값 이름: 01 `pypdf-plain`, 02 `pdfplumber`, **03 `python-docx`·`beautifulsoup`·`csv.DictReader`**. 04절은 모듈 `document_processing.py` `load_hwpx()`가 쓰는 **`zip-xml`**을 같은 글로 쓰세요. HWP 이진 형식은 모듈이 읽지 않습니다(`recognize_hwp_kind()`가 형식만 가림).
- 「열」 대신 **「칸」**, 「행 사전」 대신 **「딕셔너리」**로 씁니다. 「필드」·「스키마」는 쓰지 않습니다(01절 「쓰지 않은 말」).
- 쓰지 않은 말: 「DOM」·「문서 객체 모델」, 「본문 선택자」(→ 고를 태그 목록), 「CSV 방언」(→ 구분자), 「형식 보존 단위」(→ 자리 칸), 「정규화」, 「청킹」.

### 03에서 새로 가르친 것

- **API·동작(노트북에서 실행한 것만)**: `from docx import Document as DocxDocument`(LangChain `Document`와 이름이 겹쳐 `as`로 다른 이름을 붙이는 자리 — 노트북 1절 설명 셀에 한 문장, Ch 4 01절 `import pandas as pd`와 같은 표기), `DocxDocument(경로)`·`docx_file.paragraphs`·`paragraph.text`·`paragraph.style.name`, `docx_file.tables`·`table.rows`·`row.cells`·`cell.text`, `BeautifulSoup(글, "html.parser")`·**`find_all("h1")`·`find_all(["h1", "p"])`**(Part 1 §2 「처음 쓰면 한 문장」 대상 — 노트북 5절 설명 셀에 뜻)·`tag.name`·`tag.get_text(" ", strip=True)`, `csv.DictReader(파일)`·`reader.fieldnames`, `open(..., newline="")`(설명 셀에 한 문장).
- **Python 모양**: 두 겹 `for`(Ch 5에서 배운 모양 — CSV 행마다 칸 이름으로 값 꺼내기), 딕셔너리에 칸 하나 더 대입(`csv_record["row"] = 2`), `"page" in 기록`으로 칸 유무 보기, 함수가 `if`로 두 가지 글 가운데 하나를 만들기(`make_unit_mark`). 01·02절과 같은 후보 경로 `for`+`break`.
- **01·02절이 안 쓴 것 가운데 03도 안 쓴 것**: `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·try·`raise`·`+=`·`enumerate`·`zip`·`sum`·`max`·`any`·`all`·`isinstance`·`join`·`list()`·f-string 안 계산·타입힌트·`@`·`BaseModel`·모델 문장 `assert`·`Path.cwd()`·`parents`.
- **셀 줄 수(규격 §2-4)**: 처음 쓴 Before 셀이 13줄, After 셀이 15줄이어서 각각 둘로 나눴습니다(권장 3~12줄). 게이트는 15줄까지 통과시키므로 **주석·빈 줄을 뺀 줄 수를 직접 세세요**. 03 최대는 12줄입니다.
- **함수 본문 10줄(규격 §2-2 L2)**: `read_row_values` 4줄 · `pick_tag_texts` 4줄 · `make_cell_text` 4줄 · `make_row_text` 9줄(02절과 같은 코드) · `make_unit_record` 5줄 · `make_unit_mark` 7줄.
- **이어 쓸 이름과 값**: `candidates`·`root_path`(교재 출력 `.`), **`fixtures_path`**(= `root_path + "/labs/part3/ch10-document-processing/fixtures"`, 01절과 같은 이름), `docx_path`·`html_path`·`csv_path`, `docx_file`·`paragraph_texts`·`paragraph_styles`, `read_row_values(table_row)`, `docx_tables`·`first_docx_table`·`docx_header`(`['지역', '추가 일수']`)·`docx_first_row`(`['제주', '2일']`), `soup`·`title_tags`·`body_tags`·`table_tags`·`style_tags`, `pick_tag_texts(tag_tree, wanted_tags)`·`wanted_tags = ["h1", "p"]`·`picked_tags`·`picked_texts`·`changed_tags = ["p"]`·`changed_texts`, `csv_header`(`['상품', '보관']`)·`csv_rows`·`csv_row_texts`, `make_cell_text(label, cell)`·`make_row_text(header_row, row)`(02절과 같은 코드), **`make_unit_record(file_path, parser)`**·**`make_unit_mark(chunk)`**, `docx_record`·`html_record`·`csv_record`·`row_documents`·`before_text`·`before_record`·`before_document`·`table_word = "추가 일수"`·`after_text`·`after_record`·`after_document`.
- **출력 라벨(전부)**: 「고른 경로:」「DOCX 견본이 있는가:」「HTML 견본이 있는가:」「CSV 견본이 있는가:」「객체 이름:」「문단 수:」「문단 글:」「문단 꾸밈 이름:」「표 목록의 표 수:」「첫 표의 행 수:」「머리글 행:」「첫 행:」「h1 태그 수:」「p 태그 수:」「table 태그 수:」「style 태그 수:」「고를 태그 목록:」「고른 글:」「첫 글의 태그 이름:」「둘째 글의 태그 이름:」「칸 이름:」「행 수:」「첫 행의 자료형:」「DOCX 표의 한 행:」「CSV 첫 행:」「CSV 둘째 행:」「DOCX 기록:」「HTML 기록:」「CSV 기록:」「DOCX 기록에 page 칸이 있는가:」「세 기록의 doc_id:」「행 Document 수:」「첫 행의 출처 표시:」「둘째 행의 출처 표시:」「둘째 행의 기록:」「바꾼 태그 목록:」「고른 글 수:」「이어 붙인 글자 수:」「본문 글자 수:」「출처 표시:」「표 머리글이 본문에 있는가:」「본문:」「더한 뒤 글자 수:」
- **실행값(2026-09-18, 새 커널 두 번 같음)**: `python-docx: 1.2.0`·`beautifulsoup4: 4.15.0`·`langchain-core: 1.6.2`, `고른 경로: .`, 견본 세 줄 모두 `True`, `문단 수: 2`·`문단 글: ['배송 안내', '제주 배송에는 이틀이 더 필요합니다.']`·`문단 꾸밈 이름: ['Heading 1', 'Normal']`, `표 목록의 표 수: 1`·`첫 표의 행 수: 2`·`머리글 행: ['지역', '추가 일수']`·`첫 행: ['제주', '2일']`, `h1 태그 수: 1`·`p 태그 수: 1`·`table 태그 수: 0`·`style 태그 수: 1`, `고른 글: ['반품 안내', '수령 후 7일 이내 신청합니다.']`·`첫 글의 태그 이름: h1`·`둘째 글의 태그 이름: p`, `칸 이름: ['상품', '보관']`·`행 수: 2`·`첫 행: {'상품': '쿠키', '보관': '실온'}`·`첫 행의 자료형: dict`, `DOCX 표의 한 행: 지역: 제주 / 추가 일수: 2일`·`CSV 첫 행: 상품: 쿠키 / 보관: 실온`·`CSV 둘째 행: 상품: 케이크 / 보관: 냉장`, `DOCX 기록: {'doc_id': 'sample', 'source': 'sample.docx', 'file_type': 'docx', 'parser': 'python-docx'}`·`HTML 기록: {… 'file_type': 'html', 'parser': 'beautifulsoup'}`·`CSV 기록: {… 'file_type': 'csv', 'parser': 'csv.DictReader', 'row': 2}`·`DOCX 기록에 page 칸이 있는가: False`·`세 기록의 doc_id: sample sample sample`, `행 Document 수: 2`·`첫 행의 출처 표시: [sample csv row.2]`·`둘째 행의 출처 표시: [sample csv row.3]`·`둘째 행의 기록: {… 'row': 3}`, `바꾼 태그 목록: ['p']`·`고른 글 수: 1`·`고른 글: ['수령 후 7일 이내 신청합니다.']`, Before `이어 붙인 글자 수: 26`·`본문 글자 수: 26`·`출처 표시: [sample docx]`·`표 머리글이 본문에 있는가: False`, After `더한 뒤 글자 수: 45`·`표 머리글이 본문에 있는가: True`.
- **견본 세 개 읽기 결과(04~08절이 쓸 값)**: `sample.docx`는 문단 2개(제목 `배송 안내`·본문 1개)와 두 행짜리 표 1개(`지역`·`추가 일수` / `제주`·`2일`)이고, **문단 목록에 표 글이 들어오지 않습니다**. `sample.html`은 `style`·`h1`·`p` 태그 하나씩이고 **`table` 태그가 없습니다**. `sample.csv`는 칸 이름 줄 + 행 2개(`쿠키`·`실온` / `케이크`·`냉장`)이고 파일 앞 표시(BOM)가 없어 `encoding="utf-8"`로 읽었습니다. 나머지 견본 두 개는 `legacy-signature.hwp`(23바이트)·`minimal-marker.hwpx`(470바이트)입니다.
- **결론 태도(01·02·Ch 9와 같음)**: 「이번 실행에서는」, 어느 형식이 읽기 쉬운지·어느 태그 목록이 나은지 판정하지 않음, 실행하지 않은 동작은 「이번에 실행하지 않았습니다」, 두 실행 공통 값은 한 조건 효과로 적지 않음(03-4 회색 상자).

### 쪽 번호가 없는 형식의 출처 기록 (03이 정했습니다 — 04절이 그대로 이어받을 것)

- **네 칸**(`doc_id`·`source`·`file_type`·`parser`)만 적고 `page` 칸은 넣지 않습니다. 파일 안의 자리를 적을 수 있는 형식만 **자리 칸 하나**를 더합니다(CSV는 `row`, HWPX는 모듈이 쓰는 `section`).
- 함수는 `make_unit_record(file_path, parser)`입니다. 01절 `make_source_record(file_path, page, parser)`에서 쪽 번호 칸만 뺀 코드이고 본문 5줄입니다. 자리 칸은 부른 뒤 `csv_record["row"] = 2`처럼 대입해 더합니다.
- **출처 표시는 `make_unit_mark(chunk)`가 만듭니다.** 기록에 `row` 칸이 있으면 `[sample csv row.2]`, 없으면 `[sample docx]`입니다. 01·02절 `make_source_mark()`는 `page` 칸을 읽으므로 이 절 기록에는 쓸 수 없습니다(노트북 8절에서 `DOCX 기록에 page 칸이 있는가: False`로 보였습니다).
- 이 모양은 실습 폴더 `document_processing.py` `normalize_metadata()`·`load_csv()`와 같습니다. 그 함수는 `page`가 없으면 그 칸을 넣지 않고 `row`·`section` 같은 칸을 대신 붙이며, `page`가 1보다 작으면 오류를 냅니다.
- **04절은 `make_unit_mark()`가 만들 표시를 정하세요.** HWPX에 `section` 칸을 쓰면 `make_unit_mark()`가 `row` 칸만 보므로 그대로는 `[minimal-marker hwpx]`까지만 나옵니다. 같은 함수를 넓힐지, HWPX에 자리 칸을 두지 않을지 정해 본문에 한 문장 적어 주세요.
- **doc_id가 겹칩니다.** 견본 세 개의 `doc_id`가 모두 `sample`입니다(파일 이름 앞부분). 03 b7에 「실제 문서 모음에서는 폴더 이름이나 접두를 붙여 갈라 둔다」를 적었습니다. 04절 견본 두 개는 `legacy-signature`·`minimal-marker`로 갈라집니다.

### 04절이 이어받을 연결과 확인할 것

- 03 b8·노트북 정리 끝: 「04절에서는 HWP와 HWPX를 가릅니다. 이름이 비슷하지만 파일 안의 모양이 다릅니다. HWPX 견본을 열어 압축 파일 속 XML을 직접 보고, 그때도 같은 칸 이름에 담습니다.」
- **개선 전 04 노트북**을 먼저 읽고 어떤 견본·API를 쓰는지 확인하세요. 견본은 `fixtures/legacy-signature.hwp`·`minimal-marker.hwpx`이고, 모듈이 쓰는 이름은 `recognize_hwp_kind()`(파일 시그니처 `D0CF11E0A1B11AE1` 비교)와 `load_hwpx()`(`zipfile` + `xml.etree.ElementTree`, `parser="zip-xml"`, `section` 칸)입니다.
- **03과 겹치지 않게**: 03이 「형식마다 구조 정보가 붙은 자리가 다르다」와 「표가 어디에 들어 있는가」를 다뤘습니다. 04는 **같은 이름의 두 형식이 파일 안에서 얼마나 다른가**(이진 파일 대 압축 파일)와 **압축 파일을 풀어 XML에서 글을 꺼내는 일**에 무게를 두세요. 「형식마다 남는 구조 정보」 표를 되풀이하지 마세요.
- 04절이 `zipfile`·`ElementTree`를 쓰면 **Part 1·2와 01~03절에서 가르치지 않은 것**입니다. 규격 §4 세 문장(뜻 → 일상 예 → 코드)으로 풀고, `with zipfile.ZipFile(...) as ...`는 03절 `with open(...)`·02절 `with pdfplumber.open(...)` 뒤라 세 번째 자리입니다.
- 파일 시그니처를 읽으려면 바이트를 읽어야 합니다(`open(..., "rb")`·`read(8)`·`bytes.fromhex`). Ch 2 05절은 글 모드만 배웠으니 처음 쓰는 자리에 한 문장이 필요합니다.
- **아직 안 가르친 것(04가 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 전체 + 01·02·03에서도 안 한 것 — 글자 인식(OCR) 실행, 선 없는 표·병합 셀 표, 두 단 레이아웃과 읽기 순서, 표가 여러 개인 DOCX와 `iter_inner_content()`, 메뉴·바닥글이 많은 HTML, `table` 태그가 있는 HTML, 태그를 고르지 않고 전체 글 꺼내기, 구분자가 쉼표가 아닌 CSV, BOM이 붙은 CSV, 압축 파일과 XML, 바이트 읽기, 토큰 기준 스플리터, 임베딩·검색·점수(이 챕터 05~08), 실습 폴더 모듈 `import`, `chunk_id`, 여러 문서 한 번에 읽기, 파일 크기·수정 시각 읽기.

### 산출 파일·실습 폴더·묶음

- 03도 `runs/`를 읽지도 쓰지도 않습니다(40개 파일 해시 전후 같음, `455ab5b1…`). 이 챕터 `runs/`를 쓰는 곳은 개선 전 **08절**입니다(§01 → §02의 08절 계약 목록을 그대로 보세요).
- 실습 폴더 테스트 `38 passed`(전후 같음). `document_processing.py`·`experiment.py`·`tests/`·`fixtures/`는 고치지 않았습니다.
- **학생 묶음**: 03이 읽는 `fixtures/sample.docx`·`sample.html`·`sample.csv`는 `build_bundle.py` 31행 `FIXTURES`에 이미 들어 있어 허용 목록을 고치지 않았습니다. 04절 견본 `legacy-signature.hwp`·`minimal-marker.hwpx`도 같은 목록에 있습니다. 새 입력이 생기면 묶음을 `/tmp`에 풀어 **묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리**에서 경로 셀을 돌려 보세요(03에서 세 파일로 확인, 각각 `.`·`../../..`·`../../../..`).
- 절 수는 8개 그대로라 `textbook/part3/_build_index.py`(ch10 칸 8)와 `qa/visual-results.json` 행 수는 고치지 않았습니다.

## §04 → §05

(04절 품질 개선 2026-09-18. 결과는 `04-diagnosis.md`, 게이트 G1~G7 0(수정 전 G2 2·G5 10·G6 31·G7 3 = 46), 코드 셀 24(준비 2), 검사 문장 442(검토 반영 뒤 게이트 값. 절 작업 기록 339는 틀렸습니다), **서비스 요청 0번**(모델·임베딩 없음, API 키 없이 실행), 새 커널로 두 번 이어 실행해 24개 셀 출력 값이 모두 같음(교재 출력은 마지막 실행 2026-09-18T03:37:02Z). 삽화 04-5 1차 채택(job `ed86ddc5-…`, 2크레딧, 잔액 2802), Mermaid 4장. **빌드 도구·챕터 밖 파일 변경 0건**)

### 04가 확인한 실행 환경 (§01 → §02 ~ §03 → §04 그대로 쓸 수 있음)

- `run_section.sh textbook/part3/ch10-document-processing 05`로 생성기 → 새 커널 → 렌더 → 첨부 → 빌드 → 게이트가 한 번에 돌아갑니다. `chapter.json`이 없어 verify는 따로:
  `UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch10-document-processing uv run --project labs/part3/ch10-document-processing python textbook/_notebook/verify.py --chapter textbook/part3/ch10-document-processing`
  → 04 뒤 `PASS 8 sections / 118 code cells (max 24 lines)`(03 뒤 102).
- 04 뒤 디스크 HTML 기준: `/tmp/ch10-04/hash/final.txt`. 작업 전후 `sha256sum *.html`로 다른 절이 바뀌지 않았는지 보세요(04에서는 04 HTML만 `da5c8dbb…` → `0aef680f…`).
- `visual.cjs`·묶음 풀기·삽화 저장 방법은 §01 → §02와 같습니다. `.cache/vm/shot/`에 검수용 캡처를 두었습니다(`ch10-04-cand1.png`·`ch10-04-page-illu.png`·`ch10-04-page-mmd3.png`).
- 기기 루트 여유 약 498MB. 작업 폴더 `/tmp/ch10-04`(해시·탐색 실행·묶음·삽화 원본·visual 사본·화면 캡처).
- **게이트 라벨**: 04는 `--label wip --section 04`만 돌렸습니다(`gates-wip-04.json`). `gates-after-04.json`은 만들지 않았습니다. 라벨을 `after-04`처럼 주면 파일 이름이 `gates-after-04-04.json`이 되므로 라벨은 `wip`이나 `after`만 주세요.
- **두 번 실행 결과**: 값은 모두 같았고 `outputs_sha256`은 달랐습니다(`f3f04a12…` → `f471de84…`). 차이는 `%pip` 셀 출력이 한 덩이일 때와 두 덩이일 때가 있는 것뿐입니다(02·03절과 같은 현상). 해시만 보지 말고 셀 단위로 값을 대조하세요.
- **Mermaid 라벨 줄바꿈**: 공용 `config.json`에 줄바꿈 폭 설정이 없어 한 줄기 흐름도는 폭이 약 255로만 나옵니다. 그러면 페이지에서 2배 이상 늘어나 아주 길어집니다(04-2 첫 판 255.8×723.4). 가지를 옆으로 두거나 `<br>`을 넣어 폭을 500 이상으로 만들고, 그래도 868을 넘으면 라벨을 줄이세요(04-4 첫 판 877.3 → 809.5).

### 용어 (04에서 정한 것, 05~08도 같게)

- **01절 네 말**(파서·파일 형식·출처 기록·출처 계보), **02절 네 말**(글자 층·표 읽기·글자 인식·OCR 후보 쪽), **03절 네 말**(문단·꾸밈 이름·태그·자리 칸), Ch 9 용어를 그대로 씁니다. 04가 새로 정한 말은 네 개입니다: **형식 표시(file signature)**, **이진 파일(binary file)**, **압축 묶음(ZIP)**, **이름 공간(namespace)**.
- **「형식 표시」와 03절 「파일 앞 표시(BOM)」는 다른 것입니다.** 형식 표시는 파일 맨 앞에서 형식을 알리는 값이고, 03절 BOM은 글자 인코딩을 알리는 표시입니다. 두 말을 섞지 마세요.
- 「ZIP 컨테이너」·「네임스페이스」·「HWP 네이티브 형식」·「OWPML」은 쓰지 않았습니다(차례로 → 압축 묶음, 이름 공간, 「형식 HWP」, 규격 이름은 b2에 한 번만).
- `parser` 값 이름: 01 `pypdf-plain`, 02 `pdfplumber`, 03 `python-docx`·`beautifulsoup`·`csv.DictReader`, **04 `zip-xml`**. 여섯 개가 되었고 모두 실습 폴더 `document_processing.py`가 쓰는 글과 같습니다.
- 갈래 이름은 한국어로 두었습니다: `hwp-후보`·`hwpx`·`모름`. 실습 폴더 모듈 `recognize_hwp_kind()`는 같은 갈래를 `ole-candidate`·`hwpx`·`unknown`으로 적습니다(본문 b7에 적어 두었습니다).

### 04에서 새로 가르친 것

- **API·동작(노트북에서 실행한 것만)**: `open(file_path, "rb")`·`read(8)`·`bytes.hex()`(이진 파일로 읽는 첫 자리 — 노트북 3절 설명 셀에 뜻 → 일상 예 → 코드), `import zipfile`·`zipfile.is_zipfile(경로)`·`with zipfile.ZipFile(경로) as archive:`(라이브러리 객체에 `with`를 쓰는 **세 번째 자리** — 02절 `pdfplumber.open()`·03절 `open()` 뒤)·`archive.namelist()`·`archive.read(이름)`, `from xml.etree import ElementTree`·`ElementTree.fromstring(바이트)`·`root.tag`·`root.iter()`·`node.text`, 글 `startswith()`·`endswith()`·`split("}")[-1]`, `try/except zipfile.BadZipFile as error`(점을 이은 오류 이름은 Ch 4 모양)·`type(error).__name__`·`str(error)`.
- **Python 모양**: `continue`로 건너뛰기, `node.text is not None`으로 값 없음 가리기, 함수가 함수 밖 이름을 읽기(Ch 5 모양 — `ole_marker`·`section_names`·`wanted_name`), 함수가 함수를 부르기(`read_hwpx_body` → `read_body_text` → `make_local_name`), 정의 셀에 이름 하나를 함께 두기(`ole_marker` + `recognize_file_kind`, 값을 식 안에 그대로 쓰지 않으려고).
- **01~03절이 안 쓴 것 가운데 04도 안 쓴 것**: `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`raise`·`+=`·`enumerate`·`zip`·`sum`·`max`·`any`·`all`·`isinstance`·`join`·f-string 안 계산·타입힌트·`@`·`BaseModel`·모델 문장 `assert`·`Path.cwd()`·`parents`.
- **함수 본문 10줄(규격 §2-2 L2)**: `read_head_hex` 3줄 · `make_local_name` 1줄 · `read_body_text` 8줄 · `make_unit_record` 6줄(03절과 같은 코드) · `make_unit_mark` 6줄(03절과 같은 코드) · `make_section_mark` 6줄 · `recognize_file_kind` 6줄 · `read_hwpx_body` 4줄. 셀 최대 12줄(Before 셀).
- **이어 쓸 이름과 값**: `candidates`·`root_path`(교재 출력 `.`), `fixtures_path`(01·03절과 같은 이름), `hwp_path`·`hwpx_path`, `read_head_hex(file_path)`·`hwp_head`·`hwpx_head`, `hwp_is_zip`·`hwpx_is_zip`, `entry_names`(2개)·`section_names`(1개), `xml_bytes`(204바이트)·`root`·`make_local_name(tag_name)`·`local_names`, `read_body_text(xml_root, wanted_name)`·`wanted_name = "t"`·`body_text`(15자), `make_unit_record(file_path, parser)`·`hwpx_record`·`make_unit_mark(chunk)`·`make_section_mark(chunk)`·`hwpx_document`·`unit_mark`·`section_mark`, `changed_name = "p"`·`changed_text`, Before `opened_names`·`error_name`·`error_message`, After `ole_marker`·`recognize_file_kind(file_path)`·`read_hwpx_body(file_path)`·`read_report`.
- **출력 라벨(전부)**: 「고른 경로:」「HWP 견본이 있는가:」「HWPX 견본이 있는가:」「HWP 견본의 앞 여덟 바이트:」「HWPX 견본의 앞 여덟 바이트:」「두 값이 같은가:」「HWP 견본이 압축 묶음인가:」「HWPX 견본이 압축 묶음인가:」「압축 묶음 안의 항목 수:」「항목 이름:」「본문 XML 수:」「본문 XML 이름:」「꺼낸 바이트 수:」「맨 위 요소의 태그 이름:」「요소 수:」「요소 이름:」「고른 요소 이름:」「본문 글자 수:」「본문:」「HWPX 기록:」「기록의 칸 수:」「page 칸이 있는가:」「section 칸의 값:」「메타데이터 칸 수:」「row 칸을 보는 표시:」「section 칸을 보는 표시:」「바꾼 요소 이름:」「빈 글인가:」「읽은 항목 이름 목록:」「받은 오류 이름:」「받은 오류 글:」「갈래별 결과:」
- **실행값(2026-09-18, 새 커널 두 번 값 같음)**: `langchain-core: 1.6.2`, `고른 경로: .`, 견본 두 줄 모두 `True`, `d0cf11e0a1b11ae1`·`504b030414000000`·`두 값이 같은가: False`, 압축 묶음 `False`·`True`, `항목 수: 2`·`['Contents/content.hpf', 'Contents/section0.xml']`, `본문 XML 수: 1`·`['Contents/section0.xml']`, `꺼낸 바이트 수: 204`·`{http://www.hancom.co.kr/hwpml/2011/paragraph}section`, `요소 수: 4`·`['section', 'p', 'run', 't']`, `본문 글자 수: 15`·`한글 문서 처리 실습입니다.`, `{'doc_id': 'minimal-marker', 'source': 'minimal-marker.hwpx', 'file_type': 'hwpx', 'parser': 'zip-xml', 'section': 1}`·`기록의 칸 수: 5`·`page 칸이 있는가: False`·`section 칸의 값: 1`, `[minimal-marker hwpx]`·`[minimal-marker hwpx section.1]`, 값 바꿔 보기 `본문 글자 수: 0`·`빈 글인가: True`, Before `읽은 항목 이름 목록: []`·`BadZipFile`·`File is not a zip file`, After `{'hwp-후보': '전용 도구가 필요합니다', 'hwpx': '한글 문서 처리 실습입니다.'}`.
- **견본 두 개 읽기 결과(05~08절이 쓸 값)**: `legacy-signature.hwp`는 23바이트 이진 파일이고 앞 여덟 바이트가 `d0cf11e0a1b11ae1`이어서 압축 묶음이 아닙니다. `minimal-marker.hwpx`는 470바이트 압축 묶음이고 항목이 `Contents/content.hpf`(`<package/>` 한 줄, 노트북에서 내용을 출력하지 않음)와 `Contents/section0.xml`(204바이트) 두 개입니다. 본문 XML의 요소는 `section` → `p` → `run` → `t` 네 겹이고 글은 `t`에만 있습니다(`한글 문서 처리 실습입니다.` 15자, 마침표 포함).
- **결론 태도(01~03·Ch 9와 같음)**: 「이번 실행에서는」, 형식 표시 하나로 형식을 단정하지 않음(`hwp-후보`), **After도 HWP 본문을 읽은 것이 아님**(두 실행 모두 HWP 본문 0건, 04-4 맨 아래 회색 상자), 실행하지 않은 동작은 「이번에 실행하지 않았습니다」.

### 쪽 번호가 없는 형식의 자리 칸 (04가 결정했습니다 — 05~08절이 그대로 이어받을 것)

- HWPX 기록은 03절 네 칸에 **자리 칸 `section` 하나**를 더한 다섯 칸입니다. 번호는 **1부터** 셉니다(03절 CSV `row`는 첫 줄이 칸 이름 줄이어서 2부터).
- **`make_unit_mark()`는 고치지 않았습니다.** `row` 칸만 읽으므로 HWPX 기록에서는 `[minimal-marker hwpx]`까지만 나옵니다. 노트북 9절에서 그 결과를 출력으로 보이고, `section` 칸을 읽는 **`make_section_mark()`**를 하나 더 만들어 `[minimal-marker hwpx section.1]`을 얻었습니다. 같은 이름으로 다시 정의하지 않았습니다.
- 그래서 이 챕터에는 출처 표시 함수가 세 개입니다: `make_source_mark()`(01·02, `page`) · `make_unit_mark()`(03, `row`) · `make_section_mark()`(04, `section`). 05절 이후 형식이 섞인 글을 다룰 때 **어느 함수를 쓸지 정하고 본문에 한 문장 적으세요.** 실습 폴더 모듈은 문서 청크 이름을 만들 때 `page`·`section`·`row`를 차례로 보고 먼저 있는 칸 하나를 씁니다(`document_processing.py` `_with_chunk_metadata()`). 세 함수를 하나로 합치려면 그 모듈과 같은 순서를 쓰되 01절 `[E01 p.2]` 모양이 바뀌지 않게 하세요.

### 05절이 이어받을 연결과 확인할 것

- 04 b8·노트북 정리 끝: 「05절에서는 이렇게 읽은 글을 작은 문서 청크로 나눕니다. 같은 글을 세 가지 방식으로 나누고 나눈 자리와 길이를 견줍니다. 그때도 이 절에서 적은 출처 기록이 문서 청크마다 따라갑니다.」
- **개선 전 05 노트북**을 먼저 읽으세요. `langchain-text-splitters==1.1.2`·`tiktoken==0.14.0`을 설치하고 `CharacterTextSplitter(separator=" ", chunk_size=35, chunk_overlap=5)`·`RecursiveCharacterTextSplitter(separators=["\n\n", ". ", " ", ""], chunk_size=35/50, chunk_overlap=5, keep_separator="end")`·`RecursiveCharacterTextSplitter.from_tiktoken_encoder(encoding_name="cl100k_base", chunk_size=20, chunk_overlap=4)`·`tiktoken.get_encoding("cl100k_base")`·`split_text()`를 씁니다. 원문은 노트북 안에 적은 배송·환불 안내 두 문단이고, Before/After는 「35자 설정에서 두 근거가 나뉨 → 50자 설정에서 한 청크에 담김」입니다(`required_facts = ["결제 다음 날", "제주 지역은 이틀"]`).
- 개선 전 05가 쓰는 것 가운데 **01~04절·Part 1·2에서 안 가르친 것**: `all(...)`+제너레이터 식, `enumerate(..., start=1)`, f-string 안 `{chunk!r}`·계산, `try/except AssertionError`, 한 셀에 여러 스플리터 만들기, `keep_separator=` 인자, `from_tiktoken_encoder()`. **Ch 9 02절이 가르친 것**: `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)`·`split_documents()`·`tiktoken.encoding_for_model("text-embedding-3-small")` → 규칙 `cl100k_base`·`count_tokens(text)`. 토큰 기준 스플리터(`from_tiktoken_encoder`·`TokenTextSplitter`)는 Ch 9가 「설치판에 있다고만」 적었으므로 05가 처음 가르칩니다.
- **04와 겹치지 않게**: 04는 「같은 이름의 두 형식이 파일 안에서 다르다」와 「압축 묶음 속 XML에서 글을 꺼내기」를 다뤘습니다. 05는 **꺼낸 글을 어디에서 끊는가**에 무게를 두세요. 형식 가르기·출처 기록 만들기를 되풀이하지 말고, 문서 청크마다 기록이 따라간다는 것만 이어 쓰면 됩니다.
- **원문 결정**: 개선 전 05는 노트북 안에 적은 짧은 글을 씁니다. 01·02절이 읽은 `E01.pdf` 2쪽 글(905자)이나 03·04절 견본 글을 쓸 수도 있습니다. Ch 9 02절은 E01 500/50 문서 청크 8개(`1|45`·`2|498`·`2|452`·`3|498`·`3|462`·`4|492`·`4|412`·`5|270`)와 300/50이면 14개를 이미 보였으므로, **E01로 같은 크기를 다시 견주면 Ch 9 02절과 겹칩니다.** 어느 글을 골라도 까닭을 본문에 한 문장 적어 주세요.
- **아직 안 가르친 것(05가 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 전체 + 01~04에서도 안 한 것 — 본문 XML이 여러 개인 HWPX, 표·각주·그림이 든 HWPX, 문서 규격의 요소 순서, HWP 전용 도구·변환 도구 실행, 암호가 걸린 문서, 글자 인식(OCR) 실행, 선 없는 표·병합 셀 표, 두 단 레이아웃, 표가 여러 개인 DOCX와 `iter_inner_content()`, `table` 태그가 있는 HTML, 구분자가 쉼표가 아닌 CSV, BOM이 붙은 CSV, 토큰 기준 스플리터, 임베딩·검색·점수(이 챕터 06~08), 실습 폴더 모듈 `import`, `chunk_id`, 여러 문서 한 번에 읽기, 파일 크기·수정 시각 읽기.

### 산출 파일·실습 폴더·묶음

- 04도 `runs/`를 읽지도 쓰지도 않습니다(40개 파일 해시 전후 같음, `455ab5b1…`). 이 챕터 `runs/`를 쓰는 곳은 개선 전 **08절**입니다(§01 → §02의 08절 계약 목록을 그대로 보세요).
- 실습 폴더 테스트 `38 passed`(전후 같음). `document_processing.py`·`experiment.py`·`tests/`·`fixtures/`는 고치지 않았습니다(모듈 두 개와 견본 다섯 개 해시 `1df615e1…`).
- **학생 묶음**: 04가 읽는 `fixtures/legacy-signature.hwp`·`minimal-marker.hwpx`는 `build_bundle.py` 31행 `FIXTURES`에 이미 있어 허용 목록을 고치지 않았습니다. 묶음을 `/tmp/ch10-04/bundle`에 풀어 **묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리**에서 경로 셀을 돌려 모두 찾았고(`.`·`../../..`·`../../../..`), 묶음 사본과 저장소 원본의 해시도 같습니다. 05절이 새 입력을 읽게 되면 같은 방법으로 확인하세요.
- 절 수는 8개 그대로라 `textbook/part3/_build_index.py`(ch10 칸 8)와 `qa/visual-results.json` 행 수는 고치지 않았습니다.
- 루트 `textbook/qa/upgrade-progress.md`의 Ch 10 행은 아직 「절 개선 중(01 완료)」입니다. 챕터 밖 파일이라 절 작업자가 고치지 않았습니다(02·03·04 모두 같음). 오케스트레이터 몫입니다.

## §05 → §06

(05절 품질 개선 2026-09-18. 결과는 `05-diagnosis.md`, 게이트 G1~G7 0(수정 전 G1 2·G3 1·G5 11·G6 22·G7 3 = 39), 코드 셀 24(준비 2), 검사 문장 409, **서비스 요청 0번**(모델·임베딩 없음, API 키 없이 실행), 새 커널로 두 번 이어 실행해 `outputs_sha256` `18851bbd…` 같음(교재 출력은 마지막 실행 2026-09-18T04:16:42Z). 삽화 05-5 2차 채택(1차 `c6660167-…` 탈락, 2차 `25a3ed40-…`, 4크레딧, 잔액 2798), Mermaid 4장. **빌드 도구·챕터 밖 파일 변경 0건**)

### 05가 확인한 실행 환경 (§01 → §02 ~ §04 → §05 그대로 쓸 수 있음)

- `run_section.sh textbook/part3/ch10-document-processing 06`으로 생성기 → 새 커널 → 렌더 → 첨부 → 빌드 → 게이트가 한 번에 돌아갑니다. `chapter.json`이 없어 verify는 따로:
  `UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch10-document-processing uv run --project labs/part3/ch10-document-processing python textbook/_notebook/verify.py --chapter textbook/part3/ch10-document-processing`
  → 05 뒤 `PASS 8 sections / 134 code cells (max 24 lines)`(04 뒤 118).
- 05 뒤 디스크 HTML 기준: `/tmp/ch10-05/hash/final.txt`. 작업 전후 `sha256sum *.html`로 다른 절이 바뀌지 않았는지 보세요(05에서는 05 HTML만 `77490c4a…` → `f1981402…`).
- `visual.cjs`·묶음 풀기·삽화 저장 방법은 §01 → §02와 같습니다. `.cache/vm/shot/`에 검수용 캡처를 두었습니다(`ch10-05-cand1.png`·`ch10-05-cand2.png`·`ch10-05-page-illu.png`·`ch10-05-page-mmd3.png`).
- 기기 루트 여유 약 479MB. 작업 폴더 `/tmp/ch10-05`(해시·탐색 실행·묶음·삽화 원본·visual 사본, 19MB).
- **게이트 라벨**: 05도 `--label wip --section 05`만 돌렸습니다(`gates-wip-05.json`).
- **두 번 실행 결과**: 값과 `outputs_sha256`이 모두 같았습니다(`18851bbd…`). 02~04절에서 보였던 `%pip` 출력 덩이 차이가 이번에는 나오지 않았습니다. 해시가 달라도 셀 단위로 값을 대조하면 됩니다.
- **`tiktoken` 규칙 파일**: `tiktoken.get_encoding("cl100k_base")`는 규칙 파일이 없으면 한 번 내려받습니다. 기기에는 2026-09-17(Ch 9 작업)에 저장된 파일이 `$TMPDIR/data-gym-cache/`에 있어 이번 실행에서는 내려받지 않았습니다. 그래서 「모델과 임베딩에 요청을 보내지 않는다」로 적고 「인터넷에 아무 요청도 보내지 않는다」로는 적지 않았습니다.
- **06절은 이 챕터에서 처음으로 서비스에 요청을 보냅니다**(개선 전 06이 `OpenAIEmbeddings(model="text-embedding-3-small", dimensions=256)`를 씀). 키는 루트 `.env`, 준비 셀은 `nbkit.KEY`를 쓰고 준비물에 호출 수·예상 비용·실행일을 적으세요(규격 §3). 01~05절 준비물 문장(「API 키가 필요 없습니다」)을 그대로 복사하지 마세요.

### 용어 (05에서 정한 것, 06~08도 같게)

- **01절 네 말**(파서·파일 형식·출처 기록·출처 계보), **02절 네 말**(글자 층·표 읽기·글자 인식·OCR 후보 쪽), **03절 네 말**(문단·꾸밈 이름·태그·자리 칸), **04절 네 말**(형식 표시·이진 파일·압축 묶음·이름 공간), Ch 9 용어를 그대로 씁니다. 05가 새로 정한 말은 네 개입니다: **문자 방식(character splitter)**, **재귀 방식(recursive splitter)**, **토큰 방식(token splitter)**, **조각 수 한도**.
- 세 「방식」 이름은 실습 폴더 `document_processing.py`가 `chunk_method` 칸에 적는 `char`·`recursive`·`token`과 짝입니다. 06절 구조·시맨틱 나누기는 같은 파일에서 `structural`·`semantic`입니다.
- **한정어 없는 「청크」를 쓰지 않습니다**(규격 §4). 05는 개선 전 본문의 「청크」를 모두 「문서 청크」로 바꿨습니다. 「조각」은 Ch 5 토큰 뜻 전용입니다.
- **「겹침」**(Ch 9 02절 말)을 씁니다. 「오버랩」은 쓰지 않았습니다.
- **「끊을 자리 순서」**는 Ch 9 02절 뜻(separators 목록)이고, **「끊는 자리」**는 실제로 갈라진 자리입니다. 두 말을 섞지 마세요.
- **「지킬 말」**은 Ch 8 03절 뜻(사람이 원문에서 고른 꼭 남길 말)입니다. 05는 `정기 휴관일`·`화요일에도 휴관` 두 개를 골랐습니다.
- 쓰지 않은 말: 「청킹」, 「오버랩」, 「구분자 우선순위」(→ 끊을 자리 순서), 「스플리터 객체」(→ 스플리터), 「승자」, 「유니코드 경계」(실행하지 않아 항목을 뺐습니다).

### 05에서 새로 가르친 것

- **API·동작(노트북에서 실행한 것만)**: `CharacterTextSplitter(separator=, chunk_size=, chunk_overlap=)`·`split_text(글)`(노트북 3절 설명 셀에 뜻 — Ch 9 02절 `split_documents()`와 받는 값이 다름), `RecursiveCharacterTextSplitter(separators=, chunk_size=, chunk_overlap=, keep_separator="end")`(4절, `keep_separator` 뜻 한 문장), `splitter.split_documents([Document])`(6절, Ch 9 02절과 같은 메서드), `tiktoken.get_encoding("cl100k_base")`(7절 — Ch 9 02절은 `encoding_for_model()`로 같은 규칙 이름을 얻었음), `RecursiveCharacterTextSplitter.from_tiktoken_encoder(encoding_name=, separators=, chunk_size=, chunk_overlap=, keep_separator=)`(10절, 클래스 이름에 점을 붙여 부르는 첫 자리), 글 안의 줄바꿈 표시 `"\n"`과 `split("\n")`(2절).
- **Python 모양**: 목록을 받아 목록을 반환하는 함수(`make_length_list`·`make_token_list`), 번호를 1부터 세며 모으기(`find_chunks_with_words`·`find_over_limit`), 빈 목록과 견주기(`missing == []`), 목록끼리 견주기(`changed_texts == character_texts`), 글끼리 견주기(`first_chunk.page_content == recursive_texts[0]`), 함수가 함수 밖 이름을 읽기(`count_tokens`가 `encoding`을, Ch 5·04절 모양), 정의 셀에 이름 하나를 함께 두기(`encoding` + `count_tokens`).
- **01~04절이 안 쓴 것 가운데 05도 안 쓴 것**: `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·try·`raise`·`with`·`+=`·`enumerate`·`zip`·`sum`·`max`·`any`·`all`·`isinstance`·`join`·f-string 안 계산·타입힌트·`@`·`BaseModel`·모델 문장 `assert`·`Path.cwd()`·`parents`.
- **함수 본문 10줄(규격 §2-2 L2)**: `load_pdf_pages` 9줄(01절과 같은 코드) · `make_length_list` 4줄 · `find_missing_words` 5줄(Ch 9 02절과 같은 코드) · `find_chunks_with_words` 8줄 · `make_source_record` 6줄(01절) · `make_source_mark` 4줄(01절) · `count_tokens` 1줄(Ch 9 02절) · `make_token_list` 4줄 · `find_over_limit` 7줄. 셀 최대 12줄(재귀 스플리터 셀).
- **이어 쓸 이름과 값**: `candidates`·`root_path`(교재 출력 `.`), `corpus_path`·`pdf_path`(= `corpus_path + "/pdf/easy/E01.pdf"`), `pages`·`plain_text`(905자)·`text_lines`(26줄), `make_length_list(chunk_texts)`, `character_splitter`·`character_texts`(6개)·`character_lengths`, **`separator_order = ["\n\n", ". ", "\n", " ", ""]`**·`recursive_splitter`·`recursive_texts`(6개)·`recursive_lengths`, `find_missing_words(text, words)`·`find_chunks_with_words(chunk_texts, words)`·`closure_words = ["정기 휴관일", "화요일에도 휴관"]`·`character_found`·`recursive_found`·`missing_in_second`, `make_source_record(file_path, page, parser)`·`make_source_mark(chunk)`(01절과 같은 코드)·`page_two_record`·`page_two_document`·`chunk_documents`(6개)·`first_chunk`·`last_chunk`, `encoding`·`count_tokens(text)`·`make_token_list(chunk_texts)`·`whole_tokens`(869)·`recursive_tokens`, `changed_order = ["\n\n", "\n", ". ", " ", ""]`·`changed_splitter`·`changed_texts`, `find_over_limit(token_counts, limit)`·`token_limit = 150`·`recursive_over`, `token_splitter`·`token_texts`(13개)·`token_counts`·`token_over`.
- **출력 라벨(전부)**: 「pypdf:」「langchain-core:」「langchain-text-splitters:」「tiktoken:」「고른 경로:」「나눌 글의 글자 수:」「나눌 글의 줄 수:」「빈 줄이 있는가:」「문자 방식 문서 청크 수:」「문서 청크별 문자 수:」「문자 방식 셋째 문서 청크의 문자 수:」「문자 방식 셋째 문서 청크:」「끊을 자리 순서:」「재귀 방식 문서 청크 수:」「재귀 방식 둘째 문서 청크:」「재귀 방식 셋째 문서 청크:」「지킬 말 두 개:」「문자 방식에서 둘 다 든 문서 청크 번호:」「재귀 방식에서 둘 다 든 문서 청크 번호:」「재귀 방식 둘째에서 빠진 말:」「문서 청크 Document 수:」「첫 문서 청크의 메타데이터 칸 수:」「첫 문서 청크의 출처 표시:」「마지막 문서 청크의 출처 표시:」「첫 문서 청크 본문이 앞의 결과와 같은가:」「나눌 글 전체의 조각 수:」「재귀 방식 문서 청크의 조각 수:」「재귀 방식 문서 청크의 문자 수:」「바꾼 끊을 자리 순서:」「문자 방식 결과와 같은가:」「문서 청크 하나의 조각 수 한도:」「한도를 넘은 문서 청크 번호:」「토큰 방식 문서 청크 수:」「문서 청크별 조각 수:」
- **실행값(2026-09-18, 새 커널 두 번 같음)**: `pypdf: 6.18.0`·`langchain-core: 1.6.2`·`langchain-text-splitters: 1.1.2`·`tiktoken: 0.14.0`, `고른 경로: .`, `나눌 글의 글자 수: 905`·`줄 수: 26`·`빈 줄이 있는가: False`, 문자 방식 `6`·`[156, 156, 184, 172, 152, 80]`·셋째 `184`자, 재귀 방식 `['\n\n', '. ', '\n', ' ', '']`·`6`·`[185, 147, 86, 164, 130, 188]`, 지킬 말 `['정기 휴관일', '화요일에도 휴관']`·문자 방식 `[3]`·재귀 방식 `[]`·둘째에서 빠진 말 `['화요일에도 휴관']`, `문서 청크 Document 수: 6`·`메타데이터 칸 수: 5`·`[E01 p.2]`(첫·마지막 같음)·`True`, `나눌 글 전체의 조각 수: 869`·재귀 방식 조각 수 `[190, 133, 92, 155, 120, 177]`, 값 바꿔 보기 `['\n\n', '\n', '. ', ' ', '']`·`[156, 156, 184, 172, 152, 80]`·`문자 방식 결과와 같은가: True`, Before `한도: 150`·`[1, 4, 6]`, After `13`·`[54, 52, 83, 81, 52, 92, 75, 79, 76, 43, 59, 85, 33]`·`[]`·문자 수 `[52, 49, 82, 92, 54, 86, 77, 86, 85, 44, 62, 88, 36]`.
- **E01 2쪽 나누기 결과(06~08절이 쓸 값)**: 이 글에는 빈 줄이 없어 끊을 자리 순서의 첫 후보가 쓰이지 않습니다. 목표 200자에서 문자 방식(경계 `"\n"`)과 재귀 방식(문장 끝 우선) 모두 문서 청크 6개이고, 재귀 방식 쪽이 길이가 더 들쭉날쭉합니다(86~188자). 끊을 자리 순서를 줄 우선으로 바꾸면 **문자 방식 결과와 본문까지 같아집니다**. 조각 수는 문자 수보다 큰 자리가 있습니다(185자에 190조각). 탐색 실행에서만 본 값(본문에는 없음): 문자 방식 문서 청크의 조각 수 `[163, 141, 187, 156, 148, 72]`, 목표 120조각이면 문서 청크 11개.
- **조각 수 한도 150**: 사람이 정한 값입니다. 탐색 실행에서 조각 수가 92~190인 것을 본 뒤 「근거 세 개에 450조각」 계산과 맞춰 골랐고, 과정과 「흐름을 보여 주려고 정한 예」를 본문 b7 첫 항목에 적었습니다(규격 §3, 02절 기준값 20과 같은 방식).
- **설치판 소스로 확인한 동작(langchain-text-splitters 1.1.2)**: `CharacterTextSplitter`는 기본 구분자 `"\n\n"` 하나만 쓰고 `keep_separator` 기본값이 `False`라 합칠 때 구분자를 다시 넣습니다. `RecursiveCharacterTextSplitter`는 `keep_separator` 기본값이 `True`라 구분자가 뒤 조각 앞에 붙고 `"end"`를 주면 앞 조각 끝에 남습니다. `_merge_splits`는 조각 하나가 목표보다 길면 경고를 적습니다(이번 실행에서는 나오지 않았습니다).
- **결론 태도(01~04·Ch 9와 같음)**: 「이번 실행에서는」, 어느 나누기가 검색에 더 나은지 판정하지 않음(검색을 돌리지 않았음), 두 방식 결과가 같아진 것도 「이 글에서는」으로 한정, 실행하지 않은 동작은 「이번에 실행하지 않았습니다」.

### 문서 청크에 기록을 붙이는 방법 (05가 정했습니다 — 06~08절이 그대로 이어받을 것)

- `split_text()`는 **글 목록**을 반환하므로 기록이 따라가지 않습니다. `Document`를 만들어 **`split_documents([page_two_document])`**로 나누면 다섯 칸 기록이 문서 청크마다 복사됩니다(노트북 6절 `첫 문서 청크의 메타데이터 칸 수: 5`).
- 쪽이 있는 형식이라 **01절 `make_source_mark()`**(칸 `page`)를 썼습니다. 쪽이 없는 형식이면 03절 `make_unit_mark()`(칸 `row`)나 04절 `make_section_mark()`(칸 `section`)를 골라야 합니다. 세 함수는 그대로 두었고 같은 이름으로 다시 정의하지 않았습니다.
- **여섯 문서 청크의 출처 표시가 모두 `[E01 p.2]`로 같습니다.** 쪽 안에서 몇 번째인지는 이 기록에 없습니다. 문서 청크 이름(`chunk_id`)은 이 절에서 붙이지 않았고, 실습 폴더 `document_processing.py` `_with_chunk_metadata()`가 `E01:page2:recursive:0` 모양으로 붙입니다(칸 `chunk_id`·`chunk_method`). 08절 기록의 `chunk_id`는 `ch10:recursive:0000`이라 모양이 또 다릅니다(§01 → §02의 08절 계약과 Ch 9 검토 B R-3).
- **실습 폴더 `split_char()`는 라이브러리 `CharacterTextSplitter`와 모양이 다릅니다.** 모듈은 구분자를 쓰지 않고 문자 수로 글을 그대로 자릅니다(`doc.page_content[start:start + chunk_size]`). 같은 파일 `split_recursive()`·`split_token()`은 노트북과 같은 클래스를 쓰지만 끊을 자리 순서가 `["\n\n", "\n", "다. ", ". ", " ", ""]`로 다릅니다(줄이 문장보다 앞, 한국어 종결 어미 표시 있음). 본문 b7에 두 항목으로 적었습니다.

### 06절이 이어받을 연결과 확인할 것

- 05 b8·노트북 정리 끝: 「06절에서는 길이가 아니라 글의 구조와 뜻으로 끊는 자리를 정합니다. 제목 표시가 바뀌는 자리에서 나누고, 문장 사이의 거리로 나누는 방법을 견줍니다. 그때도 이 절에서 본 대로 나눈 결과의 수와 길이를 함께 확인합니다.」
- **개선 전 06 노트북**을 먼저 읽으세요. `python-dotenv==1.2.3`·`langchain-openai==1.6.0`·`langchain-text-splitters==1.1.2`·`langchain-experimental==0.4.2`를 설치하고, `MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "section"), ("##", "topic")])`·`split_text(markdown_text)`와 `SemanticChunker(embeddings)`·`create_documents([글])`·`breakpoint_threshold_type="percentile"`·`breakpoint_threshold_amount=50`·`0`을 씁니다. 원문은 노트북 안에 적은 배송·환불 Markdown과 여덟 문장짜리 글입니다.
- **05와 겹치지 않게**: 05는 「무엇을 길이로 세는가」와 「끊을 자리 순서」를 다뤘습니다. 06은 **글에 이미 있는 구조 표시**와 **문장 사이의 뜻 차이**로 끊는 자리를 정하는 데 무게를 두세요. 「목표 크기를 바꿔 문서 청크 수를 견주기」는 Ch 9 02·07절과 05절에서 이미 했습니다.
- **원문 결정**: 개선 전 06은 노트북 안에 적은 글을 씁니다. 01~05절이 읽은 `E01.pdf` 2쪽 글에는 `#` 같은 제목 표시가 없고 「1. 도서관 소개」·「2. 이용 시간」·「3. 회원 가입」처럼 번호 제목이 줄로만 있습니다(05 노트북 3·4절 출력에서 볼 수 있습니다). 03절 `sample.html`의 `h1` 태그나 `sample.docx`의 꾸밈 이름 `Heading 1`을 제목 표시로 바꿔 쓰는 길도 있습니다. 어느 글을 골라도 까닭을 본문에 한 문장 적어 주세요.
- **기록 결정이 하나 필요합니다.** `MarkdownHeaderTextSplitter`는 제목을 **메타데이터 칸으로 새로 만들어** `Document`를 반환합니다(개선 전 노트북은 칸 이름을 `section`·`topic`으로 두었습니다). 그런데 **`section`은 04절이 HWPX 자리 칸 이름으로 이미 쓰고 있습니다**(`make_section_mark()`가 그 칸을 읽습니다). 칸 이름을 그대로 두면 뜻이 둘이 됩니다. 이름을 바꿀지, 05절처럼 `split_documents()`로 다섯 칸 기록을 먼저 붙이고 제목 칸을 더할지 정해 본문에 한 문장 적으세요.
- **06은 임베딩을 부릅니다.** 개선 전 `SemanticChunker`는 인접 문장 임베딩 거리로 끊을 자리를 정하므로 문장 수만큼 요청이 생깁니다. 준비물에 예상 호출 수·비용·실행일을 적고(규격 §3), Ch 9가 쓴 `text-embedding-3-small`과 같은 이름을 쓰세요. 개선 전 06은 `dimensions=256`을 주는데 Ch 9는 기본값(1536)이었습니다 — 다르게 두려면 까닭을 적으세요.
- 개선 전 06이 쓰는 것 가운데 **01~05절·Part 1·2에서 안 가르친 것**: `warnings.filterwarnings(...)`로 폐기 경고 감추기(`langchain-experimental` is being sunset), `enumerate(..., start=1)`, f-string 안 계산, 한 셀에 스플리터 여러 개 만들기, `create_documents([글])`, 백분위수(percentile) 개념, 딕셔너리를 만들어 `items()`로 도는 비교 셀. 경고를 감추는 줄은 학생에게 보여 줄 필요가 있는지 다시 생각해 보세요(감추면 폐기 예정이라는 사실이 사라집니다).
- **아직 안 가르친 것(06이 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 전체 + 01~05에서도 안 한 것 — 겹침을 준 나누기와 인접 문서 청크의 실제 중복 재기, 여러 쪽·여러 문서를 한 번에 나누기, 02절 표 읽기 결과를 문서 청크로 쓰기, 문서 청크 이름(`chunk_id`), 다른 규칙 이름(`o200k_base`)으로 조각 세기, 임베딩·검색·점수(이 챕터 07~08), 실습 폴더 모듈 `import`, 글자 인식(OCR) 실행, 선 없는 표·병합 셀 표, 두 단 레이아웃, 본문 XML이 여러 개인 HWPX, 암호가 걸린 문서.

### 산출 파일·실습 폴더·묶음

- 05도 `runs/`를 읽지도 쓰지도 않습니다(40개 파일 해시 전후 같음, `1cc170e8…`). 이 챕터 `runs/`를 쓰는 곳은 개선 전 **08절**입니다(§01 → §02의 08절 계약 목록을 그대로 보세요).
- 실습 폴더 테스트 `38 passed`(전후 같음). `document_processing.py`·`experiment.py`·`tests/`·`fixtures/`는 고치지 않았습니다(모듈 두 개 해시 `95b63e9c…`).
- **학생 묶음**: 05가 읽는 입력은 `labs/data/rag-corpus/pdf/easy/E01.pdf` 하나로 01·02절과 같습니다. `build_bundle.py` 63행에 이미 있어 허용 목록을 고치지 않았습니다. 묶음을 `/tmp/ch10-05/bundle`에 풀어 **묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리**에서 경로 셀을 돌려 모두 찾았고(`.`·`../../..`·`../../../..`), 묶음 사본과 저장소 원본의 해시도 같습니다(`cd0ff7d7…`). 06절이 새 입력을 읽게 되면 같은 방법으로 확인하세요.
- 절 수는 8개 그대로라 `textbook/part3/_build_index.py`(ch10 칸 8)와 `qa/visual-results.json` 행 수는 고치지 않았습니다.
- 루트 `textbook/qa/upgrade-progress.md`의 Ch 10 행은 아직 「절 개선 중(01 완료)」입니다. 챕터 밖 파일이라 절 작업자가 고치지 않았습니다(02·03·04·05 모두 같음). 오케스트레이터 몫입니다.

## §06 → §07

(06절 품질 개선 2026-09-18. 결과는 `06-diagnosis.md`, 게이트 G1~G7 0(수정 전 G3 2·G5 11·G6 26·G7 3 = 42), 코드 셀 26(준비 3), 검사 문장 453, **임베딩 요청 2번**(`text-embedding-3-small`, 이 챕터 첫 서비스 요청, 예상 비용 0.001달러 미만), 새 커널로 두 번 이어 실행해 출력 값 62줄이 모두 같음(교재 출력은 마지막 실행 2026-09-18T04:51:49Z). 삽화 06-5 1차 채택(job `f44d613a-…`, 2크레딧, 잔액 2796), Mermaid 4장. **빌드 도구·챕터 밖 파일 변경 0건**)

### 06이 확인한 실행 환경 (§01 → §02 ~ §05 → §06 그대로 쓸 수 있음)

- `run_section.sh textbook/part3/ch10-document-processing 07`로 생성기 → 새 커널 → 렌더 → 첨부 → 빌드 → 게이트가 한 번에 돌아갑니다. `chapter.json`이 없어 verify는 따로:
  `UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch10-document-processing uv run --project labs/part3/ch10-document-processing python textbook/_notebook/verify.py --chapter textbook/part3/ch10-document-processing`
  → 06 뒤 `PASS 8 sections / 152 code cells (max 24 lines)`(05 뒤 134).
- 06 뒤 디스크 HTML 기준: `/tmp/ch10-06/hash/final.txt`. 작업 전후 `sha256sum *.html`로 다른 절이 바뀌지 않았는지 보세요(06에서는 06 HTML만 `be2df150…` → `f497c06a…`).
- `visual.cjs`·묶음 풀기·삽화 저장 방법은 §01 → §02와 같습니다. `.cache/vm/shot/`에 검수용 캡처를 두었습니다(`ch10-06-cand1.png`·`ch10-06-page-illu.png`·`ch10-06-page-mmd3.png`).
- 기기 루트 여유 약 464MB. 작업 폴더 `/tmp/ch10-06`(해시·탐색 실행·묶음·삽화 원본·visual 사본·화면 캡처).
- **게이트 라벨**: 06도 `--label wip --section 06`만 돌렸습니다(`gates-wip-06.json`).
- **키와 요청**: 루트 `.env`를 `nbkit.KEY`가 `find_dotenv(usecwd=True)`로 읽습니다. 06에서 키 확인 셀이 처음 들어갔고 `OPENAI_API_KEY 설정 여부: True`가 나옵니다. 이 챕터에 `langchain` 메인 패키지는 없지만 `langchain_openai`는 있어 임베딩은 그대로 부를 수 있습니다(`init_chat_model`은 06에서도 확인하지 않았습니다).
- **두 번 실행 결과**: 출력 값은 모두 같았고 `outputs_sha256`은 달랐습니다(`b5c417b6…` → `d303aecf…`). 차이는 `langchain-experimental` 폐기 예고 경고 앞의 임시 파일 경로 한 곳뿐입니다(`ipykernel_25` → `ipykernel_29`). 해시만 보지 말고 셀 단위로 값을 대조하세요.
- **Mermaid 폭**: `sequenceDiagram`은 세로줄 이름과 가장 긴 메시지가 폭을 정합니다. 06-3 첫 판이 888이어서 세로줄 이름을 「임베딩 모델」로 줄이고 숫자를 메모로 옮겨 765로 맞췄습니다(868 상한, 규격 §5-3).

### 용어 (06에서 정한 것, 07·08도 같게)

- **01절 네 말**(파서·파일 형식·출처 기록·출처 계보), **02절 네 말**(글자 층·표 읽기·글자 인식·OCR 후보 쪽), **03절 네 말**(문단·꾸밈 이름·태그·자리 칸), **04절 네 말**(형식 표시·이진 파일·압축 묶음·이름 공간), **05절 네 말**(문자 방식·재귀 방식·토큰 방식·조각 수 한도), Ch 9 용어를 그대로 씁니다. 06이 새로 정한 말은 네 개입니다: **구조 방식(structural splitter)**, **시맨틱 방식(semantic splitter)**, **제목 표시(header marker)**, **끊는 기준값(breakpoint threshold)**.
- 다섯 「방식」 이름(문자·재귀·토큰·구조·시맨틱)은 실습 폴더 `document_processing.py`의 `chunk_method` 값 `char`·`recursive`·`token`·`structural`·`semantic`과 짝입니다. 08절 실험 설정에서 이 이름을 그대로 쓰세요.
- **백분위수**는 규격 §4 세 문장으로 b4에 풀었습니다(값을 줄 세운 자리 → 학급 성적 예 → 기준값 95·50의 뜻). 「임계값」·「중단점」은 쓰지 않았습니다.
- 한정어 없는 「청크」를 쓰지 않습니다. 「조각」은 Ch 5 토큰 뜻 전용입니다.
- 쓰지 않은 말: 「구조 기반 청킹」·「의미 경계」·「중단점」·「임계값」·「청킹」(본문에서는 절 제목에만 남음)·「오버랩」·「정규화」·「문맥」.

### 06에서 새로 가르친 것

- **API·동작(노트북에서 실행한 것만)**: `MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "heading")])`·`split_text(글)`(제목 칸만 담은 `Document` 목록 반환, `strip_headers` 기본값 True라 제목 줄은 본문에서 빠짐), `chunk.metadata["heading"]`, `OpenAIEmbeddings(model=)`(Ch 9 03절과 같은 자리, 이 셀은 요청을 보내지 않음), `tiktoken.get_encoding("cl100k_base")`(05절과 같음), `SemanticChunker(embedding_model)`·`SemanticChunker(embedding_model, breakpoint_threshold_amount=50)`·`split_documents([Document])`·속성 `breakpoint_threshold_amount`, 딕셔너리 `copy()`(Ch 2에서 배운 메서드를 이 챕터에서 처음 씀).
- **Python 모양**: 글 슬라이싱으로 규칙 판정(`"." in line[:3] and len(line) < 20`), 글 `+`로 줄을 이어 붙이며 줄바꿈 넣기(02절 `make_row_text` 모양), 딕셔너리 사본에 칸 하나 대입(03절 `csv_record["row"] = 2` 모양), `Document` 목록에서 본문만 모아 05절 함수에 넘기기. 01~05절과 같은 후보 경로 `for`+`break`.
- **01~05절이 안 쓴 것 가운데 06도 안 쓴 것**: `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·try·`raise`·`with`·`+=`·`enumerate`·`zip`·`sum`·`max`·`any`·`all`·`isinstance`·`join`·f-string 안 계산·타입힌트·`@`·`BaseModel`·모델 문장 `assert`·`Path.cwd()`·`parents`·`warnings.filterwarnings`.
- **함수 본문 10줄(규격 §2-2 L2)**: `load_pdf_pages` 9줄(01절) · `mark_heading_line` 3줄 · `make_markdown_text` 6줄 · `make_text_list` 4줄 · `make_length_list` 4줄(05절) · `make_source_record` 6줄(01절) · `make_source_mark` 4줄(01절) · `make_heading_record` 3줄 · `count_tokens` 1줄(05절) · `find_missing_words` 5줄(05절) · `find_chunks_with_words` 8줄(05절). 셀 최대 10줄.
- **이어 쓸 이름과 값**: `candidates`·`root_path`(교재 출력 `.`), `corpus_path`·`pdf_path`(= `corpus_path + "/pdf/easy/E01.pdf"`), `pages`·`plain_text`(905자)·`text_lines`(26줄), `mark_heading_line(line)`·`make_markdown_text(text_lines)`·`markdown_text`(911자)·`markdown_lines`, `header_rules = [("#", "heading")]`·`structure_splitter`·`structure_chunks`(3개)·`structure_texts`·`first_structure`, `make_text_list(chunk_documents)`·`make_length_list(chunk_texts)`, `make_source_record(file_path, page, parser)`·`make_source_mark(chunk)`·`make_heading_record(page_record, heading)`·`page_two_record`·`heading_documents`(3개)·`first_heading_document`, `changed_rules = [("##", "heading")]`·`changed_splitter`·`changed_chunks`(1개), `embedding_model_name = "text-embedding-3-small"`·`embedding_model`·`encoding`·`count_tokens(text)`, `whole_tokens`(869)·`buffer_times = 3`·`sent_tokens`(2607)·`embedding_rate = 0.02`·`tokens_per_million`·`call_cost`(5.21e-05), `page_two_document`·`semantic_splitter`·`semantic_chunks`(2개)·`semantic_texts`·`second_lines`, `lower_amount = 50`·`lower_splitter`·`lower_chunks`(10개)·`lower_texts`, `closure_words = ["정기 휴관일", "화요일에도 휴관"]`·`structure_found`·`semantic_found`·`lower_found`.
- **출력 라벨(전부)**: 「pypdf:」「langchain-core:」「langchain-text-splitters:」「langchain-experimental:」「langchain-openai:」「tiktoken:」「python-dotenv:」「OPENAI_API_KEY 설정 여부:」「고른 경로:」「나눌 글의 글자 수:」「나눌 글의 줄 수:」「첫 줄:」「일곱째 줄:」「표시를 붙인 뒤 글자 수:」「늘어난 글자 수:」「스물한째 줄:」「제목 표시와 칸 이름 규칙:」「구조 방식 문서 청크 수:」「문서 청크별 문자 수:」「첫 문서 청크의 메타데이터:」「문서 청크의 제목 칸:」「첫 문서 청크의 첫 줄:」「기록의 칸 수:」「첫 문서 청크의 기록:」「첫 문서 청크의 출처 표시:」「셋째 문서 청크의 제목 칸:」「바꾼 규칙:」「문서 청크 수:」「첫 문서 청크의 문자 수:」「임베딩 모델 이름:」「조각 세는 규칙 이름:」「나눌 글 전체의 조각 수:」「한 번에 보낼 조각 수 어림:」「요청 한 번의 비용 어림(달러):」「기본 끊는 기준값:」「시맨틱 방식 문서 청크 수:」「첫 문서 청크의 기록 칸 수:」「둘째 문서 청크의 첫 줄:」「바꾼 끊는 기준값:」「마지막 문서 청크:」「지킬 말 두 개:」「구조 방식에서 둘 다 든 문서 청크 번호:」「시맨틱 방식 기준값 95에서:」「시맨틱 방식 기준값 50에서:」
- **실행값(2026-09-18, 새 커널 두 번 같음)**: `pypdf: 6.18.0`·`langchain-core: 1.6.2`·`langchain-text-splitters: 1.1.2`·`langchain-experimental: 0.4.2`·`langchain-openai: 1.6.0`·`tiktoken: 0.14.0`·`python-dotenv: 1.2.3`, `고른 경로: .`, `나눌 글의 글자 수: 905`·`줄 수: 26`·`첫 줄: 1. 도서관 소개`·`일곱째 줄: 2. 이용 시간`, `표시를 붙인 뒤 글자 수: 911`·`늘어난 글자 수: 6`·`# 1. 도서관 소개`·`# 2. 이용 시간`·`# 3. 회원 가입`, `[('#', 'heading')]`·`구조 방식 문서 청크 수: 3`·`[223, 470, 182]`·`{'heading': '1. 도서관 소개'}`, `기록의 칸 수: 6`·`{'doc_id': 'E01', 'source': 'E01.pdf', 'file_type': 'pdf', 'parser': 'pypdf-plain', 'page': 2, 'heading': '1. 도서관 소개'}`·`[E01 p.2]`·`셋째 문서 청크의 제목 칸: 3. 회원 가입`, 값 바꿔 보기 `[('##', 'heading')]`·`문서 청크 수: 1`·`{}`·`911`, `임베딩 모델 이름: text-embedding-3-small`·`조각 세는 규칙 이름: cl100k_base`, `869`·`2607`·`5.21e-05`, `기본 끊는 기준값: 95`·`2`·`[233, 671]`·`기록 칸 수: 5`·`둘째 문서 청크의 첫 줄: 2. 이용 시간`, `바꾼 끊는 기준값: 50`·`10`·`[102, 53, 28, 47, 79, 106, 403, 43, 34, 1]`·`마지막 문서 청크: 2`, 지킬 말 `['정기 휴관일', '화요일에도 휴관']`·구조 `[2]`·95 `[2]`·50 `[6]`.
- **E01 2쪽 나누기 결과(07·08절이 쓸 값)**: 이 글의 제목 줄은 `1. 도서관 소개`·`2. 이용 시간`·`3. 회원 가입` 세 개이고 제목 표시는 없습니다. 표시를 붙이면 911자입니다. 구조 방식 3개(223·470·182자)이고 제목 글은 본문에서 빠집니다. 시맨틱 방식은 기준값 95에서 2개(233·671자, 끊는 자리는 둘째 제목 앞 한 곳), 50에서 10개입니다. 기준값 50의 마지막 문서 청크는 쪽 번호 줄 `2` 한 자이고 가장 긴 403자에는 표가 들어 있습니다. 탐색 실행에서만 본 값(본문에 없음): 기준값 0이면 18개 `[2, 99, 53, 28, 47, 2, 41, 34, 19, 49, 36, 31, 263, 62, 44, 43, 34, 1]`, 문장 나누기 기본 규칙으로 나눈 문장은 19개(첫 문장이 `1.` 두 자).
- **설치판 소스로 확인한 동작(langchain-experimental 0.4.2, langchain-text-splitters 1.1.2)**: `SemanticChunker`는 문장 나누기 기본 규칙이 `(?<=[.?!])\s+`이고 `buffer_size` 기본값 1이라 문장마다 앞뒤 문장을 붙여 임베딩합니다. `embed_documents()`를 **한 번** 불러 문장 목록을 함께 보냅니다(요청 한 번). 기준값 기본값은 `percentile` 95이고, 이웃한 두 벡터의 코사인 거리를 구해 기준값보다 큰 자리에서 끊습니다. `split_documents()`는 메타데이터를 문서 청크마다 깊은 사본으로 복사합니다. `MarkdownHeaderTextSplitter`는 `strip_headers` 기본값 True라 제목 줄을 본문에서 뺍니다.
- **결론 태도(01~05·Ch 9와 같음)**: 「이번 실행에서는」, 세 결과 공통 값은 한 방식의 효과로 적지 않음(06-4 맨 아래 회색 상자), 어느 방식·기준값이 검색에 더 나은지 판정하지 않음(검색을 돌리지 않았음), 실행하지 않은 동작은 「이번에 실행하지 않았습니다」.

### 제목 칸 이름과 임베딩 설정 (06이 결정했습니다 — 07·08절이 그대로 이어받을 것)

- **제목 칸 이름은 `heading`입니다.** 개선 전 06은 `section`·`topic`이었는데 04절이 HWPX 자리 칸 이름으로 `section`을 쓰고 있어 뜻이 둘이 됩니다(handoff §05 → §06 결정 항목). 같은 이름을 쓰면 04절 `make_section_mark()`가 제목 글을 자리 번호로 읽고, 실습 폴더 `_with_chunk_metadata()`도 `page`·`section`·`row`를 차례로 보므로 문서 청크 이름이 제목 글로 바뀝니다. 그래서 다른 이름을 골랐고 근거를 본문 b4·b7에 적었습니다. `##` 칸(`topic`)은 이 글의 제목 단계가 하나뿐이라 두지 않았습니다.
- 그래서 이 챕터 기록 칸은 이제 여섯 가지입니다: `doc_id`·`source`·`file_type`·`parser`(01·03)·`page`(01)·`row`(03)·`section`(04)·`heading`(06). 출처 표시 함수는 세 개 그대로입니다(`make_source_mark` `page` · `make_unit_mark` `row` · `make_section_mark` `section`). 06은 쪽이 있는 형식이라 `make_source_mark()`를 썼고 새 함수를 만들지 않았습니다.
- **임베딩 설정**: Ch 9 03절과 같은 이름(`embedding_model_name`·`embedding_model`)과 같은 모델 `text-embedding-3-small`을 쓰고 **차원 수를 주지 않습니다**(기본값). 개선 전 06의 `dimensions=256`은 뺐습니다(Ch 9 색인과 같은 설정으로 이어야 하고 `dimensions`는 Ch 9 요약 §6 「아직 안 가르친 것」).
- **요청 수 세는 법**: 시맨틱 방식은 나눌 때마다 `embed_documents()` 한 번입니다(문장 수만큼 나뉘지 않습니다). 보내는 조각 수는 앞뒤 문장을 붙이므로 글 전체의 세 배쯤으로 어림했습니다(`buffer_times = 3`). 비용 어림은 Ch 9 03절과 같은 방식(100만 토큰당 0.02달러, `round(raw_cost, 7)`)입니다.

### 07절이 이어받을 연결과 확인할 것

- 06 b8·노트북 정리 끝: 「07절에서는 문서 청크를 벡터로 바꾸는 단계를 따로 봅니다. 문장 하나와 문장 목록을 임베딩해 벡터의 숫자 개수를 보고, 같은 글을 두 번 보낼 때 값을 저장해 두는 방법을 봅니다.」
- **개선 전 07 노트북**을 먼저 읽으세요. `python-dotenv==1.2.3`·`langchain-openai==1.6.0`·`langchain-classic==1.0.8`을 설치하고, `OpenAIEmbeddings(model="text-embedding-3-small", dimensions=256)`·`embed_documents([글])`·`dimensions=128`과 `CacheBackedEmbeddings.from_bytes_store(embeddings, byte_store, namespace=, key_encoder="sha256")`·`LocalFileStore(폴더)`·`TemporaryDirectory`·`Path.rglob("*")`를 씁니다. 원문은 노트북 안에 적은 배송·환불 세 문장이고, Before/After는 「256차원 캐시 이름을 128차원 모델에 재사용 → 이름에 차원을 넣어 가름」입니다. 형식은 `lesson_format`이 없어 그 절 작업자가 정해야 합니다(개선 전 `_src`는 `{{notebook:07-…}}` 한 개와 b6 「실험 결과 해석」이라 experiment 모양입니다).
- **`dimensions` 결정이 하나 필요합니다.** 06은 Ch 9와 같이 차원 수를 주지 않았습니다(기본 1536). 개선 전 07은 256과 128을 쓰며 그 차이가 학습 목표(같은 설정의 벡터만 섞을 수 있다)입니다. 07이 `dimensions`를 처음 가르치는 자리가 되므로, 규격 §4 세 문장으로 풀고 **Ch 9·06절 색인은 기본값이라는 사실을 한 문장 적으세요**. 07에서 만든 256차원 벡터를 08절 색인에 이어 쓸지도 함께 정해야 합니다(08은 색인 여러 벌을 만듭니다).
- **06과 겹치지 않게**: 06은 「나누는 자리」와 「나눌 때 생기는 임베딩 요청」을 다뤘습니다. 07은 **벡터 자체**(숫자 개수, 같은 글을 두 번 보낼 때 값을 저장해 두기)에 무게를 두세요. 「임베딩 요청 수·비용 어림」은 Ch 9 03절과 06절에서 이미 보였으니 되풀이하지 말고 캐시로 요청이 줄어드는 것을 재는 데 쓰면 됩니다.
- 개선 전 07이 쓰는 것 가운데 **01~06절·Part 1·2에서 안 가르친 것**: `TemporaryDirectory(prefix=)`, `Path.rglob("*")`·`path.is_file()`, 내포식(`[len(vector) for vector in vectors]`), `try/except AssertionError`, `list()`, `CacheBackedEmbeddings`·`LocalFileStore`·`namespace`·`key_encoder="sha256"`, `dimensions=`, 벡터 값 슬라이싱 출력(`single_vector[:5]` — 소수 값은 실행마다 달라질 수 있어 결과 읽기 첫 단락에 넣지 마세요, Ch 9 §1 태도).
- **아직 안 가르친 것(07이 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 전체 + 01~06에서도 안 한 것 — 기준값을 0까지 낮춘 시맨틱 나누기, 다른 임베딩 모델·다른 차원, 02절 표 읽기 결과를 문서 청크로 쓰기, 여러 쪽·여러 문서를 한 번에 나누기, 문서 청크 이름(`chunk_id`), 검색·점수 재기(08), 색인 여러 벌 견주기(08), 실습 폴더 모듈 `import`, 글자 인식(OCR) 실행, 두 단 레이아웃, 본문 XML이 여러 개인 HWPX, 암호가 걸린 문서.

### 산출 파일·실습 폴더·묶음

- 06도 `runs/`를 읽지도 쓰지도 않습니다(40개 파일 해시 전후 같음, `1cc170e8…`). 이 챕터 `runs/`를 쓰는 곳은 개선 전 **08절**입니다(§01 → §02의 08절 계약 목록을 그대로 보세요).
- 실습 폴더 테스트 `38 passed`(전후 같음). `document_processing.py`·`experiment.py`·`tests/`·`fixtures/`는 고치지 않았습니다(모듈 두 개 해시 `95b63e9c…`, `fixtures/` 해시 `aebfec32…`).
- **실습 폴더 함수와 다른 점**: `split_structural()`은 제목 표시와 빈 줄을 경계로 삼은 뒤 긴 덩이만 재귀 방식으로 다시 나누고, `split_semantic()`은 문장 임베딩의 코사인 유사도가 기준(기본 0.55)보다 낮은 자리에서 끊습니다. 노트북이 쓴 두 도구와 이름만 비슷합니다. 본문 b7에 한 항목으로 적었습니다.
- **학생 묶음**: 06이 읽는 입력은 `labs/data/rag-corpus/pdf/easy/E01.pdf` 하나로 01·02·05절과 같습니다. 허용 목록을 고치지 않았고, 묶음을 `/tmp/ch10-06/bundle`에 풀어 **묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리**에서 경로 셀을 돌려 모두 찾았습니다(`.`·`../../..`·`../../../..`, 묶음 사본과 원본 해시 `cd0ff7d7…` 같음). 07절이 새 입력을 읽게 되면 같은 방법으로 확인하세요.
- 절 수는 8개 그대로라 `textbook/part3/_build_index.py`(ch10 칸 8)와 `qa/visual-results.json` 행 수는 고치지 않았습니다.
- 루트 `textbook/qa/upgrade-progress.md`의 Ch 10 행은 아직 「절 개선 중(01 완료)」입니다. 챕터 밖 파일이라 절 작업자가 고치지 않았습니다(02·03·04·05·06 모두 같음). 오케스트레이터 몫입니다.
## §07 → §08

(07절 품질 개선 2026-09-18. 결과는 `07-diagnosis.md`, 게이트 G1~G7 0(수정 전 G1 3·G3 4·G5 12·G6 29·G7 3 = 51), 코드 셀 23(준비 3), 검사 문장 426, **임베딩 요청 6번**(`text-embedding-3-small`, 비용 어림 `5e-05`달러), 새 커널로 세 번 이어 실행해 출력 값이 모두 같음(교재 출력은 마지막 실행 2026-09-18T05:27:07Z). 삽화 07-5 1차 채택(job `a401f432-…`, 2크레딧, 잔액 2794), Mermaid 4장. **빌드 도구·챕터 밖 파일 변경 0건**)

### 형식 판정 — handoff §06 → §07 기록과 어긋난 점

- §06 → §07은 「07은 `lesson_format`이 없어 형식을 정해야 하고 개선 전 `_src`가 experiment 모양」이라고 적었습니다. **실제로는 paired였습니다.** 개선 전 `_src` b5에 `{{notebook:07-…|example}}`, b6 「일부러 실패해 보기」에 `{{notebook:07-…|failure}}`가 있고, 개선 전 노트북에도 `lesson_part` `before`·`after` 셀 네 개가 있었습니다.
- 그래서 **paired를 유지**했습니다. 08절도 개선 전 `_src`의 `{{notebook:}}` 토큰 수와 b6 제목, 노트북의 `lesson_part`를 직접 열어 확인하세요(개선 전 08 노트북 메타데이터는 `lesson_format: experiment`이고 `_src` b6은 「실험 결과 해석」입니다).

### 07이 확인한 실행 환경 (§01 → §02 ~ §06 → §07 그대로 쓸 수 있음)

- `run_section.sh textbook/part3/ch10-document-processing 08`로 생성기 → 새 커널 → 렌더 → 첨부 → 빌드 → 게이트가 한 번에 돌아갑니다. `chapter.json`이 없어 verify는 따로:
  `UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch10-document-processing uv run --project labs/part3/ch10-document-processing python textbook/_notebook/verify.py --chapter textbook/part3/ch10-document-processing`
  → 07 뒤 `PASS 8 sections / 166 code cells (max 24 lines)`(06 뒤 152).
- 07 뒤 디스크 HTML 기준: `/tmp/ch10-07/hash/final.txt`. 작업 전후 `sha256sum *.html`로 다른 절이 바뀌지 않았는지 보세요(07에서는 07 HTML만 `d954618139…` → `f6d93f2601…`).
- `visual.cjs`·묶음 풀기·삽화 저장 방법은 §01 → §02와 같습니다. `.cache/vm/shot/`에 검수용 캡처를 두었습니다(`ch10-07-cand1.png`·`ch10-07-page-illu.png`·`ch10-07-page-mmd3.png`).
- 기기 루트 여유 약 458MB. 작업 폴더 `/tmp/ch10-07`(해시·탐색 실행·삽화 원본·visual 사본). `part3-practice.zip`을 푼 폴더는 11MB라 확인 뒤 지웠습니다.
- **게이트 라벨**: 07도 `--label wip --section 07`만 돌렸습니다(`gates-wip-07.json`).
- **세 번 실행 결과**: 값은 모두 같았고 `outputs_sha256`은 `ce6ec276…` → `118b6980…` → `ce6ec276…`로 갈렸습니다. 전체 출력 JSON을 셀 단위로 대조해 차이가 `%pip` 셀 출력 덩이 수(1개 또는 2개)뿐임을 확인했습니다(02~04절과 같은 현상). 해시만 보지 말고 셀 단위로 값을 대조하세요.
- **Mermaid 폭**: 한 줄기 흐름도는 폭이 좁게 나옵니다. 07-1 첫 판이 265.1×705.8이어서 두 설정을 왼쪽·오른쪽 갈래로 나눠 534.1×606.8로 고쳤습니다(§04 → §05 메모와 같은 문제). 07-4는 815.1에서 라벨을 줄여 781.2로 낮췄습니다.

### 용어 (07에서 정한 것, 08도 같게)

- **01절 네 말**(파서·파일 형식·출처 기록·출처 계보), **02절 네 말**(글자 층·표 읽기·글자 인식·OCR 후보 쪽), **03절 네 말**(문단·꾸밈 이름·태그·자리 칸), **04절 네 말**(형식 표시·이진 파일·압축 묶음·이름 공간), **05절 네 말**(문자 방식·재귀 방식·토큰 방식·조각 수 한도), **06절 네 말**(구조 방식·시맨틱 방식·제목 표시·끊는 기준값), Ch 9 용어를 그대로 씁니다. 07이 새로 정한 말은 네 개입니다: **차원 수(dimensions)**, **벡터 캐시(vector cache)**, **가르는 이름(namespace)**, **저장 이름표(cache key)**.
- **「벡터 캐시」와 Ch 9 「벡터스토어」는 다른 것입니다.** 07 b4에 표로 갈라 두었습니다(담는 까닭·찾는 방법·본문 보관 여부·쓰는 이름). 08절이 색인을 만들 때 「벡터스토어」는 Ch 9 뜻(검색을 위해 벡터를 담는 곳)으로만 쓰세요.
- **「가르는 이름」은 사람이 적는 글입니다.** 「네임스페이스」·「캐시 키」는 쓰지 않았습니다(차례로 → 가르는 이름, 저장 이름표).
- Ch 9 06절 **「색인 이름표」**(index key, 설정으로 만든 이름)와 07절 **「저장 이름표」**(cache key, 글로 만든 파일 이름)는 다른 것입니다. 08절이 실험 설정마다 이름을 만들면 Ch 9 말인 「색인 이름표」를 쓰세요.
- 쓰지 않은 말: 「인덱스 구성 기록표」, 「다국어 임베딩」, 「모델 버전」, 「입력 접두사」(→ 앞머리 글), 「좌표계」·「주소 체계」, 한정어 없는 「청크」, 「청킹」·「오버랩」·「정규화」·「문맥」.

### 07에서 새로 가르친 것

- **API·동작(노트북에서 실행한 것만)**: `embed_documents([글])`·`embed_documents(글 목록)`(Ch 9 01·03절은 `embed_query()`만 가르침 — 노트북 4절 설명 셀에 뜻), **`OpenAIEmbeddings(model=, dimensions=256)`**(규격 §4 세 문장으로 6절에 풂), `import tempfile`·`tempfile.mkdtemp(prefix=)`(Ch 1·2 준비 셀과 같은 함수 — 처음 쓰는 자리에 한 문장), `os.listdir(경로)`로 파일 수 세기(01절과 같은 함수), `LocalFileStore(폴더)`, `CacheBackedEmbeddings.from_bytes_store(모델, 저장소, namespace=, key_encoder="sha256")`, 속성 `embedding_model.model`·`embedding_model.dimensions`.
- **Python 모양**: 글 `+ " "`로 한 글자 더하기, `startswith()`로 이름 앞머리 확인(04절 모양), `type(객체).__name__`(04절 모양), `목록[0]`으로 첫 벡터 고르기, 목록끼리 견주기(`first_vectors == second_vectors`), `is not None`으로 인자를 주었는지 보기. 01~06절과 같은 후보 경로 `for`+`break`.
- **01~06절이 안 쓴 것 가운데 07도 안 쓴 것**: `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·try·`raise`·`with`·`+=`·`enumerate`·`zip`·`sum`·`max`·`any`·`all`·`isinstance`·`join`·f-string 안 계산·타입힌트·`@`·`BaseModel`·모델 문장 `assert`·`Path`·`Path.cwd()`·`parents`.
- **함수 본문 10줄(규격 §2-2 L2, 직접 셈)**: `load_pdf_pages` 9줄(01절과 같은 코드) · `make_length_list` 4줄(05절) · `count_tokens` 1줄(05·06절) · `make_size_list` 4줄(새로). 셀 최대 12줄(After 셀 11줄).
- **이어 쓸 이름과 값**: `candidates`·`root_path`(교재 출력 `.`), `corpus_path`·`pdf_path`(= `corpus_path + "/pdf/easy/E01.pdf"`), `pages`·`plain_text`(905자), `make_length_list(chunk_texts)`(05절), **`separator_order = ["\n\n", ". ", "\n", " ", ""]`·`recursive_splitter`**(05절 4절과 같은 설정: `chunk_size=200`·`chunk_overlap=0`·`keep_separator="end"`)·`chunk_texts`(6개), `encoding`·`count_tokens(text)`, `one_text`(= `chunk_texts[0]`, 185자)·`whole_tokens`(869)·`one_tokens`(190)·`list_requests = 2`·`one_requests = 4`·`sent_tokens`(2498), `embedding_rate = 0.02`·`tokens_per_million`·`raw_cost`·`total_cost`(5e-05), **`embedding_model_name = "text-embedding-3-small"`·`embedding_model`**(Ch 9 03절·06절과 같은 이름, 차원 수 안 줌), `one_vectors`·`single_vector`, `make_size_list(vectors)`·`all_vectors`, **`short_dimensions = 256`·`short_model`**, `short_vectors`, `cache_folder`·`folder_names`, **`cache_name = "text-embedding-3-small-1536-"`**·`byte_store`·`cached_embeddings`, `first_vectors`·`first_names`·`second_vectors`·`second_names`·`first_name`·`starts_with_cache_name`, `changed_text`·`changed_vectors`·`changed_names`, Before `wrong_cache`·`wrong_vectors`·`wrong_size`·`wrong_names`, After **`short_cache_name = "text-embedding-3-small-256-"`**·`short_cache`·`right_vectors`·`right_size`·`right_names`.
- **출력 라벨(전부)**: 「pypdf:」「langchain-core:」「langchain-text-splitters:」「langchain-openai:」「langchain-classic:」「tiktoken:」「python-dotenv:」「OPENAI_API_KEY 설정 여부:」「고른 경로:」「Document 수:」「나눌 글의 글자 수:」「문서 청크 수:」「문서 청크별 문자 수:」「조각 세는 규칙 이름:」「글 전체의 조각 수:」「첫 문서 청크의 조각 수:」「이 절이 보낼 조각 수 어림:」「100만 조각당 요금(달러):」「이 절 전체의 비용 어림(달러):」「임베딩 모델 이름:」「차원 수를 주었는가:」「보낸 글의 글자 수:」「받은 벡터 수:」「벡터의 숫자 개수:」「첫 숫자의 자료형:」「보낸 글 수:」「벡터마다 숫자 개수:」「첫 벡터가 앞의 결과와 같은 개수인가:」「준 차원 수:」「기본 설정 벡터의 숫자 개수:」「차원 수를 준 벡터의 숫자 개수:」「폴더 안의 파일 수:」「빈 폴더인가:」「가르는 이름:」「벡터 캐시의 자료형:」「첫 요청 뒤 저장 파일 수:」「두 번째 요청 뒤 저장 파일 수:」「두 벡터 목록이 같은가:」「첫 파일 이름이 가르는 이름으로 시작하는가:」「첫 파일 이름의 글자 수:」「가르는 이름의 글자 수:」「바꾼 글의 글자 수:」「앞의 글과 글자까지 같은가:」「저장 파일 수:」「받은 벡터의 숫자 개수:」「기대한 숫자 개수:」「돌아온 벡터의 숫자 개수:」「두 값이 같은가:」
- **실행값(2026-09-18, 새 커널 세 번 같음)**: `pypdf: 6.18.0`·`langchain-core: 1.6.2`·`langchain-text-splitters: 1.1.2`·`langchain-openai: 1.6.0`·`langchain-classic: 1.0.8`·`tiktoken: 0.14.0`·`python-dotenv: 1.2.3`, `OPENAI_API_KEY 설정 여부: True`·`고른 경로: .`, `Document 수: 5`·`나눌 글의 글자 수: 905`, `문서 청크 수: 6`·`문서 청크별 문자 수: [185, 147, 86, 164, 130, 188]`, `조각 세는 규칙 이름: cl100k_base`·`글 전체의 조각 수: 869`·`첫 문서 청크의 조각 수: 190`·`이 절이 보낼 조각 수 어림: 2498`·`100만 조각당 요금(달러): 0.02`·`이 절 전체의 비용 어림(달러): 5e-05`, `임베딩 모델 이름: text-embedding-3-small`·`차원 수를 주었는가: False`, `보낸 글의 글자 수: 185`·`받은 벡터 수: 1`·`벡터의 숫자 개수: 1536`·`첫 숫자의 자료형: float`, `보낸 글 수: 6`·`받은 벡터 수: 6`·`벡터마다 숫자 개수: [1536, 1536, 1536, 1536, 1536, 1536]`·`첫 벡터가 앞의 결과와 같은 개수인가: True`, `준 차원 수: 256`·`기본 설정 벡터의 숫자 개수: 1536`·`차원 수를 준 벡터의 숫자 개수: 256`, `폴더 안의 파일 수: 0`·`빈 폴더인가: True`, `가르는 이름: text-embedding-3-small-1536-`·`벡터 캐시의 자료형: CacheBackedEmbeddings`, `첫 요청 뒤 저장 파일 수: 6`·`두 번째 요청 뒤 저장 파일 수: 6`·`두 벡터 목록이 같은가: True`, `첫 파일 이름이 가르는 이름으로 시작하는가: True`·`첫 파일 이름의 글자 수: 92`·`가르는 이름의 글자 수: 28`, 값 바꿔 보기 `바꾼 글의 글자 수: 186`·`앞의 글과 글자까지 같은가: False`·`저장 파일 수: 7`·`받은 벡터의 숫자 개수: 1536`, Before `기대한 숫자 개수: 256`·`돌아온 벡터의 숫자 개수: 1536`·`두 값이 같은가: False`·`저장 파일 수: 7`, After `가르는 이름: text-embedding-3-small-256-`·`돌아온 벡터의 숫자 개수: 256`·`두 값이 같은가: True`·`저장 파일 수: 8`.
- **E01 2쪽 임베딩 결과(08절이 쓸 값)**: 05절 4절과 같은 설정으로 나눈 문서 청크 여섯 개를 `text-embedding-3-small` 기본 설정으로 임베딩하면 벡터마다 숫자 1536개입니다. 차원 수 256을 주면 256개입니다. 보낸 글 수와 받은 벡터 수가 같고 순서도 같습니다. 저장 이름표는 「가르는 이름 28자 + 지문 64자 = 92자」입니다. 임베딩 값(소수)은 실행마다 조금 달라질 수 있어 **출력하지 않았습니다**.
- **설치판 소스로 확인한 동작(langchain-classic 1.0.8, langchain-openai 1.6.0)**: `_make_default_key_encoder()`가 저장 이름표를 「가르는 이름 + sha256 16진수 64자」로 만들고 `LocalFileStore._get_full_path()`가 그 이름을 그대로 파일 이름으로 씁니다(폴더가 한 겹이라 `os.listdir()`로 셀 수 있음). `CacheBackedEmbeddings.embed_documents()`는 저장값이 없는 글만 모아 한 번 임베딩하고 모두 있으면 요청을 보내지 않습니다. 값은 `json.dumps()`로 저장하고 `json.loads()`로 되살립니다. `OpenAIEmbeddings`의 `dimensions` 기본값은 `None`, `chunk_size` 기본값은 1000이라 글 여섯 개는 요청 한 번입니다. 질문 쪽 캐시는 기본으로 끕니다(`query_embedding_cache=False`, 07에서 실행하지 않음).
- **결론 태도(01~06·Ch 9와 같음)**: 「이번 실행에서는」, 두 칸 공통 값은 한 조건 효과로 적지 않음(07-4 맨 아래 회색 상자), 어느 차원 수가 검색에 더 나은지 판정하지 않음(검색을 돌리지 않았음), **파일 수로 요청 수를 말하지 않음**(그 셀에서 세지 않았고, 소스에서 얻은 근거와 구분해 적었음), 실행하지 않은 동작은 「이번에 실행하지 않았습니다」.

### `dimensions`와 색인 설정 (07이 결정했습니다 — 08절이 그대로 이어받을 것)

- **07이 `dimensions`를 처음 가르쳤습니다.** 규격 §4 세 문장(뜻 → 일상 예 → 코드)으로 b4 용어 표와 노트북 6절에 풀었고, **Ch 9 03절과 06절 색인은 이 인자를 주지 않은 기본값 1536개**라는 사실을 본문 b4·b7과 노트북 4절 결과 읽기에 적었습니다.
- **색인에 넣을 벡터는 기본 설정으로 만듭니다.** 07의 256차원 벡터는 개수를 견주려고 만든 것이고 **08절 색인에 이어 쓰지 않습니다**. 개수가 다른 벡터를 한 색인에 섞으면 검색 점수를 계산할 수 없기 때문입니다. 근거는 본문 b7 두 번째 항목에 적었습니다.
- **그런데 개선 전 08절 기록의 `config`에는 `dimensions: 256`이 들어 있습니다**(아래 계약 표). 08절이 색인을 기본 설정으로 다시 만들면 그 칸 값이 바뀝니다. 읽는 쪽을 확인한 결과 **그 칸을 검사하는 곳은 없었습니다**(`check_course_continuity.py` 219행의 `settings['dimensions'] == 256`은 **Ch 12** `advanced-continuity-integrated-result.json`을 봅니다). 그래도 값을 바꾸면 본문·기록·챕터 요약에 까닭을 적으세요.
- 개선 전 08은 임베딩 모델을 **두 개**(`text-embedding-3-small`·`text-embedding-3-large`) 씁니다. 「다른 임베딩 모델」은 Ch 9 요약 §6과 07절에서 아직 안 가르친 것입니다. 08이 두 모델을 견주려면 규격 §4 세 문장으로 풀고 요청 수·비용을 다시 어림하세요. 한 모델만 쓰기로 하면 기록 줄 수가 줄어드니 **아래 「기록 줄 수 7」 제약**을 먼저 보세요.
- 벡터 캐시(`CacheBackedEmbeddings`)를 08절 색인에 쓸지는 정하지 않았습니다. 07은 임시 폴더에만 저장했고 색인에는 넣지 않았습니다.

### 08절이 이어받을 연결과 확인할 것

- 07 b8·노트북 정리 끝: 「08절에서는 나누기와 임베딩 설정을 하나씩 바꿔 색인을 여러 벌 만듭니다. 설정마다 검색 결과가 어떻게 달라지는지 기록으로 남겨 견줍니다. 그때 이 절의 모델 이름과 차원 수가 실험 설정의 한 칸으로 다시 나옵니다.」 07 b8 둘째 단락은 Ch 11이 그 기록에 정답 문서를 붙여 지표를 계산한다고 적었습니다.
- **개선 전 08 노트북**을 먼저 읽으세요. `python-dotenv==1.2.3`·`langchain-core==1.6.2`·`langchain-openai==1.6.0`·`langchain-text-splitters==1.1.2`·`tiktoken==0.14.0`·`pypdf==6.18.0`을 설치하고, 앞부분은 노트북 안에 적은 쇼핑몰 규정 글로 세 나누기 방식 × 두 임베딩 모델 여섯 조합을 `InMemoryVectorStore.from_documents()`·`similarity_search_with_score(k=2)`로 견줍니다. 뒷부분(8·9절)은 **실제 `rag-corpus` 디지털 PDF 18건**과 Ch 11 평가셋 Q001로 여섯 실행을 만들어 `runs/`에 기록합니다.
- 개선 전 08이 쓰는 것 가운데 **01~07절·Part 1·2에서 안 가르친 것**: 내포식 여러 곳, 제너레이터 식 + `next(...)`, `Path.cwd()`·`parents`·`glob`, `enumerate(..., start=1)`, f-string 안 계산과 `{index:02d}`·`{i:04d}` 형식 지정, 딕셔너리를 만들어 `items()`로 도는 비교 셀, `datetime.now(UTC).strftime()`, `mkdir(parents=True, exist_ok=True)`, `write_text()`, `dict.fromkeys`, `text-embedding-3-large`, `strip_headers=False`, `InMemoryVectorStore.from_documents()`(Ch 9 03절은 `InMemoryVectorStore(embedding=)` + `add_documents()`), 영어 출력 라벨.
- **07과 겹치지 않게**: 07은 「벡터의 숫자 개수」와 「같은 글을 두 번 보낼 때 저장해 두기」를 다뤘습니다. 08은 **설정을 하나씩 바꿔 색인을 여러 벌 만들고 검색 결과를 기록으로 견주는 일**에 무게를 두세요. 「임베딩 요청 수·비용 어림」은 Ch 9 03절과 06·07절에서 이미 보였으니 준비물에 수만 적고 되풀이하지 마세요.
- **Ch 9 「점수 = 코사인 유사도」는 `InMemoryVectorStore` 한정입니다**(Ch 9 요약 §5). 08이 다른 벡터스토어를 쓰면 「점수가 크면 가깝다」를 그대로 이어 쓰지 마세요.
- **아직 안 가르친 것(08이 설명 없이 전제하면 안 됨)**: Ch 9 요약 §6 전체 + 01~07에서도 안 한 것 — 다른 임베딩 모델, 차원 수 128, 질문 쪽 벡터 저장, 문서·질문 앞머리 글, 벡터로 검색해 점수 재기, 문서 사이 순위 비교, 색인 파일 저장과 다시 불러오기, `as_retriever()`, 점수 기준값·거르기·MMR, 여러 질문을 한 번에 돌려 평균 내기, 검색 지표(Ch 11), 글자 인식(OCR) 실행, 두 단 레이아웃, 본문 XML이 여러 개인 HWPX, 암호가 걸린 문서, 실습 폴더 모듈 `import`.

### 산출 파일 계약 — 08절이 유일하게 `runs/`를 씁니다 (먼저 읽을 것)

- 07도 `runs/`를 읽지도 쓰지도 않습니다(40개 파일 해시 전후 같음, `455ab5b1…`). 01~07절 모두 그렇습니다.
- **현재 기록**: `labs/part3/ch10-document-processing/runs/continuity-ch10-indexing.jsonl`(정본, **6줄**, SHA-256 `9e59586aae770b71a84fdc0d0db02bf7de386c8744ab83110a722d67690732b3`)과 사본 폴더 `runs/continuity/`(24개). **앞 사본은 지우지 마세요**(과정 단계 검사가 옛 바이트를 그 이름으로 찾습니다).

| 항목 | 값 |
|---|---|
| 최상위 키 7개 | `qid`·`question`·`gold_doc_ids`·`source_chapter`(`ch10`)·`source_run_id`·`config`·`retrieved`. Ch 9와 달리 **`answer` 칸이 없습니다** |
| `config` 키 6개 | `chunk_method`·`split_config`·`embedding`·`dimensions`(현재 256)·`k`(현재 5)·`inputs`. `inputs`는 `corpus_scope`·`corpus_manifest_sha256`·`evaluation_dataset_sha256` |
| `retrieved` 항목 키 5개 | `doc_id`·`chunk_id`·`page`·`rank`·`score`. `rank`는 1부터 빈틈없이, `page` 1 이상, `chunk_id`는 빈 값이 아니어야 합니다 |
| `chunk_id` 모양 | `ch10:recursive:0000`(네 자리 채움). Ch 9는 `ch09:6f9f83db90:0`입니다 — **모양 차이를 08절 본문·챕터 요약에 적으세요**(Ch 9 검토 B R-3) |
| 라벨 | `question`·`gold_doc_ids`는 `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl` Q001과 글자까지 같아야 하고, `config` 안에 라벨 키를 넣으면 검사가 멈춥니다 |
| **줄 수 7 제약** | `textbook/part3/qa/finalize_continuity_evidence.py` 51행이 `assert len(source_ids) == 7`입니다(ch09 1줄 + **ch10 6줄**). 실행 수를 바꾸면 이 줄을 함께 고쳐야 합니다 |
| **k=5와 지표 제약** | 같은 파일 54~58행이 ch10 실행마다 `recall_at_5 == 1`·`precision_at_5 == .2`·`ndcg_at_5 == 1`·`recall_at_logged_candidates == 1`을 확인합니다. 곧 **검색 개수 5에 정답 문서가 정확히 하나** 들어야 합니다. `evaluate.py` 232~236행이 `logged_k >= 5`에서만 @5를 계산하므로 k를 5보다 작게 두면 `None`이 되어 이 검사가 걸립니다 |
| `dimensions` 칸 | 읽는 쪽이 없습니다. `check_course_continuity.py` 219행의 `settings['dimensions'] == 256`은 **Ch 12** 기록을 봅니다 |

- **읽는 쪽 목록**: `labs/part3/ch11-evaluation/evaluate.py` 176~250행 · `textbook/part3/qa/check_continuity.py` 58~78·140~155행 · `textbook/qa/check_course_continuity.py` 94~112·172~198행 · `textbook/part3/qa/run_continuity_bundle.py` 45~54행(묶음 연기 실행이 **08절 노트북만** 씀) · `textbook/part3/qa/finalize_continuity_evidence.py` 15·37·44~58행.
- **이 파일을 다시 쓸 때**: (a) 위 읽는 쪽을 먼저 확인하고, (b) 08 본문·그림의 인용 값을 새 출력으로 모두 맞추고, (c) 앞 사본은 그대로 두고, (d) 계약 표와 챕터 요약·진행표를 새로 적습니다. `finalize_continuity_evidence.py` 15행 `assert len(visual) == 88`도 절 수가 늘면 함께 봅니다(Ch 9 마감 때 90으로 고칠 예정).

### 실습 폴더·묶음·절 수

- 실습 폴더 테스트 `38 passed`(전후 같음). `document_processing.py`(`37ca2cc9…`)·`experiment.py`(`342e85b0…`)·`tests/`·`fixtures/`(`2681052c…`)는 고치지 않았습니다(수정 시각 2026-09-08 그대로).
- **학생 묶음**: 07이 읽는 입력은 `labs/data/rag-corpus/pdf/easy/E01.pdf` 하나로 01·02·05·06절과 같습니다. 벡터를 저장하는 폴더는 `tempfile.mkdtemp()`로 만드는 시스템 임시 폴더라 묶음 대상이 아닙니다. 허용 목록을 고치지 않았고, 묶음을 `/tmp/ch10-07/bundle`에 풀어 **묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리**에서 경로 셀을 돌려 모두 찾았습니다(`.`·`../../..`·`../../../..`, 묶음 사본과 원본 해시 `cd0ff7d7…` 같음). 08절이 평가셋·말뭉치 manifest를 읽게 되면 `textbook/part3/public-files.json`(`labs/part3/` 접두만)과 `textbook/_notebook/build_bundle.py`의 `data`·`FIXTURES` 목록을 함께 보고 같은 방법으로 확인하세요. Ch 9 요약 §7에 따라 `labs/data/rag-corpus/queries.jsonl`은 이미 묶음에 들어갑니다.
- 절 수는 8개 그대로라 `textbook/part3/_build_index.py`(ch10 칸 8)와 `qa/visual-results.json` 행 수는 고치지 않았습니다. **실습 절 09를 붙일 때** `_build.py` `SECTIONS`에 주제까지 넣은 제목 한 줄, `render_index()`의 「개념 8절」, `_src/index.html` 절 표, `_build_index.py` ch10 절 수 칸(8 → 9, 강의 시수 8은 그대로)을 함께 고칩니다(§01 → §02).
- meta 시수: 01~08 모두 「강의 1h | 실습 2h」이고 합이 강의 8h·실습 16h로 `_build.py` `render_index()`의 「24h · 강의 8h · 실습 16h」와 같습니다(규격 §7-2). 07은 그대로 두었습니다.
- 챕터 안 기록: `qa/verification.md` 표에 **06절 행이 빠져 있어 06·07 두 행을 함께 채웠습니다**(06절 작업에서는 메모만 더했습니다). 08절 작업 때 표에 행을 하나 더하세요.
- 루트 `textbook/qa/upgrade-progress.md`의 Ch 10 행은 아직 「절 개선 중(01 완료)」입니다. 챕터 밖 파일이라 절 작업자가 고치지 않았습니다(02·03·04·05·06·07 모두 같음). 오케스트레이터 몫입니다.

## §08 → 실습

(08절 품질 개선 2026-09-18. 결과는 `08-diagnosis.md`, 게이트 G1~G7 0(수정 전 G1 15·G2 5·G3 9·G5 13·G6 17·G7 3 = 62), 코드 셀 29(준비 3), 검사 문장 480, **임베딩 요청 13번**(`text-embedding-3-small` 기본 설정, 비용 어림 `0.0078194`달러), 새 커널로 네 번 실행(교재 출력은 마지막 실행 2026-09-18T06:19:03Z). 삽화 08-5 1차 채택(job `590109ab-…`, 2크레딧, 잔액 2792), Mermaid 4장. **빌드 도구·챕터 밖 파일 변경 0건**. 이 챕터 개념 8절이 모두 끝났습니다)

### 08이 확인한 실행 환경 (§01 → §02 ~ §07 → §08 그대로 쓸 수 있음)

- `run_section.sh textbook/part3/ch10-document-processing 09`로 생성기 → 새 커널 → 렌더 → 첨부 → 빌드 → 게이트가 한 번에 돌아갑니다. `chapter.json`이 없어 verify는 따로:
  `UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch10-document-processing uv run --project labs/part3/ch10-document-processing python textbook/_notebook/verify.py --chapter textbook/part3/ch10-document-processing`
  → 08 뒤 `PASS 8 sections / 185 code cells (max 14 lines)`(07 뒤 166).
- **한 호출에 다 넣지 마세요.** 08 노트북은 새 커널 실행이 10초 안팎이지만, 기기 셸은 호출당 180초라 `run_section.sh`를 통째로 돌리면 설치·실행·렌더·빌드가 겹쳐 아슬아슬합니다. 08에서는 생성기 + `execute.py`를 따로 돌리고(`timeout 175`), 그다음 `run_section.sh … --no-exec`로 렌더·첨부·빌드·게이트를 돌렸습니다.
- 08 뒤 디스크 HTML 기준: `/tmp/ch10-08/hash/final.txt`. 작업 전후 `sha256sum *.html`로 다른 절이 바뀌지 않았는지 보세요(08에서는 08 HTML만 `ba441182…` → `0273e394…`).
- `visual.cjs`·묶음 풀기·삽화 저장 방법은 §01 → §02와 같습니다. `.cache/vm/shot/`에 검수용 캡처를 두었습니다(`ch10-08-page-illu.png`·`ch10-08-page-mmd2.png`·`ch10-08-page-mmd3.png`).
- 기기 루트 여유 약 566MB. 작업 폴더 `/tmp/ch10-08`(해시·탐색 실행·삽화 원본·visual 사본). `part3-practice.zip`을 푼 폴더는 11MB라 확인 뒤 지웠습니다.
- **게이트 라벨**: 08도 `--label wip --section 08`만 돌렸습니다(`gates-wip-08.json`).
- **네 번 실행 결과**: 문서 청크 수 여섯 개와 1위·2위 결과는 네 번 모두 같았습니다. `outputs_sha256`은 실행마다 달랐고 차이는 두 가지입니다 — 실행 이름(날짜·시각)과 **상위 세 번째부터 다섯 번째 문서의 순서**(`recursive | 100` 줄에서 `M04`와 `H03`이 바뀜). 점수 차가 소수 셋째 자리 수준이라 생기는 차이라 **1위와 2위까지만 결론에 썼습니다**.
- **Mermaid 폭**: 칸(`subgraph`) 테두리가 노드 합보다 넓게 잡혀 두 칸을 나란히 두면 888이 나왔습니다(08-4 첫 판). 칸을 없애고 상자를 두 갈래로 두어 536으로 낮췄습니다. 또 **칸을 넘어가는 화살표가 있으면 칸 안 `direction` 설정이 무시됩니다**(08-2 첫 판 1492.9) → 화살표를 칸끼리(`MAKE --> FIND`) 이으세요.
- **`xychart-beta` 주의**: 마지막 가로축 라벨이 SVG 테두리를 1.5px 넘어 `visual.cjs` `svgBounds`에 걸렸습니다. 라벨을 짧게 줄이고 단위를 캡션으로 옮겨 통과했습니다.

### 이 챕터가 가르친 것 (실습 절이 쓸 수 있는 전부)

- **01절**: `os.listdir()`·`sorted()`·`Path(경로).name`·`stem`·`suffix`·`type(객체).__name__`, `PdfReader`·`reader.pages`·`page.extract_text()`·`extract_text(extraction_mode="layout")`, `Document(page_content=, metadata=)`, `딕셔너리.keys()`. 함수 `load_pdf_pages(pdf_path, doc_id)`·`make_source_record(file_path, page, parser)`·`make_source_mark(chunk)`.
- **02절**: `pdfplumber.open()`·`extract_text(layout=True)`·`extract_tables()`. 함수 `make_cell_text()`·`make_row_text()`. 용어 글자 층·표 읽기·글자 인식·OCR 후보 쪽.
- **03절**: `DocxDocument`·`paragraphs`·`style.name`·`tables`, `BeautifulSoup`·`find_all`·`get_text`, `csv.DictReader`. 함수 `read_row_values()`·`pick_tag_texts()`·`make_unit_record()`·`make_unit_mark()`.
- **04절**: `open(..., "rb")`·`read(8)`·`hex()`, `zipfile.is_zipfile`·`ZipFile`·`namelist()`·`read()`, `ElementTree.fromstring`·`root.iter()`. 함수 `read_head_hex()`·`make_local_name()`·`read_body_text()`·`make_section_mark()`·`recognize_file_kind()`·`read_hwpx_body()`.
- **05절**: `CharacterTextSplitter(separator=, chunk_size=, chunk_overlap=)`·`split_text()`, `RecursiveCharacterTextSplitter(separators=, keep_separator="end")`·`split_documents()`, `tiktoken.get_encoding()`, `RecursiveCharacterTextSplitter.from_tiktoken_encoder()`. 함수 `make_length_list()`·`count_tokens()`·`make_token_list()`·`find_missing_words()`·`find_chunks_with_words()`·`find_over_limit()`.
- **06절**: `MarkdownHeaderTextSplitter(headers_to_split_on=)`·`split_text()`·`chunk.metadata["heading"]`, `SemanticChunker(embedding_model, breakpoint_threshold_amount=)`·`split_documents()`, 딕셔너리 `copy()`. 함수 `mark_heading_line()`·`make_markdown_text()`·`make_text_list()`·`make_heading_record()`.
- **07절**: `OpenAIEmbeddings(model=)`·`embed_documents()`·`dimensions=256`·속성 `model`·`dimensions`, `tempfile.mkdtemp()`, `LocalFileStore`, `CacheBackedEmbeddings.from_bytes_store(namespace=, key_encoder="sha256")`. 함수 `make_size_list()`.
- **08절(새로)**: `InMemoryVectorStore(embedding=)`·`add_documents()`·`similarity_search_with_score(질문, k=)`·`store.store[문서 id]["vector"]`(Ch 9 03절과 같은 모양을 이 챕터에서 처음 씀), `with open(경로, encoding="utf-8")`로 파일 읽기, `str(숫자).zfill(4)`, `time.strftime("%Y%m%dT%H%M%S")`, `os.makedirs(경로, exist_ok=True)`, `hashlib.sha256(바이트).hexdigest()`(Ch 7 08절 코드), `json.dumps(딕셔너리, ensure_ascii=False)`·`json.loads()`, `글.splitlines()`. 함수 `name_chunks()`·`run_setting()`·`make_doc_id_list()`·`print_result_rows()`·`make_retrieved_list()`·`make_record()`.
- **08절 용어 네 개**: **실험 격자(experiment grid)**, **같게 유지할 조건(controlled condition)**, **기록 줄 수(logged candidates)**, **결과를 확인한 자료 범위(evaluation scope)**. 「실험 기록」은 새로 만들지 않고 Ch 9 06절 **「실행 기록 한 줄」**을 씁니다. 설정으로 만든 이름이 필요하면 Ch 9 말 **「색인 이름표」**를 쓰세요(08은 이름을 만들지 않고 `config` 칸에 설정을 그대로 적었습니다).
- **01~08절이 쓰지 않은 Python**: `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·try·`raise`·`+=`·`enumerate`·`zip`·`sum`·`max`·`any`·`all`·`isinstance`·`join`·`sorted(key=)`·f-string 안 계산·f-string 형식 지정·타입힌트·`@`·`BaseModel`·`Path.cwd()`·`parents`·`glob`·`datetime`·모델 답·임베딩 값 `assert`. `with`는 08절이 파일 읽기·쓰기에서 처음 썼습니다.

### 실습 절(09)이 이어 쓸 이름과 값

- **경로**: `candidates = [".", "../../..", "../../../.."]`·`root_path`(교재 출력 `.`), `corpus_path`(= `root_path + "/labs/data/rag-corpus"`), `manifest_path`, `pdf_path`(= `corpus_path + "/pdf/easy/E01.pdf"`), `fixtures_path`.
- **문서·쪽**: `E01.pdf` 2쪽 글 905자·26줄(01·02·05·06·07절), 쪽별 글자 수 `45 · 905 · 925 · 871 · 270`. 말뭉치 18건 93쪽(08절), 글자 층이 빈 쪽 3개(`H05` 1~3쪽)라 글이 있는 문서는 17건.
- **나누기**: `separator_order = ["\n\n", ". ", "\n", " ", ""]`, 05절 목표 200자 재귀 방식 문서 청크 6개 `[185, 147, 86, 164, 130, 188]`, 06절 구조 방식 3개 `[223, 470, 182]`·시맨틱 방식 기준값 95에서 2개, 08절 목표 400자 여섯 설정 `[212, 232, 228, 245, 220, 235]`.
- **임베딩·색인**: `embedding_model_name = "text-embedding-3-small"`·`embedding_model`(차원 수 안 줌 = 숫자 1536개), `search_count = 5`, `chunk_target = 400`, `overlap_values = [0, 100]`.
- **질문·정답**: 평가셋 Q001 「미르시립도서관의 정기 휴관일은 언제인가요?」·정답 문서 ID `['E01']`(글자까지 같아야 함, 평가셋 30줄). 05·06절 지킬 말 `closure_words = ["정기 휴관일", "화요일에도 휴관"]`.
- **조각·비용**: `encoding`·`count_tokens(text)`(규칙 `cl100k_base`), 2쪽 글 조각 수 869, 말뭉치 전체 조각 수 59238, `embedding_rate = 0.02`·`tokens_per_million = 1000000`.
- **비유 계열**: 01-5 서류와 봉투 → 02-5 칸막이 상자 → 03-5 공책과 장부 → 04-5 잠긴 상자와 주머니 → 05-5 세 줄로 자른 띠 → 06-5 문패와 무늬 → 07-5 서랍과 표찰 → 08-5 상자 세 개와 기록 용지. Ch 9의 카드 상자(= 벡터스토어)·흰 카드(= 문서 청크)·노란 쪽지(= 질문)를 이어 씁니다.

### 요청 수와 비용 제약

- 절별 서비스 요청: 01~05절 **0번**, 06절 임베딩 2번, 07절 임베딩 6번, 08절 임베딩 13번(색인 6 + 검색 6 + 값 바꿔 보기 1). 답을 쓰는 모델(`init_chat_model`)은 **이 챕터에서 한 번도 부르지 않았습니다**.
- 실습 절은 규격 §7-2에 따라 **모델 호출 3~5번**입니다. 색인 한 벌을 만들면 임베딩 요청이 한 번, 검색 한 번에 또 한 번입니다. 말뭉치 18건으로 색인을 만들면 한 벌에 약 59000조각(약 0.0012달러)이므로, 실습에서는 **색인을 두 벌 이하**로 두거나 문서 하나(`E01.pdf`)만 쓰세요.
- 이 챕터에 `langchain` 메인 패키지가 없습니다. `from langchain.chat_models import init_chat_model`이 되는지 확인하지 않았습니다(01~08절 모두 부르지 않음). 실습에서 답을 쓰는 모델이 필요하면 **먼저 import가 되는지 확인**하세요.
- 요금 확인일: 임베딩 `text-embedding-3-small` 100만 토큰당 0.02달러(OpenAI 모델 안내 2026-09-17 확인).

### 실습 절이 건드리면 안 되는 파일과 기록 계약

- **`runs/continuity-ch10-indexing.jsonl`을 실습 절이 쓰지 마세요.** 08절만 쓰는 파일이고 Ch 11 입력입니다. 현재 정본 SHA-256 **`58cc790c45df9bf9cfbdda21a4de267bd10a7749568f1306d9625657d5ebda45`**, 6줄, `source_run_id` `20260918T061902-ch10-01` ~ `-06`.
- **`runs/continuity/` 사본 48개도 지우지 마세요**(`check_course_continuity.py` 184행이 옛 정본의 줄마다 그 이름의 사본을 찾습니다). `runs/` 전체는 64개입니다.

| 항목 | 값 |
|---|---|
| 최상위 키 7개 | `qid`·`question`·`gold_doc_ids`·`source_chapter`(`ch10`)·`source_run_id`·`config`·`retrieved`. Ch 9와 달리 `answer` 칸이 없습니다 |
| `config` 키 6개 | `chunk_method`(`char`·`recursive`·`token`)·`split_config`·`embedding`·`dimensions`(**1536**, 07절 결정으로 256에서 바뀜)·`k`(5)·`inputs`. `inputs`는 `corpus_scope`(`"디지털 PDF 18건"`)·`corpus_manifest_sha256`·`evaluation_dataset_sha256` |
| `retrieved` 항목 키 5개 | `doc_id`·`chunk_id`·`page`·`rank`·`score`. `rank`는 1부터 빈틈없이, `page` 1 이상 |
| `chunk_id` 모양 | `ch10:char:0000`(네 자리 채움). Ch 9는 `ch09:6f9f83db90:0`입니다 — 모양 차이를 08절 b7과 노트북 6절에 적었습니다 |
| 줄 수 7 제약 | `finalize_continuity_evidence.py` 51행 `assert len(source_ids) == 7`(ch09 1줄 + ch10 6줄) |
| k=5와 지표 제약 | 같은 파일 54~58행이 ch10 실행마다 `recall_at_5 == 1`·`precision_at_5 == .2`·`ndcg_at_5 == 1`·`recall_at_logged_candidates == 1`을 봅니다. `evaluate.py`의 `dedupe_docs()` 때문에 **정답 문서 E01이 겹침 없는 상위 목록의 첫 자리**여야 하고 상위 5건에 정답 문서가 하나만 있어야 합니다. 08절 여섯 실행을 `evaluate.py`로 직접 돌려 네 조건을 모두 확인했습니다 |

- **다른 챕터 기록도 읽지 않았습니다.** Ch 6·7·8 비용 기록 사슬과 Ch 9 `runs/`는 이 챕터가 읽지도 쓰지도 않습니다.
- **과정 단계 검사를 실제로 돌려 확인했습니다.** `textbook/qa/check_course_continuity.py`는 **212행 zip 신선도**(`part1-practice.zip/…`)에서, `textbook/part3/qa/check_continuity.py`는 **154행 zip 신선도**(`part2-practice.zip/…`)에서 멈춥니다. 정본을 다시 쓴 것이 두 검사의 기록 계약 블록을 지나갔다는 뜻입니다(zip 재생성은 전체 마감 몫).
- **실습 폴더 모듈은 고치지 않습니다.** `document_processing.py`(`37ca2cc9…`)·`experiment.py`(`342e85b0…`)·`tests/`·`fixtures/`(수정 시각 2026-09-08). 모듈 함수는 노트북과 이름이 비슷하고 모양이 다릅니다 — `split_char()`는 구분자를 쓰지 않고 문자 수로 그대로 자르고, `split_recursive()`·`split_token()`의 끊을 자리 순서는 `["\n\n", "\n", "다. ", ". ", " ", ""]`이며, `experiment.py`는 임베딩 모델 두 개와 구조 방식을 쓰고 `runs/examples/`에 적습니다. 실습 절에서도 모듈을 부르지 않는 쪽이 앞 절과 이어집니다.

### 테스트·묶음·절 수 상태

- 실습 폴더 테스트 **38 passed**(01~08절 작업 전후 모두 같음). 테스트는 `runs/continuity-*`를 읽지 않습니다.
- **학생 묶음**: 이 챕터 노트북이 읽는 입력은 `labs/data/rag-corpus/pdf/*/*.pdf`·`manifest.json`, `labs/part3/ch10-document-processing/fixtures/` 다섯 개, `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl`입니다. 모두 `build_bundle.py`(`data`·`FIXTURES`)와 `textbook/part3/public-files.json`에 이미 있어 **01~08절에서 허용 목록을 고치지 않았습니다.** 실습 절이 새 입력을 읽게 되면 `part3-practice.zip`을 풀어 묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리에서 경로 셀을 돌려 확인하세요.
- **절 수는 8개 그대로**입니다. 실습 절 09를 붙일 때 함께 고칠 곳: `_build.py` `SECTIONS`에 주제까지 넣은 제목 한 줄, `render_index()`의 「개념 8절」과 「24h · 강의 8h · 실습 16h」 문장, `_src/index.html` 절 표, `textbook/part3/_build_index.py` `CHAPTERS`의 ch10 절 수 칸(8 → 9, 강의 시수 8은 그대로), `qa/visual-results.json` 행 수(+2), `textbook/part3/qa/finalize_continuity_evidence.py` 15행 `assert len(visual) == 88`(Ch 9가 90으로 고칠 예정이므로 ch10 09절까지 붙으면 92).
- meta 시수: 01~08 모두 「강의 1h | 실습 2h」이고 합이 강의 8h·실습 16h로 `render_index()`와 같습니다. **실습 절 30분은 챕터 시수에 더하지 않고** 챕터 요약에 적습니다(규격 §7-2).
- 챕터 안 기록: `qa/verification.md` 표에 08절 행을 더했고 아래 메모도 채웠습니다. `집필점검표.md` 첫 표의 08절 행을 채웠고, 두 번째 표(게이트·검증)에 **07절 행이 빠져 있어 07·08 두 행을 함께 더했습니다**(07절 값은 `07-diagnosis.md`·`qa/verification.md`에서 가져왔습니다). 첫 표의 07절 행은 본문 안 `|`가 이스케이프되지 않아 칸이 여덟 개로 보입니다 — 07절 기록이라 고치지 않았고 2차 검토 대상으로 적어 둡니다.
- 루트 `textbook/qa/upgrade-progress.md`의 Ch 10 행은 아직 「절 개선 중(01 완료)」입니다. 챕터 밖 파일이라 절 작업자가 고치지 않았습니다(02~08 모두 같음). 오케스트레이터 몫입니다.

### 실습 절 주제 후보와 제약 (정하는 것은 실습 절 작업자)

- 08 b8·노트북 정리 끝은 **지금 Ch 11·Ch 12를 가리킵니다**(브리핑 지시대로 그대로 두었습니다). 실습 절을 붙일 때 그 단락과 노트북 정리 끝을 09절로 고치세요(규격 §7-2).
- 챕터 소재와 이어지는 작은 상황 하나에 앞 절 기능 2~3개를 붙입니다. 이 챕터에서 아직 한 번에 이어 보지 않은 묶음은 「형식이 다른 문서 두 개를 읽어(01·03·04) 같은 칸 기록을 붙이고(01·03) 한 방식으로 나눠(05) 한 색인에 넣어 찾기(08)」입니다. 견본 `fixtures/`와 `E01.pdf`를 함께 쓰면 요청 수가 적습니다.
- 「강사 시연」이라는 이름·문구를 쓰지 않습니다. 새 문법·새 API를 넣지 않고 위 「가르친 것」 목록 안에서만 씁니다.

### 아직 안 가르친 것 (실습 절이 설명 없이 전제하면 안 됨)

Ch 9 요약 §6 전체에 더해, 01~08절에서도 하지 않은 것:

- **검색·색인**: 다른 임베딩 모델, 차원 수를 준 색인, 점수 기준값·거르기·MMR, 색인 파일 저장과 다시 불러오기, `as_retriever()`, `similarity_search_with_score_by_vector`, `ids` 직접 지정, 문서·질문 앞머리 글, 질문 쪽 벡터 저장, 여러 질문을 한 번에 돌려 평균 내기, 같은 조건 반복 요청, 검색 지표 계산(Ch 11), 다른 벡터스토어(점수 뜻이 달라질 수 있음 — Ch 9 요약 §5).
- **생성**: 답을 쓰는 모델 호출, 근거를 넣은 메시지 목록, 출처 인용 검사, 답 정확성 판정. **이 챕터는 검색 결과까지만 봅니다.**
- **문서**: 글자 인식(OCR) 실행, 두 단 레이아웃과 읽기 순서, 선 없는 표·병합 셀 표, 본문 XML이 여러 개인 HWPX, 암호가 걸린 문서, HWP 전용 도구, 상용 파서(Upstage·LlamaParse), 02절 표 읽기 결과를 문서 청크로 쓰기, 시맨틱 방식 기준값 0.
- **Python**: 위 「01~08절이 쓰지 않은 Python」 목록, 실습 폴더 모듈 `import`, `set` 메서드, `deepcopy`, 딕셔너리 `|`, `**딕셔너리` 풀어 넘기기.

## 실습 → 챕터 검토

(09절 챕터 끝 실습 절 2026-09-18. 결과는 `09-diagnosis.md`, 게이트 G1~G7 **0**(새로 만든 절이라 「전」 수치 없음), 챕터 전체 **9/9 PASS**, 코드 셀 30(준비 3), 검사 문장 443, **임베딩 요청 4번**(`text-embedding-3-small` 기본 설정, 비용 어림 `3.62e-05`달러), 새 커널로 두 번 실행(교재 출력은 두 번째, 2026-09-18T06:57:44Z). 삽화 09-4 1차 채택(job `4060bc9e-…`, 2차 `d2620fb0-…` 탈락, 4크레딧, 잔액 2788), Mermaid 3장. `verify.py --chapter` `PASS 9 sections / 215 code cells (max 14 lines)`. 이 챕터 개념 8절 + 실습 1절이 모두 끝났습니다)

### 09절이 만든 것과 실행 결과

- 제목 「09 · 문서 처리 실습: 형식이 다른 문서를 한 색인에 모아 찾기」, 파일·slug `09-문서-처리-실습`, 형식 experiment, meta 「실습 30분 · 새 용어 0」.
- 조립: 형식별 읽기(01·03·04) → 형식별 기록(01·03·04) → 표시 함수 고르기 `pick_mark()`(새) → 재귀 방식 200자 나누기(05) → 색인·검색(08) → 점검표 `print_hit_rows()`(새). 조립 함수는 `run_index(index_documents, index_splitter)` 하나입니다.
- 실행 1(색인에 PDF 한 건, 문서 청크 6개): 상위 다섯 줄이 모두 `[E01 p.2]`, 1위 147자 점수 `0.33`(질문과 관계없는 도서관 운영 목표 글).
- 실행 2(색인에 세 형식, 문서 청크 8개): 1위 `[sample docx]` 26자 점수 `0.63`, 2~5위는 `[E01 p.2]` 네 줄이 차례 그대로 한 칸씩 내려감. HWPX 문서 청크는 두 실행 모두 상위 다섯 줄에 없습니다.
- **점수 경계 하나**: 셋째 줄 점수가 두 실행에서 `0.31`·`0.3`로 갈렸습니다(소수 둘째 자리 자름). 1위 점수 `0.33`·`0.63`만 그림 라벨과 결론에 썼습니다.
- 새 함수 세 개(`pick_mark`·`run_index`·`print_hit_rows`) 말고는 **새 API·새 문법 0개**입니다. 답을 쓰는 모델은 이 챕터에서 끝까지 부르지 않았습니다(`init_chat_model` import 가능 여부도 확인하지 않았습니다).

### 실습 절이 답한 앞 절의 물음

- handoff §04 → §05의 「출처 표시 함수가 세 개이니 형식이 섞인 글에서 어느 것을 쓸지 정하라」에 답했습니다. 세 함수를 고치지 않고 `pick_mark()`가 `page`·`section`·`row` 순서로 칸을 보고 고릅니다(실습 폴더 `_with_chunk_metadata()`와 같은 순서).
- handoff §03 → §04의 「`doc_id`가 겹칠 수 있다」는 b7 항목으로 이어 적었습니다. 이번 세 파일은 `E01`·`sample`·`minimal-marker`로 갈립니다.

### 챕터 검토자가 확인할 것

- **09절 본문**: b3 절 표(01·03·04·05·07·08·Ch 9 05절), b4 비유 단락과 삽화(카드 수를 노트북 문서 청크 수 8과 맞추지 않았고 그 사실을 그림 읽기에 적었습니다), b4 조립도·함수 표·표시 순서 표, b5 실행 1 순서 그림, b6 비교 그림과 점수 경계 단락, b7 열 항목, b9 복습 5문제.
- **08절 수정 두 곳**(`mdpatch.py`, **재실행 없음**): `_src` b8 「다음 학습」 두 단락과 노트북 정리 끝 세 줄. 08 노트북은 마크다운 셀 하나만 달라졌고 코드 셀·출력은 그대로입니다.
- **`_src/index.html`**: 09행과 학습 범위·자료·다음 학습 단락을 고쳤습니다. 남은 개선 전 문장은 「챕터 개요」 첫 단락과 `[[미정: 임베딩 모델]]` 표시입니다(강사 확인 항목이라 두었습니다).
- **챕터 밖 파일 두 개**: `textbook/part3/_build_index.py` ch10 절 수 8 → 9, `textbook/part3/qa/finalize_continuity_evidence.py` 15행 `assert len(visual) == 88` → `92`(주석 세 줄). 앞 절들은 챕터 밖 파일을 고치지 않았습니다.
- **화면 검사 파일 두 개**: `textbook/_notebook/checks/ch10-document-processing/visual-results.json`(18 → 20행, 공용 `visual.cjs` 20/20 PASS)와 챕터 `qa/visual-results.json`(18 → 20행). 후자는 `qa/check_visual.cjs`의 14px 허용 목록을 공용 `visual.cjs`와 같게 맞춘 뒤 다시 돌린 결과입니다.
- **옮긴 파일 하나**: `qa/check_content.py` → `qa/upgrade/before/qa-scripts/`(b1~b11·instructor·`{{code:}}`·`{{output:}}` 요구, 참조 코드 0곳, Ch 9 선례). `qa/content-results.json`은 그 스크립트의 개선 전 결과로 남아 있습니다.

### 건드리지 않은 것 (해시 확인)

- `runs/` 전체 64개 묶음 해시 `2a73b21a073dfc9f76b606393abd85a0b94f409174cfdf8e6014737f45cdf84e`, 정본 `continuity-ch10-indexing.jsonl` `58cc790c45df9bf9cfbdda21a4de267bd10a7749568f1306d9625657d5ebda45`(6줄), 사본 48개 그대로.
- `document_processing.py` `37ca2cc9…`·`experiment.py` `342e85b0…`·`tests/`·`fixtures/` 그대로, 테스트 **38 passed**(작업 전후 같음).
- 01~07절 HTML 해시 그대로. 08절 HTML은 다음 절 링크와 b8 문단만 달라짐(`0273e394…` → `98d3c32c…`). Ch 11 평가셋과 Ch 6~9 사슬 기록은 읽지도 쓰지도 않았습니다.

### 전체 마감에 남은 순서

1. `textbook/downloads/part3-practice.zip` 재생성 — 09 노트북이 아직 묶음에 없습니다. 09절이 읽는 입력 세 개(`pdf/easy/E01.pdf`·`fixtures/sample.docx`·`fixtures/minimal-marker.hwpx`)는 이미 허용 목록에 있어 `build_bundle.py`·`public-files.json`은 고치지 않았습니다. `check_public_file()`·`validate()`·`validate_parts()`를 09 노트북에 직접 돌려 통과했습니다.
2. `textbook/part3/qa/run_continuity_bundle.py`(묶음 연기 실행은 08절 노트북만 씁니다).
3. ch09 HTML을 공용 `visual.cjs`로 다시 찍어 `checks/ch09-rag-first-run/visual-results.json`을 14 → 16행으로. 그다음 `finalize_continuity_evidence.py`가 92를 만족합니다(지금은 90).
4. `textbook/part3/_build_index.py`로 Part 3 목차 재생성(ch10이 9절로 표시됩니다). 절 수 검사는 이미 지납니다.
5. 두 continuity 검사는 지금 각각 `check_continuity.py` 154행·`check_course_continuity.py` 212행 zip 신선도에서 멈춥니다(09절 전과 같은 자리).
6. 챕터 요약 `qa/upgrade/chapter-summary.md`와 루트 `textbook/qa/upgrade-progress.md` Ch 10 행(아직 「절 개선 중(01 완료)」)은 오케스트레이터 몫입니다.

### 챕터 요약에 넣을 것 (오케스트레이터용 메모)

- 실습 절 30분은 `_build.py` `render_index()`의 「24h · 강의 8h · 실습 16h」에 더하지 않고 실습 16h 안입니다(규격 §7-2). 01~08절 meta 합(강의 8h·실습 16h)은 그대로이고 09절 meta는 「실습 30분」입니다.
- 이 챕터가 쓴 출처 표시 함수는 세 개이고 09절이 `pick_mark()`로 고릅니다. Ch 11·12가 형식이 섞인 색인을 다루면 이 순서를 이어 쓰세요.
- 09절은 파일을 쓰지 않습니다. Ch 11이 읽는 입력은 08절 기록 여섯 줄 그대로입니다.
- 아직 안 가르친 것(§08 → 실습 목록 그대로)에 더해 09절도 하지 않은 것: DOCX 표·HTML 견본을 문서 청크로 쓰기, 쪽이 없는 형식에 자리 칸을 새로 두기, 검색 결과 여섯째 줄 아래 순위 보기, 점수 기준값·거르기, 여러 질문 평균, 검색 지표(Ch 11).

## §2-7 리팩터 (2026-09-21)

규격 `textbook/QUALITY-UPGRADE.md` §2-7을 Ch 10에 적용했습니다(Ch 5·7·8·9 다음, 모양은 Ch 9 `handoff.md` §2-7). 앞 절·Ch 8·Ch 9에서 배운 함수는 도구 파일 `labs/part3/ch10-document-processing/notebooks/rag_tools.py`에서 한 줄로 가져옵니다. 그림·결과 읽기·설명·정직성 규칙과 절마다의 학습 내용은 그대로 두고, 코드와 그 코드를 가리키던 문장만 고쳤습니다. 삽화는 새로 만들지 않았습니다. 리팩터 직전 스냅숏은 `qa/upgrade/before-2-7/`(`_src`·노트북·`tests/*.py`·`generators/author_*.py`·그림 mmd/캡션·빌드 HTML·`lab/`(README·pyproject)·`part3/`(옛 `part3-practice.zip`·`_build_index.py`·`public-files.json`·Part 3 목차·`integration-results.json`·`delivery-results.json`)·`runs/continuity-ch10-indexing.jsonl`(옛 정본)·`runs-sha256-before.txt`/`runs-sha256-after.txt`·`runs/moved/`)입니다.

### 조사 결과 (AST, 노트북 아홉 개)

- 함수 이름 37개, 정의 66번 → 다시 정의 29번. **챕터 안에서 다시 적은 29번은 모두 처음 정의와 본문이 같았습니다**(`ast.unparse` 대조, 주석만 다름).
- 앞 챕터와 같은 이름 5개: `load_pdf_pages`(Ch 9 02, Ch 9 도구 파일 판과 본문 같음) · `make_source_mark`(Ch 9 03 노트북과 본문 같음) · `find_missing_words`(Ch 8 03, Ch 9 도구 파일 판과 같음) · `count_tokens`(아래) · `make_record`(Ch 6 02 `make_record(model_id, status, output_tokens)`와 **이름만 같고 본문·인자·뜻이 다름** → 08에 그대로 둠, 08만 씀).
- `count_tokens`: 이 챕터 05~08절 판은 `def count_tokens(text): return len(encoding.encode(text))`(바깥 `encoding`을 읽는 한 줄 판, 노트북은 「Ch 9 02절과 같은 코드」라고 적었지만 Ch 9 판은 두 줄이었음). 계산이 같고 이 챕터가 새로 고친 판이 아니라 Ch 9 도구 파일 판 `count_tokens(encoding, text)`(본문 두 줄)로 합쳤습니다.
- 벡터 계산(점곱·길이·코사인·거리·softmax·정렬)은 **0곳**입니다. 07 `make_size_list()`는 벡터마다 숫자 개수(`len`)만 세고, 08·09의 점수는 `InMemoryVectorStore`가 계산합니다. 그래서 NumPy는 쓰지 않았습니다(새 NumPy 이름 0개).

### 도구 파일 `rag_tools.py` (함수 14개, 코드 97줄(import 세 줄 포함), SHA-256 `fac633b15d0fc07d38eccfc7b4adb170e65c7db5e8f686dd6daad8588a355138`)

| 함수(인자) | 배운 절 | 가져가는 절 | 배운 판과 다른 점 |
|---|---|---|---|
| `count_tokens(encoding, text)` | Ch 8 01 | 05·06·07·08 | 바깥 `encoding`을 읽던 판 → 규칙 객체를 첫 인자로(Ch 9 도구 파일 판과 같음). 05절 준비 설명에 한 문장, 호출 5곳 `count_tokens(encoding, …)` |
| `find_missing_words(text, words)` | Ch 8 03 | 05(그리고 `find_chunks_with_words` 안) | 없음 |
| `load_pdf_pages(pdf_path, doc_id)` | Ch 9 02 | 01·05·06·07·08·09 | 없음(본문 9줄, Ch 9 판 그대로) |
| `make_source_mark(chunk)` | Ch 9 03 | 01·02·05·06·09 | 없음 |
| `make_source_record(file_path, page, parser)` | 01 | 02·05·06·09 | 없음 |
| `make_cell_text(label, cell)` | 02 | (`make_row_text` 안에서만) | 없음 |
| `make_row_text(header_row, row)` | 02 | 03 | 없음(본문 9줄) |
| `make_unit_record(file_path, parser)` | 03 | 04·09 | 없음 |
| `make_unit_mark(chunk)` | 03 | 04·09 | 없음 |
| `make_local_name(tag_name)` | 04 | (`read_body_text` 안에서만) | 없음 |
| `read_body_text(xml_root, wanted_name)` | 04 | 09 | 없음 |
| `make_section_mark(chunk)` | 04 | 09 | 없음 |
| `make_length_list(chunk_texts)` | 05 | 06·07 | 없음 |
| `find_chunks_with_words(chunk_texts, words)` | 05 | 06 | 없음 |

- 머리: Ch 9 모양 독스트링(무엇을 모았는지 / `from rag_tools import 함수이름` / 노트북과 같은 폴더 / 함수마다 배운 절 주석 / 노트북 이름을 읽지 않고 인자로 받음) + `from pathlib import Path`·`from pypdf import PdfReader`·`from langchain_core.documents import Document`. 함수마다 `# NN절에서 배웠습니다 — …` 또는 `# Ch 8/Ch 9 NN절에서 배웠습니다 — …`, 인자가 바뀐 `count_tokens`만 둘째 줄 주석. 순서는 Ch 8 → Ch 9 → 이 챕터 01~05절.
- 금지 문법 0건(게이트 함수 `g1_ladder`·`g2_shape`를 파일 전체에 돌리면 `multiple_defs_in_cell`·`over_15_lines`만 — 셀 규칙이라 해당 없음, Ch 7~9와 같음). 함수 본문 최대 9줄(`load_pdf_pages`·`make_row_text`, 배운 판 그대로), 규격 §2-2 L2(10줄 이하) 안. 14개 모두 처음 가르친 판과 `ast.unparse` 글자가 같습니다(`count_tokens`만 Ch 9 도구 파일 판과 같음).
- 넣지 않은 것(그 절만 씀): 02 `count_page_lengths`·`find_ocr_candidates`, 03 `read_row_values`·`pick_tag_texts`, 04 `read_head_hex`·`recognize_file_kind`·`read_hwpx_body`, 05 `make_token_list`·`find_over_limit`, 06 `mark_heading_line`·`make_markdown_text`·`make_text_list`·`make_heading_record`, 07 `make_size_list`, 08 `name_chunks`·`run_setting`·`make_doc_id_list`·`print_result_rows`·`make_retrieved_list`·`make_record`, 09 `pick_mark`·`run_index`·`print_hit_rows`.
- **01도 가져옵니다**: 01은 Ch 9 함수 두 개(`load_pdf_pages`·`make_source_mark`)를 「같은 코드로」 다시 적던 절이라 §2-7 3항대로 가져오고(Ch 7 01 선례), 이 절에서 처음 가르친 `make_source_record()`만 노트북에 남겼습니다. 01 「6. Ch 9 출처 표시 함수 그대로 쓰기」의 학습 내용(칸이 늘어도 두 칸만 읽는 함수는 그대로 동작)은 가져온 함수로 같은 출력(`출처 표시: [E01 p.2]`)을 보여 그대로입니다.

### 가져오기 셀과 설명

- 기존 import 준비 셀 끝에 `# …를 도구 파일에서 가져옵니다` + `from rag_tools import …`(알파벳 순, 길면 두 줄): 01 `load_pdf_pages, make_source_mark` / 02 `make_source_mark, make_source_record` / 03 `make_row_text` / 04 `make_unit_mark, make_unit_record` / 05 `count_tokens, find_missing_words, load_pdf_pages` + `make_source_mark, make_source_record` / 06 `count_tokens, find_chunks_with_words, load_pdf_pages` + `make_length_list, make_source_mark, make_source_record` / 07 `count_tokens, load_pdf_pages, make_length_list` / 08 `count_tokens, load_pdf_pages` / 09 `load_pdf_pages, make_section_mark, make_source_mark, make_source_record` + `make_unit_mark, make_unit_record, read_body_text`. 안에서만 쓰는 `make_cell_text`·`make_local_name`·(06의) `find_missing_words`는 가져오지 않습니다.
- 쓰지 않게 된 import를 뺐습니다(AST로 확인): 04·09 `from pathlib import Path`, 05·06 `Path`·`PdfReader`, 07·08 `PdfReader`·`Document`, 09 `PdfReader`. 준비 셀 첫 주석의 「PDF 읽기·문서 객체」를 그에 맞춰 줄였습니다(05~08).
- 준비 설명 셀: 고정 세 문장 「앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.」 + 「이 노트북은 NN절 `f()`…를 가져옵니다.」(01~09 모두). 인자 모양 문장은 처음 가져오는 05만(「함수 `count_tokens()`는 Ch 9 도구 파일 판처럼 조각 세는 규칙 객체를 첫 인자로 받습니다.」).
- 정의 셀과 「이 셀은 함수를 만들기만 하므로 출력이 없습니다」 결과 읽기를 지우고 앞뒤 설명 단락으로 합쳤습니다(「준비 셀에서 가져온 Ch 9 02절 로더 함수 `load_pdf_pages()`는 …」). 소절이 통째로 없어진 곳이 없어 **노트북 절 번호는 그대로**입니다.
- `count_tokens` 셀: 05 「조각을 세는 규칙을 이름에 담고 … 함수를 만듭니다」 셀 → `encoding = tiktoken.get_encoding("cl100k_base")` + `print("조각 세는 규칙 이름:", encoding.name)`(새 출력 한 줄 `조각 세는 규칙 이름: cl100k_base`). 05 `make_token_list()` 설명에 「조각 세는 규칙 `encoding`은 함수 밖에서 읽습니다」를 옮김. 07은 셀에서 `def`만 빼고, 08은 규칙만 불러오던 셀에 같은 `print` 한 줄을 더함(새 출력 한 줄). 06은 정의 셀을 지움(규칙은 임베딩 준비 셀에서 이미 만듦).
- 「같은 코드로 다시 정의합니다」 류 문장: 생성기·노트북·`_src`에서 함수 재정의를 말하던 곳 **0건**. 남긴 「같은 코드」는 경로 후보 셀(데이터 셀)과 06·07·08 「2절은 01·05절과 같은 코드라 강의에서 빠르게 확인합니다」(강의 범위 문장, Ch 9와 같게 둠), 02 값 바꿔 보기 주석 「같은 코드에서 쪽 번호만 4로 바꿔」입니다.
- `_src`: 01~08 b3 목록 뒤에 「노트북은 … 를 도구 파일 `rag_tools.py`에서 가져옵니다」 한 단락, 05·06·07 b3 「조각 세기」 항목(「`count_tokens(text)`를 만들었습니다」 → 「`count_tokens()`로 조각 수를 셌습니다」), 01 b5 01-3 도식 읽기(「Ch 9 03절과 같은 코드」 → 「준비 셀에서 도구 파일로 가져온 Ch 9 03절 함수」), 06 b7 「01절 `make_source_mark()`」 → 「Ch 9 03절」, 09 b3 표 뒤 한 단락·b4 도식 읽기·함수 표 「가져온 곳」(「01절(같은 코드)」 → 「Ch 9 02절(도구 파일)」 등)·「출처 표시를 고르는 순서」의 「01절 함수」 → 「Ch 9 03절 함수」·b5 「함수를 만드는 셀은 열한 개이고 … 정의 셀은 실행만」 → 「함수를 만드는 셀은 세 개입니다. 앞 절에서 배운 함수 일곱 개는 준비 셀에서 도구 파일로부터 가져옵니다」, 01~09 b5 실행 날짜·코드 셀 수(아래).
- 그림: **01-3** 파란 상자 라벨 「Ch 9 03절과 같은 코드」 → 「Ch 9 03절 함수(도구 파일)」(mmd 변경으로 다시 렌더, viewBox 폭 510, PNG로 확인). 09-1 `caption.md` 읽는 법(「노트북에서 정의하는 함수」 → 「노트북이 부르는 함수(기록 붙이기는 도구 파일에서 가져옴)」). 그 밖의 그림 라벨·수치는 출력이 같아 그대로.
- lab README 한 문장(「01~09절 노트북은 앞 절과 앞 챕터에서 배운 함수를 `notebooks/rag_tools.py`에서 가져오므로, 이 파일을 노트북과 같은 폴더에 그대로 둡니다」).

### 리팩터 전 생성기 문제 한 곳(고침)

- `author_06.py` `FIGURE_ALT`가 검토 반영 전 순서(「보라 상자 … 요청 2번과 파란 상자 끊는 기준값 95」)로 남아 캡션·`_src`·노트북 06-1 alt(「파란 상자 끊는 기준값 95 백분위수와 보라 상자 …」)와 달랐습니다. 캡션 판으로 맞췄습니다. 01~05·08·09는 리팩터 전 생성기 = 리팩터 전 노트북(06·07 실행 날짜 한 줄 말고)이었습니다(`/tmp/ch10-27/gensync.py`).
- 리팩터 뒤 01~09 생성기를 `/tmp`에 다시 써서 지금 노트북과 대조: 코드·마크다운 셀 글자 모두 같음.

### 실습 폴더 테스트

- `tests/test_cache_experiment.py`·`test_chunking.py`·`test_loaders.py`는 `document_processing.py`·`experiment.py`만 가져오고 노트북을 읽지 않습니다(`import`·`grep` 확인) → **고치지 않음**. 전 38 passed → 후 **38 passed**(`UV_PROJECT_ENVIRONMENT=.cache/vm/venv-ch10-document-processing UV_NO_SYNC=1 uv run --project labs/part3/ch10-document-processing python -m pytest -q -p no:cacheprovider labs/part3/ch10-document-processing/tests`).

### 절별 전 → 후 (코드 줄은 주석·빈 줄 제외, `textbook/_notebook/upgrade/count_code.py`)

| 절 | 코드 셀 | 코드 줄 | 바뀐 것 |
|---|---|---|---|
| 01 | 18 → 16 | 116 → 102 (−14) | Ch 9 함수 두 개(`load_pdf_pages`·`make_source_mark`) 정의 삭제 |
| 02 | 18 → 16 | 143 → 132 (−11) | `make_source_record`·`make_source_mark` 정의 삭제 |
| 03 | 23 → 21 | 182 → 168 (−14) | `make_cell_text`·`make_row_text` 정의 삭제 |
| 04 | 24 → 22 | 148 → 133 (−15) | `make_unit_record`·`make_unit_mark` 정의 삭제, `Path` import 뺌 |
| 05 | 24 → 20 | 170 → 141 (−29) | 정의 4개 삭제 + `count_tokens` 정의를 규칙 셀로(출력 한 줄 더함) |
| 06 | 26 → 19 | 185 → 141 (−44) | 정의 7개 삭제 |
| 07 | 23 → 21 | 160 → 142 (−18) | 정의 2개 삭제 + 규칙 셀에서 `def` 뺌 |
| 08 | 29 → 28 | 259 → 247 (−12) | `load_pdf_pages` 정의 삭제 + 규칙 셀에서 `def` 빼고 `print` 한 줄 |
| 09 | 30 → 22 | 211 → 155 (−56) | 정의 8개 삭제 |
| 합계 | **215 → 185** | **1574 → 1361 (−213, −13.5%)** | 도구 파일 97줄을 더해도 1458(−116) |

줄이 늘어난 절은 없습니다. `verify.py --chapter` 셀 최대 14줄(리팩터 전부터 있던 셀, 02 [14] 등).

### 다시 실행과 대조

- 01~09를 `run_section.sh`로 새 커널 2회: A(`/tmp/ch10-27/A/`, 2026-09-21 06:22~06:25 UTC)·B(교재 출력, `/tmp/ch10-27/B/`, 06:25:30~06:26:05 UTC). `/tmp/ch10-27/cmp.py`(소스로 짝지음, 스트림 이름 무시). 값을 고르려고 더 실행하지 않았습니다. 실행 뒤 설명 수정(05 준비 단락 나누기, 09 문장 첫머리 「PDF는」 → 「문서 E01은」)은 B 실행 전에 생성기에 넣었습니다. B 실행 뒤에는 앞 정의 셀이 없어져 어색해진 결과 읽기 네 곳(05 두 곳·06·09의 「이 셀도 함수를 만들기만」)을 `mdpatch.py`로 「이 셀은」으로 고치고 `--no-exec`로만 빌드했습니다(다시 실행하지 않음).
- **A·B 차이**: 01~05·07 **없음** / 06 폐기 예고 경고의 임시 경로(`ipykernel_31` ↔ `_340`, 본문이 「실행할 때마다 달라진다」고 이미 적음) / 08 `recursive | 100` 줄 3·4위(A `M04`·`H03`, B `H03`·`M04` — b5 「3위부터 5위는 순서가 바뀔 수 있습니다」 그대로) / 09 실행 1·비교 표 2위 점수(A `0.3`, B `0.31` — b6 점수 경계 단락이 이미 적은 경계).
- **리팩터 전(2026-09-18)과 대조(첫 주석 줄로 짝지음)**: B의 모든 셀 출력이 리팩터 전과 **글자까지 같습니다.** 다른 것은 새로 생긴 출력 두 줄(05·08 `조각 세는 규칙 이름: cl100k_base`)과 06 준비 셀 경고의 임시 경로·줄 번호뿐입니다. 그래서 결과 읽기·그림 라벨·복습의 인용 값은 **고칠 곳이 없었습니다**. 08은 A에서 3·4위가 바뀐 것을 b5에 「이 페이지 출력 바로 앞의 새 커널 실행에서는 `recursive | 100` 줄의 3위와 4위가 서로 바뀌었습니다」로 적었습니다(1·2위 결론 밖).
- **§2-7 10항 판단 — 입력을 고친 절 없음.** 모델 답을 쓰는 절이 없고(답 모델 0번), 임베딩 결과로 결론을 쓰는 06·07·08·09도 핵심 관찰(06 문서 청크 3개·2개와 지킬 말 번호, 07 1536·256과 캐시 파일 수, 08 여섯 설정 문서 청크 수와 1·2위, 09 실행 1 모두 `[E01 p.2]`·실행 2 1위 `[sample docx]` `0.63`)이 두 실행과 리팩터 전 모두 같습니다.
- 날짜: 생성기 `RUN_DATE`(nbkit) 2026-09-21, 09 키 셀 결과 읽기 「2026-09-21에」(글자로 박힌 날짜를 고침), `_src` 01~09 b5 「이 페이지의 출력은 2026-09-21에」와 코드 셀 수(01·02 열여섯, 03 스물한, 04 스물두, 05 스무, 06 열아홉, 07 스물한 — 07은 「세 번 이어」 → 「두 번 이어」, 08 「네 번 이어」 → 「두 번 이어」). 문서·요금 확인 날짜(2026-09-17·18)는 그대로.
- `outputs_sha256`(전 → 후): 01 `1adf1138` → `ca12fc0c`, 02 `f7b750bc` → `d962fb4d`, 03 `7df82873` → `dbe74eba`, 04 `f471de84` → `f3bb9e35`, 05 `18851bbd` → `84447efa`, 06 `d303aecf` → `9da21fc0`, 07 `ce6ec276` → `6b0b863b`, 08 `36944dba` → `492eb323`, 09 `0c1619ae` → `8a3eca0a`(셀 수가 바뀌어 모두 바뀜).

### 산출 파일(runs) — 전후 해시와 읽는 쪽

| 파일 | 리팩터 전 | 리팩터 후 |
|---|---|---|
| `runs/continuity-ch10-indexing.jsonl` | `58cc790c45df9bf9cfbdda21a4de267bd10a7749568f1306d9625657d5ebda45`(6줄, `source_run_id` `20260918T061902-ch10-01`~`-06`, 6685바이트) | **`0984e1679db1d16afbb37b3b98e4846a0b6629a0a486a917e9d4a0aaa7e69188`**(6줄, `20260921T062600-ch10-01`~`-06`, 6686바이트) |
| 사본 | `runs/continuity/20260918T061902-ch10-0N.jsonl` 등 48개(그대로 남김) | `runs/continuity/20260921T062600-ch10-01`~`-06.jsonl`(정본 줄과 글자 같음). A 실행 사본 `20260921T062506-ch10-0N.jsonl` 6개는 `qa/upgrade/before-2-7/runs/moved/`로 `mv -n`(삭제 아님) |
| `runs/` 나머지 | — | 같음(`runs-sha256-before.txt`/`after.txt` 대조: 정본 한 줄이 바뀌고 사본 여섯 줄이 늘었을 뿐). `runs/` 64 → 70개 |

- **계약 유지**: 최상위 키 7개·`config` 6키(값 전부 같음 — `chunk_method`·`split_config`·`embedding`·`dimensions` 1536·`k` 5·`inputs` 지문 `27541f41…`·`9544b332…`)·`question`·`gold_doc_ids`·`retrieved` 여섯 줄의 `doc_id`·`chunk_id`(`ch10:char:0000` 네 자리)·`page`·`rank`가 **리팩터 전과 모두 같고**, 다른 것은 `source_run_id`와 `score` 일부(소수 넷째 자리 아래, 예: 1줄 4위 `0.466148` → `0.467213`, 2줄 1위 `0.649152` → `0.64923`)뿐입니다.
- **읽는 쪽 확인**: `grep -rn "continuity-ch10-indexing" --exclude-dir=.venv --exclude-dir=.cache textbook labs`.
  - 코드로 읽음 — 값을 박아 두지 않아 수정 없음: `labs/part3/ch11-evaluation/evaluate.py`(`/tmp` 출력으로 실행 → ch10 여섯 실행 지표 `recall_at_5 1.0`·`precision_at_5 0.2`·`ndcg_at_5 1.0`·`recall_at_logged_candidates 1.0`·`recall_at_50 None`, `continuity-upstream-20260918.json`의 ch10 지표와 **모두 같음** — `finalize_continuity_evidence.py` 54~58행 조건 충족), `textbook/part3/qa/check_continuity.py`·`textbook/qa/check_course_continuity.py`(`/tmp/ch10-27/chk/` 사본으로 결과 파일 쓰기만 막고 실행 → 기록 계약 블록 통과, 묶음 재생성 뒤 **`llm-practice.zip` Stale(Part 1 노트북)에서 멈춤** — Ch 9 뒤와 같은 자리), `finalize_continuity_evidence.py`·`run_continuity_bundle.py`(전체 마감 몫, 실행 안 함), `textbook/_notebook/build_bundle.py`(`public-files.json` 경로만).
  - **Ch 11 노트북 01~06이 코드로 읽음**: 01 `config`의 `chunk_method`·`k`, `retrieved`의 순위·문서·쪽·`chunk_id`, 01~05 고유 문서·정답 순위·재현율, 06 `config.inputs` 지문·`evaluate.py --retrieval-log`. 읽는 키·값은 **모두 같음** → 01~05 노트북 출력은 다시 실행해도 같을 것으로 봅니다(실행하지 않음). **바뀌는 것은 06 노트북 출력의 실행 이름 열두 줄**(HTML 06 822~827행 `20260918T061902-ch10-0N | ch10 | 1 | 5 | 1.0 | 0.2 | 1.0`·928~933행 `… | 5 | 2 | 1.0 | 1.0` → `20260921T062600-ch10-0N …`)과 06이 쓰는 `continuity-upstream-*.json`·`upstream-top2-*.json`의 ch10 `run_id`·`top_results` 점수입니다. **Ch 11 노트북은 다시 실행하지 않았습니다.** Ch 11 `_src`는 ch10 실행 이름·해시·점수를 인용하지 않습니다.
  - 새 값으로 고친 것: `textbook/qa/upgrade-contracts.md` §3·§4·§5 줄 추가, 이 handoff·`chapter-summary.md`·`qa/verification.md`·`집필점검표.md`, `author_08.py` 독스트링(다시 실행하면 파일이 바뀐다는 한 줄), `textbook/part3/qa/delivery-results.json`·`integration-results.json`(검사·목차 스크립트가 다시 씀).
  - 그대로 둔 것(당시 기록): Ch 10 `08-diagnosis.md`·`09-diagnosis.md`·`review-round1-A/B.md`·`before/`·`gates-before.json`·이 handoff 앞 절들, Ch 11 `qa/upgrade/handoff.md`·`chapter-summary.md`·`0N-diagnosis.md`·`author_06.py` 40행 독스트링 `58cc790c…`·`review-pack/`, Ch 12 `review-round1-A/B.md`·`qa/verification.md`, `textbook/part3/qa/continuity-evidence/*`·`textbook/qa/continuity-evidence/*`(2026-09-09 옛 증거), `labs/part3/ch11-evaluation/runs/*`(Ch 11 06이 쓴 파일), `textbook/qa/upgrade-progress.md`(읽지 말라는 지시).

### 공용 도구·챕터 밖 변경

- `textbook/part3/public-files.json`: `labs/part3/ch10-document-processing/notebooks/rag_tools.py` 한 줄 추가(ch10 기록 줄 앞).
- `textbook/part3/_build_index.py`: 고치지 않음(절 수 칸 9 맞음). 실행 결과 `Part 3: 36 verified sections; 91 bundled files`(90 → 91) → `textbook/downloads/part3-practice.zip` 다시 만듦(`df60a02b…7666` → `040e53eaf259…45bc5`, 항목 93 → 94, 11.9MB), `textbook/part3/index.html`은 바이트 같음, `textbook/part3/qa/integration-results.json` 다시 씀(코드 셀 1036 → 1006).
- `textbook/part3/qa/check_delivery.py`: **끝까지 통과**(종료 코드 0, 노트북 36·코드 셀 1006·공개 항목 591) → `textbook/part3/qa/delivery-results.json` 다시 씀(`part3-practice.zip` 94항목·새 해시, `llm-practice.zip`은 같음).
- `textbook/qa/upgrade-contracts.md` §3·§4·§5 줄 추가, `textbook/qa/refactor-2-7-progress.md` Ch 10 행.
- 챕터 안: `qa/public-files.json`(새, Ch 9 모양), lab README 한 문장, `author_06.py` alt 고침(위), `figures/01-3-다섯-칸-기록.mmd` 라벨·`09-1-조립도.caption.md` 읽는 법.
- 공용 도구(`run_section.sh`·`count_code.py`·`mdpatch.py`·`upgrade_gates.py`·`build_bundle.py`·`check_*`) 변경 없음.
- **다시 만들지 않은 묶음**: `textbook/downloads/part4-practice.zip`은 `textbook/part3/public-files.json`을 상류 목록으로 읽으므로 지금 묶음 속 `continuity-ch10-indexing.jsonl`은 옛 바이트이고 Ch 10 `rag_tools.py`가 없습니다(Part 4 노트북은 둘 다 쓰지 않음). `llm-practice.zip`도 그대로. `finalize_continuity_evidence.py` 기대값도 그대로. 모두 전체 마감 몫.

### 검사

- `upgrade_gates.py --label after-2-7` **9/9 PASS, G1~G7 0**(`qa/upgrade/gates-after-2-7.json`). `verify.py --chapter` `PASS 9 sections / 185 code cells (max 14 lines)`. 빌드 HTML 10개 `{{` 0건. `visual.cjs`(사본 `/tmp/ch10-27/vis/vis.cjs` = Ch 9 사본, playwright-core + chrome-headless-shell) 01~09 × 1280·390px **18/18 PASS**(`textbook/_notebook/checks/ch10-document-processing/visual-results.json` 20행은 그대로 둠 — `finalize` 행 수 기대값 때문).
- 생성기 ↔ 노트북 대조: 01~09 코드·마크다운 셀 글자 같음. 노트북 AST로 가져오지 않은 이름·쓰지 않는 import 0건(08 `corpus_scope`를 다음 셀에서 만드는 정의 순서는 리팩터 전부터 있던 것, chapter-summary §15). review-pack 01~09 다시 만듦.
- 학생 묶음 확인: 새 `part3-practice.zip`을 `/tmp/ch10-27/bundle`에 풀어 `notebooks/`를 커널 작업 폴더로 09를 새 커널 실행(PYTHONPATH 없음, 키는 실행 프로세스 환경에만) → 코드 셀 22개 오류 0, 경로 셋째 후보 `../../../..`, `rag_tools`에서 일곱 함수 가져오기 정상(임베딩 요청 4번, 값은 교재에 쓰지 않음). 이 실행은 결과 읽기 네 곳(05·06·09 「이 셀도」 → 「이 셀은」, `mdpatch.py`)을 고치기 전 묶음(`4ec90ae2…6f6c`)으로 했고, 그 뒤 다시 만든 지금 묶음(`040e53ea…45bc5`)의 09 노트북과 코드 셀 글자가 같습니다.
- 서비스 요청: 06 2×2 + 07 6×2 + 08 13×2 + 09 4×2 + 묶음 확인 4 = **54번**(모두 임베딩 `text-embedding-3-small`, 답 모델 0번). 01~05는 요청 0. 예상 비용 약 0.016달러(08 색인 여섯 벌 × 2회가 대부분, 08 어림 `0.0078194`달러/회).

### Ch 11 작업자에게

1. Ch 10 기록이 `0984e167…69188`(`source_run_id` `20260921T062600-ch10-01`~`-06`)로 바뀌었습니다. 계약·키·`config`·순위·쪽·문서·`chunk_id`·지표는 같고 **실행 이름과 `score` 소수 넷째 자리 아래만** 다릅니다. Ch 11 06을 다시 실행하면 표의 실행 이름 열두 줄(HTML 06 822~827·928~933행 근처 노트북 출력)과 `continuity-upstream-*.json`·`upstream-top2-*.json`의 ch10 `run_id`·점수가 새 값이 됩니다. 01~05는 읽는 값이 같아 출력이 그대로일 것입니다. 고칠 곳: Ch 11 `author_06.py` 40행 독스트링 해시(`58cc790c…` → `0984e167…`, Ch 9 `294713765a…` → `e0323e89…`도 같은 줄), handoff 계약 해시 줄(당시 기록이면 그대로).
2. Ch 10 `rag_tools.py`는 Ch 10 폴더 안에 따로 있습니다. Ch 11 노트북이 Ch 9·10 함수를 다시 적고 있으면(`unique_doc_ids`·`find_gold_rank` 등은 Ch 11 자체 함수) Ch 11 도구 파일로 옮기되, 앞 챕터 함수는 `# Ch 9/Ch 10 NN절에서 배웠습니다`로 적고 인자 모양은 Ch 9·10 도구 파일 판(`count_tokens(encoding, text)`·`load_pdf_pages(pdf_path, doc_id)`)을 따르세요.
3. Ch 11 06을 다시 실행하면 `runs/`에 `continuity-upstream-*.json`이 새로 생기고 `finalize_continuity_evidence.py` 49행이 가장 새 파일을 고릅니다(계약 §3). 51행 `len(source_ids) == 7`(ch09 1 + ch10 6)은 줄 수가 같아 그대로 맞습니다.
4. 벡터 계산: Ch 10은 NumPy를 쓰지 않았습니다(벡터 계산 0곳). Ch 11에서 코사인·정렬을 직접 계산하면 「Ch 5 02절처럼」으로 가리키고 `np.argsort` 같은 새 이름만 처음 자리에서 한 문장.
5. 임베딩 검색 3~5위 순서와 점수 둘째 자리는 새 커널 두 번에서도 흔들렸습니다(08 `recursive | 100` 3·4위, 09 2위 `0.3`/`0.31`). Ch 10처럼 1·2위·문서 이름·지표만 결론에 쓰면 다시 실행해도 인용이 그대로입니다.
