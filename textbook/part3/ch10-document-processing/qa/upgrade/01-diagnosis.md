# Ch 10 01절 「문서와 메타데이터」 품질 개선 기록

작업 2026-09-18. 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md`.
앞 내용: `textbook/qa/upgrade-course-summary.md`(Part 1·2), 바로 앞 챕터 `textbook/part3/ch09-rag-first-run/qa/upgrade/chapter-summary.md`.
**이 챕터 첫 절**이라 수정 전 게이트를 챕터 전체로 먼저 남겼습니다(`gates-before.json`, 덮어쓰지 않음).

## 1. 게이트 전후

| 게이트 | 수정 전(01절) | 수정 후(01절) |
|---|---|---|
| G1 문법 사다리 | 0 | 0 |
| G2 셀 모양 | 0 | 0 |
| G3 주석 | 0 | 0 |
| G4 실제 모델 | 0 | 0 |
| G5 노트북 설명 | 9 | 0 |
| G6 문장 | 25 | 0 |
| G7 그림 | 3 | 0 |
| 합계 | **37** | **0 (PASS)** |

- 챕터 전체 수정 전 합계(`gates-before.json`, 8절): G1 22 · G2 9 · G3 16 · G4 0 · G5 86 · G6 206 · G7 24 = **363**, 통과 절 0/8.
- 코드 셀 7 → **18**(준비 셀 2 포함), 검사 문장 126 → **306**(검토 반영 뒤 `gates-after.json`. 절 작업 때 기록한 296은 게이트 결과와 달라 검토 A C-7에서 바로잡았습니다).
- G8: 새 커널 실행 PASS(`fresh_kernel: true`, Python 3.12.13, `executed_at` 2026-09-18T01:49:37Z), `verify.py --chapter` **PASS 8 sections / 77 code cells (max 24 lines)**(01절 전 66), `visual.cjs` 1280px·390px 2건 PASS, 빌드 HTML `{{` 잔존 0.

## 2. 수정 전 주요 문제

- **G5**: 제목 셀·「오늘 볼 그림」 첨부가 없었고(노트북 첫 셀이 바로 개념 설명), 코드 셀 일곱 개 모두 뒤 설명 셀이 출력 값을 인용하지 않았습니다. 마지막 After 셀 뒤에는 결과 읽기 셀이 아예 없었습니다.
- **G6**: 70자 초과 9문장, 영문 용어·코드 이름에 조사를 바로 붙여 시작한 문장 13개, 5문장 넘는 단락 3개.
- **G7**: Mermaid 0장(옛 Excalidraw SVG 1장 `01-문서-계약.svg`), 삽화 0장, 그림 설계표 없음.
- 그 밖에(게이트가 세지 않은 것)
  - **데이터가 Ch 9와 끊겼습니다.** 개선 전 01은 `E02.pdf`를 썼고 Ch 9 01~07절은 `E01.pdf`와 출처 표시 `[E01 p.N]`을 썼습니다.
  - **노트북이 읽은 값이 아닌 지어낸 값을 썼습니다.** `raw = {"page": "2", "tags": ["배송", "환불"]}`처럼 로더가 반환한 척하는 딕셔너리를 노트북 안에서 만들고 `int()`·`",".join()`으로 바꿨습니다. 태그 칸은 이 챕터 어디서도 쓰이지 않습니다.
  - **`file_type`·`parser` 칸이 왜 필요한지 실행으로 보이지 않았습니다.** 본문 표에만 적혀 있었습니다.
  - 경로 찾기가 `Path.cwd()`와 `parents`를 쓰고(Ch 9는 후보 경로 `for`+`break`), Before가 `try/except AssertionError`로 감싸여 있었습니다.
  - 본문 b2·b4에 「문서 100건은 아직 제공되지 않았으며」 같은 제작 상황 문장이 있었습니다(규격 §4).

## 3. 바꾼 것

### 학습 질문과 데이터

- 학습 질문(형식이 여러 가지인 문서에서 출처 기록의 칸을 정하고 쪽 번호 기준을 맞추기)과 **paired 형식**은 유지했습니다. Before/After 주제(0부터 센 목록 자리를 쪽 번호로 적기)도 유지했습니다.
- 데이터를 `E02.pdf` → **`E01.pdf`**로 바꿨습니다. Ch 9 01~07절과 같은 문서이고, 출처 표시도 같은 `[E01 p.2]`가 나옵니다.
- Ch 9 코드를 **같은 코드로** 이어 씁니다: `load_pdf_pages(pdf_path, doc_id)`(Ch 9 02절), `make_source_mark(chunk)`(Ch 9 03절). 칸을 다섯 개로 늘려도 `make_source_mark()`가 그대로 동작하는 것을 출력으로 보였습니다.

### 새로 실행으로 보인 것

- 같은 E01 2쪽을 **기본 읽기**(`extract_text()`)와 **레이아웃 읽기**(`extract_text(extraction_mode="layout")`)로 읽어 `905자 26줄` 대 `1396자 51줄`, 글자 수 차이 `491`을 보였습니다.
- Ch 8 03절이 쓴 문장 「정기 휴관일입니다」가 기본 읽기에는 없고(`False`) 레이아웃 읽기에는 있습니다(`True`). Ch 9 01절이 `False`를 본 자리를 이어 「읽는 방법이 글을 바꾼다」로 잇습니다.
- 그래서 Ch 9의 세 칸 기록이 두 결과에 똑같이 붙는 것을 `이 기록에 읽은 방법을 적는 칸이 있는가: False`로 보이고, `file_type`·`parser`를 더해 **다섯 칸**으로 만듭니다.
- 이 챕터가 읽을 파일을 폴더에서 직접 셉니다: `easy | 6`·`medium | 6`·`hard | 6`·`scanned | 3`(21건)과 견본 확장자 `.hwp`·`.hwpx`·`.csv`·`.docx`·`.html`.
- `parser` 값 `pypdf-plain`은 실습 폴더 `document_processing.py`의 `load_pdf(mode="plain")`이 쓰는 이름과 같게 맞췄습니다. 같은 다섯 칸을 만드는 모듈 함수 `normalize_metadata()`가 있고 인자 모양이 다르다는 점을 본문 b7 주의 메모에 적었습니다(규격 §7-2). **모듈은 노트북에서 부르지 않았습니다.**

### 코드 사다리

- 뺀 것: `Path.cwd()`·`parents`, 지어낸 `raw` 딕셔너리, `",".join()`, 타입힌트, `try/except AssertionError`. 
- 쓴 것: 후보 경로 `for`+`break`(Ch 8 06·Ch 9 01 모양), `os.listdir()`, `sorted()`, `Path` 속성 `name`·`stem`·`suffix`, 글 `+`로 경로 만들기, 함수 두 개(`load_pdf_pages` 본문 9줄·`make_source_record` 본문 6줄·`make_source_mark` 본문 4줄, 주석·빈 줄 뺀 줄 수를 직접 셈 — 규격 §2-2 L2).
- `Path`는 Part 1 §2 「처음 쓰면 한 문장」 목록에 있어, 노트북 1절 결과 읽기와 본문 b4에서 뜻을 풀고 쓰는 자리를 5절 이후로 두었습니다.
- **서비스 요청 0번**입니다(모델·임베딩 없음, API 키 없이 실행). Ch 9 02절과 같은 방식입니다. 새 커널로 두 번 실행해 18개 코드 셀 출력이 모두 같았습니다(교재 출력은 마지막 실행).

### 문장

- 70자 초과 9문장을 둘로 나누고, 영문·코드 이름으로 시작한 13문장에 종류 이름을 붙였습니다(「라이브러리 pypdf의」, 「속성 `name`은」, 「칸 `doc_id`는」, 「출력 `1쪽 본문 글자 수: 45`와」).
- 개선 전 `<dl class="term">` 정의 네 개는 한 단락으로 묶여 12문장이 되었습니다. Ch 9 01절처럼 **용어 표**(`<table>`)로 바꿨습니다(표는 G6 대상이 아니고, 뜻·일상 예·이 절에서 보이는 모습 세 칸을 나란히 둘 수 있습니다).
- 제작 상황 문장(문서 100건 미확보, `[[미정]]`)은 본문에서 뺐습니다.

### 그림

- 설계표 `qa/upgrade/01-figures.md`. Mermaid 4장 + 삽화 1장.
  - `01-1-형식과-기록`(핵심 개념·「오늘 볼 그림」, viewBox 542.5): 원본 여섯 형식 → 형식마다 다른 읽기 → 본문 글과 다섯 칸 기록 → 회색 문서 청크·색인.
  - `01-2-두-읽기`(실행 예제, 427.9): 같은 2쪽 → 두 읽기 → 905자·1396자 → 「세 칸 기록은 둘이 같음」.
  - `01-3-다섯-칸-기록`(실행 예제, 510.0): 경로에서 세 칸 + 사람이 넣는 두 칸 → 다섯 칸 → `make_source_mark()` → `[E01 p.2]`.
  - `01-4-쪽-번호`(일부러 실패해 보기, 718.6): Before 빨강 / After 노랑 / 「두 기록 모두 오류를 내지 않음」 회색.
  - 색: 파일·기록 초록, 코드 단계 파랑, 출력 값 노랑, Before 결함 결과 빨강 한 상자, 실행 안 한 단계 회색. **보라 0장**(모델을 부르지 않음). Ch 9 §10 색 선례를 따랐습니다.
  - 네 장 모두 PNG를 직접 확인했습니다. viewBox 폭은 모두 868 이하입니다.
- 삽화 `01-5-서류와-봉투`: 1차 job `b14b33cb-…` 탈락(봉투가 네 개만 보이고 빈 줄이 세로), 2차 job `97390942-…` 채택. `nano_banana_pro`, 16:9, 2k, 4크레딧(잔액 2808). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0을 확인했습니다(규격 §5-4). 자세한 기록은 `figures/01-5-서류와-봉투.prompt.md`.
- 옛 도식 `figures/01-문서-계약.svg`·`.excalidraw`·`.caption.md`는 지우지 않고 `qa/upgrade/before/figures/`에 사본을 두었습니다.

## 4. 빌드 도구 변경 (챕터 파일만)

`chapter.json`이 없는 챕터라 자체 `_build.py`를 씁니다. Ch 9 `_build.py`와 같은 방법으로 아래를 더했습니다(공용 `textbook/_template`·`_notebook`은 고치지 않았습니다).

- `inline_illustration(name, spec)` — 세 칸 `{{img:이름|alt|캡션}}`을 `<figure class="illustration">`로. 두 칸 `{{img:이름|캡션}}`은 개선 전과 같은 `<img alt>` 그대로(하위 호환).
- `inline_mermaid(spec)` — `{{mermaid:이름|alt|캡션}}`을 `<figure class="mmd">`로. 출력은 `textbook/_template/builder.py`의 `_inline_mermaid`와 같고, 이 챕터 CSS의 `figure svg{min-width:760px}` 때문에 인라인 style에 `min-width:0` 하나만 더합니다(Ch 9와 같은 차이).
- 치환 뒤 `\{\{[a-z]+:` 모양이 남으면 `ValueError`로 빌드를 멈춥니다.
- `{{svg:}}`·`{{code:}}`·`{{output:}}`·`{{notebook:}}`은 그대로입니다. 02~08 개선 전 `_src`는 아직 `{{svg:}}`를 씁니다.
- **확인 방법과 결과**: (a) 고치기 전 디스크 HTML 9개 해시를 `/tmp/ch10-01/hash/disk-before.txt`에 남기고, (b) `_build.py`만 고친 뒤 다시 빌드해 9개 해시가 **모두 같음**을 확인했습니다, (c) 01절 본문을 새로 쓴 뒤 다시 빌드해 **01 HTML만 달라지고** 02~08·index는 같음을 확인했습니다, (d) 빌드 HTML 9개에 `{{`가 0건입니다.
- `run_section.sh`는 `chapter.json`이 없으면 verify를 건너뜁니다. `verify.py --chapter`를 따로 실행했습니다.

## 5. 산출 파일과 실습 폴더

- 01절은 `runs/`를 **읽지도 쓰지도 않습니다**. `labs/part3/ch10-document-processing/runs/` 전체 해시가 작업 전후 같습니다. Ch 9 `runs/continuity-ch09-search.jsonl`(`294713765a…`)도 건드리지 않았습니다.
- 실습 폴더 테스트: 작업 전 **38 passed**, 작업 후 **38 passed**(`document_processing.py`·`tests/`·`experiment.py` 고치지 않음).
- **학생 묶음**: 01 노트북이 새로 읽는 입력은 `labs/data/rag-corpus/pdf/*/`(21건)과 `labs/part3/ch10-document-processing/fixtures/`(5건)입니다. 둘 다 이미 `textbook/_notebook/build_bundle.py`의 `data`와 `FIXTURES` 목록에 있어 **허용 목록을 고치지 않았습니다**. `textbook/downloads/part3-practice.zip`을 `/tmp`에 풀어 경로 셀을 세 자리(묶음 맨 위·실습 폴더 맨 위·`notebooks`)에서 돌려 모두 같은 개수를 얻었습니다.
  - 이 확인에서 **후보 경로 실수를 잡았습니다.** 처음에는 `[".", "../..", "../../.."]`로 썼는데 `notebooks` 폴더에서는 프로젝트 맨 위에 닿지 않았습니다. `[".", "../../..", "../../../.."]`로 고쳐 다시 실행했습니다.
- `textbook/part3/qa/check_continuity.py`는 노트북 보존·변경 검사를 지나 **154행 zip 신선도**에서 멈춥니다(`part2-practice.zip`). `textbook/qa/check_course_continuity.py`는 **212행 zip 신선도**에서 멈춥니다(`part1-practice.zip`). 둘 다 Ch 9 마감 때와 같은 자리이고 전체 마감 몫입니다. 01 노트북은 `notebook-before-invariants.json`의 「바뀐 노트북」으로 들어가 새 커널 증명으로 통과합니다. `finalize_continuity_evidence.py`의 실행 입력 목록에는 들어가지 않습니다(묶음 연기 실행은 이 챕터 08절 노트북만 씁니다).
- 절 수는 8개 그대로라 `textbook/part3/_build_index.py`(ch10 칸 8)와 `qa/visual-results.json` 행 수는 고치지 않았습니다.

## 6. 옛 생성기

- 이 챕터에는 옛 **노트북** 생성기(`make_*.py`·`_make_notebooks.py`)가 없습니다(`find`로 확인).
- 옛 **도식** 생성기 `figures/_gen_figures.py`는 첫머리에 설명 주석과 `raise SystemExit(...)`을 넣어 실행을 막았습니다(규격 §8, PLAYBOOK §2-1). 삭제하지 않았고, 챕터 마감 때 `qa/upgrade/before/generators/`로 옮깁니다. 이 파일은 `textbook/part3/qa/continuity-evidence/before-manifest.json`에 등록돼 있지만, 두 검사 스크립트가 해시를 보는 항목은 `labs/**/runs/**`뿐이라 검사에 걸리지 않습니다(두 스크립트를 실제로 돌려 확인).
- 개선 전 QA 스크립트(`qa/check_content.py`·`qa/check_visual.cjs`)는 개선 전 본문·도식 기준이라 이번에 실행하지 않았습니다. 챕터 마감 때 확인합니다.

## 7. 검토자가 볼 곳

1. `qa/upgrade/review-pack/01-문서와-메타데이터.md` — 본문·노트북 셀과 출력·그림 원본이 한 파일에 있습니다.
2. `figures/01-*.png` 네 장과 `01-5-서류와-봉투.png` — 그림 요소가 본문 「도식 읽기」·「그림 읽기」와 1:1로 맞는지.
3. 이어짐 — Ch 9 `load_pdf_pages()`·`make_source_mark()`·E01·`[E01 p.2]`를 같은 코드·같은 값으로 쓰는지, Ch 9가 「이번에 실행하지 않았다」고 적은 표·스캔본·HWP를 02~04절로 넘기는지.

## 8. 남은 것

- **강사 확인 대상**: 노트북 준비물의 「강의와 실습 범위」 문장(2~6절 강의, 7~9절 함께 실행)은 작업자가 정했습니다. meta 시수는 개선 전과 같은 강의 1h·실습 2h입니다(여덟 절 합 = 챕터 24h, 규격 §7-2).
- **삽화**: 봉투 앞면 빈 줄이 네 줄로 그려져 다섯 칸과 수가 맞지 않습니다. 캡션과 그림 읽기에서 줄 수를 세지 않고 「같은 자리」만 짚었습니다. 다시 만들 때 줄 수를 맞춥니다.
- **02절 작업자에게**: `qa/upgrade/handoff.md` §01 → §02.
- 정리 대상(삭제하지 않고 목록만, 삭제 승인 필요): 옛 도식 `figures/01-문서-계약.svg`·`.excalidraw`·`.caption.md`, `figures/_gen_figures.py`(마감 때 `before/generators/`로), `qa/upgrade/gates-wip-01.json`, `.cache/vm/shot/`(검수용 화면 캡처 두 장), 기기 `/tmp/ch10-01`.

## 검토 반영 (별도 세션 검토 1차, 2026-09-18 챕터 마감 세션)

검토 보고서: `review-round1-A.md`(§01~05)·`review-round1-B.md`(§06~09), 각 끝 「반영 결과」. 이 절은 **다시 실행하지 않았습니다**(설명·본문·그림만 바뀜, 규격 §3). 노트북 `code_sha256`·`outputs_sha256`·`executed_at`가 반영 전후 같습니다.

- **[중] 01-1** b2 「PDF 21건 가운데 18건은 글자를 뽑을 수 있고」 → 「스캔본 폴더 3건은 글자 층이 없고, 남은 18건 가운데 `H05`도 세 쪽 모두 0자여서 글을 얻은 문서는 17건」. b10 말뭉치 설명서 항목도 「디지털 PDF 18건(글을 얻은 문서 17건)」으로. 08절 기록(「글이 있는 문서 수: 17」)과 맞췄습니다.
- **[중] C-2** b5·노트북 [0] 준비물 「인터넷 서비스에 요청을 한 번도 보내지 않습니다」 → 「모델과 임베딩에는 요청을 한 번도 보내지 않습니다. 첫 셀의 패키지 설치만 인터넷을 씁니다.」(05절 기준 문장).
- **[중] C-3** b3 「긴 글을 검색 단위로 나눈 조각을 가리키며」 → 「검색 단위로 자른 문서의 한 부분을 가리키며」. 「조각」은 Ch 5 토큰 뜻 전용입니다(규격 §4).
- **[하] 01-2** 노트북 [4] 「이 절에서 5절부터 `Path`를 씁니다」 → 「2절에서 확장자를 볼 때 처음 쓰고, 5절에서 세 속성을 함께 씁니다」. §3의 기록도 같은 사실로 봅니다.
- **[하] C-4** b8 「표의 행과 열이 남는지」 → 「표의 행과 칸이 남는지」(03절이 정한 말).
- **[하] C-7** 위 §2의 검사 문장 기록을 296 → 306으로 바로잡았습니다(게이트 결과 값). handoff §01 → §02도 같이 고쳤습니다. `sorted(목록)`은 이 절이 가르친 것이라 04~07 diagnosis·handoff의 「안 쓴 것」 목록에서 뺐습니다.
- 검토 A Q1(강의·실습 범위 문장, 다섯 칸 계약)은 권고대로 **유지**했습니다. 삽화 01-5 봉투 줄 수는 권고대로 캡션·그림 읽기로 처리한 상태를 유지합니다.
