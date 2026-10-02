"""Check locked student environments without the verification runner's extras."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent / "continuity-evidence"


def main():
    work = Path(tempfile.mkdtemp(prefix="course-locked-environments-"))
    rows = []
    for source in sorted((ROOT / "labs").glob("part*/ch*/pyproject.toml")):
        lab = work / source.parent.name
        lab.mkdir()
        for name in ("pyproject.toml", "uv.lock"):
            shutil.copy2(source.parent / name, lab / name)
        sync = subprocess.run(["uv", "sync", "--locked", "--project", str(lab)],
                              capture_output=True, text=True, check=False)
        assert sync.returncode == 0, sync.stderr
        python = lab / ".venv/bin/python"
        kernel = lab / "kernels/python3"
        kernel.mkdir(parents=True)
        (kernel / "kernel.json").write_text(json.dumps({
            "argv": [str(python), "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            "display_name": "Student chapter environment", "language": "python"}))
        manager = KernelManager(kernel_name="python3", kernel_spec_manager=KernelSpecManager(
            kernel_dirs=[str(kernel.parent)]))
        needs_pip = any("%pip" in "".join(cell["source"]) for path in (source.parent / "notebooks").glob("*.ipynb")
                        for cell in json.loads(path.read_text())["cells"] if cell["cell_type"] == "code")
        notebook = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(
            "import sys, importlib.metadata, json\n"
            "assert sys.version_info[:2] == (3, 12)\n"
            "print(json.dumps({'python': sys.version.split()[0], "
            "'ipykernel': importlib.metadata.version('ipykernel'), "
            "'environment': sys.prefix}))")])
        if needs_pip:
            notebook.cells.append(nbformat.v4.new_code_cell("%pip --version"))
        try:
            NotebookClient(notebook, km=manager, timeout=60,
                           resources={"metadata": {"path": str(lab)}}).execute()
        finally:
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
        result = json.loads(notebook.cells[0].outputs[0].text)
        if needs_pip:
            pip_output = "".join(output.get("text", "") for output in notebook.cells[1].outputs)
            assert "No module named pip" not in pip_output and "pip 26.2 " in pip_output, pip_output
            result["pip_magic"] = "passed: pip 26.2"
        else:
            result["pip_magic"] = "not needed: no student pip cell"
        assert Path(result["environment"]) == python.parent.parent
        rows.append({"chapter": source.parent.name, "sync_locked": True,
                     "fresh_kernel": True, "runner_extras_in_student_environment": False,
                     **result})
        print(source.parent.name, result["python"], "kernel", result["ipykernel"], flush=True)
        (OUT / "locked-environment-results.json").write_text(json.dumps(
            {"status": "running", "chapters": rows}, ensure_ascii=False, indent=2))
    (OUT / "locked-environment-results.json").write_text(json.dumps(
        {"status": "passed", "chapters": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
