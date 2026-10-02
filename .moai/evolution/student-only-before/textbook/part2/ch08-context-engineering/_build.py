"""Ch 8 교재 빌드 — _src/*.html 본문 조각을 공통 골격(헤더·CSS·목차·hljs)에 끼우고
도식 SVG는 인라인, 삽화는 base64 JPEG로 심어 단일 파일 HTML을 만든다.

실행: python _build.py   (표준 라이브러리 + Pillow)
치환 토큰:
  {{svg:이름}}        figures/이름.svg 인라인
  {{img:이름|캡션}}   figures/이름.png → JPEG base64 <figure>
"""

from __future__ import annotations

import ast
import base64
import html
import io
import re
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_notebook"))
from render import CSS as NOTEBOOK_CSS
from render import SCRIPT as NOTEBOOK_SCRIPT
from render import expand_notebooks

SRC = HERE / "_src"
FIG = HERE / "figures"
LAB = HERE.parents[2] / "labs" / "part2" / "ch08-context-engineering"

CHAPTER = "Ch 8 · Context Engineering 기초"
SECTIONS = [
    ("01-컨텍스트와-토큰-예산", "01 · 컨텍스트와 토큰 예산"),
    ("02-Write와-Select", "02 · Write와 Select"),
    ("03-Compress와-Isolate", "03 · Compress와 Isolate"),
    ("04-네-가지-실패-모드", "04 · 네 가지 실패 모드"),
    ("05-Context-rot-측정", "05 · Context rot 측정"),
    ("06-단계적-공개와-설계-비교", "06 · 단계적 공개와 설계 비교"),
]

CSS = """
:root{--ivory:#FAF9F5;--paper:#FFFFFF;--slate:#141413;--clay:#D97757;--clay-d:#B85C3E;--oat:#E3DACC;
--olive:#788C5D;--g100:#F0EEE6;--g300:#D1CFC5;--g500:#5F5E57;--g700:#3D3D3A;
--sans:"Noto Sans KR","Pretendard",system-ui,-apple-system,sans-serif;
--serif:"Noto Serif KR","Pretendard",ui-serif,Georgia,serif;
--mono:"JetBrains Mono",ui-monospace,"SF Mono",Menlo,Consolas,monospace;
--max-width:860px;--radius-panel:12px;--border:1.5px solid var(--g300);
--blue:#4a9eed;--blue-bg:#eaf4ff;--purple:#8b5cf6;--green:#22c55e;--green-bg:#edfbef;--yellow:#f59e0b;--yellow-bg:#fff8e6;--red:#ef4444;--red-bg:#fff0f0}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--ivory);color:var(--slate);font-family:var(--sans);font-size:17px;line-height:1.75;word-break:keep-all}
a{color:#9E4527;overflow-wrap:anywhere}
.page{max-width:var(--max-width);margin:0 auto;padding:32px 24px 96px}
header.top{border-bottom:var(--border);padding-bottom:20px;margin-bottom:24px}
header.top .crumb{font-size:14px;color:var(--g500);margin:0 0 6px}
header.top h1{font-family:var(--serif);font-size:30px;line-height:1.3;margin:0 0 10px;letter-spacing:-0.01em}
header.top .meta{font-size:14px;color:var(--g700);display:flex;gap:14px;flex-wrap:wrap}
header.top .meta span{background:var(--g100);padding:3px 10px;border-radius:999px}
nav.toc{background:var(--paper);border:var(--border);border-radius:var(--radius-panel);padding:14px 18px;margin:0 0 32px;font-size:16px}
nav.toc b{display:block;margin-bottom:6px;color:var(--g700)}
nav.toc ol{margin:0;padding-left:20px;columns:2;column-gap:24px}
nav.toc li{margin:2px 0}
h2{font-family:var(--serif);font-size:24px;margin:48px 0 14px;padding-top:14px;border-top:var(--border);letter-spacing:-0.01em}
h2 .no{display:inline-block;min-width:34px;color:#9E4527;font-family:var(--mono);font-size:16px;margin-right:6px}
h3{font-size:19px;margin:30px 0 10px}
h4{font-size:17px;margin:22px 0 8px;color:var(--g700)}
p{margin:0 0 14px}
ul,ol{margin:0 0 14px;padding-left:24px}
li{margin:4px 0}
strong{color:var(--slate)}
code{font-family:var(--mono);font-size:max(14px,0.9em);background:var(--g100);padding:1px 5px;border-radius:4px;overflow-wrap:anywhere}
pre{background:#1f1f1d;color:#f1efe8;border-radius:10px;padding:16px 18px;overflow-x:auto;font-size:14px;line-height:1.6;margin:10px 0 18px}
pre code{background:transparent;padding:0;color:inherit;font-size:inherit}
pre.out{background:var(--g100);color:var(--slate);border:1px dashed var(--g300);font-size:14px}
pre.out::before{content:"실행 결과";display:block;font-family:var(--sans);font-size:14px;color:var(--g700);margin-bottom:6px}
.look{font-size:16px;color:var(--g700);border-left:3px solid var(--clay);padding:4px 12px;margin:-8px 0 18px;background:var(--paper)}
.look b{color:#9E4527}
figure{margin:22px 0 26px;background:var(--paper);border:var(--border);border-radius:var(--radius-panel);padding:14px}
figure .diagram{overflow-x:auto}figure svg{width:760px;max-width:none;height:auto;display:block}
figure img{width:100%;height:auto;display:block;border-radius:8px}
figcaption{font-size:14px;color:var(--g700);margin-top:10px;line-height:1.6}
figcaption .gaze{display:block;color:var(--g500);margin-top:4px}
.tw{overflow-x:auto;margin:10px 0 20px}
table{border-collapse:collapse;width:100%;margin:0;font-size:16px;background:var(--paper)}
th,td{border:1px solid var(--g300);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--g100);font-weight:700}
.goal{background:var(--paper);border:var(--border);border-radius:var(--radius-panel);padding:14px 18px 6px}
.goal li{list-style:none;position:relative;padding-left:26px}
.goal li::before{content:"☐";position:absolute;left:0;color:var(--clay)}
.callout{border-radius:10px;padding:12px 16px;margin:14px 0 18px;border:1px solid;font-size:16px}
.callout.blue{background:var(--blue-bg);border-color:var(--blue)}
.callout.green{background:var(--green-bg);border-color:var(--green)}
.callout.yellow{background:var(--yellow-bg);border-color:var(--yellow)}
.callout.red{background:var(--red-bg);border-color:var(--red)}
.callout b:first-child{display:block;margin-bottom:4px}
.term{background:var(--paper);border:var(--border);border-radius:10px;padding:10px 16px;margin:10px 0 18px;font-size:16px}
.term dt{font-weight:700;margin-top:6px}
.term dd{margin:0 0 4px 0;color:var(--g700)}
details{border:var(--border);border-radius:var(--radius-panel);background:var(--paper);padding:0 18px;margin:14px 0 22px}
details summary{cursor:pointer;font-weight:700;padding:12px 0;list-style:none}
details summary::before{content:"▸ ";color:var(--clay)}
details[open] summary::before{content:"▾ "}
details.instructor{background:#f6f3ea;border-color:var(--oat)}
details.quiz{background:var(--paper)}
.quiz-q{margin:10px 0 4px;font-weight:700}
.quiz-a{color:var(--g700);font-size:16px;margin:0 0 12px;padding-left:14px;border-left:2px solid var(--oat)}
.nav-foot{display:flex;justify-content:space-between;gap:12px;margin-top:48px;padding-top:18px;border-top:var(--border);font-size:16px}
.tag{display:inline-block;font-size:14px;padding:1px 8px;border-radius:999px;background:var(--g100);color:var(--g700);vertical-align:middle;margin-left:4px}
.tbd{background:#fff3bf;border-bottom:2px dotted var(--yellow);padding:0 3px}
.file{font-family:var(--mono);font-size:14px;color:var(--g700);margin:-4px 0 6px}
@media (max-width:640px){body{font-size:16px}nav.toc ol{columns:1}h2{font-size:22px}}
@media (max-width:640px){.page{padding:24px 18px 64px}.nav-foot{flex-wrap:wrap}.nav-foot span{min-width:0;max-width:100%}}
@media print{figure svg{width:100%;max-width:100%}body{background:#fff;color:#000;font-size:12pt}.page{max-width:none}pre{white-space:pre-wrap}details{page-break-inside:avoid}details summary::before{content:""}nav.toc{display:none}}
"""

CSS += "\n" + NOTEBOOK_CSS

HEAD = """<!doctype html><html lang="ko"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {chapter}</title>
<style id="chapter-styles">{css}</style>
{hljs}
</head><body><div class="page">
<!-- 생성: _build.py · 원본 조각 _src/{slug}.html · 도식 figures/*.svg · 삽화 figures/*.png (Higgsfield, 요청 nano_banana_pro·완료 nano_banana_2, 2026-09-08) -->
<header class="top">
<p class="crumb">한경 KDT · LLM Agent 개발 &amp; 바이브코딩 · Part 2 LLM 기초 · {chapter}</p>
<h1>{title}</h1>
<div class="meta">{meta}</div>
</header>
"""

HLJS = """<script>
// 본문과 기본 서식은 외부 서버 연결 없이 표시합니다.
window.addEventListener("load", () => {
  const addStylesheet = (href) => {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = href;
    document.head.appendChild(link);
  };
  addStylesheet("https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=Noto+Serif+KR:wght@400;700&family=JetBrains+Mono:wght@400;500&display=swap");
  const script = document.createElement("script");
  script.src = "https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11/highlight.min.js";
  script.async = true;
  script.onload = () => {
    if (!window.hljs) return;
    addStylesheet("https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11/styles/github.min.css");
    document.querySelectorAll("pre:not(.out) code").forEach(el => hljs.highlightElement(el));
  };
  document.head.appendChild(script);
}, {once: true});
</script>"""

TOC_BLOCKS = ["학습 목표", "왜 지금 이것인가", "선수 지식 되짚기", "핵심 개념", "실행 예제",
              "일부러 실패해 보기", "주의할 점과 실무 메모", "정리와 다음 절", "복습 문제", "강사 노트", "참고 자료"]

FOOT = NOTEBOOK_SCRIPT.replace("{", "{{").replace("}", "}}") + """
<div class="nav-foot"><span>{prev}</span><span><a href="index.html">챕터 목차</a></span><span>{next}</span></div>
</div></body></html>
"""


def inline_svg(name: str) -> str:
    svg = (FIG / f"{name}.svg").read_text(encoding="utf-8")
    return '<div class="diagram" tabindex="0" aria-label="도식: 가로로 이동하여 전체 보기">' + svg + "</div>"


def inline_img(name: str) -> str:
    im = Image.open(FIG / f"{name}.png").convert("RGB")
    im = im.resize((1100, int(1100 * im.size[1] / im.size[0])), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def inline_code(path: str, function: str | None = None) -> str:
    source = (LAB / path).read_text(encoding="utf-8")
    if function:
        node = next(n for n in ast.parse(source).body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                    and n.name == function)
        start = min([node.lineno] + [d.lineno for d in node.decorator_list])
        source = "\n".join(source.splitlines()[start - 1:node.end_lineno]) + "\n"
    reference = path + (":" + function if function else "")
    return (f'<pre><code class="language-python" data-source="{html.escape(reference)}">'
            + html.escape(source) + "</code></pre>")


def inline_output(path: str) -> str:
    return (f'<pre class="out" data-output="{html.escape(path)}">'
            + html.escape((LAB / path).read_text(encoding="utf-8")) + "</pre>")


def render(slug: str, title: str, i: int) -> str:
    body = (SRC / f"{slug}.html").read_text(encoding="utf-8")
    body = expand_notebooks(body, LAB)
    body = re.sub(r"\{\{code:([^}:]+)(?::([^}]+))?\}\}", lambda m: inline_code(m.group(1), m.group(2)), body)
    body = re.sub(r"\{\{output:([^}]+)\}\}", lambda m: inline_output(m.group(1)), body)
    body = re.sub(r"\{\{svg:([^}]+)\}\}", lambda m: inline_svg(m.group(1)), body)
    body = body.replace("<table>", "<div class=\"tw\"><table>").replace("</table>", "</table></div>")

    def img(m):
        name, alt = m.group(1), m.group(2)
        return f'<img src="{inline_img(name)}" alt="{alt}">'

    body = re.sub(r"\{\{img:([^|}]+)\|([^}]*)\}\}", img, body)
    meta_m = re.search(r"<!--meta:(.*?)-->", body, re.DOTALL)
    meta = ""
    if meta_m:
        meta = "".join(f"<span>{x.strip()}</span>" for x in meta_m.group(1).split("|") if not x.strip().startswith("코드"))
    toc = "<nav class='toc'><b>이 절의 구성</b><ol>" + "".join(
        f'<li><a href="#b{j + 1}">{t}</a></li>' for j, t in enumerate(TOC_BLOCKS)) + "</ol></nav>"
    prev = f'<a href="{SECTIONS[i - 1][0]}.html">← {SECTIONS[i - 1][1]}</a>' if i > 0 else "&nbsp;"
    nxt = f'<a href="{SECTIONS[i + 1][0]}.html">{SECTIONS[i + 1][1]} →</a>' if i + 1 < len(SECTIONS) else "챕터 끝"
    return (HEAD.format(title=title, chapter=CHAPTER, hljs=HLJS, css=CSS, slug=slug, meta=meta)
            + toc + body + FOOT.format(prev=prev, next=nxt))


INDEX_BODY = (SRC / "index-body.html").read_text(encoding="utf-8")


def render_index() -> str:
    meta = "".join(f"<span>{x}</span>" for x in ["16h", "강의 6h · 실습 10h", "절 6개", "Jupyter Notebook"])
    body = INDEX_BODY.replace("<table>", "<table>")  # 이미 .tw로 감쌈
    foot = FOOT.format(prev="&nbsp;", next=f'<a href="{SECTIONS[0][0]}.html">{SECTIONS[0][1]} →</a>')
    return HEAD.format(title=CHAPTER, chapter="Ch 8 · 챕터 목차", hljs=HLJS, css=CSS,
                       slug="index", meta=meta) + body + foot


if __name__ == "__main__":
    (HERE / "index.html").write_text(render_index(), encoding="utf-8")
    print("wrote index.html")
    for i, (slug, title) in enumerate(SECTIONS):
        if not (SRC / f"{slug}.html").exists():
            raise FileNotFoundError(SRC / f"{slug}.html")
        out = HERE / f"{slug}.html"
        out.write_text(render(slug, title, i), encoding="utf-8")
        print("wrote", out.name, f"{out.stat().st_size // 1024} KB")
