from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from cicd_demo import run_candidate  # noqa: E402

baseline = json.loads((root / "data/regression-baseline.json").read_text())
cases = json.loads((root / "data/regression-current.json").read_text())["cases"]
results = [run_candidate(case["qid"]) for case in cases]
facts = [all(fact in response for fact in case["required_facts"]) for case, (response, _) in zip(cases, results)]
groundedness = sum(facts) / len(facts)
extra_calls = sum(
    max(0, len(tools) - len(case["expected_tools"])) for case, (_, tools) in zip(cases, results)
)
checks = {
    "groundedness": groundedness >= baseline["groundedness"],
    "trajectory": extra_calls <= baseline["trajectory_extra_calls"],
}
print(f"groundedness={groundedness:.2f} required={baseline['groundedness']:.2f}")
print(f"trajectory_extra_calls={extra_calls} allowed={baseline['trajectory_extra_calls']}")
for name, passed in checks.items():
    print(f"{name}: {'PASS' if passed else 'FAIL'}")
sys.exit(0 if all(checks.values()) else 1)
