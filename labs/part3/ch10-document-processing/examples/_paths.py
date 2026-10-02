import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
CORPUS = ROOT.parents[1] / "data" / "rag-corpus"
FIXTURES = ROOT / "fixtures"
