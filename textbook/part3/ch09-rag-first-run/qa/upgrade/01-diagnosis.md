# 01-RAG-지도 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 01, `figures/01-*`, 옛 빌더 사본 `_build.before-upgrade.py`). 챕터 전체 수정 전 게이트는 이 절 작업 전에 남긴 `gates-before.json`(6절 합계 G1 12·G2 6·G3 10·G4 2·G5 72·G6 151·G7 15 = 268, 0/6). 이 챕터에는 옛 노트북 생성기(`make_*.py`·`_make_notebooks.py`)가 없어 실행 막는 줄을 넣을 대상이 없었습니다(`find`로 확인).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 1 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 15 | 0 |
| G6 | 31 | 0 |
| G7 | 2 | 0 |
| 코드 셀 | 13 | 21(준비 3) |
| 검사한 문장 | 169 | 438 |

G8: `run_section.sh` 새 커널 PASS 두 번(2026-09-17 14:54·14:55, 21 코드 셀, 코드 해시 `fb30edf8…ff233` 같음). 교재 출력은 두 번째 실행(`outputs_sha256` `44561e7a6a89d55db5e85405e6c01fa11e713fd5b312f23599b4554e9de9eb52`). 두 실행에서 검색 결과·문서 청크 수·벡터 앞 숫자는 같았고, 모델 답 세 개 가운데 Before와 After 답 글이 달랐음(아래 「실행 출력」). 결과 읽기는 두 번째 출력으로 `[[READ_…]]` 자리를 채움(`mdpatch.py`, 재실행 없음). `chapter.json`이 없어 `verify.py --chapter textbook/part3/ch09-rag-first-run`을 따로 실행 → `PASS 6 sections / 68 code cells (max 25 lines)`(max 25는 개선 전 02~06). 빌드 HTML `{{` 0건, `figure.mmd` 4·`figure.illustration` 1. `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch09-01/vis/vis.cjs` 사본 + HTML 사본). `runs/`는 읽지도 쓰지도 않음. Ch 8·7·6 runs 사슬 파일도 읽지 않음.

## 수정 전 주요 문제

- G2: [19] 생성 셀 16줄(f-string 삼중 따옴표 프롬프트 + 모델 셀 + `invoke`)
- G5: 제목 셀·핵심 그림 없음, 모든 코드 셀 뒤 결과 읽기 없음(12건), 마지막 After 코드 뒤 설명 없음
- G6: 70자 초과 12(참고 자료 3 포함), 영문+조사 시작 15(「RAG는」「k는」「`PdfReader`가」「Before는」 등), 5문장 넘는 단락 4
- G7: Mermaid 0(옛 Excalidraw `01-파이프라인.svg` 하나), 설계표 없음, 삽화는 두 칸 `{{img:이름|캡션}}`
- 사다리 밖 문법(게이트가 세지 않은 것): `from pathlib import Path`·`Path.cwd().resolve()`·`start.parents`·`folders.extend()`, `enumerate(…, start=1)`·f-string 안 딕셔너리 인덱싱(`f"{hit.metadata['doc_id']} p.{…}"`), f-string 삼중 따옴표 프롬프트, `"\n\n".join()`, `try/except AssertionError`로 실패 표시, 모델 문장 속 단어 `assert "월요일" in answer.text`(규격 §3 금지)
- 모델: `init_chat_model(…, temperature=0, reasoning_effort="none", max_tokens=300)` — 출력 상한 300이 Ch 8 출력 예약분과 이어지지 않음. 실행일 문장 없음
- 내용: (1) 01 `_src` 정의 「청크 = 문서를 검색 단위로 자른 조각」·RAG 정의 「관련 조각」 — Ch 5 「조각」 = 토큰과 충돌(과정 요약 Part 1 §5·규격 §4 「청크」 결정). (2) 스트림 청크(Ch 6 04)와의 구분 없음. (3) 「API 비용을 줄이려고 질문과 관련된 2~3쪽만 임베딩」 — 사람이 쪽을 먼저 고른 뒤 검색해서, b2 「Select를 사람이 아니라 검색이 한다」와 어긋남. (4) 메시지 목록 대신 문자열 하나로 `invoke`(Ch 7·8은 system·developer·user 목록, 과정 요약 Part 2 §2 「문자열 하나로 invoke」 처음 쓰면 풀기 대상). (5) b3가 「Ch 5 임베딩」「Ch 8 Select」를 개선 전 기준으로 적고, Ch 8이 E01 글을 옮겨 적은 것·PDF 추출 띄어쓰기 차이를 잇지 않음. (6) 도식 설명 「파란 상자는 학생 코드… LLM 생성도 그 흐름 안」·「왼쪽에서 오른쪽으로」가 옛 SVG 기준. (7) 참고 자료 확인일 2026-09-07·09, 임베딩 모델 차원·요금 확인일 없음. (8) Before 결과를 「출처 검사 실패」라는 `except` 문구로만 보여 줌. (9) 옛 비유 삽화 `01-오픈북-비유.png`는 사람이 그려진 오픈북 좌우 비교로, Ch 7·8 책상 색 약속과 이어지지 않음

## 바꾼 것

- **빌더(`_build.py`, 이 절에서 먼저 처리, PLAYBOOK §2 7단계)**: Ch 8 `_build.py`의 `inline_mermaid(spec)`·`inline_illustration(name, spec)`을 가져와 `{{mermaid:이름|alt|캡션}}`·세 칸 `{{img:이름|alt|캡션}}`을 더함. 두 칸 `{{img:이름|캡션}}`은 개선 전과 같은 `<img alt>`(이스케이프하지 않는 옛 동작까지). 치환 뒤 `\{\{[a-z]+:` 토큰이 남으면 `ValueError`로 멈춤. **다른 점 하나**: 이 챕터 CSS `figure svg{width:100%;min-width:760px}` 때문에 Mermaid SVG 인라인 style에 `min-width:0`을 더함(작은 도식이 760px로 늘어나지 않게, CSS는 바꾸지 않아 다른 절 HTML 불변). 확인: (a) 바꾸기 전 다시 빌드한 7개 HTML = 디스크 HTML(해시 같음), (b) 바꾼 뒤 다시 빌드한 7개 = (a), (c) Ch 8 그림으로 `inline_mermaid`가 `_template/builder.py _inline_mermaid`와 `min-width:0;`만 빼면 문자열까지 같고, 세 칸·빈 캡션 `inline_illustration`은 `_inline_img`와 같음(`/tmp/ch09-01/tokentest.py`), (d) 01 개선 뒤 02~06·index HTML 해시 같음(`/tmp/ch09-01/hash/after01.txt`). 공용 도구(`_template`, `_notebook`)는 고치지 않음
- **용어(규격 §4 「청크」 결정)**: 한정어 없는 「청크」를 쓰지 않고 「문서 청크」로 씀(노트북·본문·그림·캡션). 처음 쓰는 자리(노트북 3절, 본문 b5 「PDF에서 벡터스토어까지」·용어 표)에 「Ch 6 04절 스트림 청크와 다른 것」·「Ch 5 「조각」(토큰)과도 다름」 문장. 개선 전 「관련 조각」「자른 조각」 정의 삭제. 메타데이터는 Ch 8 02 뜻(내용 옆 설명 값)으로 이음. 코드 이름 `chunks`·`chunk_size`·`chunk_overlap`은 라이브러리 이름이라 그대로
- 모델: `nbkit.key_and_model_cells()`(KEY → `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` → 실행일 `RUN_DATE` 2026-09-17 결과 읽기 + temperature 0 ≠ `do_sample=False`). `max_tokens=300` 뺌. 임베딩 `OpenAIEmbeddings(model="text-embedding-3-small")`(API 모델, 기본 벡터 길이 1536 — OpenAI Embeddings 안내 2026-09-17 확인·노트북 출력 `질문 벡터의 숫자 개수: 1536`, 요금 100만 토큰당 0.02달러 — 모델 안내 2026-09-17 확인, 준비물·b7·참고 자료에 적음). 로컬 모델·torch 없음
- 데이터: `E01.pdf`·chunk_size 500/50·k=2와 k=1 비교·Before(검색 없이)/After(검색 근거)·paired 형식 유지. **PDF 5쪽 전체를 색인**(개선 전 2~3쪽만). 질문을 Ch 8 `closure_question`(「…정기 휴관일은 언제이고, 공휴일이 월요일과 겹치면 어떻게 되나요?」)으로, 메시지 목록을 Ch 7·8 모양(`persona_text` Ch 8과 같은 글, `task_text`는 Ch 8 글에서 출처 예시 `[E01 p.2]`를 빼고 「문장마다 끝에 근거 앞에 붙은 출처 표시를 그대로 적으세요」 — 검색이 출처를 고르므로 지시에 실제 쪽 번호를 넣지 않음, b5·복습 5에 까닭)
- 기본 경로: 설치(버전 7줄) → import(`os`·`PdfReader`·`Document`·`RecursiveCharacterTextSplitter`·`OpenAIEmbeddings`·`InMemoryVectorStore`·`init_chat_model`) → 키 → 모델 → 2절 후보 경로 세 개 `for`+`break`(Ch 8 06 모양, `os.path.exists`) / 쪽 수·2쪽 글자 수·「휴관」 줄(`split("\n")`+`in`)·Ch 8 글 비교 `False` / 쪽마다 `Document`(카운터 `page_number = page_number + 1`) → 3절 `split_documents`·쪽별 글자 수 → 4절 `embed_query`·벡터 길이 / `from_documents`·`len(store.store)` → 5절 `similarity_search(k=2)`·출처 표시(변수만 넣은 f-string)·앞 20자 `replace` → 6절 k=1·`assert len == 1` → 7절 페르소나·과업 명세 / 근거 글 `+`·user 글·목록·출력 → 8절 `invoke`·답 / `find_cited_marks(answer_text, marks)`(Ch 8 02 `find_cited_notes` 모양, 본문 5줄) / 「월요일」·검색 출처 → Before 질문만 목록·`invoke` / 검사 → After 7절 목록 다시 `invoke` / 검사 → 정리
- 쓰지 않은 것: `Path`·`enumerate(start=)`·f-string 안 계산·삼중 따옴표 프롬프트·`join`·`raise`·try·내포식·조건 표현식·`lambda`·`+=`·`@`·`BaseModel`·타입힌트·반복문 안 요청·모델 문장 `assert`. 새로 쓴 모양: 라이브러리 객체에 키워드 인자 딕셔너리(`metadata={…}`), 속성 `pages`·`page_content`·`metadata`, 글 `split("\n")`로 줄 나누기(Part 2 `split()`), 글 슬라이싱 뒤 메서드 하나(`[:20].replace(…)`), 변수만 넣은 f-string(Part 1 L1)
- 요청 수: 노트북 임베딩 4번 + mini 3번 = 7번. 탐색 실행 1번(`/tmp/ch09-01/probe1.py`, 임베딩 요청 3번 — 질문 벡터·벡터스토어 넣기·k=4 점수 검색, 모델 요청 없음) + 새 커널 2회 × 7 = 합계 임베딩 11번·mini 6번. 예상 비용 합계 약 0.004달러
- 탐색 뒤 정한 것(규격 §3, 본문 b7에 과정 공개): 탐색(5쪽 전체, k=4 점수)에서 1위 `E01 p.1` 표지 0.5832, 2위 `E01 p.2` 첫 문서 청크 0.5748(휴관 문장 포함), 3위 p.2 둘째 0.3833, 4위 p.5 0.3554. 이를 보고 5쪽 전체를 넣고 k=2와 k=1 비교를 유지하면 「가까운 순서 ≠ 답이 들어 있음」이 보인다고 판단. 두 점수 차이가 0.01보다 작아 순서가 뒤바뀔 수 있다는 것도 b7에 적음(노트북 두 실행에서는 같은 순서)
- 실행 출력(2026-09-17, 두 번째 새 커널): `고른 경로: labs/data/rag-corpus/pdf/easy/E01.pdf`(execute.py가 프로젝트 맨 위를 작업 폴더로 씀 — 결과 읽기에 밝힘, `notebooks`·실습 폴더 맨 위 후보는 `test -f`로 경로만 확인), `쪽 수: 5`·`2쪽 글자 수: 905`·휴관 줄 `매주 월요일은 정기 휴관일 입니다. … 그 다음 날인`/`화요일에도 휴관합니다.`·`Ch 8 글 「정기 휴관일입니다」가 있는가: False`, `Document 수: 5`, `문서 청크 수: 8`(1|45, 2|498, 2|452, 3|498, 3|462, 4|492, 4|412, 5|270), `질문 글자 수: 45`·`질문 벡터의 숫자 개수: 1536`, `벡터스토어에 넣은 문서 청크 수: 8`, k=2 `[E01 p.1] | 45`·`[E01 p.2] | 498`, `k=1 출처: ['[E01 p.1]']`, 8절 답 「미르시립도서관의 정기 휴관일은 매주 월요일입니다. 공휴일이 월요일과 겹치면 그 다음 날인 화요일에도 휴관합니다. [E01 p.2]」·검색 출처 `['[E01 p.2]']`, Before 답 「…매주 월요일입니다. (근거) 공휴일이 월요일과 겹치면 휴관하고, 그 다음 날인 화요일에 휴관합니다. (근거)」·`월요일` True·검색 출처 `[]`, After 답 「…매주 월요일입니다. 법정 공휴일이 월요일과 겹치면 그 다음 날인 화요일에도 휴관합니다. [E01 p.2]」·검색 출처 `['[E01 p.2]']`
- 첫 새 커널 출력(교재에 싣지 않음, 원인 판단 없음): 8절 답은 두 번째와 글자 같음. Before 답 「…매주 월요일입니다. 공휴일이 월요일과 겹치면 휴관하고, 그 다음 날인 화요일도 휴관합니다. [출처: 미르시립도서관 이용안내]」(출처 모양을 지어 적음), After 답은 8절 답과 같음. 두 실행 모두 Before가 근거 없이 월요일·화요일 휴관을 적고 검색 출처는 빈 목록 → 결론 「답을 원문의 어느 쪽과 대조할 수 있는가」는 두 실행에서 같음. 본문은 두 번째 출력만 인용하고 「한 번 실행한 결과, 일반화하지 않음」으로 씀(규격 §3·Ch 8 07 선례)
- 라이브러리 확인(설치 버전 소스): langchain-core 1.6.2 `InMemoryVectorStore.similarity_search` → `similarity_search_with_score` → `embed_query(query)` 뒤 `cosine_similarity` + `argsort()[::-1][:k]`(코사인 유사도 큰 순서), 속성 `self.store: dict`. langchain-openai 1.6.0 `OpenAIEmbeddings.dimensions` 기본 None·`chunk_size` 1000(문서 청크 8개 한 요청). langchain 1.4.0 설치판에 `langchain/chains` 없음(`ls`, b7 문장 근거)
- 용어 표 6개(RAG, 색인, Document, 문서 청크, 벡터스토어, top-k 검색) = meta 「새 용어 6」. meta 시수 「강의 1h | 실습 1h」 유지(01~06 합 강의 6h·실습 10h = `render_index()` 16h)
- 그림: Mermaid 4장(01-1 두 흐름·01-2 색인·01-3 k 비교·01-4 Before-After, PNG 직접 확인, viewBox 829·255·481·752) + 삽화 01-5 두 책상과 카드 상자 1장(2회 생성, 1차 job `5a2c5436-…` 탈락, 2차 job `c1135ec1-a1fe-45c2-9dea-cb278b167ad5` 채택, 4크레딧, 잔액 2834 → 2830). 옛 `01-파이프라인.svg/.excalidraw`·`01-오픈북-비유.png/.caption.md`는 지우지 않고 본문에서 쓰지 않음(정리 대상)
- 본문: 10블록 모두 다시 씀. b2 Ch 8 골라 넣기·Ch 5 07 찾아보는 단계 없음·에이전트 없음·Ch 11, b3 표(Ch 4 05, Ch 5 02·07, Ch 6 01, Ch 7 01~03, Ch 8 02·03·06) + E01 옮겨 적기와 PDF 읽기 차이, b4 비유·RAG 정의·두 흐름·용어 표, b5 색인·k·답, b6 Before/After 해석(빨강 1상자, 두 답 공통 「월요일」 회색 상자), b7 검색 누락(05절)·탐색 뒤 정한 값·PDF 추출 차이·메모리 벡터스토어·요금·`langchain.chains` 없음·rag-corpus 21건(`ls`)·기준 버전, b8 02절 연결, b9 복습 5문제, b10 참고 자료 확인일 2026-09-17. 제작 이력 문장 없음(규격 §4)

## 검토

- 스스로 확인: 결과 읽기·본문·캡션·그림 라벨의 숫자와 인용을 두 번째 새 커널 출력과 대조(G5·G7 0). 그림 방향 말(01-1·01-4 「위 칸·아래 칸, 칸마다 왼쪽에서 오른쪽」, 01-2 「위에서 아래로」, 01-3 「왼쪽 갈래·오른쪽 갈래」), 색 이름을 PNG와 대조. 01-4의 결과 상자에 두 답 공통 값(「월요일」, 휴관 요일 문장)을 넣지 않음(규격 §5-3)
- 삽화 검수(저장 파일 기준, `figures/01-5-두-책상과-카드-상자.prompt.md`): 오른쪽 책상에만 카드 두 장, 오른쪽 상자 빈칸·왼쪽 상자 꽉 참이 그림만으로 읽힘. 약점(클립보드 위 연필, 카드 수·간격 고르지 않음)은 그림 읽기에 「뜻이 없는 소품」으로 적음. 저장 PNG ↔ 채택 job 결과 픽셀 차이 0
- 별도 세션 검토: 아직(메인 세션 차례)

## 남은 것

- 뒤 절 작업자에게: `qa/upgrade/handoff.md` §01 → §02
- 정리 대상(삭제 승인 필요, 목록만): `figures/01-파이프라인.svg`·`.excalidraw`·`01-오픈북-비유.png`·`.caption.md`(옛 도식·삽화), `qa/upgrade/gates-wip-01.json`, 기기 `/tmp/ch09-01`, 실습 폴더 옛 `.venv`(2026-09-09)·`.cache/index-*.json`(약 30MB, 옛 예제 색인)
- 챕터 마감 때: `_src/index.html`(목차 본문, 게이트 밖)의 01절 설명·「청크」 표기를 절 본문과 대조(규격 §7-2). 개선 전 QA 스크립트 `qa/check_content.py`·`qa/test_notebook_migration.py`·`qa/test_build.py`는 개선 전 노트북·본문 기준이라 01 개선 뒤 일부가 맞지 않을 수 있음(실행하지 않음, 챕터 마감 때 확인)

## 검토 반영 (2026-09-17, 챕터 마감 세션)

별도 세션 검토 1차 A(§01~04)·B(§05~07)를 받아 반영했습니다. 보고서와 반영 내역 전체는 `review-round1-A.md`·`review-round1-B.md` 끝 「반영 결과」, 챕터 차원 정리는 `chapter-summary.md`입니다. **이 절 노트북은 다시 실행하지 않았습니다**(`code_sha256`·`outputs_sha256`·`executed_at` 전후 같음). 반영 뒤 게이트 `--label after --strict` 7/7 PASS(G1~G7 0), `verify.py --chapter` `PASS 7 sections / 175 code cells`, `visual.cjs` 16건 PASS, 실습 폴더 테스트 10 passed, 빌드 HTML `{{` 0건.

- **판정 accept**(상 0·중 0·하 1). 01-1 반영: b5와 노트북 5절 설명 셀의 `similarity_search()` 설명에 `InMemoryVectorStore` 한정을 더했습니다 — 「질문을 임베딩한 뒤 가까운 문서 청크부터 k개를 반환합니다. 이 벡터스토어(`InMemoryVectorStore`)는 가까운 정도를 코사인 유사도로 잽니다.」 Ch 10·12가 다른 벡터스토어를 쓸 때 점수 뜻이 달라진다는 인계는 `chapter-summary.md` §5.
- 결정 요청 네 가지(5쪽 전체 색인 / Before가 근거 없이 맞은 답의 결론 한정 / 과업 명세에서 `[E01 p.2]` 예시 제거 / 01-4 회색 처리)는 검토 권고대로 **모두 유지**했습니다(A Q1).
- **미반영 한 가지**: 검토 A C-4·Q6의 제목 변경(`01 · RAG 지도 — 검색으로 Select를 자동화한다` → 권고 「01 · RAG 지도 — 골라 넣기를 검색이 대신하면」)은 오케스트레이터 지시대로 **강사 확인 대상**으로만 남기고 `_build.py`를 고치지 않았습니다. 이 절만 서술형 제목이고 영문 용어에 조사를 바로 붙였다는 지적입니다.
- C-5의 노트북 [30](주석 뺀 15줄)을 두 셀로 나누는 일은 코드를 바꾸므로 재실행 금지 원칙대로 두었습니다 → `chapter-summary.md` §14.
- 챕터 공통: `_src/index.html` 목차 본문(C-1)과 실습 폴더 `README.md`(C-2)를 이번 마감에 다시 썼습니다. 01절 관련 문장은 「제공 PDF 경로, 쪽별 Document, 문서 청크, 검색 개수 `k`, 출처가 있는 답」·「Mermaid 4장 · 삽화 1장」입니다.
