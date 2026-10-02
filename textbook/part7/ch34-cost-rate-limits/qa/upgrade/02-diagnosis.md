# 02절 진단과 개선 기록 — Batch API (paired, 노트북 모델 0 · 노트북 밖 실제 일괄 작업 한 번)

- 작업일 2026-09-29(UTC 23:0x~23:4x). 생성기 `qa/upgrade/author_02.py`(`e3cf7ef1…`). 규격 `textbook/QUALITY-UPGRADE.md` §2·§2-7·§3·§4·§5-3·§5-4·§6. 1차 지시서 `qa/upgrade/handoff.md` 「챕터 공통」·「§01 → §02」(12항). 노트북 밖 일괄 작업 기록 `qa/upgrade/probe/02-batch.md`.

## 1. 게이트 전후

| | 코드 셀 | 코드 줄 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 5 | 32 | 66 | 12 | 5 | 5 | 0 | 7 | 10 | 3 | **42** |
| 수정 뒤(`gates-wip-02.json`, `--no-exec`) | **29** | 159 | **405** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 코드 줄은 주석·빈 줄·`%` 줄을 뺀 줄. 도구 파일 `cost_tools.py` 코드 줄 34(02 판 전체, 따로). 준비 셀 밖 셀 최대 9줄 · 함수 본문 최대 7줄(`pair_by_order`) · 호출 깊이 최대 2(AST 따로 — `.cache/ch34-01/tools/pregate.py`).
- AST 따로 0건: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·별표 풀기·`+=`·대입 풀기(for 포함)·`while`·`try`·`raise`·클래스·데코레이터·힌트·기본값 매개변수·`key=`/`reverse=` 인자·`set`·`next`·`enumerate`·`zip`·`sum`·`max`·`min`·`all`·`any`·`isinstance`·`getattr`·`sorted`·노트북 `.get`·한 글자 변수·비동기. 처음 쓰는 이름은 결과 읽기에서 한 문장씩: `tempfile.mkdtemp`(Ch 23 선례)·`os.path.getsize`·`json.dumps(…, ensure_ascii=False)`·`dict.copy`·`list.copy`·`list.reverse`·`in`(딕셔너리 키)·슬라이스 `[n:]`.
- 과정 금지어(산문, 코드 백틱 뺌): 0건(01 금지어 목록 + 이 챕터 대체어 + 「제출」 단독·「업로드」·「배치」·「식별자」·「검증」·「사전」·「직렬화」·「엔드포인트」·「완료 창」). 제목 풀이 한 곳(노트북 1절 첫 문장·본문 b2 「제목의 Batch API는 …」 — 01 선례, **강사 확인**). 사용자가 금지한 표현(과정 규칙) 0건(생성기·노트북·본문·그림·기록 파일 모두).

## 2. 수정 전 주요 문제 (준비 노트 §1·§2-02·§4 확인)

1. 준비 셀이 `Path.cwd()`에서 위로 폴더를 찾음 → 루트 커널에서 `FileNotFoundError` · `next(… for …)`·`(here, *here.parents)`·한 글자 변수 `p`·`r`·`x`.
2. 모델 `"gpt-5-mini"`·요청 주소 `/v1/responses` — 과정 표준 모델·LangChain 기본 길(Chat Completions)·Ch 15 08 입력 파일 모양과 다름.
3. `runs/batch-input.jsonl`을 실습 폴더에 씀(출력에 가린 절대 위치 `[사용자 폴더]/…`까지) · 내포식·f-string·`all(…)`·집합 내포식.
4. **paired Before가 약함**: 목록을 JSON 배열 한 줄로 만들고 우리 `isinstance` 검사가 「요청 객체로 판정: False」 — 서비스가 거절하는 장면이 아니고, 파일로 쓰지도 않았고, Ch 15 08 `line_problems`와 겹침. After도 다른 자료를 읽음(같은 조건 비교 아님).
5. 제출 0 → Ch 15 08과 거의 같은 절(맡긴 뒤의 일을 가르치지 않음). 옛 `qa/verification.md` 「확인 필요」: 「실제 처리 완료 시간, 결과 파일, 청구 비용을 확인하지 않았습니다」.
6. 금지어: 「배치」 11/3 · 「Batch」 9/3 · 「제출」 6/3 · 「검증」 4/3 · 「식별자」 3/1 · 「업로드」 · 「직렬화」 · 「엔드포인트」 · 「사전」 · 「필드」 · 「완료 창」 · 비유 「창구·접수함」(Ch 6 「상담 창구」·금지 소품 「창구」와 겹침).
7. 결과 읽기 0 · 첫 줄 주석 0 · 제목 셀·그림 0 · 준비물(요청 수·비용)·실행일 없음 · Mermaid 0·삽화 0·설계표 없음.
- 틀린 사실: 옛 본문의 할인 50%·완료 창 24시간·`custom_id` 고유·「결과 순서를 가정하지 말 것」은 공식 안내와 맞음(참). 과정과 어긋난 것은 위 2(모델·요청 주소)와 4(Before 판정 방식). 옛 b10 두 링크는 2026-09-11 확인 — 새 b10은 2026-09-29 확인.

## 3. 설계 (챕터 리드 결정 1·3·4·8·9 · handoff §01 → §02 12항)

- **노트북 모델 0**: 키 셀·모델 셀·설치 셀 없음(표준 라이브러리 `json`·`os`·`tempfile` + 도구 파일). 준비 셀 = 가져오기 하나(도구 파일 줄 포함 — 고정 세 문장 + 커널 폴더 한 문장 + 실행 도구 한 문장) + Ch 30 과정 표준 파일 위치 셀(후보 `..`·`.`·`labs/part7/ch34-cost-rate-limits`, 찾을 파일 `data/batch-output.jsonl`, 고른 후보 출력 안 함, `assert` 한 줄 — `author_01.FIND_LAB` 모양).
- **실제 조건(권장 설계 ①)**: 노트북 밖에서 한 번 맡긴 실제 일괄 작업 — 입력 5줄 가운데 `inquiry-2`만 `reasoning_effort` low + `temperature` 0(공식 GPT-5.4 안내의 「온도 칸은 none일 때만」 규칙 — 제출 전에 문서로 확인, mini는 문서에 따로 없어 이번에 처음 봄). 서비스가 400 `unsupported_value`로 거절 → 오류 파일 → 결과 파일 4줄(차례 `inquiry-1·3·4·5`).
  - **Before**(빨강) `pair_by_order`: 결과 줄을 입력 차례대로 짝지음 → `inquiry-2 | inquiry-3 | 환불` · 이름표가 서로 다른 짝 **3** · 결과 없이 남은 입력 `['inquiry-5']`(실제로 거절된 것은 둘째).
  - **After**(노랑) `ids_not_in`(Ch 15 08) → `['inquiry-2']`·오류 파일에도 없는 것 `[]` · `answers_by_name` + 오류 코드 딕셔너리 → `pair_by_name` 다섯 줄 모두 제 짝, `inquiry-2 | 오류 파일 | unsupported_value`.
  - **값 바꿔 보기**: 결과 줄 차례만 거꾸로(이 셀이 바꾼 차례라고 밝힘) → 이름표로 만든 답 딕셔너리 같음 `True` · 차례대로 짝지으면 셋째 짝만 우연히 맞고, 넷째 짝 `inquiry-4 | inquiry-1 | 배송`은 이름표가 다른데 답이 우연히 문의와 맞아 보임.
  - 공식 안내 문장 근거: 「the output line order may not match the input line order … use the custom_id field」·「Any failed requests … error file」.
- **입력 JSONL은 운영체제 임시 폴더**(`tempfile.mkdtemp(prefix="ch34-02-")`, 위치는 출력하지 않음, 「임시 폴더의 파일은 실습 폴더 밖에 있어 그대로 둡니다」 — Ch 23·Ch 31 03 선례). 노트북이 만든 입력 파일은 노트북 밖에서 맡긴 파일과 **바이트까지 같음**(생성기 `check_input_bytes()` — 메모리에서 sha256 `6ea21c43…` 대조, `probe/cells_input.py`와 셀 글 대조).
- **할인 셈**: 결과 줄 토큰 합(173·18)이 작업 기록 사용량과 같은지 `True True`(거절된 줄 토큰 0) → 합으로 사용량 딕셔너리(`input_tokens`·`output_tokens` — 캐시 입력 키는 넣지 않음, 결과 줄 캐시 입력 모두 0) → `estimate_cost` 0.00021075 × `batch_discount = 0.5` = 0.000105375달러.
- **말**: 「일괄 처리(Batch API)」(Ch 15 08) · **요청 이름표(custom_id)**(Ch 15 08 「요청 식별자」 — Ch 19 금지어라 02가 정함, handoff 용어 표에 더함) · 결과 파일·오류 파일·작업 상태(새 용어 4 — meta 그대로) · 일괄 작업·처리 기한(Ch 15 08) · 「맡기다」(「제출」 단독 대신) · LangChain 메서드 `batch`(곧바로 함께 보냄, 할인 없음)와 가르는 문장(노트북 3절·본문 b4 마지막 단락·복습 5).
- **Ch 15 08과 겹치는 것은 이음 문장으로**: 입력 줄 네 칸·JSONL 쓰기·다시 읽기는 도구 파일 함수로 가져와 결과 읽기 한두 문장, 새로 가르친 것은 맡긴 뒤의 일(작업 상태·결과/오류 파일·이름표로 짝짓기·할인 셈·취소는 문서로만).
- **흉내 0**: 결과 파일은 받은 파일에서 칸을 뺀 것(값을 만들지 않음 — `probe/make_data02.py`), 가짜 모델·정해 둔 답 서버 0. 거꾸로 한 차례만 노트북이 만든 것이라고 밝힘.

## 4. 노트북 밖 일괄 작업 (한 번 — `probe/02-batch.md`)

- §0(설계·판단 규칙·자료 파일 칸·요청 수·어림) 저장 **23:08:21Z** → 마른 실행(닫힌 포트, 서비스 요청 0) → 제출 셸 23:08:46Z → 파일 올리기·작업 만들기(두 호출 `max_retries=0`) **23:08:49Z** `validating`.
- 상태 확인 넷: +6초 `validating` · +53초 `validating` · +81초 `in_progress`(완료 1/5) · +140초 **`completed`**. 작업 객체 시각: `in_progress` 23:09:52Z · `finalizing` 23:10:56Z · `completed` 23:10:57Z → **128초**(30분 규칙 안, 취소 없음). `errors` None.
- 결과: 완료 4 · 실패 1 · 모두 5 · 응답 모델 `gpt-5.4-mini-2026-03-17` · 결과 줄 답 「배송」·「환불」·「배송」·「결제」(문의 종류와 모두 맞음 — 모델이 쓴 글, 한 번) · 오류 줄 `inquiry-2` 400 `invalid_request_error`·`temperature`·`unsupported_value`·「Unsupported value: 'temperature' does not support 0 with this model. Only the default (1) value is supported.」 · 사용량 입력 173·캐시 입력 0·출력 18(거절된 줄 0).
- ID(`file-8Zv…`·`batch_6abc…`·결과 `file-PTY…`·오류 `file-VLQ…`)는 `$ROOT/.cache/ch34-02/resume/ids.json`·`raw-batch-final.json`에만. 원본 결과·오류 파일(ID 포함) `resume/raw-output.jsonl`(`9e752925…`)·`raw-errors.jsonl`(`e206522b…`).
- 흔들림 처리: 제출은 조건대로 **한 번만**(다시 맡겨 5번 보지 않음 — 챕터 리드 결정 9 「노트북 밖에서 한 번」). 거절·결과 줄 차례·걸린 시간은 본문에서 「이번에 맡긴 작업에서는」·「한 번 맡긴 작업에서 본 결과」로 한정하고 일반화하지 않음. 노트북 출력은 자료 파일로 정해져 매번 같음 → 짝짓기 Before/After를 노트북 밖 새 프로세스 **5번**(`probe/pair5.py`, 23:25Z) 돌려 5/5 같음.

## 5. 실행

- 첫 실행 전: `/tmp/ch34-02/tryA`(생성기 `--nb-copy` 사본, 도구 파일 02 판은 `PYTHONPATH` 임시 폴더, `--cwd labs/…/notebooks`) — PASS 29셀 · pregate G5 1(결과 읽기 인용 `inquiry-5`가 그 셀 출력에 없음 → 「다섯째 요청」으로 고침) · 게이트 `--label wip-02 --section 02` **G1·G2 0**(G3~G6 0, G7 3 — 그림 전).
- **새 커널 A**(`env -u OPENAI_API_KEY … run_section.sh … 02`, 프로젝트 맨 위 커널, `executed_at` **2026-09-29T23:24:53Z**) — PASS 29셀, `code_sha256` `51e2b77e959b…`, `outputs_sha256` `0d10754ff204…`(그림 첨부 단계에서 멈춤 — 그림 전이라 예상한 일, 실행·저장은 끝난 뒤).
- **새 커널 B**(`--nb-copy /tmp/ch34-02/B`, `--cwd labs/…/notebooks` 학생 자리, `PYTHONPATH` 없이 — 실습 폴더의 도구 파일 02 판을 학생 자리에서 가져옴, 23:25:03Z) — PASS 29셀, `code_sha256`·`outputs_sha256` **A와 같음**, 셀별 출력 **29/29 같음**(`.cache/ch34-01/tools/cmpout.py`). 모델을 부르지 않고 자료 파일만 읽으므로 다를 까닭이 없음.
- 그림 뒤 `--no-exec` 두 번(렌더·첨부·빌드·verify·게이트) — 노트북 코드·출력은 A 그대로(29/29), 생성기 `cells()`와 노트북 셀 63개 글·`lesson_part`가 모두 같고 `_src`가 `src_html()`과 글자까지 같음.
- 저장 출력: Traceback·임시 파일 위치·`/sessions`·작업/요청/파일 ID·시각·키 0(스트림 출력만).
- **노트북의 실습 폴더 쓰기 0**: 쓰는 곳은 `tempfile.mkdtemp` 임시 폴더뿐. 옛 `runs/batch-input.jsonl` `ee6ac19d…` 그대로(루트 떠돌이 `batch-input.jsonl`도 같은 해시 그대로). 실습 폴더 `notebooks/`·`qa/`에 `__pycache__`·`.pyc` 새로 생긴 것 0(`.venv` 안의 옛 `__pycache__`는 2026-09-11 학생 환경 것).

## 6. 교재 출력 값 (A = B, 자료 파일로 정해짐)

| 견준 것 | Before — 입력 차례대로 | After — 요청 이름표로 |
|---|---|---|
| 둘째 문의에 붙은 것 | `inquiry-3`의 답 `환불` | 오류 코드 `unsupported_value` |
| 이름표가 서로 다른 짝 | `3` | 없음 |
| 결과 없이 남은 입력 | `['inquiry-5']` | `['inquiry-2']`(오류 파일에 있음, `[]`) |
| 결과 차례를 거꾸로 했을 때 | 셋째 짝만 우연히 맞음 · 넷째 짝 답이 우연히 맞아 보임 | 답 딕셔너리 같음 `True` |

- 그 밖: 입력 파일 1780바이트 · 작업 상태 `completed`·`{'completed': 4, 'failed': 1, 'total': 5}` · 결과/오류 줄 수 4·1(`True True`) · 토큰 표 40·44·43·46 / 4·5·4·5 / 캐시 입력 0 · 합 173·18 = 작업 사용량 · 예상 비용 `0.00021075` → `0.000105375`달러.

## 7. 서비스 요청 수와 요금표 어림 (청구 금액 아님, mini 0.75·0.075·4.50달러/100만 토큰 — `https://developers.openai.com/api/docs/models/gpt-5.4-mini` 2026-09-29, 할인 50% — `…/guides/batch` 2026-09-29)

| 단계 | 요청 | 어림 |
|---|---|---|
| 노트북 밖 일괄 작업(모델 요청 5줄 — 받아들여짐 4·거절 1) | 파일 올리기 1 · 작업 만들기 1 · 상태 확인 4 · 내려받기 2 | 약 0.000105달러(동기 요금이면 0.00021075) |
| 마른 실행(닫힌 포트) | 0 | 0 |
| 새 커널 A·B · tryA · 짝짓기 5번 · 게이트·그림 | 0 | 0 |
| **합** | 모델 요청 5줄(일괄 작업 안) | **약 0.0001달러** |

- 노트북 한 번 = 모델 요청 0 · 0달러. 절 1달러 상한 안. 서비스 오류는 설계한 400 한 줄뿐.

## 8. 고친 것과 앞 챕터 이음

- 모델·요청 주소를 과정 표준으로(`gpt-5.4-mini`·`/v1/chat/completions`·`temperature` 0·`reasoning_effort` none — Ch 15 08 입력 파일 모양과 같음).
- Before를 실제 결과 파일의 결함으로(옛 `isinstance` 판정 뺌) · 옛 「실제 Batch 제출: 수행하지 않음」 → 노트북 밖 한 번 맡긴 결과를 자료로(노트북에서는 맡기지 않았다고 준비물·3절·b7에 공개).
- **Ch 15 08의 남은 물음에 답**: 「이 본문이 일괄 처리에서 받아들여지는지는 제출하지 않아 확인하지 않았습니다」 → 이번에 맡긴 작업에서 none + 0 네 줄은 200(노트북 3절·b3). Ch 15 08 본문은 고치지 않음(여전히 참 — Ch 15는 맡기지 않았음).
- Ch 15 08 「손으로 적은 결과 줄 다섯 개를 요청 식별자로」 → 이 절은 받은 결과 파일로 같은 `ids_not_in`(노트북 6절 첫 단락).
- 옛 b10 두 링크(2026-09-11) → 참고 자료 넷(Batch API · Using GPT-5.4 · GPT-5.4 mini · 설치판 openai 3.13.0 소스 행 `resources/batches.py` 47~67·`types/batch.py` 40~42·96·`types/file_create_params.py` 31), 모두 2026-09-29 확인.
- 01 b8 「02절은 일괄 처리(Batch API)를 다룹니다. 곧바로 답이 필요 없는 요청을 모아 맡기는 방법입니다」 — 02 내용과 맞아 고치지 않음.
- 이음: 01(문의 분류·요금표·`estimate_cost`) · Ch 15 08(네 칸·JSONL·함수 넷·손 결과 줄) · Ch 6 06(`estimate_cost`·예상 비용 ≠ 청구) · Ch 23(임시 폴더) · 04(요청 제한 — b7 한 문장). Ch 31 언급 0(인계 규칙).

## 9. 도구 파일 `labs/part7/ch34-cost-rate-limits/notebooks/cost_tools.py` 02 판

- **01 판 `af9e1288…` → 02 판 `72429dfa57754a1d041b09f1b93f07ed041a17d463e09bf57d50f00ef5486533`**: 머리 설명(01 그대로) 뒤 `import json` 한 줄 + `estimate_cost`(01 그대로) + Ch 15 08 함수 넷.
  - `make_batch_line`·`write_jsonl`: Ch 15 08 노트북 셀(`labs/part4/…/08-Batch-평가-입력.ipynb`)의 def~return **글자 그대로** · 주석 `# Ch 15 08절에서 배웠습니다 — Ch 15 08절 노트북 셀의 같은 이름 함수를 옮겼습니다` + 설명 한 줄(`write_jsonl`은 셀 첫 줄 그대로, **`make_batch_line`만 설명 줄의 「요청 식별자」(Ch 19 금지어)·「판정 요청 글」을 「요청 이름표(custom_id)」·「요청 글」로 바꾸고 그 사실을 줄 끝에 적음**).
  - `read_jsonl`·`ids_not_in`: Ch 15 `rag_tools.py` 마감 판(`6c59d0f2…` 해시 확인) 설명·def~return 글자 그대로 · 주석 `# Ch 15 08절에서 배웠습니다 — Ch 15 도구 파일 rag_tools.py의 같은 이름 함수를 옮겼습니다`.
- 대조 사슬(`author_02.check_tools02()`, 실행마다): `author_01.check_tools()`(01 사슬) → 02 판이 `TOOLS_HEAD`로 시작·`strip_later_imports(02 판)`이 01 판으로 시작 → 함수 차례 다섯·가져오기 `import json` 하나 → 넷 모두 원본과 def~return 글자·AST 같음 → `rag_tools.py`의 두 함수가 Ch 15 08 셀과도 글자·설명 같음 → 금지 문법 0.
- 쓰기 가드 `write_tools()`: 같으면 그대로, 없거나 01 판이면 02 판으로 쓰고, 02 판으로 시작하는 더 긴 판은 건너뜀, 그 밖은 멈춤. **01 생성기 `write_tools()`를 02 판 위에서 불러 `skip` 확인**(01을 다시 실행해도 02 판을 덮어쓰지 않음).
- 가져오는 절 01·02. 02 준비 셀 결과 읽기에 고정 세 문장 + 커널 폴더 한 문장 + 실행 도구 한 문장. 공개 목록 줄은 01이 이미 넣음(02 판으로 바뀌어도 줄은 같음).

## 10. 자료 파일 (실습 폴더 `data/` — 새 폴더)

| 파일 | 바이트 | sha256 | 담은 칸 |
|---|---|---|---|
| `data/batch-output.jsonl` | 1408 | `41e43483d7d561b195b167e58bc996d8f536ad602789f79cd88822dd2b5ff951` | 줄마다 `custom_id`·`response.status_code`·`response.body`(`model`·`choices[0]`의 `index`·`message.role`·`message.content`·`finish_reason`·`usage` 넷)·`error` |
| `data/batch-errors.jsonl` | 307 | `965a252266a9b2d82cc13f9bb9bcaeeb4b51e86b89ab76ef80c15fbbb17083ae` | `custom_id`·`response.status_code`·`response.body.error`(`message`·`type`·`param`·`code`)·`error` |
| `data/batch-job.json` | 399 | `6c8031d8a30f8bdb8d1808bdaec9ba25650a8cdda6d1e4df39c537f4356702b1` | 작업 객체의 `endpoint`·`completion_window`·`model`·`status`·`request_counts`·`usage` |

- 뺀 것: 줄 `id`·`request_id`·`body.id`·`created`·`object`·`service_tier`·`system_fingerprint`·`refusal`·`annotations`·세부 토큰 칸 · 작업/파일 ID·시각 칸·`metadata`. 줄 차례는 받은 그대로. `make_data02.py`가 ID·시각 모양 글 0을 확인. 출처·맡긴 날은 본문 b7·노트북 준비물·3절에.
- 공개 목록 두 곳에 세 줄: 챕터 `qa/public-files.json`(`cfbb3767…` → `a6a0cbd0097a02300bed73474476f7c34fe83fa2960b554a2fae1660b902c92a`, `cost_tools.py` 줄 뒤) · Part `textbook/part7/public-files.json`(`46cb1691…` → `ea0bd104251df438aea074558a9b1b18881c49d1628effb88f69ac6dd3883cf0`, 정렬 자리 101~103행) — `collect_public_files.py`와 같은 셈을 메모리에서 해 결과가 같음(114줄, 스크립트는 실행 안 함). **`part7-practice.zip`·`llm-practice.zip`·`final-artifact-hashes.json`은 다시 만들지 않음(마감 몫)**.

## 11. 그림

- 설계표 `qa/upgrade/02-figures.md`(렌더 전에 씀) · Mermaid **4장**(02-1 일괄 처리를 맡기고 받는 차례 303 · 02-2 다섯 줄이 간 곳 616 · 02-3 차례대로 짝지은 결과 487 · 02-4 차례와 이름표로 짝지은 두 결과 588 — viewBox 폭, 모두 868 이하, PNG를 열어 확인, 02-3·02-4는 자동 줄바꿈을 `<br>`로 미리 나눠 다시 렌더) · **빨강은 Before 결과 상자 둘뿐**(02-3·02-4 왼쪽) · **보라 0** · 노트북 밖 단계 회색·점선(02-1) · 받은 오류 400 노랑(02-2) · 값 바꿔 보기 상자는 After 칸 안에만(도식 읽기에 「왼쪽 칸에는 해당하지 않습니다」).
- 삽화 **1장** `02-5-한꺼번에-꽂아-둔-배터리`(비유 계열 「충전 거치대와 배터리」의 「한꺼번에 꽂기」): 1차 job `dd4ed46a-6699-4899-a2e3-9968dcf32bba`(원본 `6626d6c8…`) 탈락 — 관계는 읽혔으나 거의 흰 가로줄 226/614 · **2차 job `6d54643e-efa3-4872-986d-5bcf8add1204` 채택**(원본 `7bcbc5f9…` 2752 × 1536 → 저장 1100 × 614 `489d9d51ddfaa33f22201d6d435204a2e5aff0d1fddbe086d9649a13beab87af`, 거의 흰 가로줄 22/614). 거래 23:27:20.235510Z·23:28:31.781514Z 「Nano Banana Pro −2」씩 → **이 절 4크레딧**(잔액 2245 → 2241). `jobs_wait` 모델 표시 `nano_banana_2`(요청 `nano_banana_pro` — 기록만). 결과 URL을 다시 받아 픽셀 대조 bbox `None`·가장 큰 차이 0 · 저장 PNG(보기 사본 bbox `None`)를 열어 셈: 표시등 초록·빨강·초록·초록·초록 · 색 띠 파랑·노랑·보라·분홍·청록. 1차 저장본은 같은 파일 이름에 두었다가 2차로 바꿔 씀(따로 남긴 파일 없음 — 원본은 `/tmp/ch34-02/illu/`).
- 캡션 파일 다섯이 생성기 `FIGn_CAP`·`ILLU_CAP`과 같음.

## 12. 검사

- `run_section.sh … 02 --no-exec`: 렌더 → 첨부 1 → 빌드 → `verify.py --chapter` **PASS 5 sections / 67 code cells (max 19 lines)**(19줄은 03~05 옛 판) → 게이트 wip **G1~G7 0 PASS**(검사 문장 405).
- 빌드한 `02-Batch-API.html` `{{` 0건 · 도식 읽기 4 · 그림 읽기 1 · 다른 절 HTML·`index.html` 바이트 같음(보호 파일 대조).
- `visual.cjs`는 이 절에서 돌리지 않음(챕터 마감 몫).
- `pack.py` → `qa/upgrade/review-pack/02-Batch-API.md`.

## 13. 보호 파일 (`before-manifest.json` 191개)

- **같음 179 · 바뀜 12 · 없어짐 0**. 바뀜 12 = 01이 바꾼 넷 그대로(01 본문·HTML·노트북·옛 생성기 — 01 뒤 해시와 같음) + **02에서 바뀐 여덟**(02 본문·HTML·노트북 · 공개 목록 둘 · `집필점검표.md` · `qa/verification.md` · 노트북 계약 JSON — `manifest-changes.md` 「02절 뒤」). 옛 `runs/` 셋·03~05 파일·옛 그림은 같음.

## 14. 챕터 밖 수정

- `textbook/part7/public-files.json`(자료 파일 세 줄) · `textbook/_notebook/checks/notebook-contracts-part7-ch34-cost-rate-limits.json`(`verify.py --chapter`가 다시 씀, `63f32135…` → `6d20d454cda78470f2f59672d493768407e54d7bb44d1ad69014d66841e4e542`). 그 밖 챕터 밖 파일·공용 도구 고침 0. Ch 15 08 파일·`rag_tools.py`는 읽기만.

## 15. 완료 챕터가 Ch 34에 기대는 문장 (고치지 않음, 참·거짓만)

- `textbook/part7/_src/index.html`·`index.html` 「Ch34의 사용량 관리로 이어집니다」 — **참**.
- `textbook/part7/ch33-cicd/04-모니터링과-알림.html`(Ch 33 — 이번 개선 제외) 「Ch34에서 p95 계산을 더 자세히 다룹니다」 — 05(옛 판) 기준으로 **참**(02와 무관, 05가 바꾸면 05 몫).
- `textbook/part6/ch27-deepagents/08-통합-실행과-운영-한계.html` 149행 — 그림 base64 안의 글자, **거짓 양성**.
- (지시 목록 밖 part4) Ch 15 08 「제출 뒤의 차례 — 이번에 하지 않음」·「이 본문이 일괄 처리에서 받아들여지는지는 … 확인하지 않았습니다」 — Ch 15 자신에 대해 **참**(02가 답을 보탬). `grep 'Ch *34'` part4 0건.

## 16. 강사 확인 대상

1. **노트북 밖 실제 결과를 자료 파일로 두는 방식**: 학생 노트북은 맡기지 않고 교재 작성 때 한 번 맡긴 결과(ID·시각 뺌)를 읽음 — 규격 §3 「실제 처리를 미리 계산한 값으로 바꾸지 않습니다」와의 관계는 「실제로 받은 파일을 칸만 줄여 둠」으로 준비물·3절·b7에 밝힘. 학생이 제 키로 맡기는 셀은 두지 않음.
2. 거절될 줄의 설계(`inquiry-2`만 low + `temperature` 0)와 문의 다섯의 차례(이웃 종류가 모두 다름)는 **흐름을 보여 주려고 정한 예**(b7에 밝힘). 거절은 한 번 맡긴 작업에서 본 사실.
3. 코드 32 → 159줄 · 코드 셀 5 → 29(규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줄 것 — Ch 15 08 함수 넷은 도구 파일로 뺐음).
4. 제목의 「Batch API」는 제목에만, 본문 첫 자리 한 문장으로 풂(01 선례) · 새 말 「요청 이름표(custom_id)」(Ch 15 08 「요청 식별자」의 이 챕터 말) · 일상 예 「외투 보관표」·「수선집에 맡긴 옷」.
5. 도구 파일 `make_batch_line`의 설명 줄만 이 챕터 말로 바꿈(본문 글자 그대로) — 01 머리 설명 「앞 챕터 도구 파일에서 옮긴 함수는 설명 주석과 본문을 글자 그대로」는 도구 파일에서 옮긴 함수(`estimate_cost`·`read_jsonl`·`ids_not_in`)에만 해당.
6. 자료 파일 셋 추가 → 학생 묶음·zip·`final-artifact-hashes.json`은 마감 몫.
7. 삽화: 배터리 몸통이 회색(01 원통과 색이 같음, 모양·띠·선반·구도는 다름) · 빨간 칸 배터리가 안 찼다는 것은 표시등으로만 보임 · 재생성 1회(여백).
8. OpenAI 계정에 남은 파일 셋·작업 기록 하나(아래 17) — 지우지 않음(지우는 API 부르지 않음).

## 17. 지워야 하지만 지우지 않은 것 (삭제 승인 대상)

- **OpenAI 계정(서비스에 올린 것)**: 입력 파일 1개(`purpose` batch, `file-8Zv…`) · 결과 파일 1개(`file-PTY…`) · 오류 파일 1개(`file-VLQ…`) · 일괄 작업 기록 1개(`batch_6abc…`, `metadata` 교재 설명 한 줄). 전체 ID는 `$ROOT/.cache/ch34-02/resume/ids.json`·`raw-batch-final.json`. 설치판 설명: 용도 batch 파일 기본 30일 뒤 만료 · 안내: 결과 파일은 작업이 끝나고 30일 뒤 자동 삭제.
- 연결 폴더: `.cache/ch34-02/resume/`(ids.json·polls.jsonl·raw-output.jsonl·raw-errors.jsonl·raw-batch-create.json·raw-batch-final.json — ID 포함) · `.cache/ch34-02-view/`(삽화 보기 사본 둘) · `qa/upgrade/probe/02-batch.md.tmp`(§0 초안 — 저장 시각 자리 표시가 남은 임시 파일, 실수로 probe 폴더에 씀) · `qa/upgrade/gates-wip-02-02.json`·`gates-wip-02.json`(게이트 중간 결과).
- 기기 `/tmp/ch34-02/`(약 16MB — 스크립트 원본·`nb0`·`tryA`·`A.ipynb`·`B/`·`tools/`(02 판 사본)·`illu/`(원본 PNG 1·2차와 다시 받은 사본)·`figs/`·생성기 조각 `a02_part1~5.py`·`a02_draft.py`·`dryrun.py`·`handoff.before.md`) · 기기 임시 폴더 `$TMPDIR/ch34-02-*` **12개**(노트북 셀의 `mkdtemp` — 제출 스크립트·마른 실행·dryrun·tryA·A·B·짝짓기 5번, 각 입력 파일 1780바이트 하나씩).
- 옛 `runs/batch-input.jsonl`(`ee6ac19d…` — 02가 더는 쓰지 않음, 공개 목록·zip·`final-artifact-hashes.json` 줄과 함께 마감이 처분) · 루트 떠돌이 `batch-input.jsonl`(같은 해시) · 옛 그림 `figures/02-batch-flow.{svg,excalidraw}`(본문 참조 0 — 마감이 다른 절 옛 그림과 함께).
- `__pycache__`·`.pyc` 새로 만든 것 0(모든 파이썬 호출 `PYTHONDONTWRITEBYTECODE=1`·`sys.dont_write_bytecode = True`).

## 18. 기기 디스크

- 루트(`/`, `/tmp` 포함) 여유 **1.5G → 1.5G**(작업 전후, `/tmp/ch34-02` 약 16MB) · 연결 폴더(사용자 디스크) 여유 **73G → 73G**.
