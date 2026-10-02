# 새 컴퓨터에서 이어 가기 — 준비 단계

이 문서는 저장소를 새 맥(또는 Linux)에 받아 교재 작업을 이어 가기 위한 준비 순서입니다. 경로는 모두 저장소 루트 기준입니다. 2026-10-02에 옛 작업 기기(Cowork Linux VM, aarch64)에서 쓰던 명령과 스크립트를 읽고 정리했습니다.

## 0. 저장소에 없는 것

저장소에는 다음이 들어 있지 않습니다. 새 컴퓨터에서 다시 준비합니다.

| 없는 것 | 까닭 | 다시 준비하는 곳 |
|---|---|---|
| `.env`(API 키) | 비밀값 | 2단계 |
| 실습 폴더의 `.venv` | 컴퓨터마다 다시 만드는 가상환경 | 3단계 |
| `.cache/vm/`(PostgreSQL `pgenv`·데이터 `pgdata`) | 작업 기기 전용 실행 환경 | 6단계 |
| `/tmp`의 Mermaid·playwright 도구 | 기기를 다시 만들거나 재부팅하면 사라짐 | 4·5단계 |
| 실습 폴더 `.cache/`(Ch 9·10 강사용 확장 스크립트의 임베딩 캐시) | 다시 만들 수 있는 캐시 | 그 스크립트를 다시 돌리면 새로 만듦(임베딩 요청이 생김) |
| `.cache/` 나머지, 파이썬 캐시, `.DS_Store`, `.omx/` | 캐시와 로컬 도구 상태 | 필요 없음 |

전체 마감 기록(`.cache/final-close/`, 약 11MB)은 저장소에 함께 올렸습니다. 마감 기록 문서(`textbook/qa/final-close-log.md`)가 가리키는 전후 해시·도구가 여기에 있습니다.

## 1. 저장소 받기

한글 파일 이름이 약 1만 개 있습니다. 받기 전에 git 설정을 한 번 해 둡니다.

```bash
git config --global core.precomposeunicode true   # 맥에서 한글 파일 이름을 한 가지 모양(NFC)으로 다룸
git config --global core.quotepath false          # git status 에 한글 이름을 그대로 보여 줌
```

저장소는 **`한국경제신문`이라는 폴더 이름으로** 받습니다. 작업 스크립트가 이 이름을 씁니다. 크기는 약 830MB입니다.

```bash
mkdir -p ~/working/claude/projects
cd ~/working/claude/projects
git clone https://github.com/mhso-dev/hankyung-llm-lecture2027.git 한국경제신문
cd 한국경제신문
```

### 작업 스크립트가 가정하는 경로

`textbook/_notebook/upgrade/run_section.sh`·`pack.py`·`patch.py`·`mdpatch.py`와 Ch 12·23·31의 `qa/upgrade/pre_exec.sh`는 저장소 위치를 **`$HOME/mnt/한국경제신문`**으로 가정합니다. 검사 스크립트(`textbook/qa/*.py`·`textbook/partN/qa/*.py`·`verify.py`·`upgrade_gates.py`)는 자기 위치에서 루트를 찾으므로 경로와 상관없습니다.

- **Cowork(Claude 데스크톱 앱)에서 작업할 때**: 받은 `한국경제신문` 폴더를 Cowork에 연결합니다. 기기 셸에서는 자동으로 `$HOME/mnt/한국경제신문`에 보입니다. 기기 셸은 Linux입니다.
- **Claude Code나 터미널에서 바로 작업할 때**: 그 경로에 링크를 하나 둡니다.

```bash
mkdir -p ~/mnt
ln -s ~/working/claude/projects/한국경제신문 ~/mnt/한국경제신문
ls ~/mnt/한국경제신문/AGENTS.md    # 파일 이름이 보이면 됨
```

### git으로 받은 뒤 달라지는 점

- 파일 시각이 모두 받은 시각이 됩니다. 「기록이 HTML보다 오래됨」 같은 시각 비교로 다시 할 일을 고르지 말고, 해시와 내용으로 대조합니다. Mermaid 렌더 도장(`*.render.json`)은 내용 해시라 그대로 씁니다.
- 실행 권한 비트는 쓰지 않습니다. 스크립트는 `bash …`·`python3 …`로 부릅니다.

## 2. `.env` 만들기

```bash
cp .env.example .env
```

편집기로 `.env`를 열어 `=` 오른쪽에 값을 넣습니다. 값은 채팅이나 문서에 붙여 넣지 않습니다.

| 키 이름 | 쓰는 곳 |
|---|---|
| `OPENAI_API_KEY` | **필수** — Ch 6 이후 실제 모델을 부르는 절, Part 3 연속성 묶음 검사 |
| `ANTHROPIC_API_KEY` | 선택 — Ch 6 세 제공자 비교 |
| `GOOGLE_API_KEY` | 선택 — Ch 6 세 제공자 비교 |
| `LANGSMITH_API_KEY` | 선택 — Ch 15 트레이싱 |

- 키는 저장소 루트 `.env`에서만 읽습니다. 노트북은 `find_dotenv(usecwd=True)`로 위 폴더를 거슬러 올라가며 이 파일을 찾습니다.
- `.env`가 올라가지 않는지 확인: `git check-ignore -v .env`가 `.gitignore` 줄을 보여 주면 됩니다.
- `.moai/credentials.env`는 키 이름과 발급처 안내만 있는 파일입니다(값 없음).
- 옛 컴퓨터의 키를 옮기거나, 새로 발급합니다. 채팅에 붙여 넣은 적이 있는 키는 폐기하고 다시 발급합니다.

## 3. Python 3.12·uv와 실습 환경

### 설치

```bash
# uv (맥은 brew install uv 도 됨)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12
uv --version            # 옛 작업 기기는 0.12.x
python3 --version       # 생성기·검사 스크립트용 — 3.10 이상, 연속성 검사 하나는 3.11 이상
node --version          # Mermaid·화면 검사용 — 20 이상 (옛 작업 기기 22). 맥은 brew install node
```

시스템 `python3`가 3.11보다 낮으면 `textbook/qa/check_course_continuity.py`만 `uv run --no-project --python 3.12 python …`으로 부릅니다. 나머지 검사·빌드 스크립트는 표준 라이브러리만 씁니다.

### 실습 폴더 가상환경

34개 실습 폴더(`labs/partN/chNN-…/`)마다 `pyproject.toml`과 `uv.lock`이 있습니다(Python `>=3.12,<3.13`). 가상환경은 저장소에 없으므로 필요한 챕터만 만듭니다.

```bash
cd labs/part6/ch22-middleware
uv sync --locked
uv run python --version     # Python 3.12.x
cd ../../..
```

한 번에 모두 만들려면 아래처럼 합니다. Ch 5(torch·로컬 모델)와 Ch 12(리랭커)는 크고, Ch 5·12는 첫 실행 때 모델 파일(합쳐 약 6GB)을 내려받습니다.

```bash
for d in labs/part*/ch*/; do (cd "$d" && uv sync --locked) || echo "실패: $d"; done
```

### 작업 도구가 쓰는 환경 변수

절 하나를 다시 만드는 `bash textbook/_notebook/upgrade/run_section.sh <챕터 폴더> NN [--no-exec]`는 실습 폴더의 `.venv`를 쓰지 않고 아래 값을 스스로 정합니다.

| 변수 | 값 | 하는 일 |
|---|---|---|
| `UV_CACHE_DIR` | `/tmp/uv-cache` | uv 캐시 |
| `UV_LINK_MODE` | `copy` | 연결 폴더에서 링크 대신 복사 |
| `UV_PROJECT_ENVIRONMENT` | `/tmp/venv-<챕터 폴더 이름>` | 절 실행용 가상환경(없으면 `uv run`이 만듦) |
| `UV_PROJECT_ENVIRONMENT`·`HF_HOME`·`UV_NO_SYNC` | `.cache/vm/venv-<챕터>`·`.cache/vm/hf`·`1` | **`.cache/vm/venv-<챕터>`가 있을 때만** 위 값을 바꿈(디스크가 좁은 기기용) |
| `PUPPETEER_CACHE_DIR` | `/tmp/pptr-cache` | Mermaid 렌더용 Chromium 위치(4단계) |
| `LD_LIBRARY_PATH` | `/tmp/libs/root/usr/lib/<aarch64 또는 x86_64>-linux-gnu` | Linux에서 Chromium이 찾는 `libXdamage`(4단계). 맥은 무시됨 |
| `PYTHONPATH` | `<실습 폴더>/notebooks` | 노트북이 도구 파일(`*_tools.py`)을 가져오게 함 |
| `N` | 절 번호 | Ch 23 훅이 02절에서만 DB를 켬 |

직접 줄 수 있는 값: `MMDC`(mermaid-cli 실행 파일 위치, 없으면 `/tmp/mmd/node_modules/.bin/mmdc`), `UPGRADE_RUN_DATE`(노트북에 적는 실행 날짜를 고정). 노트북 실행(`textbook/_notebook/execute.py`)은 `uv run --project <실습 폴더> --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip --with python-dotenv==1.2.3`으로 새 커널을 띄웁니다.

**디스크가 좁은 기기**(Cowork VM 루트 9.6GB 등)에서 큰 챕터를 다시 실행할 때는 가상환경을 저장소 폴더 안 `.cache/vm/`에 먼저 만들어 둡니다(`.cache/`는 올라가지 않음). 이 폴더가 있으면 `run_section.sh`가 `UV_NO_SYNC=1`로 그대로 쓰므로 미리 완전히 만들어야 합니다.

```bash
ROOT=$HOME/mnt/한국경제신문; CH=ch05-llm-principles
UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-$CH \
  uv sync --locked --project $ROOT/labs/part1/$CH
```

## 4. Mermaid 렌더 도구

그림 원본은 챕터 `figures/*.mmd`이고, `textbook/_notebook/mermaid/render_mermaid.py`가 SVG(본문)·PNG(노트북)로 렌더합니다. 도구는 `/tmp`에 둡니다(약 1.1GB). 출처: `textbook/_notebook/mermaid/README.md`.

```bash
mkdir -p /tmp/mmd && cd /tmp/mmd
export npm_config_cache=/tmp/npm-cache PUPPETEER_CACHE_DIR=/tmp/pptr-cache
npm install --no-audit --no-fund @mermaid-js/mermaid-cli@11.17.0
/tmp/mmd/node_modules/.bin/mmdc --version     # 11.17.0
```

Linux에서만 — Chromium이 `libXdamage.so.1`을 찾지 못할 때:

```bash
mkdir -p /tmp/libs && cd /tmp/libs && apt-get download libxdamage1 && dpkg-deb -x libxdamage1_*.deb root
```

- `run_section.sh`가 `PUPPETEER_CACHE_DIR=/tmp/pptr-cache`로 고정하므로 다른 곳에 설치하지 않습니다.
- 맥은 재부팅하면 `/tmp`가 비고, Cowork VM은 기기를 다시 만들면 비어서 그때마다 다시 설치합니다.
- 렌더는 원본과 설정이 같으면 건너뜁니다(`.render.json`). 같은 원본을 다시 렌더할 때만 `--force`를 줍니다.

## 5. 화면 검사 도구 (playwright)

`textbook/_notebook/visual.cjs`는 챕터 HTML을 1280px·390px 두 폭으로 열어 글자 크기·대비·잘림·가로 넘침·그림 경계를 잽니다. 옛 작업 기기는 playwright 1.63.0과 Chromium headless shell을 `/tmp`에 두었습니다.

```bash
mkdir -p /tmp/pw && cd /tmp/pw
npm init -y >/dev/null
npm install --no-audit --no-fund playwright@1.63.0
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers npx playwright install --only-shell chromium
```

실행(예: Ch 12):

```bash
cd $HOME/mnt/한국경제신문
NODE_PATH=/tmp/pw/node_modules PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers \
LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu \
node textbook/_notebook/visual.cjs textbook/part3/ch12-retrieval-tuning
```

- 결과는 `textbook/_notebook/checks/<챕터 폴더 이름>/visual-results.json`과 PNG에 덮어씁니다(저장소에 있는 파일). 끝나면 `git status`로 바뀐 파일을 확인합니다.
- `LD_LIBRARY_PATH`는 Linux에서만 필요합니다(x86_64는 `x86_64-linux-gnu`). 이 값이 없으면 브라우저가 `libXdamage.so.1`을 못 찾아 결과를 쓰기 전에 멈춥니다.
- 글꼴과 렌더가 기기마다 조금 달라 0.1~0.5px 차이가 날 수 있습니다. Ch 12 라벨 0.552px(점검표 ④)처럼 경계에 걸린 값은 같은 종류의 기기에서 견줍니다.

## 6. DB가 필요한 챕터 (Ch 12·23·31) — PostgreSQL + pgvector

교재 본문은 학생 기준으로 Docker 컨테이너를 씁니다. 옛 작업 기기에는 Docker가 없어 conda-forge PostgreSQL을 `.cache/vm/pgenv`에 두고, `run_section.sh`가 절 실행 직전에 챕터 `qa/upgrade/pre_exec.sh`를 불러 서버를 켰습니다. 이 둘은 저장소에 없으므로 다시 만듭니다.

### 훅이 기대하는 것

| 챕터 | 훅이 하는 일 | 필요한 것 |
|---|---|---|
| Ch 12 (01~03절) | `.cache/vm/pgenv/bin/pg_ctl`로 **이미 있는** 데이터 폴더 `.cache/vm/pgdata`를 `127.0.0.1:55432`에 켬. `initdb`는 하지 않음. `pg_ctl`이 없으면 아무 말 없이 넘어감(로그 `/tmp/pg-ch12.log`) | `pgenv` + `pgdata`(계정 `student`, 데이터베이스 `rag_lab`) |
| Ch 23 (02절만) | `pgenv/bin`으로 `/tmp/ch23-02/pgdata`에 새 클러스터를 만들어(없을 때만) `55432`에 켜고, 끝나면 끔. 55432를 다른 서버가 쓰고 있으면 멈춤 | `pgenv`만 |
| Ch 31 (모든 절) | `pgenv/bin`으로 `/tmp/ch31-pg/data`에 새 클러스터를 만들어(없을 때만) `55431`에 켜고(계정 `postgres`, 데이터베이스 `ch31_lab`), 끝나면 끔. `pg_dump`를 찾도록 `pgenv/bin`을 `PATH` 끝에 더함 | `pgenv`만 |

Ch 23·31 훅은 `pgenv`가 없으면 `initdb`에서 실패해 `run_section.sh`가 멈춥니다. 작업 도구로 이 챕터들을 다시 실행하려면 `pgenv`가 있어야 합니다.

### `pgenv` 다시 만들기 (micromamba)

옛 작업 기기의 기록(`pgenv/conda-meta/history`, 2026-09-18)은 `micromamba create -y -p …/.cache/vm/pgenv -c conda-forge postgresql=17 pgvector`이고, 설치된 판은 PostgreSQL 17.11·pgvector 0.8.1입니다. 교재 출력과 맞추려면 판을 고정합니다.

```bash
cd $HOME/mnt/한국경제신문
mkdir -p .cache/vm/mamba && cd .cache/vm/mamba
# 맥(Apple Silicon): osx-arm64 · Linux aarch64: linux-aarch64 · Linux x86_64: linux-64
curl -Ls https://micro.mamba.pm/api/micromamba/osx-arm64/latest | tar -xvj bin/micromamba
cd $HOME/mnt/한국경제신문
export MAMBA_ROOT_PREFIX=$PWD/.cache/vm/mamba
./.cache/vm/mamba/bin/micromamba create -y -p "$PWD/.cache/vm/pgenv" -c conda-forge postgresql=17.11 pgvector=0.8.1
.cache/vm/pgenv/bin/postgres --version     # postgres (PostgreSQL) 17.11
```

### Ch 12용 `pgdata` 다시 만들기

옛 데이터 폴더는 계정 `student`, 암호 방식 md5, 로케일 C.UTF-8이었습니다. 같은 모양으로 만듭니다. 암호 `local-practice-only`는 교재와 실습 README에 이미 적힌 수업 전용 연습 값입니다.

```bash
cd $HOME/mnt/한국경제신문
PGBIN=$PWD/.cache/vm/pgenv/bin; PGDATA=$PWD/.cache/vm/pgdata
printf '%s\n' 'local-practice-only' > /tmp/ch12-pwfile
"$PGBIN/initdb" -D "$PGDATA" -U student --pwfile=/tmp/ch12-pwfile -A md5 --encoding=UTF8 --locale=C
"$PGBIN/pg_ctl" -D "$PGDATA" -o "-p 55432 -c listen_addresses=127.0.0.1" -l /tmp/pg-ch12.log -w start
PGPASSWORD=local-practice-only "$PGBIN/createdb" -h 127.0.0.1 -p 55432 -U student rag_lab
"$PGBIN/psql" "postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab" -tAc \
  "SELECT name, default_version FROM pg_available_extensions WHERE name = 'vector'"   # vector|0.8.1
"$PGBIN/pg_ctl" -D "$PGDATA" -m fast -w stop
```

`vector` 확장은 Ch 12 02절 노트북이 `CREATE EXTENSION IF NOT EXISTS vector`로 만듭니다. 서버는 `127.0.0.1`에만 묶고, 확인이 끝나면 끕니다.

### Docker가 있는 컴퓨터 — 학생 방식

노트북을 학생처럼 직접 열어 확인할 때는 교재의 Docker 명령을 그대로 씁니다(각 실습 폴더 README).

```bash
# Ch 12 (Ch 23 02절도 같은 컨테이너를 씀)
docker run --name hankyung-part3-pgvector \
  -e POSTGRES_USER=student -e POSTGRES_PASSWORD=local-practice-only -e POSTGRES_DB=rag_lab \
  -p 127.0.0.1:55432:5432 -d pgvector/pgvector:0.8.2-pg17

# Ch 31
docker run --name kdt-ch31-postgres \
  -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=ch31_lab \
  -p 127.0.0.1:55431:5432 -d pgvector/pgvector:0.8.1-pg17
```

- 컨테이너가 55432·55431을 쓰고 있으면 Ch 23·31 훅은 다른 서버로 보고 멈춥니다. 작업 도구로 다시 실행하기 전에는 `docker stop …`으로 끕니다.
- 훅은 Linux VM에서 쓰려고 만들었습니다. Ch 31 훅의 남은 잠금 파일 처리는 `/proc`를 읽으므로 맥에서는 그 부분이 동작하지 않습니다. 맥에서 `/tmp/ch31-pg/data/postmaster.pid`가 남아 서버가 안 켜지면 서버를 끄거나 그 파일을 다른 이름으로 옮깁니다.

## 7. 외부 도구 연결

| 도구 | 쓰는 곳 | 확인 |
|---|---|---|
| Higgsfield | 삽화(`nano_banana_pro`, 16:9, 2k) | claude.ai 커넥터입니다. 같은 계정이면 연결이 따라오는지 크레딧 잔액과 거래 기록으로 확인합니다. 삽화는 절마다 1장, 다시 만들기 최대 1회, 마감 담당은 부르지 않습니다 |
| `korean-spell-check` | 한국어 감사 2차 | moai-writer 플러그인 스킬입니다. 글을 바깥 서비스(`nara-speller.co.kr`)로 보내므로 **공개 문서에만** 씁니다. 플러그인이 안 보이면 Cowork에서 다시 설치합니다(설치 목록은 `AGENTS.md` 머리말) |
| Excalidraw | 도식 초안(선택) | claude.ai 커넥터, 키 없음 |
| claude.ai 프로젝트 「한국경제신문_LLM_Agent」 | 진행 문서 공유 | 세션에 이 프로젝트를 붙이면 문서 여섯을 읽고 쓸 수 있습니다. 문서와 저장소 사본의 짝은 `AGENTS.md` 맨 위 절 |

키 이름과 발급처 안내는 `.moai/credentials.env`에 있습니다(값 없음).

## 8. 검사 한 바퀴

전체 마감 기록(`textbook/qa/final-close-log.md` 3·7단계)의 명령입니다. 저장소 루트에서 실행합니다.

```bash
cd $HOME/mnt/한국경제신문
export PYTHONDONTWRITEBYTECODE=1
```

**(1) 게이트 G1~G7 — 읽기만 함, 몇 초.** 기대값: 절 236, 코드 셀 5282, 게이트 합 모두 0, 실패 없음.

```bash
python3 - <<'PY'
import json, importlib.util
from pathlib import Path
root = Path.cwd()
spec = importlib.util.spec_from_file_location("ug", root / "textbook/_notebook/checks/upgrade_gates.py")
ug = importlib.util.module_from_spec(spec); spec.loader.exec_module(ug)
targets = {f"ch{n:02d}" for n in [*range(1, 32), 34]}
total = dict.fromkeys(["G1", "G2", "G3", "G4", "G5", "G6", "G7"], 0)
sections, cells, failed = 0, 0, []
for ch in sorted(root.glob("textbook/part*/ch*")):
    if ch.name[:4] not in targets:
        continue
    if (ch / "chapter.json").is_file():
        cfg = json.loads((ch / "chapter.json").read_text(encoding="utf-8"))
        lab = root / cfg["lab_path"]
        slugs = [s["slug"] for s in cfg["sections"]]
    else:
        lab = root / "labs" / ch.relative_to(root / "textbook")
        slugs = sorted(p.stem for p in (ch / "_src").glob("[0-9][0-9]-*.html"))
    for slug in slugs:
        r = ug.check_section(ch, lab, slug)
        sections += 1
        cells += r["code_cells"]
        for g, n in r["counts"].items():
            total[g] += n
        if not r["passed"]:
            failed.append(f"{ch.name}/{slug}")
print("절", sections, "코드 셀", cells, "게이트 합", total, "실패", failed or "없음")
PY
```

챕터 하나만 볼 때는 `python3 textbook/_notebook/checks/upgrade_gates.py <챕터 폴더> --label <이름>`도 됩니다. 이 명령은 `qa/upgrade/gates-<이름>.json`을 새로 쓰므로 `before`·`after`는 쓰지 않습니다(기록 파일을 덮어씀).

**(2) 학생 묶음 = 디스크 — 읽기만 함.** zip 10개 모두 `diff=0 missing=0 extra=0`이면 됩니다.

```bash
python3 .cache/final-close/4-index-zip/tools/zipcheck.py /tmp/zipcheck.json
```

**(3) 노트북·교재 대조 — `verify.py`.** 32챕터 모두 `PASS`. 결과 파일을 다시 쓰지만 내용이 같으면 바이트도 같습니다.

```bash
for ch in $(ls -d textbook/part*/ch* | grep -v -e ch32 -e ch33); do
  printf '%s ' "$ch"; python3 textbook/_notebook/verify.py --chapter "$ch" | tail -1
done
```

**(4) 전달·그림·연속성 검사** — 결과 JSON을 다시 씁니다. 끝나면 `git status`로 바뀐 파일을 봅니다.

```bash
python3 textbook/part1/qa/check_delivery.py --revised-existing   # 지금은 100행에서 멈춤(점검표 ③)
python3 .cache/final-close/4-index-zip/tools/part1_check_delivery_skip_quiz.py --revised-existing --output /tmp/part1-delivery.json   # ③ 한 줄만 건너뛴 사본(통과)
for n in 2 3 4 5 6 7; do python3 textbook/part$n/qa/check_delivery.py; done
python3 textbook/qa/check_course_delivery.py
python3 textbook/part7/qa/check_secrets.py
for n in 4 5 6 7; do python3 textbook/part$n/qa/check_figures.py; done       # 133·98·221·100쌍
python3 textbook/part3/qa/check_continuity.py
uv run --no-project --python 3.12 python textbook/qa/check_course_continuity.py
python3 textbook/part6/qa/check_visual_reports.py
python3 textbook/part5/qa/check_notebook_readiness.py   # 지금은 타입힌트에서 실패(점검표 ①)
python3 textbook/part6/qa/check_notebook_readiness.py   # 같음
```

**(5) 묶음 실행 검사 — 노트북을 실제로 돌림.** 키 없이 도는 노트북만 고른 검사입니다. 시간이 걸리고 uv가 환경을 새로 받습니다.

```bash
U="env -u UV_PROJECT_ENVIRONMENT -u UV_NO_SYNC -u OPENAI_API_KEY -u PYTHONPATH UV_LINK_MODE=symlink"
for n in 4 5 6; do $U UV_CACHE_DIR=/tmp/uv-cache python3 textbook/part$n/qa/check_bundle_execution.py; done
$U UV_CACHE_DIR=/tmp/uv-cache python3 textbook/part7/qa/check_bundle_execution.py --pre-exec   # Ch 31 훅으로 DB를 켬(6단계 pgenv 필요)
```

- Part 3 연속성 묶음 검사 `textbook/part3/qa/run_continuity_bundle.py`는 **모델을 부릅니다**(지난번 약 37번, 약 0.03달러). 사람이 정한 뒤에만 돌립니다.
- `textbook/part3/qa/finalize_continuity_evidence.py`는 점검표 ④(Ch 12 화면 라벨)를 정한 뒤에 돌립니다.
- Part 4 `check_language_freeze.py`·Part 5 `finalize_evidence.py`는 2026-09-10 언어 감사 승인 해시가 기준이라 지금 원고로는 통과하지 않습니다(점검표 ⑤).

## 9. 묶음과 목차 다시 만들기

노트북·공개 자료가 바뀐 Part만 다시 만듭니다(전체 마감 4단계 방식). 스크립트는 표준 라이브러리만 씁니다.

```bash
python3 textbook/partN/_build_index.py                                # Part N 목차 + textbook/downloads/partN-practice.zip
python3 textbook/_notebook/build_bundle.py                            # llm-practice.zip (전체)
python3 textbook/part1/ch01-development-environment/_build_delivery.py   # ch01-practice.zip
python3 textbook/part1/ch02-python/qa/build_bundle.py                 # ch02-practice.zip
python3 textbook/_notebook/build_index.py                             # textbook/index.html (과정 목차)
```

다시 만든 뒤 8단계 (2)·(4)를 돌립니다. Part 1~6의 `_src`나 노트북이 바뀌었으면 Part 7 기준 파일도 새로 만듭니다. 이 명령은 파일을 새로 만들기만 하므로(이미 있으면 멈춤) 옛 파일을 먼저 다른 이름으로 옮깁니다(지우지 않음).

```bash
mv -n textbook/part7/qa/existing-artifacts-final-close.json textbook/part7/qa/existing-artifacts-final-close.before-<날짜>.json
python3 textbook/part7/qa/check_delivery.py --write-baseline
python3 textbook/part7/qa/check_delivery.py
```

새 해시는 `textbook/qa/upgrade-contracts.md` §5에 덧붙입니다.

## 10. git 쓸 때 주의

- 한글 파일 이름: 1단계의 `core.precomposeunicode true`·`core.quotepath false`. 지금 저장소의 한글 경로는 모두 NFC 모양입니다.
- 큰 파일: 가장 큰 파일이 약 34MB입니다(`textbook/qa/continuity-evidence/full-course-before.tar.gz`, `textbook/downloads/llm-practice.zip`). GitHub 경고 기준(50MB)보다 작습니다. 묶음을 다시 만들면 zip이 새 판으로 바뀌어 저장소가 그만큼 커집니다.
- 올리기 전에 `git status`에서 `.env`·`.venv`·`.cache/vm`이 보이지 않는지 확인합니다.
- 검사 스크립트가 다시 쓰는 결과 파일(`*-results.json`·`visual-results.json` 등)이 바뀌어 보이면, 내용이 바뀐 것인지 시각·순서만 바뀐 것인지 확인하고 올립니다.

## 11. 막힐 때

- **Cowork 연결 폴더에서 `uv sync`나 SQLite가 실패**: 연결 폴더는 지우기가 막혀 있어 uv가 옛 파일을 지우다 멈추거나 SQLite 저널을 못 지웁니다. 가상환경은 `/tmp`에(`run_section.sh` 기본값), 임시 실행 폴더도 `/tmp`에 둡니다. 지우기가 꼭 필요하면 사용자 승인을 받습니다.
- **기기 셸 호출 시간 제한(Cowork 180초)**: 긴 설치·실행은 `timeout 165`로 나눠 다시 부릅니다. 호출이 끝나면 그 안에서 켠 서버도 꺼지므로 DB 훅은 절 실행마다 다시 켭니다.
- **메모리**: Ch 12 07·08절 리랭커는 메모리를 약 3GB 씁니다.
- **어느 문서를 믿을지**: `AGENTS.md` 맨 위 절과 `textbook/qa/upgrade-final-checklist.md` 맨 위 절이 지금 상태입니다. 그 아래 옛 기록은 고치지 않았습니다.
