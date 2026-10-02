from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TEMPLATE = REPO / "textbook" / "_template"
NOTEBOOK_RUNTIME = REPO / "textbook" / "_notebook"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scaffold = _load("lesson_scaffold", TEMPLATE / "scaffold.py")
builder = _load("lesson_builder", TEMPLATE / "builder.py")


def _copy_runtime(root: Path) -> None:
    shutil.copytree(TEMPLATE, root / "textbook" / "_template")
    target = root / "textbook" / "_notebook"
    target.mkdir(parents=True)
    for name in ("render.py", "execute.py", "theme.css", "copy.js"):
        shutil.copy2(NOTEBOOK_RUNTIME / name, target / name)


def _finish_config_and_sources(chapter: Path) -> None:
    config_path = chapter / "chapter.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["part_title"] = "Part 9 · 템플릿 검증"
    config["hours"] = "총 2h · 강의 1h · 실습 1h"
    config["objectives"] = ["실행 결과를 HTML에서 확인할 수 있습니다."]
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for source in (chapter / "_src").glob("*.html"):
        text = re.sub(r"\[\[작성:.*?\]\]", "템플릿 검증 내용", source.read_text(encoding="utf-8"))
        source.write_text(text, encoding="utf-8")


def _finish_notebook(path: Path, *, lesson_format: str) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        if cell["cell_type"] == "markdown":
            source = "".join(cell["source"])
            source = re.sub(r"\[\[작성:.*?\]\]", "실제 실행 결과를 확인합니다.", source)
            cell["source"] = source.splitlines(keepends=True)
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    common = [
        'runtime = "Python 3.12"\nprint("준비:", runtime)',
        'base = 2\nprint("기본 결과:", base)',
        'observed = base * 3\nprint("중간 결과:", observed)',
        'changed = 4\nprint("한 값 비교:", base, changed)',
    ]
    tail = (
        [
            'try:\n    int("잘못된 숫자")\nexcept ValueError as error:\n    print("Before 관찰:", type(error).__name__)',
            'fixed = int("3")\nprint("After 결과:", fixed)\nassert fixed == 3',
        ]
        if lesson_format == "paired"
        else ['results = [base * value for value in (1, 2, 3)]\nprint("실험 결과:", results)\nassert results == [2, 4, 6]']
    )
    assert len(code_cells) == len(common + tail)
    for cell, source in zip(code_cells, common + tail, strict=True):
        cell["source"] = source.splitlines(keepends=True)
        cell["outputs"] = []
        cell["execution_count"] = None
    notebook["metadata"].pop("verification", None)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def test_scaffold_executes_and_builds_paired_and_experiment(tmp_path: Path) -> None:
    _copy_runtime(tmp_path)
    chapter, lab = scaffold.create_scaffold(
        root=tmp_path,
        part=9,
        chapter="ch99-template-test",
        title="템플릿 검증",
        section="01-paired",
        lesson_format="paired",
    )
    with pytest.raises(FileExistsError, match="덮어쓰지"):
        scaffold.create_scaffold(
            root=tmp_path,
            part=9,
            chapter="ch99-template-test",
            title="템플릿 검증",
            section="01-paired",
            lesson_format="paired",
        )
    scaffold.add_section(
        root=tmp_path,
        part=9,
        chapter="ch99-template-test",
        section="02-experiment",
        lesson_format="experiment",
    )
    with pytest.raises(FileExistsError, match="절 번호"):
        scaffold.add_section(
            root=tmp_path,
            part=9,
            chapter="ch99-template-test",
            section="02-another",
            lesson_format="paired",
        )

    with pytest.raises(ValueError, match="unfinished"):
        builder.build_chapter(chapter, root=tmp_path)
    _finish_config_and_sources(chapter)
    paired = lab / "notebooks" / "01-paired.ipynb"
    experiment = lab / "notebooks" / "02-experiment.ipynb"
    _finish_notebook(paired, lesson_format="paired")
    _finish_notebook(experiment, lesson_format="experiment")
    with pytest.raises(ValueError, match="successful fresh-kernel verification"):
        builder.build_chapter(chapter, root=tmp_path)

    subprocess.run(
        [
            sys.executable,
            str(tmp_path / "textbook" / "_notebook" / "execute.py"),
            str(paired),
            str(experiment),
            "--cwd",
            str(tmp_path),
            "--kernel-python",
            sys.executable,
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    subprocess.run([sys.executable, str(chapter / "_build.py")], check=True, cwd=tmp_path)

    index = (chapter / "index.html").read_text(encoding="utf-8")
    paired_html = (chapter / "01-paired.html").read_text(encoding="utf-8")
    experiment_html = (chapter / "02-experiment.html").read_text(encoding="utf-8")
    assert "01-paired.html" in index and "02-experiment.html" in index
    assert "실패와 수정 비교" in index and "실험 결과 해석" in index
    assert "Ch 99 · 템플릿 검증" in index
    assert "Before 관찰:" in paired_html and "ValueError" in paired_html
    assert "After 결과:" in paired_html and "3" in paired_html
    assert "실험 결과:" in experiment_html and "[2, 4, 6]" in experiment_html
    assert 'data-lesson-format="paired"' in paired_html
    assert 'data-lesson-format="experiment"' in experiment_html


def test_cli_add_section_and_path_validation(tmp_path: Path) -> None:
    _copy_runtime(tmp_path)
    command = [
        sys.executable,
        str(TEMPLATE / "scaffold.py"),
        "--root",
        str(tmp_path),
        "--part",
        "9",
        "--chapter",
        "ch98-cli-test",
        "--title",
        "CLI 검증",
        "--section",
        "01-first",
        "--format",
        "paired",
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)
    subprocess.run(
        [*command[:-3], "02-second", "--format", "experiment", "--add-section"],
        check=True,
        capture_output=True,
        text=True,
    )
    config = json.loads(
        (tmp_path / "textbook" / "part9" / "ch98-cli-test" / "chapter.json").read_text(encoding="utf-8")
    )
    assert [section["slug"] for section in config["sections"]] == ["01-first", "02-second"]
    with pytest.raises(ValueError, match="chapter"):
        scaffold.create_scaffold(
            root=tmp_path,
            part=9,
            chapter="../escape",
            title="잘못된 경로",
            section="01-test",
            lesson_format="paired",
        )
def test_scaffold_rejects_paths_and_unfinished_notebook(tmp_path: Path) -> None:
    _copy_runtime(tmp_path)
    with pytest.raises(ValueError, match="chapter"):
        scaffold.create_scaffold(
            root=tmp_path,
            part=9,
            chapter="../escape",
            title="탈출 거부",
            section="01-test",
            lesson_format="paired",
        )
    chapter, lab = scaffold.create_scaffold(
        root=tmp_path,
        part=9,
        chapter="ch98-unfinished",
        title="미완성 거부",
        section="01-test",
        lesson_format="paired",
    )
    _finish_config_and_sources(chapter)
    with pytest.raises(ValueError, match="notebook contains unfinished"):
        builder.build_chapter(chapter, root=tmp_path)
    notebook = json.loads((lab / "notebooks" / "01-test.ipynb").read_text(encoding="utf-8"))
    assert "verification" not in notebook["metadata"]
    assert all(not cell.get("outputs") for cell in notebook["cells"] if cell["cell_type"] == "code")


@pytest.mark.parametrize("body", [
    '<h2>강사 노트</h2>',
    '<details class="instructor">진행 안내</details>',
    "<details class='instructor'>진행 안내</details>",
])
def test_builder_rejects_instructor_content(body: str) -> None:
    with pytest.raises(ValueError, match="instructor"):
        builder._assert_publishable(body, "01-example")
