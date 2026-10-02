"""Build the Part 5 contents and public notebook archive after lesson validation."""
from __future__ import annotations

import hashlib
import html
import json
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUNTIME = HERE.parent / '_notebook'
sys.path.insert(0, str(RUNTIME))
from build_bundle import practice_files  # noqa: E402
from verify import verify_lesson  # noqa: E402

CHAPTERS = (
    ('ch17-agent-overview', 5, 3,
     '실행 기록에서 다음 단계를 정한 쪽을 가르고, 모델이 고르는 루프와 정지 조건을 실행해 자율성의 대가를 잰 뒤 환불 문의 흐름을 진단합니다.'),
    ('ch18-workflow-patterns', 4, 12,
     'OpenAI SDK로 다섯 워크플로우 패턴을 직접 만들고, 같은 과제에서 요청 수·토큰 수·걸린 초·품질 칸을 견준 뒤 라우팅 검사와 나눠 쓰기를 잇는 실습을 합니다.'),
    ('ch19-model-tools', 6, 10,
     '조회 함수를 도구로 감싸 입력 형식과 설명을 적고, 모델이 고른 도구를 실행해 도구 메시지로 잇고, 읽기·쓰기 도구를 나눠 주문 취소 문의를 처리하는 실습을 합니다.'),
    ('ch20-tool-node', 3, 5,
     '모델 노드와 도구 실행 노드를 되돌아가는 엣지로 잇고 도구 오류·실행 한도·명시적 종료를 다룬 뒤, 규칙 갈래와 모델 선택을 견주고 자료실 문의 그래프에 오류 처리 함수와 실행 한도를 붙이는 실습을 합니다.'),
)


def main() -> None:
    sections, reports = [], []
    for slug, lecture, practice, description in CHAPTERS:
        chapter = HERE / slug
        config = json.loads((chapter / 'chapter.json').read_text())
        if not config['sections'] or not (chapter / 'index.html').is_file():
            raise ValueError(f'Incomplete chapter: {slug}')
        links = []
        for lesson in config['sections']:
            filename = lesson['slug'] + '.html'
            notebook = ROOT / 'labs/part5' / slug / 'notebooks' / (lesson['slug'] + '.ipynb')
            reports.append(verify_lesson(notebook, chapter / filename))
            links.append(f'<li><a href="{slug}/{html.escape(filename, quote=True)}">'
                         f'{html.escape(lesson["title"])}</a></li>')
        sections.append(f'<section><h2><a href="{slug}/index.html">'
                        f'Ch {slug[2:4]} · {html.escape(config["title"])}</a></h2>'
                        f'<p>{description}</p><p>강의 {lecture}시간 · 실습 {practice}시간 · '
                        f'{len(links)}절</p><ol>{"".join(links)}</ol></section>')
    css = (RUNTIME / 'theme.css').read_text() + '''
    *{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,sans-serif;
    line-height:1.8;word-break:keep-all;color:#202020;background:#fff}
    a{color:#2456a6;overflow-wrap:anywhere}h1{font-size:30px;line-height:1.4}
    h2{font-size:24px;margin-top:40px}li{margin:8px 0}p,li{font-size:16px}
    .intro{padding:18px;background:#f5f7fa;border:1px solid #cbd5e1;border-radius:8px}
    '''
    introduction = (HERE / '_src/index.html').read_text()
    page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Part 5 · Agent 입문</title><style>{css}</style></head>
    <body><main class="page"><header class="top"><p><a href="../index.html">전체 교재</a></p>
    <h1>Part 5 · Agent 입문</h1>
    <p>Ch 17–20 · {len(reports)}절 · 총 48시간 · 강의 18시간 · 실습 30시간</p></header>
    {introduction}{''.join(sections)}
    </main></body></html>'''
    (HERE / 'index.html').write_text(page)
    # Ch19 reuses the public Ch4 query data; bundle it at its original relative path.
    files = [path for path in practice_files(ROOT)
             if path.relative_to(ROOT).as_posix().startswith(
                 ('labs/part5/', 'labs/part1/ch04-data-tools/'))]
    output = HERE.parent / 'downloads/part5-practice.zip'
    output.parent.mkdir(exist_ok=True)
    prefix, manifest = 'part5-practice/', []
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        archive.writestr(prefix + '시작하기.md', (HERE / 'practice-start.md').read_text())
        archive.writestr(prefix + 'env.example', 'OPENAI_API_KEY=\n')
        for path in files:
            relative, data = path.relative_to(ROOT).as_posix(), path.read_bytes()
            archive.writestr(prefix + relative, data)
            manifest.append({'path': relative, 'sha256': hashlib.sha256(data).hexdigest()})
        archive.writestr(prefix + 'manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2))
    with ZipFile(output) as archive:
        assert archive.testzip() is None
        for entry in manifest:
            assert hashlib.sha256(archive.read(prefix + entry['path'])).hexdigest() == entry['sha256']
    (HERE / 'qa/integration-results.json').write_text(json.dumps({
        'sections': len(reports), 'code_cells': sum(r['code_cells'] for r in reports),
        'max_cell_lines': max(r['max_cell_lines'] for r in reports),
        'notebook_html_downloads_match': True, 'bundle_files': len(files),
        'bundle_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
        'bundle_manifest_verified': True,
    }, ensure_ascii=False, indent=2))
    print(f'Part 5: {len(reports)} verified sections; {len(files)} bundled files')


if __name__ == '__main__':
    main()
