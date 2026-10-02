# 04-스트리밍과-content-blocks — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 04, `figures/04-streaming.*`). 챕터 전체 수정 전 게이트는 01절 때 남긴 `gates-before.json`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 2 | 0 |
| G2 | 2 | 0 |
| G3 | 0 | 0 |
| G4 | 1 | 0 |
| G5 | 11 | 0 |
| G6 | 26 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 7 | 19(준비 3) |
| 검사한 문장 | 154 | 417 |

G8: `run_section.sh` 새 커널 PASS(2026-09-17, 19 코드 셀, `outputs_sha256` `95515df1…`), `verify.py --chapter` PASS(6절 88 코드 셀), `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch06-04/vis/` 사본으로 실행, 작은 글자·대비·잘림·SVG 경계·가로 스크롤·깨진 그림·복사 0).

## 수정 전 주요 문제

- G1·G2: 목록 내포식 `[len(chunk.content_blocks) for …]`, `next((c.content_blocks[0] for c in chunks if …), None)`(제너레이터 식·한 글자 변수 `c`), `bool(combined.text.strip())`(두 겹 호출)
- G4: 모델 셀에 `temperature=0` 없음(`max_tokens=180, timeout=30, max_retries=1`)
- G5: 제목 셀·핵심 그림·결과 읽기 셀 없음(11건). G6: 영문 시작 18, 70자 초과 6, 5문장 넘는 단락 1. G7: Mermaid 0(옛 Excalidraw 1장), 삽화 0, 설계표 없음
- 사다리·앞 내용 밖: 키 셀 `raise FileNotFoundError`/`RuntimeError`, `print(…, end="", flush=True)`, 내장 `sum`·`bool`, 목록에 system 없는 user 한 줄(01~03은 system+user)
- 앞 절과 어긋남(인계 §03 → §04): b3 「02절에서 `content_blocks`로 표준화된 내용 블록을 확인했습니다」 — 개선된 02는 `content_blocks`를 뺐으므로 사실과 다름. 「첫 절의 모델 초기화에서 timeout·max_retries를 적었다」류 옛 01 전제. `AIMessageChunk`를 「조각」「조각 수」로 부름(Ch 5 조각 = 토큰)
- 내용: b4의 JSON 중간 검증·실시간 자막·이미지 블록 표·`completed`/`partial` 기록, `stream_usage=True`로 사용량 수집 요청 등 대부분 노트북에서 실행하지 않은 동작. 사용량 누락을 가르친다면서 노트북은 사용량이 있는 경우만 실행(`결합 메시지 usage 있음: True`). 청크 수 20·블록 수 16을 해석 없이 인용
- 옛 HTML은 `flush=True` 출력이 청크마다 따로 저장되어 출력 칸이 21개로 나뉘어 있었음

## 바꾼 것

- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(nbkit `key_and_model_cells`, 실행일 nbkit `RUN_DATE` = 2026-09-17). `timeout`·`max_retries`는 뺌(05절 주제), 출력 상한은 값 바꿔 보기 2에서만 01절 값 12로
- 데이터 유지: user 질문 「LangChain 스트리밍을 열두 단어 이내로 설명하세요.」, stream과 invoke 비교, experiment 형식. system은 02절 「한 문장의 한국어로 답하세요.」를 다시 씀
- 기본 경로: 준비(버전 5줄·import·키·모델) → 2 튜플 목록 → 3 `invoke` 기준 답(`AIMessage`·출력 토큰·끝난 이유) → 4 `answer_stream = model.stream(messages)`(`generator`, 요청 0, `stream_usage 설정: True`) → 5 `for`로 꺼내 `chunks`·`shown_text`(경계 `|`)·`받은 청크 수: 18` → 같은 객체 다시 꺼내기 `0`(assert) → 6 `enumerate`로 글자 없는 청크 네 개(0·15 `stop`·16 사용량·17)·`글자가 든 청크 수: 14` → 7 `+`로 합치기(`AIMessageChunk`·17토큰·`stop`·invoke 답과 같은가 `False`) → 글만 이어 붙인 `str`과 비교(`True`, assert) → 8 `content`·`content_blocks`(글 블록 하나, 0번 `[]`) → 9 값 바꿔 보기 1 `stream(messages, stream_usage=False)` → 17청크·`사용량: None`·`if/else`로 기록 값 `None`(assert) → 10 값 바꿔 보기 2 `max_tokens=12` 모델 객체 → 스트리밍 `|토|큰|을| 실|시간|으로| 순|차| 전||||` → 13청크·12토큰·`length` → 11 실험 결과 해석 표(기본 18/17/stop, 사용량 끔 17/None/stop, 출력 상한 12 13/12/length)
- 요청 수: 노트북 4번(모두 mini). 새 커널 실행 2번 = 8 + 탐색 4(`/tmp/ch06-04/probe1·2·3.py`: LangChain stream 1, stream_usage False·max_tokens 12 2, openai SDK 원시 스트림 1) = 서비스 요청 합계 12
- 새 커널 실행 2번의 이유: 첫 실행에서 `print(chunk.text, end="|", flush=True)` 출력이 노트북에 21개로 나뉘어 저장되고 `render.py`가 칸마다 「출력:」을 붙임 → 공용 도구를 고치지 않고 `shown_text`에 모아 한 번에 출력하도록 코드를 바꿔 다시 실행. 이 과정은 b7에 적음. 두 실행 사이에 답 문장이 바뀌어(청크 20 → 18, 토큰 19 → 17) 결과 읽기·본문·그림 라벨·캡션을 마지막 출력으로 모두 다시 맞춤(탐색 실행에서는 23·22)
- 라이브러리 확인(설치 버전 소스): langchain-core 1.6.2 `BaseChatModel.stream`은 `yield`가 든 제너레이터 함수 → 호출 줄에서는 본문이 실행되지 않고 첫 `next`에서 `_stream`(요청) 실행. 반복이 끝나면 `chunk_position="last"`인 빈 `AIMessageChunk`를 한 번 더 `yield`(816~830행), 받는 도중 예외는 `raise`로 다시 냄. `AIMessageChunk.__add__` → `add_ai_message_chunks`가 content·response_metadata·usage_metadata(`add_usage`)를 합침. `BaseMessage.text`는 type text 블록만 모음, `content_blocks`는 문자열 content를 `{"type": "text"}` 블록으로, 빈 문자열은 빈 목록. `KNOWN_BLOCK_TYPES`에 reasoning·image·tool_call 등. langchain-openai 1.6.0 `stream_usage`는 `openai_api_base`·`OPENAI_BASE_URL`·custom client가 없으면 `True`로 켜짐(1332~1351행), `_stream(stream_usage=…)` 인자로 호출마다 바꿈 → `stream_options={"include_usage": …}`
- 탐색 실행으로 확인: openai 3.10.0 원시 스트림 첫 청크는 `role: assistant`·`content: ''`, 사용량 청크는 choices 없이 따로 옴(04-2 서버 쪽 화살표 근거). temperature 0에서도 실행마다 답 문장이 달랐음(탐색 두 번은 「LangChain 스트리밍은…」, 새 커널 두 번은 「토큰을…」)
- 온라인 문서(2026-09-17 확인): LangChain Models의 stream·청크 합산, Messages의 content_blocks, ChatOpenAI 문서 「set `stream_usage=True`」 안내 → 설치한 판은 기본으로 켜져 있어 b7에 차이를 적음, Python 3.12 glossary generator
- 01·02·03절 인계 반영: 튜플 목록·라벨 줄 따로, 「모델 객체를 만들 때는 요청 0번」·03 「양식 붙이기 요청 0번」을 4절 `stream()` 줄 요청 0번으로 이음, 01 호출 메서드 표 「도착하는 대로 받는 답의 일부」·「04절에서 실행」 실행, 01 `usage_metadata`·`finish_reason`·출력 상한 12·`length` 재사용(다시 정의 안 함), 02 기록표의 모르는 값 `None`을 9절에 이음, 비교 결과를 변수에 담아 출력(02), 답 문장은 assert하지 않고 제너레이터 빈 것·글 같음·None만 assert, temperature 0 ≠ `do_sample=False` 한 문장, **청크는 「조각」으로 부르지 않음**(b3에서 Ch 5 조각 = 토큰과 구분), 03 「칸(필드)」은 쓰지 않고 딕셔너리 「키」로(그림 영역만 03처럼 「칸」), b3의 「02절에서 content_blocks 확인」 문장을 없애고 「이 절에서 처음 씀」으로 고침
- 규격 §2-2: `@` 줄·`BaseModel` 없음. Python 새 모양은 모두 배운 것(`enumerate` Ch 2 02, 슬라이싱 Ch 2 03, `get` 01, `if/else`). `print`의 `end`·`flush`는 코드에서 뺌
- 본문 10블록 다시 씀: 이 절의 질문, 앞에서 배운 내용 표(01·01 메서드 표·02·03, Ch 2 02·03, Ch 5 01·04), 비유(구슬 꿰기), stream 줄과 요청 줄(제너레이터 세 문장), 청크와 청크 더하기, content·text·content_blocks, 용어 표 6개, 실행 예제 뒤 「청크가 도착한 순서」·「글만 이어 붙인 글과 합친 메시지」, 실험 결과 해석(None ≠ 0, 오류 없는 끊김, 청크 수 ≠ 속도, 요청마다 다른 문장), 주의 메모 10개, 복습 6문제, 참고 자료 5개
- 뺀 것: b4 상황 표(설문 JSON·자막·이미지 블록·completed/partial), 「화면 갱신 횟수 제한」 메모, 청크 20·블록 16 해석. 실행하지 않은 동작은 b7에 「이번에 실행하지 않았습니다」로만(연결 끊김, 구조화 호출 스트리밍, 다른 블록 종류·제공자, 다른 주소의 stream_usage 기본값, 첫 청크 시간)
- 그림: Mermaid 4장(04-1 스트리밍 흐름 TB, 04-2 청크 도착 순서 sequenceDiagram, 04-3 이어 붙인 글과 합친 메시지, 04-4 세 번 비교), 삽화 1장(04-5 구슬 꿰기, job 5a0f07fb-9684-4e97-9a3c-de45ca56da94, 2크레딧, 1회 생성 통과, 저장 PNG 픽셀 대조 차이 0). 옛 `{{svg:04-streaming}}`은 본문에서 뺌(파일은 `figures/`에 남기고 `before/figures/`에 사본). 클라우드 `/mnt/user-data/outputs`가 입출력 오류라 기기에서 job 결과를 직접 받아 줄였고, 원본 SHA-256 앞 16자가 클라우드에서 받은 원본과 같음을 확인

## 검토

- 별도 세션 검토 1차(2026-09-17, `qa/upgrade/review-round1.md`): **accept**(하 2, 공통 C-1·C-5 반영 전제). 반영 결과: C-1 준비물 요금 문장, C-5 준비물 「강의와 실습 범위」 단락과 b5 셋째 단락(강의 3~7절, 8~11절은 실습 시간, **강사 확인 대상**), 04-1 도식 읽기 앞 새 단락(노트북 출력만으로는 청크 출처를 모름, 서버 쪽 순서는 원시 스트림 탐색 실행 결과), 04-2 [25] 「다시 실행하면 두 답이 같게 나와 `True`일 수도 있습니다.」 결정 Q4 권고대로(모아 출력·04-2 그림 유지). 반영 방법: `mdpatch.py` → `run_section.sh … 04 --no-exec`(노트북 재실행 없음, 코드 셀·출력 그대로), 마감 게이트 `gates-after.json` G1~G7 0.
- 리뷰 묶음(반영 뒤 다시 만듦): `qa/upgrade/review-pack/`, 반영 전 묶음 `qa/upgrade/before/review-round1/review-pack/`
- 검토자가 볼 곳: (1) 04-2의 서버 쪽 화살표(0번 빈 글·사용량 청크 따로)는 탐색 실행 원시 스트림, 마지막 빈 청크는 langchain-core 소스 근거이고 노트북은 LangChain 청크만 출력한 점, (2) `flush=True` 실시간 출력을 코드에서 빼고 `shown_text`로 모아 출력한 판단과 b7 설명(학생이 「글이 조금씩 늘어나는 모습」을 노트북에서 직접 보지 않음), (3) b6 마지막 단락 「요청마다 다른 문장」 해석과, 7절 `3절 invoke 답과 글이 같은가`가 재실행마다 True/False가 바뀔 수 있는 출력인 점(assert 안 함)

## 남은 것

- 기기 `/tmp/ch06-04`(탐색 스크립트·visual 사본·치환 json·삽화 원본)는 정리 대상
- 옛 도식 `figures/04-streaming.*`는 정리 대상 목록에만 적음(삭제하지 않음)
- 챕터 루트 `verification.md`·`집필점검표.md` 위쪽 04 행(2026-09-09 기록, 「청크 결합」)은 개선 전 기록이라 챕터 마감 때 갱신
- 강사 확인
