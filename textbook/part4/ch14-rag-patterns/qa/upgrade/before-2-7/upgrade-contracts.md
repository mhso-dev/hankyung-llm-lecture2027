# 산출 파일·데이터 계약 (upgrade-contracts)

**무엇이 들어 있나**: 챕터별 기록 파일 이름·키·줄 수·해시와 읽는 쪽, 「다시 실행하면 안 되는 노트북」, 이어 쓸 데이터·이름·함수·비유, 실습 폴더 테스트 계약, 학생 묶음 허용 목록, pgvector 실행 방법, 리랭커 모델·revision·메모리, 챕터별 기준 버전.
**누가 읽나**: `runs/`·계약 파일을 읽거나 쓰는 절, 실습 절, 챕터 마감 담당. 절 작업의 판단 기준은 `upgrade-course-summary.md`(모두 읽음), 전체 마감은 `upgrade-final-checklist.md`(마감 담당만).

2026-09-19에 `upgrade-course-summary.md`의 Part별 §4에서 옮겼습니다(내용 그대로). 근거는 각 챕터 `qa/upgrade/chapter-summary.md`.

## 1. 이어 쓸 데이터·이름·함수 — Part 1

| 챕터 | 이어 쓸 것 |
|---|---|
| Ch1 | 3000 × 2 = 6000(`price`·`count`·`total`), `hello.py` → `총액: 6000원`. 실습 폴더 = `labs/…`, 연습 폴더 = 학생이 만든 폴더 |
| Ch2 | 무선 키보드 39000 × 2, 할인 0.1 → 70200, `calculate_line_total(unit_price: int, quantity: int = 1) -> int`, `OrderLine(name, count)`, `orders.txt`(연필,3/노트,2) → 합계 8000, `bad_orders.txt` → 5000 |
| Ch3 | `team.git`, `author`·`reviewer`, `.gitignore` `.env`/`__pycache__/`/`*.log`, `config.txt` `discount=10`, 더미 키 `DEMO-ONLY-NOT-A-REAL-SECRET` |
| Ch4 | **O101 C001 paid 32000 / O102 C002 pending 18000 / O103 C001 paid 27000**, 합계 77000·결제 완료 59000. **C001 김하나·C002 이두리**(C003 = 고객 표에 없는 번호). `fetch_orders(file_name: str, status: str) -> list`, `find_customer_orders`, `fetch_all_orders`, `run_pipeline` → `{'김하나': 59000, '이두리': 18000}` |
| Ch4 파일 | **`labs/part1/ch04-data-tools/data/article-text.json`**(기사 A10 「골목상권 매출 회복」, SHA-256 `e2418544…a93103d1`): Ch5 01이 읽고 `run_course_bundle.py`가 바이트 비교 → **바꾸지 않음** |
| Ch4 실습 폴더 | `data_tools.py`(고치지 않음): **`fetch_orders(csv_path, *, status=None)`**, `find_customer_orders(database, customer_id)`(키 다름, 금액 내림차순), `fetch_articles`, `parse_article_html`. `data/orders.csv`에 O104 C003 cancelled 9000. **Ch19 01이 이 판을 씀** → 01절 모양과 차이를 잇거나 맞출지 결정 |
| Ch5 | `model_name`·`tokenizer`·`model`, `cosine_similarity`(02), `make_input_text`(04), `ask_model(input_text)`(05·07), `make_input(system_text, user_text)`·`find_numbers`·`find_new_numbers(answer, source_text)`(07), `pick_document`(09). 지어낸 「초록 패스」(300만 원)·「노을 워커 3」(4200mAh), 「해바라기 작전」 314159. 지시 `"주어진 문서 범위에서만 답하세요."`, 보류 `"제공된 정보로는 확인할 수 없습니다"` |

**비유 계열**(뜻이 바뀌면 그림 읽기에 적음): Ch3 **창고 선반**(열린 상자 = 색인, 봉한 상자 = 커밋, 선반 = main, 깃발 = 브랜치 이름, 열쇠 = 시크릿) → Ch4 **쟁반·카드 상자·서류철**(쟁반 = 한 페이지, 빈 쟁반 = `None`, 카드 꽂이 = 기본 키) → Ch5 **나무 쟁반·블록**(블록 = 토큰 → 문장 → 후보 조각, 칸막이 쟁반 빈칸 = 출력 몫) → Ch6 01-5 **쟁반 = 하네스** → Ch7·8 **한 책상 색 약속**(파란 명찰 = system, 주황 클립보드 = developer, 노란 메모지 = user) → Ch10 **도막**(문서 청크) · Ch11 **흰 카드/색 딱지**.

## 2. 이어 쓸 데이터·이름·함수와 runs 사슬 — Part 2

| 챕터 | 이어 쓸 것 |
|---|---|
| Ch6 | `StudyCard`(concept·explanation·difficulty 1~3), 오타 `gpt-5.4-mimi`, `timeout=0.001`, `mini_prices`·`nano_prices`, 요금표는 응답한 모델 이름으로 |
| Ch7 | `persona_text`(친절한 고객 상담원), **A-1042 텀블러 뚜껑 교환 문의**, `task_text`(네 글), `check_words`, `allowed_labels = ["배송", "교환", "환불"]`, `required_keys`(`category`·`next_action`·`customer_message`), `check_layers`·`build_prompt` |
| Ch8 | 미르시립도서관 안내 담당자, `[E01 p.2]`, **예산 600 · 예약분 120 · 여유분 40 → 가용분 440**(추정−실제 14), 기록 **E01**(p.2 휴관·p.3 대출·p.5 주차)·**E02**(p.5 주차·p.2 급여)·**E04**(p.2 대출), `loan_note`·`closure_note`(테스트 요구), `input_budget`·`count_tokens`·`find_missing_words`·`ask_library` |

- 주의: Ch8 `context_lab.py`는 개선 전 영어 모양(노트북 안 씀), E01 글은 pypdf 띄어쓰기를 사람이 고친 글.
- **공용 함수** `timed_invoke(run_model, input_messages)` → `(응답, 걸린 초)`(Ch6 06·Ch7 01), `make_prompt_record(condition, run_response, run_elapsed)` + `add_cost_items()`(Ch7). §2-7 뒤 Ch7은 `timed_invoke`·`make_prompt_record`·07 검사 함수를 `labs/part2/ch07-prompt-engineering/notebooks/llm_tools.py`에서 가져옴(검사 함수는 `required_keys`·`allowed_labels`를 인자로). Ch6 `estimate_cost(usage, 세 요금)`(기본값 없음) ≠ `estimate_openai_cost(usage, input_rate=0.75, cached_input_rate=0.075, output_rate=4.50)`(Ch7 08·Ch8, 테스트가 인자 하나로 `0.000093`).
- **요청 기록 칸** Ch7 08 키 9개 `조건`·`답`·`응답한 모델`·`입력/캐시 입력/출력 토큰 수`·`끝난 이유`·`걸린 초`(`round(…, 2)`)·`예상 비용(달러)`.

**runs 사슬 최종 상태**(`labs/part2/<챕터>/runs/`, Ch8 06 2026-09-17 12:16:54로 끝)

| 파일 | SHA-256 | 계약(바꾸지 않음) |
|---|---|---|
| ch06 `provider-comparison-continuity.json` | `f18920c6…4f4c` | 키 6개, `pricing["openai"]`·`["date"]` |
| ch07 `prompt-ab-continuity.json` | `a8aaafb7…95e9` | 키 6개, `source_record{path, sha256, run_id}` = Ch6, `versions` 목록 3개, 사본 `continuity/20260917T070701/` |
| ch07 `prompt-ab-continuity.json` — **§2-7 리팩터로 바뀜(2026-09-21) 전 → 후** | `a8aaafb7…95e9` → **`434640f4…a561`** | run_id `ch07-prompt-ab-20260917T070701` → `ch07-prompt-ab-20260921T034935`, 사본 `continuity/20260921T034935/`(옛 사본은 Ch7 `qa/upgrade/before-2-7/runs/moved/`). 계약(키 6개·출처 Ch6·요금·`versions` 3개) 같음. **Ch8 06 재실행 전까지 Ch8 출처 끊김** |
| ch08 `context-design-continuity.json` | **`125fc147…58ad`** | 키 7개, 출처 = Ch7, `results` 목록 3개, 사본 `continuity/20260917T121654/` 하나 |
| ch08 `context-design-continuity.json` — **§2-7 리팩터로 바뀜(2026-09-21) 전 → 후** | `125fc147…58ad` → **`043750ee…a5d2`** | run_id `ch08-context-20260917T121654` → `ch08-context-20260921T050226`, 출처 = Ch7 `434640f4…a561`, 사본 `continuity/20260921T050226/`(옛 사본·A 실행 사본은 Ch8 `qa/upgrade/before-2-7/runs/moved/`). 계약(키 7개·요금·`results` 3개·같은 바이트 사본) 같음. **Ch6 → 7 → 8 사슬 이어짐** |
| ch07 `prompt-ab-v1.json`·ch08 `ex0*.jsonl`·`data/memory.json` | Ch8 요약 §9 | 바꾸지 않음 |

- **다시 실행 금지**: Ch6 06·Ch7 08·Ch8 06. 꼭 고치면 이 순서로 함께 재실행하고 인용 숫자를 모두 새로. 실습 절은 파일을 안 씀.
- **읽는 쪽**: Ch8 `tests/`, `check_course_continuity.py`·`run_course_bundle.py`·`build_bundle.py`(Ch9 이후 노트북은 안 읽음).
- **R-1** Ch6 06·Ch7 08은 실습 폴더 맨 위에서 열면 경로를 못 찾음 / **R-2** Ch8 06은 다른 챕터 `notebooks`에서 열면 그 챕터 `runs/`에 씀(둘 다 안내 문장만).
- **테스트** Ch8 21 passed(연결 5 + 예제 16). `check_course_continuity.py`는 212행 `Stale archive: part1-practice.zip`에서 멈춤.
- **§2-7 리팩터(2026-09-21)**: Ch7 08을 새 커널로 다시 실행(도구 파일 가져오기)해 위 ch07 해시가 바뀜 → Ch8 테스트 20 passed · 1 failed(`test_continuity_logs_form_a_hash_verified_chain` 127행 ch08 출처 run_id). **Ch8 06을 새 커널로 다시 실행해 사슬을 잇는 일이 남음**(Ch8 리팩터 작업자). 세부 Ch7 `qa/upgrade/handoff.md` 「§2-7 리팩터」.
- **§2-7 리팩터 Ch8(2026-09-21)**: Ch8 06을 새 커널로 다시 실행해 위 줄의 남은 일을 끝냄 → ch08 해시 `043750ee…a5d2`, Ch8 테스트 **21 passed**(`test_ch06_ch08_continuity.py` `load_function()`이 노트북의 `from llm_tools import`를 확인한 뒤 `notebooks/llm_tools.py` 정의를 읽도록 고침, 확인 성질 같음). Ch8은 앞 절·Ch7 08 함수 9개를 `labs/part2/ch08-context-engineering/notebooks/llm_tools.py`에서 가져옴(`count_tokens(encoding, text)`·`build_notes_messages(persona_text, task_text, notes, question)`·`check_answer(answer_text, notes, keep_words)` — 인자로 받는 모양). `estimate_openai_cost`는 Ch7 08 노트북·Ch8 도구 파일 두 곳(본문 같음). `check_course_continuity.py`는 이제 `llm-practice.zip` Stale에서 멈춤. 세부 Ch8 `qa/upgrade/handoff.md` 「§2-7 리팩터」.

## 3. 이어 쓸 데이터·이름과 산출 파일 계약 — Part 3

| 챕터 | 이어 쓸 것 |
|---|---|
| Ch9 | `labs/data/rag-corpus/pdf/easy/E01.pdf`(5쪽, 쪽 글자 수 45·905·925·871·270). **500/50 문서 청크 8개**, 300/50이면 14개. 디지털 PDF 18건 = 쪽 93·문서 청크 176. `closure_question`(45자)·06절 **Q001 짧은 질문**(평가셋과 글자까지 같음)·`closure_keep_words`·`closure_answer_sources=["E01 p.2"]`·`abstain_sentence`(Ch5 07) |
| Ch10 | **2쪽 905자**가 01·02·05·06·07절의 나눌 글. 18건 93쪽 62,512자, `pdf/hard/H05.pdf` 세 쪽 모두 0자 → **글이 있는 문서 17건**. `fixtures/` 다섯(`sample.docx`·`sample.html`·`sample.csv`·`legacy-signature.hwp`·`minimal-marker.hwpx`). 05절 목표 200자·08절 400자 여섯 설정 |
| Ch11 | 평가셋 `ch11-evaluation/data/evaluation-queries.jsonl` **30줄·칸 7개**, easy/medium/hard 10씩, **dev 15 / test 15**, 정답 문서 여섯(E01 6·E02 4·M01 8·M02 2·H01 8·H02 2), 질문마다 정답 **한 개**. 기준선 다섯 셀 → 색인 쪽 90·글 있는 문서 17. `candidate_count` **50**(줄이지 말 것)·`cutoff_narrow` 5. **개발 15문항 자리 5 값 `0.867 \| 0.173 \| 0.751`** |
| Ch12 | **core 벌** 문서 **12개**·질문 **8개**(`C01`~`C08`) = 01~06절. **advanced 벌** 부모 **6건**·문서 청크 **175개**·질문 30개(Ch11 평가셋 복제본) = 07~13절, 자주 쓴 `Q002`·`Q085`. **1차 검색 = 두 순위를 `fuse_rank()`로 합친 앞 여덟 개**(07~13절 공통). 손잡이 = 06절 가중치 6 × 10절 관련성 비중 6 = **36벌** |

**두 벌·두 챕터의 숫자를 나란히 놓지 않습니다**(Ch12 07 b3·07~13절 b7; Ch11 값과는 01 b7에 한 번만). **개발 15 / 시험 15 약속** = 개발로 고르고 시험은 다 고른 뒤 한 번(Ch11 여섯 절, Ch12 07절 인용 → 12절 9절에서 처음 엶).

| 기록 파일 | 쓰는 절 | 줄·키 | SHA-256 |
|---|---|---|---|
| `ch09-…/runs/continuity-ch09-search.jsonl` | Ch9 06 | 한 줄. 최상위 8키(`qid`·`question`·`gold_doc_ids`·`source_chapter`·`source_run_id`·`config`·`retrieved`·`answer`), `config` 7키, `retrieved` 5키(`doc_id`·`chunk_id`·`page`·`rank`·`score`). **k=2** → @5 셋 `None`·`recall_at_logged_candidates 1` | `294713765a11…` |
| `ch09-…/runs/continuity-ch09-search.jsonl` — **§2-7 리팩터로 바뀜(2026-09-21) 전 → 후** | Ch9 06 | 계약 같음(8키·`config` 7키 값 같음·`retrieved` 5키·**k=2**·`chunk_id` `ch09:6f9f83db90:0`/`:1`·순위·쪽·답 글자). `source_run_id` `20260917T181822-ch09` → `20260921T055009-ch09`, `score` `0.6492`·`0.5647` → `0.6491`·`0.5653`. 사본 `continuity/20260921T055009-ch09.jsonl`(옛 사본 9개 그대로, A 실행 사본은 Ch9 `qa/upgrade/before-2-7/runs/moved/`) | `294713765a11…` → **`e0323e897794…`** |
| `ch10-…/runs/continuity-ch10-indexing.jsonl` | Ch10 08 | **6줄**. 최상위 7키(**`answer` 없음**), `config` 6키(`dimensions` 1536·`k` **5**), `retrieved` 항목 5개. 실행마다 `recall_at_5 1`·`precision_at_5 .2`·`ndcg_at_5 1`·`recall_at_50 None` | `58cc790c45df…` |
| `ch10-…/runs/continuity-ch10-indexing.jsonl` — **§2-7 리팩터로 바뀜(2026-09-21) 전 → 후** | Ch10 08 | 계약 같음(6줄·7키·`config` 6키 값 같음·k=5·`retrieved`의 `doc_id`·`chunk_id` `ch10:char:0000`·`page`·`rank` 모두 같음·지표 같음). `source_run_id` `20260918T061902-ch10-0N` → `20260921T062600-ch10-0N`, `score` 일부 소수 넷째 자리 아래만 다름. 사본 `continuity/20260921T062600-ch10-0N.jsonl`(옛 사본 48개 그대로, A 실행 사본은 Ch10 `qa/upgrade/before-2-7/runs/moved/`) | `58cc790c45df…` → **`0984e1679db1…`** |
| `ch11-…/runs/notebook-run-20260918.json` · `continuity-upstream-20260918.json` · `upstream-top2-20260918.json` | Ch11 06의 8·9·12절 | 첫째는 06 노트북이 다시 읽음(이름에 `continuity`가 없어 증거 폴더로 안 옮겨짐), 둘째는 `finalize…py` 49행이 `continuity-upstream-*.json` 중 **가장 새 파일**을 고름, 셋째(`--top-k 2`)는 읽는 쪽 없음 | — |
| `ch11-…/runs/notebook-run-*.json` · `continuity-upstream-*.json` · `upstream-top2-*.json` — **§2-7 리팩터로 바뀜(2026-09-21) 전 → 후** | Ch11 06 | 06을 새 커널로 다시 실행해 `*-20260921.json` 세 개가 **새로 생김**(20260918 세 개는 그대로, 이름이 날짜라 덮어쓰지 않음). 새 `continuity-upstream`은 20260918 판과 키·실행 수 7·`query_ids`·지표·순위가 같고 `run_date`·실행 `run_id` 7개(지금 Ch9·10 기록의 `source_run_id`와 맞음)·`score`만 다름. `runs/` 14 → 17개, 기존 14개·`before-manifest.json` 10개 바이트 불변 | 묶음 `6b891bf97b31…` → **`589d400dcbf5…`** · `continuity-upstream-20260921.json` **`7ef93f8b0e59…`** · `notebook-run-20260921.json` `32d473281e31…` · `upstream-top2-20260921.json` `660de0ccbbf1…` |
| `ch12-…/runs/advanced-continuity-experiment-log.jsonl` | Ch12 12 | 개발 **36줄**, 한 줄 **17칸**, `settings` 7칸, `results` 15줄 | `9b447a41…` → §2-7 리팩터로 바뀜 `f16aa358…` |
| `…/advanced-continuity-test-result.json` | Ch12 12 | 시험 15문항 한 번, `selected_run_id`·`comparison_policy`. `ndcg_at_5 < 1`인 줄 **1개**(`Q090`) | `f9b16717…` → §2-7 리팩터로 바뀜 `7b9b9db7…`(`run_id`·`selected_run_id`·`run_date` 말고 내용 같음, `ndcg_at_5 < 1` 여전히 `Q090` 한 줄) |
| `…/advanced-continuity-integrated-result.json` | Ch12 12 | 스모크 1건(`generation_smoke_test`, `Q002`), `retrieval_metrics` `None`. `dimensions` **256**·`chat` **`gpt-5.4-mini`**·`reranker` **`null`**·`context_selection` `matched-chunk-text` | `ce76d3d8…` → §2-7 리팩터로 바뀜 `7b142cd5…`(`run_id` 말고 내용 같음) |

- `chunk_id` 세 모양: `ch09:6f9f83db90:0` / `ch10:char:0000`(네 자리) / `E01-P03-C01`. 읽는 쪽은 빈 값인지만 보지만 나란히 보면 섞입니다. Ch12 `metrics` 여섯 칸(`recall_at_3`·`recall_at_5`·`recall_at_50`·`precision_at_5`·`ndcg_at_5`·`chunk_precision_at_5`)은 **반올림하지 않고 저장**, 검사가 **다시 계산하는 칸은 네 개**(`abs_tol=1e-10`). `question`·`gold_doc_ids`는 평가셋 Q001과 글자까지 같고 `config` 안에 넣지 않습니다.
- **기록 한 줄 칸 수**: Ch9 8칸 · Ch10 7칸 · Ch11 7칸 한국어 키 · Ch12 17칸.
- **읽는 쪽**: `evaluate.py` 176~254행 · `part3/qa/check_continuity.py` 44~46·58~78·81~137·138~159행(85행 `len(experiments)==36`, 127~129행 사본) · `qa/check_course_continuity.py` 43·50·94~112·115~180·172~199·212·216·**219행** · `run_continuity_bundle.py` 19·45~54·79~83행 · `finalize_continuity_evidence.py` 15·37·44~59행(51행 `len(source_ids)==7`) · Ch11 06 노트북(줄 수만) · Ch12 `tests/test_continuity.py` 61~129행 · Ch13 `qa/author_ch13.py`(출력만) · **Ch15 `_author.py` 210~212행(깨짐 — 마감 파일 「뒤 챕터 인계」)**.
- **사본**: Ch9 1 + 옛 8, Ch10 6 + 옛 24, Ch12 `runs/continuity/20260918T232052/`(§2-7 리팩터로 바뀜 → 지금 정본 사본 `20260921T082024/`, 옛 사본 8개 그대로). **앞 사본은 지우지 않습니다**(`check_course_continuity.py` 184행이 옛 정본의 줄마다 그 이름을 찾음).
- **고치지 않는 계약 파일**: 평가셋 `9544b332…`(Ch12 `advanced-queries.json`과 완전히 같아야 함) · `evaluate.py` `41c9408f…` · `test_evaluate.py` `d738970f…` · Ch11 `runs/baseline.json` `4ec8435c…`·`notebook-log.json` `6ef314fe…`(`before-manifest.json`이 바이트로 봄) · Ch12 `runs/core-01~06-*.json` · Ch9 `harness.py`·`prompts.py`·`rag.py` · Ch10 `document_processing.py`·`experiment.py`·`fixtures/` · `labs/data/rag-corpus/` 전체. **Ch6~8 비용 사슬은 Part 3가 읽지도 쓰지도 않습니다.**
- **Ch13(2026-09-19)**: `runs/`에 **쓰지 않습니다**. 읽는 파일은 Ch12 `data/advanced-documents.json`(07·08절)과 `runs/advanced-continuity-integrated-result.json`(07절만)뿐이고 둘 다 바이트가 그대로입니다. `labs/part4/ch13-langgraph-basics/runs/graph-integrated-result.json`은 **개선 전 07절이 남긴 파일**이고 지금 교재와 값이 다릅니다(`reranker`·`duration_ms`·`retrieved`). 코드로 읽는 쪽 0건이고 묶음 목록 두 곳에 **명시 한 줄**로만 있습니다(`textbook/part4/public-files.json` 12행 · `ch13-…/qa/public-files.json` 10행). 삭제 승인과 목록 정리는 마감 파일 참고. **§2-7 리팩터 Ch13(2026-09-21)**: 07이 읽는 통합 기록은 이제 **`7b142cd5…`**(Ch12 §2-7 판)이고 07 노트북 3절이 읽은 일곱 값(`Q002`·`['E01']`·`E01-P03-C02`·`C01`·`C06`·`None`·`matched-chunk-text`)이 리팩터 전 출력과 같습니다. `advanced-documents.json` `832d89c2…` 그대로. 07 노트북·본문은 해시를 인용하지 않아 챕터 요약·검토 보고서의 옛 해시에만 「§2-7로 바뀜」을 덧붙였습니다. 여전히 `runs/`에 쓰지 않고 `graph-integrated-result.json` `c704a2eb…` 그대로입니다.
- **Ch14 자료·이어 쓴 것(2026-09-20)**: `labs/part4/ch14-rag-patterns/data/documents.json`·`queries.json`은 Ch12 **core 벌**(`core-documents.json`·`core-queries.json`)과 **바이트가 같습니다**(문서 **12건** · 질문 **8건** `C01`~`C08`). **advanced 벌이 아닙니다** — Ch13 07·08절 값과 섞지 마세요. 함수 여덟을 이름·인자·코드까지 같게 다시 정의: 거리 넷과 `rank_by_distance`(Ch12 01·**05절 판** — §2-7 리팩터로 Ch12 쪽은 바뀜: Ch12 도구 파일 판은 `rank_by_distance(question_vector, doc_vectors, doc_ids, top_count)` 인자 넷·NumPy `np.argsort`이고 거리 넷 가운데 `cosine_similarity`(Ch5 02 NumPy)·`cosine_distance`만 남음. Ch14 §2-7 작업자가 맞출 것) · `print_ranked`·`unique_doc_ids`·`find_gold_rank`(Ch11 01절), 02·03·09절은 `fuse_scores`·`fuse_rank`(Ch12 06절)를 더함. **정본은 모두 `qa/upgrade/author_NN.py`.** 값 `top_all` **12**·`top_three` **3**·`similarity_top` 1·`dimensions` **256**·임베딩 `text-embedding-3-small`·답 모델 **`gpt-5.4-mini`**(`temperature=0`·`reasoning_effort="none"`).
- **Ch14 산출 파일 하나, 09절이 다시 씁니다** — `labs/part4/ch14-rag-patterns/runs/pattern-comparison.json`, `8b1fd13cd844…` → **`94d10997803eabdc37111b484bc832ccaf6d2e07b6ebd4c9855b0311de897f50`**(4540 → 4454바이트). 칸은 머리 다섯(`chat_model`·`embedding_model`·`embedding_dimensions` 256·`document_hash`·`query_hash`) + `rows` **아홉 줄**(줄마다 칸 일곱 `pattern`·`qid`·`question`·`gold_doc_id`·`found_ids`·`rank`·`service_calls` — 산출 파일이라 칸 이름만 영어). **코드로 읽는 곳 0건**, 묶음 허용 목록 둘에 경로 있음(`ch14-…/qa/public-files.json` 18행 · `textbook/part4/public-files.json` 28행). **01~08절과 10절 실습 절은 파일을 쓰지 않습니다.**
- **Ch14 절별 정답 문서**: 01 `FAC-001` · 02 `LIB-001`·`LIB-002` · 03 `FAC-003`·`ACC-003`(값 바꿔 보기 `ACC-002`) · 04 `FAC-004` · 05 `LIB-004` · 06 `FAC-002` · 07 `LIB-003` · 08 `ACC-001`·`ACC-004` · 09 `LIB-002`·`FAC-003`·`ACC-001` · 10 실습 `LIB-002`. **문서 열두 건이 모두 한 번 이상 쓰였고 아직 안 쓴 자료 질문은 `C04`·`C07` 둘뿐**입니다. **Ch15가 전제하면 안 되는 것**: 답 품질 판정(정답률·근거 충실도·LLM 판정자·평가 벌·회귀 검사)과 검색 품질 지표(`Recall@3` 포함, Ch11·12 몫) · 걸린 시간·토큰·비용 · 여덟 질문 전체 비교 · advanced 벌·그래프·리랭커·pgvector·MMR·BM25·kiwipiepy(열 절 0건) · 기준값으로 문서를 거르기(06·07절은 다시 검색할지·고쳐 쓸지만 정하고 08절만 갈래 이름으로 덜어 냄). **07절 근거 점수와 10절 출처 표시는 정답률이 아닙니다.**
- **§2-7 리팩터 Ch9(2026-09-21)**: Ch9 06을 새 커널로 다시 실행(도구 파일 가져오기)해 위 줄의 해시가 바뀜 — (a) 읽는 쪽 확인: `check_continuity.py`·`check_course_continuity.py` ch09 블록 통과, `evaluate.py` ch09 지표 같음(`top_results` 점수만 다름), Ch11 01~06 노트북이 코드로 읽는 키·값 같음(06 출력의 실행 이름 두 줄만 다음 재실행 때 바뀜, Ch11은 재실행 안 함), (b) 본문·그림 인용 없음(06은 점수·실행 이름을 인용하지 않음), (c) 앞 사본 그대로, (d) 이 줄·진행표. Ch9 02~07은 앞 절·Ch8 함수 8개를 `labs/part3/ch09-rag-first-run/notebooks/rag_tools.py`에서 가져옴(`count_tokens(encoding, text)`·`build_notes_messages(persona_text, task_text, notes, question)`·`check_answer(answer_text, notes, keep_words)`). 세부 Ch9 `qa/upgrade/handoff.md` 「§2-7 리팩터」.
- **§2-7 리팩터 Ch10(2026-09-21)**: Ch10 08을 새 커널로 다시 실행(도구 파일 가져오기)해 위 줄의 해시가 바뀜 — (a) 읽는 쪽 확인: `evaluate.py` ch10 여섯 실행 지표 같음(`finalize…py` 54~58행 조건 충족), `check_continuity.py`·`check_course_continuity.py` 기록 블록 통과, Ch11 01~06 노트북이 코드로 읽는 키·값 같음(06 출력의 실행 이름 열두 줄만 다음 재실행 때 바뀜, Ch11은 재실행 안 함), (b) 본문·그림 인용 없음(08은 실행 이름·점수를 인용하지 않고 B 출력이 리팩터 전과 같음), (c) 앞 사본 그대로, (d) 이 줄·진행표. Ch10 01~09는 앞 절·Ch8·Ch9 함수 14개를 `labs/part3/ch10-document-processing/notebooks/rag_tools.py`에서 가져옴(`count_tokens(encoding, text)`는 Ch9 도구 파일 판). 세부 Ch10 `qa/upgrade/handoff.md` 「§2-7 리팩터」.
- **§2-7 리팩터 Ch11(2026-09-21)**: Ch11 06을 새 커널로 다시 실행(도구 파일 가져오기)해 위 줄의 새 파일 세 개가 생김 — (a) 읽는 쪽 확인: `finalize…py` 49~66행 조건을 새 보고서에 돌려 통과(실행 7개 `run_id` = 지금 Ch9·10 `source_run_id`), `run_continuity_bundle.py`는 번들 안에서만 옮김(전체 마감), `check_continuity.py`·`check_course_continuity.py`의 `before-manifest.json` 블록 통과(`llm-practice.zip` Stale에서 멈춤), **Ch12는 Ch11 `runs/`를 읽지 않고 평가셋 `9544b332…`는 그대로**(Ch12 tests 4 passed), (b) 본문 인용은 06 실행 날짜·파일 이름 네 곳과 `_src` 06 용어 표·07 b7 실행 ID만 고침(지표 값은 전과 같음), (c) 옛 20260918 파일 그대로, (d) 이 줄·진행표. Ch11 02~07은 앞 절·Ch9 함수 13개를 `labs/part3/ch11-evaluation/notebooks/rag_tools.py`에서 가져옴(`search(store, question, count, candidate_count)` — 05절 판은 바깥 이름을 읽음). `evaluate.py`·`tests/test_evaluate.py`·평가셋은 고치지 않음. 세부 Ch11 `qa/upgrade/handoff.md` 「§2-7 리팩터」.
- **§2-7 리팩터 Ch12(2026-09-21)**: Ch12 12를 새 커널로 두 번 다시 실행(도구 파일 가져오기)해 위 세 줄의 해시가 바뀜(사본 `runs/continuity/20260921T082024/`, 첫 실행 사본은 `ch12-…/qa/upgrade/before-2-7/runs/moved/20260921T081609/`로 `mv -n`) — (a) 읽는 쪽 확인: 실습 폴더 `tests/` 4 passed, `check_continuity.py`·`check_course_continuity.py` ch12 블록·원본 기록 보존 블록 통과(`llm-practice.zip` Stale에서 멈춤), **Ch13 07이 읽는 `qid`·`question`·`gold_doc_ids`·`retrieved[].chunk_id`·`settings.reranker`·`context_selection`이 같아 Ch13 노트북·본문 영향 없음**(Ch13 문서의 옛 해시 인용만 남음), **Ch15 `_author.py` 211행이 세는 `ndcg_at_5 < 1`은 여전히 1줄**(`Q090`, 212행 기대 2와 어긋난 상태 그대로), (b) 고른 설정 `[0.0, 1.0]`·`1.0`·시험 지표·통합 기록 값이 같아 본문 인용은 12절 7절 두 표(`_src` b6)와 b7 흔들림 문장만 고침, (c) 옛 사본 8개 그대로, (d) 이 줄·진행표·마감 파일. 키·칸 이름·36줄·`chat` `gpt-5.4-mini`·`dimensions` 256 같음. Ch12 01~13은 앞 절·Ch5·Ch8·Ch11 함수를 `labs/part3/ch12-retrieval-tuning/notebooks/rag_tools.py`(33개)에서 가져옴. 세부 Ch12 `qa/upgrade/handoff.md` 「§2-7 리팩터 A」·「§2-7 리팩터 B」.
- **다시 실행하면 안 되는 노트북**: **Ch9 06 · Ch10 08 · Ch11 06 · Ch12 12**. 다시 쓰면 (a) 읽는 쪽 먼저 확인, (b) 본문·그림 인용 값을 새 출력으로, (c) 앞 사본은 그대로, (d) 계약 표와 진행표를 새로. `runs/`에 `continuity-upstream-`을 새로 쓰지 말고, `continuity`가 들어가면 `run_continuity_bundle.py` 79~83행이 증거 폴더로 옮깁니다. **파일을 쓰지 않는 쪽이 가장 안전**(실습 절 넷 선례).

## 4. 함수 재정의·실습 폴더 테스트 계약

- **지표 함수 인자 모양**: `recall_at(doc_ids, gold_doc_ids, cutoff)` 계열은 **이미 중복을 뺀 고유 문서 ID 목록**을 받고 자르기는 함수 안에서. `evaluate.py`의 같은 이름 함수는 `dedupe_docs()`를 안에서 부르는 다른 판 — **섞지 않음**. Ch12 07절부터 `unique_chunk_ids`.
- **`tests/test_evaluate.py` 계약**(Ch11 05 셀을 `ast`로 찾아 실행): 이름 `metrics`·인자 하나 `item`·반환 튜플 `(재현율, 정밀도)`·바깥 이름은 `search` 하나·`cutoff = 5`는 함수 안에서.
- **앞 절 함수 재정의 개수**: Ch9 07 7개, Ch10 09 8개, Ch11 07 13/16개, Ch12 12 24개. 거리 네 개(`dot_product`·`vector_length`·`cosine_similarity`·`cosine_distance`)는 Ch12 01~13절이 글자까지 같음(**§2-7 리팩터로 바뀜** — 아래 Ch12 줄). **이름·인자 모양을 바꾸면 절 사이 표를 못 견주고 실습 폴더 테스트가 멈춥니다.**
- **§2-7 리팩터 뒤(2026-09-21) Ch9**: 07은 재정의 0개 — 여섯 개를 `rag_tools.py`에서 가져오고(`find_cited_notes`는 `check_answer` 안에서만), 02~06도 앞 절·Ch8 함수를 다시 적지 않음. Ch9 `tests/`는 노트북을 읽지 않아 그대로 10 passed.
- **§2-7 리팩터 뒤(2026-09-21) Ch10**: 01~09 모두 앞 절·Ch8·Ch9 함수를 다시 적지 않음 — 09 실습 절 재정의 8개 → 0개(일곱 개 가져오고 `make_local_name`은 `read_body_text` 안에서만). Ch10 `tests/`는 노트북을 읽지 않아 그대로 38 passed.
- **§2-7 리팩터 뒤(2026-09-21) Ch11**: 02~07 모두 앞 절·Ch9 함수를 다시 적지 않음 — 07 실습 절 재정의 13/16개 → 0개(여덟 개 가져오고 `rank_weight`·`dcg_at`·`ideal_dcg`는 `ndcg_at` 안, `make_candidate_list`·`mean_score`는 `search`·`group_mean` 안에서만). 지표 함수 인자 모양은 그대로이고 `search`만 `store`·`candidate_count`를 인자로 받음. `tests/test_evaluate.py` 계약의 `metrics`는 05 노트북에 그대로 남아 테스트를 고치지 않음(8 passed).
- **§2-7 리팩터 뒤(2026-09-21) Ch12**: 01~13 모두 앞 절·Ch5·Ch8·Ch11 함수를 다시 적지 않음 — 12절 재정의 24개 → 0개(import 세 줄로 12개), 13 실습 절 13개 → 0개(8개 가져옴). 도구 파일 `rag_tools.py` 33개: 01~06 구역(칸 `doc_id` — `rank_by_distance(question_vector, doc_vectors, doc_ids, top_count)`·`rank_by_bm25(bm25_model, question_terms, doc_ids, top_count)`·`fuse_rank(ranking_list, weight_list, rank_constant)` 등)과 07~13 구역(칸 `chunk_id` 판 `rank_chunks_by_distance`·`rank_chunks_by_bm25`·`unique_chunk_ids`, `parent_ids_of(…, parent_by_chunk)`, `chunk_precision_at(…, parent_by_chunk)`, `eligible_items`, `count_tokens(encoding, text)`, MMR 다섯 개 `mmr_pick(…, vector_by_chunk)`, Ch11 `precision_at`·`ndcg_at` 계열). 처음 가르친 절(07 `parent_ids_of`·08 `eligible_items`·`chunk_precision_at`·10 MMR)은 노트북 판(바깥 이름을 읽음)을 그대로 둠. **실습 폴더 `tests/test_continuity.py`의 이름 공간이 도구 파일을 먼저 읽도록 고침**(`tool_namespace()`, 확인하는 성질 그대로, 4 passed).
- **§2-7 리팩터 뒤(2026-09-21) Ch13**: 07·08 재정의 11개·12개(`normalize` 포함) → 0개. 도구 파일 `labs/part4/ch13-langgraph-basics/notebooks/rag_tools.py` 16개: 01~06 구역(`print_state`·`normalize`(02 판)·`make_query`·`make_answer`·`ask_more` — 뒤 절이 AST 그대로 다시 쓰던 것만, 02·03·06이 가져감)과 Ch12 검색 부품 구역 11개(Ch12 도구 파일과 AST 같음 — 07·08은 `kiwi_terms(kiwi, text, keep_tags)`·`fuse_rank(…, rank_constant)`·`unique_chunk_ids`·`parent_ids_of(…, parent_by_chunk)`·`rank_chunks_by_distance(question_vector, chunk_vectors, chunk_ids, top_count)`·`rank_chunks_by_bm25(bm25_model, question_terms, chunk_ids, top_count)`을 가져감). `dot_product`·`vector_length`는 없어짐. 노드 `normalize` 01 판·04·05 `clean` 판과 `choose_path`(노트북 `enough_score`를 읽음)는 노트북에 둠. 실습 폴더 `tests/` 없음.
- **준비 셀 묶기 결과**(Ch12): 09절 12개→8셀, 10절 13→9, 11절 14→9, **12절 24→16**, 13절 13→8. **(§2-7 리팩터로 없어짐 — 위 줄)** 함수 본문 10줄·셀 3~12줄(15 상한), 기록된 예외 둘(Ch12 08 `evaluate` 11줄·10 `mmr_row` 13줄).
- **테스트 명령·결과**: Ch8 21 passed(연결 5 + 예제 16) · 실습 폴더 Ch11 `--with pytest==8.4.2`(**8 passed**) · Ch12 `--with pytest==9.1.0`(**4 passed**). `check_course_continuity.py`는 `tomllib`이 필요해 Python 3.11 이상(Ch6 가상환경, 또는 `uv run --project labs/part3/ch10-document-processing`·`ch11-evaluation`). 통과하면 225행에서 결과 파일을 씁니다.
- **`%pip` 셀**(Ch11 02~07)을 넣거나 설치 목록을 바꾸면 dev `pip==26.2`·`uv.lock`·학생 묶음을 함께 확인(규격 §7-2).

## 5. 학생 묶음 허용 목록

- 규격 §7-2(Ch9 B C-1): **묶음 허용 목록(`public-files.json`·`build_bundle.py`)과 금지 목록(`check_delivery.py` 계열)을 함께 확인하고, 묶음을 풀어 경로 셀을 돌려 봅니다.** 절 수를 세는 `_build_index.py`와 과정 단계 검사 허용 목록도 함께 고치고 어디까지 통과하는지 적습니다(Ch9 B C-2·R-1).
- **정답키 공개 정책**(Ch9): `queries.jsonl`을 학생 묶음에 넣고 세 delivery 검사 금지 목록을 바꾸는 안 → **사용자 결정 2026-09-18: 현재 상태 유지**.
- 경로 셀은 **묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리**에서 확인합니다. Part 3 실습 절 넷은 파일을 쓰지 않습니다.
- Part 3 마감 시점 상태: `part3-practice.zip` **92항목**, `Part 3: 36 verified sections`, `check_delivery.py` 통과(노트북 36).
- **§2-7 리팩터 Ch9 뒤(2026-09-21)**: `textbook/part3/public-files.json`에 `labs/part3/ch09-rag-first-run/notebooks/rag_tools.py` 추가 → `part3-practice.zip` **93항목**(`Part 3: 36 verified sections; 90 bundled files`, `df60a02b…7666`), `check_delivery.py` 통과(코드 셀 1036). `part4-practice.zip`은 이 목록을 상류로 읽으므로 다시 만들어야 새 Ch9 기록·도구 파일이 들어감(전체 마감).
- **§2-7 리팩터 Ch10 뒤(2026-09-21)**: `textbook/part3/public-files.json`에 `labs/part3/ch10-document-processing/notebooks/rag_tools.py` 추가 → `part3-practice.zip` **94항목**(`Part 3: 36 verified sections; 91 bundled files`, `040e53ea…45bc5`), `check_delivery.py` 통과(코드 셀 1006). `part4-practice.zip`은 새 Ch10 기록·도구 파일도 아직 없음(전체 마감).
- **§2-7 리팩터 Ch11 뒤(2026-09-21)**: `textbook/part3/public-files.json`에 `labs/part3/ch11-evaluation/notebooks/rag_tools.py` 추가(챕터 `qa/public-files.json` 새로) → `part3-practice.zip` **95항목**(`Part 3: 36 verified sections; 92 bundled files`, `e7f18258…fa6fb`), `check_delivery.py` 통과(코드 셀 956). `part4-practice.zip`은 Ch11 도구 파일도 아직 없음(전체 마감).
- **§2-7 리팩터 Ch12 뒤(2026-09-21)**: `textbook/part3/public-files.json`에 `labs/part3/ch12-retrieval-tuning/notebooks/rag_tools.py` 추가(작업자 A, 챕터 `qa/public-files.json` 새로) → 챕터 마감(작업자 B)에서 `part3-practice.zip` 재생성 **96항목**(`Part 3: 36 verified sections; 93 bundled files`, `c6dea7c1…077aac5a5`, 새 12절 기록 세 개 포함), `check_delivery.py` 통과(코드 셀 827). 묶음을 풀어 `notebooks/`에서 10절을 PYTHONPATH 없이 새 커널로 돌려 통과. `part4-practice.zip`은 Ch12 도구 파일·새 12절 기록이 아직 없음(전체 마감).
- **§2-7 리팩터 Ch13 뒤(2026-09-21)**: `textbook/part4/public-files.json`(08 노트북 줄 아래)과 챕터 `qa/public-files.json`(`include`)에 `labs/part4/ch13-langgraph-basics/notebooks/rag_tools.py` 추가 → `part4-practice.zip` 재생성 `2baa4786…` → **`484a448ddb54d527…`**(`Part 4: 32 verified sections; 94 bundled files`, 89 → 94파일·97항목). **Part 3 목록을 상류로 읽어 Ch9·10·11·12 `rag_tools.py` 넷과 Ch9·10·12 새 기록도 이번에 함께 들어감**(Ch14 10 노트북 2026-09-20 수정분도). `check_delivery.py`는 `part4-practice.zip` 통과 뒤 `llm-practice.zip` Ch1 01절에서 Stale(전과 같은 자리). 묶음을 풀어 `notebooks/`에서 08절을 PYTHONPATH 없이 새 커널로 돌려 통과.

## 6. pgvector 실행 방법 (Ch12 01~03)

- 본문은 학생 기준 **Docker**: `pgvector/pgvector:0.8.2-pg17`, 컨테이너 `hankyung-part3-pgvector`, `postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab`, 표 `ch12_core_hnsw`·`ch12_core_filter`.
- **작업 VM에는 Docker가 없어** conda-forge PostgreSQL을 `.cache/vm/pgenv`·`pgdata`에 두고 같은 접속 정보로 띄웁니다. 교재 출력은 **PostgreSQL 17.11 · pgvector 0.8.1**, 판 번호 갈래 셋(필수 최소 0.7.0 / 교재 출력 / 공식 문서 v0.8.6).
- `run_section.sh`가 절 실행 직전 `qa/upgrade/pre_exec.sh`를 source 하고 그 스크립트가 `pg_ctl start` 뒤 `SELECT 1`로 열 번까지 기다립니다. **기기 셸은 호출이 끝나면 서버도 꺼지므로 절 실행마다 다시 켜집니다.**

## 7. 리랭커 둘 (Ch12 07·08, 로컬 CPU)

- `max_length=256`, **revision 고정**: `BAAI/bge-reranker-v2-m3` `953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e`(약 2.2GB, 07절 최대 RSS 약 **3.1GB**) · `Dongjin-kr/ko-reranker` `8c2ab1a833734491…`(약 1.1GB).
- 08절은 **한 모델씩 올렸다 내려** 최대 RSS 2.76GB(VM 3.8GB), 준비물·README에 「메모리 약 3GB」. 표·그림은 **A·B**로만 부르고, 12·13절은 리랭커를 부르지 않습니다(`reranker` `null`). `HF_HOME=$ROOT/.cache/vm/hf`는 리랭커 둘로 3.8G → **6.0GB**.

## 8. 기준 버전

| 묶음 | 값 |
|---|---|
| 공통 | Python **3.12.13**, uv 0.12.3, Docker 없음, tiktoken 0.14.0, langchain-core 1.6.2, 새 커널 `nbclient==0.11.0`·`ipykernel==7.3.0` |
| Git(2026-09-16) | 출력 2.34.1, 필수 2.28 이상, 설명서 요구 2.36 이상, git-filter-repo 2.47.0 |
| Ch4 | pandas 3.0.5, SQLite 3.53.1, httpx 0.28.1, bs4 4.15.0, lxml 6.1.3, pytest 9.1.1 |
| Ch5 | torch 2.8.0+cpu, transformers 4.56.2, sentence-transformers 5.1.1, `Qwen/Qwen2.5-0.5B-Instruct` 등 revision 고정(Ch5 요약 §7) |
| Ch6~8 | langchain 1.4.0, langchain-core 1.6.2, langchain-openai 1.6.0, openai 3.10.0(Ch8 3.8.0), tiktoken 0.14.0 |
| Ch9 | pypdf **6.17.0**, text-splitters 1.1.2, openai 3.8.0, numpy 2.5.3 |
| Ch10 | pypdf **6.18.0**, pdfplumber 0.11.10, python-docx 1.2.0, bs4 4.15.0, langchain-experimental 0.4.2, langchain-classic 1.0.8, **`langchain` 메인 패키지 없음** |
| Ch11 | pypdf 6.1.1, **numpy 2.5.3**(없으면 `similarity_search`가 `ImportError`), dev `pip==26.2` |
| Ch12 | langchain-openai **1.6.1**, psycopg 3.3.5, kiwipiepy 0.23.2, rank-bm25 0.2.2, sentence-transformers 6.0.1, `numpy 2.5.3`(§2-7부터 01~13절 설치 셀·도구 파일), dev `pip==26.2` |
| Ch13 | langgraph **1.2.11**, langchain 1.4.0, langchain-openai 1.6.1, kiwipiepy 0.23.2, rank-bm25 0.2.2, dev `pip==26.2`. **교재 출력은 작업 환경 `openai 3.16.2`로 만들었고 학생 잠금은 `3.11.0`입니다**(마운트 폴더라 내림 설치가 막혀 맞추지 못함 — `%pip` 여섯 줄에 `openai`가 없고 `langchain-openai==1.6.1`이 요구하는 판을 `3.11.0`이 만족하므로 학생 묶음·출력 표기에는 영향이 없습니다. 판을 맞추려고 07·08절을 다시 실행하지 않았습니다). 잠금에 **쓰지 않는 패키지 넷**(`numpy`·`pypdf`·`scikit-learn`·`sentence-transformers`)이 남아 있음 — 전체 마감 몫 **§2-7로 바뀜(2026-09-21)**: `numpy 2.5.3`을 이제 도구 파일이 씀 — 02·03·06·07·08 설치 셀에 `numpy==2.5.3`(02·03·06은 NumPy를 직접 안 쓰지만 도구 파일이 맨 위에서 import). 쓰지 않는 패키지는 `pypdf`·`scikit-learn`·`sentence-transformers` 셋 |
| Ch14 | 실습 폴더 `pyproject.toml`·`uv.lock`: langchain **1.4.0**, langchain-openai **1.6.1**, python-dotenv 1.2.3, `numpy 2.5.3`, dev `ipykernel==7.3.0`·`pip==26.2`. 교재 출력 환경 Linux · Python 3.12.13. **`numpy`는 열 노트북 import 0건인데 잠금에 남아 있음** — 빼려면 `uv lock` → `uv sync --locked` → `part4-practice.zip`·`llm-practice.zip` 재생성이 함께 필요해 **전체 마감 몫**(Ch12·13 선례) |
| 요금(2026-09-17, 100만 토큰당) | `gpt-5.4-mini` 0.75 / 캐시 입력 0.075 / 출력 4.50 · nano 0.20 / 0.02 / 1.25 · 임베딩 0.02. Part 3은 절마다 0.01달러 아래 |

## 9. 부록 — 새로 가르친 문법·API 자세한 목록

과정 요약 §1은 한 줄 머리말만 싣고, 절 번호·인자까지 있는 자세한 판은 각 챕터 `chapter-summary.md` §1과 아래 표에 둡니다(2026-09-19 분할 때 과정 요약 §1에서 그대로 옮김).

### 9-1. Part 1 (Ch1~5)

#### Python 문법 (A·B 공통)

| 처음 | 문법 |
|---|---|
| Ch1 | 대입, `==`, `print(라벨, 값)`, 목록, 여러 줄 `for`, `len()`, `assert`, `is not None`, `if/else`, `[0]`·`[-1]`, `"""…"""`, `in`·`not`·`and`·`or` |
| Ch2 01~03 | 자료형·`type()`·`int()`, 변수만 넣은 f-string, `elif`·`range`·`while`·`break`·`continue`·`enumerate()`, 슬라이싱, 빈 목록+`for`+`append()`(기본 모양), 튜플 풀어 담기, 딕셔너리 `get(키, 기본값)`·`items()`, `set()`, `sorted()`, `is`/`==`, `copy()` |
| Ch2 04~07 | `def`·`return`·`None`·기본값 매개변수·`round()` / `with open(…, encoding="utf-8")`, 키워드 인자, `try/except 이름 as error` / `class`·`__init__`·`self` / `import`·`from … import`, `__name__`, 타입힌트 `x: int = 1`·`-> int` |
| Ch2 08·12 | pytest, `subprocess.run([...], capture_output=True, text=True)`·종료 코드 / `async def`·`await`·`gather(코루틴, 코루틴)`(하나씩만)·.py의 `asyncio.run(main())`·`to_thread`·`time.perf_counter()` |
| Ch3·4 | 모드 `"a"`, `shlex.split()`, `cwd=` / `import pandas as pd`, `__version__`, `-> list`·`-> dict`, 점 이은 오류 이름, 인자에 딕셔너리 |
| Ch5 | 타입힌트 없는 함수, 함수 안에서 바깥 이름 읽기, 두 겹 `for`, `int(n / 2)`, 튜플 반환, `isdigit()`, `json.loads()`, `math.sqrt()`·`exp()`, 텐서 `.tolist()` |

- **B 전용**(Ch2 09~11, A는 건너뜀): `@` 줄·데코레이터 정의·`*args`/`**kwargs`·`@contextmanager`·`yield`·`try/finally`(09), `BaseModel`·`Field`·`ValidationError`(10), 패키징·`@pytest.fixture`(11). A 순서: 01~08 → 「A트랙 보충 실습」 6과제 → 12 → 13
- **심화 셀만**: Ch2 `__dict__`·parametrize·monkeypatch, Ch5 03 `outputs.logits`. **준비·환경 예외 셀만**: Ch1 `pathlib.Path`·`TemporaryDirectory`, Ch4 `subprocess.Popen`·`os.path.exists` → 모두 기본 경로 전제 금지

#### 도구·API

| 처음 | 도구와 범위 |
|---|---|
| Ch1 02~05 | 터미널·`uv sync --locked`·`uv run`, pdb, git 맛보기(`init`·`add`·`commit`·`status --short`·`diff`) |
| Ch3 01~05 | git: `config`(저장소만)·`diff --cached`·`check-ignore` / bare 원격·`clone`·`push -u`·`switch -c`·`fetch`·`merge --no-ff` / 거절된 push·`pull`·충돌 해결 / `revert`·`worktree`·`reset --hard`·`reflog` / `log -S`·git-filter-repo·`push --force` |
| Ch4 01·02 | pandas: `read_csv(dtype=str)`·`dtypes`·마스크·`loc`·`to_dict(orient="records")`·`to_numeric` / `merge(on=, how="left", validate=)`·`drop_duplicates()` |
| Ch4 03 | sqlite3: `connect`·`execute(sql, [값])`·`commit`·`fetchall`·`IntegrityError`, SQL `CREATE TABLE`(PK·FK)·`INSERT`·`SELECT`·`WHERE`·`ORDER BY`·`JOIN`·`?` |
| Ch4 04·05 | httpx `get(params=, timeout=2.0)`·`json()`·`raise_for_status()` / bs4 `select_one`·`get_text(strip=True)`, robotparser `can_fetch`, `json.dumps` |
| Ch5 01~03 | `AutoTokenizer`(`revision=`)·`tokenize`·`encode`·`decode` / `SentenceTransformer.encode`(384차원)·`cosine_similarity` 직접 / `AutoModelForCausalLM`·`output_attentions=True`·`return_tensors="pt"` |
| Ch5 04~08 | 메시지 딕셔너리 목록·`apply_chat_template(…, tokenize=False, add_generation_prompt=True)`·`generate(input_ids=, max_new_tokens=, do_sample=False)` / `set_seed`·`generation_config`·`do_sample=True, temperature=, top_p=` / `num_parameters()` |

### 9-2. Part 2 (Ch6~8)

| 처음 | API·기법 |
|---|---|
| Ch6 01~02 | `init_chat_model`, 튜플 목록 `invoke`, `.text`(괄호 없음)·`usage_metadata`·`finish_reason`, `max_tokens` / 메시지 클래스, `os.getenv` |
| Ch6 03~04 | `BaseModel`·`Field(ge=, le=)`, `with_structured_output()`·`include_raw=True` / `stream()`·`AIMessageChunk` `+`·`content_blocks` |
| Ch6 05~06 | `timeout=`·`max_retries=`, `with_retry()`·`with_fallbacks()` / `cache_read`, 요금표, `time.strftime`, `json.dumps`·`json.loads`, `os.path.exists` |
| Ch7 01~05 | 역할 `"developer"`·`convert_to_messages` / 과업 명세 / Few-shot / `ChatPromptTemplate`·`MessagesPlaceholder` / `tool_calls`·짧은 근거·CoT |
| Ch7 06~08 | 표본 합의 / JSON 세 층 검사 / 버전 기록·A/B·`hashlib.sha256(바이트).hexdigest()`·`os.makedirs` |
| Ch8 01~06 | `tiktoken`·토큰 예산 / Write·Select / Compress·Isolate / 실패 모드 네 이름 / 길이별 측정 / 단계적 공개 |

- **Python 새 모양**: 원소 하나 튜플, 글 `+`·`split()`·`strip()`, `counts.get(k, 0) + 1`, `range(len(목록))`, `for … in [리터럴]:` + `break`
- **A/B**: `BaseModel`·`ValidationError`는 Ch6 01·03에서 세 문장 + Ch2 10 링크 끝 → 「Ch6 03 양식 클래스」로 이음. `@`는 아직 0건(첫 사용 때 Ch2 09 링크). 엄격 모드·try `finally`는 B만

### 9-3. Part 3 (Ch9~12)

| 처음 | API·기법 |
|---|---|
| Ch9 01~03 | `pypdf.PdfReader`·`pages`·`extract_text()`, `Document(page_content=, metadata=)`, `RecursiveCharacterTextSplitter(chunk_size=, chunk_overlap=)`·`split_documents()`, `OpenAIEmbeddings(model=)`·`embed_query()`, `InMemoryVectorStore`·`add_documents()`·`store.store`·`similarity_search(k=)`·`similarity_search_with_score(k=)`, `tiktoken.encoding_for_model` |
| Ch9 04~06 | `usage_metadata["input_tokens"]`, 출처 인용 검사(`make_note`·`find_cited_notes`·`check_answer`), 하네스 `yaml.safe_load`·`json.dumps(sort_keys=True)`·`os.replace`·`make_index_key`, 색인 이름표·실행 기록 한 줄·JSONL |
| Ch10 01~04 | `os.listdir()`·`sorted(목록)`, `Path(글).name`·`.stem`·`.suffix`, `type(객체).__name__`, `extract_text(extraction_mode="layout")`, pdfplumber `extract_text(layout=True)`·`extract_tables()`, python-docx `paragraphs`·`style.name`·`tables`, bs4 `find_all`·`get_text(" ", strip=True)`, `csv.DictReader(newline=, encoding="utf-8-sig")`, `read(8)`·`hex()`, `zipfile.ZipFile`·`namelist`, `ElementTree.fromstring`·`root.iter()` |
| Ch10 05~08 | `CharacterTextSplitter`·`split_text()`, `RecursiveCharacterTextSplitter(separators=, keep_separator="end")`, `tiktoken.get_encoding()`·`.from_tiktoken_encoder()`, `MarkdownHeaderTextSplitter`·`metadata["heading"]`, `SemanticChunker(breakpoint_threshold_amount=)`, `embed_documents()`·`dimensions=256`, `LocalFileStore`·`CacheBackedEmbeddings.from_bytes_store(namespace=, key_encoder="sha256")`, `str(숫자).zfill(4)` |
| Ch11 01~06 | **지표 함수** `recall_at(doc_ids, gold_doc_ids, cutoff)`·`precision_at`·`rank_weight`→`dcg_at`→`ideal_dcg`→`ndcg_at`(`math.log2()`), `unique_doc_ids`·`find_gold_rank`·`mean_score`·`group_mean`·`error_name`·`metrics(item)`; 06절 `subprocess.run(cwd=)`·`sys.executable`로 `evaluate.py` 실행(실행 ID·지표 규칙 이름·말뭉치 지문) |
| Ch12 01~06 | **pgvector** `psycopg.connect(autocommit=True)`·`execute`·`fetchall`, `CREATE EXTENSION vector`, `vector(256)`·`halfvec`, `<=>`, `CREATE INDEX … USING hnsw`, `EXPLAIN`, `set_config('이름', %s, false)`, `hnsw.iterative_scan`(off·strict_order·relaxed_order)·`max_scan_tuples`, L2 거리·코사인 거리 / **Kiwi·BM25** `Kiwi().tokenize`·`token.form`·`token.tag`, `BM25Okapi`·`get_scores` / **RRF** `fuse_scores`·`fuse_rank`(순위 상수 60·가중치) |
| Ch12 07~13 | **리랭커** `CrossEncoder(revision=, max_length=, device=)`·`predict()`·`.tolist()`, `parent_ids_of`·`rerank`·`chunk_precision_at` / **부모 문서** `tiktoken.get_encoding("o200k_base")`·`parent_texts_of`·`summarize` / **MMR** `mmr_score`·`best_candidate`·`mmr`·`mmr_pick` / **질문 재작성** `rewrite_question` / 12절 `hashlib.sha256`·`write_text`·`evaluate_config`·`log_row`·`knob_mean` + Ch11 04 nDCG 네 함수·03 `precision_at`을 처음 다시 씀 |

**새 모양**: 경로 후보 `for`+`break`, 튜플 반환 목록 풀기, 함수가 딕셔너리 반환, `keys()`·`get(키, 기본값)+1`, `range(len(목록))`+`break`, 딕셔너리 `copy()`, `str(목록)`으로 벡터를 SQL에, **점수에 음수를 붙여 `sorted`**. 드물게 `try/except zipfile.BadZipFile as error`(Ch10 04 Before), `with`(파일·라이브러리 객체), `raise`(Ch12 08·12, 테스트 요구).

### 9-4. 그 밖에 과정 요약에서 옮긴 이름·값

- **출력 함수 이름** `print_hits`·`print_scores` → Ch12 05절이 `print_ranked(hit_list, value_name)`로 합침. 값 칸 이름은 `rank_by_distance` = `거리`, `rank_by_bm25` = `점수`. 도우미 Ch3 `run_git(command, folder=".")`, Ch2 13 기록장 `print_report()`.
- **모델 이름** 생성 `gpt-5.4-mini`(Ch6만 nano도) · 임베딩 `text-embedding-3-small` · 로컬 `Qwen/Qwen2.5-0.5B-Instruct`(revision 고정) · Ch6 오타 실험용 `typo_model`·`gpt-5.4-mimi`.
- **실행 날짜 환경 변수** `nbkit.RUN_DATE` = `UPGRADE_RUN_DATE` 또는 오늘 자동(Ch6 03부터).
- **verify 기대 출력** Ch9 `PASS 7 sections / 175 code cells (max 16 lines)` · Ch10 `PASS 9 / 215 (max 14)` · Ch12 `PASS 13 / 459 (max 20)`(§2-7 리팩터 뒤 `PASS 13 / 330 (max 21)`).
- **자체 `_build.py`(Ch8~10)** Ch8 `inline_mermaid()`·`inline_illustration()`(`_template/builder.py`와 같은 출력)을 가져와 `\{\{[a-z]+:` 잔존·전후 HTML 해시 확인, 실습 절은 `SECTIONS`에 주제까지. `chapter.json`이 없어 `run_section.sh`가 verify를 건너뜀 → `verify.py --chapter` 따로.
- **uv 주의** uv 0.12.13부터 `uv run`이 기존 환경의 `nvidia/cusparselt` 파일을 지우려다 마운트 폴더 삭제가 막혀 `Operation not permitted`로 멈춤 → `UV_NO_SYNC=1`. `UV_CACHE_DIR="$VM/uv"`로 두면 `--with` 덧붙임 환경이 마운트 폴더 안 임시 폴더를 지우려다 멈추므로 uv 캐시는 `/tmp/uv-cache`.

### 9-5. 과정 요약에서 줄인 문장 (원문 참고)

- **설치판 확인 사례**(Ch6~8): `max_retries` None → 재시도 2, `timeout` None → 제한 없음(온라인 「6」·「10분」과 다름), 스트리밍 사용량 기본 켬, developer → `SystemMessage` + `__openai_role__`, tiktoken → `o200k_base`, 반환형 `.text` = `TextAccessor`, `with_structured_output()` → `RunnableSequence`(요청 0번), `stream()` → `generator`. 관찰만 — 양식을 붙이면 입력 61 → 190토큰, 범위 규칙 양식에 9 요구 → 3(서버가 막는 증거 아님), 캐시 입력은 생긴다고 보장 안 함.
- **temperature 0 사례**: 규격 §3 시범은 temperature 0에도 글자 수 398 → 381 → 「매번 비슷한 답, 똑같다고 보장하지 않음」. Ch6 02는 「말투」 → 「톤」. 결론은 「이번 실행에서는」·「질문 두 개·모델 하나·한 번 실행」으로 한정하고, 환각 원인 설명은 「이 로컬 `generate()`에 찾아보는 단계가 없음」까지만 적습니다.
- **출력 읽기 세부**: 모델 답은 `replace("\n", " ")`로 한 줄로 만들고 `<|im_end|>`는 그대로 둡니다. 준비 셀은 `import os`·`import tempfile` → `mkdtemp(prefix="chNN-MM-")` → `os.chdir()` → `os.listdir()`. Ch6 메시지 목록은 `[("system", …), ("user", …)]`, Ch8은 `max_tokens=output_reserve`를 붙여 `KEY` 셀만 씁니다. 키는 루트 `.env`(`find_dotenv(usecwd=True)`), Ch6 02·Ch7·Ch8 생성기는 `RUN_DAY = "2026-09-17"`을 따로 둡니다.
- **`outputs_sha256` 흔들림의 원인**: 첫 셀 `%pip install -q`의 stdout이 stream 조각 둘로 나뉘는 자리뿐이고 출력 글은 같음 → 셀별 출력 글자 해시로 대조(Ch11 §18·Ch12 05절).
- **그림 표기 세부**: 화살표 868을 넘으면 `TB`와 `A ~~~ B`, 점선은 「점선 화살표」로 부르고, 칸 관계는 「위 칸·아래 칸」·「왼쪽 칸·오른쪽 칸」으로 서술합니다. 마지막 가로축 라벨이 테두리를 넘어 `svgBounds`에 걸리므로 라벨을 줄이고 단위는 캡션으로. Ch12 06-3은 세 방법 값이 겹쳐 `flowchart TB`로 바꿨습니다. 노랑으로 바뀐 선례 `print_records`(노랑 → 파랑), 받은 오류 예 `MergeError`·`JSONDecodeError`. 오류 이름은 영문 `candidate_miss` 계열 금지.
- **삽화 실행 세부**: 클라우드 outputs 입출력 오류 → 기기 셸 `curl` + pillow로 폭 1100px 저장·픽셀 대조. `run_section.sh`는 「오늘 볼 그림」 PNG가 없거나 `_src`가 10블록이 아니면 멈추므로 `.mmd`와 자리 표시 `_src`를 먼저 만듭니다. 설명만 고칠 때는 `run_section.sh … NN --no-exec`.
- **Ch12 11절 선례**: 개선 전 `assert "미르시립도서관" in standalone`을 개수 확인으로 바꿨습니다(모델 답 `assert` 금지). Ch8의 「여분 자리」는 Ch7 04 「빈자리」와 같은 뜻입니다.
