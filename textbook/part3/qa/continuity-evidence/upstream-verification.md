# Ch 8 → Ch 9 → Ch 10 연결 수정 및 재검증

## 근거 표기 방법

노트북 셀 번호는 마크다운과 코드 셀을 모두 포함한 **1부터 시작하는 전체 셀 번호**로 적고, 코드 셀은 실행 번호 `In[n]`과 핵심 변수 이름을 함께 적습니다. 수정하면서 셀이 추가되었으므로 번호만으로 근거를 식별하지 않습니다.

## 수정 결과

| 연결 | 수정 내용 | 최종 산출물 |
|---|---|---|
| Ch 8 → Ch 9 | Ch 8의 후속 예고에서 검색 선택 평가는 Ch 11, 생성 답의 내용·근거·출처 형식 자동 평가는 Ch 15로 분리했습니다. | `textbook/part2/ch08-context-engineering/_src/06-단계적-공개와-설계-비교.html`과 빌드 HTML |
| Ch 9 선수 지식 | Ch 4가 `pypdf`를 이미 사용했다는 잘못된 설명을 바로잡았습니다. Ch 4의 HTML 파싱 개념은 이어 받고, PDF·`PdfReader`·`extract_text()`는 Ch 9에서 처음 도입한다고 명시했습니다. 출처 형식은 Ch 11에서 판정 기준을 합의하고 Ch 15에서 자동 평가한다고 구분했습니다. | Ch 9 `_src/01`, `_src/02`, `_src/04`, index와 빌드 HTML |
| Ch 9 → Ch 10 → Ch 11 | Ch 9 06의 임시 소규모 검색을 18개 디지털 PDF와 Ch 11 Q001의 실제 검색·생성으로 바꿨습니다. Ch 10 08은 기존의 짧은 원문 3×2 관찰을 유지하고, 같은 18개 PDF와 Q001을 3가지 청킹×2가지 임베딩으로 다시 검색하는 6개 연결 실행을 추가했습니다. | Ch 9 06 노트북 전체 셀 11~18(`documents`, `hits`, `record`), Ch 10 08 노트북 전체 셀 14~19(`digital_items`, `continuity_runs`, `records`) |
| Ch 10 → Ch 11 | 두 노트북이 `qid`, `question`, `gold_doc_ids`, 순위가 있는 `retrieved`, `source_chapter`, `source_run_id`, `config`를 JSONL로 기록합니다. 각 검색 항목은 `doc_id`, 안정 문자열 `chunk_id`, 1부터 시작하는 `page`·`rank`, 숫자 `score`를 가집니다. | `runs/continuity-ch09-search.jsonl`, `runs/continuity-ch10-indexing.jsonl` |
| 입력 추적 | 두 로그의 `config.inputs`에 말뭉치 범위, `manifest.json` SHA-256, Ch 11 평가 질문셋 SHA-256을 기록했습니다. Ch 10은 각 청킹 방법의 실제 인자도 `split_config`에 기록합니다. | 말뭉치 해시 `27541f4121edb594a598432d8a3ac3539436aadbcce3ca38faa14f74ed7749df`, 질문셋 해시 `9544b332d5ac120e2af8beeffb148d6fd29387b4dd7f6ca16a927f971e7fe1bd` |
| 로그 보존 | 고정 이름 JSONL은 다음 챕터가 읽는 최신 포인터로 원자적으로 교체하고, 각 행은 `runs/continuity/<source_run_id>.jsonl`에도 별도 보존합니다. 기존 `runs.jsonl`과 과거 상세 로그는 수정하지 않았습니다. | Ch 9 최신 실행 `20260909T161218875711-ch09`, Ch 10 최신 6개 실행 `20260909T160602375493-ch10-01`~`06` |
| 학생 실행 경로 | Ch 9 06이 ZIP에 없는 `textbook/_notebook/execute.py` 대신 `uv run --project ... --with nbconvert ... jupyter nbconvert` 명령을 출력하도록 바꿨습니다. Ch 9·10 README의 준비 명령은 잠금 파일을 지키는 `uv sync --locked`로 맞췄습니다. | Ch 9 06 전체 셀 17~18 / `In[9]`, Ch 9·10 README |
| Ch 10 후속 범위 | `file_type`·`parser`를 Ch 12가 실패 유형별로 집계한다는 잘못된 예고를 제거했습니다. Ch 10의 실제 PDF 6설정 연결 실행과 Ch 12의 고정 청크 TF-IDF·MMR 36회 비교는 문서·질문·평가 단위가 다른 별도 범위라고 목차에 명시했습니다. | Ch 10 `_src/01`, `_src/08`, index와 빌드 HTML |

Ch 9 06의 Before/After는 둘 다 E01의 같은 쪽과 Q001을 사용합니다. `chunk_size`만 500에서 100으로 바꾸고 이전 색인을 잘못 재사용하는 실패를 확인한 뒤, 같은 입력을 다시 나눠 15개 청크를 만들었습니다. 새 검색의 첫 청크 길이는 68자였습니다. 문서 범위와 질문을 함께 바꾸던 중간 구현은 최종본에 남지 않습니다.

## 실제 실행 결과

- Ch 9 06, Python 3.12.13 새 커널: `PASS 06-실험-하네스.ipynb: 11 cells`. 18개 디지털 PDF의 물리적 93쪽을 읽어 176개 청크를 만들었고 Q001 top-2는 E01이었습니다. 생성 답은 `미르시립도서관의 정기 휴관일은 **매주 월요일**입니다. [E01 p.2]`였습니다. 빈 텍스트 3쪽을 제외하는 Ch 11의 후보 단위는 90쪽이므로 93쪽과 90쪽은 서로 다른 집계를 뜻합니다.
- Ch 10 08, Python 3.12.13 새 커널: `PASS 08-인덱싱-비교-실험.ipynb: 10 cells`. 3가지 청킹×2가지 임베딩의 6개 실제 검색을 실행했고 여섯 설정 모두 Q001의 1위 문서 ID가 E01이었습니다.
- 학생용 재실행 명령: Ch 9 노트북이 출력한 `uv ... --with nbconvert==7.17.0 ... jupyter nbconvert --execute --inplace` 명령을 `RUN_NAME=k4 RETRIEVAL_K=4`로 실제 실행해 종료 코드 0을 확인했습니다. 이후 교재 정본은 내부 실행기로 기본 k=2를 새 커널에서 다시 실행해 실제 출력과 검증 메타데이터를 고정했습니다.
- Ch 11 strict loader: `evaluate.py --split dev`에 두 canonical JSONL을 직접 넣어 7개 실행과 각 Q001 1행을 읽었습니다. 모든 실행은 `recall_at_logged_candidates=1.0`이었습니다. Ch 9은 기록 후보가 2개이므로 Recall@5·@50, Precision@5, nDCG@5가 모두 `null`입니다. Ch 10의 6개 실행은 기록 후보가 5개이므로 Recall@5=1.0, Precision@5=0.2, nDCG@5=1.0이고 Recall@50은 `null`입니다.
- canonical JSONL SHA-256: Ch 9 `4f9fce621e29c4e267d466a38629d6ee78da876593f882397e0ed5e25f5bae61` 1행, Ch 10 `37949f0c677e91de29602f853f968b335dd8ea8aace55e50953e3ef51343b192` 6행. 각 canonical 행이 같은 `source_run_id`의 불변 파일과 정확히 같은지 검사했습니다.

## 회귀·빌드 검증

- `uv sync --locked`: Ch 9·Ch 10 모두 성공했습니다.
- Ch 9 단위 테스트: `uv run pytest -q tests` → 10개 통과.
- Ch 10 단위 테스트: `uv run pytest -q tests` → 38개 통과.
- 단위 테스트 48개와 최신 strict loader의 원본 표준 출력은 `textbook/part3/qa/continuity-evidence/upstream-tests.txt`에 보존했습니다.
- 세 챕터 `_build.py`: Ch 8 6절, Ch 9 6절, Ch 10 8절을 다시 빌드했습니다.
- HTML↔노트북 검사: Ch 8 `PASS 6 sections / 77 code cells (max 21 lines)`, Ch 9 `PASS 6 sections / 59 code cells (max 25 lines)`, Ch 10 `PASS 8 sections / 66 code cells (max 24 lines)`.
- 수정한 노트북·빌드 HTML·canonical 로그에서 사용자 절대 경로, API 키 문자열, `sk-` 형태 비밀값을 검색했으며 발견되지 않았습니다.
- 설명만 바꾼 Ch 8, Ch 9 01·02·04, Ch 10 01과 목차는 관련 노트북을 재호출하지 않았습니다. `_build.py`와 HTML↔노트북 검사를 통해 기존 코드·출력·실행 메타데이터가 그대로 포함되는지 확인했습니다.
- 작성자와 다른 독립 검토자가 최종 `_src`, 빌드 HTML, canonical 로그를 대조했습니다. 그 과정에서 Ch 9 01의 짧은 예제 범위, Ch 9 목차의 JSONL 필드 설명, Ch 9 06의 존재하지 않는 빈 `metrics` 설명을 찾아 수정했습니다. 수정 후에는 검토 범위에 남은 중요 결함이 없다고 판정했습니다.

## 비교 한계와 남은 작업

Q001 한 질문에서 정답 문서 E01이 검색되었다는 결과는 연결 경로와 로그 형식이 실행된다는 증거입니다. 한 질문의 같은 문서 ID 기준 지표만으로 세 청킹과 두 임베딩의 근거 청크 품질이나 전체 설정 우열을 결정할 수 없습니다. 설정 선택에는 개발용 질문 전체와 청크 수준 정답 근거가 추가로 필요합니다.

화면 크기별 표시·코드 복사, 최종 배포 ZIP 압축 해제 실행, 프로젝트 전체 한국어 감사는 전체 통합을 맡은 최종 책임자가 수행합니다. 이 문서 작성 시점에는 upstream 코드·로그·빌드·strict loader 검증까지 완료했습니다.
