"""전체 마감 7단계: 지운 뒤 보존 대상·그림 참조·공개 목록 확인(읽기만 함, 결과는 인자로 받은 JSON 하나)."""
import time
T0 = time.time()
def tick(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
import csv, glob, hashlib, json, os, re, sys, zipfile
from pathlib import Path
ROOT = Path.home() / "mnt" / "한국경제신문"
OUT = Path(sys.argv[1])
os.chdir(ROOT)
R = {}
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def nfiles(d):
    return sum(len(fs) for _, _, fs in os.walk(d))

# 1) 지운 목록
rows = list(csv.reader(open("textbook/qa/deletion-manifest-2026-10-01.tsv", encoding="utf-8"), delimiter="\t"))[1:]
KEEP = {"labs/part7/ch31-database/.venv", ".cache/vm/pgdata"}
left, kept_ok, deleted_bytes = [], [], {"connected": [0, 0], "device": [0, 0]}
for k, p, typ, size, why in rows:
    ap = str(ROOT / p) if k == "connected" else p
    if p in KEEP:
        kept_ok.append([p, os.path.isdir(ap)]); continue
    deleted_bytes[k][0] += 1; deleted_bytes[k][1] += int(size)
    if os.path.lexists(ap): left.append(p)
R["manifest"] = {"rows": len(rows), "left": left, "kept": kept_ok, "pgenv": os.path.isdir(".cache/vm/pgenv"),
                 "deleted_rows_bytes": deleted_bytes,
                 "render_json_in_tsv": sum(1 for r in rows if r[1].endswith(".render.json")),
                 "env_in_tsv": sum(1 for r in rows if r[1].endswith(".env") or "/.env" in r[1])}

tick('# 2) 보존 대상')
# 2) 보존 대상
chap = sorted(p for p in glob.glob("textbook/part*/ch*") if os.path.isdir(p))
before = {}
for c in chap:
    up = Path(c) / "qa/upgrade"
    ent = {}
    for sub in ("before", "probe", "review-pack"):
        d = up / sub
        if d.is_dir(): ent[sub] = nfiles(d)
    for d in sorted(up.glob("before-*")) if up.is_dir() else []:
        if d.is_dir(): ent[d.name] = nfiles(d)
    if (Path(c) / "qa/before").is_dir(): ent["qa/before"] = nfiles(Path(c) / "qa/before")
    gen = list(up.glob("before/generators/blocked/*")) if up.is_dir() else []
    ent["blocked_generators"] = len(gen)
    for g in ("gates-before.json", "gates-after.json", "gates-after-2-7.json"):
        if (up / g).is_file(): ent.setdefault("gates_kept", []).append(g)
    ent["gates_wip_left_in_qa_upgrade"] = len([x for x in up.glob("gates-wip*")] + [x for x in up.glob("gates-closecheck*")] + [x for x in up.glob("gates-pre*")]) if up.is_dir() else 0
    before[Path(c).name] = ent
R["chapters"] = before
R["review_pack_total"] = sum(v.get("review-pack", 0) for v in before.values())
runs12 = Path("labs/part3/ch12-retrieval-tuning/runs/continuity")
R["ch12_continuity"] = {d.name: nfiles(d) for d in sorted(runs12.iterdir()) if d.is_dir()} if runs12.is_dir() else None
R["ch12_deleted_copies_gone"] = all(not (runs12 / n).exists() for n in ("20260918T231546", "20260918T231622", "20260918T231828"))
R["ch09_ch10_runs_continuity"] = {p: (len(os.listdir(p)) if os.path.isdir(p) else None) for p in
    ("labs/part3/ch09-rag-first-run/runs/continuity", "labs/part3/ch10-document-processing/runs/continuity")}
R["render_json_count"] = len([p for p in glob.glob("textbook/**/*.render.json", recursive=True)])
R["pre_exec"] = {p: (sha(p)[:8] if os.path.isfile(p) else None) for p in sorted(glob.glob("textbook/part*/ch*/qa/upgrade/pre_exec.sh"))}
R["env_exists"] = os.path.isfile(".env")
R["moai_exists"] = os.path.isdir(".moai")
# 자료·도구 파일 해시(점검표 §4, 2단계 뒤 도구 파일은 새 해시)
tick('want = {')
want = {"0177cebc": "labs/part4/ch15-evaluation-advanced", "ae2fe4f4": "labs/part4/ch16-guardrails", "92e3d109": "labs/part4/ch16-guardrails",
        "736271dd": "labs/part4/ch16-guardrails", "d4f76099": "labs/part4/ch16-guardrails", "18209add": "labs/part5/ch17-agent-overview",
        "5a158a68": "labs/part5/ch18-workflow-patterns", "fa5975b5": "labs/part5/ch19-model-tools", "34161a6f": "labs/part5/ch20-tool-node",
        "f4113158": "labs/part6/ch21-create-agent", "25cfe5df": "labs/part6/ch21-create-agent", "a850b2cd": "labs/part6/ch23-persistence",
        "c60467bd": "labs/part6/ch23-persistence", "b0201de7": "labs/part6/ch23-persistence", "295bfaf6": "labs/part6/ch24-human-in-the-loop",
        "6df804b8": "labs/part6/ch25-streaming", "0748a8eb": "labs/part6/ch26-delegation", "ed5c4240": "labs/part6/ch27-deepagents",
        "570ed3cc": "labs/part6/ch28-mcp", "5dc77333": "labs/part6/ch28-mcp", "b75636c4": "labs/part6/ch29-agent-evaluation",
        "333e9a62": "labs/part7/ch30-fastapi-serving"}
found = {}
for pref, d in want.items():
    hit = []
    for dp, dns, fns in os.walk(d):
        dns[:] = [x for x in dns if x not in (".venv", "__pycache__", "runs") or d.endswith(("ch15-evaluation-advanced","ch16-guardrails"))]
        for f in fns:
            p = os.path.join(dp, f)
            if f.endswith((".py", ".json", ".jsonl", ".sh", ".csv")) and os.path.getsize(p) < 5_000_000 and sha(p).startswith(pref): hit.append(p)
    found[pref] = hit
R["data_tool_hashes"] = found
# zip 10개
tick('ZIP = {')
ZIP = {"ch01": "cf1c6645198a560ba654d8bf04e98a6386c407350651b856a56316a509fc6bc2", "ch02": "f9ea0719fc1eaeaf9afbe446e728858f39820081158339d59e05019343ea6dcc",
       "llm": "b0c5a072cee25d80c118b35925a7bf134d7a88139e33c8e782409f0e866f5638", "part1": "b82d8fc12f7c7df198462e41e704c30888e20ebb27677be53d65251acaa4002d",
       "part2": "11a0e5158705530a0f3adb29995828cf7e8e93fa2dbb4ec440f8b7c370e55baf", "part3": "c6dea7c1722e7f7b7cffb4dd2799aa6e083dc93927de1858c27782d077aac5a5",
       "part4": "29cc6d1fa9be0c6a141d5fb6d8d56fefa76021c93415ba321b49ec17bd9da8d9", "part5": "faf00151f902de75a951dc603f1a8f8bff56c0cf97602b8bc9732fe50d75ce15",
       "part6": "5a1736be9221690a7c72af138da51a3f4ea96b54deefb2ba5d201ca390238aed", "part7": "710053c5061e14d6fe40a04b9845539f4b9880672986f435e9bbb3e0212473b8"}
zr = {}
for k, h in ZIP.items():
    p = f"textbook/downloads/{k}-practice.zip"
    cur = sha(p)
    with zipfile.ZipFile(p) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        # zip 속 파일이 디스크에 있는지(맨 앞 폴더 이름 하나를 떼고도 찾아 봄)
        miss = 0; diff = 0
        for n in names:
            cands = [ROOT / n] + [ROOT / n.split("/", 1)[1]] if "/" in n else [ROOT / n]
            hit = next((c for c in cands if c.is_file()), None)
            if hit is None: miss += 1
            elif hashlib.sha256(z.read(n)).hexdigest() != sha(hit): diff += 1
    zr[k] = {"same": cur == h, "entries": len(names), "disk_missing_raw": miss, "disk_diff_raw": diff}
R["zips"] = zr
tick('# pack 입력')
# pack 입력 2,955
pk = [l.rstrip("\n").split("\t") for l in open(".cache/final-close/6-docs/log/pack-inputs-before.tsv", encoding="utf-8") if l.strip()]
pm, pd = [], []
for h, p in pk:
    if not os.path.isfile(p): pm.append(p)
    elif sha(p) != h: pd.append(p)
R["pack_inputs"] = {"n": len(pk), "missing": pm, "changed": pd}
R["final_close_log_tools"] = {d: os.path.isdir(d) for d in sorted(glob.glob(".cache/final-close/*/log") + glob.glob(".cache/final-close/*/tools"))}
R["excluded_kept"] = {"ch22_old_fig_files": len([p for p in glob.glob("textbook/part6/ch22-middleware/figures/*") ]),
                      "ch13_graph_integrated": os.path.isfile("labs/part4/ch13-langgraph-basics/runs/graph-integrated-result.json")}
R["user_venvs"] = {p: os.path.isdir(p) for p in sorted(glob.glob("labs/part*/ch*/.venv"))}

tick('# 3) 그림 참조')
# 3) 그림 참조
TOK = re.compile(r"\{\{(mermaid|img|svg):([^|}]+)")
miss_fig, nref = [], 0
for src in sorted(glob.glob("textbook/part*/ch*/_src/*.html")):
    figs = Path(src).parent.parent / "figures"
    for kind, name in TOK.findall(Path(src).read_text(encoding="utf-8")):
        nref += 1
        need = [figs / f"{name}.svg"] if kind in ("mermaid", "svg") else [figs / f"{name}.png"]
        if kind == "mermaid": need.append(figs / f"{name}.mmd")
        for n in need:
            if not n.is_file(): miss_fig.append(f"{src} -> {n.name}")
tick('IMG = re.compile')
IMG = re.compile(r"<img\b[^>]*?\bsrc=[\"']([^\"']+)[\"']", re.I)
html_files = [p for p in glob.glob("textbook/**/*.html", recursive=True) if "/_src/" not in p and "/qa/" not in p and "/_template/" not in p]
miss_img, nimg, ndata = [], 0, 0
for h in html_files:
    for s in IMG.findall(Path(h).read_text(encoding="utf-8", errors="replace")):
        if s.startswith("data:"): ndata += 1; continue
        if re.match(r"^[a-z]+://", s): continue
        nimg += 1
        t = (Path(h).parent / s.split("#")[0].split("?")[0]).resolve()
        if not t.exists(): miss_img.append(f"{h} -> {s}")
tick('cap_orphan = []')
cap_orphan = []
caps = glob.glob("textbook/part*/ch*/figures/*.caption.md")
for c in caps:
    stem = c[: -len(".caption.md")]
    if not any(os.path.isfile(stem + e) for e in (".svg", ".png")): cap_orphan.append(c)
cap_refs_miss = []
for c in caps:
    txt = Path(c).read_text(encoding="utf-8")
    for m in re.findall(r"([\w가-힣\-\.]+\.(?:svg|png|mmd|excalidraw))", txt):
        if not (Path(c).parent / m).is_file(): cap_refs_miss.append(f"{c} -> {m}")
R["figures"] = {"src_files": len(glob.glob("textbook/part*/ch*/_src/*.html")), "src_refs": nref, "src_missing": miss_fig,
                "html_files": len(html_files), "html_img_file_refs": nimg, "html_img_data": ndata, "html_img_missing": miss_img,
                "captions": len(caps), "caption_without_figure": cap_orphan, "caption_named_file_missing": cap_refs_miss}
tick('# 4) 공개 목록')
# 4) 공개 목록
lists = sorted(p for p in glob.glob("textbook/**/public-files.json", recursive=True) + glob.glob("textbook/**/prerequisite-files.json", recursive=True)
               if "/before" not in p and "/upgrade/" not in p)
SKIPKEYS = {"exclude", "excluded", "note", "policy", "chapter", "public", "lab"}
def entries(l):
    d = json.load(open(l, encoding="utf-8"))
    chdir = Path(l).parent.parent if Path(l).parent.name == "qa" else Path(l).parent
    labdir = Path("labs") / chdir.relative_to("textbook") if str(chdir).count("/") >= 2 else None
    def walk(x, base=None):
        if isinstance(x, str):
            yield (str(base / x) if base is not None else x)
        elif isinstance(x, list):
            for y in x: yield from walk(y, base)
        elif isinstance(x, dict):
            for k, y in x.items():
                if k in SKIPKEYS: continue
                b = chdir if k == "textbook" else (labdir if k == "labs" else base)
                yield from walk(y, b)
    yield from walk(d)
lm, nent, npat = [], 0, 0
for l in lists:
    for s in entries(l):
        if s.startswith("**") or ("/" not in s): continue
        nent += 1
        if any(ch in s for ch in "*?["):
            npat += 1
            if not glob.glob(s): lm.append(f"{l}: {s}")
        elif not os.path.exists(s): lm.append(f"{l}: {s}")
R["public_lists"] = {"lists": len(lists), "entries": nent, "patterns": npat, "missing": lm}
OUT.write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: R[k] for k in ("manifest", "review_pack_total", "ch12_continuity", "ch12_deleted_copies_gone", "ch09_ch10_runs_continuity", "render_json_count", "pre_exec", "env_exists", "zips", "excluded_kept")}, ensure_ascii=False, indent=0))
print("pack", R["pack_inputs"]["n"], len(R["pack_inputs"]["missing"]), len(R["pack_inputs"]["changed"]))
print("figures", {k: (v if not isinstance(v, list) else len(v)) for k, v in R["figures"].items()})
print("public", R["public_lists"]["lists"], R["public_lists"]["entries"], len(R["public_lists"]["missing"]))
print("hash miss", [k for k, v in found.items() if len(v) != 1], {k: len(v) for k, v in found.items() if len(v) > 1})
