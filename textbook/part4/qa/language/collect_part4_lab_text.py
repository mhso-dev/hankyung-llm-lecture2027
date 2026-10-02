#!/usr/bin/env python3
"""Collect Part 4 README prose and notebook Markdown without code or outputs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_fenced_code(text: str) -> str:
    kept: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            kept.append(line)
    return "\n".join(kept).strip()


def notebook_markdown(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells: list[str] = []
    for index, cell in enumerate(notebook.get("cells", []), start=1):
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", [])
        raw = source if isinstance(source, str) else "".join(source)
        prose = without_fenced_code(raw)
        if prose:
            cells.append(f"[markdown cell {index}]\n{prose}")
    return "\n\n".join(cells)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--chapter", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--include-readme", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    chapter = root / "labs" / "part4" / args.chapter
    blocks: list[str] = []
    files: list[dict[str, str | int]] = []

    if args.include_readme:
        path = chapter / "README.md"
        if path.is_file():
            prose = without_fenced_code(path.read_text(encoding="utf-8"))
            relative = path.relative_to(root)
            blocks.append(f"\n===== {relative.as_posix()} =====\n{prose}\n")
            files.append(
                {
                    "path": relative.as_posix(),
                    "source_sha256": sha256(path),
                    "prose_characters": len(prose),
                    "kind": "readme",
                }
            )

    for path in sorted((chapter / "notebooks").glob("[0-9][0-9]-*.ipynb")):
        prose = notebook_markdown(path)
        relative = path.relative_to(root)
        blocks.append(f"\n===== {relative.as_posix()} =====\n{prose}\n")
        files.append(
            {
                "path": relative.as_posix(),
                "source_sha256": sha256(path),
                "prose_characters": len(prose),
                "kind": "notebook_markdown",
            }
        )

    text = "\n".join(blocks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    manifest = {
        "snapshot": args.output.name,
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "files": len(files),
        "prose_characters": sum(int(item["prose_characters"]) for item in files),
        "items": files,
        "note": "Read-only extraction. Notebook code cells, outputs, metadata, and fenced README code blocks are excluded.",
    }
    args.output.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
