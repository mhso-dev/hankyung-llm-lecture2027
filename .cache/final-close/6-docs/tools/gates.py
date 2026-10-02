import json, sys, importlib.util
from pathlib import Path
ROOT = Path.home() / "mnt" / "한국경제신문"
spec = importlib.util.spec_from_file_location("ug", ROOT / "textbook/_notebook/checks/upgrade_gates.py")
ug = importlib.util.module_from_spec(spec); spec.loader.exec_module(ug)
TARGET = [f"ch{n:02d}" for n in list(range(1, 32)) + [34]]
out = {}
for chapter in sorted((ROOT / "textbook").glob("part*/ch*")):
    tag = chapter.name[:4]
    if tag not in TARGET:
        continue
    if (chapter / "chapter.json").is_file():
        cfg = json.loads((chapter / "chapter.json").read_text(encoding="utf-8"))
        lab = ROOT / cfg["lab_path"]
        slugs = [s["slug"] for s in cfg["sections"]]
    else:
        lab = ROOT / "labs" / chapter.relative_to(ROOT / "textbook")
        slugs = sorted(p.stem for p in (chapter / "_src").glob("[0-9][0-9]-*.html"))
    reports = []
    for slug in slugs:
        try:
            reports.append(ug.check_section(chapter, lab, slug))
        except Exception as e:
            reports.append({"slug": slug, "error": repr(e)})
    totals = {g: sum(r.get("counts", {}).get(g, 0) for r in reports) for g in ["G1","G2","G3","G4","G5","G6","G7"]}
    # compare gates-after
    ga = chapter / "qa/upgrade/gates-after.json"
    cmp = None
    if ga.is_file():
        after = json.loads(ga.read_text(encoding="utf-8"))
        a_secs = {s["slug"]: s for s in after.get("sections", [])}
        diffs = []
        for r in reports:
            a = a_secs.get(r["slug"])
            if a is None:
                diffs.append(f"{r['slug']}:not_in_after"); continue
            if "error" in r: diffs.append(f"{r['slug']}:error"); continue
            if a.get("counts") != r["counts"]: diffs.append(f"{r['slug']}:counts {a.get('counts')} vs {r['counts']}")
            if a.get("sentences") != r["sentences"]: diffs.append(f"{r['slug']}:sentences {a.get('sentences')}->{r['sentences']}")
            if a.get("code_cells") != r["code_cells"]: diffs.append(f"{r['slug']}:code_cells {a.get('code_cells')}->{r['code_cells']}")
        extra = [s for s in a_secs if s not in {r['slug'] for r in reports}]
        for s in extra: diffs.append(f"{s}:only_in_after")
        cmp = {"after_totals": after.get("totals"), "after_passed": after.get("passed_sections"), "diffs": diffs}
    out[chapter.name] = {
        "part": chapter.parent.name, "lab": str(lab.relative_to(ROOT)), "sections": len(slugs),
        "slugs": slugs,
        "code_cells": sum(r.get("code_cells", 0) for r in reports),
        "sentences": sum(r.get("sentences", 0) for r in reports),
        "totals": totals,
        "passed": sum(1 for r in reports if r.get("passed")),
        "nonzero": {r["slug"]: (r.get("issues") if "issues" in r else r.get("error")) for r in reports if not r.get("passed")},
        "per_section": {r["slug"]: [r.get("code_cells"), r.get("sentences")] for r in reports},
        "cmp": cmp,
    }
Path("/sessions/rcw-01fa62dwjghtyrmrgyqrfwx5/mnt/한국경제신문/.cache/final-close/6-docs/log/gates-result.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
tot_s = sum(v["sections"] for v in out.values())
print("chapters", len(out), "sections", tot_s)
for k, v in out.items():
    t = sum(v["totals"].values())
    d = v["cmp"]["diffs"] if v["cmp"] else "no-after"
    print(k, v["sections"], v["passed"], v["code_cells"], v["sentences"], t, (len(d) if isinstance(d, list) else d))
