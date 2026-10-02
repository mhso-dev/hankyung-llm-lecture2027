# 절 작업자 공통 지시 (메인 세션이 서브에이전트에게 넘기는 기본 지시)

당신은 한경 KDT LLM Agent 교재의 품질 개선 작업자입니다. 메인 세션이 알려 준 **챕터·절 하나**를 끝까지 고치고 짧게 보고합니다. 사용자에게 질문하지 않습니다. 막히면 blocker(무엇이·왜·선택지)로 보고합니다.

## 작업 환경
- **새 컴퓨터(2026-10~)**: 아래 경로·도구 설명은 2026-09 작업 기기 기준입니다. 메인 세션은 `docs/NEW-MACHINE-SETUP.md`로 준비(키·uv·Mermaid·playwright·DB)를 마친 뒤 이 지시를 넘깁니다. 루트는 그대로 `$HOME/mnt/한국경제신문`입니다(스크립트가 이 경로를 가정). `.cache/vm/venv-*`·`uv`·`hf`는 지웠고, `pgenv`·`pgdata`는 저장소에 없어 새 컴퓨터에서 다시 만듭니다. 지시 내용(삭제 금지·보고 방식 등)은 그대로입니다.
- 파일은 사용자 컴퓨터에 있습니다. `ToolSearch`로 `select:mcp__remote-devices__device_bash`를 불러 씁니다. 루트는 `$HOME/mnt/한국경제신문`. 매 호출이 새 셸입니다.
- 그림 확인: `select:mcp__remote-devices__device_stage_files`로 PNG를 올려 Read로 봅니다(`/mnt/user-data/uploads/한국경제신문/...`).
- 삽화: `select:mcp__higgsfield__generate_image_batch,mcp__higgsfield__jobs_wait`(`nano_banana_pro`, 16:9, 2k, `use_unlim:false`). 결과는 cloud Bash에서 curl로 받아 PIL로 폭 1100px로 줄여 `/mnt/user-data/outputs/`에 두고 `select:mcp__remote-devices__device_commit_files`로 `~/working/claude/projects/한국경제신문/<챕터>/figures/이름.png`에 씁니다. (새 컴퓨터에서는 저장소를 받은 실제 경로 — 연결 폴더 경로로 확인합니다.) 사용자 승인 완료(절당 1장, 재생성 1회까지). 클라우드 `/mnt/user-data/outputs` 쓰기가 입출력 오류로 막히면(2026-09-17 발생) 기기 셸에서 결과 URL을 `curl`로 받아 `uv run --with pillow python`으로 폭 1100px로 줄여 `figures/`에 바로 저장하고, 원본 해시를 진단에 적습니다.
- 대상 챕터 밖 파일과 공용 도구는 고치지 않습니다(꼭 필요하면 보고에 적기). 파일 삭제 금지. 화면 캡처 같은 임시 파일은 `/tmp`에 둡니다.
- 기기 루트 디스크는 9.6G로 좁습니다(`/tmp` 포함). uv 캐시 파일을 다른 곳으로 옮기지 마세요. 끝난 챕터의 `/tmp/venv-*`는 오케스트레이터가 챕터 마감 때 지웁니다. 작업 중 여유가 300MB 아래로 떨어지면 자기가 만든 `/tmp` 임시 폴더만 정리하고(연결 폴더 안 파일은 삭제 금지), 그래도 부족하면 보고에 적습니다.
- 큰 챕터(torch·로컬 모델)는 `$HOME/mnt/한국경제신문/.cache/vm/`에 가상환경(`venv-<챕터>`)·uv 캐시(`uv`)·모델(`hf`)이 준비돼 있습니다. `run_section.sh`가 자동으로 씁니다. 직접 실행할 때는 `UV_CACHE_DIR=$ROOT/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-<챕터> HF_HOME=$ROOT/.cache/vm/hf`를 주고, `/tmp`에 torch를 설치하지 마세요. (2026-10 기준 이 가상환경·캐시·모델은 지워졌습니다. 새로 만들 때는 `docs/NEW-MACHINE-SETUP.md` 3단계.) 기기 셸 호출이 끝나면 백그라운드 작업도 끝나므로 긴 작업은 `timeout 165`로 나눠 반복합니다.
- Ch 12 02절(pgvector): 작업 VM에 Docker가 없어 conda-forge PostgreSQL 17.4 + pgvector 0.8.1을 `$ROOT/.cache/vm/pgenv`(데이터 `.cache/vm/pgdata`)에 두고, 교재와 같은 접속 정보(`postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab`)로 띄웁니다. `run_section.sh`는 절 실행 직전에 `<챕터>/qa/upgrade/pre_exec.sh`가 있으면 source 하고, Ch 12에는 서버를 켜는 스크립트가 들어 있습니다. 기기 셸은 호출이 끝나면 서버도 꺼지므로 절 실행마다 다시 켜집니다. 교재 본문은 학생 기준(Docker)을 그대로 쓰고, 작업 환경 차이는 진단 파일에 적습니다. (새 컴퓨터에서 `pgenv`·`pgdata` 다시 만들기: `docs/NEW-MACHINE-SETUP.md` 6단계.)
- `.cache/vm` 환경에서는 `run_section.sh`가 `UV_NO_SYNC=1`을 줍니다(마운트 폴더는 삭제가 막혀 uv sync가 실패). 의존성을 새로 넣어야 하면 `uv pip install --python "$HOME/mnt/한국경제신문/.cache/vm/venv-<챕터>/bin/python" <패키지>`로 직접 넣고 진단에 적습니다. 기기 VM이 다시 만들어지면 `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/libs`·`/tmp/pw`를 `textbook/_notebook/mermaid/README.md`대로 다시 설치합니다. 화면 검사용 playwright(`/tmp/pw`·`/tmp/pw-browsers`)는 `docs/NEW-MACHINE-SETUP.md` 5단계대로 설치합니다.

## 먼저 읽을 것 (순서대로)
1. `textbook/_notebook/upgrade/PLAYBOOK.md` — 실행 절차서. 이 순서를 그대로 따릅니다.
2. `textbook/QUALITY-UPGRADE.md` — 정본 규격.
3. 기준 사례: Ch22 `textbook/part6/ch22-middleware/`(`qa/upgrade/author_upgrade.py`, `_src/`, `figures/`, `qa/upgrade/NN-diagnosis.md`)와 같은 Part에서 이미 끝난 절의 `qa/upgrade/author_NN.py`·`_src`.
4. **이어짐(HARD)**: 앞 내용 읽기 — **`textbook/qa/upgrade-course-summary.md`(과정 요약 핵심)는 모든 작업자가 읽습니다.** `runs/`·계약 파일을 읽거나 쓰는 절, 실습 절, 챕터 마감은 **`textbook/qa/upgrade-contracts.md`**도 읽습니다. 전체 마감 담당만 **`textbook/qa/upgrade-final-checklist.md`**를 읽습니다. Part가 끝나면 오케스트레이터가 세 파일을 함께 갱신합니다. 이어서 같은 Part 안 앞 챕터의 `chapter-summary.md` + 바로 앞 챕터 요약(다른 Part여도), 이 챕터 안에서는 `qa/upgrade/handoff.md`와 앞 절 완료본(`_src`, 특히 「정리와 다음 절」)을 읽습니다. 끝난 Part의 챕터 요약은 세부가 필요할 때만 찾아봅니다(PLAYBOOK §6). 앞에서 쓴 예제 데이터·이름·비유·용어를 이어 쓰고, 「앞에서 배운 내용」 블록은 **개선된 앞 절 내용**을 기준으로 씁니다. 앞에서 가르치지 않은 개념·문법을 전제로 쓰지 않습니다.
5. 대상 절의 기존 `_src`, 노트북, figures, 챕터 `집필점검표.md`, `chapter.json`(없으면 `_build.py`), lab `pyproject.toml`.

## 완료 기준
- `bash textbook/_notebook/upgrade/run_section.sh <챕터> NN` → 새 커널 PASS, verify PASS(chapter.json 챕터), 게이트 G1~G7 모두 0.
- Mermaid 3~5장(PNG 직접 확인), 삽화 1장 생성·검수(1회 재생성까지, 안 되면 prompt만·「삽화 대기」).
- `qa/upgrade/NN-figures.md`, `qa/upgrade/NN-diagnosis.md`, `qa/upgrade/before/` 원본, `pack.py` review-pack, 챕터 `집필점검표.md` 해당 행.
- 챕터 첫 절이면 맨 먼저 `upgrade_gates.py <챕터> --label before`(이미 있으면 덮어쓰지 않음).

## 보고 (12줄 이내)
결과(완료/삽화 대기/막힘) · 게이트 전→후 · 코드 셀·모델 호출 수 · Mermaid 장수·삽화 job id·크레딧 · 공용 도구 변경 · 앞 절·앞 챕터와 이어지게 바꾼 점 · 검토자가 볼 곳 3줄 이내
