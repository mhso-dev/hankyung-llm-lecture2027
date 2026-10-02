#!/usr/bin/env python3
"""Ch 9의 교재 코드·출력 블록이 실습 원본과 연결되었는지 확인합니다."""

from __future__ import annotations

import ast
import hashlib
import html
import json
import re
from pathlib import Path

CHAPTER = Path(__file__).resolve().parents[1]
SRC = CHAPTER / "_src"
LAB = CHAPTER.parents[2] / "labs" / "part3" / "ch09-rag-first-run"

SECTIONS = [
    "01-RAG-지도",
    "02-로더와-스플리터",
    "03-임베딩과-벡터스토어",
    "04-생성과-출처-인용",
    "05-첫-실패-보기",
    "06-실험-하네스",
    "07-RAG-실습",
]
PAGES = ["index", *SECTIONS]

PRESERVED_OUTPUTS = {
    "01-RAG-지도": ["ex01_rag_preserved.txt", "ex01_without_context_preserved.txt"],
    "02-로더와-스플리터": ["ex02.txt", "ex02_overlap_preserved.txt"],
    "03-임베딩과-벡터스토어": ["ex03_preserved.txt", "ex03_failure_preserved.txt"],
    "04-생성과-출처-인용": [
        "ex04_preserved.txt",
        "ex04_missing_tag_preserved.txt",
        "ex04_empty_hits_preserved.txt",
        "ex04_search_miss_preserved.txt",
    ],
    "05-첫-실패-보기": ["ex05_preserved.txt"],
    "06-실험-하네스": ["ex06_preserved.txt"],
}

PRE_RE = re.compile(r"<pre(?:\s+class=\"[^\"]*\")?>(.*?)</pre>", re.DOTALL)
CODE_RE = re.compile(r"^<code\s+class=\"[^\"]*\">(.*?)</code>$", re.DOTALL)
TOKEN_RE = re.compile(r"\{\{(code|output):([^}]+)\}\}")


def source_code(spec: str) -> str:
    filename, _, symbols_text = spec.partition("#")
    source = (LAB / filename).read_text(encoding="utf-8")
    if not symbols_text:
        return source.rstrip()

    tree = ast.parse(source)
    lines = source.splitlines()
    requested = set(symbols_text.split(","))
    selected: list[tuple[int, int]] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name not in requested:
                continue
            start = min([node.lineno, *(d.lineno for d in node.decorator_list)])
            selected.append((start, node.end_lineno or node.lineno))
    found = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and node.name in requested
    }
    if found != requested:
        raise AssertionError(f"찾을 수 없는 심볼: {spec} ({sorted(requested - found)})")
    return "\n\n\n".join("\n".join(lines[start - 1 : end]) for start, end in selected)


def visible_pre(block: str) -> str:
    code = CODE_RE.fullmatch(block)
    return html.unescape(code.group(1) if code else block).rstrip()


def check_reference_expansion() -> list[str]:
    """남아 있는 과거 code/output 참조가 정확히 확장되었는지 확인합니다."""
    checked: list[str] = []
    for slug in PAGES:
        source_text = (SRC / f"{slug}.html").read_text(encoding="utf-8")
        rendered_text = (CHAPTER / f"{slug}.html").read_text(encoding="utf-8")
        source_blocks = PRE_RE.findall(source_text)
        rendered_blocks = PRE_RE.findall(rendered_text)
        referenced_blocks = [block for block in source_blocks if TOKEN_RE.search(block)]
        for index, source_block in enumerate(referenced_blocks, start=1):
            match = TOKEN_RE.search(source_block)
            assert match
            kind, spec = match.groups()
            expected = (
                source_code(spec)
                if kind == "code"
                else (LAB / "runs" / "examples" / spec).read_text(encoding="utf-8").rstrip()
            )
            assert any(
                visible_pre(rendered_block) == expected for rendered_block in rendered_blocks
            ), f"{slug} pre #{index}: {spec} 불일치"
            checked.append(f"{slug}#{index}:{kind}:{spec}")
        assert "{{code:" not in rendered_text and "{{output:" not in rendered_text
    return checked


def check_preserved_outputs() -> list[str]:
    checked: list[str] = []
    for slug, filenames in PRESERVED_OUTPUTS.items():
        before = (CHAPTER / "qa" / "before" / f"{slug}.html").read_text(encoding="utf-8")
        old_outputs = [html.unescape(block).rstrip() for block in re.findall(
            r'<pre class="out">(.*?)</pre>', before, re.DOTALL
        )]
        saved_outputs = [
            (LAB / "runs" / "examples" / name).read_text(encoding="utf-8").rstrip()
            for name in filenames
        ]
        assert old_outputs == saved_outputs, f"{slug}: 보존 출력이 qa/before와 다릅니다"
        checked.extend(f"{slug}:{name}" for name in filenames)
    return checked


def check_output_manifest() -> list[str]:
    manifest_path = LAB / "runs" / "examples" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["algorithm"] == "sha256"
    checked: list[str] = []
    for entry in manifest["entries"]:
        path = LAB / "runs" / "examples" / entry["file"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == entry["sha256"], entry["file"]
        checked.append(entry["file"])
    assert len(checked) == sum(len(names) for names in PRESERVED_OUTPUTS.values())
    return checked


def main() -> None:
    references = check_reference_expansion()
    preserved = check_preserved_outputs()
    manifest = check_output_manifest()
    print(f"PASS: source/output references {len(references)} blocks")
    print(f"PASS: preserved output snapshots {len(preserved)} blocks")
    print(f"PASS: output manifest hashes {len(manifest)} files")


if __name__ == "__main__":
    main()
