# 07-LangChain-실습 — 챕터 끝 실습 절 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md` §7-2, `textbook/_notebook/upgrade/PLAYBOOK.md` §3, `.claude/agents/easy-upgrade-editor.md` 6.8. 기준 사례: Ch 22 `09-Middleware-실습`(`author_upgrade.py` `section_09`, 실제 API 모델 실습), Ch 5 `09-LLM-동작-원리-실습`(`author_09.py`, 검토 반영본).
새 절이라 수정 전 원본은 없습니다. 06절에서 고친 문장과 연결 파일의 수정 전 사본은 `qa/upgrade/before/06-to-07/`(`_src/06`, 06 노트북, `author_06.py`, `chapter.json`, `index.html`, 실습 폴더 `README.md`)에 두었습니다.
생성기: `qa/upgrade/author_07.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part2/ch06-langchain-start 07`. 설명만 고칠 때는 `mdpatch.py` → `--no-exec`(단, 생성기 결과 읽기 네 곳은 처음에 같은 자리 표시 글이라 `/tmp/ch06-07/readings.py`로 순서대로 채움).
먼저 읽은 것: `textbook/qa/upgrade-course-summary.md`, Ch 5 `chapter-summary.md`, 이 챕터 `qa/upgrade/handoff.md` 전체(특히 `## §06 → 실습`), `_src/06` 전체와 01~05 생성기의 코드 셀, `author_06.py`, 05 `with_fallbacks` 셀, 06-5 삽화 프롬프트·06 그림 설계표, Ch 5 `_src/09`·`author_09.py`·`09-diagnosis.md`·`09-figures.md`, Ch 22 `section_09`, Ch 7 `chapter.json`·01 `_src` b3(다음 학습 문장 확인).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 새 절 | 0 |
| G2 | 새 절 | 0 |
| G3 | 새 절 | 0 |
| G4 | 새 절 | 0 |
| G5 | 새 절 | 0 (첫 검사 1건: 모델 셀 결과 읽기 첫 단락의 `gpt-5.4-nano` 인용이 그 셀 출력에 없음 → 「nano 모델」로) |
| G6 | 새 절 | 0 (첫 검사 3건: 70자 초과 → 문장 나눔) |
| G7 | 새 절 | 0 |
| 코드 셀 | 새 절 | 19 (준비 3, 함수 정의 셀 6개, 양식 클래스 셀 1개, 심화 셀 없음) |
| 검사한 문장 | 새 절 | 370 (`gates-wip-07.json`) |
| 모델 호출 | 새 절 | 노트북 한 번에 답을 받는 요청 4번(mini 2·nano 2) + 답 없이 시간 초과로 끝나는 시도 2번 |

- 새 커널 실행 PASS 세 번(`PASS 07-LangChain-실습.ipynb: 19 cells`). 첫 실행(A)은 7·8번 셀이 호출 객체 종류를 반복문 앞에서 출력해 노트북 출력이 셀마다 두 개(stream 두 칸)로 나뉨 → 그 줄을 반복문 뒤로 옮김(04·06 인계). 두 번째(B, 02:32:22)와 세 번째(C, 02:32:49 UTC)는 같은 코드(`code_sha256` `83ec2cfa…`)로, 셀마다 출력 한 칸·출력 줄 모양이 같고(숫자·설명 문장을 가린 비교에서 19셀 모두 같음) 토큰 수·걸린 초·설명 문장만 달랐음. 교재 출력은 C(`outputs_sha256` `cc2a57d9…`).
- 탐색(기기 셸): `/tmp/ch06-07/probe1.py`(조립 모양 확인, 답 4·시간 초과 2), `probe2.py`(같은 첫 질문을 양식 없이 일반 호출 → 입력 61·출력 74토큰, b7). 서비스 요청 합계: 답을 받은 요청 17번(노트북 A·B·C 12 + probe 5), 시간 초과 시도 8번. 요금표로 어림한 합계 약 0.006달러.
- `verify.py --chapter` `PASS 7 sections / 130 code cells (max 16 lines)`. `visual.cjs` 06·07·index × 1280·390px 6건 PASS(`/tmp/ch06-07/vis/vis.cjs`, 06절 사본 복사, 공용 도구는 고치지 않음). 빌드 HTML: SVG 3·삽화 1, 남은 `{{` 0, 챕터 `index.html` 「절 7개」와 07 링크, 06 HTML 아래 이동 링크가 07을 가리킴. 06절 `--no-exec` 다시 검사 G1~G7 0(문장 452).
- 기기 루트 여유 639MB(시작 644MB). `/tmp`에 가상환경을 만들지 않음(`$ROOT/.cache/vm/venv-ch06-langchain-start`).

## 주제와 구성

- 주제: 「학습 카드 요청에 폴백과 비용 기록 붙이기」. 초급 학습자에게 LangChain 용어 카드를 만들어 주는 작은 도우미. 기본 경로가 늦으면 대체 경로가 카드를 만들고, 요청마다 기록 한 줄을 남김
- 조립한 핵심 네 개: 03절 구조화 출력(`StudyCard`·`with_structured_output(…, include_raw=True)`), 05절 타임아웃과 폴백(`timeout`·`max_retries=0`·`with_fallbacks([backup_path], exceptions_to_handle=(ModelTimeoutError,))`), 06절 비용 기록(요금표·`estimate_cost`·`timed_invoke`), 05절 응답한 모델 `model_name`으로 요금표 고르기(`estimate_answer_cost`). 01·02절(`init_chat_model`, 튜플 목록, `usage_metadata`, nano, 기록표 한 줄)은 보조. 04절 스트리밍과 05절 `with_retry()`는 쓰지 않는다고 본문 b3·노트북 2번에 적음
- 바꾸는 값: `build_card_path(primary_timeout)`의 인자 하나(실행 1 `30` → 실행 2 `0.001`). 질문·양식·대체 경로(nano, 30초, 재시도 0)·기록 함수는 같음
- 질문: 03절 모양 「LangChain의 with_fallbacks를 학습 카드로 만드세요. 개념 이름, 한 문장 설명, 1~3 난이도를 적으세요.」, 같은 모양의 `usage_metadata`. system 03절 「초급 학습자를 위한 학습 카드를 만듭니다.」
- 노트북 순서(PLAYBOOK §3): 준비(버전·import·키·모델) → 주제 + 준비 모델 설정(None) → 재료(양식, 질문, 요금표) → 비용 함수 2(`estimate_cost` 06과 같은 코드, `estimate_answer_cost`) → 기록 장치 3(`timed_invoke` 06과 같은 코드, `make_card_record` 키 8개, `print_report` Ch 4·5) → 조립(대체 경로 셀, `build_card_path` 줄마다 절 주석) → 실행 1 → 실행 2 → 비교 표 → 응답한 모델을 적지 않았다면(mini 요금표로 다시 계산) → 정리 3줄
- 실행 1(C): `호출 객체 종류: RunnableWithFallbacks`, 두 기록 `gpt-5.4-mini-2026-03-17`, 190/0/64토큰·1.41초·0.0004305달러, 188/0/57·1.15·0.0003975, 난이도 2·2, 합 0.000828
- 실행 2(C): 두 기록 `gpt-5.4-nano-2026-03-17`, 190/0/70·0.9·0.0001255, 188/0/59·1.1·0.00011135, 합 0.000237. mini 요금표로 다시 계산한 합 0.000864(약 3.6배)
- 앞선 실행 값(본문에 적은 것): B의 걸린 초 실행 1 1.06·0.98, 실행 2 0.86·1.22(b6·복습 5). A는 코드가 달라 인용하지 않음
- 설계 과정: 실행 2의 값은 05절 5절에서 시간 초과를 실제로 낸 0.001초로 정하고, probe1에서 두 질문 모두 nano가 답하는 것을 확인한 뒤 노트북에 넣음(b7 「흐름을 보여 주려고 정한 예」). 질문을 둘로 한 것은 기록표에 줄이 여럿 있어야 합계와 요금표 비교가 보이기 때문(답을 받는 요청 4번, 규격 §7-2의 3~5번 안). 기록에 캐시 입력 키를 넣은 것은 10번 셀에서 사용량 딕셔너리를 다시 담을 때 캐시 입력까지 같게 계산하려는 것(네 요청 모두 0)
- 사다리: L1~L6 범위(L5 `BaseModel` 필드만, 03절에서 §2-2 링크 완료라 다시 풀지 않고 「03절과 같은 코드」로 적음). 셀 하나에 함수 하나, 함수 본문 최대 8문장(`estimate_answer_cost`), 코드 셀 최대 14줄(`make_card_record`). 두 겹 호출 없음, 내포식·조건 표현식·f-string·`raise`·`+=`·`lambda` 없음. 함수 안에서 바깥 이름(`nano_prices`·`mini_prices`·`backup_path`)을 읽는다고 설명 셀에 적음(05·06절 방식). `upgrade_allow` 없음
- 반복문 안 출력 금지: 요청을 기다리는 반복문 안에서 출력하면 노트북 출력이 여러 칸으로 나뉘어(첫 실행 A에서 확인) 요청이 끝난 뒤 한꺼번에 출력

## 앞 절에서 가져온 이름과 연속성 판단

- 같은 코드로 가져온 것: 03절 `StudyCard`, 06절 요금표 두 딕셔너리·`pricing_date`·`estimate_cost`·`timed_invoke`, Ch 4 06·Ch 5 09 `print_report`, nbkit 키·모델 셀(06과 같은 설명 셀)
- 가져온 값·모양: 03절 system 지시와 질문 모양, 05절 `timeout=0.001`·`ModelTimeoutError`·`with_fallbacks(… exceptions_to_handle=(…,))`·원소 하나 튜플·`assert "nano" in …`, 05절 3절 두 값 None, 06절 `max_retries=0`(요청 한 번 = 기록 한 줄), 02절 nano, 04·06 인계 「반복문 안 출력 칸 나뉨」
- 새 이름: `system_message`·`questions`·`estimate_answer_cost`·`make_card_record`·`backup_model`·`backup_path`·`build_card_path`·`primary_model`·`primary_path`·`card_path`·`records_1`·`records_2`·`runs`·`mini_price_total`·`answered_price_total`·`token_usage`·`wrong_cost`. 06 `make_cost_record`와 이름을 섞지 않음(06 인계), 02 `make_record`와도 다름
- 용어: 새 용어 0개. 「응답한 모델」(05)·「예상 비용」「캐시 입력」(06)·「칸(필드)」「원본 답(raw)」(03)·「시도」(05, 요청 한 번)·「기록표/기록 한 줄」(02·06)을 같은 뜻으로 씀. 딕셔너리 키는 「키」(04 인계, 03 「칸」과 구분). 「조각」·「청크」 안 씀
- 06절 「다음 학습」: 06 b8을 07 실습 안내 + 「10절에서 저장한 파일은 07절이 쓰지 않고, Ch 7의 08절이 읽습니다」로 바꾸고, 기존 Ch 7 08 세 문장은 07 b8로 옮김. 06 노트북 정리 끝 문장·`author_06.py` 같은 문장도 바꿈(`mdpatch.py`, 재실행 없음, 06 게이트 0 다시 확인)
- 뒤 챕터 연결(07 b8·노트북 정리): Ch 7 01 문장은 Ch 7 01 `_src` b3(「Ch 6의 `init_chat_model("openai:gpt-5.4-mini")`, `invoke()`, `AIMessage.text`, `AIMessage.usage_metadata`를 사용합니다」, 개선 전)과 Ch 7 `chapter.json` 01 제목 「역할별 메시지와 제약」에서 확인. Ch 7 08 문장은 06절 작업자가 확인한 원문 그대로. 이 실습은 파일을 쓰지 않아 Ch 7·8 사슬(06 인계)에 영향 없음(`runs/provider-comparison-continuity.json` 수정 시각 02:04, 06 실행 그대로)

## 사실 주장 확인

- 노트북 출력으로 확인: 위 실행 1·2·비교 값, 버전 다섯 줄, 준비 모델 `timeout: None`·`max_retries: None`, 두 호출 객체 종류, 네 요청 캐시 입력 0
- 계산으로 확인(본문·결과 읽기): `(190 × 0.75 + 64 × 4.50) ÷ 1000000` = 0.0004305, `(190 × 0.20 + 70 × 1.25) ÷ 1000000` = 0.0001255, 복습 2 `(188 × 0.75 + 57 × 4.50)` = 397.5 → 0.0003975(출력과 같음), 0.000828 ÷ 0.000237 ≈ 3.5, 0.000864 ÷ 0.000237 ≈ 3.6
- 기기 셸에서만 확인했다고 적은 것(b6·b7): 같은 첫 질문을 양식 없이 보낸 입력 61토큰(probe2, 한 번), 0.001초에서 두 질문 모두 nano가 답함(probe1)
- 소스로 확인: langchain-core 1.6.2 `runnables/fallbacks.py` 93~96행 설명(「Any exception that is not a subclass of these exceptions will be raised immediately.」)과 198~204행 `except self.exceptions_to_handle`·나머지 `raise`
- 실행하지 않았다고 적은 것: 시간 초과 시도의 서버 도달·과금, 실패 시도와 대체 요청 시간 분리, 모델 이름 오타·양식 검사 오류가 난 조립, 다른 대체 모델, 카드 품질 비교, 다른 버전·Windows·macOS
- 참고 자료: 03·05·06절 작업에서 2026-09-17에 확인한 문서 4개 + 라이선스(이 절에서 다시 열지 않았다고 b10에 적음)

## 그림

- Mermaid 3장(PNG 직접 확인): 07-1 조립도(flowchart TB 7노드, viewBox 430), 07-2 실행 1 순서(sequenceDiagram 참가자 셋 `messageAlign: left`, 메모는 결과를 받은 직후·반복 뒤, 703), 07-3 두 실행 비교(LR 두 칸 + 칸 안 TB, 처음 두 칸이 세로로 쌓이고 실행 2가 위에 와서 `R1 ~~~ R2`를 더함, 350 → 726)
- 삽화 1장: 07-4 갈림길 카드와 꼬리표(03-5 양식 카드·05-5 레일과 모래시계·06-5 저울·동전·초시계를 한 장면에). nano_banana_pro 16:9 2k, 1회 생성, 2크레딧(생성 전 잔액 2868). 채택 job `3ae8b10f-fc06-4722-b32f-bc03771fb542`. 기기 셸 `curl` 원본(SHA-256 앞 16자 `33230a530531cef7`) → 1100×614 저장, 같은 폭으로 줄인 원본과 픽셀 차이 0(bbox None). 그림 읽기·검수 메모는 저장 파일을 보고 씀(문이 길 끝 옆에 선 점, 동전 네 닢 안팎)
- 색(§5-3): 재료·넣은 값 초록, 정의한 함수 파랑, 실행한 두 모델 보라, 기록·출력 값 노랑, 출력에 나오지 않은 기본 경로 시간 초과 회색(폴백이 받아 넘긴 오류라 빨강 아님), 빨강 0장. 근거는 `07-figures.md`

## 바꾼 다른 파일

- `chapter.json` sections 끝에 `07-LangChain-실습`(「LangChain 실습: 학습 카드 요청에 폴백과 비용 기록 붙이기」, experiment). 챕터 시수 「총 16h · 강의 6h · 실습 10h」는 바꾸지 않음(07 30분은 실습 10h 안, 규격 §7-2). 챕터 `index.html`은 빌드가 다시 만듦(「절 7개」)
- `_src/06-토큰-비용-지연-비교.html` b8, 06 노트북 정리 끝 문장, `author_06.py` 같은 문장(`mdpatch.py`)
- `labs/part2/ch06-langchain-start/README.md`: 「여섯 노트북은」→「일곱 노트북은」, 07 한 줄(파일을 만들거나 고치지 않음). 같은 README 첫 단락의 「Anthropic과 Google 키가 없으면 관련 비교 행은 `skipped`」는 개선된 02·06과 맞지 않지만 이번 범위 밖이라 그대로 둠(챕터 검토 때 확인)
- `집필점검표.md` 품질 개선 표에 07 행
- 옛 생성기 `labs/part2/ch06-langchain-start/_make_notebooks.py`는 실행하지 않음(01절 때 넣은 `raise SystemExit` 그대로, 챕터 마감 때 옮김)
- 루트 `textbook/qa/upgrade-progress.md`는 챕터 밖이라 고치지 않음(Ch 06 행이 아직 「대기」)

## 검토에서 볼 곳

- 결론 범위(b6 마지막 두 단락, 노트북 9·10번 결과 읽기, 복습 4·5): 걸린 초·비용 차이를 두 질문·한 번 실행 밖으로 넓히지 않았는지, 「요금표는 응답한 모델로 고른다」가 관찰이 아니라 기록 원칙으로 읽히는지
- 조립 모양: 05절이 모델 객체에 붙인 `with_fallbacks()`를 구조화 호출 객체에 붙인 것이 새 API로 읽히지 않는지(노트북 6번 설명·b4 마지막 단락), 07-3 회색 상자(출력에 없는 시간 초과) 색 판단
- 삽화 07-4 비유(주황 꼬리표 = 응답한 모델)가 그림만으로 읽히는지, 07-2 메모 시점(결과를 받은 직후 기록 / 반복 뒤 출력)

## 검토

- 별도 세션 검토 1차(2026-09-17, `qa/upgrade/review-round1.md`): **accept-with-fixes**(상 0·중 1·하 4). 반영 결과(같은 날 마감 세션): 07-1(중) 복습 4 해설을 「같은 토큰 수라도 요금표가 달라 예상 비용이 달라졌습니다」 + 「출력 토큰 수와 걸린 초도 달랐지만, 06절에서 같은 모델도 요청마다 달랐으므로 폴백 때문이라고 말하지 않습니다」로 고치고 입력 토큰 수 문장 삭제, 07-2 노트북 6번 설명·b4에 05절 `RunnableLambda(ask_current_model)`의 `with_retry()`와 잇는 두 문장, 07-3 [1] 「카드 양식과 질문 두 개」(같은 셀 그림 alt의 「초록 상자 요금표」도 07-1 mmd에 없어 고침), 07-4 복습 3 해설(05절은 좁은 목록에서 오타가 드러남, 넓히면 가려질 수 있음은 소스로 본 동작), 07-5 [11] 「키」·[39] 「원소는 (실행 이름, 기록 목록) 튜플」. 결정 Q7 권고대로(결론 범위·07-3 회색·삽화 꼬리표 유지). 고친 문장은 모두 설명 셀·본문이라 생성기에도 있었고, 치환 전 생성기·노트북·`_src` 위치별 개수를 확인함. 반영 방법: `run_section.sh … 07 --no-exec`, 재실행 없음, `gates-after.json` G1~G7 0.
- 리뷰 묶음(반영 뒤 다시 만듦): `qa/upgrade/review-pack/07-LangChain-실습.md`, 반영 전 `qa/upgrade/before/review-round1/review-pack/`

## 남은 것

- 리뷰 묶음: `qa/upgrade/review-pack/07-LangChain-실습.md`(06도 다시 만듦)
- 정리 대상(삭제하지 않고 목록만): `/tmp/ch06-07`(probe1·2.py, runA·B·C.ipynb 사본, readings.py, reps1·reps06.json, 삽화 원본 `illus-orig.png`, visual 사본과 화면 캡처), `qa/upgrade/before/06-to-07/`(06 수정 전 사본), `qa/upgrade/gates-wip-07.json`
- 챕터 검토(별도 세션)와 `chapter-summary.md`는 다음 단계(handoff `## 실습 → 챕터 검토`)
