"""docins.py FILE MODE ANCHOR TEXTFILE — 문서에 줄을 덧붙이기만 한다(기존 줄은 그대로).
MODE after  : ANCHOR로 시작하는 줄(꼭 하나) 바로 뒤에 TEXTFILE 내용을 넣는다.
MODE before : ANCHOR와 같은 줄(꼭 하나) 바로 앞에 넣는다(앞 빈 줄 규칙 유지 — 빈 줄 앞에 넣음)."""
import sys, hashlib
from pathlib import Path
p = Path(sys.argv[1]); mode = sys.argv[2]; anchor = sys.argv[3]; add = Path(sys.argv[4]).read_text(encoding='utf-8').rstrip('\n') + '\n'
text = p.read_text(encoding='utf-8'); lines = text.splitlines(True)
if mode == 'after':
    idx = [i for i, l in enumerate(lines) if l.startswith(anchor)]
    assert len(idx) == 1, ('anchor count', len(idx))
    pos = idx[0] + 1
else:
    idx = [i for i, l in enumerate(lines) if l.rstrip('\n') == anchor]
    assert len(idx) == 1, ('anchor count', len(idx))
    pos = idx[0]
    while pos > 0 and lines[pos - 1].strip() == '': pos -= 1
new = ''.join(lines[:pos]) + add + ''.join(lines[pos:])
assert new.replace(add, '', 1) == text
p.write_text(new, encoding='utf-8')
print(p, hashlib.sha256(text.encode()).hexdigest()[:12], '->', hashlib.sha256(new.encode()).hexdigest()[:12], 'inserted at line', pos + 1)
