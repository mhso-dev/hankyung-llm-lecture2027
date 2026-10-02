"""02절 일괄 처리 제출 — 한 번만. ID는 resume/ids.json에만 적고, 화면에는 앞 몇 자만 찍는다."""
import datetime
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, "/tmp/ch34-02")
import cells_input  # noqa: E402
from dotenv import load_dotenv  # noqa: E402
from openai import OpenAI  # noqa: E402

ROOT = Path(os.environ["HOME"]) / "mnt/한국경제신문"
RESUME = ROOT / ".cache/ch34-02/resume"
IDS = RESUME / "ids.json"
EXPECT = "6ea21c43d31e390d12efa718adff4e9411b4b26176cd87baaae46f5da8c5ca4d"

if IDS.exists():
    raise SystemExit("resume/ids.json이 있어 제출하지 않습니다(한 번 조건)")
namespace = {}
input_path = cells_input.build(namespace)
data = open(input_path, "rb").read()
sha = hashlib.sha256(data).hexdigest()
assert sha == EXPECT, sha
if os.environ.get("DRY") != "1":
    load_dotenv(ROOT / ".env")
client = OpenAI(max_retries=0)
t0 = datetime.datetime.now(datetime.timezone.utc)
with open(input_path, "rb") as file:
    uploaded = client.files.create(file=file, purpose="batch")
t1 = datetime.datetime.now(datetime.timezone.utc)
record = {"file_id": uploaded.id, "input_sha256": sha, "upload_started": t0.isoformat(), "uploaded_at": t1.isoformat()}
IDS.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
batch = client.batches.create(
    input_file_id=uploaded.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={"note": "ch34-02 textbook batch, five lines"},
)
t2 = datetime.datetime.now(datetime.timezone.utc)
record["batch_id"] = batch.id
record["created_at"] = t2.isoformat()
record["status_at_create"] = batch.status
IDS.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
(RESUME / "raw-batch-create.json").write_text(batch.model_dump_json(indent=1), encoding="utf-8")
print("올린 파일 ID 앞:", uploaded.id[:8], "· 크기:", len(data))
print("작업 ID 앞:", batch.id[:10])
print("만든 시각:", t2.isoformat(), "· 상태:", batch.status)
