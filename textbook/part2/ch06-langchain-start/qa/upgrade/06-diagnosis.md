# 06-토큰-비용-지연-비교 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 06, `figures/06-observation.*`, **`runs/provider-comparison-continuity.json`** — 수정 전 정본, run_id `ch06-provider-20260909T173655923454Z`, SHA-256 `531b30d0…`). 챕터 전체 수정 전 게이트는 01절 때 남긴 `gates-before.json`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 3 | 0 |
| G2 | 3 | 0 |
| G3 | 0 | 0 |
| G4 | 2 | 0 |
| G5 | 14 | 0 |
| G6 | 23 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 9 | 21(준비 3) |
| 검사한 문장 | 169 | 450 |

G8: `run_section.sh` 새 커널 PASS(2026-09-17 두 번 실행, 마지막 `outputs_sha256` `e8fbd975…`, 21 코드 셀), `verify.py --chapter` PASS(6절 111 코드 셀), `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch06-06/vis/` 사본, 작은 글자·대비·잘림·SVG 경계·가로 스크롤·깨진 그림·복사 0). HTML 출력 칸 18개(출력 있는 코드 셀 17개 + 설치 셀의 pip 안내 한 칸, 반복 출력 칸 나뉨 없음).

## 수정 전 주요 문제

- G1: 목록 내포식 `[r for r in records if …]`, 조건 표현식 `None if cost is None else round(cost, 8)`, 제너레이터 식 `next((path for path in [Path.cwd(), *Path.cwd().parents] if …), None)`. G2: 한 줄 `if … :  # 키 필요`, 한 글자 변수 `r`, 15줄 넘는 셀. 사다리 밖(게이트가 세지 않은 것): 키 셀·경로 셀 `raise`, f-string 안 식, `or {}`로 기본값, `*` 풀기, `pathlib.Path`·`datetime`·`mkdir(parents=True, exist_ok=False)`·`relative_to`, 숫자 밑줄 `1_000_000`, 식 안 숫자 `* 1000`, 다섯 칸 튜플 풀어 담기
- G4: 모델 셀 두 곳에 `temperature=0` 없음(`max_tokens=180, timeout=30, max_retries=1`). G5: 제목 셀·핵심 그림·결과 읽기 없음(14). G6: 70자 초과·영문 시작(23). G7: Mermaid 0(옛 Excalidraw 1), 삽화 0, 설계표 없음
- 앞 절과 어긋남(인계 §05 → §06): b3 「두 번째 절에서 제공자별 원본 메타데이터와 표준 필드를 구분했습니다」 — 개선된 02는 `response_metadata`의 다른 키를 다루지 않고, 05가 `model_name`을 처음 읽음. b6 「04절의 스트림에 시작 시각과 첫 비어 있지 않은 텍스트 청크 시각을 추가해야」 — 개선된 04 모양과 맞지 않는 설명. 준비물·요금이 2026-09-09 값만 있고 01~05 준비물이 그 날짜를 인용
- 내용: 세 제공자 비교를 내세웠지만 실제 측정은 OpenAI 한 행 한 번(Anthropic·Google `skipped`)이라 비교할 값이 없음. 캐시 입력 계산을 설명했지만 실행에서 `cache_read`는 0뿐. `max_retries=1`이 걸린 시간·요청 수에 섞일 수 있다는 점 없음. 「첫 텍스트 지연」 표·예시가 실행하지 않은 값 중심. 누락 값 설명이 `or {}` 코드 해설에 기댐

## 바꾼 것

- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(nbkit `key_and_model_cells`, 실행일 nbkit `RUN_DATE` = 2026-09-17). 비교 모델 두 개는 `max_tokens=180, timeout=30, max_retries=0`
- 데이터 유지: 개선 전 질문 「AIMessage의 역할을 한 문장으로 설명하세요.」를 02·04·05절 system 「한 문장의 한국어로 답하세요.」 + user 「AIMessage의 역할을 설명하세요.」 튜플 목록으로. 출력 상한 180, `usage_metadata`·`perf_counter()`·요금·캐시 입력 계산, `runs/provider-comparison-continuity.json` 저장, experiment 형식 유지
- 비교를 실행으로: 키 없는 두 제공자 줄(02절이 이미 기록) 대신, 키가 있는 OpenAI `gpt-5.4-mini`·`gpt-5.4-nano`(02·05절 모델)를 같은 조건으로 **번갈아 세 번씩** 보내 기록표 6줄. 캐시 입력은 **긴 system 지시(지금 시각 + 규칙 문장 80번)를 두 번** 보내 실제로 `cache_read` 1792를 받음
- 기본 경로: 준비(버전 5줄·`json`·`time`·import·키·모델) → 2 튜플 목록 → 3 요청 1번·`걸린 초: 0.97`·사용량 딕셔너리 전체(`input_token_details`·`output_token_details`) → 4 요금표 딕셔너리(2026-09-17) → 함수 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`(`None`이면 `None`, 캐시 키 없으면 `get(키, 0)`) → 교재 예 `9.3e-05`·`None`(assert) → 3절 사용량 `0.00018225`·1,000번 `0.1823` → 5 두 모델·후보 목록(세 칸 튜플) → 6 `timed_invoke(run_model, input_messages)`(튜플 반환) → `make_cost_record(model_id, run_response, run_elapsed, prices)`(키 9개 딕셔너리) → `range(3)` × 후보 번갈아 요청 6번(assert 6) → 7 기록표 출력 → 8 실험 결과 해석: `sorted()`·`int(len / 2)` 가운데 값, `set()` 서로 다른 답 수, 비용 합 → 9 값 바꿔 보기: `time.strftime()` 시각 + 규칙 문장 80번 긴 지시(`messages[1]` 재사용) → 두 번 요청 기록 → 할인 없이 계산한 비용·입력 토큰 수 같음(assert) → 10 기록 딕셔너리(`run_id`·`run_date`·`source_chapter`·`conditions`·`pricing`·`records`) → `os.path.exists("../runs")` 경로 고르기·`json.dumps(…, ensure_ascii=False, indent=2)`·`with open`·다시 읽기(assert)
- 요청 수: 노트북 9번(mini 6·nano 3, 모두 답). 새 커널 실행 2번 = 18 + 탐색 20(`/tmp/ch06-06/probe1·2·3.py`: 짧은 요청 6, 긴 지시 14) → 서비스 요청 합계 38, 모두 답을 받음. 요금표로 어림한 합계 0.05달러 미만
- 새 커널 실행 2번의 이유: 첫 실행에서 규칙 문장 50번(1238토큰) 두 요청이 모두 `cache_read` 0 → 탐색 probe3(50번 1247토큰 0, 80번 1967토큰 1792·1792, 100번 2447토큰 2304·2304)로 80번을 정하고 다시 실행. 결과 읽기·본문·그림 라벨은 두 번째(마지막) 출력으로 `mdpatch.py`와 직접 작성. 첫 실행의 걸린 초 가운데 값은 mini 0.9·nano 1.01(마지막 실행 1.1·0.71과 순서 반대) → b6에 적음
- 요금 확인(2026-09-17): OpenAI 모델 페이지 `gpt-5.4-mini` 입력 0.75·캐시 입력 0.075·출력 4.50(2026-09-09 값과 같음, 01~05 준비물 인용 유지 가능), `gpt-5.4-nano` 0.20·0.02·1.25(02절 「nano 요금은 확인하지 않음」을 이 절이 확인), 두 페이지 모두 regional processing 10% 추가 표기. 요금 요약 페이지 정적 표에는 gpt-5.4 모델이 보이지 않아 모델 페이지 값을 씀. Batch·Flex 등은 미확인(b7). 프롬프트 캐싱 안내: 앞부분 전체 일치, GPT-5.6 이전 모델 최소 길이는 요청 설정에 따라 다름, 128 단위 내림, 이전 모델 캐시 쓰기 추가 요금 없음
- 라이브러리 확인(설치 버전 소스): langchain-openai 1.6.0 `_create_usage_metadata`가 `prompt_tokens` → `input_tokens`, `prompt_tokens_details.cached_tokens` → `input_token_details.cache_read`, `completion_tokens_details.reasoning_tokens` → `output_token_details.reasoning`, `service_tier`가 priority·flex면 키 앞에 접두어(이번 응답은 default). LangChain Messages 문서 예와 키 이름 같음
- 01~05절 인계 반영: 튜플 목록·라벨 줄(01), `usage_metadata`·출력 상한 이름(01), 02 기록표 「한 줄에 한 설정」·nano·키 없는 제공자는 02에서 기록했다고 b3에 적음(개선 전 b3의 「02절 원본 메타데이터 구분」 문장 삭제), 04 「모르는 사용량은 None」→ `estimate_cost(None, …)` 실행, 04 첫 청크 시간 미측정 이어 적음(개선된 04 모양 `for chunk in answer_stream:`으로 b7), 05 `perf_counter`·`round`·`model_name`·`timeout=30` 이어 씀, 05 인계대로 `max_retries`가 기록에 섞이는 영향 → `max_retries=0`과 이유(b3·노트북 5절·복습 4). 챕터 용어: 「출력 상한」 유지, 「조각」 안 씀(b7의 「조각 수」는 Ch 5 01 토큰 뜻 그대로), 03 「칸(필드)」과 겹치지 않게 개선 전 「다음 학습」 문장의 「측정 필드」를 「측정 항목」으로 바꿈, 02 `make_record`와 이름이 겹치지 않게 `make_cost_record`
- 규격 §2-2: `@` 줄·`BaseModel` 없음. Python 새 모양은 모두 배운 것 또는 한 문장 풀이: `9.3e-05` 과학 표기(한 문장), `time.strftime(모양)`(한 문장), 글 `+` 잇기, 세 칸 튜플 풀어 담기(Ch 5), 튜플 반환(Ch 5 08), `set()`(Ch 2 03·Ch 5 06), `sorted()`(Ch 2 03), `int(len(x) / 2)`(Ch 5), `os.path.exists()`(Ch 5 01 준비 셀), `json.dumps(ensure_ascii=, indent=)`(Ch 4 05), `json.loads()`(Ch 5 01), 가운데 값(median, 세 문장). 내포식·조건 표현식·`raise`·f-string·`Path`·`datetime`·`or`로 기본값·`+=`·`isinstance`는 쓰지 않음
- 본문 10블록 다시 씀: 이 절의 질문, 앞에서 배운 내용 표(01·02·04·05, Ch 2 02~04, Ch 4 05·Ch 5 01·08), 비유(소포·저울·동전·초시계), 토큰 사용량과 캐시 입력, 예상 비용 계산(말 → 식 → 숫자 대입, 요금표), 걸린 시간과 가운데 값, 용어 표 6개, 실행 예제 뒤 「번갈아 보낸 순서」·「캐시 입력이 생긴 두 요청」, 실험 결과 해석(순위 안 정함, 첫 실행과 순서 반대, 선택 기준 미설정), 주의 메모 10개, 복습 5문제, 참고 자료 5개
- 뺀 것: 세 제공자 `skipped` 행과 Anthropic·Google 요금(요청하지 않은 모델의 요금 문장), 「첫 텍스트 지연」 표·가정 예시(실행하지 않은 값), 실행 시각별 사본 폴더(`runs/continuity/<시각>/` — `mkdir`·`Path` 필요, b7·README에 적음)
- 그림: Mermaid 4장(06-1 요청 한 번의 기록 TB, 06-2 번갈아 보낸 순서 sequenceDiagram, 06-3 두 모델 세 번 비교 TB, 06-4 캐시 입력 두 요청 TB), 삽화 1장(06-5 소포 세 가지 재기, job a265a646-fb9e-4c11-8696-5a4bad360f33, 2크레딧, 1회 생성 통과, 원본 SHA-256 앞 16자 `7a0aed7a2e365e77`, 저장 PNG 픽셀 대조 차이 0). 옛 `{{svg:06-observation}}`은 본문에서 뺌(파일은 `figures/`에 남기고 `before/figures/`에 사본)
- 실습 폴더 `README.md` 한 문장: 「실행 시각별 사본을 생성합니다 … 마지막 노트북이 이 정본을 읽습니다」 → 「실행할 때마다 덮어씁니다(사본 없음) … Ch 7의 08절 노트북이 이 파일을 읽습니다」

## 뒤 챕터 영향 (챕터 밖 파일은 고치지 않음)

- **Ch 7 08절 노트북**(`labs/part2/ch07-prompt-engineering/notebooks/08-프롬프트-버전과-AB-비교.ipynb` 셀 10·18): 필수 키 6개와 `pricing["openai"] == {0.75, 0.075, 4.50}`·`pricing["date"]`만 읽음 → 새 파일로 확인 True. 기록표 줄 키가 한국어로 바뀐 것은 Ch 7이 읽지 않음
- **해시 사슬 끊김**: 이 절 실행이 `runs/provider-comparison-continuity.json`을 덮어써(새 run_id `ch06-provider-20260917T020433`, SHA-256 `f18920c6…`) Ch 7 `runs/prompt-ab-continuity.json`의 `source_record`(옛 run_id·`531b30d0…`)와 맞지 않음. Ch 7 08을 다시 실행하면 이어짐
- **Ch 8 테스트** `labs/part2/ch08-context-engineering/tests/test_ch06_ch08_continuity.py`: `estimate_cost` 추출·`0.000093`은 통과(직접 확인). `test_log_paths_are_portable…`(노트북 원문에 `[Path.cwd(), *Path.cwd().parents]`·`runs_dir = course_root` 요구)와 `test_continuity_logs_form_a_hash_verified_chain`(위 해시)은 이 판에서 실패 예상 → Ch 7·8 작업자가 테스트·노트북을 함께 고칠 대상(실행하지 않음)

## 검토

- 별도 세션 검토 1차(2026-09-17, `qa/upgrade/review-round1.md`): **accept**(하 2, 공통 C-1·C-2·C-5 반영 전제). 반영 결과: C-1 b4 「01~05절 준비물의 비용 어림도 이 요금표 기준입니다.」, C-2 [43] 결과 읽기 끝 「기록표 줄의 키는 한국어이고, Ch 7 08절은 이 줄을 읽지 않습니다.」(한국어 기록 키 유지, 계약·알려진 실패·해소 순서는 `chapter-summary.md` §4·§9), C-5 범위 단락(강의 3~7절, 8~10절은 실습 시간, **강사 확인 대상**), 06-1 [27] 새 단락(캐시 입력 키를 바로 꺼내 키가 없으면 오류, 코드는 다음 재실행 때 `get`), 06-2 [43] `os.path.exists()` 뜻 한 문장. **06은 다시 실행하지 않음**: `runs/provider-comparison-continuity.json` SHA-256 `f18920c6…` 그대로. 옛 실행 사본 3개는 `before/runs/continuity/`로 `mv -n`. 결정 Q6 권고대로(OpenAI 두 모델 비교·캐시 80번 유지). 반영 방법: `mdpatch.py` → `run_section.sh … 06 --no-exec`(노트북 재실행 없음, 코드 셀·출력 그대로), 마감 게이트 `gates-after.json` G1~G7 0.
- 리뷰 묶음(반영 뒤 다시 만듦): `qa/upgrade/review-pack/`, 반영 전 묶음 `qa/upgrade/before/review-round1/review-pack/`
- 검토자가 볼 곳: (1) 세 제공자 비교를 OpenAI 두 모델 번갈아 세 번으로 바꾼 판단과, 해석을 「순위 안 정함 + 첫 실행에서 순서 반대」로 한정한 문장(b6), (2) 캐시 입력 시연(규칙 문장 80번 + 시각 접두어)이 탐색 뒤 정한 값이고 캐시 생성이 보장되지 않는다는 문장(노트북 9절·b6·b7), (3) 저장 파일 모양 변경(사본 폴더 없음·한국어 기록 키)과 Ch 7·8 연결 영향

## 남은 것

- 기기 `/tmp/ch06-06`(탐색 스크립트·visual 사본·치환 json·삽화 원본)는 정리 대상
- 옛 도식 `figures/06-observation.*`, `labs/.../runs/continuity/2026090*`(옛 실행 사본 3개)는 정리 대상 목록에만 적음(삭제하지 않음)
- 실습 폴더 `README.md` 첫 단락 「Anthropic과 Google 키가 없으면 관련 비교 행은 `skipped`로 기록됩니다」는 개선된 02(「키 없음」)·06(요청 안 함)과 맞지 않음 → 챕터 마감 때 고침
- 챕터 루트 `verification.md`·`집필점검표.md` 위쪽 06 행(2026-09-09 기록)은 개선 전 기록이라 챕터 마감 때 갱신
- 강사 확인
