"""Bind visual and extracted execution evidence to the final delivery files.

전체 마감 2026-10-01: 화면 기록 행 수 고정값 94(실습 절이 붙기 전 쪽 수가 섞인 값)를 지금 구조에 맞게 고침 —
폴더마다 지금 공개 HTML 쪽 × 두 너비(1280·390)가 모두 기록돼 있어야 하고, 합은 98(ch08 16 + ch09 16 + ch10 20 +
ch11 16 + ch12 28 + part3 2)이다. ch08(07 실습 쪽 빠짐, 2026-09-14 기록)·ch09(07 실습 쪽 빠짐)를 다시 찍기 전에는
아래 visual 블록에서 멈추는 것이 맞다(다음 단계 화면 재촬영 뒤 통과).
"""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = Path(__file__).parent / 'continuity-evidence'
PAGES = {'ch08-context-engineering': 'textbook/part2/ch08-context-engineering',
         'ch09-rag-first-run': 'textbook/part3/ch09-rag-first-run',
         'ch10-document-processing': 'textbook/part3/ch10-document-processing',
         'ch11-evaluation': 'textbook/part3/ch11-evaluation',
         'ch12-retrieval-tuning': 'textbook/part3/ch12-retrieval-tuning',
         'part3': 'textbook/part3'}
visual = []
for chapter, folder in PAGES.items():
    path = ROOT / 'textbook/_notebook/checks' / chapter / 'visual-results.json'
    rows = json.loads(path.read_text())
    assert all(row['passed'] for row in rows)
    pages = {page.name for page in (ROOT / folder).glob('*.html')}
    expected = {(page, width) for page in pages for width in (1280, 390)}
    recorded = {(row['file'], row['width']) for row in rows}
    assert recorded == expected and len(rows) == len(expected), (chapter, sorted(expected - recorded), sorted(recorded - expected))
    visual.extend({'chapter': chapter, **row} for row in rows)
# 이력: 2026-09-18 ch10 18 → 20(실습 절 09) · ch11 14 → 16(실습 절 07) · 2026-09-19 ch12 26 → 28(실습 절 13).
# 옛 고정값 94는 ch08·ch09 기록에 실습 쪽이 빠진 채 맞아떨어진 값이었다. 98을 94·96 등으로 내리지 마세요.
# 전체 마감 순서: (1) part1·part2·part3·llm 묶음 재생성 → (2) part3/qa/run_continuity_bundle.py →
# (3) 공용 visual.cjs 로 ch08·ch09 8 쪽씩 재촬영(각 14 → 16) → (4) 이 스크립트 실행 →
# (5) part3/qa/check_continuity.py 와 qa/check_course_continuity.py 를 끝까지 → (6) part3/_build_index.py 로 Part 3 목차.
assert len(visual) == 98, len(visual)
(EVIDENCE / 'visual-results.json').write_text(json.dumps(visual, ensure_ascii=False, indent=2))

path = EVIDENCE / 'bundle-execution-results.json'
report = json.loads(path.read_text())
original = {row['path']: row['sha256'] for row in json.loads((Path(report['temporary_extraction']) / 'manifest.json').read_text())}
archive_path = ROOT / 'textbook/downloads/part3-practice.zip'
with ZipFile(archive_path) as archive:
    final = json.loads(archive.read('part3-practice/manifest.json'))
    changed = [row['path'] for row in final if row['sha256'] != original.get(row['path'])]
    # The smoke execution uses these three notebooks, their project files, the
    # evaluator and the corpus. Other Ch11 lessons are not execution dependencies.
    smoke_lessons = {row['notebook'] for row in report['notebooks']}
    def execution_input(name):
        if name.endswith('.md'):
            return False
        if name.startswith('labs/data/') or name in smoke_lessons:
            return True
        for chapter in ('ch09-rag-first-run', 'ch10-document-processing', 'ch11-evaluation'):
            prefix = 'labs/part3/' + chapter + '/'
            if name.startswith(prefix) and '/notebooks/' not in name:
                return True
        return False
    assert not any(execution_input(name) for name in changed), changed
    report['final_archive_sha256'] = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    report['final_archive_changed_files_since_execution'] = changed
    report['final_archive_execution_inputs_identical'] = True
evidence_runs = EVIDENCE / 'bundle-execution'
source_ids = []
for chapter, name in (('ch09-rag-first-run', 'continuity-ch09-search.jsonl'), ('ch10-document-processing', 'continuity-ch10-indexing.jsonl')):
    source_ids.extend(json.loads(line)['source_run_id'] for line in (evidence_runs / chapter / 'runs' / name).read_text().splitlines() if line)
latest = max((evidence_runs / 'ch11-evaluation/runs').glob('continuity-upstream-*.json'), key=lambda item: item.stat().st_mtime)
evaluation = json.loads(latest.read_text())
assert len(source_ids) == 7 and set(source_ids) == {run['run_id'] for run in evaluation['runs']}
for run in evaluation['runs']:
    assert run['query_ids'] == ['Q001']
    metrics = run['metrics']
    assert metrics['recall_at_50'] is None and metrics['recall_at_logged_candidates'] == 1
    if run['source_chapter'] == 'ch09':
        assert all(metrics[key] is None for key in ('recall_at_5', 'precision_at_5', 'ndcg_at_5'))
    else:
        assert metrics['recall_at_5'] == 1 and metrics['precision_at_5'] == .2 and metrics['ndcg_at_5'] == 1
report['fresh_handoff_source_run_ids'] = source_ids
report['fresh_handoff_evaluated_runs'] = 7
report['cutoff_policy_verified'] = True
report['evaluation_evidence'] = str(latest.relative_to(ROOT))
path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
print(json.dumps({'visual_checks': len(visual), 'execution_inputs_preserved': True, 'changed_non_execution_files': changed}, ensure_ascii=False))
