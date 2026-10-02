> 이 기록은 Ch8–12 우선 검증 당시의 실행 증거입니다. 이후 Ch1–12 확장 검증에서 변경한 모델·출력·배포물의 현재 상태는 [전체 연결성 검증](../../../qa/chapter-continuity-verification.md)을 확인합니다. 아래 과거 실행 기록은 보존합니다.

# Ch11→Ch12 및 Ch12 후반 연결성 수정 후 검증

검증일은 2026-09-10입니다. 수정 전 파일은 `before.tar.gz`와 `before-manifest.json`에 보존했습니다. 이 문서는 `tuning-review.md`에 기록한 문제를 수정한 뒤 현재 `_src`, 학생용 노트북, 데이터, 실행 로그를 다시 대조한 결과입니다.

## 수정 결과

| 연결 구간 | 최종 연결 관계 | 수정·검증 근거 | 판정 |
|---|---|---|---|
| Ch9→Ch12 01절 | Ch9 학생용 노트북의 실제 `InMemoryVectorStore.similarity_search()`와 반환 `Document`를 되짚습니다. 배포하지 않는 내부 `rag.py`의 `search()`를 선수 함수로 제시하지 않습니다. | `textbook/part3/ch12-retrieval-tuning/_src/01-벡터-거리와-정확-검색.html` | 수정 완료 |
| Ch10·Ch11→Ch12 07절 | 전반의 교육용 12문서·8문항과 후반의 PDF 6건·Ch11 30문항을 구분했습니다. `doc_id`, `parent_id`, `page`, `chunk_id`, `gold_doc_ids`의 대응과 서로 다른 입력·지표의 직접 비교 금지를 명시했습니다. | `_src/07-cross-encoder-리랭킹.html`; `data/advanced-documents.json`; `data/advanced-queries.json` | 수정 완료 |
| Ch11 dev/test→Ch12 07~12절 | 07·09·10·11절의 한 문항 예시는 개발용 Q001을 사용합니다. 08절의 두 리랭커·후보 수 비교는 개발 15문항만 사용합니다. 11절의 대화형 재작성도 Q001 주제로 바꿨습니다. 12절에서 개발 15문항으로 설정을 고른 뒤 시험 15문항을 한 번 평가합니다. 별도 통합 스모크는 개발용 Q002를 사용합니다. | 학생용 노트북 07~12; `_src/07`~`_src/12`; `advanced-continuity-test-result.json` | 수정 완료 |
| Ch11 질문·로그→Ch12 실험 로그 | 12절은 Ch11 `evaluation-queries.jsonl`을 직접 읽고 배포 복제본과 완전 일치를 검사합니다. 각 개발 실행에는 질문·말뭉치 지문, `qid`, 분할, 정답 ID, 반환 수, `doc_id/page/chunk_id/rank`, 질문별 지표와 tier 집계를 남깁니다. | 노트북 12 ‘Ch11 원본 질문 확인’, ‘36개 개발 설정 실행’, ‘개발 로그 저장과 시험 1회 평가’; `runs/advanced-continuity-*` | 수정 완료 |
| Ch11 평가 단위→Ch12 평가 단위 | Ch12는 상위 50개 청크를 후보로 만든 뒤 `parent_id` 중복을 제거해 고유 부모 문서 순위를 평가합니다. `candidate_unit=chunk`, `evaluation_unit=unique-parent-document`, 별도 정책 이름을 기록해 Ch11의 고유 문서 후보 지표와 직접 비교하지 않게 했습니다. Recall은 정답 ID 교집합 비율로 계산합니다. 현재 30문항의 정답은 모두 하나이므로 기존 수치는 같지만 여러 정답으로 확장해도 필드 뜻이 유지됩니다. | 노트북 12 평가 함수·설정·로그; `tests/test_continuity.py`; `_src/12` 6절 | 수정 완료 |
| 36개 TF-IDF+MMR 실험→통합 RAG | 36개 실행은 Ch11 개발 질문으로 설정을 선택하는 검색 평가입니다. 별도 통합 실행은 PDF에서 직접 읽은 35개 쪽 본문을 dense·Kiwi BM25·RRF·CrossEncoder에 전달하고 같은 쪽 본문과 출처로 답변 형식만 확인합니다. 검색 지표와 생성 답변 품질은 평가하지 않았음을 로그에 `null`/`not_evaluated`로 남겼습니다. | 노트북 12; `_src/12`; `figures/12-통합-RAG.svg`; `advanced-continuity-integrated-result.json` | 수정 완료 |
| Ch12→Ch13·Ch15 | Ch13에는 질문·검색 결과·출처 객체 형식과 처리 단계 순서를 전달합니다. Ch15에는 `generation_evaluation.status=not_evaluated`인 통합 실행을 전달해 답변 정확성·근거성·출처 표기를 검색 평가와 분리합니다. | `_src/12` 8절; `advanced-continuity-integrated-result.json` | 수정 완료 |

## 실행 및 회귀 검증

- `uv sync --locked --project labs/part3/ch12-retrieval-tuning`은 잠금 파일의 106개 패키지를 해석하고 83개 설치 패키지를 확인했습니다.
- Python 3.12 새 커널에서 학생용 07~12절을 준비 셀부터 순서대로 실행했습니다. 통과한 코드 셀 수는 각각 4, 5, 4, 4, 5, 12개입니다. 07·08절은 로컬 CrossEncoder를 실제 실행했고, 11절은 `gpt-4.1-mini`, 12절은 `text-embedding-3-small`과 `gpt-4.1-mini`를 실제 호출했습니다.
- 12절 통합 실행은 PDF 6건 35쪽을 직접 읽었습니다. 개발용 Q002에서 E01 3쪽을 검색했고, 답변에 `[E01 p.3]` 출처를 포함했습니다. 이 값은 연결 스모크 결과이며 품질 점수로 해석하지 않습니다.
- `uv run --project labs/part3/ch12-retrieval-tuning --with pytest pytest -q labs/part3/ch12-retrieval-tuning/tests/test_continuity.py`는 4개 검사를 통과했습니다. Ch11 원본과 Ch12 복제본 완전 일치, dev/test 15/15, ID·쪽·청크 대응, 36개 개발 실행과 15개 시험 결과, 질문별 추적 필드, 정책·지문·통합 출처를 검사합니다. 또한 08절과 12절의 학생용 지표 함수를 AST로 분리 실행해 정답 2개 중 1개 검색은 Recall 0.5, 중복 정답·중복 검색은 한 번만 계산하는지 확인했습니다. 빈 정답이나 `answerable:false` 문항은 평균에서 제외하고, 평가 가능한 문항이 하나도 없으면 명시적 오류를 내는지 확인했습니다. 10절 MMR이 후보를 중복 선택하지 않는지도 검사합니다.
- 최종 정본 로그는 36×15=540개의 개발 질문 결과와 15개의 시험 질문 결과를 담습니다. 실행 ID는 `advanced-continuity-20260910T014213-*`이며, 같은 실행의 불변 사본을 `runs/continuity/20260910T014213/`에 보존했습니다.
- 수정 전 `advanced-experiment-log.jsonl`, `advanced-test-result.json`, `advanced-integrated-result.json`은 덮어쓰지 않았습니다. 현재 배포 정본은 `advanced-continuity-experiment-log.jsonl`, `advanced-continuity-test-result.json`, `advanced-continuity-integrated-result.json`입니다.
- 과거 일회성 생성기 `qa/advanced_author.py`는 현재 검토 결과를 덮어쓰지 못하도록 실행을 중단하며 유지보수 경로를 안내합니다.
- `_gen_figures.py`로 13쌍의 SVG·Excalidraw를 다시 생성했습니다. 통합 흐름은 실제 구현에 맞게 ‘쪽 본문·출처 선택’으로 동기화했습니다.
- `_build.py`는 index와 12개 절을 다시 빌드했습니다. `textbook/_notebook/verify.py --chapter textbook/part3/ch12-retrieval-tuning`은 12개 절과 75개 코드 셀을 통과했고 셀 길이 상한 25줄을 지켰습니다.

## 한국어 감사와 독립 검토 반영

수정 본문에서 폐기된 `search()`, 시험용 Q009 예시, ‘30문항 전체로 설정 선택’, ‘같은 175개 청크’, 잘못된 부모 본문 출처 표현을 다시 검색해 남지 않았음을 확인했습니다. 독립 검토자가 지적한 질문별 page/chunk/rank 누락, 시험 로그 날짜 누락, `source_chapter` 의미, 후보·평가 단위, 생성 평가 미실시 표시를 모두 반영했습니다. 외부 맞춤법 서비스는 대량 상업적 자동 전송 제한 때문에 실행하지 않았고, 로컬 정독과 독립 의미 검토로 대체했습니다. 최종 화면 검사는 전체 챕터 배포본을 만드는 상위 검증에서 수행합니다.

## 남은 한계

- 고급 평가는 공개 PDF 6건과 30문항에 한정됩니다. 정답 ID가 모두 하나이므로 여러 정답 문항의 실제 점수 변화는 관찰하지 못했고 합성 입력 회귀 검사로 계산 규칙만 확인했습니다.
- 50개 청크 후보를 6개 부모 문서로 합치므로 Recall이 포화됩니다. 상위 순서는 Precision@5와 nDCG@5, 질문별 순위로 판단해야 합니다.
- 통합 실행은 개발 질문 1건의 처리 연결만 확인했습니다. 생성 답변의 정확성·근거성·출처 정확성 평가는 Ch15에서 별도로 수행해야 합니다.
- 실행은 현재 macOS·CPU 환경에서 확인했습니다. 다른 운영체제와 GPU의 시간·수치 차이는 검증하지 않았습니다.
