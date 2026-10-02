"""6단계 삭제 목록 — 연결 폴더 안 작은 항목 후보와 참조 확인(읽기 전용, 결과는 6-docs/log 에만 씀)."""
import json, os, re, glob, zipfile
from pathlib import Path
ROOT = Path.home() / "mnt/한국경제신문"
os.chdir(ROOT)
W = ROOT / ".cache/final-close/6-docs/log"
EXCL_CH = {"ch32-docker", "ch33-cicd"}
SKIP_DIRS = {".venv", "node_modules", ".git"}
PRESERVE_PARTS = {"before", "probe", "review-pack"}   # 보존 폴더 안은 손대지 않음

def fsize(p):
    p = Path(p)
    if p.is_symlink() or p.is_file():
        return os.lstat(p).st_size, 1
    tot = n = 0
    for dp, dn, fn in os.walk(p):
        for f in fn:
            try:
                tot += os.lstat(os.path.join(dp, f)).st_size; n += 1
            except OSError:
                pass
    return tot, n

chapters = [Path(c) for c in sorted(glob.glob("textbook/part*/ch*")) if Path(c).name not in EXCL_CH]
# ---- 참조 말뭉치
corpus_src = {f: Path(f).read_text(errors="ignore") for f in glob.glob("textbook/part*/ch*/_src/*.html")}
corpus_html = {}
for f in glob.glob("textbook/**/*.html", recursive=True):
    if "/before" in f or "/_src/" in f or "/checks/" in f or "/qa/" in f:
        continue
    corpus_html[f] = Path(f).read_text(errors="ignore")
corpus_cap = {f: Path(f).read_text(errors="ignore") for f in glob.glob("textbook/**/*.caption.md", recursive=True) if "/before" not in f}
lists = {}
for pat in ("textbook/**/public-files.json", "textbook/**/prerequisite-files.json", "labs/**/public-files.json"):
    for f in glob.glob(pat, recursive=True):
        if "/before" in f or "/.venv/" in f:
            continue
        lists[f] = Path(f).read_text(errors="ignore")
zipnames = {}
for z in sorted(glob.glob("textbook/downloads/*.zip")):
    with zipfile.ZipFile(z) as zf:
        zipnames[z] = zf.namelist()

import unicodedata
NFC = lambda x: unicodedata.normalize("NFC", x)
def _tok(text, pat):
    return set(re.split(pat, NFC(text)))
TOK_NAME = {}   # group -> {token: [files]}
TOK_STEM = {}
for group, corpus in (("_src", corpus_src), ("html", corpus_html), ("caption", corpus_cap), ("list", lists)):
    dn, ds = {}, {}
    for f, t in corpus.items():
        for tk in _tok(t, r"[^\w.\-]+"):
            dn.setdefault(tk, []).append(f)
        if group in ("_src", "html"):
            for tk in _tok(t, r"[^\w\-]+"):
                ds.setdefault(tk, []).append(f)
    TOK_NAME[group], TOK_STEM[group] = dn, ds
ZIP_BASE = {}
for z, names in zipnames.items():
    for n in names:
        ZIP_BASE.setdefault(NFC(n.rsplit("/", 1)[-1]), set()).add(z)

def _chdir_of(f):
    parts = Path(f).parts
    return "/".join(parts[:3]) if len(parts) >= 3 and parts[0] == "textbook" and parts[2].startswith("ch") else None

CORPUS_ALL = {"_src": corpus_src, "html": corpus_html, "caption": corpus_cap, "list": lists}
def refs_name(name, stem=None, figpath=None):
    """이름 토큰으로 후보를 찾고, 경로로 같은 그림을 가리키는지 확인(다른 챕터가 같은 이름의 제 그림을 부르는 경우는 뺌)."""
    name = NFC(name); hits = []
    figch = _chdir_of(figpath) if figpath else None
    chname = figch.split("/")[-1] if figch else None
    for group in TOK_NAME:
        cand = set(TOK_NAME[group].get(name, []))
        if stem and group in TOK_STEM:
            cand |= set(TOK_STEM[group].get(NFC(stem), []))
        for f in sorted(cand):
            if figpath is None:
                hits.append(f"{group}:{f}"); continue
            text = NFC(CORPUS_ALL[group][f])
            same = _chdir_of(f) == figch
            cross = f"{chname}/figures/{name}" in text or (stem and f"{chname}/figures/{NFC(stem)}" in text)
            if group == "list":
                ok = (NFC(str(figpath)) in text) or (same and f"figures/{name}" in text)
            else:
                ok = same or cross
            if ok:
                hits.append(f"{group}:{f}")
    for z in sorted(ZIP_BASE.get(name, ())):
        if figpath is None:
            hits.append(f"zip:{z}"); continue
        with zipfile.ZipFile(z) as zf:
            if any(NFC(n).endswith(f"{chname}/figures/{name}") for n in zf.namelist()):
                hits.append(f"zip:{z}")
    return hits

def refs_path(rel):
    """폴더·파일 경로가 공개 목록이나 zip 안에 있는지."""
    rel = str(rel).rstrip("/")
    hits = []
    for f, t in lists.items():
        if rel in t:
            hits.append(f"list:{f}")
    for z, names in zipnames.items():
        for n in names:
            inner = n.split("/", 1)[1] if "/" in n else n
            if inner == rel or inner.startswith(rel + "/"):
                hits.append(f"zip:{z}"); break
    return hits

rows, excluded, notes = [], [], []
def add(kind, path, why, cat):
    sz, n = fsize(path)
    rows.append({"cat": cat, "where": "connected", "path": str(path), "type": "폴더" if Path(path).is_dir() and not Path(path).is_symlink() else "파일", "bytes": sz, "files": n, "why": why})

# ---- A. 옛 그림
SUF = (".render.json", ".caption.md", ".prompt.md", ".excalidraw", ".mmd", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".md", ".json", ".txt")
fig_stats = {}
for ch in chapters:
    fdir = ch / "figures"
    if not fdir.is_dir():
        continue
    used = set()
    for f in (ch / "_src").glob("*.html"):
        used |= {NFC(u.strip()) for u in re.findall(r"\{\{(?:mermaid|img):([^|}]+)", f.read_text(errors="ignore"))}
    pend = {NFC(p.name[:-len(".prompt.md")]) for p in fdir.glob("*.prompt.md") if not (fdir / (p.name[:-len(".prompt.md")] + ".png")).exists()}
    keep = used | pend
    st = fig_stats.setdefault(ch.name, {"old": 0, "bytes": 0, "kept_render_json": 0, "dirs": [], "excluded_ref": 0})
    for f in sorted(fdir.iterdir()):
        if f.is_dir():
            st["dirs"].append(f.name); continue
        base = f.name
        if base == "_gen_figures.py":
            continue
        stem = None
        for s in SUF:
            if base.endswith(s):
                stem = base[:-len(s)]; break
        if stem is None:
            stem = f.stem
        if NFC(stem) in keep:
            continue
        if base.endswith(".render.json"):
            st["kept_render_json"] += 1
            excluded.append({"path": str(f), "why": "렌더 도장 *.render.json — 보존 대상(점검표 §4·과정 요약 §8)"}); continue
        hits = refs_name(base, stem if base.endswith((".svg", ".png", ".jpg")) else None, figpath=f)
        if hits:
            st["excluded_ref"] += 1
            excluded.append({"path": str(f), "why": "부르는 곳 있음: " + "; ".join(hits[:4])}); continue
        st["old"] += 1; st["bytes"] += f.stat().st_size
        add("file", f, f"옛 그림 — 지금 _src가 {{{{mermaid:}}}}·{{{{img:}}}}로 부르지 않음, 이름 참조 0(_src·HTML·caption·공개 목록·zip)", "old-figure")

# ---- B. gates-wip·closecheck·pre
for f in sorted(glob.glob("textbook/part*/ch*/qa/upgrade/gates-*.json")):
    p = Path(f)
    if p.parts[2] in EXCL_CH:
        continue
    if re.match(r"gates-(wip|closecheck|pre)", p.name):
        hits = refs_path(f)
        if hits:
            excluded.append({"path": f, "why": "공개 목록·zip에 있음: " + "; ".join(hits)}); continue
        add("file", p, "작업 중 게이트 기록(gates-wip·closecheck·pre) — 최종 기록은 gates-after.json(보존)", "gates-wip")
other_gw = [f for f in glob.glob("textbook/**/gates-*.json", recursive=True) if re.search(r"/gates-(wip|closecheck|pre)", f) and "/qa/upgrade/gates-" not in f]
notes.append({"gates_wip_outside_qa_upgrade": other_gw})

# ---- C. 캐시 폴더
for base in ("textbook", "labs"):
    for dp, dn, fn in os.walk(base):
        parts = Path(dp).parts
        if len(parts) >= 3 and parts[2] in EXCL_CH:
            dn[:] = []; continue
        for d in list(dn):
            if d in SKIP_DIRS or d in PRESERVE_PARTS:
                if d in PRESERVE_PARTS:
                    # 보존 폴더 안 캐시는 세기만
                    for dp2, dn2, fn2 in os.walk(os.path.join(dp, d)):
                        for d2 in dn2:
                            if d2 in ("__pycache__", ".pytest_cache", ".ruff_cache"):
                                excluded.append({"path": os.path.join(dp2, d2), "why": f"보존 폴더({d}/) 안 — 손대지 않음"})
                dn.remove(d); continue
            if d in ("__pycache__", ".pytest_cache", ".ruff_cache"):
                p = os.path.join(dp, d)
                hits = refs_path(p)
                if hits:
                    excluded.append({"path": p, "why": "공개 목록·zip에 있음: " + "; ".join(hits)})
                else:
                    add("dir", Path(p), f"파이썬 도구 캐시({d}) — 실행하면 다시 생김", "py-cache")
                dn.remove(d)

# ---- D. 개별 파일·폴더 16항목(+ _to_delete 폴더)
singles = [
    ("labs/part4/ch13-langgraph-basics/runs/graph-integrated-result.json", "개선 전 07절 기록(점검표 §2-2 1번) — 지금 교재와 값이 반대, 코드로 읽는 곳 0"),
    ("labs/part7/ch34-cost-rate-limits/runs/batch-input.jsonl", "Ch 34 옛 runs/ 셋(점검표 §2-20) — 공개 목록에서 줄을 뺀 개선 전 기록"),
    ("labs/part7/ch34-cost-rate-limits/runs/cache-measurement.json", "Ch 34 옛 runs/ 셋(점검표 §2-20) — 공개 목록에서 줄을 뺀 개선 전 기록"),
    ("labs/part7/ch34-cost-rate-limits/runs/routing-comparison.json", "Ch 34 옛 runs/ 셋(점검표 §2-20) — 공개 목록에서 줄을 뺀 개선 전 기록"),
    ("batch-input.jsonl", "루트의 옛 Batch 입력 사본(점검표 §2-20, Ch 34 runs/ 사본과 같은 크기)"),
    ("labs/part6/ch27-deepagents/workspace", "Ch 27 실습 폴더 작업 폴더(점검표 §2-15) — 노트북이 실행 때 만듦"),
    ("labs/part6/ch27-deepagents/workspace-05", "Ch 27 실습 폴더 작업 폴더(점검표 §2-15) — 노트북이 실행 때 만듦"),
    ("labs/part6/ch27-deepagents/workspace-08", "Ch 27 실습 폴더 작업 폴더(점검표 §2-15) — 노트북이 실행 때 만듦"),
    ("textbook/qa/_to_delete", "2026-09-19 분할 작업의 임시 스크립트 폴더(_trim_tmp.py 하나, 점검표 §4)"),
    ("labs/part4/ch16-guardrails/depth-notes.json", "Ch 16 옛 생성 메모(점검표 §2-5 10번, 사본은 before/generators/)"),
    ("textbook/part7/ch34-cost-rate-limits/qa/upgrade/probe/02-batch.md.tmp", "probe/ 안의 쓰다 만 임시 파일(점검표 §2-20) — 02-batch.md는 보존"),
    ("labs/part3/ch12-retrieval-tuning/runs/continuity/20260918T231546", "Ch 12 12절 사본 넷 중 셋(점검표 §4 Part 3) — 정본 사본 20260918T232052·20260921T082024는 보존"),
    ("labs/part3/ch12-retrieval-tuning/runs/continuity/20260918T231622", "Ch 12 12절 사본 넷 중 셋(점검표 §4 Part 3) — 정본 사본 20260918T232052·20260921T082024는 보존"),
    ("labs/part3/ch12-retrieval-tuning/runs/continuity/20260918T231828", "Ch 12 12절 사본 넷 중 셋(점검표 §4 Part 3) — 정본 사본 20260918T232052·20260921T082024는 보존"),
    ("textbook/_notebook/checks/--chapter", "빈 폴더(잘못된 인자로 생김, 점검표 §4 Part 1)"),
    ("textbook/_notebook/checks/ch34-cost-optimization", "빈 폴더(옛 챕터 이름, 점검표 §2-20)"),
]
for rel, why in singles:
    p = Path(rel)
    if not p.exists():
        excluded.append({"path": rel, "why": "지금 없음"}); continue
    hits = refs_path(rel) + [h for h in refs_name(p.name) if p.is_file() and h.startswith(("list:", "zip:"))]
    hits = sorted(set(hits))
    if hits:
        excluded.append({"path": rel, "why": "공개 목록·zip에 있음: " + "; ".join(hits)}); continue
    add("x", p, why, "single")

# ---- E. 실습 폴더 .venv 18
VENV18 = ["part3/ch12-retrieval-tuning", "part4/ch13-langgraph-basics", "part4/ch16-guardrails", "part5/ch17-agent-overview",
          "part5/ch18-workflow-patterns", "part5/ch19-model-tools", "part5/ch20-tool-node", "part6/ch21-create-agent",
          "part6/ch23-persistence", "part6/ch24-human-in-the-loop", "part6/ch25-streaming", "part6/ch26-delegation",
          "part6/ch27-deepagents", "part6/ch28-mcp", "part6/ch29-agent-evaluation", "part7/ch30-fastapi-serving",
          "part7/ch31-database", "part7/ch34-cost-rate-limits"]
venv_rows = []
for v in VENV18:
    p = Path("labs") / v / ".venv"
    if not p.is_dir():
        excluded.append({"path": str(p), "why": "지금 없음"}); continue
    venv_rows.append(str(p))
json.dump({"rows": rows, "excluded": excluded, "notes": notes, "fig_stats": fig_stats, "venv18": venv_rows,
           "corpus": {"src": len(corpus_src), "html": len(corpus_html), "caption": len(corpus_cap), "lists": len(lists), "zips": {k: len(v) for k, v in zipnames.items()}}},
          open(W / "manifest-a.json", "w"), ensure_ascii=False, indent=1)
from collections import Counter
c = Counter(r["cat"] for r in rows); b = Counter()
for r in rows: b[r["cat"]] += r["bytes"]
print("rows", dict(c), dict(b))
print("excluded", len(excluded), Counter(e["why"].split(":")[0][:30] for e in excluded))
print({k: (v["old"], v["bytes"], v["kept_render_json"], v["excluded_ref"], v["dirs"]) for k, v in fig_stats.items()})
print(notes)
