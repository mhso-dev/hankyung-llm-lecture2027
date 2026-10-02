# 02-메시지와-제공자-전환 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 02, `figures/02-provider-switch.*`). 챕터 전체 수정 전 게이트는 01절 때 남긴 `gates-before.json`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 4 | 0 |
| G2 | 2 | 0 |
| G3 | 0 | 0 |
| G4 | 2 | 0 |
| G5 | 11 | 0 |
| G6 | 10 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 7 | 18(준비 3) |
| 검사한 문장 | 144 | 354 |

G8: `run_section.sh` 새 커널 PASS(2026-09-17, 18 코드 셀), `verify.py --chapter` PASS(6절), `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch06-02/vis/` 사본으로 실행, 작은 글자·대비·잘림·가로 스크롤·깨진 그림 0).

## 수정 전 주요 문제

- G1: 딕셔너리 내포식 `{name: bool(os.getenv(key)) for name, (key, _) in ...}`, 목록 내포식 `[item.type for item in objects]`·`[r["provider"] for r in records if ...]` 2개
- G2: 한 글자 변수 `r`. 그 밖에 괄호 안 풀어 담기 `for name, (key_name, model_id) in providers.items():`, 한 줄 `if … :  # 키 필요`, f-string 안 식 `f"skipped: {key_name} 필요"`, `raise FileNotFoundError`/`RuntimeError`(A 트랙 미교육), 한 dict 리터럴에 다섯 키를 한 줄씩 이어 씀
- G4: 모델 셀 두 곳에 `temperature=0` 없음(`max_tokens=180, timeout=30, max_retries=1`)
- G5: 제목 셀·핵심 그림·결과 읽기 셀 없음(11건)
- G6: 영문 시작 8(「LangChain은」, 「`continue`는」, 「Anthropic과 Google 행은」 등), 70자 초과 1, 5문장 넘는 단락 1
- G7: Mermaid 0(옛 Excalidraw `02-provider-switch.svg` 1장), 삽화 0, 설계표 없음
- 내용: 「제공자 전환」은 키가 없어 OpenAI 한 번만 실행하고 나머지는 `skipped` 글자뿐. 「요청 오류」 상태를 학습 목표에 두고도 실행하지 않음. `content_blocks`(04절 주제)를 설명 없이 기록. 튜플과 객체가 같은 입력이 되는지 확인하지 않음(역할 목록 출력만). b4 「역할은 권한이 아님」·「이전 답을 assistant 메시지로」는 실행하지 않은 동작을 설명
- 앞 절과 어긋남: 01절이 가르친 「출력 상한」 `max_tokens=180`을 이유 없이 씀, 01절 튜플·`ValidationError`·「요청 0번」과 잇지 않음

## 바꾼 것

- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(nbkit `key_and_model_cells`, 실행일 2026-09-17 줄 — nbkit `RUN_DATE`는 공용 값 2026-09-16이라 생성기에서 `RUN_DAY`로 따로 적음). 출력 상한·`timeout`·`max_retries`는 뺌(05절 주제)
- 데이터 유지: 개선 전 system 「한 문장의 한국어로 답하세요.」, user 「채팅 모델에서 system 메시지의 역할은 무엇인가요?」, 세 제공자 이름 `openai:gpt-5.4-mini`·`anthropic:claude-haiku-4-5`·`google_genai:gemini-2.5-flash-lite`, experiment 형식
- 기본 경로: 설치(버전 5줄) → import → 키 → 모델 → 2절 튜플 목록 → 3절 `SystemMessage`·`HumanMessage` 목록(`type(message).__name__ | message.type | message.content`) → 4절 두 목록을 같은 모델로(입력 토큰 수 비교 `assert`) → 5절 값 바꿔 보기 1 `gpt-5.4-nano`(객체 셀·호출 셀) → 6절 값 바꿔 보기 2 콜론 앞 anthropic: 인자 그대로 `ValidationError` → 추론 설정 줄 삭제 `ChatAnthropic`·키 False → 7절 오타 `gpt-5.4-mimi` `ModelNotFoundError`(404) → 8절 `make_record()` 함수·기록 목록·다른 제공자 반복(`for model_id, key_name in other_providers:`)·기록표 출력 → 9절 상태별 줄 수(`get(키, 0) + 1`, `assert`)
- 요청 수: 노트북 4번(mini 2·nano 1·오타 1, 답을 받은 호출 3). Anthropic·Google 요청 0
- 실행 출력(2026-09-17): `SystemMessage | system |`·`HumanMessage | human |`, 입력 33·33(`True`), mini 출력 39, nano 입력 33·출력 44, `1 validation error for ChatAnthropic`·`Input should be 'max', 'xhigh', 'high', 'medium' or 'low'`, `ChatAnthropic`·`ANTHROPIC_API_KEY 설정 여부: False`, `OpenAIModelNotFoundError`·`Error code: 404`·`model_not_found`, `상태별 줄 수: {'실행함': 2, '요청 오류': 1, '키 없음': 2}`. 튜플·객체 두 답은 「말투」→「톤」으로 낱말이 달랐음(한 번 실행한 모습으로만 적음)
- 라이브러리 확인(설치 버전 소스): `langchain/chat_models/base.py` `_init_chat_model_helper`가 `creator_func(model=model, **kwargs)`로 인자를 그대로 넘김, 제공자 표 anthropic → `ChatAnthropic`·google_genai → `ChatGoogleGenerativeAI`. `langchain_anthropic` 1.7.1 `reasoning_effort: Literal["max","xhigh","high","medium","low"] | None`. `langchain_core.exceptions.ModelNotFoundError`(HTTP 404)를 OpenAI(`OpenAIModelNotFoundError(openai.NotFoundError, ModelNotFoundError)`)·Anthropic·Google 통합이 모두 씀. openai SDK는 404를 재시도하지 않음(`_should_retry`: 408·409·429·5xx). `langchain.messages.SystemMessage`는 `langchain_core.messages`와 같은 클래스
- 탐색 실행(교재 밖, 기기 셸 `/tmp/ch06-02/probe1.py`·`probe2.py`): 키 없이 `anthropic:` 객체 생성 가능, `google_genai:`는 생성 단계 `ValidationError`(`GOOGLE_API_KEY/GEMINI_API_KEY` 안내), `reasoning_effort="none"` Anthropic 거부, 오타 이름 404(요청 1번) → 노트북 설계와 b7 주의 메모에 「탐색 실행으로 먼저 확인한 뒤 정한 예」를 밝힘(규격 §3). 합계 서비스 요청: 노트북 4 + 탐색 1 = 5
- 01절 인계 반영: 튜플 모양·`for role, content in messages:`·라벨 줄 따로 이어 씀, 「모델 객체를 만들 때는 요청 0번」을 5·6절에서 다시 확인, `ValidationError`는 다시 정의하지 않고 「01절 노트북 8절에서 본 값 검사 오류」 + Ch 2 10절 링크(b3), `type(값).__name__`·`get(키, 기본값)` 재사용, temperature 0 ≠ `do_sample=False` 한 문장(모델 셀), 답 문장은 `assert`하지 않고 입력 토큰 수·상태 줄 수만 `assert`, 01절 비유(창구 노란 쪽지 = 프롬프트 전체)와 이 절 노란 카드(user 질문)의 뜻 차이를 그림 읽기에 적음
- Ch 5 인계: 역할 딕셔너리 `{"role": "user", …}` ↔ 튜플 user ↔ 객체 human(b3), Ch 5 08절 필수 조건·선택 기준과 모델 이름 바꾸기는 다르다고 적음, 한 번 받은 토큰 수로 모델 차이를 일반화하지 않음
- 본문 10블록 다시 씀: 이 절의 질문, 앞에서 배운 내용 표(01절, Ch 2 03·04·05, Ch 5 04·08), 비유(우편함 세 개), 메시지 객체와 역할 이름, 콜론 앞과 뒤(통합 패키지), 용어 표 6개, 실행 예제 뒤 「모델 이름을 하나씩 바꾸면」·「멈춘 자리가 다른 세 경우」, 실험 결과 해석, 주의 메모 9개(키 True ≠ 인증, 두 제공자 미실행, Google 키 이름, 인자 판 의존, `ModelNotFoundError` 범위, 역할 ≠ 권한 미실행, 탐색 뒤 정한 예, 기준 버전), 복습 5문제
- 그림: Mermaid 4장(02-1 두 표기 같은 요청, 02-2 모델 이름 바꾸기, 02-3 멈춘 자리, 02-4 기록표), 삽화 1장(02-5 우편함 세 개, job 8465ddcc-47a5-402c-bd1a-f18a946f31d6, 2크레딧, 1회 생성 통과, 저장 PNG 픽셀 대조 차이 0). 옛 `{{svg:02-provider-switch}}`는 본문에서 뺌(파일은 `figures/`에 남기고 `before/figures/`에 사본)
- 01절 연결 문장 수정(`mdpatch.py … 01`): 01 본문 b8·노트북 끝의 「모델 이름만 바꿔 다른 제공자에게 같은 요청을 보냅니다」가 02 실행(다른 제공자 요청 0)과 맞지 않아 「모델 이름과 제공자 이름을 하나씩 바꿔, 그대로 되는 것과 다시 확인할 것을 나눕니다」로 고침. 01 게이트 다시 0

## 검토

- 별도 세션 검토 1차(2026-09-17, `qa/upgrade/review-round1.md`): **accept**(하 3, C-1 반영 전제). 반영 결과: C-1 준비물 「요금은 06절 4절에서 2026-09-17에 확인한 mini·nano 공식 요금 기준입니다.」(nano 요금 미확인 문장 삭제), 02-1 그림 02-2 가운데 칸 `ValidationError`를 `fail`(빨강) → `measure`(노랑)로 바꿔 다시 렌더·PNG 확인, 도식 읽기·alt·캡션·`02-figures.md`(experiment의 값 바꿔 보기에서 받아 출력한 오류라 Before가 아님, Ch 5 `ValueError` 선례), 02-2 [30] 「받혔습니다」→「`except ModelNotFoundError` 줄이 이 오류를 받았습니다」, 02-3 용어 표·b6에 `키 있음, 부르지 않음`. 결정 Q2 권고대로(nano·「키 있음, 부르지 않음」 설계 유지). 이 절 그림의 빨강은 0장. 위 「검토자가 볼 곳」 (1)의 빨강 판단은 검토에서 뒤집힘. 반영 방법: `mdpatch.py` → `run_section.sh … 02 --no-exec`(노트북 재실행 없음, 코드 셀·출력 그대로), 마감 게이트 `gates-after.json` G1~G7 0.
- 리뷰 묶음(반영 뒤 다시 만듦): `qa/upgrade/review-pack/`, 반영 전 묶음 `qa/upgrade/before/review-round1/review-pack/`
- 검토자가 볼 곳: (1) 02-2 가운데 칸 `ValidationError` 빨강(받아 출력했지만 그대로 옮긴 인자의 결함, 다음 셀에서 고침 → 01-4 선례)과 02-4 요청 오류 노랑(받아 상태로 기록)의 구분, (2) 실습에 새 모델 이름 `gpt-5.4-nano`를 넣은 판단(규격 §3 시범에서 동작 확인된 이름, 챕터 다른 절은 안 씀)과 nano 요금 미확인 문장, (3) 다른 제공자 줄을 키가 있어도 「키 있음, 부르지 않음」으로 적게 한 설계(실행하지 않은 제공자 코드를 싣지 않으려고)

## 남은 것

- 기기 `/tmp/ch06-02`(탐색 스크립트·visual 사본·치환 json)는 정리 대상
- 옛 도식 `figures/02-provider-switch.*`는 정리 대상 목록에만 적음(삭제하지 않음)
- 강사 확인
