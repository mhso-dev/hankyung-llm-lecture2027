"""Build the Part 6 contents and public notebook archive after lesson validation."""
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
    ('ch21-create-agent', 6, 10, '함수 create_agent 한 줄로 에이전트 그래프를 만들어 Ch 20 그래프와 견주고, 구조화 출력 두 전략·실행 정보·옛 함수 옮기기·검색 도구를 다룬 뒤, 같은 평가 질문으로 고정 흐름과 에이전트 흐름을 견주고 대출 문의 에이전트에 양식과 실행 정보를 붙이는 실습을 합니다.'),
    ('ch22-middleware', 8, 16, '호출 전후의 처리에 가드레일을 연결하고 순서와 합성을 확인합니다.'),
    ('ch23-persistence', 6, 10, '체크포인터로 실행 상태를 스레드마다 메모리·PostgreSQL·SQLite에 저장하고, 저장 시점에 따라 강제 종료 뒤 파일에 남는 것을 견주고, 멈춘 실행을 이어 갈 때의 남은 쓰기와 멱등 키를 확인한 뒤, 멈춘 대출 처리를 이어 가고 기록은 한 번만 남기는 실습을 합니다.'),
    ('ch24-human-in-the-loop', 3, 5, '노드 안의 멈춤 표시로 그래프를 멈추고 사람의 답으로 이어 가며, 허용 답 목록에 없는 답이면 조건부 엣지로 다시 묻고, 지난 체크포인트에 값을 고쳐 넣어 새 가지로 다시 실행한 뒤, 대출 연장 신청에 세 기능을 모아 사람의 마지막 답 하나를 바꾸는 실습을 합니다.'),
    ('ch25-streaming', 3, 5, '스트림 모드 일곱을 한 실행에서 받아 사건의 수와 자리를 세고, 모델을 부르는 노드에서 진행 값과 스트림 청크를 함께 받아 이어 붙이며, 사건마다 시각을 적어 첫 사건·첫 토큰 도착·전체 걸린 시간을 한 요청 안에서 잰 뒤, 자료실 문의 답에 세 기능을 모아 요청 전 진행 값 하나를 끄는 실습을 합니다.'),
    ('ch26-delegation', 4, 4, '전문 에이전트를 도구로 부르는 서브에이전트, 다음 차례의 담당을 넘기는 핸드오프, 문의를 분류해 고른 담당에게 보내는 라우터를 만들고, 같은 문의로 세 구조의 모델 요청 수를 셈으로 견주며 한도로 멈춘 실행과 일이 끝난 실행을 완료 조건으로 가른 뒤, 요청 수 셈으로 호출 한도를 정하고 완료 조건으로 확인하는 실습을 합니다.'),
    ('ch27-deepagents', 8, 16, '함수 create_deep_agent가 미리 붙이는 미들웨어와 도구를 조립 결과로 확인하고, 할 일 목록·파일 도구와 백엔드·긴 도구 결과 옮겨 두기·서브에이전트 위임을 호출 한도 두 곳과 요청 수 셈으로 실행한 뒤, 주어진 자료로 답하게 해 출처를 코드로 확인하고 권한 규칙과 사람 승인을 붙이며, 메모 파일 쓰기에 사람 승인을 켜고 끄는 실습을 합니다.'),
    ('ch28-mcp', 5, 11, '서버 파일의 MCP 서버에 메모리로 붙어 판 번호와 기능 목록을 보고, 서버 객체에 도구를 붙여 입력 검사를 확인하며, 서버를 자식 프로세스와 HTTP 서버로 띄워 넘기는 환경 변수와 접근 토큰의 범위를 견준 뒤, MCPAdapter로 바꾼 도구를 에이전트에 붙여 도구 정의가 더하는 입력 토큰을 세고, 에이전트에 붙이는 도구 수를 바꾸는 실습을 합니다.'),
    ('ch29-agent-evaluation', 3, 5, '질문 하나와 기준 궤적으로 최종 답·한 단계·궤적 평가가 보는 자리를 견주고, 궤적 맞춰 보기 네 모드와 인자 비교 방식의 판정 차이를 본 뒤, 실제로 실행한 에이전트 궤적을 네 모드와 평가 모델로 함께 판정하고, 앞 챕터 실행 기록을 공통 칸으로 옮겨 요청 수 셈과 95 백분위수로 읽으며, 호출 한도만 바꾼 두 실행을 견주는 실습을 합니다.'),
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
            notebook = ROOT / 'labs/part6' / slug / 'notebooks' / (lesson['slug'] + '.ipynb')
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
    <title>Part 6 · Agent 개발</title><style>{css}</style></head>
    <body><main class="page"><header class="top"><p><a href="../index.html">전체 교재</a></p>
    <h1>Part 6 · Agent 개발</h1>
    <p>Ch 21–29 · {len(reports)}절 · 총 128시간 · 강의 46시간 · 실습 82시간</p></header>
    {introduction}{''.join(sections)}
    </main></body></html>'''
    (HERE / 'index.html').write_text(page)
    # Explicit prerequisite files supplement the Part 6 public files.
    prerequisites = json.loads((HERE / 'prerequisite-files.json').read_text())
    available = {path.relative_to(ROOT).as_posix(): path for path in practice_files(ROOT)}
    files = [path for name, path in available.items() if name.startswith('labs/part6/')]
    for name in prerequisites:
        if name not in available:
            raise ValueError(f'Prerequisite is not a published public file: {name}')
        files.append(available[name])
    files = list(dict.fromkeys(files))
    output = HERE.parent / 'downloads/part6-practice.zip'
    output.parent.mkdir(exist_ok=True)
    prefix, manifest = 'part6-practice/', []
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
    print(f'Part 6: {len(reports)} verified sections; {len(files)} bundled files')


if __name__ == '__main__':
    main()
