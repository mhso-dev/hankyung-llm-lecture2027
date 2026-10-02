# Ch 1 개발 환경 — 공식 문서 조사 노트

조사일: 2026-09-09 (KST). 아래 내용은 교재의 설치 안내와 검증 셀을 작성하기 위한 근거이며, 설치 화면이나 제품 버전은 배포 시점에 다시 확인한다.

## 1. uv와 Python 3.12

- **기준 선택**: uv의 현재 지원 정책(2026-03-19)은 CPython 3.12를 Tier 1으로 분류합니다. 이 과정에서는 프로젝트 단위로 Python 3.12를 고정하고, 전역 `pip install` 대신 프로젝트의 `.venv`를 사용합니다.  
  출처: <https://docs.astral.sh/uv/reference/policies/python/>
- **uv 설치**: 공식 독립 설치기는 macOS/Linux에서 `curl -LsSf https://astral.sh/uv/install.sh | sh`, Windows PowerShell에서 `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`를 제시합니다. macOS에는 `brew install uv`, Windows에는 `winget install --id=astral-sh.uv -e`도 공식 설치 경로입니다. 내려받은 스크립트는 실행 전에 `less`/`more`로 확인할 수 있다고 안내합니다.  
  출처: <https://docs.astral.sh/uv/getting-started/installation/>
- **프로젝트 최소 흐름**: `uv init <프로젝트명>`으로 `pyproject.toml`, `.python-version`, `.gitignore` 등을 만들고, `uv python install 3.12`와 `uv python pin 3.12`로 관리 Python과 프로젝트 기본 버전을 맞춥니다. 누락된 Python은 uv가 필요할 때 내려받을 수 있으나, 실습에서는 명시 설치와 고정이 결과를 재현하기 쉽습니다.  
  출처: <https://docs.astral.sh/uv/guides/install-python/>, <https://docs.astral.sh/uv/guides/projects/>
- **잠금 파일의 역할**: `pyproject.toml`은 허용할 의존성 범위를, `uv.lock`은 실제로 선택된 정확한 버전을 기록합니다. `uv run`·`uv sync`·`uv lock`은 프로젝트 환경과 잠금 파일을 만들거나 갱신하며, `uv.lock`은 Git에 포함하고 직접 편집하지 않습니다. `uv run`은 실행 전에 잠금 파일과 환경이 최신인지 확인합니다.  
  출처: <https://docs.astral.sh/uv/guides/projects/>, <https://docs.astral.sh/uv/concepts/projects/layout/>
- **교재용 확인 명령**: `uv --version` → `uv python list 3.12` → `uv run python --version`. 마지막 명령의 출력이 `Python 3.12.x`인지 확인합니다. `uv python list`는 설치·사용 가능한 버전을 표시합니다.  
  출처: <https://docs.astral.sh/uv/guides/install-python/>

## 2. VS Code: 인터프리터, 디버거, 노트북

- **필수 확장**: Python 확장은 Python 환경을 찾고 실행·언어 기능에 연결합니다. Python Debugger 확장은 Python 확장과 함께 설치되며 `debugpy` 기반 디버깅을 제공합니다. `.ipynb` 실행에는 Jupyter 확장을 설치합니다.  
  출처: <https://code.visualstudio.com/docs/python/environments>, <https://code.visualstudio.com/docs/python/debugging>, <https://code.visualstudio.com/docs/languages/python>
- **인터프리터 선택**: 폴더를 연 뒤 상태 표시줄의 Python 버전을 누르거나 `Python: Select Interpreter`를 실행해 해당 프로젝트의 `.venv`를 고릅니다. 선택한 환경은 실행, 디버깅, IntelliSense에 사용됩니다. 환경이 보이지 않으면 `Python Environments: Refresh All Environment Managers`를 실행합니다. 기본 탐색 위치는 워크스페이스 안의 `./**/.venv`입니다.  
  출처: <https://code.visualstudio.com/docs/python/environments>
- **디버그의 최소 경로**: 편집기 실행 단추의 메뉴에서 `Python Debugger: Debug Python File`을 선택하거나 F5를 누릅니다. 일반적인 경우 디버거는 선택한 워크스페이스 인터프리터를 사용합니다. 다른 인터프리터가 꼭 필요할 때만 `.vscode/launch.json`의 `python` 속성을 설정합니다.  
  출처: <https://code.visualstudio.com/docs/python/debugging>
- **노트북 커널은 별도 확인**: 노트북 오른쪽 위 `Select Kernel` 또는 `Notebook: Select Notebook Kernel`에서 `.venv`의 Python 환경을 선택합니다. 현재 VS Code 문서는 노트북 커널 탐색이 Python Environments API가 아니라 이전 Python 확장 API를 사용한다고 명시합니다. 따라서 상태 표시줄의 인터프리터와 노트북 커널이 다를 수 있으므로, 첫 노트북에서 둘 다 확인하도록 안내합니다.  
  출처: <https://code.visualstudio.com/docs/datascience/jupyter-kernel-management>, <https://code.visualstudio.com/docs/python/environments>

## 3. Git 설치와 상태 확인

- **설치 경로**: macOS는 우선 `git --version`을 실행해 Xcode Command Line Tools 설치 안내를 받거나 공식 macOS 설치본을 사용할 수 있습니다. Windows는 Git for Windows의 공식 다운로드 경로를, Linux는 배포판 패키지 관리자의 `apt install git-all` 또는 `dnf install git-all` 예를 제공합니다.  
  출처: <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>
- **첫 검증**: `git --version`으로 실행 파일이 PATH에 있는지 확인합니다. 프로젝트 폴더에서는 `git status`를 실행합니다. 이 명령은 HEAD와 인덱스의 차이, 작업 디렉터리와 인덱스의 차이, 아직 추적하지 않은 파일을 보여 줍니다. 따라서 파일을 만든 직후 변경 내용을 확인하는 기본 명령으로 적합합니다.  
  출처: <https://git-scm.com/docs/git-status>

## 4. Docker Desktop: OS별 조건, 시작과 확인

- **공통 교재 원칙**: Docker 명령줄 도구가 설치되었다는 사실과 Docker Engine이 실행 중이라는 사실은 구분합니다. Docker Desktop을 먼저 시작한 뒤 `docker desktop status`로 상태를 확인합니다. 최신 Docker Desktop CLI 문서는 `docker desktop start`, `status`, `stop`, `restart`를 제공한다고 설명합니다. 이 하위 명령이 로컬 설치본에 없다면 앱 메뉴/시작 메뉴에서 Docker Desktop을 열고, `docker version`으로 Client와 Server 정보를 확인합니다.  
  출처: <https://docs.docker.com/desktop/features/desktop-cli/>, <https://docs.docker.com/reference/cli/docker/desktop/start/>
- **Windows (Linux 컨테이너 기본 경로)**: WSL 2 백엔드는 기본 선택이며, 최소 WSL 2.1.5, 지원 중인 Windows 10 22H2(빌드 19045) 또는 Windows 11 23H2(빌드 22631) 이상, 64비트 SLAT CPU, 8 GB RAM, BIOS/UEFI 가상화, WSL 2 기능이 필요합니다. Windows Server는 Docker Desktop 지원 대상이 아닙니다. Windows Home/Education에서는 Windows 컨테이너를 실행할 수 없고 Linux 컨테이너만 가능합니다. 설치 뒤 Docker Desktop은 자동 시작하지 않으므로 시작 메뉴에서 열어야 합니다.  
  출처: <https://docs.docker.com/desktop/setup/install/windows-install/>
- **macOS**: Apple silicon/Intel별 설치본을 고르고, 지원되는 macOS(현재와 직전 두 주요 버전) 및 최소 4 GB RAM이 필요합니다. Apple silicon에서 Darwin/AMD64 선택 도구에는 Rosetta 2가 필요할 수 있습니다. `Docker.dmg`를 열어 `Docker.app`을 Applications에 넣고 앱을 실행합니다.  
  출처: <https://docs.docker.com/desktop/setup/install/mac-install/>
- **Linux**: Desktop 지원 패키지는 Ubuntu, Debian, RHEL, Fedora의 amd64/x86_64에 제공됩니다. Arch 계열 패키지는 실험적입니다. 64비트 CPU/커널 가상화, KVM, QEMU 5.2 이상, systemd, 지원 데스크톱 환경, 최소 4 GB RAM이 필요합니다. Docker Desktop for Linux는 VM에서 동작하므로 중첩 가상화 환경은 지원하지 않습니다. 기존 Docker Engine과 Desktop을 함께 실행하면 포트 충돌이 날 수 있습니다.  
  출처: <https://docs.docker.com/desktop/setup/install/linux/>
- **교재에서 분리해 안내할 제한**: 이 장에서는 Linux 컨테이너 실습만 공통 경로로 잡습니다. Windows 컨테이너, Windows Server, 중첩 가상화 환경은 사전 지원을 약속하지 않습니다. Docker Desktop 이용 조건·조직별 구독은 수강생과 교육기관의 사용 조건에 따라 달라질 수 있으므로, 실습 본문에서 단정하지 않고 Docker의 최신 약관 페이지를 확인하도록 연결합니다.  
  출처: <https://docs.docker.com/desktop/setup/install/windows-install/>, <https://docs.docker.com/desktop/setup/install/linux/>

## 집필 시 버전·표현 주의

- uv 설치 문서는 2026-09-08, uv Python 지원 정책은 2026-03-19 기준입니다. Python 3.12는 해당 정책에서 Tier 1이지만, 고정할 **3.12.x 패치 번호**는 실습을 실행한 날의 `uv python list 3.12` 결과로 결정합니다.
- VS Code의 환경 탐색 및 Python Environments 확장 UI는 변하는 영역입니다. 고정된 메뉴 위치만 전제하지 말고 명령 팔레트 명령도 함께 적습니다.
- Docker 요구 사항은 Docker Desktop 배포판과 OS 지원 수명에 따라 바뀝니다. 특히 Windows 빌드·WSL 최소 버전, macOS 지원 범위는 배포 직전에 공식 설치 페이지를 다시 확인합니다.

## 5. Python 3.12 첫 코드와 현재 폴더

- **튜토리얼의 위치**: Python 3.12 공식 튜토리얼은 언어의 기본 개념과 기능을 단계적으로 소개하며, 인터프리터를 곁에 두고 예제를 실행하는 학습 방식을 권합니다. 이 장에서는 언어 문법을 모두 설명하지 않고, 이후 실습에서 필요한 실행·파일·오류 확인의 출발점으로 연결합니다. 조사일 현재 고정 문서는 Python 3.12.14이며 2026-09-07 UTC에 갱신되었습니다.  
  출처: <https://docs.python.org/3.12/tutorial/index.html>
- **경로는 `pathlib.Path`로 다루기**: `pathlib`는 운영체제에 맞는 파일 시스템 경로 객체를 제공합니다. 처음 사용하는 경우 문서는 `Path`를 우선 권합니다. 예를 들어 `Path('.')`는 현재 폴더를, `Path('data') / 'input.txt'`는 운영체제의 구분자에 맞춰 만든 하위 경로를 나타냅니다. 문자열을 `"/"`로 직접 이어 붙이지 않는 예제로 사용합니다.  
  출처: <https://docs.python.org/3.12/library/pathlib.html>
- **`venv`와 uv의 관계**: 표준 `venv`는 독립 패키지 집합을 담는 가벼운 가상 환경을 만들며, 관례상 프로젝트 안의 `.venv`를 사용합니다. 환경 폴더는 Git에 올리지 않고 삭제·재생성 가능한 결과물로 취급합니다. Python 3.12에서는 `setuptools`가 더 이상 venv의 핵심 의존성이 아닙니다. uv 프로젝트도 기본적으로 프로젝트 옆 `.venv`를 관리하므로, 이 장에서는 둘을 섞어 만들지 않고 uv 흐름만 사용합니다.  
  출처: <https://docs.python.org/3.12/library/venv.html>, <https://docs.astral.sh/uv/guides/projects/>
- **환경 활성화 표기는 OS별로 다름**: 표준 문서의 활성화 명령은 zsh/bash에서 `source <venv>/bin/activate`, Windows PowerShell에서 `<venv>\\Scripts\\Activate.ps1`입니다. 그러나 활성화는 필수가 아니며, 환경의 Python 실행 파일을 직접 지정해도 됩니다. uv 실습에서는 `uv run`이 잠금된 프로젝트 환경에서 명령을 실행하므로 활성화를 기본 단계로 요구하지 않는 편이 일관됩니다.  
  출처: <https://docs.python.org/3.12/library/venv.html>, <https://docs.astral.sh/uv/guides/projects/>
- **Python의 가장 작은 디버거 예시**: 표준 `pdb`는 중단점, 한 줄씩 실행, 호출 스택·변수 검사, 예외 뒤 분석을 지원합니다. 코드에 `breakpoint()`를 넣거나 `python -m pdb 파일명.py`로 시작할 수 있고, 중단 뒤에는 `p 변수명`, `next`, `step`, `continue`를 사용합니다. VS Code 디버거의 중단점·변수 보기와 연결해 설명하되, 둘을 동시에 실행하는 실습은 만들지 않습니다.  
  출처: <https://docs.python.org/3.12/library/pdb.html>
- **현재 폴더(CWD) 확인·이동**: macOS/Linux의 zsh에서는 `pwd`가 현재 작업 폴더의 절대 경로를 출력하고, `cd <경로>`로 폴더를 옮깁니다. PowerShell에서는 `Get-Location`이 현재 작업 위치를 반환하며 `Set-Location <경로>` 또는 별칭 `cd <경로>`로 이동합니다. Windows에서는 파일 시스템 이외의 PowerShell 공급자 위치도 있을 수 있으므로, 교재의 경로 예시는 보통 파일 시스템 드라이브(`C:\\...`)에서 실행하게 적습니다.  
  출처: <https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html>, <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-location?view=powershell-7.6>, <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.5>

## 설치와 터미널 추가 확인

2026-09-09 공식 https://code.visualstudio.com/docs/setup/setup-overview 경로는 https://code.visualstudio.com/docs/getstarted/overview 로 이동함을 본문 확인했습니다. 교재는 최종 주소를 사용합니다. 통합 터미널 https://code.visualstudio.com/docs/terminal/basics 도 본문 확인했습니다. 설치/열기/명령 입력 안내에 사용했습니다.
