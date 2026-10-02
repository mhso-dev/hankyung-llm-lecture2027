"""받은 결과·오류 파일과 작업 객체(ID 포함, resume/)에서, 실행마다 다른 값을 뺀 자료 파일 셋을 만든다.

뺀 것: 줄 id(batch_req_…)·response.request_id·body.id(chatcmpl-…)·body.created·object·service_tier·system_fingerprint·
message.refusal·annotations·completion_tokens_details·prompt_tokens_details.audio_tokens · 작업 ID·파일 ID·시각 칸·metadata.
줄 차례는 받은 파일 그대로. 쓰기는 없을 때만(있으면 내용이 같은지만 봄).
"""
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(os.environ["HOME"]) / "mnt/한국경제신문"
RESUME = ROOT / ".cache/ch34-02/resume"
DATA = ROOT / "labs/part7/ch34-cost-rate-limits/data"


def read_lines(path):
    rows = []
    for text in path.read_text(encoding="utf-8").split("\n"):
        if text != "":
            rows.append(json.loads(text))
    return rows


def output_row(raw):
    body = raw["response"]["body"]
    choice = body["choices"][0]
    usage = body["usage"]
    return {
        "custom_id": raw["custom_id"],
        "response": {
            "status_code": raw["response"]["status_code"],
            "body": {
                "model": body["model"],
                "choices": [{"index": choice["index"],
                             "message": {"role": choice["message"]["role"], "content": choice["message"]["content"]},
                             "finish_reason": choice["finish_reason"]}],
                "usage": {"prompt_tokens": usage["prompt_tokens"], "completion_tokens": usage["completion_tokens"],
                          "total_tokens": usage["total_tokens"],
                          "prompt_tokens_details": {"cached_tokens": usage["prompt_tokens_details"]["cached_tokens"]}},
            },
        },
        "error": raw["error"],
    }


def error_row(raw):
    err = raw["response"]["body"]["error"]
    return {
        "custom_id": raw["custom_id"],
        "response": {"status_code": raw["response"]["status_code"],
                     "body": {"error": {"message": err["message"], "type": err["type"], "param": err["param"], "code": err["code"]}}},
        "error": raw["error"],
    }


def job_row(raw):
    return {"endpoint": raw["endpoint"], "completion_window": raw["completion_window"], "model": raw["model"],
            "status": raw["status"], "request_counts": raw["request_counts"], "usage": raw["usage"]}


def put(path, text):
    if path.exists():
        assert path.read_text(encoding="utf-8") == text, path
        print("same", path.name)
    else:
        path.write_text(text, encoding="utf-8")
        print("wrote", path.name)


outs = [output_row(r) for r in read_lines(RESUME / "raw-output.jsonl")]
errs = [error_row(r) for r in read_lines(RESUME / "raw-errors.jsonl")]
job = job_row(json.loads((RESUME / "raw-batch-final.json").read_text(encoding="utf-8")))
out_text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in outs)
err_text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in errs)
job_text = json.dumps(job, ensure_ascii=False, indent=1) + "\n"
if "--write" in sys.argv:
    DATA.mkdir(exist_ok=True)
    put(DATA / "batch-output.jsonl", out_text)
    put(DATA / "batch-errors.jsonl", err_text)
    put(DATA / "batch-job.json", job_text)
else:
    print(out_text + err_text + job_text)
# 남긴 글에 ID·시각 모양이 없는지
for text in (out_text, err_text, job_text):
    for bad in ("batch_req_", "chatcmpl-", "file-", "batch_6", "request_id", "created", "1790"):
        assert bad not in text, bad
print("no ids/time ok")
