# Ch 15 평가 심화 — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part4/ch15-evaluation-advanced` 01~08절(품질 개선) + **09절 챕터 끝 실습 절 신설**, 노트북 `labs/part4/ch15-evaluation-advanced/notebooks/01~09-*.ipynb`, 도구 파일 `notebooks/rag_tools.py`.
- 기간: 2026-09-21(01~08절 개선 · 03·04절 재현성 탐색과 결정 A · 09절 신설 · 검토 1차 반영 · 챕터 마감). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 여덟 절 합계 **236**(절별 38·36·23·30·20·30·17·42, 통과 0/8, `gates-before.json`) → 마감 뒤 **9/9 PASS, G1~G7 모두 0**(`gates-after.json`, 검사 문장 353·374·377·393·376·408·351·390·361 = **3,383**).
- 코드 셀 30·26·25·27·23·28·25·26·23 = **233**(`verify.py --chapter` → `PASS 9 sections / 233 code cells (max 13 lines)`), Mermaid **36장**(절마다 4장), 삽화 **9장**(절마다 1장), 복습 문제는 HTML에만.
- 서비스 요청(노트북 한 번씩 실행할 때): 절별 0·14·8·8·3·3·6·0·4 = **46번**, 모두 평가 모델 `gpt-5.4-mini`, 임베딩 0. 준비물의 절별 예상 비용 상한을 더하면 미화 0.2달러 아래(예상 비용 ≠ 청구 금액).
- 화면 검사 `visual.cjs`: HTML **열 개**(아홉 절 + `index.html`) × 1280px·390px = **20행 모두 PASS**(`textbook/_notebook/checks/ch15-evaluation-advanced/visual-results.json`).
- **노트북 재실행 0건으로 마감**: 아홉 노트북의 `code_sha256`·`outputs_sha256`이 검토 반영 전후 같습니다(설명 셀·첨부 그림만 바뀜).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → 계약 `textbook/qa/upgrade-contracts.md`(§3 「Ch15 산출 파일」 Part 4 표) → Ch 14 요약 → **이 문서**. 절 사이 세부는 `handoff.md`, 절별 기록은 `NN-diagnosis.md`(끝의 §13이 검토 반영), 검토는 `review-round1-A.md`(01~05)·`review-round1-B.md`(06~09)와 이 문서 §15, 재현성 탐색은 `fix-03-04-probe.md`·`07-probe.md`·`09-probe.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 라이브러리·API·문법 | 새로 만든 함수 | 새 용어 |
|---|---|---|---|
| 01 실패 로그와 평가 대상 | 새 API 0(`json.loads`·`with open`·`platform.python_version()`, Ch 11 함수는 도구 파일에서) | `count_answers` · `failure_row` · `find_failures` · `add_count` · `search_mark` · `target_row` | 실패 로그 · 평가 사례 · 검색 쪽 실패 · 답 쪽 실패 · 평가 모델(judge) (5) |
| 02 4대 RAG 평가자 | `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` → `invoke` → `reply.text` → `json.loads`(이 챕터 첫 모델 요청) · 딕셔너리 안의 딕셔너리·`dict.values()`·`dict.copy()`·목록 슬라이스·`type()` | `build_judge_prompt` · `judge_once` · `judge_case` | 정답 일치도 · 답변 관련성 · 근거 충실도 · 검색 관련성 · 판정 머리글 (5) |
| 03 judge 프롬프트와 편향 | 새 문법 0(`hashlib.sha256`은 Ch 7 08 이름 — 머리글 지문) | `score_cases` · `build_pair_prompt` · `picked_name` · `always_first` | 치우침(편향) · 위치 치우침 · 쌍 비교 · 차례 바꾸기 검사 (4) |
| 04 제시 라벨과 일치율 | 새 문법 0 | `box_name` · `count_boxes` · `agreement_rate` · `always_one` · `scores_of` | 제시 라벨 · 일치율 · 네 칸 표 · 한쪽으로 몰린 라벨 (4) |
| 05 로컬 트레이싱과 지연 | `time.perf_counter()`(Ch 2 12·Ch 6 05·06에서 쓴 이름) · `model.stream()`과 스트림 청크 `+`(Ch 6 04) · `usage_metadata`·`input_token_details["cache_read"]` · `json.dumps(…, indent=2)` · 목록 `[-1]` | `make_steps` · `longest_step` · `make_trace` | 실행 추적 · 단계 기록 · 전체 지연 · 첫 토큰 도착 시간 (4) |
| 06 대화당 비용 백분위수 | `math.ceil` · 목록 슬라이스 `[:5]`·`[-5:]` · 목록 `copy()` · `sorted()`(Ch 6 06) · Ch 6 06 `estimate_cost`(도구 파일, 본문의 `.get` 한 문장으로 풂) | `make_request_rows` · `cost_by_conversation` · `average` · `nearest_rank` | 대화당 비용 · 백분위수 · 가장 가까운 자리 방식 · 긴 꼬리 (4) |
| 07 회귀 스위트(paired) | `and`로 두 조건 · `assert not …` | `check_by_average` · `broken_cases` · `check_by_case` | 회귀 · 회귀 스위트 · 기준선 · 통과 조건 (4) |
| 08 Batch 평가 입력 | **이 챕터 첫 파일 쓰기** `with open(…, "w", encoding="utf-8")` + `json.dumps(…, ensure_ascii=False) + "\n"`(Ch 9 06 관례) · `os.makedirs` · JSONL 읽기 · 목록 `+` · 글 `split("-")`·`count()`(마감에서 설명 한 문장 더함)·슬라이스 · 목록 `==` | `make_prompts` · `make_batch_line` · `make_batch_lines` · `write_jsonl` · `read_jsonl` · `line_problems` · `duplicate_ids` · `ids_not_in` | 일괄 처리(Batch API) · 요청 식별자(custom_id) · 요청 주소(url) · 요청 본문(body) (4) |
| 09 실습 | **새 API·새 문법·새 말 0개** | `lines_for` · `send_lines` · `scores_for` · `check_question` · `print_costs` | 0 |

- 새 용어 합계 **34개**(절 meta 「새 용어」 5·5·4·4·4·4·4·4·0과 같음).
- **쓰지 않은 Python 이름(아홉 절 모두 0건, AST 확인)**: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`:=`·`global`·`key=`·`reverse=`·`set`·`setdefault`·노트북의 `.get`·`enumerate`·`zip`·`next`·`all`·`any`·`sum`·`max`·`min`·`+=`·기본값 매개변수·타입힌트·튜플 풀기·`re`·`Path`·`statistics`·클래스 정의. `numpy`는 쓰지 않습니다(도구 파일도 `json`·`math`만).
- 셀 모양: 코드 셀 최대 13줄(`verify.py` 기준), 도구 파일 함수 본문 최대 9줄(검토 B 확인). **모델이 쓴 글·점수·비용에 건 `assert`는 0건**이고 손으로 적은 작은 예·정한 값·줄 수·칸 이름만 `assert` 합니다.

## 2. 앞 챕터에서 이어 쓴 부품과 값

- **Ch 11**: `unique_doc_ids`·`find_gold_rank`(01절)·`rank_weight`(04절)·`error_name`(05절) — 도구 파일에 AST 같게 둠. 말: 정답 자리·자르는 자리·자리 무게·오류 이름 셋(후보 밖·뒤로 밀림·앞자리 안).
- **Ch 12**(읽기만, 보호 파일): `labs/part3/ch12-retrieval-tuning/runs/advanced-continuity-experiment-log.jsonl`(개발 36줄·17칸) · `advanced-continuity-test-result.json`(시험 15문항). `run_id`는 인용하지 않고 고른 설정은 가중치 `[0.0, 1.0]`·관련성 비중 `1.0`으로 가리킴. 01절 값: 자르는 자리 1 → 실패 로그 **27줄**(개발 `Q005` 26 + 시험 `Q090` 1), 자르는 자리 5 → 0줄, `Q090` 정답 자리 2·nDCG `0.6309` = `rank_weight(2)`.
- **Ch 6 06**: `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`(도구 파일, 노트북 셀 18과 글자까지 같음) · 요금표 `pricing_date = "2026-09-17"`·`mini_prices = {"ordinary_input": 0.75, "cached_input": 0.075, "output": 4.50}`(100만 토큰당 달러) · 걸린 초의 가운데 값. **Ch 6 04** 스트림 청크, **Ch 7 08** `hashlib`·기준선, **Ch 2 08** 회귀 테스트, **Ch 9 06** JSONL 쓰기 관례, **Ch 2 12·Ch 6 05** `time.perf_counter()`.
- **Ch 14 07절 근거 점수는 정답률이 아니었습니다** — 01절 b3가 그렇게 잇고 「평가 모델로 답을 여러 기준에서 판정하는 일은 이 챕터가 처음」으로 한정했습니다(검토 A-3).
- **자료 파일** `labs/part4/ch15-evaluation-advanced/data/evaluation-cases.json`(보호 파일 `dc48b1bc…`, 고치지 않음): 사례 세 건 `Q002`(도서 대출, `E01`) · `Q006`(주차장 요금, `E01`) · `Q090`(계약 입회인, `H01` — **모른다고 답하는 것이 기준 답**), 사례 칸 14개, 판정 글 `judge_raw`(판 `groundedness-v1.0.0`, 2026-09-10 한 번 받은 글, Q002·Q006 1 · Q090 0). **머리 칸(`source_experiment_kind`·`created_at`)은 지금 Ch 12와 달라 인용하지 않습니다.**

## 3. 절별 사례·판

| 절 | 사례·입력 | 판정 머리글·판 | 요청 |
|---|---|---|---|
| 01 | Ch 12 기록 두 개 + 자료 사례 세 건 | — | 0 |
| 02 | `Q002`·`Q006`·`Q090` × 평가 넷 | `rag-judge-v1.0.0`(평가 이름 → 머리글) | 14 |
| 03 | 세 건 + 쌍 비교 두 글(짧은 답 43자·긴 답 86자) | `rag-judge-v1.0.0` ↔ `v1.1.0`(문장 하나 더함) · `rag-pair-v1.0.0` · 규칙 함수 `always_first` | 8 |
| 04 | 답 넷(`Q002`·`Q006`·`Q090`·`Q002-바꾼 답`), 제시 라벨 1·1·1·0 | `v1.0.0`·`v1.1.0` · 규칙 함수 `always_one` | 8 |
| 05 | `Q002`(invoke·stream), 값 바꿔 보기 `Q090` | `v1.0.0` | 3 |
| 06 | 세 건 판정 + **이 절에서 정한** 대화 백 개(요청 기록 420줄) | `v1.0.0` | 3 |
| 07 | 이전 판(자료 답) ↔ 이후 판(Q002 바꾼 답·Q090 새 답 — 이 절에서 만든 답) | `v1.0.0` | 6 |
| 08 | 이전·이후 판 판정 요청 여섯 개 → 입력 파일 | `v1.0.0` 요청 글(보내지 않음) | 0 |
| 09 | 입력 파일에서 두 줄씩(실행 1 `Q090`, 실행 2 `Q002`) | 파일에 든 `v1.0.0` 요청 글 | 4 |

- `rag-judge-v1.0.0` 근거 충실도 **Q002 1 · Q006 1 · Q090 0**은 02~07·09절 모든 실행에서 같았습니다. 07 이후 판은 **0 · 1 · 1**(노트북 두 번 + 확인 다섯 번씩), 두 판 평균 모두 `0.666667`, 깨진 사례 `['Q002']`.
- 04절 네 칸 일치율은 이번 두 실행에서 두 판 모두 `0.75`(Q090만 라벨 1 · 판정 0). 06절 정한 목록은 평균 `0.0042`, p50 `0.003`·p95 `0.006`·p99 `0.025`, 대화-100만 두 배이면 평균 `0.0048`·세 백분위수 그대로.

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀)

- 01 실패 로그 · 평가 사례 · 검색 쪽 실패 · 답 쪽 실패 · 평가 모델(judge) / 02 네 평가 · 판정 머리글 · 판정 요청 글 / 03 치우침(편향) · 위치 치우침 · 쌍 비교 · 차례 바꾸기 검사 / 04 제시 라벨 · 일치율 · 네 칸 표 · 한쪽으로 몰린 라벨 / 05 실행 추적 · 단계 기록 · 전체 지연 · 첫 토큰 도착 시간 / 06 대화당 비용 · 백분위수 · 가장 가까운 자리 방식 · 긴 꼬리 / 07 회귀 · 회귀 스위트 · 기준선 · 통과 조건(+ 이전 판·이후 판·깨진 사례) / 08 일괄 처리 · 요청 식별자 · 요청 주소 · 요청 본문(+ 입력 파일·판 표시·제출 전 검사) / 09 **새 말 0개**.
- **제시 라벨은 사람 라벨이 아닙니다**(교재 작성자 한 사람이 판정 전에 적은 라벨). 03절이 04절을 예고하는 문장도 마감에서 「교재가 제시한 라벨과 견주는 일」로 고쳤습니다(검토 A-7).
- **「두 실행」**: 09절에서는 실행 1·실행 2만 가리킵니다. 새 커널 두 번은 「새 커널로 두 번 실행했을 때」로 적습니다(검토 B-13).
- **금지어(아홉 절 0건)**: 「분기」·「경로」·「반환」·「임계값」·「폴백」·「재정렬」·「쿼리」·「인덱스」·「융합」·「RRF」 단독·「조각」·「노드」·「한 겹 더」·「돌려줍니다」·「돌려 보」·「레코드」·「캐시」 단독(「캐시 입력」으로)·「강사 시연」·「개선 전」. 「묶음」은 개발·시험과 학생 묶음 뜻이고 일괄 처리에 쓰지 않았습니다. **예외 한 곳: 03절 제목·파일 이름의 「프롬프트」**(본문은 「판정 머리글」 — §11·§14).
- 「청크」는 「문서 청크」·「스트림 청크」로만(01절 노트북 한 곳을 마감에서 고침, 검토 A-2).

## 5. 색 규칙 (Mermaid 36장, 빨강 1장)

- **자료·기록 파일·넣은 값·이 절에서 정한 값 초록(tool)** · **코드로 정한 처리·기준·도구 파일 함수 파랑(flow)** · **그 절에서 실제로 부른 평가 모델 보라(model)** · **출력으로 확인한 값 노랑(measure)** · **두 칸 공통 사실·실행에서 달랐던 값의 메모 회색(클래스 없음)** · **빨강은 07-3 Before 결과 하나**(잘못 통과시킨 paired 결함).
- 자료 파일의 답·판정 글은 이번에 부른 모델이 아니라 파일에 적힌 글이라 초록입니다(02-4).
- **점선은 「갈래·이번에 하지 않은 일」로만** — 마감 뒤 점선이 남은 그림은 `08-1`(이번에 하지 않은 제출) 하나입니다. 06-1의 평균 쪽과 05-1의 「사용량」 곁 화살표는 실행한 흐름이라 **실선 + 라벨**로 바꿨습니다(검토 B-5, 리드 결정).
- **흔들린 값은 그림 라벨·캡션에 넣지 않습니다**: 03-3 「03절 두 실행에서 같은 점수」, 04-3·04-4 「02절 판」 값 + 「새 판은 이번 두 실행에서 …」, 05-3에서 캐시 입력 1792를 뺌(검토 A-10·A-15).
- 원본 viewBox 폭 **868 이하**(최대 `01-3` 835). 칸 비교는 `flowchart LR/TB` + 칸 안 `direction TB` + `~~~`, subgraph 제목에 `<br>` 금지, 개수는 한글.

## 6. 서비스 요청과 흔들린 값

- 절별 요청 0·14·8·8·3·3·6·0·4 = **46번**(실행 한 번). **일반 절의 요청 수는 강사 확인 대상이 아닙니다**(규격 §7-2 새 줄 — 3~5번은 챕터 끝 실습 절 규칙). 02·03·04·07 진단의 「3~5번 초과」 항목을 「요청 수 기록(일반 절)」으로 고쳤습니다. 09 실습 절은 4번이라 범위 안입니다.
- **03·04 재현성 결정 A**: `rag-judge-v1.1.0`의 Q090은 03절 두 실행에서 1, 글자까지 같은 요청 글(5129자)로 04절 두 실행에서 0이었습니다. 노트북 밖 탐색(`fix-03-04-probe.md`)에서 v1.1.0 Q090 **여섯 번 모두 1**, v1.0.0은 모두 0. 입력·실행 결과는 그대로 두고 문장만 더했습니다 — 03 b7(「04절 노트북 출력에서는 … 0을 냈습니다. 교재 출력을 만든 뒤 노트북 밖에서 같은 요청을 여섯 번 더 보냈을 때는 새 판이 모두 1을 냈습니다」)·03 노트북 결과 읽기와 정리(마감에서 더함, A-6)·04 b6 두 셈 문장(「새 판이 Q090에만 1을 내면 … 1.0」, 마감에서 「값 바꿔 보기에서 … 1.0에서 0.75로」). 03 쌍 비교는 뒤집히지 않았고 04 판 바꾸기 표는 두 판을 가르지 못했습니다 — **설계를 바꾸지 않고** 본문이 그 사실을 그대로 적습니다(강사 확인 §11).
- **06 캐시 입력**: 새 커널 A는 세 요청 모두 캐시 입력 0, B(교재 출력)는 1792·1792·2816 → 출력 토큰·예상 비용도 달랐습니다. 마감에서 b6 둘째 단락의 값·비교(「세 배 넘게」)를 빼고 두 경우(있으면 줄고, 0이면 할인 없는 값과 같아짐)만 적었습니다. 「세 배 넘게」는 노트북 결과 읽기 둘째 단락(「이번 실행에서」)에만 있습니다(리드 결정).
- **05 걸린 초·스트림 청크 수·stream 출력 토큰**은 실행마다 다름. b6은 「교재 출력에서」로 한정한 초 값만 두고 그 값에서 끌어낸 비교(0.993 ↔ 0.994 반올림 설명)를 값 없는 설명으로 바꿨습니다(A-16). 두 실행에서 같은 관찰(가장 긴 단계 = 모델 요청, 첫 토큰 도착 시간 > 전체 지연의 절반, 입력 토큰 수)만 결론·그림에.
- **09 비용 표**: 출력 토큰·예상 비용은 새 커널 두 번에서 다름, 캐시 입력은 두 번 같았지만(2816·2816·1792·1792) 06절에서 흔들려 결론에 쓰지 않음.
- 모든 판정의 까닭 문장은 실행마다 달라 결론·그림에 넣지 않았습니다.
- **규격 두 줄(오늘 사용자가 더함, 마감에서 PLAYBOOK에도 같은 뜻으로 넣음)**: §2-7 9번 끝(흔들린 값은 결과 읽기 둘째 단락·본문 표·「확인할 점」에만, 비교·결론 금지) · §2-7 10번 끝(입력을 고치기 전에 먼저 흔들림 확인) · §7-2(3~5번은 실습 절 규칙).
- **준비물 실행 시간**: 01~07절 준비물을 08·09절과 같은 꼴 「교재 출력을 만든 실행에서는 노트북 전체가 약 N초 만에 끝났습니다」로 맞췄습니다(셀 메타데이터 `execution`의 첫 셀 입력 → 마지막 셀 응답, 커널 기동 제외 — 01 1초 안 · 02 약 14초 · 03 약 8초 · 04 약 9초 · 05 약 5초 · 06 약 5초 · 07 약 7초). 01절의 잰 적 없는 「10초 안팎」은 뺐습니다(A-1·B-7).

## 7. 09절 실습 절 주제와 결과

- 제목 「**평가 심화 실습: 입력 파일에서 두 줄씩 골라 회귀와 비용 보기**」, `format: experiment`, meta 「실습 30분 · 새 용어 0」. **챕터 시수에 더하지 않습니다**(규격 §7-2). 01~08절 meta 합은 강의 8h · 실습 8h로 `chapter.json` `hours` 「총 16h · 강의 8h · 실습 8h」와 같습니다(`_build_index.py`도 8·8).
- 붙인 앞 절 기능 셋: **08절 입력 파일 읽기**(`read_jsonl`·`split("-")`·`ids_not_in`) + **07절 회귀 스위트**(`broken_cases`·`check_by_case`) + **06절 요청 한 번 비용**(`usage_metadata`·`mini_prices`·`estimate_cost`). 바탕은 02절 `rag-judge-v1.0.0` 요청 글(파일 본문에 든 글).
- 결과(새 커널 A·B 모두 같음): 실행 1 `Q090` `{'Q090': 0}` → `{'Q090': 1}`, 깨진 사례 `[]`, 통과 `True` · 실행 2 `Q002` `{'Q002': 1}` → `{'Q002': 0}`, 깨진 사례 `['Q002']`, 통과 `False` · `보낸 요청 수: 4` · `보내지 않은 요청: ['old-Q006', 'new-Q006']` · 합친 점수로 다시 걸면 통과 `False`.
- **두 사례는 07절 결과를 보고 고른 예**입니다(본문 b4·b7, 마감에서 노트북에도 한 문장, B-15). 파일의 본문 설정 칸은 보내지 않고 같은 설정의 모델 객체로 판정 요청 글만 보냈습니다(마감에서 「파일에 든 판정 요청 글이 판정되는지」로 표현을 좁힘, B-14). 일괄 처리 제출 0번, 파일 쓰기 0번.
- 판정 부분은 07절 요청 여섯 가운데 넷과 같은 글·같은 점수입니다. 파일 읽기·요청마다 비용·일부만 보낸 결과로는 이후 판을 정할 수 없다는 흐름이 더해져 받아들였습니다(B-16, 강사 확인 §11).

## 8. 도구 파일 `notebooks/rag_tools.py` — 함수 표와 해시 변천

| 함수(인자) | 배운 곳 | 가져오는 절 |
|---|---|---|
| `unique_doc_ids(hit_list)` · `find_gold_rank(doc_ids, gold_doc_ids)` | Ch 11 01절 | 01 |
| `rank_weight(rank)` | Ch 11 04절 | 01 |
| `error_name(gold_rank, cutoff)` | Ch 11 05절 | 01 |
| `build_judge_prompt(judge_head, pair, case)` | Ch 15 02절 | 03·05·06·07·08 |
| `judge_once(judge_model, prompt_text)`(판정 딕셔너리만, 사용량 없음) | Ch 15 02절 | 03 |
| `score_cases(judge_model, judge_head, pair, case_list)`(사례 한 건에 요청 1번) | Ch 15 03절 | 04·07 |
| `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`(본문에 `.get` 둘) | Ch 6 06절 | 06·09 |
| `scores_of(verdicts)` | Ch 15 04절 | 07 |
| `average(values)`(여섯째 자리 반올림) | Ch 15 06절 | 07 |
| `check_by_average(old_scores, new_scores)` · `broken_cases(…)` · `check_by_case(…)` | Ch 15 07절 | 09 |
| `read_jsonl(file_path)` · `ids_not_in(first_ids, second_ids)` | Ch 15 08절 | 09 |

- 함수 **열다섯**, `import json`·`import math`만, 함수마다 `# Ch N NN절에서 배웠습니다 — …` 주석, 전역 이름 기대기 0, 금지 문법 0(`estimate_cost`의 `.get`은 Ch 6 원본 그대로). 02절만 가져오지 않습니다(가져오는 절마다 노트북·`_src`에 고정 세 문장 한 번).
- **해시 변천**: 01 새로 만듦 `c6605eea315adb8d…`(Ch 11 넷) → 03 `163f8b027fc4d2c4…`(02절 둘 + `import json`) → 04 `3bd16966f98d6c87…`(03절 `score_cases`) → 05 그대로 → 06 `c6eb7639c90fc061…`(Ch 6 06 `estimate_cost`) → 07 `123a0b62c004913d…`(04 `scores_of`·06 `average`) → 09 **`6c59d0f239370dbc208a7ca2be71fbe2147574e2ea13d5d044ce0ced5afdbea1`**(07 셋·08 둘). 바꿀 때마다 앞 절 노트북 사본을 새 커널로 실행해 셀별 출력이 같은 것을 확인했습니다(각 진단 §5·§6). **마감에서는 바꾸지 않았습니다.**
- 노트북에만 있는 함수(뒤에서 다시 쓰면 같은 본문으로 옮김): 01 여섯, 02 `judge_case`, 03 `build_pair_prompt`·`picked_name`·`always_first`, 04 `box_name`·`count_boxes`·`agreement_rate`·`always_one`, 05 셋, 06 `make_request_rows`·`cost_by_conversation`·`nearest_rank`, 08 여섯(`make_prompts`·`make_batch_line`·`make_batch_lines`·`write_jsonl`·`line_problems`·`duplicate_ids`), 09 다섯.

## 9. 산출 파일 계약 — `runs/batch-eval-input.jsonl`

- **이 챕터가 쓰는 산출 파일은 이것 하나이고 08절이 씁니다.** 01~07·09절은 파일을 쓰지 않습니다(09는 읽기만).
- 해시: 개선 전 `4f898d7d14b6094ae4bc32f3e277ccf99744749c20357c8daab470bffb8f3bd5`(3줄·941바이트, 2026-09-10) → **`0177cebc207151657385a7a11ec2147b0bc45edc2b35f09c7f6fb2b7f8988e3e`**(6줄·51145바이트). 내용이 결정적이라 08을 다시 실행해도 같습니다(묶음에서 푼 폴더 실행도 같은 해시).
- 칸 구성: 줄마다 `custom_id`·`method`·`url`·`body`(이 차례). `custom_id` `old-Q002`·`old-Q006`·`old-Q090`·`new-Q002`·`new-Q006`·`new-Q090`, `method` `POST`, `url` `/v1/chat/completions`, `body` `model` `gpt-5.4-mini`·`temperature` `0`·`reasoning_effort` `none`·`messages`(사용자 메시지 하나 = 판정 요청 글 3161·3183·5093·3160·3183·5117자), `ensure_ascii=False`, 줄 끝 `\n`.
- **읽는 쪽**: 09 노트북 셀 [15]·[17]·[21]·[25](`custom_id`를 `split("-")`로 나눈 판 표시·질문 번호, `url`, `body.model`·`body.temperature`·`body.reasoning_effort`, `body.messages[0]["content"]`) · `textbook/part4/qa/check_bundle_execution.py` 31행(08 노트북을 묶음에서 키 없이 실행) · 이름만: 묶음 허용 목록 두 곳 · Part 7 선행 목록 두 곳(`part7-practice.zip`에 들어감) · Ch 34 02 b3. **칸 이름·`custom_id` 모양을 바꾸면 09가 깨집니다.** `upgrade-contracts.md` §3 Part 4 표에 같은 줄을 넣었습니다(B-12).
- 보호 파일 36개(`qa/upgrade/before-manifest.json`, 수정 전 기록이라 고치지 않음): 마감 대조 결과 **35개는 원래 값 그대로**, 이 파일 하나만 08절 값 `0177cebc…`입니다.

## 10. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `textbook/part4/public-files.json` | 01·09절 | 도구 파일 `notebooks/rag_tools.py` 줄(01) · 09 노트북 줄(09) |
| `labs/part4/ch15-evaluation-advanced/notebooks/rag_tools.py`·`runs/batch-eval-input.jsonl` | 01~09절 | 실습 폴더(챕터 몫) — §8·§9 |
| `labs/part4/ch15-evaluation-advanced/README.md` | 09절 + **마감** | 09절 단락(09) → 마감에서 전체를 다시 씀: 노트북 **아홉**, 도구 파일 소개(고정 세 문장 뜻 + 함수 열다섯·배운 곳), 자료 파일 설명(기준 답은 교재 작성자 한 사람), Ch 12 기록 두 개, 모델 `gpt-5.4-mini`·요청 46번(절별)·예상 비용 상한 0.2달러 아래(≠ 청구 금액)·01·08은 키 없이, 입력 파일 설명, `[[미정: judge 모델]]`·「Groundedness judge」·「상대 경로」 없앰 |
| `textbook/part4/_build_index.py` | **마감** | ch15 설명 한 줄 「실제 실패 기록에서 평가 항목을 정하고, 답변 평가·추적·비용 분포·회귀 검사를 연결합니다.」 → 「실패 로그에서 평가 사례를 고르고, 평가 모델 판정과 제시 라벨 일치율, 실행 추적과 대화당 비용, 회귀 스위트와 일괄 처리 입력 파일을 다룹니다.」(ch16 줄은 그대로) |
| `textbook/part4/index.html` · `textbook/downloads/part4-practice.zip` · `textbook/part4/qa/integration-results.json` | 09절 + **마감** | `python3 textbook/part4/_build_index.py` → **`Part 4: 33 verified sections; 97 bundled files`**, 마지막 zip `f8f28c17f3b11724…`(zip 100항목·manifest 97, Stale 0) |
| `textbook/downloads/part7-practice.zip` · `textbook/part7/qa/integration-results.json` | **마감** | `python3 textbook/part7/_build_index.py` 한 번 → `Part 7: 29 verified sections; 108 bundled files`. 바뀐 항목은 입력 파일(941 → 51145바이트)과 zip 안 `manifest.json`의 그 해시 한 줄뿐, `integration-results.json`은 `bundle_sha256` 한 칸만(`820e382c…` → `1e805674…`), **`textbook/part7/index.html`과 나머지 `qa/*.json` 해시 그대로** |
| `textbook/part4/qa/bundle-execution.json` | **마감** | `check_bundle_execution.py`가 다시 씀(ch13 05·ch15 08 PASS, ch16 테스트 7 passed, 마지막 zip `f8f28c17…` 기준) |
| `textbook/_notebook/checks/ch15-evaluation-advanced/visual-results.json`·스크린숏 넷 | **마감** | 18행 → **20행**(열 HTML), 모두 PASS |
| `textbook/_notebook/checks/notebook-contracts-part4-ch15-evaluation-advanced.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀(공용 검사 산출 파일) |
| `textbook/qa/upgrade-contracts.md` | **마감** | §3 끝(Ch14 줄 아래)에 「Ch15 산출 파일」 한 줄과 Part 4 표(입력 파일 한 행, 09절 읽는 쪽 포함). 다른 행은 그대로 |
| `textbook/_notebook/upgrade/PLAYBOOK.md` | **마감** | §3에 「3~5번 기준은 챕터 끝 실습 절 규칙」, §4에 「흔들린 값 인용 범위(비교·결론 금지)」·「입력을 고치기 전에 먼저 흔들림 확인」 — 규격 §2-7 9·10번 끝·§7-2 새 줄과 같은 뜻 |
| `textbook/qa/upgrade-progress.md` · `textbook/qa/upgrade-final-checklist.md` | **마감** | Ch 15 행 한 줄 · §2-4 Ch 15 항목과 §3·§4 Ch 15 줄 |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`(오늘 챕터 리드(오케스트레이터)가 세 줄을 이미 더함), 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs` — 화면 검사는 `/tmp` playwright를 쓰는 사본 `.cache/ch15close/vis15.cjs`로 돌림), `labs/part4/ch15-evaluation-advanced/pyproject.toml`·`uv.lock`(§14), `labs/part4/continuity-guide.md`(틀린 문장 없음), **Ch 16 이후 파일 전부**(Part 7 묶음 재생성만 예외), 검사 스크립트(환경 변수로만 돌림).
- **파일을 지운 것은 없습니다.** 옛 생성기 둘만 `mv -n`으로 옮겼습니다(§14 1번). `check_bundle_execution.py`가 스스로 만든 임시 폴더는 스크립트가 끝에서 지웠습니다(스크립트 동작).

## 11. 기준 버전·확인 날짜

- 실습 폴더 `pyproject.toml`·`uv.lock`: `langchain 1.4.0` · `langchain-openai 1.6.1` · `langsmith 0.7.14`(노트북 import 0 — §14) · `python-dotenv 1.2.3`, dev `ipykernel 7.3.0`·`pip 26.2`. 노트북 `%pip`은 세 패키지(`langchain`·`langchain-openai`·`python-dotenv`)이고 01·08절은 설치 셀이 없습니다.
- **교재 출력 환경**: Linux · Python **3.12.13** · `langchain-core 1.6.3` · `openai 3.16.2`(작업 가상환경 `.cache/vm/venv-ch15-evaluation-advanced`) ↔ **학생 잠금 `langchain-core 1.6.2` · `openai 3.11.0`**. 잠금 판에서 `reply.text`·stream 사용량 합치기는 확인하지 않았습니다(검토 A 「확인하지 못한 것」).
- 요금: `gpt-5.4-mini` 100만 토큰당 입력 0.75 · 캐시 입력 0.075 · 출력 4.50달러(Ch 6 06 요금표 2026-09-17, 검토 B가 2026-09-21 모델 페이지와 같음을 확인).
- 참고 자료(모두 **2026-09-21 확인**): LangSmith `https://docs.langchain.com/langsmith/evaluation-concepts` · `…/evaluation-types` · `…/evaluate-rag-tutorial` · `…/improve-judge-evaluator-feedback` · `…/observability-concepts` · MT-Bench `https://arxiv.org/abs/2306.05685` · Percentile `https://en.wikipedia.org/wiki/Percentile` · OpenAI `https://developers.openai.com/api/docs/guides/batch` · `…/models/gpt-5.4-mini` · `…/guides/reasoning`.

## 12. 강사 확인 대상

1. **`chapter.json` 학습 목표(네 줄 → 여섯 줄)**. 「사람 라벨 일치율」(04절은 제시 라벨이 사람 라벨이 아니라고 가르침)·「캐시 사용량」(「캐시」 단독)을 실제 내용으로 고치고 05·06절 몫을 두 줄로 나눴으며 09절 몫 한 줄을 더했습니다(새 전문은 `chapter.json`). **`hours`는 그대로**(총 16h · 강의 8h · 실습 8h = 01~08절 meta 합).
2. **03절 제목의 「프롬프트」**(과정 금지어). 바꾸면 파일 이름·`chapter.json`·묶음 목록·Part 목차·과정 검사가 함께 바뀌어 이번에도 두었습니다.
3. **Q090 기준**: 모른다고 답한 답을 1로 셀지(04 제시 라벨 1 = `v1.1.0` 취지) 0으로 셀지 정하지 않았습니다(02·03·04 진단 강사 확인과 이어짐).
4. **03·04 재현성(결정 A)**과 **대비를 잃은 두 실험**(03 쌍 비교가 뒤집히지 않음 — 치우침은 규칙 함수로만 보임, 04 판 바꾸기 표가 두 판을 가르지 못함). 설계를 바꾸려면 노트북을 다시 실행해야 합니다.
5. **학생이 확인할 수 없는 자료 파일 판정 조건**(질문·근거·응답 세 칸, 추론 설정 없음): 사실은 두고 「교재 제작 기록(`prepare_runs.py`)에 따르면」으로 출처를 밝혔습니다(A-5). 그 파일은 학생 묶음에서 빠집니다.
6. **05·06절 시간·비용 인용 범위**: 리드 결정대로 05 b6 초 값은 「교재 출력에서」 한정으로 두고 비교를 뺐고, 06 b6은 값 없이 두 경우만. 06 노트북 결과 읽기 둘째 단락의 「세 배 넘게」는 리드 결정으로 남겼습니다(규격 §2-7 9번 끝의 「비교 금지」와 나란히 두고 한 번 봐 주세요).
7. **06절 정한 목록 설계**(대화 백 개, 요청 한 번 0.001달러)·**07절 이후 판 답 둘은 이 절에서 만든 답**·**07 Before 결함을 빨강으로**·**08 요청 주소 `/v1/chat/completions`**(Ch 34 02는 Responses — 수업에서 차이를 짚기)·**일괄 처리 실제 제출 0번**.
8. **09절**: 두 사례를 07절 결과를 보고 고른 예(B-15), 판정 부분이 07의 부분 집합(B-16 — 받아들임), 파일의 요청을 일괄 처리가 아니라 하나씩 보냄.
9. **준비물 실행 시간 문장**: 01~07절을 셀 실행 기록으로 읽은 「교재 출력을 만든 실행에서는 약 N초」로 맞췄습니다(커널 기동 제외, 학생 첫 설치는 더 걸림).
10. 교재 출력 환경 ↔ 학생 잠금의 판 차이(`langchain-core`·`openai`, §11), 자료 파일 머리 칸이 지금 Ch 12와 다름(01 강사 확인 1), 삽화 아홉 장의 「그림만 보고 관계가 읽히는가」 판정(05-5 모래시계가 작음, 06-5 바구니 넷), **한국어 감사 3단**은 별도 세션 몫.

## 13. 뒤 챕터 인계 — Ch 16 가드레일·안정화가 이어받을 것

1. **Ch 16 실습 폴더에는 `rag_tools.py`가 없습니다**(Ch 16은 `guardrails.py` 모듈과 `tests/` — `check_bundle_execution.py`가 테스트 7개를 돌림). Ch 15 도구 파일 함수를 쓰려면 Ch 16 규격에 맞게 따로 정하세요.
2. **말**: 「평가 모델(judge)」·「판정 머리글」·「판정 요청 글」·「예상 비용」(≠ 청구 금액)·「캐시 입력」·「실행 추적」·「첫 토큰 도착 시간」·「회귀 스위트」·「통과 조건」·「일괄 처리」를 그 뜻 그대로 이어 쓰세요. 「캐시」 단독·「프롬프트」는 쓰지 않습니다.
3. **09 b8 연결**: 「Ch 16 가드레일·안정화」로 넘기며 **상한을 두어 막는 일은 하지 않았다**는 것까지만 적었습니다(Ch 16 내용을 앞당겨 가르치지 않음). Ch 16 `chapter.json`의 04절 「호출 한도와 비용 상한」 내용은 이번에 확인하지 않았습니다.
4. **산출 파일**: `runs/batch-eval-input.jsonl`(§9) — Ch 16은 읽지 않습니다. 칸 이름·모양을 바꾸지 마세요(09절이 읽음).
5. **Part 4 묶음**: `part4-practice.zip`은 마감 판(`f8f28c17…`)이고 `check_delivery.py`에서 Part 4 쪽은 끝까지 통과합니다. Ch 16을 고치면 다시 만들어야 합니다.

## 14. 아직 가르치지 않은 것 (Ch 16이 설명 없이 전제하면 안 되는 것)

- **일괄 처리(Batch API) 실제 제출**: 아홉 절 모두 0번. 파일 올리기·일괄 작업·상태·결과 파일·오류 파일·할인 청구는 안내에 적힌 차례로만 설명했습니다. 일괄 판정이 동기 판정과 같은지 모릅니다. Responses 주소 `/v1/responses`의 본문(`input`·`reasoning.effort`)은 쓰지 않았습니다.
- **비용·호출 수 상한으로 요청을 막기**: 09절은 요청 한 번의 예상 비용을 **세기만** 했고, 07절 통과 조건에도 비용·지연 상한이 없습니다. 예상 비용 값(캐시 입력·출력 토큰에 따라 흔들림)을 인용하지 마세요.
- **캐시 입력이 늘 생긴다**: 06절 실행 A와 09 확인 실행 첫 요청은 0이었습니다.
- **판정이 늘 같다**: v1.1.0 Q090은 실행에 따라 갈렸습니다. 이 챕터의 점수는 **정답률도 사람 판단과의 일치율도 아닙니다**(사례 세 건, 제시 라벨은 교재 작성자 한 사람).
- **걸린 시간 분포**: 05절이 요청 한 번씩 잰 것뿐, 백분위수로 모은 적 없음. **LangSmith 화면·업로드·데이터셋**: 한 번도 실행하지 않았습니다. 여러 사람이 매긴 라벨·부분 점수·구조화 출력 판정도 없습니다.
- **문법**: §1의 「쓰지 않은 Python 이름」 목록이 그대로 걸립니다. 파일 쓰기는 08절 JSONL 한 번뿐입니다.

## 15. 남은 것 (전체 마감 몫)

1. **옛 생성기 둘은 옮겼습니다(삭제 아님, 2026-09-21 완료)**: 01절이 `raise SystemExit`로 막은 `_author.py`·`figures/_gen_figures.py` → `qa/upgrade/before/generators/blocked/`(원본 사본은 이미 `before/generators/`에 있음, 해시 `52d38e6a…`·`bec0e17b…` 옮기기 전후 같음). `_build.py`·`run_section.sh`·게이트·`verify.py`·`_build_index.py`·`check_delivery.py`·`check_bundle_execution.py` 어디도 부르지 않음을 `grep`으로 확인했고(`textbook/part7/qa/check_figures.py`의 `_gen_figures.py` 확인은 Part 7 챕터만 봄), 옮긴 뒤 `_build.py`를 다시 돌려 HTML 열 개 해시가 같았습니다. `labs/…/prepare_runs.py`는 자료 스크립트라 옮기지 않았습니다(**돌리면 자료 파일이 새로 생겨 02~09절이 흔들림**). `depth-notes.json`은 옛 `_author.py`만 읽던 파일입니다.
2. **옛 도식 스물네 개 삭제 승인**: `figures/0N-평가-흐름.{svg,excalidraw,caption.md}`(01~08절 각 셋, 본문 참조 0, 사본 `qa/upgrade/before/figures/`).
3. **`qa/upgrade/gates-wip-01~09.json`**은 `gates-after.json`으로 갈음됩니다(삭제 승인 대상).
4. **`nearest_rank`의 `/ 100`**(06 노트북 셀 [49], 규격 §2-3 식 안의 숫자): 고치면 모델 절이라 재실행이 필요해 두었습니다. **다음 재실행 때 `percent_unit = 100`**(B-6).
5. **`pyproject.toml`의 `langsmith==0.7.14`**: 아홉 노트북 import 0건(LangSmith 화면·업로드를 하지 않음, `langchain`의 의존성으로는 잠금에 남음). 빼면 `uv lock` → 묶음 재생성이 따라와 **빼지 않았습니다**.
6. **03절 제목의 「프롬프트」**(§12 2번).
7. **도구 파일 가져오기와 작업 폴더**(과정 공통): 자리 찾기 셀은 「notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요」라고 안내하지만 `from rag_tools import …`는 작업 폴더가 `notebooks/`여야 동작합니다(Ch 14도 같은 모양). 규격 §2-7 5번과 함께 과정 전체에서 정할 일입니다.
8. **`llm-practice.zip` 재생성**: 2026-09-14 판이라 낡은 항목 **149개**. `textbook/part4/qa/check_delivery.py`는 `part4-practice.zip`을 끝까지 통과한 뒤 **111행 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`**에서 멈춥니다(작업 전과 같은 자리).
9. **Part 7 `check_delivery.py`**: `part7-practice.zip`의 Ch 15 입력 파일 항목은 해소(108항목 Stale 0)했지만, 그 대조에 닿기 전 **72~75행 `existing-artifacts-before.json`(376개 가운데 375개 해시가 바뀌고 `textbook/part2/ch07-prompt-engineering/_src/index-body.html` 하나는 없음)에서 `FileNotFoundError`로 멈춥니다** — 과정 전체 품질 개선이 Part 7 기록 이전 파일을 바꾼 결과라 전체 마감 몫입니다. 그 뒤의 `llm-practice.zip` 대조도 Stale입니다.
10. **삭제 승인 대상(캐시·임시 폴더)**: `.cache/vm/bundle-check/`(uv 캐시 약 7.7~7.9GB + 하드링크 가상환경 `prewarm-ch13` — 이번 마감에서 만듦, 디스크 공유라 실제 합계 약 7.9GB · `linktest` 작은 파일 둘 · 로그) · `.cache/vm/venv-ch15-evaluation-advanced`(170MB) · `.cache/ch15-01~09` · `.cache/ch15close`(마감 전후 사본·해시 기록·그림 확인 사본, 13MB) · `/tmp/ch15-01~09`·`/tmp/ch15-fix`·`/tmp/reviewA15`·`/tmp/reviewB15` · 챕터·실습 폴더 `__pycache__` 다섯(`textbook/part4/ch15-evaluation-advanced/`·`figures/`·`qa/upgrade/`, `labs/…/`·`notebooks/`).
11. **2차 검토**: 검토 보고서 둘의 「확인하지 못한 것」(삽화 판독, 학생 잠금 판에서의 동작, Chat Completions 본문이 일괄 처리에서 받아들여지는지)과 §12.

## 16. 검토 1차와 반영 (2026-09-21 마감)

- 판정: **A(01~05절) 상 0 · 중 4 · 하 12**(01·02 accept, 03·04·05 accept with fixes), **B(06~09절) 상 2 · 중 1 · 하 16**(06·09 accept with fixes). reject 0건, **재실행이 필요한 건 0건**.
- **[상] 2건 모두 반영**: B-1(06-3 「왼쪽 네 막대에 대화 85개」 → **95개**) · B-13(09 「두 실행」 두 뜻 → 새 커널 쪽 세 자리를 「새 커널로 두 번 실행했을 때」로, 복습 4번 질문·해설을 A·B 출력과 맞춤).
- **[중] 5건 모두 반영**: A-6(03 노트북 흔들림 안내) · A-7(03→04 「사람 판단」 예고 → 제시 라벨) · A-10(04-3·04-4·03-3 라벨·캡션·도식 읽기 한정 + 04 b6 셈 문장 + 진단·설계표 바로잡기) · A-14(05 b3 「Ch 6 06절에서 처음 쟀다」 → Ch 2 12·Ch 6 05) · B-2(06 b6 흔들린 값·비교 빼기).
- **[하] 28건 가운데 26건을 고쳐 반영**, B-16은 권하는 고침이 없는 설계 판단이라 **받아들이고 강사 확인에 올림**, **반영하지 않은 1건은 B-6**(`nearest_rank`의 `/ 100` — 코드를 고치면 모델 절이라 재실행이 필요, §15 4번). 고친 것: A-1·A-2·A-3·A-4·A-5·A-8·A-9·A-11·A-12·A-13·A-15·A-16 · B-3·B-4·B-5·B-7·B-8·B-9·B-10·B-11·B-12·B-14·B-15·B-17(README)·B-18(`chapter.json`)·B-19(Part 7 묶음).
- 검토가 적지 않았지만 같은 규칙이라 함께 고친 자리: **02~05절 준비물 실행 시간**(B-7을 01~07절 모두에), **05-1의 「사용량」 점선 → 실선**(B-5 리드 규칙), 02·03·04·07 진단의 요청 수 항목(규격 §7-2 새 줄), `05-figures.md`·`06-figures.md`·`03-figures.md`·`04-figures.md` 설계 기록.
- **노트북을 다시 실행하지 않았습니다.** 아홉 노트북 모두 `code_sha256`·`outputs_sha256`이 작업 전과 같고 `metadata.verification` 기록과도 일치합니다(9/9). 고친 방법은 `mdpatch.py`(생성기 + 노트북 설명 셀 + `_src` 동시) → `run_section.sh … --no-exec` · `.mmd` 여섯 장 `--force` 다시 렌더(03-3·04-3·04-4·05-1·05-3·06-1, 폭 667·635·557·514·641·468, **여섯 장 모두 PNG를 직접 열어 도식 읽기와 맞는 것을 확인**) · `attach_figures.py`(05·06 「오늘 볼 그림」) · `_build.py`뿐입니다. 마감 뒤 생성기 `author_01~09.py`의 `SRC_HTML`·`cells()`가 `_src`·노트북 설명 셀·코드와 글자까지 같은 것을 대조했습니다(9/9).
