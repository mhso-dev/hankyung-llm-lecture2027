"""Ch 9 교재 빌드 — _src/*.html 본문 조각을 공통 골격(헤더·CSS·목차·hljs)에 끼우고
도식 SVG는 인라인, 삽화는 base64 JPEG로 심어 단일 파일 HTML을 만든다.

실행: python _build.py   (표준 라이브러리 + Pillow)
치환 토큰:
  {{svg:이름}}        figures/이름.svg 인라인
  {{img:이름|캡션}}   figures/이름.png → JPEG base64 <figure>
"""

from __future__ import annotations

import base64
import io
import re
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "_src"
FIG = HERE / "figures"

CHAPTER = "Ch 9 · RAG 첫 완주 + 실험 하네스"
SECTIONS = [
    ("01-RAG-지도", "01 · RAG 지도 — 검색으로 Select를 자동화한다"),
    ("02-로더와-스플리터", "02 · 로더와 스플리터 — PDF가 청크가 되기까지"),
    ("03-임베딩과-벡터스토어", "03 · 임베딩·벡터스토어·top-k 검색"),
    ("04-생성과-출처-인용", "04 · 생성과 출처 인용 — 첫 완주"),
    ("05-첫-실패-보기", "05 · 첫 실패를 일부러 보기"),
    ("06-실험-하네스", "06 · 실험 하네스 — 설정·실행·한 줄 기록"),
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
nav.toc{background:var(--paper);border:var(--border);border-radius:var(--radius-panel);padding:14px 18px;margin:0 0 32px;font-size:15px}
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
.look{font-size:15px;color:var(--g700);border-left:3px solid var(--clay);padding:4px 12px;margin:-8px 0 18px;background:var(--paper)}
.look b{color:#9E4527}
figure{margin:22px 0 26px;background:var(--paper);border:var(--border);border-radius:var(--radius-panel);padding:14px}
figure svg{width:100%;height:auto;display:block}
figure img{width:100%;height:auto;display:block;border-radius:8px}
figcaption{font-size:14px;color:var(--g700);margin-top:10px;line-height:1.6}
figcaption .gaze{display:block;color:var(--g500);margin-top:4px}
.tw{overflow-x:auto;margin:10px 0 20px}
table{border-collapse:collapse;width:100%;margin:0;font-size:15px;background:var(--paper)}
th,td{border:1px solid var(--g300);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--g100);font-weight:700}
.goal{background:var(--paper);border:var(--border);border-radius:var(--radius-panel);padding:14px 18px 6px}
.goal li{list-style:none;position:relative;padding-left:26px}
.goal li::before{content:"☐";position:absolute;left:0;color:var(--clay)}
.callout{border-radius:10px;padding:12px 16px;margin:14px 0 18px;border:1px solid;font-size:15.5px}
.callout.blue{background:var(--blue-bg);border-color:var(--blue)}
.callout.green{background:var(--green-bg);border-color:var(--green)}
.callout.yellow{background:var(--yellow-bg);border-color:var(--yellow)}
.callout.red{background:var(--red-bg);border-color:var(--red)}
.callout b:first-child{display:block;margin-bottom:4px}
.term{background:var(--paper);border:var(--border);border-radius:10px;padding:10px 16px;margin:10px 0 18px;font-size:15px}
.term dt{font-weight:700;margin-top:6px}
.term dd{margin:0 0 4px 0;color:var(--g700)}
details{border:var(--border);border-radius:var(--radius-panel);background:var(--paper);padding:0 18px;margin:14px 0 22px}
details summary{cursor:pointer;font-weight:700;padding:12px 0;list-style:none}
details summary::before{content:"▸ ";color:var(--clay)}
details[open] summary::before{content:"▾ "}
details.instructor{background:#f6f3ea;border-color:var(--oat)}
details.quiz{background:var(--paper)}
.quiz-q{margin:10px 0 4px;font-weight:700}
.quiz-a{color:var(--g700);font-size:15.5px;margin:0 0 12px;padding-left:14px;border-left:2px solid var(--oat)}
.nav-foot{display:flex;justify-content:space-between;gap:12px;margin-top:48px;padding-top:18px;border-top:var(--border);font-size:15px}
.tag{display:inline-block;font-size:14px;padding:1px 8px;border-radius:999px;background:var(--g100);color:var(--g700);vertical-align:middle;margin-left:4px}
.tbd{background:#fff3bf;border-bottom:2px dotted var(--yellow);padding:0 3px}
.file{font-family:var(--mono);font-size:14px;color:var(--g700);margin:-4px 0 6px}
@media (max-width:640px){body{font-size:16px}nav.toc ol{columns:1}h2{font-size:22px}}
@media print{body{background:#fff;color:#000;font-size:12pt}.page{max-width:none}pre{white-space:pre-wrap}details{page-break-inside:avoid}details summary::before{content:""}nav.toc{display:none}}
"""

HEAD = """<!doctype html><html lang="ko"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {chapter}</title>
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=Noto+Serif+KR:wght@400;700&family=JetBrains+Mono:wght@400;500&display=swap">
{hljs}
<style>{css}</style>
</head><body><div class="page">
<!-- 생성: _build.py · 원본 조각 _src/{slug}.html · 도식 figures/*.svg · 삽화 figures/*.png (Higgsfield nano_banana_pro, 2026-09-07) -->
<header class="top">
<p class="crumb">한경 KDT · LLM Agent 개발 &amp; 바이브코딩 · Part 3 RAG · {chapter}</p>
<h1>{title}</h1>
<div class="meta">{meta}</div>
</header>
"""

HLJS = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11/styles/github-dark.min.css">
<script src="https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11/highlight.min.js"></script>
<script>document.addEventListener("DOMContentLoaded",()=>{document.querySelectorAll("pre:not(.out) code").forEach(el=>hljs.highlightElement(el));});</script>"""

TOC_BLOCKS = ["학습 목표", "왜 지금 이것인가", "선수 지식 되짚기", "핵심 개념", "실행 예제",
              "일부러 실패해 보기", "주의할 점과 실무 메모", "정리와 다음 절", "복습 문제", "강사 노트", "참고 자료"]

FOOT = """
<div class="nav-foot"><span>{prev}</span><span><a href="index.html">챕터 목차</a></span><span>{next}</span></div>
</div></body></html>
"""


def inline_svg(name: str) -> str:
    svg = (FIG / f"{name}.svg").read_text(encoding="utf-8")
    return svg


def inline_img(name: str) -> str:
    im = Image.open(FIG / f"{name}.png").convert("RGB")
    im = im.resize((1100, int(1100 * im.size[1] / im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def render(slug: str, title: str, i: int) -> str:
    body = (SRC / f"{slug}.html").read_text(encoding="utf-8")
    body = re.sub(r"\{\{svg:([^}]+)\}\}", lambda m: inline_svg(m.group(1)), body)
    body = body.replace("<table>", "<div class=\"tw\"><table>").replace("</table>", "</table></div>")

    def img(m):
        name, alt = m.group(1), m.group(2)
        return f'<img src="{inline_img(name)}" alt="{alt}">'

    body = re.sub(r"\{\{img:([^|}]+)\|([^}]*)\}\}", img, body)
    meta_m = re.search(r"<!--meta:(.*?)-->", body, re.S)
    meta = ""
    if meta_m:
        meta = "".join(f"<span>{x.strip()}</span>" for x in meta_m.group(1).split("|"))
    toc = "<nav class='toc'><b>이 절의 구성</b><ol>" + "".join(
        f'<li><a href="#b{j + 1}">{t}</a></li>' for j, t in enumerate(TOC_BLOCKS)) + "</ol></nav>"
    prev = f'<a href="{SECTIONS[i - 1][0]}.html">← {SECTIONS[i - 1][1]}</a>' if i > 0 else "&nbsp;"
    nxt = f'<a href="{SECTIONS[i + 1][0]}.html">{SECTIONS[i + 1][1]} →</a>' if i + 1 < len(SECTIONS) else "챕터 끝"
    return (HEAD.format(title=title, chapter=CHAPTER, hljs=HLJS, css=CSS, slug=slug, meta=meta)
            + toc + body + FOOT.format(prev=prev, next=nxt))


INDEX_BODY = """
<h2><span class="no">Ch 9</span>챕터 개요</h2>
<p>목표는 하나입니다. <strong>이틀 안에 돌아가는 RAG를 만든다.</strong> 텍스트 로더 → 스플리터 → 임베딩 → 벡터스토어 → top-k 검색 → 출처 인용까지 평범한 파이썬 함수 다섯 개로 완주하고, 같은 시간에 실험 하네스(설정 YAML → 실행 → 한 줄 기록)를 만듭니다. 품질은 아직 측정하지도, 올리지도 않습니다. 첫 실패를 일부러 보고, 그것이 Ch 11(측정)·Ch 12(튜닝)·Ch 16(가드레일)의 동기가 되는 것까지가 이 챕터입니다.</p>
<div class="callout blue"><b>커리큘럼 두 규칙</b>① 이 챕터에 에이전트는 없습니다 — 검색 횟수·k·프롬프트·폴백은 전부 학생이 코드에 적고, 모델은 답 문장만 만듭니다. ② 측정이 튜닝보다 먼저입니다 — 하네스의 <code>metrics</code> 칸은 비어 있고 Ch 11이 채웁니다.</div>
<h2><span class="no">목표</span>챕터를 마치면</h2>
<div class="goal"><ul>
<li><code>labs/data/rag-corpus/</code>의 PDF 18건을 청크 176개로 색인하고, 질문 하나에 출처가 붙은 답을 받을 수 있습니다.</li>
<li>검색 결과 (청크, 점수)를 읽고 "검색이 틀렸나, 생성이 틀렸나"를 가릴 수 있습니다.</li>
<li>같은 출력 "문서에서 찾을 수 없습니다"가 두 가지 원인에서 나온다는 것을 설명하고, 정답 문서 ID가 왜 필요한지 말할 수 있습니다.</li>
<li><code>--set</code> 한 줄로 설정을 바꿔 실행하고 <code>runs.jsonl</code>에 한 줄이 남는 하네스를 돌릴 수 있습니다.</li>
</ul></div>
<h2><span class="no">절</span>구성 — 16h (강의 6 · 실습 10)</h2>
<div class="tw"><table>
<tr><th>절</th><th>개념</th><th>강의</th><th>실습</th><th>코드</th><th>도식·삽화</th></tr>
<tr><td><a href="01-RAG-지도.html">01 RAG 지도</a></td><td>Select의 자동화, 색인·질의 두 흐름, 학생/모델 경계, 문서 세트</td><td>1h</td><td>1h</td><td>—</td><td>파이프라인 도식 · 오픈북 삽화</td></tr>
<tr><td><a href="02-로더와-스플리터.html">02 로더와 스플리터</a></td><td>Document, 쪽 단위 로더, RecursiveCharacterTextSplitter, 겹침, 글자 vs 토큰</td><td>1h</td><td>2h</td><td><code>load_pdfs</code> <code>split_docs</code></td><td>청크 경계 도식</td></tr>
<tr><td><a href="03-임베딩과-벡터스토어.html">03 임베딩·벡터스토어·top-k</a></td><td>임베딩, 코사인 유사도, InMemoryVectorStore, dump/load, 점수 읽기</td><td>1h</td><td>2h</td><td><code>build_index</code> <code>search</code></td><td>벡터 검색 도식</td></tr>
<tr><td><a href="04-생성과-출처-인용.html">04 생성과 출처 인용</a></td><td>컨텍스트 조립, 시스템 프롬프트, 출처 태그, Answer, 첫 완주</td><td>1h</td><td>2h</td><td><code>format_context</code> <code>generate</code> <code>answer</code></td><td>—</td></tr>
<tr><td><a href="05-첫-실패-보기.html">05 첫 실패를 일부러 보기</a></td><td>환각의 조건, 거부, unanswerable, 확률적 실패, 같은 출력·다른 원인</td><td>1h</td><td>2h</td><td><code>examples/ex05_failure.py</code> <code>prompts.py</code></td><td>실패 경로 도식 · 안내원 삽화</td></tr>
<tr><td><a href="06-실험-하네스.html">06 실험 하네스</a></td><td>config.yaml, --set, 설정 해시 캐시, runs.jsonl 한 줄, 눈으로 비교의 한계</td><td>1h</td><td>1h</td><td><code>harness.py</code> <code>config.yaml</code></td><td>하네스 루프 도식 · 실험 노트 삽화</td></tr>
</table></div>
<h2><span class="no">준비</span>실습 환경</h2>
<pre><code class="language-bash">cd labs/part3/ch09-rag-first-run
uv sync            # Python 3.12 · langchain 1.4 · langchain-openai 1.6 · pypdf 6 · pyyaml
uv run pytest -q   # 10 passed</code></pre>
<p><code>OPENAI_API_KEY</code>는 프로젝트 루트 <code>.env</code>에 둡니다. 임베딩 모델은 <span class="tbd">[[미정: 임베딩 모델]]</span> 확정 전까지 <code>text-embedding-3-small</code>, 생성 모델은 <code>gpt-5.4-mini</code>입니다. 챕터 전체 실행 비용은 미화 0.2달러 미만입니다.</p>
<h2><span class="no">연결</span>이 챕터가 만든 것 · 다음 챕터로 넘기는 것</h2>
<div class="tw"><table>
<tr><th>만든 것</th><th>어디에서 다시 쓰이는가</th></tr>
<tr><td><code>rag.py</code> — <code>load_pdfs</code>·<code>split_docs</code>·<code>build_index</code>·<code>search</code>·<code>format_context</code>·<code>generate</code>·<code>answer</code></td><td>Ch 10(로더·청킹 교체) · Ch 12(<code>search</code> 내부를 하이브리드·리랭킹으로) · Ch 13(각 함수가 그래프 노드로)</td></tr>
<tr><td><code>Document.metadata</code>의 <code>doc_id</code>·<code>page</code>·<code>chunk_id</code></td><td>Ch 11(정답 문서 ID 비교) · Ch 12(pgvector 컬럼·메타데이터 필터)</td></tr>
<tr><td>출처 태그 형식 <code>[doc_id p.페이지]</code></td><td>Ch 11("무엇을 맞다고 볼지" 합의) · Ch 16(출력 검증) · 중간 프로젝트 요건</td></tr>
<tr><td><code>harness.py</code> + <code>config.yaml</code> + <code>runs/runs.jsonl</code>(<code>metrics: {}</code>)</td><td>Ch 10 실습(3 청킹 × 2 임베딩) · Ch 11(지표 함수가 <code>metrics</code>를 채움) · Ch 12(실험 로그 30건) · Ch 15(judge·p95)</td></tr>
<tr><td><code>prompts.py</code>의 <code>strict</code>·<code>helpful</code></td><td>Ch 16(프롬프트 규칙의 한계 → 가드레일) · Ch 22(Middleware)</td></tr>
<tr><td>실패 사례 — 검색 실패, 확률적 환각, 부칙 누락 오답, 문서 속 지시문</td><td>Ch 11·12·15·16의 첫 문장</td></tr>
</table></div>
<p>새 용어(챕터 전체 30개 이내): RAG, 색인, 청크, 벡터스토어, top-k, 출처 인용, Document, 로더, 스플리터, chunk_size·chunk_overlap, separators, 임베딩, 코사인 유사도, 질문 임베딩, dump/load, 컨텍스트 조립, 시스템 프롬프트, usage_metadata, 환각, 거부, unanswerable, 확률적 실패, 실험 하네스, 설정 파일, run_id, 설정 해시, JSONL.</p>
"""


def render_index() -> str:
    meta = "".join(f"<span>{x}</span>" for x in ["16h", "강의 6h · 실습 10h", "절 6개", "W4~W5", "코드 labs/part3/ch09-rag-first-run"])
    body = INDEX_BODY.replace("<table>", "<table>")  # 이미 .tw로 감쌈
    foot = FOOT.format(prev="&nbsp;", next=f'<a href="{SECTIONS[0][0]}.html">{SECTIONS[0][1]} →</a>')
    return HEAD.format(title="Ch 9 · RAG 첫 완주 + 실험 하네스", chapter="Part 3 RAG", hljs=HLJS, css=CSS,
                       slug="index", meta=meta) + body + foot


if __name__ == "__main__":
    (HERE / "index.html").write_text(render_index(), encoding="utf-8")
    print("wrote index.html")
    for i, (slug, title) in enumerate(SECTIONS):
        if not (SRC / f"{slug}.html").exists():
            print("skip (no src):", slug)
            continue
        out = HERE / f"{slug}.html"
        out.write_text(render(slug, title, i), encoding="utf-8")
        print("wrote", out.name, f"{out.stat().st_size // 1024} KB")
