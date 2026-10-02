"""Generate the student entry page using the shared notebook theme."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
chapters = [
    ('01', '오리엔테이션 · 개발환경', 'part1/ch01-development-environment', 5,
     '개발 도구와 Python 실행 환경을 준비하고 첫 스크립트의 오류를 직접 확인합니다.'),
    ('02', '파이썬 프로그래밍', 'part1/ch02-python', 12,
     '기초 문법부터 테스트·데이터 검증·패키징을 익히고 두 트랙 모두 비동기 실행을 확인합니다.'),
    ('03', 'Git과 GitHub 협업', 'part1/ch03-git-github', 5,
     '변경을 커밋하고 리뷰하며 충돌 해결과 이력 복구를 실습합니다.'),
    ('04', '데이터 다루기', 'part1/ch04-data-tools', 5,
     '표·SQL·HTTP·문서에서 데이터를 조회하는 함수를 만들고 테스트합니다.'),
    ('05', 'LLM 동작 원리', 'part1/ch05-llm-principles', 8,
     '로컬 모델로 토큰·유사도·샘플링을 측정하고 생성 결과의 한계를 확인합니다.'),
    ('06', 'LangChain 시작', 'part2/ch06-langchain-start', 6,
     '첫 모델 호출부터 메시지·구조화 출력·스트리밍을 익히고 오류와 사용량을 확인합니다.'),
    ('07', '프롬프트 엔지니어링', 'part2/ch07-prompt-engineering', 8,
     '같은 과제에서 역할·예시·출력 지시를 바꾸며 답과 토큰·지연을 비교합니다.'),
    ('08', '컨텍스트 엔지니어링', 'part2/ch08-context-engineering', 6,
     '모델에 보낼 자료의 양을 정하고, 필요한 정보를 골라 정리합니다.'),
    ('09', 'RAG 첫 완주와 실험 기록', 'part3/ch09-rag-first-run', 6,
     '문서를 나누고 검색한 뒤, 근거를 포함한 답을 생성합니다.'),
    ('10', '문서 처리와 임베딩', 'part3/ch10-document-processing', 8,
     '여러 형식의 문서를 읽고 검색할 단위로 나눕니다. 문서를 숫자로 바꾼 결과와 저장해 둔 결과의 재사용도 확인합니다.'),
    ('11', '평가 기초', 'part3/ch11-evaluation', 6,
     '정답 문서 ID가 있는 질문으로 검색 누락과 상위 순위의 품질을 따로 측정합니다.'),
    ('12', '검색 품질과 튜닝', 'part3/ch12-retrieval-tuning', 12,
     '벡터·키워드 검색을 병합하고 후보를 재정렬하며 같은 평가셋으로 설정을 비교합니다.'),
    ('13', 'LangGraph 기초', 'part4/ch13-langgraph-basics', 7,
     '상태·노드·분기를 실행하고 검색부터 답변까지 이어지는 그래프를 만듭니다.'),
    ('14', 'RAG 패턴 확장', 'part4/ch14-rag-patterns', 9,
     '질문 재작성과 검색 보완 방법을 직접 구현하고 품질·지연·사용량을 비교합니다.'),
    ('15', '평가 심화', 'part4/ch15-evaluation-advanced', 8,
     '실패 기록에서 평가 항목을 정하고 모델 평가·추적·비용 분포·회귀 검사를 연결합니다.'),
    ('16', '가드레일 · 안정화', 'part4/ch16-guardrails', 6,
     '입출력과 호출 한도를 검증하고 문서 속 지시문에 대한 반응을 확인합니다.'),
]
rows = ''.join(f'<tr><td>Ch {number}</td><td><a href="{folder}/index.html">{title}</a>'
               f'<p>{description}</p></td><td>{count}절</td></tr>'
               for number, title, folder, count, description in chapters)
style = ':root{--sans:system-ui,-apple-system,sans-serif;--mono:ui-monospace,monospace}'
style += '*{box-sizing:border-box}body{margin:0;line-height:1.8;word-break:keep-all;font-family:var(--sans)}'
style += 'table{border-collapse:collapse;width:100%;margin:30px 0}td{padding:18px 10px;border-bottom:1px solid #ddd;vertical-align:top}td p{margin:8px 0 0;color:#555;font-size:16px}h2{margin-top:36px}'
style += (HERE / 'theme.css').read_text()
part_links = ''.join(
    f'<p><a href="{folder}/index.html">{title} 전체 읽기</a> · '
    f'<a href="downloads/{folder}-practice.zip" download>{label} 실습 파일 받기</a></p>'
    for folder, label, title in (
        ('part1', 'Part 1', 'Part 1 · 개발 기반'),
        ('part2', 'Part 2', 'Part 2 · LangChain과 프롬프트'),
        ('part3', 'Part 3', 'Part 3 · RAG'),
        ('part4', 'Part 4', 'Part 4 · 그래프 · 평가 · 안정화'),
    )
    if (HERE.parent / folder / 'index.html').is_file()
    and (HERE.parent / 'downloads' / f'{folder}-practice.zip').is_file()
)
page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LLM Agent 개발 &amp; 바이브코딩 교재</title><style>{style}</style></head>
<body><main class="page"><header class="top"><p>한경 KDT · LLM Agent 개발 &amp; 바이브코딩</p>
<h1>개념을 읽고 셀을 실행하며 배웁니다</h1>
<p>개발을 처음 시작해도 설명을 읽고 셀을 하나씩 실행하며 따라갈 수 있도록 구성했습니다.
기본 결과를 확인한 뒤 값 하나를 바꾸고 무엇이 달라졌는지 비교합니다.</p></header>
{part_links}
<table><tbody>{rows}</tbody></table>
<h2>처음 실습할 때</h2>
<p>처음 개발한다면 <a href="part1/ch01-development-environment/index.html">Ch 1 개발환경</a>부터 읽습니다. Ch 1 실습에는 API 키가 필요하지 않으며 도구 설치와 가상환경 준비를 안내합니다.</p>
<ol>
<li><a href="downloads/llm-practice.zip" download>노트북과 실습 파일 함께 받기</a>를 선택하고 압축을 풉니다.
노트북과 문서가 들어 있는 <code>labs</code> 안의 파일을 다른 폴더로 옮기지 않습니다.</li>
<li>모델을 호출하는 API 실습에서는 압축을 풀어 생긴 <code>llm-practice</code> 폴더의 <code>env.example</code>을 복사해 <code>.env</code>로 저장하고,
<code>OPENAI_API_KEY=</code> 오른쪽에 본인의 키를 넣습니다. 키를 코드나 출력에 붙여 넣지 않습니다.</li>
<li>지금 학습할 챕터 폴더에서 <code>uv sync --locked</code>로 잠금 파일의 패키지와 커널을 준비합니다. 그 챕터의 <code>.venv</code>를 노트북 커널로 선택하고 원하는 절을 엽니다.
코드 셀을 선택하고 <code>Shift+Enter</code>를 눌러 첫 셀부터 순서대로 실행합니다.
설치 셀이 있는 절에서는 설치가 끝날 때까지 기다립니다. 실행 중 표시가 사라진 뒤 오류 메시지가 없는지 확인합니다.</li>
</ol>
<p>Ch1에서 uv를 준비한 뒤 <a href="https://code.visualstudio.com/docs/getstarted/overview">VS Code</a>에서 지금 학습할 챕터 폴더를 엽니다. 예를 들어 Ch6은 <code>labs/part2/ch06-langchain-start</code>입니다. Microsoft의 Python·Jupyter 확장을 설치하고 그 폴더의 터미널에서 <code>uv sync --locked</code>를 실행합니다. <code>uv run python --version</code>으로 Python 3.12를 확인한 뒤 Select Kernel → Python Environments에서 같은 챕터의 <code>.venv</code>를 선택합니다. 다음 챕터에서도 그 챕터의 환경을 준비하고 선택합니다. 커널은 코드를 실행하고 변수를 기억하는 프로그램입니다. JupyterLab은 같은 폴더에서 <code>uv run --with jupyterlab==4.4.9 jupyter lab</code>으로 실행할 수 있습니다. <a href="https://code.visualstudio.com/docs/datascience/jupyter-notebooks#_setting-up-your-environment">공식 노트북 환경 안내</a>와 묶음의 ‘시작하기.md’에서 단계별 준비 방법을 확인합니다. 최초 설치·모델 다운로드·API 호출에는 인터넷 연결이 필요합니다. 실습 파일 묶음에는 프로그램 자체가 포함되어 있지 않습니다.</p>
<h2>한 절을 따라 하는 순서</h2>
<p>짧은 설명을 읽고 기본 코드를 실행합니다. 안내에 적힌 본문·문서 수·숫자 목록의 길이·출처 등의 값을 확인한 뒤,
지정한 값 하나만 바꿔 결과를 비교합니다. Before/After가 있는 절은 기본값으로 돌아온 다음 두 단계를 차례대로 실행합니다. 현상을 측정하는 절은 실험 결과와 해석을 확인합니다.
‘원리 더 알아보기’가 표시된 절에서는 먼저 기본 실습을 마친 뒤 해당 설명을 읽습니다.</p>
<p>API 셀을 다시 실행하면 사용량에 따른 비용이 발생하며, 모델이 생성한 문장은 실행마다 달라질 수 있습니다.</p>
<details><summary>실행이 막혔을 때 확인할 점</summary>
<p><code>NameError</code>는 앞에서 만드는 변수가 준비되지 않았을 때 나타날 수 있습니다. 첫 셀부터 실행했는지 확인합니다.
<code>ModuleNotFoundError</code>가 나오면 현재 챕터에서 <code>uv sync --locked</code>를 실행했는지와 그 챕터의 <code>.venv</code>를 선택했는지 확인합니다. 설치 셀이 있는 절은 그 셀도 실행합니다.</p>
<p><code>FileNotFoundError</code>가 나오면 제공 파일이 제자리에 있는지 확인합니다. 노트북만 낱개로 옮겼다면 실습 파일 묶음의 원래 폴더 구조로 되돌립니다.
키 관련 오류는 <code>.env</code>의 파일명과 키 이름을 확인하며, 키 값 자체는 출력하지 않습니다.</p>
<p>변수가 예상과 다르게 남아 있으면 커널을 다시 시작하고 첫 셀부터 실행합니다. 커널을 다시 시작하면 이전 변수는 사라집니다.</p></details>
<p>이 HTML은 교재를 읽고 코드를 복사하는 화면입니다. 코드 실행과 값 수정은 Jupyter에서 합니다.</p>
</main></body></html>'''
(HERE.parent / 'index.html').write_text(page, encoding='utf-8')
