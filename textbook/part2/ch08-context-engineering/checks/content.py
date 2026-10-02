"""교재 구조·코드/출력 일치·내부 링크를 검증한다."""
from __future__ import annotations
import ast
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT.parents[2] / 'labs' / 'part2' / 'ch08-context-engineering'
sections = sorted(ROOT.glob('[0-9][0-9]-*.html'))
assert len(sections) == 6, len(sections)
reports = []
responses = {r['response'] for p in (LAB / 'runs').glob('*.jsonl') for line in p.read_text().splitlines() if 'response' in (r := json.loads(line))}
for path in sections + [ROOT / 'index.html']:
    text = path.read_text()
    soup = html.fromstring(text)
    assert not re.search(r'\{\{(?:svg|img|code|output):|LAB_EX\d+_INSERT|RESULT_EX\d+_INSERT|RESEARCH_REFERENCES', text), path
    code_count = 0
    for block in soup.xpath('//code[@data-source]'):
        ref = block.get('data-source').split(':')
        source = (LAB / ref[0]).read_text()
        if len(ref) > 1:
            node = next(n for n in ast.parse(source).body if getattr(n, 'name', None) == ref[1])
            start = min([node.lineno] + [d.lineno for d in node.decorator_list])
            source = '\n'.join(source.splitlines()[start-1:node.end_lineno]) + '\n'
        assert block.text_content() == source, (path, ref)
        code_count += 1
    for block in soup.xpath('//*[@data-output]'):
        assert block.text_content() == (LAB / block.get('data-output')).read_text(), (path, 'output')
    for block in soup.xpath('//pre[@class="out" and not(@data-output)]'):
        assert block.text_content() in responses, (path, 'response excerpt')
    for link in soup.xpath('//a[@href]'):
        href = link.get('href')
        u = urlsplit(href)
        if u.scheme or u.netloc: continue
        target = path if not u.path else path.parent / unquote(u.path)
        assert target.exists(), (path, href)
        if u.fragment and target.suffix == '.html':
            target_soup = soup if target == path else html.fromstring(target.read_text())
            assert target_soup.xpath('//*[@id=$identifier]', identifier=unquote(u.fragment)), (path, href)
    if path.name != 'index.html':
        headings = [h.get('id') for h in soup.xpath('//h2[@id]')]
        assert headings == [f'b{i}' for i in range(1,12)], (path, headings)
        assert len(soup.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," quiz-q ")]')) in range(3,6), path
        assert soup.xpath('//details[@class="instructor"]'), path
        assert code_count >= 1, path
    for e in soup.xpath('//script|//style|//pre|//*[local-name()="svg"]|//nav|//header|//details[@class="instructor"]|//*[@class="nav-foot"]'):
        if e.getparent() is not None: e.getparent().remove(e)
    body = ' '.join(soup.text_content().split())
    banned = ['함정','당연히','간단히','쉽게','돌려줍','돌립니다','이걸','이게','회수 지점','선수 지식 회수']
    hits = [w for w in banned if (re.search(r'(?<![가-힣])' + w, body) if w in ['이게','이걸'] else w in body)]
    assert not hits, (path, hits)
    reports.append({'file':path.name,'prose_chars':len(body),'hangul_chars':len(re.findall('[가-힣]',body)),'code_blocks_verified':code_count})
(ROOT / 'checks' / 'content-results.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(reports,ensure_ascii=False,indent=2))
