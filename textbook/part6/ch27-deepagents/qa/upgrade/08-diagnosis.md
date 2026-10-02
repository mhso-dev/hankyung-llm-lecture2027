# 08절 진단 — 통합 실행과 운영 한계 (2026-09-28)

- 생성기 `qa/upgrade/author_08.py`(`cfe161ae…`) · 노트북 `labs/part6/ch27-deepagents/notebooks/08-통합-실행과-운영-한계.ipynb`(`fba43561…`, `code_sha256` `33c153ec1ba5…`, `outputs_sha256` `d88cc3b198b6…`) · `_src/08-통합-실행과-운영-한계.html`(`b4e1ea7f…`) · 빌드 HTML(`958abceb…`) · 그림 `figures/08-1~08-6` · 흔들림 확인 `08-probe.md`·`probe/probe08.py`(`d2b217cf…`)·`probe/probe-08-P.jsonl`(`4a5db64d…`) · 도구 파일 `harness_tools.py` **08절 판 `7a40d99477ca7c4371a7120e6088c3ac77ed5919300091873f214694675372ed`**(07 판 `0c4ee4f9…` + 07절 노트북 `check_citations`·`call_args` 글자 그대로).
- 형식 **experiment** 유지, 슬러그 `08-통합-실행과-운영-한계` 그대로(07절 b8·Part 6 목차 링크), 제목 「통합 실행과 운영 한계」 그대로 — b2에서 「통합 실행」·「운영 한계」를 풂. **본문 마지막 절**(b8은 Ch 28 01로 — 09 실습 절이 생기면 그 절이 링크를 고침).
- 챕터 리드 결정 M2: **앞 절반(2~5절) 모델 없음 · 뒤 절반(6·7절) 실제 모델 한 흐름(invoke 두 번 — 승인 자리에서 멈춘 뒤 이어 감)**. **새 도구 0 · 사용자 서브에이전트 0 · 디스크 쓰기 0**(자료·보고 파일은 기본 `StateBackend` 상태 칸 `files`, 체크포인터는 메모리 `InMemorySaver`).

## 1. 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 뒤(`gates-wip-08.json`) |
|---|---|---|
| 코드 셀 | 5 | **31**(준비 셋(설치·가져오기·키) + 모델 셀 하나 + 본문 스물일곱) |
| 검사 문장 | 67 | **460** |
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 3 · 3 · 2 · 1 · 5 · 7 · 3 = **24** | **0 · 0 · 0 · 0 · 0 · 0 · 0 (PASS)** |
| 코드 줄(주석·빈 줄·`%` 줄 뺌) | — | 193(설치·가져오기 준비 셀 포함, 도구 파일 함수 여섯은 가져오기) |

- **첫 실행 전** `upgrade_gates.py … --label wip-08 --section 08`: G1 0 · G2 0 · G3 0 · G4 0 · G5 0 · G6 7(긴 문장 다섯 — b3·b4·b6·b10·노트북 정리, 영어로 시작한 문장 둘 — b9) · G7 22(그림 전). G6은 실행 전 고침(`gates-wip-08-08.json` — 그 뒤 마지막 확인으로 다시 씀, 검사 문장 402 → 455). 실행 뒤 흔들리는 값 단락을 `mdpatch.py`로 채운 뒤에도 G5·G6 0, 그림 뒤 G7 0(검사 문장 460).
- AST 따로(`/tmp/ch27-01/tools/extra_check.py` 05 판): **노트북 금지 문법 0건·허용 표시 0**(데코레이터·힌트 0) · 도구 파일 `estimate_cost` `.get` 둘(허용 표시, 02 판 그대로). `try/except TypeError as error` 한 셀(5절 값 바꿔 보기 — Ch 2 05절·04절 `PATH_OUTSIDE` 선례, 「셀은 끝까지 · 실제 프로그램은 멈춤」 문장). 호출 깊이(`depth.py`) **최대 2**. 준비 셀 밖 셀 최대 10줄(`SEED`·`REPORT_AGENT`), 함수 본문 최대 7줄(`review_graph`, 주석 한 줄 뺌), 셀당 정의 하나.
- 새로 쓴 이름·모양: `FilesystemPermission(…, paths=["/sources/**"], mode="deny")`(01절 4절 모양 — `**`는 한 문장) · `create_deep_agent(…, permissions=, interrupt_on=, checkpointer=InMemorySaver())` · `agent.nodes["HumanInTheLoopMiddleware.after_model"].bound`(04절 `tools_only_graph`의 `agent.nodes["tools"].bound` 모양) · `builder.compile(checkpointer=…)`(Ch 23 01) · `get_state(config).next`·`.values`(Ch 24 01·Ch 23 01) · `result["__interrupt__"][0].value`(Ch 24 01) · **`Command(resume={"decisions": [{"type": "approve"}]})`(새 API — 5절 첫 자리에서 Ch 24 `Command(resume=답)`과 같은 점·다른 점을 풂)** · `model.profile["max_input_tokens"]`(05절). 새 함수 하나 `review_graph(agent, checkpointer)`(노트북 — 처음 가르침).
- 금지어(`ban27.py`): 노트북 설명·주석·`_src`·`.mmd`·캡션 **0건** — 걸린 24줄은 모두 거짓 양성(「체크포인터」 속 「포인터」·「프로그램」 속 「로그」 — Ch 24 마감 선례와 같음), `glob`으로 함께 잡힌 옛 그림 `08-흐름.caption.md`의 「거부」는 본문 참조 0인 옛 파일(삭제 승인 목록). 「결정적」·「최대」·「재개」·「중단」·「인터럽트」·「게이트」·「캐시」·「지시」·「반환」·「검증」 0건(「최대 반복 수」는 「반복 수 하나로 뭉뚱그리지 않고」로).
- `verify.py --chapter`: `PASS 8 sections / 232 code cells (max 13 lines)`(08 옛 노트북 16줄이 빠짐). 빌드 HTML `{{`·`[[` 0건, 인라인 SVG 5·삽화 JPEG 1. `genmatch.py`: 66셀 차이 0·`_src` 같음.

## 2. 수정 전 주요 문제 (옛 판 — 학생 본문에는 쓰지 않음)

1. **모델이 채운 인자 글에 `assert`** — `assert report.file_data['content'].strip() == 'status: complete'`(모델이 요청 글의 따옴표 안 글을 옮긴 값) · `assert denied`(모델이 둘째 쓰기를 시도했는가 — 모델 판단) · `assert result['messages'][-1].text`(규격 §3 위반).
2. **실습 폴더에 씀** — `FilesystemBackend(root_dir=LAB / 'workspace-08')` → `workspace-08/run/report.md`(실행마다 덮어씀). 준비 셀 `LAB = next(… for parent in [cwd, *cwd.parents] if …)`(제너레이터·별표 풀기).
3. **temperature 없는 모델** `init_chat_model('openai:gpt-5.4-mini')`(G4) · 안전 규칙 없음(기본 general-purpose 한도 없음) · 요청 수 세기 없음.
4. 옛 b3 「Ch 24의 사람 승인과 이 장의 permissions는 도구 실행 경계를 다룹니다」 — **Ch 24 요약 192행 부분 참**(Ch 24는 쓰기 노드 하나의 승인 지점만, 모델이 고른 도구 호출 승인·`HumanInTheLoopMiddleware` 장면 0). 옛 판은 `interrupt`를 쓰지 않고 `deny`만.
5. md 「최대 반복 수는 무한 실행을 막는 경계일 뿐」 — 「최대」 금지어 · 실행 한도·호출 한도·바퀴 한도 가운데 무엇인지 없음.
6. 내포식 둘·`'…' in str(…).lower()` 호출 겹침·한 줄 복합문·`m` · 결과 읽기 셀 0 · 제목 셀·핵심 그림 없음 · Mermaid 0 · 삽화 0 · 옛 SVG 토큰 `{{svg:08-흐름}}` · b10 여덟 절 공통 · 금지어 「경로」·「검증」·「반환」·「최대」.

## 3. 바꾼 것

- **노트북(31 코드 셀, 일곱 절)**: 1절 준비(설치 다섯 — `langgraph==1.2.11`(작은 그래프·체크포인터·`Command`) · 가져오기(도구 파일 한 줄, 함수 여섯) · 키 · 모델) → **2절(모델 없음)** general-purpose 명세(02절 셀과 같은 글) → 바깥 한도 10(03절 셀과 같은 글) → 자료 셋(07절 셀과 같은 글) → `tools_only_graph`(04절 셀과 같은 글) → 규칙 없는 Deep Agent의 작은 그래프에 손 요청 `write_file` 셋 → **3절(모델 없음)** 권한 규칙 → 보고 에이전트(한도·명세·규칙·`interrupt_on`·`InMemorySaver`, 만들기만) → 노드 여덟·`도구 수: 9`·`실행 한도: 9999` → **4절(모델 없음)** 손 요청 둘(보고 폴더·자료 폴더) → `success`·`error` → 상태 칸·새 책 소식 그대로 → 값 바꿔 보기 같은 이름 `FilesystemMiddleware` → 둘 다 `success`·글이 바뀜 → **5절(모델 없음)** `review_graph` → 승인 작은 그래프 → 손 요청 하나 → `__interrupt__`·다음 노드 `('review',)`·보고 파일 없음 → 질문 값 → 결정 목록으로 이어 감 → `success`·보고 파일 → 값 바꿔 보기 Ch 24 모양 답 `TypeError` → **6절** 실행(멈춤) → 결정 목록 만들기(코드가 넣는 승인) → 같은 스레드로 이어 감 → `show_messages` → 상태 칸·자료 그대로 → 보고 파일·`check_citations` → **7절** 도구 요청 응답 수·`task`(07절 셀 + `run_new` 한 줄) → 요청 수 셈(07절 셀과 같은 글) → 예상 비용(02절 셀과 같은 글) → 한도와 기준 넷 → 정리 셋.
- **본문 10블록** 블록 단위로 다시 씀: b2(통합 실행·운영 한계 풀이) · b3(Ch 24 01 승인 지점·`Command(resume=답)` · Ch 23 01 체크포인터 · Ch 20 03 실행 한도 · Ch 16 04·Ch 22 04 호출 한도 · Ch 17 03 바퀴 한도 · Ch 19 06 결과 상태 · Ch 2 05 `try/except` · 01~07절) · b4 비유(자물쇠 문과 막아 둔 문) + 삽화 + 「도구 실행 경계」(새 용어, 조립 표) + 08-1 + 「두 장치가 걸리는 자리」 + 「결정 목록」(새 용어, Ch 24 비교 표) + 08-3 · b5 + 08-4 · b6 구조 값 단락 + 08-2 + 값 성격 표 + 모델 판단 단락 + **「운영 한계」 표(일곱 줄)** + 바퀴 한도 단락 + 08-5 + 두 커널 문장 · b7 열 항목 · b8(Ch 28 01) · b9 네 문제 · b10 절 자료(확인 2026-09-28).
- **새 용어 2**(meta): 도구 실행 경계(Ch 24 요약이 넘긴 말 — 뜻 → 공연장 입구 → 승인 노드·권한 판정) · 결정 목록(`decisions` — 뜻 → 안건마다 찬반 표 → `{"decisions": [...]}`). 이어 쓴 말: 멈춤 표시·질문 값·사람의 답으로 이어 가기·승인 지점(Ch 24·Ch 17) · 체크포인터·스레드(Ch 23) · 결과 상태(Ch 19 06) · 실행 한도·호출 한도·바퀴 한도(용어 표) · 권한 규칙·사람 승인 미들웨어(01) · 상태 칸 `files`·파일 위치(04) · 백엔드(02) · 출처 표시·출처 확인(07). 「자료 폴더」·「보고 폴더」·「승인 노드」·「승인 작은 그래프」는 일반 말(이 절 안).
- `assert`는 키 셀 하나뿐(옛 판 `assert` 넷 뺌). 노트북 셀은 멈추지 않거나 보고 파일이 없어도 멈추지 않게 `if`로 씀(§0에서 정함).

## 4. 흔들림 확인 (노트북 밖, `08-probe.md`)

- §0(설계 결정 — 조립할 기능과 뺀 기능·안전 규칙·입력·결정·판단 규칙·그림 라벨 규칙)을 **2026-09-28T16:00:16Z에 적음**(`date -u`와 같은 명령에서 파일 쓰기) → **첫 호출 시작 16:00:24Z**(회차 기록 16:00:27Z). 그 전 15:59:27Z에 `probe08.py DRY 1`(가짜 키 글·`.env` 읽지 않음, 조립·손 요청·승인 작은 그래프만 — 요청 0). 모델 없는 탐색 `x1_shape.py`(권한·같은 이름 미들웨어·승인 작은 그래프·`edit`·결정 0개·Ch 24 모양 답)·`x2_untracked.py`(`UntrackedValue` 칸이 이어 간 invoke에서 `None`)로 모양을 먼저 봄.
- 조건 하나 × **5번**(요청 24번, 서비스 오류 0): **구조 값 5/5** · **모델 판단 값 가운데 이어 간 뒤 요청 수 밖 5/5**(멈출 때까지 `grep` → `read_file` → `write_file`(요청 3) · 멈춘 요청 `write_file` `/reports/answer.md` 하나 · `task` 0 · 다시 멈추지 않음 · 자료 그대로 · 보고 파일 있음 · 한도 안) · **이어 간 뒤 요청 수 1/5 1 · 4/5 2**(적은 보고 파일을 `read_file`로 다시 읽음 — 시스템 메시지 글이 시키지 않은 일) → **입력 그대로**(규격 §2-7 10번 끝).
- 흔들린 값: `grep` 낱말(1/5 「휴관일」 · 4/5 「무인 반납함」 — 둘 다 무인 반납함 안내 하나만 찾음) · `grep`·`read_file` 인자 · 입력 8104 ↔ 10364 · 출력 155 ↔ 187 · 캐시 입력 · 예상 비용 0.006776~0.008615(캐시 뺌). 다섯 번 같았지만 §0에서 흔들리는 값으로 정한 것: 보고 파일 글(112자)·판정(두 줄 모두 `True`)·답 글·첫 요청 입력 1920.
- **노트북 결과(사실대로)**: 두 커널 모두 이어 간 뒤 바로 답해 요청 4(노트북 밖 1/5와 같음). 결과 읽기 둘째 단락·b6 표·b7에 「노트북 밖 다섯 번 가운데 네 번은 보고 파일을 다시 읽어 요청 5」와 셈 한 문장(「다시 읽었다면 요청은 5번이 됩니다」). 전체 요청 수·이어 간 뒤 요청 수·결과 메시지 수 8·도구 요청 응답 수 3은 결론·그림에서 뺌.

## 5. 실행과 값

- 교재 출력 **A**: 생성기 16:14:33Z → `execute.py`(`run_section.sh`와 같은 명령·환경, 실행과 렌더를 두 호출로 나눔) 16:14:42Z · `PASS … 31 cells` · `code_sha256` `33c153ec1ba5…` · `outputs_sha256` `d88cc3b198b6…`. 사본 **B**(그림 전, `--tools-copy`로 디스크 도구 파일 복사 — `cmp` 같음): 16:14:59Z, 같은 `code_sha256`. **셀별 출력 대조 28/31 같음**(`cmpout.py`) — 갈린 셋: code27 보고 파일 둘째 문장(판정은 같음), code29 `입력 토큰: 8104 | 출력 토큰: 160` ↔ 8110·164, code30 `예상 비용(달러): 0.006798` ↔ 0.006821(모두 흔들리는 값). 마크다운을 채우고 그림을 붙인 뒤 디스크 노트북도 A와 31/31 같음(`code_sha256`·`outputs_sha256`·`executed_at` 그대로).
- **구조 값(결론·그림)**: `명세의 키: ['name', 'description', 'system_prompt', 'middleware']` · `바깥 호출 한도: 10` · `자료 파일 위치:` 셋 · `상태 칸 files의 파일 위치:` 셋 · `막는 일: ['write']`·`막는 파일 위치: ['/sources/**']`·`규칙의 효과: deny` · `노드:` 여덟 · `도구 수: 9` · `실행 한도: 9999` · 손 요청 둘 `success`·`error`(`Error: permission denied for write on /sources/new-books.md`) · `새 책 소식이 그대로인가: True` ↔ 같은 이름 `success`·`success`·`False` · `작은 그래프의 노드: ['__start__', 'review', 'tools', '__end__']` · `결과 키: ['messages', 'files', '__interrupt__']` · `다음 노드: ('review',)` · `멈춘 동안 보고 파일이 있는가: False` · `질문 값의 키: ['action_requests', 'review_configs']` · `멈춘 도구 요청: write_file | /reports/check.md` · `고를 수 있는 결정: ['approve', 'edit', 'reject', 'respond']` · 이어 간 뒤 `success`·`보고 파일이 있는가: True` · `받은 오류: TypeError | string indices must be integers, not 'str'` · `도구를 요청한 응답 수 + 1과 같은가: True` · 7절 `실행 한도(그래프 단계 수): 9999`·`바깥 호출 한도(invoke 한 번의 요청 수): 10`·`general-purpose 호출 한도(task 한 번의 요청 수): 2`·`요약이 켜지는 기준(토큰): 340000`.
- **모델 판단 값(흔들림 확인 5/5 + 두 커널 같음 — 「이번 실행에서는」 한정어와 함께만)**: `멈췄는가: True` · `멈출 때까지의 결과 메시지 수: 6` · 응답마다 `['grep']` → `['read_file']` → `['write_file']`(멈춤) · `멈춘 도구 요청: write_file | /reports/answer.md` · `넣을 결정 수: 1` · `다시 멈췄는가: False` · `자료 셋이 그대로인가: True`·보고 파일 있음 · `task 요청 수: 0`.
- **흔들리는 값(둘째 단락·b6 표·확인할 점·b7만)**: `결과 메시지 수: 8` · `도구를 요청한 응답 수: 3` · `요청 수: 4`(두 커널 같음, 노트북 밖 1/5) · 보고 파일 글·판정 · `입력 토큰: 8104 | 출력 토큰: 160` · `예상 비용(달러): 0.006798`.
- 걸린 시간은 재지 않음. 흔들리는 값은 `[[READ_…]]` 자리 표시로 두고 A·B 대조 뒤 `mdpatch.py`로 노트북·`_src`에 채우고, 생성기는 `FILLS` 딕셔너리를 `placeholder()`가 내놓게 바꿈(`genmatch.py` 66셀 차이 0·`_src` 같음). 채운 뒤 설명만 고친 곳(b4 비유를 삽화에 맞춤·삽화 alt·그림 읽기, b6 「이 챕터의 Deep Agent에는」)은 `--src-only`·`mdpatch.py` → `run_section.sh … --no-exec`(**다시 실행하지 않음**).

## 6. 파일 쓰기 자리 (챕터 리드 결정 3)

- 노트북·흔들림 확인 모두 **디스크 쓰기 0** — 자료 셋·손 요청 보고 파일·모델 보고 파일은 기본 `StateBackend`의 상태 칸 `files`에만, 체크포인터는 메모리 `InMemorySaver`. 임시 폴더 셀·`tempfile` 없음. 옛 판의 `workspace-08/run/report.md` 쓰기를 없앰(옛 파일은 그대로 — 마감 삭제 승인 목록).
- **실습 폴더에 쓴 것**: 08 노트북 하나와 도구 파일 `harness_tools.py`(08 판). `workspace*` 안 파일은 그대로(`find -newer 08-probe.md` 0건). 08 실행은 `PYTHONDONTWRITEBYTECODE=1`.

## 7. 안전 규칙 적용 (챕터 공통 (가)·(나))

- (가) 바깥 `middleware=[ModelCallLimitMiddleware(run_limit=10, exit_behavior="end")]` — 03절 셀과 같은 글. 한도에 닿지 않음(흔들림 확인 5번 · 두 커널).
- (나) `subagents=[helper_spec]` — 02절 셀과 같은 글(자기 한도 2). 이번 실행 general-purpose 0(`task 요청 수: 0`). 이 명세도 바깥의 `permissions`·`interrupt_on`을 물려받음(설치판 `graph.py` 664·720행 — 06 b7, 이 절 b7).
- (다) 사용자 서브에이전트 없음. **상한 = invoke 한 번마다 10 + general-purpose를 부른 횟수 × 2** — 설치판 `model_call_limit.py` 34행 `run_model_call_count`는 `UntrackedValue`라 이어 가는 invoke에서 0부터 다시 셈(노트북 밖 `x2_untracked.py` 모델 없는 확인 — 칸이 `None`, b6·b7·운영 한계 표). (라) `recursion_limit` 주지 않음. 스레드 전체를 세는 `thread_limit`은 쓰지 않음(b7 한 문장).
- 요청 수 세기: 서브에이전트가 없어 넣은 질문 뒤 `AIMessage` 수 = 요청 수(02절 셈) — 승인으로 나뉜 invoke 둘의 메시지가 같은 스레드에 쌓여 한 목록으로 셈. 기록 훅은 쓰지 않음.

## 8. 도구 파일

- **08절 판 = 07절 판 + 07절 노트북 셀 `check_citations`·`call_args`**(07 노트북 디스크 셀의 주석과 본문 글자 그대로, 위에 「Ch 27 07절에서 배웠습니다 — 07절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다」 줄). `check_citations`는 같은 파일의 `find_source_marks`(07 판)를 부름. 가져오기 줄 0(머리 설명 그대로 — 02 판으로 시작).
- 대조 사슬: `author_08.check_tools()` = `author_07.check_tools()`(07 → 06 → … → 02 + guardrails) + 08 판이 07 판으로 시작 · 함수 이름 차례(02 판 여섯 + `find_source_marks`·`check_citations`·`call_args`) · 가져오기 0 · 더한 블록 글 · 두 함수 AST가 07 노트북 셀과 같음. 쓰기 가드: 없거나 02·07·08 판일 때만 쓰고, 08 판으로 시작하는 뒤 절 판은 건너뜀(아니면 `assert`). `--tools-copy`는 디스크 판(B 실행에 씀). `author_07.py`·`author_02.py` 가드는 디스크가 제 판이 아니면 건너뜀(덮어쓰지 않음 — 07 가드는 `strip_later_imports(디스크).startswith(07 판)` 확인 뒤 skip).
- 01~07 노트북은 가져오는 이름이 그대로라 다시 실행하지 않음(`verify.py --chapter` PASS). 07 노트북은 여전히 두 함수를 노트북 셀로 가르침(처음 가르친 절).
- 처음 가르친 함수 `review_graph(agent, checkpointer)`는 노트북에 둠(09가 다시 쓰면 옮김 — 단 `StateGraph`·`FilesystemState`·`START`·`END`를 쓰므로 `tools_only_graph`처럼 도구 파일로 옮기면 가져오기가 생김). `tools_only_graph`는 04절 셀 글 그대로 다시 적음(05·06·07과 같은 판단).
- `check_same_as_prev()`: `HELPER_SPEC`·`COST`(02) · `OUTER_LIMIT`(03) · `DEF_GRAPH`(04) · `SOURCES`·`USAGE`·07 `COUNT`(07) 디스크 셀 글자 대조 + 08 `COUNT` = 07 `COUNT` + `run_new` 한 줄 + `LIMITS` 요약 셈 세 줄이 05 노트북에 있음. `check_same_as_probe()`: 명세·한도·자료·작은 그래프·자료 넣기·규칙·보고 에이전트·승인 작은 그래프·손 요청 둘·결정·이어 가기·실행 줄이 `probe08.py`에 있는지(probe의 결과 목록 이름 `msgs`만 다름 — 건너뜀 표시).
- 묶음: 도구 파일은 이미 두 공개 목록에 있음(목록 변경 0). 내용이 바뀌어 zip은 마감 `_build_index.py` 때 다시 만들 것. 설치 셀 추가 패키지 0(도구 파일 가져오기 0).

## 9. 고친 틀린 사실·과장

- 옛 「보고서 글 `status: complete`·거부 메시지·마지막 글 `assert`」 → 뺌. 권한 `deny`는 모델 없는 손 요청의 결과 상태로(`success`·`error`), 모델 실행의 값은 판정 입력·둘째 단락에만.
- 옛 b3 「Ch 24의 사람 승인과 이 장의 permissions는 도구 실행 경계를 다룹니다」(부분 참) → 새 b3 「Ch 24 01절에서는 쓰기 노드 앞의 승인 지점에서 … 이 절에서는 모델이 고른 도구 요청 앞에서 멈추는 사람 승인과, 파일 도구 안에서 요청을 막는 권한 규칙을 함께 봅니다. 두 장치 모두 도구가 실행되기 전의 경계를 다룹니다」 — 이 절이 모델이 고른 `write_file` 앞 승인(6절)·`HumanInTheLoopMiddleware` 장면(5·6절)을 보여 **참**이 됨.
- 옛 「최대 반복 수는 무한 실행을 막는 경계일 뿐」 → 7절 한도 셀(라벨에 세는 것)·b6 운영 한계 표·바퀴 한도 단락(Deep Agent에는 바퀴 한도 설정이 따로 없고 호출 한도가 막음).
- 옛 b6 「삭제·glob·서브에이전트 상속 규칙은 별도 테스트가 필요」 → 서브에이전트 물려받기는 06·이 절 b7(소스), 공식 권한 문서의 범위(내장 파일 도구만)는 b7·b10.
- 옛 b4 「종료는 … 차단 파일의 부재를 함께 검사해 판정」 → 차단 파일 부재 대신 「새 책 소식이 그대로인가」(자료 글 비교)로.

## 10. 그림

- Mermaid **5장**: 08-1(폭 791.8) · 08-2(682.6) · 08-3(751.5) · 08-4(768.0) · 08-5(642.7 — 첫 렌더 `flowchart TB` 326.1 × 904.6로 두 칸이 위아래로 쌓여 `flowchart LR`로 바꿈) — 모두 868 이하, PNG 직접 열어 확인. 보라는 08-4 모델 띠(실제로 부른 모델)만 · 08-1·08-2·08-3·08-5 보라 0 · 빨강 0(`error`·`TypeError`는 노랑). 노트북 첨부 08-1 하나(`attached 1`). 08-3 메시지 라벨의 결과 키는 `__interrupt__`의 밑줄을 뺀 「interrupt」(Mermaid 굵은 글씨 방지 — 설계표에 적음). 08-3 메모에 「첫 줄부터 다시 실행」(소스·Ch 24 사실)은 넣지 않음(노랑 메모는 출력 값만). 08-4의 이어 간 뒤 요청은 수를 적지 않음(흔들림). 라벨에 `grep` 낱말·보고 파일 글·판정 결과·답 글·토큰·비용 없음.
- 삽화 **1장** `08-6-자물쇠-문과-막아-둔-문`: **1차 job `dda8886f-345e-4ec6-854c-06fcaee23f15` 채택**(재생성 0회). 거래 16:18:13.051335Z 「Nano Banana Pro −2」 = **2크레딧**(잔액 2325 → 2323, 바로 앞 거래 15:39:26Z는 07절 몫). 작업 조회 모델 표시 `nano_banana_2`(요청 `nano_banana_pro` — 01~07과 같은 표시 차이). 원본 `949935ee…`(2752 × 1536) → 저장 1100 × 614 `5bac4451…`, 다시 받은 원본(해시 같음)을 같은 폭으로 줄여 픽셀 대조 bbox `None`·최대 차이 0. **프롬프트와 다른 점**: 널빤지 둘이 엇갈리지 않고 나란히 비스듬히 박힘 · 열쇠가 두 문 사이 틀의 고리에 걸림 → 본문 비유·alt·그림 읽기를 그림에 맞춤(「비스듬히 박아」·「자물쇠 바로 옆 고리」). 06 「열린 작은 창」과 겹치지 않게 창 대신 문. 세부 `figures/08-6-자물쇠-문과-막아-둔-문.prompt.md`.
- 옛 그림 `08-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0 — 삭제 승인 목록).

## 11. 뒤 챕터가 이 절에 기대는 문장 (고치지 않음, 참·거짓만)

- `grep -rn 'Ch *27' textbook/part6/ch2[8-9]-*/_src textbook/part7`: **1건** — Ch 28 01 b3 「Ch27에서는 파일시스템과 하위 작업 기능을 미리 조립한 하네스를 사용했습니다」 → **참**(08도 파일 도구·상태 칸으로 자료와 보고 파일을 다룸, 「하위 작업」은 06 위임 — Ch 28 개선 때 말 확인). Ch 28~29·Part 7 `_src`에 `DeepAgents`·`interrupt_on`·`HumanInTheLoopMiddleware` 0건. Ch 28 03 b3 「Ch24에서 사람이 승인해야 하는 작업 경계를 확인했습니다」는 Ch 24 문장(08과 무관).
- **Ch 24 요약 §15 192행 「Ch 27 08 b3 … 도구 실행 경계」 → 참이 됨**(위 §9). Ch 24 요약 §13-1 「모델이 고른 도구 호출을 사람이 승인하는 장면·`HumanInTheLoopMiddleware` 0건」을 이 절이 처음 보임(Ch 24 파일은 고치지 않음).
- `labs/part6/continuity-guide.md` 13행 「Ch27 파일·위임·컨텍스트 관리를 조립한 에이전트 → 최종 프로젝트의 조사 과정 구성」 → **부분 참**(08은 파일·출처 확인·권한·승인을 조립, 위임은 06에서만 — 마감 대조) · 8행 「Ch27의 컨텍스트 관리」·12행 「Ch27의 서브에이전트 위임과 완료 조건」 → 08과 무관.
- 07 b8·노트북 정리 끝 「08절에서는 앞 절들의 기능을 한 흐름에서 함께 실행하고, 운영에서 남는 한계를 봅니다」 → **참**(3·6절 조립·한 흐름, 7절·b6 운영 한계 표).
- 08 b8 「Ch 28 01절에서는 도구를 같은 프로그램 밖의 서버로 옮겨, 여러 클라이언트가 같은 방식으로 찾게 하는 MCP를 봅니다」 → Ch 28 01 b2(「기능을 별도 프로세스나 원격 서비스로 옮기고 여러 클라이언트가 같은 방식으로 발견하도록 만드는 MCP」)와 맞음. 09 실습 절이 생기면 09가 b8 링크를 고침.

## 12. 서비스 요청·비용

- 이 절 모델 요청: 흔들림 확인 **24** + 교재 출력 A **4** + 사본 B **4** = **32번**(탐색 `x1_shape.py`·`x2_untracked.py`·`DRY`는 가짜 키 글·모델 없음으로 요청 0). 임베딩 0. 요약 요청 0.
- 예상 비용(요금표 2026-09-17, 청구 금액 아님, 캐시 입력을 빼지 않은 어림): 흔들림 확인 0.041236(캐시 반영 0.014363) + A 0.006798 + B 0.006821 ≈ **약 0.055달러**. 절 1달러 한도 안.

## 13. 강사 확인 대상

1. **조립 범위**: 01 안전 규칙·04 파일 도구·07 자료와 출처 판정 + 권한·사람 승인·체크포인터. 03 할 일 목록·06 사용자 서브에이전트는 요청 수를 늘려 뺐고, 05 옮겨 두기는 기준만 표에(b4·진단 §3).
2. **사람의 답은 코드가 넣은 승인**(Ch 24와 같은 공개 — 6절 결과 읽기·b7). 사람이 고르는 화면·메시지는 만들지 않음.
3. **Ch 24 이음의 새 API**: `Command(resume={"decisions": [...]})`를 5절 첫 자리에서 Ch 24 `Command(resume=답)`과 같은 점(같은 호출·노드가 첫 줄부터 다시)·다른 점(답의 모양은 미들웨어가 정함 — 글 하나면 `TypeError`)으로 풂. 새 용어 「결정 목록」·「도구 실행 경계」.
4. **승인 작은 그래프 `review_graph`**: 조립한 에이전트의 승인 노드(`agent.nodes["HumanInTheLoopMiddleware.after_model"].bound`)와 도구 실행 노드만 든 그래프로 멈춤·이어 가기를 모델 없이 보임(04 `tools_only_graph` 모양). 거절 결정은 이 그래프가 도구 실행 노드로 곧장 가서 실제 에이전트와 다르게 실행될 수 있어 노트북에 넣지 않음(`create_agent`는 짝 도구 메시지가 없는 요청만 도구 실행 노드로 보냄 — 설치판 langchain 1.4.0 `agents/factory.py` 1953~1964행. 본문 b7은 `reject`를 「노트북에서 실행하지 않았습니다」로만).
5. **이어 간 뒤 요청 수가 흔들림**(노트북 밖 4/5는 보고 파일을 다시 읽음, 교재 출력·B는 읽지 않음) — 결론은 셈에, 전체 요청 수는 흔들리는 값.
6. **운영 한계 표**(b6, 일곱 줄) — 호출 한도가 이어 가는 invoke에서 0부터(설치판 34행 + 노트북 밖 확인), 바퀴 한도 설정이 따로 없음.
7. 코드 셀 5 → 31, 코드 줄 193(규격 상한 32 안). 준비물의 「요청은 한 번은 4번, 네 번은 5번」은 노트북 밖 기록 값.

## 14. 챕터 밖 수정·보호 파일·남은 것

- **챕터 밖 수정**: `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json`(`verify.py --chapter`가 다시 씀) · 실습 폴더 도구 파일 `labs/part6/ch27-deepagents/notebooks/harness_tools.py`(08 판 — 챕터 실습 폴더 안). 공용 도구·과정 문서·앞 챕터 파일(Ch 24·Ch 28 `_src`는 읽기만)·묶음 목록은 고치지 않음.
- 보호 파일(`before-manifest.json` 238개): `manifest-changes.md` 「08절 뒤」 참고.
- 지워야 하지만 지우지 않은 것(삭제 승인 목록): 기기 `/tmp/ch27-08/`(탐색 `x1_shape.py`·`x2_untracked.py` · `fills.py`·`reps1.json`·`reps2.json` · 흔들림 확인 원 기록 `probe/`(`probe-08-P.jsonl`·`dry.jsonl`·`run1.out`·`run2.out`) · 사본 `A/`·`B/`(B에 도구 파일 사본) · 삽화 원본 `illu/`(`orig1.png`·`orig1b.png`·`view1.png`)) · `.cache/ch27-08-view/`(그림 확인 사본 하나 — 이 절이 만듦) · `qa/upgrade/gates-wip-08-08.json`·`gates-wip-08.json`(run_section 기록) · 옛 그림 `figures/08-흐름.*` · 실습 폴더 `workspace-08/run/report.md`(옛 08이 쓴 파일) · `qa/__pycache__/` · 노트북 폴더 `__pycache__/`(앞 절, 옛 도구 파일 판의 캐시). `rm`은 한 번도 부르지 않음.

## 마감 반영 (2026-09-28)

검토 1차(`review-round1-A.md`·`review-round1-B.md`)를 글·그림·기록으로 반영했습니다. **노트북은 다시 실행하지 않았고** 코드 셀은 한 글자도 바꾸지 않았습니다(`code_sha256`·`outputs_sha256`·`executed_at` 전후 같음). 고친 방법: 생성기 문자열 치환(`.cache/ch27-close/tools/gapply.py`·`smartrep.py` — 바뀐 생성기의 `cells()` 코드 셀이 노트북과 다르면 멈춤) → 달라진 마크다운 셀만 노트북에 옮김 → `src_html()`로 `_src` → `run_section.sh … NN --no-exec`. 전체 기록은 `chapter-summary.md`.

- **B-4 [중]** 승인 작은 그래프 `review_graph`는 승인 노드 뒤 곧장 도구 실행 노드로 가서, 거절·대신 답하기 결정을 넣어도 쓰기를 그대로 실행한다는 경고를 셀 35(정의 셀 결과 읽기, 다섯 문장 단락)와 b7(새 항목)에 — 실제 에이전트는 설치판 langchain 1.4.0 `agents/factory.py` 1953~1964행에서 짝 도구 메시지가 있는 요청을 건너뜀. 마감이 노트북 밖에서 모델 없이 다시 확인(`/tmp/ch27-close/x_reject.py` — 가짜 키 글·닿지 않는 주소, 요청 0): `approve` → `success` 하나 · `reject` → 거절 `error` + `Updated file /reports/check.md` `success` · `respond` → 대신 답한 `success` + `Updated file` `success`, 세 경우 모두 보고 파일 생김.
- B-5 b3 「쓰기 앞의 승인 지점에서 … 그때 멈춘 자리는 쓰기까지 담은, 우리가 만든 노드 하나」(Ch 24 01 `ask_then_charge` — b4 표 「쓰기 노드 안의 interrupt」와 같은 뜻) · B-6 b10 Deep Agents 사람 승인 문서 항목에 「문서 예에도 이 과정에서 쓰지 않은 인자 `version`이 있습니다」 · B-9 셀 57 「07절 6절 셀에 넣은 질문 뒤만 자르는 줄 하나를 더하고, 첫 줄 주석을 바꾼 글」(단락 나눔). 셀 58 첫 줄 주석 「(07절 6절 셀에 첫 줄 run_new만 더함)」은 코드라 그대로.
- 마크다운 셀 35·57. 노트북 `ac7b0a9f` → `70decb2f` · `_src` `3cf66f38` → `724496a7` · HTML → `55577df2` · `author_08.py` `68833ee1` → `5acd93b3`(도구 파일 08 판 `TOOLS` 그대로 — `author_09.check_tools()` 통과).
