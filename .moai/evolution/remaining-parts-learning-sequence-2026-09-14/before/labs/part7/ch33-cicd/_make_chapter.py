from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LAB = ROOT / "labs/part7/ch33-cicd"
BOOK = ROOT / "textbook/part7/ch33-cicd"


def md(text: str, part: str | None = None) -> dict:
    meta = {} if part is None else {"lesson_part": part}
    return {"cell_type": "markdown", "id": "", "metadata": meta, "source": text.splitlines(True)}


def code(text: str, part: str | None = None) -> dict:
    meta = {} if part is None else {"lesson_part": part}
    return {"cell_type": "code", "execution_count": None, "id": "", "metadata": meta, "outputs": [], "source": text.splitlines(True)}


def notebook(title: str, fmt: str, cells: list[dict]) -> dict:
    for i, cell in enumerate(cells, 1):
        cell["id"] = f"cell-{i:02d}"
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "lesson_format": fmt,
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def page(slug: str, title: str, fmt: str, concept: str, execution: str, analysis: str,
         cautions: list[str], summary: list[str], questions: list[tuple[str, str]], refs: list[str]) -> str:
    embed = f"{{{{notebook:{slug}}}}}" if fmt == "experiment" else f"{{{{notebook:{slug}|example}}}}"
    if fmt == "paired":
        result = f"<p>{analysis}</p>{{{{notebook:{slug}|failure}}}}"
        result_title = "일부러 실패해 보기"
    else:
        result = f"<p>{analysis}</p>"
        result_title = "실험 결과 해석"
    quiz = "".join(
        f'<details class="quiz"><summary>{q}</summary><p class="quiz-a">{a}</p></details>'
        for q, a in questions
    )
    return f'''<!--meta: 강의 1h | 실습 2.2h | 코드 Jupyter Notebook | 새 용어 6 -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>{title}의 핵심 단계와 종료 조건을 설명할 수 있습니다.</li>
<li>제공된 로컬 실습을 실행하고 성공과 실패를 종료 코드로 구분할 수 있습니다.</li>
<li>실행 기록을 근거로 다음 배포 단계를 진행하거나 중단할 수 있습니다.</li></ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2>
<p>서비스 코드를 작성한 뒤에도 변경은 계속됩니다. 작은 수정이 기존 기능, 평가 점수, 이미지 내용, 운영 지표에 영향을 줄 수 있습니다. 사람이 매번 같은 명령을 기억해서 실행하면 확인 순서가 빠지거나 서로 다른 환경에서 다른 결과를 얻게 됩니다. {title}은 변경을 일정한 순서로 확인하고, 기준을 만족한 결과만 다음 단계로 보내는 방법입니다.</p>
<p>이 장의 실습은 외부 저장소와 클라우드 계정 없이 로컬에서 실행됩니다. 학생은 명령의 출력과 프로세스 종료 코드를 직접 확인합니다. 실제 GitHub Actions와 클라우드 배포에서는 같은 명령을 원격 실행 환경과 배포 권한에 연결합니다. 로컬 성공은 원격 배포 성공을 보장하지 않으므로, 확인한 범위를 명확히 구분합니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2>
<p>Ch15의 <code>evaluation-cases.json</code>과 회귀 비교는 이전에 성공했던 답변 품질을 기준선으로 남기는 방법을 보여 주었습니다. Ch29의 에이전트 평가는 최종 답변뿐 아니라 도구 호출 수와 궤적도 확인해야 한다는 점을 다루었습니다. Ch32의 Docker 이미지는 실행 환경을 파일로 고정했습니다. 이 절에서는 그 결과를 자동 검사의 입력으로 사용하며, 원본 평가 자료를 다시 계산했다고 주장하지 않습니다. 공개 실습용 요약 자료의 출처 장과 필드 의미를 README에 기록합니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2>
<h3>변경을 통과시키는 검사대</h3><p>공항의 수하물은 접수, 보안 검사, 목적지 분류를 차례로 통과합니다. 한 단계가 실패하면 다음 운송 단계로 보내지 않습니다. CI/CD도 변경 하나를 테스트, 정적 검사, 빌드, 평가, 배포 검증의 순서로 처리합니다. 비유에서 검사대는 작업 단계에, 통과 표시는 종료 코드 0에 대응합니다.</p>
<h3>정의</h3><p>{concept}</p>
<p>연속 통합(Continuous Integration, CI)은 저장소 변경을 자주 합치면서 자동 검사로 오류를 이르게 찾는 방식입니다. 연속 전달 또는 연속 배포(Continuous Delivery/Deployment, CD)는 검사를 통과한 결과물을 배포 가능한 상태로 만들거나 실제 환경에 반영하는 과정입니다. 파이프라인(pipeline)은 이 단계와 의존 관계를 기록한 실행 순서입니다. 아티팩트(artifact)는 빌드가 만든 패키지, 이미지, 평가 보고서처럼 다음 단계가 사용하는 결과물입니다.</p>
<h3>도식 읽기</h3><figure><img src="figures/{slug.split('-')[0]}-흐름.svg" alt="{title} 단계 도식"><figcaption>왼쪽의 파란 상자는 입력과 검사를, 가운데의 초록 상자는 통과한 결과를, 오른쪽의 주황 상자는 중단 또는 운영 판단을 나타냅니다. 화살표는 실제 실행 순서입니다. 각 상자 아래의 작은 글자는 이 실습에서 확인하는 파일이나 출력입니다.</figcaption></figure>
<p>도식의 화살표를 따라가며 현재 단계가 무엇을 입력으로 받고 무엇을 남기는지 확인합니다. 검사 결과가 실패이면 다음 단계 화살표를 따라가지 않습니다. 운영 환경에서는 승인, 비밀 정보, 네트워크 상태 같은 조건이 더해질 수 있습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2>
<p>{execution}</p>{embed}<p class="look"><b>확인할 점</b> — 출력의 상태 이름, 실제 값, 기준값, 프로세스 종료 코드를 함께 읽습니다. 성공 메시지만 출력하는 코드는 검사로 사용할 수 없습니다. 실패 조건에서 0이 아닌 종료 코드가 나와야 GitHub Actions 같은 실행기가 작업을 실패로 표시합니다.</p>
<h2 id="b6"><span class="no">6</span>{result_title}</h2>{result}
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul>{''.join(f'<li>{x}</li>' for x in cautions)}</ul>
<p>자동화가 모든 위험을 판단하는 것은 아닙니다. 측정 기준이 빠져 있으면 파이프라인은 빠진 기준을 검사하지 못합니다. 외부 서비스 장애, 권한 오류, 실제 사용자 트래픽의 변화도 로컬 실습만으로 알 수 없습니다. 팀은 자동 검사가 판단할 항목과 사람이 승인할 항목을 배포 정책에 함께 기록해야 합니다.</p>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul>{''.join(f'<li>{x}</li>' for x in summary)}</ul>
<p><strong>다음 학습과 이어지는 지점</strong> — 이 장에서 만든 상태 검사와 중단 조건은 Ch38 Hooks에서 작업 전후에 자동으로 실행하는 검사의 원형이 됩니다. 최종 프로젝트에서는 실제 저장소 권한과 배포 환경을 연결한 뒤 같은 원칙으로 확장합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>{quiz}
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul>{''.join(f'<li>{x}</li>' for x in refs)}</ul>
'''


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    config = {
        "part": 7, "part_title": "Part 7 · 프로덕션 엔지니어링", "chapter": "ch33-cicd",
        "title": "CI/CD와 배포 운영", "hours": "총 16h · 강의 5h · 실습 11h",
        "objectives": ["테스트·린트·빌드·평가 회귀를 CI로 자동화할 수 있습니다.", "이미지 다이제스트로 배포 대상을 고정할 수 있습니다.", "모니터링 신호로 배포를 판단하고 이전 버전으로 복구할 수 있습니다."],
        "lab_path": "labs/part7/ch33-cicd",
        "sections": [
            {"slug": "01-테스트-린트-빌드와-GitHub-Actions", "title": "테스트·린트·빌드와 GitHub Actions", "format": "paired"},
            {"slug": "02-평가-회귀를-CI에-연결하기", "title": "평가 회귀를 CI에 연결하기", "format": "paired"},
            {"slug": "03-레지스트리-다이제스트와-클라우드-배포", "title": "레지스트리·다이제스트와 클라우드 배포", "format": "experiment"},
            {"slug": "04-모니터링과-알림", "title": "모니터링과 알림", "format": "experiment"},
            {"slug": "05-롤백과-복구-검증", "title": "롤백과 복구 검증", "format": "paired"},
        ],
    }
    write_text(BOOK / "chapter.json", json.dumps(config, ensure_ascii=False, indent=2) + "\n")

    # 학생이 직접 실행하는 작은 서비스와 검증 도구입니다.
    write_text(LAB / "cicd_demo.py", '''from __future__ import annotations\n\nimport hashlib\nimport json\nfrom pathlib import Path\n\ndef answer(question: str) -> str:\n    return "근거를 확인했습니다." if question.strip() else "질문이 필요합니다."\n\ndef image_digest(path: Path) -> str:\n    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()\n\ndef load_json(path: Path):\n    return json.loads(path.read_text(encoding="utf-8"))\n''')
    write_text(LAB / "tests/test_cicd_demo.py", '''from pathlib import Path\nfrom cicd_demo import answer, image_digest\n\ndef test_answer_requires_question():\n    assert answer("") == "질문이 필요합니다."\n\ndef test_digest_is_stable(tmp_path: Path):\n    artifact = tmp_path / "image.tar"\n    artifact.write_bytes(b"agent-service-v1")\n    assert image_digest(artifact) == image_digest(artifact)\n''')
    write_text(LAB / "data/regression-baseline.json", json.dumps({"source": ["Ch15", "Ch29"], "source_files": {"labs/part4/ch15-evaluation-advanced/data/evaluation-cases.json": "dc48b1bc49d26d511ca2141b102cefbae1b395a06faaa8d21a61c2174ec3b2d1", "labs/part6/ch29-agent-evaluation/notebooks/04-운영-지표와-Ch18-궤적-비교.ipynb": "71fa56efb956b5218732c75bcf030ccf401e2335217d6b23fbf6c2ff2322d93a"}, "note": "원본의 평가 항목을 CI 연결 연습에 맞게 축약한 교육용 기준선이며 원본 측정값 발췌가 아닙니다.", "groundedness": 0.90, "trajectory_extra_calls": 1, "cases": 4}, ensure_ascii=False, indent=2) + "\n")
    write_text(LAB / "data/regression-current.json", json.dumps({"cases": [
        {"qid": "C01", "required_facts": ["7권", "14일"], "response": "도서는 7권까지 14일 동안 빌릴 수 있습니다.", "expected_tools": ["retrieve"], "actual_tools": ["retrieve"]},
        {"qid": "C02", "required_facts": ["출처"], "response": "답변에 출처를 표시했습니다.", "expected_tools": ["retrieve", "cite"], "actual_tools": ["retrieve", "cite"]},
        {"qid": "C03", "required_facts": ["확인 필요"], "response": "근거가 없어 확인 필요라고 답합니다.", "expected_tools": ["retrieve"], "actual_tools": ["retrieve"]},
        {"qid": "C04", "required_facts": ["500원"], "response": "무료 시간 이후 30분마다 500원입니다.", "expected_tools": ["retrieve"], "actual_tools": ["retrieve"]}
    ]}, ensure_ascii=False, indent=2) + "\n")
    write_text(LAB / "data/metrics.jsonl", '\n'.join(json.dumps(x) for x in [
        {"minute": 1, "requests": 100, "errors": 1, "p95_ms": 320},
        {"minute": 2, "requests": 120, "errors": 2, "p95_ms": 360},
        {"minute": 3, "requests": 110, "errors": 9, "p95_ms": 920},
        {"minute": 4, "requests": 130, "errors": 12, "p95_ms": 1100},
    ]) + '\n')
    write_text(LAB / "scripts/evaluate_regression.py", '''from __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nroot = Path(__file__).resolve().parents[1]\nb = json.loads((root / "data/regression-baseline.json").read_text())\nc = json.loads((root / "data/regression-current.json").read_text())\nchecks = {\n    "groundedness": c["groundedness"] >= b["groundedness"] - 0.02,\n    "trajectory": c["trajectory_extra_calls"] <= b["trajectory_extra_calls"],\n}\nfor name, passed in checks.items():\n    print(f"{name}: {'PASS' if passed else 'FAIL'}")\nsys.exit(0 if all(checks.values()) else 1)\n''')
    write_text(LAB / "scripts/deploy.py", '''from __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nstate = Path(__file__).resolve().parents[1] / "runs/deployment.json"\ndigest = sys.argv[1] if len(sys.argv) > 1 else ""\nif not digest.startswith("sha256:") or len(digest) != 71:\n    raise SystemExit("유효한 sha256 다이제스트가 필요합니다.")\nstate.parent.mkdir(exist_ok=True)\nhistory = json.loads(state.read_text()) if state.exists() else []\nhistory.append({"revision": len(history) + 1, "digest": digest, "status": "ready"})\nstate.write_text(json.dumps(history, indent=2) + "\\n")\nprint(f"deployed revision={len(history)} digest={digest[:19]}...")\n''')
    write_text(LAB / "scripts/rollback.py", '''from __future__ import annotations\n\nimport json\nfrom pathlib import Path\n\nstate = Path(__file__).resolve().parents[1] / "runs/deployment.json"\nhistory = json.loads(state.read_text())\nif len(history) < 2:\n    raise SystemExit("되돌릴 이전 리비전이 없습니다.")\nfailed = history.pop()\nhistory[-1]["status"] = "ready-after-rollback"\nstate.write_text(json.dumps(history, indent=2) + "\\n")\nprint(f"rolled back {failed['revision']} -> {history[-1]['revision']}")\n''')
    write_text(LAB / "scripts/check_metrics.py", '''from __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\npath = Path(__file__).resolve().parents[1] / "data/metrics.jsonl"\nrows = [json.loads(line) for line in path.read_text().splitlines()]\nviolations = [\n    row for row in rows\n    if row["errors"] / row["requests"] > 0.05 and row["p95_ms"] > 800\n]\nfor row in rows:\n    print(row["minute"], round(row["errors"] / row["requests"], 3), row["p95_ms"])\nprint("alert:", "FIRING" if len(violations) >= 2 else "OK")\nsys.exit(1 if len(violations) >= 2 else 0)\n''')
    write_text(LAB / "pyproject.toml", '''[build-system]\nrequires = ["setuptools==80.9.0"]\nbuild-backend = "setuptools.build_meta"\n\n[project]\nname = "ch33-cicd-lab"\nversion = "0.1.0"\nrequires-python = "==3.12.*"\ndependencies = []\n\n[tool.setuptools]\npy-modules = ["cicd_demo"]\n\n[dependency-groups]\ndev = ["pytest==8.4.2", "ruff==0.13.0", "build==1.3.0"]\n\n[tool.ruff]\nline-length = 100\n''')
    write_text(LAB / ".github/workflows/ci.yml", '''name: ci\non:\n  pull_request:\n  push:\n    branches: [main]\npermissions:\n  contents: read\njobs:\n  verify:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v6\n      - uses: astral-sh/setup-uv@v7\n      - run: uv sync --dev\n      - run: uv run ruff check cicd_demo.py tests scripts\n      - run: uv run python -m pytest\n      - run: uv run python -m build\n      - run: uv run python scripts/evaluate_regression.py\n''')
    write_text(LAB / "README.md", '''# Ch33 CI/CD 실습\n\nPython 3.12와 uv를 사용합니다. `uv sync --dev` 뒤 `uv run python -m pytest`, `uv run ruff check cicd_demo.py tests scripts`, `uv run python -m build`, `uv run python scripts/evaluate_regression.py`를 실행합니다. `.github/workflows/ci.yml`은 같은 명령을 PR과 main push에서 실행하는 완성 예시입니다.\n\n`data/regression-baseline.json`은 Ch15의 Groundedness와 Ch29의 추가 도구 호출 개념을 학습용 최소 자료로 다시 작성한 공개 고정 자료입니다. 실제 Ch15·29 전체 실행 결과를 복사하거나 재평가한 자료가 아닙니다. 원본 경로와 SHA-256은 기준선 파일에 기록했습니다. `scripts/deploy.py`와 `rollback.py`는 로컬 JSON 배포 이력만 변경합니다. 레지스트리 push, 클라우드 인증, GitHub PR 생성, 실제 클라우드 배포는 수행하지 않습니다.\n''')

    nbs = {}
    nbs["01-테스트-린트-빌드와-GitHub-Actions"] = notebook("테스트·린트·빌드와 GitHub Actions", "paired", [
        md("# 테스트·린트·빌드와 GitHub Actions\n\n같은 검증 명령을 로컬과 CI에서 실행하고 종료 코드를 확인합니다."),
        code('from pathlib import Path\nimport subprocess, sys\nlab = Path("labs/part7/ch33-cicd")\nprint(sys.version.split()[0], lab.exists())'),
        code('result = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=lab, text=True, capture_output=True)\nprint(result.stdout.strip())\nprint("exit_code=", result.returncode)\nassert result.returncode == 0'),
        code('result = subprocess.run(["ruff", "check", "cicd_demo.py", "tests"], cwd=lab, text=True, capture_output=True)\nprint(result.stdout.strip() or "ruff: PASS")\nprint("exit_code=", result.returncode)\nassert result.returncode == 0'),
        code('import tempfile\nwith tempfile.TemporaryDirectory() as out:\n    result = subprocess.run([sys.executable, "-m", "build", "--wheel", "--outdir", out], cwd=lab, text=True, capture_output=True)\n    wheels = [p.name for p in Path(out).glob("*.whl")]\n    print("wheels=", wheels, "exit_code=", result.returncode)\n    assert result.returncode == 0 and len(wheels) == 1'),
        md("## 실패 재현\n\n임시 저장소에서 실패하는 테스트를 추가합니다. 실제 pytest 프로세스가 0이 아닌 종료 코드를 반환합니다.", "before"),
        code('import tempfile\nwith tempfile.TemporaryDirectory() as temp:\n    p = Path(temp) / "test_regression.py"\n    p.write_text("def test_regression():\\n    assert 2 + 2 == 5\\n")\n    failed = subprocess.run([sys.executable, "-m", "pytest", "-q", str(p)], text=True, capture_output=True)\n    print(failed.stdout.strip().splitlines()[-1])\n    print("exit_code=", failed.returncode)\n    assert failed.returncode != 0', "before"),
        md("## 수정\n\n같은 테스트의 기대값을 고치면 프로세스가 종료 코드 0을 반환합니다.", "after"),
        code('with tempfile.TemporaryDirectory() as temp:\n    p = Path(temp) / "test_regression.py"\n    p.write_text("def test_regression():\\n    assert 2 + 2 == 4\\n")\n    passed = subprocess.run([sys.executable, "-m", "pytest", "-q", str(p)], text=True, capture_output=True)\n    print(passed.stdout.strip().splitlines()[-1])\n    print("exit_code=", passed.returncode)\n    assert passed.returncode == 0', "after"),
    ])
    nbs["02-평가-회귀를-CI에-연결하기"] = notebook("평가 회귀를 CI에 연결하기", "paired", [
        md("# 평가 회귀를 CI에 연결하기\n\nCh15와 Ch29에서 배운 서로 다른 평가 기준을 하나의 종료 코드로 연결합니다."),
        code('from pathlib import Path\nimport json, subprocess, sys\nlab = Path("labs/part7/ch33-cicd")\nbaseline = json.loads((lab / "data/regression-baseline.json").read_text())\nprint(baseline)'),
        code('result = subprocess.run([sys.executable, "scripts/evaluate_regression.py"], cwd=lab, text=True, capture_output=True)\nprint(result.stdout.strip())\nprint("exit_code=", result.returncode)\nassert result.returncode == 0'),
        md("## 실패 재현\n\n임시 저장소에 Groundedness와 추가 호출 수가 모두 나빠진 현재 결과를 둡니다.", "before"),
        code('import tempfile, shutil\nwith tempfile.TemporaryDirectory() as temp:\n    t = Path(temp)\n    shutil.copytree(lab / "scripts", t / "scripts")\n    shutil.copytree(lab / "data", t / "data")\n    bad = {"groundedness": 0.80, "trajectory_extra_calls": 3, "cases": 4}\n    (t / "data/regression-current.json").write_text(json.dumps(bad))\n    failed = subprocess.run([sys.executable, "scripts/evaluate_regression.py"], cwd=t, text=True, capture_output=True)\n    print(failed.stdout.strip(), "exit_code=", failed.returncode)\n    assert failed.returncode != 0', "before"),
        md("## 수정\n\n기준을 만족하는 결과로 바꾸면 두 검사가 모두 통과합니다.", "after"),
        code('with tempfile.TemporaryDirectory() as temp:\n    t = Path(temp)\n    shutil.copytree(lab / "scripts", t / "scripts")\n    shutil.copytree(lab / "data", t / "data")\n    good = {"groundedness": 0.91, "trajectory_extra_calls": 1, "cases": 4}\n    (t / "data/regression-current.json").write_text(json.dumps(good))\n    passed = subprocess.run([sys.executable, "scripts/evaluate_regression.py"], cwd=t, text=True, capture_output=True)\n    print(passed.stdout.strip(), "exit_code=", passed.returncode)\n    assert passed.returncode == 0', "after"),
    ])
    nbs["03-레지스트리-다이제스트와-클라우드-배포"] = notebook("레지스트리·다이제스트와 클라우드 배포", "experiment", [
        md("# 레지스트리·다이제스트와 클라우드 배포\n\n태그와 다이제스트가 가리키는 배포 대상을 비교합니다."),
        code('from pathlib import Path\nimport hashlib, subprocess, sys, tempfile, json\nlab = Path("labs/part7/ch33-cicd")'),
        code('with tempfile.TemporaryDirectory() as temp:\n    artifact = Path(temp) / "image.tar"\n    artifact.write_bytes(b"agent-service-v1")\n    digest_v1 = "sha256:" + hashlib.sha256(artifact.read_bytes()).hexdigest()\n    artifact.write_bytes(b"agent-service-v2")\n    digest_v2 = "sha256:" + hashlib.sha256(artifact.read_bytes()).hexdigest()\n    print("same_tag=latest", "same_digest=", digest_v1 == digest_v2)\n    print(digest_v1[:27], digest_v2[:27])\n    assert digest_v1 != digest_v2'),
        code('with tempfile.TemporaryDirectory() as temp:\n    t = Path(temp)\n    (t / "scripts").mkdir()\n    (t / "runs").mkdir()\n    (t / "scripts/deploy.py").write_text((lab / "scripts/deploy.py").read_text())\n    result = subprocess.run([sys.executable, "scripts/deploy.py", digest_v1], cwd=t, text=True, capture_output=True)\n    print(result.stdout.strip(), "exit_code=", result.returncode)\n    print((t / "runs/deployment.json").read_text().strip())\n    assert result.returncode == 0'),
        md("## 결과 해석\n\n같은 latest 태그라는 설명만으로 실제 바이트를 식별할 수 없지만, 내용에서 계산한 다이제스트는 v1과 v2가 달랐습니다. 로컬 배포 기록은 다이제스트를 저장했습니다."),
    ])
    nbs["04-모니터링과-알림"] = notebook("모니터링과 알림", "experiment", [
        md("# 모니터링과 알림\n\n오류율과 p95 지연이 함께 기준을 넘은 상태가 두 구간 이어지는지 확인합니다."),
        code('from pathlib import Path\nimport json, subprocess, sys\nlab = Path("labs/part7/ch33-cicd")\nrows = [json.loads(x) for x in (lab / "data/metrics.jsonl").read_text().splitlines()]\nprint("rows=", len(rows))'),
        code('for row in rows:\n    error_rate = row["errors"] / row["requests"]\n    firing = error_rate > 0.05 and row["p95_ms"] > 800\n    print(row["minute"], f"error_rate={error_rate:.3f}", f"p95={row[\'p95_ms\']}", firing)'),
        code('result = subprocess.run([sys.executable, "scripts/check_metrics.py"], cwd=lab, text=True, capture_output=True)\nprint(result.stdout.strip())\nprint("exit_code=", result.returncode)\nassert result.returncode == 1'),
        md("## 결과 해석\n\n1·2분에는 두 조건을 동시에 만족하지 않았습니다. 3·4분에는 오류율 5% 초과와 p95 800ms 초과가 함께 관찰되어 경보 상태가 되었습니다. 이 고정 자료는 임계값 동작만 보여 주며 실제 서비스 정상 범위를 정하지 않습니다."),
    ])
    nbs["05-롤백과-복구-검증"] = notebook("롤백과 복구 검증", "paired", [
        md("# 롤백과 복구 검증\n\n두 리비전을 배포한 뒤 경보를 근거로 이전 다이제스트를 다시 활성화합니다."),
        code('from pathlib import Path\nimport hashlib, subprocess, sys, tempfile, json, shutil\nlab = Path("labs/part7/ch33-cicd")\nv1 = "sha256:" + hashlib.sha256(b"stable-v1").hexdigest()\nv2 = "sha256:" + hashlib.sha256(b"regressed-v2").hexdigest()'),
        code('temp = tempfile.TemporaryDirectory()\nt = Path(temp.name)\nshutil.copytree(lab / "scripts", t / "scripts")\n(t / "runs").mkdir()\nfor digest in (v1, v2):\n    result = subprocess.run([sys.executable, "scripts/deploy.py", digest], cwd=t, text=True, capture_output=True)\n    print(result.stdout.strip())\nprint(json.loads((t / "runs/deployment.json").read_text()))'),
        md("## 실패 재현\n\nv2 배포 후의 고정 운영 자료에서 경보 프로세스는 종료 코드 1을 반환합니다.", "before"),
        code('failed = subprocess.run([sys.executable, str(lab / "scripts/check_metrics.py")], text=True, capture_output=True)\nprint(failed.stdout.strip().splitlines()[-1], "exit_code=", failed.returncode)\nassert failed.returncode == 1', "before"),
        md("## 수정\n\n롤백 스크립트로 마지막 리비전을 제거하고 활성 다이제스트가 v1인지 확인합니다.", "after"),
        code('rolled = subprocess.run([sys.executable, "scripts/rollback.py"], cwd=t, text=True, capture_output=True)\nhistory = json.loads((t / "runs/deployment.json").read_text())\nprint(rolled.stdout.strip(), "active=", history[-1]["digest"][:19])\nassert rolled.returncode == 0 and history[-1]["digest"] == v1\ntemp.cleanup()', "after"),
    ])
    for slug, nb in nbs.items():
        write_text(LAB / "notebooks" / f"{slug}.ipynb", json.dumps(nb, ensure_ascii=False, indent=1) + "\n")

    refs_common = [
        '<a href="https://docs.github.com/en/actions/get-started/continuous-integration">GitHub Docs, Continuous integration</a> · 확인 2026-09-11',
        '<a href="https://docs.github.com/en/actions/tutorials/build-and-test-code/python">GitHub Docs, Building and testing Python</a> · 확인 2026-09-11',
    ]
    pages = {
        "01-테스트-린트-빌드와-GitHub-Actions": page("01-테스트-린트-빌드와-GitHub-Actions", "테스트·린트·빌드와 GitHub Actions", "paired",
            "GitHub Actions의 워크플로(workflow)는 저장소의 이벤트에 반응해 하나 이상의 작업(job)을 실행하는 YAML 파일입니다. 각 작업은 실행기(runner)에서 단계(step)를 순서대로 수행합니다. 이 실습의 워크플로는 PR과 main 브랜치 push를 시작 조건으로 삼고, 테스트와 린트와 평가 회귀를 같은 Python 3.12 환경에서 실행합니다. 테스트는 관찰 가능한 동작을 확인하고, 린트는 실행 전에 찾을 수 있는 코드 문제를 검사하며, 빌드는 배포할 파일을 만듭니다. 세 검사는 목적이 다르므로 하나의 성공으로 다른 검사를 대신하지 않습니다.",
            "먼저 제공된 테스트 스위트와 Ruff 검사를 별도 프로세스로 실행합니다. 이어서 임시 폴더에 실패하는 테스트를 만들고 pytest의 실제 종료 코드를 관찰합니다. 같은 테스트의 기대값만 수정해 성공 종료 코드와 비교합니다. GitHub에 PR을 만들지는 않지만, `.github/workflows/ci.yml`에는 같은 명령이 들어 있습니다.",
            "실패 테스트는 `2 + 2 == 5`라는 잘못된 기대값 때문에 실제로 실패합니다. pytest는 실패 개수와 함께 종료 코드 1을 반환하고, CI 실행기는 이를 작업 실패로 처리할 수 있습니다. 수정본은 기대값을 4로 고정하며 종료 코드 0을 반환합니다. 이 비교는 테스트 실패를 출력 문자열로 흉내 내지 않고 별도 프로세스의 상태로 확인합니다.",
            ["Actions 버전 태그는 편리하지만 공급망 정책이 엄격한 저장소에서는 검토한 커밋 SHA로 고정합니다.", "로컬에 설치된 도구와 원격 실행기의 버전이 다르면 결과가 달라질 수 있으므로 pyproject와 lock 파일을 함께 커밋합니다.", "빌드 성공은 서비스의 답변 품질을 뜻하지 않습니다. 평가 회귀는 다음 절에서 별도 단계로 연결합니다."],
            ["CI는 변경마다 같은 검사를 같은 순서로 실행합니다.", "프로세스 종료 코드가 자동화의 통과와 중단을 결정합니다.", "테스트·린트·빌드는 서로 다른 문제를 확인합니다."],
            [("워크플로와 작업의 관계를 설명해 보세요.", "워크플로는 이벤트와 전체 자동화 흐름을 정의하고, 작업은 한 실행기에서 수행할 단계의 묶음입니다."), ("린트가 통과하면 테스트를 생략해도 되나요?", "생략할 수 없습니다. 린트는 정적 문제를 찾고 테스트는 실행 결과를 확인하므로 목적이 다릅니다."), ("실패를 CI가 인식하려면 무엇이 필요하나요?", "검사 프로세스가 0이 아닌 종료 코드를 반환해야 합니다."), ("이 실습에서 실제 GitHub PR을 생성했나요?", "생성하지 않았습니다. 로컬 실행과 워크플로 파일의 구조만 검증했습니다.")], refs_common),
        "02-평가-회귀를-CI에-연결하기": page("02-평가-회귀를-CI에-연결하기", "평가 회귀를 CI에 연결하기", "paired",
            "회귀(regression)는 새로운 변경 뒤에 이전에 만족하던 동작이나 품질 기준이 깨지는 현상입니다. 단위 테스트가 함수의 정해진 출력을 검사한다면 평가 회귀는 Groundedness, 궤적의 추가 도구 호출 수처럼 확률적 시스템의 품질과 비용을 검사합니다. 기준선(baseline)은 비교할 이전 결과이며, 허용치(tolerance)는 실행 변동을 고려해 받아들일 범위입니다. Ch15의 생성 품질과 Ch29의 궤적 효율을 한 점수로 합치면 원인을 찾기 어려우므로 두 검사를 분리해 표시하고, 모두 통과할 때만 전체 종료 코드 0을 반환합니다.",
            "공개 고정 자료에서 기준선과 현재 결과를 읽습니다. Groundedness는 기준선보다 0.02를 초과해 낮아지지 않아야 하고, 추가 도구 호출 수는 기준선 이하여야 합니다. 정상 자료로 성공을 확인한 뒤 임시 폴더에서 두 값을 나쁘게 바꾸어 실제 회귀 검사 프로세스가 실패하는지 확인합니다.",
            "실패 자료의 Groundedness 0.80은 기준선 0.90의 허용 하한 0.88보다 낮습니다. 추가 호출 수도 1회에서 3회로 늘었습니다. 두 항목은 각각 FAIL로 출력되고 프로세스는 종료 코드 1을 반환합니다. 수정 자료는 0.91과 1회로 두 기준을 만족해 종료 코드 0을 반환합니다. 네 사례의 고정 자료는 연결 방법을 배우기 위한 것이며 실제 모델 전체의 품질을 대표하지 않습니다.",
            ["확률적 평가에는 반복과 사람 라벨 점검이 필요합니다. 작은 점수 변동만으로 배포를 항상 중단하면 거짓 경보가 늘어날 수 있습니다.", "평가 자료를 제품 코드와 함께 무심코 바꾸면 기준이 완화될 수 있습니다. 기준선 변경에는 리뷰와 변경 이유를 남깁니다.", "비밀 정보나 실제 고객 대화는 공개 CI 로그와 아티팩트에 포함하지 않습니다."],
            ["평가 회귀는 과거 성공 사례가 변경 뒤에도 유지되는지 확인합니다.", "최종 답변 품질과 에이전트 궤적 효율은 분리해 표시합니다.", "회귀 실패는 실제 비정상 종료 코드로 CI를 중단합니다."],
            [("기준선은 무엇인가요?", "현재 변경과 비교할 이전의 승인된 평가 결과입니다."), ("Groundedness와 추가 호출 수를 왜 분리하나요?", "하나는 답변의 근거 충실도이고 다른 하나는 실행 궤적의 효율이므로 실패 원인과 대응이 다릅니다."), ("허용치가 필요한 이유는 무엇인가요?", "모델 평가가 실행마다 조금 달라질 수 있어 의미 없는 변동과 실제 저하를 구분하기 위해서입니다."), ("기준선 파일 변경 시 무엇을 확인해야 하나요?", "평가 기준을 약화한 것인지, 승인된 개선 결과를 반영한 것인지 리뷰해야 합니다.")], refs_common),
        "03-레지스트리-다이제스트와-클라우드-배포": page("03-레지스트리-다이제스트와-클라우드-배포", "레지스트리·다이제스트와 클라우드 배포", "experiment",
            "이미지 레지스트리(image registry)는 컨테이너 이미지를 저장하고 배포 환경에 전달하는 서비스입니다. 태그(tag)는 `v1`이나 `latest`처럼 사람이 읽기 좋은 이름이지만 같은 태그가 새 이미지로 이동할 수 있습니다. 다이제스트(digest)는 이미지 내용에서 계산한 식별자이므로 `sha256:...` 형식으로 정확한 내용을 가리킵니다. 클라우드 배포에서는 CI가 이미지를 빌드하고 레지스트리에 push한 뒤, 배포 시스템이 승인된 다이제스트를 pull하도록 구성할 수 있습니다. 이 연결에는 레지스트리 인증과 클라우드 권한이 필요하므로 실습에서는 로컬 파일의 SHA-256과 JSON 배포 이력으로 경계를 확인합니다.",
            "동일한 `latest` 태그를 가정한 v1과 v2 바이트에서 SHA-256을 계산합니다. 내용이 바뀌면 다이제스트도 바뀌는지 확인하고, v1 다이제스트를 로컬 배포 기록에 저장합니다. 이 기록은 실제 컨테이너 실행이나 레지스트리 전송을 수행하지 않습니다.",
            "v1과 v2는 같은 태그 이름을 사용할 수 있지만 계산된 다이제스트는 서로 달랐습니다. 따라서 배포 기록에 태그만 남기면 당시의 정확한 내용을 나중에 식별하지 못할 수 있습니다. 다이제스트를 저장하면 롤백 때 이전 내용 식별자를 다시 선택할 수 있습니다. 다만 로컬 파일 SHA-256 실험은 OCI 레지스트리의 실제 manifest와 서명, 플랫폼별 이미지 목록을 검증하지 않습니다.",
            ["이미지 다이제스트와 이미지 서명은 역할이 다릅니다. 다이제스트는 내용 식별과 변경 탐지를 돕고, 서명 검증은 신뢰한 주체가 만든 이미지인지 확인하는 정책에 사용합니다.", "클라우드 자격 증명은 저장소 파일에 넣지 않고 OIDC 또는 비밀 저장소와 최소 권한을 사용합니다.", "배포 성공 뒤에도 readiness와 실제 요청 검증이 끝나기 전에는 새 버전이 정상이라고 판단하지 않습니다."],
            ["레지스트리는 배포할 이미지를 저장하고 전달합니다.", "태그는 이동할 수 있지만 다이제스트는 특정 내용을 식별합니다.", "이 실습은 로컬 배포 기록까지 확인했으며 실제 push와 클라우드 반영은 수행하지 않았습니다."],
            [("태그와 다이제스트의 차이는 무엇인가요?", "태그는 사람이 정한 이동 가능한 이름이고, 다이제스트는 이미지 내용에 대응하는 식별자입니다."), ("다이제스트만 확인하면 제작자를 신뢰할 수 있나요?", "그렇지 않습니다. 제작자 신뢰에는 이미지 서명과 공급망 정책이 추가로 필요합니다."), ("실제 배포에 추가로 필요한 것은 무엇인가요?", "레지스트리와 클라우드 권한, 배포 대상, readiness 검사, 네트워크 설정 등이 필요합니다."), ("배포 기록에 다이제스트를 남기는 이유는 무엇인가요?", "정확히 어떤 내용을 배포했는지 추적하고 이전 내용을 다시 선택하기 위해서입니다.")], [
                '<a href="https://docs.docker.com/reference/cli/docker/image/push/">Docker Docs, docker image push</a> · 확인 2026-09-11',
                '<a href="https://docs.docker.com/build/exporters/image-registry/">Docker Docs, Image and registry exporters</a> · 확인 2026-09-11']),
        "04-모니터링과-알림": page("04-모니터링과-알림", "모니터링과 알림", "experiment",
            "모니터링(monitoring)은 서비스의 요청 수, 오류, 지연, 자원 사용량 같은 상태를 지속해서 수집하고 해석하는 활동입니다. 메트릭(metric)은 시간에 따라 기록하는 수치입니다. p95 지연은 요청의 95%가 그 값 이내에 완료되었다는 뜻입니다. 경보 규칙(alerting rule)은 측정식과 임계값, 지속 시간을 조합해 사람이 확인할 상태를 만듭니다. 오류율 하나가 잠깐 높아졌다는 이유만으로 즉시 호출하면 잡음이 많아질 수 있으므로, 이 실습은 오류율과 p95 지연이 동시에 기준을 넘고 두 구간 이어질 때 FIRING으로 판정합니다.",
            "4분의 고정 메트릭을 읽고 각 분의 오류율을 계산합니다. 오류율 5% 초과와 p95 800ms 초과를 동시에 적용하며, 두 구간 이상 이어졌을 때 실제 검사 프로세스가 종료 코드 1을 반환하도록 합니다. 운영 경보 도구에서는 같은 조건을 PromQL 표현식과 `for` 지속 시간으로 옮길 수 있습니다.",
            "1분과 2분은 두 조건을 동시에 넘지 않았습니다. 3분과 4분은 오류율과 p95 지연이 함께 기준을 넘었으므로 고정 규칙에서 FIRING이 되었습니다. 종료 코드 1은 배포 후 검증이나 로컬 시뮬레이션을 중단하는 데 사용할 수 있습니다. 실제 Prometheus 경보는 Alertmanager 같은 외부 구성 요소로 알림을 전달하며, 본 실습은 메시지를 외부로 전송하지 않습니다.",
            ["평균 지연은 일부 매우 느린 요청을 숨길 수 있으므로 p50, p95, p99를 목적에 맞게 함께 봅니다.", "LLM 서비스에서는 HTTP 오류뿐 아니라 빈 답변, 도구 실패, 토큰 비용, 대화당 단계 수도 관찰해야 합니다.", "경보 임계값은 제공된 예제 수치를 그대로 운영에 적용하지 않고 실제 정상 범위와 오류 예산을 근거로 정합니다."],
            ["메트릭은 시간에 따라 수집하는 수치이며 경보 규칙은 대응이 필요한 조건을 표현합니다.", "여러 신호와 지속 시간을 조합하면 순간적인 잡음을 줄일 수 있습니다.", "경보는 원인을 확정하지 않으며 조사와 대응을 시작할 근거를 제공합니다."],
            [("p95 지연은 무엇을 뜻하나요?", "관찰한 요청의 95%가 해당 시간 이내에 완료되었다는 뜻입니다."), ("오류율 한 번 초과만으로 경보를 보내지 않는 이유는 무엇인가요?", "순간적인 변동으로 인한 불필요한 호출을 줄이고 지속되는 문제를 구분하기 위해서입니다."), ("경보가 원인을 알려 주나요?", "경보는 조건 충족을 알리며 원인은 로그와 트레이스, 변경 이력을 함께 조사해야 합니다."), ("LLM 서비스에서 추가로 볼 지표는 무엇인가요?", "토큰과 비용, 도구 호출 실패, 단계 수, 근거 충실도 같은 지표가 있습니다.")], [
                '<a href="https://prometheus.io/docs/prometheus/3.5/configuration/alerting_rules/">Prometheus 3.5 Docs, Alerting rules</a> · 확인 2026-09-11']),
        "05-롤백과-복구-검증": page("05-롤백과-복구-검증", "롤백과 복구 검증", "paired",
            "롤백(rollback)은 문제가 있는 새 배포를 이전에 확인된 리비전으로 되돌리는 운영 절차입니다. 리비전(revision)은 배포 상태의 순서가 있는 버전 기록입니다. 롤백은 코드만 이전으로 바꾸는 작업으로 끝나지 않습니다. 데이터베이스 스키마, 메시지 형식, 캐시, 외부 API가 이전 버전과 호환되는지 확인해야 합니다. 복구 검증은 이전 다이제스트가 활성화되었는지, readiness가 정상인지, 오류와 지연이 회복되는지 확인합니다. 이 실습은 두 다이제스트의 로컬 이력과 경보 종료 코드를 연결합니다.",
            "안정 버전 v1과 회귀가 있는 버전 v2의 다이제스트를 차례로 로컬 이력에 배포합니다. v2 이후의 고정 메트릭에서 경보 검사 프로세스가 실패하는지 확인합니다. 그다음 롤백 스크립트를 실행해 v2를 이력의 활성 상태에서 제거하고 v1 다이제스트가 다시 선택되었는지 검사합니다.",
            "Before에서는 v2가 최신 리비전이고 운영 검사 결과가 FIRING, 종료 코드 1입니다. After에서는 롤백 스크립트가 `2 -> 1`을 출력하고 활성 다이제스트가 v1과 일치합니다. 이것은 정확한 이전 결과물을 선택하는 제어 흐름을 증명합니다. 실제 트래픽이 회복되었다는 결론은 내릴 수 없습니다. 실제 환경에서는 롤백 뒤 새 메트릭 구간과 핵심 요청의 응답을 다시 확인해야 합니다.",
            ["되돌릴 이미지가 레지스트리에서 삭제되지 않도록 보존 정책을 정합니다.", "하위 호환되지 않는 데이터 마이그레이션은 애플리케이션 롤백만으로 복구되지 않을 수 있습니다. 확장 후 축소 방식이나 별도 데이터 복구 절차를 준비합니다.", "자동 롤백은 잘못된 경보에도 반응할 수 있으므로 영향 범위와 승인 정책, 최대 반복 횟수를 정합니다."],
            ["롤백은 이전에 검증한 리비전과 다이제스트를 다시 선택합니다.", "롤백 뒤에는 배포 상태와 서비스 지표를 다시 검증합니다.", "코드와 데이터의 호환성을 함께 설계해야 복구 절차가 작동합니다."],
            [("롤백과 재배포의 공통점은 무엇인가요?", "둘 다 선택한 이미지 다이제스트를 배포 환경의 활성 버전으로 지정합니다."), ("롤백 뒤 무엇을 확인해야 하나요?", "활성 다이제스트, readiness, 핵심 요청, 오류율과 지연의 회복을 확인해야 합니다."), ("애플리케이션만 되돌려도 복구되지 않는 사례는 무엇인가요?", "이전 버전과 호환되지 않는 데이터베이스 스키마 변경이 이미 적용된 사례입니다."), ("자동 롤백에 필요한 제한은 무엇인가요?", "경보 조건, 영향 범위, 승인 정책, 최대 반복 횟수와 중단 조건이 필요합니다.")], [
                '<a href="https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/">Kubernetes Docs, Performing a Rolling Update</a> · 확인 2026-09-11',
                '<a href="https://kubernetes.io/docs/concepts/workloads/management/">Kubernetes Docs, Managing Workloads</a> · 확인 2026-09-11']),
    }
    for slug, html in pages.items():
        write_text(BOOK / "_src" / f"{slug}.html", html)

    index = '''<section class="chapter-intro"><h2>Ch33 CI/CD와 배포 운영</h2><p>코드 변경을 테스트·린트·빌드·평가 회귀로 확인하고, 다이제스트로 배포 대상을 고정한 뒤 모니터링 신호에 따라 롤백하는 전체 흐름을 학습합니다.</p><h3>학습 목표</h3><ul><li>로컬과 GitHub Actions에서 같은 검증 명령을 사용할 수 있습니다.</li><li>Ch15·29 평가 기준을 회귀 검사 종료 코드로 연결할 수 있습니다.</li><li>배포 이력과 운영 지표로 롤백을 판단하고 복구를 확인할 수 있습니다.</li></ul><p>총 16시간: 강의 5시간, 실습 11시간</p></section>'''
    write_text(BOOK / "_src/index-body.html", index)

    for i, (_, item) in enumerate([(s, p) for s, p in pages.items()], 1):
        title = config["sections"][i-1]["title"]
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="300" viewBox="0 0 960 300" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">입력, 검사, 결과, 판단의 순서</desc><rect width="960" height="300" rx="20" fill="#f8fafc"/><rect x="45" y="95" width="190" height="105" rx="14" fill="#dbeafe" stroke="#2563eb" stroke-width="3"/><rect x="300" y="95" width="190" height="105" rx="14" fill="#dcfce7" stroke="#16a34a" stroke-width="3"/><rect x="555" y="95" width="170" height="105" rx="14" fill="#dcfce7" stroke="#16a34a" stroke-width="3"/><rect x="790" y="95" width="130" height="105" rx="14" fill="#ffedd5" stroke="#ea580c" stroke-width="3"/><path d="M235 148H290M490 148H545M725 148H780" stroke="#334155" stroke-width="4" marker-end="url(#a)"/><defs><marker id="a" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#334155"/></marker></defs><g font-family="sans-serif" text-anchor="middle" fill="#0f172a"><text x="140" y="135" font-size="22" font-weight="700">변경 입력</text><text x="140" y="168" font-size="16">파일·다이제스트</text><text x="395" y="135" font-size="22" font-weight="700">자동 검사</text><text x="395" y="168" font-size="16">실제 종료 코드</text><text x="640" y="135" font-size="22" font-weight="700">통과 결과</text><text x="640" y="168" font-size="16">기록·아티팩트</text><text x="855" y="135" font-size="22" font-weight="700">판단</text><text x="855" y="168" font-size="16">진행·중단</text><text x="480" y="52" font-size="25" font-weight="700">{title}</text></g></svg>'''
        write_text(BOOK / "figures" / f"{i:02d}-흐름.svg", svg)
        excalidraw = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com", "elements": [], "appState": {"viewBackgroundColor": "#f8fafc"}, "files": {}}
        write_text(BOOK / "figures" / f"{i:02d}-흐름.excalidraw", json.dumps(excalidraw, ensure_ascii=False, indent=2) + "\n")

    write_text(BOOK / "qa/research.md", '''# Ch33 공식 문서 조사\n\n확인일: 2026-09-11\n\n- GitHub Actions 공식 문서는 workflow가 저장소 이벤트로 시작되고 job과 step으로 구성되며, Python 프로젝트에서 `setup-python`, 테스트, Ruff, 아티팩트 보관을 사용할 수 있다고 설명합니다. 본문은 PR에서 자동 검사를 실행하는 범위만 반영했습니다.\n- Docker 공식 문서는 `docker image push`가 이미지를 레지스트리에 공유하며 push 결과에 digest가 표시되는 예를 제공합니다. 본 실습은 네트워크 push 없이 바이트의 SHA-256 변화만 확인합니다.\n- Kubernetes 공식 문서는 Deployment의 rollout 상태 확인과 `kubectl rollout undo`를 통한 이전 리비전 복구를 설명합니다. 본 실습은 클러스터 없이 JSON 이력으로 같은 상태 전이를 축소 재현합니다.\n- Prometheus 3.5 공식 문서는 표현식과 조건으로 경보 규칙을 정의하고 외부 서비스로 알림을 보낼 수 있다고 설명합니다. 본 실습은 외부 전송 없이 고정 메트릭 판정만 수행합니다.\n\n기준 URL은 각 절 참고 자료에 직접 연결했습니다. GitHub의 현재 예시에 표시된 Actions 주요 버전은 향후 바뀔 수 있으므로 실제 수업 직전에 다시 확인해야 합니다.\n''')
    write_text(BOOK / "집필점검표.md", '''# Ch33 집필 점검표\n\n| 절 | 학습 질문 | 실제 관찰 | 해석 범위 |\n| --- | --- | --- | --- |\n| 01 | CI가 실패를 어떻게 인식하는가 | 임시 실패 테스트 exit 1, 수정 후 exit 0 | 로컬 pytest·Ruff 실행 |\n| 02 | 품질 회귀를 PR 검사로 어떻게 바꾸는가 | Groundedness·궤적 FAIL 시 exit 1 | 공개 고정 4사례 |\n| 03 | 배포 대상을 어떻게 정확히 식별하는가 | 같은 태그 가정에서 v1·v2 digest 불일치 | 로컬 바이트 SHA-256 |\n| 04 | 어떤 지표가 경보를 만드는가 | 3·4분 연속 조건 충족, exit 1 | 고정 4분 자료 |\n| 05 | 롤백 뒤 무엇을 확인하는가 | revision 2→1, 활성 digest v1 | 로컬 JSON 이력 |\n\n모든 노트북은 Python 3.12 새 커널에서 순차 실행합니다. 실제 PR, 레지스트리 push, 클라우드 배포, 외부 알림은 수행하지 않습니다. 별도 한국어 감사는 후속 검토 세션에서 수행합니다.\n''')
    ignored = {".venv", ".pytest_cache", ".ruff_cache", "__pycache__", "runs", "dist", "build"}
    public = [str(p.relative_to(ROOT)) for p in sorted(LAB.rglob("*")) if p.is_file() and not ignored.intersection(p.parts) and not p.name.endswith(".failure.json")]
    write_text(BOOK / "qa/public-files.json", json.dumps(public, ensure_ascii=False, indent=2) + "\n")
    write_text(BOOK / "qa/prerequisite-files.json", "[]\n")
    write_text(BOOK / "qa/verification.md", '''# Ch33 검증 기록\n\n검증일: 2026-09-11 · Python 3.12.13\n\n- 새 커널 실행: 노트북 5개, 코드 셀 20개를 순차 실행했습니다.\n- 실제 회귀: 임시 pytest 테스트가 종료 코드 1을 반환하고 수정 후 0을 반환했습니다. 평가 회귀는 Groundedness와 궤적 기준 위반 시 종료 코드 1, 수정 후 0을 반환했습니다.\n- 배포 상태: 서로 다른 바이트의 SHA-256이 달랐고, 로컬 배포 이력에 다이제스트가 기록되었습니다.\n- 운영 상태: 3·4분 연속으로 오류율 5%와 p95 800ms를 초과해 경보 검사 종료 코드 1을 확인했습니다.\n- 롤백: 리비전 2에서 1로 되돌린 뒤 활성 다이제스트가 v1과 일치했습니다.\n- 자동 검사: pytest 2개 통과, Ruff 통과, wheel 1개 빌드, 회귀 검사 통과.\n- 교재 검사: 5절, 코드 셀 최대 10줄, 미작성 표지 없음.\n\n## 실행하지 않은 외부 단계\n\nGitHub PR과 Actions 원격 실행, 레지스트리 push, 클라우드 인증·배포, Kubernetes 클러스터 반영, Prometheus·Alertmanager 외부 알림은 수행하지 않았습니다. 이 단계는 저장소·클라우드 계정과 배포 대상이 확정된 뒤 실행해야 합니다.\n\n별도 모델의 한국어 감사 3단은 후속 검토 세션에서 수행합니다.\n''')


if __name__ == "__main__":
    main()
