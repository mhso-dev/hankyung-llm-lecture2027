#!/usr/bin/env python3
"""Collect Part 4 source prose for a read-only language audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path


class TextOnly(HTMLParser):
    """Extract visible prose while protecting code and preformatted output."""

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
            value = data.strip()
            if value and not value.startswith("{{notebook:"):
                self.parts.append(value)


def visible_prose(path: Path) -> str:
    parser = TextOnly()
    parser.feed(path.read_text(encoding="utf-8"))
    return "\n".join(parser.parts)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--chapter", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    source_dir = root / "textbook" / "part4" / args.chapter / "_src"
    sections: list[str] = []
    files: list[dict[str, str | int]] = []

    for path in sorted(source_dir.glob("[0-9][0-9]-*.html")):
        relative = path.relative_to(root)
        prose = visible_prose(path)
        sections.append(f"\n===== {relative.as_posix()} =====\n{prose}\n")
        files.append(
            {
                "path": relative.as_posix(),
                "source_sha256": sha256(path),
                "prose_characters": len(prose),
            }
        )

    text = "\n".join(sections)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    manifest = {
        "snapshot": args.output.name,
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "sections": len(files),
        "files": files,
        "note": "Read-only extraction. Code, preformatted output, scripts, styles, and notebook placeholders are excluded.",
    }
    manifest_path = args.output.with_suffix(".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
