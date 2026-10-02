from __future__ import annotations

import json
from pathlib import Path

state = Path(__file__).resolve().parents[1] / "runs/deployment.json"
history = json.loads(state.read_text())
deployments = [event for event in history if event["event"] == "deploy"]
if len(deployments) < 2:
    raise SystemExit("되돌릴 이전 리비전이 없습니다.")
source, target = deployments[-1], deployments[-2]
history.append({
    "revision": len(history) + 1,
    "event": "rollback",
    "source_revision": source["revision"],
    "target_revision": target["revision"],
    "digest": target["digest"],
    "reason": "health-check-failed",
    "status": "ready-after-rollback",
})
state.write_text(json.dumps(history, indent=2) + "\n")
print(f"rolled back {source['revision']} -> {target['revision']}")
