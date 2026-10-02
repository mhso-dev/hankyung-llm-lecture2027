# Ch 3 Git & GitHub 협업 실습

이 챕터의 모든 Git 저장소는 노트북이 만든 임시 폴더에 있습니다. 실제 GitHub 계정에 로그인하거나 실제 원격 저장소에 게시하지 않습니다. 02절은 로컬 bare 저장소를 원격처럼 사용해 브랜치 게시·변경 비교·리뷰 반영·병합을 연습합니다. GitHub의 Pull Request 화면과 승인 기능을 직접 생성하는 실습은 아닙니다.

`labs/part1/ch03-git-github` 폴더에서 다음 명령을 실행합니다.

```text
uv sync --locked
uv run python --version
uv run python -c "from importlib.metadata import version; print(version('git-filter-repo'))"
```

Python 3.12와 `git-filter-repo` 2.47.0을 확인한 뒤 VS Code에서 이 폴더의 `.venv` 커널을 선택합니다. Git은 2.28 이상이 필요합니다. 교재 출력은 Git 2.34.1로 만들었고, 05절 이력 정리 도구 설명서는 Git 2.36.0 이상을 요구 사항으로 적어 둡니다. 노트북은 각각 독립적이므로 어느 절부터 시작해도 됩니다. 다만 개념은 01절부터 05절까지 순서대로 이어지고, 06절은 앞 절의 명령을 함께 쓰는 실습입니다. 03~06 노트북은 앞 절에서 배운 함수(`run_git()`·`print_report()`)를 `notebooks/git_tools.py`에서 가져오므로, 이 파일을 노트북과 같은 폴더에 그대로 둡니다.

05절의 `DEMO-ONLY-NOT-A-REAL-SECRET`은 실습 전용 더미 문자열입니다. 실제 키를 노트북, 명령 기록, 채팅에 입력하지 않습니다. 실제 자격 증명이 노출되었다면 먼저 발급 서비스에서 폐기하거나 교체하고, 저장소 관리자와 이력 정리 범위 및 협업자의 재복제 절차를 조율해야 합니다.

HTML 교재에서는 코드를 읽고 복사할 수 있지만 실행할 수 없습니다. 노트북 내려받기 버튼으로 `.ipynb` 파일을 받아 첫 셀부터 실행합니다.
