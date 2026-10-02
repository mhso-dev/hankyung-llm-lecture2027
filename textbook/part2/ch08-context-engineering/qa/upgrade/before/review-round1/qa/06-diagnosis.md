# 06-단계적-공개와-설계-비교 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 06, `figures/06-단계적-공개.svg/.excalidraw`, `runs/`, `test_ch06_ch08_continuity.before-06.py`). 앞 내용: `textbook/qa/upgrade-course-summary.md`(Part 1), Ch 6·Ch 7 `chapter-summary.md`(특히 Ch 7 §9 runs 계약·해소 순서·R-1), 이 챕터 `handoff.md` §01 → §02 ~ §05 → §06, 01~05절 완료본(`_src/0N-*`, 노트북, `author_0N.py`, `0N-diagnosis.md`).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 1 | 0 |
| G2 | 4 | 0 |
| G3 | 2 | 0 |
| G4 | 1 | 0 |
| G5 | 15 | 0 |
| G6 | 26 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 18 | 31(준비 3) |
| 검사한 문장 | 179 | 500 |

수정 전 수치는 챕터 `gates-before.json`의 06 항목입니다. 수정 후는 `gates-wip-06.json`(`run_section.sh … 06 --no-exec` 마지막 실행).

G8: `run_section.sh` 새 커널 PASS 두 번(2026-09-17). 첫 실행 12:15 UTC `outputs_sha256` `4a6ed4f5…`(runs 파일 `ac545626…`, 사본 `runs/continuity/20260917T121541/`). 두 번째 12:16:57 UTC `outputs_sha256` `d72096cdb94d…`(최종, `code_sha256` `6dd95a1f…`, 첫 실행 뒤 설명 셀 빈 줄 여섯 곳과 문장 하나만 고치고 코드 셀은 그대로). 결과 읽기는 두 번째 출력으로 채움(`mdpatch.py` 세 번, 재실행 없음, 전후 코드·출력 해시 같음 `/tmp/ch08-06/nbhash.py`). `verify.py --chapter textbook/part2/ch08-context-engineering` → `PASS 6 sections / 158 code cells (max 16 lines)`. 빌드 HTML `{{` 0건, `figure.mmd` 4·`figure.illustration` 1. `visual.cjs` 1280px·390px 14건 PASS(`/tmp/ch08-01/vis/vis.cjs`, HTML 사본 `/tmp/ch08-06/html`). 작업 전후 챕터 HTML 해시(`/tmp/ch08-06/html-before.txt`)에서 06만 바뀜(`97b9ebfe…` → `35ac73c8…`, 01~05·index 그대로).

## runs 사슬 해소 (Ch 7 요약 §9 순서 (3)·(4))

| 항목 | 작업 전 | 작업 후 |
|---|---|---|
| `runs/context-design-continuity.json` | `88b3520b…`(run_id `ch08-context-20260909T174025306280Z`, 출처 옛 Ch 7 `e124b791…`) | **`125fc147e81fb8b6234ff87045120a30f9fdccd6bae52fc0dc8d7c68670e58ad`**(run_id `ch08-context-20260917T121654`, 출처 Ch 7 `a8aaafb775e710438a1bd9e5d79340d3032f61be30c4dbb2e8aa4dd7b82095e9`·run_id `ch07-prompt-ab-20260917T070701`) |
| `runs/continuity/` | 옛 사본 3개 | `20260917T121654/context-design-continuity.json` 하나(같은 바이트) |
| Ch 8 테스트 | 3 통과·실패 2(①103행 ②`test_log_paths…`) | 전체 `tests/` **21 통과**(`test_ch06_ch08_continuity.py` 5 통과) |
| `check_course_continuity.py` | 73행 멈춤 | 66~76행 `part2_handoffs` ch07·ch08 통과, 172~199행 옛 로그 대조 통과, **212행 `Stale archive: part1-practice.zip/…/01-과정-지도와-학습-규칙.ipynb`에서 멈춤**(과정 전체 zip 재생성 대기, 이 챕터와 무관, 스크립트 고치지 않음) |

- 두 번째 새 커널 실행이 사슬에 준 영향: 기록 파일을 덮어써 해시가 `ac545626…` → `125fc147…`로 바뀌고, 사본 폴더가 하나 더 생김(`20260917T121541` + `20260917T121654`). 첫 실행 사본은 교재 출력이 아니라 `mv -n`으로 `qa/upgrade/before/runs/continuity/20260917T121541/`에 옮김. 옛 정본 `88b3520b…` 사본은 `before/runs/context-design-continuity.json`(cp), 옛 사본 폴더 3개는 `before/runs/continuity/`(mv -n). 삭제 없음
- 두 실행 모두 출처는 Ch 7 `a8aaafb7…`로 같음. **최종 실행(12:16:54)이 사슬 끝**이고, 그 뒤 설명만 `mdpatch.py` → `--no-exec`로 고쳐 runs 파일은 바뀌지 않음. Ch 7 08·Ch 6 06은 다시 실행하지 않음(`a8aaafb7…`·`f18920c6…` 그대로)
- 테스트 수정(실습 폴더 파일, 수정 전 사본 `qa/upgrade/before/test_ch06_ch08_continuity.before-06.py`): `test_log_paths_are_portable_from_student_working_directories`를 옛 문자열 요구(`[Path.cwd(), *Path.cwd().parents]`·`runs_dir = course_root`)에서 다음으로 바꿈. 코드 셀 원문을 JSON으로 읽어 (a) Ch 6 06·Ch 7 08은 `os.path.exists("../runs")`와 `"labs/part2/<챕터>/runs` 글이 있고, `notebooks/../runs`가 실제 runs 폴더인지 (b) Ch 8 06은 후보 목록 `["labs/part2/ch08-context-engineering", "..", "."]`·`candidate + "/runs"`·`candidate + "/notebooks"`·Ch 7 경로·기록 파일 경로 글이 있고, `notebooks` 폴더·실습 폴더 맨 위·프로젝트 맨 위 세 작업 폴더에서 같은 규칙으로 실습 폴더와 Ch 7 파일을 찾는지 확인. Ch 6 06·Ch 7 08의 실습 폴더 맨 위 제한(R-1)은 테스트 주석에 알려진 제한으로 적음. 학생 노트북에는 금지 문법을 넣지 않음. 테스트 ②(103행)는 코드 수정 없이 새 실행으로 풀림
- `check_course_continuity.py`·`run_course_bundle.py`·`build_bundle.py`(챕터 밖 공용)는 고치지 않음. 읽는 조건(`source_record` 경로·지문·run_id, 사본, `settings.pricing_usd_per_million`, `len(results) == 3`)을 모두 만족

## 수정 전 주요 문제

- G1: 셀 8 `next((path for path in [Path.cwd(), *Path.cwd().parents] …), None)` 제너레이터 식. G2: 15줄 넘는 셀 4(8·21·27·36). G3: 첫 줄 주석 없음 2. G4: 모델 셀 `temperature=0` 없음·`max_tokens=300`. G5: 제목 셀·핵심 그림 없음, 결과 읽기 없음·출력 인용 없음 13. G6: 70자 초과 문장 다수(참고 자료 3 포함), 영문+조사 시작 5(「`E01-p3`은」「`selected_id`는」「`break`는」 등), 5문장 넘는 단락 3. G7: Mermaid 0(옛 Excalidraw), 삽화 0, 설계표 없음
- 사다리 밖 문법(게이트가 세지 않은 것): `raise FileNotFoundError`·`RuntimeError`·`ValueError`, `from hashlib import sha256`·`Path`·`read_text`·`read_bytes`·`write_text`, 집합 리터럴과 `<=`, f-string(user 글·출력), `"\n".join`, `(… or {})`·`or 0`, `1_000_000`, 반복문 안 `model.invoke` + `time.perf_counter()` + `raise`, 반복문 안 f-string `print`, `datetime`·`timezone`·`strftime("%f")`, `mkdir(parents=True, exist_ok=False)`, 영어 키(`design`·`latency_ms`·`checks`)·영어 라벨(`input=`·`cost_usd=`)
- 01~05와 어긋남: 메시지가 system 규칙 「근거의 조건·예외·출처를 빠뜨리지 마세요.」 + user f-string(Ch 7 모양 아님), 문서 id `E01-p2` 모양(02~05는 `E01 p.2`·한국어 기록 키), 문서 글 「월요일 휴관」·「회원 1명당 최대 7권, …」이 01~03 원문·기록과 다름, 예산표(600·120·40)·05절 함수·`estimate_openai_cost` 기본값 모양을 잇지 않음(기본값 없는 다른 본문), 경로 R-1과 같은 문제(작업 폴더에서 부모로 올라가며 찾는 방식)
- 내용: 확인 검사가 「연장」 포함·「E01」 포함뿐이라 조건 누락을 못 봄(`_src`가 스스로 한계를 적음), 세 설계 비교에서 출력 토큰 차이가 비용을 바꾸는 점을 다루지 않음, b5 숫자가 2026-09-09 실행 값, 참고 자료 확인일 2026-09-08, b7 「에이전트라는 표현을 사용하지 않습니다」 등 문장이 길고 추상적

## 바꾼 것

- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none", max_tokens=output_reserve)` — 02~05처럼 출력 예약분 120(`assert`). 키 셀 nbkit `KEY`, 실행일 `RUN_DAY = "2026-09-17"`. 준비 3셀(설치·import `hashlib`·`json`·`time`·`tiktoken`·키)
- 형식: paired 유지(`lesson_part` before/after, b6 「일부러 실패해 보기」). Before를 「질문과 다른 문서 선택」에서 「목록 세 줄만 넣고 본문을 열지 않은 요청」으로 바꾸고(단계적 공개의 1단계에서 멈춘 결함), 잘못 고른 출처(E01 p.5)는 7절 값 바꿔 보기(요청 없음, 지킬 말 검사)로 옮김. After는 고른 출처 본문을 연 목록(`assert after_messages == selected_messages`) 실제 요청
- 데이터: 문서 세 개 = E01 2쪽 「2. 이용 시간」 본문(01절 근거 문단 본문), 3쪽 「4. 자료 대출」 본문(03절 원문에서 제목 줄을 뺀 글), 5쪽 「12. 찾아오시는 길」 원문(pypdf 6.18.0으로 확인, 띄어쓰기 바로잡음). 한 줄 설명 = 02절 한 문장 기록 글자 같음(테스트가 요구하는 「회원은 최초 2시간 무료입니다.」가 여기 있음). 질문·지킬 말·줄인 기록 = 03절 글자 같음. 답 확인은 지킬 말 가운데 연장 조건 세 개 `condition_words`
- 탐색(`/tmp/ch08-06/probe1.py`, 요청 4번: 목록만·전체·고른·줄인): 전체·고른 답이 연장 질문에 「7권」「14일」을 다시 적지 않아 지킬 말 다섯 개로는 두 답이 조건을 놓친 것처럼 보임 → 답 확인을 연장 조건 세 개로 정하고 b7 주의 메모에 「탐색 뒤 정한 예」로 밝힘(규격 §3). 목록만 답은 「정보가 없습니다」(오류 없음)
- 경로(R-1 해소): 후보 `["labs/part2/ch08-context-engineering", "..", "."]` 가운데 `runs`·`notebooks` 폴더가 모두 있는 첫 후보를 `for` + `break`로 고름. Ch 7 파일은 `lab_folder + "/../ch07-prompt-engineering/runs/…"`, 출처 경로 글은 프로젝트 맨 위 기준 `ch07_relative`. 세 작업 폴더에서 같은 실습 폴더를 찾는 것은 테스트로 확인(노트북은 프로젝트 맨 위에서만 실행)
- runs 새 모양(계약 유지): 최상위 키 7개 `run_id`·`run_date`·`source_chapter`(`ch08`)·`source_record{path, sha256, run_id}`·`settings{model, temperature, reasoning_effort, max_tokens 120, pricing_date 2026-09-17, pricing_usd_per_million}`·`question`·`results`(목록 3개, 한국어 키 8개 `설계`·`답`·`입력 토큰 수`·`캐시 입력 토큰 수`·`출력 토큰 수`·`끝난 이유`·`예상 비용(달러)`·`답에서 빠진 연장 조건`). 옛 키 `model`·`comparison_policy`·`latency_ms`·`checks` 등은 읽는 쪽이 없어 뺌(grep: 테스트·`check_course_continuity.py`·`run_course_bundle.py`·`build_bundle.py`만 읽음). 걸린 시간은 재지 않음
- 기본 경로: 준비 3셀 → 2절 05와 같은 8셀(페르소나·과업 명세 / `input_budget` / 600·120·40 / `count_tokens` / 모델 / `find_missing_words` / `build_notes_messages` / `estimate_openai_cost`) → 3절 경로 고르기 / Ch 7 파일 읽기(키·run_id·요금·버전 수·`assert`) / 지문(`"rb"`·`hashlib.sha256`, 64글자만 출력) → 4절 본문 세 개 토큰 수 / 문서·목록(`for`, 목록 줄도 `출처`·`내용` 키) / 질문·지킬 말·연장 조건 / `open_document(document_list, source)`(`for`·`return`·`None`) / 고른 출처 열기·목록 줄 비교 → 5절 세 목록·추정·가용분 / `make_design_record(design_name, run_response)`(키 8개, 본문 10줄) / 요청 셀 3개 / 기록표(반복문은 출력만)·비용 합계 → 6절 기록 딕셔너리 / `os.makedirs`+`json.dumps`+`with open` 두 번 / 다시 읽어 지문·설계 수·사본 비교·`assert` → 7절 다른 출처·없는 출처 `None` → 8절 Before 한 셀 → 9절 After 한 셀 → 정리
- 쓰지 않은 것: f-string·`raise`·try·내포식·제너레이터 식·조건 표현식·`Path`·`next`·`datetime`·`join`·집합 연산·`+=`·`sum`·`max`·`@`·`BaseModel`·타입힌트·`**` 풀기·반복문 안 요청과 `print`·글 슬라이싱·`time.perf_counter`. 새로 쓴 모양: 함수 안 반복문의 `return`(찾으면 바로 반환)·끝의 `return None`, `for 이름 in [목록 리터럴]:` + `break`로 첫 후보 고르기, `이름 is not None`을 `print` 인자로, 딕셔너리 목록에 같은 함수 쓰기(`open_document(catalog, …)`)
- 요청 수: 노트북 5번(mini). 탐색 4번 + 새 커널 2회 × 5 = 합계 14번. 비용 어림(mini 요금): 탐색 약 0.0018달러, 새 커널 한 번 약 0.0024달러(최종 기록표 세 요청 `0.001568` + Before·After) — 합계 약 0.007달러
- 두 실행 비교(교재에는 두 번째만 인용): 추정 입력·목록 검사·경로·지문 글자 수는 같음. 첫 실행 전체 입력 출력 63(`0.000609`), 고른 입력 104(`0.000641`), 줄인 53, Before 60(첫 문장 끝에도 `[E01 p.3]`), After 104(5절 고른 답과 글자 같음). 두 번째 실행 전체 57(`0.000582`), 고른 104, 줄인 53, Before 50, After 64(5절 고른 답과 다름). 두 실행 모두 고른 입력 예상 비용이 전체 입력보다 컸음 — 본문은 「한 번의 결과로 순위를 정하지 않음」으로만 씀
- meta 시수: 「강의 1h | 실습 1h」 유지(01~06 합 강의 6h·실습 10h = `render_index()` 16h). 새 용어 5 → 6
- 그림: Mermaid 4장(06-1 목록에서 본문으로·06-2 세 입력 설계·06-3 기록 사슬·06-4 Before-After, PNG 직접 확인, viewBox 폭 386·683·273·786) + 삽화 06-5 목록 카드와 책 1장(1회 생성 채택, job `2f0bae72-785f-4d96-a9dc-6f5c3ee0c5f6`, 2크레딧, 생성 전 잔액 2838, 저장 PNG와 job 결과 픽셀 차이 0). 옛 `06-단계적-공개.svg/.excalidraw`는 지우지 않고 본문에서 쓰지 않음(정리 대상)
- 본문: 10블록 모두 다시 씀. b3 표(Ch 6 06·Ch 7 08, 01~05), b4 비유(목록 카드와 책)·단계적 공개·목록 줄은 근거가 아님·세 입력 설계 표·사람이 고르는 이 절과 Ch 9·용어 표 6개, b5 세 설계의 답과 비용(출력 토큰이 비용을 바꿈, 계산)·기록 파일과 기록 사슬·작업 폴더와 경로 고르기(Ch 6 06·Ch 7 08은 `notebooks` 폴더나 프로젝트 맨 위에서 엶)·값 바꿔 보기, b6 Before/After·06-4, b7 탐색 뒤 정한 연장 조건·목록 설명 품질 안 잼·잘못 고른 본문 요청 안 함·비용 변동·캐시 0·걸린 시간 안 잼·다시 실행 순서·작업 폴더·기준 버전, b8 Ch 9 01·Ch 11 연결, b9 복습 5문제, b10 참고 자료(Anthropic 두 글 WebFetch 확인 2026-09-17, LangChain 글은 이 절에서 인용하지 않아 뺌). 제작 이력 문장 없음

## 검토

- 스스로 확인: 결과 읽기·본문·캡션·그림 라벨 숫자와 답 인용을 두 번째 새 커널 출력과 대조(G5·G7 0). 그림 방향 말(06-1~06-3 「위에서 아래로」, 06-4 「위 칸·아래 칸, 칸마다 왼쪽에서 오른쪽으로」), 색 이름을 PNG와 대조. 빨강은 06-4 Before 결과 한 상자(paired Before 결함). 06-2는 세 답 공통 값을 따로 둔 상자에, 06-4는 두 답 공통 `[E01 p.3]`을 뺌(규격 §5-3)
- 계산 대조: 434 − 231 = 203, `203 × 0.75 / 1000000 = 0.00015225`, `47 × 4.50 / 1000000 = 0.0002115`, 추정과 실제 차이 14(420/434·217/231·128/142), 440 − 420 = 20, 기록표 합계 0.000582 + 0.000641 + 0.000345 = 0.001568
- 사실 대조: Anthropic 「Equipping agents for the real world with Agent Skills」(2025-10-16, 시작 때 `name`·`description`을 시스템 프롬프트에 넣고 관련 있으면 `SKILL.md` 전체를 읽음), 「Effective context engineering for AI agents」(2025-09-29, lightweight identifiers·just in time·progressive disclosure) WebFetch 2026-09-17
- 뒤 챕터 연결 확인(실제 파일): Ch 9 01 `_src` b2 「Ch 8에서 … Select … 실습에서는 사람이 손으로 골랐습니다」, b3 「`pypdf.PdfReader` … 각 쪽의 추출 결과를 `Document` 객체로」, 노트북 E01.pdf 사용. Ch 7 09 b8 「그 절은 도서관 질문으로 입력 설계 세 가지(full·selected·compressed)를 비교합니다」는 이번 06과 맞아 고치지 않음
- 삽화 검수(저장 파일 기준, `figures/06-5-목록-카드와-책.prompt.md`): 목록 카드 색 점 ↔ 빈칸 ↔ 펼친 하늘색 책이 그림만으로 읽힘. 약점(빈칸이 흰 면, 빈칸이 가운데라 목록 둘째 줄과 자리가 같아 보임)은 그림 읽기에서 처리
- 별도 세션 검토: 아직(챕터 마감 때)

## 남은 것

- 뒤 작업자에게: `qa/upgrade/handoff.md` §06 → 실습
- 챕터 마감 때: `_src/index-body.html` 06절 「주요 내용」 표가 개선 전 설명인지 확인(index HTML 해시가 바뀌므로 06에서는 고치지 않음). 07 실습 절을 붙일 때 06 b8 「다음 학습」과 노트북 끝 문장을 실습 절로 고침. README가 06 설명과 맞는지(현재 「세 설계 비교 결과」로 맞음)
- 정리 대상(삭제 승인 필요, 목록만): `figures/06-단계적-공개.svg`·`.excalidraw`, `qa/upgrade/gates-wip-06.json`, `qa/upgrade/before/runs/continuity/20260917T121541/`(첫 새 커널 사본), 기기 `/tmp/ch08-06`
- `examples/ex06_compare.py`·`tests/test_ex06_compare.py`·`runs/ex06_compare.jsonl`(`test_legacy_logs_are_unchanged`)은 개선 전 그대로이고 노트북·본문은 쓰지 않음
