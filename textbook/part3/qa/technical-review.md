# Part 3 Ch 9–12 기술·의미 독립 검토

- 검토자: Terra 별도 검토 패스
- 시작: 2026-09-09 KST
- 범위: Ch 9·10의 기존 실행 근거와 Ch 11·12의 새 본문·노트북이 만들려는 주장 사이의 일치. 언어 감사는 범위 밖이다.
- 수정 권한: 없음. 이 문서는 검토 기록만 담는다.

## 판정 기준

1. 교재가 제시한 수치가 같은 실행에서 다시 만들어지는가.
2. 지표의 분모·평가 단위·빈 결과 정책이 본문, 코드, 로그에서 동일한가.
3. 1차 검색, 리랭킹, MMR, 필터, parent 전달처럼 다른 단계의 효과를 섞어 주장하지 않는가.
4. 학습용 예시의 결과를 새 질문·중간/어려운 문서 일반 성능으로 부풀리지 않는가.
5. “30개 실험 로그”가 30번의 실제 설정 변경·평가 실행인지, 형식만 복제한 행인지 확인한다.

## Ch 11 초기 판정 — 수정 필요

검토 시점에는 `textbook/part3/ch11-evaluation/_src/*.html`과 노트북 6개가 `[[작성: …]]` 자리표시자를 남긴 초안이다. 따라서 본문 설명·실행 출력의 최종 의미 판정은 보류한다.

### R1. 문서 ID 기준 지표와 page 결과의 중복이 서로 맞지 않음 (중요)

`labs/part3/ch11-evaluation/evaluate.py`의 검색 결과는 page 단위지만 정답은 `gold_doc_ids` 문서 단위다. `recall_at`은 set으로 바꾸어 문서 중복을 제거하지만, `precision_at`과 `ndcg_at`은 상위 page마다 같은 정답 `doc_id`를 다시 1점으로 센다.

재현된 `runs/baseline.json`의 Q001 상위 5개는 `E01, E01, E01, E01, M04`이며 P@5가 0.8로 기록됐다. 문서 ID 기준 정답이 E01 하나라면 중복 문서는 한 문서의 근거 조각일 뿐이므로 P@5와 nDCG에서 네 번의 독립 정답이 될 수 없다.

**필요 조치**: 정렬된 page 결과를 문서 ID 기준으로 한 번만 남긴 뒤 Recall@50·P@5·nDCG@5를 모두 계산하거나, 반대로 정답을 page/chunk ID로 다시 설계한다. 두 방식을 한 지표에 섞지 않는다.

### R2. nDCG의 이상적 순위(IDCG) 계산이 gold 집합을 쓰지 않음 (중요)

`ndcg_at`의 `ideal_count`는 `len(gold)`가 아니라 반환된 결과 전체에 들어 있는 관련 **page 수**에서 계산된다. 다중 정답 문서가 있는 질문에서 일부 정답을 놓치면 IDCG도 작아져 nDCG가 높아질 수 있으며, 같은 문서의 page 중복도 이상 점수에 들어간다.

**필요 조치**: R1에서 평가 단위를 정한 뒤 `ideal_count = min(k, len(gold_units))`로 계산한다. 이진 관련도에서 정답 하나를 6위에 두면 nDCG@5=0, 정답을 1위에 두면 1이 되는 작은 고정 순위 예제로 단위 검증한다.

### R3. Recall@50=1.0은 검색기가 완전하다는 증거가 아님 (중요)

새 커널에서 `uv run python evaluate.py --output /tmp/ch11-review-baseline.json --top-k 5`를 실행해 baseline 수치 `Recall@50=1.0`, `P@5=0.433333…`, `nDCG@5=0.569948…`, 30문항을 재생성했다.

같은 실행에서 non-scanned 말뭉치는 90 page·17 document이고, 각 질의의 top-50에는 12~17개의 서로 다른 문서가 포함됐다. 30개 gold 문서는 모두 top-50에 포함됐다. 즉 이 작은 말뭉치와 넓은 후보 창에서 후보 대부분을 노출한 상태에 가깝다. 이 값은 “이 baseline·이 질의셋에서는 후보 50개에 gold가 있었다”까지만 뜻하며, 검색기의 일반적 recall 또는 Ch 12 조정의 우수성을 보장하지 않는다.

**필요 조치**: 본문·캡션에 이 범위를 명시한다. Ch 12에서는 후보 수를 줄인 비교, medium/hard 문서, 새 질문을 포함한 test 분리를 사용해야 1.0을 넘어서는 차이를 관찰할 수 있다.

### R4. 질의셋 분포와 새 질문 test 분리가 없음 (중요)

`evaluation-queries.jsonl` 30개는 모두 `tier: easy`이고 E01–E05만 gold로 둔다. manifest에는 medium·hard 문서가 있으나 이 baseline의 질의셋에는 없다. 질문 문장이 공개 PDF 표현에 가까운 학습용 질문이라, 이 한 집합으로 청킹·가중치·리랭커를 반복 튜닝하면 동일 질문에 맞춘 결과가 된다.

**필요 조치**: 학습용 development와 마지막 test 질문을 파일/필드로 분리하고, test는 파라미터·모델 선정 후 한 번만 본다. test에도 medium/hard 및 정답 문서 없는 질의를 별도 `answerable:false` 정책으로 포함할지 명시한다. test를 만들 수 없다면 “학습용 비교이며 일반화 평가는 아님”을 적는다.

### R5. 빈 정답과 빈 후보의 정책이 코드·로그에 없음 (보통)

현재 `gold_doc_ids=[]`이면 모든 지표가 0으로 평균에 섞인다. 이는 거부해야 하는 질문, 주석 누락, 관련 문서가 정말 없는 경우를 구분하지 못한다. 빈 후보도 반환 개수를 기록하지 않아 필터나 API 제한으로 k개를 채우지 못한 원인을 읽을 수 없다.

**필요 조치**: `answerable`, `expected_action`, `returned_count`, `metrics_policy`를 로그에 남긴다. `answerable:false`는 검색 지표 평균에서 제외하고 제외 수를 보고한다. `answerable:true`의 빈 후보는 Recall/P@k/nDCG@k=0으로 기록한다.

## Ch 12 도착 후 확인할 항목

- pgvector: `vector`/`halfvec` 차원, 연산자 클래스, 임베딩 차원, pgvector 확장 버전이 실행 출력과 일치하는가. HNSW+필터는 post-filter라 LIMIT보다 적은 행이 나올 수 있다는 실측/경계를 보이는가. iterative scan의 strict/relaxed 순서 보장 차이를 구분하는가.
- RRF: dense와 sparse가 독립 후보 목록을 만들고 rank(1부터 시작)만 합산하는가. cosine/BM25 원점수를 직접 합산했다고 RRF라고 부르지 않는가.
- Cross-Encoder: 같은 1차 후보 집합·동일 후보 수로 모델을 비교하는가. 후보 밖 문서를 회복했다고 주장하지 않는가. 모델 내려받기·실행 출력과 모델 revision·라이선스가 기록되는가.
- MMR: 후보 중복을 줄이는 재정렬임을 유지하는가. λ를 바꿀 때 후보 집합·평가 질의·k를 고정하는가.
- parent-document: child 검색 단위와 parent 전달 단위를 분리하고, gold의 문서/child 평가 단위를 섞지 않는가. 전달 parent 중복 제거와 컨텍스트 토큰 증가를 기록하는가.
- query rewrite: 원 질문을 보존하고, rewrite만/원문만/양쪽 RRF를 분리 비교하는가. 고유명사·부정·날짜 조건이 사라지는 실패를 확인하는가.
- 30 로그: 각 행마다 실제 run ID, 설정, 질의셋 버전, 말뭉치 fingerprint, 결과 지표, latency, 날짜가 있고 행 사이에 바뀐 변수가 하나인지 확인한다.

## 2026-09-09 중간 재검토

### Ch 11 코드 수정 확인과 남은 불일치

`evaluate.py`는 page 순위를 문서 ID 기준으로 중복 제거하고, IDCG를 `min(k, len(gold))`로 바꾸었다. `metrics_policy: unique-doc-macro-v1`도 추가됐다. 이는 R1·R2의 **평가 함수** 수정으로 적절하다.

그러나 현재 노트북 생성기 `_make_notebooks.py`에는 같은 정책이 아직 반영되지 않았다.

- 01절의 `required == set(item)` 검사는 새 `answerable`, `split` 필드가 있는 실제 JSONL에서 실패한다.
- 03절 설명은 “상위 5개 페이지”라고 하지만 `search()`는 문서 중복을 제거해 문서를 반환한다.
- 04절은 반환 상위 5개의 gain만 정렬해 IDCG를 만들므로, 정답이 여러 개인 질의에서 놓친 gold가 있으면 nDCG가 다시 높게 계산된다. `len(gold)`를 기준으로 IDCG를 만들어야 한다.
- 05·06절은 `answerable:false` 제외와 `returned_count` 기록을 구현하지 않는다. JSONL에는 dev/test 분리가 새로 들어갔지만, 현재 계산은 split을 선택하지 않고 모두 섞는다.

이 생성기를 수정해 노트북을 다시 만들고 빈 커널로 실행하기 전까지 R1·R2는 최종 통과가 아니다.

### Ch 11 질의셋 개선과 남은 경계

새 JSONL에는 medium/hard 질의와 `dev`/`test` 필드가 생겼다. 이전의 all-easy 문제는 완화됐다. 다만 test가 파라미터 선택 이후 한 번만 읽혔는지, `answerable:false` 사례의 평균 제외 규칙을 실제 코드·로그가 지키는지는 아직 검증되지 않았다.

재실행 시 질문은 dev/test 15/15, easy/medium/hard 10/10/10, 모든 질문은 단일 `gold_doc_id`였다. 문서 ID 중복 제거 뒤 searchable 문서는 17개인데 `candidate_k=50`이므로 `search()`는 모든 질의에 사실상 전 말뭉치를 반환한다. 따라서 `Recall@50=1.0`은 이 코드 경로에서 **항상 참**이며 검색기 비교 지표가 될 수 없다. 또한 단일 정답 문서만 쓰는 P@5의 이론상 최댓값은 0.2라서, 재실행 값 P@5=0.2는 “상위 5개 안에 정답 문서가 모든 질문에서 있었다”는 뜻일 뿐 20% 품질이라는 뜻이 아니다. nDCG@5=0.905…만이 이 단일-gold 구성의 순위 차이를 보인다.

**리더 결정에 따른 수용 조건**: 새 문서나 실패 사례를 만들지 않는다. 수계산은 51위 통제 순위 목록으로 Recall@50=0이 되는 경우를 보여 주고, 실제 제공자료에서는 Recall@5/가변 k, 반환한 고유 문서 수, `17 < 50`의 천장 효과를 함께 표시한다. 단일 정답만 유지한다면 P@5의 상한 0.2와 해석을 본문·출력에 명시한다. 이 조건을 만족하면 R@50 포화는 자료의 한계로 수용한다. 다만 Ch 12가 R@50=1을 검색 개선의 근거로 쓰면 안 된다.

### Ch 11 최종 재실행 — 통과

`uv run python evaluate.py --output /tmp/ch11-terra-review.json --top-k 5`를 새로 실행했다. `unique-doc-macro-v1`, 30개 answerable 문항, 문항별 `returned_count=17`을 확인했고, Recall@5=1.0·Recall@50=1.0·Precision@5=0.2·nDCG@5=0.9051549589가 재현됐다. `02-Recall-at-50`의 51위 통제 목록은 정답 50위=1, 51위=0을 출력한다. 본문은 검색 가능한 17개 문서와 단일 gold의 P@5 최대 0.2를 명시한다.

Python 3.12 임시 커널에서 01–06 노트북을 순서대로 실행해 모두 통과했다. 따라서 R1·R2의 문서 단위 처리와 IDCG, R3의 포화 범위 설명, R5의 반환 문서 수 기록은 현재 Ch11 산출물에서 통과다. 이 기준선은 test 선택용 튜닝 결과가 아니라 작은 학습 말뭉치의 진단 값으로만 사용해야 한다.

### Ch 12 초기 상태

`ch12-retrieval-tuning`의 12개 노트북과 본문은 현재 자리표시자 초안이므로 실행·해석은 판정할 수 없다. `README.md`는 pgvector Docker를 `0.8.2-pg17`로 고정한다. 현재 공식 리서치의 최신 v0.8.6과 다른 버전을 쓸 수는 있으나, 본문에는 의도적 고정인지와 컨테이너에서 확인한 `extversion`을 남겨야 버전 혼동이 없다.

## Ch 12 advanced 초안 재검토 — 실행 전 수정 필요

### R6. 평가 질문의 gold 문서가 입력에 없음 (중요)

`advanced-documents.json`의 parent는 E01–E05 다섯 문서뿐인데, `advanced-queries.json`의 30개 gold는 E01·E02·M01·M02·H01·H02를 포함한다. 따라서 M01/M02/H01/H02 질문은 어떤 검색·리랭킹 설정으로도 gold를 반환할 수 없다. 07·08·12절의 “30문항” 결과는 입력 집합이 다르므로 설정 품질이 아니라 데이터 누락을 재게 된다.

**필요 조치**: (a) advanced 문서에 모든 gold parent를 넣거나 (b) 평가 질문을 E01–E05의 gold만 가진 독립된 고정 집합으로 제한한다. 본문·노트북·로그의 질의 수와 문서 ID 범위를 같은 값으로 맞춘다.

### R7. parent-document 노트북이 존재하지 않는 질의 ID를 참조함 (중요)

09절은 `qid == "Q017"`을 찾지만 현재 advanced 질의 ID는 Q001–Q010, Q037–Q046, Q085–Q094이다. 이는 빈 커널에서 `StopIteration`으로 끝난다.

**필요 조치**: 실제로 존재하고 parent가 포함된 질의 ID로 바꾸고, 새 커널 실행으로 확인한다.

### R8. 2개 리랭커 후보·한국어 범위·평가 split이 맞지 않음 (중요)

07·08절은 `cross-encoder/ms-marco-TinyBERT-L2-v2`와 `cross-encoder/ms-marco-MiniLM-L6-v2`를 CPU에서 호출한다. 이들은 본문이 설명하는 한국어 검색 실험 및 공식 리서치에서 확인한 한국어/다국어 후보(`BAAI/bge-reranker-v2-m3`, `Dongjin-kr/ko-reranker`)와 다르다. English MS MARCO 모델을 기술 smoke test로만 쓸 수는 있지만, 한국어 품질 비교의 두 후보라고 설명하면 근거가 없다.

12절은 dev/test 필드가 있는 30문항 전체에서 36개 조합을 만들고 그 전체에서 최고 설정을 고른다. test가 선택에 들어가므로 test 결과가 독립 검증이 아니다.

**필요 조치**: 선택할 모델·언어 범위를 본문과 패키지에 맞추거나 실험 목적을 기술 확인으로 좁힌다. 설정 선택은 dev만, 최종 보고는 고정 test만으로 분리한다. 각 로그에는 모델 ID/revision, 후보 수, 실행 시간, 입력 문서 집합 버전을 남긴다.

### R6–R8 수정본 확인 — 실행 증거 대기

수정 중인 `advanced-documents.json`은 E01·E02·H01·H02·M01·M02를 모두 parent로 포함한다. 09절도 Q009를 사용하도록 바뀌었고, 07·08절은 `BAAI/bge-reranker-v2-m3`와 `Dongjin-kr/ko-reranker`를 명시한다. 12절은 36개 조합을 dev에서만 선택한 뒤 고정 test로 한 번 평가한다. 이 변경은 R6–R8의 **코드 경로**를 해소한다.

두 CrossEncoder의 실제 모델 내려받기·추론과 빈 커널 순차 실행, 그리고 test 보고 출력이 아직 이 검토 패스에서 확인되지는 않았다. 08절이 두 모델의 후보 수 비교를 전체 30문항으로 실행한다면, 그 결과를 모델 선택의 독립 test 성능으로 해석하지 않는다는 설명도 필요하다.

### R9. 종합 로그의 실행 식별·입력 고정 정보가 부족함 (보통)

12절의 각 dev 행에는 현재 날짜·설정·지표·split·문항 수가 남지만, `run_id`, 입력 문서/질의 파일 fingerprint, 설정별 실행 시간은 없다. 날짜와 설정만으로는 같은 날 재실행한 두 결과를 구별할 수 없고, 입력이 바뀐 뒤의 값을 같은 실험으로 비교할 수도 없다.

**필요 조치**: JSONL 각 행에 고유 run ID, `advanced-documents.json`과 `advanced-queries.json`의 SHA-256(또는 같은 역할의 고정 fingerprint), 실제 평가에 걸린 시간을 기록한다. 36행이 모두 dev 실행인지와 선택된 단 하나의 설정을 test에서 평가한 결과도 별도 행 또는 명확한 출력으로 남긴다.

### R9 수정본 재검토 — 일부 통과, 최종 보완 필요

새 `advanced-experiment-log.jsonl`은 36행 모두 dev 15문항이며, 고유 `advanced-dev-01`부터 `advanced-dev-36`, `corpus_sha256`, `duration_ms`, 정책, 설정, 지표를 기록한다. 기록한 `corpus_sha256`은 현재 `advanced-documents.json` SHA-256과 일치한다. `advanced-test-result.json`은 선택한 dev run ID가 실제 36행 중 하나임을 가리키고 test 15문항을 한 번 평가한다. 따라서 36회 실제 dev 실행과 test 선택 분리는 확인됐다.

다만 질문 파일 SHA-256은 없으므로 `advanced-queries.json` 변경을 로그에서 탐지할 수 없다. test 결과에는 별도 test run ID·실행 시간·`metrics_policy`도 없다. 이 항목을 추가하고, 08절 본문의 이전 English 모델명도 현재 Korean/multilingual 모델명으로 동기화해야 Ch12 advanced의 최종 통과로 판정한다.

### R10. 36개 ‘종합’ 설정이 전체 검색 파이프라인을 튜닝하지 않음 (중요)

12절의 실제 36개 조합은 `char`/`char_wb` TF-IDF 분석기, n-gram, 반환 수, MMR λ만 바꾼다. dense 검색·Kiwi BM25·직접 RRF·CrossEncoder는 이 36회 경로에 들어가지 않고, 생성 모델에 출처 있는 근거를 전달해 답변하는 단계도 없다. 따라서 이 로그는 sparse+MMR 진단 실험으로는 유효하지만, ‘종합 튜닝’ 또는 제공 PDF를 읽어 검색·답변까지 완주한 증거는 아니다.

**필요 조치**: 36개 탐색을 확대하지 말고 이름과 해석 범위를 sparse+MMR 진단으로 좁힌다. 12절 마지막에 고정 한 조건으로 공개 PDF 6건을 dense와 Kiwi BM25로 각각 순위화하고, 직접 RRF·기존 CrossEncoder·parent 중복 제거를 거쳐 출처 태그를 포함한 context를 `init_chat_model`에 전달하는 실제 한 번의 통합 실행을 추가한다. 질문, 모델, 반환 chunk/parent ID, 답변, 출처, 실행 시간을 저장해 학생이 중간 단계를 재현할 수 있어야 한다.

### Ch 12 advanced 최종 재검토 — R6–R10 구현 통과, 참고 버전 정정 필요

수정된 `advanced-experiment-log.jsonl`은 36개의 고유 dev run ID, 문서·질의 SHA-256, 설정, 실행 시간, 지표 정책을 담는다. `advanced-test-result.json`은 `advanced-test-01`, 선택한 dev run ID, 고정 test 15문항, 실행 시간, 두 fingerprint, 정책을 기록한다. 따라서 R6–R9의 데이터 범위·모델 후보·test 누출·로그 재현성 조건은 통과다.

통합 실행 `advanced-integrated-01`도 확인했다. `E02-P03-C01`은 실제 원문에 ‘자기계발 연 60만 원’을 포함하고, 저장된 답변의 `[E02 p.3]` 출처는 retrieved ID와 일치한다. 이 실행은 제공 PDF 6건 로딩→dense·Kiwi BM25→직접 RRF→`BAAI/bge-reranker-v2-m3`→parent 중복 제거→`init_chat_model` 답변의 경로를 실제로 완주한다. 36행 탐색은 TF-IDF+MMR 진단으로 분리해 설명하므로 R10도 통과다.

다만 07–12절 참고 자료는 실행 환경 `sentence-transformers==6.0.1`과 달리 ‘Sentence Transformers 5.x’라고 적는다. `6.0.1` 또는 `6.x`로 고치고 HTML을 다시 빌드해야 최종 버전 정합성까지 통과다.

## Ch 9·10 연결 경계

Ch 9·10이 넘긴 `metadata.doc_id/page/chunk_id`와 `gold_doc_id`는 Ch 11·12에서 평가에 쓰는 입력이다. 청킹·파싱 설정을 바꾸면 retrieved `chunk_id`는 바뀔 수 있지만 `doc_id`가 바뀌면 전후 비교가 무효다. Ch 10의 오프라인 특징 벡터 실험은 실제 임베딩 품질 비교가 아니라는 기존 한계를 유지해야 한다.

## 최종 판정 준비 상태

- **Ch 9·10**: 기존 QA 회귀 검사 20건과 공통 구조 검증이 통과한 상태다. Ch10의 오프라인 특징 벡터는 실제 임베딩 품질 비교가 아니라는 한계를 유지해야 한다.
- **Ch 11**: R1–R5 통과. 문서 ID 단위 지표, 빈 정답 제외, 반환 수, 51위 통제, `17 < 50` 포화, P@5 상한 0.2가 코드·노트북·본문에서 일치한다.
- **Ch 12**: R6–R10의 입력 범위, parent ID, 한국어/다국어 CrossEncoder 후보, dev/test 분리, 36행 실행 기록, 통합 검색·출처 답변 경로는 통과했다. `advanced-integrated-01`의 E02-P03-C01과 `[E02 p.3]` 출처를 실제 원문과 대조했다.
- **최종 확인**: 07–12절 `_src`와 다시 빌드된 HTML의 ‘Sentence Transformers 5.x’ 표기는 모두 `Sentence Transformers 6.0.1`로 바뀌었다. 잠금 환경과 참고 자료가 일치하므로 **Ch 9–12 기술·의미 독립 검토는 통과**로 확정한다.
