#!/usr/bin/env python3
"""Collect the Part 2 student-facing Korean prose for a read-only language audit."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path


class TextOnly(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.suppressed_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"code", "pre", "script", "style"}:
            self.suppressed_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"code", "pre", "script", "style"} and self.suppressed_depth:
            self.suppressed_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.suppressed_depth:
            self.parts.append(data)


def html_text(path: Path) -> str:
    parser = TextOnly()
    parser.feed(path.read_text())
    return "\n".join(line.strip() for line in parser.parts if line.strip())


def notebook_markdown(path: Path) -> str:
    notebook = json.loads(path.read_text())
    sections = []
    for index, cell in enumerate(notebook["cells"]):
        if cell.get("cell_type") == "markdown":
            source = "".join(cell.get("source", []))
            sections.append(f"[markdown cell {index}]\n{source.strip()}")
    return "\n\n".join(sections)


def markdown_prose(path: Path) -> str:
    """Remove fenced code so audit metrics do not score executable text."""
    return re.sub(r"```.*?```", "", path.read_text(), flags=re.DOTALL).strip()


def public_python_strings(path: Path) -> str:
    """Keep Korean-bearing literals from a page-builder; omit Python and CSS syntax."""
    tree = ast.parse(path.read_text())
    strings = [
        node.value.strip()
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and re.search(r"[가-힣]", node.value)
        and node.value.strip()
    ]
    return "\n\n".join(strings)


def add(sections: list[str], path: Path, text: str) -> None:
    sections.append(f"\n===== {path.as_posix()} =====\n{text.strip()}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--chapter",
        action="append",
        choices=("ch06-langchain-start", "ch07-prompt-engineering", "ch08-context-engineering"),
        help="Chapter slug to collect; repeat to collect more than one. Defaults to all Part 2 chapters.",
    )
    parser.add_argument("--include-shared", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    sections: list[str] = []
    slugs = args.chapter or ("ch06-langchain-start", "ch07-prompt-engineering", "ch08-context-engineering")
    for slug in slugs:
        chapter = root / "textbook" / "part2" / slug
        for path in sorted((chapter / "_src").glob("*.html")):
            add(sections, path.relative_to(root), html_text(path))
        lab = root / "labs" / "part2" / slug
        add(sections, (lab / "README.md").relative_to(root), markdown_prose(lab / "README.md"))
        for path in sorted((lab / "notebooks").glob("*.ipynb")):
            add(sections, path.relative_to(root), notebook_markdown(path))

    if args.include_shared:
        practice_start = root / "textbook/_notebook/practice-start.md"
        add(sections, practice_start.relative_to(root), markdown_prose(practice_start))
        builder = root / "textbook/part2/_build_index.py"
        add(sections, builder.relative_to(root), public_python_strings(builder))

    text = "\n".join(sections)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    manifest = {
        "snapshot": args.output.name,
        "sha256": hashlib.sha256(text.encode()).hexdigest(),
        "sections": len(sections),
        "note": "Read-only extraction. HTML prose, notebook Markdown, README, and public Part 2 start-page source are included.",
    }
    args.output.with_suffix(".manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
