"""한정어 없는 「청크」(스트리밍 뜻)를 「스트림 청크」로 바꾸는 치환 목록을 만든다(쓰기 없음, 목록 JSON만).
사용: build_reps.py <생성기> <노트북> <_src> <출력 reps.json> [<추가 치환 json>]
- 노트북 마크다운: 백틱 코드·그림 문법 ![..](..) 밖의 글만.
- _src: 태그 사이 글과 {{mermaid/img:이름|대체|캡션}}의 캡션만. <code>·대체 텍스트·그림 이름은 그대로.
- 만든 목록을 mdpatch.py와 같은 순서·방식으로 메모리에서 적용해, 의도한 결과와 같은지 확인한다.
"""
import json, re, sys, importlib.util, tempfile, os
gen_p, nb_p, src_p, out_p = sys.argv[1:5]
extra = json.load(open(sys.argv[5], encoding="utf-8")) if len(sys.argv) > 5 else []
POST = [("스트림 청크와 스트림 청크 더하기", "스트림 청크와 더하기"),
        ("글자 스트림 청크", "글자가 든 스트림 청크"),
        ("사용량 스트림 청크", "사용량이 든 스트림 청크")]
def fix(seg):
    seg = re.sub(r"(?<!스트림 )(?<!문서 )청크", "스트림 청크", seg)
    for a, b in POST: seg = seg.replace(a, b)
    for a, b in extra: seg = seg.replace(a, b)
    return seg
gen = open(gen_p, encoding="utf-8").read()
nb = json.load(open(nb_p, encoding="utf-8"))
src = open(src_p, encoding="utf-8").read()
t = lambda s: s if isinstance(s, str) else "".join(s)
md_idx = [i for i, c in enumerate(nb["cells"]) if c["cell_type"] == "markdown"]
md_all = [t(nb["cells"][i]["source"]) for i in md_idx]
code_all = [t(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
keep_md = re.compile(r"(`[^`]*`|!\[[^\]]*\]\([^)]*\))")
def fix_md(s):
    return "".join(p if keep_md.fullmatch(p) else fix(p) for p in keep_md.split(s))
md_final = [fix_md(s) for s in md_all]
tok = re.compile(r"(\{\{(?:mermaid|img):[^}]*\}\}|<code>.*?</code>|<pre[\s\S]*?</pre>|<[^>]+>)")
def fix_src(s):
    out = []
    for p in tok.split(s):
        if p.startswith("{{mermaid:") or p.startswith("{{img:"):
            head, _, cap = p[:-2].rpartition("|")
            out.append(head + "|" + fix(cap) + "}}")
        elif p and tok.fullmatch(p): out.append(p)
        else: out.append(fix(p))
    return "".join(out)
src_final = fix_src(src)
def total(old, g, mds, s):
    return g.count(old) + sum(m.count(old) for m in mds) + s.count(old)
def diffs(a, b):
    """a→b 바뀐 구간들(앞뒤 공통 부분을 뺀 최소 구간)을 차례로 낸다 — 줄 단위."""
    res = []
    al, bl = a.split("\n"), b.split("\n")
    assert len(al) == len(bl)
    pos = 0
    for x, y in zip(al, bl):
        if x != y: res.append((pos, x, y))
        pos += len(x) + 1
    return res
reps = []
def add_rep(text, start, old_seg, new_seg, cur, md_mode=False):
    # text[start:start+len(old_seg)] == old_seg; 문맥을 넓혀 cur(세 대상) 안에서 하나뿐이게
    end = start + len(old_seg); ctx = 0
    while True:
        lo, hi = max(0, start - ctx), min(len(text), end + ctx)
        old = text[lo:hi]; new = text[lo:start] + new_seg + text[end:hi]
        g, mds, s = cur
        if md_mode: ok = sum(m.count(old) for m in mds) == 1 and s.count(old) == 0 and g.count(old) <= 1
        else: ok = total(old, *cur) == 1
        if ok and not any(old in c for c in code_all): return [old, new]
        if lo == 0 and hi == len(text): raise SystemExit("cannot make unique: " + old_seg[:60])
        ctx += 2
# 노트북 마크다운(생성기에도 같은 글이 있으면 함께 맞음) — 줄 단위로, 셀 문맥을 넓혀 하나뿐이게
g_cur, md_cur, s_cur = gen, list(md_all), src
for k, (a, b) in enumerate(zip(md_all, md_final)):
    for pos, x, y in diffs(a, b):
        # 줄 안의 최소 바뀐 구간
        i = 0
        while x[i] == y[i]: i += 1
        j = 0
        while x[len(x)-1-j] == y[len(y)-1-j] and len(x)-1-j > i: j += 1
        old_seg, new_seg = x[:len(x)-j] , y[:len(y)-j]
        # 줄 전체를 기본 단위로(읽기 쉬운 목록), 하나뿐이 아니면 셀 안 문맥으로 넓힘
        old, new = x, y
        n_gen = g_cur.count(old); n_md = sum(m.count(old) for m in md_cur); n_src = s_cur.count(old)
        if not (n_md == 1 and n_src == 0 and n_gen <= 1) or any(old in c for c in code_all):
            old, new = add_rep(md_cur[k], md_cur[k].find(x), x, y, (g_cur, md_cur, s_cur), md_mode=True)
        if g_cur.count(old) == 0:
            # 생성기 쪽 글이 다름(예: {RUN_DATE}) — 바뀐 최소 구간으로 줄여 다시
            i2 = 0
            while x[i2] == y[i2]: i2 += 1
            # 문장 시작까지 되돌림
            st = max(x.rfind(". ", 0, i2) + 2, 0)
            old, new = x[st:], y[st:]
            assert total(old, g_cur, md_cur, s_cur) == 2 and g_cur.count(old) == 1, old
        reps.append([old, new])
        g_cur = g_cur.replace(old, new); md_cur = [m.replace(old, new) for m in md_cur]; s_cur = s_cur.replace(old, new)
# _src — 바뀐 조각마다
pieces_a, pieces_b = tok.split(src), tok.split(src_final)
assert len(pieces_a) == len(pieces_b)
pos_a = 0; delta = 0
for a, b in zip(pieces_a, pieces_b):
    if a != b:
        start = pos_a + delta
        assert s_cur[start:start+len(a)] == a
        old, new = add_rep(s_cur, start, a, b, (g_cur, md_cur, s_cur))
        reps.append([old, new])
        g_cur = g_cur.replace(old, new); md_cur = [m.replace(old, new) for m in md_cur]; s_cur = s_cur.replace(old, new)
        delta += len(b) - len(a)
    pos_a += len(a)
json.dump(reps, open(out_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# mdpatch.py와 같은 방식으로 원본에서 다시 적용해 확인
g2, md2, s2 = gen, list(md_all), src
for old, new in reps:
    hits = (old in g2) + any(old in m for m in md2) + (old in s2)
    assert hits, "MISS " + old[:50]
    g2 = g2.replace(old, new); md2 = [m.replace(old, new) for m in md2]; s2 = s2.replace(old, new)
print("src == intended:", s2 == src_final)
print("md == intended:", md2 == md_final)
print("스트림 스트림:", s2.count("스트림 스트림") + sum(m.count("스트림 스트림") for m in md2) + g2.count("스트림 스트림"))
# 생성기: 임시 사본을 불러 셀을 만들어 보고, 마크다운은 의도와, 코드는 지금 노트북과 견줌
tmp = os.path.join(os.path.dirname(out_p), "gen_sim_" + os.path.basename(gen_p))
open(tmp, "w", encoding="utf-8").write(g2)
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(gen_p)))
spec = importlib.util.spec_from_file_location("gen_sim", tmp)
mod = importlib.util.module_from_spec(spec)
mod.__file__ = os.path.abspath(gen_p)
exec(compile(g2, os.path.abspath(gen_p), "exec"), mod.__dict__)
cells = mod.cells() if hasattr(mod, "cells") else [getattr(mod, n) for n in dir(mod) if n.startswith("section_")][0]()[2]
gm = [t(c["source"]) for c in cells if c["cell_type"] == "markdown"]
gc = [t(c["source"]) for c in cells if c["cell_type"] == "code"]
print("gen code == nb code:", gc == code_all)
bad = [i for i, (x, y) in enumerate(zip(gm, md2)) if x != y]
print("gen md != patched nb md (cells):", bad)
if hasattr(mod, "src_html"): print("gen src_html == patched src:", mod.src_html() == s2)
print("reps", len(reps))
