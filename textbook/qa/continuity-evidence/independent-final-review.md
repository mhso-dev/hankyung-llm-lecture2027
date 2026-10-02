# Ch1–Ch12 연결성 독립 최종 기술 검토

검토일은 2026-09-10입니다. 작성 담당자의 완료 보고나 기존 QA PASS를 판정 근거로 대신하지 않고, 현재 학생용 `_src`, 노트북, 데이터, 로그, 빌드 HTML, 배포 ZIP과 실행 증거를 직접 대조했습니다. 검토자는 학생용 파일을 수정하지 않았습니다.

## Verdict

**PASS** — Ch1부터 현재 마지막 Ch12까지의 연결 경로에서 남은 중요 기술 결함을 발견하지 못했습니다. 수정 전 독립 검토에서 확정한 F01~F13은 모두 현재 코드·설명·실행 결과·배포물에 반영됐습니다. Ch13과 Ch15는 아직 작성되지 않았으므로 Ch12가 넘길 항목과 평가 상태까지만 확인했으며, 후속 구현을 완료했다고 판정하지 않았습니다.

## Evidence

### 챕터 연결

| 연결 | 독립 판정 근거 |
| --- | --- |
| Ch1→Ch2→Ch3→Ch4 | Python 3.12·uv·챕터별 `.venv`와 실제 Git 도입 시점을 대조했습니다. Ch3의 임시 저장소를 Ch4가 이어받는다는 잘못된 설명은 제거됐고, Ch4는 별도 프로젝트와 배포 데이터를 사용합니다. Ch3 README의 `git-filter-repo` 버전 명령을 챕터 폴더에서 실행해 2.47.0을 확인했습니다. |
| Ch4→Ch5 | Ch4 05는 배포된 `article.html`을 파싱해 `article-text.json`을 직접 기록하고 다시 읽습니다. 압축 해제본에서 이 JSON을 먼저 삭제한 뒤 Ch4 05가 새로 만들고 Ch5 01이 같은 파일을 읽어 GPT-2 81개·KLUE 17개 토큰을 출력했습니다. |
| Ch5→Ch6 | Ch5의 로컬 모델 선택표는 판단 원리이고 Ch6은 외부 API 후보와 호출로 전환함을 설명합니다. Ch6의 Pydantic은 이 절에서 새로 도입하며 Ch2 클래스 문법과 구분합니다. |
| Ch6→Ch7→Ch8 | 현재 정본 SHA-256 연쇄를 다시 계산했습니다. Ch7의 `source_record`는 Ch6 정본 `531b30d0…`과 run ID를, Ch8은 Ch7 정본 `e124b791…`과 run ID를 정확히 가리킵니다. 세 로그에는 같은 가격 기준일과 일반 입력·캐시 입력·출력 단가가 남습니다. 챕터별 `notebooks/` 작업 폴더의 새 커널 실행도 압축 해제본에서 통과했습니다. |
| Ch8→Ch9 | 실제 E01 PDF와 Ch8 02·03·06을 다시 대조했습니다. 주차는 최초 2시간, 휴관 예외는 공휴일이 월요일과 겹칠 때 다음 화요일, 대출 범위는 회원 한 사람으로 일치합니다. `effective_date`는 합성 필터 값으로 설명합니다. Ch8의 복합 ID `E01-p3`과 Ch9의 `doc_id=E01,page=3` 대응도 명시했습니다. |
| Ch9→Ch10 | Ch9 02는 `cl100k_base`로 실제 첫 청크 498자·491토큰을 측정하며 Ch5 토크나이저와 직접 비교하지 않습니다. Ch10 HWPX 예제는 `t` 요소의 평문 추출까지만 주장하고 문단·표 구조 보존이나 Ch11 파서 평가를 완료했다고 쓰지 않습니다. |
| Ch9·10→Ch11 | Ch11 `evaluate.py`가 Ch9 1행과 Ch10 6행을 실제로 읽습니다. 챕터 폴더에서 README의 상대 경로 명령을 실행해 7개 실행을 확인했습니다. 후보 수가 부족한 컷오프는 `null`이고, `candidate_count/candidate_doc_ids`와 보고용 `returned_count/top_results`가 구분됩니다. |
| Ch11→Ch12 | Ch11 JSONL과 Ch12 질문 복제본은 30개 질문·정답 ID·dev/test 15/15가 완전히 같습니다. Ch12는 36개 dev 설정×15문항과 선택 설정의 test 15문항을 분리합니다. 555개 질문 결과의 Recall·Precision·nDCG를 저장 순위에서 다시 계산하는 검사가 통과했습니다. |
| Ch12 전반→후반·통합 실행 | 전반 12문서·8질문과 후반 PDF 6건·부모 6개·자식 175개·질문 30개의 전환과 직접 비교 제한이 명시됐습니다. `advanced-documents.json`의 부모·자식 본문을 현재 PDF에서 다시 생성했을 때 정본과 일치했습니다. 36개 TF-IDF+MMR 검색 설정과 Q002 통합 RAG를 구분하며, 통합 로그는 256차원·`gpt-5.4-mini`·생성 평가 `not_evaluated`를 기록합니다. |

### 직접 실행한 검증

- `uv run --project labs/part2/ch08-context-engineering --with pytest pytest -q labs/part2/ch08-context-engineering/tests/test_ch06_ch08_continuity.py` — **5 passed**. 경로 탐색, 가격 계산, 원문 사실, 로그 ID·지문 연결을 확인했습니다.
- `uv run --project labs/part3/ch11-evaluation --with pytest==9.0.2 pytest -q labs/part3/ch11-evaluation/tests/test_evaluate.py` — **8 passed**. 다중 정답 Recall, 후보 수 경계, ID 중복, 출처 필드와 질문 불일치 거부를 확인했습니다.
- `uv run --project labs/part3/ch11-evaluation --with ruff==0.15.7 ruff check ...` — **All checks passed**.
- `uv run --project labs/part3/ch12-retrieval-tuning --with pytest pytest -q labs/part3/ch12-retrieval-tuning/tests/test_continuity.py` — **4 passed**. 질문 복제, ID 대응, dev/test 분리, 다중 정답·MMR·통합 실행 필드를 확인했습니다.
- `uv run --no-project --python 3.12 --with pytest --with nbformat --with nbclient --with ipykernel --with python-dotenv==1.2.3 --with pillow pytest -q textbook/_notebook/tests` — **38 passed, 하위 검사 16개 passed**. 첫 실행에서 검증 환경에 `python-dotenv`가 빠져 난 4개 실패는 같은 명령에 실행기의 선언 의존성을 포함해 재현·해소했습니다.
- `textbook/_notebook/verify.py` 직접 실행 — Ch6 **6절/48셀**, Ch7 **8절/58셀**, Ch8 **6절/80셀**, Ch12 **12절/81셀** PASS. 최신 노트북 코드·출력과 빌드 HTML·내장 다운로드가 일치합니다.
- 현재 `check_course_continuity.py`의 결과 파일 쓰기만 `/tmp`로 바꾼 독립 실행 — 변경·데이터 재실행 **18개**, 코드·출력·메타데이터 보존 **69개**, Ch9·10 전달 행 **7개**, 현재 ZIP **4개** PASS. 총 87개 노트북을 모두 확인했습니다.

### 데이터·로그·원본 보존

- 수정 전 보존본 `full-course-before.tar.gz`의 SHA-256은 `061fdfc23ce4bd7810a65c4c99aa650f9ea11a86d9f58497efa46c1cbc5c1ba8`이며, 966개 파일과 87개 노트북 불변 정보가 별도 매니페스트에 있습니다.
- 수정 전 로그 97개 중 93개는 현재도 바이트가 같습니다. 갱신한 정본 포인터 4개의 이전 바이트는 실행별 이력에 남습니다.
- Ch12 핵심 로그 6개의 `before-*` 사본 해시는 수정 전 매니페스트와 각각 정확히 같습니다. 새 UTC 실행본 6개와 현재 포인터도 대응별로 바이트가 같습니다.
- Ch11/12 질문·정답·분할, Ch12 부모·자식 식별자, Ch9/10의 질문·검색 순위·출처가 모두 현재 정본에 연결됩니다. 검색 평가와 생성 답변 평가는 로그 필드와 본문에서 분리됩니다.

### 빌드·배포

- `course-delivery-results.json` — HTML **103개**, 노트북 **87개/620셀**, 링크 **1,531개**, 복습 문제 **315개**, 공개 파일의 자격 증명 노출 **0건**.
- `global-visual-results.json` — 1280px와 390px에서 **206/206 화면 PASS**. 최신 HTML보다 뒤에 생성된 결과이며 잘림·가로 스크롤·도식 경계·이미지·코드 복사 오류가 모두 0입니다.
- `language/final-semantic-review.md` — 변경 산문 52개의 현재 해시가 수집본과 모두 일치하고, 원문·수정본 의미 대조와 수치·경로 보호를 거쳐 최종 **ACCEPT** 판정을 받았습니다.
- SVG 87개와 Excalidraw 정본 87개는 수정 전 해시를 유지합니다. 이번 연결 수정에 도식 내용 변경이 필요하지 않았고, 현재 SVG는 HTML에 반영됐습니다.
- ZIP 매니페스트와 현재 학생 파일을 바이트 비교했습니다. `part1-practice.zip` SHA-256 `de9cc842…c2c90`, `part2-practice.zip` `000c1855…da08`, `part3-practice.zip` `4d36a480…38b0`, `llm-practice.zip` `a750de3e…fd95`입니다.
- 최종 `llm-practice.zip`을 새 폴더에 풀고 ZIP의 잠금 환경만으로 대표 노트북 11개를 새 커널 실행했습니다. Ch4 파일 생성→Ch5 소비, Ch6→7→8 로그 SHA 연쇄, Ch9 토큰 확인→Ch11 실제 로그 평가, Ch12 토큰 단위와 36개 dev 설정→test 1회→Q002 통합 RAG가 모두 통과했습니다. API 키는 프로세스 환경으로만 전달됐고 ZIP·출력에 기록되지 않았습니다.

## Gaps

- 없음. 현재 Ch1–Ch12 연결성 완료 판정을 막는 기술 증거 공백은 없습니다.

## Risks

- Anthropic·Google 키가 없어 Ch6의 두 공급자 분기는 `skipped`입니다. OpenAI 경로와 파일 전달은 실제 API로 확인했습니다.
- Windows/Linux와 VS Code의 수동 커널 선택 화면은 실행하지 않았습니다. macOS에서 Python 3.12.13, uv, 챕터별 잠금 환경, 챕터·노트북 작업 폴더를 검증했습니다.
- Ch13과 Ch15 학생용 구현은 아직 없습니다. Ch12는 처리 단계·입출력과 실제 답변·출처·`not_evaluated` 상태를 전달하므로, 후속 집필 때 이 계약을 실제 코드와 다시 대조해야 합니다.
