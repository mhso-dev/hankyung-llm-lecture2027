"""Build the Part 7 contents and public notebook archive after lesson validation."""
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
from build_bundle import practice_files  # noqa: E402 — shared local build runtime
from verify import verify_lesson  # noqa: E402 — shared local build runtime

CHAPTERS = (
    ('ch30-fastapi-serving', 10, 22, '처리 함수의 입력 형식과 의존성 재정의에서 시작해 ainvoke·astream과 SSE 사건의 이어 받기·오류 사건을 보고, CORS·접근 토큰·시간 제한과 응답 문서·생성 SDK를 확인한 뒤, 실제 에이전트를 HTTP로 부르고 한 요청 흐름을 잇는 실습을 합니다.'),
    ('ch31-database', 5, 11, '비동기 엔진과 연결 풀, 한 묶음 작업과 취소, Alembic 판 올리기·내리기, 반납과 대기 제한을 보고, pgvector 색인·체크포인터 표의 백업과 복원을 확인한 뒤, 세 기능을 상담 예약 그래프 하나로 잇는 실습을 합니다.'),
    ('ch32-docker', 5, 11, '서비스 이미지를 빌드하고 데이터베이스와 함께 실행하며 크기·캐시·상태를 측정합니다.'),
    ('ch33-cicd', 5, 11, '테스트와 평가 회귀를 자동으로 확인하고 배포·모니터링·롤백 절차를 구성합니다.'),
    ('ch34-cost-rate-limits', 3, 5, '공통 앞부분 뒤에 둔 요청의 캐시 입력과 요금을 세고, 일괄 처리 결과를 요청 이름표로 짝지으며, 모델 라우터와 모델마다 요금표, 겹친 다시 보내기와 한꺼번에 보내는 수, 예산 가드의 예약과 95 백분위수를 본 뒤, 세 기능을 문의 셋의 흐름 하나로 잇는 실습을 합니다.'),
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
            notebook = ROOT / 'labs/part7' / slug / 'notebooks' / (lesson['slug'] + '.ipynb')
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
    <title>Part 7 · 서비스화와 배포</title><style>{css}</style></head>
    <body><main class="page"><header class="top"><p><a href="../index.html">전체 교재</a></p>
    <h1>Part 7 · 서비스화와 배포</h1>
    <p>Ch 30–34 · {len(reports)}절 · 총 88시간 · 강의 28시간 · 실습 60시간</p></header>
    {introduction}{''.join(sections)}
    </main></body></html>'''
    (HERE / 'index.html').write_text(page)
    # Explicit prerequisite files supplement the Part 7 public files.
    prerequisites = json.loads((HERE / 'prerequisite-files.json').read_text())
    available = {path.relative_to(ROOT).as_posix(): path for path in practice_files(ROOT)}
    files = [path for name, path in available.items() if name.startswith('labs/part7/')]
    for name in prerequisites:
        if name not in available:
            raise ValueError(f'Prerequisite is not a published public file: {name}')
        files.append(available[name])
    files = list(dict.fromkeys(files))
    output = HERE.parent / 'downloads/part7-practice.zip'
    output.parent.mkdir(exist_ok=True)
    prefix, manifest = 'part7-practice/', []
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
    print(f'Part 7: {len(reports)} verified sections; {len(files)} bundled files')


if __name__ == '__main__':
    main()
