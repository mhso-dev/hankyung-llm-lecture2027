from __future__ import annotations

import json
import sys
from pathlib import Path

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1] / "data/metrics.jsonl"
rows = sorted((json.loads(line) for line in path.read_text().splitlines()), key=lambda row: row["minute"])
streak = longest = 0
for row in rows:
    violation = row["errors"] / row["requests"] > 0.05 and row["p95_ms"] > 800
    streak = streak + 1 if violation else 0
    longest = max(longest, streak)
    print(row["minute"], round(row["errors"] / row["requests"], 3), row["p95_ms"], violation)
print("alert:", "FIRING" if longest >= 2 else "OK", f"longest_streak={longest}")
sys.exit(1 if longest >= 2 else 0)
