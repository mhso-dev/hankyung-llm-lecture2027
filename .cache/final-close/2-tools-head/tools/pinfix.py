"""pinfix.py FILE OLD_HASH NEW_HASH NOTE — 생성기의 해시 상수 줄(따옴표 안 OLD_HASH, 꼭 한 곳)을 새 값으로 바꾸고 그 줄 바로 위에 설명 한 줄을 더한다."""
import sys, hashlib, re
from pathlib import Path
p = Path(sys.argv[1]); old, new, note = sys.argv[2], sys.argv[3], sys.argv[4]
t = p.read_text(encoding='utf-8'); lines = t.splitlines(True)
idx = [i for i, l in enumerate(lines) if ('"' + old + '"') in l]
assert len(idx) == 1, ('pin count', len(idx))
i = idx[0]
indent = re.match(r'\s*', lines[i]).group(0)
lines[i] = lines[i].replace('"' + old + '"', '"' + new + '"')
lines.insert(i, indent + '# ' + note + '\n')
nt = ''.join(lines)
compile(nt, str(p), 'exec')
p.write_text(nt, encoding='utf-8')
print(p.name, hashlib.sha256(t.encode()).hexdigest()[:12], '->', hashlib.sha256(nt.encode()).hexdigest()[:12], 'line', i + 2)
