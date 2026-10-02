# -*- coding: utf-8 -*-
"""RAG 실습 문서 세트 공통 렌더러 — HTML → PDF (weasyprint, Noto Sans CJK 임베딩)."""
from __future__ import annotations
import json, os, random, re
from pathlib import Path
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "pdf"
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_S = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"

BASE_CSS = f"""
@font-face {{ font-family: 'KR'; src: url('{FONT}'); font-weight: 400; }}
@font-face {{ font-family: 'KR'; src: url('{FONT_B}'); font-weight: 700; }}
@font-face {{ font-family: 'KRS'; src: url('{FONT_S}'); font-weight: 700; }}
@page {{ size: A4; margin: 24mm 22mm 24mm 22mm;
  @bottom-center {{ content: counter(page); font-family: 'KR'; font-size: 9pt; color: #666; }} }}
body {{ font-family: 'KR', sans-serif; font-size: 11pt; line-height: 1.8; color: #111; }}
h1 {{ font-size: 22pt; margin: 0 0 6pt; line-height: 1.3; }}
h2 {{ font-size: 15pt; margin: 18pt 0 6pt; border-bottom: 1.5px solid #333; padding-bottom: 3pt; }}
h3 {{ font-size: 12pt; margin: 12pt 0 4pt; }}
p {{ margin: 0 0 9pt; text-align: justify; }}
table {{ border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 9.5pt; page-break-inside: auto; }}
th, td {{ border: 1px solid #555; padding: 3pt 5pt; vertical-align: top; }}
th {{ background: #e8e8e8; }}
.small {{ font-size: 8.5pt; color: #444; }}
.box {{ border: 1px solid #333; padding: 8pt 10pt; margin: 8pt 0; background: #f7f7f7; }}
.cover {{ page-break-after: always; text-align: center; padding-top: 120pt; }}
.cover .org {{ font-size: 13pt; color: #444; margin-top: 30pt; }}
.pb {{ page-break-before: always; }}
ul, ol {{ margin: 0 0 8pt 0; }}
li {{ margin-bottom: 2pt; }}
.fn {{ font-size: 8.5pt; color: #333; border-top: 1px solid #999; margin-top: 10pt; padding-top: 4pt; }}
.right {{ text-align: right; }}
.center {{ text-align: center; }}
.toc li {{ list-style: none; }}
"""

def render(doc_id: str, tier: str, title: str, body_html: str, extra_css: str = "", meta: dict | None = None) -> Path:
    out_dir = PDF / tier
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{doc_id}.pdf"
    html = f"<html><head><meta charset='utf-8'><title>{title}</title><style>{BASE_CSS}{extra_css}</style></head><body>{body_html}</body></html>"
    (ROOT / "build" / "html").mkdir(exist_ok=True)
    (ROOT / "build" / "html" / f"{doc_id}.html").write_text(html, encoding="utf-8")
    HTML(string=html, base_url=str(ROOT / "build")).write_pdf(str(out))
    # 페이지 수 기록
    from pypdf import PdfReader
    n = len(PdfReader(str(out)).pages)
    m = {"doc_id": doc_id, "tier": tier, "title": title, "file": f"pdf/{tier}/{doc_id}.pdf", "pages": n}
    if meta: m.update(meta)
    mf = ROOT / "build" / "manifest_parts"
    mf.mkdir(exist_ok=True)
    (mf / f"{doc_id}.json").write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{tier}] {doc_id} {title} — {n}p")
    return out

def cover(title: str, org: str, sub: str = "", date: str = "") -> str:
    return f"<div class='cover'><h1>{title}</h1><p class='org'>{org}</p><p>{sub}</p><p class='small'>{date}</p></div>"

def table(headers: list[str], rows: list[list], cls: str = "") -> str:
    h = "".join(f"<th>{x}</th>" for x in headers)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table class='{cls}'><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>"

def hf_css(left: str, right: str) -> str:
    """머리글·바닥글 오염(청크에 섞여 들어오는 텍스트)용."""
    return f"""@page {{ @top-left {{ content: '{left}'; font-family:'KR'; font-size: 8pt; color:#777; }}
    @top-right {{ content: '{right}'; font-family:'KR'; font-size: 8pt; color:#777; }} }}"""

def rng(seed: int) -> random.Random:
    return random.Random(seed)

def won(n: int) -> str:
    return f"{n:,}원"
