"""Build the Part 4 entry and verified practice archive."""
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
from build_bundle import practice_files  # noqa: E402 — shared notebook tooling lives beside the chapters.
from verify import verify_lesson  # noqa: E402 — shared notebook tooling lives beside the chapters.

CHAPTERS = (
    ('ch13-langgraph-basics', 8, 8,
     '상태·노드·갈래를 실행하고, Ch12 검색과 답 만들기를 그래프로 잇습니다.'),
    ('ch14-rag-patterns', 8, 16,
     '질문 재작성과 보정 검색 같은 RAG 패턴을 직접 적고, 같은 질문 벌로 정답 문서의 자리와 서비스 요청 수를 견줍니다.'),
    ('ch15-evaluation-advanced', 8, 8,
     '실패 로그에서 평가 사례를 고르고, 평가 모델 판정과 제시 라벨 일치율, 실행 추적과 대화당 비용, 회귀 스위트와 일괄 처리 입력 파일을 다룹니다.'),
    ('ch16-guardrails', 3, 5,
     '질문과 출처를 검사하고 개인정보를 가리며 대화 기록을 줄이고, 호출 한도·비용 상한 예약과 감사 기록, 문서 속 지시문 검사를 한 흐름으로 잇습니다.'),
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
            notebook = ROOT / 'labs/part4' / slug / 'notebooks' / (lesson['slug'] + '.ipynb')
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
    page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Part 4 · 그래프 · 평가 · 안정화</title><style>{css}</style></head>
    <body><main class="page"><header class="top"><p><a href="../index.html">전체 교재</a></p>
    <h1>Part 4 · 그래프 · 평가 · 안정화</h1>
    <p>Ch 13–16 · {len(reports)}절 · 총 64시간 · 강의 27시간 · 실습 37시간</p></header>
    <div class="intro"><p>Part 3에서 만든 검색과 답변 생성 함수를 그래프로 연결합니다.
    질문과 근거를 처리하는 방법을 비교하고, 실제 실패를 평가한 뒤 입력·출력·사용량을 제한합니다.
    Ch 13 → Ch 14 → Ch 15 → Ch 16 순서로 학습합니다.</p>
    <p><a href="../downloads/part4-practice.zip" download>Part 4 노트북과 실습 자료 받기</a></p>
    <p>HTML은 설명을 읽고 코드를 복사하는 화면입니다. 코드는 Python 3.12용 Jupyter 커널에서
    준비 셀부터 실행합니다. 압축 파일의 ‘시작하기.md’와 각 챕터의 README에 준비 방법이 있습니다.</p></div>
    {''.join(sections)}
    <section><h2>앞에서 만든 자료와 연결하기</h2>
    <p>Ch 12에서 검증한 검색·병합·재정렬·출처 있는 답변 생성은 Ch 13의 그래프 노드로 이어집니다.
    Ch 11의 질문과 정답 문서 ID는 Ch 14의 검색 지표를 계산할 때 다시 사용합니다.
    Ch 15는 Ch 12의 실제 검색 실험 로그를 읽어 실패를 분석합니다. 검색 로그에 답변이 없다면
    그 기록만으로 답변의 정확성을 평가할 수 없으므로 필요한 답변을 따로 생성하고 기록합니다.</p>
    <p>각 노트북은 새 커널에서 실행합니다. 앞 절의 변수에 의존하지 않으며 필요한 파일은
    준비 셀에서 읽습니다. 전달 파일과 실습 범위는 묶음의 <code>labs/part4/continuity-guide.md</code>에 있습니다.</p></section>
    <section><h2>실험에서 확인한 범위</h2>
    <p>어느 노드로 이동할지는 조건문·임계값·호출 횟수로 정합니다. 모델은 질문을 재작성하거나
    답변과 평가 결과를 생성합니다. 이 파트에서 배운 조건과 처리 순서는 중간 프로젝트에 적용합니다.</p>
    <p>같은 질문에서 검색 품질이 나아져도 호출 수나 지연이 늘 수 있습니다. 문서 수·질문 수·
    정답 기준·모델을 함께 기록하고, 실행한 표본 밖에서도 같은 결과가 나오는지는 추가로 확인합니다.
    모델 평가 점수만으로 답변이 정확하다고 판단하지 않습니다. 실제 근거와 사람이 검토한 평가 기준도 확인합니다.</p>
    <p>제공 문서와 개인정보 예시는 학습용 합성 자료입니다. API 생성 문장과 처리 시간은 실행마다
    달라질 수 있습니다. API 재실행에는 사용량에 따른 비용이 발생합니다. 계정이 필요한 외부
    평가 서비스와 비동기 작업은 각 절에서 실제 실행 여부를 확인합니다.</p></section>
    <section><h2>중간 프로젝트에 적용하기</h2>
    <p>검색부터 출처 있는 답변까지 이어지는 그래프와 RAG 패턴 한 가지 이상, 가드레일 한 가지 이상을
    연결합니다. 평가 질문 50문항을 준비하고 개선 전후의 검색 재현율(Recall@50)과 답변의 근거 충실도(Groundedness)를 구분해 제시합니다.
    Recall@50은 정답 문서 중 상위 50개 검색 결과에 포함된 문서의 비율이며, Groundedness는 답변의 주장을 검색 문서가 뒷받침하는지 살펴봅니다.
    대화당 비용의 95백분위수(p95)와 전체 처리 흐름 도식도 함께 작성합니다. p95는 측정한 대화 비용을 작은 순서로 나열했을 때 약 95% 지점의 값입니다. 교재의 작은 실험 결과를 프로젝트의
    50문항 평가 결과로 옮겨 적지 않고, 자신의 전체 흐름을 다시 실행해 측정합니다.</p>
    <p>이후 Ch 21에서는 코드로 정했던 흐름과 모델이 선택하는 흐름을 비교합니다.
    Ch 22에서는 직접 만든 검증과 호출 제한을 Middleware로 구성하는 방법을 배웁니다.</p></section>
    </main></body></html>'''
    (HERE / 'index.html').write_text(page)
    upstream_files = set(json.loads((HERE.parent / 'part3/public-files.json').read_text()))
    upstream_files.discard('labs/part3/continuity-guide.md')
    files = [path for path in practice_files(ROOT)
             if path.relative_to(ROOT).as_posix().startswith(('labs/part4/', 'labs/data/'))
             or path.relative_to(ROOT).as_posix() in upstream_files]
    output = HERE.parent / 'downloads/part4-practice.zip'
    output.parent.mkdir(exist_ok=True)
    prefix, manifest = 'part4-practice/', []
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
    print(f'Part 4: {len(reports)} verified sections; {len(files)} bundled files')


if __name__ == '__main__':
    main()
