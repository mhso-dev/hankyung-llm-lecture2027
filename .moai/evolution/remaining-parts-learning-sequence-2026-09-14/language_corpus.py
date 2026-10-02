"""Extract prose for the independent language review without executable cells."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


class Prose(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('pre', 'script', 'style', 'svg'):
            self.skip += 1
        elif tag in ('p', 'li', 'h2', 'h3', 'summary', 'tr') and not self.skip:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('pre', 'script', 'style', 'svg'):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def prose(source):
    source = re.sub(r'```.*?```', '[코드 블록]', source, flags=re.S)
    source = re.sub(r'\{\{(?:notebook|svg):.*?\}\}', '', source)
    parser = Prose()
    parser.feed(source)
    return '\n'.join(line.strip() for line in ''.join(parser.parts).splitlines() if line.strip())


def corpus(paths, prefix):
    blocks = []
    for relative in paths:
        p = prefix / relative
        if p.suffix == '.ipynb':
            sources = [c['source'] if isinstance(c['source'], str) else ''.join(c['source'])
                       for c in json.loads(p.read_text())['cells'] if c['cell_type'] == 'markdown']
            source = '\n\n'.join(sources)
        else:
            source = p.read_text()
        blocks.extend([relative.as_posix(), prose(source)])
    return '\n\n'.join(blocks) + '\n'


def main():
    chapters = sorted(ROOT.glob('textbook/part[2-7]/ch*'))
    for chapter in chapters:
        paths = sorted(p.relative_to(ROOT) for p in (chapter / '_src').glob('[0-9]*.html'))
        paths += sorted(p.relative_to(ROOT) for p in (ROOT / 'labs' / chapter.parent.name / chapter.name / 'notebooks').glob('[0-9]*.ipynb'))
        run = HERE / 'language' / chapter.name
        run.mkdir(parents=True, exist_ok=True)
        before = corpus(paths, HERE / 'before-language')
        after = corpus(paths, ROOT)
        (run / '01_input.txt').write_text(before)
        (run / 'final.md').write_text(after)
        print(chapter.name, len(before), len(after))

if __name__ == '__main__':
    main()
