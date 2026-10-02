import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_nonconsecutive_metric_violations_do_not_fire(tmp_path: Path):
    rows = [
        {"minute": 1, "requests": 100, "errors": 9, "p95_ms": 900},
        {"minute": 2, "requests": 100, "errors": 1, "p95_ms": 300},
        {"minute": 3, "requests": 100, "errors": 9, "p95_ms": 900},
    ]
    metrics = tmp_path / "metrics.jsonl"
    metrics.write_text("\n".join(json.dumps(row) for row in rows))
    result = subprocess.run(
        [sys.executable, ROOT / "scripts/check_metrics.py", metrics], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "longest_streak=1" in result.stdout


def test_regression_script_scores_case_content():
    result = subprocess.run(
        [sys.executable, ROOT / "scripts/evaluate_regression.py"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "groundedness=1.00" in result.stdout


def test_candidate_code_regression_fails_gate(tmp_path: Path):
    shutil.copytree(ROOT / "scripts", tmp_path / "scripts")
    shutil.copytree(ROOT / "data", tmp_path / "data")
    source = (ROOT / "cicd_demo.py").read_text()
    source = source.replace("7권까지 14일", "8권까지 10일")
    (tmp_path / "cicd_demo.py").write_text(source)
    result = subprocess.run(
        [sys.executable, tmp_path / "scripts/evaluate_regression.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "groundedness: FAIL" in result.stdout
