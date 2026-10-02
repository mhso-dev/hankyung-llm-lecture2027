# 08-프롬프트-버전과-AB-비교 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 08, `figures/08-prompt-version-log.*`, `runs/prompt-ab-continuity.json` 옛 정본 사본, `runs/continuity/` 옛 사본 폴더 4개). 수정 전 게이트는 챕터 `gates-before.json`의 08 행.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 5 | 0 |
| G2 | 3 | 0 |
| G3 | 0 | 0 |
| G4 | 1 | 0 |
| G5 | 8 | 0 |
| G6 | 28 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 9 | 27(준비 3) |
| 검사한 문장 | 122 | 515 |

G8: `run_section.sh` 새 커널 PASS 두 번(2026-09-17 07:06·07:07 UTC, 첫 실행 26셀, 두 번째 27셀 — 첫 실행 뒤 `list(…keys())` 중첩 호출 3곳을 변수로 풀고 「두 번째 답 출력」 셀 1개를 더함, 두 번째 실행 출력이 교재 출력). 결과 읽기는 `mdpatch.py` 네 번(`/tmp/ch07-08/reps1.json` 자리 표시 채우기, `reps2`·`reps3`·`reps4` 문장 다듬기) → `--no-exec`로 렌더·첨부·빌드·verify(`PASS 8 sections / 175 code cells`)·게이트 0(`gates-wip-08.json`, `--section 08`로만 실행). 노트북 verification `outputs_sha256` `6b6e8558…62880255`(설명만 고친 뒤에도 코드 셀 출력 글이 두 번째 새 커널 사본 `/tmp/ch07-08/run2.ipynb`와 같음). `visual.cjs` 1280px·390px PASS(`/tmp/ch07-08/vis/vis.cjs` 사본 + HTML 사본, 작은 글자·대비·잘림·가로 스크롤·깨진 그림·복사 불일치 0). 코드 셀 출력 칸은 셀마다 0~1개(요청 반복문 셀은 반복이 끝난 뒤 한 줄만 출력).
meta 「강의 0.5h | 실습 0.5h」는 개선 전 값을 유지했지만 코드 셀 27개·문장 515개라 시수와 맞지 않을 수 있음 → 강사 확인 대상(07과 같음).

## 수정 전 주요 문제

- G1(5): 한 셀 함수 둘(`run`·`mention_flags`), 딕셔너리 내포식 2(`mention_flags`, 저장 셀 `versions`), 제너레이터 식 `next((path for path in [Path.cwd(), *Path.cwd().parents] if …), None)`, 조건 표현식(`None if cost is None else …`). 그 밖에 `raise RuntimeError`·`raise FileNotFoundError`(A 트랙 미교육), `import json, os, time` 한 줄, 집합 비교 `required <= ch06_record.keys()`, `datetime`·f-string·`mkdir(parents=True, exist_ok=False)`·`relative_to`, `or {}`·`or 0` 기본값, `1_000_000`, `sum(…)`
- G2(3): 15줄 넘는 셀 3(경로·지문 셀, 비용 표 셀, 저장 셀). G4: 모델 셀 `max_tokens=220`, `temperature=0`·`reasoning_effort="none"` 없음
- G5(8): 제목 셀·핵심 그림 없음, 결과 읽기가 출력을 인용하지 않음 5, 저장 셀 뒤 결과 읽기 없음 1. 그 밖에 반복문 안 `print`(출력 칸 여러 개)
- G6(28): 70자 초과 12, 영문 시작 13(「`v2`와 `v3`의 차이는」「`mention_count`는」「`run_id`는」 등), 5문장 넘는 단락 3
- G7(3): Mermaid 0(옛 Excalidraw `08-prompt-version-log.svg` 1장), 삽화 0, 설계표 없음
- 내용: (1) b3 「같은 측정 형식만 이어서 사용」 — Ch 6 06 기록은 한국어 키·초 단위, 개선 전 08은 영어 키·`latency_ms`(Ch 6 요약 §4) → 「같은 측정 항목」으로 고침. (2) b3 「과업 제약, 관련 예시, 공개 근거, 반복 표본, JSON 필드 진단」 — 04 틀이 빠지고 07은 「JSON 답 세 층 검사」로 바뀜. (3) b3 「Ch 4의 05절에서 다룬 `json.dumps()`·`json.loads()`」 — Ch 4 05는 `json.dumps`, `json.loads`는 Ch 5·Ch 6 06(과정 요약 §1-2) → b3 표를 Ch 6 06 기준으로 다시 씀. (4) 목록 system 「고객 지원 요청을 처리하세요.」 + user(버전 글 + 옛 `TASK`) — 01~07 목록(system 페르소나·developer 과업 명세·user 고객 문의)과 다름. (5) b6 숫자(95·118·139, 113·108·71, 1.560초 등)는 2026-09-09 한 번 실행(규격과 다른 설정), 집필점검표 표 숫자(출력 128/82/70)와도 어긋남. (6) `mention_count` 합계·`human_review_required` 영어 키, 「필드」 말(Ch 6: 딕셔너리 자리는 키). (7) 새 용어 7개가 흩어지고 일상 예·코드 모습 없음, SHA-256을 「지문」이라고만 부르고 뜻 → 일상 예 → 코드 순서 없음. (8) b8 「같은 측정 필드를 남깁니다」 — 개선 전 Ch 8 06은 영어 키라 Ch 7과 필드가 같지 않음. (9) 참고 자료 확인일 2026-09-09, LangSmith·pathlib 링크는 개선 뒤 쓰지 않음
- 앞 절·앞 챕터와 어긋남: 대문자 `TASK`·`MENTIONS`, 옛 `run()`, 영어 키 표·`json.dumps` 전체 출력, 반복문 안 출력, 요청 결과를 딕셔너리 내포식으로

## 바꾼 것

- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(nbkit `key_and_model_cells`, 실행일 줄 `RUN_DAY = "2026-09-17"`). 출력 상한 없음
- 데이터·설계(07 인계 반영): 과업 명세만 세 버전 — `v1_task = goal_text + "\n" + required_text`(기준선, 2줄), `v2_task`(+ 금지 사항·출력 형식 = 02절 `task_text`, 4줄), `v3_task`(+ 빈 줄 + 03절 `relevant_example` = 03절 `relevant_developer`, 10줄). 개선 전 세 전략(기준선 → 형식·금지 → + 관련 예시)과 「v1→v2는 두 글을 묶어 바꿈」 설명을 이어 씀. 버전 기록 딕셔너리 `{"버전", "바꾼 것", "바꾼 이유", "과업 명세"}` → 요청 뒤 `"기록"` 키 추가, 목록 `prompt_versions`
- Ch 6 기록 파일(2·3절): 경로는 Ch 6 06 모양(`os.path.exists("../runs")`이면 `../../ch06-langchain-start/…`, 아니면 프로젝트 맨 위 기준 `ch06_relative`), `with open` + `json.loads(file.read())`, 최상위 키·실행 이름·요금 확인 날짜·mini 요금 출력, `pricing["openai"]` `assert`. 지문은 규격 §4 세 문장(뜻 → 사람 지문 → `hashlib.sha256(바이트).hexdigest()`) + 모드 `"rb"` 한 문장 + `encode("utf-8")` 한 문장, 주문번호 끝 숫자만 다른 두 글의 지문 비교(`0ff2abab…`·`6099ca9b…`)
- 함수(5절): `estimate_openai_cost(usage, input_rate=0.75, cached_input_rate=0.075, output_rate=4.50)` — Ch 6 06 `estimate_cost()`와 같은 본문 + mini 요금 기본값(Ch 2 04 기본값 매개변수). 교재 예로 기본값·파일 요금 계산이 같은지 `assert`. `timed_invoke`·`make_prompt_record`(01~07 같은 코드) + `add_cost_items(record, run_response)`(Ch 6 06 기록에만 있던 `응답한 모델`·`캐시 입력 토큰 수`(`get`)·`예상 비용(달러)` 세 키를 더함) → 기록 키 9개 = Ch 6 06 `make_cost_record` 키에서 `모델` 대신 `조건`
- 요청: 6절 세 버전 한 번씩(반복문 안 기록만, 출력은 끝난 뒤), 답 원문, 7절 기록표(Ch 6 06 항목)·줄 수·첫 줄·확인 단어 표시, 10절 값 바꿔 보기(버전마다 보낸 횟수 1 → 2, 세 버전 한 번 더)·첫·둘째 실행 나란히 보기(`range(len(…))`)·두 번째 답 원문
- 기록 파일(8·9절): 최상위 키 6개(아래 계약), 경로 고르기 `../runs`, `os.makedirs(copy_folder)`(한 문장, 이미 있으면 오류라 옛 사본을 덮어쓰지 않음 — 설치한 Python 3.12.13에서 `FileExistsError` 확인), `json.dumps(…, ensure_ascii=False, indent=2)` + `with open`으로 기록 파일과 사본, 다시 읽어 실행 이름·출처 지문·버전 수·두 파일 지문 비교 `assert`
- 새로 풀어 쓴 것: 파일 지문(hash)·SHA-256·바이트·모드 `"rb"`·`encode()`·`os.makedirs()`·기본값 매개변수로 요금 두기, 프롬프트 버전·버전 기록·기준선·고정 조건·A/B 비교·기록 사슬(용어 표 7개). 쓰지 않은 것: `Path`·`next`·`datetime`·f-string·`raise`·`**` 풀기·내포식·조건 표현식·`sum`·`max`·`zip`·`+=`·`join`·글 슬라이싱·`isinstance`·집합 비교·`json.dump`/`json.load`·틀·`with_structured_output`·`@`·`BaseModel`
- 요청 수: 노트북 6번(mini). 탐색 실행 3번(`/tmp/ch07-08/probe1.py`: 세 버전 한 번씩, `estimate_openai_cost` 교재 예 `== 0.000093` 확인. 버전 문구·값 바꿔 보기는 탐색 뒤 바꾸지 않음) + 새 커널 실행 2번 × 6 = 합계 15번. 예상 비용 합계 약 0.0086달러(Ch 6 06절 mini 요금, 세 실행 토큰으로 계산)
- 실행 출력(2026-09-17, 두 번째 새 커널 = 교재 출력): 기록표 `v1 | 100 | 0 | 136 | stop | 1.38 | 0.000687`·`v2 | 134 | 0 | 99 | stop | 0.96 | 0.000546`·`v3 | 225 | 0 | 78 | stop | 0.9 | 0.00051975`, 응답한 모델 `gpt-5.4-mini-2026-03-17`, 줄 수 14·3·3, 첫 줄 `안녕하세요. 불편을 드려 죄송합니다.`·`분류: 교환 요청(파손)`×2, 확인 단어 모두 `[True, True, True]`, 보상 약속 0. 기준선 답은 굵은 글씨·`### 다음 안내` 제목·번호 목록. v3 다음 행동 줄 `파손 사진을 먼저 받아 주문번호 A-1042로 교환 접수를 진행합니다.`(03절 예시 답 모양과 비슷). 실행 이름 `ch07-prompt-ab-20260917T070701`, 9절 네 줄 모두 확인 결과 `True`·`버전 수: 3`. 두 번째 실행 `v1 | 100 100 | 136 138 | 14 10 | False`·`v2 | 134 134 | 99 89 | 3 3 | False`·`v3 | 225 225 | 78 78 | 3 3 | True`, v1 두 번째 답 `안녕하세요. 문의 주셔서 감사합니다.`·줄 목록, v2 두 번째 답은 고객 문장 줄만 다름
- 두 번 실행과 탐색에서 달라진 것(입력 토큰 100·134·225는 탐색·두 새 커널·두 번씩 모두 같음, 134·225는 02·03절과 같음): 첫 새 커널 출력 139·89·75(두 번째 133·99·78), 줄 수 10·3·3(두 번째 13·3·3), v3 두 답 다름, 예상 비용 `v2` 0.000501 < `v3` 0.00050625(교재 출력은 반대) → 본문 「비용 순서는 실행마다 바뀜, v3는 입력 91토큰 많아 출력이 약 15토큰 넘게 적어야 더 쌈」(91×0.75÷4.5≈15.2로 계산). 탐색 출력 138·89·78, 줄 수 10·3·3. v2·v3 세 줄·분류 첫 줄, 기준선 여러 줄 목록, 보상 약속 0은 모든 실행에서 봄 → 「이 차이는 두 번 보낸 결과에서 모두 같음」까지만
- 결과 읽기 작성 방식: 모델 출력에 기대는 결과 읽기 6곳 + 해석·정리를 생성기에 `[[READ_…]]` 자리 표시로 두고 두 번째 새 커널 뒤 `mdpatch.py`로 생성기·노트북에 함께 채움(생성기에 채운 글이 남음). 「오늘 볼 그림」 alt·읽기는 `FIG1ALT`·`FIG1READ` 낱말 자리 표시(06 인계)
- 문서 확인(2026-09-17): Python 3.12 hashlib 문서 「hexdigest — Like digest() except the digest is returned as a string object of double length, containing only hexadecimal digits」(WebFetch). os.makedirs는 WebFetch 발췌에 본문이 잘려, 설치한 Python 3.12.13에서 중간 폴더 생성·이미 있으면 `FileExistsError`를 실행해 확인하고 참고 자료에 그 사실을 적음. json 문서는 07절 확인(2026-09-17). 개선 전 LangSmith·LangChain Models·pathlib 링크는 본문에서 쓰지 않아 뺌
- 본문 10블록 다시 씀: 학습 목표 4, 이 절의 질문, 앞에서 배운 내용 표(07·06·03·02·01·Ch 6 06·Ch 2 04) + 01~07 일곱 주제 단락 + Ch 6 측정 항목 단락 + 개선 전 설계 고친 단락, 비유(07 책상 → 클립보드 셋·답 카드 셋·초록 서류철·실·회색 서류철, 날짜 붙인 문서 판), 버전 기록과 고정 조건(A/B 비교 정의), 같은 측정 항목, 파일 지문과 기록 사슬, 용어 표 7개, 실행 예제 뒤 「세 버전의 기록표」, 실험 결과 해석(「같은 버전을 한 번 더 보내면」), 주의 메모 8개(탐색 요청 수·흐름을 보여 주려고 정한 예, 규격 §3), 복습 5문제, 참고 자료 4개
- 그림: Mermaid 4장(08-1 세 버전 798px, 08-2 기록 사슬 528px, 08-3 세 버전 기록표 725px, 08-4 두 번 보낸 결과 844px), 삽화 1장(08-5 버전 클립보드와 서류철, job 3233704c-2b09-43f3-a61e-5732a61d1bd5, 2크레딧, 1회 생성 통과, 원본 SHA-256 `bbf072f8…b7e20fcf83`, 저장 PNG 픽셀 대조 차이 0). 옛 `{{svg:08-prompt-version-log}}`는 본문에서 뺌(파일은 `figures/`에 남기고 `before/figures/`에 사본). 빨강 0장, 회색 = 실행 안 한 Ch 8 06절(08-2), 파랑 = `hashlib.sha256` 코드 단계
- 다음 학습 문장: 대상(Ch 8 06·Ch 11·Ch 15)은 개선 전 그대로 두고, 사실과 다른 「같은 측정 필드를 남깁니다」만 뺌(개선 전 Ch 8 06 노트북은 영어 키 `latency_ms` 등). Ch 8 06 노트북 셀 8·27, Ch 8 06 `_src` b3·b4(full·selected·compressed, 도서관 질문), Ch 11 `chapter.json`(검색 평가), Ch 15 `chapter.json`(judge·평가) 확인. 09 실습 절을 붙일 때 고칠 곳
- Ch 6·01~07 인계 반영: 옛 `TASK`·`run()`·`mention_flags()` 0건. `timed_invoke`·`make_prompt_record`·한국어 키·`check_words`·02·03 글 글자까지 같음. 그림 색 01~07과 같음. 「필드」「칸」「조각」「청크」「출력 상한」「쟁반」「카드 꽂이」「우편함」「투명 봉투」「양식」 쓰지 않음, 딕셔너리 자리는 「키」. temperature 0 ≠ `do_sample=False` 한 문장(모델 셀)

## runs 파일 계약과 사슬 상태(Ch 6 요약 §4·§9 해소 순서 (2) 완료)

- **읽는 쪽(실제 파일로 확인)**
  - Ch 8 06 노트북 셀 8: `required = {"run_id", "run_date", "source_chapter", "source_record", "settings", "versions"}` ⊆ 키, `settings["pricing_usd_per_million"] == {0.75, 0.075, 4.50}`, `run_id` 출력, 파일 SHA-256 계산. 셀 27: `settings["pricing_date"]`·`settings["pricing_usd_per_million"]`을 옮겨 적고, 자기 `source_record = {"path": str(ch07_relative), "sha256", "run_id"}`를 씀. `versions` 안은 읽지 않음
  - Ch 8 `tests/test_ch06_ch08_continuity.py`: `test_cached_input_cost_is_separated_in_all_three_chapters`가 이 노트북 코드 셀에서 **함수 `estimate_openai_cost`만 꺼내 따로 실행**하고 `estimate_openai_cost(usage) == 0.000093`(인자 하나) → 기본값 요금이 필요(통과). `test_continuity_logs_form_a_hash_verified_chain`이 `ch07["source_record"]["run_id"] == ch06["run_id"]`·`sha256` 일치·`ch07["settings"]["pricing_usd_per_million"]`·`len(ch07["versions"]) == 3`을 봄. `test_log_paths_are_portable_from_student_working_directories`는 이 노트북 원문에도 `"[Path.cwd(), *Path.cwd().parents]"`·`"runs_dir = course_root"` 문자열을 요구. `test_legacy_logs_are_unchanged`는 `runs/prompt-ab-v1.json` 해시(`16a4b672…`, 건드리지 않음)
  - `textbook/qa/check_course_continuity.py` 66~76행: `source_record.path`가 상대 경로, `ROOT/path` 파일 SHA-256 == `sha256`, 그 파일 `run_id` == `source_record.run_id`, `runs/continuity/*/prompt-ab-continuity.json` 가운데 기록 파일과 바이트가 같은 사본이 하나 이상
  - `textbook/qa/run_course_bundle.py`: 노트북을 `notebooks` 폴더에서(`--cwd notebook.parent`) 실행하고 `source["sha256"] == sha(extracted / source["path"])`
- **이 절이 쓴 파일**: `runs/prompt-ab-continuity.json`(SHA-256 `a8aaafb775e710438a1bd9e5d79340d3032f61be30c4dbb2e8aa4dd7b82095e9`), 사본 `runs/continuity/20260917T070701/prompt-ab-continuity.json`(같은 바이트). 최상위 키 정확히 6개 `run_id`(`ch07-prompt-ab-20260917T070701`)·`run_date`(`2026-09-17`)·`source_chapter`(`ch07`)·`source_record`(`path` = `labs/part2/ch06-langchain-start/runs/provider-comparison-continuity.json`, `sha256` = `f18920c6…4f4c`, `run_id` = `ch06-provider-20260917T020433`)·`settings`(`model`·`temperature`·`reasoning_effort`·`repetitions` 1·`system`·`user`·`check_words`·`pricing_date` `2026-09-17`·`pricing_usd_per_million` = Ch 6 `pricing.openai`)·`versions`(목록 3개, 원소 키 `버전`·`바꾼 것`·`바꾼 이유`·`과업 명세`·`기록`, `기록` 키 9개 한국어). **옛 파일과 달라진 모양**: 최상위 `model`·`input`·`mention_screen`·`comparison_policy` 4개를 빼고 `settings` 안으로, `versions`는 딕셔너리(이름 → prompt·change·result·metrics)에서 목록으로, `settings.max_tokens` 없음. 읽는 쪽 네 곳 모두 이 차이를 읽지 않음(위 확인)
- **실행으로 확인한 상태(2026-09-17)**: 위 `check_course_continuity.py` 네 조건을 같은 코드로 따로 돌려 ch07 `True True True True`, ch08 `True False False True`. 스크립트 전체는 73행에서 멈추지만 이제 멈춘 곳은 ch08 차례(ch07은 통과). Ch 8 테스트 `2 failed, 3 passed`: 실패는 ① 경로 문자열(첫 경우 Ch 6 06에서 멈춤, Ch 7 08도 같은 문자열이 없음) ② `test_continuity_logs_form_a_hash_verified_chain` 103행 `ch08["source_record"]["run_id"] == ch07["run_id"]`(ch07 두 줄 99·100행은 통과). 통과 3: 비용 함수(이 노트북 `estimate_openai_cost` 포함)·Ch 8 source id·legacy 로그
- **다음 해소 순서**: (3) Ch 8 06 새 커널 실행(이 파일을 읽어 `source_record`를 `ch07-prompt-ab-20260917T070701`·`a8aaafb7…`로) → (4) Ch 8 테스트 수정(실패 ①의 문자열 검사를 `os.path.exists("../runs")` 모양도 받게, Ch 7 08도 이 모양). **이 노트북을 다시 실행하면 기록 파일 해시가 바뀌므로**, Ch 8 06을 먼저 다시 실행한 뒤에는 08을 다시 실행하지 않음(설명만 고칠 때는 `mdpatch.py` → `--no-exec`)
- 옛 사본 폴더 4개(`20260909T172556981866Z`·`…173709587105Z`·`…174009751770Z`, 첫 새 커널 `20260917T070602`)는 `qa/upgrade/before/runs/continuity/`로 옮김(삭제 아님, Ch 6 선례). 옛 정본 `prompt-ab-continuity.json`(`e124b791…`)은 `qa/upgrade/before/runs/`에 사본

## 검토자가 볼 곳

1. 결론 범위: b6 「v2·v3 첫 실행 출력 차이 21, 같은 v2 다시 보내 10」(두 번 보낸 한 실행), 「비용 순서가 실행마다 바뀜」(앞선 새 커널 값을 본문에 인용), 「금지 사항 효과는 이번 실행에서 보이지 않음」
2. runs 계약: 최상위 키를 6개로 줄이고 `versions`를 목록으로 바꾼 것이 Ch 8 06 개선 작업자에게 괜찮은지, `estimate_openai_cost` 기본값(Ch 8 테스트 때문)을 학생에게 「mini 요금 기본값」으로만 설명한 것
3. 삽화 08-5: 답 카드가 초록 서류철 안에 들어간 모양이 아님(그림 읽기에서 이름 붙임), 책상 색이 클립보드와 가까움. meta 시수(강사 확인)

## 검토

- 별도 세션 검토 1차(2026-09-17, `qa/upgrade/review-round1-B.md`): **accept-with-fixes**(중 1·하 1, 공통 C-2 반영 전제). **08 노트북은 다시 실행하지 않았습니다**(runs 사슬). 반영: 08-1(중) 노트북 [48] 설명 셀만 「이 셀만 다시 실행하면 `os.makedirs()`에서 `FileExistsError` / 앞 셀에서 만든 실행 시각 폴더가 이미 있기 때문이고, 기록 파일도 바뀌지 않음 / 8절 첫 셀부터 다시 실행하면 새 실행 이름으로 덮어쓰고 사본 폴더가 하나 더」로(코드 셀 그대로, `author_08.py`의 같은 문장도 mdpatch가 함께 고침). 08-2 [48] 9절 첫 단락 「3절에서는 한 글자만 달라도 지문이 달라졌습니다. 그래서 두 지문이 같으면 두 파일의 내용도 같다고 봅니다.」 R-1 코드는 고치지 않고(재실행 필요) 노트북 [10] 2절 설명에 「작업 폴더가 실습 폴더 맨 위이면 두 경로를 모두 찾지 못해 다음 셀에서 멈추므로, `notebooks` 폴더에서 엽니다」, 실습 폴더 README에 같은 뜻 한 문장, Ch 8 인계는 `chapter-summary.md` §9. C-2 b3 둘째 단락·b4 「개선 전 이 절의 표」 문장 삭제, meta(**강사 확인**). 반영 전후 같음: 노트북 코드+출력 해시 앞 16자 `14593bfd5ee03ad2`, `verification.executed_at` `2026-09-17T07:07:04`, `runs/prompt-ab-continuity.json`·사본 SHA-256 `a8aaafb775e7…82095e9`, `prompt-ab-v1.json` `16a4b672…4341`, Ch 6 파일 `f18920c6…4f4c`. 결정 Q3 권고대로 결론 범위·runs 새 모양·삽화 08-5 유지.
- 반영 방법: `mdpatch.py` → `run_section.sh … 08 --no-exec`(노트북 재실행 없음, 코드 셀·출력·`verification` 메타데이터로 만든 해시가 반영 전과 같음). 마감 게이트 `gates-after.json`(`--strict`) G1~G7 0, 코드 셀 27, 검사 문장 516. 리뷰 묶음은 다시 만들었고 반영 전 묶음은 `qa/upgrade/before/review-round1/review-pack/`에 있습니다.

## 남은 것

- 기기 `/tmp/ch07-08`(탐색 스크립트·`run2.ipynb`·visual 사본·치환 json·삽화 원본 `illus-08-5-a.png`)은 정리 대상
- 옛 도식 `figures/08-prompt-version-log.*`는 정리 대상 목록에만 적음(삭제하지 않음)
- 별도 세션 검토, 강사 확인(meta 시수), 09 실습 절을 붙일 때 b8·노트북 끝 「다음 학습」 고치기

## §2-7 리팩터 (2026-09-21)

- 코드: `timed_invoke`(Ch 6 06)·`make_prompt_record`(01) 정의 두 셀을 지우고 준비 셀에서 `from llm_tools import make_prompt_record, timed_invoke`. 모듈 `time`은 `time.strftime` 때문에 남김. `estimate_openai_cost`·`add_cost_items`는 이 절만 쓰는 함수라 노트북에 둠(Ch 8 테스트 `test_cached_input_cost…`가 이 노트북 코드 셀에서 `estimate_openai_cost`를 AST로 꺼냄 — 인자 하나 호출 `0.000093` 그대로). 코드 셀 27 → 25, 코드 줄 207 → 192.
- 새 커널 두 번(A·B). B가 교재 출력(`executed_at` `2026-09-21T03:49:39`, `outputs_sha256` `46e3b46a…`). B 기록표: v1 100/128/0.000651, v2 134/94/0.0005235, v3 225/77/0.00051525. 예상 비용 순서는 두 실행 모두 v1 > v2 > v3 → 「실행마다 바뀜」 대신 「v3가 더 싸려면 출력이 약 15토큰 넘게 적어야 하고 두 실행 차이 17·16이라 다음 실행에서 바뀔 수 있음」. v2·v3 출력 차이 17, 같은 v2 다시 보내기 차이 11(94 → 83), v3 두 답 글자까지 같음, 기준선 답 10줄(둘째 14줄).
- **runs 파일 전 → 후**: `runs/prompt-ab-continuity.json` `a8aaafb775e710438a1bd9e5d79340d3032f61be30c4dbb2e8aa4dd7b82095e9`(run_id `ch07-prompt-ab-20260917T070701`) → `434640f485d47bd936685b286f654d78249fb8a41e0a64e54b48cc64fb30a561`(run_id `ch07-prompt-ab-20260921T034935`, run_date 2026-09-21). 사본 `runs/continuity/20260921T034935/`(같은 바이트). 옛 사본 `20260917T070701`과 A 실행 사본 `20260921T034813`(`827cf2c7…`)은 `qa/upgrade/before-2-7/runs/moved/`로 `mv -n`. 키 6개·`source_record`(Ch 6 `f18920c6…4f4c`, `ch06-provider-20260917T020433`)·요금·`versions` 3개는 그대로.
- 위 「다음 해소 순서」의 (3)은 이제 **이 새 파일(`434640f4…`, `ch07-prompt-ab-20260921T034935`)을 출처로** Ch 8 06을 새 커널 실행. 그 전까지 Ch 8 테스트 20 passed · 1 failed(`test_continuity_logs_form_a_hash_verified_chain` 127행), `check_course_continuity.py` ch08 출처 불일치. Ch 8 06을 다시 실행한 뒤에는 이 노트북을 다시 실행하지 않음(같은 규칙).
