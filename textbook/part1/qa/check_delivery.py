"""Check Part 1 navigation, notebook correspondence, diagrams, and archives.

전체 마감 2026-10-01: 챕터 끝 실습 절과 그림 이름 규칙을 지금 구조에 맞게 고침 — 절 수 35 → 40(실습 절 5 포함),
실습 절(마지막 절 `NN-…-실습`)은 meta 「실습 30분」을 읽고 Part 시수 합(37h·59h)에는 넣지 않음(규격 §7-2),
절마다 그림 하나(.svg + .excalidraw) 대신 원고가 부르는 Mermaid 그림(.mmd → .svg·.png)이 절마다 3~5장(규격 §5-1)이고
원본과 렌더의 이름이 같아야 함. 옛 Ch 1~2 기준 파일과 달라진 것은 전처럼 `--revised-existing`으로 허용함.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
SECTIONS = 40  # 35절 + 챕터 끝 실습 절 5(2026-10-01)
sys.path.insert(0, str(ROOT / "textbook/_notebook"))
from execute import secret_values
from verify import verify_lesson


class Content(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.quizzes = 0
        self.visible: list[str] = []
        self.skip = 0
        self.summary = False
        self.summary_counted = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in ("script", "style", "code", "svg", "pre"):
            self.skip += 1
        if tag in ("a", "img"):
            self.links.append(values.get("href" if tag == "a" else "src") or "")
        if "quiz-q" in (values.get("class") or "").split():
            self.quizzes += 1
        if tag == "summary":
            self.summary = True
            self.summary_counted = False

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "code", "svg", "pre"):
            self.skip -= 1
        if tag == "summary":
            self.summary = False

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.visible.append(data)
        if self.summary and not self.summary_counted and re.match(r"(?:문제\s*)?\d+[.)\s]", data.strip()):
            self.quizzes += 1
            self.summary_counted = True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revised-existing', action='store_true',
                        help='Allow requested revisions to the historical Ch 1–2 baseline.')
    parser.add_argument('--output', type=Path,
                        help='Write a new verification record without replacing historical results.')
    args = parser.parse_args()
    part = ROOT / "textbook/part1"
    chapters = sorted(path for path in part.glob("ch*") if (path / "chapter.json").is_file())
    assert len(chapters) == 5
    pages = [part / "index.html", ROOT / "textbook/index.html"]
    lessons, prose, diagrams, hours = [], [], [], []
    for chapter in chapters:
        config = json.loads((chapter / "chapter.json").read_text())
        pages.append(chapter / "index.html")
        lecture = practice = 0.0
        diagrams_by_section = {}
        for index, section in enumerate(config["sections"]):
            slug = section["slug"]
            page = chapter / f"{slug}.html"
            notebook = ROOT / "labs/part1" / chapter.name / "notebooks" / f"{slug}.ipynb"
            lessons.append(verify_lesson(notebook, page))
            pages.append(page)
            source = (chapter / "_src" / f"{slug}.html").read_text()
            assert re.findall(r'<h2 id="b(\d+)"', source) == [str(i) for i in range(1, 11)]
            if index == len(config["sections"]) - 1 and slug.endswith("-실습"):
                # 챕터 끝 실습 절은 「실습 30분」으로 적고 챕터 시수에 더하지 않는다(규격 §7-2)
                assert re.search(r'실습\s*\d+\s*분', source), f"Missing section hours: {page}"
            else:
                timing = re.search(r'강의\s*([\d.]+)h\s*[|·]\s*실습\s*([\d.]+)h', source)
                assert timing, f"Missing section hours: {page}"
                lecture += float(timing[1])
                practice += float(timing[2])
            diagrams_by_section[slug] = re.findall(r'\{\{mermaid:([^|}]+)', source)
            assert 3 <= len(diagrams_by_section[slug]) <= 5, f"Mermaid diagrams per section: {page}"
            parser = Content()
            parser.feed(source)
            assert 3 <= parser.quizzes <= 5, f"Quiz count: {page}: {parser.quizzes}"
            visible = "".join(parser.visible)
            assert "[[작성:" not in source
            prose.append({"chapter": chapter.name, "section": slug,
                          "prose_chars": len(re.sub(r"\s", "", visible)),
                          "quiz_questions": parser.quizzes})
        # 원고가 부르는 Mermaid 그림마다 편집 원본(.mmd)과 렌더(.svg·.png)가 같은 이름으로 있어야 한다
        drawings = sorted((chapter / "figures").glob("[0-9]*.mmd"))
        svgs = [p.with_suffix(".svg") for p in drawings if p.with_suffix(".svg").is_file()]
        pngs = [p.with_suffix(".png") for p in drawings if p.with_suffix(".png").is_file()]
        referenced = {name for names in diagrams_by_section.values() for name in names}
        assert len(svgs) == len(pngs) == len(drawings) == len(referenced)
        assert {p.stem for p in drawings} == referenced
        diagrams.append({"chapter": chapter.name, "svg": len(svgs), "mmd": len(drawings), "png": len(pngs)})
        hours.append({"chapter": chapter.name, "lecture": lecture, "practice": practice})
    assert sum(row["lecture"] for row in hours) == 37
    assert sum(row["practice"] for row in hours) == 59
    baseline = json.loads((part / "qa/existing-chapters-baseline.json").read_text())
    unchanged = 0
    for entry in baseline:
        matches = hashlib.sha256((ROOT / entry["path"]).read_bytes()).hexdigest() == entry["sha256"]
        unchanged += int(matches)
        if not args.revised_existing:
            assert matches, entry["path"]
    credentials = [value.encode() for value in secret_values(ROOT)]
    missing, exposed = [], []
    links = 0
    for page in pages:
        data = page.read_bytes()
        if any(secret in data for secret in credentials):
            exposed.append(str(page.relative_to(ROOT)))
        parser = Content()
        parser.feed(data.decode())
        for href in parser.links:
            target = urlsplit(href)
            if target.scheme or target.netloc or not target.path:
                continue
            links += 1
            if not (page.parent / unquote(target.path)).resolve().exists():
                missing.append({"page": str(page.relative_to(ROOT)), "link": href})
    archives = []
    for filename in ("part1-practice.zip", "llm-practice.zip"):
        path = ROOT / "textbook/downloads" / filename
        with ZipFile(path) as archive:
            assert archive.testzip() is None
            names = archive.namelist()
            prefix = "part1-practice/" if filename.startswith("part1") else "llm-practice/"
            manifest = json.loads(archive.read(prefix + "manifest.json"))
            for entry in manifest:
                assert hashlib.sha256(archive.read(prefix + entry["path"])).hexdigest() == entry["sha256"]
                assert hashlib.sha256((ROOT / entry["path"]).read_bytes()).hexdigest() == entry["sha256"]
            for name in names:
                assert not {".env", ".venv", "__pycache__", ".git"}.intersection(Path(name).parts)
                if any(secret in archive.read(name) for secret in credentials):
                    exposed.append(f"{filename}:{name}")
            count = sum("/labs/part1/" in n and n.endswith(".ipynb") for n in names)
            assert count == SECTIONS
            archives.append({"file": filename, "entries": len(names), "part1_notebooks": count,
                             "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    assert len(lessons) == SECTIONS
    report = {"html_pages": len(pages), "notebooks": len(lessons),
              "code_cells": sum(row["code_cells"] for row in lessons),
              "max_cell_lines": max(row["max_cell_lines"] for row in lessons),
              "quiz_questions": sum(row["quiz_questions"] for row in prose),
              "local_links": links, "missing_links": missing, "exposed_credentials": exposed,
              "diagrams": diagrams, "hours": hours, "existing_files_unchanged": unchanged,
              "historical_baseline_files": len(baseline),
              "existing_revisions_allowed": args.revised_existing,
              "prose": prose, "archives": archives}
    destination = args.output or part / "qa/delivery-results.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    assert not missing and not exposed, f"See {destination}"
    print(json.dumps({key: value for key, value in report.items() if key != "prose"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
