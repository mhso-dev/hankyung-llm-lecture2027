from __future__ import annotations

import json
import sys
from pathlib import Path

state = Path(__file__).resolve().parents[1] / "runs/deployment.json"
digest = sys.argv[1] if len(sys.argv) > 1 else ""
if not digest.startswith("sha256:") or len(digest) != 71:
    raise SystemExit("유효한 sha256 다이제스트가 필요합니다.")
state.parent.mkdir(exist_ok=True)
history = json.loads(state.read_text()) if state.exists() else []
history.append({"revision": len(history) + 1, "event": "deploy", "digest": digest, "status": "ready"})
state.write_text(json.dumps(history, indent=2) + "\n")
print(f"deployed revision={len(history)} digest={digest[:19]}...")
