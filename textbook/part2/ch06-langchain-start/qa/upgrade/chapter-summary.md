# Ch 06 LangChain 시작 — 챕터 요약 (다음 챕터 작업자용)

작성 2026-09-17(품질 개선 6절 + 실습 절 07 + 별도 세션 검토 1차 반영 뒤). 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md` §6. 앞 내용: `textbook/qa/upgrade-course-summary.md`(Part 1), 바로 앞 챕터 `textbook/part1/ch05-llm-principles/qa/upgrade/chapter-summary.md`. Part 2 첫 챕터라 같은 Part 안 앞 챕터 요약은 없습니다. 절 사이 인계 원문: `qa/upgrade/handoff.md`(절마다 「새로 가르친 것」「아직 안 가르친 것」 전체 목록). 검토: `qa/upgrade/review-round1.md`, 끝에 「반영 결과」.

절: 01 계층 지도와 첫 호출(paired) · 02 메시지와 제공자 전환(experiment) · 03 구조화 출력과 검증(paired) · 04 스트리밍과 content blocks(experiment) · 05 타임아웃 재시도 폴백(paired) · 06 토큰 비용 지연 비교(experiment) · 07 LangChain 실습: 학습 카드 요청에 폴백과 비용 기록 붙이기(experiment). **처음으로 인터넷 서비스 모델을 실제로 부른 챕터**입니다(OpenAI `gpt-5.4-mini`·`gpt-5.4-nano`만. Anthropic·Google 요청 0번). 코드 셀 130개(15·18·19·19·19·21·19), 게이트 7/7(G1~G7 0, 수정 전 273건), Mermaid 27장(4·4·4·4·4·4·3)·삽화 7장(대기 없음), 모든 노트북 새 커널 실행 PASS.

## 1. 새로 가르친 개념·API·함수·용어 (노트북에서 실행한 것만)

| 절 | 새 API·값 | 직접 만든 함수 | 용어 표 |
|---|---|---|---|
| 01 | `from langchain.chat_models import init_chat_model`, `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` → `ChatOpenAI`(콜론 앞 = 제공자, 만들 때 요청 0번), `model.model_name`·`temperature`·`max_tokens`, `invoke(튜플 목록)` → `AIMessage`, `.text`(**괄호 없음**, 실제 자료형 `TextAccessor`), `.usage_metadata`(`input_tokens`·`output_tokens`·`total_tokens`), `.response_metadata["finish_reason"]`(`stop`/`length`), 인자 `max_tokens=12`, 튜플 내용 `None` → 요청 전 `ValidationError: 2 validation errors for HumanMessage`, `from importlib.metadata import version` | 없음 | API, 제공자, 모델 객체, 메시지와 역할, 응답 객체, 토큰 사용량, 끝난 이유, **출력 상한**(= `max_tokens` = Ch 5 04절 출력 몫), 값 검사 오류. 개념: 프롬프트·컨텍스트·하네스·루프 계층 지도(LangChain = 모델 호출 칸, LangGraph = 루프 Ch 13, DeepAgents = 하네스 Ch 27) |
| 02 | `from langchain.messages import SystemMessage, HumanMessage`, `SystemMessage("글")`, `.type`(`system`·`human`)·`.content`, 튜플 목록과 객체 목록의 입력 토큰 수 같음(33), `openai:gpt-5.4-nano`, `anthropic:claude-haiku-4-5` → `ChatAnthropic`(키 없이 객체만), 같은 호출에 `reasoning_effort="none"` → 생성 단계 `ValidationError`, `from langchain_core.exceptions import ModelNotFoundError`·오타 `gpt-5.4-mimi` → `OpenAIModelNotFoundError`(404, 요청 뒤), `os.getenv(키) is None` | `make_record(model_id, status, output_tokens)` | 메시지 객체, 역할 이름(user ↔ human), 통합 패키지, **실행 상태**(실행함·키 없음·요청 오류, 키가 있으면 `키 있음, 부르지 않음`), 모델 없음 오류, 상태 코드 |
| 03 | `from pydantic import BaseModel, Field`(규격 §2-2 세 문장 + Ch 2 10절 링크 완료), `Field(description=, ge=1, le=3)`, 범위 밖 값 `ValidationError`, `model.with_structured_output(StudyCard)` → `RunnableSequence`(요청 0번) → `invoke` → `StudyCard` 객체, `model_dump()`, `include_raw=True` → `dict`(`raw`·`parsed`·`parsing_error`), `모양클래스.model_json_schema()` | 없음(양식 클래스 `StudyCard`·`NoRangeCard`) | 구조화 출력, 양식 클래스, **칸(필드)**, 범위 규칙, 파싱, 원본 답(raw), JSON 스키마 |
| 04 | `model.stream(messages)` → `generator`(요청 0번, 첫 청크를 꺼낼 때 요청), `AIMessageChunk`, 청크 `+` 합친 메시지, `model.stream_usage`(`True`), `stream(…, stream_usage=False)` → 사용량 `None`, `content`(str)·`content_blocks`(`[{'type': 'text', 'text': …}]`), 스트리밍 `max_tokens=12` → `length`, `enumerate` 재사용 | 없음 | 스트리밍, **청크(chunk) = 한 번에 도착하는 답의 일부**(「조각」 아님), 제너레이터, 합친 메시지, 사용량 청크, 내용 블록 |
| 05 | `init_chat_model(…, timeout=, max_retries=)`, `model.request_timeout`·`max_retries`·`root_client.timeout`/`.max_retries`(적지 않으면 None·None·**시간 제한 없음**·openai 재시도 2), `ModelTimeoutError`(실제 이름 `OpenAITimeoutError`, `timeout=0.001`로 실제 재현), 오류 속성 `is_retryable`, `response_metadata["model_name"]`(날짜판 `gpt-5.4-mini-2026-03-17`), `from langchain_core.runnables import RunnableLambda`, `RunnableLambda(함수).with_retry(retry_if_exception_type=(…,), stop_after_attempt=3)` → `RunnableRetry`, `모델.with_fallbacks([대체 모델], exceptions_to_handle=(…,))` → `RunnableWithFallbacks`, 원소 하나 튜플 `(ModelTimeoutError,)`, `time.perf_counter()`·`round(elapsed, 1)` | `ask_current_model(input_messages)`(바깥 `current_model`·`attempt_log`) | 타임아웃, 재시도, **시도**(요청 한 번, 첫 시도 포함), 시간 초과 오류, 다시 시도할 수 있는 오류, 폴백, **응답한 모델**(응답 메타데이터 `model_name`) |
| 06 | `usage_metadata` 전체(`input_token_details` `{'audio', 'cache_read'}`, `output_token_details` `{'audio', 'reasoning'}`), 캐시 입력 `cache_read`(긴 지시 둘째 요청 1792/1958), 요금표 딕셔너리 키 `ordinary_input`·`cached_input`·`output`, 과학 표기 `9.3e-05`, `time.strftime("%Y%m%dT%H%M%S")`, `sorted()` + `ordered[int(len(ordered) / 2)]`, `set()`·`add()`, `os.path.exists("../runs")`(뜻 한 문장), `json.dumps(…, ensure_ascii=False, indent=2)` + `with open` + `json.loads(file.read())` | **`estimate_cost(usage, input_rate, cached_input_rate, output_rate)`**(Ch 8 테스트가 이름·인자 순서로 꺼냄), **`timed_invoke(run_model, input_messages)`** → `(응답, 걸린 초)`, `make_cost_record(model_id, run_response, run_elapsed, prices)`(한국어 키 9개) | 캐시 입력, 요금표, 예상 비용(청구 금액 아님), 걸린 시간, 가운데 값, 실행 이름(`run_id`) |
| 07 | 새 API 0개. 구조화 호출 객체에 `with_fallbacks()`(05 `with_retry()`처럼 호출 객체에도 같은 메서드) | `estimate_answer_cost(raw_message)`(응답한 모델 이름에 nano가 있으면 nano 요금표), `make_card_record(result, run_elapsed)`(키 8개), `build_card_path(primary_timeout)` + 06 `estimate_cost`·`timed_invoke` 같은 코드, Ch 4 06 `print_report` | 새 용어 0개 |

- **Python 쪽**: 기본 경로 130셀에서 `lambda`·내포식·제너레이터 식·조건 표현식·f-string·`*`/`**` 풀기·`raise`·try `else`/`finally`·이름 없는 `except`·`global`·`:=`·`+=`·`//`·데코레이터(`@`)·`isinstance`·`zip`·`max`·`sum`·`any`·`next`·`Path`·`datetime`·`os.environ` **0건**(검토 AST). 클래스는 `BaseModel` 필드만 3개(03 둘, 07 하나). 함수 정의는 0·1·0·0·1·3·6개, 타입힌트 없음. 새로 풀어 쓴 모양: `type(값).__name__`, 튜플 목록 `for role, content in messages:`, `get(키, 기본값)`, `try/except 오류이름 as error` + `print(error)`(라벨 줄 따로), 원소 하나 튜플, 튜플 반환·풀어 담기, 두 겹 `for`, 글 `+`로 이름 잇기
- **기록 모양**: 한 요청 = 딕셔너리 한 줄, 모르는 값은 0이 아니라 `None`(02·04·06). 딕셔너리 키는 「키」, 양식 클래스 자리는 「칸(필드)」(03·04 인계, 07-5 검토)

## 2. 반복해 쓴 모델·함수·데이터·비유·이름

- **모델 셀**: 모든 절 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(규격 §3). `gpt-5.4-nano`는 02(이름만 바꾸기) → 05(폴백 대체) → 06(비교) → 07(대체 경로). 모델 준비 셀 결과 읽기에 실행일(01 2026-09-16, 02~07 2026-09-17)
- **메시지**: 튜플 목록 `[("system", …), ("user", …)]`이 기본 모양(01~07). system 「한 문장의 한국어로 답하세요.」(02·04·05·06), 01 「두 문장 이내의 한국어로 답하세요.」, 03·07 「초급 학습자를 위한 학습 카드를 만듭니다.」
- **데이터·이름**: 03 `StudyCard`(concept·explanation·difficulty `Field(ge=1, le=3)`) → 07 같은 코드. 오타 모델 `gpt-5.4-mimi`(02 → 05). `timeout=0.001`(05 → 07). 06 `estimate_cost`·`timed_invoke` → 07 같은 코드. 요금표 이름 `pricing_date`·`mini_prices`·`nano_prices`
- **출력 라벨**: 「모델 객체 종류:」「응답 객체 종류:」「답:」「입력 토큰 수:」「출력 토큰 수:」「끝난 이유:」「오류 종류:」「오류 메시지:」「응답한 모델:」「걸린 초:」「예상 비용(달러):」(전체 목록은 handoff 절마다)
- **비유와 삽화**(뜻이 바뀌는 곳마다 그림 읽기에 적음): 01-5 도서관 상담 창구(노란 쪽지 = 프롬프트, 서류철 = 컨텍스트, 쟁반 = 하네스, 둥근 회전판 = 루프 — Ch 5 쟁반 칸 = 토큰과 뜻 다름) → 02-5 우편함 세 개(파란 카드 = system, 노란 카드 = user, 자물쇠 회색 우편함 = 키 없는 제공자) → 03-5 흰 메모와 초록 양식 카드(동그라미 셋 = 난이도) → 04-5 구슬 꿰기(구슬 = 청크, 노란 빈 꼬리표 = 끝난 이유·사용량 청크) → 05-5 나무 레일(모래시계 = 타임아웃, 구슬 한 알 = 요청 한 번, 옆길 컵 = 폴백) → 06-5 저울·동전·초시계(한 줄 = 기록표 한 줄) → 07-4 갈림길 카드와 주황 꼬리표(꼬리표 = 응답한 모델). 일상 예: 번호 저장 전화기(모델 객체), 주소 빈 송장을 받지 않는 택배 접수대(`ValidationError`), 신청서 양식, 티슈 상자(제너레이터), 전화 신호음·문자(타임아웃·폴백), 복사해 둔 서류(캐시 입력), 키 순서로 선 세 사람(가운데 값)

## 3. 07 실습 절 주제와 결과

- 「LangChain 실습: 학습 카드 요청에 폴백과 비용 기록 붙이기」(30분, 따로 과제 없음). 03 `StudyCard` 구조화 호출(`include_raw=True`)을 기본 경로 mini에 붙이고, 05 `with_fallbacks([backup_path], exceptions_to_handle=(ModelTimeoutError,))`로 시간 초과일 때만 nano 구조화 호출로 넘기며, 06 `timed_invoke`·`estimate_cost` + `estimate_answer_cost`로 요청마다 기록 한 줄
- 실행 1 `build_card_path(30)`: 두 질문 모두 `gpt-5.4-mini-2026-03-17`, 190/0/64토큰·0.0004305달러, 188/0/57·0.0003975, 합 0.000828
- 실행 2(값 하나 `0.001`): 두 질문 모두 `gpt-5.4-nano-2026-03-17`, 190/0/70·0.0001255, 188/0/59·0.00011135, 합 0.000237. 같은 토큰 수를 mini 요금표로 계산하면 0.000864(약 3.6배)
- 결론은 「요금표는 응답한 모델 이름으로 고른다」(기록 원칙). 출력 토큰 수·걸린 초 차이는 폴백 탓으로 말하지 않음(06에서 같은 모델도 요청마다 달랐음, 검토 07-1). 답을 받는 요청 4번 + 답 없는 시간 초과 시도 2번
- **시수**: 07 실습 30분은 `chapter.json` 「총 16h · 강의 6h · 실습 10h」에 더하지 않고 실습 10h 안으로 봄(규격 §7-2)

## 4. 다음 챕터(Ch 07 프롬프트 엔지니어링)가 이어받을 것

Ch 07은 8절(01 역할별 메시지와 제약 ~ 08 프롬프트 버전과 AB 비교, 모두 experiment, `chapter.json` 「총 24h · 강의 8h · 실습 16h」)이고 아직 개선 전입니다. 아래는 개선 전 Ch 07 파일을 읽고 확인한 것입니다.

- **Ch 7 01 `_src` b2 4행 「Ch 6에서는 문자열이나 메시지 목록을 모델에 전달하여 첫 응답을 받았습니다」는 사실과 다름**. Ch 6은 문자열 하나로 `invoke`한 적이 없습니다(01~07 모두 튜플 목록, 02만 메시지 객체 목록). 「튜플 목록이나 메시지 객체 목록」으로 고치고, 문자열 하나로 부르려면 그 자리에서 한 문장으로 가르칩니다
- **Ch 7 08 `_src` b3 「같은 측정 형식만 이어서 사용합니다」는 모양이 다름**. Ch 6 기록 키는 한국어(`모델`·`응답한 모델`·`입력 토큰 수`·`캐시 입력 토큰 수`·`출력 토큰 수`·`끝난 이유`·`걸린 초`·`예상 비용(달러)`)이고 시간 단위는 초(`round(elapsed, 2)`)입니다. Ch 7 개선 전 표는 영어 키·`latency_ms`. 「같은 측정 항목」으로 고칩니다. 같은 b3의 「`time.perf_counter()`로 호출 지연을 기록」은 맞습니다(05·06)
- **`runs/provider-comparison-continuity.json` 계약(바꾸지 않음)**: 최상위 키 6개 `run_id`·`run_date`·`source_chapter`·`conditions`·`pricing`·`records`, `pricing["openai"] == {"ordinary_input": 0.75, "cached_input": 0.075, "output": 4.50}`(mini), `pricing["date"]`(`2026-09-17`). Ch 7 08 노트북 셀 10(필수 키 6개 `assert`, `pricing["openai"]` `assert`, 파일 SHA-256)·셀 18(`run_id`·`pricing["date"]`·`pricing["openai"]`)이 읽는 것은 이것뿐이고 `records` 키는 읽지 않습니다. 현재 파일: run_id `ch06-provider-20260917T020433`, SHA-256 `f18920c63088bded645bc4712b8ee16436e46d394499bfeaa4cc081f76ef4f4c`, `conditions` = `repetitions`·`max_tokens`·`max_retries`·`messages`, `pricing` = `date`·`unit`·`openai`·`openai_nano`, 기록 6줄(mini·nano 번갈아 세 번). 06 노트북은 실행마다 이 파일을 덮어쓰고 시각별 사본을 만들지 않습니다. **Ch 6 06을 다시 실행하면 해시가 바뀌므로 다시 실행하지 않습니다**
- **Ch 7 08 노트북 셀 10·18이 쓰는 문법**: `next((path for path in [Path.cwd(), *Path.cwd().parents] if …), None)`, `raise FileNotFoundError`, `required <= ch06_record.keys()`, `datetime`·f-string 안 식·딕셔너리 내포 — 모두 Ch 6이 가르치지 않았고 사다리 금지 대상. 경로는 Ch 6 06의 `os.path.exists("../runs")` + 긴 경로 모양(Ch 5 01 모양)으로 바꿀 수 있습니다. 해시는 Ch 6에서 가르치지 않았으므로(Part 1에도 없음) 쓰면 세 문장으로 풉니다
- **알려진 실패와 해소 순서(§9)**: Ch 7 08은 품질 개선 때 새 커널로 다시 실행해 `source_record`를 현재 Ch 6 파일 해시로 이어야 합니다. 옛 Ch 7 08 노트북을 지금 돌려 사슬만 잇지 않습니다(개선 전 Ch 7 본문 b6의 토큰·지연 숫자와 어긋남)
- **출력 상한**: Ch 6은 `max_tokens`를 「출력 상한」이라 부르고 Ch 5 04 출력 몫과 같은 뜻이라고 01 용어 표에 적었습니다. Ch 7이 `max_tokens`를 쓰면 「01절 출력 상한」으로 잇습니다. Ch 8 01 「출력 예약분」은 Ch 8 작업자 몫
- **temperature**: API `temperature=0`을 `do_sample=False`와 같다고 쓰지 않음(01 모델 셀, 02~07 결과 읽기). 같은 입력을 temperature 0으로 보내도 낱말이 달랐음(02 「말투」→「톤」, 04 invoke·stream 답 다름) → 「비슷한 답, 똑같다고 보장하지 않음」
- **구조화 출력은 양식을 요청에 실어 입력이 늘어남**: 07 같은 첫 질문을 양식 없이 보내면 입력 61토큰, 양식을 붙이면 190토큰(기기 셸 한 번, 07 b7). Ch 7 07 「구조화 출력 프롬프트 진단」이 토큰 수를 비교하면 이 차이를 잇습니다. 03 After(범위 규칙 있는 양식에 「difficulty는 반드시 9」)는 노트북에서 3이었고, 검토에서 세 번 더 보내도 3(`NoRangeCard`는 두 번 모두 9)이었지만 **서버가 늘 막는다는 증거로 쓰지 않습니다**. `parsing_error`에 오류가 담기는 경우는 실행하지 않았고, 범위 밖 값의 `ValidationError`는 `invoke()`에서 날 수 있다(소스)까지만 적었습니다
- **노트북 출력 칸**: 요청을 기다리는 반복문 안의 `print`(특히 `flush`)는 노트북에 stream 출력 여러 개로 저장되어 `render.py` HTML이 칸마다 나뉩니다(04 첫 실행 21칸, 07 첫 실행). **요청이 끝난 뒤 한꺼번에 출력**합니다. Ch 7 06 Self-Consistency처럼 반복 요청을 찍는 셀에 해당
- **예상 호출 수·비용**: 06 요금표 기준 짧은 요청 한 번은 mini 약 0.0002달러·nano 약 0.00005달러, 약 2,000토큰 지시는 mini 약 0.0016달러. 캐시 입력은 규칙 문장 50번(약 1,250토큰)에서 0, 80번(1,958토큰)에서 1792 — 생긴다고 보장하지 않음
- **평가·환각**: Ch 6은 답 내용의 정확성을 판정하지 않았습니다(모든 절 해석 범위). Ch 5 07 판정 규칙(새 숫자·보류 문장)은 Ch 6에서 쓰지 않았습니다
- Ch 6 07 b8·노트북 끝은 「Ch 7 01이 `init_chat_model`·`invoke`·`usage_metadata`를 씀」이라고 적었습니다(개선 전 Ch 7 01 `_src` 확인). Ch 7 01이 바뀌면 Ch 6 07 b8을 다시 확인합니다

## 5. 아직 가르치지 않은 것 (Ch 07이 설명 없이 전제하면 안 되는 것)

- **LangChain**: `ChatPromptTemplate`·`MessagesPlaceholder`·프롬프트 템플릿 전체(Ch 7 04 주제), 대화 이력(앞 답 `AIMessage`를 목록에 넣기 — 01은 「넣지 않으면 이어진 대화가 아님」까지), `AIMessage(…)` 직접 만들기, **문자열 하나로 `invoke`**, `batch`·`ainvoke`·`astream`(01 표에 「이 챕터에서 실행하지 않음」), 파이프 `|` 연결(`RunnableSequence`는 이름만 봄), 구조화 호출 스트리밍·`with_structured_output`의 `method`/`strict`·`TypedDict`·JSON 스키마 딕셔너리 양식·`parsing_error`가 채워진 경우, 재시도와 폴백을 한 호출에 함께 붙이기·폴백 여러 개·모두 실패, `with_retry`의 대기 인자, 도구 호출·에이전트(Ch 19~), 콜백
- **서비스**: 다른 제공자 실제 요청·그 사용량, 429·5xx·401, 첫 청크 시간, 캐시 유지 시간·`prompt_cache_key`, Batch·Flex·지역 처리 요금, 실제 청구 금액, 추론 토큰이 0이 아닌 설정(`reasoning_effort`는 01에서 「none」 뜻만)
- **Python**: `print`의 `end`·`flush`, `+=`, 내장 `sum`·`max`·`zip`·`any`·`all`·`bool()`, `lambda`·내포식·제너레이터 식·조건 표현식, **f-string**(Part 1에서 변수만 넣은 모양은 배웠지만 Ch 6 기본 경로 0건), `raise`·try `else`/`finally`(A), `isinstance`, `pathlib.Path`·`datetime`, `@` 줄, `*args`·`*목록` 풀기, `or`로 기본값, 해시(`hashlib`)·`read_bytes()`, 집합 비교 `<=`, 상속·`ConfigDict`·`model_validate()`, 정규식
- **평가**: 답 정확성 판정, 비율 지표, LLM 판정자(Ch 15), mention_count 같은 문장 속 낱말 세기 지표

## 6. A·B 트랙 제약

- A 트랙(기본 경로)은 Ch 2 09~11절(데코레이터 `@`, Pydantic `BaseModel`, 패키징)을 건너뜀. Ch 6은 `@` 줄 0건. `BaseModel`·`Field`·`ValidationError`는 01(`ValidationError`)·03(`BaseModel`·`Field`)에서 세 문장 + Ch 2 10절 링크를 마쳤으므로 Ch 7은 「Ch 6 03절 양식 클래스」로 이어 쓰면 되고 다시 세 문장을 쓰지 않아도 됩니다. 클래스 이름 뒤 괄호 `(BaseModel)`의 뜻은 「그 틀의 값 검사 기능을 물려받은 양식」 한 문장으로만 풀었고 상속 설계는 가르치지 않았습니다
- 엄격 모드·선언하지 않은 칸 거부는 확장 경로(B)의 Ch 2 10절에만 있음(03 b7). try `finally`는 B만

## 7. 기준 버전·요금 확인 날짜

- 실습 폴더 `labs/part2/ch06-langchain-start/pyproject.toml`·`uv.lock`: langchain **1.4.0**, langchain-core **1.6.2**, langchain-openai **1.6.0**, openai **3.10.0**, tenacity **9.1.4**, langchain-anthropic **1.7.1**, langchain-google-genai **4.4.0**, pydantic **2.13.5**, python-dotenv **1.2.3**. 노트북 준비물마다 기준 버전과 「다른 버전과 Windows·macOS에서는 이번에 실행하지 않았습니다」
- 요금(OpenAI 모델 페이지, **확인 2026-09-17**, 100만 토큰당 달러): mini 0.75·캐시 0.075·출력 4.50(2026-09-09 값과 같음), nano 0.20·0.02·1.25. 두 페이지 모두 regional processing 10% 추가 표기, 날짜판 `gpt-5.4-mini-2026-03-17`·`gpt-5.4-nano-2026-03-17`. 01~05 준비물 비용 문장은 「06절 4절에서 2026-09-17에 확인한 공식 요금 기준」(검토 C-1)
- 소스로 확인한 기본값: langchain-openai `max_retries` None이면 넘기지 않아 openai 기본 2, `timeout` None은 그대로 넘겨 시간 제한 없음, openai 재시도 대상 시간 초과·연결·408·409·429·5xx(404 아님), 폴백 모두 실패 시 `first_error`. **온라인 LangChain Models 문서 「default: 6」, openai README 「기본 10분」은 설치 판과 다름**(05 b7). 온라인 문서는 OpenAI 스트리밍 사용량을 opt-in으로 안내, 설치 판은 기본 주소일 때 기본 켬(04 b7)
- 노트북 출력: 06 run_id `ch06-provider-20260917T020433`, 07 `outputs_sha256` `cc2a57d9…`

## 8. 실행 환경

- Cowork 기기 셸(Linux aarch64, Python 3.12.13). 가상환경 `$ROOT/.cache/vm/venv-ch06-langchain-start`, uv 캐시 `$ROOT/.cache/vm/uv`(`run_section.sh` 자동, torch 없음). 절 새 커널 실행 10~30초. 키는 루트 `.env`의 `OPENAI_API_KEY`(`find_dotenv(usecwd=True)`), 값은 출력하지 않음. 기기 루트 여유 약 633MB(마감 시점)
- 시스템 `python3`는 3.12가 아니라 `tomllib`이 없음 → `check_course_continuity.py` 같은 검사는 `uv run --project labs/part2/ch06-langchain-start python …`, Ch 8 테스트는 `uv run --no-project --with pytest python -m pytest -q -p no:cacheprovider …`
- `run_section.sh`는 노트북이 첨부하는 「오늘 볼 그림」 PNG가 없으면 첨부 단계에서 멈춤 → `.mmd`를 먼저 두고 실행. `visual.cjs`는 공용 도구를 고치지 않고 `/tmp/chNN-*/vis/vis.cjs`(`require('/tmp/pw/node_modules/playwright')`) + `LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu`, HTML을 사본 폴더에 복사해 실행
- 클라우드 `/mnt/user-data/outputs`가 입출력 오류로 막혀(2026-09-17) 04~07 삽화는 기기 셸 `curl` + `uv run --no-project --with pillow`로 1100px 저장, 원본 해시와 픽셀 대조 기록
- 07 생성기 `author_07.py`의 결과 읽기 네 곳은 자리 표시 글이라 `/tmp/ch06-07/readings.py`로 채웠음 → 07을 생성기로 다시 만들면 결과 읽기를 다시 채워야 함. 설명만 고칠 때는 `mdpatch.py` → `--no-exec`(노트북 단락은 **빈 줄로만** 나뉘어 G6가 셈)

## 9. 알려진 뒤 챕터 실패와 해소 순서

- **원인**: 06 품질 개선 실행(2026-09-17 02:04)이 `runs/provider-comparison-continuity.json`을 다시 써서 SHA-256이 옛 `531b30d0…`에서 `f18920c6…`로 바뀜. 기록 키도 영어에서 한국어로 바뀌었지만 **뒤 챕터 코드는 기록 키를 읽지 않아 키 언어는 실패 원인이 아님**(검토 C-2 판단, 영어로 되돌려도 풀리지 않음)
- **실패 ①** Ch 8 `labs/part2/ch08-context-engineering/tests/test_ch06_ch08_continuity.py::test_log_paths_are_portable_from_student_working_directories`: 06 노트북 원문에 `"[Path.cwd(), *Path.cwd().parents]"`·`"runs_dir = course_root"` 문자열이 없음(사다리가 금지한 문법을 테스트가 요구)
- **실패 ②** 같은 파일 `test_continuity_logs_form_a_hash_verified_chain`: Ch 7 `prompt-ab-continuity.json`의 `source_record.run_id`가 옛 `ch06-provider-20260909T173655923454Z`
- **실패 ③** `textbook/qa/check_course_continuity.py` 66~76행 `part2_handoffs`: 73행 `assert digest(source_path.read_bytes()) == source["sha256"]`에서 멈춤(이 뒤 검사는 실행되지 않아 결과 모름). 마감 세션에서 옮기기 전후 두 번 실행해 같은 자리 확인. 통과한 Ch 8 테스트 3개(`test_cached_input_cost_is_separated_in_all_three_chapters` 등)는 그대로 통과
- **해소 순서**: (1) Ch 6 06 — 끝남, 다시 실행하지 않음 → (2) **Ch 7 08 품질 개선 때 새 커널 실행**(source_record를 현재 Ch 6 파일로) → (3) Ch 8 06 새 커널 실행(Ch 7 파일로) → (4) Ch 8 테스트 수정: 실패 ①은 문자열 검사를 「노트북이 `../runs` 또는 `labs/part2/<챕터>/runs`로 경로를 고른다」 검사로 바꿈(예: `'os.path.exists("../runs")' in source or '[Path.cwd(), *Path.cwd().parents]' in source`, `runs_dir = course_root` 조건도 함께 완화), 실패 ②·③은 (2)(3) 뒤 통과 확인. `check_course_continuity.py`는 ch07·ch08 `runs/continuity/` 사본만 요구하므로 Ch 7 08·Ch 8 06 재실행 때 그 사본을 만드는지 확인
- 옛 실행 사본 3개(`runs/continuity/20260909T172541476581Z`·`…173324758111Z`·`…173655923454Z`)는 `qa/upgrade/before/runs/continuity/`로 옮김(삭제 아님, 마지막 것이 옛 정본 `531b30d0…`와 같음)

## 10. 그림 색 판단 선례

- 넣은 문장·설정·양식·요금표·재료 **초록**, 실행한 코드 줄·라이브러리 단계·정의한 함수(`invoke`·`stream`·`with_fallbacks`·`estimate_cost`) **파랑**, 실행한 서비스 모델 **보라**(없는 모델 이름 `typo_model`은 서버에 없어 초록), 출력으로 확인한 값·객체 종류·끊긴 답·사용량 `None`·모델별로 모은 결과 **노랑**, 실행하지 않은 단계·요청을 보내지 않은 제공자·출력에 나오지 않은 폴백 안 시간 초과·「순위는 정하지 않음」 **회색**
- 오류: 받아 출력·기록한 `OpenAITimeoutError`·404·**02-2 `ValidationError`(검토 02-1에서 빨강 → 노랑, Before가 아닌 값 바꿔 보기에서 받아 출력한 오류)** 노랑. 빨강은 paired Before 결함 결과만: 01-4 `ValidationError`(요청 전 거부), 03-4 오류 없이 범위 밖 9를 받아들인 결과, 05-4 폴백 없이 답을 못 받은 결과
- sequenceDiagram: `messageAlign: left` + 한 줄 라벨, 요청 실선·응답 점선, 메모는 기록 시점(만든 직후 / 응답 뒤 / 반복 뒤). 긴 오류 이름은 `%%{init: {"flowchart": {"wrappingWidth": 320}}}%%` + `<br>`. LR이 868을 넘으면 TB나 한 상자로 합침(01-1·03-1·06-3). LR 두 칸 subgraph가 세로로 쌓이면 `R1 ~~~ R2`(07-3)

## 11. 강사 확인 대상

- **04·05·06 강의·실습 범위 문장**(검토 C-5): 04 강의 3~7절·실습 8~11절, 05 강의 3~5·7·9·10절·실습 6·8절, 06 강의 3~7절·실습 8~10절(준비물·b5). 검사 문장 수 04 417·05 419·06 450으로 1시간 강의에 많음(강의 속도는 재지 않음). meta 「강의 1h · 실습은 챕터 전체 10h 안에서」 유지
- 챕터 시수 「총 16h · 강의 6h · 실습 10h」 유지, 07 실습 30분은 실습 10h 안
- 결정 Q1~Q8 권고대로 유지한 설계: 01 Before 빨강·출력 상한 12 실험, 02 nano 도입·「키 있음, 부르지 않음」, 03 뺀 범위(엄격 모드·추가 칸 거부·JSON 주문), 04 `flush` 없이 모아 출력, 05 `timeout=0.001` 실패 재현·`root_client` 노출, 06 세 제공자 비교를 OpenAI 두 모델로 바꿈·캐시 시연 규칙 문장 80번, 07 결론 범위·07-3 회색·삽화 꼬리표
- runs 파일 한국어 기록 키 유지와 알려진 실패 3건을 Ch 7·8 개선 때 푸는 순서(§9)
- 규격에 더한 세 줄(§3 서비스 모델 절은 설명 수정 때 재실행 안 함, §5-3 Before가 아닌 절의 받은 오류 노랑, §7-2 뒤 챕터가 읽는 산출 파일 계약)
- 기준 버전 표기와 온라인 문서·설치 판 차이 문장(05 b7 기본 재시도 6·10분, 04 b7 스트리밍 사용량)

## 12. 남은 것

- **전체 마감 때**: 다운로드 묶음 `textbook/downloads/part2-practice.zip`(Ch 6은 개선 전 노트북·옛 README, 07 없음) 재생성, Part 2 목차(`textbook/part2/_build_index.py`·`index.html`, Ch 6 절 수 6) 재생성
- 2차 검토(`review-round1.md` 끝 「볼 곳」), 강사 확인
- 다시 실행할 일이 생기면 함께 고칠 코드(지금은 결과 읽기 문장으로만 바로잡음): 05 [24] 주석 「(시도 3번)」→「(소스 기준 최대 시도 3번)」(`author_05.py`), 06 `make_cost_record()`·07 `make_card_record()`의 `run_usage["input_token_details"]["cache_read"]` → `details = run_usage.get("input_token_details", {})` 두 줄. **06은 다시 실행하면 runs 해시가 또 바뀌므로 Ch 7 08 사슬과 함께 계획**
- Ch 13 루프를 삽화로 다시 그리면 프롬프트에 「a curved motion arc drawn around the round board」처럼 도는 모양을 적음(01-5는 회전이 보이지 않아 그림 읽기 문장으로 보강, 검토 01-1)
- 정리 대상(삭제하지 않고 목록만, 삭제 승인 필요): `figures/01-layer-map.*`~`06-observation.*`(옛 Excalidraw·SVG 12개)·`figures/_gen_figures.py`, `labs/part2/ch06-langchain-start/__pycache__/_make_notebooks.cpython-312.pyc`·`.ruff_cache`·`.venv`(2026-09-09 옛 가상환경), `qa/upgrade/__pycache__`, `qa/upgrade/gates-wip-01.json`~`07.json`, `qa/upgrade/before/06-to-07/`(06 수정 전 사본)·`before/review-round1/`(검토 반영 전 review-pack·README·chapter.json·02-2 그림), `.cache/vm/venv-ch06-langchain-start`(전체 마감 때), 기기 `/tmp/ch06-01`~`/tmp/ch06-07`·`/tmp/ch06-review`·`/tmp/ch06-close`·`/tmp/ch06-make_notebooks.bak.py`
- **전체 마감 2026-09-30: 청크 표기** — 04 본문·노트북 마크다운(생성기 `author_04.py` 글 문자열 포함)의 한정어 없는 「청크」 → 「스트림 청크」, 「사용량 청크」 → 「사용량이 든 스트림 청크」(치환 100곳, 긴 문장 넷은 줄여 씀) · 노트북 5절 설명에 「셀 주석과 출력 라벨의 「청크」는 스트림 청크를 줄여 쓴 말입니다」 한 문장 · 05 한 곳·06 세 곳(04절을 가리키는 문장) · 캡션 기록 `figures/04-1·2·3·5.caption.md`의 설명 대상 문장·캡션 줄. 그대로 둔 것: 코드 셀 주석·출력 라벨(셀 18·20·22·24·26·28·30·36·38·40), 그림 04-1~04-4 라벨(`.mmd`·SVG·PNG)과 그 대체 텍스트, 그림 이름 `04-2-청크-도착-순서` — 다시 렌더·재실행 몫. 노트북 04·05·06 `code_sha256`·`outputs_sha256` 전후 같음(04 `6e83108e7d88`/`95515df1b0a0`). 게이트 7/7 · `verify.py` PASS 7/130. 기록 `textbook/qa/final-close-log.md`.
