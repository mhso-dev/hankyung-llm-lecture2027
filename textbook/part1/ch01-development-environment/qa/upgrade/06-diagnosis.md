# 06-개발환경-실습 — 챕터 끝 실습 절 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md` §7-2, `textbook/_notebook/upgrade/PLAYBOOK.md` §3. 기준 사례: Ch 22 `09-Middleware-실습`.
새 절이라 수정 전 원본(`qa/upgrade/before/`)은 없습니다. 생성기: `qa/upgrade/author_06.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch01-development-environment 06`.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 새 절 | 0 |
| G2 | 새 절 | 0 |
| G3 | 새 절 | 0 |
| G4 | 새 절 | 0 |
| G5 | 새 절 | 0 |
| G6 | 새 절 | 0 |
| G7 | 새 절 | 0 |
| 코드 셀 | 새 절 | 19 (준비 1 + 본 경로 18, 심화 셀 없음) |
| 검사한 문장 | 새 절 | 250 (노트북 설명 셀 + `_src`) |
| 모델 호출 | 새 절 | 0 (API 키 불필요) |

새 커널 실행 PASS(Python 3.12.13, Linux aarch64 기기 VM, git 2.34.1, docker 없음, 2026-09-16), verify PASS(챕터 6절 84셀, 최대 14줄). 빌드 HTML 1280px·390px에서 가로 넘침 없음(scrollWidth 1280/390, 로컬 puppeteer, `qa/upgrade/_shot06/`). 05절 게이트도 `--no-exec` 재확인 0건.

## 주제와 구성

- 주제: 「새 연습 폴더 점검하기」. 1~5절에서 따로 배운 확인 여섯 가지를 점검표 한 장으로 모으고, 작업 폴더 하나만 바꿔 어느 칸이 달라지는지 봅니다.
- 노트북 순서(PLAYBOOK §3): 준비(import 6개) → 주제 소개 → 재료 만들기(임시 폴더에 `practice/data/message.txt`, `hello.py` 네 줄, `git init`·`git add`·`-c` 이름으로 커밋) → 기록 장치(점검표 칸 이름 목록 `check_names` 6칸, 칸마다 배운 절을 주석으로) → 실행 1(칸마다 예상 → 실행 → 결과 읽기, `run_1`로 모아 출력) → 실행 2(`base_folder = workspace` 하나만 바꿔 예상 → 실행, `run_2`) → 칸별 비교 → 실패 이유 읽기(`stderr`에 알아볼 글이 있는지 `in`) → cleanup → 정리 3줄
- 실행 1(작업 폴더 practice): Python 3.12 `True`, 가상환경 `True`, message.txt `True`, hello.py 종료 코드 `0`·`총액: 6000원`·`True`, git 종료 코드 `0`·상태 `0`줄·`True`, Docker `명령을 찾지 못함`·`False` → True 칸 수 `5`
- 실행 2(작업 폴더 한 칸 위 임시 폴더): Python `True`, 가상환경 `True`, message.txt `False`, hello.py 종료 코드 `2`·`False`, git 종료 코드 `128`·`False`, Docker `False` → True 칸 수 `2`, 달라진 칸 수 `3`. 오류 메시지에 `can't open file`·`not a git repository` 있음 `True`
- 사다리: L1(대입·print·`==`·`!=`·`and`·`is not None`·for·여러 줄 if/else·목록과 인덱싱·`len()`·`assert`)과, 환경 챕터 예외(`QUALITY-UPGRADE.md` §2 끝)로 표준 라이브러리 import와 그 결과 값의 메서드를 쓰고, import나 점(.)으로 부르는 메서드·속성이 있는 코드 셀에 `upgrade_allow=["stdlib-import"]`를 적음. 함수 정의는 01~05절에 없어 쓰지 않음. 그래서 실행 2는 같은 확인을 셀 네 개로 다시 적음(변수 이름 끝에 `_2`)

## 앞 절에서 가져온 이름

- 01절: 목록에 문자열 담기(`course_map` 모양), for와 번호 늘리기(`number = number + 1` → `index = index + 1`), 실행 전 예상, `==` 비교
- 02절: `tempfile.TemporaryDirectory()`·`workspace`·`project = workspace / "practice"`·`data/message.txt`·`"안녕, 터미널!"`·`relative_path`·`base_folder`·Before의 한 칸 위 기준 폴더·`mkdir()`·`write_text()`·`is_dir()`/`is_file()`·`cleanup()`
- 03절: `platform.python_version()`·`startswith("3.12")`·`sys.prefix != sys.base_prefix`·`subprocess.run(capture_output, text, check)`·`returncode`(0이 아니면 실패)·`stderr`·`splitlines()`
- 04절: `hello.py` 네 줄(`hello_source`)·`sys.executable`·`strip()`·예상 출력 `"총액: 6000원"`·연산자 `in`
- 05절: `shutil.which()`·`git_path`·`git init`/`git add`/`git status --short`·`status_command`·`cwd`·`-c user.name=Ch1 Student`/`user.email=student@example.com`·`--quiet`·Docker if/else(`명령을 찾지 못함`)·`docker_path`

새 문법·새 API 없음. 4절과 다른 점은 hello.py를 파일 전체 경로가 아니라 파일 이름 `"hello.py"`와 `cwd=base_folder`로 실행한 것 하나이고(인자 `cwd`는 5절), 본문 핵심 개념에 그 차이를 적음.

## 사실 주장 확인

- 실행 출력으로 확인(2026-09-16, 기기 VM): 노트북 전체 출력. 기기 셸에서 저장소가 아닌 임시 폴더의 `git status --short` → 종료 코드 128, 첫 줄 `fatal: not a git repository (or any parent up to mount point /)`, 둘째 줄 `Stopping at filesystem boundary ...`. 파일이 없는 폴더에서 `python3 hello.py` → 종료 코드 2, `can't open file ... [Errno 2] No such file or directory`
- git 오류의 괄호 안 문구와 줄 수가 환경마다 달라서 노트북은 전체나 마지막 줄을 출력하지 않고 `"not a git repository" in git_error`만 확인. 본문 주의 항목에 적음
- 실행하지 않은 것: Docker가 설치된 컴퓨터의 Docker 칸(`else` 아래 줄 두 곳, 실행 2의 `docker_command`는 실행 1의 `else`에서 만든 목록을 씀), Windows에서의 오류 문구, 저장소 안에 들어 있는 임시 폴더에서의 Git 칸

## 그림

- Mermaid 3장: 06-1 조립도(flowchart LR, 551px), 06-2 실행 1 순서(sequenceDiagram, 732px), 06-3 두 실행 비교(flowchart TB 두 칸, 769px). PNG 직접 확인
- 처음 06-1을 TB로 그려 원본 폭 1149px → LR로 바꿔 551px
- 삽화 1장: 06-4 두 방과 가방(02-5 서랍·편지 비유를 이어 씀). nano_banana_pro 16:9 2k, 1회 생성 채택, 2크레딧, job a977e4cf-873c-4cc0-9fbb-a15912e87f5b

## 검토에서 볼 곳

- 실행 2 Docker 셀의 `else` 아래 줄이 실행 1 `else`에서 만든 `docker_command`를 씀. Docker가 있는 컴퓨터에서는 두 실행 모두 `else`로 가므로 동작하지만, 실행하지 않은 경로임
- 06-3에서 Docker 「명령을 찾지 못함」을 두 실행 모두 빨강으로 둔 것(05-1·05-4와 같은 대상·같은 색)과 「색이 바뀐 것은 왼쪽 상자 하나뿐」 설명이 맞는지
- 비유(방 = 작업 폴더, 가방 속 필통 = 커널의 Python·가상환경)가 Docker 칸(컴퓨터에 딸린 것)까지 설명하지 않는 점. 본문은 필통을 Python과 가상환경에만 대응시킴

## 바꾼 다른 파일

- `chapter.json` sections 끝에 `06-개발환경-실습`(experiment) 추가
- `_src/05-Git과-Docker-준비.html` 「다음 학습과 이어지는 지점」을 6절 실습으로 고침(`run_section.sh ... 05 --no-exec` 게이트 0건). 05 노트북 마지막 셀의 「다음 장 Ch 2에서는」 문장은 검토 1차(05-2)에서 6절 실습으로 고침

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1.md`

- 판정 accept-with-fixes(중 2·하 5, 공통 C-1 중·C-4 하). 모두 반영했습니다.
- C-1(중): 코드 셀 19개 중 15개 `upgrade_allow=["stdlib-import"]`(목록·반복·비교만 하는 네 셀은 표시 없음)
- 06-1(중): 임시 폴더 안의 `practice`는 「연습 폴더」로 통일(제목 「개발환경 실습: 새 연습 폴더 점검하기」, `chapter.json`, 노트북 [0]·[5]·[9]·[13], 커밋 메시지, 본문, 06-3 캡션, 복습 3). 「실습 폴더」는 `labs/part1/ch01-development-environment`만 가리킴. 정리 셀 [41]은 「교재 실습 폴더(`labs/part1/ch01-development-environment`)의 `hello.py`는 이 임시 폴더 밖에…」로 고쳐 바로 앞 문장과의 모순을 없앰
- 06-2(중): [16] 「5절의 여섯 가지 준비 상태에서 uv 응답과 Docker 서버 칸을 빼고, 파일과 hello.py 칸을 넣었습니다. Git 칸은 버전 응답 대신 상태 출력이 0줄인지 봅니다.」
- 06-3(하) 06-1 초록 상자 다섯 개 설명(노트북 [1]·본문·캡션). 06-4(하) 06-2에 「도식 읽기」 표시와 첫 노란 메모 설명(본문·캡션). 06-5(하) 주의 4번째 항목 비교 대상. 06-6(하) 「다음 장부터 실습 폴더를 새로 열면 이 점검표 순서로 먼저 확인해 볼 수 있습니다.」(본문 이유·다음 학습·노트북 [5]). 06-7(하) 06-3 왼쪽 상자 라벨 「hello.py·git 종료 코드 0」
- C-4(하): 「도구 Docker」로 시작하던 문장 4곳(본문 1·노트북 3)을 다시 씀

재실행: `run_section.sh … 06`(새 커널 PASS, 코드 셀 출력은 수정 전과 글자 단위로 같음) → 챕터 `upgrade_gates.py --label after --strict` 6/6 PASS(G1~G7 0), `verify.py --chapter` `PASS 6 sections / 84 code cells (max 14 lines)`, `visual.cjs` 7페이지 × 1280·390px 14건 PASS. 리뷰 묶음 `pack.py`로 갱신.

## 남은 것

- 강사 확인(2차 검토는 보고서 「다음 조치」 4대로 중 항목과 C-4 문장만 대조하면 됨)
- 실습 묶음 `textbook/downloads/ch01-practice.zip` 재생성(C-2, 전체 챕터가 끝난 뒤 일괄)
