import csv, os, sys
ROOT=os.path.expanduser('~/mnt/한국경제신문')
TMPDIR=os.environ.get('TMPDIR','/tmp').rstrip('/')
HOME=os.path.expanduser('~')
EXCLUDE={'labs/part7/ch31-database/.venv','.cache/vm/pgdata','.cache/vm/pgenv'}
rows=list(csv.reader(open(os.path.join(ROOT,'textbook/qa/deletion-manifest-2026-10-01.tsv')),delimiter='\t'))[1:]
plan=[];skipped=[];bad=[];missing=[]
for r in rows:
    kind,path=r[0],r[1]
    if kind=='connected':
        if path in EXCLUDE or path.startswith('.cache/vm/pgenv') or path.startswith('.cache/vm/pgdata'):
            skipped.append(path);continue
        if path.startswith('/') or '..' in path.split('/') or path in ('','.') : bad.append(path);continue
        top=path.split('/')[0]
        if top in ('.env','.git','.moai') or path.startswith('textbook/downloads') or '/qa/upgrade/before' in path or '/review-pack' in path or '/probe/' in path and not path.endswith('.tmp'):
            bad.append(path);continue
        full=os.path.join(ROOT,path)
    else:
        full=os.path.expanduser(path)
        if not (full.startswith('/tmp/') or full.startswith(TMPDIR+'/') or full.startswith(HOME+'/ch16work')):
            bad.append(path);continue
        if full.rstrip('/') in ('/tmp',TMPDIR,HOME): bad.append(path);continue
    if not os.path.lexists(full): missing.append(path);continue
    plan.append(full)
open(os.path.join(ROOT,'.cache/final-close/7-delete/plan.txt'),'w').write('\n'.join(plan)+'\n')
print('rows',len(rows),'plan',len(plan),'skipped',skipped,'bad',len(bad),'missing',len(missing))
for b in bad[:20]: print('BAD',b)
for m in missing[:10]: print('MISSING',m)
