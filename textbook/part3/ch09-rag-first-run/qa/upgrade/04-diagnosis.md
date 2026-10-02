# 04-생성과-출처-인용 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 04). 개선 전 04절에는 그림 파일이 없었습니다(`figures/04-*` 없음, 본문에 도식·삽화 토큰 없음). 챕터 전체 수정 전 게이트는 01절 작업 전에 남긴 `gates-before.json`(04절 G1 0·G2 1·G3 0·G4 0·G5 12·G6 26·G7 3 = 42).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 1 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 12 | 0 |
| G6 | 26 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 10 | 25(준비 3) |
| 검사한 문장 | 104 | 430 |

G8: 새 커널 PASS 두 번(같은 코드 `code_sha256` `a486b717…9f08d3`). 1차 16:33:06(`execute.py` 직접) `outputs_sha256` `15bf502c…10a7`, 2차 16:37:30(`run_section.sh`) `b58e59834ae26309d0cf40c21be0da9a5d1227e71052f019d577b599b06140bb`(교재 출력). 두 실행의 구조(요청 수, 검색 순서 p.2·p.1·p.3, 기록 출처, 입력 784토큰, 5절·7절·After 답 글과 검사 결과, Before 기록 출처·검사 결과)는 같았고, Before 답 둘째 문장만 달랐음(1차 「회원 한 사람은 도서를 한 번에 7권까지…」 → 2차 「도서는 한 번에 7권까지…」, 끝 표시 `[E01.pdf]`는 같음). 결과 읽기는 1차 출력으로 생성기에 쓴 뒤 2차 출력과 대조해 그 한 문장만 `mdpatch.py`로 맞춤(재실행 없음). 1차 문장은 교재에 싣지 않음(규격 §4). `chapter.json`이 없어 `verify.py --chapter textbook/part3/ch09-rag-first-run`을 따로 실행 → `PASS 6 sections / 107 code cells (max 25 lines)`. 빌드 HTML `{{` 0건(7개 모두), 04 HTML `figure.mmd` 4·`figure.illustration` 1. `visual.cjs` 1280px·390px PASS(`/tmp/ch09-01/vis/vis.cjs` 사본 + `/tmp/ch09-04/html/`). 다른 절 HTML 해시: 04만 바뀜(01·02·03·05·06·index 작업 전과 같음, `SECTIONS` 제목 안 바꿈). 실습 폴더 테스트 작업 전 `10 passed` = 작업 뒤 `10 passed`. `runs/` 27개 파일 SHA-256 작업 전후 같음(읽기·쓰기 0). Ch 6·7·8 runs 사슬 파일도 읽지 않음.

## 수정 전 주요 문제

- G2: After 셀 [20] 주석 제외 코드 15줄 초과(Document 복사·태그·삼중 따옴표 프롬프트·호출·`assert`를 한 셀에)
- G5: 제목 셀·핵심 그림 없음, 결과 읽기가 출력 값을 인용하지 않음(9건), After 코드 뒤 설명 없음
- G6: 70자 초과 13(참고 자료 한 줄 3 포함), 영문+조사 시작 12(본문 8·노트북 4 — 「`[D01 p.1]`은」「metadata가」「Before는」「AIMessage를」 등), 5문장 넘는 단락 1
- G7: Mermaid 0, 삽화 0, 설계표 없음
- 규격 밖(게이트가 세지 않은 것): 모델 셀에 `reasoning_effort` 없음(규격 §3), 모델 문장 속 단어 `assert "월요일" in answer.text`·`assert source_tag in answer.text`·`assert fixed_tag in fixed_answer.text`(규격 §3 금지), f-string 삼중 따옴표 프롬프트와 f-string 안 인덱싱 `f"[{broken.metadata['doc_id']} p.{…['page']}]"`, 문자열 하나 `invoke`(Ch 7·8 메시지 목록과 끊김), try `except KeyError`로 만든 Before(실제 서비스와 무관한 파이썬 오류), `type(…).__name__`, 영어 라벨(`metadata:`·`content:`)
- 이어짐: (1) 01~03절이 E01 5쪽·문서 청크 8개·`[E01 p.N]`·03 두 가지 질문과 k=3으로 이어 왔는데 04만 합성 Document D01·D02(「정기 휴관일은 매주 월요일입니다」「대출 기간은 14일입니다」). (2) 임베딩 객체 이름 `embedding`(01·03은 `embedding_model`). (3) 「출처 태그」「문맥 조립」「프롬프트」 등 01·Ch 8과 다른 말(Ch 8·01은 「출처 표시」「user 글」「메시지 목록」). (4) Ch 8 02·03·04 검사 함수(`find_cited_notes`·`find_missing_words`·`check_answer`)와 판정 한계(표시 모양만 믿지 않기)를 잇지 않음. (5) 「청크」 단독 표기. (6) b10 확인일 2026-09-07, meta 「코드 04-생성과-출처-인용.ipynb」

## 바꾼 것

- **형식·학습 질문 유지**: paired. 검색 결과의 메타데이터로 출처 표시 만들기 → 본문과 함께 모델에 넣기 → 답과 출처 검사 → 메타데이터를 잘못 옮긴 Before와 고친 After. 개선 전 Before(`page`를 빠뜨려 `KeyError`)는 「메타데이터를 잘못 옮기면 출처가 쪽을 가리키지 못한다」는 뜻을 살려, 실제로 흔한 실수인 **`source` 키(영어 뜻이 「출처」)를 출처로 넣기**로 바꿈 → 세 기록 출처가 `E01.pdf`로 같아지고 Ch 8 `check_answer()`가 세 기록을 모두 맞다고 반환(요청 전 기록 출처는 결정적, 검사 결과는 답에 `[E01.pdf]`가 나온 이번 실행). 빨강은 Before 결함 결과 한 상자.
- **데이터(합성 D01·D02 → E01 문서 청크)**: 01~03절과 같은 E01 5쪽·500/50 문서 청크 8개, 03절과 같은 빈 벡터스토어 + `add_documents()`, 03절 After와 같은 두 가지 질문 `combined_question`·지킬 말 `combined_keep_words = ["월요일", "7권"]`·k=3(handoff §03 → §04 결정). 새로 정한 값 없음(탐색 실행 없음). 점수는 03에서 봤으므로 `similarity_search()`로 메타데이터와 글자 수만(소수 넷째 자리 변동 회피).
- **Ch 8 함수 이어 쓰기**: 검색 결과를 Ch 8 04 `build_notes_messages()`가 읽는 기록 모양(키 `출처`·`내용`)으로 옮기는 새 함수 `make_note(chunk)`(본문 4줄, 출처 `f"{doc_id} p.{page}"` — 01 f-string 모양). `build_notes_messages`(Ch 8 04 같은 코드, 본문 10줄)·`find_cited_notes`(Ch 8 02 같은 코드)·`find_missing_words`(Ch 8 03·Ch 9 02·03 같은 코드)·`check_answer`(Ch 8 04 코드에서 바깥 이름 `closure_keep_words` → `combined_keep_words`만 바꿈, 주석과 설명 셀에 밝힘). 01 `find_cited_marks()`(표시 목록 받음)는 쓰지 않고 b3에 「같은 일을 하는 Ch 8 02절 함수」로 이음. 03 `make_source_mark()`는 쓰지 않음(출처 표시 대괄호는 `build_notes_messages`가 붙임).
- **메시지 목록**: 01절 `persona_text`·`task_text` 같은 글, `[("system", …), ("developer", …), ("user", …)]`. `messages[2][1]`로 user 글 꺼내기(Ch 8 07 `body_messages[2][1]` 모양). 모델 셀 `nbkit.key_and_model_cells()`(01과 같은 설명 셀 교체).
- **출처 인용 검사의 한계(Ch 7 05·Ch 8 04와 이음)**: 5절 검사 뒤 6절 「기록 내용과 대조하기」 — 기록마다 `find_missing_words(note["내용"], …)`로 어느 기록에 어느 지킬 말이 있는지 봄(결정적 출력 `E01 p.2 | ['7권']`·`E01 p.1 | ['월요일', '7권']`·`E01 p.3 | ['월요일']`). 이번 답이 두 표시를 끝에 모아 적어 문장-표시 짝이 답에 없고 사람이 맞췄다는 것, 지킬 말이 있어도 뜻은 원문으로 확인한다는 것을 결과 읽기·b5·04-2 회색 상자·b7에. Ch 8 04 Before의 「목록에 없는 표시」는 이번에 나오지 않았다고 b7에.
- **값 바꿔 보기**: 과업 명세에서 출처 문장만 뺀 `plain_task_text`(요청 1번, user 글·모델 같음). 이번 답에는 표시가 없고 검사 결과 같은 기록 `[]`, 빠진 지킬 말 `[]`. 「한 번 본 결과라 일반화하지 않음」.
- **요청 수**: 서비스 요청 6번(임베딩 2: `add_documents` 1·k=3 검색 1 / mini 4: 5절·7절·Before·After). 새 커널 두 번 = 12번. 비용 어림 0.01달러 미만(입력 784토큰 × 4 기준). 모델 문장 `assert` 0, `assert`는 `pdf_path is not None`·`len(hits) == 3`만.
- **기본 경로**: 설치(버전 7줄) → import(`os`·`PdfReader`·`Document`·스플리터·`OpenAIEmbeddings`·`InMemoryVectorStore`·`init_chat_model`) → 키 → 모델 → 2절 경로 / `load_pdf_pages` / 나누기·벡터스토어 → 3절 k=3 검색 / `make_note` / 기록 목록 → 4절 페르소나·과업 명세 / `build_notes_messages` / 목록·user 글 → 5절 `invoke`·입력 토큰 / `find_cited_notes` / `find_missing_words` / `check_answer` / 검사 → 6절 기록 내용 대조 → 7절 출처 문장 뺀 목록 → Before 기록·목록 / `invoke` / 검사 → After `messages` 다시 `invoke` / 검사 → 정리
- **쓰지 않은 것**: 내포식·try·`raise`·조건 표현식·`lambda`·`+=`·`join`·`Path`·`enumerate`·`zip`·`sum`·`max`·`@`·`BaseModel`·타입힌트·f-string 안 계산·반복문 안 요청·모델 문장 `assert`·구조화 출력. 새로 쓴 모양: 메타데이터 딕셔너리 통째 출력, 함수가 딕셔너리 리터럴 반환(`make_note`), 딕셔너리 `keys()`(03과 같음), 목록 두 겹 인덱싱 `messages[2][1]`(Ch 8 07).
- **함수 본문 줄 수 직접 셈**(규격 §2-2 L2): `load_pdf_pages` 9, `make_note` 4, `build_notes_messages` 10, `find_cited_notes` 6, `find_missing_words` 5, `check_answer` 7(주석 제외). 셀당 코드 줄 3~13.
- **용어**: 한정어 없는 「청크」 0건. 새 용어 1개 「출처 인용(citation)」 = meta 「새 용어 1」. 개선 전 「출처 태그」「문맥 조립」「프롬프트(문자열)」는 Ch 8·01 말 「출처 표시」「근거」「user 글」「메시지 목록」으로. 「기록」은 Ch 8 04 `build_notes_messages()`가 읽는 딕셔너리 뜻으로 쓰고, 내용이 사람이 적은 한 문장이 아니라 문서 청크 본문이라는 것을 노트북 3절·b4에 적음.
- **meta 시수**: 「강의 1h | 실습 2h」 유지(01~06 합 강의 6h·실습 10h = `render_index()` 16h). 코드 표기 「Jupyter Notebook」(01~03과 같음).
- **그림**: Mermaid 4장(04-1 검색에서 출처 검사까지·04-2 표시 검사와 내용 대조·04-3 출처 문장 있음과 없음·04-4 Before-After, PNG 직접 확인, viewBox 856·464·800·805) + 삽화 04-5 답안지의 같은 스티커 1장(1회 생성 채택, job `b1d21487-24ee-4239-bcad-f8d9fdeeb7e9`, 2크레딧, 잔액 2822 → 2820, 원본 SHA-256 `388944cb…e5fe`, 저장 PNG `0425e4c0…eb5e3a`, 채택 job 결과를 다시 받아 픽셀 대조 차이 0).
- **본문**: 10블록 모두 다시 씀. b2 01 한 번 받은 답·03 k=3 근거·검사의 한계, b3 표(Ch 6 01·Ch 7 05·Ch 8 02·03·04·Ch 9 01·02·03) + 함수 선택 한 문장, b4 비유·삽화·그림 읽기(그림은 문장마다 스티커, 실제 답은 끝에 모음)·04-1·용어 표, b5 기록으로 옮기기·답과 출처 검사(04-2)·값 바꿔 보기(04-3), b6 Before/After 해석(04-4, 빨강 1상자, 공통 값 회색), b7 검사 한계 네 가지·LangChain 예의 source(웹 주소)·입력 784토큰과 Ch 8 01 입력 가용분·Ch 11 평가·요금·기준 버전, b8 05절 연결, b9 복습 5문제, b10 참고 자료 3건(확인 2026-09-17). 제작 이력 문장 없음(규격 §4).

## 검토

- 스스로 확인: 결과 읽기·본문·캡션·그림 라벨의 인용을 두 번째 새 커널 출력과 대조(G5·G7 0). 1차와 달라진 Before 답 둘째 문장은 `mdpatch.py`로 맞추고 1차 글 잔존 0(`grep "회원 한 사람은 도서를"`). 그림 방향 말(04-1·04-3·04-4 「위 칸·아래 칸, 칸마다 왼쪽에서 오른쪽」, 04-2 「위에서 아래로」), 색 이름을 PNG와 대조. 04-3·04-4 결과 상자에 두 조건 공통 값을 넣지 않음(규격 §5-3). 7절 「출처 표시 없음」은 값 바꿔 보기 출력이라 노랑.
- 문장 확인(게이트 밖): 「로더 함수가 쪽마다 같은 파일 이름을 `source`에 적었다」는 `load_pdf_pages` 코드(`doc_id + ".pdf"`)로 확인. 「Ch 8 04절 Before 답은 목록에 없는 E01 p.2 표시를 적었다」는 Ch 8 04 `_src` 68행으로 확인. LangChain RAG 문서의 `source` 예는 2026-09-17 WebFetch(페이지 제목 「Retrieval Augmented Generation (RAG) with Deep Agents」, `doc.metadata.get('source', …)`를 본문 앞에 붙여 에이전트 파일을 만듦)로 확인하고 b7·b10에 그 범위로만 씀. 05절 연결 문장은 개선 전 05 노트북·`_src`(검색 누락과 답 없음 구분, 검색된 문서 ID 함께 보기)로 확인.
- 삽화 검수(저장 파일 기준, `figures/04-5-답안지의-같은-스티커.prompt.md`): 카드 세 장 세모·동그라미·네모, 답안지 두 줄 끝 세모·네모, 동그라미 없음 — 그림만 보고 「답안지가 두 카드를 가리킨다」가 읽힘. 약점(답안지 줄 묶음이 두 줄씩, 클립보드 왼쪽이 조금 잘림, 그림은 문장마다 스티커)은 그림 읽기에 적음.
- 별도 세션 검토: 아직(메인 세션 차례)

## 남은 것

- 뒤 절 작업자에게: `qa/upgrade/handoff.md` §04 → §05
- 정리 대상(삭제 승인 필요, 목록만): `qa/upgrade/gates-wip-04.json`, 기기 `/tmp/ch09-04`(1차 노트북 사본·삽화 원본·html 사본·해시·reps)
- 챕터 마감 때: `_src/index.html` 04 행(개선 전 「두 Document」「출처 태그」 등)을 절 본문과 대조(규격 §7-2). `_build.py` `SECTIONS` 04 제목 「생성과 출처 인용 — 첫 완주」는 그대로 둠(첫 완주는 01절에서 이미 한 번 함 — 마감 때 제목 검토 후보). 개선 전 QA `qa/check_content.py`·`qa/test_notebook_migration.py`의 04 전용 조건(개선 전 노트북 기준, 실행하지 않음), `qa/check_content.py` 31~35행이 읽는 `runs/examples/ex04_preserved.txt`·`ex04_missing_tag_preserved.txt`·`ex04_empty_hits_preserved.txt`·`ex04_search_miss_preserved.txt`(개선 전 예제 출력, 읽지도 바꾸지도 않음)
- 강사 확인 후보: Before를 `KeyError`에서 `source` 키 실수로 바꾼 설계, 값 바꿔 보기(과업 명세 출처 문장 빼기), 새 함수 `make_note()`와 Ch 8 `check_answer()` 바깥 이름 바꾸기

## 검토 반영 (2026-09-17, 챕터 마감 세션)

별도 세션 검토 1차 A(§01~04)·B(§05~07)를 받아 반영했습니다. 보고서와 반영 내역 전체는 `review-round1-A.md`·`review-round1-B.md` 끝 「반영 결과」, 챕터 차원 정리는 `chapter-summary.md`입니다. **이 절 노트북은 다시 실행하지 않았습니다**(`code_sha256`·`outputs_sha256`·`executed_at` 전후 같음). 반영 뒤 게이트 `--label after --strict` 7/7 PASS(G1~G7 0), `verify.py --chapter` `PASS 7 sections / 175 code cells`, `visual.cjs` 16건 PASS, 실습 폴더 테스트 10 passed, 빌드 HTML `{{` 0건.

- **판정 accept**(상 0·중 0·하 1). 04-1 반영: 노트북 [0] 준비물을 「6절 기록 내용 대조, 7절 값 바꿔 보기와 Before·After는 함께 실행하고 실습 시간에 읽습니다.」로 고쳐 `_src` b5와 6절 제목(「기록 내용과 대조하기」)에 맞췄습니다. 원문(PDF 쪽) 대조는 b7·[41]이 사람 몫으로 남긴 일이라 준비물에서 「원문 대조」를 뺐습니다.
- 결정 요청 세 가지(메타데이터 `source` 키 실수로 만든 Before / 값 바꿔 보기 = 과업 명세에서 출처 문장 빼기 / 출처 표시를 끝에 모은 답의 짝 맞춤을 사람이 한 한계)는 권고대로 **모두 유지**했습니다(A Q4). 검토에서 실제 API로 두 번 재현해 `입력 784`가 같고 둘째 문장만 달라지는 것을 확인했습니다.
- **미반영 한 가지**: 검토 A C-4·Q6의 제목 변경(`04 · 생성과 출처 인용 — 첫 완주` → 권고 「04 · 생성과 출처 인용 — 답에 출처를 붙이고 검사하기」)은 오케스트레이터 지시대로 **강사 확인 대상**으로만 남겼습니다. 「첫 완주」가 01절과 챕터 제목 `Ch 9 · RAG 첫 완주 + 실험 하네스`에 이미 있다는 지적입니다.
- C-5 반영으로 b5와 노트북 준비물에 「2절은 01·02절과 같은 코드라 강의에서 빠르게 확인합니다.」를 더했습니다(**강사 확인 대상**).
