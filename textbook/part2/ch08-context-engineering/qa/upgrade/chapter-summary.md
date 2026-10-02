# Ch 08 컨텍스트 엔지니어링 — 챕터 요약 (다음 챕터 작업자용)

작성 2026-09-17(품질 개선 6절 + 실습 절 07 + 별도 세션 검토 1차 A·B 반영 뒤). **Part 2 마지막 챕터**입니다. 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md` §6. 앞 내용: `textbook/qa/upgrade-course-summary.md`(Part 1), 같은 Part 앞 챕터 `part2/ch06-langchain-start/qa/upgrade/chapter-summary.md`·`part2/ch07-prompt-engineering/qa/upgrade/chapter-summary.md`. 절 사이 인계 원문: `qa/upgrade/handoff.md`(절마다 「새로 가르친 것」「이어 쓸 이름과 값」「출력 라벨」「아직 안 가르친 것」 전체 목록). 검토: `qa/upgrade/review-round1-A.md`(§01~04)·`review-round1-B.md`(§05~07), 각 끝에 「반영 결과」.

**Ch 09 작업자는 과정 요약(Part 1) + Ch 06·07 요약 + 이 파일만 읽고 시작할 수 있게 썼습니다.** 세부 값·라벨이 필요하면 handoff를 찾아봅니다.

절: 01 컨텍스트와 토큰 예산 · 02 Write와 Select · 03 Compress와 Isolate · 04 네 가지 실패 모드 · 05 컨텍스트 로트(Context rot) 측정(파일 이름·slug는 `05-Context-rot-측정`) · 06 단계적 공개와 설계 비교 · 07 컨텍스트 엔지니어링 실습: 도서관 안내 질문 세 개에 예산표와 지킬 말 검사 붙이기. 형식 01·02·03·04·06 paired, 05·07 experiment. 모델은 모든 절 OpenAI `gpt-5.4-mini` 하나. 코드 셀 183개(22·23·26·29·27·31·25), 게이트 7/7(G1~G7 0, 수정 전 274건), 검사 문장 409·408·412·452·465·513·465, Mermaid 27장(4×6 + 3)·삽화 7장(대기 없음), 모든 노트북 새 커널 실행 PASS(실행일 모두 2026-09-17, 07만 검토 반영으로 13:54 재실행). 노트북 모델 호출 01 3 · 02 2 · 03 3 · 04 5 · 05 4 · 06 5 · 07 5번(05만 가장 긴 입력 3만 토큰, 비용 어림 0.03달러 안팎, 나머지 0.01달러 미만).

## 0. §2-7 리팩터 (2026-09-21) — 아래 표보다 먼저 읽을 것

- 앞 절·Ch 7 08에서 배운 함수 9개를 `labs/part2/ch08-context-engineering/notebooks/llm_tools.py`(코드 57줄)로 모으고, 02~07 준비 셀에서 `from llm_tools import …` 한 줄로 가져옴: `input_budget`·`count_tokens`(01), `find_cited_notes`(02), `find_missing_words`(03), `build_notes_messages`·`check_answer`(04), `count_marks`(05), `open_document`(06), `estimate_openai_cost`(Ch 7 08). NumPy 없음(벡터 계산 없음).
- **도구 파일 판은 바깥 이름 대신 인자로 받음**: `count_tokens(encoding, text)`, `build_notes_messages(persona_text, task_text, notes, question)`, `check_answer(answer_text, notes, keep_words)`. 노트북은 `encoding = tiktoken.encoding_for_model("gpt-5.4-mini")` 셀(출력 `토큰화 규칙 이름: o200k_base`)을 두고 넘김. 처음 가르친 절(01·02·03·04·05·06)의 노트북 판은 옛 모양 그대로.
- 코드 셀 183 → **161**(22·22·24·26·21·27·19), 코드 줄 1335 → **1186**(−149, −11.2%, 도구 파일 포함 1243). 노트북 절 번호는 그대로.
- 02~07 새 커널 두 번 다시 실행(2026-09-21, 교재 출력 = 두 번째). 결론에 닿은 변화: 02 Before 답이 「10권·`[E01 p.2]`」 → 「파일 내용이 없어 확인할 수 없음, 출처 표시 없음」, 04 Before 출처 표시 `[E01 p.2]` → `[상담 메모]`, 05 「세 답 글자까지 같음」 → 「첫머리 주어만 다름」, 06 세 설계 비용이 입력 순서(0.000609·0.000448·0.000372), 07 실행 1 휴관 답의 빠진 지킬 말 없음(합계 0.001204). 핵심 관찰은 모두 유지돼 §2-7 10항으로 입력을 고친 절은 없음. 아래 §1~§3·§9의 2026-09-17 값 가운데 이 줄과 다른 것은 옛 값이고, 세부는 `handoff.md` 「§2-7 리팩터」.
- runs: `context-design-continuity.json` `125fc147…58ad` → **`043750ee…a5d2`**(run_id `ch08-context-20260921T050226`, 출처 Ch 7 `434640f4…a561`), 사본 `continuity/20260921T050226/` 하나. Ch 6 → 7 → 8 사슬 이어짐, Ch 8 `tests/` **21 passed**(`load_function()`이 노트북의 `from llm_tools import`를 보고 도구 파일에서 정의를 읽도록 고침).

## 1. 새로 가르친 개념·기법·함수·용어 (노트북에서 실행한 것만)

| 절 | 새 API·값 | 직접 만든 함수(노트북 셀, 실습 폴더 모듈 아님) | 용어 표 |
|---|---|---|---|
| 01 | `import tiktoken`, `tiktoken.encoding_for_model("gpt-5.4-mini")` → 규칙 `o200k_base`, `encoding.encode(글)`, `init_chat_model(…, max_tokens=계산한 값)`, `usage_metadata["input_tokens"]`·`["output_tokens"]`, `response_metadata["finish_reason"]`(`stop`·`length`) | `input_budget(total_budget, output_reserve, safety_margin)`(뺄셈만), `count_tokens(text)`(바깥 `encoding`) | 컨텍스트(목록에 실린 글만), 컨텍스트 윈도(`gpt-5.4-mini` 400,000·최대 출력 128,000), 토큰 예산(노트북 「수업 예산」), **출력 예약분**(= Ch 5 출력 몫 = Ch 6 출력 상한), **여유분**(추정이 실제보다 적게 나오는 몫을 받는 여분 자리), **입력 가용분**(= 예산 − 예약분 − 여유분), 추정 토큰 수 |
| 02 | `json.dumps(…, ensure_ascii=False, indent=2)`·`json.loads(file.read())`, `tempfile.mkdtemp`·`os.chdir`·`os.listdir`(Ch 2 05 모양) | `find_cited_notes(answer_text, notes)`(출처 표시가 답에 있는 기록만) | 적어 두기(Write), 골라 넣기(Select), **기록**(사실 한 문장 + 설명 값 딕셔너리 — Ch 6·7 요청 기록과 다른 뜻), 기록 파일(`library-notes.json`), 메타데이터(책등 분류 번호), 선택 조건, 출처 표시(`[E01 p.3]`) |
| 03 | 없음 | `find_missing_words(text, words)`, `build_messages(note, question)` | 줄이기(Compress), 원문, **지킬 말**(사람이 원문에서 고른 꼭 남길 말 목록), **줄인 기록**, 나누기(Isolate), 업무별 메시지 목록. 「요약」은 모델 요약(Ch 16 03·Ch 22 03)에만 |
| 04 | 없음 | `build_notes_messages(notes, question)`(기록마다 `"[" + 출처 + "] " + 내용 + "\n"` + 빈 줄 + `"질문: "`), `check_answer(answer_text, notes)` → `{"답의 출처 표시와 같은 기록", "답에서 빠진 지킬 말"}`(바깥 `closure_keep_words`) | 실패 모드, **컨텍스트 오염**(환각이나 다른 오류가 들어가 뒤에서 되풀이해 쓰임 — 요청 한 번만 실행), **산만**(아주 긴 컨텍스트에 치우쳐 학습한 것을 덜 씀 — 실행 안 함), **혼란**(필요 없는 내용을 답에 써서 답이 나빠짐), **충돌**(새로 쌓인 정보가 다른 정보와 맞지 않음), 기준 목록. 출처 Breunig 원글·LangChain 글. **산만 ≠ 컨텍스트 로트**(길이별 저하 자체는 로트) |
| 05 | `usage_metadata["input_token_details"]["cache_read"]`(인덱스로 꺼냄 — §12), `estimate_openai_cost`(Ch 7 08 같은 코드) | `build_long_notes(filler_count, before_count)`(Ch 5 05 `make_document` 모양), `count_marks(answer_text, mark)`(`split` 뒤 `len − 1`), `make_length_record(filler_count, run_response)` | 컨텍스트 로트(Ch 5 05 뜻, 입력 길이 기준), 무관한 기록, 근거 앞 기록 수, 같게 둔 조건, 측정 입력(예산을 일부러 넘김), 출처 표시 수. 본문 말 「요청 전 비용 상한」(캐시 없음·출력 예약분 전부 가정, **여유분을 더하지 않은 어림** — 실제 입력은 추정보다 14 많음, 정확한 상한은 여유분 40을 더해 계산), **요청 기록**(요청 한 번의 측정 딕셔너리, Ch 6·7 뜻) |
| 06 | `hashlib.sha256(바이트).hexdigest()`·모드 `"rb"`·`os.makedirs`·`os.path.exists`·`time.strftime`(모두 Ch 7 08 뜻 그대로) | `open_document(document_list, source)`(없으면 `None`), `make_design_record(design_name, run_response)`(바깥 `condition_words`), `estimate_openai_cost(usage, input_rate=0.75, cached_input_rate=0.075, output_rate=4.50)` | 단계적 공개, 목록 줄, 입력 설계, 전체 입력(full)·고른 입력(selected)·줄인 입력(compressed). Ch 7 「파일 지문」「기록 사슬」「기록 파일」(요청 기록을 담은 파일 — 02 기록 파일과 다른 파일이라고 b3에 적음) |
| 07 | 새 API 0개 | 같은 코드 7개(`input_budget`·`count_tokens`·`find_missing_words`·`count_marks`·`estimate_openai_cost`·`open_document`·`build_notes_messages`) + 새 4개 `add_answer_items(record, run_response, evidence, words)`·`print_records(records)`·`choose_evidence(plan, available)`(튜플 반환)·조립 함수 `ask_library(plan, available)`(본문 10줄) | 새 용어 0개 |

- **Python 쪽(기본 경로 183셀)**: f-string·`raise`·try·내포식·조건 표현식·`lambda`·`Path`·`next`·`datetime`·`join`·`splitlines`·`count()`·`+=`·`sum`·`max`·`zip`·`isinstance`·`@`·`BaseModel`·타입힌트·`**` 풀기·반복문 안 요청과 요청을 기다리는 `print` **0건**(검토 A·B AST). 새로 풀어 쓴 모양: 비교식을 `print` 인자로, 딕셔너리 목록 리터럴(한 기록 한 줄), 두 조건 변수 + `if … and …:`, 함수가 바깥 이름을 읽음(`encoding`·`persona_text`·`model`·`shared_tokens`), 함수 안 반복문의 `return`·끝의 `return None`, `for … in [리터럴]:` + `break`(06 경로), `range(수)`로 `append`(05), `split(표시)` 뒤 `len − 1`, 딕셔너리 `copy()`·`record[키] = 값`, 목록·메시지 목록 `==` + `assert`, 튜플 반환·풀어 담기(07, Ch 7 07 모양), `get(키, "-")`(07), `range(len(목록))`(07, Ch 7 08), `if missing_words == [] and estimate <= available:`(07)
- **결론 태도(Ch 9도 지킬 것)**: 한 번 본 결과는 「이번 실행에서는」, 원인 보류(설계가 정한 결과는 제외 — 07 「이 조립 함수에서는」), 검사 함수는 말·표시가 있는지만(품질 점수 아님, 뜻은 원문 대조), 두 조건 답에 모두 있던 값은 한 조건 효과로 적지 않음, 출력 토큰·비용은 요청마다 달라 순위로 쓰지 않음(06 같은 목록 출력 104 vs 64), 탐색 뒤 정한 값은 b7에 과정과 「흐름을 보여 주려고 정한 예」

## 2. 반복해 쓴 메시지 목록·함수·데이터·비유·이름

- **모델 셀**: 01 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`, 02~07 `…, max_tokens=output_reserve`(120). 결과 읽기 「이 노트북의 출력은 2026-09-17에 이 모델로 실행한 결과입니다」 + temperature 0 ≠ `do_sample=False`
- **메시지 목록(01~07 같은 모양)**: `[("system", persona_text), ("developer", task_text), ("user", user_text)]`. `persona_text = "당신은 미르시립도서관 안내 담당자입니다."`, `task_text = "주어진 근거에 있는 정보만 쓰세요. 두 문장 이내로 답하고, 문장마다 끝에 출처를 [E01 p.2]처럼 적으세요."`(01만 「문장마다」 없음). user 글 = 근거 줄들 + 빈 줄 + `질문: …`
- **예산 값**: `total_budget = 600`·`output_reserve = 120`·`safety_margin = 40` → `available = 440`(07 실행 2만 300 → 140). **메시지 3개 목록의 추정과 실제 차이는 01~07 모든 목록에서 14**(「이번 목록에서도」로만 씀, 메시지 형식 표시로 「보이는」 몫). `페르소나 + 과업 명세 토큰 수: 55`
- **데이터(글자까지 같게 이어 씀, 출처는 `labs/data/rag-corpus/pdf/easy/E0N.pdf` 쪽을 사람이 옮겨 적음)**
  - 02 `records` 5개(키 `출처`·`기관`·`주제`·`내용`): E01 p.2 미르시립도서관 휴관 「매주 월요일은 정기 휴관일입니다.」 / E01 p.3 대출 「도서는 7권까지 14일 동안 대출할 수 있습니다.」 / E01 p.5 주차 「회원은 최초 2시간 무료입니다.」(= `data/memory.json`, 테스트가 요구) / **E02 p.5 별빛제과 주차** 「본사 주차장은 선착순이며 월 3만 원의 주차비가 급여에서 공제됩니다.」(05 무관한 기록) / **E04 p.2 청담해운 대출** 「무주택 직원의 전세자금 대출 기간은 2년이며 2회 연장할 수 있습니다.」
  - 03 `loan_original`(E01 3쪽 「4. 자료 대출」 세 문단, 243자·141토큰), `keep_words = ["7권", "14일", "예약이 없는 경우", "1회", "7일 연장"]`, `loan_note` 「회원 한 사람의 도서 대출 기준은 7권·14일이며, 다른 이용자의 예약이 없는 경우에만 1회 7일 연장할 수 있습니다.」(39토큰, 테스트가 요구), `closure_note` 「매주 월요일은 정기 휴관일이고 법정 공휴일에도 휴관하며, 공휴일이 월요일과 겹치면 다음 화요일도 휴관합니다.」(40토큰, 테스트가 요구), `closure_question = "미르시립도서관의 정기 휴관일은 언제이고, 공휴일이 월요일과 겹치면 어떻게 되나요?"`(01·03·04·05·07), `closure_keep_words = ["월요일", "법정 공휴일", "화요일"]`, `loan_question = "미르시립도서관에서 빌린 도서의 대출 기간을 연장할 수 있나요?"`
  - 04 `memo_note`(출처 「상담 메모」, 일부러 틀린 글 「미르시립도서관은 매주 월요일 하루만 휴관하고, 공휴일에는 문을 엽니다.」), **E02 p.2 별빛제과 급여** `pay_note` 「급여는 매월 25일에 지급되며, 25일이 주말이나 공휴일이면 그 전 영업일에 지급합니다.」
  - 06 `hours_text`(E01 2쪽 이용 시간)·`loan_text`(3쪽 자료 대출)·`way_text`(5쪽 찾아오시는 길, 「이후 30분마다 500원」 포함), `documents`(키 `출처`·`제목`·`설명`·`내용`), `catalog`(키 `출처`·`내용`), `condition_words = ["예약이 없는 경우", "1회", "7일 연장"]`
  - 07 `plans`(키 `이름`·`질문`·`출처`·`지킬 말`·`줄인 기록`), 주차 질문 「미르시립도서관에 회원이 차를 세우면 몇 시간 무료이고, 그 뒤에는 요금이 얼마인가요?」·지킬 말 `["2시간", "30분마다 500원"]`
- **요청 없이 늘 같은 값**: 01 추정 187, 02 124, 03 대출 128·휴관 136·한 목록 213·나눈 합 264, 04 혼란 235·충돌 170·Before 124, 05 456·3336·32136·0개 136, 06 목록만 159·전체 420·고른 217·줄인 128·E01 p.5 192, 07 본문 목록 184·217·197·줄인 기록 목록 136·128·103
- **출력 라벨(대표)**: 「수업 예산:」「출력 예약분:」「여유분:」「입력 가용분:」「추정 입력 합계:」「입력 가용분 안에 드는가:」「답:」「실제 입력 토큰 수:」「실제 출력 토큰 수:」「끝난 이유:」「실제 입력 - 추정 입력:」「답의 출처 표시와 같은 기록:」「…에서 빠진 지킬 말:」「기록표(…):」(05 — 본문은 「요청 기록표」로 부름)「요청 전 표(…)」「요청 뒤 표(…)」「예상 비용 합계(달러):」(절마다 전체 목록은 handoff)
- **비유와 삽화(Ch 7 한 책상 색 약속을 이음: 파란 명찰 = system 페르소나, 주황 클립보드 = developer 과업 명세, 노란 메모지 = 질문, 빈 답안지와 연필 = 출력 예약분)**: 01-5 세로 테이프로 나눈 긴 책상(구역 = 예산 나누기, 가운데 빈 띠 = 여유분, 바닥 열린 상자 = 목록에 넣지 않은 자료) → 02-5 초록 탭 카드(고른 기록)·바닥 **기록 카드 상자**(기록 파일, 탭 색 = 메타데이터) → 03-5 떨어진 작은 책상 둘(업무별 목록)·바닥 긴 종이의 초록 형광 띠(지킬 말, 줄 수 ≠ 개수) → 04-5 2×2 책상(갈색 **종잇조각** = 상담 메모, 아주 높은 종이 더미 = 산만·실행 안 함) → 05-5 높이만 다른 종이 더미 셋(무관한 기록, 비율 아님 — 04 더미와 뜻이 다르다고 적음) → 06-5 목록 카드·책꽂이 빈칸·펼친 하늘색 책(본문) → 07-4 긴 책상(예산 600, 펼친 책)·짧은 책상(300, 카드)·바닥 **회색 통**(보내지 않은 주차 기록, 빈 점선 네모 = 빠진 지킬 말). 일상 예: 시험지에 인쇄된 지문(컨텍스트), 용돈에서 교통비 먼저 떼기(예산), 공책에 적어 두기·과목 쪽 펴기(Write·Select), 긴 공지문을 문자로 옮길 때 「단, …」 남기기(Compress), 과목별 공책(Isolate), 잘못 적힌 인수인계 메모(오염), 두꺼운 업무 일지(산만), 옆에 놓인 급여 안내문(혼란), 「공휴일 휴관」과 「공휴일 개관」이 함께 붙은 게시판(충돌), 두꺼운 회의록(컨텍스트 로트), 책등 분류 번호(메타데이터)
- **쓰지 않은 말(검토 C-3 반영 뒤)**: 「조각」(Ch 5 토큰 — 04 삽화는 「종잇조각」), 「청크」, 「필드」·「칸(필드)」, 「빈자리」(Ch 7 틀의 채울 자리 — 01은 「여분 자리」), 「카드 상자」 단독(Ch 4 표 — 02는 「기록 카드 상자」), 「쟁반」(Ch 4·5), 「압축」「독립 메시지」「출처 식별자」「통제 조건」, 「요약」(사람이 줄인 것에는 안 씀). **Ch 8 그림의 subgraph는 「칸」**(05-3 「큰 상자」도 칸으로 맞춤). 「기록」 두 뜻: 02~04·07 「기록/줄인 기록」 = 사실 한 문장 딕셔너리, 05·06·07 「요청 기록/요청 기록표」 = 요청 한 번의 측정값(05·06 코드 주석·출력 라벨은 옛 말 「기록 한 줄」「기록표」 그대로 — 다시 실행할 때 맞춤)

## 3. 07 실습 절 주제와 결과

- 「컨텍스트 엔지니어링 실습: 도서관 안내 질문 세 개에 예산표와 지킬 말 검사 붙이기」(30분, 따로 과제 없음, 「강사와 함께 실행」). 질문 계획 `plans` → `choose_evidence()`(06 본문 열기 → 본문 목록 추정 > 입력 가용분이면 03 줄인 기록) → `ask_library()`(04 목록·01 추정·03 넣기 전 지킬 말 검사, **빠진 지킬 말이 없고 추정이 가용분 안일 때만** `invoke`) → `add_answer_items()`(05 `count_marks`·Ch 7 08 비용) → `print_records()`(요청 전 표·요청 뒤 표). 바꾸는 값 하나 = 수업 예산 600 → 300(요청 없는 예산표를 보고 정함, b7)
- 결과(2026-09-17 13:54 새 커널): 실행 1(가용분 440) 세 질문 모두 본문·보냄 — 휴관 `198 | 52 | stop | 1 | ['법정 공휴일'] | 0.000382`, 대출 연장 `231 | 104 | stop | 2 | [] | 0.000641`, 주차 `211 | 30 | stop | 1 | [] | 0.000293`(답에 「이후에는 30분마다 500원」), 합계 0.001316. 실행 2(가용분 140) 세 질문 모두 줄인 기록 — 휴관 `150 | 66 | stop | 2 | [] | 0.000409`, 대출 연장 `142 | 59 | stop | 2 | [] | 0.000372`, **주차 `103 | ['30분마다 500원'] | 보내지 않음`**, 합계 0.000781
- 결론: 「이 조립 함수에서는 예산을 줄이면 본문 대신 줄인 기록이 들어가고, 이번에는 넣기 전 지킬 말 검사가 조건이 빠진 주차 기록을 막았다」, 「요청 뒤 답 검사는 실행 1 휴관 답에서 빠진 `법정 공휴일`을 찾았다」(본문에 있던 말, 01 After 답과 같은 모양 — 한 번 본 결과라 일반화·원인 판단 안 함). 입력 429 → 292(137토큰)는 넣은 자료가 정한 값, 비용 차이 약 0.00054 = 주차 요청 0.00029 + 입력 0.00010 + 출력 31토큰 0.00014(출력 쪽은 요청마다 달라짐)
- **시수**: 07 실습 30분은 `_build.py` 「16h · 강의 6h · 실습 10h」에 더하지 않고 실습 10h 안(규격 §7-2). 07은 파일을 쓰지 않음(runs·`memory.json` 해시 영향 없음, 재실행 전후 확인)

## 4. 다음 챕터(Part 3 Ch 09 RAG 첫 실행)가 이어받을 것

Ch 9는 6절(01 RAG 지도 · 02 로더와 스플리터 · 03 임베딩과 벡터스토어 · 04 생성과 출처 인용 · 05 첫 실패 보기 · 06 실험 하네스)이고 아직 개선 전입니다(`qa/upgrade/` 비어 있음). 아래는 개선 전 Ch 9 `_src`를 읽고 확인한 것입니다.

- **빌드 도구(PLAYBOOK §2 7단계)**: Ch 9도 `chapter.json`이 없고 자체 `_build.py`(`SECTIONS`, `{{img:이름|캡션}}` 두 칸, `{{mermaid:}}` 없음). **Ch 8 01이 한 방법을 그대로 쓸 수 있습니다**: `part2/ch08-context-engineering/_build.py`의 `inline_mermaid()`·`inline_illustration()`(`textbook/_template/builder.py` `_inline_mermaid`·`_inline_img`와 문자열까지 같은 출력, 옛 두 칸 모양 하위 호환), 치환 뒤 `\{\{[a-z]+:` 잔존 검사(마감 때 넓힘). 바꾸기 전후 기존 HTML 해시가 같은지 확인. `run_section.sh`는 `chapter.json`이 없으면 verify를 건너뛰므로 `verify.py --chapter`를 따로(가상환경 `.cache/vm/venv-ch09-…`가 있으면 그 환경). `upgrade_gates.py`·`mdpatch.py`는 `chapter.json` 없이 `_src/NN-*.html`·`labs/<part>/<ch>` 경로로 동작(Ch 8 확인). 실습 절 07을 붙일 때 `SECTIONS` 제목에 주제까지(규격 §7-2, Ch 8 검토 B 07-1)
- **E01 원문**: Ch 8은 `E01.pdf` 2·3·5쪽을 사람이 읽고 **pypdf 추출의 띄어쓰기(「정기 휴관일 입니다」「7일 연장 할」)를 바로잡아** 셀에 옮겨 적었습니다. Ch 9 01은 같은 PDF를 `pypdf`로 쪽마다 읽으므로 추출 글자가 Ch 8 글과 다를 수 있습니다 → 「Ch 8과 같은 글」이라고 쓰기 전에 출력으로 확인. 출처 표시 모양 `[E01 p.2]`는 Ch 9 01 답 `[E01 p.쪽]`과 같음
- **이어 쓸 연결(확인한 문장)**: Ch 9 01 b2 「Ch 8에서 … Select는 "지금 필요한 것만 골라 넣는다"였고, 실습에서는 사람이 손으로 골랐습니다」 = Ch 8 02 골라 넣기·06 사람이 목록에서 출처 고르기·07 b8(「사람이 목록을 보고 적던 출처를 Ch 9에서는 검색이 고릅니다」). Ch 9 04 b3 「Ch 8 모델에 넣을 정보량」은 01 토큰 예산·입력 가용분으로 이을 수 있음(Ch 9에서 k를 늘리면 추정 입력이 늘어난다는 문장은 Ch 9 출력으로 확인)
- **고칠 것(Ch 9 개선 때)**: (1) **Ch 9 05 b3** 「Ch 8 실패 모드 Distraction·Confusion — 관련 없는 청크가 … 산만해지거나 혼동」은 Ch 8 04 정의와 어긋남 → 「관련 없는 문서 덩어리(청크)가 목록에 들어오는 조건은 Ch 8 04절 혼란과 이어짐, 산만은 아주 긴 컨텍스트에 치우치는 경우의 이름」으로, 한국어 이름 오염·산만·혼란·충돌을 씀. (2) **Ch 9 01 `_src` 38·42행**이 청크를 「조각」으로 정의(과정 요약 Part 1 §5) → 「문서 덩어리(청크)」. (3) Ch 9 「메타데이터」는 Ch 8 02 용어(내용 옆 설명 값, 책등 분류 번호)와 같은 뜻으로 잇기. (4) 답 확인은 Ch 8처럼 「말·표시가 있는지만 보는 검사, 품질 점수 아님」 — 검색 지표·평가셋은 Ch 11
- **용어 약속(Ch 9 연결 문장에서 뜻 바꾸지 않기)**: 컨텍스트·컨텍스트 윈도·토큰 예산(수업 예산)·출력 예약분·여유분·입력 가용분·추정 토큰 수, 적어 두기(Write)·골라 넣기(Select)·줄이기(Compress)·나누기(Isolate), 기록(02 뜻)·요청 기록(Ch 6·7 뜻)·기록 파일, 출처 표시, 지킬 말·줄인 기록, 오염·산만·혼란·충돌, 컨텍스트 로트, 단계적 공개. §2 「쓰지 않은 말」도 그대로
- **실습 폴더 모듈 주의(규격 §7-2)**: `labs/part2/ch08-context-engineering/context_lab.py`·`examples/`의 같은 주제 함수는 개선 전 영어 모양이고 노트북은 쓰지 않음. Ch 9 노트북·실습 코드는 Ch 8 모듈·runs를 읽지 않음(2026-09-17 grep: `context-design-continuity` 읽는 쪽은 Ch 8 테스트·`textbook/qa/check_course_continuity.py`·`run_course_bundle.py`·`textbook/_notebook/build_bundle.py`·part4~7 `qa/before-integration/build_bundle.py`뿐)
- **요청을 기다리는 반복문 안 `print` 금지·반복 요청은 `append`만**(Ch 6 인계 유지), 모델 설정은 `temperature=0, reasoning_effort="none"`, 출력 상한을 줄 때는 「출력 예약분」과 잇기

## 5. 아직 가르치지 않은 것 (Ch 09가 설명 없이 전제하면 안 되는 것)

Ch 7 요약 §5 전체에 더해, Ch 8에서도 하지 않은 것:

- **검색·문서**: 검색·임베딩·벡터스토어·`Document`·로더·스플리터·청크(모두 Ch 9~), PDF를 코드로 읽기(`pypdf` — Ch 8은 원문을 옮겨 적음), 모델에게 목록을 보여 주고 문서를 고르게 하기(도구·에이전트 Ch 19~), 한 목록에 여러 출처 본문 열기, 목록 설명 품질 평가
- **컨텍스트 기법**: 모델에게 요약·줄이기 맡기기(Ch 16 03·Ch 22 03), 지킬 말을 코드가 원문에서 뽑기, 뜻 보존 자동 판정, 서브에이전트·보안 격리(Ch 26), 한 목록에 두 업무를 실제로 보낸 답(03은 추정만), 산만 재현·한 답에 여러 실패 이름 재현, 대화 기록에 틀린 앞선 답 넣기(`AIMessage`), 문서 속 프롬프트 인젝션(Ch 16 06), 도구가 많을 때의 혼란(Ch 19 04), 서비스 모델에서 근거 자리 바꾸기, 질문과 비슷한 방해 기록, 조건이 빠진 줄인 기록을 실제로 보낸 답(07은 보내지 않음), 질문별 예산
- **측정**: 같은 조건 반복 요청으로 평균·가운데 값, 답 정확성 판정·비율 지표·LLM 판정자(Ch 11·15), 걸린 시간(Ch 8은 안 잼 — Ch 6 06·Ch 7 01 `timed_invoke`는 배움), 캐시 입력이 생기는 조건·유지 시간(05에서 값만 봄), 1만 개 이상 긴 입력 실제 요청
- **파일·Python**: `json.dump()`·`json.load()`, 파일 덧붙이기로 기록 추가·수정·삭제, 판·시행일 날짜 조건, `runs/` 밖 기록 파일 쓰기·지우기·옮기기, 파일 지문으로 바뀐 파일을 잡는 실제 재현, `Path`·`next`·`datetime`·f-string·`join`·`raise`·try·내포식·`+=`·`sum`·`max`·`@`·`BaseModel`·타입힌트, Windows·macOS 경로 동작

## 6. A·B 트랙 제약

- Ch 8은 `@` 줄·`BaseModel`·`Field` 0건이라 규격 §2-2 세 문장이 필요한 자리가 없었음. try/except도 0건. A 트랙 학생 기준으로 막히는 문법 없음
- 06 `hashlib`·`os.makedirs`·`time.strftime`은 Ch 7 08(A·B 공통)에서 배운 뜻 그대로 한 문장씩만 다시 풂

## 7. 기준 버전·요금 확인 날짜

- 실습 폴더 `labs/part2/ch08-context-engineering/pyproject.toml`·`uv.lock`: langchain **1.4.0**, langchain-core **1.6.2**, langchain-openai **1.6.0**, **openai 3.8.0**(Ch 6·7은 3.10.0), tiktoken **0.14.0**, python-dotenv **1.2.3**, pypdf **6.18.0**(노트북은 쓰지 않음). 새 커널 `nbclient==0.11.0`·`ipykernel==7.3.0`, Linux aarch64 Python 3.12.13. 노트북 준비물마다 기준 버전과 「다른 버전과 Windows·macOS에서는 이번에 실행하지 않았습니다」
- 요금(100만 토큰당 달러): mini 입력 0.75·캐시 0.075·출력 4.50 — **Ch 6 06절에서 2026-09-17에 확인한 값**(Ch 8은 요금 페이지를 다시 열지 않고 인용). 06 기록 파일 `settings.pricing_date` `2026-09-17`. 강사용 `DEVELOPMENT.md` 2026-09-08·`context_lab.py` 2026-09-07 확인일은 서로 다름(§12)
- 문서 확인 2026-09-17: OpenAI `gpt-5.4-mini` 모델 안내(400,000·128,000, 스냅숏 `gpt-5.4-mini-2026-03-17`), Drew Breunig 「How Long Contexts Fail」(2025-06-22, 네 정의·Databricks 32k·도구 여러 개·39% 하락), LangChain 「Context Engineering」(2025-07-02), Anthropic 「Effective context engineering for AI agents」(2025-09-29)·「Equipping agents for the real world with Agent Skills」(2025-10-16), Chroma 「Context Rot」(2025-07-14, 모델 18개)
- 소스 확인: tiktoken 0.14.0 「gpt-5」 접두어 → `o200k_base`, langchain-openai `get_num_tokens_from_messages()` = 187 + 메시지마다 경계 3 + 역할 이름 1 + 답 시작 3 = 202(검토 A, 본문에는 「보이는 몫」까지만)

## 8. 실행 환경

- Cowork 기기 셸(Linux aarch64). 가상환경 `$ROOT/.cache/vm/venv-ch08-context-engineering`, uv 캐시 `$ROOT/.cache/vm/uv`(`run_section.sh` 자동, torch 없음, 새 커널 10~15초). 키는 루트 `.env`(`find_dotenv(usecwd=True)`), 값은 출력하지 않음. 기기 루트 여유 약 550MB(마감 시점)
- 결과 읽기 채우기: 생성기에 `[[READ_…]]` 자리 표시 → 두 번째 새 커널 뒤 `mdpatch.py`. 노트북 단락은 **빈 줄로만** 나뉘어 G6가 5문장을 셈. 「오늘 볼 그림」 alt에는 자리 표시를 두지 않음
- 서비스 모델 절 설명 수정: `mdpatch.py` → `run_section.sh … NN --no-exec`만. `mdpatch.py`는 생성기·노트북·`_src`에 같은 글을 **모두** 바꾸므로 여러 줄 치환은 `\n`까지 넣어 한 자리만 맞추고, 반영 전후 노트북 코드+출력 해시를 비교(`/tmp/ch08-close/nbhash.py`)
- Mermaid: 렌더 도장은 지우지 않음(mmd를 고치면 자동, 같은 mmd는 `--force`). 칸 안 세로 쌓기는 `direction TB` + `a ~~~ b`, 긴 라벨은 `<br>` 위치 직접, LR 네 상자 한 줄은 폭 873 → 라벨 세 줄
- `visual.cjs`는 공용 도구를 고치지 않고 `/tmp/ch08-close/vis/vis.cjs`(`require('/tmp/pw/node_modules/playwright')`) + `LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu`, HTML 사본 폴더. 결과 JSON 키는 `passed`
- 테스트: `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=$ROOT/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch08-context-engineering uv run --project labs/part2/ch08-context-engineering --with pytest python -m pytest -q -p no:cacheprovider --basetemp=/tmp/… labs/part2/ch08-context-engineering/tests`. `check_course_continuity.py`는 Ch 6 가상환경으로(시스템 `python3`에 `tomllib` 없음), 끝까지 통과하면 225행에서 결과 파일을 씀

## 9. runs 사슬 최종 상태·계약·테스트 (Part 2 사슬 끝)

**해소 순서 완료**: (1) Ch 6 06 → (2) Ch 7 08(07:07) → (3) **Ch 8 06 품질 개선 새 커널 실행(2026-09-17 12:16:54)** → (4) Ch 8 테스트 수정. 검토 반영·마감 전후 모든 해시 같음.

| 파일 | SHA-256 | 비고 |
|---|---|---|
| `labs/part2/ch06-langchain-start/runs/provider-comparison-continuity.json` | `f18920c63088bded645bc4712b8ee16436e46d394499bfeaa4cc081f76ef4f4c` | 사슬 처음 |
| `labs/part2/ch07-prompt-engineering/runs/prompt-ab-continuity.json` | `a8aaafb775e710438a1bd9e5d79340d3032f61be30c4dbb2e8aa4dd7b82095e9` | run_id `ch07-prompt-ab-20260917T070701`, 출처 = Ch 6 |
| `labs/part2/ch08-context-engineering/runs/context-design-continuity.json` | **`125fc147e81fb8b6234ff87045120a30f9fdccd6bae52fc0dc8d7c68670e58ad`** | run_id `ch08-context-20260917T121654`, 출처 = Ch 7 |
| 위 파일 — **§2-7 리팩터로 바뀜(2026-09-21) 전 → 후** | `125fc147…58ad` → **`043750eeffb6dc15f56b915da51e87dd69e51adcfd266dbdbd246abb0a66a5d2`** | run_id `ch08-context-20260921T050226`, 출처 = Ch 7 `434640f4…a561`(run_id `ch07-prompt-ab-20260921T034935`), 사본 `continuity/20260921T050226/`(옛 사본은 `qa/upgrade/before-2-7/runs/moved/`) |
| `…/ch08-…/runs/continuity/20260917T121654/context-design-continuity.json` | 같음 | 사본 **하나**(첫 새 커널 사본 `20260917T121541`·옛 사본 3개는 `qa/upgrade/before/runs/continuity/`) |
| `…/ch07-…/runs/prompt-ab-v1.json` | `16a4b67210853c925e75ced02cc88fa704957aa196a2572a05f8fce49fbf4341` | 바꾸지 않음 |
| Ch 8 `runs/ex01_budget.jsonl`·`ex04_failures.jsonl`·`ex05_rot.jsonl`·`ex06_compare.jsonl` | `e3b6a71d…`·`d23dbb45…`·`6a9db927…`·`5cb060d6…` | 개선 전 예제 실행 증거, `test_legacy_logs_are_unchanged` |
| Ch 8 `data/memory.json` | `0aa9fae5d8240aa6d9f01fb373871ead4b4b6b35e6c057eab2aaf6a6899fabd2` | 02 기록 세 글과 같음 |

- **Ch 8 파일 계약(바꾸지 않는 것)**: 최상위 키 7개 `run_id`·`run_date`·`source_chapter`(`ch08`)·`source_record{path(프로젝트 맨 위 기준 상대 경로), sha256, run_id}`·`settings{model, temperature 0, reasoning_effort none, max_tokens 120, pricing_date 2026-09-17, pricing_usd_per_million {0.75, 0.075, 4.5}}`·`question`·`results`(**목록 3개**, 원소 한국어 키 8개 `설계`·`답`·`입력 토큰 수`·`캐시 입력 토큰 수`·`출력 토큰 수`·`끝난 이유`·`예상 비용(달러)`·`답에서 빠진 연장 조건`), `runs/continuity/*/`에 같은 바이트 사본. 06 노트북 코드 셀의 `estimate_openai_cost(usage, input_rate=0.75, cached_input_rate=0.075, output_rate=4.50)`(테스트가 인자 하나로 `0.000093`), 06 원문의 「회원은 최초 2시간 무료입니다.」·「90분 무료」 없음, 02 원문 같은 조건, 03 원문 「공휴일이 월요일과 겹치면 다음 화요일도 휴관」·「회원 한 사람의 도서 대출 기준」(`test_ch08_source_ids_match_preserved_memory`)
- **읽는 쪽**: Ch 8 `tests/test_ch06_ch08_continuity.py`(5개), `textbook/qa/check_course_continuity.py` 66~76행(`part2_handoffs` 경로·지문·run_id·사본)·172~199행(노트북 불변 조건, 07은 목록 밖), `textbook/qa/run_course_bundle.py` 104~111행, `textbook/_notebook/build_bundle.py` 81~87행. Ch 9 이후 노트북·실습 코드는 읽지 않음(§4)
- **뒤 챕터가 이 파일을 다시 쓸 때 규칙**: Ch 8 06을 다시 실행하면 해시가 바뀌고 사본 폴더가 하나 늘어 06 본문·그림 인용 숫자와 이 표가 어긋남 → (a) 먼저 위 읽는 쪽 코드를 확인하고, (b) 06 인용 숫자 전부·이 표·진행표를 새로 맞추고, (c) 앞 사본 폴더는 `mv -n`으로 `qa/upgrade/before/runs/continuity/`에 옮김. **Ch 7 08·Ch 6 06을 다시 실행하면 Ch 8 06 출처가 끊김** → 코드를 꼭 고쳐야 하면 Ch 6 06 → Ch 7 08 → Ch 8 06 순서로 함께 재실행. 07 실습은 파일을 쓰지 않으므로 사슬과 무관
- **테스트 상태**: **21 passed**(Ch 6·7·8 연결 5개 + 예제 16개), 마감 전후 같음. 06에서 `test_log_paths_are_portable_from_student_working_directories`를 노트북 `os.path.exists` 경로 방식 확인으로 고침(수정 전 사본 `qa/upgrade/before/test_ch06_ch08_continuity.before-06.py`, 검토 B가 「약해지지 않음」 판정). `check_course_continuity.py`는 73행·172~199행 통과, **212행 `Stale archive: part1-practice.zip/…`에서 멈춤**(전체 마감 zip 재생성 대상, Ch 8과 무관)
- **R-1(Ch 6 06·Ch 7 08)**: 실습 폴더 맨 위에서 열면 경로를 못 찾음 → 두 노트북은 그대로(재실행 금지), **Ch 8 06은 후보 세 개 `for`+`break`로 해소**
- **R-2(새 알려진 제한, 코드 고치지 않음)**: Ch 8 06 [25] 경로 고르기 조건이 「`runs`와 `notebooks`가 있다」뿐이라, **다른 챕터 실습 폴더(예: `labs/part2/ch07-prompt-engineering/notebooks`)를 작업 폴더로 열면 그 챕터를 실습 폴더로 고르고** 6절이 그 챕터 `runs/`에 기록 파일과 사본을 씀(검토 B chdir 실행으로 경로 셀 확인, 쓰기는 코드 논리). 06 재실행 금지라 06 b7 주의 항목·06 노트북 준비물·README에 「이 챕터의 세 작업 폴더에서 연다」만 적음. 다음 재실행 때 조건에 `os.path.exists(candidate + "/notebooks/06-단계적-공개와-설계-비교.ipynb")`를 더하고, 테스트는 06 [25] 셀 원문을 꺼내 세 작업 폴더에서 `exec`하는 방식으로 보강(검토 B 권고, 이번에는 테스트를 읽기 전용으로 둠)

## 10. 그림 색 판단 선례

- 넣은 글·기록·목록·원문·사람이 정한 지킬 말·예산 값·기록 파일 **초록**(틀린 상담 메모도 「넣은 기록」이라 초록), 정의한 함수(`input_budget`·`find_missing_words`·`build_long_notes`·`make_length_record`·`open_document`·`choose_evidence`·`ask_library`·`add_answer_items`·**`print_records`** — 검토 B 07-4로 노랑에서 파랑)·`hashlib.sha256`·코드 단계 **파랑**, 실행한 `gpt-5.4-mini` **보라**, 출력으로 확인한 값·검사 결과·추정 입력·「보내지 않음」(코드가 정해 기록한 결과)·`False`/넘침(값 바꿔 보기) **노랑**, 실행하지 않은 요청·단계(산만, 한 목록 요청, 열지 않은 문서, Ch 6 → Ch 7 연결)·모델 최대 한도·함께 바뀐 조건 설명 **회색**(점선은 화살표). **빨강은 paired Before 결함 결과 한 상자씩**(01-4·02-4·03-4·04-3·06-4), experiment 05·07은 0장
- 원인 과장 막기: 두 조건 답에 모두 있던 값은 결과 상자에서 뺌(02-4 주차 2시간, 03-4 1회 7일 연장, 04-3 정기 휴관일·출처 모양, 05-4 빠진 지킬 말 없음, 06-4 `[E01 p.3]`, 07-3 대출 연장 빠진 말 없음). **두 실행에서 달라진 값은 양쪽 칸에 모두 적음**(07-3 휴관 `법정 공휴일` / 없음, 재실행 뒤)
- 모양: 도식 읽기의 점선은 「점선 화살표」로 부름(상자 테두리는 실선 — 04 [1]·06-1 검토), subgraph = 「칸」, sequenceDiagram 메모는 응답 직후·반복 뒤, 두 줄 메모는 `<br>`(07-2 viewBox 787)

## 11. 강사 확인 대상

- **강의·실습 범위 문장**(01~06 노트북 준비물 「**강의와 실습 범위**」 + `_src` b5 한 단락, 검토 A C-5): 01 강의 2~6절·실습 7~9절, 02·03·04 강의 3·4·6절·실습 5·7절, 05 강의 3·5·7절·실습 4·6절, 06 강의 4·5·8·9절·실습 3·6·7절(05·06은 작업자가 정함)
- **meta 시수**: 01 「1h\|1h」, 02~05 「1h\|2h」, 06 「1h\|1h」 → 합 강의 6h·실습 10h = `_build.py`·커리큘럼 v6 16h(유지). 06이 코드 셀 31·검사 문장 513으로 가장 무거운데 실습 1h인 배분(바꾸면 다른 절 하나를 함께 내려 합 유지 — 검토 B C-3). 07 30분은 실습 10h 안
- 결정 권고대로 유지한 설계(A Q1~Q6·B Q1~Q4): 01 탐색 뒤 정한 600·120·40, 02 Before·E02·E04 기록, 03 나누기가 토큰을 줄이지 않은 해석, 04 네 이름 정의·상담 메모, 05 「요청 전 비용 상한」 말 유지 + 여유분 문장, 탐색 뒤 정한 무관한 기록 수, 06 비용 순위 보류·연장 조건 세 개, 07 예산 300·새 함수 4개
- 07 재실행으로 결론에 더한 「요청 뒤 답 검사가 실행 1 휴관 답의 빠진 말을 찾음」 문장과 07-3 휴관 두 상자
- 05 표시 제목 한국어 먼저(slug 유지), 07 표시 제목에 주제, 「요청 기록」 통일
- 규격에 더한 세 줄(§2-2 L2 함수 본문 줄 수는 게이트가 세지 않으니 직접 세기, §3 검토 반영 재실행에서 출력이 달라져도 원하는 출력이 나올 때까지 다시 실행하지 않기, §7-2 자체 빌드 챕터 목차 페이지 문장을 마감 때 절 본문과 대조)과 PLAYBOOK §4 세 줄

## 12. 남은 것

- **전체 마감 때**: `textbook/downloads/part2-practice.zip`(Ch 6~8 개선 전, 07 없음) 재생성 뒤 `check_course_continuity.py` 끝까지(225행 결과 파일 씀), Part 2 목차(`textbook/part2/_build_index.py`·`index.html`, Ch 8 절 수·제목) 재생성, Part 2 과정 요약(`textbook/qa/upgrade-course-summary.md` 끝 `# Part 2`), 과거 결과 목록에 남은 `_make_notebooks.py` 경로(`textbook/_notebook/checks/topic-alignment-lint.json`·`plain-language-contracts.json`, `textbook/qa/continuity-evidence/before-manifest.json`·`part3/qa/continuity-evidence/before-manifest.json`) 재생성
- **챕터 밖으로 넘긴 것**: Ch 7 04 b6 「기록에서 무엇을 고르고 줄일지는 Ch 8 02·03절」 → 「무엇을 고르고 줄일지는 Ch 8 02·03절, 대화 기록을 모델로 요약하는 방법은 Ch 16 03절」(검토 A C-6, Ch 7 `mdpatch.py` → `--no-exec`, Ch 7 2차 검토 때), Ch 9 05 b3·01 「조각」(§4), Ch 26 01 「문맥 격리」·03 「나누기(Isolate)」 말 맞추기(Ch 26 개선 때)
- 2차 검토(두 보고서 끝 「2차 검토 때 볼 곳」), 강사 확인
- **다시 실행하면 함께 고칠 코드(지금은 재실행 금지·불필요)**: 05 [43] `make_length_record()`·06 [43] `make_design_record()`의 `run_usage["input_token_details"]["cache_read"]` → `details = run_usage.get("input_token_details", {})` + `details.get("cache_read", 0)`(Ch 6 요약 §12와 같은 모양, 06은 §9 순서), 05 [39] 비용 어림에 `estimate_10 + safety_margin` 모양·그림 05-2 라벨 「요청 전 비용 어림」, 06 [25] R-2 조건·[27] `assert` 메시지 「기록 파일이 있어야 합니다」, 01 [16] 코드 셀(주석 제외 15줄)을 소개 문단 셀·구역 표 셀로 나누기, 05·06 코드 주석 「기록 한 줄」 → 「요청 기록 한 줄」, 07 `print_records()` 물리 11줄(문장 10개 — 규격 L2를 줄 수로 엄격히 보면 넘음)
- 강사용 `DEVELOPMENT.md` 가격 확인일(09-08)과 `context_lab.py` 주석(09-07)이 다름 — 강사용 확장 자료를 손볼 때 확인
- 옛 파일 옮김(삭제 아님, `mv -n`): `labs/part2/ch08-context-engineering/_make_notebooks.py` → `qa/upgrade/before/generators/_make_notebooks.py`(막음 줄 그대로). 옮긴 뒤 빌드 HTML `{{` 0·`verify.py` PASS·테스트 21 passed
- 정리 대상(삭제하지 않고 목록만, 삭제 승인 필요): 옛 도식·삽화 `figures/01-컨텍스트-예산.svg/.excalidraw`·`01-책상-예산.png/.caption.md`·`02-저장과-선택.*`·`03-압축과-분리.*`·`04-실패-진단.*`·`05-길이와-위치.*`·`06-단계적-공개.*`·`figures/_gen_figures.py`, 실습 폴더 `__pycache__`·`tests/__pycache__`·`.venv`(2026-09-09)·`.ruff_cache`·`.pytest_cache`, `qa/upgrade/gates-wip-01.json`~`07.json`, `qa/upgrade/before/06-to-07/`·`before/review-round1/`·`before/runs/continuity/20260917T121541/`, `.cache/vm/venv-ch08-context-engineering`(전체 마감 때), 기기 `/tmp/ch08-01`~`/tmp/ch08-07`·`/tmp/ch08-reviewA`·`/tmp/rv08b`·`/tmp/ch08-close`
