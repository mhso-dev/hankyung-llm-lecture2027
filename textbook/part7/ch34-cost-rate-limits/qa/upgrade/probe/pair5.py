"""짝짓기 Before/After가 매번 같은지 — 새 프로세스에서 노트북 코드 셀(생성기 글)을 차례로 실행해 5·6절 출력의 해시를 찍는다."""
import contextlib, hashlib, importlib.util, io, os, sys
sys.dont_write_bytecode = True
ROOT = os.path.expanduser("~/mnt/한국경제신문")
spec = importlib.util.spec_from_file_location("a02", ROOT + "/textbook/part7/ch34-cost-rate-limits/qa/upgrade/author_02.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
os.chdir(ROOT + "/labs/part7/ch34-cost-rate-limits/notebooks"); sys.path.insert(0, ".")
names = ["IMPORTS","FIND_LAB","INQUIRIES","NAMES","SETTINGS","THINKING","BUILD","WRITE","SHOW_LINE","JOB","READ_FILES","DEF_NAMES","SHOW_NAMES","DEF_ANSWER","SHOW_OUTPUT","SHOW_ERROR","PRICES","TOKENS","CHECK_USAGE","COST","DEF_ORDER","CALL_ORDER","COUNT_ORDER","MISSING","DEF_BOOK","BUILD_BOOKS","DEF_PAIR_NAME","CALL_NAME","VARY"]
g = {}; before = io.StringIO(); after = io.StringIO()
for name in names:
    target = io.StringIO()
    if name in ("CALL_ORDER", "COUNT_ORDER"): target = before
    if name in ("MISSING", "BUILD_BOOKS", "CALL_NAME", "VARY"): target = after
    with contextlib.redirect_stdout(target):
        exec(getattr(mod, name), g)
print("before", hashlib.sha256(before.getvalue().encode()).hexdigest()[:16], "after", hashlib.sha256(after.getvalue().encode()).hexdigest()[:16], "mismatch", g["mismatch_count"], "missing", g["missing_names"])
