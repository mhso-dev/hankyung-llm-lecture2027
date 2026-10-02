# 04절 진단 — 파일시스템과 중간 결과 (2026-09-28)

- 생성기 `qa/upgrade/author_04.py`(`0427fca5…`) · 노트북 `labs/part6/ch27-deepagents/notebooks/04-파일시스템과-중간-결과.ipynb`(`4ab0023c…`, `code_sha256` `b3c842d492d8…`) · `_src/04-파일시스템과-중간-결과.html`(`94b81208…`) · 빌드 HTML(`33bfbb65…`) · 그림 `figures/04-1~04-5` · 흔들림 확인 `04-probe.md`·`probe/probe04.py`(`d69401b1…`)·`probe/probe-04-P.jsonl`(`fa2e9c02…`) · 도구 파일 `harness_tools.py`는 **바꾸지 않음**(02절 판 `14ee39ca…` 그대로).
- 형식 **experiment** 유지, 슬러그 `04-파일시스템과-중간-결과` 그대로(03절 b8·Part 6 목차 링크), 제목 「파일시스템과 중간 결과」 그대로(금지어 없음 — 강사 확인 대상 아님).
- 챕터 리드 결정 M2: **앞 절반(2·3절) 모델 없음 · 뒤 절반(5·6절) 실제 모델 한 번 실행(요청 3)**. **이 챕터에서 디스크에 쓰는 유일한 절** — `FilesystemBackend(root_dir=tempfile.mkdtemp(prefix="ch27-04-"))`, `os.chdir` 없음, 실습 폴더 `workspace*`에 쓴 것 0.

## 1. 게이트 전후

| 항목 | 수정 전(`gates-before.json`) | 수정 뒤(`gates-wip-04.json`) |
|---|---|---|
| 코드 셀 | 4 | **31**(준비 넷(설치·가져오기·키·임시 폴더) + 모델 셀 하나 + 본문 스물여섯) |
| 검사 문장 | 69 | **417** |
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | 3 · 0 · 1 · 0 · 6 · 20 · 3 = **33** | **0 · 0 · 0 · 0 · 0 · 0 · 0 (PASS)** |
| 코드 줄(`count_code.py`, 주석·빈 줄 뺌) | 26 | 180(도구 파일 함수 다섯은 가져오기 — 02절 판, 더한 줄 0) |

- **첫 실행 전** `upgrade_gates.py … --label wip-04 --section 04`(`gates-wip-04-04.json`): G1 0 · G2 0 · G3 0 · G4 0 · G5 0 · G6 3(70자 넘는 문장 둘 — b8 다음 절 문장·b10 백엔드 문서 설명 · 코드 이름으로 시작한 문장 하나 — 정리 3) · G7 18(그림 전). G6은 실행 전에 고쳐 0. 실행 뒤 G5 1(3절 손 요청 셀 결과 읽기 첫 단락의 `hand_write_1` — 출력에 없는 숫자 든 인용)은 `mdpatch.py`로 둘째 단락으로 옮김.
- AST 따로(`/tmp/ch27-04/tools/extra_check.py` — 02 판 그대로): **금지 문법 0건**. 허용 표시 하나 — 셀 `record_tool_names`의 `@wrap_model_call`(02절 셀 그대로). `try/except ValueError as error` 한 셀(2절 `..` 셀 — Ch 2 05절, 받은 오류 출력; 챕터 허용 범위 「뒤 절이 오류를 받으면 `try/except 이름` 한 셀」). 호출 깊이(`depth.py`) **최대 2**. 준비 셀 밖 셀 최대 10줄(5절 `WRITTEN` 셀), 함수 본문 최대 5줄(`tools_only_graph`), 셀당 정의 하나. 힌트는 `@tool` 매개변수 `topic: str` 하나(02절 셀 그대로). 새로 쓴 이름: `FilesystemBackend`·`FilesystemState`·`StateGraph`(01절)·`os.path.join`·`os.path.isfile`·`str.lstrip`·`with open`(Ch 2 05)·`tempfile.mkdtemp`(Ch 23) — 앞 설명 셀·주석에 한 문장씩.
- 금지어(`ban27.py`): 노트북 설명·주석·`_src`·`.mmd`·캡션에서 걸림은 「캐시 입력」 둘(과정 약속 말)과 거짓 양성 셋(「프로그램」의 「로그」·「체크포인터」의 「포인터」)뿐. 「경로」·「반환」·「측정」·「검증」·「보장」·「영속」·「격리」·「지시」·「의존」·「한 겹 더」 0건.
- `verify.py --chapter`: `PASS 8 sections / 131 code cells (max 17 lines)`(17줄은 05~08 옛 노트북). 빌드 HTML `{{`·`[[` 0건, 인라인 SVG 4·삽화 JPEG 1.

## 2. 수정 전 주요 문제 (옛 판 — 학생 본문에는 쓰지 않음)

1. **실습 폴더 `workspace/`에 씀**(`FilesystemBackend(root_dir=LAB / 'workspace')` — 연결 폴더), 07도 같은 폴더를 써서 저장 출력 `목록: ['/research/final.md', '/research/source-a.md']`에 **07이 쓴 파일이 섞임**(실행 차례에 기대는 출력). 옛 폴더는 그대로 둠(마감 삭제 승인 목록).
2. 준비 셀 `LAB = next(parent / … for parent in [cwd, *cwd.parents] if …)`(제너레이터·별표 풀기) · c8 내포식·제너레이터·`any` `assert` · 첫 줄 주석 없는 준비 셀 · 모델 요청 0(「중간 결과를 파일로 적는 장면」이 모델 없이 백엔드 직접 호출뿐).
3. `StateBackend`와의 비교 없음 — 03절 b8 「디스크에 쓰는 백엔드와 상태 칸에 두는 백엔드로 견줍니다」를 옛 판은 채우지 못함.
4. 금지어 「경로」 19/9/2(「가상 경로」 새 말 포함) · 반환 4/2 · 보장 2 · 영속 1 · 메타데이터 1 · 명시 1/1 · 표면 1. 결과 읽기 셀 0 · 제목 셀·핵심 그림 없음 · Mermaid 0 · 삽화 0 · 옛 SVG 토큰 `{{svg:04-흐름}}` · b10 여덟 절 공통 여섯(확인 2026-09-11) · b1·b3·b8 틀 문장.
5. 옛 b3 「FilesystemBackend의 파일은 체크포인터 메시지와 다른 저장 표면」·옛 b6 「여러 스레드의 영속성은 측정하지 않습니다」 — 말이 흐리고 `StateBackend`(체크포인터와 같은 상태 안)와 가르지 않음.

## 3. 바꾼 것

- **노트북(31 코드 셀, 여섯 절)**: 1절 준비(설치 다섯 — `langgraph==1.2.11` 더함(작은 그래프) · 가져오기(도구 파일 한 줄, 함수 다섯) · 키 · 모델 · 빈 임시 폴더 `work_folder`) → **2절(모델 없음, 디스크 백엔드 직접 호출)** `백엔드 종류: FilesystemBackend`·`virtual_mode 값: True`·`명령을 실행할 수 있는가: False` → `write` `WriteResult`·`오류: None`·`쓴 파일 위치: /notes/rules.md` → 운영체제 `os.listdir` `['notes']`·`['rules.md']` → `with open` `디스크 파일 글자 수: 67`·`쓴 글과 같은가: True` → 파일 위치 규칙 둘 `/etc/rules.md` → `['etc', 'notes']` · `..` → `받은 오류: ValueError | Path traversal not allowed` → **3절(모델 없음, 값 바꿔 보기)** 작은 그래프 함수 `tools_only_graph`(상태 형식 `FilesystemState`) → 두 Deep Agent `도구가 같은가: True`·노드 `['__start__', 'tools', '__end__']` → 손 요청 `write_file /drafts/memo.md` → 기본 백엔드 `상태 칸 files의 파일 위치: ['/drafts/memo.md']`·임시 폴더 그대로 → 파일 항목 칸 넷 → 디스크 백엔드 `상태 칸 files의 파일 위치: []`·`['drafts', 'etc', 'notes']` → **4절** 규정 글·`lookup_rule`·명세·기록 훅(02절 셀과 같은 글) · 바깥 한도 10(03절 셀과 같은 글) → **5절** 새 임시 폴더 `run_folder`·디스크 백엔드 → `run_agent`(도구 열) → 한 번 실행 → `show_messages` → `write_file` 인자 모으기 → 상태 칸·임시 폴더 → 디스크 파일 == 요청 인자 글 → **6절** 두 셈·받은 도구·예상 비용(02절 셀과 같은 글) → 정리 셋.
- **본문 10블록** 블록 단위로 다시 씀: b2(중간 결과 풀이 · 이 챕터 디스크 쓰기 유일한 절) · b3(Ch 2 05·Ch 23 01·Ch 8 02, Ch 13 04·Ch 20 01·Ch 21 03, 01절 6절·02절·03절) · b4 비유(온실 안 선반 ↔ 헛간 선반의 모종판) + 삽화 + 「두 백엔드와 기준 폴더」(새 용어 **기준 폴더** 세 문장 정의: 뜻 → 아파트 호수 → 코드 `root_dir=`) + 04-1 + 「파일 위치 규칙」 + 04-2 + 「중간 결과와 적어 두기」(Ch 8 02 이음 · 적은 글이 요청 인자로 메시지 목록에도 남음) + 안전 설정 · b5 + 04-3 · b6 값 성격 표 + 04-4 + 모델 판단 단락 + 두 커널 문장 · b7 열 항목 · b8 · b9 네 문제 · b10 절 자료(확인 2026-09-28).
- **새 용어 1**(meta): 「기준 폴더」(`root_dir`). 「백엔드」(02)·「파일 위치」(01 용어 표)·「기록 훅」·「호출 한도」·「general-purpose 서브에이전트」·「서브에이전트 명세」·「적어 두기(Write)」(Ch 8 02)·「라이브러리 상태 형식」(Ch 21 03)은 이어 씀. 「중간 결과」는 제목 말이라 1절·b2에서 한 문장으로 풂(새 용어로 세지 않음). 「경로」·「가상 경로」 0건 — API 이름 `root_dir`·`file_path`는 코드에만.
- `assert`는 키 셀 하나뿐(옛 판 `assert` 둘 뺌 — 모델 판단 값에는 걸지 않음).
- 준비 셀 `LAB = next(…)` 뺌(실습 폴더를 찾지 않음). 임시 폴더 이름은 출력하지 않고 폴더 안 이름만(`"ch27-04-" in work_folder` `True`만).

## 4. 흔들림 확인 (노트북 밖, `04-probe.md`)

- §0(입력·판단 규칙·그림 라벨 규칙)을 **2026-09-28T13:28Z에 적음**(파일 쓰기 뒤 기기 시각 13:28:11Z) → **첫 회차 시작 13:28:17Z**(회차 1 기록 시각 13:28:19Z). Ch 26 A-8 교훈대로 §0 먼저. 스크립트 `probe04.py`도 §0 전에 씀(요청 0).
- 조건 하나(디스크 백엔드 Deep Agent) × **5번**, 회차마다 새 임시 폴더(요청 15번, 서비스 오류 0): **구조 값 5/5**(그래프 도구 열 · 받은 도구 아홉·`execute` 없음 · 상태 칸 `files` `[]` · 디스크 `notes/rules.md` 글 == 요청 인자 글 · 요청 3 == 훅 3 == 도구 요청 응답 2 + 1) · **모델 판단 값 5/5**(`write_file` 한 번 `/notes/rules.md` · 우리 도구 요청 모두 첫 응답에 함께 · `task` 0 · 그 밖 파일 도구 0 · 한도 안 · 요청 3 · 임시 폴더 맨 위 `['notes']`) → **입력 그대로**.
- 흔들린 값: 첫 응답 `lookup_rule` 요청 수 **3(3번) ↔ 4(2번 — 묻지 않은 「운영」까지)** → 메시지 수 8 ↔ 9 · 파일 글자 수 145 ↔ 193 · 답 글(176~208자) · 출력 토큰 283~343 · 캐시 입력 · 예상 비용 0.005843~0.006201(캐시 뺌). 첫 요청 입력 토큰 1891은 다섯 번 같음(결론에는 쓰지 않음).

## 5. 실행과 값

- 교재 출력 **A**: `author_04.py` + `execute.py`(`run_section.sh`와 같은 명령, 실행과 렌더를 두 호출로 나눔) 2026-09-28T13:41:37Z · `PASS … 31 cells` · `code_sha256` `b3c842d492d8…` · `outputs_sha256` `2b527415…`. 사본 **B**(그림 전, `--tools-copy`로 디스크 도구 파일 복사): 13:42:01Z, 같은 `code_sha256`, **`outputs_sha256` `2b527415…` 같음**. **셀별 출력 대조 31/31 같음**(`cmpout.py`, 셀 출력 글 연결 해시 `fd37d203b85e8973` — 마크다운을 채운 뒤 디스크 노트북도 A와 31/31 같음). 흔들림 확인에서 달랐던 `lookup_rule` 수·메시지 수·토큰도 이번 두 커널에서는 같았지만(3·8·`6093 | 284`·`0.005848`), §0 규칙대로 흔들리는 값으로 둠.
- **구조 값(결론·그림)**: `백엔드 종류: FilesystemBackend` · `virtual_mode 값: True` · `명령을 실행할 수 있는가: False` · `쓰기 결과 종류: WriteResult`·`오류: None` · `['notes']`·`['rules.md']` · `디스크 파일 글자 수: 67`·`쓴 글과 같은가: True` · `쓴 파일 위치: /etc/rules.md`·`['etc', 'notes']` · `받은 오류: ValueError | Path traversal not allowed` · `두 Deep Agent의 도구가 같은가: True` · `['__start__', 'tools', '__end__']` · 3절 두 셀 `Updated file /drafts/memo.md | success` · `['/drafts/memo.md']` ↔ `[]` · `['etc', 'notes']` ↔ `['drafts', 'etc', 'notes']` · 파일 항목 칸 `['content', 'encoding', 'created_at', 'modified_at']` · 5절 `그래프에 등록된 도구 수: 10` · `상태 칸 files의 파일 위치: []` · `임시 폴더 안에 파일이 있는가: True`·`요청 인자의 글과 같은가: True` · `받은 도구 수: 9`·`execute를 받았는가: False` · 두 셈 같음.
- **모델 판단 값(흔들림 확인 5/5 + 두 커널 같음 — 「이번 실행에서는」 한정어와 함께만)**: `write_file 요청 수: 1`·`적으려 한 파일 위치: /notes/rules.md` · 임시 폴더 `['notes']` · `task` 0 · `응답으로 센 요청 수: 3`.
- **흔들리는 값(둘째 단락·b6 표·확인할 점·b7만)**: `결과 메시지 수: 8`(밖에서는 9도) · 첫 응답 `lookup_rule` 셋(밖에서는 넷도) · 파일에 적은 글 · `입력 토큰: 6093 | 출력 토큰: 284` · `예상 비용(달러): 0.005848`(캐시 입력을 빼지 않은 어림).
- 걸린 시간은 재지 않음. 흔들리는 값은 `[[READ_…]]` 자리 표시로 두고 교재 출력(A)·B 대조 뒤 `mdpatch.py`로 노트북·`_src`에 채우고, 생성기의 `placeholder(…)` 호출은 채운 글로 바꿈(`genmatch.py` 셀 66 차이 0·`_src` 같음). `_src`만의 표 한 줄(모델 판단 행에 요청 3 더함)·그림 설명은 생성기를 고친 뒤 `--src-only` → `run_section.sh … --no-exec`(**다시 실행하지 않음**).

## 6. 파일 쓰기 자리 (챕터 리드 결정 3)

- 노트북: `work_folder`(2·3절 — `notes/rules.md`·`etc/rules.md`·`drafts/memo.md`) · `run_folder`(5절 — 모델이 쓴 `notes/rules.md`) 둘. 둘 다 `tempfile.mkdtemp(prefix="ch27-04-")`(작업 기기에서는 세션 임시 폴더 `$TMPDIR`), 기본 백엔드 쪽은 상태 칸 `files`(디스크 0).
- **실습 폴더에 쓴 것 0**: `labs/part6/ch27-deepagents/workspace`·`workspace-05`·`workspace-08` 안에 04 작업 뒤(04-probe.md보다 새로) 바뀐 파일 0(`find -newer`), `before-manifest.json` 대조도 같음(§13). 노트북은 실습 폴더 위치를 찾지 않음.
- 임시 폴더는 지우지 않음(`rm` 0회) — 삭제 승인 목록 §13.

## 7. 안전 규칙 적용 (챕터 공통 (가)·(나))

- (가) 바깥 `middleware=[ModelCallLimitMiddleware(run_limit=10, exit_behavior="end"), record_tool_names]` — 03절 셀과 같은 글(§0에서 첫 요청 전에 정함). 한도에 닿지 않음(흔들림 확인 5번 · 두 커널).
- (나) `subagents=[같은 이름 general-purpose 명세]`(02절 셀과 같은 글, 자기 한도 2). 이번 실행 `task` 0.
- 상한: 한 번 실행 요청 ≤ 10 + `task` 부른 횟수 × 2(본문 b4·4절 결과 읽기). (라) `recursion_limit`은 주지 않음.
- 요청 수 세기: 이번 실행이 더한 메시지만 잘라 `sum_usage` = 기록 훅 요청 수(두 커널 모두 3).

## 8. 도구 파일 — 바꾸지 않음

- 04절은 02절 판에서 함수 다섯(`estimate_cost`·`show_messages`·`sum_usage`·`tool_call_names`·`tool_names`)만 가져옴(`names_only_in`은 쓰지 않음) → **더한 함수 0, 도구 파일 쓰기 0**. `author_04.check_tools()` = `author_03.check_tools()`(= `author_02.check_tools()` runner·delegation·01 셀 대조 + 디스크 판이 02절 판으로 시작). `--tools-copy`는 디스크 판 복사(B 실행에 씀).
- 노트북에 둔 것: 작은 그래프 함수 `tools_only_graph(agent)`(이 절에서 처음 가르침 — 01절 6절 셀의 흐름을 함수로 묶음, 상태 형식 `FilesystemState`. 뒤 절(05 옮겨 두기 확인·06 `files` 공유·08 권한)이 다시 쓰면 그 절이 이 셀 글 그대로 도구 파일로 옮김).
- 02·03절 셀과 같은 글이라고 적은 셀(`RULES`·`DEF_TOOL`·`HELPER_SPEC`·`DEF_HOOK`·`COST` / `OUTER_LIMIT`)은 `author_02`·`author_03` 문자열을 그대로 쓰고 `check_same_as_prev()`로 02·03 노트북 디스크 셀과 글자 대조. `check_same_as_probe()`로 노트북 셀 글과 `probe04.py` 대조.
- 설치 셀: 도구 파일이 가져오는 패키지 0(추가 0) · 이 절이 `StateGraph`를 직접 가져와 `langgraph==1.2.11`을 넣음(01절 판과 같은 다섯, 잠금 판). 묶음 목록 변경 0.

## 9. 고친 틀린 사실·과장

- 옛 b4 「가상 경로의 `/`는 컴퓨터의 파일 시스템 루트를 뜻하지 않습니다」 → 참(설치판 `_resolve_path` 202~206행, 2절 출력 `['etc', 'notes']`). 새 판은 「파일 위치의 맨 앞 `/`는 기준 폴더」로 씀.
- 옛 b4 「`write_file`은 … 성공 여부를 구조화된 결과로 반환」 → 백엔드 메서드 `write`는 `WriteResult`, 파일 도구 `write_file`은 도구 메시지(`Updated file …`)를 냄 — 둘을 가름(2절·3절 출력).
- **공식 백엔드 문서는 `virtual_mode` 기본값을 `False`로 적음**(「the default (`virtual_mode=False`) provides no security」, 확인 2026-09-28) ↔ 설치판 0.7.0 `backends/filesystem.py` 141행 `virtual_mode: bool = True`, 0.7.0 릴리스 노트도 `True`, 2절 출력 `True`. b7·b10에 적음.
- 옛 b3 「Ch 23에서 상태 저장 범위를 구분」 → Ch 23 요약 「Store는 한 줄뿐」과 느슨했음. 새 b3는 Ch 23 01의 임시 폴더만 잇고, 체크포인터와의 관계는 b7에 문서 인용 + 「실행하지 않았습니다」.
- 인계서의 「Ch 8 03 「적어 두기(Write)」」 → 실제로는 **Ch 8 02절 「Write와 Select」**가 적어 두기를 정의(03은 Compress·Isolate). b3·b4는 02절로 링크.

## 10. 그림

- Mermaid **4장**: 04-1(폭 603) · 04-2(720) · 04-3(814 — 첫 판 956을 참여자 이름·`actorMargin`·메모 줄바꿈으로 줄임) · 04-4(642) — 모두 868 이하, PNG 직접 열어 확인. 보라는 04-3 모델 띠·04-4 모델 응답 상자(실제로 부른 모델) · 앞 절반 그림 04-1·04-2 보라 0 · 빨강 0(04-2 `ValueError`는 받아 출력한 오류라 노랑). 노트북 첨부 04-1 하나(`attached 1`). 라벨에 파일 글·글자 수·토큰·`lookup_rule` 수·임시 폴더 이름 없음.
- 삽화 **1장** `04-5-온실과-헛간의-모종판`: 1차 job `9bdac4a0-e987-40d6-ab1e-d80fc165c620` 탈락(온실 안 모종판이 다리 달린 탁자 위 — 01절 소품 「작업대」와 겹침 · 물건이 작고 위아래 여백이 큼) → **2차 job `28714173-f8a7-4d16-8897-c7c00534d111` 채택**(재생성 1회 — 상한). 거래 13:43:30.087394Z·13:44:58.685502Z 「Nano Banana Pro −2」 두 줄 = **4크레딧**(잔액 2335 → 2331, 바로 앞 거래 13:08:12Z는 03절 몫). 작업 조회 모델 표시 `nano_banana_2`(요청 `nano_banana_pro` — 01~03과 같은 표시 차이). 원본 `0a98fb0b…`(2752 × 1536) → 저장 1100 × 614 `8b111465…`, 다시 받은 원본(해시 같음)을 같은 폭으로 줄여 픽셀 대조 bbox `None`·최대 차이 0. 헛간 쪽 모종판 오른쪽 끝 칸이 문틀에 조금 가림(프롬프트 「fully visible」과 다름) — 두 자리 가름에 영향이 없어 두고 그림 읽기에 밝힘. 세부 `figures/04-5-온실과-헛간의-모종판.prompt.md`.
- 옛 그림 `04-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0 — 삭제 승인 목록).

## 11. 뒤 챕터가 이 절에 기대는 문장 (고치지 않음, 참·거짓만)

- `grep -rn 'Ch *27' textbook/part6/ch2[8-9]-*/_src textbook/part7`: **1건** — Ch 28 01 b3 「Ch27에서는 파일시스템과 하위 작업 기능을 미리 조립한 하네스를 사용했습니다」 → **참**(04는 파일 도구·백엔드를 기본 조립 그대로 쓰고, `task`도 조립에 있음. 「하위 작업」은 Ch 28 몫 말). Part 7 0건.
- 03 b8 「04절에서는 중간 결과를 파일로 적어 두는 장면을 봅니다. 디스크에 쓰는 백엔드와 상태 칸에 두는 백엔드를 견줍니다」 → **참**(3절 두 백엔드 견주기 · 5절 모델이 `write_file`로 규정 메모를 적음).
- 챕터 안 05~08 옛 `_src`에서 04를 가리키는 문장 0건(`grep '04절\|04-파일시스템'`). 옛 05 `_src`·노트북은 `workspace-05/`에 씀(05 몫 — 인계 §04 → §05).

## 12. 서비스 요청·비용

- 이 절 모델 요청: 흔들림 확인 **15** + 교재 출력 A **3** + 사본 B **3** = **21번**(탐색 `x1_shape.py`·`x2_files_key.py`·`x3_seen.py`·`x5_msgonly.py`·`x6_cells.py`·`x7_evict.py`(05 인계용 옮겨 두기 확인)는 가짜 키 글로 요청 0 — `x3`은 핸들러를 부르지 않는 **노트북 밖 탐색 전용** 훅). 임베딩 0.
- 예상 비용(요금표 2026-09-17, 청구 금액 아님, 캐시 입력을 빼지 않은 어림): 흔들림 확인 0.029909 + A 0.005848 + B 0.005848 = **약 0.042달러**(흔들림 확인 캐시 반영 어림 0.014617). 절 1달러 한도 안.

## 13. 강사 확인 대상

1. 모델 실행을 **디스크 백엔드 한 조건**으로만 함 — `StateBackend` ↔ `FilesystemBackend` 비교는 3절에서 같은 손 요청(모델 없음)으로 결정적으로 보임. 두 백엔드를 모두 모델로 돌리면 요청·셀이 두 배.
2. 질문이 파일 위치 `/notes/rules.md`를 정해 줌(07 `final.md` 선례, b7 「흐름을 보여 주려고 정한 예」) — 모델이 스스로 중간 결과를 적었다고 읽지 않게 b7에 한 문장.
3. 2절 `..` 셀의 `try/except ValueError as error`(Ch 2 05절) — 챕터 허용 범위 안이지만 Ch 27 첫 `try`.
4. 새 용어 「기준 폴더」(`root_dir`) — 「뿌리 폴더」·「루트」 대신 고름.
5. 코드 셀 4 → 31, 코드 줄 26 → 180(규격 상한 32 안).
6. 공식 문서와 설치판의 `virtual_mode` 기본값 차이를 본문 b7·b10에 적음.

## 14. 챕터 밖 수정·보호 파일·남은 것

- **챕터 밖 수정**: `textbook/_notebook/checks/notebook-contracts-part6-ch27-deepagents.json`(`verify.py --chapter`가 다시 씀). 공용 도구·과정 문서·앞 챕터 파일·묶음 목록·도구 파일은 고치지 않음.
- 보호 파일(`before-manifest.json` 238개): `manifest-changes.md` 「04절 뒤」 참고.
- 지워야 하지만 지우지 않은 것(삭제 승인 목록): **임시 폴더 16개** — 기기 세션 임시 폴더 `$TMPDIR/ch27-04-*` 11개(흔들림 확인 5 · `x6_cells.py` 2 · 교재 출력 A 2 · 사본 B 2)와 `$TMPDIR/ch27-04x-*` 5개(탐색 `x1` 3 · `x2` 1 · `x3` 1) · 기기 `/tmp/ch27-04/`(탐색 `x1_shape.py`·`x2_files_key.py`·`x3_seen.py`·`x5_msgonly.py`·`x6_cells.py`·`x7_evict.py` · `tools/` · 사본 `A/`·`B/` · 흔들림 확인 원 기록 `probe/` · 삽화 원본 `illu/`(1·2차 원본·다시 받은 원본·1100 사본) · `reps1.json`·`reps2.json`) · `.cache/ch27-04-view/`(그림 확인 사본 셋 — 이 절이 만듦) · `qa/upgrade/gates-wip-04-04.json`·`gates-wip-04.json`(run_section 기록) · 옛 그림 `figures/04-흐름.*` · 옛 `labs/…/workspace*`(01 이후 목록 그대로) · `qa/__pycache__/`. `rm`은 한 번도 부르지 않음.

## 마감 반영 (2026-09-28)

검토 1차(`review-round1-A.md`·`review-round1-B.md`)를 글·그림·기록으로 반영했습니다. **노트북은 다시 실행하지 않았고** 코드 셀은 한 글자도 바꾸지 않았습니다(`code_sha256`·`outputs_sha256`·`executed_at` 전후 같음). 고친 방법: 생성기 문자열 치환(`.cache/ch27-close/tools/gapply.py`·`smartrep.py` — 바뀐 생성기의 `cells()` 코드 셀이 노트북과 다르면 멈춤) → 달라진 마크다운 셀만 노트북에 옮김 → `src_html()`로 `_src` → `run_section.sh … NN --no-exec`. 전체 기록은 `chapter-summary.md`.

- A-12 b4 비유 「어디에 둘지는 모종판이 아니라, 정해 둔 보관 방식을 따릅니다」·「이 보관 방식이 02절에서 정의한 백엔드에 해당합니다」(02 b4 「보관 방식」과 같은 짝) · A-7 b10 `supports_execution` 1156~1173 → **1156~1175행** · A-14 셀 41 「넣을 수 있는 주제어를 알려 주는 정해 둔 글」(셀 40 주석 「정해 둔 안내 글」은 코드 — 다음 재실행 몫).
- **A-13 다음 재실행 몫(기록)**: 셀 42 첫 줄 주석 「(02절 셀과 한도만 다름)」은 03 셀 글을 그대로 쓴 것이라 04 자리에서 어색함 — 지금은 셀 43이 풂(「이 셀을 처음 쓴 03절에서 적은 말」), 다음 재실행 때 `author_04`의 한도 셀 주석을 04 판으로.
- 마크다운 셀 41. 노트북 `4ab0023c` → `0896cbd7` · `_src` `94b81208` → `00c5cef8` · HTML → `01f1cc38` · `author_04.py` `0427fca5` → `97c4dfe6`.
