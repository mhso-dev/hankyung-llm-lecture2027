# 전체 품질 개선 + 챕터 끝 실습 진행표

요청(2026-09-16): 모든 챕터를 품질 개선(체인 ⑨)한 뒤 챕터 끝 실습 절을 붙인다. 멈추지 않고 끝까지. Ch 32·33은 실습 절 제외. **Ch 1부터 한 챕터씩 순서대로**(병렬·워크플로 취소 — 앞 챕터 내용이 다음 챕터에 이어지도록). 챕터 끝마다 `qa/upgrade/chapter-summary.md`.
절차서: `textbook/_notebook/upgrade/PLAYBOOK.md`. 상태: 대기 / 절 개선 중 / 실습 절 / 검토 / 완료 / 삽화 대기 / 막힘.

| 챕터 | 절 수 | 상태 | 실습 절 | 게이트(전→후) | 검토 | 메모 |
|---|---|---|---|---|---|---|
| Ch 01 개발환경 | 5 | 완료(강사 확인 대기) | 06-개발환경-실습 | 255→0 | 1회 | 검토 1차 상 0·중 11·하 27 모두 반영(05-7 변형), ch01-practice.zip 재생성 대기 |
| Ch 02 파이썬 | 12 | 완료(강사 확인 대기) 2026-09-16 | 13-파이썬-실습 | 413→0 (13/13, 코드 셀 190) | 1회(A·B 분담) | 검토 1차 상 0·중 11·하 44 중 중 10·하 44 반영(zip만 미룸), verify·visual 28건 PASS, 강사 확인: 03·05 강의 범위·규격 추가 규칙 4개, ch02-practice.zip 재생성 대기 |
| Ch 03 Git·GitHub | 5 | 완료(강사 확인 대기) 2026-09-16 | 06-Git-실습 | 233→0 (6/6, 코드 셀 112) | 1회 | 검토 1차 상 0·중 4·하 23 모두 반영, 05-5 삽화를 채택 job 결과로 교체(새 생성 없음), verify·visual 14건 PASS, 규격 추가 3줄(§5-3·§5-4·§6), 강사 확인: 02 강의 범위·기준 Git 버전, part1-practice.zip·Part 목차 재생성 대기 |
| Ch 04 데이터 도구 | 5 | 완료(강사 확인 대기, 삽화 1장 대기) 2026-09-16 | 06-데이터-도구-실습 | 237→0 (6/6, 코드 셀 96) | 1회 | 검토 1차 상 0·중 6·하 18 중 중 6·하 17 반영(C-3 공용 Mermaid 설정 건 넘김), verify·visual 14건·pytest 10 PASS, article-text.json SHA-256 전후 같음, 삽화 02-5 대기(재생성 한도 소진), 규격 추가 2줄(§2-4·§7-2), 강사 확인: 03 강의 범위·기준 버전, part1-practice.zip·Part 목차 재생성 대기 |
| Ch 05 LLM 동작 원리 | 8 | 완료(강사 확인 대기) 2026-09-16 | 09-LLM-동작-원리-실습 | 262→0 (9/9, 코드 셀 132) | 1회(A·B 분담) | 검토 1차 상 0·중 8·하 34 모두 반영, 02·03 새 커널 재실행(반영 전 셀 출력 같음, 03 심화 셀 2개), verify·visual 20건 PASS, article-text.json SHA-256 같음, 옛 생성기 막음 줄 + before/generators로 옮김, 규격 추가 5줄(§3·§4·§5-3·§7-2·§8), 강사 확인: 03 강의 범위·심화 셀·챕터 16h 유지, 로컬 모델 캐시 .cache/vm 전체 마감 때 정리, part1-practice.zip·Part 목차 재생성 대기 |
| Ch 06 LangChain 시작 | 6 | 완료(강사 확인 대기) 2026-09-17 | 07-LangChain-실습 | 273→0 (7/7, 코드 셀 130) | 1회 | 검토 1차 상 0·중 4·하 22 모두 반영(재실행 없음, 02-2 그림만 다시 렌더), verify·visual 16건 PASS, 옛 생성기·옛 runs 사본 before/로 이동, 규격 추가 3줄(§3·§5-3·§7-2). **알려진 뒤 챕터 실패**: Ch 8 06에서 해소(2026-09-17 — Ch 7 08 새 커널 재실행 → Ch 8 06 새 커널 실행 → Ch 8 테스트 수정, Ch 8 테스트 21 통과·`check_course_continuity.py` 73행 통과). 이 챕터 06 재실행 금지는 유지(chapter-summary §9). 강사 확인: 04·05·06 강의·실습 범위 문장, part2-practice.zip·Part 2 목차 재생성 대기 |
| Ch 07 프롬프트 엔지니어링 | 8 | 완료(강사 확인 대기) 2026-09-17 | 09-프롬프트-엔지니어링-실습 | 272→0 (9/9, 코드 셀 200) | 1회(A·B 분담) | 검토 1차 상 0·중 6·하 27 모두 반영(재실행 없음, 08 재실행 금지 지킴, 02-2·02-3·03-3 그림만 다시 렌더), verify·visual 20건 PASS, 옛 생성기·`_src/index-body.html` before/로 이동, 규격 추가 3줄(§4·§5-3·§7-2). **runs 사슬**: Ch 7 08 새 커널 실행 완료로 `prompt-ab-continuity.json` `a8aaafb7…`(출처 = Ch 6 `f18920c6…`), 반영 전후 해시 같음. Ch 8 `test_ch06_ch08_continuity.py` 2건·`check_course_continuity.py` 73행 실패는 Ch 8 06에서 해소(2026-09-17, Ch 8 06 새 커널 실행·테스트 수정). **Ch 8 06 실행 뒤 Ch 7 08 재실행 금지** 유지, R-1 작업 폴더 제한은 이 챕터 08 노트북에 남음(Ch 8 06은 해소). 강사 확인: 05~08 meta 1h/2h·03·04·05 강의 범위 문장, part2-practice.zip·Part 2 목차 재생성 대기 |
| Ch 08 컨텍스트 엔지니어링 | 6 | 완료(강사 확인 대기) 2026-09-17 | 07-컨텍스트-엔지니어링-실습 | 274→0 (7/7, 코드 셀 183) | 1회(A·B 분담) | 자체 _build.py(`{{mermaid:}}`·세 칸 `{{img:}}` 추가, 잔존 검사 넓힘). 검토 1차 상 0·중 7·하 32 모두 반영(하위 권고 3가지 미반영: 01 [16] 셀 나누기·Ch 7 04 b6·R-2 테스트 보강), **01~06 재실행 없음**(06은 runs 사슬 끝), 07만 `ask_library()` 10줄로 고쳐 새 커널 재실행 → 모델 출력 변경분(실행 1 휴관 빠진 `법정 공휴일`) 인용·그림 재대조, verify `PASS 7 sections / 183 code cells`·visual 16건·tests 21 PASS, **runs 사슬 해소 완료**(Ch 8 06 `context-design-continuity.json` `125fc147…` 출처 = Ch 7 `a8aaafb7…` ← Ch 6 `f18920c6…`, 반영 전후 해시 같음, R-1 해소·새 알려진 제한 R-2), 옛 생성기 before/generators로 이동, 규격 추가 3줄(§2-2·§3·§7-2). 강사 확인: 01~06 강의·실습 범위 문장, 06 meta 1h/1h 배분. part2-practice.zip·Part 2 목차·Part 2 과정 요약 대기 |
| Ch 09 RAG 첫 실행 | 7 | 완료(강사 확인 대기) 2026-09-17 | 07-RAG-실습 | 268→0 (7/7, 코드 셀 175) | 1회(A·B 분담) | 자체 _build.py(`{{mermaid:}}`·세 칸 `{{img:}}` 추가, 잔존 검사 넓힘, `chapter.json` 없어 `verify.py --chapter` 따로). 검토 1차 **상 2·중 11·하 27 중 상 2·중 11·하 26 반영**(미반영: 01·04 절 제목 — 강사 확인 대상), **01~07 재실행 0**(설명·그림만 `mdpatch.py` → `--no-exec`, 노트북 일곱 개 코드+출력 해시 전후 같음), 03-1·03-2·06-1·06-2·07-2 그림만 다시 렌더, 07 표시 제목 「07 · RAG 실습: 문서 청크 크기를 바꿔 검색부터 답 검사까지」로 줄임. verify `PASS 7 sections / 175 code cells`·visual 16건·tests 10 passed·빌드 HTML `{{` 0. **계약 변경**: `runs/continuity-ch09-search.jsonl` `4f9fce62…` → **`294713765a…`**(최상위 8키·`retrieved` 5키 그대로, `config`에 `corpus` 추가·`inputs.corpus_scope` 한국어, `chunk_id` `ch09:6f9f83db90:0` — Ch 10은 네 자리 채움, **k=2 전제 유지**). `config.yaml`만 주석 한 줄로 `6da4af21…` → `1e425071…`, `harness.py`·`prompts.py`·`rag.py`·Ch 11 평가셋·Ch 6·7·8 사슬 해시 불변. **챕터 밖 수정**: `public-files.json`+`build_bundle.py`에 06절이 읽는 `config.yaml`·`labs/data/rag-corpus/queries.jsonl` 추가(없으면 학생·`run_continuity_bundle.py`가 06절을 실행 못 함) → 이에 딸려 `check_course_delivery.py`·`part3/qa/check_delivery.py`·`part4/qa/check_delivery.py`의 정답키 금지 목록을 `rag-corpus/build/`·`queries.csv`로 조정(**정답키 공개 정책 = 강사 확인**), `check_course_continuity.py` 182·184행 ch09 허용(→ 212행 zip 신선도까지 감), `part3/_build_index.py` 절 수 칸 분리(07절 있는 상태 수용). 규격 §7-2 두 줄·PLAYBOOK §4 두 줄 추가. **전체 마감 순서**: part3·llm(필요하면 part4) zip 재생성 → `run_continuity_bundle.py` `--reuse-upstream` **없이** → `visual.cjs`로 `qa/visual-results.json` 14 → 16행 → `finalize_continuity_evidence.py` `assert len(visual) == 88` → **90** → `check_continuity.py`·`check_course_continuity.py` 끝까지 → Part 3 목차 재생성. 옛 QA 스크립트 두 개(`test_notebook_migration.py`·`check_structure.py`) `before/qa-scripts/`로 이동, `check_content.py`에 07 추가. 강사 확인: 01·04 제목, 강의·실습 범위 문장, 07 요청 6번. 정답키 공개 정책은 **사용자 결정(2026-09-18): 묶음에 포함 유지** |
| Ch 10 문서 처리 | 8 | 절 개선 중(01~04 완료) | 예정 | 363 → (01절 37→0, 1/8) | 대기 | 자체 _build.py(01절에서 `{{mermaid:}}`·세 칸 `{{img:}}` 추가 + 잔존 토큰 검사, 02~08·index HTML 해시 불변, `chapter.json` 없어 `verify.py --chapter` 따로 → `PASS 8 sections / 77 code cells`). 01 문서와 메타데이터: **서비스 요청 0번**(모델·임베딩 없음), 코드 셀 18, 새 커널 두 번 출력 같음, Mermaid 4장·삽화 1장(job `97390942-…`, 4크레딧, 잔액 2808), visual 2건 PASS, 실습 폴더 tests 38 passed 전후 같음, `runs/` 읽기·쓰기 0. 데이터를 `E02.pdf` → **Ch 9와 같은 `E01.pdf`**로 바꾸고 Ch 9 `load_pdf_pages()`·`make_source_mark()`를 같은 코드로 이어 씀. 같은 2쪽을 기본 읽기 905자 / 레이아웃 읽기 1396자로 읽어 **다섯 칸 출처 기록**(`doc_id`·`source`·`file_type`·`parser`·`page`, 실습 폴더 `normalize_metadata()`와 같은 칸 이름)이 필요한 까닭을 출력으로 보임. 새 용어 4(파서·파일 형식·출처 기록·출처 계보). 챕터 파일 새로 만듦: `집필점검표.md`, `qa/upgrade/handoff.md`, `gates-before.json`. 옛 도식 생성기 `figures/_gen_figures.py`에 `raise SystemExit` 넣음(삭제 아님, 마감 때 `before/generators/`로). **챕터 밖 수정 0건**(학생 묶음 허용 목록은 이미 `fixtures/`·corpus 포함 → 묶음 풀어 세 자리에서 경로 셀 확인). `check_continuity.py` 154행·`check_course_continuity.py` 212행 zip 신선도에서 멈춤(Ch 9 마감과 같은 자리, 전체 마감 몫). 강사 확인: 01 강의·실습 범위 문장. 삽화 재생성 때 봉투 빈 줄 수(4줄 → 5줄) 맞추기 |
| Ch 11 평가 기초 | 6 | 대기 | 예정 | | | |
| Ch 12 검색 튜닝 | 12 | 대기 | 예정 | | | |
| Ch 13 LangGraph 기초 | 7 | 대기 | 예정 | | | |
| Ch 14 RAG 패턴 | 9 | 대기 | 예정 | | | |
| Ch 15 평가 심화 | 8 | 대기 | 예정 | | | |
| Ch 16 가드레일 | 6 | 대기 | 예정 | | | |
| Ch 17 Agent 개요 | 5 | 대기 | 예정 | | | |
| Ch 18 워크플로우 패턴 | 6 | 대기 | 예정 | | | |
| Ch 19 모델과 도구 | 6 | 대기 | 예정 | | | |
| Ch 20 ToolNode | 4 | 대기 | 예정 | | | |
| Ch 21 create_agent | 6 | 대기 | 예정 | | | |
| Ch 22 Middleware | 9 | 완료(강사 확인) | 09-Middleware-실습 | 386→0 | 2회+1회 | 시범 |
| Ch 23 Persistence | 6 | 대기 | 예정 | | | |
| Ch 24 Human-in-the-Loop | 3 | 대기 | 예정 | | | |
| Ch 25 Streaming | 3 | 대기 | 예정 | | | |
| Ch 26 위임 구조 | 4 | 대기 | 예정 | | | |
| Ch 27 DeepAgents | 8 | 대기 | 예정 | | | |
| Ch 28 MCP | 5 | 대기 | 예정 | | | |
| Ch 29 Agent 평가 | 4 | 대기 | 예정 | | | |
| Ch 30 FastAPI 서빙 | 9 | 대기 | 예정 | | | |
| Ch 31 DB·상태 영속화 | 5 | 대기 | 예정 | | | |
| Ch 32 Docker | 5 | 대기 | 제외(사용자 결정) | | | Docker 실행 환경 없음 |
| Ch 33 CI/CD | 5 | 대기 | 제외(사용자 결정) | | | Docker 실행 환경 없음 |
| Ch 34 비용·Rate Limit | 5 | 대기 | 예정 | | | |
