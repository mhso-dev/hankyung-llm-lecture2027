import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rag import DATA_DIR, load_pdfs

scanned = load_pdfs([DATA_DIR / "pdf" / "scanned" / "S01-E01-scan.pdf"])
print(len(scanned))
