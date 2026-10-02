"""리뷰 묶음: python3 textbook/_notebook/upgrade/pack.py <챕터 경로> NN [NN...]
→ 챕터 qa/upgrade/review-pack/{slug}.md (_src HTML, 실행된 노트북 셀·출력, Mermaid 원본·캡션, 삽화 프롬프트)"""
import glob, json, sys
from pathlib import Path
ROOT = Path.home() / "mnt/한국경제신문"
ch = ROOT / sys.argv[1]
lab = ROOT / (json.load(open(ch / "chapter.json"))["lab_path"] if (ch / "chapter.json").exists() else "labs/" + sys.argv[1].split("textbook/", 1)[1])
for n in sys.argv[2:]:
    src = Path(glob.glob(str(ch / f"_src/{n}-*.html"))[0]); slug = src.stem
    nb = json.loads((lab / "notebooks" / f"{slug}.ipynb").read_text())
    out = [f"# {slug}", "", "## _src 본문 (HTML 원본)", "", "```html", src.read_text().rstrip(), "```", "", "## 노트북 셀 (순서대로)", ""]
    for i, c in enumerate(nb["cells"]):
        s = c["source"] if isinstance(c["source"], str) else "".join(c["source"])
        meta = {k: v for k, v in c["metadata"].items() if k != "attachments"}
        if c["cell_type"] == "markdown":
            out += [f"### [{i}] markdown {meta}", "", s, ""]
        else:
            text = ""
            for o in c.get("outputs", []):
                t = o.get("text", ""); text += t if isinstance(t, str) else "".join(t)
                if o.get("output_type") == "error": text += f"{o.get('ename')}: {o.get('evalue')}\n"
            out += [f"### [{i}] code {meta}", "", "```python", s, "```", "", "출력:", "```", text, "```", ""]
    out += ["## 그림", ""]
    for f in sorted(ch.glob(f"figures/{n}-[0-9]-*.mmd")):
        out += [f"### {f.name}", "", "```mermaid", f.read_text().rstrip(), "```", ""]
        cap = f.with_suffix(".caption.md")
        if cap.exists(): out += [cap.read_text().rstrip(), ""]
    for f in sorted(ch.glob(f"figures/{n}-[0-9]-*.prompt.md")):
        out += [f"### {f.name}", "", f.read_text().rstrip(), ""]
    d = ch / "qa/upgrade/review-pack"; d.mkdir(parents=True, exist_ok=True)
    (d / f"{slug}.md").write_text("\n".join(out) + "\n"); print("pack", slug)
