# Ch 10 검증 기록

확인일: 2026-09-08. 대상: 강의 8h·실습 16h, HTML 8절과 목차, 복습 32문항, 도식 8개, 실행 예제 8개.

| 항목 | 결과 | 근거 |
|---|---|---|
| Python 실행 환경 | 3.12.13 · uv.lock 고정 | `labs/part3/ch10-document-processing/pyproject.toml`, `uv.lock` |
| 회귀 테스트 | 38 passed · 0 failed | `labs/part3/ch10-document-processing/tests/VERIFICATION.md` |
| 린트·문법 | Ruff 전체 통과 · compileall 통과 | 실습 담당자의 최종 실행 결과 |
| 정적 타입 검사 | 미실행 | mypy·pyright·ty 실행 파일 없음; 타입힌트는 포함 |
| 절 구성·분량·링크 | 8/8 통과 | `content-results.json` |
| 코드·출력 원본 일치 | 8/8 통과 | 빌드 시 실행 소스 함수·저장 출력 직접 삽입 후 대조 |
| 화면 4축 | PC 1280px / 모바일 390px, 18/18 통과 | `visual-results.json` |
| 도식 | SVG·Excalidraw 내용 일치, 7개 이하 상자, 글자 ≥14px, 대비 ≥4.63:1 | `../figures/verification.md` |
| 한국어 검토 | 일반 슬롭 정리·로컬 맞춤법·윤문 완료, 다른 모델 Phase 6 accept | `language/`, `final-reading.md` |

화면 검사는 본문 16px 이상, 캡션·코드 14px 이상, 본문 대비 4.5:1 이상(큰 글자 3:1), 숨김 처리로 잘린 내용 0건, 문서 가로 넘침 0건, `.page` 밖 본문 텍스트 0건을 확인했습니다. 도식은 원래 글자 크기를 유지하고 내부 영역만 가로로 이동할 수 있습니다.

언어 자동 게이트는 WARN입니다. 수정량이 작은 점과 근거가 부족한 동향 문장에서 `2026년`을 삭제한 점이 경고 원인입니다. 연도 삭제는 독립 정독에서 요청한 근거 범위 보정으로 기록했고, 나머지 수치·조건·코드·출처는 보호 불변식과 정독으로 대조했습니다. 외부 맞춤법 서비스를 포함한 3단 체인 전체 통과를 뜻하지 않습니다. 최종 보정 후 다시 빌드하여 본문 8/8·화면 18/18을 확인했습니다.

## 실행 범위

말뭉치는 고유 디지털 PDF 18건이며, 스캔 PDF 3건은 별도 실패 사례 자료입니다. 재귀·토큰·구조 청킹에서 각각 137·211·136개의 청크를 만들었습니다. 오프라인 특징 벡터를 사용한 6개 설정의 두 번째 캐시 요청은 모두 미스 0건입니다. 질의는 기존 질의셋의 Q001·Q037·Q088 세 개이며, 전체 검색 품질을 대표하지 않습니다. 로그의 `metrics`는 Ch 11에서 채울 빈 딕셔너리입니다.

## 확인 필요 항목

- 실제 임베딩 API: `OPENAI_API_KEY`가 없어 미실행했습니다. 저장된 6개 결과의 백엔드는 `educational-feature-hash`입니다. 실제 small·large 모델 비교나 품질 측정 결과가 아닙니다. API 호출 비용은 0달러이며 출력의 금액은 호출 전 추정값입니다.
- 문서 100건: 현재 18건 기준선만 실행했습니다. 파일 내용 해시로 중복을 제외하며, 100건을 요구하면 사전 검사가 실패합니다. 도메인 문서 추가 확보가 필요합니다.
- OCR·상용 파서: OCR 엔진과 Upstage·LlamaParse 호출은 미실행입니다. 로컬 PDF 비교는 pypdf와 pdfplumber로 실행했습니다.
- HWP·HWPX: OLE 컨테이너는 전용 파서 필요로 거부합니다. HWPX 예제는 최소 ZIP/XML 표식이며 한컴오피스 호환 문서가 아닙니다. 실제 업무 문서·표·각주·병합 셀·변환 호환성은 검증하지 않았습니다.
- 외부 맞춤법: `korean-spell-check`의 “상업적 대량 처리” 금지와 서비스의 비상업용 제한에 따라 전송하지 않았습니다. 로컬 정독에서 맞춤법을 함께 검토합니다. 지침: `/Users/mhso/.codex/plugins/cache/moai-cowork/moai-writer/1.4.1/skills/korean-spell-check/SKILL.md`.
- Excalidraw: MCP 미리보기 도구가 없어 `create_view`는 미실행입니다. 공통 생성기에서 SVG와 Excalidraw JSON을 함께 만들고 브라우저로 확인했습니다. 여덟 개념 모두 관계를 정확히 표시하는 도식이 적합하여 별도 생성 삽화는 사용하지 않았습니다.

## 실제 패키지 버전

`pypdf 6.18.0`, `pdfplumber 0.11.10`, `python-docx 1.2.0`, `beautifulsoup4 4.15.0`, `langchain-core 1.6.2`, `langchain-text-splitters 1.1.2`, `openai 2.54.0`, `tiktoken 0.14.0`, `pytest 8.4.2`, `ruff 0.16.6`입니다. 프로젝트의 LangChain 1.4 기준과 개별 배포 패키지의 버전 번호는 구분합니다. 이 챕터는 `langchain` 메인 패키지 대신 `langchain-core`의 Document와 별도 스플리터 패키지를 사용합니다.

## 품질 개선 (2026-09-18~, 규격 `../../QUALITY-UPGRADE.md`)

위 기록은 개선 전(2026-09-08) 상태입니다. 품질 개선은 절 단위로 진행하며 절마다 아래 검사를 다시 받습니다. 절별 기록은 `upgrade/NN-diagnosis.md`, 표는 `../집필점검표.md`입니다.

| 절 | 확인일 | 게이트 G1~G7 | 새 커널 실행 | verify.py --chapter | visual.cjs | 실습 폴더 테스트 | 서비스 요청 |
|---|---|---|---|---|---|---|---|
| 01 문서와 메타데이터 | 2026-09-18 | 37 → 0 (PASS) | PASS 18 cells, `fresh_kernel: true`, Python 3.12.13 | `PASS 8 sections / 77 code cells (max 24 lines)` | 1280px·390px 2건 PASS | 38 passed(작업 전후 같음) | 0번(모델·임베딩 없음, 비용 0달러) |
| 02 PDF와 표·OCR | 2026-09-18 | 49 → 0 (PASS) | PASS 18 cells, `fresh_kernel: true`, Python 3.12.13, 두 번 실행 `outputs_sha256` 같음 | `PASS 8 sections / 87 code cells (max 24 lines)` | 1280px·390px 2건 PASS | 38 passed(작업 전후 같음) | 0번(모델·임베딩 없음, 비용 0달러) |
| 03 DOCX·HTML·CSV | 2026-09-18 | 37 → 0 (PASS) | PASS 23 cells, `fresh_kernel: true`, Python 3.12.13, 두 번 이어 실행 `outputs_sha256` 같음 | `PASS 8 sections / 102 code cells (max 24 lines)` | 1280px·390px 2건 PASS | 38 passed(작업 전후 같음) | 0번(모델·임베딩 없음, 비용 0달러) |
| 04 HWP와 HWPX | 2026-09-18 | 46 → 0 (PASS) | PASS 24 cells, `fresh_kernel: true`, Python 3.12.13, 두 번 이어 실행 출력 값 같음(`%pip` 셀 출력 덩이만 달라 `outputs_sha256`은 다름) | `PASS 8 sections / 118 code cells (max 24 lines)` | 1280px·390px 2건 PASS | 38 passed(작업 전후 같음) | 0번(모델·임베딩 없음, 비용 0달러) |
| 05 문자·재귀·토큰 청킹 | 2026-09-18 | 39 → 0 (PASS) | PASS 24 cells, `fresh_kernel: true`, Python 3.12.13, 두 번 이어 실행 `outputs_sha256` 같음(`18851bbd…`) | `PASS 8 sections / 134 code cells (max 24 lines)` | 1280px·390px 2건 PASS | 38 passed(작업 전후 같음) | 0번(모델·임베딩 없음, 비용 0달러) |
| 06 구조와 시맨틱 청킹 | 2026-09-18 | 42 → 0 (PASS) | PASS 26 cells, `fresh_kernel: true`, Python 3.12.13, 두 번 이어 실행 출력 값 같음(폐기 예고 경고 앞 임시 경로만 달라 `outputs_sha256`은 다름) | `PASS 8 sections / 152 code cells (max 24 lines)` | 1280px·390px 2건 PASS | 38 passed(작업 전후 같음) | 임베딩 2번(`text-embedding-3-small`, 비용 어림 0.001달러 미만) |
| 07 한국어 임베딩과 캐시 | 2026-09-18 | 51 → 0 (PASS) | PASS 23 cells, `fresh_kernel: true`, Python 3.12.13, 세 번 이어 실행 출력 값 같음(`%pip` 셀 출력 덩이만 달라 `outputs_sha256`은 `ce6ec276…`·`118b6980…`로 갈림) | `PASS 8 sections / 166 code cells (max 24 lines)` | 1280px·390px 2건 PASS | 38 passed(작업 전후 같음) | 임베딩 6번(`text-embedding-3-small`, 비용 어림 `5e-05`달러) |
| 08 인덱싱 비교 실험 | 2026-09-18 | 62 → 0 (PASS) | PASS 29 cells, `fresh_kernel: true`, Python 3.12.13, 네 번 이어 실행해 문서 청크 수와 1·2위 같음(실행 이름과 3~5위 순서만 달라 `outputs_sha256`은 실행마다 다름) | `PASS 8 sections / 185 code cells (max 14 lines)` | 1280px·390px 2건 PASS | 38 passed(작업 전후 같음) | 임베딩 13번(`text-embedding-3-small` 기본 설정, 비용 어림 `0.0078194`달러) |
| 09 문서 처리 실습(챕터 끝) | 2026-09-18 | 새 절 · 0 (PASS) | PASS 30 cells, `fresh_kernel: true`, Python 3.12.13, 새 커널로 두 번 실행해 값 같음(실행 2 셋째 줄 점수만 `0.31`·`0.3`로 갈림, 교재 출력은 두 번째 실행 2026-09-18T06:57:44Z · `outputs_sha256` `0c1619ae…`) | `PASS 9 sections / 215 code cells (max 14 lines)` | 1280px·390px 2건 PASS | 38 passed(작업 전후 같음) | 임베딩 4번(`text-embedding-3-small` 기본 설정, 비용 어림 `3.62e-05`달러) |

- 01절은 `runs/`를 읽지도 쓰지도 않았습니다. `labs/part3/ch10-document-processing/runs/` 전체 해시가 작업 전후 같습니다.
- 빌드 도구: 챕터 `_build.py`에 `{{mermaid:}}`와 세 칸 `{{img:}}`를 더했고, 02~08절과 목차 HTML 해시는 바뀌지 않았습니다. 빌드한 HTML 9개에 `{{` 잔존 0건입니다.
- 학생 묶음: 01절이 읽는 `labs/data/rag-corpus/pdf/*/`와 `fixtures/`는 이미 `textbook/_notebook/build_bundle.py`의 허용 목록에 있습니다. `part3-practice.zip`을 풀어 세 자리(묶음 맨 위·실습 폴더 맨 위·`notebooks`)에서 경로 셀을 돌려 확인했습니다.
- 그림: Mermaid 4장(`figures/01-1`~`01-4`, viewBox 폭 428~719)과 삽화 1장(`figures/01-5-서류와-봉투.png`, 채택 job 결과와 픽셀 차이 0). 옛 도식 `01-문서-계약.*`은 `upgrade/before/figures/`에 사본을 두었습니다.
- 옛 도식 생성기 `figures/_gen_figures.py`는 실행을 막아 두었습니다(첫머리 `raise SystemExit`). 개선한 절의 도식은 `figures/NN-k-이름.mmd`를 `render_mermaid.py`로 렌더해 만듭니다.
- 개선 전 QA 스크립트 `qa/check_content.py`·`qa/check_visual.cjs`와 위 표의 개선 전 수치(본문 8/8·화면 18/18)는 개선 전 기준이라 01절 작업에서 다시 실행하지 않았습니다. 챕터 마감 때 확인합니다.
- 02절도 `runs/`를 읽지도 쓰지도 않았습니다. 같은 폴더 40개 파일 해시가 작업 전후 같습니다.
- 02절 빌드 도구 변경은 없습니다. 01절이 더한 `{{mermaid:}}`·세 칸 `{{img:}}`를 그대로 썼고, 개선 전 `{{svg:02-표-구조}}`를 `{{mermaid:}}` 네 개로 바꿨습니다. 02절 HTML만 달라졌습니다(`666e2acd…` → `dcfe8da182…`).
- 02절 학생 묶음: 노트북이 읽는 `pdf/easy/E01.pdf`와 `pdf/scanned/S01-E01-scan.pdf`는 `build_bundle.py` 63행의 `pdf/*/*.pdf`에 이미 들어 있습니다. 묶음에서 두 파일을 풀어 세 자리에서 경로 셀을 돌려 확인했고 허용 목록은 고치지 않았습니다.
- 02절 그림: Mermaid 4장(`figures/02-1`~`02-4`, viewBox 폭 466~818)과 삽화 1장(`figures/02-5-칸막이-상자.png`, 1차 채택, 채택 job 결과와 픽셀 차이 0). 옛 도식 `02-표-구조.*`은 `upgrade/before/figures/`에 사본을 두었습니다.
- 03절도 `runs/`를 읽지도 쓰지도 않았습니다. 같은 폴더 40개 파일 해시가 작업 전후 같습니다(`455ab5b1…`).
- 03절 빌드 도구 변경은 없습니다. 개선 전 `{{svg:03-형식별-단위}}`를 `{{mermaid:}}` 네 개와 `{{img:}}` 하나로 바꿨습니다. 03절 HTML만 달라졌습니다(`36664a7d…` → `74d29499…`).
- 03절 학생 묶음: 노트북이 읽는 `fixtures/sample.docx`·`sample.html`·`sample.csv`는 `build_bundle.py` 31행 `FIXTURES`에 이미 들어 있습니다. 묶음에서 견본을 풀어 세 자리에서 경로 셀을 돌려 확인했고 허용 목록은 고치지 않았습니다.
- 03절 그림: Mermaid 4장(`figures/03-1`~`03-4`, viewBox 폭 513~846)과 삽화 1장(`figures/03-5-공책과-장부.png`, 1차 채택, 채택 job 결과와 픽셀 차이 0). 옛 도식 `03-형식별-단위.*`은 `upgrade/before/figures/`에 사본을 두었습니다.
- 03절은 쪽 번호가 없는 형식의 출처 기록을 네 칸으로 정했습니다(CSV만 `row` 칸 하나 더). 출처 표시는 `make_unit_mark()`가 만들고, 01·02절 `make_source_mark()`는 `page` 칸을 읽어 이 절 기록에는 쓰지 않았습니다.
- 04절도 `runs/`를 읽지도 쓰지도 않았습니다. 같은 폴더 40개 파일 해시가 작업 전후 같습니다(`455ab5b1…`).
- 04절 빌드 도구 변경은 없습니다. 개선 전 `{{svg:04-hwp-hwpx}}`를 `{{mermaid:}}` 네 개와 `{{img:}}` 하나로 바꿨습니다. 04절 HTML만 달라졌습니다(`da5c8dbb…` → `0aef680f…`).
- 04절 학생 묶음: 노트북이 읽는 `fixtures/legacy-signature.hwp`·`minimal-marker.hwpx`는 `build_bundle.py` 31행 `FIXTURES`에 이미 들어 있습니다. 묶음에서 견본을 풀어 세 자리에서 경로 셀을 돌려 확인했고 허용 목록은 고치지 않았습니다.
- 04절 그림: Mermaid 4장(`figures/04-1`~`04-4`, viewBox 폭 511~810)과 삽화 1장(`figures/04-5-잠긴-상자와-주머니.png`, 1차 채택, 채택 job 결과와 픽셀 차이 0). 옛 도식 `04-hwp-hwpx.*`은 `upgrade/before/figures/`에 사본을 두었습니다.
- 04절은 쪽 번호가 없는 형식의 자리 칸을 HWPX에서 `section`으로 정했습니다(값 1부터, `parser`는 `zip-xml`). 03절 `make_unit_mark()`는 `row` 칸만 읽어 이 기록에서는 자리 칸이 표시에 나오지 않았고, 그 함수를 고치지 않고 `make_section_mark()`를 하나 더 만들었습니다.
- 04절은 미교육 문법 세 가지(바이트 읽기·압축 묶음·XML 요소 나무)를 처음 쓰는 자리에서 뜻 → 일상 예 → 코드로 풀었습니다. 형식 표시 하나로 형식을 단정하지 않아 갈래 이름을 `hwp-후보`로 두었고, After도 HWP 본문을 읽은 것은 아니라는 사실을 본문·그림에 적었습니다.
- 05절도 `runs/`를 읽지도 쓰지도 않았습니다. 같은 폴더 40개 파일 해시가 작업 전후 같습니다(`1cc170e8…`).
- 05절 빌드 도구 변경은 없습니다. 개선 전 `{{svg:05-청크-경계}}`를 `{{mermaid:}}` 네 개와 `{{img:}}` 하나로 바꿨습니다. 05절 HTML만 달라졌습니다(`77490c4a…` → `f1981402…`).
- 05절 학생 묶음: 노트북이 읽는 입력은 `labs/data/rag-corpus/pdf/easy/E01.pdf` 하나입니다(01·02절과 같은 파일). `build_bundle.py` 63행 `pdf/*/*.pdf`에 이미 들어 있어 허용 목록을 고치지 않았고, `part3-practice.zip`을 풀어 세 자리에서 경로 셀을 돌려 확인했습니다(묶음 사본과 원본 해시 `cd0ff7d7…` 같음).
- 05절 그림: Mermaid 4장(`figures/05-1`~`05-4`, viewBox 폭 700~825, 하나는 `xychart-beta` 주황 막대·초록 선)과 삽화 1장(`figures/05-5-세-줄로-자른-띠.png`, 2차 채택, 채택 job 결과와 픽셀 차이 0). 옛 도식 `05-청크-경계.*`은 `upgrade/before/figures/`에 사본을 두었습니다.
- 05절은 나눌 글을 01·02절이 읽은 `E01.pdf` 2쪽(905자)으로 바꿨고, `split_documents()`로 문서 청크 여섯 개에 01절 다섯 칸 기록이 따라가는 것을 출력으로 보였습니다(출처 표시 여섯 개 모두 `[E01 p.2]`).
- 05절 조각 수 한도 150은 사람이 정한 값입니다. 탐색 실행에서 문서 청크 조각 수가 92~190인 것을 본 뒤 근거 세 개에 450조각을 주는 계산과 맞춰 골랐고, 그 과정을 본문 b7 첫 항목에 적었습니다(규격 §3).
- 05절은 어느 나누기가 검색에 더 나은지 판정하지 않았습니다. 검색을 돌리지 않았고, 「끊을 자리 순서만 바꾸니 이 글에서는 문자 방식과 결과가 같았다」까지만 적었습니다.
- 06절도 `runs/`를 읽지도 쓰지도 않았습니다. 같은 폴더 40개 파일 해시가 작업 전후 같습니다(`1cc170e8…`).
- 06절 빌드 도구 변경은 없습니다. 개선 전 `{{svg:06-구조-의미-청킹}}`를 `{{mermaid:}}` 네 개와 `{{img:}}` 하나로 바꿨습니다. 06절 HTML만 달라졌습니다(`be2df150…` → `f497c06a…`).
- 06절 학생 묶음: 노트북이 읽는 입력은 `labs/data/rag-corpus/pdf/easy/E01.pdf` 하나입니다(01·02·05절과 같은 파일). 허용 목록을 고치지 않았고, `part3-practice.zip`을 풀어 세 자리에서 경로 셀을 돌려 확인했습니다(묶음 사본과 원본 해시 `cd0ff7d7…` 같음).
- 06절 그림: Mermaid 4장(`figures/06-1`~`06-4`, viewBox 폭 531~765, 하나는 `sequenceDiagram` 실선 요청·점선 응답)과 삽화 1장(`figures/06-5-문패와-무늬.png`, 1차 채택, 채택 job 결과와 픽셀 차이 0). 옛 도식 `06-구조-의미-청킹.*`은 `upgrade/before/figures/`에 사본을 두었습니다.
- 06절은 **이 챕터에서 처음으로 서비스에 요청을 보냅니다**(임베딩 `text-embedding-3-small` 2번). Ch 9 03절과 같은 이름·같은 기본 설정을 쓰고 개선 전 `dimensions=256`은 뺐습니다. 요청 전에 조각 수 2607과 비용 5.21e-05달러를 어림해 출력으로 보였습니다(규격 §3).
- 06절 제목 칸 이름은 `heading`입니다. 04절 `section`은 자리 칸이라 뜻이 달라 같은 이름을 쓰지 않았고(handoff §05 → §06 결정), 근거를 본문 b4·b7에 적었습니다. 출처 표시는 쪽이 있는 형식이라 01절 `make_source_mark()`로 `[E01 p.2]`입니다.
- 06절은 폐기 예고 경고를 감추지 않았습니다. 개선 전 `warnings.filterwarnings(...)` 셀을 빼고, 경고가 무엇을 알리는지 import 셀 뒤 설명에 한 문장으로 적었습니다.
- 06절은 어느 방식·기준값이 검색에 더 나은지 판정하지 않았습니다. 「문서 청크 수는 3개·2개·10개로 달랐지만 지킬 말 두 개는 세 결과 모두 한 문서 청크에 있었다」까지만 적고, 세 결과 공통 값은 회색 상자로 뺐습니다.
- 07절도 `runs/`를 읽지도 쓰지도 않았습니다. 같은 폴더 40개 파일 해시가 작업 전후 같습니다(`455ab5b1…`). 실습 폴더 모듈 두 개(`37ca2cc9…`·`342e85b0…`)와 `fixtures/`(`2681052c…`)도 그대로입니다.
- 07절 빌드 도구 변경은 없습니다. 개선 전 `{{svg:07-임베딩-캐시}}`를 `{{mermaid:}}` 네 개와 `{{img:}}` 하나로 바꿨습니다. 07절 HTML만 달라졌습니다(`d954618139…` → `f6d93f2601…`).
- 07절 학생 묶음: 노트북이 읽는 입력은 `labs/data/rag-corpus/pdf/easy/E01.pdf` 하나입니다(01·02·05·06절과 같은 파일). 벡터를 저장하는 폴더는 `tempfile.mkdtemp()`로 만드는 시스템 임시 폴더라 묶음 대상이 아닙니다. `part3-practice.zip`을 풀어 세 자리에서 경로 셀을 돌려 확인했고(묶음 사본과 원본 해시 `cd0ff7d7…`) 허용 목록은 고치지 않았습니다.
- 07절 그림: Mermaid 4장(`figures/07-1`~`07-4`, viewBox 폭 534~819, 하나는 `sequenceDiagram` 실선 요청·점선 응답)과 삽화 1장(`figures/07-5-서랍과-표찰.png`, 1차 채택, 채택 job 결과와 픽셀 차이 0). 옛 도식 `07-임베딩-캐시.*`은 `upgrade/before/figures/`에 사본을 두었습니다.
- 07절 임베딩 요청은 6번입니다. 요청 전에 조각 수 2498과 비용 `5e-05`달러를 어림해 출력하고 요금 확인일(2026-09-17)을 준비물·본문 b5에 적었습니다. 임베딩 값은 실행마다 소수 아래 자리가 달라질 수 있어 숫자 개수와 자료형만 출력했고 모델 값에 `assert`를 쓰지 않았습니다.
- 07절 `dimensions` 결정: 기본값(1536)과 256을 견주고, Ch 9 03절·06절 색인이 기본값이라는 사실을 본문 b4·b7과 노트북 4절에 적었습니다. **08절 색인에는 07의 256차원 벡터를 이어 쓰지 않습니다**(개수가 다른 벡터를 한 색인에 섞으면 검색 점수를 계산할 수 없음).
- 07절은 파일 수로 요청 수를 말하지 않았습니다. 노트북 7절 출력은 저장 파일 수와 두 목록이 같다는 것까지만 보이고, 「저장값이 없는 글만 모아 한 번 부른다」는 설치판 소스에서 얻은 근거로 구분해 적었습니다.
- 07절 작업에서 이 표의 06절 행이 빠져 있던 것을 함께 채웠습니다(06절 작업에서는 아래 메모만 더했습니다).
- 08절은 이 챕터에서 **유일하게 `runs/`를 씁니다**. 정본 `runs/continuity-ch10-indexing.jsonl`을 다시 썼고(`9e59586a…` → `58cc790c45df9bf9cfbdda21a4de267bd10a7749568f1306d9625657d5ebda45`, 여섯 줄) 실행별 사본을 `runs/continuity/`에 여섯 개씩 남겼습니다. 앞 사본은 지우지 않았고 폴더가 24개 → 48개, `runs/` 전체가 40개 → 64개가 되었습니다.
- 08절 기록 계약은 읽는 쪽 다섯 곳을 열어 확인했습니다(`evaluate.py` 176~250행, `check_continuity.py` 58~78·140~155행, `check_course_continuity.py` 94~112·172~198행, `run_continuity_bundle.py` 45~54행, `finalize_continuity_evidence.py` 15·37·44~58행). 최상위 칸 7개·`config` 칸 6개·`retrieved` 칸 5개·`chunk_id` 네 자리 채움·줄 수 6·검색 개수 5를 그대로 두었습니다. `chunk_method` 값은 `char`·`recursive`·`token`입니다.
- 08절 기록으로 `evaluate.py`의 `load_retrieval_records()`·`evaluate_retrieval_records()`를 직접 돌려 여섯 실행 모두 `recall_at_5 1.0`·`precision_at_5 0.2`·`ndcg_at_5 1.0`·`recall_at_logged_candidates 1.0`·`recall_at_50 None`을 얻었습니다(`finalize_continuity_evidence.py` 54~58행 조건).
- 08절 `config` 칸 `dimensions` 값이 256 → **1536**으로 바뀌었습니다. 07절이 「색인에 넣을 벡터는 기본 설정으로 만든다」고 정했고 Ch 9 03·06절 색인도 기본값입니다. 값은 노트북이 색인에서 직접 재서 적습니다. 이 칸을 읽는 쪽은 없습니다(`check_course_continuity.py` 219행은 Ch 12 기록을 봅니다). `inputs.corpus_scope`도 `"18 digital PDFs"` → `"디지털 PDF 18건"`으로 바꿨습니다.
- 08절 빌드 도구 변경은 없습니다. 개선 전 `{{svg:08-실험-격자}}`를 `{{mermaid:}}` 네 개와 `{{img:}}` 하나로 바꿨습니다. 08절 HTML만 달라졌습니다(`ba441182…` → `0273e394…`).
- 08절 학생 묶음: 새로 읽는 입력은 `labs/data/rag-corpus/manifest.json`·`pdf/*/*.pdf` 18건·`labs/part3/ch11-evaluation/data/evaluation-queries.jsonl`입니다. 앞 둘은 `build_bundle.py` 63·64행에, 평가셋은 `textbook/part3/public-files.json`에 이미 있어 허용 목록을 고치지 않았습니다. `part3-practice.zip`을 풀어 세 자리에서 경로 셀을 돌려 모두 찾았습니다(묶음 사본과 원본 해시 manifest `27541f41…`·평가셋 `9544b332…`).
- 08절 그림: Mermaid 4장(`figures/08-1`~`08-4`, viewBox 폭 536~800, 하나는 `xychart-beta` 주황 막대)과 삽화 1장(`figures/08-5-상자-세-개와-기록-용지.png`, 1차 채택, 채택 job 결과와 픽셀 차이 0). 옛 도식 `08-실험-격자.*`은 `upgrade/before/figures/`에 사본을 두었습니다. `visual.cjs`에서 `xychart` 마지막 가로축 라벨이 테두리를 1.5px 넘어 「토큰 100」으로 줄여 통과했습니다(1280px·390px 두 건 PASS).
- 08절 임베딩 요청은 13번입니다(색인 6번 + 검색 6번 + 값 바꿔 보기 1번). 요청 전에 조각 수 390970과 비용 `0.0078194`달러를 어림해 출력했습니다. 답을 쓰는 모델은 부르지 않았습니다.
- 08절은 새 커널로 네 번 실행했습니다(교재 출력은 2026-09-18T06:19:03Z). 문서 청크 수 여섯 개와 1위·2위 결과는 네 번 모두 같았고, 상위 세 번째부터 다섯 번째 문서의 순서가 한 실행에서 달라졌습니다. 점수 차가 소수 셋째 자리 수준이라 **1위와 2위까지만 결론에 썼습니다**. 점수 값은 본문·캡션·그림 라벨에 넣지 않았습니다.
- 08절은 임베딩 모델을 하나만 씁니다. 개선 전 두 모델 비교는 아직 안 가르친 것이라 빼고, 바꾸는 조건을 05절 세 나누기 방식과 겹침 두 값으로 옮겼습니다(강사 확인 대상, `qa/upgrade/08-diagnosis.md` §8).
- 08절 실습 폴더 테스트 `38 passed`(작업 전후 같음). `document_processing.py`(`37ca2cc9…`)·`experiment.py`(`342e85b0…`)·`tests/`·`fixtures/`는 고치지 않았습니다(수정 시각 2026-09-08 그대로).
- 09절(챕터 끝 실습)은 파일을 쓰지 않습니다. `runs/` 전체 64개 파일 해시와 정본 `58cc790c…`, 실습 폴더 모듈 두 개(`37ca2cc9…`·`342e85b0…`) 해시가 작업 전후 같습니다.
- 09절 주제는 형식이 다른 문서 세 개(`E01.pdf` 2쪽·`sample.docx`·`minimal-marker.hwpx`)를 한 색인에 모아 같은 질문으로 찾기입니다. 01·03·04절 읽기와 기록, 05절 재귀 방식 나누기, 08절 색인·검색을 조립 함수 `run_index()`로 이었고, 01·03·04절 출처 표시 함수 세 개를 고르는 `pick_mark()`를 새로 만들었습니다.
- 09절 실행 1(색인에 PDF 한 건, 문서 청크 6개)은 상위 다섯 줄이 모두 `[E01 p.2]`였고 1위 점수가 `0.33`입니다. 실행 2(세 형식 함께, 문서 청크 8개)는 1위가 `[sample docx]` 26자 점수 `0.63`이고 PDF 문서 청크 네 개가 한 칸씩 내려갔습니다. HWPX 문서 청크는 두 실행 모두 상위 다섯 줄에 없었습니다.
- 09절 임베딩 요청은 4번입니다(색인 2번 + 검색 2번). 요청 전에 조각 수 1810과 비용 `3.62e-05`달러를 어림해 출력했습니다. 답을 쓰는 모델은 이 절에서도 부르지 않았습니다.
- 09절 빌드 도구 변경은 `_build.py` `SECTIONS`에 09 제목 한 줄과 `render_index()` 메타의 「개념 8절」 → 「개념 8절 + 실습 1절」입니다. 08절 HTML은 다음 절 링크 한 줄과 b8 「다음 학습」 문단만 달라졌고(`0273e394…` → `98d3c32c…`), 01~07절 HTML 해시는 그대로입니다.
- 09절 학생 묶음: 읽는 입력 세 개는 모두 `build_bundle.py`의 `data`·`FIXTURES`에 이미 있어 허용 목록을 고치지 않았습니다. `part3-practice.zip`에 세 파일이 있는 것을 확인했고, `build_bundle.py`의 `check_public_file()`·`validate()`·`validate_parts()`를 09 노트북에 직접 돌려 통과했습니다. 묶음 자체는 전체 마감 때 다시 만듭니다(지금은 09 노트북이 들어 있지 않습니다).
- 09절 그림: Mermaid 3장(`figures/09-1`~`09-3`, viewBox 폭 504~750)과 삽화 1장(`figures/09-4-세-묶음과-한-상자.png`, 1차 채택, 채택 job 결과와 픽셀 차이 0). 실습 절이라 조립도·실행 1 순서·실행 1·2 비교 세 장입니다(규격 §7-2).
- 09절 절 수 반영: `_src/index.html` 절 표에 09행(30분 · 실습 16h 안)과 개선 전 08절 설명 문장을 고쳤고, `textbook/part3/_build_index.py` ch10 절 수 칸을 8 → 9로 올렸습니다(강의 8h·실습 16h는 그대로). Part 3 목차와 zip 재생성은 전체 마감 몫입니다.
- 09절 화면 검사: 공용 `visual.cjs`를 `/tmp` 사본으로 돌려 10페이지 × 2폭 **20/20 PASS**이고, 그 결과를 `textbook/_notebook/checks/ch10-document-processing/visual-results.json`(18행 → 20행)에 갱신했습니다. `textbook/part3/qa/finalize_continuity_evidence.py`의 `assert len(visual) == 88`은 92로 고쳤습니다(ch10 20행 반영 + Ch 9 실습 절 07 몫 16행, Ch 9 HTML을 다시 찍기 전에는 90이라 이 검사는 전체 마감 때 지나갑니다).
- 09절에서 챕터 안 QA 스크립트 두 개를 정리했습니다. `qa/check_visual.cjs`는 14px 허용 목록을 공용 `visual.cjs`와 같게 맞춰(`.nb-toolbar`·`.nb-prompt`·`button`·`.copy-status` 추가) 20/20 PASS가 되었고 `qa/visual-results.json`이 18행 → 20행이 되었습니다. `qa/check_content.py`는 b1~b11 열한 블록·`<details class="instructor">`·`{{code:}}`·`{{output:}}`을 요구하는 개선 전 전제라 `qa/upgrade/before/qa-scripts/`로 `mv -n`했습니다(삭제 아님, 참조하는 코드 0곳). 위 표 「절 구성·분량·링크 8/8」과 「화면 4축 18/18」 줄은 개선 전 수치입니다.
- 09절 뒤 과정 단계 검사는 앞과 같은 자리에서 멈춥니다. `textbook/part3/qa/check_continuity.py` 154행(`part2-practice.zip` 신선도), `textbook/qa/check_course_continuity.py` 212행(`part1-practice.zip` 신선도)입니다. `runs/`를 건드리지 않아 해시 허용 목록은 고치지 않았습니다.
