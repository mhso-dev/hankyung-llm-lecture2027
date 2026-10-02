# Ch 09 RAG 첫 실행 — 절 사이 인계

절 작업자가 다음 절 작업자에게 넘기는 기록입니다. 앞 내용: `textbook/qa/upgrade-course-summary.md`(Part 1·Part 2 절), 바로 앞 챕터 요약 `textbook/part2/ch08-context-engineering/qa/upgrade/chapter-summary.md`(§4 Ch 09 인계). 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md`.

## §01 → §02

(01절 품질 개선 2026-09-17. 결과는 `01-diagnosis.md`, 게이트 G1~G7 0(수정 전 G2 1·G5 15·G6 31·G7 2), 코드 셀 21(준비 3), 노트북 요청 7번(임베딩 4 + mini 3, 탐색 임베딩 3 + 새 커널 2회 × 7 = 임베딩 11·mini 6). 챕터 첫 절이라 `gates-before.json`은 6절 전체 수정 전 기록(G1 12·G2 6·G3 10·G4 2·G5 72·G6 151·G7 15 = 268). 삽화 01-5 채택(2차 job `c1135ec1-…`, 4크레딧), Mermaid 4장)

### 빌더 변경과 02~06 작업자가 쓸 토큰 모양 (먼저 읽을 것)

- **`_build.py`를 고쳤습니다**(챕터 파일만, 공용 `_template`·`_notebook`은 그대로). 옛 사본 `qa/upgrade/before/_build.before-upgrade.py`. 절 목록은 `SECTIONS` 하드코딩이고 `chapter.json`은 없습니다. 실습 절 07을 붙일 때 `SECTIONS`에 주제까지 넣은 제목 한 줄(규격 §7-2)과 `render_index()`의 「절 6개」, `_src/index.html` 표를 함께 고칩니다
- **토큰 모양**(`_src`에 이대로 씁니다)
  - `{{notebook:slug|example}}`·`{{notebook:slug|failure}}`(paired) 또는 `{{notebook:slug}}`(experiment) — 공용 `render.expand_notebooks`, 개선 전부터 동작. 02~05 개선 전 노트북은 `lesson_part` before/after가 있는 paired, 06 형식은 06 작업자가 노트북 메타데이터 `lesson_format`으로 확인
  - `{{mermaid:이름|alt|캡션}}` — `figures/이름.svg`를 `<figure class="mmd">`로 넣고 캡션을 붙입니다. `_src`에서 `<figure>`로 감싸지 않습니다. alt·캡션에 `|`·`}` 금지
  - `{{img:이름|alt|캡션}}` — 삽화 PNG를 폭 1100px JPEG `<figure class="illustration">`로. `_src`에서 `<figure>`로 감싸지 않고 바로 아래에 「그림 읽기」 단락
  - 옛 두 칸 `{{img:이름|캡션}}`는 개선 전과 같은 `<img alt>`(감싸는 `<figure>`는 `_src`가 씀), 옛 `{{svg:이름}}`·`{{code:}}`·`{{output:}}`도 그대로 동작. 02~06 개선 전 `_src`는 `{{svg:0N-…}}`·두 칸 `{{img:}}` → 개선 때 `{{mermaid:}}`·세 칸으로 바꾸고 옛 SVG·Excalidraw·PNG는 지우지 않습니다
  - 치환 뒤 `\{\{[a-z]+:` 모양이 남으면 `ValueError: <slug>: 치환하지 못한 토큰`으로 빌드가 멈춥니다
  - **Ch 8과 다른 점**: 이 챕터 CSS에 `figure svg{width:100%;min-width:760px}`가 있어, `inline_mermaid()`만 SVG 인라인 style에 `min-width:0`을 더합니다(CSS는 그대로라 다른 절 HTML 불변). 그 밖의 출력은 `_template/builder.py`와 문자열까지 같음
- **빌더 확인 방법**: (a) 바꾸기 전 다시 빌드한 7개 HTML = 디스크 HTML, (b) 바꾼 뒤 7개 해시 같음, (c) `/tmp/ch09-01/tokentest.py`(Ch 8 그림으로 `_template/builder.py`와 문자열 비교), (d) 01 개선 뒤 02~06·index HTML 해시 같음(`/tmp/ch09-01/hash/after01.txt`). 02~06 작업 전후에 `cd textbook/part3/ch09-rag-first-run && sha256sum *.html`로 다른 절 HTML이 바뀌지 않았는지 봅니다
- **verify**: `run_section.sh`는 `chapter.json`이 없으면 verify를 건너뜁니다. `verify.py --chapter`는 `chapter.json` 없이 동작하므로 따로 실행: `UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch09-rag-first-run uv run --project labs/part3/ch09-rag-first-run python textbook/_notebook/verify.py --chapter textbook/part3/ch09-rag-first-run` → 01 뒤 `PASS 6 sections / 68 code cells (max 25 lines)`. 추가로 `grep -c "{{" textbook/part3/ch09-rag-first-run/NN-*.html`(0)과 `visual.cjs` 사본(아래)
- **게이트·mdpatch·pack**: `upgrade_gates.py`·`mdpatch.py`·`pack.py`는 `chapter.json` 없이 `_src/NN-*.html`·`labs/part3/ch09-rag-first-run`으로 동작(01에서 확인). 게이트는 `--section NN`으로만 돌렸습니다

### 용어 결정 적용(규격 §4 「청크」, 02~06도 같게)

- **「문서 청크」**로 부르고 한정어 없는 「청크」를 쓰지 않았습니다(노트북·본문·그림 라벨·캡션·alt). 01 노트북 3절과 본문 b5·용어 표에 「Ch 6 04절 스트림 청크와 다른 것, Ch 5 「조각」(토큰)과도 다름」 문장을 두었습니다 → 02~06은 처음 자리 문장을 되풀이하지 말고 「01절에서 정한 문서 청크」로 이어 쓰면 됩니다
- 코드 이름(`chunks`·`chunk`·`chunk_size`·`chunk_overlap`·`chunk_id`)은 그대로 둡니다. 출력 라벨은 「문서 청크 수:」처럼 한국어로
- 「조각」은 토큰 뜻으로만. **개선 전 02 `_src`에 「LangChain이 텍스트 조각을 다루는 기본 단위」(28행)·「두 조각으로 갈라지는」(60행)과 「청크」 단독 표기가 많습니다** → 「문서 청크」와 「두 부분으로」 등으로
- 메타데이터 = Ch 8 02 뜻(내용 옆에 적어 두고 찾거나 고를 때 쓰는 설명 값). 01은 `doc_id`·`page`·`source` 세 키
- 새 용어 표(01): RAG(검색 증강 생성, 오픈북 시험), 색인(indexing), Document, 문서 청크(chunk, 긴 공지문을 문단 카드에 나눠 옮기기), 벡터스토어(vector store), top-k 검색. 실패 모드 이름은 01에 쓰지 않았습니다(05 b3는 Ch 8 04 네 이름 — 오염·산만·혼란·충돌 — 원글 정의로)

### 실행 환경

- 가상환경 `$ROOT/.cache/vm/venv-ch09-rag-first-run`을 이 절에서 만들었습니다(`uv sync --locked`, uv 캐시 `$ROOT/.cache/vm/uv`, 33초). `run_section.sh`가 자동으로 씁니다. torch·로컬 모델 없음(임베딩은 OpenAI API). 새 커널 실행 약 10초. 키는 루트 `.env`(`find_dotenv(usecwd=True)`), 탐색 스크립트는 `ROOT=$PWD UV_CACHE_DIR=… UV_PROJECT_ENVIRONMENT=… uv run --project labs/part3/ch09-rag-first-run python /tmp/…` + `load_dotenv(os.environ["ROOT"] + "/.env")`
- **기준 버전(uv.lock)**: pypdf **6.17.0**(Ch 8 폴더는 6.18.0), langchain 1.4.0, langchain-core 1.6.2, langchain-openai 1.6.0, langchain-text-splitters 1.1.2, langchain-community 0.4.2(01은 안 씀), openai 3.8.0, tiktoken 0.14.0(01은 안 씀, 개선 전 02가 씀), python-dotenv 1.2.3, numpy 2.5.3(`InMemoryVectorStore` 코사인 계산). 새 커널 `nbclient==0.11.0`·`ipykernel==7.3.0`, Linux aarch64 Python 3.12.13
- **임베딩 모델**: `text-embedding-3-small`(API), 기본 벡터 길이 1536(OpenAI Embeddings 안내 2026-09-17 확인 + 01 출력), 요금 100만 토큰당 0.02달러(모델 안내 2026-09-17 확인). `config.yaml`의 가격 주석 확인일은 2026-09-07(실습 폴더 파일이라 고치지 않음)
- **execute.py 작업 폴더 = 프로젝트 맨 위**: 01 경로 후보는 첫째(`labs/data/…`)가 골라집니다. 결과 읽기에 그렇게 밝혔고, `notebooks`(셋째)·실습 폴더 맨 위(둘째)는 `test -f`로만 확인
- Mermaid 렌더만 따로: `PUPPETEER_CACHE_DIR=/tmp/pptr-cache LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu python3 textbook/_notebook/mermaid/render_mermaid.py textbook/part3/ch09-rag-first-run --only NN-`. 렌더 도장 지우지 않음(같은 mmd는 `--force`). 칸 안 노드를 칸 밖 노드와 이으면 칸 방향(`direction LR`)이 무시됨 → 칸끼리 잇기(`INDEX --> ASK`)
- `visual.cjs`: `/tmp/ch09-01/vis/vis.cjs`(`require('/tmp/pw/node_modules/playwright')` 사본) + HTML을 `/tmp/ch09-01/html/`에 복사 → `cd /tmp/ch09-01/vis && LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu node vis.cjs /tmp/ch09-01/html`
- 삽화: 기기 셸 `curl` + `/tmp/ch09-01/resize.py`(폭 1100)·`cmp.py`(채택 job 결과와 픽셀 대조). Higgsfield 잔액 2830(01 뒤)
- `run_section.sh`는 「오늘 볼 그림」 PNG가 없으면 첨부 단계에서 멈추므로 `.mmd`를 먼저 두고 실행. 기기 루트 여유 약 590MB
- **옛 생성기 없음**: 이 챕터 `labs/`·`textbook/`에 `make_*.py`·`_make_notebooks.py`가 없습니다(01에서 `find`). 막는 줄 넣을 대상 없음
- 개선 전 QA 스크립트 `qa/check_content.py`·`qa/test_notebook_migration.py`·`qa/test_build.py`는 개선 전 본문·노트북 기준(실행하지 않음, 챕터 마감 때 확인)

### runs 파일

- 01은 `runs/`를 읽지도 쓰지도 않았습니다. Ch 8 06·Ch 7 08·Ch 6 06 사슬 파일(끝 `125fc147…58ad`)도 읽지 않았습니다
- 이 챕터 runs를 쓰는 곳은 개선 전 06(`runs/continuity-ch09-search.jsonl`·`runs/continuity/`)입니다. 읽는 쪽: `textbook/qa/check_course_continuity.py` 94행, `textbook/part3/qa/check_continuity.py` 60·75행, Ch 11 06 노트북(`labs/part3/continuity-guide.md`). `textbook/qa/run_course_bundle.py` 26행은 **02 노트북**을 실행 목록에 둡니다 → 02 작업자는 그 스크립트가 02에서 무엇을 기대하는지(파일 이름 등) 읽고 확인해 주세요(01에서는 목록만 확인)
- 개선 전 02~05 노트북에는 `runs` 글자가 없습니다(`grep -c`, 01 작업 때). `run_course_bundle.py`는 실습 묶음 zip(`textbook/downloads/llm-practice.zip`)을 풀어 02 노트북을 실행하는 전체 마감용 검사입니다

### 01에서 새로 가르친 것

- **Python 모양**: 라이브러리 객체에 키워드 인자와 딕셔너리 리터럴(`Document(page_content=…, metadata={…})`), 반복문 안 카운터 `page_number = page_number + 1`, 글 `split("\n")`로 줄 나누기 + `in`, 글 슬라이싱 뒤 메서드 하나(`hit.page_content[:20].replace("\n", " ")`), 변수만 넣은 f-string(`f"[{doc_id} p.{page}]"`, Part 1 L1 — 01 첫 사용 자리에 「Ch 2 01절」로 잇기), `len(딕셔너리)`, 목록 `==` 없이 `assert len(hits_k1) == 1`, 후보 경로 `for`+`break`(Ch 8 06 모양), 함수 `find_cited_marks(answer_text, marks)`(본문 5줄, Ch 8 02 `find_cited_notes` 모양). 쓰지 않은 것: `Path`·`enumerate(start=)`·`join`·`raise`·try·내포식·`any()`·조건 표현식·`lambda`·`+=`·`@`·`BaseModel`·타입힌트·반복문 안 요청·모델 문장 `assert`
- **API(노트북에서 실행한 것만)**: `from pypdf import PdfReader`·`PdfReader(경로)`·`reader.pages`·`page.extract_text()` / `from langchain_core.documents import Document`·`page_content`·`metadata` / `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)`·`split_documents(Document 목록)` / `OpenAIEmbeddings(model="text-embedding-3-small")`·`embed_query(글)` → 숫자 1536개 목록 / `InMemoryVectorStore.from_documents(문서 청크 목록, 임베딩 객체)`·속성 `store`(딕셔너리, 개수만) / `store.similarity_search(질문, k=2)` → Document 목록(안에서 `embed_query` 후 코사인 유사도 큰 순서, langchain-core 1.6.2 소스). **점수(`similarity_search_with_score`)는 01에서 쓰지 않았습니다**(03 차례). `os.path.exists`
- **이어 쓸 이름과 값**: `candidates`·`pdf_path`, `reader`, `page_two_text`(2쪽 905자), `pages`(Document 5개, 메타데이터 `{'doc_id': 'E01', 'page': N, 'source': 'E01.pdf'}`), `splitter`·`chunks`(8개: 1|45, 2|498, 2|452, 3|498, 3|462, 4|492, 4|412, 5|270), `embedding_model`, `question_text = "미르시립도서관의 정기 휴관일은 언제이고, 공휴일이 월요일과 겹치면 어떻게 되나요?"`(Ch 8 `closure_question`과 같은 글, 45자), `question_vector`(1536), `store`, `hits`(k=2: `[E01 p.1]` 표지 45자 1위, `[E01 p.2]` 498자 2위 — 휴관 문장은 2위 안), `hit_marks = ['[E01 p.1]', '[E01 p.2]']`, `hits_k1`·`marks_k1 = ['[E01 p.1]']`, `persona_text = "당신은 미르시립도서관 안내 담당자입니다."`(Ch 8과 같음), `task_text = "주어진 근거에 있는 정보만 쓰세요. 두 문장 이내로 답하고, 문장마다 끝에 근거 앞에 붙은 출처 표시를 그대로 적으세요."`(**Ch 8 글에서 출처 예시 `[E01 p.2]`를 뺌** — 검색이 출처를 고르므로), `evidence_text`(출처 표시 + 빈칸 + 본문 + `"\n\n"` 반복), `user_text = evidence_text + "질문: " + question_text`, `messages`(system·developer·user), `response`·`answer_text`, `find_cited_marks`, `before_user_text = "질문: " + question_text`·`before_messages`·`before_text`, `after_text`
- **출력 라벨**: 「pypdf:」 등 버전 7줄, 「PDF를 찾았는가:」「고른 경로:」「쪽 수:」「2쪽 글자 수:」「2쪽에서 「휴관」이 든 줄:」「Ch 8 글 「정기 휴관일입니다」가 있는가:」「Document 수:」「2쪽 메타데이터:」「문서 청크 수:」「문서 청크(쪽 | 글자 수):」「질문 글자 수:」「질문 벡터의 숫자 개수:」「앞 숫자 세 개:」「벡터스토어에 넣은 문서 청크 수:」「k=2 검색 결과(출처 | 글자 수 | 앞 20자):」「k=2 출처:」「k=1 출처:」「페르소나:」「과업 명세:」「메시지 수:」「user 글:」「답:」「답에 「월요일」이 있는가:」「답에 쓰인 검색 출처:」
- **실행값(2026-09-17 두 번째 새 커널)**: 위 값 + 8절 답 「미르시립도서관의 정기 휴관일은 매주 월요일입니다. 공휴일이 월요일과 겹치면 그 다음 날인 화요일에도 휴관합니다. [E01 p.2]」(출처는 끝에 한 번, 「법정 공휴일에도 휴관」 없음), Before 답 「…매주 월요일입니다. (근거) 공휴일이 월요일과 겹치면 휴관하고, 그 다음 날인 화요일에 휴관합니다. (근거)」·`[]`, After 답 「…매주 월요일입니다. 법정 공휴일이 월요일과 겹치면 그 다음 날인 화요일에도 휴관합니다. [E01 p.2]」·`['[E01 p.2]']`. 첫 새 커널 Before는 「[출처: 미르시립도서관 이용안내]」를 지어 적음(교재에 안 실음). 결론은 「답을 원문의 어느 쪽과 대조할 수 있는가」까지, 두 답 공통 「월요일」은 효과로 쓰지 않음
- **E01 PDF 추출 글(Ch 8 인계 (3) 확인 결과)**: pypdf 6.17.0 `extract_text()`는 2쪽에서 「매주 월요일은 정기 휴관일 입니다.」(띄어 씀), 「… 그 다음 날인」/「화요일에도 휴관합니다.」(줄바꿈), 「규모」/「이며」·「메이커 스」/「페이스」(낱말 중간 줄바꿈), 구역 표는 `|` 없이 빈칸으로 이어진 줄, 3쪽 「영상 자료 2점 입니다」·「7일 연장 할 수 있습니다」·「대출이 정지 됩니다」, 쪽 끝에 쪽 번호 한 줄(`2`). **Ch 8 글(사람이 고친 글)과 「같은 글」이라고 쓰지 말고 출력으로 확인**. 01은 `"정기 휴관일입니다" in page_two_text` → `False`로 보여 줌
- **데이터 출처**: `labs/data/rag-corpus/pdf/easy/E01.pdf`(5쪽, 1쪽 표지 45자). 실습 자료 폴더 PDF 21건(easy 6·medium 6·hard 6·scanned 3, `ls` 확인). 01은 5쪽 전체 색인
- **비유**: 똑같은 나무 책상 두 개(Ch 7·8 색 약속 — 파란 명찰 = system 페르소나, 주황 클립보드 = developer 과업 명세, 노란 메모지 = 질문, 빈 답안지와 연필 = 답 자리), 오른쪽 책상에만 흰 카드 두 장(= user 글에 넣은 검색 근거), 책상마다 앞 바닥에 흰 카드가 한 줄로 꽂힌 긴 나무 상자(= 벡터스토어, Ch 8 01-5처럼 책상 밖 = 요청에 안 들어감), 왼쪽 상자 꽉 참(검색 안 함) / 오른쪽 상자 빈칸(검색이 고름). 본문 이름 「카드가 꽂힌 긴 상자」(「카드 상자」 단독은 Ch 4, 「기록 카드 상자」는 Ch 8 02). 일상 예: 오픈북 시험(RAG), 긴 공지문을 문단 카드 몇 장에 나눠 옮기기(문서 청크). 개선 전 02 비유 「사서가 책을 색인 카드로 옮기기·카드 구석 메모 = metadata」는 01 카드와 이어 쓸 수 있음(「색인 카드」라는 말은 01 「색인(indexing)」과 뜻이 겹치니 확인)
- **그림 색(01)**: 코드가 만든 자료·넣은 글(PDF·Document·문서 청크·벡터스토어·질문·user 글) 초록, 코드 단계(`PdfReader`·스플리터·`similarity_search`) 파랑, 실행한 서비스 모델 두 개(`text-embedding-3-small`·`gpt-5.4-mini`) 보라, 출력으로 확인한 값(검색 결과·답·k=1 결과) 노랑, 두 조건 공통 값 회색, 빨강은 Before 결함 결과 한 상자. subgraph = 「칸」
- **02절이 이어받을 연결**: 01 b8 「02절에서는 이 흐름의 앞 두 단계인 PDF 읽기와 문서 청크 나누기를 더 자세히 봅니다. 01절에서 본 표지 45자 문서 청크처럼, 나누는 방법이 검색 결과에 어떤 문서 청크를 남기는지와 이어집니다.」(노트북 정리 끝은 첫 문장만). 개선 전 02 `_src` 69행이 이미 「표지 한 쪽이 45자짜리 Document가 됩니다. 검색에서 제목 단어와 겹치면 높은 점수를 받아 자리를 차지합니다(03절)」라고 적음 → 01 k=2 1위 표지 결과와 맞음(01은 점수 숫자를 출력하지 않았으니 「점수」는 03 출력으로). 개선 전 02 b3 「PDF 파싱은 Ch 9 01절에서 처음 도입」은 개선된 01과 맞음. 02가 2쪽 하나만 읽는다면(`reader.pages[1]`) 01 `pages[1]`·2쪽 문서 청크 498/452와 같은 값인지 출력으로 확인
- **개선 전 02 노트북이 쓰는 것 중 01·Part 1·2에서 안 가르친 것**: `from pathlib import Path`·`Path.cwd().resolve()`·`start.parents`·`folders.extend`·`/` 경로 연산·`relative_to()`, `enumerate(chunks, start=1)`, f-string 안 계산(`f"PDF가 없습니다: {pdf_path}"`은 변수만이라 허용, 복잡한 것 확인), 내포식 `[chunk.page_content for chunk in …]`, 제너레이터 식 + `any()`, try `else`·`raise AssertionError`, 글 곱하기(`"가나다…" * 3`), `print` 인자 여러 개에 영어 라벨 섞임, `%pip install`에 `tiktoken`(01은 안 씀 — 02에서 임베딩 토큰화 규칙 `cl100k_base`를 보인다면 Ch 8 01 `encoding_for_model`·`o200k_base`와 규칙이 다르다고 한 문장)
- **아직 안 가르친 것(02가 설명 없이 전제하면 안 됨)**: Ch 8 요약 §5 전체 + 01에서도 안 한 것: 검색 점수(`similarity_search_with_score`)·점수 해석(03), 표지 거르기·최소 길이, 글자 수 대신 토큰 수로 나누기(`from_tiktoken_encoder`·`TokenTextSplitter`), `split_text`, 구분자 목록 `separators`, 겹침 효과(01은 50을 그대로 썼을 뿐), `chunk_id`, LangChain PDF 로더 클래스, 벡터스토어 파일 저장·다시 불러오기, 여러 PDF 색인, 임베딩 비용 계산, 문서 청크 벡터 길이 직접 확인, 모델에게 출처 형식 강제(구조화 출력), 답 정확성 판정·검색 지표(Ch 11), `Path`·`any()`·내포식·`enumerate(start=)`·`join`·`raise`·try `else`

## §02 → §03

(02절 품질 개선 2026-09-17. 결과는 `02-diagnosis.md`, 게이트 G1~G7 0(수정 전 G1 4·G5 10·G6 26·G7 3 = 43), 코드 셀 19(준비 2), **서비스 요청 0번**(모델·임베딩 없음, API 키 없이 실행), 새 커널 세 번(출력 결정적). 삽화 02-5 채택(2차 job `5c628a59-…`, 4크레딧, 잔액 2826), Mermaid 4장. 실습 폴더 테스트 전후 `10 passed`, `runs/` 읽기·쓰기 0)

### 빌더·검증에서 바뀐 것

- **`_build.py` `SECTIONS` 02 제목**을 「PDF가 청크가 되기까지」 → 「PDF가 문서 청크가 되기까지」로 고쳤습니다(규격 §4). 그래서 **01·03 HTML의 이전/다음 링크 한 줄이 바뀝니다**(새 제목을 옛 제목으로 되돌리면 작업 전 해시와 같음을 확인). 03 작업자는 03 제목 「03 · 임베딩·벡터스토어·top-k 검색」을 바꾸면 02·04 HTML 링크 줄이 같은 방식으로 바뀐다는 것만 알고 전후 해시를 비교하면 됩니다. 02 뒤 해시 기준: `/tmp/ch09-02/hash/after02b.txt`(04·05·06·index는 01 뒤와 같음)
- verify는 §01 → §02와 같은 명령(`verify.py --chapter`)으로 02 뒤 `PASS 6 sections / 79 code cells (max 25 lines)`. `grep -c "{{" 02-*.html` 0. `visual.cjs`는 `/tmp/ch09-01/vis/vis.cjs`에 HTML 사본 폴더(`/tmp/ch09-02/html`)를 넘겨 1280·390 PASS
- 서비스 요청이 없는 절이라 설명을 고칠 때 재실행해도 출력이 같았습니다(03은 임베딩 요청이 있으니 규격 §3대로 설명만 고칠 때는 `mdpatch.py` → `--no-exec`)
- `textbook/qa/run_course_bundle.py`는 zip 안 02 노트북을 `notebooks` 폴더에서 실행 → 셋째 후보 경로(`../../../data/…`)가 있음을 `test -f`로 확인. 스크립트는 02의 파일 이름·출력 값을 읽지 않고 PASS·검증 메타데이터만 봄

### 02에서 새로 가르친 것(노트북에서 실행한 것만)

- **API·동작**: 로더 개념을 직접 만든 함수로(`load_pdf_pages`), `type(값)` 출력(`<class 'str'>`·`<class 'dict'>`), `"\n\n" in 글`(빈 줄), 목록 슬라이싱 `[-2:]`·`[:2]`·`[:3]`, `RecursiveCharacterTextSplitter(chunk_size=…, chunk_overlap=…)` 크기·겹침 바꾸기(500/50, 300/50, 380/50, 380/100), `tiktoken.encoding_for_model("text-embedding-3-small")` → `cl100k_base`, 같은 문서 청크를 `gpt-5.4-mini` 규칙 `o200k_base`로 세기
- **설치판 소스로 확인해 본문에 쓴 것**(langchain-text-splitters 1.1.2): 끊을 자리 순서 빈 줄 → 줄바꿈 → 빈칸 → 글자 하나(기본 `["\n\n", "\n", " ", ""]`), 길이는 `len`(글자 수), **겹침은 줄을 쪼개지 않고 앞 문서 청크 끝에서 겹침 안에 드는 줄만 다시 넣음(최대값)**, 메타데이터는 문서 청크마다 복사(`deepcopy`), 크기보다 긴 줄은 다음 구분자로 다시 나눔(E01에서는 실행 안 됨). langchain-openai 1.6.0 `OpenAIEmbeddings`는 `tiktoken_enabled=True`·`check_embedding_ctx_length=True`라 보내기 전에 `cl100k_base`로 토큰화, `embedding_ctx_length` 기본 8191. `from_tiktoken_encoder()`·`TokenTextSplitter`는 있다고만 적음(실행 안 함)
- **용어 표(02)**: 로더(loader), 스플리터(text splitter), 크기(chunk size, 최대 글자 수), 겹침(chunk overlap, 이웃 문서 청크가 함께 갖는 글의 최대 글자 수, 줄 단위), 끊을 자리 순서(separators). 「구분자」라는 말은 쓰지 않았습니다. 「색인 카드」도 쓰지 않음(01 「색인」과 겹침)
- **Python 모양**: 함수가 라이브러리 객체를 만들어 목록 반환(본문 9줄), 함수 안 반복문 카운터, `print` 인자에 `type(…)`, 목록 슬라이싱을 `print` 인자와 `for`에. 쓰지 않은 것: f-string(02는 0건)·`Path`·`enumerate(start=)`·`join`·`raise`·try·내포식·`any()`·조건 표현식·`lambda`·`+=`·`@`·`BaseModel`·타입힌트

### 이어 쓸 이름과 값

- 01과 같은 코드·값: `candidates`·`pdf_path`(교재 출력 `labs/data/rag-corpus/pdf/easy/E01.pdf`), `pages`(Document 5개, 메타데이터 `{'doc_id': 'E01', 'page': N, 'source': 'E01.pdf'}`), `splitter`·`chunks`(500/50, 8개: 1\|45, 2\|498, 2\|452, 3\|498, 3\|462, 4\|492, 4\|412, 5\|270)
- 02에서 새로: `load_pdf_pages(pdf_path, doc_id)`(목록 반환, `source` = `doc_id + ".pdf"`), `encoding`(= `cl100k_base`, **바깥 이름** — Ch 8 01 `count_tokens(text)`와 같은 코드가 읽음), `embedding_model_name = "text-embedding-3-small"`(01의 임베딩 **객체** 이름은 `embedding_model` — 03에서 둘을 섞지 않기), `answer_encoding`(`o200k_base`), `small_splitter`·`small_chunks`(300/50, 14개), `closure_keep_words = ["월요일", "법정 공휴일", "화요일"]`(Ch 8 03과 같음), `find_missing_words(text, words)`(Ch 8 03과 같은 코드), `before_splitter`·`before_chunks`(380/50, 11개), `after_splitter`·`after_chunks`(380/100, 11개)
- **토큰 수(`cl100k_base`)**: 1\|45\|48, 2\|498\|491, 2\|452\|421, 3\|498\|431, 3\|462\|412, 4\|492\|467, 4\|412\|387, 5\|270\|228. 2쪽 첫 문서 청크 `o200k_base` 330. 300자 2쪽: 242\|237, 283\|274, 269\|248, 191\|179
- **쪽 글 모양**: 쪽마다 `1|45|5`, `2|905|26`, `3|925|25`, `4|871|26`, `5|270|9`(쪽 \| 글자 수 \| 줄 수), 다섯 쪽 모두 빈 줄 없음, 마지막 줄 = 쪽 번호 숫자. 2쪽 500/50 경계에서 다시 넣은 두 줄 `['구역 평일 주말 비고', '종합자료실(2층) 09:00~22:00 09:00~18:00']` 합 44자. 2쪽 휴관 조건 두 줄: 56자 `매주 월요일은 정기 휴관일 입니다. 법정 공휴일에도 휴관하며, 공휴일이 월요일과 겹치면 그 다음 날인` / `화요일에도 휴관합니다.`
- **Before/After 값**: 380/50 2쪽 `370 | ['화요일']`·`351 | ['월요일', '법정 공휴일']`·`191 | [세 말 모두]`, 380/100 2쪽 `370 | ['화요일']`·`369 | []`·`319 | [세 말 모두]`, 문서 청크 수 11 \| 11. 500/50에서는 498자 문서 청크 하나에 휴관 세 말이 모두 있음(탐색 출력, b7). 탐색: 세 말을 모두 가진 문서 청크가 없던 설정은 130/0·140/0·160/50·370/0·370/50·380/0·380/50뿐(`/tmp/ch09-02/probe2.py`)
- **출력 라벨**: 「pypdf:」「langchain-core:」「langchain-text-splitters:」「tiktoken:」「PDF를 찾았는가:」「고른 경로:」「Document 수:」「2쪽 메타데이터:」「본문 자료형:」「메타데이터 자료형:」「쪽 글(쪽 \| 글자 수 \| 줄 수 \| 빈 줄이 있는가 \| 마지막 줄):」「2쪽에서 「:00~」가 든 줄:」「문서 청크 수:」「문서 청크(쪽 \| 글자 수 \| 메타데이터):」「앞 문서 청크의 마지막 두 줄:」「뒤 문서 청크의 처음 두 줄:」「다시 넣은 두 줄의 글자 수 합:」「임베딩 모델 이름:」「토큰화 규칙 이름:」「문서 청크(쪽 \| 글자 수 \| 토큰 수):」「답 모델 토큰화 규칙 이름:」「2쪽 첫 문서 청크의 토큰 수(답 모델 규칙):」「500자 문서 청크 수:」「300자 문서 청크 수:」「300자로 나눈 2쪽 문서 청크(글자 수 \| 토큰 수):」「2쪽 문서 청크(글자 수 \| 빠진 지킬 말):」「앞 문서 청크의 마지막 줄:」「뒤 문서 청크의 첫 줄:」「앞 문서 청크 마지막 줄의 글자 수:」「문서 청크 수(Before \| After):」「뒤 문서 청크의 처음 세 줄:」「빠진 지킬 말:」
- **비유·삽화**: 02-5 나무 책상 왼쪽 긴 종이(Document 한 쪽)·오른쪽 같은 크기 흰 카드 세 장(문서 청크)·모든 종이와 카드의 같은 초록 스티커(메타데이터 복사)·이웃 카드 경계의 노란 형광 띠 짝(겹침). 본문에 「이 카드들은 03절에서 01절의 카드가 꽂힌 긴 상자, 곧 벡터스토어에 들어갑니다」와 「Ch 8 03-5 초록 형광 띠(지킬 말)와 달리 노란 띠는 겹침」을 적음 → 03 삽화는 01-5 「카드가 꽂힌 긴 상자」(= 벡터스토어)와 이 카드(= 문서 청크)를 이을 수 있음. 일상 예: 두꺼운 안내 책자를 쪽마다 펼쳐 옮겨 적기(로더), 긴 공지문을 크기가 같은 문단 카드에 나눠 옮기기(스플리터, 01과 같음), 앞 카드 마지막 줄을 다음 카드 첫머리에 한 번 더 적기(겹침)
- **그림 색(02)**: 코드가 만든 자료(PDF·쪽 글·Document·문서 청크) 초록, 코드 단계(`load_pdf_pages`·스플리터 규칙) 파랑, 출력으로 확인한 값 노랑, 실행 안 한 단계(03절 임베딩) 회색 점선, xychart 막대 `#f59e0b` 주황(글자 수)·선 `#22c55e` 초록(토큰 수), 빨강은 02-4 Before 결함 결과 한 상자, 두 설정 공통 값 회색 상자. 보라 없음(모델 안 부름). subgraph = 「칸」

### 03절이 이어받을 연결과 확인할 것

- 02 b8·노트북 정리 끝: 「03절에서는 나눈 문서 청크를 임베딩해 벡터스토어에 넣고 검색하는 단계를 봅니다. 01절 k=1 표지 결과처럼, 어떤 문서 청크가 가까운 순서로 올라오는지와 이어집니다.」(노트북은 첫 문장만, 「더 자세히 봅니다」). 점수(`similarity_search_with_score`)는 01·02 모두 쓰지 않았습니다
- **개선 전 03 노트북**: 짧은 Document 세 건(`D01` 도서관 휴관·`D02` 해솔식당·`D03` 별빛회사 급여, 메타데이터 `doc_id`만), 임베딩 객체 이름 `embedding`(01은 `embedding_model`), `InMemoryVectorStore(embedding=…)` + `add_documents()`(01은 `from_documents()`), `similarity_search_with_score`·`round(score, 3)`, 튜플 풀기 `for document, score in hits`, Before/After `combined_query` k=1 → k=2에 내포식·`issubset`·try `else`·`raise AssertionError`. 01·02가 E01 5쪽·문서 청크 8개·`[E01 p.N]`으로 이어 왔으니, 03이 D01~D03 합성 문장을 유지할지 E01 문서 청크로 바꿀지 결정이 필요합니다(학습 질문·paired 형식은 유지). E01로 바꾸면 01 b7에 적은 탐색 점수(표지 0.5832, 2쪽 첫 문서 청크 0.5748, 차이 0.01 미만)가 03 출력으로 다시 보일 수 있으니 출력으로 확인
- 02에서 겹침으로 휴관 조건을 모은 380/100 설정은 흐름을 보여 주는 예입니다. 03이 색인 설정을 새로 쓸 때 01과 같은 500/50을 쓰면 「01절과 같은 설정」으로 이으면 됩니다(500/50에서도 휴관 세 말은 498자 문서 청크 하나에 있음)
- 임베딩 요청이 문서 청크 수와 글 길이에 따라 늘어난다는 문장(02 b5·b6 「임베딩할 글이 늘어납니다」)은 02가 요청을 보내지 않고 쓴 말입니다. 03에서 임베딩 토큰·비용을 숫자로 말하려면 03 출력(또는 `count_tokens` 합)으로
- **아직 안 가르친 것(03이 설명 없이 전제하면 안 됨)**: §01 → §02 목록에서 02가 가르친 것(로더·스플리터 규칙·겹침·글자 수와 토큰 수)을 뺀 나머지 전부. 특히 검색 점수·점수 해석, 튜플 반환 목록 풀기 `for a, b in …`(Ch 2 01~03 튜플 풀어 담기는 배움 — 모양이 다르면 한 문장), `round()`(Ch 2 04), `add_documents()`, 벡터스토어 저장·다시 불러오기, 여러 PDF 색인, `chunk_id`, 표지·쪽 번호 줄 거르기, 토큰 기준 스플리터, 내포식·`issubset`·`set` 연산(`set()`은 Ch 2 03에서 배움, 메서드 `issubset`은 처음), try `else`·`raise`
- 챕터 마감 때 볼 것(02에서 넘김): `_src/index.html` 02 행 「PDF 한 쪽 … 청크 크기 변경」·「청크 경계 도식」과 새 용어 줄의 「청크」, 옛 도식 `figures/02-청크-경계.svg/.excalidraw`(정리 대상), 개선 전 QA `qa/check_content.py` 29행·`qa/test_notebook_migration.py` 77행(02 전용 조건)

### 실행 환경(02에서 확인)

- 기기 루트 여유 약 580MB(02 뒤). 작업 폴더 `/tmp/ch09-02`(probe·삽화 원본·html 사본·해시)
- tiktoken 규칙 파일은 새 커널에서 처음 한 번 내려받음(기기 셸 `tempfile.gettempdir()` = `$HOME/tmp`, `/tmp/data-gym-cache` 아님). 내려받기는 기기 허용 목록에서 동작
- 삽화: 1차 탈락 원인은 「같은 줄」 띠의 길이가 달라 짝이 안 읽힘·색인 카드의 붉은 줄. 2차 프롬프트에 줄 수·띠 자리·「모든 띠 길이·색 같음」·「red lines 없음」을 적어 통과(`figures/02-5-공지문과-문단-카드.prompt.md`)

## §03 → §04

(03절 품질 개선 2026-09-17. 결과는 `03-diagnosis.md`, 게이트 G1~G7 0(수정 전 G1 2·G5 10·G6 19·G7 3 = 34), 코드 셀 21(준비 3), **서비스 요청 6번 = 모두 임베딩 `text-embedding-3-small`, 답 모델 0번**, 새 커널 두 번(구조 같음, 점수 소수 넷째 자리만 다름 → 두 번째 출력으로 설명을 `mdpatch.py`로 맞춤). 삽화 03-5 채택(2차 job `3b5bed77-…`, 4크레딧, 잔액 2822), Mermaid 4장. 실습 폴더 테스트 전후 `10 passed`, `runs/` 27개 파일 해시 전후 같음(읽기·쓰기 0), 다른 절 HTML 해시 같음)

### 결정 두 가지 (04~06이 따를 것)

- **데이터**: 개선 전 03 합성 문장 D01~D03(도서관·해솔식당·별빛회사)은 쓰지 않고 01·02와 같은 **E01 5쪽 → 500/50 문서 청크 8개**로 이었습니다(근거는 `03-diagnosis.md` 「데이터 결정」). 개선 전 04 노트북도 짧은 합성 Document 두 건(`D01` 휴관 p.1·`D02` 대출 p.2)을 씁니다 → 04가 E01 문서 청크로 바꾸면 01 8절(검색 근거 → 메시지 목록 → 답·`find_cited_marks()`)과 03 Before 두 가지 질문을 이어 쓸 수 있습니다
- **임베딩 이름**: 객체 `embedding_model`(01과 같음), 모델 이름 글 `embedding_model_name = "text-embedding-3-small"`(02와 같음). 01은 이미 `embedding_model`이라 01 코드·설명은 바꾸지 않았습니다(mdpatch 없음). **개선 전 04·05·06 노트북은 `embedding`** → 개선 때 `embedding_model`로 통일(`grep -n "embedding = \|embedding=embedding" labs/part3/ch09-rag-first-run/notebooks/0[456]-*.ipynb`로 자리 확인). 실습 폴더 모듈 `rag.py`·`harness.py`의 이름은 노트북과 따로입니다(03은 읽지 않음, 04~06이 쓰면 확인)

### 03에서 새로 가르친 것(노트북에서 실행한 것만)

- **API**: `InMemoryVectorStore(embedding=embedding_model)`(빈 벡터스토어, 요청 없음), `store.add_documents(chunks)` → 저장 ID 목록(요청 1번, uuid4 무작위 글 — 실행마다 다름, 인용 안 함), 속성 `store.store`(저장 ID를 키로 삼는 딕셔너리, 항목 키 `id`·`vector`·`text`·`metadata`), `embedding_model.model`(모델 이름), `store.similarity_search_with_score(질문, k=…)` → (Document, 점수) 튜플 목록, 검색 결과 Document 속성 `id`(= 저장 ID), `embed_query()`(01에서 배움). **점수 = 질문 벡터와 저장 벡터의 코사인 유사도, 큰 순서**(langchain-core 1.6.2 소스, numpy — simsimd 없음)
- **설치판 소스로 확인해 본문에 쓴 것**: `from_documents()` = 빈 벡터스토어 + 넣기 같은 순서, 문서 청크 벡터는 넣을 때 한 번만 만들고 검색 때는 질문만 임베딩(`similarity_search_with_score` = `embed_query` + by_vector), `ids`를 안 주면 uuid4, `dump()`·`load()` 있음(실행 안 함), langchain-openai 1.6.0 `embed_documents`는 여덟 글을 한 요청으로(`chunk_size` 1000), `embed_query` = `embed_documents([text])[0]`. OpenAI Embeddings 안내(2026-09-17): 기본 1536·`dimensions`·「길이 1로 맞춘 벡터」(b7에 「이번에 확인하지 않음」)
- **Python 모양**: 튜플 목록을 `for hit, score in scored_hits:`로 나눠 담기(Ch 5 02 [36] `for first_sentence, second_sentence in …` 모양이라고 설명), `round(score, 4)`(Ch 2 04, Ch 5 02 모양), 딕셔너리 `keys()` 출력, `type(목록[0])`, 반복문 안 순위 카운터 `rank = rank + 1`, 아주 작은 수 `round(raw_cost, 7)` → `5.77e-05`와 `e-05` 표기 한 문장, 이름 있는 수 `embedding_rate = 0.02`·`tokens_per_million = 1000000`. 쓰지 않은 것: 내포식·`issubset`·try·`raise`·조건 표현식·`lambda`·`+=`·`join`·`Path`·`enumerate`·`zip`·`sum`·`max`·`@`·`BaseModel`·타입힌트·f-string 안 계산·반복문 안 요청·**서비스 값(점수·검색 결과 내용) `assert`**(개수 `len(after_hits) == 3`만)
- **용어 표(03)**: 저장 항목(문서 청크 하나를 넣을 때 생기는 딕셔너리, 저장 ID·벡터·본문·메타데이터), 저장 ID(id), 검색 점수(score, 이 벡터스토어에서는 코사인 유사도). 01 용어(벡터스토어·임베딩·top-k 검색·문서 청크)·Ch 5 코사인 유사도·Ch 8 지킬 말은 같은 뜻으로 이음. 「질문 임베딩」은 그림 라벨로만(용어 표에 없음). 「청크」 단독·「조각」 0건

### 이어 쓸 이름과 값

- 01·02와 같은 코드·값: `candidates`·`pdf_path`, `load_pdf_pages(pdf_path, doc_id)`(02 코드 그대로), `pages`(5), `splitter`·`chunks`(500/50, 8개), `embedding_model_name`·`encoding`(`cl100k_base`)·`count_tokens(text)`(02·Ch 8 01 코드), `embedding_model`, `question_text`(01·Ch 8 휴관일 질문, 45자), `find_missing_words(text, words)`(Ch 8 03·02 코드)
- 03에서 새로: `total_tokens = 2885`(02 4절 여덟 토큰 수 합)·`embedding_rate = 0.02`·`tokens_per_million`·`raw_cost`·`index_cost`(`5.77e-05`), `store`(빈 벡터스토어에 넣음)·`stored_ids`(8)·`stored_item`·`stored_vector`, **`make_source_mark(chunk)`**(메타데이터로 `[E01 p.2]` 글 반환, 본문 4줄 — 01의 f-string 세 줄을 함수로. 04가 출처 표시를 여러 번 만들면 같은 코드로 이어 쓰기), `scored_hits`(k=2), `dot_product(first, second)`·`vector_length(vector)`·`cosine_similarity(first, second)`(**Ch 5 02 [15]·[20]·[22] 셀과 주석까지 같은 코드**, `import math`), `question_vector`, `all_hits`(k=8), `combined_question = "미르시립도서관의 정기 휴관일은 언제이고, 도서는 몇 권까지 빌릴 수 있나요?"`, `combined_keep_words = ["월요일", "7권"]`, `before_hits`·`before_text`·`before_missing`(k=1), `after_hits`·`after_text`·`after_missing`(k=3). 근거 글 = 본문 + `"\n\n"` 반복(01 7절 `evidence_text`는 출처 표시 + 빈칸 + 본문 + `"\n\n"` — 03은 출처 표시를 근거 글에 넣지 않고 출력 줄에만 씀)
- **실행값(2026-09-17 두 번째 새 커널, 교재 출력)**: 저장 항목 키 `dict_keys(['id', 'vector', 'text', 'metadata'])`, 2쪽 첫 항목 메타데이터 `{'doc_id': 'E01', 'page': 2, 'source': 'E01.pdf'}`·본문 앞 20자 `1. 도서관 소개 미르시립도서관은 1`. 휴관일 질문 k=2 `[E01 p.1] | 45 | 0.5833`·`[E01 p.2] | 498 | 0.5748`(01 b7 탐색 「차이 0.01 미만」과 맞음), 직접 계산 같은 값. k=8 순위 p.1 0.5833 · p.2(498) 0.5748 · p.2(452) 0.3833 · p.5 0.3553 · p.3(498) 0.3383 · p.3(462) 0.3367 · p.4(412) 0.3225 · p.4(492) 0.1542. 두 가지 질문 k=1 `[E01 p.2] | 498 | 0.6257`·`['7권']`, k=3 2위 표지 `0.5981`·3위 `[E01 p.3] | 498 | 0.3842`·`[]`. **점수는 실행마다 소수 넷째 자리가 달라짐**(첫 새 커널 1위 0.5832·8위 0.1541 등 — 교재에 싣지 않음). 순위·출처는 두 실행과 탐색 두 번 모두 같았음
- **탐색에서 본 것(04·05 참고, `/tmp/ch09-03/probe1.py`·`probe2.py`)**: 휴관+연장 질문(`…정기 휴관일은 언제이고, 빌린 도서의 대출 기간을 연장할 수 있나요?`)은 1위 표지 0.5832·2위 2쪽 0.5704·3위 3쪽(498) 0.4514. 권수+주차 질문은 1위 2쪽(휴관)·2위 5쪽·…·5위 3쪽(`7권`). 휴관+주차 질문은 1위 2쪽·2위 표지·3위 2쪽(452)·4위 5쪽. 3쪽 498자 문서 청크에 「7권」「14일」「7일 연장」「1회」「예약이 없는 경우」가 모두 있음(pypdf 글 「7일 연장 할 수 있습니다」 띄어 씀). 5쪽 270자 문서 청크에 「30분마다 500원」. 표지 45자는 질문마다 1~4위 안에 들어옴(05 「검색 누락」과 이어질 수 있음, 출력으로 확인)
- **출력 라벨**: 「pypdf:」「langchain-core:」「langchain-openai:」「langchain-text-splitters:」「tiktoken:」「numpy:」「openai:」「OPENAI_API_KEY 설정 여부:」「PDF를 찾았는가:」「고른 경로:」「Document 수:」「문서 청크 수:」「문서 청크(쪽 | 글자 수):」「임베딩 모델 이름:」「토큰화 규칙 이름:」「넣을 토큰 수 합계:」「색인 비용 어림(달러):」「넣기 전 저장 항목 수:」「넣은 뒤 저장 항목 수:」「저장 ID 수:」「첫 저장 ID:」「저장 항목의 키:」「벡터의 숫자 개수:」「메타데이터:」「본문 앞 20자:」「반환값의 원소 수:」「첫 원소의 자료형:」「k=2 검색 결과(출처 | 글자 수 | 점수):」「출처 | 벡터스토어 점수 | 직접 계산한 코사인 유사도:」「k=8 검색 결과(순위 | 출처 | 글자 수 | 점수):」「k=1 검색 결과(출처 | 글자 수 | 점수):」「k=3 검색 결과(출처 | 글자 수 | 점수):」「근거 글에서 빠진 지킬 말:」
- **준비 셀 처리**: 02는 키·모델 없음, 03은 `nbkit.KEY` 준비 셀 하나(모델 셀 없음, `key_and_model_cells()` 안 씀). 실행일 문장은 임베딩 객체 셀 결과 읽기에 「이 임베딩 모델로」. 04는 답 모델을 부르므로 01처럼 `key_and_model_cells()` + 설명 셀 교체 방식
- **비유·삽화**: 03-5 나무 책상 왼쪽 노란 메모지(질문)의 산 모양 회색 막대 줄(질문 벡터), 오른쪽 뚜껑 없는 긴 나무 상자(01-5 벡터스토어)에 흰 카드(문서 청크)가 한 줄, 카드마다 초록 스티커(02-5 메타데이터)와 모양이 다른 회색 막대 다섯 개(벡터), 메모지와 비슷한 산 모양 카드 두 장만 높이 올라옴(k=2). 이 그림은 검색만이라 01-5 책상 물건(명찰·클립보드·답안지)이 없고 상자가 책상 위에 있다고 그림 읽기에 적음 → 04 삽화가 답 받기를 그리면 01-5 책상 색 약속(파란 명찰 = system, 주황 클립보드 = developer, 노란 메모지 = user, 빈 답안지 = 답)과 03 막대 카드를 이을 수 있음. 개선 전 비유 「지도 위의 핀」은 쓰지 않음
- **그림 색(03)**: 문서 청크·저장 항목·질문·질문 벡터·저장 벡터 초록, 실행한 임베딩 모델 보라(01-2와 같음), 검색 단계·정의한 함수 파랑, 출력으로 확인한 점수·빠진 지킬 말 없음 노랑, xychart 점수 막대 `#f59e0b` 주황, 빨강은 03-4 Before 한 상자, 두 조건 공통 값(같은 질문·1위 p.2) 회색 상자. subgraph = 「칸」

### 04절이 이어받을 연결과 확인할 것

- 03 b8·노트북 정리 끝: 「04절에서는 검색한 문서 청크를 출처 표시와 함께 메시지 목록에 넣고 답을 받습니다. 이 절 Before처럼 근거 글에 무엇이 들어갔는지가 답과 출처 표시로 이어집니다.」(노트북은 「…답을 받는 단계를 봅니다」). 03 Before 결과 읽기에도 「근거를 넣어 답을 받는 단계는 04절에서 봅니다」 → 04가 E01·메시지 목록으로 답을 받는지 확인하고, 다르면 03 설명은 `mdpatch.py` → `--no-exec`(재실행 금지)
- **개선 전 04 노트북**: 합성 Document 두 건(`D01` p.1·`D02` p.2), `embedding`, `from_documents`, 질문 「정기 휴관일은 언제인가요?」 k=1, f-string 삼중 따옴표 프롬프트(문자열 하나 `invoke`), `init_chat_model("openai:gpt-5.4-mini", temperature=0)`(`reasoning_effort` 없음), 모델 문장 `assert "월요일" in answer.text`·`assert source_tag in answer.text`, k=2 비교, Before/After = 검색 결과를 새 Document로 옮기며 `page` 빠뜨림 → `KeyError`(try/except) → 고침. 01·03과 이으려면: 01 7절 메시지 목록(`persona_text`·`task_text` 「근거 앞에 붙은 출처 표시를 그대로」·`evidence_text`), 01 `find_cited_marks()`, 03 `make_source_mark()`, 모델 문장 `assert` 대신 검사 함수 출력. `KeyError`는 Before 결함이라 빨강(받아서 출력해도 paired Before 결함 결과 — 규격 §5-3)
- 03이 확인한 「표지 45자가 검색 자리를 차지함」은 04 k 비교·05 검색 누락과 이어질 수 있습니다(출력으로 확인). 03은 답을 받지 않았으므로 「표지가 들어가면 답이 나빠진다」는 쓰지 않았습니다
- 근거 글 길이와 Ch 8 01 입력 가용분: 03 b6 끝에 「근거 글을 메시지에 넣을 때는 Ch 8 01절 입력 가용분 안에 드는지도 함께 봅니다」 한 문장만 적었고 계산은 안 함. 04에서 k를 늘려 입력 토큰을 말하려면 `usage_metadata` 출력으로(`o200k_base`와 임베딩 `cl100k_base` 구분 — 02 결정)
- **아직 안 가르친 것(04가 설명 없이 전제하면 안 됨)**: §02 → §03 목록에서 03이 가르친 것(점수·튜플 나눠 담기·`add_documents`·저장 항목·`id`)을 뺀 나머지. 특히 점수 기준값·거르기(`score_threshold`)·MMR, 벡터스토어 저장·다시 불러오기(`dump`/`load` 실행 안 함), `ids` 지정·`chunk_id`, 여러 PDF 색인, 표지·쪽 번호 줄 거르기, `dimensions`, 다른 임베딩 모델, `similarity_search_with_score_by_vector`, `as_retriever()`, 검색 결과로 답 받기(01 8절에서 한 번만), 개수 2로 두 가지 질문 검색(03은 실행 안 함), 모델 문장 `assert`, 구조화 출력으로 출처 강제, 검색 평가(Ch 11)
- 챕터 마감 때 볼 것(03에서 넘김): `_src/index.html` 03 행(「짧은 Document 세 건, 실제 임베딩, InMemoryVectorStore, k 변경」·「벡터 검색 도식」)과 새 용어 줄 「질문 임베딩」·「청크」, 옛 도식 `figures/03-벡터-검색.svg/.excalidraw`(정리 대상), 개선 전 QA `qa/check_content.py` 20·30행·`qa/test_notebook_migration.py` 9행(03 전용 조건), `runs/examples/ex03_*_preserved.txt`(개선 전 D01~D03 출력, 읽지도 바꾸지도 않음)

### 실행 환경(03에서 확인)

- 기기 루트 여유 약 565MB(03 뒤). 작업 폴더 `/tmp/ch09-03`(probe·삽화 원본·html 사본·해시 `hash/before03.txt`·`after03.txt`·`runs-all-before.txt`)
- 서비스 임베딩 값 변동: 같은 질문 글을 두 번 `embed_query`하면 탐색에서 값이 같았고, 문서 청크를 따로 다시 임베딩하면 최대 0.000458 달랐음 → 새 커널마다 점수 소수 넷째 자리가 바뀔 수 있음. 결과 읽기에 점수를 인용한 절은 마지막 새 커널 출력과 대조(G5가 첫 단락 숫자를 잡음) 뒤 `mdpatch.py`로 맞추고, 조사(「0.5833과」 등)를 함께 확인
- 삽화: 클라우드 Bash `curl`은 스크래치패드에서 동작(검수용 축소본 보기), 저장은 기기 셸 `curl` + `uv run --no-project --with pillow`(`/tmp/ch09-02/resize.py`·`cmp.py`)

## §04 → §05

(04절 품질 개선 2026-09-17. 결과는 `04-diagnosis.md`, 게이트 G1~G7 0(수정 전 G2 1·G5 12·G6 26·G7 3 = 42), 코드 셀 25(준비 3), **서비스 요청 6번 = 임베딩 2(`add_documents` 1·k=3 검색 1) + `gpt-5.4-mini` 4(5절·7절 값 바꿔 보기·Before·After)**, 새 커널 두 번(구조 같음, Before 답 둘째 문장만 달라 두 번째 출력으로 `mdpatch.py`). 삽화 04-5 채택(1회 생성, job `b1d21487-…`, 2크레딧, 잔액 2820), Mermaid 4장. 실습 폴더 테스트 전후 `10 passed`, `runs/` 27개 파일 해시 전후 같음(읽기·쓰기 0), 다른 절 HTML 해시 같음(04만 바뀜), `verify.py --chapter` → `PASS 6 sections / 107 code cells (max 25 lines)`)

### 결정 (05~06이 따를 것)

- **Before 설계**: 개선 전 04 Before(`page`를 빠뜨려 `KeyError`)는 쓰지 않고, 메타데이터 **`source` 키(파일 이름 `E01.pdf`)로 출처를 만든 기록**으로 바꿨습니다. 세 기록 출처가 같아 Ch 8 `check_answer()`가 세 기록을 모두 「답의 출처 표시와 같은 기록」으로 반환합니다(빨강 1상자). 05가 「검색 결과 출처를 함께 보는」 표를 만들 때도 출처는 `doc_id`·`page`로(04 `make_note()`)
- **검사 함수 선택**: 01 `find_cited_marks(answer_text, marks)`(표시 목록) 대신 Ch 8 기록 모양 + Ch 8 02 `find_cited_notes()`·03 `find_missing_words()`·04 `build_notes_messages()`·`check_answer()`를 **같은 코드로**. `check_answer()`만 바깥 지킬 말 이름을 `closure_keep_words` → `combined_keep_words`로 바꿨고(주석·설명 셀에 밝힘), 05가 다른 지킬 말을 쓰면 같은 방식으로 이름만 바꾸고 설명에 적기
- **모델 문장 `assert` 0**: `assert`는 `pdf_path is not None`·`len(hits) == 3`만. 서비스 답의 내용은 결과 읽기에 「이번 실행에서는」으로. 개선 전 05 노트북의 `assert "찾을 수 없습니다" in missed_answer.text`·`assert "대출" in recovered_answer.text`·`assert "정지" in …`와 `assert selected_id == "DISTRACTOR"`(서비스 검색 결과)는 규격 §3 위반 → 뺄 것

### 04에서 새로 가르친 것(노트북에서 실행한 것만)

- **API·동작**: 새 API 없음. `similarity_search(k=3)` 뒤 `hit.metadata` 딕셔너리 통째 출력, `response.usage_metadata["input_tokens"]`(Ch 6 01 뜻), `messages[2][1]`(Ch 8 07 모양). 03처럼 `InMemoryVectorStore(embedding=embedding_model)` + `add_documents(chunks)`
- **새 함수**: `make_note(chunk)` → `{"출처": f"{doc_id} p.{page}", "내용": chunk.page_content}`(본문 4줄)
- **용어 표(04)**: 출처 인용(citation, 답에 근거의 출처 표시를 적어 읽는 사람이 그 근거를 찾아가게 하는 일, 일상 예 「자료: 안내 책자 3쪽」). 「기록」은 Ch 8 04 `build_notes_messages()`가 읽는 키 `출처`·`내용` 딕셔너리 뜻 그대로, 내용이 문서 청크 본문이라는 것만 다름(노트북 3절·b4). 개선 전 「출처 태그」「문맥 조립」「프롬프트」는 쓰지 않음(→ 출처 표시·근거·user 글·메시지 목록). 「청크」 단독·「조각」 0건
- **Python 모양**: 함수가 딕셔너리 리터럴 반환, 두 겹 인덱싱 `messages[2][1]`. 쓰지 않은 것: 내포식·try·`raise`·조건 표현식·`lambda`·`+=`·`join`·`Path`·`enumerate`·f-string 안 계산·반복문 안 요청·`@`·`BaseModel`·타입힌트·구조화 출력

### 이어 쓸 이름과 값

- 01~03과 같은 코드·값: `candidates`·`pdf_path`, `load_pdf_pages(pdf_path, doc_id)`, `pages`(5)·`splitter`·`chunks`(500/50, 8), `embedding_model_name`·`embedding_model`, `store`·`stored_ids`, `persona_text`·`task_text`(01 글), `combined_question`·`combined_keep_words = ["월요일", "7권"]`(03)
- 04에서 새로: `hits`(k=3, 메타데이터 page 2·1·3, 글자 수 498·45·498), `make_note`, `notes`·`note_sources = ['E01 p.2', 'E01 p.1', 'E01 p.3']`, `build_notes_messages`, `messages`·`user_text`, `response`·`answer_text`·`input_tokens`(784), `find_cited_notes`, `find_missing_words`, `check_answer`, `check`, `plain_task_text = "주어진 근거에 있는 정보만 쓰세요. 두 문장 이내로 답하세요."`·`plain_messages`·`plain_text`·`plain_check`, `before_notes`·`before_sources`·`before_messages`·`before_text`·`before_check`, `after_text`·`after_check`
- **실행값(2026-09-17 두 번째 새 커널, 교재 출력)**: 5절 답 「미르시립도서관의 정기 휴관일은 매주 월요일입니다. 도서는 한 번에 7권까지 빌릴 수 있습니다. [E01 p.2] [E01 p.3]」(과업 명세는 문장마다라고 했지만 **두 표시를 끝에 모음** — 01 답도 끝에 한 번), `실제 입력 토큰 수: 784`, `답 검사: {'답의 출처 표시와 같은 기록': ['E01 p.2', 'E01 p.3'], '답에서 빠진 지킬 말': []}`. 6절 기록 내용 대조 `E01 p.2 | ['7권']`·`E01 p.1 | ['월요일', '7권']`·`E01 p.3 | ['월요일']`(결정적). 7절 출처 문장 뺀 답은 표시 없음·`[]`·`[]`. Before `기록의 출처: ['E01.pdf', 'E01.pdf', 'E01.pdf']`(결정적), 답 끝 `[E01.pdf]`, 검사 `['E01.pdf', 'E01.pdf', 'E01.pdf']`·`[]`. After는 5절과 같은 글·같은 검사. 첫 새 커널 Before 둘째 문장 「회원 한 사람은 도서를 …」(교재에 안 실음)
- **출력 라벨**: 「pypdf:」 등 버전 7줄, 「OPENAI_API_KEY 설정 여부:」「모델 이름:」「temperature:」「PDF를 찾았는가:」「고른 경로:」「Document 수:」「문서 청크 수:」「넣은 뒤 저장 항목 수:」「검색 결과 수:」「k=3 검색 결과(메타데이터 | 글자 수):」「기록 수:」「기록의 출처:」「첫 기록의 키:」「페르소나:」「과업 명세:」「메시지 수:」「user 글:」「답:」「실제 입력 토큰 수:」「답 검사:」「기록마다 내용에서 빠진 지킬 말(출처 | 빠진 지킬 말):」「Before 기록의 출처:」「After 기록의 출처:」
- **비유·삽화**: 04-5 나무 책상(01-5 색 약속: 파란 명찰 = system, 주황 클립보드 = developer, 노란 메모지 = 질문, 답안지와 연필 = 답), 가운데 흰 카드 세 장(k=3 근거, 01-5·03-5 카드 = 문서 청크)의 초록 스티커(02-5·03-5 메타데이터) 안 흰 모양 세모·동그라미·네모(= 2쪽·표지·3쪽, 쪽마다 다른 출처), 답안지 두 줄 끝 세모·네모 스티커(출처 표시), 동그라미 없음(표지 안 씀). 그림은 문장마다 스티커 — 실제 답은 끝에 모음이라고 그림 읽기에 적음. 05 삽화가 검색 누락을 그리면 「상자에서 카드가 안 올라옴」(03-5)·「답안지 스티커」(04-5)를 이을 수 있음. 개선 전 05 삽화 `05-지어낸-숫자.png`(안내원·빨간 경고)는 이 계열과 다름
- **그림 색(04)**: 검색 결과·기록·developer 글 초록, 정의한 함수 파랑, `gpt-5.4-mini` 보라, 답·검사 결과·7절 「출처 표시 없음」 노랑, 코드가 확인하지 않은 것(문장-표시 짝, 뜻)·두 조건 공통 값 회색, 빨강은 04-4 Before 한 상자. subgraph = 「칸」

### 05절이 이어받을 연결과 확인할 것

- 04 b8: 「05절에서는 첫 실패를 일부러 만들어 봅니다. 답만 읽지 않고 검색한 문서 청크의 출처를 함께 봅니다. 이 절에서 답의 출처 표시로 기록을 가려낸 것처럼, 답이 이상할 때 먼저 어떤 근거가 들어갔는지 확인합니다.」 노트북 정리 끝: 「다음 05절에서는 답만 읽지 않고 검색한 문서 청크의 출처를 함께 보며, 첫 실패를 일부러 만들어 봅니다.」 → 05가 실제로 출처(검색 결과)를 함께 보는지 확인하고, 다르면 04 설명은 `mdpatch.py` → `run_section.sh … 04 --no-exec`(재실행 금지)
- **05 b3 실패 모드 설명을 Ch 8 04 정의에 맞출 것(Ch 8 요약 §4 (1), 과정 요약 Part 2 §10)**: 개선 전 05 `_src` b3 「Ch 8 실패 모드 Distraction·Confusion — 관련 없는 청크가 프롬프트에 들어오면 모델이 산만해지거나 혼동할 수 있습니다」는 Ch 8 04 정의와 어긋남. Ch 8 04 정의(Breunig 원글, 한국어 이름): **오염**(환각·오류가 컨텍스트에 들어가 뒤에서 되풀이 쓰임, Ch 8은 요청 한 번만 실행), **산만**(아주 긴 컨텍스트에 치우쳐 학습한 것을 덜 씀 — Ch 8 실행 안 함, 컨텍스트 로트와 다름), **혼란**(필요 없는 내용이 컨텍스트에 있어 모델이 그 내용을 답에 써서 답이 나빠짐), **충돌**(새로 쌓인 정보가 다른 정보와 맞지 않음). → 「관련 없는 문서 청크가 목록에 들어오는 조건은 Ch 8 04절 혼란과 이어짐(조건을 넣은 것과 답이 나빠진 것은 따로 적음), 산만은 아주 긴 컨텍스트에 치우치는 경우의 이름이라 이 절과 다름」으로, 영문 Distraction·Confusion 대신 한국어 이름 산만·혼란. Ch 8 04 결론 태도 「혼란 조건을 넣었고 이번 답에서는 보이지 않았다」도 이어 쓰기(`textbook/part2/ch08-context-engineering/_src/04-네-가지-실패-모드.html` 30·47·61·89행)
- **개선 전 05 노트북(합성 문서)**: `DISTRACTOR`(「책을 3일 늦게 반납했습니다. 안내 데스크에 문의하세요.」)·`ANSWER`(「자료를 늦게 반납하면 연체 일수만큼 대출이 정지됩니다.」)·A/S 질문, 임베딩 `embedding`, `from_documents`, `init_chat_model("openai:gpt-5.4-mini", max_tokens=80)`(temperature·reasoning_effort 없음), f-string 삼중 따옴표 프롬프트(문자열 하나 `invoke`), `"\n".join`, 모델 문장·서비스 검색 결과 `assert`, try `except AssertionError`·`else`·`raise`, After가 모델을 다시 부르지 않고 앞 결과를 재출력. 01~04와 이으려면: E01 문서 청크·`load_pdf_pages()`·`embedding_model`·01 메시지 목록·04 `make_note()`/`build_notes_messages()`/`check_answer()`. E01 3쪽 문서 청크(498자)에 「반납 예정일을 넘기면 연체 일수만큼 대출이 정지 됩니다」·「3일 늦게 반납하면 반납일부터 3일 동안 새로 대출할 수 없습니다」가 있음(04 user 글 출력으로 확인, pypdf 띄어쓰기 「정지 됩니다」) → 개선 전 05 연체 질문을 E01 3쪽으로 이을 수 있음(검색 순위는 05 출력으로 확인). 「문서에 답이 없는 질문」은 E01에 없는 내용(예: A/S)을 E01 색인에 물으면 되고, 표지 45자 문서 청크가 자리를 차지하는 03 관찰과 이어질 수 있음(출력으로 확인)
- 03 탐색 참고(handoff §02 → §03 끝): 휴관+주차 질문 1위 2쪽·2위 표지·3위 2쪽(452)·4위 5쪽, 권수+주차 질문은 「7권」 문서 청크 5위. 05에서 k를 줄여 근거가 빠지는 장면을 만들 때 이 순위를 출력으로 다시 확인하고, 질문·k를 탐색 뒤 정하면 b7에 과정과 「흐름을 보여 주려고 정한 예」(규격 §3)
- 04 b7에 적은 검사 한계(05가 「실패를 나눠 읽기」에 쓸 수 있음): 표시 검사는 표시가 답 어딘가에 있는지만, 같은 표시를 가진 기록은 모두 맞음, 지킬 말 검사는 말만(뜻은 원문), 목록에 없는 표시(Ch 8 04 Before)는 이번에 안 나옴, 구조화 출력으로 표시 강제는 실행 안 함
- **아직 안 가르친 것(05가 설명 없이 전제하면 안 됨)**: §03 → §04 목록에서 04가 가르친 것(검색 결과로 답 받기·출처 검사)을 뺀 나머지. 특히 점수 기준값·거르기(`score_threshold`)·MMR, 벡터스토어 저장·다시 불러오기, 여러 PDF 색인, 표지 거르기, `as_retriever()`, 구조화 출력, 검색 평가·답 정확성 판정(Ch 11), LLM 판정자(Ch 15), 문서 속 지시문(Ch 16), 「환각」「답변 거부」는 Part 1 Ch 5 07 환각 판정 규칙(새 숫자·정답 숫자·보류 문장)과 Ch 8 04 오염 정의로 잇고 새 뜻으로 정의하지 않기, `"\n".join`·try `else`·`raise`
- 챕터 마감 때 볼 것(04에서 넘김): `_src/index.html` 04 행(개선 전 설명), `_build.py` `SECTIONS` 04 제목 「생성과 출처 인용 — 첫 완주」(첫 완주는 01에서 이미 함 — 제목 검토 후보, 바꾸면 03·05 HTML 링크 줄이 바뀜), 개선 전 QA `qa/check_content.py` 21·31~35행·`qa/test_notebook_migration.py` 10행(04 전용 조건, `runs/examples/ex04_*_preserved.txt` 네 파일 — 읽지도 바꾸지도 않음)

### 실행 환경(04에서 확인)

- 기기 루트 여유 약 555MB(04 뒤). 작업 폴더 `/tmp/ch09-04`(1차 노트북 사본 `run1.ipynb`·출력 비교 `dump.py`·삽화 원본·html 사본·해시 `hash/before04.txt`·`after04.txt`·`runs-before.txt`·`runs-after.txt`·mdpatch reps)
- 첫 새 커널은 `run_section.sh` 대신 생성기 + `execute.py`를 직접 실행(자리 표시 결과 읽기로 출력 먼저 보기). `run_section.sh`는 「오늘 볼 그림」 `.mmd`가 있어야 첨부 단계에서 멈추지 않음(04-1 `.mmd`를 먼저 두고 두 번째 새 커널)
- 삽화: 클라우드 스크래치패드 `curl` + PIL로 검수용 축소본 보기, 저장은 기기 셸 `curl` + `uv run --no-project --with pillow`(`/tmp/ch09-02/resize.py`·`cmp.py`). Higgsfield 잔액 2820
- LangChain RAG 문서(`docs.langchain.com/oss/python/langchain/rag`)는 2026-09-17 제목이 「Retrieval Augmented Generation (RAG) with Deep Agents」로 에이전트 예제임(04 b7·b10은 `source` 메타데이터를 본문 앞에 붙이는 부분만 인용)

## §05 → §06

(05절 품질 개선 2026-09-17. 결과는 `05-diagnosis.md`, 게이트 G1~G7 0(수정 전 G4 1·G5 12·G6 22·G7 2 = 37), 코드 셀 30(준비 3), **서비스 요청 8번 = 임베딩 5(`add_documents` 1 + 검색 4) + `gpt-5.4-mini` 3(와이파이 질문·Before·After)**, 새 커널 네 번(초안 2회 + 구조 확인 1회 + 교재 출력 1회 — 코드를 두 번 고쳤고, 교재 출력은 마지막 `run_section.sh` 실행. Before 답이 실행마다 보류/보류 아님으로 달랐음 → 05-diagnosis 표). 삽화 05-5 채택(2차 job `54dd57cc-…`, 4크레딧, 잔액 2816), Mermaid 4장. 실습 폴더 테스트 전후 `10 passed`, `runs/` 27개 파일 해시 전후 같음(읽기·쓰기 0), 다른 절 HTML 해시 같음(05만 바뀜), `verify.py --chapter` → `PASS 6 sections / 127 code cells (max 25 lines)`)

### 결정 (06이 따를 것)

- **실패 재현은 합성 문서 없이 E01로**: 개선 전 05의 `DISTRACTOR`·`ANSWER`·A/S 문맥 문자열은 쓰지 않았습니다. 검색 누락은 **01절 휴관일 질문 k=1**(표지만 나옴), 답이 없는 질문은 **E01에 없는 와이파이 질문**으로 만들었습니다. 두 질문의 k=1 검색 출처가 같은 `['E01 p.1']`이라, 가르는 값은 답이 아니라 정답 출처입니다
- **모델 문장·서비스 검색 결과 `assert` 0**: 05의 `assert`는 `pdf_path is not None` 하나입니다. 개선 전 06 Before/After의 `assert new_sha != config_sha`·`assert len(new_hits[0].page_content) <= 100`처럼 코드가 정하는 값은 괜찮지만, 답 글·검색 결과 내용에는 `assert`를 쓰지 않습니다(규격 §3)
- **실패 이름**: Ch 8 04 네 이름(오염·산만·혼란·충돌)은 「목록에 들어간 내용 때문에 답이 틀어진 경우」, 05의 검색 누락·답이 없는 질문은 「필요한 근거가 목록에 들어오지 않은 경우」로 자리를 갈랐습니다(05 b3). 06이 실패를 말할 때도 이 구분을 지키고, 새 정의를 만들지 않습니다
- **보류 지시**: 05 과업 명세 = 04절 글 + Ch 5 07 보류 지시 한 문장, 보류 문장 `"제공된 정보로는 확인할 수 없습니다"`(이름 `abstain_sentence`). 개선 전 06 프롬프트는 `prompts.py` 없이 노트북 안에 f-string으로 「근거에 답이 없으면 '확인할 수 없습니다.'라고 답하세요」를 씁니다 → 06에서 지시 글을 고치면 05·Ch 5 07 보류 문장과 글자를 맞추고, **답에 출처 표시가 없으면 사슬 검사가 막힙니다**(아래 계약)

### 05에서 새로 가르친 것(노트북에서 실행한 것만)

- **API·동작**: 새 API 0개. `similarity_search(k=1)`·`similarity_search(k=8)`(01·04와 같은 메서드), `in`으로 보류 문장 찾기, 목록 `in`/`not in`으로 출처 찾기
- **새 함수 두 개**: `find_missing_sources(hit_sources, answer_sources)`(정답 출처 가운데 검색 출처에 없는 것, 본문 5줄), `find_new_words(answer_text, source_text, words)`(답에는 있고 입력 글에는 없는 말, 본문 5줄, Ch 5 07 `find_new_numbers(answer, input_text)` 생각 — 입력 글은 근거+질문이 든 user 글 `messages[2][1]`)
- **용어 표(05, 3개)**: 정답 출처(질문을 보내기 전에 사람이 원문을 읽고 적은, 답이 든 쪽의 출처 목록), 검색 누락(정답 출처가 벡터스토어에는 있는데 검색 결과에 들지 않음), 답이 없는 질문(정답 출처가 빈 목록). 「검색 출처」는 검색 결과 기록의 출처만 모은 목록이라 용어 표에 넣지 않았습니다. 환각·답변 보류·보류 문장은 Ch 5 07, 지킬 말은 Ch 8 03, 기록·출처 표시는 Ch 8 02·04 뜻 그대로
- **Python 모양**: 함수 안 `if word in answer_text and word not in source_text:`, `len(missing) < len(wifi_words)` 뒤 카운터, 글 `+`로 과업 명세 잇기. 쓰지 않은 것: 내포식·try·`raise`·조건 표현식·`lambda`·`+=`·`join`·`Path`·`enumerate`·`zip`·`sum`·`max`·`@`·`BaseModel`·타입힌트·f-string 안 계산·반복문 안 요청·구조화 출력·점수

### 이어 쓸 이름과 값

- 01~04와 같은 코드·값: `candidates`·`pdf_path`, `load_pdf_pages(pdf_path, doc_id)`, `pages`(5)·`splitter`·`chunks`(500/50, 8)·`store`·`stored_ids`, `embedding_model_name`·`embedding_model`, `make_note(chunk)`, `find_missing_words(text, words)`, `build_notes_messages(notes, question)`, `find_cited_notes(answer_text, notes)`, `check_answer(answer_text, notes)`(바깥 이름 **Ch 8 04 원래 이름 `closure_keep_words`**), `persona_text`
- 05에서 새로: `task_text`(04 글 + 보류 지시 한 문장), `abstain_sentence = "제공된 정보로는 확인할 수 없습니다"`, `all_notes`(문서 청크 8개 기록), `closure_question`(01절 질문, Ch 8 이름)·`closure_keep_words`, `wifi_question = "미르시립도서관의 와이파이 비밀번호는 무엇인가요?"`·`wifi_words = ["와이파이", "Wi-Fi", "무선", "인터넷"]`, `closure_answer_sources = ["E01 p.2"]`·`wifi_answer_sources = []`, `wifi_hits`·`wifi_notes`·`wifi_sources`·`wifi_messages`·`wifi_text`·`wifi_cited`·`wifi_missing_sources`·`wifi_new_words`, `wide_hits`·`word_hit_count`, `before_*`·`after_*`(hits·notes·sources·messages·text·check·missing_sources·new_words)
- **실행값(2026-09-17 교재 출력, 17:07:35)**: 기록 8개 `E01 p.1 | 45`·`E01 p.2 | 498`·`E01 p.2 | 452`·`E01 p.3 | 498`·`E01 p.3 | 462`·`E01 p.4 | 492`·`E01 p.4 | 412`·`E01 p.5 | 270`, 휴관 지킬 말이 모두 든 기록 `E01 p.2 | 498 | []` 하나(나머지 일곱 줄 세 말 모두 빠짐), 와이파이 네 말은 여덟 줄 모두 `| 4`, 정답 출처 `['E01 p.2']`·`[]`. 와이파이 k=1 `검색 출처: ['E01 p.1']`·답 `제공된 정보로는 확인할 수 없습니다. [E01 p.1]`·`보류 문장 있음: True`·`답의 출처 표시와 같은 기록 수: 1`·`검색 결과에 없는 정답 출처: []`·`user 글에 없는데 답에 나온 말: []`. k=8 `검색 결과 수: 8`·`와이파이 말이 하나라도 든 검색 결과 수: 0`. Before k=1 답 `미르시립도서관의 정기 휴관일은 매주 월요일입니다. 공휴일이 월요일과 겹치면 휴관일은 다음 날로 변경됩니다. [E01 p.1]`·`보류 문장 있음: False`·`답 검사: {'답의 출처 표시와 같은 기록': ['E01 p.1'], '답에서 빠진 지킬 말': ['법정 공휴일', '화요일']}`·`검색 결과에 없는 정답 출처: ['E01 p.2']`·새 말 `[]`. After k=2 `검색 출처: ['E01 p.1', 'E01 p.2']`·답 `… 그 다음 날인 화요일에도 휴관합니다. [E01 p.2]`·`답 검사: {… ['E01 p.2'], … ['법정 공휴일']}`·`검색 결과에 없는 정답 출처: []`
- **Before 답은 실행마다 달랐음**(보류 1회·보류 아님 3회, 05-diagnosis 표). 06이 05 결과를 인용하면 「이번 실행에서」로만 쓰고, 결정적인 값(검색 출처·정답 출처·빠진 정답 출처·기록 표)만 단정합니다
- **출력 라벨**: 「pypdf:」 등 버전 7줄, 「OPENAI_API_KEY 설정 여부:」「모델 이름:」「temperature:」「PDF를 찾았는가:」「고른 경로:」「Document 수:」「문서 청크 수:」「넣은 뒤 저장 항목 수:」「기록 수:」「모든 기록(출처 | 글자 수):」「휴관일 질문의 지킬 말이 빠진 기록(출처 | 글자 수 | 빠진 지킬 말):」「와이파이 말이 빠진 기록(출처 | 빠진 말 수):」「휴관일 질문의 정답 출처:」「와이파이 질문의 정답 출처:」「페르소나:」「과업 명세:」「보류 문장:」「k=1 검색 결과(출처 | 글자 수 | 앞 20자):」「검색 출처:」「답:」「보류 문장 있음:」「답의 출처 표시와 같은 기록 수:」「검색 결과에 없는 정답 출처:」「user 글에 없는데 답에 나온 말:」「k=8 검색 결과 수:」「와이파이 말이 하나라도 든 검색 결과 수:」「답 검사:」「요청 | 검색 출처 | 정답 출처 | 검색 결과에 없는 정답 출처 | 보류 문장 있음 | user 글에 없는데 답에 나온 말:」
- **비유·삽화**: 05-5 똑같은 나무 책상 두 개(왼쪽 메모지 세모 = 휴관일 질문, 오른쪽 메모지 별 = 와이파이 질문), 책상마다 가운데가 빈 흰 카드 하나(k=1 표지), 책상 앞 바닥에 같은 긴 상자(01-5 벡터스토어)와 카드 일곱 장(네모·마름모·하트·세모·초승달·더하기·육각형). 세모 카드는 상자 안에 있고 별 카드는 없음. 카드 위쪽 작은 초록 동그라미는 이 그림에서 뜻이 없다고 그림 읽기에 적음(04-5는 스티커 모양 = 출처였음). 일상 예: 시험 문제를 내기 전에 답이 있는 교과서 쪽 적기(정답 출처), 답이 적힌 쪽이 책에 있는데 다른 쪽만 펴 보기(검색 누락), 안내 책자에 없는 것을 묻는 손님(답이 없는 질문)
- **그림 색(05)**: 검색 결과·검색 출처·E01 원문·사람이 적은 정답 출처 초록, 정의한 함수(`find_missing_words`) 파랑, `gpt-5.4-mini` 보라, 출력으로 확인한 값 노랑, 실행하지 않은 요청(k=8 뒤 모델 호출)과 두 조건 공통 값 회색 점선, **빨강은 Before 결함 결과(휴관일 k=1 검색 누락) 하나**(같은 요소라 05-1·05-4 두 그림에 같은 빨강). subgraph = 「칸」

### 06절이 이어받을 연결과 확인할 것

- 05 b8: 「06절에서는 k 같은 설정과 검색 결과, 답을 실행마다 기록 한 줄로 파일에 남깁니다. 이 절에서 화면으로 비교한 설정과 결과를, 나중에 다시 꺼내 비교할 수 있게 하는 단계입니다.」 노트북 정리 끝은 첫 문장만. 06 모양이 달라지면 05 설명은 `mdpatch.py` → `run_section.sh … 05 --no-exec`(재실행 금지, 서비스 요청 8번)
- **06이 읽고 쓰는 파일의 계약(꼭 먼저 확인)**: 개선 전 06 노트북은 `labs/part3/ch09-rag-first-run/runs/continuity-ch09-search.jsonl`(한 줄, SHA-256 `4f9fce62…ae61`)과 사본 `runs/continuity/{source_run_id}.jsonl`(7개, 2026-09-09)을 씁니다. 읽는 쪽과 조건:
  - `textbook/qa/check_course_continuity.py` 94~110행과 `textbook/part3/qa/check_continuity.py` 60~75행(같은 코드): 키 `qid`·`question`·`gold_doc_ids`·`source_chapter`(`ch09`)·`source_run_id`·`config`·`retrieved`·`answer`. **`question`과 `gold_doc_ids`는 `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl`의 Q001과 글자까지 같아야 합니다**(Q001 = 「미르시립도서관의 정기 휴관일은 언제인가요?」, `gold_doc_ids: ["E01"]`, `split: dev` — 05·01의 긴 휴관일 질문으로 바꾸면 검사가 막힘). `config`에 `qid`·`question`·`gold_doc_ids` 키를 넣지 않음, `retrieved`는 `rank`가 1부터 차례이고 원소마다 `doc_id`·`chunk_id`·`page`(1 이상), **`answer`에 `[E01 p.2]` 모양 출처 표시가 하나 이상 있고 그 (문서, 쪽)이 모두 `retrieved` 안에 있어야 함**(정규식 `\[([A-Z][0-9]+) p\.(\d+)\]`) → 06 답이 보류 문장만 적으면 검사가 막힙니다. 05 와이파이 답처럼 보류 뒤에 표시를 붙이면 통과하지만, 표시가 내용을 뒷받침한다는 뜻은 아님(05 b7)
  - `labs/part3/ch11-evaluation/notebooks/06-실험-로그와-자동-실행.ipynb`: 파일이 있는지와 줄 수만 읽음. `labs/part3/continuity-guide.md` 9행·실습 폴더 `README.md` 14행이 파일 이름과 폴더를 가리킴
  - `textbook/part3/qa/run_continuity_bundle.py` 17·51~54행: zip을 풀어 06 노트북을 실행하고, `labs/part3/ch09-rag-first-run/` 아래 파일 해시를 앞 실행 manifest와 비교합니다(노트북·`harness.py`·`config.yaml`을 고치면 「Upstream execution inputs changed」로 걸림 → 마감 때 재생성 대상으로 적기)
  - `config.yaml`(SHA-256 `6da4af21…4cda`)·`harness.py`(`fc4269d0…785e`)는 노트북이 아니라 `tests/test_harness.py` 3개가 읽습니다: `load_config`의 `--set` 덮어쓰기(`split.chunk_size=1000`·`corpus.tiers=[easy]`), `index_key`가 `retrieval.k`·`generation.prompt`를 무시하고 `split`을 반영, `load_queries`가 `queries.limit=2`·`queries.types=[unanswerable]`로 easy 2건을 남김 → `config.yaml`의 키 이름(`corpus.tiers`·`split`·`embedding`·`retrieval.k`·`generation.prompt`·`queries.file/tiers/types/limit`·`prices`)과 `labs/data/rag-corpus/queries.jsonl`의 `tier`·`type` 값을 바꾸지 마세요. 06 노트북은 `harness.py`를 import하지 않고 같은 단계를 셀로 풀어 씁니다(테스트는 노트북을 읽지 않음)
  - 06을 다시 실행하면 `continuity-ch09-search.jsonl` 해시와 사본 폴더 수가 바뀝니다. 앞 사본은 지우지 말고 필요하면 `mv -n`으로 옮기고, 바뀐 해시·줄 수를 진단과 챕터 요약에 적습니다(규격 §7-2, Ch 6 C-2 선례)
- **개선 전 06 노트북이 쓰는 것 중 01~05·Part 1·2에서 안 가르친 것**: `yaml.safe_load`·YAML 파일 쓰기, `from copy import deepcopy`, 딕셔너리 합치기 `|`, `from datetime import UTC, datetime`·`strftime`, `TemporaryDirectory`, `Path.cwd().parents`와 `next(...)`(규격 §2-3 금지), `**cfg["split"]` 풀어 넘기기, 내포식·제너레이터 식(`context = "\n".join(f"…" for …)`), `enumerate(…, start=1)`, f-string 삼중 따옴표 프롬프트, `hashlib.sha256(…).hexdigest()[:10]`(Ch 7 08은 자르지 않은 지문), `read_bytes`, `chunk_id` 메타데이터, PDF 18건 색인(01~05는 E01 하나), `%pip install pyyaml`, `os.getenv("RETRIEVAL_K", "2")`로 조건 바꾸기, `jupyter nbconvert --execute` 명령, `InMemoryVectorStore.dump/load`(03에서 「있다고만」 적음)
- **아직 안 가르친 것(06이 설명 없이 전제하면 안 됨)**: §04 → §05 목록에서 05가 가르친 것(정답 출처·검색 누락·답이 없는 질문·보류 지시·`find_new_words`)을 뺀 나머지. 특히 점수 기준값·거르기·MMR, 여러 PDF 색인과 문서 사이 순위, 표지 거르기, `as_retriever()`, 구조화 출력, 검색 지표·정답 문서 ID 단위 평가(Ch 11 01~04), LLM 판정자(Ch 15), 문서 속 지시문(Ch 16), 시간·비용 재기(Ch 6 06 `timed_invoke`는 배움), 같은 조건 반복 요청으로 평균 내기
- 05는 정답 출처를 **쪽 단위**(`E01 p.2`)로 적었고, Ch 11 01절과 06 기록 파일은 **문서 단위**(`gold_doc_ids: ["E01"]`)로 적습니다. 06이 두 말을 함께 쓰면 「05 정답 출처는 쪽까지, 06·Ch 11 정답 문서 ID는 문서까지」를 한 문장으로 가르고, 05 b7의 쪽 단위 한계(2쪽 452자 기록)와 이어 주세요
- 챕터 마감 때 볼 것(05에서 넘김): `_src/index.html` 20행(「정답 문서 누락, 문서 집합의 답 부재, `k` 변경, 검색 ID 확인」·「실패 경로 도식 · 안내원 삽화」)과 33행, 옛 도식·삽화 `figures/05-실패-경로.svg/.excalidraw`·`05-지어낸-숫자.png/.caption.md`(정리 대상), 개선 전 QA `qa/check_content.py` 22·37행·`qa/test_notebook_migration.py` 11행(05 전용 조건), `runs/examples/ex05_preserved.txt`·`examples/ex05_failure.py`·`ex05_injection.py`(읽지도 바꾸지도 않음)

### 실행 환경(05에서 확인)

- 기기 루트 여유 약 550MB(05 뒤). 작업 폴더 `/tmp/ch09-05`(`probe1.py` 임베딩 탐색·실행 사본 `run1/runA/runA2/runB.ipynb`·`dump.py`·`nbhash.py`(코드+출력 해시)·삽화 원본·html 사본·해시·reps)
- 서비스 답 변동: 같은 목록·temperature 0에서도 Before 답이 보류/보류 아님으로 달라졌습니다(네 실행). 결론에 닿는 자리라 다시 돌려 고르지 않고 마지막 실행으로 썼습니다(규격 §3, Ch 8 07 선례). 검색 순위·기록 표는 네 실행 모두 같았습니다
- 삽화: 클라우드 스크래치패드 `curl` + PIL로 검수용 축소본 보기, 저장은 기기 셸 `curl` + `uv run --no-project --with pillow`(`/tmp/ch09-02/resize.py`·`cmp.py`). Higgsfield 잔액 2816

## §06 → 실습

(06절 품질 개선 2026-09-17. 결과는 `06-diagnosis.md`, 게이트 G1~G7 0(수정 전 G1 6·G2 4·G3 10·G4 1·G5 13·G6 27·G7 2 = 63), 코드 셀 32(준비 3), **서비스 요청 7번 = 임베딩 6(색인 2·검색 4) + `gpt-5.4-mini` 1(5절 답)**, 새 커널 두 번(1차 18:05:02 직접 실행, 교재 출력은 2차 `run_section.sh` 18:18:22 — 답이 한 문장에서 두 문장으로 달라져 새 출력으로 고침). 삽화 06-5 채택(1회 생성, job `1cc07d6c-…`, 2크레딧, 잔액 2814), Mermaid 4장. 실습 폴더 테스트 전후 `10 passed`, 다른 절 HTML 해시 같음(06만 바뀜), `verify.py --chapter` → `PASS 6 sections / 148 code cells (max 16 lines)`, `visual.cjs` 1280·390 PASS)

### 챕터 01~06이 가르친 것 (실습 절이 쓸 수 있는 것)

- **데이터**: `labs/data/rag-corpus/pdf/easy/E01.pdf`(미르시립도서관 이용 안내, 5쪽). 01~05절은 E01 하나만, **06절만 디지털 PDF 18건**(`manifest.json`의 `tier`가 easy·medium·hard인 항목)을 색인합니다. E01 500/50 문서 청크 8개는 `1|45`·`2|498`·`2|452`·`3|498`·`3|462`·`4|492`·`4|412`·`5|270`. 18건 색인은 쪽 93·문서 청크 176, 1000/50이면 107.
- **질문 두 갈래**: 01·03·04·05절 긴 질문(`closure_question` = 「미르시립도서관의 정기 휴관일은 언제이고, 공휴일이 월요일과 겹치면 어떻게 되나요?」, `combined_question`, `wifi_question`)과 **06절 Q001 짧은 질문**(「미르시립도서관의 정기 휴관일은 언제인가요?」, Ch 11 평가셋 글과 같아야 함). 실습 절이 기록 파일을 쓰지 않는다면 질문을 자유롭게 고를 수 있고, 쓴다면 Q001 글을 그대로 써야 합니다.
- **같은 코드로 이어 쓰는 함수**: `load_pdf_pages(pdf_path, doc_id)`(02), `count_tokens(text)`·`encoding`(02), `make_source_mark(chunk)`·`dot_product`·`vector_length`·`cosine_similarity`(03), `make_note(chunk)`·`build_notes_messages(notes, question)`·`find_cited_notes(answer_text, notes)`·`check_answer(answer_text, notes)`(04·05, Ch 8 코드), `find_missing_words(text, words)`(02·03·05, Ch 8 03), `find_missing_sources(hit_sources, answer_sources)`·`find_new_words(answer_text, source_text, words)`(05), **`make_index_key(index_settings)`·`make_hit_item(hit, score, rank)`(06 새 함수)**. 01의 `find_cited_marks(answer_text, marks)`는 04부터 `find_cited_notes()`로 갈아탔습니다.
- **이어 쓰는 이름**: `candidates`·`pdf_path`(01~05) / `labs_prefix`·`corpus_path`·`config_path`·`queries_path`·`runs_path`(06) / `pages`·`splitter`·`chunks`·`store`·`stored_ids`·`embedding_model`·`embedding_model_name` / `persona_text`·`task_text`(05·06 같은 글, 04 글 + Ch 5 07 보류 지시) / `abstain_sentence`(05) / `closure_keep_words = ["월요일", "법정 공휴일", "화요일"]`·`combined_keep_words = ["월요일", "7권"]` / `record_keys`·`logged_config`·`record`·`retrieved`·`notes`·`sources`(06).
- **API**: `PdfReader`·`page.extract_text()` / `Document(page_content=, metadata=)` / `RecursiveCharacterTextSplitter(chunk_size=, chunk_overlap=)`·`split_documents()` / `OpenAIEmbeddings(model=)`·`embed_query()` / `InMemoryVectorStore(embedding=)`·`add_documents()`·`store.store`·`similarity_search(k=)`·`similarity_search_with_score(k=)` / `init_chat_model(..., temperature=0, reasoning_effort="none")`·`invoke(메시지 목록)`·`response.text`·`response.usage_metadata["input_tokens"]` / `tiktoken.encoding_for_model()` / **06 새로: `yaml.safe_load(글)`, `json.dumps(딕셔너리, sort_keys=True)`, `hashlib.sha256(바이트).hexdigest()`(Ch 7 08), `time.strftime("%Y%m%dT%H%M%S")`(Ch 7 08), `os.makedirs`(Ch 7 08), `os.replace`, `open(…, "w", encoding="utf-8")`**.
- **Python 모양(06에서 새로 쓴 것)**: 딕셔너리 리터럴을 여러 줄로 쓰기, 함수가 딕셔너리 반환, 글 `+`로 경로 만들기, 목록 안 딕셔너리를 `for`로 걸러 담기(`if item["tier"] in 목록`), `딕셔너리.keys()` 출력, 글 슬라이싱 `[:10]`, `str(숫자)`로 이어 붙이기. 06에서도 쓰지 않은 것: 내포식·제너레이터 식·`Path`·`enumerate`·`zip`·`sum`·`max`·`join`·`raise`·try·조건 표현식·`lambda`·`+=`·`@`·`BaseModel`·타입힌트·f-string 안 계산·반복문 안 요청.
- **용어(06 새로 6개)**: 실험 하네스, 실행 설정, 색인 이름표(index key), 실행 기록 한 줄, 정답 문서 ID(문서 단위), JSONL. 「캐시」·「설정 해시」는 쓰지 않았습니다(개선 전 06과 `_src/index.html`에만 남음). 「청크」 단독·「조각」 0건.
- **실패 이름 자리(05 결정 유지)**: Ch 8 04 네 이름(오염·산만·혼란·충돌)은 「목록에 들어간 내용 때문에 답이 틀어진 경우」, 05의 검색 누락·답이 없는 질문은 「필요한 근거가 목록에 들어오지 않은 경우」, 06의 Before는 「기록에 적은 설정과 실제 실행이 어긋난 경우」입니다. 새 정의를 만들지 마세요.

### 실습 절이 지켜야 할 산출 파일 계약 (꼭 먼저 읽을 것)

- **실습 절은 `runs/`에 쓰지 않는 것이 가장 안전합니다.** Ch 6·7·8 실습 절도 runs 파일을 쓰지 않았습니다(과정 요약 Part 2 §4). 쓰면 아래 계약을 모두 지켜야 하고, 최신 기록 파일을 덮어쓰면 Ch 11 입력이 실습 절 결과로 바뀝니다.
- 06절이 쓴 파일: `labs/part3/ch09-rag-first-run/runs/continuity-ch09-search.jsonl`(한 줄, SHA-256 **`294713765a115b567e162aaf37a25467577841965c1075b86553adc4080666d5`**)과 사본 `runs/continuity/20260917T181822-ch09.jsonl`(같은 내용). 사본 폴더는 9개(2026-09-09 7개 + 2026-09-17 2개), 앞 사본은 지우지 않습니다.
- 계약(읽는 쪽에서 확인한 것): 기록 키 8개 `qid`·`question`·`gold_doc_ids`·`source_chapter`(`ch09`)·`source_run_id`·`config`·`retrieved`·`answer`. `config`에 `qid`·`question`·`gold_doc_ids`를 넣지 않음. `retrieved` 항목 키 5개 `doc_id`·`chunk_id`·`page`·`rank`·`score`(`score`는 `labs/part3/ch11-evaluation/evaluate.py` 178행이 **필수**로 봄), `rank`는 1부터 차례, `page` 1 이상. `answer`에 `[E01 p.2]` 모양 출처 표시가 하나 이상 있고 그 (문서, 쪽)이 모두 `retrieved` 안에 있어야 함(정규식 `\[([A-Z][0-9]+) p\.(\d+)\]`). `question`·`gold_doc_ids`는 `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl` Q001과 글자까지 같아야 함.
- 읽는 쪽 파일: `textbook/qa/check_course_continuity.py` 94~112행, `textbook/part3/qa/check_continuity.py` 60~78행, `labs/part3/ch11-evaluation/evaluate.py` 176~200행, `textbook/part3/qa/finalize_continuity_evidence.py` 44~56행(ch09 실행의 `recall_at_5`·`precision_at_5`·`ndcg_at_5`가 `None`이고 `recall_at_logged_candidates`가 1이어야 함 → **검색 개수를 5 이상으로 올린 기록을 쓰면 걸림**), Ch 11 06 노트북(줄 수만 읽음).
- **고치지 않는 파일**: `config.yaml`(`6da4af21…`), `harness.py`(`fc4269d0…`), `prompts.py`(`4613ba02…`), `rag.py`(`16caec34…`), `labs/data/rag-corpus/` 전체, `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl`. `tests/test_harness.py` 3개가 `config.yaml`의 키 이름(`corpus.tiers`·`split`·`embedding`·`retrieval.k`·`generation.prompt`·`queries.file/tiers/types/limit`)과 `labs/data/rag-corpus/queries.jsonl`의 `tier`·`type` 값을 읽습니다.
- Ch 6·7·8 비용 기록 사슬 파일(`125fc147…58ad`·`a8aaafb7…95e9`·`f18920c6…4f4c`)은 읽지도 쓰지도 않습니다.
- **테스트 상태**: 실습 폴더 `uv run --project labs/part3/ch09-rag-first-run python -m pytest labs/part3/ch09-rag-first-run/tests -q` → `10 passed`(01~06 전후 같음). 06절 기록으로 통과하는 테스트는 실습 폴더에 없고, 계약 검사는 `textbook/qa`·`textbook/part3/qa` 스크립트가 합니다.

### 실습 절이 따를 요청 수·비용 제약

- 규격 §7-2: 30분 안팎, **모델 호출 3~5번**. 06절은 요청 7번(임베딩 6 + mini 1)이라 실습 절은 더 줄이는 쪽이 좋습니다.
- 임베딩 요청은 색인 한 번에 문서 청크 전부를 담습니다. 18건 색인은 토큰 61,071로 요청 한 번 0.0012달러쯤입니다. **E01 하나(문서 청크 8개, 토큰 2,885)로 색인하면 0.0001달러 미만**입니다(03절 출력). 실습 절이 색인을 여러 번 만들면 그만큼 늘어납니다.
- 요금: `gpt-5.4-mini` 100만 토큰당 입력 0.75·출력 4.50달러(Ch 6 06절 2026-09-17 확인), 임베딩 0.02달러. `config.yaml` `prices` 값도 같고 파일 주석 확인일은 2026-09-07입니다.
- 실습 절 30분은 `chapter.json` 챕터 시수에 더하지 않습니다(이 챕터는 `chapter.json`이 없어 `_build.py` `render_index()`의 「16h · 강의 6h · 실습 10h」와 `_src/index.html`을 봅니다). 01~06 절 meta 합은 강의 6h·실습 10h로 이미 맞습니다(01 1/1, 02 1/2, 03 1/2, 04 1/2, 05 1/2, 06 1/1) → **실습 절 meta 시수는 이 합에 더하지 않도록 적고 챕터 요약에 밝힙니다.**

### 실습 절이 함께 고칠 파일

- `_build.py` `SECTIONS`에 `("07-RAG-첫-실행-실습", "07 · RAG 첫 실행 실습 — {주제}")` 한 줄을 더하고, `render_index()`의 `"절 6개"`를 `"절 7개"`로, `_src/index.html` 절 표에 07 행을 더합니다. 06 제목을 바꾸면 05 HTML의 다음 링크 줄이 바뀌니 전후 해시를 비교하세요.
- 05절 b8과 노트북 정리 끝은 06절을 가리키고 있어 그대로 두어도 됩니다. **06절 b8 「다음 학습과 이어지는 지점」은 지금 Ch 10 08절·Ch 11 06절을 가리킵니다(실습 절이 붙으면 실습 절을 가리키게 고쳐야 함, 규격 §7-2).** 06 노트북 마지막 정리 줄 「다음 학습에서는 이 기록 모양을 그대로 쓰면서 색인 설정을 여러 가지로 늘려 비교합니다.」도 같은 자리입니다. 설명만 고치면 `mdpatch.py` → `run_section.sh … 06 --no-exec`(06은 서비스 요청 7번이라 재실행 금지).

### 아직 안 가르친 것 (실습 절이 설명 없이 전제하면 안 됨)

- §05 → §06 목록에서 06이 가르친 것(YAML 읽기·색인 이름표·기록 한 줄·정답 문서 ID·파일 지문·실행 이름·`os.replace`)을 뺀 나머지 전부.
- 특히: 점수 기준값·거르기(`score_threshold`)·MMR, 색인 파일 저장과 다시 불러오기(`InMemoryVectorStore.dump`/`load` — 03절에서 「있다고만」 적음), `as_retriever()`, 구조화 출력으로 출처 강제, 검색 지표와 정답 문서 ID 단위 평가(Ch 11 01~04), LLM 판정자(Ch 15), 문서 속 지시문(Ch 16), 여러 질문을 한 번에 돌려 평균 내기, 시간·비용을 코드로 재기(Ch 6 06 `timed_invoke`는 배움), 같은 조건 반복 요청, 문서 사이 순위 비교와 표지 거르기(Ch 10), 여러 실행이 같은 파일에 함께 쓰기.
- 문법: `Path`·내포식·제너레이터 식·`enumerate`·`zip`·`join`·`raise`·try·`lambda`·`+=`·`@`·`BaseModel`·타입힌트·f-string 안 계산·`deepcopy`·딕셔너리 `|`·`**딕셔너리` 풀어 넘기기.

### 실행 환경(06에서 확인)

- 기기 루트 여유 약 543MB(06 뒤). 작업 폴더 `/tmp/ch09-06`(`probe1.py` easy 6건·`probe2.py` 전체 흐름·`probe3.py` 18건·`probe4.py` 크기 1000·300, 삽화 원본 `orig.png`·`recheck.png`, html 사본, 해시 `hash/before06-*.txt`·`after06-*.txt`, `reps1~3.json`).
- 새 커널 실행 약 40초(PDF 18건 읽기 0.7초·색인 0.8초). `run_section.sh`는 `.mmd`와 「오늘 볼 그림」 PNG, 그리고 **삽화 PNG**가 있어야 빌드 단계에서 멈추지 않습니다(`{{img:}}`가 PNG를 인라인함).
- 클라우드 `/mnt/user-data/outputs` 입출력 오류는 06 작업에서도 그대로였습니다. 생성기는 기기 셸 heredoc으로 썼고, 삽화는 기기 셸 `curl` + `uv run --no-project --with pillow`(`/tmp/ch09-02/resize.py`·`cmp.py`)로 저장·픽셀 대조했습니다.
- `qa/verification.md`는 개선 전 검증 기록이라 01~05절과 같이 고치지 않았습니다. 루트 `textbook/qa/upgrade-progress.md`의 Ch 09 행도 「대기」 그대로 두었습니다(챕터 밖 파일).

## 실습 → 챕터 검토

(07 실습 절 신설 2026-09-17. 결과는 `07-diagnosis.md`, 게이트 G1~G7 0(첫 실행 G6 3·G7 1), 코드 셀 27(준비 3), **서비스 요청 6번 = 임베딩 4(색인 2·검색 2) + `gpt-5.4-mini` 2(실행 1·2 답)**, 새 커널 두 번(1차 18:41, 교재 출력 2차 18:53 — 실행 2 답이 달라져 새 출력으로 씀). 삽화 07-4 채택(1회 생성, job `ae02dee3-…`, 2크레딧, 잔액 2812), Mermaid 3장. 실습 폴더 테스트 전후 `10 passed`, `runs/` 27개 파일 해시 전후 같음(읽기·쓰기 0), 01~05 HTML 해시 같음, `verify.py --chapter` → `PASS 7 sections / 175 code cells (max 16 lines)`, `visual.cjs` 06·07 1280·390 PASS)

### 절 이름·제목·자리

- 파일·slug `07-RAG-실습`, 표시 제목 「07 · RAG 첫 실행 실습: 문서 청크 크기를 바꿔 검색부터 답 검사까지 비교하기」(규격 §7-2 「제목에 주제 포함」). 오케스트레이터 지시의 짧은 이름 예(`07-RAG-실습`)를 파일 이름으로 쓰고, 제목은 챕터 이름 「RAG 첫 실행」으로 적었습니다. 형식 experiment, meta는 `<!--meta: 실습 30분 | 코드 Jupyter Notebook | 새 용어 0개 -->`.
- `_build.py` `SECTIONS`에 07 한 줄, `render_index()`의 `"절 6개"` → `"절 7개"`, `_src/index.html` 절 표에 07 행을 더했습니다. 수정 전 사본은 `qa/upgrade/before/06-to-07/`(`_build.before-07.py`·`index-body.before-07.html`·`06-실험-하네스.before-07.html`·`06-실험-하네스.before-07.ipynb`·`author_06.before-07.py`·`README.before-07.md`).
- **시수**: 실습 30분은 `render_index()`의 「16h · 강의 6h · 실습 10h」에 더하지 않았습니다(규격 §7-2). 01~06 절 meta 합(강의 6h·실습 10h)은 그대로입니다. 07 meta에는 시간을 「실습 30분」으로만 적었습니다.

### 06절에서 고친 것 (재실행 없음)

- 06 b8 「다음 학습과 이어지는 지점」을 07절을 가리키게 고쳤고, 기존 Ch 10 08절·Ch 11 06절 안내는 07절 b8로 옮겼습니다. 06 노트북 마지막 정리 줄도 07절을 가리킵니다. `mdpatch.py` → `run_section.sh … 06 --no-exec`만 썼고, **06 노트북 코드+출력 해시는 그대로**(`86b3ba41…`, 기록 계약 유지). 06 HTML만 바뀝니다(`ccee14a4…` → `d28945db…`, 다음 링크 한 줄 + b8 한 단락).
- 06 b7의 「Ch 11은 검색 항목이 5건보다 적으면 Recall@5 같은 지표를 계산하지 않습니다」는 그대로 두었습니다(b8에서 옮긴 문장과 겹치지 않음).
- 실습 폴더 `README.md`에 07절 한 줄을 더했습니다(「01~06절」 → 「01~07절」 + 07절 설명 한 문장).

### 07절이 가르친 것 (새 API·새 문법 0개)

- **이어 쓴 함수 일곱 개(같은 코드)**: `load_pdf_pages()`(02), `make_note()`(04), `find_missing_words()`(Ch 8 03·02·03·05), `find_cited_notes()`(Ch 8 02·04·05), `check_answer()`(Ch 8 04·04·05, 바깥 이름 `closure_keep_words` 그대로), `find_missing_sources()`(05), `build_notes_messages()`(Ch 8 04·04~06).
- **새 함수 다섯 개**: `search_notes(question_text, question_store, wanted_count)`(검색 + 기록으로 옮기기, 본문 5줄), `make_search_row(notes)`(검색 출처·근거 글자 수·근거에서 빠진 지킬 말·검색 결과에 없는 정답 출처, 9줄), `add_answer_items(row, run_response, notes)`(입력 토큰 수·보류 문장 있음·답의 출처 표시와 같은 기록 수·답에서 빠진 지킬 말·답, 9줄), `check_question(question_text, question_store, wanted_count)`(조립, 6줄), `print_rows(rows)`(표 두 개, 6줄). 본문 줄 수는 주석·빈 줄을 빼고 직접 셌습니다(규격 §2-2 L2).
- **Python 모양**: 벡터스토어를 함수 인자로 넘기기, `for chunk_list, chunk_size in [(chunks, 500), (small_chunks, 300)]:`(튜플 풀어 담기 + 리터럴 목록 + 두 겹 `for`), `row[키] = 값`으로 딕셔너리 채우기, `abstain_sentence in answer_text`, `len(check[키])`. 쓰지 않은 것: 내포식·제너레이터 식·`Path`·`enumerate`·`zip`·`sum`·`max`·`join`·`raise`·try·조건 표현식·`lambda`·`+=`·`@`·`BaseModel`·타입힌트·f-string 안 계산·반복문 안 요청·모델 문장 `assert`(`assert`는 `pdf_path is not None` 하나).
- **새 용어 0개**. 「점검표 한 줄」은 06절 「실행 기록 한 줄」을 파일 없이 화면으로만 보는 것이라고 b4에 적었고 용어 표를 두지 않았습니다.

### 이어 쓴 이름과 값

- 01~06절과 같은 이름: `candidates`·`pdf_path`, `pages`·`splitter`·`chunks`(500/50, 8개), `small_splitter`·`small_chunks`(300/50, 14개 — 02절 이름), `embedding_model_name`·`embedding_model`, `store`·`stored_ids`, `closure_question`·`closure_keep_words`·`closure_answer_sources`(05), `persona_text`·`task_text`·`abstain_sentence`(05·06 같은 글).
- 07에서 새로: `hit_count = 2`(두 실행에서 같게 둔 값), `small_store`·`small_stored_ids`, `run1_row`·`run2_row`, 점검표 키 아홉 개 `검색 출처`·`근거 글자 수`·`근거에서 빠진 지킬 말`·`검색 결과에 없는 정답 출처`·`입력 토큰 수`·`보류 문장 있음`·`답의 출처 표시와 같은 기록 수`·`답에서 빠진 지킬 말`·`답` + 실행 셀이 더하는 `문서 청크 크기`·`문서 청크 수`.
- **실행값(2026-09-17 18:53 교재 출력)**: `Document 수: 5`·`500자 문서 청크 수: 8`·`300자 문서 청크 수: 14`, 지킬 말 세 개가 모두 든 문서 청크 `500 | E01 p.2 | 498`·`300 | E01 p.2 | 283`, 저장 항목 8·14. 검색 뒤 점검표 `500 | 8 | ['E01 p.1', 'E01 p.2'] | 543 | [] | []`와 `300 | 14 | ['E01 p.1', 'E01 p.2'] | 287 | ['월요일', '법정 공휴일', '화요일'] | []`. 답 뒤 점검표 `500 | 513 | False | 1 | ['법정 공휴일']`와 `300 | 345 | False | 1 | ['법정 공휴일']`.
- 실행 1 답 「미르시립도서관의 정기 휴관일은 매주 월요일입니다. 공휴일이 월요일과 겹치면 그 다음 날인 화요일에도 휴관합니다. [E01 p.2]」, 실행 2 답 「… 공휴일이 월요일과 겹치면 휴관일은 다음 날인 화요일로 변경됩니다. [E01 p.2]」.
- **실행 2 답은 실행마다 달랐습니다**(탐색은 보류 문장, 1차 새 커널은 목록에 없는 표시 `[E01 p.3]`·`기록 수: 0`, 교재는 2차). 규격 §3대로 다시 돌려 고르지 않았습니다. 결정적인 값(검색 출처·근거 글자 수·근거에서 빠진 지킬 말·빠진 정답 출처·입력 토큰 수·문서 청크 수)은 세 실행 모두 같았습니다.
- **출력 라벨**: 「pypdf:」 등 버전 7줄, 「OPENAI_API_KEY 설정 여부:」「모델 이름:」「temperature:」「PDF를 찾았는가:」「고른 경로:」「Document 수:」「500자 문서 청크 수:」「300자 문서 청크 수:」「질문:」「지킬 말:」「정답 출처:」「검색 개수:」「휴관 지킬 말이 모두 든 문서 청크(문서 청크 크기 | 출처 | 글자 수):」「임베딩 모델 이름:」「넣은 뒤 저장 항목 수:」「검색 뒤 점검표(문서 청크 크기 | 문서 청크 수 | 검색 출처 | 근거 글자 수 | 근거에서 빠진 지킬 말 | 검색 결과에 없는 정답 출처):」「답 뒤 점검표(문서 청크 크기 | 입력 토큰 수 | 보류 문장 있음 | 답의 출처 표시와 같은 기록 수 | 답에서 빠진 지킬 말):」「답:」

### 결론 태도와 결정

- 결론은 「문서 청크 크기를 바꾸면 검색 출처가 같아도 근거 내용이 달라질 수 있다」와 「그래서 점검표에 근거 글 검사 칸이 함께 있어야 한다」까지입니다. 어느 크기가 좋은지는 정하지 않았습니다(질문 하나·크기 두 가지·크기마다 한 번).
- 05절 b7의 쪽 단위 한계와 06절 문서 단위 정답 문서 ID를 이 절 출력으로 이었습니다. 두 실행의 「검색 결과에 없는 정답 출처」가 모두 빈 목록인데 근거 내용은 달랐습니다.
- 답 뒤 검사 세 칸(보류 문장 있음·기록 수·답에서 빠진 지킬 말)이 두 실행에서 같았습니다. 이 값은 07-3 그림에서 한 조건의 결과 상자에 넣지 않고 맨 아래 회색 상자로 뺐습니다(규격 §5-3).
- 크기 300자는 탐색 실행 뒤 정한 예임을 b7 첫 항목에 적었습니다(규격 §3). 탐색 스크립트는 `/tmp/ch09-07/probe1.py`·`probe2.py`.
- 이 노트북이 출력하지 않는 숫자(표지 45자, 2쪽 242자)는 본문·라벨·결과 읽기에서 뺐습니다. 대신 점검표에 「근거 글자 수」 칸을 두었습니다.

### 그림 색(07)

문서 청크 두 벌·질문·지킬 말·정답 출처 초록, 정의한 함수 다섯 개 파랑, 실행한 `text-embedding-3-small`·`gpt-5.4-mini` 보라, 출력으로 확인한 점검표 값 노랑, 두 실행에 모두 같았던 값 회색. **빨강 0장**(experiment 절, Ch 8 05·07 선례). subgraph = 「칸」. 07-3은 처음 `flowchart LR`로 폭 1126이 나와 06-3·06-4처럼 `flowchart TB` + 칸 안 `direction LR`로 바꿨습니다(viewBox 394·760·606).

### 챕터 검토자가 볼 것

- 별도 세션 검토: 한국어 감사 3단, 그림-본문 대조표, 삽화 「그림만 보고 관계가 읽히는가」, 실행마다 달라질 수 있는 자리(실행 2 답 한 곳).
- **챕터 마감 때 볼 것(07에서 넘김)**: `_src/index.html`은 07 행만 더했고 나머지는 개선 전 문장입니다 — 새 용어 줄의 「청크」·「설정 해시」·「캐시」, 01~06 행 설명, `[[미정: 임베딩 모델]]`, 「챕터 개요」의 옛 설계 문장(규격 §7-2 목차 페이지 대조). 개선 전 QA 스크립트 `qa/check_content.py`·`qa/test_notebook_migration.py`·`qa/test_build.py`는 절 6개 기준이라 07절을 모릅니다. `qa/verification.md`도 개선 전 기록입니다.
- 앞 절에서 넘어온 마감 목록(01~06 각 인계 「챕터 마감 때 볼 것」)은 그대로 남아 있습니다. 옛 도식·삽화 파일(`figures/0N-*.svg`·`.excalidraw`·옛 PNG)은 지우지 않았습니다.
- 루트 `textbook/qa/upgrade-progress.md`의 Ch 09 행은 챕터 밖 파일이라 고치지 않았습니다.
- 기기 루트 여유 약 519MB(07 뒤). 작업 폴더 `/tmp/ch09-07`(probe·해시·삽화 원본·html 사본·reps1~3.json·`dump.py`·`nbhash.py`).

## §2-7 리팩터 (2026-09-21)

규격 `textbook/QUALITY-UPGRADE.md` §2-7을 Ch 9에 적용했습니다(Ch 5·7·8 다음, Part 3 첫 챕터, 모양은 Ch 8 `handoff.md` §2-7). 앞 절·Ch 8에서 배운 함수는 도구 파일 `labs/part3/ch09-rag-first-run/notebooks/rag_tools.py`에서 한 줄로 가져오고, 03절 코사인 유사도는 Ch 5 02절에서 배운 식을 NumPy로 한 셀에 적습니다. 그림·결과 읽기·설명·정직성 규칙은 그대로 두고 코드와 다시 실행으로 바뀐 인용만 고쳤습니다. 삽화는 새로 만들지 않았습니다. 리팩터 직전 스냅숏은 `qa/upgrade/before-2-7/`(`_src`·노트북·`tests/*.py`·`generators/author_*.py`·그림 mmd/캡션·빌드 HTML·`lab/`(README·pyproject)·`part3/`(옛 `part3-practice.zip`·`_build_index.py`·`public-files.json`·목차·`integration-results.json`·`delivery-results.json`)·`runs/continuity-ch09-search.jsonl`(옛 정본)·`runs-sha256-before.txt`/`runs-sha256-after.txt`·`runs/moved/`)입니다.

### 도구 파일 `rag_tools.py` (함수 8개, 코드 58줄(import 두 줄 포함), SHA-256 `4a85b7202b70…c684`)

| 함수(인자) | 배운 절 | 가져가는 절 | 배운 판과 다른 점 |
|---|---|---|---|
| `count_tokens(encoding, text)` | Ch 8 01 | 02·03 | Ch 8 01절 판은 바깥 `encoding`을 읽음 → 첫 인자로(Ch 8 도구 파일 판과 같음, 02절 준비 설명에 한 문장) |
| `find_cited_notes(answer_text, notes)` | Ch 8 02 | 05·06(그리고 `check_answer` 안) | 없음 |
| `find_missing_words(text, words)` | Ch 8 03 | 02~05·07(그리고 `check_answer` 안) | 없음 |
| `build_notes_messages(persona_text, task_text, notes, question)` | Ch 8 04 | 04~07 | Ch 8 04절 판(= 이 챕터 04~07절이 다시 적던 판)은 바깥 `persona_text`·`task_text`를 읽음 → 앞의 두 인자로(04절 준비 설명에 한 문장) |
| `check_answer(answer_text, notes, keep_words)` | Ch 8 04 | 04·05·07 | 바깥 지킬 말 이름 → 셋째 인자로(04절 준비 설명에 한 문장) |
| `load_pdf_pages(pdf_path, doc_id)` | 02 | 03~07 | 없음(02절 판 그대로, 본문 9줄) |
| `make_note(chunk)` | 04 | 05~07 | 없음 |
| `find_missing_sources(hit_sources, answer_sources)` | 05 | 07 | 없음 |

- 머리: Ch 8 모양 독스트링(무엇을 모았는지 / `from rag_tools import 함수이름` / 노트북과 같은 폴더 / 함수마다 배운 절 주석 / 노트북 이름을 읽지 않고 인자로 받음) + `from pypdf import PdfReader`·`from langchain_core.documents import Document`(로더 함수가 씀). 함수마다 `# NN절에서 배웠습니다 — 하는 일` 또는 `# Ch 8 NN절에서 배웠습니다 — …`, 인자가 바뀐 세 함수는 둘째 줄 주석. 순서는 Ch 8 함수(01~04절) → 이 챕터 함수(02·04·05절).
- 금지 문법 0건(게이트 함수 `g1_ladder`·`g2_shape`를 파일 전체에 돌리면 `multiple_defs_in_cell`·`over_15_lines`만 — 셀 규칙이라 해당 없음, Ch 7·8과 같음). 본문 줄 수 `build_notes_messages` 10(Ch 8 도구 파일 판 그대로)·`load_pdf_pages` 9(02절 판 그대로)·나머지 2~7, 규격 §2-2 L2(10줄 이하) 안.
- **NumPy 함수는 넣지 않았습니다.** 벡터 계산은 03절 5절 한 곳뿐이고 뒤 절(04~07)은 벡터를 직접 계산하지 않습니다(`grep`·AST로 확인). 03절은 한 셀에서 `np.array`·`@`·`np.linalg.norm`(모두 Ch 5 02절에서 푼 이름)으로 계산하고 「Ch 5 02절처럼」으로 가리켰습니다. 새 NumPy 이름은 0개.
- **넣지 않은 것**(그 절만 씀): 01 `find_cited_marks`, 03 `make_source_mark`(03만 씀), 05 `find_new_words`, 06 `make_index_key`·`make_hit_item`, 07 `search_notes`·`make_search_row`·`add_answer_items`·`check_question`·`print_rows`.
- **`check_answer` 두 판**: 04절 판은 `combined_keep_words`, 05·07절 판은 `closure_keep_words`를 바깥에서 읽어 본문이 한 줄 달랐습니다. 두 판 모두 Ch 8 04절 원래 판(`closure_keep_words`)에서 바깥 이름만 다르므로, 지킬 말을 셋째 인자로 받는 Ch 8 도구 파일 판 하나로 합쳤습니다(04는 `combined_keep_words`, 05·07은 `closure_keep_words`를 넘김). 합치지 않은 동명·비슷한 함수는 없습니다. 01 `find_cited_marks(answer_text, marks)`(표시 목록)와 Ch 8 02 `find_cited_notes(answer_text, notes)`(기록 목록)는 인자·반환이 달라 따로 둡니다.
- 인자 모양 문장은 처음 가져오는 절만: 02(`count_tokens()`는 토큰화 규칙 객체를 첫 인자로), 04(`build_notes_messages()`는 페르소나·과업 명세를 앞의 두 인자로, `check_answer()`는 지킬 말 목록을 셋째 인자로).

### 가져오기 셀과 설명

- 기존 import 준비 셀 끝에 `# …를 도구 파일에서 가져옵니다` + `from rag_tools import …`(알파벳 순): 02 `count_tokens, find_missing_words` / 03 `count_tokens, find_missing_words, load_pdf_pages` / 04 `build_notes_messages, check_answer, find_missing_words, load_pdf_pages` / 05 `build_notes_messages, check_answer, find_cited_notes, find_missing_words, load_pdf_pages, make_note` / 06 `build_notes_messages, find_cited_notes, load_pdf_pages, make_note` / 07 `build_notes_messages, check_answer, find_missing_sources, find_missing_words, load_pdf_pages, make_note`. 04·07은 `find_cited_notes`를 `check_answer` 안에서만 써서 가져오지 않습니다. 03~07은 로더를 가져오므로 준비 셀에서 `pypdf`·`Document` 불러오기를 뺐습니다(03은 `math` 대신 `import numpy as np`, `%pip`에 `numpy==2.5.3` — 잠금과 같은 판).
- 준비 설명 셀: 고정 세 문장 「앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.」 + 「이 노트북은 NN절 `f()`…를 가져옵니다.」(02~07 모두).
- 가져온 함수만 설명하던 정의 셀과 「정의만 하는 셀이라 출력이 없습니다」 결과 읽기를 지우고 같은 소절의 설명 단락으로 합쳤습니다(「준비 셀에서 가져온 02절 로더 함수 `load_pdf_pages()`는 …」). 소절이 통째로 없어진 곳이 없어 **노트북 절 번호는 그대로**입니다.
- 「같은 코드로 다시 정의합니다」 류 문장: 생성기·노트북·`_src`에서 함수 재정의를 말하던 곳 0건(07 `_src` b3 「함수 일곱 개는 02~06절과 같은 코드로 다시 정의합니다」 → 「앞 절과 Ch 8에서 배운 함수 여섯 개는 도구 파일 `rag_tools.py`에서 가져옵니다」, b5 「5·6절 정의 셀은 앞 절과 같은 코드라 실행만 하고…」 → 「앞 절 함수는 준비 셀에서 가져오므로, 5·6절은 이 실습에서 새로 만드는 점검표·조립 함수만 정의합니다」). 남긴 「같은 코드」는 경로 후보 셀(데이터 셀, 01·02절과 글자까지 같음)과 03·04 「2절은 01·02절과 같은 코드라 강의에서 빠르게 확인합니다」(강의 범위 문장)입니다. 각 절 `_src` b3 표 셋째 칸에 「(도구 파일 `rag_tools.py`에서 가져옴)」, 05·06 b5에 「노트북은 앞 절과 Ch 8에서 배운 함수를 도구 파일 `rag_tools.py`에서 가져옵니다」.
- 바깥 이름 설명: 07 `add_answer_items()` 「`abstain_sentence`와 `closure_keep_words`를 읽습니다」, `check_question()` 「`model`과 `persona_text`·`task_text`를 읽습니다」(가져온 함수에 넘기는 값이 늘어서).
- 03절 5절: 반복문 판 세 함수(`dot_product`·`vector_length`·`cosine_similarity`)와 정의 셀 셋을 지우고, 「코사인 유사도는 Ch 5 02절에서 배웠습니다. 두 벡터의 점곱을 두 벡터 길이의 곱으로 나눈 값입니다. … Ch 5 02절처럼 NumPy의 `np.array()`·`@`·`np.linalg.norm()`으로 이 식을 적습니다.」 + 계산 셀 하나. 03-2 그림 파란 상자 셋을 `@ 점곱`·`np.linalg.norm`·`코사인 유사도`로, b3 표 Ch 5 02절 행·b5·b8·도식 읽기·캡션을 NumPy로 고침.
- lab README 한 문장(「02~07절 노트북은 앞 절과 Ch 8에서 배운 함수를 `notebooks/rag_tools.py`에서 가져오므로, 이 파일을 노트북과 같은 폴더에 그대로 둡니다」).

### 리팩터 전 생성기 문제 두 곳(고침)

- `author_05.py` 50행 `FIGURE_READ = "…"`가 한 줄 문자열 안에 줄바꿈이 들어가 **구문 오류**였습니다(검토 반영 때 `mdpatch.py`가 `\n`을 실제 줄바꿈으로 바꾼 것으로 보임). 삼중 따옴표로 고치고, 고친 리팩터 전 생성기로 `/tmp`에 다시 써서 리팩터 전 노트북과 대조 → 실행 날짜 한 줄 말고 같음(생성기와 노트북이 맞았음을 확인).
- `author_07.py` `FIGURE_ALT`가 검토 반영 전 문장(「파란 상자 build_notes_messages 메시지 목록 세 개」)으로 남아 캡션·본문·노트북의 07-1 alt(「메시지 목록 화살표」)와 달랐습니다. 캡션 판으로 맞췄습니다. 01~04·06은 리팩터 전 생성기 = 리팩터 전 노트북(실행 날짜만 다름).
- 리팩터 뒤 02~07 생성기를 `/tmp`에 다시 써서 지금 노트북과 대조: 코드·마크다운 셀 글자 모두 같음(`/tmp/ch09-27/gensync.py`).

### 실습 폴더 테스트

- `tests/test_harness.py`·`test_rag.py`는 `harness.py`·`rag.py`만 가져오고 노트북을 읽지 않습니다(AST·`grep` 확인) → **고치지 않음**. 전 10 passed → 후 **10 passed**(`uv run --project labs/part3/ch09-rag-first-run --with pytest==9.1.0 python -m pytest -q -p no:cacheprovider labs/part3/ch09-rag-first-run/tests`, `UV_PROJECT_ENVIRONMENT=.cache/vm/venv-ch09-rag-first-run`·`UV_NO_SYNC=1`).

### 절별 전 → 후 (코드 줄은 주석·빈 줄 제외, `textbook/_notebook/upgrade/count_code.py`)

| 절 | 코드 셀 | 코드 줄 | 바뀐 것 |
|---|---|---|---|
| 01 | 21 → 21 | 152 → 152 | 없음(재실행 안 함, 노트북·HTML 바이트 같음) |
| 02 | 19 → 17 | 117 → 109 (−8) | `count_tokens`·`find_missing_words` 정의 삭제(`load_pdf_pages`는 처음 가르쳐 남김) |
| 03 | 21 → 15 | 146 → 116 (−30) | + `load_pdf_pages` 삭제, 반복문 코사인 세 함수 → NumPy 한 셀 |
| 04 | 25 → 20 | 172 → 129 (−43) | 정의 5개 삭제(`make_note`는 처음 가르쳐 남김) |
| 05 | 30 → 24 | 224 → 176 (−48) | 정의 6개 삭제 |
| 06 | 32 → 28 | 302 → 268 (−34) | 정의 4개 삭제 |
| 07 | 27 → 20 | 185 → 131 (−54) | 정의 7개 삭제 |
| 합계 | **175 → 145** | **1298 → 1081 (−217, −16.7%)** | 도구 파일 58줄을 더해도 1139(−159) |

줄이 늘어난 절·셀은 없습니다. `verify.py --chapter` 셀 최대 16줄(리팩터 전부터 있던 셀).

### 다시 실행과 대조

- 02~07을 `run_section.sh`로 새 커널 2회: A(`/tmp/ch09-27/A/`)·B(교재 출력, `/tmp/ch09-27/B/`), 2026-09-21 05:36~05:53 UTC. `/tmp/ch09-27/cmp.py`(소스로 짝지음)·`cmp2.py`(첫 주석 줄로 짝지음, 리팩터 전과 대조). 실행 뒤 고친 설명은 `/tmp/ch09-27/mdsync.py`(생성기가 새로 쓴 마크다운만 실행본에 옮김, 코드 셀 글자가 하나라도 다르면 멈춤)와 `mdpatch.py`로 넣어 **다시 실행하지 않았습니다**. 값을 고르려고 더 실행하지 않았습니다.
- A·B 차이: 02 없음(요청 0) / 03 임베딩 점수 넷째 자리(A k=2 `0.5832`·`0.5748`, B `0.5833`·`0.574`, 순위·출처 같음)와 무작위 저장 ID / 04 모델 답 세 개(5절 A는 문장마다 표시, B는 끝에 모음 / Before A는 끝에 한 번, B는 문장마다 `[E01.pdf]` / After 둘째 문장 어순) — 검사 출력은 모두 같음 / 05 **없음** / 06 점수 넷째 자리와 5절 답 표시 모양(A 끝에 한 번, B 문장마다) — 검사 출력·키·순위 같음 / 07 **없음**.
- 교재 인용·그림 라벨은 B 값(Ch 5·7·8 선례). A가 결론에 닿는 자리만 본문 주의 메모에 「이 페이지 출력 바로 앞의 새 커널 실행에서는 …」: 03 b7(k=2 점수 `0.5832`·`0.5748`, 순위·출처 같음), 04 b7(표시 붙이는 자리가 답마다 달랐음), 06 b5(같은 두 문장의 맨 끝에만 표시 한 번).
- 리팩터 전(2026-09-17)과 달라져 본문·그림·복습을 고친 곳:
  - **03**: 점수 넷째 자리(B 기준 `0.5748 → 0.574`, `0.3553 → 0.3554`, `0.3225 → 0.3219`, `0.1542 → 0.1541`, `0.6257 → 0.6251`; `0.5833`·`0.3833`·`0.3383`·`0.3367`·`0.5981`·`0.3842`는 같음) → 결과 읽기·`_src` 전체·복습 4·03-1·03-2·03-3·03-4 그림 라벨·캡션·설계표. 결론(점수 = 코사인 유사도, 1·2위 차이 0.01 미만, 3위부터 0.4 미만, 가장 낮은 점수도 0보다 큼, k=1 「7권」 빠짐·k=3 모두 들어옴·2위 표지)은 두 실행 모두 같음.
  - **04**: Before 답이 문장마다 `[E01.pdf]`(옛 답은 끝에 하나) → 결과 읽기·`_src` b6 두 문장·b7 「표시를 붙이는 자리」·04-4 빨간 상자 「문장마다 E01.pdf」. 5절·After 답은 리팩터 전과 글자까지 같음. 검사 출력(같은 기록 3개/2개, 빠진 지킬 말 없음)은 두 실행·리팩터 전 모두 같음.
  - **05**: Before 답 「…다음 날인 화요일로 변경됩니다」(옛 「다음 날로 변경」), 빠진 지킬 말 `['법정 공휴일']`(옛 `['법정 공휴일', '화요일']`), `user 글에 없는데 답에 나온 말: ['화요일']`(옛 `[]`), 표의 Before 줄 끝 칸 `['화요일']` → 결과 읽기 3칸·`_src` b6 네 단락·b7 `find_new_words()` 항목·05-4 그림(「user 글에 없던 말」을 회색 상자에서 빼고 양쪽 결과 상자에: Before 화요일 / After 없음). A·B 같음. 결론(검색 누락은 답이 아니라 정답 출처 대조로 보임, Before는 보류하지 않고 근거 없는 휴관 내용)은 그대로이고, 새 말 검사가 「화요일」을 잡은 것을 한 문장 더함.
  - **06**: B 답·기록 한 줄 글자 수 `936`은 리팩터 전과 같음. 점수 `0.6492`·`0.5647` → `0.6491`·`0.5653`(본문·그림은 원래 점수를 인용하지 않음). 06-1 그림 라벨 「답 문장마다 E01 p.2」 그대로 맞음.
  - **07**: 실행 2 답이 넣지 않은 `[E01 p.3]`을 적어 `답의 출처 표시와 같은 기록 수` 1 → **0**(옛 답은 `[E01 p.2]`), 답 둘째 문장 「다음 날인 화요일에 휴관합니다」 → 8절 두 결과 읽기·9절 결과 읽기·실험 결과 해석·정리·`_src` b6 네 단락·b7 두 항목·b8·복습 3(「출처 표시 칸 0만 보고 근거가 비었다고 말할 수 있나」로)·07-3 그림(「기록 수」를 회색 상자에서 빼고 양쪽 답 뒤 상자에, 캡션 「근거 글 검사는 답을 받기 전에, 출처 표시 칸은 답을 받은 뒤에 달랐습니다」). A·B 같음. 3쪽이 04절에서 대출 권수 근거로 쓴 쪽이라는 문장을 더함(E01 3쪽에 「휴관」이 없는 것은 기기 셸에서 따로 확인, 교재에는 04절 출력으로만 적음).
- **§2-7 10항 판단 — 입력을 고친 절 없음.** 각 절의 핵심 관찰은 두 실행 모두 유지됐습니다: 02(출력 모두 리팩터 전과 같음), 03(점수 = 직접 계산한 코사인 유사도, k=1 → k=3), 04(`source` 값 출처는 세 기록이 같아 검사가 모두 맞다고 함), 05(검색 누락은 정답 출처 대조로 보임), 06(색인 이름표로 설정과 색인이 맞는지 가름, 기록 계약), 07(크기를 바꾸면 검색 출처가 같아도 근거 내용이 달라지고, 근거 글 검사 칸이 답을 받기 전에 가름). 뒤집힌 것은 07의 곁가지 관찰 「답 뒤 검사 세 칸으로는 두 실행을 가를 수 없었다」뿐입니다(이번에는 출처 표시 칸이 갈림). 학습 목표(b1 세 줄)와 이 절의 질문(검색 출처만으로 근거를 알 수 있는가 → 아니오)은 그대로라 새 출력으로 결과 읽기·결론·그림을 고치고 한 번 본 결과로 한정했습니다. **검토자가 07 「답 뒤 검사로는 못 가른다」를 핵심 관찰로 본다면 10항 대상 후보**입니다(Ch 8 07과 같은 모양).
- 날짜: 생성기 `RUN_DATE`(nbkit) 2026-09-21, 07 `RUN_DAY` 2026-09-21, `_src` 02~07 b5 「이 페이지의 출력은 2026-09-21에」. 문서·요금 확인 날짜(2026-09-17)는 그대로. 01은 2026-09-17 그대로.
- `outputs_sha256`(전 → 후): 02 `4d9610e2` → `c6bc1946`, 03 `8c3cd4d3` → `779c8255`, 04 `b58e5983` → `7f005946`, 05 `1f75540d` → `9fa9dd57`, 06 `7940bcd8` → `ee22ab8e`, 07 `74ad7858` → `4700fcbc`. 01 `44561e7a` 그대로.

### 산출 파일(runs) — 전후 해시와 읽는 쪽

| 파일 | 리팩터 전 | 리팩터 후 |
|---|---|---|
| `runs/continuity-ch09-search.jsonl` | `294713765a115b567e162aaf37a25467577841965c1075b86553adc4080666d5`(`source_run_id` `20260917T181822-ch09`) | **`e0323e897794f569175ca69113b28b460cce8481435690d32651c8494406b40e`**(`source_run_id` `20260921T055009-ch09`, 1100바이트 같음) |
| 사본 | `runs/continuity/20260917T181822-ch09.jsonl`(그대로 남김) | `runs/continuity/20260921T055009-ch09.jsonl`(같은 바이트). A 실행 사본 `20260921T054950-ch09.jsonl`(`59534c7e…9ee1`)은 `qa/upgrade/before-2-7/runs/moved/`로 `mv -n`(삭제 아님) |
| `runs/` 나머지 27개(옛 사본 9개·`runs.jsonl`·`*-baseline/chunk1000/k8/helpful.jsonl`·`examples/`) | — | 같음(`runs-sha256-before.txt`/`after.txt` 대조: 정본 한 줄이 바뀌고 사본 한 줄이 늘었을 뿐) |

- **계약 유지**: 최상위 키 8개·`config` 7키(값 전부 같음 — `name` `k2`·`corpus`·`split` 500/50·`embedding`·`retrieval` `{"k": 2}`·`generation`·`inputs`(지문 `27541f41…`·`9544b332…`))·`retrieved` 5키·**k=2**·`chunk_id` `ch09:6f9f83db90:0`/`:1`·`page` 1/2·`rank` 1/2·`answer` 글자(문장마다 `[E01 p.2]`)가 리팩터 전과 같고, 다른 것은 `source_run_id`와 `score`(`0.6492`·`0.5647` → `0.6491`·`0.5653`) 둘뿐입니다.
- **읽는 쪽 확인**: `grep -rn "continuity-ch09-search" --exclude-dir=.venv --exclude-dir=.cache textbook labs`.
  - 코드로 읽음 — 값을 박아 두지 않아 수정 없음: `textbook/part3/qa/check_continuity.py` 58~78행·`textbook/qa/check_course_continuity.py` 94~112·172~199행(`/tmp` 사본으로 결과 파일 쓰기만 막고 실행 → 두 블록 통과, **`llm-practice.zip` Stale(Part 1 노트북)에서 멈춤** — 리팩터 전에는 `part3-practice.zip/…ch09…/02-…ipynb` Stale에서 멈췄음), `textbook/part3/qa/finalize_continuity_evidence.py`·`run_continuity_bundle.py`(전체 마감 몫, 실행 안 함), `labs/part3/ch11-evaluation/evaluate.py`(`/tmp` 출력으로 실행 → ch09 실행 지표 `recall_at_logged_candidates 1.0`·@5 셋 `None`, 리팩터 전 `continuity-upstream-20260918.json`의 ch09 실행과 **`top_results`의 `score` 두 값 말고 같음**), `textbook/_notebook/build_bundle.py`(`public-files.json` 경로만).
  - **Ch 11 노트북 01~05·06이 코드로 읽음**: 01 `ch09_record["config"]["retrieval"]["k"]`·`retrieved`의 순위·문서·쪽·`chunk_id`, 01~05 `unique_doc_ids`·`recall_at`·정답 순위, 06 `evaluate.py --retrieval-log`. 읽는 키·값(`k` 2·`E01`·쪽 1/2·`ch09:6f9f83db90:0`·정답 문서 `E01` 1위)은 **모두 같음** → 01~05 노트북 출력은 다시 실행해도 같을 것으로 봅니다(실행하지 않음). **바뀌는 것은 06 노트북 출력의 실행 이름 두 줄**(`20260917T181822-ch09 | ch09 | 1 | 2 | None | None | None`·`20260917T181822-ch09 | 2 | 2 | None | None` → `20260921T055009-ch09 …`)과 06이 쓰는 `continuity-upstream-*.json`의 ch09 `run_id`·`top_results` 점수입니다. **Ch 11 노트북은 다시 실행하지 않았습니다**(다음 차례). Ch 11 `tests/` **8 passed**(`--with pytest==8.4.2`, `test_evaluate.py`는 합성 기록만 씀).
  - 새 값으로 고친 것: `textbook/qa/upgrade-contracts.md` §3(「§2-7 리팩터로 바뀜 전 → 후」 줄 추가), 이 handoff·`chapter-summary.md` §4·`qa/verification.md`·`집필점검표.md`, `textbook/part3/qa/delivery-results.json`·`integration-results.json`(검사·목차 스크립트가 다시 씀).
  - 그대로 둔 것(당시 기록): Ch 9 `06-diagnosis.md`·`07-diagnosis.md`·`review-round1-A/B.md`·`review-pack/`(06·07은 다시 만듦 — 본문만 담아 해시 인용 없음)·`gates-before.json`, Ch 10 `qa/upgrade/01-diagnosis.md`·`08-figures.md`·`review-round1-A.md`, Ch 11 `qa/upgrade/handoff.md`(123·180·248·308·497행 `294713765a…`)·`author_06.py` 40행 독스트링 `294713765a…`·`chapter-summary.md`·`review-pack/`, `textbook/part3/qa/continuity-evidence/*`·`textbook/qa/continuity-evidence/*`(2026-09-09 옛 증거), `textbook/qa/upgrade-progress.md`(읽지 말라는 지시).

### 공용 도구·챕터 밖 변경

- `textbook/part3/public-files.json`: `labs/part3/ch09-rag-first-run/notebooks/rag_tools.py` 한 줄 추가(`config.yaml` 줄 뒤).
- `textbook/part3/_build_index.py`: 고치지 않음(절 수 칸 맞음). 실행 결과 `Part 3: 36 verified sections; 90 bundled files`(89 → 90) → `textbook/downloads/part3-practice.zip` 다시 만듦(`883a9755…a0f7` → `df60a02b…7666`, 항목 92 → 93), `textbook/part3/index.html`은 바이트 같음, `textbook/part3/qa/integration-results.json` 다시 씀(코드 셀 1066 → 1036).
- `textbook/part3/qa/check_delivery.py`: **끝까지 통과**(노트북 36·코드 셀 1036·링크 누락 0·비밀 값 0·묶음 두 개) → `textbook/part3/qa/delivery-results.json` 다시 씀(`part3-practice.zip` 93항목·새 해시, `llm-practice.zip`은 같음).
- `textbook/qa/upgrade-contracts.md` §3 줄 추가, `textbook/qa/refactor-2-7-progress.md` Ch 9 행.
- 챕터 안: `qa/public-files.json`(새, Ch 8 모양), lab README 한 문장, `author_05.py` 구문 오류·`author_07.py` alt 고침(위).
- 공용 도구(`run_section.sh`·`count_code.py`·`mdpatch.py`·`upgrade_gates.py`·`build_bundle.py`·`check_*`) 변경 없음. 검사 스크립트는 결과 파일 쓰기 줄만 바꾼 `/tmp/ch09-27/chk/` 사본으로도 돌렸습니다(`check_continuity.py`·`check_course_continuity.py`).
- **다시 만들지 않은 묶음**: `textbook/downloads/part4-practice.zip`은 `textbook/part3/public-files.json`을 상류 목록으로 읽어 Ch 9 기록을 담으므로, 지금 묶음 속 `continuity-ch09-search.jsonl`은 옛 바이트이고 `rag_tools.py`가 없습니다(Part 4 노트북은 둘 다 쓰지 않음). `llm-practice.zip`도 그대로. 둘 다 전체 마감 몫.

### 검사

- `upgrade_gates.py --label after-2-7` **7/7 PASS, G1~G7 0**(`qa/upgrade/gates-after-2-7.json`). `verify.py --chapter` `PASS 7 sections / 145 code cells (max 16 lines)`. 빌드 HTML 8개 `{{` 0건(01·index HTML은 바이트 같음). `visual.cjs`(사본 `/tmp/ch09-27/vis.cjs` = Ch 8 사본) 02~07 × 1280·390px **12/12 PASS**. 다시 렌더한 그림 03-1·03-2·03-3·03-4·04-4·05-4·07-3(viewBox 폭 852·466·700·797·805·794·651, 모두 868 미만), SVG 글자로 라벨 확인.
- 생성기 ↔ 노트북 대조: 02~07 코드·마크다운 셀 글자 같음. review-pack 02~07 다시 만듦.
- 학생 묶음 확인: 새 `part3-practice.zip`을 `/tmp/ch09-27/bundle`에 풀어 `notebooks/`를 커널 작업 폴더로 03을 새 커널 실행(PYTHONPATH 없음, 키는 실행 프로세스 환경에만) → 15셀 오류 0, 경로 셋째 후보 `../../../data/…`, `rag_tools` 가져오기·NumPy 계산 정상(임베딩 요청 6번, 값은 교재에 쓰지 않음). 이 실행은 03 준비물 문장 하나(numpy 쓰임)를 고치기 전 묶음(`55df9a5f…f455`)으로 했고, 그 뒤 다시 만든 지금 묶음(`df60a02b…7666`)의 03 노트북과 코드 셀 글자가 같습니다.
- 서비스 요청: 03 6×2 + 04 6×2 + 05 8×2 + 06 7×2 + 07 6×2 + 묶음 확인 6 = **72번**(임베딩 52·`gpt-5.4-mini` 20, temperature 0·reasoning_effort none). 02는 요청 0. 예상 비용 약 0.02달러(06 색인 두 번 × 2회가 대부분).

### Ch 10·11 작업자에게

1. **Ch 11**: Ch 9 기록이 `e0323e89…406b40e`(`source_run_id` `20260921T055009-ch09`)로 바뀌었습니다. 계약·키·순위·쪽·`chunk_id`·답 글자는 같고 `score` 두 값과 실행 이름만 다릅니다. Ch 11 06 노트북을 다시 실행하면 표의 실행 이름 두 줄(HTML 06 821·927행 근처 노트북 출력)과 `continuity-upstream-*.json`의 ch09 `run_id`가 새 값이 됩니다. Ch 11 `_src` 01~06은 실행 이름·해시·점수를 인용하지 않습니다(`ch09:6f9f83db90:0`·`ch09 | 2 | False | None`·1줄·k=2·E01 1위는 그대로 맞음). 고칠 곳: Ch 11 `author_06.py` 40행 독스트링 해시, `qa/upgrade/handoff.md` 계약 해시 줄(당시 기록이면 그대로).
2. **Ch 11 06을 다시 실행하면** `runs/`에 `continuity-upstream-*.json`이 새로 생기고 `finalize_continuity_evidence.py` 49행이 가장 새 파일을 고릅니다(계약 §3). `finalize…py` 51행 `len(source_ids) == 7`은 증거 폴더의 번들 실행 기록을 세므로 이번 변경과 무관합니다.
3. **Ch 10**: Ch 9 기록을 읽지 않습니다(08절은 겉 모양만 같게 씀). 도구 파일 이름은 RAG 챕터라 `rag_tools.py`(Ch 10 폴더 안에 따로). Ch 10에서 다시 적는 Ch 9 함수(`load_pdf_pages`·`make_note`·`find_missing_words`·`count_tokens` 등)는 이 표의 인자 모양(`count_tokens(encoding, text)`·`build_notes_messages(persona_text, task_text, notes, question)`·`check_answer(answer_text, notes, keep_words)`)을 따르고 `# Ch 9 NN절에서 배웠습니다`로 옮기면 됩니다. 본문이 다르면 따로 둡니다.
4. 벡터 계산: Ch 9는 03절 5절 한 곳만 NumPy(`np.array`·`@`·`np.linalg.norm`, 새 이름 0개)로 썼습니다. Ch 10·11에서 코사인·거리·정렬을 직접 계산하면 「Ch 5 02절처럼」으로 가리키고, `np.argsort`·`axis=1` 같은 새 이름만 처음 자리에서 한 문장.
5. 임베딩 점수는 새 커널 두 번에서도 소수 넷째 자리가 달랐습니다(03 k=2 `0.5832`/`0.5833`). 점수를 결과 읽기 첫 단락·그림 라벨에 쓰면 다시 실행할 때마다 고쳐야 하므로, 06처럼 출처·글자 수 앞부분만 인용하는 모양이 안정적입니다.
