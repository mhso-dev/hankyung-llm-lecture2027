# Ch1–Ch12 연결성 수정과 재검증

검증일: 2026-09-10(Asia/Seoul). 상태: 완료. 확인하지 못한 범위는 마지막 절에 명시합니다.

현재 작성된 Ch1부터 마지막 Ch12까지 87개 절의 `_src`, 학생 노트북, 원문 데이터, 실제 로그를 대조했습니다. 기존 완료 보고서의 PASS는 근거로 대신하지 않았습니다. 아래 연결 판정은 수정 후 현재 파일 기준입니다. 수정 전 파일 966개와 87개 노트북의 실행 상태는 [수정 전 검토](chapter-continuity-review.md)의 보존본에 남아 있습니다.

## 최종 연결 관계

| 구간 | 앞에서 전달하는 내용 → 다음 장의 실제 사용 | 수정 후 판정·근거 |
|---|---|---|
| Ch1→Ch2 | Python 3.12·uv·챕터 `.venv`, `hello.py`의 저장·실행 원리 → Ch2 독립 프로젝트의 변수·함수·파일 실습 | 일치. Git의 실제 사용 예고는 Ch3으로 교정했습니다. `ch01-03-review.md`의 본문 행·셀 표, `ch01-03-verification.md`의 새 환경·명령 출력 |
| Ch2→Ch3 | `Path`, 파일 쓰기, 함수·타입 힌트, `subprocess` → 새 임시 Git 저장소에서 커밋·분기·충돌 실습 | 일치. 각 노트북은 앞 커밋을 불러오지 않고 원리를 적용합니다. Ch2 async의 직접 적용은 향후 Ch18·30으로 구분합니다. 같은 상세 기록과 Ch3 02의 `workspace/remote/author` 셀 |
| Ch3→Ch4 | diff·시크릿 예방·변경 검토 습관 → 별도 Ch4 프로젝트의 데이터 함수·테스트 | 일치. 임시 Git 저장소를 물려받는다는 설명을 고쳤습니다. `git-filter-repo` 버전 확인도 실제 패키지 메타데이터 조회로 수정했습니다. Ch3 README 및 `ch01-03-verification.md` |
| Ch4→Ch5 | 실제 `data/article.html` 파싱 → `data/article-text.json`의 `schema_version/source/record` → Ch5 01 토큰 측정 | 실제 파일 전달 완료. Ch4가 JSON을 직접 생성하고 Ch5가 읽습니다. 원문·생성 JSON 일치, GPT-2 81개·KLUE 17개 관찰. `ch04-05-review.md`, `ch04-05-verification.md`, JSON 삭제 후 배포본 실행 |
| Ch5→Ch6 | 로컬 모델의 작업 적합성·실행 조건·라이선스 판단 → API 모델 후보 선택과 호출·비용 측정 | 일치. 로컬 모델 표를 자동 입력하는 구현은 없으며 후보와 실행 방식의 전환 이유를 설명했습니다. A트랙 클래스 기초와 Ch6의 Pydantic 첫 도입도 구분했습니다. `ch06-08-review.md`, Ch5 08·Ch6 01/03 본문 |
| Ch6→Ch7 | `provider-comparison-continuity.json`의 사용량·가격 정책·실행 ID → Ch7 08이 실제 파일과 SHA-256을 확인하고 A/B 기록 작성 | 실제 로그 전달 완료. 입력·캐시·출력 토큰, 지연, 예상 비용, 단가 기준일의 의미를 유지합니다. 서로 다른 질문의 결과를 개선율로 비교하지 않습니다. `ch06-08-verification.md`, `course-static-results.json` |
| Ch7→Ch8 | 프롬프트 원문·변경 이유·응답·사용량 기록 → Ch8 06이 `prompt-ab-continuity.json`의 ID·지문·가격 정책을 이어 사용 | 실제 로그 전달 완료. 단어 포함 수는 정독 보조이며 생성 답변 품질 점수로 쓰지 않습니다. `context-design-continuity.json`에 실제 입력·응답·자동 확인·미평가 상태를 기록합니다. 같은 실행 기록과 회귀 검사 5개 |
| Ch8→Ch9 | 작은 근거를 선택하는 원리와 `E01-p3` → PDF 검색의 `InMemoryVectorStore.similarity_search()`, `doc_id=E01/page=3` | 일치. 동일 원천 위치를 가리키되 ID 형식은 다릅니다. PDF와 충돌한 주차 시간·휴관 예외·회원 조건을 수정하고 재실행했습니다. 필터 예제의 가상 시행일을 실제 문서 날짜와 구분했습니다. `ch06-08-verification.md`, Part3 `continuity-guide.md` |
| Ch9→Ch10 | PDF 18건, 문서·쪽·청크·검색 순위와 실제 Q001 검색/답변 → Ch10의 파싱·청킹 원리 실습 뒤 같은 PDF·Q001의 여섯 설정 로그 | 일치. 작은 독립 예제와 후반 PDF 재사용을 명시합니다. Ch9 02에서 실제 청크 토큰을 측정하고 설치 핀을 잠금 버전에 맞췄습니다. Ch10 HWPX는 현재 본문 문자열 추출만 수행하므로 구조 보존·파서별 평가 예고를 바로잡았습니다. `ch09-10-addendum-verification.md` |
| Ch10→Ch11 | Ch9 1행·Ch10 6행의 실제 검색 로그 → Ch11 06에서 기록된 후보·문서 ID를 평가 | 실제 입력 7행 재평가 완료. 부족한 후보의 Recall@50은 미측정(null)이고, 자체 페이지 검색 기준선과 연결 확인 Q001 점수를 직접 비교하지 않습니다. `ch11-upstream-refresh.txt`, `course-static-results.json`, 별도 고유 평가 파일 |
| Ch11→Ch12 | 동일 질문 30개·gold 문서 ID·개발/시험 15개씩 → 후반 부모 PDF 6건·청크 175개에서 설정 선택·시험 | 일치. 전반 12문서·8질문 예제에서 바뀌는 이유·대응·비교 한계를 명시합니다. 36건은 TF-IDF+MMR 개발 설정 비교, 1건은 선택 설정의 시험 결과입니다. 통합 RAG는 별도 Q002 답변 실행입니다. 검색 지표와 생성 평가를 분리합니다. `course-static-results.json`, Ch12 07~12 본문·노트북 |

위 표의 구간별 상세 기록은 모두 `continuity-evidence/`에 있습니다. 파일·행 및 셀 번호를 포함한 수정 전 근거는 [검토 기록](chapter-continuity-review.md)과 각 담당 구간의 `*-review.md`를 확인합니다. 잘못된 예고만 삭제해 실제 전달을 생략하지 않았습니다. Ch4→5, Ch6→7→8, Ch9→10→11은 현재 학생 파일을 읽고 쓰는 연결입니다. 독립 실행이 필요한 Git 저장소·원리 예제는 유지하며 앞 학습과의 관계를 설명했습니다.

Ch5의 모델 토큰(GPT-2·KLUE), Ch9/10의 임베딩용 토큰, Ch12의 Kiwi 검색 토큰은 분할 규칙과 용도가 다릅니다. 이 수치를 직접 비교하지 않습니다. Ch12 08의 여섯 지표 행은 두 리랭커가 각각 20개 후보를 한 번 점수화한 결과를 재사용한 것이며, 후보 수별 지연을 여섯 번 측정했다는 설명을 교정했습니다.

Ch12 12의 통합 실행은 임베딩 256차원과 `gpt-5.4-mini`를 명시하고 실제 응답·출처를 기록했습니다. Ch12 11의 `gpt-4.1-mini`는 별도 질문 재작성 예제임을 설명합니다. 모델 이름 일부가 같아도 문서·질문·청킹·평가 단위가 다른 결과를 직접 비교할 수 없습니다.

## 실행·회귀·원본 보존

- 학생 잠금 환경 12개를 분리 복사한 뒤 `uv sync --locked`와 실제 Python 3.12.13 커널을 확인했습니다. Ch6~12에 빠진 ipykernel, `%pip`를 사용하는 Ch6~10·12에 빠진 pip를 기존 과정 표준 버전으로 추가했습니다. 기존 잠금 패키지 버전은 변경하지 않았습니다. `locked-environment-results.json`, `pip-before.json`, `kernel-dependency-diff.json`에 전후 증거가 있습니다.
- 코드 변경 노트북 17개는 준비 셀부터 새 커널로 실행했습니다. Ch11 06은 코드 변경 없이 새 Ch10 로그를 입력하기 위해 추가 재실행했습니다. 나머지 69개는 수정 전과 코드·출력·실행 횟수·노트북 메타데이터가 같습니다. 87개 전체를 새로 실행했다는 뜻은 아닙니다. 각 실행 시간·코드/출력 해시는 `course-static-results.json`에 있습니다.
- Ch6~8의 최종 실행은 각 챕터 잠금 `.venv`와 `notebooks/` 작업 폴더로 수행했습니다. Ch12 01~06도 같은 방법으로 임베딩 API와 pgvector를 실제 실행했습니다. 컨테이너는 검증 뒤 중지했습니다. `ch06-08-tests.txt`, `ch12-core-path-verification.md`를 확인합니다.
- 87개 노트북의 코드 셀에서 사용한 경로를 별도 검토자가 읽고 챕터·노트북 폴더 탐색 16개 검사를 통과했습니다. 현재 미해결 cwd 오류는 없습니다. `cwd-independent-review.md`에 근거가 있습니다.
- 공통 실행·빌드·다운로드 회귀 38개와 하위 검사 16개, Ch4 데이터 검사 10개, Ch6~8 연결 검사 5개, Ch9 검사 10개, Ch11 평가 검사 8개, Ch12 연결 검사 4개가 통과했습니다. 개별 명령과 원출력은 해당 `*-tests.txt` 및 `shared-tests-final.txt`에 보존했습니다. QA 도구 실행 환경의 누락 패키지는 보완 후 재검사했으며 학생 환경 검증과 구분합니다. `root-lint-final.txt`도 통과했습니다.
- 수정 전 로그 97개 중 93개는 현재 파일도 바이트가 같고, 갱신한 현재 파일 4개는 기존 실행 원본을 별도 이력에 보존했습니다. Ch12 core 로그 6개는 수정 전 백업과 새 UTC 실행본을 따로 남겼으며 결과 값은 이전과 같았습니다. 기존 실행을 새 출력으로 가장하지 않았습니다. `course-static-results.json`과 `ch12-core-path-verification.md`를 확인합니다.
- Ch11/12 질문·정답·개발/시험 분할 일치를 확인하고 Ch12 37개 실행의 질문별 결과 555개와 집계를 원시 순위에서 다시 계산했습니다. 통합 답변 인용은 실제 검색 문서·쪽 안에 있으며 생성 품질은 `not_evaluated`입니다.

## 빌드·배포·화면

`_src`에서 다시 빌드한 87개 절의 620개 코드 셀·실제 출력·내장 다운로드가 원본 노트북과 일치합니다. 전체 목차를 포함한 HTML 103개, 로컬 링크 1,531개, 복습 문제 315개를 검사했습니다. 깨진 링크와 공개 파일의 키 노출은 없습니다. `course-static-results.json`, `course-delivery-results.json`이 현재 파일의 근거입니다.

SVG 87개와 편집 원본 87개는 수정 전 SHA-256을 유지합니다. 변경한 연결 설명은 도식의 내용 변경을 요구하지 않았으므로 도식 생성/API 호출을 반복하지 않았습니다. PC 1280px·모바일 390px의 총 206개 화면에서 글자 크기·대비·잘림·도식 경계·가로 넘침·셀별/전체 코드 복사·다운로드가 통과했습니다. 대표 화면은 별도 검토자가 직접 확인했습니다. `global-visual-results.json`은 103개 HTML과 검사 결과의 해시를 연결합니다.

최종 배포 묶음은 다음과 같습니다. ZIP 내 manifest의 모든 항목을 현재 파일과 바이트 비교했고 압축 무결성을 확인했습니다.

- `part1-practice.zip`: 60개 manifest 파일, SHA-256 `de9cc84278e5e3442adba8a03b9d7f393db2719d0212d9bb601f2587ac7c2c90`
- `part2-practice.zip`: 32개 manifest 파일, SHA-256 `000c18552c8e061d326ba83627ceff8fcbcb89c0693b12372ec15b57ef66da08`
- `part3-practice.zip`: 83개 manifest 파일, SHA-256 `4d36a48004cad7af879537bc3454b793d7a0783499f180464785567ea21d38b0`
- `llm-practice.zip`: 175개 manifest 파일, SHA-256 `a750de3e00a8bf7878f391eda12bb79322f982f7eba20251751352630633fd95`

압축 해제본에서는 Ch1 `hello.py`와 노트북 11개를 실제 새 커널로 실행해 통과했습니다. Ch4 05→Ch5 01, Ch6 06→Ch7 08→Ch8 02·03·06, Ch9 02, Ch11 06, Ch12 04·12 순서입니다. Ch4 JSON을 먼저 삭제한 뒤 새로 생성한 파일을 Ch5에 입력했고, Ch6→7→8의 새 실행 ID·SHA-256 연결도 확인했습니다. `bundle-execution-results.json`과 `bundle-execution/`에 실행 노트북·출력을 보존합니다. 학생 커널은 ZIP의 pyproject·uv.lock으로 만든 챕터 `.venv`입니다. 저장소의 데이터·전용 모듈을 대신 읽지 않습니다. 외부 검증 실행기만 별도 프로세스에서 사용하며 API 키는 검증 프로세스 환경으로만 전달합니다.

## 독립 검토와 한국어 감사

작성 담당자와 다른 검토자가 현재 본문·코드·데이터·실행 증거를 다시 대조했습니다. 독립 기술 검토에서 남은 중요 구현 결함은 없었습니다. 판정 근거는 `continuity-evidence/independent-final-review.md`의 PASS와 `continuity-evidence/language/final-semantic-review.md`의 ACCEPT에 기록했습니다. 최종 한국어·의미 검토에서도 남은 중요 결함은 없습니다. 한국어 검토 범위는 최종 수집한 변경 산문 52개 파일이며 코드·경로·수치는 보호합니다.

외부 맞춤법 검사는 생략했습니다. [korean-spell-check SKILL.md](/Users/mhso/.codex/plugins/cache/moai-cowork/moai-writer/1.4.1/skills/korean-spell-check/SKILL.md:35)가 “상업적 대량 처리”를 사용 금지로 명시하여 이번 교재 일괄 감사에 적용했습니다. 일반 슬롭 검사 뒤 로컬 맞춤법·문맥 정독, korean-humanize Phase 6 원문 대비 의미 검수를 수행했습니다. 외부 서비스에 원문을 전송하지 않았습니다.

## 확인하지 못한 범위와 영향

- Ch13 이후는 아직 집필되지 않았습니다. 커리큘럼과 예고의 범위는 확인했지만 실제 후속 코드 연결이 실행됐다고 표시하지 않습니다. Ch13에는 단계별 입출력, Ch15에는 실제 응답·출처·미평가 상태를 전달합니다. 검색 지표 통과를 생성 답변 품질 통과로 확대하지 않습니다.
- Anthropic·Google API 키가 없어 Ch6의 해당 제공자 실행은 `skipped`입니다. OpenAI 호출·비용·로그 전달은 실제 실행했지만 두 제공자의 사용량·캐시 형식은 미검증입니다.
- 실행 환경은 macOS의 Python 3.12·uv입니다. Windows/Linux 및 실제 VS Code 확장 UI에서의 수동 커널 선택은 별도 실행하지 않았습니다. 챕터 잠금 환경, 실제 커널 경로, 압축 해제 폴더의 상대 경로는 직접 검증했습니다.
- 모델 가중치·패키지 최초 다운로드와 유료 API는 인터넷이 필요합니다. ZIP은 가중치·키를 포함하지 않으며 README에 준비 방법을 안내합니다. 교재의 고의 실패 예제와 실제 API 응답의 품질 한계는 유지했습니다.
