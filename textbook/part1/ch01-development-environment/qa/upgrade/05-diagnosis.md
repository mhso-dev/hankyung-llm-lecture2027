# 05-Git과-Docker-준비 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/05-tool-readiness.*`).
생성기: `qa/upgrade/author_05.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch01-development-environment 05`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 0 | 0 |
| G3 | 5 | 0 |
| G4 | 0 | 0 |
| G5 | 6 | 0 |
| G6 | 88 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 7 | 14 (준비 1 + 본 경로 13, 심화 셀 없음) |
| 검사한 문장 | 221 | 365 |
| 모델 호출 | 0 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, Linux aarch64 기기 VM, git 2.34.1, docker 없음, 2026-09-16), verify PASS(5절 65셀). 빌드 HTML 1280px·390px에서 가로 넘침 없음(scrollWidth 1280/390, 로컬 puppeteer, `qa/upgrade/_shot05/`).

## 수정 전 주요 문제

- G1·G2는 0이었지만 사다리 L1 밖 문법이 있었음: `try/except subprocess.TimeoutExpired`(L3), f-string 출력, `bool(...)`·`and`를 한 줄에 몰아 쓴 판정, `sys.version_info[:2] == (3, 12)`. 셀마다 `if git_ready:`로 감싼 긴 분기
- G3: 코드 셀 5개에 첫 줄 주석 없음
- G5: 제목 셀·「오늘 볼 그림」 없음. 결과 읽기 셀 없이 다음 소제목으로 넘어감(출력 값 인용 없음)
- G6: 70자 초과 문장 다수(도식 색 설명 한 문장, 여섯 항목 나열, A/B 트랙 조건), 코드 이름·영문 용어+조사로 시작하는 문장(「`git status`는」, 「Docker는」 등), 5문장 넘는 단락
- G7: Mermaid 0장, 삽화 0장, 설계표 없음. Excalidraw 도식 `05-tool-readiness.svg`는 색 범례를 한 문장으로 설명
- 내용: 정본 출력이 도구가 모두 있는 검증 환경(2026-09-09, Docker 서버 29.4.1)의 결과라 이번 작업 환경에서 재현 불가. 저장소 실습이 `??` 한 번에서 끝나 「Git이 변경을 기록한다」는 역할이 실행으로 보이지 않음. 「앞에서 배운 내용」이 개선 전 02~04절 기준(4절 `hello.py`의 `price = 3000` 한 줄만 저장). 설치 조건(WSL 2·KVM 등)의 확인일이 2026-09-09

## 바꾼 것

- 노트북(experiment, 학습 질문 「설치와 실행 준비 구분」·임시 Git 저장소·`hello.py`·여섯 가지 준비 상태 유지): 제목 셀(API 키 불필요, 호출 0번·비용 없음·1분 이내, Docker 없어도 끝까지 실행) → 오늘 볼 그림(05-1) → 준비(import 6개) → 명령 찾기 `shutil.which()`(git·uv `True`, docker `False`, git 없으면 assert) → 버전 질문(git 종료 코드 `0`, `git version 2.34.1`, uv `0`) → `git init`(종료 코드 `0`, `.git` `True`, 상태 `0`줄) → 4절 `hello.py` 네 줄 저장(`?? hello.py`) → `git add`(`A  hello.py`) → `-c user.name/user.email`로 커밋(종료 코드 `0`, 상태 `0`줄) → **실험** 수량 3(`M hello.py`) → `git diff`를 for·if로 걸러 `-count = 2`·`+count = 3` → **값 바꿔 보기** 수량 2로 되돌림(상태 `0`줄) → Docker 클라이언트 if/else(`명령을 찾지 못함`, `False`) → Docker 서버 if/else(`확인하지 않음`, `False`) → 여섯 가지 준비 상태 → cleanup `False` → 정리
- 사다리: 기본 경로는 대입·print(쉼표 인자)·`==`·`!=`·`is not None`·`and`·`or`·`not`·for·여러 줄 if/else·`len()`·`assert`, 준비 셀의 표준 라이브러리 import(환경 챕터 예외(`QUALITY-UPGRADE.md` §2 끝)로 표준 라이브러리 import와 그 결과 값의 메서드를 쓰고, import나 점(.)으로 부르는 메서드·속성이 있는 코드 셀에 `upgrade_allow=["stdlib-import"]`를 적음), 글·경로·실행 결과의 메서드(`write_text`·`splitlines`·`strip`·`replace`·`startswith`·`is_dir`·`cleanup`)만 사용. `try/except`·f-string 출력·`timeout` 제거. 스크립트 글 안의 f-string은 4절 `hello.py` 원문이라 유지
- Docker: 이 환경에 docker가 없어 「명령을 찾지 못함」을 실제 출력으로 보여 주고, 설치된 컴퓨터의 클라이언트·서버 출력은 노트북·본문·복습 5번에 「이번에 실행하지 않았습니다」로 적음. 서버 셀의 `timeout=10`+`TimeoutExpired`는 L3라 빼고, 오래 멈추면 셀 실행을 멈추라는 안내로 대신함(실행하지 않음)
- 커밋 해시·날짜는 출력하지 않고 본문·노트북에 그 이유를 적음
- 이어짐: 01절 「예상 → 실행 → 비교」와 값 하나만 바꾸기, 02절 `workspace`·`write_text()`·`cleanup()`·새 터미널에서 명령 응답 확인, 03절 `platform.python_version()`·`sys.prefix != sys.base_prefix`·`shutil.which()`·`subprocess.run(capture_output, text, check)`·`returncode`·`splitlines()`, 04절 `hello.py` 네 줄·`replace("count = 2", "count = 3")`·디버거 출력 고르기 for/if 패턴을 다시 정의하지 않고 이어 씀. A/B 자가진단 4번을 개선된 04절(pdb `n` 뒤에 `total` 생김)에 맞춤
- 본문 10블록 전체를 다시 씀. 리모컨·빠진 플러그 비유, 용어 7개 표(Git·저장소·커밋·GitHub·Docker·클라이언트·데몬), 세 단계 확인, 상태 표시 표(`??`·`A`·`M`·출력 없음), 저장소 작업 4단계 표, 여섯 항목 표(False일 때 할 일), 운영체제별 Docker Desktop 조건 표(2026-09-16 재확인), A/B 트랙 자가진단(`[[미정]]` 표시 유지), 복습 5문항(01~04절 형식)
- 「다음 학습과 이어지는 지점」은 Ch 2로 둠(챕터 끝 실습 절을 붙일 때 고칠 것)
- 그림: Mermaid 4장(05-1 준비 단계, 05-2 상태 변화, 05-3 기록 비교, 05-4 여섯 항목) + 삽화 1장(05-5 리모컨과 빠진 플러그, 1회 생성 채택). 기존 Excalidraw 도식은 본문에서 뺌(원본 `before/figures/`, `figures/`의 옛 파일은 삭제하지 않음)

## 사실 주장 확인

- 실행 출력으로 확인(2026-09-16, 기기 VM, Python 3.12.13, git 2.34.1): 노트북 전체 출력. 기기 셸에서 같은 순서를 Python으로 따로 실행해 `A  hello.py`(두 칸)·` M hello.py`(앞 한 칸)·diff 원문(`diff --git`, `index`, `---`, `+++`, `@@` 줄 포함)을 확인. 전역 Git 설정이 없는 기기 셸에서 `-c` 없이 `git commit` → 종료 코드 128, `Author identity unknown`
- git-status 문서(2.53.0): 짧은 형식 `XY PATH`, X는 index, Y는 work tree, `??` untracked, `A` added, `M` modified
- docker version 문서: Client 구역(CLI)과 Server 구역(Engine), 예 `docker version --format '{{.Server.Version}}'`. 데몬에 연결하지 못할 때의 종료 코드·출력은 문서에 없고 실행하지 않음 → 본문은 「서버가 실행 중이어야 받을 수 있다」와 코드의 판정 기준만 적음
- Docker Desktop 설치 문서(2026-09-16 조회): Windows WSL 2·가상화·Windows 10/11 빌드·RAM 8GB, Mac Apple silicon/Intel 설치본·현재와 이전 두 macOS·RAM 4GB, Linux KVM·QEMU 5.2+·systemd·GNOME/KDE/MATE·RAM 4GB, 큰 조직의 상업적 사용 유료 구독
- 확인 필요: Git이 이름 설정 없이 시스템 사용자 이름·호스트 이름으로 추측해 커밋하는 경우(macOS 등)는 실행하지 않음 → 본문은 「실패할 수 있습니다」로 적음. Windows에서 git 출력 모양, Docker Desktop이 꺼진 상태의 서버 셀 동작은 실행하지 않음

## 검토에서 볼 곳

- Docker 두 셀의 `else`/`if` 아래 줄(실행하지 않은 경로)이 설치된 컴퓨터에서 맞게 동작하는지와, 본문·노트북이 이를 실행한 것처럼 쓰지 않았는지
- 커밋·`git add`·`git diff`를 Ch 1에서 짧게 보여 준 범위가 Ch 3 01절(커밋과 gitignore, 저장소에 이름 적기)과 겹치지 않고 이어지는지
- 05-1·05-4의 빨강(실제로 준비되지 않은 Docker)과 회색(확인하지 않은 서버 단계) 구분이 본문 도식 읽기와 맞는지

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept-with-fixes(중 2·하 5, 공통 C-1 중·C-3 하·C-4 하). 모두 반영했습니다(05-7은 변형 반영).
- C-1(중): 코드 셀 14개 모두 `upgrade_allow=["stdlib-import"]`
- 05-1(중, 사실 오류): 인자 없는 `git diff`는 기록할 목록(index)과 파일을 비교합니다(git-diff 공식 문서 「changes … relative to the index」). 기기 셸 git 2.34.1에서 커밋 뒤 파일을 바꾸고 `git add` 전 7줄, 뒤 0줄, `git diff --cached` 7줄을 확인. [26] 설명·[27] 주석·[28] 결과 읽기·05-3 그림 화살표(「git diff 기록할 목록과 비교(지금은 기록과 같음)」)·본문 결과 해석을 고치고, 주의할 점에 `git add` 뒤 0줄 항목 추가(노트북에는 넣지 않았다고 적음)
- 05-2(중): 노트북 정리의 다음 학습을 「다음 절 6절 실습에서는 1~5절의 확인을 한 점검표로 모아 새 연습 폴더를 점검합니다.」로. 본문 다음 학습의 「새 실습 폴더」도 「새 연습 폴더」
- 05-3(하) `M` 앞 빈칸은 노트북 출력에 없고 기기 셸에서 확인했다고 적음(노트북·본문). 05-4(하) 맨 위 파란 상자 설명. 05-5(하) 「서버 칸이 `False`이면…」과 「앱이 꺼진 상태의 출력은 이번에 실행하지 않았습니다」
- 05-6(하): 「도구 Docker」「도구 Git」 16곳(본문 7·노트북 9)을 영문 조사 시작 없이 다시 씀(예: 「셋째 줄은 Docker를 설치한 컴퓨터에서 `True`로 나올 것입니다.」). 보고서 예문 「Docker를 설치한 컴퓨터에서는…」은 G6 영문 시작에 걸려 어순을 바꿈
- 05-7(하, 변형): 학생 문장은 「공식 배치 기준은 첫 주에 강사가 안내합니다.」로 바꾸고, 확정 시 일괄 치환하도록 `[[미정: Ch 1 A/B 트랙 공식 배치 기준]]`을 HTML 주석으로 남김(AGENTS.md 미정 플레이스홀더 규칙)
- C-3(하) 「경로 기능 `Path`」. C-4(하) 「운영체제별 Docker Desktop 설치 조건은…」, 소제목 「클라이언트와 서버로 나뉘는 Docker」·「파일 상태 표시 읽기」, 복습 2 해설 「처음 보는 파일이라는 뜻입니다.」

재실행: `run_section.sh … 05`(새 커널 PASS, 코드 셀 출력은 수정 전과 글자 단위로 같음) → 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0), `verify.py --chapter` `PASS 6 sections / 84 code cells (max 14 lines)`, `visual.cjs` 7페이지 × 1280·390px 14건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 강사 확인(2차 검토는 보고서 「다음 조치」 4대로 중 항목과 C-4 문장만 대조하면 됨)
- 실습 묶음 `textbook/downloads/ch01-practice.zip` 재생성(C-2, 전체 챕터가 끝난 뒤 일괄)
