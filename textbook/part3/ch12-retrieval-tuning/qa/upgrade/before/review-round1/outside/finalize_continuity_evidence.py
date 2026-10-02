"""Bind visual and extracted execution evidence to the final delivery files."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = Path(__file__).parent / 'continuity-evidence'
visual = []
for chapter in ('ch08-context-engineering', 'ch09-rag-first-run', 'ch10-document-processing', 'ch11-evaluation', 'ch12-retrieval-tuning', 'part3'):
    path = ROOT / 'textbook/_notebook/checks' / chapter / 'visual-results.json'
    rows = json.loads(path.read_text())
    assert all(row['passed'] for row in rows)
    visual.extend({'chapter': chapter, **row} for row in rows)
# 행 수 = ch08 14 + ch09 16 + ch10 20 + ch11 16 + ch12 26 + part3 2.
# 2026-09-18: Ch 10 에 실습 절 09 를 붙여 ch10 이 18 → 20 이 되었다(공용 visual.cjs 재실행, 20/20 PASS).
# 2026-09-18: Ch 11 에 실습 절 07 을 붙여 ch11 을 8 쪽으로 다시 찍었다(14 → 16, 16/16 PASS).
# ch09 16 은 Ch 9 실습 절 07 몫이고 아직 14 다 — 전체 마감 때 ch09 HTML 을 visual.cjs 로 다시 찍어야 이 검사가 지나간다.
# 이 값을 92 나 90 으로 내리지 마세요(ch10 20 행·ch11 16 행을 버립니다).
assert len(visual) == 94, len(visual)
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
