"""Shared Jupyter-style HTML presentation for verified lesson notebooks."""
from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path

from execute import code_hash, output_hash

CSS = (Path(__file__).with_name('theme.css')).read_text()
SCRIPT = '<script>' + Path(__file__).with_name('copy.js').read_text() + '</script>'


def text(value: str | list[str]) -> str:
    return value if isinstance(value, str) else ''.join(value)


def markdown(source: str, attachments: dict | None = None) -> str:
    # Lesson authors use HTML-compatible Markdown; ordinary prose remains readable.
    if re.search(r'<(?:p|h[1-6]|ul|ol|div|table|details)\b', source):
        return source
    result = []
    for block in source.strip().split('\n\n'):
        image = re.fullmatch(r'!\[([^\]]*)\]\(attachment:([^)]+)\)', block.strip())
        if image and attachments and image[2] in attachments:
            mime, data = next(iter(attachments[image[2]].items()))
            result.append(f'<img class="nb-image" src="data:{mime};base64,{data}" alt="{html.escape(image[1])}">')
            continue
        escaped = html.escape(block)
        escaped = re.sub(r'`([^`]+)`', r'<code>\1</code>', escaped)
        escaped = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', escaped)
        heading = re.match(r'^(#{1,6}) (.*)', escaped, re.DOTALL)
        if heading:
            level = min(len(heading[1]) + 1, 6)
            result.append(f'<h{level}>{heading[2]}</h{level}>')
        else:
            result.append(f'<p>{escaped}</p>')
    return '\n'.join(result)


def validate(nb: dict) -> None:
    report = nb.get('metadata', {}).get('verification', {})
    if report.get('status') != 'passed' or not report.get('fresh_kernel'):
        raise ValueError('Notebook has no successful fresh-kernel verification')
    version = nb.get('metadata', {}).get('language_info', {}).get('version', '')
    if not version.startswith('3.12.'):
        raise ValueError('Notebook was not executed by a Python 3.12 kernel')
    if report.get('code_sha256') != code_hash(nb):
        raise ValueError('Notebook code changed after execution; rerun required')
    if report.get('outputs_sha256') != output_hash(nb):
        raise ValueError('Notebook outputs changed after execution; rerun required')
    count = 0
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            count += 1
            if cell.get('execution_count') is None:
                raise ValueError('Unexecuted notebook cell')
            if cell['execution_count'] != count:
                raise ValueError('Notebook execution counts must be sequential from 1')
            if any(o['output_type'] == 'error' for o in cell.get('outputs', [])):
                raise ValueError('Notebook contains an uncaught error')


def lesson_part(cell: dict) -> str:
    return cell.get('metadata', {}).get('lesson_part', 'example')


def validate_parts(nb: dict) -> None:
    order = {'example': 0, 'before': 1, 'after': 2}
    stages = [lesson_part(cell) for cell in nb['cells']]
    if any(stage not in order for stage in stages):
        raise ValueError('Unknown notebook lesson_part')
    lesson_format = nb.get('metadata', {}).get('lesson_format', 'paired')
    if lesson_format not in {'paired', 'experiment'}:
        raise ValueError(f'Unknown notebook lesson format: {lesson_format}')
    if lesson_format == 'experiment':
        if any(stage != 'example' for stage in stages):
            raise ValueError('Experiment notebooks may contain only example cells')
        if not any(cell['cell_type'] == 'code' for cell in nb['cells']):
            raise ValueError('Experiment notebook requires code cells')
        return
    ranks = [order[stage] for stage in stages]
    if ranks != sorted(ranks):
        raise ValueError('Cells must follow example, before, after order')
    for stage in order:
        cells = [c for c in nb['cells']
                 if lesson_part(c) == stage and c['cell_type'] == 'code']
        if not cells:
            raise ValueError(f'Missing code cells for {stage}')
        observed = any(text(output.get('text', '') if output['output_type'] == 'stream'
                            else output.get('data', {}).get('text/plain', '')).strip()
                       for cell in cells for output in cell.get('outputs', []))
        if stage != 'example' and not observed:
            raise ValueError(f'Missing observed output for {stage}')


def render_cells(cells: list[dict]) -> str:
    parts = []
    for cell in cells:
        source = text(cell['source'])
        if cell['cell_type'] == 'markdown':
            if cell.get('metadata', {}).get('html') == 'skip':
                continue  # 노트북 전용 안내(제목·핵심 그림)는 HTML 본문과 겹치므로 생략한다.
            parts.append(f'<div class="nb-markdown">{markdown(source, cell.get("attachments"))}</div>')
        elif cell['cell_type'] == 'code':
            count = cell['execution_count']
            parts.append(f'<div class="nb-cell"><div class="nb-prompt">In [{count}]:</div>'
                         '<div class="nb-input"><button type="button" class="copy-cell" '
                         'aria-label="이 셀의 코드 복사">복사</button>'
                         f'<pre><code class="language-python nb-source">{html.escape(source)}</code></pre></div></div>')
            for output in cell.get('outputs', []):
                data = output.get('data', {})
                if output['output_type'] == 'stream':
                    rendered = html.escape(text(output.get('text', '')))
                elif 'text/plain' in data:
                    rendered = html.escape(text(data['text/plain']))
                else:
                    raise ValueError('Unsupported output: provide text/plain for the lesson')
                # Preserve progress-stream carriage returns through HTML file reads.
                rendered = rendered.replace('\r', '&#13;')
                parts.append('<div class="nb-result"><div class="nb-prompt">출력:</div>'
                             f'<pre class="nb-output">{rendered}</pre></div>')
    return '\n'.join(parts)


def render_notebook(lab: Path, slug: str, part: str | None = None) -> str:
    path = lab / 'notebooks' / f'{slug}.ipynb'
    raw = path.read_bytes()
    nb = json.loads(raw)
    validate(nb)
    lesson_format = nb.get('metadata', {}).get('lesson_format', 'paired')
    if lesson_format not in {'paired', 'experiment'}:
        raise ValueError(f'Unknown notebook lesson format: {lesson_format}')
    if lesson_format == 'experiment' or part is not None:
        validate_parts(nb)
    if lesson_format == 'experiment' and part is not None:
        raise ValueError('Experiment notebook must use one unsplit notebook token')
    if part is not None and part not in {'example', 'failure'}:
        raise ValueError(f'Unknown notebook display part: {part}')
    parts = [(f'<section class="notebook" data-notebook="{html.escape(slug)}" '
              f'data-lesson-format="{lesson_format}" '
              'aria-label="순서대로 실행하는 노트북">')]
    if part != 'failure':
        download = base64.b64encode(raw).decode()
        timestamp = nb['metadata']['verification']['executed_at'][:10]
        copy_note = ('전체 코드 복사에는 실험 셀 전체가 포함됩니다. '
                     if lesson_format == 'experiment' else
                     '전체 코드 복사에는 아래의 Before/After 셀도 포함됩니다. ')
        parts.append(f'<div class="nb-toolbar"><span>Python 3.12 · 실행 확인 {timestamp}</span>'
                     '<button type="button" class="copy-all">전체 코드 복사</button>'
                     f'<a download="{html.escape(path.name)}" '
                     f'href="data:application/x-ipynb+json;base64,{download}">노트북만 내려받기</a></div>'
                     '<p class="nb-guide">준비된 Python 3.12 노트북에서 첫 셀부터 '
                     '<code>Shift+Enter</code>로 하나씩 실행합니다. '
                     '안내한 결과를 먼저 확인하고 지정한 값 하나를 바꿔 비교합니다. '
                     '문서를 사용하는 실습은 파일 묶음이 필요합니다. '
                     '<a href="../../downloads/llm-practice.zip" download>노트북과 실습 파일 함께 받기</a> · '
                     '<a href="../../index.html">처음 실습하는 방법</a>. '
                     + copy_note +
                     '이 HTML에서는 코드를 실행하지 않습니다.</p>')
    if part == 'failure':
        parts.append('<p class="nb-guide">앞의 실행 예제를 실행한 같은 노트북에서 '
                     'Before 다음 After 순서로 실행합니다. 출력은 실제 실행 결과입니다.</p>'
                     '<div class="nb-comparison">')
        for stage, title in [('before', 'Before — 실패 코드'), ('after', 'After — 수정 코드')]:
            parts.append(f'<section class="nb-stage" data-lesson-stage="{stage}"><h3>{title}</h3>')
            parts.append(render_cells([c for c in nb['cells'] if lesson_part(c) == stage]))
            parts.append('</section>')
        parts.append('</div>')
    else:
        cells = nb['cells'] if part is None else [c for c in nb['cells'] if lesson_part(c) == part]
        parts.append(render_cells(cells))
    parts.append('<p class="copy-status" role="status" aria-live="polite"></p></section>')
    return '\n'.join(parts)


def expand_notebooks(body: str, lab: Path) -> str:
    pattern = r'\{\{notebook:([^}|]+)(?:\|([^}]+))?\}\}'
    tokens = re.findall(pattern, body)
    for slug in {slug for slug, _ in tokens}:
        modes = [mode for name, mode in tokens if name == slug]
        if modes != [''] and modes != ['example', 'failure']:
            raise ValueError('Split notebook requires one example token followed by one failure token')
    return re.sub(pattern, lambda m: render_notebook(lab, m[1], m[2]), body)
