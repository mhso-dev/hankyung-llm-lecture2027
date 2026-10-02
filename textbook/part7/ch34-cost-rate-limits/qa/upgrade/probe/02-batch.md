# 02절 일괄 처리(Batch API) 실제 제출 기록 (노트북 밖, 2026-09-29)

챕터 리드 결정 9(handoff 「02 Batch 실제 제출 조건」)·§01 → §02 3·4·7번. 노트북은 제출하지 않고, **노트북 밖에서 한 번** 맡긴 작업의 결과 파일·오류 파일을 실습 폴더 자료로 둔 뒤 읽기만 합니다. 작업·파일·요청 ID는 이 파일에 적지 않습니다(앞 몇 자만). ID는 `$ROOT/.cache/ch34-02/resume/`에만 둡니다. 키는 루트 `.env`에서만 읽고 출력하지 않습니다.

## 0. 제출 전에 적은 설계와 판단 규칙 (이 절을 적은 시각은 아래 「§0 저장 시각」 줄 — 제출 전에 적음)

### 0-1. 문서·설치판으로 먼저 확인한 것 (모델 요청 0)

- 일괄 처리 안내 `https://developers.openai.com/api/docs/guides/batch`(2026-09-29 확인): 「50% cost discount compared to synchronous APIs」 · 「Each batch completes within 24 hours (and often more quickly)」(보통 걸리는 시간은 없음) · 입력 줄 네 칸 `custom_id`·`method`·`url`·`body`, 「Each request must include a unique `custom_id` value」 · 「Note that each input file can only include requests to a single model.」 · 상태 여덟(`validating`·`failed`·`in_progress`·`finalizing`·`completed`·`expired`·`cancelling`·`cancelled`) · 결과 줄 예 `{"id": "batch_req_123", "custom_id": "request-2", "response": {"status_code": 200, "request_id": "req_123", "body": {...}}, "error": null}` · 「Any failed requests in the batch will have their error information written to an error file that can be found via the batch's `error_file_id`.」 · 「Note that the output line order **may not match** the input line order. Instead of relying on order to process your results, use the custom_id field …」 · 만료 때 끝난 요청만 결과 파일에 · 취소는 `cancelling`을 거쳐 최대 10분 · 결과 파일은 작업이 끝나고 30일 뒤 자동 삭제 · 한 작업 요청 5만 줄·200MB.
- GPT-5.4 안내 `https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.4`(2026-09-29 확인) 「GPT-5.4 parameter compatibility」: `temperature`·`top_p`·`logprobs`는 reasoning effort가 `none`일 때만 받고, 「Requests that include these fields will raise an error for GPT-5.4 or GPT-5.2 with any other reasoning effort setting …」. 안내 문장은 GPT-5.4를 적고 GPT-5.4 mini를 따로 적지는 않음 → **mini에서도 거절되는지는 이번 제출로 처음 봄**.
- 모델 안내 `https://developers.openai.com/api/docs/models/gpt-5.4-mini`(2026-09-29 확인): 요청 주소 Chat Completions·Batch 지원 · reasoning effort `none`(기본)·`low`·`medium`·`high`·`xhigh` · 100만 토큰당 입력 0.75·캐시 입력 0.075·출력 4.50달러.
- 설치판 openai 3.13.0(`$ROOT/.cache/vm/venv-ch34-cost-rate-limits`): `client.files.create(file=…, purpose="batch")` · `client.batches.create(input_file_id=…, endpoint="/v1/chat/completions", completion_window="24h", metadata=…)` · `batches.retrieve`·`batches.cancel`·`files.content` · `Batch.status` 여덟 · `request_counts`(`total`·`completed`·`failed`) · `types/chat/completion_create_params.py` 318~319행 temperature 「between 0 and 2」.
- Ch 15 08은 같은 본문 모양(`temperature` 0·`reasoning_effort` none)을 「일괄 처리에서 받아들여지는지는 제출하지 않아 확인하지 않았습니다」로 남김 — 이번 제출이 처음 확인함.

### 0-2. 입력 (노트북 2절 셀과 같은 코드로 만듦 — `/tmp/ch34-02/cells_input.py`, 뒤에 `author_02.py`와 바이트 대조)

- 요청 주소 `/v1/chat/completions`, 모델 `gpt-5.4-mini` 한 가지(한 파일 한 모델), 요청 **5줄**, 이름표 `inquiry-1`~`inquiry-5`.
- 줄 1·3·4·5 본문 설정 = 과정 표준 `{"model": "gpt-5.4-mini", "temperature": 0, "reasoning_effort": "none"}` + 사용자 메시지 하나.
- **줄 2(`inquiry-2`)만** `reasoning_effort`를 `"low"`로 바꾸고 `temperature` 0은 그대로 둠 — 위 GPT-5.4 안내대로면 서비스가 거절할 줄(생각하는 단계만 켜고 온도는 그대로 둔, 실제로 할 법한 실수). 같은 모델이라 한 파일 한 모델 규칙 안.
- 문의 글: 1 배송(01절 문의 글 1) · 2 결제 · 3 환불(01절 문의 글 2) · 4 배송 · 5 결제 — 이웃한 문의의 종류가 모두 달라, 차례대로 짝지으면 밀린 답이 눈에 보이게 정한 예(흐름을 보여 주려고 정한 차례 — b7에 밝힘).
- 입력 파일 1780바이트, sha256 `6ea21c43d31e390d12efa718adff4e9411b4b26176cd87baaae46f5da8c5ca4d`(마른 만들기, 2026-09-29).

### 0-3. 제출 조건과 기다림

- 제출 **한 번**(파일 올리기 1 + 작업 만들기 1, 두 호출 모두 `max_retries=0` — 시간 초과 뒤 SDK가 다시 보내 작업이 둘 생기지 않게). `resume/ids.json`이 있으면 스크립트가 제출하지 않음. 실패하면 다시 제출하지 않고 기록.
- 상태 확인은 셸 호출 하나 165초 안(`timeout 165`)으로 나눠 여러 번. **제출 뒤 30분**이 지나도 `completed`·`failed`·`expired`가 아니면 `batches.cancel` 한 번 → `cancelled`까지 확인하고 사실대로 적음(그때는 이 설계를 쓰지 않고 준비 노트의 다른 후보로, 흉내는 쓰지 않음).
- 작업 `metadata`에는 교재 설명 한 줄만(개인 정보 없음).

### 0-4. 판단 규칙 (결과를 본 뒤 넓히지 않음)

- **결정적인 값(자료 파일에 고정 — 노트북 출력은 새 커널마다 같아야 함)**: 결과 파일 줄 수 · 오류 파일 줄 수 · 줄마다 이름표·상태 코드·오류 코드·답 글·사용량 토큰 수 · 입력 차례대로 짝지을 때 이름표가 어긋난 짝의 수 · 이름표로 짝지을 때 어긋난 짝의 수. 자료 파일이 고정이므로 노트북의 모든 출력은 매번 같음 → 짝짓기 Before/After를 노트북 밖에서 **다섯 번** 돌려 같음을 확인(§3).
- **서비스 판단 값(한 번 제출에서 본 사실)**: 줄 2가 거절되는지 · 거절 이유 · 줄 1·3·4·5가 받아들여지는지 · 결과 파일 줄 차례 · 걸린 시간 · 상태 변화. 한 번만 제출하므로 본문에는 「이번에 맡긴 작업에서는」으로 한정하고, 일반화(「늘 거절된다」·「보통 몇 분」)는 쓰지 않음. 답 글은 모델이 쓴 글이라 파일에 고정되어도 「모델이 쓴 글」이라고 밝힘.
- **Before 결함이 보이는 조건**: 결과 파일 줄 수 < 입력 줄 수(줄 2가 오류 파일로 감). 이러면 결과 파일 차례와 상관없이 차례대로 짝지으면 적어도 한 짝이 어긋남(빨강 = 이 어긋난 짝지음 결과만). 결과 파일 줄 차례가 입력과 달라도 Before 결함은 그대로 보임.
- **설계가 안 되는 경우**: (가) 줄 2도 받아들여져 결과 5줄·오류 0줄 → 차례 짝짓기 결함이 보이지 않을 수 있음(결과 차례가 입력과 같으면) — 입력 줄을 고쳐 다시 제출하지 않음(한 번 조건), 준비 노트 후보 ②(요청 줄 형식)로 바꾸고 진단에 적음. (나) 작업 전체가 `failed`(입력 검사 실패) → 후보 ③(실패한 작업의 오류 모양)을 실제 기록으로 검토. (다) 30분 안에 끝나지 않음 → 취소하고 사실대로.

### 0-5. 자료 파일로 둘 것 (실행마다 다른 값은 뺌)

- `labs/part7/ch34-cost-rate-limits/data/batch-output.jsonl`: 결과 파일 줄마다 `custom_id` · `response.status_code` · `response.body`의 `model`·`choices[0]`(`index`·`message.role`·`message.content`·`finish_reason`)·`usage`(`prompt_tokens`·`completion_tokens`·`total_tokens`·`prompt_tokens_details.cached_tokens`) · `error`. **뺌**: 줄 `id`(`batch_req_…`) · `response.request_id` · `body.id`(`chatcmpl-…`) · `body.created`(시각) · `system_fingerprint` 등 그 밖의 칸.
- `data/batch-errors.jsonl`: 오류 파일 줄마다 `custom_id` · `response.status_code` · `response.body.error`(`message`·`type`·`param`·`code`) · `error`. 뺌: 줄 `id`·`request_id`.
- `data/batch-job.json`: 작업 객체에서 `endpoint`·`completion_window`·`status`·`request_counts`만. 뺌: 작업·파일 ID·시각 칸·`metadata`.
- 줄 차례는 받은 파일 그대로. 원본(ID 포함)은 `resume/`에만.
- 노트북은 세 파일을 **읽기만**. 공개 목록 두 곳(챕터 `qa/public-files.json`·`textbook/part7/public-files.json`)에 줄 추가.

### 0-6. 요청 수와 요금표 어림 (청구 금액 아님)

- 서비스 요청: 파일 올리기 1 · 작업 만들기 1 · 상태 확인 몇 번 · 내려받기 2(결과·오류) — 모델 요청은 일괄 처리 안의 **5줄**(거절될 줄 포함).
- 어림: 줄 하나 입력 약 60토큰·출력 약 5토큰 → 받아들여진 4줄 × (60 × 0.75 + 5 × 4.50) ÷ 100만 × 0.5 ≈ 0.0001달러 미만. 거절된 줄은 토큰을 쓰지 않을 것으로 봄(결과 `usage`로 확인).
- 절 1달러 상한 안.

- §0 저장 시각(기기 `date -u`, 위 본문을 쓴 직후): **2026-09-29T23:08:21Z**.

## 1. 제출과 결과 (한 번, 2026-09-29)

- 스크립트 사본: `probe/cells_input.py`(노트북 2절 셀 글) · `probe/submit02.py`(제출 한 번) · `probe/poll02.py`(상태 확인·내려받기) · `probe/make_data02.py`(자료 파일 셋) — 기기 `/tmp/ch34-02/`의 사본, ID는 들어 있지 않음(모두 `resume/ids.json`에서 읽음).
- 마른 실행(제출 전): 가짜 키 글 + `OPENAI_BASE_URL=http://127.0.0.1:9/v1`(닫힌 포트) → 파일 올리기에서 연결 오류, 서비스 요청 0, `resume/` 쓰기 0.
- 제출 셸 시작 **23:08:46Z** → 파일 올리기(`max_retries=0`, 1780바이트, 파일 ID `file-8Zv…`) → 작업 만들기(`max_retries=0`, 작업 ID `batch_6abc…`) **23:08:49Z** 상태 `validating`. §0 저장(23:08:21Z) 뒤.
- 상태 확인 넷(`resume/polls.jsonl`): +6초 `validating` 0/0 · +53초 `validating` · +81초 `in_progress` 완료 1/5 · +140초 **`completed` 완료 4 · 실패 1 · 모두 5**. 작업 객체 시각 칸: 만든 때 23:08:49Z → `in_progress` 23:09:52Z → `finalizing` 23:10:56Z → `completed` **23:10:57Z**(만든 때부터 **128초**, 약 2분). `errors` None(입력 검사 통과). 취소 없음(30분 규칙 안).
- **결과 파일 4줄**(원본 sha256 `9e752925…`, 1줄씩 이름표·상태·답): `inquiry-1` 200 「배송」 · `inquiry-3` 200 「환불」 · `inquiry-4` 200 「배송」 · `inquiry-5` 200 「결제」 — 줄 차례는 입력 차례에서 `inquiry-2`만 빠진 차례. 응답 모델 `gpt-5.4-mini-2026-03-17`, `finish_reason` 모두 `stop`, 사용량 입력 40·44·43·46 · 출력 4·5·4·5 · 캐시 입력 모두 0 · 추론 토큰 0.
- **오류 파일 1줄**(원본 sha256 `e206522b…`): `inquiry-2` 상태 코드 **400** · `type` `invalid_request_error` · `param` `temperature` · `code` `unsupported_value` · 글 「Unsupported value: 'temperature' does not support 0 with this model. Only the default (1) value is supported.」 — 0-1의 GPT-5.4 안내 규칙이 GPT-5.4 mini에서도 이번 작업에서 그대로 일어남. 줄 바깥 칸 `error`는 null(오류는 `response.body.error`에 있음).
- 작업 객체 사용량: 입력 **173**(= 40 + 44 + 43 + 46) · 캐시 입력 0 · 출력 **18**(= 4 + 5 + 4 + 5) · 모두 191 — 거절된 줄은 토큰을 쓰지 않음.
- Ch 15 08의 남은 물음(본문 `temperature` 0·`reasoning_effort` none이 일괄 처리에서 받아들여지는가)은 줄 1·3·4·5에서 이번 작업에서는 받아들여짐(상태 200).

## 2. 요청 수와 요금표 어림 (청구 금액 아님)

- 서비스 호출: 파일 올리기 1 · 작업 만들기 1 · 상태 확인 4 · 파일 내려받기 2 = 8번(모델 요청 아님). 일괄 처리 안 모델 요청 **5줄**(받아들여짐 4 · 거절 1).
- 요금표(mini 0.75·0.075·4.50달러/100만 토큰, 2026-09-29): 동기 요금으로 세면 (173 × 0.75 + 18 × 4.50) ÷ 100만 = **0.00021075달러** → 안내의 50% 할인을 넣으면 **약 0.000105달러**. 절 1달러 상한 안.
- 계정에 남은 것(지우지 않음 — 서비스 파일 지우기 API 부르지 않음): 입력 파일 1개(`purpose` batch)·결과 파일 1개·오류 파일 1개·작업 기록 1개. 안내: 결과 파일은 작업이 끝나고 30일 뒤 자동 삭제. 입력 파일의 만료는 이번에 정하지 않음(설치판 `files.create`의 `expires_after`를 주지 않음).

## 3. 자료 파일과 짝짓기가 매번 같은지

- 자료 파일(`make_data02.py --write`, 없을 때만 씀, ID·시각 모양 글 0 확인): `labs/part7/ch34-cost-rate-limits/data/batch-output.jsonl`(1408바이트, `41e43483d7d561b195b167e58bc996d8f536ad602789f79cd88822dd2b5ff951`) · `data/batch-errors.jsonl`(307바이트, `965a252266a9b2d82cc13f9bb9bcaeeb4b51e86b89ab76ef80c15fbbb17083ae`) · `data/batch-job.json`(399바이트, `6c8031d8a30f8bdb8d1808bdaec9ba25650a8cdda6d1e4df39c537f4356702b1`). 원본의 `\u` 글자 표기를 한글 그대로 적음(`json.loads` 값은 원본에서 뺀 칸과 같음).
- 짝짓기가 매번 같은지(`probe/pair5.py` — 새 프로세스 다섯, 생성기의 코드 셀 글을 `notebooks/` 자리에서 차례로 실행, 23:25Z): Before 출력 해시 `b0d2ac4b97fc50f5` · After 출력 해시 `235b6c6b7bef5bc1` · 이름표가 서로 다른 짝 3 · 결과 파일에 없는 입력 `['inquiry-2']` — **5/5 같음**. 새 커널 A(23:24:53Z)·B(23:25:03Z)도 29셀 모두 같음(`02-diagnosis.md`).
