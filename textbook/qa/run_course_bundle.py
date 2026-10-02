"""Execute representative cross-chapter paths using only extracted student files."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent / "continuity-evidence/bundle-execution"
LESSONS = (
    ("part1/ch04-data-tools", "05"),
    ("part1/ch05-llm-principles", "01"),
    ("part2/ch06-langchain-start", "06"),
    ("part2/ch07-prompt-engineering", "08"),
    ("part2/ch08-context-engineering", "02"),
    ("part2/ch08-context-engineering", "03"),
    ("part2/ch08-context-engineering", "06"),
    ("part3/ch09-rag-first-run", "02"),
    ("part3/ch11-evaluation", "06"),
    ("part3/ch12-retrieval-tuning", "04"),
    ("part3/ch12-retrieval-tuning", "12"),
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    archive_path = ROOT / "textbook/downloads/llm-practice.zip"
    work = Path(tempfile.mkdtemp(prefix="course-delivery-"))
    with ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        assert all(not Path(name).is_absolute() and ".." not in Path(name).parts
                   for name in archive.namelist())
        archive.extractall(work)
    extracted = work / "llm-practice"
    environment = os.environ.copy()
    for key, value in dotenv_values(ROOT / ".env").items():
        if key.endswith("API_KEY") and value:
            environment[key] = value
    assert environment.get("OPENAI_API_KEY")
    (extracted / ".env").write_text("# Keys are supplied only in the verification process environment.\n")
    report = {"archive_sha256": sha(archive_path), "extracted": str(extracted),
              "student_files_from_zip_only": True, "credentials_written": False,
              "runner_extras_in_student_kernel": False, "notebooks": [], "commands": []}

    def command(args, cwd, label):
        result = subprocess.run(args, cwd=cwd, env=environment, text=True, capture_output=True, check=False)
        output = result.stdout + result.stderr
        for key, value in environment.items():
            if any(word in key for word in ("API_KEY", "TOKEN", "SECRET")) and len(value) > 10:
                output = output.replace(value, "[비밀값]")
        output = output.replace(str(Path.home()), "[사용자 폴더]")
        (OUT / (label + ".txt")).write_text(output)
        assert result.returncode == 0, f"{label} failed; see redacted execution log"
        return output

    prepared = set()
    try:
        hello_lab = extracted / "labs/part1/ch01-development-environment"
        command(["uv", "sync", "--locked"], hello_lab, "ch01-sync")
        output = command(["uv", "run", "python", "hello.py"], hello_lab, "ch01-hello")
        assert "총액: 6000원" in output
        report["commands"].append({"chapter": "ch01", "command": "uv run python hello.py", "passed": True})
        # Prove Ch4 produces the file; Ch5 must consume this new result.
        (extracted / "labs/part1/ch04-data-tools/data/article-text.json").unlink()
        for chapter, prefix in LESSONS:
            lab = extracted / "labs" / chapter
            if chapter not in prepared:
                command(["uv", "sync", "--locked"], lab, lab.name + "-sync")
                prepared.add(chapter)
            notebook = next((lab / "notebooks").glob(prefix + "-*.ipynb"))
            before_bytes = notebook.read_bytes()
            command([sys.executable, str(ROOT / "textbook/_notebook/execute.py"), str(notebook),
                     "--cwd", str(notebook.parent), "--kernel-python", str(lab / ".venv/bin/python")],
                    extracted, lab.name + "-" + prefix)
            nb = json.loads(notebook.read_text())
            target = OUT / chapter / notebook.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(notebook, target)
            report["notebooks"].append({"path": str(notebook.relative_to(extracted)),
                                         "shipped_sha256": hashlib.sha256(before_bytes).hexdigest(),
                                         "executed_sha256": sha(notebook),
                                         "verification": nb["metadata"]["verification"]})
            if (lab / "runs").exists():
                shutil.copytree(lab / "runs", OUT / chapter / "runs", dirs_exist_ok=True)
            print("Extracted ZIP fresh kernel:", chapter, prefix, flush=True)
            (OUT.parent / "bundle-execution-results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))

        article = extracted / "labs/part1/ch04-data-tools/data/article-text.json"
        assert article.read_bytes() == (ROOT / "labs/part1/ch04-data-tools/data/article-text.json").read_bytes()
        shutil.copy2(article, OUT / "article-text.json")
        handoffs = []
        for chapter, filename in (
            ("ch07-prompt-engineering", "prompt-ab-continuity.json"),
            ("ch08-context-engineering", "context-design-continuity.json"),
        ):
            row = json.loads((extracted / "labs/part2" / chapter / "runs" / filename).read_text())
            source = row["source_record"]
            assert source["sha256"] == sha(extracted / source["path"])
            handoffs.append({"run_id": row["run_id"], "source": source})
        report["article_handoff"] = {"sha256": sha(article), "generated_by_ch04_then_read_by_ch05": True}
        report["part2_handoffs"] = handoffs
        report["status"] = "passed"
    finally:
        (extracted / ".env").unlink(missing_ok=True)
        (OUT.parent / "bundle-execution-results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print("Full ZIP representative paths passed", flush=True)


if __name__ == "__main__":
    main()
