"""Generate the five Ch 3 lesson notebooks from reviewed cell sources."""

from __future__ import annotations

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
    all_cells = [md(f"# {title}\n\n모든 저장소는 임시 폴더에 만들며 실제 GitHub 계정이나 원격 저장소를 변경하지 않습니다.\n"), *cells]
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
    md("## 준비\n\n임시 저장소를 만들고 이 노트북에만 적용되는 작성자 정보를 설정합니다."),
    code(COMMON),
    code('''# 저장소를 main 브랜치로 초기화합니다.
repo = root / "orders"
repo.mkdir()
git("init", "-b", "main", cwd=repo)
configure(repo)
print(repo.name, git("branch", "--show-current", cwd=repo))'''),
    md("## 기본 실행\n\n무시 규칙을 첫 커밋에, 프로그램을 다음 커밋에 기록합니다."),
    code('''(repo / "app.py").write_text('print("주문 2건")\\n', encoding="utf-8")
(repo / ".gitignore").write_text(".env\\n__pycache__/\\n", encoding="utf-8")
(repo / ".env").write_text("APP_MODE=demo\\n", encoding="utf-8")
git("add", ".gitignore", cwd=repo)
git("commit", "-m", "chore: 생성 파일 추적 제외", cwd=repo)
git("add", "app.py", cwd=repo)
git("commit", "-m", "feat: 주문 요약 추가", cwd=repo)
print(git("status", "--short", "--ignored", cwd=repo))
print(git("log", "-2", "--pretty=%s", cwd=repo))'''),
    md("## 값 하나를 바꿔 비교\n\n출력 숫자만 2에서 3으로 바꾸고 차이를 확인합니다."),
    code('''(repo / "app.py").write_text('print("주문 3건")\\n', encoding="utf-8")
print(git("diff", "--", "app.py", cwd=repo))
git("add", "app.py", cwd=repo)
git("commit", "-m", "fix: 주문 건수 수정", cwd=repo)
print(git("log", "--oneline", "-2", cwd=repo))'''),
    md("## 실패 재현\n\n이미 추적 중인 파일은 나중에 무시 규칙을 추가해도 추적 상태가 유지됩니다.", "before"),
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
    md("## 준비\n\n로컬 bare 저장소를 원격 저장소처럼 사용합니다."),
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
    md("## 기본 실행\n\n기능 브랜치를 만들고 커밋한 뒤 원격에 게시합니다."),
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
    md("## PR 자료와 변경 범위\n\n기본 브랜치에 준비된 템플릿을 읽고 기능 코드 차이만 확인합니다."),
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
    md("## 수정\n\n작성자가 입력을 정수로 제한하고 리뷰어가 원격 변경을 받아 병합합니다.", "after"),
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
    md("## 준비\n\n공용 원격과 두 작업 폴더를 만들고 출고 기준을 기록합니다."),
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
print("공용 원격 준비 완료")'''),
    md("## 기본 실행\n\nAlice가 정책을 반영한 안내를 먼저 원격에 게시합니다."),
code('''(alice / "message.txt").write_text("배송 안내: 14시 이전은 오늘 출고\\n", encoding="utf-8")
git("add", "message.txt", cwd=alice)
git("commit", "-m", "docs: 당일 출고 안내", cwd=alice)
git("push", cwd=alice)
print(git("log", "--oneline", "-2", cwd=alice))'''),
    md("## 값 하나를 바꿔 비교\n\nBob은 이전 main에서 같은 줄을 다른 문장으로 수정합니다."),
    code('''git("clone", remote.as_posix(), bob.as_posix())
configure(bob)
git("reset", "--hard", "HEAD~1", cwd=bob)
(bob / "message.txt").write_text("배송 안내: 내일 출고\\n", encoding="utf-8")
git("add", "message.txt", cwd=bob)
git("commit", "-m", "docs: 익일 출고 안내", cwd=bob)
push = subprocess.run(["git", "push", "origin", "main"], cwd=bob,
                      text=True, capture_output=True)
print("push 종료 코드:", push.returncode)
print("원격보다 이전 이력:", "non-fast-forward" in push.stderr)
assert push.returncode != 0 and "non-fast-forward" in push.stderr'''),
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
    md("## 준비\n\n정상 파일과 두 개의 커밋을 만듭니다."),
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
    md("## 기본 실행\n\n잘못된 공개 변경은 revert로 반대 변경을 새 커밋에 기록합니다."),
    code('''(repo / "config.txt").write_text("discount=90\\n", encoding="utf-8")
git("add", "config.txt", cwd=repo)
git("commit", "-m", "fix: 할인율 90 설정", cwd=repo)
bad = git("rev-parse", "HEAD", cwd=repo)
git("revert", "--no-edit", bad, cwd=repo)
print((repo / "config.txt").read_text(encoding="utf-8").strip())
print(git("log", "--oneline", "-3", cwd=repo))'''),
    md("## worktree로 두 작업 폴더 사용\n\n별도 브랜치를 별도 폴더에 연결합니다."),
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
    md("## 수정\n\nreflog에서 이동 전 커밋을 찾아 새 브랜치 이름을 붙입니다.", "after"),
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
    md("## 준비\n\n예제 문자열은 실제 서비스에서 사용할 수 없는 더미 자격 증명입니다."),
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
    md("## 기본 실행\n\n추적 전에는 .gitignore와 staged diff 검사를 함께 적용합니다."),
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
    md("## 수정\n\n격리된 예제 저장소의 모든 참조에서 .env 경로를 제거한 뒤 원격을 강제로 갱신합니다.", "after"),
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
        "# Bob의 임시 복제본만 이전 커밋으로 옮겨 서로 다른 변경을 만듭니다.",
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
        "# staged diff는 이번 커밋에 실제로 포함될 내용만 보여 줍니다.",
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
