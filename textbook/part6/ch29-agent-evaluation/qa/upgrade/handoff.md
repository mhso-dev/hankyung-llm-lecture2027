# Ch 29 Agent 평가 — 절 사이 인계 (handoff)

- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 28 `chapter-summary.md` → 준비 조사 `qa/upgrade/chapter-lead-notes.md` → **이 파일** → 앞 절 `NN-diagnosis.md`·완료본(`_src`·노트북·생성기).
- **01절 완료 2026-09-29**(게이트 27 → 0, 코드 셀 5 → 23, 검사 문장 358, **모델 요청 0**, 새 커널 두 번 셀별 출력 글 23/23 같음, **도구 파일 `notebooks/eval_tools.py` 첫 판**(`dab0888f…`), 공용·챕터 옛 생성기 둘 막음, Mermaid 4 + 삽화 1(재생성 0·2크레딧)). 세부 값은 `01-diagnosis.md`.
- **02절 완료 2026-09-29**(게이트 41 → 0, 코드 셀 5 → 27, 검사 문장 415, **모델 요청 0**, 새 커널 두 번 셀별 출력 글 27/27 같음, **도구 파일 02판**(`4a3d8143…` — 01 셀 셋 더함 + 가져오기 줄 `langchain.messages`), Mermaid 4 + 삽화 1(재생성 0·2크레딧)). 세부 값은 `02-diagnosis.md`.
- **03절 완료 2026-09-29**(게이트 22 → 0, 코드 셀 5 → 28, 검사 문장 429, **모델 요청 노트북 한 번 5(에이전트 3 + 평가 모델 2)·이 절 합계 40(흔들림 확인 25 포함)**, 흔들림 확인 5/5 같음(평가 모델 `True`·`False` 모두 5/5, §0 02:11:04Z → 첫 요청 02:11:11Z), 새 커널 두 번 셀별 출력 26/28 같음(갈린 둘은 판정 까닭 글만), **도구 파일 03판**(`617a82bc…` — 02 셀 `four_modes` + Ch 21 `sum_usage`·`estimate_cost`, 가져오기 줄 그대로), Mermaid 4 + 삽화 1(재생성 0·2크레딧)). 세부 값은 `03-diagnosis.md`·`03-probe.md`.
- **04절 완료 2026-09-29**(게이트 41 → 0, 코드 셀 9 → 25, 검사 문장 397, **모델 요청 0**, 새 커널 두 번 셀별 출력 25/25 같음(`outputs_sha256`까지), 계약 파일 둘 읽기만(`25cfe5df…`·`5ba7f5a0…` 그대로), **학생 묶음(zip을 풀어 `notebooks/`에서, 키 없이) PASS 25셀**, **도구 파일 04판**(`223881ec…` — Ch 15 06 노트북 셀 `average`·`nearest_rank` 글자 그대로 + 가져오기 줄 `import math`), Mermaid 4 + 삽화 1(재생성 0·2크레딧)). 세부 값은 `04-diagnosis.md`.
- **05절(실습) 완료 2026-09-29**(새 절 `05-Agent-평가-실습`, 게이트 0, 코드 셀 24, 검사 문장 371, **모델 요청 노트북 한 번 5(실행 1 = 3 + 실행 2 = 2, 평가 모델 0)·이 절 합계 35(흔들림 확인 25 포함)**, 흔들림 확인 모든 칸 5/5(§0 03:28:07Z → 첫 요청 03:28:14Z), 새 커널 두 번 24/24 같음(`outputs_sha256`까지), **도구 파일 05판**(`d624b8f3…` — 04 셀 `show_row`), 04 끝 문장 → 05(04 해시 그대로), `part6-practice.zip` 다시 만듦, Mermaid 3 + 삽화 1(재생성 0·2크레딧)). 세부 값은 `05-diagnosis.md`·아래 「실습 → 챕터 검토」.
- **전체 마감 2026-09-30 — 도구 파일 머리 줄**: `eval_tools.py` 머리 설명에 Ch 15 06절 노트북 셀(`average`·`nearest_rank`) 출처 한 줄만 더함 — `d624b8f3…` → **`b75636c4f0cb6bc2719d2f0bfa22a6840ac7acf2b28bc67e6f974c266bcc0a47`**(함수 본문·노트북 해시 같음, 생성기 `author_01.TOOLS_HEAD`와 판 해시 고정값 셋 `author_03`(02판)·`author_04`(03판)·`author_05.TOOLS_04_SHA`, 뒤 챕터 고정값 Ch 34 `author_01.EVAL_TOOLS_SHA`도 새 값). 가져오기 줄 주석 둘(「01절에서 옮긴」·「04절에서 옮긴」)은 머리 설명 밖이라 그대로. 기록 `textbook/qa/final-close-log.md` 2단계·`chapter-summary.md` §11 끝.

## 챕터 공통 (01절에서 정한 것)

### 챕터 리드 결정 (그대로 이어 지키세요)

1. **모델 M2**: **01·02 모델 없음**(코드로 만든 궤적 — 결정적, 요청 0, 키 셀 없음) · **03 앞 절반 모델 없음 + 뒤 절반 실제 모델**(실제 에이전트를 한 번 돌려 궤적을 만들고, 그 궤적을 궤적 맞춰 보기(결정적)와 평가 모델(흔들림)로 평가 — 이 챕터에서 평가받는 에이전트를 실제로 돌리는 유일한 자리) · **04 모델 없음**(Ch 18 06·Ch 21 06 저장 기록 읽기). 모델은 `nbkit.key_and_model_cells("openai:gpt-5.4-mini")`(`temperature=0`·`reasoning_effort="none"`, 키는 루트 `.env`에서만), 평가 모델은 `create_trajectory_llm_as_judge(judge=모델 객체, …)`에 **과정 표준 모델 객체**(규격 §3 — 문자열 `model="openai:…"`이면 설치판이 온도·추론 설정 없이 `init_chat_model(model=model)`만 부름, openevals 0.2.0 `llm.py` 254행). 가짜 채팅 모델 금지. 에이전트에는 작은 실행 한도·호출 한도(Ch 22 04 `ModelCallLimitMiddleware(run_limit=N, exit_behavior="end")` — invoke 한 번마다 셈, Ch 26~28 안전 규칙).
2. **01 설계(끝남)**: 세 전략(최종 답·한 단계·궤적)을 코드로 만든 궤적 넷으로 같은 기준 궤적과 견줌 — 표·거짓을 낸 평가·첫 응답·답만 틀림 뜯어보기·값 바꿔 보기(답 글만). 01은 모드 `strict` 하나만 첫 정의, **네 모드·횟수 짝짓기·인자 비교는 02 몫**.
3. **04 계약(04 몫)**: 아래 「04 계약 대조표」. **01·04 슬러그 고정**(Ch 28 06 b8 → 01 · Ch 21 06 b2 → 04).
4. **용어**: 아래 표. 「궤적」 첫 자리는 01이 함(Ch 17 04 이음) — 02~04는 「01절에서 본 것처럼」으로.
5. **도구 파일 `eval_tools.py`**: 아래.
6. **옛 생성기**: 공용 `textbook/part6/_author_ch21_ch29.py`(`650f6506…` → `391be055…`)·`figures/_gen_figures.py`(`65b435f8…` → `3577112d…`)를 01이 막음(설명 주석 + `raise SystemExit`, Ch 21 건너뛰기 조건 그대로). `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6b_enrich.py`(`8528cb33…`)·`part6b_review_fixes.py`(`a0299166…`)는 **고치지 않고 실행 금지**(기록만). 옮기기(`mv -n` → `qa/upgrade/before/generators/blocked/`)는 마감.
7. **슬러그 넷 그대로**, 절 제목 말은 강사 확인(챕터 제목 「실행 경로」·03 「LLM judge」·04 「Ch18 궤적」 — 제목에만).
8. **문법 범위**: 아래 「허용 문법 범위」.
9. **비유 계열 「오르골 종이띠」**: 아래.
10. **준비 셀 과정 표준**: 설치 `%pip`은 그 절이 쓰는 패키지만·잠금 판 번호까지(01 = `agentevals==0.0.9`·`langchain==1.4.0`), 가져오기, 모델 절만 키·모델 셀(03). 03이 `create_agent`·모델을 쓰면 `langchain-openai==1.6.0`·`python-dotenv==1.2.3`를 더함(잠금 판). 04가 도구 파일을 가져오면 그 파일이 가져오는 패키지도(규격 §2-7 6번 — 지금 판은 가져오기 0).
11. **실행 규칙(01이 씀)**: 절 실행은 `PYTHONDONTWRITEBYTECODE=1 bash … run_section.sh …`로 — 도구 파일을 가져오는 커널이 실습 폴더 `notebooks/__pycache__`에 pyc를 쓰지 않게(연결 폴더라 지울 수 없음). 첫 실행 전 기기 사본에서 `execute.py --cwd 사본`으로 한 번 돌려 `.failure.json`이 실습 폴더에 남지 않게. 그림 파일 없이 첫 `run_section.sh`를 부르면 `attach_figures.py`에서 멈춤(실행·저장은 끝난 뒤) — 01은 이 차례로 B를 그림 전에 돌림.

### 모델 설정과 03 설계 (03 몫 — 01은 요청 0)

- 모델 셀: `nbkit.key_and_model_cells("openai:gpt-5.4-mini")` → 실행일 결과 읽기. 평가 모델: `create_trajectory_llm_as_judge(judge=model, prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE)`(준비 노트 §6-2 — 결과 `{'key': 'trajectory_accuracy', 'score': 참·거짓, 'comment': 판정 까닭, 'metadata': None}`, 평가 한 번에 요청 1번, 출력 형식은 `json_schema`).
- 앞 절반(모델 없음): 01 궤적(기준·답만 틀림 등)을 평가 모델에 넣을 **요청 글 모양**(설치판 `_format_inputs` — 태그 모양 글)·결과 칸 이름·평가 모델 객체 만들기(요청 0)까지. 뒤 절반(실제 모델): `create_agent(model, tools=[…], system_prompt=…, middleware=[ModelCallLimitMiddleware(…)])` 한 번 → 궤적 → `strict`(와 02의 다른 모드) + 평가 모델 판정. 도구는 01의 이름(`search_documents(query)`·`check_source(doc_id)`)을 **평범한 `@tool` 함수**로 만들면 01 궤적과 이어짐(결과 글은 01 `tool_results` 모양 — Ch 14 LIB-001 글, 임베딩 없이 — 제안).
- 흔들림: `03-probe.md` §0(판단 규칙·그림 라벨 규칙)을 **첫 요청 전에** 적고, 노트북에 넣을 요청마다 노트북 밖 5번 → 새 커널 두 번. 결론·그림·정리·복습에는 결정적 값(궤적 맞춰 보기 점수·요청 수 셈 「도구를 요청한 응답 수 + 1」)과 「5/5·두 커널 같음」인 평가 모델 점수만(한정어와 함께). 판정 까닭 글·흔들린 점수·토큰·비용은 결과 읽기 둘째 단락·b6 표·b7에만(규격 §2-7 9·10번 끝). 옛 기록에 같은 입력의 판정이 `True`(저장 노트북)·`False`(옛 검증 기록)로 갈린 선례가 있음(준비 노트 §8-2). 원하는 점수가 나올 때까지 다시 돌리지 않음.
- 판정 까닭(`comment`)은 영어로 옴 — 결론에 쓰지 않고, 판정 기준 네 줄(단계 사이 논리·진행·상대적 효율·기준과 뜻이 같음)만 한국어로 풂. 「효율」은 금지어 목록에 있어 「도구를 덜 부르는 쪽」 등으로 풀기.
- 03 b3는 01 값 바꿔 보기(「뜻이 같은지 보려면 … 03절에서 궤적을 평가 모델로 판정합니다」)를 받아야 참 — 01 정리·b6·b7이 03을 가리킴(「평가 모델로 판정」).

### 04 계약 대조표 (04 몫 — 준비 노트 §3을 옮김, 읽기만)

| 파일 | 해시(지금) | 04가 읽는 것 | 만든 쪽 |
|---|---|---|---|
| `labs/part6/ch21-create-agent/data/rag-comparison.json` | `25cfe5df3cfd729c130bce4af26c716cfcc3bcd4b4ff6e4a9d0a725816b02f51` | 줄 3(`C01`·`C05`·`C07`) · `qid`·`agent_usage`{`model_calls`·`input_tokens`·`output_tokens`}·`agent_supported`·`tool_calls`·`agent_latency_s`·`agent_trace` | Ch 21 06(**다시 실행 금지**) |
| `labs/part5/ch18-workflow-patterns/notebooks/06-같은-과제로-다섯-패턴-비교.ipynb` | `5ba7f5a01fa8a8625a4673e6f6a007691907078b20c41ee828aa266252ba0b20` | 셀 49 저장 출력의 `" \| "` 줄(머리 `pattern` 뺌) 마지막 다섯, 여섯 칸 | Ch 18 06(**다시 실행 금지** — 저장 출력을 읽는 모양 유지, Ch 18 문장) |

| 자리 | 옛 값 | 새 값(지금 파일로 셈) |
|---|---|---|
| `_src/04-…` 6·7·9행 Ch 18 다섯 패턴 평균 | 0.88 · 2.8 · 610.2 · 4.145 | **0.96 · 2.8 · 862.2 · 4.206** |
| 같은 줄 Ch 21 세 줄 평균 | 1.0 · 2 · 1 · 519.7 · 1.880 | **1.0 · 2 · 1 · 688 · 1.731** |
| 같은 줄 p95(가장 가까운 자리 방식, 셋이면 최댓값) | 2.094초 · 541 | **2.003 · 699** |
| 10행 복습 3 해설 | 2.094초 | **2.003** |
| 노트북 셀 8 Ch 18 표 줄 수 | 6 | **5** |

- **학생 묶음에서 멈추는 파일 찾기**(`textbook/` 찾기·`커리큘럼_v6.html` `assert`)를 과정 표준 파일 위치 셀(Ch 19~21 모양 — `candidates` + `for`·`break`, 묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리 — 묶음 안 상대 위치 `../../ch21-create-agent/data/…`·`../../../part5/ch18-workflow-patterns/notebooks/…`)로.
- 걸린 초·토큰은 **각 기록이 한 번 실행한 값**이라는 한정과 함께 표·결과 읽기 둘째 단락에만(초로 순위 매기지 않기), 결론은 세는 값(요청 수·도구 요청 수·줄 수·성공 여부). Ch 18 `tool_calls: 0`은 손 값 — 공개하거나 기록에서 끌어내기. Ch 18 품질 칸 = 코드 검사 0~5 ↔ Ch 21 `agent_supported` = 평가 모델 판정(척도가 다름 — 한 칸에 담으면 밝힘). 「Ch 18 궤적」 — Ch 18 기록에는 도구 궤적이 없음(b2·b3에서 밝힘).
- 04가 Ch 15 06 `nearest_rank(values, percent)`를 쓰면 **도구 파일에 원본 글자 그대로**(노트북 셀 `06-대화당-비용-백분위수.ipynb` 1095행 부근) — `nearest_rank_p95` 새 이름 금지. `statistics.mean`·`all`·`max`는 04가 처음 쓰면 한 문장씩(또는 Ch 15 `average`).
- Ch 21 06 b7 「Ch 29 04절 노트북 12~18번 셀이 …」 — 04를 다시 쓰면 셀 번호가 바뀜(Ch 21 파일은 고치지 않음, 마감 인계).

### 용어 표 (01에서 정함 — 02~04는 그대로 이어 씀)

| 말 | 뜻 | 코드에서 | 첫 자리 |
|---|---|---|---|
| **궤적(trajectory)** | **(마감 A-1에서 넓힘)** 에이전트가 질문에서 최종 답까지 밟은 단계의 차례 — 이 챕터는 질문·모델 응답(도구 호출 요청)·도구 결과·마지막 답을 일어난 차례대로 담은 **메시지 목록 전체**로 적음. Ch 17 04 「실행 기록의 단계를 차례대로 늘어놓은 것(단계 차례·궤적)」을 이어 씀. 궤적 맞춰 보기의 모드는 이 목록 가운데 **도구 호출 요청**을 견줌. 도구 이름만 차례대로 모은 목록은 **「도구 차례」**(`called_tool_names`)로 가름 — 옛 정의 「에이전트가 도구를 부른 차례」는 쓰지 않음 | 메시지 목록(`make_trajectory`) · 도구 차례 `called_tool_names(messages)` | 01 |
| **기준 궤적(reference trajectory)** | 좋은 에이전트라면 밟을 것이라고 사람이 미리 적어 둔 궤적(「흐름을 보여 주려고 정한 예」) | `reference` | 01 |
| **최종 답 평가(final response)** · **한 단계 평가(single step)** · **궤적 평가(trajectory)** | 마지막 답만 / 한 단계만 떼어 / 모든 단계를 판정(LangSmith evaluation-approaches). 영어 원어는 괄호 소문자 한 번씩, 영어 세 이름을 본문 말로 쓰지 않음 | `final_answer_pass`·`first_step_pass`·`trajectory_pass`·`three_results` | 01 |
| **궤적 맞춰 보기(trajectory match)** | 실제 궤적을 기준 궤적과 코드 규칙으로 맞춰 보는 방법. 「매칭」은 02 제목에만 | `create_trajectory_match_evaluator(…)` | 01 |
| 모드 **`strict`** | 메시지 수·역할·차례와 도구 요청의 이름·인자가 모두 기준과 같아야 참, **메시지 글은 견주지 않음**. 본문은 「모드 `strict`는」(백틱 코드 + 모드 — 영문 시작 조사 금지) | `trajectory_match_mode="strict"` | 01 |
| (02가 정할 말) 모드 `unordered`·`subset`·`superset` · 인자 비교 방식(`tool_args_match_mode` — `exact`·`ignore`·`subset`·`superset`) | 첫 자리에서 한 번씩 한국어 풀이(차례 무관·기준 안에서만·기준을 모두 담음 등). 「집합」 금지(과정 금지 문법 `set`과 헷갈림 — 「모음」·「기준 도구 요청을 모두 담음」) | — | 02 |
| (03이 정할 말) 평가 모델(judge) · 판정 머리글 · 판정 까닭 · 판정 기준 | **Ch 15 말 그대로**: 「평가 모델(judge)」(Ch 15 01 — 과정 요약 §5·Ch 15 `_src` 01~09·Ch 18·21. **「판정 모델」은 과정 말이 아님** — Ch 15 04에 한 번 있을 뿐, 챕터 리드 결정 4의 「판정 모델」은 이 말로 바꿔 씀) · 「판정 머리글」(`TRAJECTORY_ACCURACY_PROMPT…`는 백틱, 「프롬프트」·「루브릭」 본문 0) · 판정 까닭(`comment` — Ch 21 06 「까닭:」 줄) · 판정 기준(Ch 15 02·07) · 평가받는 에이전트(「피평가」 금지) | — | 03 |
| (04가 정할 말) 운영 지표 · 95 백분위수(가장 가까운 자리 방식 — Ch 15 06) · 걸린 초 · 칸 | 「지연」·「스텝」·「불리언」·「열」·「필드」·「Agentic」 금지 | — | 04 |
| (이어 씀) 평가 모델(judge)·코드 검사·도구 호출 요청(칸 넷 `name`·`args`·`id`·`type`)·도구 메시지·호출 ID·딕셔너리·칸·참·거짓 값·요청 수 셈·호출 한도·실행 한도·바퀴 한도 | Ch 15 01·Ch 18 05·Ch 19 04·05·Ch 26~28 — 한도 셋은 섞지 않음 | — | 앞 챕터 |

- 새 용어 meta: 01 = **5**(기준 궤적·최종 답 평가·한 단계 평가·궤적 평가·궤적 맞춰 보기 — 「궤적」은 이어 씀). 옛 meta 5·5·5·5는 옛 생성기 틀 값 — 절마다 실제 새 말 수로.
- 대체어: 반환 → 내놓다 · 검증 → 검사 · 측정 → 재다·세다 · 사전 → 딕셔너리 · 경로 → 차례·흐름(파일이면 파일 위치) · 블랙박스 → 「안쪽을 보지 않고」 · 지연 → 걸린 초 · 옵션 → 설정·인자 · 보장 → 「늘 … 라고 할 수 없다」 · 재실행 → 다시 실행 · 루브릭 → 판정 기준 · 프롬프트 → 판정 머리글·요청 글 · 피평가 에이전트 → 평가받는 에이전트 · 「돌려 만든」 → 「실행해 만든」.

### 금지어 (01 설명·주석·캡션·`.mmd`·alt 0건 — 제목·슬러그·코드 백틱 말고)

- Ch 28 목록 전부(Ch 27 목록 + 「프로토콜」·「세션」·「핸드셰이크」·「리소스」·「인스턴스」·「스펙」·「레거시」·「안내 글」) + 과정 목록(§5) + 「한 겹 더」·「쉽게·간단히·당연히」·「강사 시연」·「개선 전」 + 준비 노트 목록(「반환」·「검증」·「측정」·「추정」·「지연」·「경로」·「스키마」·「사전」·「프롬프트」·「루브릭」·「스텝」·「불리언」·「필드」·「집합」·「범주」·「명시」·「노출」·「보장」·「효율」·「블랙박스」·「피평가」·「판정식」·「수치」·「실측」·「운영 화면」·「실행 경로」·「결정적」·「알 수 있습니다」 등) + 이 챕터가 더한 말 「매칭」(02 제목 밖)·「판정 모델」·영어 세 이름(Final Response·Single step·Trajectory). **「궤적」은 이 챕터 본문 말이라 허용**(Ch 28 금지어였음).
- 검사 스크립트 `/tmp/ch29-01/tools/ban29.py`(인자: `_src` 파일·노트북·추가 글롭 — `.mmd`는 라벨만). 거짓 양성: 참고 자료 원제목(「LangSmith Trajectory evals」).
- G6 함정: 괄호 뒤 「).」 · 「`코드`는」 영문 시작 조사 · 「그림 읽기 —」 머리가 첫 문장 글자 수에 들어감 · 표 칸(`</td>`)은 단락 하나로 셈(다섯 문장 이하) · 결과 읽기 첫 단락의 숫자 든 백틱 인용은 **그 셀 출력**에 있어야 함(`LIB-001`처럼 다른 셀 출력의 값은 둘째 단락으로).

### 허용 문법 범위 (01절 AST 확인 — `/tmp/ch29-01/tools/extra_check.py` 0건, 호출 깊이 최대 2)

- 쓰는 것: 함수(셀당 하나, 본문 8줄 이하 — 01 최대 6, 힌트·기본값 없음) · 여러 줄 `if`·`for` · 목록 `append` · `not`·`==`·`in` · 딕셔너리 여러 줄(키마다 한 줄)·목록 안 딕셔너리 · 번호 `[1]`·음수 번호 `[-1]`(01 첫 풀이 — Ch 16 03 음수 슬라이스) · `type(x).__name__`(Ch 19 06) · `list(딕셔너리)` · `len` · 키워드 인자(`trajectory_match_mode=`·`outputs=`·`reference_outputs=`·`content=`·`tool_calls=`·`tool_call_id=`).
- 쓰지 않는 것(01 0건): f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`getattr`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`sorted`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`.items`·`+=`·기본값 매개변수·힌트·대입 풀기·`for` 풀기·별표 풀기·`while`·`try`·세미콜론·`isinstance`·클래스·데코레이터·`async`. 03의 `@tool` 매개변수 `: str`(Ch 19 01 선례)·04의 `statistics.mean`·`all`·`max`는 그 절 몫(처음 쓰면 한 문장).
- `assert`: 01은 0개(만든 대로 늘 참인 옛 `assert` 뺌). 라이브러리 점수(결정적)에 걸지는 02가 판단 — 걸면 「만든 대로 늘 참」이 아닌 성질(예: 모드에 따라 갈리는 값)에만. 모델 판단·모델 글·잰 값에는 금지.
- 셀 모양: 준비 셀 밖 셀 10줄 이하(01 최대 10) · 첫 줄 주석이 그 셀이 하는 일 · 정의 셀 결과 읽기 「정의 셀이라 출력이 없습니다」 · 여러 줄 출력은 라벨 줄 따로 · 코드 셀 20~32(01 23).

### 도구 파일 — `notebooks/eval_tools.py` (01 첫 판 `dab0888f0305d9c0fe5137a25666031b5a62b298034efebeeb13a757d85aafdf`)

- 함수 둘: `tool_call_names(response)`(Ch 19 04) · `show_messages(messages)`(Ch 19 06) — **Ch 21 `runner_tools.py`(`f4113158…`)의 설명 주석·본문 글자 그대로**(Ch 27 `harness_tools.py`·Ch 28 `connect_tools.py`와도 본문 같음). 가져오기 0. 가져오는 절: 01.
- 이름은 과정 도구 파일 스물넷과 겹치지 않음. `tool_names`는 과정에 두 모양이 있어 새 함수 이름으로 쓰지 않음(01은 `called_tool_names`).
- **01이 처음 가르친 함수(01 노트북에만)**: `make_trajectory(question, calls, results, answer)` · `called_tool_names(messages)` · `final_answer_pass(messages, reference)` · `first_step_pass(messages, reference)` · `trajectory_pass(messages, reference, evaluator)` · `three_results(messages, reference, evaluator)`. 02·03이 다시 쓰면 **그 절이 01 셀 글 그대로** 도구 파일에 더함(주석 `# Ch 29 01절에서 배웠습니다 — 01절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다`) + 처음 가져오는 절에 인자 한 문장.
- **생성기 대조 사슬(Ch 27 `author_02.py` 본)**: 01 생성기의 `TOOLS_HEAD`·`TOOLS`·`strip_later_imports`·`check_tools`를 `import author_01`로 받아 **01 판으로 시작하는지**(`strip_later_imports(new).startswith(author_01.TOOLS)`) 확인하고 뒤에 더함 · 뒤 절이 가져오기 줄을 더하면 머리 설명과 첫 `# Ch` 주석 사이에(`strip_later_imports`가 빼고 견줌) · 쓰기 가드(없거나 같은 판일 때만 쓰고 더 긴 판이면 `skip`) · `--tools-copy DIR`(B 사본). **01 생성기는 뒤 절 판을 덮어쓰지 않음**(쓰기 가드 확인 — 01을 다시 돌리면 `skip`). 머리 설명은 「이 챕터 앞 절 노트북에서 처음 적은 함수를 옮길 때는, 그 셀의 주석과 본문을 글자 그대로 옮깁니다」를 이미 담아 바꾸지 않아도 됨.
- 묶음: 01이 챕터 `qa/public-files.json`에 한 줄 + `collect_public_files.py`(Part 목록 92 → 93, `e0052b91…`). **zip(`part6-practice.zip` `5002dce3…`)은 마감에서 한 번**. 도구 파일이 패키지를 가져오게 되면 가져오는 모든 노트북 설치 셀에(규격 §2-7 6번).

### 색 (01절 Mermaid 4장)

- 코드로 적은 자료·값(질문·답 글·도구 요청 목록·결과 글·궤적 메시지) **초록(tool)** · 우리 코드(정의한 함수·만든 평가 함수)와 값 바꿔 보기에서 **바꾼 값 파랑(flow)**(Ch 28 06 B-10 규칙) · 출력으로 확인한 값 **노랑(measure)** · 라이브러리가 정한 것·설치판 소스로만 본 것·여러 조건 공통 값 **회색** · **보라 = 그 절에서 실제로 부른 모델만**(01·02·04 0, 03 뒤 절반만 — 평가 모델·에이전트 모델) · **빨강 0**(네 절 모두 experiment).
- 모양: 넷 이상 한 줄은 `flowchart TB` · 나란한 조건 `~~~` · 「보는 자리」 같은 갈래는 점선 · subgraph 제목 `<br>` 금지 · 라벨 안 대괄호·따옴표 금지(도구 목록은 줄을 나눠 적음) · 개수는 한글 · 긴 코드 이름·가운뎃점 목록은 `<br>`로 미리 나눔(01 첫 렌더에서 가운뎃점 뒤 끊김) · viewBox 폭 868 이하(01 최대 563) · 노드 id `call`·`end` 금지 · 라벨 숫자는 출력에 있는 것만(G7) · `%% classes` 줄.

### 비유 계열 — 「오르골 종이띠」 (01절이 엶)

- **01-5(채택, job `0defeb4c-9d52-4c66-ab90-98cc098bae03`)**: 흰 바탕 왼쪽 닫힌 나무 오르골 상자 하나(= 에이전트, 옆면 손잡이), 상자 틈에서 나온 구멍 띠 하나(= 실제 궤적), 그 띠 첫 구멍·끝 위 돋보기 둘(= 한 단계 평가·최종 답 평가), 아래 떨어진 띠 하나(= 기준 궤적, 나란히 둔 모습 = 궤적 평가). 곡의 끝 소리 = 최종 답(그림에는 소리를 그리지 않음 — 띠 끝으로). 구멍 수·띠 길이·아래 띠 기울기·손잡이는 짝짓지 않는다고 밝힘.
- **뒤 절 후보**: 02 기준 띠 하나와 실제 띠 넷(같은 구멍 같은 차례 / 차례 뒤섞임 / 구멍이 빠짐 / 구멍이 더 있음) — 네 모드 · 03 검사대 위에 두 띠를 겹쳐 비추는 판(평가 모델 — 사람 없이, Ch 15 저울 피함) · 04 길이가 다른 띠 여러 줄이 한 받침대에 걸림(운영 기록).
- 사람·손·글자·숫자·음표·화살표·화면 없음. **금지 소품**: 도킹 포트·정거장·우주선·온실·모종판·예인선·바지선·밧줄·홈통·물방울·도미노·체스판·즉석사진·세탁기·승강 상자·전표·가마·물레·발자국·말뚝·쟁반·서랍·바구니·저울·도장·개찰구·플러그. 스타일 문구 규격 §5-4 그대로, `generate_image` `params` `{"model":"nano_banana_pro",…,"aspect_ratio":"16:9","resolution":"2k","use_unlim":false,"count":1}`, 절당 1장·재생성 1회까지, 개수는 「exactly two …」 모양으로, 크레딧은 거래 기록으로 그 절 몫(작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro` — 기록만).

## §01 → §02

**02절 주제**: 「궤적 매칭 네 모드」(experiment, **모델 없음 — 결정적, 요청 0, 키 셀 없음**). 옛 판(`before/notebooks/02-…ipynb`·`before/_src/02-*.html`): 01과 같은 `trace(*tools: str)` · 네 모드 셀(뒤집음 strict `False`·unordered `True`, search만 subset `True`·superset `False`, `audit_log` 더함 subset `False`·superset `True`) · 내포식·f-string·한 글자 변수 `m` · 「반환」·「경로」·「사전」·「집합」·「필드」·「옵션」 · b3 틀 문장.

1. **01이 남긴 자리**: 01 정리 끝·b8 「02절에서는 모드 `strict` 말고 모드 셋을 더 봅니다. 네 모드가 차례와 빠진 요청·더한 요청을 어떻게 달리 보는지 견줍니다」 → **02는 네 모드를 같은 기준 궤적과 견주고, 차례·빠진 요청·더한 요청이 모드마다 다르게 판정되는 장면을 보여야 참**. 01이 보인 것(궤적 만들기·세 평가·`strict`의 첫 정의·답만 틀림 `strict` 참)은 「01절에서 본 것처럼」으로 되풀이하지 않음. Ch 17 04 「단계 차례를 맞춰 보며 평가하는 방법은 Ch 29 02절」도 02가 참으로 만듦.
2. **모델 없이 결정적**(준비 노트 §6-1 — 다섯 번 같음, 01 탐색도 같은 설치판): 새 커널 두 번 셀별 대조, `02-probe.md` 없음.
3. **뒤집은 궤적**: `strict` `False` · `unordered` `True`(01의 「차례 바꿈」 궤적 `reversed_order`와 같은 요청 — 01에서는 `strict`·한 단계 평가가 `False`였음).
4. **짧은 궤적**(검색만): `subset` `True` · `superset` `False`.
5. **도구를 더한 궤적**(예: 검색·출처 확인 뒤 도구 하나 더): `subset` `False` · `superset` `True` — 4번과 반대.
6. **짝짓기는 횟수까지 셈**: 01의 「검색 세 번」 궤적(`wasteful`) → `strict`·`unordered`·`subset` `False`, `superset` `True`(설치판 `trajectory/utils.py` 90~134행 — 한 번 짝지은 실제 요청은 다시 못 씀). 「기준 도구 모음 안에 있으면 참」으로 쓰면 틀림.
7. **인자 비교**: 인자만 다른 궤적(예: 검색어 「도서 대출 기간」 → 다른 글)은 네 모드 모두 `False` → `tool_args_match_mode="ignore"`면 `True`(`exact`·`subset`·`superset`은 `False`, 도구별 덮어쓰기 `tool_args_match_overrides={"search_documents": "ignore"}`도 `True`) — 셀 수 한도 안에서 고르기. 한 응답에 도구 요청 둘인 궤적(`strict`만 `False`)은 선택.
8. **라이브러리 점수 `assert`**: 결정적이라 허용할 수 있음 — 걸면 모드에 따라 갈리는 값(예: 뒤집은 궤적 `strict` `False`·`unordered` `True`)에, 만든 대로 늘 참인 것(자기 자신과 견줌 등)에는 걸지 않음. 01은 `assert` 0.
9. **모드 이름 첫 정의(02 몫)**: `unordered`·`subset`·`superset`은 첫 자리에서 한 번씩 한국어 풀이(설치판 `unordered.py`는 두 방향 `superset` · `subset` = 실제 요청이 모두 기준 요청과 짝지어짐 · `superset` = 기준 요청이 모두 실제 요청과 짝지어짐), 본문은 「모드 `subset`은」. 「집합」 금지. 모드 이름이 틀리면 `ValueError`(`match.py` 81행 — 실행하면 받을 오류는 노랑).
10. **01의 궤적 함수를 다시 쓰면 도구 파일로**: `make_trajectory`·`called_tool_names`(·필요하면 `trajectory_pass`)를 01 셀 글 그대로 `eval_tools.py`에 더하고(생성기 대조 사슬 — 위 「도구 파일」), 설치 셀은 그대로(도구 파일 가져오기 0). 01의 `tool_results`·`search_args`·`source_args`·`question` 등 노트북 전역 값은 도구 파일에 넣지 않고 02 노트북에서 다시 정함(인자로 넘김). 01 판을 가져오기만 하면 새 판 없음.
11. **b3·b10 새로**: b3 = 01절(세 평가·`strict`·답만 틀림) + Ch 17 04 예고 · b10 = LangChain Agent evals(네 모드 정의 — 2026-09-29 확인 원문 「Strict: Exact match of message structure and tool calls in the same order (message content can differ)」·Subset 「Agent calls only tools from reference (no extras)」·Superset 「at least the reference tools (extras allowed)」) · LangSmith trajectory-evals · 설치판 `trajectory/unordered.py`·`subset.py`·`superset.py`·`utils.py` 행. 옛 참고 자료 둘(확인 2026-09-11)을 그대로 두지 않음. 그림은 Mermaid 3~5(모드 넷 × 궤적 표·짝짓기 그림) + 삽화 1(오르골 계열 — 위 후보), 보라·빨강 0.
12. **기록**: `02-diagnosis.md`·`02-figures.md`(렌더 전)·`집필점검표.md`·`qa/verification.md` 행 · 이 파일에 「§02 → §03」 · 보호 파일 대조(`manifest-changes.md`에 덧붙임 — 01 뒤 10개 해시는 01 기록 값) · 새 커널 두 번(A·B, B는 그림 전) 셀별 대조 · `PYTHONDONTWRITEBYTECODE=1`.

## §02 → §03

**03절 주제**: 「LLM judge로 궤적 평가」(experiment, 챕터 리드 결정 1 — **앞 절반 모델 없음 + 뒤 절반 실제 모델**, 이 챕터에서 평가받는 에이전트를 실제로 돌리는 유일한 자리). 옛 판(`before/notebooks/03-…ipynb`·`before/_src/03-*.html`): `trace(*tools)`로 만든 **실제 = 기준** 궤적 하나를 `create_trajectory_llm_as_judge(model="openai:gpt-5.4-mini", prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE)`(문자열 — 온도·추론 설정 없음) 한 번 + `strict` 한 번 · `assert evaluation["score"] in [True, False]`(자료형) · 「프롬프트」 7/2·「루브릭」 6/2·「반환」·「지연」·「피평가」·「사전」 · b7 「절당 1달러 미만」(옛 틀).

1. **02가 남긴 자리(참으로 만들 것)**: 02 b8 「03절에서는 코드 규칙 대신 평가 모델(judge)이 궤적을 읽고 판정합니다. 실제 에이전트를 한 번 실행해 만든 궤적도, 이 절의 모드와 평가 모델로 함께 판정합니다」·02 정리 끝 → **03 뒤 절반은 실제 에이전트 궤적을 02의 모드(결정적)와 평가 모델로 함께 판정해야 참**. 01 b6·b7·정리 「뜻이 같은지 보려면 … 03절에서 궤적을 평가 모델로 판정합니다」도 03이 받음(챕터 공통 「03 설계」 끝줄). 02가 보인 것(네 모드·짝짓기 횟수·인자 비교 방식·덮어쓰기)은 「02절에서 본 것처럼」으로 되풀이하지 않음.
2. **앞 절반(모델 없음) — 맞춰 보기와 평가 모델이 보는 것의 차이**: 01 「답만 틀림」 궤적(`strict` 참 — 모드는 메시지 글을 보지 않음, 01 5절)과 02 궤적 하나(예: 차례 바꿈·검색 세 번)를 평가 모델에 넣을 **요청 글 모양**(설치판 `agentevals/trajectory/llm.py` 77~95행 `_format_inputs` — `<user>`·`<assistant><tool_call>`·`<tool><tool_result>` 태그 글)을 출력해 「평가 모델은 답 글·도구 결과 글까지 읽는다 ↔ 모드는 요청 이름·인자·메시지 수만 본다」를 보임. 평가 함수 **만들기**까지만(요청 0) — `create_trajectory_llm_as_judge(judge=model, prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE)`. 결과 모양은 설치판 소스로만: `{'key': 'trajectory_accuracy', 'score': 참·거짓, 'comment': 판정 까닭, 'metadata': None}`(openevals 0.2.0 `llm.py` 70~117행, 칸 `reasoning` → `comment`) — 앞 절반에서는 「노트북에서는 아직 부르지 않았습니다」.
3. **뒤 절반(실제 모델)**: 모델 셀 `nbkit.key_and_model_cells("openai:gpt-5.4-mini")`(`temperature=0`·`reasoning_effort="none"`, 키는 루트 `.env`) → 도구 둘 `search_documents(query: str)`·`check_source(doc_id: str)`를 평범한 `@tool` 함수로(결과 글은 01·02 `tool_results` 글 — Ch 19 01 `: str` 선례, 임베딩 없음) → `create_agent(model, tools=[…], system_prompt=…, middleware=[ModelCallLimitMiddleware(run_limit=N, exit_behavior="end")])`(Ch 21 01·Ch 22 04 — 작은 호출 한도, invoke 한 번마다 셈) 한 번 → 결과 `messages`가 실제 궤적 → **02 모드로 판정(결정적 — 같은 궤적이면 늘 같음)** + **평가 모델 판정(`judge=` 과정 표준 모델 객체 — 흔들림)**. 요청 수 셈은 Ch 26~28 「도구를 요청한 응답 수 + 1」(에이전트) + 평가 한 번에 요청 1번(평가 모델, 따로 셈).
4. **실제 궤적의 인자 — 02 값 바꿔 보기를 쓸 자리**: 모델이 쓴 검색어는 기준 「도서 대출 기간」과 다를 수 있음(흔들림 — Ch 21 06 기록의 검색어도 「책 대출 기간」 등). 02 7절처럼 기본 `exact`면 인자 하나만 달라도 네 모드 모두 거짓 → **검색 도구만 덮어쓰기 `{"search_documents": "ignore"}`**(02에서 `검색어가 다름: True`·`출처 문서가 다름: False`)로 견주면 검색어 흔들림을 빼고 차례·출처 문서 ID만 봄. 쓰면 「02절에서 본 것처럼」 한 문장 + 까닭(검색어는 모델이 고르는 값).
5. **흔들림(규격 §2-7 9·10번 끝)**: `03-probe.md` §0(판단 규칙·그림 라벨 규칙)을 **첫 요청 전에** 적음 → 노트북에 넣을 요청마다 노트북 밖 **5번**(에이전트 궤적 5번 — 도구 차례·요청 수가 같은지, 평가 모델 5번 — 같은 궤적에 점수가 같은지) → 새 커널 두 번. **옛 기록이 이미 갈림**: 같은 입력(실제 = 기준)에 저장 노트북 `True`(2026-09-10) ↔ 옛 검증 기록·`집필점검표.md`·옛 생성기 `DETAILS` `False`(2026-09-11, 「질문이 모호한데 대출 주제를 임의로 골랐다」). 결론·그림·정리·복습에는 결정적 값(02 모드 판정·요청 수 셈)과 「5/5·두 커널 같음」인 평가 모델 점수만(한정어), 판정 까닭 글·흔들린 점수·토큰·비용은 결과 읽기 둘째 단락·b6 표·b7에만. 원하는 점수가 나올 때까지 다시 돌리지 않음.
6. **옛 판에서 고칠 것**: 문자열 `model="openai:…"` → `judge=` 모델 객체(설치판은 문자열이면 `init_chat_model(model=model)`만 — openevals `llm.py` 254행, 게이트 G4가 못 봄) · `assert evaluation["score"] in [True, False]`(자료형만 — 모델 판단에 기대지 않으니 허용 범위지만, 모드 판정처럼 결정적 값에만 거는 01·02 방침과 맞춰 판단) · 평가 모델 점수·판정 까닭에 `assert` 금지 · b7 「절당 1달러 미만으로 예상」(옛 틀) → 실제 요청 수·요금표 어림(2026-09-17 mini 입력 0.75·캐시 입력 0.075·출력 4.50달러/100만 토큰, 청구 금액 아님).
7. **말**: 「judge」·「LLM judge」는 **제목에만**, 본문은 Ch 15 01 「평가 모델(judge)」(원어 괄호 첫 자리) · 「프롬프트」 → 「판정 머리글」(코드 이름 `TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE`는 백틱)·「요청 글」 · 「루브릭」 → 「판정 기준」(머리글의 기준 네 줄: 단계 사이 논리·진행·상대적으로 도구를 덜 부르는 쪽·기준과 뜻이 같음 — 「효율」 금지) · `comment` → 「판정 까닭」(Ch 21 06 「까닭:」) · 「피평가」 → 「평가받는 에이전트」 · 「판정 모델」 금지. 02가 정한 말(짝짓기·인자 비교 방식·도구별 덮어쓰기·모드 넷 풀이)은 그대로 이어 씀. 판정 까닭은 영어로 옴 — 결론에 쓰지 않음.
8. **도구 파일 `eval_tools.py` 02판(`4a3d81431a29d0a62d33e13766f0c57652a85fd5a4e87de6e7df9bfc9a1e58bf`)**:

| 함수 | 배운 곳 | 인자 | 03에서 |
|---|---|---|---|
| `tool_call_names(response)` | Ch 19 04(Ch 21 판) | 모델 응답 하나 | 에이전트 궤적의 첫 응답 도구 이름 |
| `show_messages(messages)` | Ch 19 06(Ch 21 판) | 메시지 목록 | 실제 에이전트 궤적 한 줄씩 보기 |
| `make_trajectory(question, calls, results, answer)` | Ch 29 01 | 질문·요청 목록·결과 글 딕셔너리·답 글 | 앞 절반 코드로 만든 궤적·기준 궤적 |
| `called_tool_names(messages)` | Ch 29 01 | 메시지 목록 | 실제 궤적의 도구 차례 |
| `trajectory_pass(messages, reference, evaluator)` | Ch 29 01 | 궤적·기준 궤적·평가 함수 | 모드 판정 칸 `score`(평가 모델 결과도 같은 칸 이름 `score` — 그대로 쓸 수 있음) |

   - 가져오기 줄 `from langchain.messages import AIMessage, HumanMessage, ToolMessage` → **03 설치 셀에 `langchain==1.4.0` 필수**(규격 §2-7 6번) + 모델 절이라 `langchain-openai==1.6.0`·`python-dotenv==1.2.3`(잠금 판, 챕터 공통 10번).
   - **02 노트북에만 있는 함수**: `four_modes(messages, reference, evaluators)`(모드 이름 키 점수 딕셔너리) · `unpaired_names(names, other_names)`(이름만 두 방향 짝). 03이 다시 쓰면 **02 셀 글 그대로** 도구 파일에 더함(주석 `# Ch 29 02절에서 배웠습니다 — 02절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다`) — `four_modes`는 `trajectory_pass`를 부르므로 같은 파일 안에서 풀림. 02 노트북 전역 `evaluators`·`reference` 등은 도구 파일에 넣지 않고 인자로.
   - **생성기 대조 사슬**: `import author_02` → `author_02.check_tools()`(안에서 `author_01.check_tools()`까지) → `author_01.strip_later_imports(03판).startswith(author_01.strip_later_imports(author_02.TOOLS))` → 더한 셀 글 해시·02 노트북 디스크 셀·AST 대조. 가져오기 줄을 더하면 머리 설명과 첫 `# Ch` 주석 사이(주석 줄은 `# Ch`로 시작하지 않게 — `strip_later_imports`가 첫 `\n\n# Ch `까지 뺌). 쓰기 가드: 없거나 01·02판·03판일 때만 쓰고 더 긴 판은 `skip`. **01·02 생성기는 03판을 덮어쓰지 않음**(01은 `strip` 뒤 01판으로 시작하면 `skip`, 02는 `later_version`이면 `skip` — 02 가드 확인함).
9. **설치판에서 확인할 것(03 준비)**: `create_trajectory_llm_as_judge`(`agentevals/trajectory/llm.py` 98~150행) 인자 `judge=`·`prompt=`·`continuous`·`choices`·`use_reasoning` · 요청 형식은 `with_structured_output` → `json_schema`(평가 한 번에 요청 1번, 준비 노트 §6-2 `e3_struct.py`) · 결과 칸 `score`는 참·거짓(기본). 준비 노트 확인 스크립트 `/tmp/ch29-prep/exp/e2_judge.py`·`e3_struct.py`(가짜 키로 만들기만, 요청 0)를 다시 돌려 볼 수 있음. 에이전트 결과 `messages`를 모드·평가 모델에 그대로 넣을 수 있음(02와 같은 `outputs=`·`reference_outputs=` — `create_agent`의 결과 `messages`에 시스템 메시지가 들어가는지, 들어가면 기준 궤적과 메시지 수가 어긋나 `strict`가 거짓이 되는지를 이 판에서 노트북 밖에서 먼저 확인할 것 — 02는 확인하지 않음).
10. **b3·b10 새로**: b3 = 01(세 평가·답만 틀림 `strict` 참)·02(네 모드·인자 비교 방식·덮어쓰기) + Ch 15 01 평가 모델(judge)·02 판정 머리글·03 치우침 + Ch 21 01 `create_agent`(모델 객체)·06 판정 여섯 모두 1 + Ch 22 04 호출 한도 · b10 = LangChain Agent evals(평가 모델 판정 — 확인일 새로)·openevals/agentevals 설치판 행(`llm.py` 27~71 머리글 둘·77~95 `_format_inputs`·openevals `llm.py` 70~117·254). 옛 참고 자료 둘(2026-09-11)을 그대로 두지 않음.
11. **그림·비유**: Mermaid 3~5(요청 글 모양·모드 ↔ 평가 모델이 보는 자리·실제 궤적 → 두 판정·요청 수 셈) + 삽화 1 — 오르골 계열 후보 「검사대 위에 두 띠를 겹쳐 비추는 판」(사람 없이, **Ch 15 저울 피함**, 01 소품 상자·돋보기와 02 소품 「띠 다섯 줄·둥근·네모·세모 구멍」 되풀이 금지). 색: **보라 = 03 뒤 절반에서 실제로 부른 모델만**(에이전트 모델·평가 모델), 앞 절반은 회색 점선(부르지 않은 평가 모델), 빨강 0. 흔들린 값(판정 까닭·흔들린 점수)은 그림 라벨에 넣지 않음 — `03-probe.md` §0 라벨 규칙을 먼저.
12. **기록**: `03-probe.md`(§0을 첫 요청 전에) · `03-diagnosis.md`·`03-figures.md`(렌더 전)·`집필점검표.md`·`qa/verification.md` 행 · 이 파일에 「§03 → §04」(04 계약 대조표는 위 「04 계약 대조표」 — 04가 도구 파일을 가져오면 `langchain` 설치 필요) · 보호 파일 대조(`manifest-changes.md` 「02절 뒤」에 이어 덧붙임) · 새 커널 두 번(A·B, B는 그림 전 — 모델 절이라 요청 수·출력이 흔들릴 수 있음, 결정적 값·5/5 값만 대조 결론에) · `PYTHONDONTWRITEBYTECODE=1`(도구 파일 가져오기 pyc 0) · 첫 실행 전 기기 사본으로 한 번(`.failure.json` 방지 — 모델 절이면 요청 수가 늘어나니 사본 실행 요청도 셈에 넣음).

## §03 → §04

**04절 주제**: 「운영 지표와 Ch18 궤적 비교」(experiment, 챕터 리드 결정 1 — **모델 없음**, 요청 0, 키 셀 없음, 이 챕터 본문 마지막 절). 옛 판(`before/notebooks/04-…ipynb`·`before/_src/04-*.html`): 셀 9 · `find_project_root`(별표 풀기 `[Path.cwd(), *Path.cwd().parents]`·힌트·`raise FileNotFoundError`) + `커리큘럼_v6.html` `assert` · Ch 18 06 **저장 출력**의 `" | "` 줄 읽기 · Ch 21 06 계약 파일 읽기 · 공통 칸 `final_score`·`model_calls`·`tool_calls`·`tokens`·`latency_s` · `nearest_rank_p95(values: list[float])`(새 이름) · 내포식·제너레이터 식 14(c16 하나에 다섯) · f-string 둘 · `statistics.mean`·`all`·`max`·`round` 다섯 · `.get` 셋 · 튜플 대입 여섯 칸 · 옛 인용값(위 「04 계약 대조표」).

1. **03이 남긴 자리(참으로 만들 것)**: 03 b8·정리 「04절에서는 모델을 부르지 않고, 앞 챕터가 저장한 실행 기록을 읽어 운영 지표를 견줍니다」 → **04는 모델 요청 0, Ch 18 06·Ch 21 06 기록을 읽기만 하고, 운영 지표(요청 수·도구 요청 수·토큰·걸린 초 등)를 견줘야 참**. 03이 보인 것(평가 모델 판정·요청 수 셈 「도구를 요청한 응답 수 + 1」·평가 모델 요청은 따로 셈·에이전트 한 번 요청 3)은 「03절에서 본 것처럼」으로. Ch 21 06 `agent_usage.model_calls` = 2(세 질문)는 도구 요청 1 + 1과 맞음 — 03 셈을 그대로 적용할 수 있음(결정적 읽기).
2. **계약 — 읽기만(다시 실행·다시 쓰기 금지)**: Ch 21 06 `labs/part6/ch21-create-agent/data/rag-comparison.json`(**`25cfe5df3cfd729c130bce4af26c716cfcc3bcd4b4ff6e4a9d0a725816b02f51`**, 03 작업 뒤 다시 확인 — 같음) · Ch 18 06 `labs/part5/ch18-workflow-patterns/notebooks/06-같은-과제로-다섯-패턴-비교.ipynb`(**`5ba7f5a01fa8a8625a4673e6f6a007691907078b20c41ee828aa266252ba0b20`**, 같음 — 셀 49 **저장 출력**의 `" | "` 줄에서 머리 `pattern` 뺀 마지막 다섯, 여섯 칸; Ch 18 06 b7 「Ch 29 04절이 저장된 출력에서 읽습니다」가 참이려면 파일이 아니라 저장 출력을 읽는 모양 유지). 읽는 칸과 만든 쪽은 위 「04 계약 대조표」.
3. **옛 인용값 → 새 값(챕터 공통 대조표, 지금 파일로 셈)**: Ch 18 다섯 패턴 평균 **0.96 · 2.8 · 862.2 · 4.206**(옛 0.88·2.8·610.2·4.145) · Ch 21 세 줄 평균 **1.0 · 2 · 1 · 688 · 1.731**(옛 1.0·2·1·519.7·1.880) · p95(가장 가까운 자리 방식, 셋이면 최댓값) **2.003 · 699**(옛 2.094·541) · 10행 복습 3 해설 **2.003** · 노트북 Ch 18 표 줄 **5**(옛 저장 출력 6). `_src/04-…` 6·7·9·10행이 옛 값 — 04가 새 출력으로 다시 씀.
4. **학생 묶음에서 멈추는 파일 찾기 → 과정 표준 파일 위치 셀**: 옛 `find_project_root`가 `textbook/`을 찾고 `커리큘럼_v6.html`을 `assert` → `part6-practice.zip`에는 둘 다 없어 `FileNotFoundError`(준비 노트 §2 04·§11-1). Ch 19~21 모양(Ch 21 `author_06.py` 86~92행 `ROOT_FIND` — `candidates = [".", "../../..", "../../../.."]` + `for`·`break` + `os.path.exists(candidate + "/labs/…")` + `assert root_path is not None, …`)으로, **묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리**에서 같은 파일을 찾게. 확인은 묶음을 `/tmp`에 풀어 그 셀을 돌려 봄(규격 §7-2, Ch 9 06). zip 다시 만들기는 마감.
5. **모델 없음·키 셀 없음**: 설치 셀은 04가 쓰는 패키지만(잠금 판). **04가 도구 파일을 가져오면 `langchain==1.4.0`을 설치 셀에 꼭**(도구 파일 03판이 `from langchain.messages import …`를 가져옴 — 규격 §2-7 6번; 01~03은 모두 있음, 03 진단 §9). 04가 도구 파일의 `sum_usage`·`estimate_cost`를 쓸 일은 적음(기록 파일에 메시지 목록이 없음) — 쓰지 않으면 가져오지 않아도 됨.
6. **걸린 초·토큰은 한정과 함께 표·둘째 단락에만**: 두 기록이 각각 **한 번 실행한 값**(앞 챕터를 다시 실행하면 바뀜)이라는 한정을 표 머리·결과 읽기 둘째 단락·b7에. **초로 순위를 매기지 않음**(규격 §2-7 9번 끝·Ch 25·26 선례). **결론은 세는 값**(요청 수·도구 요청 수·줄 수·성공 여부·`agent_supported`) — 03이 보인 「요청 수 = 도구를 요청한 응답 수 + 1」로 Ch 21 줄(`model_calls` 2 = `tool_calls` 1 + 1)을 읽을 수 있음.
7. **Ch 18 `tool_calls: 0`은 손 값** — 옛 04가 상수로 넣음(Ch 18 06 기록에 도구 칸 없음). 공개(「Ch 18 기록에는 도구 칸이 없어 0으로 적었다」 한 문장)하거나 기록에서 끌어내기(도구 호출 API를 안 쓴 워크플로우라는 Ch 18 요약 사실). **품질 칸 뜻**: Ch 18 `quality/5` = 코드 검사 0~5 ↔ Ch 21 `agent_supported` = 평가 모델 판정 참·거짓 — 한 칸에 담으면 척도가 다르다고 밝힘(03 용어 「평가 모델」·「판정」을 이어 씀).
8. **Ch 15 06 `nearest_rank`는 도구 파일에 원본 글자 그대로**: `labs/part4/ch15-evaluation-advanced/notebooks/06-대화당-비용-백분위수.ipynb` 1095행 `def nearest_rank(values, percent):`의 셀 주석·본문 그대로(주석 `# Ch 15 06절에서 배웠습니다 — Ch 15 06절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다` 꼴 — Ch 28 `spec_length` 선례) + 대조 사슬(`import author_03` → `author_03.check_tools()` → `strip_later_imports(04판).startswith(strip_later_imports(author_03.TOOLS))` → 셀 글 해시·Ch 15 노트북 디스크 셀·AST). `nearest_rank_p95` 새 이름 금지. `math.ceil`을 쓰면 가져오기 줄(`import math`)을 머리 설명과 첫 `# Ch` 주석 사이에(주석 줄이 `# Ch`로 시작하지 않게) — 그러면 04판을 가져오는 모든 노트북(01~04)은 `math`가 표준 라이브러리라 설치 셀 변경 없음. 쓰기 가드: 없거나 01·02·03판·04판일 때만 쓰고 더 긴 판은 `skip`(03 가드는 04판을 `skip` — `author_03.later_version`).
9. **고칠 문법**: `statistics.mean`·`all`·`max`·내포식·제너레이터 식 **14**·f-string 둘·`.get` 셋·튜플 대입·힌트·별표 풀기·`round` 다섯 한 줄 → `for`·`append`·`count = count + 1`·Ch 15 `average`(또는 손셈)·`nearest_rank`. 처음 쓰는 이름(`statistics.mean`·`all`·`max`를 남기면)은 한 문장씩. `assert`는 줄 수·`tool_calls ≥ 1`·`status` 모두 `ok`처럼 **계약 파일 구조 값**에만(Ch 21 06 b7 「줄 수와 도구 호출 수를 assert로 확인」이 참으로 남게), 걸린 초·토큰에는 걸지 않음.
10. **04 슬러그 고정**(Ch 21 06 `_src` 8행 b2 링크 `../ch29-agent-evaluation/04-운영-지표와-Ch18-궤적-비교.html`). 제목 「Ch18 궤적」은 **제목에만**(강사 확인) — Ch 18 기록에는 도구 차례가 없으므로 b2·b3에서 「Ch 18 기록은 요청 수·토큰·걸린 초·품질 칸이고 도구 차례는 없다」를 밝힘(「궤적」은 이 챕터 본문 말이지만 Ch 18 줄에는 쓰지 않음).
11. **Ch 21 06 b7 「Ch 29 04절 노트북 12~18번 셀이 이 절의 비교 기록 파일을 읽고, 줄 수와 도구 호출 수를 `assert`로 확인합니다」** — 04를 다시 쓰면 셀 번호가 바뀌어 옛 번호가 됨. Ch 21 파일은 고치지 않고 04 진단·이 파일에 새 셀 번호를 적어 **마감 몫**으로 넘김(줄 수·도구 호출 수 `assert`가 남는지는 04가 지킴).
12. **기록·그림**: `04-diagnosis.md`·`04-figures.md`(렌더 전)·`집필점검표.md`·`qa/verification.md` 행 · 이 파일에 「§04 → 마감」 · 보호 파일 대조(`manifest-changes.md` 「03절 뒤」에 이어) · 새 커널 두 번(모델 없음 — 셀별 출력이 모두 같아야 함, `04-probe.md` 없음) · `PYTHONDONTWRITEBYTECODE=1` · Mermaid 3~5(두 기록 → 같은 칸으로 옮겨 담기 · 세는 값 비교 · 95 백분위수 = 셋이면 최댓값 등) + 삽화 1(오르골 계열 후보 「길이가 다른 띠 여러 줄이 한 받침대에 걸림」 — 01 상자·돋보기, 02 띠 다섯·둥근/네모/세모 구멍, 03 겹친 띠 둘·상자 없는 오르골 기계 둘·손잡이 되풀이 금지), **보라 0**(모델 없음)·빨강 0 · 용어 「운영 지표」·「95 백분위수(가장 가까운 자리 방식 — Ch 15 06)」·「걸린 초」·「칸」, 금지어 「지연」·「스텝」·「불리언」·「열」·「필드」·「Agentic」·「판정식」·「수치」·「운영 화면」 0.

- **03이 확인한 것(04 참고)**: 03 노트북은 파일을 쓰지 않고 읽는 파일은 `.env`·도구 파일뿐 — 04 계약 파일에 영향 없음. 03 흔들림 확인에서 평가 모델 한 번 입력 약 680·출력 약 90~100토큰(노트북 밖 — **마감 B-3에서 바로잡음: 입력 679~682·출력 87~104토큰**), 에이전트 한 번(요청 3) 입력 933·출력 63(5/5 같음) — 04가 Ch 21 06 기록의 에이전트 토큰(688 평균, 요청 2)과 견줄 때 **조건이 다른 실행**(질문·도구·시스템 메시지 글이 다름)이라 한 표에 넣지 않음을 권함.

## §04 → 실습(05)

**05절 주제**: 챕터 끝 실습 절(규격 §7-2 · PLAYBOOK §3) — **04절이 본문 마지막 절**이라 이제 마감 담당이 만듭니다. 01~04 기능 2~3개를 한 작은 상황(도서관 규정 질문 — 01~03 소재)에 붙이고, 실행 1 → 값 하나만 바꾼 실행 2 → 비교. 새 문법·새 API·새 말 0, 30분 안팎, **서비스 요청 3~5번**(넘으면 까닭을 진단에 적고 강사 확인).

1. **슬러그·제목·형식**: 후보 **`05-Agent-평가-실습`** — 규격 §7-2 `{NN+1}-{챕터 이름}-실습`, 챕터 짧은 이름 「Agent 평가」(`textbook/_notebook/build_index.py` 62행 `('29', 'Agent 평가', …)`), 선례 Ch 17 `06-Agent-개요-실습` · Ch 21 `07-create-agent-실습` · Ch 26 `05-위임-구조-실습` · Ch 27 `09-DeepAgents-실습` · Ch 28 `06-MCP-실습`(모두 짧은 이름 그대로). 다른 후보 `05-에이전트-평가-실습`(본문 말 「에이전트」)은 선례와 어긋남. 제목 「Agent 평가 실습: {주제}」 · `chapter.json` `sections`에 `experiment`로 더함 · meta 「실습 30분 · 새 용어 0」 — **챕터 시수(3h·5h)에 더하지 않음**(절 meta 01~04 합 강의 3h·실습 5h 그대로, 챕터 요약에 적음) · `textbook/part6/_build_index.py` 27행 `(3, 5)` 그대로 · `_notebook/build_index.py` 절 수 4 그대로(실습 절 빼고 세는 약속) · 옛 `qa/check_scope.py` `SECTION_COUNTS` 4 ≠ 5(Ch 21 07 선례처럼 멈춤 기록만).
2. **04가 남긴 자리(05가 고칠 것)**: 04 b8 「다음 학습과 이어지는 지점」은 지금 **Part 7 Ch 30 01**을 가리킴(`author_04.py` `L_CH30_01` 문장, 노트북 정리 끝 「다음 학습은 Part 7 Ch 30 01절입니다. 그 절에서는 웹 서비스가 받을 요청과 내놓을 응답의 모양을 정합니다.」). 05를 만든 뒤 두 문장을 05로 바꿈(PLAYBOOK §3 「앞 절의 「다음 학습과 이어지는 지점」을 실습 절로」) — `author_04.py` 두 문자열을 고치고 `--src-only` + 노트북 마크다운만 옮김(04는 모델 요청 0이라 다시 실행해도 출력은 같지만, `executed_at`·해시가 바뀌므로 마크다운만 옮기는 쪽을 권함). 05의 「다음 학습」은 Ch 30 01(04가 확인한 문장을 그대로 옮길 수 있음 — Ch 30 01 `_src` b2·b3).
3. **붙일 앞 절 기능 후보(요청 3~5번 안 — 결정하지 않음)**:
   - **안 A(요청 3~4)** — 실행 1: 03 모양의 평가받는 에이전트 한 번(`@tool` 둘·`create_agent`·호출 한도 — 요청 3) → 02 도구별 덮어쓰기 네 모드(`four_modes`, 요청 0) → 04 공통 칸 한 줄(요청 수·도구 요청 수를 `sum_usage`·`tool_call_names`로 세어 03 셈 확인, 요청 0). 실행 2: 같은 궤적에 값 하나만(요청 0 — 아래 4번 (b)·(c)) 또는 평가 모델 판정 한 번(요청 1).
   - **안 B(요청 5)** — 실행 1: 에이전트 한 번(요청 3) + 모드 판정 · 실행 2: 호출 한도 하나만 바꾼 에이전트(요청 2 — 아래 4번 (a)). 두 실행의 궤적·요청 수를 04 공통 칸 두 줄로 모아 견줌.
   - 되풀이 금지(아래 7번)와 겹치지 않게 — 03 6절(답 글 하나만 틀리게 → 평가 모델만 거짓)을 실행 2로 되풀이하지 않음.
4. **실행 2의 값 하나 후보**: (a) **호출 한도 4 → 2**(Ch 22 04 `ModelCallLimitMiddleware(run_limit=…, exit_behavior="end")` — 도구 둘을 다 부르기 전에 멈추면 궤적이 기준과 달라져 모드 `superset`만 거짓 등; 한도에 닿았을 때 결과 목록 끝 메시지 모양·요청 수는 **노트북 밖에서 먼저 확인** — 03은 한도에 닿은 실행 0) · (b) **모드 하나**(`strict` → `subset` 등, 요청 0 — 02가 이미 보인 판정 표를 되풀이하지 않도록 실제 에이전트 궤적 한 줄에만) · (c) **기준 궤적의 도구 하나**(예: 기준에서 `check_source`를 뺌 — `subset`·`superset`이 갈림, 요청 0). 흔들리는 값(검색어·답 글·판정 까닭·토큰)은 결론에 쓰지 않고, 결정적 값(모드 판정·요청 수 셈)과 「노트북 밖 다섯 번·두 커널 같음」 모델 판단 값만(03 절차 — `05-probe.md` §0을 첫 요청 전에).
5. **도구 파일 `eval_tools.py` 04판(`223881ecd08b583b6625f5249122745fbdfec5feb222cf2feda50294f3d1e262`)** — 가져오기 `langchain.messages`(→ 설치 셀 `langchain==1.4.0` 필수)·`math`(표준 라이브러리):

| 함수 | 배운 곳 | 인자 | 05에서 쓸 자리(후보) |
|---|---|---|---|
| `tool_call_names(response)` | Ch 19 04(Ch 21 판) | 모델 응답 하나 | 도구를 요청한 응답 세기 |
| `show_messages(messages)` | Ch 19 06(Ch 21 판) | 메시지 목록 | 실행 1·2 궤적 보기 |
| `make_trajectory(question, calls, results, answer)` | Ch 29 01 | 질문·요청 목록·결과 글 딕셔너리·답 글 | 기준 궤적 |
| `called_tool_names(messages)` | Ch 29 01 | 메시지 목록 | 도구 차례 |
| `trajectory_pass(messages, reference, evaluator)` | Ch 29 01 | 궤적·기준·평가 함수 | 칸 `score` 하나 |
| `four_modes(messages, reference, evaluators)` | Ch 29 02 | 궤적·기준·모드 이름 키 평가 함수 딕셔너리 | 네 모드 한 줄 |
| `sum_usage(messages)` | Ch 19 05(Ch 21 판) | 메시지 목록 | 요청 수·토큰(평가 모델 요청은 안 셈) |
| `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` | Ch 6 06(Ch 21 판) | 사용량·요금 셋 | 예상 비용(청구 아님) |
| `average(values)` | Ch 15 06(노트북 셀) | 값 목록 | (쓸 일 적음) |
| `nearest_rank(values, percent)` | Ch 15 06(노트북 셀) | 값 목록·백분위 | (쓸 일 적음 — 줄 둘이면 늘 가장 큰 값) |

   - **04 노트북에만 있는 함수**(도구 파일 아님): `printed_lines_of(cell)` · `split_row(line)` · `ch18_row(parts, full_quality)` · `ch21_row(record)` · `show_row(row)` · `column_values(rows, key)`. 05가 다시 쓰면 04 셀 글 그대로 도구 파일에 더함(주석 `# Ch 29 04절에서 배웠습니다 — 04절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다`) + 대조 사슬(`import author_04` → `author_04.check_tools()` → `strip_later_imports(05판).startswith(strip_later_imports(author_04.TOOLS))` → 04 노트북 디스크 셀·AST) + 쓰기 가드(없거나 01~04판·05판일 때만). 공통 칸 한 줄을 실제 에이전트 결과에서 만들려면 `ch21_row`(비교 기록 파일 칸 이름에 묶임)보다 04 셈을 풀어 쓰는 쪽이 짧을 수 있음 — 실습 절은 「앞 절에서 쓴 이름만」.
   - 03 생성기 가드는 04판을 `skip`(확인), 04 생성기 가드는 더 긴 판을 `skip`.
6. **허용 문법 범위(01~04 끝, AST 확인)**: 01~03 목록(챕터 공통 「허용 문법 범위」) + 03 `@tool`·매개변수 `: str`·`copy()`·`format`·`startswith`·`_format_inputs` + **04가 더한 것** `with open(…, encoding="utf-8") as file` + `json.loads(file.read())`(Ch 21 06) · `os.path.exists`(자리 찾기 셀) · 글 메서드 `join`(Ch 16 01)·`splitlines`·`strip`·`split` · 음수 슬라이스 `[-5:]`(Ch 16 03) · `int(글)`·`float(글)`·**`float(참·거짓 값)`(04 첫 풀이)** · `round(…, 3)` · `sorted`(Ch 6 06·Ch 15 06) · `math.ceil`(Ch 15 06) · 딕셔너리 두 겹 읽기(`record["agent_usage"]["model_calls"]`) · 딕셔너리를 내놓는 함수(본문 8줄) · 값 `None`(모르는 값). **여전히 0**: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·`statistics`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`.items`·`+=`·기본값 매개변수·반환 힌트·대입 풀기·별표 풀기·`while`·`try`·세미콜론·`isinstance`·클래스·`async`. 호출 깊이 2 이하 · 준비 셀 밖 셀 10줄 이하 · 함수 본문 8줄 이하.
7. **금지 소품·되풀이 금지**:
   - 삽화(「오르골 종이띠」 계열, 05가 마지막): 01 닫힌 나무 오르골 상자·돋보기 둘·띠 둘 · 02 가로로 쌓은 띠 다섯·둥근/네모/세모 구멍 · 03 조금 비켜 겹친 띠 둘·상자 없는 오르골 기계 둘·손잡이 · **04 가로 나무 막대 하나·작은 고리·세로로 걸린 띠 여덟(다섯·셋 두 무리)** — 되풀이 금지. + 챕터 공통 금지 소품(도킹 포트·정거장·우주선·온실·모종판·예인선·바지선·밧줄·홈통·물방울·도미노·체스판·즉석사진·세탁기·승강 상자·전표·가마·물레·발자국·말뚝·쟁반·서랍·바구니·저울·도장·개찰구·플러그) + 04가 더한 빨래집게. 05 후보: 「기준 띠 하나에 실제 띠를 대 본 뒤 한 곳만 바꾼 띠를 다시 대 봄」(실행 1·2 — 사람 없이) 등.
   - 장면: 01 세 평가 × 궤적 넷 표 · 02 네 모드 × 궤적 다섯 표·짝짓기 횟수·인자 비교 방식 넷 · 03 궤적 글(`_format_inputs`)·답 글 하나만 틀리게 → 평가 모델만 거짓 · 04 두 기록 공통 칸 표·95 백분위수 자리 표(줄 수 3·5·19·20·100)·백분위 50. 05는 이것들을 「01~04절에서 본 것처럼」으로 짚고 되풀이하지 않음.
8. **04 b8과 05의 관계**: 04 b8은 05가 생기기 전이라 Ch 30 01을 가리킴(2번). 05 b3의 「절 | 배운 것 | 실습에서 쓰는 곳」 표에 04 줄(운영 지표·공통 칸·요청 수 셈을 기록에 적용)을 넣으면 04 b8 → 05 → Ch 30 01로 이어짐. 04의 결론(요청 수 셈이 기록과 맞음·줄이 적으면 95 백분위수 = 가장 큰 값)은 05에서 다시 셈하지 않아도 됨.
9. **용어**: 04 새 말 둘 — **운영 지표**(에이전트를 실행할 때마다 모으는 값: 요청 수·도구 요청 수·토큰 수·걸린 초·성공 여부) · **공통 칸**(서로 다른 기록의 값을 같은 이름의 칸으로 옮겨 담은 것, 기록에 없는 칸은 `None`). 이어 쓴 말: 95 백분위수·가장 가까운 자리 방식(Ch 15 06) · 걸린 초(Ch 18·21) · 품질 칸 = 코드 검사(Ch 18) · 평가 모델 판정(Ch 15·21) · 요청 수 셈(03·Ch 26~28). 05 새 말 0. 금지어 챕터 목록 그대로 + 「지연」·「열」·「필드」·「스텝」·「불리언」·「Agentic」·「판정식」·「수치」·「운영 화면」·「공통 열」 0(04 확인).
10. **걸린 초·토큰 태도(04가 정함)**: 한 번 실행한 걸린 초·토큰 수는 표·결과 읽기 둘째 단락·b7에만, 두 실행(또는 두 구조)의 순위 금지(과정 「비용·시간 순위」 금지). 05가 실행 1·2의 토큰을 견주면 「교재 출력에서는」으로 둘째 단락에만, 결론은 요청 수·모드 판정.
11. **마감 몫 전부**(05와 함께 챕터 마감 담당):
   - 실습 폴더 **README 다시 쓰기**(지금 3줄 — 「01·02·04절은 저장된 실제 궤적과 결정적 평가」는 틀림: 01·02는 코드로 만든 궤적, 04는 앞 챕터 기록 읽기) — 노트북 다섯, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 절마다 요청 수·키 필요 여부(01·02·04 키 없음·요청 0, 03 요청 5, 05 …), **04가 읽는 앞 챕터 파일 둘과 「두 절을 다시 실행하지 않음」**, 도구 파일 단락(함수 열·배운 곳·가져오는 절 01~04·`langchain`·`math`), 예상 비용(청구 아님).
   - `chapter.json` **`objectives`** 둘(「같은 평가셋과 명시적 기준으로 동작을 비교합니다」 — 「명시」 금지어·Ch 29에 평가셋 없음 · 「코드와 궤적」) → 절 본문 말로 · 절 제목 · **목차 설명** `textbook/part6/_build_index.py` 27행·`_notebook/build_index.py` 62~63행(「최종 답변·한 단계의 선택·전체 궤적을 평가하고 운영 지표를 비교합니다」 — 대체로 참, 05 반영 대조) → `_build.py`·`_build_index.py` 다시.
   - `labs/part6/continuity-guide.md` 15행(「최종 프로젝트의 평가 설계」 셋째 칸 — 대조, 보호 파일).
   - **옛 생성기 이동**(Ch 21·29 모두 마감이 되므로 이제 옮김): 공용 `textbook/part6/_author_ch21_ch29.py`(`391be055…` — 01이 막은 판) · `figures/_gen_figures.py`(`3577112d…`) → `qa/upgrade/before/generators/blocked/`(`mv -n`, 해시 기록 — Ch 21 요약·계약 §5·체크리스트 약속). `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6b_enrich.py`(`8528cb33…`)·`part6b_review_fixes.py`(`a0299166…`)는 **실행 금지·기록만**(Ch 25~29를 씀).
   - **옛 그림 삭제 승인 목록**: `figures/0N-흐름.{svg,excalidraw,caption.md}` N=1~4 열둘(사본 `before/figures/`, 본문 참조 0, 공개 목록에 줄 없음 — 03 캡션에 옛 금지어).
   - `__pycache__`: 04가 만든 것 0(모든 실행 `PYTHONDONTWRITEBYTECODE=1`). 공용 `textbook/_notebook/upgrade/__pycache__`·`checks/__pycache__`는 09-16~23 옛 파일(이 챕터 몫 아님 — 기록만).
   - **`visual.cjs`**(1280px·390px): 이 챕터 01~04 모두 절 작업에서 돌리지 않음 → 마감에서 한 번.
   - **zip**: 공개 목록 두 곳에 05 줄(도구 파일 줄은 01이 올림) → `part6-practice.zip`(`5002dce3…`) 다시 만들기(도구 파일 04판·01~05 노트북) → 묶음을 풀어 **04 첫 셀·자리 찾기 셀**(04가 새 노트북·04판으로 `notebooks/`에서 키 없이 PASS 확인 — `04-diagnosis.md` §6)·05 첫 셀 확인 → `check_bundle_execution.py`(Ch 24 01·Ch 28 01 PASS 그대로인지) → `check_delivery.py`(`llm-practice.zip` Stale 예상). **04는 모델·키 없이 도는 절이라 묶음 실행 검사 목록 후보**(전체 마감 판단).
   - **Ch 21 06 셀 번호 문장**(handoff는 b7이라 적었지만 실제는 **b10 참고 자료** — 「Ch 29 04절 노트북 12~18번 셀이 …」): 새 판은 비교 기록 파일을 읽는 셀이 **27~51**(0부터 센 노트북 셀 번호 — 옛 문장과 같은 셈법), 줄 수 `assert` 셀 27·도구 호출 수 `assert` 셀 31(코드 셀로는 13~25). Ch 21 파일(`_src`·HTML·`author_06.py`)은 이 절이 고치지 않음 — 마감에서 고칠지 판단(Ch 21 마감 판 해시가 바뀜).
   - **Ch 30 03·09 「Ch29 평가셋」**(거짓에 가까움 — Ch 29는 평가셋을 만들지 않음) · Ch 30 `_src/_generate.py` 같은 문장 — Ch 30 몫 인계.
   - **Ch 33 문장**: 04 「Ch29에서 운영 지표를 정의」 **참** · 02 「궤적 효율」 느슨함 · `data/regression-baseline.json` Ch 29 04 옛 해시(출처 기록) — Ch 33 몫 인계.
   - `.moai` 보조 스크립트 둘 기록(위) · `qa/research.md`·`technical-notes.md`·`verification.md`·`집필점검표.md` 「개선 전 판」 표시(이미 머리 문장 있음 — 확인) · `pyproject.toml` `pillow`(import 0 — 강사 확인, Ch 21 B-16처럼).
   - 과정 문서(오케스트레이터): `upgrade-contracts.md` Ch 21 06 줄(아직 없음 — Ch 21 요약 §9)·Ch 18 06 줄(98행)에 「Ch 29 04가 새 값으로 고침·`None`·공통 칸」 · 과정 요약 §5 Ch 29 용어(04: 운영 지표·공통 칸).
12. **기록**: `05-diagnosis.md`·`05-figures.md`(렌더 전)·`05-probe.md`(요청이 있으면 §0을 첫 요청 전에) · `집필점검표.md`·`qa/verification.md` 행 · 챕터 요약 `chapter-summary.md`(Part 6 마지막 챕터 — Part 6 마감 누적 문서 세 파일은 오케스트레이터) · 보호 파일 대조(`manifest-changes.md` 「04절 뒤」에 이어) · 새 커널 두 번(A·B, B는 그림 전) · `PYTHONDONTWRITEBYTECODE=1` · 첫 실행 전 기기 사본으로 한 번(모델 절이면 그 요청도 셈에 넣음).

- **04가 확인한 것(05 참고)**: 04 노트북은 파일을 쓰지 않음 · 읽는 파일은 Ch 18 06 노트북·Ch 21 계약 파일·도구 파일뿐 · 계약 파일 둘 해시 그대로 · 04판 도구 파일로 01·02 노트북 사본 23/23·27/27 같음, 03 가져오기 이름 모두 가져와짐(03은 실행 안 함).

## 실습 → 챕터 검토

**05절 `05-Agent-평가-실습`을 새로 만들었습니다**(2026-09-29). 제목은 「Agent 평가 실습: 호출 한도를 줄인 실행을 궤적과 운영 지표로 견주기」이고 `chapter.json`에 `format: experiment`로 더했습니다(`hours` 「총 8h · 강의 3h · 실습 5h」 그대로 — 실습 절 30분은 더하지 않음, 01~04 meta 합 강의 3h·실습 5h 그대로, `objectives`는 마감 몫). 기록은 `qa/upgrade/05-diagnosis.md`, 흔들림 확인은 `qa/upgrade/05-probe.md`, 그림 설계표는 `qa/upgrade/05-figures.md`(렌더 전에 적음), 검토 묶음은 `qa/upgrade/review-pack/05-Agent-평가-실습.md`입니다. 위 「챕터 공통」의 준비 셀·용어·색·비유·실행 규칙은 그대로 삽니다. 슬러그는 위 「§04 → 실습(05)」 1번 후보 그대로.

### 1. 이 절이 한 것

- **주제**: 03절의 평가받는 에이전트(도서관 질문 하나·도구 둘·시스템 메시지 글·실행 한도 20 — 03과 같은 값, 출처를 출력 줄과 b7에)를 **호출 한도 4(실행 1)와 2(실행 2)**로 한 번씩 실행하고, 두 궤적을 02의 네 모드와 04의 공통 칸으로 평가. 인계 안 B·4번 (a).
- **붙인 앞 절 기능 셋 — 모두 흐름 안에서 쓰임**: **03** 평가받는 에이전트(`@tool` 둘 03 셀 글 그대로 · `create_agent` · 셈 「요청 수 = 도구를 요청한 응답 수 + 1」 — 두 실행) · **02** 네 모드와 도구별 덮어쓰기(`four_modes` + `search_documents` `ignore` — 두 궤적) · **04** 공통 칸(칸 여섯 · `show_row` — 두 실행을 한 표에, 04 5절 모양으로 「점수가 1.0인 실행 · 셈이 맞은 실행」을 셈). 이 절이 처음 적은 함수 넷(노트북에): 조립 `run_agent(limit)`(노트북 전역 이름을 읽음) · `count_asked(messages)`(03 셈 셀의 반복문 모양) · `model_part(messages)`(마지막 메시지 사용량 `None`이면 `[:-1]` — Ch 26 05 판단) · `run_row(name, messages, usage, score)`(04 `ch21_row` 모양).
- **바꾼 값 하나**: 호출 한도 4 → 2. 한도에 닿은 끝 모양(Ch 22 04)·끝 메시지 사용량 `None`(Ch 26 04·05)은 이미 배운 것이라 **b2 「새로 볼 것」은 이 챕터의 평가(네 모드·공통 칸·요청 수 셈)가 그 실행을 어떻게 판정하는지로 한정**(Ch 26 B-7 교훈). 01~04 비교는 되풀이하지 않음.
- **뺀 것과 까닭**(b3 마지막 단락 + 진단 §2): 03 평가 모델(두 실행에 한 번씩이면 요청 7 — §7-2 3~5를 넘음) · 01 최종 답 평가(실행 1 답 글이 기준 답과 글자까지 같은지는 흔들리는 값) · 04 95 백분위수(줄 둘이면 늘 가장 큰 값) · 03 궤적 글(평가 모델을 부르지 않음).
- **새 문법·새 API·새 말 0**(01~04 노트북·도구 파일 04판과 AST 대조 — 노드·내장 이름·속성·키워드 인자·연산자·문자열 첨자 새 것 0, 가져온 이름은 도구 파일로 옮긴 `show_row` 하나, `/tmp/ch29-05/tools/inventory29.py`). `is None`은 03 키 셀·도구 파일 `estimate_cost`에 있는 모양, `[:-1]`은 04 음수 슬라이스와 같은 문법(Ch 26 05에서 설명). 점수 칸은 두 줄 모두 모드 `strict`(검색어 뺌) 판정 — 04의 「기록마다 제 잣대」와 다르다는 것을 b4·노트북 4절·b7에 밝힘. `assert`는 키 셀뿐. 파일 쓰기 0. 걸린 시간은 재지 않음.
- 코드 셀 **24**, 준비 셀 밖 셀 최대 9줄, 함수 본문 최대 8줄(`run_row`), 호출 깊이 최대 2, 코드 줄 143, 검사 문장 371, 게이트 G1~G7 **0**(챕터 전체 5/5). meta 「실습 30분 · 새 용어 0」. Mermaid 3(조립도·실행 1 실제 순서·실행 1·2 비교) + 삽화 1(재생성 0). 모델 요청 노트북 한 번 **5번**(3 + 2, 상한 6, 평가 모델 0).

### 2. 실행으로 확인한 값 (새 커널 A 03:40:54Z · B 03:41:13Z, 24/24 같음·`outputs_sha256`까지 + 노트북 밖 흔들림 확인 5회차, 모든 칸 5/5 — 챕터 요약이 인용할 수 있는 값)

- 구조(모델 없음 또는 라이브러리가 정함): `기준 궤적의 도구 차례: ['search_documents', 'check_source']`·`메시지 수: 6` · `평가 함수를 만든 모드: [...넷]` · `실행 한도: 20` · 한도에 닿으면 끝 메시지 `Model call limits exceeded: run limit (2/2)`·`사용량 기록이 없는가: True`(설치판 `model_call_limit.py` 37~60·168~208행).
- 모델 판단(흔들림 확인 다섯 번 + 두 커널): 두 실행 모두 도구 `search_documents` → `check_source`, 메시지를 차례대로 본 출력은 **호출 한도 줄 말고 한 줄도 다르지 않음** · 실행 1 `끝에서 뺀 메시지 수: 0`·`도구를 요청한 응답 수: 2`·`모델 요청 수: 3`·셈 `True` · 실행 2 `끝에서 뺀 메시지 수: 1`·`2`·`2`·**셈 `False`** · **두 실행 모두 `{'strict': True, 'unordered': True, 'subset': True, 'superset': True}`** · 공통 칸 `실행 1(한도 4) | 3 | 2 | 996 | None | 1.0`·`실행 2(한도 2) | 2 | 2 | 615 | None | 1.0` · **`점수가 1.0인 실행: 2 | 셈이 맞은 실행: 1 | 전체 실행: 2`**. → 결론 「도구를 모두 부른 뒤 한도에 닿은 실행은 답을 쓰지 못했어도 네 모드로는 통과했고, 요청 수 셈과 끝 메시지의 사용량 기록이 가려냈다」(한정어와 함께).
- **흔들리는(결론·그림·정리·복습에 안 쓴) 값**: 실행 1 답 글(기준 답과 글자까지 같음 — A·B·노트북 밖 다섯 번 모두) · 토큰 수 996·615(실행 1 입력 933·출력 63 / 실행 2 569·46, 노트북 밖과 같음) · 검색어 「일반 도서 대출 기간 며칠」(노트북은 출력하지 않음) · 예상 비용(노트북은 셈하지 않음 — 노트북 밖 토큰으로 두 실행 약 0.0016달러).
- `code_sha256` **`7dba1d37a0bd6752b6525950ff94fa84adee054a8f60d8b0857dee6d4420fce7`** · `outputs_sha256` **`2793f969c4acc6e048e02e9fb1bf89ab0551deaae10201addbf291b5d89a42eb`**(A·B 같음) · 노트북 파일 `053ab017…`(자리 표시 채움·그림 첨부 뒤).

### 3. 함께 고친 파일 (검토자가 볼 곳)

**챕터 안**
- `chapter.json` — 05절 추가(`d84d0a07` → `4e565b61`, 형식은 원래 파일과 같은 들여쓰기). **`hours`·`objectives` 그대로**.
- **도구 파일 05판**: `labs/part6/ch29-agent-evaluation/notebooks/eval_tools.py` `223881ec…`(04판) → **`d624b8f360c993e5f93d779dbf58f3ad41e60f6bd47dda2c3aecd9c5da6f0af9`** — 04 노트북 셀 `show_row` 글자 그대로(주석 `# Ch 29 04절에서 배웠습니다 — …`), 가져오기 줄 그대로. 대조 사슬 `author_05.check_tools()`(04 → 03 → 02 → 01 + 04판 해시 고정 + 04 디스크 셀·AST). 01~04 생성기 가드는 05판을 `skip`(판정 흉내로 확인) — **01~04 생성기의 도구 파일 줄은 바꾸지 않음**. 01·02·04 사본 실행 23/23·27/27·25/25 같음, 03 가져오기 이름 확인.
- **04절 마지막 문장**: 04 b8·노트북 정리 끝이 Part 7 Ch 30 01을 가리켜 05와 어긋나 **두 곳을 함께** 05로 — `mdpatch.py … 04`(생성기에 `L_05` 한 줄 + b8 문자열, 노트북 마크다운 셀 52) → `author_04.py --src-only` → `run_section.sh … 04 --no-exec`(04 게이트 0). **04 노트북 `code_sha256` `43163e6ac114…`·`outputs_sha256` `cccaacaa28da…`·`executed_at` 03:03:14Z 그대로**(셀별 출력 25/25, 메타데이터 같음, 바뀐 셀은 마크다운 하나). 04 노트북 `3c1c41fd` → `95dfbec8` · `_src/04` `fd2bf9c9` → `e120a5d4`(b8 말고 같음) · 04 HTML `1305131f` → `6f5f2a80` · `author_04.py` `370829e4` → `e0bc07da`(`L_CH30_01`은 `author_05`가 써서 둠). Ch 30 01 링크·문장은 05 b8·노트북 정리 끝으로 옮김. 01~03 HTML 바이트 같음, 챕터 `index.html` `934283ad` → `2821043d`.
- 챕터 `qa/public-files.json` — **05 HTML·05 노트북 두 줄**(`57815fa5` → `4913e24d`).
- 새 파일: 노트북 05 · `_src/05`(`7b93c106…`) · 빌드 `05-Agent-평가-실습.html`(`c6eaca34…`, `{{`·`[[` 0건) · `figures/05-1`~`05-3`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`) · `figures/05-4-끝이-다른-두-띠.{png,prompt.md,caption.md}` · `qa/upgrade/author_05.py`(`4f516b75…`) · `05-probe.md`·`05-figures.md`·`05-diagnosis.md` · `probe/probe05.py`(`978d1685…`)·`probe/probe-05-R.jsonl`(`7a5012f4…`) · `gates-wip-05-05.json`·`gates-wip-05.json`·`gates-wip-ch29-after05.json` · `review-pack/05-Agent-평가-실습.md`(04 묶음도 다시 만듦).
- `집필점검표.md` 품질 개선 표 05 행(`8fcf2bdd` → `e7bc38dc`) · `qa/verification.md` 품질 개선 검증 표 05 행(`34de337d` → `7f08c234`) · `qa/upgrade/manifest-changes.md` 「05절 뒤」 · 이 파일 맨 위 한 줄과 이 절.

**챕터 밖**
- `labs/part6/ch29-agent-evaluation/README.md` — 맨 아래 **05절 한 단락만**(`e252d099` → `8be9903b`). 옛 첫 단락은 마감 몫.
- `textbook/part6/public-files.json` — `collect_public_files.py` → **05 노트북 한 줄**(`e0052b91` → `47429ce7`, `Explicit public files: 94; prerequisites: 13`). `prerequisite-files.json` 바이트 같음.
- `textbook/part6/index.html`(`4e3d5941` → `a8c95c20`) · `textbook/downloads/part6-practice.zip`(`5002dce3` → **`f5d87d6634b2e7f4e29da651c20e378be966d17ceaa04921d5a8503d5eda81b9`**) · `textbook/part6/qa/integration-results.json`(`7a46d6c8` → `0526eb39`) — `python3 -B textbook/part6/_build_index.py` 한 번(**`Part 6: 56 verified sections; 110 bundled files`**). zip 113항목, `__pycache__`·`.pyc`·`.env`·`.venv` 0, **Ch 29 항목 아홉이 디스크와 같음**(도구 파일 05판·01~05 노트북 — 01~04 새 판이 이제 zip에 들어감). 묶음을 풀어 04를 `notebooks/`에서 키 없이 → PASS 25셀(셀 3 `../../../..`만 다름), 05 가져오기 줄 됨. `_build_index.py`는 고치지 않음.
- `textbook/_notebook/checks/notebook-contracts-part6-ch29-agent-evaluation.json` — `verify.py --chapter`가 다시 씀(`49dc8ded` → `c1ea214f`).
- **고치지 않음**: 01~03 노트북·`_src` · 04 노트북 코드·출력 · 계약 파일 둘 · `pyproject.toml`·`uv.lock` · 옛 생성기 둘·`.moai` 보조 스크립트 둘 · 옛 그림 · `labs/part6/continuity-guide.md` · Ch 21·28·30·33 파일 · `textbook/index.html` · `bundle-execution.json`·`llm-practice.zip`·`delivery-results.json` · 공용 도구·규격·과정 요약·`build_index.py`·`check_scope.py`·`check_course_continuity.py` · claude.ai 프로젝트 문서.

### 4. 검사 결과

- `run_section.sh … 05 --no-exec`: 게이트 G1~G7 **0**(챕터 전체 `gates-wip-ch29-after05.json` **5/5 PASS**), `verify.py --chapter` **`PASS 5 sections / 127 code cells (max 13 lines)`**, 빌드 HTML `{{`·`[[` 0건, SVG 셋·삽화 하나. 04 `--no-exec` 게이트 0.
- AST(`inventory29.py` 새 이름 0 · `extra_check.py` 허용 표시 둘만 · `depth.py` 최대 2) · `ban29.py` 0건 · 생성기 대조 `genmatch.py` 05 `cells 52 diff 0` · `author_05`의 `check_tools()`·`check_same_as_prev()`(03 셀 글 넷·03과 같은 줄)·`check_same_as_probe()` 통과 · `author_04.check_contracts()`(계약 파일 둘 해시 그대로).
- `check_delivery.py` — **117행 `llm-practice.zip`의 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`에서 멈춤**(알려진 일, 전체 마감 몫). `delivery-results.json` 안 바뀜(`3cc2d143…`).
- 돌리지 않음(마감 몫): `check_bundle_execution.py` · `check_scope.py`(`SECTION_COUNTS` 4 ≠ 5 예상) · `check_course_continuity.py` · `visual.cjs` · 옛 검사 넷.
- 보호 파일 217개: **192 같음 · 25 바뀜 · 없어진 파일 0** = 04절 뒤 19개(이 절이 다시 바꾼 여덟: 04 노트북·`_src`·HTML · `집필점검표.md`·`verification.md` · 공개 목록 둘 · notebook-contracts) + **이 절이 새로 바꾼 여섯**(`chapter.json`·챕터 `index.html`·실습 폴더 `README.md`·`part6/index.html`·`part6-practice.zip`·`integration-results.json`) — `manifest-changes.md` 「05절 뒤」.
- 흔들림 확인: §0 03:28:07Z(본문 03:27:54Z) → 첫 요청 03:28:14Z, 25요청, 모든 칸 5/5 → 후보 1 그대로. 삽화 `05-4` **1차 job `d4a3dc8d-ffba-49eb-9c4a-a79038f819bf` 채택**, 2크레딧(거래 03:44:07.982093Z, 잔액 2295), 저장 PNG ↔ 채택 job 픽셀 차이 0. 설계표는 렌더 전, 새 커널 두 번째 실행은 그림 전.

### 5. 챕터 마감 담당이 이어서 할 것 (「§04 → 실습(05)」 11번 마감 몫 전부 + 01~04 진단의 마감 몫 + 05가 더한 것)

1. **묶음 실행 검사**: 05가 `part6-practice.zip`을 다시 만들어 **zip 안 Ch 29는 이제 01~05 새 판·도구 파일 05판**입니다. 지금 `textbook/part6/qa/bundle-execution.json`은 옛 zip 기준이라 **옛 값**. README·`objectives`·목차 설명을 고친 뒤 `_build_index.py`를 마지막에 한 번 더 → `check_bundle_execution.py`(Ch 24 01·Ch 28 01 PASS 그대로인지) → 새 `bundle-execution.json`·zip 해시를 챕터 요약·계약 §5에. **Ch 29 04는 모델·키 없이 도는 절(묶음에서 PASS 25셀 확인)이라 묶음 실행 검사 목록 후보**(전체 마감 판단).
2. **실습 폴더 README 다시 쓰기 전체**(지금은 옛 3줄 + 05 한 단락): 옛 첫 단락 「01·02·04절은 저장된 실제 궤적과 결정적 평가」는 틀림(01·02는 코드로 만든 궤적, 04는 앞 챕터 기록 읽기) · 금지어 「결정적」·「LLM judge」 · 노트북 다섯 · `uv sync --locked` → `.venv` → `notebooks/`에서 열기 · 절마다 요청 수·키(01·02·04 키 없음·요청 0, **03 요청 5, 05 요청 5** — 03·05 `.env` 필요) · **04가 읽는 앞 챕터 파일 둘과 「두 절을 다시 실행하지 않음」** · 도구 파일 단락(05판 함수 열하나 · 배운 곳 · 가져오는 절 01~05 · `langchain`·`math`) · 예상 비용(청구 아님). 그다음 `_build_index.py`.
3. **`chapter.json` `objectives` 둘**: 「에이전트의 실행 구조를 코드와 궤적으로 설명합니다」 · 「같은 평가셋과 **명시적** 기준으로 동작을 비교합니다」(「명시」 금지어 · **Ch 29에는 평가셋이 없음**) → 절 본문 말로 + **05 실습 줄을 넣을지**(예: 「실습에서 호출 한도만 바꾼 두 실행을 네 모드와 공통 칸으로 견주고, 한도에 닿은 실행을 요청 수 셈으로 가려낼 수 있습니다」) → `_build.py`로 `index.html`까지. 챕터 제목 「실행 경로」(금지어)·절 제목 「LLM judge」·「Ch18 궤적」·「매칭」은 강사 확인.
4. **목차 설명**: `textbook/part6/_build_index.py` 27행(「최종 답변·한 단계의 선택·전체 궤적을 평가하고 운영 지표를 비교합니다.」 — 대체로 참, Ch 21·23~28 선례처럼 「…실습을 합니다」를 더할지) · `textbook/_notebook/build_index.py` 62~63행(절 수 4 — 실습 절을 빼고 세는 약속, 설명 대조)과 `textbook/index.html` Ch 29 행.
5. **`labs/part6/continuity-guide.md` 15행**(「Ch29 답변·선택·궤적 평가」 — 04·05 반영 대조, 보호 파일).
6. **옛 생성기 이동**(Ch 21·29 모두 마감이 되므로): 공용 `textbook/part6/_author_ch21_ch29.py`(`391be055…` — 01이 막은 판) · `figures/_gen_figures.py`(`3577112d…`) → `qa/upgrade/before/generators/blocked/`(`mv -n`, 해시 기록, 부르는 스크립트 0을 `grep`으로 확인). `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6b_enrich.py`(`8528cb33…`)·`part6b_review_fixes.py`(`a0299166…`)는 **실행 금지·기록만**.
7. **옛 그림 삭제 승인 목록**: `figures/0N-흐름.{svg,excalidraw,caption.md}` N=1~4 열둘(사본 `before/figures/`, 본문 참조 0, 공개 목록 줄 없음).
8. **`visual.cjs`**(1280px·390px, G8) — 01~05 HTML과 `index.html`을 한 번에(절 작업에서 모두 돌리지 않음).
9. **검사 스크립트**: `check_scope.py` `SECTION_COUNTS` ch29 4 → 5(Part 6 전체 몫) · `check_course_continuity.py` 해시 허용 목록(PLAYBOOK §4 Ch 9 교훈) · `check_delivery.py`(`llm-practice.zip` Stale 예상) · 옛 검사 넷 돌려 기록.
10. **Ch 21 06 셀 번호 문장**(b10 참고 자료 「Ch 29 04절 노트북 12~18번 셀이 …」): 새 판은 비교 기록 파일을 읽는 셀이 **27~51**(0부터 센 노트북 셀 번호), 줄 수 `assert` 셀 27·도구 호출 수 `assert` 셀 31(코드 셀로는 13~25) — 04 진단 §11. Ch 21 파일을 고칠지 마감에서 판단(Ch 21 마감 판 해시가 바뀜). **05는 04 코드 셀을 바꾸지 않아 이 번호 그대로**.
11. `pyproject.toml` `pillow`(import 0 — 강사 확인, Ch 21 B-16처럼) · `qa/research.md`·`technical-notes.md`·`verification.md`·`집필점검표.md` 옛 기록 「개선 전 판」 표시(머리 문장 있음 — 확인).
12. **`__pycache__`**: 01~05 작업이 만든 것 0(모든 실행 `PYTHONDONTWRITEBYTECODE=1`). 공용 `textbook/_notebook/__pycache__`·`upgrade/__pycache__`·`checks/__pycache__`는 09-08~23 옛 파일(이 챕터 몫 아님 — 기록만).
13. **챕터 요약 `qa/upgrade/chapter-summary.md`**(PLAYBOOK §6, Part 6 마지막 챕터): 새로 가르친 것·용어(새 용어 01 5 · 02 · 03 3 · 04 2 · **05 0**) · 도구 파일 표(05판 `d624b8f3…`, 함수 열하나) · 요청 수(노트북 한 번 01 0 · 02 0 · 03 5 · 04 0 · **05 5**, 절 작업 전체 03 40 · **05 35**) · **실습 30분은 챕터 시수에 더하지 않음** · 05 주제와 결과(위 2번) · 비유 「오르골 종이띠」 다섯 장(05 = 나무판 둘에 띠와 점 찍은 카드, 끝이 구멍 무리 ↔ 회색 종이) · `gates-after.json`(`--label after`) · 한국어 감사 3단·그림 판독 별도 세션(01~05) · 뒤 챕터 인계(아래 6번). Part 6 마감 누적 문서 세 파일은 오케스트레이터.
14. **강사 확인 대상 모음**: 01~04 진단 「강사 확인 대상」 · **05 진단 §12**(코드 셀 24 · 새 함수 넷 · 점수 칸 = 모드 `strict` 판정 · 결론을 「도구를 모두 부른 뒤 한도에 닿은 실행」으로 한정 · 평가 모델·최종 답 평가를 뺀 까닭 · **그림 바꾼 값 색을 과제 지시 초록 대신 챕터 규칙 파랑**으로 · 삽화 카드·구멍 · 제목 길이 · 슬러그).
15. 과정 문서(오케스트레이터): `upgrade-contracts.md` Ch 21 06 줄(아직 없음)·Ch 18 06 줄(98행)에 「Ch 29 04가 새 값으로 고침·`None`·공통 칸」 · 과정 요약 §5 Ch 29 용어(04 운영 지표·공통 칸, 05 새 말 0) · §7 실습 절 선례 「한도에 닿은 실행을 궤적 맞춰 보기와 운영 지표로 견줌(Ch 29 05)」.
16. **Ch 30·33 문장**(대기 챕터 — 고치지 않음, 인계만): Ch 30 03·09 「Ch29 평가셋」(거짓에 가까움 — 아래 6번) · Ch 30 `_src/_generate.py` 같은 문장 · Ch 33 04 「Ch29에서 운영 지표를 정의」 참 · Ch 33 02 「궤적 효율」 느슨함 · Ch 33 `data/regression-baseline.json` Ch 29 04 옛 해시(출처 기록).

### 6. Ch 30 작업자가 전제하면 안 되는 것 (Part 7 첫 챕터)

- **Ch 29에는 평가셋이 없습니다.** 01~03·05는 질문 **하나**(「일반 도서는 며칠 동안 빌릴 수 있나요?」)와 기준 궤적 **하나**(`search_documents` → `check_source`)만 쓰고, 04는 Ch 21 06의 세 질문(`C01`·`C05`·`C07`) 기록과 Ch 18 06 저장 출력을 **읽기만** 합니다(마감 B-16에서 고침). Ch 29는 평가셋·평가 결과 파일을 만들지 않았습니다. Ch 30 03·09의 「Ch29 평가셋으로 … 반복 평가」는 지금 판과 맞지 않습니다(평가셋·반복 평가·평가 결과 파일 없음).
- **Ch 29는 뒤 챕터가 읽는 산출 파일을 만들지 않았습니다**(노트북 파일 쓰기 0 — 01~05 모두). Ch 29 04는 Ch 18 06 노트북·Ch 21 06 `data/rag-comparison.json`을 **읽기만** 했고, 두 파일(`5ba7f5a0…`·`25cfe5df…`)은 그대로입니다. Ch 29 파일을 Ch 30이 읽는다고 전제하지 말 것(파일 계약 없음).
- **도구 파일 `eval_tools.py`(05판)는 Ch 29 실습 폴더에만 있습니다**(`langchain.messages`·`math`를 가져옴). Ch 30 실습 폴더와 잠금이 다르면 파일째 가져오지 말 것. `show_row`·`average`·`nearest_rank` 등 이름을 Ch 30이 쓴다면 그 챕터 규칙대로 다시 확인.
- **에이전트는 `create_agent` + 도구 둘(교재용 — 어떤 검색어에도 같은 글을 내놓는 검색 도구·`LIB-001`만 있는 출처 확인 도구) + 호출 한도 + 실행 한도 20**, 모델은 `gpt-5.4-mini`(temperature 0, `reasoning_effort="none"`)만 썼습니다. 웹 서버·HTTP·비동기 실행(`ainvoke`)·스트리밍·체크포인터는 Ch 29에서 쓰지 않았습니다(Ch 30 01부터 새로).
- **평가 모델(judge)은 03에서만** 두 번 불렀고(같은 모델 객체 — 자기 판정), 05는 부르지 않았습니다. 평가 모델 점수는 「노트북 밖 다섯 번과 두 커널 같음」 한정어로만 결론에 썼습니다. 판정 까닭 글·토큰은 결론 밖.
- **결론 값의 태도**: 요청 수 셈 「요청 수 = 도구를 요청한 응답 수 + 1」은 **답까지 간 실행에서만 맞고**, 도구를 모두 부른 뒤 호출 한도에 닿은 실행(05 실행 2)에서는 요청 수 = 도구를 요청한 응답 수였습니다. 한도가 끼운 끝 메시지(`Model call limits exceeded: …`)는 사용량 `None`이라 `sum_usage`에 그대로 넘기면 `TypeError` — 05는 `model_part`로 뺐습니다.
- **말**: 「궤적」·「기준 궤적」·「궤적 맞춰 보기」·모드 넷·「평가 모델(judge)」·「평가받는 에이전트」·「운영 지표」·「공통 칸」은 Ch 29 말입니다. 「매칭」(02 제목)·「LLM judge」(03 제목)·「실행 경로」(챕터 제목)는 제목에만. 「결정적」·「지연」·「측정」·「반환」·「프롬프트」는 본문 0.
- 05 소재(호출 한도 4 → 2·공통 칸 두 줄)를 Ch 30이 이어 쓴다는 약속은 없습니다. 05 b8은 「Part 7 Ch 30 01절에서는 웹 서비스가 받을 요청과 내놓을 응답의 모양을 정합니다」로만 이었습니다(04가 확인한 Ch 30 01 b2·b3와 맞음).

## 검토 반영과 챕터 마감 (2026-09-29)

별도 세션 검토 둘(`review-round1-A.md` 01~02·공통 중 6 · 하 10, `review-round1-B.md` 03~05·마감 몫 중 3 · 하 13)을 반영하고 챕터를 마감했습니다. 전체 기록은 `chapter-summary.md`, 절별 마감 기록은 각 `NN-diagnosis.md` 끝 「마감 반영 (2026-09-29)」과 `02-figures.md` 02-3 줄입니다. **[중] 9를 모두 반영**했고 **[하] 23을 모두 처리**했습니다(19건 고침 · A-7 일부 반영(01 셀 37은 다음 재실행) · A-14·B-15 도구 파일 머리 설명은 전체 마감 항목 · A-16 묶음 실행 검사 후보는 기록). **다시 실행한 노트북은 02·04 둘**(둘 다 모델 없음 — A·B 27/27·25/25 같음)이고, 01·03·05는 `code_sha256`·`outputs_sha256`·`executed_at`이 전후 같습니다(마크다운만 — 모델 요청 0 · 삽화 생성 0). 이 파일 위 기록 가운데 마감으로 사실이 바뀐 자리만 적습니다.

1. **위 「실습 → 챕터 검토」 §5의 마감 목록은 끝났습니다**: 실습 폴더 README 전체(`b108b2d3…` — 노트북 다섯, 절별 모델 요청 01 0 · 02 0 · 03 5 · 04 0 · 05 5, 01·02·04 키 없음·03·05 키 필요, 04가 읽는 앞 챕터 기록 둘의 묶음 안 자리와 「두 절을 다시 실행하지 않음」, 도구 파일 함수 열하나) · `chapter.json` `objectives` 둘 → 다섯(「평가셋」·「명시」를 뺌, `hours` 그대로 — `174ae411`) → `_build.py`로 챕터 `index.html` · `textbook/part6/_build_index.py` ch29 설명 줄 · `textbook/_notebook/build_index.py` Ch 29 설명(절 수 4는 그대로)과 `textbook/index.html`(Ch 29 설명만) · `labs/part6/continuity-guide.md` Ch 29 줄(뒤 칸 「Ch33 평가 회귀 검사의 궤적 기준과 모니터링 지표」) · 챕터 공개 목록은 옛 그림 줄이 원래 없어 그대로 · 옛 기록 넷(`qa/research.md`·`qa/technical-notes.md`·`qa/verification.md`·`집필점검표.md`) 머리에 「개선 전 판」 표시, 뒤 둘은 끝 「마감」 절 · 옛 생성기 둘(공용 `textbook/part6/_author_ch21_ch29.py` `391be055…`·`figures/_gen_figures.py` `3577112d…`) → `qa/upgrade/before/generators/blocked/`(`mv -n`, 해시 같음, 부르는 스크립트 0) · `part6-practice.zip` **`6d746be1…`**(Ch 29 아홉 항목·Ch 21 06 기록·Ch 18 06 노트북·continuity-guide가 디스크와 같음 — 마지막에 한 번) · `check_bundle_execution.py` **PASS**(Ch 24 01·Ch 28 01 값 그대로, `bundle-execution.json` **`f858a5ca…`**) · 04는 새 zip을 풀어 키 없이 PASS 25셀(묶음 실행 검사 후보 — 최종 점검표 §2-17 7번) · `gates-after.json` 5/5 · `verify.py --chapter` PASS 5/127 · `visual.cjs` 12행 PASS · `chapter-summary.md`. 옛 그림 열둘·`gates-wip-*.json` 열하나·캐시·임시 폴더·`llm-practice.zip`·과정 문서 줄(9·15번)·Ch 30·33 문장(16번)은 `textbook/qa/upgrade-final-checklist.md` §2-17과 요약 §17.
2. **위 §5 6번 「`.moai` 보조 스크립트 둘은 실행 금지·기록만」**(검토 A-13 — 챕터 리드 결정): 기록만 하지 않고 두 파일 `from __future__` 줄 뒤에 설명 주석 세 줄과 `raise SystemExit(…)` 한 줄을 더해 막았습니다(옮기지 않음 — `part6b_enrich.py` → `11ffa9fa…` · `part6b_review_fixes.py` → `fea9f8c7…`, `/tmp` 사본 실행으로 종료 코드 1). 옮길지·지울지는 사용자·강사.
3. **위 §5 10번 「Ch 21 06 셀 번호 문장」**: Ch 21 06 b10을 「Ch 29 04절 노트북의 코드 셀 13~25가 이 절의 비교 기록 파일을 읽어 씁니다. 코드 셀 13과 15는 줄 수와 도구 호출 수를 `assert`로 확인합니다.」로 고쳤습니다(`_src`·`author_06.py`·HTML만 — `src_html()` = `_src` 전후 모두 참). **Ch 21 06 노트북은 이 문장이 없어 손대지 않았고 실행하지 않았습니다**(코드·출력·파일 해시·`executed_at` 같음, `data/rag-comparison.json` `25cfe5df…` 그대로). 04 마감 재실행은 코드 셀 [11]에서 출력 한 줄만 빼서 코드 셀 번호는 그대로입니다. Ch 21 요약 §9의 옛 번호·`assert` 셋은 기록이라 고치지 않았습니다.
4. **위 「용어 표」 궤적 줄**(검토 A-1 — 챕터 리드 결정): 「궤적」을 **질문에서 최종 답까지 밟은 단계의 차례 — 질문·모델 응답(도구 호출 요청)·도구 결과·마지막 답을 담은 메시지 목록 전체**로 넓혔고, 모델 응답 안 도구 호출 요청에서 도구 이름만 차례대로 모은 목록은 **「도구 차례」**로 부릅니다. 궤적 맞춰 보기의 모드는 이 메시지 목록 가운데 도구 호출 요청을 견줍니다(인자 비교 방식에 따라 인자까지). 01 b4·용어 표·비유(「띠 한 줄이 궤적」)·01-5 그림 읽기·02 [6]·그림 읽기를 고쳤고 용어 표 줄에 「마감 A-1」 표시를 했습니다. 위 「§01 → §02」 이후 「궤적 = 도구 이름 목록」처럼 읽히는 문장은 이 뜻으로 읽을 것.
5. **위 「04 계약 대조표」 「결론은 세는 값(요청 수·도구 요청 수·줄 수·성공 여부)」**(검토 B-5 — 챕터 리드 결정): 04 새 판은 **「세는 값도 한 번 실행한 값입니다」**로 가릅니다. 두 기록의 값은 모두 앞 챕터를 한 번 실행한 값이고, 노트북은 기록을 읽기만 해서 같은 값이 나오지만 앞 챕터를 다시 실행하면 바뀔 수 있습니다. Ch 18 요청 수 가운데 2·2·3은 코드가, 5·2는 모델 답이 정한 작업 수·바퀴 수에서 나왔고, Ch 21 도구 요청 수는 모델이 고른 값, 판정은 평가 모델이 한 번 내린 값입니다. 다시 실행해도 그대로인 것은 짜임새가 정한 셈뿐입니다. b1·b4 비유·새 소제목과 세 단락·b6 「이 기록에서」·표 성격 칸·확인할 점·b7·b8·복습 2·노트북 [38]·[40]·정리·04-3 칸 제목(「Ch 18 기록 다섯 줄」·「Ch 21 기록 세 줄」, 다시 렌더)·캡션을 고쳤습니다.
6. **04 3절 셀 [11]의 `executed_at` 출력**(검토 B-6 (나) — 챕터 리드 결정): Ch 18 06 노트북의 `metadata.verification.executed_at`(계약 밖 칸) 출력 줄을 빼고 04를 다시 실행했습니다. 04 `code_sha256` `43163e6ac114…` → **`4ed26b54f6ff58c1e9d96c0934eaf0d549c68defab89116c1a46d5952e921c28`**, `outputs_sha256` `cccaacaa28da…` → **`492d4e24d7f3b3e772bdd80f1f80707d773b5814624a205449c22a14104a441b`**(A 04:46:54Z · B 04:47:06Z 25/25 같음, 인용 값 바뀐 것 0). 계약은 Ch 18 06 셀 49 저장 출력의 `" | "` 줄뿐입니다.
7. **02 긴 한 줄 코드**(검토 A-7): 02 코드 셀 여섯(29·43·47·51·53·55 — 노트북 셀 번호)을 딕셔너리 키마다 한 줄·평가 함수 여러 줄로 고치고, 셀 47·55는 딕셔너리 `copy()`(Ch 18 05)로 줄 수를 지켰습니다. 02 `code_sha256` `8e80cc8d5a27…` → **`238911432b500912149f0dbdd20021d4818118517fa9ecb44c7c1c66bff183f8`**, `outputs_sha256` `ecc6f928477e…` → **`274931b425d1236a2a98cfc6f668b8a6edfdea7e369b5d27225d1c18ba25c900`**(A 04:43:56Z · B 04:44:07Z 27/27 같음 — 출력 글을 이어 붙이면 옛 판과 같고, 설치 셀의 출력이 나뉜 모양만 달라 `outputs_sha256`이 바뀜). **01 셀 37 같은 모양은 01을 다시 실행하지 않아 남음**(최종 점검표 §2-17 5번).
8. **위 「§03 → §04」 03 흔들림 확인 토큰 수**(검토 B-3): 줄 안에 「마감 B-3에서 바로잡음: 입력 679~682·출력 87~104토큰」 표시를 더했고, 03 노트북 [59]도 같은 범위로 고쳤습니다.
9. **03·05 b7의 노트북 밖 가짜 모델 근거 문장**(검토 B-8 — 챕터 리드 결정): 세 문장을 코드 사실(`sum_usage` 88~96행)·02 네 모드 뜻으로 셈한 예상·「이번에 세지/실행하지 않았습니다」로 바꿨습니다. 「모델 대신 정해 둔 응답」은 교재에 0건입니다. `03-probe.md`·`05-probe.md`의 해당 확인 기록은 노트북 밖 기록으로 그대로 둡니다.
10. **위 「실습 → 챕터 검토」 §6 첫 항목**(검토 B-16): 「04는 Ch 21 06 세 질문 기록과 Ch 18 06 저장 출력을 읽기만 합니다」로 좁혔습니다(항목 안 「마감 B-16에서 고침」).
11. **커널 폴더 문장**(검토 A-10): 다섯 노트북 모두 도구 파일 가져오기 단락을 Part 6(Ch 24~28) 두 문장 「커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다」·「교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다」로 맞췄습니다(01·03·05 마크다운만, 02·04는 재실행과 함께).
12. **목록 `copy()` 출처**(검토 A-3): 02 b3·노트북 [38]·03 b3·노트북 [51]의 출처를 Ch 2 03절로 고쳤습니다(딕셔너리 `copy()`는 Ch 18 05).
13. **Ch 30 작업자에게**: 요약 §16 — 특히 **Ch 29에는 평가셋이 없음 · Ch 29가 만든 산출 파일 없음 · 도구 파일 `eval_tools.py`는 Ch 29 실습 폴더에만 · 에이전트는 `create_agent` + 교재용 도구 둘 + 호출 한도 + 실행 한도 20 · 평가 모델은 03에서만 · 요청 수 셈은 답까지 간 실행에서만**. 05 b8은 Ch 30 01을 「웹 서비스가 받을 요청과 내놓을 응답의 모양을 정합니다」로만 이었습니다. Ch 30 03·09 「Ch29 평가셋」 문장은 요약 §17.
