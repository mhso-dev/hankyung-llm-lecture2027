"""Check published lessons, local links, archives, and preserved earlier sources.

전체 마감 2026-10-01: 앞 Part 원본 보존 대조의 기준 파일을 지금 구조에 맞게 바꿈 — 옛 `existing-artifacts-before.json`
(2026-09-11 Part 7 집필 전 Part 1~6 `_src`·노트북 376개)은 품질 개선으로 375개가 바뀌고 1개가 옮겨져 기준이 될 수 없어
그대로 두고, 같은 범위(Part 1~6 챕터 `_src/*.html`·`labs/part1~6/ch*/notebooks/*.ipynb`)를 전체 마감 때 다시 적은
`existing-artifacts-final-close.json`을 읽는다. 기준 파일은 묶음 재생성 뒤 `--write-baseline`으로 한 번만 만든다
(이미 있으면 덮어쓰지 않음, 없으면 대조 단계에서 멈춤).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
PART = ROOT / "textbook/part7"
BASELINE = PART / "qa/existing-artifacts-final-close.json"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and "href" in values:
            self.links.append(values["href"])


def earlier_sources():
    # 옛 existing-artifacts-before.json과 같은 범위: Part 1~6 챕터 _src/*.html과 실습 폴더 노트북
    paths = []
    for number in range(1, 7):
        paths += (ROOT / f"textbook/part{number}").glob("ch*/_src/*.html")
        paths += (ROOT / f"labs/part{number}").glob("ch*/notebooks/*.ipynb")
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(paths)}


def write_baseline():
    with BASELINE.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(earlier_sources(), ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {BASELINE.relative_to(ROOT)}: {len(json.loads(BASELINE.read_text()))} earlier sources")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-baseline", action="store_true",
                        help="Record the final-close baseline once (after bundle regeneration) and stop.")
    if parser.parse_args().write_baseline:
        write_baseline()
        return
    reports, broken = [], []
    for chapter in sorted(PART.glob("ch*/chapter.json")):
        config = json.loads(chapter.read_text())
        lab = ROOT / "labs/part7" / chapter.parent.name
        for section in config["sections"]:
            slug = section["slug"]
            source = (chapter.parent / "_src" / f"{slug}.html").read_text()
            page = chapter.parent / f"{slug}.html"
            body = page.read_text()
            nb = json.loads((lab / "notebooks" / f"{slug}.ipynb").read_text())
            assert "[[작성:" not in source and "[[작성:" not in json.dumps(
                nb, ensure_ascii=False
            ), slug
            blocks = re.findall(r"id=[\"\'](b\d+)[\"\']", source)
            assert all(f"b{n}" in blocks for n in range(1, 11)), (slug, blocks)
            assert "/Users/" not in body and "/private/tmp/" not in body, slug
            prose = re.sub(r"<[^>]+>", " ", source)
            codes = [c for c in nb["cells"] if c["cell_type"] == "code"]
            quiz = source.split('id="b9"')[1].split('id="b10"')[0]
            questions = quiz.count("quiz-q") or quiz.count("<details")
            assert 3 <= questions <= 5 and quiz.count("quiz-a") == questions, slug
            reports.append(
                {
                    "chapter": chapter.parent.name,
                    "section": slug,
                    "prose_characters": len(prose),
                    "code_cells": len(codes),
                    "review_questions": questions,
                    "execution": nb["metadata"]["verification"],
                }
            )
    for page in list(PART.glob("ch*/*.html")) + [PART / "index.html"]:
        parser = Links()
        parser.feed(page.read_text())
        for href in parser.links:
            url = urlsplit(href)
            if url.scheme or url.netloc or not url.path:
                continue
            target = page.parent / unquote(url.path)
            if not target.is_file():
                broken.append({"page": str(page.relative_to(ROOT)), "href": href})
    assert not broken, broken
    if not BASELINE.is_file():
        raise SystemExit(f"Missing {BASELINE.relative_to(ROOT)}: run --write-baseline after bundle regeneration")
    prior = json.loads(BASELINE.read_text())
    changed = [
        name
        for name, digest in prior.items()
        if not (ROOT / name).is_file()
        or hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest
    ]
    assert not changed, changed
    archives = []
    for name, prefix in [
        ("part7-practice.zip", "part7-practice/"),
        ("llm-practice.zip", "llm-practice/"),
    ]:
        path = ROOT / "textbook/downloads" / name
        with ZipFile(path) as archive:
            assert archive.testzip() is None
            manifest = json.loads(archive.read(prefix + "manifest.json"))
            for entry in manifest:
                data = archive.read(prefix + entry["path"])
                assert hashlib.sha256(data).hexdigest() == entry["sha256"], entry[
                    "path"
                ]
                assert data == (ROOT / entry["path"]).read_bytes(), entry["path"]
                assert Path(entry["path"]).name != ".env", entry["path"]
        archives.append(
            {
                "file": name,
                "files": len(manifest),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    output = {
        "sections": reports,
        "links_broken": broken,
        "earlier_sources_checked": len(prior),
        "earlier_sources_changed": changed,
        "archives": archives,
    }
    (PART / "qa/delivery-results.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2)
    )
    print(
        json.dumps(
            {
                "sections": len(reports),
                "code_cells": sum(x["code_cells"] for x in reports),
                "broken_links": len(broken),
                "earlier_sources_changed": len(changed),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
