#!/usr/bin/env python3
"""Build the final Part 3 student-prose snapshot and source manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from collect_lab_text import notebook_markdown, without_fenced_code
from collect_student_text import html_text


CHAPTERS = (
    "ch09-rag-first-run",
    "ch10-document-processing",
    "ch11-evaluation",
    "ch12-retrieval-tuning",
)


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def add_file(
    blocks: list[str],
    items: list[dict[str, str | int]],
    root: Path,
    path: Path,
    kind: str,
    prose: str,
) -> None:
    relative = path.relative_to(root).as_posix()
    blocks.append(f"\n===== {relative} =====\n{prose}\n")
    items.append(
        {
            "path": relative,
            "kind": kind,
            "source_sha256": digest_bytes(path.read_bytes()),
            "prose_sha256": digest_bytes(prose.encode("utf-8")),
            "prose_characters": len(prose),
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--archive",
        type=Path,
        default=Path("textbook/downloads/part3-practice.zip"),
    )
    args = parser.parse_args()

    root = args.root.resolve()
    archive = args.archive if args.archive.is_absolute() else root / args.archive
    blocks: list[str] = []
    items: list[dict[str, str | int]] = []

    for slug in CHAPTERS:
        chapter = root / "textbook" / "part3" / slug
        section_paths = sorted((chapter / "_src").glob("[0-9][0-9]-*.html"))
        for path in section_paths:
            add_file(blocks, items, root, path, "section", html_text(path))
        add_file(blocks, items, root, chapter / "index.html", "chapter_index", html_text(chapter / "index.html"))

    part_index = root / "textbook" / "part3" / "index.html"
    add_file(blocks, items, root, part_index, "part_index", html_text(part_index))

    for slug in CHAPTERS:
        chapter = root / "labs" / "part3" / slug
        readme = chapter / "README.md"
        add_file(
            blocks,
            items,
            root,
            readme,
            "readme",
            without_fenced_code(readme.read_text(encoding="utf-8")),
        )
        for path in sorted((chapter / "notebooks").glob("[0-9][0-9]-*.ipynb")):
            add_file(blocks, items, root, path, "notebook_markdown", notebook_markdown(path))

    with zipfile.ZipFile(archive) as bundle:
        start_names = [name for name in bundle.namelist() if name.endswith("/시작하기.md")]
        if len(start_names) != 1:
            raise SystemExit(f"expected one 시작하기.md in archive, found {len(start_names)}")
        start_name = start_names[0]
        start_bytes = bundle.read(start_name)
        start_prose = without_fenced_code(start_bytes.decode("utf-8"))
        blocks.append(f"\n===== {archive.relative_to(root).as_posix()}::{start_name} =====\n{start_prose}\n")
        items.append(
            {
                "path": f"{archive.relative_to(root).as_posix()}::{start_name}",
                "kind": "archive_start",
                "source_sha256": digest_bytes(start_bytes),
                "prose_sha256": digest_bytes(start_prose.encode("utf-8")),
                "prose_characters": len(start_prose),
            }
        )

    counts: dict[str, int] = {}
    for item in items:
        kind = str(item["kind"])
        counts[kind] = counts.get(kind, 0) + 1
    expected = {
        "section": 32,
        "chapter_index": 4,
        "part_index": 1,
        "readme": 4,
        "notebook_markdown": 32,
        "archive_start": 1,
    }
    if counts != expected:
        raise SystemExit(f"scope count mismatch: expected {expected}, found {counts}")

    text = "\n".join(blocks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    build_script = root / "textbook" / "part3" / "_build_index.py"
    manifest = {
        "snapshot": args.output.name,
        "snapshot_sha256": digest_bytes(text.encode("utf-8")),
        "scope_counts": counts,
        "prose_characters": sum(int(item["prose_characters"]) for item in items),
        "build_index_source_sha256": digest_bytes(build_script.read_bytes()),
        "archive_sha256": digest_bytes(archive.read_bytes()),
        "items": items,
        "note": (
            "Read-only extraction. HTML code/pre/script/style, notebook code cells, "
            "outputs and metadata, and fenced README code blocks are excluded."
        ),
    }
    manifest_path = args.output.with_suffix(".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: value for key, value in manifest.items() if key != "items"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
