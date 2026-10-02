"""Verify current continuity artifacts, preserved execution state and ZIP freshness."""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import tarfile
import tomllib
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = Path(__file__).parent / 'continuity-evidence'
sys.path.insert(0, str(ROOT / 'textbook/_notebook'))
from render import validate, validate_parts
from verify import verify_lesson


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    before = json.loads((EVIDENCE / 'notebook-before-invariants.json').read_text())
    changed, preserved, refreshed = [], [], []
    for record in before:
        nb = json.loads((ROOT / record['path']).read_text())
        validate(nb)
        validate_parts(nb)
        notebook_path = Path(record["path"])
        chapter_html = ROOT / "textbook" / notebook_path.parts[1] / notebook_path.parts[2] / (notebook_path.stem + ".html")
        verify_lesson(ROOT / notebook_path, chapter_html)
        codes = [cell for cell in nb['cells'] if cell['cell_type'] == 'code']
        sources = [cell['source'] for cell in codes]
        lab = (ROOT / record['path']).parent.parent
        locked = {row['name']: row['version'] for row in tomllib.loads((lab / 'uv.lock').read_text())['package']}
        assert locked.get('ipykernel') == '7.3.0'
        for cell in codes:
            cell_source = ''.join(cell['source'])
            if '%pip' in cell_source:
                assert locked.get('pip') == '26.2'
                for name, version in re.findall(r'([A-Za-z0-9_.-]+)(?:\[[^\]]+\])?==([0-9][A-Za-z0-9_.+-]*)', cell_source):
                    assert locked.get(name.lower().replace('_', '-')) == version, (record['path'], name, version)

        # Compare normalized source representation: nbformat may serialize as lines.
        text = lambda values: [''.join(value) if isinstance(value, list) else value for value in values]
        same_code = text(sources) == text(record['source'])
        data_refresh = record['path'] == 'labs/part3/ch11-evaluation/notebooks/06-실험-로그와-자동-실행.ipynb'
        if same_code and not data_refresh:
            assert [cell.get('outputs', []) for cell in codes] == record['outputs'], record['path']
            assert [cell.get('execution_count') for cell in codes] == record['execution_counts'], record['path']
            assert nb.get('metadata', {}) == record['metadata'], record['path']
            preserved.append(record['path'])
        else:
            proof = nb['metadata']['verification']
            assert proof['fresh_kernel'] and proof['python_version'].startswith('3.12.')
            assert proof['executed_at'] > record['metadata']['verification']['executed_at']
            if same_code:
                refreshed.append({'path': record['path'], 'reason': 'Ch10 fresh retrieval log is evaluated as actual input', **proof})
            else:
                changed.append({'path': record['path'], **proof})

    part2_handoffs = []
    for chapter, filename in (("ch07-prompt-engineering", "prompt-ab-continuity.json"),
                              ("ch08-context-engineering", "context-design-continuity.json")):
        path = ROOT / "labs/part2" / chapter / "runs" / filename
        row = json.loads(path.read_text())
        source = row["source_record"]
        assert not Path(source["path"]).is_absolute()
        source_path = ROOT / source["path"]
        assert digest(source_path.read_bytes()) == source["sha256"]
        assert json.loads(source_path.read_text())["run_id"] == source["run_id"]
        assert any(p.read_bytes() == path.read_bytes() for p in (path.parent / "continuity").glob("*/" + filename))
        part2_handoffs.append({"path": str(path.relative_to(ROOT)), "run_id": row["run_id"], "source": source})

    evaluation = [json.loads(line) for line in (ROOT / 'labs/part3/ch11-evaluation/data/evaluation-queries.jsonl').read_text().splitlines() if line]
    tuning = json.loads((ROOT / 'labs/part3/ch12-retrieval-tuning/data/advanced-queries.json').read_text())
    assert evaluation == tuning, 'Ch11/Ch12 query, gold or split drift'
    ids = [row['qid'] for row in evaluation]
    assert len(ids) == len(set(ids)) == 30
    splits = {name: [r['qid'] for r in evaluation if r['split'] == name] for name in ('dev', 'test')}
    assert len(splits['dev']) == len(splits['test']) == 15
    assert set(splits['dev']).isdisjoint(splits['test'])
    documents = json.loads((ROOT / 'labs/part3/ch12-retrieval-tuning/data/advanced-documents.json').read_text())
    parents = {item['doc_id'] for item in documents['parents']}
    assert all(set(item['gold_doc_ids']) <= parents for item in evaluation)
    assert all(item['parent_id'] in parents and item['page'] >= 1 for item in documents['chunks'])
    assert len({item['chunk_id'] for item in documents['chunks']}) == len(documents['chunks'])

    by_id = {row['qid']: row for row in evaluation}
    handoffs = []
    for name in ('ch09-rag-first-run/runs/continuity-ch09-search.jsonl',
                 'ch10-document-processing/runs/continuity-ch10-indexing.jsonl'):
        path = ROOT / 'labs/part3' / name
        rows = [json.loads(line) for line in path.read_text().splitlines() if line]
        assert rows
        for row in rows:
            query = by_id[row['qid']]
            assert row['question'] == query['question']
            assert row['gold_doc_ids'] == query['gold_doc_ids']
            assert query['split'] == 'dev'
            assert row['source_run_id'] and row['config']
            assert not ({'qid', 'question', 'gold_doc_ids'} & set(row['config'])), 'Labels must be separate from retrieval settings'
            assert row['retrieved']
            assert [hit['rank'] for hit in row['retrieved']] == list(range(1, len(row['retrieved']) + 1))
            assert all(hit['doc_id'] and hit['chunk_id'] and hit['page'] >= 1 for hit in row['retrieved'])
            if row['source_chapter'] == 'ch09':
                citations = re.findall(r'\[([A-Z][0-9]+) p\.(\d+)\]', row['answer'])
                actual_sources = {(hit['doc_id'], str(hit['page'])) for hit in row['retrieved']}
                assert citations and set(citations) <= actual_sources, 'Ch9 answer source must reference retrieved pages'
        handoffs.append({'path': str(path.relative_to(ROOT)), 'rows': len(rows), 'sha256': digest(path.read_bytes())})

    run_root = ROOT / 'labs/part3/ch12-retrieval-tuning/runs'
    experiments = [json.loads(line) for line in (run_root / 'advanced-continuity-experiment-log.jsonl').read_text().splitlines() if line]
    test = json.loads((run_root / 'advanced-continuity-test-result.json').read_text())
    integrated = json.loads((run_root / 'advanced-continuity-integrated-result.json').read_text())
    assert len(experiments) == 36
    runs = {row['run_id']: row for row in experiments}
    assert len(runs) == 36 and test['selected_run_id'] in runs
    assert test['settings'] == runs[test['selected_run_id']]['settings']
    chunks = {row['chunk_id']: row for row in documents['chunks']}
    metric_names = ('recall_at_5', 'recall_at_50', 'precision_at_5', 'ndcg_at_5')
    for run in experiments + [test]:
        assert run['source_chapter'].lower() == 'ch12' and run['run_date']
        assert run['settings']['candidate_unit'] == 'chunk'
        assert run['settings']['report_unit'] == 'unique-parent-document'
        assert run['metrics_policy'] == 'chunk-candidate-unique-parent-macro-v1'
        assert run['query_count'] == 15 and run['excluded_query_count'] == 0
        assert len(run['results']) == 15
        assert {row['qid'] for row in run['results']} == set(splits[run['split']])
        assert run['corpus_fingerprint'] == experiments[0]['corpus_fingerprint']
        assert run['query_fingerprint'] == experiments[0]['query_fingerprint']
        for row in run['results']:
            query = by_id[row['qid']]
            assert row['split'] == query['split'] and row['gold_doc_ids'] == query['gold_doc_ids']
            hits = row['top_results']
            assert row['returned_count'] == len(hits)
            assert [hit['rank'] for hit in hits] == list(range(1, len(hits) + 1))
            for hit in hits:
                chunk = chunks[hit['chunk_id']]
                assert hit['doc_id'] == chunk['parent_id'] and hit['page'] == chunk['page']
            top = list(dict.fromkeys(hit['doc_id'] for hit in hits))[:5]
            gold = set(query['gold_doc_ids'])
            ideal = sum(1 / math.log2(i + 2) for i in range(min(5, len(gold))))
            expected = {
                'recall_at_5': len(gold & set(top)) / len(gold),
                'recall_at_50': len(gold & set(row['candidate_doc_ids'])) / len(gold),
                'precision_at_5': len(gold & set(top)) / 5,
                'ndcg_at_5': sum((doc in gold) / math.log2(i + 2) for i, doc in enumerate(top)) / ideal,
            }
            assert all(math.isclose(row[name], value, abs_tol=1e-10) for name, value in expected.items()), row['qid']
        groups = [(run['results'], run['metrics'])] + [
            ([row for row in run['results'] if row['tier'] == tier], values)
            for tier, values in run['slices'].items()
        ]
        assert set(run['slices']) == {'easy', 'medium', 'hard'}
        for rows, metrics in groups:
            assert rows and all(math.isclose(metrics[name], sum(row[name] for row in rows) / len(rows), abs_tol=1e-10) for name in metric_names)
    for filename in ('advanced-continuity-experiment-log.jsonl', 'advanced-continuity-test-result.json', 'advanced-continuity-integrated-result.json'):
        snapshots = list((run_root / 'continuity').glob('*/' + filename))
        assert any(path.read_bytes() == (run_root / filename).read_bytes() for path in snapshots), 'Current tuning log has no immutable snapshot'
    query = by_id[integrated['qid']]
    assert query['split'] == integrated['split'] == 'dev'
    assert integrated['question'] == query['question'] and integrated['gold_doc_ids'] == query['gold_doc_ids']
    assert integrated['retrieval_metrics'] is None and integrated['generation_evaluation']['status'] == 'not_evaluated'
    sources = {(hit['doc_id'], str(hit['page'])) for hit in integrated['retrieved']}
    citations = re.findall(r'\[([A-Z][0-9]+) p\.(\d+)\]', integrated['response'])
    assert citations and set(citations) <= sources

    originals = json.loads((EVIDENCE / 'before-manifest.json').read_text())
    logs = [entry for entry in originals if entry['path'].startswith('labs/') and '/runs/' in entry['path']]
    original_log_bytes_unchanged, refreshed_aliases = [], []
    with tarfile.open(EVIDENCE / 'full-course-before.tar.gz') as snapshot:
        for entry in logs:
            current = ROOT / entry['path']
            if digest(current.read_bytes()) == entry['sha256']:
                original_log_bytes_unchanged.append(entry['path'])
                continue
            # Current aliases may refresh only when their original runs remain immutable.
            assert entry['path'].startswith(('labs/part3/ch12-retrieval-tuning/runs/advanced-continuity-', 'labs/part3/ch12-retrieval-tuning/runs/core-')) or entry['path'] == 'labs/part3/ch10-document-processing/runs/continuity-ch10-indexing.jsonl', entry['path']
            original = snapshot.extractfile(entry['path']).read()
            assert digest(original) == entry['sha256']
            if entry['path'].endswith('continuity-ch10-indexing.jsonl'):
                snapshots = current.parent / 'continuity'
                originals = [json.loads(line) for line in original.decode().splitlines() if line]
                for row in originals:
                    saved = snapshots / (row['source_run_id'] + '.jsonl')
                    assert json.loads(saved.read_text()) == row, f"Original source run lost: {saved}"
                preserved_paths = [str((snapshots / (row['source_run_id'] + '.jsonl')).relative_to(ROOT)) for row in originals]
            else:
                candidates = ((run_root / 'core-history').glob('before-*-' + current.name)
                              if current.name.startswith('core-') else (run_root / 'continuity').glob('*/' + current.name))
                matches = [path for path in candidates
                           if path.read_bytes() == original]
                assert matches, f"Original execution lost: {entry['path']}"
                preserved_paths = [str(matches[0].relative_to(ROOT))]
            refreshed_aliases.append({'path': entry['path'], 'preserved_original': preserved_paths})

    archives = []
    for name in ('part1-practice.zip', 'part2-practice.zip', 'part3-practice.zip', 'llm-practice.zip'):
        path = ROOT / 'textbook/downloads' / name
        with ZipFile(path) as archive:
            assert archive.testzip() is None
            prefix = archive.namelist()[0].split('/')[0] + '/'
            manifest = json.loads(archive.read(prefix + 'manifest.json'))
            entries = {entry['path'] for entry in manifest}
            for entry in manifest:
                data = archive.read(prefix + entry['path'])
                assert digest(data) == entry['sha256']
                assert data == (ROOT / entry['path']).read_bytes(), f'Stale archive: {name}/{entry["path"]}'
            if name in ('part3-practice.zip', 'llm-practice.zip'):
                assert all(item['path'] in entries for item in handoffs)
                assert 'labs/part3/continuity-guide.md' in entries
                assert 'labs/part3/ch11-evaluation/evaluate.py' in entries
            archives.append({'path': str(path.relative_to(ROOT)), 'files': len(manifest), 'sha256': digest(path.read_bytes())})
    assert len(changed) + len(preserved) + len(refreshed) == 87
    assert integrated['settings']['dimensions'] == 256 and integrated['settings']['chat'] == 'gpt-5.4-mini'
    report = {'data_driven_fresh_executions': refreshed, 'changed_code_fresh_executions': changed, 'code_output_metadata_preserved': preserved,
              'part2_handoffs': part2_handoffs, 'question_sets_identical': True, 'splits': splits, 'handoffs': handoffs,
              'archives_current': archives, 'original_logs_preserved': len(logs), 'original_log_bytes_unchanged': original_log_bytes_unchanged, 'refreshed_current_aliases': refreshed_aliases,
              'tuning_runs_recomputed': len(experiments) + 1, 'tuning_question_results_recomputed': 555,
              'integrated_generation_evaluated': False}
    (EVIDENCE / 'course-static-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({'fresh_notebooks': len(changed) + len(refreshed), 'preserved_notebooks': len(preserved),
                      'handoff_rows': sum(item['rows'] for item in handoffs), 'archives': len(archives)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
