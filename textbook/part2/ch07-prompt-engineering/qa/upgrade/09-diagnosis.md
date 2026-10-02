# 09-프롬프트-엔지니어링-실습 — 챕터 끝 실습 절 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md` §7-2, `textbook/_notebook/upgrade/PLAYBOOK.md` §3, `.claude/agents/easy-upgrade-editor.md` 6.8. 기준 사례: Ch 22 `09-Middleware-실습`, Ch 6 `07-LangChain-실습`(`author_07.py`, 검토 반영본, 같은 Part 앞 챕터 실습).
새 절이라 수정 전 원본은 없습니다. 08절에서 고친 문장과 연결 파일의 수정 전 사본은 `qa/upgrade/before/08-to-09/`(`_src/08`, 빌드된 08 HTML `….built.html`, 08 노트북, `author_08.py`, `chapter.json`, `index.html`, 실습 폴더 `README.md`)에 두었습니다.
생성기: `qa/upgrade/author_09.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part2/ch07-prompt-engineering 09`. 설명만 고칠 때는 `mdpatch.py` → `--no-exec`(생성기에는 채운 결과 읽기가 남아 있음, `/tmp/ch07-09/reps1.py`·`reps2.json`·`reps3.json`).
먼저 읽은 것: `textbook/qa/upgrade-course-summary.md`, Ch 6 `chapter-summary.md`, 이 챕터 `qa/upgrade/handoff.md` 전체(특히 `## §08 → 실습`), `_src/08` 전체, `author_06.py`·`author_07.py`·`author_08.py` 코드 셀, `08-figures.md`·08-5·Ch 6 07-4 삽화 프롬프트, Ch 22 `_src/09`, Ch 6 `_src/07`·`author_07.py`·`07-figures.md`·`07-diagnosis.md`, `집필점검표.md`, `chapter.json`, 공용 `nbkit.py`·`run_section.sh`·`mdpatch.py`·`upgrade_gates.py`·`builder.py` 색인 부분.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 새 절 | 0 |
| G2 | 새 절 | 0 |
| G3 | 새 절 | 0 |
| G4 | 새 절 | 0 |
| G5 | 새 절 | 0 (첫 검사: 자리 표시 5건 → 채움, 그 뒤 2건: 결과 읽기 첫 단락 `v1_version`·`v2_version` 인용이 출력에 없음 → 「실행 1·2 버전 딕셔너리」) |
| G6 | 새 절 | 0 (첫 검사 2건: 70자 초과 → 문장 나눔) |
| G7 | 새 절 | 0 (첫 검사 1건: 설계표 없음 → `09-figures.md`) |
| 코드 셀 | 새 절 | 25 (준비 3: 설치·import·키, 함수 정의 셀 10개, 심화 셀 없음) |
| 검사한 문장 | 새 절 | 381 (`gates-wip-09.json`) |
| 모델 호출 | 새 절 | 노트북 한 번에 4번(`gpt-5.4-mini`, 실행 1·2에 2번씩) |

- 새 커널 실행 PASS 두 번(`PASS 09-프롬프트-엔지니어링-실습.ipynb: 25 cells`). 첫 실행 A(2026-09-17 07:41 UTC)와 두 번째 B(07:42 UTC)는 같은 코드, 셀마다 출력 한 칸, 출력 줄 모양 같음. 달라진 것은 출력 토큰 수·걸린 초·답 문장뿐(입력 토큰 수·세 층 검사 결과·category 값은 같음). 교재 출력은 B(코드+출력 해시 앞 16자 `7524fc8fe380ee1d`, A 사본 `/tmp/ch07-09/run1.ipynb` `f8aaabc3979c02ab`). 결과 읽기는 B를 보고 `mdpatch.py`로 채움(G5 첫 단락 인용 대조 + 모든 결과 읽기 인용을 스크립트로 대조: 출력에 없는 인용은 설명 단락의 코드 이름뿐)
- 탐색(기기 셸 `/tmp/ch07-09/probe1.py`, 네 요청 × 세 번 = 12번): 조립 모양 확인과 「기타」 흐름 확인. `make_rules_format("배송, 교환, 환불")`이 07절 `rules_format_text`와 같음(`same as 07: True`). 분류를 출력한 두 번 모두 v1 글꼴 = 배송, v2 글꼴 = 기타, 텀블러 = 교환. 입력 191·169·193·171은 세 번 모두 같음. 출력 토큰은 v1 텀블러 100·89, v1 글꼴 125·85, v2 텀블러 100·99, v2 글꼴 90·69(셋째 탐색은 토큰 줄 미출력)
- 서비스 요청 합계 20번(탐색 12 + 노트북 A·B 8), 모두 mini. 입력 약 180·출력 약 100토큰으로 어림하면 약 0.012달러
- `verify.py --chapter` `PASS 9 sections / 200 code cells (max 15 lines)`. `visual.cjs` 08·09·index × 1280·390px 6건 PASS(`/tmp/ch07-09/vis/vis.cjs`, HTML 사본 `/tmp/ch07-09/html`, 공용 도구는 고치지 않음). 빌드 09 HTML: SVG 3·삽화 JPEG 1, 남은 `{{` 0, 출력 칸 16. 챕터 `index.html` 「절 9개」, 08 HTML 아래 이동 링크가 09를 가리킴
- 08절 `--no-exec` 다시 검사 G1~G7 0, 08 노트북 코드+출력 해시 앞 16자 `14593bfd5ee03ad2`가 고치기 전과 같음(재실행 없음)
- runs 파일은 열지 않음: 수정 시각만 확인(`provider-comparison-continuity.json` 02:04:33, `prompt-ab-continuity.json` 07:07:01, 사본 `continuity/20260917T070701/` 07:07:01, `prompt-ab-v1.json` 2026-09-09) — 08 두 번째 새 커널 뒤 그대로. 작업 시작 때 한 번 `sha256sum`으로 세 파일 지문을 대조했고(읽기만, handoff 값과 같음) 그 뒤로는 열지 않음
- 기기 루트 여유 583MB(시작 587MB). 가상환경은 `$ROOT/.cache/vm/venv-ch07-prompt-engineering`(새로 만들지 않음)

## 주제와 구성

- 주제: 「고객 문의 분류 틀에 JSON 검사와 버전 기록 붙이기」. 상담 창구 문의를 JSON으로 분류하는 작은 분류기. 07절 11절에서 글꼴 문의가 세 층을 지났지만 배송으로 분류된 관찰(07 해석 범위 「「기타」 허용 이름 … 실행하지 않음」)을 이어받음
- 조립한 핵심 네 개: 01·02절 역할 나누기와 과업 명세(system 페르소나 · developer 과업 명세 · user 고객 문의), 04절 틀(`ChatPromptTemplate.from_messages` + `convert_to_messages` developer 객체 + 빈자리 `{inquiry}`), 06·07절 허용 이름과 JSON 세 층 검사(07절 함수 네 개 같은 코드), 08절 버전 기록 딕셔너리(+ 키 `허용 이름`, 기록에 새 키 더하기). 기록은 01절 `timed_invoke`·`make_prompt_record`
- 쓰지 않은 것(본문 b3·노트북 2번에 적음): 03절 예시, 04절 대화 기록(`MessagesPlaceholder`), 05절 근거 줄, 06절 표본 합의, 08절 비용 함수·파일 저장
- 바꾸는 값: 허용 이름 글 하나(`"배송, 교환, 환불"` → `"배송, 교환, 환불, 기타"`). 출력 형식 글(`make_rules_format`)과 검사 목록(`split(", ")`)을 같은 글에서 만들어 두 곳이 어긋나지 않게 함. 페르소나·과업 명세 앞부분·문의 두 개·모델·조립 함수는 같음
- 노트북 순서(PLAYBOOK §3): 준비(버전·import·키·모델) → 2 주제 → 3 재료(과업 명세 앞부분·문의 두 개) → 4 두 버전(`make_rules_format`·출력 형식·버전 딕셔너리) → 5 기록 장치 07절 세 층 검사(함수 네 개 + `find_category` + 「기타」 답 글을 v1·v2 목록으로 검사 `assert`) → 6 기록 장치 01절(`timed_invoke`·`make_prompt_record`) → 7 조립(`build_prompt`, 틀 채운 메시지 객체 확인, `ask_inquiry` 줄마다 절 주석) → 8 실행 1(요청 2·답 원문·기록표·검사표) → 9 실행 2(요청 2·답 원문) → 10 두 실행 비교 → 실험 결과 해석 → 정리 3줄
- 실행 1(B): `v1 · 텀블러 문의 | 191 | 104 | stop | 1.94`·`읽음 | [] | [] | 교환`, `v1 · 글꼴 문의 | 169 | 92 | stop | 1.23`·`읽음 | [] | [] | 배송`(next_action `주문 배송 관련 문의가 아니어서` = 답 스스로 배송 문의가 아니라고 적음 → 내용 오류)
- 실행 2(B): 텀블러 193/102·교환, 글꼴 171/131·기타(next_action이 고객에게 하는 말). 네 답 모두 세 층 통과. 입력 +2(두 문의)
- 앞선 실행 A(본문 b6·복습 4에 적은 것): 출력 v1 101·93, v2 94·94. 글꼴 출력 92 → 131 차이를 허용 이름 탓으로 보지 않는 근거
- 설계 과정: 「기타」와 두 문의는 탐색에서 흐름을 확인한 뒤 정함(b7 「흐름을 보여 주려고 정한 예」). 문의를 둘로 한 것은 틀 하나에 문의를 바꿔 채우는 04절 쓰임과 「바뀌지 않아야 하는 문의(텀블러)」를 함께 보이려는 것(요청 4번, 규격 §7-2의 3~5번 안). 5절 확인 셀은 검사 함수가 바깥 이름 `allowed_labels`를 읽어 버전을 바꿀 때 목록도 바꿔야 한다는 점을 요청 없이 보이려고 더함
- 사다리: L1~L4 범위와 `try/except 이름`(07절 코드). 셀 하나에 함수 하나, 함수 본문 최대 6문장(`ask_inquiry`), 코드 셀 최대 12줄(재료 셀·비교 셀). 두 겹 호출 없음(`convert_to_messages([...])[0]`·`prompt.invoke({...}).to_messages()`는 04절 모양), 내포식·조건 표현식·f-string·`raise`·`+=`·`lambda`·`join`·`next` 없음. 새로 보인 모양: 글 메서드 `split(", ")`(02절 `split("\n")`과 같은 메서드, 한 문장 설명), 바깥 이름에 다른 목록을 다시 담아 함수 결과가 바뀌는 것(06·07 「함수가 바깥 목록을 읽음」 이음). `upgrade_allow` 없음
- 반복문 안 출력 없음: 요청 반복문은 `append`만, 출력은 끝난 뒤(Ch 6·06·07·08 인계). 셀마다 출력 칸 한 개

## 앞 절에서 가져온 이름과 연속성 판단

- 같은 코드로 가져온 것: 07절 `parse_json_answer`·`find_missing_keys`·`find_value_problems`·`check_layers`·`required_keys`, 01절 `timed_invoke`·`make_prompt_record`(키 6개), 02절 `persona_text`·`goal_text`·`required_text`·`forbidden_text`, 07절 `task_start_text` 모양, 01~08 `inquiry_text`, 03·07 `font_inquiry_text`, nbkit 키·모델 셀(08과 같은 설치 셀)
- 가져온 값·모양: 07절 값 규칙 네 문장(허용 이름 자리만 인자), 06·07 `allowed_labels` 이름, 04절 틀 모양·`input_variables`·메시지 객체 출력 줄(`클래스 | 역할 이름 | 추가 정보`), 08절 버전 딕셔너리 키(`버전`·`바꾼 것`·`바꾼 이유`·`과업 명세`)와 `prompt_versions`·`version["기록"] = …`·`range(len(목록))`, 07 기록표·검사표 라벨 모양
- 새 이름: `make_rules_format`·`find_category`·`build_prompt`·`ask_inquiry`, `inquiries`·`v1_label_text`·`v2_label_text`·`v1_format_text`·`v2_format_text`·`added_characters`·`v1_version`·`v2_version`·`other_text`·`v1_check`·`v2_check`·`other_category`·`v1_prompt`·`v2_prompt`·`font_messages`·`run1_records`·`run2_records`·`first_check`·`second_check`. 기록 새 키 `검사`·`category`(08 `add_cost_items`처럼 더함). 08절 `estimate_openai_cost`는 쓰지 않아 Ch 8 테스트가 꺼내는 이름과 겹치지 않음
- 용어: 새 용어 0개. 「허용 이름」「형식 오류」(06), 「세 층 검사」「내용 오류」「값 규칙」「키」(07), 「프롬프트 버전」「버전 기록」「기준선」(08), 「틀」「빈자리」(04), 「과업 명세」「페르소나」(02)를 같은 뜻으로 씀. 「필드」「칸」「양식」「조각」「청크」「쟁반」「카드 꽂이」「우편함」「투명 봉투」 안 씀(본문 일상 예 「우편물 분류 선반의 칸」은 비유 문장 한 곳, Ch 6 02-5 「우편함」 삽화와 다른 말)
- 08절 「다음 학습」: 08 b8을 「09절은 이 챕터의 실습 … 09절은 이 절의 기록 파일을 읽거나 고치지 않습니다 … Ch 8 06절과 그 뒤 챕터 연결은 09절 끝에서 안내」로, 08 노트북 정리 끝 문장·`author_08.py` 같은 문장도(`mdpatch.py`, 재실행 없음). 기존 Ch 8 06(full·selected·compressed)·Ch 11·Ch 15 문장은 09 b8로 옮김(Ch 8 06 노트북·`_src`에 `prompt-ab-continuity` 있음을 grep으로 확인, Ch 11 `chapter.json` 제목 「평가 기초 — 측정 가능한 검색 품질」, `textbook/part4/ch15-evaluation-advanced` 폴더 확인)
- 비유 삽화: 02-5~08-5 책상·파란 명찰(system)·주황 클립보드(developer)·노란 메모지(user) 약속을 이어 씀. 연보라 답 카드 대신 메모지가 들어간 상자로 분류 결과를 보인다고 그림 읽기에 적음

## 사실 주장 확인

- 노트북 출력으로 확인: 위 실행 1·2·비교 값, `v2 출력 형식에서 늘어난 글자 수: 4`, 버전 두 줄 허용 이름 목록, 「기타」 답 글 v1/v2 검사 결과, `채울 이름: ['inquiry']`·developer 표시
- 07절 값과 대조: 입력 191(07 「값 규칙」)·169(07 글꼴 문의) — handoff §07 → §08 실행값
- 기기 셸에서만 확인했다고 적은 것(b7): v1 출력 형식 글이 07절 글과 글자까지 같음(probe1 `same as 07: True`), 탐색 분류 결과
- 실행하지 않았다고 적은 것: 맞는 이름이 있는 문의까지 기타로 가는 경우, next_action 말투 검사, 버전마다 여러 번 보내기, 속도 비교, 파일 저장, 다른 버전·Windows·macOS
- 참고 자료: 04·07절 작업에서 2026-09-17에 확인한 문서 3개 + 라이선스(이 절에서 다시 열지 않았다고 b10에 적음)

## 그림

- Mermaid 3장(PNG 직접 확인): 09-1 조립도(flowchart TB 7노드, viewBox 358), 09-2 실행 1 순서(sequenceDiagram 참가자 셋 `messageAlign: left`, 요청 실선·응답 점선, 메모는 응답 직후·반복 뒤, 716), 09-3 두 실행 비교(LR 큰 상자 둘 + 안쪽 TB, `R1 ~~~ R2`, 696)
- 삽화 1장: 09-4 분류함과 기타 상자. nano_banana_pro 16:9 2k, 1회 생성, 2크레딧(생성 전 잔액 2850). 채택 job `eaa5c8fb-8383-4001-8c47-bab61c044dfa`. 클라우드 출력 폴더 입출력 오류로 기기 셸 `curl` 원본(SHA-256 `c8832468…fc076bc99c`) → 1100×614 저장, 같은 폭으로 줄인 원본과 픽셀 차이 0(bbox None). 그림 읽기·검수 메모는 저장 파일을 보고 씀(오른쪽 클립보드 줄이 두 배쯤 많음, 컵이 유리컵 모양)
- 색(§5-3): 재료·버전 기록·허용 이름 초록, 정의한 함수 파랑, 실행한 모델 보라, 기록·검사 결과·원문 판단 노랑, 빨강·회색 0장(내용 오류는 받아 기록한 관찰). 근거는 `09-figures.md`

## 바꾼 다른 파일

- `chapter.json` sections 끝에 `09-프롬프트-엔지니어링-실습`(「프롬프트 엔지니어링 실습: 고객 문의 분류 틀에 JSON 검사와 버전 기록 붙이기」, experiment). 챕터 시수 「총 24h · 강의 8h · 실습 16h」는 바꾸지 않음(09 30분은 실습 16h 안, 규격 §7-2). 챕터 `index.html`은 빌드가 다시 만듦(「절 9개」). `_src/index-body.html`은 빌더가 읽지 않는 옛 파일이라 고치지 않음(개선 전 절 표·시간 배분 그대로 → 챕터 검토 때 정리 여부 결정)
- `_src/08-프롬프트-버전과-AB-비교.html` b8, 08 노트북 정리 끝 문장, `author_08.py` 같은 문장(`mdpatch.py`, 08 재실행 없음)
- `labs/part2/ch07-prompt-engineering/README.md`: 「8개 노트북은」→「9개 노트북은」, 09 한 줄(파일을 만들거나 고치지 않음). 같은 README의 「모든 실습은 같은 고객 문의와 같은 평가 항목」「응답 원문·토큰·지연 시간·평가 결과」 등 개선 전 문장은 범위 밖이라 그대로 둠(챕터 검토 때 확인)
- `집필점검표.md` 품질 개선 표에 09 행
- 옛 생성기 `labs/part2/ch07-prompt-engineering/_make_notebooks.py`는 실행하지 않음(01절 때 넣은 `raise SystemExit` 그대로, 챕터 마감 때 옮김)
- 루트 `textbook/qa/upgrade-progress.md`·과정 요약은 챕터 밖이라 고치지 않음

## 검토에서 볼 곳

- 결론 범위(b6 마지막 단락, 노트북 10번 결과 읽기·실험 결과 해석, 복습 3·4): 글꼴 문의 분류 변화를 문의 두 개·한 번 실행 밖으로 넓히지 않았는지, 「4글자 몫으로 보입니다」 표현, 입력 토큰 수가 같다는 것을 글자 같음의 증명으로 쓰지 않았는지
- 5절 확인 셀과 실행 셀의 `allowed_labels` 다시 담기가 초보자에게 읽히는지(바깥 이름을 바꿔 함수 결과가 달라지는 모양, b7 셀 순서 주의)
- 삽화 09-4 비유(붓 메모지 = 글꼴 문의, 회색 빈 상자 = 기타)가 그림만으로 읽히는지, 「답 카드 대신 메모지」 설명

## 검토

- 별도 세션 검토 1차(2026-09-17, `qa/upgrade/review-round1-B.md`): **accept**(하 2). 반영: 09-1 노트북 [44] 「08절에서는 키 `기록`에 기록 딕셔너리 하나를 담았습니다. 이 실습은 버전마다 문의가 둘이라 기록 두 줄을 목록으로 담습니다.」 09-2 09-3 도식 읽기 「노란 상자 두 개는 10번 비교 표의 문의별 결과 / 왼쪽 글꼴 문의 상자의 끝 줄은 8번 답 원문」, 09-1 도식 읽기 둘째 단락 「함수 `find_category()`는 07절 함수가 아니라 이 실습에서 새로 정의한 함수입니다」(권고 문장은 코드 이름+조사로 시작해 「함수」를 앞에 둠, 그림은 다시 렌더하지 않음). C-4 비유 「우편물 분류 선반의 칸」 → 「우편물 분류함의 상자」(그림과 같게, `figures/09-4-…caption.md`·`prompt.md`·`09-figures.md`). 결정 Q4 권고대로 결론 범위·`allowed_labels` 다시 담기·삽화 09-4·08 b8 새 문장 유지. 실습 30분은 챕터 시수에 더하지 않음(`chapter-summary.md` §3).
- 반영 방법: `mdpatch.py` → `run_section.sh … 09 --no-exec`(노트북 재실행 없음, 코드 셀·출력·`verification` 메타데이터로 만든 해시가 반영 전과 같음). 마감 게이트 `gates-after.json`(`--strict`) G1~G7 0, 코드 셀 25, 검사 문장 385. 리뷰 묶음은 다시 만들었고 반영 전 묶음은 `qa/upgrade/before/review-round1/review-pack/`에 있습니다.

## 남은 것

- 리뷰 묶음: `qa/upgrade/review-pack/09-프롬프트-엔지니어링-실습.md`(08도 다시 만듦)
- 정리 대상(삭제하지 않고 목록만): `/tmp/ch07-09`(probe1.py, run1.ipynb 사본, reps1.py·reps1~3.json·reps08.py/json, outhash.py, 삽화 원본 `hf_09-4_a.png`, visual 사본과 화면 캡처), `qa/upgrade/before/08-to-09/`(08 수정 전 사본), `qa/upgrade/gates-wip-09.json`
- 챕터 검토(별도 세션)와 `chapter-summary.md`는 다음 단계(handoff `## 실습 → 챕터 검토`)
