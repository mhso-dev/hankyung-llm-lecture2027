> 후속 전체 검증: 최종 ZIP 현재 파일 대조·압축 해제본 실행은 `bundle-execution-results.json`, 최종 화면은 `global-visual-results.json`에서 확인합니다. 아래는 담당 구간 실행 당시의 기록입니다.

# Ch 3 → Ch 4 → Ch 5 → Ch 6 연결 수정 후 검증

> 검증일: 2026-09-10  
> 수정 전 보존본: `textbook/qa/continuity-evidence/full-course-before.tar.gz`  
> 실행 원문: `textbook/qa/continuity-evidence/ch04-05-tests.txt`  
> 노트북 셀 번호는 마크다운을 포함해 0부터 세는 위치입니다.

## 수정 결과

| 연결 | 수정 후 실제 경로 | 검증 결과 |
| --- | --- | --- |
| Ch 3 → Ch 4 | Ch 3은 임시 Git 저장소를 Ch 4에 전달하지 않고, 별도의 Ch 4 프로젝트에서 시크릿 제외와 diff 확인 습관만 계속 적용한다고 설명합니다. Ch 4는 배포된 가상 CSV·JSON·HTML과 로컬 HTTP 서버만 사용합니다. | Ch 3 `_src/05-시크릿-이력-정리와-예방.html:9`, Ch 4 `README.md:3-10`, `data_tools.py`와 테스트를 직접 대조했습니다. 실행 산출물 전달과 개념적 습관의 연결이 구분됩니다. |
| Ch 4 조회 함수 → 후속 도구화 | `fetch_orders`, `find_customer_orders`, `fetch_articles`는 `data_tools.py`에 있으며 CSV·SQLite·로컬 REST 입력을 각각 처리합니다. | `tests/test_data_tools.py`의 정상·필터·HTTP 오류·반복 페이지 검사가 포함된 전체 10개 검사가 통과했습니다. Ch 19에서 도구 함수로 감쌀 수 있는 반환값은 `list[dict]`로 유지됩니다. |
| Ch 4 HTML 파싱 → Ch 5 토큰화 | Ch 4 05가 배포된 `data/article.html`을 읽어 파싱하고, `schema_version`, `source`, `record`를 가진 `data/article-text.json`을 직접 기록한 뒤 다시 읽어 같은지 확인합니다. 같은 파싱을 재현하는 `data_tools.py`의 `parse_article_html()`도 전달 파일과 원문을 회귀 검사합니다. Ch 5 01은 이 파일을 직접 읽어 `record.text`를 GPT-2와 KLUE tokenizer에 넣습니다. | 전달 JSON이 없는 임시 배포 구조에서 Ch 4 노트북 05 셀 2·4를 실행해 파일이 새로 생기고 배포 JSON과 같음을 확인했습니다. Ch 5 노트북 01 셀 4의 기존 Python 3.12 실행 결과는 기사 `A10`의 제목·요약 결합 텍스트를 GPT-2 81개, KLUE 17개 토큰으로 측정합니다. 회귀 검사는 JSON `record`와 현재 HTML의 재파싱 결과가 정확히 같은지 확인합니다. |
| Ch 5 01·03 → Ch 5 04 | 04절은 tokenizer와 토큰 수 측정의 출처를 01절로, 입력 토큰 관계의 직관을 03절로 나눠 지칭합니다. | `_src/04-컨텍스트-윈도.html:4`와 빌드 HTML을 대조했습니다. 존재하지 않는 “03절 tokenizer”를 선수 도구로 참조하지 않습니다. |
| Ch 5 08 → Ch 6 | Ch 5의 로컬 Qwen·MiniLM·KLUE 표는 작업·라이선스 필터 예제임을 유지합니다. Ch 6에서는 이 표를 복사하지 않고 외부 생성 API 후보 OpenAI·Anthropic·Google에 작업 적합성과 키 준비 여부를 적용한다고 설명합니다. | `_src/08-모델-선택-기준.html:10`과 Ch 6의 공급자 전환 본문·노트북을 직접 대조했습니다. Ch 6의 1회 호출을 품질 순위로 해석하지 않는 한계를 명시했습니다. |
| Ch 5 품질 개념 → Ch 11·15 | 후속 평가를 한 종류의 “모델 품질”로 묶지 않고 Ch 11의 검색 결과 평가와 Ch 15의 생성 답변 정확성·근거성 평가로 나눕니다. | Ch 5 08의 `_src`와 빌드 HTML 모두 두 평가 단위를 구분합니다. |
| Ch 5 토큰·임베딩·컨텍스트 개념 → Ch 8·9·12 | 개념은 이어지지만 모델, 문서, 질문, 측정 단위가 달라 Ch 5 수치와 후속 수치를 직접 비교하지 않습니다. Ch 12는 GPT-2·KLUE 모델 토큰, `cl100k_base` 청킹 토큰, Kiwi 검색 토큰의 용도와 규칙이 다르다고 보강됐습니다. | Ch 8·9·12의 현재 `_src`를 읽어 모델과 평가 단위를 대조했습니다. Ch 12 `_src/04-한국어-Kiwi와-BM25.html:4`에 비교 제한이 명시돼 있습니다. |

## 데이터와 배포 경로

`article-text.json`의 스키마는 다음 의미로 고정했습니다.

- `schema_version`: `ch04-parsed-article-v1`
- `source`: 배포 묶음 최상위 기준 `labs/part1/ch04-data-tools/data/article.html`
- `record.id`, `record.title`, `record.summary`, `record.published`: 원본 HTML의 기사 필드
- `record.text`: 제목, 줄바꿈, 요약을 결합한 모델 입력 문자열

원본 HTML SHA-256은 `b554f51d18e0495562a31548557083b26f0bda3b09d73fb9b6673565283f521a`, 전달 JSON SHA-256은 `e241854443edac502e0a9e090191ace34dbced1885a600db3af29a20a93103d1`입니다. `textbook/_notebook/build_bundle.py:59`의 Ch 4 공개 자료 목록에 `data/article-text.json`이 포함돼 있습니다. 최종 ZIP의 압축 해제 실행은 전체 배포 담당 검증에서 다시 확인합니다.

두 README는 압축 해제 최상위가 아니라 각 챕터 폴더에서 터미널을 열고 `uv sync --locked`를 실행하도록 작업 폴더를 명시합니다. Ch 5 노트북은 상위 디렉터리를 탐색해 배포 묶음의 고정 상대 경로에서 Ch 4 파일을 찾으므로 저장소와 압축 해제본에서 같은 코드를 사용합니다.

## 실행과 정적 검증

재현 가능한 전체 명령과 stdout은 `ch04-05-tests.txt`에 보존했습니다.

- Ruff 0.16.6: 수정 Python 파일 4개 `All checks passed!`
- README 준비 명령: 각 챕터 폴더에서 `uv sync --locked` 실행 → Ch 4는 58개 패키지 해석·53개 확인, Ch 5는 81개 해석·62개 확인
- Ch 4 회귀 검사: `uv run python -m pytest -q tests/test_data_tools.py` → `10 passed in 0.82s`
- Ch 4 05 새 커널: 전달 JSON이 없는 임시 배포 구조와 정본에서 각각 코드 셀 6개 PASS, 생성 파일이 정본 JSON과 같음
- Ch 5 01: 코드 변경 없이 기존 Python 3.12.13 실행 메타데이터와 `schema: ch04-parsed-article-v1`, `GPT-2: 81 | KLUE: 17` 출력을 보존하고 다시 검사함
- Ch 5 08 교차 재검토: 현재 `_src`와 빌드 HTML은 Ch 11 검색 지표와 Ch 15 생성 답변 평가를 이미 구분하며, 노트북 마크다운에는 Ch 11 품질 예고가 없음. 수정 전 보존본과 현재 노트북의 코드·출력·메타데이터 SHA-256이 각각 동일함
- Ch 4 `_src` 빌드 후 계약 검사: 5절, 코드 셀 30개, 최대 24줄 PASS
- Ch 5 `_src` 빌드 후 계약 검사: 8절, 코드 셀 34개, 최대 21줄 PASS

계약 검사는 빌드 HTML의 코드, 출력, 내장 다운로드 노트북이 실행 노트북과 같은지 확인합니다. 두 노트북은 서로 새 커널에서 독립 실행됐고, Ch 5 01은 Ch 4 커널의 변수를 전달받지 않고 JSON 파일만 읽었습니다.

## 한국어와 의미 검토

수정한 본문과 README에서 프로젝트 금지 표현을 다시 검색했고 일치 항목이 없었습니다. 코드·경로·수치가 바뀌지 않도록 `_src`와 빌드 HTML을 대조했습니다. 작성자와 다른 독립 검토자는 Ch 4 파서와 JSON이 같고 Ch 5 새 커널이 해당 JSON을 실제로 소비했으며, Ch 6 전환과 Ch 11·15 평가 구분이 정확하다고 판정했습니다. 분리된 한국어 검토자도 원문 대비 의미 보존, 초보자 설명, 코드·경로·수치 보호를 확인해 중요 결함 없음으로 판정했습니다. 외부 맞춤법 서비스는 상업적 대량 처리 제한 때문에 생략하고 로컬 맞춤법 정독으로 대체했습니다. 전체 Phase 6 최종 검수는 ZIP 재생성과 다른 챕터 동결 뒤 총괄 검증에서 확정합니다. Ch 4~5 소스 범위에는 남은 중요 결함이 없습니다.

## 남은 제한

- GPT-2 81개와 KLUE 17개는 이 기사 문자열과 고정 tokenizer에서 얻은 값입니다. 다른 tokenizer나 문서의 비용·한도 비교값으로 사용하지 않습니다.
- Ch 5의 어텐션 가중치는 교육용 계산이고 실제 공급자 모델 내부에서 측정한 값이 아닙니다.
- Ch 5의 Context rot 실험과 Ch 8 실험은 모델·프롬프트·평가 조건이 다르므로 결과 수치를 직접 비교하지 않습니다.
- Ch 5의 로컬 모델 필터 표는 Ch 6의 공급자 목록으로 변환되는 데이터 파일이 아닙니다. 작업 적합성과 실행 가능성이라는 선택 절차만 이어집니다.
- 검토 시점의 기존 `textbook/downloads/part1-practice.zip`에는 새 `article-text.json`이 없어 Ch 5 01이 실패합니다. 빌더 입력 목록은 수정됐지만, 최종 ZIP을 재생성하고 압축 해제본에서 Ch 4 05 → Ch 5 01을 실행하는 전체 배포 검증이 끝나기 전에는 ZIP 검증을 완료로 표시하지 않습니다.
