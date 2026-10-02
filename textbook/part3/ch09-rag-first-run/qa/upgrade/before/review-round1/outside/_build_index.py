"""Build Part 3 entry and bundle only verified public practice files."""
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
from build_bundle import practice_files
from verify import verify_lesson

CHAPTERS = (
    ('ch09-rag-first-run', 'Ch 9 · RAG 첫 완주와 실험 기록', 6, 10,
     '문서를 검색해 근거와 함께 답을 생성합니다. 설정을 바꾸어 실행하고 결과를 기록합니다.'),
    ('ch10-document-processing', 'Ch 10 · 문서 처리와 임베딩', 8, 16,
     '문서 형식과 청크 경계를 확인합니다. 같은 자료에서 청킹과 임베딩 설정을 비교합니다.'),
    ('ch11-evaluation', 'Ch 11 · 평가 기초', 6, 10,
     '정답 문서 ID가 있는 질문을 준비하고, 후보의 누락과 상위 순위의 품질을 따로 측정합니다.'),
    ('ch12-retrieval-tuning', 'Ch 12 · 검색 품질과 튜닝', 12, 28,
     '검색·병합·재정렬을 직접 구현하고 같은 질문과 정답 기준으로 설정을 비교합니다.'),
)

START = """# Part 3 실습 시작하기

Part 3은 Ch 9 → Ch 10 → Ch 11 → Ch 12 순서로 학습합니다. 먼저 문서를 검색해 답을 만들고, 문서를 처리하는 방법과 평가 지표를 익힌 뒤 검색 설정을 조절합니다. 질문과 정답 기준을 유지해야 변경 전후를 비교할 수 있습니다.

압축을 푼 `part3-practice` 폴더 전체를 보관합니다. 노트북은 `labs/part3`의 챕터별 `notebooks` 폴더에 있습니다. 제공 PDF는 `labs/data/rag-corpus/pdf`에 있으므로 노트북만 다른 폴더로 옮기지 않습니다. 문서는 가상 기관을 다룬 학습용 자료이며 실제 기관의 안내가 아닙니다. 평가용 질문의 정답 문서 ID는 검색 지표를 계산하기 위한 학습 자료입니다.

`labs/part3/continuity-guide.md`에서 챕터 간 실행 순서와 전달 파일을 확인합니다. Ch9 06절과 Ch10 08절의 검색 로그를 Ch11 06절에서 읽어 평가합니다. 배포 묶음에 포함된 검증 로그로 Ch11을 독립 실행할 수도 있으며, 앞 두 절을 다시 실행하면 자신의 검색 결과를 평가할 수 있습니다.

VS Code에서 지금 학습할 챕터 폴더(예: `labs/part3/ch09-rag-first-run`)를 열고 그 폴더의 터미널에서 `uv sync --locked`로 패키지와 커널을 준비합니다. 이 챕터의 `.venv`를 노트북 커널로 선택합니다. 각 챕터의 `README.md`에서 세부 준비 사항을 확인합니다. Python 3.12를 사용하는 Jupyter Notebook·JupyterLab 또는 VS Code Jupyter 화면에서 노트북을 엽니다. 준비한 Python 3.12 커널을 고른 뒤 첫 셀부터 `Shift+Enter`로 실행합니다. 패키지 설치가 마무리될 때까지 기다린 뒤 코드 바로 뒤의 출력과 해설을 읽습니다. 각 절은 새 커널에서 독립 실행합니다.

묶음 맨 위의 `env.example`을 `.env`라는 이름으로 복사하고 `OPENAI_API_KEY=` 오른쪽에 본인의 키를 저장합니다. 키를 코드나 출력에 붙여 넣지 않습니다. API를 호출하는 생성·임베딩 예제에는 사용량에 따른 비용이 발생합니다. 로컬 리랭커는 첫 실행 때 모델 파일을 내려받으므로 네트워크와 저장 공간이 필요합니다. 다운로드 시간과 추론 시간을 구분합니다.

Ch 12의 pgvector 절은 Docker로 별도 실습용 PostgreSQL을 준비합니다. 02절과 실습 README의 명령·연결 정보를 먼저 확인합니다. 학습용 포트는 `127.0.0.1:55432`이며 실제 업무 데이터베이스를 연결하지 않습니다. 같은 이름의 컨테이너가 이미 있으면 새로 만들기 전에 실행 상태를 확인합니다. 실습 후에는 본인이 만든 실습 컨테이너를 중지합니다.

오류가 발생하면 먼저 준비 셀과 파일 위치를 확인합니다. `NameError`는 앞 셀의 변수 생성 여부, `ModuleNotFoundError`는 해당 챕터의 잠금 환경 준비와 `.venv` 선택 여부, `FileNotFoundError`는 묶음의 폴더 구조를 확인합니다. 데이터베이스 연결 오류는 컨테이너 상태와 실습 포트를 확인합니다. 변수 상태를 확인하기 어려우면 커널을 다시 시작하고 처음부터 실행합니다.

TF-IDF와 MMR 설정을 바꾼 36건의 개발용 검색 비교 기록이 있어도 검색 품질이 개선되었다고 곧바로 결론 내리지 않습니다. 같은 평가셋의 지표·누락 사례·처리 시간을 함께 읽고, 설정을 고르는 데 쓰지 않은 질문으로 다시 확인합니다. 제공 자료에서의 결과를 모든 한국어 업무 문서에 적용하지 않습니다.

`manifest.json`은 파일별 SHA-256 목록입니다. 실행 결과의 문장·순위·시간은 API·모델·환경에 따라 달라질 수 있습니다. 이 HTML 교재는 설명과 코드 복사용이며, 코드는 Jupyter에서 실행합니다.
"""


def main() -> None:
    sections, reports = [], []
    for slug, title, lecture, practice, description in CHAPTERS:
        chapter = HERE / slug
        sources = sorted((chapter / '_src').glob('[0-9][0-9]-*.html'))
        if len(sources) != lecture or not (chapter / 'index.html').is_file():
            raise ValueError(f'Incomplete chapter: {slug}')
        for source in sources:
            notebook = ROOT / 'labs/part3' / slug / 'notebooks' / f'{source.stem}.ipynb'
            reports.append(verify_lesson(notebook, chapter / source.name))
        links = ''.join(
            f'<li><a href="{slug}/{html.escape(source.name, quote=True)}">'
            f'{html.escape(source.stem.replace("-", " "))}</a></li>' for source in sources)
        sections.append(
            f'<section><h2><a href="{slug}/index.html">{html.escape(title)}</a></h2>'
            f'<p>{description}</p><p>강의 {lecture}시간 · 실습 {practice}시간 · '
            f'{len(sources)}절</p><ol>{links}</ol></section>')
    css = (RUNTIME / 'theme.css').read_text() + """
    *{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,sans-serif;
    line-height:1.8;word-break:keep-all;color:#202020;background:#fff}
    a{color:#2456a6;overflow-wrap:anywhere}h1{font-size:30px;line-height:1.4}
    h2{font-size:24px;margin-top:40px}li{margin:8px 0}p,li{font-size:16px}
    .intro{padding:18px;background:#f5f7fa;border:1px solid #cbd5e1;border-radius:8px}
    """
    page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Part 3 · RAG</title><style>{css}</style></head>
    <body><main class="page"><header class="top"><p><a href="../index.html">전체 교재</a></p>
    <h1>Part 3 · RAG</h1><p>Ch 9–12 · 32절 · 총 96시간 · 강의 32시간 · 실습 64시간</p></header>
    <div class="intro"><p>문서에서 근거를 찾아 답을 만드는 과정을 끝까지 실행합니다.
    문서 처리와 평가 지표를 익힌 뒤 검색 방법과 설정을 비교합니다. Ch 9 → Ch 10 → Ch 11 → Ch 12 순서로 읽습니다.</p>
    <p><a href="../downloads/part3-practice.zip" download>Part 3 노트북과 실습 자료 받기</a></p>
    <p>HTML은 교재를 읽고 코드를 복사하는 화면입니다. 코드는 Python 3.12용 Jupyter 커널에서
    첫 셀부터 실행합니다. 키·패키지·데이터베이스 준비는 묶음의 ‘시작하기.md’와 각 절의 준비 설명을 확인합니다.</p></div>
    {''.join(sections)}
    <section><h2>챕터 간 실행 연결</h2><p>Ch9 06절과 Ch10 08절의 실제 검색 로그를 Ch11 06절에서 읽어 검색 지표를 계산합니다. 각 노트북은 새 커널에서 실행하며, 앞 장의 변수 대신 저장한 파일을 사용합니다. 배포 묶음의 <code>labs/part3/continuity-guide.md</code>에 실행 순서와 식별자 대응을 정리했습니다.</p><p>Ch12의 36건은 TF-IDF와 MMR 설정 비교입니다. 검색부터 답변 생성까지 이어지는 통합 RAG는 별도로 실행하고 기록합니다. Ch11은 검색을 평가하며 생성 답변 평가는 Ch15에서 이어집니다.</p></section>
    <section><h2>실험 결과를 읽을 때</h2>
    <p>검색 후보에 정답이 포함되었는지와 정답이 상위에 있는지를 따로 확인합니다.
    Recall@50은 후보 누락을, Precision@5와 nDCG@5는 상위 결과의 관련성과 순서를 살펴보는 데 사용합니다.
    지표를 비교할 때 질문·정답 문서 ID·문서 집합과 설정을 함께 기록합니다.</p>
    <p>제공 PDF 21건은 학습용 합성 자료입니다. 자신의 업무 분야 문서 100건을 사용하는 확장 실습에서는
    문서 사용 권한과 개인정보를 확인하고, 실제 문서에서 평가 질문과 정답 근거를 다시 작성합니다.</p>
    <p>리랭커에 입력한 후보에 정답 문서가 없다면 재정렬만으로 해당 문서를 추가할 수 없습니다.
    한 설정의 평균 점수가 높아져도 어떤 질문의 결과가 나빠졌는지 함께 읽습니다.
    실제 문서의 출처와 내용을 확인하는 과정은 지표 계산과 별도로 필요합니다.</p>
    <p>Part 3을 마치면 Ch 13에서 이 검색 흐름을 그래프로 옮깁니다.
    Part 3에서 만든 질문·정답 문서 ID·실험 기록은 다음 평가 실습에도 사용합니다.</p></section>
    </main></body></html>'''
    (HERE / 'index.html').write_text(page)
    files = [path for path in practice_files(ROOT)
             if path.relative_to(ROOT).as_posix().startswith(('labs/part3/', 'labs/data/'))]
    output = HERE.parent / 'downloads/part3-practice.zip'
    output.parent.mkdir(exist_ok=True)
    prefix, manifest = 'part3-practice/', []
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        archive.writestr(prefix + '시작하기.md', START)
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
    qa = HERE / 'qa'
    qa.mkdir(exist_ok=True)
    (qa / 'integration-results.json').write_text(json.dumps({
        'sections': len(reports), 'code_cells': sum(r['code_cells'] for r in reports),
        'max_cell_lines': max(r['max_cell_lines'] for r in reports),
        'notebook_html_downloads_match': True, 'bundle_files': len(files),
        'bundle_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
        'bundle_manifest_verified': True,
    }, ensure_ascii=False, indent=2))
    print(f'Part 3: {len(reports)} verified sections; {len(files)} bundled files')


if __name__ == '__main__':
    main()
