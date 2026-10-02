# 03-구조화-출력과-검증 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 03, `figures/03-structured-output.*`). 챕터 전체 수정 전 게이트는 01절 때 남긴 `gates-before.json`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 1 | 0 |
| G2 | 1 | 0 |
| G3 | 0 | 0 |
| G4 | 1 | 0 |
| G5 | 21 | 0 |
| G6 | 34 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 14 | 19(준비 3) |
| 검사한 문장 | 173 | 368 |

G8: `run_section.sh` 새 커널 PASS(2026-09-17, 19 코드 셀, `outputs_sha256` `120ab544…`), `verify.py --chapter` PASS(6절 76 코드 셀), `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch06-03/vis/` 사본으로 실행, 작은 글자·대비·잘림·SVG 경계·가로 스크롤·깨진 그림·복사·Before/After 배치 0).

## 수정 전 주요 문제

- G1·G2: 상속 클래스 `ClosedStudyCard(StudyCard)` + `ConfigDict(extra="forbid")` + 한 줄에 키 여러 개인 딕셔너리(16줄 셀)
- G4: 모델 셀에 `temperature=0` 없음(`max_tokens=180, timeout=30, max_retries=1`)
- G5: 제목 셀·핵심 그림·결과 읽기 셀 없음(21건)
- G6: 영문 시작 26(「`StudyCard`와」, 「Pydantic은」, 「Before는」 등), 70자 초과 6, 5문장 넘는 단락 2
- G7: Mermaid 0(옛 Excalidraw `03-structured-output.svg` 1장), 삽화 0, 설계표 없음
- 사다리·앞 내용 밖: `raise FileNotFoundError`/`RuntimeError`/`AssertionError`, try `else`, 비교 이어 쓰기 `1 <= x <= 3`, 문자열 하나로 `invoke("…")`(01·02는 목록만), `error.errors()[0]["loc"][0]`, A 트랙에 `BaseModel`을 「10절 B 경로에서 다룬」으로만 소개(규격 §2-2 세 문장 없음)
- 내용: 학습 질문의 「실제 모델 응답 검증」은 난이도 9 요구가 3으로 바뀌어 관찰하지 못했고, 실패 장면(Before/After)은 모델과 무관한 로컬 딕셔너리 7 → 2. 본문 b4의 `method` 세 가지·Anthropic/Google 시그니처·TypedDict/JSON Schema 선택표·strict 두 층 설명 대부분이 노트북에서 실행하지 않은 동작. 「parsing_error에 파싱·검증 오류가 담긴다」는 설명이 설치한 판 소스(openai SDK가 호출 안에서 먼저 검증)와 어긋날 수 있음
- 앞 절과 어긋남: 02 인계 「답을 이름 있는 칸으로 받고 AIMessage와 비교」를 실행하지 않음(일반 호출과 나란히 보지 않음), 01의 출력 상한을 이유 없이 `max_tokens=180`, b8 「도착하는 조각」(Ch 5 조각 = 토큰)

## 바꾼 것

- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(nbkit `key_and_model_cells`, 실행일은 nbkit `RUN_DATE` 자동 = 2026-09-17). 출력 상한·`timeout`·`max_retries`는 뺌(05절 주제)
- 데이터 유지: 양식 `StudyCard`(concept·explanation·`difficulty: int = Field(ge=1, le=3, description="1부터 3까지의 난이도")`), AIMessage·SystemMessage 학습 카드 요청, 「difficulty는 반드시 9로 쓰세요」 충돌 질문, paired 형식
- 기본 경로: 준비(버전 5줄·import·키·모델) → 2절 튜플 목록 + 일반 호출(`응답 객체 종류: AIMessage`, `"난이도" in response.text` → `True`, 답 글 라벨 줄 따로) → 3절 `BaseModel`·`Field` 세 문장 + 양식 셀(출력 없음) → 4절 키워드 인자로 카드 2 만들기·7은 `ValidationError`(요청 0) → 5절 `with_structured_output(StudyCard)`(`RunnableSequence`, 요청 0) → 6절 구조화 호출(`StudyCard`·`난이도: 1`·`int`, assert 종류) → 7절 값 바꿔 보기 개념만 SystemMessage(`model_dump()`, assert 종류) → 8절 `include_raw=True`(`dict`, 키 세 개, `raw 종류: AIMessage`·JSON 글·`parsed 종류: StudyCard`·`parsing_error: None`) → 9절 Before `NoRangeCard`(설명만) + 9 질문 → `"difficulty":9`·`parsing_error: None`·`난이도가 1~3 안인가: False` → 10절 After `model_json_schema()` 규칙 비교(`'maximum': 3, 'minimum': 1`은 StudyCard만) → 같은 질문을 `raw_model`로 → `"difficulty":3`·`True`·assert
- 요청 수: 노트북 6번(모두 mini). 새 커널 실행 2번(첫 실행에서 `type(response.text).__name__`이 `TextAccessor`로 나와 `in` 확인으로 바꾸고 다시 실행) = 12 + 탐색 4(`/tmp/ch06-03/probe1.py`) = 서비스 요청 합계 16
- 실행 출력(2026-09-17 마지막 실행): `답 글 속에 난이도가 있는가: True`, 답 글 `- **난이도:** 1`, `1 validation error for StudyCard`·`less than or equal to 3`·`input_value=7`, `호출 객체 종류: RunnableSequence`, `결과 종류: StudyCard`·`난이도: 1`·`난이도의 자료형: int`, 7절 `{'concept': 'LangChain SystemMessage', …, 'difficulty': 1}`, 8절 `{"concept":"AIMessage",…,"difficulty":1}`·`parsing_error: None`, Before `"difficulty":9`·`NoRangeCard`·`False`, After `'maximum': 3, 'minimum': 1`·`"difficulty":3`·`StudyCard`·`True`. 7절 개념 이름 칸은 두 실행에서 `LangChain SystemMessage`, 설명 문장은 실행마다 달랐음(결과 읽기는 칸 이름·종류만 인용)
- 라이브러리 확인(설치 버전 소스): langchain-openai 1.6.0 `with_structured_output` 기본 `method="json_schema"`, Pydantic 클래스면 `llm | RunnableLambda(_oai_structured_outputs_parser)`(= `RunnableSequence`), `include_raw=True`면 `RunnableMap(raw=llm) | parser.with_fallbacks([parser_none], exception_key="parsing_error")` → parser 단계 오류만 `parsing_error`에 담김. `_generate`는 `response_format`이 있으면 `root_client.chat.completions.with_raw_response.parse()`. openai 3.10.0 `type_to_response_format_param` → `to_strict_json_schema(model_json_schema)` + `"strict": true`(보낸 모양: difficulty에 `"maximum": 3, "minimum": 1`, `additionalProperties: false`), `parse_chat_completion` → `_parse_content` → `model.model_validate_json(content)` → 범위 밖 값이면 호출 단계에서 `ValidationError`(로컬 `ChatCompletion`으로 확인, API 요청 없음: `1 validation error for StudyCard … input_value=9`). langchain-core 1.6.2 `AIMessage.text`는 `TextAccessor(str)`
- 탐색 실행(교재 밖, 요청 4): 범위 규칙 없는 양식 + 9 질문 → 9, ge/le 양식 + 같은 질문 → 3, 일반 호출 답은 마크다운 목록 → 노트북 Before/After와 b7 주의 메모에 「탐색 실행으로 먼저 확인한 뒤 정한 예」를 밝힘(규격 §3)
- OpenAI 문서(2026-09-17 확인): 「Structured Outputs … ensures the model will always generate responses that adhere to your supplied JSON Schema」. 숫자 `minimum`·`maximum` 지원 목록은 가져온 문서에서 찾지 못함 → 본문은 「보낸 양식에 최대 3이 들어 있었다」까지만 쓰고 「서버가 늘 지키게 하는지는 여러 번 확인하지 않음」으로 적음
- 01·02절 인계 반영: 튜플 목록·`for role, content in messages:`·라벨 줄 따로, `messages[0]` 재사용(01 6절 모양), 「모델 객체를 만들 때는 요청 0번」을 5절 양식 붙이기로 이음, `ValidationError`는 다시 정의하지 않고 「01절에서 본 값 검사 오류」, `type(값).__name__`, 답 문장은 assert하지 않고 결과 종류·범위(검사 통과한 카드라 늘 참)만 assert, temperature 0 ≠ `do_sample=False` 한 문장, 「칸(필드)」로 02 기록표 칸(딕셔너리 키)과 구분(b3), 7절 `model_dump()` = 02 기록표 한 줄 모양, 02 우편함 카드(메시지)와 03 양식 카드의 뜻 차이를 그림 읽기에 적음, b8 다음 절은 「답의 일부」(조각 안 씀)
- 규격 §2-2: `BaseModel`(뜻 → 신청서 양식 → `class StudyCard(BaseModel):`)·`Field` 설명 + Ch 2 10절 링크(노트북 3절, 본문 b3·b4). `model_dump()`·`model_json_schema()`는 처음 쓰는 자리에서 한 문장. `@` 줄 없음
- 본문 10블록 다시 씀: 이 절의 질문, 앞에서 배운 내용 표(01·02, Ch 2 05~07·10, Ch 4 04, Ch 5 07), 비유(메모와 양식 카드), 카드 양식, 양식을 붙인 호출, 원본 답·읽은 카드·읽기 오류, 용어 표 7개, 실행 예제 뒤 「문장 답과 카드 비교」·「원본 답을 함께 받을 때 오간 것」, 일부러 실패해 보기 해석, 주의 메모 8개(설명 ≠ 규칙, 3은 한 번 본 모습, 형식 ≠ 내용(같은 개념 1·3), `parsing_error`에 안 담기는 오류(소스, 미실행), `method` 기본값·다른 방식·제공자 미실행, 엄격 모드·추가 칸 거부·딕셔너리 양식 미실행, 탐색 뒤 정한 예, 기준 버전), 복습 5문제
- 뺀 것(노트북·본문): 상속 `ClosedStudyCard`·`ConfigDict(extra="forbid")`, `model_validate(…, strict=True)`의 `int_type`, JSON 주문 예제(`OrderItem`·`JSONDecodeError`·`greater_than_equal`), `method` 세 방식·TypedDict/JSON Schema 선택표. 앞의 셋은 로컬 Pydantic 기능이라 Ch 2 10절(엄격 모드)로 넘기고 b7에 「이번에 실행하지 않았습니다」로만 적음
- 그림: Mermaid 4장(03-1 카드 양식 흐름 TB, 03-2 문장 답과 카드, 03-3 원본 답과 카드 sequenceDiagram, 03-4 Before-After), 삽화 1장(03-5 메모와 양식 카드, job 8acd97c9-d366-475a-a459-49f4152831c3, 2크레딧, 1회 생성 통과, 저장 PNG 픽셀 대조 차이 0). 옛 `{{svg:03-structured-output}}`은 본문에서 뺌(파일은 `figures/`에 남기고 `before/figures/`에 사본)

## 검토

- 별도 세션 검토 1차(2026-09-17, `qa/upgrade/review-round1.md`): **accept**(하 3, C-1 반영 전제). 반영 결과: C-1 준비물 요금 문장, 03-1 노트북 3절·b4 「클래스 이름 뒤 괄호에 `BaseModel`을 적으면, 그 틀의 값 검사 기능을 물려받은 양식이 됩니다.」, 03-2 b6 끝을 세 문장으로 좁힘(규칙 `Field(ge=1, le=3)`가 있어야 9가 들어가지 못함, 모델이 3을 적은 까닭은 가리지 않음), 03-3 b7 「확장 경로(B 트랙)의 Ch 2 10절」. 결정 Q3 권고대로(Before 빨강·뺀 범위 유지). 검토자가 `StudyCard` 3번·`NoRangeCard` 2번 재현(3·9) — 본문에는 넣지 않음. 반영 방법: `mdpatch.py` → `run_section.sh … 03 --no-exec`(노트북 재실행 없음, 코드 셀·출력 그대로), 마감 게이트 `gates-after.json` G1~G7 0.
- 리뷰 묶음(반영 뒤 다시 만듦): `qa/upgrade/review-pack/`, 반영 전 묶음 `qa/upgrade/before/review-round1/review-pack/`
- 검토자가 볼 곳: (1) Before 결함을 로컬 딕셔너리에서 실제 모델(범위 규칙을 설명에만 적은 양식 → 9)로 바꾼 판단과, 오류 없이 끝난 결과를 03-4에서 빨강으로 칠한 것(Before 결함 결과 선례), (2) After의 3을 「보낸 양식에 최대 3이 들어 있었다」까지만 쓰고 서버 강제를 단정하지 않은 문장과 b7 `parsing_error`에 안 담기는 오류(소스 확인·미실행) 문장, (3) 개선 전 strict 모드·extra 금지·JSON 주문 예제를 뺀 범위(Ch 2 10절과 겹침, 강의 1h)

## 남은 것

- 기기 `/tmp/ch06-03`(탐색 스크립트·visual 사본·치환 json)는 정리 대상
- 옛 도식 `figures/03-structured-output.*`는 정리 대상 목록에만 적음(삭제하지 않음)
- 챕터 루트 `verification.md` 「실제 관찰 범위」의 03 문장(9 → 3, 로컬 `less_than_equal`)은 개선 전 기록이라 챕터 마감 때 갱신
- 강사 확인
