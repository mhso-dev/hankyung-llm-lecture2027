# 05-CoT와-ReAct의-경계 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 05, `figures/05-reasoning-boundary.*`). 수정 전 게이트는 챕터 `gates-before.json`의 05 행.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 2 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 1 | 0 |
| G5 | 6 | 0 |
| G6 | 19 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 7 | 18(준비 3) |
| 검사한 문장 | 111 | 415 |

G8: `run_section.sh` 새 커널 PASS 두 번(2026-09-17, 18 코드 셀, 두 번째 실행 출력이 교재 출력), 결과 읽기는 `mdpatch.py` 네 번 → `--no-exec`로 렌더·첨부·빌드·verify(`PASS 8 sections / 125 code cells`)·게이트 0(`gates-wip-05.json`, `--section 05`로만 실행). `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch07-05/vis/vis.cjs` 사본 + HTML 사본, 작은 글자·대비·잘림·가로 스크롤·깨진 그림·복사 불일치 0). 코드 셀 출력 칸은 셀마다 1개(요청 반복문 없음, 반복문은 요청이 끝난 값만 출력). 노트북 코드 셀 출력 텍스트 이어 붙인 SHA-256 `00b06ab6…a3bff99c03b`(두 번째 새 커널 사본 `/tmp/ch07-05/run2.ipynb`와 같음, 설명만 고친 뒤에도 같음). `runs/` 파일은 건드리지 않음(`provider-comparison-continuity.json`은 08 전용).

## 수정 전 주요 문제

- G1: 한 셀에 함수 두 개(`run`·`mention_flags`), 딕셔너리 내포식. 그 밖에 `raise RuntimeError`(A 트랙 미교육), `import json, os, time` 한 줄, `json.dumps(…, indent=2)`로 결과 전체 출력(영어 키 `text`·`usage`·`latency_s`), 딕셔너리 `.items()` 반복 한 줄 출력
- G4: 모델 셀 `init_chat_model("openai:gpt-5.4-mini", max_tokens=220)` — `temperature=0`·`reasoning_effort="none"` 없음
- G5: 제목 셀·핵심 그림·결과 읽기 셀 없음(6건)
- G6: 70자 초과 10, 영문 시작 8(「ReAct는」「`run()`은」「`mention_flags(text)`는」 등), 5문장 넘는 단락 1
- G7: Mermaid 0(옛 Excalidraw `05-reasoning-boundary.svg` 1장), 삽화 0, 설계표 없음
- 내용: (1) b3 「system에 공통 역할을, user에 현재 과제와 출력 조건을 두었습니다」는 개선된 01~04(과업 명세는 developer, user는 고객 문의만)와 다름(04 인계). (2) b4 「공개된 OpenAI 모델 지침도 GPT-5 계열에는 상세한 단계 지시를 늘리는 방식보다 목표, 성공 기준, 제약, 출력 형식을 먼저」 — 2026-09-17에 연 gpt-5.4 모델 안내 「Lower reasoning effort」는 「With reasoning effort set to `none`, prompting is important. … encourage it to "think" or outline its steps before answering.」로 반대 방향. 링크 `latest-model?model=gpt-5.5`는 설정한 모델이 아님(`latest-model` 기본 페이지는 이제 다른 모델). (3) b7 「상세한 단계별 풀이 지시는 토큰과 지연을 늘릴 수 있습니다」를 실행하지 않고 적음. (4) b6 「둘째 조건은 … 지연도 더 길었습니다」 한 번 잰 값(2026-09-09, 규격과 다른 설정). (5) 근거 줄을 입력과 대조한다고 했지만 노트북에 대조 단계가 없음(json 출력만). (6) 「비공개 내부 추론」을 말하면서 추론 토큰 수(Ch 6 06 `output_token_details`)를 보지 않음, ReAct가 아니라는 근거를 코드에서 보이지 않음(`tool_calls`). (7) 새 용어 5개 `<p>`에 흩어져 있고 일상 예·코드 모습 없음, b4 영수증 예는 노트북에 없는 계산 이야기
- 앞 절·앞 챕터와 어긋남: 01~04·Ch 6 기록 모양(한국어 키·`timed_invoke`·`make_prompt_record`)과 다른 영어 키, 대문자 `TASK`·`MENTIONS`, 옛 `run()`, 01~04 목록과 다른 메시지 배치

## 바꾼 것

- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(nbkit `key_and_model_cells`, 실행일 줄 `RUN_DAY = "2026-09-17"`). 모델 준비 결과 읽기에 Ch 6 01 「긴 추론 없이 바로 답하게 함」 한 문장. 출력 상한 없음
- 데이터·설계(04 인계 반영): 2절에서 04 목록과 글자까지 같은 `answer_messages`(= 03 `zero_messages`, 입력 134). 3절에서 출력 형식 한 글만 `evidence_format_text`(「분류, 근거, 다음 행동, 고객에게 보낼 한 문장을 한 줄씩 네 줄로 답하세요. 근거 줄에는 고객 문의와 회사 규정에서 다시 찾을 수 있는 사실만 짧게 적으세요.」)로 바꾼 `evidence_messages`, system·user 같음 `assert`. **04 틀을 쓰지 않은 이유**(노트북 2절·본문 b3 한 문장): 조건마다 바꾸는 것이 developer 글이고, 04 틀은 developer를 메시지 객체로 고정하므로 조건마다 틀을 새로 만들어야 함 → 03처럼 튜플 목록
- 근거 대조(개선 전 말만 있던 것): 7절 `for line in 답.split("\n")` + `if "근거" in line` + `break`(Ch 2 03)로 근거 줄 찾기, 결과 읽기에서 세 문장을 입력 글과 하나씩 대조. 확인 단어 표를 「고객 문의 | 과업 명세 | 근거 줄」 세 열로(01 표시를 입력 쪽까지 넓힘)
- ReAct 경계(코드로 보이기): 8절 `run_response.usage_metadata["output_token_details"]["reasoning"]`(Ch 6 06) + 응답 객체 속성 `tool_calls`(처음 쓰는 자리에서 한 문장, Ch 19 연결), `assert run_response.tool_calls == []`(도구를 알려 주지 않았으므로 매번 같은 값, 규격 §3). 답 원문 「주문번호 A-1042 확인했습니다」와 빈 도구 호출 목록을 나란히 적음
- 값 바꿔 보기: 출력 형식 한 글을 「답하기 전에 판단 과정을 단계별로 자세히 적으세요. 그다음 분류, 다음 행동, 고객에게 보낼 한 문장을 한 줄씩 세 줄로 답하세요.」로(gpt-5.4 안내의 none 권고를 실제로 해 봄), 세 조건 나란히 보기(입력·출력 토큰, 글자 수, 줄 수, 추론 토큰)
- 새로 풀어 쓴 것(처음 쓰는 자리 한두 문장): 짧은 근거(회의록 「3쪽 표 참고」), 사고의 연쇄(답안지 풀이), `tool_calls`, ReAct·관찰(전화 상담원이 주문 화면을 열어 봄). 쓰지 않은 것: f-string·`Path`·`next`·해시·`**` 풀기·글 슬라이싱·`startswith`·`join`·`strip`·`count`·`+=`·`sum`·`max`·내포식·조건 표현식·문자열 하나로 `invoke`·틀·파이프 `|`. 반복문 안 `print`는 요청이 끝난 값만 출력(출력 칸 1개)
- 요청 수: 노트북 3번(mini). 탐색 실행 4번(`/tmp/ch07-05/probe1.py`: 답만·짧은 근거·판단 과정 첫 문구 「먼저 판단 과정을 단계별로 적은 뒤」, `probe2.py`: 「자세히」를 더한 지금 문구) + 새 커널 실행 2번 × 3 = 합계 10번. 예상 비용 합계 0.01달러 미만(Ch 6 06절 mini 요금 기준)
- 실행 출력(2026-09-17, 두 번째 새 커널): 답만 `분류: 교환/파손 접수`·`주문번호 A-1042 확인했습니다.`, 짧은 근거 `분류: 교환 요청`·근거 줄 세 문장(고객 말 요약·필수 정보 첫 문장과 같은 글·고객 문의 둘째 문장과 같은 글), 기록표 `답만 | 134 | 95 | stop | 1.06`·`짧은 근거 | 162 | 130 | stop | 1.72`·더한 입력 28·출력 35, 글자·줄 `159 | 3`·`209 | 4`, 확인 단어 근거 줄 열 모두 True, 추론 토큰 0·`[]` 두 줄, 판단 과정 답 `판단 과정:` 한 줄 세 문장(「사진 확인 전에는 교환 확정이나 보상을 약속할 수 없습니다」 = 입력에 없는 덧붙인 판단)·`분류: 파손 교환 요청`·`주문번호 A-1042 확인되었으며,`, 세 조건 `134|95|159|3|0`·`162|130|209|4|0`·`152|148|246|4|0`. 보상 약속 세 답 모두 없음
- 두 번 실행에서 달라진 것(구조는 같음, 입력 토큰은 탐색·두 실행 모두 134·162·152): 첫 실행 출력 108·121·155, 글자 170·191·249, 걸린 초 2.0·1.4(이번과 순서 반대), **근거 줄이 고객 말 한 문장뿐(규정·번호 없음, 확인 단어 근거 줄 열 모두 False)**. 탐색: 답만 134/83, 짧은 근거 162/130(근거 줄 글자까지 이번과 같음), 판단 과정 첫 문구 146/124·지금 문구 152/159, 판단 과정은 네 번 모두 한 줄 → 본문 「네 번 본 모양이지만 늘 그렇다고 하지 않음」, 근거 줄 빠짐은 「보장 없음」 근거로
- 결과 읽기 작성 방식: 모델 출력에 기대는 결과 읽기 9곳 + 해석·정리를 생성기에 `[[READ_…]]` 자리 표시로 두고 두 번째 새 커널 뒤 `mdpatch.py`(`/tmp/ch07-05/reps1.json`~`reps4.json`)로 생성기·노트북에 함께 채움. 다시 실행하면 결과 읽기를 새 출력과 다시 대조해야 함
- 문서·소스 확인(2026-09-17): OpenAI Model guidance `latest-model?model=gpt-5.4` 「Lower reasoning effort」(위 인용), Reasoning models 「While reasoning tokens are not visible via the API, they still occupy space in the model's context window and are billed as output tokens.」, Reasoning best practices 「Avoid chain-of-thought prompts: Since these models perform reasoning internally, prompting them to 'think step by step' or 'explain your reasoning' is unnecessary.」, arXiv 2201.11903(Wei 외 2022, 「a series of intermediate reasoning steps」, 예시 몇 개, 산수·상식·기호 추론), arXiv 2210.03629(Yao 외 2022, reasoning traces와 task-specific actions를 번갈아, Wikipedia API). 설치한 langchain-core 1.6.2 `messages/ai.py` 170행 `tool_calls: list[ToolCall] = Field(default_factory=list)`. 뒤 챕터 연결은 개선 전 Ch 19 05(`bind_tools`·`ToolMessage`)·Ch 20 01(`ToolNode`·`tools_condition`) `_src` b1·b2 확인
- 본문 10블록 다시 씀: 학습 목표 4, 이 절의 질문, 앞에서 배운 내용 표(04·03·02·01·Ch 6 01·06·Ch 2 03) + 04 인계 단락(틀 대신 튜플 목록 이유)·개선 전 설계와 안내 문장 고친 단락, 비유(04 책상 두 개 → 연보라 답 카드·초록 근거 줄·점선 실, 회의록 「3쪽 표 참고」), 짧은 근거와 대조, 사고의 연쇄와 추론 토큰(두 공식 안내가 설정마다 다름), ReAct가 더하는 것(전화 상담원, 「확인했습니다」 ≠ 행동), 용어 표 6개, 실행 예제 뒤 「근거 줄 대조」, 실험 결과 해석(근거 줄·빠진 규정·속도 보류·도구 없음, 판단 과정 한 줄·덧붙인 판단·범위), 주의 메모 9개(탐색 뒤 정한 문구와 탐색 요청 수, 규격 §3), 복습 5문제, 참고 자료 7개
- 그림: Mermaid 4장(05-1 출력 형식만 바꾸기, 05-2 요청 한 번과 ReAct 반복, 05-3 근거 줄 대조, 05-4 세 조건 비교), 삽화 1장(05-5 근거 줄과 실, job 7c74e0d7-7628-4e52-b9ca-e4fe936a5c82, 2크레딧, 1회 생성 통과, 원본 SHA-256 `d9b231fa…f89d50c2d`, 저장 PNG 픽셀 대조 차이 0). 옛 `{{svg:05-reasoning-boundary}}`는 본문에서 뺌(파일은 `figures/`에 남기고 `before/figures/`에 사본). 빨강 0장, 파랑 0장, 회색 = ReAct 단계·앞선 실행·속도 순위. 05-1은 렌더 도장 파일 `05-1-…render.json`을 지운 뒤 다시 렌더해 새로 만듦(작업 중 이 절이 만든 파일, 내용 파일 삭제 없음)
- Ch 6·01~04 인계 반영: 옛 `TASK`·`run()`·`mention_flags()` 0건. `timed_invoke`·`make_prompt_record`·한국어 키 6개·기록표 모양·`check_words`·조건 이름 방식 01~04와 같음. 그림 색 01~04와 같음(넣은 글 초록·모델 보라·확인한 값 노랑·안 한 것 회색). 「칸」「양식」「조각」「청크」「출력 상한」「쟁반」「카드 꽂이」「우편함」「투명 봉투」 쓰지 않음(05-3 subgraph는 「큰 상자」). `BaseModel`·`@` 없음(§2-2 링크 불필요). temperature 0 ≠ `do_sample=False` 한 문장(모델 셀), 답 문장 `assert` 없음(system·user 같음, `tool_calls == []`만)

## 검토자가 볼 곳

1. 공식 안내 문장: b4 「추론 모델 안내는 단계별 지시가 필요 없다 / gpt-5.4 안내는 none이면 단계를 적게 해 보라」 두 문장과 개선 전 문장을 고친 b3 단락, 참고 자료 링크(`?model=gpt-5.4`)
2. 결론 범위: 근거 줄 「입력에 없는 사실은 찾지 못함」(이번 실행)과 앞선 실행의 규정 빠짐을 함께 적은 처리(b5 도식 읽기·b6), 판단 과정 줄의 덧붙인 판단 판정, 「근거 줄은 계산 기록이 아님」을 「증거 없음」으로 적은 문장(b4·복습 4)
3. meta 「강의 0.5h | 실습 0.5h」 유지(개선 전 값, 01~04는 1h/2h): 코드 셀 18개·문장 415개라 강의 범위 확인 필요

## 남은 것

- 기기 `/tmp/ch07-05`(탐색 스크립트·`run1.ipynb`·`run2.ipynb`·visual 사본·치환 json·삽화 원본 `illus-05-5-a.png`·`illus-05-5-check.png`)는 정리 대상
- 옛 도식 `figures/05-reasoning-boundary.*`는 정리 대상 목록에만 적음(삭제하지 않음)
- 별도 세션 검토, 강사 확인(meta 시수)
