"""Check publication bytes against available secret values without printing them."""
import json
import sys
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "textbook/_notebook"))
from execute import secret_values  # noqa: E402 — shared notebook runtime


def main():
    secrets = [value.encode() for value in secret_values(ROOT)]
    files = set((ROOT / "textbook/part7").glob("ch*/*.html"))
    files.update((ROOT / "textbook/part7").glob("ch*/_src/*.html"))
    files.update(ROOT / name for name in json.loads(
        (ROOT / "textbook/part7/public-files.json").read_text()))
    exposed = [str(path.relative_to(ROOT)) for path in files
               if any(secret in path.read_bytes() for secret in secrets)]
    for name in ("part7-practice.zip", "llm-practice.zip"):
        with ZipFile(ROOT / "textbook/downloads" / name) as archive:
            for member in archive.namelist():
                if any(secret in archive.read(member) for secret in secrets):
                    exposed.append(f"{name}:{member}")
    report = {"known_secrets_available": bool(secrets), "source_files": len(files),
              "archives": 2, "exposed_paths": exposed}
    (ROOT / "textbook/part7/qa/secret-scan.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2))
    assert not exposed, "Secret detected; consult private QA report for paths"
    print(f"PASS secret scan: {len(files)} files and 2 archives")


if __name__ == "__main__":
    main()
