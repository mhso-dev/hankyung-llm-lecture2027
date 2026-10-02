# Ch 27 DeepAgents — Harness 계층 — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part6/ch27-deepagents`(절 여덟 — 01~08 모두 experiment) · `labs/part6/ch27-deepagents`. 바로 앞 Ch 26(완료, 모델 결정 M2)을 잇는 Part 6 일곱째 챕터입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본 63개, 937,195바이트 — 원본과 `cmp` 모두 같음, **`workspace*` 세 폴더 사본 포함**) · `gates-before.json`(`915e2c70…`) · `before-manifest.json`(238개, `0484871c…`) · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch27-deepagents`(292MB, 사용자 디스크).
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(전부) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 과정 요약(전부) · 계약 파일(`grep -n '^#'` 뒤 Ch 21~26 인계 줄·비유 계열 줄) · Ch 26 `chapter-summary.md`(전부)·`chapter-lead-notes.md`(전부)·`before-manifest.json`(모양) · Ch 21·23·24 요약의 Ch 27 줄 · Ch 22 03·08 `_src`·노트북 훅 이름 · Ch 6 01 `_src`(하네스 정의) · Ch 9 06 `_src`(실험 하네스) · Ch 23·24·26 노트북 준비 셀 · Ch 28 01 `_src` b3 · Part 6 목록·묶음·검사 스크립트 · 챕터 `qa/` 기록 넷·`집필점검표.md`. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.
- **원고·노트북·그림은 하나도 고치지 않았습니다.** 연결 폴더 안 파일 삭제 0건, 노트북 실행 0건, 서비스 모델 요청 0건, `uv cache prune` 안 함. 확인은 기기 `/tmp/ch27-prep/exp/`의 작은 스크립트(`e1_default.py`~`e6_nodes.py`)와 설치판 소스·공식 문서로 했습니다. 모델 객체는 가짜 키 글(`sk-not-a-real-key`)로 **만들기만** 했고(요청 0), 모델 응답이 필요한 확인은 하지 않았습니다. 도구 실행 확인은 손으로 만든 `AIMessage(tool_calls=…)`를 `ToolNode`에 넣는 모양(Ch 20 01 선례)이라 가짜 모델이 아닙니다. 임시 파일은 모두 `/tmp/ch27-prep/exp/` 아래.
- `chapter.json` `hours` = 「총 24h · 강의 8h · 실습 16h」. 절 meta 「강의 1h | 실습 2h」 × 8 → 강의 **8h**·실습 **16h** — 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part6/_build_index.py` 25행 (8, 16)·`qa/check_scope.py` `EXPECTED` (8,16)·`SECTION_COUNTS` 8도 같습니다. 새 용어 meta 4 × 8 = 32(옛 생성기 틀 값 — 실제 새 말 목록 없음).

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-28)

| 절 | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 하네스와 일곱 기능 | 4 | 71 | 0 | 2 | 1 | 0 | 5 | 11 | 3 | 22 |
| 02 create deep agent와 도구 | 5 | 69 | 6 | 4 | 2 | 1 | 7 | 19 | 3 | 42 |
| 03 플래닝과 시스템 프롬프트 | 5 | 75 | 3 | 1 | 2 | 1 | 7 | 15 | 3 | 32 |
| 04 파일시스템과 중간 결과 | 4 | 69 | 3 | 0 | 1 | 0 | 6 | 20 | 3 | 33 |
| 05 컨텍스트 관리와 오프로딩 | 5 | 72 | 2 | 2 | 2 | 1 | 6 | 14 | 3 | 30 |
| 06 서브에이전트 위임 | 4 | 68 | 4 | 2 | 1 | 1 | 5 | 16 | 3 | 32 |
| 07 출처 검증형 deep research | 4 | 67 | 2 | 1 | 1 | 0 | 5 | 18 | 3 | 30 |
| 08 통합 실행과 운영 한계 | 5 | 67 | 3 | 3 | 2 | 1 | 5 | 7 | 3 | 24 |
| **합계** | **36** | **558** | **23** | **15** | **12** | **5** | **46** | **120** | **24** | **245** |

- 통과 절 **0/8**. 코드 줄(`count_code.py`, 주석·빈 줄 뺌) 24·28·25·26·46·26·41·36 = **252줄**.
- G1 23 = 리스트 내포식 13(02 c10 넷 · 03 c8 둘 · 04 c8 · 05 c8 · 06 c8 셋 · 08 c8·c10) · 제너레이터 식 10(02 c10 둘 · 03 c8 · 04 c4·c8 · 05 c4 · 06 c8 · 07 c4·c8 · 08 c4). 조건 표현식·`lambda`·클래스 0.
- G2 15 = 한 글자 변수 `m` 10(02 c10 넷 · 03 c8 · 05 c8 · 06 c8 둘 · 08 c8·c10) · 한 줄 복합문 2(01 c6·08 c8 `for …: print(…)`) · 호출 두 겹 2(01 c8 `sum(features.values())` · 05 c8) · 15줄 넘는 셀 1(07 c6 16줄).
- G3 12 = 첫 줄 주석 없는 셀(준비 셀 c4 여덟 · 모델 셀 c6 넷 — 02·03·05·08).
- **G4 5 = 02·03·05·06·08 `init_chat_model('openai:gpt-5.4-mini')`에 `temperature`·`reasoning_effort` 없음. 07은 `create_deep_agent(model='openai:gpt-5.4-mini')` 문자열이라 게이트가 못 잡음 — 실제로는 여섯 절 모두 누락.** 가짜 모델 0.
- G5 46 = 절마다 제목 셀·핵심 그림 첨부 없음 16 + 결과 읽기 인용 없음 22 + 마지막 코드 셀 뒤 결과 읽기 없음 8.
- G6 120 = 70자 초과 64(8·10·8·5·7·10·13·3) · 영문으로 시작해 조사가 붙은 문장 56(3·9·7·15·7·6·5·4). §4 금지어는 G6가 대부분 세지 않음(§1 표).
- G7 24 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 것 (AST로 따로 셈, `/tmp/ch27-prep/ast_scan.py`)

- **`next(… for … if …)` + 별표 풀기 `[cwd, *cwd.parents]`**: 04·05·07·08 준비 셀 c4(과정 요약 2-2 금지 모양 그대로, 실습 폴더 위치 `LAB` 찾기).
- **f-string**: 03 c10 `f'({reduction:.1%})'`(형식 지정 — 과정 요약 2-1 「처음 쓰면 한 문장」, Ch 13~26은 f-string 0건).
- **타입힌트·데코레이터**: `@tool` 함수 넷(02 `course_lookup(chapter: int) -> str` · 05 `large_result() -> str` · 06·07 `source_lookup(source_id: str) -> str`) — 반환 힌트는 Ch 19~26 「0건」, 매개변수 `: int`는 Ch 19 선례 밖(`: str`만), 「이 줄은 아래 함수를 도구로 등록합니다」 설명 0.
- **그 밖**: `getattr(m, 'tool_calls', [])`(02·03·06 — 이중 `for` 내포식 안) · `.get` 둘(03 `result.get('todos')` · 07 `provided.get(…)`) · `all`·`any`·`sum`(01·02·03·04·06·07 — Ch 26 「쓰지 않은 것」) · 튜플 대입 `before, after = 5395, 1895`(03) · 식 안 숫자 `'근거 문장입니다. ' * 3000`·`[:500]`·`[:700]`·`< 3000`(05·06·07) · **`re` 모듈 `re.search(r'path: (/[^\s]+)', …)`**(05 — Ch 16 02 선례 모양은 `findall`·`sub`만) · `.lstrip('/')`·`relative_to(…).as_posix()`(05) · `assert A and B`(05·06) · `'…' in str(x).lower()`(06·08 호출 겹침) · **`inspect.getsource`**(01 — 과정 처음) · 딕셔너리 한 줄에 여러 칸(06·07 `researcher` 스펙) · 모델 셀·에이전트 만들기·출력이 한 셀(02·03·05·06·07·08 c6) · 준비 셀에 `%pip`·import·키·버전 출력이 섞임(규격 §2-4 준비 네 셀과 다름).

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청(한 번 실행) | 파일 쓰기와 자리 | 손 값 | 금지 문법(셀) | 금지어(`_src` b1~b9 / 노트북 md / 코드 주석) | `assert`(무엇에) |
|---|---|---|---|---|---|---|---|
| 01 | `inspect.getsource(deepagents.graph.create_deep_agent)` 문자열 안에 미들웨어 이름 일곱(`FilesystemMiddleware`·`SubAgentMiddleware`·`create_summarization_middleware`·`SkillsMiddleware`·`MemoryMiddleware`·`HumanInTheLoopMiddleware`·`AsyncSubAgentMiddleware`)이 있는지 `True` 일곱 → 합계 7 | **0**(모델·키 셀 없음, `dotenv`만 읽음) | 없음 | 없음(합계 7은 셈) | c6 한 줄 복합문·딕셔너리 13줄 · c8 호출 두 겹·`sum`·`all` · c4 첫 줄 주석 없음 | 경로 6/3/2 · 측정 2 · 검증 2/0/1 · 런타임 1(복습 3) · 표면 1/1 · 하네스 11/6(정의 필요) | 판 번호 · **`all(features.values())`(문자열 존재 — §2 01의 결함)** |
| 02 | `@tool course_lookup`(딕셔너리 `{27: 'DeepAgents 하네스'}[chapter]`) + `create_deep_agent(model=…, tools=[…])` → 그래프 노드 출력 → `invoke` → 메시지 종류·이름(`HumanMessage`·`AIMessage`·`ToolMessage course_lookup`·`AIMessage`) | **2**(저장 출력의 `AIMessage` 둘) | 없음(기본 `StateBackend` — 쓰면 상태 칸 `files`, 이번엔 안 씀) | 없음 | c6 힌트·`@tool`·모델+에이전트 한 셀 · c8 `getattr` · c10 내포식 넷·제너레이터 둘·`m` 넷·`any` | 반환 6/5/1 · 측정 2 · 명시 2/1 · 궤적 1/1 · 표면 2/1 · 시그니처 1 · 보장 1/1 · 스키마 1 | **모델의 도구 선택(흔들리는 값)** · 도구 결과 글에 `'DeepAgents'` |
| 03 | `middleware=[TodoListMiddleware()]` → 「먼저 write_todos로 두 할 일」 요청 → 호출 이름 `['write_todos', 'write_todos']`·할 일 둘 모두 `completed` / 릴리스 PR 숫자 5,395·1,895로 64.9%(65%) 다시 셈 | **3**(어림 — `write_todos`는 한 응답에 둘을 못 부르는 규칙이라 요청 둘 + 마지막 답) | 없음(할 일은 상태 칸 `todos`) | **5,395·1,895·64.9%·65%**(PR 값 — 이 실행 값 아님, b1·b2·b4·b5·b6·b7·복습 2) · `gpt-5.5` 「hello」 첫 차례 | c6 첫 줄 주석 없음 · c8 내포식 둘·제너레이터·`m`·`.get`·`getattr` · c10 f-string 형식 지정·튜플 대입 | 측정 9/2 · 프롬프트 8/3 · 검증 4/2/1 · 스키마 1 · 표면 1 · 「opt-in」 영어 | 모델 선택(`write_todos` 부름) · `todos` 있음 · `round(reduction, 2) == 0.65`(손 값) |
| 04 | `FilesystemBackend(root_dir=LAB/'workspace')`로 직접 `write`·`read`·`ls`(모델 없음) → 두 줄 읽기·가상 경로 목록 | **0**(키 셀 없음, `dotenv`만) | **실습 폴더 `workspace/research/source-a.md`(연결 폴더)** · 목록 출력 `['/research/final.md', '/research/source-a.md']` — **07이 쓴 파일이 섞임(실행 차례 의존)** | 없음 | c4 `next`+제너레이터+별표 · c8 내포식·제너레이터·`any` | **경로 19/9/2**(파일 경로 뜻 — §9-2) · 반환 4/2 · 보장 2 · 영속 1 · 메타데이터 1 · 명시 1/1 · 표면 1 | 읽은 글 머리 `'# 자료 A'` · 목록에 경로(결정적) |
| 05 | `@tool large_result`(30,000자) + `FilesystemBackend(LAB/'workspace-05')` + **`middleware=[FilesystemMiddleware(…, tool_token_limit_before_evict=200)]`(같은 이름이라 기본 자리를 바꿈 — §5-1)** → `invoke` → `ToolMessage` 길이 1653·안내 글 → `re.search`로 경로 → 파일 글 30,000자 같음 | **2~3**(도구 요청 + 마지막 답, `read_file` 여부는 출력에 없음) | **`workspace-05/large_tool_results/call_…`(호출 ID마다 새 파일 — 지금 여섯 개 쌓임)** | 200(토큰 한도) · 3000(되풀이·`assert` 기준) · **「약 1,600자」**(b6·b8·복습 2 — 한 번 실행 값) | c4 `next` · c6 14줄·힌트·`@tool`·식 안 숫자 · c8 내포식·슬라이스·`m`·호출 두 겹 · c10 `re`·`and` | 오프로딩 12/7(새 말) · 경로 9/4/1 · 반환 3/1 · 측정 3 · 검증 1/1/1 · 문맥 1 · 임계 1 | 도구 메시지 있음(모델 선택) · `len(notice) < 3000` · 파일 글 같음 · 마지막 답 글 있음 |
| 06 | `@tool source_lookup` + 서브에이전트 스펙 딕셔너리(`name`·`description`·`system_prompt`·`tools`) + `create_deep_agent(model, tools=[source_lookup], subagents=[…])` → 「task 도구로 source-reviewer에게」 → 부모 호출 `['task']`·위임 보고 앞 500자 | **4 이상**(부모 2 + 서브에이전트 2 이상 — 서브에이전트 요청은 부모 목록에 없음) | 없음 | 없음 | c6 힌트·`@tool`·딕셔너리 여러 칸 한 줄 · c8 내포식 셋·제너레이터·`m` 둘·`getattr`·슬라이스 | **반환 14/5** · **문맥 9/2** · 격리 3/1 · 관측 1/1 · 궤적 1 · 표면 1/1 · 명시 1/1 | 부모가 `task` 부름(모델 선택) · **보고 글에 `'planning opt-in'`(모델 글 속 단어 — 규격 §3 위반)** |
| 07 | 고정 자료 둘(`overview`·`release`, 영어 한 문장씩) + `source_lookup`(`.get` → `'UNKNOWN SOURCE'`) + `FilesystemBackend(LAB/'workspace')` + 서브에이전트 + **`model='openai:gpt-5.4-mini'` 문자열(Responses API·temperature 없음 — §5-2)** → 영어 요청 → 마지막 답·사용량·`/research/final.md` 앞 700자 | **어림 7~10**(부모: 위임 1~2 응답 + `write_file` 1 + 마지막 1 / 서브에이전트: 부른 횟수 × 2 안팎) | **`workspace/research/final.md`(04와 같은 폴더, 실행마다 덮어씀)** | **사용량 2,379·34·2,413**(b6·README — 한 번 실행 값, 캐시 읽기 2048) · `집필점검표.md`는 **2,498·38**(다른 실행 값, 어긋남) | c4 `next` · c6 16줄·`.get`·힌트·`@tool` · c8 `all`+제너레이터·슬라이스·`getattr` | **검증 8/2/3** · 측정 4 · 페이지 2/1 · 반환 3/2 · 프롬프트 1 · 하네스 1 · 제목 영어 「deep research」 4/1 | **파일 글에 세 제목(모델이 쓴 글 — 규격 §3 위반)** |
| 08 | `FilesystemBackend(LAB/'workspace-08')` + `FilesystemPermission(operations=['write'], paths=['/blocked.txt'], mode='deny')` + `create_deep_agent(…, permissions=[…])` → 「report 쓰고 blocked도 시도」 → 도구 메시지 `Updated file /run/report.md`·`Error: permission denied for write on /blocked.txt` → 보고서 글·마지막 답 | **2~3**(쓰기 둘이 한 응답이면 2, 따로면 3) | **`workspace-08/run/report.md`** · `/blocked.txt` 없음 | 없음 | c6 첫 줄 주석 없음 · c8 한 줄 복합문·내포식·`m` · c10 내포식·`or`·`m` | 경로 8/5/2 · 검증 4/2/1 · 반환 2 · **최대 0/1**(md 「최대 반복 수」) | **보고서 글 `== 'status: complete'`(모델이 쓴 인자)** · 거부 메시지 있음 · 마지막 답 글 있음 |

- **서비스 요청 합계(한 번 실행 어림) 약 20~24번**(01 0 · 02 2 · 03 3 · 04 0 · 05 2~3 · 06 4+ · 07 7~10 · 08 2~3). 임베딩 0. 노트북 `%pip`은 여덟 절 모두 `deepagents==0.7.0 langchain==1.4.0 langchain-openai==1.6.0 python-dotenv==1.2.3`(01·04도 같음). 실습 폴더 dev에 `pip==26.2`, 잠금에 `pip 26.2` 있음(규격 §7-2 조건 충족).
- **`temperature=0`**: 0곳. **`reasoning_effort="none"`**: 0곳. 모델 이름은 문자열 그대로(02·03·05·06·08 `init_chat_model('openai:gpt-5.4-mini')`, 07 `create_deep_agent(model='openai:gpt-5.4-mini')`).
- **걸린 시간**: 어느 절도 재지 않음. 저장된 셀 실행 기록(참고만): 모델 셀 `invoke` 02 2.2초 · 03 2.6초 · 05 2.5초 · 06 4.4초 · 07 10.2초 · 08 2.6초, `deepagents` 가져오기+에이전트 만들기 0.6~1.2초.
- **흔들리는 값 처리**: 02·03·05·06의 `assert`가 모델 선택(도구 이름)에 걸림, 06·07·08은 모델이 쓴 글·인자에 걸림(규격 §3 위반). 노트북 밖 되풀이 확인 기록 없음. 05 「약 1,600자」·07 사용량을 결론·정리·README에 씀.
- **옛 그림 토큰**: 절마다 b4 「도식 읽기」의 `{{svg:NN-흐름}}` 하나(`figures/_gen_figures.py`가 `textbook/part5/_figure.py`의 `linear()`로 만든 상자 넷 세로 흐름도) · 노트북 토큰 `{{notebook:slug}}` 여덟. Mermaid·삽화 0장.
- 노트북 `metadata.verification`: 여덟 모두 `passed`. 실행일 **2026-09-10**(01·02·03·06 16:21 UTC · 04·05·07·08 16:38~16:39 UTC). `code_sha256` 앞 12자 01 `5452a8d5efa2` · 02 `f302f7a3c451` · 03 `7b6c4edf3a6b` · 04 `8f1f81208263` · 05 `fe50b75d8ba4` · 06 `02000e813991` · 07 `c2cbe546a56d` · 08 `5e0d3c79be96`. 파일 해시 `ff1694dc…`·`22ab1526…`·`17de24d5…`·`cf642b1f…`·`3e3f95dd…`·`c05bd813…`·`992d162c…`·`543fd1cc…`(`part6-practice.zip`·`llm-practice.zip` 안 판과 같음). 셀 수 9·11·11·9·11·9·9·11. **챕터 `qa/verification.md`의 04·05·07·08 해시는 지금 노트북과 다름**(옛 판 기록).
- 노트북 설명 셀: 제목(질문 한 줄) · 「설치」 · 「실행 환경 준비」 · 「단계 1~3」 + `_src` b4 「코드 읽기와 비교 경계」와 같은 글(옛 도구 `part6b_enrich.py`가 끼움) · **결과 읽기 셀 0**, 「이 노트북에서 할 일」·준비물(요청 수·비용·시간)·실행일 문장 없음, 셀 첨부 그림 0.
- `_src` 틀(옛 생성기 `author_ch27.py` 한 틀): b1 둘째·셋째 목표가 여덟 절 같음(「실행 출력에서 … 구성과 결과를 구분할 수 있습니다」·「이 실험이 확인한 범위를 설명할 수 있습니다」) · b3 둘째 단락 여덟 절 같음(「노트북은 앞 절 변수에 의존하지 않으며 …」) · b4 「도식 읽기」 첫 문장(색 뜻) 여덟 절 같음 · b8 셋째 항목 여덟 절 같음(「버전과 측정 범위를 실행 기록에 함께 남깁니다」) · **b10 참고 자료 여섯이 여덟 절 같음**(개요·백엔드·서브에이전트·0.7.0 릴리스·모델 가격·MIT 라이선스, 확인 2026-09-11) · b9 복습 셋.

## 2. 절별로 더 봐야 할 것

### 01 하네스와 일곱 기능
- **슬러그 고정**: Ch 26 05 b8(완료, `_src`·HTML·`author_05.py` 592·604행 `L_CH27_01`, `author_04.py` 844행)이 `../ch27-deepagents/01-하네스와-일곱-기능.html`을 링크하고 「긴 작업에 자주 쓰는 기능을 미리 묶어 둔 DeepAgents를 봅니다」라고 소개합니다 → **01 슬러그 유지** · 01이 「미리 묶어 둔 기능」을 보여야 참.
- **지금 판의 검사 방법이 결함**: `inspect.getsource(create_deep_agent)`는 독스트링과 주석까지 담습니다. 설치판에서 다시 보니 **`'TodoListMiddleware' in source`도 `True`**입니다(함수 본문 주석 「`TodoListMiddleware` is from langchain …」). 즉 이 방법은 0.7.0에서 **조립하지 않는 미들웨어까지 True**로 내놓아 「조립 경로가 있다」도 보이지 못합니다(`/tmp/ch27-prep/exp` 확인 — 일곱 이름 중 여섯은 독스트링에도 있음). 구 `qa/verification.md` 「03절은 기본 생성 소스에 TodoListMiddleware가 없고」와도 부딪힘.
- **모델 없이 결정적으로 보일 수 있는 대안(e1·e6)**: 설정을 바꿔 가며 에이전트를 만들고 **공개 값**을 출력 — `agent.get_graph().nodes`(노드 이름)와 도구 실행 노드의 도구 이름. 기본: 노드 `['__start__', 'model', 'tools', 'PatchToolCallsMiddleware.before_agent', '__end__']`, 도구 아홉 `['delete', 'edit_file', 'execute', 'glob', 'grep', 'ls', 'read_file', 'task', 'write_file']` · `TodoListMiddleware()`를 더하면 노드 `TodoListMiddleware.after_model`·도구 `write_todos` · `skills=` → 노드 `SkillsMiddleware.before_agent` · `memory=` → `MemoryMiddleware.before_agent` · `interrupt_on=`(또는 권한 `mode="interrupt"`) → `HumanInTheLoopMiddleware.after_model` · 비동기 서브에이전트(`graph_id`) → 도구 다섯 더(`start_async_task`·`check_async_task`·`update_async_task`·`cancel_async_task`·`list_async_tasks`) · 권한 `deny`는 노드·도구 변화 없음(파일 도구 안에서 판정). 설정 `agent.config["recursion_limit"]` = **9999**. 도구 이름은 `agent.nodes["tools"].bound.tools_by_name`(과정 처음 — 쓰면 한 문장).
- **모델 객체에 키가 필요**: `init_chat_model("openai:gpt-5.4-mini", …)`는 키가 없으면 만들 때 `OpenAIError: Missing credentials`로 멈춤(e6 끝). 모델 없는 01도 키 셀이 있어야 함(요청 0 — Ch 21 04 선례 「모델 객체 때문에 키 셀은 있음」). 묶음 실행 검사처럼 키 없이 돌리려면 다른 모양이 필요(§4-5).
- **「일곱 기능」 분류는 교재가 만든 것**: 공식 개요(2026-09-28 확인)는 제목 넷 「Execution environment」·「Context management」·「Delegation」·「Steering」, 설치판 독스트링은 기본 도구(파일·`execute`·`task`)와 미들웨어 차례(기본: Filesystem → SubAgent → Summarization → PatchToolCalls → (사용자) → AnthropicPromptCaching(비 Anthropic 모델에서는 아무 일 안 함) / 선택: Skills·AsyncSubAgent·Memory·HITL)로 설명합니다. 「파일 권한」은 미들웨어가 아니라 `FilesystemMiddleware` 안 판정. 분류 수를 둘지(일곱 / 기본 넷 + 선택 넷 / 공식 넷) 정할 자리(§12-3).
- b3 「Ch 21의 create_agent는 모델과 도구의 반복을 만들었습니다 … Ch 23 … Ch 24 … Ch 26 …」 — Ch 21·23·24·26 요약이 모두 **참**으로 기록(§4-3). 「DeepAgents는 … LangChain과 LangGraph 위에서」는 설치판으로 참(`create_deep_agent`가 마지막에 `create_agent(…)`를 부름, `graph.py` 922~944행).
- **Ch 6 01의 하네스 정의를 이어 써야 함**(§4-3): Ch 6 01 b4 「하네스(harness)는 모델 호출을 둘러싼 실행 틀입니다. 입력을 준비하고, 호출하고, 결과를 검사하고, 기록하는 코드」 + 비유 「쟁반·도장·공책」. Ch 9 06 「실험 하네스」(설정을 읽고 같은 차례로 실행해 기록하는 코드)는 **다른 뜻** → 01에서 한 문장으로 가를 자리.

### 02 create deep agent와 도구
- 제목 「create deep agent와 도구」(밑줄 빠진 함수 이름)·슬러그 `02-create-deep-agent와-도구` — 슬러그는 Part 6 목차만 링크(다시 만들어짐) → 바꿀 수 있음(강사 확인).
- b4 「기본 파일 도구는 ls, read_file, write_file, edit_file, delete, glob, grep입니다. execute는 … 샌드박스 백엔드가 있을 때만」 — **부분 참**: 그래프에 등록된 도구는 아홉(파일 일곱 + `execute` + `task`)이지만, `FilesystemMiddleware.wrap_model_call`이 요청마다 백엔드가 명령 실행을 지원하지 않으면 **`execute`를 모델에게 보내는 도구 목록에서 뺍니다**(`middleware/filesystem.py` 2405~2430·2690~2715행). `StateBackend`·`FilesystemBackend` 모두 빠지는 것은 `{'execute'}`(e2 — `delete`는 둘 다 지원). 즉 「그래프 도구 아홉 ↔ 모델이 받는 도구 여덟」. `task`는 서브에이전트 미들웨어가 붙임(기본 general-purpose 서브에이전트가 늘 있어 늘 붙음).
- b4 「`tools`에는 업무 도구를 전달하고 … 사용자 도구는 기본 하네스 도구에 추가됩니다」(복습 2) — 참(독스트링 「Passing tools here is additive — it never removes a built-in」, e1 도구 열 개).
- b4 「0.7에서는 write_file이 기존 파일 전체를 교체」 — 참(0.7.0 릴리스 노트 「replaces it entirely if it already exists」, e2 덮어쓰기 `error=None`). **도구 메시지 「Updated file …」는 새 파일에도 똑같이 나옴**(e2 첫 쓰기) → 08 「Updated file」을 「이미 있던 파일」로 읽지 말 것.
- 도구 `course_lookup(chapter: int)` — 모델이 정수 인자를 채움(흔들림 작음). `{27: …}[chapter]` 딕셔너리 바로 읽기는 다른 장이면 `KeyError`.
- **모델 요청 수 세기**: 결과 `messages`에는 부모 에이전트 목록만 있음. 서브에이전트를 부르지 않는 02는 `AIMessage` 수 = 요청 수(Ch 19 `sum_usage` 그대로 씀).

### 03 플래닝과 시스템 프롬프트
- b4 「0.7.0부터 TodoListMiddleware와 write_todos는 기본 구성에서 빠졌습니다」 — **참**(릴리스 노트·공식 개요 「Starting in v0.7 task planning is opt-in only」·e1 기본 도구에 `write_todos` 없음). 「작성된 기본 시스템 프롬프트도 비어 있으며」 — 참(e1 `system_prompt` `''` — 사용자가 `system_prompt=`를 주면 그 글만). 다만 **`TodoListMiddleware()`를 직접 더하면 그 미들웨어가 자기 긴 안내 글(`WRITE_TODOS_SYSTEM_PROMPT`)을 시스템 메시지에 붙임**(`langchain/agents/middleware/todo.py` 203~252행) — 「빈 프롬프트」와 「계획 켜기」를 한 절에서 말할 때 섞지 말 것.
- **65%는 이 노트북이 잰 값이 아님**: PR #5009 `gpt-5.5` 「hello」 첫 차례 5,395 → 1,895토큰. 지금 판도 b6·b7에서 그렇게 한정했지만 b1 「측정 범위와 함께 확인」·b5·셀 10이 손 숫자로 계산해 `assert`. 규격 §3 「기준 값 밝히기」·과정 금지어 「측정」 — 남길지(인용 한 줄 + 링크) / 뺄지 / 이 과정 모델로 `system_prompt` 없는 기본 에이전트와 `TodoListMiddleware` 붙인 에이전트의 첫 요청 입력 토큰을 직접 견줄지(요청 2, 흔들림 작음 — 입력 토큰은 Ch 8 06 「입력 토큰 수는 같음」 선례) 정할 자리.
- 할 일 목록(칸 `todos`, 각 `content`·`status` — `pending`·`in_progress`·`completed`)은 **흔들리는 값**: 항목 글·개수·`write_todos` 부른 횟수. `completed`는 모델이 적은 표시일 뿐(지금 b6·b7이 바르게 한정). `write_todos`는 한 응답에 둘을 못 부름(안내 글 131행 「should never be called multiple times in parallel」).
- b3 「Ch 26에서 위임 완료 조건을 문장으로 적었습니다」 — Ch 26 요약 §13·§15 **참**(04 b4 「서브에이전트의 완료 조건」 + 노트북 8절). Ch 17 03 「정지 조건」·Ch 26 04 「완료 조건」과 할 일 목록을 잇는 자리.
- 제목 「플래닝과 시스템 프롬프트」 — 「프롬프트」는 Ch 7 이후 금지어(→ 「시스템 메시지(글)」·「지시 글」), 「플래닝」 영어 음차 → 제목에만 두고 본문 풀이(강사 확인, Ch 15·16·18 선례).

### 04 파일시스템과 중간 결과
- **실습 폴더에 쓰고, 07과 같은 폴더를 씀**: `LAB/'workspace'`에 쓰고 목록을 출력하는데, 저장된 출력에 07이 쓴 `/research/final.md`가 함께 나옴 → **노트북 사이 실행 차례 의존**(옛 `qa/technical-review.md` 「실행 순서 의존 제거」와 다름). 07을 먼저 돌렸는지에 따라 출력이 달라짐(`assert`는 둘 다 통과).
- **쓰기 자리 선례**: Ch 23·24 준비 셀 `practice_folder = tempfile.mkdtemp(prefix="ch23-03-")` → `os.chdir(practice_folder)` → `os.listdir()`(과정 요약 §3 「준비 셀」, Ch 23 「파일은 임시 폴더에만」). Ch 27은 **키를 읽는 절에서 `os.chdir()` 뒤에는 `find_dotenv(usecwd=True)`가 `.env`를 못 찾음** → 키 셀을 옮기기 전에 두거나, `chdir` 없이 `FilesystemBackend(root_dir=tempfile.mkdtemp(prefix="ch27-04-"))`로 루트만 임시 폴더로(도구 파일을 쓰면 Ch 3 교훈대로 가져오기도 옮기기 전에).
- 설치판(e2): `virtual_mode` 기본 `True` · `../outside.md`·`/../outside.md` → `ValueError: Path traversal not allowed` · `/etc/x.md`는 루트 아래 `etc/x.md`로(컴퓨터의 `/etc` 아님 — b4 「가상 경로의 /는 컴퓨터의 루트가 아님」 참) · `read` → `ReadResult`(칸 `file_data` = `content`·`encoding`) · `ls` → 항목의 `path` · 덮어쓰기 `WriteResult(error=None, …)`.
- **권한 규칙은 백엔드를 직접 부를 때는 걸리지 않음**(독스트링 「Direct backend usage does not currently incorporate permissions」, e2 `blocked2.txt` 쓰기 성공) — 04처럼 백엔드를 직접 부르는 셀과 08 권한을 이어 설명할 때 주의.
- **`StateBackend`(기본)는 그래프 밖에서 못 씀**(e2 `RuntimeError`) — 파일은 상태 칸 `files`(`/경로: {content, encoding, created_at, modified_at}`)에 들어가고 디스크는 그대로(e2). 미리 넣으려면 `invoke({"messages": …, "files": {…}})`. → **디스크를 전혀 쓰지 않는 파일 장면**이 가능(§9-3).
- b3 「Ch 23에서 상태 저장 범위를 구분했습니다 … 체크포인터 메시지와 다른 저장 표면」 — Ch 23 요약 206행 「참 — Store는 한 줄뿐, 느슨함(Ch 27 작업 때 확인)」. `StateBackend` 파일은 **체크포인터와 같은 상태 안**(스레드마다), `FilesystemBackend`는 디스크, `StoreBackend`는 LangGraph Store(Ch 23 01 b7 「Store는 실행 안 함」) → b3를 「상태 안(StateBackend) ↔ 디스크(FilesystemBackend)」로 맞출 자리. 「영속」·「표면」·「메타데이터」·「보장」 말.

### 05 컨텍스트 관리와 오프로딩
- **같은 이름 미들웨어는 기본 자리를 바꿈**: `middleware=`에 `FilesystemMiddleware(…)`를 넣으면 `_apply_custom_middleware`가 이름이 같은 기본 `FilesystemMiddleware`를 **그 자리에서 바꿈**(`graph.py` 201~235행, e5 — 주 에이전트 자리 한도 20000 → 200). 지금 판 b4 「이 예제의 FilesystemMiddleware 한도는 …」는 참이지만, **이 교체로 `permissions=`(파일 도구 안 판정)도 함께 사라짐**(교체한 객체에 `_permissions` 없음) — 권한과 한도를 함께 쓰는 절(08·09)에서 주의.
- **옮기는 기준**: 도구 결과 글이 `4 × 한도`자를 **넘으면**(`len(content) > NUM_CHARS_PER_TOKEN * limit`, `filesystem.py` 2846행) `/large_tool_results/<호출 ID>`에 쓰고 안내 글 + 앞 몇 줄 미리보기만 남김. 기본 한도 **20000토큰(= 80,000자)**, 사람 메시지는 50000토큰. 파일 도구 일곱(`ls`·`glob`·`grep`·`read_file`·`edit_file`·`write_file`·`delete`)의 결과는 옮기지 않음(1199~1206행). e2 — 한도 200이면 30,000자 결과가 안내 1613자로, 파일 30,000자(호출 ID `call_big1`) · 기본 한도면 옮기지 않고 30,000자 그대로. **모델 없이 결정적으로 보일 수 있음**(손으로 만든 도구 요청 → `ToolNode(…, wrap_tool_call=미들웨어.wrap_tool_call)` — 호출 ID를 우리가 정해 파일 이름도 결정적). 안내 글 길이는 호출 ID 길이만큼 달라짐(옛 1653 ↔ e2 1613).
- **요약은 실행하지 않았음(b4·b7이 그렇게 한정 — 참)**. 설치판 기준: Deep Agents의 요약 미들웨어(`deepagents.middleware.summarization.SummarizationMiddleware`, 이름 「SummarizationMiddleware」)는 모델 프로필에 `max_input_tokens`가 있으면 **그 85% 이상에서 시작·10%를 남김**(`compute_summarization_defaults`, 249~286행 — 공식 문서 「Triggers at 85% … Keeps 10%」). `gpt-5.4-mini` 프로필 `max_input_tokens` = **400000** → 약 340,000토큰에서 시작 → **수업에서는 켜지지 않음**. 켜 보이려면 같은 이름으로 작은 기준(`trigger=("messages", 4)` 등)의 Deep Agents 요약 미들웨어를 `middleware=`에 넣어 기본 자리를 바꿈(요약 요청 1번 더 — Ch 22 03 5번 선례).
- **Ch 22 03과 다른 점(소스 확인)**: Deep Agents 요약은 **상태의 `messages`를 지우지 않고**(`wrap_model_call`에서 요청만 바꿈, 비공개 칸 `_summarization_event`) 밀려난 메시지를 백엔드 `/conversation_history/{thread_id}.md`에 적어 둠 — Ch 22 03 LangChain 판(상태를 `RemoveMessage`로 다시 씀)과 다름(`create_summarization_middleware` 독스트링 1611~1642행). 과정 말로는 Ch 8 03 「줄이기(Compress)」.
- 「오프로딩(offloading)」 새 말(영어 음차) — 「큰 도구 결과를 파일로 옮겨 두기」처럼 풀거나 새 용어로 정의(§9-2). 복습 1 「200은 무엇의 단위」 — 토큰 한도지만 실제 판정은 글자 수(4배)라는 점을 적을 자리.

### 06 서브에이전트 위임
- **부모도 `source_lookup`을 직접 가짐**(`tools=[source_lookup]`) + **기본 general-purpose 서브에이전트가 늘 있고 부모 도구를 그대로 물려받음**(e4 — `general-purpose` 도구 `['source_lookup']`) → 모델이 ① 직접 조회 ② source-reviewer에 위임 ③ general-purpose에 위임 가운데 고름 = **흔들리는 값**. 지금 판은 요청 글에 「task 도구로 source-reviewer에게」를 적어 줄였음. 위임을 결론에 쓰려면 부모 도구에서 조회 도구를 빼는 설계(구조로 정해지는 값)가 흔들림을 줄임.
- **설치판 `task` 동작(소스 `middleware/subagents.py` 252~269·474~568행, e3·e4)**: 서브에이전트는 **넘긴 글 한 줄(`HumanMessage(description)`)로 시작한 새 목록**(부모 `messages`·`todos`·`structured_response`는 안 넘김) · **상태 칸 `files`는 넘기고 돌려받음**(e4 — 부모 파일이 보이고, 서브에이전트가 쓴 파일이 부모 `files`에 더해짐 → `StateBackend`만으로 부모·서브에이전트가 파일을 함께 씀) · 돌려주는 것은 마지막 글 있는 `AIMessage`의 글 하나를 담은 `ToolMessage`. Ch 26 01 「안쪽 목록 ↔ 바깥 목록」과 같은 모양 → Ch 26 말 「바깥 목록·안쪽 목록」을 이어 쓸 수 있음.
- **요청 수 셈**: 서브에이전트 요청은 부모 결과 목록에 없음(Ch 26 01 함정과 같음). 세려면 ① 서브에이전트 스펙 `middleware`와 부모 `middleware`에 **Ch 22 02 모양 기록 훅(`@wrap_model_call`)**을 함께 붙여 요청마다 목록에 한 줄 ② `get_usage_metadata_callback()`(모델 이름별 토큰 합 — 요청 수는 안 셈, 과정 안 씀) ③ 스트림 `subgraphs=True`(과정 안 씀, Ch 25 인계). **general-purpose 서브에이전트에는 부모 `middleware=`가 옮겨 가지 않음**(e5 — 기본 자리 이름과 같은 것만 물려받음, `graph.py` 777행) → 기록 훅·호출 한도가 general-purpose 요청을 놓침.
- b4 「서브에이전트는 문맥을 격리하지만 도구 권한까지 자동으로 줄이지는 않습니다 … 상속 규칙은 항목마다 다르므로」 — 설치판: 도구는 스펙에 `tools`가 없으면 부모 도구를 물려받고(`graph.py` 728행), 권한은 스펙에 없으면 부모 규칙(664행), `interrupt_on`도 물려받음(720행), 스킬은 안 물려받음. 공식 문서 표와 같음. 「문맥」·「격리」·「반환」 말.
- b3 「Ch 26에서 서브에이전트의 완료 조건을 적었습니다」 — Ch 26 요약 §15 **참**(단 §4-1 인계 1·2를 전제하지 말 것).
- **`assert 'planning opt-in' in 보고 글`은 규격 §3 위반** — 구조 값(`task` 도구 메시지 있음·호출 ID 짝·`files` 칸 키)으로.

### 07 출처 검증형 deep research
- **웹 검색을 쓰지 않음**(§6): 고정 자료 둘을 딕셔너리로, `source_lookup`이 ID로 찾아 내놓음(없는 ID는 `'UNKNOWN SOURCE'`). 제목·b2 「deep research」 영어, 「검증」(Ch 16 금지어 → 「검사」)·「페이지」 말. 본문은 이미 「제공 자료에 대한 출처 검증형 조사」로 한정(좋음).
- **모델을 문자열로 넘겨 과정 표준 설정이 빠짐**: `create_deep_agent(model='openai:gpt-5.4-mini')` → Deep Agents 제공자 설정이 **OpenAI Responses API(`use_responses_api=True`)**로 만들고 `temperature`·`reasoning_effort` 없음(e1 끝, `profiles/provider/_openai.py`). 모델 객체를 넘기면 **그대로 씀**(`_models.py` 54~55행 「returns it unchanged」) → 과정 표준 모델 셀 객체를 넘기는 것으로 바로잡을 수 있음. 서브에이전트·요약도 같은 객체를 씀(`spec.get("model", model)`, `create_summarization_middleware(model, …)`).
- 요청 글·자료·`final.md`가 모두 **영어**(학생 교재는 한국어 — 자료실 글 선례처럼 한국어 교재용 글로 바꿀 자리). 세 제목 `assert`는 모델이 쓴 파일 글에 걸림(규격 §3) → 파일이 있는지·출처 ID 칸 등 구조 값으로.
- 사용량 2,379·34·2,413은 **부모 마지막 요청 하나의 값**(b6·b7·README가 그렇게 한정 — 참)이고 흔들리는 값. `집필점검표.md` 2,498·38은 다른 실행 값(어긋남).
- 공식 deep research 예(2026-09-28 확인, `docs.langchain.com/oss/python/deepagents/deep-research`): Tavily(`TAVILY_API_KEY`, 패키지 `tavily-python`·`httpx`·`markdownify`) · `TodoListMiddleware`로 계획 · `/research_request.md`·`/final_report.md` · 인용 `[1]`·`[2]` + `### Sources` · 연구 서브에이전트 하나부터, 동시 최대 3 · 검색 2~5번·위임 최대 3바퀴 — **이 과정 환경에서는 재현 불가**(§6).

### 08 통합 실행과 운영 한계
- 권한 `deny`는 **모델 없이 결정적으로 보일 수 있음**(e2): 손으로 만든 도구 요청 둘 → `write_file | Updated file /run/report.md | success` · `write_file | Error: permission denied for write on /blocked.txt | error`, `blocked.txt` 없음. 결과 메시지 칸 `status`가 `success`·`error`(Ch 19 06 「결과 상태」 말). 모델 절로 두면 쓰기 둘이 한 응답인지·차례인지, 두 번째를 시도하는지가 흔들림.
- `assert report == 'status: complete'`는 모델이 채운 인자 글(흔들림 — 지금 판은 따옴표 안 글을 그대로 옮겨 통과).
- b3 「Ch 24의 사람 승인과 이 장의 permissions는 도구 실행 경계를 다룹니다」 — **Ch 24 요약 192행: 부분 참**(Ch 24는 쓰기 노드 하나의 승인 지점만, 모델이 고른 도구 호출 승인·`HumanInTheLoopMiddleware` 장면 0) → 「Ch 27이 보이거나 「부작용 앞 승인 지점」으로 맞춤」. Deep Agents 쪽 수단: `interrupt_on={"write_file": True}` 또는 권한 `mode="interrupt"`(둘 다 `HumanInTheLoopMiddleware`를 붙임, e3·e6) — **체크포인터 필요, 이어 가기는 `Command(resume={"decisions": [{"type": "approve"}]})`**(`human_in_the_loop.py` 51·130~134행) — Ch 24 `Command(resume=값)`과 모양이 달라 **새 API**.
- md 「최대 반복 수는 무한 실행을 막는 경계일 뿐」 — 「최대」 금지어 · Ch 20 「실행 한도」·Ch 16/22 「호출 한도」·Ch 17 「바퀴 한도」 가운데 무엇인지 적을 자리. **Deep Agents 그래프 실행 한도는 9999**(e1), 서브에이전트에는 부모 한도가 닿지 않음(§5-5).
- b8 「Ch 28에서는 허용된 기능을 MCP 서버로 공개하고 …」 — Ch 28(대기) 01과 맞음(고치지 않음).

## 3. 실습 폴더 구조와 읽는 곳

```
labs/part6/ch27-deepagents/
  README.md (절별 표·「생성되는 파일」·사용량 단락 — 07 사용량 2,379·34·2,413, 「절당 1달러 미만」)
  pyproject.toml   uv.lock (101 package 항목, export 100줄)
  notebooks/01~08-*.ipynb
  workspace/research/source-a.md (04가 씀, 57바이트) · workspace/research/final.md (07이 씀, 856바이트)
  workspace-05/large_tool_results/call_… × 6 (05가 실행마다 하나씩 더함, 파일마다 72,000바이트 = 30,000자)
  workspace-08/run/report.md (08이 씀, 「status: complete」)
  .venv/ (macOS 판 215MB — home = /Users/…/cpython-3.12-macos-aarch64-none, uv 0.11.6, prompt kdt-ch27-deepagents)
  (없음: data/ · runs/ · tests/ · 도구 파일 · 노트북 생성기)
```

- **노트북이 쓰는 파일**: 04 `workspace/research/source-a.md`(백엔드 직접) · 05 `workspace-05/large_tool_results/<호출 ID>`(도구 결과 옮기기) · 07 `workspace/research/final.md`(모델의 `write_file`) · 08 `workspace-08/run/report.md`(모델의 `write_file`). 모두 **연결 폴더 안 실습 폴더**(`LAB`은 `pyproject.toml`이 있는 부모 폴더를 거슬러 찾음). 읽는 파일은 여덟 절의 `.env`와 04·05·07·08이 방금 쓴 파일뿐. **`workspace*`를 읽는 다른 코드: 0**(`grep` — 챕터 원고·README·옛 생성기·기록 파일의 글만). 묶음 허용 목록에 `workspace*` 없음(README가 밝힘), zip에도 없음. SQLite 파일은 쓰지 않음(Ch 23 연결 폴더 멈춤 문제는 해당 없음). 규격 선례(Ch 23·24)는 **쓰기는 임시 폴더**.
- **before/ 스냅숏에 `workspace*` 포함**: 세 폴더 파일 9개 합 432,929바이트라 원본 모양 그대로 `before/workspace*/`에 복사(04 목록 출력에 07 파일이 섞인 증거·05 파일이 쌓인 증거 보존). 원본은 그대로 둠(삭제 금지 — 마감에서 삭제 승인 목록).
- **Ch 27 파일을 코드로 읽는 곳**(`grep -rIl`, `textbook`·`labs`·`.moai`, `.venv`·`.cache` 제외):

| 자리 | 무엇을 | 성격 |
|---|---|---|
| `textbook/part6/public-files.json` 60~70행 | README·노트북 여덟·`pyproject.toml`·`uv.lock` = 11줄 | 묶음 허용 목록(Ch 26과 달리 잠금 둘도 목록에 있음) |
| 챕터 `qa/public-files.json` | 실습 파일 11(HTML 줄 없음, 옛 SVG 줄 없음) | `collect_public_files.py`가 Part 목록으로 모음 |
| `textbook/downloads/part6-practice.zip`(105항목)·`llm-practice.zip`(455항목) | Ch 27 11파일이 **디스크와 같음** | 묶음 |
| `textbook/part6/_build_index.py` 25행 · `textbook/_notebook/build_index.py` 58~59행 · `build_bundle.py` 26행 | (8, 16, 「파일과 서브에이전트를 사용해 중간 자료가 남는 조사 에이전트를 만듭니다.」) · (절 수 8, 짧은 이름 「DeepAgents」, 「파일·서브에이전트·컨텍스트 관리를 연결해 조사 과정을 구성합니다.」) · 공개 챕터 목록 | 실습 절을 붙이면 Part 목차는 절 아홉(`_notebook/build_index.py`는 실습 절을 빼고 세는 약속 — 8 그대로) |
| Part 6·7 선행 목록 · `existing-artifact-hashes.json` · 챕터 `qa/prerequisite-files.json`(없음) | **Ch 27 줄 0** | 뒤 챕터가 Ch 27 파일을 읽지 않음 |
| Part 6 `check_bundle_execution.py` 30~31행 | Ch 24 01·Ch 28 01만(**Ch 27 안 봄**) | 묶음 실행 계약 없음 |
| 옛 검사(고치지 않음, 기록만) | `check_scope.py` 13행 `EXPECTED` (8,16)·`SECTION_COUNTS` 8(실습 절을 붙이면 8 ≠ 9, 이미 Ch 21에서 멈춤) · `check_notebook_readiness.py`(노트북 수 단언 — 결과 파일을 먼저 씀 → 되돌림 선례) · `check_figures.py`(SVG마다 `.excalidraw` 짝) · `check_visual_reports.py` · `check_delivery.py`(`llm-practice.zip` 신선도) | Ch 21~26 선례대로 이미 어긋난 상태 |
| 기록만 | `final-artifact-hashes.json`(Ch 27 줄 54 — **28줄은 이미 옛 해시**: HTML 8·`_src` 8·노트북 8·`08-흐름` 셋·`_gen_figures.py`, 26줄은 같음) · `notebook-executions.json`·`notebook-readiness.json`·`figure-consistency.json`(각 8) · `visual-results.json`(18) · `lesson-scope.json`·`prose-repetition-initial.json`(1) · `verification.md` · `ch27-technical-review.md` · `language/ch27-final.{json,md}`·`language/ch27-original/`(옛 원문 사본 — `workspace` 글 포함) · Part 7 `existing-artifacts-before.json`(16)·`before-integration/build_*.py` · `_notebook/checks/notebook-contracts-part6-ch27-deepagents.json`(verify가 다시 씀)·`checks/ch27-deepagents/`(옛 화면 검사 PNG 넷·`visual-results.json`) · `_notebook/checks/part6/part6b_*.py`·`.moai/…/part6b_*.py` · Ch 26 `before-manifest.json`(Ch 27 줄 8 — 지금과 모두 같음) | — |

- **옛 생성기**:

| 파일 | 무엇을 씀 | 비고 |
|---|---|---|
| **`qa/author_ch27.py`**(555줄, `45453725…`, **Ch 27 전용**) | `_src` 여덟·노트북 여덟(출력 없이) | 머리에 `refuse_existing_drafts()` — 대상 파일이 하나라도 있으면 `FileExistsError`로 멈춤(덮어쓰기 막음). 그래도 규격 §8대로 01절에서 첫머리 `raise SystemExit(...)`·마감에서 `mv -n` → `qa/upgrade/before/generators/blocked/`. 부르는 스크립트 0(`grep` — 기록 문서·Ch 26 `before-manifest.json`만). `qa/__pycache__/author_ch27.cpython-312.pyc` 있음(삭제 승인 목록) |
| `figures/_gen_figures.py`(`45d40ea2…`) | `NN-흐름.{svg,excalidraw,caption.md}` 24개(`textbook/part5/_figure.py`) | 옛 그림 여덟 벌. 사본 `before/generators/`·`before/figures/` |
| (챕터 밖) `_notebook/checks/part6/part6b_enrich.py`·`part6b_review_fixes.py`(`.moai/…`에도 같은 이름) | Ch 27 노트북 설명 셀·`_src` 단락 덧붙임·다시 실행(45~56·131~155행) | 기록만(Ch 21~26 선례) |
| `textbook/part6/_author_ch21_ch29.py` | **Ch 27 안 씀**(`grep` 0) | — |

- **판**: `requires-python = ">=3.12,<3.13"`, `dependencies = ["deepagents==0.7.0", "langchain==1.4.0", "langchain-openai==1.6.0", "python-dotenv==1.2.3"]`(**`langgraph`는 직접 고정하지 않음** — 잠금 1.2.11), dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`, `[tool.uv] package = false`. 잠금 주요 판: `deepagents 0.7.0`(업로드 2026-07-29)·`langchain-core 1.6.2`·`langgraph 1.2.11`·`langgraph-prebuilt 1.1.0`·`langgraph-checkpoint 4.2.0`·`openai 3.11.0`·`pydantic 2.13.5`·**`langchain-anthropic 1.7.1`·`anthropic 1.4.0`·`langchain-google-genai 4.4.0`·`google-genai 2.22.0`·`google-auth 2.58.0`·`cryptography 50.0.1`·`wcmatch 11.0.1`**(deepagents가 끌어옴). **`numpy`·`pillow`·`langgraph-checkpoint-sqlite`·`tavily-python`·`markdownify` 없음**(`httpx`는 있음). `pyproject.toml`·`uv.lock` 수정 시각 09-10 그대로.
- **Ch 26 잠금과 견줌**: 패키지 판 **모두 같고**, Ch 27에 13개가 더 있음(`deepagents`·`anthropic`·`langchain-anthropic`·`google-genai`·`langchain-google-genai`·`google-auth`·`pyasn1`·`pyasn1-modules`·`cryptography`·`bracex`·`wcmatch`·`docstring-parser`·`filetype`) + 프로젝트 이름. → Ch 26 `delegation_tools.py`(가져오기 `langgraph.types.Send`)는 Ch 27 잠금에서도 import는 되지만, Ch 26 요약 §13-6 약속대로 **파일째 가져오지 말고 함수만 옮김**(§8). Ch 21 `runner_tools.py`는 맨 위 `numpy`라 Ch 27에서 import 자체가 멈춤.
- `pytest`·`tests/` 없음. 실습 폴더 `.venv`는 macOS 판(삭제 승인 대상).

## 4. 앞뒤 챕터 이음새

### 4-1. Ch 26 인계(요약 §13·§14·§15, 계약 §3 Ch26 줄) 항목별 지금 상태

| 인계 항목 | 지금 Ch 27 원고·설치판 | 상태 |
|---|---|---|
| Ch 27 01 b3 「Ch 26은 위임 구조를 다뤘습니다」 · 03 b3 「Ch 26에서 위임 완료 조건을 문장으로 적었습니다」 · 06 b3 「Ch 26에서 서브에이전트의 완료 조건을 적었습니다」는 참 | 세 문장 그대로 | **참** — b3를 다시 쓸 때도 Ch 26 04 b4 「서브에이전트의 완료 조건」 자리를 가리키면 됨. Ch 26 05 b8이 Ch 27 01 슬러그를 링크(고정) |
| ① 서브에이전트 안쪽 실행에 바깥 실행 한도가 닿지 않음(`create_agent` 9999) → **DeepAgents 서브에이전트에는 안쪽 한도를 따로** | 원고는 한도를 말하지 않음(08 md 「최대 반복 수」 한 줄) | **설치판도 같음(e3)**: `task`가 서브에이전트를 `{"configurable": {"ls_agent_type": "subagent"}}`로 부르고, 서브에이전트 그래프에 묶인 설정이 부딪히는 키에서 이김(`subagents.py` 559~567행 주석 「the subagent's bound config still wins collisions (e.g. … `recursion_limit`)」). 모델 없는 확인: 묶인 한도 없는 그래프는 부모 `{"recursion_limit": 5}`에 `GraphRecursionError`, `with_config({"recursion_limit": 9999})`로 묶인 그래프(선언형 서브에이전트 = `create_agent` 모양)는 부모 한도 5를 무시하고 20단계 끝까지. Deep Agents 부모 그래프도 9999(`graph.py` 937행). **안쪽 한도를 따로 주는 방법**: 서브에이전트 스펙 `middleware`에 `ModelCallLimitMiddleware(run_limit=…, exit_behavior="end")`(e4 — 스택에 들어감). **general-purpose 서브에이전트에는 부모 `middleware=`의 한도가 옮겨 가지 않음**(e5) → 기본 서브에이전트를 쓰는 한 그 요청은 한도 밖 |
| ② Ch 26 전문 에이전트는 모두 도구 없음 — 요청 수 셈은 그 조건 값 | Ch 27 서브에이전트는 **도구를 가짐**(06·07 `source_lookup` + 파일 도구 일곱 — 서브에이전트 스택에도 `FilesystemMiddleware`, e4) | Ch 26 셈 「전문 = 부른 횟수 × 1」을 그대로 쓰면 틀림 → 「부른 횟수 × 서브에이전트 안 요청 수(도구 요청 응답 수 + 1)」. 서브에이전트 안 요청은 부모 목록에 없음(§2 06) |
| ③ 핸드오프 한 응답 넘기기 둘이면 400, 적용 쪽이 실행마다 다름 — 「첫째만 적용」 금지 | Ch 27에 핸드오프 없음 | 해당 없음. 단 `task` 둘을 한 응답에 부르면 도구 실행 노드가 **함께 실행**(도구 설명 「Launch multiple agents concurrently … single message with multiple tool calls」) — 둘 다 `ToolMessage`로 돌아옴(`ParentCommand` 없음). 도착·기록 차례는 흔들리는 값 |
| ④ 스트리밍 0건 | Ch 27도 0건 | 어긋남 없음. Deep Agents 그래프는 `stream`·`astream`이 있음(e3), 서브에이전트 사건은 `subgraphs=True`(과정 안 씀, Ch 25 인계)가 있어야 보임 — 실행하지 않음 |
| ⑤ 완료 조건의 필요한 분야는 손으로 정한 값(정답 판정 아님) | 06 b4 「완료 조건은 … 파일에 기록하기처럼 확인 가능하게」 · 08 b4 「종료는 … 파일 본문, 거부 ToolMessage, 차단 파일의 부재를 함께 검사해 판정」 | 참(말로만) — 03 할 일 `completed`도 모델이 적은 표시라 완료 조건의 근거가 아님(지금 b6·b7이 한정) |
| ⑥ `delegation_tools.py`는 Ch 26 폴더에만 — 잠금이 다르면 파일째 가져오지 말 것 | 도구 파일 없음 | 잠금은 Ch 26 + 13개(판 같음) — import는 되지만 파일째 가져오지 않고 함수만 옮김(§8) |
| ⑦ 말: 「문맥」·「맥락」·「제어권」·「병렬」·「추정」·「측정」·「지연」·「반환」·「조각」·「이벤트」·「로그」 0 | 「반환」 02·04·05·06·07·08(06 b 14회) · 「측정」 여덟 절 모두 · 「문맥」 05 1·06 9+2 · 「검증」 여러 절 | **고칠 자리**(§1 표, §9-2) |

### 4-2. 앞 챕터에서 가르친 것 (Ch 27이 전제할 수 있는 것)

| 챕터·절 | 가르친 것 | Ch 27과의 관계 |
|---|---|---|
| Ch 6 01 | **하네스 = 모델 호출을 둘러싼 실행 틀**(입력 준비·호출·결과 검사·기록 코드), 비유 쟁반·도장·공책, 계층 지도 표 「DeepAgents — 긴 작업에 필요한 기능을 갖춘 하네스 — **Ch 27 DeepAgents — Harness 계층**」 | 01 정의의 뿌리 · 챕터 제목을 바꾸면 Ch 6 01 표 글자와 달라짐(§4-3) |
| Ch 6 06 | `estimate_cost`·요금표·「예상 비용」(청구 금액 아님) | 비용 어림 |
| Ch 8 03 | **적어 두기(Write)·골라 넣기(Select)·줄이기(Compress)·나누기(Isolate)** | Deep Agents 기능과 한 줄로 이어짐: 파일에 적어 둠 = Write · `read_file`·`grep`으로 필요한 것만 = Select · 옮겨 두기·요약 = Compress · 서브에이전트 = Isolate |
| Ch 9 06 | 「실험 하네스」(설정을 읽고 같은 차례로 실행·기록하는 코드) | **다른 뜻** — 01에서 가름 |
| Ch 16 04 · Ch 22 04 | 호출 한도(`ModelCallLimitMiddleware(run_limit=…, exit_behavior="end")` — 한도를 붙인 에이전트 요청만) | 서브에이전트 안쪽 한도(§4-1 ①) |
| Ch 17 03 | 정지 조건 넷 · 바퀴 한도 ≠ 호출 한도 | 08 「종료」 말 |
| Ch 18 04 | 작업 나눠 맡기기(계획 모델·작업 모델) | 03 계획·06 위임과 가를 한 문장(Ch 18은 코드가 나눔 ↔ Deep Agents는 모델이 `write_todos`·`task`를 고름) |
| Ch 19 01·04·05·06 | `@tool`(세 문장 + Ch 2 09 링크)·독스트링·`tool_calls`·`ToolMessage`·호출 ID·`sum_usage`·`show_messages`·`tool_call_names`·결과 상태 `status` | 도구 만들기·요청 수·08 `status: error` |
| Ch 20 01·03 | 손으로 만든 `AIMessage(tool_calls=…)` + `ToolNode` · 실행 한도 `recursion_limit`·`GraphRecursionError` | **모델 없는 파일 도구·권한·옮겨 두기 장면의 모양**(e2) · 9999 |
| Ch 21 01·02·03 | `create_agent(model, tools=…, system_prompt=…)`(모델 **객체**)·에이전트 그래프 노드·`response_format`·`ToolRuntime` | `create_deep_agent`는 마지막에 `create_agent`를 부름(같은 인자 이름 + `subagents`·`backend`·`skills`·`memory`·`permissions`·`interrupt_on`) |
| Ch 22 01~08 | 훅 `@before_model`·`@after_model`·`@wrap_model_call`·`@wrap_tool_call` 등 · 기록 훅(02 `record_model_input`) · `SummarizationMiddleware(trigger=, keep=)`(03, 메시지 6 → 3) · 호출 한도(04) · 등록 순서(07) · 컨텍스트 분리(08, `request.override(messages=…)`) | Deep Agents는 미들웨어로 만들어짐 — 기본 스택과 차례(§5-1), 기록 훅으로 부모·서브에이전트 요청 세기(§2 06), 05 요약 기준, 같은 이름이면 자리를 바꿈 |
| Ch 23 01 | `InMemorySaver`·`thread_id`·`get_state` | `StateBackend` 파일은 상태 안 → 체크포인터가 있으면 스레드마다 이어짐(실행하지 않음) · 요약 기록 파일 이름에 `thread_id` |
| Ch 24 01~03 | 노드 안 `interrupt`·`Command(resume=값)`·승인 지점 | 08 승인 — Deep Agents는 `HumanInTheLoopMiddleware`(`decisions` 모양, 새 API) |
| Ch 25 01~03 | 스트림 모드 | 서브에이전트 사건은 `subgraphs=True`가 있어야(안 씀) |
| Ch 26 01~05 | 서브에이전트·중앙 에이전트·전문 에이전트·바깥/안쪽 목록·완료 조건·요청 수 셈 | 06·07의 직접 선례(§4-1) |

### 4-3. 완료 챕터가 Ch 27에 기대는 문장 — 개선 뒤에도 참이어야 함

| 자리 | 문장 | 조건 |
|---|---|---|
| **Ch 26 05 `_src` b8(+ HTML·`author_05.py` 592·604·674행, `author_04.py` 844행)** | 「이 절로 Ch 26이 끝납니다. Ch 27 01절에서는 긴 작업에 자주 쓰는 기능을 미리 묶어 둔 DeepAgents를 봅니다」 + **01 슬러그 링크** | **01 슬러그 `01-하네스와-일곱-기능` 유지** · 01이 「미리 묶어 둔 기능」을 보임 |
| **Ch 6 01 `_src` 42행 표(+ HTML 180행)** · 목표 「LangChain, LangGraph, DeepAgents를 계층 지도의 알맞은 자리에」 · b4 하네스 정의 | 「DeepAgents — 긴 작업에 필요한 기능을 갖춘 하네스 — **Ch 27 DeepAgents — Harness 계층**」 | 챕터 제목 글자를 바꾸면 이 표가 옛 제목으로 남음(완료 챕터 — 고치지 않음, 인계에 적을 것) · 하네스 뜻을 Ch 6 01과 다르게 정의하지 말 것 |
| Ch 21 요약 220행 · Ch 23 요약 205·206행 · Ch 24 요약 191·192행 · Ch 26 요약 §15 | 01 b3(Ch 21·23·24·26) 참 · 02 b3(Ch 21) 참 · 04 b3(Ch 23) 느슨함 · 08 b3(Ch 24) 부분 참 | 04·08 b3는 §2 04·08대로 맞춤 |
| Ch 8·22·23·24·25 `_src` | Ch 27 언급 0(`grep`) | — |

### 4-4. 뒤 챕터(대기)·Part·과정 파일이 Ch 27에 기대는 문장 — 고치지 않음

| 자리 | 문장 | Ch 27 쪽 사실(지금 판) |
|---|---|---|
| **Ch 28 01 `_src` b3(+ HTML·`qa/author_ch28.py` 51행)** | 「Ch27에서는 파일시스템과 하위 작업 기능을 미리 조립한 하네스를 사용했습니다. MCP는 …」 | 참 — 개선 뒤에도 파일시스템·서브에이전트를 보이면 참(「하위 작업」은 Ch 27 말이 아님 — Ch 28 개선 때 확인) |
| `labs/part6/continuity-guide.md` 8·12·13행 | 「Ch16의 입력 검사… \| Ch22 … \| **Ch27의 컨텍스트 관리**」 · 「Ch26 … \| **Ch27의 서브에이전트 위임과 완료 조건**」(Ch 26 마감이 고침) · 「Ch6의 하네스 개념, Ch22의 미들웨어 \| **Ch27 파일·위임·컨텍스트 관리를 조립한 에이전트** \| 최종 프로젝트의 조사 과정 구성」 | 셋 모두 지금 원고와 맞음. 13행을 마감 때 새 본문과 대조(보호 파일, 묶음에 들어감). 14행 「Ch37의 비용·컨텍스트 측정」은 Ch 28 줄(없는 챕터 — Ch 28 몫) |
| `textbook/part6/practice-start.md` 15행 · `_src/index.html`(「Ch 26–28은 …」) | 「Ch 26의 위임, Ch 27의 DeepAgents, Ch 28의 MCP로 연결」 | 참 |
| `textbook/part6/_build_index.py` 25행 · `_notebook/build_index.py` 58~59행 | 「파일과 서브에이전트를 사용해 중간 자료가 남는 조사 에이전트를 만듭니다.」 · 「파일·서브에이전트·컨텍스트 관리를 연결해 조사 과정을 구성합니다.」 | 마감 때 새 본문·`objectives`와 대조 |
| Ch 28~31·34·Part 7 노트북·코드 | Ch 27 파일을 읽는 코드 0(Ch 29 평가 포함 — `grep` 0) | **산출 파일 계약 없음** |

### 4-5. Part 6 묶음·목록·기록·검사

- Part 6·7 선행 목록·`existing-artifact-hashes.json`에 Ch 27 줄 **0**. `final-artifact-hashes.json` Ch 27 줄 54개 중 28개가 이미 옛 판(만드는 스크립트 없음, 기록만).
- 공개 목록 두 곳 + zip 두 개(§3). **묶음 실행 검사 계약 없음**(목록은 Ch 24 01·Ch 28 01). 모델 없는 절(01·04, 새 판에서 모델 없는 앞 절반)을 넣을지는 전체 마감 후보 — 단 **모델 객체를 만드는 셀은 키가 없으면 멈춤**(§2 01) → 키 없이 돌릴 절은 모델 객체도 만들지 않아야 함(Ch 20 03·Ch 24 01 선례: 모델·키 셀 없이).
- 도구 파일을 만들면 `notebooks/…_tools.py` 줄을 두 목록에 더하고 zip 다시 만들기(Ch 26 마감 모양 — `python3 textbook/part6/_build_index.py`를 마지막에 한 번).
- **뒤 챕터가 Ch 27 노트북·출력·파일(`workspace*`)을 읽는 코드: 0.** 쓰기를 임시 폴더·상태 칸으로 옮겨도 깨지는 계약 없음.
- 옛 검사 스크립트(기록만, 고치지 않음): Ch 26 마감 기록대로 넷 모두 Ch 27에 닿기 전에 멈춤(`check_scope.py` Ch 21 07 · `check_figures.py` Ch 21 SVG 짝 · `check_notebook_readiness.py` 노트북 수 단언 — 결과 파일을 먼저 씀 → 되돌림 · `check_visual_reports.py` `ch22-middleware`). 실습 절을 붙이면 `check_scope.py` `SECTION_COUNTS` 8 ≠ 9. `check_delivery.py`는 `llm-practice.zip` Part 1 Stale에서 멈춤.

## 5. 설치판 동작 — 소스와 모델 없는 확인 (2026-09-28, `deepagents 0.7.0`·`langchain 1.4.0`·`langchain-core 1.6.2`·`langgraph 1.2.11`·`langgraph-prebuilt 1.1.0`·`langchain-openai 1.6.0`)

### 5-1. `create_deep_agent` 인자와 기본 스택
- 서명(`deepagents/graph.py` 268~288행): `model, tools, *, system_prompt, middleware, subagents, skills, memory, permissions, backend, interrupt_on, response_format, state_schema, context_schema, checkpointer, store, debug, name, cache` → 내놓는 것은 `create_agent(…)`로 만든 `CompiledStateGraph`에 `.with_config({"recursion_limit": 9_999, "metadata": {…}})`(922~944행).
- **기본 미들웨어(e1, 차례대로)**: `FilesystemMiddleware` → `SubAgentMiddleware`(**general-purpose 서브에이전트가 늘 자동으로 붙음** — 같은 이름 스펙을 주거나 하네스 프로필로 끄지 않는 한) → Deep Agents `SummarizationMiddleware`(`_DeepAgentsSummarizationMiddleware`) → `PatchToolCallsMiddleware` → (사용자 `middleware=`) → `AnthropicPromptCachingMiddleware`(Anthropic 모델이 아니면 아무 일 안 함). 선택: `skills=` → 맨 앞 `SkillsMiddleware` · 비동기 서브에이전트 → `AsyncSubAgentMiddleware` · `memory=` → `MemoryMiddleware` · `interrupt_on=` 또는 권한 `mode="interrupt"` → 맨 끝 `HumanInTheLoopMiddleware`. **`TodoListMiddleware` 없음**(사용자가 더하면 `PatchToolCalls` 뒤·캐시 앞).
- **사용자 미들웨어 합치기**(`_apply_custom_middleware`, 201~235행): 이름(`.name`)이 기본 스택에 있으면 **그 자리를 바꿈**, 없으면 기본 스택 뒤·꼬리 앞에 끼움. 기본 스택에서 `FilesystemMiddleware`·`SubAgentMiddleware`는 프로필로 뺄 수 없음(`_REQUIRED_MIDDLEWARE`).
- **기본 도구(e1)**: 그래프 도구 실행 노드에 아홉 — `delete`·`edit_file`·`execute`·`glob`·`grep`·`ls`·`read_file`·`task`·`write_file`(+ 사용자 도구, + `write_todos`는 `TodoListMiddleware`를 더할 때). 모델에게 보내는 목록에서는 명령 실행을 못 하는 백엔드면 `execute`가 빠짐(§2 02). 비동기 서브에이전트를 주면 도구 다섯 더(e6).
- **기본 시스템 메시지**: `system_prompt=None`이면 빈 글 `''`(e1) — 도구 사용 안내 글도 기본으로 안 붙음(주석 628~640행). 사용자 글을 주면 그 글만(프로필이 없을 때).
- 그래프 노드(e1·e6): 기본 `['__start__', 'model', 'tools', 'PatchToolCallsMiddleware.before_agent', '__end__']` — 노드 훅이 있는 미들웨어만 노드가 됨(파일·서브에이전트·요약은 `wrap_*` 훅이라 노드 없음).

### 5-2. 모델 — 객체와 문자열
- **모델 객체는 그대로 씀**(`_models.py` 54~55행) → 과정 표준 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` 객체를 넘기면 설정이 그대로(Chat Completions API, `use_responses_api` 없음 — e1 `None`). 서브에이전트(스펙에 `model`이 없으면 부모 모델 — 657행)·general-purpose·요약 미들웨어도 같은 객체.
- **문자열은 Deep Agents 제공자 설정을 거침**: `"openai:…"` → `use_responses_api=True`(Responses API), `temperature`·`reasoning_effort` 없음(e1 끝 `True | None | None`, `profiles/provider/_openai.py`). 옛 07이 이 모양. `model=None`은 0.5.3부터 사용 중단 경고(기본 Claude).
- 하네스 프로필(모델별 설정)은 `openai:gpt-5.1-codex`·`5.2-codex`·`5.3-codex`·Anthropic 세 모델·NVIDIA 한 모델만 등록 — `gpt-5.4-mini`는 기본 프로필(기본 글 비어 있음, 도구 설명 바꿈 없음).
- 모델 프로필 `max_input_tokens` = **400000**(e1) → 요약 기준에 쓰임(§5-4).

### 5-3. 백엔드 — 파일이 실제로 어디에 쓰이는가
- `StateBackend()`(기본): 상태 칸 `files`(딕셔너리 `경로: {content, encoding, created_at, modified_at}`)에 씀 — **디스크 0**(e2). 그래프 안에서만 동작(밖에서 부르면 `RuntimeError`, `backends/state.py` 49~90행). 미리 넣기 `invoke({"messages": …, "files": {…}})`. 체크포인터가 있으면 스레드마다 이어짐(소스 설명, 실행 안 함).
- `FilesystemBackend(root_dir=…, virtual_mode=True)`: 디스크 `root_dir` 아래. `virtual_mode` 기본 `True`(0.7.0부터) — `..` 거부, `/…`는 루트 아래로(e2). **`root_dir`에 `tempfile.mkdtemp(…)`를 주면 임시 폴더에만 씀**(e2가 그렇게 확인).
- `CompositeBackend(default=…, routes={"/research/": …}, artifacts_root="/")`: 경로 머리로 백엔드를 고름(e2 만들기만). `StoreBackend`(LangGraph Store — 네임스페이스 필수), `LocalShellBackend`(명령 실행 가능 — `execute`가 살아남, 실습 금지 권장), `LangSmithSandbox`·`ContextHubBackend`도 있음(실행 안 함).
- 옮겨 둔 도구 결과는 `<artifacts_root>/large_tool_results/<호출 ID>`, 요약으로 밀려난 대화는 `<artifacts_root>/conversation_history/<thread_id>.md` — 둘 다 **그 에이전트의 백엔드**에 씀(`StateBackend`면 상태 칸, `FilesystemBackend`면 디스크).

### 5-4. 요약·옮겨 두기가 켜지는 기준
- **옮겨 두기**: 도구 결과 글자 수 > `4 × tool_token_limit_before_evict`(기본 20000 → 80,000자). 파일 도구 결과는 제외. 사람 메시지는 50000토큰(200,000자) 넘으면. 안내 글에 경로 + 앞부분 미리보기(공식 문서 「preview of the first 10 lines」).
- **요약**: 모델 프로필에 `max_input_tokens`가 있으면 `("fraction", 0.85)`에서 시작·`("fraction", 0.10)` 남김, 없으면 `("tokens", 170000)`·`("messages", 6)`(`summarization.py` 249~286행). `gpt-5.4-mini`는 400,000의 85% = **340,000토큰** → 수업 실행에서 켜지지 않음. 요약 요청은 같은 모델에 한 번 더 나감.

### 5-5. `task` 서브에이전트와 실행 한도
- 도구 `task(description, subagent_type)`(인자 둘, e3). 설명 글에 쓸 수 있는 서브에이전트 이름 목록(e3 `['general-purpose', 'source-reviewer']`)과 사용 규칙(「stateless」·「returns a single final report」·「Launch multiple agents concurrently」)이 들어감(`subagents.py` 285~297행).
- 서브에이전트 입력 = 부모 상태에서 `messages`·`todos`·`structured_response`·비공개 칸을 뺀 것 + `messages = [HumanMessage(description)]` → **`files`는 함께 씀**(e4). 출력 = 마지막 글 있는 `AIMessage`의 글 하나를 담은 `ToolMessage` + `files` 등 칸 갱신(474~512행).
- **실행 한도**: 부모의 `{"recursion_limit": N}`은 서브에이전트에 닿지 않음(선언형 서브에이전트는 `create_agent` 9999로 묶임 — e3). **호출 한도**: 선언형 스펙 `middleware`에 `ModelCallLimitMiddleware`를 넣으면 그 서브에이전트에만 걸림(e4). general-purpose에는 부모 `middleware=`가 옮겨 가지 않음(e5) — 이름 「general-purpose」 스펙을 직접 주면 기본을 바꿀 수 있음(독스트링).
- 스펙 칸(설치판 `SubAgent`, `subagents.py` 36~127행): `name`·`description`·`system_prompt`·`tools`·`model`·`middleware`·`interrupt_on`·`skills`·`permissions`·`response_format`. **공식 문서의 `mode`(isolated/forked)는 설치판 0.7.0에 없음**(문서가 새 판을 설명 — §5-7).

### 5-6. 권한·사람 승인·스트리밍
- `FilesystemPermission(operations=[…], paths=[…], mode="allow"|"deny"|"interrupt")`(`filesystem.py` 247~285행): 선언 차례대로 첫 규칙이 이김, 맞는 규칙이 없으면 허용. 경로는 `/`로 시작·`..`·`~` 금지. **파일 도구 안에서 판정**(백엔드 직접 호출에는 안 걸림 — e2). 서브에이전트는 스펙에 `permissions`가 없으면 부모 규칙을 물려받음. 명령 실행 백엔드와는 함께 못 씀(`NotImplementedError`, 1400~1407행).
- 사람 승인: `interrupt_on={"write_file": True}` 또는 `mode="interrupt"` → `HumanInTheLoopMiddleware`(노드 `HumanInTheLoopMiddleware.after_model`, e6) · 체크포인터 필요 · 이어 가기 `Command(resume={"decisions": [{"type": "approve" | "edit" | "reject" | "respond", …}]})`. **실행하지 않음**(모델 필요).
- 스트리밍: 그래프에 `stream`·`astream`(e3). 서브에이전트는 도구 함수 안에서 `invoke`되므로 그 사건은 `subgraphs=True`여야 보임(소스 설명 — 실행 안 함).

### 5-7. 공식 문서와 설치판의 차이 (2026-09-28 확인)
- 서브에이전트 문서의 `mode`(isolated/forked)·「forked는 부모 기록과 시스템 메시지를 물려받음」 — **설치판 0.7.0에 없음**(`task`는 늘 넘긴 글 한 줄로 시작). 개요의 「delete tool support」·계획 opt-in은 0.7과 맞음. 컨텍스트 문서의 20,000토큰·85%·10%는 설치판과 같음. → 본문은 **설치판 소스**를 근거로(규격 §3 「설치한 버전의 소스로 확인」), 문서와 다른 곳은 「이 과정 판(0.7.0)에서는」으로 한정.
- 0.7.0 릴리스 노트(2026-07-29 업로드 판): 계획 opt-in · 기본 글 비움 · 백엔드 팩토리 제거 · `write_file` 덮어씀 · `delete` 도구(쓰기 권한으로 판정) · `virtual_mode=True` 기본.

## 6. 07 deep research의 웹 검색 — 상황과 선택지

- **지금 판은 웹 검색을 하지 않습니다.** 조사 도구 `source_lookup`은 노트북 안 딕셔너리 `provided`(영어 한 문장씩 두 자료)를 ID로 찾아 내놓는 일반 Python 함수입니다. 루트 `.env`의 키 이름은 **`OPENAI_API_KEY` 하나뿐**(검색 API 키 없음, 값은 보지 않음). 잠금에 `tavily-python`·`markdownify` 없음(`httpx`는 있음).
- **규격 §3과의 관계**: 가짜 **모델**은 금지이지만 「도구 함수는 학생이 작성하는 일반 Python 함수이므로 정해진 값을 반환해도 됩니다」 → 고정 자료 도구는 규격 위반이 아님. 모델(부모·서브에이전트)은 실제로 부름. 단 「deep research」라는 이름이 웹 조사를 떠올리게 하므로 범위 한정 문장이 필요(지금 판 b4·b7이 이미 함).
- 공식 예는 Tavily(`TAVILY_API_KEY`)·`tavily-python`·`httpx`·`markdownify` + `TodoListMiddleware` + 연구 서브에이전트(동시 최대 3, 위임 최대 3바퀴, 검색 2~5번) + `/final_report.md`의 `[1]`·`### Sources` — 이 과정에서 따라 하려면 키 발급·잠금 변경·웹 결과 흔들림(같은 질문도 검색 결과가 바뀜)·요청 수 급증이 따름.

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **W1 고정 자료 도구 유지(한국어로)** | 지금 모양 — 교재용 짧은 자료 2~3개를 딕셔너리로, `source_lookup(source_id)` | 새 API 0 · 결정적 도구 · 요청 적음 | 「조사」 부분이 ID 조회 한 번이라 서브에이전트가 할 일이 적음 · 출처 ID가 이미 요청 글에 있음 |
| **W2 자료를 상태 파일로 넣고 기본 파일 도구로 찾기** | `invoke({"messages": …, "files": {"/sources/a.md": …, …}})` → 서브에이전트가 기본 `ls`·`grep`·`read_file`로 찾고, 부모가 `/research/final.md`를 상태에 씀(`StateBackend`, 디스크 0) | **새 도구 0** · 04~06(파일·옮겨 두기·위임)을 그대로 모음 · 출처 ID = 파일 경로 · 파일 쓰기 자리 문제 없음 · 서브에이전트와 `files` 공유(e4) | 파일 항목 모양(`content`·`encoding`·`created_at`·`modified_at`)을 손으로 만들어야 함(설치판 `create_file_data` 도움 함수는 과정 밖) · 모델의 `grep` 인자·차례가 흔들림 |
| **W3 과정 자료실 문서를 검색 도구로** | Ch 9~14 `labs/data/rag-corpus`(PDF 18개·`build/html` 18개) 또는 Ch 21 05 검색 함수를 도구로 | 앞 과정 자료와 이어짐 | **Part 6 묶음에 자료실 없음**(`public-files.json` 0줄) · PDF는 `pypdf`, 임베딩 검색은 `numpy`·임베딩 요청 — 잠금·묶음·요청 모두 늘어남 |
| **W4 실제 웹 검색(Tavily 등)** | 공식 예 모양 | 문서와 같음 | 키 없음(강사 결정·학생 발급) · 잠금 변경 · 결과가 날마다 바뀜 → 두 커널 비교·그림 라벨 불가 · 요청·비용 큼 |

## 7. 모델·비용 선택지와 흔들림 처리 (결정하지 않음 — 장단점만)

### 7-1. 모델 없이 결정적으로 보일 수 있는 것 (e1~e6에서 확인)
- 01: 설정마다 그래프 노드·도구 이름·`recursion_limit` 9999(키 셀 필요, 요청 0).
- 02: 기본 도구 아홉과 사용자 도구가 더해짐(도구 이름 목록) · 빈 기본 시스템 메시지.
- 04: `FilesystemBackend` 직접 쓰기·읽기·목록·덮어쓰기·루트 밖 거부 / `StateBackend` 파일이 상태 칸에 들어감(손으로 만든 도구 요청 + `ToolNode`).
- 05: 옮겨 두기 — 한도 200이면 안내 글 + 파일, 기본 한도면 그대로(호출 ID를 정해 파일 이름도 결정적).
- 06: `task` 도구 인자·서브에이전트 이름 목록 / `files` 공유(모델 없는 서브에이전트 그래프) / 부모 한도가 서브에이전트에 닿지 않음.
- 08: 권한 `deny` → `status` `success`·`error`, 차단 파일 없음.
- 모델이 있어야 보이는 것: 모델이 `write_todos`·`task`·파일 도구를 **고르는** 장면, 서브에이전트가 도구를 써서 보고를 쓰는 장면, 요약이 실제로 만든 글, 실제 요청·토큰·비용.

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **M1 모델 없음** | 여덟 절 모두 위 구조만 | 결정적 · 비용 0 · 흔들림 0 | 「하네스가 모델에게 도구를 쥐여 주고 모델이 고른다」는 챕터 목표가 안 보임 · 03 계획·06 위임·07 조사가 빈 껍데기 · 01 외 키 셀도 모델 객체 때문에 필요 |
| **M2 절마다 앞 절반 모델 없음 + 뒤 절반 실제 모델**(Ch 25·26 틀) | 01 모델 없음(키 셀만) · 02~08은 구조를 먼저 결정적으로 보이고, 한 번의 에이전트 실행으로 모델 선택을 봄 | 구조 값은 흔들림 0으로 결론·그림에 · 모델 장면은 실제로 · Ch 26 M2와 같은 틀 | 셀 수 늘어남(§2-7 「코드를 늘려 가면서 개선할 필요는 없다」) · 한 노트북에 두 조건 설명 |
| **M2′ 04·08도 모델 없음** | M2 + 04(파일)·08(권한)을 모델 없이만 | 파일 쓰기·권한 판정이 완전히 결정적 · 요청 적음 | 08 「통합 실행」이 에이전트 실행 없이 끝남 — 제목과 어긋남 |
| **M3 여덟 절 모두 모델 중심** | 지금 판 모양을 표준 모델 셀로 | 문서 예와 가까움 | 흔들림 최대(도구 차례·파일 이름·위임 여부·할 일 목록) · 결론이 모델 선택에 기댐 · 요청 최대 |

### 7-2. 흔들리는 값과 처리
- **흔들리는 값**: 할 일 목록(항목 글·개수·상태 차례·`write_todos` 부른 횟수) · 모델이 고른 파일 이름·경로(07 `final.md`는 요청 글이 정해 주면 흔들림 작음) · 도구 요청 차례·한 응답에 몇 개 · 위임 여부·어느 서브에이전트(general-purpose 포함)·몇 번 · 서브에이전트 보고 글 · 출처 목록(어느 자료를 인용했나) · 답 글·토큰·예상 비용 · 옮겨 둔 파일 이름(호출 ID — 서비스가 정함) · 안내 글 길이.
- **구조가 정하는 값**(모델 판단이 정해지면 코드로 정해짐): 한 번 실행의 요청 수 = 부모 모델 응답 수 + Σ(서브에이전트마다 그 안 모델 응답 수) (+ 요약이 켜지면 요약 요청) — 결과 목록에는 부모 응답만 있음 · 도구가 결과를 옮기는지(글자 수 > 4 × 한도) · 권한 판정 · `task`가 돌려주는 메시지 수(1) · 서브에이전트 입력 메시지 수(1) · 기본 도구 이름 · 한도로 멈춘 실행은 마지막 답 없음(Ch 26 05 셈).
- **규격 §2-7 9번 끝**: 결론·그림 라벨·캡션·정리·복습에는 새 커널 두 번 모두 같았던 값과 구조 값만. 할 일 글·파일 이름·요청 수·토큰·비용은 결과 읽기 둘째 단락·본문 표(「교재 출력」)·「확인할 점」·b7에만 「이번 실행에서는」. 그 값으로 「계획을 켜면 낫다」·「서브에이전트가 싸다」 같은 비교 결론을 쓰지 않음(Ch 26 04·05 선례 — 결론은 요청 수 셈).
- **규격 §2-7 10번 끝**: 결론에 쓸 모델 판단(「부모가 `task`를 한 번 부름」·「`write_todos`를 부름」·「두 번째 쓰기를 시도해 거부됨」)은 **입력을 확정하기 전에 노트북 밖에서 같은 요청 5번**으로 확인하고 `NN-probe.md` §0에 판단 규칙·그림 라벨 규칙을 **첫 요청 전에** 적음(Ch 25·26 선례, Ch 26 A-8 교훈). 원래 관찰이 5/5가 아니면: 입력을 고치기 전에 흔들림 확인 → 원래 관찰이 다시 나오면 입력 그대로 + b7 「같은 요청도 실행한 때에 따라 … 달라질 수 있다」 + 「…이면 …이 됩니다」 셈 한 문장.
- **흔들림을 구조로 줄이는 방법**(입력 설계, 결정은 작업자): 부모 도구에서 조회 도구를 빼 위임을 구조로 만들기 · general-purpose를 같은 이름 스펙으로 바꾸거나 설명으로 쓸 곳을 좁히기 · 요청 글에 파일 이름을 정해 주기 · 시스템 메시지 글에 「두 문장」처럼 길이 · 할 일 수를 정해 주기.

### 7-3. 서비스 요청·비용 어림 (요금표 2026-09-17 mini 입력 0.75·캐시 입력 0.075·출력 4.50달러/100만 토큰 — 청구 금액 아님)
- **요청 하나의 크기**: Deep Agent 요청은 도구 설명(파일 일곱 + `task` + 사용자 도구)이 커서 짧은 질문도 입력 **약 2,000~2,500토큰**(옛 07 부모 마지막 요청 입력 2,379 중 캐시 읽기 2,048). 요청당 약 0.0005달러(캐시가 대부분 맞을 때) ~ 0.002달러(캐시 없음, 출력 100토큰 안팎).
- **노트북 한 번(M2 어림)**: 01 0 · 02 2~4 · 03 3~6 · 04 0~3 · 05 2~4(요약을 켜 보이면 +1~2) · 06 4~8 · 07 7~10 · 08 2~4 → **약 20~39번**. **09 실습 절**: 실행 1·2가 서브에이전트를 쓰면 한 번에 4 안팎 → 8 안팎(규격 §7-2 3~5번 넘음 — 강사 확인), 부모만 쓰면 2~3 × 2 = 4~6.
- **절별 누적(새 커널 두 번 + 노트북 밖 흔들림 확인 다섯 번 + 개발 시도)**: 가장 큰 07 — 커널 둘 20 + 확인 다섯 40~50 + 시도 20 ≈ 80~90요청 × 0.0005~0.002 = **약 0.04~0.18달러**. 06 ≈ 60요청 ≈ 0.03~0.12달러. 나머지 절은 각 0.05달러 안. **절마다 1달러 안**. 챕터 전체 **약 250~350요청 · 약 0.15~0.7달러**(Ch 26 273요청·0.095달러보다 요청당 입력이 큼). 임베딩 0. 삽화 약 18크레딧(아홉 장, 재생성 1회씩이면 최대 36).
- **요청 수를 줄이는 방법**: 작은 과제(자료 둘·할 일 둘) · 요청 글에 도구·파일 이름을 정해 줌 · 부모 `middleware=[ModelCallLimitMiddleware(run_limit=N, exit_behavior="end")]` + 서브에이전트 스펙 `middleware`에도 한도(general-purpose는 따로 — §5-5) · `invoke(…, {"recursion_limit": N})`(부모 그래프만) · 흔들림 확인은 결론에 쓰는 한 요청만.
- **실행 시간**: 옛 셀 기준 에이전트 실행 2~10초. 흔들림 확인 다섯 번 × 07(10초 안팎)은 셸 180초 안. `run_section.sh`는 노트북 한 번 + 렌더·빌드·게이트라 07 새 판(요청 7~10)도 여유. 두 커널 실행은 호출을 나눔(PLAYBOOK §0).

## 8. §2-7 판단 근거 — 도구 파일

### 사실
- 지금 여덟 노트북은 서로 함수를 다시 쓰지 않음(정의한 함수는 `@tool` 넷뿐: 02 `course_lookup` · 05 `large_result` · 06·07 `source_lookup` — 06과 07은 **같은 이름·다른 본문**). 같은 모양 코드가 되풀이되는 곳: 준비 셀(설치·`.env`·판 출력 — 여덟 절), `LAB` 찾기(`next(…)` — 04·05·07·08), 도구 요청 이름 모으기(내포식 `[call for m in … for call in getattr(m, 'tool_calls', [])]` — 02·03·06), 도구 메시지 고르기(02·05·06·08).
- 개선하면 절 사이에 되풀이될 자리: 메시지 목록 출력(Ch 19 06 `show_messages` — 02·03·05~09) · 도구 요청 이름(Ch 19 04 `tool_call_names`) · 요청 수·토큰 합(Ch 19 05 `sum_usage` — 부모 목록) · 예상 비용(Ch 6 06 `estimate_cost`) · 메시지 종류 이름(Ch 26 01 `message_kinds`) · **이 챕터 새 함수 후보**: 에이전트의 도구 이름 목록·노드 이름 목록(01 → 02·03·09) · 상태 칸 `files`의 경로와 첫 줄 출력(04 → 05~09) · 할 일 목록 출력(03 → 07·09) · 부모·서브에이전트 요청을 한 목록에 적는 기록 훅(06 → 07·09, Ch 22 02 `record_model_input` 모양 — 훅은 Ch 22에서 학습 대상이었고 Ch 27에서는 도구) · 도구 메시지에서 이름·`status`만 뽑기(08 → 09).
- 노드·도구·에이전트·훅이 노트북 전역(`model`·기록 목록)을 읽으면 도구 파일로 옮길 수 없음(Ch 26: 노드·도구·에이전트는 노트북에 두고 04·05가 03·04 셀과 글자 같게 다시 적음 — 생성기 대조). 기록 훅은 기록 목록을 인자로 받을 수 없는 데코레이터 모양이라 노트북에 둘 가능성이 큼.
- **앞 챕터 도구 파일은 파일째 가져오지 않음**: Ch 26 `delegation_tools.py`(import는 되지만 Ch 26 요약 §13-6·계약) · Ch 25 `stream_tools.py`(계약·해시가 Ch 25에 묶임) · Ch 21 `runner_tools.py`(맨 위 `numpy` — Ch 27 잠금에 없음) · Ch 23 `checkpoint_tools.py`(SQLite). 규격 §2-7 3번대로 쓸 함수만 **같은 본문으로 옮기고 `# Ch N MM절에서 배웠습니다`**(Ch 26 `delegation_tools.py`가 Ch 21 판 넷을 글자 그대로 옮긴 선례).
- 과정의 도구 파일 이름(`find labs -name '*_tools.py'` + `guardrails.py`): `git_tools`(Ch 3)·`data_tools`(Ch 4, 실습 폴더 맨 위)·`llm_tools`(Ch 5·7·8)·`rag_tools`(Ch 9~15)·`guardrails`(Ch 16)·`agent_tools`(Ch 17)·`workflow_tools`(Ch 18)·`order_tools`(Ch 19)·`graph_tools`(Ch 20)·`runner_tools`(Ch 21)·`checkpoint_tools`(Ch 23)·`approval_tools`(Ch 24)·`stream_tools`(Ch 25)·`delegation_tools`(Ch 26). **안 겹치는 후보**: **`harness_tools.py`**(챕터 말 「하네스」, `labs/` 전체 0) · `deep_tools.py` · `research_tools.py`(07 소재에 치우침).
- 교훈(Ch 24 A-10·Ch 25·Ch 26 첫 판부터): 앞 절 생성기가 뒤 절이 함수를 더한 도구 파일을 덮어쓰지 않게 `strip_later_imports`·판마다 해시 대조·쓰기 가드 · 머리 설명 첫 줄을 「앞 챕터 함수」로만 쓰면 뒤에 이 챕터 함수가 더해질 때 모자란 말이 됨(Ch 24 A-13·Ch 25 A-14·Ch 26 A-18 — 첫 판부터 「앞 챕터와 이 챕터에서 배운 함수」로).
- 도구 파일을 만들면 가져오는 절은 **`os.chdir()` 전에 가져옴**(Ch 3) — 04 등 임시 폴더로 옮기는 절.

### 선택지 (결정하지 않음 — 장단점만)

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| A. 도구 파일 없음(Ch 2·4·6·22 선례) | 절마다 노트북에 | 목록·zip 변경 없음 | 02~09가 `show_messages`·`sum_usage`·`estimate_cost`(Ch 19·6 함수)를 다시 적으면 §2-7 3번과 충돌 |
| B. `harness_tools.py`에 앞 챕터 함수만 | `tool_call_names`·`show_messages`·`sum_usage`(Ch 19)·`estimate_cost`(Ch 6)(+ `message_kinds` Ch 26) — Ch 21/26 판 글자 그대로, import 0 | §2-7 3번을 지킴 · 02부터 가져옴 · numpy 없음 | 절마다 쓰는 함수가 달라 「이 절이 쓰는 함수는 …」 한정 문장 필요(Ch 21 01 A-1 선례) |
| C. B + 이 챕터 도움 함수 | 도구 이름·노드 이름 목록(01) · `files` 칸 출력(04) · 할 일 출력(03) · 도구 메시지 이름·`status`(08) | 07·08·09 코드가 가장 짧음 | 처음 가르친 절은 노트북에 남겨 판이 둘 · 생성기 대조 사슬이 길어짐 · 도구 이름 목록은 `agent.nodes["tools"].bound.tools_by_name`(과정 처음)을 도구 파일에 숨기게 됨 |

## 9. 과정 규칙과 부딪히는 것 (선택지와 장단점만)

### 9-1. 모델과 규격 §3 — §7 표. 모델은 과정 표준 객체를 넘길 수 있음(§5-2). 07만 문자열이라 Responses API로 바뀜.

### 9-2. 용어
- **하네스**: Ch 6 01이 이미 정의(모델 호출을 둘러싼 실행 틀 — 입력 준비·호출·결과 검사·기록) + 쟁반 비유. Ch 27은 그 정의를 이어 「긴 작업에 자주 쓰는 틀을 미리 조립해 둔 것(DeepAgents)」으로 좁혀 쓰는 편이 Ch 6 01 표·Ch 28 01 b3와 맞음. Ch 9 06 「실험 하네스」와 가르는 한 문장. 제목의 영어 「Harness」는 제목에만(강사 확인).
- **경로**: Ch 13 이후 금지어(「경로」 → 「차례·흐름·갈래」 — 뜻이 route). 그런데 Ch 27은 파일 위치(`/research/final.md`)를 줄곧 다룸. (가) 「파일 경로」는 Ch 10(Part 3, 14회) 선례로 파일 위치 뜻에만 허용하고 흐름 뜻 「경로」(지금 01 「조립 경로」 등)는 뺌 / (나) 「파일 위치」·「가상 위치」로 모두 바꿈 — 설치판·공식 문서 말(path)과 멀어짐. 「가상 경로」(virtual path — 루트 아래로 대응되는 `/…` 이름)는 새 말.
- **오프로딩(offloading)**: 영어 음차 새 말(05 12회). (가) 「옮겨 두기(offloading)」처럼 한국어 이름 + 원어 한 번 / (나) 음차를 새 용어로 정의. Ch 8 03 「줄이기(Compress)」와의 관계 한 문장. 「이빅션(evict)」은 소스 인자 이름에만.
- **서브에이전트·위임**: Ch 26 말(서브에이전트 = 도구로 감싸 부르는 전문 에이전트, 바깥/안쪽 목록) 그대로 이음 — Deep Agents `task`는 그 모양을 미리 만들어 둔 것. 「general-purpose」 서브에이전트는 이름 그대로(코드 값) + 「기본 서브에이전트」 풀이.
- **계획·할 일 목록**: 「플래닝」 → 「계획」, `todos` → 「할 일 목록」. Ch 18 04 「계획 모델」과 가름(Ch 18은 코드가 나눔).
- **백엔드**: 새 말(파일을 실제로 어디에 두는지 정하는 부품). 「상태 백엔드(StateBackend)」·「파일시스템 백엔드」 등 이름 붙이기.
- 그 밖 금지어 → 대체어: 반환 → 내놓다 · 측정 → 재다·세다 · 검증 → 검사·확인(Ch 16) · 스키마 → 입력 형식(Ch 19)·양식(Ch 21) · 런타임 → 실행 객체 표시(Ch 21 03)·실행 · 문맥 → 컨텍스트(Ch 8)·목록 · 격리 → 나누기(Isolate, Ch 8 03) · 영속 → 상태 저장(Ch 23) · 궤적 → 단계 차례(Ch 17 04) · 관측 → 보기·기록 · 표면 → (뺌) · 시그니처 → 인자 목록 · 메타데이터 → 칸(Ch 25 「칸 `metadata`」) · 페이지 → 쪽 · 임계 → 기준값 · 명시 → 적어 둔 · 보장 → (뺌) · 최대 → (뺌 / 한도) · 프롬프트 → 시스템 메시지(글)·요청 글 · 「opt-in」 → 「직접 더해야 켜짐」.
- **한도 말 셋**(Ch 26 요약 §4): 실행 한도(그래프 단계 수, Deep Agents 9999) · 호출 한도(한도를 붙인 에이전트 요청 수) · 바퀴 한도(루프 바퀴) — 08 md 「최대 반복 수」를 어느 것인지로.

### 9-3. 파일 쓰기 자리
- 규격·선례: 파일은 임시 폴더(Ch 23·24 준비 셀 `mkdtemp(prefix="chNN-MM-")`), 실행마다 새 파일 이름(Ch 23 `new_prefix`). 지금 판은 실습 폴더(연결 폴더)에 쓰고 쌓임(05 여섯 개), 04·07이 같은 폴더를 씀.
- (가) **`StateBackend`(기본)로 파일 장면을 상태 칸에** — 디스크 0, 노트북 사이 의존 0, 결과 `result["files"]`로 출력(03·06·07·08·09) / (나) **`FilesystemBackend(root_dir=tempfile.mkdtemp(prefix="ch27-04-"))`** — 디스크에 실제로 생기는 것을 보여야 하는 04(와 05)만 / (다) 지금처럼 실습 폴더 — 규격 선례와 어긋나고 학생 묶음을 풀어 돌리면 `part6-practice/labs/…/workspace*`가 생김. 임시 폴더로 `os.chdir()`하면 `.env`를 못 찾으니 키 셀을 먼저(§2 04).
- 옛 `workspace*` 폴더는 지우지 않음 — 마감 삭제 승인 목록.

### 9-4. 제목·슬러그
- 챕터 제목 「DeepAgents — Harness 계층」 · 02 「create deep agent와 도구」 · 03 「플래닝과 시스템 프롬프트」 · 05 「…오프로딩」 · 07 「출처 검증형 deep research」. **01 슬러그는 Ch 26 05 b8 링크로 고정**. 02~08 슬러그는 Part 6 목차만 링크(다시 만들어짐)·옛 기록 파일만 적음 → 바꿀 수 있음(강사 확인). 챕터 제목을 바꾸면 Ch 6 01 표(완료)와 글자가 달라짐 → 인계. 선례대로 「제목에만 남음(강사 확인)」 + 본문 첫 자리 풀이가 가장 작은 변경.

### 9-5. 문법·셀 모양
- `@tool` 함수 매개변수 `: str`만 허용(Ch 19 01) — 02 `chapter: int`는 `: str`로 바꾸거나 한 문장, 반환 힌트 `-> str` 뺌 · `next(…)`·별표 풀기 없이(Ch 26은 `LAB`을 찾지 않고 도구 파일·`notebooks/` 기준, Ch 10~12는 `candidates` + `for`·`break`) · 내포식·`getattr`·`any`·`all`·`sum`·`.get` 없이(Ch 26 「쓰지 않은 것」) · `re.search` 대신 도구 메시지 칸이나 알려진 경로(호출 ID를 우리가 정하면 필요 없음) · f-string 없음(Ch 13~26 0건) · 준비 네 셀 · 모델 셀은 `nbkit.key_and_model_cells()`.
- 새로 쓰게 될 이름(쓰면 첫 자리 풀이): `create_deep_agent`·`subagents=`·`backend=`·`permissions=`·`FilesystemBackend`·`StateBackend`·`FilesystemPermission`·`TodoListMiddleware`·상태 칸 `files`·`todos`·`task` 도구 · (쓰면) `agent.nodes["tools"].bound.tools_by_name`·`ToolNode(…, wrap_tool_call=…)`·`CompositeBackend`·`HumanInTheLoopMiddleware` 이어 가기 모양.
- `assert`: 모델 글·모델이 쓴 인자·모델이 쓴 파일 글에 걸지 않음(06·07·08 지금 판 위반) · 모델 선택(도구 이름·위임)도 흔들리는 값 → 구조 값(도구 이름 목록·노드 이름·`status`·파일 있음·메시지 수)과 키 셀에만(Ch 21~26 선례).

### 9-6. 03 「65%」와 「측정」
- PR 숫자를 다시 계산하는 셀은 이 과정이 잰 값이 아님. (가) 본문 인용 한 줄 + 링크(셀·`assert` 뺌) / (나) 이 과정 모델로 계획 없는·있는 에이전트 첫 요청 입력 토큰을 직접 세어 봄(요청 2 — 「계획을 켜면 입력이 늘어난다」는 구조 값: `TodoListMiddleware` 안내 글이 붙음) / (다) 지금처럼 — 「측정」·손 값 `assert`.

### 9-7. 참고 자료 b10
- 여덟 절이 같은 여섯 → 절마다(01 개요·릴리스 · 02 개요·`create_deep_agent` 독스트링 · 03 릴리스·PR #5009 · 04·05 백엔드·컨텍스트 문서 · 06 서브에이전트 문서 · 07 deep research 문서(웹 검색 예 — 이 과정 범위 밖 표시) · 08 권한·HITL 문서). 확인일 새로(이 조사 2026-09-28). 문서가 설치판보다 새 판인 곳(§5-7) 표시.

### 9-8. 실습 절 요청 수
- Deep Agent 한 번 실행에 요청이 여럿(부모 2 + 서브에이전트 2 안팎) → 실습 절 실행 1·2가 서브에이전트를 쓰면 8 안팎 → 규격 §7-2 「3~5번을 넘으면 까닭을 진단에 적고 강사 확인」(Ch 14 10절 선례). 줄이려면 실습 절을 부모 한 에이전트(파일·권한·할 일 목록) 중심으로 하거나, 실행 2를 모델 없는 구조 값(권한·한도) 하나만 바꾼 실행으로.

## 10. 삽화 비유 계열 후보

**이미 쓴 계열**(과정 요약 §5·계약 20행·Ch 22~26 요약): Ch 3 창고 선반 · Ch 4 쟁반·카드 상자·서류철 · Ch 5 나무 쟁반·블록 · **Ch 6 도서관 상담 창구(쟁반 = 하네스·서류철 = 컨텍스트·회전판 = 루프)**·우편함·구슬·나무 레일·저울 · Ch 7·8 한 책상 색 약속 · Ch 10 도막 · Ch 11 흰 카드/색 딱지 · Ch 13 작업대·갈림길 나무 길 · Ch 14 나무판·마개 · Ch 15 사과·저울·바구니·모래시계 · Ch 16 쪽지·도장·개찰구·체 · Ch 17 눈 위 발자국 · Ch 18 도자기 가마·물레 · Ch 19 식당 주문 전표와 내주는 창 · Ch 20 자료실 승강 상자 · Ch 21 세탁기 · Ch 22 공항 검사·우편 가림막·전화 연결·방문자 명부·두 겹 봉투·서류함·메모 정리 책상 · Ch 23 체스판·즉석사진 · Ch 24 도미노 줄·비워 둔 자리 · Ch 25 대나무 홈통·물방울 · Ch 26 항구의 예인선·바지선. 선례: 사람·손·동물·화면·글자·숫자·시계·화살표 없음.

| 후보 | 그림 요소(절별) | 장점 | 겹침·위험 |
|---|---|---|---|
| **A. 온실과 모종판** | 01 물뿌리개·선반·호스·모종판이 미리 갖춰진 온실(하네스) · 03 씨앗 봉투를 차례로 꽂은 줄(할 일 목록 — 글자 없이 봉투 색으로) · 04 칸마다 모종이 자라는 모종판(파일에 둔 중간 결과) · 05 큰 퇴비 자루는 헛간으로 옮기고 꼬리표 끈만 온실에 남김(옮겨 두기) · 06 작은 화분 하나를 옆 작은 온실에 맡겼다가 다 자란 한 포기만 돌아옴(서브에이전트) · 08 잠긴 울타리 문(권한) | 식물·원예 계열 0건 · 「미리 갖춘 틀 / 칸에 두기 / 옮겨 두기 / 맡기기」가 한 장소에서 읽힘 | 「자람」이 시간 흐름으로 읽혀 걸린 시간을 연상할 수 있음 · 모종판 칸 수가 뜻을 얻지 않게(그림 읽기에 밝힘) |
| **B. 공구 벽과 칸 서랍 수레** | 01 공구가 미리 걸린 구멍판 벽(하네스) · 03 체크 칸만 있는 빈 판(할 일) · 04 칸 서랍에 반쯤 만든 부품(중간 결과) · 05 큰 상자는 창고 선반으로, 수레에는 꼬리표만 · 06 작은 공구 가방을 옆 작업대로 보내 완성 부품 하나만 돌아옴 · 08 자물쇠 걸린 서랍 | 「미리 걸어 둔 공구」가 하네스에 가장 가까움 | Ch 13 작업대·Ch 3 창고 선반·Ch 22 서류함과 소재가 가까움 · 공구가 많아 관계와 무관한 요소가 늘기 쉬움(「no signs, no labels」) |
| **C. 캠핑 트레일러** | 01 장비가 다 실린 트레일러(하네스) · 03 냉장고 문 자석판에 붙인 빈 카드 줄 · 04 수납 칸 · 05 지붕 짐칸으로 올린 큰 짐 · 06 작은 짐수레를 근처 샘터에 보내 물통 하나만 돌아옴 · 08 잠긴 짐칸 | 「필요한 것을 다 싣고 긴 여행을 떠남」이 긴 작업과 맞음 | 운송 계열(Ch 20 승강 상자·Ch 26 항구)과 가까움 · 차량이 크고 세부가 많아 판독이 어려울 수 있음 |
| **D. 화물 열차 편성** | 01 기관차 뒤 역할이 다른 칸이 미리 이어진 열차 · 04 창고 칸 · 05 곁선로에 떼어 둔 큰 화물칸 · 06 지선으로 보낸 작은 궤도차가 상자 하나만 싣고 돌아옴 · 08 닫힌 건널목 차단기 | 칸 연결이 「미리 조립」을 보임 | Ch 26 항구(배·짐)와 같은 운송 계열로 읽힘 · 03 계획을 담을 요소가 약함 |

- 스타일 문구는 규격 §5-4 그대로. **Ch 6 01 「쟁반 = 하네스」와의 관계**를 01 그림 읽기 한 문장으로(「Ch 6의 쟁반보다 큰, 미리 갖춘 틀」). 크레딧: 절마다 1장(01~09) 약 18크레딧, 재생성 1회씩이면 최대 36.

## 11. 위험과 깨진 것

1. **01 검사 방법 결함** — 소스 문자열 검색이 독스트링·주석까지 세어, 조립하지 않는 `TodoListMiddleware`도 `True`. 「일곱 기능 True 7」은 조립 여부를 보이지 못함(§2 01).
2. **흔들림을 `assert`로 굳힌 절** — 02·03·05·06 모델 선택, 06 보고 글 속 단어·07 모델이 쓴 파일의 제목·08 모델이 채운 인자 글(규격 §3 위반). 노트북 밖 되풀이 확인 기록 없음.
3. **모델 설정 누락** — 여섯 절 모두 `temperature=0`·`reasoning_effort="none"` 없음(07은 문자열이라 Responses API로 바뀌고 게이트도 못 잡음).
4. **실습 폴더(연결 폴더)에 쓰기·쌓임·실행 차례 의존** — 04·05·07·08. 04 목록에 07 파일이 섞이고, 05 파일이 실행마다 늘어 여섯. 학생 묶음을 풀어 돌려도 `workspace*`가 생김.
5. **요금 사고 가능성** — Deep Agents 부모 그래프 실행 한도 9999, **서브에이전트에는 부모 한도가 닿지 않고**(묶인 9999), **general-purpose 서브에이전트에는 부모 `middleware=`의 호출 한도도 옮겨 가지 않음**. 모델이 위임을 되풀이하면 요청이 크게 늘 수 있음 → 부모 호출 한도 + 선언형 서브에이전트 스펙 한도 + (general-purpose를 쓰면) 같은 이름 스펙으로 바꿔 한도.
6. **요청 수 세기 누락** — 부모 결과 목록에는 서브에이전트 요청이 없음(06·07). README 「부모 마지막 메시지 사용량 ≠ 전체」는 바르지만 전체를 세는 셀이 없음.
7. **같은 이름 미들웨어 교체의 부작용** — `middleware=[FilesystemMiddleware(…)]`는 기본 자리를 바꾸면서 `permissions=` 판정을 잃음(05 모양을 08·09에 합치면 권한이 사라짐). 요약 미들웨어도 같은 이름이면 바뀜.
8. **문서와 설치판 차이** — 서브에이전트 `mode`(forked) 등 공식 문서가 0.7.0보다 새 판(§5-7). 문서만 보고 쓰면 실행 안 되는 코드·틀린 설명.
9. **용어** — 「반환」·「측정」·「검증」·「문맥」·「경로」·「스키마」·「런타임」·「격리」·「프롬프트」 등 · 「오프로딩」 새 음차 · 「하네스」 두 뜻(Ch 6 ↔ Ch 9 06) · 제목 영어(Harness·deep research·create deep agent) · 07 자료·요청 글·산출 파일이 영어.
10. **손 값** — 03 PR 숫자 64.9%·65%를 셀로 계산해 `assert` · 05 「약 1,600자」 · 07 사용량 2,379·34·2,413(README·b6)과 `집필점검표.md` 2,498·38 어긋남 · `qa/verification.md` 04·05·07·08 해시가 지금 노트북과 다름 · `집필점검표.md` 「24개 코드 셀」(실제 36).
11. **Ch 24 이음** — 08 b3 「사람 승인과 permissions는 도구 실행 경계」 부분 참. Deep Agents 승인은 `HumanInTheLoopMiddleware`(`decisions` 모양, 새 API, 체크포인터 필요).
12. **웹 검색 의존 없음(좋음) / 이름과 범위 차이** — 「deep research」가 웹 조사를 떠올리게 함. 실제 웹 검색은 키·잠금·흔들림 문제로 재현 불가(§6).
13. **실행 시간·셸 180초** — 옛 에이전트 실행 2~10초. 흔들림 확인 다섯 번 × 07은 한 호출 안(여유 작음 — 새 판에서 요청이 늘면 나눔). 07 새 판이 서브에이전트 둘·파일 쓰기면 한 번 15~30초 어림.
14. **서비스 요청·비용** — 요청당 입력 2,000토큰 이상(도구 설명). 챕터 전체 약 250~350요청·약 0.15~0.7달러(§7-3), 절마다 1달러 안. 09 실습 절이 3~5번을 넘을 가능성.
15. **뒤 챕터 계약** — 파일 계약 없음(Ch 28~31·34·Part 7 코드가 Ch 27 파일을 안 읽음). 문장만: Ch 26 05 b8(01 슬러그·「미리 묶어 둔 기능」) · Ch 6 01 표(챕터 제목 글자) · Ch 28 01 b3(「파일시스템과 하위 작업 기능을 미리 조립한 하네스」) · `continuity-guide.md` 8·12·13행.
16. **옛 생성기** — `qa/author_ch27.py`는 덮어쓰기를 스스로 막지만(대상 파일이 있으면 `FileExistsError`) 규격 §8대로 막고 옮길 대상. `figures/_gen_figures.py`도 같음. 공용 옛 생성기는 없음(`_author_ch21_ch29.py`는 Ch 27 안 씀).
17. **기기 디스크** — 루트 여유 **2.3G(작업 전후 같음)**. 가상환경 292MB는 사용자 디스크(`$ROOT/.cache/vm`, 여유 67G)에, 기기 `/tmp/ch27-prep` 216KB. 절 실행(`run_section.sh`)은 `.cache/vm` 환경을 자동으로 씀. Mermaid 도구 `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/libs`·`/tmp/pw*`는 기기에 있음(Ch 26 작업분). 삽화 받기·PNG 확인은 `/tmp`에 몇 MB.

## 12. 01절 작업자가 먼저 결정해야 할 것

1. **모델과 흔들림(§7)** — M1 / **M2(01 모델 없음·키 셀만, 02~08 앞 절반 구조 + 뒤 절반 실제 모델)** / M2′ / M3 가운데 하나, 과정 표준 모델 **객체**를 `create_deep_agent(model=…)`에 넘기기(문자열 금지 — §5-2), 요금 사고 막기(부모 `ModelCallLimitMiddleware` + 서브에이전트 스펙 한도 + general-purpose 처리 — §5-5), 흔들림 확인 규칙을 `NN-probe.md` §0에 첫 요청 전에. 요청 수를 셀 방법(부모 목록 + 서브에이전트 기록 훅 — Ch 22 02 모양).
2. **파일 쓰기 자리(§9-3)** — 실습 폴더 `workspace*` 대신 (가) `StateBackend` 상태 칸 / (나) `FilesystemBackend(root_dir=tempfile.mkdtemp(prefix="ch27-NN-"))` / 둘을 절마다 나눔. 키 셀을 임시 폴더 이동보다 먼저. 04가 07 결과에 기대지 않게.
3. **01 설계와 분류(§2 01)** — 문자열 검색을 버리고 설정마다 노드 이름·도구 이름을 출력하는 모델 없는 비교로 할지 · 「일곱 기능」 분류를 둘지(공식 넷·설치판 기본 넷 + 선택 넷) · 하네스 정의를 Ch 6 01에서 이어 받고 Ch 9 06 「실험 하네스」와 가르는 문장 · 01 슬러그 고정.
4. **용어와 제목(§9-2·9-4)** — 「경로」(파일 위치 뜻 허용 여부)·「가상 경로」 · 「오프로딩」 이름 · 「계획·할 일 목록」 · 「백엔드」 · 한도 말 셋 · 제목 영어(Harness·create deep agent·플래닝·프롬프트·deep research) 제목에만 둘지 · 03 65% 처리(§9-6). `handoff.md`에 용어 표로 먼저.
5. **07 설계(§6)** — W1(고정 자료 도구, 한국어로) / **W2(자료를 상태 파일로 넣고 기본 파일 도구로 찾기)** / W3 / W4 · 서브에이전트 수·부모가 조회 도구를 가질지(위임을 구조로 만들지) · 도구 파일(§8 A/B/C, 이름 후보 `harness_tools.py`, 첫 판부터 생성기 대조 사슬) · **옛 생성기 `qa/author_ch27.py`·`figures/_gen_figures.py` 첫머리 막기**(설명 주석 + `raise SystemExit(...)`).

## 13. 챕터 마감으로 미룰 것

- **09 실습 절 신설**(규격 §7-2): 슬러그 후보 **`09-DeepAgents-실습`**(챕터 제목 머리말 「DeepAgents」 — `_notebook/build_index.py` 짧은 이름과 같음; 선례 `09-Middleware-실습`·`07-create-agent-실습`·`04-Streaming-실습`처럼 영어 제목 말 그대로, `05-위임-구조-실습`·`07-워크플로우-패턴-실습`처럼 한국어 머리말) · 다른 후보 `09-하네스-실습`. 제목 「DeepAgents 실습: …」, `format: experiment`, meta 「실습 30분 · 새 용어 0」(**챕터 시수 8·16h에 더하지 않음**). 새 문법·API 0, 요청 3~5번이 넘을 가능성(§9-8 — 강사 확인). 주제 예 — 01~08 소재를 이어 조사 에이전트 하나에 「상태 파일로 받은 자료 → (서브에이전트) → 보고서 파일 · 권한으로 막을 곳 · 호출 한도」를 조립하고, 실행 2는 값 하나(예: 권한 규칙 하나·호출 한도 하나·옮겨 두기 한도)만 바꿈.
- 옛 생성기 `qa/author_ch27.py`·`figures/_gen_figures.py` → `qa/upgrade/before/generators/blocked/`(`mv -n`, 해시 기록 — `45453725…`·`45d40ea2…`).
- 옛 그림 24개(`figures/0N-흐름.{svg,excalidraw,caption.md}`, N=1~8) 삭제 승인 목록(사본 `before/figures/`, `final-artifact-hashes.json`이 해시를 적은 기록 파일). 챕터 공개 목록에 옛 SVG 줄은 **원래 없음**.
- 실습 폴더 `workspace/`·`workspace-05/`·`workspace-08/`(9파일) 삭제 승인 목록(사본 `before/workspace*/`, 읽는 코드 0).
- `chapter.json` `objectives`(「deep research」·「비용과 한계를 기록」) · 절 제목 · `textbook/part6/_build_index.py` 25행 설명 · `_notebook/build_index.py` 58~59행 설명(절 수 8 그대로 — 실습 절 빼고 세는 약속) · 챕터 목차를 개선 본문과 대조 → `_build.py`·`_build_index.py`.
- 실습 폴더 README 다시 쓰기(노트북 아홉, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 절마다 요청 수·키 필요 여부, 「예상 비용」, 도구 파일 단락, **파일이 생기는 자리 문장을 새 판대로** — 지금 README 「04·05·07·08절은 … workspace …를 자동으로 만듭니다」) · `labs/part6/continuity-guide.md` 13행(새 본문과 대조) · `qa/research.md`·`technical-review.md`·`verification.md`·`집필점검표.md`에 「개선 전 판」 표시.
- Part 6 공개 목록에 09·(도구 파일) 줄 → `part6-practice.zip` 다시 만들기(마지막에 한 번) → `check_delivery.py`(`llm-practice.zip` Stale 예상) · 묶음을 풀어 09 첫 셀 확인 · 옛 검사 넷 돌려 기록(`check_notebook_readiness.py` 결과 파일 되돌림). 묶음 실행 검사에 모델 없는 절(01)을 넣을지는 전체 마감 후보 — 모델 객체 셀이 키 없이 멈추는 점 함께(강사 확인).
- **뒤 챕터 인계**(고치지 않음): Ch 28 01 b3(「하위 작업」 말) · Ch 6 01 표(챕터 제목을 바꾸면) · `continuity-guide.md` · Part 6 소개·`practice-start.md`(참) · Ch 26 05 b8(01 슬러그·내용).
- 삭제 승인 대상: 실습 폴더 `.venv`(macOS 215MB) · `qa/__pycache__/author_ch27.cpython-312.pyc` · `qa/upgrade/gates-wip-*.json` · `.cache/vm/venv-ch27-deepagents`(292MB) · 기기 `/tmp/ch27-prep`(216KB — 확인 스크립트·임시 폴더 `exp/ch27-e2-*`·`exp/ch27-e6-*`).

## 14. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 8 · `notebooks` 8 · `figures` 25(SVG·excalidraw·caption 각 8 + `_gen_figures.py`) · `generators` 2(`author_ch27.py`·`_gen_figures.py`) · `qa` 4(`public-files.json`·`research.md`·`technical-review.md`·`verification.md`) · 실습 폴더 3(`pyproject.toml`·`uv.lock`·`README.md`) · **`workspace` 2 · `workspace-05` 6 · `workspace-08` 1** · `chapter.json`·`_build.py`·`index.html`·`집필점검표.md` = **63개, 937,195바이트**. 원본과 `cmp` 모두 같음. Ch 26 모양을 따름(절 HTML은 넣지 않음 — 보호 파일 목록에 해시) |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 245, 통과 0/8), `915e2c70…` |
| `qa/upgrade/before-manifest.json` | sha256 **238개**(`0484871c…`) — ① 이 챕터 실습 폴더(README·잠금 둘·노트북 여덟·`workspace*` 9)·원고(`_src`·HTML·목차·`chapter.json`·`_build.py`·점검표·그림 25·`qa/` 다섯) ② 이 챕터가 읽거나 이어 쓸 앞 챕터 파일: Ch 26 도구 파일·잠금 둘·노트북 다섯·`_src` 다섯 · Ch 25·24·23·21·20·19 도구 파일 · Ch 24·23 01·Ch 21 01~03·Ch 22 01~08 노트북과 `_src` · Ch 19 01·04·05·06·Ch 17 03·Ch 8 03·Ch 6 01·06 노트북 · Ch 8 03 `_src` ③ Ch 27을 가리키는 완료 챕터 파일: Ch 6 01 `_src`·HTML·요약 · Ch 26 05 HTML·`author_04.py`·`author_05.py`·준비 조사 · Ch 21~26 요약 ④ Ch 27에 기대는 뒤 챕터·Part·과정 파일: Ch 28 01 `_src`·HTML·`author_ch28.py` · 연속성 안내 · Part 6 소개·목차·`practice-start.md` · 목차 스크립트 둘·`build_bundle.py`·`textbook/index.html` · 목록 셋 · zip 둘 · Part 6 `qa/` 기록 전부(JSON·`verification.md`·`integration-review.md`·`ch27-technical-review.md`·언어 기록)·옛 검사 스크립트 일곱 · Part 7 기록 셋 · 검사 기록(`notebook-contracts-…-ch27-…json`·`checks/ch27-deepagents/`)·`part6b_*.py` 넷 · `part5/_figure.py`·`_template/builder.py` ⑤ 규격·과정 문서·공용 도구(`upgrade/`·게이트·`verify.py`·`execute.py`·`render.py`·`visual.cjs`·Mermaid 도구)·`.env.example` |
| `qa/upgrade/chapter-lead-notes.md` | 이 파일 |
| `$ROOT/.cache/vm/venv-ch27-deepagents` | Python 3.12.13 · 292MB |

### 가상환경 만든 방법과 결과
- Ch 26 준비와 같은 방법: `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy uv venv --python 3.12.13 …/venv-ch27-deepagents` → `uv pip install --python …/bin/python pip==26.2` → 잠금 목록 `uv export --project labs/part6/ch27-deepagents --frozen --no-hashes --all-groups --no-emit-project`(실습 폴더 파일 그대로 — 수정 시각 09-10 그대로), 주석 줄만 뺀 100줄(`/tmp/ch27-prep/req-clean.txt`, 환경 표시 `; sys_platform == …` 유지) → **`bin/python -m pip install --no-cache-dir -r`**(한 호출, 170초 안에 끝남). 설치 오류 0, **`uv cache prune` 안 함**(`/tmp/uv-cache` 53MB는 원래 있던 것).
- 크기 어림(만들기 전): Ch 26 환경 238MB + deepagents·Anthropic·Google·cryptography 13개 → 약 280~300MB, 사용자 디스크(여유 67G)라 기기 루트 여유(2.3G)는 거의 그대로일 것 → 만듦. **기기 루트 디스크 여유 2.3G(전후 같음)**.
- 결과: `pip freeze --all`과 잠금 대조 **판 차이 0**(설치 97 = 잠금 100 − 이 기기에 해당하지 않는 셋: `appnope`(darwin)·`colorama`(win32)·`httpx2-jsfetch`(emscripten); `cffi`·`pycparser`는 CPython 표시라 설치됨). `deepagents 0.7.0`·`langchain 1.4.0`·`langchain-core 1.6.2`·`langchain-openai 1.6.0`·`langgraph 1.2.11`·`langgraph-prebuilt 1.1.0`·`langgraph-checkpoint 4.2.0`·`langchain-anthropic 1.7.1`·`langchain-google-genai 4.4.0`·`wcmatch 11.0.1`·`python-dotenv 1.2.3`·`ipykernel 7.3.0`·`nbclient 0.11.0`·`pip 26.2`. `pip check` 이상 없음. 커널 스펙 `share/jupyter/kernels/python3` 있음.
- import 확인만(`env -u OPENAI_API_KEY`): `create_deep_agent`·백엔드 다섯(`FilesystemBackend`·`StateBackend`·`CompositeBackend`·`StoreBackend`·`LocalShellBackend`)·`FilesystemMiddleware`·`FilesystemPermission`·`SubAgentMiddleware`·`SubAgent`·`CompiledSubAgent`·Deep Agents `SummarizationMiddleware`·`create_summarization_middleware`·`DeepAgentState`·`create_agent`·`TodoListMiddleware`·`ModelCallLimitMiddleware`·`HumanInTheLoopMiddleware`·`wrap_model_call`·`after_model`·`init_chat_model`·`tool`·`ToolRuntime`·메시지 셋·`Command`·`InMemorySaver`·`GraphRecursionError`·`get_usage_metadata_callback`·`dotenv`·`ipykernel`·`nbclient`·`pip` 모두 됨. `numpy`·`tavily`·`PIL`·`langgraph.checkpoint.sqlite`·`markdownify`는 없음(잠금대로), `httpx`는 있음. 모델 객체는 키 없이 만들면 `OpenAIError`(가짜 키 글로 만들기만 확인, 요청 0). 루트 `.env` 키 이름은 `OPENAI_API_KEY` 하나(값은 보지 않음). `run_section.sh`는 `$ROOT/.cache/vm/venv-<챕터 폴더 이름>`을 자동으로 씀.

### 참고 자료 (2026-09-28 확인)
- Deep Agents 개요 `https://docs.langchain.com/oss/python/deepagents/overview` — 「agent harness」 = 「the same core tool calling loop … with built-in capabilities」 · 제목 넷 Execution environment·Context management·Delegation·Steering · 「Starting in v0.7 task planning is opt-in only」. 판·날짜 표시 없음. 웹 검색 언급 없음.
- Deep Agents 서브에이전트 `https://docs.langchain.com/oss/python/deepagents/subagents` — isolated(기본)/forked `mode`(**설치판 0.7.0에 없음**) · general-purpose 자동 추가·`GeneralPurposeSubagentProfile(enabled=False)` · 스펙 칸(`name`·`description`·`system_prompt`·`mode`·`tools`·`model`·`middleware`·`interrupt_on`·`skills`·`response_format`·`permissions`) · 도구·권한·`interrupt_on`은 물려받고 스킬은 안 물려받음 · 「issue several … in a single turn to run them in parallel」 · 한도에 대한 문장 없음 · Tavily 예(`internet_search`).
- Deep Agents 컨텍스트 `https://docs.langchain.com/oss/python/deepagents/context-engineering` — 「tool call results exceed 20,000 tokens」 → 경로 + 앞 10줄 미리보기 · 「Triggers at 85% of the model's max_input_tokens」·「Keeps 10%」.
- Deep research 예 `https://docs.langchain.com/oss/python/deepagents/deep-research` — `TAVILY_API_KEY`·`tavily-python`·`httpx`·`markdownify` · `TodoListMiddleware` · `/research_request.md`·`/final_report.md` · 인용 `[1]`·`### Sources` · 동시 최대 3·위임 최대 3바퀴·검색 2~5번. 예 폴더 `https://github.com/langchain-ai/deepagents/tree/main/examples/deep_research`.
- deepagents 0.7.0 릴리스 `https://github.com/langchain-ai/deepagents/releases/tag/deepagents%3D%3D0.7.0` — 계획 opt-in · 기본 글 비움 · 백엔드 팩토리 제거 · `write_file` 덮어씀 · `delete` 도구 · `virtual_mode=True` 기본(잠금의 업로드 2026-07-29).
- 설치판 소스(`deepagents 0.7.0`): `graph.py` 182~199행(`_merge_fs_interrupt_on`)·201~235행(`_apply_custom_middleware` — 같은 이름은 자리 바꿈)·238~265행(`_REQUIRED_MIDDLEWARE`)·268~580행(`create_deep_agent` 서명·독스트링 — 기본 도구·미들웨어 차례)·584~627행(모델·프로필·기본 `StateBackend`)·628~640행(도구 안내 글 없음 주석)·647~748행(선언형 서브에이전트 스택·물려받기)·750~814행(general-purpose)·816~920행(주 스택)·922~944행(`create_agent` + `recursion_limit` 9999) · `_models.py` 35~57행(객체는 그대로, 문자열은 제공자 설정) · `profiles/provider/_openai.py`(`use_responses_api=True`) · `profiles/harness/_openai_codex.py`(codex 모델만) · `middleware/filesystem.py` 99~105행(도구별 읽기/쓰기 판정)·247~299행(`FilesystemPermission`·`_check_fs_permission`)·640행(`NUM_CHARS_PER_TOKEN = 4`)·1199~1206행(옮기지 않는 도구)·1269~1450행(`FilesystemMiddleware` — 기본 한도 20000·50000)·2405~2430·2690~2715행(`execute`·`delete`를 모델 요청에서 빼기)·2813~2850행(옮기기 판정)·3136~3160행(`wrap_tool_call`) · `middleware/summarization.py` 249~286행(`compute_summarization_defaults`)·487~600행(요약 미들웨어·`/conversation_history`)·1594행(`SummarizationMiddleware` 별칭)·1601~1671행(`create_summarization_middleware`) · `middleware/subagents.py` 36~127행(`SubAgent` 칸)·252~269행(넘기지 않는 칸)·285~305행(`task` 설명·general-purpose)·340~385행(서브에이전트 컴파일)·474~512행(돌려주는 `Command`)·530~567행(`task` — 넘긴 글 한 줄·설정 `ls_agent_type`·묶인 설정이 이김) · `backends/state.py` 37~120·205~220행 · `backends/filesystem.py` 90~210행(`virtual_mode`)·495행(`write` 덮어씀) · `backends/composite.py` 178~230행 · `backends/protocol.py` 867행(`_supports_delete`). (`langchain 1.4.0`) `agents/middleware/todo.py` 31·61~131·203~252행 · `agents/middleware/human_in_the_loop.py` 51~134행(`decisions`) · `agents/middleware/model_call_limit.py` 94행.
- 모델 없는 확인 파일(기기 `/tmp/ch27-prep/exp/`): `e1_default.py`(기본 미들웨어·도구·노드·빈 시스템 글·9999·모델 프로필 400000·문자열 모델 Responses API) · `e2_backends.py`(`FilesystemBackend` 쓰기·덮어쓰기·루트 밖 거부 · 권한 `deny` · 백엔드 직접 쓰기는 권한 밖 · `StateBackend` 상태 칸 · 옮겨 두기 한도 200/기본 · `execute` 빼기) · `e3_subagents.py`(부모 한도가 묶인 서브에이전트에 안 닿음 · `task` 인자·설명 · `interrupt_on`·권한 interrupt → HITL) · `e4_subfiles.py`(선언형 서브에이전트 스택·한도 미들웨어 · `files` 공유) · `e5_limits.py`(부모 한도가 general-purpose에 안 옮겨 감 · 같은 이름 교체) · `e6_nodes.py`(설정마다 노드·도구 이름 · 키 없이 모델 객체 만들기 실패). AST·금지어 세기 `ast_scan.py`·`banscan.py`·`dump.py`.
- 앞 챕터: Ch 6 01 `_src` 42행·b4(하네스 정의) · Ch 9 06 `_src`(실험 하네스) · Ch 22 03·08 `_src`·노트북 훅 이름 · Ch 23·24 노트북 준비 셀(`mkdtemp`) · Ch 21 요약 220행 · Ch 23 요약 205·206행 · Ch 24 요약 191·192행 · Ch 26 요약 §13~§15 · Ch 26 `author_04.py` 844행·`author_05.py` 592·604행 · Ch 28 01 `_src` b3.
