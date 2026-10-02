# 이어서 작업하기 — 새 컴퓨터의 Claude에게 붙여 넣을 프롬프트

새 컴퓨터에서 `docs/NEW-MACHINE-SETUP.md`의 1~2단계(저장소 받기, `.env`)를 마친 뒤 Claude(Cowork 또는 Claude Code)에 아래 프롬프트 가운데 하나를 그대로 붙여 넣습니다. `<저장소 위치>`만 실제 경로로 바꿉니다. Cowork에서는 받은 `한국경제신문` 폴더를 먼저 연결합니다.

- **(가) 짧은 판** — 평소에 씁니다. Claude가 문서를 읽고 상태를 요약한 뒤 다음 할 일을 묻습니다.
- **(나) 긴 판** — 프로젝트를 처음 보는 세션이거나, 작업 규칙을 확실히 전하고 싶을 때 씁니다.

---

## (가) 짧은 판

```text
이 저장소는 한국경제신문 KDT 「LLM Agent 개발 & 바이브코딩」 교재 작업 폴더입니다.
위치: <저장소 위치> (Cowork 기기 셸에서는 $HOME/mnt/한국경제신문)
먼저 세 문서를 읽어 주세요.
1) AGENTS.md 맨 위 「지금 상태와 이어서 작업하기 (2026-10-02)」 절
2) docs/claude-project/quality-upgrade-status.md
3) textbook/qa/upgrade-final-checklist.md 맨 위 「전체 마감 결과」 절
읽은 뒤 지금 상태를 다섯 줄 안으로 요약하고, docs/NEW-MACHINE-SETUP.md 기준으로 이 컴퓨터에 준비가 덜 된 것(.env의 키 이름, uv, Python 3.12, Mermaid·playwright 도구, PostgreSQL pgenv)을 확인만 해서 알려 주세요. 설치와 수정은 아직 하지 마세요.
그다음 남은 사람 결정(①~⑪과 과정 전체 결정) 가운데 무엇부터 할지 저에게 물어봐 주세요.
API 키 값은 출력하지 말고, 파일은 지우지 마세요.
```

---

## (나) 긴 판

```text
# 이어서 작업하기 — 한경 KDT LLM Agent 교재

## 1. 프로젝트 배경
- 이 저장소는 한국경제신문 KDT 「LLM Agent 개발 & 바이브코딩」 과정(2026년 12월 개강, 24주)의 교재 작업 폴더입니다. GitHub: https://github.com/mhso-dev/hankyung-llm-lecture2027
- 위치: <저장소 위치>. 작업 스크립트(run_section.sh·pack.py·patch.py·mdpatch.py·pre_exec.sh)는 $HOME/mnt/한국경제신문 경로를 가정합니다. Cowork는 연결 폴더가 그 경로에 보이고, 기기에서 바로 쓸 때는 docs/NEW-MACHINE-SETUP.md 1단계의 링크가 있어야 합니다.
- 산출물은 세 가지입니다. HTML 교재(textbook/ — Jupyter 노트북 모양, 절마다 노트북과 같은 셀·실제 출력), 실습 노트북(labs/ — 챕터마다 pyproject.toml·uv.lock), 검사 도구(textbook/_notebook/·textbook/qa/·textbook/partN/qa/).
- 사용자는 강사이자 유일한 검토자입니다. 대화는 한국어로, 일상적인 말로 합니다.

## 2. 지금 상태 (2026-10-02)
- 교재 품질 개선(체인 ⑨)은 대상 32챕터가 모두 끝났습니다. Ch 1~31과 Ch 34, 236절(챕터 끝 실습 절 포함)이고 Ch 22는 시범 챕터였습니다. Ch 32(Docker)·Ch 33(CI/CD)은 사용자 결정으로 뺐습니다. 대상 챕터는 모두 「완료(강사 확인 대기)」, Ch 22만 강사 확인 끝.
- 전체 마감(2026-09-30~10-01, 1~7단계)도 끝났습니다. 236절 게이트 G1~G7 0건, 코드 셀 5,282개, 학생 묶음 zip 10개 = 디스크. 기록은 textbook/qa/final-close-log.md.
- 남은 일은 모두 사람이 정할 것입니다(textbook/qa/upgrade-final-checklist.md 맨 위 절).
  ① Part 5·6 노트북 함수 타입힌트 — AGENTS.md §15 「타입힌트를 사용한다」와 개선 챕터의 결정(힌트 없음)이 부딪침
  ② Ch 29 01절 assert 0개 — AGENTS.md §15 「assert 또는 검증 셀」
  ③ Ch 2 01~12절 복습 문항 6개(규칙 3~5개) — Part 1 전달 검사가 멈춤
  ④ Ch 12 03·04·05절 그림 라벨이 화면 검사 허용치를 0.552px 넘음 → 정한 뒤 다시 찍고 finalize_continuity_evidence.py
  ⑤ 2026-09-10 언어 감사 기준 스크립트 둘을 새 감사로 할지 은퇴시킬지
  ⑥ build_index.py Ch 13 설명의 과정 금지어 「분기」
  ⑦ 다시 렌더·재실행 때 함께 고칠 글
  ⑧ Ch 22 옛 그림 24개(공개 목록에 남음)
  ⑨ Ch 13 runs/graph-integrated-result.json(공개 목록·묶음에 있음)
  ⑩ 옛 화면 기록 파일을 둘지 새로 모을지
  ⑪ 일부 챕터 요약이 적은 실습 폴더 .venv가 사용자 것인지
  과정 전체 결정: 코드 양 증가 수용 · 목차 절 수에 실습 절 포함 여부 · 묶음 실행 검사 후보 · 실습 폴더 잠금 정리 · openai 판 차이 · Part 6 묶음의 Ch 19 잠금 · 도구 파일 안내 문장 · 「예상 비용」의 뜻 · 규격 반영 · 기록 파일의 옛 해시 · 막아 둔 .moai 스크립트 · 삽화(Ch 4 02-5 대기) · 2차 검토(한국어 감사·삽화 판독·Windows·macOS 실행) · 제외 챕터로 넘긴 문장 · OpenAI 계정의 Ch 34 02 Batch 파일 4건 · 강사 확인 331항목

## 3. 읽는 순서
1) AGENTS.md 맨 위 「지금 상태와 이어서 작업하기 (2026-10-02)」 절 (CLAUDE.md가 AGENTS.md를 불러옴)
2) docs/claude-project/quality-upgrade-status.md
3) textbook/qa/upgrade-final-checklist.md 맨 위 「전체 마감 결과」 절
4) textbook/qa/final-close-log.md
5) 할 일을 고른 뒤: textbook/QUALITY-UPGRADE.md(규격), textbook/_notebook/upgrade/PLAYBOOK.md(절차), textbook/_notebook/upgrade/AGENT-BRIEF.md(절 작업자 기본 지시), textbook/qa/upgrade-course-summary.md(판단 기준), textbook/qa/upgrade-contracts.md(산출 파일 계약), textbook/qa/upgrade-progress.md와 챕터별 qa/upgrade/chapter-summary.md

## 4. 사용자가 정한 작업 규칙 (모두 지킵니다)
- 절 작업자·검토자·마감 담당은 모두 Opus로 합니다. 챕터는 차례대로 한 챕터씩, 한 챕터 안에서는 준비 → §01..N(절마다 하나씩) → 새 실습 절 → 검토 A·B를 동시에 → 마감 → 누적 문서 → 프로젝트 문서 동기화 순서입니다.
- 워크플로(Workflow) 도구는 쓰지 않습니다. 병렬로 여러 챕터를 고치지 않습니다.
- 규격 §2-7(앞에서 배운 함수는 도구 파일에서 가져오기) 규칙과 코드 밀도 규칙은 바꾸지 않습니다.
- API 키 값은 출력하거나 저장하지 않습니다. 키는 저장소 루트 .env에서만 읽습니다.
- 지우기는 꼭 필요하거나 사용자가 승인했을 때만 합니다. 하위 작업자는 지우지 않고 보고만 합니다. 작업 지시에 rm을 넣지 않습니다.
- korean-spell-check는 글을 바깥 서비스로 보내므로 공개 문서에만 씁니다.
- 사용자가 금지한 표현(과정 규칙) — 「한」「겹」「더」를 이어 쓴 세 어절 — 은 어디에도 쓰지 않습니다. 금지어 목록에 적을 때도 글자를 나눠 적습니다.
- 발표 자료 디자인은 평범하게 합니다. 대본은 일상적인 말로, 동작 지시·시간 표기 없이, 추상적이지 않게 자세히 씁니다. 교육일지 같은 공적 문서는 초보자용 순화어 대신 표준 용어로 씁니다.
- Higgsfield 삽화는 절마다 1장, 다시 만들기는 최대 1회입니다(서비스 쪽 실패는 세지 않음). 크레딧은 거래 기록으로 확인합니다. 마감 담당은 Higgsfield를 부르지 않습니다.
- 작업 기기에서 띄우는 서버는 127.0.0.1에만 묶고, 끝나면 프로세스를 정리합니다.
- Batch 작업은 Ch 34 02절 조건(노트북 밖에서 한 번, 5줄 이하, 30분 안 기다림) 밖에서는 만들지 않습니다.
- 실제 모델은 temperature=0, reasoning_effort="none"으로 부릅니다. 모델 판정이 결론인 절은 노트북 밖에서 같은 요청을 5번 보내 흔들림을 확인하고, 판단 규칙(§0)은 첫 요청 전에 기록합니다. 흔들리는 값은 결과 읽기 둘째 단락·표·「확인할 점」·참고 블록에만 두고, 모델 출력에는 assert를 쓰지 않습니다. 새 커널로 두 번 실행해 같은 값만 결론과 그림에 씁니다.
- 그림 색: 자료 초록, 우리 코드 파랑, 실제로 부른 모델 보라, 출력·오류 노랑, 라이브러리 회색. 빨강은 paired 절 Before의 결함 결과에만 씁니다.

## 5. 작업 방식
- 한 챕터씩, 한 절씩 순서대로 합니다. 절 작업자 → 새 실습 절 → 검토 A·B → 마감 → 누적 문서(upgrade-course-summary.md·upgrade-contracts.md·upgrade-progress.md·upgrade-final-checklist.md) → 프로젝트 문서 동기화 순서이고, 모두 Opus입니다. 워크플로 도구는 쓰지 않습니다.
- 하위 작업자에게는 textbook/_notebook/upgrade/AGENT-BRIEF.md를 기본 지시로 넘기고, 절차는 PLAYBOOK.md를 따릅니다. 절 하나는 bash textbook/_notebook/upgrade/run_section.sh <챕터 폴더> NN [--no-exec]로 생성기 → 새 커널 실행 → Mermaid 렌더 → 빌드 → verify → 게이트까지 돌립니다.
- 마감 전에는 게이트 G1~G7 0건, verify PASS, 화면 검사, 검토 반영을 확인합니다. 끝낸 척하지 않고, 막힌 것은 무엇이·왜·선택지로 보고합니다.
- 사용자에게 무엇을 할지 먼저 묻고, 계획과 완료 기준을 보여 승인받은 뒤 실행합니다.

## 6. 이 컴퓨터에서 먼저 확인할 것 (docs/NEW-MACHINE-SETUP.md)
- 저장소가 $HOME/mnt/한국경제신문에서 보이는지(스크립트가 가정하는 경로).
- 루트 .env가 있고 OPENAI_API_KEY 이름이 들어 있는지 — 이름만 확인하고 값은 출력하지 않습니다.
- uv, Python 3.12, node(20 이상)가 있는지.
- /tmp/mmd(mermaid-cli 11.17.0)·/tmp/pptr-cache, Linux면 /tmp/libs, 화면 검사용 /tmp/pw·/tmp/pw-browsers가 있는지.
- Ch 12·23·31을 다시 실행할 일이 있으면 .cache/vm/pgenv(PostgreSQL 17.11 + pgvector 0.8.1)와 .cache/vm/pgdata가 있는지.
- 읽기만 하는 확인 둘: NEW-MACHINE-SETUP.md 8단계 (1) 게이트(절 236·코드 셀 5282·합 0 기대)와 (2) zipcheck.py(zip 10개 diff 0 기대).
- 없는 것은 목록으로 보고하고, 설치는 사용자 승인을 받은 뒤 합니다.

## 7. 다음 후보 작업
- 남은 사람 결정 ①~⑪과 과정 전체 결정입니다. 무엇부터 할지는 사용자에게 묻습니다.
- 참고로 지난 진행 문서가 적은 순서는 이렇습니다. 첫째, ④ Ch 12 그림 라벨을 정하면 그림을 고치거나 검사 허용치를 정한 뒤 Ch 12 화면을 다시 찍고 textbook/part3/qa/finalize_continuity_evidence.py를 돌립니다. 둘째, ①~③을 정하면 규칙이나 해당 노트북·원고를 고친 뒤 묶음을 다시 만들고 Part 7 기준 파일을 새로 만듭니다. 셋째, 2차 검토(한국어 감사·삽화 판독·Windows·macOS 실행) — 검토 묶음 236절이 준비돼 있습니다.

## 8. claude.ai 프로젝트 「한국경제신문_LLM_Agent」와의 관계
- 프로젝트 문서 여섯은 저장소 문서의 사본입니다. 한쪽을 바꾸면 다른 쪽도 같은 내용으로 맞춥니다.
  claude/quality-upgrade-status.md ↔ docs/claude-project/quality-upgrade-status.md
  textbook/final-close-log.md ↔ textbook/qa/final-close-log.md
  textbook/upgrade-final-checklist.md ↔ textbook/qa/upgrade-final-checklist.md
  textbook/upgrade-final-check-2026-09-30.md ↔ textbook/qa/upgrade-final-check-2026-09-30.md
  textbook/upgrade-course-summary.md ↔ textbook/qa/upgrade-course-summary.md
  textbook/QUALITY-UPGRADE.md ↔ textbook/QUALITY-UPGRADE.md
- 프로젝트 문서는 통째로 다시 쓰는 방식이라, 저장소 원본을 먼저 고친 뒤 같은 내용을 올립니다.

## 9. 지금 할 일
위 3번 순서대로 읽고, 지금 상태를 다섯 줄 안으로 요약해 주세요. 6번 항목을 확인만 해서 알려 주세요(설치·수정 없이). 그다음 7번 가운데 무엇부터 할지 저에게 물어봐 주세요.
```
