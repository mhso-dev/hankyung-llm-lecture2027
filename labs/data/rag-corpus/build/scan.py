# -*- coding: utf-8 -*-
"""스캔본 변형 — 텍스트 레이어 제거(이미지 PDF), 기울기·노이즈·명암 편차·JPEG 열화. OCR 실습용."""
import subprocess, io, random, shutil
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import img2pdf
from common import ROOT, PDF

def scanify(src: Path, dst: Path, seed: int, dpi=150, skew=1.2, noise=12, quality=55, gray=True):
    tmp = ROOT / "build" / "tmp_scan"; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(src), str(tmp / "p")], check=True)
    rnd = random.Random(seed); pages = []
    for i, png in enumerate(sorted(tmp.glob("p-*.png"))):
        im = Image.open(png).convert("L" if gray else "RGB")
        # 기울기
        ang = rnd.uniform(-skew, skew)
        im = im.rotate(ang, resample=Image.BICUBIC, expand=False, fillcolor=255 if gray else (255, 255, 255))
        # 명암·대비 편차 (페이지마다 다르게)
        im = ImageEnhance.Brightness(im).enhance(rnd.uniform(0.9, 1.05))
        im = ImageEnhance.Contrast(im).enhance(rnd.uniform(0.85, 1.1))
        # 가우시안 블러 살짝 + 노이즈
        im = im.filter(ImageFilter.GaussianBlur(rnd.uniform(0.3, 0.7)))
        if noise:
            import numpy as np
            a = np.asarray(im).astype("int16")
            a = a + np.random.default_rng(seed + i).integers(-noise, noise + 1, a.shape)
            # 얼룩 몇 개
            for _ in range(rnd.randint(2, 6)):
                cx, cy, r = rnd.randint(0, a.shape[1]-1), rnd.randint(0, a.shape[0]-1), rnd.randint(8, 40)
                y0, y1 = max(0, cy - r), min(a.shape[0], cy + r); x0, x1 = max(0, cx - r), min(a.shape[1], cx + r)
                a[y0:y1, x0:x1] = a[y0:y1, x0:x1] - rnd.randint(10, 40)
            im = Image.fromarray(a.clip(0, 255).astype("uint8"))
        b = io.BytesIO(); im.save(b, format="JPEG", quality=quality); pages.append(b.getvalue())
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(img2pdf.convert(pages, layout_fun=img2pdf.get_layout_fun((img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297)))))
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[scan] {src.name} → {dst.relative_to(ROOT)} ({len(pages)}p)")

def build():
    keys = ROOT / "build" / "answer_keys"; keys.mkdir(exist_ok=True)
    # H05: 배포본은 스캔본만. 텍스트판은 정답 확인용으로 build/answer_keys 에 보관
    h05 = PDF / "hard" / "H05.pdf"
    if h05.exists():
        shutil.move(str(h05), str(keys / "H05-text.pdf"))
    scanify(keys / "H05-text.pdf", PDF / "hard" / "H05.pdf", seed=5, skew=1.8, noise=16, quality=45)
    # 쉬운 내용·어려운 형식(S 계열): E01, M03 의 스캔 변형본
    scanify(PDF / "easy" / "E01.pdf", PDF / "scanned" / "S01-E01-scan.pdf", seed=11, skew=1.0, noise=10, quality=60)
    scanify(PDF / "medium" / "M03.pdf", PDF / "scanned" / "S02-M03-scan.pdf", seed=12, skew=0.8, noise=8, quality=60)
    # 계약서 전체 스캔본 (팩스 품질)
    scanify(PDF / "hard" / "H01.pdf", PDF / "scanned" / "S03-H01-scan.pdf", seed=13, skew=2.0, noise=20, quality=40)

if __name__ == "__main__":
    build()
