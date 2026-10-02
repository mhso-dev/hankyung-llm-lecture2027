"""Build a chapter from chapter.json with the shared verified-notebook renderer."""

from __future__ import annotations

import base64
import html
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
NOTEBOOK_RUNTIME = HERE.parent / "_notebook"
if str(NOTEBOOK_RUNTIME) not in sys.path:
    sys.path.insert(0, str(NOTEBOOK_RUNTIME))

from render import CSS as NOTEBOOK_CSS
from render import SCRIPT as NOTEBOOK_SCRIPT
from render import expand_notebooks

PLACEHOLDER = "[[작성:"
TOC_BLOCKS = [
    "학습 목표", "이 내용을 배우는 이유", "앞에서 배운 내용", "핵심 개념", "실행 예제",
    "일부러 실패해 보기", "주의할 점과 실무 메모", "정리와 다음 절", "복습 문제", "참고 자료",
]
BASE_CSS = (HERE / "chapter.css").read_text(encoding="utf-8")
CSS = BASE_CSS + "\n" + NOTEBOOK_CSS
HLJS = """<script>
window.addEventListener("load", () => {
  const addCss = href => { const link = document.createElement("link"); link.rel = "stylesheet"; link.href = href; document.head.appendChild(link); };
  addCss("https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=Noto+Serif+KR:wght@400;700&family=JetBrains+Mono:wght@400;500&display=swap");
  const script = document.createElement("script");
  script.src = "https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11/highlight.min.js";
  script.async = true;
  script.onload = () => {
    if (!window.hljs) return;
    addCss("https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11/styles/github.min.css");
    document.querySelectorAll("pre:not(.out) code").forEach(el => hljs.highlightElement(el));
  };
  document.head.appendChild(script);
}, {once: true});
</script>"""


def _inside(root: Path, relative: str) -> Path:
    if Path(relative).is_absolute():
        raise ValueError("Configured paths must be relative to the project root")
    target = (root / relative).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("Configured path escapes the project root") from exc
    return target


def _load_config(chapter_dir: Path, root: Path) -> dict:
    path = chapter_dir / "chapter.json"
    config = json.loads(path.read_text(encoding="utf-8"))
    if PLACEHOLDER in json.dumps(config, ensure_ascii=False):
        raise ValueError("chapter.json contains unfinished [[작성: ...]] fields")
    required = {"part", "part_title", "chapter", "title", "hours", "objectives", "lab_path", "sections"}
    missing = required - config.keys()
    if missing:
        raise ValueError(f"chapter.json missing fields: {sorted(missing)}")
    _inside(root, config["lab_path"])
    if not config["sections"]:
        raise ValueError("chapter.json requires at least one section")
    seen: set[str] = set()
    seen_numbers: set[str] = set()
    for section in config["sections"]:
        if set(section) != {"slug", "title", "format"}:
            raise ValueError("each section requires only slug, title, and format")
        slug = section["slug"]
        if not re.fullmatch(r"\d{2}-[0-9A-Za-z가-힣][0-9A-Za-z가-힣_-]*", slug):
            raise ValueError(f"invalid section slug: {slug!r}")
        if slug in seen:
            raise ValueError(f"duplicate section slug: {slug!r}")
        seen.add(slug)
        number = slug.split("-", 1)[0]
        if number in seen_numbers:
            raise ValueError(f"duplicate section number: {number!r}")
        seen_numbers.add(number)
        if section["format"] not in {"paired", "experiment"}:
            raise ValueError(f"invalid lesson format: {section['format']!r}")
    return config


def _assert_publishable(body: str, slug: str) -> None:
    if PLACEHOLDER in body:
        raise ValueError(f"{slug}: source contains unfinished [[작성: ...]] fields")
    if "강사 노트" in body or 'class="instructor"' in body or "class='instructor'" in body:
        raise ValueError(f"{slug}: student lesson must not contain instructor notes")


def _inline_svg(figures: Path, name: str) -> str:
    svg = (figures / f"{name}.svg").read_text(encoding="utf-8")
    return '<div class="diagram" tabindex="0" aria-label="도식: 가로로 이동하여 전체 보기">' + svg + "</div>"


def _inline_img(figures: Path, name: str, alt: str) -> str:
    alt, _, caption = alt.partition("|")
    image = Image.open(figures / f"{name}.png").convert("RGB")
    image = image.resize((1100, int(1100 * image.height / image.width)), Image.Resampling.LANCZOS)
    buffer = io.BytesIO()
    image.save(buffer, "JPEG", quality=82, optimize=True)
    data = base64.b64encode(buffer.getvalue()).decode()
    tag = f'<img src="data:image/jpeg;base64,{data}" alt="{html.escape(alt)}">'
    if not caption:
        return tag
    return f'<figure class="illustration">{tag}<figcaption>{caption}</figcaption></figure>'


def _inline_mermaid(figures: Path, spec: str) -> str:
    """{{mermaid:이름|대체 텍스트|캡션}} — render_mermaid.py 가 만든 SVG를 넣는다."""
    name, _, rest = spec.partition("|")
    alt, _, caption = rest.partition("|")
    svg = (figures / f"{name}.svg").read_text(encoding="utf-8")
    viewbox = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', svg)
    width = min(760, round(float(viewbox[1]))) if viewbox else 760
    svg = re.sub(r'<svg\b', f'<svg role="img" aria-label="{html.escape(alt)}"', svg, count=1)
    svg = re.sub(r'(<svg\b[^>]*?)\swidth="[^"]*"', r'\1', svg, count=1)
    svg = re.sub(r'(<svg\b[^>]*?)\sstyle="[^"]*"', r'\1', svg, count=1)
    svg = svg.replace("<svg ", f'<svg style="width:{width}px;max-width:none;height:auto" ', 1)
    figcaption = f"<figcaption>{caption}</figcaption>" if caption else ""
    return ('<figure class="mmd"><div class="diagram" tabindex="0" aria-label="도식: 가로로 이동하여 전체 보기">'
            + svg + "</div>" + figcaption + "</figure>")


def _wrap_tables(body: str) -> str:
    pattern = r'(?<!<div class="tw">)(<table\b[^>]*>.*?</table>)'
    return re.sub(pattern, r'<div class="tw">\1</div>', body, flags=re.DOTALL)


def _head(title: str, config: dict, meta: str) -> str:
    number = re.match(r"ch(\d+)-", config["chapter"])
    chapter_label = f"Ch {int(number.group(1))}" if number else config["chapter"]
    chapter = f"{chapter_label} · {config['title']}"
    return f"""<!doctype html><html lang="ko"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — {html.escape(chapter)}</title>
<style id="chapter-styles">{CSS}</style>{HLJS}</head><body><div class="page">
<header class="top"><p class="crumb">한경 KDT · LLM Agent 개발 &amp; 바이브코딩 · {html.escape(config['part_title'])} · {html.escape(chapter)}</p>
<h1>{html.escape(title)}</h1><div class="meta">{meta}</div></header>"""


def _footer(previous: str, following: str) -> str:
    return NOTEBOOK_SCRIPT + f'<div class="nav-foot"><span>{previous}</span><span><a href="index.html">챕터 목차</a></span><span>{following}</span></div></div></body></html>'


def _render_section(chapter_dir: Path, lab: Path, config: dict, section: dict, index: int) -> str:
    slug = section["slug"]
    body = (chapter_dir / "_src" / f"{slug}.html").read_text(encoding="utf-8")
    _assert_publishable(body, slug)
    expected = section["format"]
    notebook = json.loads((lab / "notebooks" / f"{slug}.ipynb").read_text(encoding="utf-8"))
    if PLACEHOLDER in json.dumps(notebook, ensure_ascii=False):
        raise ValueError(f"{slug}: notebook contains unfinished [[작성: ...]] fields")
    actual = notebook.get("metadata", {}).get("lesson_format", "paired")
    if actual != expected:
        raise ValueError(f"{slug}: chapter format {expected!r} does not match notebook {actual!r}")
    body = expand_notebooks(body, lab)
    _assert_publishable(body, slug)
    figures = chapter_dir / "figures"
    body = re.sub(r"\{\{svg:([^}]+)\}\}", lambda match: _inline_svg(figures, match[1]), body)
    body = re.sub(r"\{\{img:([^|}]+)\|([^}]*)\}\}", lambda match: _inline_img(figures, match[1], match[2]), body)
    body = re.sub(r"\{\{mermaid:([^}]+)\}\}", lambda match: _inline_mermaid(figures, match[1]), body)
    body = _wrap_tables(body)
    meta_match = re.search(r"<!--meta:(.*?)-->", body, re.DOTALL)
    meta = "" if not meta_match else "".join(
        f"<span>{html.escape(value.strip())}</span>"
        for value in meta_match[1].split("|")
        if value.strip() and not value.strip().startswith("코드")
    )
    titles = TOC_BLOCKS.copy()
    if expected == "experiment":
        titles[5] = "실험 결과 해석"
    toc = "<nav class='toc'><b>이 절의 구성</b><ol>" + "".join(f'<li><a href="#b{number}">{title}</a></li>' for number, title in enumerate(titles, 1)) + "</ol></nav>"
    sections = config["sections"]
    previous = "&nbsp;" if index == 0 else f'<a href="{sections[index - 1]["slug"]}.html">← {html.escape(sections[index - 1]["title"])}</a>'
    following = "챕터 끝" if index + 1 == len(sections) else f'<a href="{sections[index + 1]["slug"]}.html">{html.escape(sections[index + 1]["title"])} →</a>'
    return _head(section["title"], config, meta) + toc + body + _footer(previous, following)


def _render_index(config: dict) -> str:
    meta = "".join(f"<span>{html.escape(value)}</span>" for value in [config["hours"], f"절 {len(config['sections'])}개", "Jupyter Notebook"])
    goals = "".join(f"<li>{html.escape(goal)}</li>" for goal in config["objectives"])
    format_names = {"paired": "실패와 수정 비교", "experiment": "실험 결과 해석"}
    rows = "".join(
        f'<tr><td><a href="{section["slug"]}.html">{html.escape(section["title"])}</a></td>'
        f'<td>{format_names[section["format"]]}</td></tr>'
        for section in config["sections"]
    )
    body = f'<h2>챕터 개요</h2><div class="goal"><ul>{goals}</ul></div><h2>절 목록</h2><div class="tw"><table><tr><th>절</th><th>실습 형식</th></tr>{rows}</table></div>'
    first = config["sections"][0]
    return _head(config["title"], config, meta) + body + _footer("&nbsp;", f'<a href="{first["slug"]}.html">{html.escape(first["title"])} →</a>')


def build_chapter(chapter_dir: Path, *, root: Path | None = None) -> list[Path]:
    chapter_dir = chapter_dir.resolve()
    root = root.resolve() if root else chapter_dir.parents[2]
    try:
        chapter_dir.relative_to(root)
    except ValueError as exc:
        raise ValueError("chapter directory escapes the project root") from exc
    config = _load_config(chapter_dir, root)
    if chapter_dir.name != config["chapter"]:
        raise ValueError("chapter.json chapter does not match its directory")
    lab = _inside(root, config["lab_path"])
    rendered = [(chapter_dir / f"{section['slug']}.html", _render_section(chapter_dir, lab, config, section, index)) for index, section in enumerate(config["sections"])]
    rendered.insert(0, (chapter_dir / "index.html", _render_index(config)))
    for path, content in rendered:
        path.write_text(content, encoding="utf-8")
    return [path for path, _ in rendered]
