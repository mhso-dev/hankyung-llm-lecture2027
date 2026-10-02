# Ch 10 노트북 전환 및 실행 검증

최신 단계별 실습 검증은 textbook/_notebook/GUIDED-PRACTICE-VERIFICATION.md를 참고합니다. 아래는 이전 전환 기록입니다.

## Before/After 최신 검증 — 2026-09-08

실행 예제 다음에 Before 실패 코드·실제 출력과 After 수정 코드·실제 출력을 배치했습니다. 모든 셀은 Python 3.12.13 새 커널에서 순서대로 실제 실행했습니다.

| 절 | 코드 셀 | Before | After | 결과 |
|---|---:|---:|---:|---|
| 01-문서와-메타데이터 | 5 | 1 | 1 | PASS |
| 02-PDF와-표-OCR | 5 | 1 | 1 | PASS |
| 03-DOCX-HTML-CSV | 5 | 1 | 1 | PASS |
| 04-HWP와-HWPX | 5 | 1 | 1 | PASS |
| 05-문자-재귀-토큰-청킹 | 6 | 1 | 1 | PASS |
| 06-구조와-시맨틱-청킹 | 5 | 1 | 1 | PASS |
| 07-한국어-임베딩과-캐시 | 5 | 1 | 1 | PASS |
| 08-인덱싱-비교-실험 | 7 | 1 | 1 | PASS |

총 43셀, 최대 16줄입니다. 실패·수정 셀은 HTML의 6번 블록에 표시하며, 전체 코드·출력·다운로드 대조를 통과했습니다. 변경 전 원본은 챕터 qa/before-after-before에 보관했습니다.

아래는 이전 호출 전환 시점의 기록입니다. 최신 셀 개수와 해시는 공통 checks/notebook-contracts.json을 기준으로 합니다.

## 정리 계획

1. 기존 `_src` 원본을 `qa/notebook-before/`에 보관합니다.
2. 기존 모듈·예제·테스트는 유지하고 실행 예제 영역만 노트북으로 바꿉니다.
3. 외부 패키지가 필요한 절에는 설치 셀을 두고, 개념 확인과 예상 실패를 짧은 셀로 구성합니다.
4. 각 노트북을 새 Python 3.12 커널에서 실행하고 코드와 출력 해시를 기록합니다.
5. HTML 원본의 실행 예제에는 같은 이름의 노트북 토큰을 연결합니다.

## 변경 전 기준선

- 백업: `_src`의 절 8개와 `index.html`을 `qa/notebook-before/`에 보관했습니다.
- 테스트: `uv run --project labs/part3/ch10-document-processing pytest labs/part3/ch10-document-processing/tests -q`
- 결과: 38개 통과, 실패 0개

## Before/After 보강 계획

보강 전 노트북 8개와 `_src` 9개는 `qa/before-after-before/`에 보관했습니다. 각 노트북은 기본 예제 뒤에 Before와 After를 연속으로 둡니다. Before는 구체적인 예외나 잘못된 결과를 출력하고, After는 같은 원인을 수정해 단언문과 실제 출력으로 확인합니다. 세부 계획은 `qa/before-after-plan.md`에 기록했습니다.

## LangChain 전환 계획

1. 06~08절 노트북과 관련 `_src`를 `qa/langchain-before/`에 보관합니다.
2. 직접 SDK 호출을 `OpenAIEmbeddings.embed_documents()`와 `embed_query()`로 교체합니다.
3. 공급자 사용량 필드를 만들지 않고 `tiktoken` 로컬 추정치를 구분해 기록합니다.
4. 06~08절만 새 커널에서 실행하고 캐시 1회와 JSONL 여섯 줄을 확인합니다.

전환 전 노트북 3개와 `_src` 3개는 `qa/langchain-before/`에 보관했습니다. 전환 후 실행 명령은 다음과 같습니다.

```bash
uv -q run --project labs/part3/ch10-document-processing \
  --with nbclient --with ipykernel --with pip --with python-dotenv \
  python textbook/_notebook/execute.py \
  labs/part3/ch10-document-processing/notebooks/06-구조와-시맨틱-청킹.ipynb \
  labs/part3/ch10-document-processing/notebooks/07-한국어-임베딩과-캐시.ipynb \
  labs/part3/ch10-document-processing/notebooks/08-인덱싱-비교-실험.ipynb
```

## 실행 결과

실행 명령은 다음과 같습니다.

```bash
uv -q run --project labs/part3/ch10-document-processing \
  --with nbclient --with ipykernel --with pip --with python-dotenv \
  python textbook/_notebook/execute.py \
  labs/part3/ch10-document-processing/notebooks/*.ipynb
```

8개 노트북은 모두 Python 3.12.13 새 커널에서 통과했습니다. 01~05절 실행 뒤 06절 After 셀의 누락된 로컬 함수를 확인해 셀 내부 계산으로 수정했고, 06~08절을 새 커널에서 다시 실행했습니다. 가장 긴 코드 셀은 16줄입니다. 설치 셀은 `uv.lock`에서 실제 실행한 버전으로 고정했습니다.

| 절 | 상태 | 코드 SHA-256 앞 12자 | 출력 SHA-256 앞 12자 | 최대 셀 줄 수 |
|---|---|---:|---:|---:|
| 01 문서와 메타데이터 | 통과 | `3d3aa63695d5` | `455863d755fa` | 8 |
| 02 PDF와 표 OCR | 통과 | `9ea69cf0ace8` | `895744563603` | 10 |
| 03 DOCX HTML CSV | 통과 | `ef7e69b2bc1a` | `bb50da7021ca` | 11 |
| 04 HWP와 HWPX | 통과 | `b50759c0e75b` | `de25ceb7bce7` | 15 |
| 05 문자 재귀 토큰 청킹 | 통과 | `7a434522f0b3` | `45675949f9a3` | 11 |
| 06 구조와 시맨틱 청킹 | 통과 | `6b7aa818868c` | `fdd65665fed7` | 13 |
| 07 한국어 임베딩과 캐시 | 통과 | `e7135062b31d` | `5ea1bb6a296d` | 14 |
| 08 인덱싱 비교 실험 | 통과 | `be386eb02a21` | `73a861a107d9` | 16 |

06~08절은 LangChain `OpenAIEmbeddings`로 실제 API를 검증했습니다. 06절은 `embed_documents()`로 세 문장을 임베딩합니다. 07절은 첫 요청에 `embed_documents()`를 한 번 호출한 뒤 두 번째 요청을 캐시에서 읽으며, `api_calls=1`과 256차원을 출력합니다. 08절은 같은 원문에서 재귀 3개, 토큰 5개, 구조 2개의 청크를 계산한 뒤 `embed_documents()`와 `embed_query()`로 여섯 조합을 실행합니다. LangChain 인터페이스는 공급자 사용량을 반환하지 않으므로 실제 토큰 사용량을 주장하지 않습니다. 노트북은 `tiktoken`으로 센 로컬 추정치와 전략·모델·질문·청크 ID·최상위 출처를 JSONL 여섯 줄로 저장합니다.

Before/After 실행도 8개 절에서 모두 통과했습니다. 04절 Before는 레거시 HWP를 ZIP으로 열어 `BadZipFile`을 포착합니다. After는 파일 시그니처로 레거시 HWP를 지원하지 않는 형식으로 분류하고 ZIP 열기를 건너뛰며, HWPX만 ZIP/XML로 읽어 실제 본문을 출력합니다. 다른 절은 쪽 번호, 빈 PDF 텍스트 층, CSV 열, 청크 오버랩, 시맨틱 임계값, 벡터 차원, 검색 정답 부재를 각각 같은 원인의 수정 코드와 연결합니다.

## 정적 검사

- HTML 노트북 토큰: 16개 (`example` 8개, `failure` 8개)
- Before/After 메타데이터 셀: 32개(절마다 마크다운 2개와 코드 2개)
- 셀 순서: 8개 모두 example → before → after
- 노트북의 사용자 홈 절대 경로: 0개
- `__file__`, `sys.path`, 로컬 `document_processing`·`experiment` import: 0개
- `_src` 실행 경로의 `{{code:...}}` 조각: 0개
- Before 코드: 8개 모두 구체적인 예외 또는 잘못된 결과를 출력
- After 코드: 8개 모두 같은 원인을 수정하고 단언문과 실제 출력을 생성
- 잠금 파일: `uv lock --check` 통과, `langchain-openai==1.6.0` 확인
- 회귀 테스트: 38개 통과
- Ruff: 모듈 전체 통과. 8개 노트북은 셀 단위 import 배치와 교육용 인접 쌍 표현 규칙만 제외하고 통과

## 한국어 슬롭 검수

### 진단 요약

새로 쓴 노트북 설명과 실행 연결 문단을 검토했습니다. 대시 대비 헤드라인, 조사·체언 종결 조각문, `A에서 B로` 전환 공식은 발견되지 않았습니다. 심각도는 낮음입니다.

### 수정 텍스트

검수 결과를 반영한 문장은 각 노트북의 마크다운 셀과 `_src`에 직접 저장했습니다. 반복되는 실행 안내는 절마다 대상과 관찰값을 구체적으로 적었습니다.

### 주요 변경사항

- 긴 모듈 코드를 노출하던 실행 경로를 독립 실행 가능한 노트북으로 교체했습니다.
- 오프라인 특징 벡터 수치는 과거 회귀 기록으로 구분하고 실제 API 출력과 분리했습니다.
- HWPX 실습이 ZIP/XML 검사 범위임을 명시하고 레거시 HWP 지원을 주장하지 않았습니다.
- 실패 설명을 실행 가능한 Before/After 셀로 바꾸고 각 수정이 같은 원인을 해결하는지 확인했습니다.

## 확인 필요 항목

- HWPX 픽스처는 ZIP/XML 로더 경계를 확인하는 최소 표식입니다. 실제 한컴오피스 호환성과 레거시 HWP 본문 추출은 검증 범위에 포함되지 않습니다.
- PDF 실습은 텍스트 층과 OCR 후보 쪽을 판별합니다. OCR 엔진 실행이나 OCR 정확도 평가는 포함하지 않습니다.
- 08절의 원문 하나와 질문 하나 실험은 API와 3×2 실행 구조, 최소 JSONL 기록을 검증합니다. 최종 임베딩 모델과 청킹 방식은 Ch 11의 정답 질의셋 평가 전까지 확정하지 않습니다.
