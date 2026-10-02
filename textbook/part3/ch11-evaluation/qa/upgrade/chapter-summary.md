# Ch 11 평가 기초 — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part3/ch11-evaluation` 01~07절(01~06 품질 개선 + 07 챕터 끝 실습 절 신설), 노트북 `labs/part3/ch11-evaluation/notebooks/01~07-*.ipynb`.
- 기간: 2026-09-18(절 작업) + 2026-09-18(검토 1차 반영·챕터 마감). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 6절 합계 **277**(G1 78·G2 38·G3 32·G4 0·G5 44·G6 67·G7 18, 통과 0/6) → 반영 뒤 **7/7 PASS, G1~G7 0**(`gates-after.json`).
- 코드 셀 23·25·25·32·38·42·32 = **217**, 검사 문장 **391·392·398·458·475·478·411**, Mermaid **28장**(5·4·4·4·4·4·3), 삽화 **7장**(절마다 1장, 모두 채택), 복습 문제는 HTML에만.
- **이 챕터는 답을 쓰는 모델을 한 번도 부르지 않습니다.** 서비스 요청은 임베딩뿐이고 절마다 0·17·16·16·17·16·5번입니다(0.01달러 미만).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md`(Part 1·2) → Ch 9 요약 → Ch 10 요약 → **이 문서**. 절 사이 세부는 `handoff.md`, 절별 기록은 `NN-diagnosis.md`, 검토와 반영은 `review-round1.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 라이브러리·API | 새로 만든 함수(노트북 셀) | 새 용어 |
|---|---|---|---|
| 01 | `open(경로, "rb")`·`read()`, `hashlib.sha256(바이트).hexdigest()`, `json.loads(한 줄)`, `os.path.exists`, `글.splitlines()`, `딕셔너리.keys()`, `딕셔너리.get(키, 기본값) + 1`, `목록[:5]`·`목록[-1]`, `range(len(목록))` + `break` | `unique_doc_ids(hit_list)` 5줄 · `find_gold_rank(doc_ids, gold_doc_ids)` 6줄 · `count_gold_docs(query_list)` 5줄 | 질의셋 · 정답 문서 ID · 관련도 판정 · 개발 분할 · 시험 분할 · 고유 문서 (6) |
| 02 | `OpenAIEmbeddings(model=)`·속성 `dimensions`, `InMemoryVectorStore(embedding=)`·`add_documents()`·`store.store`·`similarity_search(질문, k=)`, `PdfReader`·`reader.pages`·`page.extract_text()`, `Document(page_content=, metadata=)`, `str(number).zfill(2)`, `round(값, 3)` | `recall_at(doc_ids, gold_doc_ids, cutoff)` 6줄 · `mean_score(score_list)` 4줄 · `make_candidate_list(hit_documents)` 6줄 · `load_pdf_pages(pdf_path, doc_id)` 9줄(Ch 10 08절 코드) | 후보 목록 · 자르는 자리 · 재현율 · 질문 평균 (4) |
| 03 | 새 라이브러리 호출 0개 | `precision_at(doc_ids, gold_doc_ids, cutoff)` 6줄 | 정밀도 · 고정 분모 · 받은 개수 · 지표 천장 (4) |
| 04 | `math.log2()`(챕터에서 처음, Ch 5 02절 `math.sqrt()`와 이음) | `rank_weight(position)` 1줄 · `dcg_at(...)` 6줄 · `ideal_dcg(...)` 7줄 · `ndcg_at(...)` 3줄 | 자리 무게 · 자리 무게 합 · 가장 좋은 무게 합 · 0에서 1로 맞추기 (4) |
| 05 | 새 라이브러리 호출 0개. Python 쪽은 `딕셔너리.keys()`를 반복문 인자로 넘기기, 미리 만든 키로 세기 | `search(question, count)` 7줄 · `group_mean(rows, metric)` 4줄 · `print_group_table(rows, field, values)` 7줄 · `error_name(gold_rank, cutoff)` 5줄 · `metrics(item)` 8줄 | 조건별 평균 · 묶음 크기 · 오류 이름 · 후보 밖 · 뒤로 밀림 (5, 「앞자리 안」은 표 아래 문장) |
| 06 | `subprocess.run(cwd=)`·`sys.executable`·`time.strftime`·`os.makedirs`(모두 Ch 2 08·Ch 3 05·Ch 6 06·Ch 7 08절에서 배운 이름) | 없음(01~04절 함수 여덟 개를 다시 정의해 씀) | 실행 ID · 지표 규칙 이름 · 말뭉치 지문 · 보고서 자리 수 · 자동 실행 (5) |
| 07 실습 | **새 API·새 문법 0개** | `print_score_rows(rows)` 3줄 · `score_rows_at(cutoff)` 10줄 · `run_once(run_name, cutoff)` 10줄 | 0 |

- **쓰지 않은 Python 이름(일곱 절 모두 0건, AST로 확인)**: `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·`try`·`raise`·`+=`·세미콜론·한 줄 복합문·f-string 안 계산·타입힌트·`@`·`BaseModel`, 그리고 이름 `sum`·`max`·`min`·`sorted`·`set`·`enumerate`·`zip`·`join`·`next`·`isinstance`·`any`·`all`·`Counter`·`re`·`Path`. 호출한 내장 이름은 `len`·`print`·`open`·`range`·`round`·`str`뿐입니다.
- 주석·빈 줄을 뺀 셀 최대 줄 수는 일곱 절 모두 **12줄**(규격 §2-4 권장 3~12줄 안), 함수 본문 최대 **10줄**(07절 `score_rows_at`·`run_once`).
- `assert`는 코드가 정하는 값에만 씁니다(`missing_count == 0`·`recall_at(...) == 1.0`·`파일이 생겼는가`). 모델 문장 `assert`는 없습니다(답 모델을 부르지 않음).

## 2. 기준선 다섯 셀 (02~07절이 그대로 씁니다 — Ch 12가 먼저 읽을 곳)

02절이 handoff 선택지 2번(Ch 9·Ch 10에서 배운 임베딩 검색)을 골랐고 **03~07절이 같은 코드를 다시 만들어 씁니다.** 노트북 4~6절의 다섯 셀이 전부입니다.

1. `manifest.json`에서 `tier != "scanned"`인 **디지털 PDF 18건** 고르기(전체 21행)
2. `load_pdf_pages(pdf_path, doc_id)`(Ch 10 08절과 같은 코드)로 **쪽 Document 93개** 모으기
3. `len(page_document.page_content) > 0`인 쪽만 남겨 **색인에 넣을 쪽 90개**, **글이 있는 문서 17건**(`pdf/hard/H05.pdf` 세 쪽이 0자)
4. `OpenAIEmbeddings("text-embedding-3-small")`(차원 수 인자 없음) + `InMemoryVectorStore` + `add_documents` → 임베딩 요청 **1번**, `색인에 들어간 항목 수: 90`
5. `store.similarity_search(질문, k=candidate_count)` → 질문 하나에 요청 **1번**. 점수를 쓰지 않으므로 Ch 9 01절의 `similarity_search()` 판입니다(`_with_score` 아님)

- **후보 단위는 쪽이고 문서 ID 중복 제거를 자르기보다 먼저 합니다**(01절이 정한 순서). 실습 폴더 `evaluate.py` 56~74행도 쪽에 점수를 매기고 중복을 뺀 뒤 앞 50개를 남깁니다 — **후보 단위와 순서는 같고 점수 매기는 방법만 다릅니다**(임베딩 대 낱말·두 글자 조각 겹침).
- **후보 개수 50**은 `evaluate.py` 232~237행 때문입니다(기록 줄 수가 50 이상일 때만 `recall_at_50`, 5 이상이면 @5 셋). **줄이지 마세요** — 01~07절 값이 이어지지 않습니다.
- **두 기준선의 숫자를 나란히 놓지 않습니다.** 02~07절 b7에 같은 문장이 있습니다(`evaluate.py` 280행 `comparison_policy`).
- 검색 점수는 출력하지도 라벨에 넣지도 않습니다(일곱 절 모두).

## 3. 지표 이름·천장·해석 규칙 (Ch 12가 그대로 이어 씁니다)

| 지표 | 이 챕터 함수 | 도구 칸 이름 | 이번 실행 값(개발 분할 15문항, 자르는 자리 5) |
|---|---|---|---|
| 재현율 | `recall_at(doc_ids, gold_doc_ids, cutoff)` | `recall_at_5`·`recall_at_50`·`recall_at_logged_candidates` | 자리 1 `0.6` · 자리 5 **`0.867`** · 자리 10 `1.0` · 자리 50 `1.0` |
| 정밀도 | `precision_at(...)` | `precision_at_5` | 자리 1 `0.6` · 자리 5 **`0.173`** · 자리 10 `0.1` |
| nDCG | `rank_weight`→`dcg_at`→`ideal_dcg`→`ndcg_at` | `ndcg_at_5` | 자리 1 `0.6` · 자리 5 **`0.751`** · 자리 10 `0.789` |

- **천장 두 개를 본문에서 갈라 적습니다.** (1) 글이 있는 문서가 **17건**이라 고유 문서 목록은 17개를 넘지 못하고 자리 50은 목록을 자르지 못합니다 → 자리 50 재현율 `1.0`은 천장에 닿은 값입니다. (2) 개발 분할 15문항이 모두 정답 문서 한 개라 자리 5 정밀도의 최댓값은 **0.2**입니다 → 실측 `0.173`을 품질 점수로 읽지 않습니다.
- **나누는 수는 받은 개수가 아니라 약속한 자르는 자리입니다**(고정 분모). 받은 개수는 `evaluate.py`의 **`candidate_count`** 칸이고, `returned_count`는 보고서에 남긴 항목 수(`--top-k`)입니다 — 두 칸을 섞지 마세요(검토 03-1).
- **정답 문서가 한 개인 이 평가셋에서는 nDCG가 정답 문서 자리의 무게와 같습니다**(자리 1 `1.0`·2 `0.631`·3 `0.5`·4 `0.431`·5 `0.387`). 만점은 검색 결과가 아니라 정답 라벨로 계산합니다.
- **실행마다 흔들리는 값 = 받은 개수(고유 문서 수, 13~16)**. 표·그림 라벨·결론에 넣지 않습니다(02~07절 b7에 같은 항목). 정답 문서 자리는 여러 실행에서 같았습니다. 그림 라벨에서도 뺐습니다(`02-4`는 「Q085 고유 문서 목록」).
- **한 번 본 결과는 「이번 실행에서는」, 실행하지 않은 동작은 「이번에 실행하지 않았습니다」.** 어느 검색 방법·어느 설정·어느 자르는 자리가 나은지 판정하지 않습니다.

## 4. 오류 이름 갈래 (05절에서 정함 — Ch 12가 원인을 찾을 때 쓰는 이름)

- 정답 문서 자리 하나로 셋을 가릅니다: **후보 밖**(자리 0) · **뒤로 밀림**(자리가 자르는 자리보다 큼) · **앞자리 안**(그 안). 판정 흐름은 그림 `05-3`(마름모 파랑, 결과 상자 노랑).
- 이번 실행 결과 `{'후보 밖': 0, '뒤로 밀림': 2, '앞자리 안': 13}`(뒤로 밀림 = `Q085`·`Q086`, 정답 문서 `H01`이 고유 목록 10번째).
- **이름은 위치일 뿐 원인이 아닙니다**(05 b7). 영문 `candidate_miss`·`ranking_miss`·`top5_hit`은 쓰지 않고 **`evaluate.py`에도 없는 이름**이라 보고서 계약과 충돌하지 않습니다. 보고서 JSON에 오류 이름을 넣지 마세요.
- Ch 9 05절 「검색 누락」 자리를 후보 목록과 앞 다섯 자리로 한 번 더 가른 이름이고, Ch 8 04절 네 이름(목록에 든 내용 때문에 답이 틀어지는 자리)과는 b4·b7에서 갈라 적었습니다.

## 5. 06절 기록 계약 (파일 이름·키·사본과 읽는 쪽 — 꼭 먼저 읽을 것)

**이 챕터에서 `runs/`에 쓰는 절은 06절 하나입니다.** 01~05·07절은 파일을 쓰지 않습니다.

| 파일 | 쓰는 쪽 | 읽는 쪽 |
|---|---|---|
| `runs/notebook-run-20260918.json` | 06 노트북 8절(직접 씀) | 06 노트북이 다시 읽음. 이름에 `continuity`가 없어 증거 폴더로 옮겨지지 않음 |
| `runs/continuity-upstream-20260918.json` | 06 노트북 9절(`evaluate.py` 실행) | `finalize_continuity_evidence.py` 49행이 `continuity-upstream-*.json` 가운데 **가장 새 파일**을 고름 |
| `runs/upstream-top2-20260918.json` | 06 노트북 12절(`--top-k 2`) | 없음 |

- **읽는 쪽 다섯 갈래**(다시 쓸 일이 생기면 먼저 열 것): `textbook/part3/qa/run_continuity_bundle.py` 19·45~54·79~83행 · `textbook/part3/qa/finalize_continuity_evidence.py` 15·37·44~59행 · `textbook/qa/check_course_continuity.py` 43·50·94~112·172~199·212·216행 · `textbook/part3/qa/check_continuity.py` 44~46·58~78·138~159행 · `labs/part3/ch11-evaluation/evaluate.py` 176~254행.
- **`finalize_continuity_evidence.py` 49~59행이 보는 조건(7/7 통과 확인)**: 실행 7개(ch09 1 + ch10 6), 모든 실행이 `query_ids == ['Q001']`·`recall_at_50 is None`·`recall_at_logged_candidates == 1`, ch09는 `recall_at_5`·`precision_at_5`·`ndcg_at_5`가 모두 `None`, ch10 여섯 실행은 `1`·`0.2`·`1`.
- **이름 규칙**: `runs/`에 파일을 쓸 때 이름에 `continuity-upstream-`을 넣지 마세요(49행 glob이 그 파일을 고릅니다). `continuity`가 들어가면 `run_continuity_bundle.py` 79~83행이 증거 폴더로 옮깁니다. **파일을 쓰지 않는 쪽이 가장 안전합니다**(Ch 9 07·Ch 10 09·Ch 11 07 실습 절 선례).
- **`before-manifest.json`이 바이트로 보는 두 파일은 건드리지 않았습니다**: `runs/baseline.json` `4ec8435c7c26a7b1…`·`runs/notebook-log.json` `6ef314fec3e9a3ec…`. `labs/**/runs/**` 49개 항목이 모두 그대로입니다.
- `runs/` 묶음 해시: 작업 전 11개 `d03e2c098d786271…` → 작업 뒤 14개 **`6b891bf97b31b42f0ea9697bfb5fdd30fde326494fc673c1e01dcdcd3ea0c6d2`**(기존 11개 바이트 불변, 검토 반영 뒤에도 같음). **§2-7 리팩터(2026-09-21) 뒤 17개 `589d400dcbf5c9d4195280c5adfe251e72cc9f9f9f5602659fdc7177129f9ef5`**(06 재실행으로 `*-20260921.json` 세 개가 더해짐, 기존 14개 바이트 불변, §19). 계산법은 프로젝트 맨 위에서 `find labs/part3/ch11-evaluation/runs -type f | sort | xargs sha256sum | sha256sum`.
- 파일 이름에 **날짜만** 넣습니다(`time.strftime("%Y%m%d")`). 같은 날 두 번 실행하면 덮어씁니다(06 b7이 밝힘).
- 06 노트북은 `check_course_continuity.py` 50행에서 `data_refresh`로 따로 다루어지므로 코드가 같아도 출력이 달라진 상태를 받아들입니다.

## 6. `tests/test_evaluate.py`가 05절 노트북에 요구하는 계약

- 126~138행이 `notebooks/05-조건별-평가와-오류-분류.ipynb`에서 `def metrics(item):`가 든 코드 셀을 `ast`로 찾아 **실제로 실행**하고 `metrics({"question": ..., "gold_doc_ids": ["G", "H"]})`가 `(0.5, _)`를 내는지 봅니다.
- 지킬 네 가지: 함수 이름 **`metrics`** · 인자 하나 **`item`**(키 `question`·`gold_doc_ids`) · 반환 **튜플 `(재현율, 정밀도)`** · 함수가 부르는 바깥 이름은 **`search`(인자 두 개)** 하나뿐. 자르는 자리는 함수 안에서 `cutoff = 5`로 따로 만듭니다(바깥 `cutoff_narrow`를 쓰면 `NameError`).
- 테스트 파일은 고치지 않았습니다(`d738970fdf1b7c50…`). 01~07절 작업 전후와 검토 반영 뒤 모두 **8 passed**입니다.
- 실행법: `uv run --project labs/part3/ch11-evaluation --with pytest==8.4.2 python -m pytest labs/part3/ch11-evaluation/tests -q`(실습 폴더 dev에 `pytest`가 없습니다).

## 7. 실습 폴더 의존성·환경 (2026-09-18 두 번 바뀜)

- `labs/part3/ch11-evaluation/pyproject.toml`
  - 02절이 `langchain-core==1.6.2`·`langchain-openai==1.6.0`·`python-dotenv==1.2.3`·`numpy==2.5.3`를 더했습니다(`pypdf==6.1.1` 유지). `numpy`가 없으면 `similarity_search`가 `ImportError: cosine_similarity requires numpy`로 멈춥니다.
  - **챕터 마감(검토 C-1)이 dev 그룹을 `dev = ["pip==26.2", "ipykernel==7.3.0"]`로 고쳤습니다.** 02~07절 첫 코드 셀이 `%pip install -q …`이고, 학생 안내는 `uv sync --locked` → 그 `.venv`를 커널로 선택이라 잠금에 `pip`이 없으면 **첫 셀에서 멈춥니다.** `check_course_continuity.py` 43행도 `%pip`이 든 셀마다 `locked.get('pip') == '26.2'`를 봅니다.
- 해시: `pyproject.toml` **`10e07ede49be713d…`**, `uv.lock` **`2c42823dd43918bb…`**(그 전 `c51274c699840de9…`·`d0ec3790585c295f…`).
- `pytest`는 넣지 않았습니다(Ch 12도 dev에 없음). 잠금 변경을 최소로 두고 테스트는 `--with pytest`로 돌립니다.
- 가상환경은 `run_section.sh` 규칙대로 `$ROOT/.cache/vm/venv-ch11-evaluation`(`uv sync --locked --project labs/part3/ch11-evaluation`). torch는 쓰지 않습니다. 새 커널은 `nbclient==0.11.0`·`ipykernel==7.3.0`, Linux aarch64 Python **3.12.13**.
- **규격 추가 규칙(이 챕터에서 나옴)**: `%pip` 셀을 새로 넣으면 실습 폴더 dev 그룹의 `pip`·`uv.lock`·학생 묶음을 함께 확인합니다(`QUALITY-UPGRADE.md` §7-2, `PLAYBOOK.md` §4에 한 줄씩 넣었습니다).

## 8. 고치지 않는 계약 파일과 해시 (반영 전후 모두 같음)

| 파일 | SHA-256 | 보는 쪽 |
|---|---|---|
| `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl` | `9544b332d5ac120e…` | `check_continuity.py` 44~46행이 Ch 12 `advanced-queries.json`과 **완전히 같아야 한다**고 봄 — **한 글자도 고치지 마세요** |
| `labs/part3/ch11-evaluation/evaluate.py` | `41c9408fb7de1434…` | `check_continuity.py` 158행·`check_course_continuity.py` 216행이 묶음에 있는지 봄. 06 노트북이 `subprocess`로 실행 |
| `labs/part3/ch11-evaluation/tests/test_evaluate.py` | `d738970fdf1b7c50…` | 126~138행이 05절 노트북 셀을 직접 실행(§6) |
| `labs/part3/ch09-rag-first-run/runs/continuity-ch09-search.jsonl` | `294713765a115b56…` | k=2 전제, @5 셋이 `None` |
| `labs/part3/ch10-document-processing/runs/continuity-ch10-indexing.jsonl` | `58cc790c45df9bf9…` | 6줄·k=5 |
| `labs/part3/ch11-evaluation/runs/baseline.json` · `runs/notebook-log.json` | `4ec8435c7c26a7b1…` · `6ef314fec3e9a3ec…` | `before-manifest.json`이 바이트로 봄 |
| Ch 6·7·8 비용 사슬 | `f18920c6…` · `a8aaafb7…` · `125fc147…` | 이 챕터는 읽지도 쓰지도 않음 |

## 9. 반복해 쓴 데이터·이름·비유

- **데이터**: 평가셋 `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl` **30줄·칸 7개**(`query_id`·`question`·`gold_doc_ids`·`tier`·`type`·`split`·`answerable`, 답 문장 칸 없음), 난이도 `{'easy': 10, 'medium': 10, 'hard': 10}`, 분할 `{'dev': 15, 'test': 15}`, 정답 문서 여섯 가지(`E01` 6·`E02` 4·`M01` 8·`M02` 2·`H01` 8·`H02` 2), 질문마다 정답 문서 **한 개**. 말뭉치 `labs/data/rag-corpus`(목록 21행·디지털 18건·쪽 93개·글이 있는 문서 17건). 앞 챕터 기록 7줄(ch09 1 + ch10 6, 질문은 모두 `Q001`).
- **이어 쓴 이름**: `candidates = [".", "../../..", "../../../.."]`·`root_path`, `corpus_path`·`manifest_path`·`dataset_path`·`ch09_log_path`·`ch10_log_path`, `queries`(30)·`dev_queries`(15)·`records`(7), `manifest_rows`·`digital_rows`(18)·`corpus_pages`(93)·`index_pages`(90)·`text_doc_ids`(17), `embedding_model_name`·`embedding_model`·`store`, `candidate_count`(50)·`cutoff_narrow`(5)·`cutoff_wide`(50)·`cutoff_top`(1), `unique_by_qid`·`rank_by_qid`·`score_rows`·`run_day`·`run_date_text`·`dataset_fingerprint`.
- **기록 한 줄의 칸**: 06절 일곱 칸(`실행 ID`·`실행 날짜`·`지표 규칙 이름`·`실행 설정`(여섯 칸 덩어리)·`입력 지문`·`질문 수`·`지표`), 07절은 `실행 설정`을 `자르는 자리` 한 칸으로 줄인 일곱 칸. 지표 규칙 이름은 노트북 기록 `고유 문서 기준 질문 평균 v1`, 도구 보고서 `unique-doc-observed-candidates-v1`(**규칙이 달라 값도 다릅니다** — 06 b7·용어 표에 적음).
- **비유 계열(삽화 7장)**: 01-6 쪽지와 책 → 02-5 넓은 쟁반·좁은 문·작은 쟁반 → 03-5 칸이 다섯인 쟁반 → 04-5 받침 높이가 다른 쟁반 → 05-5 한 무더기를 세 더미로 → 06-5 공책에 한 줄로 옮기기 → 07-4 쟁반 둘과 공책 두 줄. **흰 카드**는 02~04절 후보 한 줄, 05절부터 질문 한 장(뜻이 바뀐 자리를 「그림 읽기」에 적음), **파란 카드**는 정답 문서, **색 딱지**는 기록 한 줄의 값 한 갈래. 카드 상자(Ch 9 색인)·봉투(Ch 10 출처 기록)·서랍(Ch 10 벡터 캐시)은 뜻이 정해져 있어 쓰지 않았습니다.
- **그림 색 선례**: 질문 묶음·기록 묶음·색인 **초록(tool)**, 계산·나누기·사람이 정한 판정 규칙 **파랑(flow)**, 출력으로 확인한 값 **노랑(measure)**, 두 칸 공통 값·계약 **회색**. **보라 0장**(임베딩 요청은 본문 단락으로만), **빨강 0장**(실패 상자가 없는 챕터). `xychart-beta`는 주황 막대(정밀도)·초록 선(재현율)·파란 선(nDCG). subgraph 두 개는 「위 칸·아래 칸」으로 서술(칸을 넘는 화살표가 있어 칸 안 `direction`이 무시됨). viewBox 폭 최대 720(06-2), 렌더 도장 `*.render.json`은 지우지 않습니다.

## 10. 07 실습 절 주제와 결과

- 제목 「평가 기초 실습: 자르는 자리를 바꿔 두 실행 견주기」, 파일·slug `07-평가-기초-실습`, 형식 `experiment`, meta 「실습 30분 · 새 용어 0」(**챕터 시수에 더하지 않음**, 규격 §7-2).
- 조립: 01절 `find_gold_rank` → 05절 `search` → 02·03·04절 세 지표 → 05절 `group_mean` → 06절 기록 한 줄을 `run_once(run_name, cutoff)` 하나로 이었습니다. 함수 열여섯 개 가운데 **열세 개가 01~06절과 같은 코드**입니다.
- 질문은 **개발 분할 앞 네 문항** `Q001`~`Q004`(정답 문서 자리 `1`·`1`·`3`·`3`)이라 요청이 색인 1 + 검색 4 = **5번**입니다. 두 실행이 같은 검색 결과를 다시 써서 실행이 두 번이어도 요청이 늘지 않습니다.
- 결과: 실행 1(자리 5) 재현율 `1.0`·정밀도 `0.2`·nDCG `0.75`, 실행 2(자리 1) 세 값 모두 `0.5`. 비교표 두 줄에서 질문 수 `4`와 입력 지문 `9544b332d5`가 같습니다.
- **네 문항 값(1.0·0.2·0.75)을 15문항 값(0.867·0.173·0.751) 자리에 쓰지 않습니다.** 네 문항은 모두 `easy`이고 정답 문서가 `E01` 하나입니다(본문 일곱 곳에서 조건을 밝힘).
- 파일을 쓰지 않습니다. 실행 ID는 `cut5-20260918`·`cut1-20260918`(기록의 값이고 본문·도식은 「실행 1·실행 2」로만 부릅니다).

## 11. Ch 12(검색 품질과 튜닝)가 이어받을 것

1. **평가셋과 분할**: `evaluation-queries.jsonl` 30줄은 계약 파일이고 Ch 12 `advanced-queries.json`과 완전히 같아야 합니다(`check_continuity.py` 44~46행). **개발 분할 15문항으로 설정을 고르고 시험 분할 15문항은 설정을 다 고른 뒤 한 번만** — 이 챕터가 여섯 절 내내 지킨 약속입니다. Ch 12가 시험 분할을 처음 보는 절을 만들 때 그 약속을 인용하세요.
2. **세 지표 함수와 인자 모양**: `recall_at(doc_ids, gold_doc_ids, cutoff)`·`precision_at(...)`·`ndcg_at(...)`은 **이미 중복을 뺀 고유 문서 ID 목록**을 받고 자르기는 함수 안에서 합니다. `evaluate.py`의 같은 이름 함수는 `dedupe_docs()`를 함수 안에서 부르는 판이라 인자 모양이 다릅니다 — Ch 12에서 두 판을 섞지 마세요.
3. **기준선과 값**: 임베딩 기준선 다섯 셀(§2)과 개발 분할 15문항 자리 5 값 `0.867 | 0.173 | 0.751`이 Ch 12 비교의 출발점입니다. Ch 12가 다른 검색 방법(BM25·하이브리드·재정렬)을 쓰면 **후보 단위·중복 제거 순서·자르는 자리·질문 묶음이 같을 때만** 이 값과 견줄 수 있습니다.
4. **오류 이름 셋**(§4)으로 「왜 뒤로 밀렸는지」를 Ch 12가 답합니다. 이 챕터는 자리만 보고 이름을 붙였고 원인은 보지 않았습니다.
5. **기록 한 줄과 도구**(§5): Ch 12 12절이 「36개 설정을 개발 문항 15개에서 비교하고 시험 1회」로 적었고 `check_continuity.py` 85행이 `len(experiments) == 36`을 봅니다. 06·07절의 기록 한 줄 모양(설정·지표·날짜·지표 규칙 이름·입력 지문)을 그대로 이어 쓰면 두 챕터 기록을 나란히 읽을 수 있습니다.
6. **아직 가르치지 않은 Python**(§12)을 Ch 12가 처음 쓰면 그 자리에서 세 문장으로 풀어야 합니다.

## 12. 아직 가르치지 않은 것 (Ch 12가 설명 없이 전제하면 안 되는 것)

Ch 9 요약 §6 + Ch 10 요약 §7에 더해, 이 챕터 일곱 절에서도 하지 않은 것입니다.

- **평가**: 시험 분할 보기, 답할 수 없는 질문을 실제로 빼는 장면, 정답 문서가 여러 개인 질문의 평균(함수 동작만 04절에서 확인), 관련도를 0과 1이 아닌 여러 단계로 매기기, 로그2가 아닌 감쇠 방법, 점수 기준값·거르기, 질문을 새로 만들어 라벨 붙이기, 운영 질문 분포와의 대표성, 답 문장 판정·LLM 판정자(Ch 15).
- **검색**: 다른 임베딩 모델, 차원 수를 준 색인, MMR·재정렬·질문 재작성(Ch 12), 다른 벡터스토어, **검색 점수를 값으로 쓰기**(이 챕터는 점수를 출력조차 하지 않음), 색인 저장과 다시 불러오기, 어휘 겹침(BM25 계열) 검색을 노트북에서 구현하기.
- **도구**: `evaluate.py`를 `import`해서 함수를 직접 부르기(06절은 `subprocess`로 실행만), `argparse`로 인자를 받는 스크립트 만들기, `evaluate.py`의 기본 모드(낱말·두 글자 조각 겹침) 실행.
- **Python**: `min`·`max`·`sum`·`sorted`·`set`·`enumerate`·`zip`·`join`·`Counter`·`re`·`Path`·`try`·`raise`·`+=`·`lambda`·내포식·클래스·타입힌트·`@`·`BaseModel`이 일곱 절 모두 **0건**입니다.

## 13. 용어 (Ch 9·Ch 10에서 이어받고 이 챕터가 더한 말)

- **이어 쓴 말**: 문서 청크(한정어 없는 「청크」 금지), 색인, 벡터스토어, 검색 점수, 실행 설정, 실행 기록 한 줄, 기록 줄 수, 겹침, 자리 칸 `row`·`section`·`heading`, 출처 표시 `[E01 p.2]`. **「조각」은 Ch 5 토큰 뜻 전용**입니다.
- **이 챕터가 더한 말 28개**: §1 표의 새 용어 칸(01 6 · 02 4 · 03 4 · 04 4 · 05 5 · 06 5 · 07 0).
- **쓰지 않기로 한 말**: 「청킹」, 한정어 없는 「청크」, 「오버랩」, 「임계값」, 「텍스트 레이어」, 「열」(→ 칸), 「필수 필드」(→ 필수 칸), 「사전」(→ 딕셔너리), 「페이지」(→ 쪽), 「옵션」, 「거시 평균」(→ 질문 평균), 「절단 깊이」(→ 자르는 자리), 「후보 집합」(→ 후보 목록), 「단일 정답 라벨」, 「슬라이스」, 「상위 5개 적중」, 「누적 할인」·「이상적 DCG」·「순위 할인」·「등급 관련도」, 「설정 스냅샷」, 「회귀 실행」, 「강사 시연」, 영문 `candidate_miss`·`ranking_miss`·`top5_hit`.
- **비유에서 쓰는 「색 딱지」**(06·07절): 기록 한 줄의 값 한 갈래를 가리킵니다. 검토 C-3으로 「조각」에서 바꿨습니다(Ch 10이 「도막」으로 바꾼 것과 같은 처리).

## 14. 챕터 밖 수정 (전부 목록)

- `textbook/part3/_build_index.py` — `CHAPTERS`의 ch11 절 수 칸 **6 → 7**(강의 6h·실습 10h 그대로). 이 스크립트를 돌리면 Part 3 목차와 **`textbook/downloads/part3-practice.zip`이 함께 다시 만들어집니다**(83 → **91항목**, `Part 3: 35 verified sections; 88 bundled files`).
- `textbook/downloads/part3-practice.zip` — 07 노트북·새 `pyproject.toml`·새 `uv.lock`(`pip` 포함)이 들어갔습니다. 학생의 `ModuleNotFoundError` 두 갈래(패키지·`pip`)가 모두 풀립니다. 세 자리(묶음 맨 위·실습 폴더 맨 위·`notebooks`)에서 경로 셀 실행을 확인했습니다.
- `labs/part3/ch11-evaluation/pyproject.toml`·`uv.lock` — §7.
- `labs/part3/ch11-evaluation/README.md` — 07절 한 줄 추가.
- `labs/part3/ch11-evaluation/_make_notebooks.py` — 첫머리에 설명 주석 + `raise SystemExit(...)`(옛 생성기 실행 막음). **`qa/upgrade/before/generators/`로 옮기는 일은 남았습니다**(§15).
- `textbook/_notebook/checks/ch11-evaluation/visual-results.json` — 14행 → **16행**(16/16 PASS). 스크린숏 네 장도 새로 찍었습니다.
- `textbook/part3/qa/finalize_continuity_evidence.py` — 15행 `assert len(visual)` **92 → 94**, 주석 「ch11 14」 → 「ch11 16」 + 「92나 90으로 내리지 마세요」.
- `textbook/part3/qa/check_delivery.py` — 112행 `len(notebooks) == 32` → **35**, 113행 `quizzes >= 32 * 3` → `35 * 3`. 이제 끝까지 통과합니다. 같은 실행이 `textbook/part3/qa/delivery-results.json`을 새로 씁니다(스크립트가 늘 쓰는 결과 파일).
- `textbook/part3/ch09-rag-first-run/qa/upgrade/chapter-summary.md` §9 4단계 · `textbook/part3/ch10-document-processing/qa/upgrade/chapter-summary.md` §8·§9 3·4단계 — `finalize` 값 92 → **94**와 ch11 16행 사실을 적어 마감 작업자가 되돌리지 않게 했습니다.
- **고치지 않은 것**: 빌드 도구(`chapter.json` + 공용 `_template/builder.py`로 충분), 묶음 허용 목록(`public-files.json`·`build_bundle.py`의 `data`·`FIXTURES`), 묶음 금지 목록, `evaluate.py`·`tests/`·평가셋·Ch 9·Ch 10 기록.
- **권한 한 문장**: 검토 보고서의 결정 요청 열여덟 항목은 모두 권고대로 유지한 것이고, 강사가 뒤집을 수 있는 항목은 §16(강사 확인 대상)에만 있습니다.

## 15. 전체 마감 순서 (Ch 9 요약 §9 · Ch 10 요약 §9에 이어 붙인 판)

0. **끝났습니다**: 실습 폴더 dev 그룹 `pip==26.2` + `uv.lock` 재생성(검토 C-1).
1. `textbook/downloads/part3-practice.zip`은 **2026-09-18 마감에서 이미 다시 만들었습니다**(91항목, 새 `uv.lock` 포함). `llm-practice.zip`(104개 항목이 옛 판)·`part1`·`part2`·(필요하면 `part4`) 묶음은 **아직 재생성 전**입니다.
2. `textbook/part3/qa/run_continuity_bundle.py`를 **`--reuse-upstream` 없이** 실행합니다(옛 `temporary_extraction` 폴더가 없어 재사용 경로를 쓸 수 없습니다). 이 스크립트가 묶음에서 Ch 9 06 · Ch 10 08 · **Ch 11 06** 노트북을 실제로 돌립니다.
3. 공용 `visual.cjs`로 **ch09 8쪽(14 → 16행)**을 다시 찍습니다. **ch10은 20행, ch11은 16행으로 이미 맞습니다.**
4. `textbook/part3/qa/finalize_continuity_evidence.py`를 실행합니다. 15행은 **이미 94**입니다(고치지 마세요. 2026-09-18 기준 실제 합은 92 = ch09만 14). 37행은 2번을 먼저 끝내야 통과합니다. **2026-09-19 Ch 12 마감 갱신**: ch12가 실습 절 13을 붙여 26 → **28행**이 되었습니다. 그래서 지금 실제 합은 **94**(ch09 14 + ch08 14 + ch10 20 + ch11 16 + ch12 28 + part3 2)이고, 이 94는 **ch09의 -2와 ch12의 +2가 상쇄된 값**입니다. 기대값은 **94 그대로** 두었습니다. ch09 8쪽을 다시 찍어 16행이 되면 합이 **96**이 되므로, 그때 15행을 96으로 올리고 실행하세요.
5. `textbook/part3/qa/check_delivery.py`는 **이미 끝까지 통과**합니다(노트북 35·quiz 149). Part 3에 절을 더 붙이면 112~113행 숫자를 다시 맞추세요.
6. `textbook/part3/qa/check_continuity.py`·`textbook/qa/check_course_continuity.py`를 끝까지 실행합니다. **2026-09-18 기준 각각 154행 `part2-practice.zip`·212행 `part1-practice.zip` 신선도에서 멈춥니다**(1번을 끝내면 지나갑니다). `check_course_continuity.py`는 `tomllib`이 필요해 Python 3.11 이상으로 돌립니다(`uv run --project labs/part3/ch11-evaluation python …`).
7. 옛 생성기 `labs/part3/ch11-evaluation/_make_notebooks.py`를 `qa/upgrade/before/generators/`로 `mv -n`, `figures/_gen_figures.py`와 옛 SVG·Excalidraw 여섯 쌍 정리(삭제 승인 필요).
8. `textbook/qa/upgrade-progress.md`는 이 챕터 행을 갱신했습니다. 과정 요약 `textbook/qa/upgrade-course-summary.md`의 Part 3 절은 **Part 3 마지막 챕터(Ch 12) 뒤**에 씁니다.

## 16. 강사 확인 대상

- **분량과 시수 배분**(검토 C-7, 유지): 05·06절이 코드 셀 38·42개·검사 문장 475·478로 가장 무거운데 실습 시수가 1h로 가장 적고, 02~04절(25·25·32셀)이 2h입니다. 시수 합(강의 6h·실습 10h = `chapter.json` 「총 16h」)을 깨지 않으려고 개선 전 배분을 유지했습니다.
- **01절에서 검색기를 뺀 것**과 **b4 「답변 판정 기준」 표를 뺀 것**(검토 유지 권고): 01절은 앞 챕터 기록 7줄만 읽고 검색은 02절부터 합니다. 판정 기준(필수·금지·출처 형식)은 Ch 15 몫입니다.
- **30문항 기준선을 임베딩 검색으로 고른 것**(handoff 선택지 2번): 실습 폴더 의존성이 네 개 늘고 절마다 임베딩 요청 16~17번이 듭니다. `evaluate.py`의 어휘 겹침 기준선과는 숫자를 나란히 놓지 않습니다.
- **본문 값이 바뀐 자리**: 03절 `P@5 0.200` → 실측 `0.173`(0.2는 천장), 04절 `약 0.893` → `0.751`, 05절 개선 전 난이도 값과 「어휘 겹침 검색이 유리」 문장 삭제, 06절 도구 기본 모드 값 삭제.
- **오류 이름 한국어 셋**(후보 밖·뒤로 밀림·앞자리 안)과 **갈래 칸 영문 값 그대로 출력**(`single`·`table`·`multi_doc`·`reasoning`·`temporal`·`multi_hop` — 평가셋이 계약 파일).
- **06절이 `runs/`에 파일 세 개를 쓰는 것**(노트북이 직접 쓰는 `notebook-run-{날짜}.json` 포함)과 기록의 한국어 칸 이름 대 보고서 영어 칸 이름.
- **07 실습 절**: 질문을 네 문항으로 줄인 것(요청 5번), 실행 ID `cut5`·`cut1`이 영문 약어인 것, 실습 30분을 챕터 시수에 더하지 않은 것.
- **삽화 `06-5`의 빨강 색 딱지**: 이 챕터 도식은 빨강 0장(실패 색을 비워 둠)이라 다시 만들 때 색을 바꾸기를 권합니다.

## 17. 기준 버전·요금 확인 날짜

- 실습 폴더 `pyproject.toml`·`uv.lock`: pypdf **6.1.1**, langchain-core **1.6.2**, langchain-openai **1.6.0**, numpy **2.5.3**, python-dotenv **1.2.3**, dev `pip==26.2`·`ipykernel==7.3.0`. 절마다 준비물에 기준 버전 + 「다른 버전과 Windows·macOS에서는 이번에 실행하지 않았습니다」.
- 요금: 임베딩 `text-embedding-3-small` 100만 토큰당 **0.02달러**(2026-09-17 확인). 색인 한 벌에 보낼 조각 수는 59190개 어림이고 절당 0.01달러 미만입니다. 답을 쓰는 모델은 부르지 않았습니다.
- 소스로 확인한 동작(`evaluate.py`): 56~74행 기준선(쪽 점수 → 문서 중복 제거 → 앞 50개), 77~93행 지표 함수, 161~167·224~231행 `candidate_count`/`returned_count`, 176~254행 보고서 쓰기, 232~237행 `logged_k >= 5`·`>= 50` 규칙, 280행 `comparison_policy`.

## 18. 남은 것

- **전체 마감**: §15의 1·2·3·4·6·7단계.
- **다시 실행하면 함께 고칠 코드(지금은 재실행 금지)**: 02 노트북 7절 질문별 표의 둘째 칸(받은 개수 — 03절 모양으로 세 칸으로 줄이기, 검토 02-1), 02~06절 준비 셀의 `%pip` 다섯 줄이 같은 내용이라 한 곳만 고치면 어긋나는 점(생성기마다 따로 적혀 있음).
- **삽화를 다시 만들 때 고칠 것**: `06-5`의 빨강 딱지를 다른 색으로(§16), `07-4`의 왼쪽 쟁반 빈 아랫줄은 지금 「그림 읽기」가 설명하고 있으므로 그림을 고치면 그 설명도 함께 고칠 것.
- **`outputs_sha256`이 실행마다 흔들립니다**: 차이는 첫 셀 `%pip install -q`의 stdout이 stream 조각 두 개로 나뉘는 자리뿐이고 출력 글은 같습니다(`execute.py` `output_hash()`가 조각 목록을 그대로 셈, 공용 `nbkit.install_source()` 셀이라 고치지 않았습니다). 다음 챕터에서 `outputs_sha256`이 어긋나면 먼저 이 자리를 보세요.
- **기록 정정 이력**: handoff·`집필점검표.md`·`verification.md`가 적었던 04 `3af98079…` · 05 `71f76c73…` · 06 `39d283de…`는 노트북에 저장된 `code_sha256`과 달랐습니다(04 노트북은 검토 반영에서 열지도 않았습니다). 마감에서 저장된 값 `4cfaa1bf…`·`1fddc8df…`·`c06a2617…`로 고쳤고, 일곱 노트북 모두 **저장된 값 = 다시 계산한 값**입니다.
- **정리 대상**(삭제하지 않고 목록만, 삭제 승인 필요): 옛 도식 `figures/0[1-6]-*.svg`·`.excalidraw`·`.caption.md` 개선 전 판과 `figures/_gen_figures.py`, `qa/upgrade/gates-wip-01.json`~`07.json`·`gates-wip.json`, `qa/upgrade/before/review-round1/`, 챕터·실습 폴더 `__pycache__`·`.pytest_cache`, `.cache/vm/venv-ch11-evaluation`(전체 마감 때), 기기 `/tmp/ch11-01`~`/tmp/ch11-07`·`/tmp/ch11-close`·`/tmp/ch11-02-pyproject.bak`.
- 2차 검토(`review-round1.md` 끝 「2차 검토 때 볼 곳」)와 강사 확인(§16).

## 19. §2-7 리팩터 (2026-09-21)

- 앞 절·Ch 9 함수 13개를 `labs/part3/ch11-evaluation/notebooks/rag_tools.py`(코드 86줄)로 모으고 02~07절 준비 셀에서 한 줄로 가져옵니다: Ch 9 02 `load_pdf_pages`, 01 `unique_doc_ids`·`find_gold_rank`, 02 `recall_at`·`mean_score`·`make_candidate_list`, 03 `precision_at`, 04 `rank_weight`·`dcg_at`·`ideal_dcg`·`ndcg_at`, 05 `search`·`group_mean`. **도구 파일 `search`는 `search(store, question, count, candidate_count)`**(05절 판은 바깥 이름을 읽음 — 06절이 알림). 챕터 안 다시 정의 49번은 모두 처음 정의와 본문이 같았습니다. NumPy는 쓰지 않았습니다(벡터 계산 0곳). `evaluate.py`의 같은 이름 함수는 다른 판이라 넣지 않았고 파일도 고치지 않았습니다.
- 코드 셀 217 → **167**, 코드 줄 1647 → **1312**(−335, −20.3%; 도구 파일 포함 1398). 01은 그대로. 05·06 「3. 앞 절 지표 함수」와 07 「6. 앞 절 지표 함수 가져오기」는 코드 셀 없는 설명 소절로 남겨 절 번호를 지켰습니다. 게이트 7/7·verify `PASS 7 sections / 167 code cells (max 15 lines)`·visual 12건·tests 8 passed(`metrics`가 05 노트북에 남아 테스트 그대로)·Ch 12 tests 4 passed.
- 02~07 새 커널 두 번: A·B 같음, **리팩터 전과 출력이 같고 06·07 실행 날짜·실행 ID와 06 도구 보고서의 Ch 9·10 실행 이름 열네 줄만 다름**. 인용 값은 날짜 말고 수정 없음. §2-7 10항 입력 수정 없음.
- **06을 다시 실행해 `runs/`에 `continuity-upstream-20260921.json`(`7ef93f8b…`)·`notebook-run-20260921.json`(`32d47328…`)·`upstream-top2-20260921.json`(`660de0cc…`)이 새로 생겼습니다**(20260918 파일은 그대로). 새 보고서의 실행 7개 `run_id`가 지금 Ch 9·10 기록(`e0323e89…`·`0984e167…`)의 `source_run_id`와 맞고 지표는 전과 같습니다. Ch 12는 Ch 11 `runs/`를 읽지 않고, 평가셋(`9544b332…`)은 그대로입니다.
- 학생 묶음: `part3-practice.zip` 95항목(`e7f18258…fa6fb`), `check_delivery.py` 통과. 세부는 `handoff.md` 「§2-7 리팩터 (2026-09-21)」.
