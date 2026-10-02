"""Ch12 07~12절 옛 노트북·본문 생성기(개선 전 증거로 남겨 둔 파일).

이 파일이 만드는 본문과 노트북은 검토를 마친 Ch11 → Ch12 이어짐 설계와 맞지 않습니다.
"""
from __future__ import annotations

# 품질 개선(2026-09-18, Ch 12 01절, QUALITY-UPGRADE.md §8·PLAYBOOK §2-1): 이 옛 생성기는 실행하지 않습니다.
# 개선한 절은 qa/upgrade/author_NN.py 가 노트북을 쓰고 _build.py 가 본문을 빌드합니다.
# 이 파일을 실행하면 개선한 _src 와 노트북을 개선 전 판으로 덮어씁니다.
# 챕터를 마감할 때 qa/upgrade/before/generators/ 로 옮깁니다(삭제하지 않습니다).
raise SystemExit("Ch 12 품질 개선 뒤에는 이 생성기를 실행하지 않습니다. qa/upgrade/author_NN.py 와 _build.py 를 쓰세요.")

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHAPTER = ROOT / "textbook/part3/ch12-retrieval-tuning"
LAB = ROOT / "labs/part3/ch12-retrieval-tuning"
DATA = LAB / "data"
NOTEBOOKS = LAB / "notebooks"
FIGURES = CHAPTER / "figures"


def md(text: str) -> dict:
    return {"cell_type": "markdown", "id": "", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text: str) -> dict:
    return {
        "cell_type": "code", "execution_count": None, "id": "", "metadata": {},
        "outputs": [], "source": text.strip().splitlines(keepends=True),
    }


def notebook(title: str, cells: list[dict]) -> dict:
    all_cells = [md(f"# {title}\n\n이 노트북은 공개 PDF 6건과 Ch11의 30문항을 사용합니다. 첫 셀부터 순서대로 실행합니다.\n"), *cells]
    for index, cell in enumerate(all_cells, 1):
        cell["id"] = f"cell-{index:02d}"
    return {
        "cells": all_cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "lesson_format": "experiment",
        },
        "nbformat": 4, "nbformat_minor": 5,
    }


def build_data() -> None:
    from pypdf import PdfReader

    manifest = json.loads((ROOT / "labs/data/rag-corpus/manifest.json").read_text(encoding="utf-8"))
    queries = [json.loads(line) for line in (ROOT / "labs/part3/ch11-evaluation/data/evaluation-queries.jsonl").read_text(encoding="utf-8").splitlines()]
    gold_ids = {doc_id for item in queries for doc_id in item["gold_doc_ids"]}
    selected = {item["doc_id"]: item for item in manifest if item["doc_id"] in gold_ids}
    parents, chunks = [], []
    for doc_id, item in sorted(selected.items()):
        path = ROOT / "labs/data/rag-corpus" / item["file"]
        pages = [re.sub(r"\s+", " ", page.extract_text() or "").strip() for page in PdfReader(path).pages]
        full_text = "\n".join(pages)
        parents.append({"doc_id": doc_id, "title": item["title"], "text": full_text, "source": item["file"]})
        for page_no, page_text in enumerate(pages, 1):
            # 검색 단위를 충분히 작게 유지하되 문장의 절반을 자르지 않습니다.
            sentences = re.split(r"(?<=[.!?다요])\s+", page_text)
            groups = [" ".join(sentences[i:i + 3]).strip() for i in range(0, len(sentences), 3)]
            for chunk_no, text in enumerate(filter(None, groups), 1):
                chunks.append({
                    "chunk_id": f"{doc_id}-P{page_no:02d}-C{chunk_no:02d}",
                    "parent_id": doc_id, "page": page_no, "title": item["title"], "text": text,
                })
    if set(selected) != gold_ids:
        raise ValueError(f"원문이 없는 정답 문서 ID: {sorted(gold_ids - set(selected))}")
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "advanced-documents.json").write_text(json.dumps({"parents": parents, "chunks": chunks}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATA / "advanced-queries.json").write_text(json.dumps(queries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


COMMON = '''from pathlib import Path
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

root = next(path for path in [Path.cwd(), *Path.cwd().parents] if (path / "labs/part3/ch12-retrieval-tuning").exists())
data = json.loads((root / "labs/part3/ch12-retrieval-tuning/data/advanced-documents.json").read_text())
queries = json.loads((root / "labs/part3/ch12-retrieval-tuning/data/advanced-queries.json").read_text())
chunks, parents = data["chunks"], {item["doc_id"]: item for item in data["parents"]}
vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=1)
matrix = vectorizer.fit_transform([item["text"] for item in chunks])
print(f"부모 문서 {len(parents)}건 · 자식 청크 {len(chunks)}개 · 평가 질문 {len(queries)}개")'''


def write_notebooks() -> None:
    notebooks: dict[str, dict] = {}
    notebooks["07-cross-encoder-리랭킹"] = notebook("CrossEncoder로 후보를 다시 정렬하기", [
        md("## 입력 준비\n\n문자 단위 TF-IDF로 작은 후보 목록을 먼저 만듭니다. 리랭커는 이 목록 밖의 문서를 볼 수 없습니다.\n"),
        code(COMMON),
        md("## 작은 성공 예제\n\nQ009 한 문항에서 상위 8개 청크를 만들고 순서를 확인합니다.\n"),
        code('''query = next(item for item in queries if item["qid"] == "Q009")
qv = vectorizer.transform([query["question"]])
base_scores = cosine_similarity(qv, matrix)[0]
candidate_idx = np.argsort(-base_scores)[:8]
for rank, idx in enumerate(candidate_idx, 1):
    print(rank, chunks[idx]["chunk_id"], f"{base_scores[idx]:.3f}")'''),
        md("## 실제 CrossEncoder 추론\n\n질문과 후보 본문을 한 쌍으로 넣어 관련성 점수를 계산합니다.\n"),
        code('''from sentence_transformers import CrossEncoder

model_name = "BAAI/bge-reranker-v2-m3"
reranker = CrossEncoder(model_name, max_length=256, device="cpu")
pairs = [(query["question"], chunks[idx]["text"]) for idx in candidate_idx]
rerank_scores = reranker.predict(pairs, show_progress_bar=False)
order = np.argsort(-rerank_scores)
for rank, pos in enumerate(order[:5], 1):
    idx = candidate_idx[pos]
    print(rank, chunks[idx]["chunk_id"], f"{rerank_scores[pos]:.3f}")'''),
        md("## 후보 밖 문서는 회복되는가?\n\n후보 수를 2개로 줄여 정답 문서가 빠지면 리랭커가 추가할 수 없는지 확인합니다.\n"),
        code('''small_idx = np.argsort(-base_scores)[:2]
small_parents = {chunks[idx]["parent_id"] for idx in small_idx}
gold = set(query["gold_doc_ids"])
print("후보 부모 ID:", sorted(small_parents))
print("정답 문서 포함:", bool(gold & small_parents))
print("리랭커 입력 쌍 수:", len(small_idx))'''),
    ])
    notebooks["08-후보-수와-리랭커-비교"] = notebook("후보 수와 리랭커 두 모델 비교", [
        md("## 입력과 모델 준비\n\n동일한 30문항과 후보 순서를 유지하고 CrossEncoder 모델과 후보 수만 바꿉니다.\n"),
        code(COMMON),
        code('''from sentence_transformers import CrossEncoder
from time import perf_counter

model_names = ["BAAI/bge-reranker-v2-m3", "Dongjin-kr/ko-reranker"]
models = {name: CrossEncoder(name, max_length=256, device="cpu") for name in model_names}
print("모델 준비:", list(models))'''),
        md("## 평가 함수\n\n고정 후보에서 정답 부모 문서의 포함 여부와 상위 5개 순위의 nDCG@5, 실제 추론 시간을 기록합니다.\n"),
        code('''candidate_sets = {}
for item in queries:
    scores = cosine_similarity(vectorizer.transform([item["question"]]), matrix)[0]
    candidate_sets[item["qid"]] = np.argsort(-scores)[:20]

def score_fixed_candidates(model):
    started, scored = perf_counter(), {}
    for item in queries:
        idxs = candidate_sets[item["qid"]]
        pairs = [(item["question"], chunks[i]["text"]) for i in idxs]
        scored[item["qid"]] = model.predict(pairs, show_progress_bar=False)
    return scored, perf_counter() - started

def evaluate(scored, candidate_k):
    recalls, ndcgs = [], []
    for item in queries:
        idxs = candidate_sets[item["qid"]][:candidate_k]
        order = np.argsort(-scored[item["qid"]][:candidate_k])[:5]
        top_ids = list(dict.fromkeys(chunks[idxs[pos]]["parent_id"] for pos in order))
        gold = set(item["gold_doc_ids"])
        recalls.append(float(bool(gold & {chunks[i]["parent_id"] for i in idxs})))
        rank = next((i for i, doc_id in enumerate(top_ids, 1) if doc_id in gold), None)
        ndcgs.append(0.0 if rank is None else 1 / np.log2(rank + 1))
    return float(np.mean(recalls)), float(np.mean(ndcgs))'''),
        md("## 두 모델과 세 후보 수 비교\n\n총 6개 조건을 실행합니다. 결과는 이 컴퓨터에서 관찰한 값이며 다른 장치에서는 시간이 달라집니다.\n"),
        code('''rows = []
for name, model in models.items():
    scored, seconds = score_fixed_candidates(model)
    for candidate_k in (5, 10, 20):
        recall, ndcg = evaluate(scored, candidate_k)
        rows.append((name.split("/")[-1], candidate_k, recall, ndcg, seconds))
for row in rows:
    print(f"{row[0]:24s} k={row[1]:2d} recall={row[2]:.3f} nDCG={row[3]:.3f} time={row[4]:.2f}s")'''),
    ])
    notebooks["09-Parent-document-검색"] = notebook("자식 청크로 찾고 부모 문서를 반환하기", [
        md("## 입력 준비\n\n검색 점수는 자식 청크에서 계산하고, 반환 단계에서 parent_id로 원문 전체를 찾습니다.\n"),
        code(COMMON),
        md("## 작은 성공 예제\n\n한 질문에서 가장 가까운 자식 청크와 그 부모 문서를 나란히 봅니다.\n"),
        code('''question = next(item for item in queries if item["qid"] == "Q009")
scores = cosine_similarity(vectorizer.transform([question["question"]]), matrix)[0]
best = int(np.argmax(scores))
child = chunks[best]
parent = parents[child["parent_id"]]
print("자식:", child["chunk_id"], child["text"][:180])
print("부모:", parent["doc_id"], parent["title"], "글자 수", len(parent["text"]))'''),
        md("## 직접 구현\n\n여러 자식이 같은 부모를 가리킬 때 부모는 한 번만 반환합니다.\n"),
        code('''def parent_document_search(question, child_k=8, parent_k=3):
    scores = cosine_similarity(vectorizer.transform([question]), matrix)[0]
    result, seen = [], set()
    for idx in np.argsort(-scores)[:child_k]:
        parent_id = chunks[idx]["parent_id"]
        if parent_id not in seen:
            result.append(parents[parent_id])
            seen.add(parent_id)
        if len(result) == parent_k:
            break
    return result

for item in parent_document_search(question["question"]):
    print(item["doc_id"], item["title"], len(item["text"]))'''),
        md("## 청크 수 변경\n\nchild_k만 바꾸어 반환되는 부모 ID가 어떻게 달라지는지 확인합니다.\n"),
        code('''for child_k in (3, 8, 20):
    result = parent_document_search(question["question"], child_k=child_k)
    print(child_k, [item["doc_id"] for item in result])'''),
    ])
    notebooks["10-MMR-다양성-선택"] = notebook("MMR로 관련성과 다양성을 함께 고려해 선택하기", [
        md("## 입력 준비\n\n최대 주변 관련성(Maximal Marginal Relevance, MMR)을 수식 그대로 직접 구현합니다.\n"),
        code(COMMON),
        md("## MMR 함수\n\nλ가 1에 가까우면 질문 관련성을, 0에 가까우면 이미 고른 청크와의 차이를 더 크게 봅니다.\n"),
        code('''def mmr(query_vector, candidate_matrix, k=5, lambda_mult=0.5):
    relevance = cosine_similarity(query_vector, candidate_matrix)[0]
    selected, remaining = [], list(range(candidate_matrix.shape[0]))
    while remaining and len(selected) < k:
        if not selected:
            choice = max(remaining, key=lambda i: relevance[i])
        else:
            redundancy = cosine_similarity(candidate_matrix[remaining], candidate_matrix[selected]).max(axis=1)
            values = lambda_mult * relevance[remaining] - (1 - lambda_mult) * redundancy
            choice = remaining[int(np.argmax(values))]
        selected.append(choice)
        remaining.remove(choice)
    return selected'''),
        md("## λ 값 비교\n\n같은 질문과 같은 후보 행렬에서 λ만 바꿉니다.\n"),
        code('''question = "복지와 근무 제도를 비교해서 알려 주세요"
qv = vectorizer.transform([question])
for value in (1.0, 0.5, 0.2):
    chosen = mmr(qv, matrix, k=6, lambda_mult=value)
    parent_ids = [chunks[idx]["parent_id"] for idx in chosen]
    print(f"lambda={value:.1f}", parent_ids, "고유 부모", len(set(parent_ids)))'''),
        md("## 관련성 점수도 함께 읽기\n\n다양성이 커져도 질문과 무관한 결과가 선택될 수 있으므로 점수를 확인합니다.\n"),
        code('''relevance = cosine_similarity(qv, matrix)[0]
chosen = mmr(qv, matrix, k=6, lambda_mult=0.2)
for idx in chosen:
    print(chunks[idx]["chunk_id"], f"관련성={relevance[idx]:.3f}")'''),
    ])
    notebooks["11-질문-재작성과-검색"] = notebook("대화 질문을 독립 검색어로 재작성하기", [
        md("## 입력과 API 키 준비\n\n프로젝트 루트의 .env를 읽고 키의 존재만 확인합니다. 실제 값은 출력하지 않습니다.\n"),
        code(COMMON + '''
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
load_dotenv(root / ".env")
print("OPENAI_API_KEY 준비:", bool(__import__("os").getenv("OPENAI_API_KEY")))'''),
        md("## 실제 모델 호출\n\n대화 맥락이 필요한 후속 질문을 문서 검색용 한 문장으로 바꿉니다.\n"),
        code('''model = init_chat_model("openai:gpt-4.1-mini", temperature=0)
prompt = """다음 대화의 마지막 질문을 독립적인 한국어 검색 질문 한 문장으로 바꾸세요.
설명이나 따옴표를 덧붙이지 마세요.
사용자: 별빛제과의 복지 제도를 살펴보고 있어요.
사용자: 그 회사 자기계발비는 얼마예요?"""
response = model.invoke(prompt)
rewritten = response.text.strip()
print("재작성 결과:", rewritten)'''),
        md("## 원문과 재작성 질문의 검색 결과 비교\n\n검색 함수는 그대로 두고 질문 문자열만 바꿉니다.\n"),
        code('''def top_parents(question, k=5):
    scores = cosine_similarity(vectorizer.transform([question]), matrix)[0]
    return [chunks[idx]["parent_id"] for idx in np.argsort(-scores)[:k]]

original = "그 회사 자기계발비는 얼마예요?"
print("원문     :", top_parents(original))
print("재작성문 :", top_parents(rewritten))'''),
        md("## 원문과 재작성문의 순위 결합\n\n두 질문을 따로 검색한 뒤 RRF로 결합합니다. 원문 결과를 지우지 않으므로 재작성에서 빠진 표현도 후보에 남길 수 있습니다.\n"),
        code('''def ranked_indices(question, k=10):
    scores = cosine_similarity(vectorizer.transform([question]), matrix)[0]
    return list(np.argsort(-scores)[:k])

rrf_scores = {}
for ranking in (ranked_indices(original), ranked_indices(rewritten)):
    for rank, idx in enumerate(ranking, 1):
        rrf_scores[idx] = rrf_scores.get(idx, 0.0) + 1 / (60 + rank)
fused = sorted(rrf_scores, key=rrf_scores.get, reverse=True)[:5]
print("RRF 결합 :", [chunks[idx]["parent_id"] for idx in fused])'''),
        md("## 모든 질문을 재작성할 필요는 없습니다\n\n이미 기관명과 대상이 있는 Q009에는 재작성을 추가하지 않아도 되는지 비교합니다.\n"),
        code('''standalone = next(item["question"] for item in queries if item["qid"] == "Q009")
print("독립 질문:", standalone)
print("검색 결과:", top_parents(standalone))
assert "별빛제과" in standalone'''),
    ])
    notebooks["12-종합-튜닝과-실험-로그"] = notebook("30문항으로 36개 검색 설정 평가하기", [
        md("## 입력 준비\n\nCh11의 30문항과 정답 문서 ID를 읽습니다. 각 로그 행에는 설정과 세 지표를 함께 저장합니다.\n"),
        code(COMMON),
        md("## 지표와 평가 함수\n\nRecall@50은 후보 포함 여부, Precision@5와 nDCG@5는 상위 순서를 확인합니다.\n"),
        code('''def metrics(candidate_ids, top_ids, gold_ids):
    gold = set(gold_ids)
    recall = float(bool(gold & set(candidate_ids[:50])))
    recall_5 = float(bool(gold & set(top_ids[:5])))
    precision = sum(doc_id in gold for doc_id in top_ids[:5]) / 5
    gains = [1.0 if doc_id in gold else 0.0 for doc_id in top_ids[:5]]
    dcg = sum(gain / np.log2(rank + 2) for rank, gain in enumerate(gains))
    ideal = sum(1 / np.log2(rank + 2) for rank in range(min(len(gold), 5)))
    return recall_5, recall, precision, dcg / ideal if ideal else 0.0'''),
        md("## MMR 선택 함수\n\n각 실험에서 같은 직접 구현을 사용합니다.\n"),
        code('''def mmr(query_vector, candidate_matrix, k=5, lambda_mult=0.5):
    relevance = cosine_similarity(query_vector, candidate_matrix)[0]
    selected, remaining = [], list(range(candidate_matrix.shape[0]))
    while remaining and len(selected) < k:
        if not selected:
            choice = max(remaining, key=lambda i: relevance[i])
        else:
            redundancy = cosine_similarity(candidate_matrix[remaining], candidate_matrix[selected]).max(axis=1)
            values = lambda_mult * relevance[remaining] - (1 - lambda_mult) * redundancy
            choice = remaining[int(np.argmax(values))]
        selected.append(choice)
        remaining.remove(choice)
    return selected'''),
        md("## 설정 한 개 평가\n\n개발 문항과 시험 문항을 섞지 않도록 평가 대상을 인자로 받습니다.\n"),
        code('''def evaluate_config(config, subset):
    vec = TfidfVectorizer(analyzer=config["analyzer"], ngram_range=config["ngram"]).fit([c["text"] for c in chunks])
    docs, values = vec.transform([c["text"] for c in chunks]), []
    for item in subset:
        qv = vec.transform([item["question"]])
        base = cosine_similarity(qv, docs)[0]
        candidates = np.argsort(-base)[:50]
        chosen = mmr(qv, docs[candidates], k=config["report_k"], lambda_mult=config["lambda"])
        candidate_ids = list(dict.fromkeys(chunks[idx]["parent_id"] for idx in candidates))
        top_ids = list(dict.fromkeys(chunks[candidates[pos]]["parent_id"] for pos in chosen))
        values.append(metrics(candidate_ids, top_ids, item["gold_doc_ids"]))
    mean = np.mean(values, axis=0)
    return {"recall_at_5": float(mean[0]), "recall_at_50": float(mean[1]), "precision_at_5": float(mean[2]), "ndcg_at_5": float(mean[3])}'''),
        md("## 36개 개발 설정 실행\n\n문자 분석기, n-gram, 보고 순위, MMR λ를 조합합니다. 후보 수는 50으로 고정합니다. 개발 문항으로 설정을 고른 뒤 시험 문항은 한 번만 평가합니다.\n"),
        code('''from datetime import date
from itertools import product
from hashlib import sha256
from time import perf_counter

fingerprint = sha256((root / "labs/part3/ch12-retrieval-tuning/data/advanced-documents.json").read_bytes()).hexdigest()
query_fingerprint = sha256((root / "labs/part3/ch12-retrieval-tuning/data/advanced-queries.json").read_bytes()).hexdigest()
rows = []
for analyzer, ngram, report_k, lam in product(("char", "char_wb"), ((2, 3), (2, 4), (3, 5)), (3, 5), (0.4, 0.8, 1.0)):
    settings = {"analyzer": analyzer, "ngram": ngram, "candidate_k": 50, "report_k": report_k, "lambda": lam}
    dev = [item for item in queries if item["split"] == "dev"]
    started = perf_counter()
    result = evaluate_config(settings, dev)
    rows.append({"run_id": f"advanced-dev-{len(rows)+1:02d}", "run_date": str(date.today()), "corpus_sha256": fingerprint, "query_sha256": query_fingerprint, "settings": settings, "metrics": result, "duration_ms": round((perf_counter() - started) * 1000, 2), "split": "dev", "query_count": len(dev), "excluded_query_count": 0, "metrics_policy": "unique-doc-macro-v1"})
print("실험 로그 수:", len(rows))
print("첫 행:", rows[0])'''),
        md("## 로그 저장과 개발 설정 선택\n\n원자료를 JSONL로 보존하고 개발 nDCG@5가 가장 높은 행을 확인합니다.\n"),
        code('''run_dir = root / "labs/part3/ch12-retrieval-tuning/runs"
run_dir.mkdir(parents=True, exist_ok=True)
path = run_dir / "advanced-experiment-log.jsonl"
path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\\n" for row in rows))
best = max(rows, key=lambda row: row["metrics"]["ndcg_at_5"])
test = [item for item in queries if item["split"] == "test"]
test_started = perf_counter()
test_metrics = evaluate_config(best["settings"], test)
test_path = run_dir / "advanced-test-result.json"
test_path.write_text(json.dumps({"run_id": "advanced-test-01", "selected_run_id": best["run_id"], "settings": best["settings"], "metrics": test_metrics, "duration_ms": round((perf_counter() - test_started) * 1000, 2), "split": "test", "query_count": len(test), "excluded_query_count": 0, "corpus_sha256": fingerprint, "query_sha256": query_fingerprint, "metrics_policy": "unique-doc-macro-v1"}, ensure_ascii=False, indent=2))
print("저장:", path)
print("시험 결과 저장:", test_path)
print("개발 nDCG@5가 가장 높은 설정:", best["settings"])
print("개발 지표:", best["metrics"])
print("시험 지표:", test_metrics, "문항", len(test))
assert len(rows) >= 30 and len(dev) + len(test) == 30'''),
        md("## 제공 PDF 6건 통합 실행\n\n앞의 36개 행은 TF-IDF와 MMR 설정 실험입니다. 마지막에는 PDF 로딩부터 검색·리랭킹·부모 반환·답변까지 한 질문으로 연결합니다.\n"),
        code('''from pypdf import PdfReader
from time import perf_counter

integration_started = perf_counter()
loaded_pages = []
for parent in parents.values():
    pdf_path = root / "labs/data/rag-corpus" / parent["source"]
    pages = [page.extract_text() or "" for page in PdfReader(pdf_path).pages]
    loaded_pages.extend(pages)
print("PDF 6건에서 읽은 페이지:", len(loaded_pages))
assert len(loaded_pages) >= 30 and all(page.strip() for page in loaded_pages)'''),
        md("## Dense 검색과 Kiwi BM25\n\nOpenAI 임베딩과 한국어 형태소 기반 BM25를 같은 175개 청크에서 각각 실행합니다.\n"),
        code('''from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from kiwipiepy import Kiwi
from rank_bm25 import BM25Okapi

load_dotenv(root / ".env")
target = next(item for item in queries if item["qid"] == "Q009")
embedding = OpenAIEmbeddings(model="text-embedding-3-small")
dense_docs = np.array(embedding.embed_documents([item["text"] for item in chunks]))
dense_query = np.array(embedding.embed_query(target["question"]))
dense_scores = cosine_similarity([dense_query], dense_docs)[0]
kiwi = Kiwi()
tokenized = [[token.form for token in kiwi.tokenize(item["text"])] for item in chunks]
bm25 = BM25Okapi(tokenized)
sparse_scores = bm25.get_scores([token.form for token in kiwi.tokenize(target["question"])])
print("dense·sparse 점수:", len(dense_scores), len(sparse_scores))'''),
        md("## 직접 RRF와 CrossEncoder\n\n두 순위의 상위 50개를 RRF로 합친 뒤 다국어 리랭커가 상위 10개만 다시 점수화합니다.\n"),
        code('''def rrf_pair(first, second, rank_constant=60):
    scores = {}
    for ranking in (first, second):
        for rank, idx in enumerate(ranking, 1):
            scores[idx] = scores.get(idx, 0.0) + 1 / (rank_constant + rank)
    return sorted(scores, key=scores.get, reverse=True)

dense_rank = list(np.argsort(-dense_scores)[:50])
sparse_rank = list(np.argsort(-sparse_scores)[:50])
rrf_candidates = rrf_pair(dense_rank, sparse_rank)[:10]
from sentence_transformers import CrossEncoder
ce = CrossEncoder("BAAI/bge-reranker-v2-m3", max_length=256, device="cpu")
ce_scores = ce.predict([(target["question"], chunks[i]["text"]) for i in rrf_candidates], show_progress_bar=False)
reranked = [rrf_candidates[pos] for pos in np.argsort(-ce_scores)]
print("RRF→CE 상위 청크:", [chunks[i]["chunk_id"] for i in reranked[:5]])'''),
        md("## 부모 원문과 출처를 답변에 전달\n\n같은 부모를 한 번만 선택하고, 모델에는 doc_id·page·chunk_id와 부모 원문을 함께 전달합니다.\n"),
        code('''retrieved, seen = [], set()
for idx in reranked:
    child = chunks[idx]
    if child["parent_id"] in seen:
        continue
    retrieved.append({"doc_id": child["parent_id"], "page": child["page"], "chunk_id": child["chunk_id"], "text": parents[child["parent_id"]]["text"]})
    seen.add(child["parent_id"])
    if len(retrieved) == 2:
        break
context = "\\n\\n".join(f"[{item['doc_id']} p.{item['page']} {item['chunk_id']}]\\n{item['text']}" for item in retrieved)
print("부모 문서:", [(item["doc_id"], item["page"], item["chunk_id"]) for item in retrieved])'''),
        code('''from langchain.chat_models import init_chat_model

chat = init_chat_model("openai:gpt-4.1-mini", temperature=0)
prompt = f"""아래 자료만 사용해 질문에 한국어로 답하세요.
답 끝에 [doc_id p.쪽] 형식으로 출처를 표시하세요.

질문: {target['question']}

자료:
{context}"""
answer = chat.invoke(prompt).text.strip()
print("답변:", answer)'''),
        md("## 통합 결과 저장\n\n질문, 검색한 출처, 실제 응답, 전체 시간을 한 JSON 파일로 보존합니다.\n"),
        code('''integrated = {
    "run_id": "advanced-integrated-01",
    "question": target["question"],
    "retrieved": [{k: item[k] for k in ("doc_id", "page", "chunk_id")} for item in retrieved],
    "response": answer,
    "duration_ms": round((perf_counter() - integration_started) * 1000, 2),
    "settings": {"dense": "text-embedding-3-small", "sparse": "Kiwi+BM25", "fusion": "RRF(k=60)", "reranker": "BAAI/bge-reranker-v2-m3", "chat": "gpt-4.1-mini"},
}
integrated_path = run_dir / "advanced-integrated-result.json"
integrated_path.write_text(json.dumps(integrated, ensure_ascii=False, indent=2))
print("통합 결과:", integrated_path)
print("전체 시간:", integrated["duration_ms"], "ms")'''),
    ])
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    for slug, content in notebooks.items():
        (NOTEBOOKS / f"{slug}.ipynb").write_text(json.dumps(content, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


LESSONS = {
    "07-cross-encoder-리랭킹": ("CrossEncoder 리랭킹", "질문과 각 후보 본문을 함께 읽어 관련성 점수를 계산하는 교차 인코더", "08절에서 후보 수와 모델을 동시에 비교합니다."),
    "08-후보-수와-리랭커-비교": ("후보 수와 리랭커 비교", "후보 수가 검색할 수 있는 범위를 정하고 모델이 그 범위 안의 순서를 바꾸는 실험", "09절에서 작은 청크로 찾은 뒤 긴 부모 문서를 반환합니다."),
    "09-Parent-document-검색": ("Parent-document 검색", "자식 청크로 검색하고 parent_id를 따라 원문 전체를 반환하는 두 단계 검색", "10절에서 중복된 결과를 줄이는 MMR을 적용합니다."),
    "10-MMR-다양성-선택": ("MMR 다양성 선택", "질문 관련성과 이미 선택한 결과와의 차이를 한 점수로 결합하는 선택 방법", "11절에서 대화 맥락이 빠진 질문을 검색 가능한 문장으로 바꿉니다."),
    "11-질문-재작성과-검색": ("질문 재작성과 검색", "대명사와 생략된 대상을 대화 맥락으로 보충해 독립 검색 질문을 만드는 처리", "12절에서 개발·시험 질문을 구분해 설정 비교를 기록하고 통합 검색·생성을 실행합니다."),
    "12-종합-튜닝과-실험-로그": ("종합 튜닝과 실험 로그", "가설·설정·지표·날짜를 한 행에 기록해 검색 변경의 효과를 비교하는 절차", "Ch13에서 검색 결과를 생성 모델에 전달할 때 이 설정을 기준선으로 사용합니다."),
}


def lesson_html(slug: str, title: str, definition: str, next_text: str) -> str:
    num = slug[:2]
    figure = f"{num}-" + {"07":"리랭킹-흐름","08":"후보-모델-격자","09":"부모-자식-검색","10":"mmr-선택","11":"질문-재작성","12":"실험-로그"}[num]
    experiment = {
        "07": "Q009에서 8개 후보를 만든 뒤 bge-reranker-v2-m3가 계산한 점수로 상위 순서를 다시 정렬했습니다. 후보를 2개로 줄인 실행에서는 입력 목록의 부모 ID만 확인했습니다. 이 결과는 리랭커가 새 문서를 검색하지 않는다는 경계를 보여 줍니다.",
        "08": "설정 선택과 분리한 기술 비교로 30문항 전체에서 bge-reranker-v2-m3와 ko-reranker를 각각 후보 5·10·20개에 적용했습니다. 두 모델은 동일한 상위 20개 후보를 한 번씩 점수화했고, 후보 수별 계산은 그 점수를 재사용했습니다. bge 모델은 세 후보 수에서 nDCG@5 1.000, ko-reranker는 후보 5에서 0.988, 후보 10·20에서 1.000을 기록했습니다. 전체 점수화 시간은 각각 31.56초와 35.89초였습니다.",
        "09": "Q009에서 가장 가까운 자식 청크의 <code>parent_id</code>를 따라 2천 자가 넘는 원문을 반환했습니다. <code>child_k</code>를 3·8·20으로 바꾸면 발견되는 부모의 수와 순서가 달라집니다. 긴 원문을 반환했다고 답 품질이 자동으로 높아졌다고 결론 내릴 수는 없습니다.",
        "10": "같은 질문에서 λ를 1.0·0.5·0.2로 바꾸고 선택된 부모 ID의 고유 개수를 비교했습니다. λ가 작을수록 중복 억제가 강해지지만 관련성 점수가 낮은 청크가 포함될 수 있습니다. 따라서 고유 개수와 관련성 점수를 함께 읽습니다.",
        "11": "실제 채팅 모델이 ‘그 회사’를 ‘별빛제과’로 보충한 독립 질문을 반환했습니다. 원문 검색, 재작성문 검색, 두 순위의 RRF 결합을 따로 출력해 원문을 보존했습니다. API 출력은 모델 버전과 시점에 따라 달라질 수 있습니다. 이미 대상을 포함한 Q009에는 재작성을 적용하지 않습니다.",
        "12": "문자 분석기 2종, n-gram 범위 3종, 보고 순위 2종, λ 3종을 조합해 36개 개발 설정을 실행했습니다. 후보 수는 50으로 고정해 Recall@50의 의미를 유지했습니다. 개발 nDCG@5는 0.9754, 선택 설정의 시험 nDCG@5는 0.9508이었습니다. 별도 통합 실행은 PDF 6건 35쪽을 읽고 dense·Kiwi BM25·RRF·CrossEncoder·부모 반환을 거쳐 ‘연간 60만 원’과 [E02 p.3] 출처를 생성했으며 14.72초가 걸렸습니다.",
    }[num]
    diagram_reading = {
        "07": "도식은 위에서 아래로 질문, 1차 후보 8개, CrossEncoder 점수, 상위 5개 순서로 읽습니다.",
        "08": "도식은 위에서 아래로 30문항, 후보 수 세 조건, 두 모델의 고정 후보 추론, Recall·nDCG·시간 순서로 읽습니다.",
        "09": "도식은 위에서 아래로 질문, 자식 청크 검색, parent_id 조회, 부모 원문 반환 순서로 읽습니다.",
        "10": "도식은 위에서 아래로 질문 관련성, 후보 집합, MMR λ 적용, 관련성과 다양성 관찰 순서로 읽습니다.",
        "11": "도식은 위에서 아래로 대화 맥락, 후속 질문, 모델 재작성, 원문·재작성·RRF 결과 순서로 읽습니다.",
        "12": "도식은 위에서 아래로 가설, 개발 설정 36개, 선택 설정의 시험 평가 1회, JSONL 로그 순서로 읽습니다.",
    }[num]
    integration_figure = "" if num != "12" else '<h3>통합 실행 흐름</h3>{{svg:12-통합-RAG}}<p>앞 도식은 TF-IDF와 MMR의 36개 진단 실험을 보여 줍니다. 다음 도식은 제공 PDF 로딩, dense와 Kiwi BM25 검색, RRF, CrossEncoder, 부모 원문과 출처 선택, 답변 생성을 연결한 별도 통합 실행을 보여 줍니다.</p>'
    definition_detail = {
        "07": "1차 후보 목록은 리랭커가 볼 수 있는 범위입니다. 질문과 후보 본문을 한 쌍으로 입력해 점수를 계산하고, 그 점수의 내림차순으로 같은 후보를 다시 정렬합니다.",
        "08": "문항별 상위 20개 후보를 먼저 고정합니다. 두 모델은 이 목록을 각각 한 번 점수화하며 후보 5·10·20 비교는 저장한 점수를 재사용합니다.",
        "09": "자식 청크에서 검색 점수를 계산한 뒤 <code>parent_id</code>가 같은 결과를 제거합니다. 남은 ID 순서대로 부모 원문을 한 번씩 반환합니다.",
        "10": "MMR은 질문 관련성에서 이미 선택한 결과와의 최대 유사도를 뺀 결합 점수를 계산합니다. λ를 적용한 점수가 가장 큰 후보를 하나씩 반복 선택합니다.",
        "11": "입력은 대화 맥락과 후속 질문이고 출력은 독립 검색 질문입니다. 재작성문은 검색 입력으로 추가하며 원문 질문과 원문 검색 순위도 별도로 보존합니다.",
        "12": "각 개발 행은 가설, 설정, 문서·질문 SHA, 지표, 날짜, 시간을 함께 기록합니다. 개발 행으로 설정을 고른 뒤 시험 결과는 별도 run_id로 한 번 기록합니다.",
    }[num]
    cost_note = {
        "07": "로컬 CrossEncoder 추론은 API 비용이 없지만 첫 실행에서 모델 가중치를 내려받을 시간과 저장 공간이 필요합니다.",
        "08": "두 모델의 가중치가 크므로 후보 점수를 한 번 계산해 재사용합니다. 모델별 저장 공간과 CPU 시간을 실행 전에 확인합니다.",
        "09": "부모 원문을 많이 반환하면 생성 모델의 입력 토큰과 비용이 늘 수 있습니다. 부모 수와 글자 수도 로그에 남깁니다.",
        "10": "MMR 계산은 로컬에서 실행되어 API 비용이 없지만 후보 수가 늘면 후보끼리 비교하는 연산이 증가합니다.",
        "11": "짧은 질문 재작성 1회의 예상 API 비용은 미화 1달러 미만입니다. 실제 청구액은 모델 가격과 토큰 수를 확인합니다.",
        "12": "OpenAI 임베딩 175개와 답변 생성 1회의 예상 API 비용은 미화 1달러 미만입니다. 실제 청구액은 사용량 기록으로 확인합니다.",
    }[num]
    reason = {
        "07": "1차 검색 점수는 질문과 문서를 따로 표현한 뒤 비교하므로 세부 조건을 놓칠 수 있습니다. CrossEncoder는 질문과 후보 본문을 함께 읽어 같은 후보 안의 순서를 다시 정합니다. 후보 목록을 고정해야 순서 변화가 리랭커에서 왔는지 판단할 수 있습니다.",
        "08": "리랭커가 검토할 후보를 늘리면 정답 문서가 포함될 여지가 커지지만 추론 시간도 늘어납니다. 또한 모델마다 한국어 문장의 순위를 다르게 계산합니다. 같은 후보 목록을 두 모델에 입력하고 후보 수별 점수를 재사용해야 품질과 시간의 관계를 비교할 수 있습니다.",
        "09": "짧은 청크는 검색에는 유리하지만 생성 모델에 전달하면 문장의 앞뒤 근거가 잘릴 수 있습니다. 자식 청크로 위치를 찾고 부모 원문을 반환하면 검색 단위와 전달 단위를 따로 조절할 수 있습니다. 이때 부모 중복을 제거해야 같은 원문이 입력을 반복해서 차지하지 않습니다.",
        "10": "상위 결과가 같은 문서의 비슷한 청크로 채워지면 서로 다른 근거를 확인하기 어렵습니다. MMR은 질문 관련성과 선택 결과 사이의 차이를 함께 계산합니다. λ만 바꾸어 고유 부모 수와 관련성 점수를 같이 보면 다양성을 얻기 위해 무엇을 잃었는지 확인할 수 있습니다.",
        "11": "대화의 후속 질문에는 앞 문장의 기관명이나 대상이 생략될 수 있습니다. 이 질문을 그대로 검색하면 핵심 단어가 없어 관련 문서를 놓칠 수 있습니다. 원문을 보존한 채 독립 질문을 하나 더 만들고 두 순위를 따로 비교하면 재작성으로 뜻이 달라졌는지도 확인할 수 있습니다.",
        "12": "검색 설정을 여러 개 바꾸면 좋은 결과가 어느 조건에서 나왔는지 기억만으로 재현하기 어렵습니다. 가설, 입력 해시, 설정, 지표, 시간을 한 행에 남기고 개발 문항으로 설정을 선택해야 합니다. 시험 문항은 선택이 끝난 뒤 한 번만 사용해 결과에 맞춘 설정 선택을 피합니다.",
    }[num]
    summary = {
        "07": ("CrossEncoder는 고정된 1차 후보의 순서만 다시 정합니다.", "질문과 후보 본문을 함께 입력한 실제 점수를 확인했습니다."),
        "08": ("두 리랭커는 동일한 고정 후보를 한 번씩 점수화했습니다.", "후보 수별 nDCG@5와 모델별 추론 시간을 함께 비교했습니다."),
        "09": ("자식 청크의 순위를 부모 ID 순서로 변환했습니다.", "중복 부모를 제거한 뒤 부모 원문의 길이와 반환 수를 확인했습니다."),
        "10": ("MMR은 질문 관련성과 선택 결과 사이의 차이를 결합합니다.", "λ별 고유 부모 수와 관련성 점수를 함께 확인했습니다."),
        "11": ("대화 맥락과 후속 질문으로 독립 검색 질문을 만들었습니다.", "원문·재작성문·RRF 순위를 따로 보존해 의미 변화를 확인했습니다."),
        "12": ("36개 개발 로그에서 설정을 고르고 시험 문항은 한 번 평가했습니다.", "선택한 구성 요소를 실제 PDF 검색과 답변 생성까지 연결했습니다."),
    }[num]
    scope = {
        "07": ("Q009의 고정 후보로 CrossEncoder 점수와 순서 변화를 비교할 수 있습니다.", "Q009의 후보 수만 줄여 리랭커가 처리할 수 있는 범위를 확인합니다.", "이 결과는 Q009의 고정 후보에서 관찰한 실행 사례입니다."),
        "08": ("제공된 30문항으로 후보 수와 두 모델의 결과를 비교할 수 있습니다.", "30문항에서 같은 후보 목록을 사용해 후보 수와 모델 조건을 비교합니다.", "이 결과는 공개 PDF 6건과 30문항에서 관찰한 기준선입니다."),
        "09": ("Q009에서 자식 후보 수에 따른 부모 반환 결과를 비교할 수 있습니다.", "Q009에서 <code>child_k</code>만 바꾸어 부모 수와 순서 변화를 확인합니다.", "이 결과는 Q009의 자식 검색과 부모 반환에서 관찰한 실행 사례입니다."),
        "10": ("Q009에서 λ에 따른 관련성과 다양성 변화를 비교할 수 있습니다.", "Q009의 후보와 선택 수를 유지하고 λ만 바꾸어 결과를 비교합니다.", "이 결과는 Q009의 후보에 MMR을 적용해 관찰한 실행 사례입니다."),
        "11": ("대화형 후속 질문과 Q009에서 원문·재작성문 검색을 비교할 수 있습니다.", "대화형 후속 질문을 재작성하고 Q009에는 재작성을 적용하지 않는 조건을 확인합니다.", "이 결과는 대화형 후속 질문 1개와 Q009에서 관찰한 실행 사례입니다."),
        "12": ("제공된 30문항을 개발·시험으로 나누어 설정을 선택하고 평가할 수 있습니다.", "30문항을 개발 15개와 시험 15개로 나누어 설정 선택과 최종 평가를 분리합니다.", "이 결과는 공개 PDF 6건과 30문항에서 관찰한 기준선입니다."),
    }[num]
    references = {
        "07": '<li><a href="https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html">Sentence Transformers Retrieve &amp; Re-Rank</a> · 확인 2026-09-09 · Sentence Transformers 6.0.1</li><li><a href="https://huggingface.co/BAAI/bge-reranker-v2-m3">BAAI bge-reranker-v2-m3 모델 카드</a> · 확인 2026-09-09</li>',
        "08": '<li><a href="https://huggingface.co/BAAI/bge-reranker-v2-m3">BAAI bge-reranker-v2-m3 모델 카드</a> · 확인 2026-09-09</li><li><a href="https://huggingface.co/Dongjin-kr/ko-reranker">Dongjin-kr ko-reranker 모델 카드</a> · 확인 2026-09-09</li>',
        "09": '<li><a href="https://docs.haystack.deepset.ai/reference/rankers-api">Haystack Rankers API</a> · 확인 2026-09-09</li><li><a href="https://trec.nist.gov/pubs/trec30/papers/Overview-2021.pdf">TREC 2021 Overview</a> · 확인 2026-09-09</li>',
        "10": '<li><a href="https://docs.haystack.deepset.ai/reference/rankers-api">Haystack Rankers API의 MMR 설명</a> · 확인 2026-09-09</li><li><a href="https://reference.langchain.com/python/langchain-core/vectorstores/utils/maximal_marginal_relevance">LangChain MMR 참고 구현</a> · 확인 2026-09-09</li>',
        "11": '<li><a href="https://docs.langchain.com/oss/python/concepts/providers-and-models">LangChain 모델과 provider</a> · 확인 2026-09-09 · LangChain 1.4 기준</li>',
        "12": '<li><a href="https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion">Elasticsearch Reciprocal Rank Fusion</a> · 확인 2026-09-09</li><li><a href="https://github.com/bab2min/kiwipiepy">Kiwi 공식 README</a> · 확인 2026-09-09 · kiwipiepy 0.23.2</li><li><a href="https://docs.langchain.com/oss/python/concepts/providers-and-models">LangChain 모델과 provider</a> · 확인 2026-09-09 · LangChain 1.4 기준</li>',
    }[num]
    quiz2 = {
        "10": '<details class="quiz"><summary>2. 이해 — λ가 작아지면 무엇을 더 중요하게 보나요?</summary><p class="quiz-q">MMR 식에서 λ=0.2의 의미를 설명해 보세요.</p><p class="quiz-a">질문 관련성보다 이미 고른 결과와의 차이에 더 큰 비중을 둡니다. 관련성 0인 청크도 선택될 수 있으므로 점수를 함께 확인합니다. <b>오답 시 다시 볼 곳:</b> 6절 ‘실험 결과 해석’</p></details>',
        "11": '<details class="quiz"><summary>2. 이해 — 원문 질문을 왜 보존하나요?</summary><p class="quiz-q">재작성문만 검색할 때 생길 수 있는 문제를 적어 보세요.</p><p class="quiz-a">모델이 고유명사·날짜·부정 조건을 빠뜨리거나 뜻을 넓힐 수 있습니다. 원문과 재작성문을 따로 검색하고 RRF로 결합하면 두 순위를 비교할 수 있습니다. <b>오답 시 다시 볼 곳:</b> 5절 ‘원문과 재작성문의 순위 결합’</p></details>',
        "12": '<details class="quiz"><summary>2. 이해 — 개발과 시험 문항을 왜 분리하나요?</summary><p class="quiz-q">36개 설정을 시험 문항으로 고를 때 생기는 문제를 설명해 보세요.</p><p class="quiz-a">시험 결과에 맞춘 설정이 되어 새 질문에서의 품질을 과대평가할 수 있습니다. 개발 문항으로 설정을 고른 뒤 시험 문항은 한 번만 평가합니다. <b>오답 시 다시 볼 곳:</b> 6절 ‘실험 결과 해석’</p></details>',
    }.get(num, '<details class="quiz"><summary>2. 이해 — 후보 수를 늘리면 항상 좋은가요?</summary><p class="quiz-q">후보 수와 품질·비용의 관계를 설명해 보세요.</p><p class="quiz-a">후보 수를 늘리면 정답 문서가 포함될 가능성이 커질 수 있지만 리랭킹 연산과 지연도 늘어납니다. 실제 평가 지표와 시간을 함께 측정해야 합니다. <b>오답 시 다시 볼 곳:</b> 7절 ‘주의할 점과 실무 메모’</p></details>')
    quiz1 = {
        "07": '<details class="quiz"><summary>1. 이해 — 이번 절에서 고정한 조건은 무엇인가요?</summary><p class="quiz-q">리랭킹 비교에서 바꾸지 않은 입력을 두 가지 적어 보세요.</p><p class="quiz-a">Q009와 1차 검색이 만든 고정 후보 및 후보 본문을 유지했습니다. 후보가 같아야 순서 변화가 CrossEncoder 점수에서 왔는지 확인할 수 있습니다. <b>오답 시 다시 볼 곳:</b> 3절 ‘앞에서 배운 내용’</p></details>',
        "09": '<details class="quiz"><summary>1. 이해 — 이번 절에서 고정한 조건은 무엇인가요?</summary><p class="quiz-q">부모 반환 비교에서 바꾸지 않은 입력을 두 가지 적어 보세요.</p><p class="quiz-a">Q009와 같은 자식·부모 문서를 유지하고 <code>child_k</code>만 바꿨습니다. <b>오답 시 다시 볼 곳:</b> 3절 ‘앞에서 배운 내용’</p></details>',
        "10": '<details class="quiz"><summary>1. 이해 — 이번 절에서 고정한 조건은 무엇인가요?</summary><p class="quiz-q">λ 비교에서 바꾸지 않은 입력을 두 가지 적어 보세요.</p><p class="quiz-a">Q009와 고정 후보 유사도 행렬, 선택 수를 유지하고 λ만 바꿨습니다. <b>오답 시 다시 볼 곳:</b> 3절 ‘앞에서 배운 내용’</p></details>',
        "11": '<details class="quiz"><summary>1. 이해 — 이번 절에서 고정한 조건은 무엇인가요?</summary><p class="quiz-q">질문 재작성 비교에서 바꾸지 않은 입력을 적어 보세요.</p><p class="quiz-a">같은 문서 본문을 사용하고, 대화 맥락과 후속 질문의 원문을 보존했습니다. 이미 독립적인 Q009도 같은 문서에서 비교했습니다. <b>오답 시 다시 볼 곳:</b> 3절 ‘앞에서 배운 내용’</p></details>',
    }.get(num, '<details class="quiz"><summary>1. 이해 — 이번 절에서 고정한 조건은 무엇인가요?</summary><p class="quiz-q">설정 비교에서 바꾸지 않은 입력을 두 가지 적어 보세요.</p><p class="quiz-a">30개의 질문과 각 질문의 정답 문서 ID, 공개 PDF에서 추출한 본문을 유지했습니다. 입력을 고정해야 설정 변화와 결과 변화의 관계를 설명할 수 있습니다. <b>오답 시 다시 볼 곳:</b> 3절 ‘앞에서 배운 내용’</p></details>')
    quiz3 = {
        "10": '<details class="quiz"><summary>3. 적용 — 중복 결과가 많을 때 무엇을 바꾸나요?</summary><p class="quiz-q">질문과 후보를 유지한 채 실행할 비교를 적어 보세요.</p><p class="quiz-a">선택 수를 고정하고 λ만 여러 값으로 바꾸어 고유 부모 수와 관련성 점수를 함께 비교합니다. <b>오답 시 다시 볼 곳:</b> 5절 ‘λ 값 비교’</p></details>',
        "11": '<details class="quiz"><summary>3. 적용 — 어떤 질문을 재작성해야 하나요?</summary><p class="quiz-q">Q009와 “그 회사 자기계발비는?”를 비교해 판단해 보세요.</p><p class="quiz-a">Q009는 기관명과 대상이 있어 그대로 검색할 수 있습니다. “그 회사”처럼 대화 맥락 없이는 대상을 알 수 없는 후속 질문에 재작성을 적용합니다. <b>오답 시 다시 볼 곳:</b> 5절 마지막 셀</p></details>',
        "12": '<details class="quiz"><summary>3. 적용 — 실험 한 행에 무엇을 기록하나요?</summary><p class="quiz-q">재현 가능한 로그 필드를 네 가지 이상 적어 보세요.</p><p class="quiz-a">run_id, 날짜, 문서와 질문 SHA, 설정, 지표, 실행 시간, 분할, 문항 수, 지표 정책을 기록합니다. <b>오답 시 다시 볼 곳:</b> 5절 ‘36개 개발 설정 실행’</p></details>',
    }.get(num, '<details class="quiz"><summary>3. 적용 — 한 문항의 성공을 어떻게 전체 평가로 넓히나요?</summary><p class="quiz-q">작은 성공 예제 다음에 실행할 평가 절차를 적어 보세요.</p><p class="quiz-a">질문과 정답 기준을 고정하고 30문항 전체에서 같은 검색 함수를 실행한 뒤 질의별 지표의 평균과 실행 시간을 기록합니다. <b>오답 시 다시 볼 곳:</b> 5절 ‘실행 예제’</p></details>')
    quiz4 = {
        "07": '<details class="quiz"><summary>4. 분석 — 리랭커가 정답 문서를 새로 찾았나요?</summary><p class="quiz-q">후보 2개 실험의 부모 ID를 근거로 판단해 보세요.</p><p class="quiz-a">아닙니다. 리랭커는 입력받은 두 후보의 순서만 바꿨습니다. 후보에 없는 문서는 점수화할 수 없습니다. <b>오답 시 다시 볼 곳:</b> 6절 ‘실험 결과 해석’</p></details>',
        "08": '<details class="quiz"><summary>4. 분석 — 어느 모델이 항상 더 좋았나요?</summary><p class="quiz-q">후보 수별 nDCG@5와 시간을 함께 해석해 보세요.</p><p class="quiz-a">항상 우수한 모델을 정할 수 없습니다. 후보 5개에서는 bge가 높았고 10·20개에서는 두 모델이 같았습니다. 시간도 이 실행 환경에서만 관찰한 값입니다. <b>오답 시 다시 볼 곳:</b> 6절 ‘실험 결과 해석’</p></details>',
        "09": '<details class="quiz"><summary>4. 분석 — 긴 부모 원문이 답 품질을 보장하나요?</summary><p class="quiz-q">검색 지표와 생성 입력의 차이를 설명해 보세요.</p><p class="quiz-a">보장하지 않습니다. 자식 청크가 정답 문서를 찾았는지는 검색 지표로 확인할 수 있지만, 긴 부모 원문이 답변에 도움이 되는지는 생성 단계에서 별도로 평가해야 합니다. <b>오답 시 다시 볼 곳:</b> 6절 ‘실험 결과 해석’</p></details>',
        "10": '<details class="quiz"><summary>4. 분석 — 고유 부모 수가 늘면 품질도 높아졌나요?</summary><p class="quiz-q">λ=0.2 출력의 관련성 점수를 근거로 판단해 보세요.</p><p class="quiz-a">단정할 수 없습니다. 고유 부모는 5개였지만 관련성 0인 청크도 포함되었습니다. 다양성과 정확도는 별도 관찰입니다. <b>오답 시 다시 볼 곳:</b> 6절 ‘실험 결과 해석’</p></details>',
        "11": '<details class="quiz"><summary>4. 분석 — 이번 재작성으로 검색이 개선됐나요?</summary><p class="quiz-q">원문·재작성·RRF 출력을 근거로 판단해 보세요.</p><p class="quiz-a">세 결과 모두 E02를 상위에 포함했으므로 이 한 질문에서는 개선을 관찰하지 못했습니다. 재작성 문장이 더 구체적이라는 사실만 확인했습니다. <b>오답 시 다시 볼 곳:</b> 6절 ‘실험 결과 해석’</p></details>',
        "12": '<details class="quiz"><summary>4. 분석 — Recall@50=1이면 튜닝이 끝났나요?</summary><p class="quiz-q">개발·시험 nDCG@5와 함께 해석해 보세요.</p><p class="quiz-a">아닙니다. 이 말뭉치에서는 Recall@50이 포화됐지만 상위 순서는 달라질 수 있습니다. nDCG@5와 실제 통합 답변, 다른 질문 분포를 추가로 확인합니다. <b>오답 시 다시 볼 곳:</b> 6절 ‘실험 결과 해석’</p></details>',
    }.get(num, '<details class="quiz"><summary>4. 분석 — 새 문서를 추가한 로그를 이전 로그와 바로 비교할 수 있나요?</summary><p class="quiz-q">비교 가능성을 판단하고 필요한 정보를 적어 보세요.</p><p class="quiz-a">문서 집합이 달라졌으므로 바로 비교하면 안 됩니다. 문서 집합의 버전 또는 해시, 청킹 설정, 모델 이름과 버전, 실행 장치, 날짜를 남기고 같은 입력 조건의 행끼리 비교합니다. <b>오답 시 다시 볼 곳:</b> 6절 ‘실험 결과 해석’</p></details>')
    return f'''<!--meta: 강의 1h | 실습 1h | 코드 Jupyter Notebook | 새 용어 4 -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul><li>{definition}의 입력과 출력을 설명할 수 있습니다.</li><li>{scope[0]}</li><li>관찰한 수치가 설명하는 범위와 설명하지 못하는 범위를 구분할 수 있습니다.</li></ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>{reason}</p><p>Ch11에서 만든 질문과 정답 문서 ID를 유지한 채 한 조건씩 바꿉니다. {scope[1]}</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>Ch10에서 PDF를 문서와 청크로 나누고 메타데이터에 출처를 보존했습니다. Ch11의 <code>evaluation-queries.jsonl</code>은 질문마다 <code>gold_doc_ids</code>를 제공합니다. 이 절에서는 그 정답 ID에 해당하는 공개 PDF 6건을 다시 추출한 <code>advanced-documents.json</code>과 같은 30문항을 사용합니다. 앞 절의 변수나 실행 상태는 필요하지 않습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>쉬운 예</h3><p>도서관에서 책을 찾을 때 먼저 검색대가 관련 서가를 좁히고, 그 안에서 제목과 목차를 자세히 읽어 우선순위를 정한다고 생각해 봅니다. 첫 단계가 서가를 빠뜨리면 다음 단계는 그 책을 검토할 수 없습니다. 반대로 후보를 지나치게 많이 가져오면 자세히 읽는 시간이 늘어납니다.</p><h3>정의</h3><p>{definition}입니다. {definition_detail}</p><h3>도식 읽기</h3>{{{{svg:{figure}}}}}<p>{diagram_reading} 초록은 입력·문서·후보, 파랑은 직접 구현한 선택·설정, 보라는 모델 점수·질문 재작성, 노랑은 측정 결과·로그를 뜻합니다. 화살표는 데이터 전달 방향입니다.</p>{integration_figure}
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 Python 3.12 새 커널에서 실행합니다. 먼저 부모 문서 수, 자식 청크 수, 질문 수를 출력해 입력 범위를 확인합니다. 다음 셀은 가장 작은 문항 하나에서 중간 결과를 보여 줍니다. 마지막 셀은 조건을 바꾸거나 평가 범위를 넓힙니다. 출력의 문서 ID, 점수, 실행 시간 또는 로그 수를 본문 설명과 대조합니다.</p>{{{{notebook:{slug}}}}}<p class="look"><b>확인할 점</b> — 코드가 실제 검색 또는 모델 추론을 수행하는지, 정답 문서 ID를 결과 뒤에 새로 붙이지 않는지, 비교할 때 질문과 원문이 유지되는지 확인합니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>{experiment}</p><p>한 번의 출력은 이 데이터와 실행 환경에서 관찰한 결과입니다. 다른 도메인, 더 긴 문서, 다른 언어 비율에서는 순서와 시간이 달라질 수 있습니다. 설정을 채택하기 전에는 실제 서비스 질문을 같은 형식으로 추가해 다시 계산해야 합니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>이번 절의 중간 결과를 확인한 뒤 다음 단계로 전달합니다. 검색 후보, 선택 결과, 부모 원문, 재작성 질문, 로그 행은 서로 다른 데이터입니다.</li><li>실행 시간은 CPU, GPU, 배치 크기, 입력 길이, 모델 캐시에 따라 달라집니다. 장치와 패키지 버전을 로그에 함께 남깁니다.</li><li>{cost_note}</li><li>공개 PDF 6건과 30문항은 학습용 기준선입니다. 실제 서비스의 문서 분포와 질문 유형을 대신하지 않습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>{summary[0]}</li><li>{summary[1]}</li><li>{scope[2]}</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — {next_text}</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>
{quiz1}
{quiz2}
{quiz3}
{quiz4}
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul>{references}</ul>
'''


def write_lessons() -> None:
    for slug, (title, definition, next_text) in LESSONS.items():
        (CHAPTER / "_src" / f"{slug}.html").write_text(lesson_html(slug, title, definition, next_text), encoding="utf-8")


def main() -> None:
    raise SystemExit(
        "legacy generator disabled: it would overwrite the reviewed Ch12 sources and notebooks"
    )


if __name__ == "__main__":
    main()
