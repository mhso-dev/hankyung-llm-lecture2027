# 02-로더와-스플리터 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 02, `figures/02-청크-경계.svg`·`.excalidraw`). 챕터 전체 수정 전 게이트는 01절 작업 전에 남긴 `gates-before.json`(02절 G1 4·G2 0·G3 0·G4 0·G5 10·G6 26·G7 3 = 43).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 4 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 0 | 0 |
| G5 | 10 | 0 |
| G6 | 26 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 8 | 19(준비 2) |
| 검사한 문장 | 110 | 411 |

G8: `run_section.sh` 새 커널 PASS 세 번(2026-09-17 15:32·15:42 같은 코드 `2ffb2c78…8cae1`에서 `outputs_sha256` `82aebdb5…bce5c` 두 번 같음 — 모델 요청이 없어 출력이 결정적. 이어서 4절 토큰화 규칙 셀에 모델 이름 줄 하나를 더해(셀 2줄 → 4줄, 규격 §2-4) 세 번째 실행(15:46, `code_sha256` `e2f8f8a3…427cc`, `outputs_sha256` `4d9610e2b7bbc77e169bf76c7c1f3704c2bb07815090b48ace612dd41f7d804a`), 교재 출력은 세 번째. 세 번째 출력은 더한 한 줄 말고 두 번째와 같은 값). `chapter.json`이 없어 `verify.py --chapter textbook/part3/ch09-rag-first-run`을 따로 실행 → `PASS 6 sections / 79 code cells (max 25 lines)`. 빌드 HTML `{{` 0건, `figure.mmd` 4·`figure.illustration` 1. `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch09-01/vis/vis.cjs` 사본 + `/tmp/ch09-02/html/` HTML 사본). 실습 폴더 테스트 작업 전 `10 passed` = 작업 뒤 `10 passed`. `runs/`는 읽지도 쓰지도 않음(파일 시각 2026-09-09 그대로). Ch 6·7·8 runs 사슬 파일도 읽지 않음.

`_build.py` `SECTIONS`의 02 제목을 「PDF가 청크가 되기까지」 → 「PDF가 문서 청크가 되기까지」로 고침(규격 §4 「청크」 결정). 그래서 01·03 HTML의 이전/다음 링크 한 줄이 바뀜: 새 01·03 HTML에서 새 제목을 옛 제목으로 되돌리면 작업 전 해시와 같음(확인). 04·05·06·index HTML 해시는 그대로.

## 수정 전 주요 문제

- G1: [14]·[16] 내포식 `[chunk.page_content for chunk in …]`·제너레이터 식 + `any()`
- G5: 제목 셀·핵심 그림 없음, 코드 셀 뒤 결과 읽기가 출력 값을 인용하지 않음(7건), 마지막 After 코드 뒤 설명 없음
- G6: 70자 초과 10(참고 자료 3 포함), 영문+조사 시작 13(「`split_documents()`는」「`extract_text()`는」「Document의」 등), 5문장 넘는 단락 2
- G7: Mermaid 0(옛 Excalidraw `02-청크-경계.svg` 하나), 삽화 0, 설계표 없음
- 사다리 밖 문법(게이트가 세지 않은 것): `from pathlib import Path`·`Path.cwd().resolve()`·`start.parents`·`folders.extend()`·`/` 경로 연산·`relative_to()`, `enumerate(chunks, start=1)`, try `else`·`raise AssertionError`, 글 곱하기 `"가나다라마바사아자차" * 3`, `separators=[""]`(구분자 목록을 직접 줌 — 설명 없음), `print` 인자 여러 개에 영어 라벨(`metadata:`, `content:`)
- 내용: (1) 「청크」 단독 표기와 「Document = LangChain이 텍스트 조각을 다루는 기본 단위」(「조각」 = Ch 5 토큰과 충돌, 규격 §4). (2) PDF 2쪽 한 쪽만 읽어 01절 5쪽 색인과 이어지지 않음. (3) Before/After가 실제 PDF가 아닌 지어낸 글(「가나다…」 + 「정기 휴관일은 월요일입니다.」)에 글자 단위 구분자 `[""]`를 준 경우라, 실제 E01에서 스플리터가 줄 단위로 끊는 동작과 달랐음. 겹침 0→5로 「월요일」 한 낱말만 살림. (4) 겹침이 줄 단위로 들어간다는 것(설치판 소스)과 「겹침 50 = 최대」라는 뜻이 없음. (5) b4 도식 설명 「겹침이 0이면 "3일 늦게 반납하면 반납일부터 3일"에서 끊기고」는 3쪽 글인데 캡션은 「E01 2쪽이 청크 #0과 #1」이고 노트북은 그 경계를 실행하지 않음. (6) `chunk_id` 덧붙이기를 설명했으나 노트북에서 실행하지 않음. (7) 글자 수와 토큰 수 비교에서 Ch 8 01절 `o200k_base`와의 규칙 차이 없음. (8) b7 PyPDFLoader 경고·「Ch 10 Docling·Upstage」 확인일 2026-09-07, 이번에 실행·확인하지 않은 내용. (9) 참고 자료 확인일 2026-09-07. (10) meta 「코드 02-로더와-스플리터.ipynb」(01은 「Jupyter Notebook」)

## 바꾼 것

- **형식·학습 질문 유지**: paired, PDF → Document → 문서 청크, 메타데이터 복사, 크기 500 → 300 값 바꿔 보기, 글자 수와 토큰 수(`cl100k_base`), 겹침 Before/After.
- **이어짐(01절·Ch 8)**: 01절 후보 경로 셀 그대로, 01절 셀 코드(쪽마다 Document)를 로더 함수 `load_pdf_pages(pdf_path, doc_id)`로 묶음(본문 9줄, 메타데이터 키 `doc_id`·`page`·`source` 01과 같음, `source`는 `doc_id + ".pdf"`로 같은 값 `E01.pdf`). 5쪽 전체를 읽고 01절과 같은 500/50으로 문서 청크 8개(01 출력과 같은 1|45 … 5|270). Ch 8 01절 `count_tokens(text)`(바깥 `encoding`)·Ch 8 03절 `find_missing_words(text, words)`·`closure_keep_words = ["월요일", "법정 공휴일", "화요일"]`를 같은 코드·같은 뜻으로 씀. Ch 8 01절 `o200k_base`와 임베딩 규칙 `cl100k_base` 비교 셀 추가.
- **용어**: 한정어 없는 「청크」 0건(노트북·본문·그림·캡션·alt·빌더 제목). 01절에서 정한 「문서 청크」로 이어 쓰고 구분 문장은 b3 한 번만. 「조각」은 토큰 뜻으로 한 번(4절·b5). 크기·겹침은 「글자 수」, 토큰은 「토큰 수」로 모든 문장에서 단위를 붙임. 새 용어 5개(로더, 스플리터, 크기, 겹침, 끊을 자리 순서) = meta 「새 용어 5」. 「색인 카드」(01 「색인」과 겹침)는 쓰지 않음.
- **Before/After를 실제 PDF로**: E01 2쪽 휴관 조건은 추출 글에서 두 줄(`…그 다음 날인` 56자 / `화요일에도 휴관합니다.`). 크기 380·겹침 50에서 경계가 두 줄 사이에 오고 56자 줄이 겹침 50 안에 들지 않아 세 말을 모두 가진 문서 청크가 없음(빨강) → 겹침 100에서 369자 문서 청크에 두 줄이 함께(노랑). 바꾼 값은 겹침 하나.
- **탐색 뒤 정한 값(규격 §3, b7에 공개)**: `/tmp/ch09-02/probe.py`~`probe4.py`(요청 없음). 크기 100~600(10 간격) × 겹침 0·50·60·80·100을 5쪽 전체에 적용해 휴관 세 말을 모두 가진 문서 청크 수를 셈 → 0인 설정은 130/0·140/0·160/50·370/0·370/50·380/0·380/50뿐. 380/50(01절 겹침과 같음)과 380/100을 흐름을 보여 주는 예로 고름. 500/50에서는 498자 문서 청크 하나에 휴관 조건이 들어 있음을 b7에 적음. E01 본문 줄 대부분 54~61자(5쪽 한 줄 74자)도 탐색 출력.
- **라이브러리 확인(설치 버전 소스)**: langchain-text-splitters 1.1.2 `RecursiveCharacterTextSplitter` 기본 구분자 `["\n\n", "\n", " ", ""]`, `keep_separator=True`, `length_function=len`, `strip_whitespace=True`; `_merge_splits`는 문서 청크를 낸 뒤 앞 조각 합이 `chunk_overlap` 이하가 될 때까지 앞에서 뺌 → 겹침 안에 드는 끝 줄만 남음; `create_documents`는 메타데이터 `deepcopy`; 크기보다 긴 조각은 다음 구분자로 다시 나눔(E01에서는 실행 안 됨); `chunk_overlap > chunk_size`는 `ValueError`(본문에 안 씀). `from_tiktoken_encoder`·`TokenTextSplitter` 있음(실행 안 함). tiktoken 0.14.0 `text-embedding-3-small` → `cl100k_base`, 규칙 파일은 `tempfile.gettempdir()/data-gym-cache`에 캐시. langchain-openai 1.6.0 `OpenAIEmbeddings` `tiktoken_enabled=True`·`check_embedding_ctx_length=True`·`embedding_ctx_length=8191` → 보내기 전에 `encoding_for_model(model)`로 토큰화.
- **기본 경로**: 설치(버전 4줄) → import(`os`·`PdfReader`·`Document`·스플리터·`tiktoken`) → 2절 경로 / 로더 함수 정의 / 호출·자료형(`type()`, Ch 2 01) / 쪽마다 글자 수·줄 수·빈 줄·마지막 줄 / 표 줄(`":00~" in line`) → 3절 500/50 문서 청크와 메타데이터 / 경계 끝 두 줄·첫 두 줄·글자 수 합 → 4절 `encoding_for_model` / `count_tokens` 정의 / 문서 청크별 토큰 수 / 답 모델 규칙 330 → 5절 300/50 → Before `find_missing_words` 정의 / 380/50 / 경계 줄·56 → After 380/100 / 첫 세 줄·`assert after_missing == []` → 정리
- **쓰지 않은 것**: `Path`·`enumerate(start=)`·`join`·`raise`·try·내포식·제너레이터 식·`any()`·조건 표현식·`lambda`·`+=`·`@`·`BaseModel`·타입힌트·f-string·반복문 안 요청·API 키·모델. 새로 쓴 모양: 함수가 라이브러리 객체를 만들어 목록 반환(로더), `type(값)` 출력, 목록 슬라이싱 `[-2:]`·`[:2]`·`[:3]`을 `print` 인자·`for`에, 글 `in`으로 빈 줄(`"\n\n"`) 확인.
- **요청 수**: 서비스 모델·임베딩 요청 0번(개선 전 02도 0번). tiktoken 규칙 파일 두 개 내려받기(첫 실행). 비용 0.
- **meta 시수**: 「강의 1h | 실습 2h」 유지(01~06 합 강의 6h·실습 10h = `render_index()` 16h). 코드 표기 「Jupyter Notebook」(01과 같음).
- **그림**: Mermaid 4장(02-1 로더와 스플리터·02-2 줄 모으기와 겹침·02-3 글자 수와 토큰 수 xychart·02-4 Before-After, PNG 직접 확인, viewBox 705·719·700·836) + 삽화 02-5 공지문과 문단 카드 1장(2회 생성, 1차 job `a4f7be1f-…` 탈락, 2차 job `5c628a59-29d9-4669-9b47-ac5fc4e2107c` 채택, 4크레딧, 잔액 2830 → 2826). 옛 `02-청크-경계.svg/.excalidraw`는 지우지 않고 본문에서 쓰지 않음(정리 대상).
- **본문**: 10블록 모두 다시 씀. b2 01 k=1 표지·문서 청크 단위 근거·Ch 8 01 토큰 예산과 단위, b3 표(Ch 2 01·04, Ch 5 01, Ch 8 01·03, Ch 9 01) + 용어 구분 한 문장·API 키 없음, b4 비유·삽화·로더와 스플리터·용어 표, b5 쪽 글 모양·규칙과 겹침·글자 수와 토큰 수·300자, b6 Before/After 해석(빨강 1상자, 두 설정 공통 값 회색 상자), b7 탐색 뒤 정한 값·겹침과 줄 길이·긴 줄 다시 나누기(실행 안 함)·쪽 번호 줄과 표지·표와 Ch 10 02·04·토큰 기준 스플리터(Ch 10 05)·`OpenAIEmbeddings` 8191·PDF 로더 클래스 실행 안 함·tiktoken 내려받기·기준 버전, b8 03절 연결, b9 복습 5문제, b10 참고 자료 3건(확인 2026-09-17, WebFetch로 제목 확인). 제작 이력 문장 없음(규격 §4).

## 검토

- 스스로 확인: 결과 읽기·본문·캡션·그림 라벨의 숫자와 인용을 두 번째 새 커널 출력과 대조(G5·G7 0). 두 실행 출력 해시가 같음. 그림 방향 말(02-1·02-4 「위 칸·아래 칸, 칸마다 왼쪽에서 오른쪽」, 02-2 「위에서 아래로」, 02-3 가로축·세로축), 색 이름(xychart 주황 막대·초록 선)을 PNG와 대조. 02-4 결과 상자에 두 설정 공통 값(앞 문서 청크 370자 `['화요일']`, 문서 청크 수 11)을 넣지 않음(규격 §5-3). 함수 본문 줄 수 직접 셈: `load_pdf_pages` 9, `count_tokens` 2, `find_missing_words` 5. 주석 제외 셀당 코드 줄은 3~13줄(13 = 01절과 같은 경로 셀, 15줄 초과 0).
- 삽화 검수(저장 파일 기준, `figures/02-5-공지문과-문단-카드.prompt.md`): 초록 스티커가 긴 종이와 카드 세 장에 모두 붙음, 이웃 카드 경계의 노란 띠 짝이 그림만으로 읽힘. 약점(긴 종이 노란 띠 셋, 셋째 카드 줄 수 적음)은 그림 읽기에 「뜻이 없는 소품」으로 적음. Ch 8 03-5 초록 형광 띠(지킬 말)와 뜻이 다르다는 문장을 본문에 둠. 저장 PNG ↔ 채택 job 결과 픽셀 차이 0.
- 별도 세션 검토: 아직(메인 세션 차례)

## 남은 것

- 뒤 절 작업자에게: `qa/upgrade/handoff.md` §02 → §03
- 정리 대상(삭제 승인 필요, 목록만): `figures/02-청크-경계.svg`·`.excalidraw`(옛 도식), `qa/upgrade/gates-wip-02.json`, 기기 `/tmp/ch09-02`
- 챕터 마감 때: `_src/index.html` 02 행(「PDF 한 쪽, Document 본문·출처 정보, 청크 크기 변경」·「청크 경계 도식」)과 새 용어 줄 「청크」를 절 본문과 대조(규격 §7-2). 개선 전 QA 스크립트 `qa/check_content.py` 29행(`ex02.txt`·`ex02_overlap_preserved.txt`)·`qa/test_notebook_migration.py` 77행(02 전용 조건)은 개선 전 노트북 기준(실행하지 않음). 실습 폴더 `config.yaml` 10행 주석 「02절 주의할 점 참고」는 b7 「크기와 겹침은 글자 수」와 맞음(고치지 않음)
- `textbook/qa/run_course_bundle.py`는 실습 묶음 zip의 02 노트북을 `notebooks` 폴더를 작업 폴더로 실행함 → 셋째 후보 경로(`../../../data/…`)를 고름(`test -f`로 경로 확인, zip 실행은 전체 마감 때). 파일 이름·출력 기대값은 읽지 않음(노트북 PASS·검증 메타데이터만)

## 검토 반영 (2026-09-17, 챕터 마감 세션)

별도 세션 검토 1차 A(§01~04)·B(§05~07)를 받아 반영했습니다. 보고서와 반영 내역 전체는 `review-round1-A.md`·`review-round1-B.md` 끝 「반영 결과」, 챕터 차원 정리는 `chapter-summary.md`입니다. **이 절 노트북은 다시 실행하지 않았습니다**(`code_sha256`·`outputs_sha256`·`executed_at` 전후 같음). 반영 뒤 게이트 `--label after --strict` 7/7 PASS(G1~G7 0), `verify.py --chapter` `PASS 7 sections / 175 code cells`, `visual.cjs` 16건 PASS, 실습 폴더 테스트 10 passed, 빌드 HTML `{{` 0건.

- **판정 accept**(상 0·중 0·하 3). 반영: (02-1) b7 「같은 탐색에서 본 E01의 문장 줄은 대부분 54~61자였습니다. 10자를 넘는 줄 72개 가운데 30개가 이 길이였고, 표 줄과 제목 줄은 더 짧았습니다.」 (02-2) b7 「휴관 세 말을 모두 가진 문서 청크가 없던 설정은 크기·겹침 짝 일곱 가지뿐이었습니다. 크기 130·140·370·380은 겹침 0에서, 크기 160·370·380은 겹침 50에서 갈라졌습니다.」 (02-3) 용어 표 겹침 뜻과 b5·노트북 [20]에 구분자 1자를 포함한 45자 기준을 더했습니다.
- **02-3 문구 하나는 권고와 다르게 적었습니다.** 권고의 「끊긴 조각 단위」에서 「조각」을 쓰지 않고 「스플리터가 끊어 낸 단위로 들어가며, E01에서는 그 단위가 줄」로 썼습니다. 규격 §4가 「조각」을 Ch 5 토큰 뜻으로만 쓰게 하고, 같은 라운드에서 07절의 「조각」 9곳을 「문서 청크」로 고쳤기 때문입니다(뜻은 같습니다).
- 결정 요청 두 가지(380/100 탐색 공개, 02 제목 변경)는 권고대로 **유지**했습니다(A Q2). 검토자가 탐색 일곱 설정과 500/50 결과를 재현해 확인했습니다.
