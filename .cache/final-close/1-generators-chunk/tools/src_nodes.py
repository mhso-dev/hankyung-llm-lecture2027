import re, sys, json
src = open(sys.argv[1], encoding='utf-8').read()
# tokens: mermaid/img placeholders, code, tags, text
pat = re.compile(r"(\{\{(?:mermaid|img):[^}]*\}\}|<code>.*?</code>|<pre[\s\S]*?</pre>|<[^>]+>)")
pos = 0; out = []
for m in pat.finditer(src):
    t = src[pos:m.start()]
    if '청크' in t: out.append(('TEXT', t))
    tok = m.group(0)
    if '청크' in tok:
        if tok.startswith('{{'):
            name, _, rest = tok[2:-2].partition('|'); alt, _, cap = rest.partition('|')
            out.append(('FIG', f"{name} || ALT={alt.count('청크')} || CAP={cap}"))
        elif tok.startswith('<code>') or tok.startswith('<pre'):
            out.append(('CODE', tok[:120]))
        else:
            out.append(('TAG', tok[:120]))
    pos = m.end()
t = src[pos:]
if '청크' in t: out.append(('TEXT', t))
for k, v in out: print(k, '|', v.replace('\n', '⏎')[:400])
print(len(out))
