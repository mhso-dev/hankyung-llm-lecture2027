"""6단계 삭제 목록 합치기 — manifest-a.json + du 기록 → TSV·요약 JSON (읽기 전용, 쓰는 것은 TSV 하나와 6-docs/log)."""
import json, os, re, glob, subprocess
from pathlib import Path
from collections import Counter, defaultdict
ROOT = Path.home() / "mnt/한국경제신문"; os.chdir(ROOT)
L = ROOT / ".cache/final-close/6-docs/log"
TMPDIR = os.environ.get("TMPDIR", "/tmp"); HOME = str(Path.home())
a = json.load(open(L / "manifest-a.json"))
rows, held, skipped = [], [], []

# 1) 그림: 부르는 곳이 있는 그림과 같은 이름(줄기)의 짝은 함께 뺌(.svg만 남으면 check_figures가 .excalidraw 짝을 요구)
def stem_of(name):
    for s in (".render.json", ".caption.md", ".prompt.md", ".excalidraw", ".mmd", ".svg", ".png", ".jpg", ".md"):
        if name.endswith(s): return name[:-len(s)]
    return Path(name).stem
blocked = {(str(Path(e["path"]).parent), stem_of(Path(e["path"]).name)) for e in a["excluded"] if e["why"].startswith("부르는 곳 있음")}
cat_label = {"old-figure": "옛그림", "gates-wip": "게이트작업기록", "py-cache": "파이썬캐시", "single": "개별항목"}
for r in a["rows"]:
    if r["cat"] == "old-figure" and (str(Path(r["path"]).parent), stem_of(Path(r["path"]).name)) in blocked:
        skipped.append({"path": r["path"], "bytes": r["bytes"], "why": "같은 줄기의 .svg가 챕터 공개 목록에 있어 짝(.excalidraw·.caption.md)도 함께 남김"})
        continue
    rows.append(("connected", r["path"], r["type"], r["bytes"], cat_label[r["cat"]], r["why"]))

# 2) 실습 폴더 .venv 18
for line in open(L / "du-venv.tsv"):
    p, s, n = line.rstrip("\n").split("\t")
    why = "실습 폴더 macOS .venv(점검표 §4 삭제 승인 18개)"
    if "ch31-database" in p:
        why += " — Part 7 묶음 실행 검사 러너를 3단계에서 uv run --project <풀린 묶음>으로 고쳐 더는 쓰지 않음(5단계 통과)"
    if "ch12-" in p or "ch13-" in p:
        why = "실습 폴더 .venv(깨진 빈 판, 점검표 §4 삭제 승인 18개)"
    rows.append(("connected", p, "폴더", int(s), "실습venv", why))

# 3) .cache (vm/pgenv·final-close/*/log·tools 제외)
for line in open(L / "du-cache.tsv"):
    p, s, n = line.rstrip("\n").split("\t")
    if p == ".cache/final-close": continue
    rows.append(("connected", p, "폴더", int(s), "캐시", "챕터 작업·보기·마감 임시 폴더(.cache, 전체 점검 §8)"))
for line in open(L / "du-vm.tsv"):
    p, s = line.rstrip("\n").split("\t")
    name = p.split("/")[-1]
    why = {"bundle-check": "묶음 실행 검사 uv 캐시·임시(다음 검사는 캐시를 새로 받음)",
           "hf": "Hugging Face 모델 캐시(재실행 때 다시 받음, 약 6GB)",
           "mamba": "PostgreSQL 환경을 만든 micromamba 꾸러미 캐시(pgenv는 자기 완결 — 밖을 가리키는 링크 0)",
           "pg": "옛 PostgreSQL 시도 폴더(훅이 쓰지 않음)",
           "pgdata": "Ch 12 pgvector 데이터 폴더 — Ch 12 pre_exec.sh가 initdb 없이 켬(Ch 12 01~03 재실행 때 새로 만들어야 함)",
           "pgembed-try": "pgembed 시험 폴더(쓰지 않기로 한 결정, Ch 31)",
           "pgtool": "옛 PostgreSQL 도구 시도", "shot": "옛 화면 캡처 작업 폴더"}.get(name, "챕터 실행 가상환경(run_section.sh가 다시 만듦)")
    rows.append(("connected", p, "폴더", int(s), "캐시", why))
for d in sorted(glob.glob(".cache/final-close/*/*/")):
    d = d.rstrip("/")
    if d.split("/")[-1] in ("log", "tools"): continue
    s = int(subprocess.run(["du", "-sb", d], capture_output=True, text=True).stdout.split()[0])
    rows.append(("connected", d, "폴더", s, "캐시", "전체 마감 단계 사본·작업 폴더(전후 해시는 같은 단계 log/와 final-close-log.md)"))

# 4) 기기
HOLD = {"/tmp/pw": "Ch 12 화면 재촬영(visual.cjs) — 사람 결정 뒤 다시 찍을 때 필요",
        "/tmp/pw-browsers": "Ch 12 화면 재촬영(visual.cjs) — 사람 결정 뒤 다시 찍을 때 필요",
        "/tmp/libs": "Ch 12 화면 재촬영 — 브라우저가 쓰는 libXdamage(LD_LIBRARY_PATH)",
        f"{TMPDIR}/fc5-part3": "finalize_continuity_evidence.py가 읽는 temporary_extraction — finalize 뒤에 지울 것(다시 만들면 모델 요청)"}
SYSTEM = ("hsperfdata_root", "systemd-private-", "data-gym-cache", "node-compile-cache", "generator-cli-")
for line in open(L / "du-device.tsv"):
    p, t, s = line.rstrip("\n").split("\t")
    s = int(s or 0); base = p.rsplit("/", 1)[-1]
    if p in HOLD:
        held.append({"path": p, "type": t, "bytes": s, "why": HOLD[p]}); continue
    if base.startswith(SYSTEM):
        skipped.append({"path": p, "bytes": s, "why": "시스템·도구가 스스로 관리하는 폴더(이번 작업물 아님)"}); continue
    if p.startswith("/tmp/"):
        why = {"mmd": "Mermaid 렌더 도구(npm 설치본)", "pptr-cache": "Mermaid 렌더용 Puppeteer 브라우저",
               "npm-cache": "npm 캐시", "npm-cache-ch31close": "npm 캐시(Ch 31 마감)", "uv-cache": "uv 캐시(Part 3 연속성 묶음 등)",
               "finalcheck": "전체 점검(2026-09-30) 임시 스크립트·결과", "fc1-builds.txt": "1단계 빌드 기록 임시 파일",
               "ch31-pg": "Ch 31 훅 DB 데이터(지우면 다음 훅이 initdb부터 — 괜찮음)"}.get(base, "챕터 작업·검토·누적 문서 임시 폴더")
    elif p.startswith(TMPDIR):
        why = {"fc3-ch33": "3단계 Part 7 러너 시험 임시 폴더", "fc3-ch34": "3단계 Part 7 러너 시험 임시 폴더",
               "fc5-part6": "5단계 Part 6 묶음 실행 풀린 폴더"}.get(base, "챕터 노트북 실행 임시 폴더($TMPDIR)")
    else:
        why = "Ch 16 작업 폴더(세션 홈, 점검표 §2-5)"
    rows.append(("device", p, t, s, "기기", why))

with open(ROOT / "textbook/qa/deletion-manifest-2026-10-01.tsv", "w") as o:
    o.write("구분\t경로\t종류\t크기(바이트)\t까닭\n")
    for w, p, t, s, c, why in rows:
        o.write(f"{w}\t{p}\t{t}\t{s}\t[{c}] {why}\n")
summ = defaultdict(lambda: [0, 0])
for w, p, t, s, c, why in rows:
    summ[(w, c)][0] += 1; summ[(w, c)][1] += s
tot = defaultdict(lambda: [0, 0])
for (w, c), (n, s) in summ.items():
    tot[w][0] += n; tot[w][1] += s
out = {"by_cat": {f"{w}|{c}": v for (w, c), v in summ.items()}, "total": dict(tot), "held": held, "skipped": skipped,
       "lines": len(rows)}
json.dump(out, open(L / "manifest-summary.json", "w"), ensure_ascii=False, indent=1)
for k, v in sorted(out["by_cat"].items()): print(k, v[0], v[1], f"{v[1]/2**30:.3f}GiB")
print("total", out["total"], {k: f"{v[1]/2**30:.3f}GiB" for k, v in tot.items()})
print("held", [(h["path"], h["bytes"]) for h in held])
print("skipped", len(skipped), sum(x["bytes"] for x in skipped), Counter(x["why"][:20] for x in skipped))
