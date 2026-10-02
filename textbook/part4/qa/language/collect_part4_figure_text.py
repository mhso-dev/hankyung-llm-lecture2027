#!/usr/bin/env python3
"""Collect Part 4 figure captions and visible SVG labels for language review."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path


TEXT_RE = re.compile(r"<text\b[^>]*>(.*?)</text>", re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def svg_labels(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    labels: list[str] = []
    for raw in TEXT_RE.findall(source):
        value = html.unescape(TAG_RE.sub("", raw)).strip()
        if value:
            labels.append(value)
    return "\n".join(labels)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--chapter", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    figure_dir = root / "textbook" / "part4" / args.chapter / "figures"
    blocks: list[str] = []
    files: list[dict[str, str | int]] = []

    for path in sorted(figure_dir.glob("*.caption.md")):
        text = path.read_text(encoding="utf-8").strip()
        relative = path.relative_to(root)
        blocks.append(f"\n===== {relative.as_posix()} =====\n{text}\n")
        files.append(
            {
                "path": relative.as_posix(),
                "source_sha256": sha256(path),
                "characters": len(text),
                "kind": "caption",
            }
        )

    for path in sorted(figure_dir.glob("*.svg")):
        text = svg_labels(path)
        relative = path.relative_to(root)
        blocks.append(f"\n===== {relative.as_posix()} =====\n{text}\n")
        files.append(
            {
                "path": relative.as_posix(),
                "source_sha256": sha256(path),
                "characters": len(text),
                "kind": "svg_labels",
            }
        )

    text = "\n".join(blocks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    manifest = {
        "snapshot": args.output.name,
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "files": len(files),
        "items": files,
        "note": "Read-only extraction of caption Markdown and visible SVG text labels.",
    }
    args.output.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
