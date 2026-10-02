import re, glob, sys, json
# 한정어 없는 「청크」: 앞이 "스트림 "/"문서 "가 아닌 것 (code 태그 안은 따로 셈)
def scan(text):
    res = []
    for m in re.finditer('청크', text):
        pre = text[max(0, m.start()-4):m.start()]
        if pre.endswith('스트림 ') or pre.endswith('문서 '): continue
        res.append(m.start())
    return res
files = sys.argv[1:] or sorted(glob.glob('textbook/part*/*/_src/*.html'))
tot = 0
for f in files:
    s = open(f, encoding='utf-8').read()
    # code 태그 제거판에서 셈
    for kind, t in (('prose', re.sub(r'<code>[^<]*</code>', lambda m: '□'*len(m.group(0)), s)),):
        hits = scan(t)
        for h in hits:
            tot += 1
            print(f.replace('textbook/','')[:55], '|', s[max(0,h-45):h+25].replace('\n',' '))
print('TOTAL', tot)
