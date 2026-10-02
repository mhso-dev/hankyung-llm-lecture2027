"""Smoke-test the public archive from a fresh extraction and notebook cwd.

전체 마감 2026-10-01: 노트북 실행기를 지금 구조에 맞게 고침 — 옛 32행은 Ch 31 실습 폴더의 macOS `.venv` 파이썬으로
execute.py를 돌려 작업 기기(Linux)에서 멈췄다. Part 4·5·6 `check_bundle_execution.py`와 같게 묶음 속 챕터 프로젝트에서
`uv run --project <챕터> --with nbclient==0.11.0 --with python-dotenv==1.2.3 python execute.py`로 돌리고(커널은 그 챕터의
`uv sync --locked` `.venv`), 보고서에 묶음 이름·해시를 적는다. 실행 대상(SMOKE_SECTIONS)은 그대로다.
DB가 필요한 절(Ch 31 03)은 학생처럼 README의 Docker 컨테이너를 켜 둔 뒤 돌리거나, 작업 기기에서는 `--pre-exec`를 주어
그 챕터 `qa/upgrade/pre_exec.sh`(127.0.0.1:55431 PostgreSQL 훅)를 같은 셸에서 먼저 불러 실행한다(셸이 끝나면 훅이 서버를 끔).
"""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
REPORT = ROOT / "textbook/part7/qa/bundle-execution.json"
SMOKE_SECTIONS = {"ch30-fastapi-serving": "01", "ch31-database": "03", "ch33-cicd": "02"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pre-exec", action="store_true",
                        help="Source textbook/part7/<chapter>/qa/upgrade/pre_exec.sh before a smoke notebook (work machine).")
    args = parser.parse_args()
    archive_path = ROOT / "textbook/downloads/part7-practice.zip"
    results = []
    with tempfile.TemporaryDirectory(prefix="part7-student-") as folder:
        with ZipFile(archive_path) as archive:
            archive.extractall(folder)
        extracted = Path(folder) / "part7-practice"
        for lab in sorted((extracted / "labs/part7").glob("ch*")):
            sync = subprocess.run(
                ["uv", "sync", "--locked", "--project", str(lab)],
                capture_output=True, text=True, check=True,
            )
            python = lab / ".venv/bin/python"
            subprocess.run([str(python), "-c", "import ipykernel, pip"], check=True)
            entry = {"chapter": lab.name, "locked_sync": sync.returncode == 0,
                     "notebook_kernel_import": True}
            if lab.name in SMOKE_SECTIONS:
                number = SMOKE_SECTIONS[lab.name]
                notebook = next((lab / "notebooks").glob(f"{number}-*.ipynb"))
                runner = [
                    "uv", "run", "--project", str(lab), "--with", "nbclient==0.11.0",
                    "--with", "python-dotenv==1.2.3", "python",
                    str(ROOT / "textbook/_notebook/execute.py"), str(notebook),
                    "--cwd", str(lab / "notebooks"), "--kernel-python", str(python),
                ]
                hook = ROOT / "textbook/part7" / lab.name / "qa/upgrade/pre_exec.sh"
                if args.pre_exec and hook.is_file():
                    # 훅을 불러 둔 같은 셸에서 실행기를 돌린다(훅의 trap EXIT가 셸이 끝날 때 서버를 끈다)
                    runner = ["bash", "-c", '. "$1" || exit 1; shift; "$@"', "pre_exec", str(hook), *runner]
                    entry["pre_exec"] = str(hook.relative_to(ROOT))
                subprocess.run(runner, cwd=lab, check=True)
                nb = json.loads(notebook.read_text())
                entry["execution"] = nb["metadata"]["verification"]
                entry["notebook"] = notebook.name
                entry["cwd"] = "chapter/notebooks"
            results.append(entry)
            print(f"PASS extracted archive: {lab.name}", flush=True)
        assert not list(extracted.rglob(".env"))
    REPORT.write_text(json.dumps({"archive": archive_path.name,
                                  "archive_sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
                                  "chapters": results, "actual_env_files": 0},
                                 ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
