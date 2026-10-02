"""02절 일괄 처리 상태 확인(한 번 부를 때 retrieve 한 번). 끝나면 결과·오류 파일을 resume/에 내려받는다."""
import datetime
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from dotenv import load_dotenv  # noqa: E402
from openai import OpenAI  # noqa: E402

ROOT = Path(os.environ["HOME"]) / "mnt/한국경제신문"
RESUME = ROOT / ".cache/ch34-02/resume"
record = json.loads((RESUME / "ids.json").read_text(encoding="utf-8"))
load_dotenv(ROOT / ".env")
client = OpenAI()
now = datetime.datetime.now(datetime.timezone.utc)
created = datetime.datetime.fromisoformat(record["created_at"])
batch = client.batches.retrieve(record["batch_id"])
elapsed = (now - created).total_seconds()
line = {"checked_at": now.isoformat(), "elapsed_s": round(elapsed), "status": batch.status,
        "request_counts": batch.request_counts.model_dump() if batch.request_counts else None}
with open(RESUME / "polls.jsonl", "a", encoding="utf-8") as file:
    file.write(json.dumps(line, ensure_ascii=False) + "\n")
print(json.dumps(line, ensure_ascii=False))
if batch.status in ("completed", "failed", "expired", "cancelled"):
    (RESUME / "raw-batch-final.json").write_text(batch.model_dump_json(indent=1), encoding="utf-8")
    if batch.output_file_id:
        (RESUME / "raw-output.jsonl").write_bytes(client.files.content(batch.output_file_id).read())
        print("결과 파일 내려받음")
    if batch.error_file_id:
        (RESUME / "raw-errors.jsonl").write_bytes(client.files.content(batch.error_file_id).read())
        print("오류 파일 내려받음")
    print("errors:", batch.errors)
