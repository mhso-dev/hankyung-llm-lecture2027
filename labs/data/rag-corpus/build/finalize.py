# -*- coding: utf-8 -*-
"""질의셋(정답 문서 ID·페이지) + manifest 생성. 페이지는 PDF 텍스트에서 정답 토큰을 찾아 실측한다."""
import json, re, csv
from pathlib import Path
from pypdf import PdfReader
from common import ROOT, PDF
import easy, medium, hard

def page_texts(pdf: Path):
    return [(p.extract_text() or "") for p in PdfReader(str(pdf)).pages]

def tokens(s: str):
    s = re.sub(r"\(.*?\)", " ", s)  # 괄호 안 보조 설명 제외
    t = re.findall(r"[가-힣A-Za-z]{2,}|\d[\d,\.]*", s)
    return [x for x in t if x not in {"이상","이하","이내","가능","불가","동일","기준","경우","원","만","억"}]

def norm(s): return s.replace(" ", "").replace(",", "")

def gold_pages(texts, query):
    toks = tokens(query["answer"]) + tokens(query["anchor"])
    scores = []
    for i, t in enumerate(texts):
        nt = norm(t)
        hit = sum(1 for k in toks if norm(k) in nt)
        scores.append((hit, i + 1))
    best = max(h for h, _ in scores)
    if best == 0: return []
    return [p for h, p in scores if h >= best][:2]

def build():
    Q = []
    tier_of = {}
    for mod, tier in ((easy, "easy"), (medium, "medium"), (hard, "hard")):
        for qd in mod.QUERIES if mod.QUERIES else mod.build():
            qd["tier"] = tier; Q.append(qd)
    # 텍스트 소스: H05는 스캔본이므로 answer_keys 텍스트판으로 페이지 산정
    cache = {}
    def texts_for(doc):
        if doc in cache: return cache[doc]
        tier = Q_tier[doc]
        src = PDF / tier / f"{doc}.pdf"
        if doc == "H05":
            k = ROOT / "build" / "answer_keys" / "H05-text.pdf"
            if k.exists(): src = k
        cache[doc] = page_texts(src); return cache[doc]
    Q_tier = {q["doc_id"]: q["tier"] for q in Q}
    out = []
    for i, qd in enumerate(Q, 1):
        gp = gold_pages(texts_for(qd["doc_id"]), qd)
        if qd["type"] in ("image", "ocr") and not gp: gp = []
        out.append(dict(qid=f"Q{i:03d}", tier=qd["tier"], doc_id=qd["doc_id"], question=qd["question"],
                        answer=qd["answer"], type=qd["type"], gold_pages=gp, anchor=qd["anchor"], answerable=True))
    n = len(out)
    # 교차 문서 질의 (여러 문서를 함께 검색해야 답이 나옴)
    cross = [
        ("E03+M01", ["E03","M01"], "R2를 완충하면 몇 시간 쓸 수 있나요? 빠른 시작 가이드와 사양서의 설명이 다른 이유는?", "가이드의 '최대 8시간'은 대기 기준, 사양서 §4.3은 주행 5.5h·운반 4.5h 등 조건별 수치를 제시(사양서 §1이 이를 명시)", "multi_doc"),
        ("E02+M03", ["E02","M03"], "별빛제과 신입사원이 공장 '노란 구역'에 들어가려면 무엇이 필요하고, 그 구역에서 다루는 원료의 예는?", "알레르기 교육 이수 필요(온보딩 §7); 대장 §3에 공장별 취급 원료(밀·우유·달걀·땅콩 등)", "multi_doc"),
        ("E04+M02", ["E04","M02"], "청담해운 해상 직원의 승선 최대 기간과, 청담해운이 운영하는 정기 항로 수는?", "승선 최대 6개월(복지 안내 §5), 정기 항로 5개(약관 제3조 / 복지 안내 §1)", "multi_doc"),
        ("M01+H01", ["M01","H01"], "R2에 들어가는 라이다 모듈의 감지 거리와 누리테크 공급 단가는?", "0.05~8m(사양서 §4.1), NT-LD-16 단가 184,000원(계약 별첨 1, 2026.2~)", "multi_doc"),
        ("M06+H02", ["M06","H02"], "한빛 화재공제의 자기부담금은 안내서와 약관에서 각각 어떻게 되어 있나요?", "안내서(M06)에는 화재공제 자기부담금 언급 없음(배상책임 10만 원만), 약관 제4조 제1항은 사고당 20만 원 — 약관이 우선(M06 §1)", "multi_doc"),
        ("M03+H06", ["M03","H06"], "별빛제과 L1 라인 땅콩·호두 혼입 가능 표시 제외의 근거를 감사 보고서는 어떻게 평가했나요?", "표시 대장 §5(ATP 3회 적합, 2026.1.20 승인)를 HACCP 감사 §3 알레르기 관리에서 '기록 적정'으로 확인", "multi_doc"),
        ("M04+H03", ["M04","H03"], "2025년 하반기 계획의 청년 참여 목표 25%는 달성되었나요? 그 결과 2026년 청년 예산은?", "미달(22%, H03 윤서아 질의) — 그럼에도 청년 프로그램 4.2억→5억으로 증액(버스킹 만족도 4.4)", "multi_doc"),
        ("H04 vs M01", ["H04","M01"], "오로라 로보틱스의 2025년 3분기 사고 건수는 몇 건인가요?", "해당 없음 — 사고 통계는 오로라 '로지스틱스'(별개 회사) 문서. 로보틱스 문서에는 사고 통계가 없음", "disambiguation"),
    ]
    for i, (tag, docs, qq, aa, tp) in enumerate(cross, 1):
        out.append(dict(qid=f"X{i:02d}", tier="cross", doc_id="+".join(docs), question=qq, answer=aa, type=tp, gold_pages=[], anchor=tag, answerable=True))
    # 답이 없는 질의 (환각 검사용)
    unans = [
        ("E01", "미르시립도서관의 2025년 연간 방문자 수는?"), ("E03", "도우미봇 R2의 출시 가격은 얼마인가요?"),
        ("M02", "청담해운의 국제 항로 운임은 얼마인가요?"), ("M05", "누리테크의 2025년 신입 채용 인원은?"),
        ("H01", "누리테크가 오로라 로보틱스에 공급하는 배터리 팩의 단가는?"), ("H03", "제312회 정례회에서 복지국 예산은 어떻게 결정되었나요?"),
        ("H02", "한빛 화재공제의 2026년 공제료 인상률은?"), ("M04", "2025년 하반기 미르강 가을축제의 실제 방문객 수는?"),
        ("E05", "강릉 바다마을 여행 상품의 겨울 시즌 가격은?"), ("H06", "평택 3공장 L7 라인 감사 결과 부적합 건수는?"),
    ]
    for i, (d, qq) in enumerate(unans, 1):
        out.append(dict(qid=f"N{i:02d}", tier=Q_tier[d], doc_id=d, question=qq, answer="문서에 없음 — '알 수 없다'고 답해야 함", type="unanswerable", gold_pages=[], anchor="-", answerable=False))
    (ROOT / "queries.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in out) + "\n", encoding="utf-8")
    with open(ROOT / "queries.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader()
        for x in out: w.writerow({**x, "gold_pages": ";".join(map(str, x["gold_pages"]))})
    # manifest
    parts = sorted((ROOT / "build" / "manifest_parts").glob("*.json"))
    man = [json.loads(p.read_text(encoding="utf-8")) for p in parts]
    for m in man:
        if m["doc_id"] == "H05": m["note"] = "배포본은 텍스트 레이어 없는 스캔 이미지 PDF. 텍스트판은 build/answer_keys/H05-text.pdf"
    for sid, src, note in (("S01", "E01", "쉬운 내용·스캔 형식(기울기 1°, 노이즈)"), ("S02", "M03", "기호 표(●△)를 OCR로 읽어야 함"), ("S03", "H01", "팩스 품질 스캔, 서명면 포함")):
        base = next(m for m in man if m["doc_id"] == src)
        man.append(dict(doc_id=sid, tier="scanned", title=base["title"] + " (스캔본)", file=f"pdf/scanned/{sid}-{src}-scan.pdf",
                        pages=base["pages"], org=base["org"], genre=base["genre"] + "·스캔", difficulty_reason=note, source_doc=src))
    (ROOT / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"queries {len(out)} (answerable {n}, cross {len(cross)}, unanswerable {len(unans)}); docs {len(man)}")
    missing = [x["qid"] for x in out if x["answerable"] and x["tier"] != "cross" and not x["gold_pages"]]
    print("gold_pages 미산정:", missing)

if __name__ == "__main__":
    build()
