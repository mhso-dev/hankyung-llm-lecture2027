# Ch 08 절 사이 인계 메모

절 작업자가 다음 절 작업자에게 넘기는 메모입니다. 절을 마칠 때 맨 아래에 `## §NN → §NN+1`을 붙입니다.
「이어 쓸 이름과 값」은 다음 절이 쓸 수 있는 후보이고, 「아직 안 가르친 것」은 다음 절이 설명 없이 전제하면 안 되는 것입니다.
앞 내용: `textbook/qa/upgrade-course-summary.md`(Part 1 전체), 같은 Part 앞 챕터 `textbook/part2/ch06-langchain-start/qa/upgrade/chapter-summary.md`, 바로 앞 챕터 `textbook/part2/ch07-prompt-engineering/qa/upgrade/chapter-summary.md`(§4 「Ch 08이 이어받을 것」, §5 「아직 가르치지 않은 것」, §9 runs 계약·해소 순서·R-1).

## §01 → §02

(01절 품질 개선 2026-09-17. 결과는 `01-diagnosis.md`, 게이트 G1~G7 0(수정 전 G4 1·G5 12·G6 25·G7 2), 코드 셀 22(준비 3), 노트북 모델 호출 3번(탐색 4 + 새 커널 2회 × 3 = 합계 10). 챕터 첫 절이라 `gates-before.json`은 6절 전체 수정 전 기록(G1 4·G2 6·G3 2·G4 6·G5 80·G6 159·G7 17 = 274). 삽화 01-5 채택(job `8cb93eb3-…`), Mermaid 4장)

### 빌더 변경과 02~06 작업자가 쓸 토큰 모양 (먼저 읽을 것)

- **`_build.py`를 고쳤습니다**(챕터 파일만, 공용 `_template`·`_notebook`은 그대로). 옛 사본 `qa/upgrade/before/_build.before-upgrade.py`. 절 목록은 여전히 `SECTIONS` 하드코딩이고 `chapter.json`은 없습니다. 실습 절 07을 붙일 때 `SECTIONS`에 한 줄 더하고, `render_index()`의 「절 6개」와 `_src/index-body.html` 표도 함께 고칩니다
- **토큰 모양**(`_src`에 이대로 씁니다)
  - `{{notebook:slug}}` — experiment 노트북 전체. paired는 b5에 `{{notebook:slug|example}}`, b6에 `{{notebook:slug|failure}}` 한 번씩(공용 `render.expand_notebooks`, 개선 전부터 동작). 02~06 개선 전 노트북은 모두 `lesson_part` before/after가 있는 paired입니다(개선 전 `_src` b6 「일부러 실패해 보기」). 형식을 바꾸면 노트북 메타데이터 `lesson_format`과 b6 제목·코드 유무를 함께 맞춥니다(verify가 검사)
  - `{{mermaid:이름|alt|캡션}}` — `figures/이름.svg`(render_mermaid.py 결과)를 `<figure class="mmd">`로 넣고 캡션을 붙입니다. `_src`에서 `<figure>`로 감싸지 않습니다. alt·캡션에 `|`·`}` 금지
  - `{{img:이름|alt|캡션}}` — 삽화 `figures/이름.png`를 폭 1100px JPEG로 `<figure class="illustration">`에 넣습니다. `_src`에서 `<figure>`로 감싸지 않고, 바로 아래에 「그림 읽기」 단락을 둡니다
  - 옛 두 칸 `{{img:이름|alt}}`는 개선 전과 같은 `<img alt>`만 넣습니다(감싸는 `<figure>`·`<figcaption>`은 `_src`가 씀). 옛 `{{svg:이름}}`도 그대로 동작. 02~06 개선 전 `_src`는 `{{svg:0N-…}}`만 씁니다 → 개선 때 `{{mermaid:}}`로 바꾸고 옛 SVG·Excalidraw는 지우지 않습니다
  - 치환 뒤 `{{svg:|img:|mermaid:|notebook:|code:|output:` 토큰이 남으면 빌드가 `ValueError: <slug>: 치환하지 못한 토큰`으로 멈춥니다(오타 조기 발견)
- **빌더 확인 방법**: (a) 바꾸기 전 다시 빌드한 7개 HTML이 디스크 HTML과 해시 같음, (b) 바꾼 뒤 7개 해시 같음, (c) 새 두 함수 출력이 `_template/builder.py`와 문자열까지 같음(`/tmp/ch08-01/tokentest.py`), (d) 01 개선 뒤 02~06·index HTML 해시 같음(`/tmp/ch08-01/hash/rebuild-new.txt`). 02~06 작업 전후에 `cd textbook/part2/ch08-context-engineering && sha256sum *.html`로 다른 절 HTML이 바뀌지 않았는지 볼 수 있습니다
- **verify**: `run_section.sh`는 `chapter.json`이 없으면 verify를 건너뜁니다. 그러나 `verify.py --chapter`는 `chapter.json`을 요구하지 않고 `_src/NN-*.html`·노트북·빌드 HTML 짝으로 검사하므로 이 챕터에 씁니다. 명령: `UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch08-context-engineering uv run --project labs/part2/ch08-context-engineering python textbook/_notebook/verify.py --chapter textbook/part2/ch08-context-engineering` → 01 뒤 `PASS 6 sections / 89 code cells (max 25 lines)`. 결과 파일 `textbook/_notebook/checks/notebook-contracts-part2-ch08-context-engineering.json`을 다시 씁니다. 추가로 빌드 HTML 토큰 잔존 `grep -c "{{" textbook/part2/ch08-context-engineering/NN-*.html`(0)과 `visual.cjs` 사본(아래) 확인
- **게이트**: `upgrade_gates.py`는 `chapter.json`이 없으면 `_src/NN-*.html` 이름으로 절을 찾고 실습 폴더를 `labs/part2/ch08-context-engineering`로 봅니다(동작 확인). `--section NN`으로만 돌려 `gates-wip.json`(챕터 전체)을 만들지 않았습니다
- **mdpatch.py**: 이 챕터에서 동작 확인(`chapter.json` 없으면 `labs/…` 경로로 찾음). 생성기 `qa/upgrade/author_NN.py`·노트북 마크다운·`_src`에 같은 글을 바꿉니다. 노트북 단락은 빈 줄로만 나뉘어 G6가 5문장을 셉니다

### 실행 환경

- 가상환경 `$ROOT/.cache/vm/venv-ch08-context-engineering`을 이 절에서 만들었습니다(`uv sync --locked`, uv 캐시 `$ROOT/.cache/vm/uv`, 23초). `run_section.sh`가 자동으로 씁니다. torch 없음. 새 커널 실행 약 8초. 키는 루트 `.env`(`find_dotenv(usecwd=True)`), 탐색 스크립트는 `ROOT=$PWD UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch08-context-engineering uv run --project labs/part2/ch08-context-engineering python /tmp/…`에 `load_dotenv(os.environ["ROOT"] + "/.env")`
- **기준 버전(uv.lock)**: langchain 1.4.0, langchain-core 1.6.2, langchain-openai 1.6.0, **openai 3.8.0**(Ch 6·7은 3.10.0), tiktoken 0.14.0, python-dotenv 1.2.3, pypdf 6.18.0. 새 커널 `nbclient==0.11.0`·`ipykernel==7.3.0`, Linux aarch64 Python 3.12.13
- Mermaid 렌더만 따로: `PUPPETEER_CACHE_DIR=/tmp/pptr-cache LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu python3 textbook/_notebook/mermaid/render_mermaid.py textbook/part2/ch08-context-engineering --only NN-`. 렌더 도장은 지우지 않음(같은 mmd는 `--force`)
- `visual.cjs`: `/tmp/ch08-01/vis/vis.cjs`(`require('/tmp/pw/node_modules/playwright')`로 바꾼 사본) + HTML을 `/tmp/ch08-01/html/`에 복사 → `cd /tmp/ch08-01/vis && LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu node vis.cjs /tmp/ch08-01/html`
- 삽화: 기기 셸 `curl` + `/tmp/ch08-01/resize.py`(폭 1100)·`cmp.py`(채택 job 결과와 픽셀 대조). Higgsfield 잔액 2846(01 뒤)
- `run_section.sh`는 「오늘 볼 그림」 PNG가 없으면 첨부 단계에서 멈추므로 `.mmd`를 먼저 두고 실행. 기기 루트 여유 약 620MB
- **옛 생성기**: `labs/part2/ch08-context-engineering/_make_notebooks.py`에 `raise SystemExit`를 넣었습니다(`from __future__` 줄 바로 뒤). 02~06 옛 노트북은 그대로. 챕터 마감 때 `qa/upgrade/before/generators/`로 `mv -n`. `figures/_gen_figures.py`는 옛 Excalidraw 도식 생성기라 정리 대상 목록에만

### runs 파일

- 01은 `runs/`를 읽지도 쓰지도 않았습니다. `runs/context-design-continuity.json` SHA-256 `88b3520bb65415b39acf7f805a9769ed01918ef57f63c307474ab9f5c5ba77aa`(수정 시각 2026-09-09 17:40, 옛 Ch 7 출처), Ch 7 `prompt-ab-continuity.json` `a8aaafb7…82095e9`, Ch 6 `f18920c6…4f4c` 그대로
- Ch 8 테스트 `test_ch06_ch08_continuity.py`: 01 전후 같은 결과(3 통과, 알려진 실패 2 — `test_log_paths_are_portable…`·`test_continuity_logs_form_a_hash_verified_chain` 103행). `test_ch08_source_ids_match_preserved_memory`는 **02·06 노트북 원문에 `data/memory.json`의 E01-p5 글(「회원은 최초 2시간 무료입니다.」)이 있고 「90분 무료」가 없어야** 하며, 03 원문에 「공휴일이 월요일과 겹치면 다음 화요일도 휴관」·「회원 한 사람의 도서 대출 기준」이 있고 「임시 휴관은 별도 공지」·「성인 회원 1명 기준」이 없어야 합니다 → 02·03 예제 글을 바꿀 때 확인
- 해소 순서(Ch 7 요약 §9): **06 차례**입니다. 02~05는 runs를 쓰지 않습니다. 06을 새 커널로 실행해 `source_record`를 Ch 7 파일 `a8aaafb7…`로 잇고 `runs/continuity/<실행 시각>/` 같은 바이트 사본을 만든 뒤 테스트 ①② 수정. 06 실행 뒤 Ch 7 08 재실행 금지. 06 노트북에는 `estimate_openai_cost(usage)`(인자 하나 → 0.000093)가 있어야 함. R-1 작업 폴더 제한

### 01에서 새로 가르친 것

- **Python 모양**: 비교식을 `print` 인자로 바로(`long_estimate <= available`), 인자 셋 받는 뺄셈 함수(`input_budget`), 함수가 바깥 이름 `encoding`을 읽음(Ch 5 모양), 같은 이름에 글 `+`로 다시 담기로 긴 원문 여러 줄 나눠 쓰기(Ch 7 03), `len(글)`(Ch 7 02), `in`으로 글 포함 여부(Ch 1), 모델 객체 속성 `max_tokens`와 `assert`. 쓰지 않은 것: f-string·`raise`·try·내포식·조건 표현식·`Path`·`json`·`+=`·`sum`·`@`·`BaseModel`·타입힌트·반복문 안 요청
- **API(노트북에서 실행한 것만)**: `import tiktoken`, `tiktoken.encoding_for_model("gpt-5.4-mini")` → 규칙 객체(`name` = `o200k_base`, tiktoken 0.14.0 소스 「gpt-5」 접두어), `encoding.encode(글)` → 토큰 번호 목록. Ch 6 01 `init_chat_model(…, max_tokens=N)`을 계산한 값으로 줌(`max_tokens=leftover_output`·`max_tokens=output_reserve`), `usage_metadata["input_tokens"]`·`["output_tokens"]`, `response_metadata["finish_reason"]`(`stop`·`length`). 소스만(본문에 안 씀): langchain-openai `get_num_tokens_from_messages()`
- **용어(본문 용어 표 7개)**: 컨텍스트(시험지에 인쇄된 지문, 목록에 넣지 않은 변수·파일은 아님), 컨텍스트 윈도(Ch 5 04 같은 뜻, `gpt-5.4-mini` 400,000·최대 출력 128,000 — OpenAI 모델 안내 2026-09-17), 토큰 예산(노트북 「수업 예산」, 용돈에서 교통비 먼저 떼기), **출력 예약분**(= Ch 5 04 출력 몫 = Ch 6 01 출력 상한과 같은 크기, 「예산표에서는 예약분, 모델 설정에서는 출력 상한」), 여유분(추정이 실제보다 적게 나오는 몫을 받는 빈자리), 입력 가용분(= 수업 예산 − 출력 예약분 − 여유분), 추정 토큰 수(요청 전 내 컴퓨터에서 센 글 내용 토큰 수, 실제 사용량과 따로 적음). 「조각」은 「Ch 5 01절에서 「조각」이라고 부른 단위」로 한 번만, 「청크」 안 씀
- **이어 쓸 이름과 값**: `persona_text = "당신은 미르시립도서관 안내 담당자입니다."`, `task_text = "주어진 근거에 있는 정보만 쓰세요. 두 문장 이내로 답하고, 끝에 출처를 [E01 p.2]처럼 적으세요."`, `evidence_text`(E01 2쪽 「2. 이용 시간」 세 줄: `[E01 p.2] 2. 이용 시간` / 평일·주말 시간 / `매주 월요일은 정기 휴관일입니다. 법정 공휴일에도 휴관하며, 공휴일이 월요일과 겹치면 그 다음 날인 화요일에도 휴관합니다.`), `question_text = "미르시립도서관의 정기 휴관일은 언제이고, 공휴일이 월요일과 겹치면 어떻게 되나요?"`, `intro_text`(「1. 도서관 소개」, 240자), `table_text`(구역별 이용 시간 표 6행 `|`, 326자), `user_text = evidence_text + "\n\n" + "질문: " + question_text`, `messages`(system 페르소나·developer 과업 명세·user), `long_user_text`·`long_messages`, `input_budget(total_budget, output_reserve, safety_margin)`, `total_budget = 600`·`output_reserve = 120`·`safety_margin = 40`·`available = 440`, `encoding`, `count_tokens(text)`, `estimated_input = 187`·`long_estimate = 570`, `leftover_model`·`reserved_model`. 출력 라벨 「페르소나:」「과업 명세:」「근거:」「질문:」「소개 문단 글자 수:」「구역 표 글자 수:」「메시지 수:」「소개 문단이 이번 목록에 들어 있는가:」「수업 예산:」「출력 예약분:」「여유분:」「입력 가용분:」「토큰화 규칙 이름:」「질문 글자 수:」「질문 토큰 수:」「예산표(칸 | 추정 토큰 수):」「추정 입력 합계:」「입력 가용분 안에 드는가:」「답:」「실제 입력 토큰 수:」「실제 출력 토큰 수:」「끝난 이유:」「실제 입력 - 추정 입력:」「차이가 여유분 안에 드는가:」「출력이 출력 예약분 안에 드는가:」「긴 목록 추정 입력 합계:」「넘친 토큰 수:」「답에 남은 칸:」「출력 상한(max_tokens):」「실제 합계:」「수업 예산을 넘었는가:」「수업 예산 안에 드는가:」
- **실행값(2026-09-17, 두 새 커널 출력 같음 `outputs_sha256` `b790d25d…`)**: 추정 15·37·135 = 187, 질문 글자 45·토큰 32, 실제 입력 201(추정 + 14)·출력 52·stop, 긴 목록 추정 570(+383)·넘침 130, Before 남은 칸 30 → 실제 584·30·length·합계 614(예산 넘음), After 출력 상한 120 → 201·52·stop·합계 253. 6절·After 답 글자 같음(「…매주 월요일입니다. 공휴일이 월요일과 겹치면 그 다음 날인 화요일에도 휴관합니다. [E01 p.2]」), Before 답 「…매주 월요일이며, 법정 공휴일에도 휴」에서 끊김. 탐색 짧은 목록 답은 62토큰으로 「법정 공휴일에도 휴관」을 담음(노트북 답은 안 담음). 메시지 3개일 때 추정과 실제 차이 14는 탐색·두 실행 모두 같음
- **데이터 출처**: 근거·긴 자료는 `labs/data/rag-corpus/build/html/E01.html` 2쪽 원문(Ch 9 01 노트북이 PDF로 읽는 같은 쪽, 출처 표시 `[E01 p.2]`도 Ch 9 01 답과 같은 모양). **개선 전 02 노트북은 `records`(id `E01-p2`·`E01-p3`·`E01-p5`, 짧은 글 「매주 월요일 휴관」·「7권, 14일 대출」·「회원은 최초 2시간 무료입니다.」)를 임시 폴더 JSON에 쓰고 주제로 고릅니다**. 01의 `[E01 p.2]` 원문과 02의 `E01-p2` 짧은 글은 표기가 다르므로, 02가 01 글을 잇는다면 「01절 근거 문단을 한 줄로 줄인 기록」처럼 한 문장으로 잇거나 표기를 맞춰 주세요(테스트는 E01-p5 글만 요구)
- **비유**: 세로 테이프 두 줄로 나눈 긴 나무 책상(책상 윗면 = 수업 예산, 오른쪽 빈 답안지·연필 = 출력 예약분, 가운데 빈 띠 = 여유분, 왼쪽 구역 = 입력 가용분 — 파란 명찰 = system 페르소나, 주황 클립보드 = developer 과업 명세, 흰 종이 두 장 = 근거, 노란 메모지 = 질문), 책상 왼쪽 바닥 열린 종이 상자의 종이 묶음 = 변수에만 있고 목록에 넣지 않은 자료. Ch 7 한 책상 색 약속을 이음. 개선 전 02 `_src` 비유가 「선반·서랍」류라면 01-5 바닥 상자(책상 밖 = 컨텍스트 아님)와 이어 쓸 수 있음. 「쟁반」은 Ch 5 04 그림을 가리킬 때만
- **그림 색(01)**: 정한 값·넣은 글·목록 초록, 계산·정의한 함수(`input_budget`·`count_tokens`) 파랑, 실행한 `gpt-5.4-mini` 보라, 출력으로 확인한 값 노랑(값 바꿔 보기의 `False`·넘침도 노랑), 노트북에서 실행하지 않은 값·단계(모델 최대 한도, 요청 안 보냄) 회색, 빨강은 paired Before 결함 결과(끊긴 답·예산 넘음) 한 상자
- **02절이 이어받을 연결**: 01 본문 b8·노트북 끝 「02절에서는 자료를 파일에 적어 두고, 질문에 필요한 기록만 골라 메시지에 넣습니다. 7절의 긴 목록처럼 넘치는 자료를 보내기 전에 줄이는 첫 방법입니다. 같은 E01 문서는 Ch 9에서 검색으로 찾게 됩니다.」(노트북 정리 셀 끝은 첫 문장 + 「도서관 문서는 이 절과 같습니다.」). 개선 전 02 `_src` b3 「01절에서 외부 파일은 그 자체로 현재 컨텍스트가 아니라고 배웠습니다」·「입력 가용분 안에서 지시, 질문, 근거를 배분」은 개선된 01과 맞음(01은 「변수나 파일에 있어도 목록에 넣지 않으면 컨텍스트가 아님」). 개선 전 02 b3 「Ch 6에서 작성한 모델 호출 코드에서 사용자 메시지를 만드는 위치를 찾습니다」는 01처럼 Ch 7 목록 모양으로 이어 주세요. 02가 선택 뒤 예산을 확인한다면 01 `input_budget`·`count_tokens`·`available = 440`을 같은 코드로 이어 쓸 수 있음. 01 결론 「이번 목록에서 추정과 실제 차이 14」, 「여유분 40·예산 600은 흐름을 보여 주려고 정한 예」를 일반화하지 말고 이어 씀
- **개선 전 02 노트북이 쓰는 것 중 01·Ch 6·7·Part 1에서 안 가르친 것**: 공용 셀 `raise FileNotFoundError`·`raise RuntimeError`, `max_tokens=300`(temperature 누락), `from pathlib import Path`·`from tempfile import gettempdir`·`Path(...) / "..."`·`write_text`·`read_text`, `json.dumps(records, ensure_ascii=False)`(Ch 6·7은 `with open` + `write`), 집합 `{"대출", "주차"}` 리터럴과 집합 빼기 `selected_ids - {"E01-p5"}`, 날짜 글 비교 `row["effective_date"] <= criteria["as_of"]`, f-string `f"[{row['id']}] {row['text']}"`·`f"""…"""`, `"\n".join(context_lines)`, `print(response.text)` 라벨 없음·영어 라벨 `input_tokens:`, `model.invoke([...])`를 인자 안에서 목록 리터럴로
- **아직 안 가르친 것(02가 설명 없이 전제하면 안 됨)**: Ch 7 요약 §5 전체(문자열 하나로 `invoke`, `AIMessage(…)` 직접 만들기, 대화 기록 여러 번, 틀 `|` 체인, 틀 `partial`, `with_structured_output` 재실행, 도구 호출, `batch`·`astream`, 콜백, 추론 none 아닌 요청, 캐시 입력, f-string, `Path`·`datetime`·`next`·`raise`, 내포식·조건 표현식·`lambda`, `+=`·`sum`·`max`·`zip`·`any`·`all`, `print`의 `end`·`flush`, `@`·`*args`·`**` 풀기, `or` 기본값, `join()`·`splitlines`·`count()`·`startswith()`·`replace`·정규식, 글 슬라이싱, 예외 튜플, `isinstance`, `json.dump()`·`json.load()`, 집합 비교 `<=`, `os.makedirs(…, exist_ok=True)`, 파일 삭제·옮기기, `range()`로 요청 반복, 답 정확성 판정·비율 지표·LLM 판정자) + 01에서도 안 한 것: `tempfile`·임시 폴더, 집합 빼기·집합 리터럴, 날짜 비교, 글 `join`, langchain-openai `get_num_tokens_from_messages()`, 메시지 형식 표시의 실제 모양(요청 본문), 여유분을 정하는 일반 규칙, 다른 제공자의 토큰화 규칙, 추론 설정 none이 아닌 요청의 출력 상한과 추론 토큰

## §02 → §03

(02절 품질 개선 2026-09-17. 결과는 `02-diagnosis.md`, 게이트 G1~G7 0(수정 전 G2 1·G4 1·G5 15·G6 32·G7 3), 코드 셀 23(준비 4), 노트북 모델 호출 2번(탐색 3 + 새 커널 2회 × 2 = 합계 7). 삽화 02-5 채택(job `c211dfee-…`, 잔액 2844), Mermaid 4장. 최종 `outputs_sha256` `d3643c52…`)

### 빌더·검사(§01 인계 그대로 동작 확인)

- `_build.py`는 고치지 않았습니다. `{{mermaid:이름|alt|캡션}}`·세 칸 `{{img:}}`·`{{notebook:slug|example}}`/`|failure}}` 모두 01 인계대로 동작. `run_section.sh`는 verify를 건너뛰므로 `verify.py --chapter` 따로 → `PASS 6 sections / 97 code cells (max 25 lines)`(max 25는 개선 전 03~06). 빌드 HTML `{{` 0건. 03~06·index HTML 해시는 01 인계 `/tmp/ch08-01/hash/rebuild-new.txt`와 같음(01 HTML은 01 마지막 수정 뒤 값 `8f29aad6…`)
- 결과 읽기 채우기: 생성기에 `[[READ_…]]` 자리 표시 → 두 번째 새 커널 뒤 `mdpatch.py`(`/tmp/ch08-02/fill.py`가 만든 `reps1.json`). 「오늘 볼 그림」 alt에는 자리 표시를 두지 않음
- 노트북 소제목 번호가 01(1~9절)과 달리 1~7절입니다(2 이어 쓰기, 3 Write, 4 Select, 5 값 바꿔 보기, 6 Before, 7 After). 결과 읽기에서 절 번호를 가리킬 때 확인(02에서 「9절 After」 오타를 `mdpatch.py`로 고침)
- `visual.cjs`: `/tmp/ch08-01/vis/vis.cjs` 사본 그대로 + HTML 사본 폴더(`/tmp/ch08-02/html`)

### 실행 환경

- 01과 같음(`$ROOT/.cache/vm/venv-ch08-context-engineering`, 새 커널 약 10초). 탐색 스크립트는 `ROOT=$PWD UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch08-context-engineering uv run --project labs/part2/ch08-context-engineering python /tmp/ch08-02/probe1.py`
- E01·E02·E04 쪽별 원문은 같은 가상환경의 pypdf 6.18.0으로 `labs/data/rag-corpus/pdf/easy/E0N.pdf`를 읽어 확인(E01 1쪽 표지 「2026년판 · 발행 2026. 3. 1.」, 2쪽 소개·이용 시간·표·회원 가입 앞부분, 3쪽 자료 대출·반납과 연체·예약, 4쪽 열람실 뒷부분·디지털자료실·메이커 스페이스·행사·대관, 5쪽 찾아오시는 길·주차·문의)
- 삽화: 기기 셸 `curl` + `/tmp/ch08-02/resize.py`·`cmp.py`(01 사본). 기기 루트 여유 약 600MB
- 02 노트북은 준비 셀에서 `tempfile.mkdtemp(prefix="ch08-02-")`로 `/tmp`에 빈 폴더를 만들고 `library-notes.json`(535글자)을 씁니다. 실행마다 새 폴더가 남습니다(작음)

### runs 파일

- 02는 `runs/`와 `data/memory.json`을 읽지도 쓰지도 않았습니다. `runs/context-design-continuity.json` `88b3520b…` 그대로, `memory.json` `0aa9fae5d8240aa6d9f01fb373871ead4b4b6b35e6c057eab2aaf6a6899fabd2`
- Ch 8 테스트 결과 01 뒤와 같음(3 통과·알려진 실패 2). `test_ch08_source_ids_match_preserved_memory`의 02 조건(「회원은 최초 2시간 무료입니다.」 있음, 「90분 무료」 없음) 통과. **03 조건**: 03 노트북 원문에 「공휴일이 월요일과 겹치면 다음 화요일도 휴관」·「회원 한 사람의 도서 대출 기준」이 있어야 하고 「임시 휴관은 별도 공지」·「성인 회원 1명 기준」이 없어야 함(개선 전 03 셀 14 `closure["exception"]`, 셀 22 `changed_loan["condition"]`에 있음) → 03 예제 글을 바꿀 때 두 문자열을 남기거나 테스트 수정 계획을 챕터 요약에 적기
- 해소 순서는 §01과 같음: 06 차례. 03~05는 runs를 쓰지 않음

### 02에서 새로 가르친 것

- **Python 모양**: 딕셔너리 목록 리터럴(한 기록 한 줄), `print("…:", 딕셔너리)`·`print(딕셔너리 목록)`(키·값이 작은따옴표로 나옴), 딕셔너리 목록 `==` 비교 + `assert`, `with open(이름, encoding="utf-8")` 읽기 모드 생략(Ch 2 05는 `"r"`를 적었고, Ch 6 06·Ch 7 08 노트북도 생략 모양을 씀), 두 조건을 변수 두 개(`same_institution`·`needed_topic`)에 담아 `if … and …:`, 반복문 안에서 `append` 두 개와 글 `+` 다시 담기, 인자 두 개 함수가 목록을 돌며 조건에 맞는 원소만 담아 반환(`find_cited_notes`), 비교식을 `print` 인자로(01), 준비 셀 `tempfile.mkdtemp`+`os.chdir`+`os.listdir`(Ch 2 05 모양, 경로는 출력 안 함). 쓰지 않은 것: f-string·`raise`·try·내포식·조건 표현식·`Path`·`join`·집합 리터럴·집합 빼기·`+=`·`sum`·`next`·`@`·`BaseModel`·타입힌트·반복문 안 요청·반복문 안 `print`·날짜 비교
- **API(노트북에서 실행한 것만)**: `json.dumps(records, ensure_ascii=False, indent=2)`·`json.loads(file.read())`(Ch 6 06 다시), `tempfile.mkdtemp`·`os.chdir`·`os.listdir`(Ch 2 05 다시), `init_chat_model(…, max_tokens=output_reserve)`(01 After), `tiktoken.encoding_for_model`·`encode`(01). 새 라이브러리 API 없음
- **용어(본문 용어 표 7개)**: 적어 두기(Write, 나중에 쓸 정보를 메시지 목록 밖에 저장, 공책에 적어 두기), 골라 넣기(Select, 저장한 정보 가운데 필요한 것만 골라 메시지 목록에 넣기, 공책에서 그 과목 쪽만 펴기), 기록(사실 한 문장 + 설명 값을 담은 딕셔너리 하나), 기록 파일(`library-notes.json`), 메타데이터(내용 옆에 적어 두고 찾거나 고를 때 쓰는 설명 값, 책등 분류 번호), 선택 조건(사람이 코드에 적음), 출처 표시(`[E01 p.3]`). 줄이기(Compress)·나누기(Isolate)라는 한국어 이름을 b2에서 한 번 씀(03이 이어 쓰거나 바꾸면 02 b2·b8 문장 확인). 「조각」「청크」「틀」「빈자리」「칸(필드)」 안 씀, 딕셔너리 자리는 「키」. 개선 전 02의 「출처 식별자」「외부 저장소」「적용 조건」「점진적 공개」는 본문에서 뺌(06이 「단계적 공개」를 쓰면 02와 겹치지 않음)
- **이어 쓸 이름과 값**: `persona_text`(01과 같음), `task_text = "주어진 근거에 있는 정보만 쓰세요. 두 문장 이내로 답하고, 문장마다 끝에 출처를 [E01 p.2]처럼 적으세요."`(01에서 「문장마다」만 더함), `total_budget = 600`·`output_reserve = 120`·`safety_margin = 40`·`available = 440`, `input_budget()`·`count_tokens()`·`encoding`, `model`(출력 상한 120), `records`(5개: `{"출처": "E01 p.2", "기관": "미르시립도서관", "주제": "휴관", "내용": "매주 월요일은 정기 휴관일입니다."}` / E01 p.3 대출 「도서는 7권까지 14일 동안 대출할 수 있습니다.」 / E01 p.5 주차 「회원은 최초 2시간 무료입니다.」 / E02 p.5 별빛제과 주차 「본사 주차장은 선착순이며 월 3만 원의 주차비가 급여에서 공제됩니다.」 / E04 p.2 청담해운 대출 「무주택 직원의 전세자금 대출 기간은 2년이며 2회 연장할 수 있습니다.」), `notes_text`·`library-notes.json`·`loaded`, `question_text = "미르시립도서관에서 도서는 몇 권까지 빌릴 수 있고, 회원 주차는 몇 시간 무료인가요?"`, `needed_institution`·`needed_topics = ["대출", "주차"]`, `selected`·`selected_sources`, `evidence_text`(줄마다 `"[" + 출처 + "] " + 내용 + "\n"`), `user_text = evidence_text + "\n" + "질문: " + question_text`, `messages`, `estimated_input = 124`, `topic_only_sources`·`topic_only_text`(37 → 101토큰), `before_user_text`(「근거: library-notes.json 파일에 저장해 두었습니다.」 + 질문), `find_cited_notes(answer_text, notes)`. 출력 라벨 「작업 폴더의 파일:」「기록 수:」「첫 기록:」「파일에 쓴 글자 수:」「다시 읽은 기록 수:」「처음 목록과 같은가:」「질문:」「고를 기관:」「고를 주제:」「고른 기록 수:」「고른 기록 출처:」「user 글:」「메시지 수:」「추정 입력 합계:」「입력 가용분 안에 드는가:」「주제만 본 기록 수:」「주제만 본 기록 출처:」「근거 토큰 수(기관 + 주제):」「근거 토큰 수(주제만):」「고른 기록이 user 글에 들어 있는가:」「답:」「실제 입력 토큰 수:」「실제 출력 토큰 수:」「끝난 이유:」「답의 출처 표시와 같은 기록:」「실제 입력 - 추정 입력:」「차이가 여유분 안에 드는가:」
- **실행값(2026-09-17, 두 번째 새 커널)**: 추정 124(메시지 3개)·실제 138·차이 14(01과 같은 값), Before 추정 101·실제 115(차이 14)·출력 49·stop·답 「최대 10권」「2시간 무료」 두 문장 모두 `[E01 p.2]`·찾은 기록 = E01 p.2 휴관, After 출력 42·stop·답 두 문장이 기록 문장과 같은 글자·`[E01 p.3]`·`[E01 p.5]`. 첫 새 커널 After 둘째 문장은 「회원 주차는 최초 2시간 무료입니다.」·출력 44. 탐색에서 질문만 보낸 답은 「5권」
- **데이터 출처와 주의**: 기록 `내용`은 원문을 한 문장으로 옮겨 적은 것(원문 그대로 아님)이라고 노트북 3절·b4에 적음. E01 5쪽 원문 「회원은 최초 2시간 무료, 이후 30분마다 500원입니다.」의 추가 요금이 기록에 없다는 것을 b4·b7에서 「기록에 없는 조건은 출처로 원문 확인」 → 「원문을 줄이면서 조건을 지키는 방법은 03절」로 넘김. **03이 줄이기(Compress)를 가르칠 때 이 예(주차 추가 요금이 빠진 기록)나 개선 전 03의 대출 연장 조건 예를 이어 쓸 수 있음**. E01 3쪽 원문 「회원 한 사람이 한 번에 빌릴 수 있는 자료는 도서 7권과 영상 자료 2점입니다. 대출 기간은 도서 14일, 영상 자료 7일입니다.」 + 연장 문단 「다른 이용자의 예약이 없는 경우 1회에 한해 7일 연장」(개선 전 03 `loan_original`은 원문과 표현이 다름 — 03이 원문으로 바꾸면 테스트 문자열 「회원 한 사람의 도서 대출 기준」과 함께 확인)
- **비유**: 01-5 책상(파란 명찰 = system 페르소나, 주황 클립보드 = developer 과업 명세, 노란 메모지 = 질문, 오른쪽 빈 답안지·연필 = 출력 예약분)에 초록 탭 흰 카드 두 장(고른 기록), 책상 왼쪽 바닥 열린 나무 카드 상자(기록 파일, 남은 회색·갈색·보라 탭 카드 = 고르지 않은 기록), 상자 옆 빈 카드와 펜(적어 두기). 탭 색 = 메타데이터(색 하나 = 조건 하나 아님). 01-5 세로 테이프 구역선은 02 그림에 없음. Ch 4 「카드 상자」(표)와 뜻이 달라 「기록 카드 상자」로만 부름. 개선 전 03 `_src` 비유는 「회의록 한 장 정리」·「업무별 서류철」 — 서류철은 Ch 4 비유와 겹치므로 03이 쓰면 그림 읽기에 뜻을 적기
- **그림 색(02)**: 넣은 글·기록·파일 초록, 코드 단계(`json.dumps`·`with open`·`json.loads`·조건 반복문) 파랑, `gpt-5.4-mini` 보라, 출력 값 노랑, 출력하지 않은 빠진 기록·실행하지 않은 요청 회색(점선), 빨강은 Before 결과 한 상자. 두 답에 모두 있던 「주차 2시간」은 비교 그림에서 뺌. 02-1은 TB + 칸끼리 화살표(`WRITE --> SELECT`)로 칸 안 LR 배치를 얻음(노드 사이 화살표로 칸을 넘으면 칸 안 `direction`이 무시되어 폭 1691이 됐음)
- **03절이 이어받을 연결**: 02 본문 b8·노트북 끝 「03절에서는 고른 자료가 여전히 길 때 조건을 지키며 줄이는 방법을 다룹니다. 업무마다 메시지 목록을 나누는 방법도 함께 봅니다.」(노트북은 한 문장). b7 「원문을 줄이면서 조건을 지키는 방법은 03절에서 다룹니다」, b2 「줄이기(Compress)와 나누기(Isolate)는 03절에서 다룹니다」. Ch 7 04 b6 「기록에서 무엇을 고르고 줄일지는 Ch 8 02·03절에서 다룹니다」와 맞음. 03 개선 전 셀 16 「근거의 조건·예외·출처를 빠뜨리지 마세요.」 system + f-string user, `compress(record: dict[str, str]) -> str`(타입힌트·`raise ValueError`·f-string·`" | ".join`·집합 빼기 `set(required) - record.keys()`) — 모두 A 트랙 미교육 모양. 03이 02 `records`의 키(`출처`·`기관`·`주제`·`내용`)를 이으면 압축 기록의 키도 한국어로 맞출 수 있음. 02는 `messages` 하나로 두 기록(대출·주차)을 함께 넣었으므로, 03 Isolate가 「주제마다 목록 나누기」를 보이려면 02 질문·기록을 이어 쓸 수 있음
- **아직 안 가르친 것(03이 설명 없이 전제하면 안 됨)**: §01 목록 전체 + 02에서도 안 한 것: `json.dump()`·`json.load()`(파일 객체에 바로), 파일 덧붙이기 모드 `"a"`로 기록 추가, 기록 수정·삭제, 조건에 맞는 기록이 없을 때 처리, 판·시행일(날짜) 조건, 여러 파일에 나눠 저장, 메타데이터로 정렬·가장 최근 판 고르기, 모델에게 기록을 고르게 하기, 검색·임베딩·벡터스토어(Ch 9~), 도구로 파일 읽기(Ch 19), 요약을 모델에 맡기기(요약 요청), `isinstance`, 딕셔너리 `keys()` 집합 연산

## §03 → §04

(03절 품질 개선 2026-09-17. 결과는 `03-diagnosis.md`, 게이트 G1~G7 0(수정 전 G4 1·G5 12·G6 29·G7 3), 코드 셀 26(준비 3), 노트북 모델 호출 3번(탐색 4 + 새 커널 2회 × 3 = 합계 10). 삽화 03-5 채택(job `67fee777-…`, 잔액 2842), Mermaid 4장. 최종 `outputs_sha256` `08696210…`)

### 빌더·검사(§01·§02 인계 그대로 동작 확인)

- `_build.py`는 고치지 않았습니다. 토큰 세 모양 모두 01 인계대로 동작. `verify.py --chapter` → `PASS 6 sections / 110 code cells (max 25 lines)`. 빌드 HTML `{{` 0건. 작업 전후 챕터 HTML 해시(`/tmp/ch08-03/hash/before.txt`·`after.txt`)에서 03만 바뀜 — 04 작업 전후에도 같은 방법으로 확인할 수 있습니다(03 HTML 최종 해시 `aa1be07f9e4571b5e92c61c1328c94c94af675a7bb5dc54202290a37f7335cba`)
- 결과 읽기 채우기: 생성기 `[[READ_…]]` 자리 표시 → 두 번째 새 커널 뒤 `mdpatch.py`(`/tmp/ch08-03/fill.py` → `reps1.json`). 첫 실행 뒤 G6에 걸린 노트북 문장은 생성기를 고쳐 두 번째 실행에 반영
- 노트북 소제목 번호: 1 준비, 2 이어 쓰기, 3 Compress, 4 Isolate, 5 값 바꿔 보기, 6 Before, 7 After(02와 같은 7절 틀)
- Mermaid: 칸(subgraph) 안 세로 쌓기가 필요하면 `direction TB` + `R1 ~~~ R2 ~~~ R3`(노드 → 칸 화살표가 있으면 칸 안 `direction LR`이 무시되거나 바깥 LR을 따라감, 03-2 기록)
- `visual.cjs`: `/tmp/ch08-01/vis/vis.cjs` 그대로 + HTML 사본 폴더(`/tmp/ch08-03/html`), 1280·390 PASS

### 실행 환경

- 01·02와 같음(`$ROOT/.cache/vm/venv-ch08-context-engineering`, 새 커널 약 10초). 탐색은 `ROOT=$PWD UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch08-context-engineering uv run --project labs/part2/ch08-context-engineering python /tmp/ch08-03/probe1.py before after closure`. 토큰만 셀 때는 `/tmp/ch08-03/counts.py`(요청 없음)
- E01 원문은 같은 가상환경 pypdf로 `labs/data/rag-corpus/pdf/easy/E01.pdf` 쪽별 확인(3쪽 「4. 자료 대출」·「5. 반납과 연체」·「6. 예약과 상호대차」·「7. 열람실과 좌석 예약」 앞부분). pypdf 추출은 「정기 휴관일 입니다」「7일 연장 할」처럼 띄어쓰기가 끼므로 노트북 글은 바로잡아 적음
- 삽화: 기기 셸 `curl` + `/tmp/ch08-03/resize.py`·`cmp.py`(01 사본). 기기 루트 여유 약 600MB
- 03 노트북은 파일·폴더를 만들지 않습니다(`tempfile` 없음)

### runs 파일

- 03은 `runs/`와 `data/memory.json`을 읽지도 쓰지도 않았습니다. `runs/context-design-continuity.json` `88b3520b…`, `memory.json` `0aa9fae5…` 그대로
- Ch 8 테스트 결과 02 뒤와 같음(3 통과·알려진 실패 2). `test_ch08_source_ids_match_preserved_memory`의 03 조건은 코드 글로 지킴: 대출 기록 `내용` 「회원 한 사람의 도서 대출 기준은 7권·14일이며, …」, 휴관 기록 `내용` 「…, 공휴일이 월요일과 겹치면 다음 화요일도 휴관합니다.」. **03을 다시 만들 때 두 글을 바꾸면 테스트가 실패**합니다. 04~05는 이 테스트 조건이 없고, 06은 「회원은 최초 2시간 무료입니다.」가 있어야 하고 「90분 무료」가 없어야 함
- 실습 폴더 `context_lab.py`·`examples/ex03_compress_isolate.py`·`tests/test_ex03_compress_isolate.py`(영어 키 `fact`·`condition`·`exception`·`source`)는 개선 전 그대로이고 03 노트북은 쓰지 않음. 04에 대응하는 `ex04_failures.py`와 `runs/ex04_failures.jsonl`(SHA-256 `d23dbb45…`, `test_legacy_logs_are_unchanged`가 요구)은 **다시 실행하거나 바꾸지 않습니다**
- 해소 순서(Ch 7 요약 §9): 06 차례. 04·05는 runs를 쓰지 않음

### 03에서 새로 가르친 것

- **Python 모양**: 인자 둘 함수가 목록을 돌며 `not in`인 원소만 담아 반환(`find_missing_words`), 함수 안에서 목록 리터럴을 만들어 반환(`build_messages`, 바깥 `persona_text`·`task_text` 읽음), 딕셔너리 `copy()` 뒤 키 하나 바꾸기(Ch 2 `copy()`, 「복사본을 고쳐도 원래 딕셔너리는 그대로」 한 문장), 빈 목록 `== []` `assert`, `messages[2][1]`(Ch 7 01 인덱스 두 번), 여러 줄 딕셔너리 리터럴(키 한 줄씩), 반복문 안 `append`만 하고 끝난 뒤 `print`. 쓰지 않은 것: f-string·`raise`·try·내포식·조건 표현식·`Path`·`join`·집합 연산·`+=`·`sum`·`max`·`next`·`@`·`BaseModel`·타입힌트·`**` 풀기·반복문 안 요청과 `print`·`json`·`tempfile`·날짜 비교·`splitlines`
- **API(노트북에서 실행한 것만)**: 새 라이브러리 API 없음. `tiktoken.encoding_for_model`·`encode`(01), `init_chat_model(…, max_tokens=output_reserve)`·`invoke`·`usage_metadata`·`response_metadata["finish_reason"]`(01·02)
- **용어(본문 용어 표 6개)**: 줄이기(Compress, 원문 표현을 줄여 토큰 수를 줄이되 답에 필요한 사실과 조건은 남기는 일, 긴 공지문을 문자로 옮길 때 「단, …」 조건은 남김), 원문(줄이기 전 문서 글, 출처 표시가 가리키는 쪽의 글), **지킬 말**(이번 질문에 답하려고 원문에서 꼭 남길 말을 사람이 고른 목록), **줄인 기록**(사람이 원문을 읽고 지킬 말을 남기며 줄여 적은 기록, 키는 02 기록과 같음), 나누기(Isolate, 서로 다른 업무의 자료를 한 목록에 섞지 않고 업무마다 목록을 따로 만들어 보내는 일, 과목별 공책), 업무별 메시지 목록(요청 하나에 목록 하나). 「요약」은 모델이 만드는 요약(Ch 16 03·Ch 22 03)에만 씀. 「조각」「청크」「틀」「빈자리」「칸(필드)」「서류철」「압축본」「독립 메시지」 안 씀. 「확인 단어 표시」(Ch 7 01)를 「예약」 `in` 확인에 이어 씀(품질 점수 아님)
- **이어 쓸 이름과 값**: `persona_text`·`task_text`(02와 같음), 600/120/40 → `available = 440`, `input_budget()`·`count_tokens()`·`encoding`, `model`(출력 상한 120), `loan_original`(E01 3쪽 「4. 자료 대출」 세 문단, 243자·141토큰), `loan_question = "미르시립도서관에서 빌린 도서의 대출 기간을 연장할 수 있나요?"`, `keep_words = ["7권", "14일", "예약이 없는 경우", "1회", "7일 연장"]`, `find_missing_words(text, words)`, `note_02_text`(02 대출 기록 글, 16토큰), `loan_note = {"출처": "E01 p.3", "기관": "미르시립도서관", "주제": "대출", "내용": "회원 한 사람의 도서 대출 기준은 7권·14일이며, 다른 이용자의 예약이 없는 경우에만 1회 7일 연장할 수 있습니다."}`(66자·39토큰), `closure_note`(E01 p.2 휴관, 「매주 월요일은 정기 휴관일이고 법정 공휴일에도 휴관하며, 공휴일이 월요일과 겹치면 다음 화요일도 휴관합니다.」, 40토큰), `closure_question`(01 질문과 같음), `closure_keep_words = ["월요일", "법정 공휴일", "화요일"]`, `build_messages(note, question)`(user 글 = `"[" + 출처 + "] " + 내용 + "\n\n" + "질문: " + 질문`), `loan_messages`·`closure_messages`, `shared_tokens = 55`, `loan_estimate = 128`·`closure_estimate = 136`, `find_cited_notes(answer_text, notes)`(02와 같은 코드), `all_notes`, `mixed_user_text`(두 기록 + 「질문 1:」「질문 2:」)·`mixed_estimate = 213`·`separated_total = 264`, `dropped_note`(조건 뺀 기록, 추정 119), `before_messages`·`before_response`·`after_response`. 출력 라벨 「원문:」「원문 글자 수:」「원문 토큰 수:」「질문:」「지킬 말:」「원문에서 빠진 지킬 말:」「02절 대출 기록에서 빠진 지킬 말:」「02절 대출 기록 토큰 수:」「줄인 기록에서 빠진 지킬 말:」「줄인 기록 글자 수:」「줄인 기록 토큰 수:」「휴관 기록에서 빠진 지킬 말:」「휴관 기록 토큰 수:」「대출 목록 user 글:」「대출 목록에 휴관 출처가 있는가:」「휴관 목록에 대출 출처가 있는가:」「페르소나 + 과업 명세 토큰 수:」「대출 목록 추정 입력 합계:」「휴관 목록 추정 입력 합계:」「대출 목록이 입력 가용분 안에 드는가:」「휴관 목록이 입력 가용분 안에 드는가:」「답:」「실제 입력 토큰 수:」「실제 출력 토큰 수:」「끝난 이유:」「답의 출처 표시와 같은 기록:」(출처 목록)「한 목록에 두 출처가 모두 있는가:」「한 목록 추정 입력 합계:」「나눈 두 목록 추정 입력의 합:」「조건을 뺀 기록에서 빠진 지킬 말:」「3절 줄인 기록에서 빠진 지킬 말:」「추정 입력 합계:」「답에 「예약」이 있는가:」「실제 입력 - 추정 입력:」「차이가 여유분 안에 드는가:」
- **실행값(2026-09-17, 두 번째 새 커널)**: 휴관 답 「미르시립도서관의 정기 휴관일은 매주 월요일이며, 법정 공휴일에도 휴관합니다. [E01 p.2] 공휴일이 월요일과 겹치면 다음 화요일도 휴관합니다. [E01 p.2]」 150/66/stop, Before 답 「네, 미르시립도서관에서 빌린 도서는 1회 7일 연장할 수 있습니다. [E01 p.3] 대출 기준은 7권·14일입니다. [E01 p.3]」 133/56/stop·「예약」 False, After 답 「네, 다른 이용자의 예약이 없는 경우에만 1회 7일 연장할 수 있습니다. [E01 p.3] 대출 기준은 7권·14일입니다. [E01 p.3]」 142/52/stop·차이 14·「예약」 True. 메시지 3개 목록의 추정과 실제 차이는 01·02·03 모든 목록에서 14(「이번 목록에서도」로만 씀). 나눈 두 목록 합 264 > 한 목록 213(「이번 예에서 나누기는 전체 토큰을 줄이지 않았다」)
- **비유**: 01·02 긴 책상 → 떨어져 선 작은 나무 책상 두 개(= 대출·휴관 업무별 메시지 목록, 사이 빈 바닥 = 따로 보내는 요청), 책상마다 파란 명찰·주황 클립보드·노란 메모지·빈 답안지와 연필·초록 탭 카드. 왼쪽 책상 앞 바닥 긴 종이(= E01 3쪽 원문)의 초록 형광 띠(= 지킬 말), 초록 형광펜, 왼쪽 카드의 칠한 세 줄(= 줄인 대출 기록), 오른쪽 카드 회색 줄(= 휴관 기록). 칠한 줄 수 ≠ 지킬 말 개수. 02 기록 카드 상자는 그림에 없음. 04가 책상을 이어 쓰면 「한 책상에 섞인 카드」로 실패 모드를 그릴 수 있음(그리게 되면 그림 읽기에 뜻 적기)
- **그림 색(03)**: 원문·목록·사람이 정한 지킬 말 초록, 함수(`find_missing_words`·`build_messages`) 파랑, `gpt-5.4-mini` 보라, 검사 출력·추정 입력·After 답 노랑(02 기록의 빠진 말 세 개도 노랑 — 검사가 받아 출력한 값), 실행하지 않은 요청 회색(점선), 빨강은 03-4 Before 결과 한 상자
- **04절이 이어받을 연결**: 03 본문 b8·노트북 끝 「04절에서는 컨텍스트에 넣은 자료 때문에 답이 틀어지는 경우를 네 가지 이름으로 나눠 봅니다. 줄이다가 빠진 조건이나 다른 업무의 자료가 섞인 목록도 그런 경우의 예입니다.」(노트북은 첫 문장만). 03 b5 「넣은 자료 때문에 답이 틀어지는 경우는 04절에서 다룹니다」. 개선 전 04 `_src` b3 「Compress — … 요약 과정에서 조건이 빠지면 원문과 다른 주장처럼 사용될 수 있습니다」는 03 Before(조건 뺀 줄인 기록 → 조건 없는 답)와 맞음. 단 **개선 전 04 b3 「Select — 현재 질문과 관련된 문서 조각만 고릅니다」는 「조각」(Ch 5 = 토큰) → 02 용어 「기록」으로**, b3 Isolate 설명도 03 「업무마다 메시지 목록을 따로 만듦」으로 맞춰 주세요. 04가 한 목록에 여러 자료를 넣어 보내면 03 5절(한 목록은 보내지 않음)을 「이번에 보냅니다」로 이을 수 있음
- **주의 — 개선 전 04 노트북 기준 근거가 E01 원문과 다름**: 셀 8 `clean = "[E01 p.2] 미르시립도서관의 정기 휴관일은 오직 매주 월요일 하루뿐입니다."` — E01 2쪽 원문(01 근거 문단·03 휴관 기록)은 법정 공휴일에도 휴관하고 공휴일이 월요일과 겹치면 화요일도 휴관합니다. 「오직 … 하루뿐」은 원문과 어긋나므로 04가 01·03 휴관 기록을 기준으로 쓰면 Clash 조건(「오직 매주 화요일 하루뿐」)도 함께 다시 설계해야 합니다. 셀 23의 합성 `effective_date`·「합성 부록」도 02에서 뺀 합성 메타데이터와 같은 문제
- **개선 전 04 노트북이 쓰는 것 중 01~03·Ch 6·7·Part 1에서 안 가르친 것**: 공용 셀 `raise FileNotFoundError`·`raise RuntimeError`, 모델 셀 `max_tokens=300`(temperature 누락), 딕셔너리 값 f-string 삼중 따옴표, 반복문 안 `model.invoke` + `print(f"\n[{name}] …")`(반복문 안 print 금지), `if usage is None: raise RuntimeError`, `"문장" * 12` 글 반복 곱하기, 튜플 `("월요일", "화요일", "수요일")`을 `for`로, `or` 세 개 이은 `in` 검사, `max(eligible, key=effective_date)`(내장 `max`·key 인자), 타입힌트 `dict[str, str]`, `splitlines()[-1]`, 날짜 글 비교 `<=`, `model.invoke([...])` 인자 안 목록 리터럴, 영어 조건 이름(`clean`·`poisoning`…)과 라벨 `input_tokens=`
- **아직 안 가르친 것(04가 설명 없이 전제하면 안 됨)**: §02 목록 전체 + 03에서도 안 한 것: 모델에게 요약·줄이기 맡기기(Ch 16 03·Ch 22 03), 지킬 말을 코드가 원문에서 뽑기, 뜻 보존 자동 판정·답 정확성 판정, 한 목록에 두 업무를 넣어 실제로 보낸 결과(03은 추정만), 여러 요청 반복 보내기(03은 목록마다 셀 하나), 서브에이전트·에이전트·도구 호출(Ch 19~26), 접근 권한·보안 격리, 글 곱하기 `*`, 내장 `max`·`key=` 인자, `splitlines`, 날짜 비교, 여러 줄 삼중 따옴표 글(01~03은 글 `+` 다시 담기)

## §04 → §05

(04절 품질 개선 2026-09-17. 결과는 `04-diagnosis.md`, 게이트 G1~G7 0(수정 전 G4 1·G5 13·G6 33·G7 3), 코드 셀 29(준비 3), 노트북 모델 호출 5번(탐색 7 + 새 커널 2회 × 5 = 합계 17). 삽화 04-5 채택(job `f9a8c66e-…`, 잔액 2840), Mermaid 4장. 최종 `outputs_sha256` `017eafb9…`)

### 빌더·검사(§01~§03 인계 그대로 동작 확인)

- `_build.py`는 고치지 않았습니다. 토큰 세 모양 모두 01 인계대로 동작. `verify.py --chapter` → `PASS 6 sections / 127 code cells (max 25 lines)`(max 25는 개선 전 05·06). 빌드 HTML `{{` 0건. 작업 전후 챕터 HTML 해시(`/tmp/ch08-04/hash/before.txt`·`after.txt`)에서 04만 바뀜(04 HTML 최종 해시 `a065f1cfebb378b3c648983e56fda1958ddce123e18c026595e6322b382b8785`). 05 작업 전후에도 같은 방법으로 확인
- 결과 읽기 채우기: 생성기 `[[READ_…]]` 자리 표시 → 두 번째 새 커널 뒤 `mdpatch.py`(`/tmp/ch08-04/fill.py` → `reps1.json`). 노트북 소제목 번호: 1 준비, 2 이어 쓰기, 3 혼란, 4 충돌, 5 값 바꿔 보기, 6 Before, 7 After(02·03과 같은 7절 틀)
- Mermaid: 4개 상자를 한 줄에 둔 TB는 라벨이 한 줄이면 폭 873 → 라벨을 `<br>` 세 줄로 848(04-1). 긴 출처 목록 라벨은 `<br>` 위치를 직접 정해야 「E02 / p.2」로 끊기지 않음(04-2)
- `visual.cjs`: `/tmp/ch08-01/vis/vis.cjs` 그대로 + HTML 사본 폴더(`/tmp/ch08-04/html`), 1280·390 PASS

### 실행 환경

- 01~03과 같음(`$ROOT/.cache/vm/venv-ch08-context-engineering`, 새 커널 약 15초). 탐색은 `ROOT=$PWD UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch08-context-engineering uv run --project labs/part2/ch08-context-engineering python /tmp/ch08-04/probe1.py base confusion …`
- E01·E02 쪽별 원문: `/tmp/ch08-04/pages.py E01 E02`(같은 가상환경 pypdf, 「공휴일」「주차」가 든 쪽만 출력)
- 삽화: 클라우드 컨테이너 scratchpad에서 `curl`로 받아 후보를 먼저 보고(Read), 채택 뒤 기기 셸 `curl` + `/tmp/ch08-04/resize.py`·`cmp.py`(01 사본)로 저장·픽셀 대조. 기기 루트 여유 약 590MB
- 04 노트북은 파일·폴더를 만들지 않습니다

### runs 파일

- 04는 `runs/`와 `data/memory.json`을 읽지도 쓰지도 않았습니다. `runs/context-design-continuity.json` `88b3520b…`, `runs/ex04_failures.jsonl` `d23dbb45…`, `memory.json` `0aa9fae5…` 그대로
- Ch 8 테스트 결과 03 뒤와 같음(3 통과·알려진 실패 2). 테스트는 04·05 노트북을 읽지 않음. **`runs/ex05_rot.jsonl`(SHA-256 `6a9db927…`)은 `test_legacy_logs_are_unchanged`가 요구** → 05 작업 때 `examples/ex05_rot.py`를 다시 실행하거나 파일을 바꾸지 않음. `tests/test_ex05_rot.py`는 예제 파일을 읽음(노트북 아님, 확인해 볼 것)
- 해소 순서(Ch 7 요약 §9): 06 차례. 05는 runs를 쓰지 않음

### 04에서 새로 가르친 것

- **Python 모양**: 함수 안 반복문에서 글을 `+`로 같은 이름에 다시 담아 반환(`build_notes_messages`, 01의 글 이어 붙이기를 함수 안에서), 함수가 앞 셀에서 정의한 두 함수를 불러 결과를 한국어 키 딕셔너리로 반환(`check_answer`), 한 줄 딕셔너리 리터럴 여러 개(02 모양), 메시지 목록 `==` + `assert`(Ch 7 01), 딕셔너리 `print` 한 줄(02), 뺄셈 식을 `print` 인자로. 쓰지 않은 것: f-string·`raise`·try·내포식·조건 표현식·`Path`·`join`·집합 연산·`+=`·`sum`·`max`·`next`·`@`·`BaseModel`·타입힌트·`**` 풀기·반복문 안 요청과 `print`·`json`·`tempfile`·글 곱하기 `*`·`splitlines`·`count()`·날짜 비교·`range()`로 요청 반복·assistant 튜플·`AIMessage` 직접 만들기
- **API**: 새 라이브러리 API 없음. `tiktoken.encoding_for_model`·`encode`(01), `init_chat_model(…, max_tokens=output_reserve)`·`invoke`·`usage_metadata`·`response_metadata["finish_reason"]`(01~03)
- **용어(본문 용어 표 6개)**: 실패 모드(컨텍스트에 넣은 자료 때문에 답이 틀어지는 경우를 모양별로 나눈 이름, 공식 오류 코드 아님), **컨텍스트 오염**(Context Poisoning, 환각이나 다른 오류가 컨텍스트에 들어가 뒤에서 되풀이해 쓰임), **컨텍스트 산만**(Context Distraction, 아주 긴 컨텍스트에 치우쳐 모델이 학습한 것을 덜 씀 — 실행 안 함), **컨텍스트 혼란**(Context Confusion, 필요 없는 내용이 컨텍스트에 있어 모델이 그 내용을 답에 써서 답이 나빠짐), **컨텍스트 충돌**(Context Clash, 새로 쌓인 정보가 컨텍스트 안의 다른 정보와 맞지 않음), 기준 목록(휴관 기록 하나만 넣은 목록). 출처: Drew Breunig 「How Long Contexts Fail」(2025-06-22)·LangChain 「Context Engineering」(2025-07-02), **확인 2026-09-17**. 개선 전 04 정의(혼동 = 비슷한 대상, 산만화 = 무관한 정보로 근거 놓침)는 원글과 달라 뺐음
- **산만과 컨텍스트 로트(05가 반드시 이을 것)**: 04 b4 「산만과 컨텍스트 로트」 — 「두 말 모두 긴 컨텍스트를 다룹니다. Ch 5 05절의 컨텍스트 로트는 입력이 길어질수록 필요한 정보를 찾아 쓰는 결과가 나빠지는 현상입니다. 길이를 바꿔 가며 재는 말입니다. 산만은 긴 기록 때문에 모델이 기록 속 내용에 치우친 사례에 붙인 이름입니다. 입력 길이에 따른 변화는 05절에서 같은 근거를 두고 잽니다.」 → 05는 「컨텍스트 로트」(Ch 5 05 용어, Part 1 §5 「입력 길이 기준」)로 쓰고, 산만을 측정했다고 쓰지 않음. 05 제목 「Context rot 측정」의 영어 표기는 챕터 마감·05 작업자가 판단(용어 표에 한국어 「컨텍스트 로트」를 먼저)
- **이어 쓸 이름과 값**: `persona_text`·`task_text`(02·03과 같음), 600/120/40 → `available = 440`, `input_budget()`·`count_tokens()`·`encoding`, `model`(출력 상한 120), `closure_note`(03과 같은 글, E01 p.2), `closure_question`(01·03과 같음), `closure_keep_words = ["월요일", "법정 공휴일", "화요일"]`, `find_missing_words(text, words)`(03), `find_cited_notes(answer_text, notes)`(02), **`build_notes_messages(notes, question)`**(user 글 = 기록마다 `"[" + 출처 + "] " + 내용 + "\n"` + `"\n" + "질문: " + question`, 기록 하나면 03 `build_messages()`와 같은 글), **`check_answer(answer_text, notes)`** → `{"답의 출처 표시와 같은 기록": [...], "답에서 빠진 지킬 말": [...]}`(바깥 `closure_keep_words` 읽음), `base_notes`·`base_messages`·`shared_tokens = 55`·`base_estimate = 136`, `loan_note`(03)·`parking_note`(02 「회원은 최초 2시간 무료입니다.」)·`pay_note`(E02 p.2 별빛제과 급여 「급여는 매월 25일에 지급되며, 25일이 주말이나 공휴일이면 그 전 영업일에 지급합니다.」), `confusion_notes`(4개, 추정 235), `memo_note`(출처 「상담 메모」, 「미르시립도서관은 매주 월요일 하루만 휴관하고, 공휴일에는 문을 엽니다.」 — 일부러 틀린 글), `clash_notes`(추정 170)·`reversed_notes`, `before_notes`(124)·`after_notes`. 출력 라벨 「휴관 기록 출처:」「질문:」「지킬 말:」「기준 목록 user 글:」「기준 목록 추정 입력 합계:」「혼란 목록 기록 수:」「혼란 목록 기록 출처:」「혼란 목록 추정 입력 합계:」「기준 목록보다 늘어난 토큰 수:」「입력 가용분 안에 드는가:」「답:」「실제 입력 토큰 수:」「실제 출력 토큰 수:」「끝난 이유:」「혼란 목록 답 검사:」「충돌 목록 user 글:」「충돌 목록 추정 입력 합계:」「충돌 목록 답 검사:」「순서를 바꾼 목록의 첫 기록 출처:」「순서를 바꾼 목록 추정 입력 합계:」「충돌 목록과 추정 입력이 같은가:」「순서를 바꾼 목록 답 검사:」「Before 목록 기록 출처:」「Before 목록 추정 입력 합계:」「Before 답 검사:」「상담 메모 출처:」「상담 메모에서 빠진 지킬 말:」「After 목록 기록 출처:」「실제 입력 - 추정 입력:」「차이가 여유분 안에 드는가:」「After 답 검사:」
- **실행값(2026-09-17, 두 번째 새 커널)**: 혼란·충돌·순서 바꿈·After 답은 모두 「미르시립도서관의 정기 휴관일은 매주 월요일이며, 법정 공휴일에도 휴관합니다. [E01 p.2] 공휴일이 월요일과 겹치면 다음 화요일도 휴관합니다. [E01 p.2]」(실제 입력 249·184·150, 순서 바꿈 셀은 사용량을 출력하지 않음, 출력 66), 검사 `['E01 p.2']`·`[]`. Before 답 「미르시립도서관의 정기 휴관일은 매주 월요일입니다 [E01 p.2]. 공휴일에는 문을 열며, 공휴일이 월요일과 겹쳐도 휴관하지 않습니다 [E01 p.2].」 138/60, 검사 `[]`·`['법정 공휴일', '화요일']`(첫 새 커널은 같은 문장에 `[상담 메모]` — 교재에는 쓰지 않음). 추정과 실제 차이 14는 01~04 모든 메시지 3개 목록에서 같음(「이번 목록에서도」로만)
- **결론 태도**: 혼란·충돌 조건은 「넣었고, 이번 답에서는 보이지 않았다」로만 씀(늘 괜찮다고 하지 않음), 원인 보류(모델이 왜 휴관 기록을 따랐는지, Before가 왜 `[E01 p.2]`를 적었는지 — 과업 명세 예시와 같은 모양까지). 05의 「길이를 늘려도 정답 유지」도 같은 태도로 쓸 수 있음
- **비유**: 03 떨어진 작은 책상 두 개 → 2×2 책상 네 개(= 조건마다 따로 보낸 목록). 노란 메모지 = 질문, 답안지와 연필 = 출력 예약분, 초록 탭 카드 = 휴관 기록(02·03 고른 기록), 회색·보라 탭 카드 = 필요 없는 기록, 찢어진 갈색 종잇조각 = 상담 메모, 답안지 갈색 물결 줄 = 메모를 따라 적은 답(오염), **왼쪽 아래 아주 높은 흰 종이 더미 = 아주 긴 컨텍스트(산만, 실행 안 함)**. 파란 명찰·주황 클립보드는 04 그림에서 뺌. 05가 긴 입력을 그리면 「높은 종이 더미 사이에 초록 탭 카드 한 장」으로 이을 수 있으나, 04에서는 그 더미를 「산만」으로 불렀으므로 05 그림 읽기에서 「이번에는 컨텍스트 로트를 재는 긴 입력」이라고 뜻을 다시 적을 것
- **그림 색(04)**: 넣은 기록·목록·상담 메모 초록(틀린 글이어도 넣은 기록), `find_missing_words` 파랑, `gpt-5.4-mini` 보라, 답 검사 출력 노랑, 실행하지 않은 산만 회색(점선), 빨강은 04-3 Before 결과 한 상자. 04-3은 두 답 공통 「정기 휴관일은 매주 월요일」·출처 표시 모양을 결과 상자에서 뺌
- **05절이 이어받을 연결**: 04 본문 b8·노트북 끝 「05절에서는 같은 근거를 둔 채 입력 길이만 늘려, 답이 달라지는지 잽니다.」, b4 「입력 길이에 따른 변화는 05절에서 같은 근거를 두고 잽니다」. 05가 질문·근거를 바꾸면 이 두 문장을 `mdpatch.py`로 확인(04 재실행 불필요)
- **주의 — 개선 전 05 노트북 기준 근거·예산이 01~04와 어긋남**: 셀 6 `evidence = "[E01 p.2] 정기 휴관일은 매주 월요일입니다."`(법정 공휴일·화요일 조건 없음 = 02 기록 글, 03 Compress 관점에서는 조건이 빠진 기록)·질문 「정기 휴관일과 출처를 알려 주세요」. 01~04의 휴관 질문·`closure_note`로 이을지, 짧은 질문을 유지하고 「02절 휴관 기록 글」이라고 밝힐지 정할 것. **셀 8 입력은 64·2,224·21,664토큰으로 01~04 수업 예산 600(입력 가용분 440)을 크게 넘음** → 05가 길이를 늘리려면 「수업 예산 600은 01절에서 흐름을 보여 주려고 정한 예」(01 b7)를 잇고, 이번 측정용 예산(또는 모델 컨텍스트 윈도 400,000, 01 용어 표)을 새로 정해 한 문장으로 밝힐 것. 비용: 21,664토큰 입력 한 번 약 0.016달러(mini 0.75/100만), 세 번이면 0.05달러 — 준비물 비용 문장 확인
- **개선 전 05 노트북이 쓰는 것 중 01~04·Ch 6·7·Part 1에서 안 가르친 것**: 공용 셀 `raise FileNotFoundError`·`raise RuntimeError`, 모델 셀 `max_tokens=300`(temperature 누락), **글 곱하기 `note * count`**, `for name, count in repeat_counts.items()`(Ch 2 `items()`는 배웠음) 안 f-string 삼중 따옴표, `prompt.count(evidence)`(`count()` 미교육), 비교 연쇄 `a < b < c`, **두 겹 `for trial in range(1, 4)` 안 `model.invoke` + `print`(반복문 안 요청·print 금지)**, 목록 내포 `[record for record in records if …]`·`sum(… for …)`·제너레이터 식, 영어 조건 이름(`short`·`medium`·`long`)·영어 키(`length`·`trial`·`input_tokens`·`answer`·`keyword_pass`), 라벨 없는 여러 줄 `print(record["answer"])`. 글 곱하기 대신 01의 같은 이름에 `+`로 다시 담기는 반복 횟수가 커서 셀이 길어짐 → 반복문 안에서 글 `+` 다시 담기(04 `build_notes_messages` 모양, 요청 없음)로 만들 수 있음. 반복 요청은 조건마다 셀 하나(요청 수·비용 줄이기 검토)
- **아직 안 가르친 것(05가 설명 없이 전제하면 안 됨)**: §03 목록 전체 + 04에서도 안 한 것: 산만 재현(아주 긴 컨텍스트), 한 답에 여러 실패 이름이 겹치는 실제 재현, 대화 기록에 틀린 앞선 답을 넣기(assistant 튜플·`AIMessage`), 문서 속 프롬프트 인젝션(Ch 16 06), 도구가 많을 때의 혼란(Ch 19 04), 검색이 가져온 자료(Ch 9 05), 모델에게 기록을 고르거나 대조하게 하기, 뜻 보존 자동 판정·답 정확성 판정·비율 지표, 같은 조건 반복 요청으로 평균 내기, 입력 가용분을 넘는 입력을 실제로 보내기(01은 추정만), 근거 위치(앞·가운데·뒤) 바꾸기(Ch 5 05는 로컬 모델에서 자리 차이를 봄 — 서비스 모델에서는 아직), 긴 입력의 비용·지연 측정

## §05 → §06

(05절 품질 개선 2026-09-17. 결과는 `05-diagnosis.md`, 게이트 G1~G7 0(수정 전 G1 3·G2 1·G4 1·G5 13·G6 14·G7 3), 코드 셀 27(준비 3), 노트북 모델 호출 4번(탐색 9 + 새 커널 2회 × 4 = 합계 17, 비용 어림 약 0.09달러). 삽화 05-5 채택(job `e377f5dd-…`, 생성 전 잔액 2840 → 2크레딧), Mermaid 4장. 최종 `outputs_sha256` `b3aac7ca…`. 형식 experiment 유지(b6 「실험 결과 해석」, 코드 없음))

### 06이 할 일 — runs 사슬을 새로 실행해 잇는 차례 (먼저 읽을 것)

- **05는 `runs/`와 `data/memory.json`을 읽지도 쓰지도 않았습니다.** `runs/context-design-continuity.json` SHA-256 `88b3520bb65415b39acf7f805a9769ed01918ef57f63c307474ab9f5c5ba77aa`(옛 출처 `source_record.sha256` `e124b791…`, run_id `ch07-prompt-ab-20260909T174009751770Z`), `ex01_budget.jsonl` `e3b6a71d…`·`ex04_failures.jsonl` `d23dbb45…`·`ex05_rot.jsonl` `6a9db927…`·`ex06_compare.jsonl` `5cb060d6…`, `memory.json` `0aa9fae5…`, Ch 7 `prompt-ab-continuity.json` `a8aaafb7…82095e9`, Ch 6 `f18920c6…4f4c` 모두 그대로. Ch 8 테스트 결과 04 뒤와 같음(3 통과·알려진 실패 2: `test_log_paths_are_portable…`·`test_continuity_logs_form_a_hash_verified_chain` 103행)
- **06 차례(Ch 7 요약 §9 해소 순서 (3))**: 06 품질 개선 때 새 커널로 실행해 `context-design-continuity.json`의 `source_record`를 현재 Ch 7 파일(`path` `labs/part2/ch07-prompt-engineering/runs/prompt-ab-continuity.json`, `sha256` `a8aaafb775e710438a1bd9e5d79340d3032f61be30c4dbb2e8aa4dd7b82095e9`, `run_id` `ch07-prompt-ab-20260917T070701`)로 잇고, 같은 바이트 사본 `runs/continuity/<실행 시각>/context-design-continuity.json`을 만듭니다. 그 뒤 테스트 ②와 `check_course_continuity.py` 73행 통과 확인, 테스트 ① 수정은 (4) 순서. **06 실행 뒤 Ch 7 08·Ch 6 06을 다시 실행하지 않습니다**
- **06 파일 계약(읽는 쪽 확인, 개선 전 파일 기준)**: 최상위 키 9개 `run_id`·`run_date`·`source_chapter`·`source_record{path, sha256, run_id}`·`model`·`settings{max_tokens, pricing_date, pricing_usd_per_million}`·`question`·`comparison_policy`·`results`(목록 3개, 원소 키 `design`·`context`·`answer`·`usage`·`latency_ms`·`cache_read_tokens`·`estimated_cost_usd`·`checks`). 읽는 쪽이 요구하는 것: 테스트 ② `ch08["source_record"]["run_id"]`·`["sha256"]`, `ch08["settings"]["pricing_usd_per_million"] == {0.75, 0.075, 4.50}`, **`len(ch08["results"]) == 3`**. `check_course_continuity.py` 64~74행 `source_record.path` 상대 경로·지문·run_id·`runs/continuity/*/` 같은 바이트 사본. `run_course_bundle.py` 104~111행 `source_record.sha256`·`path`, `build_bundle.py` 81~87행 파일 있음. `results` 안 키·다른 최상위 키는 읽는 쪽이 없음(한국어 키로 바꿔도 위 조건은 통과) → 바꾸면 계약을 챕터 요약에 적기
- **`estimate_openai_cost`**: 테스트 `test_cached_input_cost…`가 **06 노트북** 코드 셀에서 이 이름의 함수를 꺼내 인자 하나로 `== 0.000093`을 요구합니다. 05 노트북은 Ch 7 08절과 같은 코드 `estimate_openai_cost(usage, input_rate=0.75, cached_input_rate=0.075, output_rate=4.50)`(`if usage is None: return None`, `usage.get("input_token_details", {})`, `details.get("cache_read", 0)`, `price_unit = 1000000`)를 정의해 썼습니다. 06이 같은 코드를 쓰면 테스트를 통과합니다(Ch 7 08 같은 코드로 통과 확인됨). 개선 전 06 셀 20은 기본값 없는 다른 본문(`or {}`·`1_000_000`)
- 06 개선 전 노트북 셀 8·27은 `next(… for …)`·`[Path.cwd(), *Path.cwd().parents]`·`raise`·`from hashlib import sha256`·집합 `<=`·`datetime`·f-string·`mkdir(parents=True, exist_ok=False)`을 씁니다. Ch 7 요약 §4 대로 Ch 7 08 모양(`os.path.exists("../runs")` + 긴 경로, `hashlib.sha256(바이트).hexdigest()`, `time.strftime("%Y%m%dT%H%M%S")`, `os.makedirs(경로)`)으로 바꿀 수 있고, R-1(실습 폴더 맨 위에서 열면 경로를 못 찾음) 제한이 함께 생깁니다. 테스트 ① 문자열 조건(`[Path.cwd(), *Path.cwd().parents]`·`runs_dir = course_root`)은 해소 순서 (4)에서 고칠 대상
- **`test_ch08_source_ids_match_preserved_memory`의 06 조건**: 06 노트북 원문에 「회원은 최초 2시간 무료입니다.」가 있어야 하고 「90분 무료」가 없어야 함(개선 전 셀 10 `E01-p5` 문서 글). 06 문서 글을 02 `records`·04 `parking_note` 글로 이으면 그대로 통과

### 빌더·검사(§01~§04 인계 그대로 동작 확인)

- `_build.py`는 고치지 않았습니다. `{{mermaid:}}`·세 칸 `{{img:}}`·experiment `{{notebook:slug}}` 모두 동작. `SECTIONS` 제목 「05 · Context rot 측정」은 유지(바꾸면 04·06·index HTML 해시가 바뀜, 마감 때 판단). `verify.py --chapter` → `PASS 6 sections / 145 code cells (max 25 lines)`(max 25는 개선 전 06). 빌드 HTML `{{` 0건. 작업 전후 챕터 HTML 해시(`/tmp/ch08-05/hash/before.txt`·`after.txt`)에서 05만 바뀜(05 최종 `dbf1d47b6c2b87818634dc0625a2ad789f9b4a8b3d7e10a88433f2a01789d81c`, 06 `97b9ebfe…`·index `ea87325b…` 그대로)
- 결과 읽기 채우기: 생성기 `[[READ_…]]` 자리 표시 → 두 번째 새 커널 뒤 `mdpatch.py`(`/tmp/ch08-05/fill.py` → `reps1.json`). 노트북 소제목: 1 준비, 2 이어 쓰기(04 함수 같은 코드), 3 측정 목록, 4 기록 함수, 5 세 길이 요청, 6 값 바꿔 보기, 7 기록표, 실험 결과 해석, 정리
- G6: 노트북 준비물 단락이 빈 줄 없이 6문장이면 걸림(05 첫 실행). 참고 자료 한 줄 설명도 70자 넘으면 걸림
- Mermaid: 칸 안 세로 쌓기 `direction TB` + `l10 ~~~ l100`(03 인계 방법)으로 05-3을 만듦. 긴 라벨은 `<br>` 위치를 직접 정함(05-1)
- `visual.cjs`: `/tmp/ch08-01/vis/vis.cjs` 그대로 + HTML 사본 폴더(`/tmp/ch08-05/html`), 1280·390 14건 PASS

### 실행 환경

- 01~04와 같음(`$ROOT/.cache/vm/venv-ch08-context-engineering`, 새 커널 약 10초 — 3만 토큰 요청도 1~2초). 탐색은 `ROOT=$PWD UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch08-context-engineering uv run --project labs/part2/ch08-context-engineering python /tmp/ch08-05/probe1.py 10:middle 1000:first …`(`/tmp/ch08-05/common.py`에 01~04 글·함수 사본), 토큰만 `counts.py`
- 삽화: 클라우드 `/mnt/user-data/outputs`는 쓰지 않고 기기 셸 `curl` + `/tmp/ch08-05/resize.py`·`cmp.py`(04 사본). 기기 루트 여유 약 585MB
- **캐시 입력 주의**: 같은 입력을 몇 분 안에 다시 보내면 `usage_metadata["input_token_details"]["cache_read"]`가 생겨 예상 비용이 크게 달라짐(05 두 번째 새 커널 1000개 목록 32000/32150, 0.024338 → 0.002773). 06이 설계별 비용을 비교하면 탐색·첫 실행 뒤 두 번째 실행의 캐시 입력을 반드시 함께 적고, 비교 결론에서 캐시 차이를 설계 효과로 쓰지 않기

### 05에서 새로 가르친 것

- **Python 모양**: `range(수)`로 같은 원소를 정한 횟수만큼 `append`(함수 안 두 반복문, Ch 2), `int` 인덱스 리터럴 `notes_1000[500]`, 글 `split(표시 글)` 뒤 `len(pieces) - 1`로 표시 수 세기(Ch 7 `split(", ")` 모양), 딕셔너리 리터럴을 함수 인자로(`estimate_openai_cost({"input_tokens": …, "output_tokens": …})`), 함수가 반환한 딕셔너리에 `record[키] = 값`으로 키 더하기(Ch 7 08 `add_cost_items` 모양), 비교식 여러 개를 `print` 인자로, 이미 받은 기록만 반복문에서 `print`(요청 없음, Ch 7 01 기록표 모양)와 `total_cost = total_cost + …`, `round(값, 6)`. 쓰지 않은 것: f-string·`raise`·try·내포식·조건 표현식·`Path`·`join`·집합 연산·`+=`·`sum`·`max`·`next`·`@`·`BaseModel`·타입힌트·`**` 풀기·반복문 안 요청·요청을 기다리는 반복문 안 `print`·`json`·`tempfile`·글 곱하기·`count()`·`splitlines`·`time`·`hashlib`
- **API**: 새 라이브러리 API 없음. `usage_metadata["input_token_details"]["cache_read"]`(Ch 6 06 값, 인덱스로 직접 꺼냄), `estimate_openai_cost`(Ch 7 08 같은 코드), 01~04 API
- **용어(본문 용어 표 6개)**: 컨텍스트 로트(context rot, Ch 5 05와 같은 뜻 = 입력이 길어질수록 필요한 정보를 찾아 쓰는 결과가 나빠지는 현상, 04 산만과 다른 말), 무관한 기록(질문과 관계없이 입력을 길게 만드는 기록, Ch 5 05 무관한 문장과 같은 역할), 근거 앞 기록 수(휴관 기록 앞 무관한 기록 수 = 자리), 같게 둔 조건(개선 전 「통제 조건」), 측정 입력(길이에 따른 답 변화를 재려고 만든 입력, 수업 예산을 일부러 넘김), 출처 표시 수(답 글의 `[E01 p.2]` 횟수). 본문에 「요청 전 비용 상한」(캐시 없음·출력 예약분 전부 가정)도 씀. 「조각」「청크」「틀」「빈자리」「칸(필드)」 안 씀
- **이어 쓸 이름과 값**: `persona_text`·`task_text`(02~04 같음), 600/120/40 → `available = 440`, `input_budget()`·`count_tokens()`·`encoding`, `model`(출력 상한 120), `closure_note`·`closure_question`·`closure_keep_words`(03·04), `find_missing_words()`(03)·`find_cited_notes()`(02)·`build_notes_messages()`·`check_answer()`(04), **`filler_note`**(`{"출처": "E02 p.5", "기관": "별빛제과", "주제": "주차", "내용": "본사 주차장은 선착순이며 월 3만 원의 주차비가 급여에서 공제됩니다."}`, user 글 한 줄 32토큰), `filler_line`, **`build_long_notes(filler_count, before_count)`**, `notes_10`·`notes_100`·`notes_1000`·`notes_0`, `messages_*`, `shared_tokens`, `estimate_10 = 456`·`estimate_100 = 3336`·`estimate_1000 = 32136`·`estimate_0 = 136`, `context_window = 400000`, **`estimate_openai_cost(usage, input_rate=0.75, cached_input_rate=0.075, output_rate=4.50)`**, `planned_*`, **`count_marks(answer_text, mark)`**, **`make_length_record(filler_count, run_response)`** → `check_answer` 두 키 + `무관한 기록 수`·`실제 입력 토큰 수`·`캐시 입력 토큰 수`·`출처 표시 수`·`예상 비용(달러)`, `response_*`·`record_*`, `length_records`, `total_cost`. 출력 라벨 「무관한 기록 출처:」「무관한 기록에서 빠진 지킬 말:」「무관한 기록 한 줄 토큰 수:」「기록 수(10·100·1000개 조건):」「가운데 자리의 기록 출처:」「추정 입력 합계(10·100·1000개):」「입력 가용분 안에 드는가:」「가장 긴 user 글에서 빠진 지킬 말:」「컨텍스트 윈도 안에 드는가:」「예상 비용 상한(달러, 10·100·1000개):」「세 요청 예상 비용 상한 합계(달러):」「답:」「끝난 이유:」「실제 출력 토큰 수:」「기록:」「기록 수:」「추정 입력 합계:」「기록표(무관한 기록 수 | 실제 입력 토큰 수 | 캐시 입력 토큰 수 | 출처 표시 수 | 답의 출처 표시와 같은 기록 | 답에서 빠진 지킬 말 | 예상 비용(달러)):」「네 요청 예상 비용 합계(달러):」
- **실행값(2026-09-17, 두 번째 새 커널)**: 추정 456·3336·32136(모두 `False`), 윈도 `True`, 비용 상한 0.000882·0.003042·0.024642·합계 0.028566. 10·100·1000개 답은 글자까지 같음 「미르시립도서관은 매주 월요일이 정기 휴관일이며 법정 공휴일에도 휴관합니다. 공휴일이 월요일과 겹치면 다음 화요일도 휴관합니다. [E01 p.2]」(출력 58·stop), 실제 입력 470·3350·32150, 캐시 0·2816·32000, 출처 표시 1, 빠진 지킬 말 없음, 예상 비용 0.000614·0.000873·0.002773. 0개 답 두 문장 끝마다 `[E01 p.2]`(150/66, 출처 표시 2, 0.000409). 합계 0.004669. 메시지 3개 목록의 추정과 실제 차이 14는 네 목록 모두 같음(470−456·3350−3336·32150−32136·150−136, 본문에는 쓰지 않음)
- **결론 태도**: 「이번 세 요청에서는 길이에 따른 저하(컨텍스트 로트)를 보지 못했다」까지(모델 하나·질문 하나·되풀이 기록·가운데만·한 번씩). 0개 vs 10개 출처 표시 수 차이는 길이와 기록 유무가 함께 바뀐 비교라 원인 보류(04 혼란 목록은 서로 다른 기록 네 개에 표시 둘). Ch 5 05(로컬 Qwen 0.5B, 자리 바꿈)와 한 규칙으로 묶지 않음. 개선 전 06 b2 「05절에서는 길이를 달리한 세 조건의 답을 관찰했고, 이번 실행에서는 성능 저하를 확인하지 못했습니다」는 뜻이 맞음(「세 조건」 = 무관한 기록 10·100·1000개로 이을 수 있음). 06이 「긴 입력은 답을 망친다」를 설계 이유로 쓰지 않도록 주의 — 05가 보여 준 것은 「길면 요청 전 비용 상한이 토큰 수만큼 늘고, 답이 나빠지는지는 재 봐야 안다」
- **비유**: 04 네 책상 → 한 줄로 선 작은 책상 세 개, 책상마다 흰 종이 더미(= 무관한 기록, 높이만 다름·비율 아님)와 초록 탭 카드 한 장(= 휴관 기록), 똑같은 답안지(= 같았던 세 답), 노란 메모지 = 질문. 04-5 높은 더미(= 산만, 실행 안 함)와 뜻이 다르다고 05 그림 읽기에 적음. 파란 명찰·주황 클립보드는 04·05 그림에 없음. 06이 단계적 공개를 그리면 「더미 대신 목차 카드만 올리고 필요한 카드 한 장만 꺼내기」로 이을 수 있음(그리면 그림 읽기에 뜻 적기)
- **그림 색(05)**: 기록·목록·정한 예산 초록, 정의한 함수(`build_long_notes`·`make_length_record`) 파랑, `gpt-5.4-mini` 보라, 출력 값(추정 입력·True/False·비용 상한·답 기록) 노랑, 함께 바뀐 조건 설명 상자 회색, 빨강 0장(experiment)
- **06절이 이어받을 연결**: 05 b8·노트북 끝 「06절에서는 문서 목록을 먼저 보고 필요한 문서의 본문만 여는 단계적 공개를 배웁니다. 입력 설계 몇 가지를 같은 질문으로 보내 토큰 수와 비용을 비교합니다.」(노트북은 한 문장 「…단계적 공개를 배우고, 입력 설계 몇 가지를 같은 질문으로 비교합니다.」) — 개선 전 06 `_src` b1(문서 목록 → 필요한 본문, full·selected·compressed 비교) 기준. 06이 설계 이름·수를 바꾸면 이 문장을 `mdpatch.py`로 확인(05 재실행 불필요). Ch 7 09 b8 「그 절은 도서관 질문으로 입력 설계 세 가지(full·selected·compressed)를 비교합니다」도 함께 확인
- **개선 전 06 노트북이 쓰는 것 중 01~05·Ch 6·7·Part 1에서 안 가르친 것**: 공용 셀 `raise FileNotFoundError`·`RuntimeError`·`ValueError`, 모델 셀 `max_tokens=300`(temperature 누락), `from hashlib import sha256`·`from pathlib import Path`·`next(… for …)`·`*Path.cwd().parents`·`read_text`·`read_bytes`, 집합 리터럴과 `<=`, f-string(`f"[{document['id']}] …"`·`f"근거: {context}\n질문: {question}"`), `"\n".join()`, `(… or {})`·`or 0`, 숫자 `1_000_000`, 반복문 안 `model.invoke` + `time.perf_counter()` + `raise`(셀 21), 반복문 안 f-string `print`(셀 23), `datetime`·`timezone`·`strftime("%f")`, `mkdir(parents=True, exist_ok=False)`·`write_text`, 슬라이스 값 바꿔 보기 `catalog[:base_limit]`(Part 1에서 배움), 영어 키(`design`·`latency_ms`·`checks`…)와 영어 라벨(`input=`·`cost_usd=`), system 규칙 + user f-string 메시지(Ch 7 모양 아님), 문서 id `E01-p2` 모양(02~05는 출처 `E01 p.2`·기록 키 한국어) — 문서 글 「월요일 휴관」은 03·04 휴관 기록보다 조건이 적음
- **아직 안 가르친 것(06이 설명 없이 전제하면 안 됨)**: §04 목록 전체 + 05에서도 안 한 것: 서비스 모델에서 근거 자리 바꾸기(탐색 한 번만, 결론에서 뺌), 질문과 비슷한 방해 기록, 같은 조건 반복 요청으로 평균 내기, 걸린 시간 측정(05는 재지 않음 — Ch 6 06·Ch 7 01 `timed_invoke`는 배움), 캐시가 생기는 조건·유지 시간, 무관한 기록 10000개 이상 실제 요청, 산만 재현, 파일로 기록 저장(05는 파일 없음), 모델에게 문서를 고르게 하기(도구·에이전트, Ch 19~)

## §06 → 실습

(06절 품질 개선 2026-09-17. 결과는 `06-diagnosis.md`, 게이트 G1~G7 0(수정 전 G1 1·G2 4·G3 2·G4 1·G5 15·G6 26·G7 3), 코드 셀 31(준비 3), 노트북 모델 호출 5번(탐색 4 + 새 커널 2회 × 5 = 합계 14, 약 0.007달러). 삽화 06-5 채택(job `2f0bae72-…`, 생성 전 잔액 2838 → 2크레딧), Mermaid 4장. 최종 `outputs_sha256` `d72096cd…`. paired 유지)

### 실습 절(07) 작업자가 먼저 읽을 것 — runs 사슬 최종 상태와 건드리면 안 되는 파일

- **사슬 끝(2026-09-17 12:16:54 UTC 06 두 번째 새 커널 실행)**: `labs/part2/ch08-context-engineering/runs/context-design-continuity.json` SHA-256 **`125fc147e81fb8b6234ff87045120a30f9fdccd6bae52fc0dc8d7c68670e58ad`**, run_id `ch08-context-20260917T121654`, 사본 `runs/continuity/20260917T121654/context-design-continuity.json`(같은 바이트, 이 폴더 하나만). 출처 `source_record` = Ch 7 `labs/part2/ch07-prompt-engineering/runs/prompt-ab-continuity.json` `a8aaafb775e710438a1bd9e5d79340d3032f61be30c4dbb2e8aa4dd7b82095e9`(run_id `ch07-prompt-ab-20260917T070701`) ← Ch 6 `provider-comparison-continuity.json` `f18920c63088bded645bc4712b8ee16436e46d394499bfeaa4cc081f76ef4f4c`
- **실습 절이 하면 안 되는 것**: 06 노트북 다시 실행(기록 파일 해시가 바뀌고 사본 폴더가 늘어 교재 출력·본문 인용과 어긋남), Ch 7 08·Ch 6 06 다시 실행(사슬이 끊김), `runs/` 안 파일 쓰기·옮기기(`context-design-continuity.json`, `continuity/`, `ex01_budget.jsonl` `e3b6a71d…`·`ex04_failures.jsonl` `d23dbb45…`·`ex05_rot.jsonl` `6a9db927…`·`ex06_compare.jsonl` `5cb060d6…` — `test_legacy_logs_are_unchanged`), `data/memory.json` `0aa9fae5…`. **실습 노트북은 파일을 쓰지 않는 쪽**을 권함(Ch 7 09 선례). 파일을 써야 하면 `runs/` 밖 새 이름으로. 06 설명만 고칠 때는 `mdpatch.py` → `run_section.sh … 06 --no-exec`
- 코드를 꼭 고쳐 06을 다시 실행해야 하면: Ch 6 06 → Ch 7 08 → Ch 8 06 순서(Ch 7 요약 §9), 또는 06만 다시 실행하고 06 본문·그림 인용 숫자 전부와 이 메모의 해시를 새로 맞추고, 앞 실행 사본 폴더는 `mv -n`으로 `qa/upgrade/before/runs/continuity/`에 옮김(06에서 첫 실행 사본 `20260917T121541` 옮긴 선례)
- **06 파일 계약(바꾸지 않음)**: 최상위 키 7개 `run_id`·`run_date`·`source_chapter`(`ch08`)·`source_record{path(프로젝트 맨 위 기준 상대 경로), sha256, run_id}`·`settings{model, temperature 0, reasoning_effort none, max_tokens 120, pricing_date 2026-09-17, pricing_usd_per_million {0.75, 0.075, 4.5}}`·`question`·`results`(목록 3개, 원소 한국어 키 8개 `설계`·`답`·`입력 토큰 수`·`캐시 입력 토큰 수`·`출력 토큰 수`·`끝난 이유`·`예상 비용(달러)`·`답에서 빠진 연장 조건`). 읽는 쪽: Ch 8 테스트(`source_record.run_id`·`sha256`, `settings.pricing_usd_per_million`, `len(results) == 3`), `textbook/qa/check_course_continuity.py` 66~76행(경로·지문·run_id·사본), `run_course_bundle.py` 104~111행, `build_bundle.py` 81~87행. 06 노트북 코드 셀의 `estimate_openai_cost(usage, input_rate=0.75, cached_input_rate=0.075, output_rate=4.50)` 이름·기본값(테스트가 인자 하나로 `0.000093`), 06 노트북 원문의 「회원은 최초 2시간 무료입니다.」와 「90분 무료」 없음(`test_ch08_source_ids_match_preserved_memory`)
- **테스트 상태**: `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch08-context-engineering uv run --project labs/part2/ch08-context-engineering --with pytest python -m pytest -q -p no:cacheprovider labs/part2/ch08-context-engineering/tests` → **21 통과**(Ch 6·7·8 연결 테스트 5개 포함). 06에서 `test_log_paths_are_portable_from_student_working_directories`를 고침(수정 전 사본 `qa/upgrade/before/test_ch06_ch08_continuity.before-06.py`): 노트북 코드 원문의 `os.path.exists` 경로 방식과 실제 폴더를 확인. Ch 6 06·Ch 7 08의 R-1(실습 폴더 맨 위)은 테스트 주석에 알려진 제한으로 남김. 실습 노트북은 이 테스트 대상이 아님
- **`check_course_continuity.py`**(`UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch06-langchain-start uv run --project labs/part2/ch06-langchain-start python textbook/qa/check_course_continuity.py`): 73행 통과, 172~199행 통과, **212행 `Stale archive: part1-practice.zip/…`에서 멈춤**(과정 전체 zip 재생성 전이라 끝까지 가지 않음 → 225행 결과 파일도 쓰지 않음). 스크립트는 고치지 않음. 노트북 불변 조건 목록(`notebook-before-invariants.json`, 87개)에 07 실습 노트북은 없음

### 빌더·검사(§01~§05 인계 그대로 동작 확인)

- `_build.py`는 고치지 않았습니다. paired `{{notebook:slug|example}}`·`|failure}}`, `{{mermaid:}}`, 세 칸 `{{img:}}` 동작. `verify.py --chapter` → `PASS 6 sections / 158 code cells (max 16 lines)`(06 개선으로 max 25 → 16). 빌드 HTML `{{` 0건. 작업 전후 챕터 HTML 해시(`/tmp/ch08-06/html-before.txt`)에서 06만 바뀜(06 최종 `35ac73c822b2bc465fe99cebdad314599bd4de3a03bfcf0b205b488288ae600b`)
- **실습 절 07을 붙일 때**: `_build.py` `SECTIONS`에 한 줄(`("07-컨텍스트-엔지니어링-실습", "07 · 컨텍스트 엔지니어링 실습")` 같은 모양), `render_index()` 「절 6개」, `_src/index-body.html` 절 표를 함께 고침 → 06·index HTML 해시가 바뀜(06은 다음 절 링크 때문). 06 b8 「다음 학습과 이어지는 지점」(지금 Ch 9 01·Ch 11)과 노트북 정리 셀 끝 문장(「다음 학습인 Ch 9 01절은 …」)을 07 실습으로 고침(`mdpatch.py` → `--no-exec`, 06 재실행 금지). 실습 30분은 챕터 시수 16h에 더하지 않음(규격 §7-2)
- `visual.cjs`: `/tmp/ch08-01/vis/vis.cjs` 그대로 + HTML 사본 폴더(`/tmp/ch08-06/html`), 결과 `/tmp/ch08-01/vis/checks/html/visual-results.json`(1280·390 14건 PASS)
- G6: 노트북 단락은 빈 줄로만 나뉨. 06 첫 실행에서 6문장 단락 6곳이 걸려 빈 줄을 넣음. 영어 단어+조사 바로 뒤 빈칸(「Before와 」)도 걸리므로 「질문·모델·과업 명세는 Before와 같고」처럼 문장 가운데에 둠

### 실행 환경

- 01~05와 같음(`$ROOT/.cache/vm/venv-ch08-context-engineering`, 새 커널 약 15초, 요청 5번). 탐색은 `ROOT=$PWD UV_CACHE_DIR=$PWD/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$PWD/.cache/vm/venv-ch08-context-engineering uv run --project labs/part2/ch08-context-engineering python /tmp/ch08-06/probe1.py catalog full selected compressed`(`/tmp/ch08-06/common.py`에 06 글·문서·목록 사본, 파일 쓰기 없음), 토큰만 `counts.py`
- `execute.py`의 기본 작업 폴더는 프로젝트 맨 위(`--cwd` 기본값) → 교재 출력의 경로는 긴 경로 `labs/part2/ch08-context-engineering`
- 삽화: 클라우드 scratchpad에서 후보 확인, 기기 셸 `curl` + `/tmp/ch08-06/resize.py`·`cmp.py`로 저장·픽셀 대조. Higgsfield 잔액 2836(06 뒤 추정). 기기 루트 여유 약 570MB
- 입력이 모두 1,000토큰 미만이라 캐시 입력 0(05의 긴 입력과 다름)

### 챕터 전체(01~06)에서 가르친 것 — 실습이 이어 쓸 수 있는 것

- **개념·용어**(절 용어 표): 01 컨텍스트, 컨텍스트 윈도(`gpt-5.4-mini` 400,000), 토큰 예산(수업 예산), 출력 예약분(= Ch 5 출력 몫 = Ch 6 출력 상한), 여유분, 입력 가용분, 추정 토큰 수 / 02 적어 두기(Write), 골라 넣기(Select), 기록, 기록 파일, 메타데이터, 선택 조건, 출처 표시 / 03 줄이기(Compress), 원문, 지킬 말, 줄인 기록, 나누기(Isolate), 업무별 메시지 목록 / 04 실패 모드, 컨텍스트 오염·산만(실행 안 함)·혼란·충돌, 기준 목록 / 05 컨텍스트 로트, 무관한 기록, 근거 앞 기록 수, 같게 둔 조건, 측정 입력, 출처 표시 수 / 06 단계적 공개, 목록 줄, 입력 설계, 전체 입력(full)·고른 입력(selected)·줄인 입력(compressed). Ch 7 08 「파일 지문」「기록 사슬」을 06에서 같은 뜻으로 씀
- **함수(모두 노트북 셀에서 정의, 실습 폴더 모듈 아님)**: `input_budget(total_budget, output_reserve, safety_margin)`·`count_tokens(text)`(01~06), `find_cited_notes(answer_text, notes)`(02·04·05), `find_missing_words(text, words)`(03~06), `build_messages(note, question)`(03), `build_notes_messages(notes, question)`(04~06, 키 `출처`·`내용`만 읽음), `check_answer(answer_text, notes)`(04·05, 바깥 `closure_keep_words`), `build_long_notes(filler_count, before_count)`·`count_marks(answer_text, mark)`·`make_length_record(filler_count, run_response)`(05), `estimate_openai_cost(usage, …)`(05·06 = Ch 7 08), `open_document(document_list, source)`·`make_design_record(design_name, run_response)`(06, 바깥 `condition_words`). 실습 폴더 `context_lab.py`·`examples/`의 같은 주제 함수는 개선 전 영어 모양이고 노트북은 쓰지 않음(실습 절도 쓰지 말 것)
- **데이터(글자 같게 이어 쓸 수 있음)**: `persona_text = "당신은 미르시립도서관 안내 담당자입니다."`, `task_text`(02~06 「문장마다 끝에 출처를 [E01 p.2]처럼」), 600·120·40 → 440, 모델 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none", max_tokens=output_reserve)`. 02 `records` 5개(E01 p.2 휴관·p.3 대출·p.5 주차, E02 p.5 별빛제과 주차, E04 p.2 청담해운 대출). 03 `loan_original`·`loan_question`·`keep_words`·`loan_note`, `closure_note`·`closure_question`·`closure_keep_words`. 04 `memo_note`(틀린 상담 메모)·`pay_note`(E02 p.2). 05 `filler_note`(= 02 E02 p.5). 06 `hours_text`·`loan_text`·`way_text`, `documents`(키 `출처`·`제목`·`설명`·`내용`), `catalog`(키 `출처`·`내용`), `condition_words = ["예약이 없는 경우", "1회", "7일 연장"]`
- **실행값 기준(요청 없는 것은 늘 같음)**: 메시지 3개 목록의 추정과 실제 차이 14(01~06 모든 목록), 01 추정 187, 02 124, 03 대출 128·휴관 136, 04 혼란 235·충돌 170, 05 456·3336·32136·0개 136, 06 목록만 159·전체 420·고른 217·줄인 128·E01 p.5 192
- **Python 모양(A 트랙, 06까지)**: 딕셔너리 목록 리터럴, 함수 안 반복문에서 글 `+` 다시 담기, 함수가 다른 함수를 부름, 함수 안 반복문의 `return`·끝의 `return None`, `for … in [리터럴]:` + `break`, `range()`로 `append`, `split(표시)` 뒤 `len - 1`, 딕셔너리 `copy()`·`record[키] = 값`, 목록 `==`·`assert`, 이미 받은 기록만 반복문에서 `print`, `json.dumps`+`with open`/`json.loads(file.read())`, `tempfile.mkdtemp`+`os.chdir`(02), `hashlib.sha256(바이트).hexdigest()`·모드 `"rb"`(06, Ch 7 08 뜻 그대로), `os.makedirs`·`os.path.exists`·`time.strftime`(06, Ch 6·7 뜻 그대로)
- **결론 태도(실습도 지킬 것)**: 한 번 본 결과는 「이번 실행에서는」, 원인 보류(설계가 정한 결과는 제외), 검사 함수는 말·표시가 있는지만 봄(품질 점수 아님, 뜻은 원문 대조), 두 조건 답에 모두 있던 값은 한 조건 효과로 적지 않음, 출력 토큰 수·비용은 요청마다 달라 순위로 쓰지 않음(06 After가 같은 목록인데 출력 64 vs 104)

### 실습 절 설계에 쓸 수 있는 제약과 후보(권고, 결정은 실습 작업자)

- 규격 §7-2: 30분 안팎, 모델 호출 3~5번, 새 문법·새 API 없음, 실행 1 → 값 하나만 바꾼 실행 2, 그림 조립도·실행 1 순서·실행 1·2 비교 + 삽화 1장, 「강사 시연」 금지. 요청을 기다리는 반복문 안 `print` 금지(요청은 셀마다 또는 반복문 안 `append`만)
- 비용 어림(mini 요금, Ch 6 06 확인 2026-09-17): 06 모양 요청 한 번 0.0003~0.0007달러. 실습 네 번이면 0.003달러 안팎. 05처럼 긴 입력(3만 토큰)을 넣으면 요청 한 번 상한 약 0.025달러이고, 같은 입력 반복은 캐시 입력으로 비용이 달라지므로 실습에서는 짧은 입력 권장
- 소재 후보: 미르시립도서관 안내 질문 하나에 02 골라 넣기(기관·주제 조건) → 06 목록에서 출처 고르기·본문 열기 → 03 지킬 말 검사 → 01 예산표 확인을 조립하고, 값 하나(예: 고른 출처, 목록 한 줄 설명, 출력 예약분)만 바꿔 실행 2. 06 `open_document`·`make_design_record`·`build_notes_messages`·`find_missing_words`를 같은 코드로 재정의해 쓰면 새 문법 없음
- 06에서 요청하지 않은 것(실습이 실행하면 새 관찰로 적을 것): 잘못 고른 본문(E01 p.5)을 실제로 보낸 답, 목록 한 줄 설명을 바꿔 고르는 결과, 여러 출처를 함께 연 목록

### 아직 안 가르친 것(실습이 설명 없이 전제하면 안 됨)

- §05 목록 전체 + 06에서도 안 한 것: 모델에게 목록을 보여 주고 문서를 고르게 하기(도구 호출·에이전트, Ch 19~), 검색·임베딩·벡터스토어(Ch 9~), PDF를 코드로 읽기(`pypdf`, Ch 9 01 — 06은 원문을 옮겨 적음), 한 목록에 여러 출처 본문을 골라 열기, 목록 설명 품질 평가, 같은 설계 반복 요청으로 평균·가운데 값, 걸린 시간 측정(Ch 6 06·Ch 7 01 `timed_invoke`는 배웠지만 Ch 8에서는 안 씀), 캐시 입력이 생기는 조건·유지 시간, 기록 파일을 `runs/` 밖에 쓰고 지우기·옮기기, 파일 지문으로 바뀐 파일을 잡는 실제 재현, `Path`·`next`·`datetime`·f-string·`join`·`raise`·try·내포식·`+=`·`sum`·`max`·`@`·`BaseModel`·타입힌트, Windows·macOS 경로 동작
- 알려진 제한 R-1: Ch 6 06·Ch 7 08 노트북은 실습 폴더 맨 위에서 열면 경로를 못 찾음(두 노트북 재실행 없이는 고치지 않음). 06은 해소

## 실습 → 챕터 검토

(07절 챕터 끝 실습 새로 만듦 2026-09-17. 결과는 `07-diagnosis.md`, 게이트 G1~G7 0, 코드 셀 25(준비 3), 노트북 모델 호출 5번(탐색 5 + 새 커널 2회 × 5 = 합계 15, 약 0.007달러). Mermaid 3장, 삽화 07-4 채택(job `1369d516-…`, 2크레딧, 생성 전 잔액 2836). 최종 노트북은 두 번째 새 커널 출력. experiment, Part 2 마지막 절)

### 검토자가 먼저 볼 것

- **주제·조립**: 「컨텍스트 엔지니어링 실습: 도서관 안내 질문 세 개에 예산표와 지킬 말 검사 붙이기」. `plans`(휴관·대출 연장·주차, 키 `이름`·`질문`·`출처`·`지킬 말`·`줄인 기록`) → `choose_evidence(plan, available)`(06 `open_document` 본문 → 본문 목록 추정 > 입력 가용분이면 03 줄인 기록, 튜플 반환) → `ask_library(plan, available)`(04 `build_notes_messages`·01 추정·03/04 넣기 전 `find_missing_words`, 빠진 말 없고 가용분 안일 때만 `invoke`) → `add_answer_items(record, run_response, evidence, words)`(키 `답`·`실제 입력 토큰 수`·`출력 토큰 수`·`끝난 이유`·`예상 비용(달러)`·`출처 표시 수`·`답에서 빠진 지킬 말`) → `print_records(records)`(요청 전 표·요청 뒤 표·합계). 같은 코드 7개: `input_budget`·`count_tokens`·`find_missing_words`·`count_marks`·`estimate_openai_cost`·`open_document`·`build_notes_messages`
- **바꾼 값 하나**: 수업 예산 600 → 300(입력 가용분 440 → 140). 요청 없는 예산표 `휴관 | 184 | 136 | []`·`대출 연장 | 217 | 128 | []`·`주차 | 197 | 103 | ['30분마다 500원']`를 본 뒤 정한 값(b7에 과정). 휴관 136은 140에 4 차이
- **결과(교재 출력)**: 실행 1 세 질문 본문·보냄, 198/70/2·231/104/2·211/30/1, 합계 0.001397. 실행 2 세 질문 줄인 기록, 휴관 150/67/2·대출 연장 142/53/2 보냄, 주차 `보내지 않음`, 합계 0.000759. 결론은 「예산을 줄이면 본문 대신 줄인 기록이 들어가고, 이번에는 넣기 전 지킬 말 검사가 조건이 빠진 주차 기록을 막았다」까지, 비용 차이는 요청 수·출력 변동이 섞여 예산 효과로만 보지 않음(06 같은 목록 104·64)
- **실행마다 달라진 것**: 첫 새 커널은 대출 연장 실행 1 출력 62·출처 표시 1(한 문장 끝에만), 휴관 69·실행 2 휴관 66·대출 52. 넣은 자료·추정·요청 여부·실제 입력은 두 새 커널·탐색 모두 같음. 본문에는 이전 실행 수치를 싣지 않음(규격 §4)
- **그림 대조**: 07-2는 `choose_evidence` 반환을 「근거 본문 · 종류 본문」으로, 추정은 `ask_library` 요청 화살표에(첫 판 오류를 고침). 07-3은 두 실행 공통 「빠진 지킬 말 없음」을 상자에서 뺌, 「보내지 않음」은 노랑(코드가 정해 기록한 결과, 빨강 0장). 07-1 「빠진 지킬 말 있음」 화살표는 예산 넘음 경우도 같은 길이지만 이번에 일어나지 않아 라벨에 넣지 않음 → 검토 판단
- **새 문법·API 0 확인할 곳**: 튜플 반환(Ch 7 07 `parse_json_answer` 모양), `record.get(키, "-")`(Part 1·Ch 6), `range(len(plans))`(Ch 7 08), 함수 안 여러 줄 `print(...,` 이어 쓰기(Ch 7 09). 새 함수 4개는 Ch 7 09(새 함수 4개) 선례

### 바꾼 파일(수정 전 사본 `qa/upgrade/before/06-to-07/`)

- 새로: `qa/upgrade/author_07.py`, `labs/.../notebooks/07-컨텍스트-엔지니어링-실습.ipynb`, `_src/07-컨텍스트-엔지니어링-실습.html`, 빌드 `07-컨텍스트-엔지니어링-실습.html`, `figures/07-1-조립도.*`·`07-2-실행1-순서.*`·`07-3-두-실행-비교.*`(mmd·svg·png·render.json·caption.md), `figures/07-4-두-책상과-회색-통.png`·`.prompt.md`·`.caption.md`, `qa/upgrade/07-figures.md`·`07-diagnosis.md`·`gates-wip-07.json`·`review-pack/07-…md`
- 고침: `_build.py`(`SECTIONS` 07 한 줄, 「절 7개」), `_src/index-body.html`(07 행, 「일곱 노트북」), 06 `_src` b8·06 노트북 정리 셀 끝 문장·`author_06.py`(`mdpatch.py`, 06 재실행 없음, 코드·출력 해시 `6dd95a1f…`/`bc5ea57b…` 같음, `gates-wip-06.json` 0 다시 씀, `review-pack/06-…md` 다시 만듦), 빌드 06·index HTML, 실습 폴더 `README.md`(07 행), `집필점검표.md`(07 행 + 실습 30분 시수 문장)
- 빌드 HTML 해시: 01~05 그대로(`/tmp/ch08-07/hash/html-before.txt`·`html-after.txt`), 06 `b059271b…`, 07 `ca2d2230…`, index `66727713…`

### runs 사슬·테스트(작업 전후 같음)

- 07 노트북은 파일을 쓰지 않음. `runs/context-design-continuity.json`·`continuity/20260917T121654/` `125fc147…`, `ex01_budget.jsonl` `e3b6a71d…`·`ex04_failures.jsonl` `d23dbb45…`·`ex05_rot.jsonl` `6a9db927…`·`ex06_compare.jsonl` `5cb060d6…`, `data/memory.json` `0aa9fae5…`, Ch 7 `a8aaafb7…`, Ch 6 `f18920c6…` 모두 같음(diff 없음)
- 실습 폴더 테스트 `uv run … pytest … labs/part2/ch08-context-engineering/tests` → 작업 전후 **21 통과**. `verify.py --chapter` → `PASS 7 sections / 183 code cells (max 18 lines)`. 빌드 HTML `{{` 0건. `visual.cjs` 사본 06·07·index × 1280·390 PASS(`/tmp/ch08-07/html`)
- 07 노트북은 `notebook-before-invariants.json`·Ch 8 테스트 대상이 아님. `check_course_continuity.py`는 돌리지 않음(06 인계대로 212행 zip 신선도에서 멈추는 상태)

### 챕터 요약·Part 2 과정 요약에 넘길 것

- 07이 새로 가르친 것: 새 용어·새 API 0. 조립 모양(근거 고르기 → 넣기 전 검사 → 통과할 때만 요청 → 요청 전 표·요청 뒤 표)과 「예산표는 길이만, 지킬 말 검사는 말의 포함만」 두 검사를 함께 쓰는 태도
- 이어 쓸 이름·값(뒤 챕터 후보): `plans` 모양, 주차 질문·주차 지킬 말 `["2시간", "30분마다 500원"]`, 본문 목록 추정 184·217·197, 줄인 기록 목록 136·128·103, 입력 가용분 440·140
- 실습 30분은 `chapter.json`이 없어 `_build.py` 「16h · 강의 6h · 실습 10h」에 더하지 않음(01~06 meta 합 6h·10h, index-body 합계 행 그대로)
- 뒤 챕터 연결: 07 b8 「Ch 9 01절은 같은 E01 문서를 PDF에서 쪽마다 읽고, 사람이 목록을 보고 적던 출처를 검색이 고름」, 「검색으로 고른 문서가 맞았는지는 Ch 11」(Ch 9 01 `_src` b2 확인). Ch 7 09 b8의 「그 절은 도서관 질문으로 입력 설계 세 가지(full·selected·compressed)를 비교」는 06 기준 그대로 맞음
- 아직 안 가르친 것(06 목록에 더해): 조건이 빠진 줄인 기록을 실제로 보낸 답, 질문별 예산·줄인 기록 다시 적기, 모델에게 줄이기·고르기 맡기기, 반복 요청 평균, 걸린 시간 측정
- 챕터 마감 대상(07이 건드리지 않음): `_src/index-body.html` 개선 전 문장(「Poisoning·Distraction·Confusion·Clash는 … 비슷한 대상」 등 04 개선 전 정의, 「05 … 세 길이·각 3회」 행 설명, 「02 … 출처 식별자」), `SECTIONS` 제목 「05 · Context rot 측정」, 옛 생성기 `_make_notebooks.py` 이동, `textbook/qa/upgrade-progress.md` Ch 08 행, `/tmp/ch08-01`~`/tmp/ch08-07` 정리. 기기 루트 여유 약 566MB

## 챕터 마감 → Ch 09

(2026-09-17 검토 1차 A·B 반영과 챕터 마감. 결과는 두 검토 보고서 끝 「반영 결과」, `07-diagnosis.md` §7.) **다음 챕터 작업자는 이 메모 대신 `chapter-summary.md`를 먼저 읽습니다**(Ch 09 인계 §4, runs 사슬 최종 상태 §9, 강사 확인 §11, 남은 것 §12). 마감에서 바뀐 이름: 05 표시 제목 「컨텍스트 로트(Context rot) 측정」, 07 표시 제목에 주제, 05·06·07 요청 측정값 「요청 기록」·「요청 기록표」, 01 「여분 자리」, 02 「기록 카드 상자」, 04 「종잇조각」, 그림 subgraph 「칸」. 07은 재실행으로 출력이 바뀜(실행 1 휴관 답 `['법정 공휴일']`·합계 0.001316/0.000781) — 위 「실습 → 챕터 검토」의 07 수치는 마감 전 값입니다.

## §2-7 리팩터 (2026-09-21)

규격 `textbook/QUALITY-UPGRADE.md` §2-7을 Ch 8에 적용했습니다(Ch 5·Ch 7 다음 셋째 챕터, 모양은 Ch 7 `handoff.md` §2-7). 앞 절·Ch 7에서 배운 함수는 도구 파일 `labs/part2/ch08-context-engineering/notebooks/llm_tools.py`에서 한 줄로 가져옵니다. 벡터 계산이 없어 NumPy는 쓰지 않았습니다. 리팩터 직전 스냅숏은 `qa/upgrade/before-2-7/`(`_src`·노트북·`tests/*.py`·`generators/author_*.py`·그림 mmd/캡션·빌드 HTML·lab README/pyproject·`runs/`·`part2/`(옛 `part2-practice.zip`·`_build_index.py`·`public-files.json`·목차·qa json)·`runs-sha256-before.txt`/`runs-sha256-after.txt`·`runs/moved/`)입니다. 그림·결과 읽기·설명·정직성 규칙은 그대로 두고, 코드와 다시 실행으로 바뀐 인용만 고쳤습니다. 삽화는 새로 만들지 않았습니다.

### 도구 파일 `llm_tools.py` (함수 9개, 코드 57줄, SHA-256 `c4f8cd5f73aa…daa75`)

| 함수(인자) | 배운 절 | 가져가는 절 | 배운 판과 다른 점 |
|---|---|---|---|
| `input_budget(total_budget, output_reserve, safety_margin)` | 01 | 02~07 | 없음 |
| `count_tokens(encoding, text)` | 01 | 02~07 | 01절 판은 바깥 이름 `encoding`을 읽음 → 첫 인자로(호출마다 `count_tokens(encoding, 글)`) |
| `find_cited_notes(answer_text, notes)` | 02 | 03·04(그리고 `check_answer` 안) | 없음 |
| `find_missing_words(text, words)` | 03 | 04~07(그리고 `check_answer` 안) | 없음 |
| `build_notes_messages(persona_text, task_text, notes, question)` | 04 | 05~07 | 04절 판은 바깥 `persona_text`·`task_text`를 읽음 → 앞의 두 인자로 |
| `check_answer(answer_text, notes, keep_words)` | 04 | 05 | 04절 판은 바깥 `closure_keep_words`를 읽음 → 셋째 인자로 |
| `count_marks(answer_text, mark)` | 05 | 07 | 없음 |
| `open_document(document_list, source)` | 06 | 07 | 없음 |
| `estimate_openai_cost(usage, input_rate=0.75, cached_input_rate=0.075, output_rate=4.50)` | Ch 7 08 | 05·06·07 | 없음(Ch 7 08 노트북 판과 본문 같음, Ch 7 08 노트북에는 그대로 남음) |

- 머리: Ch 5·7 모양 독스트링(무엇을 모았는지 / `from llm_tools import 함수이름` / 노트북과 같은 폴더 / 함수마다 배운 절 주석 / 노트북 이름(`encoding`·`persona_text`·`task_text`·`closure_keep_words`)을 읽지 않고 인자로 받음). import 없음(규칙 객체는 인자로 받음). 함수마다 `# NN절에서 배웠습니다 — 하는 일`(`estimate_openai_cost`는 `# Ch 7 08절에서 배웠습니다`), 인자가 바뀐 세 함수는 둘째 줄 주석.
- 금지 문법 0건: 게이트 함수 `g1_ladder`·`g2_shape`를 파일 전체에 돌리면 `multiple_defs_in_cell`·`over_15_lines`만 나옴(셀 규칙이라 해당 없음, Ch 7과 같음). 주석·빈 줄을 뺀 본문 줄 수: `build_notes_messages` 10(문장 5, 목록 리터럴을 다섯 줄에 적은 04절 모양), `estimate_openai_cost` 9(Ch 7 08 판 그대로), 나머지 2~7. 규격 §2-2 L2(본문 10줄 이하) 안이고, 배운 판과 같은 모양으로 두려고 줄이지 않았습니다.
- **넣지 않은 것**(그 절만 씀): 03 `build_messages`, 05 `build_long_notes`·`make_length_record`, 06 `make_design_record`, 07 `add_answer_items`·`print_records`·`choose_evidence`·`ask_library`. Ch 7 도구 파일 함수(`timed_invoke`·`make_prompt_record`·검사 함수)는 Ch 8에서 쓰지 않음.
- **합치지 않은 비슷한 함수**: 03 `build_messages(note, question)`(기록 하나) ↔ 04 `build_notes_messages`(기록 목록) — 인자·본문이 달라 따로 둠. 05 `make_length_record` / 06 `make_design_record` / 07 `add_answer_items` — 요청 기록 키가 절마다 달라 합치지 않음. Ch 6 `estimate_cost(usage, 세 요금)`(기본값 없음)은 이름·인자가 달라 합치지 않음. 두 노트북 이상에 같은 본문으로 있던 함수는 위 9개뿐(AST로 확인, 버전마다 1판).

### 가져오기 셀과 설명

- 기존 import 준비 셀 끝에 `# …를 도구 파일에서 가져옵니다` + `from llm_tools import …`(알파벳 순): 02 `count_tokens, input_budget` / 03 `+ find_cited_notes` / 04 `count_tokens, find_cited_notes, find_missing_words, input_budget` / 05 `build_notes_messages, check_answer, count_tokens, estimate_openai_cost, find_missing_words, input_budget`(`find_cited_notes`는 `check_answer` 안에서만 쓰여 가져오지 않음) / 06 `build_notes_messages, count_tokens, estimate_openai_cost, find_missing_words, input_budget` / 07 `+ count_marks, open_document`(일곱 개). 01은 두 함수를 처음 가르치는 절이라 바꾸지 않았고 다시 실행하지 않았습니다.
- 준비 설명 셀: 고정 세 문장 「앞에서 배운 함수는 `llm_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.」 + 「이 노트북은 NN절 `f()`…를 가져옵니다.」(02~07 모두). 인자 모양 문장은 처음 가져오는 절만: 02(`count_tokens()`는 토큰화 규칙 객체를 첫 인자로), 05(`build_notes_messages()`는 페르소나·과업 명세를 앞의 두 인자로, `check_answer()`는 지킬 말 목록을 셋째 인자로).
- `count_tokens`의 규칙 객체: 옛 「`encoding` + `def count_tokens`」 셀을 `encoding = tiktoken.encoding_for_model("gpt-5.4-mini")` + `print("토큰화 규칙 이름:", encoding.name)` 셀로 바꿈(출력 `o200k_base`, 결과 읽기 「01절과 같습니다」). 07은 이 셀을 6절에 둠(3절 「토큰 수는 6절에서 토큰화 규칙 객체를 만든 뒤 셉니다」).
- 가져온 함수만 설명하던 정의 셀과 「정의만 하는 셀이라 출력이 없습니다」 결과 읽기를 지우고, 같은 소절의 설명 단락으로 합침(코드 없는 설명: 무엇을 받고 무엇을 반환하는지). 소절이 통째로 없어진 곳이 없어 **노트북 절 번호는 그대로**입니다(`_src`·그림 캡션의 「노트북 N절」 인용 바꿀 곳 없음).
- 「같은 코드로 정의합니다」 류 문장: 생성기 md·노트북 md·`_src` 모두 0건(`_src` 02·03·04 앞 절 표의 「2절 같은 코드」 → 「준비 셀에서 가져옴」, 05·06 b5 「노트북은 앞 절 함수를 도구 파일 `llm_tools.py`에서 가져온 뒤」, 07 b3 「앞 절 함수 일곱 개는 도구 파일 `llm_tools.py`에서 가져옵니다」). 남긴 「같은 코드」 한 곳: 07 3절 「06절과 같은 코드로 문서 세 개와 목록을 만듭니다」 — 함수가 아니라 데이터 셀이고, 06 셀과 본문이 글자까지 같음을 확인해 둠.
- 07 조립 함수 설명 「함수 안에서 바깥 이름 `model`과 `shared_tokens`를 읽습니다」 → 「`model`·`shared_tokens`·`encoding`·`persona_text`·`task_text`를 읽습니다」(가져온 함수에 넘기는 값이 늘어서).
- lab README: 「예제 데이터는 셀 안에 포함되어 있고, 실습 폴더의 `context_lab.py`·`examples/`는 가져오지 않습니다. 02~07 노트북은 앞 절과 Ch 7 08절에서 배운 함수를 `notebooks/llm_tools.py`에서 가져오므로, 이 파일을 노트북과 같은 폴더에 그대로 둡니다.」, 사본 폴더 이름 `20260921T050226`.

### 실습 폴더 테스트(규격 §2-7 7항)

- `tests/test_ch06_ch08_continuity.py`의 `load_function()`만 고침(수정 전 사본 `before-2-7/tests/`): 노트북 코드 셀에서 함수 정의를 먼저 찾고, 없으면 **노트북이 그 이름을 `from llm_tools import`로 가져오는지 AST로 확인한 뒤** 노트북 폴더의 `llm_tools.py`에서 정의를 읽습니다. 가져오지도 정의하지도 않으면 실패. 확인 성질(`estimate_openai_cost(usage) == 0.000093`, Ch 6 `estimate_cost(usage, 0.75, 0.075, 4.50) == 0.000093`)은 그대로이고, Ch 7 08은 노트북에 정의가 있어 그대로 노트북에서 읽습니다. 나머지 테스트(`context_lab.py`·`examples/`를 읽는 16개, 경로·문자열·해시 검사)는 손대지 않음.
- 결과: 리팩터 전 20 passed · 1 failed(127행) → **21 passed**(`uv run --project labs/part2/ch08-context-engineering --with pytest==9.1.0 python -m pytest -q -p no:cacheprovider …`, `UV_PROJECT_ENVIRONMENT=.cache/vm/venv-ch08-context-engineering`·`UV_NO_SYNC=1`).

### 절별 전 → 후 (코드 줄은 주석·빈 줄 제외, `textbook/_notebook/upgrade/count_code.py`)

| 절 | 코드 셀 | 코드 줄 | 바뀐 것 |
|---|---|---|---|
| 01 | 22 → 22 | 159 → 159 | 없음(처음 가르친 절, 재실행 안 함) |
| 02 | 23 → 22 | 161 → 157 (−4) | `input_budget` 정의 삭제, `count_tokens` 정의 셀 → 규칙 객체 셀 |
| 03 | 26 → 24 | 175 → 164 (−11) | + `find_cited_notes` 정의 삭제 |
| 04 | 29 → 26 | 184 → 167 (−17) | + `find_missing_words` 정의 삭제(`build_notes_messages`·`check_answer`는 처음 가르쳐 남김) |
| 05 | 27 → 21 | 194 → 148 (−46) | 정의 6개 삭제(+ `find_cited_notes`), `check_answer`에 지킬 말 인자 |
| 06 | 31 → 27 | 257 → 226 (−31) | 정의 5개 삭제(`estimate_openai_cost` 포함) |
| 07 | 25 → 19 | 205 → 165 (−40) | 정의 7개 삭제 |
| 합계 | **183 → 161** | **1335 → 1186 (−149, −11.2%)** | 도구 파일 57줄을 더해도 1243(−92) |

줄이 늘어난 절·셀은 없습니다(10줄 넘는 셀은 모두 리팩터 전부터 있던 셀).

### 다시 실행과 대조

- 02~07을 `run_section.sh`로 새 커널 2회: A(2026-09-21 04:58~05:02 UTC, 사본 `/tmp/ch08-27/A/`), B(교재 출력, `/tmp/ch08-27/B/`). `/tmp/ch08-27/cmp.py`(Ch 7 도구)로 코드 셀을 소스로 짝지어 대조. **요청 없는 셀 출력·입력 토큰 수는 A·B·리팩터 전 모두 같음**(추정 입력 187·124·136·456/3336/32136·420/217/128·184/217/197 등). 달라진 것은 모델을 부른 셀뿐이고, 교재 인용·그림 라벨은 B 값, 결론에 닿은 A 값은 「교재 출력 바로 앞의 새 커널 실행에서는 …」으로 적었습니다(Ch 7 모양). 값을 고르려고 더 실행하지 않았습니다.
- A·B 차이: 02 없음 / 03 After 답 둘째 문장(A 「회원 한 사람의 도서 대출 기준은…」 59토큰, B 「대출 기준은…」 52토큰 — B = 리팩터 전) / 04 충돌 답 줄바꿈과 출력 66·67 / 05 캐시(A는 100·1000개 요청 캐시 0·비용 0.002737·0.024338, B는 2816·32000·0.000837·0.002773)와 1000개 답 첫머리 주어 / 06 전체 입력 답 어순(토큰 같음)·9절 After(A 104토큰 둘째 문장 더함, B 61토큰) / 07 실행 2 대출 연장(A 52토큰·합계 0.000749, B 59·0.000781).
- 리팩터 전(2026-09-17)과 달라져 본문·그림·복습을 고친 곳(A·B가 같은 관찰):
  - **02 Before**: 옛 답은 기록에 없는 「10권」과 과업 명세 예시 표시 `[E01 p.2]`를 적었음 → 이번 두 실행 모두 「`library-notes.json`의 내용이 제공되지 않아 … 확인할 수 없습니다」(출처 표시 없음, `find_cited_notes` → `[]`, 출력 62). 결과 읽기·After 결과 읽기(「두 값과 출처 표시가 모두 넣은 기록과 이어짐」)·정리·`_src` b6 두 단락·도식 읽기·b7 두 항목(지시 한 문장 / 출처 표시 확인)·복습 4(두 답의 `find_cited_notes` 결과 비교로)·b8·**02-4 그림**(빨간 상자 「답 확인할 수 없음 · 7권 · 2시간 없음 · 출처 표시 없음」, 노란 상자에 2시간 더함 — Before에 없어져 공통값이 아님).
  - **04 Before**: 옛 답은 `[E01 p.2]`를 적어 `find_cited_notes` → `[]` → 이번 두 실행 모두 `[상담 메모]`를 적어 `['상담 메모']`(출력 60 → 58). 틀린 내용 되풀이·빠진 지킬 말 두 개는 그대로. 결과 읽기 두 칸·`_src` b6 두 단락·b7 「출처 표시만 믿지 않습니다」·복습 3(표시가 넣은 기록과 같아도 그 기록이 틀리면 답도 틀림)·**04-3 그림**(출처 표시 Before 상담 메모 / After E01 p.2). 04 충돌 출력 66 → 67, 답이 두 줄로 나뉨(「글자까지 같은」 → 「같은 두 문장, 이번에는 두 줄」).
  - **05**: 100개 답이 첫머리 「미르시립도서관은」 없는 두 문장(58 → 50), 합계 0.004669 → 0.004633. 「세 답 글자까지 같음」 → 「세 답 첫머리 주어만 다름」(두 실행 모두 참: A는 100·1000개, B는 100개에 주어 없음) — 결과 읽기·실험 결과 해석·`_src`·**05-3 그림**. 캐시 단락은 A 값(캐시 0, 0.024338달러 ≈ 요청 전 어림)을 들어 「처음 보내면 어림에 가깝다」를 실제로 확인한 문장으로 바꿈. 결론(길이를 늘려도 지킬 말·출처 표시 수 같음)은 그대로.
  - **06**: 세 설계 출력 57·104·53 → 63·61·59, 비용 0.000582·0.000641·0.000345 → 0.000609·0.000448·0.000372, 합계 0.001568 → 0.001429(A·B 같음) → 「고른 입력이 전체보다 비쌈」이 「이번에는 입력이 큰 순서」로. 결론(한 번의 결과로 순위를 정하지 않음)은 그대로이고, 근거를 「입력 203토큰 = 출력 약 34토큰 요금」과 A의 9절 After 104토큰으로 바꿈. 결과 읽기 네 칸·`_src` b5·b6·b7·b8·복습 3(순서가 바뀌는 출력 차이 34토큰을 계산)·**06-2 그림** 라벨. Before 출력 50 → 60(두 문장 모두 `[E01 p.3]`, 「첫 문장에는 출처 표시가 없었습니다」 → 「첫 문장의 표시는 연장 조건의 근거가 아님」). Ch 7 실행 이름 `…20260917T070701` → `…20260921T034935`(3절·6절 결과 읽기).
  - **07**: 실행 1 휴관 답에 「법정 공휴일」이 들어가 빠진 지킬 말 없음(옛 `['법정 공휴일']`), 출력 52·104 → 70·61, 출처 표시 1·2 → 2·1, 합계 0.001316 → 0.001204. 「요청 뒤 답 검사가 실행 1 휴관 답의 빠진 말을 찾았다」를 「보낸 다섯 답 모두 빠진 지킬 말 없음, 넣기 전 검사는 넣을 글만 보므로 답 쪽은 요청 뒤 검사로 따로 봄」으로. 비용 분해 0.00054 = 0.00029 + 0.00010 + 0.00014 → 0.00042 = 0.00029 + 0.00010 + 0.00003(출력 6토큰). 결과 읽기 네 칸·실험 결과 해석·정리·`_src` b5·b6·b8·복습 4·**07-2·07-3 그림**(07-3 휴관 상자의 빠진 지킬 말은 두 실행 모두 없어 뺌).
- **§2-7 10항 판단 — 입력을 고친 절 없음.** 각 절의 핵심 관찰은 두 실행 모두 유지됐습니다: 02 「파일에 적어 둔 기록은 메시지에 넣지 않으면 모델에 가지 않는다」(이번에는 모델이 스스로 내용이 없다고 답함), 04 「틀린 기록이 들어가면 답이 되풀이한다」, 05 「길이를 늘려도 이번에는 지킬 말·출처 표시가 같다」, 06 「목록만 넣으면 연장 조건이 빠지고 본문을 열면 들어간다·비용 순위는 정하지 않는다」, 07 「예산을 줄이면 줄인 기록이 들어가고 넣기 전 검사가 주차 기록을 막는다」(학습 목표 세 개 모두 코드가 정한 결과). 사라진 것은 곁가지 관찰(02·04의 「지어낸 출처 표시」, 06의 「같은 목록 출력 차이」(A에는 있음), 07의 「요청 뒤 답 검사가 빠진 말을 찾음」)이라, 새 출력으로 결과 읽기·결론·그림을 고치고 한 번 본 결과로 한정했습니다(규격 §3 「검토 반영 재실행에서 출력이 달라져도 고르지 않음」). 검토자가 07 「요청 뒤 답 검사」를 핵심 관찰로 본다면 10항 대상 후보입니다(보고에 적음).
- 날짜: 생성기 `RUN_DAY` 2026-09-21(02~07), `_src` b5 「이 페이지의 출력은 2026-09-21에」. 문서·요금 확인 날짜(2026-09-17)는 그대로.
- `outputs_sha256`(전 → 후): 02 `d3643c52` → `e7ef9aac`, 03 `08696210` → `34d19387`, 04 `017eafb9` → `e850cda1`, 05 `b3aac7ca` → `15ff2f94`, 06 `d72096cd` → `93f2293a`, 07 `e8119816` → `9d6122ca`. 01 `b790d25d` 그대로.
- 학생 묶음 확인: 새 `part2-practice.zip`을 `/tmp/ch08-27/bundle`에 풀어 `notebooks`를 커널 작업 폴더로 07을 새 커널 실행(PYTHONPATH 없음, 키는 실행 프로세스 환경에만) → 19셀 오류 0(요청 5번, 값은 교재에 쓰지 않음).

### 산출 파일(runs) 사슬 — 전후 해시와 읽는 쪽

| 파일 | 리팩터 전 | 리팩터 후 |
|---|---|---|
| ch08 `runs/context-design-continuity.json` | `125fc147e81fb8b6234ff87045120a30f9fdccd6bae52fc0dc8d7c68670e58ad`(run_id `ch08-context-20260917T121654`, 출처 = 옛 Ch 7 `a8aaafb7…`) | **`043750eeffb6dc15f56b915da51e87dd69e51adcfd266dbdbd246abb0a66a5d2`**(run_id `ch08-context-20260921T050226`, run_date 2026-09-21, 2178바이트, `source_record` = Ch 7 `434640f4…a561`·`ch07-prompt-ab-20260921T034935`) |
| 사본 | `runs/continuity/20260917T121654/` | `runs/continuity/20260921T050226/`(같은 바이트, 사본 폴더는 이것 하나). 옛 사본과 A 실행 사본 `20260921T050219`(`bef6cc5d…25c5`)는 `qa/upgrade/before-2-7/runs/moved/`로 `mv -n`(삭제 아님) |
| ch08 `ex01_budget`·`ex04_failures`·`ex05_rot`·`ex06_compare.jsonl`, `data/memory.json` | `e3b6a71d…`·`d23dbb45…`·`6a9db927…`·`5cb060d6…`, `0aa9fae5…` | 같음 |
| ch07 `prompt-ab-continuity.json`·`prompt-ab-v1.json`, ch06 `provider-comparison-continuity.json` | `434640f4…`·`16a4b672…`·`f18920c6…` | 같음(읽기만) |

- 계약 유지: 최상위 키 7개, `source_record{path(상대), sha256, run_id}`, `settings`(model·temperature 0·reasoning_effort none·max_tokens 120·pricing_date 2026-09-17·요금 {0.75, 0.075, 4.5}), `question`, `results` 목록 3개(한국어 키 8개), 같은 바이트 사본.
- **사슬: Ch 6 → Ch 7 → Ch 8 이어짐.** 테스트 `test_continuity_logs_form_a_hash_verified_chain` 통과, `textbook/qa/check_course_continuity.py`(Ch 6 가상환경) 66~76행 `part2_handoffs` 두 조건과 172~199행 통과, 묶음 신선도에서 part1·part2·part3 zip 통과 뒤 **`llm-practice.zip/labs/part1/ch01-…/01-과정-지도와-학습-규칙.ipynb` Stale archive에서 멈춤**(전체 마감 몫, Ch 8과 무관). 리팩터 전에는 `part2-practice.zip/…ch08…/02-Write와-Select.ipynb`에서 멈췄음.
- 읽는 쪽 전체(`grep -rlE "context-design-continuity|ch08-context-engineering/runs/ex0|125fc147|20260917T121654|ch08-context-20260917"`)와 처리:
  - 값을 박아 두지 않고 그때 계산 — 수정 없음: `textbook/qa/check_course_continuity.py` 66~76행, `textbook/qa/run_course_bundle.py` 104~111행, `textbook/_notebook/build_bundle.py` 83~87행(존재만), Ch 8 `tests/test_ch06_ch08_continuity.py`, 옛 `part4~7/qa/before-integration/build_bundle.py`(보관본). Ch 9 이후 노트북·실습 코드는 읽지 않음.
  - 새 값으로 고친 것: lab README 사본 폴더 이름, `textbook/qa/upgrade-contracts.md` §2(「§2-7 리팩터로 바뀜 전 → 후」 줄 추가), 이 handoff·`chapter-summary.md`·`qa/verification.md`·`집필점검표.md`, `author_06.py` 인용(재실행으로), `06-diagnosis.md`.
  - 그대로 둔 것(당시 기록): Ch 8 `01~06-diagnosis.md`·`review-round1-A/B.md`·`review-pack/*`·`before/*`의 `125fc147…`·`20260917T121654`, Part 3 문서(Ch 9 `handoff.md`·`chapter-summary.md`·`06-diagnosis.md`·`review-round1-A.md`, Ch 10·11 `chapter-summary.md`, Ch 11 `review-round1.md`, Ch 12 `review-round1-A/B.md`·`verification.md`)의 「Ch 6·7·8 사슬」 기록, `textbook/qa/continuity-evidence/*`(2026-09-09 옛 증거), `textbook/qa/upgrade-progress.md`(읽지 말라는 지시), `textbook/qa/chapter-continuity-verification.md`.

### 공용 도구·챕터 밖 변경

- `textbook/part2/public-files.json`: `labs/part2/ch08-context-engineering/notebooks/llm_tools.py` 한 줄 추가(Ch 7 줄 뒤).
- `textbook/part2/_build_index.py`: 고치지 않음(Ch 7 작업자가 넣은 Ch 8 절 수 칸 7 그대로 맞음). 실행 결과 `Part 2: 23 verified sections; 37 bundled files`(36 → 37) → `textbook/downloads/part2-practice.zip` 다시 만듦(`d2bd54ef…d58e` → `7f894a76…d76b`, 2.29MB, 묶음 속 Ch 8 노트북·README·도구 파일 = 교재 파일), `textbook/part2/index.html`·`textbook/part2/qa/integration-results.json` 다시 만들어짐.
- `textbook/qa/upgrade-contracts.md` §2 줄 추가, `textbook/qa/refactor-2-7-progress.md` Ch 8 행.
- 챕터 안: `qa/public-files.json`(새, Ch 7 모양), `tests/test_ch06_ch08_continuity.py`, lab README 두 문장. 공용 도구(`run_section.sh`·`count_code.py`·`mdpatch.py`·`upgrade_gates.py`·`build_bundle.py`) 변경 없음. `visual.cjs`는 사본 `/tmp/ch08-27/vis.cjs`(Ch 7 사본).

### 검사

- `upgrade_gates.py --label after-2-7` **7/7 PASS, G1~G7 0**(`qa/upgrade/gates-after-2-7.json`). `verify.py --chapter` `PASS 7 sections / 161 code cells (max 17 lines)`(17줄 셀은 리팩터 전부터 있던 셀). 빌드 HTML `{{` 0건. `visual.cjs` 02~07 × 1280·390px 12건 PASS. 다시 렌더한 그림 6장(02-4·04-3·05-3·06-2·07-2·07-3) 폭 683~830(모두 868 미만), SVG 글자로 라벨 확인.
- 생성기 ↔ 노트북 대조: 02~07 코드 셀 글자 같음, 마크다운(첨부 참조 제외) 글자 같음.
- `textbook/part2/qa/check_delivery.py`: 링크·비밀 값·zip 무결성·노트북 실행 흔적 검사는 지나고 **90행 `assert len(notebooks) == 20 and sum(counts) == 180`에서 멈춤**(지금 Part 2 23노트북·470셀: Ch 6 130·Ch 7 179·Ch 8 161 — 전체 마감 몫). `delivery-results.json`은 쓰지 않음.
- 서비스 요청: A 24 + B 24 + 묶음 확인 5 = **53번**, `gpt-5.4-mini`만(temperature 0, reasoning_effort none). 예상 비용 약 0.05달러(05 A 실행의 캐시 없는 긴 요청들 0.028달러 포함).

### Ch 9 작업자에게

1. Ch 8 사슬은 끝났습니다(`043750ee…a5d2`, run_id `ch08-context-20260921T050226`). Ch 9 이후는 이 파일을 읽지 않으므로 Ch 9 리팩터가 Ch 8을 다시 실행할 일은 없습니다. Ch 8 06을 다시 실행하면 해시가 바뀌고 사본 폴더가 늘어 06 인용·계약 문서가 어긋납니다.
2. Ch 9는 RAG 챕터라 도구 파일 이름이 `rag_tools.py`입니다(규격 §2-7 3항). Ch 9 07 노트북이 Ch 8과 같은 이름 `find_missing_words`·`find_cited_notes`·`check_answer`·`build_notes_messages`·`add_answer_items`를 정의합니다(grep으로 이름만 확인, 본문은 대조하지 않음). Ch 8 판과 본문이 같으면 `# Ch 8 NN절에서 배웠습니다`로 옮기고 Ch 8 도구 파일 판의 인자 모양(규칙 객체·페르소나·지킬 말을 인자로)을 따르며, 다르면 이름만 같은 다른 함수로 보고 따로 둡니다.
3. Ch 9 03 노트북에 코사인 유사도 함수(`def cosine…`)가 있어 NumPy로 바꿀 자리입니다. 이름 설명은 Ch 5 02·03절에서 푼 것(`np.array`·`@`·`np.linalg.norm`·`np.argmax` 등)을 「Ch 5 02절처럼」으로 가리키고, 새 이름(`np.argsort`·`axis=1` 등)만 한 문장씩.
4. `textbook/part3/public-files.json`에 도구 파일을 더하고 `check_delivery.py`(Part 3는 통과하던 검사)와 `check_course_continuity.py`(지금 `llm-practice.zip` Stale에서 멈춤)를 다시 돌려 봅니다.
5. 같은 입력을 다시 보내도 모델 답의 곁가지(출처 표시 모양, 한 문장/두 문장)가 바뀌었습니다(02·04·06·07). 결론은 코드가 정한 결과와 두 실행이 같은 값에만 두면 다시 실행해도 흔들리지 않습니다.
