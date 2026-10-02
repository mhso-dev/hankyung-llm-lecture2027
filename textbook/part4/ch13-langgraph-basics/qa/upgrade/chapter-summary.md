# Ch 13 LangGraph 기초 — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part4/ch13-langgraph-basics` 01~08절(01~07 품질 개선 + 08 챕터 끝 실습 절 신설), 노트북 `labs/part4/ch13-langgraph-basics/notebooks/01~08-*.ipynb`.
- 기간: 2026-09-19(01~07절 개선 + 08 실습 절 + 검토 1차 반영·챕터 마감). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 일곱 절 합계 **337**(절별 44·33·35·53·33·43·96, 통과 0/7) → 반영 뒤 **8/8 PASS, G1~G7 0**(`gates-after.json`, `--label after --strict`).
- 코드 셀 24·22·26·27·26·27·32·32 = **216**, 검사 문장 269·271·307·326·314·325·320·381 = **2,513**, Mermaid **31장**(01~07 각 4장 + 08절 3장), 삽화 **8장**(절마다 1장, 모두 채택), 복습 문제는 HTML에만. **§2-7 리팩터로 바뀜(2026-09-21)**: 코드 셀 24·21·24·27·26·24·26·25 = **197**, 코드 줄 1287 → 1131(§17).
- 서비스 요청: 01~06절 **0번**, 07절 **5번**(임베딩 3 + 답 모델 2), 08절 **4번**(임베딩 3 + 답 모델 1). 챕터 전체가 미화 0.02달러 아래입니다. 삽화 크레딧 18(잔액 2707 → 2689, 생성 9회 가운데 02절 1차만 탈락).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → 계약 `textbook/qa/upgrade-contracts.md` → Ch 12 요약 → **이 문서**. 절 사이 세부는 `handoff.md`(400여 행), 절별 기록은 `NN-diagnosis.md`, 검토와 반영은 `review-round1.md`(끝에 「반영 결과」)입니다.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 라이브러리·API | 새로 만든 함수 | 새 용어 |
|---|---|---|---|
| 01 | `TypedDict`, `StateGraph`·`add_node`·`add_edge`·`compile`·`invoke`, `START`·`END`, `get_graph().draw_mermaid()`·`.nodes` | `normalize` · `make_query` · `print_state` · `run_row` | 상태 · 노드 · 엣지 · 상태 그래프 · 가상 시작점과 가상 끝점 · 컴파일 · 실행 흔적 (7) |
| 02 | `Annotated`, `operator.add` | `normalize_whole`(01절 판 다시 보기) | 리듀서 · 덮어쓰기 · 이어 붙이기 · 표시 `Annotated` (4) |
| 03 | `add_conditional_edges`, `path_map` | `choose_path` · `new_state` | 조건부 엣지 · 조건 함수 · 이름표 표 · 기준값 (4) |
| 04 | `add_messages`, `HumanMessage`·`AIMessage`·`AnyMessage`, 속성 `.text` | `write_question` · `write_answer` · `print_messages` | 메시지 리듀서 · 메시지 번호 · 바꿔 넣기 · 공통 형식 `AnyMessage` (4) |
| 05 | `Send`(조건 함수가 목록으로 내놓음), 오류 `InvalidUpdateError` | `inspect_document` · `to_each_document` · `order_rows` | 팬아웃 · `Send` · 갈래별 상태 · 한꺼번에 낸 갱신 (4) |
| 06 | `Command(update=, goto=)`, `add_node(..., destinations=(...))` | `route` · `make_answer` · `ask_more` | `Command` · 담긴 갱신 · 담긴 다음 노드 이름 · 적어 둔 목적지 (4) |
| 07 | `OpenAIEmbeddings(model=, dimensions=256)`·`embed_documents`·`embed_query`, `Kiwi`·`BM25Okapi`, `init_chat_model`(`gpt-5.4-mini`) — 모두 Ch 9~12에서 쓰던 그대로 | `search_distance` · `search_words` · `fuse` · `pick_report` · `make_reply` | 설정 칸 (1) |
| 08 실습 | **새 API·새 문법 0개** | `search_docs`(07절 노드 넷을 하나로) | 0 |

- 새 용어 합계 **28개**. 절 meta의 「새 용어」 칸과 같습니다.
- **쓰지 않은 Python 이름(여덟 절 모두 0건, AST 확인)**: `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·`try`·`+=`·세미콜론·한 줄 복합문·**f-string**·기본값 매개변수·셀당 함수 둘, 그리고 이름 `Literal`·`numpy`·`sklearn`·`pandas`·`key=`·`reverse=`·한 글자 변수(`i` 제외). 부른 내장 이름은 **`len`·`print`·`open`·`range`·`round`·`str`·`sorted`·`type` 여덟 개**뿐입니다. **§2-7로 바뀜**: 노트북은 여전히 `numpy`를 부르지 않지만 도구 파일 `notebooks/rag_tools.py`가 NumPy로 벡터 계산을 하고 02·03·06·07·08 설치 셀에 `numpy==2.5.3`이 들어갔습니다(§17).
- 클래스 정의는 **상태 형식 아홉 개**(`TypedDict`)뿐이고 필드만 적었습니다(규격 §2-2 L5). `assert`는 여덟 절에 **13개**이고 모두 실행 흔적 목록·개수·키 존재 확인입니다. **모델 답에 건 `assert`는 0건**입니다.
- 주석·빈 줄을 뺀 셀 코드 줄 수 최댓값은 **15줄**(07·08절), 함수 본문 최댓값은 **9줄**(07·08절 `rank_by_bm25`)로 규격 §2-2 L2 안입니다. **§2-7로 바뀜**: 셀 최댓값은 `verify.py` 기준 23 → 18줄(주석 포함), 함수 본문 최댓값은 9줄(07 `print_state` — 칸 여덟 줄을 적는 출력 함수, 리팩터 전 그대로, 규격 L2 10줄 안)이고 그다음이 8줄(07 `new_state`·08 `print_state`·08 `search_docs`, 도구 파일 `rank_by_bm25`·`fuse_scores`·`fuse_rank`).

## 2. 상태 형식·칸·노드 이름 (절 사이 약속)

| 절 | 상태 형식 | 칸 |
|---|---|---|
| 01 | `FlowState` | `question`·`query`·`trace`(규칙 없음) |
| 02 | `RuleState` | 같은 칸 셋, `trace`에 `Annotated[list[str], operator.add]` |
| 03 | `RouteState` | `question`·`query`·`score`·`answer`·`trace` |
| 04 | `ChatState` | `question`·`messages`·`trace` |
| 05 | `FanState`(+ 규칙 없는 판 `NoRuleState`) | `question`·`documents`·`results`·`trace` |
| 06 | `DecisionState` | `question`·`score`·`decision`·`answer`·`trace` |
| 07 | `RagState` | 칸 여덟(질문·가중치 설정 칸·순위 둘·후보·보고 자리·답·실행 흔적) |
| 08 | `GuideState` | `question`·`gate`·`score`·`picked_ids`·`decision`·`messages`·`trace` |

- **칸 구성이 바뀌면 상태 형식 이름을 새로 붙입니다**(03 diagnosis §3에서 정한 규칙, 08절까지 지킴).
- 같은 뜻에는 같은 칸 이름: `question`·`query`·`trace`(01~03), `messages`(04·08), `score`·`decision`(03·06·08), `picked_ids`(07·08).
- **02절이 정한 약속**: 규칙을 적은 칸에는 노드가 **자기 몫만** 냅니다(`{"trace": ["이름"]}`). 02~08절 노드가 **전부** 이 모양입니다. 01절만 앞 값을 이어 붙이고 그 사실을 01 b7·02 b3에 적었습니다.

### 노드 `normalize`는 코드가 **두 판**입니다 (2026-09-19 검토 C-3에서 세 판을 바로잡음 → 2026-09-21 §2-7 정리로 두 판)

| 판 | 절 | 모양 |
|---|---|---|
| 앞 흔적을 이어 붙이는 판 | 01(노트북) | `new_trace = state["trace"] + ["normalize"]`(02절이 「하지 말라」고 가르친 모양) |
| 변수 이름 `clean_question`(02절 판) | 02(노트북, 처음 가르침) · 03·04·05·06·08(도구 파일 `rag_tools.py`에서 가져옴) | `clean_question = state["question"].strip()` |

- 07절만 이 노드를 넣지 않았습니다(질문이 Ch 12 `Q002`라 앞뒤 빈칸이 없음, b3에 한 줄).
- 04·05절이 적던 셋째 판(변수 이름 `clean`, 하는 일은 02절 판과 같음)은 2026-09-21 §2-7 정리에서 없앴습니다. 04·05절도 도구 파일의 02절 판을 가져옵니다(`_src` b3 「02절 판을 … 도구 파일에서 가져옵니다」 / 「04절처럼 02절 판을」).
- **「글자까지 같다」는 대조한 절만 적습니다.** 06절은 「02절 판」, 08절 표는 「02절 노드를 도구 파일에서 가져옴」으로 적었습니다. 다음 챕터도 이 기준을 쓰세요(규격 §4에 한 줄 추가).

## 3. 리듀서·`Send`·`Command`·조건부 엣지 사용 규칙

- **리듀서는 칸에 적고 노드는 자기 갱신만 냅니다.** 합치는 일은 칸의 규칙이 합니다(02·04절이 실행으로 보임).
- 한 상태에 **칸마다 다른 리듀서**를 적을 수 있습니다. 08절이 처음으로 규칙 있는 칸 둘(`trace`에 `operator.add`, `messages`에 `add_messages`)을 함께 씁니다.
- **`add_messages`는 번호가 같으면 그 자리 글을 바꾸고 `operator.add`는 번호를 보지 않습니다**(04절 `메시지 리듀서가 만든 수: 3` ↔ `operator.add가 만든 수: 4`).
- **`Send`는 조건 함수가 목록으로 내놓습니다.** 갈래가 여럿인 칸에는 합칠 규칙이 있어야 하고(없으면 `InvalidUpdateError`), 갈래가 하나면 규칙이 없어도 덮어쓰기로 끝납니다. **모이는 차례는 실행에서 본 것이고 라이브러리 약속이 아닙니다** — 차례가 필요하면 자리 번호를 함께 보냅니다(05절 `order_rows`).
- **`Command`는 갱신과 다음 노드 이름을 함께 나릅니다.** 목적지는 `add_node(..., destinations=(...))`로 적고, 적지 않아도 **결과는 같고 구조 문자열만 달라집니다**(06절이 두 판을 모두 실행해 확인). 반환형 `Command[Literal[...]]`은 쓰지 않았습니다.
- **조건부 엣지와 `Command`는 같은 일을 합니다.** 06절이 03절 판을 같은 점수로 실행해 「답 칸은 같고 판단 이유 칸이 빈 글로 남으며 지난 노드 수가 셋과 둘」임을 보였고 **「어느 쪽이 낫다」를 쓰지 않았습니다**. 08절은 그래서 조건부 엣지를 빼고 `Command`만 썼습니다.
- **조건 함수는 `add_node`로 등록하지 않습니다.** 구조 도식에서도 노드와 같은 모양·색으로 그리지 않습니다(03-1 검토, 규격 §5-3에 한 줄 추가).

## 4. 출력 함수와 기록 함수

- `print_state(label, state)`는 여덟 절 모두 같은 이름·인자이고 줄 수만 칸 수에 맞춰 3·3·5·3·4·5·8·7입니다.
- `run_row(...)`의 칸은 절마다 견줄 값에 맞춥니다: 01·02·03·05·06·08은 `(run_name, state)`, 04는 `(list_name, messages)`, 07은 `(run_name, state, parent_ids)`.
- **여러 줄로 나오는 값은 개수만 적고 따로 출력합니다**(규격 §2-4): 04·08절 `print_messages()`, 05절 결과 칸 `for`, 07절 순위 두 칸은 수만·답 칸은 글자 수만.
- 정의 셀마다 결과 읽기에 「정의 셀이라 출력이 없습니다」를 적습니다(G5).

## 5. 색 규칙 — 이 챕터에서 더한 것

- **라이브러리가 주는 것은 클래스 없이 회색**: `START`·`END`(01절) · `add_messages`(04절) · `Send`(05절) · `Command`(06절). 32장에서 예외 0건입니다.
- **우리가 만든 노드와 노드가 낸 갱신은 파랑**, 상태·칸·넣은 값은 **초록**, **출력으로 확인한 값만 노랑**, 두 조건 공통 사실은 **회색**, 모델은 **보라**(`07-2`·`08-2` 둘뿐), **빨강 0장**입니다.
- **01절과 02절이 같은 자리를 달리 칠한 판단**: 01절 `01-2`의 「낸 갱신」은 노랑(그 절이 갱신을 출력함), 02절 `02-2`·`02-4`는 파랑(출력하지 않음). 03~08절이 그 자리를 그대로 지켰습니다.
- 잡아서 출력한 오류는 노랑입니다(05절 `InvalidUpdateError`, 규격 §5-3·Ch 6 02-1 선례).
- 도식 모양: 칸 두 개를 나란히 둘 때는 `flowchart LR` + 칸 안 `direction TB` + `~~~`. 원본 viewBox 폭은 모두 **868 이하**(최대 845.2, `02-3`)입니다. 갈래(조건부 엣지·`Command` 목적지)는 **점선 `-.->`**로 그립니다(`03-2`·`06-2`·`08-1`, 라이브러리 구조 문자열과 같은 모양).

## 6. 07·08절이 Ch 12에서 이어 쓴 것

- **함수 열한 개를 이름·인자·코드까지 같게 다시 정의**했습니다(AST 대조): `dot_product` · `vector_length` · `cosine_similarity` · `cosine_distance` · `kiwi_terms` · `rank_by_distance` · `rank_by_bm25` · `fuse_scores` · `fuse_rank` · `unique_chunk_ids` · `parent_ids_of`. 07절은 준비 셀 **일곱 개**, 08절은 **여섯 개**에 담고 `lesson_role="setup"` + `upgrade_allow=["multiple_defs_in_cell"]`을 붙였습니다(Ch 12 09절 방법). **§2-7 리팩터로 바뀜(2026-09-21)**: 07·08은 이제 다시 정의하지 않고 도구 파일에서 여섯 개(`kiwi_terms`·`fuse_rank`·`unique_chunk_ids`·`parent_ids_of`·`rank_chunks_by_distance`·`rank_chunks_by_bm25`, Ch 12 도구 파일과 같은 본문·NumPy)를 가져옵니다. `dot_product`·`vector_length`는 없어졌습니다(§17).
- **이어 쓴 값**: 부모 문서 **6건** · 문서 청크 **175개**(`data/advanced-documents.json`) · 순위 상수 **60** · 1차 후보 **8**(07절) · 보고 자리 **5** · 모델에 넣을 자리 **3** · 임베딩 `text-embedding-3-small`·`dimensions=256` · 답 모델 `gpt-5.4-mini`·`temperature=0`.
- **읽기만 한 Ch 12 파일 두 개**: `labs/part3/ch12-retrieval-tuning/data/advanced-documents.json`(07·08절) · `runs/advanced-continuity-integrated-result.json`(07절만, sha256 `ce76d3d8…` — **§2-7로 바뀜 → `7b142cd5…`**, Ch 12 §2-7 리팩터가 다시 쓴 판. `run_id` 말고 내용 같음, 07절이 읽는 값 같음). **바이트가 그대로입니다**(마감에서 `before-manifest.json`의 `runs/`·`data/` 125개를 다시 계산해 어긋난 항목 0건).
- **Ch 12 요약 §13-2 인계는 07절에서 처리했습니다**: b3과 `qa/author_ch13.py` 261~265행의 「검색된 E01·E02 쪽」을 실제 값(`E01-P03-C02`·`E01-P03-C01`·`E01-P03-C06`, `reranker` `None`, `context_selection` `matched-chunk-text`)으로 고쳤습니다.
- **리랭커는 부르지 않습니다**(파일 약 2.2GB·메모리 약 3GB, Ch 12 12·13절이 고른 설정도 `reranker` `null`). contracts §7과 같습니다.

## 7. 서비스 요청과 흔들리는 값

- 01~06절 **0번**(그래프 구조·상태 규칙이 주제라 API 키 셀도 두지 않음), 07절 **5번**, 08절 **4번**. 코드로 세어 본문·준비물·실습 폴더 `README.md`와 같습니다.
- **인용하지 않은 값**: 모델 답 문장과 글자 수(07절 47·84), 04절 자동 번호 값, 임베딩 벡터 안의 숫자. 본문·표·그림 라벨·정리 어디에도 넣지 않았습니다.
- **여덟 절 b7에 「걸린 시간을 재지 않았습니다」**가 있고 「빨라졌다」류 문장은 0건입니다(Ch 12부터 이어지는 규칙).
- 08절 기준값 `5.0`·`9.0`과 03·06절 점수 `0.82`·`0.41`·기준값 `0.7`은 **흐름을 보여 주려고 정한 예**이고 잰 값이 아닙니다(규격 §3, b4·b7·diagnosis에 적음).

## 8. 08절 실습 절 주제와 결과

- 제목 「**LangGraph 기초 실습: 자료를 보고 답할지 되물을지 정하기**」, `format: experiment`, meta 「실습 30분」(**챕터 시수에 더하지 않음**, 규격 §7-2).
- 붙인 앞 절 기능 **셋**: 06절 `Command`·`destinations`, 04절 `add_messages`, 07절 Ch 12 검색 부품(바탕은 01절 `StateGraph`·02절 `operator.add`). **뺀 것**: 05절 `Send`와 03절 조건부 엣지(30분·요청 네 번, 조건부 엣지는 `Command`와 같은 일 — b3 한 단락에 밝힘).
- 노드 다섯(`normalize`·`search_docs`·`route`·`make_reply`·`ask_more`), 고정 엣지 다섯, 갈래 두 자리는 `Command`. 구조 줄 일곱(실선 다섯 + 점선 둘).
- 결과: 두 실행 모두 `점수 칸 7.64`·보고 자리 칸 `['E01-P03-C02', 'E02-P05-C02', 'E02-P05-C01', 'E02-P03-C04', 'H01-P04-C01']`(부모 차례 `['E01', 'E02', 'H01']`). 기준값 `5.0`이면 `자료가 넉넉함` → `make_reply`(모델 호출), `9.0`이면 `자료가 모자람` → `ask_more`(모델 호출 없음). 메시지 수는 두 실행 모두 **2**이고 실행 1의 마지막만 모델 답입니다.
- **파일을 쓰지 않습니다**(Part 3 실습 절 넷·07절 선례, contracts §3).

## 9. 산출 파일 계약 — `runs/graph-integrated-result.json` (마감 결정)

- **이 챕터는 `runs/`에 쓰지 않습니다.** 07·08절 노트북 어디에도 파일을 쓰는 코드가 없습니다(개선 전 07절은 이 파일을 다시 썼습니다).
- 남아 있는 `labs/part4/ch13-langgraph-basics/runs/graph-integrated-result.json`(sha256 `c704a2eb…`, 2026-09-10)은 **개선 전 07절이 남긴 기록이고 지금 교재와 값이 다릅니다**: `reranker`가 `BAAI/bge-reranker-v2-m3`, `duration_ms` `13186.79`, `retrieved`에 `E02-P03-C01`. 교재 본문은 「이 절은 리랭커를 부르지 않습니다」·「걸린 시간은 이번에 재지 않았습니다」입니다.
- **코드로 읽는 쪽은 0건**입니다(`grep -rn "graph-integrated-result" --exclude-dir=.venv textbook labs`). 나오는 자리는 묶음 목록 둘과 QA 문서뿐입니다.
- **이 세션에서는 지우지 않았습니다**(삭제 승인 대상). 전체 마감에서 할 일을 `textbook/qa/upgrade-final-checklist.md`에도 같은 내용으로 적었습니다:
  1. `labs/part4/ch13-langgraph-basics/runs/graph-integrated-result.json` 삭제 승인.
  2. `textbook/part4/public-files.json` **12행** 제거.
  3. `textbook/part4/ch13-langgraph-basics/qa/public-files.json` `include` **10행** 제거.
  4. `python3 textbook/part4/_build_index.py`로 `textbook/downloads/part4-practice.zip` 재생성(지금 91항목 = 88 + `시작하기.md`·`env.example`·`manifest.json`, 지운 뒤 90항목) 뒤 `textbook/part4/qa/check_delivery.py` 다시 실행.

## 10. 챕터 밖 수정 (전부 목록)

- `textbook/part4/_build_index.py` — **20행** ch13 설명 「상태·노드·**분기**를 실행하고, 검색과 **답변 생성 함수**를 그래프로 연결합니다.」 → 「상태·노드·**갈래**를 실행하고, Ch12 검색과 **답 만들기**를 그래프로 잇습니다.」(규격 §7-2 목차 대조, 검토 C-2와 같은 까닭). 이 스크립트를 돌리면 **Part 4 목차와 `textbook/downloads/part4-practice.zip`이 함께 다시 만들어집니다** → `Part 4: 31 verified sections; 88 bundled files`.
- `textbook/downloads/part4-practice.zip` — 마감에서 다시 만들었습니다(91항목). 08절 작업 뒤 이번 검토 반영으로 노트북 다섯 개의 **마크다운만** 바뀌어 묶음이 낡았기 때문입니다(`check_delivery.py`가 `Stale file`로 잡았습니다).
- `textbook/_notebook/checks/ch13-langgraph-basics/visual-results.json` — 16행(7절 + index) → **18행**(8절 + index), 1280px·390px 모두 PASS. 스크린숏 네 장(index·01절)도 다시 찍었습니다.
- `textbook/qa/upgrade-progress.md`·`upgrade-final-checklist.md`·`upgrade-contracts.md` §8 — 이 챕터 몫을 적었습니다.
- `textbook/QUALITY-UPGRADE.md`·`textbook/_notebook/upgrade/PLAYBOOK.md` §4 — 새 규칙 세 줄(§11 아래 「규격 추가」).
- **고치지 않은 것**: 빌드 도구(공용 `_template/builder.py`로 충분), 묶음 허용 목록 두 곳(위 §9의 마감 몫), `labs/part3/*`(읽기만), Ch 9~12 기록, Ch 6~8 사슬, Ch 14·15 파일, `textbook/qa/check_course_continuity.py`(202행 묶음 목록에 part4가 없어 고칠 해시 허용 목록이 없음), `textbook/part4/_build_index.py`의 ch14~16 줄.
- **권한 한 문장**: 검토 보고서의 결정 요청 **스물세 항목 가운데 스물한 항목은 권고대로 유지**했고, 나머지 둘(`runs/` 파일 처리·`chapter.json` 목표 문장)은 §12 강사 확인 대상에 있습니다. 파일을 지우거나 삭제 승인을 받은 것은 **없습니다**.

## 11. 기준 버전·확인 날짜

- 실습 폴더 `pyproject.toml`·`uv.lock`: `langgraph 1.2.11` · `langchain 1.4.0` · `langchain-core 1.6.2` · `langchain-openai 1.6.1` · `kiwipiepy 0.23.2` · `rank-bm25 0.2.2` · `python-dotenv 1.2.3`, dev `pip==26.2`·`ipykernel==7.3.0`. 교재 출력 환경은 Linux · Python **3.12.13**입니다.
- **`openai` 판 차이(다시 실행하지 않음)**: 작업 가상환경 `.cache/vm/venv-ch13-langgraph-basics`에는 **`openai 3.16.2`**가 들어 있고 실습 폴더 잠금은 **`3.11.0`**입니다(07절에서 `langchain-openai`를 넣을 때 딸려 왔고 마운트 폴더라 내림 설치가 막힘). **학생 묶음·노트북 출력 표기에 영향이 없습니다** — `%pip` 여섯 줄에 `openai`가 없고 `langchain-openai==1.6.1`이 요구하는 판을 `3.11.0`이 만족하며, 판을 찍는 셀 여섯 개(`langgraph`·`langchain`·`langchain-openai`·`python-dotenv`·`kiwipiepy`·`rank-bm25`)에 `openai`가 없습니다. 같은 줄을 `textbook/qa/upgrade-contracts.md` §8에도 남겼습니다.
- **잠금에 남은 쓰지 않는 패키지 넷**: `numpy 2.5.3`·`pypdf 6.18.0`·`scikit-learn 1.9.0`·`sentence-transformers 6.0.1`(여덟 노트북에 import 0건). 빼면 학생 `uv sync --locked` 설치량이 크게 줄지만 `uv.lock`과 묶음 둘을 다시 만들어야 해 **전체 마감 몫**입니다. **§2-7로 바뀜(2026-09-21)**: `numpy`는 이제 도구 파일이 씁니다(설치 셀 `numpy==2.5.3`). 쓰지 않는 패키지는 `pypdf`·`scikit-learn`·`sentence-transformers` 셋입니다.
- 참고 자료 확인일: **01~06절은 2026-09-10**(이번 개선에서 다시 열지 않았습니다, Ch 12 06절 선례 — 01·02 diagnosis에 까닭), **05절 오류 안내 링크 하나와 07·08절 세 링크는 2026-09-19**입니다.
- 요금: 임베딩 `text-embedding-3-small` 0.02달러/100만 토큰, 답 모델 `gpt-5.4-mini`. 07·08절 각각 0.01달러 아래입니다.

## 12. 강사 확인 대상

- **`chapter.json` 학습 목표 다섯 줄**(검토 C-2 반영): 둘째 줄 「분기」 → 「코드가 정하는 갈래」, 넷째 줄 「검색·병합·재정렬·생성」 → 「검색과 순위 합치기와 답 만들기 … 구조 문자열로 확인」(07절은 리랭킹을 하지 않습니다), **08절 몫 다섯째 줄을 새로 더했습니다**. 목차 페이지에 보이는 문장이라 강사가 한 번 읽어 두는 편이 좋습니다.
- **`runs/graph-integrated-result.json` 삭제 승인**(§9). 사람이 정해야 합니다.
- **모델 요청 0번과 API 키 셀을 뺀 절 여섯 개**(01~06절). 그래프 구조·상태 규칙이 주제라 서비스를 부르지 않았습니다.
- **`Literal`을 뺀 결정**(03·06절): `path_map`과 `destinations`로 같은 일을 했습니다.
- **코드 셀 수**(07·08절 32개)와 07절 시수 강의 2h·실습 2h. **시수는 바꾸지 않았습니다**(절 meta 합 강의 8h·실습 8h = `chapter.json` 총 16h).
- **참고 자료 확인일 2026-09-10 유지**(01~06절).
- **실습 폴더 잠금의 쓰지 않는 패키지 넷**(§11).
- **`textbook/part4/_build_index.py` ch13 설명 한 줄 수정**(§10).

## 13. 뒤 챕터 인계 — Ch 14 RAG 패턴이 이어받을 것

1. **Ch 12 부품과 값**: 함수 열한 개를 **글자까지 같은 코드로** 다시 정의하고 값(문서 청크 175·부모 6·순위 상수 60·보고 자리 5·넣을 자리 3·`dimensions=256`·`gpt-5.4-mini`)을 그대로 쓰세요. 이름이나 인자 모양을 바꾸면 절 사이 표를 견줄 수 없습니다. **§2-7로 바뀜**: 다시 정의하지 말고 Ch 12 도구 파일 본문을 그 챕터 도구 파일로 옮겨 가져오세요(`handoff.md` 「§2-7 리팩터」 Ch 14 인계).
2. **그래프 말과 규칙**: 「칸」·「노드」·「엣지」·「갈래」·「기준값」·「실행 흔적」·「갱신」, 상태 형식 이름 규칙(칸이 바뀌면 새 이름), 「규칙을 적은 칸에는 자기 몫만」, 색 규칙(라이브러리 제공은 회색·출력으로 확인한 값만 노랑·갈래는 점선). **「분기」·「경로」·「반환」·「임계값」·「재정렬」은 쓰지 않습니다.**
3. **Ch 14는 지금 LangGraph를 쓰지 않습니다**(노트북 아홉 개에 `StateGraph` 0건, 이 챕터 파일을 읽는 코드도 0건). 08절 b8은 그래서 「Ch 14에서는 검색 앞뒤에 붙이는 RAG 패턴을 배웁니다」까지만 적었습니다(규격 §7-2 「뒤 챕터 연결 문장은 확인한 것만」). Ch 14를 그래프로 다시 쓰기로 하면 그때 이 문장을 함께 손보세요.
- 그 밖에 **`runs/graph-integrated-result.json` 처리**(§9)와 **잠금 정리**(§11)는 전체 마감 몫입니다. Ch 15 01절이 Ch 12 기록 때문에 깨져 있는 건은 그대로 남아 있습니다(`upgrade-final-checklist.md` §2).

## 14. 아직 가르치지 않은 것 (Ch 14가 설명 없이 전제하면 안 되는 것)

- 체크포인터·`thread_id`·스트리밍·`interrupt`(여덟 절 모두 없음), 손으로 만든 리듀서, 하위 그래프, `Command`로 다른 그래프 건너뛰기.
- 갈래가 셋 이상인 이동, 노드가 자기 자신으로 다시 가는 경우, 갈래 안에서 다시 갈래 펼치기, 여러 노드가 같은 칸에 한꺼번에 갱신을 내는 경우(05절 오류 장면 하나뿐).
- **걸린 시간 재기**(Ch 12부터 한 번도 재지 않음). 「노드로 나눠 빨라졌다」를 쓰지 마세요.
- 검색 품질·답 품질 판정(지표는 Ch 11·Ch 12, 답 정확성과 LLM 판정자는 Ch 15, 가드레일은 Ch 16), 점수 기준값으로 문서를 **거르는** 일(08절은 길만 골랐습니다), 리랭커·pgvector·MMR·질문 재작성·PDF 다시 읽기.
- `Literal`·f-string·`lambda`·내포식·`key=`·`reverse=`·`numpy`·`sklearn`(여덟 절 0건). **§2-7로 바뀜**: NumPy는 도구 파일 안에서만 씁니다(노트북 import 0건 그대로).

## 15. 남은 것 (전체 마감 몫)

1. **`runs/graph-integrated-result.json`** 삭제 승인 → 목록 두 곳(행 번호는 §9) → `part4-practice.zip` 재생성 → `check_delivery.py`.
2. **`llm-practice.zip` 재생성**: 2026-09-14 판이라 이 챕터 노트북이 일곱 개뿐이고 Ch 12 개선분도 빠져 있습니다. 지금 `check_delivery.py`는 `part4-practice.zip`을 끝까지 통과한 뒤 **`llm-practice.zip`의 `labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`에서 `Stale file`로 멈춥니다**.
3. **실습 폴더 잠금 정리**: 쓰지 않는 패키지 넷(`numpy`·`pypdf`·`scikit-learn`·`sentence-transformers`)을 뺄지 정합니다. 빼면 `uv.lock`과 묶음 둘을 다시 만들어야 합니다. **§2-7로 바뀜**: `numpy`는 빼면 안 됩니다(도구 파일이 씀) — 대상은 셋.
4. **삭제 승인 대상**: `.cache/vm/venv-ch13-firstattempt-unused`(첫 시도 가상환경, 내림 설치가 막혀 남음), `labs/part4/ch13-langgraph-basics/.venv`(깨진 채 남아 `uv run --project`가 멈춥니다), `.cache/vm/venv-ch13-langgraph-basics`, `/tmp/ch13-*`·`/tmp/ch13rv`·`/tmp/ch13rev`·`/tmp/ch13close`, `qa/upgrade/gates-wip-*.json`.
5. **옛 파일 정리**(삭제 아님, `qa/upgrade/before/generators/`로 `mv -n`): `qa/author_ch13.py`·`figures/_gen_figures.py`(둘 다 첫머리 `raise SystemExit`으로 막아 둠). 옛 도식 `figures/NN-흐름.{caption.md,excalidraw,svg}` **스물한 개**도 본문에서 참조하지 않습니다.
6. **2차 검토**: `review-round1.md` 끝 「2차 검토 때 볼 곳」과 「반영 결과」.

## 16. 검토 1차와 반영 (2026-09-19)

- 판정: **여덟 절 모두 accept**, 상 0 · 중 6 · 하 12. reject 사유 없음.
- **중 6건 모두 반영**: C-1(모델 부르는 절 문장 네 자리) · C-2(`chapter.json` 목표) · C-3(`normalize` 세 판) · 03-1(`03-2` 그림의 조건 함수 상자) · 08-1(b5 셀 수) · 08-2(b6·복습 5 근거 표기).
- **하 12건 가운데 11건 반영**, 1건은 까닭을 적고 넣지 않았습니다(01절 `01-2` 「도식 읽기」에 한 줄 더하기 — 그 단락이 이미 다섯 문장이라 G6 `dense_paragraph`에 걸림, 검토도 「필수 아님」으로 적음).
- 검토가 적지 않았지만 같은 사실이라 함께 고친 자리 넷: 04절 b3·04 노트북·05 노트북·06 노트북의 `normalize` 「글자까지 같다」 문장, 07 노트북의 「이 값은 호출마다」, 08절 b8의 Ch 14 연결 문장, `handoff.md`의 같은 주장 세 곳.
- **01~08절 노트북을 다시 실행하지 않았습니다**(규격 §3). 여덟 노트북 모두 `code_sha256`·`outputs_sha256`이 실행 기록과 같습니다. 고친 방법은 `mdpatch.py`·`_src` 직접 편집·`.mmd` 두 장 다시 렌더(`03-2`·`08-2`)·`run_section.sh … --no-exec`입니다. **렌더 도장은 지우지 않았고 31장 모두 해시가 맞습니다.**

## 17. §2-7 리팩터 (2026-09-21)

- 규격 §2-7을 적용했습니다. 도구 파일 `labs/part4/ch13-langgraph-basics/notebooks/rag_tools.py`(함수 16개·코드 줄 91·NumPy): **01~06절 구역** `print_state`(01)·`normalize`·`make_query`(02)·`make_answer`·`ask_more`(03) — 뒤 절 노트북 판과 AST가 같은 것만. **Ch 12 검색 부품 구역** 11개 — Ch 12 도구 파일과 AST가 같고 07·08은 `kiwi_terms(kiwi, text, keep_tags)`·`fuse_rank(…, rank_constant)`·`unique_chunk_ids`·`parent_ids_of(…, parent_by_chunk)`·`rank_chunks_by_distance`·`rank_chunks_by_bm25` 여섯 개를 가져갑니다.
- 가져오는 절: 02(1개)·03(2)·**04(1)·05(1)**·06(3)·07(6)·08(7). 01은 손대지 않았습니다. 처음 리팩터 때는 04·05의 `normalize`(`clean` 판)를 노트북에 두었다가, 같은 날 결정으로 **04·05도 02절 판을 가져오게 바꿔 두 판이 됐습니다**(아래 줄). `choose_path`(03·06)는 노트북 이름 `enough_score`를 읽어 옮기지 않았습니다.
- 코드 셀 216 → **195**, 코드 줄 1287 → **1129**(−158, −12.3%; 도구 파일 포함 1220, −5.2%). 07 275 → 205, 08 274 → 201, 04 120 → 119, 05 141 → 140.
- **04·05 `normalize` 정리(2026-09-21, 추가)**: 정의 셀 두 개를 지우고 준비 셀에서 `from rag_tools import normalize`, 설치 셀에 `numpy==2.5.3`(도구 파일이 불러옴). 모델 요청 0번, 새 커널 2회 두 실행 셀별 출력 글자 같음, 리팩터 전과 설치 셀 `numpy: 2.5.3` 한 줄만 다름(04 자동 번호는 글자 수만 출력해 원래 흔들리지 않음) → 인용 수정 없음. 게이트 8/8·`verify` 195셀·`{{` 0·visual 04·05 4/4(`visual-after-2-7.json` 14/14), `part4-practice.zip` `07a40b22…`(95파일). 도구 파일 `6dc956c5…` 그대로.
- 02·03·06·07·08 새 커널 2회 — 두 실행 셀별 출력 글자가 모두 같음. 리팩터 전과 값 출력 같음(07 실행 2·08 실행 1의 모델 답 표현과 07 답 칸 글자 수 `84` → `89`만 다름, 인용 안 함). **08 점수 `7.64`와 기준값 `5.0`·`9.0` 관계 그대로**, §2-7 10항 입력 수정 없음.
- 게이트 `after-2-7` 8/8 PASS·G1~G7 0, `verify` 197셀(max 18, 04·05 정리 뒤 195셀), `{{` 0, visual 12/12(`qa/upgrade/visual-after-2-7.json`, 04·05 정리 뒤 14/14). `part4-practice.zip` 재생성 `484a448d…`(94파일, Ch 9~12 도구 파일 넷도 함께 들어감 — 뒤에 Ch 14·04·05 정리로 `07a40b22…`), `check_delivery.py`는 `part4-practice.zip` 통과 뒤 `llm-practice.zip`에서 멈춤(전과 같은 자리). 서비스 요청 22번(0.01달러 아래).
- 세부와 Ch 14 인계는 `handoff.md` 「§2-7 리팩터 (2026-09-21)」.
