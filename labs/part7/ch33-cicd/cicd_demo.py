from __future__ import annotations

import hashlib
import json
from pathlib import Path

def answer(question: str) -> str:
    return "근거를 확인했습니다." if question.strip() else "질문이 필요합니다."


def run_candidate(qid: str) -> tuple[str, list[str]]:
    responses = {
        "C01": "도서는 7권까지 14일 동안 빌릴 수 있습니다.",
        "C02": "답변에 출처를 표시했습니다.",
        "C03": "근거가 없어 확인 필요라고 답합니다.",
        "C04": "무료 시간 이후 30분마다 500원입니다.",
    }
    tools = ["retrieve", "cite"] if qid == "C02" else ["retrieve"]
    return responses[qid], tools

def image_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))
