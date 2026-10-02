# Ch 12 검색 품질과 튜닝 — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part3/ch12-retrieval-tuning` 01~13절(01~12 품질 개선 + 13 챕터 끝 실습 절 신설), 노트북 `labs/part3/ch12-retrieval-tuning/notebooks/01~13-*.ipynb`.
- 기간: 2026-09-18(01~12절) + 2026-09-19(13 실습 절·검토 1차 반영·챕터 마감). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 12절 합계 **557**(절별 42·47·41·53·58·66·33·39·25·31·28·94, 통과 0/12) → 반영 뒤 **13/13 PASS, G1~G7 0**(`gates-after.json`).
- 코드 셀 31·39·51·28·30·31·37·33·32·31·31·54·31 = **459** → **§2-7 리팩터(2026-09-21)로 24·31·39·24·19·20·24·21·23·22·22·38·23 = 330**(코드 줄 3658 → 2669, −27.0%, 도구 파일 `rag_tools.py` 220줄 별도, §18), 검사 문장 291·350·406·303·307·331·380·341·306·309·316·424·341, Mermaid **51장**(01~12 각 4장 + 13절 3장), 삽화 **13장**(절마다 1장, 모두 채택), 복습 문제는 HTML에만.
- 서비스 요청: 절마다 임베딩 9·9·9·**0**·9·9·16·16·16·16·21·31·3번, 답을 쓰는 모델 0·0·0·0·0·0·0·0·0·0·**10**·**1**·**2**번, 로컬 리랭커 0·0·0·0·0·0·**17**·**30**·0·0·0·0·0번. 챕터 전체가 미화 0.1달러 아래입니다.
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md`(Part 1·2) → Ch 9 요약 → Ch 10 요약 → Ch 11 요약 → **이 문서**. 절 사이 세부는 `handoff.md`(1,100여 행), 절별 기록은 `NN-diagnosis.md`, 검토와 반영은 `review-round1-A.md`(§01~07)·`review-round1-B.md`(§08~13)입니다.

## 1. 자료가 두 벌입니다 (core 벌 / advanced 벌) — 가장 먼저 알아야 할 것

| | core 벌 (01~06절) | advanced 벌 (07~13절) |
|---|---|---|
| 문서 | `data/core-documents.json` 교육용 문서 **12개** | `data/advanced-documents.json` 공개 PDF **6건**에서 만든 **문서 청크 175개**(부모 6건) |
| 질문 | `data/core-queries.json` **8개**(`C01`~`C08`), 정답이 문서 ID 글 하나 | `data/advanced-queries.json` **30개**(Ch 11 평가셋 복제본), 개발 15 / 시험 15, 정답이 부모 문서 ID **목록** |
| 후보 단위 | 문서 | 문서 청크 |
| 정답 단위 | 문서 | **부모 문서**(`parent_ids_of()`로 바꾼 뒤 지표를 잽니다) |
| 자르는 자리 | 1·2·3 | 재현율 자리 3 · 문서 청크 정밀도 자리 5 |
| 지표 | 재현율만 | 재현율·문서 청크 정밀도·(12절만) 정밀도·nDCG |

- **두 벌의 숫자를 나란히 놓지 않습니다.** 07 b3이 「이 절부터 자료가 바뀝니다 … 앞 절 숫자와 이 절 숫자를 나란히 놓지 않습니다」로 가르고, 07~13절 b7에 같은 항목이 있습니다.
- **Ch 11 개발 15문항 값(`0.867`·`0.173`·`0.751`)과도 나란히 놓지 않습니다.** 01 b7에 한 번만 적고 02~13절에서 되풀이하지 않습니다.
- `advanced-queries.json`은 Ch 11 `evaluation-queries.jsonl` 30문항의 독립 실행용 복제본이고, 12절이 실행 중에 두 파일이 같은지 확인합니다(`Ch 11 원본 질문 줄 수: 30`·`이 챕터 복제본과 같은가: True`).

## 2. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 라이브러리·API | 새로 만든 함수 | 새 용어 |
|---|---|---|---|
| 01 | `OpenAIEmbeddings(model=, dimensions=256)`·`embed_documents`·`embed_query`, NumPy `np.array`·`@`·`np.linalg.norm(axis=1)`·`np.argsort`·`shape`(§2-7 리팩터로 바뀜 — 전에는 `math.sqrt`) | `cosine_distance` · `l2_distance` · `measure_all` · `rank_by_distance` · `score_one`(§2-7 리팩터로 바뀜 — 전에는 `dot_product`·`vector_length`·`cosine_similarity`도 적었음. 이제 `@`·`np.linalg.norm`이 대신하고 `cosine_similarity`는 Ch 5 02절 NumPy 판을 도구 파일에서 가져옴) | L2 거리 · 코사인 거리 · 정확 검색 · 근사 검색 · 단위 길이 벡터 (5) |
| 02 | `psycopg.connect(autocommit=True)`·`cursor()`·`execute`·`fetchall`, `CREATE EXTENSION vector`, `vector(256)`·`halfvec`, `<=>`, `CREATE INDEX … USING hnsw`, `EXPLAIN`, `set_config()` | `run_search` · `print_hits` · `find_scan_line` · `set_seqscan` · `try_hnsw_index` | 벡터 데이터베이스 · 색인 · HNSW · 후보 목록 크기 · 계획 줄 · 순차 스캔 · 색인 스캔 · 차원 한도 (8) |
| 03 | 조건이 붙은 SQL, `hnsw.iterative_scan`(`off`·`strict_order`·`relaxed_order`), `hnsw.max_scan_tuples` | `find_category` · `make_filler_vectors` · `rank_in_category` · `run_filtered_search` · `set_iterative_scan` · `pick_hits` | 메타데이터 필터 · 나중 걸러 내기 · 선택도 · 반복 탐색 · 채움 행 (5) |
| 04 | `Kiwi()`·`tokenize`·`token.form`·`token.tag`, `BM25Okapi`·`get_scores`·`corpus_size`·`avgdl` | `kiwi_terms` · `count_docs_with` · `terms_by_policy` · `rank_by_bm25` · `print_scores` | 형태소 · 형태소 분석기 · 품사 표시 · 검색 낱말 · 낱말 정책 · BM25 · 낱말 겹침 검색 (7) |
| 05 | 새 라이브러리 0개(01·04절 함수를 한 노트북에서 함께 씀) | `print_ranked`(값 칸 이름을 인자로 받음) | 벡터 거리 검색 · 말 바꾼 질문 · 낱말 일치 · 점수 방향 (4) |
| 06 | 새 라이브러리 0개 | `fuse_scores` · `fuse_rank` | 순위 합치기 · 합친 점수 · 순위 상수 · 가중치 · 하이브리드 검색 (5) |
| 07 | `CrossEncoder(revision=, max_length=, device=)`·`predict()`·`.tolist()` | `unique_chunk_ids`(§2-7부터 도구 파일의 문서 청크 판을 가져옴) · `parent_ids_of` · `make_pairs` · `rerank` | 1차 검색 · 리랭킹 · 교차 인코더 · 리랭킹 점수 · 부모 문서 (5) |
| 08 | 같은 `CrossEncoder`를 **모델 두 개**로 | `eligible_items` · `score_candidates` · `order_by_score` · `chunk_precision_at` · `evaluate` | 후보 수 · 보고 자리 · 문서 청크 정밀도 (3) |
| 09 | `tiktoken.get_encoding("o200k_base")`·`encode()`(Ch 8 01절과 같은 이름·같은 식) | `count_tokens`(§2-7부터 Ch 8·9·10 도구 파일 판 `count_tokens(encoding, text)`을 가져옴) · `total_tokens` · `parent_texts_of` · `summarize` | 부모 문서 넘기기 · 넘길 부모 수 · 입력 가용분 (3) |
| 10 | 새 라이브러리 0개 | `similarity_to_chosen` · `mmr_score` · `best_candidate` · `mmr` · `mmr_pick` · `mmr_row` | 최대 주변 관련성 · 관련성 비중 · 고유 부모 수 (3) |
| 11 | `init_chat_model`(Ch 6~9와 같은 모양, `gpt-5.4-mini`·`temperature=0`) | `ranking_lists` · `candidates_of` · `measure` · `rewrite_question` · `branch_row` | 질문 재작성 · 독립 질문 · 대화 기록 (3) |
| 12 | `hashlib.sha256`·`time.strftime`·파일 쓰기(`write_text`) | `file_fingerprint` · `write_text` · `question_lists` · `metrics` · `top_results_of` · `metric_summary` · `result_row` · `slice_summary` · `evaluate_item` · `evaluate_config` · `log_row` · `knob_mean` · `print_knob_rows`, 그리고 Ch 11 04절 `rank_weight`·`dcg_at`·`ideal_dcg`·`ndcg_at`와 03절 `precision_at`을 **이 챕터에서 처음** 다시 씀(§2-7부터 Ch 11 도구 파일 판을 Ch 12 도구 파일에서 가져옴) | 손잡이 · 설정 한 벌 · 입력 지문 · 실험 기록 한 줄 (4) |
| 13 실습 | **새 API·새 문법 0개** | `print_rows` · `column_mean` · `context_of` · `score_row` · `run_weights` | 0 |

- 새 용어 합계 **55개**.
- **쓰지 않은 Python 이름(열세 절 모두 0건, AST 확인)**: `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`try`·`+=`·세미콜론·한 줄 복합문·f-string·타입힌트·기본값 매개변수·셀당 함수 둘, 그리고 이름 `numpy`·`np`(**§2-7 리팩터로 바뀜**: 01절이 `np.array`·`np.linalg.norm(axis=1)`·`np.argsort`·`np.round`·`shape`·`tolist`를 쓰고 01~13절이 NumPy를 쓰는 도구 파일에서 함수를 가져옴 — 07~13절 노트북은 NumPy 이름을 직접 쓰지 않음)·`sklearn`·`TfidfVectorizer`·`set`·`next`·`enumerate`·`zip`·`sum`·`max`·`min`·`any`·`all`·`isinstance`·`Counter`·`re`·`Path`·`float`·`key=`·`reverse=`·`목록.index`·`목록.remove`. 호출한 내장 이름은 `len`·`print`·`open`·`range`·`round`·`str`·`sorted`뿐입니다.
- `raise`는 08절 `evaluate`와 12절 `evaluate_config` 두 곳뿐이고 둘 다 실습 폴더 테스트가 요구합니다. `assert`는 코드가 정하는 값에만 걸었고 **모델 답에 건 `assert`는 0건**입니다.
- 주석·빈 줄을 뺀 셀 최대 줄 수는 15(규격 §2-4 상한)이고, 함수 본문 10줄을 넘긴 곳은 **두 군데**입니다: 08절 `evaluate` **11줄**, 10절 `mmr_row` **13줄**. 둘 다 까닭과 함께 진단에 적은 **기록된 예외**입니다(§12).

## 3. 절 사이에 그대로 이어 쓴 함수와 준비 셀 묶기

- **거리 네 개**(`dot_product`·`vector_length`·`cosine_similarity`·`cosine_distance`)는 01·02·03·05·06·07·08·09·10·11·12·13절이 **글자까지 같은 코드**였습니다. Ch 9 03절 함수 세 개에서 이어받았습니다. **§2-7 리팩터(2026-09-21)로 바뀜**: 도구 파일 `labs/part3/ch12-retrieval-tuning/notebooks/rag_tools.py`의 `cosine_similarity`(Ch 5 02절 NumPy 식)·`cosine_distance`(01절, 값 1을 함수 안에서 정함) 두 개만 남고 노트북에는 다시 적지 않습니다(`dot_product`·`vector_length`는 `@`·`np.linalg.norm`이 대신).
- **순위 두 개**(`rank_by_distance` 값 칸 `거리` / `rank_by_bm25` 값 칸 `점수`)와 **합치기 두 개**(`fuse_scores`·`fuse_rank`, 순위 상수 60)는 05~13절이 같은 코드였습니다. **1차 검색 = 두 순위를 `fuse_rank()`로 합친 앞 여덟 개**가 07~13절의 공통 약속입니다. **§2-7 리팩터로 바뀜**: 도구 파일 판 `rank_by_distance(question_vector, doc_vectors, doc_ids, top_count)`·`rank_by_bm25(bm25_model, question_terms, doc_ids, top_count)`(칸 `doc_id`, 01~06절)와 문서 청크 판 `rank_chunks_by_distance(question_vector, chunk_vectors, chunk_ids, top_count)`·`rank_chunks_by_bm25(bm25_model, question_terms, chunk_ids, top_count)`(칸 `chunk_id`, 07~13절), `fuse_rank(ranking_list, weight_list, rank_constant)`를 가져옵니다.
- **지표 함수**는 Ch 11에서 이어받았습니다: `unique_doc_ids`(07절부터 `unique_chunk_ids`)·`find_gold_rank`·`recall_at`·`mean_score`, 08절이 더한 `chunk_precision_at`, 12절이 되살린 `precision_at`·`rank_weight`·`dcg_at`·`ideal_dcg`·`ndcg_at`. **자르기는 함수 안에서** 합니다.
- **준비 셀 묶기**(09절이 시작, 10~13절이 이음 — **§2-7 리팩터로 없어짐**: 앞 절 함수는 준비 셀 한 줄 `from rag_tools import …`로 가져옵니다): 앞 절에서 이미 읽은 함수는 셀 하나에 여러 개를 담고 `metadata`에 `lesson_role="setup"` + `upgrade_allow=["multiple_defs_in_cell"]`를 붙입니다. 09절 함수 12개 → 준비 셀 8개, 10절 13개 → 9개, 11절 14개 → 9개, 12절 **24개 → 16개**, 13절 13개 → 8개. 이 방법이 없으면 12절 코드 셀이 70개를 넘습니다.
- 새 절을 쓸 때 이 함수들은 **도구 파일에서 가져오세요**(§2-7, 리팩터 전 문장 「같은 코드로 다시 정의하세요」를 대신함). 이름이나 인자 모양을 바꾸면 절 사이 표를 견줄 수 없고 실습 폴더 테스트가 멈춥니다. 뒤 챕터(실습 폴더가 다름)는 자기 도구 파일에 같은 본문으로 옮기고 「Ch 12 NN절에서 배웠습니다」를 답니다.

## 4. 12절 기록 계약 (뒤 챕터가 읽는 파일 — 꼭 먼저 읽을 것)

12절이 `labs/part3/ch12-retrieval-tuning/runs/`에 세 파일을 쓰고, 같은 내용을 `runs/continuity/20260918T232052/`에 사본으로 둡니다. **§2-7 리팩터 재실행(2026-09-21)으로 바뀜**: 지금 정본과 같은 사본은 `runs/continuity/20260921T082024/`이고 옛 사본 폴더도 모두 남아 있습니다.

| 파일 | 내용 | 해시(2026-09-19) |
|---|---|---|
| `advanced-continuity-experiment-log.jsonl` | 개발 36줄(설정 한 벌 = 한 줄), 한 줄 **17칸**, `settings` **7칸**, 질문별 `results` **15줄**, 갈래 세 개(`easy`·`medium`·`hard`) | `9b447a417c3ed9ec…` → §2-7 리팩터로 바뀜 `f16aa3587b2bdb11…` |
| `advanced-continuity-test-result.json` | 고른 설정으로 시험 15문항 **한 번**, `selected_run_id`·`comparison_policy` | `f9b16717d910d861…` → §2-7 리팩터로 바뀜 `7b9b9db75a3986f6…`(`run_id`·`selected_run_id`·`run_date` 말고 내용 같음) |
| `advanced-continuity-integrated-result.json` | 검색부터 답까지 이은 **스모크 1건**(`run_type: generation_smoke_test`, 질문 `Q002`), `retrieval_metrics`는 `None` | `ce76d3d8e3139d16…` → §2-7 리팩터로 바뀜 `7b142cd570aa8a4f…`(`run_id` 말고 내용 같음) |

- **`metrics` 칸 여섯 개**: `recall_at_3`·`recall_at_5`·`recall_at_50`·`precision_at_5`·`ndcg_at_5`·`chunk_precision_at_5`. 지표는 **반올림하지 않고** 저장합니다(`0.20000000000000004`).
- **`settings`**: `input`·`dense`(`text-embedding-3-small`)·`sparse`(`Kiwi+BM25`)·`fusion`(`RRF(k=60)`)·`weights` `[0.0, 1.0]`·`relevance_weight` `1.0`·**`reranker` `null`**·`context_selection` `matched-chunk-text`·**`chat` `gpt-5.4-mini`**·**`dimensions` `256`**.
- **읽는 쪽 다섯 곳**(모두 소스를 열어 확인했습니다):
  1. 실습 폴더 `tests/test_continuity.py` 61~129행 — 36줄·칸 이름·`dimensions == 256`·`chat == "gpt-5.4-mini"`·`chunk_id`가 `{doc_id}-P{page:02d}-`로 시작·사본 일치. **4 passed**.
  2. `textbook/part3/qa/check_continuity.py` 81~137행 — 네 칸(`recall_at_5`·`recall_at_50`·`precision_at_5`·`ndcg_at_5`)을 질문마다 **다시 계산해** `abs_tol=1e-10`으로 대조 + 갈래 평균.
  3. `textbook/qa/check_course_continuity.py` 115~180행 + **219행**(`dimensions == 256`·`chat == 'gpt-5.4-mini'`).
  4. `textbook/part4/ch13-langgraph-basics/qa/author_ch13.py` — 통합 기록의 `question`과 `retrieved[].doc_id`를 읽어 출력만 합니다(멈추지 않음). → §13 인계.
  5. `textbook/part4/ch15-evaluation-advanced/_author.py` 210~212행 — 36줄의 `response` 칸 유무(**0**, 의도대로)와 시험 기록의 `ndcg_at_5 < 1`인 줄 수. → **§13 인계(깨짐)**.
- **다시 계산되는 칸은 네 개뿐**입니다. 12절이 더한 `recall_at_3`·`chunk_precision_at_5`는 검사가 다시 계산하지 않습니다. 하필 **고르는 칸으로 쓴 것이 `chunk_precision_at_5`**라 12 b7에 그 사실을 적었습니다.
- **칸 이름과 계산을 바꾸지 마세요.** 바꾸면 위 세 검사가 멈춥니다. 값은 다시 실행하면 바뀔 수 있고, 그때는 **읽는 쪽 코드의 알려진 실패를 챕터 요약·진행표에 적어야 합니다**(이번에 Ch 15가 그 사례입니다).

## 5. pgvector 실행 방법 (01~03절, 작업 환경과 학생 환경이 다름)

- **교재 본문은 학생 기준(Docker)을 그대로 씁니다**: `pgvector/pgvector:0.8.2-pg17` 이미지, 컨테이너 `hankyung-part3-pgvector`, 접속 `postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab`, 표 `ch12_core_hnsw`·`ch12_core_filter`.
- **작업 VM에는 Docker가 없습니다.** conda-forge PostgreSQL을 `$ROOT/.cache/vm/pgenv`(데이터 `$ROOT/.cache/vm/pgdata`)에 두고 같은 접속 정보로 띄웁니다. `run_section.sh`가 절 실행 직전에 `qa/upgrade/pre_exec.sh`를 source 하고, 그 스크립트가 `pg_ctl start` 뒤 `SELECT 1`로 열 번까지 기다립니다. **기기 셸은 호출이 끝나면 서버도 꺼지므로 절 실행마다 다시 켜집니다.**
- 교재 출력의 판 번호는 **PostgreSQL 17.11 · pgvector 0.8.1**입니다(`pre_exec.sh` 주석의 17.4는 처음 설치 판이고 실제 출력은 17.11). 본문 판 번호 갈래는 셋입니다: **필수 최소 0.7.0 / 교재 출력 17.11 + 0.8.1 / 공식 문서 v0.8.6**. 02·03절 b7에 「실습 폴더 안내의 이미지에서는 0.8.2이고 **이번 교재 출력은 그 환경에서 만들지 않았습니다**」를 적었습니다.
- 03절은 이 챕터에서 **유일한 `paired` 절**입니다(Before = 반복 탐색 `off`로 받아 온 줄 수 0, After = `strict_order`로 3).

## 6. 리랭커 두 개 (07·08절, 로컬 모델 — 메모리 주의)

| 이름 | 판 번호(revision) | 파일 크기 | 쓰는 절 | 메모리 |
|---|---|---|---|---|
| `BAAI/bge-reranker-v2-m3` | `953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e` | 약 **2.2GB** | 07(호출 17번)·08(리랭커 A) | 07절 최대 RSS **약 3.1GB**(3.8GB VM) |
| `Dongjin-kr/ko-reranker` | `8c2ab1a833734491…` | 약 1.1GB | 08(리랭커 B) | 08절은 **한 모델씩 올렸다 내려** 최대 RSS **2.76GB** |

- 둘 다 `max_length=256`·`device="cpu"`이고 **판 번호를 고정해** 받습니다. 점수는 0과 1 사이 값이라 「로짓」이 아니라 **「리랭킹 점수」**로 부르고 확률로 읽지 않습니다(설치판 소스 `cross_encoder/model.py` `get_default_activation_fn()` 확인).
- 08절 표·그림의 칸 이름은 **A·B**입니다. 모델 이름으로 우열을 말하지 않습니다.
- 07·08절 준비물과 실습 폴더 `README.md`에 **「메모리 약 3GB, 다른 프로그램을 닫고 실행」**을 적었습니다.
- 12·13절은 리랭커를 **부르지 않습니다**(36벌 × 15문항이면 리랭킹 540번, 통합 실행에만 넣으면 고른 설정과 돈 설정이 달라짐). 계약 파일의 `settings.reranker`는 `null`입니다.

## 7. 천장에 닿은 지표와 「가를 수 없다」 규칙

이 챕터의 advanced 벌에서는 **부모 문서가 6건뿐**이고 1차 후보가 이미 정답 부모를 앞자리에 두어 여러 지표가 최댓값에 붙습니다.

| 천장 | 어디서 | 값 |
|---|---|---|
| 부모 문서 재현율 자리 1·2·3 | 07절 두 단계 서른 줄 | 모두 `1.0` |
| 부모 문서 재현율 자리 3 | 08절 아홉 줄 · 09절 · 10절 여섯 줄 · 11절 다섯 줄 · 12절 36줄 · 13절 네 줄 | 모두 `1.0` |
| 부모 문서 정밀도 자리 5 | 12절 36줄 | 모두 `0.2`(정답 부모가 한 건이라 최댓값) |
| 재현율 자리 5·50 | 12절 36줄 | 모두 `1.0` |

- **규칙**: 천장에 닿은 지표도 **표에서 빼지 않고 값 그대로 싣고**, 「이 조건에서는 가를 수 없다」를 b6·b7·복습에 적습니다(Ch 11 요약 §3에서 이어받음).
- **가르는 값을 따로 냅니다**: 08절이 **세는 단위를 문서 청크로 바꿔**(문서 청크 정밀도 자리 5) 천장을 풀었고, 09절은 고유 부모 수·조각 수·입력 가용분에 든 질문 수, 10절은 고유 부모 수, 12절은 `chunk_precision_at_5`와 `ndcg_at_5`를 썼습니다.
- **「합치면 좋아진다」·「어느 방법이 낫다」를 쓰지 않습니다.** 06절은 「합친 값이 두 방법보다 높은 자리는 없었습니다」, 07절은 「이 자료에서 리랭킹이 재현율을 올리지 못했다」까지만, 08절은 「어느 리랭커가 낫다고 말하지 않음」으로 닫았습니다.

## 8. 실행마다 흔들리는 값 (그림 라벨·정리에서 뺀 것)

같은 글을 보내도 임베딩 값이 호출마다 아주 조금 달라집니다. 07~13절 b7에 같은 문장이 있습니다(08절은 검토 반영으로 추가).

| 흔들린 값 | 본 자리 | 처리 |
|---|---|---|
| 거리 소수 셋째 자리 아래 | 01·02·03·05·06절 | 소수 둘째 자리까지만 출력하고 그림 라벨에서 뺌 |
| 반복 탐색을 켠 여러 질문의 받아 온 줄 수(0~3) | 03절 | 표·그림·결론에서 빼고 첫 질문 하나만 실음, b7에 「이번에 실행하지 않았습니다」 |
| 문서 청크 정밀도 자리 5 `0.84` ↔ `0.853` | 08·09절 | 값은 표에 싣고 b7에 흔들림을 적음 |
| 문서 청크 다섯 개의 조각 수 평균 **600 ↔ 596** | 09절 | **그림 `09-1` 라벨·캡션·정리에서 뺐습니다**(마감). `09-3` 막대 값은 막대를 그리는 데이터라 그대로 두고 alt에서만 뺐습니다(§2-7 재실행 두 번은 모두 600이라 막대를 `600`으로 맞춤) |
| 부모 문서 두 건의 조각 수 평균 **4206 ↔ 4213** | 09절(§2-7 재실행에서 처음 흔들림) | 그림 `09-1`·`09-4` 라벨·`09-1` 캡션·정리·b6 본문을 「약 4200」·「4200을 넘었습니다」로 바꾸고 다시 렌더. 결과 읽기·b5 「확인할 점」은 출력 그대로 `4206`, b7에 `4213`을 적음. `09-3` 막대 데이터는 `4206` |
| 비중 0.5의 정밀도 소수 둘째 자리 0.01쯤 | 10절 | 열다섯 질문 평균은 그림 라벨에 넣지 않음 |
| 「기록 없이 재작성문」 정밀도 `0.72` ↔ `0.76` | 11절 | 그림 라벨과 정리 세 줄에서 뺌 |
| 손잡이별 평균의 문서 청크 정밀도 소수 셋째 자리 | 12절 | 그림 라벨·정리에는 네 번 실행에서 모두 같았던 값만 넣음 |

- **기준**: 흔들리는 값은 **본문 표와 「확인할 점」에는 출력 그대로 싣고**(학생이 자기 출력과 맞춰 볼 자리), **그림 라벨·캡션·정리 세 줄에서는 뺍니다**. 09절만 기준이 달랐고 마감에서 맞췄습니다.
- 흔들리지 **않은** 값: 부모 쪽 조각 수(`2502`·`1913`·`1799`·`3712`, `4206`은 §2-7 재실행에서 흔들림 — 위 표)·입력 가용분 `3400`·고유 부모 수·재현율·정답 자리·모델이 쓴 답 문장(13절은 두 번 실행에서 글자까지 같았음).

## 9. 반복해 쓴 데이터·이름·비유

- **core 벌 문서 ID**: `LIB-001`~`LIB-004`·`FAC-*`·`ACC-*`·`OTH-*`, 질문 `C01`~`C08`. 자주 나오는 상위 세 개는 `LIB-004`·`LIB-001`·`LIB-003`(01·02·03절에서 같은 값).
- **advanced 벌**: 부모 `E01`(도서관 안내)·`E02`·`M01`·`M02`·`H01`(공급 계약서)·`H02`, 문서 청크 ID `E01-P03-C01` 모양(`{부모}-P{쪽:02d}-C{번호}`), 예로 자주 쓴 질문 `Q002`(대출 권수·기간)·`Q085`(지체상금).
- **비유**: 01 쪽지와 열두 권 · 02 서가와 끈 · 03 끈과 빈 쟁반 · 04 꼬리를 떼어 맞춘 단추 · 05 비슷한 색과 똑같은 무늬 · 06 두 줄에서 받은 몫 · 07 쪽지와 여덟 권 · 08 쟁반 다섯 칸 · 09 카드 다섯 장과 책 두 권 · 10 같은 과일과 섞인 과일 · 11 구멍 난 쪽지와 **네모 딱지** · 12 연습 자물쇠와 봉한 상자 · 13 두 관과 깔때기.
- **용어 규칙**: 「자」 = 거리 재는 방법, 한정어 없는 「청크」 금지(늘 **「문서 청크」**), **「조각」은 Ch 5 토큰 뜻 전용**(09절 34곳), 「유클리드 거리」 대신 **L2 거리**, 「λ」·`lambda_mult` 대신 **「관련성 비중」**(`relevance_weight`, LangChain 이름은 b4 용어 표와 b10에 괄호로만), `k` 대신 `pick_count`, 「LIMIT보다 적게」 대신 「받아 올 줄 수보다 적게」.
- **쓰지 않기로 한 말**: 「임계값」·「쉽게」·「간단히」·「당연히」·「한 겹 더」·「인덱스」·「컬럼」·「쿼리」·「토큰화」·「원점수」·「정규화」·「검색기」·「포화」·「로짓」·「레이턴시」·「하이퍼파라미터」·「그리드 서치」·「오버피팅」·「베이스라인」·「청킹」·「오버랩」·「자식 청크」·「강사 시연」·「개선 전」·`Recall@`·`nDCG@`·`top-k`·`TF-IDF`.

## 10. 13절 실습 절 주제와 결과

- 제목 「**검색 품질 실습: 가중치 하나를 바꿔 답까지 보기**」, `format: experiment`, meta 「실습 30분」(챕터 시수에 더하지 않음).
- 05절 순위 둘 → 06절 가중치로 합치기 → 08절 보고 자리와 두 지표 → 12절 답 쓰기를 **한 줄기**로 잇고, 12절 손잡이 가운데 하나인 **06절 가중치 한 자리**만 바꿔 두 번 실행합니다.
- 결과: 실행 1 `[1.0, 1.0]` → `Q002` 정밀도 자리 5 `1.0`·두 질문 평균 `1.0`, 답에 권수와 기간이 모두 있음. 실행 2 `[1.0, 0.0]` → `Q002` 정밀도 `0.4`·평균 `0.7`, 보고 자리 다섯 가운데 셋이 `E02`로 바뀌고 답은 「자료에서 찾지 못했다」. 재현율 자리 3은 네 줄 모두 `1.0`이라 가를 수 없습니다.
- 서비스 요청 **다섯 번**(임베딩 3 + 답 모델 2), 실행 1분 안팎, **파일을 쓰지 않습니다**. pgvector(Docker)·리랭커(메모리·시간)·MMR(셀 수)은 뺐습니다.

## 11. 챕터 밖 수정 (전부 목록)

- `textbook/part3/_build_index.py` — **27행** ch12 절 수 `12` → `13`(13절 신설). 마감에서 **47행**(학생 묶음 `시작하기.md`의 「TF-IDF와 MMR … 36건」) · **81행**(「Ch 9–12 · 32절」 → **36절**) · **88행**(Part 3 목차의 「Ch12의 36건은 TF-IDF와 MMR 설정 비교」)을 「RRF 가중치와 MMR 관련성 비중」으로 고쳤습니다. 이 스크립트를 돌리면 **Part 3 목차와 `textbook/downloads/part3-practice.zip`이 함께 다시 만들어집니다**(`Part 3: 36 verified sections`, **92항목**).
- `textbook/part3/qa/check_delivery.py` — 112~113행 `len(notebooks) == 35` → **36**, `quizzes >= 35*3` → `36*3`. 끝까지 통과합니다(같은 실행이 `delivery-results.json`을 새로 씁니다).
- `textbook/part3/qa/finalize_continuity_evidence.py` — **주석만** 사실대로 고쳤습니다(ch09 14 · ch12 **28** · 지금 합 **94**). **기대값 `assert len(visual) == 94`는 그대로**이고, 「ch09를 다시 찍어 16이 되면 96으로 올린다」와 전체 마감 순서 여섯 단계를 같은 주석에 적었습니다.
- `textbook/_notebook/checks/ch12-retrieval-tuning/visual-results.json` — 26행 → **28행**(14쪽 × 두 폭, 28/28 PASS). 스크린숏 네 장도 새로 찍었습니다.
- `labs/part3/ch12-retrieval-tuning/README.md` — 13절 한 단락 추가 + 마감에서 **다섯 문장**(36건 손잡이·통합 기록 설명·CrossEncoder 쓰는 절·11절 모델 이름·API 키가 필요한 절)과 07·08절 메모리 문장.
- `labs/part3/ch12-retrieval-tuning/tests/test_continuity.py` — 08·10·12절 블록의 불러오기 방식(`load_notebook_namespace()`)과 넣는 값을 고쳤습니다. **확인을 약화시키지 않았고 08·12절은 오히려 확인이 늘었습니다**(검토 B가 개선 전 계약과 하나씩 대조해 확인).
- `chapter.json` — 13절 추가(시수는 더하지 않음)와 `objectives` 셋째·넷째·다섯째 줄 수정.
- **고치지 않은 것**: 빌드 도구(공용 `_template/builder.py`로 충분), 묶음 허용 목록(`public-files.json`·`build_bundle.py`), `data/*`, `runs/*`, Ch 9~11 기록, Ch 6~8 사슬, Ch 13·Ch 15 파일.
- **권한 한 문장**: 검토 보고서 두 개의 결정 요청 마흔세 항목은 모두 **권고대로 유지**한 것이고, 강사가 뒤집을 수 있는 항목은 §12(강사 확인 대상)에만 있습니다.

## 12. 강사 확인 대상

- **07·08·09절 실습 시수 1h → 3h**: 이 조정으로 절 meta 합이 강의 12h·실습 28h가 되어 `chapter.json`과 정확히 맞았습니다. 배분 자체가 맞는지는 강사 몫입니다(09절은 코드 셀 32개·실행 6~8초인데 실습 3h).
- **12절 코드 셀 54개·앞 절 함수 24개 재정의**: 절을 나누지 않았습니다. (a) meta 실습 1h를 올릴지, (b) 노트북 5절 머리말에 「준비 셀 열여섯 개는 읽지 말고 실행만」을 더 굵게 적을지.
- **08절 코드 셀 33개·03절 51개**: 규격에 셀 수 상한은 없습니다. 수업 분량 문제로만 봅니다.
- **기록된 함수 예외 두 개**: 08절 `evaluate` 11줄, 10절 `mmr_row` 13줄(규격 §2-2 L2는 10줄). 나누려면 그 절을 다시 실행해야 하고 10절은 다시 실행하면 문서 청크 쪽 값이 흔들립니다.
- **13절 질문 수 2 대 3**: 지금은 질문 두 개(서비스 요청 5번 = 임베딩 3 + 답 모델 2). 셋으로 늘리면 답 모델 3번·임베딩 4번이 되고 값의 폭이 넓어지지만 30분 수업에는 둘이 맞아 보입니다.
- **08절 두 번째 리랭커 `Dongjin-kr/ko-reranker`**: 개선 전 모델을 그대로 두었고 표·그림은 A·B로만 부릅니다.
- **실습 폴더 잠금의 쓰지 않는 패키지**(`pgvector`·`pypdf`, 그리고 테스트만 쓰는 `numpy`·`scikit-learn`): 빼려면 `uv.lock`과 묶음 두 개를 다시 만들어야 해 전체 마감 몫으로 미뤘습니다.
- **본문 값이 바뀐 자리**(개선 전 기록과 다름): 03절 「필터 반환 0개 → 5개」 → 실제 **0 → 3**, 06절 「RRF 7/8」 → 자리 3 재현율 **1.0(8/8)**, 08절 여섯 행이 모두 `1.000`이던 표 → 아홉 행 가운데 다섯 값이 갈림, 12절 36벌 손잡이가 「문자 분석기·n-gram·보고 순위·λ」 → **RRF 가중치 × MMR 관련성 비중**.
- **06절 참고 자료 확인일 2026-09-09**: 이번 개선에서 두 링크를 다시 열지 않아 날짜를 그대로 두었습니다(01~05·07절은 2026-09-18).

## 13. 뒤 챕터 인계 (반드시 처리할 것)

### 13-1. Ch 15 01절 — **지금 깨져 있습니다**

- **무엇이**: `textbook/part4/ch15-evaluation-advanced/_author.py` **212행** `assert len(rows) == 36 and len(low) == 2`가 **실패합니다**.
- **왜**: 211행이 12절 시험 기록에서 `low = [r for r in test['results'] if r['ndcg_at_5'] < 1]`을 뽑는데, **12절을 다시 실행하면서 그 줄 수가 2 → 1로 바뀌었습니다.**
- **현재 값**: `labs/part3/ch12-retrieval-tuning/runs/advanced-continuity-test-result.json`에서 `ndcg_at_5 < 1`인 줄은 **한 개**입니다 — `Q090`, 첫 문서 `H02`, 정답 `['H01']`, `recall_at_5` `1.0`, `ndcg_at_5` `0.6309`. 개선 전에는 두 개였습니다(`Q006` 첫 문서 `E02` · `Q090` 첫 문서 `E02`, 둘 다 `0.6309`).
- **함께 고칠 것**: (1) `_author.py` 212행 기대값 `2` → **`1`**, (2) 배포본 노트북 `labs/part4/ch15-evaluation-advanced/notebooks/01-실패-로그와-평가-대상.ipynb` 셀 7의 저장 출력 **두 줄 → 한 줄**(셀 9에 그 `assert`가 있음), (3) `labs/part4/ch15-evaluation-advanced/data/evaluation-cases.json`의 **`Q006` 선정 근거**(「시험 기록에서 nDCG가 1보다 작은 질문」으로 뽑은 사례인데 이제 그 조건에 맞지 않음).
- **지금 멈추는 공용 검사는 없습니다**(`check_course_continuity.py`는 Ch 15 노트북의 저장된 출력만 보고 다시 실행하지 않습니다). 다만 `part4-practice.zip`·`llm-practice.zip`에 12절 기록 세 파일이 함께 들어가므로 **학생이 한 묶음 안에서 Ch 15 01절을 실행하면 그 자리에서 막힙니다.**
- **Ch 12에서는 고치지 않았습니다**(Ch 15는 아직 「대기」). 루트 진행표 `textbook/qa/upgrade-progress.md` Ch 15 행에도 같은 내용을 적었습니다.

### 13-2. Ch 13 07절 — 낡은 문장(코드는 멈추지 않음)

- `textbook/part4/ch13-langgraph-basics/qa/author_ch13.py` **251행** `prior`와 그 문장이 그대로 들어간 `_src/07-RAG-통합과-시각화.html` **b3**: 「Ch12의 `runs/advanced-continuity-integrated-result.json`에는 Q002 질문, **검색된 E01·E02 쪽**, 실제 모델 응답, 고정 설정이 있습니다」.
- 지금 통합 기록의 `retrieved`는 **`E01-P03-C02`·`E01-P03-C01`·`E01-P03-C06` 세 건(모두 `E01`, 모두 3쪽)**이고, `settings.reranker`는 `null`, `context_selection`은 `matched-chunk-text`입니다. 「쪽」이 아니라 **문서 청크 본문**을 넣습니다.
- Ch 13 작업 때 `prior` 문장과 b3을 지금 값으로 고치세요. 질문 `Q002`와 답이 있다는 사실은 그대로 맞습니다.

### 13-3. Ch 13~15가 이어받을 것(정상)

- 12절 기록 세 파일의 **칸 이름과 계약**(§4). 값이 바뀌면 읽는 쪽 코드를 확인하고 알려진 실패를 요약·진행표에 적습니다.
- **모델 이름 `gpt-5.4-mini`**(11·12·13절)와 **`dimensions=256`**. `check_course_continuity.py` 219행이 두 값을 봅니다.
- **지표 이름과 천장 규칙**(§7), **흔들리는 값 처리 기준**(§8), **용어 규칙**(§9).
- **생성 답 평가는 Ch 15 몫**입니다. 이 챕터는 답이 맞는지 판정하지 않았고 모델 답에 `assert`를 걸지 않았습니다.

## 14. 아직 가르치지 않은 것 (뒤 챕터가 설명 없이 전제하면 안 되는 것)

- `sklearn`·`pandas`·`torch` API(리랭커 안에서 도는 것은 학생이 쓰지 않습니다). **`numpy`는 §2-7 리팩터로 바뀜**: Ch 5 02절에서 소개했고 이 챕터 01절이 `shape`·`axis=1`·배열 빼기·`np.argsort`를 더했습니다(그 밖의 NumPy API는 가르치지 않음). 내포식·`lambda`·f-string·`set`·`zip`·`enumerate`·`key=`/`reverse=`·기본값 매개변수·클래스 정의.
- 벡터 데이터베이스의 색인 종류 비교(IVFFlat 등), 검색에 걸린 시간 재기(이 챕터는 **한 번도 시간을 재지 않았습니다**), 큰 말뭉치에서의 성능, 다국어·영문 말뭉치.
- 답 품질 판정·근거 확인·출처 표기 검사(Ch 15), 에이전트·그래프(Ch 13), 가드레일(Ch 16).
- 여러 차례 오간 대화, 대상이 둘 이상인 대화(11절은 대화 다섯 개·한 번의 후속 질문만).

## 15. 기준 버전·확인 날짜

- 실습 폴더 `pyproject.toml`·`uv.lock`(해시 `5b10531e…`·`f13e8c6f…`): `langchain 1.4.0`·`langchain-openai 1.6.1`·`python-dotenv 1.2.3`·`psycopg 3.3.5`·`kiwipiepy 0.23.2`·`rank-bm25 0.2.2`·`sentence-transformers 6.0.1`·`tiktoken 0.14.0`·`numpy 2.5.3`(§2-7부터 01~13절 설치 셀에 적음), dev `pip==26.2`·`ipykernel==7.3.0`. 절마다 준비물에 기준 버전 + 「다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다」.
- 교재 출력 환경: Linux · Python **3.12.13** · PostgreSQL **17.11** + pgvector **0.8.1** · 메모리 3.8GB.
- 요금: 임베딩 `text-embedding-3-small` 0.02달러/100만 토큰, 답 모델 `gpt-5.4-mini`. 절마다 0.01달러 아래.
- 참고 자료 확인일: 01~05·07~13절 **2026-09-18~19**, **06절만 2026-09-09**(이번 개선에서 다시 확인하지 않음).

## 16. 전체 마감 순서 (Ch 9 요약 §9 · Ch 10 요약 §9 · Ch 11 요약 §15에 이어 붙인 판)

0. **끝났습니다**(Ch 12 마감에서): `part3-practice.zip` 재생성(92항목, 새 README·새 `시작하기.md`), ch12 화면 검사 28행, `check_delivery.py` 통과, review-pack 열세 개.
1. `textbook/downloads/` 묶음 재생성: **`part1-practice.zip`·`part2-practice.zip`**(지금 두 검사가 여기서 멈춥니다), **`llm-practice.zip`**(지금 묶음의 ch12 노트북 열두 개가 2026-09-14 판이고 13절 노트북이 없습니다), 필요하면 `part4-practice.zip`.
2. `textbook/part3/qa/run_continuity_bundle.py`를 **`--reuse-upstream` 없이** 실행(묶음에서 Ch 9 06 · Ch 10 08 · Ch 11 06 노트북을 실제로 돌립니다).
3. 공용 `visual.cjs`로 **ch09 8쪽을 다시 찍어 14 → 16행**으로. ch10 20 · ch11 16 · **ch12 28**은 이미 맞습니다.
4. `textbook/part3/qa/finalize_continuity_evidence.py` **15행을 `94` → `96`으로 올린 뒤** 실행합니다. 지금 94는 ch09의 -2와 ch12의 +2가 상쇄된 값이라 3단계를 끝내야 96이 됩니다. 37행은 2단계를 먼저 끝내야 통과합니다.
5. `textbook/part3/qa/check_continuity.py`와 `textbook/qa/check_course_continuity.py`를 끝까지 실행합니다(2026-09-19 기준 각각 **154행 part2 zip**·**212행 part1 zip** 신선도에서 멈춤, 1단계를 끝내면 지나갑니다). `check_course_continuity.py`는 `tomllib`이 필요해 Python 3.11 이상으로 돌립니다.
6. `textbook/part3/_build_index.py`를 마지막에 한 번 더 돌려 Part 3 목차와 `part3-practice.zip`을 맞춥니다.
7. 옛 생성기·옛 그림 정리(삭제 승인 필요): `figures/_gen_figures.py`, `qa/advanced_author.py`를 `qa/upgrade/before/generators/`로 `mv -n`, 옛 excalidraw·SVG(`01-정확-검색`·`02-HNSW` 등), `qa/upgrade/gates-wip*.json`.
8. 삭제 승인이 필요한 것: `labs/part3/ch12-retrieval-tuning/.venv`(08절이 남긴 빈 폴더), `runs/continuity/` 사본 여덟 개 가운데 12절 실행이 만든 넷 중 **셋**(`20260918T231546`·`231622`·`231828`) — **정본과 같은 사본 하나(`20260918T232052`)는 검사가 요구하므로 남겨야 합니다**(`check_continuity.py` 127~129행·`check_course_continuity.py` 161~163행). §2-7 리팩터 재실행 뒤로는 정본과 같은 사본이 **`20260921T082024`**이고, `check_course_continuity.py`의 원본 기록 보존 검사가 옛 정본 바이트를 사본 폴더에서 찾으므로 옛 사본도 지우기 전에 검사를 다시 돌려 보세요. 첫 실행 사본 `20260921T081609`는 `qa/upgrade/before-2-7/runs/moved/`로 옮겼습니다. 그 밖에 `/tmp/ch12-0N`·`/tmp/ch12close`·`/tmp/ch12-rv`, `.cache/vm/venv-ch12-retrieval-tuning`·`.cache/vm/hf`(6.0GB)·`.cache/vm/pgenv`·`.cache/vm/pgdata`.
9. 과정 요약 `textbook/qa/upgrade-course-summary.md`에 **Part 3 절**을 덧붙입니다(Ch 12가 Part 3 마지막 챕터입니다. 오케스트레이터 몫, PLAYBOOK §6).

## 17. 남은 것

- **전체 마감**: §16의 1~9단계.
- **뒤 챕터 인계 두 건**: §13-1(Ch 15 01절 깨짐, 반드시)·§13-2(Ch 13 07절 문장).
- **다시 실행하면 함께 고칠 것(지금은 재실행 금지)**: 07절 리랭킹 점수 반올림 자리(`round(…, 4)` → 6, 그러면 3·4·5위 동률이 풀림), 07절에 두 문서 청크 본문을 찍는 셀, 04절 품사 목록 두 벌을 한 표에서 견주는 셀, 10절 `mmr_row`를 두 함수로 나누기, 08절 `evaluate` 11줄.
- **잠금 정리**(검토 A C-5): `pgvector`·`pypdf`를 뺄지 `tests/`와 함께 정합니다. 빼면 `uv.lock`과 묶음 두 개를 다시 만들어야 합니다.
- **삽화를 다시 만들 때**: `13-4`의 두 관 모두 깔때기 쪽 끝에 갈색 테가 보여 「열린 입구」와 「마개」가 구슬 유무로만 갈립니다(지금은 「그림 읽기」가 말로 보완).
- **기록 정정 이력**: 06 `3927dbe0…` · 08 `2f734c20…` · 09 `9b66adad…` · 13 `54340aac…`/`ede466d5…`는 노트북에 저장된 값과 달라 마감에서 저장된 값(`28482c02…`·`0f6b0786…`·`493506d5…`·`7b61e25b…`/`504b3811…`)으로 고쳤습니다. 09 `executed_at`은 `2026-09-18T20:52:05Z`입니다. `runs` 48개 묶음 해시 `96d6b005…`는 재현되지 않아 개별 파일 해시로 바꿨습니다. **열세 노트북 모두 저장된 값 = 다시 계산한 값**입니다.
- 2차 검토(두 보고서 끝 「2차 검토 때 볼 곳」)와 강사 확인(§12).

## 18. §2-7 리팩터 (2026-09-21, 작업자 A 01~06 · 작업자 B 07~13·마감)

- **규칙**: 앞 절·앞 챕터에서 배운 함수는 실습 폴더 `notebooks/rag_tools.py`에서 `from rag_tools import …` 한 줄로 가져오고 벡터 계산은 NumPy로 합니다(`textbook/QUALITY-UPGRADE.md` §2-7). 함수를 처음 가르친 절은 노트북에 그대로 둡니다.
- **도구 파일**(함수 33개, 코드 220줄, SHA-256 `db3fe94f…`): 01~06 구역 16개(A)·07~13 구역 17개(B). 07~13 구역 = 문서 청크 판 `rank_chunks_by_distance`·`rank_chunks_by_bm25`·`unique_chunk_ids`, 07 `parent_ids_of(…, parent_by_chunk)`, 08 `eligible_items`·`chunk_precision_at(…, parent_by_chunk)`, Ch 8 `count_tokens(encoding, text)`, 10 MMR 다섯 개(`mmr_pick(…, vector_by_chunk)`), Ch 11 `precision_at`·`rank_weight`·`dcg_at`·`ideal_dcg`·`ndcg_at`(Ch 11 도구 파일 판). 인자 표는 `handoff.md` 「§2-7 리팩터 A」·「§2-7 리팩터 B」.
- **수치**: 코드 셀 459 → 330, 코드 줄 3658 → 2669(−989, −27.0%; 도구 파일을 더해도 2889, −21.0%). 07~13만 2280 → 1591(−30.2%). 12절 준비 셀 16개(함수 24개, 164줄) → import 세 줄.
- **다시 실행**: 01~06(A)·07~13(B) 새 커널 두 번. 07·08은 리팩터 전과 값 출력이 모두 같고, 09 `596` → `600`·`0.853` → `0.84`·부모 두 건 `4206`(한 번은 `4213`), 10 `0.75` → `0.76`, 12 7절 두 표, 13 답 표현이 달라져 인용·그림(09 세 장)을 고쳤습니다. **§2-7 10항으로 입력을 고친 절은 없습니다.**
- **12절 산출 파일**: 세 파일 해시가 바뀌었고(§4 표) 고른 설정·시험 지표·통합 기록 값은 같습니다. Ch 13 07·08이 읽는 값은 그대로이고 Ch 15 01절 `ndcg_at_5 < 1`은 여전히 `Q090` 한 줄입니다(§13-1).
- **테스트**: `tests/test_continuity.py`의 `load_notebook_function()`·`load_notebook_namespace()`가 도구 파일을 먼저 읽습니다(`tool_namespace()`). 확인하는 성질은 그대로, 4 passed.
