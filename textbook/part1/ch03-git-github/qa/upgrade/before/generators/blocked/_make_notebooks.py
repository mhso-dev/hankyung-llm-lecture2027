"""Generate the five Ch 3 lesson notebooks from reviewed cell sources."""

from __future__ import annotations

raise SystemExit("옛 생성기 — 품질 개선 뒤 실행 금지. 지금 판은 qa/upgrade/author_*.py")

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def md(source: str, part: str | None = None) -> dict:
    metadata = {} if part is None else {"lesson_part": part}
    return {"cell_type": "markdown", "metadata": metadata, "source": source.splitlines(keepends=True)}


def code(source: str, part: str | None = None) -> dict:
    metadata = {} if part is None else {"lesson_part": part}
    return {
        "cell_type": "code", "execution_count": None, "metadata": metadata,
        "outputs": [], "source": source.splitlines(keepends=True),
    }


def notebook(title: str, cells: list[dict]) -> dict:
    references = {
        "커밋과 .gitignore": "이 절에서는 HEAD가 현재 커밋을 가리킨다는 관계까지만 사용합니다.",
        "GitHub Flow와 PR 리뷰": "이 절에서는 HEAD와 브랜치에 더해 `origin/main`을 마지막으로 확인한 원격 `main`의 위치로 읽습니다.",
        "병합 충돌 해결": "이 절에서는 현재 브랜치의 HEAD와 `origin/main`을 비교해 로컬과 원격의 갈라진 이력을 읽습니다.",
        "revert, reflog, worktree": "이 절에서는 `HEAD~1`을 현재 커밋의 첫 번째 부모 한 단계 전으로 읽습니다.",
        "시크릿 이력 정리와 예방": "이 절에서는 브랜치와 태그처럼 커밋을 가리키는 이름을 묶어 참조(reference)라고 부릅니다.",
    }[title]
    introduction = f"""# {title}

모든 저장소는 임시 폴더에 만들며 실제 GitHub 계정이나 원격 저장소를 변경하지 않습니다.

## 명령을 실행하기 전에 알아둘 Git 상태

Git은 파일을 세 자리에서 봅니다. **작업 폴더(working tree)** 는 지금 편집하는 파일이 있는 자리입니다. **색인(index)** 은 다음 커밋에 넣을 파일 상태를 골라 두는 자리이며, 스테이징 영역(staging area)이라고도 합니다. **커밋(commit)** 은 색인에 고른 상태를 저장소 이력에 기록한 결과입니다. 따라서 `git add app.py`는 파일을 영구 저장하는 명령이 아니라 현재 `app.py`를 색인에 올리는 명령입니다. 이어서 `git commit -m "메시지"`를 실행해야 그 상태가 커밋으로 기록됩니다.

**HEAD** 는 현재 체크아웃한 커밋을 가리킵니다. 보통 HEAD는 `main` 같은 **브랜치(branch)** 이름을 가리키고, 브랜치 이름은 다시 최신 커밋을 가리킵니다. 새 커밋을 만들면 현재 브랜치가 새 커밋으로 이동합니다. {references}

명령은 왼쪽부터 `git` → 하위 명령 → 옵션 → 대상으로 읽습니다. 예를 들어 `git status --short`에서 `status`는 상태를 보고, `--short`는 짧은 형식으로 표시하라는 옵션입니다. 코드의 `git("status", "--short", cwd=repo)`는 터미널에서 같은 명령을 실행하도록 인자를 나눈 Python 표현입니다.
"""
    all_cells = [md(introduction), *cells]
    for number, cell in enumerate(all_cells, 1):
        cell["id"] = f"cell-{number:02d}"
    return {
        "cells": all_cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "lesson_format": "paired",
        },
        "nbformat": 4, "nbformat_minor": 5,
    }


COMMON = '''# 셀이 만든 저장소만 사용하는 임시 작업 폴더를 준비합니다.
import subprocess
import sys
import tempfile
from pathlib import Path
workspace = tempfile.TemporaryDirectory(prefix="git-lesson-")
root = Path(workspace.name)
# cwd는 명령을 실행할 폴더이며 check=True는 명령 실패를 예외로 알립니다.
def git(*args: str, cwd: Path | None = None, check: bool = True) -> str:
    """지정한 임시 저장소에서 Git 명령을 실행합니다."""
    result = subprocess.run(["git", *args], cwd=cwd or root,
                            text=True, capture_output=True, check=check)
    return result.stdout.strip() or result.stderr.strip()
def configure(repo: Path) -> None:
    """실습 저장소에만 작성자 정보를 설정합니다."""
    git("config", "user.name", "Git Learner", cwd=repo)
    git("config", "user.email", "learner@example.invalid", cwd=repo)'''


lessons: dict[str, dict] = {}

lessons["01-커밋과-gitignore"] = notebook("커밋과 .gitignore", [
    md("""## 준비

임시 저장소를 만들고 이 노트북에만 적용되는 작성자 정보를 설정합니다. `git init -b main`에서 `init`은 현재 폴더를 Git 저장소로 만들고, `-b main`은 첫 브랜치 이름을 `main`으로 정합니다. 아직 커밋이 없으므로 브랜치 이름만 준비된 상태입니다.

이 절에서는 `app.py`가 작업 폴더, 색인, 커밋을 차례로 이동하는 모습을 확인합니다. `.env`는 작업 폴더에는 있지만 `.gitignore` 규칙 때문에 색인에 올라가지 않습니다. 두 파일이 같은 폴더에 있어도 Git의 추적 상태는 다를 수 있습니다."""),
    code(COMMON),
    code('''# 저장소를 main 브랜치로 초기화합니다.
repo = root / "orders"
repo.mkdir()
git("init", "-b", "main", cwd=repo)
configure(repo)
print(repo.name, git("branch", "--show-current", cwd=repo))'''),
    md("""## 기본 실행

커밋 메시지 앞의 `feat`, `fix`, `chore`는 이 교재가 변경 목적을 구분하려고 사용한 팀 관례입니다. Git이 요구하는 필수 문법이 아니며 저장소마다 다른 규칙을 사용할 수 있습니다.

무시 규칙을 첫 커밋에, 프로그램을 다음 커밋에 기록합니다. `git add .gitignore`는 그 파일만 색인에 올리고, `git commit -m ...`의 `-m`은 커밋 메시지를 명령줄에서 지정합니다. 다음 `git add app.py`는 새 색인을 구성하므로 두 커밋은 서로 다른 목적을 갖습니다.

실행 뒤 `git status --short --ignored`에서 앞의 `!!`는 무시된 파일, `git log -2 --pretty=%s`의 `-2`는 최근 두 커밋, `%s`는 제목만 출력하라는 뜻입니다. `.env`가 `!!`로 보이고 두 메시지가 역시간순으로 나오면 작업 폴더의 모든 파일이 자동으로 커밋되는 것이 아님을 확인한 것입니다."""),
    code('''(repo / "app.py").write_text('print("주문 2건")\\n', encoding="utf-8")
(repo / ".gitignore").write_text(".env\\n__pycache__/\\n", encoding="utf-8")
(repo / ".env").write_text("APP_MODE=demo\\n", encoding="utf-8")
git("add", ".gitignore", cwd=repo)
git("commit", "-m", "chore: 생성 파일 추적 제외", cwd=repo)
git("add", "app.py", cwd=repo)
git("commit", "-m", "feat: 주문 요약 추가", cwd=repo)
print(git("status", "--short", "--ignored", cwd=repo))
print(git("log", "-2", "--pretty=%s", cwd=repo))'''),
    md("""## 값 하나를 바꿔 비교

출력 숫자만 2에서 3으로 바꾸고 차이를 확인합니다. 이때 변경은 먼저 작업 폴더에만 존재합니다. `git diff -- app.py`는 작업 폴더와 색인의 차이를 보여 주므로 `-` 줄의 2와 `+` 줄의 3을 읽습니다. `git add` 뒤에는 같은 명령의 출력이 사라지고 변경이 색인으로 이동합니다. 마지막 커밋 뒤에는 작업 폴더·색인·HEAD 커밋이 다시 같은 파일 상태를 가리킵니다."""),
    code('''(repo / "app.py").write_text('print("주문 3건")\\n', encoding="utf-8")
print(git("diff", "--", "app.py", cwd=repo))
git("add", "app.py", cwd=repo)
git("commit", "-m", "fix: 주문 건수 수정", cwd=repo)
print(git("log", "--oneline", "-2", cwd=repo))'''),
    md("""## 실패 재현

이미 추적 중인 파일은 나중에 무시 규칙을 추가해도 추적 상태가 유지됩니다. `*.log`에서 별표 `*`는 파일 이름의 임의 문자열과 일치하므로 `debug.log`, `server.log`처럼 `.log`로 끝나는 파일을 무시합니다.""", "before"),
    code('''tracked = repo / "debug.log"
tracked.write_text("first run\\n", encoding="utf-8")
git("add", "debug.log", cwd=repo)
git("commit", "-m", "chore: 디버그 로그 기록", cwd=repo)
with (repo / ".gitignore").open("a", encoding="utf-8") as file:
    file.write("*.log\\n")
tracked.write_text("second run\\n", encoding="utf-8")
print("추적 여부:", git("ls-files", "debug.log", cwd=repo))
print("변경 상태:", git("status", "--short", cwd=repo))''', "before"),
    md("## 수정\n\n색인에서만 파일을 제거하면 작업 폴더의 파일은 남고 이후 변경은 무시됩니다.", "after"),
    code('''git("rm", "--cached", "debug.log", cwd=repo)
git("add", ".gitignore", cwd=repo)
git("commit", "-m", "chore: 로그 파일 추적 제외", cwd=repo)
tracked.write_text("third run\\n", encoding="utf-8")
print("파일 존재:", tracked.exists())
print("추적 결과:", git("ls-files", "debug.log", cwd=repo) or "없음")
print("무시 규칙:", git("check-ignore", "-v", "debug.log", cwd=repo))
assert tracked.exists() and not git("ls-files", "debug.log", cwd=repo)''', "after"),
])

lessons["02-GitHub-Flow와-PR-리뷰"] = notebook("GitHub Flow와 PR 리뷰", [
    md("""## 준비

로컬 bare 저장소를 원격 저장소처럼 사용합니다. **원격(remote)** 은 네트워크 자체가 아니라 다른 Git 저장소의 위치에 붙인 이름입니다. `git clone 원격경로 author`는 원격의 이력과 브랜치를 받아 `author` 작업 폴더를 만들고, 그 원격을 관례적인 이름인 `origin`으로 등록합니다. **bare 저장소**에는 편집용 작업 폴더가 없어서 중앙 공유 저장소 역할에 알맞습니다.

`git push -u origin main`은 현재 `main` 커밋을 원격 `main`에 보내며, `-u`는 이후 `git push`가 사용할 추적 관계를 기록합니다. push는 작업 폴더의 미커밋 파일을 보내지 않고 커밋과 참조를 전송합니다."""),
    code(COMMON),
    code('''# bare 저장소는 원격 역할만 담당합니다.
remote = root / "team.git"
git("init", "--bare", "--initial-branch=main", remote.as_posix())
author = root / "author"
git("clone", remote.as_posix(), author.as_posix())
configure(author)
(author / "README.md").write_text("# 주문 서비스\\n", encoding="utf-8")
template = author / ".github" / "pull_request_template.md"
template.parent.mkdir()
template.write_text("## 변경\\n- 변경 이유\\n\\n## 확인\\n- [ ] 로컬 실행\\n", encoding="utf-8")
git("add", "README.md", template.relative_to(author).as_posix(), cwd=author)
git("commit", "-m", "docs: 저장소와 PR 템플릿 시작", cwd=author)
git("push", "-u", "origin", "main", cwd=author)
print(git("remote", "-v", cwd=author).splitlines()[0])'''),
    md("""## 기본 실행

기능 브랜치를 만들고 커밋한 뒤 원격에 게시합니다. `git switch -c feature/order-summary`에서 `switch`는 체크아웃할 브랜치를 바꾸고 `-c`는 현재 커밋에서 새 브랜치를 만듭니다. 이 직후 `main`과 기능 브랜치는 같은 커밋을 가리키지만, 기능 커밋을 만들면 기능 브랜치만 앞으로 이동합니다.

`git branch -vv` 출력에서 별표는 현재 브랜치, 대괄호의 `origin/feature/order-summary`는 추적하는 원격 브랜치입니다. `git diff --stat origin/main...HEAD`의 점 세 개는 두 참조의 공통 조상부터 HEAD까지 기능 브랜치가 추가한 변경을 요약합니다. **풀 리퀘스트(Pull Request, PR)** 는 이 차이와 변경 이유를 사람에게 검토해 달라고 요청하는 GitHub의 협업 단위입니다."""),
    code('''git("switch", "-c", "feature/order-summary", cwd=author)
(author / "summary.py").write_text(
    """def summarize(count: int) -> str:
    return f'주문 {count}건'
""", encoding="utf-8"
)
git("add", "summary.py", cwd=author)
git("commit", "-m", "feat: 주문 요약 함수 추가", cwd=author)
git("push", "-u", "origin", "feature/order-summary", cwd=author)
print(git("branch", "-vv", cwd=author))'''),
    md("""## PR 자료와 변경 범위

기본 브랜치에 준비된 템플릿을 읽고 기능 코드 차이만 확인합니다. `--stat`은 실제 코드 대신 바뀐 파일과 줄 수를 요약합니다. 리뷰할 때는 요약으로 범위를 확인한 뒤 실제 diff도 읽어야 합니다.

GitHub Flow의 합치기 단계에는 merge, squash merge, rebase merge 같은 선택이 있을 수 있습니다. **fast-forward**는 현재 브랜치 이름을 기존 자손 커밋으로 앞으로 옮기기만 하면 되는 관계입니다. `--no-ff`는 이 단순 이동이 가능해도 부모가 둘인 병합 커밋을 만들라는 옵션입니다. **rebase**는 한 브랜치의 커밋을 다른 기준 위에서 다시 만든다는 뜻이라 커밋 해시가 바뀝니다."""),
    code('''pr_body = template.read_text(encoding="utf-8").replace(
    "- 변경 이유", "- 주문 건수 요약 함수 추가"
).replace("- [ ] 로컬 실행", "- [x] 로컬 실행")
print(git("diff", "--stat", "origin/main...HEAD", cwd=author))
print(pr_body)'''),
    md("## 실패 재현\n\n리뷰어가 빈 문자열 입력에 대한 설명과 처리가 없음을 실제 diff에서 발견합니다.", "before"),
    code('''reviewer = root / "reviewer"
git("clone", remote.as_posix(), reviewer.as_posix())
configure(reviewer)
git("switch", "feature/order-summary", cwd=reviewer)
before = (reviewer / "summary.py").read_text(encoding="utf-8")
print(before)
print("리뷰 의견: count가 빈 문자열이면 주문 건수가 비어 보입니다.")
print("재현:", subprocess.check_output(
    [sys.executable, "-c", "from summary import summarize; print(summarize(''))"],
    cwd=reviewer, text=True,
).strip())''', "before"),
    md("## 수정\n\n작성자가 입력을 정수로 제한하고 리뷰어가 원격 변경을 받아 병합합니다.\n\nCh 2의 07절에서 배운 `count: int`와 `-> str`은 입력과 반환값의 예상 자료형을 표시하지만 실행 중 값을 검사하지 않습니다. `isinstance(count, int)`는 현재 `count`가 정수 유형인지 확인하여 `True` 또는 `False`를 반환합니다. 이 결과가 거짓이면 `raise TypeError`로 잘못된 입력을 알립니다.", "after"),
    code('''(author / "summary.py").write_text(
    """def summarize(count: int) -> str:
    if not isinstance(count, int):
        raise TypeError('count는 정수여야 합니다')
    return f'주문 {count}건'
""", encoding="utf-8"
)
git("add", "summary.py", cwd=author)
git("commit", "-m", "fix: 주문 건수 입력 확인", cwd=author)
git("push", cwd=author)
git("fetch", "origin", cwd=reviewer)
git("switch", "main", cwd=reviewer)
git("merge", "--no-ff", "origin/feature/order-summary", "-m", "merge: 주문 요약", cwd=reviewer)
git("push", "origin", "main", cwd=reviewer)
print(git("log", "--oneline", "--graph", "-4", cwd=reviewer))
check = subprocess.run([sys.executable, "-c",
    "from summary import summarize; summarize('')"], cwd=reviewer, text=True, capture_output=True)
print("빈 문자열 종료 코드:", check.returncode)
print("입력 오류:", check.stderr.splitlines()[-1])
assert check.returncode != 0 and "TypeError: count는 정수여야 합니다" in check.stderr
assert git("rev-parse", "HEAD", cwd=reviewer) == git("rev-parse", "origin/main", cwd=reviewer)''', "after"),
])

lessons["03-병합-충돌-해결"] = notebook("병합 충돌 해결", [
    md("""## 준비

공용 원격과 두 작업 폴더를 만들고 출고 기준을 기록합니다. **병합(merge)** 은 갈라진 두 커밋 흐름의 변경을 하나의 결과로 합치는 작업입니다. 서로 다른 파일이나 서로 다른 줄을 바꿨다면 Git이 자동으로 합칠 수 있습니다. 같은 파일의 같은 줄을 서로 다르게 바꾸면 어느 내용을 선택할지 알 수 없어 **병합 충돌(merge conflict)** 로 멈춥니다.

이 실습은 `message.txt` 한 줄을 Alice와 Bob이 서로 다르게 수정합니다. `policy.txt`는 정답을 자동 생성하는 파일이 아니라 사람이 최종 문장을 판단할 근거입니다. 충돌 해결은 표시를 지우는 작업만이 아니라 두 변경의 의도를 확인해 올바른 파일 내용을 새로 결정하는 과정입니다."""),
    code(COMMON),
    code('''# 두 작업자가 함께 사용할 원격을 준비합니다.
remote = root / "team.git"
git("init", "--bare", "--initial-branch=main", remote.as_posix())
alice, bob = root / "alice", root / "bob"
git("clone", remote.as_posix(), alice.as_posix())
configure(alice)
(alice / "policy.txt").write_text(
    "14시 이전 결제: 오늘 출고\\n14시 이후 결제: 내일 출고\\n", encoding="utf-8"
)
(alice / "message.txt").write_text("배송 안내: 준비 중\\n", encoding="utf-8")
git("add", "policy.txt", "message.txt", cwd=alice)
git("commit", "-m", "docs: 출고 기준 기록", cwd=alice)
git("push", "-u", "origin", "main", cwd=alice)
# Bob은 Alice의 두 번째 변경이 게시되기 전에 공통 시작점을 복제합니다.
git("clone", remote.as_posix(), bob.as_posix())
configure(bob)
print("공용 원격과 Bob의 공통 시작점 준비 완료")'''),
    md("## 기본 실행\n\nAlice가 정책을 반영한 안내를 먼저 원격에 게시합니다."),
code('''(alice / "message.txt").write_text("배송 안내: 14시 이전은 오늘 출고\\n", encoding="utf-8")
git("add", "message.txt", cwd=alice)
git("commit", "-m", "docs: 당일 출고 안내", cwd=alice)
git("push", cwd=alice)
print(git("log", "--oneline", "-2", cwd=alice))'''),
    md("""## 값 하나를 바꿔 비교

Bob은 Alice가 두 번째 커밋을 push하기 전에 복제한 공통 `main`에서 같은 줄을 다른 문장으로 수정합니다. 따라서 두 사람은 같은 부모 커밋에서 자연스럽게 갈라지며 브랜치 위치를 따로 옮길 필요가 없습니다.

Bob의 push가 `non-fast-forward`로 거절되는 이유는 원격 `main`에 Bob이 갖고 있지 않은 Alice의 커밋이 있기 때문입니다. 강제 push로 덮는 대신 `git pull --no-rebase origin main`으로 원격 커밋을 가져와 병합합니다. `--no-rebase`는 가져온 커밋 위로 Bob의 커밋을 다시 만들지 않고 두 흐름을 병합하라는 뜻입니다."""),
    code('''(bob / "message.txt").write_text("배송 안내: 내일 출고\\n", encoding="utf-8")
git("add", "message.txt", cwd=bob)
git("commit", "-m", "docs: 익일 출고 안내", cwd=bob)
push = subprocess.run(["git", "push", "origin", "main"], cwd=bob,
                      text=True, capture_output=True)
print("push 종료 코드:", push.returncode)
print("push 거절:", push.returncode != 0)
print("거절 이유 끝줄:", push.stderr.strip().splitlines()[-1])
assert push.returncode != 0'''),
    md("## 실패 재현\n\nBob이 원격 변경을 가져와 병합하면 같은 줄의 차이에서 충돌합니다.", "before"),
    code('''merge = subprocess.run(
    ["git", "pull", "--no-rebase", "origin", "main"], cwd=bob,
    text=True, capture_output=True)
print("종료 코드:", merge.returncode)
print(git("status", "--short", cwd=bob))
print((bob / "message.txt").read_text(encoding="utf-8"))
assert merge.returncode != 0
assert "<<<<<<<" in (bob / "message.txt").read_text(encoding="utf-8")''', "before"),
    md("## 수정\n\n저장소의 정책 문서를 근거로 안내를 확정하고 원격에 게시합니다.", "after"),
    code('''resolved = "배송 안내: 14시 이전 결제는 오늘 출고, 14시 이후 결제는 내일 출고\\n"
(bob / "message.txt").write_text(resolved, encoding="utf-8")
git("add", "message.txt", cwd=bob)
git("commit", "-m", "merge: 출고 정책에 맞춰 충돌 해결", cwd=bob)
git("push", "origin", "main", cwd=bob)
print((bob / "policy.txt").read_text(encoding="utf-8").strip())
print((bob / "message.txt").read_text(encoding="utf-8").strip())
parents = git("show", "--pretty=%P", "--no-patch", "HEAD", cwd=bob)
print("병합 부모:", parents)
saved = (bob / "message.txt").read_text(encoding="utf-8")
assert all(marker not in saved for marker in ("<<<<<<<", "=======", ">>>>>>>"))
assert not git("status", "--porcelain", cwd=bob)
assert len(parents.split()) == 2
assert git("rev-parse", "HEAD", cwd=bob) == git("rev-parse", "origin/main", cwd=bob)''', "after"),
])

lessons["04-revert-reflog-worktree"] = notebook("revert, reflog, worktree", [
    md("""## 준비

정상 설정 파일과 첫 커밋을 만듭니다. 이 절의 세 도구는 같은 종류의 기능이 아닙니다. **revert**는 이미 공유한 커밋의 효과를 취소하는 새 커밋을 만듭니다. **reflog**는 이 로컬 저장소에서 HEAD나 브랜치가 이동한 기록을 보여 줍니다. **worktree**는 같은 저장소의 다른 브랜치를 별도 작업 폴더에 연결합니다. 문제 상황을 먼저 구분한 뒤 도구를 선택해야 합니다."""),
    code(COMMON),
    code('''# 복구 실습용 저장소를 준비합니다.
repo = root / "recovery"
repo.mkdir()
git("init", "-b", "main", cwd=repo)
configure(repo)
(repo / "config.txt").write_text("discount=10\\n", encoding="utf-8")
git("add", "config.txt", cwd=repo)
git("commit", "-m", "feat: 할인율 10 설정", cwd=repo)
good = git("rev-parse", "HEAD", cwd=repo)
print(git("log", "--oneline", "-1", cwd=repo))'''),
    md("""## 기본 실행

잘못된 공개 변경은 revert로 반대 변경을 새 커밋에 기록합니다. `git revert --no-edit <커밋>`에서 `<커밋>`은 취소할 대상이고, `--no-edit`는 Git이 만든 기본 되돌림 메시지를 편집기 없이 사용합니다. `discount=90` 커밋은 이력에 남고 새 커밋이 그 패치를 반대로 적용해 파일을 `discount=10`으로 되돌립니다.

반면 reset은 현재 브랜치가 가리키는 위치를 옮깁니다. 파일 결과가 같아 보일 수 있어도 이력의 모양이 다릅니다. 공유한 잘못을 고칠 때는 기존 커밋을 보존하는 revert가 협업자가 이미 받은 이력과 맞추기 쉽습니다."""),
    code('''(repo / "config.txt").write_text("discount=90\\n", encoding="utf-8")
git("add", "config.txt", cwd=repo)
git("commit", "-m", "fix: 할인율 90 설정", cwd=repo)
bad = git("rev-parse", "HEAD", cwd=repo)
git("revert", "--no-edit", bad, cwd=repo)
print((repo / "config.txt").read_text(encoding="utf-8").strip())
print(git("log", "--oneline", "-3", cwd=repo))'''),
    md("""## worktree로 두 작업 폴더 사용

별도 브랜치를 별도 폴더에 연결합니다. `git worktree add -b fix/urgent <경로>`에서 `add`는 작업 폴더를 추가하고, `-b fix/urgent`는 새 브랜치를 만들며, 마지막 인자는 폴더 위치입니다. 기본 폴더는 `main`의 `config.txt`를 유지하고 추가 폴더는 `fix/urgent`에서 `hotfix.txt`를 커밋합니다. 두 폴더는 커밋 객체를 공유하지만 체크아웃한 브랜치와 작업 파일은 구분됩니다."""),
    code('''worktree = root / "urgent-fix"
git("worktree", "add", "-b", "fix/urgent", worktree.as_posix(), cwd=repo)
(worktree / "hotfix.txt").write_text("urgent=true\\n", encoding="utf-8")
git("add", "hotfix.txt", cwd=worktree)
git("commit", "-m", "fix: 긴급 설정 추가", cwd=worktree)
print("기본 폴더 브랜치:", git("branch", "--show-current", cwd=repo))
print("추가 폴더 브랜치:", git("branch", "--show-current", cwd=worktree))
print(git("worktree", "list", "--porcelain", cwd=repo))'''),
    md("## 실패 재현\n\n아직 공유하지 않은 커밋을 hard reset으로 지우면 일반 log에서 보이지 않습니다.", "before"),
    code('''git("switch", "-c", "experiment", cwd=repo)
(repo / "idea.txt").write_text("recover me\\n", encoding="utf-8")
git("add", "idea.txt", cwd=repo)
git("commit", "-m", "experiment: 복구할 아이디어", cwd=repo)
lost = git("rev-parse", "HEAD", cwd=repo)
git("reset", "--hard", "HEAD~1", cwd=repo)
visible = git("log", "--format=%H", "-3", cwd=repo)
print("일반 log에 있음:", lost in visible)
print("파일 존재:", (repo / "idea.txt").exists())
assert lost not in visible''', "before"),
    md("""## 수정

reflog에서 이동 전 커밋을 찾아 새 브랜치 이름을 붙입니다. `git reflog --format=%H%x09%gs -5`는 최근 5개 행을 `전체 해시`, 탭 문자, `이동 이유` 순서로 출력합니다.

`reflog.splitlines()`는 출력 문자열을 행 목록으로 반환합니다. `next(...)`는 메시지에 `commit: experiment: 복구할 아이디어`가 포함된 첫 행을 고릅니다. `line.split("\\t", 1)[0]`은 첫 번째 탭에서 행을 최대 한 번 나누고 탭 앞의 해시를 반환합니다. 이 해시가 `git branch recovered-idea <해시>`의 복구 대상입니다.""", "after"),
    code('''reflog = git("reflog", "--format=%H%x09%gs", "-5", cwd=repo)
print(reflog)
assert lost in reflog
candidate = next(
    line.split("\\t", 1)[0] for line in reflog.splitlines()
    if "commit: experiment: 복구할 아이디어" in line
)
git("branch", "recovered-idea", candidate, cwd=repo)
recovered = git("show", "recovered-idea:idea.txt", cwd=repo)
print("복구 내용:", recovered)
print("복구 브랜치:", git("rev-parse", "--short", "recovered-idea", cwd=repo))
assert candidate == lost
assert recovered == "recover me"''', "after"),
])

lessons["05-시크릿-이력-정리와-예방"] = notebook("시크릿 이력 정리와 예방", [
    md("""## 준비

예제 문자열은 실제 서비스에서 사용할 수 없는 더미 자격 증명입니다. **시크릿(secret)** 은 API 키, 접근 토큰, 비밀번호처럼 권한을 부여하는 값입니다. 실제 값이 노출되면 Git 이력 정리를 기다리지 말고 발급 서비스에서 먼저 폐기하거나 교체해야 합니다. 이미 복제되거나 로그에 남은 값은 저장소 파일을 지워도 다시 통제할 수 없기 때문입니다.

이 실습은 `DEMO-ONLY-NOT-A-REAL-SECRET`만 사용합니다. 원격도 임시 폴더의 bare 저장소이므로 외부에 게시되지 않습니다. 이후 출력의 “0건”은 이 임시 저장소에서 검사한 참조에 더미 값이 없다는 뜻이며 외부 캐시나 다른 복제본까지 삭제했다는 뜻은 아닙니다."""),
    code(COMMON),
    code('''# 실제 인증에 사용할 수 없는 더미 문자열만 사용합니다.
DUMMY = "DEMO-ONLY-NOT-A-REAL-SECRET"
remote = root / "secret-remote.git"
git("init", "--bare", "--initial-branch=main", remote.as_posix())
repo = root / "secret-demo"
git("clone", remote.as_posix(), repo.as_posix())
configure(repo)
(repo / "app.py").write_text('print("safe app")\\n', encoding="utf-8")
git("add", "app.py", cwd=repo)
git("commit", "-m", "feat: 안전한 앱 시작", cwd=repo)
git("push", "-u", "origin", "main", cwd=repo)
print("더미만 사용:", DUMMY)'''),
    md("""## 기본 실행

추적 전에는 `.gitignore`와 스테이징한 변경 검사를 함께 적용합니다. `git check-ignore -v .env`에서 `-v`는 어떤 규칙이 어느 파일에 적용됐는지 보여 줍니다. `git ls-files .env`는 색인에 등록된 경로를 찾으며, 빈 출력이면 `.env`가 현재 커밋 후보에 포함되지 않았다는 뜻입니다.

`.gitignore`는 아직 추적하지 않는 경로를 기본 `git add` 대상에서 제외할 뿐 파일을 암호화하거나 과거 커밋을 지우지 않습니다. `git diff --cached -- settings.example`은 다음 커밋에 들어갈 실제 내용을 보여 주므로 커밋 직전 시크릿 검사 지점으로 사용합니다."""),
    code('''(repo / ".gitignore").write_text(".env\\n", encoding="utf-8")
(repo / ".env").write_text(f"DEMO_API_KEY={DUMMY}\\n", encoding="utf-8")
git("add", ".gitignore", cwd=repo)
git("commit", "-m", "chore: 환경 파일 제외", cwd=repo)
print(git("check-ignore", "-v", ".env", cwd=repo))
print("색인에 없음:", git("ls-files", ".env", cwd=repo) == "")'''),
    md("## 값 하나를 바꿔 검사\n\n안전한 설정 예시는 커밋할 수 있지만 더미 키 패턴이 있으면 검사를 실패로 판정합니다."),
    code('''(repo / "settings.example").write_text("DEMO_API_KEY=replace-me\\n", encoding="utf-8")
git("add", "settings.example", cwd=repo)
staged = git("diff", "--cached", "--", "settings.example", cwd=repo)
contains_dummy = DUMMY in staged
print("더미 자격 증명 발견:", contains_dummy)
print(staged)
assert not contains_dummy
git("commit", "-m", "docs: 설정 예시 추가", cwd=repo)
print("안전한 설정 예시 커밋 완료")'''),
    md("## 실패 재현\n\n파일을 다음 커밋에서 삭제해도 이전 커밋 객체에는 내용이 남습니다.", "before"),
    code('''git("check-ignore", "-q", ".env", cwd=repo)
git("add", "-f", ".env", cwd=repo)
git("commit", "-m", "test: 더미 키를 잘못 기록", cwd=repo)
leak_commit = git("rev-parse", "HEAD", cwd=repo)
git("rm", ".env", cwd=repo)
git("commit", "-m", "fix: 환경 파일 삭제", cwd=repo)
git("push", cwd=repo)
historic = git("show", f"{leak_commit}:.env", cwd=repo)
print("현재 파일 존재:", (repo / ".env").exists())
print("이전 커밋 내용:", historic.strip())
assert DUMMY in historic''', "before"),
    md("""## 수정

격리된 예제 저장소의 모든 참조에서 `.env` 경로를 제거한 뒤 원격을 강제로 갱신합니다. `git filter-repo --force`의 `--force`는 새로 복제한 저장소인지 확인하는 안전 검사를 완화합니다. 이 실습은 방금 만든 임시 mirror에만 사용하며 실제 작업 저장소에서 실행할 이유가 되지 않습니다.

`git rev-list --objects --all`의 각 행은 객체 해시와 경로를 담습니다. `objects.splitlines()`가 행 목록을 만들고, `line.endswith(" .env")`는 공백 뒤 경로가 정확히 `.env`로 끝나는 행인지 검사합니다. `any(...)`는 그런 행이 하나라도 있으면 `True`, 하나도 없으면 `False`를 반환합니다. 따라서 출력 `False`는 검사한 모든 참조에서 `.env` 경로를 찾지 못했다는 뜻입니다. 별도의 `git log -S` 결과 0건은 더미 문자열을 추가하거나 제거한 커밋도 찾지 못했다는 뜻입니다.

`len(value_hits.splitlines()) if value_hits else 0`은 결과 문자열이 있으면 행 수를 세고, 빈 문자열이면 0을 사용합니다. 따라서 검색 결과가 없을 때 출력되는 0은 빈 결과를 숫자로 표시한 값입니다.""", "after"),
    code('''clean = root / "clean-history"
git("clone", "--mirror", remote.as_posix(), clean.as_posix())
result = subprocess.run(
    ["git", "filter-repo", "--force", "--path", ".env", "--invert-paths"],
    cwd=clean, text=True, capture_output=True, check=True,
)
git("remote", "add", "origin", remote.as_posix(), cwd=clean)
git("push", "--force", "--mirror", cwd=clean)
objects = git("rev-list", "--objects", "--all", cwd=clean)
value_hits = git("log", "-S", DUMMY, "--all", "--format=%H", cwd=clean)
print("정리 후 .env 경로 있음:", any(line.endswith(" .env") for line in objects.splitlines()))
print("정리 후 더미 값 커밋 수:", len(value_hits.splitlines()) if value_hits else 0)
verify = root / "verify-remote"
git("clone", "--mirror", remote.as_posix(), verify.as_posix())
remote_objects = git("rev-list", "--objects", "--all", cwd=verify)
remote_hits = git("log", "-S", DUMMY, "--all", "--format=%H", cwd=verify)
print("원격 재검사 값 커밋 수:", len(remote_hits.splitlines()) if remote_hits else 0)
assert not any(line.endswith(" .env") for line in objects.splitlines())
assert not any(line.endswith(" .env") for line in remote_objects.splitlines())
assert not value_hits and not remote_hits''', "after"),
])


# 핵심 Git 동작 가까이에 각 셀에서 확인할 목적을 설명합니다.
CELL_NOTES = {
    "01-커밋과-gitignore": [
        None, None,
        "# 무시 규칙과 기능 코드를 나누어 기록하고 두 커밋의 메시지를 확인합니다.",
        "# 파일의 출력 숫자 하나를 바꾼 뒤 diff로 실제 변경을 읽습니다.",
        "# 이미 추적하는 debug.log는 무시 규칙을 추가해도 변경 대상으로 남습니다.",
        "# --cached는 색인에서만 제거하므로 작업 폴더의 로그 파일은 유지됩니다.",
    ],
    "02-GitHub-Flow와-PR-리뷰": [
        None, None,
        "# 타입힌트는 실행 시 값을 검사하지 않으므로 별도 입력 검증이 필요합니다.",
        "# 기본 브랜치의 템플릿을 채우고 세 점 비교로 기능 브랜치의 변경을 확인합니다.",
        "# 리뷰어의 복제본에서 빈 문자열을 직접 전달해 잘못된 출력을 재현합니다.",
        "# 수정 커밋을 공유하고 실제 TypeError와 원격 main 갱신을 함께 확인합니다.",
    ],
    "03-병합-충돌-해결": [
        None, None,
        "# Alice가 수정한 같은 줄을 먼저 원격 main에 반영합니다.",
        "# Bob이 공통 시작점에서 같은 줄을 다르게 수정해 별도 커밋을 만듭니다.",
        "# --no-rebase로 원격 main을 병합하면 같은 줄의 충돌 표시가 남습니다.",
        "# 정책에 맞춘 실제 파일에서 충돌 표시 제거와 병합 완료를 확인합니다.",
    ],
    "04-revert-reflog-worktree": [
        None, None,
        "# revert는 할인율을 되돌리는 새 커밋을 만들어 기존 이력을 유지합니다.",
        "# 별도 worktree에서 긴급 수정 브랜치를 사용하고 기본 폴더와 비교합니다.",
        "# 임시 저장소의 미공유 커밋만 이동시켜 일반 log에서 사라짐을 관찰합니다.",
        "# reflog의 커밋 메시지로 복구 대상을 찾아 새 브랜치 이름을 붙입니다.",
    ],
    "05-시크릿-이력-정리와-예방": [
        None, None,
        "# .env를 추적하기 전에 무시 규칙이 적용되는지 확인합니다.",
        "# 스테이징한 변경은 이번 커밋에 실제로 포함될 내용만 보여 줍니다.",
        "# 가상 키 파일을 다음 커밋에서 삭제해도 과거 커밋에는 값이 남습니다.",
        "# 격리된 원격의 모든 참조를 갱신하고 새 복제본에서 경로와 값을 검사합니다.",
    ],
}
for slug, data in lessons.items():
    code_cells = [cell for cell in data["cells"] if cell["cell_type"] == "code"]
    for cell, note in zip(code_cells, CELL_NOTES[slug], strict=True):
        if note:
            cell["source"] = [note + "\n", *cell["source"]]

if __name__ == "__main__":
    for slug, data in lessons.items():
        target = HERE / "notebooks" / f"{slug}.ipynb"
        target.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("wrote", target.name)
