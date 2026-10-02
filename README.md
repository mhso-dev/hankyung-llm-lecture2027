# 한경 KDT 「LLM Agent 개발 & 바이브코딩」 교재

한국경제신문 KDT 「LLM Agent 개발 & 바이브코딩」 과정(2026년 12월 개강, 24주)의 교재 작업 저장소입니다. 세 가지가 들어 있습니다.

- **HTML 교재** — 개념 하나를 한 절로 쓴 자습용 교재입니다. Jupyter 노트북 모양 화면에 코드와 실제 실행 출력이 함께 실려 있습니다. Part 1~7, Ch 1~34입니다.
- **실습 노트북** — 교재 절마다 같은 셀과 출력을 가진 노트북이 있습니다. 챕터마다 고정한 패키지(`pyproject.toml`·`uv.lock`)로 실행합니다.
- **검사 도구** — 노트북 실행, 교재 빌드, 품질 게이트, 학생 묶음·그림·화면·연속성 검사 스크립트입니다.

과정표는 [`커리큘럼_v6.html`](커리큘럼_v6.html)(「LLM Agent 개발 & 바이브코딩 — 커리큘럼」)입니다.

## 지금 상태 (2026-10-02)

교재 품질 개선이 **대상 32챕터 모두 끝났습니다**(Ch 1~31·Ch 34, 236절 — 챕터 끝 실습 절 포함, Ch 22는 시범). Ch 32(Docker)·Ch 33(CI/CD)은 이번 개선에서 뺐습니다. 전체 마감(2026-09-30~10-01)도 끝나 236절 모두 품질 게이트 0건이고, 학생 묶음 10개가 디스크 내용과 같습니다. 남은 일은 사람이 정할 결정(타입힌트 규칙, Ch 12 그림 라벨, 복습 문항 수, 2차 검토 등)입니다.

- 한 장 요약: [`docs/claude-project/quality-upgrade-status.md`](docs/claude-project/quality-upgrade-status.md)
- 남은 결정: [`textbook/qa/upgrade-final-checklist.md`](textbook/qa/upgrade-final-checklist.md) 맨 위 「전체 마감 결과」 절
- 작업 지침: [`AGENTS.md`](AGENTS.md) 맨 위 「지금 상태와 이어서 작업하기」 절

## 교재 보기

브라우저로 [`textbook/index.html`](textbook/index.html)을 엽니다. 과정 전체 목차에서 Part 목차(`textbook/partN/index.html`), 챕터 목차(`textbook/partN/chNN-…/index.html`), 절 쪽으로 이어집니다. 쪽마다 HTML 파일 하나로 완결되어 있습니다. 글꼴과 코드 색은 인터넷(Google Fonts·highlight.js CDN)에서 불러오므로 연결이 없으면 모양만 조금 달라집니다.

HTML은 읽고 코드를 복사하는 화면입니다. 코드는 Jupyter(또는 VS Code 노트북)에서 실행합니다.

## 실습 묶음

학생에게 나눠 주는 묶음은 [`textbook/downloads/`](textbook/downloads/)에 있습니다.

| 파일 | 담긴 것 |
|---|---|
| `llm-practice.zip` | 전체 노트북 246개와 실행에 필요한 공개 자료(아래 묶음 아홉의 합) |
| `part1-practice.zip` ~ `part7-practice.zip` | Part별 노트북과 자료 |
| `ch01-practice.zip`·`ch02-practice.zip` | Ch 1·Ch 2만 |

묶음을 풀면 `시작하기.md`가 있습니다. 실습 시작 방법(폴더 구조 유지, `env.example`을 `.env`로 복사, 챕터 폴더에서 `uv sync --locked`, VS Code 커널 고르기)은 [`textbook/_notebook/practice-start.md`](textbook/_notebook/practice-start.md)와 각 Part의 `practice-start.md`에 있습니다.

## 폴더 구조

```text
.
├── README.md              이 문서
├── AGENTS.md              작업 지침 원본 (맨 위 「지금 상태와 이어서 작업하기」 절부터 읽음)
├── CLAUDE.md              Claude가 AGENTS.md를 불러오게 하는 한 줄
├── 커리큘럼_v6.html        과정표
├── .env.example           키 이름 예시 — 복사해서 .env 로 (값은 올리지 않음)
├── docs/
│   ├── NEW-MACHINE-SETUP.md   새 컴퓨터 준비
│   ├── RESUME-PROMPT.md       새 컴퓨터의 Claude에게 붙여 넣을 프롬프트
│   └── claude-project/        claude.ai 프로젝트 문서 사본 (진행 상황)
├── textbook/              HTML 교재
│   ├── index.html             과정 전체 목차 (여기서 시작)
│   ├── QUALITY-UPGRADE.md     품질 개선 규격
│   ├── AUTHORING.md           새 절을 쓸 때의 기준
│   ├── part1/ … part7/        Part 목차와 챕터 폴더
│   │   └── chNN-…/            절 HTML · _src/(원고 원본) · figures/(Mermaid·삽화) · qa/(챕터 기록) · chapter.json
│   ├── downloads/             학생 실습 묶음 zip 10개
│   ├── qa/                    과정 전체 기록과 검사 스크립트 (진행표·점검표·마감 기록·계약)
│   ├── _notebook/             실행·빌드·검사 도구 (execute.py · render.py · verify.py · visual.cjs · mermaid/ · upgrade/ · checks/)
│   └── _template/             새 챕터 골격 도구
├── labs/                  실습 폴더
│   ├── part1/ … part7/chNN-…/ pyproject.toml · uv.lock · notebooks/ · README.md (챕터마다)
│   └── data/                  여러 챕터가 쓰는 자료 (rag-corpus)
├── .moai/                 프로젝트 맥락과 옛 작업 근거 (context.md · evolution/ · credentials.env — 키 이름 안내만, 값 없음)
├── .claude/agents/ · .codex/agents/   작업 에이전트 정의
├── .cache/final-close/    전체 마감 단계별 기록·도구 (나머지 .cache 는 올리지 않음)
├── qa/language/           Part 7 한국어 감사 옛 기록 (2026-09-11)
├── _workspace/            2026-09-10~11 한국어 윤문 작업 기록
├── Claude outputs/        Ch 22 시범 개선 때의 사본 (옛 자료)
└── 01-…ipynb ~ 08-…ipynb  Ch 5 옛 노트북 사본 (실행 출력 없음 — 교재와 묶음은 labs/part1/ch05-llm-principles/notebooks/ 를 씀)
```

## 새 컴퓨터에서 시작하기

1. [`docs/NEW-MACHINE-SETUP.md`](docs/NEW-MACHINE-SETUP.md)대로 준비합니다. 저장소를 `한국경제신문`이라는 폴더 이름으로 받고, `.env`를 만들고, Python 3.12·uv·도구를 설치합니다.
2. Claude(Cowork 또는 Claude Code)에게 [`docs/RESUME-PROMPT.md`](docs/RESUME-PROMPT.md)의 프롬프트를 붙여 넣습니다.

## 비밀값

- 실제 키는 저장소 루트의 `.env`에만 둡니다. `.env`는 `.gitignore`에 있어 올라가지 않습니다.
- 새로 받았으면 `.env.example`을 `.env`로 복사한 뒤 값을 채웁니다. 키 이름은 `OPENAI_API_KEY`(필수), `ANTHROPIC_API_KEY`·`GOOGLE_API_KEY`(Ch 6 세 제공자 비교 — 선택), `LANGSMITH_API_KEY`(Ch 15 — 선택)입니다.
- 키 값을 채팅·노트북·출력·문서에 붙여 넣지 않습니다. 붙여 넣었다면 그 키는 폐기하고 다시 발급합니다.
- 학생 묶음에는 실제 키가 들어 있지 않습니다(`textbook/part7/qa/check_secrets.py`로 확인).

## 주요 문서

| 문서 | 내용 |
|---|---|
| [`AGENTS.md`](AGENTS.md) | 작업 지침 — 지금 상태, 사용자 작업 규칙, 집필·실행·그림 규격 |
| [`docs/NEW-MACHINE-SETUP.md`](docs/NEW-MACHINE-SETUP.md) | 새 컴퓨터 준비와 검사 명령 |
| [`docs/RESUME-PROMPT.md`](docs/RESUME-PROMPT.md) | 「이어서 작업하기」 프롬프트 |
| [`docs/claude-project/quality-upgrade-status.md`](docs/claude-project/quality-upgrade-status.md) | 품질 개선 진행 상황 한 장 |
| [`textbook/QUALITY-UPGRADE.md`](textbook/QUALITY-UPGRADE.md) | 품질 개선 규격 (코드 문법 사다리·실제 모델 호출·문장·그림·노트북·게이트) |
| [`textbook/_notebook/upgrade/PLAYBOOK.md`](textbook/_notebook/upgrade/PLAYBOOK.md) | 절 하나를 고치는 실행 절차 |
| [`textbook/_notebook/upgrade/AGENT-BRIEF.md`](textbook/_notebook/upgrade/AGENT-BRIEF.md) | 절 작업자에게 넘기는 기본 지시 |
| [`textbook/qa/upgrade-final-checklist.md`](textbook/qa/upgrade-final-checklist.md) | 전체 마감 점검표 — 맨 위 절이 남은 결정 |
| [`textbook/qa/final-close-log.md`](textbook/qa/final-close-log.md) | 전체 마감 1~7단계 기록 |
| [`textbook/qa/upgrade-final-check-2026-09-30.md`](textbook/qa/upgrade-final-check-2026-09-30.md) | 전체 점검 보고서 |
| [`textbook/qa/upgrade-course-summary.md`](textbook/qa/upgrade-course-summary.md) | 과정 요약 — 절을 쓸 때의 판단 기준 |
| [`textbook/qa/upgrade-contracts.md`](textbook/qa/upgrade-contracts.md) | 산출 파일·데이터 계약, 기준 버전 |
| [`textbook/qa/upgrade-progress.md`](textbook/qa/upgrade-progress.md) | 챕터별 진행 기록 |
| [`textbook/qa/deletion-manifest-2026-10-01.md`](textbook/qa/deletion-manifest-2026-10-01.md) | 전체 마감 때 지운 것과 남긴 것 |
