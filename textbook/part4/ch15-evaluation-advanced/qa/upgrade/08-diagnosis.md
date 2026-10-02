# 08절 진단과 개선 기록 — Batch 평가 입력

- 절: `08-Batch-평가-입력` · 형식 **experiment**(유지) · 작업 2026-09-21
- 정본 생성기: `qa/upgrade/author_08.py`(노트북 + `_src` 본문을 함께 씀, `--src-only`는 본문만, `AUTHOR08_NB_ONLY=1`은 노트북만). **모델 요청 0번 절**이라 출력이 모두 결정적입니다. 설명만 고칠 때는 `mdpatch.py` → `run_section.sh … --no-exec`(다시 실행해도 같은 출력·같은 파일이 나오지만 노트북 해시 비교를 위해 규격 §3 차례를 따름).
- 수정 전 사본: `qa/upgrade/before/`(`_src`·노트북·`figures/08-평가-흐름.*`·옛 생성기, 챕터 첫 절 전에 이미 있음). **이번에 옛 입력 파일 사본 `before/runs/batch-eval-input.jsonl`(`4f898d7d…`)을 더했습니다**(복사, 원본은 노트북이 다시 씀).

## 1. 게이트 전후

| 게이트 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 9 | 5 | 0 | 0 | 6 | 19 | 3 | 42 |
| 수정 후(`gates-wip-08.json`) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

코드 셀 4 → **26**(준비 셀 2: import·자리 찾기 + 기본 경로 24, 설치 셀·키 셀·모델 셀 없음), 코드 줄(주석·빈 줄 제외) 37 → 175, 검사 문장 78 → **387**. 기본 경로 셀 최대 **10줄**(`PROMPTS` — 07절 글자 수 대조), 함수 본문 최대 **8줄**(`line_problems`). **첫 실행 전 `upgrade_gates.py … --section 08`로 G1~G6 0을 먼저 확인**(G6 넷 — 괄호 뒤 마침표 한 곳·영문 시작 두 곳·70자 넘는 참고 자료 한 줄, 한 단락 여섯 문장 한 곳 — 을 고친 뒤 실행), 게이트 때문에 다시 실행한 일 없음.

## 2. 수정 전 주요 문제

1. **요청 본문이 이 챕터의 판정 요청이 아니었습니다**: `input`이 f-string `"질문: …\n응답: …"` — 판정 머리글도 근거 문서도 없는 글이라 02~07절이 보낸 판정 요청과 다릅니다. 모델 설정(`temperature`·추론 설정)도 없었습니다.
2. 금지 문법: f-string `custom_id`·`next(p for p in [Path.cwd(), *Path.cwd().parents] …)`·`''.join(… for x in rows)`·`[json.loads(line) for …]`·`all(…)` 여섯 번·`len(set(ids))`·집합 내포식·`sorted(set(…) - set(…))`·`.get('model')`·`Path` (G1 9, G2 5).
3. 셀 앞뒤 설명·결과 읽기 없음(G5 6), 70자 넘는 문장·「엔드포인트」·「택배 운송장」 비유(과정 금지어)(G6 19), 옛 `{{svg:08-평가-흐름}}` 한 장(G7 3).
4. b8 「Ch16에서는 이 회귀 결과와 실행 추적을 사용해 …」는 Ch 16 개선본에서 확인하지 않은 연결이었습니다. 「공식 문서는 50% 할인」은 2026-09-10 확인 날짜만 있었습니다.

## 3. 결정

### 3-1. `runs/batch-eval-input.jsonl` — **다시 씀**(보호 파일·묶음 허용 목록에 있는 파일, 이름·자리 그대로)

- **까닭**: 이 절의 학습 목표가 입력 파일을 쓰는 것이고, 노트북을 실행하면 파일을 씁니다(학생도 같음). 옛 파일 세 줄은 이 챕터의 판정 요청이 아니라서(§2-1) 옛 바이트를 지킬 까닭이 없습니다. 이름·자리를 바꾸면 허용 목록 두 곳·Part 7 선행 목록 두 곳·README 7행을 모두 고쳐야 해서 그대로 뒀습니다.
- **전후 해시**: `4f898d7d14b6094ae4bc32f3e277ccf99744749c20357c8daab470bffb8f3bd5`(3줄·941바이트, 2026-09-10) → **`0177cebc207151657385a7a11ec2147b0bc45edc2b35f09c7f6fb2b7f8988e3e`**(6줄·51145바이트). 새 커널 두 번(A·B)과 묶음 모양 확인 실행(§6) 모두 같은 해시 — 내용이 결정적입니다(시각·실행 이름 없음).
- **새 파일의 계약**: 줄 여섯, 줄마다 칸 넷 `custom_id`·`method`·`url`·`body`(이 차례), `custom_id` = `old-Q002`·`old-Q006`·`old-Q090`·`new-Q002`·`new-Q006`·`new-Q090`, `method` `POST`, `url` `/v1/chat/completions`, `body` 칸 넷 `model` `gpt-5.4-mini`·`temperature` `0`·`reasoning_effort` `none`·`messages`(사용자 메시지 하나, 내용 = 판정 요청 글 3161·3183·5093·3160·3183·5117자). `ensure_ascii=False`, 줄 끝 `\n`.
- **읽는 쪽**(`grep -rn 'batch-eval-input'` — `.cache`·`before`·`node_modules` 밖, `.py`·`.json`·`.md`·`.html`·`.ipynb`·`.toml`·`.txt`·`.sh`):
  - `textbook/part4/public-files.json` 44행 · `ch15-…/qa/public-files.json` 9행 — **이름만**(묶음 허용 목록). 고칠 것 없음.
  - `textbook/part7/prerequisite-files.json` 2행 · `textbook/part7/ch34-cost-rate-limits/qa/prerequisite-files.json` 2행 — **이름만**. `textbook/part7/_build_index.py` 63~69행이 이 이름이 공개 파일인지만 보고 Part 7 묶음에 넣습니다(내용을 읽지 않음). → **알려진 실패**: `part7-practice.zip`(108항목, 작업 전 모두 현재 파일과 같았음)의 이 한 항목이 옛 바이트라 `textbook/part7/qa/check_delivery.py` 92행 `assert data == (ROOT / entry["path"]).read_bytes()`에서 멈춥니다(같은 대조를 스크립트로 확인, 검사 스크립트 자체는 결과 파일을 써서 실행하지 않음). **해소 순서**: Ch 15 마감에서 `part4-practice.zip`을 다시 만든 뒤 `python3 textbook/part7/_build_index.py`로 Part 7 묶음을 다시 만듭니다(챕터 밖이라 이번에 하지 않음). `llm-practice.zip`에도 이 파일이 있으나 그 묶음은 이미 Ch 1 01절에서 Stale입니다.
  - `textbook/part7/ch34-cost-rate-limits/_src/02-Batch-API.html` 4행(b3) — 「Ch 15의 `runs/batch-eval-input.jsonl`에서는 평가 입력 형식을 준비했습니다. 이번 절은 같은 JSON Lines(JSONL) 원리를 Responses API의 실제 배치 요청 구조에 적용합니다」. 새 파일도 평가 입력 형식이라 문장은 그대로 맞습니다. **Ch 34 작업자에게**: 새 파일의 요청 주소는 `/v1/chat/completions`(Responses 아님)이고 본문 칸이 `messages`·`reasoning_effort`입니다. Ch 34 02 노트북은 이 파일을 읽지 않습니다(`ticket-*` 요청을 자기 `runs/batch-input.jsonl`에 씀).
  - `labs/part4/ch15-evaluation-advanced/README.md` 7행 — 「OpenAI Batch API 제출 형식의 로컬 검증 결과입니다. 실제 업로드, Batch 완료, 실제 할인 청구를 확인한 기록은 아닙니다.」 여전히 맞는 문장입니다. README 전체는 개선 전 판이라 챕터 마감에서 한 번에 고칩니다(handoff 공통).
  - `textbook/part4/qa/check_bundle_execution.py` 31행 — 08 **노트북**을 묶음에서 API 키 없이 실행(파일은 묶음 임시 폴더 안에 새로 씀). §6 확인 실행으로 통과를 봤습니다.
  - 옛 생성기 `_author.py`(실행 막힘)·`.moai/`·`qa/language/snapshots`·`textbook/part4/qa/language/*`(2026-09-10 옛 기록)·Ch 14 `before-2-7/part4-public-files.json` — 옛 기록, 고칠 것 없음.
  - **코드로 이 파일의 내용을 읽는 쪽은 0건**입니다. `textbook/qa/upgrade-contracts.md`에는 이 파일이 **적혀 있지 않았습니다**(`grep -n 'batch-eval-input'` 0건) — 과정 공통 파일이라 이번에 줄을 더하지 않았고, Part 4 갱신 때 §3 Part 4 표에 더할 줄을 아래에 둡니다.
    > `ch15-…/runs/batch-eval-input.jsonl` | Ch 15 08 | 6줄, 줄마다 `custom_id`·`method`·`url`·`body`, `url` `/v1/chat/completions`, `body` `model`·`temperature`·`reasoning_effort`·`messages`, `custom_id` `old-/new-` + 질문 번호. 읽는 쪽: 묶음 허용 목록 두 곳·Part 7 선행 목록 두 곳(이름만), Ch 34 02 b3(이름만) | `4f898d7d…` → `0177cebc…`
- 보호 파일 대조(`before-manifest.json` 36개): 작업 전 어긋남 0 → 작업 끝 **1건 = 이 파일**(의도한 변경). 나머지 35개 어긋남 0.

### 3-2. 모델 요청 0번 · G4

- `check_bundle_execution.py`가 학생 묶음에서 **API 키 없이** 08을 실행하므로(`scope` 「no API key copied」) 키 확인 셀·모델 셀·모델 요청을 넣지 않았습니다. 설치 셀도 없습니다(표준 기능 + 도구 파일, 도구 파일은 `json`·`math`만 가져옴 — 01절 선례).
- **G4 판정**: 규격 §7 G4는 「가짜 모델 클래스·import 0건, 모델 생성 셀의 `temperature=0` 누락 0건」입니다. `upgrade_gates.py`(`check_notebook`)는 코드 셀에서 `FAKE_MODEL` 정규식(`BaseChatModel`·`FakeListChatModel`·`GenericFakeChatModel`·`FakeMessagesListChatModel`·`class Scripted`)과 `init_chat_model(...)` 호출의 `temperature=0` 유무만 셉니다. 이 노트북에는 둘 다 없어 **G4 0은 구조상 0**(모델을 부르지 않는 절, 01절과 같음)입니다. 모델 설정은 요청 본문의 **데이터**(`"temperature": 0`·`"reasoning_effort": "none"`)로만 들어 있고, 가짜 모델로 판정을 흉내 내지 않았습니다(결과 줄은 「손으로 적은 요청 식별자」로 밝힘).
- **07절 요청 글과 같은 글인지**: 머리글·두 칸 짝·이후 판 답·이후 판 사례 목록·자리 찾기·자료 읽기를 07 생성기와 **문자열이 같은** 코드로 적었습니다(`ROOT_PATH`·`READ_CASES`·`JUDGE_HEAD`·`NEW_ANSWERS`·`NEW_CASES` 다섯 문자열 대조 `True`). 노트북 2절이 `build_judge_prompt`로 만든 요청 글 여섯의 글자 수를 07 노트북 5절 출력(3161·3183·5093 / 3160·3183·5117)과 출력으로 대조해 세 줄 모두 `True`. 본문은 「글자 수가 같다고 글이 같다는 보장은 아니다 → 같은 코드로 적었으므로 같은 글」로 적었습니다.

### 3-3. 요청 본문 모양 — 확인한 것과 확인하지 못한 것

| 무엇 | 어떻게 확인했나 | 결과 |
|---|---|---|
| 02~07절 모델 요청이 나가는 주소와 칸 이름 | 설치판 `langchain-openai` 1.6.1(`.cache/vm/venv-ch15-evaluation-advanced`) 소스 `chat_models/base.py` 1924~1937·1939~1966·4464~4476행 + **요청을 보내지 않고** `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none", api_key=가짜 글자)._get_request_payload("안녕")`(`/tmp/ch15-08/payload_probe.py`, 네트워크 요청 없음, 키 값 출력 없음) | `_use_responses_api` **False** → `root_client.chat.completions` 호출(1448·1807행), 본문 `{"model": "gpt-5.4-mini", "stream": false, "temperature": 0.0, "reasoning_effort": "none", "messages": [{"content": "안녕", "role": "user"}]}` |
| 일괄 처리 입력 한 줄 모양 | OpenAI Batch 안내 https://developers.openai.com/api/docs/guides/batch (2026-09-21 확인, platform.openai.com/docs/guides/batch가 여기로 옮겨감) | 칸 넷 `custom_id`·`method`·`url`·`body`, 「the parameters in each line's `body` field are the same as the parameters for the underlying endpoint」, 「each input file can only include requests to a single model」, 「Each request must include a unique `custom_id` value」, 주소 `/v1/responses`·`/v1/chat/completions`·`/v1/embeddings`·`/v1/completions`·`/v1/moderations`·`/v1/images/generations`·`/v1/images/edits`·`/v1/videos`, 용도 `"batch"`, 처리 기한 `"24h"`(유일), 「50% cost discount compared to synchronous APIs」, 한 묶음 요청 50,000개·파일 200 MB, 결과 줄 칸 `id`·`custom_id`·`response`·`error`, 「the output line order may not match the input line order」, 실패한 요청은 `error_file_id`의 오류 파일, 상태 `validating`·`failed`·`in_progress`·`finalizing`·`completed`·`expired`·`cancelling`·`cancelled` |
| `gpt-5.4-mini` 추론 설정 | 모델 안내 https://developers.openai.com/api/docs/models/gpt-5.4-mini (2026-09-21) | 「Reasoning.effort supports: none (default), low, medium, high and xhigh」, 끝점 목록에 Batch `v1/batch` |
| Chat Completions 칸 `reasoning_effort`·`temperature` | 설치판 `openai` 3.16.2 `types/chat/completion_create_params.py` 230~239·318~324행(공식 API 참조 페이지는 WebFetch로 본문을 읽지 못함 — 스크립트로 그려지는 페이지) | `reasoning_effort`: 「Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, and `max` … Not all reasoning models support every value」, `temperature`: 「between 0 and 2」 |
| Batch 만들기 칸 | 설치판 `openai` 3.16.2 `types/batch_create_params.py` | `completion_window` `Literal["24h"]`, `endpoint` 목록(위와 같음), 입력 파일은 용도 `batch`, 요청 50,000개·200 MB |
| Responses 주소의 추론 설정 모양 | Reasoning 안내 https://developers.openai.com/api/docs/guides/reasoning (2026-09-21) | `reasoning={"effort": "low"}` 꼴(본문 b7에 「`/v1/responses`면 칸 `reasoning` 안의 `effort`」 한 줄, 이 절은 그 모양으로 파일을 만들지 않음) |

- **결정**: 주소 `/v1/chat/completions`, 본문 `model`·`temperature` 0·`reasoning_effort` `none`·`messages`(사용자 메시지 하나). 02~07절이 실제로 보낸 요청과 같은 주소·같은 칸 이름이라 「같은 요청을 파일에 담는다」가 맞습니다. `stream` 칸은 넣지 않았습니다(기본값 false로 보고, 이 절은 스트림을 다루지 않음 — 본문에는 적지 않음). 과정 설정과의 대응은 본문 b4 「모델 설정을 본문 칸으로」와 노트북 3절에 한 문장씩(「이 과정의 LangChain 판은 이 설정의 요청을 주소 `/v1/chat/completions`로 보냅니다」·「두 설정은 같은 이름의 본문 칸에 들어갑니다」).
- **확인하지 못한 것(강사 확인 대상, 본문 b7에 적음)**: (1) 이 본문이 일괄 처리에서 실제로 받아들여지는지(`temperature` 0과 `reasoning_effort` `none`을 함께 준 `gpt-5.4-mini` 요청은 02~07절 **동기 요청**에서만 정상이었음). (2) 일괄 처리로 받은 판정이 하나씩 보낸 판정과 같은지. (3) 요청 식별자에 쓸 수 있는 글자·길이 제한(안내에서 찾지 못함 — 이 절은 영문·숫자·줄표만 씀). (4) 겹친 요청 식별자가 든 파일을 올렸을 때 서비스의 동작. (5) 50% 할인·24시간이 실제 청구·걸린 시간에서 그대로인지. (6) Chat Completions API 참조 페이지 원문(스크립트로 그려져 WebFetch로 읽지 못해 설치판 SDK 문서 문자열로 대신함).

### 3-4. 실제 제출 — **하지 않음**

- 파일 올리기·일괄 작업 만들기·상태 확인·결과 받기 요청을 한 번도 보내지 않았습니다(API 키도 쓰지 않음). 본문 b4 「제출 뒤의 차례 — 이번에 하지 않음」은 안내에 적힌 차례만, b7 첫 항목 「이 절은 입력 파일까지 만들고 제출은 하지 않았습니다」, 그림 `08-1`의 점선 끝 회색 상자 「이번에 하지 않음」.
- 결과 잇기(노트북 7절)는 **손으로 적은 결과 줄 다섯 개의 요청 식별자**(`new-Q090`부터 차례를 섞고 `old-Q006`을 뺌)로만 연습했고, 「실제로 받은 결과가 아니라 흐름을 보여 주려고 정한 값」을 코드 주석·설명 셀·b7에 적었습니다. 실제 결과 줄의 칸(`id`·`custom_id`·`response`·`error`)은 흉내 내지 않았습니다.

### 3-5. 용어 · 비유

- 새 용어 넷(meta `새 용어 4`): **일괄 처리(Batch API)**(요청 여러 개를 파일 하나에 담아 한꺼번에 맡기고 결과는 나중에 파일로 받는 방식) · **요청 식별자(custom_id)**(요청 한 줄마다 붙이는 겹치지 않는 이름) · **요청 주소(url)** · **요청 본문(body)**. 뜻 → 일상 예(궤짝·이름표·가게 창구·주문서) → 이 절 코드(`batch-eval-input.jsonl`·`old-Q002`·`/v1/chat/completions`·설정 세 칸과 메시지). 그 밖에 「요청 방식(method)」 `POST`는 한 문장으로 풂. 「묶음」은 01절(개발·시험)과 학생 묶음 뜻이 있어 **쓰지 않고** 「일괄 처리」로 옮겼습니다. 「엔드포인트」·「completion window」·「purpose」는 「요청 주소」·「처리 기한」·「용도」로.
- JSONL은 Ch 9 06절에서 연 말이라 「한 줄에 JSON 하나를 두는 형식」 한 문장으로 가리킴(노트북 3절·b3). `Batch`는 절 제목(`chapter.json`)과 「일괄 처리(Batch API)」에만.
- 금지어(분기·경로·반환·임계값·재정렬·쿼리·인덱스·융합·RRF·조각·노드·한 겹 더·돌려줍니다·돌립니다·돌려 보·재 보·회수·함정·간단히·쉽게·당연히·개선 전·강사 시연·레코드·Recall@·top-k·프롬프트·문맥·거부·사전·페이지·옵션·정규화·검색기·컬럼·집합·택배·「캐시」 단독·한정어 없는 「청크」·게이트·엔드포인트) 본문·노트북 설명·코드 주석·`print` 라벨 **0건**(코드 이름 `build_judge_prompt`·`make_prompts` 제외, 07절 `banned.py`로 셈).
- 비유: 챕터 계열 **바구니·사과·저울** — 나무 궤짝 하나(입력 파일) 안의 바구니 여섯(요청 여섯), 바구니마다 빨간 사과 한 알(판정받을 답), 손잡이마다 색이 다른 빈 이름표(요청 식별자), 옆 저울 접시는 빔(모델 요청 0번). 「택배 운송장」 비유는 없앴습니다.

## 4. 설계 — 노트북 차례

1 준비(import `json`·`os`·`platform` + `from rag_tools import build_judge_prompt`, 고정 세 문장 / 자리 찾기) → 2 07절 요청 글 다시 만들기(사례 읽기·머리글·이후 판 답 둘·이후 판 사례·`make_prompts`·07절 글자 수 대조) → 3 요청 한 줄의 모양(본문 설정·요청 주소·`make_batch_line`·한 줄의 칸) → 4 요청 여섯 줄(`make_batch_lines`·`old`/`new`) → 5 입력 파일 쓰기와 다시 읽기(`write_jsonl`·쓰기·`read_jsonl`·다시 읽기·첫 줄 앞부분) → 6 제출 전 검사(`line_problems`·검사 표·`duplicate_ids`·겹친 요청 식별자) → 7 결과를 요청 식별자로 잇기(`ids_not_in`·손 결과 줄·판 표시와 질문 번호) → 8 값 바꿔 보기(두 판 모두 `judge` → 겹친 세 이름) → 정리 세 줄.

- **이 절이 처음 가르친 함수 여덟(노트북에만 있음)**: `make_prompts(judge_head, pair, case_list)` · `make_batch_line(custom_id, url, settings, prompt_text)` · `make_batch_lines(version_tag, prompts, url, settings)`(안에서 `make_batch_line`) · `write_jsonl(file_path, lines)` · `read_jsonl(file_path)` · `line_problems(line, url, model_name)` · `duplicate_ids(id_list)` · `ids_not_in(first_ids, second_ids)`.
- 이 챕터에서 처음 쓴 파이썬: **파일 쓰기** `with open(…, "w", encoding="utf-8")` + `file.write(json.dumps(…, ensure_ascii=False) + "\n")`(Ch 9 06 관례), `os.makedirs`(Ch 9 06·Ch 7 08), 줄마다 `json.loads`로 JSONL 읽기(Ch 9 06 `split("\n")`), 목록 `+`로 잇기, 글 `split("-")`, 글 `count("\n")`, 글 슬라이스 `[:154]`, 목록 `==` 비교. 판정 머리글·`copy()`·`list(….keys())`는 앞 절에서 씀.
- AST로 따로 센 금지 문법(f-string·`key=`·`reverse=`·`set`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`setdefault`·`.get`·`+=`·한 줄 다중 대입·튜플 풀기·기본값 매개변수·타입힌트·내포식·`lambda`·조건 표현식·클래스·세미콜론) **0건**(07절 `astcheck.py` 사본 `/tmp/ch15-08/astcheck.py`).
- `assert`는 정한 값에서 나온 줄 수·겹친 요청 식별자·손 결과 줄의 짝 찾기에만(여섯 개). 모델이 쓴 글은 이 절에 없습니다.

## 5. 도구 파일 (§2-7) — **바꾸지 않음**

- 다시 쓰는 앞 절 함수는 02절 `build_judge_prompt` 하나이고 이미 도구 파일에 있습니다. 07절 `check_by_average`·`broken_cases`·`check_by_case`와 01~06절 노트북에만 있는 함수는 이 절이 쓰지 않아 옮기지 않았습니다(07절 `broken_cases`의 「인자 차례를 바꿔 두 번 부르기」 모양만 새 함수 `ids_not_in`에 이어 씀). `rag_tools.py` 해시 `123a0b62…` 그대로 → 01·03~07 노트북 확인 사본 실행은 필요 없었습니다(01~07 노트북·`_src` 해시 작업 전후 같음).
- 고정 세 문장은 노트북 1절·b3에 규격 문구대로 한 번씩.
- 노트북이 새로 **읽는** 파일은 없고(자료 파일은 01절부터), 새로 **쓰는** 파일은 허용 목록에 이미 있는 이름이라 `public-files.json`을 고치지 않았습니다.

## 6. 실행값 · 요청 수 · 비용

| 실행 | 때(UTC) | 코드 | 입력 파일 | 비고 |
|---|---|---|---|---|
| A | 18:35:48 | `code_sha256` `b86060ce…`, outputs `8dff52a6…` | `0177cebc…` | `run_section.sh … 08` 안의 새 커널 |
| B | 18:36:13 | `b86060ce…`(같음), outputs `8dff52a6…`(같음) | `0177cebc…`(같음) | **교재 출력**. A와 셀별 출력 **26/26 같음**(`cmp_outputs.py`). 뒤에 `mdpatch.py`로 설명 네 곳만 고침(출력 26/26 그대로) |
| 묶음 모양 확인 | 18:38:15 | 같은 노트북 사본(`code_sha256` 같음, outputs `311efc78…` — 자리 찾기 줄 때문) | `0177cebc…`(같음) | `/tmp/ch15-08/bundle/part4-practice/labs/part4/…`에 노트북·도구 파일·자료 파일만 두고 `--cwd notebooks`, `OPENAI_API_KEY`·`PYTHONPATH` 없이 새 커널 → PASS. 셀별 출력 25/26 같음, 다른 한 셀은 `찾은 프로젝트 맨 위: ../../../..`(자리 찾기 — 기대한 차이) |

- 두 실행이 같은 까닭: 모델·임베딩 요청이 없고 모든 값이 자료 파일과 코드에 적은 값이라 결정적입니다. 달라진 셀·달라진 파일 바이트 없음.
- **서비스 요청 0번**(모델·임베딩·파일 올리기·일괄 작업 모두 0, API 키를 읽는 셀 없음). 탐색 실행 없음. 확인에 쓴 요청 본문 모양 점검(§3-3)도 요청을 보내지 않았습니다.
- 준비물의 실행 시간: B의 execute 한 번이 `real 0.86`초(커널 시작 포함) — 「교재 출력을 만든 실행에서는 노트북 전체가 몇 초 안에 끝났습니다」.
- 작업 환경 판: 02~07절과 같은 가상환경(Python 3.12.13, `langchain 1.4.0`·`langchain-core 1.6.3`·`langchain-openai 1.6.1`·`openai 3.16.2`). 노트북 코드는 표준 기능만 씀.

## 7. 탐색 실행과 정한 예 (규격 §3 — b7에 밝힘)

- 탐색 실행 없음(모델 요청 0번). 정한 값: 판 표시 `old`·`new`, 07절 글자 수 여섯(07 출력에서 옮겨 적음), 손으로 적은 결과 줄 다섯 개(차례를 섞고 `old-Q006`을 뺌), 값 바꿔 보기 `judge`. 모두 실행 A 전에 생성기에 적었고 이후 바꾸지 않았습니다(A와 B 사이 코드 같음).

## 8. 그림

- Mermaid 4장: `08-1`(폭 393) · `08-2`(627) · `08-3`(667) · `08-4`(528). **보라 0**(모델을 부르지 않음) · **빨강 0**(experiment, 겹친 요청 식별자는 코드가 잡아 출력한 결과라 노랑). 제출 뒤의 일은 점선 끝 회색 「이번에 하지 않음」. 설계표 `qa/upgrade/08-figures.md`.
- 첫 렌더를 PNG로 직접 보고 세 장을 고쳤습니다 — `08-1` 파일 이름·검사 상자 줄바꿈, `08-2` 칸 안 상자에서 칸 밖으로 잇는 선 때문에 `direction TB`가 무시되어 폭 1157 → 선을 칸끼리 이어 627, `08-4` 두 상자 줄바꿈(555 → 528). 두 번째 렌더를 다시 열어 확인(확인용 사본 `.cache/ch15-08/fig08-1-a·b`·`fig08-2-a·b`·`fig08-3-a`·`fig08-4-a·b.png`).
- 삽화 `08-5-궤짝에-담은-이름표-바구니`: **1차 job `e3767412-fff9-42d8-b035-c4d81cffb88c` 채택**(재생성 없음). 2크레딧, 잔액 2649 → **2647**. 원본 `03d373fc…`(2752 × 1536) → 저장 1100 × 614 `4eb498ffa9f5f77503ac7f7ed976ad5e8d7082803b5197f84135212c210fbf53`. **결과 URL을 다시 받아(같은 해시) 같은 폭으로 줄인 그림과 픽셀 대조 차이 0**(bbox `None`, extrema 모두 `(0, 0)`). 저장 PNG와 같은 파일(`.cache/ch15-08/illu-job1-preview.png`·`illu-job1.png`, 해시 같음)을 직접 열어 그림 읽기를 썼습니다. 프롬프트의 개수·배치(궤짝 하나·바구니 여섯·사과 여섯·색이 다른 이름표 여섯·빈 저울 접시)가 그대로 그려졌습니다.
- 옛 그림 `figures/08-평가-흐름.{svg,excalidraw,caption.md}`은 그대로 두었습니다(본문 참조 0, 사본 `before/figures/`).

## 9. 챕터 밖 수정

- **없습니다.** `public-files.json` 두 곳·Part 7 선행 목록·빌드 도구·공용 도구·`upgrade-contracts.md`를 고치지 않았습니다. Part 7 묶음은 이 파일 한 항목이 Stale이 됐습니다(§3-1, 챕터 밖이라 다시 만들지 않음).
- 챕터 안(실습 폴더 포함): 노트북 08 다시 씀, **`runs/batch-eval-input.jsonl` 다시 씀**(의도), `_src/08-*.html` 다시 씀, `qa/upgrade/author_08.py`·`08-figures.md`·`08-diagnosis.md`·`gates-wip-08.json`·`review-pack/08-Batch-평가-입력.md`·`before/runs/batch-eval-input.jsonl`(옛 파일 사본) 새로, `figures/08-1`~`08-5` 새로, `handoff.md`에 「§08 → 실습(09)」, `집필점검표.md`·`qa/verification.md` 08절 행. 빌드 HTML은 08만 바뀜(01~07·`index.html` sha256 작업 전과 같음, `_build.py` 두 번 같음). 도구 파일 그대로.
- `part4-practice.zip`은 다시 만들지 않았습니다 → 08 노트북과 이 파일도 묶음에서 Stale(챕터 마감에서 `_build_index.py`로 해소).

## 10. 검사

- `run_section.sh … 08` → 새 커널 PASS, `verify.py --chapter` `PASS 8 sections / 210 code cells (max 11 lines)`, 게이트 G1~G7 **0**(PASS). 설명·그림을 고친 뒤 `run_section.sh … 08 --no-exec` 두 번 모두 0.
- 빌드 HTML 아홉 개 `{{` 잔존 **0건**, `_build.py`를 두 번 돌려 아홉 개 sha256 같음. 08절 HTML에 Mermaid `svg` 4 · 삽화 1.
- 금지 문법 AST 따로 셈 0건(§4), 금지어 0건(§3-5). 「07절과 같은 코드」는 두 생성기의 다섯 문자열 대조 `True`(§3-2).
- 보호 파일 36개: 작업 전 어긋남 0 → 끝 **1건(의도한 `runs/batch-eval-input.jsonl`)**. `data/evaluation-cases.json`은 읽기만 했습니다(`dc48b1bc…`, 머리 칸 값 출력·인용 0).

## 11. 강사 확인 대상

1. **입력 파일을 다시 썼습니다**(보호 파일·묶음 허용 목록 파일, 이름·자리 그대로, `4f898d7d…` → `0177cebc…`). Part 7 묶음의 이 한 항목이 Stale이 되어 `textbook/part7/qa/check_delivery.py`가 멈춥니다 — Part 4 묶음 재생성 뒤 Part 7 묶음 재생성으로 해소(§3-1).
2. **요청 주소를 `/v1/chat/completions`로 정했습니다**(옛 08·Ch 34는 `/v1/responses`). 02~07절이 LangChain으로 실제 보낸 주소·칸 이름과 맞추려는 결정이고, 설치판 소스와 요청 없는 본문 점검으로 확인했습니다. Ch 34 02(Responses API 일괄 처리)와 나란히 읽힐 때 수업에서 주소 차이를 한 번 짚어 주면 좋겠습니다.
3. **확인하지 못한 것**(§3-3 끝 여섯 가지) — 특히 이 본문이 일괄 처리에서 받아들여지는지, 일괄 판정이 동기 판정과 같은지. 실제 제출은 이 챕터에서 한 번도 하지 않았습니다.
4. 결과 잇기는 손으로 적은 요청 식별자 다섯 개로만 보였습니다(실제 결과 줄 흉내 없음).
5. 한국어 감사 3단·삽화 판정은 별도 세션 몫입니다.

## 12. 지우지 않은 것(삭제 승인 대상)

- `/tmp/ch15-08/`(실행 사본 `runA.ipynb`·`runB.ipynb`, 옛 입력 파일 사본 `batch-eval-input.before.jsonl`, 본문 점검 `payload_probe.py`, 모의 계산 `sim/sim.py`, 묶음 모양 확인 폴더 `bundle/`, 대조 스크립트 `astcheck.py`·`banned.py`·`cmp_outputs.py`·`show.py`, 고침 목록 `reps1.json`, 삽화 원본·대조용 `job1-orig.png`·`job1-again.png`·`job1-1100.png`, 해시 기록 `pre-hashes.txt`·`post-hashes.txt`·`jsonl-A.txt`·`jsonl-B.txt`·`build1.txt`·`build2.txt`, 기록 사본 `집필점검표.before.md`·`verification.before.md`·`handoff.before.md`) — 기기 임시 폴더.
- `.cache/ch15-08/`(그림 확인용 PNG 사본 `fig08-1-a`·`-b`, `fig08-2-a`·`-b`, `fig08-3-a`, `fig08-4-a`·`-b`, `illu-job1-preview.png`, `illu-job1.png`).
- `figures/08-평가-흐름.{svg,excalidraw,caption.md}` — 옛 도식(본문 참조 0, 사본 `before/figures/`).
- `qa/upgrade/gates-wip-08.json`은 챕터 마감의 `gates-after.json`으로 갈음됩니다.

## 13. 검토 1차 반영 (2026-09-21 챕터 마감)

- **B-11** 글 메서드 `count()`를 처음 쓰면서 풀지 않던 것: 코드 앞 설명 셀 [37] 끝에 「글의 메서드 `count()`는 괄호 안에 준 글이 몇 번 나오는지 셉니다.」(검토는 결과 읽기 [39]를 권했으나 규격 §6 「코드 앞 설명 셀: 처음 나오는 함수의 뜻」에 맞춰 앞 셀에 둠).
- **B-12** §3-1 계약 초안에 09절 읽는 쪽을 넣어 `textbook/qa/upgrade-contracts.md` Part 4 표 자리에 Ch 15 입력 파일 줄을 더했습니다(09 노트북 셀 [15]·[17]·[21]·[25] — `custom_id` 모양 `old-`/`new-` + 질문 번호, `url`, `body.model`·`body.temperature`·`body.reasoning_effort`, `body.messages[0].content`).
- **B-19** Part 7 묶음의 옛 입력 파일: 마감에서 `textbook/part7/_build_index.py`를 한 번 돌려 `part7-practice.zip`을 다시 만들었습니다(`chapter-summary.md` §9).
- 노트북은 다시 실행하지 않았습니다. 이 절 노트북의 `code_sha256`·`outputs_sha256`은 작업 전과 같고 설명 셀만 바뀌었습니다(`mdpatch.py` → `run_section.sh … --no-exec`). 생성기 `author_NN.py`의 `SRC_HTML`·`cells()` 설명 셀이 `_src`·노트북과 글자까지 같은 것을 마감 대조로 확인했습니다. 게이트 G1~G7 0.
