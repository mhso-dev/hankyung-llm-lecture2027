# Ch 09 RAG 첫 실행 — 챕터 요약 (다음 챕터 작업자용)

작성 2026-09-17(품질 개선 6절 + 실습 절 07 + 별도 세션 검토 1차 A·B 반영 뒤). **Part 3 첫 챕터**입니다. 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md` §6. 앞 내용: `textbook/qa/upgrade-course-summary.md`(Part 1·2), 바로 앞 챕터 `part2/ch08-context-engineering/qa/upgrade/chapter-summary.md`. 절 사이 인계 원문: `qa/upgrade/handoff.md`(절마다 「새로 가르친 것」「이어 쓸 이름과 값」「출력 라벨」「아직 안 가르친 것」 전체 목록). 검토: `qa/upgrade/review-round1-A.md`(§01~04)·`review-round1-B.md`(§05~07), 각 끝에 「반영 결과」.

**Ch 10 작업자는 과정 요약(Part 1·2) + 이 파일만 읽고 시작할 수 있게 썼습니다.** 세부 값·라벨이 필요하면 handoff를 찾아봅니다.

절: 01 RAG 지도 · 02 로더와 스플리터 · 03 임베딩·벡터스토어·top-k 검색 · 04 생성과 출처 인용 · 05 첫 실패를 일부러 보기 · 06 실험 하네스 · 07 RAG 실습: 문서 청크 크기를 바꿔 검색부터 답 검사까지. 형식 01~06 paired, 07 experiment. 모델은 생성 `gpt-5.4-mini`, 임베딩 `text-embedding-3-small` 둘. 코드 셀 175개(21·19·21·25·30·32·27), 게이트 7/7(G1~G7 0, 수정 전 6절 합계 268 = G1 12·G2 6·G3 10·G4 2·G5 72·G6 151·G7 15), 검사 문장 440·415·428·435·529·642·452, Mermaid 27장(4×6 + 3)·삽화 7장(대기 없음), 모든 노트북 새 커널 실행 PASS(실행일 모두 2026-09-17, 01 14:55 · 02 15:46 · 03 16:06 · 04 16:37 · 05 17:07 · 06 18:18 · 07 18:53 — **검토 반영에서 다시 실행한 절은 없음**). 서비스 요청 01 7 · 02 **0** · 03 6 · 04 6 · 05 8 · 06 7 · 07 6번(각 절 0.01달러 미만, 06 색인만 61,071토큰).

이 챕터는 `chapter.json`이 없고 자체 `_build.py`를 씁니다. `run_section.sh`가 verify를 건너뛰므로 `verify.py --chapter`를 따로 실행합니다(`PASS 7 sections / 175 code cells (max 16 lines)`).

## 1. 새로 가르친 개념·기법·함수·용어 (노트북에서 실행한 것만)

| 절 | 새 API·값 | 직접 만든 함수(노트북 셀, 실습 폴더 모듈 아님) | 용어 표 |
|---|---|---|---|
| 01 | `from pypdf import PdfReader`·`reader.pages`·`page.extract_text()`, `Document(page_content=, metadata=)`, `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)`·`split_documents()`, `OpenAIEmbeddings(model="text-embedding-3-small")`·`embed_query()`, `InMemoryVectorStore(embedding=)`·`add_documents()`·`store.store`·`similarity_search(k=)` | `load_pdf_pages(pdf_path, doc_id)`, `make_source_mark(chunk)`, `find_cited_marks(answer_text, marks)` | RAG(검색 증강 생성), 색인(indexing), Document, **문서 청크(chunk)**, 벡터스토어(vector store), top-k 검색 |
| 02 | `tiktoken.encoding_for_model("text-embedding-3-small")` → 규칙 `cl100k_base`, `splitter._separators` 확인(소스 읽기) | `count_tokens(text)`(바깥 `encoding`), `find_missing_words(text, words)`(Ch 8 03 코드) | 로더(loader), 스플리터(text splitter), 크기(chunk size), 겹침(chunk overlap), 끊을 자리 순서(separators) |
| 03 | `similarity_search_with_score(k=)` → `(문서, 점수)` 튜플 목록, `store.store[hit.id]["vector"]` | `dot_product`·`vector_length`·`cosine_similarity`(Ch 5 02 코드) | 저장 항목, 저장 ID(id), 검색 점수(score) |
| 04 | `response.usage_metadata["input_tokens"]`, `init_chat_model(..., temperature=0, reasoning_effort="none")`(Ch 6) | `make_note(chunk)`, `build_notes_messages(notes, question)`, `find_cited_notes(answer_text, notes)`, `check_answer(answer_text, notes)`(Ch 8 04 코드, 바깥 지킬 말 이름만 절마다 다름) | 출처 인용(citation) |
| 05 | 없음 | `find_missing_sources(hit_sources, answer_sources)`, `find_new_words(answer_text, source_text, words)` | 정답 출처, 검색 누락, 답이 없는 질문 |
| 06 | `yaml.safe_load(글)`, `json.dumps(딕셔너리, sort_keys=True)`, `hashlib.sha256(바이트).hexdigest()`(Ch 7 08), `time.strftime("%Y%m%dT%H%M%S")`, `os.makedirs`, `os.replace`, `open(…, "w", encoding="utf-8")` | `make_index_key(index_settings)`, `make_hit_item(hit, score, rank)` | 실험 하네스, 실행 설정, **색인 이름표**(index key), **실행 기록 한 줄**, **정답 문서 ID**(문서 단위), JSONL |
| 07 | 새 API 0개 | 같은 코드 7개(`load_pdf_pages`·`make_note`·`find_missing_words`·`find_cited_notes`·`check_answer`·`find_missing_sources`·`build_notes_messages`) + 새 5개 `search_notes`·`make_search_row`·`add_answer_items`·`check_question`(조립)·`print_rows`(본문 5·9·9·6·6줄) | 새 용어 0개 |

- **Python 쪽(175셀)**: `lambda`·내포식·제너레이터 식·조건 표현식·`:=`·`global`·함수 안 함수·`*args`/`**kwargs`·클래스·try·`raise`·`with`·`+=`·세미콜론·한 줄 복합문·`Path`·`sum`·`max`·`min`·`zip`·`enumerate`·`sorted`·`any`·`all`·`next`·`isinstance`·`join`·`extend`·f-string 안 계산·반복문 안 요청 **0건**(검토 A·B AST). 호출한 내장 이름은 `len`·`print`·`type`·`range`·`round`·`str`·`open`뿐입니다. 새로 풀어 쓴 모양: 경로 후보 `for`+`break`, 변수만 넣은 f-string, 튜플 반환 목록 풀기 `for hit, score in …`, 딕셔너리 리터럴을 여러 줄로, 함수가 딕셔너리 반환, 글 `+`로 경로 만들기, 목록 안 딕셔너리 걸러 담기, `딕셔너리.keys()` 출력, 글 슬라이싱 `[:10]`, `str(숫자)` 이어 붙이기
- **결론 태도(Ch 10도 지킬 것)**: 한 번 본 결과는 「이번 실행에서는」, 검사 함수는 말·표시가 있는지만 보고 품질 점수가 아니며 뜻은 원문으로 대조, 두 조건 답에 모두 있던 값은 한 조건 효과로 적지 않음(맨 아래 회색 상자), 점수는 실행마다 소수 넷째 자리가 달라져 결과 읽기 첫 단락·그림 라벨에 넣지 않음, 탐색 뒤 정한 값은 b7에 과정과 「흐름을 보여 주려고 정한 예」

## 2. 반복해 쓴 메시지 목록·함수·데이터·비유·이름

- **모델 셀**: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`. 결과 읽기에 「이 노트북의 출력은 2026-09-17에 이 모델로 실행한 결과입니다」
- **메시지 목록(01·04~07 같은 모양)**: `[("system", persona_text), ("developer", task_text), ("user", user_text)]`. `persona_text = "당신은 미르시립도서관 안내 담당자입니다."`, `task_text` = 04 기본 글, 05·06·07은 그 글 + Ch 5 07 보류 지시 한 문장. user 글 = `"[출처] 내용\n"` 줄들 + 빈 줄 + `"질문: …"`. **과업 명세에 쪽 번호 예시를 넣지 않습니다**(검색이 출처를 고르는 챕터라 출처 검사가 뜻을 잃기 때문, 01 b5)
- **데이터**: `labs/data/rag-corpus/pdf/easy/E01.pdf`(미르시립도서관 이용 안내, 5쪽 — 쪽 글자 수 45·905·925·871·270, 줄 수 5·26·25·26·9, 마지막 줄은 쪽 번호). 01~05·07은 E01 하나, **06절만 디지털 PDF 18건**(`manifest.json`의 `tier`가 easy·medium·hard). E01 500/50 문서 청크 8개 = `1|45`·`2|498`·`2|452`·`3|498`·`3|462`·`4|492`·`4|412`·`5|270`, 300/50이면 14개(2쪽은 242·283·269·191). 18건 색인은 쪽 93·문서 청크 176, 1000/50이면 107
- **질문 두 갈래**: 01·03·04·05·07 긴 질문 `closure_question` 「미르시립도서관의 정기 휴관일은 언제이고, 공휴일이 월요일과 겹치면 어떻게 되나요?」(45자)와 **06절 Q001 짧은 질문** 「미르시립도서관의 정기 휴관일은 언제인가요?」(Ch 11 평가셋 글과 **글자까지 같아야 함**). 03·04 `combined_question`, 05 와이파이 질문(답이 없는 질문)
- **지킬 말·정답 출처**: `closure_keep_words = ["월요일", "법정 공휴일", "화요일"]`, `combined_keep_words = ["월요일", "7권"]`, `closure_answer_sources = ["E01 p.2"]`, `abstain_sentence = "제공된 정보로는 확인할 수 없습니다."`(Ch 5 07 글)
- **출력 라벨(대표)**: 「쪽 수:」「Document 수:」「문서 청크 수:」「벡터스토어에 넣은 문서 청크 수:」「저장 항목의 키:」「벡터의 숫자 개수:」「검색 결과 수:」「답에 쓰인 검색 출처:」「실제 입력 토큰 수:」「답 검사:」「보류 문장 있음:」「검색 결과에 없는 정답 출처:」「색인 이름표:」「기록에서 빠진 필수 키:」「검색 항목의 순위:」「두 파일의 질문 글이 같은가:」(절마다 전체 목록은 handoff)
- **비유와 삽화(Ch 7·8의 파란 명찰 = system 페르소나, 주황 클립보드 = developer 과업 명세, 노란 메모지 = 질문, 답안지 = 답을 이어 씀)**: 01-5 두 책상 + 바닥 카드 상자(= 벡터스토어, 흰 카드 = 문서 청크) → 02-5 긴 공지문과 문단 카드(초록 스티커 = 메타데이터, 노란 띠 = 겹침) → 03-5 같은 상자에 막대 카드(= 벡터)와 노란 메모지(= 질문), 두 장만 올라옴(k=2) → 04-5 카드 세 장의 세모·동그라미·네모 스티커와 답안지 스티커(= 출처 표시) → 05-5 두 책상·같은 상자에 일곱 장, 맞는 카드가 올라오지 않음(검색 누락) / 아예 없음(답이 없는 질문) → 06-5 눈금 받침(실행 설정)·상자·흰 종이(답)·기록 용지 첫 줄(실행 기록 한 줄) → 07-4 카드 너비만 다른 두 상자(문서 청크 크기), 초록 형광 줄 = 지킬 말. 일상 예: 열린 책 시험(RAG), 책등 분류 번호(메타데이터), 긴 공지문을 카드에 옮겨 적기(문서 청크·겹침), 옷장 상자에 붙인 쪽지(색인 이름표), 요리 저울과 타이머(실험 하네스), 같은 요리에서 소금만 줄이기(실행 설정), 실험 일지 한 줄(실행 기록 한 줄), 시험지 정답표(정답 문서 ID), 공책 한 줄에 기록 하나(JSONL)
- **쓰지 않은 말**: 한정어 없는 **「청크」**(반드시 「문서 청크」), **「조각」**(Ch 5 토큰 뜻 전용 — 02 용어 표는 겹침을 「스플리터가 끊어 낸 단위」로 풂), **「스트림 청크」**(Ch 6 04 뜻 — 01 용어 표가 세 말을 갈라 둠), 「캐시」·「설정 해시」(06은 「색인 이름표」), 「출처 태그」(→ 출처 표시), 「문맥」·「프롬프트」(→ 근거·user 글·메시지 목록·과업 명세), 「거부」·「unanswerable」(→ 답변 보류·보류 문장·답이 없는 질문), 「설정 딕셔너리」(→ 설정 파일·실행 설정), 「최신 포인터」(→ 최신 기록 파일), 「청킹」

## 3. 07 실습 절 주제와 결과

- 「07 · RAG 실습: 문서 청크 크기를 바꿔 검색부터 답 검사까지」(30분, 따로 과제 없음, 강사와 함께 실행). 파일·slug `07-RAG-실습`, 형식 experiment, meta `실습 30분 | 새 용어 0개`. **검토 B 07-7 권고로 표시 제목을 줄였습니다**(옛 제목의 「RAG 첫 실행」은 폴더 이름이고 교재 어디에도 표시되지 않음)
- 조립: 재료(500자 8개 / 300자 14개) → `search_notes()` → `make_search_row()`(답 전 검사) → `build_notes_messages()` → `gpt-5.4-mini` → `add_answer_items()`(답 뒤 검사)를 조립 함수 `check_question()` 하나로. `print_rows()`는 조립 함수가 아니라 **7·8·9절 실행 셀**이 부릅니다(검토 B 07-3). 바꾸는 값 하나 = 문서 청크 크기 500 → 300
- 결과(2026-09-17 18:53): 검색 뒤 점검표 `500 | 8 | ['E01 p.1', 'E01 p.2'] | 543 | [] | []`·`300 | 14 | ['E01 p.1', 'E01 p.2'] | 287 | ['월요일', '법정 공휴일', '화요일'] | []`, 답 뒤 점검표 `500 | 513 | False | 1 | ['법정 공휴일']`·`300 | 345 | False | 1 | ['법정 공휴일']`
- 결론: 「문서 청크 크기를 바꾸면 검색 출처가 같아도 근거 내용이 달라질 수 있다」, 「쪽 단위 정답 출처와 답 뒤 검사 세 칸으로는 두 실행을 가를 수 없었고, 근거 글을 지킬 말로 검사한 칸이 갈랐다」까지. 어느 크기가 좋은지는 정하지 않습니다(질문 하나·크기 두 가지·크기마다 한 번)
- **시수**: 07 실습 30분은 `_build.py` `render_index()`의 「16h · 강의 6h · 실습 10h」에 더하지 않고 실습 10h 안(규격 §7-2). 01~06 meta 합(강의 6h·실습 10h)은 그대로. `_src/index.html` 절 표 07행은 「30분(실습 10h 안)」으로 적었습니다
- 07은 **파일을 쓰지 않습니다**(`runs/`·`config.yaml`·`harness.py`·`prompts.py`·`rag.py`·Ch 11 평가셋 해시 전후 같음)

## 4. runs 산출 파일 계약 (Ch 10·11이 읽음 — 꼭 먼저 읽을 것)

**06절이 쓰는 파일 두 개**: `labs/part3/ch09-rag-first-run/runs/continuity-ch09-search.jsonl`(정본, 한 줄)과 같은 바이트 사본 `runs/continuity/20260917T181822-ch09.jsonl`. 사본 폴더는 9개(2026-09-09 7개 + 2026-09-17 2개), **앞 사본은 지우지 않습니다**(과정 단계 검사가 옛 바이트를 그 이름으로 찾습니다).

| 항목 | 값 |
|---|---|
| `runs/continuity-ch09-search.jsonl` | SHA-256 **`294713765a115b567e162aaf37a25467577841965c1075b86553adc4080666d5`**(옛 정본 `4f9fce62…ae61`), `source_run_id` `20260917T181822-ch09` |
| 최상위 키 8개 | `qid`·`question`·`gold_doc_ids`·`source_chapter`(`ch09`)·`source_run_id`·`config`·`retrieved`·`answer` — **바꾸지 않음** |
| `config` 키 7개 | `name`(`k2`)·`corpus`·`split`·`embedding`·`retrieval`·`generation`·`inputs`. **옛 기록보다 `corpus`가 하나 늘었고**(`{"tiers": ["easy","medium","hard"]}`), `inputs.corpus_scope`가 `"18 digital PDFs"` → `"디지털 PDF 18건"`으로 바뀌었습니다. 이 칸을 읽는 쪽은 없습니다(`evaluate.py`는 보고서 `settings`로 실어 나르고, 검사 스크립트는 라벨 세 개가 없는지만 봅니다) |
| `retrieved` 항목 키 5개 | `doc_id`·`chunk_id`·`page`·`rank`·`score`. `score`는 `labs/part3/ch11-evaluation/evaluate.py` 178행이 **필수**로 봅니다. `rank`는 1부터 차례, `page` 1 이상 |
| `chunk_id` 모양 | `ch09:6f9f83db90:0`(옛 `ch09:d853036bf1:0000`). 앞부분이 바뀐 까닭은 **이름표 입력에 `corpus`를 더해 실습 폴더 `harness.py index_key()`와 입력 집합을 맞췄기 때문**이고, 번호에 0을 채우지 않는 것은 `str(number)`이기 때문입니다. **Ch 10은 `ch10:recursive:0000`처럼 네 자리를 채웁니다** — 읽는 쪽 세 곳 모두 `chunk_id`가 빈 값이 아닌지만 보므로 깨지지 않지만, 두 챕터 기록을 나란히 볼 때 모양이 다릅니다(검토 B R-3) |
| 검색 개수 | **k=2 전제**. `evaluate.py` 232~236행은 `logged_k >= 5`에서만 `recall_at_5`·`precision_at_5`·`ndcg_at_5`를 계산하고, `textbook/part3/qa/finalize_continuity_evidence.py` 52~56행은 ch09 실행의 그 셋이 `None`이고 `recall_at_logged_candidates == 1`임을 확인합니다. Ch 11 06 `_src`도 같은 전제를 적었습니다. **검색 개수를 5 이상으로 올린 기록을 쓰면 마감 검증이 걸립니다** |
| `answer` | `[E01 p.2]` 모양 출처 표시가 하나 이상 있고 그 (문서, 쪽)이 모두 `retrieved` 안에 있어야 합니다(정규식 `\[([A-Z][0-9]+) p\.(\d+)\]`). 이번 답은 두 문장이고 **문장마다** 표시가 붙었습니다 |
| 라벨 | `question`·`gold_doc_ids`는 `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl` Q001과 글자까지 같아야 하고, 06 노트북이 그 파일에서 읽어 옵니다. 라벨을 `config` 안에 넣지 않습니다 |

**읽는 쪽 목록**(검토 B가 빠진 한 곳을 찾아 보탬): `labs/part3/ch11-evaluation/evaluate.py` 176~200·205~250행 · `textbook/part3/qa/check_continuity.py` 58~78·140~155행 · **`textbook/qa/check_course_continuity.py` 94~112행과 172~198행**(이 두 번째 블록이 06 diagnosis의 계약 표에 빠져 있었고 실제로 막혔습니다 → §8) · `textbook/part3/qa/run_continuity_bundle.py` 45~54행 · `textbook/part3/qa/finalize_continuity_evidence.py` 15·37·44~56행 · Ch 11 06 노트북(줄 수만).

**고치지 않는 파일과 해시**: `harness.py` `fc4269d0…785e`, `prompts.py` `4613ba02…f9cf`, `rag.py` `16caec34…c243`, Ch 11 평가셋 `9544b332…e1bd`, `labs/data/rag-corpus/` 전체, `runs/` 나머지 26개. **`config.yaml`만 주석 한 줄을 고쳐 `6da4af21…4cda` → `1e425071aba21b1a1d99f933003ea423dfe3757a003dabbb5542dd3d9aed1bd1`로 바뀌었습니다**(`[[미정: 임베딩 모델]]` 표시를 없앰 — 키 이름·값은 그대로라 `tests/test_harness.py` 3개가 그대로 통과). Ch 6·7·8 비용 기록 사슬(`f18920c6…4f4c`·`a8aaafb7…95e9`·`125fc147…58ad`)은 읽지도 쓰지도 않습니다.

**이 파일을 다시 쓸 때**: (a) 위 읽는 쪽을 먼저 확인하고, (b) 06 본문·그림의 인용 값(이름표 `6f9f83db90`·`9fa7a45db1`, 문서 청크 176·107, 입력 499토큰 등)을 새 출력으로 모두 맞추고, (c) 앞 사본은 지우지 말고 그대로 두고, (d) 이 표와 진행표를 새로 적습니다. **06 재실행은 기본적으로 금지**입니다(서비스 답이 실행마다 달라지고 Ch 11 입력이 바뀝니다).

## 5. 다음 챕터가 이어받을 것

- **Ch 10 문서 처리와 임베딩**(8절, 자체 `_build.py`·`chapter.json` 없음, 아직 개선 전)
  - 빌드 도구: Ch 8·Ch 9가 한 방법을 그대로 쓸 수 있습니다 — 자체 `_build.py`에 `inline_mermaid()`·`inline_illustration()`(`textbook/_template/builder.py` `_inline_mermaid`·`_inline_img`와 같은 출력)을 더하고, 치환 뒤 `\{\{[a-z]+:` 잔존 검사를 둡니다. 바꾸기 전후 기존 HTML 해시가 같은지 확인하세요. Ch 9 `_build.py` 모듈 설명에 「두 칸 `{{img:}}`·`{{svg:}}`는 사용처 없음」과 「표 감싸기 순서가 템플릿과 다름(결과는 같음)」을 적어 두었습니다
  - **Part 3 목차**: `textbook/part3/_build_index.py` `CHAPTERS`에 이제 **절 수 칸이 따로** 있습니다(`('ch09-rag-first-run', 제목, 6, 10, 7, 설명)`). Ch 10에 실습 절 09를 붙이면 그 칸을 8 → 9로 올리고 강의 시수 8은 그대로 둡니다(§8)
  - 이어 쓸 것: 08절이 06절 기록의 **겉 모양**(질문·정답 문서 ID·검색 항목 다섯 칸)을 같게 씁니다. `config` 칸 이름은 그 절 설정에 맞게 다르고 `answer` 칸은 없습니다. `chunk_id` 자리 채움 차이(§4)를 08절 본문·요약에 적으세요
  - 용어: 문서 청크·색인·벡터스토어·top-k 검색·검색 점수·문서 청크 크기·겹침·끊을 자리 순서·색인 이름표를 Ch 9 뜻 그대로 씁니다. **01 b5·03 b4의 「점수 = 코사인 유사도」는 `InMemoryVectorStore` 기준**입니다 — Ch 10·12에서 다른 벡터스토어(pgvector 등)를 쓰면 점수가 거리일 수 있으므로 「점수가 크면 가깝다」를 그대로 이어 쓰지 마세요
  - Ch 9가 「이번에 실행하지 않았다」고 적은 것을 Ch 10이 맡습니다: 표·각주가 많은 PDF 읽기(Ch 10 02), HWP·HWPX(Ch 10 04), 토큰 기준 스플리터·나누는 방식 비교(Ch 10 05), 문서 사이 순위와 표지 거르기, 임베딩 모델 비교
- **Ch 11 평가 기초**: `evaluate.py`가 **Ch 9 06절 기록을 읽습니다**(§4의 필수 키·k=2 전제). Ch 9는 지표를 계산하지 않고 「말·표시가 있는지만 보는 검사」까지만 가르쳤습니다. 05절 정답 출처(쪽 단위)와 06절 정답 문서 ID(문서 단위)의 차이를 Ch 11이 이어받습니다
- **Ch 12 검색 품질과 튜닝**: `chunk_id`로 문서 청크를 되찾는 방식(`check_continuity.py` 89·108행)은 Ch 12 `advanced-documents.json` 청크만 대상입니다. Ch 9 기록과는 무관합니다

## 6. 아직 가르치지 않은 것 (Ch 10이 설명 없이 전제하면 안 되는 것)

Ch 8 요약 §5 전체에 더해, Ch 9에서도 하지 않은 것:

- **검색·색인**: 점수 기준값·거르기(`score_threshold`)·MMR, 색인 파일 저장과 다시 불러오기(`InMemoryVectorStore.dump`/`load` — 03절에서 「있다고만」 적음), `as_retriever()`, `similarity_search_with_score_by_vector`, `ids` 직접 지정, `dimensions`, 다른 임베딩 모델, 여러 질문을 한 번에 돌려 평균 내기, 같은 조건 반복 요청, 문서 사이 순위 비교·표지·쪽 번호 줄 거르기, 여러 실행이 같은 파일에 함께 쓰기
- **문서**: 토큰 기준 스플리터(`from_tiktoken_encoder`·`TokenTextSplitter` — 설치판에 있다고만 적음), `split_text`, LangChain PDF 로더 클래스, PDF 아닌 형식(docx·html·hwp), 스캔본·OCR, 표 구조 살려 읽기
- **생성·평가**: 구조화 출력으로 출처 형식 강제, 모델에게 요약·줄이기 맡기기, 답 정확성 판정·검색 지표(Ch 11), LLM 판정자(Ch 15), 문서 속 지시문·프롬프트 인젝션(Ch 16), 시간·비용을 코드로 재기(Ch 6 06 `timed_invoke`는 배움)
- **Python**: `Path`·내포식·제너레이터 식·`enumerate`·`zip`·`sum`·`max`·`join`·`raise`·try·`lambda`·`+=`·`@`·`BaseModel`·타입힌트·f-string 안 계산·`deepcopy`·딕셔너리 `|`·`**딕셔너리` 풀어 넘기기·`set` 메서드(`issubset`)

## 7. 실습 묶음 허용 목록 (이번에 고친 챕터 밖 공용 파일)

검토 B C-1: 개선된 **06 노트북이 `labs/part3/ch09-rag-first-run/config.yaml`과 `labs/data/rag-corpus/queries.jsonl`을 읽는데 두 파일이 `part3-practice.zip`에 없었습니다**(학생이 06절 4절에서 `FileNotFoundError`, `run_continuity_bundle.py`도 zip에서 06을 실행하므로 마감 검증이 막힘). 개선 전 06은 임시 폴더에 YAML을 직접 쓰고 질문을 노트북 안에 적었기 때문에 필요 없던 입력입니다.

- `textbook/part3/public-files.json`에 `labs/part3/ch09-rag-first-run/config.yaml` 한 줄 추가(이 파일은 `labs/part3/` 접두만 허용). 이 목록은 `textbook/part4/_build_index.py`가 상류 파일로도 읽으므로 `part4-practice.zip`에도 한 파일이 늘어납니다
- `textbook/_notebook/build_bundle.py` `data` 목록에 `labs/data/rag-corpus/queries.jsonl` 추가(`manifest.json`과 같은 방식). `labs/data/`를 담는 묶음(part3·part4·llm)에 들어가고, `labs/part1`·`part2`·`part5`~`part7`만 담는 묶음은 바뀌지 않습니다
- **정답키 제외 규칙을 함께 고쳤습니다(강사 확인 대상)**: `queries.jsonl`에는 정답 문서 ID·정답 쪽 힌트·정답 예시가 있어 `textbook/qa/check_course_delivery.py` 85행·`textbook/part3/qa/check_delivery.py` 85행·`textbook/part4/qa/check_delivery.py` 104행이 **이 파일이 묶음에 없어야 한다**고 못 박고 있었습니다(검토 B가 보지 못한 곳). 세 검사의 금지 목록을 `rag-corpus/build/`(정답키 생성기 폴더)와 `rag-corpus/queries.csv`로 바꾸고, `textbook/part3/_build_index.py`의 학생 안내(`시작하기.md`)에 「정답 문서 ID와 정답 쪽 힌트, 정답 예시가 함께 있습니다 … 답을 먼저 읽지 않고 실행한 뒤에 봅니다」를 적었습니다. part5~7 `check_delivery.py`는 고치지 않았습니다(그 묶음에는 들어가지 않음)
- 되돌리려면 06 노트북이 `queries.jsonl`을 읽지 않게 코드를 고치고 06을 다시 실행해야 합니다(§4의 재실행 규칙). 정답 예시를 학생 묶음에 넣지 않기로 하면 그 길뿐입니다

## 8. 과정 단계 검사·목차 스크립트 수정 (챕터 밖)

- **`textbook/qa/check_course_continuity.py` 182·184행**(검토 B R-1): `before-manifest.json`에 옛 해시(`4f9fce62…`)로 등록된 `continuity-ch09-search.jsonl`이 바뀌어 182행 `AssertionError`로 멈췄습니다. 허용 목록에 ch09 기록 파일을 더하고 184행 분기를 ch10과 같은 모양(`endswith(('continuity-ch10-indexing.jsonl', 'continuity-ch09-search.jsonl'))`)으로 넓혔습니다. 이 분기는 원본 줄마다 `runs/continuity/<source_run_id>.jsonl`이 같은 JSON인지 확인하므로, **옛 사본 `20260909T161218875711-ch09.jsonl`을 지우면 다시 막힙니다**
  - 고친 뒤 실행 결과: **212행 zip 신선도까지 갑니다**(`AssertionError: Stale archive: part1-practice.zip/…`). 172~198행 원본 로그 보존 블록은 통과합니다. zip 신선도는 전체 마감 몫입니다
- **`textbook/part3/_build_index.py`**(검토 B C-2): `CHAPTERS` 항목이 `(slug, 제목, 강의, 실습, 설명)`이고 56행이 `len(sources) != lecture`로 절 수를 검사해, 07절이 붙자 `ValueError: Incomplete chapter: ch09`로 멈췄습니다. **절 수 칸을 따로 두었습니다**(`(slug, 제목, 6, 10, 7, 설명)`, ch10 8, ch11 6, ch12 12). 목차 문장은 `강의 {lecture}시간 · 실습 {practice}시간 · {len(sources)}절`이라 「6시간 · 10시간 · 7절」로 나옵니다. Part 3 목차·zip 재생성은 전체 마감 몫이고, 이번에는 스크립트가 07절 있는 상태를 받아들이게만 했습니다
- **개선 전 QA 스크립트 네 개**(검토 B C-5·07-10 정정): `qa/check_content.py`는 **통과합니다**(개선본에 `{{code:}}`·`{{output:}}`이 0개라 보존 출력 12블록과 manifest 해시만 검사) → `SECTIONS`에 07을 더해 07 페이지도 보게 했습니다. `qa/test_build.py`·`qa/test_code_evidence.py`는 절 목록과 무관하고 **6 passed**입니다. `qa/test_notebook_migration.py`는 `{{svg:}}` 5개·`{{img:}}` 3개·노트북 코드에 `except `를 요구하는 개선 전 전제라 2건이 실패하고, `qa/check_structure.py`는 b1~b11 열한 블록과 `<details class="instructor">`를 요구해 01~07 전부에서 실패합니다 → 두 파일을 `qa/upgrade/before/qa-scripts/`로 `mv -n`했습니다(삭제 아님, 참조하는 코드 0곳)

## 9. 전체 마감 순서 (이 순서를 지켜야 검증이 끝까지 갑니다)

1. `textbook/downloads/part3-practice.zip`·`llm-practice.zip`(필요하면 `part4-practice.zip`) 재생성 — §7 허용 목록 수정 뒤라야 06 노트북이 zip에서 실행됩니다
2. `textbook/part3/qa/run_continuity_bundle.py`를 **`--reuse-upstream` 없이** 실행 — 옛 `temporary_extraction` 폴더가 이미 없어 재사용 경로는 쓸 수 없습니다. `bundle-execution-results.json`과 `bundle-execution/`이 새로 만들어집니다
3. `visual.cjs`로 ch09 HTML 8개를 다시 찍어 **`textbook/part3/ch09-rag-first-run/qa/visual-results.json`을 14행 → 16행**으로 갱신(지금은 개선 전 14행. 이번 마감에서는 `/tmp` 사본으로 돌려 **16/16 PASS**를 확인만 했습니다)
4. `textbook/part3/qa/finalize_continuity_evidence.py` 15행 **`assert len(visual) == 88`을 90으로** 고쳐 실행(ch09가 2행 늘어남). 37행 `assert not any(execution_input(name) for name in changed)`은 2번을 먼저 끝내야 통과합니다
5. `textbook/part3/qa/check_continuity.py`·`textbook/qa/check_course_continuity.py`를 끝까지 실행(각각 zip 신선도에서 멈춰 있음)
6. Part 3 목차 `textbook/part3/_build_index.py` 재생성(절 7개 표시), `textbook/qa/upgrade-progress.md`·과정 요약 Part 3 절은 Part 3 마지막 챕터 뒤

## 10. 그림 색 판단 선례

- 넣은 글·문서 청크·저장 항목·질문·설정·색인·기록 파일 **초록**, 정의한 함수·검색 단계·이름표 만들기 **파랑**, 실행한 `gpt-5.4-mini`·`text-embedding-3-small` **보라**, 출력으로 확인한 값·검사 결과·검색 결과·기록 한 줄 **노랑**, 실행하지 않은 단계·두 조건 공통 값·Ch 11이 읽는 칸 **회색**(점선은 화살표). **빨강은 paired Before 결함 결과 한 상자씩**(01-4·02-4·03-4·04-4·05-1·05-4·06-4), experiment 07은 0장. `xychart-beta` 막대는 주황(03-3·02-3)
- 원인 과장 막기: 두 조건 답에 모두 있던 값은 결과 상자에서 빼 맨 아래 회색 상자로(01-4 「월요일 True」, 03-4 1위 2쪽, 04-3·04-4, 05-1·05-3·05-4, 06-3·06-4, 07-3 다섯 칸). 두 실행에서 달라진 값은 양쪽 칸에 모두 적습니다
- 모양: subgraph = 「칸」, 칸 안 세로 쌓기는 `direction TB` + `a ~~~ b`, sequenceDiagram은 실선 요청·점선 응답 + `messageAlign: left`, 메모는 그 기록이 남는 시점에. viewBox 폭 868 이하(이번 27장 최대 856). **렌더 도장 `*.render.json`은 지우지 않습니다**(mmd를 고치면 자동 재렌더, 같은 mmd는 `render_mermaid.py --force`)

## 11. 강사 확인 대상

- **절 제목 두 개(반영하지 않음, 검토 A C-4·Q6)**: `01 · RAG 지도 — 검색으로 Select를 자동화한다`는 이 챕터의 유일한 서술형 제목이고 영문 용어에 조사를 바로 붙였습니다(권고: 「01 · RAG 지도 — 골라 넣기를 검색이 대신하면」). `04 · 생성과 출처 인용 — 첫 완주`의 「첫 완주」는 01절과 챕터 제목 `Ch 9 · RAG 첫 완주 + 실험 하네스`에 이미 있습니다(권고: 「04 · 생성과 출처 인용 — 답에 출처를 붙이고 검사하기」). 바꾸면 이웃 절 HTML의 이전/다음 링크 한 줄과 `_src/index.html` 절 표가 함께 바뀝니다
- **07 표시 제목**을 「07 · RAG 실습: 문서 청크 크기를 바꿔 검색부터 답 검사까지」로 줄였습니다(파일·slug `07-RAG-실습` 유지)
- **강의·실습 범위 문장**: 01~06 노트북 준비물 「강의와 실습 범위」 + `_src` b5 한 단락. 03·04에 「2절은 01·02절과 같은 코드라 강의에서 빠르게 확인합니다」를, 07 b5에 「5·6절 정의 셀은 앞 절과 같은 코드라 실행만 하고 … 3·4·7·8·9절 출력을 강사와 함께 읽습니다」를 더했습니다(작업자가 정함)
- **meta 시수**: 01 1h/1h, 02~05 1h/2h, 06 1h/1h → 합 강의 6h·실습 10h = 16h(유지). 06이 코드 셀 32·검사 문장 642로 가장 무거운데 실습 1h인 배분
- **07 실습 요청 6번**: 규격 §7-2는 3~5번이지만 Ch 8 07 선례가 「5번(최대 6번)」이고 까닭(색인을 두 번 만듦)이 준비물에 있습니다. 줄이려면 실행 2에서 색인을 만들지 않아야 해 주제가 사라집니다
- **정답키 공개 정책**(§7): `labs/data/rag-corpus/queries.jsonl`을 학생 묶음에 넣기로 하고 세 delivery 검사의 금지 목록을 바꿨습니다. → **사용자 결정 2026-09-18: 현재 상태 유지(묶음에 포함)**. 학생이 06절 하네스를 그대로 실행할 수 있게 하고, 정답 라벨이 보이는 점은 `시작하기.md` 안내로 알립니다. Ch 11 평가 실습도 같은 정답셋을 쓰므로, Ch 11 작업 때 「답을 먼저 읽지 않고 실행한 뒤 확인」 안내를 이어 씁니다
- 검토 권고대로 유지한 설계(A Q1~Q5·B Q1~Q3): 01 5쪽 전체 색인·Before 결론 한정·과업 명세에서 쪽 번호 예시 제거·01-4 회색, 02 380/100 탐색 공개·02 제목, 03 합성 문서 D01~D03 제거·임베딩 이름 두 개·「개수 2」 추론, 04 `source` 키 Before·값 바꿔 보기·짝 맞춤을 사람이 한 한계, 05 전부, 06 k=2·평가셋에서 라벨 읽기·이름표 입력에 `corpus` 추가·두 실행 답 차이, 07 비교 설계·삽화
- 규격에 더한 두 줄(§7-2)과 PLAYBOOK §4 두 줄(§13)

## 12. 기준 버전·요금 확인 날짜

- 실습 폴더 `labs/part3/ch09-rag-first-run/pyproject.toml`·`uv.lock`: langchain **1.4.0**, langchain-core **1.6.2**, langchain-openai **1.6.0**, langchain-text-splitters **1.1.2**, openai **3.8.0**, pypdf **6.17.0**, tiktoken **0.14.0**, numpy **2.5.3**, pyyaml, python-dotenv **1.2.3**. 새 커널 `nbclient==0.11.0`·`ipykernel==7.3.0`, Linux aarch64 Python 3.12.13. 절마다 준비물에 기준 버전 + 「다른 버전과 Windows·macOS에서는 이번에 실행하지 않았습니다」
- 요금: `gpt-5.4-mini` 100만 토큰당 입력 0.75·출력 4.50달러(Ch 6 06절 2026-09-17 확인), 임베딩 `text-embedding-3-small` 0.02달러(OpenAI 모델 안내 2026-09-17 확인). **`config.yaml` `prices` 주석의 확인일은 2026-09-07**이고 값은 같습니다(계약 파일이라 날짜는 고치지 않았습니다). `rag.py` 27행에는 `[[미정: 임베딩 모델]]` 주석이 남아 있습니다(학생 묶음에 들어가지 않는 파일)
- 소스 확인: langchain-text-splitters 1.1.2 기본 `separators=["\n\n","\n"," ",""]`·`length_function=len`·`_merge_splits`의 겹침 처리(구분자 길이 포함), langchain-core 1.6.2 `similarity_search_with_score` = `embed_query` → `cosine_similarity` → `argsort()[::-1][:k]`, langchain-openai 1.6.0 `OpenAIEmbeddings` `embedding_ctx_length=8191`·`chunk_size=1000`·`dimensions=None`, langchain 1.4.0에 `langchain.chains` 없음

## 13. 규격·절차서에 더한 줄

- `QUALITY-UPGRADE.md` §7-2: 절을 더하거나 노트북이 읽는 파일을 바꾸면 실습 묶음 허용 목록(`textbook/part3/public-files.json`·`textbook/_notebook/build_bundle.py`)과 묶음 금지 목록(`check_delivery.py` 계열)을 함께 확인한다 / 절 수를 세는 목차 스크립트(`_build_index.py`)와 과정 단계 검사(`check_course_continuity.py`)의 허용 목록도 함께 확인한다
- `PLAYBOOK.md` §4: 같은 두 줄을 실행 절차 관점으로(묶음에서 노트북을 실제로 풀어 실행해 보기, 과정 단계 검사가 어디까지 가는지 적기)

## 14. 남은 것

- **전체 마감**: §9 순서. `textbook/qa/upgrade-progress.md` Ch 09 행은 「완료(강사 확인 대기)」로 갱신했습니다
- **다시 실행하면 함께 고칠 코드(지금은 재실행 금지)**: 05·06·07 준비 셀 [5]의 쓰이지 않는 `import os`(바로 뒤 키 확인 셀이 다시 `import os` — 01~04도 같은 모양, 검토 B 05-1), 06 `chunk_id` 번호에 네 자리 채우기(Ch 10과 맞추려면, R-3), 01 노트북 [30]을 두 셀로 나누기(주석 뺀 15줄, 규격 권장 3~12줄 초과 — 검토 A C-5), `rag.py` 76행 주석 「몇 번 청크」와 27행 `[[미정]]` 표시
- **삽화를 다시 만들 때 고칠 것**: 05-5는 상자 카드에서 초록 스티커를 완전히 빼고 큰 모양만 남긴다(지금은 「모두 같아서 뜻이 없다」를 그림 읽기에 적어 처리 — 02-5·03-5·04-5에서 초록 스티커를 메타데이터·출처로 배운 학생에게 생각할 거리)
- **빌더**: `_build.py`의 표 감싸기를 img·mermaid 치환 뒤로 옮겨 `_template/builder.py`와 순서를 맞추기(현재 결과는 같음)
- 2차 검토(두 보고서 끝 「2차 검토 때 볼 곳」), 강사 확인(§11)
- 정리 대상(삭제하지 않고 목록만, 삭제 승인 필요): 옛 도식·삽화 `figures/01-파이프라인.svg/.excalidraw`·`01-오픈북-비유.png/.caption.md`·`02-청크-경계.*`·`03-벡터-검색.*`·`05-실패-경로.*`·`05-지어낸-숫자.*`·`06-하네스-루프.*`·`06-실험-노트.*`·`figures/_gen_figures.py`, `qa/upgrade/gates-wip-01.json`~`07.json`, `qa/upgrade/before/06-to-07/`·`before/review-round1/`, 개선 전 QA 자료(`qa/langchain-before/`·`qa/notebook-before/`·`qa/before-after-before/`·`qa/language/_workspace/`), `textbook/part3/__pycache__`·`textbook/qa/__pycache__`·`textbook/part3/qa/__pycache__`·챕터 `__pycache__`(마감 세션의 `py_compile`이 만든 것 포함), 실습 폴더 `__pycache__`·`.venv`(2026-09-09)·`.ruff_cache`·`.pytest_cache`·`.cache/index-*.json`, `.cache/vm/venv-ch09-rag-first-run`(전체 마감 때), 기기 `/tmp/ch09-01`~`/tmp/ch09-07`·`/tmp/ch09-rvA`·`/tmp/rv09b`·`/tmp/ch09-close`
