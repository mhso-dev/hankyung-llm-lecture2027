#!/usr/bin/env python3
"""Collect selected Part 3 student prose for a read-only language audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path


class TextOnly(HTMLParser):
    """Extract visible prose while protecting code, output, and page machinery."""

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


def html_text(path: Path) -> str:
    parser = TextOnly()
    parser.feed(path.read_text(encoding="utf-8"))
    return "\n".join(parser.parts)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--include-revised",
        action="store_true",
        help="Include Ch 9 section 06 and Ch 10 section 08 after their revision is complete.",
    )
    parser.add_argument(
        "--chapter",
        action="append",
        help="Collect this Part 3 chapter slug. Repeat to collect multiple chapters.",
    )
    parser.add_argument(
        "--section",
        action="append",
        help="Collect only this two-digit section number. Repeat as needed.",
    )
    parser.add_argument(
        "--include-index",
        action="store_true",
        help="Include the selected chapter index pages.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    if args.chapter:
        chapters = {slug: set() for slug in args.chapter}
    else:
        chapters = {
            "ch09-rag-first-run": set()
            if args.include_revised
            else {"06-실험-하네스.html"},
            "ch10-document-processing": set()
            if args.include_revised
            else {"08-인덱싱-비교-실험.html"},
        }
    selected_sections = set(args.section or [])
    sections: list[str] = []
    files: list[dict[str, str | int]] = []

    for slug, excluded in chapters.items():
        source_dir = root / "textbook" / "part3" / slug / "_src"
        for path in sorted(source_dir.glob("[0-9][0-9]-*.html")):
            if path.name in excluded:
                continue
            if selected_sections and path.name[:2] not in selected_sections:
                continue
            relative = path.relative_to(root)
            prose = html_text(path)
            sections.append(f"\n===== {relative.as_posix()} =====\n{prose}\n")
            files.append(
                {
                    "path": relative.as_posix(),
                    "source_sha256": sha256(path),
                    "prose_characters": len(prose),
                }
            )

        if args.include_index:
            path = root / "textbook" / "part3" / slug / "index.html"
            relative = path.relative_to(root)
            prose = html_text(path)
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
        "excluded": []
        if args.chapter or args.include_revised
        else [
            "textbook/part3/ch09-rag-first-run/_src/06-실험-하네스.html",
            "textbook/part3/ch10-document-processing/_src/08-인덱싱-비교-실험.html",
        ],
        "files": files,
        "note": "Read-only extraction. Code, preformatted output, scripts, styles, and notebook placeholders are excluded.",
    }
    manifest_path = args.output.with_suffix(".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
