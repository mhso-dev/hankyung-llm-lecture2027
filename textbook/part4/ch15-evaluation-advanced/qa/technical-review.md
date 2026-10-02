# Ch 15 기술 정독

## 검토 범위와 실행 상태

- 검토일: 2026-09-10 (KST)
- 대상: `_src/01`~`08`, 대응 노트북과 `data/evaluation-cases.json`입니다. 소스·노트북의 파일 시스템 수정 시각은 09:18:33~09:18:48 +0900입니다.
- 저장 출력이 있는 노트북은 01~03뿐입니다. 01은 Part 3 실험 로그와 새 생성 응답 세 건을 읽었고, 02는 평가자 표와 Q002 judge 원문을 출력했으며, 03은 규칙 기반 순서 편향 예제를 출력했습니다. 04~08은 아직 실행 출력이 없으므로 아래 판정은 코드·본문의 정적 근거입니다.
- Part 3 연결: `evaluation-cases.json`의 Q002 질문은 “도서는 한 번에 몇 권까지, 며칠 동안 빌릴 수 있나요?”이며, 현재 Part 3 통합 결과의 질문과 일치합니다. `gold_doc_ids`와 `reference answer`는 다른 항목으로 취급해야 합니다.
- 적절히 구분한 항목: 05의 로컬 trace·cache read/creation·TTFT/total 수치는 고정 실습값이라고 본문에 명시했고, 06의 비용도 교육용 합성값이라고 구분했습니다. 07의 Before/After는 같은 Q002·Q006·Q090 키를 비교하고 교육용 회귀 판정 입력이라고 명시했습니다. 08의 cloud 미실행은 제출 전 JSONL 검증 범위로 명시했으므로 그 자체는 결함이 아닙니다.

## 발견 사항

### T1 — 높음: Correctness에 필요한 `reference_answer`가 사례 데이터와 실행 코드에 없습니다

**근거**

- `02-4대-RAG-평가자.ipynb` 82~89행은 Correctness만 `reference=True`라고 올바르게 표시합니다.
- 그러나 `evaluation-cases.json`의 Q002·Q006·Q090에는 `reference_answer` 필드가 없고, 노트북 02의 실제 계산은 질문-응답 단어 겹침, 출처 문자열, 저장된 Groundedness judge 원문뿐입니다.
- `_src/02-4대-RAG-평가자.html` 6~7행은 Q002에 네 평가자를 적용한다고 설명합니다.

**영향**

Correctness를 적용했다고 설명하지만 응답을 비교할 정답 답변이 없습니다. `gold_doc_ids`를 정답 답변으로 쓰지 않는다는 본문의 올바른 주장이 코드에서 완결되지 않습니다.

**수정 및 재확인**

각 사례에 출처와 작성 기준을 표시한 `reference_answer`를 추가하고 Correctness 입력을 `response` 대 `reference_answer`로 출력합니다. 또는 노트북의 범위를 “네 평가자의 입력 표와 Groundedness 예시”로 고쳐 Correctness 실행을 주장하지 않습니다. 최종 출력에서 Correctness만 reference answer를 받으며 나머지 셋은 받지 않는지 확인합니다.

### T2 — 높음: 순서 편향 실험의 후보 동일성 비교가 실제로 계산되지 않습니다

**근거**

- `03-judge-프롬프트와-편향.ipynb` 48~54행의 `biased_pairwise`는 언제나 `'A'`를 반환합니다.
- A/B와 B/A의 출력은 모두 `'A'`이지만, 후보 순서를 바꾸었을 때 `'A'`가 가리키는 실제 답은 달라집니다.
- 노트북은 56행에서 `같은 답을 가리키는가: False`를 상수로 출력합니다. 후보 ID로 승자를 다시 변환하거나 비교하지 않습니다.

**영향**

출력 결론은 예시의 의도와 맞더라도, 순서 교환 뒤 같은 실제 후보가 이겼는지 계산으로 증명하지 않습니다. 학생은 A/B 레이블과 후보 정체성을 혼동할 수 있습니다.

**수정 및 재확인**

후보에 고정 ID(`short`, `long`)를 주고, 각 순서의 winner 레이블을 해당 ID로 역매핑해 `winner_ab != winner_ba`를 계산합니다. 규칙 기반 의도적 나쁜 judge라는 현재 범위와 특정 모델의 편향률이 아니라는 한계는 유지합니다. 출력에서 A/B와 B/A의 실제 winner ID가 서로 다른지 확인합니다.

### T3 — 높음: 04 노트북이 문법 오류로 실행되지 않습니다

**근거**

- `04-제시-라벨과-일치율.ipynb`의 labels 목록 끝에 Python 문법에 없는 `+]`가 있습니다.
- 저장된 `04-제시-라벨과-일치율.failure.json`은 Cell 5의 `SyntaxError`를 기록하며, 현재 노트북에는 실행 출력이 없습니다.

**영향**

본문이 설명하는 여섯 제시 라벨, 일치율 0.833, 혼동 행렬을 재현할 수 없습니다. 사람 라벨이 아닌 작성자 제시 라벨이라는 설명 자체는 적절하지만 계산 근거가 없습니다.

**수정 및 재확인**

불필요한 `+`를 제거하고 빈 커널에서 실행합니다. `사례 수: 6`, 정확 일치율 `0.833`, `TP/TN/FP/FN`과 “교육용 작성자 기준” 표시가 함께 나오는지 확인합니다. 이는 사람 검토 결과나 운영 judge 정확도로 표시하지 않습니다.

### T4 — 중간: Batch의 `custom_id`는 입력에서만 검사하며 결과를 원래 사례에 연결하지 않습니다

**근거**

- `08-Batch-평가-입력.ipynb` 51~60행은 `judge-{qid}` custom_id를 JSONL 입력에 만듭니다.
- 68~77행은 JSON 구문·ID 유일성·method·endpoint·body만 검증합니다. 결과 JSONL을 읽어 custom_id로 case를 찾는 코드는 없습니다.
- `_src/08-Batch-평가-입력.html`은 custom_id가 비동기 결과를 원래 사례와 연결한다고 설명합니다.

**영향**

입력 스키마 검증은 맞지만, 학습 목표인 결과-사례 연결을 실행으로 보여 주지 못합니다. 실제 cloud Batch를 실행하지 않는 범위는 유지할 수 있습니다.

**수정 및 재확인**

실제 API 결과라고 주장하지 않는 작은 모의 결과 JSONL을 추가해 `custom_id → qid → case` 매핑을 검증합니다. 입력 custom_id와 결과 custom_id의 집합 차이(누락·중복·알 수 없는 ID)를 출력합니다. cloud 업로드·완료·청구는 계속 미실행으로 표시합니다.

## 최종 실행 뒤 확인할 항목

- 04~08을 빈 커널에서 실행하고, 05의 TTFT=첫 토큰 시각−generate 시작, total=trace 종료−시작이라는 정의와 cache read/creation의 별도 필드를 출력으로 확인합니다.
- 06은 표본 수 100을 분모로 한 nearest-rank p50/p95/p99임을 출력에 남깁니다. 비용 원자료가 합성값이므로 OpenAI 실제 가격이나 청구액이라고 부르지 않습니다. 실제 단가 기반 계산을 추가하는 경우에만 확인 날짜가 있는 공식 가격 출처와 입력·출력·캐시 토큰별 산식을 함께 둡니다.
- 07은 Before/current/fixed가 같은 QID 집합인지, 사례별 품질 기준과 p95 total·p99 비용이 모두 게이트에 들어가는지 확인합니다. 교육용 고정 입력의 실패를 실제 API 실패로 표시하지 않습니다.
- 08은 OpenAI Batch 요청 스키마의 POST·`/v1/responses`·model·input 검증 및 custom_id 유일성은 적절합니다. 정적 입력 검증은 서버 수락·Batch 완료·50% 실제 할인 청구의 증거가 아닙니다. [OpenAI Batch API](https://developers.openai.com/api/reference/resources/batches)

## 2026-09-10 재검

T1~T4의 수정과 저장 출력 재확인을 마쳤습니다. 이 재검은 기술·실행 근거만 다루며 본문 언어·도식 검토를 대신하지 않습니다.

- **T1 Correctness 입력: 확인됨.** 세 사례에 `reference_answer`와 `reference_kind: 교육용 작성자 기준`이 추가됐습니다. 02는 Q002에서 Correctness의 `response` 대 `reference_answer`, Relevance의 `response` 대 `question`, Groundedness의 저장 judge 원문, Retrieval relevance의 `context` 대 `question`을 분리해 출력합니다. 단어 겹침은 교육용 근사이며 사람 라벨이나 운영 점수로 설명하지 않습니다.
- **T2 순서 편향: 확인됨.** 03은 `short`·`long` 고정 후보 ID를 사용하고 첫 후보를 선택하는 의도적 나쁜 judge를 A/B와 B/A 순서에 적용합니다. 저장 출력은 실제 winner가 `short`, `long`으로 달라지고 “같은 후보인가: False”가 계산 결과임을 보입니다. 특정 상용 모델의 편향률이라는 주장은 없습니다.
- **T3 제시 라벨: 확인됨.** 04의 문법 오류가 제거됐고, 새 커널 출력은 사례 수 6, 정확 일치율 0.833, `TP=3/TN=2/FP=1/FN=0`을 보여 줍니다. 출력과 본문 모두 교육용 작성자 기준이며 인간 평가가 아니라고 표시합니다.
- **T4 Batch 결과 연결 검증: 확인됨.** 08은 JSONL 요청의 custom_id 유일성·POST·`/v1/responses`·필수 body를 검증한 뒤, 모의 결과의 누락 `judge-Q090`, 알 수 없는 ID `judge-UNKNOWN`, 중복 `judge-Q006`을 출력합니다. 이 모의 결과 검증은 실제 cloud 업로드·완료·할인 청구와 구별돼 있습니다.
